# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg1Slots.py -- file 04 Seg-1 (0x0804020c..0x080407fc)
#   19 functions: tick_card_display_seq_op15 / tick_equip_preview_display_sequence /
#   tick_set_display_mode_seq / tick_lp_compare_init_display_seq /
#   invoke_card_display_op_by_equip_mode / invoke_card_display_op_equip_mode0..5 /
#   commit_display_index_on_effect5 / tick_display_slot_flag_clear_seq /
#   advance_card_display_seq_counter / set_slot_facedown_bit_by_flag /
#   apply_card_flags_to_zone_bitmap / commit_field_slot_bit_with_display_op24 /
#   tick_card_effect_category_display_seq / tick_display_op40_seq
#
# Sections:
#   A. EQ_SLOTS    -- 33 total (28 reuse + 5 new in duel_field.inc)
#   B. REF_SLOTS   -- 22 EWRAM global address references
#   C. RENAME_SLOTS -- 9 PTR_gP1LifePoints_* label renames
#   D. PLATE_REWRITES -- 17 FUN_ stale name substitutions
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).

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
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- duel_field.inc: DISPLAY_SEQ_STEP_LOCK_OFF = 0x0000080c (13 slots) ---
    (0x08040254, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_cdseq_op15_step_lock_off',
     'step lock offset 0x80c in gDuelDisplaySeqState'),
    (0x08040298, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_equip_preview_step_lock_off', None),
    (0x08040334, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_set_disp_mode_step_lock_off', None),
    (0x080403e4, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_lp_cmp_init_step_lock_off', None),
    (0x0804044c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'invoke_equip_mode_step_lock_off', None),
    (0x080404c0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'commit_disp_idx_e5_step_lock_off', None),
    (0x08040600, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_slot_flag_clear_step_lock_off', None),
    (0x08040630, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'adv_cdseq_ctr_step_lock_off', None),
    (0x08040694, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'set_slot_fd_bit_step_lock_off', None),
    (0x08040714, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'apply_card_flags_bitmap_step_lock_off', None),
    (0x08040748, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'commit_fslot_bit_disp24_step_lock_off', None),
    (0x080407b0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_card_effect_cat_step_lock_off', None),
    (0x080407f8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_disp_op40_step_lock_off', None),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 (1 slot) ---
    (0x080403cc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'tick_lp_cmp_init_lp_block2_off',
     'gP1LifePoints+0x1ce8: XOR flag at LP compare init'),

    # --- ewram.inc: P1LP_TIMER_OFF = 0x00001cec (1 slot) ---
    (0x080403d0, 0x00001cec, 'P1LP_TIMER_OFF',
     'tick_lp_cmp_init_lp_timer_off',
     'gP1LifePoints+0x1cec: timer field incremented at LP compare init'),

    # --- duel_field.inc: FIELD_STATE_OFF = 0x00001cf4 (2 slots) ---
    (0x080403d8, 0x00001cf4, 'FIELD_STATE_OFF',
     'tick_lp_cmp_init_field_state_off',
     'gP1LifePoints+0x1cf4: equip activation phase/field state code'),
    (0x08040424, 0x00001cf4, 'FIELD_STATE_OFF',
     'invoke_equip_mode_field_state_off', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (4 slots) ---
    (0x080403e0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_lp_cmp_init_player_stride',
     'player block stride 0x868 (P2 offset from P1)'),
    (0x080405d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_slot_flag_clear_player_stride', None),
    (0x0804070c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_card_flags_bitmap_player_stride_a', None),
    (0x080406cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_card_flags_bitmap_player_stride_b', None),

    # --- oam_attr.inc: OAM_ATTR0_HIDDEN = 0x0000ffff (1 slot) ---
    (0x080405d8, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'tick_slot_flag_clear_oam_attr0_hidden',
     'AND mask clears low-16 bits (OAM attr0 hidden pattern)'),

    # --- duel_field.inc: EFFECT_ZONE_BITMASK_OFF = 0x000010d0 (3 slots) ---
    (0x080405dc, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'tick_slot_flag_clear_effect_zone_bitmask_off',
     'gP1LifePoints+0x10d0: effect zone bitmask field'),
    (0x08040658, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'set_slot_fd_bit_effect_zone_bitmask_off', None),
    (0x0804068c, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'apply_card_flags_bitmap_effect_zone_bitmask_off', None),

    # --- ewram.inc: HAND_ARRAY_TO_COUNT_NEG_OFF = 0xfffffbfc (1 slot) ---
    (0x080405f0, 0xfffffbfc, 'HAND_ARRAY_TO_COUNT_NEG_OFF',
     'tick_slot_flag_clear_hand_neg_off',
     'negative offset: gP1HandSlotArray -> gP1HandCountBase'),

    # --- ewram.inc: ALT_HAND_ARRAY_TO_COUNT_NEG_OFF = 0xfffffa4c (1 slot) ---
    (0x080405fc, 0xfffffa4c, 'ALT_HAND_ARRAY_TO_COUNT_NEG_OFF',
     'tick_slot_flag_clear_alth_neg_off',
     'negative offset: gP1AltHandSlotArray -> gP1AltHandCountBase'),

    # --- duel_field.inc: ACTIVE_EFFECT_CATEGORY_OFF = 0x000010d8 (1 slot) ---
    (0x08040788, 0x000010d8, 'ACTIVE_EFFECT_CATEGORY_OFF',
     'tick_card_effect_cat_active_cat_off',
     'gP1LifePoints+0x10d8: active effect category field'),

    # --- duel_field.inc NEW: DISP_SET_VARIANT_OFF = 0x00001cfc (1 slot) ---
    (0x08040310, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'tick_set_disp_mode_variant_off',
     'gP1LifePoints+0x1cfc: display mode variant (1=A / 2=B)'),

    # --- duel_field.inc NEW: SET_DISPLAY_STATE_SLOT_OFF = 0x00000894 (1 slot) ---
    (0x08040314, 0x00000894, 'SET_DISPLAY_STATE_SLOT_OFF',
     'tick_set_disp_mode_state_slot_off',
     'gP1LifePoints+0x894: set-mode display state slot index'),

    # --- duel_field.inc NEW: EQUIP_MAIN_PHASE_OFF = 0x00001d18 (1 slot) ---
    (0x080403d4, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',
     'tick_lp_cmp_init_equip_phase_off',
     'gP1LifePoints+0x1d18: equip main-phase dispatch index; cleared at LP-compare init'),

    # --- duel_field.inc NEW: HAND_SLOT_FACE_ARRAY_OFF = 0x0000041a (1 slot) ---
    (0x080405e0, 0x0000041a, 'HAND_SLOT_FACE_ARRAY_OFF',
     'tick_slot_flag_clear_hand_face_off',
     'gP1LifePoints+0x41a = gP1HandSlotArray+2: face-status byte-2'),

    # --- duel_field.inc NEW: ALT_HAND_SLOT_FACE_ARRAY_OFF = 0x000005d2 (1 slot) ---
    (0x080405e4, 0x000005d2, 'ALT_HAND_SLOT_FACE_ARRAY_OFF',
     'tick_slot_flag_clear_alth_face_off',
     'gP1LifePoints+0x5d2 = gP1AltHandSlotArray+2: face-status byte-2 (alt hand)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gDuelDisplaySeqState (ewram.inc, 0x0201bcc0) -- 16 slots ---
    (0x08040228, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_cdseq_op15_state_base',
     'gDuelDisplaySeqState base ptr'),
    (0x0804027c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_equip_preview_state_base', None),
    (0x080402cc, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_set_disp_mode_state_base', None),
    (0x08040318, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_set_disp_mode_ctr_base', None),
    (0x080403c4, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_lp_cmp_init_state_base', None),
    (0x0804041c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'invoke_equip_mode_state_base', None),
    (0x080404bc, 0x0201bcc0, 'gDuelDisplaySeqState',
     'commit_disp_idx_e5_state_base', None),
    (0x080405cc, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_slot_flag_clear_state_base', None),
    (0x0804062c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'adv_cdseq_ctr_state_base', None),
    (0x08040650, 0x0201bcc0, 'gDuelDisplaySeqState',
     'set_slot_fd_bit_state_base', None),
    (0x08040690, 0x0201bcc0, 'gDuelDisplaySeqState',
     'set_slot_fd_bit_state_base_b', None),
    (0x080406c4, 0x0201bcc0, 'gDuelDisplaySeqState',
     'apply_card_flags_bitmap_state_base', None),
    (0x08040710, 0x0201bcc0, 'gDuelDisplaySeqState',
     'apply_card_flags_bitmap_state_base_b', None),
    (0x08040744, 0x0201bcc0, 'gDuelDisplaySeqState',
     'commit_fslot_bit_disp24_state_base', None),
    (0x08040780, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_card_effect_cat_state_base', None),
    (0x080407dc, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_disp_op40_state_base', None),

    # --- gDuelCardCtxBase (ewram.inc, 0x0201e2a0) -- 2 slots ---
    (0x080402d0, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_set_disp_mode_card_ctx', None),
    (0x080403dc, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_lp_cmp_init_card_ctx', None),

    # --- gP1HandCountBase (ewram.inc, 0x0201c4f4) -- 1 slot ---
    (0x080405e8, 0x0201c4f4, 'gP1HandCountBase',
     'tick_slot_flag_clear_hand_cnt', None),

    # --- gP1HandSlotArray (ewram.inc, 0x0201c8f8) -- 1 slot ---
    (0x080405ec, 0x0201c8f8, 'gP1HandSlotArray',
     'tick_slot_flag_clear_hand_arr', None),

    # --- gP1AltHandCountBase (ewram.inc, 0x0201c4fc) -- 1 slot ---
    (0x080405f4, 0x0201c4fc, 'gP1AltHandCountBase',
     'tick_slot_flag_clear_alth_cnt', None),

    # --- gP1AltHandSlotArray (ewram.inc, 0x0201cab0) -- 1 slot ---
    (0x080405f8, 0x0201cab0, 'gP1AltHandSlotArray',
     'tick_slot_flag_clear_alth_arr', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    PTR_gP1LifePoints_* already emit correct .word gP1LifePoints;
#    only the slot label is changed to a function-scoped name.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0804030c, 'tick_set_disp_mode_lp_base',
     'gP1LifePoints base ptr for tick_set_display_mode_seq'),
    (0x080403c8, 'tick_lp_cmp_init_lp_base',
     'gP1LifePoints base ptr for tick_lp_compare_init_display_seq'),
    (0x08040420, 'invoke_equip_mode_lp_base',
     'gP1LifePoints base ptr for invoke_card_display_op_by_equip_mode'),
    (0x080405d0, 'tick_slot_flag_clear_lp_base',
     'gP1LifePoints base ptr for tick_display_slot_flag_clear_seq'),
    (0x08040654, 'set_slot_fd_bit_lp_base',
     'gP1LifePoints base ptr for set_slot_facedown_bit_by_flag (pool a)'),
    (0x08040688, 'set_slot_fd_bit_lp_base_b',
     'gP1LifePoints base ptr for set_slot_facedown_bit_by_flag (pool b)'),
    (0x080406c8, 'apply_card_flags_bitmap_lp_base',
     'gP1LifePoints base ptr for apply_card_flags_to_zone_bitmap (pool a)'),
    (0x08040708, 'apply_card_flags_bitmap_lp_base_b',
     'gP1LifePoints base ptr for apply_card_flags_to_zone_bitmap (pool b)'),
    (0x08040784, 'tick_card_effect_cat_lp_base',
     'gP1LifePoints base ptr for tick_card_effect_category_display_seq'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_token, new_token)
#    Full substring replace in existing plate comment (WARN if not found).
#    All text pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # tick_card_display_seq_op15 (0x0804020c): 2 substitutions
    (0x0804020c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    (0x0804020c, 'FUN_08040a04', 'tick_card_display_seq_op3b'),
    # tick_equip_preview_display_sequence (0x08040258)
    (0x08040258, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_set_display_mode_seq (0x0804029c)
    (0x0804029c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_lp_compare_init_display_seq (0x08040338)
    (0x08040338, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # invoke_card_display_op_equip_mode0 (0x08040450)
    (0x08040450, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # invoke_card_display_op_equip_mode1 (0x0804045c)
    (0x0804045c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # invoke_card_display_op_equip_mode2 (0x08040468)
    (0x08040468, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # invoke_card_display_op_equip_mode3 (0x08040474)
    (0x08040474, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # invoke_card_display_op_equip_mode4 (0x08040480)
    (0x08040480, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # invoke_card_display_op_equip_mode5 (0x0804048c)
    (0x0804048c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # commit_display_index_on_effect5 (0x08040498)
    (0x08040498, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_display_slot_flag_clear_seq (0x080404c4)
    (0x080404c4, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # advance_card_display_seq_counter (0x08040604)
    (0x08040604, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # apply_card_flags_to_zone_bitmap (0x08040698)
    (0x08040698, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # commit_field_slot_bit_with_display_op24 (0x08040718)
    (0x08040718, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_effect_category_display_seq (0x0804074c)
    (0x0804074c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # NOTE: tick_display_op40_seq (0x080407b4) already uses correct name -- no update needed
    # NOTE: set_slot_facedown_bit_by_flag and advance_card_display_seq_counter use
    #       FUN_0803be4c (listed above as 0x08040604/0x08040698 respectively)
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
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
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

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

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
    print("=== RefineF04Seg1Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-1: 0x0804020c..0x080407fc, 19 fn, 64 slots")
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
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF04Seg1Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

main()
