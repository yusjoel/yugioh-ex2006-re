# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8f.py -- p5 file09 Seg-8 final pool fix pass F
#
# spell_vanishing_sub_6818 body (0x76818..0x7688f) was clearListing'd in pass E,
# wiping the pools at 0x76884/888/88c. Solution: split disasm at pool boundaries.
#
# B4 structure around 0x76884:
#   sub_6818 code: 0x76818..0x76883 (ends before pool cluster at 0x76884)
#   pool cluster: 0x76884 (gP1LifePoints) + 0x76888 (PLAYER_BLOCK_STRIDE) + 0x7688c (mask)
#   sub_6890 starts: 0x76890

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

POOL_DWORDS = [
    (0x08076884, 0x0201c4e0),
    (0x08076888, 0x00000868),
    (0x0807688c, 0xfffffeec),
]

CODE_SECTIONS = [
    # sub_6818 body: ends at 0x76883 (before pool at 0x76884)
    (0x08076818, 0x08076883, 'spell_vanishing_sub_6818_pre_pool'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _force_dword(addr_int, expected_val):
    if DRY:
        print("[dry] force_dword 0x%08x" % addr_int)
        return
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        pass
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword 0x%08x (0x%08x)" % (addr_int, expected_val & 0xFFFFFFFF))
    except Exception as e:
        print("[warn] force_dword 0x%08x: %s" % (addr_int, e))

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
    print("=== PoolFixF09Seg8f (DRY=%s) ===" % DRY)
    print("  %d pool fixes + %d code sections" % (len(POOL_DWORDS), len(CODE_SECTIONS)))

    print("\n--- Step 1: Disasm code sections (no pool overlap) ---")
    for (sa, hi, label) in CODE_SECTIONS:
        _disasm(sa, hi, label)

    print("\n--- Step 2: Force pool DWords after disasm ---")
    for (addr, val) in POOL_DWORDS:
        _force_dword(addr, val)

    print("\n=== PoolFixF09Seg8f DONE ===")

main()
