# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F12-Seg-6 [0x080984d0, 0x08099314): slots and ASCII comments only.
# Proposal SHA256: 93f23b649fb8608e14278e60094b7c4dda05a8ed85812cbc61441b64644ee9a5
# Usage: RefineF12Seg6Slots.py dry|apply|check
# No function renames, disassembly, carve, or memory writes.

from ghidra.program.model.symbol import SourceType, RefType, SymbolType
from ghidra.program.model.listing import CodeUnit

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
DRY = MODE != 'apply'

# BEGIN PROPOSAL TABLES
EQ_SLOTS = [
    (0x08098560, 0x0000131d, 'GRAVEKEEPERS_SERVANT_CID', 'activate_effect_zone_gravekeepers_servant_cid_98560'),
    (0x08098598, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_card_activation_chain_active_offset_98598'),
    (0x0809879c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_card_activation_chain_active_offset_9879c'),
    (0x080987a0, 0x00001469, 'THE_DARK_DOOR_CID', 'tick_card_activation_the_dark_door_cid_987a0'),
    (0x080987a8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_card_activation_player_stride_987a8'),
    (0x080987b0, 0x9c080000, 'MIRROR_WALL_CID_SHIFTED', 'tick_card_activation_mirror_wall_shifted_987b0'),
    (0x080987b8, 0x0000195f, 'HERO_BARRIER_CID', 'tick_card_activation_hero_barrier_cid_987b8'),
    (0x080987bc, 0x0804b165, 'CHECK_CARD_ID_IS_NORMAL_SUMMON_TYPE_THUMB', 'tick_card_activation_normal_summon_predicate_987bc'),
    (0x080987c0, 0x000019a8, 'CYBER_BARRIER_DRAGON_CID', 'tick_card_activation_cyber_barrier_dragon_cid_987c0'),
    (0x080987c4, 0x00000fb6, 'TIME_WIZARD_CID', 'tick_card_activation_time_wizard_cid_987c4'),
    (0x080987c8, 0x00008020, 'SPRITE_RECORD_P2_SIDE', 'tick_card_activation_sprite_p2_20_987c8'),
    (0x080987d8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_card_activation_chain_active_offset_987d8'),
    (0x080988c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_card_activation_player_stride_988c4'),
    (0x080988cc, 0x000018ad, 'ANCIENT_GEAR_SOLDIER_CID', 'tick_card_activation_ancient_gear_soldier_cid_988cc'),
    (0x080988d4, 0x0000158d, 'GRAVEKEEPERS_ASSAILANT_CID', 'tick_card_activation_gravekeepers_assailant_cid_988d4'),
    (0x080988e0, 0x00001954, 'VWXYZ_DRAGON_CATAPULT_CANNON_CID', 'tick_card_activation_vwxyz_dragon_catapult_cannon_cid_988e0'),
    (0x08098984, 0x24200000, 'EQUIP_ACTIVATION_PACKED_TYPE18', 'tick_card_activation_packed_type18_98984'),
    (0x08098988, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_card_activation_player_stride_98988'),
    (0x08098994, 0x0000153f, 'ORDEAL_OF_A_TRAVELER_CID', 'tick_card_activation_ordeal_of_a_traveler_cid_98994'),
    (0x08098998, 0x000013f9, 'FAIRY_BOX_CID', 'tick_card_activation_fairy_box_cid_98998'),
    (0x08098a28, 0x00001931, 'PREPARE_TO_STRIKE_BACK_CID', 'tick_card_activation_prepare_to_strike_back_cid_98a28'),
    (0x08098a2c, 0x24200000, 'EQUIP_ACTIVATION_PACKED_TYPE18', 'tick_card_activation_packed_type18_98a2c'),
    (0x08098a38, 0x00000482, 'SPRITE_ROW_PROCESSED_COUNT_OFF', 'tick_card_activation_row_processed_count_offset_98a38'),
    (0x08098a40, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_card_activation_chain_active_offset_98a40'),
    (0x08098a70, 0x00000482, 'SPRITE_ROW_PROCESSED_COUNT_OFF', 'tick_card_activation_row_processed_count_offset_98a70'),
    (0x08098b1c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_98b1c'),
    (0x08098b24, 0x00001cfc, 'EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF', 'tick_equip_activation_chain_active_offset_98b24'),
    (0x08098b54, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'tick_equip_activation_sprite_p2_1b_98b54'),
    (0x08098c04, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID', 'tick_equip_activation_diffusion_wave_motion_cid_98c04'),
    (0x08098c0c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_98c0c'),
    (0x08098c14, 0x000015d2, 'GIANT_ORC_CID', 'tick_equip_activation_giant_orc_cid_98c14'),
    (0x08098c24, 0x00001505, 'ASURA_PRIEST_CID', 'tick_equip_activation_asura_priest_cid_98c24'),
    (0x08098c40, 0x00001915, 'INDOMITABLE_FIGHTER_LEI_LEI_CID', 'tick_equip_activation_indomitable_fighter_lei_lei_cid_98c40'),
    (0x08098c44, 0x00001644, 'BERSERK_DRAGON_CID', 'tick_equip_activation_berserk_dragon_cid_98c44'),
    (0x08098c48, 0x00001912, 'GOBLIN_ELITE_ATTACK_FORCE_CID', 'tick_equip_activation_goblin_elite_attack_force_cid_98c48'),
    (0x08098c6c, 0x00001958, 'EHERO_WILDEDGE_CID', 'tick_equip_activation_ehero_wildedge_cid_98c6c'),
    (0x08098c74, 0x000014d6, 'SPEAR_DRAGON_CID', 'tick_equip_activation_spear_dragon_cid_98c74'),
    (0x08098c90, 0x000014d6, 'SPEAR_DRAGON_CID', 'tick_equip_activation_spear_dragon_cid_98c90'),
    (0x08098d14, 0x00001505, 'ASURA_PRIEST_CID', 'tick_equip_activation_asura_priest_cid_98d14'),
    (0x08098d18, 0x000017df, 'NINJA_GRANDMASTER_SASUKE_CID', 'tick_equip_activation_ninja_grandmaster_sasuke_cid_98d18'),
    (0x08098d2c, 0x000017d8, 'MYSTIC_SWORDSMAN_LV4_CID', 'tick_equip_activation_mystic_swordsman_lv4_cid_98d2c'),
    (0x08098d44, 0x00001829, 'SASUKE_SAMURAI_4_CID', 'tick_equip_activation_sasuke_samurai_4_cid_98d44'),
    (0x08098e04, 0x00001963, 'NANOBREAKER_CID', 'tick_equip_activation_nanobreaker_cid_98e04'),
    (0x08098e0c, 0x28200000, 'EQUIP_ACTIVATION_PACKED_TYPE20', 'tick_equip_activation_packed_type20_98e0c'),
    (0x08098e10, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_98e10'),
    (0x08098e18, 0x00001829, 'SASUKE_SAMURAI_4_CID', 'tick_equip_activation_sasuke_samurai_4_cid_98e18'),
    (0x08098e20, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_equip_activation_chain_active_offset_98e20'),
    (0x08098e3c, 0x00001cf8, 'EQUIP_CHAIN_STEP_FROM_FIELD_OFF', 'tick_equip_activation_chain_step_offset_98e3c'),
    (0x08098ed0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_98ed0'),
    (0x08098ed4, 0x0000129c, 'BIG_SHIELD_GARDNA_CID', 'tick_equip_activation_big_shield_gardna_cid_98ed4'),
    (0x08098edc, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_equip_activation_chain_active_offset_98edc'),
    (0x08098f48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_98f48'),
    (0x08098f4c, 0x00001508, 'SUPER_ROBOYAROU_CID', 'tick_equip_activation_super_roboyarou_cid_98f4c'),
    (0x08098f50, 0x00001397, 'LUMINOUS_SOLDIER_CID', 'tick_equip_activation_luminous_soldier_cid_98f50'),
    (0x08098f54, 0x00001184, 'INSECT_SOLDIERS_OF_THE_SKY_CID', 'tick_equip_activation_insect_soldiers_of_the_sky_cid_98f54'),
    (0x08098f5c, 0x00001507, 'SUPER_ROBOLADY_CID', 'tick_equip_activation_super_robolady_cid_98f5c'),
    (0x08098f74, 0x000018f2, 'STEAMROID_CID', 'tick_equip_activation_steamroid_cid_98f74'),
    (0x08098f78, 0x000017ed, 'PENUMBRAL_SOLDIER_LADY_CID', 'tick_equip_activation_penumbral_soldier_lady_cid_98f78'),
    (0x08098f84, 0x00001952, 'ETOILE_CYBER_CID', 'tick_equip_activation_etoile_cyber_cid_98f84'),
    (0x08099038, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_99038'),
    (0x080990bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_990bc'),
    (0x080990c4, 0x00001508, 'SUPER_ROBOYAROU_CID', 'tick_equip_activation_super_roboyarou_cid_990c4'),
    (0x080990c8, 0x000010c6, 'upd_cid_10c6', 'tick_equip_activation_upd_cid_10c6_990c8'),
    (0x080990cc, 0x00001397, 'LUMINOUS_SOLDIER_CID', 'tick_equip_activation_luminous_soldier_cid_990cc'),
    (0x080990e4, 0x000017ed, 'PENUMBRAL_SOLDIER_LADY_CID', 'tick_equip_activation_penumbral_soldier_lady_cid_990e4'),
    (0x080990e8, 0x00001621, 'CATS_EAR_TRIBE_CID', 'tick_equip_activation_cats_ear_tribe_cid_990e8'),
    (0x080990f4, 0x000018f2, 'STEAMROID_CID', 'tick_equip_activation_steamroid_cid_990f4'),
    (0x08099154, 0x00001cb8, 'EQUIP_ZONE_COUNT_TABLE_OFF', 'tick_equip_activation_zone_count_table_offset_99154'),
    (0x080991b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_991b0'),
    (0x08099258, 0x00001752, 'DISC_FIGHTER_CID', 'tick_equip_activation_disc_fighter_cid_99258'),
    (0x0809925c, 0x000018f3, 'DRILLROID_CID', 'tick_equip_activation_drillroid_cid_9925c'),
    (0x08099260, 0x28200000, 'EQUIP_ACTIVATION_PACKED_TYPE20', 'tick_equip_activation_packed_type20_99260'),
    (0x08099264, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_99264'),
    (0x0809926c, 0x00001476, 'ANCIENT_LAMP_CID', 'tick_equip_activation_ancient_lamp_cid_9926c'),
    (0x08099270, 0x00001286, 'BLAST_SPHERE_CID', 'tick_equip_activation_blast_sphere_cid_99270'),
    (0x080992f4, 0x0000148a, 'DREAMSPRITE_CID', 'tick_equip_activation_dreamsprite_cid_992f4'),
    (0x080992f8, 0x000019bd, 'ADHESIVE_EXPLOSIVE_CID', 'tick_equip_activation_adhesive_explosive_cid_992f8'),
    (0x08099300, 0x28200000, 'EQUIP_ACTIVATION_PACKED_TYPE20', 'tick_equip_activation_packed_type20_99300'),
    (0x08099304, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_activation_player_stride_99304'),
    (0x08099310, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_equip_activation_chain_active_offset_99310'),
]

REF_SLOTS = [
    (0x0809855c, 0x0201bb90, 'gEquipChainSlotRefs', 'activate_effect_zone_chain_base_9855c'),
    (0x08098590, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_card_activation_chain_base_98590'),
    (0x0809859c, 0x080985a0, 'switchD_0809858e__switchdataD_080985a0', 'tick_card_activation_phase_table_ptr_9859c'),
    (0x08098794, 0x0201bc7c, 'gEquipSlotActivationSnapshot', 'tick_card_activation_snapshot_base_98794'),
    (0x080987a4, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_card_activation_chain_base_987a4'),
    (0x080987ac, 0x0201c510, 'gDuelFieldSlots', 'tick_card_activation_field_slots_base_987ac'),
    (0x080987b4, 0x0201c520, 'gDuelFieldSlotState', 'tick_card_activation_field_state_base_987b4'),
    (0x080988c0, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_card_activation_chain_base_988c0'),
    (0x080988c8, 0x0201c510, 'gDuelFieldSlots', 'tick_card_activation_field_slots_base_988c8'),
    (0x080988d0, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_card_activation_card_ctx_base_988d0'),
    (0x08098980, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_card_activation_chain_base_98980'),
    (0x0809898c, 0x0201c510, 'gDuelFieldSlots', 'tick_card_activation_field_slots_base_9898c'),
    (0x08098990, 0x0201c520, 'gDuelFieldSlotState', 'tick_card_activation_field_state_base_98990'),
    (0x08098a30, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_card_activation_chain_base_98a30'),
    (0x08098a34, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_activation_phase_flags_base_98a34'),
    (0x08098a6c, 0x0201b290, 'gDuelPhaseFlags', 'tick_card_activation_phase_flags_base_98a6c'),
    (0x08098b18, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98b18'),
    (0x08098b20, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_98b20'),
    (0x08098c08, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98c08'),
    (0x08098c10, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_98c10'),
    (0x08098c70, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98c70'),
    (0x08098c8c, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98c8c'),
    (0x08098d10, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98d10'),
    (0x08098e08, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98e08'),
    (0x08098e14, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_98e14'),
    (0x08098fb0, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_98fb0'),
    (0x08099034, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_99034'),
    (0x0809903c, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_9903c'),
    (0x080990b8, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_990b8'),
    (0x080990c0, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_990c0'),
    (0x08099104, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_99104'),
    (0x08099118, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_99118'),
    (0x08099158, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_99158'),
    (0x080991ac, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_991ac'),
    (0x080991b4, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_991b4'),
    (0x08099254, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_99254'),
    (0x08099268, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_99268'),
    (0x080992fc, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_activation_chain_base_992fc'),
    (0x08099308, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_activation_field_slots_base_99308'),
]

RENAME_SLOTS = [
    (0x08098594, 'tick_card_activation_lp_base_98594', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
    (0x08098798, 'tick_card_activation_lp_base_98798', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
    (0x080987d4, 'tick_card_activation_lp_base_987d4', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
    (0x08098a3c, 'tick_card_activation_lp_base_98a3c', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
    (0x08098e1c, 'tick_equip_activation_lp_base_98e1c', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
    (0x08098ed8, 'tick_equip_activation_lp_base_98ed8', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
    (0x0809930c, 'tick_equip_activation_lp_base_9930c', 'gP1LifePoints base; paired offset addresses the equip activation phase.'),
]

PLATES = [
    (0x080984d0, 'activate_effect_zone_display_for_slot', "Activates Gravekeeper's Servant and Toll display effects for r0=player_side. Reads the paired player and slot from gEquipChainSlotRefs. Sets chain[+0x10]=1 once; repeated calls return without requeueing. Tests the eligibility result's bit1 before counting Gravekeeper's Servant zones and queuing their display. Counts Toll zones and queues one 500-unit sprite per hit. Returns 1."),
    (0x08098564, 'tick_card_activation_phase_by_state', 'Ticks the 0..4 card activation display phases for r0=player_side. State is [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Phases cache activation state, display card-specific triggers, apply packed activations, then poll for refresh completion. Uses gEquipChainSlotRefs and gDuelFieldSlots; clears the processed sprite-row count at phase 3 and after its phase-4 notification. Returns 0 while pending, 1 when complete. Called through advance_equip_display_phase_via_table.'),
    (0x08098a88, 'tick_equip_zone_activation_display_state', 'Ticks equip activation display phases 0..3 for r0=player_side. Uses gEquipChainSlotRefs for the player/slot pair. State is [gDuelFieldSlots+EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF], the same word as [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Caches slot state, queues card-specific displays, and applies packed activations. A phase-2 mismatch writes step 11 and clears the phase. Returns 0 while pending, 1 when complete, through restore_high_regs_epilogue_equip_tick.'),
    (0x080992e2, 'restore_high_regs_epilogue_equip_tick', 'Shared return tail of tick_equip_zone_activation_display_state; requires its existing stack frame. Releases 0xc local bytes, restores r8/r9/r10 and r4-r7, then returns through the saved caller address. Preserves r0. Reached by BL at 0x08098b12, B at 0x08098e38, and fall-through from 0x080992e0. This is not an independent APCS entry.'),
]

ORIGINAL_LABELS = {
    0x0809855c: 'DAT_0809855c',
    0x08098560: 'DAT_08098560',
    0x08098590: 'DAT_08098590',
    0x08098594: 'PTR_gP1LifePoints_08098594',
    0x08098598: 'DAT_08098598',
    0x0809859c: 'PTR_switchdataD_080985a0_0809859c',
    0x08098794: 'DAT_08098794',
    0x08098798: 'PTR_gP1LifePoints_08098798',
    0x0809879c: 'DAT_0809879c',
    0x080987a0: 'DAT_080987a0',
    0x080987a4: 'DAT_080987a4',
    0x080987a8: 'DAT_080987a8',
    0x080987ac: 'DAT_080987ac',
    0x080987b0: 'DAT_080987b0',
    0x080987b4: 'DAT_080987b4',
    0x080987b8: 'DAT_080987b8',
    0x080987bc: 'DAT_080987bc',
    0x080987c0: 'DAT_080987c0',
    0x080987c4: 'DAT_080987c4',
    0x080987c8: 'DAT_080987c8',
    0x080987d4: 'PTR_gP1LifePoints_080987d4',
    0x080987d8: 'DAT_080987d8',
    0x080988c0: 'DAT_080988c0',
    0x080988c4: 'DAT_080988c4',
    0x080988c8: 'DAT_080988c8',
    0x080988cc: 'DAT_080988cc',
    0x080988d0: 'DAT_080988d0',
    0x080988d4: 'DAT_080988d4',
    0x080988e0: 'DAT_080988e0',
    0x08098980: 'DAT_08098980',
    0x08098984: 'DAT_08098984',
    0x08098988: 'DAT_08098988',
    0x0809898c: 'DAT_0809898c',
    0x08098990: 'DAT_08098990',
    0x08098994: 'DAT_08098994',
    0x08098998: 'DAT_08098998',
    0x08098a28: 'DAT_08098a28',
    0x08098a2c: 'DAT_08098a2c',
    0x08098a30: 'DAT_08098a30',
    0x08098a34: 'DAT_08098a34',
    0x08098a38: 'DAT_08098a38',
    0x08098a3c: 'PTR_gP1LifePoints_08098a3c',
    0x08098a40: 'DAT_08098a40',
    0x08098a6c: 'DAT_08098a6c',
    0x08098a70: 'DAT_08098a70',
    0x08098b18: 'DWORD_08098b18',
    0x08098b1c: 'DWORD_08098b1c',
    0x08098b20: 'DWORD_08098b20',
    0x08098b24: 'DWORD_08098b24',
    0x08098b54: 'DAT_08098b54',
    0x08098c04: 'DAT_08098c04',
    0x08098c08: 'DAT_08098c08',
    0x08098c0c: 'DAT_08098c0c',
    0x08098c10: 'DAT_08098c10',
    0x08098c14: 'DAT_08098c14',
    0x08098c24: 'DAT_08098c24',
    0x08098c40: 'DAT_08098c40',
    0x08098c44: 'DAT_08098c44',
    0x08098c48: 'DAT_08098c48',
    0x08098c6c: 'DAT_08098c6c',
    0x08098c70: 'DAT_08098c70',
    0x08098c74: 'DAT_08098c74',
    0x08098c8c: 'DAT_08098c8c',
    0x08098c90: 'DAT_08098c90',
    0x08098d10: 'DAT_08098d10',
    0x08098d14: 'DAT_08098d14',
    0x08098d18: 'DAT_08098d18',
    0x08098d2c: 'DAT_08098d2c',
    0x08098d44: 'DAT_08098d44',
    0x08098e04: 'DAT_08098e04',
    0x08098e08: 'DAT_08098e08',
    0x08098e0c: 'DAT_08098e0c',
    0x08098e10: 'DAT_08098e10',
    0x08098e14: 'DAT_08098e14',
    0x08098e18: 'DAT_08098e18',
    0x08098e1c: 'PTR_gP1LifePoints_08098e1c',
    0x08098e20: 'DAT_08098e20',
    0x08098e3c: 'DAT_08098e3c',
    0x08098ed0: 'DAT_08098ed0',
    0x08098ed4: 'DAT_08098ed4',
    0x08098ed8: 'PTR_gP1LifePoints_08098ed8',
    0x08098edc: 'DAT_08098edc',
    0x08098f48: 'DAT_08098f48',
    0x08098f4c: 'DAT_08098f4c',
    0x08098f50: 'DAT_08098f50',
    0x08098f54: 'DAT_08098f54',
    0x08098f5c: 'DAT_08098f5c',
    0x08098f74: 'DAT_08098f74',
    0x08098f78: 'DAT_08098f78',
    0x08098f84: 'DAT_08098f84',
    0x08098fb0: 'DAT_08098fb0',
    0x08099034: 'DAT_08099034',
    0x08099038: 'DAT_08099038',
    0x0809903c: 'DAT_0809903c',
    0x080990b8: 'DAT_080990b8',
    0x080990bc: 'DAT_080990bc',
    0x080990c0: 'DAT_080990c0',
    0x080990c4: 'DAT_080990c4',
    0x080990c8: 'DAT_080990c8',
    0x080990cc: 'DAT_080990cc',
    0x080990e4: 'DAT_080990e4',
    0x080990e8: 'DAT_080990e8',
    0x080990f4: 'DAT_080990f4',
    0x08099104: 'DAT_08099104',
    0x08099118: 'DAT_08099118',
    0x08099154: 'DAT_08099154',
    0x08099158: 'DAT_08099158',
    0x080991ac: 'DAT_080991ac',
    0x080991b0: 'DAT_080991b0',
    0x080991b4: 'DAT_080991b4',
    0x08099254: 'DAT_08099254',
    0x08099258: 'DAT_08099258',
    0x0809925c: 'DAT_0809925c',
    0x08099260: 'DAT_08099260',
    0x08099264: 'DAT_08099264',
    0x08099268: 'DAT_08099268',
    0x0809926c: 'DAT_0809926c',
    0x08099270: 'DAT_08099270',
    0x080992f4: 'DAT_080992f4',
    0x080992f8: 'DAT_080992f8',
    0x080992fc: 'DAT_080992fc',
    0x08099300: 'DAT_08099300',
    0x08099304: 'DAT_08099304',
    0x08099308: 'DAT_08099308',
    0x0809930c: 'PTR_gP1LifePoints_0809930c',
    0x08099310: 'DAT_08099310',
}

CALLBACK_EOL = 'THUMB callback: check_card_id_is_normal_summon_type+1 = 0x0804b165.'
SWITCH_TARGETS = [0x080985b4, 0x080985c6, 0x08098610, 0x080987dc, 0x08098a44]
# END PROPOSAL TABLES

symTbl = currentProgram.getSymbolTable()
refMgr = currentProgram.getReferenceManager()
listing = currentProgram.getListing()
eqTbl = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'AUX_REF', 'EOL'))


def fail(message):
    FAILS.append(message)
    print('FAIL: ' + message)


def _check(slot, value):
    actual = memory.getInt(toAddr(slot)) & 0xffffffff
    if actual != value:
        fail('VALUE 0x%08x expected=0x%08x actual=0x%08x' % (slot, value, actual))
        return False
    cu = listing.getDefinedDataAt(toAddr(slot))
    if cu is None or cu.getLength() != 4:
        fail('DATA4 0x%08x' % slot)
        return False
    return True


def require_ascii(text, where):
    if any(ord(c) > 127 for c in text):
        fail('ASCII ' + where)


def require_name_available(name, addr):
    for symbol in symTbl.getGlobalSymbols(name):
        if symbol.getAddress() != toAddr(addr):
            fail('NAME_COLLISION %s at %s' % (name, symbol.getAddress()))


def require_callback_primary():
    primary = symTbl.getPrimarySymbol(toAddr(0x0804b164))
    fn = getFunctionAt(toAddr(0x0804b164))
    if (primary is None or fn is None or
            primary.getSymbolType() != SymbolType.FUNCTION or
            primary.getName() != 'check_card_id_is_normal_summon_type' or
            fn.getName() != 'check_card_id_is_normal_summon_type'):
        fail('CALLBACK_FUNCTION_PRIMARY 0x0804b164')


def preflight():
    all_slots = [r[0] for r in EQ_SLOTS + REF_SLOTS + RENAME_SLOTS]
    if len(all_slots) != 126 or len(set(all_slots)) != 126:
        fail('SLOT_COVERAGE')
    for slot, value, name, label in EQ_SLOTS + REF_SLOTS:
        _check(slot, value)
        require_name_available(label, slot)
        if not 0x080984d0 <= slot < 0x08099314:
            fail('SLOT_RANGE 0x%08x' % slot)
        names = [s.getName() for s in symTbl.getSymbols(toAddr(slot))]
        if ORIGINAL_LABELS[slot] not in names and label not in names:
            fail('SLOT_PATTERN 0x%08x names=%s' % (slot, names))
    for slot, value, name, label in EQ_SLOTS:
        eq = eqTbl.getEquate(name)
        if eq is not None and (eq.getValue() & 0xffffffff) != value:
            fail('EQUATE_VALUE ' + name)
        for existing in eqTbl.getEquates(toAddr(slot)):
            if existing.getName() != name:
                fail('OTHER_EQUATE 0x%08x %s' % (slot, existing.getName()))
    for slot, target, name, label in REF_SLOTS:
        require_name_available(name, target)
        primary = symTbl.getPrimarySymbol(toAddr(target))
        if primary is not None and primary.getSymbolType() == SymbolType.FUNCTION:
            fail('REF_TARGET_FUNCTION 0x%08x' % target)
    for slot, label, eol in RENAME_SLOTS:
        _check(slot, 0x0201c4e0)
        require_name_available(label, slot)
        require_ascii(eol, 'RENAME 0x%08x' % slot)
        names = [s.getName() for s in symTbl.getSymbols(toAddr(slot))]
        if ORIGINAL_LABELS[slot] not in names and label not in names:
            fail('RENAME_PATTERN 0x%08x' % slot)
    for addr, fn_name, text in PLATES:
        fn = getFunctionAt(toAddr(addr))
        cu = listing.getCodeUnitAt(toAddr(addr))
        if fn is None or fn.getName() != fn_name or cu is None:
            fail('PLATE_FUNCTION 0x%08x %s' % (addr, fn_name))
        elif not cu.getComment(CodeUnit.PLATE_COMMENT):
            fail('PLATE_PATTERN 0x%08x' % addr)
        require_ascii(text, 'PLATE 0x%08x' % addr)
        if len(text) > 500:
            fail('PLATE_LENGTH 0x%08x %d' % (addr, len(text)))
    require_callback_primary()
    require_ascii(CALLBACK_EOL, 'CALLBACK')
    for i, target in enumerate(SWITCH_TARGETS):
        _check(0x080985a0 + i * 4, target)
    print('PREFLIGHT slots=126 EQ=80 REF=39 RENAME=7 PLATE=4 AUX_REF=1 EOL=8 FAIL=%d' % len(FAILS))


def slot_label(slot, name):
    addr = toAddr(slot)
    label = symTbl.getGlobalSymbol(name, addr)
    if label is None:
        label = symTbl.createLabel(addr, name, SourceType.USER_DEFINED)
    for old in list(symTbl.getSymbols(addr)):
        if old.getName() != name and old.getName().startswith(('DAT_', 'DWORD_', 'PTR_', 'UNK_')):
            if old.getSymbolType() != SymbolType.LABEL:
                raise RuntimeError('Non-label auto symbol at 0x%08x' % slot)
            old.delete()
    label.setPrimary()


def add_primary_data_ref(slot, target):
    addr, to = toAddr(slot), toAddr(target)
    for old in list(refMgr.getReferencesFrom(addr)):
        # Recreate operand 0: merging a same-target DEFAULT reference does not
        # upgrade its source to USER_DEFINED on this Ghidra version.
        if old.getOperandIndex() == 0:
            refMgr.delete(old)
    ref = refMgr.addMemoryReference(addr, to, RefType.DATA, SourceType.USER_DEFINED, 0)
    refMgr.setPrimary(ref, True)


def apply_all():
    for slot, value, name, label in EQ_SLOTS:
        eq = eqTbl.getEquate(name)
        if eq is None:
            eq = eqTbl.createEquate(name, value)
        eq.addReference(toAddr(slot), 0)
        slot_label(slot, label)
        COUNTS['EQ'] += 1
    for slot, target, name, label in REF_SLOTS:
        addr = toAddr(target)
        target_symbol = symTbl.getGlobalSymbol(name, addr)
        if target_symbol is None:
            target_symbol = symTbl.createLabel(addr, name, SourceType.USER_DEFINED)
        elif target_symbol.getSource() != SourceType.USER_DEFINED:
            target_symbol.setName(name, SourceType.USER_DEFINED)
        target_symbol.setPrimary()
        add_primary_data_ref(slot, target)
        slot_label(slot, label)
        COUNTS['REF'] += 1
    for slot, label, eol in RENAME_SLOTS:
        slot_label(slot, label)
        listing.getCodeUnitAt(toAddr(slot)).setComment(CodeUnit.EOL_COMMENT, eol)
        COUNTS['RENAME'] += 1
        COUNTS['EOL'] += 1
    # This navigation reference must retain the existing even-address FUNCTION.
    add_primary_data_ref(0x080987bc, 0x0804b164)
    COUNTS['AUX_REF'] += 1
    listing.getCodeUnitAt(toAddr(0x080987bc)).setComment(CodeUnit.EOL_COMMENT, CALLBACK_EOL)
    COUNTS['EOL'] += 1
    for addr, fn_name, text in PLATES:
        listing.getCodeUnitAt(toAddr(addr)).setComment(CodeUnit.PLATE_COMMENT, text)
        COUNTS['PLATE'] += 1


def verify_applied():
    for slot, value, name, label in EQ_SLOTS:
        _check(slot, value)
        found = list(eqTbl.getEquates(toAddr(slot)))
        if len(found) != 1 or found[0].getName() != name or (found[0].getValue() & 0xffffffff) != value:
            fail('POST_EQUATE 0x%08x' % slot)
    for slot, target, name, label in REF_SLOTS:
        primary = symTbl.getPrimarySymbol(toAddr(target))
        if (primary is None or primary.getName() != name or
                primary.getSource() != SourceType.USER_DEFINED):
            fail('POST_TARGET 0x%08x' % slot)
        refs = [r for r in refMgr.getReferencesFrom(toAddr(slot)) if r.isPrimary()]
        if (len(refs) != 1 or refs[0].getToAddress() != toAddr(target) or
                refs[0].getReferenceType() != RefType.DATA or
                refs[0].getSource() != SourceType.USER_DEFINED):
            print('POST_REF_DETAIL %s' % [(str(r.getToAddress()), r.getOperandIndex(), str(r.getReferenceType()), str(r.getSource()), r.isPrimary()) for r in refMgr.getReferencesFrom(toAddr(slot))])
            fail('POST_REF 0x%08x' % slot)
    for slot, label in [(r[0], r[3]) for r in EQ_SLOTS + REF_SLOTS] + [(r[0], r[1]) for r in RENAME_SLOTS]:
        primary = symTbl.getPrimarySymbol(toAddr(slot))
        if primary is None or primary.getName() != label:
            fail('POST_SLOT 0x%08x' % slot)
        if any(s.getName().startswith(('DAT_', 'DWORD_', 'PTR_', 'UNK_')) for s in symTbl.getSymbols(toAddr(slot))):
            fail('POST_AUTO_SLOT 0x%08x' % slot)
    for slot, label, eol in RENAME_SLOTS:
        if listing.getCodeUnitAt(toAddr(slot)).getComment(CodeUnit.EOL_COMMENT) != eol:
            fail('POST_EOL 0x%08x' % slot)
    require_callback_primary()
    if list(symTbl.getSymbols(toAddr(0x0804b165))) != ODD_SYMBOLS_BEFORE:
        fail('POST_ODD_SYMBOL_CHANGED')
    if getFunctionAt(toAddr(0x0804b165)) != ODD_FUNCTION_BEFORE:
        fail('POST_ODD_FUNCTION_CHANGED')
    refs = [r for r in refMgr.getReferencesFrom(toAddr(0x080987bc)) if r.isPrimary()]
    if (len(refs) != 1 or refs[0].getToAddress() != toAddr(0x0804b164) or
            refs[0].getReferenceType() != RefType.DATA or refs[0].getSource() != SourceType.USER_DEFINED):
        fail('POST_CALLBACK_REF')
    if listing.getCodeUnitAt(toAddr(0x080987bc)).getComment(CodeUnit.EOL_COMMENT) != CALLBACK_EOL:
        fail('POST_CALLBACK_EOL')
    for addr, fn_name, text in PLATES:
        if listing.getCodeUnitAt(toAddr(addr)).getComment(CodeUnit.PLATE_COMMENT) != text:
            fail('POST_PLATE 0x%08x' % addr)
        if getFunctionAt(toAddr(addr)).getName() != fn_name:
            fail('POST_FUNCTION_NAME 0x%08x' % addr)
    for i, target in enumerate(SWITCH_TARGETS):
        _check(0x080985a0 + i * 4, target)


print('=== RefineF12Seg6Slots mode=%s ===' % MODE)
ODD_SYMBOLS_BEFORE = list(symTbl.getSymbols(toAddr(0x0804b165)))
ODD_FUNCTION_BEFORE = getFunctionAt(toAddr(0x0804b165))
preflight()
if FAILS:
    raise RuntimeError('PREFLIGHT FAIL; no writes performed')
if MODE == 'apply':
    transaction = currentProgram.startTransaction('Refine F12-Seg-6 slots')
    success = False
    try:
        apply_all()
        verify_applied()
        if FAILS:
            raise RuntimeError('POSTCHECK FAIL; transaction rolled back')
        success = True
    finally:
        currentProgram.endTransaction(transaction, success)
elif MODE == 'check':
    verify_applied()
    if FAILS:
        raise RuntimeError('CHECK FAIL')
else:
    COUNTS.update({'EQ': 80, 'REF': 39, 'RENAME': 7, 'PLATE': 4, 'AUX_REF': 1, 'EOL': 8})
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'AUX_REF', 'EOL')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
