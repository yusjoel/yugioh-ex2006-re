# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg2Slots.py -- file 02 Seg-2 (0x0802e108..0x0802f3a8)
#   campaign card-select display + equip chain node management (23 fn, 94 slots)
#   tick_campaign_card_select_display_state / tick_aob_display_with_sprite_enable_blend /
#   tick_aob_display_with_fadein / find_active_equip_chain_head /
#   replace_slot_chain_ref_by_id / replace_chain_refs_by_slot_id_for_player /
#   link_equip_node_to_chain / append_equip_chain_node_at_tail /
#   replace_chain_refs_for_slot / replace_chain_refs_by_id_filtered /
#   replace_equip_chain_slot_refs_by_match / replace_chain_node_ref_by_zone_match /
#   clear_chain_refs_for_low_zone_nodes / clear_equip_refs_for_leaving_slot /
#   clear_equip_chain_refs_for_slot_zone / repair_slot_equip_chain_node_refs /
#   rebuild_equip_chain_refs / purge_equip_chain_refs_for_zone_slot /
#   clear_zone_slot_card_ref_bits / update_equip_chain_zone_slot_refs /
#   count_slot_chain_copies_of_card / count_zone_chain_eligible_cards /
#   count_equip_chain_default_flags
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (new + reuse existing inc constants)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- FUN_ -> current name in plate comments (pure ASCII)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: PLAYER_BLOCK_STRIDE = 0x868 reuses ewram.inc constant (already defined).
# NOTE: FIELD_PLAYER_STRIDE = 0x868 (proposal name) -> reuse PLAYER_BLOCK_STRIDE.
# NOTE: carve labels (deck_type_table, scene_scroll_table) are created in rom.s;
#       REF_SLOTS below reference them.
# NOTE: R4 disasm (Block1/Block2) handled in RefineF02Seg2Disasm.py.

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

    # --- gDuelSceneBase = 0x02023360 (ewram.inc, EQ_REUSE, 8 slots) ---
    (0x0802e144, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx', None),
    (0x0802e204, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_b', None),
    (0x0802e424, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_c', None),
    (0x0802e468, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_d', None),
    (0x0802e484, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_e', None),
    (0x0802e7a0, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_f', None),
    (0x0802e880, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_g', None),
    (0x0802e914, 0x02023360, 'gDuelSceneBase',
     'tick_campaign_scene_ctx_h', None),

    # --- CAMPAIGN_CARD_ANIM_STEP_MASK = 0xfffffe03 (duel_field.inc, EQ_REUSE, 4 slots) ---
    (0x0802e1ac, 0xfffffe03, 'CAMPAIGN_CARD_ANIM_STEP_MASK',
     'tick_campaign_step_mask_a', None),
    (0x0802e200, 0xfffffe03, 'CAMPAIGN_CARD_ANIM_STEP_MASK',
     'tick_campaign_step_mask_b', None),
    (0x0802e884, 0xfffffe03, 'CAMPAIGN_CARD_ANIM_STEP_MASK',
     'tick_campaign_step_mask_c', None),
    (0x0802e8dc, 0xfffffe03, 'CAMPAIGN_CARD_ANIM_STEP_MASK',
     'tick_campaign_step_mask_d', None),

    # --- FIELD_SLOT_PHASE_MASK = 0xfffffc07 (duel_field.inc NEW, 3 slots) ---
    (0x0802e7a8, 0xfffffc07, 'FIELD_SLOT_PHASE_MASK',
     'tick_campaign_phase_mask_a',
     'clears bits[9:3] of AOB state halfword (scene_ctx+0x60)'),
    (0x0802e80c, 0xfffffc07, 'FIELD_SLOT_PHASE_MASK',
     'tick_campaign_phase_mask_b', None),
    (0x0802e844, 0xfffffc07, 'FIELD_SLOT_PHASE_MASK',
     'tick_campaign_phase_mask_c', None),

    # --- PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc, EQ_REUSE, 12 slots) ---
    (0x0802ea30, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'replace_slot_chain_player_stride',
     'player data block stride 0x868 bytes'),
    (0x0802eabc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'replace_chain_slot_player_stride', None),
    (0x0802eb34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'link_equip_node_player_stride', None),
    (0x0802ed90, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'clear_equip_refs_player_stride', None),
    (0x0802ee58, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'repair_slot_chain_player_stride', None),
    (0x0802ef14, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'rebuild_chain_refs_player_stride', None),
    (0x0802efe4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'purge_equip_chain_player_stride', None),
    (0x0802f034, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'purge_equip_chain_player_stride_b', None),
    (0x0802f0cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'clear_zone_ref_player_stride', None),
    (0x0802f144, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'update_chain_zone_player_stride', None),
    (0x0802f1f0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'update_chain_zone_player_stride_b', None),
    (0x0802f26c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_chain_copies_player_stride', None),
    (0x0802f31c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_zone_chain_player_stride', None),

    # --- NODE_POOL_NEG_OFFSET = 0xffffeb50 (duel_field.inc NEW, 4 slots) ---
    (0x0802eb38, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'link_equip_node_pool_neg_off',
     'neg offset (-0x14b0) from gEquipNodePool to gDuelFieldSlots base'),
    (0x0802ef20, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'rebuild_chain_refs_pool_neg_off', None),
    (0x0802f148, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'update_chain_zone_pool_neg_off', None),
    (0x0802f32c, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'count_zone_chain_pool_neg_off', None),

    # --- EQUIP_CHAIN_LINK_OFFSET = 0xfffffc02 (duel_field.inc NEW, 1 slot) ---
    (0x0802eb90, 0xfffffc02, 'EQUIP_CHAIN_LINK_OFFSET',
     'append_equip_chain_link_off',
     'chain link sub-array base offset within node (-0x3fe)'),

    # --- gPrng = 0x03000040 (iwram.inc, EQ_REUSE) ---
    (0x0802e420, 0x03000040, 'gPrng',
     'tick_campaign_prng_ctx', None),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # --- deck_type_table @ 0x09e59dc4 (carve Host C sub-split) ---
    (0x0802e1a8, 0x09e59dc4, 'deck_type_table',
     'tick_campaign_deck_type_tbl',
     '8-entry u16 deck_type->sprite_tile_offset lookup'),
    (0x0802e888, 0x09e59dc4, 'deck_type_table',
     'tick_campaign_deck_type_tbl_b', None),

    # --- tick_campaign_dispatch_tbl_ptr: ptr to dispatch table at 0x0802e20c ---
    # (also in RENAME_SLOTS for EOL; here we create label at target 0x0802e20c)
    (0x0802e208, 0x0802e20c, 'dispatch_table_seg2_blk1',
     'tick_campaign_dispatch_tbl_ptr',
     'ptr to 8-entry phase dispatch table at 0x0802e20c (MOV PC target)'),

    # --- scene_scroll_table @ 0x09e59dd4 (carve Host C sub-split) ---
    (0x0802e7ac, 0x09e59dd4, 'scene_scroll_table',
     'tick_campaign_scroll_tbl',
     '0x20-entry u16 symmetric scroll position table'),

    # --- gEquipChainSlotRefs = 0x0201bb90 (new global) ---
    (0x0802ea2c, 0x0201bb90, 'gEquipChainSlotRefs',
     'replace_slot_chain_refs_base',
     'equip chain slot reference array base'),

    # --- gDuelFieldSlots = 0x0201c510 (new global, 8 slots) ---
    (0x0802eac0, 0x0201c510, 'gDuelFieldSlots',
     'replace_chain_slot_field_slots',
     'duel field zone slot array; player*0x868 + slot*0x14'),
    (0x0802ed8c, 0x0201c510, 'gDuelFieldSlots',
     'clear_equip_refs_field_slots', None),
    (0x0802ee5c, 0x0201c510, 'gDuelFieldSlots',
     'repair_slot_chain_field_slots', None),
    (0x0802ef18, 0x0201c510, 'gDuelFieldSlots',
     'rebuild_chain_refs_field_slots', None),
    (0x0802efe8, 0x0201c510, 'gDuelFieldSlots',
     'purge_equip_chain_field_slots', None),
    (0x0802f038, 0x0201c510, 'gDuelFieldSlots',
     'purge_equip_chain_field_slots_b', None),
    (0x0802f0d0, 0x0201c510, 'gDuelFieldSlots',
     'clear_zone_ref_field_slots', None),
    (0x0802f1ec, 0x0201c510, 'gDuelFieldSlots',
     'update_chain_zone_field_slots', None),
    (0x0802f270, 0x0201c510, 'gDuelFieldSlots',
     'count_chain_copies_field_slots', None),
    (0x0802f320, 0x0201c510, 'gDuelFieldSlots',
     'count_zone_chain_field_slots', None),

    # --- gEquipNodePool = 0x0201d9c0 (new global, 12 slots) ---
    (0x0802eac4, 0x0201d9c0, 'gEquipNodePool',
     'replace_chain_slot_node_pool',
     'equip chain node pool; node_idx*8 stride'),
    (0x0802eb30, 0x0201d9c0, 'gEquipNodePool',
     'link_equip_node_pool_base', None),
    (0x0802eb8c, 0x0201d9c0, 'gEquipNodePool',
     'append_equip_node_pool_base', None),
    (0x0802ebb8, 0x0201d9c0, 'gEquipNodePool',
     'replace_chain_refs_for_slot_pool', None),
    (0x0802ebf8, 0x0201d9c0, 'gEquipNodePool',
     'replace_chain_refs_id_filtered_pool', None),
    (0x0802ec38, 0x0201d9c0, 'gEquipNodePool',
     'replace_equip_chain_slot_pool', None),
    (0x0802ec7c, 0x0201d9c0, 'gEquipNodePool',
     'replace_chain_node_zone_pool', None),
    (0x0802ecb4, 0x0201d9c0, 'gEquipNodePool',
     'clear_chain_low_zone_pool', None),
    (0x0802ed9c, 0x0201d9c0, 'gEquipNodePool',
     'clear_equip_refs_node_pool', None),
    (0x0802edec, 0x0201d9c0, 'gEquipNodePool',
     'clear_equip_chain_zone_pool', None),
    (0x0802ee60, 0x0201d9c0, 'gEquipNodePool',
     'repair_slot_chain_node_pool', None),
    (0x0802ef1c, 0x0201d9c0, 'gEquipNodePool',
     'rebuild_chain_refs_node_pool', None),
    (0x0802efec, 0x0201d9c0, 'gEquipNodePool',
     'purge_equip_chain_node_pool', None),
    (0x0802f0f4, 0x0201d9c0, 'gEquipNodePool',
     'clear_zone_ref_node_pool', None),
    (0x0802f324, 0x0201d9c0, 'gEquipNodePool',
     'count_zone_chain_node_pool', None),

    # --- gDuelFieldSlotState = 0x0201c520 (new global, 2 slots) ---
    (0x0802ed98, 0x0201c520, 'gDuelFieldSlotState',
     'clear_equip_refs_slot_state',
     'parallel slot state flags at gDuelFieldSlots+0x10'),
    (0x0802f330, 0x0201c520, 'gDuelFieldSlotState',
     'count_zone_chain_slot_state', None),

    # --- EQUIP_NODE_BASE_OFFSET = 0x000014b0 (duel_field.inc NEW, 2 slots; treat as EQ via REF) ---
    # Note: these are positive offset constants referenced as literals; using EQ approach
    # (they appear in the EQ list but also need REF-style labeling as positive offsets)
    # Actually per proposal these are EQ_SLOTS; already in EQ_SLOTS above via REF notes.
    # Correcting: 0x0802f274 and 0x0802f1f4 are EQ slots for EQUIP_NODE_BASE_OFFSET.

]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # dispatch table pointers
    # NOTE: 0x0802e208 is handled in REF_SLOTS (slot label set there); skip here.
    (0x0802e530, 'tick_campaign_sub_dispatch_tbl_ptr',
     'ptr to 8-entry sub-state dispatch table at 0x0802e534'),
    (0x0802e534, 'tick_campaign_sub_dispatch_tbl_start',
     'sub-state dispatch table[0] -> block2 start (THUMB, MOV PC target)'),

    # sprite attribute constants
    (0x0802e7a4, 'tick_campaign_sprite_attr_a',
     'scene_ctx+0x48 sprite attr: tile_hi=0x0080 x=0x68'),
    (0x0802e808, 'tick_campaign_sprite_attr_b',
     'scene_ctx+0x48 sprite attr variant b: 0x0068 0x0068'),

    # equip chain offsets (gP1LifePoints-relative)
    (0x0802e984, 'find_equip_head_chain_off',
     'gP1LifePoints+0x14ea = equip_node_pool+0xa (chain head entry)'),
    (0x0802ea28, 'replace_slot_chain_clear_off',
     'gP1LifePoints+0x14e6 = equip_node_pool+0x6 (8-hword clear area)'),
    (0x0802ea34, 'replace_slot_chain_p0_list_off',
     'gP1LifePoints+0x10e6 = player0 chain slot list base'),
    (0x0802ea38, 'replace_slot_chain_p1_list_off',
     'gP1LifePoints+0x14ee = player1 chain slot list base'),

    # sentinel and check constants
    (0x0802ecb8, 'clear_chain_low_zone_sentinel',
     'card_id sentinel: 0x164f (Guardian Tryce) skipped in ref clear'),
    (0x0802ed94, 'clear_equip_refs_slot_active_check',
     'lsls#0x13 result for active slot (bits[31:19] = 0x1368)'),
    (0x0802eda0, 'clear_equip_refs_zone_word_mask',
     'lower 20-bit mask for zone slot word compare'),
    (0x0802eda4, 'clear_equip_refs_zone_type_pattern',
     'zone type pattern 0x31368 matched in equip ref scan'),
    (0x0802eda8, 'clear_equip_refs_zone_ref_limit',
     'zone ref index limit 0x197f for find_chain_node_by_dual_halfword'),

    # chain head / rebuild offsets
    (0x0802ede8, 'clear_equip_chain_zone_head_off',
     'gP1LifePoints+0x10e2 = equip zone chain head base offset'),
    (0x0802ef7c, 'rebuild_chain_refs_card_id_a',
     'card_id filter 0x1561 (Relinquished) for equip chain scan'),
    (0x0802ef80, 'rebuild_chain_refs_card_id_b',
     'card_id filter 0x1852 (Thousand-Eyes Restrict) for equip chain scan'),

    # purge type thresholds
    (0x0802f03c, 'purge_equip_chain_type_thr_a',
     'card type threshold 0x18c2 for purge path dispatch'),
    (0x0802f040, 'purge_equip_chain_type_thr_b',
     'card type threshold 0x1343 for purge path dispatch'),
    (0x0802f044, 'purge_equip_chain_type_thr_c',
     'card type threshold 0x1743 for purge path dispatch'),
    (0x0802f0c8, 'purge_equip_chain_type_thr_d',
     'card type threshold 0x1957 for purge path dispatch'),

    # card_id extraction masks
    (0x0802f278, 'count_chain_copies_card_id_mask',
     'upper 14-bit card_id extraction mask (lsls+lsrs with 0xfffa0000)'),
    (0x0802f328, 'count_zone_chain_card_id_mask',
     'same mask reused in count_zone_chain_eligible_cards'),

]

# EQ for EQUIP_NODE_BASE_OFFSET (0x000014b0, duel_field.inc NEW)
# These are positive offset literal pool slots -> add to EQ_SLOTS extension
EQ_SLOTS_EXTRA = [
    (0x0802f274, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'count_chain_copies_node_base_off',
     'positive offset from gDuelFieldSlots to gEquipNodePool (0x1d9c0-0x1c510=0x14b0)'),
    (0x0802f1f4, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'update_chain_zone_node_base_off', None),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. tick_opponent_aob_display (0x0802dfb8, Seg-1) plate: FUN_0802e108 -> tick_campaign_card_select_display_state
    (0x0802dfb8,
     'FUN_0802e108',
     'tick_campaign_card_select_display_state'),

    # 2. find_active_equip_chain_head (0x0802e95c) plate: FUN_0802eac8 -> link_equip_node_to_chain
    (0x0802e95c,
     'FUN_0802eac8',
     'link_equip_node_to_chain'),

    # 3. find_active_equip_chain_head (0x0802e95c) plate: FUN_0802eb3c -> append_equip_chain_node_at_tail
    (0x0802e95c,
     'FUN_0802eb3c',
     'append_equip_chain_node_at_tail'),

    # 4. replace_slot_chain_ref_by_id (0x0802e988) plate: FUN_0802eeac -> rebuild_equip_chain_refs
    (0x0802e988,
     'FUN_0802eeac',
     'rebuild_equip_chain_refs'),

    # 5. replace_slot_chain_ref_by_id (0x0802e988) plate: FUN_0802ef84 -> purge_equip_chain_refs_for_zone_slot
    (0x0802e988,
     'FUN_0802ef84',
     'purge_equip_chain_refs_for_zone_slot'),

    # 6. count_equip_chain_default_flags (0x0802f394) plate: FUN_0802f3a8 -> query_zone_chain_count_with_eligibility
    (0x0802f394,
     'FUN_0802f3a8',
     'query_zone_chain_count_with_eligibility'),
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
    print("=== RefineF02Seg2Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-2: 0x0802e108..0x0802f3a8, 23 fn, 94 slots")

    all_eq = EQ_SLOTS + EQ_SLOTS_EXTRA

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(all_eq))
    eq_ok = 0
    for entry in all_eq:
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

    print("\n=== RefineF02Seg2Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d" % (
        len(all_eq), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

main()
