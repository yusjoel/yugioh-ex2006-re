# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8c.py -- p5 file09 Seg-8 literal pool fix pass C (third round)
#
# sub_6616 body (0x08076616..0x080766a3) was cleared by PoolFixF09Seg8b.py when
# it clearListing'd 0x65f0..0x666b (to re-disasm sub_65f0). This clobbered the
# sub_6616 disasm done in PoolFixF09Seg8.py.
#
# Solution: re-disassemble sub_6616 AFTER the pool cluster at 0x666c is stable.
# The pool DWords at 0x666c/670/674/678 are already correct (.word) from pass B.
# Just need to clearListing + disasm the code at 0x76616..0x7666b.

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

def _disasm_at(sa, hi, label):
    if DRY:
        print("[dry] disasm %s @ 0x%08x..0x%08x" % (label, sa, hi))
        return
    stub_lo = _addr(sa)
    stub_hi = _addr(hi)
    try:
        clearListing(stub_lo, stub_hi)
    except Exception as e:
        print("[warn] clearListing for redisasm %s: %s" % (label, e))
    _set_tmode(sa, hi)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x..0x%08x" % (label, sa, hi))

def main():
    print("=== PoolFixF09Seg8c (DRY=%s) ===" % DRY)
    print("  Re-disasm mustering_dark_scorpions_sub_6616 body (0x76616..0x766a3)")
    print("  (Was clobbered when PoolFixF09Seg8b clearListing'd 0x65f0..0x666b)")
    print()

    # sub_6616 body: 0x08076616..0x080766a3
    # (do NOT go past 0x666b which is the code end; pool at 0x666c is already DWord)
    # Actually the sub body code goes from 0x76616 all the way to 0x766a7 (end before sub_66a8)
    # But 0x6678 pool and 0x666c pool are already force_dword'd
    # So disasm the whole range 0x76616..0x766a7 (code + already-fixed pools)
    _disasm_at(0x08076616, 0x080766a7, 'mustering_dark_scorpions_sub_6616')

    print("\n=== PoolFixF09Seg8c DONE ===")

main()
