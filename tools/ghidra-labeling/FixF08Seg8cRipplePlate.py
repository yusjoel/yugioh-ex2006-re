# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg8cRipplePlate.py -- ripple fix for FUNC_RENAME
#   dispatch_neo_daedalus_placement_check_by_state -> tick_spear_cretin_placement_state_machine
#
# Target: dispatch_spear_cretin_activate_if_chain_subtype @ 0x0806b53c
#   plate contains 3 occurrences of old name (in Returns/Side-effects/description lines)
#   All text must be pure ASCII.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_pre-F08Seg8c

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _apply_plate_fix(func_addr, old_text, new_text):
    for txt in [old_text, new_text]:
        if any(ord(ch) > 127 for ch in txt):
            print("[PLATE FAIL] non-ASCII in plate_fix @ 0x%08x -- SKIPPING" % func_addr)
            return False
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return False
    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
        return False
    count = existing.count(old_text)
    if count == 0:
        print("[WARN] plate_fix 0x%08x: '%s' not found (0 hits)" % (func_addr, old_text))
        return False
    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s' (%d hits)" % (
            func_addr, old_text, new_text, count))
        return True
    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s' (%d hits replaced)" % (
        func_addr, old_text, new_text, count))
    return True


def main():
    print("=== FixF08Seg8cRipplePlate (DRY=%s) ===" % DRY)
    print("  Ripple fix: dispatch_neo_daedalus_placement_check_by_state -> tick_spear_cretin_placement_state_machine")
    print("  Target: dispatch_spear_cretin_activate_if_chain_subtype @ 0x0806b53c")

    # Fix the plate of dispatch_spear_cretin_activate_if_chain_subtype (0x0806b53c)
    # This plate has 3 occurrences of the old name
    ok = _apply_plate_fix(
        0x0806b53c,
        'dispatch_neo_daedalus_placement_check_by_state',
        'tick_spear_cretin_placement_state_machine'
    )
    print("  Result: %s" % ("ok" if ok else "FAIL"))
    print("=== FixF08Seg8cRipplePlate DONE ===")


main()
