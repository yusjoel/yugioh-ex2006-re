# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg2DarkMagicianCid.py -- Rename DARK_MAGICIAN_CID equate to DARK_MAGICIAN_CID_0FC9
#
# The equate DARK_MAGICIAN_CID (0x0fc9) was created in Seg-2 but the canonical name
# in card_info.inc is DARK_MAGICIAN_CID_0FC9. This script renames the equate and
# relabels the 3 slot labels that referenced it.
#
# Affected slots: 0x08065d6c, 0x08065fb0, 0x08065ffc

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
    print("=== FixF08Seg2DarkMagicianCid (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()

    old_name = "DARK_MAGICIAN_CID"
    new_name = "DARK_MAGICIAN_CID_0FC9"
    value = 0x00000fc9

    eq = et.getEquate(old_name)
    if eq is None:
        print("[INFO] equate '%s' not found -- nothing to do" % old_name)
        # Check if new name already exists
        eq2 = et.getEquate(new_name)
        if eq2 is not None:
            print("[INFO] equate '%s' already exists with value 0x%x" % (new_name, eq2.getValue()))
        print("=== Done (no-op) ===")
        return

    print("[INFO] Found equate '%s' value=0x%x" % (old_name, eq.getValue() & 0xFFFFFFFF))

    if DRY:
        print("[dry] Would rename equate '%s' -> '%s'" % (old_name, new_name))
        # List references
        refs = list(eq.getReferences())
        print("[dry]   %d references" % len(refs))
        for r in refs:
            print("[dry]   ref at 0x%s" % r.getAddress())
        print("=== FixF08Seg2DarkMagicianCid DONE (dry) ===")
        return

    # Check if new equate already exists
    eq_new = et.getEquate(new_name)
    if eq_new is not None:
        print("[INFO] '%s' already exists -- removing old '%s' refs and adding to new" % (new_name, old_name))
        # Move references from old to new
        refs = list(eq.getReferences())
        for r in refs:
            eq.removeReference(r.getAddress(), r.getOpIndex())
            eq_new.addReference(r.getAddress(), r.getOpIndex())
            print("[MOVE] ref 0x%s -> '%s'" % (r.getAddress(), new_name))
        et.removeEquate(old_name)
        print("[DEL] removed equate '%s'" % old_name)
    else:
        # Rename by: create new, move refs, delete old
        refs = list(eq.getReferences())
        eq_new = et.createEquate(new_name, value)
        print("[CREATE] equate '%s' = 0x%x" % (new_name, value))
        for r in refs:
            eq_new.addReference(r.getAddress(), r.getOpIndex())
            eq.removeReference(r.getAddress(), r.getOpIndex())
            print("[MOVE] ref 0x%s -> '%s'" % (r.getAddress(), new_name))
        et.removeEquate(old_name)
        print("[DEL] removed equate '%s'" % old_name)

    print("=== FixF08Seg2DarkMagicianCid DONE ===")


main()
