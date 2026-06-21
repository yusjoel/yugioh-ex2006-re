# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg5bSlots.py -- f10 Seg-5b (0x0807ec10..0x0807f730)
#   tick_equip_zone15_bitmap_with_sprite_output / tick_equip_effect_display_state_machine_alt /
#   dispatch_equip_display_by_state_code / dispatch_equip_zone_sprite_banisher_or_lp /
#   tick_prng_pair_zone_sprite_by_field_card / enqueue_field_slot_sprite_for_zone11 /
#   enqueue_field_slot_sprite_for_equip_head / dispatch_equip_zone_sprite_shape_b_by_state /
#   submit_equip_slot_lp_indicators_from_bitmap / find_equip_display_entry_by_card_id /
#   check_card_equip_criteria_by_ext_field6 / check_slot_card_equip_criteria_by_state_code /
#   check_card_equip_display_criteria_match / get_equip_display_type_code_by_card_id
#
# Sections:
#   A. EQ_SLOTS  -- data-equate: 26 slots (22 REUSE + 4 NEW)
#   B. REF_SLOTS -- USER label + DATA ref + slot rename: 12 slots
#   D. PLATE_OPS -- C8 stale FUN_ substitution (5 in-file + 1 cross-file full-rewrite)
#                   C9 CJK plate full-rewrite to ASCII (2 plates)
#
# NEW constants (already added to constants/*.inc before running this script):
#   FGD_CID=0x157e (card_info.inc), FLUTE_SUMMONING_KURIBOH_CID=0x19ec (card_info.inc)
#   ZONE_ENTRY_OFFSET_5CC=0x5cc (ewram.inc), EQUIP_DISPLAY_ROM_TABLE_BASE=0x09e59e14 (ewram.inc)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

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
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values verified against ROM via python struct.unpack_from.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # REUSE: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc L251) -- 10 slots
    (0x0807ec94, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_zone15_stride'),
    (0x0807ecec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_zone15_stride_b'),
    (0x0807f064, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_banisher_stride'),
    (0x0807f144, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'enqueue_zone11_stride'),
    (0x0807f1e4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'enqueue_equip_head_stride'),
    (0x0807f278, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'enqueue_equip_head_stride_b'),
    (0x0807f4c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'shape_b_stride'),
    (0x0807f50c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'submit_lp_bitmap_stride'),
    (0x0807f5bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'find_equip_entry_stride'),
    (0x0807f65c, 0x000019ef, 'EHERO_ERIKSHIELER_CID', 'check_criteria_match_erikshieler'),
    # REUSE: EQUIP_PHASE_FRAME_OFF=0x4a4 (ewram.inc L437) -- 4 slots
    (0x0807f05c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'dispatch_equip_banisher_frame_off'),
    (0x0807f0a0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'tick_prng_frame_off'),
    (0x0807f0d8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'tick_prng_frame_off_b'),
    (0x0807f13c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'enqueue_zone11_frame_off'),
    (0x0807f490, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'shape_b_frame_off'),
    # REUSE: BANISHER_OF_THE_LIGHT_CID=0x1332 (card_info.inc)
    (0x0807f09c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'tick_prng_banisher_cid'),
    # REUSE: P1LP_BLOCK2_OFF_1CE8=0x1ce8 (ewram.inc L276)
    (0x0807f488, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'shape_b_lp_block2_off'),
    # REUSE: EHERO CIDs (card_info.inc)
    (0x0807f6d8, 0x000018a6, 'EHERO_AVIAN_CID', 'get_display_code_avian'),
    (0x0807f6dc, 0x000018a7, 'EHERO_BURSTINATRIX_CID', 'get_display_code_burstinatrix'),
    (0x0807f6e0, 0x000018a8, 'EHERO_CLAYMAN_CID', 'get_display_code_clayman'),
    (0x0807f6e4, 0x000018f9, 'EHERO_BUBBLEMAN_CID', 'get_display_code_bubbleman'),
    (0x0807f714, 0x000019ef, 'EHERO_ERIKSHIELER_CID', 'get_display_code_erikshieler'),
    # NEW: FGD_CID=0x157e (card_info.inc, 2 slots)
    (0x0807f658, 0x0000157e, 'FGD_CID', 'check_criteria_match_fgd'),
    (0x0807f710, 0x0000157e, 'FGD_CID', 'get_display_code_fgd'),
    # NEW: ZONE_ENTRY_OFFSET_5CC=0x5cc (ewram.inc)
    (0x0807f510, 0x000005cc, 'ZONE_ENTRY_OFFSET_5CC', 'shape_b_zone_entry_off'),
    # NEW: EQUIP_DISPLAY_ROM_TABLE_BASE=0x09e59e14 (ewram.inc)
    (0x0807f5ec, 0x09e59e14, 'EQUIP_DISPLAY_ROM_TABLE_BASE', 'find_equip_entry_table_base'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gDuelPhaseFlags=0x0201b290 (ewram.inc L353) -- 6 slots
    (0x0807ec2c, 0x0201b290, 'gDuelPhaseFlags', 'DAT_0807ec2c'),
    (0x0807ed24, 0x0201b290, 'gDuelPhaseFlags', 'DAT_0807ed24'),
    (0x0807ee94, 0x0201b290, 'gDuelPhaseFlags', 'DAT_0807ee94'),
    (0x0807f008, 0x0201b290, 'gDuelPhaseFlags', 'DWORD_0807f008'),
    (0x0807f068, 0x0201b290, 'gDuelPhaseFlags', 'DWORD_0807f068'),
    (0x0807f0c0, 0x0201b290, 'gDuelPhaseFlags', 'DWORD_0807f0c0'),
    (0x0807f48c, 0x0201b290, 'gDuelPhaseFlags', 'DWORD_0807f48c'),
    # gDuelFieldSlots=0x0201c510 (ewram.inc L314) -- 3 slots
    (0x0807ec98, 0x0201c510, 'gDuelFieldSlots', 'DAT_0807ec98'),
    (0x0807f1e8, 0x0201c510, 'gDuelFieldSlots', 'DWORD_0807f1e8'),
    (0x0807f27c, 0x0201c510, 'gDuelFieldSlots', 'DWORD_0807f27c'),
    (0x0807f5c0, 0x0201c510, 'gDuelFieldSlots', 'DWORD_0807f5c0'),
    # gP1HandSlotArray=0x0201c8f8 (ewram.inc L334) -- 1 slot
    (0x0807ecf0, 0x0201c8f8, 'gP1HandSlotArray', 'DAT_0807ecf0'),
]

# ---------------------------------------------------------------------------
# D. PLATE_OPS: list of operations
#    Mode 'sub': (func_addr, 'sub', old_substr, new_substr)
#      -> substring replace in existing plate; WARN if not found (treat as FAIL)
#    Mode 'set': (func_addr, 'set', new_plate_text)
#      -> full plate replacement (used for CJK rewrites and cross-file full-rewrite)
# ---------------------------------------------------------------------------
PLATE_OPS = [
    # --- C8 in-file stale FUN_ substitutions ---
    # find_equip_display_entry_by_card_id (0x0807f5d4): FUN_0807f644 -> check_card_equip_display_criteria_match
    (0x0807f5d4, 'sub', 'FUN_0807f644', 'check_card_equip_display_criteria_match'),
    # check_card_equip_criteria_by_ext_field6 (0x0807f5f0): 2 substitutions
    (0x0807f5f0, 'sub', 'FUN_0807f644', 'check_card_equip_display_criteria_match'),
    (0x0807f5f0, 'sub', 'FUN_0807f800', 'check_equip_slot_criteria_by_ext_field6_any'),
    # check_slot_card_equip_criteria_by_state_code (0x0807f618): 2 in-file subs
    (0x0807f618, 'sub', 'FUN_0807f848', 'check_equip_slot_criteria_by_state_code_any'),
    (0x0807f618, 'sub', 'FUN_0807f8f0', 'find_first_equip_slot_criteria_by_state_code'),
    # get_equip_display_type_code_by_card_id (0x0807f6f0): FUN_0807f7bc -> fill_equip_criteria_display_code_array
    (0x0807f6f0, 'sub', 'FUN_0807f7bc', 'fill_equip_criteria_display_code_array'),
    # --- C8 cross-file full-rewrite (line-11578 plate) ---
    # check_slot_card_equip_criteria_by_state_code (0x0807f618): full rewrite of cross-file FUN_ line
    # (The 2 in-file subs above run first; this replaces remaining cross-file FUN_ references)
    (0x0807f618, 'sub', 'FUN_08054d5c', 'check_equip_slot_eligible_by_display_criteria_loop'),
    (0x0807f618, 'sub', 'FUN_080598d8', 'tick_equip_atk_zone_sprite_display_seq'),
    # --- C9 CJK plate full rewrites (ASCII replacement) ---
    # A) tick_equip_effect_display_state_machine_alt (0x0807ed04)
    (0x0807ed04, 'set',
     '@ 29-case switch state machine frame driver for equip card effect display (sibling of 0807d104).\n'
     '@ State code = [IWRAM_BASE+0x4a0] - 0x64; switch index 0..0x1c (29 cases):\n'
     '@ 0x80 -> lookup_slot_display_value_by_card_id + dispatch_effect_handler_by_card_id;\n'
     '@ on success -> trigger_card_display_op31_if_not_active(0x3a) return 0x7e;\n'
     '@ on fail non-spell -> trigger_card_display_op31(0xd) return 0x78;\n'
     '@ on fail spell -> return 0x0;\n'
     '@ 0x7e -> init_effect_slot_display_context(player, 6, card_id, display_val) return 0x7d;\n'
     '@ 0x7d -> get_monster_slot_entry_ptr x2 both sides; extract tile_col/flip;\n'
     '@ render_spell_zone_sprite_with_field_copy_check return 0x64;\n'
     '@ 0x78 -> count_field_cards_pair_allowed_for_card + get_card_type_bits;\n'
     '@ if count < type_bits then set_lp_row_type7_if_opponent_linked; return 0x64;\n'
     '@ 0x64 -> check_card_type_is_spell; non-spell -> enqueue_lp_counter_sprite_by_player; return 0x0.\n'
     '@ \n'
     '@ Constants:\n'
     '@ - IWRAM_BASE = 0x0201b290\n'
     '@ - STATE_OFFSET = 0x94*8 = 0x4a0\n'
     '@ - TRIGGER_OP1 = 0x3a (trigger op success path)\n'
     '@ - TRIGGER_OP2 = 0xd (trigger op spell_fail path)\n'
     '@ - DISPLAY_CTX_MODE = 6 (init_effect_slot_display_context mode)'),
    # B) tick_prng_pair_zone_sprite_by_field_card (0x0807f0a4)
    (0x0807f0a4, 'set',
     '@ 3-step frame state machine for rendering paired-zone sprites after prng sampling.\n'
     '@ Routes on [IWRAM_BASE+0x4a0]: 0x80 -> increment_lp_bar_display_counter;\n'
     '@ write [IWRAM+0x4a4]=0 (COUNTER_OFFSET reset); return 0x7f;\n'
     '@ 0x7f -> read [IWRAM+0x4a4] counter; if > 1 return 0x7e (wait);\n'
     '@ else sample_prng_scaled for random index;\n'
     '@ read gP1LifePoints[player*0x868+0x18+rand_offset] card_id;\n'
     '@ call render_pair_zone_sprites_if_field_card_present(opponent, card_id_bits13, 0, 1); return 0x7f;\n'
     '@ 0x7e -> decrement_lp_bar_display_counter; return 0x0.\n'
     '@ Side effects: write IWRAM COUNTER_OFFSET; LP bar counter +1/-1; render paired-zone sprites.\n'
     '@ \n'
     '@ Constants:\n'
     '@ - IWRAM_BASE = 0x0201b290\n'
     '@ - STATE_OFFSET = 0x94*8 = 0x4a0\n'
     '@ - COUNTER_OFFSET = 0x4a4\n'
     '@ - PLAYER_STRIDE = 0x868\n'
     '@ - HAND_ENTRY_OFFSET = 0x18 (gP1LifePoints base + player*0x868 + 0x18)\n'
     '@ - RENDER_ZONE_FLAG = 1 (render_pair_zone_sprites_if_field_card_present last param)'),
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF10Seg5bSlots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nD = 0
    nD_fail = 0
    made = set()

    # --- A. EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
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
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B. REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- D. PLATE_OPS ---
    for entry in PLATE_OPS:
        func_int = entry[0]
        mode     = entry[1]
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int); nD_fail += 1; continue

        if mode == 'sub':
            old_s = entry[2]
            new_s = entry[3]
            if DRY:
                print("[D dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
                nD += 1; continue
            plate = cu.getComment(CodeUnit.PLATE_COMMENT)
            if plate is None:
                print("[D FAIL] no plate @ 0x%08x (wanted sub '%s')" % (func_int, old_s)); nD_fail += 1; continue
            if old_s not in plate:
                print("[D FAIL] '%s' not in plate @ 0x%08x -- WARN treated as FAIL" % (old_s, func_int)); nD_fail += 1; continue
            new_plate = plate.replace(old_s, new_s)
            cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
            print("[D ok-sub] 0x%08x '%s'->'%s'" % (func_int, old_s, new_s)); nD += 1

        elif mode == 'set':
            new_plate = entry[2]
            if DRY:
                print("[D dry] 0x%08x plate set (%d chars)" % (func_int, len(new_plate)))
                nD += 1; continue
            cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
            print("[D ok-set] 0x%08x plate replaced (%d chars)" % (func_int, len(new_plate))); nD += 1

    print("")
    print("[done] A=%d B=%d D=%d D_FAIL=%d (DRY=%s)" % (nA, nB, nD, nD_fail, DRY))
    if nD_fail > 0:
        print("[ERROR] %d PLATE_OPS failed -- check stale FUN_ resolution" % nD_fail)


main()
