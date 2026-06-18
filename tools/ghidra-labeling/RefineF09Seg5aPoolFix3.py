# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5aPoolFix3.py -- Final fix for B4 machine_dup_sub_3690 code at LAB_080736c6
#
# After FIX2, the code at 0x080736c6..0x080736ed (LAB_080736c6 region) was still ROM_INCBIN.
# This is a continuation of machine_dup_sub_3690 code that branches from LAB_080736a8
# at 0x080736b8 (bgt LAB_080736c6).
# It contains LAB_080736c8, LAB_080736d2, LAB_080736ea.
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
    print("=== RefineF09Seg5aPoolFix3 (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    if DRY:
        print("[dry] clearListing 0x080736c6..0x080736ed")
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x080736c6 (LAB_080736c6)")
        return

    # =========================================================================
    # FIX-B4-FINAL: LAB_080736c6 code @ 0x080736c6..0x080736ed
    # This is the third code section of machine_dup_sub_3690 after:
    #   - inline pools at 0x080736a0/a4 (previously fixed)
    #   - LAB_080736a8 code block at 0x080736a8..0x080736c5
    # The code at LAB_080736a8 has a `bgt LAB_080736c6` at 0x080736b8
    # which jumps to 0x080736c6. This section contains LAB_080736c8/d2/ea.
    # =========================================================================
    print("\n--- FIX-B4-FINAL: LAB_080736c6 @ 0x080736c6..0x080736ed ---")
    a_lo = _addr(0x080736c6)
    a_hi = _addr(0x080736ed)
    print("[B4F.1] clearListing 0x080736c6..0x080736ed")
    try:
        clearListing(a_lo, a_hi)
        print("        done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B4F.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("        TMode set")
    else:
        print("[WARN] TMode not found")
    print("[B4F.3] DisassembleCommand @ 0x080736c6 (LAB_080736c6)")
    cmd = DisassembleCommand(_addr(0x080736c6), None, False)
    if cmd.applyTo(currentProgram):
        print("        disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    # Verify LAB_ targets were created
    for lab_addr, lab_name in [(0x080736c8, 'LAB_080736c8'),
                                (0x080736d2, 'LAB_080736d2'),
                                (0x080736ea, 'LAB_080736ea')]:
        ea = _addr(lab_addr)
        syms = [s.getName() for s in sym_tbl.getSymbols(ea)]
        if lab_name in syms:
            print("[OK] %s defined at 0x%08x" % (lab_name, lab_addr))
        else:
            print("[NOTE] %s not yet in sym_tbl @ 0x%08x (may be created during GAS export)" % (lab_name, lab_addr))

    print("\n=== RefineF09Seg5aPoolFix3 DONE ===")
    print("  LAB_080736c6 disassembled -> LAB_080736c8/d2/ea should be defined by Ghidra flow analysis")


main()
