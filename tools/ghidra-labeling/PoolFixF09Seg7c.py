# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg7c.py -- third-pass pool fix for B4 remaining pool DWords
#   Fixes residual .byte/.incbin pool areas not caught by previous passes.
#
# Remaining errors after PoolFixF09Seg7b:
#   DAT_08075de4: 1 DWord at 0x08075de4 (THUMB+1 callee ptr 0x08053e15)
#                 2B pad at 0x08075de2
#   DAT_08075f24/f28: pool cluster (2 DWords)
#                     2B pad at 0x08075f22, DWords at 0x08075f24/0x08075f28
#   DAT_08075f54/f58/f5c/f60: within ROM_INCBIN 0x75f52, 0x16
#                              2B pad at 0x08075f52, 4 DWords at 0x75f54/58/5c/60

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

POOL_DWORDS = [
    # Pool within magical_dim_sub_5dc4 tail (THUMB+1 callee ptr 0x08053e15)
    # 2B pad at 0x08075de2, DWord at 0x08075de4
    0x08075de4,
    # Pool within magical_dim_sub_5f02 tail
    # 2B pad at 0x08075f22, DWords at 0x08075f24/f28
    0x08075f24,
    0x08075f28,
    # Pool within magical_dim_sub_5f2c tail (ROM_INCBIN 0x75f52, 0x16)
    # 2B pad at 0x08075f52, DWords at 0x08075f54/58/5c/60
    0x08075f54,
    0x08075f58,
    0x08075f5c,
    0x08075f60,
]

# Re-disasm the stubs that contain these pools
# (need to clear and re-disasm the code portions, avoid the pool areas)
REDISASM_STUBS = [
    # magical_dim_sub_5dc4: code at 0x75dc4..0x75de1 (pool at 0x75de2..0x75de7)
    (0x08075dc4, 0x08075de1, 'magical_dim_sub_5dc4_code'),
    # magical_dim_sub_5f02: code at 0x75f02..0x75f21 (pool at 0x75f22..0x75f2b)
    (0x08075f02, 0x08075f21, 'magical_dim_sub_5f02_code'),
    # magical_dim_sub_5f2c: code at 0x75f2c..0x75f51 (pool at 0x75f52..0x75f67 = ROM_INCBIN)
    (0x08075f2c, 0x08075f51, 'magical_dim_sub_5f2c_code'),
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
    print("=== PoolFixF09Seg7c (DRY=%s) ===" % DRY)
    print("  Force-DWord: %d; Re-disasm: %d stubs" % (len(POOL_DWORDS), len(REDISASM_STUBS)))

    if DRY:
        for a in POOL_DWORDS:
            print("[dry] force_dword @ 0x%08x" % a)
        for lo, hi, label in REDISASM_STUBS:
            print("[dry] redisasm %s @ 0x%08x..0x%08x" % (label, lo, hi))
        return

    # Step 1: Force pool DWords (some may overwrite disasmed instructions)
    print("\n--- Step 1: Force pool DWords ---")
    for a in POOL_DWORDS:
        _force_dword(a)

    # Step 2: Re-disasm code portions ONLY (not the pool areas)
    print("\n--- Step 2: Re-disasm code portions ---")
    for lo, hi, label in REDISASM_STUBS:
        _redisasm(lo, hi, label)

    # Step 3: Re-force pool DWords (in case Step 2 clearListing hit them)
    print("\n--- Step 3: Re-force pool DWords (idempotent) ---")
    for a in POOL_DWORDS:
        _force_dword(a)

    print("\n=== PoolFixF09Seg7c DONE ===")


main()
