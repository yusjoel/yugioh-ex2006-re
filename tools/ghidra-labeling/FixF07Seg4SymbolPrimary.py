# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg4SymbolPrimary.py -- Fix primary symbol at offset addresses
#
# Problem: At 0x09e3f104, 'zone_monster_field_bonus_table' is primary (spurious).
# At 0x0201d5b4, 'gDuelFieldSlots' is primary (spurious, belongs at 0x0201c510).
# Fix: set the correct label as primary, remove spurious duplicates.

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def fix_primary(addr_int, correct_label, remove_spurious=None):
    """Set correct_label as primary at addr_int; optionally remove spurious label."""
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    syms = list(sym_tbl.getSymbols(a))
    names = [s.getName() for s in syms]
    print("  current: primary='%s' all=%s" % (
        sym_tbl.getPrimarySymbol(a).getName() if sym_tbl.getPrimarySymbol(a) else '(none)',
        names))
    if DRY:
        print("  [dry] would set primary='%s' at 0x%08x" % (correct_label, addr_int))
        if remove_spurious:
            print("  [dry] would remove '%s' at 0x%08x" % (remove_spurious, addr_int))
        return
    # Remove spurious label first
    if remove_spurious and remove_spurious in names:
        for s in syms:
            if s.getName() == remove_spurious:
                s.delete()
                print("  [ok ] deleted spurious label '%s' @ 0x%08x" % (remove_spurious, addr_int))
                break
        syms = list(sym_tbl.getSymbols(a))  # refresh
    # Set primary
    target_sym = None
    for s in syms:
        if s.getName() == correct_label:
            target_sym = s
            break
    if target_sym is None:
        print("  [FAIL] label '%s' not found at 0x%08x" % (correct_label, addr_int))
        return
    if target_sym.isPrimary():
        print("  [ok ] '%s' is already primary at 0x%08x" % (correct_label, addr_int))
    else:
        target_sym.setPrimary()
        print("  [ok ] set primary='%s' at 0x%08x" % (correct_label, addr_int))

def main():
    print("=== FixF07Seg4SymbolPrimary (DRY=%s) ===" % DRY)

    print("\n[1] 0x09e3f104: set 'zone_monster_field_bonus_dest_entry7' as primary")
    print("    (remove spurious 'zone_monster_field_bonus_table' at this offset addr)")
    fix_primary(0x09e3f104, 'zone_monster_field_bonus_dest_entry7',
                remove_spurious='zone_monster_field_bonus_table')

    print("\n[2] 0x0201d5b4: set 'gDuelFieldSlotsEffectZoneBase' as primary")
    print("    (remove spurious 'gDuelFieldSlots' at this offset addr)")
    fix_primary(0x0201d5b4, 'gDuelFieldSlotsEffectZoneBase',
                remove_spurious='gDuelFieldSlots')

    print("\n=== FixF07Seg4SymbolPrimary DONE ===")

main()
