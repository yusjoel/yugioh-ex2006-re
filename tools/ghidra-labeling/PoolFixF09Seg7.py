# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg7.py -- pool fix for B4 and B6 inline literal pool words
#   Forces all remaining .byte-exported pool DWords to proper DWord data type.
#   Fixes GAS "invalid offset, value too big (0xFFFFFFFC)" errors.
#
# B4 pools (in magical_dim sub-stubs):
#   DAT_08075dbc: 2 DWords (0x75dbc, 0x75dc0)
#   DAT_08075e10: 4 DWords (0x75e10, 0x75e14, 0x75e18, 0x75e1c)
#   DAT_08075e40: 1 DWord  (0x75e40)  [gDuelCardCtxBase]
#   DAT_08075e7c: 4 DWords (0x75e7c, 0x75e80, 0x75e84, 0x75e88)
#   DAT_08075eb4: 3 DWords (0x75eb4, 0x75eb8, 0x75ebc)
#   DAT_08075ef0: 2 DWords (0x75ef0, 0x75ef4)
#
# B6 pools (in friendship sub-stubs):
#   DAT_08076004: 2 DWords (0x76004, 0x76008)
#   DAT_0807602c: 1 DWord  (0x7602c)  [alignment: 0x0000 pad at 0x7602a, DWord at 0x7602c]
#   DAT_08076074: 4 DWords (0x76074, 0x76078, 0x7607c, 0x76080)
#   DAT_080760f4: 3 DWords (0x760f4, 0x760f8, 0x760fc) [2B pad at 0x760f2]
#   DAT_08076150: 3 DWords (0x76150, 0x76154, 0x76158)
#
# NOTE: After force-DWord, re-disasm sub-stubs if needed.
# All labels pure ASCII. No CJK.

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

# All pool DWord addresses to force
POOL_DWORDS = [
    # B4: DAT_08075dbc (2x)
    0x08075dbc,
    0x08075dc0,
    # B4: DAT_08075e10 (4x)
    0x08075e10,
    0x08075e14,
    0x08075e18,
    0x08075e1c,
    # B4: DAT_08075e40 (1x) - gDuelCardCtxBase
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
    # B6: DAT_0807602c (1x) - OAM tile code (alignment pad 0x0000 at 0x7602a)
    0x0807602c,
    # B6: DAT_08076074 (4x)
    0x08076074,
    0x08076078,
    0x0807607c,
    0x08076080,
    # B6: DAT_080760f4 (3x) - 2B pad at 0x760f2
    0x080760f4,
    0x080760f8,
    0x080760fc,
    # B6: DAT_08076150 (3x)
    0x08076150,
    0x08076154,
    0x08076158,
]

# Sub-stubs that need re-disasm after pool fix (those whose code follows a pool)
# Format: (start_addr, end_addr, label)
REDISASM_STUBS = [
    # B4 sub-stubs that need re-disasm after pool insertion
    (0x08075d5c, 0x08075dc3, 'magical_dim_sub_5d5c'),
    (0x08075dc4, 0x08075de7, 'magical_dim_sub_5dc4'),
    (0x08075de8, 0x08075e1f, 'magical_dim_sub_5de8'),
    (0x08075e20, 0x08075e5f, 'magical_dim_sub_5e20'),
    (0x08075e60, 0x08075e8b, 'magical_dim_sub_5e60'),
    (0x08075e8c, 0x08075ebf, 'magical_dim_sub_5e8c'),
    (0x08075ec0, 0x08075f01, 'magical_dim_sub_5ec0'),
    (0x08075f02, 0x08075f2b, 'magical_dim_sub_5f02'),
    (0x08075f2c, 0x08075f6f, 'magical_dim_sub_5f2c'),
    # B6 sub-stubs that need re-disasm after pool insertion
    (0x08075fe0, 0x08075ff3, 'friendship_sub_5fe0'),
    (0x08075ff4, 0x0807602f, 'friendship_sub_5ff4'),
    (0x08076030, 0x0807609d, 'friendship_sub_6030'),
    (0x0807609e, 0x080760ff, 'friendship_sub_609e'),
    (0x08076100, 0x08076145, 'friendship_sub_6100'),
    (0x08076146, 0x0807615b, 'friendship_default_6146'),
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

def _redisasm(lo_int, hi_int, label):
    # clearListing, setTMode, re-disasm
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] redisasm clearListing %s @ 0x%08x: %s" % (label, lo_int, e))
    _set_tmode(lo_int, hi_int)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] redisasm %s @ 0x%08x: %s" % (label, lo_int, cmd.getStatusMsg()))
    else:
        print("[ok ] redisasm %s @ 0x%08x..0x%08x" % (label, lo_int, hi_int))

def main():
    print("=== PoolFixF09Seg7 (DRY=%s) ===" % DRY)
    print("  Force-DWord: %d pool words" % len(POOL_DWORDS))
    print("  Re-disasm: %d sub-stubs" % len(REDISASM_STUBS))

    if DRY:
        for a in POOL_DWORDS:
            print("[dry] force_dword @ 0x%08x" % a)
        for lo, hi, label in REDISASM_STUBS:
            print("[dry] redisasm %s @ 0x%08x..0x%08x" % (label, lo, hi))
        return

    # Step 1: Force all pool DWords
    print("\n--- Step 1: Force pool DWords ---")
    for a in POOL_DWORDS:
        _force_dword(a)

    # Step 2: Re-disasm all sub-stubs (pool splits may have cleared code)
    print("\n--- Step 2: Re-disasm sub-stubs ---")
    for lo, hi, label in REDISASM_STUBS:
        _redisasm(lo, hi, label)

    print("\n=== PoolFixF09Seg7 DONE ===")
    print("  Forced %d DWords, re-disasmed %d stubs" % (len(POOL_DWORDS), len(REDISASM_STUBS)))


main()
