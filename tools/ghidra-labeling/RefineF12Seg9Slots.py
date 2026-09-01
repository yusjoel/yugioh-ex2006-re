# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F12-Seg-9 [0x0809b178, 0x0809c3d8): slots and ASCII comments only.
# Proposal SHA256: 9c3892c87c14f6de87fa0a001d90d373f24a3a070e176d2107f31a23cf80265b
# Usage: RefineF12Seg9Slots.py dry|apply|check
# No function renames, disassembly, carve, or memory writes.

from ghidra.program.model.symbol import SourceType, RefType, SymbolType
from ghidra.program.model.listing import CodeUnit

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
DRY = MODE != 'apply'

# BEGIN PROPOSAL TABLES
EQ_SLOTS = [
    (0x0809b240, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_display_state_player_stride_9b240'),
    (0x0809b24c, 0x00001cf8, 'EQUIP_CHAIN_STEP_FROM_FIELD_OFF', 'equip_display_state_chain_step_from_field_offset_9b24c'),
    (0x0809b338, 0x000014d6, 'SPEAR_DRAGON_CID', 'equip_display_state_spear_dragon_cid_9b338'),
    (0x0809b33c, 0x00001993, 'AXE_DRAGONUTE_CID', 'equip_display_state_axe_dragonute_cid_9b33c'),
    (0x0809b344, 0x000018cd, 'KAMINOTE_BLOW_CID', 'equip_display_state_kaminote_blow_cid_9b344'),
    (0x0809b348, 0x00001866, 'KANGAROO_CHAMP_CID', 'equip_display_state_kangaroo_champ_cid_9b348'),
    (0x0809b34c, 0x0000170e, 'RYU_KOKKI_CID', 'equip_display_state_ryu_kokki_cid_9b34c'),
    (0x0809b354, 0x00001837, 'BIG_CORE_CID', 'equip_display_state_big_core_cid_9b354'),
    (0x0809b370, 0x000019a6, 'EHERO_NEO_BUBBLEMAN_CID', 'equip_display_state_ehero_neo_bubbleman_cid_9b370'),
    (0x0809b384, 0x000019bf, 'BES_COVERED_CORE_CID', 'equip_display_state_bes_covered_core_cid_9b384'),
    (0x0809b468, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_display_state_player_stride_9b468'),
    (0x0809b508, 0x00001837, 'BIG_CORE_CID', 'equip_display_state_big_core_cid_9b508'),
    (0x0809b50c, 0x00001703, 'PRICKLE_FAIRY_CID', 'equip_display_state_prickle_fairy_cid_9b50c'),
    (0x0809b510, 0x0000129c, 'BIG_SHIELD_GARDNA_CID', 'equip_display_state_big_shield_gardna_cid_9b510'),
    (0x0809b528, 0x0000170d, 'GETSU_FUHMA_CID', 'equip_display_state_getsu_fuhma_cid_9b528'),
    (0x0809b544, 0x00001962, 'BES_TETRAN_CID', 'equip_display_state_bes_tetran_cid_9b544'),
    (0x0809b55c, 0x000019bf, 'BES_COVERED_CORE_CID', 'equip_display_state_bes_covered_core_cid_9b55c'),
    (0x0809b56c, 0x000019c7, 'CHAINSAW_INSECT_CID', 'equip_display_state_chainsaw_insect_cid_9b56c'),
    (0x0809b680, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_display_state_player_stride_9b680'),
    (0x0809b704, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_display_state_chain_active_from_lp_offset_9b704'),
    (0x0809b734, 0x00001cf8, 'EQUIP_CHAIN_STEP_FROM_FIELD_OFF', 'equip_display_state_chain_step_from_field_offset_9b734'),
    (0x0809b7ac, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID', 'equip_display_state_black_luster_soldier_envoy_cid_9b7ac'),
    (0x0809b7b0, 0x00001cf8, 'EQUIP_CHAIN_STEP_FROM_FIELD_OFF', 'equip_display_state_chain_step_from_field_offset_9b7b0'),
    (0x0809b7dc, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_display_state_chain_active_from_lp_offset_9b7dc'),
    (0x0809b80c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9b80c'),
    (0x0809b84c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9b84c'),
    (0x0809b8b8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'equip_zone_state_current_player_from_lp_offset_9b8b8'),
    (0x0809b8bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_zone_state_player_stride_9b8bc'),
    (0x0809b8c4, 0x000015d2, 'GIANT_ORC_CID', 'equip_zone_state_giant_orc_cid_9b8c4'),
    (0x0809b8cc, 0x00001566, 'TOON_GOBLIN_AF_CID', 'equip_zone_state_toon_goblin_af_cid_9b8cc'),
    (0x0809b8e4, 0x00001915, 'INDOMITABLE_FIGHTER_LEI_LEI_CID', 'equip_zone_state_indomitable_fighter_lei_lei_cid_9b8e4'),
    (0x0809b8f0, 0x00001983, 'MYTHICAL_BEAST_CERBERUS_CID', 'equip_zone_state_mythical_beast_cerberus_cid_9b8f0'),
    (0x0809b954, 0x000014d6, 'SPEAR_DRAGON_CID', 'equip_zone_state_spear_dragon_cid_9b954'),
    (0x0809b95c, 0x00001419, 'GOBLIN_ATTACK_FORCE_CID', 'equip_zone_state_goblin_attack_force_cid_9b95c'),
    (0x0809ba24, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'equip_zone_state_current_player_from_lp_offset_9ba24'),
    (0x0809ba28, 0x00001392, 'SWORD_OF_DRAGONS_SOUL_CID', 'equip_zone_state_sword_of_dragons_soul_cid_9ba28'),
    (0x0809ba9c, 0x000012a6, 'SWORD_HUNTER_CID', 'equip_zone_state_sword_hunter_cid_9ba9c'),
    (0x0809baa4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9baa4'),
    (0x0809bad8, 0x00001415, 'RED_MOON_BABY_CID', 'equip_zone_state_red_moon_baby_cid_9bad8'),
    (0x0809badc, 0x00501415, 'RED_MOON_BABY_ACTIVATION_PACKED', 'equip_zone_state_red_moon_baby_activation_packed_9badc'),
    (0x0809baf4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9baf4'),
    (0x0809bb4c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'equip_zone_state_current_player_from_lp_offset_9bb4c'),
    (0x0809bb50, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_zone_state_player_stride_9bb50'),
    (0x0809bb58, 0x000012e2, 'MAGIC_ARM_SHIELD_CID', 'equip_zone_state_magic_arm_shield_cid_9bb58'),
    (0x0809bb5c, 0x00001cfc, 'EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF', 'equip_zone_state_chain_active_from_field_offset_9bb5c'),
    (0x0809bbe8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_zone_state_player_stride_9bbe8'),
    (0x0809bbf0, 0x00001362, 'MAGICAL_HATS_CID', 'equip_zone_state_magical_hats_cid_9bbf0'),
    (0x0809bc00, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9bc00'),
    (0x0809bc8c, 0x00001512, 'AFTER_THE_STRUGGLE_CID', 'equip_zone_state_after_the_struggle_cid_9bc8c'),
    (0x0809bc94, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_zone_state_player_stride_9bc94'),
    (0x0809bca0, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9bca0'),
    (0x0809bd1c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_zone_state_player_stride_9bd1c'),
    (0x0809bd20, 0x004e1571, 'HELPOEMER_ACTIVATION_PACKED', 'equip_zone_state_helpoemer_activation_packed_9bd20'),
    (0x0809bd28, 0xab880000, 'HELPOEMER_CID_SHIFTED', 'equip_zone_state_helpoemer_cid_shifted_9bd28'),
    (0x0809bd2c, 0xfffffbfc, 'HAND_ARRAY_TO_COUNT_NEG_OFF', 'equip_zone_state_card_array_to_count_neg_offset_9bd2c'),
    (0x0809bd30, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_zone_state_chain_active_from_lp_offset_9bd30'),
    (0x0809bd54, 0x00001469, 'THE_DARK_DOOR_CID', 'equip_zone_state_the_dark_door_cid_9bd54'),
    (0x0809bd58, 0x000011ed, 'eval_gap_cid_11ed', 'equip_zone_state_eval_gap_cid_11ed_9bd58'),
    (0x0809bdc4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_zone_state_player_stride_9bdc4'),
    (0x0809bdcc, 0x000012a6, 'SWORD_HUNTER_CID', 'equip_zone_state_sword_hunter_cid_9bdcc'),
    (0x0809bdf8, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'equip_zone_state_chain_step_from_lp_offset_9bdf8'),
    (0x0809be64, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_chain_attr_player_stride_9be64'),
    (0x0809be6c, 0x9fc80000, 'FAIRY_BOX_CID_SHIFTED', 'scan_chain_attr_fairy_box_cid_shifted_9be6c'),
    (0x0809beac, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'advance_equip_step_chain_step_from_lp_offset_9beac'),
    (0x0809beb0, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'advance_equip_step_chain_active_from_lp_offset_9beb0'),
    (0x0809bed8, 0x00001d94, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'tick_equip_phase_outer_state_from_lp_offset_9bed8'),
    (0x0809bf24, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'tick_equip_phase_chain_step_from_lp_offset_9bf24'),
    (0x0809bf28, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_equip_phase_chain_active_from_lp_offset_9bf28'),
    (0x0809bf30, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'tick_equip_phase_oam_equip_sprite_tile_p2_1b_9bf30'),
    (0x0809bf38, 0x00001d94, 'EQUIP_PHASE_DISPLAY_STATE_OFF', 'tick_equip_phase_outer_state_from_lp_offset_9bf38'),
    (0x0809bf54, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'tick_equip_phase_chain_step_from_lp_offset_9bf54'),
    (0x0809bfc0, 0x000014ff, 'YATA_GARASU_CID', 'check_new_equip_yata_garasu_cid_9bfc0'),
    (0x0809bfc8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_new_equip_player_stride_9bfc8'),
    (0x0809c028, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'dispatch_equip_action_current_player_from_lp_offset_9c028'),
    (0x0809c02c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_action_player_stride_9c02c'),
    (0x0809c030, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c030'),
    (0x0809c0a0, 0x000014ff, 'YATA_GARASU_CID', 'dispatch_equip_action_yata_garasu_cid_9c0a0'),
    (0x0809c0a4, 0x00001548, 'RECKLESS_GREED_CID', 'dispatch_equip_action_reckless_greed_cid_9c0a4'),
    (0x0809c0ac, 0x00008023, 'SPRITE_ATTR_DUEL_PHASE_P2_B', 'dispatch_equip_action_sprite_attr_duel_phase_p2_b_9c0ac'),
    (0x0809c0d4, 0x00000133, 'TRIGGER_OP_PARAM_133', 'dispatch_equip_action_trigger_op_param_133_9c0d4'),
    (0x0809c100, 0x0000800c, 'SPRITE_ATTR_DUEL_PHASE_P2_0C', 'dispatch_equip_action_sprite_attr_duel_phase_p2_0c_9c100'),
    (0x0809c104, 0x00008028, 'OAM_ZONE_SPRITE_PAIR_P2_FIRST', 'dispatch_equip_action_oam_zone_sprite_pair_p2_first_9c104'),
    (0x0809c19c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_action_player_stride_9c19c'),
    (0x0809c1a0, 0x00001911, 'CYBER_ARCHFIEND_CID', 'dispatch_equip_action_cyber_archfiend_cid_9c1a0'),
    (0x0809c1a8, 0x00001504, 'HINO_KAGU_TSUCHI_CID', 'dispatch_equip_action_hino_kagu_tsuchi_cid_9c1a8'),
    (0x0809c1e0, 0x000014fd, 'MAHARAGHI_CID', 'dispatch_equip_action_maharaghi_cid_9c1e0'),
    (0x0809c1e4, 0x025014fd, 'MAHARAGHI_ACTIVATION_PACKED', 'dispatch_equip_action_maharaghi_activation_packed_9c1e4'),
    (0x0809c2b4, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c2b4'),
    (0x0809c2b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_equip_action_player_stride_9c2b8'),
    (0x0809c2bc, 0x000014c4, 'FREED_THE_MATCHLESS_GENERAL_CID', 'dispatch_equip_action_freed_the_matchless_general_cid_9c2bc'),
    (0x0809c2c8, 0xcc200000, 'MAGICAL_BLAST_CID_SHIFTED', 'dispatch_equip_action_magical_blast_cid_shifted_9c2c8'),
    (0x0809c2cc, 0x004e1984, 'MAGICAL_BLAST_ACTIVATION_PACKED', 'dispatch_equip_action_magical_blast_activation_packed_9c2cc'),
    (0x0809c2ec, 0x000014c4, 'FREED_THE_MATCHLESS_GENERAL_CID', 'dispatch_equip_action_freed_the_matchless_general_cid_9c2ec'),
    (0x0809c2f4, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c2f4'),
    (0x0809c31c, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c31c'),
    (0x0809c334, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c334'),
    (0x0809c354, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'dispatch_equip_action_eligibility_state_from_lp_offset_9c354'),
    (0x0809c358, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'dispatch_equip_action_eligibility_type_from_lp_offset_9c358'),
    (0x0809c35c, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c35c'),
    (0x0809c374, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'dispatch_equip_action_eligibility_count_from_lp_offset_9c374'),
    (0x0809c378, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c378'),
    (0x0809c388, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c388'),
    (0x0809c3a4, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c3a4'),
    (0x0809c3c4, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF', 'dispatch_equip_action_card_play_phase_from_lp_offset_9c3c4'),
]

REF_SLOTS = [
    (0x0809b23c, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b23c'),
    (0x0809b244, 0x0201c510, 'gDuelFieldSlots', 'equip_display_state_field_base_9b244'),
    (0x0809b248, 0x0201e20c, 'gEquipChainActivePhase', 'equip_display_state_active_phase_ptr_9b248'),
    (0x0809b340, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b340'),
    (0x0809b3d8, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b3d8'),
    (0x0809b464, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b464'),
    (0x0809b46c, 0x0201c510, 'gDuelFieldSlots', 'equip_display_state_field_base_9b46c'),
    (0x0809b4b8, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b4b8'),
    (0x0809b504, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b504'),
    (0x0809b684, 0x0201c510, 'gDuelFieldSlots', 'equip_display_state_field_base_9b684'),
    (0x0809b6dc, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_display_state_chain_base_9b6dc'),
    (0x0809b738, 0x0201e20c, 'gEquipChainActivePhase', 'equip_display_state_active_phase_ptr_9b738'),
    (0x0809b7b4, 0x0201e20c, 'gEquipChainActivePhase', 'equip_display_state_active_phase_ptr_9b7b4'),
    (0x0809b810, 0x0809b814, 'switchD_0809b806__switchdataD_0809b814', 'equip_zone_state_switch_table_9b810'),
    (0x0809b8c0, 0x0201c510, 'gDuelFieldSlots', 'equip_zone_state_field_base_9b8c0'),
    (0x0809b958, 0x0201c510, 'gDuelFieldSlots', 'equip_zone_state_field_base_9b958'),
    (0x0809bb54, 0x0201c510, 'gDuelFieldSlots', 'equip_zone_state_field_base_9bb54'),
    (0x0809bbe4, 0x0201e1c8, 'gEquipZoneCountTable', 'equip_zone_state_current_player_ptr_9bbe4'),
    (0x0809bbec, 0x0201c510, 'gDuelFieldSlots', 'equip_zone_state_field_base_9bbec'),
    (0x0809bc90, 0x0201e1c8, 'gEquipZoneCountTable', 'equip_zone_state_current_player_ptr_9bc90'),
    (0x0809bc98, 0x0201c510, 'gDuelFieldSlots', 'equip_zone_state_field_base_9bc98'),
    (0x0809bd24, 0x0201c8f8, 'gP1HandSlotArray', 'equip_zone_state_card_word_array_base_9bd24'),
    (0x0809bdc8, 0x0201c510, 'gDuelFieldSlots', 'equip_zone_state_field_base_9bdc8'),
    (0x0809be68, 0x0201c510, 'gDuelFieldSlots', 'scan_chain_attr_field_base_9be68'),
    (0x0809bea4, 0x09e5aaec, 'equip_display_step_fn_table', 'advance_equip_step_handler_table_9bea4'),
    (0x0809bf2c, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_phase_chain_base_9bf2c'),
    (0x0809c034, 0x0809c038, 'switchD_0809c020__switchdataD_0809c038', 'dispatch_equip_action_switch_table_9c034'),
    (0x0809c0a8, 0x0201e2a0, 'gDuelCardCtxBase', 'dispatch_equip_action_display_ctx_base_9c0a8'),
    (0x0809c1a4, 0x0201c4ec, 'gP1ZoneHandCount', 'dispatch_equip_action_zone_count_base_9c1a4'),
    (0x0809c2c0, 0x0201c510, 'gDuelFieldSlots', 'dispatch_equip_action_field_base_9c2c0'),
    (0x0809c2c4, 0x0201c8f8, 'gP1HandSlotArray', 'dispatch_equip_action_card_word_array_base_9c2c4'),
    (0x0809c314, 0x0201e2a0, 'gDuelCardCtxBase', 'dispatch_equip_action_display_ctx_base_9c314'),
]

RENAME_SLOTS = [
    (0x0809b700, 'equip_display_state_lp_base_9b700', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809b7d8, 'equip_display_state_lp_base_9b7d8', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809b808, 'equip_zone_state_lp_base_9b808', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809b848, 'equip_zone_state_lp_base_9b848', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809b9dc, 'equip_zone_state_lp_base_9b9dc', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809ba2c, 'equip_zone_state_lp_base_9ba2c', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809baa0, 'equip_zone_state_lp_base_9baa0', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809baf0, 'equip_zone_state_lp_base_9baf0', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809bbfc, 'equip_zone_state_lp_base_9bbfc', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809bc9c, 'equip_zone_state_lp_base_9bc9c', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809bea8, 'advance_equip_step_lp_base_9bea8', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809bed4, 'tick_equip_phase_lp_base_9bed4', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809bf34, 'tick_equip_phase_lp_base_9bf34', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809bfc4, 'check_new_equip_lp_base_9bfc4', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c024, 'dispatch_equip_action_lp_base_9c024', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c2b0, 'dispatch_equip_action_lp_base_9c2b0', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c2f0, 'dispatch_equip_action_lp_base_9c2f0', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c318, 'dispatch_equip_action_lp_base_9c318', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c330, 'dispatch_equip_action_lp_base_9c330', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c3a0, 'dispatch_equip_action_lp_base_9c3a0', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
    (0x0809c3c0, 'dispatch_equip_action_lp_base_9c3c0', 'gP1LifePoints base; preserve the existing operand0 DATA/DEFAULT primary reference.'),
]

EXTRA_EOL = [
    (0x0809bb5c, 'Byte offset from gDuelFieldSlots to gEquipChainActivePhase; not DISP_SET_VARIANT_OFF from gP1LifePoints.'),
    (0x0809bbe4, 'Current player selector word; gP1LifePoints+P1LP_BLOCK2_OFF_1CE8.'),
    (0x0809bc90, 'Current player selector word; gP1LifePoints+P1LP_BLOCK2_OFF_1CE8.'),
    (0x0809bd24, 'Card-word array at gP1LifePoints+0x418; count at +0x14; four-byte entries. Retain existing global name.'),
    (0x0809c2c4, 'Card-word array at gP1LifePoints+0x418; count at +0x14; four-byte entries. Retain existing global name.'),
]

PLATES = [
    (0x0809b178, 'update_equip_activation_display_state', 'r0=player_side. Uses the shared equip phase at gEquipChainActivePhase. Phase 0 checks paired slot contexts and card chains, queues card-specific activation/display work, then advances phase. Phase 1 queues code 0x1e; the phase-six gate selects step 12, while an eligible Black Luster Soldier chain selects step 2 and resets phase. Other phases set step 1 and reset phase. Step uses gDuelFieldSlots+EQUIP_CHAIN_STEP_FROM_FIELD_OFF. Always returns 0.'),
    (0x0809b7e0, 'update_equip_zone_sprite_by_state', 'r0=player_side, saved in r10. Dispatches shared EQUIP_CHAIN_ACTIVE_OFF states 0..8: row setup, card-specific field scans, Sword Hunter/Red-Moon Baby work, Magic-Arm Shield, Magical Hats, After the Struggle and an opposing Helpoemer array scan. Work paths return 0; selected paths advance phase or retry it. Default queues The Dark Door; absent CID 0x11ed returns 1, otherwise queues that CID and clears step/phase. Internal return tail at 0x0809bde6 uses this frame.'),
    (0x0809bdfc, 'scan_equip_chain_slots_for_attr_enqueue', 'r0=player_side. Scan both players, field slots 5..9 (stride 0x14), comparing slot_word<<19 with FAIRY_BOX_CID_SHIFTED. Matching slots call enqueue_equip_chain_attrs_for_slot_range(player, slot). If check_activation_phase_counter_is_six returns 0, set caller player state bit 0x12 with sprite update. Always returns 1. Uses the field base and PLAYER_BLOCK_STRIDE; no mask test and no scan of slots 0..4.'),
    (0x0809be70, 'advance_equip_display_phase_via_table', 'r0=player_side. Index equip_display_step_fn_table by [gP1LifePoints+EQUIP_CHAIN_STEP_OFF], without a bounds check. A null entry returns 1. Otherwise invoke the Thumb handler with player_side; a nonzero result clears EQUIP_CHAIN_ACTIVE_OFF and increments the step. A zero result leaves both unchanged. Every non-null entry path returns 0. Table contains 14 handlers followed by a null terminator.'),
    (0x0809bebc, 'tick_equip_phase_display_by_state', 'r0=player_side; r1=extra_flag. Outer state is [gP1LifePoints+EQUIP_PHASE_DISPLAY_STATE_OFF]. State 0 sets step=6 and active phase=1, updates occupancy, optionally queues sprite code 0x1b/0x801b from chain context, sets chain+0x14=1 and advances outer state; returns 0. State 1 calls advance_equip_display_phase_via_table, then returns whether the stored unsigned step exceeds 8; it does not test that call result. Other states return 0.'),
    (0x0809bf60, 'check_field_allows_new_equip_action', 'r0=player_side. Require a Yata-Garasu node in zone 0xb, zero player count at gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0xc, no occupied monster zones, and no active equip slots. Then return 1 if the opposing player has a valid monster-pair slot or an available effect zone for Yata-Garasu; otherwise return 0. Pure checks; the +0xc word is a count, not an equip-lock flag.'),
    (0x0809bfd4, 'dispatch_equip_action_sprite_by_phase_state', 'Input registers unused. Read current player from gP1LifePoints+P1LP_BLOCK2_OFF_1CE8; dispatch CARD_PLAY_PHASE_CTR_OFF states 0..7. Handles draw-block display, Cyber Archfiend/Hino-Kagu-Tsuchi, Maharaghi, Freed/Magical Blast, display-context waits, zone pipeline and LP row update. Phase 2 can retry or fall through to phase 3. Returns 0 after work, phase updates or retries; returns 1 on blocked phase 0 or phase>7. Internal tail at 0x0809c3ca restores this frame.'),
]

ORIGINAL_LABELS = {
    0x0809b23c: 'DAT_0809b23c',
    0x0809b240: 'DAT_0809b240',
    0x0809b244: 'DAT_0809b244',
    0x0809b248: 'DAT_0809b248',
    0x0809b24c: 'DAT_0809b24c',
    0x0809b338: 'DAT_0809b338',
    0x0809b33c: 'DAT_0809b33c',
    0x0809b340: 'DAT_0809b340',
    0x0809b344: 'DAT_0809b344',
    0x0809b348: 'DAT_0809b348',
    0x0809b34c: 'DAT_0809b34c',
    0x0809b354: 'DAT_0809b354',
    0x0809b370: 'DAT_0809b370',
    0x0809b384: 'DAT_0809b384',
    0x0809b3d8: 'DAT_0809b3d8',
    0x0809b464: 'DAT_0809b464',
    0x0809b468: 'DAT_0809b468',
    0x0809b46c: 'DAT_0809b46c',
    0x0809b4b8: 'DAT_0809b4b8',
    0x0809b504: 'DAT_0809b504',
    0x0809b508: 'DAT_0809b508',
    0x0809b50c: 'DAT_0809b50c',
    0x0809b510: 'DAT_0809b510',
    0x0809b528: 'DAT_0809b528',
    0x0809b544: 'DAT_0809b544',
    0x0809b55c: 'DAT_0809b55c',
    0x0809b56c: 'DAT_0809b56c',
    0x0809b680: 'DAT_0809b680',
    0x0809b684: 'DAT_0809b684',
    0x0809b6dc: 'DAT_0809b6dc',
    0x0809b700: 'PTR_gP1LifePoints_0809b700',
    0x0809b704: 'DAT_0809b704',
    0x0809b734: 'DAT_0809b734',
    0x0809b738: 'DAT_0809b738',
    0x0809b7ac: 'DAT_0809b7ac',
    0x0809b7b0: 'DAT_0809b7b0',
    0x0809b7b4: 'DAT_0809b7b4',
    0x0809b7d8: 'PTR_gP1LifePoints_0809b7d8',
    0x0809b7dc: 'DAT_0809b7dc',
    0x0809b808: 'PTR_gP1LifePoints_0809b808',
    0x0809b80c: 'DAT_0809b80c',
    0x0809b810: 'PTR_switchdataD_0809b814_0809b810',
    0x0809b848: 'PTR_gP1LifePoints_0809b848',
    0x0809b84c: 'DAT_0809b84c',
    0x0809b8b8: 'DAT_0809b8b8',
    0x0809b8bc: 'DAT_0809b8bc',
    0x0809b8c0: 'DAT_0809b8c0',
    0x0809b8c4: 'DAT_0809b8c4',
    0x0809b8cc: 'DAT_0809b8cc',
    0x0809b8e4: 'DAT_0809b8e4',
    0x0809b8f0: 'DAT_0809b8f0',
    0x0809b954: 'DAT_0809b954',
    0x0809b958: 'DAT_0809b958',
    0x0809b95c: 'DAT_0809b95c',
    0x0809b9dc: 'PTR_gP1LifePoints_0809b9dc',
    0x0809ba24: 'DAT_0809ba24',
    0x0809ba28: 'DAT_0809ba28',
    0x0809ba2c: 'PTR_gP1LifePoints_0809ba2c',
    0x0809ba9c: 'DAT_0809ba9c',
    0x0809baa0: 'PTR_gP1LifePoints_0809baa0',
    0x0809baa4: 'DAT_0809baa4',
    0x0809bad8: 'DAT_0809bad8',
    0x0809badc: 'DAT_0809badc',
    0x0809baf0: 'PTR_gP1LifePoints_0809baf0',
    0x0809baf4: 'DAT_0809baf4',
    0x0809bb4c: 'DAT_0809bb4c',
    0x0809bb50: 'DAT_0809bb50',
    0x0809bb54: 'DAT_0809bb54',
    0x0809bb58: 'DAT_0809bb58',
    0x0809bb5c: 'DAT_0809bb5c',
    0x0809bbe4: 'DAT_0809bbe4',
    0x0809bbe8: 'DAT_0809bbe8',
    0x0809bbec: 'DAT_0809bbec',
    0x0809bbf0: 'DAT_0809bbf0',
    0x0809bbfc: 'PTR_gP1LifePoints_0809bbfc',
    0x0809bc00: 'DAT_0809bc00',
    0x0809bc8c: 'DAT_0809bc8c',
    0x0809bc90: 'DAT_0809bc90',
    0x0809bc94: 'DAT_0809bc94',
    0x0809bc98: 'DAT_0809bc98',
    0x0809bc9c: 'PTR_gP1LifePoints_0809bc9c',
    0x0809bca0: 'DAT_0809bca0',
    0x0809bd1c: 'DAT_0809bd1c',
    0x0809bd20: 'DAT_0809bd20',
    0x0809bd24: 'DAT_0809bd24',
    0x0809bd28: 'DAT_0809bd28',
    0x0809bd2c: 'DAT_0809bd2c',
    0x0809bd30: 'DAT_0809bd30',
    0x0809bd54: 'DAT_0809bd54',
    0x0809bd58: 'DAT_0809bd58',
    0x0809bdc4: 'DAT_0809bdc4',
    0x0809bdc8: 'DAT_0809bdc8',
    0x0809bdcc: 'DAT_0809bdcc',
    0x0809bdf8: 'DAT_0809bdf8',
    0x0809be64: 'DAT_0809be64',
    0x0809be68: 'DAT_0809be68',
    0x0809be6c: 'DAT_0809be6c',
    0x0809bea4: 'DAT_0809bea4',
    0x0809bea8: 'PTR_gP1LifePoints_0809bea8',
    0x0809beac: 'DAT_0809beac',
    0x0809beb0: 'DAT_0809beb0',
    0x0809bed4: 'PTR_gP1LifePoints_0809bed4',
    0x0809bed8: 'DAT_0809bed8',
    0x0809bf24: 'DAT_0809bf24',
    0x0809bf28: 'DAT_0809bf28',
    0x0809bf2c: 'DAT_0809bf2c',
    0x0809bf30: 'DAT_0809bf30',
    0x0809bf34: 'PTR_gP1LifePoints_0809bf34',
    0x0809bf38: 'DAT_0809bf38',
    0x0809bf54: 'DAT_0809bf54',
    0x0809bfc0: 'DAT_0809bfc0',
    0x0809bfc4: 'PTR_gP1LifePoints_0809bfc4',
    0x0809bfc8: 'DAT_0809bfc8',
    0x0809c024: 'PTR_gP1LifePoints_0809c024',
    0x0809c028: 'DAT_0809c028',
    0x0809c02c: 'DAT_0809c02c',
    0x0809c030: 'DAT_0809c030',
    0x0809c034: 'PTR_switchdataD_0809c038_0809c034',
    0x0809c0a0: 'DAT_0809c0a0',
    0x0809c0a4: 'DAT_0809c0a4',
    0x0809c0a8: 'DAT_0809c0a8',
    0x0809c0ac: 'DAT_0809c0ac',
    0x0809c0d4: 'DAT_0809c0d4',
    0x0809c100: 'DAT_0809c100',
    0x0809c104: 'DAT_0809c104',
    0x0809c19c: 'DAT_0809c19c',
    0x0809c1a0: 'DAT_0809c1a0',
    0x0809c1a4: 'DAT_0809c1a4',
    0x0809c1a8: 'DAT_0809c1a8',
    0x0809c1e0: 'DAT_0809c1e0',
    0x0809c1e4: 'DAT_0809c1e4',
    0x0809c2b0: 'PTR_gP1LifePoints_0809c2b0',
    0x0809c2b4: 'DAT_0809c2b4',
    0x0809c2b8: 'DAT_0809c2b8',
    0x0809c2bc: 'DAT_0809c2bc',
    0x0809c2c0: 'DAT_0809c2c0',
    0x0809c2c4: 'DAT_0809c2c4',
    0x0809c2c8: 'DAT_0809c2c8',
    0x0809c2cc: 'DAT_0809c2cc',
    0x0809c2ec: 'DAT_0809c2ec',
    0x0809c2f0: 'PTR_gP1LifePoints_0809c2f0',
    0x0809c2f4: 'DAT_0809c2f4',
    0x0809c314: 'DAT_0809c314',
    0x0809c318: 'PTR_gP1LifePoints_0809c318',
    0x0809c31c: 'DAT_0809c31c',
    0x0809c330: 'PTR_gP1LifePoints_0809c330',
    0x0809c334: 'DAT_0809c334',
    0x0809c354: 'DAT_0809c354',
    0x0809c358: 'DAT_0809c358',
    0x0809c35c: 'DAT_0809c35c',
    0x0809c374: 'DAT_0809c374',
    0x0809c378: 'DAT_0809c378',
    0x0809c388: 'DAT_0809c388',
    0x0809c3a0: 'PTR_gP1LifePoints_0809c3a0',
    0x0809c3a4: 'DAT_0809c3a4',
    0x0809c3c0: 'PTR_gP1LifePoints_0809c3c0',
    0x0809c3c4: 'DAT_0809c3c4',
}

SWITCH_WORDS = [
    (0x0809b814, 0x0809b838),
    (0x0809b818, 0x0809b850),
    (0x0809b81c, 0x0809b9e0),
    (0x0809b820, 0x0809ba30),
    (0x0809b824, 0x0809baa8),
    (0x0809b828, 0x0809baf8),
    (0x0809b82c, 0x0809bb60),
    (0x0809b830, 0x0809bc04),
    (0x0809b834, 0x0809bca4),
    (0x0809c038, 0x0809c058),
    (0x0809c03c, 0x0809c108),
    (0x0809c040, 0x0809c1ac),
    (0x0809c044, 0x0809c1f4),
    (0x0809c048, 0x0809c2d0),
    (0x0809c04c, 0x0809c338),
    (0x0809c050, 0x0809c38c),
    (0x0809c054, 0x0809c3a8),
]

EXTERNAL_WORDS = [
    (0x09e5aaec, 0x080977a1, 'enqueue_frozen_soul_zone_sprite_or_default'),
    (0x09e5aaf0, 0x08097829, 'dispatch_equip_activation_state_by_substate'),
    (0x09e5aaf4, 0x08097c2d, 'dispatch_equip_slot_display_state_by_phase'),
    (0x09e5aaf8, 0x08098265, 'tick_activation_display_state_machine'),
    (0x09e5aafc, 0x080984d1, 'activate_effect_zone_display_for_slot'),
    (0x09e5ab00, 0x08098565, 'tick_card_activation_phase_by_state'),
    (0x09e5ab04, 0x08098a89, 'tick_equip_zone_activation_display_state'),
    (0x09e5ab08, 0x08099315, 'dispatch_equip_field_phase_handler'),
    (0x09e5ab0c, 0x08099aad, 'run_equip_slot_display_update_state_machine'),
    (0x09e5ab10, 0x08099e0d, 'run_equip_spell_display_state_machine'),
    (0x09e5ab14, 0x0809a1a5, 'eval_equip_slot_pair_eligibility'),
    (0x09e5ab18, 0x0809b179, 'update_equip_activation_display_state'),
    (0x09e5ab1c, 0x0809b7e1, 'update_equip_zone_sprite_by_state'),
    (0x09e5ab20, 0x0809bdfd, 'scan_equip_chain_slots_for_attr_enqueue'),
    (0x09e5ab24, 0x00000000, 'NULL'),
]

SWITCH_LABELS = {
    0x0809b814: (7217, 'switchD_0809b806::switchdataD_0809b814', 'switchD_0809b806__switchdataD_0809b814'),
    0x0809c038: (7144, 'switchD_0809c020::switchdataD_0809c038', 'switchD_0809c020__switchdataD_0809c038'),
}
# END PROPOSAL TABLES

symTbl = currentProgram.getSymbolTable()
refMgr = currentProgram.getReferenceManager()
listing = currentProgram.getListing()
eqTbl = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL'))


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


PRESERVED_REFS = {}
RENAME_REFS = {}
CASE_SYMBOLS = {}
FUNCTION_BODIES = {}
EXTERNAL_STATE = None


def all_refs(slot):
    return sorted((str(r.getFromAddress()), str(r.getToAddress()), r.getOperandIndex(),
                   str(r.getReferenceType()), str(r.getSource()), r.isPrimary())
                  for r in refMgr.getReferencesFrom(toAddr(slot)))


def case_symbols(addr):
    return sorted((s.getID(), s.getName(True), str(s.getSymbolType()),
                   str(s.getSource()), s.isPrimary()) for s in symTbl.getSymbols(toAddr(addr)))


def require_switch_symbol(target, post=False):
    symbol_id, old_full, name = SWITCH_LABELS[target]
    symbol = symTbl.getSymbol(symbol_id)
    if (symbol is None or symbol.getID() != symbol_id or
            symbol.getAddress() != toAddr(target) or symbol.getSymbolType() != SymbolType.LABEL):
        fail('SWITCH_ID_ADDRESS_TYPE 0x%08x id=%d' % (target, symbol_id))
        return None
    if symbol.getName(True) not in (old_full, name) or symbol.getName() not in (old_full.split('::')[-1], name):
        fail('SWITCH_PATTERN 0x%08x %s' % (target, symbol.getName(True)))
    for other in symTbl.getGlobalSymbols(name):
        if other.getID() != symbol_id:
            fail('SWITCH_NAME_COLLISION 0x%08x id=%d' % (target, other.getID()))
    if not symbol.isPrimary():
        fail('SWITCH_PRIMARY 0x%08x' % target)
    if post and (symbol.getName() != name or symbol.getName(True) != name or
                 symbol.getSource() != SourceType.USER_DEFINED):
        fail('POST_SWITCH_NORMALIZED 0x%08x' % target)
    print('SWITCH_SYMBOL phase=%s address=%08x id=%d name=%s source=%s' %
          ('post' if post else 'pre', target, symbol.getID(), symbol.getName(True), symbol.getSource()))
    return symbol


def require_rename_reference(slot):
    refs = [r for r in refMgr.getReferencesFrom(toAddr(slot)) if r.isPrimary()]
    if (len(refs) != 1 or refs[0].getFromAddress() != toAddr(slot) or
            refs[0].getToAddress() != toAddr(0x0201c4e0) or
            refs[0].getOperandIndex() != 0 or refs[0].getReferenceType() != RefType.DATA or
            refs[0].getSource() != SourceType.DEFAULT):
        fail('RENAME_EXISTING_REF 0x%08x' % slot)
    target = symTbl.getPrimarySymbol(toAddr(0x0201c4e0))
    if (target is None or target.getName() != 'gP1LifePoints' or
            target.getSymbolType() != SymbolType.LABEL or target.getSource() != SourceType.USER_DEFINED):
        fail('RENAME_TARGET_LABEL 0x%08x' % slot)


def external_state():
    definitions, outgoing, incoming = [], [], []
    for value in range(0x09e5aaec, 0x09e5ab28):
        addr = toAddr(value)
        data = listing.getDefinedDataAt(addr)
        if data is not None:
            definitions.append((str(data.getAddress()), data.getLength(),
                                data.getDataType().getPathName(), str(data.getMinAddress()), str(data.getMaxAddress())))
        for row in all_refs(value):
            outgoing.append(row)
        for ref in refMgr.getReferencesTo(addr):
            # The sole permitted incoming change is the planned base reference.
            if (value == 0x09e5aaec and ref.getFromAddress() == toAddr(0x0809bea4)
                    and ref.getOperandIndex() == 0):
                continue
            incoming.append((str(ref.getFromAddress()), str(ref.getToAddress()), ref.getOperandIndex(),
                             str(ref.getReferenceType()), str(ref.getSource()), ref.isPrimary()))
    return (definitions, sorted(outgoing), sorted(incoming))


def verify_tables():
    for slot, target in SWITCH_WORDS:
        _check(slot, target)
        if target & 1 or getInstructionAt(toAddr(target)) is None:
            fail('SWITCH_EVEN_CODE 0x%08x' % target)
        mode = currentProgram.getProgramContext().getValue(currentProgram.getRegister('TMode'), toAddr(target), False)
        if mode is None or int(mode) != 1:
            fail('SWITCH_THUMB_CONTEXT 0x%08x' % target)
    for addr in (0x0809b806, 0x0809c020):
        if memory.getShort(toAddr(addr)) & 0xffff != 0x4687:
            fail('SWITCH_MOV_PC 0x%08x' % addr)
    for slot, value, name in EXTERNAL_WORDS:
        actual = memory.getInt(toAddr(slot)) & 0xffffffff
        if actual != value:
            fail('EXTERNAL_RAW_VALUE 0x%08x expected=%08x actual=%08x' % (slot, value, actual))
        if value:
            fn = getFunctionAt(toAddr(value & 0xfffffffe))
            if not value & 1 or fn is None or fn.getName() != name:
                fail('EXTERNAL_THUMB_FUNCTION 0x%08x' % slot)
    if listing.getDefinedDataAt(toAddr(0x09e5ab24)) is not None:
        fail('EXTERNAL_NULL_DEFINITION_CHANGED')
    if getFunctionAt(toAddr(0x09e5aaec)) is not None:
        fail('EXTERNAL_TABLE_NOT_FUNCTION')


def preserved_refs(slot, target):
    return sorted((str(r.getFromAddress()), str(r.getToAddress()), r.getOperandIndex(),
                   str(r.getReferenceType()), str(r.getSource()))
                  for r in refMgr.getReferencesFrom(toAddr(slot))
                  if not (r.getOperandIndex() == 0 and r.getToAddress() == toAddr(target)))


def preflight():
    global EXTERNAL_STATE
    verify_tables()
    EXTERNAL_STATE = external_state()
    print('EXTERNAL_STATE_BEFORE %r' % (EXTERNAL_STATE,))
    for target in SWITCH_LABELS:
        require_switch_symbol(target)
    for slot, target in SWITCH_WORDS:
        CASE_SYMBOLS[target] = case_symbols(target)
    all_slots = [r[0] for r in EQ_SLOTS + REF_SLOTS + RENAME_SLOTS]
    if len(all_slots) != 157 or len(set(all_slots)) != 157:
        fail('SLOT_COVERAGE')
    for slot, value, name, label in EQ_SLOTS + REF_SLOTS:
        _check(slot, value)
        require_name_available(label, slot)
        if not 0x0809b178 <= slot < 0x0809c3d8:
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
        PRESERVED_REFS[slot] = preserved_refs(slot, target)
        primary = symTbl.getPrimarySymbol(toAddr(target))
        if primary is not None and primary.getSymbolType() == SymbolType.FUNCTION:
            fail('REF_TARGET_FUNCTION 0x%08x' % target)
    for slot, label, eol in RENAME_SLOTS:
        _check(slot, 0x0201c4e0)
        require_name_available(label, slot)
        require_ascii(eol, 'RENAME 0x%08x' % slot)
        if not 0x0809b178 <= slot < 0x0809c3d8:
            fail('RENAME_RANGE 0x%08x' % slot)
        RENAME_REFS[slot] = all_refs(slot)
        require_rename_reference(slot)
        names = [s.getName() for s in symTbl.getSymbols(toAddr(slot))]
        if ORIGINAL_LABELS[slot] not in names and label not in names:
            fail('RENAME_PATTERN 0x%08x' % slot)
    for slot, text in EXTRA_EOL:
        if slot not in all_slots:
            fail('EXTRA_EOL_SLOT 0x%08x' % slot)
        require_ascii(text, 'EXTRA_EOL 0x%08x' % slot)
    for addr, fn_name, text in PLATES:
        fn = getFunctionAt(toAddr(addr))
        cu = listing.getCodeUnitAt(toAddr(addr))
        if fn is None or fn.getName() != fn_name or cu is None:
            fail('PLATE_FUNCTION 0x%08x %s' % (addr, fn_name))
        else:
            FUNCTION_BODIES[addr] = str(fn.getBody())
        if cu is not None and not cu.getComment(CodeUnit.PLATE_COMMENT):
            fail('PLATE_PATTERN 0x%08x' % addr)
        require_ascii(text, 'PLATE 0x%08x' % addr)
        if len(text) > 500:
            fail('PLATE_LENGTH 0x%08x %d' % (addr, len(text)))
    print('PREFLIGHT slots=157 EQ=104 REF=32 RENAME=21 PLATE=7 EOL=26 FAIL=%d' % len(FAILS))


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
        if old.getOperandIndex() == 0 and old.getToAddress() == to:
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
        if target in SWITCH_LABELS:
            target_symbol = symTbl.getSymbol(SWITCH_LABELS[target][0])
            # Preserve the exact switch Symbol object; normalize its GAS spelling.
            target_symbol.setNamespace(currentProgram.getGlobalNamespace())
            target_symbol.setName(name, SourceType.USER_DEFINED)
        elif target_symbol is None:
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
    for slot, text in EXTRA_EOL:
        listing.getCodeUnitAt(toAddr(slot)).setComment(CodeUnit.EOL_COMMENT, text)
        COUNTS['EOL'] += 1
    for addr, fn_name, text in PLATES:
        listing.getCodeUnitAt(toAddr(addr)).setComment(CodeUnit.PLATE_COMMENT, text)
        COUNTS['PLATE'] += 1


def verify_applied():
    verify_tables()
    after = external_state()
    if after != EXTERNAL_STATE:
        fail('POST_EXTERNAL_DEFINITIONS_OR_REFS')
    print('EXTERNAL_STATE_AFTER %r' % (after,))
    print('EXTERNAL_PRESERVED definitions=%d outgoing_refs=%d other_incoming_refs=%d null_defined=False' %
          (len(after[0]), len(after[1]), len(after[2])))
    for target in SWITCH_LABELS:
        require_switch_symbol(target, True)
    for slot, target in SWITCH_WORDS:
        if case_symbols(target) != CASE_SYMBOLS[target]:
            fail('POST_CASE_SYMBOLS 0x%08x' % target)
    for addr, body in FUNCTION_BODIES.items():
        if str(getFunctionAt(toAddr(addr)).getBody()) != body:
            fail('POST_FUNCTION_BODY 0x%08x' % addr)
    for slot, refs in RENAME_REFS.items():
        require_rename_reference(slot)
        if all_refs(slot) != refs:
            fail('POST_RENAME_REFS 0x%08x' % slot)
    for slot, text in EXTRA_EOL:
        if listing.getCodeUnitAt(toAddr(slot)).getComment(CodeUnit.EOL_COMMENT) != text:
            fail('POST_EXTRA_EOL 0x%08x' % slot)
    for slot, value, name, label in EQ_SLOTS:
        _check(slot, value)
        found = list(eqTbl.getEquates(toAddr(slot)))
        if len(found) != 1 or found[0].getName() != name or (found[0].getValue() & 0xffffffff) != value:
            fail('POST_EQUATE 0x%08x' % slot)
    for slot, target, name, label in REF_SLOTS:
        if preserved_refs(slot, target) != PRESERVED_REFS[slot]:
            fail('POST_PRESERVED_REFS 0x%08x' % slot)
        primary = symTbl.getPrimarySymbol(toAddr(target))
        if (primary is None or primary.getName() != name or
                primary.getSymbolType() != SymbolType.LABEL or
                primary.getSource() != SourceType.USER_DEFINED):
            fail('POST_TARGET 0x%08x' % slot)
        refs = [r for r in refMgr.getReferencesFrom(toAddr(slot)) if r.isPrimary()]
        if (len(refs) != 1 or refs[0].getToAddress() != toAddr(target) or
                refs[0].getFromAddress() != toAddr(slot) or refs[0].getOperandIndex() != 0 or
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
    for addr, fn_name, text in PLATES:
        if listing.getCodeUnitAt(toAddr(addr)).getComment(CodeUnit.PLATE_COMMENT) != text:
            fail('POST_PLATE 0x%08x' % addr)
        if getFunctionAt(toAddr(addr)).getName() != fn_name:
            fail('POST_FUNCTION_NAME 0x%08x' % addr)


print('=== RefineF12Seg9Slots mode=%s ===' % MODE)
preflight()
if FAILS:
    raise RuntimeError('PREFLIGHT FAIL; no writes performed')
if MODE == 'apply':
    transaction = currentProgram.startTransaction('Refine F12-Seg-9 slots')
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
    COUNTS.update({'EQ': 104, 'REF': 32, 'RENAME': 21, 'PLATE': 7, 'EOL': 26})
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
