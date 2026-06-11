# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg3Slots.py -- file 03 Seg-3 (0x08037128..0x08037904)
#   graveyard/field array ops + equip eligibility + fn-ptr label (13 fn, 49 slots)
#   count_graveyard_entries_by_card_id / remove_slot_by_index_from_graveyard_arrays /
#   erase_slot_from_graveyard_arrays_by_ptr / remove_slot_from_field_array_by_player /
#   count_hand_cards_with_field5 / count_graveyard_normal_summon_cards /
#   count_zone_slots_with_card_field5 / check_zone_slot_equip_eligible /
#   check_zone_slot_equip_eligible_alt / place_equip_card_if_type_matches /
#   erase_slot_from_field_array_c_by_ptr / eval_equip_bonus_for_slot /
#   find_field_zone_slot_with_fieldspell
#   + unlabeled fn at 0x0803777c (check_level_conv_lab_node_match)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (36 slots)
#   B. REF_SLOTS  -- USER-label + DATA-ref (12 PTR_gP1LifePoints + 1 fn-ptr)
#   C. LABEL_FN   -- createLabel for unlabeled fn at 0x0803777c
#   D. PLATE_FULL -- full plate rewrite for all 13 functions (pure ASCII, no FUN_/CJK)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: New constants: card_info.inc x9, ewram.inc x1, duel_field.inc x1 written separately.

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

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 (1 slot, DWORD_ at entry point) ---
    (0x0803716c, 0x0201c4e0, 'gP1LifePoints',
     'count_graveyard_entries_by_card_id_lp_ptr', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (15 slots) ---
    (0x08037170, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_graveyard_entries_by_card_id_stride', None),
    (0x080371f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'remove_slot_by_index_from_gy_stride', None),
    (0x08037260, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'erase_slot_from_gy_by_ptr_stride', None),
    (0x08037308, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'remove_slot_from_field_arr_stride', None),
    (0x08037358, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_hand_cards_field5_stride', None),
    (0x080373a8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_gy_normal_summon_stride', None),
    (0x08037430, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_zone_slots_field5_stride', None),
    (0x0803748c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_slot_equip_elig_stride', None),
    (0x080374dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_slot_equip_elig_stride_b', None),
    (0x080375c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_slot_equip_elig_alt_stride', None),
    (0x08037610, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_zone_slot_equip_elig_alt_stride_b', None),
    (0x08037688, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'place_equip_card_if_type_stride', None),
    (0x08037750, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'erase_slot_from_field_arr_c_stride', None),
    (0x08037888, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'eval_equip_bonus_for_slot_stride', None),
    (0x080378dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_field_zone_slot_fieldspell_stride', None),
    (0x08037900, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_field_zone_slot_fieldspell_stride_b', None),

    # --- ewram.inc: gP1HandSlotArray = 0x0201c8f8 (1 slot) ---
    (0x08037490, 0x0201c8f8, 'gP1HandSlotArray',
     'check_zone_slot_equip_elig_zone_base', None),

    # --- ewram.inc: gP1AltHandSlotArray = 0x0201cab0 (1 slot) ---
    (0x080375c4, 0x0201cab0, 'gP1AltHandSlotArray',
     'check_zone_slot_equip_elig_alt_zone_base', None),

    # --- card_info.inc: A_LEGENDARY_OCEAN_CARD_ID = 0x0000150b (1 slot; reuse) ---
    (0x0803788c, 0x0000150b, 'A_LEGENDARY_OCEAN_CARD_ID',
     'eval_equip_bonus_for_slot_a_leg_ocean_cid', None),

    # --- duel_field.inc: SCENE_SLOT_MASK_LO = 0x00000fff (1 slot; reuse) ---
    (0x080377ac, 0x00000fff, 'SCENE_SLOT_MASK_LO',
     'check_level_conv_lab_node_match_mask', None),

    # --- card_info.inc: GRADIUS_OPTION_CID = 0x000014fc (NEW; 2 slots) ---
    (0x08037494, 0x000014fc, 'GRADIUS_OPTION_CID',
     'check_zone_slot_equip_elig_gradius_opt_cid', None),
    (0x080375c8, 0x000014fc, 'GRADIUS_OPTION_CID',
     'check_zone_slot_equip_elig_alt_gradius_opt_cid', None),

    # --- card_info.inc: GRADIUS_CID = 0x00001414 (NEW; 2 slots) ---
    (0x080374a4, 0x00001414, 'GRADIUS_CID',
     'check_zone_slot_equip_elig_gradius_cid', None),
    (0x080375d8, 0x00001414, 'GRADIUS_CID',
     'check_zone_slot_equip_elig_alt_gradius_cid', None),

    # --- card_info.inc: ULTIMATE_OFFERING_CID = 0x000012f3 (NEW; 2 slots) ---
    (0x080374e0, 0x000012f3, 'ULTIMATE_OFFERING_CID',
     'check_zone_slot_equip_elig_ult_off_cid', None),
    (0x08037614, 0x000012f3, 'ULTIMATE_OFFERING_CID',
     'check_zone_slot_equip_elig_alt_ult_off_cid', None),

    # --- card_info.inc: XYZ_DRAGON_CANNON_CID = 0x000015b4 (NEW; 1 slot) ---
    (0x0803750c, 0x000015b4, 'XYZ_DRAGON_CANNON_CID',
     'check_zone_slot_equip_elig_xyz_cid', None),

    # --- card_info.inc: HELPOEMER_CID = 0x00001571 (NEW; 1 slot) ---
    (0x08037520, 0x00001571, 'HELPOEMER_CID',
     'check_zone_slot_equip_elig_helpoemer_cid', None),

    # --- card_info.inc: SPHINX_TELEIA_CID = 0x000017c8 (NEW; 1 slot) ---
    (0x08037540, 0x000017c8, 'SPHINX_TELEIA_CID',
     'check_zone_slot_equip_elig_sphinx_teleia_cid', None),

    # --- card_info.inc: YZ_TANK_DRAGON_CID = 0x000015fa (NEW; 1 slot) ---
    (0x08037544, 0x000015fa, 'YZ_TANK_DRAGON_CID',
     'check_zone_slot_equip_elig_yz_tank_cid', None),

    # --- card_info.inc: LEVEL_CONVERSION_LAB_CID = 0x000018d9 (NEW; 1 slot) ---
    (0x080377a8, 0x000018d9, 'LEVEL_CONVERSION_LAB_CID',
     'check_level_conv_lab_node_match_cid', None),

    # --- card_info.inc: COST_DOWN_CID = 0x000015c7 (NEW; 1 slot) ---
    (0x08037890, 0x000015c7, 'COST_DOWN_CID',
     'eval_equip_bonus_for_slot_cost_down_cid', None),

    # --- ewram.inc: gP1FieldArrayCBase = 0x0201c600 (NEW; 2 slots) ---
    (0x08037754, 0x0201c600, 'gP1FieldArrayCBase',
     'erase_slot_from_field_arr_c_base', None),
    (0x080378e0, 0x0201c600, 'gP1FieldArrayCBase',
     'find_field_zone_slot_fieldspell_base', None),

    # --- duel_field.inc: FIELD_ARRAY_C_TO_COUNT_NEG_OFF = 0xfffffeec (NEW; 1 slot) ---
    (0x08037758, 0xfffffeec, 'FIELD_ARRAY_C_TO_COUNT_NEG_OFF',
     'erase_slot_from_field_arr_c_neg_off', None),

]  # end EQ_SLOTS (36 entries)

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    For PTR_gP1LifePoints_* slots: createLabel at slot + addMemoryReference to target.
#    For fn-ptr slot: createLabel at target fn + createLabel at slot + addMemoryRef.
# ---------------------------------------------------------------------------
# 12 PTR_gP1LifePoints_* -> gP1LifePoints (0x0201c4e0)
REF_LP_SLOTS = [
    (0x080371f4, 'remove_slot_by_idx_from_gy_lp_ptr'),
    (0x0803725c, 'erase_slot_from_gy_by_ptr_lp_ptr'),
    (0x08037304, 'remove_slot_from_field_arr_lp_ptr'),
    (0x08037354, 'count_hand_cards_field5_lp_ptr'),
    (0x080373a4, 'count_gy_normal_summon_lp_ptr'),
    (0x0803742c, 'count_zone_slots_field5_lp_ptr'),
    (0x080374d8, 'check_zone_slot_equip_elig_lp_ptr'),
    (0x0803760c, 'check_zone_slot_equip_elig_alt_lp_ptr'),
    (0x08037684, 'place_equip_card_type_lp_ptr'),
    (0x0803774c, 'erase_slot_from_field_arr_c_lp_ptr'),
    (0x080377e0, 'eval_equip_bonus_lp_ptr'),
    (0x080378d8, 'find_field_zone_fieldspell_lp_ptr'),
]
LP_TARGET = 0x0201c4e0

# fn-ptr slot: DAT_08037884 = 0x0803777d (THUMB odd addr -> fn at 0x0803777c)
FN_PTR_SLOT_ADDR  = 0x08037884
FN_PTR_VALUE      = 0x0803777d
FN_LABEL          = 'check_level_conv_lab_node_match'   # label at 0x0803777c
FN_ADDR           = 0x0803777c                           # even (body)
FN_PTR_SLOT_LABEL = 'eval_equip_bonus_for_slot_pred_fn'

# ---------------------------------------------------------------------------
# C. LABEL_FN: createLabel for unlabeled fn at 0x0803777c
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# D. PLATE_FULL: (func_addr, new_plate_ascii_text)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: count_graveyard_entries_by_card_id (0x08037128)
    (0x08037128,
     'count_graveyard_entries_by_card_id: Count entries in player graveyard word array matching target card_id.'
     ' Reads gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x1c (alt-hand/GY count).'
     ' Traverses word array at gP1LP+0x5d0 (=0xba<<3, stride 4B); extracts bits[12:0] as card_id.'
     ' Returns r4=total match count. r0=u8 player_id [0..1]; r1=u16 card_id (16-bit truncated).'
     ' indeg=0; referenced via fn-ptr or dead code.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE=0x868; GY_WORD_OFF=0x5d0 (0xba<<3); GY_COUNT_OFF=0x1c.'),

    # PLATE-2: remove_slot_by_index_from_graveyard_arrays (0x08037174)
    (0x08037174,
     'remove_slot_by_index_from_graveyard_arrays: Remove one slot by index from graveyard dual arrays'
     ' (word array gP1LP+0x5d0 and hword array gP1LP+0x788), decrement count at gP1LP+0x1c.'
     ' If slot_idx>=count returns 0. Decrements count.'
     ' If slot_idx<new_count: shift-left both arrays via write_word_from_deref_src (word) and ldrh/strh (hword).'
     ' Returns 1 on success, 0 if out of range.'
     ' r0=u8 player_id [0..1]; r1=u32 slot_idx (loaded to r12 at entry via 0x468c=mov r12,r1).'
     ' Caller: erase_slot_from_graveyard_arrays_by_ptr (finds match then calls this to delete by index).'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; GY_WORD_OFF=0x5d0; GY_HWORD_OFF=0x788 (0xf1<<3); GY_COUNT_OFF=0x1c.'),

    # PLATE-3: erase_slot_from_graveyard_arrays_by_ptr (0x0803720c)
    (0x0803720c,
     'erase_slot_from_graveyard_arrays_by_ptr: Forward-search graveyard word array for element matching'
     ' r1=slot_ptr (loaded to r8 at entry via 0x4688=mov r8,r1);'
     ' on match call remove_slot_by_index_from_graveyard_arrays(player_id, idx).'
     ' Returns 1 on success, 0 if not found.'
     ' r0=u8 player_id [0..1]; r1=slot_ptr (r8, forwarded as target to check_deref_words_equal).'
     ' Caller: erase_slot_from_zone_array_by_type (file02, 0x08032194) on graveyard card removal.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; GY_WORD_OFF=0x5d0; GY_COUNT_OFF=0x1c.'),

    # PLATE-4: remove_slot_from_field_array_by_player (0x0803727c)
    (0x0803727c,
     'remove_slot_from_field_array_by_player: Remove slot by index from player field arrays'
     ' A (gP1LP+0x260=0x98<<2) and B (gP1LP+0x418=0x83<<3)'
     ' using swap-to-tail and decrement.'
     ' Reads count at gP1LP+0x14 (gP1HandCountBase) and capacity at gP1LP+0x10 (gP1SlotCountBase).'
     ' Loops via swap_deref_words from tail toward target; decrements count.'
     ' Returns void (pop{r0};bx r0).'
     ' r0=u8 player_id (bit0) [0..1]; r1=u32 slot_index (0-based).'
     ' Caller: tick_field_clear_display_sequence (0x08040e54) during field clear phase.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; FIELD_CNT_OFF=0x14; CAP_OFF=0x10;'
     ' ARR_A_OFF=0x260 (0x98<<2); ARR_B_OFF=0x418 (0x83<<3).'),

    # PLATE-5: count_hand_cards_with_field5 (0x0803730c)
    (0x0803730c,
     'count_hand_cards_with_field5: Count hand cards where check_card_field5_is_nonzero(card_id) returns true.'
     ' Reads hand count at gP1LP+0x14; if 0 returns 0.'
     ' Iterates hand array at gP1LP+0x418 (0x83<<3), extracts bits[12:0] as card_id,'
     ' calls check_card_field5_is_nonzero; increments r6 on nonzero. Returns r6.'
     ' r0=u8 player_id [0..1]. Returns u32 count.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; HAND_CNT_OFF=0x14; HAND_ARR_OFF=0x418 (0x83<<3).'),

    # PLATE-6: count_graveyard_normal_summon_cards (0x0803735c)
    (0x0803735c,
     'count_graveyard_normal_summon_cards: Count cards in player graveyard (gP1LP+0x418, count at gP1LP+0x14)'
     ' matching check_card_id_is_normal_summon_type. Returns total count.'
     ' Called by eval_slot_score_entry_full (0x08037ec0) LP-cost branch; result scaled x5 into r10.'
     ' r0=u8 player_id [0..1]. Returns u32 count.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; GY_BASE_OFF=0x418 (0x83<<3); GY_CNT_OFF=0x14.'),

    # PLATE-7: count_zone_slots_with_card_field5 (0x080373ac)
    (0x080373ac,
     'count_zone_slots_with_card_field5: Count zone slots in r9/r8 zone table where flag byte==0x40 or ==0x80'
     ' AND check_card_field5_is_nonzero(card_id) is true.'
     ' r0=player_side (bit0, saved r5); Non-APCS r9=player_stride multiplier; r8=zone array base.'
     ' Inner loop 2-player x count slots; reads flag byte at gP1LP+0xf1*8 (=0x788) stride;'
     ' on flag match reads card_id from r9 base; checks field5.'
     ' Returns r6=matching slot count.'
     ' r0=u8 player_side [0..1]; r9=zone_stride (non-APCS); r8=zone_base (non-APCS).'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; FLAG_BYTE_OFF=0x788 (0xf1<<3);'
     ' ZONE_FLAG_A=0x40; ZONE_FLAG_B=0x80.'),

    # PLATE-8: check_zone_slot_equip_eligible (0x08037434)
    (0x08037434,
     'check_zone_slot_equip_eligible: Check equip eligibility of zone slot at gP1HandSlotArray[player*PLAYER_BLOCK_STRIDE+slot*4].'
     ' Extracts card_id (bits[12:0]). Five-step chain: (1) check_card_is_equip_target_eligible;'
     ' (2) check_card_has_equip_placement_type -> fail: eval_equip_placement_full_check;'
     ' (3) bit21 of slot word set -> fail; (4) check_card_stat_field8_is_6;'
     ' (5) check_toon_world_equip_present.'
     ' Special: card_id==GRADIUS_OPTION_CID (0x14fc) -> count_paired_slots_with_field5_default(player,0x1414);'
     ' card_id==LAVA_GOLEM_CID (0x14fc+0x7c=0x1578) -> read gP1LP+0x8e*2=0x11c bit17; if 0 call'
     ' check_value_in_slot_chain(player, ULTIMATE_OFFERING_CID=0x12f3, 0xb);'
     ' additional range/ID blacklist: [XYZ_DRAGON_CANNON_CID 0x15b4; TYRANT_DRAGON_CARD_ID 0x14d5;'
     ' HELPOEMER_CID 0x1571; SPHINX_TELEIA_CID 0x17c8; YZ_TANK_DRAGON_CID 0x15fa].'
     ' indeg=21. r0=u8 player_side; r1=u8 zone_player_id bit0; r2=u8 slot_index [0..4]. Returns bool.'
     ' Constants: gP1HandSlotArray=0x0201c8f8; PLAYER_BLOCK_STRIDE;'
     ' GRADIUS_OPTION_CID=0x14fc; GRADIUS_CID=0x1414; ULTIMATE_OFFERING_CID=0x12f3;'
     ' XYZ_DRAGON_CANNON_CID=0x15b4; HELPOEMER_CID=0x1571;'
     ' SPHINX_TELEIA_CID=0x17c8; YZ_TANK_DRAGON_CID=0x15fa.'),

    # PLATE-9: check_zone_slot_equip_eligible_alt (0x08037568)
    (0x08037568,
     'check_zone_slot_equip_eligible_alt: Alt variant of check_zone_slot_equip_eligible (0x08037434);'
     ' structure fully symmetric.'
     ' Only difference: zone table base=gP1AltHandSlotArray=0x0201cab0 (vs gP1HandSlotArray=0x0201c8f8).'
     ' Same five-step check chain and same special card_id handling'
     ' (GRADIUS_OPTION_CID / Lava Golem / ULTIMATE_OFFERING_CID / range blacklist). indeg=3.'
     ' r0=u8 player_side; r1=u8 zone_player_id bit0; r2=u8 slot_index [0..4]. Returns bool.'
     ' Constants: gP1AltHandSlotArray=0x0201cab0; PLAYER_BLOCK_STRIDE; (same card IDs as primary variant).'),

    # PLATE-10: place_equip_card_if_type_matches (0x08037630)
    (0x08037630,
     'place_equip_card_if_type_matches: For zone_type=0xb insert: verifies slot card_type is equip'
     ' (map_field8_to_card_type_category==3) and routes to correct array.'
     ' r0=player_id, r1=slot_ptr (saved r4). Extracts card_type (bits[12:0] from slot[0]);'
     ' skips if card_type==0 or check_card_field8_is_9.'
     ' Calls map_field8_to_card_type_category: if category==3 (equip):'
     ' append_slot_ref_to_equip_array; else: write_word_from_deref_src to gP1LP+0x120 (gP1FieldArrayCBase'
     ' per player), increments count at gP1LP+0x0c.'
     ' Returns void (pop{r0};bx r0).'
     ' Callers: dispatch_card_placement_by_zone_type (file02, 0x08032280) case 0xb;'
     '          retire_equip_slot_with_relink (file02, 0x08031954) re-check on field update.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; FIELD_C_ARR_OFF=0x120 (0x90<<1); FIELD_C_CNT_OFF=0x0c.'),

    # PLATE-11: erase_slot_from_field_array_c_by_ptr (0x080376a0)
    (0x080376a0,
     'erase_slot_from_field_array_c_by_ptr: Search field array C'
     ' (gP1FieldArrayCBase=gP1LP+0x120, count at gP1ZoneHandCount=gP1LP+0x0c)'
     ' for slot_ptr (r1=r10 via 0x468a=mov r10,r1).'
     ' On match: count-=1; if r8<new_count: dual left-shift loop via write_word_from_deref_src;'
     ' zeros old last entry via zero_fill_by_halfword. Returns 1 on success, 0 if not found.'
     ' r0=u8 player_id [0..1]; r1=slot_ptr (r10, target for check_deref_words_equal).'
     ' Caller: erase_slot_from_zone_array_by_type (file02, 0x08032194) on field-zone card exit.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; gP1FieldArrayCBase=0x0201c600;'
     ' FIELD_ARRAY_C_TO_COUNT_NEG_OFF=0xfffffeec (gP1FieldArrayCBase-0x114=gP1ZoneHandCount per player).'),

    # PLATE-12: eval_equip_bonus_for_slot (0x080377b0)
    (0x080377b0,
     'eval_equip_bonus_for_slot: Evaluate equip bonus score for slot'
     ' (r0=player_side, r1=slot_idx).'
     ' Reads card_id from gP1LP+slot*4+0x10e0 (zone-chain hword base, 0x87<<5 from gP1LP).'
     ' Calls get_card_extended_stat_field5(card_id); if 0 returns 0.'
     ' Calls find_equip_chain_node_by_pred with pred=check_level_conv_lab_node_match'
     ' (fn-ptr 0x0803777d) to locate Level Conversion Lab node'
     ' (A_LEGENDARY_OCEAN_CARD_ID=0x150b used for subsequent check_card_stat_field7_equals(card_id, 3)).'
     ' Two-player bonus loop at gP1LP+0xf8 (=gDuelFieldSlots_p2_base) + gP1LP+0x108 offset;'
     ' loop for player=0..1, slot=0..count: reads card_id,'
     ' checks A_LEGENDARY_OCEAN_CARD_ID (0x150b) match via check_card_matches_active_effect_slot;'
     ' adjusts score. Calls count_slot_chain_nodes_by_card_id(COST_DOWN_CID=0x15c7, 0xb); subtracts result*2.'
     ' Returns max(score, 1). r0=u8 player_side [0..1]; r1=u8 slot_idx [0..4]. Returns u32 bonus_score.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; ZONE_CHAIN_HWORD_OFF=0x87<<5=0x10e0;'
     ' A_LEGENDARY_OCEAN_CARD_ID=0x150b; COST_DOWN_CID=0x15c7; gDuelFieldSlots_p2_base offset=0xf8.'),

    # PLATE-13: find_field_zone_slot_with_fieldspell (0x08037894)
    (0x08037894,
     'find_field_zone_slot_with_fieldspell: Scan field array C'
     ' (gP1FieldArrayCBase=gP1LP+0x120, count at gP1LP+0x0c)'
     ' for first card with extended field6==0x17 (field spell type).'
     ' Returns 0-based slot index; returns -1 (rsbs r0,r0,#0) if not found. Skips card_id==0 slots.'
     ' Symmetric sibling to find_field_zone_slot_with_equip_type (0x08037904, Seg-4);'
     ' only difference is field6 check value (0x17 vs 0x16). Pure read-only.'
     ' r0=u8 player_id [0..1]. Returns s32 slot_index (>=0 if found, -1 if not).'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; gP1FieldArrayCBase=0x0201c600;'
     ' FIELD_C_CNT_OFF=0x0c; FIELDSPELL_FIELD6=0x17.'),

]  # end PLATE_FULL

# ===========================================================================
# Helpers
# ===========================================================================

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

def _apply_ref_lp(slot_addr, target_addr, slot_label):
    """Create USER-label at slot + DATA memory reference to target."""
    a_slot   = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl  = currentProgram.getSymbolTable()
    ref_mgr  = currentProgram.getReferenceManager()

    if not _check(slot_addr, target_addr, slot_label):
        print("[SKIP] REF 0x%08x (%s) value mismatch" % (slot_addr, slot_label))
        return

    if DRY:
        print("[dry] REF 0x%08x  -> 0x%08x  label=%s" % (slot_addr, target_addr, slot_label))
        return

    # create slot label
    existing = sym_tbl.getSymbols(a_slot)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # add DATA reference from slot to target
    ref = ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_mgr.setPrimary(ref, True)

    print("[REF] 0x%08x -> 0x%08x  (%s)" % (slot_addr, target_addr, slot_label))

def _apply_fn_ptr_ref(slot_addr, fn_addr, fn_label, slot_label):
    """Create USER-label at fn body, label at slot, DATA-ref slot->fn."""
    a_slot = _addr(slot_addr)
    a_fn   = _addr(fn_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] FN_LABEL 0x%08x -> %s" % (fn_addr, fn_label))
        print("[dry] REF(fn-ptr) 0x%08x -> 0x%08x  label=%s" % (slot_addr, fn_addr, slot_label))
        return

    # create function label at fn body addr
    existing_fn = sym_tbl.getSymbols(a_fn)
    names_fn = [s.getName() for s in existing_fn]
    if fn_label not in names_fn:
        sym_tbl.createLabel(a_fn, fn_label, SourceType.USER_DEFINED)
    print("[FN ] 0x%08x -> %s" % (fn_addr, fn_label))

    # create slot label
    existing = sym_tbl.getSymbols(a_slot)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # add DATA reference from slot to fn body (note: GAS uses fn+1 for THUMB odd addr)
    ref = ref_mgr.addMemoryReference(a_slot, a_fn, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_mgr.setPrimary(ref, True)
    print("[REF] 0x%08x -> 0x%08x  (%s) [fn-ptr THUMB+1 in ROM, label at even]" % (
        slot_addr, fn_addr, slot_label))

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
    print("=== RefineF03Seg3Slots (DRY=%s) ===" % DRY)
    print("  Seg-3: 0x08037128..0x08037904, 13 fn (+1 unlabeled), graveyard/field/equip-elig ops")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
    print("  EQ done: %d" % len(EQ_SLOTS))

    # B. REF_SLOTS -- PTR_gP1LifePoints_* (12 slots)
    print("\n--- B. REF_SLOTS lp_ptr (%d) ---" % len(REF_LP_SLOTS))
    for (slot_addr, slot_label) in REF_LP_SLOTS:
        _apply_ref_lp(slot_addr, LP_TARGET, slot_label)
    print("  REF lp_ptr done: %d" % len(REF_LP_SLOTS))

    # B2. fn-ptr slot (1)
    print("\n--- B2. fn-ptr slot ---")
    # verify ROM slot value = 0x0803777d
    if not _check(FN_PTR_SLOT_ADDR, FN_PTR_VALUE, FN_PTR_SLOT_LABEL):
        print("[SKIP] fn-ptr slot value mismatch, skipping")
    else:
        _apply_fn_ptr_ref(FN_PTR_SLOT_ADDR, FN_ADDR, FN_LABEL, FN_PTR_SLOT_LABEL)

    # C. LABEL_FN -- already done inside _apply_fn_ptr_ref above
    print("\n--- C. LABEL_FN (check_level_conv_lab_node_match @ 0x%08x) ---" % FN_ADDR)
    print("  (handled in B2 fn-ptr block above)")

    # D. PLATE_FULL
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)
    print("  PLATE_FULL done: %d" % len(PLATE_FULL))

    print("\n=== RefineF03Seg3Slots DONE ===")
    print("  EQ=%d  REF_LP=%d  REF_FN_PTR=1  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_LP_SLOTS), len(PLATE_FULL)))

main()
