# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg8aSlots.py -- f10 Seg-8a slot symbolization [0x08082290..0x08082b18)
#
# Seg-8a: 7 named fns + 2 ROM_INCBIN (BLK1+BLK2) + 1 JT
# C13=49: 38 EQ + 10 RENAME (gP1LifePoints) + 1 DAT_ (R4 base)
# REF=0 (no standalone USER-label REF slots)
# FUNC_RENAME=0 (all 7 named fns correct)
# PLATE=7 (6 CJK mojibake -> ASCII; 1 new plate for Seg-8a context)
#   Note: tick_equip_display_4state (L18116) plate is already ASCII from prior session.
#         Plates 1-6 at the 6 other named fns need full CJK->ASCII rewrite.
#
# NEW constants added to constants/*.inc before running this script:
#   card_info.inc: GRAVEDIGGER_GHOUL_CID=0x12ed, DISAPPEAR_CID=0x1515,
#                  TWO_PRONGED_ATTACK_CID=0x12e7
#   duel_field.inc: set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9,
#                   check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr=0x0805000d,
#                   EQUIP_DISPLAY_OP_PARAM_1A1=0x000001a1
#
# REUSE constants (by value, grep-verified):
#   ewram.inc:   gDuelPhaseFlags=0x0201b290, gEquipChainSlotRefs=0x0201bb90,
#                gDuelFieldSlots=0x0201c510, gDuelCardCtxBase=0x0201e2a0,
#                PLAYER_BLOCK_STRIDE=0x868, ELIGIB_SPRITE_CTRL_OFF=0x1d68,
#                ELIGIB_ANIM_STATE_OFF=0x1d6c, gP1LifePoints
#   duel_field.inc: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff,
#                   EQUIP_ACT_SCORE_MODE_103=0x103, TRIGGER_OP_PARAM_10D3=0x10d3,
#                   lookup_equip_score_mooyan_p1=0x199, DRAW_DECIMAL_WIN_LABEL_ARG=0x10f,
#                   EQUIP_ACTIVATION_AUX_OFF=0x4b4
#                   ELIGIB_SPRITE_CTRL_OFF/ELIGIB_ANIM_STATE_OFF=0x1d68/0x1d6c
#   card_info.inc: DARK_BLADE_THE_DRAGON_KNIGHT_CID=0x183c, WHITE_HORNS_DRAGON_CID=0x1996
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType

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
    # ---- tick_equip_activation_display_4state literal pools ----
    # REUSE: gDuelPhaseFlags=0x0201b290
    (0x080822b0, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_display_4state_phase_flags_b0',
     'gDuelPhaseFlags: duel phase state base'),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff
    (0x08082364, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_act_display_4state_attr_clear_64',
     'AND mask clears bits[15:14] of effect node attr word'),
    # REUSE: gEquipChainSlotRefs=0x0201bb90
    (0x08082368, 0x0201bb90, 'gEquipChainSlotRefs',
     'tick_equip_act_display_4state_chain_refs_68', None),
    # REUSE: PLAYER_BLOCK_STRIDE=0x868
    (0x0808236c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_act_display_4state_stride_6c', None),
    # REUSE: gDuelFieldSlots=0x0201c510
    (0x08082370, 0x0201c510, 'gDuelFieldSlots',
     'tick_equip_act_display_4state_field_slots_70', None),
    # REUSE: gDuelCardCtxBase=0x0201e2a0
    (0x08082374, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_act_display_4state_card_ctx_74', None),
    # REUSE: EQUIP_ACT_SCORE_MODE_103=0x103
    (0x08082398, 0x00000103, 'EQUIP_ACT_SCORE_MODE_103',
     'tick_equip_act_display_4state_score_mode_98',
     'r0=0x103 to invoke_card_display_op_0x31_sub3 state 0'),
    # NEW: EQUIP_DISPLAY_OP_PARAM_1A1=0x1a1
    (0x0808239c, 0x000001a1, 'EQUIP_DISPLAY_OP_PARAM_1A1',
     'tick_equip_act_display_4state_op_param_9c',
     'r2=0x1a1 to invoke_card_display_op_0x31_sub3 (sibling 0x103/0x1a0/0x1a2)'),
    # REUSE: gDuelPhaseFlags
    (0x080823d8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_display_4state_phase_flags_d8', None),
    # REUSE: gEquipChainSlotRefs
    (0x08082408, 0x0201bb90, 'gEquipChainSlotRefs',
     'tick_equip_act_display_4state_chain_refs_08b', None),
    # REUSE: gDuelCardCtxBase
    (0x08082440, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_act_display_4state_card_ctx_40', None),
    # NEW: set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9
    (0x0808245c, 0x080905e9, 'set_equip_activation_state_by_mode_alt_fn_ptr',
     'tick_equip_act_display_4state_fn_ptr_alt_5c',
     'THUMB+1 ptr to set_equip_activation_state_by_mode_alt (0x080905e8)'),
    # REUSE: ELIGIB_SPRITE_CTRL_OFF=0x1d68
    (0x0808248c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'tick_equip_act_display_4state_sprite_ctrl_8c',
     'gP1LifePoints+ELIGIB_SPRITE_CTRL_OFF: sprite ctrl halfword offset'),
    # REUSE: ELIGIB_ANIM_STATE_OFF=0x1d6c
    (0x08082490, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'tick_equip_act_display_4state_anim_state_90', None),

    # ---- dispatch_equip_activation_display_if_slot_card_id_ok literal pools ----
    # REUSE: PLAYER_BLOCK_STRIDE=0x868
    (0x080824d8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_equip_act_disp_stride_d8', None),
    # REUSE: gDuelFieldSlots=0x0201c510
    (0x080824dc, 0x0201c510, 'gDuelFieldSlots',
     'dispatch_equip_act_disp_field_slots_dc', None),

    # ---- tick_equip_display_4state_with_effect_slot_array literal pools ----
    # REUSE: gDuelCardCtxBase
    (0x080824fc, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_disp_4state_slot_arr_card_ctx_fc', None),
    # REUSE: gDuelCardCtxBase
    (0x08082544, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_disp_4state_slot_arr_card_ctx_44', None),
    # REUSE: TRIGGER_OP_PARAM_10D3=0x10d3
    (0x08082548, 0x000010d3, 'TRIGGER_OP_PARAM_10D3',
     'tick_equip_disp_4state_slot_arr_trigger_48',
     'trigger op param 0x10d3; asm/10 L18485'),
    # REUSE: gDuelPhaseFlags
    (0x08082564, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_disp_4state_slot_arr_phase_flags_64', None),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x080825a4, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_disp_4state_slot_arr_attr_clear_a4', None),
    # NEW: check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr=0x0805000d
    (0x080825a8, 0x0805000d, 'check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr',
     'tick_equip_disp_4state_slot_arr_fn_ptr_a8',
     'THUMB+1 ptr to check_equip_slot_eligible_by_card_id_and_prereqs (0x0805000c)'),
    # REUSE: ELIGIB_SPRITE_CTRL_OFF=0x1d68
    (0x080825d8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'tick_equip_disp_4state_slot_arr_sprite_ctrl_d8', None),
    # REUSE: lookup_equip_score_mooyan_p1=0x199
    (0x080825fc, 0x00000199, 'lookup_equip_score_mooyan_p1',
     'tick_equip_disp_4state_slot_arr_score_mooyan_fc',
     'r1=0x199 equip score op; sibling of state 2 invoke sub3'),

    # ---- tick_equip_display_3state_with_effect_node_probe literal pools ----
    # REUSE: gDuelPhaseFlags
    (0x0808265c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_disp_3state_probe_phase_flags_5c', None),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x080826a8, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_disp_3state_probe_attr_clear_a8', None),
    # REUSE: gDuelCardCtxBase
    (0x080826ac, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_disp_3state_probe_card_ctx_ac', None),
    # REUSE: DRAW_DECIMAL_WIN_LABEL_ARG=0x10f
    (0x080826c8, 0x0000010f, 'DRAW_DECIMAL_WIN_LABEL_ARG',
     'tick_equip_disp_3state_probe_win_label_c8',
     'trigger op param 0x10f; DRAW_DECIMAL_WIN_LABEL_ARG'),
    # NEW: set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9 (2nd slot)
    (0x080826cc, 0x080905e9, 'set_equip_activation_state_by_mode_alt_fn_ptr',
     'tick_equip_disp_3state_probe_fn_ptr_alt_cc',
     'THUMB+1 ptr to set_equip_activation_state_by_mode_alt (0x080905e8)'),

    # ---- enqueue_equip_slot_sprite_with_attr_strip ----
    # REUSE: gDuelPhaseFlags (state tracking base)
    (0x08082740, 0x0201b290, 'gDuelPhaseFlags',
     'enqueue_equip_slot_sprite_phase_flags_40', None),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x0808276c, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'enqueue_equip_slot_sprite_attr_clear_6c',
     'AND mask [r0+4] with 0xfffc7fff: clear bits[15:14] attr field'),

    # ---- tick_equip_display_by_card_id_group_a_4state CID slots ----
    # NEW: GRAVEDIGGER_GHOUL_CID=0x12ed
    (0x080829dc, 0x000012ed, 'GRAVEDIGGER_GHOUL_CID',
     'tick_equip_disp_group_a_ghoul_cid_dc',
     'BST node: 0x12ed Gravedigger Ghoul -> type 2'),
    # REUSE: DARK_BLADE_THE_DRAGON_KNIGHT_CID=0x183c
    (0x080829f4, 0x0000183c, 'DARK_BLADE_THE_DRAGON_KNIGHT_CID',
     'tick_equip_disp_group_a_dark_blade_cid_f4',
     'BST node: 0x183c Dark Blade the Dragon Knight -> type 3'),
    # NEW: DISAPPEAR_CID=0x1515
    (0x080829f8, 0x00001515, 'DISAPPEAR_CID',
     'tick_equip_disp_group_a_disappear_cid_f8',
     'BST node: 0x1515 Disappear -> type 1'),
    # REUSE: WHITE_HORNS_DRAGON_CID=0x1996
    (0x08082a04, 0x00001996, 'WHITE_HORNS_DRAGON_CID',
     'tick_equip_disp_group_a_white_horns_cid_04',
     'BST node: 0x1996 White Horns Dragon -> type 5'),
    # REUSE: gDuelPhaseFlags
    (0x08082a30, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_disp_group_a_phase_flags_30', None),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x08082a80, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_disp_group_a_attr_clear_80', None),
    # REUSE: EQUIP_ACTIVATION_AUX_OFF=0x4b4
    (0x08082ab0, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF',
     'tick_equip_disp_group_a_aux_off_b0',
     'gDuelPhaseFlags+0x4b4 equip activation auxiliary counter offset'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: gP1LifePoints already-symbolic (10 slots) + other renames
#    (slot_addr, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # gP1LifePoints already-symbolic (10 slots)
    (0x08082378, 'tick_equip_act_display_4state_lp_ptr_78',
     'gP1LifePoints: EWRAM LP tracking base (ewram.inc)'),
    (0x080823b0, 'tick_equip_act_display_4state_lp_ptr_b0', None),
    (0x080823d4, 'tick_equip_act_display_4state_lp_ptr_d4', None),
    (0x08082404, 'tick_equip_act_display_4state_lp_ptr_04b', None),
    (0x08082488, 'tick_equip_act_display_4state_lp_ptr_88', None),
    (0x080825d4, 'tick_equip_disp_4state_slot_arr_lp_ptr_d4', None),
    (0x0808262c, 'tick_equip_act_display_4state_lp_ptr_2c', None),
    (0x08082a84, 'tick_equip_disp_group_a_lp_ptr_84', None),
    (0x08082aac, 'tick_equip_disp_group_a_lp_ptr_ac', None),
    (0x08082b14, 'tick_equip_disp_group_a_lp_ptr_b14', None),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: Full CJK->ASCII plate replacements for 6 functions in Seg-8a
#    All text pure ASCII. setPlateComment replaces entire plate.
#    Function tick_equip_activation_display_4state plate already ASCII - skip.
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # 1. dispatch_equip_activation_display_if_slot_card_id_ok (0x080824a4)
    (0x080824a4,
     "@ Equip activation display router, card-ID prerequisite. indeg=0, Sub-type A.\n"
     "@ Receives card_entry_ptr(r0) and secondary_ptr(r1).\n"
     "@ Extracts player_id(bit0) and slot_idx(bits[5:1]) from card_entry[+2].\n"
     "@ Computes target slot card_id at [gDuelFieldSlots+player*PLAYER_BLOCK_STRIDE+slot*0x14];\n"
     "@   if mismatch returns -1.\n"
     "@ Reads confirm_flag at [gDuelCardCtxBase+player*4+8];\n"
     "@   if==1 calls select_equip_target_slot_by_effect_strategy;\n"
     "@   else calls tick_equip_activation_display_3state.\n"
     "@ Passes result through. Exit Sub-case E (pop {r1};bx r1)."),

    # 2. tick_equip_display_4state_with_effect_slot_array (0x08082510)
    (0x08082510,
     "@ Equip display 4-state machine with effect slot array push. indeg=0, Sub-type A.\n"
     "@ confirm_flag==1 fast path: select_equip_target_slot_by_effect_strategy +\n"
     "@   push_to_effect_slot_array, return 1.\n"
     "@ Otherwise 4-state machine at [gDuelPhaseFlags+0x96*8]:\n"
     "@   state 0: trigger op 0x65 + clear card_entry flags +\n"
     "@     set_equip_activation_state_by_mode with fn_ptr=check_equip_slot_eligible_fn_ptr;\n"
     "@   state 1: check_activation_display_state_is_confirmed;\n"
     "@     confirmed->enqueue_equip_slot_sprite_with_code_rotation;\n"
     "@   state 2: invoke_card_display_op_0x31_sub3(0x7f, 0x198, 0x199);\n"
     "@   state 3: push_to_effect_slot_array + set_lp_display_row_type15, return 1.\n"
     "@ Exit Sub-case E (pop {r1};bx r1)."),

    # 3. tick_equip_display_3state_with_effect_node_probe (0x0808263c)
    (0x0808263c,
     "@ Equip display 3-state machine with effect node dual-scan. indeg=0, Sub-type A.\n"
     "@ Reads [gDuelPhaseFlags+0x96*8]:\n"
     "@   state 0: clear flags; node_count>1 and confirmed->select_equip_target_slot;\n"
     "@     unconfirmed->trigger op 0x10f + set_equip_activation_state with\n"
     "@       fn_ptr=set_equip_activation_state_by_mode_alt_fn_ptr;\n"
     "@     count<=1->dual loop invoke_effect_node_handler_3arg(slot 0..1, zone 0..4),\n"
     "@       hit->enqueue_sprite + state:=2;\n"
     "@   state 1: tick_equip_activation_display_3state;\n"
     "@   state 2: resolve_slot_card_id_for_pair -> strh card_id to [entry+0xc], return 1.\n"
     "@ Exit Sub-case E (pop {r1};bx r1)."),

    # 4. enqueue_equip_slot_sprite_with_attr_strip (0x08082744)
    (0x08082744,
     "@ Equip slot sprite enqueue helper, clears attr bits first.\n"
     "@ Receives effect_node_ptr(r0).\n"
     "@ ANDs [r0+4] with DUAL_LABEL_RENDER_STATE_CLEAR(0xfffc7fff) to clear bits[15:14].\n"
     "@ ANDs [r0+6] with ~0x1d=0xe2 to clear state flag bits[4:0].\n"
     "@ Extracts slot_idx via bits[13:9] of [r0+0x14]: lsls#0x12/lsrs#0x17 (net shift 5).\n"
     "@ Extracts player_id via bit[21] of [r0+0x14]: lsls#0x16/lsrs#0x1f.\n"
     "@ Calls enqueue_equip_slot_sprite_with_code_rotation(node_ptr, player_id, slot_idx).\n"
     "@ Returns 1 always. Exit: pop {r1};bx r1 (Sub-case E)."),

    # 5. check_effect_slot_zone_field_by_type (0x08082770)
    (0x08082770,
     "@ Effect slot zone-field type check.\n"
     "@ Receives effect_node_ptr(r0), player_id_or_side(r1), slot_type_qualifier(r2).\n"
     "@ Push {r4,r5,r6,r7,lr}: spills r0->r5, r1->r6, r2->r7.\n"
     "@ Calls set_equip_activation_state_by_mode_alt(node_ptr, ...).\n"
     "@ ZONE_FIELD_BITS = bits[4:3] of [r5+6]: 3-case dispatch [0..2].\n"
     "@ case 0: extract bit0 of [r5+2] as player_id; compare with r6.\n"
     "@ case 1: combine r6/r7 into 16-bit; compare with read_effect_slot_side_and_type result.\n"
     "@ case 2: XOR effect_slot player_id with r6; nonzero=fail.\n"
     "@ Returns 0 (no match) or 1 (match). Exit Sub-case E."),

    # 6. tick_equip_display_by_card_id_group_a_4state (0x080829bc)
    (0x080829bc,
     "@ Equip display 4-state machine routed by card_id group A.\n"
     "@ card_id BST dispatch:\n"
     "@   0x12ed (Gravedigger Ghoul) -> type 2,\n"
     "@   0x12f9 (Soul Release, computed DWORD_080829dc+0xc=0x12ed+0xc) -> type 5,\n"
     "@   0x1480 (Kycoo the Ghost Destroyer, computed 0xa4<<5) -> type 2,\n"
     "@   0x1515 (Disappear) -> type 1,\n"
     "@   0x183c (Dark Blade the Dragon Knight) -> type 3,\n"
     "@   0x1996 (White Horns Dragon) -> type 5.\n"
     "@ After BST reads IWRAM state at [gDuelPhaseFlags+0x4b0].\n"
     "@ state 0: clear attr_bits + dispatch_card_effect_activation +\n"
     "@   format_game_text + trigger.\n"
     "@ state 1: check_confirmed -> enqueue_sprite or step-1.\n"
     "@ state 2: load [gDuelPhaseFlags+0x4b4] as palette_id,\n"
     "@   call get_effect_slot_entry_ptr_by_palette_id + find_slot_by_palette_id_in_table\n"
     "@   + pack_equip_slot_sprite_with_code_attr.\n"
     "@ state>=3: step+1, return 1."),
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

def _apply_cjk_plate(func_addr, new_plate_text):
    """Full plate rewrite (CJK->ASCII). WARN=FAIL per reviewer requirement."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] PLATE 0x%08x: ASCII rewrite" % func_addr)
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    # Verify set succeeded
    read_back = cu.getComment(CodeUnit.PLATE_COMMENT)
    if read_back is None or len(read_back) < 10:
        print("[FAIL] plate 0x%08x: set failed or too short" % func_addr)
    else:
        print("[PLT] 0x%08x: ASCII plate applied (%d chars)" % (func_addr, len(new_plate_text)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF10Seg8aSlots (DRY=%s) ===" % DRY)
    print("  Seg-8a: [0x08082290..0x08082b18) -- EQ=%d, RENAME=%d, PLATE=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(CJK_PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # C. PLATE_REWRITES (CJK->ASCII)
    print("\n--- C. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineF10Seg8aSlots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(CJK_PLATE_REWRITES)))

main()
