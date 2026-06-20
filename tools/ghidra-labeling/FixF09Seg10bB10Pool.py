# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF09Seg10bB10Pool.py -- Fix ROM_INCBIN residue in B10 sub_9df0
#
# Problem: B10 sub_9df0 [0x79df0..0x79e4d] has a literal pool at 0x79e04/0x79e08
# that causes disasm to stop after the 'b LAB_79e4e' at 0x79e00.
# The code continuation at 0x79e0c..0x79e4d was not disassembled.
#
# Structure of sub_9df0:
#   [0x79df0..0x79e00]: code path 1 -> 'b 0x79e4e' (exits stub)
#   [0x79e02]:           2-byte alignment pad
#   [0x79e04..0x79e0b]: DWord pool (gP1LifePoints, P1LP_BLOCK2_OFF_1CE8) -- already forced
#   [0x79e0c..0x79e2a]: code path 2 -> 'b 0x79e50' (branches to default epilogue)
#   [0x79e2c..0x79e4c]: code path 3 -> 'b 0x79e50' (branches to default epilogue)
#   (0x79e4e = neo_daedalus_lp_default_9e4e entry)
#
# Fix: clearListing+setTMode+disasm at 0x79e0c (covers paths 2+3)
# Also fix 0x79e02 alignment pad (2 bytes = .hword/.byte pad)
#
# Branch targets LAB_08079e2c and LAB_08079e4a are within paths 2+3 -> resolved.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=1 for 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")

def _disasm_at(sa, hi_int, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(hi_int)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, sa))

def main():
    print("=== FixF09Seg10bB10Pool ===")
    print("  Fixing ROM_INCBIN residue at 0x79e0c..0x79e4d (sub_9df0 code paths 2+3)")

    lo = _addr(0x08079e0c)
    hi = _addr(0x08079e4d)

    # Clear listing for the residue range
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x08079e0c..0x08079e4d")
    except Exception as e:
        print("[warn] clearListing: %s" % e)

    # setTMode for the residue range
    _set_tmode(0x08079e0c, 0x08079e4d)

    # Disasm from 0x79e0c (code path 2 start, falls through from 0x79e00 pool)
    # This covers: 0x79e0c..0x79e2a (path2), 0x79e2c..0x79e4c (path3, fallthrough from bne)
    # Path 3 start at 0x79e2c is a branch target (LAB_08079e2c) from bne @ 0x79d5c
    # Path 3 code at 0x79e4a is branch target (LAB_08079e4a) from multiple branches
    #
    # Both paths 2 and 3 end with 'b' that jumps out of this range -> disasm stops naturally
    # Disassemble with unrestricted range to allow all branches to be resolved
    _disasm_at(0x08079e0c, 0x08079e4d, 'sub_9df0_path2')

    # Also disasm from 0x79e2c in case path2 ends before reaching path3
    # (path2 ends at b+0x79e2a, path3 starts at 0x79e2c which is a separate branch target)
    try:
        lo2 = _addr(0x08079e2c)
        hi2 = _addr(0x08079e4d)
        clearListing(lo2, hi2)
        ctx = currentProgram.getProgramContext()
        tmode = ctx.getRegister("TMode")
        if tmode is not None:
            ctx.setValue(tmode, lo2, hi2, BigInteger.ONE)
        cmd = DisassembleCommand(lo2, AddressSet(lo2, hi2), True)
        if cmd.applyTo(currentProgram):
            print("[ok ] disasm sub_9df0_path3 @ 0x08079e2c")
        else:
            print("[warn] disasm path3: %s" % cmd.getStatusMsg())
    except Exception as e:
        print("[warn] path3 disasm: %s" % e)

    print("=== FixF09Seg10bB10Pool DONE ===")
    print("  Expected: LAB_08079e2c and LAB_08079e4a now resolved as code labels")

main()
