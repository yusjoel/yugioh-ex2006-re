# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg9Slots.py -- F06 Seg-9 (0x08059de0..0x0805b480)
#   equip eligibility / placement rule / zone activation cluster (23 named fn)
#   EQ=131  REF=1  RENAME=2  PLATE=7 (4 CJK mojibake repair + 3 stale-FUN_ rewrite)
#
# New constants added to constants/card_info.inc before running this script:
#   SPECIAL_EQUIP_SENTINEL_ID=0x19a3, ZONE_STATUS_MASK=0x303e,
#   SPECIAL_EQUIP_TARGET_CID_A=0x131e, and 20 new CID equates.
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (131 slots; all reuse existing inc constants)
#   B. REF_SLOTS  -- USER label + DATA ref + slot rename (1 fn-ptr slot)
#   C. RENAME_SLOTS -- plain rename + EOL (2 PTR_gP1LifePoints_* renames)
#   D. PLATE_FULL -- full ASCII plate rewrites (7 functions)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython double UTF-8 mojibake prevention).
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_084354-pre-F06Seg9

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
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==== Seg-9a slots ====
    # gDuelPhaseFlags = 0x0201b290 (ewram.inc)
    (0x08059dfc, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_15910', None),
    (0x08059efc, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_16059', None),
    (0x08059f48, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_16110', None),
    (0x0805a048, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_16264', None),

    # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac (duel_field.inc)
    (0x08059e00, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'equip_activation_step_off_15912', None),
    (0x08059f00, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'equip_activation_step_off_16061', None),
    (0x08059f4c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'equip_activation_step_off_16112', None),
    (0x0805a04c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'equip_activation_step_off_16266', None),

    # ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (ewram.inc)
    (0x08059e60, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_off_15959', None),

    # ELIGIB_ANIM_STATE_OFF = 0x00001d6c (ewram.inc)
    (0x08059e64, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_state_off_15961', None),

    # DARK_RULER_VANDALGYON_CID = 0x0000190a (card_info.inc)
    (0x08059fdc, 0x0000190a, 'DARK_RULER_VANDALGYON_CID', 'dark_ruler_vandalgyon_cid_16190', None),

    # PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc)
    (0x0805a094, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_16302', None),
    (0x0805a274, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_16418', None),
    (0x0805a2c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_16460', None),
    (0x0805a3d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_16600', None),

    # gDuelFieldSlots = 0x0201c510 (ewram.inc)
    (0x0805a2c4, 0x0201c510, 'gDuelFieldSlots', 'gDuelFieldSlots_16462', None),

    # SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (gl_scrollbar.inc)
    (0x0805a338, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'scrollbar_clr_bits14_6_16520', None),
    (0x0805a3dc, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'scrollbar_clr_bits14_6_16604', None),

    # gP1FieldArrayCBase = 0x0201c600 (ewram.inc)
    (0x0805a3d8, 0x0201c600, 'gP1FieldArrayCBase', 'gP1FieldArrayCBase_16602', None),

    # ==== Seg-9b slots ====
    # gDuelCardCtxBase = 0x0201e2a0 (ewram.inc)
    (0x0805a4b0, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_16712', None),
    (0x0805a5ec, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_16881', None),
    (0x0805a7c4, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_17122', None),
    (0x0805a910, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_17291', None),
    (0x0805a954, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_17327', None),
    (0x0805a998, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_17363', None),
    (0x0805ae98, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_18012', None),
    (0x0805af60, 0x0201e2a0, 'gDuelCardCtxBase', 'gDuelCardCtxBase_18113', None),

    # ACTIVATION_STATE_B_OFF = 0x00001d78 (duel_field.inc)
    (0x0805a4b8, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_16718', None),
    (0x0805a5f4, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_16885', None),
    (0x0805a7cc, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_17126', None),
    (0x0805a918, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_17295', None),
    (0x0805a958, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_17329', None),
    (0x0805a99c, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_17365', None),
    (0x0805aea0, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_18016', None),
    (0x0805af64, 0x00001d78, 'ACTIVATION_STATE_B_OFF', 'activation_state_b_off_18115', None),

    # PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) -- Seg-9b
    (0x0805a4bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_16718b', None),
    (0x0805a790, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_17096', None),
    (0x0805ae40, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_17965', None),
    (0x0805af5c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_18111', None),
    (0x0805b018, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_18200', None),
    (0x0805b0bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_18284', None),
    (0x0805b154, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_18361', None),
    (0x0805b1e0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_18432', None),
    (0x0805b478, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_18783', None),

    # gDuelFieldSlots = 0x0201c510 (ewram.inc) -- Seg-9b
    (0x0805a4c0, 0x0201c510, 'gDuelFieldSlots', 'gDuelFieldSlots_16720', None),
    (0x0805a794, 0x0201c510, 'gDuelFieldSlots', 'gDuelFieldSlots_17098', None),
    (0x0805b0c0, 0x0201c510, 'gDuelFieldSlots', 'gDuelFieldSlots_18286', None),
    (0x0805b158, 0x0201c510, 'gDuelFieldSlots', 'gDuelFieldSlots_18363', None),
    (0x0805b47c, 0x0201c510, 'gDuelFieldSlots', 'gDuelFieldSlots_18785', None),

    # SLOT_CARD_EMPTY = 0x0000ffff (card_info.inc)
    (0x0805a4c4, 0x0000ffff, 'SLOT_CARD_EMPTY', 'slot_card_empty_16722', None),

    # gDuelPhaseFlags = 0x0201b290 (ewram.inc) -- Seg-9b
    (0x0805a4fc, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_16751', None),
    (0x0805a6e4, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_17009', None),
    (0x0805a7f8, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_17148', None),
    (0x0805ae4c, 0x0201b290, 'gDuelPhaseFlags', 'gDuelPhaseFlags_17971', None),

    # LP_BAR_ANIM_STATE_OFF = 0x000004cc (ewram.inc)
    (0x0805a500, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_state_off_16753', None),
    (0x0805a6e8, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_state_off_17011', None),
    (0x0805a7fc, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_state_off_17150', None),
    (0x0805ae50, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_state_off_17973', None),

    # CHAIN_NODE_CARD_ARR_OFF = 0x000004f4 (ewram.inc)
    (0x0805a564, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'chain_node_card_arr_off_16806', None),
    (0x0805a860, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'chain_node_card_arr_off_17203', None),
    (0x0805ae54, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'chain_node_card_arr_off_17975', None),

    # SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4 (ewram.inc)
    (0x0805a568, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'sprite_row_entry_data_off_16808', None),
    (0x0805a6f0, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'sprite_row_entry_data_off_17015', None),
    (0x0805a864, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'sprite_row_entry_data_off_17205', None),

    # OAM_ATTR2_CLR_BITS_11_6 = 0xfffff03f (oam_attr.inc)
    (0x0805a56c, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6', 'oam_attr2_clr_bits11_6_16810', None),
    (0x0805a868, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6', 'oam_attr2_clr_bits11_6_17207', None),
    (0x0805b0c8, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6', 'oam_attr2_clr_bits11_6_18290', None),
    (0x0805b160, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6', 'oam_attr2_clr_bits11_6_18367', None),
    (0x0805b1ec, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6', 'oam_attr2_clr_bits11_6_18438', None),
    (0x0805b298, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6', 'oam_attr2_clr_bits11_6_18525', None),

    # COCOON_OF_EVOLUTION_CID = 0x00000fee (card_info.inc)
    (0x0805a5f8, 0x00000fee, 'COCOON_OF_EVOLUTION_CID', 'cocoon_of_evolution_cid_16887', None),
    (0x0805b324, 0x00000fee, 'COCOON_OF_EVOLUTION_CID', 'cocoon_of_evolution_cid_18599', None),

    # P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 (ewram.inc)
    (0x0805a640, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_16924', None),
    (0x0805a94c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_17323', None),
    (0x0805ab00, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_17547', None),

    # ANTI_SPELL_FRAGRANCE_CID = 0x00001390 (card_info.inc, NEW)
    (0x0805a644, 0x00001390, 'ANTI_SPELL_FRAGRANCE_CID', 'anti_spell_fragrance_cid_16926', None),
    (0x0805ae34, 0x00001390, 'ANTI_SPELL_FRAGRANCE_CID', 'anti_spell_fragrance_cid_17959', None),

    # MAKYURA_THE_DESTRUCTOR_CID = 0x000014a5 (card_info.inc)
    (0x0805a6dc, 0x000014a5, 'MAKYURA_THE_DESTRUCTOR_CID', 'makyura_the_destructor_cid_17005', None),

    # BUBBLE_ILLUSION_CID = 0x0000198a (card_info.inc)
    (0x0805a6e0, 0x0000198a, 'BUBBLE_ILLUSION_CID', 'bubble_illusion_cid_17007', None),

    # gEquipChainSlotRefs = 0x0201bb90 (ewram.inc)
    (0x0805a6ec, 0x0201bb90, 'gEquipChainSlotRefs', 'gEquipChainSlotRefs_17013', None),

    # cid_18f5 -- neutral low-conf label (no card-stats.s entry; card_id context confirmed)
    # No equate created; use RENAME_SLOTS for label only
    # cid_1684 -- neutral low-conf label (same reason)

    # CATHEDRAL_OF_NOBLES_CID = 0x0000146f (card_info.inc)
    (0x0805a798, 0x0000146f, 'CATHEDRAL_OF_NOBLES_CID', 'cathedral_of_nobles_cid_17100', None),
    (0x0805b3f4, 0x0000146f, 'CATHEDRAL_OF_NOBLES_CID', 'cathedral_of_nobles_cid_18712', None),

    # ACTIVATION_STATE_A_OFF = 0x00001d48 (duel_field.inc)
    (0x0805a79c, 0x00001d48, 'ACTIVATION_STATE_A_OFF', 'activation_state_a_off_17102', None),

    # EFFECT_ZONE_BITMASK_OFF = 0x000010d0 (duel_field.inc)
    (0x0805a994, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF', 'effect_zone_bitmask_off_17361', None),

    # SPECIAL_EQUIP_TARGET_CID_A = 0x0000131e (card_info.inc, NEW)
    (0x0805a908, 0x0000131e, 'SPECIAL_EQUIP_TARGET_CID_A', 'special_equip_target_cid_a_17287', None),

    # SPIRIT_RYU_CID = 0x000014d7 (card_info.inc, NEW)
    (0x0805a90c, 0x000014d7, 'SPIRIT_RYU_CID', 'spirit_ryu_cid_17289', None),

    # FIELD_STATE_OFF = 0x00001cf4 (duel_field.inc)
    (0x0805a950, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_17325', None),
    (0x0805abf8, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_17674', None),
    (0x0805ae5c, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_17979', None),

    # FIELD_SPELL_B_EFFECT_ID = 0x00001407 (card_info.inc)
    (0x0805aa5c, 0x00001407, 'FIELD_SPELL_B_EFFECT_ID', 'field_spell_b_effect_id_17465', None),

    # ANCIENT_GEAR_DRILL_CID = 0x000019ae (card_info.inc)
    (0x0805aa60, 0x000019ae, 'ANCIENT_GEAR_DRILL_CID', 'ancient_gear_drill_cid_17467', None),

    # LEVEL_MODULATION_CID = 0x00001944 (card_info.inc, NEW)
    (0x0805aa64, 0x00001944, 'LEVEL_MODULATION_CID', 'level_modulation_cid_17469', None),
    (0x0805aaf8, 0x00001944, 'LEVEL_MODULATION_CID', 'level_modulation_cid_17543', None),

    # DIFFUSION_WAVE_MOTION_CID = 0x000015ff (card_info.inc)
    (0x0805ab04, 0x000015ff, 'DIFFUSION_WAVE_MOTION_CID', 'diffusion_wave_motion_cid_17549', None),

    # ROYAL_COMMAND_CID = 0x0000148e (card_info.inc)
    (0x0805ab08, 0x0000148e, 'ROYAL_COMMAND_CID', 'royal_command_cid_17551', None),

    # FORCED_CEASEFIRE_CID = 0x0000188e (card_info.inc)
    (0x0805ab0c, 0x0000188e, 'FORCED_CEASEFIRE_CID', 'forced_ceasefire_cid_17553', None),

    # JUDGEMENT_OF_PHARAOH_CID = 0x00001679 (card_info.inc)
    (0x0805ab14, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'judgement_of_pharaoh_cid_17557', None),
    (0x0805abf0, 0x00001679, 'JUDGEMENT_OF_PHARAOH_CID', 'judgement_of_pharaoh_cid_17670', None),

    # PROTECTOR_OF_THE_SANCTUARY_CID = 0x0000178b (card_info.inc)
    (0x0805abfc, 0x0000178b, 'PROTECTOR_OF_THE_SANCTUARY_CID', 'protector_of_sanctuary_cid_17676', None),

    # JINZO_CID = 0x00001296 (card_info.inc)
    (0x0805ac00, 0x00001296, 'JINZO_CID', 'jinzo_cid_17678', None),

    # AMPLIFIER_CID = 0x000012d3 (card_info.inc)
    (0x0805ac04, 0x000012d3, 'AMPLIFIER_CID', 'amplifier_cid_17680', None),

    # SPELL_CANCELLER_CID = 0x000015da (card_info.inc, NEW)
    (0x0805ae2c, 0x000015da, 'SPELL_CANCELLER_CID', 'spell_canceller_cid_17955', None),

    # ANCIENT_GEAR_GOLEM_CID = 0x000018ab (card_info.inc)
    (0x0805ae30, 0x000018ab, 'ANCIENT_GEAR_GOLEM_CID', 'ancient_gear_golem_cid_17957', None),

    # SONIC_JAMMER_CID = 0x000013bd (card_info.inc)
    (0x0805ae38, 0x000013bd, 'SONIC_JAMMER_CID', 'sonic_jammer_cid_17961', None),

    # MECHANICAL_HOUND_CID = 0x00001910 (card_info.inc, NEW)
    (0x0805ae44, 0x00001910, 'MECHANICAL_HOUND_CID', 'mechanical_hound_cid_17967', None),

    # INVADER_OF_DARKNESS_CID = 0x00001722 (card_info.inc, NEW)
    (0x0805ae48, 0x00001722, 'INVADER_OF_DARKNESS_CID', 'invader_of_darkness_cid_17969', None),

    # CREEPING_DOOM_MANTA_CID = 0x00001832 (card_info.inc, NEW)
    (0x0805ae58, 0x00001832, 'CREEPING_DOOM_MANTA_CID', 'creeping_doom_manta_cid_17977', None),

    # PITCH_BLACK_WARWOLF_CID = 0x00001833 (card_info.inc, NEW)
    (0x0805ae60, 0x00001833, 'PITCH_BLACK_WARWOLF_CID', 'pitch_black_warwolf_cid_17981', None),

    # MIRAGE_DRAGON_CID = 0x00001834 (card_info.inc, NEW)
    (0x0805ae64, 0x00001834, 'MIRAGE_DRAGON_CID', 'mirage_dragon_cid_17983', None),

    # ANCIENT_GEAR_CANNON_CID = 0x000019bb (card_info.inc, NEW)
    (0x0805ae68, 0x000019bb, 'ANCIENT_GEAR_CANNON_CID', 'ancient_gear_cannon_cid_17985', None),

    # XING_ZHEN_HU_CID = 0x0000184a (card_info.inc)
    (0x0805ae6c, 0x0000184a, 'XING_ZHEN_HU_CID', 'xing_zhen_hu_cid_17987', None),

    # FAIRY_OF_THE_SPRING_CID = 0x00001664 (card_info.inc, NEW)
    (0x0805ae70, 0x00001664, 'FAIRY_OF_THE_SPRING_CID', 'fairy_of_the_spring_cid_17989', None),

    # CURSED_SEAL_FORBIDDEN_SPELL_CID = 0x000016dd (card_info.inc, NEW)
    (0x0805ae74, 0x000016dd, 'CURSED_SEAL_FORBIDDEN_SPELL_CID', 'cursed_seal_forbidden_spell_cid_17991', None),

    # SPECIAL_EQUIP_SENTINEL_ID = 0x000019a3 (card_info.inc, NEW)
    (0x0805af50, 0x000019a3, 'SPECIAL_EQUIP_SENTINEL_ID', 'special_equip_sentinel_id_18105', None),

    # CHAIN_ENERGY_CID = 0x0000132c (card_info.inc)
    (0x0805af54, 0x0000132c, 'CHAIN_ENERGY_CID', 'chain_energy_cid_18107', None),

    # ZONE_STATUS_MASK = 0x0000303e (card_info.inc, NEW)
    (0x0805b014, 0x0000303e, 'ZONE_STATUS_MASK', 'zone_code_mask_303e_18198', None),

    # SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (gl_scrollbar.inc) -- Seg-9b
    (0x0805b0c4, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'scrollbar_clr_bits14_6_18288', None),
    (0x0805b15c, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'scrollbar_clr_bits14_6_18365', None),
    (0x0805b1e8, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'scrollbar_clr_bits14_6_18436', None),
    (0x0805b2a0, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'scrollbar_clr_bits14_6_18529', None),

    # gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- Seg-9b
    (0x0805b1e4, 0x0201c600, 'gP1FieldArrayCBase', 'gP1FieldArrayCBase_18434', None),

    # OAM_ATTR1_X_MASK = 0x000001ff (oam_attr.inc)
    (0x0805b29c, 0x000001ff, 'OAM_ATTR1_X_MASK', 'oam_attr1_x_mask_18527', None),

    # SPARK_BLASTER_CID = 0x00001909 (card_info.inc)
    (0x0805b2f0, 0x00001909, 'SPARK_BLASTER_CID', 'spark_blaster_cid_18572', None),

    # GROUND_COLLAPSE_FIELD_CARD_ID = 0x00001432 (card_info.inc) [reuse diff-name]
    (0x0805b318, 0x00001432, 'GROUND_COLLAPSE_FIELD_CARD_ID', 'ground_collapse_field_card_id_18593', None),

    # SHADOW_SPELL_CID = 0x00001243 (card_info.inc, NEW)
    (0x0805b31c, 0x00001243, 'SHADOW_SPELL_CID', 'shadow_spell_cid_18595', None),

    # SPELLBINDING_CIRCLE_CID = 0x00001103 (card_info.inc, NEW)
    (0x0805b320, 0x00001103, 'SPELLBINDING_CIRCLE_CID', 'spellbinding_circle_cid_18597', None),

    # KUNAI_WITH_CHAIN_CID = 0x00001231 (card_info.inc)
    (0x0805b334, 0x00001231, 'KUNAI_WITH_CHAIN_CID', 'kunai_with_chain_cid_18608', None),

    # DARK_MAGIC_CURTAIN_CID = 0x000012de (card_info.inc)
    (0x0805b348, 0x000012de, 'DARK_MAGIC_CURTAIN_CID', 'dark_magic_curtain_cid_18619', None),

    # EQUIP_ZONE_BLOCKER_CID = 0x000013eb (card_info.inc) [reuse diff-name from Soul Exchange]
    (0x0805b358, 0x000013eb, 'EQUIP_ZONE_BLOCKER_CID', 'equip_zone_blocker_cid_18628',
     '= Soul Exchange CID; cross-player equip blocker effect node'),

    # STRAY_LAMBS_CID = 0x00001710 (card_info.inc, NEW)
    (0x0805b374, 0x00001710, 'STRAY_LAMBS_CID', 'stray_lambs_cid_18643', None),

    # BLAST_WITH_CHAIN_CID = 0x00001514 (card_info.inc)
    (0x0805b378, 0x00001514, 'BLAST_WITH_CHAIN_CID', 'blast_with_chain_cid_18645', None),

    # SKILL_DRAIN_CID = 0x0000166c (card_info.inc)
    (0x0805b388, 0x0000166c, 'SKILL_DRAIN_CID', 'skill_drain_cid_18654', None),

    # RARE_METALMORPH_CID = 0x0000184b (card_info.inc)
    (0x0805b3a4, 0x0000184b, 'RARE_METALMORPH_CID', 'rare_metalmorph_cid_18670', None),

    # AGENT_OF_JUDGMENT_SATURN_CID = 0x0000173f (card_info.inc, NEW)
    (0x0805b3a8, 0x0000173f, 'AGENT_OF_JUDGMENT_SATURN_CID', 'agent_of_judgment_saturn_cid_18672', None),

    # IMPENETRABLE_FORMATION_CID = 0x000018d3 (card_info.inc, NEW)
    (0x0805b3e8, 0x000018d3, 'IMPENETRABLE_FORMATION_CID', 'impenetrable_formation_cid_18706', None),

    # SMOKE_GRENADE_OF_THIEF_CID = 0x0000150d (card_info.inc, NEW)
    (0x0805b3ec, 0x0000150d, 'SMOKE_GRENADE_OF_THIEF_CID', 'smoke_grenade_of_thief_cid_18708', None),

    # MAGICAL_LABYRINTH_CID = 0x00001232 (card_info.inc)
    (0x0805b3f0, 0x00001232, 'MAGICAL_LABYRINTH_CID', 'magical_labyrinth_cid_18710', None),

    # THE_FIRST_SARCOPHAGUS_CID = 0x000017af (card_info.inc)
    (0x0805b408, 0x000017af, 'THE_FIRST_SARCOPHAGUS_CID', 'the_first_sarcophagus_cid_18723', None),

    # WAVE_MOTION_CANNON_CID = 0x000015ee (card_info.inc, NEW)
    (0x0805b40c, 0x000015ee, 'WAVE_MOTION_CANNON_CID', 'wave_motion_cannon_cid_18725', None),

    # TRIAL_OF_THE_PRINCESSES_CID = 0x000019d8 (card_info.inc, NEW)
    (0x0805b474, 0x000019d8, 'TRIAL_OF_THE_PRINCESSES_CID', 'trial_of_the_princesses_cid_18781', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DWORD_08059e2c -> set_equip_activation_state_by_mode_alt+1
    # Value: 0x080905e9 = 0x080905e8 | 1 (THUMB fn-ptr)
    (0x08059e2c, 0x080905e8, 'set_equip_activation_state_by_mode_alt',
     'set_equip_activation_state_mode_alt_ptr_15934',
     'THUMB fn-ptr: set_equip_activation_state_by_mode_alt+1 = 0x080905e9'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
#    Used for: PTR_gP1LifePoints_* renames + unmapped CID neutral labels
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_gP1LifePoints renames (value 0x0201c4e0 = gP1LifePoints)
    (0x08059e5c, 'PTR_gP1LifePoints_08059e5c', 'gP1LifePoints base ptr'),
    (0x0805a090, 'PTR_gP1LifePoints_0805a090', 'gP1LifePoints base ptr'),
    # Unmapped CID neutral labels (card_id context confirmed; no card-stats.s entry)
    (0x0805a6f4, 'cid_18f5_17017',
     'card_id arg (confirmed: ldr r2,slot then bl test_slot_has_active_card); no card-stats.s entry'),
    (0x0805ab10, 'cid_1684_17555',
     'card_id arg (confirmed: ldr r2,slot then bl find_effect_node_in_zone); no card-stats.s entry'),
    # Dispatch table label rename
    (0x0805a0e4, 'tick_bonding_photon_state_table', 'raw-ptr 5-entry state dispatch table for tick_bonding_or_photon_activation_seq'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: (func_addr, new_plate_ascii_text)
#    Full plate rewrite (CJK->ASCII or stale FUN_ -> current name).
#    All text is pure ASCII.
# ---------------------------------------------------------------------------
PLATE_FULL = [
    # P1: tick_equip_activation_if_pair_eligible (0x08059fc4) -- CJK mojibake repair
    (0x08059fc4,
     '@ Equip activation state-machine dispatcher. Driven by [gDuelPhaseFlags+0x4ac].\n'
     '@ Checks pair eligibility before dispatching to Vandalgyon or Water Dragon activation paths.\n'
     '@ indeg=0, Sub-type A. r0=card_entry_ptr, r1=secondary_ptr.\n'
     '@ Returns u32 bool (1=activated, 0=waiting/failed).'),

    # P2: tick_equip_activation_sprite_mode2_by_type (0x0805a1dc) -- CJK mojibake repair
    (0x0805a1dc,
     '@ Equip activation sprite routing for mode 2 cards. Symmetric to 0x08058550:\n'
     '@ extracts card_entry[+2] bits[11:2] (mask 0xfc0); tests 0xf0<<2 = 0x3c0 for r0/r1 path.\n'
     '@ r0=card_entry_ptr. Returns u32 (result of activation dispatch).'),

    # P3: check_card_placement_rules (0x0805a9a8) -- stale FUN_0802fc90 -> check_value_in_slot_chain
    (0x0805a9a8,
     '@ Comprehensive placement rule validator for card placement request.\n'
     '@ Sequentially checks: (1) find_paired_zone_entry_for_card (paired zone conflict);\n'
     '@ (2) check_card_field5_is_nonzero + check_value_in_slot_chain (continuous effect quota);\n'
     '@ (3) find_effect_node_in_zone (effect zone occupation);\n'
     '@ (4) get_card_field_summon_restriction (field-dependent summon limit);\n'
     '@ (5) get_card_extended_stat_field6/9 (extended attribute filters);\n'
     '@ (6) check_card_is_zone_pair_restricted (pair-restriction dual card check);\n'
     '@ (7) get_card_effect_zone_check_sides + count_available_effect_zones (side mask check).\n'
     '@ Any rule trigger: writes flag to gP1LifePoints-related player state and returns 1.\n'
     '@ All rules pass: returns 0.\n'
     '@ r8 is caller-set non-APCS player_state_base used for internal state writes.\n'
     '@ r0=ptr card_info ([+0]=card_id, [+2]=player_side+zone_index packed, [+3]=flag_bits).\n'
     '@ r8=ptr player_state_base (non-APCS, caller-set).\n'
     '@ Returns u8 (0=placement allowed, 1=placement blocked).\n'
     '@ Side-effect: [gP1LifePoints+0x1d78] may be written 0x14 on block path.'),

    # P4: build_zone_activation_entry_equip (0x0805b034) -- CJK mojibake repair
    (0x0805b034,
     '@ Constructs a zone activation entry for an equip-type card target.\n'
     '@ Called from eval_equip_activation_for_slot when target is an equip slot (indeg=1).\n'
     '@ Symmetric structure to build_zone_activation_entry_blocked.\n'
     '@ r0=card_ptr, r1=partner_ptr, r2=extra_payload. Returns u32 dispatch result.'),

    # P5: build_zone_activation_entry_blocked (0x0805b0cc) -- CJK mojibake repair
    (0x0805b0cc,
     '@ Constructs a zone activation entry for a blocked equip target check (indeg=3).\n'
     '@ Allocates 0x18-byte stack buffer, memset 0; writes r2(card_id) to [buf+0];\n'
     '@ writes player/slot fields to [buf+2]. Calls apply_card_equip_activation.\n'
     '@ r0=card_attr_packed, r1=entity_id, r2=card_id. Returns u32 bool.'),

    # P6: apply_equip_activation_via_packed_attr (0x0805b1f0) -- stale FUN_ refs
    (0x0805b1f0,
     '@ Equip activation record constructor: allocates 24-byte stack record, memset 0,\n'
     '@ unpacks 8 bit fields from r0 packed_attr to record offsets:\n'
     '@ sign bit -> [+2] bit0; bits[24..23] -> [+3] bits[6..7];\n'
     '@ bits[20..18] -> [+3] bits[5..4]; bits[15..11] -> [+2] bits[2..7];\n'
     '@ bits[31..26] -> [+2..3].\n'
     '@ r1 (u16 entity_id, 9 bits) lsls #6 -> [+4] mask 0xffff803f.\n'
     '@ r2 -> sp[0x14] (callee 4th arg). Then bl apply_card_equip_activation.\n'
     '@ r0=u32 card_attr_packed; r1=u16 entity_id [0..0xffff]; r2=u32 extra_payload.\n'
     '@ Returns u32 (decided by apply_card_equip_activation).\n'
     '@ Direct callee of apply_equip_activation_with_id_lookup when r1!=0;\n'
     '@ also called by apply_equip_activation_with_fixed_type_a /\n'
     '@ apply_equip_activation_via_deck_slot_lookup /\n'
     '@ run_equip_spell_display_state_machine /\n'
     '@ scan_hand_equip_slot_for_activation_with_name_display.\n'
     '@ Constants: BUF_SIZE=0x18, ENTITY_SHIFT=6, ATTR_MASK=0xffff803f.'),

    # P7: dispatch_card_effect_by_stat_type (0x0805b2a4) -- stale FUN_080954e8 -> step_prng_anim_frame
    (0x0805b2a4,
     '@ Dispatches card effect processing based on card stat type fields and special card IDs.\n'
     '@ r0=ptr card_entry (saved to r7).\n'
     '@ Step 1: checks [r7+0x4] bit1 (processed_bit=0x2); if set returns 0 (already handled).\n'
     '@ Step 2: calls check_card_effect_node_active; if node missing returns 0.\n'
     '@ Step 3: checks [r7+0x4] bit2 (alt_path_bit=0x4); if clear jumps to LAB_0805b3c2.\n'
     '@ Step 4: calls get_card_extended_stat_field9; matches field9 [2..3] range.\n'
     '@ Step 5: checks [r7+0x3] AND 0x30 (stat3_bits); if card_id==0x1909 returns 0 (special skip).\n'
     '@ Whole function is pure read; all exit paths are movs r0,#0 or movs r0,#1.\n'
     '@ Called by step_prng_anim_frame (duel scene main loop).\n'
     '@ Returns u32 should_continue (0=skip, 1=proceed).\n'
     '@ Constants: processed_bit=0x2, alt_path_bit=0x4, stat3_bits=0x30,\n'
     '@ card_id_special=0x1909, field9_range=[2..3].'),
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
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return True

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
    return True

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

def _apply_plate_full(func_addr, new_plate_text):
    """Full plate rewrite (CJK->ASCII or stale FUN_ substitution)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] PLATE_FULL 0x%08x: rewrite (%d chars)" % (func_addr, len(new_plate_text)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: plate set (%d chars)" % (func_addr, len(new_plate_text)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF06Seg9Slots (DRY=%s) ===" % DRY)
    print("  F06 Seg-9: 0x08059de0..0x0805b480")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d OK, %d FAIL/SKIP" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  [WARN] %d EQ slots failed value check -- review above FAIL lines" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
    print("  REF done: %d" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. PLATE_FULL
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)
    print("  PLATE done: %d" % len(PLATE_FULL))

    print("\n=== RefineF06Seg9Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
