# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg1Slots.py -- file 05 Seg-1 (0x08049014..0x0804a5b8)
#   24 functions: submit_effect_zone_lp_and_shape_sprites ..
#                 enqueue_sprite_attr_for_card_slot
#
# Sections:
#   A. EQ_SLOTS  (99 slots) -- data-equate + slot rename
#   B. REF_SLOTS (14 slots) -- gP1LifePoints PTR slots
#   C. RENAME_SLOTS (39 slots) -- clear masks / OR masks / packed literals / offsets
#   D. PLATE_SUBS (35 FUN_ -> current name substitutions, 24 functions)
#
# All slot values verified against ROM via python struct.unpack before writing.
# All EOL/plate text is pure ASCII (no CJK).
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    const_name must exist in constants/*.inc (created above).
#    All values pre-verified against ROM.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- card_info.inc new CIDs ---
    (0x08049054, 0x00001256, 'BAD_REACTION_TO_SIMOCHI_CID',    'submit_effect_zone_lp_and_shape_sprites_bad_reaction_cid'),
    (0x08049114, 0x0000123b, 'CRUSH_CARD_CID',                  'tick_duel_field_zone_sprite_update_pipeline_crush_card_cid'),
    (0x08049118, 0x0000188c, 'DECK_DEVASTATION_VIRUS_CID',       'tick_duel_field_zone_sprite_update_pipeline_dek_dev_virus_cid'),
    (0x0804911c, 0x000018d5, 'PIKERU_SECOND_SIGHT_CID',          'tick_duel_field_zone_sprite_update_pipeline_pikeru_cid'),
    (0x08049120, 0x00001209, 'HIROS_SHADOW_SCOUT_CID',           'tick_duel_field_zone_sprite_update_pipeline_hiro_scout_cid'),
    (0x08049158, 0x0000178b, 'PROTECTOR_OF_THE_SANCTUARY_CID',   'tick_duel_field_zone_sprite_update_pipeline_sanctuary_cid'),
    (0x0804959c, 0x00001353, 'APPROPRIATE_CID',                  'tick_duel_field_zone_sprite_update_pipeline_appropriate_cid'),
    (0x080495b8, 0x00001802, 'GREED_CID',                        'tick_duel_field_zone_sprite_update_pipeline_greed_cid'),
    (0x080495bc, 0x00001911, 'CYBER_ARCHFIEND_CID',              'tick_duel_field_zone_sprite_update_pipeline_cyber_archfiend_cid'),
    (0x080495c8, 0x000016cd, 'HEART_OF_THE_UNDERDOG_CID',        'tick_duel_field_zone_sprite_update_pipeline_underdog_cid'),
    (0x08049720, 0x0000106d, 'PENGUIN_KNIGHT_CID',               'tick_duel_field_zone_sprite_update_pipeline_penguin_cid_a'),
    (0x08049770, 0x000017c5, 'PETEN_THE_DARK_CLOWN_CID',         'tick_duel_field_zone_sprite_update_pipeline_peten_cid_a'),
    (0x0804977c, 0x000019fe, 'DANDYLION_CID',                    'tick_duel_field_zone_sprite_update_pipeline_dandylion_cid_a'),
    (0x08049910, 0x0000106d, 'PENGUIN_KNIGHT_CID',               'render_spell_zone_card_sprite_with_id_tree_penguin_cid'),
    (0x08049960, 0x000017c5, 'PETEN_THE_DARK_CLOWN_CID',         'render_spell_zone_card_sprite_with_id_tree_peten_cid'),
    (0x0804996c, 0x000019fe, 'DANDYLION_CID',                    'render_spell_zone_card_sprite_with_id_tree_dandylion_cid'),
    (0x08049f40, 0x0000106d, 'PENGUIN_KNIGHT_CID',               'enqueue_equip_slot_sprite_with_card_check_penguin_cid'),
    (0x08049fa8, 0x00001799, 'REGENERATING_MUMMY_CID',           'enqueue_equip_slot_sprite_with_card_check_regen_mummy_cid'),
    (0x0804a410, 0x0000198a, 'BUBBLE_ILLUSION_CID',              'render_monster_slot_card_with_lp_bar_bubble_illusion_cid'),
    (0x080492c0, 0x0000123b, 'CRUSH_CARD_CID',                   'tick_duel_field_zone_sprite_update_pipeline_crush_cid_b'),
    (0x080492c8, 0x0000188c, 'DECK_DEVASTATION_VIRUS_CID',        'tick_duel_field_zone_sprite_update_pipeline_dek_dev_cid_b'),
    (0x080492cc, 0x00001209, 'HIROS_SHADOW_SCOUT_CID',            'tick_duel_field_zone_sprite_update_pipeline_hiro_scout_cid_b'),
    # --- card_info.inc reused CIDs ---
    (0x08049154, 0x00001cf4, 'FIELD_STATE_OFF',                   'tick_duel_field_zone_sprite_update_pipeline_field_state_off'),
    (0x080495c4, 0x00001cf4, 'FIELD_STATE_OFF',                   'tick_duel_field_zone_sprite_update_pipeline_field_state_off_b'),
    (0x0804a26c, 0x00001cf4, 'FIELD_STATE_OFF',                   'enqueue_equip_slot_sprite_with_card_check_field_state_off'),
    (0x0804a214, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',              'enqueue_equip_slot_sprite_with_card_check_lp_block2_off'),
    (0x0804a268, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',              'enqueue_equip_slot_sprite_with_card_check_lp_block2_off_b'),
    (0x080492a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'tick_duel_field_zone_sprite_update_pipeline_player_stride'),
    (0x080492a8, 0x0201c740, 'gP1SlotSetCodeArray',               'tick_duel_field_zone_sprite_update_pipeline_slot_code_arr'),
    (0x080495ac, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'tick_duel_field_zone_sprite_update_pipeline_player_stride_b'),
    (0x080495b0, 0x0201c510, 'gDuelFieldSlots',                   'tick_duel_field_zone_sprite_update_pipeline_duel_slots'),
    (0x080495b4, 0x0201c520, 'gDuelFieldSlotState',               'tick_duel_field_zone_sprite_update_pipeline_slot_state'),
    (0x08049648, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'enqueue_equip_zone_sprite_attr_full_player_stride'),
    (0x08049700, 0x0201c740, 'gP1SlotSetCodeArray',               'enqueue_equip_zone_sprite_attr_full_slot_code_arr'),
    (0x08049828, 0x0201c740, 'gP1SlotSetCodeArray',               'enqueue_equip_zone_sprite_attr_full_slot_code_arr_b'),
    (0x08049b38, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'render_pair_zone_sprites_if_field_card_present_player_stride'),
    (0x08049b3c, 0x0201c4f0, 'gP1SlotCountBase',                  'render_pair_zone_sprites_if_field_card_present_slot_count_base'),
    (0x08049b40, 0x0201c4f8, 'gP1ChainZoneCountBase',             'render_pair_zone_sprites_if_field_card_present_chain_count'),
    (0x08049d0c, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'render_matched_pair_zone_sprites_player_stride'),
    (0x08049d10, 0x0201c740, 'gP1SlotSetCodeArray',               'render_matched_pair_zone_sprites_slot_code_arr'),
    (0x08049d18, 0x0201c4f0, 'gP1SlotCountBase',                  'render_matched_pair_zone_sprites_slot_count_base'),
    (0x08049d1c, 0x0201c880, 'gP1ChainZoneArray',                 'render_matched_pair_zone_sprites_chain_zone_arr'),
    (0x08049dc8, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'enqueue_pair_zone_sprite_attr_by_card_id_player_stride'),
    (0x0804a0dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'enqueue_equip_slot_sprite_with_card_check_player_stride'),
    (0x0804a150, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'enqueue_equip_slot_sprite_with_card_check_player_stride_b'),
    (0x0804a404, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'render_monster_slot_card_with_lp_bar_player_stride'),
    (0x0804a538, 0x00000868, 'PLAYER_BLOCK_STRIDE',               'enqueue_lp_field_state_sprite_by_player_player_stride'),
    (0x0804a0e0, 0x0201c5d8, 'gDuelFieldSlots_p2_base',           'enqueue_equip_slot_sprite_with_card_check_p2_slots'),
    (0x0804a154, 0x0201c5d8, 'gDuelFieldSlots_p2_base',           'enqueue_equip_slot_sprite_with_card_check_p2_slots_b'),
    (0x0804a408, 0x0201c600, 'gP1FieldArrayCBase',                'render_monster_slot_card_with_lp_bar_field_arr'),
    (0x0804964c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',         'enqueue_equip_zone_sprite_attr_full_banisher_cid'),
    (0x080499f4, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',         'render_pair_zone_sprites_if_field_card_present_banisher_cid'),
    (0x08049b94, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',         'render_spell_zone_sprite_with_field_copy_check_banisher_cid'),
    (0x08049f28, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',         'enqueue_equip_slot_sprite_with_card_check_banisher_cid'),
    (0x08049718, 0x00001653, 'DESPAIR_FROM_THE_DARK_CID',         'tick_duel_field_zone_sprite_update_pipeline_despair_cid_a'),
    (0x0804971c, 0x000012a2, 'SKULL_MARK_LADYBUG_CID',            'tick_duel_field_zone_sprite_update_pipeline_skull_ladybug_cid_a'),
    (0x08049724, 0x00001185, 'COCKROACH_KNIGHT_CID',              'tick_duel_field_zone_sprite_update_pipeline_cockroach_cid_a'),
    (0x08049738, 0x000013e3, 'ARCHFIEND_OF_GILFER_CID',           'tick_duel_field_zone_sprite_update_pipeline_archfiend_cid_a'),
    (0x08049740, 0x000014a5, 'MAKYURA_THE_DESTRUCTOR_CID',        'tick_duel_field_zone_sprite_update_pipeline_makyura_cid_a'),
    (0x08049758, 0x000016f5, 'BURNING_ALGAE_CID',                 'tick_duel_field_zone_sprite_update_pipeline_burning_algae_cid_a'),
    (0x08049908, 0x00001653, 'DESPAIR_FROM_THE_DARK_CID',         'render_spell_zone_card_sprite_with_id_tree_despair_cid'),
    (0x0804990c, 0x000012a2, 'SKULL_MARK_LADYBUG_CID',            'render_spell_zone_card_sprite_with_id_tree_skull_ladybug_cid'),
    (0x08049914, 0x00001185, 'COCKROACH_KNIGHT_CID',              'render_spell_zone_card_sprite_with_id_tree_cockroach_cid'),
    (0x08049928, 0x000013e3, 'ARCHFIEND_OF_GILFER_CID',           'render_spell_zone_card_sprite_with_id_tree_archfiend_cid'),
    (0x08049930, 0x000014a5, 'MAKYURA_THE_DESTRUCTOR_CID',        'render_spell_zone_card_sprite_with_id_tree_makyura_cid'),
    (0x08049948, 0x000016f5, 'BURNING_ALGAE_CID',                 'render_spell_zone_card_sprite_with_id_tree_burning_algae_cid'),
    (0x08049f34, 0x00001687, 'OUTSTANDING_DOG_MARRON_CID',        'enqueue_equip_slot_sprite_with_card_check_marron_cid'),
    (0x08049f38, 0x000013e3, 'ARCHFIEND_OF_GILFER_CID',           'enqueue_equip_slot_sprite_with_card_check_archfiend_cid'),
    (0x08049f3c, 0x00001185, 'COCKROACH_KNIGHT_CID',              'enqueue_equip_slot_sprite_with_card_check_cockroach_cid'),
    (0x08049f50, 0x000012a2, 'SKULL_MARK_LADYBUG_CID',            'enqueue_equip_slot_sprite_with_card_check_skull_ladybug_cid'),
    (0x08049f64, 0x0000163f, 'GRANADORA_CID',                     'enqueue_equip_slot_sprite_with_card_check_granadora_cid'),
    (0x08049f7c, 0x00001653, 'DESPAIR_FROM_THE_DARK_CID',         'enqueue_equip_slot_sprite_with_card_check_despair_cid'),
    (0x08049f9c, 0x0000179a, 'NIGHT_ASSAILANT_CID',               'enqueue_equip_slot_sprite_with_card_check_night_assailant_cid'),
    (0x08049fbc, 0x00001828, 'ROC_FROM_THE_VALLEY_OF_HAZE_CID',   'enqueue_equip_slot_sprite_with_card_check_roc_cid'),
    (0x08049fd0, 0x00001946, 'OJAMAGIC_CID',                      'enqueue_equip_slot_sprite_with_card_check_ojamagic_cid'),
    (0x0804a06c, 0x0000169f, 'PANDEMONIUM_CID',                   'enqueue_equip_slot_sprite_with_card_check_pandemonium_cid_a'),
    (0x0804a0e4, 0x0000187f, 'CENTRIFUGAL_FIELD_CID',             'enqueue_equip_slot_sprite_with_card_check_centrifugal_cid_a'),
    (0x0804a158, 0x00001522, 'VAMPIRE_LORD_CID',                  'enqueue_equip_slot_sprite_with_card_check_vampire_cid'),
    (0x0804a16c, 0x000016f9, 'MANTICORE_OF_DARKNESS_CID',         'enqueue_equip_slot_sprite_with_card_check_manticore_cid'),
    (0x0804a170, 0x0000185c, 'SACRED_PHOENIX_CID',                'enqueue_equip_slot_sprite_with_card_check_phoenix_cid'),
    (0x080495cc, 0x00001817, 'SILENT_MAGICIAN_LV4_CID',           'tick_duel_field_zone_sprite_update_pipeline_silent_mag_cid'),
    (0x080492d0, 0x000012a1, 'PARASITE_PARACIDE_CID',             'tick_duel_field_zone_sprite_update_pipeline_parasite_cid'),
    (0x080492d4, 0x000017cc, 'WATAPON_CID',                       'tick_duel_field_zone_sprite_update_pipeline_watapon_cid'),
    (0x080492c4, 0x000005dc, 'LP_COST_1500',                      'tick_duel_field_zone_sprite_update_pipeline_lp1500'),
    # --- oam_attr.inc new OAM tile P1 values ---
    (0x080490a8, 0x00008024, 'OAM_LP_ZONE_SPRITE_P1',             'submit_effect_zone_lp_and_shape_sprites_oam_p1'),
    (0x080492ac, 0x00008054, 'OAM_ZONE_UPDATE_SPRITE_P1',         'tick_duel_field_zone_sprite_update_pipeline_oam_p1'),
    (0x080495f8, 0x00008055, 'OAM_EQUIP_SLOT_TILE_P1',            'enqueue_slot_sprite_attr_by_player_oam_p1'),
    (0x080496fc, 0x00008055, 'OAM_EQUIP_SLOT_TILE_P1',            'enqueue_equip_zone_sprite_attr_full_oam_p1'),
    (0x08049b9c, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',          'render_spell_zone_sprite_with_field_copy_check_oam_p1'),
    (0x08049d14, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',          'render_matched_pair_zone_sprites_oam_p1'),
    (0x08049d40, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',          'enqueue_equip_zone_sprite_with_mode_oam_p1'),
    (0x08049e40, 0x00008056, 'OAM_EFFECT_SLOT_TILE_P1',           'enqueue_effect_slot_sprites_descending_oam_p1'),
    (0x08049f30, 0x00008031, 'OAM_EFFECT_ZONE_SPRITE_P1',         'enqueue_equip_slot_sprite_with_card_check_effect_zone_p1'),
    (0x0804a40c, 0x0000804f, 'OAM_SLOT_SPRITE_BY_PLAYER_P1',      'render_monster_slot_card_with_lp_bar_oam_p1'),
    (0x0804a4c8, 0x00008050, 'OAM_SPRITE_TYPE_SEL_P1',            'enqueue_sprite_attr_with_type_select_oam_p1'),
    (0x0804a500, 0x00008051, 'OAM_ZONE_ELIGIBLE_P1',              'check_zone_eligible_with_deck_flag_oam_p1'),
    (0x0804a53c, 0x00008057, 'OAM_LP_FIELD_STATE_P1',             'enqueue_lp_field_state_sprite_by_player_oam_p1'),
    (0x0804a56c, 0x00008053, 'OAM_LP_COUNTER_P1',                 'enqueue_lp_counter_sprite_by_player_oam_p1'),
    (0x0804a59c, 0x0000804d, 'OAM_DUEL_CARD_SLOT_P1',             'enqueue_duel_field_card_slot_sprite_oam_p1'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    All 14 slots point to gP1LifePoints = 0x0201c4e0 (ewram.inc).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x08049150, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08049150'),
    (0x080495c0, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080495c0'),
    (0x08049644, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08049644'),
    (0x080498ec, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080498ec'),
    (0x08049b34, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08049b34'),
    (0x08049b98, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08049b98'),
    (0x08049d08, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08049d08'),
    (0x08049dc4, 0x0201c4e0, 'gP1LifePoints', 'DWORD_08049dc4'),
    (0x08049e3c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_08049e3c'),
    (0x0804a210, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0804a210'),
    (0x0804a264, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0804a264'),
    (0x0804a534, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0804a534'),
    (0x0804a568, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0804a568'),
    (0x0804a598, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0804a598'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL. All EOL text is pure ASCII.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # --- Bit-clear masks (reuse existing oam_attr.inc constant names as EOL) ---
    (0x080490ac, 'tick_duel_field_zone_sprite_update_pipeline_clr_bit16',
     'OAM_SPRITE_ATTR_CLR_BIT16: clears bit16 (flip flag)'),
    (0x080490b0, 'submit_effect_zone_lp_and_shape_sprites_hi16_clr',
     'hi16 clear mask for lp_bar sprite pack (AND clears bits[31:16])'),
    (0x080492b0, 'tick_duel_field_zone_sprite_update_pipeline_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9: clears bit9 (player_side)'),
    (0x080492b4, 'tick_duel_field_zone_sprite_update_pipeline_clr_bit10',
     'OAM_SPRITE_ATTR_CLR_BIT10: clears bit10'),
    (0x080492b8, 'tick_duel_field_zone_sprite_update_pipeline_clr_x9',
     'OAM_ATTR1_X_CLEAR: clears attr1 bits[8:0] (x-pos field)'),
    (0x080495a0, 'tick_duel_field_zone_sprite_update_pipeline_clr_bit9_b',
     'OAM_SPRITE_ATTR_CLR_BIT9 (2nd ref in function)'),
    (0x080495a4, 'tick_duel_field_zone_sprite_update_pipeline_clr_x9_b',
     'OAM_ATTR1_X_CLEAR (2nd ref in function)'),
    (0x08049704, 'enqueue_equip_zone_sprite_attr_full_clr_bit11',
     'OAM_SPRITE_ATTR_CLR_BIT11: clears bit11'),
    (0x08049708, 'enqueue_equip_zone_sprite_attr_full_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9'),
    (0x0804970c, 'enqueue_equip_zone_sprite_attr_full_clr_pal',
     'OAM_ATTR2_PAL_CLEAR: clears attr2 bits[15:12] (palette field)'),
    (0x08049710, 'enqueue_equip_zone_sprite_attr_full_clr_x9',
     'OAM_ATTR1_X_CLEAR'),
    (0x08049714, 'enqueue_equip_zone_sprite_attr_full_clr_bit10',
     'OAM_SPRITE_ATTR_CLR_BIT10'),
    (0x080498f0, 'render_spell_zone_card_sprite_with_id_tree_clr_bit11',
     'OAM_SPRITE_ATTR_CLR_BIT11'),
    (0x080498f4, 'render_spell_zone_card_sprite_with_id_tree_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9'),
    (0x080498f8, 'render_spell_zone_card_sprite_with_id_tree_clr_pal',
     'OAM_ATTR2_PAL_CLEAR: clears attr2 bits[15:12]'),
    (0x080498fc, 'render_spell_zone_card_sprite_with_id_tree_x9mask',
     'OAM_ATTR1_X_MASK=0x1ff: mask for attr1 x-pos bits[8:0]'),
    (0x08049900, 'render_spell_zone_card_sprite_with_id_tree_clr_x9',
     'OAM_ATTR1_X_CLEAR'),
    (0x08049904, 'render_spell_zone_card_sprite_with_id_tree_clr_bit10',
     'OAM_SPRITE_ATTR_CLR_BIT10'),
    (0x08049f2c, 'enqueue_equip_slot_sprite_with_card_check_clr_pal',
     'OAM_ATTR2_PAL_CLEAR'),
    (0x0804a468, 'render_monster_slot_card_with_lp_bar_clr_x9',
     'OAM_ATTR1_X_CLEAR'),
    (0x0804a46c, 'render_monster_slot_card_with_lp_bar_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9'),
    (0x0804a470, 'render_monster_slot_card_with_lp_bar_clr_bits13_10',
     'OAM_SPRITE_ATTR_CLR_BITS13_10'),
    (0x0804a474, 'render_monster_slot_card_with_lp_bar_clr_bit14',
     'SLOT_ACTIVE_BIT14_CLR: clears bit14'),
    (0x0804a478, 'render_monster_slot_card_with_lp_bar_clr_bit15',
     'SLOT_ACTIVE_BIT15_CLR: clears bit15'),
    (0x0804a47c, 'render_monster_slot_card_with_lp_bar_clr_bit16',
     'OAM_SPRITE_ATTR_CLR_BIT16'),
    (0x0804a480, 'render_monster_slot_card_with_lp_bar_clr_bit17',
     'OAM_SPRITE_ATTR_CLR_BIT17'),
    (0x080490a4, 'submit_effect_zone_lp_and_shape_sprites_u16max',
     '0xffff: lp_bar effect_count clamp cap (u16 max)'),
    # --- OAM attr2 packed OR masks (new oam_attr.inc constants) ---
    (0x08049330, 'tick_duel_field_pipeline_oam_attr2_or_3250',
     'OAM_ATTR2_OR_0X3250: hi16=0x3250 attr2 OR mask; lo16=0 -- med-conf bit pattern'),
    (0x080495a8, 'tick_duel_field_pipeline_oam_attr2_or_3220',
     'OAM_ATTR2_OR_0X3220: hi16=0x3220 attr2 OR mask; lo16=0 -- med-conf bit pattern'),
    (0x0804982c, 'enqueue_equip_zone_sprite_attr_full_oam_attr2_or_384e',
     'OAM_ATTR2_OR_0X384E: hi16=0x384e attr2 OR mask; lo16=0 -- med-conf bit pattern'),
    (0x080499c0, 'render_spell_zone_card_sprite_with_id_tree_oam_attr2_or_384e',
     'OAM_ATTR2_OR_0X384E (2nd site) -- med-conf bit pattern'),
    (0x0804a2c4, 'submit_equip_slot_sprite_zone11_oam_attr2_or_3c4e',
     'OAM_ATTR2_OR_0X3C4E: hi16=0x3c4e attr2 OR mask; lo16=0 -- med-conf bit pattern'),
    # --- packed OAM+CID 32-bit literals (apply_equip_activation_with_id_lookup r2 param) ---
    (0x08049598, 'tick_duel_field_pipeline_packed_watapon',
     'hi16=0x3250(OAM_ATTR2_OR_0X3250) lo16=0x17cc(WATAPON_CID); packed r2 arg -- med-conf'),
    (0x0804a070, 'enqueue_equip_slot_sprite_packed_pandemonium_p1',
     'hi16=0x012a(r_attr bits) lo16=0x169f(PANDEMONIUM_CID); P1 path packed r2 -- med-conf'),
    (0x0804a0d8, 'enqueue_equip_slot_sprite_packed_pandemonium_p2',
     'hi16=0x002a(r_attr bits) lo16=0x169f(PANDEMONIUM_CID); P2 path packed r2 -- med-conf'),
    (0x0804a0e8, 'enqueue_equip_slot_sprite_packed_centrifugal_p1',
     'hi16=0x012a(r_attr bits) lo16=0x187f(CENTRIFUGAL_FIELD_CID); P1 path packed r2 -- med-conf'),
    (0x0804a14c, 'enqueue_equip_slot_sprite_packed_centrifugal_p2',
     'hi16=0x002a(r_attr bits) lo16=0x187f(CENTRIFUGAL_FIELD_CID); P2 path packed r2 -- med-conf'),
    # --- offset/count constants ---
    (0x080492bc, 'tick_duel_field_pipeline_lp_thresh_1499',
     '0x5db=1499; ble => field3<=1499 (i.e. less than LP_COST_1500=0x5dc); Crush Card LP gate'),
    (0x08049f68, 'enqueue_equip_slot_sprite_kaiser_glider_cid',
     '0x14e9=KAISER_GLIDER_CID (pw=52824910); direct CID slot -- high-conf'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Replace old_substr with new_substr in PLATE_COMMENT of the function.
#    Pure ASCII. Applied to all 24 functions that have FUN_ in their plates.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # submit_effect_zone_lp_and_shape_sprites (0x08049014)
    (0x08049014, 'FUN_080655ec', 'submit_equip_lp_indicators_with_bar'),
    (0x08049014, 'FUN_08067160', 'dispatch_effect_zone_lp_sprites_by_slot_flags'),
    (0x08049014, 'FUN_0806a884', 'tick_zone_sprite_pipeline_for_lp_shape_enqueue'),
    (0x08049014, 'FUN_0806b31c', 'dispatch_neo_daedalus_effect_display_by_state'),
    (0x08049014, 'FUN_0806b56c', 'dispatch_numinous_healer_lp_zone_sprites'),
    (0x08049014, 'FUN_0808ee80', 'enqueue_active_card_shape_sprites_in_zone'),
    # tick_duel_field_zone_sprite_update_pipeline (0x080490b4)
    (0x080490b4, 'FUN_080495d0', 'tick_zone_sprite_pipeline_with_update_flag'),
    (0x080490b4, 'FUN_08067750', 'tick_equip_chain_banisher_sprite_state'),
    (0x080490b4, 'FUN_0809bfd4', 'dispatch_equip_action_sprite_by_phase_state'),
    # enqueue_slot_sprite_attr_by_player (0x080495dc)
    (0x080495dc, 'FUN_080495fc', 'enqueue_equip_zone_sprite_attr_full'),
    # enqueue_equip_zone_sprite_attr_full (0x080495fc)
    (0x080495fc, 'FUN_0806abec', 'dispatch_equip_effect_slot_display_by_state_and_card'),
    (0x080495fc, 'FUN_080750c0', 'dispatch_equip_node_display_by_type_code'),
    # render_pair_zone_sprites_if_field_card_present (0x080499c4)
    (0x080499c4, 'FUN_0806d960', 'dispatch_field_spell_placement_display_by_state'),
    (0x080499c4, 'FUN_0807f0a4', 'tick_prng_pair_zone_sprite_by_field_card'),
    # enqueue_effect_slot_sprites_descending (0x08049dec)
    (0x08049dec, 'FUN_080665d4', 'dispatch_zone_state_for_reserved_icid_slot'),
    (0x08049dec, 'FUN_0806abec', 'dispatch_equip_effect_slot_display_by_state_and_card'),
    # enqueue_equip_slot_sprite_with_card_check (0x08049e44)
    (0x08049e44, 'FUN_0804a2c8', 'submit_equip_slot_sprite_zone11'),
    (0x08049e44, 'FUN_0804a2e4', 'enqueue_equip_slot_sprite_zone13'),
    (0x08049e44, 'FUN_0804a30c', 'enqueue_equip_slot_sprite_zone12'),
    # submit_equip_slot_sprite_zone11 (0x0804a2c8)
    (0x0804a2c8, 'FUN_08067c0c', 'tick_equip_head_slot_sprite_state_machine'),
    (0x0804a2c8, 'FUN_08068990', 'dispatch_equip_slot_sprite_by_state_and_zone'),
    (0x0804a2c8, 'FUN_08069260', 'dispatch_equip_zone_sprite_multi_zone_by_lp_state'),
    (0x0804a2c8, 'FUN_0807b0c8', 'update_zone_entry_sprite_by_descriptor'),
    (0x0804a2c8, 'FUN_0808f608', 'scan_chain_nodes_for_equip_zone_sprite'),
    # render_monster_slot_card_with_lp_bar (0x0804a334)
    (0x0804a334, 'FUN_0806c828', 'tick_equip_effect_node_display_state_machine'),
    (0x0804a334, 'FUN_08095d84', 'dispatch_lp_bar_animation_step'),
    # enqueue_duel_field_card_slot_sprite (0x0804a570)
    (0x0804a570, 'FUN_08090218', 'dispatch_equip_field_scan_sequence'),
    # enqueue_sprite_attr_for_card_slot (0x0804a5a0)
    (0x0804a5a0, 'FUN_0808f7c0', 'enqueue_sprite_by_field_copy_count'),
    # enqueue_sprite_attr_with_type_select (0x0804a4ac) - references file 04 functions
    (0x0804a4ac, 'FUN_08044674', 'enqueue_graveyard_spell_sprite_and_lp'),
    (0x0804a4ac, 'FUN_08044714', 'enqueue_graveyard_spell_sprite_with_zone_ref'),
    (0x0804a4ac, 'FUN_080447d4', 'enqueue_hand_card_sprite_alt_by_zone_slot'),
    (0x0804a4ac, 'FUN_080448a0', 'enqueue_graveyard_spell_sprite_with_player_xor'),
    (0x0804a4ac, 'FUN_08044a34', 'enqueue_hand_sprite_by_zone_set_code'),
    # enqueue_monster_zone_equip_sprites_and_lp_counters plate reference
    # (this function is outside Seg-1 but its plate may reference Seg-1 callers)
    # enqueue_sprite_attr_type11 plate (0x0804a484) - indeg note FUN_ refs
    # Note: enqueue_monster_zone_equip_sprites_and_lp_counters = FUN_080718c4
    # We only process functions within Seg-1 [0x08049014, 0x0804a5b8)
    # tick_zone_sprite_pipeline_with_update_flag (0x080495d0) - no FUN_ in plate expected
    # check_zone_eligible_with_deck_flag (0x0804a4cc) - no FUN_ expected
    # enqueue_lp_field_state_sprite_by_player (0x0804a504) - no FUN_ expected
    # enqueue_lp_counter_sprite_by_player (0x0804a540) - no FUN_ expected
    # render_spell_zone_card_sprite_with_id_tree (0x08049830) - no FUN_ per proposal
    # render_pair_zone_sprites_if_field_card_present already handled above
    # render_spell_zone_sprite_with_field_copy_check (0x08049b44) - no FUN_ expected
    # render_matched_pair_zone_sprites (0x08049bbc) - no FUN_ expected
    # enqueue_equip_zone_sprite_with_mode (0x08049d20) - no FUN_ expected
    # enqueue_pair_zone_sprite_attr_by_card_id (0x08049d44) - no FUN_ expected
    # enqueue_equip_slot_sprite_zone13 (0x0804a2e4) - no FUN_ expected
    # enqueue_equip_slot_sprite_zone12 (0x0804a30c) - no FUN_ expected
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF05Seg1Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
    nA_fail = nB_fail = nC_fail = nD_skip = 0
    made = set()

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS (%d entries) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s)" % (slot_int, err, cname))
            nA_fail += 1; continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s=0x%x)" % (slot_int, label, cname, value))
        nA += 1

    # --- B. REF_SLOTS ---
    print("--- B. REF_SLOTS (%d entries) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int)
            nB_fail += 1; continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label))
        nB += 1

    # --- C. RENAME_SLOTS ---
    print("--- C. RENAME_SLOTS (%d entries) ---" % len(RENAME_SLOTS))
    nC_fail = 0
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int)
            nC_fail += 1; continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- D. PLATE_SUBS ---
    print("--- D. PLATE_SUBS (%d entries) ---" % len(PLATE_SUBS))
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[D SKIP] no plate @ 0x%08x (looking for '%s')" % (func_int, old_s))
            nD_skip += 1; continue
        if old_s not in plate:
            print("[D SKIP] '%s' not in plate @ 0x%08x" % (old_s, func_int))
            nD_skip += 1; continue
        if DRY:
            print("[D dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nD += 1; continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s)); nD += 1

    print("[done] A=%d(fail=%d) B=%d(fail=%d) C=%d(fail=%d) D=%d(skip=%d) DRY=%s" % (
        nA, nA_fail, nB, nB_fail, nC, nC_fail, nD, nD_skip, DRY))


main()
