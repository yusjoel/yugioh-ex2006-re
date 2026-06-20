# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF09Seg9bPools.py -- Fix missing pool DWord definitions in Seg-9b blocks B7/B9
#
# Problem: DisassembleF09Seg9bBlocks.py missed force_dword for 4 pool words
# that Ghidra exported as .byte sequences, causing assembler errors:
#
#   asm/09 L21629: ldr r1, DAT_08077f98  -- 0x08077f98 = 0x080507ad (fn_ptr)
#   asm/09 L22135: ldr r1, DAT_08078394  -- 0x08078394 = 0x0201c4e0 (gP1LifePoints)
#   asm/09 L22139: ldr r0, DAT_08078398  -- 0x08078398 = 0x00000868 (PLAYER_BLOCK_STRIDE)
#   asm/09 L22170: ldr r7, DAT_08078454  -- 0x08078454 = 0x00000868 (PLAYER_BLOCK_STRIDE)
#
# Root cause: DisassembleF09Seg9bBlocks.py only force_dword'd:
#   B7: 0x08077fcc/0x7ff0/0x7ff4/0x7ff8 (but missed 0x08077f98)
#   B9: no pool force_dword (assumed auto-detect, but that failed for 3 slots)
#
# Fix: force_dword at the 4 missing pool addresses.
# These are within already-disassembled blocks, so clearListing only targets the 4B pool.

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

MISSING_POOLS = [
    # (addr, expected_value, context_note)
    (0x08077f98, 0x080507ad, "B7 sub_7f86 pool: fn_ptr invoke_count_zone_pair_hits_full_range"),
    (0x08078394, 0x0201c4e0, "B9 sub_8368 pool[0]: gP1LifePoints"),
    (0x08078398, 0x00000868, "B9 sub_8368 pool[1]: PLAYER_BLOCK_STRIDE"),
    (0x08078454, 0x00000868, "B9 sub_83a8 pool[1]: PLAYER_BLOCK_STRIDE"),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] read 0x%08x: %s" % (addr_int, e))
        return False
    if actual != (expected & 0xFFFFFFFF):
        print("[FAIL] 0x%08x: got 0x%08x expected 0x%08x" % (addr_int, actual, expected & 0xFFFFFFFF))
        return False
    return True

def _force_dword(addr_int, expected, note):
    print("\n  Pool @ 0x%08x: %s" % (addr_int, note))
    if not _check(addr_int, expected):
        print("  [SKIP] value mismatch")
        return

    if DRY:
        print("  [dry] force_dword @ 0x%08x (expected 0x%08x)" % (addr_int, expected & 0xFFFFFFFF))
        return

    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
        print("  [ok ] clearListing @ 0x%08x..0x%08x" % (addr_int, addr_int + 3))
    except Exception as e:
        print("  [warn] clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("  [ok ] force_dword @ 0x%08x = 0x%08x" % (addr_int, expected & 0xFFFFFFFF))
    except Exception as e:
        print("  [warn] createData @ 0x%08x: %s" % (addr_int, e))

def main():
    print("=== FixF09Seg9bPools (DRY=%s) ===" % DRY)
    print("Fixing %d missing pool DWord definitions in B7/B9 blocks" % len(MISSING_POOLS))

    for (addr, exp, note) in MISSING_POOLS:
        _force_dword(addr, exp, note)

    print("\n=== FixF09Seg9bPools DONE ===")
    print("Fixed pool DWords:")
    for (addr, exp, note) in MISSING_POOLS:
        print("  0x%08x = 0x%08x  %s" % (addr, exp & 0xFFFFFFFF, note))

main()
