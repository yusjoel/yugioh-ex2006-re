# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg6Slots.py -- file 02 Seg-6 (0x080313dc..0x0803217c)
#   equip card set-code / slot ref array ops
#   (23 fn, 64 slots: 45 DAT_ + 4 DWORD_ + 15 PTR_gP1LifePoints_)
#
# Sections:
#   A. EQ_SLOTS   -- 38 slots (32 EQ_REUSE + 6 EQ_NEW)
#                    New constants already added to:
#                      duel_field.inc (+1: EQUIP_SLOT_ACTIVE_TAG)
#                      card_info.inc  (+1: SLOT_CARD_SET_CODE_MASK)
#                      oam_attr.inc   (+1: OAM_ATTR2_TILE_CLEAR)
#   B. REF_SLOTS  -- 0 slots (PTR_gP1LifePoints_* already have .word gP1LifePoints DATA refs)
#   C. RENAME_SLOTS -- 26 slots (16 PTR_/DWORD_ label renames + 10 DAT_/DWORD_ domain labels)
#   D. PLATE_FULL -- 11 full plate rewrites (C8: entire plate replaced to guarantee no stale FUN_)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0, disasm=0 for this segment.
# NOTE: New constants added to inc files before running this script.
# NOTE: FUNC_RENAME=0; no CSV sync needed.
# NOTE: EQ slot labels differ from eq_name (avoids GAS PC-relative "value too big").

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

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, reuse, 20 slots) ---
    (0x0803143c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'get_set_code_player_stride', None),
    (0x080314c4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_min_pred_player_stride', None),
    (0x08031500, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'resolve_pair_player_stride', None),
    (0x080315f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'insert_hand_array_player_stride', None),
    (0x08031624, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'append_hand_array_player_stride', None),
    (0x08031664, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'append_equip_array_player_stride', None),
    (0x080316b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'shuffle_hand_list_player_stride', None),
    (0x080316f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_deck_pair_player_stride', None),
    (0x08031750, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_chain_zone_pair_player_stride', None),
    (0x080317cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'remove_equip_by_idx_player_stride', None),
    (0x08031870, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'erase_hand_by_ptr_player_stride', None),
    (0x08031a08, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field5_player_stride', None),
    (0x08031a80, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_pair_allowed_player_stride', None),
    (0x08031ae0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_chain_pair_player_stride', None),
    (0x08031b40, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'sort_hand_by_lp_player_stride', None),
    (0x08031b8c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'init_hand_display_player_stride', None),
    (0x08031d2c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'init_hand_slots_player_stride', None),
    (0x08031eb0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_hand_shuffled_player_stride', None),
    (0x08032170, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'serialize_zone_setcodes_player_stride', None),
    (0x0803192c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'remove_zone_slot_by_cid_player_stride', None),

    # --- gDuelFieldSlots = 0x0201c510 (ewram.inc, reuse, 3 slots) ---
    (0x08031440, 0x0201c510, 'gDuelFieldSlots',
     'get_set_code_field_slots', None),
    (0x080314c8, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_min_pred_field_slots', None),
    (0x08031504, 0x0201c510, 'gDuelFieldSlots',
     'resolve_pair_field_slots', None),

    # --- gP1SlotSetCodeArray = 0x0201c740 (ewram.inc, reuse, 4 slots) ---
    (0x08031628, 0x0201c740, 'gP1SlotSetCodeArray',
     'append_hand_array_setcode_array', None),
    (0x08031874, 0x0201c740, 'gP1SlotSetCodeArray',
     'erase_hand_by_ptr_setcode_array', None),
    (0x08031930, 0x0201c740, 'gP1SlotSetCodeArray',
     'remove_zone_slot_by_cid_setcode_array', None),
    (0x08031d34, 0x0201c740, 'gP1SlotSetCodeArray',
     'init_hand_slots_setcode_array', None),

    # --- gP1ChainZoneArray = 0x0201c880 (ewram.inc, reuse, 2 slots) ---
    (0x08031a0c, 0x0201c880, 'gP1ChainZoneArray',
     'count_field5_chain_zone_array', None),
    (0x08031d40, 0x0201c880, 'gP1ChainZoneArray',
     'init_hand_slots_chain_zone_array', None),

    # --- GPRNG_STEP_CTR_MASK = 0xffffc03f (duel_field.inc, reuse, 2 slots) ---
    # C5: value 0xffffc03f already exists as GPRNG_STEP_CTR_MASK; reuse required.
    # Usage: clear OAM attr2 bits[13:6] (frame counter field) before inserting new value.
    (0x08031d3c, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',
     'init_hand_slots_oam_frame_ctr_mask',
     'clear OAM attr2 bits[13:6] (frame counter field)'),
    (0x08032178, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',
     'serialize_zone_setcodes_oam_frame_ctr_mask',
     'clear OAM attr2 bits[13:6] (frame counter field)'),

    # --- OAM_ATTR0_HIDDEN = 0x0000ffff (oam_attr.inc, reuse, 1 slot) ---
    # C5: value 0x0000ffff already exists as OAM_ATTR0_HIDDEN; reuse required.
    # Usage: ands r0,r1 as 16-bit mask (extract low 16 bits of chain node word).
    (0x08031498, 0x0000ffff, 'OAM_ATTR0_HIDDEN',
     'find_equip_min_pred_lo16_mask', None),

    # --- EQUIP_SLOT_ACTIVE_TAG = 0xa5600000 (duel_field.inc NEW, 1 slot) ---
    (0x08031444, 0xa5600000, 'EQUIP_SLOT_ACTIVE_TAG',
     'get_set_code_active_tag',
     'equip slot active-state packed tag'),

    # --- SLOT_CARD_SET_CODE_MASK = 0x00001fff (card_info.inc NEW, 2 slots) ---
    (0x08031d38, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',
     'init_hand_slots_set_code_mask',
     'init_player_hand_display_slots: 13-bit set_code mask'),
    (0x08031eb4, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',
     'build_hand_shuffled_set_code_mask',
     'build_hand_zone_display_slots_shuffled: set_code mask'),

    # --- OAM_ATTR2_TILE_CLEAR = 0xffffe000 (oam_attr.inc NEW, 3 slots) ---
    (0x08031d30, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',
     'init_hand_slots_tile_clear_mask',
     'init_player_hand_display_slots: clear tile field'),
    (0x08031eb8, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',
     'build_hand_shuffled_tile_clear_mask',
     'build_hand_zone_display_slots_shuffled: clear tile field'),
    (0x08032174, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',
     'serialize_zone_setcodes_tile_clear_mask',
     'serialize_field_zone_setcodes_to_buf: clear tile field'),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: empty -- all PTR_gP1LifePoints_* already have .word gP1LifePoints
#    DATA refs established by prior Ghidra operations.
# ---------------------------------------------------------------------------
REF_SLOTS = [
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    26 slots: 16 PTR_/DWORD_ label renames + 10 DAT_/DWORD_ domain labels
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # --- PTR_gP1LifePoints_* slot label renames (15 PTR_ + 1 DWORD_) -- 16 slots ---
    (0x080315f0, 'insert_hand_array_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031660, 'append_equip_array_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080316b0, 'shuffle_hand_list_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080316f4, 'find_deck_pair_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0803174c, 'find_chain_zone_pair_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080317c8, 'remove_equip_by_idx_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0803186c, 'erase_hand_by_ptr_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031928, 'remove_zone_slot_by_cid_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031a04, 'erase_equip_b_by_ptr_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031a7c, 'count_field5_nonzero_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031adc, 'count_pair_allowed_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031b3c, 'count_chain_pair_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031b88, 'sort_hand_by_lp_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031d28, 'init_hand_display_slots_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031eac, 'build_hand_zone_shuffled_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0803216c, 'serialize_zone_setcodes_p1lp_base',
     'gP1LifePoints base ptr'),

    # --- DAT_/DWORD_ domain-specific renames (10 slots) ---
    (0x08031448, 'get_set_code_no_pair_sentinel',
     '(pair_result << 16) == this -> no pair found'),
    (0x08031470, 'find_equip_min_pred_card_id',
     'predicate card_id 0x1130 for min_count search'),
    (0x08031494, 'find_equip_min_pred_fn_ptr',
     'fn ptr to inline predicate at 0x08031455'),
    (0x08031508, 'resolve_pair_special_card_id_a',
     'special equip card_id A for pair substitution'),
    (0x08031530, 'resolve_pair_sub_id_a',
     'substitute card_id for 0x19a6 on pairing'),
    (0x08031558, 'resolve_pair_sub_id_b',
     'substitute card_id for (0x19a6+0x16) on pairing'),
    (0x0803162c, 'append_hand_array_neg_off',
     'gP1SlotCountBase - gP1SlotSetCodeArray = -0x250'),
    (0x08031878, 'erase_hand_by_ptr_neg_off',
     'gP1SlotCountBase - gP1SlotSetCodeArray = -0x250'),
    (0x08031934, 'remove_zone_slot_neg_off',
     'gP1SlotCountBase - gP1SlotSetCodeArray = -0x250'),
    (0x08031a10, 'erase_equip_b_by_ptr_neg_off',
     'gP1ChainZoneCountBase - gP1ChainZoneArray = -0x388'),

]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: 11 full plate rewrites (C8: entire plate replaced, not substring)
#    All stale FUN_ -> current function names. Pure ASCII.
#    Stale FUN_ mapping (12 unique tokens -> current names):
#      FUN_08032194 -> erase_slot_from_zone_array_by_type
#      FUN_08032280 -> dispatch_card_placement_by_zone_type
#      FUN_08037630 -> place_equip_card_if_type_matches
#      FUN_08040144 -> tick_hand_sort_display_init_seq
#      FUN_08040194 -> tick_hand_zone_swap_display_seq
#      FUN_080499c4 -> render_pair_zone_sprites_if_field_card_present
#      FUN_0807512c -> dispatch_equip_display_state_by_code
#      FUN_0807b77c -> invoke_equip_oam_for_chain_zone_slot_if_placeable
#      FUN_08080944 -> build_equip_criteria_for_target_slots
#      FUN_08096fe0 -> eval_equip_target_via_chain_zone_lookup
#      FUN_08093660 -> init_duel_puzzle_field_and_hand_display
#      FUN_080937a8 -> init_duel_puzzle_hand_display_both_sides
#    Format: (func_addr, new_plate_text)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: insert_slot_ref_into_hand_array (0x08031578)
    # FUN_08032280 -> dispatch_card_placement_by_zone_type
    (0x08031578,
     "Inserts a card slot reference into the player's hand array at the given position (r9=slot_idx),"
     " shifting existing elements one step right."
     " r0=player_id [0..1], r1=slot_idx [0..N-1]."
     " Steps: (1) reads hand count from [gP1LP+0x10+player*0x868];"
     " (2) shifts each element from the tail down to slot_idx right by one using write_word_from_deref_src;"
     " (3) increments count;"
     " (4) writes the original value at r9 to the new position."
     " Unlike append_slot_ref_to_hand_array this function preserves order via shifting."
     " Caller dispatch_card_placement_by_zone_type routes here when zone_type=0xd and r2==0."
     "\nConstants: hand_array_base=gP1LP+0x260, hand_count_offset=gP1LP+0x10, player_stride=0x868."),

    # PLATE-2: append_slot_ref_to_hand_array (0x080315f8)
    # FUN_08032280 -> dispatch_card_placement_by_zone_type
    (0x080315f8,
     "Appends a card slot reference to the end of the player's hand array."
     " r0=player_id [0..1], r1=slot_ptr (pointer to the source card slot)."
     " Reads hand count from [gP1LP+0x10+player*0x868], uses count as index to call"
     " write_word_from_deref_src writing slot_ptr into [gP1LP+0x260+player*0x868+count*4],"
     " then increments count."
     " Unlike insert_slot_ref_into_hand_array this function appends to the tail without moving existing elements."
     " Caller dispatch_card_placement_by_zone_type routes here when zone_type=0xd and r2!=0."
     "\nConstants: hand_array_base=0x0201c740 (=gP1LP+0x260), hand_count_base=gP1LP+0x10, player_stride=0x868."),

    # PLATE-3: append_slot_ref_to_equip_array (0x08031630)
    # FUN_08032280 -> dispatch_card_placement_by_zone_type
    # FUN_08037630 -> place_equip_card_if_type_matches
    (0x08031630,
     "Appends a card slot reference to the end of the player's equip array."
     " r0=player_id [0..1], r1=slot_ptr (pointer to the source card slot)."
     " Reads count from [gP1LP+0x18+player*0x868], uses count*4 as offset to call"
     " write_word_from_deref_src writing slot_ptr into [gP1LP+0x3a0+player*0x868+count*4],"
     " then increments count."
     " Callers: dispatch_card_placement_by_zone_type case 0xc (zone_type=equip direct insert)"
     " and place_equip_card_if_type_matches (zone_type=0xb after equip type confirmation)."
     "\nConstants: equip_array_base=gP1LP+0x3a0 (0xe8<<2), equip_count_offset=0x18, player_stride=0x868."),

    # PLATE-4: shuffle_player_hand_list (0x08031668)
    # FUN_08093660 -> init_duel_puzzle_field_and_hand_display
    (0x08031668,
     "Fisher-Yates shuffle of specified player hand list."
     " r0=player_side (bit0=[0..1]); reads gP1LP+player*0x868+0x10 (hand capacity)."
     " Iterates from tail backward: calls sample_prng_scaled(count+1) for [0..count] random index,"
     " then swap_deref_words to exchange current and random hand entries."
     " Hand array A base: gP1LP+player*0x868+0x260 (0x98<<2); entry stride=4 bytes."
     " Called by tick_hand_shuffle_display_seq (0x080400a8) and init_duel_puzzle_field_and_hand_display"
     " during hand shuffle phase."
     " Params: r0=u8 player_side [0..1] (bit0 extracted via ands)."
     " Returns void (pop{r4,r5,r6};pop{r0};bx r0 tail return)."
     "\nConstants: player_stride=0x868; hand_capacity_offset=0x10; hand_array_offset=0x260 (=0x98<<2);"
     " entry_stride=4."),

    # PLATE-5: find_chain_zone_slot_by_pair_card (0x08031710)
    # FUN_0807b77c -> invoke_equip_oam_for_chain_zone_slot_if_placeable
    # FUN_08080944 -> build_equip_criteria_for_target_slots
    # FUN_08096fe0 -> eval_equip_target_via_chain_zone_lookup
    (0x08031710,
     "Search the given player's chain zone (offset 0x18/0x3a0) for the first slot whose card"
     " pairs with target_card_id; return slot index."
     " r0=player_side (bit0), r1=target_card_id (saved to r7)."
     " Reads chain zone count from gP1LifePoints+player*0x868+0x18;"
     " iterates array from gP1LifePoints+player*0x868+0x3a0 (0xe8<<2)."
     " Each slot: extracts bits[18:0] as card_icid, calls check_card_pair_allowed(card_icid, target_card_id)."
     " On first hit: return current index r5. No hit: return -1 (rsbs)."
     " Callers: invoke_equip_oam_for_chain_zone_slot_if_placeable,"
     " build_equip_criteria_for_target_slots, eval_equip_target_via_chain_zone_lookup"
     " (all duel_field effect check flows)."
     "\nConstants: gP1LifePoints=0x0201c4e0; player_stride=0x868; chain_zone_count_offset=0x18;"
     " chain_zone_array_offset=0xe8<<2=0x3a0."),

    # PLATE-6: erase_slot_from_hand_array_by_ptr (0x080317e0)
    # FUN_08032194 -> erase_slot_from_zone_array_by_type
    # FUN_08040194 -> tick_hand_zone_swap_display_seq
    (0x080317e0,
     "Searches the hand array (gP1LP+0x260, count at gP1LP+0x10) for the element matching"
     " r9(=r1=slot_ptr), removes it by left-shifting subsequent elements, and decrements the count."
     " r0=player_id [0..1], r1=slot_ptr (r9)."
     " Forward-scans from r8=0 to count-1, calling check_deref_words_equal each iteration;"
     " on match shifts elements left and updates count."
     " Callers: erase_slot_from_zone_array_by_type (duel_field) and tick_hand_zone_swap_display_seq"
     " when a hand card leaves the field."
     "\nConstants: hand_array_base=gP1LP+0x260, hand_count_offset=gP1LP+0x10, player_stride=0x868."),

    # PLATE-7: erase_slot_from_equip_array_b_by_ptr (0x08031978)
    # FUN_08032194 -> erase_slot_from_zone_array_by_type
    (0x08031978,
     "Searches equip array B (gP1LP+0x3a0, count at gP1LP+0x18) for the element matching"
     " r9(=r1=slot_ptr), removes it by left-shifting subsequent elements, and decrements the count."
     " r0=player_id [0..1], r1=slot_ptr (r9, confirmed by 0x4689=mov r9,r1 at entry)."
     " Fully symmetric with erase_slot_from_hand_array_by_ptr;"
     " differs only in array offset (0x3a0 vs 0x260) and count offset (0x18 vs 0x10)."
     " Caller erase_slot_from_zone_array_by_type (duel_field) invokes this when an equip card leaves the field."
     "\nConstants: equip_array_B_base=gP1LP+0x3a0, equip_B_count_offset=0x18, player_stride=0x868."),

    # PLATE-8: count_monster_slots_with_field5_nonzero (0x08031a34)
    # FUN_0807512c -> dispatch_equip_display_state_by_code
    (0x08031a34,
     "Reads monster zone card count from gP1LifePoints+player*0x868+0x10;"
     " iterates array from +0x260 (0x98<<2)."
     " Each slot: extract bits[18:0] = card_icid;"
     " call check_card_field5_is_nonzero(card_icid); if nonzero increment r6."
     " Returns r6 (count). Pure read, no external writes."
     " Caller dispatch_equip_display_state_by_code"
     " (card_frame;card_ids;card_stats;duel_field;font_jp;game_str;settings) in case 0x80:"
     " compares result to total monster count ([base+0x10]) to check if all satisfy field5>0."
     "\nConstants: gP1LifePoints=0x0201c4e0; player_stride=0x868;"
     " monster_zone_count_offset=0x10; monster_zone_array_offset=0x98<<2=0x260."),

    # PLATE-9: count_chain_zone_card_pair_allowed_for_card (0x08031ae4)
    # FUN_080499c4 -> render_pair_zone_sprites_if_field_card_present
    (0x08031ae4,
     "r0=player_side (bit0), r1=target_card_id (saved to r8 via mov r8,r1)."
     " Reads chain zone count from gP1LifePoints+player*0x868+0x18;"
     " iterates array from +0x3a0 (0xe8<<2)."
     " Each slot: extract bits[18:0]=card_icid; restore r1=r8=target_card_id;"
     " call check_card_pair_allowed. On hit: r6++."
     " Returns r6. Pure read, no external writes."
     " Caller render_pair_zone_sprites_if_field_card_present (duel_field)"
     " pairs this with count_zone_card_pair_allowed_for_card and sums via cmn."
     " Sibling of count_zone_card_pair_allowed_for_card (0x08031a84, searches monster zone +0x10/+0x260);"
     " this searches chain zone +0x18/+0x3a0."
     "\nConstants: gP1LifePoints=0x0201c4e0; player_stride=0x868;"
     " chain_zone_count_offset=0x18; chain_zone_array_offset=0xe8<<2=0x3a0."),

    # PLATE-10: sort_hand_cards_by_lp_score (0x08031b44)
    # FUN_08040144 -> tick_hand_sort_display_init_seq
    (0x08031b44,
     "Called by tick_hand_sort_display_init_seq (duel event display hub case 0x58 sub-call)"
     " twice with r0=0 and r0=1, sorting both players' hand cards by LP score."
     " r0 bit0=player_id [0..1]. Reads hand LP score field from"
     " gP1LifePoints+player_id*0x868+0x10 (r6), computes count=(r6+sign_ext)/2 as sort upper bound."
     " Locates hand entry array at gP1LifePoints+0x98*4=gP1LifePoints+0x260+player_id*0x868."
     " Classic bubble/selection sort loop calling swap_deref_words to swap adjacent words for ascending order."
     " Side effects: swap_deref_words swaps adjacent word entries in hand array (sort side effect)."
     "\nConstants: HAND_LP_SCORE_OFFSET=0x10, PLAYER_ZONE_STRIDE=0x868, HAND_ARRAY_OFFSET=0x260 (0x98 lsl 2)."),

    # PLATE-11: build_hand_zone_display_slots_shuffled (0x08031d44)
    # FUN_080937a8 -> init_duel_puzzle_hand_display_both_sides
    (0x08031d44,
     "r0=turn_or_player_flag (bit0 = player side), r1=dest_display_buf ptr."
     " Reads player hand zone count and zone_set_code array from gP1LifePoints+player*0x868+0x8."
     " Writes 3 strh to display slot header: fixed value 5, (count-5), and zone[+8]."
     " Fisher-Yates shuffle (via sample_prng_scaled) randomizes zone set_code sequence."
     " Repeats for second zone group; memcpy (lsls #1 bytes) writes result to dest_buf+0x210+player_offset."
     " Caller init_duel_puzzle_hand_display_both_sides (duel_field) calls this twice in puzzle init"
     " for both player sides."
     "\nConstants: gP1LifePoints (base); player_stride=0x868; hand_area_offset=0x84<<2=0x210;"
     " SET_CODE_MASK=0x1fff."),

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
    """Replace entire plate comment at func_addr with new_plate (pure ASCII).
    After setting, reads back and verifies no FUN_[0-9a-f]{8} remains.
    """
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

    # Readback verification: confirm no FUN_[0-9a-f]{8} pattern remains
    readback = cu.getComment(CodeUnit.PLATE_COMMENT)
    if readback is None:
        print("[WARN] plate_full 0x%08x: readback returned None" % func_addr)
        return

    import re
    stale = re.findall(r'FUN_[0-9a-fA-F]{8}', readback)
    if stale:
        print("[FAIL] plate_full 0x%08x: stale FUN_ still present after write: %s" % (
            func_addr, stale))
    else:
        print("[PLF] 0x%08x: plate replaced OK, no stale FUN_ (len=%d)" % (
            func_addr, len(new_plate)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg6Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-6: 0x080313dc..0x0803217c, 23 fn, 64 slots")
    print("  EQ=%d REF=%d RENAME=%d PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

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

    # D. PLATE_FULL (11 full plate rewrites -- C8 entire plate, no stale FUN_)
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    print("\n=== RefineF02Seg6Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
