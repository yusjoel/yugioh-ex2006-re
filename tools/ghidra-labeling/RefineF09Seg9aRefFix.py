# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg9aRefFix.py -- Fix REF_SLOTS from RefineF09Seg9aSlots.py
#
# Problem: RefineF09Seg9aSlots.py set gas_label == slot_label for all 5 REF slots.
# When Ghidra exports, the .word at slot_addr resolves to the slot_label (same name),
# giving the slot its own address instead of the target address.
#
# Fix: Remove the erroneous slot labels (same name as target labels) and rename slots
# to unique names that DON'T collide with the gas_label at the target.
#
# REF corrections:
#   0x080775ac: remove 'spatial_collapse_dispatch_table_75ac' from SLOT,
#               keep it only at TARGET 0x08077648.
#               Add slot label 'spatial_collapse_dispatch_table_ptr_75ac' to slot.
#   0x080775d0: remove 'spatial_collapse_dispatch_sub_stubs_75d0' from SLOT,
#               keep it only at TARGET 0x080775d0 (self-target, no change needed).
#               Actually slot == target here, so this is a rename-only; no issue.
#   0x08077a18: remove 'jade_insect_dispatch_table_7a18' from SLOT,
#               keep it only at TARGET 0x08077b00.
#               Add slot label 'jade_insect_dispatch_table_ptr_7a18' to slot.
#   0x08077a3c: remove 'jade_insect_dispatch_sub_stubs_7a3c' from SLOT,
#               keep it only at TARGET 0x08077a3c (self-target, no issue).
#   0x08077b88: remove 'dimension_fusion_dispatch_sub_stubs_7b88' from SLOT,
#               keep it only at TARGET 0x08077b88 (self-target, no issue).
#
# Only the two table-pointer slots need fixing:
#   0x080775ac (slot != target 0x08077648)
#   0x08077a18 (slot != target 0x08077b00)
#
# For the 3 self-referencing slots, slot == target so the same label name at both
# is harmless (label resolves to correct address).

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

def _remove_label_at(addr_int, label_name):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    for sym in sym_tbl.getSymbols(a):
        if sym.getName() == label_name:
            if DRY:
                print("[dry] remove label '%s' @ 0x%08x" % (label_name, addr_int))
                return
            sym.delete()
            print("[ok ] removed label '%s' @ 0x%08x" % (label_name, addr_int))
            return
    print("[skip] label '%s' not found @ 0x%08x" % (label_name, addr_int))

def _add_label(addr_int, label_name):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
    if label_name in existing:
        print("[skip] label '%s' already @ 0x%08x" % (label_name, addr_int))
        return
    if DRY:
        print("[dry] add label '%s' @ 0x%08x" % (label_name, addr_int))
        return
    sym_tbl.createLabel(a, label_name, SourceType.USER_DEFINED)
    print("[ok ] added label '%s' @ 0x%08x" % (label_name, addr_int))

def _set_primary(addr_int, label_name):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    for sym in sym_tbl.getSymbols(a):
        if sym.getName() == label_name:
            if DRY:
                print("[dry] setPrimary '%s' @ 0x%08x" % (label_name, addr_int))
                return
            sym.setPrimary()
            print("[ok ] setPrimary '%s' @ 0x%08x" % (label_name, addr_int))
            return
    print("[warn] label '%s' not found for setPrimary @ 0x%08x" % (label_name, addr_int))

def main():
    print("=== RefineF09Seg9aRefFix (DRY=%s) ===" % DRY)
    print("Fix: remove slot=target label collision on PTR_DAT_080775ac and PTR_DAT_08077a18")

    # -----------------------------------------------------------------------
    # Fix 1: PTR_DAT_080775ac (0x080775ac)
    #   slot=0x080775ac, target=0x08077648
    #   erroneous: 'spatial_collapse_dispatch_table_75ac' label also at slot
    #   correct: remove from slot, add unique 'spatial_collapse_dispatch_table_ptr_75ac'
    # -----------------------------------------------------------------------
    print("\n--- Fix 1: PTR_DAT_080775ac @ 0x080775ac ---")
    # Remove the conflicting label from slot
    _remove_label_at(0x080775ac, 'spatial_collapse_dispatch_table_75ac')
    # Add unique label to slot
    _add_label(0x080775ac, 'spatial_collapse_dispatch_table_ptr_75ac')
    # Ensure gas_label at target is primary
    _set_primary(0x08077648, 'spatial_collapse_dispatch_table_75ac')

    # -----------------------------------------------------------------------
    # Fix 2: PTR_DAT_08077a18 (0x08077a18)
    #   slot=0x08077a18, target=0x08077b00
    #   erroneous: 'jade_insect_dispatch_table_7a18' label also at slot
    #   correct: remove from slot, add unique 'jade_insect_dispatch_table_ptr_7a18'
    # -----------------------------------------------------------------------
    print("\n--- Fix 2: PTR_DAT_08077a18 @ 0x08077a18 ---")
    _remove_label_at(0x08077a18, 'jade_insect_dispatch_table_7a18')
    _add_label(0x08077a18, 'jade_insect_dispatch_table_ptr_7a18')
    _set_primary(0x08077b00, 'jade_insect_dispatch_table_7a18')

    print("\n=== RefineF09Seg9aRefFix DONE ===")
    print("  Fix 1: spatial_collapse_dispatch_table_ptr_75ac @ slot 0x080775ac")
    print("         spatial_collapse_dispatch_table_75ac     @ target 0x08077648")
    print("  Fix 2: jade_insect_dispatch_table_ptr_7a18 @ slot 0x08077a18")
    print("         jade_insect_dispatch_table_7a18      @ target 0x08077b00")

main()
