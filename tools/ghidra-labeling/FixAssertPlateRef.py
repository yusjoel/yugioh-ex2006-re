# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixAssertPlateRef.py — 订正 plate 散文里 rename 前的旧断言名 (nns_g2d_assert_anmID)。
# Usage: tools\asm-regen\ghidra-run-script.bat FixAssertPlateRef.py [dry]
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# addr -> [(old, new), ...]
REPL = {
    0x08018260: [(u"nns_g2d_assert_anmID", u"assert_anmid_ig2d_getanmsequencescoun")],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixAssertPlateRef (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    for addr_int in sorted(REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[FAIL] no plate @ 0x%08x" % addr_int)
            continue
        new = txt
        for old, rep in REPL[addr_int]:
            if old not in new:
                print("[FAIL] 0x%08x pattern not found: %s" % (addr_int, old))
                continue
            new = new.replace(old, rep)
        if new != txt and not DRY:
            cu.setComment(CodeUnit.PLATE_COMMENT, new)
            print("[ok] 0x%08x plate updated" % addr_int)
        elif DRY:
            print("[dry] 0x%08x would update" % addr_int)
    print("[done]")


main()
