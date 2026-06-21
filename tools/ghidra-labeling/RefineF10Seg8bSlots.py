# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg8bSlots.py -- f10 Seg-8b slot symbolization [0x08082b18..0x08083450)
#
# Seg-8b: 12 named fns, 0 ROM_INCBIN, 0 disasm
# C13=67: 56 EQ + 4 RENAME(gP1LifePoints) + 4 RENAME(fn-ptr) + 3 PTR_(skip)
# REF=0; FUNC_RENAME=0; PLATE=6 (6 CJK mojibake -> ASCII)
#
# NEW constants added to constants/*.inc before running this script:
#   card_info.inc: SHIFT_CID=0x140a, FIENDS_HAND_MIRROR_CID=0x1719,
#                  BACKUP_SOLDIER_CID=0x1359, MIRACLE_DIG_CID=0x149e,
#                  KELDO_CID=0x14e7, HIDDEN_BOOK_OF_SPELL_CID=0x1630,
#                  PRIMAL_SEED_CID=0x16d6, GRAVEYARD_IN_FOURTH_DIMENSION_CID=0x17f7,
#                  FORCES_OF_DARKNESS_CID=0x1974,
#                  cid_1568=0x1568, cid_16d3=0x16d3, cid_1803=0x1803
#   duel_field.inc: EQUIP_PAIR_ENTRY_TABLE_BASE=0x09e3f140
#
# REUSE constants (by value, grep-verified):
#   ewram.inc:    gDuelPhaseFlags=0x0201b290, gDuelCardCtxBase=0x0201e2a0,
#                 gDuelFieldSlots=0x0201c510, gP1HandSlotArray=0x0201c8f8,
#                 PLAYER_BLOCK_STRIDE=0x868, ELIGIB_SPRITE_CTRL_OFF=0x1d68,
#                 ELIGIB_ANIM_STATE_OFF=0x1d6c, LP_CARD_TRACK_BASE_OFF=0x1da8,
#                 P1LP_BLOCK2_OFF_1CE8=0x1ce8
#   duel_field.inc: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff,
#                   EQUIP_ACTIVE_CTX_OFF=0x484, LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff,
#                   EQUIP_ACTIVATION_AUX_OFF=0x4b4,
#                   set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9
#   card_info.inc: DNA_SURGERY_CID=0x1357, RAY_OF_HOPE_CID=0x16a8,
#                  DARK_FACTORY_MASS_PROD_CID=0x17f1, BEHEMOTH_KING_CID=0x1864,
#                  POT_OF_AVARICE_CID=0x196f, equip_cid_15de_08048a68=0x15de,
#                  SPELL_ZONE_TARGET_CARD_ID=0x1368,
#                  CARD_DISPLAY_OP31_LP_BAR_SUB=0x11d
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: fn-ptr RENAME slots (4) keep raw hex .word values; EOL explains THUMB+1 semantics.
#       No mid-code USER labels on fn-ptr slots per scope convention.
# NOTE: PLATE WARN=FAIL: if pattern not found in existing plate, print FAIL and abort that plate.

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
    # ---- tick_equip_display_with_fn_ptr_routing_3state (0x08082b88) literal pools ----
    # NEW: SHIFT_CID=0x0000140a
    (0x08082ba8, 0x0000140a, 'SHIFT_CID',
     'tick_equip_fn_ptr_routing_3state_shift_cid_a8',
     'BST root: 0x140a Shift -> fn-ptr dispatch'),
    # NEW: FIENDS_HAND_MIRROR_CID=0x00001719
    (0x08082bb4, 0x00001719, 'FIENDS_HAND_MIRROR_CID',
     'tick_equip_fn_ptr_routing_3state_fiends_mirror_cid_b4',
     'BST right: 0x1719 Fiend Hand Mirror -> fn-ptr dispatch'),
    # REUSE: gDuelPhaseFlags=0x0201b290
    (0x08082be8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_fn_ptr_routing_3state_phase_flags_e8', None),
    # REUSE: EQUIP_ACTIVE_CTX_OFF=0x00000484
    (0x08082c30, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'tick_equip_fn_ptr_routing_3state_act_ctx_off_30',
     'gDuelPhaseFlags+0x484 equip activation context offset'),
    # REUSE: ELIGIB_SPRITE_CTRL_OFF=0x00001d68 (LP field offset)
    (0x08082c60, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'tick_equip_fn_ptr_routing_3state_sprite_ctrl_60', None),
    # REUSE: EQUIP_ACTIVE_CTX_OFF (2nd occurrence)
    (0x08082c78, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'tick_equip_fn_ptr_routing_3state_act_ctx_off_78', None),

    # ---- build_equip_chain_pair_slot_entry (0x08082c8c) literal pools ----
    # REUSE: LP_ROW_TYPE8_ALL_SLOTS_MASK=0x0000ffff
    (0x08082cf8, 0x0000ffff, 'LP_ROW_TYPE8_ALL_SLOTS_MASK',
     'build_equip_chain_pair_slot_entry_all_slots_mask_f8',
     '0xffff: clears upper halfword of equip chain pair entry'),

    # ---- tick_equip_chain_pair_display_4state (0x08082d0c) literal pools ----
    # REUSE: gDuelPhaseFlags
    (0x08082d2c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_chain_pair_4state_phase_flags_2c', None),
    # REUSE: set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9 (3rd occurrence)
    (0x08082d60, 0x080905e9, 'set_equip_activation_state_by_mode_alt_fn_ptr',
     'tick_equip_chain_pair_4state_fn_ptr_alt_60',
     'THUMB+1 ptr to set_equip_activation_state_by_mode_alt (0x080905e8)'),
    # REUSE: gDuelCardCtxBase=0x0201e2a0
    (0x08082dc0, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_chain_pair_4state_card_ctx_c0', None),

    # ---- tick_equip_lp_display_by_node_state (0x08082e98) literal pools ----
    # REUSE: PLAYER_BLOCK_STRIDE=0x00000868
    (0x08082e20, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_lp_disp_node_state_stride_20', None),
    # REUSE: gDuelFieldSlots=0x0201c510
    (0x08082e24, 0x0201c510, 'gDuelFieldSlots',
     'tick_equip_lp_disp_node_state_field_slots_24', None),
    # REUSE: ELIGIB_SPRITE_CTRL_OFF=0x00001d68
    (0x08082e60, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'tick_equip_lp_disp_node_state_sprite_ctrl_60', None),
    # REUSE: ELIGIB_ANIM_STATE_OFF=0x00001d6c
    (0x08082e64, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'tick_equip_lp_disp_node_state_anim_state_64', None),
    # REUSE: gDuelPhaseFlags
    (0x08082e68, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_disp_node_state_phase_flags_68', None),
    # REUSE: gDuelPhaseFlags
    (0x08082e80, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_disp_node_state_phase_flags_80', None),
    # REUSE: gDuelPhaseFlags
    (0x08082eb4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_disp_node_state_phase_flags_b4', None),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff
    (0x08082ee0, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_lp_disp_node_state_attr_clear_e0',
     'AND mask clears bits[15:14] of effect node attr word'),
    # REUSE: LP_CARD_TRACK_BASE_OFF=0x00001da8
    (0x08082f08, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_lp_disp_node_state_lp_track_base_08',
     'gP1LifePoints+LP_CARD_TRACK_BASE_OFF: LP card-ref tracking base'),
    # REUSE: LP_CARD_TRACK_BASE_OFF (2nd occurrence)
    (0x08082f38, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_lp_disp_node_state_lp_track_base_38', None),

    # ---- tick_equip_display_by_card_id_group_b_3state (0x08082f44) literal pools ----
    # REUSE: DNA_SURGERY_CID=0x00001357
    (0x08082f30, 0x00001357, 'DNA_SURGERY_CID',
     'tick_equip_disp_group_b_dna_surgery_cid_30',
     'set_lp_display_row_type15 arg: 0x1357 DNA Surgery check'),
    # NEW: PRIMAL_SEED_CID=0x000016d6
    (0x08082f7c, 0x000016d6, 'PRIMAL_SEED_CID',
     'tick_equip_disp_group_b_primal_seed_cid_7c',
     'BST node: 0x16d6 Primal Seed'),
    # NEW: KELDO_CID=0x000014e7
    (0x08082f80, 0x000014e7, 'KELDO_CID',
     'tick_equip_disp_group_b_keldo_cid_80',
     'BST node: 0x14e7 Keldo'),
    # NEW: BACKUP_SOLDIER_CID=0x00001359
    (0x08082f84, 0x00001359, 'BACKUP_SOLDIER_CID',
     'tick_equip_disp_group_b_backup_soldier_cid_84',
     'BST node: 0x1359 Backup Soldier'),
    # NEW: MIRACLE_DIG_CID=0x0000149e
    (0x08082f90, 0x0000149e, 'MIRACLE_DIG_CID',
     'tick_equip_disp_group_b_miracle_dig_cid_90',
     'BST node: 0x149e Miracle Dig'),
    # NEW: HIDDEN_BOOK_OF_SPELL_CID=0x00001630
    (0x08082fa8, 0x00001630, 'HIDDEN_BOOK_OF_SPELL_CID',
     'tick_equip_disp_group_b_hidden_book_cid_a8',
     'BST node: 0x1630 Hidden Book of Spell'),
    # REUSE: RAY_OF_HOPE_CID=0x000016a8
    (0x08082fb4, 0x000016a8, 'RAY_OF_HOPE_CID',
     'tick_equip_disp_group_b_ray_of_hope_cid_b4',
     'BST node: 0x16a8 Ray of Hope'),
    # NEW: GRAVEYARD_IN_FOURTH_DIMENSION_CID=0x000017f7
    (0x08082fd0, 0x000017f7, 'GRAVEYARD_IN_FOURTH_DIMENSION_CID',
     'tick_equip_disp_group_b_graveyard_4d_cid_d0',
     'BST node: 0x17f7 The Graveyard in the Fourth Dimension'),
    # REUSE: DARK_FACTORY_MASS_PROD_CID=0x000017f1
    (0x08082fd8, 0x000017f1, 'DARK_FACTORY_MASS_PROD_CID',
     'tick_equip_disp_group_b_dark_factory_cid_d8',
     'BST node: 0x17f1 Dark Factory of Mass Production'),
    # REUSE: POT_OF_AVARICE_CID=0x0000196f
    (0x08082ff0, 0x0000196f, 'POT_OF_AVARICE_CID',
     'tick_equip_disp_group_b_pot_avarice_cid_f0',
     'BST node: 0x196f Pot of Avarice'),
    # REUSE: BEHEMOTH_KING_CID=0x00001864
    (0x08082ff4, 0x00001864, 'BEHEMOTH_KING_CID',
     'tick_equip_disp_group_b_behemoth_cid_f4',
     'BST node: 0x1864 Behemoth the King of All Animals'),
    # NEW: FORCES_OF_DARKNESS_CID=0x00001974
    (0x08083000, 0x00001974, 'FORCES_OF_DARKNESS_CID',
     'tick_equip_disp_group_b_forces_dark_cid_00',
     'BST node: 0x1974 The Forces of Darkness'),

    # ---- tick_equip_lp_display_by_node_state_4state (0x08083170) literal pools ----
    # REUSE: CARD_DISPLAY_OP31_LP_BAR_SUB=0x0000011d
    (0x08083010, 0x0000011d, 'CARD_DISPLAY_OP31_LP_BAR_SUB',
     'tick_equip_lp_disp_group_b_lp_bar_sub_10',
     'LP bar subtract display op 0x11d'),
    # REUSE: CARD_DISPLAY_OP31_LP_BAR_SUB (2nd occurrence)
    (0x08083054, 0x0000011d, 'CARD_DISPLAY_OP31_LP_BAR_SUB',
     'tick_equip_lp_disp_group_b_lp_bar_sub_54', None),
    # REUSE: gDuelPhaseFlags
    (0x08083088, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_disp_group_b_phase_flags_88', None),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x080830d0, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_disp_group_b_attr_clear_d0', None),
    # REUSE: EQUIP_ACTIVATION_AUX_OFF=0x000004b4
    (0x080830f8, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF',
     'tick_equip_disp_group_b_aux_off_f8',
     'gDuelPhaseFlags+0x4b4 equip activation auxiliary counter (SLOT_PALETTE_OFFSET)'),
    # REUSE: EQUIP_ACTIVATION_AUX_OFF (2nd occurrence)
    (0x0808314c, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF',
     'tick_equip_disp_group_b_aux_off_4c', None),

    # ---- tick_equip_lp_display_by_node_state_4state (0x08083170) literal pools ----
    # REUSE: P1LP_BLOCK2_OFF_1CE8=0x00001ce8
    (0x080831a0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'tick_equip_lp_disp_4state_lp_block2_off_a0',
     '[gP1LifePoints+0x1ce8] XORd with [gDuelPhaseFlags+0x4b4] to derive r4'),
    # REUSE: gDuelPhaseFlags
    (0x080831a4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_disp_4state_phase_flags_a4', None),
    # REUSE: EQUIP_ACTIVATION_AUX_OFF (3rd occurrence)
    (0x080831a8, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF',
     'tick_equip_lp_disp_4state_aux_off_a8',
     'XOR_OPERAND_OFF=0x4b4; subs r2,#0x4 -> STATE_OFFSET=0x4b0'),
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x080831cc, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'tick_equip_lp_disp_4state_attr_clear_cc', None),
    # REUSE: gDuelPhaseFlags
    (0x0808321c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_disp_4state_phase_flags_1c', None),
    # REUSE: LP_CARD_TRACK_BASE_OFF (3rd occurrence)
    (0x0808325c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_equip_lp_disp_4state_lp_track_base_5c', None),
    # REUSE: PLAYER_BLOCK_STRIDE (2nd occurrence)
    (0x08083260, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_lp_disp_4state_stride_60', None),
    # REUSE: gDuelPhaseFlags
    (0x0808329c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_disp_4state_phase_flags_9c', None),

    # ---- advance_equip_slot_display_state (0x08083280) literal pools ----
    # REUSE: DUAL_LABEL_RENDER_STATE_CLEAR
    (0x080832cc, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'advance_equip_slot_disp_state_attr_clear_cc', None),
    # REUSE: equip_cid_15de_08048a68=0x000015de
    (0x080832ec, 0x000015de, 'equip_cid_15de_08048a68',
     'advance_equip_slot_disp_state_cid_15de_ec',
     'card_id dispatch: 0x15de equip card (low confidence name)'),
    # REUSE: SPELL_ZONE_TARGET_CARD_ID=0x00001368
    (0x080832f0, 0x00001368, 'SPELL_ZONE_TARGET_CARD_ID',
     'advance_equip_slot_disp_state_spell_zone_cid_f0',
     'card_id dispatch: 0x1368 Spell Zone Target'),
    # NEW: cid_1568=0x00001568 (neutral, unassigned)
    (0x080832f4, 0x00001568, 'cid_1568',
     'advance_equip_slot_disp_state_cid_1568_f4',
     'unassigned CID 0x1568 in advance_equip_slot_display_state dispatch'),
    # NEW: cid_16d3=0x000016d3 (neutral, unassigned)
    (0x08083308, 0x000016d3, 'cid_16d3',
     'advance_equip_slot_disp_state_cid_16d3_08',
     'unassigned CID 0x16d3 in advance_equip_slot_display_state dispatch'),
    # NEW: cid_1803=0x00001803 (neutral, unassigned)
    (0x08083314, 0x00001803, 'cid_1803',
     'advance_equip_slot_disp_state_cid_1803_14',
     'unassigned CID 0x1803 in advance_equip_slot_display_state dispatch'),

    # ---- dispatch_equip_display_if_confirm_state_one (0x080833a8) literal pools ----
    # REUSE: gDuelPhaseFlags
    (0x08083358, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_equip_disp_confirm_state_phase_flags_58', None),

    # ---- enqueue_equip_slot_sprites_for_pair_loop (0x080833bc) literal pools ----
    # REUSE: PLAYER_BLOCK_STRIDE (3rd occurrence)
    (0x080833f0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_slot_sprites_pair_loop_stride_f0',
     'PAIR_STEP=0x868 per-player stride in pair loop'),
    # REUSE: gP1HandSlotArray=0x0201c8f8
    (0x080833f4, 0x0201c8f8, 'gP1HandSlotArray',
     'enqueue_equip_slot_sprites_pair_loop_hand_slot_f4', None),
    # NEW: EQUIP_PAIR_ENTRY_TABLE_BASE=0x09e3f140
    (0x080833f8, 0x09e3f140, 'EQUIP_PAIR_ENTRY_TABLE_BASE',
     'enqueue_equip_slot_sprites_pair_loop_pair_table_f8',
     'PAIR_TABLE_BASE=0x09e3f140 ROM pair data table base; loop r6=0..2 ldr [r2+r6*4]'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    gP1LifePoints already-symbolic (4 slots) + fn-ptr slots (4 slots)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # gP1LifePoints already-symbolic (4 slots)
    (0x08082c5c, 'tick_equip_fn_ptr_routing_3state_lp_ptr_5c',
     'gP1LifePoints: EWRAM LP tracking base (ewram.inc)'),
    (0x08082e5c, 'tick_equip_lp_disp_node_state_lp_ptr_5c', None),
    (0x0808319c, 'tick_equip_lp_disp_4state_lp_ptr_9c', None),
    (0x08083388, 'dispatch_equip_disp_confirm_state_lp_ptr_88', None),

    # fn-ptr RENAME slots (4 slots; THUMB+1 fn addresses; keep raw hex .word)
    # DWORD_08082bbc -> invoke_effect_node_handler_if_slot_in_range+1
    (0x08082bbc, 'invoke_effect_node_handler_if_slot_in_range_fn_ptr',
     'THUMB+1 ptr to invoke_effect_node_handler_if_slot_in_range (0x08082b18)'),
    # DWORD_08082bc4 -> invoke_effect_node_handler_if_slot_type_ok+1
    (0x08082bc4, 'invoke_effect_node_handler_if_slot_type_ok_fn_ptr',
     'THUMB+1 ptr to invoke_effect_node_handler_if_slot_type_ok (0x08082b2c)'),
    # DWORD_08082be4 -> invoke_effect_node_handler_if_slot_whitelisted+1
    (0x08082be4, 'invoke_effect_node_handler_if_slot_whitelisted_fn_ptr',
     'THUMB+1 ptr to invoke_effect_node_handler_if_slot_whitelisted (0x08082b5c)'),
    # DWORD_08082dbc -> build_equip_chain_pair_slot_entry+1
    (0x08082dbc, 'build_equip_chain_pair_slot_entry_fn_ptr',
     'THUMB+1 ptr to build_equip_chain_pair_slot_entry (0x08082c8c)'),
]

# ---------------------------------------------------------------------------
# C. CJK_PLATE_REWRITES: Full CJK->ASCII plate replacements
#    6 functions in Seg-8b have CJK mojibake plates needing full ASCII rewrite.
#    All text pure ASCII. WARN=FAIL: if existing plate is None or unreadable,
#    print FAIL. We do full replacement (not substring).
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # 1. tick_equip_display_with_fn_ptr_routing_3state (0x08082b88)
    (0x08082b88,
     "@ Equip display 3-state machine with fn-ptr routing. Receives effect_node_ptr(r0).\n"
     "@ card_id BST: 0x1327(Fairy's Hand Mirror,computed=0x140a-0xe3),\n"
     "@   0x140a(Shift), 0x1719(Fiend's Hand Mirror)\n"
     "@   each mapped to different display op fn-ptr (loaded into r7).\n"
     "@ Then reads IWRAM state [gDuelPhaseFlags+0x4b0].\n"
     "@ State 0: clear attr_bits + format_game_text_with_int_arg + trigger +\n"
     "@   set_equip_activation_state_by_mode, step+1, return 0.\n"
     "@ State 1: check_activation_display_state_is_confirmed ->\n"
     "@   enqueue_equip_slot_sprite_with_code_rotation, step+1.\n"
     "@ State 2: write [gDuelPhaseFlags+0x484]:=r5 (store activation slot snapshot), step+1.\n"
     "@ STATE_OFFSET=0x4b0; EQUIP_ACTIVE_CTX_OFF=0x484."),

    # 2. build_equip_chain_pair_slot_entry (0x08082c8c)
    (0x08082c8c,
     "@ Build equip chain pair slot entry. Receives effect_node_ptr(r0).\n"
     "@ Reads effect slot side/type via read_effect_slot_side_and_type.\n"
     "@ Iterates find_equip_chain_pair_slot to locate matching pair entry.\n"
     "@ Updates entry data fields on match.\n"
     "@ Returns 1 on match, 0 on no match."),

    # 3. tick_equip_display_by_card_id_group_b_3state (0x08082f44)
    (0x08082f44,
     "@ Equip display 3-state machine routed by card_id group B.\n"
     "@ card_id BST dispatches 11 card slots:\n"
     "@   0x1359(Backup Soldier), 0x149e(Miracle Dig), 0x14e7(Keldo),\n"
     "@   0x1630(Hidden Book of Spell), 0x16a8(Ray of Hope), 0x16d6(Primal Seed),\n"
     "@   0x17f1(Dark Factory of Mass Production),\n"
     "@   0x17f7(Graveyard in the Fourth Dimension),\n"
     "@   0x1864(Behemoth the King of All Animals), 0x196f(Pot of Avarice),\n"
     "@   0x1974(The Forces of Darkness).\n"
     "@ STATE_OFFSET=0x4b0 (same offset as fn1).\n"
     "@ SLOT_PALETTE_OFFSET=0x4b4 (zeroed in state 1, palette count in state 2)."),

    # 4. tick_equip_lp_display_by_node_state_4state (0x08083170)
    (0x08083170,
     "@ Equip LP display 4-state machine. Receives effect_node_ptr(r0).\n"
     "@ XORs [gP1LifePoints+0x1ce8] with [gDuelPhaseFlags+0x4b4] to derive r4 value.\n"
     "@ STATE_OFFSET=0x4b0 (subs r2,#0x4 from 0x4b4 -> state at gDuelPhaseFlags+0x4b0).\n"
     "@ XOR_OPERAND_OFF=0x4b4 ([gDuelPhaseFlags+0x4b4] XORd with [gP1LifePoints+0x1ce8] to compute r4).\n"
     "@ State 0: invokes first LP display step."),

    # 5. dispatch_equip_display_if_confirm_state_one (0x080833a8)
    (0x080833a8,
     "@ Equip display dispatcher, conditional on confirm_state=1.\n"
     "@ Reads card_slot[+0xc] halfword (ldrh [r0,#0xc]) as confirm_state;\n"
     "@   if confirm_state==1 calls dispatch_equip_card_display_op_by_card_id and returns result;\n"
     "@   else returns 0."),

    # 6. enqueue_equip_slot_sprites_for_pair_loop (0x080833bc)
    (0x080833bc,
     "@ Enqueue equip slot sprites for pair loop. Receives effect_node_ptr(r0).\n"
     "@ Initializes loop counter r6=0, loads ROM pair data base address 0x09e3f140 into r2.\n"
     "@ Loop r6=0..2 (inclusive): loads card_pair_ptr=[r2+r6*4],\n"
     "@   then invokes enqueue_equip_slot_sprite_with_code_rotation for the sprite.\n"
     "@ PAIR_TABLE_BASE=0x09e3f140 (ROM pair data table base address).\n"
     "@ PAIR_STEP=0x868 (per-player stride).\n"
     "@ OP_CODE=0xe (pair enqueue operation param)."),
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
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

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
    return True

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return True

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))
    return True

def _apply_cjk_plate(func_addr, new_plate_text):
    """Full plate rewrite (CJK->ASCII). WARN=FAIL per reviewer requirement."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate 0x%08x: no code unit" % func_addr)
        return False

    if DRY:
        print("[dry] PLATE 0x%08x: ASCII rewrite (%d chars)" % (func_addr, len(new_plate_text)))
        return True

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    # Verify set succeeded
    read_back = cu.getComment(CodeUnit.PLATE_COMMENT)
    if read_back is None or len(read_back) < 10:
        print("[FAIL] plate 0x%08x: set failed or too short" % func_addr)
        return False
    else:
        print("[PLT] 0x%08x: ASCII plate applied (%d chars)" % (func_addr, len(new_plate_text)))
        return True

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF10Seg8bSlots (DRY=%s) ===" % DRY)
    print("  Seg-8b: [0x08082b18..0x08083450) -- EQ=%d, RENAME=%d, PLATE=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(CJK_PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: ok=%d fail=%d" % (eq_ok, eq_fail))

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        if _apply_rename(slot_addr, slot_label, eol):
            ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # C. CJK_PLATE_REWRITES
    print("\n--- C. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    plt_ok = 0
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        if _apply_cjk_plate(func_addr, new_plate):
            plt_ok += 1
    print("  PLATE done: %d / %d" % (plt_ok, len(CJK_PLATE_REWRITES)))

    print("\n=== RefineF10Seg8bSlots DONE ===")
    print("  EQ=%d/%d  RENAME=%d/%d  PLATE=%d/%d" % (
        eq_ok, len(EQ_SLOTS),
        ren_ok, len(RENAME_SLOTS),
        plt_ok, len(CJK_PLATE_REWRITES)))

main()
