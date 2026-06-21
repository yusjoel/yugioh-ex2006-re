# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg3Slots.py -- f10 Seg-3 (0x0807be2c..0x0807cd68)
#   19 functions; 68 residual slots: 52 EQ + 3 REF + 13 RENAME + 1 FUNC_RENAME + 1 PLATE
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (52 slots; 50 REUSE + 1 NEW LP_CARD_TRACK_ALT_OFF + 3 GAS expr)
#   B. RENAME_SLOTS -- plain rename (12 gP1LifePoints already-symbolic + 1 BLK2 base DAT_)
#   C. REF_SLOTS  -- USER label + DATA ref for fn-ptr (THUMB+1) slots (3)
#   D. FUNC_RENAME -- tick_equip_activation_display_state (drop __0807c388 suffix)
#   E. PLATE      -- tick_equip_activation_display_state plate substring replace
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii)
#    52 slots; 3 GAS expr slots use eq_name="" (handled specially below)
# ---------------------------------------------------------------------------
# GAS expression slots: .word gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF = 0x0201b734
# These 3 slots cannot be equated to a named constant (no standalone constant exists).
# We only apply slot_label (USER label) + EOL for these.
GAS_EXPR_SLOTS = [
    # (slot_addr, value, slot_label, eol_ascii)
    (0x0807bef0, 0x0201b734,
     'tick_lp_sign_flag_phase_counter',
     'gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF=0x0201b734: phase frame counter word'),
    (0x0807bf30, 0x0201b734,
     'tick_lp_sign_flag_phase_counter_b',
     'gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF=0x0201b734: phase frame counter word (dup B)'),
    (0x0807bf4c, 0x0201b734,
     'tick_lp_sign_flag_phase_counter_c',
     'gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF=0x0201b734: phase frame counter word (dup C)'),
]

EQ_SLOTS = [
    # --- tick_lp_sign_flag_display_seq ---
    (0x0807beec, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'tick_lp_sign_flag_type_select_off',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8: [gP1LifePoints+0x1ce8] LP block2 type select field'),
    # 0x0807bef0 is GAS_EXPR -- handled separately
    (0x0807bef4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_lp_sign_flag_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807bef8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_lp_sign_flag_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    # 0x0807bf30 is GAS_EXPR
    (0x0807bf34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_lp_sign_flag_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: dup B'),
    # 0x0807bf4c is GAS_EXPR

    # --- tick_equip_chain_dual_slot_activation_seq ---
    (0x0807bf84, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_chain_dual_slot_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807bfc0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_chain_dual_slot_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),
    (0x0807bfc8, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_chain_dual_slot_lp_track_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base'),

    # --- enqueue_sprite_attr_mode6_on_zone_count_hit ---
    (0x0807c084, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_chain_dual_slot_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in state-0x7f path'),

    # --- enqueue_sprite_attr_mode6_on_zone_count_hit (DAT_ slots) ---
    (0x0807c150, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_mode6_zone_count_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807c154, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_mode6_zone_count_slots_base',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- enqueue_equip_sprite_type11_by_equip_flag ---
    (0x0807c1a4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'enqueue_equip_sprite_type11_type_sel_off',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8: LP block2 type select field'),

    # --- tick_zone_activation_lp_indicator_seq ---
    (0x0807c1e4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_zone_act_lp_indicator_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),

    # --- tick_equip_zone_sprite_activation_by_node ---
    (0x0807c214, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_sprite_act_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807c250, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_zone_sprite_act_ctx_base',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x0807c2c0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_sprite_act_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: equip phase frame slot'),
    (0x0807c2c8, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'tick_equip_zone_sprite_act_banisher_off',
     'LP_BANISHER_CTX_OFF=0x1d70: [gP1LifePoints+0x1d70] LP banisher context offset'),
    (0x0807c2cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_sprite_act_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807c320, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_zone_sprite_act_lp_track_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base'),
    (0x0807c324, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_sprite_act_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: dup B'),
    (0x0807c328, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_sprite_act_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup B'),
    (0x0807c380, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_sprite_act_frame_off_c',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup C'),
    (0x0807c384, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_sprite_act_player_stride_c',
     'PLAYER_BLOCK_STRIDE=0x868: dup C'),

    # --- tick_equip_activation_display_state__0807c388 ---
    (0x0807c3a8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_display_state_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807c3e4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_display_state_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: equip phase frame slot'),
    (0x0807c454, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'tick_equip_act_display_state_eligib_off',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68: [gP1LifePoints+0x1d68] eligibility sprite ctrl field'),
    (0x0807c458, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_display_state_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup B'),

    # --- tick_equip_lp_bar_display_two_step ---
    (0x0807c49c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_bar_two_step_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807c4d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_lp_bar_two_step_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),

    # --- tick_equip_activation_zone_scan_2state ---
    (0x0807c5ac, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_zone_scan_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),

    # --- apply_equip_slot_node_activation_on_zone_match ---
    (0x0807c748, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_equip_slot_node_act_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807c74c, 0x0201c510, 'gDuelFieldSlots',
     'apply_equip_slot_node_act_slots_base',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- dispatch_equip_oam_by_zone_type_and_eligibility (DAT_ slots) ---
    (0x0807c7b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_oam_zone_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807c7b4, 0x0201c600, 'gP1FieldArrayCBase',
     'dispatch_equip_oam_zone_field_array_c',
     'gP1FieldArrayCBase=0x0201c600: P1 field array C zone slot array base'),

    # --- dispatch_equip_slot_update_by_type_gate ---
    (0x0807c854, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_slot_update_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807c858, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_slot_update_slots_base',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- tick_equip_spell_zone_placement_scan ---
    (0x0807caa8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_spell_zone_scan_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807cb44, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_spell_zone_scan_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),

    # --- tick_equip_activation_face_down_display_seq ---
    (0x0807cb9c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_face_down_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807cbcc, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_face_down_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: equip phase frame slot'),
    (0x0807cc0c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_act_face_down_lp_track_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base'),
    (0x0807cc10, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_act_face_down_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup B'),

    # --- tick_equip_lp_type18_display_seq ---
    (0x0807cc58, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_type18_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807cc98, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_lp_type18_lp_track_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: LP card tracking base'),
    (0x0807cc9c, 0x00001dac, 'LP_CARD_TRACK_ALT_OFF',
     'tick_equip_lp_type18_lp_track_alt_off',
     'LP_CARD_TRACK_ALT_OFF=0x1dac: [gP1LifePoints+0x1dac] LP card-track array alt word (+4 from base)'),

    # --- tick_banisher_equip_zone_sprite_dispatch ---
    (0x0807cce0, 0x0201b290, 'gDuelPhaseFlags',
     'tick_banisher_zone_sprite_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807cce8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_banisher_zone_sprite_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807cd1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_banisher_zone_sprite_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: dup B'),
    (0x0807cd20, 0x0201c600, 'gP1FieldArrayCBase',
     'tick_banisher_zone_sprite_field_array_c',
     'gP1FieldArrayCBase=0x0201c600: P1 field array C base'),
    (0x0807cd24, 0x00001c88, 'EQUIP_CHAIN_BASE_OFF',
     'tick_banisher_zone_sprite_chain_base_off',
     'EQUIP_CHAIN_BASE_OFF=0x1c88: [gP1FieldArrayCBase+0x1c88] equip chain base offset'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii)
#    12 gP1LifePoints already-symbolic slots + 1 BLK2 base DAT_
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0807bee8, 'tick_lp_sign_flag_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_lp_sign_flag_display_seq path A)'),
    (0x0807bf38, 'tick_lp_sign_flag_lp_base_b',
     '.word gP1LifePoints: LP state struct base (tick_lp_sign_flag_display_seq path B)'),
    (0x0807bfc4, 'tick_equip_chain_dual_slot_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_chain_dual_slot_activation_seq)'),
    (0x0807c1a0, 'enqueue_equip_sprite_type11_lp_base',
     '.word gP1LifePoints: LP state struct base (enqueue_equip_sprite_type11_by_equip_flag)'),
    (0x0807c2c4, 'tick_equip_zone_sprite_act_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_zone_sprite_activation_by_node path A)'),
    (0x0807c31c, 'tick_equip_zone_sprite_act_lp_base_b',
     '.word gP1LifePoints: LP state struct base (tick_equip_zone_sprite_activation_by_node path B)'),
    (0x0807c450, 'tick_equip_act_display_state_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_activation_display_state__0807c388)'),
    (0x0807c4d0, 'tick_equip_lp_bar_two_step_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_lp_bar_display_two_step)'),
    (0x0807cb40, 'tick_equip_spell_zone_scan_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_spell_zone_placement_scan)'),
    (0x0807cc08, 'tick_equip_act_face_down_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_activation_face_down_display_seq)'),
    (0x0807cc94, 'tick_equip_lp_type18_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_lp_type18_display_seq)'),
    (0x0807cce4, 'tick_banisher_zone_sprite_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_banisher_equip_zone_sprite_dispatch)'),
    # BLK2 base label (will be replaced by disasm)
    (0x0807c92c, 'des_frog_dispatch_stubs',
     'BLK2 R4 disasm base: Des Frog dispatch sub-stubs A..I (0x158 bytes, 9 unique entries)'),
]

# ---------------------------------------------------------------------------
# C. REF_SLOTS: (slot_addr, target_addr, fn_name, slot_label, eol_ascii)
#    fn-ptr THUMB+1 slots: set USER label + DATA ref
#    NOTE: target_addr is fn base (even), +1 THUMB handled via setComment
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0807c254, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_equip_zone_sprite_act_zone_handler_fn',
     'fn-ptr check_equip_activation_at_slot11+1 (THUMB+1=0x08065991)'),
    (0x0807c26c, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_equip_zone_sprite_act_zone_handler_fn_b',
     'fn-ptr check_equip_activation_at_slot11+1 dup (THUMB+1=0x08065991)'),
    (0x0807c408, 0x08090624, 'invoke_effect_node_with_active_flag_3arg',
     'tick_equip_act_display_state_effect_node_fn',
     'fn-ptr invoke_effect_node_with_active_flag_3arg+1 (THUMB+1=0x08090625)'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: (fn_addr, old_name, new_name)
# ---------------------------------------------------------------------------
FUNC_RENAME = [
    (0x0807c388,
     'tick_equip_activation_display_state__0807c388',
     'tick_equip_activation_display_state'),
]

# ---------------------------------------------------------------------------
# E. PLATE: (fn_addr, old_substr, new_substr)
#    Substring replace in plate comment to match FUNC_RENAME
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    (0x0807c388,
     'tick_equip_activation_display_state__0807c388',
     'tick_equip_activation_display_state'),
]


# ===========================================================================
# Helpers
# ===========================================================================

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data at 0x%08x" % slot_int
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch at 0x%08x: got=0x%x want=0x%x" % (slot_int, iv, want)
    return True, None


def main():
    print("=== RefineF10Seg3Slots (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    rf = currentProgram.getReferenceManager()
    nA = nB = nC = nD = nE = 0
    fail_count = 0

    # -----------------------------------------------------------------------
    # A. EQ_SLOTS
    # -----------------------------------------------------------------------
    print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for (slot_int, value, eq_name, slot_label, eol_text) in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[FAIL] EQ 0x%08x %s: %s" % (slot_int, eq_name, err))
            fail_count += 1
            continue
        if not DRY:
            # Create or get equate
            eq = et.getEquate(eq_name)
            if eq is None:
                eq = et.createEquate(eq_name, value & 0xffffffff)
            slot_a = _addr(slot_int)
            eq.addReference(slot_a, 0)
            # Slot label
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            # EOL comment
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[EQ ok] 0x%08x %s -> %s" % (slot_int, eq_name, slot_label))
        nA += 1

    # -----------------------------------------------------------------------
    # A2. GAS_EXPR_SLOTS (value check + label + EOL only; no equate)
    # -----------------------------------------------------------------------
    print("--- A2. GAS_EXPR_SLOTS (%d) ---" % len(GAS_EXPR_SLOTS))
    for (slot_int, value, slot_label, eol_text) in GAS_EXPR_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[FAIL] GAS_EXPR 0x%08x: %s" % (slot_int, err))
            fail_count += 1
            continue
        if not DRY:
            slot_a = _addr(slot_int)
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[GAS_EXPR ok] 0x%08x -> %s" % (slot_int, slot_label))
        nA += 1

    # -----------------------------------------------------------------------
    # B. RENAME_SLOTS
    # -----------------------------------------------------------------------
    print("--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for (slot_int, slot_label, eol_text) in RENAME_SLOTS:
        if not DRY:
            slot_a = _addr(slot_int)
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[RENAME ok] 0x%08x -> %s" % (slot_int, slot_label))
        nB += 1

    # -----------------------------------------------------------------------
    # C. REF_SLOTS
    # -----------------------------------------------------------------------
    print("--- C. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for (slot_int, target_int, fn_name, slot_label, eol_text) in REF_SLOTS:
        # Value check: THUMB+1 (target+1)
        ok, err = _check(slot_int, target_int + 1)
        if not ok:
            print("[FAIL] REF 0x%08x %s: %s" % (slot_int, fn_name, err))
            fail_count += 1
            continue
        if not DRY:
            slot_a = _addr(slot_int)
            target_a = _addr(target_int)
            # Label on target (gas label for fn)
            sm.createLabel(target_a, fn_name, SourceType.USER_DEFINED)
            # DATA ref from slot to target
            rf.addMemoryReference(slot_a, target_a, RefType.DATA, SourceType.USER_DEFINED, 0)
            # Set primary
            for ref in rf.getReferencesFrom(slot_a):
                if ref.getToAddress().equals(target_a):
                    rf.setPrimary(ref, True)
                    break
            # Slot label
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            # EOL comment
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[REF ok] 0x%08x -> %s (+1 THUMB) slot=%s" % (slot_int, fn_name, slot_label))
        nC += 1

    # -----------------------------------------------------------------------
    # D. FUNC_RENAME
    # -----------------------------------------------------------------------
    print("--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAME))
    fm = currentProgram.getFunctionManager()
    for (fn_addr, old_name, new_name) in FUNC_RENAME:
        fn = fm.getFunctionAt(_addr(fn_addr))
        if fn is None:
            print("[FAIL] FUNC_RENAME 0x%08x: no function found" % fn_addr)
            fail_count += 1
            continue
        actual = fn.getName()
        if actual != old_name:
            print("[WARN] FUNC_RENAME 0x%08x: name is '%s' (expected '%s'); proceeding anyway" % (fn_addr, actual, old_name))
        if not DRY:
            fn.setName(new_name, SourceType.USER_DEFINED)
        print("[FUNC_RENAME ok] 0x%08x: %s -> %s" % (fn_addr, actual, new_name))
        nD += 1

    # -----------------------------------------------------------------------
    # E. PLATE (substring replace)
    # -----------------------------------------------------------------------
    print("--- E. PLATE (%d) ---" % len(PLATE_SUBS))
    for (fn_addr, old_substr, new_substr) in PLATE_SUBS:
        fn_a = _addr(fn_addr)
        cu = listing.getCodeUnitAt(fn_a)
        if cu is None:
            print("[WARN] PLATE 0x%08x: no code unit found" % fn_addr)
            continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[WARN] PLATE 0x%08x: no plate comment; skipping" % fn_addr)
            continue
        if old_substr not in plate:
            # Already replaced (e.g. function was renamed in a prior session) -- treat as ok
            print("[PLATE skip] 0x%08x: substring '%s' not found (already applied or plate clean)" % (fn_addr, old_substr))
            nE += 1
            continue
        new_plate = plate.replace(old_substr, new_substr)
        if not DRY:
            cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[PLATE ok] 0x%08x: replaced '%s' -> '%s'" % (fn_addr, old_substr, new_substr))
        nE += 1

    print("")
    print("=== SUMMARY: EQ=%d RENAME=%d REF=%d FUNC_RENAME=%d PLATE=%d FAIL=%d ===" % (
        nA, nB, nC, nD, nE, fail_count))
    if fail_count > 0:
        print("[ERROR] %d slot(s) FAILED -- see FAIL lines above" % fail_count)
    else:
        print("[OK] All slots applied successfully")


main()
