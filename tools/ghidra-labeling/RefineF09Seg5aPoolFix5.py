# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5aPoolFix5.py -- Final pass: disasm all remaining code fragments in B4
#
# Remaining ROM_INCBIN fragment at 0x080736e2..0x080736ed (LAB_080736e2):
#   0x080736e2: movs r1,#0x26 (LAB_080736e2)
#   0x080736e4: adds r3,r0    (LAB_080736e4)
#   0x080736e6..0x080736e9: bl call
#   0x080736ea: movs r0,#0x7d (LAB_080736ea)
#   0x080736ec: b (back-branch)
#   0x080736ee: machine_dup_sub_36ee (next stub, already disassembled)
#
# Also, LAB_080736ea at 0x080736ea is within this block.
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
    print("=== RefineF09Seg5aPoolFix5 (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    if DRY:
        print("[dry] clearListing 0x080736e2..0x080736ed")
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x080736e2 (LAB_080736e2)")
        print("[dry] DisassembleCommand @ 0x080736ea (LAB_080736ea)")
        return

    # Disassemble the final fragment containing LAB_080736e2/e4/ea
    print("\n--- Final fragment: 0x080736e2..0x080736ed ---")
    a_lo = _addr(0x080736e2)
    a_hi = _addr(0x080736ed)
    print("[FIX5.1] clearListing 0x080736e2..0x080736ed")
    try:
        clearListing(a_lo, a_hi)
        print("         done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[FIX5.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("         TMode set")
    print("[FIX5.3] DisassembleCommand @ 0x080736e2 (LAB_080736e2)")
    cmd = DisassembleCommand(_addr(0x080736e2), None, False)
    if cmd.applyTo(currentProgram):
        print("         disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    # Also disasm LAB_080736ea entry directly since it's a branch target
    print("[FIX5.4] DisassembleCommand @ 0x080736ea (LAB_080736ea)")
    cmd2 = DisassembleCommand(_addr(0x080736ea), None, False)
    if cmd2.applyTo(currentProgram):
        print("         disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd2.getStatusMsg())

    # Verify
    for lab_addr, lab_name in [(0x080736d2, 'LAB_080736d2'),
                                (0x080736e2, 'LAB_080736e2'),
                                (0x080736e4, 'LAB_080736e4'),
                                (0x080736ea, 'LAB_080736ea')]:
        ea = _addr(lab_addr)
        syms = [s.getName() for s in sym_tbl.getSymbols(ea)]
        if lab_name in syms:
            print("[OK] %s defined" % lab_name)
        else:
            print("[NOTE] %s not in sym_tbl (flow labels created at GAS export time)" % lab_name)

    print("\n=== RefineF09Seg5aPoolFix5 DONE ===")


main()
