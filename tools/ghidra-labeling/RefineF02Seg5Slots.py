# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg5Slots.py -- file 02 Seg-5 (0x080309b8..0x080313dc)
#   effect slot zone equip valid + place_card_into_*_zone_slot + find_zone_descriptor cluster
#   (23 fn, 60 slots: 52 DAT_/DWORD_ + 8 PTR_gP1LifePoints_*)
#
# Sections:
#   A. EQ_SLOTS   -- 39 slots (24 EQ_REUSE + 15 EQ_NEW)
#                    New constants in: duel_field.inc (+4), ewram.inc (+8), card_info.inc (+1)
#   B. REF_SLOTS  -- 0 slots (PTR_gP1LifePoints_* already have .word gP1LifePoints DATA refs)
#   C. RENAME_SLOTS -- 21 slots (8 PTR_ label renames + 7 card_id + 5 neg_off + 1 zone mask)
#   D. PLATE_FULL -- 10 full plate rewrites (C8: entire plate replaced to guarantee no stale FUN_)
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

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, reuse, 15 slots) ---
    (0x08030a64, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_equip_whitelist_player_stride', None),
    (0x08030ad8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_whitelist_player_stride', None),
    (0x08030b40, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_type_player_stride', None),
    (0x08030be0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'incr_player_chain_ctr_player_stride', None),
    (0x08030cb0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'place_card_monster_zone_player_stride', None),
    (0x08030dd0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'place_card_spelltrap_zone_player_stride', None),
    (0x08030e38, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_zone_desc_player_stride', None),
    (0x08030fa8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_zone_desc_pair0_player_stride', None),
    (0x08031054, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_zone_desc_pair5_player_stride', None),
    (0x08031164, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_slot_idx_dual_player_stride', None),
    (0x080311c8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_slot_idx_setcode_player_stride', None),
    (0x08031224, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_slot_idx_zone_id_player_stride', None),
    (0x0803127c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_hand_slot_setcode_player_stride', None),
    (0x080312d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_hand_slot_setcode_alt_player_stride', None),
    (0x08031330, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_slot_card_id_zones_player_stride', None),

    # --- gDuelFieldSlots = 0x0201c510 (ewram.inc, reuse, 7 slots) ---
    (0x08030a68, 0x0201c510, 'gDuelFieldSlots',
     'check_equip_whitelist_field_slots', None),
    (0x08030adc, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_equip_whitelist_field_slots', None),
    (0x08030b44, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_equip_type_field_slots', None),
    (0x08030cb4, 0x0201c510, 'gDuelFieldSlots',
     'place_card_monster_zone_field_slots', None),
    (0x08030dd4, 0x0201c510, 'gDuelFieldSlots',
     'place_card_spelltrap_zone_field_slots', None),
    (0x08030e34, 0x0201c510, 'gDuelFieldSlots',
     'find_zone_desc_field_slots', None),
    (0x08031160, 0x0201c510, 'gDuelFieldSlots',
     'find_slot_idx_dual_field_slots', None),

    # --- gP1ZoneHandCount = 0x0201c4ec (ewram.inc, reuse, 1 slot) ---
    (0x08031050, 0x0201c4ec, 'gP1ZoneHandCount',
     'find_zone_desc_pair0_zone_hand_count', None),

    # --- gDuelEffectChainSlots = 0x0201bc54 (ewram.inc, reuse, 1 slot) ---
    (0x08031090, 0x0201bc54, 'gDuelEffectChainSlots',
     'find_zone_desc_effect_chain_slots', None),

    # --- FIELD_SLOT_COUNT_OFF = 0x00001cb4 (duel_field.inc NEW, 2 slots) ---
    (0x08030cb8, 0x00001cb4, 'FIELD_SLOT_COUNT_OFF',
     'place_card_monster_zone_slot_count_off',
     'place_card_into_monster_zone_slot: field slot count'),
    (0x08030dd8, 0x00001cb4, 'FIELD_SLOT_COUNT_OFF',
     'place_card_spelltrap_zone_slot_count_off',
     'place_card_into_spelltrap_zone_slot: field slot count'),

    # --- SLOT_FACE_STATUS_ARRAY_OFF = 0x000010b1 (duel_field.inc NEW, 2 slots) ---
    (0x08030cbc, 0x000010b1, 'SLOT_FACE_STATUS_ARRAY_OFF',
     'place_card_monster_zone_face_status_off',
     'equip_face_bits byte array base'),
    (0x08030ddc, 0x000010b1, 'SLOT_FACE_STATUS_ARRAY_OFF',
     'place_card_spelltrap_zone_face_status_off',
     'equip_face_bits byte array base'),

    # --- FIELD_SPELL_CARD_REF_OFF = 0x00001390 (duel_field.inc NEW, 1 slot) ---
    (0x08030de0, 0x00001390, 'FIELD_SPELL_CARD_REF_OFF',
     'place_card_spelltrap_zone_spell_ref_off',
     'field spell equip trigger card_id guard'),

    # --- DUEL_ACTIVE_PLAYER_OFF = 0x00001cb8 (duel_field.inc NEW, 1 slot) ---
    (0x08030de4, 0x00001cb8, 'DUEL_ACTIVE_PLAYER_OFF',
     'place_card_spelltrap_zone_active_player_off',
     'gP1LifePoints+0x1cb8 active turn player idx'),

    # --- gP1SlotCountBase = 0x0201c4f0 (ewram.inc NEW, 1 slot) ---
    (0x08030fc4, 0x0201c4f0, 'gP1SlotCountBase',
     'find_zone_desc_pair3_slot_count_base',
     'pair3 count ptr: gP1LifePoints+0x10 slot set_code count'),

    # --- gP1SlotSetCodeArray = 0x0201c740 (ewram.inc NEW, 1 slot) ---
    (0x08030fc8, 0x0201c740, 'gP1SlotSetCodeArray',
     'find_zone_desc_pair3_slot_setcode_array',
     'pair3 data ptr: gP1LifePoints+0x260 slot set_code array'),

    # --- gP1HandCountBase = 0x0201c4f4 (ewram.inc NEW, 1 slot) ---
    (0x08030fac, 0x0201c4f4, 'gP1HandCountBase',
     'find_zone_desc_pair1_hand_count_base',
     'pair1 count ptr: gP1LifePoints+0x14 hand slot count'),

    # --- gP1HandSlotArray = 0x0201c8f8 (ewram.inc NEW, 1 slot) ---
    (0x08030fb0, 0x0201c8f8, 'gP1HandSlotArray',
     'find_zone_desc_pair1_hand_slot_array',
     'pair1 data ptr: gP1LifePoints+0x418 hand slot array'),

    # --- gP1ChainZoneCountBase = 0x0201c4f8 (ewram.inc NEW, 1 slot) ---
    (0x08030fd0, 0x0201c4f8, 'gP1ChainZoneCountBase',
     'find_zone_desc_pair4_chain_zone_count_base',
     'pair4 count ptr: gP1LifePoints+0x18 chain zone count'),

    # --- gP1ChainZoneArray = 0x0201c880 (ewram.inc NEW, 1 slot) ---
    (0x08030fd4, 0x0201c880, 'gP1ChainZoneArray',
     'find_zone_desc_pair4_chain_zone_array',
     'pair4 data ptr: gP1LifePoints+0x3a0 chain zone array'),

    # --- gP1AltHandCountBase = 0x0201c4fc (ewram.inc NEW, 1 slot) ---
    (0x08030fb8, 0x0201c4fc, 'gP1AltHandCountBase',
     'find_zone_desc_pair2_alt_hand_count_base',
     'pair2 count ptr: gP1LifePoints+0x1c alt-hand count'),

    # --- gP1AltHandSlotArray = 0x0201cab0 (ewram.inc NEW, 1 slot) ---
    (0x08030fbc, 0x0201cab0, 'gP1AltHandSlotArray',
     'find_zone_desc_pair2_alt_hand_slot_array',
     'pair2 data ptr: gP1LifePoints+0x5d0 alt-hand array'),

    # --- FIELD_SPELL_B_EFFECT_ID = 0x00001407 (card_info.inc NEW, 1 slot) ---
    (0x08030a24, 0x00001407, 'FIELD_SPELL_B_EFFECT_ID',
     'check_field_spell_b_effect_id',
     'field spell type-B effect chain guard ID'),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: empty -- all PTR_gP1LifePoints_* already have .word gP1LifePoints
#    DATA refs established by prior Ghidra operations.
# ---------------------------------------------------------------------------
REF_SLOTS = [
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    21 slots: 8 PTR_ renames + 7 card_id + 5 neg_off + 1 zone mask
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # --- PTR_gP1LifePoints_* slot label renames (8 slots) ---
    (0x08030bdc, 'increment_player_chain_counter_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080310fc, 'find_slot_idx_in_dual_list_by_id_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080311c4, 'find_slot_idx_by_set_code_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031220, 'find_slot_idx_by_zone_id_chain_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x08031278, 'find_hand_slot_idx_by_set_code_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x080312d0, 'find_hand_slot_idx_by_set_code_alt_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0803132c, 'find_slot_idx_by_card_id_zones_p1lp_base',
     'gP1LifePoints base ptr'),
    (0x0803137c, 'find_lp_entry_by_flag_p1lp_base',
     'gP1LifePoints base ptr'),

    # --- card_id whitelist slots (7 slots) ---
    # check_slot_card_is_equip_whitelist / check_slot_card_is_equip_type BST comparison
    (0x08030a6c, 'check_equip_whitelist_cid_1636',
     'equip whitelist ID 0x1636'),
    (0x08030a70, 'check_equip_whitelist_cid_1472_a',
     'equip whitelist upper bound'),
    (0x08030a94, 'check_equip_whitelist_cid_172f_a',
     'equip whitelist ID 0x172f'),
    (0x08030a98, 'check_equip_whitelist_cid_1472_b',
     'check_node_in_slot_chain value'),
    (0x08030ae0, 'check_equip_type_cid_172f',
     'equip type upper bound cmp'),
    (0x08030af8, 'check_equip_type_cid_1809',
     'equip type ID 0x1809'),
    (0x08030afc, 'check_equip_type_cid_1472',
     'check_node_in_slot_chain value'),

    # --- neg-offset derived slots (5 slots) ---
    # Pure arithmetic: count_ptr - data_ptr (find_zone_descriptor_by_slot_id pairs)
    (0x08030fb4, 'find_zone_desc_pair1_neg_off',
     'gP1HandCountBase-gP1HandSlotArray = -0x404'),
    (0x08030fc0, 'find_zone_desc_pair2_neg_off',
     'gP1AltHandCountBase-gP1AltHandSlotArray = -0x5b4'),
    (0x08030fcc, 'find_zone_desc_pair3_neg_off',
     'gP1SlotCountBase-gP1SlotSetCodeArray = -0x250'),
    (0x08030fd8, 'find_zone_desc_pair4_neg_off',
     'gP1ChainZoneCountBase-gP1ChainZoneArray = -0x388'),
    (0x08031058, 'find_zone_desc_pair5_neg_off',
     'gP1ZoneHandCount-data_base = -0x114; data at gP1LP+0x120=0x0201c600'),

    # --- zone descriptor mask slot (1 slot) ---
    (0x080310b0, 'find_zone_desc_default_type_mask',
     'bits[31:16]=0xffff default table zone type'),

]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: 10 full plate rewrites (C8: entire plate replaced, not substring)
#    All stale FUN_ -> current function names. Pure ASCII.
#    Format: (func_addr, new_plate_text)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: check_slot_card_is_equip_type (0x08030aa4)
    # FUN_08030b0c -> check_slot_card_is_monster_type
    (0x08030aa4,
     "Reads EWRAM duel slot (0x0201c510 + (r0 bit0)*0x868 + r1*20), extracts low 13 bits as card_id."
     " Compares card_id against whitelist {0x172f, 0x1636, 0x1809, 0x1472}:"
     " match -> call check_node_in_slot_chain(side, slot, 0x1472, 5) and return its result."
     " No match -> call check_card_field8_is_normal(card_id) for field8 extended type check."
     " r0=u32 player_side (bit0), r1=u32 slot_idx [0..4]. Returns bool is_equip_type."
     " Callers: duel_field check_slot_card_is_monster_type (card_type==8 guard),"
     " 0x080364b0, 0x08050c58, 0x08051318, 0x08091888."
     " Constants: 0x0201c510=gDuelFieldSlots, 0x868=player stride,"
     " slot_entry=20 bytes, 0x172f/0x1809/0x1472=equip/magic card ID whitelist,"
     " 0x1636=second ID (=0x172f-0xf9, DAT_08030a6c asm:47150)."),

    # PLATE-2: write_word_from_deref_src (0x08030b88)
    # FUN_08030be4 -> place_card_into_monster_zone_slot
    # FUN_08030cc0 -> place_card_into_spelltrap_zone_slot
    # FUN_08031578 -> insert_slot_ref_into_hand_array
    # FUN_08031630 -> append_slot_ref_to_equip_array
    (0x08030b88,
     "Leaf utility, 3 instructions: reads one word from *r1 and writes it to *r0."
     " Callers (place_card_into_monster_zone_slot, place_card_into_spelltrap_zone_slot,"
     " insert_slot_ref_into_hand_array, append_slot_ref_to_equip_array,"
     " and 28 others, indeg=32) all call this when initializing field slots"
     " to copy a card pointer from the source slot into the destination slot's head word."
     " Side effect: [r0] := [r1] (single word write)."),

    # PLATE-3: swap_deref_words (0x08030b90)
    # FUN_08031668 -> shuffle_player_hand_list
    # FUN_08031b44 -> sort_hand_cards_by_lp_score
    # FUN_08036e40 -> insert_card_into_hand_list_by_zone_desc
    (0x08030b90,
     "Swap the word values at two memory addresses in-place.\n"
     "Reads [r0]->r3, [r1]->r2, writes [r0]:=r2, [r1]:=r3.\n"
     "Leaf function (no further calls).\n"
     "Called by shuffle_player_hand_list, sort_hand_cards_by_lp_score,"
     " insert_card_into_hand_list_by_zone_desc,"
     " remove_slot_from_field_array_by_player (0x0803727c)\n"
     "in array shift/sort loops (bubble-sort style element moves).\n"
     "r0=u32* ptr_a (first word address), r1=u32* ptr_b (second word address).\n"
     "Returns void (bx lr)."),

    # PLATE-4: check_deref_words_equal (0x08030b9c)
    # FUN_08036de8 -> erase_slot_from_equip_array_a_by_ptr
    # FUN_0803720c -> erase_slot_from_graveyard_arrays_by_ptr
    # FUN_080317e0 -> erase_slot_from_hand_array_by_ptr
    # FUN_08031978 -> erase_slot_from_equip_array_b_by_ptr
    # FUN_080376a0 -> erase_slot_from_field_array_c_by_ptr
    (0x08030b9c,
     "Leaf utility. Dereferences r0 and r1 each to get one word, compares them:"
     " returns 1 if equal, 0 otherwise."
     " Callers (erase_slot_from_equip_array_a_by_ptr, erase_slot_from_graveyard_arrays_by_ptr,"
     " erase_slot_from_hand_array_by_ptr, erase_slot_from_equip_array_b_by_ptr,"
     " erase_slot_from_field_array_c_by_ptr, 6 total) use this in pointer-search-and-delete"
     " slot scan loops, comparing a target card pointer r1 against each array element [r0] in turn."),

    # PLATE-5: place_card_into_monster_zone_slot (0x08030be4)
    # FUN_08032280 -> dispatch_card_placement_by_zone_type
    (0x08030be4,
     "Registers a card into the specified monster zone (zone_type 0..4) slot for the given player."
     " r0=player_id [0..1], r1=zone_idx [0..4], r2=card_slot_ptr, r3=equip_qualifier."
     " Steps: (1) zero-fills target slot 20 bytes (zero_fill_by_halfword);"
     " (2) copies card word to slot[0] via write_word_from_deref_src;"
     " (3) increments field slot counter at [base+0x1cb4];"
     " (4) writes slot metadata (slot[2]=serial, slot[3]=equip_qualifier, slot[4]=card_type_bits);"
     " (5) updates equip_face_bits in field8 status byte;"
     " (6) calls write_field_slot_bit_by_player twice (bit 0x7 and bit 0x0);"
     " (7) if field6==0x16 (special enchant) and field has a copy, calls link_equip_node_to_chain."
     " Caller dispatch_card_placement_by_zone_type default branch routes here for zone_type<=4.\n"
     "Constants: slot_base=0x0201c510, player_stride=0x868, slot_size=20, counter_offset=0x1cb4."),

    # PLATE-6: place_card_into_spelltrap_zone_slot (0x08030cc0)
    # FUN_08032280 -> dispatch_card_placement_by_zone_type
    (0x08030cc0,
     "Registers a card into the specified spell/trap zone (zone_type 5..10) slot for the given player."
     " r0=player_id [0..1], r1=zone_idx [5..10], r2=card_slot_ptr, r3=counter_ref."
     " Steps: (1) zero-fills target slot 20 bytes;"
     " (2) copies card word to slot[0];"
     " (3) increments field slot counter;"
     " (4) writes slot metadata (slot[2]=serial, slot[3]=0, slot[4]=0);"
     " (5) updates equip_face_bits in field8 status byte;"
     " (6) writes slot[6] link word;"
     " (7) calls write_field_slot_bit_by_player twice (bit 0x14 and bit 0x7)."
     " Shares base address 0x0201c510 and slot stride 20 bytes with"
     " place_card_into_monster_zone_slot but sets slot[3]=0 and has no equip-chain logic."
     " Caller dispatch_card_placement_by_zone_type default branch routes here for zone_type>4.\n"
     "Constants: slot_base=0x0201c510, player_stride=0x868, slot_size=20, counter_offset=0x1cb4."),

    # PLATE-7: find_field_slot_by_set_code_global (0x08031118)
    # FUN_080521a0 -> check_equip_slot_eligible_by_setcode_global_and_chain
    (0x08031118,
     "Search both players' full field (2 x 11 slots) for the first slot whose set_code matches r0;"
     " return packed location.\n"
     "Outer loop r5=[0..1] (player_id), inner loop r4=[0..10] (slot_index).\n"
     "Each slot from gDuelFieldSlots + player*0x868 + slot_idx*0x14;"
     " extracts set_code = bits[29:22]*2 + bit19.\n"
     "On match: return (slot_idx<<8)|player_id. No match: return -1.\n"
     "Caller check_equip_slot_eligible_by_setcode_global_and_chain (duel_field)"
     " uses return value in equip chain validation"
     " (passes to find_zone_chain_node_by_card_id_pair).\n"
     "Sibling of find_slot_idx_by_set_code (0x08031184) which searches a single player.\n"
     "Constants: gDuelFieldSlots=0x0201c510; player_stride=0x868;"
     " slot_entry=0x14; slot_count_per_player=11."),

    # PLATE-8: find_slot_idx_by_zone_id_in_chain_list (0x080311e0)
    # FUN_0803e594 -> tick_zone_card_place_with_slot_resolve_seq
    # FUN_0807fde8 -> dispatch_equip_criteria_display_by_type_code
    (0x080311e0,
     "Called by tick_zone_card_place_with_slot_resolve_seq (caseD_31) and"
     " dispatch_equip_criteria_display_by_type_code."
     " In the chain slot list starting at\n"
     "gP1LifePoints+player*0x868+0x18, searches for the slot index corresponding to zone_id.\n"
     "r0=player_id (bit0 determines player), r1=zone_id (target zone id). Count read from\n"
     "[gP1LifePoints+player*0x868+0x18+0]; search array base gP1LifePoints+player*0x868+0x3a0\n"
     "(=0xe8*4), stride=4. For each slot word extracts bits[23:16]*2+bit18 as key; if key==zone_id\n"
     "returns current index r3. Returns -1 if not found (rsbs r0,r0,#0).\n"
     "\n"
     "Constants:\n"
     "  BASE_OFFSET=0x18 (gP1LifePoints+player*0x868+0x18)\n"
     "  SEARCH_STRIDE=0x4 (4 bytes per slot entry)\n"
     "  PLAYER_STRIDE=0x868 (DAT_08031224)\n"
     "  NOT_FOUND=-1"),

    # PLATE-9: find_lp_entry_by_flag_and_type (0x08031348)
    # FUN_08020db4 -> render_lp_record_text_set_a
    # FUN_08020fa8 -> render_lp_record_text_set_b
    # FUN_0802c358 -> render_card_name_escape_to_line
    (0x08031348,
     "Linear scan of gP1LifePoints+4 array (step=4, max 0xff entries)"
     " for an entry matching flag bit0 == r0,"
     " entry_type (low 13 bits of halfword at [entry+0x10e0]) == 1,"
     " and valid_mark bit7 of [entry+0x10e0+1] set."
     " Returns 1 if matching entry found, 0 if not found."
     " r0=u32 flag_value [0..1]. Returns u32 found_flag."
     " Callers: render_lp_record_text_set_a, render_lp_record_text_set_b,"
     " render_card_name_escape_to_line (result_screen LP record display)."
     " Constants: array_step=4, field_offset=0x10e0, max_count=0xff,"
     " type_value=1, valid_bit7=1."),

    # PLATE-10: check_equip_placement_eligible_from_slot_record (0x080313b8)
    # FUN_0807d2e0 -> tick_zone_pipeline_with_neo_daedalus_oam_setup
    (0x080313b8,
     "Function: extract card_id from slot record pointer and validate equip placement legality."
     " r0=u32* slot_record_ptr (points to slot data word, saved to r4)."
     " Reads [r4+0] (card_data word), extracts bits[12:0] (card_id via lsls #0x13; lsrs #0x13);"
     " calls check_card_has_equip_placement_type(card_id)."
     " If return 0 (no equip placement type) -> directly returns 1 (eligible/placeable);"
     " if non-zero -> further extracts bit14 of [r4+0] (lsls #0x11; lsrs #0x1f),"
     " returns that bit value (1=activated/equipable, 0=not activated)."
     " Exit pop{r1};bx r1 (Sub-case E, preserves r0)."
     " Called by tick_zone_pipeline_with_neo_daedalus_oam_setup in Neo Daedalus group"
     " placement check chain to confirm whether target slot card accepts equip.\n"
     "\n"
     "Side effects: no external writes (pure read).\n"
     "\n"
     "Constants:\n"
     "- card_id_bits = bits[12:0] // lsls #19; lsrs #19 -> 13-bit card_id [0..0x1fff]\n"
     "- placement_bit = bit14 // lsls #0x11; lsrs #0x1f -> bit14 activation flag [0..1]"),

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
    print("=== RefineF02Seg5Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-5: 0x080309b8..0x080313dc, 23 fn, 60 slots")
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

    # D. PLATE_FULL (10 full plate rewrites -- C8 entire plate, no stale FUN_)
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    print("\n=== RefineF02Seg5Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
