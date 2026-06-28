# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg3Slots.py -- file 12 Seg-3 [0x08095ba8, 0x08096a4c)
#   asm/12_equip_activation_scan.s slot symbolization
#   18 named functions (14 push-prologue + 4 bx-lr leaf), 0 ROM_INCBIN blocks.
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (116 DAT_ slots)
#   B. REF_SLOTS  -- none (0 slots)
#   C. RENAME_SLOTS -- PTR_gP1LifePoints_* -> gp1lp_ptr_* (28 slots)
#   D. PLATE_FULL_REWRITES -- 4 CJK plate -> ASCII full rewrite
#   E. PLATE_SUBSTR_FIXES  -- 4 substring FUN_ replacements in ASCII plates
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython UTF-8 mojibake risk).
# No ROM_INCBIN / disasm / carve in this segment.
#
# New constants (add to .inc files BEFORE running real mode):
#   duel_field.inc:
#     ZONE_PHASE_STATUS_OFF      = 0x00001c58
#     ZONE_EVAL_PHASE_CODE_OFF   = 0x00001bd4
#     ACTIVATION_ENTRY_CLR_BITS_11_6 = 0xfffff03f
#     ACTIVATION_ENTRY_CLR_BITS_14_6 = 0xffff803f
#     ACTIVATION_ENTRY_PTR_OFF   = 0x00001d7c
#   ewram.inc:
#     LP_ANIM_RESULT_OFF         = 0x00001d74
#     LP_ANIM_TRIGGER_SENTINEL   = 0x00000fee
#     EFFECT_ID_GENERIC_WILDCARD = 0x0000fffe

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
    # ---- Group B: DAT_ slots with EXISTING constants (REUSE) ----

    # ELIGIB_SPRITE_CTRL_OFF (ewram.inc, 0x00001d68) -- 10 slots
    (0x08095c1c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5c1c',
     'init_equip_card_sprite_row_entry: player_bit from [gP1LifePoints+0x1d68]'),
    (0x08095d08, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5d08',
     'init_lp_bar_slot_entry_from_state: [+0x1d68] sprite ctrl load'),
    (0x08095d74, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5d74',
     'dispatch_lp_bar_animation_step: [+0x1d68] sprite ctrl read'),
    (0x08095dcc, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5dcc',
     'apply_slot_equip_activation_if_lp_anim_phase: [+0x1d68] sprite ctrl'),
    (0x08095e14, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5e14',
     'dispatch_effect_slot_by_display_state: [+0x1d68] sprite ctrl'),
    (0x08095e60, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5e60',
     'tick_lp_bar_anim_step_display: [+0x1d68] sprite ctrl'),
    (0x08095eb8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_5eb8',
     'eval_spell_activation_flags_by_zone: [+0x1d68] sprite ctrl'),

    # ELIGIB_ANIM_STATE_OFF (ewram.inc, 0x00001d6c) -- 3 slots
    (0x08095c20, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_5c20',
     'init_equip_card_sprite_row_entry: base_slot_a from [+0x1d6c]'),
    (0x08095d78, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_5d78',
     'dispatch_lp_bar_animation_step: [+0x1d6c] anim state read'),
    (0x08095ebc, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_5ebc',
     'eval_spell_activation_flags_by_zone: [+0x1d6c] anim state'),

    # LP_BANISHER_CTX_OFF (ewram.inc, 0x00001d70) -- 3 slots
    (0x08095c24, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'lp_banisher_5c24',
     'init_equip_card_sprite_row_entry: slot_b from [+0x1d70]'),
    (0x08095d7c, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'lp_banisher_5d7c',
     'dispatch_lp_bar_animation_step: [+0x1d70] banisher ctx'),
    (0x08095dd0, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'lp_banisher_5dd0',
     'apply_slot_equip_activation_if_lp_anim_phase: [+0x1d70] banisher ctx'),

    # PLAYER_BLOCK_STRIDE (ewram.inc, 0x00000868) -- 8 slots
    (0x08095c28, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_5c28',
     'init_equip_card_sprite_row_entry: muls player offset'),
    (0x08096024, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6024',
     'eval_spell_activation_flags_by_zone: player block stride'),
    (0x08096168, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6168',
     'eval_spell_activation_flags_by_zone path2: player stride'),
    (0x080962a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_62a4',
     'setup_equip_slot_activation_entry: muls player block offset'),
    (0x080964fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_64fc',
     'setup_equip_slot_activation_entry_alt: player stride'),
    (0x08096568, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6568',
     'setup_equip_slot_activation_entry_alt path2: player stride'),
    (0x080967e8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_67e8',
     'eval_zone_activation_flags_by_type: player block stride'),
    (0x080968a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_68a4',
     'eval_zone_activation_flags_for_player: player stride'),

    # ELIGIB_CARD_ID_OFF (ewram.inc, 0x00001d44) -- 5 slots
    (0x08095c2c, 0x00001d44, 'ELIGIB_CARD_ID_OFF', 'eligib_card_id_5c2c',
     'init_equip_card_sprite_row_entry: [+0x1d44] card_id check'),
    (0x08095c60, 0x00001d44, 'ELIGIB_CARD_ID_OFF', 'eligib_card_id_5c60',
     'trigger_lp_bar_animation_if_ready: [+0x1d44] trigger_sentinel compare'),
    (0x08095cc4, 0x00001d44, 'ELIGIB_CARD_ID_OFF', 'eligib_card_id_5cc4',
     'trigger_lp_bar_animation_if_ready: [+0x1d44] sentinel field'),
    (0x08095e1c, 0x00001d44, 'ELIGIB_CARD_ID_OFF', 'eligib_card_id_5e1c',
     'dispatch_effect_slot_by_display_state: [+0x1d44] card_id load'),
    (0x08095e64, 0x00001d44, 'ELIGIB_CARD_ID_OFF', 'eligib_card_id_5e64',
     'tick_lp_bar_anim_step_display: [+0x1d44] card_id'),

    # ACTIVATION_STATE_A_OFF (duel_field.inc, 0x00001d48) -- 14 slots
    (0x08095c30, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_5c30',
     'init_equip_card_sprite_row_entry: [+0x1d48] activation state A'),
    (0x08095c98, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_5c98',
     'trigger_lp_bar_animation_if_ready: [+0x1d48] state A check'),
    (0x08095d0c, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_5d0c',
     'init_lp_bar_slot_entry_from_state: [+0x1d48] state A'),
    (0x08095d38, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_5d38',
     'dispatch_lp_bar_animation_step: [+0x1d48] state A'),
    (0x08095e20, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_5e20',
     'dispatch_effect_slot_by_display_state: [+0x1d48] state A'),
    (0x08096430, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_6430',
     'setup_equip_slot_activation_entry: stores 4 to [+0x1d48]'),
    (0x080964f8, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_64f8',
     'setup_equip_slot_activation_entry_alt: [+0x1d48] state A'),
    (0x0809636c, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_636c',
     'setup_equip_slot_activation_entry: [+0x1d48] state A path2'),
    (0x08096574, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_6574',
     'setup_equip_slot_activation_entry_alt: [+0x1d48] state A path2'),
    (0x0809663c, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_663c',
     'setup_equip_slot_activation_entry_alt: [+0x1d48] stores 0x10'),
    (0x080966d0, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_66d0',
     'eval_zone_activation_flags_by_type: [+0x1d48] state A check'),
    (0x08096728, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_6728',
     'eval_zone_activation_flags_for_player: [+0x1d48] state A'),
    (0x08096784, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_6784',
     'eval_zone_activation_flags_for_player path2: [+0x1d48] state A'),

    # ELIGIB_STATE_CTRL_OFF (ewram.inc, 0x00001d54) -- 8 slots
    # Note: 0x08095c9c holds 0x1d54, not 0x1d48 (proposal Group B typo actstate_a_5c98)
    (0x08095c9c, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5c9c',
     'trigger_lp_bar_animation_if_ready: [+0x1d54] eligib state ctrl'),
    (0x08095d40, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5d40',
     'dispatch_lp_bar_animation_step: [+0x1d54] state ctrl clear'),
    (0x08095d80, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5d80',
     'init_lp_bar_slot_entry_from_state: [+0x1d54] state ctrl'),
    (0x08095ec0, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5ec0',
     'eval_spell_activation_flags_by_zone: [+0x1d54] state ctrl'),
    (0x08095e6c, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5e6c',
     'tick_lp_bar_anim_step_display: [+0x1d54] state ctrl'),
    (0x08095f48, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5f48',
     'eval_spell_activation_flags_by_zone entry: [+0x1d54]'),
    (0x08095f8c, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5f8c',
     'eval_spell_activation_flags_by_zone: [+0x1d54] state ctrl read'),
    (0x08095fdc, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_5fdc',
     'eval_spell_activation_flags_by_zone path2: [+0x1d54]'),

    # LP_PLAYER_SIDE_CACHE_OFF (ewram.inc, 0x00001d64) -- 7 slots
    (0x08095c64, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_5c64',
     'trigger_lp_bar_animation_if_ready: [+0x1d64] player_side cache'),
    (0x08096808, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_6808',
     'eval_zone_activation_flags_by_type: [+0x1d64] player side cache'),
    (0x080968c4, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_68c4',
     'eval_zone_activation_flags_for_player: [+0x1d64] player side'),
    (0x080968f0, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_68f0',
     'check_zone_slot_card_activatable: [+0x1d64] player side cache'),
    (0x080969bc, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_69bc',
     'write_card_display_ctx_fields: [+0x1d64] player side'),
    (0x08096a00, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_6a00',
     'init_zone_activation_display_fields: [+0x1d64] player side'),
    (0x08096a44, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_6a44',
     'init_zone_activation_display_state_p1_entry: [+0x1d64] player side'),
    (0x080967c0, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_67c0',
     'eval_zone_activation_flags_by_type: [+0x1d64] player side read'),

    # P1LP_TIMER_OFF (ewram.inc, 0x00001cec) -- 1 slot
    (0x08095f88, 0x00001cec, 'P1LP_TIMER_OFF', 'p1lp_timer_5f88',
     'eval_spell_activation_flags_by_zone: [gP1LifePoints+0x1cec] timer check'),

    # gP1FieldArrayCBase (ewram.inc, 0x0201c600) -- 1 slot
    (0x08096028, 0x0201c600, 'gP1FieldArrayCBase', 'gp1fcarrayc_6028',
     'eval_spell_activation_flags_by_zone: gP1FieldArrayCBase base for zone scan'),

    # gDuelCardCtxBase (ewram.inc, 0x0201e2a0) -- 8 slots
    (0x0809602c, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_602c',
     'eval_spell_activation_flags_by_zone: [gDuelCardCtxBase+4]=player_id'),
    (0x08096360, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6360',
     'setup_equip_slot_activation_entry: [+4] active_player XOR check'),
    (0x080963ac, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_63ac',
     'setup_equip_slot_activation_entry: [+4] player_id for blocker check'),
    (0x08096570, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6570',
     'setup_equip_slot_activation_entry_alt: [+4] paired entry player match'),
    (0x08096630, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6630',
     'setup_equip_slot_activation_entry_alt: [+4] player_id check path2'),
    (0x080966dc, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_66dc',
     'eval_zone_activation_flags_by_type: [+4] active_player'),
    (0x08096950, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6950',
     'check_zone_slot_card_activatable: [+4] player_id'),
    (0x080969c0, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_69c0',
     'init_zone_activation_display_fields: [+4] player_id write'),
    (0x08096a04, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6a04',
     'init_zone_activation_display_state_p1_entry: [+4] player_id'),
    (0x08096a48, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6a48',
     'init_zone_activation_display_state_p1_entry: [+4] player_id second ref'),
    (0x080966e4, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_blk2_66e4',
     'eval_zone_activation_flags_by_type: [gP1LifePoints+0x1cf4] P2 LP block2'),

    # PLAYER_BLOCK_STRIDE (already listed above, skipping duplicates)

    # gDuelFieldSlots (ewram.inc, 0x0201c510) -- 3 slots
    (0x080962a8, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_62a8',
     'setup_equip_slot_activation_entry: gDuelFieldSlots zone slot base'),
    (0x08096500, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_6500',
     'setup_equip_slot_activation_entry_alt: gDuelFieldSlots base'),
    (0x0809656c, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_656c',
     'setup_equip_slot_activation_entry_alt path2: gDuelFieldSlots base'),

    # EQUIP_PHASE_STATE_OFF (duel_field.inc, 0x00001cc4) -- 2 slots
    (0x08096384, 0x00001cc4, 'EQUIP_PHASE_STATE_OFF', 'eqphase_state_6384',
     'setup_equip_slot_activation_entry: [gDuelFieldSlots+0x1cc4] equip phase state'),
    (0x080966d4, 0x00001cc4, 'EQUIP_PHASE_STATE_OFF', 'eqphase_state_66d4',
     'eval_zone_activation_flags_by_type: [+0x1cc4] equip phase state'),

    # DUEL_ACTIVE_PLAYER_OFF (duel_field.inc, 0x00001cb8) -- 1 slot
    (0x080966d8, 0x00001cb8, 'DUEL_ACTIVE_PLAYER_OFF', 'duel_active_plyr_66d8',
     'eval_zone_activation_flags_by_type: [gP1LifePoints+0x1cb8] active player'),

    # FIELD_SPELL_B_EFFECT_ID (card_info.inc, 0x00001407) -- 2 slots
    (0x08096260, 0x00001407, 'FIELD_SPELL_B_EFFECT_ID', 'fspell_b_eid_6260',
     'eval_spell_activation_flags_by_zone: check_value_in_slot_chain(0,0xb,0x1407)'),
    (0x08096788, 0x00001407, 'FIELD_SPELL_B_EFFECT_ID', 'fspell_b_eid_6788',
     'eval_zone_activation_flags_by_type: FIELD_SPELL_B guard check'),

    # SPECIAL_EQUIP_TARGET_CID_A (card_info.inc, 0x0000131e) -- 1 slot
    (0x080966e8, 0x0000131e, 'SPECIAL_EQUIP_TARGET_CID_A', 'sp_eq_cid_a_66e8',
     'eval_zone_activation_flags_by_type: cmp card_id vs 0x131e special target gate'),

    # P2LP_BLOCK2_OFF_1CF4 (ewram.inc, 0x00001cf4) -- 1 slot
    (0x08096704, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_blk2_6704',
     'eval_zone_activation_flags_by_type: [gP1LifePoints+0x1cf4] P2 LP block2'),

    # SPRITE_ATTR_DUEL_PHASE_P2_B (duel_field.inc, 0x00008023) -- 1 slot
    (0x08095fd4, 0x00008023, 'SPRITE_ATTR_DUEL_PHASE_P2_B', 'sprite_p2b_5fd4',
     'eval_spell_activation_flags_by_zone: sprite attr P2B flag'),

    # LP_BAR_ANIM_STATE_OFF (ewram.inc, 0x000004cc) -- 1 slot
    (0x08096834, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_sta_6834',
     'eval_zone_activation_flags_by_type: [gDuelPhaseFlags+0x4cc] LP bar anim state'),

    # gDuelPhaseFlags (ewram.inc, 0x0201b290) -- 2 slots
    (0x08095d04, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflag_5d04',
     'trigger_lp_bar_animation_if_ready: gDuelPhaseFlags sprite buf flag addr'),
    (0x080967c4, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflag_67c4',
     'eval_zone_activation_flags_by_type: gDuelPhaseFlags base for LP anim state'),

    # ACTIVATION_STATE_B_OFF (duel_field.inc, 0x00001d78) -- 6 slots
    (0x080960f8, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_60f8',
     'eval_spell_activation_flags_by_zone: [+0x1d78] state B write'),
    (0x08096124, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_6124',
     'eval_spell_activation_flags_by_zone: [+0x1d78] state B path2'),
    (0x080961a4, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_61a4',
     'eval_spell_activation_flags_by_zone: [+0x1d78] state B path3'),
    (0x080963b4, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_63b4',
     'setup_equip_slot_activation_entry: [+0x1d78] state B'),
    (0x080966ec, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_66ec',
     'eval_zone_activation_flags_by_type: [+0x1d78] state B read'),
    (0x08096708, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_6708',
     'eval_zone_activation_flags_by_type: [+0x1d78] state B store'),

    # ACTIVATION_STATE_C_OFF (duel_field.inc, 0x00001d4c) -- 3 slots
    (0x080969b4, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_69b4',
     'write_card_display_ctx_fields: [+0x1d4c] state C clear'),
    (0x080969f4, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_69f4',
     'init_zone_activation_display_fields: [+0x1d4c] state C'),
    (0x08096a38, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6a38',
     'init_zone_activation_display_state_p1_entry: [+0x1d4c] state C'),
    (0x08096984, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6984',
     'dispatch_zone_effect_by_slot: [+0x1d4c] state C check'),

    # ELIGIB_ACT_COUNT_OFF (ewram.inc, 0x00001d58) -- 2 slots
    (0x080969fc, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_actcnt_69fc',
     'init_zone_activation_display_fields: [+0x1d58] count clear'),
    (0x08096a40, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_actcnt_6a40',
     'init_zone_activation_display_state_p1_entry: [+0x1d58] count clear'),

    # LP_PLAYER_SIDE_CACHE_OFF (additional slot)
    (0x08096860, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_6860',
     'eval_zone_activation_flags_for_player: [+0x1d64] player side cache'),

    # ---- Group C: NEW constants ----

    # LP_ANIM_RESULT_OFF (ewram.inc NEW, 0x00001d74) -- 2 slots
    (0x08095dd4, 0x00001d74, 'LP_ANIM_RESULT_OFF', 'lp_anim_result_5dd4',
     'apply_slot_equip_activation_if_lp_anim_phase: [+0x1d74] lp anim result store'),
    (0x08095e18, 0x00001d74, 'LP_ANIM_RESULT_OFF', 'lp_anim_result_5e18',
     'dispatch_effect_slot_by_display_state: [+0x1d74] result field'),

    # EFFECT_ID_GENERIC_WILDCARD (ewram.inc NEW, 0x0000fffe) -- 2 slots
    (0x08095f08, 0x0000fffe, 'EFFECT_ID_GENERIC_WILDCARD', 'effect_id_wc_5f08',
     'dispatch_effect_slot_by_display_state: passes 0xfffe as effect_id wildcard'),
    (0x08096968, 0x0000fffe, 'EFFECT_ID_GENERIC_WILDCARD', 'effect_id_wc_6968',
     'dispatch_zone_effect_by_slot: passes EFFECT_ID_GENERIC_WILDCARD to dispatch_effect_handler_by_card_id'),

    # LP_ANIM_TRIGGER_SENTINEL (ewram.inc NEW, 0x00000fee) -- 1 slot
    (0x08095cc8, 0x00000fee, 'LP_ANIM_TRIGGER_SENTINEL', 'lp_anim_sentinel_5cc8',
     'trigger_lp_bar_animation_if_ready: cmp [+ELIGIB_CARD_ID_OFF] vs 0x0fee sentinel'),

    # ZONE_PHASE_STATUS_OFF (duel_field.inc NEW, 0x00001c58) -- 6 slots
    (0x08096050, 0x00001c58, 'ZONE_PHASE_STATUS_OFF', 'zone_phase_sta_6050',
     'eval_spell_activation_flags_by_zone: [gDuelFieldSlots+0x1c58] zone phase status write'),
    (0x08096070, 0x00001c58, 'ZONE_PHASE_STATUS_OFF', 'zone_phase_sta_6070',
     'eval_spell_activation_flags_by_zone: [+0x1c58] status path2'),
    (0x0809608c, 0x00001bd4, 'ZONE_EVAL_PHASE_CODE_OFF', 'zone_eval_phase_608c',
     'eval_spell_activation_flags_by_zone: [gDuelFieldSlots+0x1bd4] zone_phase_code; cmp 2/3/4 dispatch'),
    (0x080961c0, 0x00001c58, 'ZONE_PHASE_STATUS_OFF', 'zone_phase_sta_61c0',
     'eval_spell_activation_flags_by_zone: [+0x1c58] path3 status write'),
    (0x080961d8, 0x00001c58, 'ZONE_PHASE_STATUS_OFF', 'zone_phase_sta_61d8',
     'eval_spell_activation_flags_by_zone: [+0x1c58] path4 status write'),
    (0x08096208, 0x00001c58, 'ZONE_PHASE_STATUS_OFF', 'zone_phase_sta_6208',
     'eval_spell_activation_flags_by_zone: [+0x1c58] path5 status write'),
    (0x0809625c, 0x00001c58, 'ZONE_PHASE_STATUS_OFF', 'zone_phase_sta_625c',
     'eval_spell_activation_flags_by_zone: [+0x1c58] path6 status write'),

    # ACTIVATION_ENTRY_CLR_BITS_11_6 (duel_field.inc NEW, 0xfffff03f) -- 3 slots
    (0x08096364, 0xfffff03f, 'ACTIVATION_ENTRY_CLR_BITS_11_6', 'act_entry_clr_11_6_6364',
     'setup_equip_slot_activation_entry: ands r0,r3 clears bits[11:6] of activation entry halfword [+2]'),
    (0x08096504, 0xfffff03f, 'ACTIVATION_ENTRY_CLR_BITS_11_6', 'act_entry_clr_11_6_6504',
     'setup_equip_slot_activation_entry_alt: clears bits[11:6] of entry halfword'),
    (0x08096634, 0xfffff03f, 'ACTIVATION_ENTRY_CLR_BITS_11_6', 'act_entry_clr_11_6_6634',
     'setup_equip_slot_activation_entry_alt path2: clears bits[11:6]'),

    # ACTIVATION_ENTRY_CLR_BITS_14_6 (duel_field.inc NEW, 0xffff803f) -- 3 slots
    (0x08096368, 0xffff803f, 'ACTIVATION_ENTRY_CLR_BITS_14_6', 'act_entry_clr_14_6_6368',
     'setup_equip_slot_activation_entry: ands r0,r3 clears bits[14:6] of activation entry halfword [+4]'),
    (0x08096508, 0xffff803f, 'ACTIVATION_ENTRY_CLR_BITS_14_6', 'act_entry_clr_14_6_6508',
     'setup_equip_slot_activation_entry_alt: clears bits[14:6] of entry halfword'),
    (0x08096638, 0xffff803f, 'ACTIVATION_ENTRY_CLR_BITS_14_6', 'act_entry_clr_14_6_6638',
     'setup_equip_slot_activation_entry_alt path2: clears bits[14:6]'),

    # ACTIVATION_ENTRY_PTR_OFF (duel_field.inc NEW, 0x00001d7c) -- 3 slots
    (0x080969b8, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_69b8',
     'write_card_display_ctx_fields: [gP1LifePoints+0x1d7c]:=0 zone_eval_fn ptr field'),
    (0x080969f8, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_69f8',
     'init_zone_activation_display_fields: [+0x1d7c]:=r0 zone_eval_fn callback ptr'),
    (0x08096a3c, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_6a3c',
     'init_zone_activation_display_state_p1_entry: [+0x1d7c] ptr field store'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none for Seg-3
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    All 28 PTR_gP1LifePoints_* -> gp1lp_ptr_*
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08095c18, 'gp1lp_ptr_95c18', None),
    (0x08095c94, 'gp1lp_ptr_95c94', None),
    (0x08095cc0, 'gp1lp_ptr_95cc0', None),
    (0x08095d3c, 'gp1lp_ptr_95d3c', None),
    (0x08095d70, 'gp1lp_ptr_95d70', None),
    (0x08095da8, 'gp1lp_ptr_95da8', None),
    (0x08095e10, 'gp1lp_ptr_95e10', None),
    (0x08095e68, 'gp1lp_ptr_95e68', None),
    (0x08095eb4, 'gp1lp_ptr_95eb4', None),
    (0x08095ee4, 'gp1lp_ptr_95ee4', None),
    (0x08095f64, 'gp1lp_ptr_95f64', None),
    (0x08095fd8, 'gp1lp_ptr_95fd8', None),
    (0x080960f4, 'gp1lp_ptr_960f4', None),
    (0x08096120, 'gp1lp_ptr_96120', None),
    (0x08096164, 'gp1lp_ptr_96164', None),
    (0x080963b0, 'gp1lp_ptr_963b0', None),
    (0x080966e0, 'gp1lp_ptr_966e0', None),
    (0x080967bc, 'gp1lp_ptr_967bc', None),
    (0x080967e4, 'gp1lp_ptr_967e4', None),
    (0x0809685c, 'gp1lp_ptr_9685c', None),
    (0x080968a0, 'gp1lp_ptr_968a0', None),
    (0x080968ec, 'gp1lp_ptr_968ec', None),
    (0x08096928, 'gp1lp_ptr_96928', None),
    (0x0809694c, 'gp1lp_ptr_9694c', None),
    (0x08096980, 'gp1lp_ptr_96980', None),
    (0x080969b0, 'gp1lp_ptr_969b0', None),
    (0x080969f0, 'gp1lp_ptr_969f0', None),
    (0x08096a34, 'gp1lp_ptr_96a34', None),
]

# ---------------------------------------------------------------------------
# D. PLATE_FULL_REWRITES: (func_addr, new_plate_text)
#    Full plate replacement (for CJK-corrupted plates). Pure ASCII, <=500 chars.
# ---------------------------------------------------------------------------
PLATE_FULL = [
    # 0x08096264 setup_equip_slot_activation_entry (L4471, 480 chars)
    (0x08096264,
     "Builds one equip-activation entry in the 0x18-byte stack buffer. r0=player_side, r1=slot_idx, r2=zone_slot. Guard: slot_idx<=4. If active_player (gDuelCardCtxBase+4) XOR 1 != player_side: check_card_field5_is_nonzero, slot[+8] chain_head nonzero, check_card_id_is_equip_blocker. memset(buf,0,0x18): writes card_id/player_bit/zone_code/attr_bits; stores 4 to [gP1LifePoints+ACTIVATION_STATE_A_OFF]; calls eval_equip_activation_for_slot. Returns 0x8 if activatable, else 0. indeg=1."),

    # 0x0809650c setup_equip_slot_activation_entry_alt (L4819, 494 chars)
    (0x0809650c,
     "Structural symmetric variant of setup_equip_slot_activation_entry (indeg=1), called by dispatch_zone_activation_by_state. r0=player_side, r1=slot_idx, r2=zone_slot. If find_paired_zone_entry_for_card finds pair and player==gDuelCardCtxBase+4: writes [gP1LifePoints+ACTIVATION_STATE_A_OFF]:=0x10. Else: checks eligibility, memset(buf,0,0x18), builds entry, calls eval_equip_activation_for_slot. field6==0x16/0x17: build_zone_activation_entry_blocked / _equip. Returns 0x8 if activatable, else 0."),

    # 0x0809678c eval_zone_activation_flags_by_type (L5148, 448 chars)
    (0x0809678c,
     "Evaluates zone_type (r1) activation flags for a single zone (indeg=1). Zone 0xb (FIELD_SPELL_ZONE): LP threshold check via gP1LifePoints[player*0x868+0xc], then setup_equip_context_for_zone_activation; success sets r6|=0x8. Zones 0xc..0xf: check_zone_slot_card_activatable -> dispatch_zone_effect_by_slot, OR into r6; opposite player and zone==0xd: r6|=0x1000. Other: setup_equip_context_for_slot_activation. Returns r6 (combined activation flags)."),

    # 0x08096954 dispatch_zone_effect_by_slot (L5396, 297 chars)
    (0x08096954,
     "Minimal dispatch leaf: moves r1 (slot_idx) to r2, passes EFFECT_ID_GENERIC_WILDCARD (0xfffe) as r1 to dispatch_effect_handler_by_card_id. Returns 0x8 (activatable flag) if callee returns nonzero, else 0. indeg=2; callers: eval_zone_activation_flags_by_type + eval_zone_activation_flags_for_player."),
]

# ---------------------------------------------------------------------------
# E. PLATE_SUBSTR_FIXES: (func_addr, old_sub, new_sub)
#    Substring replace in existing ASCII plates. Pure ASCII.
# ---------------------------------------------------------------------------
PLATE_SUBSTR = [
    # L3561 init_equip_card_sprite_row_entry plate: FUN_0804ce78 -> dispatch_card_eligibility_state_machine
    (0x08095ba8, 'FUN_0804ce78', 'dispatch_card_eligibility_state_machine'),
    # L3690 trigger_lp_bar_animation_if_ready plate: FUN_0804ce78 -> dispatch_card_eligibility_state_machine
    (0x08095ca0, 'FUN_0804ce78', 'dispatch_card_eligibility_state_machine'),
    # L3814 dispatch_lp_bar_animation_step plate: FUN_0804ce78 -> dispatch_card_eligibility_state_machine
    (0x08095d84, 'FUN_0804ce78', 'dispatch_card_eligibility_state_machine'),
    # L5499 init_zone_activation_display_state_p1_entry plate:
    #   FUN_08097bec -> check_equip_target_slot_eligibility
    #   FUN_08098020 -> dispatch_equip_slot_display_state_by_phase internal branch @ 0x08098020
    (0x08096a08, 'FUN_08097bec', 'check_equip_target_slot_eligibility'),
    (0x08096a08, 'FUN_08098020', 'dispatch_equip_slot_display_state_by_phase internal branch @ 0x08098020'),
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
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value & 0xFFFFFFFF), slot_label))
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

def _apply_plate_full(func_addr, new_text):
    """Full plate replacement. Fail if not ASCII."""
    for ch in new_text:
        if ord(ch) > 127:
            print("[FAIL] plate_full 0x%08x: non-ASCII char U+%04x" % (func_addr, ord(ch)))
            return False
    if len(new_text) > 500:
        print("[WARN] plate_full 0x%08x: length %d > 500" % (func_addr, len(new_text)))

    if DRY:
        print("[dry] PLATE_FULL 0x%08x: len=%d" % (func_addr, len(new_text)))
        return True

    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate_full 0x%08x: no code unit" % func_addr)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
    print("[PLT] 0x%08x: full rewrite len=%d" % (func_addr, len(new_text)))
    return True

def _apply_plate_fix(func_addr, old_sub, new_sub):
    """Substring replace in plate comment. FAIL if not found."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate_fix 0x%08x: no code unit" % func_addr)
        return False

    current = cu.getComment(CodeUnit.PLATE_COMMENT)
    if current is None:
        print("[FAIL] plate_fix 0x%08x: no plate comment" % func_addr)
        return False

    if old_sub not in current:
        print("[FAIL] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_sub))
        return False

    if DRY:
        print("[dry] PLATE_SUB 0x%08x: '%s' -> '%s'" % (func_addr, old_sub, new_sub))
        return True

    new_plate = current.replace(old_sub, new_sub)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PLT] 0x%08x: replaced '%s' -> '%s'" % (func_addr, old_sub, new_sub))
    return True

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF12Seg3Slots (DRY=%s) ===" % DRY)
    print("  Seg-3: 0x08095ba8..0x08096a4c, file 12 equip_activation_scan")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FULL=%d  PLATE_SUB=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL), len(PLATE_SUBSTR)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_skip = 0
    seen_slots = {}
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if slot_addr in seen_slots:
            print("[SKIP-DUP] 0x%08x already processed" % slot_addr)
            continue
        seen_slots[slot_addr] = slot_label
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d (skip_dup=%d)" % (eq_ok, eq_skip))

    # B. REF_SLOTS (none)
    print("\n--- B. REF_SLOTS (%d) --- none" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. PLATE_FULL
    print("\n--- D. PLATE_FULL_REWRITES (%d) ---" % len(PLATE_FULL))
    plate_full_ok = 0
    plate_full_fail = 0
    for func_addr, new_text in PLATE_FULL:
        if _apply_plate_full(func_addr, new_text):
            plate_full_ok += 1
        else:
            plate_full_fail += 1
    print("  PLATE_FULL done: ok=%d fail=%d" % (plate_full_ok, plate_full_fail))

    # E. PLATE_SUBSTR
    print("\n--- E. PLATE_SUBSTR_FIXES (%d) ---" % len(PLATE_SUBSTR))
    plate_sub_ok = 0
    plate_sub_fail = 0
    for func_addr, old_sub, new_sub in PLATE_SUBSTR:
        if _apply_plate_fix(func_addr, old_sub, new_sub):
            plate_sub_ok += 1
        else:
            plate_sub_fail += 1
    print("  PLATE_SUB done: ok=%d fail=%d" % (plate_sub_ok, plate_sub_fail))

    if plate_full_fail > 0 or plate_sub_fail > 0:
        print("[WARN] plate failures detected -- check stale FUN_ coverage")

    print("\n=== RefineF12Seg3Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE_FULL_ok=%d  PLATE_SUB_ok=%d  FAIL=%d" % (
        eq_ok, len(RENAME_SLOTS), plate_full_ok, plate_sub_ok,
        plate_full_fail + plate_sub_fail))

main()
