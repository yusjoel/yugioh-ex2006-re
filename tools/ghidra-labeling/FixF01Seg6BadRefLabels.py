# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF01Seg6BadRefLabels.py -- remove bad REF labels created at slot addresses
#   After RefineF01Seg6Slots.py's REF approach created labels at target addresses
#   but the exporter misidentified them at the slot addresses, we need to:
#   1) Remove the incorrectly named label at each slot address
#   2) Ensure the correct RENAME label is primary
#
#   Bad labels to remove:
#   - 0x0801f428: 'find_card_index_in_rom_table_count_ptr' (should be slot label only)
#   - 0x0801f42c: 'find_card_index_in_rom_table_data_ptr' (should be slot label only)
#
#   Also: Remove any DATA ref from these slots to far ROM addresses
#   (which caused the exporter to emit wrong .word expressions)

from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# Slots that got bad labels + bad DATA refs
BAD_SLOTS = [
    (0x0801f428, ['find_card_index_in_rom_table_count_ptr', 'find_card_index_count_slot'],
     0x098973f6, 'find_card_index_in_rom_table_count_slot'),
    (0x0801f42c, ['find_card_index_in_rom_table_data_ptr', 'find_card_index_data_slot'],
     0x098972f0, 'find_card_index_in_rom_table_data_slot'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF01Seg6BadRefLabels (DRY=%s) ===" % DRY)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    for slot_addr, bad_label_names, target_addr, correct_label in BAD_SLOTS:
        sa = _addr(slot_addr)
        ta = _addr(target_addr)
        print("\n--- Slot 0x%08x ---" % slot_addr)

        # 1) Remove bad labels at slot address
        syms = list(sym_tbl.getSymbols(sa))
        for sym in syms:
            name = sym.getName()
            if name in bad_label_names:
                if DRY:
                    print("[dry] would delete label '%s' at 0x%08x" % (name, slot_addr))
                else:
                    try:
                        sym.delete()
                        print("[DEL] deleted label '%s' at 0x%08x" % (name, slot_addr))
                    except Exception as e:
                        print("[WARN] cannot delete '%s' at 0x%08x: %s" % (name, slot_addr, e))

        # 2) Remove any DATA refs from slot to target (wrong refs from REF attempt)
        for ref in list(ref_mgr.getReferencesFrom(sa)):
            if ref.getToAddress().equals(ta) and ref.getReferenceType() == RefType.DATA:
                if DRY:
                    print("[dry] would remove DATA ref 0x%08x -> 0x%08x" % (slot_addr, target_addr))
                else:
                    try:
                        ref_mgr.delete(ref)
                        print("[DEL] removed DATA ref 0x%08x -> 0x%08x" % (slot_addr, target_addr))
                    except Exception as e:
                        print("[WARN] cannot remove ref: %s" % e)

        # 3) Also remove the bad label at the TARGET address (0x098973f6/0x098972f0)
        # These far ROM labels cause the exporter to emit wrong .word expressions
        target_label_names = [n for n in bad_label_names if 'count_ptr' in n or 'data_ptr' in n]
        t_syms = list(sym_tbl.getSymbols(ta))
        for sym in t_syms:
            name = sym.getName()
            if name in target_label_names:
                if DRY:
                    print("[dry] would delete label '%s' at target 0x%08x" % (name, target_addr))
                else:
                    try:
                        sym.delete()
                        print("[DEL] deleted target label '%s' at 0x%08x" % (name, target_addr))
                    except Exception as e:
                        print("[WARN] cannot delete target label '%s': %s" % (name, e))

        # 4) Ensure correct slot label is primary
        syms_after = list(sym_tbl.getSymbols(sa))
        names_after = [s.getName() for s in syms_after]
        print("[OK] remaining labels at 0x%08x: %s" % (slot_addr, names_after))
        if correct_label in names_after:
            print("[OK] correct label '%s' present" % correct_label)
        else:
            if DRY:
                print("[dry] would create label '%s' at 0x%08x" % (correct_label, slot_addr))
            else:
                sym_tbl.createLabel(sa, correct_label, SourceType.USER_DEFINED)
                print("[ADD] created label '%s' at 0x%08x" % (correct_label, slot_addr))

    print("\n=== FixF01Seg6BadRefLabels DONE ===")


main()
