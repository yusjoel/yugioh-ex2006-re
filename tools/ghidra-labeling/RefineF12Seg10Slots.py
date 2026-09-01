# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F12-Seg-10 [0x0809c3d8, 0x0809d718): slots and ASCII comments only.
# Proposal SHA256: 101400c177f1b1f44cbad8a74d97d0b462341f64d61f050fa3f8fb63598372cb
# Usage: RefineF12Seg10Slots.py dry|apply|check
# Three exact function renames; no disassembly, carve, or memory writes.

import hashlib

from ghidra.program.model.symbol import SourceType, RefType, SymbolType
from ghidra.program.model.listing import CodeUnit

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
DRY = MODE != 'apply'

# BEGIN PROPOSAL TABLES
EQ_SLOTS = [
    (0x0809c46c, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_monsters_by_player_cursor_from_lp_offset_9c46c'),
    (0x0809c470, 0x0000ffff, 'EQUIP_ACTIVATION_CID_U16_MASK', 'scan_monsters_by_player_cid_u16_mask_9c470'),
    (0x0809c474, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_monsters_by_player_player_stride_9c474'),
    (0x0809c530, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_all_monsters_cursor_from_lp_offset_9c530'),
    (0x0809c534, 0x0000ffff, 'EQUIP_ACTIVATION_CID_U16_MASK', 'scan_all_monsters_cid_u16_mask_9c534'),
    (0x0809c538, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_all_monsters_player_stride_9c538'),
    (0x0809c5f0, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_spell_traps_by_player_cursor_from_lp_offset_9c5f0'),
    (0x0809c5f4, 0x0000ffff, 'EQUIP_ACTIVATION_CID_U16_MASK', 'scan_spell_traps_by_player_cid_u16_mask_9c5f4'),
    (0x0809c5f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_spell_traps_by_player_player_stride_9c5f8'),
    (0x0809c6bc, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_all_spell_traps_cursor_from_lp_offset_9c6bc'),
    (0x0809c6c0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'scan_all_spell_traps_current_player_from_lp_offset_9c6c0'),
    (0x0809c6c4, 0x0000ffff, 'EQUIP_ACTIVATION_CID_U16_MASK', 'scan_all_spell_traps_cid_u16_mask_9c6c4'),
    (0x0809c6c8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_all_spell_traps_player_stride_9c6c8'),
    (0x0809c730, 0x0000ffff, 'EQUIP_ACTIVATION_CID_U16_MASK', 'scan_chain_by_card_cid_u16_mask_9c730'),
    (0x0809c734, 0x0a4e0000, 'EQUIP_ACTIVATION_TYPE5_ZONE_E_BASE', 'scan_chain_by_card_equip_activation_type5_zone_e_base_9c734'),
    (0x0809c758, 0x00001756, 'SOLAR_FLARE_DRAGON_CID', 'scan_monster_zone_slots_for_equip_activation_solar_flare_dragon_cid_9c758'),
    (0x0809c778, 0x00001835, 'GAIA_SOUL_CID', 'scan_all_monster_zone_slots_for_equip_activation_gaia_soul_cid_9c778'),
    (0x0809c798, 0x00001643, 'MIRAGE_KNIGHT_CID', 'scan_all_monster_zone_slots_for_equip_activation_mirage_knight_cid_9c798'),
    (0x0809c7a8, 0x000017bc, 'CRUSH_D_GANDRA_CID', 'scan_all_monster_zone_slots_for_equip_activation_crush_d_gandra_cid_9c7a8'),
    (0x0809c814, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_monster_cid_table_cursor_from_lp_offset_9c814'),
    (0x0809c818, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'scan_monster_cid_table_current_player_from_lp_offset_9c818'),
    (0x0809c81c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_monster_cid_table_player_stride_9c81c'),
    (0x0809c820, 0xffffe82e, 'EQUIP_SCAN_CID_TABLE_NEG_BASE', 'scan_monster_cid_table_equip_scan_cid_table_neg_base_9c820'),
    (0x0809c89c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_monster_cid_table_player_stride_9c89c'),
    (0x0809c8a4, 0x00001cf4, 'FIELD_STATE_OFF', 'scan_monster_cid_table_cursor_from_field_offset_9c8a4'),
    (0x0809c8c8, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_monster_cid_table_cursor_from_lp_offset_9c8c8'),
    (0x0809c908, 0x000015b8, 'INTERDIMENSIONAL_MATTER_TRANSPORTER_CID', 'scan_transporter_chain_cid_9c908'),
    (0x0809c90c, 0x0a5015b8, 'INTERDIMENSIONAL_TRANSPORTER_ACTIVATION_PACKED', 'scan_transporter_chain_interdimensional_transporter_activation_packed_9c90c'),
    (0x0809c960, 0x000016b9, 'STRIKE_NINJA_CID', 'scan_strike_ninja_chain_cid_9c960'),
    (0x0809c964, 0x0a4f16b9, 'STRIKE_NINJA_ACTIVATION_PACKED', 'scan_strike_ninja_chain_strike_ninja_activation_packed_9c964'),
    (0x0809ca00, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_f_scout_plane_player_stride_9ca00'),
    (0x0809ca08, 0x00301fff, 'DD_SCOUT_PLANE_SLOT_MATCH_MASK', 'scan_zone_f_scout_plane_dd_scout_plane_slot_match_mask_9ca08'),
    (0x0809ca0c, 0x000016be, 'DD_SCOUT_PLANE_CID', 'scan_zone_f_scout_plane_cid_9ca0c'),
    (0x0809ca10, 0x0a4f0000, 'EQUIP_ACTIVATION_TYPE5_ZONE_F_BASE', 'scan_zone_f_scout_plane_equip_activation_type5_zone_f_base_9ca10'),
    (0x0809ca64, 0x000018bc, 'DD_SURVIVOR_CID', 'scan_dd_survivor_chain_cid_9ca64'),
    (0x0809ca68, 0x014f18bc, 'DD_SURVIVOR_PACKED_OTHER_SIDE', 'scan_dd_survivor_chain_dd_survivor_packed_other_side_9ca68'),
    (0x0809ca8c, 0x004f18bc, 'DD_SURVIVOR_PACKED_SAME_SIDE', 'scan_dd_survivor_chain_dd_survivor_packed_same_side_9ca8c'),
    (0x0809ca90, 0x000018bc, 'DD_SURVIVOR_CID', 'scan_dd_survivor_chain_cid_9ca90'),
    (0x0809cab0, 0x000011cf, 'get_card_lp_cost_by_id_cid_11cf', 'scan_monster_zone_slots_for_equip_activation_reserved_icid_d_cid_9cab0'),
    (0x0809cac0, 0x000012ac, 'SATELLITE_CANNON_CID', 'scan_monster_zone_slots_for_equip_activation_satellite_cannon_cid_9cac0'),
    (0x0809cad0, 0x00001644, 'BERSERK_DRAGON_CID', 'scan_monster_zone_slots_for_equip_activation_berserk_dragon_cid_9cad0'),
    (0x0809cae0, 0x00001911, 'CYBER_ARCHFIEND_CID', 'scan_monster_zone_slots_for_equip_activation_cyber_archfiend_cid_9cae0'),
    (0x0809cb54, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_wicked_worm_beast_cursor_from_lp_offset_9cb54'),
    (0x0809cb58, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_wicked_worm_beast_player_stride_9cb58'),
    (0x0809cb5c, 0x00000fbd, 'WICKED_WORM_BEAST_CID', 'scan_wicked_worm_beast_cid_9cb5c'),
    (0x0809cb94, 0x0000150e, 'SPIRITUAL_ENERGY_SETTLE_CID', 'scan_spiritual_energy_cid_9cb94'),
    (0x0809cc54, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_spiritual_energy_player_stride_9cc54'),
    (0x0809ccf0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_field_cid_range_player_stride_9ccf0'),
    (0x0809ccf8, 0x00001388, 'EQUIP_SLOT_CARD_ID_RANGE_MAX', 'scan_field_cid_range_equip_slot_card_id_range_max_9ccf8'),
    (0x0809cdb0, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_magical_scientist_chain_cursor_from_lp_offset_9cdb0'),
    (0x0809cdb4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_magical_scientist_chain_player_stride_9cdb4'),
    (0x0809cdb8, 0x00001619, 'MAGICAL_SCIENTIST_CID', 'scan_magical_scientist_chain_cid_9cdb8'),
    (0x0809ce60, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_chain_sprite_cursor_from_lp_offset_9ce60'),
    (0x0809ce64, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_chain_sprite_player_stride_9ce64'),
    (0x0809ce8c, 0x00001409, 'LIMITER_REMOVAL_CID', 'scan_all_zone_slots_for_equip_chain_sprite_limiter_removal_cid_9ce8c'),
    (0x0809ce9c, 0x00001337, 'KARATE_MAN_CID', 'scan_all_zone_slots_for_equip_chain_sprite_karate_man_cid_9ce9c'),
    (0x0809ceac, 0x000016ce, 'WILD_NATURES_RELEASE_CID', 'scan_all_zone_slots_for_equip_chain_sprite_wild_natures_release_cid_9ceac'),
    (0x0809ced4, 0x0000148e, 'ROYAL_COMMAND_CID', 'scan_summoner_illusions_chain_cid_9ced4'),
    (0x0809ced8, 0x000014da, 'FIEND_SKULL_DRAGON_CID', 'scan_summoner_illusions_chain_cid_9ced8'),
    (0x0809cedc, 0x00001481, 'SUMMONER_OF_ILLUSIONS_CID', 'scan_summoner_illusions_chain_cid_9cedc'),
    (0x0809cef4, 0x000016a4, 'EQUIP_LOCK_A_CID', 'scan_all_zone_slots_for_equip_chain_sprite_archfiends_roar_cid_9cef4'),
    (0x0809cf04, 0x00001876, 'RESCUE_CAT_CID', 'scan_all_zone_slots_for_equip_chain_sprite_rescue_cat_cid_9cf04'),
    (0x0809cfa0, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_return_from_dd_chain_cursor_from_lp_offset_9cfa0'),
    (0x0809cfa4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_return_from_dd_chain_player_stride_9cfa4'),
    (0x0809cfa8, 0x000017be, 'RETURN_FROM_DD_CID', 'scan_return_from_dd_chain_cid_9cfa8'),
    (0x0809d0a0, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_infinite_dismissal_cursor_from_lp_offset_9d0a0'),
    (0x0809d0a4, 0x000013f8, 'INFINITE_DISMISSAL_CID', 'scan_infinite_dismissal_cid_9d0a4'),
    (0x0809d0a8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_infinite_dismissal_player_stride_9d0a8'),
    (0x0809d15c, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_chain_bitmap_cards_cursor_from_lp_offset_9d15c'),
    (0x0809d194, 0x00001468, 'DESTINY_BOARD_CID', 'scan_spell_trap_zone_for_equip_activation_destiny_board_cid_9d194'),
    (0x0809d1c0, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID', 'scan_spell_trap_zone_for_equip_activation_first_sarcophagus_cid_9d1c0'),
    (0x0809d1d8, 0x00001487, 'GARUDA_THE_WIND_SPIRIT_CID', 'scan_monster_zone_for_equip_activation_garuda_opponent_cid_9d1d8'),
    (0x0809d1f4, 0x000013f5, 'RETURN_OF_THE_DOOMED_CID', 'scan_return_doomed_chain_cid_9d1f4'),
    (0x0809d21c, 0x0a5013f5, 'RETURN_OF_THE_DOOMED_ACTIVATION_PACKED', 'scan_return_doomed_chain_return_of_the_doomed_activation_packed_9d21c'),
    (0x0809d300, 0x00001379, 'GRAVEROBBER_CID', 'scan_graverobber_cid_9d300'),
    (0x0809d304, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_graverobber_player_stride_9d304'),
    (0x0809d330, 0x00001466, 'DARK_NECROFEAR_CID', 'scan_equip_zone_for_dark_necrofear_activation_cid_9d330'),
    (0x0809d340, 0x000016f9, 'MANTICORE_OF_DARKNESS_CID', 'scan_equip_zone_for_manticore_of_darkness_activation_cid_9d340'),
    (0x0809d350, 0x00001836, 'EQUIP_ELIG_EXCL_B', 'scan_equip_zone_for_fox_fire_activation_cid_9d350'),
    (0x0809d360, 0x000019f7, 'HELIOS_DUO_MEGISTE_CID', 'scan_equip_zone_for_helios_duo_megiste_activation_cid_9d360'),
    (0x0809d370, 0x000019f8, 'HELIOS_TRIS_MEGISTE_CID', 'scan_equip_zone_for_helios_tris_megiste_activation_cid_9d370'),
    (0x0809d408, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_super_rejuvenation_cursor_from_lp_offset_9d408'),
    (0x0809d40c, 0x000014e2, 'SUPER_REJUVENATION_CID', 'scan_super_rejuvenation_cid_9d40c'),
    (0x0809d410, 0x0000178b, 'PROTECTOR_OF_THE_SANCTUARY_CID', 'scan_super_rejuvenation_cid_9d410'),
    (0x0809d414, 0x0a5014e2, 'SUPER_REJUVENATION_ACTIVATION_PACKED', 'scan_super_rejuvenation_super_rejuvenation_activation_packed_9d414'),
    (0x0809d498, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_twin_headed_behemoth_cursor_from_lp_offset_9d498'),
    (0x0809d49c, 0x000013a6, 'TWIN_HEADED_BEHEMOTH_CID', 'scan_twin_headed_behemoth_cid_9d49c'),
    (0x0809d4a0, 0x0a4e13a6, 'TWIN_HEADED_BEHEMOTH_ACTIVATION_PACKED', 'scan_twin_headed_behemoth_twin_headed_behemoth_activation_packed_9d4a0'),
    (0x0809d4c8, 0x000017b2, 'HUMAN_WAVE_TACTICS_CID', 'scan_spell_trap_zone_slots_for_equip_activation_human_wave_tactics_cid_9d4c8'),
    (0x0809d4d8, 0x000012a3, 'LITTLE_WINGUARD_CID', 'scan_monster_zone_slots_for_equip_activation_little_winguard_cid_9d4d8'),
    (0x0809d4e8, 0x000012dc, 'ECTOPLASMER_CID', 'scan_spell_trap_zone_slots_for_equip_activation_ectoplasmer_cid_9d4e8'),
    (0x0809d4f8, 0x000017b6, 'LABYRINTH_OF_NIGHTMARE_CID', 'scan_spell_trap_zone_slots_for_equip_activation_labyrinth_of_nightmare_cid_9d4f8'),
    (0x0809d508, 0x00001972, 'BOSS_RUSH_CID', 'scan_spell_trap_zone_slots_for_equip_activation_boss_rush_cid_9d508'),
    (0x0809d518, 0x00001802, 'GREED_CID', 'scan_spell_trap_zone_slots_for_equip_activation_greed_cid_9d518'),
    (0x0809d5cc, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_two_man_cell_battle_cursor_from_lp_offset_9d5cc'),
    (0x0809d5d0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_two_man_cell_battle_player_stride_9d5d0'),
    (0x0809d5d4, 0x000017f8, 'TWO_MAN_CELL_BATTLE_CID', 'scan_two_man_cell_battle_cid_9d5d4'),
    (0x0809d674, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_name_display_candidates_cursor_from_lp_offset_9d674'),
    (0x0809d714, 0x00001d24, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_name_display_candidates_cursor_from_lp_offset_9d714'),
]

REF_SLOTS = [
    (0x0809c824, 0x0809c828, 'switchD_0809c80c__switchdataD_0809c828', 'scan_monster_cid_table_cid_switch_table_9c824'),
    (0x0809c8a0, 0x0201c510, 'gDuelFieldSlots', 'scan_monster_cid_table_field_base_9c8a0'),
    (0x0809c9fc, 0x0201c4fc, 'gP1AltHandCountBase', 'scan_zone_f_scout_plane_zone_f_count_base_9c9fc'),
    (0x0809ca04, 0x0201cab0, 'gP1AltHandSlotArray', 'scan_zone_f_scout_plane_zone_f_word_array_9ca04'),
    (0x0809cc50, 0x0201c510, 'gDuelFieldSlots', 'scan_spiritual_energy_field_base_9cc50'),
    (0x0809ccec, 0x0201c510, 'gDuelFieldSlots', 'scan_field_cid_range_field_base_9ccec'),
    (0x0809ccf4, 0x0201c520, 'gDuelFieldSlotState', 'scan_field_cid_range_field_state_base_9ccf4'),
    (0x0809d0ac, 0x0201c520, 'gDuelFieldSlotState', 'scan_infinite_dismissal_field_state_base_9d0ac'),
    (0x0809d0b0, 0x0201c510, 'gDuelFieldSlots', 'scan_infinite_dismissal_field_base_9d0b0'),
    (0x0809d160, 0x09e47680, 'equip_chain_bitmap_cid_table', 'scan_chain_bitmap_cards_cid_table_9d160'),
    (0x0809d2fc, 0x0201c4ec, 'gP1ZoneHandCount', 'scan_graverobber_zone_b_count_base_9d2fc'),
    (0x0809d308, 0x0201c600, 'gP1FieldArrayCBase', 'scan_graverobber_zone_b_word_array_9d308'),
    (0x0809d30c, 0x0201c510, 'gDuelFieldSlots', 'scan_graverobber_field_base_9d30c'),
    (0x0809d678, 0x09e47688, 'equip_name_display_candidate_table', 'scan_name_display_candidates_candidate_table_9d678'),
    (0x0809d67c, 0x0201e2a0, 'gDuelCardCtxBase', 'scan_name_display_candidates_display_ctx_base_9d67c'),
    (0x0809d690, 0x0201e220, 'gEquipLpActivBitmap', 'scan_name_display_candidates_activation_flag_ptr_9d690'),
    (0x0809d6cc, 0x09e47688, 'equip_name_display_candidate_table', 'scan_name_display_candidates_candidate_table_9d6cc'),
    (0x0809d70c, 0x09e47688, 'equip_name_display_candidate_table', 'scan_name_display_candidates_candidate_table_9d70c'),
]

RENAME_SLOTS = [
    (0x0809c468, 'scan_monsters_by_player_lp_base_9c468', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c494, 'scan_monsters_by_player_lp_base_9c494', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c52c, 'scan_all_monsters_lp_base_9c52c', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c558, 'scan_all_monsters_lp_base_9c558', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c5ec, 'scan_spell_traps_by_player_lp_base_9c5ec', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c618, 'scan_spell_traps_by_player_lp_base_9c618', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c6b8, 'scan_all_spell_traps_lp_base_9c6b8', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809c810, 'scan_monster_cid_table_lp_base_9c810', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809cb50, 'scan_wicked_worm_beast_lp_base_9cb50', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809cdac, 'scan_magical_scientist_chain_lp_base_9cdac', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809ce5c, 'scan_chain_sprite_lp_base_9ce5c', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809cf9c, 'scan_return_from_dd_chain_lp_base_9cf9c', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d09c, 'scan_infinite_dismissal_lp_base_9d09c', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d158, 'scan_chain_bitmap_cards_lp_base_9d158', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d404, 'scan_super_rejuvenation_lp_base_9d404', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d494, 'scan_twin_headed_behemoth_lp_base_9d494', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d5c8, 'scan_two_man_cell_battle_lp_base_9d5c8', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d670, 'scan_name_display_candidates_lp_base_9d670', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
    (0x0809d710, 'scan_name_display_candidates_lp_base_9d710', 'gP1LifePoints base for the shared activation scan cursor and player fields.'),
]

EXTRA_EOL = [
    (0x0809c820, 'Add -0x17d2 to CID; indices 0,1,5,6,8 enter the matching case.'),
    (0x0809c8a4, 'gDuelFieldSlots+0x1cf4 = gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF; same cursor, not a second counter.'),
]

PLATES = [
    (0x0809c3d8, 'scan_monster_zone_slots_for_equip_activation_by_player', 'r0=player_side; r1=CID. Resume the shared cursor at gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF over monster slots 0..4. For each test_slot_has_active_card match, build type5/mode1 packed attributes from the player, slot, CID low16 and slot entity reference, then apply activation. Advance the cursor on every tested slot. Return 0 after the first successful activation, or 1 when cursor>4. Field slots use player*0x868 and 0x14-byte entries.'),
    (0x0809c498, 'scan_all_monster_zone_slots_for_equip_activation_by_card', 'r0=starting_player; r1=CID. Resume cursor 0..9 at gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF. Decode side=starting_player^(cursor/5), monster slot=cursor%5. Test the card, pack type5/mode1 attributes with CID low16 and the slot entity reference, then apply activation. Cursor advances on misses, failed activations and success. Return 0 after one successful activation; return 1 after all ten positions are exhausted.'),
    (0x0809c55c, 'scan_spell_trap_zone_for_equip_activation_by_player_and_card', 'r0=player_side; r1=CID. Resume cursor 0..4 at gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF, selecting spell/trap slot=cursor+5. On a card match, pack type5/mode1 attributes and the field-slot entity reference, then apply activation. Advance cursor for every tested slot; return 0 after one successful activation or 1 after exhaustion. Uses gP1LifePoints+0x30 as field base, with player stride 0x868 and slot stride 0x14.'),
    (0x0809c61c, 'scan_spell_trap_zone_slots_for_equip_activation_by_card', 'r0=CID, saved in r7; no player input. Resume the shared cursor 0..9. Read starting player from gP1LifePoints+P1LP_BLOCK2_OFF_1CE8; side=starting_player^(cursor/5), spell/trap slot=cursor%5+5. On a matching card, pack type5/mode1 attributes and slot entity reference, then apply activation. Advance cursor after each tested slot. Return 0 after one successful activation, or 1 when cursor>9.'),
    (0x0809c6e8, 'scan_equip_zone_for_activation_by_card', 'r0=starting_player; r1=CID. Try zone 0xb on starting_player then starting_player^1 via get_node_entity_id_in_slot. A positive node value supplies its low16 as the entity argument; pack TYPE5_ZONE_E_BASE with CID low16 and side bit31, call activation, then enqueue the zone sprite regardless of activation result. Return 0 after the first positive node. Return 1 when neither side has a positive node. No shared cursor.'),
    (0x0809c74c, 'scan_monster_zone_slots_for_equip_activation_solar_flare_dragon', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(player_side,0x1756) for Solar Flare Dragon and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809c75c, 'scan_all_monster_zone_slots_for_equip_activation_insect_queen', 'r0=player_side. Call scan_all_monster_zone_slots_for_equip_activation_by_card(player_side,0x12a0) for Insect Queen and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809c76c, 'scan_all_monster_zone_slots_for_equip_activation_gaia_soul', 'r0=player_side. Call scan_all_monster_zone_slots_for_equip_activation_by_card(player_side,0x1835) for Gaia Soul the Combustible Collective and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809c77c, 'scan_all_monster_zone_slots_for_equip_activation_dd_guide', 'r0=player_side. Call scan_all_monster_zone_slots_for_equip_activation_by_card(player_side,0x19c0) for D.D. Guide and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809c78c, 'scan_all_monster_zone_slots_for_equip_activation_mirage_knight', 'r0=player_side. Call scan_all_monster_zone_slots_for_equip_activation_by_card(player_side,0x1643) for Mirage Knight and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809c79c, 'scan_all_monster_zone_slots_for_equip_activation_crush_d_gandra', 'r0=player_side. Call scan_all_monster_zone_slots_for_equip_activation_by_card(player_side,0x17bc) for Crush D. Gandra and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809c7ac, 'scan_monster_zone_slots_for_equip_activation_by_cid_table', 'Input registers unused. Resume shared cursor 0..9; side=current_player^(cursor/5), monster slot=cursor%5. Switch on CID-0x17d2; accept indices 0,1,5,6,8 only, and require slot+8 halfword nonzero. Build type5/mode1 packed activation input from the slot and call activation; advance cursor and return 0 regardless of its result. Other slots advance and continue; cursor>9 returns 1. Field base+0x1cf4 and LP base+0x1d24 address the same cursor.'),
    (0x0809c8cc, 'scan_equip_zone_for_interdimensional_matter_transporter', 'r0=starting_player. Try zone 0xb on each side for Interdimensional Matter Transporter. A nonnegative node result triggers activation with player bit31|INTERDIMENSIONAL_TRANSPORTER_ACTIVATION_PACKED and entity=0. If activation returns 0, enqueue the zone sprite. Return 0 after the first node found, regardless of activation result; return 1 if both lookups are negative. No shared cursor.'),
    (0x0809c920, 'scan_equip_zone_for_strike_ninja_activation', 'r0=starting_player. Try each side zone 0xb for Strike Ninja. A nonnegative node value triggers STRIKE_NINJA_ACTIVATION_PACKED|side<<31, with entity argument=(node_value>>2)&0xffff. Enqueue the zone sprite only if activation returns 0. Return 0 after the first node found; return 1 when both lookups are negative. The entity conversion is not a plain low16 copy. No shared cursor.'),
    (0x0809c978, 'scan_zone_f_for_equip_activation_dd_scout_plane', 'r0=starting_player, saved in r9. For each side, scan zone-f word entries backward from [gP1AltHandCountBase+side*0x868]-1, using gP1AltHandSlotArray. Require (word&DD_SCOUT_PLANE_SLOT_MATCH_MASK)==DD_SCOUT_PLANE_CID and get_zone_card_attribute_by_type(side,0xf,index)!=0. Pack TYPE5_ZONE_F_BASE with CID/player and decoded entity; return 0 on successful activation. Failed candidates continue; return 1 after both lists. No monster-field scan or shared cursor.'),
    (0x0809ca34, 'scan_equip_slot_for_dd_survivor_activation', 'r0=starting_player. Try each side zone 0xb for a positive D.D. Survivor node. Derive entity side from node bit0, choose SAME_SIDE or OTHER_SIDE packed base by comparing it with scanned side, then OR type5 and entity-side bit31. Pass node low16 to activation and enqueue the scanned zone sprite, regardless of activation result. Return 0 after the first positive node, otherwise 1 after both sides. No shared cursor.'),
    (0x0809caa4, 'scan_monster_zone_slots_for_equip_activation_reserved_icid_d', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(player_side,0x11cf) for unmapped CID 0x11cf and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809cab4, 'scan_monster_zone_slots_for_equip_activation_satellite_cannon', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(player_side,0x12ac) for Satellite Cannon and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809cac4, 'scan_monster_zone_slots_for_equip_activation_berserk_dragon', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(player_side,0x1644) for Berserk Dragon and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809cad4, 'scan_monster_zone_slots_for_equip_activation_cyber_archfiend', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(player_side,0x1911) for Cyber Archfiend and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809cae4, 'scan_monster_zone_for_equip_sprite_and_bitmap_wicked_worm_beast', 'r0=player_side. Resume shared cursor over monster slots 0..4 and test WICKED_WORM_BEAST_CID. On a match, decode the slot entity reference, enqueue its card sprite and call query_equip_zone_slot_target_bit(player,slot,0,0); then cursor++ and return 0. Misses advance and continue. Return 1 after cursor>4. Field records use gP1LifePoints+0x30, player stride 0x868 and record stride 0x14.'),
    (0x0809cb78, 'scan_monster_zone_for_equip_activation_spiritual_energy_settle_machine', 'r0=starting_player. If any Spiritual Energy Settle Machine field copy exists, return 1 immediately. Otherwise scan both sides monster slots 0..4. Require check_card_stat_field8_is_7 plus the slot state/halfword gates; pack the actual slot CID, player, slot and entity and call activation. Return 0 after the first qualifying slot regardless of activation result, or 1 after no match. No shared scan cursor.'),
    (0x0809cc58, 'scan_field_slots_for_equip_bitmap_update_by_card_range', 'r0=starting_player. Scan both sides monster slots 0..4 using paired gDuelFieldSlots and gDuelFieldSlotState records. Require state bit3 and the halfword/state gates, then CID in inclusive range 0x1386..EQUIP_SLOT_CARD_ID_RANGE_MAX(0x1388). On the first match, enqueue the decoded entity sprite and prepare_equip_slot_ctx_for_bitmap_update(player,slot,0,0); return 0. Return 1 when all slots are exhausted. No shared cursor.'),
    (0x0809cd24, 'scan_all_zone_slots_for_equip_chain_sprite_magical_scientist', 'r0=starting_player. Resume shared cursor 0..9, decoding side=starting_player^(cursor/5), monster slot=cursor%5. Require a nonempty field slot and Magical Scientist in its chain. Call query_equip_zone_slot_target_bit(player,slot,0,MAGICAL_SCIENTIST_CID); enqueue the chain sprite only when it returns 0. Advance cursor and return 0 after one matching chain, regardless of bitmap result. Misses continue; exhaustion returns 1.'),
    (0x0809cdd4, 'scan_all_zone_slots_for_equip_chain_sprite_update', 'r0=starting_player; r1=CID. Resume shared cursor 0..9 across both sides monster slots 0..4. For a nonempty slot containing the requested chain CID, call enqueue_equip_slot_bitmap_update(player,slot,0,0); if it returns 0, enqueue the chain sprite with flag1. Advance cursor and return 0 after one matching chain. Misses advance and continue; cursor>9 returns 1. Side order is starting_player^(cursor/5).'),
    (0x0809ce80, 'scan_all_zone_slots_for_equip_chain_sprite_limiter_removal', 'r0=player_side. Call scan_all_zone_slots_for_equip_chain_sprite_update(player_side,0x1409) for Limiter Removal and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809ce90, 'scan_all_zone_slots_for_equip_chain_sprite_karate_man', 'r0=player_side. Call scan_all_zone_slots_for_equip_chain_sprite_update(player_side,0x1337) for Karate Man and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809cea0, 'scan_all_zone_slots_for_equip_chain_sprite_wild_natures_release', "r0=player_side. Call scan_all_zone_slots_for_equip_chain_sprite_update(player_side,0x16ce) for Wild Nature's Release and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee."),
    (0x0809ceb0, 'scan_all_zone_slots_for_equip_chain_sprite_summoner_of_illusions', 'r0=starting_player. Return 1 if Royal Command or Fiend Skull Dragon has any field copies. Otherwise call scan_all_zone_slots_for_equip_chain_sprite_update(starting_player,SUMMONER_OF_ILLUSIONS_CID), forwarding its result. The shared scan cursor is managed by that callee; this guard does not change it.'),
    (0x0809cee8, 'scan_all_zone_slots_for_equip_chain_sprite_archfiends_roar', "r0=player_side. Call scan_all_zone_slots_for_equip_chain_sprite_update(player_side,0x16a4) for Archfiend's Roar and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee."),
    (0x0809cef8, 'scan_all_zone_slots_for_equip_chain_sprite_rescue_cat', 'r0=player_side. Call scan_all_zone_slots_for_equip_chain_sprite_update(player_side,0x1876) for Rescue Cat and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809cf08, 'scan_all_zone_slots_for_return_from_different_dimension_equip', 'r0=starting_player. Resume shared cursor 0..9 across both sides monster slots. Require a nonempty slot, Return from the Different Dimension in its chain, and check_slot_fieldspell_eligible_by_side(player,slot,0)==0. Query the target bitmap; enqueue the chain sprite only if the bitmap is zero. Advance cursor and return 0 after this work. Misses advance and continue; exhaustion returns 1.'),
    (0x0809cfc4, 'scan_equip_zone_for_infinite_dismissal_activation', 'r0=starting_player. Return 1 if the shared cursor is nonzero or Infinite Dismissal has no field copies. Scan both players monster slots 0..4, collecting bits for nonempty slots with nonzero +8 halfword, chain score<=3 and state gates. If bitmap is empty, return 1. Select starting player or its opponent by available-effect-zone count, enqueue the card display and bitmap context, increment cursor, return 0.'),
    (0x0809d0c8, 'scan_equip_zone_chain_for_sprite_and_bitmap_update', 'r0=player_side. Resume shared cursor over the two u32 CIDs in equip_chain_bitmap_cid_table. Require that CID in zone 0xb chain. Build a cleared 0x18-byte local record containing CID and player, then query_equip_zone_bitmap_with_effect_guard. On nonzero bitmap, enqueue zone sprite and bitmap context, cursor++, return 0. Misses advance and continue; cursor>1 returns 1. Table entries are CIDs, not pointers or slot descriptors.'),
    (0x0809d180, 'scan_spell_trap_zone_for_equip_activation_destiny_board', 'r0=player_side. Call scan_spell_trap_zone_for_equip_activation_by_player_and_card(1-player_side,0x1468) for Destiny Board and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d198, 'scan_spell_trap_zone_for_equip_activation_bottomless_shifting_sand', 'r0=player_side. Call scan_spell_trap_zone_for_equip_activation_by_player_and_card(1-player_side,0x1540) for Bottomless Shifting Sand and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d1ac, 'scan_spell_trap_zone_for_equip_activation_first_sarcophagus', 'r0=player_side. Call scan_spell_trap_zone_for_equip_activation_by_player_and_card(1-player_side,0x17af) for The First Sarcophagus and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d1c4, 'scan_monster_zone_for_equip_activation_garuda_opponent', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(1-player_side,0x1487) for Garuda the Wind Spirit and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d1dc, 'scan_equip_zone_for_return_of_the_doomed_activation', 'r0=player_side. Return 1 unless Return of the Doomed is present in zone 0xb chain. On presence, call activation with RETURN_OF_THE_DOOMED_ACTIVATION_PACKED|player<<31 and entity=0, enqueue that chain sprite with flag0, then return 0 regardless of activation result. No shared scan cursor.'),
    (0x0809d220, 'scan_equip_chain_and_slots_for_graverobber_sprite', 'r0=starting_player. Try each side for Graverobber in zone 0xb chain. On the first chain found, scan its zone-b word array backward using gP1ZoneHandCount/gP1FieldArrayCBase, then field slots 5..10 with zero +8 halfword. Match decoded entity references via find_effect_node_in_zone; enqueue matching card/bitmap work. Finally enqueue the Graverobber chain sprite with flag1 and return 0. Return 1 if neither side has the chain. No shared cursor.'),
    (0x0809d324, 'scan_equip_zone_for_dark_necrofear_activation', 'r0=player_side. Call scan_equip_zone_for_activation_by_card(player_side,0x1466) for Dark Necrofear and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d334, 'scan_equip_zone_for_manticore_of_darkness_activation', 'r0=player_side. Call scan_equip_zone_for_activation_by_card(player_side,0x16f9) for Manticore of Darkness and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d344, 'scan_equip_zone_for_fox_fire_activation', 'r0=player_side. Call scan_equip_zone_for_activation_by_card(player_side,0x1836) for Fox Fire and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d354, 'scan_equip_zone_for_helios_duo_megiste_activation', 'r0=player_side. Call scan_equip_zone_for_activation_by_card(player_side,0x19f7) for Helios Duo Megiste and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d364, 'scan_equip_zone_for_helios_tris_megiste_activation', 'r0=player_side. Call scan_equip_zone_for_activation_by_card(player_side,0x19f8) for Helios Tris Megiste and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d374, 'scan_equip_zone_for_super_rejuvenation_activation', 'r0=starting_player. Resume shared cursor 0..1 as side=starting_player^cursor. Require a positive Super Rejuvenation type1 node, zero opposing Protector of the Sanctuary available zones, and nonzero product of type1/type2 chain-node counts. Activate with the node low16 and product payload, then enqueue type2 node-check sprite; return 0 without advancing cursor. Misses increment cursor and continue; cursor>1 returns 1.'),
    (0x0809d438, 'scan_equip_slot_for_twin_headed_behemoth_activation', 'r0=starting_player. Resume shared cursor 0..1 as side=starting_player^cursor. Find a positive Twin-Headed Behemoth zone0xb node. If (find_zone_descriptor_by_slot_id(node)>>8)&0xff equals 0xe, call activation with TWIN_HEADED_BEHEMOTH_ACTIVATION_PACKED and node low16. Regardless of descriptor type, enqueue the chain sprite and return 0 without advancing cursor. Missing nodes advance cursor; exhaustion returns 1.'),
    (0x0809d4bc, 'scan_spell_trap_zone_slots_for_equip_activation_human_wave_tactics', 'No input parameters. Load r0=0x17b2 (Human-Wave Tactics), call scan_spell_trap_zone_slots_for_equip_activation_by_card, and forward its return value. Player order and shared scan cursor are managed by the callee.'),
    (0x0809d4cc, 'scan_monster_zone_slots_for_equip_activation_little_winguard', 'r0=player_side. Call scan_monster_zone_slots_for_equip_activation_by_player(player_side,0x12a3) for Little-Winguard and forward its return value. This wrapper has its own BL/return frame; scan state and activation work are managed by the callee.'),
    (0x0809d4dc, 'scan_spell_trap_zone_slots_for_equip_activation_ectoplasmer', 'No input parameters. Load r0=0x12dc (Ectoplasmer), call scan_spell_trap_zone_slots_for_equip_activation_by_card, and forward its return value. Player order and shared scan cursor are managed by the callee.'),
    (0x0809d4ec, 'scan_spell_trap_zone_slots_for_equip_activation_labyrinth_of_nightmare', 'No input parameters. Load r0=0x17b6 (Labyrinth of Nightmare), call scan_spell_trap_zone_slots_for_equip_activation_by_card, and forward its return value. Player order and shared scan cursor are managed by the callee.'),
    (0x0809d4fc, 'scan_spell_trap_zone_slots_for_equip_activation_boss_rush', 'No input parameters. Load r0=0x1972 (Boss Rush), call scan_spell_trap_zone_slots_for_equip_activation_by_card, and forward its return value. Player order and shared scan cursor are managed by the callee.'),
    (0x0809d50c, 'scan_spell_trap_zone_slots_for_equip_activation_greed', 'No input parameters. Load r0=0x1802 (Greed), call scan_spell_trap_zone_slots_for_equip_activation_by_card, and forward its return value. Player order and shared scan cursor are managed by the callee.'),
    (0x0809d51c, 'scan_spell_trap_zone_for_two_man_cell_battle_equip', 'r0=starting_player. Resume cursor 0..9 over both sides spell/trap slots: side=starting_player^(cursor/5), slot=cursor%5+5. Test TWO_MAN_CELL_BATTLE_CID, but pack the actual field-slot CID. Attributes include type5, mode1, slot, player bit31 and side-difference bit24; pass the decoded slot entity. After a match, call activation, cursor++, return 0 regardless of result. Misses advance and continue; exhaustion returns 1.'),
    (0x0809d5f4, 'scan_equip_activation_candidates_with_name_display', 'r0=player_side. Cursor 0..4 tests five ROM CID/prompt-flag records with packed type5 activation. On success, show text0xfa with card name only if display context!=1 and record flag!=0; otherwise set gEquipLpActivBitmap=1. Add5 to cursor and return0. Cursor>=5 resumes record(cursor-5): the bitmap flag selects activation retry, else enqueue its chain sprite and increment cursor. Subtract5 and return whether cursor>4. Initial misses advance; exhaustion returns1.'),
    (0x0805b1f0, 'apply_equip_activation_via_packed_attr', 'r0=packed attributes, r1=entity reference, r2=payload. Zero a 0x18-byte stack record; store CID bits15:0 at +0. Map player bit31 to +2 bit0, slot bits20:16 to +2 bits5:1, type bits30:25 to +2 halfword bits11:6, mode bits22:21 to +3 bits5:4, and bit24 to +3 bit6. Store entity low9 at +4 bits14:6 and payload at +0x14. Return apply_card_equip_activation(record,0). Used by scan_equip_activation_candidates_with_name_display.'),
]

FUNC_RENAME = [
    (0x0809c7ac, 'scan_hand_slot_for_equip_activation_by_card_type', 'scan_monster_zone_slots_for_equip_activation_by_cid_table'),
    (0x0809c978, 'scan_monster_zone_for_equip_activation_dd_scout_plane', 'scan_zone_f_for_equip_activation_dd_scout_plane'),
    (0x0809d5f4, 'scan_hand_equip_slot_for_activation_with_name_display', 'scan_equip_activation_candidates_with_name_display'),
]

ORIGINAL_LABELS = {
    0x0809c468: 'PTR_gP1LifePoints_0809c468',
    0x0809c46c: 'DAT_0809c46c',
    0x0809c470: 'DAT_0809c470',
    0x0809c474: 'DAT_0809c474',
    0x0809c494: 'PTR_gP1LifePoints_0809c494',
    0x0809c52c: 'PTR_gP1LifePoints_0809c52c',
    0x0809c530: 'DAT_0809c530',
    0x0809c534: 'DAT_0809c534',
    0x0809c538: 'DAT_0809c538',
    0x0809c558: 'PTR_gP1LifePoints_0809c558',
    0x0809c5ec: 'PTR_gP1LifePoints_0809c5ec',
    0x0809c5f0: 'DAT_0809c5f0',
    0x0809c5f4: 'DAT_0809c5f4',
    0x0809c5f8: 'DAT_0809c5f8',
    0x0809c618: 'PTR_gP1LifePoints_0809c618',
    0x0809c6b8: 'PTR_gP1LifePoints_0809c6b8',
    0x0809c6bc: 'DAT_0809c6bc',
    0x0809c6c0: 'DAT_0809c6c0',
    0x0809c6c4: 'DAT_0809c6c4',
    0x0809c6c8: 'DAT_0809c6c8',
    0x0809c730: 'DAT_0809c730',
    0x0809c734: 'DAT_0809c734',
    0x0809c758: 'DAT_0809c758',
    0x0809c778: 'DAT_0809c778',
    0x0809c798: 'DAT_0809c798',
    0x0809c7a8: 'DAT_0809c7a8',
    0x0809c810: 'PTR_gP1LifePoints_0809c810',
    0x0809c814: 'DAT_0809c814',
    0x0809c818: 'DAT_0809c818',
    0x0809c81c: 'DAT_0809c81c',
    0x0809c820: 'DAT_0809c820',
    0x0809c824: 'PTR_switchdataD_0809c828_0809c824',
    0x0809c89c: 'DAT_0809c89c',
    0x0809c8a0: 'DAT_0809c8a0',
    0x0809c8a4: 'DAT_0809c8a4',
    0x0809c8c8: 'DAT_0809c8c8',
    0x0809c908: 'DAT_0809c908',
    0x0809c90c: 'DAT_0809c90c',
    0x0809c960: 'DAT_0809c960',
    0x0809c964: 'DAT_0809c964',
    0x0809c9fc: 'DAT_0809c9fc',
    0x0809ca00: 'DAT_0809ca00',
    0x0809ca04: 'DAT_0809ca04',
    0x0809ca08: 'DAT_0809ca08',
    0x0809ca0c: 'DAT_0809ca0c',
    0x0809ca10: 'DAT_0809ca10',
    0x0809ca64: 'DAT_0809ca64',
    0x0809ca68: 'DAT_0809ca68',
    0x0809ca8c: 'DAT_0809ca8c',
    0x0809ca90: 'DAT_0809ca90',
    0x0809cab0: 'DAT_0809cab0',
    0x0809cac0: 'DAT_0809cac0',
    0x0809cad0: 'DAT_0809cad0',
    0x0809cae0: 'DAT_0809cae0',
    0x0809cb50: 'PTR_gP1LifePoints_0809cb50',
    0x0809cb54: 'DAT_0809cb54',
    0x0809cb58: 'DAT_0809cb58',
    0x0809cb5c: 'DAT_0809cb5c',
    0x0809cb94: 'DAT_0809cb94',
    0x0809cc50: 'DAT_0809cc50',
    0x0809cc54: 'DAT_0809cc54',
    0x0809ccec: 'DAT_0809ccec',
    0x0809ccf0: 'DAT_0809ccf0',
    0x0809ccf4: 'DAT_0809ccf4',
    0x0809ccf8: 'DAT_0809ccf8',
    0x0809cdac: 'PTR_gP1LifePoints_0809cdac',
    0x0809cdb0: 'DAT_0809cdb0',
    0x0809cdb4: 'DAT_0809cdb4',
    0x0809cdb8: 'DAT_0809cdb8',
    0x0809ce5c: 'PTR_gP1LifePoints_0809ce5c',
    0x0809ce60: 'DAT_0809ce60',
    0x0809ce64: 'DAT_0809ce64',
    0x0809ce8c: 'DAT_0809ce8c',
    0x0809ce9c: 'DAT_0809ce9c',
    0x0809ceac: 'DAT_0809ceac',
    0x0809ced4: 'DAT_0809ced4',
    0x0809ced8: 'DAT_0809ced8',
    0x0809cedc: 'DAT_0809cedc',
    0x0809cef4: 'DAT_0809cef4',
    0x0809cf04: 'DAT_0809cf04',
    0x0809cf9c: 'PTR_gP1LifePoints_0809cf9c',
    0x0809cfa0: 'DAT_0809cfa0',
    0x0809cfa4: 'DAT_0809cfa4',
    0x0809cfa8: 'DAT_0809cfa8',
    0x0809d09c: 'PTR_gP1LifePoints_0809d09c',
    0x0809d0a0: 'DAT_0809d0a0',
    0x0809d0a4: 'DAT_0809d0a4',
    0x0809d0a8: 'DAT_0809d0a8',
    0x0809d0ac: 'DAT_0809d0ac',
    0x0809d0b0: 'DAT_0809d0b0',
    0x0809d158: 'PTR_gP1LifePoints_0809d158',
    0x0809d15c: 'DAT_0809d15c',
    0x0809d160: 'DAT_0809d160',
    0x0809d194: 'DAT_0809d194',
    0x0809d1c0: 'DAT_0809d1c0',
    0x0809d1d8: 'DAT_0809d1d8',
    0x0809d1f4: 'DAT_0809d1f4',
    0x0809d21c: 'DAT_0809d21c',
    0x0809d2fc: 'DAT_0809d2fc',
    0x0809d300: 'DAT_0809d300',
    0x0809d304: 'DAT_0809d304',
    0x0809d308: 'DAT_0809d308',
    0x0809d30c: 'DAT_0809d30c',
    0x0809d330: 'DAT_0809d330',
    0x0809d340: 'DAT_0809d340',
    0x0809d350: 'DAT_0809d350',
    0x0809d360: 'DAT_0809d360',
    0x0809d370: 'DAT_0809d370',
    0x0809d404: 'PTR_gP1LifePoints_0809d404',
    0x0809d408: 'DAT_0809d408',
    0x0809d40c: 'DAT_0809d40c',
    0x0809d410: 'DAT_0809d410',
    0x0809d414: 'DAT_0809d414',
    0x0809d494: 'PTR_gP1LifePoints_0809d494',
    0x0809d498: 'DAT_0809d498',
    0x0809d49c: 'DAT_0809d49c',
    0x0809d4a0: 'DAT_0809d4a0',
    0x0809d4c8: 'DAT_0809d4c8',
    0x0809d4d8: 'DAT_0809d4d8',
    0x0809d4e8: 'DAT_0809d4e8',
    0x0809d4f8: 'DAT_0809d4f8',
    0x0809d508: 'DAT_0809d508',
    0x0809d518: 'DAT_0809d518',
    0x0809d5c8: 'PTR_gP1LifePoints_0809d5c8',
    0x0809d5cc: 'DAT_0809d5cc',
    0x0809d5d0: 'DAT_0809d5d0',
    0x0809d5d4: 'DAT_0809d5d4',
    0x0809d670: 'PTR_gP1LifePoints_0809d670',
    0x0809d674: 'DAT_0809d674',
    0x0809d678: 'DAT_0809d678',
    0x0809d67c: 'DAT_0809d67c',
    0x0809d690: 'DAT_0809d690',
    0x0809d6cc: 'DAT_0809d6cc',
    0x0809d70c: 'DAT_0809d70c',
    0x0809d710: 'PTR_gP1LifePoints_0809d710',
    0x0809d714: 'DAT_0809d714',
}

SWITCH_WORDS = [
    (0x0809c828, 0x0809c84c),
    (0x0809c82c, 0x0809c84c),
    (0x0809c830, 0x0809c8a8),
    (0x0809c834, 0x0809c8a8),
    (0x0809c838, 0x0809c8a8),
    (0x0809c83c, 0x0809c84c),
    (0x0809c840, 0x0809c84c),
    (0x0809c844, 0x0809c8a8),
    (0x0809c848, 0x0809c84c),
]

EXTERNAL_WORDS = [
    (0x09e47680, 0x000017ab),
    (0x09e47684, 0x000017ac),
    (0x09e47688, 0x00001315),
    (0x09e4768c, 0x00000001),
    (0x09e47690, 0x00001449),
    (0x09e47694, 0x00000000),
    (0x09e47698, 0x0000144c),
    (0x09e4769c, 0x00000000),
    (0x09e476a0, 0x00001452),
    (0x09e476a4, 0x00000000),
    (0x09e476a8, 0x00001457),
    (0x09e476ac, 0x00000000),
]

SWITCH_LABELS = {0x0809c828: (6745, 'switchD_0809c80c::switchdataD_0809c828', 'switchD_0809c80c__switchdataD_0809c828')}

FUNCTION_GUARDS = [{'incoming': [{'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0804c932', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0809d638', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0809f662', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0809a148', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0809e62a', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '08096f34', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '08096f80', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0804d916', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0804d984', 'to': '0805b1f0', 'operand': 0, 'primary': True}, {'source': 'DEFAULT', 'type': 'UNCONDITIONAL_CALL', 'from': '0804d9e2', 'to': '0805b1f0', 'operand': 0, 'primary': True}], 'body_sha256': 'b0ea951d4215c413ea1b349033bd10ae4c8bfcea0762c92cd1675fd801f378db', 'body': '[[0805b1f0, 0805b295]]', 'body_size': 166, 'name': 'apply_equip_activation_via_packed_attr', 'addr': 134590960, 'symbol_id': 455, 'eols': []}, {'incoming': [], 'body_sha256': '45fe1530fc4b76e5f9c7f303c9ffbee32fe89835bac772faec9bec5bd5139f27', 'body': '[[0809c7ac, 0809c80d] [0809c84c, 0809c89b] [0809c8a8, 0809c8c7]]', 'body_size': 210, 'name': 'scan_hand_slot_for_equip_activation_by_card_type', 'addr': 134858668, 'symbol_id': 6772, 'eols': []}, {'incoming': [], 'body_sha256': '7573d4e6806c0add7a6e9026764cd64a7a9c261fc1be9d41b026e0985bc969ec', 'body': '[[0809c978, 0809c9f9] [0809ca14, 0809ca31]]', 'body_size': 160, 'name': 'scan_monster_zone_for_equip_activation_dd_scout_plane', 'addr': 134859128, 'symbol_id': 15795, 'eols': []}, {'incoming': [], 'body_sha256': '8e9b57ba55a564fcb4295c4108c077e8990f178bd496948eda4a8aeaa533d1bd', 'body': '[[0809d5f4, 0809d66f] [0809d680, 0809d68f] [0809d694, 0809d6cb] [0809d6d0, 0809d70b]]', 'body_size': 256, 'name': 'scan_hand_equip_slot_for_activation_with_name_display', 'addr': 134862324, 'symbol_id': 6803, 'eols': []}]
OUTSIDE_OLD_PLATE = '@ Equip activation record constructor: allocates 24-byte stack record, memset 0,\n@ unpacks 8 bit fields from r0 packed_attr to record offsets:\n@ sign bit -> [+2] bit0; bits[24..23] -> [+3] bits[6..7];\n@ bits[20..18] -> [+3] bits[5..4]; bits[15..11] -> [+2] bits[2..7];\n@ bits[31..26] -> [+2..3].\n@ r1 (u16 entity_id, 9 bits) lsls #6 -> [+4] mask 0xffff803f.\n@ r2 -> sp[0x14] (callee 4th arg). Then bl apply_card_equip_activation.\n@ r0=u32 card_attr_packed; r1=u16 entity_id [0..0xffff]; r2=u32 extra_payload.\n@ Returns u32 (decided by apply_card_equip_activation).\n@ Direct callee of apply_equip_activation_with_id_lookup when r1!=0;\n@ also called by apply_equip_activation_with_fixed_type_a /\n@ apply_equip_activation_via_deck_slot_lookup /\n@ run_equip_spell_display_state_machine /\n@ scan_hand_equip_slot_for_activation_with_name_display.\n@ Constants: BUF_SIZE=0x18, ENTITY_SHIFT=6, ATTR_MASK=0xffff803f.'
# END PROPOSAL TABLES

symTbl = currentProgram.getSymbolTable()
refMgr = currentProgram.getReferenceManager()
listing = currentProgram.getListing()
eqTbl = currentProgram.getEquateTable()
memory = currentProgram.getMemory()
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME'))


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
    for value in range(0x09e47680, 0x09e476b0):
        addr = toAddr(value)
        data = listing.getDefinedDataAt(addr)
        if data is not None:
            definitions.append((str(data.getAddress()), data.getLength(),
                                data.getDataType().getPathName(), str(data.getMinAddress()), str(data.getMaxAddress())))
        for row in all_refs(value):
            outgoing.append(row)
        for ref in refMgr.getReferencesTo(addr):
            # The sole permitted incoming change is the planned base reference.
            if any(value == target and ref.getFromAddress() == toAddr(slot) and ref.getOperandIndex() == 0
                   for slot, target, name, label in REF_SLOTS):
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
    for addr in (0x0809c80c,):
        if memory.getShort(toAddr(addr)) & 0xffff != 0x4687:
            fail('SWITCH_MOV_PC 0x%08x' % addr)
    for slot, value in EXTERNAL_WORDS:
        actual = memory.getInt(toAddr(slot)) & 0xffffffff
        if actual != value:
            fail('EXTERNAL_RAW_VALUE 0x%08x expected=%08x actual=%08x' % (slot, value, actual))
    for base in (0x09e47680, 0x09e47688):
        if getFunctionAt(toAddr(base)) is not None:
            fail('EXTERNAL_TABLE_NOT_FUNCTION 0x%08x' % base)


def preserved_refs(slot, target):
    return sorted((str(r.getFromAddress()), str(r.getToAddress()), r.getOperandIndex(),
                   str(r.getReferenceType()), str(r.getSource()))
                  for r in refMgr.getReferencesFrom(toAddr(slot))
                  if not (r.getOperandIndex() == 0 and r.getToAddress() == toAddr(target)))


FUNCTION_BODY_REFS = {}


def ref_tuple(ref):
    return (str(ref.getFromAddress()), str(ref.getToAddress()), ref.getOperandIndex(),
            str(ref.getReferenceType()), str(ref.getSource()), bool(ref.isPrimary()))


def body_references(fn):
    result = []
    addresses = fn.getBody().getAddresses(True)
    while addresses.hasNext():
        addr = addresses.next()
        result.extend(ref_tuple(ref) for ref in refMgr.getReferencesFrom(addr))
    return sorted(result)


def verify_function_guards(post=False):
    renamed = dict((addr, new) for addr, old, new in FUNC_RENAME)
    for guard in FUNCTION_GUARDS:
        addr = guard['addr']
        fn = getFunctionAt(toAddr(addr))
        expected_name = renamed.get(addr, guard['name']) if post or MODE == 'check' else guard['name']
        if fn is None:
            fail('FUNCTION_MISSING 0x%08x' % addr)
            continue
        symbol = fn.getSymbol()
        if (symbol.getID() != guard['symbol_id'] or symbol.getSymbolType() != SymbolType.FUNCTION or
                symbol.getSource() != SourceType.USER_DEFINED or not symbol.isPrimary() or
                fn.getName() != expected_name or fn.getEntryPoint() != toAddr(addr)):
            fail('FUNCTION_ID_NAME_TYPE 0x%08x' % addr)
        if str(fn.getBody()) != guard['body'] or fn.getBody().getNumAddresses() != guard['body_size']:
            fail('FUNCTION_BODY_RANGE 0x%08x' % addr)
        byte_values, eols = [], []
        addresses = fn.getBody().getAddresses(True)
        while addresses.hasNext():
            pos = addresses.next()
            byte_values.append(chr(memory.getByte(pos) & 255))
            eol = listing.getComment(CodeUnit.EOL_COMMENT, pos)
            if eol is not None:
                eols.append([str(pos), unicode(eol)])
        if hashlib.sha256(''.join(byte_values)).hexdigest() != guard['body_sha256'] or eols != guard['eols']:
            fail('FUNCTION_BYTES_OR_EOL 0x%08x' % addr)
        incoming = sorted(ref_tuple(ref) for ref in refMgr.getReferencesTo(toAddr(addr)))
        expected_refs = sorted((ref['from'], ref['to'], ref['operand'], ref['type'], ref['source'], ref['primary']) for ref in guard['incoming'])
        if incoming != expected_refs:
            fail('FUNCTION_INCOMING 0x%08x' % addr)
        if post:
            if body_references(fn) != FUNCTION_BODY_REFS[addr]:
                fail('FUNCTION_BODY_REFERENCES 0x%08x' % addr)
        else:
            FUNCTION_BODY_REFS[addr] = body_references(fn)
        if addr == 0x0805b1f0 and not post and MODE != 'check':
            if listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(addr)) != OUTSIDE_OLD_PLATE:
                fail('OUTSIDE_OLD_PLATE')
        print('FUNCTION_GUARD phase=%s addr=%08x id=%d name=%s body=%d incoming=%d' %
              ('post' if post else 'pre', addr, symbol.getID(), fn.getName(), fn.getBody().getNumAddresses(), len(incoming)))


def preflight():
    global EXTERNAL_STATE
    verify_function_guards()
    for addr, old, new in FUNC_RENAME:
        require_name_available(new, addr)
    verify_tables()
    EXTERNAL_STATE = external_state()
    print('EXTERNAL_STATE_BEFORE %r' % (EXTERNAL_STATE,))
    for target in SWITCH_LABELS:
        require_switch_symbol(target)
    for slot, target in SWITCH_WORDS:
        CASE_SYMBOLS[target] = case_symbols(target)
    all_slots = [r[0] for r in EQ_SLOTS + REF_SLOTS + RENAME_SLOTS]
    if len(all_slots) != 136 or len(set(all_slots)) != 136:
        fail('SLOT_COVERAGE')
    for slot, value, name, label in EQ_SLOTS + REF_SLOTS:
        _check(slot, value)
        require_name_available(label, slot)
        if not 0x0809c3d8 <= slot < 0x0809d718:
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
        if not 0x0809c3d8 <= slot < 0x0809d718:
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
        expected_name = next((old for value, old, new in FUNC_RENAME if value == addr), fn_name) if MODE != 'check' else fn_name
        if fn is None or fn.getName() != expected_name or cu is None:
            fail('PLATE_FUNCTION 0x%08x %s' % (addr, fn_name))
        else:
            FUNCTION_BODIES[addr] = str(fn.getBody())
        if cu is not None and not cu.getComment(CodeUnit.PLATE_COMMENT):
            fail('PLATE_PATTERN 0x%08x' % addr)
        require_ascii(text, 'PLATE 0x%08x' % addr)
        if len(text) > 500:
            fail('PLATE_LENGTH 0x%08x %d' % (addr, len(text)))
    print('PREFLIGHT slots=136 EQ=99 REF=18 RENAME=19 PLATE=56 EOL=21 FUNC_RENAME=3 FAIL=%d' % len(FAILS))


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
    for addr, old, new in FUNC_RENAME:
        getFunctionAt(toAddr(addr)).setName(new, SourceType.USER_DEFINED)
        COUNTS['FUNC_RENAME'] += 1
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
    verify_function_guards(True)
    verify_tables()
    after = external_state()
    if after != EXTERNAL_STATE:
        fail('POST_EXTERNAL_DEFINITIONS_OR_REFS')
    print('EXTERNAL_STATE_AFTER %r' % (after,))
    print('EXTERNAL_PRESERVED definitions=%d outgoing_refs=%d other_incoming_refs=%d' %
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


print('=== RefineF12Seg10Slots mode=%s ===' % MODE)
preflight()
if FAILS:
    raise RuntimeError('PREFLIGHT FAIL; no writes performed')
if MODE == 'apply':
    transaction = currentProgram.startTransaction('Refine F12-Seg-10 slots')
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
    COUNTS.update({'EQ': 99, 'REF': 18, 'RENAME': 19, 'PLATE': 56, 'EOL': 21, 'FUNC_RENAME': 3})
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
