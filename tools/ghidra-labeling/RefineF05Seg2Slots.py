# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg2Slots.py -- file 05 Seg-2 (0x0804a5b8..0x0804ad48)
#   12 functions:
#     enqueue_monster_zone_equip_sprites_and_lp_counters (0x4a5b8)
#     enqueue_sprite_attr_type10_halfword                (0x4a754)
#     increment_lp_bar_display_counter                   (0x4a76c)
#     increment_lp_bar_counter_no_player                 (0x4a7f8)
#     decrement_lp_bar_display_counter                   (0x4a870)
#     set_slot_occupy_bit_with_sprite_update             (0x4a8d8)
#     set_player_state_bit_with_sprite_update            (0x4a918)
#     set_field_slot_bit_with_sprite_update              (0x4a970)
#     map_field8_to_card_type_category                   (0x4a9dc, contains switchD_0804a9ee)
#     check_card_pair_allowed                            (0x4ab4c)
#     map_card_id_to_banlist_canonical                   (0x4ac58)
#     check_card_ids_banlist_compatible                  (0x4acc8)
#
# Sections:
#   A. EQ_SLOTS  (56 pure EQ + 34 card_id EQ = 90 with duplicates) -- data-equate + slot rename
#   B. REF_SLOTS (1 slot) -- switchD table ptr
#   C. CARD_ID_SLOTS (34 slots) -- equate with card_info.inc constants + EOL card names
#   D. PLATE_SUBS (4 FUN_ -> current name substitutions, 3 functions)
#
# All slot values pre-verified against ROM via python struct.unpack.
# All EOL/plate text is pure ASCII (no CJK).
#
# New constants written to constants/*.inc before running this script:
#   ewram.inc    +2: LP_BAR_DISPLAY_CTR_OFF=0x4c4, LP_BAR_ANIM_STATE_OFF=0x4cc
#   duel_field.inc +2: EQUIP_SPRITE_X_DELTA_A=0xffffe730, EQUIP_SPRITE_X_DELTA_B=0xffffe32c
#   oam_attr.inc +2: OAM_PLAYER_STATE_BIT_SPRITE_P1=0x8022, OAM_FIELD_SLOT_BIT_SPRITE_P1=0x802a
#   card_info.inc +5: POLYMERIZATION_CID_1303=0x1303, CYBER_HARPIE_LADY_CID=0x1477,
#                     HARPIE_LADY_1_CID=0x182a, HARPIE_LADY_3_CID=0x182c,
#                     BEWD_RANGE_CHECK_BIAS=0xfffff05a
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
#    All values pre-verified against ROM. const_name must exist in constants/*.inc.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- enqueue_monster_zone_equip_sprites_and_lp_counters pool (0x4a730..0x4a750, 9 slots) ---
    (0x0804a730, 0x0201c4e0, 'gP1LifePoints',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_lp_base'),
    (0x0804a734, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_player_off'),
    (0x0804a738, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_stride'),
    (0x0804a73c, 0x0201c4f4, 'gP1HandCountBase',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_hand_cnt'),
    (0x0804a740, 0xffffe730, 'EQUIP_SPRITE_X_DELTA_A',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_delta_a'),
    (0x0804a744, 0xffffe32c, 'EQUIP_SPRITE_X_DELTA_B',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_delta_b'),
    (0x0804a748, 0x0201c4f0, 'gP1SlotCountBase',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_slot_cnt'),
    (0x0804a74c, 0x0201c740, 'gP1SlotSetCodeArray',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_set_code'),
    (0x0804a750, 0x000012a1, 'PARASITE_PARACIDE_CID',
     'enqueue_monster_zone_equip_sprites_and_lp_counters_cid_check'),
    # --- increment_lp_bar_display_counter pool (0x4a7c4..0x4a7d8, 6 slots) ---
    (0x0804a7c4, 0x0201b290, 'gDuelPhaseFlags',
     'increment_lp_bar_display_counter_phase_flags'),
    (0x0804a7c8, 0x0201c4e0, 'gP1LifePoints',
     'increment_lp_bar_display_counter_lp_base'),
    (0x0804a7cc, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'increment_lp_bar_display_counter_block2_off'),
    (0x0804a7d0, 0x0201e2a0, 'gDuelCardCtxBase',
     'increment_lp_bar_display_counter_card_ctx'),
    (0x0804a7d4, 0x000004c4, 'LP_BAR_DISPLAY_CTR_OFF',
     'increment_lp_bar_display_counter_ctr_off'),
    (0x0804a7d8, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'increment_lp_bar_display_counter_anim_off'),
    # --- increment_lp_bar_counter_no_player pool (0x4a840..0x4a850, 5 slots) ---
    (0x0804a840, 0x0201b290, 'gDuelPhaseFlags',
     'increment_lp_bar_counter_no_player_phase_flags'),
    (0x0804a844, 0x0201c4e0, 'gP1LifePoints',
     'increment_lp_bar_counter_no_player_lp_base'),
    (0x0804a848, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'increment_lp_bar_counter_no_player_block2_off'),
    (0x0804a84c, 0x0201e2a0, 'gDuelCardCtxBase',
     'increment_lp_bar_counter_no_player_card_ctx'),
    (0x0804a850, 0x000004c4, 'LP_BAR_DISPLAY_CTR_OFF',
     'increment_lp_bar_counter_no_player_ctr_off'),
    # --- decrement_lp_bar_display_counter pool (0x4a8a8..0x4a8b8, 5 slots) ---
    (0x0804a8a8, 0x0201b290, 'gDuelPhaseFlags',
     'decrement_lp_bar_display_counter_phase_flags'),
    (0x0804a8ac, 0x0201c4e0, 'gP1LifePoints',
     'decrement_lp_bar_display_counter_lp_base'),
    (0x0804a8b0, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'decrement_lp_bar_display_counter_block2_off'),
    (0x0804a8b4, 0x0201e2a0, 'gDuelCardCtxBase',
     'decrement_lp_bar_display_counter_card_ctx'),
    (0x0804a8b8, 0x000004c4, 'LP_BAR_DISPLAY_CTR_OFF',
     'decrement_lp_bar_display_counter_ctr_off'),
    # --- set_slot_occupy_bit_with_sprite_update pool (0x4a910..0x4a914, 2 slots) ---
    (0x0804a910, 0x0201c4e0, 'gP1LifePoints',
     'set_slot_occupy_bit_with_sprite_update_lp_base'),
    (0x0804a914, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'set_slot_occupy_bit_with_sprite_update_flags_off'),
    # --- set_player_state_bit_with_sprite_update pool (0x4a964..0x4a96c, 3 slots) ---
    (0x0804a964, 0x0201c4e0, 'gP1LifePoints',
     'set_player_state_bit_with_sprite_update_lp_base'),
    (0x0804a968, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'set_player_state_bit_with_sprite_update_stride'),
    (0x0804a96c, 0x00008022, 'OAM_PLAYER_STATE_BIT_SPRITE_P1',
     'set_player_state_bit_with_sprite_update_oam_p1'),
    # --- set_field_slot_bit_with_sprite_update pool (0x4a9d0..0x4a9d8, 3 slots) ---
    (0x0804a9d0, 0x0201c4e0, 'gP1LifePoints',
     'set_field_slot_bit_with_sprite_update_lp_base'),
    (0x0804a9d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'set_field_slot_bit_with_sprite_update_stride'),
    (0x0804a9d8, 0x0000802a, 'OAM_FIELD_SLOT_BIT_SPRITE_P1',
     'set_field_slot_bit_with_sprite_update_oam_p1'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    DAT_0804a9f0 = switch table ptr -> switchD_0804a9ee__switchdataD_0804a9f4
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0804a9f0, 0x0804a9f4,
     'switchD_0804a9ee__switchdataD_0804a9f4',
     'map_field8_to_card_type_category_switch_table'),
]

# ---------------------------------------------------------------------------
# C. CARD_ID_SLOTS: (slot_addr, value, const_name, eol_ascii)
#    34 card_id slots; equate + slot rename + EOL card name annotation.
#    All EOL text is pure ASCII.
# ---------------------------------------------------------------------------
CARD_ID_SLOTS = [
    # check_card_pair_allowed (0x4ab4c) first pass BST
    (0x0804ab80, 0x000012e5, 'POLYMERIZATION_CID',
     'check_card_pair_allowed_poly_cid_a',
     'Polymerization (pw=24094653, card_0669 slot=0x12e5)'),
    (0x0804ab84, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',
     'check_card_pair_allowed_dm_cid_0fc9_a',
     'Dark Magician alt print (pw=46986414, card_0730 slot=0x0fc9)'),
    (0x0804ab88, 0xfffff05a, 'BEWD_RANGE_CHECK_BIAS',
     'check_card_pair_allowed_bewd_range_bias_a',
     'range bias -0xfa6: adds+cmp tests if cid in {0xfa6,0xfa7} (BEWD/gap range)'),
    (0x0804ab9c, 0x00000fe4, 'HARPIE_LADY_CID',
     'check_card_pair_allowed_harpie_lady_cid_a',
     'Harpie Lady (pw=76812113, card_0301 slot=0x0fe4)'),
    (0x0804aba0, 0x000010f4, 'UMI_CARD_ID',
     'check_card_pair_allowed_umi_cid_a',
     'Umi (pw=22702055, slot=0x10f4)'),
    (0x0804abbc, 0x00001477, 'CYBER_HARPIE_LADY_CID',
     'check_card_pair_allowed_cyber_harpie_cid_a',
     'Cyber Harpie Lady (pw=80316585, card_0951 slot=0x1477)'),
    (0x0804abc0, 0x00001303, 'POLYMERIZATION_CID_1303',
     'check_card_pair_allowed_poly_cid_1303_a',
     'Polymerization 2nd print (pw=24094653, card_0689 slot=0x1303)'),
    (0x0804abc4, 0x0000142d, 'DARK_MAGICIAN_CID_142D',
     'check_card_pair_allowed_dm_cid_142d_a',
     'Dark Magician (pw=46986414, card_3256 slot=0x142d)'),
    (0x0804abe0, 0x0000150b, 'A_LEGENDARY_OCEAN_CARD_ID',
     'check_card_pair_allowed_alo_cid_a',
     'A Legendary Ocean (pw=295517, slot=0x150b)'),
    (0x0804abe4, 0x0000182c, 'HARPIE_LADY_3_CID',
     'check_card_pair_allowed_harpie_lady3_cid_a',
     'Harpie Lady 3 (pw=54415063, card_1712 slot=0x182c)'),
    # check_card_pair_allowed second pass BST (duplicate constants)
    (0x0804abf8, 0x000012e5, 'POLYMERIZATION_CID',
     'check_card_pair_allowed_poly_cid_b',
     'Polymerization (pw=24094653, card_0669 slot=0x12e5)'),
    (0x0804ac0c, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',
     'check_card_pair_allowed_dm_cid_0fc9_b',
     'Dark Magician alt print (pw=46986414, card_0730 slot=0x0fc9)'),
    (0x0804ac10, 0x0000142d, 'DARK_MAGICIAN_CID_142D',
     'check_card_pair_allowed_dm_cid_142d_b',
     'Dark Magician (pw=46986414, card_3256 slot=0x142d)'),
    (0x0804ac34, 0x00000fe4, 'HARPIE_LADY_CID',
     'check_card_pair_allowed_harpie_lady_cid_b',
     'Harpie Lady (pw=76812113, card_0301 slot=0x0fe4)'),
    (0x0804ac38, 0x00001477, 'CYBER_HARPIE_LADY_CID',
     'check_card_pair_allowed_cyber_harpie_cid_b',
     'Cyber Harpie Lady (pw=80316585, card_0951 slot=0x1477)'),
    (0x0804ac3c, 0x0000182a, 'HARPIE_LADY_1_CID',
     'check_card_pair_allowed_harpie_lady1_cid',
     'Harpie Lady 1 (pw=91932350, card_1710 slot=0x182a)'),
    (0x0804ac50, 0x000010f4, 'UMI_CARD_ID',
     'check_card_pair_allowed_umi_cid_b',
     'Umi (pw=22702055, slot=0x10f4)'),
    (0x0804ac54, 0x0000150b, 'A_LEGENDARY_OCEAN_CARD_ID',
     'check_card_pair_allowed_alo_cid_b',
     'A Legendary Ocean (pw=295517, slot=0x150b)'),
    # map_card_id_to_banlist_canonical (0x4ac58) BST
    (0x0804ac70, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',
     'map_card_id_to_banlist_canonical_dm_cid_0fc9',
     'Dark Magician alt print (pw=46986414, card_0730 slot=0x0fc9)'),
    (0x0804ac74, 0x00000fa6, 'eval_gap_cid_0fa6',
     'map_card_id_to_banlist_canonical_gap_cid',
     'gap slot 0x0fa6 (not in card-stats.s; between 0x0fa5 and BEWD 0x0fa7)'),
    (0x0804ac78, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID',
     'map_card_id_to_banlist_canonical_bewd_cid',
     'Blue-Eyes White Dragon (pw=89631139, card_0001 slot=0x0fa7)'),
    (0x0804ac90, 0x00001303, 'POLYMERIZATION_CID_1303',
     'map_card_id_to_banlist_canonical_poly_1303',
     'Polymerization 2nd print (pw=24094653, card_0689 slot=0x1303)'),
    (0x0804ac94, 0x000012e5, 'POLYMERIZATION_CID',
     'map_card_id_to_banlist_canonical_poly_12e5',
     'Polymerization (pw=24094653, card_0669 slot=0x12e5)'),
    (0x0804aca0, 0x0000142d, 'DARK_MAGICIAN_CID_142D',
     'map_card_id_to_banlist_canonical_dm_142d',
     'Dark Magician (pw=46986414, card_3256 slot=0x142d)'),
    (0x0804aca8, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID',
     'map_card_id_to_banlist_canonical_bewd_cid_b',
     'Blue-Eyes White Dragon (pw=89631139, card_0001 slot=0x0fa7)'),
    (0x0804acb4, 0x000012e5, 'POLYMERIZATION_CID',
     'map_card_id_to_banlist_canonical_poly_b',
     'Polymerization (pw=24094653, card_0669 slot=0x12e5)'),
    (0x0804acbc, 0x0000142d, 'DARK_MAGICIAN_CID_142D',
     'map_card_id_to_banlist_canonical_dm_142d_b',
     'Dark Magician (pw=46986414, card_3256 slot=0x142d)'),
    # check_card_ids_banlist_compatible (0x4acc8) BST
    (0x0804acf0, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',
     'check_card_ids_banlist_compatible_dm_0fc9',
     'Dark Magician alt print (pw=46986414, card_0730 slot=0x0fc9)'),
    (0x0804acf4, 0xfffff05a, 'BEWD_RANGE_CHECK_BIAS',
     'check_card_ids_banlist_compatible_bewd_range_bias',
     'range bias -0xfa6: adds+cmp tests if cid in {0xfa6,0xfa7} (BEWD/gap range)'),
    (0x0804ad0c, 0x00001303, 'POLYMERIZATION_CID_1303',
     'check_card_ids_banlist_compatible_poly_1303',
     'Polymerization 2nd print (pw=24094653, card_0689 slot=0x1303)'),
    (0x0804ad18, 0x0000142d, 'DARK_MAGICIAN_CID_142D',
     'check_card_ids_banlist_compatible_dm_142d_a',
     'Dark Magician (pw=46986414, card_3256 slot=0x142d)'),
    (0x0804ad2c, 0x000012e5, 'POLYMERIZATION_CID',
     'check_card_ids_banlist_compatible_poly_12e5',
     'Polymerization (pw=24094653, card_0669 slot=0x12e5)'),
    (0x0804ad40, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9',
     'check_card_ids_banlist_compatible_dm_0fc9_b',
     'Dark Magician alt print (pw=46986414, card_0730 slot=0x0fc9)'),
    (0x0804ad44, 0x0000142d, 'DARK_MAGICIAN_CID_142D',
     'check_card_ids_banlist_compatible_dm_142d_b',
     'Dark Magician (pw=46986414, card_3256 slot=0x142d)'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Replace FUN_ stale names in PLATE_COMMENT. Pure ASCII.
#    3 functions targeted, 4 substitutions total.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # enqueue_monster_zone_equip_sprites_and_lp_counters (0x4a5b8)
    # "Called by FUN_080718c4 (LP bar update chain)..."
    (0x0804a5b8, 'FUN_080718c4', 'forward_equip_monster_zone_sprites_and_lp'),
    # set_slot_occupy_bit_with_sprite_update (0x4a8d8)
    # "Called by FUN_08098564 (card display state machine) and FUN_08098a88 (duel_field)."
    (0x0804a8d8, 'FUN_08098564', 'tick_card_activation_phase_by_state'),
    (0x0804a8d8, 'FUN_08098a88', 'tick_equip_zone_activation_display_state'),
    # check_card_field5_is_nonzero (0x4ad48) -- Seg-3 first fn, cross-boundary plate fix
    # "Adjacent sibling FUN_0804ad5c applies similar conversion..."
    (0x0804ad48, 'FUN_0804ad5c', 'check_card_field8_is_zero'),
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
    print("=== RefineF05Seg2Slots (DRY=%s) ===" % DRY)
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
            nA_fail += 1
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1
            continue
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
            nB_fail += 1
            continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1
            continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label))
        nB += 1

    # --- C. CARD_ID_SLOTS ---
    print("--- C. CARD_ID_SLOTS (%d entries) ---" % len(CARD_ID_SLOTS))
    for slot_int, value, cname, label, eol in CARD_ID_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[C FAIL] 0x%08x: %s (const=%s)" % (slot_int, err, cname))
            nC_fail += 1
            continue
        if DRY:
            print("[C dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nC += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s (%s=0x%x)" % (slot_int, label, cname, value))
        nC += 1

    # --- D. PLATE_SUBS ---
    print("--- D. PLATE_SUBS (%d entries) ---" % len(PLATE_SUBS))
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int)
            continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[D SKIP] no plate @ 0x%08x (looking for '%s')" % (func_int, old_s))
            nD_skip += 1
            continue
        if old_s not in plate:
            print("[D SKIP] '%s' not in plate @ 0x%08x" % (old_s, func_int))
            nD_skip += 1
            continue
        if DRY:
            print("[D dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nD += 1
            continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
        nD += 1

    print("[done] A=%d(fail=%d) B=%d(fail=%d) C=%d(fail=%d) D=%d(skip=%d) DRY=%s" % (
        nA, nA_fail, nB, nB_fail, nC, nC_fail, nD, nD_skip, DRY))


main()
