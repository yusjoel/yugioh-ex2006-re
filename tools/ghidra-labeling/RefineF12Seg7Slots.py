# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F12-Seg-7 [0x08099314, 0x0809a1a4): slots and ASCII comments only.
# Proposal SHA256: 5463ac0f317237ce2af3e3c998a0bceb2f31af53e2179253a8e540d18e0df51d
# Usage: RefineF12Seg7Slots.py dry|apply|check
# No function renames, disassembly, carve, or memory writes.

from ghidra.program.model.symbol import SourceType, RefType, SymbolType
from ghidra.program.model.listing import CodeUnit

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
DRY = MODE != 'apply'

# BEGIN PROPOSAL TABLES
EQ_SLOTS = [
    (0x08099368, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_99368'),
    (0x080993b8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_993b8'),
    (0x080993e4, 0x00001913, 'BES_CRYSTAL_CORE_CID', 'equip_field_phase_bes_crystal_core_cid_993e4'),
    (0x080993e8, 0x00001643, 'MIRAGE_KNIGHT_CID', 'equip_field_phase_mirage_knight_cid_993e8'),
    (0x080993f0, 0x00001837, 'BIG_CORE_CID', 'equip_field_phase_big_core_cid_993f0'),
    (0x08099408, 0x00001983, 'MYTHICAL_BEAST_CERBERUS_CID', 'equip_field_phase_mythical_beast_cerberus_cid_99408'),
    (0x0809941c, 0x000019bf, 'BES_COVERED_CORE_CID', 'equip_field_phase_bes_covered_core_cid_9941c'),
    (0x080994cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_field_phase_player_block_stride_994cc'),
    (0x080994d4, 0x00001cb8, 'EQUIP_ZONE_COUNT_TABLE_OFF', 'equip_field_phase_equip_zone_count_table_off_994d4'),
    (0x08099510, 0x00001512, 'AFTER_THE_STRUGGLE_CID', 'equip_field_phase_after_the_struggle_cid_99510'),
    (0x0809951c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_9951c'),
    (0x0809954c, 0x00001913, 'BES_CRYSTAL_CORE_CID', 'equip_field_phase_bes_crystal_core_cid_9954c'),
    (0x08099550, 0x00001749, 'LEGENDARY_JUJITSU_MASTER_CID', 'equip_field_phase_legendary_jujitsu_master_cid_99550'),
    (0x08099554, 0x00001643, 'MIRAGE_KNIGHT_CID', 'equip_field_phase_mirage_knight_cid_99554'),
    (0x08099564, 0x0000182c, 'HARPIE_LADY_3_CID', 'equip_field_phase_harpie_lady_3_cid_99564'),
    (0x0809957c, 0x00001983, 'MYTHICAL_BEAST_CERBERUS_CID', 'equip_field_phase_mythical_beast_cerberus_cid_9957c'),
    (0x08099590, 0x000019bf, 'BES_COVERED_CORE_CID', 'equip_field_phase_bes_covered_core_cid_99590'),
    (0x080995e0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_field_phase_player_block_stride_995e0'),
    (0x0809966c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_field_phase_player_block_stride_9966c'),
    (0x08099674, 0x00001cb8, 'EQUIP_ZONE_COUNT_TABLE_OFF', 'equip_field_phase_equip_zone_count_table_off_99674'),
    (0x08099718, 0x00001512, 'AFTER_THE_STRUGGLE_CID', 'equip_field_phase_after_the_struggle_cid_99718'),
    (0x08099720, 0x0000129a, 'REFLECT_BOUNDER_CID', 'equip_field_phase_reflect_bounder_cid_99720'),
    (0x08099724, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'equip_field_phase_player_block_stride_99724'),
    (0x08099794, 0x00008016, 'OAM_EQUIP_SPRITE_P2_16', 'equip_field_phase_oam_equip_sprite_p2_16_99794'),
    (0x08099798, 0xffff0000, 'SPRITE_HIGH_HALF_MASK', 'equip_field_phase_sprite_high_half_mask_99798'),
    (0x0809982c, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'equip_field_phase_sprite_low_half_mask_9982c'),
    (0x08099834, 0x000013aa, 'KINETIC_SOLDIER_CID', 'equip_field_phase_kinetic_soldier_cid_99834'),
    (0x08099838, 0x000014cc, 'HUNTER_7_WEAPONS_CID', 'equip_field_phase_hunter_7_weapons_cid_99838'),
    (0x08099840, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_99840'),
    (0x08099860, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'equip_field_phase_equip_chain_step_off_99860'),
    (0x08099864, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_99864'),
    (0x0809987c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_9987c'),
    (0x08099940, 0x0000ffff, 'EQUIP_ACTIVATION_CNT_CAP', 'equip_field_phase_equip_activation_cnt_cap_99940'),
    (0x08099944, 0x00008017, 'OAM_EQUIP_SPRITE_P2_17', 'equip_field_phase_oam_equip_sprite_p2_17_99944'),
    (0x08099978, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_99978'),
    (0x080999dc, 0x00008021, 'OAM_EQUIP_SPRITE_P2_21', 'equip_field_phase_oam_equip_sprite_p2_21_999dc'),
    (0x08099a70, 0x000001ff, 'EQUIP_PAYLOAD_LOW9_MASK', 'equip_field_phase_equip_payload_low9_mask_99a70'),
    (0x08099a74, 0xfffffe00, 'EQUIP_PAYLOAD_CLEAR_LOW9_MASK', 'equip_field_phase_equip_payload_clear_low9_mask_99a74'),
    (0x08099a78, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10', 'equip_field_phase_oam_sprite_attr_clr_bits13_10_99a78'),
    (0x08099a7c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'equip_field_phase_slot_active_bit14_clr_99a7c'),
    (0x08099a80, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16', 'equip_field_phase_oam_sprite_attr_clr_bit16_99a80'),
    (0x08099a84, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17', 'equip_field_phase_oam_sprite_attr_clr_bit17_99a84'),
    (0x08099a88, 0x2a200000, 'EQUIP_ACTIVATION_PACKED_TYPE21', 'equip_field_phase_equip_activation_packed_type21_99a88'),
    (0x08099a90, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'equip_field_phase_equip_chain_step_off_99a90'),
    (0x08099a94, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_field_phase_equip_chain_active_off_99a94'),
    (0x08099b00, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_slot_update_equip_chain_active_off_99b00'),
    (0x08099ba8, 0x0000ffff, 'EQUIP_ACTIVATION_CNT_CAP', 'equip_slot_update_equip_activation_cnt_cap_99ba8'),
    (0x08099bac, 0xffff0000, 'SPRITE_HIGH_HALF_MASK', 'equip_slot_update_sprite_high_half_mask_99bac'),
    (0x08099bb0, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16', 'equip_slot_update_oam_sprite_attr_clr_bit16_99bb0'),
    (0x08099bb4, 0xffe1ffff, 'OAM_SPRITE_ATTR_CLR_BITS20_17', 'equip_slot_update_oam_sprite_attr_clr_bits20_17_99bb4'),
    (0x08099bb8, 0xffdfffff, 'SLOT_BIT21_CLR', 'equip_slot_update_slot_bit21_clr_99bb8'),
    (0x08099bbc, 0xfc3fffff, 'OAM_SPRITE_ATTR_CLR_BITS25_22', 'equip_slot_update_oam_sprite_attr_clr_bits25_22_99bbc'),
    (0x08099bdc, 0x000012ac, 'SATELLITE_CANNON_CID', 'equip_slot_update_satellite_cannon_cid_99bdc'),
    (0x08099be0, 0x000013cb, 'ROCKET_WARRIOR_CID', 'equip_slot_update_rocket_warrior_cid_99be0'),
    (0x08099c34, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'equip_slot_update_p1lp_block2_off_1ce8_99c34'),
    (0x08099c38, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'equip_slot_update_p2lp_block2_off_1cf4_99c38'),
    (0x08099c74, 0x00001826, 'ELEMENT_MAGICIAN_CID', 'equip_slot_update_element_magician_cid_99c74'),
    (0x08099c78, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID', 'equip_slot_update_black_luster_soldier_envoy_cid_99c78'),
    (0x08099c7c, 0x000013b1, 'TIMEATER_CID', 'equip_slot_update_timeater_cid_99c7c'),
    (0x08099c88, 0x000017e3, 'ELEMENT_DRAGON_CID', 'equip_slot_update_element_dragon_cid_99c88'),
    (0x08099d5c, 0x00001861, 'ELEMENT_DOOM_CID', 'equip_slot_update_element_doom_cid_99d5c'),
    (0x08099d60, 0x000019d4, 'RUIN_QUEEN_OF_OBLIVION_CID', 'equip_slot_update_ruin_queen_of_oblivion_cid_99d60'),
    (0x08099d68, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'equip_slot_update_sprite_low_half_mask_99d68'),
    (0x08099d70, 0x000013b1, 'TIMEATER_CID', 'equip_slot_update_timeater_cid_99d70'),
    (0x08099d78, 0x0000129a, 'REFLECT_BOUNDER_CID', 'equip_slot_update_reflect_bounder_cid_99d78'),
    (0x08099d7c, 0x000016bf, 'BERSERK_GORILLA_CID', 'equip_slot_update_berserk_gorilla_cid_99d7c'),
    (0x08099e08, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_slot_update_equip_chain_active_off_99e08'),
    (0x08099e5c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_spell_display_equip_chain_active_off_99e5c'),
    (0x08099eb0, 0x2a200000, 'EQUIP_ACTIVATION_PACKED_TYPE21', 'equip_spell_display_equip_activation_packed_type21_99eb0'),
    (0x08099eb4, 0x00001770, 'MARSHMALLON_CID', 'equip_spell_display_marshmallon_cid_99eb4'),
    (0x08099ebc, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_spell_display_equip_chain_active_off_99ebc'),
    (0x08099efc, 0x2a200000, 'EQUIP_ACTIVATION_PACKED_TYPE21', 'equip_spell_display_equip_activation_packed_type21_99efc'),
    (0x08099f00, 0x000015d9, 'DD_CRAZY_BEAST_CID', 'equip_spell_display_dd_crazy_beast_cid_99f00'),
    (0x08099f04, 0x0000112f, 'cid_112f', 'equip_spell_display_cid_112f_99f04'),
    (0x08099f10, 0x00001135, 'cid_1135', 'equip_spell_display_cid_1135_99f10'),
    (0x08099f28, 0x0000172c, 'DD_ASSAILANT_CID', 'equip_spell_display_dd_assailant_cid_99f28'),
    (0x08099f34, 0x000018e6, 'HOLY_KNIGHT_ISHZARK_CID', 'equip_spell_display_holy_knight_ishzark_cid_99f34'),
    (0x08099f6c, 0x00008046, 'OAM_EQUIP_SPRITE_P2_46', 'equip_spell_display_oam_equip_sprite_p2_46_99f6c'),
    (0x08099ff0, 0x2a200000, 'EQUIP_ACTIVATION_PACKED_TYPE21', 'equip_spell_display_equip_activation_packed_type21_99ff0'),
    (0x08099ff4, 0x000013b1, 'TIMEATER_CID', 'equip_spell_display_timeater_cid_99ff4'),
    (0x08099ff8, 0x00001130, 'cid_1130', 'equip_spell_display_cid_1130_99ff8'),
    (0x0809a008, 0x00001208, 'cid_1208', 'equip_spell_display_cid_1208_9a008'),
    (0x0809a00c, 0x00001310, 'WALL_OF_ILLUSION_CID', 'equip_spell_display_wall_of_illusion_cid_9a00c'),
    (0x0809a024, 0x00001657, 'DD_WARRIOR_LADY_CID', 'equip_spell_display_dd_warrior_lady_cid_9a024'),
    (0x0809a028, 0x000014f1, 'KELBEK_CID', 'equip_spell_display_kelbek_cid_9a028'),
    (0x0809a03c, 0x0000172c, 'DD_ASSAILANT_CID', 'equip_spell_display_dd_assailant_cid_9a03c'),
    (0x0809a040, 0x000018e6, 'HOLY_KNIGHT_ISHZARK_CID', 'equip_spell_display_holy_knight_ishzark_cid_9a040'),
    (0x0809a07c, 0x00008046, 'OAM_EQUIP_SPRITE_P2_46', 'equip_spell_display_oam_equip_sprite_p2_46_9a07c'),
    (0x0809a184, 0x000001ff, 'EQUIP_PAYLOAD_LOW9_MASK', 'equip_spell_display_equip_payload_low9_mask_9a184'),
    (0x0809a188, 0xfffffe00, 'EQUIP_PAYLOAD_CLEAR_LOW9_MASK', 'equip_spell_display_equip_payload_clear_low9_mask_9a188'),
    (0x0809a18c, 0xfffffdff, 'OAM_SPRITE_ATTR_CLR_BIT9', 'equip_spell_display_oam_sprite_attr_clr_bit9_9a18c'),
    (0x0809a190, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10', 'equip_spell_display_oam_sprite_attr_clr_bits13_10_9a190'),
    (0x0809a194, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'equip_spell_display_slot_active_bit14_clr_9a194'),
    (0x0809a198, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16', 'equip_spell_display_oam_sprite_attr_clr_bit16_9a198'),
    (0x0809a19c, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17', 'equip_spell_display_oam_sprite_attr_clr_bit17_9a19c'),
    (0x0809a1a0, 0x00008060, 'OAM_EQUIP_SPRITE_P2_60', 'equip_spell_display_oam_equip_sprite_p2_60_9a1a0'),
]

REF_SLOTS = [
    (0x08099360, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99360'),
    (0x0809936c, 0x08099370, 'switchD_0809935c__switchdataD_08099370', 'equip_field_phase_phase_table_ptr_9936c'),
    (0x08099438, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99438'),
    (0x08099454, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99454'),
    (0x080994c8, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_994c8'),
    (0x080994d0, 0x0201c510, 'gDuelFieldSlots', 'equip_field_phase_field_slots_base_994d0'),
    (0x08099514, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99514'),
    (0x080995ac, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_995ac'),
    (0x080995e4, 0x0201c510, 'gDuelFieldSlots', 'equip_field_phase_field_slots_base_995e4'),
    (0x08099600, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99600'),
    (0x08099670, 0x0201c510, 'gDuelFieldSlots', 'equip_field_phase_field_slots_base_99670'),
    (0x0809971c, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_9971c'),
    (0x08099728, 0x0201c510, 'gDuelFieldSlots', 'equip_field_phase_field_slots_base_99728'),
    (0x08099790, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99790'),
    (0x08099830, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99830'),
    (0x08099934, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_99934'),
    (0x08099938, 0x0201bbbc, 'gDuelEquipCtx', 'equip_field_phase_context_base_99938'),
    (0x0809993c, 0x0201bbc0, 'gDuelEquipCtxSlotIndex', 'equip_field_phase_context_slot_index_base_9993c'),
    (0x080999d8, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_field_phase_chain_base_999d8'),
    (0x08099af8, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_slot_update_chain_base_99af8'),
    (0x08099d64, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_slot_update_chain_base_99d64'),
    (0x08099d6c, 0x0201bc54, 'gDuelEffectChainSlots', 'equip_slot_update_effect_chain_slots_99d6c'),
    (0x08099d74, 0x0201bc2c, 'gEquipActivationSlotBase', 'equip_slot_update_activation_slots_99d74'),
    (0x08099e54, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_spell_display_chain_base_99e54'),
    (0x08099f68, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_spell_display_chain_base_99f68'),
    (0x08099fec, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_spell_display_chain_base_99fec'),
    (0x0809a180, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_spell_display_chain_base_9a180'),
]

RENAME_SLOTS = [
    (0x08099364, 'equip_field_phase_lp_base_99364', 'gP1LifePoints base for equip display state.'),
    (0x080993b4, 'equip_field_phase_lp_base_993b4', 'gP1LifePoints base for equip display state.'),
    (0x08099518, 'equip_field_phase_lp_base_99518', 'gP1LifePoints base for equip display state.'),
    (0x0809983c, 'equip_field_phase_lp_base_9983c', 'gP1LifePoints base for equip display state.'),
    (0x0809985c, 'equip_field_phase_lp_base_9985c', 'gP1LifePoints base for equip display state.'),
    (0x08099878, 'equip_field_phase_lp_base_99878', 'gP1LifePoints base for equip display state.'),
    (0x08099974, 'equip_field_phase_lp_base_99974', 'gP1LifePoints base for equip display state.'),
    (0x08099a8c, 'equip_field_phase_lp_base_99a8c', 'gP1LifePoints base for equip display state.'),
    (0x08099afc, 'equip_slot_update_lp_base_99afc', 'gP1LifePoints base for equip display state.'),
    (0x08099e04, 'equip_slot_update_lp_base_99e04', 'gP1LifePoints base for equip display state.'),
    (0x08099e58, 'equip_spell_display_lp_base_99e58', 'gP1LifePoints base for equip display state.'),
    (0x08099eb8, 'equip_spell_display_lp_base_99eb8', 'gP1LifePoints base for equip display state.'),
]
PLATES = [
    (0x08099314, 'dispatch_equip_field_phase_handler', 'Dispatches equip field display phases 0..10 for r0=player_side. Uses gEquipChainSlotRefs and 0x38-byte player contexts at gDuelEquipCtx; phase is [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Phases score candidates, queue sprites, pack LP rows, scan candidates (phase 4), and apply activations. Mismatch exits write step 11 and clear phase; phase 0 instead routes to phase 10. Returns 0 while pending, 1 when complete. Cases 7/8/9 and out-of-range phases complete.'),
    (0x08099aac, 'run_equip_slot_display_update_state_machine', 'Ticks equip slot display phases for r0=player_side. Uses two 0x38-byte contexts at gDuelEquipCtx and phase [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Phase 0 packs two 0x14-byte activation records into LP row type 14 unless chain[+0x14] is set. Phase 1 queues Satellite Cannon/Rocket Warrior displays; phase 2 applies card-specific activations and updates sprites. Brackets row/activation work with LP display counter calls. Returns 0 through phases 0..2, 1 after phase 2.'),
    (0x08099e0c, 'run_equip_spell_display_state_machine', 'Ticks equip spell display phases for r0=player_side using paired 0x38-byte contexts at gDuelEquipCtx. State is [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Nonzero chain[+8] returns 1. Phase 0 polls two sprite scanners, applies the Marshmallon path, then advances phase; scanner activity returns 0 without advancing. Phase 1 queues card-specific displays and applies packed type-21 activations without advancing phase locally. Returns 0 in phase 0 and 1 for phase 1 or other phases.'),
]
ORIGINAL_LABELS = {
    0x08099360: 'DAT_08099360',
    0x08099364: 'PTR_gP1LifePoints_08099364',
    0x08099368: 'DAT_08099368',
    0x0809936c: 'PTR_switchdataD_08099370_0809936c',
    0x080993b4: 'PTR_gP1LifePoints_080993b4',
    0x080993b8: 'DAT_080993b8',
    0x080993e4: 'DAT_080993e4',
    0x080993e8: 'DAT_080993e8',
    0x080993f0: 'DAT_080993f0',
    0x08099408: 'DAT_08099408',
    0x0809941c: 'DAT_0809941c',
    0x08099438: 'DAT_08099438',
    0x08099454: 'DAT_08099454',
    0x080994c8: 'DAT_080994c8',
    0x080994cc: 'DAT_080994cc',
    0x080994d0: 'DAT_080994d0',
    0x080994d4: 'DAT_080994d4',
    0x08099510: 'DAT_08099510',
    0x08099514: 'DAT_08099514',
    0x08099518: 'PTR_gP1LifePoints_08099518',
    0x0809951c: 'DAT_0809951c',
    0x0809954c: 'DAT_0809954c',
    0x08099550: 'DAT_08099550',
    0x08099554: 'DAT_08099554',
    0x08099564: 'DAT_08099564',
    0x0809957c: 'DAT_0809957c',
    0x08099590: 'DAT_08099590',
    0x080995ac: 'DAT_080995ac',
    0x080995e0: 'DAT_080995e0',
    0x080995e4: 'DAT_080995e4',
    0x08099600: 'DAT_08099600',
    0x0809966c: 'DAT_0809966c',
    0x08099670: 'DAT_08099670',
    0x08099674: 'DAT_08099674',
    0x08099718: 'DAT_08099718',
    0x0809971c: 'DAT_0809971c',
    0x08099720: 'DAT_08099720',
    0x08099724: 'DAT_08099724',
    0x08099728: 'DAT_08099728',
    0x08099790: 'DAT_08099790',
    0x08099794: 'DAT_08099794',
    0x08099798: 'DAT_08099798',
    0x0809982c: 'DAT_0809982c',
    0x08099830: 'DAT_08099830',
    0x08099834: 'DAT_08099834',
    0x08099838: 'DAT_08099838',
    0x0809983c: 'PTR_gP1LifePoints_0809983c',
    0x08099840: 'DAT_08099840',
    0x0809985c: 'PTR_gP1LifePoints_0809985c',
    0x08099860: 'DAT_08099860',
    0x08099864: 'DAT_08099864',
    0x08099878: 'PTR_gP1LifePoints_08099878',
    0x0809987c: 'DAT_0809987c',
    0x08099934: 'DAT_08099934',
    0x08099938: 'DAT_08099938',
    0x0809993c: 'DAT_0809993c',
    0x08099940: 'DAT_08099940',
    0x08099944: 'DAT_08099944',
    0x08099974: 'PTR_gP1LifePoints_08099974',
    0x08099978: 'DAT_08099978',
    0x080999d8: 'DAT_080999d8',
    0x080999dc: 'DAT_080999dc',
    0x08099a70: 'DAT_08099a70',
    0x08099a74: 'DAT_08099a74',
    0x08099a78: 'DAT_08099a78',
    0x08099a7c: 'DAT_08099a7c',
    0x08099a80: 'DAT_08099a80',
    0x08099a84: 'DAT_08099a84',
    0x08099a88: 'DAT_08099a88',
    0x08099a8c: 'PTR_gP1LifePoints_08099a8c',
    0x08099a90: 'DAT_08099a90',
    0x08099a94: 'DAT_08099a94',
    0x08099af8: 'DAT_08099af8',
    0x08099afc: 'PTR_gP1LifePoints_08099afc',
    0x08099b00: 'DAT_08099b00',
    0x08099ba8: 'DAT_08099ba8',
    0x08099bac: 'DAT_08099bac',
    0x08099bb0: 'DAT_08099bb0',
    0x08099bb4: 'DAT_08099bb4',
    0x08099bb8: 'DAT_08099bb8',
    0x08099bbc: 'DAT_08099bbc',
    0x08099bdc: 'DAT_08099bdc',
    0x08099be0: 'DAT_08099be0',
    0x08099c34: 'DAT_08099c34',
    0x08099c38: 'DAT_08099c38',
    0x08099c74: 'DAT_08099c74',
    0x08099c78: 'DAT_08099c78',
    0x08099c7c: 'DAT_08099c7c',
    0x08099c88: 'DAT_08099c88',
    0x08099d5c: 'DAT_08099d5c',
    0x08099d60: 'DAT_08099d60',
    0x08099d64: 'DAT_08099d64',
    0x08099d68: 'DAT_08099d68',
    0x08099d6c: 'DAT_08099d6c',
    0x08099d70: 'DAT_08099d70',
    0x08099d74: 'DAT_08099d74',
    0x08099d78: 'DAT_08099d78',
    0x08099d7c: 'DAT_08099d7c',
    0x08099e04: 'PTR_gP1LifePoints_08099e04',
    0x08099e08: 'DAT_08099e08',
    0x08099e54: 'DAT_08099e54',
    0x08099e58: 'PTR_gP1LifePoints_08099e58',
    0x08099e5c: 'DAT_08099e5c',
    0x08099eb0: 'DAT_08099eb0',
    0x08099eb4: 'DAT_08099eb4',
    0x08099eb8: 'PTR_gP1LifePoints_08099eb8',
    0x08099ebc: 'DAT_08099ebc',
    0x08099efc: 'DAT_08099efc',
    0x08099f00: 'DAT_08099f00',
    0x08099f04: 'DAT_08099f04',
    0x08099f10: 'DAT_08099f10',
    0x08099f28: 'DAT_08099f28',
    0x08099f34: 'DAT_08099f34',
    0x08099f68: 'DAT_08099f68',
    0x08099f6c: 'DAT_08099f6c',
    0x08099fec: 'DAT_08099fec',
    0x08099ff0: 'DAT_08099ff0',
    0x08099ff4: 'DAT_08099ff4',
    0x08099ff8: 'DAT_08099ff8',
    0x0809a008: 'DAT_0809a008',
    0x0809a00c: 'DAT_0809a00c',
    0x0809a024: 'DAT_0809a024',
    0x0809a028: 'DAT_0809a028',
    0x0809a03c: 'DAT_0809a03c',
    0x0809a040: 'DAT_0809a040',
    0x0809a07c: 'DAT_0809a07c',
    0x0809a180: 'DAT_0809a180',
    0x0809a184: 'DAT_0809a184',
    0x0809a188: 'DAT_0809a188',
    0x0809a18c: 'DAT_0809a18c',
    0x0809a190: 'DAT_0809a190',
    0x0809a194: 'DAT_0809a194',
    0x0809a198: 'DAT_0809a198',
    0x0809a19c: 'DAT_0809a19c',
    0x0809a1a0: 'DAT_0809a1a0',
}
SWITCH_TARGETS = [0x0809939c, 0x08099520, 0x0809972c, 0x08099844, 0x08099880, 0x08099888, 0x0809997c, 0x08099a98, 0x08099a98, 0x08099a98, 0x080999e0]
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


def preserved_refs(slot, target):
    return sorted((str(r.getFromAddress()), str(r.getToAddress()), r.getOperandIndex(),
                   str(r.getReferenceType()), str(r.getSource()))
                  for r in refMgr.getReferencesFrom(toAddr(slot))
                  if not (r.getOperandIndex() == 0 and r.getToAddress() == toAddr(target)))


def preflight():
    all_slots = [r[0] for r in EQ_SLOTS + REF_SLOTS + RENAME_SLOTS]
    if len(all_slots) != 135 or len(set(all_slots)) != 135:
        fail('SLOT_COVERAGE')
    for slot, value, name, label in EQ_SLOTS + REF_SLOTS:
        _check(slot, value)
        require_name_available(label, slot)
        if not 0x08099314 <= slot < 0x0809a1a4:
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
        if target == 0x08099370:
            matches = [s for s in symTbl.getSymbols(toAddr(target))
                       if s.getSymbolType() == SymbolType.LABEL and
                       s.getName(True).replace('::', '__') == name]
            if len(matches) != 1:
                fail('SWITCH_LABEL_PATTERN 0x08099370')
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
    for i, target in enumerate(SWITCH_TARGETS):
        _check(0x08099370 + i * 4, target)
    print('PREFLIGHT slots=135 EQ=96 REF=27 RENAME=12 PLATE=3 EOL=12 FAIL=%d' % len(FAILS))


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
        if target_symbol is None and target == 0x08099370:
            # Reuse the existing scoped table label; keep its symbol identity.
            candidates = [s for s in symTbl.getSymbols(addr)
                          if s.getSymbolType() == SymbolType.LABEL and
                          s.getName(True).replace('::', '__') == name]
            if len(candidates) != 1:
                raise RuntimeError('SWITCH_LABEL_PATTERN 0x08099370')
            target_symbol = candidates[0]
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
        if preserved_refs(slot, target) != PRESERVED_REFS[slot]:
            fail('POST_PRESERVED_REFS 0x%08x' % slot)
        primary = symTbl.getPrimarySymbol(toAddr(target))
        if (primary is None or primary.getName() != name or
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
    for i, target in enumerate(SWITCH_TARGETS):
        _check(0x08099370 + i * 4, target)


print('=== RefineF12Seg7Slots mode=%s ===' % MODE)
preflight()
if FAILS:
    raise RuntimeError('PREFLIGHT FAIL; no writes performed')
if MODE == 'apply':
    transaction = currentProgram.startTransaction('Refine F12-Seg-7 slots')
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
    COUNTS.update({'EQ': 96, 'REF': 27, 'RENAME': 12, 'PLATE': 3, 'EOL': 12})
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
