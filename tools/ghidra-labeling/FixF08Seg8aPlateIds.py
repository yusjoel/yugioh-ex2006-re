# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg8aPlateIds.py -- fix remaining CARD_ID_ prefix in plate at 0x0806b31c
# After RefineF08Seg8aSlots ran, 2 plate rewrites were skipped because
# "Neo-Daedalus group A/B" was already replaced. Fix the remaining CARD_ID_ prefix.

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

FIXES = [
    # After prior rewrites, the line reads: CARD_ID_0x1339=0x1339 (Giant Germ (CID=0x1339))
    # We want: GIANT_GERM_CID=0x1339 (Giant Germ)
    (0x0806b31c, 'CARD_ID_0x1339=0x1339 (Giant Germ (CID=0x1339))', 'GIANT_GERM_CID=0x1339 (Giant Germ)'),
    (0x0806b31c, 'CARD_ID_0x133a=0x133a (Nimble Momonga (CID=0x133a))', 'NIMBLE_MOMONGA_CID=0x133a (Nimble Momonga)'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== FixF08Seg8aPlateIds (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    ok = 0; fail = 0
    for func_addr, old_text, new_text in FIXES:
        a = _addr(func_addr)
        cu = listing.getCodeUnitAt(a)
        if cu is None:
            print("[FAIL] no code unit @ 0x%08x" % func_addr); fail += 1; continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[FAIL] no plate @ 0x%08x" % func_addr); fail += 1; continue
        if old_text not in plate:
            print("[WARN] '%s' not found in plate @ 0x%08x" % (old_text[:40], func_addr))
            print("  current plate snippet: %s" % plate[plate.find('CARD_ID'):plate.find('CARD_ID')+80] if 'CARD_ID' in plate else "  no CARD_ID found")
            fail += 1; continue
        if DRY:
            print("[dry] FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text[:40], new_text)); ok += 1; continue
        new_plate = plate.replace(old_text, new_text)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[ok] FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text[:40], new_text)); ok += 1
    print("=== done: ok=%d fail=%d ===" % (ok, fail))

main()
