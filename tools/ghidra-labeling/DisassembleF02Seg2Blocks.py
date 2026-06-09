# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF02Seg2Blocks.py -- f02 Seg-2 R4 disasm (2 blocks)
#   Block1: 0x0802e22c..0x0802e3c7 (0x19c B) -- phase dispatch handlers (8-entry table)
#     4 raw refs from dispatch table at 0x0802e20c (entries [1..4] -> 0x0802e22c)
#     Dispatch via: MOV PC, R0 (THUMB high-reg transfer, 0x4687) -- T-bit preserved
#     Entry points: 0x0802e22c (entries 1..4), 0x0802e23c (entry 5),
#                   0x0802e2c4 (entry 7), 0x0802e324 (entry 6)
#
#   Block2: 0x0802e554..0x0802e697 (0x144 B) -- sub-state dispatch handlers (8-entry table)
#     2 raw refs from sub-dispatch table at 0x0802e534 (entries [0..1] -> 0x0802e554)
#     Same MOV PC dispatch mechanism.
#     Entry points: 0x0802e554 (entries 0..1), 0x0802e5ac (entries 6..7),
#                   0x0802e5f8 (entries 2..5)
#
# Pattern: DisassembleF01Seg6Blocks.py
#   - clearListing entire block range first (avoid ContextChangeException)
#   - setTMode=THUMB for entire range
#   - per-stub disasm_flow for each entry point (flow continues naturally)
#   - literal pool createDWord for PC-relative ldr targets after disasm
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260610-073415-pre-f02seg2

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import Data
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


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_flow(addr):
    """Disassemble at addr, let flow continue naturally (no size limit)."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _count_instructions(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    listing = currentProgram.getListing()
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


def _create_dword(addr):
    """Create a DWORD data item at addr (for literal pool PC-relative ldr targets)."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.DWordDataType.dataType
    try:
        existing = listing.getDataAt(a)
        if existing is not None and existing.getDataType().equals(dt):
            return True
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr)
        return True
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr, e))
        return False


# ---------------------------------------------------------------------------
# Block1: 0x0802e22c..0x0802e3c7 (0x19c B)
# Entry points from 8-entry dispatch table at 0x0802e20c:
#   entry[0] = 0x0802e3c8 (LAB fallthrough -- outside block, skip)
#   entry[1..4] = 0x0802e22c (same handler for phases 1-4)
#   entry[5] = 0x0802e23c
#   entry[6] = 0x0802e324
#   entry[7] = 0x0802e2c4
# ---------------------------------------------------------------------------
BLOCK1_LO = 0x0802e22c
BLOCK1_HI = 0x0802e3c7  # inclusive end (0x0802e3c8 is next label, outside block)

BLOCK1_ENTRIES = [
    0x0802e22c,  # entries [1..4]: shared phase handler
    0x0802e23c,  # entry [5]: sub-handler A
    0x0802e2c4,  # entry [7]: sub-handler C
    0x0802e324,  # entry [6]: sub-handler B
]

# ---------------------------------------------------------------------------
# Block2: 0x0802e554..0x0802e697 (0x144 B)
# Entry points from 8-entry sub-dispatch table at 0x0802e534:
#   entry[0..1] = 0x0802e554
#   entry[2..5] = 0x0802e5f8
#   entry[6..7] = 0x0802e5ac
# ---------------------------------------------------------------------------
BLOCK2_LO = 0x0802e554
BLOCK2_HI = 0x0802e697  # inclusive end (0x0802e698 is LAB_0802e698, next)

BLOCK2_ENTRIES = [
    0x0802e554,  # entries [0..1]: main sub-handler
    0x0802e5ac,  # entries [6..7]: sub-handler B
    0x0802e5f8,  # entries [2..5]: sub-handler A
]


def main():
    print("=== DisassembleF02Seg2Blocks (DRY=%s) ===" % DRY)
    print("  Block1: 0x%08x..0x%08x (0x19c B, %d entries)" % (
        BLOCK1_LO, BLOCK1_HI, len(BLOCK1_ENTRIES)))
    print("  Block2: 0x%08x..0x%08x (0x144 B, %d entries)" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_ENTRIES)))

    if DRY:
        print("\n[dry] Block1: clearListing+setTMode+%d stubs" % len(BLOCK1_ENTRIES))
        for e in BLOCK1_ENTRIES:
            print("  entry 0x%08x" % e)
        print("[dry] Block2: clearListing+setTMode+%d stubs" % len(BLOCK2_ENTRIES))
        for e in BLOCK2_ENTRIES:
            print("  entry 0x%08x" % e)
        return

    # --- Block 1 ---
    print("\n--- Block1: 0x%08x..0x%08x (%d entries) ---" % (
        BLOCK1_LO, BLOCK1_HI, len(BLOCK1_ENTRIES)))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)

    b1_ok = 0
    for entry in BLOCK1_ENTRIES:
        if _disasm_flow(entry):
            b1_ok += 1
            print("[ok ] Block1 entry 0x%08x" % entry)
        else:
            print("[warn] Block1 entry 0x%08x FAILED" % entry)

    n1 = _count_instructions(BLOCK1_LO, BLOCK1_HI)
    print("[Block1] %d instructions, %d/%d entries ok" % (n1, b1_ok, len(BLOCK1_ENTRIES)))

    # --- Block 2 ---
    print("\n--- Block2: 0x%08x..0x%08x (%d entries) ---" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_ENTRIES)))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)

    b2_ok = 0
    for entry in BLOCK2_ENTRIES:
        if _disasm_flow(entry):
            b2_ok += 1
            print("[ok ] Block2 entry 0x%08x" % entry)
        else:
            print("[warn] Block2 entry 0x%08x FAILED" % entry)

    n2 = _count_instructions(BLOCK2_LO, BLOCK2_HI)
    print("[Block2] %d instructions, %d/%d entries ok" % (n2, b2_ok, len(BLOCK2_ENTRIES)))

    # Summary
    print("\n=== DisassembleF02Seg2Blocks DONE ===")
    print("  Block1=%d instr  Block2=%d instr  Total=%d" % (n1, n2, n1 + n2))


main()
