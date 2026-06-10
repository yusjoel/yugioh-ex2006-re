# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF02Seg10aFnPtrSlot.py
# Fix the fn-ptr slot at 0x080346c0:
#   - Remove wrong label 'count_monster_slots_by_fnptr_pred_0804aea0' from 0x0804aea1
#   - Ensure slot 0x080346c0 has label 'check_field_spell_slot_placeable_fnptr'
#   - Ensure DATA ref from 0x080346c0 -> 0x0804aea0 (even addr, not odd)
# The GAS exporter will output: .word check_card_is_archfiend_type+1
# because check_card_is_archfiend_type is already at 0x0804aea0.

from ghidra.program.model.symbol import SourceType, RefType

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
    print("=== FixF02Seg10aFnPtrSlot (DRY=%s) ===" % DRY)

    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    wrong_label = 'count_monster_slots_by_fnptr_pred_0804aea0'
    odd_addr = _addr(0x0804aea1)
    even_addr = _addr(0x0804aea0)
    slot_addr = _addr(0x080346c0)
    slot_label = 'check_field_spell_slot_placeable_fnptr'

    # 1. Remove wrong label from 0x0804aea1
    for sym in sym_tbl.getSymbols(odd_addr):
        if sym.getName() == wrong_label:
            if DRY:
                print("[dry] DELETE label '%s' from 0x0804aea1" % wrong_label)
            else:
                sym.delete()
                print("[FIX] Deleted label '%s' from 0x0804aea1" % wrong_label)
            break
    else:
        print("[INFO] Label '%s' not found at 0x0804aea1 (already clean)" % wrong_label)

    # 2. Remove DATA ref from slot -> 0x0804aea1 (wrong odd target)
    for ref in list(ref_mgr.getReferencesFrom(slot_addr)):
        if ref.getToAddress().equals(odd_addr):
            if DRY:
                print("[dry] DELETE ref 0x080346c0 -> 0x0804aea1")
            else:
                ref_mgr.delete(ref)
                print("[FIX] Deleted ref 0x080346c0 -> 0x0804aea1")

    # 3. Add DATA ref from slot -> 0x0804aea0 (even addr = function entry)
    if DRY:
        print("[dry] ADD ref 0x080346c0 -> 0x0804aea0 (check_card_is_archfiend_type)")
    else:
        ref_mgr.addMemoryReference(slot_addr, even_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        for ref in ref_mgr.getReferencesFrom(slot_addr):
            if ref.getToAddress().equals(even_addr):
                ref_mgr.setPrimary(ref, True)
        print("[FIX] Added DATA ref 0x080346c0 -> 0x0804aea0")

    # 4. Ensure slot label 'check_field_spell_slot_placeable_fnptr' at 0x080346c0
    names = [s.getName() for s in sym_tbl.getSymbols(slot_addr)]
    if slot_label not in names:
        if DRY:
            print("[dry] CREATE label '%s' at 0x080346c0" % slot_label)
        else:
            sym_tbl.createLabel(slot_addr, slot_label, SourceType.USER_DEFINED)
            print("[FIX] Created label '%s' at 0x080346c0" % slot_label)
    else:
        print("[INFO] Label '%s' already at 0x080346c0" % slot_label)

    print("=== FixF02Seg10aFnPtrSlot DONE ===")

main()
