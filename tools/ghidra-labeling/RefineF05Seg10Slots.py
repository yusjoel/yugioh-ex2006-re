# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg10Slots.py -- file-05 Seg-10 (0x08052df8..0x080537c0)
#   23 functions: check_equip_slot_eligible_by_* + dispatch_equip_slot_eligible_by_*
#   (file 05 final segment)
#
# Sections:
#   A. EQ_SLOTS:
#      Group A: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc) -- 20 slots
#      Group B: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)     -- 20 slots
#      Group C: gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc) --  3 slots
#      Group D: unique values (8 slots; 2 new to card_info.inc, 6 reuse)
#      Total EQ: 51 slots
#   B. EOL_SLOTS -- ASCII EOL comments on 8 slots
#   C. PLATE_REWRITES -- full plate overwrite for 2 functions with CJK mojibake
#
# carve=0, disasm=0, section5_1=0
# All EOL/plate text is pure ASCII. No CJK.
#
# New constants added to card_info.inc before running this script:
#   BOTTOMLESS_TRAP_HOLE_CID = 0x00001518
#   FIELD5_SCORE_THRESHOLD_1499 = 0x000005db
# (both grep-verified absent from all constants/*.inc before addition)

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

def _addr(offset):
    return toAddr(offset)

def _check(addr_int, expected_val, label):
    """Verify ROM word at addr matches expected value; WARN = FAIL (not skipped)."""
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xffffffff
        if actual != (expected_val & 0xffffffff):
            print("FAIL value_check %s @0x%08x: expected=0x%08x actual=0x%08x" % (
                label, addr_int, expected_val & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("FAIL value_check %s @0x%08x: exception %s" % (label, addr_int, str(e)))
        return False

def apply_eq_slot(slot_addr, value, const_name, slot_label):
    """Create equate + label at slot_addr."""
    if not _check(slot_addr, value, const_name):
        return False
    if DRY:
        print("DRY EQ 0x%08x %s = %s" % (slot_addr, slot_label, const_name))
        return True
    try:
        eqtbl = currentProgram.getEquateTable()
        eq = eqtbl.getEquate(const_name)
        if eq is None:
            eq = eqtbl.createEquate(const_name, value & 0xffffffff)
        eq.addReference(_addr(slot_addr), 0)
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("OK  EQ 0x%08x %s = %s" % (slot_addr, slot_label, const_name))
        return True
    except Exception as e:
        print("ERR EQ 0x%08x %s: %s" % (slot_addr, slot_label, str(e)))
        return False

def apply_eol(slot_addr, eol_ascii):
    """Set EOL comment (pure ASCII only)."""
    if DRY:
        print("DRY EOL 0x%08x eol=%s" % (slot_addr, repr(eol_ascii)))
        return True
    try:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(_addr(slot_addr))
        if cu is None:
            print("FAIL EOL 0x%08x: no code unit" % slot_addr)
            return False
        cu.setComment(CodeUnit.EOL_COMMENT, eol_ascii)
        print("OK  EOL 0x%08x" % slot_addr)
        return True
    except Exception as e:
        print("ERR EOL 0x%08x: %s" % (slot_addr, str(e)))
        return False

def apply_plate_rewrite(func_addr, new_text_ascii):
    """Full overwrite of plate comment with pure ASCII text (replaces CJK mojibake)."""
    if DRY:
        print("DRY PLATE_REWRITE 0x%08x (len=%d)" % (func_addr, len(new_text_ascii)))
        return True
    try:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(_addr(func_addr))
        if cu is None:
            print("FAIL PLATE_REWRITE 0x%08x: no code unit" % func_addr)
            return False
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text_ascii)
        print("OK  PLATE_REWRITE 0x%08x" % func_addr)
        return True
    except Exception as e:
        print("ERR PLATE_REWRITE 0x%08x: %s" % (func_addr, str(e)))
        return False

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- Group A: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc) --- 20 slots
    (0x08052e4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_active_player_match_stride'),
    (0x08052ebc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_whitelist_and_setcode_match_stride'),
    (0x08052f44, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_chain_score_field10_exact_stride'),
    (0x08052fa0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_chain_score_capped6_match_stride'),
    (0x08053024, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_owner_mismatch_whitelist_prereqs_stride'),
    (0x08053084, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_zone_flag_bits_stride'),
    (0x08053100, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_whitelist_and_setcode_no_field8_stride'),
    (0x08053168, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_not17_owner_mismatch_stride'),
    (0x080531d0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_monster_space_type_score3_stride'),
    (0x0805327c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_active_ctx_score_nonzero_stride'),
    (0x080532fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_owner_mismatch_field8_no_field6_stride'),
    (0x08053364, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_not17_owner_match_stride'),
    (0x0805340c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field5_score_or_chain_type_stride'),
    (0x080534b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_type_and_occupied_stride'),
    (0x08053514, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_whitelist_and_field8_stride'),
    (0x080535a0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_whitelist_prereqs_and_eligible_stride'),
    (0x0805362c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_whitelist_prereqs_and_eligible_b_stride'),
    (0x08053688, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_with_zone_guard_stride'),
    (0x080536f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_setcode_and_eligible_stride'),
    (0x080537b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_and_prereqs_no_whitelist_stride'),

    # --- Group B: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc) --- 20 slots
    (0x08052e50, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_active_player_match_dfs'),
    (0x08052ec0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_whitelist_and_setcode_match_dfs'),
    (0x08052f48, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_chain_score_field10_exact_dfs'),
    (0x08052fa4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_chain_score_capped6_match_dfs'),
    (0x08053028, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_owner_mismatch_whitelist_prereqs_dfs'),
    (0x08053088, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_zone_flag_bits_dfs'),
    (0x08053104, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_whitelist_and_setcode_no_field8_dfs'),
    (0x0805316c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_not17_owner_mismatch_dfs'),
    (0x080531d4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_monster_space_type_score3_dfs'),
    (0x08053280, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_active_ctx_score_nonzero_dfs'),
    (0x08053300, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_owner_mismatch_field8_no_field6_dfs'),
    (0x08053368, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_not17_owner_match_dfs'),
    (0x08053410, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field5_score_or_chain_type_dfs'),
    (0x080534b4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_type_and_occupied_dfs'),
    (0x08053518, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_whitelist_and_field8_dfs'),
    (0x080535a4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_whitelist_prereqs_and_eligible_dfs'),
    (0x08053630, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_whitelist_prereqs_and_eligible_b_dfs'),
    (0x0805368c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_with_zone_guard_dfs'),
    (0x080536f8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_setcode_and_eligible_dfs'),
    (0x080537b4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_and_prereqs_no_whitelist_dfs'),

    # --- Group C: gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc) --- 3 slots
    (0x08052e54, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_prereqs_and_active_player_match_ecsr'),
    (0x08052f04, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_owner_match_and_active_ctx_ecsr'),
    (0x08053284, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_active_ctx_score_nonzero_ecsr'),

    # --- Group D: unique values (8 slots) ---
    # BOTTOMLESS_TRAP_HOLE_CID = 0x1518 (new, added to card_info.inc)
    (0x08053414, 0x00001518, 'BOTTOMLESS_TRAP_HOLE_CID', 'check_equip_slot_eligible_by_field5_score_or_chain_type_bth_cid'),
    # FIELD5_SCORE_THRESHOLD_1499 = 0x5db (new, added to card_info.inc)
    (0x08053418, 0x000005db, 'FIELD5_SCORE_THRESHOLD_1499', 'check_equip_slot_eligible_by_field5_score_or_chain_type_f5s_max'),
    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0805341c, 0x0201b290, 'gDuelPhaseFlags', 'check_equip_slot_eligible_by_field5_score_or_chain_type_dpf'),
    # LP_BAR_ANIM_STATE_OFF = 0x4cc (reuse ewram.inc; dual-use: equip chain list node count)
    (0x08053420, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'check_equip_slot_eligible_by_field5_score_or_chain_type_chain_cnt_off'),
    # CHAIN_NODE_CARD_ARR_OFF = 0x4f4 (reuse ewram.inc)
    (0x08053424, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'check_equip_slot_eligible_by_field5_score_or_chain_type_card_arr_off'),
    # CHECKMATE_CID = 0x169b (reuse card_info.inc)
    (0x08053728, 0x0000169b, 'CHECKMATE_CID', 'dispatch_equip_slot_eligible_by_card_id_tier_cothcid'),
    # THROWSTONE_UNIT_CID = 0x14c5 (reuse card_info.inc)
    (0x0805372c, 0x000014c5, 'THROWSTONE_UNIT_CID', 'dispatch_equip_slot_eligible_by_card_id_tier_tucid'),
    # ARCANE_ARCHER_OF_THE_FOREST_CID = 0x1753 (reuse card_info.inc)
    (0x08053738, 0x00001753, 'ARCANE_ARCHER_OF_THE_FOREST_CID', 'dispatch_equip_slot_eligible_by_card_id_tier_aafcid'),

]  # end EQ_SLOTS (total: 20 + 20 + 3 + 8 = 51)

# ---------------------------------------------------------------------------
# B. EOL_SLOTS: (slot_addr, eol_ascii)
#    ASCII EOL comments on specific slots.
# ---------------------------------------------------------------------------
EOL_SLOTS = [
    # gEquipChainSlotRefs slots -- active equip ctx field layout
    (0x08052e54, 'active equip ctx: [+0]=p0_player [+4]=p1_player [+0x1c]=p0_slot [+0x20]=p1_slot'),
    (0x08052f04, 'active equip ctx: [+0]=p0_player [+4]=p1_player [+0x1c]=p0_slot [+0x20]=p1_slot'),
    (0x08053284, 'active equip ctx: [+0]=p0_player [+4]=p1_player [+0x1c]=p0_slot [+0x20]=p1_slot'),
    # Bottomless Trap Hole CID
    (0x08053414, 'Bottomless Trap Hole CID (pw=29401950)'),
    # field5 score threshold
    (0x08053418, 'field5 score threshold (1499=0x5db); score<=0x5db -> ineligible; score>0x5db -> eligible path'),
    # LP_BAR_ANIM_STATE_OFF dual-use as chain count offset
    (0x08053420, 'gDuelPhaseFlags+0x4cc = equip chain list node count'),
    # CHAIN_NODE_CARD_ARR_OFF
    (0x08053424, 'gDuelPhaseFlags+0x4f4 = equip chain card ptr array'),
    # dispatch_tier CIDs
    (0x08053728, 'Checkmate CID (slot=0x169b, pw=69313735)'),
    (0x0805372c, 'Throwstone Unit CID (slot=0x14c5, pw=76075810)'),
    (0x08053738, 'Arcane Archer of the Forest CID (slot=0x1753, pw=55001420)'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, new_plate_ascii)
#    Full overwrite of plate comment. Replaces CJK mojibake with pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # PLATE-1: dispatch_equip_slot_eligible_by_field6_bit (0x08053294)
    (0x08053294,
     "Equip slot eligibility two-path dispatch. Reads card_entry byte[+6] bits[4:3] (mask 0x1c).\n"
     "If bits[4:3] != 0 (field6 nonzero): calls check_equip_slot_eligible_by_card_id_bst.\n"
     "If bits[4:3] == 0: calls check_equip_slot_eligible_by_card_id_tree.\n"
     "Passes through return value. indeg=0 (Sub-type A, dispatched via fn-ptr table)."),

    # PLATE-2: dispatch_equip_slot_eligible_by_card_id_tier (0x08053704)
    (0x08053704,
     "Four-path card_id dispatch for equip slot eligibility. Reads byte[+3] bit7 (activation flag 0x80).\n"
     "If bit7==0: call check_equip_slot_eligible_by_card_id_tree (broad tree check).\n"
     "If bit7!=0: compare halfword card_id:\n"
     "  0x14c5 (Throwstone Unit) -> eval_equip_slot_score_by_card_state\n"
     "  0x169b (Checkmate) -> check_equip_slot_eligible_by_card_id_dispatch_b\n"
     "  0x1753 (Arcane Archer of the Forest) -> check_equip_slot_eligible_by_setcode_and_prereqs\n"
     "  other -> check_equip_slot_eligible_by_card_id_tree\n"
     "Passes through each path return value."),
]

# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
def main():
    eq_ok = 0; eq_fail = 0
    eol_ok = 0; eol_fail = 0
    plate_ok = 0; plate_fail = 0

    print("=== RefineF05Seg10Slots %s ===" % ("DRY RUN" if DRY else "LIVE"))

    print("--- EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for (sa, val, cname, slabel) in EQ_SLOTS:
        # Boundary guard: must be within Seg-10 range [0x08052df8, 0x080537c0)
        if sa < 0x08052df8 or sa >= 0x080537c0:
            print("FAIL BOUNDARY 0x%08x outside [0x08052df8, 0x080537c0)" % sa)
            eq_fail += 1
            continue
        if apply_eq_slot(sa, val, cname, slabel):
            eq_ok += 1
        else:
            eq_fail += 1

    print("--- EOL_SLOTS (%d) ---" % len(EOL_SLOTS))
    for (sa, eol) in EOL_SLOTS:
        if apply_eol(sa, eol):
            eol_ok += 1
        else:
            eol_fail += 1

    print("--- PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    for (fa, new_text) in PLATE_REWRITES:
        if apply_plate_rewrite(fa, new_text):
            plate_ok += 1
        else:
            plate_fail += 1

    total_fail = eq_fail + eol_fail + plate_fail
    print("=== SUMMARY: EQ %d/%d  EOL %d/%d  PLATE %d/%d  FAIL=%d ===" % (
        eq_ok, len(EQ_SLOTS),
        eol_ok, len(EOL_SLOTS),
        plate_ok, len(PLATE_REWRITES),
        total_fail))
    if total_fail > 0:
        print("RESULT: FAIL -- %d error(s)" % total_fail)
    else:
        print("RESULT: OK")

main()
