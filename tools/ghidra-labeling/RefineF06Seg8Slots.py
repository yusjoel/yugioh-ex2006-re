# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg8Slots.py -- F06 Seg-8 (0x08058cec..0x08059de0)
#   ROM range: tick_equip_score_lp_display_seq .. tick_equip_lp_row_spell_zone_display_seq
#   22 named functions, 118 residual auto-name slots
#
# Sections:
#   A. EQ_SLOTS  -- 95 data-equate slots
#   B. REF_SLOTS -- 21 fn-ptr / RAM-ptr REF slots
#   C. RENAME_SLOTS -- 17 plain renames (5 DWORD_->PTR_gP1LifePoints_ + 10 switchD_ + 2 PTR_DAT_ table)
#   D. DAT_RENAME -- 7 DAT_ slots (fn-ptr / data)
#   E. PLATE_SET -- 3 plate rewrites (2 full ASCII CJK rewrite, 1 substring)
#
# New constants added to constants files BEFORE running this script:
#   card_info.inc:  +1 (ABYSS_SOLDIER_CID=0x1727)
#   duel_field.inc: +1 (OP31_EFFECT_NODE_COUNT_CODE=0x13d)
#
# Reused constants (must exist in constants/*.inc):
#   ewram.inc:       gDuelPhaseFlags=0x0201b290, PLAYER_BLOCK_STRIDE=0x868,
#                    gP1LifePoints=0x0201c4e0, LP_CARD_TRACK_BASE_OFF=0x1da8,
#                    gDuelCardCtxBase=0x0201e2a0, gDuelFieldSlots=0x0201c510,
#                    gP1HandSlotArray=0x0201c8f8, gP1FieldArrayCBase=0x0201c600,
#                    gEquipChainSlotRefs=0x0201bb90,
#                    ELIGIB_SPRITE_CTRL_OFF=0x1d68, LP_BANISHER_CTX_OFF=0x1d70,
#                    DISPLAY_SEQ_ACTIVE_PLAYER_OFF=0x1d10
#   duel_field.inc:  EQUIP_ACTIVATION_STEP_OFF=0x4ac,
#                    EQUIP_ACTIVE_CTX_OFF=0x484,
#                    EQUIP_ACTIVE_CTX_OFF=0x484,
#                    lookup_equip_score_mooyan_p1=0x199
#   card_info.inc:   SLOT_CARD_EMPTY=0xffff, VAMPIRE_GENESIS_CID=0x1895,
#                    DOUBLE_ATTACK_CID=0x18cb, THE_FIRST_SARCOPHAGUS_CID=0x17af,
#                    BANISHER_OF_THE_LIGHT_CID=0x1332, AXE_OF_DESPAIR_CID=0x10d6
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_071238-pre-F06Seg8

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
#    const_name must already exist in constants/*.inc.
#    slot_label != const_name; all ^[a-z][a-z0-9_]+$
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==== gDuelPhaseFlags = 0x0201b290 (ewram.inc) x25 ====
    (0x08058d08, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_score_lp_state_base'),
    (0x08058db8, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_score_lp_state_base_b'),
    (0x08058e30, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_select_disp_state_base'),
    (0x08058e64, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_select_disp_state_base_b'),
    (0x08058eb8, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_select_disp_state_base_c'),
    (0x08058fa8, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_row19_state_base'),
    (0x08059190, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_act_field_spell_state_base'),
    (0x08059270, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_eff_act_disp_state_base'),
    (0x08059334, 0x0201b290, 'gDuelPhaseFlags', 'check_zone_atk_buff_state_base'),
    (0x08059368, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_banisher_atk_act_state_base'),
    (0x080593c0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_banisher_atk_act_state_base_b'),
    (0x080594b0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_act_neo_daed_state_base'),
    (0x08059708, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_banisher_lp_state_base'),
    (0x0805977c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_banisher_slot_state_base'),
    (0x0805982c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_effect_node_state_base'),
    (0x080598a8, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_atk_zone_state_base'),
    (0x080598fc, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_atk_zone_state_base_b'),
    (0x08059934, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_atk_zone_state_base_c'),
    (0x08059958, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_atk_zone_state_base_d'),
    (0x0805999c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_atk_zone_state_base_e'),
    (0x08059a34, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_bitmap_state_base'),
    (0x08059a60, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_bitmap_state_base_b'),
    (0x08059a94, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_bitmap_state_base_c'),
    (0x08059b44, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_neo_daed_slot_state_base'),
    (0x08059b68, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_neo_daed_slot_state_base_b'),
    (0x08059c24, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_row_spell_state_base'),

    # ==== EQUIP_ACTIVATION_STEP_OFF = 0x000004ac (duel_field.inc) x26 ====
    (0x08058d0c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_score_lp_step_off'),
    (0x08058dbc, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_score_lp_step_off_b'),
    (0x08058e34, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_select_disp_step_off'),
    (0x08058e68, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_select_disp_step_off_b'),
    (0x08058ebc, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_select_disp_step_off_c'),
    (0x08058fac, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_row19_step_off'),
    (0x08059194, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_act_field_spell_step_off'),
    (0x08059274, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_eff_act_disp_step_off'),
    (0x0805936c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_banisher_atk_act_step_off'),
    (0x080593c4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_banisher_atk_act_step_off_b'),
    (0x080594b4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_act_neo_daed_step_off'),
    (0x0805970c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_banisher_lp_step_off'),
    (0x08059780, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_banisher_slot_step_off'),
    (0x08059830, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_effect_node_step_off'),
    (0x080598ac, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_atk_zone_step_off'),
    (0x08059900, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_atk_zone_step_off_b'),
    (0x08059938, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_atk_zone_step_off_c'),
    (0x0805995c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_atk_zone_step_off_d'),
    (0x080599a0, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_atk_zone_step_off_e'),
    (0x08059a38, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_bitmap_step_off'),
    (0x08059a64, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_bitmap_step_off_b'),
    (0x08059a98, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_bitmap_step_off_c'),
    (0x08059b48, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_neo_daed_slot_step_off'),
    (0x08059b6c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_neo_daed_slot_step_off_b'),
    (0x08059c28, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_row_spell_step_off'),

    # ==== LP_CARD_TRACK_BASE_OFF = 0x00001da8 (ewram.inc) x3 ====
    (0x08058d88, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'tick_equip_score_lp_track_off'),
    (0x08058de0, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'tick_equip_score_lp_track_off_b'),
    (0x08059004, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'dispatch_slot_card_sprite_track_off'),

    # ==== gDuelCardCtxBase = 0x0201e2a0 (ewram.inc) x5 ====
    (0x08058d90, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_score_lp_ctx_base'),
    (0x08058e98, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_zone_select_disp_ctx_base'),
    (0x08059220, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_eff_act_disp_ctx_base'),
    (0x0805987c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_effect_node_ctx_base'),
    (0x080593a0, 0x0201e2a0, 'gDuelCardCtxBase', 'check_zone_atk_buff_ctx_base'),

    # ==== DISPLAY_SEQ_ACTIVE_PLAYER_OFF = 0x00001d10 (ewram.inc) x1 ====
    (0x08059224, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF', 'tick_equip_eff_act_player_off'),

    # ==== ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (ewram.inc) x6 ====
    (0x08058ef8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_zone_select_disp_sprite_off'),
    (0x08059410, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'invoke_equip_zone14_sprite_off'),
    (0x080597fc, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_banisher_slot_sprite_off'),
    (0x08059a30, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_zone_bitmap_sprite_off'),
    (0x08059b0c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_neo_daed_slot_sprite_off'),

    # ==== LP_BANISHER_CTX_OFF = 0x00001d70 (ewram.inc) x2 ====
    (0x08058efc, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'tick_equip_zone_select_disp_banish_off'),
    (0x08059414, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'invoke_equip_zone14_banish_off'),

    # ==== PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) x10 ====
    (0x08058f48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_field_sarc_range_stride'),
    (0x08058f78, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_field_sarc_range_stride_b'),
    (0x080591ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_act_field_spell_stride'),
    (0x0805916c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_act_field_spell_stride_b'),
    (0x08059104, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_slot_card_sprite_stride'),
    (0x08059338, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'check_zone_atk_buff_active_ctx_off'),
    (0x0805933c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_zone_atk_buff_stride'),
    (0x080594ac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_act_neo_daed_stride'),
    (0x0805973c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_banisher_lp_stride'),
    (0x08059418, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_equip_zone14_stride'),

    # ==== gDuelFieldSlots = 0x0201c510 (ewram.inc) x2 ====
    (0x08059100, 0x0201c510, 'gDuelFieldSlots', 'dispatch_slot_card_sprite_slots_base'),
    (0x080591f0, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_act_field_spell_slots_base'),

    # ==== gP1HandSlotArray = 0x0201c8f8 (ewram.inc) x1 ====
    (0x08059170, 0x0201c8f8, 'gP1HandSlotArray', 'tick_equip_act_field_spell_hand_base'),

    # ==== gP1FieldArrayCBase = 0x0201c600 (ewram.inc) x1 ====
    (0x08059340, 0x0201c600, 'gP1FieldArrayCBase', 'check_zone_atk_buff_field_base'),

    # ==== gEquipChainSlotRefs = 0x0201bb90 (ewram.inc) x1 ====
    (0x0805904c, 0x0201bb90, 'gEquipChainSlotRefs', 'dispatch_slot_card_sprite_chain_base'),

    # ==== Card IDs x9 ====
    (0x08058d2c, 0x0000ffff, 'SLOT_CARD_EMPTY', 'tick_equip_score_lp_slot_empty'),
    (0x08058d8c, 0x0000ffff, 'SLOT_CARD_EMPTY', 'tick_equip_score_lp_slot_empty_b'),
    (0x08058f00, 0x00001895, 'VAMPIRE_GENESIS_CID', 'check_field_sarc_range_vamp_genesis_cid'),
    (0x08058f04, 0x00001727, 'ABYSS_SOLDIER_CID',   'check_field_sarc_range_abyss_soldier_cid'),
    (0x08058f10, 0x000018cb, 'DOUBLE_ATTACK_CID',   'check_field_sarc_range_double_attack_cid'),
    (0x08059108, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID', 'dispatch_slot_card_sprite_sarc_cid'),
    (0x0805910c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'dispatch_slot_card_sprite_banisher_cid'),
    (0x080592a4, 0x000010d6, 'AXE_OF_DESPAIR_CID',  'dispatch_equip_act_seq_axe_cid'),
    (0x080594ec, 0x000010d6, 'AXE_OF_DESPAIR_CID',  'tick_equip_act_neo_daed_axe_cid'),

    # ==== Misc scalar constants x2 ====
    (0x08058db4, 0x00000199, 'lookup_equip_score_mooyan_p1', 'tick_equip_score_lp_mooyan_p1'),
    (0x080598a4, 0x0000013d, 'OP31_EFFECT_NODE_COUNT_CODE',  'tick_equip_effect_node_op31_code'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    fn-ptr slots store THUMB+1 (odd addr).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gP1LifePoints = 0x0201c4e0 -- 14 pointer slots
    # 3 that were DWORD_ (new PTR_ labels) + 5 existing PTR_gP1LifePoints_ (keep labels) + 5 new
    (0x08058d84, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08058d84'),
    (0x08058ddc, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08058ddc'),
    (0x08058dfc, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08058dfc'),
    (0x08058ef4, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08058ef4'),
    (0x08059000, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08059000'),
    (0x0805940c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0805940c'),
    (0x080592a0, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080592a0'),
    (0x080594a8, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080594a8'),
    (0x08059738, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08059738'),
    (0x080597f8, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080597f8'),
    (0x08059880, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08059880'),
    (0x080598d4, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080598d4'),
    (0x08059a2c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08059a2c'),
    (0x08059b08, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08059b08'),

    # fn-ptr: check_zone_atk_buff_active_for_equip+1 = 0x080592e5 (2 slots)
    (0x080593a4, 0x080592e4, 'check_zone_atk_buff_active_for_equip',
     'dat_check_atk_buff_predicate_a'),
    (0x080593bc, 0x080592e4, 'check_zone_atk_buff_active_for_equip',
     'dat_check_atk_buff_predicate_b'),

    # fn-ptr: set_equip_activation_state_by_mode_alt = 0x080905e8+1 (2 slots)
    (0x080597b0, 0x080905e8, 'set_equip_activation_state_by_mode_alt',
     'dat_set_equip_mode_fn_ptr_a'),
    (0x08059998, 0x080905e8, 'set_equip_activation_state_by_mode_alt',
     'dat_set_equip_mode_fn_ptr_b'),

    # fn-ptr: set_equip_activation_state_by_mode = 0x08050eac+1 (1 slot)
    (0x08059acc, 0x08050eac, 'set_equip_activation_state_by_mode',
     'dat_set_equip_mode_fn_ptr_c'),

    # ROM data ptr: equip target table 0x08065991 -> check_equip_activation_at_slot11 (2 slots)
    (0x08058e9c, 0x08065990, 'check_equip_activation_at_slot11',
     'dat_equip_target_table_ptr_a'),
    (0x08058eb4, 0x08065990, 'check_equip_activation_at_slot11',
     'dat_equip_target_table_ptr_b'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, new_label)
#    switchD_ -> tick_equip_atk_zone_seq__ renames + 2 PTR_DAT_ table renames
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # 5 DWORD_ -> PTR_gP1LifePoints_ renames
    # (These are handled by REF_SLOTS above -- REF sets the label on the slot)
    # Nothing needed here for those; they are created in REF_SLOTS.

    # switchD_080598fa__ -> tick_equip_atk_zone_seq__ (10 items)
    (0x080598f0, 'tick_equip_atk_zone_seq__default'),    # switchD_080598fa__default @ 0x80598f0
    (0x080598fa, 'tick_equip_atk_zone_seq__dispatch'),   # switchD_080598fa__switchD @ 0x80598fa
    (0x08059904, 'tick_equip_atk_zone_seq__table_ptr'),  # PTR_switchdataD_08059908_08059904 @ 0x8059904
    (0x08059908, 'tick_equip_atk_zone_seq__table'),      # switchD_080598fa__switchdataD_08059908 @ 0x8059908
    (0x08059920, 'tick_equip_atk_zone_seq__case_op31_0x1a'),    # switchD_080598fa__caseD_0 @ 0x8059920
    (0x0805993c, 'tick_equip_atk_zone_seq__case_init_ctx'),     # switchD_080598fa__caseD_1 @ 0x805993c
    (0x08059960, 'tick_equip_atk_zone_seq__case_get_monster_slot'),  # switchD_080598fa__caseD_2 @ 0x8059960
    (0x08059980, 'tick_equip_atk_zone_seq__case_set_mode_alt'),  # switchD_080598fa__caseD_3 @ 0x8059980
    (0x080599ae, 'tick_equip_atk_zone_seq__case_check_confirmed'),   # switchD_080598fa__caseD_4 @ 0x80599ae
    (0x08059a3c, 'tick_equip_atk_zone_seq__case_submit_sprite'),     # switchD_080598fa__caseD_5 @ 0x8059a3c

    # PTR_DAT_ table renames (2 items)
    (0x08059568, 'equip_type80_dispatch_table_ptr'),
    (0x08059cf4, 'equip_lp_spell_zone_dispatch_table_ptr'),
]

# ---------------------------------------------------------------------------
# E. PLATE_SET: (func_entry_addr, new_text)
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_SET = [
    # PLATE-1: tick_equip_activation_if_field_spell_hand_ok @ 0x08059110
    # Full ASCII rewrite (old plate: CJK mojibake)
    (0x08059110,
     'tick_equip_activation_if_field_spell_hand_ok @ 0x08059110\n'
     'Conditional entry wrapper for equip activation state machine. Prerequisite:\n'
     'check_equip_slot_eligible_field_spell_by_hand_set_code_dispatch checks field-spell\n'
     'hand set_code; returns -1 if fails. If pass: calls tick_equip_activation_state_machine;\n'
     'if tick returns 1 (slot selected), extracts set_code from card_entry[+4] bits[14:6]\n'
     '(9-bit, lsls#0x11/lsrs#0x17), calls find_hand_slot_idx_by_set_code, then\n'
     'enqueue_equip_zone_sprite_by_slot_ptr. Propagates tick return value.\n'
     'indeg=0, Sub-type A.'),

    # PLATE-2: tick_equip_activation_if_neo_daedalus_with_lp_row @ 0x08059448
    # Full ASCII rewrite (old plate: CJK mojibake + stale FUN_08058550)
    (0x08059448,
     'tick_equip_activation_if_neo_daedalus_with_lp_row @ 0x08059448\n'
     'Conditional entry wrapper for equip activation state machine combining Neo Daedalus\n'
     'eligibility check and effect dispatch. Called by tick_equip_activation_neo_daedalus_gate\n'
     '(indeg=1). Prerequisite: check_neo_daedalus_placement_eligible; returns -1 if fails.\n'
     'If pass: iterates effect node chain and drives tick_equip_activation_state_machine.\n'
     'Step counter [gDuelPhaseFlags+0x4ac]==0: calls trigger_card_display_op31_if_not_active\n'
     '(op=0x122); ==1: calls set_lp_display_row_all_slots(opponent, AXE_OF_DESPAIR_CID).\n'
     'Exit: pop{r1}; bx r1 Sub-case E.'),
]

# PLATE-3: check_zone_atk_buff_active_for_equip @ 0x080592e4
# Substring replace only: FUN_0805934c -> tick_equip_banisher_atk_activation_display_seq
PLATE3_FUNC = 0x080592e4
PLATE3_OLD  = 'FUN_0805934c'
PLATE3_NEW  = 'tick_equip_banisher_atk_activation_display_seq'


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    """Verify 4-byte little-endian value at slot_int == want (or want|1 for THUMB fn-ptr)."""
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data at 0x%08x" % slot_int
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF06Seg8Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm      = currentProgram.getSymbolTable()
    nA = nB = nC = nD = nE = 0
    made_targets = set()
    fail_count = 0

    # -------------------------------------------------------------------------
    # A. EQ_SLOTS
    # -------------------------------------------------------------------------
    print("--- A. EQ_SLOTS (%d slots) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s want=0x%x)" % (slot_int, err, cname, value))
            fail_count += 1
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # -------------------------------------------------------------------------
    # B. REF_SLOTS
    # -------------------------------------------------------------------------
    print("--- B. REF_SLOTS (%d slots) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        ok, err = _check(slot_int, tgt_int)
        if not ok:
            # fn-ptr slots store THUMB+1 (odd); also try tgt_int|1
            ok2, _ = _check(slot_int, tgt_int | 1)
            if not ok2:
                print("[B FAIL] 0x%08x: %s (target=%s want=0x%x)" % (
                    slot_int, err, gas_label, tgt_int))
                fail_count += 1
                continue
        if DRY:
            print("[B dry] 0x%08x -> %s (0x%08x) slot_label=%s" % (
                slot_int, gas_label, tgt_int, slot_label))
            nB += 1
            continue
        target_addr = _addr(tgt_int)
        if tgt_int not in made_targets:
            createLabel(target_addr, gas_label, True, SourceType.USER_DEFINED)
            made_targets.add(tgt_int)
        ref = rm.addMemoryReference(
            _addr(slot_int), target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s @ 0x%08x)" % (
            slot_int, slot_label, gas_label, tgt_int))
        nB += 1

    # -------------------------------------------------------------------------
    # C. RENAME_SLOTS
    # -------------------------------------------------------------------------
    print("--- C. RENAME_SLOTS (%d slots) ---" % len(RENAME_SLOTS))
    for slot_int, new_label in RENAME_SLOTS:
        if DRY:
            print("[C dry] 0x%08x rename -> %s" % (slot_int, new_label))
            nC += 1
            continue
        try:
            createLabel(_addr(slot_int), new_label, True, SourceType.USER_DEFINED)
            print("[C ok] 0x%08x -> %s" % (slot_int, new_label))
            nC += 1
        except Exception as e:
            print("[C FAIL] 0x%08x: %s" % (slot_int, e))
            fail_count += 1

    # -------------------------------------------------------------------------
    # E. PLATE_SET (full ASCII rewrite)
    # -------------------------------------------------------------------------
    print("--- E. PLATE_SET (%d items) ---" % len(PLATE_SET))
    for func_int, new_text in PLATE_SET:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[E FAIL] no CodeUnit @ 0x%08x" % func_int)
            fail_count += 1
            continue
        if DRY:
            print("[E dry] 0x%08x full plate rewrite (%d chars)" % (func_int, len(new_text)))
            nE += 1
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("[E ok] 0x%08x plate set (%d chars)" % (func_int, len(new_text)))
        nE += 1

    # -------------------------------------------------------------------------
    # PLATE-3: substring replace in check_zone_atk_buff_active_for_equip plate
    # -------------------------------------------------------------------------
    print("--- PLATE-3: substring replace @ 0x%08x ---" % PLATE3_FUNC)
    cu3 = listing.getCodeUnitAt(_addr(PLATE3_FUNC))
    if cu3 is None:
        print("[P3 FAIL] no CodeUnit @ 0x%08x" % PLATE3_FUNC)
        fail_count += 1
    else:
        old_plate = cu3.getComment(CodeUnit.PLATE_COMMENT)
        if old_plate and PLATE3_OLD in old_plate:
            new_plate = old_plate.replace(PLATE3_OLD, PLATE3_NEW)
            if DRY:
                print("[P3 dry] 0x%08x: would replace '%s' -> '%s'" % (
                    PLATE3_FUNC, PLATE3_OLD, PLATE3_NEW))
            else:
                cu3.setComment(CodeUnit.PLATE_COMMENT, new_plate)
                print("[P3 ok] 0x%08x: replaced '%s' -> '%s'" % (
                    PLATE3_FUNC, PLATE3_OLD, PLATE3_NEW))
            nE += 1
        else:
            if old_plate is None:
                print("[P3 WARN] no plate @ 0x%08x" % PLATE3_FUNC)
            else:
                print("[P3 WARN] substring '%s' not found in plate @ 0x%08x" % (
                    PLATE3_OLD, PLATE3_FUNC))
                print("[P3 WARN] existing plate: %s..." % old_plate[:100])
            # WARN counts as FAIL per methodology (WARN=FAIL)
            fail_count += 1

    print("[done] A=%d B=%d C=%d E=%d FAIL=%d (DRY=%s)" % (
        nA, nB, nC, nE, fail_count, DRY))
    if fail_count > 0:
        print("[WARN] %d FAIL(s) above -- review before using non-dry run" % fail_count)


main()
