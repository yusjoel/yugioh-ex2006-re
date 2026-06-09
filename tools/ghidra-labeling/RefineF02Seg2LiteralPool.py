# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg2LiteralPool.py -- f02 Seg-2 literal pool DWord fix
#   Creates DWord data items at literal pool addresses referenced by ldr instructions
#   inside Block1 (0x0802e22c..0x0802e3c7) that Ghidra exported as undefined bytes.
#
#   Addresses found by inspecting asm/02_text_lp_fieldspell.s ldr DAT_ refs in Block1:
#     DAT_0802e238 @ 0x0802e238  (ldr r1 @ 0x0802e22c)
#     DAT_0802e278 @ 0x0802e278  (ldr r3 @ 0x0802e244)
#     DAT_0802e27c @ 0x0802e27c  (ldr r0 @ 0x0802e26c)
#     DAT_0802e2bc @ 0x0802e2bc  (ldr r1 @ 0x0802e280)
#     DAT_0802e2c0 @ 0x0802e2c0  (ldr r2 @ 0x0802e29a)
#     DAT_0802e308 @ 0x0802e308  (ldr r1 @ 0x0802e2d2)
#     DAT_0802e3c4 @ 0x0802e3c4  (ldr r0 @ 0x0802e382)
#   Block2 pools (0x0802e554..) exported correctly as labeled DWords.
#
# After running this script, re-export + rebuild.

import ghidra.program.model.data as DataTypes

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


# Literal pool addresses in Block1/Block2 that need DWord data type
LITERAL_POOL_ADDRS = [
    # Block1 (0x0802e22c..0x0802e3c7)
    0x0802e238,
    0x0802e278,
    0x0802e27c,
    0x0802e2bc,
    0x0802e2c0,
    0x0802e308,
    0x0802e3c4,
    # Block2 (0x0802e554..0x0802e697) -- 0x0802e650 missing
    0x0802e650,
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _create_dword(addr):
    """Create a DWORD data item at addr for literal pool PC-relative ldr targets."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    dt = DataTypes.DWordDataType.dataType

    if DRY:
        print("[dry] createDWord @ 0x%08x" % addr)
        return True

    existing = listing.getDataAt(a)
    if existing is not None and existing.getDataType().equals(dt):
        print("[ok ] DWord already exists @ 0x%08x" % addr)
        return True

    # Clear existing data/code at this address first
    try:
        clearListing(a, a.add(3))
    except Exception as e:
        print("[warn] clear @ 0x%08x: %s" % (addr, e))

    try:
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr)
        return True
    except Exception as e:
        print("[FAIL] createDWord 0x%08x: %s" % (addr, e))
        return False


def main():
    print("=== RefineF02Seg2LiteralPool (DRY=%s) ===" % DRY)
    print("  Creating DWord items at %d Block1 literal pool addresses" % len(LITERAL_POOL_ADDRS))

    ok = 0
    for addr in LITERAL_POOL_ADDRS:
        if _create_dword(addr):
            ok += 1

    print("\n=== RefineF02Seg2LiteralPool DONE: %d/%d DWords created ===" % (
        ok, len(LITERAL_POOL_ADDRS)))


main()
