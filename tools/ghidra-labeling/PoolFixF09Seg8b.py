# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8b.py -- p5 file09 Seg-8 literal pool fix pass B (second round)
#
# Fixes pool words that were merged into .byte blocks by Ghidra after the first
# PoolFixF09Seg8.py pass. In particular:
#
# B2 cluster at 0x0807666c (was a 16-byte .byte block; PoolFix1 did 666c/674/678 but
#   Ghidra re-merged because adjacent words were also .byte):
#   0x0807666c: 0x0201c4e0 (gP1LifePoints) -- covered by PoolFix1 but re-merged
#   0x08076670: 0x00000868 (PLAYER_BLOCK_STRIDE) -- MISSING from PoolFix1
#   0x08076674: 0x0201e2a8 -- covered by PoolFix1 but re-merged
#   0x08076678: 0x08076511 (ROM code ptr) -- covered by PoolFix1 but re-merged
#
# B4 cluster at 0x08076884:
#   0x08076884: 0x0201c4e0 (gP1LifePoints) -- MISSING from PoolFix1
#   0x08076888: 0x00000868 (PLAYER_BLOCK_STRIDE) -- MISSING from PoolFix1
#
# Also: re-disassemble the sub_65f0 leading code that references 0x666c..0x678

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

# ---------------------------------------------------------------------------
# Pool DWords that need force_dword (second round)
# ---------------------------------------------------------------------------
POOL_FIXES = [
    # B2 cluster at 0x666c (all 4 DWords in the merged .byte block)
    (0x0807666c, 0x0201c4e0, 'B2 gP1LifePoints pool (re-force)'),
    (0x08076670, 0x00000868, 'B2 PLAYER_BLOCK_STRIDE pool (missing from pass1)'),
    (0x08076674, 0x0201e2a8, 'B2 EWRAM addr pool (re-force)'),
    (0x08076678, 0x08076511, 'B2 ROM code ptr pool (re-force)'),
    # B4 cluster at 0x6884
    (0x08076884, 0x0201c4e0, 'B4 gP1LifePoints pool (missing from pass1)'),
    (0x08076888, 0x00000868, 'B4 PLAYER_BLOCK_STRIDE pool (missing from pass1)'),
]

# Code regions to re-disassemble after force_dword
# sub_65f0 body that references the 0x666c cluster
REDISASM_REGIONS = [
    # mustering_dark_scorpions_sub_65f0: 0x080765f0..0x0807666b
    (0x080765f0, 0x0807666b, 'mustering_dark_scorpions_sub_65f0'),
    # Code after 0x6678 cluster: 0x0807667c..0x080766a3
    (0x0807667c, 0x080766a3, 'mustering_dark_scorpions_sub_6616_after_cluster'),
    # B4: spell_vanishing_sub_67f8 leading up to 0x6884 cluster
    (0x080767f8, 0x08076883, 'spell_vanishing_sub_67f8_to_6884'),
    # B4: spell_vanishing_sub_6818 after 0x688c
    (0x08076890, 0x08076907, 'spell_vanishing_sub_6890_to_end'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _force_dword(addr_int, expected_val, desc):
    if not _check(addr_int, expected_val, desc):
        print("[SKIP] force_dword 0x%08x: value mismatch" % addr_int)
        return
    if DRY:
        print("[dry] force_dword 0x%08x (%s)" % (addr_int, desc))
        return
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x  (0x%08x  %s)" % (addr_int, expected_val & 0xFFFFFFFF, desc))
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

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

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== PoolFixF09Seg8b (DRY=%s) ===" % DRY)
    print("  Fixing %d pool DWords + %d re-disasm regions" % (len(POOL_FIXES), len(REDISASM_REGIONS)))

    print("\n--- Force DWord pool fixes (pass B) ---")
    for (addr, val, desc) in POOL_FIXES:
        _force_dword(addr, val, desc)

    print("\n--- Re-disassemble code regions ---")
    for (sa, hi, label) in REDISASM_REGIONS:
        _disasm_at(sa, hi, label)

    print("\n=== PoolFixF09Seg8b DONE ===")

main()
