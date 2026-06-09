# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF01Seg10StmiaPool.py -- Fix 32 stmia instructions in Seg-10 disasm block
#   These are Ghidra flow-disasm errors: 0xc03f bytes inside stubs were decoded
#   as THUMB stmia instructions instead of data (literal pool or alignment).
#   GAS cannot assemble "stmia r0,{r0-r5}" in THUMB mode without '!' writeback.
#
#   Fix: clearListing at each address + createHalfWord (0xc03f -> .hword 0xc03f)
#   This makes the ExportRangeToGas export ".hword 0xc03f" which GAS handles.

from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# 32 addresses where "stmia r0,{r0,r1,r2,r3,r4,r5}" appears in Seg-10 block
STMIA_ADDRS = [
    0x080292b0,
    0x08029300,
    0x08029340,
    0x08029394,
    0x080293cc,
    0x080294e8,
    0x08029578,
    0x080295c8,
    0x08029be0,
    0x08029d5c,
    0x08029e34,
    0x08029e60,
    0x08029fa8,
    0x08029fd4,
    0x0802a1c8,
    0x0802a3e0,
    0x0802a438,
    0x0802a4f0,
    0x0802a5b0,
    0x0802a63c,
    0x0802a780,
    0x0802a838,
    0x0802a898,
    0x0802a9f4,
    0x0802ac10,
    0x0802ac50,
    0x0802ae3c,
    0x0802b19c,
    0x0802b1d4,
    0x0802b21c,
    0x0802b398,
    0x0802b430,
]

EXPECTED_VALUE = 0xc03f  # little-endian bytes: 3f c0


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF01Seg10StmiaPool (DRY=%s) ===" % DRY)
    n_fixed = 0
    n_skip = 0

    for addr_int in STMIA_ADDRS:
        a = _addr(addr_int)
        if DRY:
            print("[dry] would fix 0x%08x: clearListing + createHalfWord" % addr_int)
            n_fixed += 1
            continue

        # Verify the bytes first (2 bytes at addr)
        mem = currentProgram.getMemory()
        try:
            b0 = mem.getByte(a) & 0xff
            b1 = mem.getByte(_addr(addr_int + 1)) & 0xff
            hword_val = b0 | (b1 << 8)
            if hword_val != EXPECTED_VALUE:
                print("[skip] 0x%08x: bytes=0x%04x != expected 0x%04x" % (addr_int, hword_val, EXPECTED_VALUE))
                n_skip += 1
                continue
        except Exception as e:
            print("[warn] read @ 0x%08x: %s" % (addr_int, e))

        try:
            clearListing(a, _addr(addr_int + 1))
            createWord(a)
            print("[ok] 0x%08x -> .hword 0xc03f" % addr_int)
            n_fixed += 1
        except Exception as e:
            print("[warn] fix @ 0x%08x: %s" % (addr_int, e))
            n_skip += 1

    print("[done] fixed=%d skip=%d (DRY=%s)" % (n_fixed, n_skip, DRY))


main()
