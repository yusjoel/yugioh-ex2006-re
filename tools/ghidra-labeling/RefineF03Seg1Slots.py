# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg1Slots.py -- file 03 Seg-1 (0x08035f54..0x08036a78)
#   equip node link by card_type + slot eligibility checks (13 fn, 84 slots)
#   link_equip_node_by_card_type_check / check_slot_equip_eligibility_by_type /
#   check_slot_field_zone_card_eligible / check_slot_equip_whitelist_with_monster_space /
#   check_slot_card_effect_eligibility / query_slot_effect_eligibility_nonzero /
#   check_slot_card_fieldspell_eligibility / check_slot_fieldspell_eligible_by_side /
#   query_slot_card_type_eligibility / check_zone_slot_equip_prerequisites /
#   check_card_equip_eligible_for_slot / check_equip_eligibility_via_request_buf /
#   check_slot_card_special_activation_eligible
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (81 slots; reuse existing + new inc constants)
#   B. RENAME_SLOTS -- plain rename + EOL (3 gap-CID + sentinel slots; pure ASCII)
#   C. PLATE_FULL -- full plate rewrite for all 13 functions (pure ASCII, no FUN_)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: New constants (card_info.inc x35, ewram.inc x1, duel_field.inc x3) written
#       to constants/*.inc files separately (see B2 in refine pipeline).

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
#    Creates equate (value->name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 (2 PTR slots) ---
    (0x08035f8c, 0x0201c4e0, 'gP1LifePoints',
     'link_equip_node_card_type_lp_ptr', None),
    (0x080365c0, 0x0201c4e0, 'gP1LifePoints',
     'check_effect_elig_lp_ptr', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (15 slots) ---
    (0x08035f90, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'link_equip_node_card_type_stride', None),
    (0x08035fcc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'link_equip_node_card_type_stride_b', None),
    (0x08036010, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'link_equip_node_card_type_stride_c', None),
    (0x08036094, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_elig_stride', None),
    (0x08036288, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_elig_0a_stride', None),
    (0x080362f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_elig_0a_stride_b', None),
    (0x080363a8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_field_zone_stride', None),
    (0x08036414, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_field_zone_stride_b', None),
    (0x080364a0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_equip_whitelist_stride', None),
    (0x08036500, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_effect_elig_stride', None),
    (0x080365c4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_effect_elig_stride_b', None),
    (0x080366d8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_fieldspell_elig_stride', None),
    (0x08036840, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_prereq_stride', None),
    (0x080368d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_equip_eligible_stride', None),
    (0x08036a64, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_special_act_stride', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (10 slots) ---
    (0x08035fd0, 0x0201c510, 'gDuelFieldSlots',
     'link_equip_node_card_type_slots', None),
    (0x08036098, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_equip_elig_slots', None),
    (0x080362fc, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_equip_elig_0a_slots', None),
    (0x08036418, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_field_zone_slots', None),
    (0x080364a4, 0x0201c510, 'gDuelFieldSlots',
     'check_equip_whitelist_slots', None),
    (0x08036504, 0x0201c510, 'gDuelFieldSlots',
     'check_effect_elig_slots', None),
    (0x080366dc, 0x0201c510, 'gDuelFieldSlots',
     'check_fieldspell_elig_slots', None),
    (0x08036844, 0x0201c510, 'gDuelFieldSlots',
     'check_zone_prereq_slots', None),
    (0x080368d8, 0x0201c510, 'gDuelFieldSlots',
     'check_equip_eligible_slots', None),
    (0x08036a68, 0x0201c510, 'gDuelFieldSlots',
     'check_special_act_slots', None),

    # --- ewram.inc: gEquipNodePool = 0x0201d9c0 (3 slots) ---
    (0x080360a0, 0x0201d9c0, 'gEquipNodePool',
     'check_slot_equip_elig_pool', None),
    (0x0803628c, 0x0201d9c0, 'gEquipNodePool',
     'check_slot_equip_elig_0a_pool', None),
    (0x080363ac, 0x0201d9c0, 'gEquipNodePool',
     'check_slot_field_zone_pool', None),

    # --- duel_field.inc: NODE_POOL_NEG_OFFSET = 0xffffeb50 (2 slots) ---
    (0x08036290, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'check_slot_equip_elig_0a_neg_off', None),
    (0x080363b0, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'check_slot_field_zone_neg_off', None),

    # --- ewram.inc: gDuelFieldSlotState = 0x0201c520 (1 slot) ---
    (0x080363b4, 0x0201c520, 'gDuelFieldSlotState',
     'check_slot_field_zone_slot_state', None),

    # --- card_info.inc: UMI_CARD_ID = 0x000010f4 (1 slot) ---
    (0x080365bc, 0x000010f4, 'UMI_CARD_ID',
     'check_effect_elig_umi_cid', None),

    # --- card_info.inc: LEGENDARY_FISHERMAN_CID = 0x000013cd (1 slot; reuse) ---
    (0x08036540, 0x000013cd, 'LEGENDARY_FISHERMAN_CID',
     'check_effect_elig_cid_b', None),

    # --- card_info.inc: GUARDIAN_KAYEST_CID = 0x0000164e (1 slot; reuse) ---
    (0x08036558, 0x0000164e, 'GUARDIAN_KAYEST_CID',
     'check_effect_elig_cid_d', None),

    # --- card_info.inc: EHERO_AVIAN_CID = 0x000018a6 (new) ---
    (0x08035fd4, 0x000018a6, 'EHERO_AVIAN_CID',
     'link_equip_node_card_type_cid_a', None),

    # --- card_info.inc: CHAIN_THRASHER_CID = 0x000019c1 (new) ---
    (0x0803600c, 0x000019c1, 'CHAIN_THRASHER_CID',
     'link_equip_node_card_type_cid_b', None),

    # --- card_info.inc: ROYAL_COMMAND_CID = 0x0000148e (new) ---
    (0x08036120, 0x0000148e, 'ROYAL_COMMAND_CID',
     'check_slot_equip_elig_cid_a', None),

    # --- card_info.inc: FIEND_SKULL_DRAGON_CID = 0x000014da (new) ---
    (0x08036124, 0x000014da, 'FIEND_SKULL_DRAGON_CID',
     'check_slot_equip_elig_cid_b', None),

    # --- card_info.inc: POSSESSED_DARK_SOUL_CID = 0x000014b8 (new) ---
    (0x08036128, 0x000014b8, 'POSSESSED_DARK_SOUL_CID',
     'check_slot_equip_elig_cid_c', None),

    # --- card_info.inc: SNATCH_STEAL_CID = 0x00001322 (new) ---
    (0x0803612c, 0x00001322, 'SNATCH_STEAL_CID',
     'check_slot_equip_elig_cid_d', None),
    (0x08036304, 0x00001322, 'SNATCH_STEAL_CID',
     'check_slot_equip_elig_0a_cid_b', None),

    # --- card_info.inc: MAGIC_ARM_SHIELD_CID = 0x000012e2 (new) ---
    (0x08036140, 0x000012e2, 'MAGIC_ARM_SHIELD_CID',
     'check_slot_equip_elig_cid_e', None),

    # --- card_info.inc: CHANGE_OF_HEART_CID = 0x000012fc (new) ---
    (0x08036148, 0x000012fc, 'CHANGE_OF_HEART_CID',
     'check_slot_equip_elig_cid_f', None),

    # --- card_info.inc: MYSTIC_BOX_CID = 0x00001430 (new) ---
    (0x08036174, 0x00001430, 'MYSTIC_BOX_CID',
     'check_slot_equip_elig_cid_g', None),

    # --- card_info.inc: DARK_NECROFEAR_CID = 0x00001466 (new) ---
    (0x0803617c, 0x00001466, 'DARK_NECROFEAR_CID',
     'check_slot_equip_elig_cid_h', None),
    (0x08036300, 0x00001466, 'DARK_NECROFEAR_CID',
     'check_slot_equip_elig_0a_cid_a', None),

    # --- card_info.inc: BRAIN_JACKER_CID = 0x00001877 (new) ---
    (0x080361a0, 0x00001877, 'BRAIN_JACKER_CID',
     'check_slot_equip_elig_cid_i', None),
    (0x0803631c, 0x00001877, 'BRAIN_JACKER_CID',
     'check_slot_equip_elig_0a_cid_d', None),

    # --- card_info.inc: ENEMY_CONTROLLER_CID = 0x00001581 (new) ---
    (0x080361a4, 0x00001581, 'ENEMY_CONTROLLER_CID',
     'check_slot_equip_elig_cid_j', None),

    # --- card_info.inc: FALLING_DOWN_CID = 0x0000169a (new) ---
    (0x080361bc, 0x0000169a, 'FALLING_DOWN_CID',
     'check_slot_equip_elig_cid_k', None),
    (0x08036318, 0x0000169a, 'FALLING_DOWN_CID',
     'check_slot_equip_elig_0a_cid_c', None),

    # --- card_info.inc: OWNER_SEAL_CID = 0x00001857 (new) ---
    (0x080361c8, 0x00001857, 'OWNER_SEAL_CID',
     'check_slot_equip_elig_cid_l', None),

    # --- card_info.inc: RESHEF_THE_DARK_BEING_CID = 0x000018c6 (new) ---
    (0x080361f4, 0x000018c6, 'RESHEF_THE_DARK_BEING_CID',
     'check_slot_equip_elig_cid_m', None),

    # --- card_info.inc: CHTHONIAN_POLYMER_CID = 0x0000195d (new) ---
    (0x0803620c, 0x0000195d, 'CHTHONIAN_POLYMER_CID',
     'check_slot_equip_elig_cid_n', None),

    # --- duel_field.inc: NODE_POOL_TO_SLOT_STATE_OFF = 0xffffeb60 (new; 2 slots) ---
    (0x08036294, 0xffffeb60, 'NODE_POOL_TO_SLOT_STATE_OFF',
     'check_slot_equip_elig_0a_slotstate_off', None),

    # --- card_info.inc: CHARMER_RANGE_MAX_CID = 0x000018c2 (new) ---
    (0x080363b8, 0x000018c2, 'CHARMER_RANGE_MAX_CID',
     'check_slot_field_zone_charmer_range_max', None),

    # --- card_info.inc: ELEMENT_MAGICIAN_CID = 0x00001826 (new) ---
    (0x0803641c, 0x00001826, 'ELEMENT_MAGICIAN_CID',
     'check_slot_field_zone_cid_a', None),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 (new; 3 slots) ---
    (0x08036508, 0x0201b290, 'gDuelPhaseFlags',
     'check_effect_elig_phase_flags', None),
    (0x080366e0, 0x0201b290, 'gDuelPhaseFlags',
     'check_fieldspell_elig_phase_flags', None),
    (0x08036848, 0x0201b290, 'gDuelPhaseFlags',
     'check_zone_prereq_phase_flags', None),

    # --- card_info.inc: CANNONBALL_SPEAR_SHELLFISH_CID = 0x00001709 (new) ---
    (0x0803653c, 0x00001709, 'CANNONBALL_SPEAR_SHELLFISH_CID',
     'check_effect_elig_cid_a', None),

    # --- card_info.inc: DEEPSEA_WARRIOR_CID = 0x000012a8 (new) ---
    (0x08036544, 0x000012a8, 'DEEPSEA_WARRIOR_CID',
     'check_effect_elig_cid_c', None),

    # --- card_info.inc: HORUS_LV6_CID = 0x000017d3 (new) ---
    (0x08036574, 0x000017d3, 'HORUS_LV6_CID',
     'check_effect_elig_cid_e', None),

    # --- card_info.inc: SILENT_SWORDSMAN_LV5_CID = 0x00001814 (new) ---
    (0x08036588, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID',
     'check_effect_elig_cid_f', None),

    # --- card_info.inc: METALLIZING_PARASITE_CID = 0x00001693 (new) ---
    (0x0803664c, 0x00001693, 'METALLIZING_PARASITE_CID',
     'check_effect_elig_equip_ref_cid', None),

    # --- card_info.inc: NON_SPELLCASTING_AREA_CID = 0x00001667 (new) ---
    (0x08036650, 0x00001667, 'NON_SPELLCASTING_AREA_CID',
     'check_effect_elig_copies_cid', None),

    # --- card_info.inc: DUST_BARRIER_CID = 0x000017a1 (new) ---
    (0x08036654, 0x000017a1, 'DUST_BARRIER_CID',
     'check_effect_elig_zones_cid', None),

    # --- card_info.inc: EHERO_WILDHEART_CID = 0x0000194e (new) ---
    (0x080366e4, 0x0000194e, 'EHERO_WILDHEART_CID',
     'check_fieldspell_elig_cid_a', None),

    # --- duel_field.inc: PHASE_LOCK_FLAG_OFF = 0x000004bc (new) ---
    (0x0803684c, 0x000004bc, 'PHASE_LOCK_FLAG_OFF',
     'check_zone_prereq_phase_lock_off', None),

    # --- duel_field.inc: EQUIP_SLOT_CARD_ID_RANGE_MAX = 0x00001388 (new) ---
    (0x08036850, 0x00001388, 'EQUIP_SLOT_CARD_ID_RANGE_MAX',
     'check_zone_prereq_cid_range_max', None),

    # --- card_info.inc: LORD_OF_D_CID = 0x0000128b (new) ---
    (0x08036854, 0x0000128b, 'LORD_OF_D_CID',
     'check_zone_prereq_lord_of_d_cid', None),

    # --- card_info.inc: KING_DRAGUN_CID = 0x00001879 (new) ---
    (0x08036858, 0x00001879, 'KING_DRAGUN_CID',
     'check_zone_prereq_king_dragun_cid', None),

    # --- card_info.inc: HORUS_SERVANT_CID = 0x000017dc (new) ---
    (0x0803685c, 0x000017dc, 'HORUS_SERVANT_CID',
     'check_zone_prereq_horus_servant_cid', None),

    # --- card_info.inc: HORUS_LV8_CID = 0x000017d4 (new) ---
    (0x08036860, 0x000017d4, 'HORUS_LV8_CID',
     'check_zone_prereq_horus_lv8_cid', None),

    # --- card_info.inc: EQUIP_TYPE_A_CID = 0x0000150c (new) ---
    (0x080368dc, 0x0000150c, 'EQUIP_TYPE_A_CID',
     'check_equip_eligible_type_a_cid', None),

    # --- card_info.inc: EXODIA_NECROSS_CID = 0x00001645 (new) ---
    (0x080368e0, 0x00001645, 'EXODIA_NECROSS_CID',
     'check_equip_eligible_type_b_cid', None),

    # --- card_info.inc: HEART_OF_CLEAR_WATER_CID = 0x0000150a (new) ---
    (0x08036974, 0x0000150a, 'HEART_OF_CLEAR_WATER_CID',
     'check_equip_eligible_chain_param', None),

    # --- card_info.inc: TIMIDITY_CID = 0x0000153c (new) ---
    (0x080369a0, 0x0000153c, 'TIMIDITY_CID',
     'check_equip_eligible_chain_alt_cid', None),

    # --- card_info.inc: DARK_MAGICIAN_OF_CHAOS_CID = 0x000016f8 (new) ---
    (0x08036a6c, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID',
     'check_special_act_dmc_cid', None),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0803609c, 'check_slot_equip_elig_zone_cid_1632',
     'card_id=0x1632 (gap slot; passed as r0 to count_zones_by_card_and_mode;'
     ' not in card-stats.s; range [0x1631..0x1633] has Miracle Restoring/Disarmament); low-conf'),
    (0x08036160, 'check_slot_equip_elig_cid_13ea',
     'card_id=0x13ea (gap slot; not in card-stats.s;'
     ' range [0x13E8..0x13EB] has Nuvia the Wicked/Soul Exchange); equip BST branch; low-conf'),
    (0x08036914, 'check_equip_eligible_chain_sentinel',
     '0xffff0000: find_equip_chain_pair_across_field return<<16 == 0xffff0000'
     ' -> no valid pair found; 7587 raw refs (ROM-wide common pattern, not EQ)'),
]

# ---------------------------------------------------------------------------
# C. PLATE_FULL: (func_addr, new_plate_text)
#    Full plate rewrite for all 13 Seg-1 functions.
#    All text is pure ASCII (no CJK). FUN_ references replaced with current names.
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: link_equip_node_by_card_type_check (0x08035f54)
    # Replaces: FUN_0803c814 -> link_equip_node_to_chain, FUN_0803ca70 -> (named caller)
    (0x08035f54,
     'link_equip_node_by_card_type_check: Links an equip node into the equip chain after a card type check.'
     ' Called by two callers in duel_field (0x0803c814=link_equip_node_to_chain / 0x0803ca70).'
     ' Accepts r0=player_id, r1=slot_idx, r6=flag (non-APCS; bit0 for player direction).'
     ' Reads current slot [+0] field at gDuelFieldSlots[player*0x868+slot_idx*0x14],'
     ' ORs in 0x200000 (bit21; active_flag), writes back.'
     ' Then checks bit22 (lsrs #0x16 & 1): if 0 (clear) enters link_equip_node_to_chain path;'
     ' if 1 applies card_type conditional check before linking.'
     ' card_type_A=EHERO_AVIAN_CID(0x18a6), card_type_B=CHAIN_THRASHER_CID(0x19c1).'
     ' Constants: gDuelFieldSlots=0x0201c510, player_stride=PLAYER_BLOCK_STRIDE=0x868,'
     ' active_flag=0x200000 (bit21).'),

    # PLATE-2: check_slot_equip_eligibility_by_type (0x08036014)
    (0x08036014,
     'check_slot_equip_eligibility_by_type: Comprehensive equip eligibility check for a field slot.'
     ' r0=player_id [0..1], r1=slot_idx [0..4], r2=flag [0..1].'
     ' Calls check_slot_card_effect_eligibility then count_zones_by_card_and_mode(0x1632 gap CID);'
     ' dispatches to different eligibility paths based on card type field attr[0xc..0xf]'
     ' (type=1/5/6/0xa/0xb etc).'
     ' BST checks against 16 specific card IDs (ROYAL_COMMAND/FIEND_SKULL_DRAGON/'
     'POSSESSED_DARK_SOUL/SNATCH_STEAL/MAGIC_ARM_SHIELD/CHANGE_OF_HEART/0x13ea gap/'
     'MYSTIC_BOX/DARK_NECROFEAR/BRAIN_JACKER/ENEMY_CONTROLLER/FALLING_DOWN/OWNER_SEAL/'
     'RESHEF_THE_DARK_BEING/CHTHONIAN_POLYMER + DARK_NECROFEAR/SNATCH_STEAL/FALLING_DOWN/'
     'BRAIN_JACKER reprise).'
     ' Returns 1 if slot can legally equip, 0 otherwise. Shared by 7 duel_field callers.'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868.'),

    # PLATE-3: check_slot_field_zone_card_eligible (0x080363bc)
    (0x080363bc,
     'check_slot_field_zone_card_eligible: Field zone card eligibility check for slot.'
     ' r0=player_id [0..1], r1=slot_idx [0..4].'
     ' Reads slot at gDuelFieldSlots+player*0x868+slot*0x14;'
     ' checks bit12 activation and [slot+0x10] limit bits (bit5/bit1).'
     ' Calls check_card_id_is_field_zone_special to filter special zone cards.'
     ' Compares card_id against ELEMENT_MAGICIAN_CID(0x1826) and related IDs.'
     ' If conditions met, calls count_eligible_zone_slots_all_flags to verify'
     ' opposite side has eligible slots.'
     ' Uses equip node pool (gEquipNodePool=0x0201d9c0) + NODE_POOL_NEG_OFFSET(0xffffeb50)'
     ' + gDuelFieldSlotState(0x0201c520) + CHARMER_RANGE_MAX_CID(0x18c2) range check.'
     ' Returns 1 (eligible) or 0 (ineligible).'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868,'
     ' NODE_POOL_NEG_OFFSET=0xffffeb50, NODE_POOL_TO_SLOT_STATE_OFF=0xffffeb60,'
     ' CHARMER_RANGE_MAX_CID=0x18c2, ELEMENT_MAGICIAN_CID=0x1826.'),

    # PLATE-4: check_slot_equip_whitelist_with_monster_space (0x08036450)
    (0x08036450,
     'check_slot_equip_whitelist_with_monster_space: Checks slot meets equip activation conditions.'
     ' indeg=14, D_shared_mid.'
     ' Steps: (1) compute slot addr in gDuelFieldSlots(0x0201c510, stride=0x868, entry=0x14);'
     ' (2) [slot+0] high 13 bits nonzero (has card);'
     ' (3) [slot+0x8] halfword nonzero;'
     ' (4) check_slot_field_zone_card_eligible;'
     ' (5) check_slot_card_is_equip_whitelist;'
     ' (6) find_first_available_monster_slot_for_player (opposite side has space).'
     ' Returns 1 if all pass, 0 otherwise. Read-only.'
     ' Params: r0=u32 player_side [0..1], r1=u32 slot_idx [0..4].'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868.'),

    # PLATE-5: check_slot_card_effect_eligibility (0x080364b0)
    # Replaces: FUN_0803279c -> count_field_copies_of_card, FUN_08032654 -> count_available_effect_zones
    (0x080364b0,
     'check_slot_card_effect_eligibility: Checks whether the card in player_side:slot_idx qualifies'
     ' for effect activation.'
     ' Guards: card_id != 0, slot_idx <= 4, [gDuelPhaseFlags+0x4c0]==0 (phase lock),'
     ' [slot+0x8]!=0.'
     ' If guards pass, compares card_id against ~10 specific magic/trap card ID whitelist'
     ' (CANNONBALL_SPEAR_SHELLFISH_CID/LEGENDARY_FISHERMAN_CID/DEEPSEA_WARRIOR_CID/'
     'GUARDIAN_KAYEST_CID/HORUS_LV6_CID/SILENT_SWORDSMAN_LV5_CID plus computed 0x181a),'
     ' then calls check_card_matches_active_effect_slot(UMI_CARD_ID=0x10f4) /'
     ' count_slot_equip_list_matches(METALLIZING_PARASITE_CID=0x1693) /'
     ' check_slot_card_is_equip_type /'
     ' count_field_copies_of_card(NON_SPELLCASTING_AREA_CID=0x1667) /'
     ' count_available_effect_zones(DUST_BARRIER_CID=0x17a1);'
     ' accumulates results into r7 via OR.'
     ' Returns 0 (not eligible), 2 (equip chain hit), or 3 (special effect hit).'
     ' Sibling check_slot_card_fieldspell_eligibility(0x08036674) handles a separate card ID whitelist;'
     ' both share the same caller set.'
     ' r0=u32 player_side, r1=u32 slot_idx [0..4]. Returns u32 eligibility_flags.'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868,'
     ' gDuelPhaseFlags=0x0201b290, phase_lock_offset=0x4c0.'),

    # PLATE-6: query_slot_effect_eligibility_nonzero (0x08036658)
    (0x08036658,
     'query_slot_effect_eligibility_nonzero: 9-instruction thin wrapper over'
     ' check_slot_card_effect_eligibility.'
     ' Calls check_slot_card_effect_eligibility(r0, r1, r2), then tests (result & (r2+1)) > 0:'
     ' returns 1 if any masked bit is set, 0 otherwise.'
     ' Normalizes the multi-value eligibility result to a bool using a caller-supplied mask.'
     ' r2 is the mask-minus-1 value (0 -> mask=1 tests bit0; 1 -> mask=2 tests bit1).'
     ' r0=u32 player_side, r1=u32 slot_idx [0..4], r2=u32 result_mask_minus1.'
     ' Returns u32 bool (0=mask not hit; 1=mask hit).'
     ' Constants: all inherited from check_slot_card_effect_eligibility.'),

    # PLATE-7: check_slot_card_fieldspell_eligibility (0x08036674)
    (0x08036674,
     'check_slot_card_fieldspell_eligibility: Sibling of check_slot_card_effect_eligibility'
     ' sharing the same 4 callers.'
     ' Checks player_side:slot_idx card effect eligibility for a smaller card ID whitelist'
     ' (EHERO_WILDHEART_CID=0x194e and 0x194e+0x75=0x19c3).'
     ' Same entry guards: card_id!=0, slot_idx<=4, [gDuelPhaseFlags+0x4c0]==0, [slot+0x8]!=0.'
     ' Reads slot+0x10 equip word and checks bit5/bit1 both 0.'
     ' Compares card_id against 0x194e/0x19c3; hit -> returns 3, no hit -> returns 0.'
     ' Pure leaf function (no callees). Corresponds to field-spell type card effect check.'
     ' r0=u32 player_side, r1=u32 slot_idx [0..4]. Returns u32 eligibility (0 or 3).'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868,'
     ' gDuelPhaseFlags=0x0201b290, phase_lock_offset=0x4c0, EHERO_WILDHEART_CID=0x194e.'),

    # PLATE-8: check_slot_fieldspell_eligible_by_side (0x080366f0)
    (0x080366f0,
     'check_slot_fieldspell_eligible_by_side: Small wrapper around'
     ' check_slot_card_fieldspell_eligibility.'
     ' Takes (r0=player_side, r1=slot_idx, r2=target_player_side),'
     ' calls check_slot_card_fieldspell_eligibility(r0, r1) for eligibility flags,'
     ' then ANDs result with (r2+1) and checks > 0.'
     ' Returns 1 if slot has fieldspell eligibility AND (eligibility_flags & (r2+1)) != 0.'
     ' Compact selector used at multiple duel sites to check if specific side has'
     ' field spell activation right. indeg=10.'
     ' r0=u32 player_side [0..1]; r1=u32 slot_idx [0..9]; r2=u32 target_player_side [0..1].'
     ' Returns u32 0/1.'),

    # PLATE-9: query_slot_card_type_eligibility (0x0803670c)
    (0x0803670c,
     'query_slot_card_type_eligibility: Routes eligibility check based on card field6'
     ' (get_card_extended_stat_field6):'
     ' field6==0x17 (field spell) -> reads byte[+0x2] bit0 for side and calls'
     ' check_slot_fieldspell_eligible_by_side;'
     ' field6==0x16 (equip/continuous) -> calls query_slot_effect_eligibility_nonzero;'
     ' other types in zone_col 5..9 -> check_card_field5_is_nonzero then same.'
     ' r0=ptr card_slot_entry; r1=u8 player_id [0..1]; r2=u8 zone_col [0..9].'
     ' Returns u8 eligible_flag (1=eligible, 0=not). 74 callers (C_util_high).'
     ' Constants: FIELD_SPELL=0x17, EQUIP_CONTINUOUS=0x16, zone_col_range=[5..9].'),

    # PLATE-10: check_zone_slot_equip_prerequisites (0x08036770)
    (0x08036770,
     'check_zone_slot_equip_prerequisites: Checks equip card activation prerequisites'
     ' for the specified zone slot before full check_card_equip_eligible_for_slot.'
     ' Check chain:'
     ' (1) slot card_id==0 -> return 0 (empty slot, eligible);'
     ' (2) slot[+8] halfword==0 -> return 1 (no equip link, cannot activate);'
     ' (3) global flag [0x0201b74c]!=0 -> return 1 (globally disabled);'
     ' (4) slot_idx>4: skip level check;'
     ' (5) slot_idx<=4: read slot[+0x10] bit5; if 0 check card_id in'
     ' [0x1386..EQUIP_SLOT_CARD_ID_RANGE_MAX=0x1388] -> return 0;'
     ' (6) calls get_slot_card_state_code; state==1 -> calls'
     ' count_field_copies_of_card(LORD_OF_D_CID=0x128b) and'
     ' count_field_copies_of_card(KING_DRAGUN_CID=0x1879),'
     ' then count_available_effect_zones; if 0 -> return 1;'
     ' (7) final: card_id in [0x17d2..HORUS_LV8_CID=0x17d4] (Horus cluster)'
     ' check with HORUS_SERVANT_CID=0x17dc as arg.'
     ' Returns 0=prerequisites met, 1=failed. 92 callers.'
     ' Params: r0=ptr card_ptr, r1=u8 player_id [0..1], r2=u8 slot_idx [0..9].'
     ' Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868,'
     ' gDuelPhaseFlags=0x0201b290, PHASE_LOCK_FLAG_OFF=0x4bc,'
     ' EQUIP_SLOT_CARD_ID_RANGE_MAX=0x1388, LORD_OF_D_CID=0x128b,'
     ' KING_DRAGUN_CID=0x1879, HORUS_SERVANT_CID=0x17dc, HORUS_LV8_CID=0x17d4.'),

    # PLATE-11: check_card_equip_eligible_for_slot (0x08036870)
    # Replaces: FUN_080369a4 -> check_equip_eligibility_via_request_buf,
    #           FUN_0804640c/FUN_08047990/FUN_0804f440/FUN_0804f550 -> named callers
    (0x08036870,
     'check_card_equip_eligible_for_slot: Determines whether a given equip card is eligible'
     ' to attach to a target field slot. indeg=37, C_util_high.'
     ' r0=ptr card_ptr (r5); r1=ptr slot_ptr (r7); r2=u8 target_slot_idx [0..9] (r4);'
     ' r3=u8 player_id [0..1] (r9).'
     ' Phase 1: extracts field5 from card_ptr[+2] (bits[6:2]); subs 5 then truncates to u16;'
     ' if >5 enters Phase 2.'
     ' Phase 2: when field5 is in [0..5], stores flag in r8.'
     ' Reads halfword slot_ptr[+0x8] zone state; if 0 jumps to LAB_08036978 (special path).'
     ' Reads slot[+0] word as card_type, compares to EQUIP_TYPE_A_CID=0x150c and'
     ' EXODIA_NECROSS_CID=0x1645.'
     ' TYPE_A path: validates equip chain via find_equip_chain_pair_across_field'
     ' (sentinel 0xffff0000=check_equip_eligible_chain_sentinel).'
     ' TYPE_B path: similar but with player_id non-zero check.'
     ' LAB_08036938: if r8!=0 AND slot_idx<=4 AND slot[+0x8]!=0 calls'
     ' query_zone_chain_count_with_eligibility(HEART_OF_CLEAR_WATER_CID=0x150a);'
     ' if >0 calls map_card_id_to_anim_type and check_slot_card_is_equip_whitelist;'
     ' combined result returns 0 (eligible) or 1 (not).'
     ' Returns u32 bool (0=eligible, 1=not eligible). Pure query (callees all read-only).'
     ' Callers: check_equip_eligibility_via_request_buf(0x080369a4)'
     ' and 4 duel_field callers at 0x0804640c/0x08047990/0x0804f440/0x0804f550.'
     ' Constants: EQUIP_TYPE_A_CID=0x150c, EXODIA_NECROSS_CID=0x1645,'
     ' HEART_OF_CLEAR_WATER_CID=0x150a, TIMIDITY_CID=0x153c.'),

    # PLATE-12: check_equip_eligibility_via_request_buf (0x080369a4)
    # Replaces: FUN_0804686e/FUN_08046974/FUN_08046e44/FUN_08046fe4/FUN_08046bd0/
    #           FUN_08068596/FUN_0809dde4 -> named callers in duel_field
    (0x080369a4,
     'check_equip_eligibility_via_request_buf: Equip request constructor.'
     ' Builds 24-byte equip request record on stack,'
     ' fills (player_id, card_id, zone_type, extra) triple plus extension bits,'
     ' then forwards to check_card_equip_eligible_for_slot for actual eligibility test.'
     ' r0=u32 player_id [0..1] (bit0 XOR 1 -> [buf+2] bit0);'
     ' r1=u32 slot_idx [0..0x14] (equip_chain slot, forwarded to callee);'
     ' r2=u16 card_id [0..0x172f] (strh [buf+0]);'
     ' r3=u32 zone_type [0..0x1f] (low 5 bits lsls #1 -> [buf+2] bits[5..1]);'
     ' sp[0x30]=u32 extra_param (forwarded to callee 4th arg).'
     ' Returns u32 eligibility (0=not eligible, !=0=eligible).'
     ' Callers in duel_field cluster at 0x08046bd0 (0x0804686e/0x08046974/0x08046e44/0x08046fe4)'
     ' + effect trigger pre-filter at 0x08068596 + card frame at 0x0809dde4.'
     ' No external side effects, only stack-local buffer.'
     ' Constants: BUF_SIZE=0x18, EXTRA_PARAM_SP_OFFSET=0x30.'),

    # PLATE-13: check_slot_card_special_activation_eligible (0x08036a10)
    (0x08036a10,
     'check_slot_card_special_activation_eligible: Checks if a zone slot card qualifies'
     ' for a special activation rule (DARK_MAGICIAN_OF_CHAOS_CID=0x16f8 exception path).'
     ' Reads slot card_id from gDuelFieldSlots+player*0x868+slot_idx*20;'
     ' checks card_id against DARK_MAGICIAN_OF_CHAOS_CID(0x16f8);'
     ' also checks slot[+0] field8 (bits[31:27]) == 9 block value.'
     ' Returns 1 if eligible for special activation rule, 0 otherwise.'
     ' Params: r0=u8 player_id [0..1]; r1=u8 slot_idx [0..9].'
     ' Returns: r0=u32 bool (0=ineligible; 1=eligible).'
     ' Side effects: none (read-only).'
     ' Constants: PLAYER_BLOCK_STRIDE=0x868, gDuelFieldSlots=0x0201c510,'
     ' SLOT_ENTRY_SIZE=20, DARK_MAGICIAN_OF_CHAOS_CID=0x16f8, FIELD8_BLOCK_VALUE=9.'),
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
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

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
    print("[PLT] 0x%08x plate set (len=%d)" % (func_addr, len(new_plate)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF03Seg1Slots (DRY=%s) ===" % DRY)
    print("  Seg-1: 0x08035f54..0x08036a78, 13 fn, equip eligibility checks")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d (fail check skipped individually above)" % eq_ok)

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # C. PLATE_FULL
    print("\n--- C. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)
    print("  PLATE_FULL done: %d" % len(PLATE_FULL))

    print("\n=== RefineF03Seg1Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
