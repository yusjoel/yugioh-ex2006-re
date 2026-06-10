# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg4Slots.py -- file 02 Seg-4 (0x0802fd00..0x080309b8)
#   find/check/count/scan equip chain node + BST card-ID dispatch cluster (23 fn, 136 slots)
#   find_chain_node_by_dual_halfword / find_effect_node_in_zone / check_node_in_slot_chain /
#   check_slot_has_node_by_card_id / check_value_in_slot_chain_zone_entity /
#   get_node_entity_id_in_slot / get_zone_node_entity_hword_by_card_and_type /
#   get_zone_node_entity_hword_or_miss / check_zone_card_id_in_node_pool /
#   check_node_in_zone_idx_chain / get_entity_id_in_zone_idx_chain /
#   get_entity_id_in_zone_idx_chain_by_type / count_chain_by_card_id_in_zone_idx /
#   count_chain_by_card_id_and_type_in_zone_idx / scan_equip_node_pool_for_card_score /
#   find_equip_chain_node_by_pred / find_zone_node_by_card_id_match /
#   check_zone_card_special_state_by_field5 / count_set_bits_in_word /
#   get_card_equip_target_zone_cost / map_card_id_to_anim_type /
#   check_effect_slot_summon_path_eligible / check_effect_slot_is_equip_activatable
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (all reuse existing inc constants except ZONE_CHAIN_CARD_ID_OFF,
#                    POPCOUNT_MASK_* which are new in ewram.inc / bitops.inc)
#   B. REF_SLOTS  -- (empty: PTR_gP1LifePoints_* already have DATA refs from prior ops)
#   C. RENAME_SLOTS -- 90 slots: 8 PTR_ label renames + 1 sw-table ptr + 81 card-ID BST slots
#   D. PLATE_REWRITES -- 3 full ASCII rewrites (CJK plates) + 9 substring FUN_ fixes
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0, disasm=0 for this segment.
# NOTE: New constants: ewram.inc +ZONE_CHAIN_CARD_ID_OFF; new bitops.inc (8 POPCOUNT_MASK_*).
# NOTE: FUNC_RENAME=0; no CSV sync needed.

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
#    Slot label MUST differ from eq_name (avoids GAS PC-relative "value too big").
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, reuse, 14 slots) ---
    (0x0802fd44, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_chain_node_dual_player_stride', None),
    (0x0802fda4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_effect_node_zone_player_stride', None),
    (0x0802fdec, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_node_slot_chain_player_stride', None),
    (0x0802fe24, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_node_card_player_stride', None),
    (0x0802fe58, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_value_slot_zone_player_stride', None),
    (0x0802fe88, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'get_node_entity_slot_player_stride', None),
    (0x0802fec0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'get_zone_entity_hword_type_player_stride', None),
    (0x0802ff00, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'get_zone_entity_hword_miss_player_stride', None),
    (0x0803003c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_node_pred_player_stride', None),
    (0x08030080, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_zone_node_card_player_stride', None),
    (0x08030114, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_card_field5_player_stride_a', None),
    (0x08030154, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_card_field5_player_stride_b', None),
    (0x080301d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_card_field5_player_stride_c', None),
    (0x08030204, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_card_field5_player_stride_d', None),

    # --- gDuelFieldSlots = 0x0201c510 (ewram.inc, reuse, 12 slots) ---
    (0x0802fd48, 0x0201c510, 'gDuelFieldSlots',
     'find_chain_node_dual_field_slots', None),
    (0x0802fda8, 0x0201c510, 'gDuelFieldSlots',
     'find_effect_node_zone_field_slots', None),
    (0x0802fdf0, 0x0201c510, 'gDuelFieldSlots',
     'check_node_slot_chain_field_slots', None),
    (0x0802fe28, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_node_card_field_slots', None),
    (0x0802fe5c, 0x0201c510, 'gDuelFieldSlots',
     'check_value_slot_zone_field_slots', None),
    (0x0802fe8c, 0x0201c510, 'gDuelFieldSlots',
     'get_node_entity_slot_field_slots', None),
    (0x0802fec4, 0x0201c510, 'gDuelFieldSlots',
     'get_zone_entity_hword_type_field_slots', None),
    (0x0802ff04, 0x0201c510, 'gDuelFieldSlots',
     'get_zone_entity_hword_miss_field_slots', None),
    (0x08030040, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_node_pred_field_slots', None),
    (0x08030084, 0x0201c510, 'gDuelFieldSlots',
     'find_zone_node_card_field_slots', None),
    (0x08030118, 0x0201c510, 'gDuelFieldSlots',
     'check_zone_card_field5_field_slots_a', None),
    (0x08030158, 0x0201c510, 'gDuelFieldSlots',
     'check_zone_card_field5_field_slots_b', None),

    # --- EQUIP_NODE_BASE_OFFSET = 0x000014b0 (duel_field.inc, reuse, 3 slots) ---
    (0x0802fd4c, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_chain_node_dual_equip_off', None),
    (0x0802fdac, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_effect_node_zone_equip_off', None),
    (0x08030044, 0x000014b0, 'EQUIP_NODE_BASE_OFFSET',
     'find_equip_node_pred_equip_off', None),

    # --- gEquipNodePool = 0x0201d9c0 (ewram.inc, reuse, 2 slots) ---
    (0x08030088, 0x0201d9c0, 'gEquipNodePool',
     'find_equip_node_pred_pool', None),
    (0x080300c0, 0x0201d9c0, 'gEquipNodePool',
     'scan_equip_pool_card_score_pool', None),

    # --- ZONE_CHAIN_CARD_ID_OFF = 0x000010e2 (ewram.inc NEW, 6 slots) ---
    (0x0802ff30, 0x000010e2, 'ZONE_CHAIN_CARD_ID_OFF',
     'check_zone_card_pool_card_id_off', None),
    (0x0802ff54, 0x000010e2, 'ZONE_CHAIN_CARD_ID_OFF',
     'check_node_zone_idx_card_id_off', None),
    (0x0802ff78, 0x000010e2, 'ZONE_CHAIN_CARD_ID_OFF',
     'get_entity_zone_idx_card_id_off', None),
    (0x0802ffa4, 0x000010e2, 'ZONE_CHAIN_CARD_ID_OFF',
     'get_entity_zone_idx_type_card_id_off', None),
    (0x0802ffcc, 0x000010e2, 'ZONE_CHAIN_CARD_ID_OFF',
     'count_chain_card_id_zone_card_id_off', None),
    (0x0802ffec, 0x000010e2, 'ZONE_CHAIN_CARD_ID_OFF',
     'count_chain_card_id_type_zone_card_id_off', None),

    # --- OAM_ATTR0_HIDDEN = 0x0000ffff (oam_attr.inc, reuse, 1 slot) ---
    # Used as MASK_LO16 in count_set_bits_in_word step5 final merge
    (0x08030268, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'count_set_bits_mask_lo16',
     'MASK_LO16 (popcount step5: lo 16 bits)'),

    # --- POPCOUNT_MASK_* (bitops.inc NEW, 8 slots) ---
    (0x08030248, 0xaaaaaaaa, 'POPCOUNT_MASK_ODD',
     'count_set_bits_mask_odd', None),
    (0x0803024c, 0x55555555, 'POPCOUNT_MASK_EVEN',
     'count_set_bits_mask_even', None),
    (0x08030250, 0xcccccccc, 'POPCOUNT_MASK_HI2',
     'count_set_bits_mask_hi2', None),
    (0x08030254, 0x33333333, 'POPCOUNT_MASK_LO2',
     'count_set_bits_mask_lo2', None),
    (0x08030258, 0xf0f0f0f0, 'POPCOUNT_MASK_HI4',
     'count_set_bits_mask_hi4', None),
    (0x0803025c, 0x0f0f0f0f, 'POPCOUNT_MASK_LO4',
     'count_set_bits_mask_lo4', None),
    (0x08030260, 0xff00ff00, 'POPCOUNT_MASK_HI8',
     'count_set_bits_mask_hi8', None),
    (0x08030264, 0x00ff00ff, 'POPCOUNT_MASK_LO8',
     'count_set_bits_mask_lo8', None),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: empty -- all PTR_gP1LifePoints_* already have .word gP1LifePoints
#    DATA refs established by prior Ghidra operations.
# ---------------------------------------------------------------------------
REF_SLOTS = [
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    90 slots: 8 PTR_gP1LifePoints_* renames + 1 sw-table + 81 card-ID BST slots
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # --- PTR_gP1LifePoints_* slot label renames (8 slots) ---
    (0x0802ff2c, 'check_zone_card_id_in_node_pool_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0802ff50, 'check_node_in_zone_idx_chain_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0802ff74, 'get_entity_id_in_zone_idx_chain_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0802ffa0, 'get_entity_id_in_zone_idx_chain_by_type_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0802ffc8, 'count_chain_by_card_id_in_zone_idx_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0802ffe8, 'count_chain_by_card_id_and_type_in_zone_idx_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080301d0, 'check_zone_card_special_state_field5_range_b_p1lp',
     'gP1LifePoints for bit5 check'),
    (0x08030200, 'check_zone_card_special_state_field5_range_a_p1lp',
     'gP1LifePoints for bit5 check'),

    # --- switch table base pointer (1 slot) ---
    (0x080302f4, 'get_card_equip_target_zone_cost_sw_table',
     'ptr to switchdataD_080302f8'),

    # --- check_zone_card_special_state_by_field5 card-ID BST slots (8 slots) ---
    (0x0803015c, 'check_zone_card_special_field5_cid_14b2', None),
    (0x08030160, 'check_zone_card_special_field5_cid_1243', None),
    (0x08030164, 'check_zone_card_special_field5_cid_1103', None),
    (0x08030174, 'check_zone_card_special_field5_cid_137d', None),
    (0x0803018c, 'check_zone_card_special_field5_cid_17b7', None),
    (0x08030190, 'check_zone_card_special_field5_cid_14fc', None),
    (0x08030194, 'check_zone_card_special_field5_cid_16a2', None),
    (0x080301a8, 'check_zone_card_special_field5_cid_184b', None),

    # --- get_card_equip_target_zone_cost card-ID BST slots (32 slots) ---
    (0x08030298, 'get_equip_zone_cost_cid_1774', None),
    (0x0803029c, 'get_equip_zone_cost_cid_158a', None),
    (0x080302ac, 'get_equip_zone_cost_cid_15fc', None),
    (0x080302c8, 'get_equip_zone_cost_cid_17d4', None),
    (0x080302f0, 'get_equip_zone_cost_cid_183a', None),
    (0x08030354, 'get_equip_zone_cost_cid_1409', None),
    (0x08030358, 'get_equip_zone_cost_cid_12f2', None),
    (0x08030360, 'get_equip_zone_cost_cid_12d0', None),
    (0x08030384, 'get_equip_zone_cost_cid_1330', None),
    (0x08030398, 'get_equip_zone_cost_cid_138e', None),
    (0x080303a0, 'get_equip_zone_cost_cid_13ee', None),
    (0x080303c8, 'get_equip_zone_cost_cid_167b', None),
    (0x080303cc, 'get_equip_zone_cost_cid_14eb', None),
    (0x080303e0, 'get_equip_zone_cost_cid_153d', None),
    (0x080303e8, 'get_equip_zone_cost_cid_15a6', None),
    (0x08030408, 'get_equip_zone_cost_cid_1853_a', None),
    (0x08030410, 'get_equip_zone_cost_cid_184b_b', None),
    (0x08030428, 'get_equip_zone_cost_cid_192d', None),
    (0x08030430, 'get_equip_zone_cost_cid_19b4', None),
    (0x08030448, 'get_equip_zone_cost_cid_14a7', None),
    (0x0803044c, 'get_equip_zone_cost_cid_12ba', None),
    (0x08030460, 'get_equip_zone_cost_cid_195e', None),
    (0x08030480, 'get_equip_zone_cost_cid_13a7', None),
    (0x08030484, 'get_equip_zone_cost_cid_111b', None),
    (0x08030498, 'get_equip_zone_cost_cid_1853_c', None),
    (0x0803049c, 'get_equip_zone_cost_cid_1493', None),
    (0x080304a4, 'get_equip_zone_cost_cid_1883', None),
    (0x080304b4, 'get_equip_zone_cost_cid_151b', None),
    (0x080304cc, 'get_equip_zone_cost_cid_138f', None),
    (0x080304dc, 'get_equip_zone_cost_cid_17ca', None),
    (0x080304e0, 'get_equip_zone_cost_cid_19b6', None),
    (0x080304f4, 'get_equip_zone_cost_cid_1352', None),

    # --- map_card_id_to_anim_type card-ID BST slots (33 slots) ---
    (0x0803054c, 'map_anim_type_cid_15f1', None),
    (0x08030550, 'map_anim_type_cid_1406', None),
    (0x08030554, 'map_anim_type_cid_12ff', None),
    (0x08030558, 'map_anim_type_cid_1086', None),
    (0x08030568, 'map_anim_type_cid_117b', None),
    (0x0803057c, 'map_anim_type_cid_12e6', None),
    (0x08030594, 'map_anim_type_cid_12eb', None),
    (0x080305c4, 'map_anim_type_cid_134d', None),
    (0x080305cc, 'map_anim_type_cid_132d', None),
    (0x080305e0, 'map_anim_type_cid_137c', None),
    (0x080305e8, 'map_anim_type_cid_13b5', None),
    (0x08030614, 'map_anim_type_cid_1517', None),
    (0x08030624, 'map_anim_type_cid_148f', None),
    (0x08030640, 'map_anim_type_cid_14df', None),
    (0x08030650, 'map_anim_type_cid_14e1', None),
    (0x08030670, 'map_anim_type_cid_15a8', None),
    (0x08030680, 'map_anim_type_cid_1541', None),
    (0x080306a4, 'map_anim_type_cid_15d7', None),
    (0x080306ac, 'map_anim_type_cid_15ef', None),
    (0x080306e4, 'map_anim_type_cid_17a8', None),
    (0x080306f4, 'map_anim_type_cid_161e', None),
    (0x08030708, 'map_anim_type_cid_167c', None),
    (0x08030718, 'map_anim_type_cid_16a6', None),
    (0x08030738, 'map_anim_type_cid_1708', None),
    (0x08030748, 'map_anim_type_cid_16dd', None),
    (0x08030764, 'map_anim_type_cid_174c', None),
    (0x0803077c, 'map_anim_type_cid_1753', None),
    (0x080307b0, 'map_anim_type_cid_17e2', None),
    (0x080307c8, 'map_anim_type_cid_188d', None),
    (0x080307dc, 'map_anim_type_cid_18de', None),
    (0x080307fc, 'map_anim_type_cid_1969', None),
    (0x08030820, 'map_anim_type_cid_19b0', None),
    (0x08030834, 'map_anim_type_cid_19c8', None),

    # --- check_effect_slot_summon_path_eligible card-ID BST slots (8 slots) ---
    (0x080308e0, 'check_summon_path_cid_1534', None),
    (0x080308e4, 'check_summon_path_cid_133b', None),
    (0x080308e8, 'check_summon_path_cid_1449', None),
    (0x080308fc, 'check_summon_path_cid_1452', None),
    (0x08030918, 'check_summon_path_cid_179a', None),
    (0x0803091c, 'check_summon_path_cid_1549', None),
    (0x08030920, 'check_summon_path_cid_1686', None),
    (0x08030934, 'check_summon_path_cid_187f', None),

]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES:
#    Part 1: Full plate replacements (3 CJK plates -> ASCII)
#      (func_addr, None, new_plate_text)
#    Part 2: Substring FUN_ fixes (9 plates, multiple entries per plate)
#      (func_addr, old_text, new_text)
# ---------------------------------------------------------------------------

# Full plate rewrites: (func_addr, None, new_ascii_plate)
PLATE_FULL = [

    # PLATE-1: get_zone_node_entity_hword_by_card_and_type (0x0802fe98)
    # Current plate has Chinese text -- replace entirely with ASCII
    (0x0802fe98,
     "Called by scan_equip_zone_for_super_rejuvenation_activation (0x0809d374).\n"
     "Computes slot_struct_addr = gDuelFieldSlots + slot_type*20*4 + (r0&1)*0x868.\n"
     "Reads [slot+0xa] chain head halfword; calls find_node_by_value_and_zone_type(head, zone_id, type_flag).\n"
     "On hit: returns node[+4] hword (entity). On miss: returns -1.\n"
     "r0=packed_player_id, r1=slot_type, r2=zone_id, r3=type_flag.\n"
     "Returns u16 entity hword or -1. No external writes.\n"
     "Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, node_entity_offset=0x4."),

    # PLATE-2: get_zone_node_entity_hword_or_miss (0x0802fed4)
    # Current plate has Chinese and stale FUN_0809bfd4 -- replace entirely with ASCII
    (0x0802fed4,
     "Called by scan_equip_zone_for_entity_sprite_and_activation (0x0809f538) and\n"
     "dispatch_equip_action_sprite_by_phase_state (0x0809bfd4).\n"
     "Computes slot_struct_addr = gDuelFieldSlots + slot_type*20*4 + (r0&1)*0x868.\n"
     "Reads [struct+0xa] chain head halfword; calls find_node_by_value_zone_entity(head, zone_id, -1).\n"
     "On hit: returns node[+4] hword (entity). On miss: returns -1 (r4 sentinel).\n"
     "r0=packed_player_id, r1=slot_type, r2=zone_id.\n"
     "Returns u16 entity hword or -1. No external writes.\n"
     "Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, miss_sentinel=-1."),

    # PLATE-3: scan_equip_node_pool_for_card_score (0x0802fff0)
    # Current plate has Chinese and stale FUN_08090a78 -- replace entirely with ASCII
    (0x0802fff0,
     "Called by build_equip_candidate_score_table (0x08090a78) (2 callsites).\n"
     "r0=player_side [0..1], r1=slot_idx [0..4], r2=card_id_filter [0..0x1fff].\n"
     "Computes gDuelFieldSlots[player*0x868+slot*0x14] base; reads [+0xa] chain head halfword.\n"
     "If head==0 returns 0. Else traverses gEquipNodePool (stride 8) while head!=0:\n"
     "  checks node[+2] low 4 bits <= 5; if node[+0]==card_id_filter accumulates node[+4] to sum.\n"
     "  Advances via node[+6] halfword.\n"
     "Returns r0=u32 accumulated score. Pure read, no external writes.\n"
     "Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, gEquipNodePool=0x0201d9c0,\n"
     "node_stride=8, node_type_max=5, chain_head_offset=0xa."),

]

# Substring FUN_ fixes: (func_addr, old_text, new_text)
PLATE_SUBS = [

    # find_effect_node_in_zone (0x0802fd60)
    (0x0802fd60, 'FUN_08033730', 'check_slot_card_can_be_equipped'),

    # check_node_in_slot_chain (0x0802fdc0)
    (0x0802fdc0, 'FUN_0802fd60', 'find_effect_node_in_zone'),

    # check_zone_card_id_in_node_pool (0x0802ff10) -- 2 replacements
    (0x0802ff10, 'FUN_0804559c', 'dispatch_card_effect_sprite_render_by_card_id'),
    (0x0802ff10, 'FUN_0805e3a8', 'check_equip_slot_eligible_with_pool_and_hand_slot'),

    # find_equip_chain_node_by_pred (0x08030048)
    (0x08030048, 'FUN_0810e5e4', 'invoke_r7'),

    # find_zone_node_by_card_id_match (0x0803009c) -- 2 replacements
    (0x0803009c, 'FUN_0810e5e4', 'invoke_r7'),
    (0x0803009c, 'FUN_0804559c', 'dispatch_card_effect_sprite_render_by_card_id'),

    # check_zone_card_special_state_by_field5 (0x080300d4) -- 2 replacements
    (0x080300d4, 'FUN_0804659c', 'check_slot_equip_target_eligibility'),
    (0x080300d4, 'FUN_08046bd0', 'dispatch_card_effect_zone_action_by_card_id'),

    # count_set_bits_in_word (0x08030208)
    (0x08030208, 'FUN_08059a78', 'tick_equip_zone_bitmap_slot_display_seq'),

    # map_card_id_to_anim_type (0x08030500) -- 3 replacements
    (0x08030500, 'FUN_08036870', 'check_card_equip_eligible_for_slot'),
    (0x08030500, 'FUN_0805d118', 'check_equip_zone_effect_eligible_by_card_id'),
    (0x08030500, 'FUN_080b40d8', 'check_slot_card_is_equippable'),

    # check_effect_slot_is_equip_activatable (0x08030988)
    (0x08030988, 'FUN_08061688', 'commit_equip_effect_node_zone_match'),

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

def _apply_plate_full(func_addr, new_plate):
    """Replace entire plate comment at func_addr with new_plate (pure ASCII)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_full 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] PLATE_FULL 0x%08x (len=%d)" % (func_addr, len(new_plate)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PLF] 0x%08x: plate replaced (len=%d)" % (func_addr, len(new_plate)))

def _apply_plate_sub(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment at func_addr."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_sub 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_sub 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_sub 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_SUB 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PLS] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg4Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-4: 0x0802fd00..0x080309b8, 23 fn, 136 slots")
    print("  EQ=%d REF=%d RENAME=%d PLATE_FULL=%d PLATE_SUBS=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL), len(PLATE_SUBS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS (empty)
    print("\n--- B. REF_SLOTS (%d) [empty] ---" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_FULL (3 full plate rewrites)
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    # D. PLATE_SUBS (substring FUN_ fixes)
    print("\n--- D. PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
    for func_addr, old_text, new_text in PLATE_SUBS:
        _apply_plate_sub(func_addr, old_text, new_text)

    print("\n=== RefineF02Seg4Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE_FULL=%d  PLATE_SUBS=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL), len(PLATE_SUBS)))

main()
