# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleSeg9BlockB.py -- p5 Seg-9 Block B (R4)
#   Disassemble ROM_INCBIN 0x1ad18, 0xec (236B) = 5 THUMB stub handlers
#   dispatched by dispatch_banlist_cursor_action_jump_table (0x0801ad00)
#   via `mov pc, r0` (raw address dispatch, stays in THUMB mode).
#
#   Stubs:
#     entry[0] 0x0801ad18 -> 0x0801ad20 (8B)
#     entry[2] 0x0801ad20 -> 0x0801ad4c (44B)
#     entry[3] 0x0801ad4c -> 0x0801ad94 (72B)
#     entry[4] 0x0801ad94 -> 0x0801ade0 (76B)
#     entry[5] 0x0801ade0 -> 0x0801ae04 (36B)
#     entry[1] 0x0801ae04 already disassembled (LAB_0801ae04), skip.
#
#   Pattern: Seg-5c-ii (DisassembleSeg5cJpHandlers.py)
#   - clearListing entire range first to avoid ContextChangeException
#   - setTMode=THUMB for entire range
#   - per-stub DisassembleCommand (stubs do NOT fall through; each ends with
#     bx lr / pop {pc} / b target)

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# Range: 0x0801ad18 .. 0x0801ae03 (inclusive) = 0xec bytes = 236B
LO = 0x0801ad18
HI = 0x0801ae03  # = LO + 0xec - 1

# Stub start addresses (per-stub DisassembleCommand)
STUBS = [
    0x0801ad18,   # entry[0] 8B
    0x0801ad20,   # entry[2] 44B
    0x0801ad4c,   # entry[3] 72B
    0x0801ad94,   # entry[4] 76B
    0x0801ade0,   # entry[5] 36B
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== DisassembleSeg9BlockB (DRY=%s) 0x%08x..0x%08x ===" % (DRY, LO, HI))
    lo = _addr(LO)
    hi = _addr(HI)
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] would clearListing(0x%08x..0x%08x) + setTMode=THUMB + per-stub DisassembleCommand for %d stubs" % (LO, HI, len(STUBS)))
        for sa in STUBS:
            print("  stub 0x%08x" % sa)
        return

    # 1) Clear entire range first (mandatory before setTMode to avoid ContextChangeException)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (LO, HI))
    except Exception as e:
        print("[warn] clearListing: %s" % e)

    # 2) Set TMode=THUMB for entire range
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=1 for 0x%08x..0x%08x" % (LO, HI))
    else:
        print("[warn] TMode register not found")

    # 3) Per-stub DisassembleCommand
    # Each stub is a standalone THUMB code block; flow exits at each stub's
    # branch (bx lr / pop {pc} / b target). Use the stub range to limit.
    stub_sizes = [8, 44, 72, 76, 36]
    for i, sa in enumerate(STUBS):
        stub_lo = _addr(sa)
        stub_hi = _addr(sa + stub_sizes[i] - 1)
        cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
        if not cmd.applyTo(currentProgram):
            print("[warn] disasm stub[%d] 0x%08x: %s" % (i, sa, cmd.getStatusMsg()))
        else:
            print("[ok ] disasm stub[%d] 0x%08x (%dB)" % (i, sa, stub_sizes[i]))

    # 4) Count instructions disassembled
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[done] %d instructions in 0x%08x..0x%08x (expected ~118 halfwords)" % (n, LO, HI))
    print("=== DisassembleSeg9BlockB DONE ===")


main()
