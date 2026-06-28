# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg4Slots.py -- file 12 Seg-4 [0x08096a4c, 0x08097828)
#   asm/12_equip_activation_scan.s slot symbolization + func rename + plate fixes.
#   26 function entries (22 named + 4 SUB_), 1 ROM_INCBIN block (0x96eec/0x34, Sec 5.1).
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (109 slots: 95 DAT_ + 14 DWORD_)
#   B. REF_SLOTS  -- 2 switchD base-pointer slots (USER-label + DATA-ref)
#   C. RENAME_SLOTS -- 15 PTR_gP1LifePoints_* -> gp1lp_ptr_*
#   D. FUNC_RENAME  -- 4 SUB_ -> semantic names
#   E. PLATE_FULL   -- 4 CJK mojibake plate full rewrites (pure ASCII, <=500 chars)
#   F. PLATE_SUBSTR -- 11 stale FUN_ substring replacements in existing plates
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython UTF-8 mojibake risk).
# ROM_INCBIN block 0x96eec/0x34 is Sec 5.1 (orphan); not disassembled here.
#
# New constants (add to .inc files BEFORE running real mode):
#   duel_field.inc:
#     EQUIP_CHAIN_CANCEL_OFF          = 0x00001d30
#     EQUIP_ACTIVATION_HANDLER_TABLE  = 0x09e47560
#     APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB = 0x08097025
#   oam_attr.inc:
#     OAM_EQUIP_ZONE_SPRITE_P2_18     = 0x00008018
#     OAM_EQUIP_ZONE_SPRITE_P2_0F     = 0x0000800f
#   card_info.inc:
#     FROZEN_SOUL_CID                 = 0x000016a1
#     GREAT_LONG_NOSE_CID             = 0x00001502
#     DD_BORDERLINE_CID               = 0x000016d4
#     EARTHBOUND_INVITATION_CID       = 0x0000177a

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
import ghidra.program.model.data as DataTypes

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
    # ---- Group A: REUSE -- gP1LifePoints offsets ----

    # ACTIVATION_STATE_C_OFF (duel_field.inc, 0x00001d4c)
    (0x08096aa0, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6aa0',
     'set_equip_activation_state_by_mode: [gP1LifePoints+0x1d4c] activation state C'),
    (0x08096b04, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6b04',
     'set_equip_activation_state_by_mode_alt: [+0x1d4c] state C'),
    (0x08096b74, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6b74',
     'dispatch_zone_activation_by_state: [+0x1d4c]-1 for 10-case switch'),
    (0x08096ec8, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6ec8',
     'zero_duel_lp_display_counters: [+0x1d4c] state C check'),
    (0x08096ee4, 0x00001d4c, 'ACTIVATION_STATE_C_OFF', 'actstate_c_6ee4',
     'zero_duel_lp_display_counters pool: ACTIVATION_STATE_C_OFF'),

    # ACTIVATION_ENTRY_PTR_OFF (duel_field.inc, 0x00001d7c)
    (0x08096aa4, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_6aa4',
     'set_equip_activation_state_by_mode: [+0x1d7c] activation entry ptr field'),
    (0x08096b08, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_6b08',
     'set_equip_activation_state_by_mode_alt: [+0x1d7c] activation entry ptr'),
    (0x08096dc4, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_6dc4',
     'dispatch_zone_activation_by_state: [+0x1d7c] entry ptr case7'),
    (0x08096df4, 0x00001d7c, 'ACTIVATION_ENTRY_PTR_OFF', 'act_entry_ptr_6df4',
     'dispatch_zone_activation_by_state: [+0x1d7c] entry ptr case8/9/10'),

    # ELIGIB_ACT_COUNT_OFF (ewram.inc, 0x00001d58)
    (0x08096aa8, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_actcnt_6aa8',
     'set_equip_activation_state_by_mode: [+0x1d58] eligib act count write'),
    (0x08096b0c, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_actcnt_6b0c',
     'set_equip_activation_state_by_mode_alt: [+0x1d58] eligib act count'),

    # LP_PLAYER_SIDE_CACHE_OFF (ewram.inc, 0x00001d64)
    (0x08096aac, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_6aac',
     'set_equip_activation_state_by_mode: [+0x1d64] player side cache'),
    (0x08096b10, 0x00001d64, 'LP_PLAYER_SIDE_CACHE_OFF', 'lp_plyrside_6b10',
     'set_equip_activation_state_by_mode_alt: [+0x1d64] player side cache'),

    # ELIGIB_STATE_CTRL_OFF (ewram.inc, 0x00001d54)
    (0x08096b38, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_6b38',
     'check_activation_display_state_is_confirmed: [+0x1d54] eligib state ctrl'),

    # LP_EQUIP_STATE_B_OFF (ewram.inc, 0x00001d50)
    (0x08096b70, 0x00001d50, 'LP_EQUIP_STATE_B_OFF', 'lp_eq_state_b_6b70',
     'dispatch_zone_activation_by_state: [+0x1d50] LP equip state B guard'),

    # ACTIVATION_STATE_B_OFF (duel_field.inc, 0x00001d78)
    (0x08096e10, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'actstate_b_6e10',
     'init_duel_zone_target_slot_refs: [+0x1d78] activation state B'),

    # ELIGIB_SPRITE_CTRL_OFF (ewram.inc, 0x00001d68)
    (0x08096eb4, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_6eb4',
     'zero_duel_lp_display_counters: [+0x1d68] sprite ctrl clear'),
    (0x08097098, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_7098',
     'submit_equip_slot_sprite_with_ref_a: [+0x1d68] sprite ctrl read'),
    (0x080970c8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_70c8',
     'submit_equip_slot_sprite_with_ref_b: [+0x1d68] sprite ctrl read'),

    # ELIGIB_ANIM_STATE_OFF (ewram.inc, 0x00001d6c)
    (0x08096eb8, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_6eb8',
     'zero_duel_lp_display_counters: [+0x1d6c] anim state clear'),

    # ELIGIB_STATE_CTRL_OFF second occurrence in zero_duel_lp_display_counters
    (0x08096ebc, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_6ebc',
     'zero_duel_lp_display_counters: [+0x1d54] eligib state ctrl clear'),

    # ELIGIB_CARD_ID_OFF (ewram.inc, 0x00001d44)
    (0x08096ec0, 0x00001d44, 'ELIGIB_CARD_ID_OFF', 'eligib_card_id_6ec0',
     'zero_duel_lp_display_counters: [+0x1d44] card_id field clear'),

    # ACTIVATION_STATE_A_OFF (duel_field.inc, 0x00001d48)
    (0x08096ec4, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_6ec4',
     'zero_duel_lp_display_counters: [+0x1d48] activation state A clear'),
    (0x0809709c, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_709c',
     'submit_equip_slot_sprite_with_ref_a: [+0x1d48] activation state A'),
    (0x080970cc, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'actstate_a_70cc',
     'submit_equip_slot_sprite_with_ref_b: [+0x1d48] activation state A'),

    # ELIGIB_ACT_TYPE_OFF (ewram.inc, 0x00001d5c)
    (0x08096ee8, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_act_type_6ee8',
     'zero_duel_lp_display_counters pool: ELIGIB_ACT_TYPE_OFF(0x1d5c) write 0xd'),

    # P1LP_TIMER_OFF (ewram.inc, 0x00001cec)
    (0x08097224, 0x00001cec, 'P1LP_TIMER_OFF', 'p1lp_timer_7224',
     'check_equip_effect_zone_preconditions: [gP1LifePoints+0x1cec] timer check'),

    # P2LP_BLOCK2_OFF_1CF4 (ewram.inc, 0x00001cf4)
    (0x08097228, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_blk2_7228',
     'check_equip_effect_zone_preconditions: [+0x1cf4] P2 LP block2 <= 3'),

    # EQUIP_CHAIN_STEP_OFF (duel_field.inc, 0x00001d28)
    (0x08097498, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eq_chain_step_7498',
     'init_equip_display_state_with_sprite: [+0x1d28] equip chain step'),
    (0x08097674, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eq_chain_step_7674',
     'check_equip_slot_activation_blocked_by_chain: [+0x1d28] chain step'),
    (0x080976b8, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eq_chain_step_76b8',
     'check_equip_slot_activation_blocked_by_chain_ext: [+0x1d28] chain step'),
    (0x080977e8, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eq_chain_step_77e8',
     'enqueue_frozen_soul_zone_sprite_or_default: writes 0xd to [+0x1d28]'),

    # EQUIP_CHAIN_ACTIVE_OFF (duel_field.inc, 0x00001d2c)
    (0x0809749c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eq_chain_active_749c',
     'init_equip_display_state_with_sprite: [+0x1d2c] chain active flag'),
    (0x080975b8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eq_chain_active_75b8',
     'fill_slot_activation_state_array: [+0x1d2c] chain active'),
    (0x08097670, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eq_chain_active_7670',
     'check_equip_slot_activation_blocked_by_chain: [+0x1d2c] chain active'),
    (0x080976b4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eq_chain_active_76b4',
     'check_equip_slot_activation_blocked_by_chain_ext: [+0x1d2c] chain active'),
    (0x080977ec, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eq_chain_active_77ec',
     'enqueue_frozen_soul_zone_sprite_or_default: writes 0 to [+0x1d2c]'),

    # EQUIP_CHAIN_CANCEL_OFF (duel_field.inc NEW, 0x00001d30)
    (0x080977f0, 0x00001d30, 'EQUIP_CHAIN_CANCEL_OFF', 'eq_chain_cancel_77f0',
     'enqueue_frozen_soul_zone_sprite_or_default: writes 1 to [+0x1d30] cancel flag'),

    # ---- Group B: REUSE -- EWRAM globals ----

    # gDuelCardCtxBase (ewram.inc, 0x0201e2a0)
    (0x08096a6c, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6a6c',
     'set_equip_activation_state_by_mode: gDuelCardCtxBase[+4] player_id'),
    (0x08096ad0, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6ad0',
     'set_equip_activation_state_by_mode_alt: gDuelCardCtxBase[+4]'),
    (0x08096be0, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6be0',
     'dispatch_zone_activation_by_state: gDuelCardCtxBase for player_id'),
    (0x08096d08, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6d08',
     'dispatch_zone_activation_by_state case5: gDuelCardCtxBase player_id'),
    (0x08096d88, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_6d88',
     'dispatch_zone_activation_by_state case7: gDuelCardCtxBase player_id'),

    # gDuelFieldSlots (ewram.inc, 0x0201c510)
    (0x08096c68, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_6c68',
     'dispatch_zone_activation_by_state: gDuelFieldSlots base for zone slots'),
    (0x08096c9c, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_6c9c',
     'dispatch_zone_activation_by_state inner: gDuelFieldSlots'),
    (0x08097574, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_7574',
     'fill_slot_activation_state_array: gDuelFieldSlots base'),
    (0x08097788, 0x0201c510, 'gDuelFieldSlots', 'gduelfldslots_7788',
     'check_equip_slot_card_type_matches_active_state: gDuelFieldSlots'),

    # gDuelPhaseFlags (ewram.inc, 0x0201b290)
    (0x08096d3c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflag_6d3c',
     'dispatch_zone_activation_by_state case5: gDuelPhaseFlags'),
    (0x08096df8, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflag_6df8',
     'dispatch_zone_activation_by_state case6: gDuelPhaseFlags zone 0xb'),

    # gEquipChainSlotRefs (ewram.inc, 0x0201bb90)
    (0x080974a0, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainrefs_74a0',
     'init_equip_display_state_with_sprite: gEquipChainSlotRefs base'),
    (0x0809756c, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainrefs_756c',
     'fill_slot_activation_state_array: gEquipChainSlotRefs base'),
    (0x080975b0, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainrefs_75b0',
     'refresh_slot_activation_display_if_changed: gEquipChainSlotRefs'),
    (0x08097660, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainrefs_7660',
     'check_equip_slot_activation_blocked_by_chain: gEquipChainSlotRefs'),
    (0x08097780, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainrefs_7780',
     'check_equip_slot_card_type_matches_active_state: gEquipChainSlotRefs'),

    # ---- Group C: REUSE -- stride/offset constants ----

    # PLAYER_BLOCK_STRIDE (ewram.inc, 0x00000868)
    (0x08096c64, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6c64',
     'dispatch_zone_activation_by_state: player block stride for zone loop'),
    (0x08096c98, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6c98',
     'dispatch_zone_activation_by_state inner: player stride'),
    (0x08096cd4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6cd4',
     'dispatch_zone_activation_by_state: player stride case2/3'),
    (0x08096d8c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6d8c',
     'dispatch_zone_activation_by_state case5: player stride'),
    (0x08096dc8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6dc8',
     'dispatch_zone_activation_by_state case6: player stride'),
    (0x0809722c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_722c',
     'check_equip_effect_zone_preconditions: player stride for P2 path'),
    (0x08097570, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_7570',
     'fill_slot_activation_state_array: player block stride'),
    (0x08097784, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_7784',
     'check_equip_slot_card_type_matches_active_state: player stride'),

    # EFFECT_ENTRY_COUNT_OFF (ewram.inc, 0x00000594)
    (0x08096d40, 0x00000594, 'EFFECT_ENTRY_COUNT_OFF', 'effect_entry_cnt_6d40',
     'dispatch_zone_activation_by_state: [gDuelPhaseFlags+0x594] effect entry count'),

    # EQUIP_ACTIVE_CTX_OFF (duel_field.inc, 0x00000484)
    (0x08096dfc, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'equip_active_ctx_6dfc',
     'dispatch_zone_activation_by_state: [gDuelPhaseFlags+0x484] active ctx slot ptr'),

    # LP_ACTIVATION_TYPE_ARRAY_BASE_OFF (ewram.inc, 0x000010e1)
    (0x08097578, 0x000010e1, 'LP_ACTIVATION_TYPE_ARRAY_BASE_OFF', 'lp_act_type_arr_7578',
     'fill_slot_activation_state_array: [gP1LifePoints+0x10e1] activation type array base'),
    (0x0809778c, 0x000010e1, 'LP_ACTIVATION_TYPE_ARRAY_BASE_OFF', 'lp_act_type_arr_778c',
     'check_equip_slot_card_type_matches_active_state: [+0x10e1] activation type array'),

    # ---- Group D: REUSE -- card CIDs ----

    # THUNDER_OF_RULER_CID (card_info.inc, 0x000015f0)
    (0x08097230, 0x000015f0, 'THUNDER_OF_RULER_CID', 'thunder_ruler_7230',
     'check_equip_effect_zone_preconditions: check_value_in_slot_chain(player,0xb,0x15f0)'),

    # AGENT_OF_JUDGMENT_SATURN_CID (card_info.inc, 0x0000173f)
    (0x08097234, 0x0000173f, 'AGENT_OF_JUDGMENT_SATURN_CID', 'agent_saturn_7234',
     'check_equip_effect_zone_preconditions: check_value_in_slot_chain(player,0xb,0x173f)'),

    # DD_BORDERLINE_CID (card_info.inc NEW, 0x000016d4)
    (0x08097238, 0x000016d4, 'DD_BORDERLINE_CID', 'dd_borderline_7238',
     'check_equip_effect_zone_preconditions: count_available_effect_zones(0/1,0x16d4,-1)'),

    # FROZEN_SOUL_CID (card_info.inc NEW, 0x000016a1)
    (0x08097268, 0x000016a1, 'FROZEN_SOUL_CID', 'frozen_soul_7268',
     'check_equip_zone_has_frozen_soul_or_great_long_nose: check_value_in_slot_chain(player,0xb,0x16a1)'),
    (0x080977e0, 0x000016a1, 'FROZEN_SOUL_CID', 'frozen_soul_77e0',
     'enqueue_frozen_soul_zone_sprite_or_default: enqueue_equip_slot_sprite_attr(player,0xb,0x16a1,1)'),

    # GREAT_LONG_NOSE_CID (card_info.inc NEW, 0x00001502)
    (0x0809726c, 0x00001502, 'GREAT_LONG_NOSE_CID', 'great_long_nose_726c',
     'check_equip_zone_has_frozen_soul_or_great_long_nose: check_slot_has_node_by_card_id(player,0xb,0x1502)'),

    # DIFFUSION_WAVE_MOTION_CID (card_info.inc, 0x000015ff)
    (0x080972d4, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID', 'diffusion_wm_72d4',
     'check_equip_slot_activation_blocked_by_chain: DIFFUSION_WAVE_MOTION_CID guard'),

    # STAUNCH_DEFENDER_CID (card_info.inc, 0x00001669)
    (0x08097354, 0x00001669, 'STAUNCH_DEFENDER_CID', 'staunch_def_7354',
     'check_equip_slot_activation_blocked_by_chain: STAUNCH_DEFENDER check'),

    # AMAZONESS_ARCHERS_CID (card_info.inc, 0x000014a6)
    (0x08097358, 0x000014a6, 'AMAZONESS_ARCHERS_CID', 'amazoness_arch_7358',
     'check_equip_slot_activation_blocked_by_chain: AMAZONESS_ARCHERS check'),
    (0x08097408, 0x000014a6, 'AMAZONESS_ARCHERS_CID', 'amazoness_arch_7408',
     'check_equip_slot_activation_blocked_by_chain_ext: AMAZONESS_ARCHERS_CID'),

    # BERSERK_GORILLA_CID (card_info.inc, 0x000016bf)
    (0x0809735c, 0x000016bf, 'BERSERK_GORILLA_CID', 'berserk_gor_735c',
     'check_equip_slot_activation_blocked_by_chain: BERSERK_GORILLA check'),
    (0x08097410, 0x000016bf, 'BERSERK_GORILLA_CID', 'berserk_gor_7410',
     'check_equip_slot_activation_blocked_by_chain_ext: BERSERK_GORILLA_CID'),

    # STAUNCH_DEFENDER_CID (card_info.inc, 0x00001669) -- second occurrence (ext check)
    (0x0809740c, 0x00001669, 'STAUNCH_DEFENDER_CID', 'staunch_def_740c',
     'check_equip_slot_activation_blocked_by_chain_ext: STAUNCH_DEFENDER_CID'),

    # DIFFUSION_WAVE_MOTION_CID second occurrence
    (0x08097404, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID', 'diffusion_wm_7404',
     'check_equip_slot_activation_blocked_by_chain_ext: DIFFUSION_WAVE_MOTION_CID'),

    # BLACK_LUSTER_SOLDIER_ENVOY_CID (card_info.inc, 0x000016cb)
    (0x08097414, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID', 'bls_envoy_7414',
     'check_equip_slot_activation_blocked_by_chain_ext: BLS_ENVOY_CID guard'),

    # EARTHBOUND_INVITATION_CID (card_info.inc NEW, 0x0000177a)
    (0x08097418, 0x0000177a, 'EARTHBOUND_INVITATION_CID', 'earthbound_inv_7418',
     'check_equip_slot_activation_blocked_by_chain_ext: check_value_in_slot_chain(1-player,0xb,0x177a)'),

    # TOON_DEFENSE_CID (card_info.inc, 0x00001561)
    (0x0809741c, 0x00001561, 'TOON_DEFENSE_CID', 'toon_defense_741c',
     'check_equip_slot_activation_blocked_by_chain_ext: TOON_DEFENSE_CID'),

    # ASTRAL_BARRIER_CID (card_info.inc, 0x00001852)
    (0x08097420, 0x00001852, 'ASTRAL_BARRIER_CID', 'astral_barrier_7420',
     'check_equip_slot_activation_blocked_by_chain_ext: ASTRAL_BARRIER_CID'),

    # RING_OF_MAGNETISM_CID (card_info.inc, 0x00001318)
    (0x08097424, 0x00001318, 'RING_OF_MAGNETISM_CID', 'ring_magnet_7424',
     'check_equip_slot_activation_blocked_by_chain_ext: RING_OF_MAGNETISM_CID'),

    # ---- Group E: REUSE -- OAM sprite attrs ----

    # OAM_EQUIP_SPRITE_TILE_P2_1B (oam_attr.inc, 0x0000801b)
    (0x080974a4, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'oam_eq_p2_1b_74a4',
     'init_equip_display_state_with_sprite: P2 sprite tile code 0x801b'),
    (0x08097668, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'oam_eq_p2_1b_7668',
     'check_equip_slot_activation_blocked_by_chain: P2 sprite tile 0x801b'),

    # OAM_EQUIP_ZONE_SPRITE_P2_18 (oam_attr.inc NEW, 0x00008018)
    (0x08097820, 0x00008018, 'OAM_EQUIP_ZONE_SPRITE_P2_18', 'oam_eq_zone_p2_7820',
     'enqueue_frozen_soul_zone_sprite_or_default: P2 zone sprite 0x8018'),

    # OAM_EQUIP_ZONE_SPRITE_P2_0F (oam_attr.inc NEW, 0x0000800f)
    (0x08097824, 0x0000800f, 'OAM_EQUIP_ZONE_SPRITE_P2_0F', 'oam_eq_zone_p2_0f_7824',
     'enqueue_frozen_soul_zone_sprite_or_default: P2 zone second sprite 0x800f'),

    # ---- Group F: REUSE -- ROM table address ----

    # EQUIP_ACTIVATION_HANDLER_TABLE (duel_field.inc NEW, 0x09e47560) -- DAT_ slot
    # NOTE: DAT_08097110 is stored as .byte sequence in Ghidra (LE bytes 60 75 e4 09).
    # A createDWord call is made before this equate to coerce it to DWORD type.
    (0x0809717c, 0x09e47560, 'EQUIP_ACTIVATION_HANDLER_TABLE', 'equip_act_tbl_717c',
     'scan_card_type_effect_handler_table: HANDLER_TABLE_BASE=0x09e47560 18-entry table'),

    # ---- Group G: DWORD_ slots ----

    # SPRITE_LOW_HALF_MASK (duel_field.inc, 0x0000ffff) -- 4 DWORD_ slots
    # AND-mask-low-16-bits usage: ands r2,r1 clears high 16 bits of card attr word
    (0x08096f3c, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'card_attr_mask_6f3c',
     'apply_equip_activation_with_fixed_type_a: ands r2,r1 mask low 16 bits of card attr'),
    (0x08096f88, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'card_attr_mask_6f88',
     'apply_equip_activation_via_deck_slot_lookup: ands mask low 16 bits card attr'),
    (0x08097044, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'card_attr_mask_7044',
     'apply_equip_activation_with_id_lookup_type_a: ands low 16 bits'),
    (0x0809706c, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'card_attr_mask_706c',
     'apply_equip_activation_with_id_lookup_type_b: ands low 16 bits'),

    # PLAYER_BLOCK_STRIDE (ewram.inc, 0x00000868) -- 3 DWORD_ slots
    (0x08096f8c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6f8c',
     'apply_equip_activation_via_deck_slot_lookup: muls player stride DWORD'),
    (0x08096fd0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_6fd0',
     'eval_equip_target_via_player_deck_lookup: player stride DWORD'),
    (0x08097014, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_7014',
     'eval_equip_target_via_chain_zone_lookup: player stride DWORD'),

    # gP1HandSlotArray (ewram.inc, 0x0201c8f8)
    (0x08096f90, 0x0201c8f8, 'gP1HandSlotArray', 'gp1handslot_6f90',
     'apply_equip_activation_via_deck_slot_lookup: DECK_BASE_P0=0x0201c8f8'),

    # gP1SlotSetCodeArray (ewram.inc, 0x0201c740)
    (0x08096fd4, 0x0201c740, 'gP1SlotSetCodeArray', 'gp1slotset_6fd4',
     'eval_equip_target_via_player_deck_lookup: DECK_BASE_P0=0x0201c740'),

    # gP1ChainZoneArray (ewram.inc, 0x0201c880)
    (0x08097018, 0x0201c880, 'gP1ChainZoneArray', 'gp1chainzone_7018',
     'eval_equip_target_via_chain_zone_lookup: CHAIN_BASE_P0=0x0201c880'),

    # EQUIP_ACTIVATION_HANDLER_TABLE -- DWORD_ occurrences
    (0x080970e0, 0x09e47560, 'EQUIP_ACTIVATION_HANDLER_TABLE', 'equip_act_tbl_70e0',
     'get_equip_handler_card_type: loads EQUIP_ACTIVATION_HANDLER_TABLE base'),
    (0x080970fc, 0x09e47560, 'EQUIP_ACTIVATION_HANDLER_TABLE', 'equip_act_tbl_70fc',
     'check_equip_handler_uses_fixed_activation: loads handler table base'),
    (0x0809713c, 0x09e47560, 'EQUIP_ACTIVATION_HANDLER_TABLE', 'equip_act_tbl_713c',
     'scan_card_type_effect_handler_table: second load of handler table base'),

    # APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB (duel_field.inc NEW, 0x08097025)
    (0x08097100, 0x08097025, 'APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB', 'equip_act_fixed_thumb_7100',
     'check_equip_handler_uses_fixed_activation: THUMB fn-ptr to apply_equip_activation_with_id_lookup_type_a'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # switchD base pointer for dispatch_zone_activation_by_state outer switch
    (0x08096b78, 0x08096b7c,
     'switchD_08096b6a__switchdataD_08096b7c',
     'zone_act_switchdata_6b78',
     'dispatch_zone_activation_by_state: outer 10-case switch table base at 0x08096b7c'),
    # switchD base pointer for inner switch in dispatch_zone_activation_by_state
    (0x08096bf4, 0x08096bf8,
     'switchD_08096bf2__switchdataD_08096bf8',
     'zone_act_inner_switchdata_6bf4',
     'dispatch_zone_activation_by_state: inner switch table base at 0x08096bf8'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    All 15 PTR_gP1LifePoints_* -> gp1lp_ptr_*
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08096a9c, 'gp1lp_ptr_96a9c', None),
    (0x08096b00, 'gp1lp_ptr_96b00', None),
    (0x08096b34, 'gp1lp_ptr_96b34', None),
    (0x08096b6c, 'gp1lp_ptr_96b6c', None),
    (0x08096eb0, 'gp1lp_ptr_96eb0', None),
    (0x08096ee0, 'gp1lp_ptr_96ee0', None),
    (0x08097094, 'gp1lp_ptr_97094', None),
    (0x080970c4, 'gp1lp_ptr_970c4', None),
    (0x08097220, 'gp1lp_ptr_97220', None),
    (0x080972cc, 'gp1lp_ptr_972cc', None),
    (0x08097494, 'gp1lp_ptr_97494', None),
    (0x080975b4, 'gp1lp_ptr_975b4', None),
    (0x0809766c, 'gp1lp_ptr_9766c', None),
    (0x080976b0, 'gp1lp_ptr_976b0', None),
    (0x080977e4, 'gp1lp_ptr_977e4', None),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: (func_addr, old_name, new_name)
#    4 SUB_ -> semantic names
# ---------------------------------------------------------------------------
FUNC_RENAME = [
    (0x080970d0, 'SUB_080970d0', 'get_equip_handler_table_entry_count'),
    (0x080970d4, 'SUB_080970d4', 'get_equip_handler_card_type'),
    (0x080970e4, 'SUB_080970e4', 'check_equip_handler_uses_fixed_activation'),
    (0x08097104, 'SUB_08097104', 'get_equip_handler_table_entry_param'),
]

# ---------------------------------------------------------------------------
# E. PLATE_FULL: (func_addr, new_plate_text)
#    Full rewrite for CJK mojibake plates. Pure ASCII, <=500 chars each.
# ---------------------------------------------------------------------------
PLATE_FULL = [
    # dispatch_zone_activation_by_state (0x08096b3c, <=500 chars)
    (0x08096b3c,
     "Zone activation dispatch hub (indeg=5, class D). Checks LP_EQUIP_STATE_B_OFF(0x1d50); if 0 return 0. Reads ACTIVATION_STATE_C_OFF(0x1d4c)-1 -> 10-case jump: 1=single zone 0xc..0xf; 2/3=multi-zone x4 groups via setup_equip_slot_activation_entry/_alt/eval_zone_flags; 4=eval_zone_flags; 5=gDuelPhaseFlags->eval_zone_flags_for_player; 6=zone 0xb eval_placement_flags; 7=invoke_r3 via ACTIVATION_ENTRY_PTR_OFF; 8=invoke_r3 cond; 9/10=same as 7/8; default=0. FLAG_DUAL_ZONE=0x1000 FLAG_ACTIVATABLE=0x8."),

    # check_equip_effect_zone_preconditions (0x08097190, ~433 chars)
    (0x08097190,
     "Checks player can activate effect in equip zone (zone=0xb). r0=player_id. All must pass: (1) P1LP_TIMER_OFF(0x1cec)!=0; (2) P2LP_BLOCK2_OFF_1CF4(0x1cf4)<=3; (3) equip zone slot bit18==0; (4) check_value_in_slot_chain(player,0xb,THUNDER_OF_RULER_CID=0x15f0)==0; (5) same for AGENT_OF_JUDGMENT_SATURN_CID=0x173f; (6) count_available_effect_zones(0,DD_BORDERLINE_CID=0x16d4,-1)>0 OR count_hand_cards_by_field6(0,0x16)>0; (7) same player 1. Returns 1=pass, 0=fail. Read-only. indeg=3."),

    # check_equip_zone_has_frozen_soul_or_great_long_nose (0x08097244, ~363 chars)
    (0x08097244,
     "Checks equip zone (zone=0xb) for Frozen Soul (FROZEN_SOUL_CID=0x16a1) or Great Long Nose (GREAT_LONG_NOSE_CID=0x1502). r0=player_id -> r4. Step 1: check_value_in_slot_chain(r4, 0xb, FROZEN_SOUL_CID) -> if hit return 1. Step 2: check_slot_has_node_by_card_id(r4, 0xb, GREAT_LONG_NOSE_CID) -> if hit return 1. Else return 0. Pure query. indeg=3. Side effects: none."),

    # enqueue_frozen_soul_zone_sprite_or_default (0x080977a0, <=500 chars)
    (0x080977a0,
     "r0=player_side. Calls check_equip_zone_has_frozen_soul_or_great_long_nose. Found: enqueue_equip_slot_sprite_attr(player,0xb,FROZEN_SOUL_CID=0x16a1,1); trigger_card_display_op31_if_not_active(player,0x136); writes gP1LifePoints+EQUIP_CHAIN_STEP_OFF=0xd, +EQUIP_CHAIN_ACTIVE_OFF=0, +EQUIP_CHAIN_CANCEL_OFF=1; return 0. Not found: P1: enqueue_sprite_attr_record(0x18,1,0,0)+(0xf,0,0,0); P2: same with OAM_EQUIP_ZONE_SPRITE_P2_18=0x8018/OAM_EQUIP_ZONE_SPRITE_P2_0F=0x800f; return 1."),
]

# ---------------------------------------------------------------------------
# F. PLATE_SUBSTR: (func_addr, old_sub, new_sub)
#    Substring replace in existing ASCII plates. Pure ASCII.
# ---------------------------------------------------------------------------
PLATE_SUBSTR = [
    # L6137 zero_duel_lp_display_counters: FUN_080b70ac -> select_equip_target_slot_by_card_id
    (0x08096ecc, 'FUN_080b70ac', 'select_equip_target_slot_by_card_id'),
    # L6518 dispatch_to_effect_handler_by_card_type: FUN_0810e5d4 -> invoke_r3
    (0x08097150, 'FUN_0810e5d4', 'invoke_r3'),
    # L6518 dispatch_to_effect_handler_by_card_type: FUN_080bb414 -> dispatch_equip_activation_full_sequence
    (0x08097150, 'FUN_080bb414', 'dispatch_equip_activation_full_sequence'),
    # L6675 check_equip_slot_activation_blocked_by_chain: FUN_08099314 -> dispatch_equip_field_phase_handler
    (0x08097278, 'FUN_08099314', 'dispatch_equip_field_phase_handler'),
    # L6925 init_equip_display_state_with_sprite: FUN_08097c2c -> dispatch_equip_slot_display_state_by_phase
    (0x08097458, 'FUN_08097c2c', 'dispatch_equip_slot_display_state_by_phase'),
    # L6925 init_equip_display_state_with_sprite: FUN_08099314 -> dispatch_equip_field_phase_handler
    (0x08097458, 'FUN_08099314', 'dispatch_equip_field_phase_handler'),
    # L6969 fill_slot_activation_state_array: FUN_0809757c -> refresh_slot_activation_display_if_changed
    (0x080974a8, 'FUN_0809757c', 'refresh_slot_activation_display_if_changed'),
    # L6969 fill_slot_activation_state_array: FUN_08098564 -> tick_card_activation_phase_by_state
    (0x080974a8, 'FUN_08098564', 'tick_card_activation_phase_by_state'),
    # L7078 refresh_slot_activation_display_if_changed: FUN_08098264 -> tick_activation_display_state_machine
    (0x0809757c, 'FUN_08098264', 'tick_activation_display_state_machine'),
    # L7078 refresh_slot_activation_display_if_changed: FUN_08098564 -> tick_card_activation_phase_by_state
    (0x0809757c, 'FUN_08098564', 'tick_card_activation_phase_by_state'),
    # L7249 check_equip_slot_card_type_matches_active_state: FUN_08099314 -> dispatch_equip_field_phase_handler
    (0x080976c8, 'FUN_08099314', 'dispatch_equip_field_phase_handler'),
]

# ---------------------------------------------------------------------------
# DWORD_COERCE: slots stored as .byte sequences that need createDWord first
# ---------------------------------------------------------------------------
DWORD_COERCE = [
    0x08097110,  # DAT_08097110 stored as 4 .byte (LE 60 75 e4 09 = 0x09e47560); coerce to DWORD
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

def _coerce_dword(addr):
    """Force a DWORD data type at addr (for .byte-encoded pool words)."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    dt = DataTypes.DWordDataType.dataType
    if DRY:
        print("[dry] coerce_dword @ 0x%08x" % addr)
        return True
    existing = listing.getDataAt(a)
    if existing is not None and existing.getDataType().equals(dt):
        print("[ok ] DWord already @ 0x%08x" % addr)
        return True
    try:
        clearListing(a, a.add(3))
    except Exception as e:
        print("[warn] clear @ 0x%08x: %s" % (addr, e))
    try:
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr)
        return True
    except Exception as e:
        print("[FAIL] coerce_dword 0x%08x: %s" % (addr, e))
        return False

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

def _apply_func_rename(func_addr, old_name, new_name):
    from ghidra.program.model.symbol import SourceType as ST
    a = _addr(func_addr)
    fn = currentProgram.getFunctionManager().getFunctionAt(a)
    if fn is None:
        # Try createFunction for unrecognized function stubs
        if DRY:
            print("[dry] FUNC_RENAME 0x%08x: createFunction then rename %s -> %s" % (func_addr, old_name, new_name))
            return 1
        try:
            fn = createFunction(a, new_name)
            if fn is not None:
                print("[FRN] 0x%08x  created+named: %s" % (func_addr, new_name))
                return 1
        except Exception as e:
            print("[WARN] FUNC_RENAME 0x%08x: createFunction failed: %s" % (func_addr, e))
        print("[WARN] FUNC_RENAME 0x%08x: no function found, rename skipped" % func_addr)
        return 0
    current = fn.getName()
    if DRY:
        print("[dry] FUNC_RENAME 0x%08x  %s -> %s" % (func_addr, current, new_name))
        return 1
    fn.setName(new_name, SourceType.USER_DEFINED)
    print("[FRN] 0x%08x  %s -> %s" % (func_addr, current, new_name))
    return 1

def _apply_plate_full(func_addr, new_text):
    """Full plate replacement. Fail if non-ASCII or >500 chars."""
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
    print("=== RefineF12Seg4Slots (DRY=%s) ===" % DRY)
    print("  Seg-4: 0x08096a4c..0x08097828, file 12 equip_activation_scan")
    print("  EQ=%d  REF=%d  RENAME=%d  FUNC_RENAME=%d  PLATE_FULL=%d  PLATE_SUB=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(FUNC_RENAME), len(PLATE_FULL), len(PLATE_SUBSTR)))

    # Pre: coerce .byte-encoded pool words to DWORD
    print("\n--- Pre: DWORD_COERCE (%d) ---" % len(DWORD_COERCE))
    for addr in DWORD_COERCE:
        _coerce_dword(addr)

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
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
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
    print("  REF done: %d" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. FUNC_RENAME
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAME))
    func_ok = 0
    for func_addr, old_name, new_name in FUNC_RENAME:
        func_ok += _apply_func_rename(func_addr, old_name, new_name)
    print("  FUNC_RENAME done: %d" % func_ok)

    # E. PLATE_FULL
    print("\n--- E. PLATE_FULL_REWRITES (%d) ---" % len(PLATE_FULL))
    plate_full_ok = 0
    plate_full_fail = 0
    for func_addr, new_text in PLATE_FULL:
        if _apply_plate_full(func_addr, new_text):
            plate_full_ok += 1
        else:
            plate_full_fail += 1
    print("  PLATE_FULL done: ok=%d fail=%d" % (plate_full_ok, plate_full_fail))

    # F. PLATE_SUBSTR
    print("\n--- F. PLATE_SUBSTR_FIXES (%d) ---" % len(PLATE_SUBSTR))
    plate_sub_ok = 0
    plate_sub_fail = 0
    for func_addr, old_sub, new_sub in PLATE_SUBSTR:
        if _apply_plate_fix(func_addr, old_sub, new_sub):
            plate_sub_ok += 1
        else:
            plate_sub_fail += 1
    print("  PLATE_SUB done: ok=%d fail=%d" % (plate_sub_ok, plate_sub_fail))

    print("\n=== RefineF12Seg4Slots DONE ===")
    print("  EQ=%d REF=%d RENAME=%d FUNC=%d PLATE_FULL=%d/%d PLATE_SUB=%d/%d" % (
        eq_ok, len(REF_SLOTS), len(RENAME_SLOTS), func_ok,
        plate_full_ok, len(PLATE_FULL),
        plate_sub_ok, len(PLATE_SUBSTR)))

main()
