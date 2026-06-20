# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg1Slots.py -- f10 Seg-1 (0x08079e60..0x0807ae84)
#   enqueue_neo_daedalus_zone_oam_on_available_slot .. tick_equip_zone_match_lp_row_type11
#   19 functions; 61 auto-name slots (47 EQ + 9 RENAME + 5 REF)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (43 reuse + 4 new)
#   B. RENAME_SLOTS -- plain rename + EOL (gP1LifePoints already-symbolic slots)
#   C. REF_SLOTS  -- USER label on ROM_INCBIN entry bases
#
# NEW constants (must be in .inc before pipeline):
#   NEO_DAEDALUS_OAM_SPRITE_BASE = 0x180d  (equip_lp_delta.inc)
#   CARD_DISPLAY_OP_ID_137       = 0x137   (duel_field.inc)
#   EQUIP_PAIRED_SLOT_PRED       = 0x181e  (duel_field.inc)
#   MAGICIANS_CIRCLE_CID         = 0x1818  (card_info.inc)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- enqueue_neo_daedalus_zone_oam_on_available_slot ---
    (0x08079ebc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_neodaed_zone_oam_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x08079ec0, 0x0201c600, 'gP1FieldArrayCBase',
     'enqueue_neodaed_zone_oam_field_array_c_base',
     'gP1FieldArrayCBase: field array C zone slot array base ptr'),

    # --- apply_partner_flags_on_equip_pair_slot_count_hit ---
    (0x08079f44, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_partner_flags_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x08079f48, 0x0201c510, 'gDuelFieldSlots',
     'apply_partner_flags_duel_field_slots',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- enqueue_equip_sprite_and_red_eyes_lp_indicator ---
    (0x0807a134, 0x00000ff8, 'RED_EYES_B_DRAGON_CID',
     'enqueue_red_eyes_lp_indicator_cid',
     'RED_EYES_B_DRAGON_CID=0xff8: Red-Eyes B. Dragon CID guard'),

    # --- dispatch_face_down_and_lp_counter_sprite_by_state ---
    (0x0807a32c, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_face_down_lp_counter_duel_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807a384, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_face_down_lp_counter_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),

    # --- dispatch_neo_daedalus_equip_sprite_by_monster_count ---
    (0x0807a5d4, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_neodaed_sprite_duel_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807a608, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'dispatch_neodaed_sprite_equip_phase_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect phase frame counter'),
    (0x0807a640, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'dispatch_neodaed_sprite_equip_phase_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in state-0x7f branch'),
    (0x0807a644, 0x0000180d, 'NEO_DAEDALUS_OAM_SPRITE_BASE',
     'dispatch_neodaed_sprite_oam_attr_base',
     'NEO_DAEDALUS_OAM_SPRITE_BASE=0x180d: OAM attr2 base ORed with player_id<<13'),

    # --- enqueue_slot_sprite_on_zone_count_and_state_code ---
    (0x0807a8e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_slot_sprite_zone_count_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807a8ec, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_slot_sprite_zone_count_duel_field_slots',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- tick_hand_effect_node_match_display_seq ---
    (0x0807a98c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_hand_effect_node_match_duel_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807a994, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_hand_effect_node_match_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807a998, 0x000012a1, 'zone_query_hand_tag_12a1',
     'tick_hand_effect_node_match_zone_query_tag',
     'zone query node-type tag for find_effect_node_in_zone (hand zone=0xb); NOT PARASITE_PARACIDE_CID'),

    # --- dispatch_equip_banisher_activation_by_state ---
    (0x0807aa14, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_banisher_activation_duel_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807aa18, 0x0201bb90, 'gEquipChainSlotRefs',
     'dispatch_banisher_activation_equip_chain_slot_refs',
     'gEquipChainSlotRefs: equip chain slot reference array'),
    (0x0807aa1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_banisher_activation_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807aa20, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_banisher_activation_duel_field_slots',
     'gDuelFieldSlots: duel field zone slot array base'),
    (0x0807aa24, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF',
     'dispatch_banisher_activation_display_seq_player_off',
     'DISPLAY_SEQ_ACTIVE_PLAYER_OFF=0x1d10: [gP1LifePoints+0x1d10] active player field'),
    (0x0807aa44, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_banisher_activation_duel_card_ctx_base',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x0807aa48, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF',
     'dispatch_banisher_activation_display_seq_player_off_b',
     'DISPLAY_SEQ_ACTIVE_PLAYER_OFF=0x1d10: dup in branch'),
    (0x0807aa58, 0x00000137, 'CARD_DISPLAY_OP_ID_137',
     'dispatch_banisher_activation_display_op_id',
     'CARD_DISPLAY_OP_ID_137=0x137: op-id arg to invoke_card_display_op_0x31_sub1'),
    (0x0807aa7c, 0x0201bb90, 'gEquipChainSlotRefs',
     'dispatch_banisher_activation_equip_chain_refs_b',
     'gEquipChainSlotRefs: dup reference'),
    (0x0807aa94, 0x0201bb90, 'gEquipChainSlotRefs',
     'dispatch_banisher_activation_equip_chain_refs_c',
     'gEquipChainSlotRefs: dup reference'),

    # --- dispatch_equip_prng_lp_row_and_bitmap_by_state ---
    (0x0807aab4, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_equip_prng_lp_row_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807aae4, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_equip_prng_lp_row_card_ctx_base',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x0807ab50, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'dispatch_equip_prng_lp_row_track_next_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] LP card-ref tracking array next'),
    (0x0807ab54, 0x0201bb90, 'gEquipChainSlotRefs',
     'dispatch_equip_prng_lp_row_chain_refs',
     'gEquipChainSlotRefs: equip chain slot reference array'),

    # --- dispatch_banisher_lp_penalty_by_field_count ---
    (0x0807abb0, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_banisher_lp_penalty_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807abb8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_banisher_lp_penalty_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807ac10, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'dispatch_banisher_lp_penalty_banisher_cid',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: Banisher of the Light card ID'),
    (0x0807ac18, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'dispatch_banisher_lp_penalty_track_base_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card-ref tracking array base'),

    # --- enqueue_equip_slot_bitmap_update_by_count ---
    (0x0807ac7c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_slot_bitmap_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807ac80, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_equip_slot_bitmap_duel_field_slots',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- enqueue_equip_sprite_on_zone_count_match ---
    (0x0807ad0c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_sprite_zone_match_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807ad10, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_equip_sprite_zone_match_duel_field_slots',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- tick_paired_slot_counter_update ---
    (0x0807ad4c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_paired_slot_counter_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807ad50, 0x0000181e, 'EQUIP_PAIRED_SLOT_PRED',
     'tick_paired_slot_counter_paired_slot_pred',
     'EQUIP_PAIRED_SLOT_PRED=0x181e: predicate for count_equipped_paired_slots_for_player'),
    (0x0807ad54, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_paired_slot_counter_phase_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect phase frame counter'),
    (0x0807ad78, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_paired_slot_counter_phase_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in state-0x7f branch'),

    # --- tick_equip_zone_match_lp_row_type11 ---
    (0x0807ae2c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_match_lp_row_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807ae30, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_match_lp_row_player_block_stride',
     'PLAYER_BLOCK_STRIDE(0x868) byte stride between P1/P2 data blocks'),
    (0x0807ae34, 0x0201c510, 'gDuelFieldSlots',
     'tick_equip_zone_match_lp_row_duel_field_slots',
     'gDuelFieldSlots: duel field zone slot array base'),
    (0x0807ae7c, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'tick_equip_zone_match_lp_row_track_next_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] LP card-ref tracking array next'),
    (0x0807ae80, 0x00001ce4, 'LP_D_TRIBE_BLOCK_OFF',
     'tick_equip_zone_match_lp_row_d_tribe_off',
     'LP_D_TRIBE_BLOCK_OFF=0x1ce4: [gP1LifePoints+0x1ce4] D.Tribe LP score field'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Slots already contain .word gP1LifePoints -- value already symbolic.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0807a380, 'lp_state_base_a380',
     '.word gP1LifePoints: LP state struct base ptr in dispatch_face_down_and_lp_counter_sprite_by_state'),
    (0x0807a990, 'player_life_ptr_a990',
     '.word gP1LifePoints: tick_hand_effect_node_match_display_seq LP ptr'),
    (0x0807aa78, 'player_life_ptr_aa78',
     '.word gP1LifePoints: dispatch_equip_banisher_activation_by_state LP ptr'),
    (0x0807aae8, 'player_life_ptr_aae8',
     '.word gP1LifePoints: dispatch_equip_prng_lp_row_and_bitmap_by_state LP ptr A'),
    (0x0807ab14, 'player_life_ptr_ab14',
     '.word gP1LifePoints: dispatch_equip_prng_lp_row_and_bitmap_by_state LP ptr B'),
    (0x0807ab4c, 'player_life_ptr_ab4c',
     '.word gP1LifePoints: dispatch_equip_prng_lp_row_and_bitmap_by_state LP ptr C'),
    (0x0807abb4, 'player_life_ptr_abb4',
     '.word gP1LifePoints: dispatch_banisher_lp_penalty_by_field_count LP ptr'),
    (0x0807ac14, 'player_life_ptr_ac14',
     '.word gP1LifePoints: dispatch_banisher_lp_penalty_by_field_count LP ptr B'),
    (0x0807ae78, 'player_life_ptr_ae78',
     '.word gP1LifePoints: tick_equip_zone_match_lp_row_type11 state-0x7f LP ptr'),
]

# ---------------------------------------------------------------------------
# C. REF_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    ROM_INCBIN entry base labels + dispatch table label rename.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0807a00c, 'equip_sprite_zone_type_stubs',
     'R4 disasm entry base: BLK2 zone-type equip sprite dispatch sub-stubs (7 entries)'),
    (0x0807a178, 'equip_sprite_red_eyes_stubs',
     'R4 disasm entry base: BLK4 Red-Eyes LP routing dispatch sub-stubs (6 entries)'),
    (0x0807a464, 'equip_sprite_player_stubs',
     'R4 disasm entry base: BLK6 player-type equip sprite dispatch sub-stubs (6 entries)'),
    (0x0807a6d0, 'equip_sprite_capacity_jump_table',
     'BLK8 dispatch jump table: 19 .word entries for zone-capacity equip sprite routing'),
    (0x0807a71c, 'equip_sprite_capacity_stubs',
     'R4 disasm entry base: BLK8 zone-capacity equip sprite dispatch sub-stubs (8 entries)'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF10Seg1Slots (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = 0

    # ---- A: EQ_SLOTS ----
    for slot_int, value, cname, label, eol in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        if eol:
            listing.setComment(_addr(slot_int), CodeUnit.EOL_COMMENT, eol)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # ---- B: RENAME_SLOTS ----
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x rename %s" % (slot_int, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.setComment(_addr(slot_int), CodeUnit.EOL_COMMENT, eol)
        print("[B ok] 0x%08x -> %s" % (slot_int, label))
        nB += 1

    # ---- C: REF_SLOTS ----
    for slot_int, label, eol in REF_SLOTS:
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        a = _addr(slot_int)
        createLabel(a, label, True, SourceType.USER_DEFINED)
        if eol:
            listing.setComment(a, CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label))
        nC += 1

    print("=== Done: A=%d B=%d C=%d ===" % (nA, nB, nC))


main()
