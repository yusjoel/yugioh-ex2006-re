# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg1Slots.py -- F06 Seg-1 (0x080537c0..0x080541cc)
#   dispatch_equip_eligibility_by_slot_equip_flag
#   check_equip_slot_eligible_by_side_setcode_and_activation
#   check_equip_slot_eligible_by_setcode_and_valid_flag
#   check_equip_slot_eligible_by_whitelist_or_type_dispatch
#   check_equip_slot_eligible_by_type_and_chain
#   check_equip_slot_eligible_by_zone_chain_scan
#   check_equip_slot_eligible_by_opposite_side_and_effect_ctx
#   check_equip_slot_eligible_by_field6_and_full_prereqs
#   check_equip_slot_eligible_by_side_mismatch_and_field8_7
#   check_equip_slot_eligible_for_gravekeeper_series
#   check_equip_slot_eligible_by_equippable_and_monster_space
#   check_equip_slot_eligible_by_opposite_side_zone_chain
#   check_equip_slot_eligible_by_type_and_space
#   check_equip_slot_eligible_by_setcode_dedup_only
#   check_equip_slot_eligible_by_same_side_and_field8_9
#   check_equip_slot_eligible_by_side_match_and_type
#   check_equip_slot_eligible_with_score_bound_and_chain_scan
#   check_equip_slot_eligible_by_opposite_side_field6_and_type
#   check_equip_slot_eligible_by_field6_10_and_equippable
#   check_equip_slot_eligible_by_type_mismatch_and_eligible
#   dispatch_equip_slot_eligible_by_type_prereqs_or_setcode
#   check_equip_slot_eligible_by_side_whitelist_setcode_and_eligible
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (45 slots)
#   B. REF_SLOTS -- USER label on target + DATA ref from slot + slot rename (1 slot)
#   C. RENAME_SLOTS -- plain rename + optional EOL (1 slot)
#   D. PLATE_SUBS -- substring FUN_ -> current name (stale FUN_ in plate EOL lines)
#   E. PLATE_SET  -- full plate rewrite for CJK-mojibake plate (1 function)
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values verified against ROM via python struct.unpack_from.
#    const_name is a pre-existing .equ in constants/*.inc (no new equates here).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # PLAYER_BLOCK_STRIDE=0x868 (ewram.inc) x19
    (0x08053840, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_setcode_and_activation_stride'),
    (0x08053898, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_and_valid_flag_stride'),
    (0x080539ac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_chain_stride_b'),
    (0x08053a28, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_chain_stride_c'),
    (0x08053ad8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_chain_stride_d'),
    (0x08053b24, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_zone_chain_scan_stride_b'),
    (0x08053b7c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_zone_chain_scan_stride_c'),
    (0x08053bec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_and_effect_ctx_stride'),
    (0x08053c60, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_and_full_prereqs_stride'),
    (0x08053cb4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_mismatch_and_field8_7_stride'),
    (0x08053d28, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_for_gravekeeper_series_stride_b'),
    (0x08053e00, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_zone_chain_stride'),
    (0x08053eac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_dedup_only_stride'),
    (0x08053f00, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_same_side_and_field8_9_stride'),
    (0x08053f4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_match_and_type_stride'),
    (0x08053ff0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_score_bound_and_chain_scan_stride'),
    (0x08054078, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_field6_and_type_stride'),
    (0x080540dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_10_and_equippable_stride'),
    (0x080541bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_whitelist_setcode_and_eligible_stride'),
    # gDuelFieldSlots=0x0201c510 (ewram.inc) x19
    (0x08053844, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_setcode_and_activation_slots'),
    (0x0805389c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_and_valid_flag_slots'),
    (0x080539b0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_chain_slots_b'),
    (0x08053a2c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_chain_slots_c'),
    (0x08053adc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_chain_slots_d'),
    (0x08053b28, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_zone_chain_scan_slots_b'),
    (0x08053b80, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_zone_chain_scan_slots_c'),
    (0x08053bf0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_and_effect_ctx_slots'),
    (0x08053c64, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_and_full_prereqs_slots'),
    (0x08053cb8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_mismatch_and_field8_7_slots'),
    (0x08053d2c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_for_gravekeeper_series_slots'),
    (0x08053e04, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_zone_chain_slots'),
    (0x08053eb0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_dedup_only_slots'),
    (0x08053f04, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_same_side_and_field8_9_slots'),
    (0x08053f50, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_match_and_type_slots'),
    (0x08053ff4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_score_bound_and_chain_scan_slots'),
    (0x0805407c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_field6_and_type_slots'),
    (0x080540e0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_10_and_equippable_slots'),
    (0x080541c0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_whitelist_setcode_and_eligible_slots'),
    # SCROLLBAR_CLEAR_BITS_14_6=0xffff803f (gl_scrollbar.inc) x2 -- reuse
    (0x080539b4, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'check_equip_slot_eligible_by_type_and_chain_setcode_clear_b'),
    (0x08053ae0, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'check_equip_slot_eligible_by_type_and_chain_setcode_clear_d'),
    # gEquipChainSlotRefs=0x0201bb90 (ewram.inc) x1
    (0x08053bf4, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_opposite_side_and_effect_ctx_chain_refs'),
    # GRAVEKEEPERS_CANNONHOLDER_CID=0x158c (card_info.inc -- new entry) x1
    (0x08053d30, 0x0000158c, 'GRAVEKEEPERS_CANNONHOLDER_CID', 'check_equip_slot_eligible_for_gravekeeper_series_excl_cid'),
    # gDuelPhaseFlags=0x0201b290 (ewram.inc) x1
    (0x08053ff8, 0x0201b290, 'gDuelPhaseFlags', 'check_equip_slot_eligible_with_score_bound_and_chain_scan_phase_flags'),
    # LP_BAR_ANIM_STATE_OFF=0x4cc (ewram.inc) x1
    (0x08053ffc, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'check_equip_slot_eligible_with_score_bound_and_chain_scan_chain_cnt_off'),
    # CHAIN_NODE_CARD_ARR_OFF=0x4f4 (ewram.inc) x1
    (0x08054000, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'check_equip_slot_eligible_with_score_bound_and_chain_scan_card_arr_off'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # fn-ptr: 0x08053e08 = check_equip_slot_eligible_triple_predicate + 1 (THUMB odd addr)
    (0x08053e08, 0x0804f550, 'check_equip_slot_eligible_triple_predicate',
     'check_equip_slot_eligible_by_opposite_side_zone_chain_fn_ptr'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL. All EOL text pure ASCII (no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # DWORD_08054138 = 0x1706 -- equip_flag discriminator (not TORPEDO_FISH_CID; med-conf)
    (0x08054138, 'dispatch_equip_slot_eligible_by_type_prereqs_or_setcode_flag_a',
     'equip_flag=0x1706: type_then_prereqs path; +3=0x1709: setcode_and_prereqs path (med-conf)'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Substring replace stale FUN_ references in existing plate comments.
#    P2 (line 1024 in check_equip_slot_eligible_by_same_side_and_field8_9)
#    P3 (line 1482 in check_equip_slot_eligible_by_side_setcode_prereqs_and_type) -- Seg-2 boundary fn
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # P2: check_equip_slot_eligible_by_same_side_and_field8_9 (0x08053ebc)
    (0x08053ebc, 'FUN_08054e5c', 'check_equip_slot_eligible_by_setcode_prereqs_all_slots'),
    # P3: check_equip_slot_eligible_by_side_setcode_prereqs_and_type (0x080541cc) -- Seg-2 boundary fn
    (0x080541cc, 'FUN_08054e5c', 'check_equip_slot_eligible_by_setcode_prereqs_all_slots'),
]

# ---------------------------------------------------------------------------
# E. PLATE_SET: (func_entry_addr, new_plate_text)
#    Full plate rewrite (existing plate has CJK mojibake). Pure ASCII text only.
# ---------------------------------------------------------------------------
PLATE_SET = [
    (0x08054118,
     'Equip slot eligibility 3-way dispatch by slot[+0xa] equip flag.\n'
     'Reads slot[+0xa] halfword: if ==DISPATCH_FLAG_A (0x1706) calls check_equip_slot_eligible_by_type_then_prereqs;\n'
     'if ==DISPATCH_FLAG_A+3 (0x1709) calls check_equip_slot_eligible_by_setcode_and_prereqs;\n'
     'else calls check_equip_slot_eligible_by_card_id_tree. Transparent return (Sub-case E).\n'
     'Params: r0=ptr card_slot; r1=u32 player_id [0..1]; r2=u32 zone_slot_idx\n'
     'Returns: r0=u32 bool (1=eligible, 0=rejected; Sub-case E)\n'
     'Side effects: none'),
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
    print("=== RefineF06Seg1Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = nE = 0
    made = set()

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS ---")
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
    print("--- B. REF_SLOTS ---")
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

    # --- C. RENAME_SLOTS ---
    print("--- C. RENAME_SLOTS ---")
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- D. PLATE_SUBS ---
    print("--- D. PLATE_SUBS ---")
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[D SKIP] no plate @ 0x%08x" % func_int); continue
        if old_s not in plate:
            print("[D WARN] '%s' not found in plate @ 0x%08x -- TREAT AS FAIL" % (old_s, func_int)); continue
        if DRY:
            print("[D dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nD += 1; continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s)); nD += 1

    # --- E. PLATE_SET (full rewrite) ---
    print("--- E. PLATE_SET ---")
    for func_int, new_text in PLATE_SET:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[E FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        if DRY:
            print("[E dry] 0x%08x full plate rewrite (%d chars)" % (func_int, len(new_text)))
            nE += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("[E ok] 0x%08x plate set (%d chars)" % (func_int, len(new_text))); nE += 1

    print("[done] A=%d B=%d C=%d D=%d E=%d (DRY=%s)" % (nA, nB, nC, nD, nE, DRY))


main()
