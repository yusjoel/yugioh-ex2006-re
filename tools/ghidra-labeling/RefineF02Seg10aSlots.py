# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg10aSlots.py -- file 02 Seg-10a (0x0803407c..0x08035280)
#   slot activation eligibility check cluster (10 functions):
#   eval_slot_target_eligibility_full / check_card_matches_active_effect_slot /
#   find_paired_zone_entry_for_card / check_card_targeted_by_spell_zone_effect /
#   check_slot_field_action_eligibility / check_field_spell_slot_placeable /
#   check_slot_monster_activation_eligible / eval_slot_activation_guard_full /
#   check_slot_card_activatable / check_slot_full_activation_eligibility
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (40 reuse + 17 new)  total=57
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename  total=11
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)  total=80
#   D. (no PLATE_REWRITES -- PLATE=0, no FUN_ stale text in segment)
#
# New constants:
#   duel_field.inc: ACTIVATION_STATE_A_OFF=0x1d48, ACTIVATION_STATE_B_OFF=0x1d78,
#                   ACTIVE_EFFECT_CATEGORY_OFF=0x10d8
#   card_info.inc: UMI_CARD_ID=0x10f4, A_LEGENDARY_OCEAN_CARD_ID=0x150b,
#                  SPELL_ZONE_TARGET_CARD_ID=0x1368, TOTAL_DEFENSE_SHOGUN_CARD_ID=0x12b4,
#                  EHERO_RAMPART_BLASTER_CARD_ID=0x1956, TWINHEADED_BEAST_CARD_ID=0x1723,
#                  TYRANT_DRAGON_CARD_ID=0x14d5, ARMED_SAMURAI_BEN_KEI_CARD_ID=0x186c
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
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- Group A: Reuse existing constants ---
    # PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc or duel_field.inc)
    (0x080340bc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_target_eligibility_full_stride',
     'inter-player block stride 0x868'),
    (0x080340c0, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_target_eligibility_full_slots', None),
    (0x08034124, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_slot_target_eligibility_full_stride_b', None),
    (0x08034128, 0x0201c510, 'gDuelFieldSlots',
     'eval_slot_target_eligibility_full_slots_b', None),
    (0x080341b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_paired_zone_entry_for_card_stride', None),
    (0x080341b4, 0x0201c510, 'gDuelFieldSlots',
     'find_paired_zone_entry_for_card_slots', None),
    (0x0803428c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_paired_zone_entry_for_card_stride_b', None),
    (0x08034290, 0x0201c510, 'gDuelFieldSlots',
     'find_paired_zone_entry_for_card_slots_b', None),
    (0x08034348, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_card_targeted_by_spell_zone_effect_stride', None),
    (0x0803434c, 0x0201c520, 'gDuelFieldSlotState',
     'check_card_targeted_spell_zone_slot_state', None),
    (0x08034350, 0x0201c510, 'gDuelFieldSlots',
     'check_card_targeted_spell_zone_slots', None),
    (0x080343a8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_field_action_eligibility_stride', None),
    (0x080343ac, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_field_action_eligibility_slots', None),
    (0x080343b0, 0x0201e2a0, 'gDuelCardCtxBase',
     'check_slot_field_action_eligibility_ctx', None),
    (0x08034518, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_field_action_eligibility_stride_b', None),
    (0x0803451c, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_field_action_eligibility_slots_b', None),
    (0x08034524, 0x0201e2a0, 'gDuelCardCtxBase',
     'check_slot_field_action_eligibility_ctx_b', None),
    (0x080345a0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_field_action_eligibility_stride_c', None),
    (0x080345a4, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_field_action_eligibility_slots_c', None),
    (0x080345d4, 0x0201e2a0, 'gDuelCardCtxBase',
     'check_slot_field_action_eligibility_ctx_c', None),
    (0x08034674, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_field_spell_slot_placeable_stride', None),
    (0x08034678, 0x0201c510, 'gDuelFieldSlots',
     'check_field_spell_slot_placeable_slots', None),
    (0x08034738, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_monster_activation_stride', None),
    (0x08034868, 0x0201bb90, 'gEquipChainSlotRefs',
     'check_slot_monster_activation_equip_refs', None),
    (0x08034880, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_monster_activation_stride_b', None),
    (0x08034884, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_monster_activation_slots_b', None),
    (0x080348dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_monster_activation_stride_c', None),
    (0x080348e0, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_monster_activation_slots_c', None),
    (0x080349f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_card_activatable_stride', None),
    (0x080349fc, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_card_activatable_slots', None),
    (0x08034acc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_full_activation_eligibility_stride', None),
    (0x08034ad0, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_full_activation_eligibility_slots', None),
    (0x08034ad4, 0x0201e2a0, 'gDuelCardCtxBase',
     'check_slot_full_activation_eligibility_ctx', None),
    (0x08034e40, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_full_activation_stride_d', None),
    (0x08034e68, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_full_activation_slots_d', None),
    (0x08034f14, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_full_activation_stride_e', None),
    (0x08034f68, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_full_activation_stride_f', None),
    (0x0803513c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_full_activation_stride_g', None),
    (0x08035158, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'check_slot_full_activation_p2_base', None),
    (0x08035278, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_full_activation_stride_h', None),

    # --- Group B: Reuse existing card_info.inc constants ---
    (0x0803467c, 0x0000164f, 'EQUIP_CHAIN_PAIR_CARD_MAX',
     'check_field_spell_slot_placeable_cmax',
     'max card_id for chain pairing path'),
    (0x08035150, 0x000012d1, 'EQUIP_LOCK_B_CID',
     'check_slot_full_activation_equip_lock_b',
     'equip lock chain effect B CID'),

    # --- Group C: New constants -> card_info.inc ---
    (0x0803414c, 0x000010f4, 'UMI_CARD_ID',
     'check_card_matches_active_effect_umi_cid',
     'Umi field spell CID (pw=22702055); special proxy activation'),
    (0x08034794, 0x000010f4, 'UMI_CARD_ID',
     'check_slot_monster_activation_umi_cid', None),
    (0x08034154, 0x0000150b, 'A_LEGENDARY_OCEAN_CARD_ID',
     'check_card_matches_proxy_ocean_cid',
     'A Legendary Ocean CID (pw=295517); proxy reference for Umi activation'),
    (0x08034294, 0x00001368, 'SPELL_ZONE_TARGET_CARD_ID',
     'find_paired_zone_target_cid',
     'cross-player spell-zone effect node type ID'),
    (0x08034354, 0x00001368, 'SPELL_ZONE_TARGET_CARD_ID',
     'check_card_targeted_spell_zone_cid', None),
    (0x08034a00, 0x000012b4, 'TOTAL_DEFENSE_SHOGUN_CARD_ID',
     'check_slot_card_activatable_tds_cid',
     'Total Defense Shogun CID (pw=75372290); slot[+0x10] bit5 activation'),
    (0x08034a04, 0x00001956, 'EHERO_RAMPART_BLASTER_CARD_ID',
     'check_slot_card_activatable_erb_cid',
     'E-Hero Rampart Blaster CID (pw=47737087); inverted bit5 + zone count'),
    (0x0803473c, 0x00001723, 'TWINHEADED_BEAST_CARD_ID',
     'check_slot_monster_activation_thb_cid',
     'Twinheaded Beast CID (pw=82035781)'),
    (0x08034740, 0x000014d5, 'TYRANT_DRAGON_CARD_ID',
     'check_slot_monster_activation_td_cid',
     'Tyrant Dragon CID (pw=94568601)'),
    (0x080348e4, 0x0000186c, 'ARMED_SAMURAI_BEN_KEI_CARD_ID',
     'check_slot_monster_activation_asbk_cid',
     'Armed Samurai - Ben Kei CID (pw=84430950)'),

    # --- Group D: New constants -> duel_field.inc ---
    (0x080343b4, 0x00001d48, 'ACTIVATION_STATE_A_OFF',
     'check_slot_field_action_activation_off_a',
     'gP1LifePoints+side*0x868+0x1d48: activation state field A; 27 raw refs'),
    (0x0803452c, 0x00001d78, 'ACTIVATION_STATE_B_OFF',
     'check_slot_field_action_activation_off_b',
     'gP1LifePoints+side*0x868+0x1d78: activation state field B; 41 raw refs'),
    (0x080345dc, 0x00001d78, 'ACTIVATION_STATE_B_OFF',
     'check_slot_field_action_activation_off_b2', None),
    (0x0803417c, 0x000010d8, 'ACTIVE_EFFECT_CATEGORY_OFF',
     'check_card_matches_category_off',
     'gP1LifePoints+0x10d8=0x0201D5B8: active effect slot category word; 16 raw refs'),
    (0x08034ad8, 0x00001d48, 'ACTIVATION_STATE_A_OFF',
     'check_slot_full_activation_off_a', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gP1LifePoints (ewram.inc, 0x0201c4e0) -- 10 slots ---
    (0x08034150, 0x0201c4e0, 'gP1LifePoints',
     'check_card_matches_active_effect_gp1lp_a',
     'gP1LifePoints base for active effect category read'),
    (0x08034178, 0x0201c4e0, 'gP1LifePoints',
     'check_card_matches_active_effect_gp1lp_b', None),
    (0x08034528, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_field_action_gp1lp_a', None),
    (0x080345d8, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_field_action_gp1lp_b', None),
    (0x08034734, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_monster_activation_gp1lp', None),
    (0x08034e3c, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_full_activation_gp1lp_a', None),
    (0x08034f10, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_full_activation_gp1lp_b', None),
    (0x08034f64, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_full_activation_gp1lp_c', None),
    (0x08035138, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_full_activation_gp1lp_d', None),
    (0x08035274, 0x0201c4e0, 'gP1LifePoints',
     'check_slot_full_activation_gp1lp_e', None),

    # --- fn-ptr slot: 0x0804aea1 = THUMB ptr for fn at 0x0804aea0 ---
    (0x080346c0, 0x0804aea1, 'count_monster_slots_by_fnptr_pred_0804aea0',
     'check_field_spell_slot_placeable_fnptr',
     'THUMB fn ptr: monster slot predicate at 0x0804aea0; 4 ROM refs'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # --- check_slot_field_action_eligibility: chain effect node CIDs ---
    (0x0803446c, 'check_slot_field_action_chain_mesmeric_ctrl',
     'Mesmeric Control CID 0x12ce (card_0655)'),
    (0x08034470, 'check_slot_field_action_chain_node_131e',
     'chain effect node type 0x131e; no card-stats entry'),
    (0x08034474, 'check_slot_field_action_chain_curse_anubis',
     'Curse of Anubis CID 0x17b3 (card_1607)'),
    (0x08034478, 'check_slot_field_action_chain_spellbinding',
     'Spellbinding Circle CID 0x1103 (card_0309)'),
    (0x0803447c, 'check_slot_field_action_chain_shadow_spell',
     'Shadow Spell CID 0x1243 (card_0544)'),
    (0x08034480, 'check_slot_field_action_chain_nightmare_wheel',
     'Nightmare Wheel CID 0x14b2 (card_0999)'),
    (0x08034484, 'check_slot_field_action_chain_flint',
     'Flint CID 0x1842 (card_1734)'),
    (0x08034488, 'check_slot_field_action_chain_unhappy_girl',
     'The Unhappy Girl CID 0x1743 (card_1518)'),
    (0x0803448c, 'check_slot_field_action_restrict_cid',
     'Thousand-Eyes Restrict CID 0x1284 (card_0594)'),
    (0x08034514, 'check_slot_field_action_dcj_cid',
     'Dragon Capture Jar CID 0x10ef (card_0291)'),
    (0x08034520, 'check_slot_field_action_final_atk_ord',
     'Final Attack Orders CID 0x15fb (card_1255)'),
    (0x080345a8, 'check_slot_field_action_goblin_atk_force',
     'Goblin Attack Force CID 0x1419 (card_0900)'),
    (0x080345ac, 'check_slot_field_action_gravity_axe',
     'Gravity Axe - Grarl CID 0x165e (card_1334)'),
    (0x080345b0, 'check_slot_field_action_swords_conceal',
     'Swords of Concealing Light CID 0x187c (card_1789)'),

    # --- check_field_spell_slot_placeable ---
    (0x08034688, 'check_field_spell_slot_terrorking_cid',
     'Terrorking Archfiend CID 0x1691 (card_1373)'),

    # --- check_slot_monster_activation_eligible ---
    (0x08034754, 'check_slot_monster_activation_gw_cid',
     'Gray Wing CID 0x14dc (card_1036)'),
    (0x08034758, 'check_slot_monster_activation_mataza_cid',
     'Mataza the Zapper CID 0x170a (card_1474, pw=22609617)'),
    (0x08034770, 'check_slot_monster_activation_master_monk_cid',
     'Master Monk CID 0x18b9 (card_1833)'),
    (0x08034774, 'check_slot_monster_activation_mermaid_knight_cid',
     'Mermaid Knight CID 0x174f (card_1530)'),
    (0x08034788, 'check_slot_monster_activation_ctd_cid',
     'Cyber Twin Dragon CID 0x18fc (card_1885)'),
    (0x0803486c, 'check_slot_monster_activation_bls_cid',
     'BLS - Envoy of the Beginning CID 0x16cb (card_1421)'),
    (0x08034870, 'check_slot_monster_activation_twin_swords_cid',
     'Twin Swords of Flashing Light - Tryce CID 0x1661 (card_1337)'),
    (0x08034874, 'check_slot_monster_activation_double_atk_cid',
     'Double Attack CID 0x18cb (card_1851)'),
    (0x08034878, 'check_slot_monster_activation_hero_heart_cid',
     'Hero Heart CID 0x19ab (card_2020)'),
    (0x0803487c, 'check_slot_monster_activation_diffusion_cid',
     'Diffusion Wave-Motion CID 0x15ff (card_1260)'),
    (0x08034888, 'check_slot_monster_activation_eh_avian_cid',
     'Elemental Hero Avian CID 0x18a6 (card_1813)'),
    (0x080348e8, 'check_slot_monster_activation_asura_priest_cid_a',
     'Asura Priest CID 0x1505 (card_1072)'),
    (0x080348ec, 'check_slot_monster_activation_berserk_dragon_cid',
     'Berserk Dragon CID 0x1644 (card_1309)'),
    (0x08034900, 'check_slot_monster_activation_eh_wildedge_cid',
     'Elemental Hero Wildedge CID 0x1958 (card_1959)'),
    (0x08034914, 'check_slot_monster_activation_asura_priest_cid_b',
     'Asura Priest CID 0x1505 second ref (card_1072)'),

    # --- check_slot_full_activation_eligibility: large CID list ---
    (0x08034e04, 'check_slot_full_activation_ekibyo_cid',
     'Ekibyo Drakmord CID 0x149d (card_0987)'),
    (0x08034e08, 'check_slot_full_activation_mask_acc_cid',
     'Mask of the Accursed CID 0x13f3 (card_0864)'),
    (0x08034e0c, 'check_slot_full_activation_flint_cid',
     'Flint CID 0x1842 (card_1734)'),
    (0x08034e10, 'check_slot_full_activation_spellbinding_cid',
     'Spellbinding Circle CID 0x1103 (card_0309)'),
    (0x08034e14, 'check_slot_full_activation_shadow_spell_cid',
     'Shadow Spell CID 0x1243 (card_0544)'),
    (0x08034e18, 'check_slot_full_activation_nightmare_wheel_cid',
     'Nightmare Wheel CID 0x14b2 (card_0999)'),
    (0x08034e1c, 'check_slot_full_activation_wrl_atk_thresh',
     'Wall of Revealing Light ATK threshold (card_1550, 0x1766)'),
    (0x08034e20, 'check_slot_full_activation_vbs_cid',
     'Vengeful Bog Spirit CID 0x14a1 (card_0989)'),
    (0x08034e24, 'check_slot_full_activation_gravity_bind_cid',
     'Gravity Bind CID 0x140e (card_0889)'),
    (0x08034e28, 'check_slot_full_activation_dark_door_cid',
     'The Dark Door CID 0x1469 (card_0940)'),
    (0x08034e2c, 'check_slot_full_activation_chain_128a',
     'chain node type ID 0x128a; no card-stats entry'),
    (0x08034e30, 'check_slot_full_activation_unhappy_girl_cid',
     'The Unhappy Girl CID 0x1743 (card_1518)'),
    (0x08034e34, 'check_slot_full_activation_restrict_cid',
     'Thousand-Eyes Restrict CID 0x1284 (card_0594)'),
    (0x08034e38, 'check_slot_full_activation_btm_cid',
     'Big-Tusked Mammoth CID 0x1865 (card_1766)'),
    (0x08034e44, 'check_slot_full_activation_level_mod_cid',
     'Level Modulation CID 0x1944 (card_1941)'),
    (0x08034e48, 'check_slot_full_activation_chain_1208',
     'chain node type ID 0x1208; no card-stats entry'),
    (0x08034e4c, 'check_slot_full_activation_tribute_doll_cid',
     'Tribute Doll CID 0x15ed (card_1243)'),
    (0x08034e50, 'check_slot_full_activation_puppet_master_cid',
     'Puppet Master CID 0x156a (card_1144)'),
    (0x08034e54, 'check_slot_full_activation_silent_fiend_cid',
     'Silent Fiend CID 0x14f7 (card_1061)'),
    (0x08034e58, 'check_slot_full_activation_magicians_unite_cid',
     "Magician's Unite CID 0x1819 (card_1695)"),
    (0x08034e5c, 'check_slot_full_activation_union_attack_cid',
     'Union Attack CID 0x1890 (card_1807)'),
    (0x08034e60, 'check_slot_full_activation_diffusion_cid',
     'Diffusion Wave-Motion CID 0x15ff (card_1260)'),
    (0x08034e64, 'check_slot_full_activation_feather_shot_cid',
     'Feather Shot CID 0x195b (card_1961)'),
    (0x08034e6c, 'check_slot_full_activation_metal_reflect_cid',
     'Metal Reflect Slime CID 0x1636 (card_1302)'),
    (0x08034e70, 'check_slot_full_activation_redeyes_cid',
     'Red-Eyes B. Dragon CID 0x0ff8 (card_0088)'),
    (0x08034e74, 'check_slot_full_activation_burst_stream_cid',
     'Burst Stream of Destruction CID 0x175b (card_1542)'),
    (0x08034e88, 'check_slot_full_activation_armor_exe_cid',
     'Armor Exe CID 0x161b (card_1279)'),
    (0x08034ea4, 'check_slot_full_activation_bls_cid',
     'BLS - Envoy of Beginning CID 0x16cb (card_1421)'),
    (0x08034ec0, 'check_slot_full_activation_andro_sphinx_cid',
     'Andro Sphinx CID 0x17c7 (card_1622, pw=15013468)'),
    (0x08034ec4, 'check_slot_full_activation_anteatereatingant_cid',
     'Anteatereatingant CID 0x19c8 (card_2043)'),
    (0x08034ee4, 'check_slot_full_activation_inferno_fire_blast_cid',
     'Inferno Fire Blast CID 0x17f6 (card_1667)'),
    (0x08034f24, 'check_slot_full_activation_time_wizard_cid',
     'Time Wizard CID 0x0fb6 (card_0016)'),
    (0x08035140, 'check_slot_full_activation_swords_reveal_cid',
     'Swords of Revealing Light CID 0x1102 (card_0308)'),
    (0x08035144, 'check_slot_full_activation_chain_130e',
     'chain node type ID 0x130e; no card-stats entry'),
    (0x08035148, 'check_slot_full_activation_score_thresh_a',
     'field_score threshold 1499 (0x5db)'),
    (0x0803514c, 'check_slot_full_activation_msngr_peace_cid',
     'Messenger of Peace CID 0x134a (card_0751, pw=44656491)'),
    (0x08035154, 'check_slot_full_activation_array_reveal_cid',
     'Array of Revealing Light CID 0x14d1 (card_1025)'),
    (0x0803515c, 'check_slot_full_activation_regulation_tribe_cid',
     'The Regulation of Tribe CID 0x1358 (card_0761)'),
    (0x08035160, 'check_slot_full_activation_score_thresh_b',
     'field_score threshold 1899 (0x76b)'),
    (0x08035164, 'check_slot_full_activation_gora_turtle_cid',
     'Gora Turtle CID 0x1523 (card_1097)'),
    (0x08035168, 'check_slot_full_activation_harpie_3_cid',
     'Harpie Lady 3 CID 0x182c (card_1712)'),
    (0x0803516c, 'check_slot_full_activation_threatening_roar_cid',
     'Threatening Roar CID 0x1886 (card_1797)'),
    (0x08035170, 'check_slot_full_activation_teva_cid',
     'Teva CID 0x172d (card_1504, pw=16469012)'),
    (0x08035174, 'check_slot_full_activation_cid_180d',
     'copy record CID 0x180d (card_2093, slot_id=0)'),
    (0x08035178, 'check_slot_full_activation_cave_dragon_cid',
     'Cave Dragon CID 0x14db (card_1035)'),
    (0x08035190, 'check_slot_full_activation_cid_1813',
     'copy record CID 0x1813 (card_2094, slot_id=0)'),
    (0x08035194, 'check_slot_full_activation_cid_195a',
     'special token/copy record CID 0x195a (card_2095)'),
    (0x080351d0, 'check_slot_full_activation_toon_skull_cid',
     'Toon Summoned Skull CID 0x127f (card_0591)'),
    (0x080351f0, 'check_slot_full_activation_betd_cid',
     'Blue-Eyes Toon Dragon CID 0x12a5 (card_0629)'),
    (0x0803527c, 'check_slot_full_activation_gk_servant_cid',
     "Gravekeeper's Servant CID 0x131d (card_0710)"),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
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
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment
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

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
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

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg10aSlots (DRY=%s) ===" % DRY)
    print("  Seg-10a: 0x0803407c..0x08035280, 10 fn, slot activation eligibility")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    print("\n=== RefineF02Seg10aSlots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=0  carve=0  disasm=0" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS)))

main()
