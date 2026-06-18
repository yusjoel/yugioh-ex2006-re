# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg1Slots.py -- F09 Seg-1 (0x0806e76c..0x0806ff50)
#   enqueue_slot_sprite_type11 + dispatch_equip_zone_token/lp + state machine cluster (20 fn)
#   EQ=40 (33 reuse + 7 NEW: BIG_MARCH_OF_ANIMALS_CID / CREATURE_SWAP_CID /
#           ICID_RESERVED_D / ICID_RESERVED_E / LP_D_TRIBE_BLOCK_OFF /
#           LP_P2_LOOP_CEIL_OFF / OAM_EQUIP_SPRITE_P2_1A)
#   REF=34
#   RENAME=3 (DAT_0806f054/fa08/fe88 -> eligible_sub_stubs_*)
#   FUNC_RENAME=0
#   PLATE=2:
#     dispatch_equip_zone_token_or_lp_sprite_by_slot_type @ 0x0806e840 (asm/09 L148):
#       FUN_0806e898 -> dispatch_equip_chain_state_sprite_by_slot
#     dispatch_equip_chain_state_sprite_by_slot @ 0x0806e898 (asm/09 L207):
#       (gP1LifePoints) -> (gDuelPhaseFlags)  [WARN/not-found treated as FAIL]
#
# NEW constants added to constants/*.inc before running:
#   card_info.inc: BIG_MARCH_OF_ANIMALS_CID=0x1882, CREATURE_SWAP_CID=0x142a,
#                  ICID_RESERVED_D=0x144c, ICID_RESERVED_E=0x1452
#   ewram.inc:     LP_D_TRIBE_BLOCK_OFF=0x1ce4, LP_P2_LOOP_CEIL_OFF=0x874
#   oam_attr.inc:  OAM_EQUIP_SPRITE_P2_1A=0x801a
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_194628-pre-F09Seg1

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    40 slots total
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- enqueue_slot_sprite_type11_with_card_id (0x6e76c..0x6e77e) ----
    # (no literal pool slots in this function)

    # ---- enqueue_slot_sprites_by_card_id_scoring (0x6e780..0x6e83e) ----
    # PYRAMID_ENERGY_CID = 0x153d (reuse card_info.inc)
    (0x0806e7b0, 0x0000153d, 'PYRAMID_ENERGY_CID', 'pyramid_energy_cid_e7b0',
     'PYRAMID_ENERGY_CID=0x153d: pw=36553614; enqueue_slot_sprites_by_card_id_scoring scoring branch'),

    # LIMITER_REMOVAL_CID = 0x1409 (reuse card_info.inc)
    (0x0806e7b4, 0x00001409, 'LIMITER_REMOVAL_CID', 'limiter_removal_cid_e7b4',
     'LIMITER_REMOVAL_CID=0x1409: pw=23171610; enqueue_slot_sprites_by_card_id_scoring scoring branch'),

    # D_TRIBE_CID = 0x15ae (reuse card_info.inc)
    (0x0806e7c8, 0x000015ae, 'D_TRIBE_CID', 'd_tribe_cid_e7c8', None),

    # BIG_MARCH_OF_ANIMALS_CID = 0x1882 (NEW card_info.inc)
    (0x0806e7cc, 0x00001882, 'BIG_MARCH_OF_ANIMALS_CID', 'big_march_cid_e7cc',
     'BIG_MARCH_OF_ANIMALS_CID=0x1882: The Big March of Animals (card_1795 pw=01689516); enqueue_slot_sprites_by_card_id_scoring scoring branch; conf:high'),

    # gP1LifePoints = 0x0201c4e0 (reuse ewram.inc)
    (0x0806e7fc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_e7fc', None),

    # LP_D_TRIBE_BLOCK_OFF = 0x1ce4 (NEW ewram.inc)
    (0x0806e800, 0x00001ce4, 'LP_D_TRIBE_BLOCK_OFF', 'lp_d_tribe_off_e800',
     'LP_D_TRIBE_BLOCK_OFF=0x1ce4: [gP1LifePoints+0x1ce4] D.Tribe LP score field; enqueue_slot_sprites_by_card_id_scoring D_TRIBE_CID path; conf:med'),

    # EQUIP_SLOT_SCORE_CAP = 0xffff (reuse oam_attr.inc)
    (0x0806e7e8, 0x0000ffff, 'EQUIP_SLOT_SCORE_CAP', 'score_cap_e7e8',
     'EQUIP_SLOT_SCORE_CAP=0xffff: equip slot score saturation cap'),

    # ---- dispatch_equip_zone_token_or_lp_sprite_by_slot_type (0x6e840..0x6e896) ----
    # gP1LifePoints = 0x0201c4e0 (reuse ewram.inc)
    (0x0806e890, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_e890', None),

    # LP_ACTIVATION_LINK_FLAG_OFF = 0x10d0 (reuse ewram.inc)
    (0x0806e894, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'lp_link_flag_off_e894',
     'LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: base=gP1LifePoints; activation link flag'),

    # ---- dispatch_equip_chain_state_sprite_by_slot (0x6e898..0x6e9fe) ----
    # INSECT_IMITATION_CID = 0x140b (reuse card_info.inc)
    (0x0806e990, 0x0000140b, 'INSECT_IMITATION_CID', 'insect_imitation_cid_e990',
     'INSECT_IMITATION_CID=0x140b: Insect Imitation (pw=72094998); dispatch_equip_chain_state_sprite_by_slot dispatch'),

    # ---- dispatch_equip_zone_entry_activation_or_bitmap (0x6ea00..0x6ebd2) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806eab4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_eab4', None),
    (0x0806eb4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_eb4c', None),
    (0x0806ebd0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_ebd0', None),

    # ---- dispatch_equip_lp_display_by_state_and_ref (0x6ebd4..0x6ecae) ----
    # LP_CARD_TRACK_BASE_OFF = 0x1da8 (reuse ewram.inc)
    (0x0806ec60, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_ec60', None),

    # ---- tick_equip_zone_slot_sprite_display_state_machine (0x6ed20..0x6edd2) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806ed18, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_ed18', None),
    (0x0806ed64, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_ed64', None),

    # ---- invoke_equip_oam_setup_if_neo_daedalus_zone14_eligible (0x6edd4..0x6ee52) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806ee4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_ee4c', None),

    # ---- tick_zone_slot_indicator_display_seq (0x6ee54..0x6ef86) ----
    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc)
    (0x0806eedc, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_eedc', None),
    (0x0806ef7c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_ef7c', None),

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806eee4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_eee4', None),
    (0x0806ef38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_ef38', None),

    # gP1LifePoints = 0x0201c4e0 (reuse ewram.inc)
    (0x0806eee0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_eee0', None),
    (0x0806ef34, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ef34', None),

    # ---- submit_lp_indicator_if_tile_count_match (0x6ef88..0x6f1c6) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806f000, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f000', None),

    # ---- enqueue_zone_subentry_sprites_with_xy_split (0x6f2cc..0x6f38e) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806f2c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f2c4', None),

    # ---- dispatch_hand_card_slot_sprite_by_state_and_card_id (0x6f390..0x6f4fe) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806f388, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f388', None),

    # ICID_RESERVED_D = 0x144c (NEW card_info.inc)
    (0x0806f40c, 0x0000144c, 'ICID_RESERVED_D', 'icid_reserved_d_f40c',
     'ICID_RESERVED_D=0x144c: reserved internal CID; dispatch_hand_card_slot_sprite_by_state_and_card_id state 0x80 BST'),
    (0x0806f478, 0x0000144c, 'ICID_RESERVED_D', 'icid_reserved_d_f478',
     'ICID_RESERVED_D=0x144c: second slot in dispatch_hand_card_slot_sprite_by_state_and_card_id state 0x7e BST'),

    # ICID_RESERVED_E = 0x1452 (NEW card_info.inc)
    (0x0806f420, 0x00001452, 'ICID_RESERVED_E', 'icid_reserved_e_f420',
     'ICID_RESERVED_E=0x1452: reserved internal CID; sibling of ICID_RESERVED_D in same BST state 0x80'),
    (0x0806f48c, 0x00001452, 'ICID_RESERVED_E', 'icid_reserved_e_f48c',
     'ICID_RESERVED_E=0x1452: second slot; sibling of ICID_RESERVED_D in state 0x7e BST'),

    # ---- submit_equip_lp_indicators_if_zone_tile_count_matched (0x6f500..0x6f5a2) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806f58c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f58c', None),

    # ---- tick_lp_zone_sprite_display_seq (0x6f5f0..0x6f786) ----
    # gP1LifePoints = 0x0201c4e0 (reuse ewram.inc)
    (0x0806f654, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f654', None),

    # LP_P2_LOOP_CEIL_OFF = 0x874 (NEW ewram.inc)
    (0x0806f658, 0x00000874, 'LP_P2_LOOP_CEIL_OFF', 'lp_p2_loop_ceil_off_f658',
     'LP_P2_LOOP_CEIL_OFF=0x874: [gP1LifePoints+0x874] P2 LP loop ceil = PLAYER_BLOCK_STRIDE(0x868)+LP_LOOP_CEIL_OFF(0xc); tick_lp_zone_sprite_display_seq state 0x80; conf:high'),

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806f6b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f6b8', None),
    (0x0806f738, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f738', None),
    (0x0806f784, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f784', None),

    # LP_CARD_TRACK_BASE_OFF = 0x1da8 (reuse ewram.inc)
    (0x0806f6b4, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_f6b4', None),
    (0x0806f734, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_f734', None),

    # gP1LifePoints (2 more slots)
    (0x0806f6b0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f6b0', None),
    (0x0806f730, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f730', None),
    (0x0806f780, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f780', None),

    # ---- enqueue_hand_to_monster_slot_equip_sprite (0x6f788..0x6fb86) ----
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806f854, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_f854', None),

    # ---- tick_equip_chain_activation_display_seq (0x6fb88..0x6ff4f) ----
    # OAM_EQUIP_SPRITE_TILE_P2_1B = 0x801b (reuse oam_attr.inc)
    (0x0806fc9c, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'oam_sprite_p2_1b_fc9c', None),

    # LP_ACTIVATION_LINK_FLAG_OFF = 0x10d0 (reuse ewram.inc)
    (0x0806fc94, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'lp_link_flag_off_fc94', None),

    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x0806fc98, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_fc98', None),
    (0x0806fd48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_fd48', None),

    # gP1LifePoints = 0x0201c4e0 (reuse ewram.inc)
    (0x0806fc90, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_fc90', None),

    # OAM_SPRITE_CODE_P1_ACTIVATION = 0x8019 (reuse oam_attr.inc)
    (0x0806fdd4, 0x00008019, 'OAM_SPRITE_CODE_P1_ACTIVATION', 'oam_sprite_p1_act_fdd4', None),

    # OAM_EQUIP_SPRITE_P2_1A = 0x801a (NEW oam_attr.inc)
    (0x0806fda8, 0x0000801a, 'OAM_EQUIP_SPRITE_P2_1A', 'oam_sprite_p2_1a_fda8',
     'OAM_EQUIP_SPRITE_P2_1A=0x801a: equip sprite OAM attr0 P2 (bit15+0x1a); tick_equip_chain_activation_display_seq state 0x7f P2 path; sibling of OAM_EQUIP_SPRITE_TILE_P2_1B(0x801b) and OAM_SPRITE_CODE_P1_ACTIVATION(0x8019); 119 ROM refs; conf:high'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    34 slots total
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # ---- enqueue_slot_sprites_by_card_id_scoring ----
    (0x0806e7fc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_e7fc'),

    # ---- dispatch_equip_zone_token_or_lp_sprite_by_slot_type ----
    (0x0806e890, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_e890'),

    # ---- dispatch_equip_chain_state_sprite_by_slot ----
    (0x0806e8b8, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_e8b8'),
    (0x0806e8bc, 0x0806e8c0, 'switchD_0806e8b6__switchdataD_0806e8c0', 'switchtbl_e8bc'),

    # ---- dispatch_equip_zone_entry_activation_or_bitmap ----
    (0x0806eab8, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_eab8'),
    (0x0806eb44, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_eb44'),
    (0x0806eb48, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_eb48'),
    (0x0806eb7c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_eb7c'),

    # ---- dispatch_equip_lp_display_by_state_and_ref ----
    (0x0806ec00, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_ec00'),
    (0x0806ec5c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ec5c'),

    # ---- tick_equip_zone_slot_sprite_display_state_machine ----
    (0x0806ed1c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_ed1c'),
    (0x0806ed68, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_ed68'),
    (0x0806ed6c, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_ed6c'),

    # ---- invoke_equip_oam_setup_if_neo_daedalus_zone14_eligible ----
    (0x0806ee50, 0x0201c8f8, 'gP1HandSlotArray', 'gp1hand_ee50'),
    (0x0806ee80, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_ee80'),
    (0x0806eee0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_eee0'),
    (0x0806ef34, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ef34'),

    # ---- submit_lp_indicator_if_tile_count_match ----
    (0x0806f004, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_f004'),

    # ---- dispatch_dual_zone_equip_chain_sprite_by_state ----
    (0x0806f25c, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_f25c'),
    (0x0806f2c8, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_f2c8'),

    # ---- dispatch_hand_card_slot_sprite_by_state_and_card_id ----
    (0x0806f38c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_f38c'),
    (0x0806f3d8, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_f3d8'),

    # ---- submit_equip_lp_indicators_if_zone_tile_count_matched ----
    (0x0806f590, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_f590'),

    # ---- set_equip_player_state_bit_after_eligibility_refresh ----
    (0x0806f61c, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_f61c'),

    # ---- tick_lp_zone_sprite_display_seq ----
    (0x0806f654, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f654'),
    (0x0806f6b0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f6b0'),
    (0x0806f730, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f730'),
    (0x0806f780, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_f780'),

    # ---- enqueue_hand_to_monster_slot_equip_sprite ----
    (0x0806f858, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_f858'),

    # ---- tick_equip_chain_activation_display_seq ----
    (0x0806fbb0, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_fbb0'),
    (0x0806fc90, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_fc90'),
    (0x0806fd44, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_chain_refs_fd44'),
    (0x0806fd4c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_fd4c'),
    (0x0806fda4, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_chain_refs_fda4'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, old_label, new_label, eol_ascii_or_None)
#    3 entries -- block-start labels for disasm blocks
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0806f054, 'DAT_0806f054', 'eligible_sub_stubs_f054',
     'THUMB dispatch sub-functions for slot-sprite dispatch table'),
    (0x0806fa08, 'DAT_0806fa08', 'eligible_sub_stubs_fa08',
     'THUMB dispatch sub-functions for equip LP state dispatch table'),
    (0x0806fe88, 'DAT_0806fe88', 'eligible_sub_stubs_fe88',
     'THUMB dispatch sub-functions for equip chain activation dispatch table'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAMES: none
# ---------------------------------------------------------------------------
FUNC_RENAMES = []

# ---------------------------------------------------------------------------
# E. PLATE fixes (2 entries):
#    PLATE_SUBS: (func_addr, old_substr, new_substr)
#    Both WARN/not-found treated as FAIL (not silently skipped).
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # dispatch_equip_zone_token_or_lp_sprite_by_slot_type @ 0x0806e840 (asm/09 L148):
    #   FUN_0806e898 -> dispatch_equip_chain_state_sprite_by_slot
    (0x0806e840, 'FUN_0806e898', 'dispatch_equip_chain_state_sprite_by_slot'),

    # dispatch_equip_chain_state_sprite_by_slot @ 0x0806e898 (asm/09 L207):
    #   (gP1LifePoints) -> (gDuelPhaseFlags)
    #   LP_STATE_BASE = 0x0201b290 (gP1LifePoints)  -->  LP_STATE_BASE = 0x0201b290 (gDuelPhaseFlags)
    (0x0806e898, '(gP1LifePoints)', '(gDuelPhaseFlags)'),
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, label):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True


def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- FAIL" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        if bad:
            print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
        else:
            cu = currentProgram.getListing().getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_addr, gas_label, slot_label, made):
    if DRY:
        print("[dry] REF 0x%08x ref->0x%08x (%s) rename %s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return True
    rm = currentProgram.getReferenceManager()
    sym_tbl = currentProgram.getSymbolTable()

    tgt_a = _addr(target_addr)
    if target_addr not in made:
        existing = [s.getName() for s in sym_tbl.getSymbols(tgt_a)]
        if gas_label not in existing:
            sym_tbl.createLabel(tgt_a, gas_label, SourceType.USER_DEFINED)
        made.add(target_addr)

    slot_a = _addr(slot_addr)
    ref = rm.addMemoryReference(slot_a, tgt_a, RefType.DATA, SourceType.USER_DEFINED, 0)
    rm.setPrimary(ref, True)

    existing_slot = [s.getName() for s in sym_tbl.getSymbols(slot_a)]
    if slot_label not in existing_slot:
        sym_tbl.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)

    print("[REF] 0x%08x -> 0x%08x (%s) label=%s" % (slot_addr, target_addr, gas_label, slot_label))
    return True


def _apply_rename_slot(slot_addr, old_label, new_label, eol):
    if DRY:
        print("[dry] RENAME 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
        return
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    syms = list(sym_tbl.getSymbols(a))
    renamed = False
    for s in syms:
        if s.getName() == old_label:
            s.setName(new_label, SourceType.USER_DEFINED)
            print("[REN] 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
            renamed = True
            break
    if not renamed:
        names = [s.getName() for s in list(sym_tbl.getSymbols(a))]
        if new_label not in names:
            sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
            print("[REN] 0x%08x  old='%s' not found; created new label %s" % (
                slot_addr, old_label, new_label))
        else:
            print("[REN] 0x%08x  %s already present" % (slot_addr, new_label))

    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        if bad:
            print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
        else:
            cu = currentProgram.getListing().getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _apply_plate_fix(func_addr, old_text, new_text):
    for txt in [old_text, new_text]:
        if any(ord(ch) > 127 for ch in txt):
            print("[PLATE FAIL] non-ASCII in plate_fix @ 0x%08x -- ABORTING" % func_addr)
            return False
    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return True
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[PLATE FAIL] 0x%08x: no CodeUnit -- FAIL" % func_addr)
        return False
    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[PLATE FAIL] 0x%08x: no plate comment -- FAIL" % func_addr)
        return False
    if old_text not in existing:
        print("[PLATE FAIL] 0x%08x: '%s' not found in plate -- FAIL" % (func_addr, old_text))
        return False
    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX ok] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg1Slots (DRY=%s) ===" % DRY)
    print("  Seg-1: 0x0806e76c..0x0806ff50")
    print("  EQ=%d  REF=%d  RENAME=%d  FUNC_RENAME=%d  PLATE_SUBS=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(FUNC_RENAMES), len(PLATE_SUBS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES !!!" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = ref_fail = 0
    made = set()
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry
        if _apply_ref(slot_addr, target_addr, gas_label, slot_label, made):
            ref_ok += 1
        else:
            ref_fail += 1
    print("  REF done: %d ok, %d fail" % (ref_ok, ref_fail))
    if ref_fail > 0:
        print("  !!! %d REF FAILURES !!!" % ref_fail)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, old_label, new_label, eol in RENAME_SLOTS:
        _apply_rename_slot(slot_addr, old_label, new_label, eol)

    # D. FUNC_RENAME (none)
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))

    # E. PLATE_SUBS
    print("\n--- E. PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
    plate_ok = plate_fail = 0
    for func_addr, old_s, new_s in PLATE_SUBS:
        if _apply_plate_fix(func_addr, old_s, new_s):
            plate_ok += 1
        else:
            plate_fail += 1
    print("  PLATE_SUBS done: %d ok, %d FAIL" % (plate_ok, plate_fail))
    if plate_fail > 0:
        print("  !!! %d PLATE FAILURES -- check plate comment text !!!" % plate_fail)

    print("\n=== RefineF09Seg1Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d/%d ok  RENAME=%d  FUNC_RENAME=%d  PLATE=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS),
        ref_ok, len(REF_SLOTS),
        len(RENAME_SLOTS),
        len(FUNC_RENAMES),
        plate_ok, len(PLATE_SUBS)))


main()
