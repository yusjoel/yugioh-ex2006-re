# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg9a.py -- fix literal pool constant words in B2/B4/B5 (non-EWRAM values)
#
# After DisassembleF09Seg9aBlocks.py, Ghidra exports non-EWRAM constant pool DWords
# (e.g. 0x000004a4 EQUIP_PHASE_FRAME_OFF, 0x00001ce8 P1LP_BLOCK2_OFF, etc.)
# as .byte sequences rather than .word, causing GAS "invalid offset, value too big".
#
# Affected addresses (identified from GAS errors + ROM scan):
#   B2 (0x080775d0/0xa8):
#     0x080775e0 = 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#     0x080775e8 = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#     0x08077644 = 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
#     0x08077668 = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#     0x0807766c = 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#   B4 (0x08077a3c/0x120):
#     0x08077a64 = 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#     0x08077a6c = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#     0x08077af8 = 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
#     0x08077b1c = 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#     0x08077b24 = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
#   B5 (0x08077b88/0xc8):
#     0x08077c0c = 0x00008056 (small constant; zone-flag related)
#     0x08077c14 = 0x00001daa (offset constant)
#
# NOTE: All EOL/plate text is pure ASCII.

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# All constant pool DWord addresses to force-fix
CONST_POOL_DWORDS = [
    # B2 constant pools
    (0x080775e0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF pool (B2 sub_75d0)'),
    (0x080775e8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8 pool (B2 sub_75d0)'),
    (0x08077644, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF pool (B2 sub_7648)'),
    (0x08077668, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8 pool (B2 default_7670)'),
    (0x0807766c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF pool (B2 default_7670)'),
    # B4 constant pools
    (0x08077a64, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF pool (B4 sub_7a3c)'),
    (0x08077a6c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8 pool (B4 sub_7a3c)'),
    (0x08077af8, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF pool (B4 sub_7ac2)'),
    (0x08077b1c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF pool (B4 sub_7b00)'),
    (0x08077b24, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8 pool (B4 sub_7b00)'),
    # B5 constant pools
    (0x08077c0c, 0x00008056, 'zone-flag constant pool (B5 sub_7bb6)'),
    (0x08077c14, 0x00001daa, 'offset constant pool (B5 sub_7c18)'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check_val(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        return actual == (expected & 0xFFFFFFFF)
    except:
        return False

def _force_dword(addr_int, expected, desc):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()

    if not _check_val(addr_int, expected):
        print("[WARN] value mismatch @ 0x%08x -- skipping %s" % (addr_int, desc))
        return

    if DRY:
        print("[dry] force_dword @ 0x%08x = 0x%08x  %s" % (addr_int, expected, desc))
        return

    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x = 0x%08x  %s" % (addr_int, expected, desc))
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s (%s)" % (addr_int, e, desc))

def main():
    print("=== PoolFixF09Seg9a (DRY=%s) ===" % DRY)
    print("  %d constant pool DWords to force-fix" % len(CONST_POOL_DWORDS))

    for (addr, val, desc) in CONST_POOL_DWORDS:
        _force_dword(addr, val, desc)

    print("\n=== PoolFixF09Seg9a DONE ===")

main()
