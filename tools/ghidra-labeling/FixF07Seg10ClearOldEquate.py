# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg10ClearOldEquate.py
# Remove the stale SPECIAL_EQUIP_SENTINEL_ID equate ref at 0x0805af50
# and ensure URIA_LORD_CID is properly referenced there.
#
# The exporter uses equate names for .word values; we need to ensure
# the equate at 0x0805af50 resolves to URIA_LORD_CID not SPECIAL_EQUIP_SENTINEL_ID.

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
    print("=== FixF07Seg10ClearOldEquate (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()

    # Slot address
    slot_addr = 0x0805af50
    a = _addr(slot_addr)

    # Check current equate refs at this address
    refs_at_slot = list(et.getEquates(a))
    print("[INFO] Equates at 0x%08x: %d" % (slot_addr, len(refs_at_slot)))
    for eq in refs_at_slot:
        print("  equate: '%s' = 0x%x" % (eq.getName(), eq.getValue()))

    old_name = 'SPECIAL_EQUIP_SENTINEL_ID'
    new_name = 'URIA_LORD_CID'

    old_eq = et.getEquate(old_name)
    new_eq = et.getEquate(new_name)

    if old_eq is not None:
        print("[INFO] Old equate '%s' refs: %d" % (old_name, len(list(old_eq.getReferences()))))
        if DRY:
            print("[dry] Would remove ref from '%s' at 0x%08x" % (old_name, slot_addr))
        else:
            old_eq.removeReference(a, 0)
            print("[OK] Removed ref from '%s' at 0x%08x" % (old_name, slot_addr))

    if new_eq is None:
        print("[ERR] '%s' equate not found" % new_name)
        return

    # Ensure ref at slot_addr exists for new equate
    existing_refs = [r.getAddress().getOffset() for r in new_eq.getReferences()]
    if slot_addr not in existing_refs:
        if DRY:
            print("[dry] Would add ref '%s' at 0x%08x" % (new_name, slot_addr))
        else:
            new_eq.addReference(a, 0)
            print("[OK] Added ref '%s' at 0x%08x" % (new_name, slot_addr))
    else:
        print("[OK] Ref '%s' at 0x%08x already exists" % (new_name, slot_addr))

    # Check final state
    refs_at_slot2 = list(et.getEquates(a))
    print("[FINAL] Equates at 0x%08x after fix: %d" % (slot_addr, len(refs_at_slot2)))
    for eq in refs_at_slot2:
        print("  equate: '%s' = 0x%x" % (eq.getName(), eq.getValue()))

    print("=== FixF07Seg10ClearOldEquate DONE ===")


main()
