# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg8aSlots.py -- file 04 Seg-8a (0x08044e30..0x0804640c)
#   update_duel_field_slot_sprite_state / enqueue_sprite_attr_with_xy_split /
#   enqueue_sprite_attr_with_shape / enqueue_equip_set_slot_sprite_by_zone_col /
#   enqueue_effect_card_slot_sprite_attr / enqueue_equip_card_sprite_attr_for_slot /
#   enqueue_effect_zone_pair_sprite_scan / apply_nitro_unit_equip_activation /
#   dispatch_card_effect_sprite_render_by_card_id
#
# Sections:
#   A. EQ_SLOTS  (116) -- equate + slot label + optional EOL
#   B. REF_SLOTS (18)  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS (9) -- plain rename + EOL (composites / packed vals)
#   D. PLATE_REWRITES (6 fn, 20 FUN_ tokens) -- substr replace

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
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- Group A: PLAYER_BLOCK_STRIDE=0x868 x11 (ewram.inc REUSE) ---
    (0x08044ed0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_08044ed0_stride', None),
    (0x0804516c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_0804516c_stride', None),
    (0x080451a8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_080451a8_stride', None),
    (0x080452dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_080452dc_stride', None),
    (0x080453f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_080453f4_stride', None),
    (0x08045488, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_08045488_stride', None),
    (0x0804558c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_0804558c_stride', None),
    (0x08045bf0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_08045bf0_stride', None),
    (0x08045c60, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_08045c60_stride', None),
    (0x08045e3c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_08045e3c_stride', None),
    (0x08045ef0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dat_08045ef0_stride', None),

    # --- Group B: OAM attr1 P2 constants (oam_attr.inc NEW) ---
    (0x08045264, 0x0000803a, 'OAM_XY_SPLIT_SPRITE_P2', 'dat_08045264_oam',
     'xy-split sprite OAM attr1 P2 (bit15=H-flip; P1=0x3a inline imm)'),
    (0x08045294, 0x0000803a, 'OAM_XY_SPLIT_SPRITE_P2', 'dat_08045294_oam', None),
    (0x080452e4, 0x0000803b, 'OAM_EQUIP_SET_SLOT_P2', 'dat_080452e4_oam',
     'equip-set slot sprite OAM attr1 P2 (bit15=H-flip; P1=0x3b inline imm)'),
    (0x08045310, 0x0000803b, 'OAM_EQUIP_SET_SLOT_P2', 'dat_08045310_oam', None),
    (0x080453fc, 0x0000803c, 'OAM_EFFECT_CARD_SLOT_P2', 'dat_080453fc_oam',
     'effect-card slot sprite OAM attr1 P2 (bit15=H-flip; P1=0x3c inline imm)'),
    (0x08045438, 0x0000803c, 'OAM_EFFECT_CARD_SLOT_P2', 'dat_08045438_oam', None),
    (0x08045490, 0x0000803c, 'OAM_EFFECT_CARD_SLOT_P2', 'dat_08045490_oam', None),
    (0x080454b8, 0x0000803c, 'OAM_EFFECT_CARD_SLOT_P2', 'dat_080454b8_oam', None),

    # --- Group C: Offset constants ---
    # P1LP_BLOCK2_OFF_1CE8=0x1ce8 x3 (ewram.inc REUSE)
    (0x08045408, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'dat_08045408_off', None),
    (0x080460e0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'dat_080460e0_off', None),
    (0x08046150, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'dat_08046150_off', None),
    # FIELD_STATE_OFF=0x1cf4 x2 (duel_field.inc REUSE)
    (0x080460e4, 0x00001cf4, 'FIELD_STATE_OFF', 'dat_080460e4_off', None),
    (0x08046154, 0x00001cf4, 'FIELD_STATE_OFF', 'dat_08046154_off', None),
    # EFFECT_ZONE_BITMASK_OFF=0x10d0 x2 (duel_field.inc REUSE)
    (0x08045a9c, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF', 'dat_08045a9c_off', None),
    (0x08045c5c, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF', 'dat_08045c5c_off', None),
    # P1LP_EQUIP_BITMAP_CTR_OFF=0x1d3c x2 (ewram.inc NEW)
    (0x080450d4, 0x00001d3c, 'P1LP_EQUIP_BITMAP_CTR_OFF', 'dat_080450d4_off',
     '[gP1LP+player*0x868+0x1d3c] modulo-10 equip-slot bitmap anim frame counter'),
    (0x08045218, 0x00001d3c, 'P1LP_EQUIP_BITMAP_CTR_OFF', 'dat_08045218_off', None),

    # --- Group D: EQUIP_CHAIN_SENTINEL=0xffff0000 x3 (duel_field.inc NEW) ---
    (0x08045a94, 0xffff0000, 'EQUIP_CHAIN_SENTINEL', 'dat_08045a94_sent',
     'gEquipChainSlotRefs list terminator sentinel; cmp rval, sentinel; beq exit'),
    (0x08045be8, 0xffff0000, 'EQUIP_CHAIN_SENTINEL', 'dat_08045be8_sent', None),
    (0x08045c54, 0xffff0000, 'EQUIP_CHAIN_SENTINEL', 'dat_08045c54_sent', None),

    # --- Group E: EQUIP_PAIR_SPRITE_EXTRA=0x101 x1 (oam_attr.inc NEW) ---
    (0x080454bc, 0x00000101, 'EQUIP_PAIR_SPRITE_EXTRA', 'dat_080454bc_pair',
     'equip pair sprite attr: type=1, mode=1'),

    # --- Group F: CID equates (card_info.inc) ---
    # REUSE existing
    (0x08044ed4, 0x00001645, 'EXODIA_NECROSS_CID', 'dat_08044ed4_cid', None),
    (0x08044f60, 0x0000147d, 'ZOMBYRA_THE_DARK_CID', 'dat_08044f60_cid', None),
    (0x08045008, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID', 'dat_08045008_cid', None),
    (0x08045028, 0x0000182d, 'RAGING_FLAME_SPRITE_CID', 'dat_08045028_cid', None),
    (0x080451c4, 0x00001368, 'SPELL_ZONE_TARGET_CARD_ID', 'dat_080451c4_cid', None),
    (0x08045400, 0x00001817, 'SILENT_MAGICIAN_LV4_CID', 'dat_08045400_cid', None),
    (0x08045524, 0x000010f4, 'UMI_CARD_ID', 'dat_08045524_cid', None),
    (0x0804572c, 0x000013ad, 'SLATE_WARRIOR_CID', 'dat_0804572c_cid', None),
    (0x08045748, 0x000013e3, 'ARCHFIEND_OF_GILFER_CID', 'dat_08045748_cid', None),
    (0x08045780, 0x00001514, 'BLAST_WITH_CHAIN_CID', 'dat_08045780_cid', None),
    (0x08045950, 0x00001951, 'WATER_DRAGON_CID', 'dat_08045950_cid', None),
    (0x080459a0, 0x000019d2, 'SAND_MOTH_CID', 'dat_080459a0_cid', None),
    (0x08045f04, 0x000014a5, 'MAKYURA_THE_DESTRUCTOR_CID', 'dat_08045f04_cid', None),
    (0x08045f3c, 0x000016f9, 'MANTICORE_OF_DARKNESS_CID', 'dat_08045f3c_cid', None),
    (0x08046234, 0x00001782, 'MOKEY_MOKEY_CID', 'dat_08046234_cid', None),
    (0x08046238, 0x00001843, 'MOKEY_MOKEY_SMACKDOWN_CID', 'dat_08046238_cid', None),
    (0x0804629c, 0x00001843, 'MOKEY_MOKEY_SMACKDOWN_CID', 'dat_0804629c_cid', None),

    # NEW card_info.inc CIDs
    (0x08044ed8, 0x00001337, 'KARATE_MAN_CID', 'dat_08044ed8_cid', None),
    (0x08044edc, 0x0000120e, 'upd_cid_120e', 'dat_08044edc_cid',
     'card gap; no card-stats entry'),
    (0x08044ee0, 0x000010c6, 'upd_cid_10c6', 'dat_08044ee0_cid',
     'card gap; no card-stats entry'),
    (0x08044ef0, 0x00001153, 'GODDESS_OF_WHIM_CID', 'dat_08044ef0_cid', None),
    (0x08044f14, 0x00001296, 'JINZO_CID', 'dat_08044f14_cid', None),
    (0x08044f30, 0x000012ac, 'SATELLITE_CANNON_CID', 'dat_08044f30_cid', None),
    (0x08044f38, 0x000012bb, 'COPYCAT_CID', 'dat_08044f38_cid', None),
    (0x08044f70, 0x000013b2, 'MUCUS_YOLK_CID', 'dat_08044f70_cid', None),
    (0x08044f8c, 0x00001527, 'ROYAL_KEEPER_CID', 'dat_08044f8c_cid', None),
    (0x08044fa4, 0x0000154c, 'EXARION_UNIVERSE_CID', 'dat_08044fa4_cid', None),
    (0x08044fd8, 0x00001835, 'GAIA_SOUL_CID', 'dat_08044fd8_cid', None),
    (0x08044fdc, 0x00001688, 'GREAT_MAJU_GARZETT_CID', 'dat_08044fdc_cid', None),
    (0x08044fec, 0x0000172b, 'EMES_THE_INFINITY_CID', 'dat_08044fec_cid', None),
    (0x08045020, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID', 'dat_08045020_cid', None),
    (0x0804504c, 0x000018fb, 'UFOROID_FIGHTER_CID', 'dat_0804504c_cid', None),
    (0x08045064, 0x000018ae, 'MILLENNIUM_SCORPION_CID', 'dat_08045064_cid', None),
    (0x08045070, 0x000018b4, 'MEGAROCK_DRAGON_CID', 'dat_08045070_cid', None),
    (0x0804508c, 0x00001996, 'WHITE_HORNS_DRAGON_CID', 'dat_0804508c_cid', None),
    (0x080450a8, 0x000019a5, 'RAVIEL_LORD_CID', 'dat_080450a8_cid', None),
    (0x080451dc, 0x000017ff, 'NINJITSU_ART_OF_DECOY_CID', 'dat_080451dc_cid', None),
    (0x080451e0, 0x00001495, 'THE_EMPERORS_HOLIDAY_CID', 'dat_080451e0_cid', None),
    (0x080451ec, 0x0000184a, 'XING_ZHEN_HU_CID', 'dat_080451ec_cid', None),
    (0x0804540c, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID', 'dat_0804540c_cid', None),
    (0x08045410, 0x000016de, 'TOWER_OF_BABEL_CID', 'dat_08045410_cid', None),
    (0x0804552c, 0x000013f7, 'TORNADO_WALL_CID', 'dat_0804552c_cid', None),
    (0x08045658, 0x00001591, 'YOMI_SHIP_CID', 'dat_08045658_cid', None),
    (0x0804565c, 0x00001342, 'MYSTIC_TOMATO_CID', 'dat_0804565c_cid', None),
    (0x08045660, 0x00000fd6, 'SANGAN_CID', 'dat_08045660_cid', None),
    (0x08045668, 0x000010dd, 'BLACK_PENDANT_CID', 'dat_08045668_cid', None),
    (0x0804568c, 0x00001185, 'COCKROACH_KNIGHT_CID', 'dat_0804568c_cid', None),
    (0x080456a4, 0x000011e4, 'WITCH_OF_THE_BLACK_FOREST_CID', 'dat_080456a4_cid', None),
    (0x080456d0, 0x0000133a, 'NIMBLE_MOMONGA_CID', 'dat_080456d0_cid', None),
    (0x080456e0, 0x00001333, 'GIANT_RAT_CID', 'dat_080456e0_cid', None),
    (0x080456f8, 0x0000133c, 'SHINING_ANGEL_CID', 'dat_080456f8_cid', None),
    (0x08045724, 0x000014ab, 'AMAZONESS_CHAIN_MASTER_CID', 'dat_08045724_cid', None),
    (0x08045758, 0x000013e9, 'upd_cid_13e9', 'dat_08045758_cid',
     'card gap; no card-stats entry'),
    (0x08045798, 0x000014f6, 'AGIDO_CID', 'dat_08045798_cid', None),
    (0x080457b0, 0x00001544, 'DARK_COFFIN_CID', 'dat_080457b0_cid', None),
    (0x080457c8, 0x0000156d, 'LORD_POISON_CID', 'dat_080457c8_cid', None),
    (0x08045800, 0x00001841, 'NECKLACE_OF_COMMAND_CID', 'dat_08045800_cid', None),
    (0x08045804, 0x000016f5, 'BURNING_ALGAE_CID', 'dat_08045804_cid', None),
    (0x08045814, 0x0000163f, 'GRANADORA_CID', 'dat_08045814_cid', None),
    (0x08045834, 0x000016c8, 'SILPHEED_CID', 'dat_08045834_cid', None),
    (0x0804583c, 0x000016cc, 'FUHMA_SHURIKEN_CID', 'dat_0804583c_cid', None),
    (0x0804586c, 0x000017c3, 'FAMILIAR_KNIGHT_CID', 'dat_0804586c_cid', None),
    (0x08045884, 0x00001796, 'EMISSARY_OF_THE_AFTERLIFE_CID', 'dat_08045884_cid', None),
    (0x080458a4, 0x000017e6, 'MASKED_DRAGON_CID', 'dat_080458a4_cid', None),
    (0x080458b4, 0x0000183d, 'MOKEY_MOKEY_KING_CID', 'dat_080458b4_cid', None),
    (0x080458e8, 0x00001914, 'GIANT_KOZAKY_CID', 'dat_080458e8_cid', None),
    (0x080458f8, 0x00001869, 'MECHA_DOG_MARRON_CID', 'dat_080458f8_cid', None),
    (0x08045914, 0x000018d7, 'KOZAKYS_SELF_DESTRUCT_CID', 'dat_08045914_cid', None),
    (0x08045924, 0x000018f4, 'UFOROID_CID', 'dat_08045924_cid', None),
    (0x08045964, 0x00001946, 'OJAMAGIC_CID', 'dat_08045964_cid', None),
    (0x08045988, 0x000019c5, 'GOKIPON_CID', 'dat_08045988_cid', None),
    (0x08045ef8, 0x000018d1, 'NITRO_UNIT_CID', 'dat_08045ef8_cid', None),
    (0x08045f00, 0x00001672, 'upd_cid_1672', 'dat_08045f00_cid',
     'card gap; no card-stats entry'),
    (0x08045f18, 0x00001522, 'VAMPIRE_LORD_CID', 'dat_08045f18_cid', None),
    (0x08045f38, 0x000018bc, 'DD_SURVIVOR_CID', 'dat_08045f38_cid', None),
    (0x08045f40, 0x0000185c, 'SACRED_PHOENIX_CID', 'dat_08045f40_cid', None),
    (0x08045f68, 0x000019f8, 'HELIOS_TRIS_MEGISTE_CID', 'dat_08045f68_cid', None),
    (0x08045fc4, 0x00001595, 'COBRA_JAR_CID', 'dat_08045fc4_cid', None),
    (0x08045fe0, 0x0000166a, 'OJAMA_TRIO_CID', 'dat_08045fe0_cid', None),
    (0x08046364, 0x00001862, 'MAJI_GIRE_PANDA_CID', 'dat_08046364_cid', None),
    (0x08046368, 0x00001875, 'FIREBIRD_CID', 'dat_08046368_cid', None),
    (0x0804636c, 0x000018b2, 'CRIOSPHINX_CID', 'dat_0804636c_cid', None),

    # Bare-CID reclassified from RENAME: Pandemonium + Centrifugal Field
    (0x08045db8, 0x0000169f, 'PANDEMONIUM_CID', 'dat_08045db8_cid', None),
    (0x08045e44, 0x0000187f, 'CENTRIFUGAL_FIELD_CID', 'dat_08045e44_cid', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gDuelFieldSlots=0x0201c510 x6 (ewram.inc REUSE)
    (0x08045170, 0x0201c510, 'gDuelFieldSlots', 'dat_08045170_ptr'),
    (0x080451ac, 0x0201c510, 'gDuelFieldSlots', 'dat_080451ac_ptr'),
    (0x080452e0, 0x0201c510, 'gDuelFieldSlots', 'dat_080452e0_ptr'),
    (0x080453f8, 0x0201c510, 'gDuelFieldSlots', 'dat_080453f8_ptr'),
    (0x0804548c, 0x0201c510, 'gDuelFieldSlots', 'dat_0804548c_ptr'),
    (0x08045590, 0x0201c510, 'gDuelFieldSlots', 'dat_08045590_ptr'),
    # gDuelFieldSlots_p2_base=0x0201c5d8 x2 (ewram.inc REUSE)
    (0x08045e40, 0x0201c5d8, 'gDuelFieldSlots_p2_base', 'dat_08045e40_ptr'),
    (0x08045ef4, 0x0201c5d8, 'gDuelFieldSlots_p2_base', 'dat_08045ef4_ptr'),
    # gEquipChainSlotRefs=0x0201bb90 x7 (ewram.inc REUSE)
    (0x080459fc, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_080459fc_ptr'),
    (0x08045a34, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_08045a34_ptr'),
    (0x08045af8, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_08045af8_ptr'),
    (0x08045b2c, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_08045b2c_ptr'),
    (0x080461bc, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_080461bc_ptr'),
    (0x0804623c, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_0804623c_ptr'),
    (0x080462a0, 0x0201bb90, 'gEquipChainSlotRefs', 'dat_080462a0_ptr'),
    # gEquipZoneCountTable=0x0201e1c8 x1 (ewram.inc NEW)
    (0x08045528, 0x0201e1c8, 'gEquipZoneCountTable', 'dat_08045528_ptr'),
    # gEquipNodePool=0x0201d9c0 x1 (ewram.inc REUSE)
    (0x08045d08, 0x0201d9c0, 'gEquipNodePool', 'dat_08045d08_ptr'),
    # apply_nitro_unit_equip_activation THUMB fn-ptr (odd addr = +1)
    (0x08045efc, 0x08045531, 'apply_nitro_unit_equip_activation', 'dat_08045efc_fnptr'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii)
#    Composite/packed vals: descriptive label + ASCII EOL
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08045594, 'nitro_unit_slot_filter',
     'slot_word<<0x13 filter: low13=NITRO_UNIT_CID(0x18d1) + activation hi-bits'),
    (0x08045598, 'nitro_unit_activation_packed',
     'packed activation: card_id=0x18d1(Nitro Unit) + ctx bits [31:13]'),
    (0x08045db4, 'archfiend_path_composite',
     'Archfiend slot path composite: upper=0x364d encode type+player fields'),
    (0x08045dbc, 'pandemonium_activation_a',
     'packed activation: card_id=0x169f(Pandemonium) + ctx=0x012a (mode A)'),
    (0x08045e38, 'pandemonium_activation_b',
     'packed activation: card_id=0x169f(Pandemonium) + ctx=0x002a (mode B)'),
    (0x08045e48, 'centrifugal_field_activation_a',
     'packed activation: card_id=0x187f(Centrifugal Field) + ctx=0x012a (mode A)'),
    (0x08045eec, 'centrifugal_field_activation_b',
     'packed activation: card_id=0x187f(Centrifugal Field) + ctx=0x002a (mode B)'),
    (0x080463d4, 'spell_path_composite_a',
     'Spell zone path composite A: upper=0x2c20 encode type+player fields'),
    (0x08046408, 'spell_path_composite_b',
     'Spell zone path composite B: upper=0x3620 encode type+player fields'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_entry_addr, [(old_fun_str, new_name), ...])
#    Substring replace FUN_<hex> in plate comments. All text ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. update_duel_field_slot_sprite_state @ 0x08044e30
    (0x08044e30, [
        ('FUN_08044dcc', 'enqueue_field_slot_sprite_with_state_update'),
        ('FUN_0805b990', 'scan_equip_zone_candidates_with_snapshot'),
    ]),

    # 2. enqueue_sprite_attr_with_xy_split @ 0x08045240
    (0x08045240, [
        ('FUN_080432bc', 'enqueue_zone_slot_sprite_attr_by_card_type'),
        ('FUN_08043d90', 'scan_equip_chain_list_for_activation_sprite'),
        ('FUN_08044e30', 'update_duel_field_slot_sprite_state'),
        ('FUN_0805847c', 'enqueue_equip_slot_sprite_with_field_bit_update'),
        ('FUN_08058f90', 'tick_equip_lp_row19_sprite_display_seq'),
    ]),

    # 3. enqueue_sprite_attr_with_shape @ 0x08045268
    (0x08045268, [
        ('FUN_0804559c', 'dispatch_card_effect_sprite_render_by_card_id'),
        ('FUN_0808e45c', 'scan_trap_zone_slots_for_equip_shape_sprite'),
        ('FUN_0808e770', 'scan_effect_zones_for_equip_activation_forced_requisition'),
        ('FUN_0808e85c', 'scan_field_slots_for_equip_sprite'),
    ]),

    # 4. enqueue_equip_set_slot_sprite_by_zone_col @ 0x08045298
    (0x08045298, [
        ('FUN_080432bc', 'enqueue_zone_slot_sprite_attr_by_card_type'),
        ('FUN_08043d90', 'scan_equip_chain_list_for_activation_sprite'),
        ('FUN_0808dc48', 'enqueue_relinquished_slot_sprite_attrs'),
        ('FUN_0808dd5c', 'scan_field_for_equip_set_slot_sprite_update'),
        ('FUN_0808f2f0', 'enqueue_exchange_slot_sprite_attrs'),
    ]),

    # 5. enqueue_effect_zone_pair_sprite_scan @ 0x080454c0
    #    FUN_08064760 appears twice; replace handles both occurrences
    (0x080454c0, [
        ('FUN_08064760', 'dispatch_equip_sprite_update_by_card_type'),
        ('FUN_0808db90', 'dispatch_equip_pair_sprites_by_state'),
    ]),

    # 6. dispatch_card_effect_sprite_render_by_card_id @ 0x0804559c
    (0x0804559c, [
        ('FUN_08047218', 'handle_card_effect_zone_eligibility_by_field6'),
        ('FUN_08047f50', 'render_slot_card_sprite_from_descriptor'),
        ('FUN_08048020', 'render_slot_card_sprite_and_effects'),
        ('FUN_08048364', 'render_slot_card_sprite_with_chaos_equip_check'),
    ]),
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
        try:
            iv = int(dv.getOffset()) & 0xffffffff
        except Exception:
            iv = None
    want32 = want & 0xffffffff
    if iv is not None and iv != want32:
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want32)
    return True, None


def main():
    print("=== RefineF04Seg8aSlots (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
    made = set()
    fails = 0

    # --- A: EQ_SLOTS ---
    for item in EQ_SLOTS:
        slot_int, val, cname, label = item[0], item[1], item[2], item[3]
        eol = item[4] if len(item) > 4 else None
        ok, err = _check(slot_int, val)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); fails += 1; continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x label=%s" % (slot_int, cname, val, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, val & 0xffffffff)
        eq.addReference(_addr(slot_int), 0)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu: cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B: REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); fails += 1; continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) label=%s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- C: RENAME_SLOTS ---
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); fails += 1; continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu: cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- D: PLATE_REWRITES ---
    for func_int, repls in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no code unit @ 0x%08x" % func_int); fails += 1; continue
        txt = cu.getComment(CodeUnit.PLATE_COMMENT)
        if txt is None:
            print("[D FAIL] no plate @ 0x%08x" % func_int); fails += 1; continue
        new = txt
        for old, rep in repls:
            if old not in new:
                print("[D WARN] 0x%08x pattern not found: %s" % (func_int, old))
            else:
                new = new.replace(old, rep)
        if DRY:
            print("[D dry] 0x%08x plate update %d repls" % (func_int, len(repls)))
            nD += 1; continue
        if new != txt:
            cu.setComment(CodeUnit.PLATE_COMMENT, new)
            print("[D ok] 0x%08x plate updated" % func_int)
        else:
            print("[D NOOP] 0x%08x plate unchanged" % func_int)
        nD += 1

    print("[done] A=%d B=%d C=%d D=%d fails=%d (DRY=%s)" % (nA, nB, nC, nD, fails, DRY))


main()
