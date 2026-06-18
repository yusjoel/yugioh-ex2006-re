# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5aPoolFix4.py -- Fix remaining ROM_INCBIN at LAB_080736d2 in B4
#
# After FIX3, code at LAB_080736d2 (0x080736d2..0x080736ed) is still ROM_INCBIN.
# This is the final code section of machine_dup_sub_3690:
#   0x080736d2..0x080736ed: code containing LAB_080736d2 and LAB_080736ea
#   b LAB_080736ea @ 0x080736d0 -> target = 0x080736ea within this range
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

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
    print("=== RefineF09Seg5aPoolFix4 (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    if DRY:
        print("[dry] clearListing 0x080736d2..0x080736ed")
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x080736d2 (LAB_080736d2)")
        return

    print("\n--- FIX-B4-LAST: LAB_080736d2 @ 0x080736d2..0x080736ed ---")
    a_lo = _addr(0x080736d2)
    a_hi = _addr(0x080736ed)
    print("[B4L.1] clearListing 0x080736d2..0x080736ed")
    try:
        clearListing(a_lo, a_hi)
        print("        done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B4L.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("        TMode set")
    else:
        print("[WARN] TMode not found")
    print("[B4L.3] DisassembleCommand @ 0x080736d2 (LAB_080736d2)")
    cmd = DisassembleCommand(_addr(0x080736d2), None, False)
    if cmd.applyTo(currentProgram):
        print("        disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    # Verify
    for lab_addr, lab_name in [(0x080736d2, 'LAB_080736d2'),
                                (0x080736ea, 'LAB_080736ea')]:
        ea = _addr(lab_addr)
        syms = [s.getName() for s in sym_tbl.getSymbols(ea)]
        if lab_name in syms:
            print("[OK] %s defined at 0x%08x" % (lab_name, lab_addr))
        else:
            print("[NOTE] %s not yet in sym_tbl (will be created by GAS export flow analysis)" % lab_name)

    print("\n=== RefineF09Seg5aPoolFix4 DONE ===")


main()
