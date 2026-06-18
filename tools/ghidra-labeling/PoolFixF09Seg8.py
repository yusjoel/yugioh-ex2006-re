# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8.py -- p5 file09 Seg-8 literal pool fix pass
#
# Fixes remaining .byte pool words in B2/B4 blocks that were not covered by
# the initial DisassembleF09Seg8Blocks.py force_dword list.
#
# B2 (mustering_dark_scorpions sub-stubs 0x765f0..0x7678b):
#   0x080766a4: 0x00000868 (PLAYER_BLOCK_STRIDE - emitted as .byte)
#   0x080766d0: 0x00001d70 (LP_BANISHER_CTX_OFF - emitted as .byte)
#   0x08076714: 0x00000868 (PLAYER_BLOCK_STRIDE - emitted as .byte)
#   0x0807671c: 0x00001656 (DARK_SCORPION_CHICK_CID - emitted as .byte)
#   0x08076720: 0x00001531 (DARK_SCORPION_BURGLARS_CID - emitted as .byte)
#   0x08076734: 0x00001685 (DARK_SCORPION_GORG_THE_STRONG_CID - emitted as .byte)
#
# B4 (spell_vanishing sub-stubs 0x767f8..0x76907):
#   0x0807688c: 0xfffffeec (raw mask constant - emitted as .byte)
#
# After force_dword, re-disassemble affected code regions to restore instructions.

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
# Pool DWords that need force_dword (missed in initial disasm pass)
# ---------------------------------------------------------------------------
# (addr, value, description)
POOL_FIXES = [
    # B2 fixes
    (0x080766a4, 0x00000868, 'B2 PLAYER_BLOCK_STRIDE pool'),
    (0x080766d0, 0x00001d70, 'B2 LP_BANISHER_CTX_OFF pool'),
    (0x08076714, 0x00000868, 'B2 PLAYER_BLOCK_STRIDE pool (2nd)'),
    (0x0807671c, 0x00001656, 'B2 DARK_SCORPION_CHICK_CID pool'),
    (0x08076720, 0x00001531, 'B2 DARK_SCORPION_BURGLARS_CID pool'),
    (0x08076734, 0x00001685, 'B2 DARK_SCORPION_GORG_THE_STRONG_CID pool'),
    # B4 fixes
    (0x0807688c, 0xfffffeec, 'B4 raw mask constant pool'),
]

# Code regions to re-disassemble after force_dword (only if code was broken)
# Each: (start, end, label) - re-disassemble the code that leads up to each pool
REDISASM_REGIONS = [
    # B2: sub_6616 body (0x08076616..0x080766a3 = before 0x080766a4 pool)
    (0x08076616, 0x080766a3, 'mustering_dark_scorpions_sub_6616_redisasm'),
    # B2: code after DWORD_080766cc (0x080766d4..0x080766cf = before 0x080766d0 pool)
    # Actually 0x080766d0 is right before sub_66d8 starts at 0x080766d8
    # sub_66d8 body: 0x080766d8..0x08076713 (before 0x08076714 pool)
    (0x080766d8, 0x08076713, 'mustering_dark_scorpions_sub_66d8_redisasm'),
    # B2: code from 0x08076718 (after DWORD_08076718) to before 0x08076720 pool
    # Actually 0x0807671c is a pool and 0x08076720 is a pool; code is at 0x08076722..0x08076733
    (0x08076722, 0x08076733, 'mustering_dark_scorpions_sub_66d8_part2_redisasm'),
    # B2: sub_6780 body: 0x08076780..0x0807678b
    (0x08076780, 0x0807678b, 'mustering_dark_scorpions_sub_6780_redisasm'),
    # B4: code at 0x08076870..0x0807688b (before 0x0807688c pool)
    (0x08076870, 0x0807688b, 'spell_vanishing_sub_68b8_redisasm'),
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
    # clearListing first to avoid ContextChangeException
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
    print("=== PoolFixF09Seg8 (DRY=%s) ===" % DRY)
    print("  Fixing %d pool DWords + %d re-disasm regions" % (len(POOL_FIXES), len(REDISASM_REGIONS)))

    print("\n--- Force DWord pool fixes ---")
    for (addr, val, desc) in POOL_FIXES:
        _force_dword(addr, val, desc)

    print("\n--- Re-disassemble code regions ---")
    for (sa, hi, label) in REDISASM_REGIONS:
        _disasm_at(sa, hi, label)

    print("\n=== PoolFixF09Seg8 DONE ===")

main()
