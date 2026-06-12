# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg3Slots.py -- file 04 Seg-3 (0x08040c88..0x080417f0)
#   19 functions: clear_display_step_lock_b/c/d/e/f/g/h /
#   clear_card_display_state_flag / tick_zone_slot_spell_remove_display_seq /
#   tick_field_clear_display_sequence / tick_player_hand_shuffle_display_seq /
#   tick_card_lp_change_cycle_display_seq / tick_find_slot_by_card_id_display_seq /
#   tick_card_change_position_display_state / tick_zone_card_place_by_id_seq /
#   tick_card_id_zone_find_display_seq / tick_spell_equip_zone_display_seq /
#   tick_card_display_op28_clear_seq / tick_card_display_op2b_lp_clear_seq
#
# Sections:
#   A. EQ_SLOTS    -- 87 total (84 reuse + 3 new: LP_CARD_TRACK_BASE/NEXT/AUX_OFF in ewram.inc)
#   B. REF_SLOTS   -- 0
#   C. RENAME_SLOTS -- 0 (no PTR_ or extra renames beyond EQ coverage)
#   D. PLATE_REWRITES -- 18 functions with stale FUN_0803be4c / (0x0803be4c)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).
# NOTE: FUNC_RENAME = 0 (no function renames in this segment).
# NOTE: PTR_gP1LifePoints_* slots (11 total) already correctly named -- no action needed.

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
#    All values verified against roms/2343.gba (python struct.unpack_from).
#    PTR_gP1LifePoints_* slots are skipped here (already correctly named).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- clear_display_step_lock_b (0x08040c88) ---
    (0x08040c94, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_b_state_base',        None),
    (0x08040c98, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_b_step_lock_off',    None),
    # --- clear_display_step_lock_c (0x08040c9c) ---
    (0x08040ca8, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_c_state_base',        None),
    (0x08040cac, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_c_step_lock_off',    None),
    # --- clear_display_step_lock_d (0x08040cb0) ---
    (0x08040cbc, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_d_state_base',        None),
    (0x08040cc0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_d_step_lock_off',    None),
    # --- clear_display_step_lock_e (0x08040cc4) ---
    (0x08040cd0, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_e_state_base',        None),
    (0x08040cd4, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_e_step_lock_off',    None),
    # --- clear_display_step_lock_f (0x08040cd8) ---
    (0x08040ce4, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_f_state_base',        None),
    (0x08040ce8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_f_step_lock_off',    None),
    # --- clear_display_step_lock_g (0x08040cec) ---
    (0x08040cf8, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_g_state_base',        None),
    (0x08040cfc, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_g_step_lock_off',    None),
    # --- clear_display_step_lock_h (0x08040d00) ---
    (0x08040d0c, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_lock_h_state_base',        None),
    (0x08040d10, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_lock_h_step_lock_off',    None),
    # --- clear_card_display_state_flag (0x08040d14) ---
    (0x08040d20, 0x0201bcc0, 'gDuelDisplaySeqState',     'clr_flag_state_base',          None),
    (0x08040d24, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clr_flag_step_lock_off',      None),
    # --- tick_zone_slot_spell_remove_display_seq (0x08040d28) ---
    (0x08040e20, 0x0201bcc0, 'gDuelDisplaySeqState',     'spell_remove_state_base',      None),
    # PTR_gP1LifePoints_08040e24: 0x0201c4e0 -- already correctly named, skip
    (0x08040e28, 0x00000818, 'DISP_SEQ_CARD_SET_CTR_OFF', 'spell_remove_step_ctr_off',   None),
    (0x08040e2c, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'spell_remove_slot_mask_a',     None),
    (0x08040e30, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',    'spell_remove_slot_mask_b',     None),
    (0x08040e34, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',    'spell_remove_slot_mask_c',     None),
    (0x08040e50, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'spell_remove_step_lock_off',  None),
    # --- tick_field_clear_display_sequence (0x08040e54) ---
    (0x08040e6c, 0x0201bcc0, 'gDuelDisplaySeqState',     'field_clear_state_base',       None),
    (0x08040eb4, 0x0201bcc0, 'gDuelDisplaySeqState',     'field_clear_state_base_b',     None),
    (0x08040eb8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'field_clear_step_lock_off',   None),
    # --- tick_player_hand_shuffle_display_seq (0x08040ebc) ---
    (0x08040ee4, 0x0201bcc0, 'gDuelDisplaySeqState',     'hand_shuffle_state_base',      None),
    # PTR_gP1LifePoints_08040f34: 0x0201c4e0 -- skip
    (0x08040f38, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'hand_shuffle_player_stride',   None),
    (0x08040f58, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'hand_shuffle_step_lock_off',  None),
    # --- tick_card_lp_change_cycle_display_seq (0x08040f5c) ---
    (0x08040f9c, 0x0201bcc0, 'gDuelDisplaySeqState',     'lp_change_state_base',         None),
    # PTR_gP1LifePoints_08040fa0: 0x0201c4e0 -- skip
    (0x08040fa4, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'lp_change_player_stride',      None),
    (0x08040fb8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'lp_change_step_lock_off',     None),
    # --- tick_find_slot_by_card_id_display_seq (0x08040fbc) ---
    (0x08040fe4, 0x0201bcc0, 'gDuelDisplaySeqState',     'find_slot_state_base',         None),
    # PTR_gP1LifePoints_08041020: 0x0201c4e0 -- skip
    (0x08041024, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'find_slot_player_stride',      None),
    (0x08041040, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'find_slot_step_lock_off',     None),
    # --- tick_card_change_position_display_state (0x08041044) ---
    (0x08041060, 0x0201bcc0, 'gDuelDisplaySeqState',     'chg_pos_state_base',           None),
    # PTR_gP1LifePoints_080410a0: 0x0201c4e0 -- skip
    (0x080410a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'chg_pos_player_stride',        None),
    (0x080410c0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'chg_pos_step_lock_off',       None),
    # --- tick_zone_card_place_by_id_seq (0x080410c4) ---
    (0x08041120, 0x0201bcc0, 'gDuelDisplaySeqState',     'zone_place_state_base',        None),
    (0x0804120c, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'zone_place_player_stride',     None),
    (0x08041210, 0x0201c600, 'gP1FieldArrayCBase',       'zone_place_field_array_c',     None),
    (0x08041214, 0x0201c4d8, 'gDuelChainDescBase',       'zone_place_chain_desc_base',   None),
    (0x08041218, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'zone_place_slot_mask_a',       None),
    (0x0804121c, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',    'zone_place_slot_mask_b',       None),
    (0x08041220, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',    'zone_place_slot_mask_c',       None),
    (0x080412ec, 0x000015c7, 'COST_DOWN_CID',            'zone_place_cost_down_cid',
     'COST_DOWN_CID=0x15c7: Cost Down card check in tick_zone_card_place_by_id_seq step2'),
    # PTR_gP1LifePoints_080412f0: 0x0201c4e0 -- skip
    (0x080412f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'zone_place_player_stride_b',   None),
    (0x080412f8, 0x00001cf4, 'FIELD_STATE_OFF',          'zone_place_field_state_off',   None),
    (0x080412fc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',     'zone_place_lp_block2_off',     None),
    (0x08041300, 0x0201e2a0, 'gDuelCardCtxBase',         'zone_place_card_ctx_base',     None),
    (0x08041304, 0x0201bcc0, 'gDuelDisplaySeqState',     'zone_place_state_base_b',      None),
    (0x0804132c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'zone_place_step_lock_off',    None),
    # --- tick_card_id_zone_find_display_seq (0x08041330) ---
    (0x08041380, 0x0201bcc0, 'gDuelDisplaySeqState',     'id_zone_find_state_base',      None),
    (0x08041458, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'id_zone_find_player_stride',   None),
    (0x0804145c, 0x0201c600, 'gP1FieldArrayCBase',       'id_zone_find_field_array_c',   None),
    (0x08041460, 0x0201c4d8, 'gDuelChainDescBase',       'id_zone_find_chain_desc_base', None),
    (0x08041464, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'id_zone_find_slot_mask_a',     None),
    (0x08041468, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',    'id_zone_find_slot_mask_b',     None),
    (0x0804146c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',    'id_zone_find_slot_mask_c',     None),
    (0x08041490, 0x0201bcc0, 'gDuelDisplaySeqState',     'id_zone_find_state_base_b',    None),
    # PTR_gP1LifePoints_080414e8: 0x0201c4e0 -- skip
    (0x080414ec, 0x00001cf4, 'FIELD_STATE_OFF',          'id_zone_find_field_state_off', None),
    (0x080414f0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',     'id_zone_find_lp_block2_off',   None),
    (0x080414f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'id_zone_find_player_stride_b', None),
    (0x080414f8, 0x0201e2a0, 'gDuelCardCtxBase',         'id_zone_find_card_ctx_base',   None),
    (0x08041518, 0x0201bcc0, 'gDuelDisplaySeqState',     'id_zone_find_state_base_c',    None),
    (0x08041548, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'id_zone_find_step_lock_off',  None),
    # --- tick_spell_equip_zone_display_seq (0x0804154c) ---
    (0x0804162c, 0x0201bcc0, 'gDuelDisplaySeqState',     'spell_equip_state_base',       None),
    (0x08041630, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'spell_equip_player_stride',    None),
    (0x08041634, 0x0201c510, 'gDuelFieldSlots',          'spell_equip_field_slots_base', None),
    (0x08041638, 0x000010b1, 'SLOT_FACE_STATUS_ARRAY_OFF', 'spell_equip_face_status_off', None),
    (0x0804163c, 0x0201e2a0, 'gDuelCardCtxBase',         'spell_equip_card_ctx_base',    None),
    # PTR_gP1LifePoints_08041640: 0x0201c4e0 -- skip
    (0x08041644, 0x00001578, 'LAVA_GOLEM_CID',           'spell_equip_type_range_base',
     'LAVA_GOLEM_CID=0x1578: base of card_id range check [0x1578..0x1578+0xfa] in tick_spell_equip_zone_display_seq'),
    (0x0804169c, 0x0201e2a0, 'gDuelCardCtxBase',         'spell_equip_card_ctx_base_b',  None),
    (0x080416a0, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'spell_equip_player_stride_b',  None),
    (0x080416a4, 0x0201c510, 'gDuelFieldSlots',          'spell_equip_field_slots_base_b', None),
    (0x080416d8, 0x0201e2a0, 'gDuelCardCtxBase',         'spell_equip_card_ctx_base_c',  None),
    # PTR_gP1LifePoints_080416dc: 0x0201c4e0 -- skip
    (0x080416e0, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'spell_equip_player_stride_c',  None),
    (0x08041754, 0x0201e2a0, 'gDuelCardCtxBase',         'spell_equip_card_ctx_base_d',  None),
    # PTR_gP1LifePoints_08041758: 0x0201c4e0 -- skip
    (0x0804175c, 0x00000868, 'PLAYER_BLOCK_STRIDE',      'spell_equip_player_stride_d',  None),
    (0x08041760, 0x0201bcc0, 'gDuelDisplaySeqState',     'spell_equip_state_base_b',     None),
    (0x08041764, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'spell_equip_step_lock_off',   None),
    # --- tick_card_display_op28_clear_seq (0x08041768) ---
    (0x08041788, 0x0201bcc0, 'gDuelDisplaySeqState',     'op28_state_base',              None),
    (0x0804178c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'op28_step_lock_off',          None),
    # --- tick_card_display_op2b_lp_clear_seq (0x08041790) ---
    (0x080417d8, 0x0201bcc0, 'gDuelDisplaySeqState',     'op2b_state_base',              None),
    # PTR_gP1LifePoints_080417dc: 0x0201c4e0 -- skip
    (0x080417e0, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',   'op2b_lp_track_base_off',
     'gP1LifePoints+0x1da8: LP card-ref tracking array base; cleared by tick_card_display_op2b_lp_clear_seq'),
    (0x080417e4, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',   'op2b_lp_track_next_off',
     'gP1LifePoints+0x1daa: 5-entry hword clear loop base (+0/+2/+4/+6/+8)'),
    (0x080417e8, 0x00001db2, 'LP_CARD_TRACK_AUX_OFF',    'op2b_lp_track_aux_off',
     'gP1LifePoints+0x1db2: auxiliary LP track clear field (1 ROM ref)'),
    (0x080417ec, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'op2b_step_lock_off',          None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none (0 new REF actions; PTR_ slots already symbolized)
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: none (all non-PTR slots handled in EQ_SLOTS above)
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_token, new_token)
#    Substring replace in existing plate comment. Pure ASCII only.
#    18 functions: 17 with FUN_0803be4c, 1 with bare (0x0803be4c).
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # clear_display_step_lock_b (0x08040c88): FUN_0803be4c
    (0x08040c88, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_c (0x08040c9c): FUN_0803be4c
    (0x08040c9c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_d (0x08040cb0): FUN_0803be4c
    (0x08040cb0, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_e (0x08040cc4): FUN_0803be4c
    (0x08040cc4, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_f (0x08040cd8): FUN_0803be4c
    (0x08040cd8, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_g (0x08040cec): FUN_0803be4c
    (0x08040cec, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_h (0x08040d00): FUN_0803be4c
    (0x08040d00, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_card_display_state_flag (0x08040d14): FUN_0803be4c
    (0x08040d14, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_zone_slot_spell_remove_display_seq (0x08040d28): FUN_0803be4c
    (0x08040d28, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_field_clear_display_sequence (0x08040e54): FUN_0803be4c
    (0x08040e54, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_player_hand_shuffle_display_seq (0x08040ebc): FUN_0803be4c
    (0x08040ebc, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_lp_change_cycle_display_seq (0x08040f5c): FUN_0803be4c
    (0x08040f5c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_change_position_display_state (0x08041044): (0x0803be4c) bare address form
    (0x08041044, '(0x0803be4c)', '(dispatch_duel_event_display_seq)'),
    # tick_zone_card_place_by_id_seq (0x080410c4): FUN_0803be4c
    (0x080410c4, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_id_zone_find_display_seq (0x08041330): FUN_0803be4c
    (0x08041330, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_spell_equip_zone_display_seq (0x0804154c): FUN_0803be4c
    (0x0804154c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_op28_clear_seq (0x08041768): FUN_0803be4c
    (0x08041768, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_op2b_lp_clear_seq (0x08041790): FUN_0803be4c
    (0x08041790, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
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
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
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
    print("=== RefineF04Seg3Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-3: 0x08040c88..0x080417f0, 19 fn, 98 slots")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
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
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1
    print("  PLATE done: %d" % plate_ok)

    print("\n=== RefineF04Seg3Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d (DRY=%s)" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), DRY))


main()
