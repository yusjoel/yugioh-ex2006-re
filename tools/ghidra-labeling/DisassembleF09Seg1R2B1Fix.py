# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg1R2B1Fix.py -- Fix B1 eligible_destiny_board_f85c body
#   The main script left ROM_INCBIN 0x6f85e/0xf6 (0x6f85e..0x6f953).
#   This script clears that range and disassembles it.
#   Also ensures pool DWORDs at 0x6f92c/30/34 are created.
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
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


def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")


def _clear_listing(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))


def _disasm_at(stub_lo_int, stub_hi_int, label):
    lo = _addr(stub_lo_int)
    hi = _addr(stub_hi_int)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, stub_lo_int, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, stub_lo_int))


def _disasm_unrestricted(start_int, label):
    """Disassemble without upper address bound (follow flow)."""
    lo = _addr(start_int)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, start_int, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm (unrestricted) %s @ 0x%08x" % (label, start_int))


def _force_dword(addr_int):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))


def _count_instrs(lo_int, hi_int):
    listing = currentProgram.getListing()
    lo_a = _addr(lo_int)
    hi_a = _addr(hi_int)
    n = 0
    inst = listing.getInstructionAt(lo_a)
    while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


def main():
    print("=== DisassembleF09Seg1R2B1Fix (DRY=%s) ===" % DRY)
    print("  Fixing B1 eligible_destiny_board_f85c body ROM_INCBIN 0x6f85e/0xf6")
    print("  Code region: 0x6f85e..0x6f953 (0xf6 bytes of THUMB instructions)")

    if DRY:
        print("[dry] clearListing(0x0806f85e..0x0806f953)")
        print("[dry] setTMode=THUMB 0x0806f85e..0x0806f953")
        print("[dry] DisassembleCommand(0x0806f85e) unrestricted")
        print("[dry] force_dword 0x0806f92c/30/34")
        return

    # The region 0x6f85e..0x6f953 is the B1 code body
    # Pool DWORDs at 0x6f92c/30/34 are INSIDE this range
    # Strategy: clear code only up to 0x6f92b (before first pool), disasm, then create pools
    print("\n--- Phase 1: clearListing 0x6f85e..0x6f92b (code only, before pool cluster) ---")
    _clear_listing(0x0806f85e, 0x0806f92b)
    _set_tmode(0x0806f85e, 0x0806f953)

    print("\n--- Phase 2: DisassembleCommand from 0x6f85e (unrestricted flow) ---")
    # Use unrestricted disasm to let Ghidra follow flow naturally
    # The b @ 0x6f952 will cause flow to stop (unconditional branch)
    _disasm_unrestricted(0x0806f85e, 'eligible_destiny_board_f85c_body_fix')
    n = _count_instrs(0x0806f85e, 0x0806f92b)
    print("    [check] %d instructions in 0x6f85e..0x6f92b" % n)

    print("\n--- Phase 3: force_dword for pools 0x6f92c/30/34 ---")
    _force_dword(0x0806f92c)
    _force_dword(0x0806f930)
    _force_dword(0x0806f934)

    n_total = _count_instrs(0x0806f85e, 0x0806f951)
    print("    [check] %d total instructions in B1 code region 0x6f85e..0x6f951" % n_total)

    print("\n=== DisassembleF09Seg1R2B1Fix DONE ===")


main()
