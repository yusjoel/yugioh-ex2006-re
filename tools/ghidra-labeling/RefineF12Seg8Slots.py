# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F12-Seg-8 [0x0809a1a4, 0x0809b178): slots and ASCII comments only.
# Proposal SHA256: 2606ce4d5862f3f2e02171a2e22acb7ca869a56e568158a859013f5690307229
# Usage: RefineF12Seg8Slots.py dry|apply|check
# No function renames, disassembly, carve, or memory writes.

from ghidra.program.model.symbol import SourceType, RefType, SymbolType
from ghidra.program.model.listing import CodeUnit

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
DRY = MODE != 'apply'

# BEGIN PROPOSAL TABLES
EQ_SLOTS = [
    (0x0809a204, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9a204'),
    (0x0809a240, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9a240'),
    (0x0809a338, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9a338'),
    (0x0809a340, 0x00001cfc, 'EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF', 'eval_equip_pair_chain_active_from_field_offset_9a340'),
    (0x0809a360, 0x000013a4, 'THUNDER_NYAN_NYAN_CID', 'eval_equip_pair_thunder_nyan_nyan_cid_9a360'),
    (0x0809a3a4, 0x0000146f, 'CATHEDRAL_OF_NOBLES_CID', 'eval_equip_pair_cathedral_of_nobles_cid_9a3a4'),
    (0x0809a3a8, 0x000013a4, 'THUNDER_NYAN_NYAN_CID', 'eval_equip_pair_thunder_nyan_nyan_cid_9a3a8'),
    (0x0809a3dc, 0x0000146f, 'CATHEDRAL_OF_NOBLES_CID', 'eval_equip_pair_cathedral_of_nobles_cid_9a3dc'),
    (0x0809a3e4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eval_equip_pair_chain_active_from_lp_offset_9a3e4'),
    (0x0809a408, 0x000013b0, 'equip_pair_cid_13b0', 'eval_equip_pair_cid_13b0_9a408'),
    (0x0809a41c, 0x000013b4, 'RIGRAS_LEEVER_CID', 'eval_equip_pair_rigras_leever_cid_9a41c'),
    (0x0809a420, 0x00001836, 'EQUIP_ELIG_EXCL_B', 'eval_equip_pair_fox_fire_cid_9a420'),
    (0x0809a47c, 0x00001529, 'GREAT_DEZARD_CID', 'eval_equip_pair_great_dezard_cid_9a47c'),
    (0x0809a480, 0x000012a6, 'SWORD_HUNTER_CID', 'eval_equip_pair_sword_hunter_cid_9a480'),
    (0x0809a494, 0x00001415, 'RED_MOON_BABY_CID', 'eval_equip_pair_red_moon_baby_cid_9a494'),
    (0x0809a4b8, 0x000017d8, 'MYSTIC_SWORDSMAN_LV4_CID', 'eval_equip_pair_mystic_swordsman_lv4_cid_9a4b8'),
    (0x0809a4c8, 0x000017da, 'ARMED_DRAGON_LV5_CID', 'eval_equip_pair_armed_dragon_lv5_cid_9a4c8'),
    (0x0809a5b4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9a5b4'),
    (0x0809a5f8, 0x000017d2, 'HORUS_LV4_CID', 'eval_equip_pair_horus_lv4_cid_9a5f8'),
    (0x0809a5fc, 0x000013b0, 'equip_pair_cid_13b0', 'eval_equip_pair_cid_13b0_9a5fc'),
    (0x0809a610, 0x000013b4, 'RIGRAS_LEEVER_CID', 'eval_equip_pair_rigras_leever_cid_9a610'),
    (0x0809a614, 0x00001836, 'EQUIP_ELIG_EXCL_B', 'eval_equip_pair_fox_fire_cid_9a614'),
    (0x0809a67c, 0x00001529, 'GREAT_DEZARD_CID', 'eval_equip_pair_great_dezard_cid_9a67c'),
    (0x0809a680, 0x000012a6, 'SWORD_HUNTER_CID', 'eval_equip_pair_sword_hunter_cid_9a680'),
    (0x0809a694, 0x00001415, 'RED_MOON_BABY_CID', 'eval_equip_pair_red_moon_baby_cid_9a694'),
    (0x0809a6b8, 0x000017d8, 'MYSTIC_SWORDSMAN_LV4_CID', 'eval_equip_pair_mystic_swordsman_lv4_cid_9a6b8'),
    (0x0809a6c8, 0x000017da, 'ARMED_DRAGON_LV5_CID', 'eval_equip_pair_armed_dragon_lv5_cid_9a6c8'),
    (0x0809a7b4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9a7b4'),
    (0x0809a7e4, 0x000017d2, 'HORUS_LV4_CID', 'eval_equip_pair_horus_lv4_cid_9a7e4'),
    (0x0809a7ec, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eval_equip_pair_chain_active_from_lp_offset_9a7ec'),
    (0x0809a8e0, 0x000001ff, 'EQUIP_PAYLOAD_LOW9_MASK', 'eval_equip_pair_payload_low9_mask_9a8e0'),
    (0x0809a8e4, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'eval_equip_pair_slot_active_bit14_clr_9a8e4'),
    (0x0809a8e8, 0xff87ffff, 'OAM_SPRITE_ATTR_CLR_BITS22_19', 'eval_equip_pair_oam_sprite_attr_clr_bits22_19_9a8e8'),
    (0x0809a8ec, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID', 'eval_equip_pair_dark_magician_of_chaos_cid_9a8ec'),
    (0x0809a8f0, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'eval_equip_pair_banisher_of_the_light_cid_9a8f0'),
    (0x0809a8f4, 0x000015d9, 'DD_CRAZY_BEAST_CID', 'eval_equip_pair_dd_crazy_beast_cid_9a8f4'),
    (0x0809a8f8, 0x0000147a, 'MYSTICAL_BEAST_SERKET_CID', 'eval_equip_pair_mystical_beast_serket_cid_9a8f8'),
    (0x0809a90c, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID', 'eval_equip_pair_dark_magician_of_chaos_cid_9a90c'),
    (0x0809a910, 0x000018e6, 'HOLY_KNIGHT_ISHZARK_CID', 'eval_equip_pair_holy_knight_ishzark_cid_9a910'),
    (0x0809a968, 0x0000174b, 'NEEDLE_BURROWER_CID', 'eval_equip_pair_needle_burrower_cid_9a968'),
    (0x0809a96c, 0x0000147a, 'MYSTICAL_BEAST_SERKET_CID', 'eval_equip_pair_mystical_beast_serket_cid_9a96c'),
    (0x0809a97c, 0x00001592, 'WINGED_SAGE_FALCOS_CID', 'eval_equip_pair_winged_sage_falcos_cid_9a97c'),
    (0x0809a998, 0x00001704, 'INSECT_PRINCESS_CID', 'eval_equip_pair_insect_princess_cid_9a998'),
    (0x0809a9ac, 0x0000170b, 'GUARDIAN_ANGEL_JOAN_CID', 'eval_equip_pair_guardian_angel_joan_cid_9a9ac'),
    (0x0809a9d4, 0x000018c8, 'ELEMENTAL_HERO_FLAME_WINGMAN_CID', 'eval_equip_pair_elemental_hero_flame_wingman_cid_9a9d4'),
    (0x0809a9d8, 0x000017c8, 'SPHINX_TELEIA_CID', 'eval_equip_pair_sphinx_teleia_cid_9a9d8'),
    (0x0809a9e0, 0x000018ae, 'MILLENNIUM_SCORPION_CID', 'eval_equip_pair_millennium_scorpion_cid_9a9e0'),
    (0x0809a9fc, 0x00001987, 'ELEMENTAL_HERO_STEAM_HEALER_CID', 'eval_equip_pair_elemental_hero_steam_healer_cid_9a9fc'),
    (0x0809aa10, 0x000019a4, 'HAMON_LORD_CID', 'eval_equip_pair_hamon_lord_cid_9aa10'),
    (0x0809aae4, 0x2c200000, 'EQUIP_ACTIVATION_PACKED_TYPE22', 'eval_equip_pair_packed_type22_9aae4'),
    (0x0809aaec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9aaec'),
    (0x0809aaf8, 0xffffeb50, 'NODE_POOL_NEG_OFFSET', 'eval_equip_pair_node_pool_to_field_negative_offset_9aaf8'),
    (0x0809ab00, 0x000015d5, 'DES_DENDLE_CID', 'eval_equip_pair_des_dendle_cid_9ab00'),
    (0x0809ab14, 0x000018d0, 'LEGENDARY_BLACK_BELT_CID', 'eval_equip_pair_legendary_black_belt_cid_9ab14'),
    (0x0809ab3c, 0x000015b3, 'Z_METAL_TANK_CID', 'eval_equip_pair_z_metal_tank_cid_9ab3c'),
    (0x0809abd0, 0x2c200000, 'EQUIP_ACTIVATION_PACKED_TYPE22', 'eval_equip_pair_packed_type22_9abd0'),
    (0x0809abd4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9abd4'),
    (0x0809ac98, 0x000001ff, 'EQUIP_PAYLOAD_LOW9_MASK', 'eval_equip_pair_payload_low9_mask_9ac98'),
    (0x0809ac9c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'eval_equip_pair_slot_active_bit14_clr_9ac9c'),
    (0x0809aca0, 0xff87ffff, 'OAM_SPRITE_ATTR_CLR_BITS22_19', 'eval_equip_pair_oam_sprite_attr_clr_bits22_19_9aca0'),
    (0x0809aca4, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID', 'eval_equip_pair_dark_magician_of_chaos_cid_9aca4'),
    (0x0809aca8, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'eval_equip_pair_banisher_of_the_light_cid_9aca8'),
    (0x0809acac, 0x000015d9, 'DD_CRAZY_BEAST_CID', 'eval_equip_pair_dd_crazy_beast_cid_9acac'),
    (0x0809acb0, 0x0000147a, 'MYSTICAL_BEAST_SERKET_CID', 'eval_equip_pair_mystical_beast_serket_cid_9acb0'),
    (0x0809acc4, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID', 'eval_equip_pair_dark_magician_of_chaos_cid_9acc4'),
    (0x0809acc8, 0x000018e6, 'HOLY_KNIGHT_ISHZARK_CID', 'eval_equip_pair_holy_knight_ishzark_cid_9acc8'),
    (0x0809ad1c, 0x0000172b, 'EMES_THE_INFINITY_CID', 'eval_equip_pair_emes_the_infinity_cid_9ad1c'),
    (0x0809ad20, 0x0000147a, 'MYSTICAL_BEAST_SERKET_CID', 'eval_equip_pair_mystical_beast_serket_cid_9ad20'),
    (0x0809ad30, 0x00001592, 'WINGED_SAGE_FALCOS_CID', 'eval_equip_pair_winged_sage_falcos_cid_9ad30'),
    (0x0809ad48, 0x000016c6, 'FENRIR_CID', 'eval_equip_pair_fenrir_cid_9ad48'),
    (0x0809ad58, 0x00001704, 'INSECT_PRINCESS_CID', 'eval_equip_pair_insect_princess_cid_9ad58'),
    (0x0809ad78, 0x000018ae, 'MILLENNIUM_SCORPION_CID', 'eval_equip_pair_millennium_scorpion_cid_9ad78'),
    (0x0809ad7c, 0x00001792, 'ABSORBING_KID_FROM_THE_SKY_CID', 'eval_equip_pair_absorbing_kid_from_the_sky_cid_9ad7c'),
    (0x0809ad90, 0x000017c8, 'SPHINX_TELEIA_CID', 'eval_equip_pair_sphinx_teleia_cid_9ad90'),
    (0x0809ada8, 0x0000194f, 'HYDROGEDDON_CID', 'eval_equip_pair_hydrogeddon_cid_9ada8'),
    (0x0809adc0, 0x000019a4, 'HAMON_LORD_CID', 'eval_equip_pair_hamon_lord_cid_9adc0'),
    (0x0809add0, 0x000019d3, 'DIVINE_DRAGON_EXCELION_CID', 'eval_equip_pair_divine_dragon_excelion_cid_9add0'),
    (0x0809aeac, 0x2c200000, 'EQUIP_ACTIVATION_PACKED_TYPE22', 'eval_equip_pair_packed_type22_9aeac'),
    (0x0809aeb0, 0x0000ffff, 'SPRITE_LOW_HALF_MASK', 'eval_equip_pair_sprite_low_half_mask_9aeb0'),
    (0x0809aeb8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9aeb8'),
    (0x0809aec4, 0xffffeb50, 'NODE_POOL_NEG_OFFSET', 'eval_equip_pair_node_pool_to_field_negative_offset_9aec4'),
    (0x0809aecc, 0x000018d0, 'LEGENDARY_BLACK_BELT_CID', 'eval_equip_pair_legendary_black_belt_cid_9aecc'),
    (0x0809aed0, 0x000015d1, 'cid_15d1_zombie_tiger', 'eval_equip_pair_zombie_tiger_cid_9aed0'),
    (0x0809aee4, 0x0000197c, 'ARMED_CHANGER_CID', 'eval_equip_pair_armed_changer_cid_9aee4'),
    (0x0809af0c, 0x000015b3, 'Z_METAL_TANK_CID', 'eval_equip_pair_z_metal_tank_cid_9af0c'),
    (0x0809b01c, 0x2c200000, 'EQUIP_ACTIVATION_PACKED_TYPE22', 'eval_equip_pair_packed_type22_9b01c'),
    (0x0809b020, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_pair_player_stride_9b020'),
    (0x0809b02c, 0x000015b3, 'Z_METAL_TANK_CID', 'eval_equip_pair_z_metal_tank_cid_9b02c'),
    (0x0809b030, 0x00001658, 'THOUSAND_NEEDLES_CID', 'eval_equip_pair_thousand_needles_cid_9b030'),
    (0x0809b034, 0x0000152c, 'GIANT_AXE_MUMMY_CID', 'eval_equip_pair_giant_axe_mummy_cid_9b034'),
    (0x0809b048, 0x000016b7, 'DES_KANGAROO_CID', 'eval_equip_pair_des_kangaroo_cid_9b048'),
    (0x0809b164, 0x00001493, 'DESTRUCTION_PUNCH_CID', 'eval_equip_pair_destruction_punch_cid_9b164'),
    (0x0809b168, 0x0000162e, 'CONTINUOUS_DESTRUCTION_PUNCH_CID', 'eval_equip_pair_continuous_destruction_punch_cid_9b168'),
    (0x0809b16c, 0x00001883, 'CROSS_COUNTER_CID', 'eval_equip_pair_cross_counter_cid_9b16c'),
    (0x0809b174, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eval_equip_pair_chain_active_from_lp_offset_9b174'),
]

REF_SLOTS = [
    (0x0809a200, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a200'),
    (0x0809a208, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9a208'),
    (0x0809a244, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9a244'),
    (0x0809a330, 0x0201bc68, 'gDuelEffectChainSlotsSecond', 'eval_equip_pair_effect_chain_second_slot_9a330'),
    (0x0809a334, 0x0201bc54, 'gDuelEffectChainSlots', 'eval_equip_pair_effect_chain_slots_base_9a334'),
    (0x0809a33c, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9a33c'),
    (0x0809a4e8, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a4e8'),
    (0x0809a518, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a518'),
    (0x0809a574, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a574'),
    (0x0809a5b0, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a5b0'),
    (0x0809a5b8, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9a5b8'),
    (0x0809a5f4, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a5f4'),
    (0x0809a634, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a634'),
    (0x0809a678, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a678'),
    (0x0809a6e8, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a6e8'),
    (0x0809a718, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a718'),
    (0x0809a774, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a774'),
    (0x0809a7b0, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a7b0'),
    (0x0809a7b8, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9a7b8'),
    (0x0809a7e0, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9a7e0'),
    (0x0809aae8, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9aae8'),
    (0x0809aaf0, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9aaf0'),
    (0x0809aaf4, 0x0201d9c0, 'gEquipNodePool', 'eval_equip_pair_node_pool_base_9aaf4'),
    (0x0809aafc, 0x0201c520, 'gDuelFieldSlotState', 'eval_equip_pair_field_state_base_9aafc'),
    (0x0809abd8, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9abd8'),
    (0x0809aeb4, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9aeb4'),
    (0x0809aebc, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9aebc'),
    (0x0809aec0, 0x0201d9c0, 'gEquipNodePool', 'eval_equip_pair_node_pool_base_9aec0'),
    (0x0809aec8, 0x0201c520, 'gDuelFieldSlotState', 'eval_equip_pair_field_state_base_9aec8'),
    (0x0809b024, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_pair_field_slots_base_9b024'),
    (0x0809b028, 0x0201e1c8, 'gEquipZoneCountTable', 'eval_equip_pair_zone_count_table_base_9b028'),
    (0x0809b058, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9b058'),
    (0x0809b160, 0x0201bb90, 'gEquipChainSlotRefs', 'eval_equip_pair_chain_base_9b160'),
]

RENAME_SLOTS = [
    (0x0809a3e0, 'eval_equip_pair_lp_base_9a3e0', 'gP1LifePoints base; paired offset selects the equip display phase word.'),
    (0x0809a7e8, 'eval_equip_pair_lp_base_9a7e8', 'gP1LifePoints base; paired offset selects the equip display phase word.'),
    (0x0809b170, 'eval_equip_pair_lp_base_9b170', 'gP1LifePoints base; paired offset selects the equip display phase word.'),
]
PLATES = [
    (0x0809a1a4, 'eval_equip_slot_pair_eligibility', 'Ticks paired equip display for r0=player_side with 0x38-byte contexts at gDuelEquipCtx. Phase is [gDuelFieldSlots+EQUIP_CHAIN_ACTIVE_FROM_FIELD_OFF]. Phase 0 sets special-card context flags; phase 1 queues card-specific displays; phase 2 renders descriptors, applies type-22 activations, walks equip nodes, and updates bitmaps. Phases 0..2 increment phase and return 0; nonzero gEquipChainSlotRefs[+8] or other phases return 1. Uses shared return tails and a 0x48-byte local frame.'),
    (0x0809b146, 'increment_counter_at_ptr', 'Shared phase-advance tail of eval_equip_slot_pair_eligibility; requires its existing stack frame. r1 points to [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. Increments that word, sets r0=0, then falls through to restore_callee_high_regs_from_frame to return to the original caller. Entered by BL at 0x0809a3d6/0x0809a7da and fall-through at 0x0809b144. This is not an independent leaf or APCS entry.'),
    (0x0809b14e, 'restore_callee_high_regs_from_frame', "Shared return tail of eval_equip_slot_pair_eligibility. Releases its 0x48-byte local frame, restores r8/r9/r10 and r4-r7, then returns through the saved caller address. Preserves r0. Reached by BL at 0x0809a32c with r0=1 or by fall-through from increment_counter_at_ptr with r0=0. Requires the parent's saved frame; this is not an independent APCS entry."),
]
ORIGINAL_LABELS = {
    0x0809a200: 'DAT_0809a200',
    0x0809a204: 'DAT_0809a204',
    0x0809a208: 'DAT_0809a208',
    0x0809a240: 'DAT_0809a240',
    0x0809a244: 'DAT_0809a244',
    0x0809a330: 'DWORD_0809a330',
    0x0809a334: 'DWORD_0809a334',
    0x0809a338: 'DWORD_0809a338',
    0x0809a33c: 'DWORD_0809a33c',
    0x0809a340: 'DWORD_0809a340',
    0x0809a360: 'DAT_0809a360',
    0x0809a3a4: 'DAT_0809a3a4',
    0x0809a3a8: 'DAT_0809a3a8',
    0x0809a3dc: 'DWORD_0809a3dc',
    0x0809a3e0: 'PTR_gP1LifePoints_0809a3e0',
    0x0809a3e4: 'DWORD_0809a3e4',
    0x0809a408: 'DAT_0809a408',
    0x0809a41c: 'DAT_0809a41c',
    0x0809a420: 'DAT_0809a420',
    0x0809a47c: 'DAT_0809a47c',
    0x0809a480: 'DAT_0809a480',
    0x0809a494: 'DAT_0809a494',
    0x0809a4b8: 'DAT_0809a4b8',
    0x0809a4c8: 'DAT_0809a4c8',
    0x0809a4e8: 'DAT_0809a4e8',
    0x0809a518: 'DAT_0809a518',
    0x0809a574: 'DAT_0809a574',
    0x0809a5b0: 'DAT_0809a5b0',
    0x0809a5b4: 'DAT_0809a5b4',
    0x0809a5b8: 'DAT_0809a5b8',
    0x0809a5f4: 'DAT_0809a5f4',
    0x0809a5f8: 'DAT_0809a5f8',
    0x0809a5fc: 'DAT_0809a5fc',
    0x0809a610: 'DAT_0809a610',
    0x0809a614: 'DAT_0809a614',
    0x0809a634: 'DAT_0809a634',
    0x0809a678: 'DAT_0809a678',
    0x0809a67c: 'DAT_0809a67c',
    0x0809a680: 'DAT_0809a680',
    0x0809a694: 'DAT_0809a694',
    0x0809a6b8: 'DAT_0809a6b8',
    0x0809a6c8: 'DAT_0809a6c8',
    0x0809a6e8: 'DAT_0809a6e8',
    0x0809a718: 'DAT_0809a718',
    0x0809a774: 'DAT_0809a774',
    0x0809a7b0: 'DAT_0809a7b0',
    0x0809a7b4: 'DAT_0809a7b4',
    0x0809a7b8: 'DAT_0809a7b8',
    0x0809a7e0: 'DWORD_0809a7e0',
    0x0809a7e4: 'DWORD_0809a7e4',
    0x0809a7e8: 'PTR_gP1LifePoints_0809a7e8',
    0x0809a7ec: 'DWORD_0809a7ec',
    0x0809a8e0: 'DAT_0809a8e0',
    0x0809a8e4: 'DAT_0809a8e4',
    0x0809a8e8: 'DAT_0809a8e8',
    0x0809a8ec: 'DAT_0809a8ec',
    0x0809a8f0: 'DAT_0809a8f0',
    0x0809a8f4: 'DAT_0809a8f4',
    0x0809a8f8: 'DAT_0809a8f8',
    0x0809a90c: 'DAT_0809a90c',
    0x0809a910: 'DAT_0809a910',
    0x0809a968: 'DAT_0809a968',
    0x0809a96c: 'DAT_0809a96c',
    0x0809a97c: 'DAT_0809a97c',
    0x0809a998: 'DAT_0809a998',
    0x0809a9ac: 'DAT_0809a9ac',
    0x0809a9d4: 'DAT_0809a9d4',
    0x0809a9d8: 'DAT_0809a9d8',
    0x0809a9e0: 'DAT_0809a9e0',
    0x0809a9fc: 'DAT_0809a9fc',
    0x0809aa10: 'DAT_0809aa10',
    0x0809aae4: 'DAT_0809aae4',
    0x0809aae8: 'DAT_0809aae8',
    0x0809aaec: 'DAT_0809aaec',
    0x0809aaf0: 'DAT_0809aaf0',
    0x0809aaf4: 'DAT_0809aaf4',
    0x0809aaf8: 'DAT_0809aaf8',
    0x0809aafc: 'DAT_0809aafc',
    0x0809ab00: 'DAT_0809ab00',
    0x0809ab14: 'DAT_0809ab14',
    0x0809ab3c: 'DAT_0809ab3c',
    0x0809abd0: 'DAT_0809abd0',
    0x0809abd4: 'DAT_0809abd4',
    0x0809abd8: 'DAT_0809abd8',
    0x0809ac98: 'DAT_0809ac98',
    0x0809ac9c: 'DAT_0809ac9c',
    0x0809aca0: 'DAT_0809aca0',
    0x0809aca4: 'DAT_0809aca4',
    0x0809aca8: 'DAT_0809aca8',
    0x0809acac: 'DAT_0809acac',
    0x0809acb0: 'DAT_0809acb0',
    0x0809acc4: 'DAT_0809acc4',
    0x0809acc8: 'DAT_0809acc8',
    0x0809ad1c: 'DAT_0809ad1c',
    0x0809ad20: 'DAT_0809ad20',
    0x0809ad30: 'DAT_0809ad30',
    0x0809ad48: 'DAT_0809ad48',
    0x0809ad58: 'DAT_0809ad58',
    0x0809ad78: 'DAT_0809ad78',
    0x0809ad7c: 'DAT_0809ad7c',
    0x0809ad90: 'DAT_0809ad90',
    0x0809ada8: 'DAT_0809ada8',
    0x0809adc0: 'DAT_0809adc0',
    0x0809add0: 'DAT_0809add0',
    0x0809aeac: 'DAT_0809aeac',
    0x0809aeb0: 'DAT_0809aeb0',
    0x0809aeb4: 'DAT_0809aeb4',
    0x0809aeb8: 'DAT_0809aeb8',
    0x0809aebc: 'DAT_0809aebc',
    0x0809aec0: 'DAT_0809aec0',
    0x0809aec4: 'DAT_0809aec4',
    0x0809aec8: 'DAT_0809aec8',
    0x0809aecc: 'DAT_0809aecc',
    0x0809aed0: 'DAT_0809aed0',
    0x0809aee4: 'DAT_0809aee4',
    0x0809af0c: 'DAT_0809af0c',
    0x0809b01c: 'DAT_0809b01c',
    0x0809b020: 'DAT_0809b020',
    0x0809b024: 'DAT_0809b024',
    0x0809b028: 'DAT_0809b028',
    0x0809b02c: 'DAT_0809b02c',
    0x0809b030: 'DAT_0809b030',
    0x0809b034: 'DAT_0809b034',
    0x0809b048: 'DAT_0809b048',
    0x0809b058: 'DAT_0809b058',
    0x0809b160: 'DAT_0809b160',
    0x0809b164: 'DAT_0809b164',
    0x0809b168: 'DAT_0809b168',
    0x0809b16c: 'DAT_0809b16c',
    0x0809b170: 'PTR_gP1LifePoints_0809b170',
    0x0809b174: 'DAT_0809b174',
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


def preserved_refs(slot, target):
    return sorted((str(r.getFromAddress()), str(r.getToAddress()), r.getOperandIndex(),
                   str(r.getReferenceType()), str(r.getSource()))
                  for r in refMgr.getReferencesFrom(toAddr(slot))
                  if not (r.getOperandIndex() == 0 and r.getToAddress() == toAddr(target)))


def preflight():
    all_slots = [r[0] for r in EQ_SLOTS + REF_SLOTS + RENAME_SLOTS]
    if len(all_slots) != 131 or len(set(all_slots)) != 131:
        fail('SLOT_COVERAGE')
    for slot, value, name, label in EQ_SLOTS + REF_SLOTS:
        _check(slot, value)
        require_name_available(label, slot)
        if not 0x0809a1a4 <= slot < 0x0809b178:
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
    print('PREFLIGHT slots=131 EQ=95 REF=33 RENAME=3 PLATE=3 EOL=3 FAIL=%d' % len(FAILS))


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


print('=== RefineF12Seg8Slots mode=%s ===' % MODE)
preflight()
if FAILS:
    raise RuntimeError('PREFLIGHT FAIL; no writes performed')
if MODE == 'apply':
    transaction = currentProgram.startTransaction('Refine F12-Seg-8 slots')
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
    COUNTS.update({'EQ': 95, 'REF': 33, 'RENAME': 3, 'PLATE': 3, 'EOL': 3})
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
