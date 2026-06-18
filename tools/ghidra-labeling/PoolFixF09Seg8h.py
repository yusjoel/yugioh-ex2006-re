# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8h.py -- p5 file09 Seg-8 final pool fix pass H
#
# After pass G, still one undefined reference:
#   LAB_08076750 (referenced from 0807672e)
#
# Pass G disassembled 0x76744..0x76747 (movs r0,#4 + b LAB_08076752),
# but 'b' stopped flow. The remainder 0x76748..0x76751 is still .byte:
#   0x76748: movs r0,#8       (target of beq from 0x76728)
#   0x7674a: ldrh r1,[r4,#8]
#   0x7674c: orrs r0,r1
#   0x7674e: b LAB_08076756
#   0x76750: movs r0,#0x10    (target of beq from 0x7672e)
#
# Fix: disassemble 0x76748..0x76751 separately.

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

CODE_SECTIONS = [
    (0x08076748, 0x08076751, 'mustering_dark_scorpions_sub_66d8_cases_0x48_to_0x51'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)

def _disasm(sa, hi, label):
    if DRY:
        print("[dry] disasm %s 0x%08x..0x%08x" % (label, sa, hi))
        return
    stub_lo = _addr(sa)
    stub_hi = _addr(hi)
    try:
        clearListing(stub_lo, stub_hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x: %s" % (sa, e))
    _set_tmode(sa, hi)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s 0x%08x..0x%08x" % (label, sa, hi))

def main():
    print("=== PoolFixF09Seg8h (DRY=%s) ===" % DRY)
    print("  Disasm 0x76748..0x76751 (LAB_08076750 target)")

    for (sa, hi, label) in CODE_SECTIONS:
        _disasm(sa, hi, label)

    print("\n=== PoolFixF09Seg8h DONE ===")

main()
