# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8g.py -- p5 file09 Seg-8 final pool fix pass G
#
# After pass F, linker reports two undefined references:
#   LAB_08076748 (referenced from 08076728)
#   LAB_08076750 (referenced from 0807672e)
#
# Both are inside a .byte block at LAB_08076744 (0x76744..0x76751):
#   0x76744: movs r0,#4   \ case for CID match
#   0x76746: b LAB_08076752
#   0x76748: movs r0,#8   \ branch target (beq from 0x76728)
#   0x7674a: ldrh r1,[r4,#8]
#   0x7674c: orrs r0,r1
#   0x7674e: b LAB_08076756
#   0x76750: movs r0,#0x10  \ branch target (beq from 0x7672e)
#   (0x76752..0x76757: already disassembled as LAB_08076752 etc)
#
# Root cause: pass E's sub_66d8_tail range (0x7673c..0x76751) only got
# partially disassembled -- Ghidra stopped at the 'b LAB_08076756' branch
# at 0x76742 without continuing into 0x76744.
#
# Fix: force-clearListing 0x76744..0x76751 and disasm that specific sub-range.

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

# Sub-range to disassemble: 0x76744..0x76751
# (These are 14 bytes of THUMB code currently exported as .byte)
CODE_SECTIONS = [
    (0x08076744, 0x08076751, 'mustering_dark_scorpions_sub_66d8_cases_0x44_to_0x51'),
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
    print("=== PoolFixF09Seg8g (DRY=%s) ===" % DRY)
    print("  Disasm 0x76744..0x76751 (LAB_08076748 + LAB_08076750 targets)")

    for (sa, hi, label) in CODE_SECTIONS:
        _disasm(sa, hi, label)

    print("\n=== PoolFixF09Seg8g DONE ===")

main()
