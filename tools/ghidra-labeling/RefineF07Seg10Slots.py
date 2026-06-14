# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg10Slots.py -- F07 Seg-10 (0x08063830..0x080643e0)
#   equip effect chain cluster: 33 named fn (no FUN_) + 4 disasm blocks (4 new fn)
#   EQ=54 (50 existing-area slots + 4 disasm literal pool slots via RENAME)
#   RENAME=3 (PTR_gP1LifePoints_ -> gp1lp_ptr_*)
#   PLATE=2 (stale FUN_ substring replacements)
#   CONST_RENAME: card_info.inc SPECIAL_EQUIP_SENTINEL_ID -> URIA_LORD_CID
#                 asm/06 slot label special_equip_sentinel_id_18105 -> uria_lord_cid_18105
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- any CJK here is a red-line error.
# Disasm literal pools (7 DWORD slots) handled in DisassembleF07Seg10Blocks.py.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value->name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 (8 DWORD_ slots) ---
    (0x08063c00, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08063c00', None),
    (0x08063c40, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08063c40', None),
    (0x08063ed8, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08063ed8', None),
    (0x08063f18, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08063f18', None),
    (0x08063f58, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08063f58', None),
    (0x080641f4, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_080641f4', None),
    (0x08064304, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08064304', None),
    (0x08064350, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ptr_08064350', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (15 slots: 7 DAT_ + 8 DWORD_) ---
    (0x080638d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080638d4', None),
    (0x08063948, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063948', None),
    (0x080639b8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080639b8', None),
    (0x08063a24, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063a24', None),
    (0x08063e2c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063e2c', None),
    (0x08063e70, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063e70', None),
    (0x08063c44, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063c44', None),
    (0x08063edc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063edc', None),
    (0x08063f1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063f1c', None),
    (0x08063f5c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063f5c', None),
    (0x0806419c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_0806419c', None),
    (0x080641f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080641f8', None),
    (0x08064308, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08064308', None),
    (0x08064354, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08064354', None),
    (0x080643d0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080643d0', None),

    # --- ewram.inc: gEquipChainSlotRefs = 0x0201bb90 (4 slots: 2 DAT_ + 2 DWORD_) ---
    (0x080639b4, 0x0201bb90, 'gEquipChainSlotRefs',
     'chain_state_ptr_080639b4', None),
    (0x08063e6c, 0x0201bb90, 'gEquipChainSlotRefs',
     'chain_state_ptr_08063e6c', None),
    (0x08064064, 0x0201bb90, 'gEquipChainSlotRefs',
     'chain_state_ptr_08064064', None),
    (0x080643cc, 0x0201bb90, 'gEquipChainSlotRefs',
     'chain_state_ptr_080643cc', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (6 slots: 4 DAT_ + 2 DWORD_) ---
    (0x080639bc, 0x0201c510, 'gDuelFieldSlots',
     'duel_slots_ptr_080639bc', None),
    (0x08063a28, 0x0201c510, 'gDuelFieldSlots',
     'duel_slots_ptr_08063a28', None),
    (0x08063e30, 0x0201c510, 'gDuelFieldSlots',
     'duel_slots_ptr_08063e30', None),
    (0x08063e74, 0x0201c510, 'gDuelFieldSlots',
     'duel_slots_ptr_08063e74', None),
    (0x080641a0, 0x0201c510, 'gDuelFieldSlots',
     'duel_slots_ptr_080641a0', None),
    (0x080643d4, 0x0201c510, 'gDuelFieldSlots',
     'duel_slots_ptr_080643d4', None),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (1 DWORD_ slot) ---
    (0x08063c04, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'active_player_off_08063c04', None),

    # --- duel_field.inc: FIELD_STATE_OFF = 0x1cf4 (1 DWORD_ slot) ---
    (0x08063c08, 0x00001cf4, 'FIELD_STATE_OFF',
     'duel_phase_off_08063c08', None),

    # --- duel_field.inc: EQUIP_FLAG_TARGET_ICID_TABLE_OFF = 0x10b0 (1 DAT_ slot) ---
    (0x08063a2c, 0x000010b0, 'EQUIP_FLAG_TARGET_ICID_TABLE_OFF',
     'stat_table_off_08063a2c',
     'stat_table_offset=0x10b0 for equip flag target CID table'),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 (1 DWORD_ slot) ---
    (0x08064190, 0x0201b290, 'gDuelPhaseFlags',
     'phase_flags_ptr_08064190', None),

    # --- ewram.inc: LP_BAR_ANIM_STATE_OFF = 0x4cc (1 DWORD_ slot) ---
    (0x08064194, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'chain_count_off_08064194',
     'STATE_CHAIN_COUNT_OFFSET=0x4cc: chain slot count in gDuelPhaseFlags+0x4cc'),

    # --- ewram.inc: SPRITE_ROW_ENTRY_DATA_OFF = 0x4d4 (1 DWORD_ slot) ---
    (0x08064198, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',
     'chain_base_off_08064198',
     'STATE_CHAIN_BASE_OFFSET=0x4d4: chain slot byte array base in gDuelPhaseFlags+0x4d4'),

    # --- duel_field.inc: LP_COST_1500 = 0x5dc (1 DWORD_ slot) ---
    (0x080641a4, 0x000005dc, 'LP_COST_1500',
     'score_max_080641a4',
     'SCORE_MAX=0x5dc (1500)'),

    # --- fn-ptr slots (raw literal, RENAME type -> EQ creates label, EOL documents fn) ---
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

    # --- CID slots (reuse existing card_info.inc entries) ---
    (0x08063ce0, 0x0000194f, 'HYDROGEDDON_CID',
     'hydrogeddon_cid_08063ce0', None),
    (0x08063ce4, 0x00001950, 'OXYGEDDON_CID',
     'oxygeddon_cid_08063ce4', None),
    (0x08063ffc, 0x00001988, 'BURST_RETURN_CID',
     'burst_return_cid_08063ffc', None),
    (0x08064004, 0x000018a7, 'EHERO_BURSTINATRIX_CID',
     'burstinatrix_cid_08064004', None),
    (0x0806401c, 0x000018f9, 'EHERO_BUBBLEMAN_CID',
     'bubbleman_cid_0806401c', None),
    (0x08064068, 0x000018a8, 'EHERO_CLAYMAN_CID',
     'clayman_pair_cid_08064068', None),
    (0x08064250, 0x000019a3, 'URIA_LORD_CID',
     'uria_lord_cid_08064250', None),
    (0x08064254, 0x000019a4, 'HAMON_LORD_CID',
     'hamon_lord_cid_08064254', None),
    (0x080642a0, 0x000019a7, 'HERO_KID_CID',
     'hero_kid_cid_080642a0', None),
    (0x08063ee0, 0x000012f3, 'ULTIMATE_OFFERING_CID',
     'ultimate_offering_cid_08063ee0', None),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
#    Used for PTR_gP1LifePoints_* slots.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x080638d0, 'gp1lp_ptr_080638d0',
     'gP1LifePoints ptr for check_slot_revival_valid_with_zone_state LP read'),
    (0x08063944, 'gp1lp_ptr_08063944',
     'gP1LifePoints ptr for check_field_spell_placeable_with_opp_zone opp LP read'),
    (0x08063da8, 'gp1lp_ptr_08063da8',
     'gP1LifePoints ptr for check_slot_eligible_dark_field_equip slot resolve'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces stale FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # check_equip_slot_target_valid_in_zone plate: FUN_0807d014 -> current name
    (0x08063954, 'FUN_0807d014', 'tick_equip_target_validity_prng_lp_display'),
    # check_slot_eligible_water_dragon_pair plate: FUN_08059fc4 -> current name
    (0x08063c94, 'FUN_08059fc4', 'tick_equip_activation_if_pair_eligible'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- WARN treated as FAIL" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment (ASCII only)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_plate_fix(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment at func_addr."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate -- FAIL" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

# ---------------------------------------------------------------------------
# CONST_RENAME: update Ghidra symbol for uria_lord_cid_18105 (asm/06 slot)
#   The card_info.inc rename and asm/06 slot label rename are done in constants
#   files separately; this updates the Ghidra label for the asm/06 slot.
# ---------------------------------------------------------------------------
def _rename_uria_lord_slot():
    """Rename Ghidra label for asm/06 slot 0x0805af50:
       special_equip_sentinel_id_18105 -> uria_lord_cid_18105"""
    slot_addr = 0x0805af50
    old_label = 'special_equip_sentinel_id_18105'
    new_label = 'uria_lord_cid_18105'
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] CONST_RENAME Ghidra label 0x%08x: %s -> %s" % (slot_addr, old_label, new_label))
        return

    # Check ROM value is 0x000019a3
    if not _check(slot_addr, 0x000019a3, 'URIA_LORD_CID'):
        print("[WARN] CONST_RENAME slot 0x%08x: value check failed, skipping" % slot_addr)
        return

    existing = sym_tbl.getSymbols(a)
    for sym in existing:
        if sym.getName() == old_label:
            sym.setName(new_label, SourceType.USER_DEFINED)
            print("[CREN] 0x%08x: %s -> %s" % (slot_addr, old_label, new_label))
            return

    # If old label not found, just create new label
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if new_label not in names:
        sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
        print("[CREN] 0x%08x: created label %s (old label not found)" % (slot_addr, new_label))
    else:
        print("[CREN] 0x%08x: %s already exists" % (slot_addr, new_label))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF07Seg10Slots (DRY=%s) ===" % DRY)
    print("  Seg-10: 0x08063830..0x080643e0, 33 named fn")
    print("  EQ=%d  RENAME=%d  PLATE=%d  CONST_RENAME=1" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        # Pre-check value
        mem = currentProgram.getMemory()
        a = _addr(slot_addr)
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
            if actual != (value & 0xFFFFFFFF):
                eq_fail += 1
                print("[FAIL] 0x%08x (%s): rom=0x%08x expect=0x%08x" % (
                    slot_addr, eq_name, actual, value & 0xFFFFFFFF))
                continue
        except Exception as e:
            eq_fail += 1
            print("[FAIL] 0x%08x (%s): read error %s" % (slot_addr, eq_name, e))
            continue
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES -- check values before real run !!!" % eq_fail)

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # C. PLATE_REWRITES
    print("\n--- C. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    # D. CONST_RENAME: asm/06 slot label rename in Ghidra
    print("\n--- D. CONST_RENAME (asm/06 URIA_LORD_CID slot label) ---")
    _rename_uria_lord_slot()

    print("\n=== RefineF07Seg10Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE=%d  CONST_RENAME=1" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

main()
