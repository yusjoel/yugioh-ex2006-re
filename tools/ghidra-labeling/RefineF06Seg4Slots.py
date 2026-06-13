# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg4Slots.py -- F06 Seg-4 (0x08055440..0x080565e8)
#   ROM range: check_equip_slot_same_player_type_mismatch .. tick_equip_activation_with_lp_row_type8_entry
#   22 fn, 153 slots (149 DAT_/DWORD_ + 4 PTR_)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (PLAYER_BLOCK_STRIDE/gDuelFieldSlots/gDuelPhaseFlags/
#                   PHASE_LOCK_FLAG_OFF/EQUIP_ACTIVATION_STEP_OFF reuse + 55 new CID +
#                   4 new duel_field.inc + LP cost reuse/new + 22 RENAME scores via EQ)
#   B. REF_SLOTS -- 5 slots (1 fn-ptr + 4 gP1LifePoints)
#   C. RENAME_SLOTS -- 3 DWORD_ slots in tick_equip_activation_with_lp_row_type8_entry
#   D. PLATE_SUBS -- P4: trigger_lp_row_type2_if_equip_tier_nonzero (2 FUN_ subst)
#   E. PLATE_SET  -- P1: tick_equip_activation_state_machine (full ASCII rewrite, CJK mojibake)
#                    P2: tick_equip_activation_with_lp_row_type8_entry (full ASCII rewrite, CJK mojibake)
#
# New constants added to constants files (done before running this script):
#   card_info.inc: 55 new CIDs (verified C5 0-hit against existing)
#   duel_field.inc: EQUIP_ACTIVATION_STEP_OFF=0x4ac / TRIGGER_OP_PARAM_107=0x107 /
#                   LP_COST_5000=0x1388 / EQUIP_ZONE_SPRITE_ATTR=0xfb6
#
# Note: slot 0x08055770 appears in both EQ_SLOTS (fn-ptr row) and REF_SLOTS;
#       it is the fn-ptr slot. EQ_SLOTS row for it is SKIPPED (handled by REF_SLOTS).

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
    # ==== Seg-4a (0x08055440..0x08055ebc) ====

    # PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) x10
    (0x08055490, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'same_player_type_mismatch_stride'),
    (0x08055514, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_cross_player_and_field6_zero_stride'),
    (0x08055580, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_cross_player_state7_type_eligible_stride'),
    (0x08055608, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_same_side_whitelist_and_space_stride'),
    (0x080556d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_rival_appears_effect_stride'),
    (0x08055768, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_activation_and_zone_pair_stride'),
    (0x080557b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_zone_present_with_score_match_stride'),
    (0x08055854, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_bst_special_cases_stride'),
    (0x08055c70, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'classify_equip_card_id_tier_abce_stride'),

    # gDuelFieldSlots = 0x0201c510 (ewram.inc) x9
    (0x08055494, 0x0201c510, 'gDuelFieldSlots', 'same_player_type_mismatch_slots'),
    (0x08055518, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_cross_player_and_field6_zero_slots'),
    (0x08055584, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_cross_player_state7_type_eligible_slots'),
    (0x0805560c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_same_side_whitelist_and_space_slots'),
    (0x080556d8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_rival_appears_effect_slots'),
    (0x0805576c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_activation_and_zone_pair_slots'),
    (0x080557b4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_zone_present_with_score_match_slots'),
    (0x08055858, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_bst_special_cases_slots'),

    # gDuelPhaseFlags = 0x0201b290 (ewram.inc) x5
    (0x08055610, 0x0201b290, 'gDuelPhaseFlags', 'check_equip_slot_eligible_by_same_side_whitelist_and_space_phase_flags'),

    # PHASE_LOCK_FLAG_OFF = 0x000004bc (duel_field.inc) x2
    (0x08055614, 0x000004bc, 'PHASE_LOCK_FLAG_OFF', 'check_equip_slot_eligible_by_same_side_whitelist_and_space_phase_lock'),

    # CID equates -- Seg-4a existing/reuse
    (0x080556dc, 0x0000192b, 'A_RIVAL_APPEARS_CID', 'check_equip_slot_eligible_by_rival_appears_effect_cid'),
    (0x0805585c, 0x00001669, 'STAUNCH_DEFENDER_CID', 'check_equip_slot_eligible_by_card_id_bst_special_cases_staunch_def'),
    (0x08055870, 0x00001908, 'BUBBLE_SHUFFLE_CID', 'check_equip_slot_eligible_by_card_id_bst_special_cases_bubble_shuf'),
    (0x080558cc, 0x000013cd, 'LEGENDARY_FISHERMAN_CID', 'check_equip_slot_eligible_by_card_id_bst_special_cases_leg_fish'),
    (0x080558d0, 0x0000164e, 'GUARDIAN_KAYEST_CID', 'check_equip_slot_eligible_by_card_id_bst_special_cases_gk'),
    (0x080558e4, 0x000010f4, 'UMI_CARD_ID', 'check_equip_slot_eligible_by_card_id_bst_special_cases_umi'),
    (0x080558fc, 0x000018f9, 'EHERO_BUBBLEMAN_CID', 'check_equip_slot_eligible_by_card_id_bst_special_cases_bubbleman'),
    (0x0805596c, 0x000017a3, 'SPELL_ECONOMICS_CID', 'get_card_lp_cost_by_id_spell_economics'),
    (0x080559b4, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID', 'get_card_lp_cost_by_id_diffusion_wm'),
    (0x080559b8, 0x00001325, 'DELINQUENT_DUO_CID', 'get_card_lp_cost_by_id_delinquent_duo'),
    (0x080559bc, 0x000011cf, 'get_card_lp_cost_by_id_cid_11cf', 'get_card_lp_cost_by_id_gap_11cf'),
    (0x080559d8, 0x00001190, 'get_card_lp_cost_by_id_cid_1190', 'get_card_lp_cost_by_id_gap_1190'),
    (0x08055a04, 0x000012de, 'DARK_MAGIC_CURTAIN_CID', 'get_card_lp_cost_by_id_dark_magic_curtain'),
    (0x08055a0c, 0x000012c3, 'BRAIN_CONTROL_CID', 'get_card_lp_cost_by_id_brain_control'),
    (0x08055a20, 0x000012fd, 'SOLEMN_JUDGMENT_CID', 'get_card_lp_cost_by_id_solemn_judgment'),
    (0x08055a28, 0x000012ff, 'SEVEN_TOOLS_OF_THE_BANDIT_CID', 'get_card_lp_cost_by_id_seven_tools'),
    (0x08055a54, 0x000014be, 'BARK_OF_DARK_RULER_CID', 'get_card_lp_cost_by_id_bark_dark_ruler'),
    (0x08055a58, 0x000013a7, 'INJECTION_FAIRY_LILY_CID', 'get_card_lp_cost_by_id_inj_fairy_lily'),
    (0x08055a60, 0x00001393, 'get_card_lp_cost_by_id_cid_1393', 'get_card_lp_cost_by_id_gap_1393'),
    (0x08055a7c, 0x000014ab, 'AMAZONESS_CHAIN_MASTER_CID', 'get_card_lp_cost_by_id_amazoness_cm'),
    (0x08055a84, 0x000014b6, 'DARK_BALTER_THE_TERRIBLE_CID', 'get_card_lp_cost_by_id_dark_balter'),
    (0x08055aa4, 0x00001599, 'CARD_SHUFFLE_CID', 'get_card_lp_cost_by_id_card_shuffle'),
    (0x08055aac, 0x0000156a, 'PUPPET_MASTER_CID', 'get_card_lp_cost_by_id_puppet_master'),
    (0x08055ac0, 0x000015b5, 'ROPE_OF_SPIRIT_CID', 'get_card_lp_cost_by_id_rope_of_spirit'),
    (0x08055ad0, 0x000015e6, 'AUTONOMOUS_ACTION_UNIT_CID', 'get_card_lp_cost_by_id_auto_action_unit'),
    (0x08055b08, 0x000017bc, 'CRUSH_D_GANDRA_CID', 'get_card_lp_cost_by_id_crush_d_gandra'),
    (0x08055b0c, 0x000016a4, 'EQUIP_LOCK_A_CID', 'get_card_lp_cost_by_id_equip_lock_a'),
    (0x08055b14, 0x0000166c, 'SKILL_DRAIN_CID', 'get_card_lp_cost_by_id_skill_drain'),
    (0x08055b28, 0x0000169c, 'FINAL_COUNTDOWN_CID', 'get_card_lp_cost_by_id_final_countdown'),
    (0x08055b38, 0x0000169d, 'get_card_lp_cost_by_id_cid_169d', 'get_card_lp_cost_by_id_gap_169d'),
    (0x08055b58, 0x00001741, 'AGENT_OF_CREATION_VENUS_CID', 'get_card_lp_cost_by_id_agent_venus'),
    (0x08055b68, 0x00001712, 'DIMENSION_FUSION_CID', 'get_card_lp_cost_by_id_dim_fusion'),
    (0x08055b7c, 0x00001775, 'RETURN_ZOMBIE_CID', 'get_card_lp_cost_by_id_return_zombie'),
    (0x08055b88, 0x000017a7, 'ENCHANTING_FITTING_ROOM_CID', 'get_card_lp_cost_by_id_enchanting_fr'),
    (0x08055bb8, 0x000018cc, 'BATTERY_CHARGER_CID', 'get_card_lp_cost_by_id_battery_charger'),
    (0x08055bc0, 0x000017f4, 'ABYSSAL_DESIGNATOR_CID', 'get_card_lp_cost_by_id_abyssal_design'),
    (0x08055bf8, 0x00001975, 'DARK_DEAL_CID', 'get_card_lp_cost_by_id_dark_deal'),
    (0x08055c04, 0x00001932, 'TRIAGE_CID', 'get_card_lp_cost_by_id_triage'),
    (0x08055c1c, 0x000019d5, 'DEMISE_KING_OF_ARMAGEDDON_CID', 'get_card_lp_cost_by_id_demise_king'),
    (0x08055c30, 0x000019e2, 'MALFUNCTION_CID', 'get_card_lp_cost_by_id_malfunction'),

    # LP costs
    (0x08055c40, 0x000005dc, 'LP_COST_1500', 'get_card_lp_cost_by_id_lp_1500'),
    (0x08055c50, 0x00000bb8, 'LP_COST_3000', 'get_card_lp_cost_by_id_lp_3000'),
    (0x08055c58, 0x00001388, 'LP_COST_5000', 'get_card_lp_cost_by_id_lp_5000'),

    # classify_equip_card_id_tier_abce (0x08055cd0) CIDs
    (0x08055d08, 0x0000161c, 'TRIBE_INFECTING_VIRUS_CID', 'classify_equip_tier_abce_tribe_infecting'),
    (0x08055d0c, 0x000014de, 'THE_DRAGONS_BEAD_CID', 'classify_equip_tier_abce_dragons_bead'),
    (0x08055d1c, 0x00001321, 'FINAL_DESTINY_CID', 'classify_equip_tier_abce_final_destiny'),
    (0x08055d30, 0x00001470, 'JUDGMENT_OF_ANUBIS_CID', 'classify_equip_tier_abce_judgment_anubis'),
    (0x08055d40, 0x000014a7, 'ROPE_OF_LIFE_CID', 'classify_equip_tier_abce_rope_of_life'),
    (0x08055d60, 0x000015b4, 'XYZ_DRAGON_CANNON_CID', 'classify_equip_tier_abce_xyz_dragon'),
    (0x08055d70, 0x000015ad, 'NON_AGGRESSION_AREA_CID', 'classify_equip_tier_abce_non_aggress'),
    (0x08055d8c, 0x000015fa, 'YZ_TANK_DRAGON_CID', 'classify_equip_tier_abce_yz_tank'),
    (0x08055d94, 0x000015fc, 'DARK_PALADIN_CID', 'classify_equip_tier_abce_dark_paladin'),
    (0x08055dc0, 0x00001851, 'SPELL_PURIFICATION_CID', 'classify_equip_tier_abce_spell_purif'),
    (0x08055dc4, 0x000016a6, 'SPELL_VANISHING_CID', 'classify_equip_tier_abce_spell_vanish'),
    (0x08055dd4, 0x0000179e, 'SPECIAL_HURRICANE_CID', 'classify_equip_tier_abce_special_hurricane'),
    (0x08055df4, 0x00001844, 'BACK_TO_SQUARE_ONE_CID', 'classify_equip_tier_abce_back_sq1'),
    (0x08055e10, 0x0000190e, 'CYBERNETIC_MAGICIAN_CID', 'classify_equip_tier_abce_cyber_mage'),
    (0x08055e20, 0x0000188e, 'FORCED_CEASEFIRE_CID', 'classify_equip_tier_abce_forced_cease'),
    (0x08055e3c, 0x000019ae, 'ANCIENT_GEAR_DRILL_CID', 'classify_equip_tier_abce_ancient_gear_drill'),
    (0x08055e50, 0x000019b6, 'DAMAGE_CONDENSER_CID', 'classify_equip_tier_abce_dmg_condenser'),

    # classify_equip_card_id_tier_abc_short (0x08055e60) CIDs
    (0x08055e7c, 0x00001661, 'TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID', 'classify_equip_tier_abc_short_twin_sw'),
    (0x08055e80, 0x000014ea, 'SPELL_REPRODUCTION_CID', 'classify_equip_tier_abc_short_spell_repro'),
    (0x08055e8c, 0x0000165f, 'WICKED_BREAKING_FLAMBERGE_BAOU_CID', 'classify_equip_tier_abc_short_baou'),
    (0x08055ea0, 0x0000198c, 'ARMED_DRAGON_LV10_CID', 'classify_equip_tier_abc_short_armed_lv10'),
    (0x08055eac, 0x000019af, 'PHANTASMAL_MARTYRS_CID', 'classify_equip_tier_abc_short_phantasmal'),

    # ==== Seg-4b (0x08055ebc..0x080565e8) ====

    # classify_equip_card_id_tier_abcx (0x08055ebc) CIDs
    (0x08055edc, 0x00001617, 'BREAKER_MAGICAL_WARRIOR_CID', 'classify_equip_tier_abcx_breaker'),
    (0x08055ee0, 0x0000128e, 'HANNIBAL_NECROMANCER_CID', 'classify_equip_tier_abcx_hannibal'),
    (0x08055eec, 0x00001615, 'MAGICAL_MARIONETTE_CID', 'classify_equip_tier_abcx_magic_mario'),
    (0x08055f08, 0x00001631, 'MIRACLE_RESTORING_CID', 'classify_equip_tier_abcx_miracle_rest'),
    (0x08055f1c, 0x00001634, 'ANTI_SPELL_CID', 'classify_equip_tier_abcx_anti_spell'),

    # lookup_equip_card_score_by_card_id_and_player (0x08055f34) CIDs
    (0x08055f70, 0x000015cf, 'KIRYU_CID', 'lookup_equip_score_kiryu'),
    (0x08055f74, 0x00001388, 'lookup_equip_card_score_cid_1388', 'lookup_equip_score_gap_1388'),
    (0x08055f78, 0x000010f8, 'MOOYAN_CURRY_CID', 'lookup_equip_score_mooyan_curry'),
    (0x08055f80, 0x000012c6, 'cid_12c6', 'lookup_equip_score_cid_12c6'),
    (0x08055f9c, 0x000014fd, 'MAHARAGHI_CID', 'lookup_equip_score_maharaghi'),
    (0x08055fa4, 0x00001519, 'OMINOUS_FORTUNETELLING_CID', 'lookup_equip_score_ominous_ft'),
    (0x08055fcc, 0x00001544, 'DARK_COFFIN_CID', 'lookup_equip_score_dark_coffin'),
    (0x08055fd4, 0x0000153f, 'ORDEAL_OF_A_TRAVELER_CID', 'lookup_equip_score_ordeal_traveler'),
    (0x08055ff0, 0x00001599, 'CARD_SHUFFLE_CID', 'lookup_equip_score_card_shuffle'),
    (0x08056000, 0x000015a5, 'REVERSAL_QUIZ_CID', 'lookup_equip_score_reversal_quiz'),
    (0x08056034, 0x00001685, 'DARK_SCORPION_GORG_THE_STRONG_CID', 'lookup_equip_score_gorg'),
    (0x08056044, 0x000015f1, 'SPELL_SHIELD_TYPE8_CID', 'lookup_equip_score_spell_shield_t8'),
    (0x08056060, 0x00001656, 'DARK_SCORPION_CHICK_CID', 'lookup_equip_score_dsc_chick'),
    (0x08056070, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'lookup_equip_score_judgment_pharaoh'),
    (0x08056094, 0x00001776, 'CORPSE_OF_YATA_GARASU_CID', 'lookup_equip_score_corpse_yata'),
    (0x080560a0, 0x0000175a, 'MYSTIK_WOK_CID', 'lookup_equip_score_mystik_wok'),
    (0x080560bc, 0x0000184e, 'FUH_RIN_KA_ZAN_CID', 'lookup_equip_score_fuh_rin_ka_zan'),
    (0x080560d4, 0x00001916, 'PROTECTIVE_SOUL_AILIN_CID', 'lookup_equip_score_protective_ailin'),

    # Score literals -- Mooyan player 0/1 and A Rival Appears player 1
    (0x080560e8, 0x00000197, 'lookup_equip_score_mooyan_p0', 'lookup_equip_score_mooyan_p0_slot'),
    (0x08056100, 0x000001c7, 'lookup_equip_score_a_rival_appears_p1', 'lookup_equip_score_a_rival_p1_slot'),
    (0x08056118, 0x00000199, 'lookup_equip_score_mooyan_p1', 'lookup_equip_score_mooyan_p1_slot'),

    # Score literals 22 BST branches (lookup_equip_score_b)
    (0x0805613c, 0x000001ad, 'lookup_equip_score_b_0x1ad', 'lookup_equip_score_b_0x1ad_slot'),
    (0x0805616c, 0x000001b9, 'lookup_equip_score_b_0x1b9', 'lookup_equip_score_b_0x1b9_slot'),
    (0x08056198, 0x000001ab, 'lookup_equip_score_b_0x1ab', 'lookup_equip_score_b_0x1ab_slot'),
    (0x080561b0, 0x000001bf, 'lookup_equip_score_b_0x1bf', 'lookup_equip_score_b_0x1bf_slot'),
    (0x080561c8, 0x000001a9, 'lookup_equip_score_b_0x1a9', 'lookup_equip_score_b_0x1a9_slot'),
    (0x080561dc, 0x000001cd, 'lookup_equip_score_b_0x1cd', 'lookup_equip_score_b_0x1cd_slot'),
    (0x0805621c, 0x000001c3, 'lookup_equip_score_b_0x1c3', 'lookup_equip_score_b_0x1c3_slot'),
    (0x08056234, 0x000001c5, 'lookup_equip_score_b_0x1c5', 'lookup_equip_score_b_0x1c5_slot'),
    (0x08056248, 0x000001af, 'lookup_equip_score_b_0x1af', 'lookup_equip_score_b_0x1af_slot'),
    (0x08056250, 0x000001a7, 'lookup_equip_score_b_0x1a7', 'lookup_equip_score_b_0x1a7_slot'),
    (0x08056278, 0x000001b1, 'lookup_equip_score_b_0x1b1', 'lookup_equip_score_b_0x1b1_slot'),
    (0x08056288, 0x000001b7, 'lookup_equip_score_b_0x1b7', 'lookup_equip_score_b_0x1b7_slot'),
    (0x080562a0, 0x000001c9, 'lookup_equip_score_b_0x1c9', 'lookup_equip_score_b_0x1c9_slot'),
    (0x080562b8, 0x000001b3, 'lookup_equip_score_b_0x1b3', 'lookup_equip_score_b_0x1b3_slot'),
    (0x080562d0, 0x000001b5, 'lookup_equip_score_b_0x1b5', 'lookup_equip_score_b_0x1b5_slot'),
    (0x08056318, 0x000001cb, 'lookup_equip_score_b_0x1cb', 'lookup_equip_score_b_0x1cb_slot'),
    (0x08056320, 0x000001a5, 'lookup_equip_score_b_0x1a5', 'lookup_equip_score_b_0x1a5_slot'),
    (0x08056328, 0x000001c1, 'lookup_equip_score_b_0x1c1', 'lookup_equip_score_b_0x1c1_slot'),
    (0x0805634c, 0x000001cf, 'lookup_equip_score_b_0x1cf', 'lookup_equip_score_b_0x1cf_slot'),

    # enqueue_equip_zone_sprite_at_slot (0x080563a4)
    (0x080563c8, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR', 'enqueue_equip_zone_sprite_attr'),

    # tick_equip_activation_state_machine (0x080563cc) Seg-4b gDuelPhaseFlags / step / param / ctx
    (0x080563f8, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_activation_sm_phase_flags'),
    (0x080563fc, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_activation_sm_step_off_a'),
    (0x08056420, 0x00000107, 'TRIGGER_OP_PARAM_107', 'tick_equip_activation_sm_trigger_param'),
    (0x08056450, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_activation_sm_card_ctx'),

    # BST card IDs in tick_equip_activation_state_machine
    (0x08056474, 0x000010e7, 'MALEVOLENT_NUZZLER_CID', 'tick_equip_activation_sm_malev_nuzzler'),
    (0x08056488, 0x00001294, 'CHIMERA_FLYING_MYTHICAL_BEAST_CID', 'tick_equip_activation_sm_chimera'),
    (0x080564bc, 0x000012a1, 'PARASITE_PARACIDE_CID', 'tick_equip_activation_sm_parasite'),

    # tick_equip_activation_state_machine gDuelPhaseFlags/step  (2nd occurrence)
    (0x080564c0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_activation_sm_phase_flags_b'),
    (0x080564c4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_activation_sm_step_off_b'),

    # dispatch_equip_zone_sprite_by_card_in_zone (0x0805652c)
    (0x080564ec, 0x000017cc, 'WATAPON_CID', 'dispatch_equip_zone_sprite_watapon'),
    (0x08056510, 0x0000190a, 'DARK_RULER_VANDALGYON_CID', 'dispatch_equip_zone_sprite_vandalgyon'),
    (0x08056514, 0x000010d6, 'AXE_OF_DESPAIR_CID', 'dispatch_equip_zone_sprite_axe_despair'),

    # set_equip_activation_player_state_bit (0x08056558) gDuelPhaseFlags/step
    (0x08056518, 0x0201b290, 'gDuelPhaseFlags', 'set_equip_activation_player_bit_phase_flags'),
    (0x0805651c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'set_equip_activation_player_bit_step_off'),

    # enqueue_lp_display_row_from_card_byte2 (0x08056578): ELIGIB_SPRITE_CTRL_OFF
    (0x08056574, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'enqueue_lp_display_row_sprite_ctrl_off'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # fn-ptr: 0x08055770 = check_equip_slot_eligible_by_type_and_card_id_pair + 1 (THUMB)
    # target fn is at asm/05 0x080525d0; fn-ptr = +1 (odd addr = THUMB)
    (0x08055770, 0x080525d0, 'check_equip_slot_eligible_by_type_and_card_id_pair',
     'check_equip_slot_eligible_by_setcode_activation_and_zone_pair_fn_ptr'),

    # gP1LifePoints = 0x0201c4e0 (ewram.inc) x4 -- PTR_ slots
    (0x08055c6c, 0x0201c4e0, 'gP1LifePoints', 'get_card_lp_cost_by_id_gp1lp'),
    (0x08056454, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_activation_gp1lp_a'),
    (0x080564e8, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_activation_gp1lp_b'),
    (0x08056570, 0x0201c4e0, 'gP1LifePoints', 'set_equip_activation_player_state_bit_gp1lp'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    DWORD_ slots in tick_equip_activation_with_lp_row_type8_entry (0x08056598)
#    These will also be covered by EQ via EQUIP_ACTIVATION_STEP_OFF + gDuelPhaseFlags;
#    RENAME used as fallback label for the slot address itself.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x080565bc, 'tick_lp_row_type8_entry_duel_state',
     'gDuelPhaseFlags base; loaded with EQUIP_ACTIVATION_STEP_OFF'),
    (0x080565c0, 'tick_lp_row_type8_entry_step_off',
     'EQUIP_ACTIVATION_STEP_OFF = 0x4ac'),
    (0x080565dc, 'tick_lp_row_type8_entry_all_slots_mask',
     '0xffff = LP_ROW_ALL_SLOTS_MASK'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    P4: trigger_lp_row_type2_if_equip_tier_nonzero (0x08056380)
#    Two stale FUN_ references to replace.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    (0x08056380, 'FUN_0805715c', 'tick_equip_activation_state_by_phase'),
    (0x08056380, 'FUN_08059be0', 'enqueue_equip_zone_sprite_with_lp_tier'),
]

# ---------------------------------------------------------------------------
# E. PLATE_SET: (func_entry_addr, new_plate_text)
#    P1: tick_equip_activation_state_machine (0x080563cc) -- CJK mojibake full rewrite
#    P2: tick_equip_activation_with_lp_row_type8_entry (0x08056598) -- CJK mojibake full rewrite
#    Pure ASCII text only.
# ---------------------------------------------------------------------------
PLATE_SET = [
    # P1: tick_equip_activation_state_machine
    (0x080563cc,
     'Equip activation per-frame state machine hub, indeg=11.\n'
     'Params: r0=card_entry_ptr, r1=second_param (encodes player/slot).\n'
     'Reads [gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF] for current step (0/1/2).\n'
     'Step 0: checks find_zone_slot_match_by_type_in_node_list; if found,\n'
     '  calls trigger_card_display_op31_if_not_active(player_id, TRIGGER_OP_PARAM_107), returns -1.\n'
     '  Else calls dispatch_card_effect_activation; if nonzero, reads\n'
     '  [gDuelCardCtxBase+player*4+8]: if ==1 calls dispatch_card_effect_by_card_id,\n'
     '  writes result to gP1LifePoints+0x1d40; else BST-dispatches on card_id\n'
     '  (MALEVOLENT_NUZZLER/AXE_OF_DESPAIR/CHIMERA/PARASITE_PARACIDE/\n'
     '   DARK_RULER_VANDALGYON + others) to text_format_code, calls\n'
     '  card_name_lookup_by_internal_id + format_game_text_with_text_arg +\n'
     '  invoke_card_display_op_0x31_sub1.\n'
     'Step 1 (LP wait): checks gP1LifePoints+0x1d40==0; if so calls\n'
     '  set_lp_display_row_all_slots by card_id (WATAPON/DARK_RULER_VANDALGYON).\n'
     'Step 2: increments [gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF].\n'
     'Returns -1=done, 0=wait, 1=step-advance.'),

    # P2: tick_equip_activation_with_lp_row_type8_entry
    (0x08056598,
     'Equip activation entry wrapper with LP display row type8 init.\n'
     'Called by tick_equip_activation_lp_cost_sprite_by_type (indeg=1).\n'
     'Reads gDuelPhaseFlags+EQUIP_ACTIVATION_STEP_OFF step counter.\n'
     'state==0xa: extracts player_id from card_entry[+2] bit0,\n'
     '  calls set_lp_display_row_type8(player_id, 0xffff, 1),\n'
     '  advances counter to 0xb; returns 0.\n'
     'state==0xb: returns 1 (sequence complete).\n'
     'other: calls tick_equip_activation_state_machine(card_entry);\n'
     '  if returns 1, sets counter to 0xa (next phase). Returns 0.'),
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
    print("=== RefineF06Seg4Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm      = currentProgram.getSymbolTable()
    nA = nB = nC = nD = nE = 0
    made_targets = set()

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS (%d slots) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s want=0x%x)" % (slot_int, err, cname, value))
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

    # --- B. REF_SLOTS ---
    print("--- B. REF_SLOTS (%d slots) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        ok, err = _check(slot_int, tgt_int)
        if not ok:
            # fn-ptr slots store odd addr; check for +1 variant
            ok2, _ = _check(slot_int, tgt_int + 1)
            if not ok2:
                print("[B FAIL] 0x%08x: %s (target=%s want=0x%x)" % (slot_int, err, gas_label, tgt_int))
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

    # --- C. RENAME_SLOTS ---
    print("--- C. RENAME_SLOTS (%d slots) ---" % len(RENAME_SLOTS))
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int)
            continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label))
            nC += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label))
        nC += 1

    # --- D. PLATE_SUBS ---
    print("--- D. PLATE_SUBS (%d items) ---" % len(PLATE_SUBS))
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int)
            continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[D FAIL] no plate @ 0x%08x" % func_int)
            continue
        if old_s not in plate:
            print("[D WARN->FAIL] '%s' not found in plate @ 0x%08x" % (old_s, func_int))
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
            continue
        if DRY:
            print("[E dry] 0x%08x full plate rewrite (%d chars)" % (func_int, len(new_text)))
            nE += 1
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("[E ok] 0x%08x plate set (%d chars)" % (func_int, len(new_text)))
        nE += 1

    print("[done] A=%d B=%d C=%d D=%d E=%d FAIL=check-above (DRY=%s)" % (nA, nB, nC, nD, nE, DRY))


main()
