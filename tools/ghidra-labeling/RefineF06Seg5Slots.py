# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg5Slots.py -- F06 Seg-5 (0x080565e8..0x08057458)
#   ROM range: tick_equip_activation_with_lp_cost_sprite .. tick_equip_activation_lp_cost_sprite_by_type
#   23 fn, 117 slots (82 DAT_ + 19 DWORD_ + 16 PTR_gP1LifePoints)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (94 slots: 82 DAT_ + 12 DWORD_ reused/new constants)
#                   Includes 3 RENAME_as_EQ slots (EQUIP_SPRITE_CARD_DATA/MODE_103/MODE_117)
#   B. REF_SLOTS -- 23 slots (16 PTR_gP1LP + 4 DWORD_gP1LP + 3 fn-ptr)
#   C. (none)    -- no RENAME_SLOTS separate from EQ
#   D. PLATE_SUBS -- P5: enqueue_equip_slot_sprite_mode4 (2 stale FUN_ substring replace)
#   E. PLATE_SET  -- P0-P4: 5 full ASCII plate rewrites (CJK mojibake + stale FUN_)
#
# New constants added to constants files BEFORE running this script:
#   card_info.inc: +7 CIDs (POISON_OF_THE_OLD_MAN/CYBER_RAIDER/SPIRITUAL_FIRE_ART/
#                            FRIENDSHIP/UNITY/ATTACK_REFLECTOR_UNIT/PITCH_BLACK_POWER_STONE)
#   duel_field.inc: +3 scalars (EQUIP_SPRITE_CARD_DATA/EQUIP_ACT_SCORE_MODE_103/EQUIP_ACT_SCORE_MODE_117)
#
# Reused constants (must exist in constants/*.inc):
#   ewram.inc: PLAYER_BLOCK_STRIDE=0x868, gDuelPhaseFlags=0x0201b290, gDuelCardCtxBase=0x0201e2a0,
#              gDuelFieldSlots=0x0201c510, ELIGIB_SPRITE_CTRL_OFF=0x1d68, ELIGIB_ANIM_STATE_OFF=0x1d6c,
#              gP1LifePoints=0x0201c4e0
#   duel_field.inc: EQUIP_ACTIVATION_STEP_OFF=0x4ac, FIELD_STATE_OFF=0x1cf4,
#                   TRIGGER_OP_PARAM_107=0x107, SCENE_SLOT_MASK_LO=0xfff
#   card_info.inc: SLOT_CARD_EMPTY=0xffff, get_card_lp_cost_by_id_cid_11cf=0x11cf,
#                  DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713, KNIGHTS_TITLE_CID=0x167d, etc.
#   oam_attr.inc: OAM_ATTR1_X_CLEAR=0xfffffe00

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
#    slot_label != const_name.
#    All values verified against ROM.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==== PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc): 11 slots ====
    (0x08056740, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'trigger_equip_lp_sprite_by_activation_state_stride'),
    (0x080568bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_zone_has_card_stride'),
    (0x08056928, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'update_equip_chain_pair_sprites_atk_stride'),
    (0x08056b2c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_score_sprite_1708_stride'),
    (0x08056b58, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_score_sprite_1927_stride'),
    (0x08056d1c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_score_15cf_stride'),
    (0x08056e5c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_score_1841_stride_a'),
    (0x08056ec4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_score_1841_stride_b'),
    (0x08057340, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'traverse_equip_zone_nodes_lp_stride'),
    (0x0805741c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_zone14_test_stride'),
    (0x080570cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_score_state2_15cf_stride'),

    # ==== gDuelPhaseFlags = 0x0201b290 (ewram.inc): 11 slots ====
    (0x08056758, 0x0201b290, 'gDuelPhaseFlags', 'trigger_equip_lp_sprite_phase_flags_a'),
    (0x080567e0, 0x0201b290, 'gDuelPhaseFlags', 'dispatch_equip_card_name_phase_flags'),
    (0x0805683c, 0x0201b290, 'gDuelPhaseFlags', 'dispatch_equip_card_name_phase_flags_b'),
    (0x08056954, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_score_sprite_phase_flags_a'),
    (0x08056a18, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_score_sprite_phase_flags_b'),
    (0x08056bf4, 0x0201b290, 'gDuelPhaseFlags', 'dispatch_equip_direct_type_zone_phase_flags'),
    (0x08056fb8, 0x0201b290, 'gDuelPhaseFlags', 'dispatch_equip_score_phase_flags_a'),
    (0x080572e8, 0x0201b290, 'gDuelPhaseFlags', 'traverse_equip_zone_nodes_phase_flags'),
    (0x08057178, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_activation_state_phase_flags_a'),
    (0x080571d0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_activation_state_phase_flags_b'),
    (0x080573a4, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone14_phase_flags'),

    # ==== EQUIP_ACTIVATION_STEP_OFF = 0x000004ac (duel_field.inc): 12 slots ====
    (0x0805675c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'trigger_equip_lp_sprite_step_off_a'),
    (0x080567e4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'dispatch_equip_card_name_step_off_a'),
    (0x08056840, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'dispatch_equip_card_name_step_off_b'),
    (0x08056958, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_score_sprite_step_off_a'),
    (0x08056a1c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_score_sprite_step_off_b'),
    (0x08056bf8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'dispatch_equip_direct_type_zone_step_off'),
    (0x08056fbc, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'dispatch_equip_score_step_off_a'),
    (0x08057208, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'enqueue_lp_display_row_from_slot_step_off'),
    (0x0805717c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_activation_state_step_off_a'),
    (0x080571d4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_activation_state_step_off_b'),
    (0x080573a8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone14_step_off'),
    (0x080572ec, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'traverse_equip_zone_nodes_step_off'),

    # ==== gDuelCardCtxBase = 0x0201e2a0 (ewram.inc): 4 slots ====
    (0x08056738, 0x0201e2a0, 'gDuelCardCtxBase', 'trigger_equip_lp_sprite_card_ctx_base'),
    (0x08056808, 0x0201e2a0, 'gDuelCardCtxBase', 'dispatch_equip_card_name_card_ctx_base'),
    (0x08056efc, 0x0201e2a0, 'gDuelCardCtxBase', 'dispatch_equip_score_card_ctx_base'),
    (0x080571b8, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_activation_state_card_ctx_base'),

    # ==== gDuelFieldSlots = 0x0201c510 (ewram.inc): 3 slots ====
    (0x080568c0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_zone_has_card_zone_base'),
    (0x0805692c, 0x0201c510, 'gDuelFieldSlots', 'update_equip_chain_pair_sprites_zone_base'),
    (0x080570d0, 0x0201c510, 'gDuelFieldSlots', 'dispatch_equip_score_state2_zone_base'),

    # ==== ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (ewram.inc): 2 slots ====
    (0x08056a64, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_score_sprite_eligib_sprite_off'),
    (0x08057418, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_zone14_eligib_sprite_off'),

    # ==== ELIGIB_ANIM_STATE_OFF = 0x00001d6c (ewram.inc): 1 slot ====
    (0x08056a68, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'tick_equip_score_sprite_anim_off'),

    # ==== FIELD_STATE_OFF = 0x00001cf4 (duel_field.inc): 2 slots ====
    (0x08056d54, 0x00001cf4, 'FIELD_STATE_OFF', 'dispatch_equip_score_field_state_off_a'),
    (0x08056ec8, 0x00001cf4, 'FIELD_STATE_OFF', 'dispatch_equip_score_field_state_off_b'),

    # ==== SLOT_CARD_EMPTY = 0x0000ffff (card_info.inc): 3 slots ====
    (0x080566a4, 0x0000ffff, 'SLOT_CARD_EMPTY', 'update_equip_slot_zone_flag_invalid_zone'),
    (0x080567b8, 0x0000ffff, 'SLOT_CARD_EMPTY', 'enqueue_lp_row_clear_lp_row_clear'),
    (0x08057054, 0x0000ffff, 'SLOT_CARD_EMPTY', 'dispatch_equip_score_lp_row_clear'),

    # ==== SCENE_SLOT_MASK_LO = 0x00000fff (duel_field.inc): 1 slot ====
    # Note: value 0xfff = Catapult Turtle CID in BST context; C5 dedup => reuse SCENE_SLOT_MASK_LO
    (0x08056a74, 0x00000fff, 'SCENE_SLOT_MASK_LO', 'tick_equip_score_sprite_display_seq_cid_0fff'),

    # ==== get_card_lp_cost_by_id_cid_11cf = 0x000011cf (card_info.inc): 1 slot ====
    (0x08056838, 0x000011cf, 'get_card_lp_cost_by_id_cid_11cf', 'dispatch_equip_card_name_reserved_icid'),

    # ==== OAM_ATTR1_X_CLEAR = 0xfffffe00 (oam_attr.inc): 1 slot ====
    # Note: used as stack-frame-delta (add sp,r4 where r4=0xfffffe00 = -512; sub sp,#0x200 idiom)
    (0x08056950, 0xfffffe00, 'OAM_ATTR1_X_CLEAR', 'tick_equip_score_sprite_display_seq_frame_neg'),

    # ==== TRIGGER_OP_PARAM_107 = 0x00000107 (duel_field.inc): 1 slot ====
    (0x080572f0, 0x00000107, 'TRIGGER_OP_PARAM_107', 'traverse_equip_zone_nodes_op_param'),

    # ==== Card ID equates -- reuse from card_info.inc (23 CIDs, 29 slots) ====
    (0x08056980, 0x00001713, 'DEDICATION_THROUGH_LIGHT_DARK_CID', 'tick_equip_score_sprite_dedication'),
    (0x08056984, 0x0000167d, 'KNIGHTS_TITLE_CID', 'tick_equip_score_sprite_knights_title'),
    (0x0805699c, 0x0000192a, 'SPIRITUAL_WIND_ART_MIYABI_CID', 'tick_equip_score_sprite_wind_art'),
    (0x080569a8, 0x000019b5, 'ATTACK_REFLECTOR_UNIT_CID', 'tick_equip_score_sprite_attack_reflector'),
    (0x080569b4, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9', 'tick_equip_score_sprite_dark_magician'),
    (0x080569bc, 0x000013c3, 'GEARFRIED_IRON_KNIGHT_CID', 'tick_equip_score_sprite_gearfried'),
    (0x080569c4, 0x000018f6, 'CYBER_DRAGON_CID', 'tick_equip_score_sprite_cyber_dragon'),
    (0x08056a6c, 0x00001708, 'ORCA_MEGA_FORTRESS_OF_DARKNESS_CID', 'tick_equip_score_sprite_orca'),
    (0x08056a70, 0x0000140b, 'INSECT_IMITATION_CID', 'tick_equip_score_sprite_insect_imitation'),
    (0x08056a88, 0x000014e4, 'BURST_BREATH_CID', 'tick_equip_score_sprite_burst_breath'),
    (0x08056aa4, 0x00001927, 'SPIRITUAL_EARTH_ART_CID', 'tick_equip_score_sprite_earth_art'),
    (0x08056aa8, 0x00001768, 'NINJITSU_ART_OF_TRANSFORMATION_CID', 'tick_equip_score_sprite_ninjitsu'),
    (0x08056abc, 0x00001929, 'SPIRITUAL_FIRE_ART_CID', 'tick_equip_score_sprite_fire_art'),
    (0x08056c2c, 0x000015e7, 'POISON_OF_THE_OLD_MAN_CID', 'dispatch_equip_score_poison_old_man_a'),
    (0x08056c30, 0x00001298, 'CYBER_RAIDER_CID', 'dispatch_equip_score_cyber_raider_a'),
    (0x08056c48, 0x000015cf, 'KIRYU_CID', 'dispatch_equip_score_kiryu_a'),
    (0x08056c50, 0x000015d3, 'SECOND_GOBLIN_CID', 'dispatch_equip_score_second_goblin_a'),
    (0x08056c74, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'dispatch_equip_score_judgement_pharaoh_a'),
    (0x08056c90, 0x00001841, 'NECKLACE_OF_COMMAND_CID', 'dispatch_equip_score_necklace_a'),
    (0x08056c9c, 0x00001916, 'PROTECTIVE_SOUL_AILIN_CID', 'dispatch_equip_score_ailin_a'),
    (0x08056d58, 0x000013f2, 'EQUIP_LOCKDOWN_CID', 'dispatch_equip_score_lockdown'),
    (0x08056d84, 0x000015d3, 'SECOND_GOBLIN_CID', 'dispatch_equip_score_second_goblin_b'),
    (0x08056db8, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'dispatch_equip_score_banisher'),
    (0x08056e28, 0x0000167a, 'FRIENDSHIP_CID', 'dispatch_equip_score_friendship'),
    (0x08056e2c, 0x0000167b, 'UNITY_CID', 'dispatch_equip_score_unity'),
    (0x08056ecc, 0x0000178b, 'PROTECTOR_OF_THE_SANCTUARY_CID', 'dispatch_equip_score_protector_sanctuary'),
    (0x08056f00, 0x00001599, 'CARD_SHUFFLE_CID', 'dispatch_equip_score_card_shuffle_a'),
    (0x08056f04, 0x00001298, 'CYBER_RAIDER_CID', 'dispatch_equip_score_cyber_raider_b'),
    (0x08056f18, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'dispatch_equip_score_judgement_pharaoh_b'),
    (0x08057008, 0x000015d3, 'SECOND_GOBLIN_CID', 'dispatch_equip_score_second_goblin_c'),
    (0x08057014, 0x000015cf, 'KIRYU_CID', 'dispatch_equip_score_kiryu_b'),
    (0x0805702c, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'dispatch_equip_score_judgement_pharaoh_c'),
    (0x08057038, 0x00001916, 'PROTECTIVE_SOUL_AILIN_CID', 'dispatch_equip_score_ailin_b'),
    (0x08057100, 0x000015d3, 'SECOND_GOBLIN_CID', 'dispatch_equip_score_second_goblin_d'),
    (0x08057158, 0x000012a1, 'PARASITE_PARACIDE_CID', 'tick_equip_activation_state_parasite'),
    (0x08057234, 0x000014de, 'THE_DRAGONS_BEAD_CID', 'tick_equip_activation_state_dragons_bead'),
    (0x08057238, 0x000012f3, 'ULTIMATE_OFFERING_CID', 'tick_equip_activation_state_ultimate_offering'),
    (0x08057244, 0x00001624, 'PITCH_BLACK_POWER_STONE_CID', 'tick_equip_activation_state_pitch_black_ps'),

    # ==== RENAME_as_EQ: 3 slots -- new constants in duel_field.inc ====
    # DWORD_08056638 -> EQUIP_SPRITE_CARD_DATA = 0x1119
    (0x08056638, 0x00001119, 'EQUIP_SPRITE_CARD_DATA', 'enqueue_equip_card_sprite_mode3_card_data'),
    # DAT_08056bf0 -> EQUIP_ACT_SCORE_MODE_103 = 0x103
    (0x08056bf0, 0x00000103, 'EQUIP_ACT_SCORE_MODE_103', 'dispatch_equip_activation_score_by_card_id_mode_a'),
    # DAT_08056d20 -> EQUIP_ACT_SCORE_MODE_117 = 0x117
    (0x08056d20, 0x00000117, 'EQUIP_ACT_SCORE_MODE_117', 'dispatch_equip_activation_score_by_card_id_mode_b'),
]

# EOL comments for selected EQ slots
EQ_EOL = {
    0x08056638: "enqueue_sprite_attr_with_mode arg r2=card_data fixed 0x1119; mode=3",
    0x08056bf0: "set_equip_activation_state_by_mode mode code 0x103; loaded into r8 via mov r8,r0 (.hword 0x4680)",
    0x08056d20: "set_equip_activation_state_by_mode mode code 0x117; loaded into r8 via mov r8,r1 (.hword 0x4688)",
    0x08056950: "sub sp,#0x200 idiom: add sp,r4 where r4=0xfffffe00 (= -512); stack frame alloc",
    0x08056a74: "in BST context = card_id 0x0fff (Catapult Turtle slot); C5 dedup -> SCENE_SLOT_MASK_LO",
}

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER label at target; DATA ref slot->target; renames slot.
#    Note: for fn-ptr slots, target_addr is the function base (even), stored value = base|1.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # ---- gP1LifePoints PTR_ slots (16) ----
    (0x08056a60, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_score_sprite_display_seq_gp1lp'),
    (0x08056d18, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_b_gp1lp'),
    (0x08056d50, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_c_gp1lp'),
    (0x08056e58, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_d_gp1lp'),
    (0x08056ec0, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_e_gp1lp'),
    (0x08056f38, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_f_gp1lp'),
    (0x08056f54, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_g_gp1lp'),
    (0x08056f70, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_h_gp1lp'),
    (0x08056f80, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_i_gp1lp'),
    (0x08056fe4, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_activation_score_j_gp1lp'),
    (0x080571bc, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_activation_state_by_phase_gp1lp_a'),
    (0x080571e4, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_activation_state_by_phase_gp1lp_b'),
    (0x08057204, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_activation_state_by_phase_gp1lp_c'),
    (0x08057230, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_activation_state_by_phase_gp1lp_d'),
    (0x0805733c, 0x0201c4e0, 'gP1LifePoints', 'traverse_equip_zone_nodes_for_lp_score_gp1lp'),
    (0x08057414, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_zone14_test_display_seq_gp1lp'),

    # ---- gP1LifePoints DWORD_ slots (4): Ghidra still labels DWORD_, asm already correct ----
    (0x0805673c, 0x0201c4e0, 'gP1LifePoints', 'trigger_equip_lp_sprite_by_activation_state_gp1lp_c'),
    (0x0805678c, 0x0201c4e0, 'gP1LifePoints', 'trigger_equip_lp_sprite_by_activation_state_gp1lp_d'),
    (0x0805680c, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_card_name_display_by_step_gp1lp_b'),
    (0x08056858, 0x0201c4e0, 'gP1LifePoints', 'dispatch_equip_card_name_display_by_step_gp1lp_c'),

    # ---- fn-ptr REF slots (3): stored value = target_fn_addr | 1 ----
    # 0x0805697c: invoke_effect_node_handler_3arg+1 (asm/11 line 11787)
    (0x0805697c, 0x080905e8, 'invoke_effect_node_handler_3arg',
     'tick_equip_score_sprite_display_seq_mode_fn'),
    # 0x080569ec: check_equip_slot_eligible_by_card_id_tree+1 (asm/05 line 17731)
    (0x080569ec, 0x08050eac, 'check_equip_slot_eligible_by_card_id_tree',
     'tick_equip_score_sprite_display_seq_fallback_fn'),
    # 0x080573cc: invoke_effect_node_handler_3arg+1 (2nd usage)
    (0x080573cc, 0x080905e8, 'invoke_effect_node_handler_3arg',
     'tick_equip_zone14_test_display_seq_mode_fn'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    P5: enqueue_equip_slot_sprite_mode4 (0x08057344)
#    Two stale FUN_ substring replacements (plate is ASCII, no CJK).
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    (0x08057344, 'FUN_0805663c', 'tick_equip_activation_with_slot_sprite_mode4'),
    (0x08057344, 'FUN_080563cc', 'tick_equip_activation_state_machine'),
]

# ---------------------------------------------------------------------------
# E. PLATE_SET: (func_entry_addr, new_plate_text)
#    P0-P4: 5 full ASCII plate rewrites (CJK mojibake lines + stale FUN_ in P0)
#    Pure ASCII text only -- no CJK allowed in Ghidra comments (Jython mojibake).
# ---------------------------------------------------------------------------
PLATE_SET = [
    # P0: tick_equip_activation_with_lp_cost_sprite (0x080565e8)
    # Line 7237: CJK mojibake + stale FUN_08057430
    (0x080565e8,
     'Wrapper: calls tick_equip_activation_state_machine; if returns 1 (slot selected), extracts\n'
     'player_id (bit0) from card_entry[+2], calls get_card_lp_cost_by_id to get LP cost for active\n'
     'card, then calls enqueue_sprite_attr_clamped(player_id, lp_cost) to enqueue LP-cost sprite attr.\n'
     'Always passes through tick return value.\n'
     'Called by tick_equip_activation_lp_cost_sprite_by_type when bits[11:6]==type_code matches.'),

    # P1: tick_equip_activation_with_slot_sprite_mode4 (0x0805663c)
    # Line 7297: CJK mojibake
    (0x0805663c,
     'Wrapper: calls tick_equip_activation_state_machine; if returns 1 (slot selected), calls\n'
     'enqueue_equip_slot_sprite_mode4(card_entry_ptr, secondary_ptr) to enqueue mode=4 equip zone\n'
     'slot sprite. Passes through tick return value.\n'
     'indeg=0, Sub-type A (no direct callers in callgraph; not in fn-ptr table).'),

    # P2: tick_equip_activation_with_type11_sprite (0x080566cc)
    # Line 7378: CJK mojibake
    (0x080566cc,
     'Wrapper: calls tick_equip_activation_state_machine; saves return to r5. If r5 < 0 (negative\n'
     'signal), extracts player_id (bit0) from card_entry[+2] and card_id (u16 at [+0]), then calls\n'
     'enqueue_sprite_attr_type11(player_id, card_id, 1, 0) to enqueue type11 sprite attr.\n'
     'Passes through r5 return value.\n'
     'indeg=0, Sub-type A.'),

    # P3: tick_equip_activation_if_neo_daedalus_eligible (0x08057294)
    # Line 9157: CJK mojibake
    (0x08057294,
     'Conditional wrapper: calls check_neo_daedalus_placement_eligible(card_entry_ptr) first.\n'
     'If returns 0 (not eligible), immediately returns -1 (rsbs r0,r0,#0).\n'
     'If eligible, calls tick_equip_activation_state_machine and passes through its return value.\n'
     'indeg=0, Sub-type A.'),

    # P4: tick_equip_activation_lp_cost_sprite_by_type (0x08057430)
    # Line 9411: CJK mojibake
    (0x08057430,
     'Type-gate stub: reads card_entry[+2] bits[11:2] (mask 0xfc0) to extract slot_type_code.\n'
     'If slot_type_code != 0x580 (0xb0<<3), returns 1 immediately (skip).\n'
     'If matches, forwards r0/r1 to tick_equip_activation_with_lp_cost_sprite and passes through\n'
     'its return value. Used as fn-ptr table entry for type-conditional LP-cost sprite dispatch.'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
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
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF06Seg5Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm      = currentProgram.getSymbolTable()
    nA = nB = nD = nE = 0
    made_targets = set()
    fail_count = 0

    # --- A. EQ_SLOTS ---
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
        # Apply EOL if defined
        eol = EQ_EOL.get(slot_int)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # --- B. REF_SLOTS ---
    print("--- B. REF_SLOTS (%d slots) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        ok, err = _check(slot_int, tgt_int)
        if not ok:
            # fn-ptr slots store odd addr (THUMB): check for base|1 variant
            ok2, _ = _check(slot_int, tgt_int | 1)
            if not ok2:
                print("[B FAIL] 0x%08x: %s (target=%s want=0x%x)" % (slot_int, err, gas_label, tgt_int))
                fail_count += 1
                continue
        if DRY:
            print("[B dry] 0x%08x -> %s (0x%08x) slot_label=%s" % (slot_int, gas_label, tgt_int, slot_label))
            nB += 1
            continue
        target_addr = _addr(tgt_int)
        if tgt_int not in made_targets:
            createLabel(target_addr, gas_label, True, SourceType.USER_DEFINED)
            made_targets.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s @ 0x%08x)" % (slot_int, slot_label, gas_label, tgt_int))
        nB += 1

    # --- D. PLATE_SUBS ---
    print("--- D. PLATE_SUBS (%d items) ---" % len(PLATE_SUBS))
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int)
            fail_count += 1
            continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[D FAIL] no plate @ 0x%08x" % func_int)
            fail_count += 1
            continue
        if old_s not in plate:
            print("[D WARN->FAIL] '%s' not found in plate @ 0x%08x" % (old_s, func_int))
            fail_count += 1
            continue
        if DRY:
            print("[D dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nD += 1
            continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
        nD += 1

    # --- E. PLATE_SET (full rewrite) ---
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

    print("[done] A=%d B=%d D=%d E=%d FAIL=%d (DRY=%s)" % (nA, nB, nD, nE, fail_count, DRY))
    if fail_count > 0:
        print("[WARN] %d FAIL(s) above -- review before using non-dry run" % fail_count)


main()
