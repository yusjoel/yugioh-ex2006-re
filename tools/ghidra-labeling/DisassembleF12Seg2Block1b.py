# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF12Seg2Block1b.py -- file 12 Seg-2 Block1 sub-stub fix
#
# After DisassembleF12Seg2Block1.py ran, ROM_INCBIN 0x952d4/0x30 remains
# because DisassembleCommand for case[2] stopped at DWORD_080952cc pool words.
# The branch targets LAB_080952f2 and LAB_080952fc are inside this sub-block.
#
# This script disassembles the remaining code at 0x080952d4..0x08095303
# (the continuation of case[2]: dispatch_effect_slot_by_display_state branch path).
#
# NOTE: All text is pure ASCII.

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


# Sub-block range: 0x080952d4..0x08095303 (0x30 bytes)
SUB_START = 0x080952d4
SUB_END   = 0x08095303  # inclusive

# Entry point for disassembly (LAB_080952d4)
SUB_ENTRY = 0x080952d4


def main():
    print("=== DisassembleF12Seg2Block1b (DRY=%s) ===" % DRY)
    print("  Sub-block: 0x080952d4..0x08095303 (0x30 bytes)")
    print("  Fix: disassemble remaining code after case[2] pool words")

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    a_lo = _addr(SUB_START)
    a_hi = _addr(SUB_END)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (SUB_START, SUB_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] DisassembleCommand @ 0x%08x (LAB_080952d4)" % SUB_ENTRY)
        print("[dry] done")
        return

    # Step 1: clearListing
    print("[1] clearListing 0x%08x..0x%08x" % (SUB_START, SUB_END))
    try:
        clearListing(a_lo, a_hi)
        print("    done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1 for 0x%08x..0x%08x" % (SUB_START, SUB_END))
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("    TMode set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand at sub-block entry
    print("[3] DisassembleCommand @ 0x%08x" % SUB_ENTRY)
    ea = _addr(SUB_ENTRY)
    cmd = DisassembleCommand(ea, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok")
    else:
        print("    [WARN] disasm: %s" % cmd.getStatusMsg())

    print("\n=== DisassembleF12Seg2Block1b DONE ===")
    print("  Sub-block 0x080952d4..0x08095303 disassembled")
    print("  POST-CHECK: grep ROM_INCBIN/.byte in [0x08095274, 0x08095334) must == 0")


main()
