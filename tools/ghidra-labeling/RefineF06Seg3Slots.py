# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg3Slots.py -- F06 Seg-3 (0x08054ba0..0x08055440)
#   ROM range: check_equip_slot_eligible_by_equip_type_and_occupied..
#              check_equip_slot_whitelist_with_zone_bitmap (22 fn + 1 disasm'd)
#
# Sections:
#   A. EQ_SLOTS  -- 42 data-equate slots (all reuse ewram.inc)
#                   PLAYER_BLOCK_STRIDE=0x868 x21 + gDuelFieldSlots=0x0201c510 x21
#                   + 2 literal pool slots inside disasm'd fn (0x080551b0 / 0x080551b4)
#   B. REF_SLOTS -- 1 USER-label + DATA-ref (gEquipChainSlotRefs=0x0201bb90)
#
# Note: disasm of ROM_INCBIN 0x55188/0x34 is done by DisassembleF06Seg3Block.py (run first).
# After DisassembleF06Seg3Block.py runs, 0x080551b0/0x080551b4 are DWORDs; EQ section handles them.
#
# 0 new constants needed (all 3 unique values reuse ewram.inc):
#   PLAYER_BLOCK_STRIDE=0x00000868 (ewram.inc L250)
#   gDuelFieldSlots=0x0201c510    (ewram.inc L311)
#   gEquipChainSlotRefs=0x0201bb90 (ewram.inc L313)

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
#    All values verified against ROM via python struct.unpack_from('<I', rom, addr-0x08000000).
#    const_name must be a pre-existing .equ in constants/*.inc.
#    slot_label must differ from const_name (no label/equate collision).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ---- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) x21 ----
    (0x08054bdc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_equip_type_and_occupied_stride'),
    (0x08054c3c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_effect_ctx_stride'),
    (0x08054ca0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_whitelist_space_and_type_stride'),
    (0x08054cf8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_equippable_and_type_code_stride'),
    (0x08054d4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_whitelist_field7_and_zone_bit_stride'),
    (0x08054dd8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_display_criteria_loop_stride'),
    (0x08054e4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_field8_or_field6_and_type_stride'),
    (0x08054ef8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_same_side_field8_zero_field6_and_type_stride'),
    (0x08054f54, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_spell_type_and_prereqs_stride'),
    (0x08054fac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_field8_zero_and_prereqs_stride'),
    (0x0805500c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_prereqs_and_type_stride'),
    (0x08055068, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_type_eligibility_no_range_stride'),
    (0x080550d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_type_code_mismatch_stride'),
    (0x08055128, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_type_stride'),
    (0x08055178, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_cross_player_type_eligible_stride'),
    # disasm'd fn literal pool:
    (0x080551b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_zone_slot_clear_equip_stride'),
    (0x08055204, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_g_and_field5_stride'),
    (0x08055278, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_slot_effect_value_beats_card_category_stride'),
    (0x08055308, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_effect_value_and_category_stride'),
    (0x08055350, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_player_match_and_empty_field6_stride'),
    (0x080553c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_mismatch_prereqs_and_eligible_stride'),
    (0x08055430, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_whitelist_with_zone_bitmap_stride'),

    # ---- gDuelFieldSlots = 0x0201c510 (ewram.inc) x21 ----
    (0x08054be0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_equip_type_and_occupied_slots'),
    (0x08054c40, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_effect_ctx_slots'),
    (0x08054ca4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_whitelist_space_and_type_slots'),
    (0x08054cfc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_equippable_and_type_code_slots'),
    (0x08054d50, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_whitelist_field7_and_zone_bit_slots'),
    (0x08054ddc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_display_criteria_loop_slots'),
    (0x08054e50, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_field8_or_field6_and_type_slots'),
    (0x08054efc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_same_side_field8_zero_field6_and_type_slots'),
    (0x08054f58, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_spell_type_and_prereqs_slots'),
    (0x08054fb0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_field8_zero_and_prereqs_slots'),
    (0x08055010, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_prereqs_and_type_slots'),
    (0x0805506c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_type_eligibility_no_range_slots'),
    (0x080550d8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_type_code_mismatch_slots'),
    (0x0805512c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_type_slots'),
    (0x0805517c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_cross_player_type_eligible_slots'),
    # disasm'd fn literal pool:
    (0x080551b4, 0x0201c510, 'gDuelFieldSlots', 'check_zone_slot_clear_equip_slots'),
    (0x08055208, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_g_and_field5_slots'),
    (0x0805527c, 0x0201c510, 'gDuelFieldSlots', 'check_slot_effect_value_beats_card_category_slots'),
    (0x0805530c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_effect_value_and_category_slots'),
    (0x08055354, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_player_match_and_empty_field6_slots'),
    (0x080553c8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_mismatch_prereqs_and_eligible_slots'),
    (0x08055434, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_whitelist_with_zone_bitmap_slots'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, value, gas_label, slot_label)
#    Creates USER label at target + DATA memory reference from slot to target.
#    gas_label must already exist in ewram.inc as a .equ (runtime addr resolves to ewram.inc value).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gEquipChainSlotRefs = 0x0201bb90 (ewram.inc L313)
    (0x08054c44, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_prereqs_and_effect_ctx_ctx'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data at 0x%08x" % slot_int
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF06Seg3Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm      = currentProgram.getSymbolTable()
    nA = nB = 0

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS (%d slots) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s want=0x%x)" % (slot_int, err, cname, value))
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # --- B. REF_SLOTS ---
    print("--- B. REF_SLOTS (%d slots) ---" % len(REF_SLOTS))
    for slot_int, target_int, gas_label, slot_label in REF_SLOTS:
        ok, err = _check(slot_int, target_int)
        if not ok:
            print("[B FAIL] 0x%08x: %s (target=%s want=0x%x)" % (slot_int, err, gas_label, target_int))
            continue
        if DRY:
            print("[B dry] 0x%08x -> %s (0x%08x) slot_label=%s" % (slot_int, gas_label, target_int, slot_label))
            nB += 1
            continue
        # Create USER label at target (or reuse existing)
        target_addr = _addr(target_int)
        existing_sym = sm.getPrimarySymbol(target_addr)
        if existing_sym is None or existing_sym.getSource() != SourceType.USER_DEFINED:
            createLabel(target_addr, gas_label, True, SourceType.USER_DEFINED)
            print("[B ok] label %s @ 0x%08x" % (gas_label, target_int))
        else:
            print("[B ok] reuse label %s @ 0x%08x" % (existing_sym.getName(), target_int))
        # Create DATA memory reference slot -> target
        rm.addMemoryReference(_addr(slot_int), target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        # Set primary symbol for slot
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> slot_label=%s ref->%s" % (slot_int, slot_label, gas_label))
        nB += 1

    print("[done] A=%d B=%d (DRY=%s)" % (nA, nB, DRY))


main()
