# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg1TailFix.py -- name the shared BLK2 tail at 0x0808526a
#
# After DisassembleCommand, Ghidra auto-created FUN_0808526a at address 0x0808526a.
# This is the shared STR+return-0 epilogue branched to by store_decremented_display_type_and_return.
# Name it to clear the FUN_ residual within block2 range [0x08085130, 0x0808527c).
#
# 0x0808526a:  STR r0,[r1]   (store SLOT_DISPLAY_TYPE back)
#              MOVS r0,#0    (return 0)
#              POP {r4}      (shared epilogue with dispatch_equip_slot_display_by_type_scarr)
#              POP {r1}
#              BX r1

from ghidra.program.model.symbol import SourceType
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
    if DRY:
        print("[dry] createFunction 0x0808526a -> store_slot_display_type_and_return_zero")
        return

    a = _addr(0x0808526a)
    fn = getFunctionAt(a)
    if fn is None:
        fn = createFunction(a, 'store_slot_display_type_and_return_zero')
    if fn is not None:
        try:
            fn.setName('store_slot_display_type_and_return_zero', SourceType.USER_DEFINED)
            print("[func] store_slot_display_type_and_return_zero @ 0x0808526a")
        except Exception as e:
            print("[warn] setName 0x0808526a: %s" % e)
    else:
        print("[FAIL] createFunction 0x0808526a")

    # Set plate
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu:
        try:
            cu.setComment(CodeUnit.PLATE_COMMENT,
                "Shared BLK2 tail: STR r0,[r1] stores updated SLOT_DISPLAY_TYPE_OFF value;\n"
                "then MOVS r0,#0 (return 0 = advance). Shared epilogue for type-0/2/5/3 sub-handlers\n"
                "that successfully advance the display type. Entered via branch from BLK2 stubs.")
            print("[plate] 0x0808526a OK")
        except Exception as e:
            print("[warn] plate 0x0808526a: %s" % e)

    print("=== RefineF11Seg1TailFix DONE ===")


main()
