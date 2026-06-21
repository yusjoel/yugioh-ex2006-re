# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg7aSlots.py -- f10 Seg-7a (0x08080ba0..0x08081900)
#   9 main functions (assemble_effect_slot_attr_with_zone_lookup /
#   pack_effect_slot_attr_with_type_flags / enqueue_equip_slot_sprite_with_code_rotation /
#   pack_equip_slot_sprite_with_code_attr / read_effect_slot_side_and_type /
#   read_effect_slot_zone_type / check_effect_slot_matches_zone_entry /
#   find_effect_slot_by_side_and_type / dispatch_equip_card_display_op_by_card_id)
#   + 24 named sub-stubs (dispatch_card_display_op_by_id_match +
#   trigger_card_display_op_by_equip_type + 22x trigger_card_display_op_0xNN)
#
# C13: 101 total auto-name slots (DAT_/DWORD_) in [0x8080ba0, 0x8081900)
#   EQ=101 (93 primary rows + 8 secondary occurrences of multi-count constants)
#   REF=0, RENAME=0, disasm=0, carve=0
#
# NEW constants (added to constants/*.inc before running this script):
#   card_info.inc +31: SPIRIT_REAPER_CID/RAIGEKI_BREAK_CID/TRAP_MASTER_CID/
#     MAN_EATER_BUG_CID/THE_RELIABLE_GUARDIAN_CID/REINFORCEMENTS_CID/
#     DUST_TORNADO_CID/KRYUEL_CID/MASK_OF_DISPEL_CID/THOUSAND_KNIVES_CID/
#     COLLECTED_POWER_CID/VISER_DES_CID/RYU_KISHIN_CLOWN_CID/DOUBLE_SNARE_CID/
#     COLLAPSE_CID/BOOK_OF_MOON_CID/MONSTER_RELIEF_CID/A_MAN_WITH_WDJAT_CID/
#     SOUL_TAKER_CID/GUARDIAN_CEAL_CID/GALE_LIZARD_CID/
#     COMPULSORY_EVACUATION_DEVICE_CID/SHIELD_CRASH_CID/
#     GRANMARG_THE_ROCK_MONARCH_CID/CATNIPPED_KITTY_CID/ASSAULT_ON_GHQ_CID/
#     PATROID_CID/VW_TIGER_CATAPULT_CID/KARMA_CUT_CID/GENERATION_SHIFT_CID
#     + cid_128a/cid_1326/cid_127/cid_125/HANE_HANE_INTERNAL_ID_0x1f5 (neutral/internal)
#   duel_field.inc +3: EFFECT_SLOT_TYPE_CLEAR_MASK/STACK_ALLOC_NEG_512/EQUIP_DISP_OP_ID_0x119
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
#    Grouped by constant for clarity.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== REUSE: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc) x3 in 7a =====
    # (4th occurrence DAT_08081b70 is in Seg-7b range, handled there)
    (0x08080c28, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'assemble_zone_lookup_stride_c28'),
    (0x08080d18, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'pack_equip_slot_sprite_stride_d18'),
    (0x08080e4c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_entry_stride_e4c'),

    # ===== REUSE: gDuelFieldSlots=0x0201c510 (ewram.inc) x3 in 7a =====
    # (4th occurrence DAT_08081b74 is in Seg-7b range, handled there)
    (0x08080c2c, 0x0201c510, 'gDuelFieldSlots',
     'assemble_zone_lookup_dfs_c2c'),
    (0x08080d1c, 0x0201c510, 'gDuelFieldSlots',
     'pack_equip_slot_sprite_dfs_d1c'),
    (0x08080e50, 0x0201c510, 'gDuelFieldSlots',
     'check_zone_entry_dfs_e50'),

    # ===== NEW: EFFECT_SLOT_TYPE_CLEAR_MASK=0xffffc01f (duel_field.inc) x2 =====
    (0x08080c30, 0xffffc01f, 'EFFECT_SLOT_TYPE_CLEAR_MASK',
     'assemble_zone_lookup_type_clr_c30'),
    (0x08080c94, 0xffffc01f, 'EFFECT_SLOT_TYPE_CLEAR_MASK',
     'pack_effect_slot_type_clr_c94'),

    # ===== REUSE: SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 (duel_field.inc) x2 =====
    (0x08080c34, 0x000010b1, 'SLOT_FACE_STATUS_ARRAY_OFF',
     'assemble_zone_lookup_face_off_c34'),
    (0x08080e54, 0x000010b1, 'SLOT_FACE_STATUS_ARRAY_OFF',
     'check_zone_entry_face_off_e54'),

    # ===== REUSE: DEMO_CLEAR_BITS_15_14=0xffff3fff (demo_state.inc) x2 =====
    (0x08080c38, 0xffff3fff, 'DEMO_CLEAR_BITS_15_14',
     'assemble_zone_lookup_dir_clr_c38'),
    (0x08080c98, 0xffff3fff, 'DEMO_CLEAR_BITS_15_14',
     'pack_effect_slot_dir_clr_c98'),

    # ===== REUSE: DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff (duel_field.inc) x2 in 7a =====
    # (3rd occurrence 0x08081bf4 is in Seg-7b)
    (0x08080d14, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'enqueue_equip_sprite_rot_state_clr_d14'),
    (0x08080d68, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'pack_equip_code_attr_state_clr_d68'),

    # ===== NEW: SPIRIT_REAPER_CID=0x1596 (card_info.inc) x1 =====
    (0x08080d20, 0x00001596, 'SPIRIT_REAPER_CID',
     'dispatch_bst_spirit_reaper_cid_d20'),

    # ===== REUSE: REAPER_ON_NIGHTMARE_CID=0x1598 (card_info.inc) x1 =====
    (0x08080d24, 0x00001598, 'REAPER_ON_NIGHTMARE_CID',
     'dispatch_bst_reaper_nightmare_cid_d24'),

    # ===== NEW: STACK_ALLOC_NEG_512=0xfffffe00 (duel_field.inc) x1 =====
    (0x08080f14, 0xfffffe00, 'STACK_ALLOC_NEG_512',
     'dispatch_bst_hub_stack_alloc_f14'),

    # ===== NEW: RAIGEKI_BREAK_CID=0x15a8 (card_info.inc) x1 =====
    (0x08080f18, 0x000015a8, 'RAIGEKI_BREAK_CID',
     'dispatch_bst_raigeki_break_cid_f18'),

    # ===== REUSE: JOWLS_OF_DARK_DEMISE_CID=0x13ab (card_info.inc) x1 =====
    (0x08080f1c, 0x000013ab, 'JOWLS_OF_DARK_DEMISE_CID',
     'dispatch_bst_jowls_dark_demise_cid_f1c'),

    # ===== REUSE: SPELLBINDING_CIRCLE_CID=0x1103 (card_info.inc) x1 =====
    (0x08080f20, 0x00001103, 'SPELLBINDING_CIRCLE_CID',
     'dispatch_bst_spellbinding_circle_cid_f20'),

    # ===== NEW: TRAP_MASTER_CID=0x1086 (card_info.inc) x1 =====
    (0x08080f3c, 0x00001086, 'TRAP_MASTER_CID',
     'dispatch_bst_trap_master_cid_f3c'),

    # ===== NEW: MAN_EATER_BUG_CID=0x119b (card_info.inc) x1 =====
    (0x08080f68, 0x0000119b, 'MAN_EATER_BUG_CID',
     'dispatch_bst_man_eater_bug_cid_f68'),

    # ===== REUSE: HANE_HANE_CID=0x11c3 (card_info.inc) x1 =====
    (0x08080f7c, 0x000011c3, 'HANE_HANE_CID',
     'dispatch_bst_hane_hane_cid_f7c'),

    # ===== NEUTRAL: cid_128a=0x128a (card_info.inc) x1 =====
    # EOL: "equip BST unassigned slot"
    (0x08080fb4, 0x0000128a, 'cid_128a',
     'dispatch_bst_cid_128a_fb4'),

    # ===== REUSE: RELINQUISHED_CID=0x1281 (card_info.inc) x1 =====
    (0x08080fd0, 0x00001281, 'RELINQUISHED_CID',
     'dispatch_bst_relinquished_cid_fd0'),

    # ===== REUSE: CYBER_RAIDER_CID=0x1298 (card_info.inc) x1 =====
    (0x08080ff0, 0x00001298, 'CYBER_RAIDER_CID',
     'dispatch_bst_cyber_raider_cid_ff0'),

    # ===== REUSE: COPYCAT_CID=0x12bb (card_info.inc) x1 =====
    # Note: slot is DWORD_08081008 -- treated as EQ (value=COPYCAT_CID)
    (0x08081008, 0x000012bb, 'COPYCAT_CID',
     'dispatch_bst_copycat_cid_1008'),

    # ===== REUSE: BRAIN_CONTROL_CID=0x12c3 (card_info.inc) x1 =====
    (0x08081010, 0x000012c3, 'BRAIN_CONTROL_CID',
     'dispatch_bst_brain_control_cid_1010'),

    # ===== NEW: THE_RELIABLE_GUARDIAN_CID=0x132a (card_info.inc) x1 =====
    (0x08081058, 0x0000132a, 'THE_RELIABLE_GUARDIAN_CID',
     'dispatch_bst_reliable_guardian_cid_1058'),

    # ===== NEW: REINFORCEMENTS_CID=0x12f1 (card_info.inc) x1 =====
    (0x08081074, 0x000012f1, 'REINFORCEMENTS_CID',
     'dispatch_bst_reinforcements_cid_1074'),

    # ===== REUSE: SNATCH_STEAL_CID=0x1322 (card_info.inc) x1 =====
    (0x080810a0, 0x00001322, 'SNATCH_STEAL_CID',
     'dispatch_bst_snatch_steal_cid_10a0'),

    # ===== NEUTRAL: cid_1326=0x1326 (card_info.inc) x1 =====
    # EOL: "equip BST unassigned slot"
    (0x080810b4, 0x00001326, 'cid_1326',
     'dispatch_bst_cid_1326_10b4'),

    # ===== REUSE: MAGICAL_HATS_CID=0x1362 (card_info.inc) x1 =====
    (0x080810e4, 0x00001362, 'MAGICAL_HATS_CID',
     'dispatch_bst_magical_hats_cid_10e4'),

    # ===== REUSE: DRIVING_SNOW_CID=0x134d (card_info.inc) x1 =====
    (0x080810f4, 0x0000134d, 'DRIVING_SNOW_CID',
     'dispatch_bst_driving_snow_cid_10f4'),

    # ===== NEW: DUST_TORNADO_CID=0x137c (card_info.inc) x1 =====
    (0x08081118, 0x0000137c, 'DUST_TORNADO_CID',
     'dispatch_bst_dust_tornado_cid_1118'),

    # ===== REUSE: RING_OF_DESTRUCTION_CID=0x138d (card_info.inc) x1 =====
    (0x0808112c, 0x0000138d, 'RING_OF_DESTRUCTION_CID',
     'dispatch_bst_ring_destruction_cid_112c'),

    # ===== NEW: KRYUEL_CID=0x139e (card_info.inc) x1 =====
    (0x08081134, 0x0000139e, 'KRYUEL_CID',
     'dispatch_bst_kryuel_cid_1134'),

    # ===== NEW: DOUBLE_SNARE_CID=0x14c3 (card_info.inc) x1 =====
    (0x08081180, 0x000014c3, 'DOUBLE_SNARE_CID',
     'dispatch_bst_double_snare_cid_1180'),

    # ===== NEW: MASK_OF_DISPEL_CID=0x13f0 (card_info.inc) x1 =====
    (0x08081198, 0x000013f0, 'MASK_OF_DISPEL_CID',
     'dispatch_bst_mask_dispel_cid_1198'),

    # ===== NEW: THOUSAND_KNIVES_CID=0x142e (card_info.inc) x1 =====
    (0x080811c8, 0x0000142e, 'THOUSAND_KNIVES_CID',
     'dispatch_bst_thousand_knives_cid_11c8'),

    # ===== NEW: COLLECTED_POWER_CID=0x148d (card_info.inc) x1 =====
    (0x080811f8, 0x0000148d, 'COLLECTED_POWER_CID',
     'dispatch_bst_collected_power_cid_11f8'),

    # ===== REUSE: AQUA_SPIRIT_CID=0x1485 (card_info.inc) x1 =====
    (0x08081210, 0x00001485, 'AQUA_SPIRIT_CID',
     'dispatch_bst_aqua_spirit_cid_1210'),

    # ===== NEW: VISER_DES_CID=0x14ac (card_info.inc) x1 =====
    (0x08081234, 0x000014ac, 'VISER_DES_CID',
     'dispatch_bst_viser_des_cid_1234'),

    # ===== REUSE: WINGED_MINION_CID=0x14b9 (card_info.inc) x1 =====
    (0x08081248, 0x000014b9, 'WINGED_MINION_CID',
     'dispatch_bst_winged_minion_cid_1248'),

    # ===== NEW: RYU_KISHIN_CLOWN_CID=0x14bb (card_info.inc) x1 =====
    (0x08081250, 0x000014bb, 'RYU_KISHIN_CLOWN_CID',
     'dispatch_bst_ryu_kishin_clown_cid_1250'),

    # ===== REUSE: BLAST_WITH_CHAIN_CID=0x1514 (card_info.inc) x1 =====
    (0x08081284, 0x00001514, 'BLAST_WITH_CHAIN_CID',
     'dispatch_bst_blast_with_chain_cid_1284'),

    # ===== REUSE: DRAGON_MANIPULATOR_CID=0x14ce (card_info.inc) x1 =====
    (0x0808129c, 0x000014ce, 'DRAGON_MANIPULATOR_CID',
     'dispatch_bst_dragon_manipulator_cid_129c'),

    # ===== NEW: COLLAPSE_CID=0x14eb (card_info.inc) x1 =====
    (0x080812b8, 0x000014eb, 'COLLAPSE_CID',
     'dispatch_bst_collapse_cid_12b8'),

    # ===== REUSE: OTOHIME_CID=0x1503 (card_info.inc) x1 =====
    (0x080812d4, 0x00001503, 'OTOHIME_CID',
     'dispatch_bst_otohime_cid_12d4'),

    # ===== REUSE: SECRET_OF_THE_BANDIT_CID=0x1511 (card_info.inc) x1 =====
    (0x080812dc, 0x00001511, 'SECRET_OF_THE_BANDIT_CID',
     'dispatch_bst_secret_bandit_cid_12dc'),

    # ===== NEW: MONSTER_RELIEF_CID=0x1579 (card_info.inc) x1 =====
    (0x08081304, 0x00001579, 'MONSTER_RELIEF_CID',
     'dispatch_bst_monster_relief_cid_1304'),

    # ===== NEW: BOOK_OF_MOON_CID=0x1538 (card_info.inc) x1 =====
    (0x08081314, 0x00001538, 'BOOK_OF_MOON_CID',
     'dispatch_bst_book_of_moon_cid_1314'),

    # ===== REUSE: ENEMY_CONTROLLER_CID=0x1581 (card_info.inc) x1 =====
    (0x08081330, 0x00001581, 'ENEMY_CONTROLLER_CID',
     'dispatch_bst_enemy_controller_cid_1330'),

    # ===== REUSE: GRAVEKEEPERS_ASSAILANT_CID=0x158d (card_info.inc) x1 =====
    (0x0808134c, 0x0000158d, 'GRAVEKEEPERS_ASSAILANT_CID',
     'dispatch_bst_gravekeepers_assailant_cid_134c'),

    # ===== NEW: A_MAN_WITH_WDJAT_CID=0x158e (card_info.inc) x1 =====
    (0x0808135c, 0x0000158e, 'A_MAN_WITH_WDJAT_CID',
     'dispatch_bst_a_man_with_wdjat_cid_135c'),

    # ===== REUSE: INFERNO_FIRE_BLAST_CID=0x17f6 (card_info.inc) x1 =====
    (0x080813ac, 0x000017f6, 'INFERNO_FIRE_BLAST_CID',
     'dispatch_bst_inferno_fire_blast_cid_13ac'),

    # ===== REUSE: CHECKMATE_CID=0x169b (card_info.inc) x1 =====
    (0x080813b0, 0x0000169b, 'CHECKMATE_CID',
     'dispatch_bst_checkmate_cid_13b0'),

    # ===== REUSE: FREEZING_BEAST_CID=0x15d7 (card_info.inc) x1 =====
    (0x080813c8, 0x000015d7, 'FREEZING_BEAST_CID',
     'dispatch_bst_freezing_beast_cid_13c8'),

    # ===== REUSE: YZ_TANK_DRAGON_CID=0x15fa (card_info.inc) x1 =====
    (0x080813e4, 0x000015fa, 'YZ_TANK_DRAGON_CID',
     'dispatch_bst_yz_tank_dragon_cid_13e4'),

    # ===== REUSE: DIFFUSION_WAVE_MOTION_CID=0x15ff (card_info.inc) x1 =====
    (0x080813f4, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID',
     'dispatch_bst_diffusion_wave_motion_cid_13f4'),

    # ===== NEW: SOUL_TAKER_CID=0x166f (card_info.inc) x1 =====
    (0x0808141c, 0x0000166f, 'SOUL_TAKER_CID',
     'dispatch_bst_soul_taker_cid_141c'),

    # ===== NEW: GUARDIAN_CEAL_CID=0x164b (card_info.inc) x1 =====
    (0x0808142c, 0x0000164b, 'GUARDIAN_CEAL_CID',
     'dispatch_bst_guardian_ceal_cid_142c'),

    # ===== REUSE: DARK_SCORPION_GORG_THE_STRONG_CID=0x1685 (card_info.inc) x1 =====
    (0x08081448, 0x00001685, 'DARK_SCORPION_GORG_THE_STRONG_CID',
     'dispatch_bst_dark_scorpion_gorg_cid_1448'),

    # ===== REUSE: TSUKUYOMI_CID=0x1694 (card_info.inc) x1 =====
    (0x0808145c, 0x00001694, 'TSUKUYOMI_CID',
     'dispatch_bst_tsukuyomi_cid_145c'),

    # ===== REUSE: FALLING_DOWN_CID=0x169a (card_info.inc) x1 =====
    (0x0808146c, 0x0000169a, 'FALLING_DOWN_CID',
     'dispatch_bst_falling_down_cid_146c'),

    # ===== NEW: COMPULSORY_EVACUATION_DEVICE_CID=0x171a (card_info.inc) x1 =====
    (0x080814a0, 0x0000171a, 'COMPULSORY_EVACUATION_DEVICE_CID',
     'dispatch_bst_compulsory_evacuation_cid_14a0'),

    # ===== NEW: GALE_LIZARD_CID=0x16ba (card_info.inc) x1 =====
    (0x080814b0, 0x000016ba, 'GALE_LIZARD_CID',
     'dispatch_bst_gale_lizard_cid_14b0'),

    # ===== REUSE: ENERGY_DRAIN_CID=0x16e3 (card_info.inc) x1 =====
    (0x080814cc, 0x000016e3, 'ENERGY_DRAIN_CID',
     'dispatch_bst_energy_drain_cid_14cc'),

    # ===== REUSE: ORCA_MEGA_FORTRESS_OF_DARKNESS_CID=0x1708 (card_info.inc) x1 =====
    (0x080814e4, 0x00001708, 'ORCA_MEGA_FORTRESS_OF_DARKNESS_CID',
     'dispatch_bst_orca_mega_fortress_cid_14e4'),

    # ===== NEW: SHIELD_CRASH_CID=0x1773 (card_info.inc) x1 =====
    (0x08081514, 0x00001773, 'SHIELD_CRASH_CID',
     'dispatch_bst_shield_crash_cid_1514'),

    # ===== REUSE: ARCANE_ARCHER_OF_THE_FOREST_CID=0x1753 (card_info.inc) x1 =====
    (0x08081524, 0x00001753, 'ARCANE_ARCHER_OF_THE_FOREST_CID',
     'dispatch_bst_arcane_archer_cid_1524'),

    # ===== REUSE: ORDER_TO_CHARGE_CID=0x179f (card_info.inc) x1 =====
    (0x08081540, 0x0000179f, 'ORDER_TO_CHARGE_CID',
     'dispatch_bst_order_to_charge_cid_1540'),

    # ===== REUSE: ARMED_DRAGON_LV5_CID=0x17da (card_info.inc) x1 =====
    (0x08081554, 0x000017da, 'ARMED_DRAGON_LV5_CID',
     'dispatch_bst_armed_dragon_lv5_cid_1554'),

    # ===== REUSE: ELEMENTAL_HERO_THUNDER_GIANT_CID=0x18c9 (card_info.inc) x1 =====
    (0x0808159c, 0x000018c9, 'ELEMENTAL_HERO_THUNDER_GIANT_CID',
     'dispatch_bst_ehero_thunder_giant_cid_159c'),

    # ===== REUSE: HARPIES_HUNTING_GROUND_CID=0x183f (card_info.inc) x1 =====
    (0x080815b4, 0x0000183f, 'HARPIES_HUNTING_GROUND_CID',
     'dispatch_bst_harpies_hunting_ground_cid_15b4'),

    # ===== NEW: GRANMARG_THE_ROCK_MONARCH_CID=0x185f (card_info.inc) x1 =====
    (0x080815d0, 0x0000185f, 'GRANMARG_THE_ROCK_MONARCH_CID',
     'dispatch_bst_granmarg_rock_monarch_cid_15d0'),

    # ===== NEW: CATNIPPED_KITTY_CID=0x1863 (card_info.inc) x1 =====
    (0x080815e0, 0x00001863, 'CATNIPPED_KITTY_CID',
     'dispatch_bst_catnipped_kitty_cid_15e0'),

    # ===== REUSE: OVERPOWERING_EYE_CID=0x1893 (card_info.inc) x1 =====
    (0x08081610, 0x00001893, 'OVERPOWERING_EYE_CID',
     'dispatch_bst_overpowering_eye_cid_1610'),

    # ===== NEW: ASSAULT_ON_GHQ_CID=0x188a (card_info.inc) x1 =====
    (0x08081620, 0x0000188a, 'ASSAULT_ON_GHQ_CID',
     'dispatch_bst_assault_ghq_cid_1620'),

    # ===== REUSE: WHITE_NINJA_CID=0x18be (card_info.inc) x1 =====
    (0x08081644, 0x000018be, 'WHITE_NINJA_CID',
     'dispatch_bst_white_ninja_cid_1644'),

    # ===== REUSE: CHARMER_RANGE_MAX_CID=0x18c2 (card_info.inc) x1 =====
    (0x0808165c, 0x000018c2, 'CHARMER_RANGE_MAX_CID',
     'dispatch_bst_charmer_range_max_cid_165c'),

    # ===== REUSE: ELEMENTAL_HERO_TEMPEST_CID=0x1957 (card_info.inc) x1 =====
    (0x08081698, 0x00001957, 'ELEMENTAL_HERO_TEMPEST_CID',
     'dispatch_bst_ehero_tempest_cid_1698'),

    # ===== NEW: PATROID_CID=0x18f0 (card_info.inc) x1 =====
    (0x080816a8, 0x000018f0, 'PATROID_CID',
     'dispatch_bst_patroid_cid_16a8'),

    # ===== REUSE: A_RIVAL_APPEARS_CID=0x192b (card_info.inc) x1 =====
    (0x080816c8, 0x0000192b, 'A_RIVAL_APPEARS_CID',
     'dispatch_bst_a_rival_appears_cid_16c8'),

    # ===== REUSE: OJAMUSCLE_CID=0x1945 (card_info.inc) x1 =====
    (0x080816e4, 0x00001945, 'OJAMUSCLE_CID',
     'dispatch_bst_ojamuscle_cid_16e4'),

    # ===== NEW: VW_TIGER_CATAPULT_CID=0x1953 (card_info.inc) x1 =====
    (0x080816f0, 0x00001953, 'VW_TIGER_CATAPULT_CID',
     'dispatch_bst_vw_tiger_catapult_cid_16f0'),

    # ===== REUSE: HERO_HEART_CID=0x19ab (card_info.inc) x1 =====
    (0x08081718, 0x000019ab, 'HERO_HEART_CID',
     'dispatch_bst_hero_heart_cid_1718'),

    # ===== REUSE: URIA_LORD_CID=0x19a3 (card_info.inc) x1 =====
    (0x0808172c, 0x000019a3, 'URIA_LORD_CID',
     'dispatch_bst_uria_lord_cid_172c'),

    # ===== NEW: KARMA_CUT_CID=0x19db (card_info.inc) x1 =====
    (0x08081748, 0x000019db, 'KARMA_CUT_CID',
     'dispatch_bst_karma_cut_cid_1748'),

    # ===== NEW: GENERATION_SHIFT_CID=0x19dd (card_info.inc) x1 =====
    (0x08081760, 0x000019dd, 'GENERATION_SHIFT_CID',
     'dispatch_bst_generation_shift_cid_1760'),

    # ===== REUSE: GAP_CID_13EA=0x13ea (card_info.inc) x1 =====
    (0x08081774, 0x000013ea, 'GAP_CID_13EA',
     'dispatch_bst_gap_cid_13ea_1774'),

    # ===== NEW: EQUIP_DISP_OP_ID_0x119=0x119 (duel_field.inc) x2 =====
    (0x08081788, 0x00000119, 'EQUIP_DISP_OP_ID_0x119',
     'trigger_equip_type_op_id_0x119_1788'),
    (0x080818c4, 0x00000119, 'EQUIP_DISP_OP_ID_0x119',
     'trigger_op_0x119_pool_slot_18c4'),

    # ===== NEW: HANE_HANE_INTERNAL_ID_0x1f5=0x1f5 (card_info.inc) x1 =====
    (0x080817bc, 0x000001f5, 'HANE_HANE_INTERNAL_ID_0x1f5',
     'trigger_op_name_0x6c_hane_hane_icid_17bc'),

    # ===== REUSE: SUMMONED_SKULL_CID=0xfbc (card_info.inc) x1 =====
    (0x08081838, 0x00000fbc, 'SUMMONED_SKULL_CID',
     'dispatch_bst_summoned_skull_cid_1838'),

    # ===== REUSE: REVIVAL_JAM_CID=0x13c7 (card_info.inc) x1 =====
    (0x08081874, 0x000013c7, 'REVIVAL_JAM_CID',
     'dispatch_bst_revival_jam_cid_1874'),

    # ===== NEUTRAL: cid_127=0x127 (card_info.inc) x2 =====
    # EOL: "equip BST unassigned slot"
    (0x08081880, 0x00000127, 'cid_127',
     'dispatch_bst_cid_127_1880'),
    (0x080818a0, 0x00000127, 'cid_127',
     'dispatch_bst_cid_127_18a0'),

    # ===== REUSE: GRADIUS_CID=0x1414 (card_info.inc) x1 =====
    (0x08081884, 0x00001414, 'GRADIUS_CID',
     'dispatch_bst_gradius_cid_1884'),

    # ===== REUSE: RED_EYES_B_DRAGON_CID=0xff8 (card_info.inc) x1 =====
    (0x080818a4, 0x00000ff8, 'RED_EYES_B_DRAGON_CID',
     'dispatch_bst_red_eyes_b_dragon_cid_18a4'),

    # ===== NEUTRAL: cid_125=0x125 (card_info.inc) x1 =====
    # EOL: "equip BST unassigned slot"
    (0x080818d4, 0x00000125, 'cid_125',
     'dispatch_bst_cid_125_18d4'),
]

# ---------------------------------------------------------------------------
# B. EOL_COMMENTS: (slot_addr, comment_text)
#    Neutral CID slots get EOL "equip BST unassigned slot"
# ---------------------------------------------------------------------------
EOL_SLOTS = [
    (0x08080fb4, 'equip BST unassigned slot'),   # cid_128a
    (0x080810b4, 'equip BST unassigned slot'),   # cid_1326
    (0x08081880, 'equip BST unassigned slot'),   # cid_127 (first)
    (0x080818a0, 'equip BST unassigned slot'),   # cid_127 (second)
    (0x080818d4, 'equip BST unassigned slot'),   # cid_125
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, old_text, new_text)
#    C8 stale FUN_ substitution. All text pure ASCII. WARN = FAIL.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # assemble_effect_slot_attr_with_zone_lookup (0x08080ba0):
    #   plate has FUN_08080c9c -> enqueue_equip_slot_sprite_with_code_rotation
    (0x08080ba0, 'FUN_08080c9c', 'enqueue_equip_slot_sprite_with_code_rotation'),

    # pack_effect_slot_attr_with_type_flags (0x08080c3c):
    #   plate has FUN_08080d28 -> pack_equip_slot_sprite_with_code_attr
    (0x08080c3c, 'FUN_08080d28', 'pack_equip_slot_sprite_with_code_attr'),

    # dispatch_card_display_op_by_id_match (0x08081758):
    #   plate has FUN_08080ea0, FUN_080817c8, FUN_080818dc
    (0x08081758, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),
    (0x08081758, 'FUN_080817c8', 'trigger_card_display_op_0x6f'),
    (0x08081758, 'FUN_080818dc', 'trigger_card_display_op_0x112'),

    # trigger_card_display_op_by_equip_type (0x08081778):
    (0x08081778, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x44 (0x0808178c):
    (0x0808178c, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x5f (0x08081798):
    (0x08081798, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x62 (0x0808179c):
    (0x0808179c, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x63 (0x080817a0):
    (0x080817a0, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x64 (0x080817a4):
    (0x080817a4, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x66 (0x080817ac):
    (0x080817ac, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x6b (0x080817b0):
    (0x080817b0, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_with_card_name_0x6c (0x080817b4):
    (0x080817b4, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x6d (0x080817c0):
    (0x080817c0, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x6e (0x080817c4):
    (0x080817c4, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x6f (0x080817c8):
    (0x080817c8, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x76 (0x080817d0):
    (0x080817d0, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x77 (0x080817d4):
    (0x080817d4, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x78 (0x080817d8):
    (0x080817d8, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x7a (0x080817dc):
    (0x080817dc, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x80 (0x080817f0):
    (0x080817f0, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x85 (0x080817f4):
    (0x080817f4, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x86 (0x080817f8):
    (0x080817f8, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x88 (0x08081800):
    (0x08081800, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x89 (0x08081804):
    #   plate mentions FUN_08080ea0 and FUN_080818dc
    (0x08081804, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),
    (0x08081804, 'FUN_080818dc', 'trigger_card_display_op_0x112'),

    # trigger_card_display_op_0x119 (0x080818c0):
    (0x080818c0, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # trigger_card_display_op_0x112 (0x080818dc):
    (0x080818dc, 'FUN_08080ea0', 'dispatch_equip_card_display_op_by_card_id'),

    # Cross-file: exec_equip_target_by_best_field7_score (0x080b675c) in asm/15:
    #   plate has FUN_08080c9c -> enqueue_equip_slot_sprite_with_code_rotation
    (0x080b675c, 'FUN_08080c9c', 'enqueue_equip_slot_sprite_with_code_rotation'),
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

def _apply_eol(slot_addr, comment):
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] EOL 0x%08x: no code unit" % slot_addr)
        return
    if DRY:
        print("[dry] EOL 0x%08x: '%s'" % (slot_addr, comment))
        return
    existing = cu.getComment(CodeUnit.EOL_COMMENT)
    if existing and comment in existing:
        print("[info] EOL 0x%08x: already set" % slot_addr)
        return
    cu.setComment(CodeUnit.EOL_COMMENT, comment)
    print("[EOL] 0x%08x: '%s'" % (slot_addr, comment))

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
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate (may already be updated)" % (
            func_addr, old_text))
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
    print("=== RefineF10Seg7aSlots (DRY=%s) ===" % DRY)
    print("  Seg-7a: 0x08080ba0..0x08081900, 9+24 fn, 101 slots (EQ101), 0 ROM_INCBIN, 0 switchD")

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

    # B. EOL_SLOTS (neutral CID comments)
    print("\n--- B. EOL_SLOTS (%d entries) ---" % len(EOL_SLOTS))
    for slot_addr, comment in EOL_SLOTS:
        _apply_eol(slot_addr, comment)

    # C. PLATE_REWRITES
    print("\n--- C. PLATE_REWRITES: FUN_ substitutions (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF10Seg7aSlots DONE ===")
    print("  EQ=%d  EOL=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(EOL_SLOTS), len(PLATE_REWRITES)))

main()
