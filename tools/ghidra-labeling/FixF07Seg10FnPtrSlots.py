# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg10FnPtrSlots.py
# Fix the 4 fn-ptr slots in Seg-10 that have equate references pointing to
# function symbols (which GAS assembles without +1 thumb bit).
# These slots must emit raw literal .word values (fn_addr+1) not symbol refs.
#
# The equate was created with the raw +1 value (e.g. 0x08050ead), but since
# the equate name matches a function name, GAS resolves it as a label (addr only).
# Fix: remove equate reference from these slots so the exporter outputs raw .word values.
#
# Slots to fix:
#   0x08063890: fn-ptr set_equip_activation_state_by_mode+1 = 0x08050ead
#   0x0806390c: fn-ptr check_equip_slot_eligible_by_same_side_and_prereqs+1 = 0x08054899
#   0x08063c60: fn-ptr check_equip_slot_eligible_by_card_id_bst+1 = 0x08050a55
#   0x080641f0: fn-ptr check_card_id_is_special_summon_type+1 = 0x0804b30d

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


FN_PTR_SLOTS = [
    (0x08063890, 0x08050ead, 'set_equip_activation_state_by_mode',
     'zone_pair_pred_0ead_ptr_08063890',
     'fn-ptr set_equip_activation_state_by_mode+1 @0x08050eac'),
    (0x0806390c, 0x08054899, 'check_equip_slot_eligible_by_same_side_and_prereqs',
     'zone_pair_pred_4899_ptr_0806390c',
     'fn-ptr check_equip_slot_eligible_by_same_side_and_prereqs+1 @0x08054898'),
    (0x08063c60, 0x08050a55, 'check_equip_slot_eligible_by_card_id_bst',
     'zone_pair_pred_0a55_ptr_08063c60',
     'fn-ptr check_equip_slot_eligible_by_card_id_bst+1 @0x08050a54'),
    (0x080641f0, 0x0804b30d, 'check_card_id_is_special_summon_type',
     'monster_slot_fnptr_080641f0',
     'fn-ptr check_card_id_is_special_summon_type+1 @0x0804b30c'),
]


def main():
    print("=== FixF07Seg10FnPtrSlots (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    sym_tbl = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()
    from ghidra.program.model.listing import CodeUnit

    for slot_addr, raw_val, eq_name, slot_label, eol in FN_PTR_SLOTS:
        a = _addr(slot_addr)
        print("\n[SLOT] 0x%08x (%s)" % (slot_addr, slot_label))

        # Verify ROM value
        mem = currentProgram.getMemory()
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
        except Exception as e:
            print("  [ERR] read error: %s" % e)
            continue
        if actual != (raw_val & 0xFFFFFFFF):
            print("  [FAIL] ROM=0x%08x expected=0x%08x -- skip" % (actual, raw_val))
            continue
        print("  [OK] ROM value verified: 0x%08x" % actual)

        # Remove equate reference (so exporter outputs raw .word value)
        eq = et.getEquate(eq_name)
        if eq is not None:
            refs = list(eq.getReferences())
            for ref in refs:
                if ref.getAddress().getOffset() == slot_addr:
                    if DRY:
                        print("  [dry] Would remove equate ref '%s' at 0x%08x" % (eq_name, slot_addr))
                    else:
                        eq.removeReference(a, 0)
                        print("  [OK] Removed equate ref '%s' at 0x%08x" % (eq_name, slot_addr))
        else:
            print("  [INFO] Equate '%s' not found (already removed or never created)" % eq_name)

        # Ensure slot label exists
        names = [s.getName() for s in sym_tbl.getSymbols(a)]
        if slot_label not in names:
            if DRY:
                print("  [dry] Would create label %s" % slot_label)
            else:
                sym_tbl.createLabel(a, slot_label, __import__('ghidra.program.model.symbol', fromlist=['SourceType']).SourceType.USER_DEFINED)
                print("  [OK] Created label %s" % slot_label)
        else:
            print("  [OK] Label %s already exists" % slot_label)

        # Ensure EOL comment
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            if DRY:
                print("  [dry] Would set EOL: %s" % eol)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
                print("  [OK] Set EOL: %s" % eol)

    print("\n=== FixF07Seg10FnPtrSlots DONE ===")


main()
