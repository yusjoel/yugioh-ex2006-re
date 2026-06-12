# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg6Slots.py -- file 04 Seg-6 (0x0804394c..0x08044674)
#   20 functions:
#   enqueue_zone_card_sprite_attr_by_slot / invoke_equip_activation_with_zero_flag /
#   apply_slot_equip_activation_with_eligibility_check / apply_slot_equip_activation_with_sprite /
#   dispatch_slot_equip_sprite_by_field6_type / enqueue_equip_chain_pair_sprite_validated /
#   scan_equip_chain_list_for_activation_sprite / enqueue_equip_chain_pair_sprite_if_eligible /
#   enqueue_equip_chain_dual_slot_sprite_with_activation_scan /
#   enqueue_face_down_slot_sprite_attr / enqueue_hand_card_sprite_by_spell_type /
#   dispatch_equip_zone_sprite_and_activation / dispatch_equip_zone_sprite_banisher_of_the_light /
#   dispatch_equip_zone_sprite_banisher_lp_row2 / dispatch_equip_zone_sprite_banisher_with_count_check /
#   dispatch_equip_zone_sprite_banisher_with_spell_check / enqueue_equip_zone_sprite_direct /
#   dispatch_equip_zone_sprite_banisher_by_field_count / dispatch_equip_zone_sprite_banisher_lp_row1 /
#   render_equip_zone_sprite_with_chain_lp
#
# Sections:
#   A. EQ_SLOTS    -- 68 slots (all reuse or new constants; addresses ROM-verified)
#   B. REF_SLOTS   -- 1 slot
#   C. RENAME_SLOTS -- 0 slots
#   D. PLATE_REWRITES -- 8 functions (all substring replace, 21 token replacements)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).
# NOTE: FUNC_RENAME = 0 (no function renames in this segment).
# NOTE: Addresses verified via python struct.unpack_from on roms/2343.gba; several
#       proposal addresses were wrong (e.g. CID BST cluster, OAM_EQUIP_SLOT_SPRITE_P1,
#       CRASS_CLOWN, BLADE_RABBIT, SAMSARA). All corrected here.

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
#    All values verified against roms/2343.gba (python struct.unpack_from).
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # === enqueue_zone_card_sprite_attr_by_slot (0x0804394c) ===
    (0x08043994, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'zcsa_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043998, 0x0201c510, 'gDuelFieldSlots',              'zcsa_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x0804399c, 0x00008035, 'OAM_ZONE_CARD_SPRITE_P1',      'zcsa_pal_p1',
     'OAM_ZONE_CARD_SPRITE_P1=0x8035: reuse'),

    # === apply_slot_equip_activation_with_sprite (0x080439e0) ===
    (0x08043ad4, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'aseas_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043ad8, 0x0201c510, 'gDuelFieldSlots',              'aseas_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    # OAM bit-clear mask cluster
    (0x08043adc, 0xfffffdff, 'OAM_SPRITE_ATTR_CLR_BIT9',     'aseas_clr_bit9',
     'OAM_SPRITE_ATTR_CLR_BIT9=0xfffffdff: AND mask clears bit9 (player_side)'),
    (0x08043ae0, 0xffffc3ff, 'OAM_SPRITE_ATTR_CLR_BITS13_10','aseas_clr_bits13_10',
     'OAM_SPRITE_ATTR_CLR_BITS13_10=0xffffc3ff: AND mask clears bits[13:10]'),
    (0x08043ae4, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',        'aseas_clr_bit14',
     'SLOT_ACTIVE_BIT14_CLR=0xffffbfff: AND mask clears bit14'),
    (0x08043ae8, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',        'aseas_clr_bit15',
     'SLOT_ACTIVE_BIT15_CLR=0xffff7fff: AND mask clears bit15'),
    (0x08043aec, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',            'aseas_clr_bits8_0',
     'OAM_ATTR1_X_CLEAR=0xfffffe00: AND mask clears attr1 bits[8:0]'),
    (0x08043af0, 0xfffeffff, 'OAM_SPRITE_ATTR_CLR_BIT16',    'aseas_clr_bit16',
     'OAM_SPRITE_ATTR_CLR_BIT16=0xfffeffff: AND mask clears bit16 (flip flag)'),
    (0x08043af4, 0xfffdffff, 'OAM_SPRITE_ATTR_CLR_BIT17',    'aseas_clr_bit17',
     'OAM_SPRITE_ATTR_CLR_BIT17=0xfffdffff: AND mask clears bit17 (composite sprite flag)'),
    # OAM attr0 P1 for equip slot (ROM-verified: 0x08043af8=0x8034)
    (0x08043af8, 0x00008034, 'OAM_EQUIP_SLOT_SPRITE_P1',     'aseas_equip_slot_pal_p1',
     'OAM_EQUIP_SLOT_SPRITE_P1=0x8034: equip slot activation OAM attr0 P1 (bit15+0x34)'),
    # Card ID: Crass Clown branch A (ROM-verified: 0x08043b30=0x1005)
    (0x08043b30, 0x00001005, 'CRASS_CLOWN_CID',              'aseas_cid_crass_clown',
     'CRASS_CLOWN_CID=0x1005: pw=93889755; card_0101; branch A'),
    # Card ID: branch B (ROM-verified: 0x08043b48=0x1048)
    (0x08043b48, 0x00001048, 'act_cid_1048_08043b48',        'aseas_cid_1048',
     'act_cid_1048_08043b48=0x1048: card_id branch B; NOT in card-stats.s; neutral name'),
    # Card ID: branch C (ROM-verified: 0x08043be8=0x1197)
    (0x08043be8, 0x00001197, 'act_cid_1197_08043be8',        'aseas_cid_1197',
     'act_cid_1197_08043be8=0x1197: card_id branch C; NOT in card-stats.s; neutral name'),
    # Second gDuelFieldSlots group
    (0x08043bf0, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'aseas_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043bf4, 0x0201c510, 'gDuelFieldSlots',              'aseas_gdfs_b',
     'gDuelFieldSlots=0x0201c510: reuse'),
    # Card ID: Blade Rabbit branch D (ROM-verified: 0x08043bec=0x1868)
    (0x08043bec, 0x00001868, 'BLADE_RABBIT_CID',             'aseas_cid_blade_rabbit',
     'BLADE_RABBIT_CID=0x1868: pw=58268433; card_1769; branch D'),

    # === dispatch_slot_equip_sprite_by_field6_type (0x08043c18) ===
    (0x08043c74, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'dses_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043c78, 0x0201c510, 'gDuelFieldSlots',              'dses_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x08043c7c, 0x0000135d, 'LIGHT_OF_INTERVENTION_CID',    'dses_cid_light_of_intervention',
     'LIGHT_OF_INTERVENTION_CID=0x135d: field_copies gate; reuse'),
    (0x08043cd4, 0x0201c510, 'gDuelFieldSlots',              'dses_gdfs_b',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x08043cd8, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'dses_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043d1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'dses_stride_c',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),

    # === enqueue_equip_chain_pair_sprite_validated (0x08043d20) ===
    (0x08043d80, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ecpsv_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043d84, 0x0201c510, 'gDuelFieldSlots',              'ecpsv_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x08043d88, 0xa5600000, 'EQUIP_SLOT_ACTIVE_TAG',        'ecpsv_equip_tag',
     'EQUIP_SLOT_ACTIVE_TAG=0xa5600000: slot_word<<19 == this -> equip slot live; reuse'),
    (0x08043d8c, 0x0000ffff, 'OAM_ATTR0_HIDDEN',             'ecpsv_no_pair',
     'OAM_ATTR0_HIDDEN=0xffff: no_pair sentinel from find_equip_chain_pair_across_field; C5 reuse'),

    # === scan_equip_chain_list_for_activation_sprite (0x08043d90) ===
    (0x08043e90, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'sclas_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043e94, 0x0201c510, 'gDuelFieldSlots',              'sclas_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x08043e98, 0x0201d9c0, 'gEquipNodePool',               'sclas_nodepool',
     'gEquipNodePool=0x0201d9c0: equip chain node pool; reuse'),
    (0x08043e9c, 0xa4e80000, 'EKIBYO_DRAKMORD_CID_SHIFTED',  'sclas_ekibyo_shifted',
     'EKIBYO_DRAKMORD_CID_SHIFTED=0xa4e80000: EKIBYO_DRAKMORD_CID(0x149d)<<19; type-match sentinel'),
    (0x08043ea0, 0x0000118a, 'AMEBA_CID',                    'sclas_ameba_range_base',
     'AMEBA_CID=0x118a: equip activation range base (0x118a..0x11c9); 28 raw ROM refs'),

    # === enqueue_equip_chain_pair_sprite_if_eligible (0x08043ea4) ===
    (0x08043f38, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ecpsie_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043f3c, 0x0201c510, 'gDuelFieldSlots',              'ecpsie_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x08043f40, 0x0000803d, 'OAM_EQUIP_CHAIN_PAIR_SPRITE_P1', 'ecpsie_chain_pair_pal_p1',
     'OAM_EQUIP_CHAIN_PAIR_SPRITE_P1=0x0000803d: equip chain pair sprite OAM attr0 P1'),

    # === enqueue_equip_chain_dual_slot_sprite_with_activation_scan (0x08043f44) ===
    (0x08043fec, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'ecdssas_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08043ff0, 0x0201c510, 'gDuelFieldSlots',              'ecdssas_gdfs',
     'gDuelFieldSlots=0x0201c510: reuse'),
    (0x08043ff4, 0x0000803e, 'OAM_EQUIP_CHAIN_DUAL_SPRITE_P1', 'ecdssas_chain_dual_pal_p1',
     'OAM_EQUIP_CHAIN_DUAL_SPRITE_P1=0x0000803e: equip chain dual-slot sprite OAM attr0 P1'),

    # === dispatch_equip_zone_sprite_and_activation (0x080440b8) ===
    # OAM_ZONE_EQUIP_SPRITE_P1 (ROM-verified: 0x08044148=0x8045)
    (0x08044148, 0x00008045, 'OAM_ZONE_EQUIP_SPRITE_P1',     'deza_zone_equip_pal_p1',
     'OAM_ZONE_EQUIP_SPRITE_P1=0x8045: zone equip shape sprite OAM attr0 P1 (bit15+0x45)'),
    # OAM_EQUIP_ZONE_SPRITE_P1 first slot (ROM-verified: 0x0804416c=0x8033)
    (0x0804416c, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',     'deza_equip_zone_pal_p1',
     'OAM_EQUIP_ZONE_SPRITE_P1=0x8033: equip zone sprite OAM attr0 P1 (bit15+0x33)'),
    # CID BST dispatch cluster (ROM-verified addresses)
    (0x080441e0, 0x000016f9, 'MANTICORE_OF_DARKNESS_CID',    'deza_cid_manticore',
     'MANTICORE_OF_DARKNESS_CID=0x16f9: pw=77121851; card_1458; BST root'),
    (0x080441e4, 0x000013e3, 'ARCHFIEND_OF_GILFER_CID',      'deza_cid_archfiend_of_gilfer',
     'ARCHFIEND_OF_GILFER_CID=0x13e3: pw=50287060; card_0853; BST node'),
    (0x080441e8, 0x000011bc, 'MINAR_CID',                    'deza_cid_minar',
     'MINAR_CID=0x11bc: pw=32539892; card_0444; BST node'),
    (0x080441f8, 0x000012a2, 'SKULL_MARK_LADYBUG_CID',       'deza_cid_skull_mark_ladybug',
     'SKULL_MARK_LADYBUG_CID=0x12a2: pw=64306248; card_0626; BST node'),
    (0x08044214, 0x00001655, 'FEAR_FROM_THE_DARK_CID',       'deza_cid_fear',
     'FEAR_FROM_THE_DARK_CID=0x1655: pw=34193084; card_1325; BST node'),
    (0x08044218, 0x000014a5, 'MAKYURA_THE_DESTRUCTOR_CID',   'deza_cid_makyura',
     'MAKYURA_THE_DESTRUCTOR_CID=0x14a5: pw=21593977; card_0991; BST node'),
    (0x0804421c, 0x00001653, 'DESPAIR_FROM_THE_DARK_CID',    'deza_cid_despair',
     'DESPAIR_FROM_THE_DARK_CID=0x1653: pw=71200730; card_1323; BST node'),
    (0x0804422c, 0x00001687, 'OUTSTANDING_DOG_MARRON_CID',   'deza_cid_outstanding_dog_marron',
     'OUTSTANDING_DOG_MARRON_CID=0x1687: pw=11548522; card_1364; BST node'),
    (0x08044254, 0x00001828, 'ROC_FROM_THE_VALLEY_OF_HAZE_CID', 'deza_cid_roc',
     'ROC_FROM_THE_VALLEY_OF_HAZE_CID=0x1828: pw=28143906; card_1708; BST node'),
    (0x08044264, 0x0000179a, 'NIGHT_ASSAILANT_CID',          'deza_cid_night_assailant',
     'NIGHT_ASSAILANT_CID=0x179a: pw=16226786; card_1585; BST node'),
    (0x08044278, 0x00001966, 'BROWW_HUNTSMAN_OF_DARK_WORLD_CID', 'deza_cid_broww',
     'BROWW_HUNTSMAN_OF_DARK_WORLD_CID=0x1966: pw=79126789; card_1972; BST node'),
    (0x0804428c, 0x00001968, 'SILLVA_WARLORD_OF_DARK_WORLD_CID', 'deza_cid_sillva',
     'SILLVA_WARLORD_OF_DARK_WORLD_CID=0x1968: pw=32619583; card_1974; BST node'),
    # SUPER_REJUVENATION_CID and GRAVEROBBER_CID
    (0x080443bc, 0x000014e2, 'SUPER_REJUVENATION_CID',       'deza_cid_super_rejuvenation',
     'SUPER_REJUVENATION_CID=0x14e2: pw=27770341; card_1042; arg to enqueue_sprite_attr_type11'),
    (0x080443c0, 0x00001379, 'GRAVEROBBER_CID',              'deza_cid_graverobber',
     'GRAVEROBBER_CID=0x1379: pw=61705417; card_0789; arg to find_effect_node_in_zone'),

    # === dispatch_equip_zone_sprite_banisher_of_the_light (0x080443c4) ===
    (0x08044408, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',    'botl_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: pw=61528025; card_0729; count_field_copies_of_card arg'),

    # === dispatch_equip_zone_sprite_banisher_lp_row2 (0x0804440c) ===
    (0x08044448, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',    'botl_lp_row2_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: reuse; count_field_copies_of_card arg'),

    # === dispatch_equip_zone_sprite_banisher_with_count_check (0x0804444c) ===
    (0x08044488, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',    'botl_count_check_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: reuse; count_field_copies_of_card arg'),

    # === dispatch_equip_zone_sprite_banisher_with_spell_check (0x0804448c) ===
    (0x0804452c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',    'botl_spell_check_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: reuse; count_field_copies_of_card arg'),
    # SAMSARA_CID (ROM-verified: 0x08044530=0x19da)
    (0x08044530, 0x000019da, 'SAMSARA_CID',                  'botl_spell_check_cid_samsara',
     'SAMSARA_CID=0x19da: pw=44182827; card_2061; second-card check'),
    # Only one PLAYER_BLOCK_STRIDE slot in this fn (ROM-verified: 0x08044534=0x868)
    (0x08044534, 0x00000868, 'PLAYER_BLOCK_STRIDE',          'botl_spell_check_stride',
     'PLAYER_BLOCK_STRIDE=0x868: reuse'),
    (0x08044538, 0x0201c600, 'gP1FieldArrayCBase',           'botl_spell_check_field_c',
     'gP1FieldArrayCBase=0x0201c600: field array C base (zone=0xb); reuse'),
    (0x0804453c, 0x000014e2, 'SUPER_REJUVENATION_CID',       'botl_spell_check_cid_super_rejuv',
     'SUPER_REJUVENATION_CID=0x14e2: reuse; second-card check'),

    # === enqueue_equip_zone_sprite_direct (0x08044540) ===
    # OAM_EQUIP_ZONE_SPRITE_P1 second slot (ROM-verified: 0x080445a0=0x8033)
    (0x080445a0, 0x00008033, 'OAM_EQUIP_ZONE_SPRITE_P1',     'eezsd_equip_zone_pal_p1',
     'OAM_EQUIP_ZONE_SPRITE_P1=0x8033: equip zone sprite OAM attr0 P1 (bit15+0x33); reuse'),

    # === dispatch_equip_zone_sprite_banisher_by_field_count (0x080445a4) ===
    (0x080445d4, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',    'botl_field_count_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: reuse; count_field_copies_of_card arg'),

    # === dispatch_equip_zone_sprite_banisher_lp_row1 (0x080445d8) ===
    (0x08044614, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',    'botl_lp_row1_cid_banisher',
     'BANISHER_OF_THE_LIGHT_CID=0x1332: reuse; count_field_copies_of_card arg'),

    # === render_equip_zone_sprite_with_chain_lp (0x08044618) ===
    (0x08044670, 0x00001379, 'GRAVEROBBER_CID',              'rezslp_cid_graverobber',
     'GRAVEROBBER_CID=0x1379: reuse; find_effect_node_in_zone arg'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # enqueue_hand_card_sprite_by_spell_type: reads gP1LifePoints pointer
    (0x080440ac, 0x0201c4e0, 'gP1LifePoints', 'ptr_gp1lp_440ac',
     'gP1LifePoints=0x0201c4e0: ewram.inc:79; read for hand slot array base'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: none in Seg-6
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: 8 functions, 21 substring replacements (all ASCII plates)
# ---------------------------------------------------------------------------
PLATE_REWRITES = [

    # --- invoke_equip_activation_with_zero_flag (0x080439a0) ---
    # 5 FUN_ tokens
    (0x080439a0, 'substr', 'FUN_08043c18',  'dispatch_slot_equip_sprite_by_field6_type'),
    (0x080439a0, 'substr', 'FUN_0808df3c',  'scan_all_slots_for_max_equip_match'),
    (0x080439a0, 'substr', 'FUN_0809b178',  'update_equip_activation_display_state'),
    (0x080439a0, 'substr', 'FUN_0809b7e0',  'update_equip_zone_sprite_by_state'),
    (0x080439a0, 'substr', 'FUN_0809eb54',  'scan_monster_zone_slots_for_equip_activation_reserved_icid_g'),

    # --- enqueue_equip_chain_pair_sprite_validated (0x08043d20) ---
    # 2 FUN_ tokens
    (0x08043d20, 'substr', 'FUN_08043ea4',  'enqueue_equip_chain_pair_sprite_if_eligible'),
    (0x08043d20, 'substr', 'FUN_08043f44',  'enqueue_equip_chain_dual_slot_sprite_with_activation_scan'),

    # --- scan_equip_chain_list_for_activation_sprite (0x08043d90) ---
    # 4 FUN_ tokens
    (0x08043d90, 'substr', 'FUN_08043ea4',  'enqueue_equip_chain_pair_sprite_if_eligible'),
    (0x08043d90, 'substr', 'FUN_08043f44',  'enqueue_equip_chain_dual_slot_sprite_with_activation_scan'),
    (0x08043d90, 'substr', 'FUN_08043d20',  'enqueue_equip_chain_pair_sprite_validated'),
    (0x08043d90, 'substr', 'FUN_08045298',  'enqueue_equip_set_slot_sprite_by_zone_col'),

    # --- dispatch_equip_zone_sprite_and_activation (0x080440b8) ---
    # 1 FUN_ token
    (0x080440b8, 'substr', 'FUN_080443c4',  'dispatch_equip_zone_sprite_banisher_of_the_light'),

    # --- dispatch_equip_zone_sprite_banisher_with_count_check (0x0804444c) ---
    # 1 FUN_ token
    (0x0804444c, 'substr', 'FUN_080a70d8',  'tick_equip_banisher_sprite_phase_by_combined_index'),

    # --- dispatch_equip_zone_sprite_banisher_with_spell_check (0x0804448c) ---
    # 2 FUN_ tokens
    (0x0804448c, 'substr', 'FUN_08086cdc',  'dispatch_equip_zone_activation_state'),
    (0x0804448c, 'substr', 'FUN_080a6cc8',  'tick_equip_multi_target_phase_with_slot_confirm'),

    # --- enqueue_equip_zone_sprite_direct (0x08044540) ---
    # 1 FUN_ token
    (0x08044540, 'substr', 'FUN_08044618',  'render_equip_zone_sprite_with_chain_lp'),

    # --- render_equip_zone_sprite_with_chain_lp (0x08044618) ---
    # 1 FUN_ token
    (0x08044618, 'substr', 'FUN_080583bc',  'tick_equip_bitmap_and_lp_chain_sprite_seq'),
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

def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] REF 0x%08x -> %s(0x%x) slot=%s" % (slot_addr, gas_label, target_addr, slot_label))
        return

    # Create target label if needed
    tgt_syms = sym_tbl.getSymbols(a_target)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    # Create slot label
    slot_syms = sym_tbl.getSymbols(a_slot)
    slot_names = [s.getName() for s in slot_syms]
    if slot_label not in slot_names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # Add DATA reference slot -> target
    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    # Set primary symbol to slot_label
    for sym in sym_tbl.getSymbols(a_slot):
        if sym.getName() == slot_label:
            sym.setPrimary()
            break

    if eol:
        cu = listing.getCodeUnitAt(a_slot)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> %s (gas=%s slot=%s)" % (slot_addr, hex(target_addr), gas_label, slot_label))

def _apply_plate_substr(func_addr, old_text, new_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_substr 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_substr 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_substr 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_SUBSTR 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF04Seg6Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-6: 0x0804394c..0x08044674, 20 fn, 69 slots")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_entries=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

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
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS (none)
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    print("  RENAME done: 0")

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d entries) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for entry in PLATE_REWRITES:
        func_addr, mode = entry[0], entry[1]
        if mode == 'substr':
            _apply_plate_substr(func_addr, entry[2], entry[3])
        else:
            print("[ERR] unknown mode '%s' for 0x%08x" % (mode, func_addr))
        plate_ok += 1
    print("  PLATE done: %d entries" % plate_ok)

    print("\n=== RefineF04Seg6Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_entries=%d (DRY=%s)" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), DRY))

main()
