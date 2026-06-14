# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg4PeriodicFnPtrs2.py -- Fix periodic fn-ptr / offset slots (corrected, F07 Seg-4)
#
# Problem analysis after first run + re-export mismatch:
#
# Group 1 (fn-ptr +1): DATA ref to EVEN addr causes Ghidra to export
#   ".word fn_label" = even addr. But ROM stores odd (fn+1) for THUMB dispatch.
#   Correct fix: REMOVE DATA ref to even addr -> Ghidra exports raw literal.
#   (amazoness slots 0x080389dc/0x80389f8 work this way: raw .word 0x0804b049)
#
# Group 2 (table offset): must also REMOVE old ref to base label before adding
#   offset-label ref. Old ref to base makes base label win in export.
#
# Group 3 (EWRAM offset): same - remove old ref to gDuelFieldSlots base,
#   add ref to gDuelFieldSlotsEffectZoneBase at exact offset addr.
#
# Slots (all verified against roms/2343.gba):

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

def _ensure_label(addr_int, label):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if label not in names:
        try:
            sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
            print("[ok ] createLabel '%s' @ 0x%08x" % (label, addr_int))
        except Exception as e:
            print("[warn] createLabel '%s' @ 0x%08x: %s" % (label, addr_int, e))
    else:
        print("[ok ] label '%s' already @ 0x%08x" % (label, addr_int))

def _remove_all_data_refs(slot_int):
    """Remove ALL DATA refs from slot (leave as raw literal)."""
    ref_mgr = currentProgram.getReferenceManager()
    a_slot = _addr(slot_int)
    removed = 0
    for ref in list(ref_mgr.getReferencesFrom(a_slot)):
        ref_mgr.delete(ref)
        print("[ok ] deleted ref 0x%08x -> 0x%08x" % (slot_int, ref.getToAddress().getOffset()))
        removed += 1
    if removed == 0:
        print("[ok ] no refs at 0x%08x (already clean)" % slot_int)
    return removed

def _fix_offset_ref(slot_int, old_base_int, target_int, target_label):
    """Remove ref to old_base, ensure label at target, add DATA ref to target."""
    ref_mgr = currentProgram.getReferenceManager()
    a_slot = _addr(slot_int)
    a_old = _addr(old_base_int)
    a_target = _addr(target_int)
    # Remove old ref(s) to base
    for ref in list(ref_mgr.getReferencesFrom(a_slot)):
        if ref.getToAddress().equals(a_old):
            ref_mgr.delete(ref)
            print("[ok ] deleted old ref 0x%08x -> 0x%08x" % (slot_int, old_base_int))
    # Ensure label at target
    _ensure_label(target_int, target_label)
    # Add/confirm ref to target
    found = False
    for ref in list(ref_mgr.getReferencesFrom(a_slot)):
        if ref.getToAddress().equals(a_target):
            ref_mgr.setPrimary(ref, True)
            found = True
            print("[ok ] existing ref 0x%08x -> 0x%08x set primary" % (slot_int, target_int))
    if not found:
        ref = ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
        ref_mgr.setPrimary(ref, True)
        print("[ok ] added DATA ref 0x%08x -> 0x%08x" % (slot_int, target_int))

def main():
    print("=== FixF07Seg4PeriodicFnPtrs2 (DRY=%s) ===" % DRY)
    n_ok = 0

    # Group 1: fn-ptr +1 slots -- REMOVE DATA refs, leave as raw literal
    # ROM stores odd addr (fn_even+1); removing ref causes Ghidra to export raw .word = odd
    FN_PTR_SLOTS = [
        0x08037884,   # check_level_conv_lab_node_match+1 = 0x0803777d
        0x0803aa74,   # check_level_conv_lab_node_match+1 = 0x0803777d
    ]
    print("\n--- Group 1: remove DATA refs from fn-ptr +1 slots (%d) ---" % len(FN_PTR_SLOTS))
    for slot_int in FN_PTR_SLOTS:
        print("\n[fn-ptr] 0x%08x: remove all refs" % slot_int)
        if DRY:
            print("  [dry] remove_all_data_refs 0x%08x" % slot_int)
            n_ok += 1
            continue
        _remove_all_data_refs(slot_int)
        n_ok += 1

    # Group 2: table offset -- 0x08040ab4 should store 0x09e3f104
    # Old ref was to zone_monster_field_bonus_table @ 0x09e3f094 (base)
    # Need ref to zone_monster_field_bonus_dest_entry7 @ 0x09e3f104 (base+0x70)
    TABLE_FIXES = [
        (0x08040ab4, 0x09e3f094, 0x09e3f104, 'zone_monster_field_bonus_dest_entry7'),
    ]
    print("\n--- Group 2: table offset fixes (%d) ---" % len(TABLE_FIXES))
    for slot_int, old_base_int, target_int, target_label in TABLE_FIXES:
        print("\n[table] 0x%08x: old_base=0x%08x -> target=0x%08x (%s)" % (slot_int, old_base_int, target_int, target_label))
        if DRY:
            print("  [dry] fix_offset_ref 0x%08x" % slot_int)
            n_ok += 1
            continue
        _fix_offset_ref(slot_int, old_base_int, target_int, target_label)
        n_ok += 1

    # Group 3: EWRAM offset -- 0x080478f0, 0x0805b888 should store 0x0201d5b4
    # Old ref was to gDuelFieldSlots @ 0x0201c510 (base)
    # Need ref to gDuelFieldSlotsEffectZoneBase @ 0x0201d5b4 (base+0x10a4)
    EWRAM_FIXES = [
        (0x080478f0, 0x0201c510, 0x0201d5b4, 'gDuelFieldSlotsEffectZoneBase'),
        (0x0805b888, 0x0201c510, 0x0201d5b4, 'gDuelFieldSlotsEffectZoneBase'),
    ]
    print("\n--- Group 3: EWRAM offset fixes (%d) ---" % len(EWRAM_FIXES))
    made_labels = set()
    for slot_int, old_base_int, target_int, target_label in EWRAM_FIXES:
        print("\n[ewram] 0x%08x: old_base=0x%08x -> target=0x%08x (%s)" % (slot_int, old_base_int, target_int, target_label))
        if DRY:
            print("  [dry] fix_offset_ref 0x%08x" % slot_int)
            n_ok += 1
            continue
        if target_label not in made_labels:
            _ensure_label(target_int, target_label)
            made_labels.add(target_label)
        _fix_offset_ref(slot_int, old_base_int, target_int, target_label)
        n_ok += 1

    total = len(FN_PTR_SLOTS) + len(TABLE_FIXES) + len(EWRAM_FIXES)
    print("\n=== FixF07Seg4PeriodicFnPtrs2 DONE: %d / %d fixed ===" % (n_ok, total))

main()
