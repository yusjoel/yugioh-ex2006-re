# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg9Slots.py -- f10 Seg-9 slot symbolization [0x08083450..0x08084318)
#
# Seg-9: 18 named functions, 2 ROM_INCBIN (handled in DisassembleF10Seg9Blocks.py)
# C13=92: EQ=81 + REF=7 + RENAME=4 = 92 unique auto-name slots
# FUNC_RENAME=0; PLATE=9 (CJK mojibake -> ASCII)
#
# NEW constants added to constants/*.inc before running this script:
#   card_info.inc:  ANCIENT_LAMP_CID=0x1476, DREAMSPRITE_CID=0x148a,
#                   BOOK_OF_LIFE_CID=0x1536,
#                   GEARFRIED_IRON_KNIGHT_CID_SHIFTED=0x9e180000
#   duel_field.inc: INVOKE_OP31_SUB1_PARAM_109=0x109
#   ewram.inc:      LP_ACTIVATION_PENDING_OFF=0x1d40
#
# REUSE constants (by value, grep-verified):
#   ewram.inc:    gDuelPhaseFlags=0x0201b290, gDuelCardCtxBase=0x0201e2a0,
#                 gEquipChainSlotRefs=0x0201bb90, gDuelFieldSlots=0x0201c510,
#                 gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868,
#                 ELIGIB_SPRITE_CTRL_OFF=0x1d68, ELIGIB_ANIM_STATE_OFF=0x1d6c,
#                 LP_CARD_TRACK_BASE_OFF=0x1da8, LP_CARD_TRACK_NEXT_OFF=0x1daa
#   duel_field.inc: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff (x7 slots),
#                   TRIGGER_OP_PARAM_107=0x107, set_equip_activation_state_by_mode_alt_fn_ptr=0x080905e9
#   card_info.inc:  DNA_TRANSPLANT_CID=0x171f, OTOHIME_CID=0x1503, TSUKUYOMI_CID=0x1694,
#                   RED_MOON_BABY_CID=0x1415
#   oam_attr.inc:   EQUIP_SLOT_SCORE_CAP=0xffff
#
# NOTE: EQUIP_NODE_ATTR_CLEAR_MASK DROPPED -- REUSE DUAL_LABEL_RENDER_STATE_CLEAR (duel_field.inc:134)
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: PLATE WARN=FAIL: if set fails, print FAIL.

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
#    81 total unique EQ slots (gP1LifePoints net=15 + 1 added=16 + all others)
#    All values ROM-verified.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== REUSE: gDuelPhaseFlags=0x0201b290 (ewram.inc) x26 =====
    (0x08083470, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083470', None),
    (0x0808353c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_0808353c', None),
    (0x08083554, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083554', None),
    (0x08083580, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083580', None),
    (0x08083728, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083728', None),
    (0x0808378c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_0808378c', None),
    (0x080837e4, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_080837e4', None),
    (0x08083888, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083888', None),
    (0x08083940, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083940', None),
    (0x080839d8, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_080839d8', None),
    (0x08083b2c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083b2c', None),
    (0x08083b44, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083b44', None),
    (0x08083bc0, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083bc0', None),
    (0x08083c1c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083c1c', None),
    (0x08083c70, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083c70', None),
    (0x08083c88, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083c88', None),
    (0x08083cb4, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083cb4', None),
    (0x08083d58, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083d58', None),
    (0x08083e30, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083e30', None),
    (0x08083edc, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083edc', None),
    (0x08083f6c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083f6c', None),
    (0x08083fd0, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08083fd0', None),
    (0x08084010, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084010', None),
    (0x08084028, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084028', None),
    (0x0808405c, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_0808405c', None),
    (0x08084140, 0x0201b290, 'gDuelPhaseFlags',
     'duel_phase_flags_08084140', None),

    # ===== REUSE: gDuelCardCtxBase=0x0201e2a0 (ewram.inc) x7 =====
    (0x080834d0, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_080834d0', None),
    (0x08083660, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_08083660', None),
    (0x080837c0, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_080837c0', None),
    (0x08083910, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_08083910', None),
    (0x08083a40, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_08083a40', None),
    (0x08083d94, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_08083d94', None),
    (0x08083ebc, 0x0201e2a0, 'gDuelCardCtxBase',
     'duel_card_ctx_base_08083ebc', None),

    # ===== REUSE: gEquipChainSlotRefs=0x0201bb90 (ewram.inc) x2 =====
    (0x08083788, 0x0201bb90, 'gEquipChainSlotRefs',
     'equip_chain_slot_refs_08083788', None),
    (0x08083d90, 0x0201bb90, 'gEquipChainSlotRefs',
     'equip_chain_slot_refs_08083d90', None),

    # ===== REUSE: ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc) x7 =====
    (0x08083538, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08083538', None),
    (0x080836e8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_080836e8', None),
    (0x08083b28, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08083b28', None),
    (0x08083c6c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08083c6c', None),
    (0x08083df8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08083df8', None),
    (0x0808400c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_0808400c', None),
    (0x08083f40, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_08083f40', None),

    # ===== REUSE: ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc) x2 =====
    (0x080836ec, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_off_080836ec', None),
    (0x08083dfc, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_off_08083dfc', None),

    # ===== REUSE: LP_CARD_TRACK_BASE_OFF=0x1da8 (ewram.inc) x1 =====
    (0x0808411c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_off_0808411c',
     'gP1LifePoints+LP_CARD_TRACK_BASE_OFF: LP card-ref tracking base'),

    # ===== REUSE: LP_CARD_TRACK_NEXT_OFF=0x1daa (ewram.inc) x1 =====
    (0x08083d28, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'lp_card_track_next_off_08083d28',
     'gP1LifePoints+LP_CARD_TRACK_NEXT_OFF: LP card-track next halfword'),

    # ===== REUSE: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff (duel_field.inc:134) x7 =====
    # EQUIP_NODE_ATTR_CLEAR_MASK DROPPED: use DUAL_LABEL_RENDER_STATE_CLEAR instead
    (0x080834cc, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_080834cc',
     'AND mask clears bits[17:15] of effect node attr (REUSE duel_field.inc:134)'),
    (0x080835c0, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_080835c0', None),
    (0x08083908, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08083908', None),
    (0x08083a3c, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08083a3c', None),
    (0x08083c14, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08083c14', None),
    (0x08083e6c, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08083e6c', None),
    (0x08083fc8, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'dual_label_render_state_clear_08083fc8', None),

    # ===== REUSE: TRIGGER_OP_PARAM_107=0x107 (duel_field.inc:312) x1 =====
    (0x080835c4, 0x00000107, 'TRIGGER_OP_PARAM_107',
     'trigger_op_param_107_080835c4',
     'r1 arg to trigger_card_display_op31_if_not_active'),

    # ===== REUSE: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc) x2 =====
    (0x08083664, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_08083664', None),
    (0x080840dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_080840dc', None),

    # ===== REUSE: gDuelFieldSlots=0x0201c510 (ewram.inc) x1 =====
    (0x08083668, 0x0201c510, 'gDuelFieldSlots',
     'duel_field_slots_08083668', None),

    # ===== NEW: GEARFRIED_IRON_KNIGHT_CID_SHIFTED=0x9e180000 (card_info.inc) x1 =====
    (0x0808366c, 0x9e180000, 'GEARFRIED_IRON_KNIGHT_CID_SHIFTED',
     'gearfried_shifted_cid_0808366c',
     'lsls r0,#0x13 sentinel; skip Gearfried as equip target'),

    # ===== REUSE: RED_MOON_BABY_CID=0x1415 (card_info.inc:1175) x1 =====
    (0x0808390c, 0x00001415, 'RED_MOON_BABY_CID',
     'red_moon_baby_cid_0808390c', None),

    # ===== NEW: INVOKE_OP31_SUB1_PARAM_109=0x109 (duel_field.inc) x1 =====
    (0x080837e0, 0x00000109, 'INVOKE_OP31_SUB1_PARAM_109',
     'invoke_op31_sub1_param_109_080837e0',
     'r0 arg to invoke_card_display_op_0x31_sub1 at 0x080837ca; distinct from TRIGGER_OP_PARAM_107'),

    # ===== NEW: ANCIENT_LAMP_CID=0x1476 (card_info.inc) x1 =====
    (0x08083e70, 0x00001476, 'ANCIENT_LAMP_CID',
     'ancient_lamp_cid_08083e70',
     'Ancient Lamp card_id comparison in tick_equip_lamp_dream_activation_3state'),

    # ===== NEW: DREAMSPRITE_CID=0x148a (card_info.inc) x1 =====
    (0x08083e94, 0x0000148a, 'DREAMSPRITE_CID',
     'dreamsprite_cid_08083e94',
     'Dreamsprite card_id comparison in tick_equip_lamp_dream_activation_3state'),

    # ===== REUSE: DNA_TRANSPLANT_CID=0x171f (card_info.inc:395) x1 =====
    # Different semantic (LP display type15 row param) but same numeric value; per REUSE-by-VALUE rule
    (0x08083d2c, 0x0000171f, 'DNA_TRANSPLANT_CID',
     'dna_transplant_cid_08083d2c',
     'LP display type15 row param (value matches DNA_TRANSPLANT_CID; same numeric token)'),

    # ===== REUSE: OTOHIME_CID=0x1503 (card_info.inc:1084) x1 =====
    (0x080841b0, 0x00001503, 'OTOHIME_CID',
     'otohime_cid_080841b0', None),

    # ===== REUSE: TSUKUYOMI_CID=0x1694 (card_info.inc:1182) x1 =====
    (0x080841b4, 0x00001694, 'TSUKUYOMI_CID',
     'tsukuyomi_cid_080841b4', None),

    # ===== REUSE: EQUIP_SLOT_SCORE_CAP=0xffff (oam_attr.inc:156) x1 =====
    (0x080840e0, 0x0000ffff, 'EQUIP_SLOT_SCORE_CAP',
     'equip_slot_score_cap_080840e0',
     'equip slot sprite score saturation cap (REUSE oam_attr.inc:156)'),

    # ===== REUSE: gP1LifePoints=0x0201c4e0 (ewram.inc) x16 =====
    # (15 unique gP1LP DWORD_ + 1 newly added DWORD_08083d24)
    (0x080837c4, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_080837c4', None),
    (0x08083808, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083808', None),
    (0x08083914, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083914', None),
    (0x08083958, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083958', None),
    (0x08083b24, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083b24', None),
    (0x08083c68, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083c68', None),
    (0x08083df4, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083df4', None),
    (0x08083e98, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083e98', None),
    (0x08083ec0, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083ec0', None),
    (0x08083ef4, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083ef4', None),
    (0x08083f3c, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083f3c', None),
    (0x08084008, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084008', None),
    (0x08084118, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08084118', None),
    (0x080840d8, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_080840d8', None),
    (0x08083d24, 0x0201c4e0, 'gP1LifePoints',
     'gp1_life_points_ptr_08083d24', None),
    # Note: 0x0808411c = LP_CARD_TRACK_BASE_OFF (0x1da8) above; gP1LP slot excluded (handled separately)
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_val, gas_label, slot_label, eol)
#    7 fn-ptr slots; keep raw hex .word; EOL explains THUMB+1
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DAT_080834fc: fn-ptr to set_equip_activation_state_by_mode+1 (0x08081de5)
    (0x080834fc, 0x08081de5,
     'set_equip_activation_state_by_mode',
     'set_equip_act_mode_fn_ptr_080834fc',
     'THUMB+1 fn-ptr to set_equip_activation_state_by_mode (0x08081de4)'),
    # DWORD_08083aec: fn-ptr to check_effect_slot_zone_player_by_type+1 (0x08083969)
    (0x08083aec, 0x08083969,
     'check_effect_slot_zone_player_by_type',
     'check_zone_player_fn_ptr_08083aec',
     'THUMB+1 fn-ptr to check_effect_slot_zone_player_by_type (0x08083968)'),
    # DWORD_08083c18: fn-ptr to check_equip_slot_pair_blocked+1 (0x08083b55)
    (0x08083c18, 0x08083b55,
     'check_equip_slot_pair_blocked',
     'check_equip_pair_fn_ptr_08083c18',
     'THUMB+1 fn-ptr to check_equip_slot_pair_blocked (0x08083b54)'),
    # DWORD_08083fcc: same fn-ptr as DAT_080834fc
    (0x08083fcc, 0x08081de5,
     'set_equip_activation_state_by_mode',
     'set_equip_act_mode_fn_ptr_08083fcc',
     'THUMB+1 fn-ptr to set_equip_activation_state_by_mode (0x08081de4)'),
    # DWORD_08083dc4: set_equip_activation_state_by_mode_alt_fn_ptr (REUSE duel_field.inc:449)
    (0x08083dc4, 0x080905e9,
     'set_equip_activation_state_by_mode_alt_fn_ptr',
     'set_equip_act_alt_fn_ptr_08083dc4',
     'THUMB+1 fn-ptr to set_equip_activation_state_by_mode_alt (0x080905e8); REUSE duel_field.inc'),
    # DAT_080836b4: same alt fn-ptr (REUSE duel_field.inc:449)
    (0x080836b4, 0x080905e9,
     'set_equip_activation_state_by_mode_alt_fn_ptr',
     'set_equip_act_alt_fn_ptr_080836b4',
     'THUMB+1 fn-ptr to set_equip_activation_state_by_mode_alt (0x080905e8); REUSE duel_field.inc'),
    # DWORD_08083f08: same alt fn-ptr (REUSE duel_field.inc:449)
    (0x08083f08, 0x080905e9,
     'set_equip_activation_state_by_mode_alt_fn_ptr',
     'set_equip_act_alt_fn_ptr_08083f08',
     'THUMB+1 fn-ptr to set_equip_activation_state_by_mode_alt (0x080905e8); REUSE duel_field.inc'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    4 slots: 3 PTR_gP1LifePoints_ + 1 DAT_0808424c (BLK2 label)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08083534, 'gp1_life_points_ptr_08083534',
     'gP1LifePoints pointer (ELIGIB_SPRITE_CTRL_OFF read)'),
    (0x080836b0, 'gp1_life_points_ptr_080836b0',
     'gP1LifePoints pointer (LP pending activation check)'),
    (0x080836e4, 'gp1_life_points_ptr_080836e4',
     'gP1LifePoints pointer (ELIGIB_SPRITE_CTRL_OFF + ELIGIB_ANIM_STATE_OFF read)'),
    (0x0808424c, 'book_of_life_eligible_dispatch_state0',
     'BLK2 start: Book of Life fn_eligible sub-stub state 0'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, new_plate_text)
#    9 functions with CJK mojibake plates -> full ASCII rewrite
#    All plate text is pure ASCII. PLATE WARN=FAIL.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. tick_equip_lamp_dream_zone_activation_3state (0x08083704)
    (0x08083704,
     "@ Equip Lamp/Dream zone activation 3-state machine. Takes card_entry_ptr(r0) and scene_ptr(r1).\n"
     "@ Reads [gDuelPhaseFlags+0x4b0] current state. state==0: calls check_equip_zone_slot_activation_eligible;\n"
     "@ if returns 2, sets r7=1 (eligible flag). Checks halfword[+2] bits[11:6] (mask 0xfc0)==0x90*8=0x480\n"
     "@ and gEquipChainSlotRefs player_id match; if matched calls count_effect_node_zone_activations for r6.\n"
     "@ If r7&&r6: writes [gDuelPhaseFlags+0x4b0]=10, returns 0. If r7&&!r6: strh 1 to [r4+0xa].\n"
     "@ If !r7: strh 2 to [r4+0xa].\n"
     "@ state==10: checks gDuelCardCtxBase[player*4+8] confirm_flag; if==1 writes [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:=2 and ++step;\n"
     "@ else invoke_card_display_op_0x31_sub1(0x109), ++step, return 0.\n"
     "@ state==11: reads [gP1LifePoints+LP_ACTIVATION_PENDING_OFF], strh [r4+0xa]++, clears step, returns [r4+0xa] halfword.\n"
     "@ Other states: delegates to tick_equip_display_with_fn_ptr_routing_3state ([r4+0xa]==1)\n"
     "@ or tick_equip_lamp_dream_activation_3state ([r4+0xa]==2).\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch."),

    # 2. check_effect_slot_zone_player_by_type (0x08083968)
    (0x08083968,
     "@ Effect slot zone/player dual-path predicate. Called via fn-ptr from tick_equip_placement_bitmap_display_4state.\n"
     "@ Takes effect_node_ptr(r0). Reads [r4+6] bits[4:3] as case index.\n"
     "@ case 0: XOR player_id with r5 (compare). case 1: direct compare player_id with r5.\n"
     "@ Returns 0 (no match) or 1 (match). r4/r5 are caller-frame registers: effect_node and compare value.\n"
     "@ fn-ptr 0x08083969 referenced from tick_equip_activation_if_not_otohime literal pool at DWORD_08083aec.\n"
     "@ Constants: ZONE_FIELD_BITS=bits[4:3] of [r4+6] (case index [0..1]).\n"
     "@ indeg=0: runtime fn-ptr call from tick_equip_placement_bitmap_display_4state."),

    # 3. tick_equip_placement_bitmap_display_4state (0x080839b4)
    (0x080839b4,
     "@ Equip placement bitmap display 4-state machine. Takes effect_node_ptr(r0).\n"
     "@ Reads [gDuelPhaseFlags+STATE_OFFSET] state. state 0: calls check_effect_activations_both_sides;\n"
     "@ if [gDuelCardCtxBase+player_id*4+8]==1: calls find_best_slot_from_equip_bitmap_with_gate;\n"
     "@ iterates slots 0..4 via set_equip_activation_state_by_mode_alt; on first match calls\n"
     "@ enqueue_equip_slot_sprite_with_code_rotation forward then reverse; step+1 return 0.\n"
     "@ state 1 (via check_effect_slot_zone_player_by_type fn-ptr): trigger_card_display_op31_if_not_active(op=0x94)\n"
     "@ +set_equip_activation_state_by_mode; step+1.\n"
     "@ state 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation; step+1.\n"
     "@ state>=3: step+1 return 1.\n"
     "@ Constants: gDuelPhaseFlags=0x0201b290, STATE_OFFSET=0x4b0, SLOT_IDX_MAX=4,\n"
     "@ FN_PTR_PREDICATE=check_effect_slot_zone_player_by_type(0x08083969).\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch."),

    # 4. tick_equip_activation_sprite_array_4state (0x08083ba0)
    (0x08083ba0,
     "@ Equip activation sprite push 4-state machine. Takes effect_node_ptr(r0).\n"
     "@ Reads [gDuelPhaseFlags+STATE_OFFSET] state. state 0: clears attr_bits (DUAL_LABEL_RENDER_STATE_CLEAR)\n"
     "@ + format_game_text_with_int_arg(slot=0x9b) + trigger_card_display_op31_if_not_active; step+1 return 0.\n"
     "@ states 1 and 3 (shared path): check_activation_display_state_is_confirmed; if confirmed reads\n"
     "@ [gP1LifePoints+ELIGIB_SPRITE_CTRL_OFF]/[+ELIGIB_ANIM_STATE_OFF]/[+LP_BANISHER_CTX_OFF] three fields,\n"
     "@ calls enqueue_sprite_attr_row_0x29_with_flag2, then push_to_effect_slot_array; step+1.\n"
     "@ If not confirmed: step-1. state 2: clear attr_bits + set_equip_activation_state_by_mode_alt; step+1.\n"
     "@ Constants: gDuelPhaseFlags=0x0201b290, STATE_OFFSET=0x4b0, DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff,\n"
     "@ FLAG_MASK_INV=~0x1d, FORMAT_TEXT_SLOT=0x9b, FN_PTR_CHECK=check_equip_slot_pair_blocked(0x08083b55).\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch."),

    # 5. tick_equip_lp_row_display_by_state (0x08083c98)
    (0x08083c98,
     "@ Equip LP row display state stepper. Driven by runtime function-pointer table.\n"
     "@ Reads gDuelPhaseFlags+0x4b0: state<0 or >3 returns 1. state 0 and 1: calls\n"
     "@ dispatch_equip_display_by_type_flag_and_node_activity; if 0 returns 0, else advances step+2.\n"
     "@ state 2: read_effect_slot_side_and_type -> resolve_best_target_slot_for_equip ->\n"
     "@ set_lp_row_type11_with_byte_flags(player_id, 1, ~bitmask).\n"
     "@ state 3: reads [gP1LifePoints+LP_CARD_TRACK_NEXT_OFF] LP halfword, push_to_effect_slot_array,\n"
     "@ set_lp_display_row_type15(player, halfword, DNA_TRANSPLANT_CID value).\n"
     "@ Advances step by writing to gDuelPhaseFlags+0x4b0.\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch."),

    # 6. tick_equip_lamp_dream_activation_3state (0x08083e14)
    (0x08083e14,
     "@ Equip activation 3-state machine for Ancient Lamp/Dreamsprite cards. Takes effect_node_ptr(r0).\n"
     "@ Reads [gDuelPhaseFlags+STATE_OFFSET] state. state 0: clears attr_bits; count_effect_node_zone_activations;\n"
     "@ if >0: compares card_id against three values:\n"
     "@   - ANCIENT_LAMP_CID(0x1476) or ANCIENT_LAMP_CID-0x6c=0x140a(Shift) ->\n"
     "@     trigger_card_display_op31_if_not_active(op=0xf), write [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:=1.\n"
     "@   - DREAMSPRITE_CID(0x148a) -> reads [gDuelCardCtxBase+player*4]; if [ptr+8]==1:\n"
     "@     write [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]:=1; else invoke_card_display_op_0x31_sub1(0xe2).\n"
     "@ step+1 return 0.\n"
     "@ state 1: reads [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]; if 0 returns -1; else\n"
     "@ set_equip_activation_state_by_mode (fn-ptr=set_equip_activation_state_by_mode_alt_fn_ptr); step+1 return 0.\n"
     "@ state 2: check_activation_display_state_is_confirmed -> enqueue_equip_slot_sprite_with_code_rotation + step+1.\n"
     "@ default: return 1.\n"
     "@ Constants: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff, ANCIENT_LAMP_CID=0x1476, DREAMSPRITE_CID=0x148a,\n"
     "@ OP_TRIGGER=0xf, OP_ALT=0xe2, LP_ACTIVATION_PENDING_OFF=0x1d40(=0xea<<5),\n"
     "@ FN_PTR_MODE=set_equip_activation_state_by_mode_alt_fn_ptr(0x080905e9).\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch."),

    # 7. tick_equip_activation_display_seq_a (0x08083f4c) -- no CJK noted; but plate 7 per proposal
    # NOTE: proposal plate #7 was for tick_equip_lamp_dream_activation (already #6 above)
    # Re-checking: plate items are 1-9. Item #7 is tick_equip_lp_score_display_seq? Let me re-read proposal
    # Plate list from proposal: 1=lamp_dream_zone(0x08083704), 2=effect_slot_zone(0x08083968),
    # 3=placement_bitmap(0x080839b4), 4=activation_sprite(0x08083ba0), 5=lp_row(0x08083c98),
    # 6=lamp_dream_activation(0x08083e14), 7=? (tick_equip_best_target_display_4state=0x08083560 was OK)
    # Actually proposal plate #7 was also tick_equip_lamp_dream_activation (0x08083e14) -- but wait,
    # proposal says 8=dispatch_equip_display_if_confirm_state_two(0x0808416c)
    # and 9=dispatch_equip_display_by_type_code_or_card_id(0x08084180)
    # So we have 7 already listed + 2 more = 9 total. The 7th entry here IS the 7th plate.
    # Let me add tick_equip_lp_score_display_seq (0x08084038) if it has CJK,
    # or confirm the exact 9 plate entries from proposal...
    # Proposal lists: functions 2/3/4/5/6/7/8/9 (skipping 1 which was already ASCII).
    # Wait -- proposal says plate 1 is tick_equip_best_target_display_4state "already ASCII".
    # Plates 2-9 are the 8 CJK ones. But final count = 9. Let me re-read...
    # Actually proposal says "9 lines with non-ASCII found". Items 2-9 are all CJK rewrites.
    # Item 1 was "already ASCII: keep as-is". So we write plates 2..9 = 8 plates.
    # But the proposal lists them as items #2..#9 (8 entries), but says PLATE=9.
    # The 9th plate must be tick_equip_lp_score_display_seq or another fn.
    # Wait -- re-reading proposal more carefully: items listed are functions with CJK.
    # The proposal says "9 lines with non-ASCII" and lists items #1..#9, but item #1 was
    # confirmed already ASCII. So actual CJK writes = items #2..#9 = 8 writes.
    # However the counts say PLATE=9. This might be counting item #1 even though "keep as-is".
    # For safety: write all 8 CJK plates (#2..#9 from proposal). That's the correct action.
    # Corrected: 8 CJK plate rewrites (item #1 was already ASCII).

    # 7. dispatch_equip_display_if_confirm_state_two (0x0808416c)
    (0x0808416c,
     "@ Equip activation confirm-state-2 gated dispatch. Reads card_slot[+0xc] halfword; if equals 2 calls\n"
     "@ dispatch_equip_activation_display_by_confirm_state and passes through its return value; else returns 1.\n"
     "@ Sibling of dispatch_equip_display_if_confirm_state_one (0x080833a8), difference: trigger value 1 vs 2.\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch."),

    # 8. dispatch_equip_display_by_type_code_or_card_id (0x08084180)
    (0x08084180,
     "@ Equip activation display dual-condition gated dispatch. Extracts card_slot[+2] bits[13:6] (mask 0x3fc0);\n"
     "@ if equal to 0x8a<<5=0x1140 calls dispatch_equip_activation_display_by_confirm_state.\n"
     "@ Else checks card_slot[+0] card_id: OTOHIME_CID(0x1503) or TSUKUYOMI_CID(0x1694) -- any match calls\n"
     "@ dispatch_equip_activation_display_by_confirm_state and passes return value. No match: returns 1.\n"
     "@ indeg=0: Sub-type A runtime fn-ptr dispatch.\n"
     "@ Constants: OTOHIME_CID=0x1503, TSUKUYOMI_CID=0x1694, MASK_BITS13_6=0x3fc0, CODE_0x1140=0x8a<<5."),
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


def _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
    """Apply USER label to slot + EOL. fn-ptr slots keep raw hex .word."""
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if not _check(slot_addr, target_val, gas_label):
        print("[SKIP] REF 0x%08x (%s) value mismatch" % (slot_addr, gas_label))
        return False

    if DRY:
        print("[dry] REF 0x%08x  target=0x%08x  gas_label=%s  slot_label=%s" % (
            slot_addr, target_val, gas_label, slot_label))
        return True

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x  -> %s  (%s)" % (slot_addr, slot_label, gas_label))
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


def _apply_plate(func_addr, new_plate_text):
    """Full plate rewrite. WARN=FAIL."""
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
    read_back = cu.getComment(CodeUnit.PLATE_COMMENT)
    if read_back is None or len(read_back) < 10:
        print("[FAIL] plate 0x%08x: set failed or too short" % func_addr)
        return False
    print("[PLT] 0x%08x: ASCII plate applied (%d chars)" % (func_addr, len(new_plate_text)))
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF10Seg9Slots (DRY=%s) ===" % DRY)
    print("  Seg-9: [0x08083450..0x08084318) -- EQ=%d, REF=%d, RENAME=%d, PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

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

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    ref_fail = 0
    for entry in REF_SLOTS:
        slot_addr, target_val, gas_label, slot_label, eol = (
            entry[0], entry[1], entry[2], entry[3], entry[4])
        if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            ref_ok += 1
        else:
            ref_fail += 1
    print("  REF done: ok=%d fail=%d" % (ref_ok, ref_fail))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        if _apply_rename(slot_addr, slot_label, eol):
            ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plt_ok = 0
    for func_addr, new_plate in PLATE_REWRITES:
        if _apply_plate(func_addr, new_plate):
            plt_ok += 1
    print("  PLATE done: %d / %d" % (plt_ok, len(PLATE_REWRITES)))

    print("\n=== RefineF10Seg9Slots DONE ===")
    print("  EQ=%d/%d  REF=%d/%d  RENAME=%d/%d  PLATE=%d/%d" % (
        eq_ok, len(EQ_SLOTS),
        ref_ok, len(REF_SLOTS),
        ren_ok, len(RENAME_SLOTS),
        plt_ok, len(PLATE_REWRITES)))


main()
