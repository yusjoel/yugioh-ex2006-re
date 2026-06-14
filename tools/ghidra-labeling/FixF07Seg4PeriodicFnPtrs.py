# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg4PeriodicFnPtrs.py -- Fix periodic fn-ptr / offset slots after F07 Seg-4 re-export
#
# Problem: After Ghidra re-export, fn-ptr slots that store THUMB fn addr+1 (odd) get
# exported as .word <fn_label> (missing +1), and table-offset/EWRAM slots with wrong base.
# Fix: Ensure DATA ref points to the correct even-addr or offset target.
#
# Slots verified via: python -c "with open('roms/2343.gba','rb') as f: f.seek(offset); ..."
#
# Group 1: fn-ptr +1 fixes (slot stores odd addr = fn_even+1)
#   0x08037884: ROM=0x0803777d -> check_level_conv_lab_node_match(0x0803777c)+1
#   0x0803aa74: ROM=0x0803777d -> same
#   0x080389dc: ROM=0x0804b049 -> check_card_is_amazoness_type(0x0804b048)+1
#   0x080389f8: ROM=0x0804b049 -> same
#   0x08045efc: ROM=0x08045531 -> apply_nitro_unit_equip_activation(0x08045530)+1
#   0x0805df94: ROM=0x08051319 -> check_equip_slot_eligible_by_equip_type(0x08051318)+1
#
# Group 2: table label offset fix (slot stores base+offset, need label at exact addr)
#   0x08040ab4: ROM=0x09e3f104 = zone_monster_field_bonus_table(0x09e3f094)+0x70
#               -> create label 'zone_monster_field_bonus_dest_entry7' at 0x09e3f104
#               -> DATA ref 0x08040ab4 -> 0x09e3f104
#
# Group 3: EWRAM offset fix (slot stores gDuelFieldSlots+0x10a4=0x0201d5b4)
#   0x080478f0: ROM=0x0201d5b4 = gDuelFieldSlots(0x0201c510)+EFFECT_ZONE_PARTITION_OFF(0x10a4)
#   0x0805b888: ROM=0x0201d5b4 -> same
#               -> create label 'gDuelFieldSlotsEffectZoneBase' at 0x0201d5b4 (EWRAM)
#               -> DATA ref slot -> 0x0201d5b4
#
# Note: asm/07 seg-4 slot 0x0805f28c stores 0x0804b049 (raw literal .word) which already
# assembles correctly, so no fix needed for that slot.
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-141354-pre-f07seg4

from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# Group 1: fn-ptr +1 fixes
# (slot_addr, fn_even_addr, fn_label)
FN_PTR_FIXES = [
    # asm/03: check_level_conv_lab_node_match (even=0x0803777c, stores 0x0803777d)
    (0x08037884, 0x0803777c, 'check_level_conv_lab_node_match'),
    (0x0803aa74, 0x0803777c, 'check_level_conv_lab_node_match'),

    # asm/03: check_card_is_amazoness_type (even=0x0804b048, stores 0x0804b049)
    (0x080389dc, 0x0804b048, 'check_card_is_amazoness_type'),
    (0x080389f8, 0x0804b048, 'check_card_is_amazoness_type'),

    # asm/04: apply_nitro_unit_equip_activation (even=0x08045530, stores 0x08045531)
    (0x08045efc, 0x08045530, 'apply_nitro_unit_equip_activation'),

    # asm/07 seg-2: check_equip_slot_eligible_by_equip_type (even=0x08051318, stores 0x08051319)
    (0x0805df94, 0x08051318, 'check_equip_slot_eligible_by_equip_type'),
]

# Group 2: table label offset -- create label at exact ROM table offset address
# (slot_addr, target_addr, target_label)
TABLE_LABEL_FIXES = [
    # asm/04: zone_monster_field_bonus_table entry7 (0x09e3f094 + 7*16 = 0x09e3f104)
    (0x08040ab4, 0x09e3f104, 'zone_monster_field_bonus_dest_entry7'),
]

# Group 3: EWRAM offset fixes
# (slot_addr, ewram_addr, ewram_label)
EWRAM_FIXES = [
    # asm/04 + asm/06: gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF (0x0201c510+0x10a4=0x0201d5b4)
    (0x080478f0, 0x0201d5b4, 'gDuelFieldSlotsEffectZoneBase'),
    (0x0805b888, 0x0201d5b4, 'gDuelFieldSlotsEffectZoneBase'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _ensure_label(addr_int, label):
    """Ensure label exists at addr_int (create if missing)."""
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


def _fix_data_ref(slot_int, target_int):
    """Remove any non-target DATA refs from slot; add/confirm DATA ref slot->target."""
    ref_mgr = currentProgram.getReferenceManager()
    a_slot   = _addr(slot_int)
    a_target = _addr(target_int)
    a_odd    = _addr(target_int + 1)

    # Remove ref to odd addr (fn-ptr case only, harmless for others)
    for ref in list(ref_mgr.getReferencesFrom(a_slot)):
        if ref.getToAddress().equals(a_odd):
            ref_mgr.delete(ref)
            print("[ok ] deleted ref 0x%08x -> 0x%08x (odd)" % (slot_int, target_int + 1))

    # Add/confirm DATA ref to target
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
    print("=== FixF07Seg4PeriodicFnPtrs (DRY=%s) ===" % DRY)
    n_ok = 0

    # Group 1: fn-ptr +1 fixes
    print("\n--- Group 1: fn-ptr +1 fixes (%d) ---" % len(FN_PTR_FIXES))
    for slot_int, fn_even_int, fn_label in FN_PTR_FIXES:
        print("\n[fn-ptr] 0x%08x -> 0x%08x (%s+1)" % (slot_int, fn_even_int, fn_label))
        if DRY:
            print("  [dry] ensure_label '%s' @ 0x%08x" % (fn_label, fn_even_int))
            print("  [dry] fix_data_ref 0x%08x -> 0x%08x" % (slot_int, fn_even_int))
            n_ok += 1
            continue
        _ensure_label(fn_even_int, fn_label)
        _fix_data_ref(slot_int, fn_even_int)
        n_ok += 1

    # Group 2: table label offset fixes
    print("\n--- Group 2: table offset label fixes (%d) ---" % len(TABLE_LABEL_FIXES))
    for slot_int, target_int, target_label in TABLE_LABEL_FIXES:
        print("\n[table] 0x%08x -> 0x%08x (%s)" % (slot_int, target_int, target_label))
        if DRY:
            print("  [dry] ensure_label '%s' @ 0x%08x" % (target_label, target_int))
            print("  [dry] fix_data_ref 0x%08x -> 0x%08x" % (slot_int, target_int))
            n_ok += 1
            continue
        _ensure_label(target_int, target_label)
        _fix_data_ref(slot_int, target_int)
        n_ok += 1

    # Group 3: EWRAM offset fixes
    print("\n--- Group 3: EWRAM offset fixes (%d) ---" % len(EWRAM_FIXES))
    made_labels = set()
    for slot_int, ewram_int, ewram_label in EWRAM_FIXES:
        print("\n[ewram] 0x%08x -> 0x%08x (%s)" % (slot_int, ewram_int, ewram_label))
        if DRY:
            print("  [dry] ensure_label '%s' @ 0x%08x" % (ewram_label, ewram_int))
            print("  [dry] fix_data_ref 0x%08x -> 0x%08x" % (slot_int, ewram_int))
            n_ok += 1
            continue
        if ewram_label not in made_labels:
            _ensure_label(ewram_int, ewram_label)
            made_labels.add(ewram_label)
        _fix_data_ref(slot_int, ewram_int)
        n_ok += 1

    total = len(FN_PTR_FIXES) + len(TABLE_LABEL_FIXES) + len(EWRAM_FIXES)
    print("\n=== FixF07Seg4PeriodicFnPtrs DONE: %d / %d fixed ===" % (n_ok, total))


main()
