# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg5bPlateFix.py -- fix remaining /0807f8f0 addr in plate @ 0x0807f618
# The plate said FUN_0807f848/0807f8f0 -- after FUN_0807f848->check_equip_slot_criteria_by_state_code_any
# the residual is /0807f8f0 which needs -> /find_first_equip_slot_criteria_by_state_code

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


def main():
    print("=== RefineF10Seg5bPlateFix (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()

    # Fix plate @ 0x0807f618: replace /0807f8f0 -> /find_first_equip_slot_criteria_by_state_code
    func_int = 0x0807f618
    old_s = '/0807f8f0'
    new_s = '/find_first_equip_slot_criteria_by_state_code'
    cu = listing.getCodeUnitAt(_addr(func_int))
    if cu is None:
        print("[FAIL] no CodeUnit @ 0x%08x" % func_int); return
    plate = cu.getComment(CodeUnit.PLATE_COMMENT)
    if plate is None:
        print("[FAIL] no plate @ 0x%08x" % func_int); return
    print("[info] plate snippet: %r" % plate[plate.find('check_equip_slot_criteria'):plate.find('check_equip_slot_criteria')+120])
    if old_s not in plate:
        print("[SKIP] '%s' not in plate @ 0x%08x -- already fixed or different text" % (old_s, func_int))
        # show context around f8f0
        idx = plate.find('f8f0')
        if idx >= 0:
            print("[info] context around f8f0: %r" % plate[max(0,idx-30):idx+40])
        return
    if DRY:
        print("[dry] would replace '%s' -> '%s'" % (old_s, new_s)); return
    new_plate = plate.replace(old_s, new_s)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[ok] plate fixed: '%s' -> '%s'" % (old_s, new_s))
    print("[done]")


main()
