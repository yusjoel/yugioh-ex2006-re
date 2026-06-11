# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg4aSlots.py -- file 03 Seg-4a (0x08037904..0x08037ec0)
#   field zone slot query + compute_zone_effect_atk_delta (12 fn, 43 slots, 1 FUNC_RENAME)
#   find_field_zone_slot_with_equip_type / count_gy_cards_by_field6 (-> renamed) /
#   count_field_zone_cards_by_field7 / count_valid_monster_pair_slots /
#   find_zone_slot_idx_allowed_for_card / count_field_zone_cards_with_field5 /
#   count_monster_slots_with_field5_ge_threshold / get_player_deck_flag_bit1 /
#   check_field_effect_zone_activation_eligible / shuffle_hand_by_player_deck_flag /
#   compute_zone_effect_atk_delta
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (32 slots)
#   B. REF_SLOTS  -- USER-label + DATA-ref (10 PTR_gP1LifePoints_* + 1 carve label)
#   C. CARVE_LABEL -- createLabel field_spell_atk_bonus_table @0x09e3ef74 (carve sync)
#   D. FUNC_RENAME -- count_gy_cards_by_field6 -> count_field_zone_cards_by_field6
#   E. PLATE_FULL -- full plate rewrite for 11 functions (pure ASCII, no FUN_/CJK)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: New constants: field_spell_bonus.inc (new, 2 consts), card_info.inc +9 CID
#       written separately. rom.s carve edited separately.

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

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x868 (13 slots) ---
    (0x0803794c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_field_zone_slot_with_equip_type_stride', None),
    (0x08037970, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_field_zone_slot_with_equip_type_stride_b', None),
    (0x080379cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_zone_cards_by_field6_stride', None),
    (0x08037a28, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_zone_cards_by_field7_stride', None),
    (0x08037a88, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_valid_monster_pair_slots_stride', None),
    (0x08037acc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_zone_slot_idx_allowed_for_card_stride', None),
    (0x08037b30, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_zone_cards_with_field5_stride', None),
    (0x08037b8c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_monster_slots_field5_ge_threshold_stride', None),
    (0x08037bb0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'get_player_deck_flag_bit1_stride', None),
    (0x08037c98, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'shuffle_hand_by_player_deck_flag_stride', None),
    (0x08037cf0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'compute_zone_effect_atk_delta_stride', None),
    (0x08037db8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'compute_zone_effect_atk_delta_stride_b', None),
    (0x08037eb8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'compute_zone_effect_atk_delta_stride_c', None),

    # --- ewram.inc: gP1FieldArrayCBase = 0x0201c600 (1 slot) ---
    (0x08037950, 0x0201c600, 'gP1FieldArrayCBase',
     'find_field_zone_slot_with_equip_type_field_arr_c', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (3 slots) ---
    (0x08037cf4, 0x0201c510, 'gDuelFieldSlots',
     'compute_zone_effect_atk_delta_slots', None),
    (0x08037dbc, 0x0201c510, 'gDuelFieldSlots',
     'compute_zone_effect_atk_delta_slots_b', None),
    (0x08037ebc, 0x0201c510, 'gDuelFieldSlots',
     'compute_zone_effect_atk_delta_slots_c', None),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (1 slot) ---
    (0x08037c10, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'check_field_effect_zone_elig_lp_field_off', None),

    # --- card_info.inc: EYE_OF_TRUTH_CID = 0x137b (NEW; 1 slot) ---
    (0x08037c04, 0x0000137b, 'EYE_OF_TRUTH_CID',
     'check_field_effect_zone_elig_eye_of_truth_cid', None),

    # --- card_info.inc: MIND_ON_AIR_CID = 0x17e7 (NEW; 1 slot) ---
    (0x08037c08, 0x000017e7, 'MIND_ON_AIR_CID',
     'check_field_effect_zone_elig_mind_on_air_cid', None),

    # --- card_info.inc: RESPECT_PLAY_CID = 0x135e (NEW; 1 slot) ---
    (0x08037c14, 0x0000135e, 'RESPECT_PLAY_CID',
     'check_field_effect_zone_elig_respect_play_cid', None),

    # --- card_info.inc: MOLTEN_DESTRUCTION_CID = 0x1346 (NEW; 1 slot) ---
    (0x08037d30, 0x00001346, 'MOLTEN_DESTRUCTION_CID',
     'compute_zone_effect_atk_delta_range_max_cid', None),

    # --- card_info.inc: YAMI_CID = 0x10f5 (NEW; 1 slot) ---
    (0x08037d34, 0x000010f5, 'YAMI_CID',
     'compute_zone_effect_atk_delta_range_min_cid', None),

    # --- card_info.inc: GAIA_POWER_CID = 0x1344 (NEW; 1 slot) ---
    (0x08037d48, 0x00001344, 'GAIA_POWER_CID',
     'compute_zone_effect_atk_delta_gaia_power_cid', None),

    # --- card_info.inc: MYSTIC_PLASMA_ZONE_CID = 0x1349 (NEW; 1 slot) ---
    (0x08037d68, 0x00001349, 'MYSTIC_PLASMA_ZONE_CID',
     'compute_zone_effect_atk_delta_mystic_plasma_cid', None),

    # --- card_info.inc: NECROVALLEY_CID = 0x159d (NEW; 1 slot) ---
    (0x08037d80, 0x0000159d, 'NECROVALLEY_CID',
     'compute_zone_effect_atk_delta_necrovalley_cid', None),

    # --- card_info.inc: HARPIES_HUNTING_GROUND_CID = 0x183f (NEW; 1 slot) ---
    (0x08037d8c, 0x0000183f, 'HARPIES_HUNTING_GROUND_CID',
     'compute_zone_effect_atk_delta_harpies_hunt_cid', None),

    # --- field_spell_bonus.inc: FIELD_SPELL_TABLE_IDX_BIAS = 0xffffef10 (NEW; 1 slot) ---
    (0x08037de0, 0xffffef10, 'FIELD_SPELL_TABLE_IDX_BIAS',
     'compute_zone_effect_atk_delta_table_idx_bias', None),

    # --- field_spell_bonus.inc: ZONE_EFFECT_ATK_PENALTY_500 = 0xfffffe70 (NEW; 4 slots) ---
    (0x08037e14, 0xfffffe70, 'ZONE_EFFECT_ATK_PENALTY_500',
     'compute_zone_effect_atk_delta_penalty_a', None),
    (0x08037e2c, 0xfffffe70, 'ZONE_EFFECT_ATK_PENALTY_500',
     'compute_zone_effect_atk_delta_penalty_b', None),
    (0x08037e44, 0xfffffe70, 'ZONE_EFFECT_ATK_PENALTY_500',
     'compute_zone_effect_atk_delta_penalty_c', None),
    (0x08037e5c, 0xfffffe70, 'ZONE_EFFECT_ATK_PENALTY_500',
     'compute_zone_effect_atk_delta_penalty_d', None),

]  # end EQ_SLOTS (32 entries)

# ---------------------------------------------------------------------------
# B. REF_SLOTS:
#   B1: PTR_gP1LifePoints_* (10 slots) -> gP1LifePoints = 0x0201c4e0
#   B2: DAT_08037ddc -> field_spell_atk_bonus_table @ 0x09e3ef74
# ---------------------------------------------------------------------------
LP_TARGET = 0x0201c4e0

REF_LP_SLOTS = [
    (0x08037948, 'find_field_zone_slot_with_equip_type_lp_ptr'),
    (0x080379c8, 'count_field_zone_cards_by_field6_lp_ptr'),
    (0x08037a24, 'count_field_zone_cards_by_field7_lp_ptr'),
    (0x08037a84, 'count_valid_monster_pair_slots_lp_ptr'),
    (0x08037ac8, 'find_zone_slot_idx_allowed_for_card_lp_ptr'),
    (0x08037b2c, 'count_field_zone_cards_with_field5_lp_ptr'),
    (0x08037b88, 'count_monster_slots_field5_ge_threshold_lp_ptr'),
    (0x08037bac, 'get_player_deck_flag_bit1_lp_ptr'),
    (0x08037c0c, 'check_field_effect_zone_activation_eligible_lp_ptr'),
    (0x08037c94, 'shuffle_hand_by_player_deck_flag_lp_ptr'),
]

# carve label ref: DAT_08037ddc -> field_spell_atk_bonus_table @ 0x09e3ef74
CARVE_SLOT_ADDR   = 0x08037ddc
CARVE_TARGET_ADDR = 0x09e3ef74
CARVE_TARGET_LABEL = 'field_spell_atk_bonus_table'
CARVE_SLOT_LABEL  = 'compute_zone_effect_atk_delta_table_base'

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: count_gy_cards_by_field6 -> count_field_zone_cards_by_field6
# ---------------------------------------------------------------------------
FUNC_RENAME_ADDR    = 0x08037974
FUNC_RENAME_OLD     = 'count_gy_cards_by_field6'
FUNC_RENAME_NEW     = 'count_field_zone_cards_by_field6'

# ---------------------------------------------------------------------------
# E. PLATE_FULL: (func_addr, new_plate_ascii_text)
#    11 functions in Seg-4a (pure ASCII, no FUN_/CJK)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: find_field_zone_slot_with_equip_type (0x08037904)
    (0x08037904,
     'find_field_zone_slot_with_equip_type: Scan field array C'
     ' (gP1FieldArrayCBase=gP1LP+0x120, count at gP1LP+0x0c)'
     ' for first card with extended field6==0x16 (equip-type field spell).'
     ' Returns 0-based slot index; returns -1 if not found. Skips card_id==0 slots.'
     ' Symmetric sibling to find_field_zone_slot_with_fieldspell (0x08037894, Seg-3);'
     ' only difference is field6 check value (0x16 vs 0x17). Pure read-only.'
     ' r0=u8 player_id [0..1]. Returns s32 slot_index (>=0 if found, -1 if not).'
     ' Constants: gP1LifePoints; gP1FieldArrayCBase=0x0201c600; PLAYER_BLOCK_STRIDE=0x868.'),

    # PLATE-2: count_field_zone_cards_by_field6 (0x08037974) -- renamed from count_gy_cards_by_field6
    (0x08037974,
     'count_field_zone_cards_by_field6: Iterates field zone array C for player'
     ' (gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x120,'
     ' count at +0x0c). Extracts bits[12:0] as card_id per entry, calls'
     ' get_card_extended_stat_field6; if field6==r8 (non-APCS, caller-set via mov r8,r1),'
     ' increments counter. Returns match count. Symmetric to count_field_zone_cards_by_field7'
     ' (same gP1FieldArrayCBase base, different stat field). Pure read-only.'
     ' r0=u8 player_id [0..1]; r1 (non-APCS saved r8)=u8 field6_target.'
     ' Returns u32 count.'
     ' Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.'),

    # PLATE-3: count_field_zone_cards_by_field7 (0x080379d0)
    (0x080379d0,
     'count_field_zone_cards_by_field7: Iterates field zone array C for player'
     ' (gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x120, count at +0x0c).'
     ' Extracts bits[12:0] as card_id; calls get_card_extended_stat_field7;'
     ' if field7==r8 (non-APCS, caller-set), increments counter.'
     ' Returns match count. Symmetric to count_field_zone_cards_by_field6. Pure read-only.'
     ' r0=u8 player_id [0..1]; r1 (non-APCS saved r8)=u8 field7_target.'
     ' Returns u32 count.'
     ' Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.'),

    # PLATE-4: count_valid_monster_pair_slots (0x08037a2c)
    (0x08037a2c,
     'count_valid_monster_pair_slots: Count zone slots in field array C for player'
     ' where check_card_id_is_normal_summon_type(card_id) is true (field1 bit check).'
     ' Reads gP1LP+player*0x868+0x120 (gP1FieldArrayCBase), count at +0x0c.'
     ' For each entry extracts card_id (bits[12:0]); calls check_card_id_is_normal_summon_type.'
     ' Returns match count. Pure read-only.'
     ' r0=u8 player_id [0..1]. Returns u32 count.'
     ' Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.'),

    # PLATE-5: find_zone_slot_idx_allowed_for_card (0x08037a8c)
    (0x08037a8c,
     'find_zone_slot_idx_allowed_for_card: Find field zone slot index in field array C'
     ' where check_card_is_equip_target_eligible(card_id) returns true for specified player.'
     ' Reads gP1LP+player*0x868+0x120 (gP1FieldArrayCBase), count at +0x0c.'
     ' Returns 0-based slot index; returns -1 if not found. Pure read-only.'
     ' r0=u8 player_id [0..1]. Returns s32 slot_index.'
     ' Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.'),

    # PLATE-6: count_field_zone_cards_with_field5 (0x08037ae4)
    (0x08037ae4,
     'count_field_zone_cards_with_field5: Count cards in field zone array C'
     ' for player where get_card_extended_stat_field5(card_id) is nonzero.'
     ' Reads gP1LP+player*0x868+0x120 (gP1FieldArrayCBase), count at +0x0c.'
     ' Returns match count. Pure read-only.'
     ' r0=u8 player_id [0..1]. Returns u32 count.'
     ' Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.'),

    # PLATE-7: count_monster_slots_with_field5_ge_threshold (0x08037b34)
    (0x08037b34,
     'count_monster_slots_with_field5_ge_threshold: Iterates monster zone cards for player'
     ' (gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x120,'
     ' count at +0x0c). Calls get_card_extended_stat_field5; if field5 >= threshold (r8'
     ' non-APCS, caller-set via mov r8,r1), increments counter. Returns match count.'
     ' Caller: find_empty_slot_for_card_id_dispatch (with r1=7). Pure read-only.'
     ' r0=u32 player_side [0..1]; r1=u32 field5_threshold [0..255] (non-APCS saved r8).'
     ' Returns u32 count.'
     ' Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.'),

    # PLATE-8: get_player_deck_flag_bit1 (0x08037b90)
    (0x08037b90,
     'get_player_deck_flag_bit1: Returns bit1 of deck status word for specified player.'
     ' Reads gP1LifePoints + (r0&1)*PLAYER_BLOCK_STRIDE + 0x11c (=0x8e*2), extracts bit1 via'
     ' lsrs #1 & 1. Pure read-only.'
     ' Callers: shuffle_hand_by_player_deck_flag (skip-deck-sort guard);'
     ' get_zone_card_attribute_by_type case_b (conditional 0/1 return).'
     ' r0=u32 packed_player_id (bit0=player index [0..1]).'
     ' Returns u32 (0 or 1).'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; deck_status_word_offset=0x11c.'),

    # PLATE-9: check_field_effect_zone_activation_eligible (0x08037bb4)
    (0x08037bb4,
     'check_field_effect_zone_activation_eligible: Check whether field-effect zone activation'
     ' is eligible for player. Guards:'
     ' (1) count_available_effect_zones(opposite, EYE_OF_TRUTH_CID=0x137b) == 0;'
     ' (2) count_available_effect_zones(opposite, MIND_ON_AIR_CID=0x17e7) == 0;'
     ' (3) gP1LifePoints+player*0x868+P1LP_BLOCK2_OFF_1CE8 check (activation state guard);'
     ' (4) count_field_copies_of_card(player, RESPECT_PLAY_CID=0x135e) == 0.'
     ' Returns 1 if all guards pass (eligible), 0 otherwise.'
     ' r0=u8 player_id [0..1]. Returns bool.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; P1LP_BLOCK2_OFF_1CE8=0x1ce8;'
     ' EYE_OF_TRUTH_CID=0x137b; MIND_ON_AIR_CID=0x17e7; RESPECT_PLAY_CID=0x135e.'),

    # PLATE-10: shuffle_hand_by_player_deck_flag (0x08037c20)
    (0x08037c20,
     'shuffle_hand_by_player_deck_flag: Shuffle (randomize) hand cards for player'
     ' if deck flag bit1 is clear (deck not sorted).'
     ' Calls get_player_deck_flag_bit1(player_id); if nonzero (bit1 set) returns immediately.'
     ' Otherwise performs Fisher-Yates shuffle on hand slot array'
     ' (gDuelFieldSlots+player*0x868, count at gP1LP+0x868*player+0x0c).'
     ' Uses prng for random index selection.'
     ' r0=u8 player_id [0..1]. Returns void.'
     ' Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; gDuelFieldSlots=0x0201c510.'),

    # PLATE-11: compute_zone_effect_atk_delta (0x08037c9c)
    (0x08037c9c,
     'compute_zone_effect_atk_delta: Compute ATK/DEF score delta for zone effect card.'
     ' For field-spell cards (YAMI_CID=0x10f5..MOLTEN_DESTRUCTION_CID=0x1346 range):'
     '   looks up field_spell_atk_bonus_table[card_id+FIELD_SPELL_TABLE_IDX_BIAS][field_level].'
     ' Binary-search card dispatch within the range:'
     '   GAIA_POWER_CID=0x1344, MYSTIC_PLASMA_ZONE_CID=0x1349.'
     ' For NECROVALLEY_CID=0x159d / HARPIES_HUNTING_GROUND_CID=0x183f zone effects:'
     '   applies ZONE_EFFECT_ATK_PENALTY_500=-500 as ATK/DEF delta for opponent gravekeeper check.'
     ' r0=u8 player_id [0..1]; r1=u16 card_id; r2=u8 field_level [0..23].'
     ' Returns s32 score_delta.'
     ' Constants: gP1LifePoints; gDuelFieldSlots=0x0201c510; PLAYER_BLOCK_STRIDE=0x868;'
     ' field_spell_atk_bonus_table (ROM 0x09e3ef74); FIELD_SPELL_TABLE_IDX_BIAS=0xffffef10;'
     ' YAMI_CID=0x10f5; MOLTEN_DESTRUCTION_CID=0x1346; GAIA_POWER_CID=0x1344;'
     ' MYSTIC_PLASMA_ZONE_CID=0x1349; NECROVALLEY_CID=0x159d;'
     ' HARPIES_HUNTING_GROUND_CID=0x183f; ZONE_EFFECT_ATK_PENALTY_500=0xfffffe70.'),

]  # end PLATE_FULL (11 entries)

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

def _apply_carve_label(target_addr, target_label, slot_addr, slot_label):
    """Create USER-label at carve target + DATA ref from slot to target + slot label."""
    a_target = _addr(target_addr)
    a_slot   = _addr(slot_addr)
    sym_tbl  = currentProgram.getSymbolTable()
    ref_mgr  = currentProgram.getReferenceManager()

    if not _check(slot_addr, target_addr, slot_label):
        print("[SKIP] CARVE REF 0x%08x (%s) value mismatch" % (slot_addr, slot_label))
        return

    if DRY:
        print("[dry] CARVE_LABEL 0x%08x -> %s" % (target_addr, target_label))
        print("[dry] CARVE REF 0x%08x -> 0x%08x  label=%s" % (slot_addr, target_addr, slot_label))
        return

    # create label at carve target (ROM data table)
    existing_tgt = sym_tbl.getSymbols(a_target)
    names_tgt = [s.getName() for s in existing_tgt]
    if target_label not in names_tgt:
        sym_tbl.createLabel(a_target, target_label, SourceType.USER_DEFINED)
    print("[LBL] 0x%08x -> %s" % (target_addr, target_label))

    # create slot label
    existing = sym_tbl.getSymbols(a_slot)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # add DATA reference from slot to target
    ref = ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_mgr.setPrimary(ref, True)
    print("[REF] 0x%08x -> 0x%08x  (%s) [carve label]" % (slot_addr, target_addr, slot_label))

def _apply_func_rename(func_addr, old_name, new_name):
    """Rename Ghidra function from old_name to new_name."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    fn = listing.getFunctionAt(a)

    if DRY:
        if fn is not None:
            print("[dry] FUNC_RENAME 0x%08x  %s -> %s" % (func_addr, fn.getName(), new_name))
        else:
            print("[dry] FUNC_RENAME 0x%08x  (no fn found at addr)" % func_addr)
        return

    if fn is None:
        print("[WARN] FUNC_RENAME 0x%08x: no function found at address" % func_addr)
        return

    current_name = fn.getName()
    if current_name == new_name:
        print("[SKIP] FUNC_RENAME 0x%08x: already named %s" % (func_addr, new_name))
        return

    fn.setName(new_name, SourceType.USER_DEFINED)
    print("[REN ] 0x%08x  %s -> %s" % (func_addr, current_name, new_name))

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
    print("=== RefineF03Seg4aSlots (DRY=%s) ===" % DRY)
    print("  Seg-4a: 0x08037904..0x08037ec0, 12 fn, field zone slot query + ATK delta")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
    print("  EQ done: %d" % len(EQ_SLOTS))

    # B1. REF_SLOTS -- PTR_gP1LifePoints_* (10 slots)
    print("\n--- B1. REF_SLOTS lp_ptr (%d) ---" % len(REF_LP_SLOTS))
    for (slot_addr, slot_label) in REF_LP_SLOTS:
        _apply_ref_lp(slot_addr, LP_TARGET, slot_label)
    print("  REF lp_ptr done: %d" % len(REF_LP_SLOTS))

    # B2. CARVE_LABEL + REF (carve sync for field_spell_atk_bonus_table)
    print("\n--- B2. CARVE_LABEL + REF (1) ---")
    _apply_carve_label(CARVE_TARGET_ADDR, CARVE_TARGET_LABEL, CARVE_SLOT_ADDR, CARVE_SLOT_LABEL)

    # D. FUNC_RENAME
    print("\n--- D. FUNC_RENAME (1) ---")
    _apply_func_rename(FUNC_RENAME_ADDR, FUNC_RENAME_OLD, FUNC_RENAME_NEW)

    # E. PLATE_FULL
    print("\n--- E. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)
    print("  PLATE_FULL done: %d" % len(PLATE_FULL))

    print("\n=== RefineF03Seg4aSlots DONE ===")
    print("  EQ=%d  REF_LP=%d  CARVE_REF=1  FUNC_RENAME=1  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_LP_SLOTS), len(PLATE_FULL)))

main()
