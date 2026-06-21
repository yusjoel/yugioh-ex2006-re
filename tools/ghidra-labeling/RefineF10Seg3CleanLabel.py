# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg3CleanLabel.py -- remove stale secondary label at 0x0807c388
# The function tick_equip_activation_display_state is already named correctly,
# but the old label tick_equip_activation_display_state__0807c388 persists as
# a secondary symbol and gets exported by the GAS exporter.
# This script removes the stale secondary label.

from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== RefineF10Seg3CleanLabel (DRY=%s) ===" % DRY)
    sm = currentProgram.getSymbolTable()
    fn_addr = _addr(0x0807c388)
    old_label = "tick_equip_activation_display_state__0807c388"
    new_fn_name = "tick_equip_activation_display_state"

    # List all symbols at this address
    syms = list(sm.getSymbols(fn_addr))
    print("Symbols at 0x0807c388:")
    for sym in syms:
        print("  [%s] '%s' primary=%s type=%s" % (sym.getSource(), sym.getName(), sym.isPrimary(), sym.getSymbolType()))

    # Find and delete the old stale label
    removed = 0
    for sym in syms:
        if sym.getName() == old_label:
            print("Found stale label '%s' -- removing" % old_label)
            if not DRY:
                sym.delete()
                print("Deleted stale label '%s'" % old_label)
            else:
                print("[DRY] Would delete stale label '%s'" % old_label)
            removed += 1

    if removed == 0:
        print("Stale label '%s' not found (already removed or never existed)" % old_label)

    # Confirm function name
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(fn_addr)
    if fn is not None:
        print("Function at 0x0807c388: '%s'" % fn.getName())
        if fn.getName() != new_fn_name:
            print("Setting function name to '%s'" % new_fn_name)
            if not DRY:
                fn.setName(new_fn_name, SourceType.USER_DEFINED)
    print("=== DONE ===")

main()
