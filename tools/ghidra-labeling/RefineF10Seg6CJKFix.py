# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg6CJKFix.py -- fix remaining 3 CJK mojibake plates in Seg-6
#   After RefineF10Seg6Slots.py, 3 plates still have mojibake:
#     0x0807f7bc = fill_equip_criteria_display_code_array
#     0x0807fb9c = build_equip_slot_criteria_from_card_range
#     0x0807fde8 = dispatch_equip_criteria_display_by_type_code
#   All text pure ASCII. Ghidra Jython mojibake prevention.

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


CJK_PLATES = [
    # fill_equip_criteria_display_code_array (0x0807f7bc) -- 2 mojibake lines
    (0x0807f7bc,
     "@ fill_equip_criteria_display_code_array: populates display code array [gDuelPhaseFlags+EQUIP_CRITERIA_DISPLAY_ARR_OFF+i*4] for i=0..count-1.\n"
     "@ count=[gDuelPhaseFlags+0x5a0]; base=[gDuelPhaseFlags+0x598]; calls get_equip_display_criteria_code_by_card_and_slot per slot.\n"
     "@ Void return (bx r0, Sub-case E via pop{r0}).\n"
     "@ Constants: CRITERIA_ARRAY_OFFSET=0xb3*8=0x598, CRITERIA_COUNT_OFFSET=0xb4*8=0x5a0, DISPLAY_CODE_ARRAY_OFFSET=0x5ac"),

    # build_equip_slot_criteria_from_card_range (0x0807fb9c) -- 1 mojibake line
    (0x0807fb9c,
     "@ build_equip_slot_criteria_from_card_range: composite equip criteria builder, indeg=2. Args: card_id(r0), context_ptr(r1).\n"
     "@ Calls map_field8_to_card_type_category to classify card; category==3 (equip-type) checks check_card_targeted_by_spell_zone_effect for existing effect;\n"
     "@ then calls check_card_id_is_equip_set_e + find_first_equip_slot_criteria_by_state_code + check_equip_slot_eligible_with_criteria_and_target.\n"
     "@ Returns 0=no eligible slot found, 1=eligible slot found."),

    # dispatch_equip_criteria_display_by_type_code (0x0807fde8) -- 1 mojibake line
    (0x0807fde8,
     "@ dispatch_equip_criteria_display_by_type_code: equip display type/criteria dispatcher head function (30-case switchD_0807fe22).\n"
     "@ Called by build_equip_criteria_for_target_slots (tags: [equip,criteria,display], indeg=1).\n"
     "@ Reads type_code from [gDuelPhaseFlags+0x4a0*8]; switchD dispatches to per-type display criteria builder.\n"
     "@ Case 0x80 -> activate_field_spell_neo_daedalus_group_if_placeable."),
]


def main():
    print("=== RefineF10Seg6CJKFix (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()

    for func_addr, new_plate in CJK_PLATES:
        cu = listing.getCodeUnitAt(_addr(func_addr))
        if cu is None:
            print("[FAIL] no CodeUnit @ 0x%08x" % func_addr)
            continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[WARN] no plate @ 0x%08x -- writing anyway" % func_addr)
            if not DRY:
                cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
                print("[PLT] 0x%08x: plate written (was empty)" % func_addr)
            else:
                print("[dry] CJK_PLATE 0x%08x: write new ASCII plate" % func_addr)
            continue
        has_cjk = any(ord(c) > 0x7f for c in plate)
        print("[info] 0x%08x: plate len=%d has_cjk=%s" % (func_addr, len(plate), has_cjk))
        if DRY:
            print("[dry] CJK_PLATE 0x%08x: rewrite to ASCII (has_cjk=%s)" % (func_addr, has_cjk))
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        # Verify
        plate2 = cu.getComment(CodeUnit.PLATE_COMMENT)
        has_cjk2 = any(ord(c) > 0x7f for c in (plate2 or ''))
        print("[PLT] 0x%08x: replaced (new len=%d, CJK=%s)" % (func_addr, len(plate2 or ''), has_cjk2))

    print("=== RefineF10Seg6CJKFix DONE ===")


main()
