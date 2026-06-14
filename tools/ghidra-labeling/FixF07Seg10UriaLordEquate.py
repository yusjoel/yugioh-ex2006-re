# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg10UriaLordEquate.py
# Rename Ghidra equate SPECIAL_EQUIP_SENTINEL_ID -> URIA_LORD_CID (value 0x19a3)
# and update equate reference at 0x0805af50 (asm/06 slot uria_lord_cid_18105).
# Also add equate reference for the new Seg-10 slot at 0x08064250.
#
# NOTE: Renaming equates in Ghidra API: no direct setName on Equate.
# Workaround: remove old equate + recreate with new name.

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
    print("=== FixF07Seg10UriaLordEquate (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()

    old_name = 'SPECIAL_EQUIP_SENTINEL_ID'
    new_name = 'URIA_LORD_CID'
    value = 0x000019a3

    # Slots that reference this equate
    slot_addrs = [
        0x0805af50,  # asm/06 slot (uria_lord_cid_18105)
        0x08064250,  # asm/07 Seg-10 slot (uria_lord_cid_08064250)
    ]

    old_eq = et.getEquate(old_name)
    if old_eq is None:
        print("[INFO] Equate '%s' not found -- checking for new name" % old_name)
        new_eq = et.getEquate(new_name)
        if new_eq is not None:
            print("[INFO] '%s' already exists; adding refs for Seg-10 slot" % new_name)
            if not DRY:
                a = _addr(0x08064250)
                new_eq.addReference(a, 0)
                print("[EQ+REF] 0x08064250 -> %s" % new_name)
            else:
                print("[dry] Would add ref 0x08064250 -> %s" % new_name)
        else:
            print("[INFO] Neither equate found. Creating '%s' fresh" % new_name)
            if not DRY:
                new_eq = et.createEquate(new_name, value)
                for addr in slot_addrs:
                    a = _addr(addr)
                    new_eq.addReference(a, 0)
                    print("[EQ+REF] 0x%08x -> %s" % (addr, new_name))
        return

    # Old equate exists -- recreate with new name
    print("[INFO] Found equate '%s' = 0x%x; renaming to '%s'" % (old_name, old_eq.getValue(), new_name))

    if DRY:
        print("[dry] Would: remove '%s', create '%s'=0x%x, re-add %d refs" % (
            old_name, new_name, value, len(slot_addrs)))
        return

    # Collect existing references before removal
    existing_refs = list(old_eq.getReferences())
    print("[INFO] Existing refs: %d" % len(existing_refs))

    # Remove old equate
    try:
        old_eq.deleteEquate()
        print("[OK] Deleted equate '%s'" % old_name)
    except Exception as e:
        print("[WARN] deleteEquate failed: %s; trying removeEquate" % e)
        try:
            et.removeEquate(old_name)
        except Exception as e2:
            print("[ERR] removeEquate also failed: %s" % e2)

    # Create new equate
    new_eq = et.getEquate(new_name)
    if new_eq is None:
        new_eq = et.createEquate(new_name, value)
        print("[OK] Created equate '%s' = 0x%x" % (new_name, value))
    else:
        print("[INFO] Equate '%s' already exists" % new_name)

    # Re-add old refs
    for ref in existing_refs:
        addr = ref.getAddress()
        new_eq.addReference(addr, 0)
        print("[REF] re-added 0x%08x" % addr.getOffset())

    # Add Seg-10 new slot ref
    a10 = _addr(0x08064250)
    new_eq.addReference(a10, 0)
    print("[REF] new Seg-10 slot 0x08064250")

    print("=== FixF07Seg10UriaLordEquate DONE ===")


main()
