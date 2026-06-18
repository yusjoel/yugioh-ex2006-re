# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg7b.py -- second-pass pool fix for B4 and B6 (DWords only, no re-disasm)
#   The first pass (PoolFixF09Seg7.py) forced DWords then re-disasmed stubs,
#   but the redisasm clearListing overwrote the forced DWords within stub ranges.
#   This pass forces all pool DWords AFTER the disasm is already done.
#
# Same DWord list as PoolFixF09Seg7.py -- no redisasm this pass.

from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

POOL_DWORDS = [
    # B4: DAT_08075dbc (2x)
    0x08075dbc,
    0x08075dc0,
    # B4: DAT_08075e10 (4x)
    0x08075e10,
    0x08075e14,
    0x08075e18,
    0x08075e1c,
    # B4: DAT_08075e40 (1x)
    0x08075e40,
    # B4: DAT_08075e7c (4x)
    0x08075e7c,
    0x08075e80,
    0x08075e84,
    0x08075e88,
    # B4: DAT_08075eb4 (3x)
    0x08075eb4,
    0x08075eb8,
    0x08075ebc,
    # B4: DAT_08075ef0 (2x)
    0x08075ef0,
    0x08075ef4,
    # B6: DAT_08076004 (2x)
    0x08076004,
    0x08076008,
    # B6: DAT_0807602c (1x)
    0x0807602c,
    # B6: DAT_08076074 (4x)
    0x08076074,
    0x08076078,
    0x0807607c,
    0x08076080,
    # B6: DAT_080760f4 (3x)
    0x080760f4,
    0x080760f8,
    0x080760fc,
    # B6: DAT_08076150 (3x)
    0x08076150,
    0x08076154,
    0x08076158,
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _force_dword(addr_int):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

def main():
    print("=== PoolFixF09Seg7b (DRY=%s) ===" % DRY)
    print("  Force-DWord only (no re-disasm): %d pool words" % len(POOL_DWORDS))

    if DRY:
        for a in POOL_DWORDS:
            print("[dry] force_dword @ 0x%08x" % a)
        return

    for a in POOL_DWORDS:
        _force_dword(a)

    print("\n=== PoolFixF09Seg7b DONE ===")
    print("  Forced %d DWords" % len(POOL_DWORDS))


main()
