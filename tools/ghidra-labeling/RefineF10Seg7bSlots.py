# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg7bSlots.py -- f10 Seg-7b (0x08081900..0x08082290)
#   12 named functions (tick_equip_activation_display_3state thru
#   tick_equip_activation_display_with_card_routing)
#
# C13: 55 total auto-name slots (excl PTR_gP1LifePoints + DWORD_gP1LifePoints + DAT_08082158)
#   EQ=42, RENAME=6, PTR_skip=7 (5 PTR_gP1LifePoints + 2 DWORD_gP1LifePoints), carve=0
#
# NEW constants (added to card_info.inc before running this script):
#   LEVEL_UP_CID=0x17f5, INFERNO_RECKLESS_SUMMON_CID=0x198e, GUARDIAN_ELMA_CID=0x164a
#
# PLATE: 13 mojibake->ASCII + 1 C8 (FUN_08081900->tick_equip_activation_display_3state)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

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
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values ROM-verified via C4 python struct.unpack.
#    PTR_gP1LifePoints_* and DWORD_gP1LifePoints_d2c/d98 are skipped (shared global).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== REUSE: gDuelPhaseFlags=0x0201b290 (ewram.inc) x15 =====
    # Note: DWORD_08081d2c and DWORD_08081d98 = 0x0201c4e0 = gP1LifePoints -> PTR_skip
    (0x0808191c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_3state_phase_flags_91c'),
    (0x08081bb8, 0x0201b290, 'gDuelPhaseFlags', 'tick_slot_3state_phase_flags_bb8'),
    (0x08081d04, 0x0201b290, 'gDuelPhaseFlags', 'tick_effect_slot_phase_flags_d04'),
    (0x08081d58, 0x0201b290, 'gDuelPhaseFlags', 'tick_5state_phase_flags_d58'),
    (0x08081e30, 0x0201b290, 'gDuelPhaseFlags', 'tick_5state_phase_flags_e30'),
    (0x08081e64, 0x0201b290, 'gDuelPhaseFlags', 'switchd_case_phase_flags_e64'),
    (0x08081e94, 0x0201b290, 'gDuelPhaseFlags', 'switchd_case1_phase_flags_e94'),
    (0x08081ec4, 0x0201b290, 'gDuelPhaseFlags', 'switchd_case3_phase_flags_ec4'),
    (0x08081f04, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_routing_phase_flags_f04'),
    (0x08081f1c, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_routing_phase_flags_f1c'),
    (0x08081f48, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_routing_phase_flags_f48'),
    (0x08081fdc, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_routing_phase_flags_fdc'),
    (0x08082020, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_routing_phase_flags_020'),
    (0x08082038, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_routing_phase_flags_038'),
    (0x08081ca8, 0x0201b290, 'gDuelPhaseFlags', 'dispatch_type_flag_phase_flags_ca8'),

    # ===== REUSE: gDuelCardCtxBase=0x0201e2a0 (ewram.inc) x3 =====
    (0x080819b8, 0x0201e2a0, 'gDuelCardCtxBase', 'dispatch_confirm_card_ctx_9b8'),
    (0x08081c84, 0x0201e2a0, 'gDuelCardCtxBase', 'dispatch_type_card_ctx_c84'),
    (0x08081d28, 0x0201e2a0, 'gDuelCardCtxBase', 'push_player_card_ctx_d28'),

    # ===== REUSE: PLAYER_BLOCK_STRIDE=0x868 (duel_field.inc) x1 =====
    (0x08081b70, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_slot_3state_stride_b70'),

    # ===== REUSE: gDuelFieldSlots=0x0201c510 (duel_field.inc) x1 =====
    (0x08081b74, 0x0201c510, 'gDuelFieldSlots', 'tick_slot_3state_dfs_b74'),

    # ===== REUSE: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff (duel_field.inc) x1 =====
    (0x08081bf4, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR', 'tick_slot_3state_attr_clear_bf4'),

    # ===== REUSE: ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc) x3 =====
    (0x08081978, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_3state_sprite_off_978'),
    (0x08081f00, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_card_routing_sprite_off_f00'),
    (0x08082018, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_card_routing_sprite_off_018'),

    # ===== REUSE: ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc) x1 =====
    (0x0808201c, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'tick_card_routing_anim_off_01c'),

    # ===== REUSE: TRIGGER_OP_PARAM_10D3=0x10d3 (duel_field.inc) x2 =====
    (0x08081c88, 0x000010d3, 'TRIGGER_OP_PARAM_10D3', 'dispatch_type_op_param_c88'),
    (0x08081cd0, 0x000010d3, 'TRIGGER_OP_PARAM_10D3', 'tick_effect_slot_op_param_cd0'),

    # ===== REUSE: lookup_equip_score_mooyan_p0=0x197 (duel_field.inc) x1 =====
    (0x08081d54, 0x00000197, 'lookup_equip_score_mooyan_p0', 'tick_effect_slot_score_param_d54'),

    # ===== REUSE: gEquipChainSlotRefs=0x0201bb90 (duel_field.inc) x1 =====
    (0x08081de0, 0x0201bb90, 'gEquipChainSlotRefs', 'enqueue_equip_slot_chain_refs_de0'),

    # ===== NEW: LEVEL_UP_CID=0x17f5 (card_info.inc) x1 =====
    (0x08081a00, 0x000017f5, 'LEVEL_UP_CID', 'lookup_bst_level_up_cid_a00'),

    # ===== REUSE: PANDEMONIUM_CID=0x169f (card_info.inc) x1 =====
    (0x08081a04, 0x0000169f, 'PANDEMONIUM_CID', 'lookup_bst_pandemonium_cid_a04'),

    # ===== REUSE: INSECT_IMITATION_CID=0x140b (card_info.inc) x1 =====
    (0x08081a08, 0x0000140b, 'INSECT_IMITATION_CID', 'lookup_bst_insect_imitation_cid_a08'),

    # ===== NEW: GUARDIAN_ELMA_CID=0x164a (card_info.inc) x1 =====
    (0x08081a10, 0x0000164a, 'GUARDIAN_ELMA_CID', 'lookup_bst_guardian_elma_cid_a10'),

    # ===== REUSE: THE_KICK_MAN_CID=0x1745 (card_info.inc) x1 =====
    (0x08081a28, 0x00001745, 'THE_KICK_MAN_CID', 'lookup_bst_kick_man_cid_a28'),

    # ===== REUSE: NINJITSU_ART_OF_TRANSFORMATION_CID=0x1768 (card_info.inc) x1 =====
    (0x08081a3c, 0x00001768, 'NINJITSU_ART_OF_TRANSFORMATION_CID', 'lookup_bst_ninjitsu_transform_cid_a3c'),

    # ===== NEW: INFERNO_RECKLESS_SUMMON_CID=0x198e (card_info.inc) x1 =====
    (0x08081a5c, 0x0000198e, 'INFERNO_RECKLESS_SUMMON_CID', 'lookup_bst_inferno_reckless_cid_a5c'),

    # ===== REUSE: SPIRITUAL_EARTH_ART_CID=0x1927 (card_info.inc) x1 =====
    (0x08081a70, 0x00001927, 'SPIRITUAL_EARTH_ART_CID', 'lookup_bst_spiritual_earth_art_cid_a70'),

    # ===== REUSE: TRIAL_OF_THE_PRINCESSES_CID=0x19d8 (card_info.inc) x1 =====
    (0x08081a88, 0x000019d8, 'TRIAL_OF_THE_PRINCESSES_CID', 'lookup_bst_trial_princesses_cid_a88'),

    # ===== REUSE: GENERATION_SHIFT_CID=0x19dd (card_info.inc) x1 =====
    (0x08081a9c, 0x000019dd, 'GENERATION_SHIFT_CID', 'lookup_bst_generation_shift_cid_a9c'),

    # ===== REUSE: NOBLEMAN_EATER_BUG_CID=0x17ea (card_info.inc) x1 =====
    (0x08081f7c, 0x000017ea, 'NOBLEMAN_EATER_BUG_CID', 'tick_routing_nobleman_eater_cid_f7c'),

    # ===== REUSE: GREENKAPPA_CID=0x11f0 (card_info.inc) x1 =====
    (0x08081f80, 0x000011f0, 'GREENKAPPA_CID', 'tick_routing_greenkappa_cid_f80'),

    # ===== REUSE: XING_ZHEN_HU_CID=0x184a (card_info.inc) x1 =====
    (0x08081f8c, 0x0000184a, 'XING_ZHEN_HU_CID', 'tick_routing_xing_zhen_hu_cid_f8c'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, new_label, eol_comment)
#    THUMB fn-ptr slots (value+1) and switchD table ptr.
#    No equate, just label rename + EOL comment.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # ===== THUMB fn-ptr renames (value = fn_addr+1) =====
    (0x08081948, 'tick_equip_act_3state_mode_alt_ptr',
     'set_equip_activation_state_by_mode_alt+1 (THUMB fn-ptr)'),
    (0x08081cd4, 'disp_by_type_mode_alt_ptr',
     'set_equip_activation_state_by_mode_alt+1 (THUMB fn-ptr)'),
    (0x08081e90, 'effect_node_handler_slot_check_ptr_a',
     'check_effect_node_handler_for_slot+1 (THUMB fn-ptr)'),
    (0x08081ec0, 'effect_node_handler_slot_check_ptr_b',
     'check_effect_node_handler_for_slot+1 (THUMB fn-ptr)'),
    (0x08081fd8, 'effect_node_handler_slot_check_ptr_c',
     'check_effect_node_handler_for_slot+1 (THUMB fn-ptr)'),
    # ===== switchD table pointer =====
    (0x08081e34, 'tick_equip_5state_switch_table_ptr',
     'ptr to switchdataD_08081e38 (5-entry jump table)'),
]

# ---------------------------------------------------------------------------
# C. CJK_PLATE_REWRITES: full ASCII plate replacement for 13 mojibake functions
#    All text pure ASCII. WARN/not-found = FAIL.
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # 1. dispatch_equip_activation_display_by_confirm_state (0x0808198c) -- L16867
    (0x0808198c,
     "@ Equip activation display routing hub (indeg=8). Called by 8 callers "
     "(0x080833a8/0x0808416c/0x08084180/0x08084460/0x08084594/0x08084d08/0x08084e2c/0x080852e4, "
     "all equip/activation routing layer). Receives card_entry_ptr(r0) and secondary_ptr(r1). "
     "Reads gActivationConfirmTable(0x0201e2a0)+[player_id*4+8] confirm_flag; if==1 calls "
     "select_equip_target_slot_by_effect_strategy; else calls tick_equip_activation_display_3state. "
     "Exit pop {r1};bx r1 Sub-case E."),

    # 2. tick_equip_slot_display_by_card_id_3state (0x08081b84) -- L17147
    (0x08081b84,
     "@ Equip slot display 3-state machine, dispatches by card_id. Receives effect_node_ptr(r0). "
     "Calls lookup_slot_display_value_by_card_id for card_id display value. "
     "Reads state from [IWRAM_BASE+0x4b0]. "
     "State 0: calls dispatch_effect_handler_by_card_id; if handler returns nonzero calls "
     "trigger_card_display_op31_if_not_active then advances +1 returns 0 (in-progress); "
     "if 0 and flag not set returns -1. "
     "State 1: trigger_card_display_op31_if_not_active + init_effect_slot_display_context "
     "then advances +1 returns 0. "
     "State 2: pack_equip_slot_sprite_with_code_attr then returns 1 (done). "
     "Other states: returns 1."),

    # 3. dispatch_equip_display_by_type_flag_and_node_activity (0x08081c54) -- L17258
    (0x08081c54,
     "@ Equip display routing fn (indeg=4). Called by "
     "0x08083c98/0x080843fc/0x08084674/0x08084d3c. "
     "Reads card_entry[+3] bits[5:4]: if==0x20 (direct type flag) returns 1 directly; "
     "if confirm_flag==1 calls select_equip_target_slot_by_effect_strategy(strategy=0x10d3); "
     "else by count_effect_node_zone_activations result: nonzero -> "
     "trigger_card_display_op31_if_not_active(op=0x65) + set_equip_activation_state_by_mode; "
     "zero -> tick_equip_activation_display_3state. "
     "Exit pop {r1};bx r1 Sub-case E."),

    # 4. enqueue_equip_slot_sprite_from_base_offset (0x08081dcc) -- L17459+17462+17463+17464
    (0x08081dcc,
     "@ Small equip sprite enqueue fn. Receives effect_node_ptr(r0). "
     "Reads from fixed base [0x0201bb90]+0 and [0x0201bb90]+0x1c as two params, "
     "then calls enqueue_equip_slot_sprite_with_code_rotation to enqueue sprite rotation attr. "
     "Always returns 1.\n"
     "@ Constants: BASE_PTR=0x0201bb90 (gEquipChainSlotRefs), OFFSET_A=0x0, OFFSET_B=0x1c"),

    # 5. check_effect_node_handler_for_slot (0x08081de4) -- L17478
    (0x08081de4,
     "@ Effect node dual-check predicate, referenced by multiple fn-ptr tables. "
     "Receives effect_node_ptr(r0). "
     "First calls invoke_effect_node_handler_3arg to invoke node 3-arg handler; "
     "if nonzero calls find_effect_slot_by_side_and_type to find matching slot; "
     "if found returns 0. "
     "If handler returns 0 and no matching slot, returns 1. "
     "Return 0 means active condition holds; return 1 means condition not met. "
     "fn-ptr addr 0x08081de5 loaded into fn-ptr tables by 5 callers."),

    # 6. tick_equip_activation_display_5state (0x08081e10) -- L17503+17508+17509
    (0x08081e10,
     "@ Equip activation display 5-state machine. Receives effect_node_ptr(r0). "
     "Reads state from [IWRAM_BASE+0x4b0]. "
     "State 0: count_effect_node_zone_activations; "
     "State 1: trigger_card_display_op31_if_not_active(op=0x94)+set_equip_activation_state_by_mode, "
     "advance +1, return 0; "
     "State 2: check_activation_display_state_is_confirmed, if confirmed "
     "enqueue_equip_slot_sprite_with_code_rotation and advance +1; "
     "State 3: trigger_card_display_op31_if_not_active(op=0x6a)+set_equip_activation_state_by_mode, "
     "advance +1, return 0; "
     "Default(>=4): advance +1 returns 1. "
     "Extension of tick_equip_activation_display_3state (0x08081900) with 2 extra states.\n"
     "@ Constants: IWRAM_BASE=0x0201b290, STATE_OFFSET=0x4b0 (0x96*8)\n"
     "@ OP_CODE_A=0x94 (state 1), OP_CODE_B=0x6a (state 3)"),

    # 7. tick_equip_activation_display_with_card_routing (0x08081f28) -- L17651+17658
    (0x08081f28,
     "@ Equip activation display 4-state machine with card_id routing. "
     "Receives effect_node_ptr(r0). Reads [IWRAM_BASE+0x4b0] state. "
     "State 0: count_effect_node_zone_activations; "
     "if card_id==0x17ea (Nobleman-Eater Bug) or 0x184a (Xing Zhen Hu) calls "
     "format_game_text_with_int_arg then trigger; "
     "if card_id==0x11f0 (Greenkappa) calls format_game_text_with_int_arg(slot=0x71); "
     "else direct trigger+set_equip_activation_state_by_mode_alt. "
     "States 2/3: check_activation_display_state_is_confirmed -> "
     "enqueue_equip_slot_sprite_with_code_rotation, advance +1. "
     "Exit pop {r1};bx r1 Sub-case E.\n"
     "@ Constants: IWRAM_BASE=0x0201b290, STATE_OFFSET=0x4b0, "
     "CARD_ID_A=0x17ea (Nobleman-Eater Bug), CARD_ID_B=0x11f0 (Greenkappa), "
     "CARD_ID_C=0x184a (Xing Zhen Hu), FORMAT_TEXT_SLOT=0x9b"),

    # 8. tick_equip_activation_display_3state (0x08081900) -- check if also mojibake
    # (plate at L16791-16793 -- has CJK as well, check below)
    # Actually from asm L16791-16793 those look like ASCII comments; check proposal --
    # proposal lists only the 7 functions above as mojibake. L16867 = 0x0808198c.
    # BUT the proposal also lists these additional mojibake entries:
    # L17462/17463/17464 (consolidated into enqueue_equip_slot_sprite_from_base_offset above),
    # L17508/17509 (consolidated into tick_equip_activation_display_5state above),
    # L17658 (consolidated into tick_equip_activation_display_with_card_routing above).
    # The 7 unique function addresses cover all 13 mojibake plate lines.
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: C8 stale FUN_ substitution
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # lookup_slot_display_value_by_card_id (0x080819cc) L16902:
    #   "Called by FUN_08081900 ..." -> "tick_equip_activation_display_3state"
    (0x080819cc, 'FUN_08081900', 'tick_equip_activation_display_3state'),
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

def _apply_eq(slot_addr, value, eq_name, slot_label):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%08x  label=%s" % (
            slot_addr, eq_name, value & 0xFFFFFFFF, slot_label))
        return True

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True

def _apply_rename(slot_addr, slot_label, eol_comment=None):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s  eol='%s'" % (slot_addr, slot_label, eol_comment or ''))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol_comment:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            existing_eol = cu.getComment(CodeUnit.EOL_COMMENT)
            if not existing_eol or eol_comment not in existing_eol:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_comment)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_cjk_plate(func_addr, new_plate_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] cjk_plate 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] CJK_PLATE 0x%08x: rewrite to ASCII (%d chars)" % (func_addr, len(new_plate_text)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    # Verify no non-ASCII in new text
    has_nonascii = any(ord(c) > 0x7f for c in new_plate_text)
    print("[PLT] 0x%08x: plate replaced (len=%d, nonASCII=%s)" % (
        func_addr, len(new_plate_text), has_nonascii))

def _apply_plate_fix(func_addr, old_text, new_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[FAIL] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[FAIL] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
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
    print("=== RefineF10Seg7bSlots (DRY=%s) ===" % DRY)
    print("  Seg-7b: 0x08081900..0x08082290, 12 fn, 55 slots (EQ42 RENAME6 PTR_skip7)")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d entries) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_skip = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        ok = _apply_eq(slot_addr, value, eq_name, slot_label)
        if ok:
            eq_ok += 1
        else:
            eq_skip += 1
    print("  EQ done: %d  fail/skip: %d" % (eq_ok, eq_skip))

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d entries) ---" % len(RENAME_SLOTS))
    for slot_addr, slot_label, eol in RENAME_SLOTS:
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # C. CJK_PLATE_REWRITES
    print("\n--- C. CJK_PLATE_REWRITES: mojibake->ASCII (%d functions) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    # D. PLATE_REWRITES (C8 stale FUN_)
    print("\n--- D. PLATE_REWRITES: FUN_ substitutions (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF10Seg7bSlots DONE ===")
    print("  EQ=%d  RENAME=%d  CJK_PLATE=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(CJK_PLATE_REWRITES), len(PLATE_REWRITES)))


main()
