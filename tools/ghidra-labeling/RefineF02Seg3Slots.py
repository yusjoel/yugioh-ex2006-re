# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg3Slots.py -- file 02 Seg-3 (0x0802f3a8..0x0802fd00)
#   zone chain count / eligibility query / equip find cluster (23 fn, 58 slots)
#   query_zone_chain_count_with_eligibility /
#   query_slot_effect_eligibility_with_equip_fallback /
#   count_slot_equip_list_matches /
#   count_active_extended_chain_nodes /
#   find_zone_chain_node_by_card_id_pair /
#   find_equip_chain_node_by_slot_pair /
#   count_equip_slots_with_active_chain /
#   find_equip_chain_pair_across_field /
#   find_node_packed_by_card_id_in_dual_lists /
#   find_card_slot_by_zone_card_id /
#   find_equip_slot_by_zone_card_id_with_flag /
#   find_equip_chain_node_by_type_d /
#   find_equip_target_for_card_slot /
#   build_equip_chain_slot_entry /
#   find_node_by_value /
#   find_node_by_value_and_zone_type /
#   find_node_by_value_zone_entity /
#   count_chain_nodes_by_card_id /
#   count_chain_nodes_by_card_id_and_type /
#   count_slot_chain_nodes_by_card_id /
#   count_slot_chain_nodes_by_card_id_and_type /
#   check_value_in_slot_chain /
#   check_value_in_effect_context_chain
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (all reuse existing inc constants)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- FUN_ -> current name in plate comments (pure ASCII)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0, disasm=0 for this segment.
# NOTE: gDuelEffectChainSlots=0x0201bc54 added to ewram.inc (new global, 17 raw refs).

from ghidra.program.model.symbol import SourceType, RefType
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

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, EQ_REUSE, 14 slots) ---
    (0x0802f4cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_list_player_stride', None),
    (0x0802f544, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_ext_nodes_player_stride', None),
    (0x0802f594, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_zone_node_player_stride', None),
    (0x0802f5d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_node_pair_player_stride', None),
    (0x0802f678, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_slots_player_stride', None),
    (0x0802f6a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_pair_player_stride', None),
    (0x0802f7f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_card_slot_player_stride', None),
    (0x0802f8b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_slot_flag_player_stride', None),
    (0x0802f910, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_type_d_player_stride', None),
    (0x0802f9d0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_target_player_stride', None),
    (0x0802fab0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_entry_player_stride', None),
    (0x0802fc58, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_slot_nodes_player_stride', None),
    (0x0802fc88, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_slot_nodes_type_player_stride', None),
    (0x0802fcb8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_chain_player_stride', None),

    # --- EQUIP_NODE_BASE_OFFSET = 0x000014b0 (duel_field.inc, EQ_REUSE, 7 slots) ---
    (0x0802f4d4, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'count_equip_list_node_base_off', None),
    (0x0802f54c, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'count_ext_nodes_node_base_off', None),
    (0x0802f618, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_equip_node_pair_node_base_off', None),
    (0x0802f7fc, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_card_slot_node_base_off', None),
    (0x0802f8b8, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_equip_slot_flag_node_base_off', None),
    (0x0802f918, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_type_d_node_base_off', None),
    (0x0802f9d8, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_equip_target_node_base_off', None),

    # --- OAM_ATTR0_HIDDEN = 0x0000ffff (oam_attr.inc, EQ_REUSE, 7 slots) ---
    (0x0802f6e0, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_equip_pair_not_found', None),
    (0x0802f764, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_packed_node_not_found', None),
    (0x0802f818, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_card_slot_not_found', None),
    (0x0802f8d4, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_equip_slot_flag_not_found', None),
    (0x0802f92c, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_type_d_not_found', None),
    (0x0802f9f8, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_equip_target_not_found', None),
    (0x0802fabc, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'build_equip_entry_no_pair_sentinel', None),

    # --- NODE_POOL_NEG_OFFSET = 0xffffeb50 (duel_field.inc, EQ_REUSE, 4 slots) ---
    (0x0802f4dc, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'count_equip_list_pool_neg_off', None),
    (0x0802f800, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'find_card_slot_pool_neg_off', None),
    (0x0802f8bc, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'find_equip_slot_flag_pool_neg_off', None),
    (0x0802f9dc, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'find_equip_target_pool_neg_off', None),

    # --- SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (gl_scrollbar.inc, EQ_REUSE, 1 slot) ---
    (0x0802fab8, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',
     'build_equip_entry_attr_mask',
     'clears bits[14:6] of node[+4] OAM attr word'),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # --- gDuelFieldSlots = 0x0201c510 (ewram.inc, existing; 14 slots) ---
    (0x0802f4d0, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_list_field_slots',
     'duel field zone slot array base'),
    (0x0802f548, 0x0201c510, 'gDuelFieldSlots',
     'count_ext_nodes_field_slots', None),
    (0x0802f598, 0x0201c510, 'gDuelFieldSlots',
     'find_zone_node_field_slots', None),
    (0x0802f5d8, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_node_pair_field_slots', None),
    (0x0802f67c, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_slots_field_slots', None),
    (0x0802f6a8, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_pair_field_slots', None),
    (0x0802f7f8, 0x0201c510, 'gDuelFieldSlots',
     'find_card_slot_field_slots', None),
    (0x0802f8b4, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_slot_flag_field_slots', None),
    (0x0802f914, 0x0201c510, 'gDuelFieldSlots',
     'find_type_d_field_slots', None),
    (0x0802f9d4, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_target_field_slots', None),
    (0x0802fab4, 0x0201c510, 'gDuelFieldSlots',
     'build_equip_entry_field_slots', None),
    (0x0802fc5c, 0x0201c510, 'gDuelFieldSlots',
     'count_slot_nodes_field_slots', None),
    (0x0802fc8c, 0x0201c510, 'gDuelFieldSlots',
     'count_slot_nodes_type_field_slots', None),
    (0x0802fcbc, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_chain_field_slots', None),

    # --- gEquipNodePool = 0x0201d9c0 (ewram.inc, existing; 7 slots) ---
    (0x0802f59c, 0x0201d9c0, 'gEquipNodePool',
     'find_zone_node_pool',
     'equip chain node pool base'),
    (0x0802f738, 0x0201d9c0, 'gEquipNodePool',
     'find_packed_node_pool', None),
    (0x0802fb18, 0x0201d9c0, 'gEquipNodePool',
     'find_node_val_pool', None),
    (0x0802fb58, 0x0201d9c0, 'gEquipNodePool',
     'find_node_val_type_pool', None),
    (0x0802fba8, 0x0201d9c0, 'gEquipNodePool',
     'find_node_val_zone_pool', None),
    (0x0802fbf0, 0x0201d9c0, 'gEquipNodePool',
     'count_nodes_card_pool', None),
    (0x0802fc30, 0x0201d9c0, 'gEquipNodePool',
     'count_nodes_card_type_pool', None),

    # --- gDuelEffectChainSlots = 0x0201bc54 (ewram.inc NEW; 2 slots) ---
    (0x0802f734, 0x0201bc54, 'gDuelEffectChainSlots',
     'find_packed_node_effect_slots',
     'effect context chain slot array; 2 entries stride 20B'),
    (0x0802fcfc, 0x0201bc54, 'gDuelEffectChainSlots',
     'check_effect_chain_slots_base', None),

    # --- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc, existing; 1 slot) ---
    (0x0802fcf8, 0x0201bb90, 'gEquipChainSlotRefs',
     'check_effect_chain_refs_base',
     'equip chain slot ref array; [+0]=activation_player [+0x1c]=slot_ref'),

]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    (0x0802f4d8, 'count_equip_list_zone_type_bias',
     'zone_type range bias: (type<<16 + 0xfffa0000)>>16 selects type [6..11]'),

]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [

    # 1. count_slot_equip_list_matches (0x0802f434) plate:
    #    FUN_0802f3e0 -> query_slot_effect_eligibility_with_equip_fallback
    (0x0802f434,
     'FUN_0802f3e0',
     'query_slot_effect_eligibility_with_equip_fallback'),

    # 2. find_equip_chain_node_by_slot_pair (0x0802f5b0) plate:
    #    FUN_0802f680 -> find_equip_chain_pair_across_field
    (0x0802f5b0,
     'FUN_0802f680',
     'find_equip_chain_pair_across_field'),

    # 3. find_node_by_value_and_zone_type (0x0802fb2c) plate -- 4 replacements:
    (0x0802fb2c,
     'FUN_0802fdc0',
     'check_node_in_slot_chain'),

    (0x0802fb2c,
     'FUN_0802fe98',
     'get_zone_node_entity_hword_by_card_and_type'),

    (0x0802fb2c,
     'FUN_0802ff34',
     'check_node_in_zone_idx_chain'),

    (0x0802fb2c,
     'FUN_0802ff84',
     'get_entity_id_in_zone_idx_chain_by_type'),

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
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (
            slot_addr, target_vaddr, gas_label, slot_label))
        return

    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (
        slot_addr, target_vaddr, gas_label, slot_label))

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
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg3Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-3: 0x0802f3a8..0x0802fd00, 23 fn, 58 slots")
    print("  EQ=%d REF=%d RENAME=%d PLATE_REWRITES=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES: FUN_ fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF02Seg3Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

main()
