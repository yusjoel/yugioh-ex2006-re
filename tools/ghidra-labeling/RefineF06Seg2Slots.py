# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg2Slots.py -- F06 Seg-2 (0x080541cc..0x08054ba0)
#   check_equip_slot_eligible_by_side_setcode_prereqs_and_type
#   check_equip_slot_eligible_by_field8_9_and_type
#   check_equip_slot_eligible_by_opposite_side_and_field6
#   check_equip_slot_eligible_by_field8_9_prereqs_and_type
#   check_equip_slot_eligible_by_opposite_side_whitelist
#   check_equip_slot_eligible_by_field6_zero_and_type
#   check_equip_slot_eligible_by_icid_mismatch_and_prereqs
#   check_equip_slot_eligible_by_no_field8_9_and_monster
#   check_equip_slot_eligible_by_icid_match
#   check_equip_slot_eligible_by_monster_and_chain_score
#   check_equip_slot_eligible_by_pair_count_triple
#   [check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight -- disasm'd separately]
#   check_equip_slot_type_and_score_match
#   check_equip_slot_eligible_with_prereqs_and_score_guard
#   check_equip_slot_eligible_with_score_guard
#   check_equip_slot_score_and_field6_flags
#   check_equip_slot_eligible_by_evolution_target_and_space
#   check_equip_slot_eligible_by_same_side_prereqs_and_type
#   check_equip_slot_eligible_by_same_side_and_prereqs
#   check_equip_slot_eligible_by_card_specific_activation
#   check_equip_slot_eligible_by_union_type_and_occupied
#   check_equip_slot_eligible_with_whitelist_prereqs_and_type
#   invoke_serial_spell_effect_node_handler
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (52 slots = 47 reuse + 5 new)
#   B. PLATE_SUBS -- substring FUN_ -> current name
#
# New constants added to constants/*.inc before running:
#   card_info.inc: TRICKYS_MAGIC_4_CID=0x180e / GILFORD_THE_LEGEND_CID=0x1938
#                  SERIAL_SPELL_CID=0x183e / THE_TRICKY_TARGET_SLOT_PATTERN=0xc0300000
#                  ULTIMATE_BASEBALL_KID_CID=0x17e1
#   duel_field.inc: EQUIP_FLAG_TARGET_ICID_TABLE_OFF=0x10b0

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
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values verified against ROM via python struct.unpack_from('<I', rom, addr-0x08000000).
#    const_name must be a pre-existing .equ in constants/*.inc.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ---- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) x21 ----
    (0x08054224, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_setcode_prereqs_and_type_stride'),
    (0x08054274, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field8_9_and_type_stride'),
    (0x080542c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_and_field6_stride'),
    (0x08054354, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field8_9_prereqs_and_type_stride'),
    (0x080543a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_whitelist_stride'),
    (0x080543fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_zero_and_type_stride'),
    (0x08054458, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_icid_mismatch_and_prereqs_stride'),
    (0x080544c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_no_field8_9_and_monster_stride'),
    (0x080544f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_icid_match_stride'),
    (0x08054560, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_monster_and_chain_score_stride'),
    (0x080545cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_pair_count_triple_stride'),
    (0x08054650, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight_stride'),
    (0x080546ac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_type_and_score_match_stride'),
    (0x0805473c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_score_guard_stride'),
    (0x08054784, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_score_and_field6_flags_stride'),
    (0x08054824, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_evolution_target_and_space_stride'),
    (0x08054888, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_same_side_prereqs_and_type_stride'),
    (0x080548dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_same_side_and_prereqs_stride'),
    (0x08054940, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_specific_activation_stride'),
    (0x08054b08, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_union_type_and_occupied_stride'),
    (0x08054b70, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_whitelist_prereqs_and_type_stride'),

    # ---- gDuelFieldSlots = 0x0201c510 (ewram.inc) x22 ----
    (0x08054228, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_setcode_prereqs_and_type_slots'),
    (0x08054278, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field8_9_and_type_slots'),
    (0x080542c4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_and_field6_slots'),
    (0x08054358, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field8_9_prereqs_and_type_slots'),
    (0x080543a8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_whitelist_slots'),
    (0x08054400, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_zero_and_type_slots'),
    (0x0805445c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_icid_mismatch_and_prereqs_slots'),
    (0x080544c8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_no_field8_9_and_monster_slots'),
    (0x080544fc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_icid_match_slots'),
    (0x08054564, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_monster_and_chain_score_slots'),
    (0x080545d0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_pair_count_triple_slots_a'),
    (0x08054610, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_pair_count_triple_slots_b'),
    (0x08054654, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight_slots'),
    (0x080546b0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_type_and_score_match_slots'),
    (0x08054740, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_score_guard_slots'),
    (0x08054788, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_score_and_field6_flags_slots'),
    (0x08054828, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_evolution_target_and_space_slots'),
    (0x0805488c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_same_side_prereqs_and_type_slots'),
    (0x080548e0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_same_side_and_prereqs_slots'),
    (0x08054944, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_specific_activation_slots'),
    (0x08054b0c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_union_type_and_occupied_slots'),
    (0x08054b74, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_whitelist_prereqs_and_type_slots'),

    # ---- SCROLLBAR_KEEP_BITS_8_0 = 0x000001ff (gl_scrollbar.inc) x2 ----
    (0x08054a2c, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0', 'check_equip_slot_eligible_by_card_specific_activation_field_mask_a'),
    (0x08054ab4, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0', 'check_equip_slot_eligible_by_card_specific_activation_field_mask_a_b'),

    # ---- SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (gl_scrollbar.inc) x2 ----
    (0x08054a30, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'check_equip_slot_eligible_by_card_specific_activation_clear_mask'),
    (0x08054ab8, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6', 'check_equip_slot_eligible_by_card_specific_activation_clear_mask_b'),

    # ---- NEW constants (5 slots) ----
    # TRICKYS_MAGIC_4_CID = 0x0000180e (card_info.inc new)
    (0x08054948, 0x0000180e, 'TRICKYS_MAGIC_4_CID', 'check_equip_slot_eligible_by_card_specific_activation_icid_trickys'),
    # GILFORD_THE_LEGEND_CID = 0x00001938 (card_info.inc new)
    (0x0805495c, 0x00001938, 'GILFORD_THE_LEGEND_CID', 'check_equip_slot_eligible_by_card_specific_activation_icid_gilford'),
    # THE_TRICKY_TARGET_SLOT_PATTERN = 0xc0300000 (card_info.inc new)
    (0x080549b4, 0xc0300000, 'THE_TRICKY_TARGET_SLOT_PATTERN', 'check_equip_slot_eligible_by_card_specific_activation_tricky_pattern'),
    # EQUIP_FLAG_TARGET_ICID_TABLE_OFF = 0x000010b0 (duel_field.inc new)
    (0x08054ab0, 0x000010b0, 'EQUIP_FLAG_TARGET_ICID_TABLE_OFF', 'check_equip_slot_eligible_by_card_specific_activation_table_off'),
    # SERIAL_SPELL_CID = 0x0000183e (card_info.inc new)
    (0x08054b9c, 0x0000183e, 'SERIAL_SPELL_CID', 'invoke_serial_spell_effect_node_handler_icid'),
]

# ---------------------------------------------------------------------------
# B. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Substring replace stale FUN_ in existing plate comment.
#    WARN treated as FAIL (no-op logged).
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # check_equip_slot_eligible_by_same_side_and_prereqs (0x08054898):
    # old: "called by FUN_0809077c (callback iterator)"
    # new: "called by invoke_count_zone_pair_hits_full_range (0x0809077c, callback iterator)"
    (0x08054898, 'FUN_0809077c', 'invoke_count_zone_pair_hits_full_range (0x0809077c,'),
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
    print("=== RefineF06Seg2Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nD = 0

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS (%d slots) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s want=0x%x)" % (slot_int, err, cname, value))
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
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # --- B. PLATE_SUBS ---
    print("--- B. PLATE_SUBS (%d subs) ---" % len(PLATE_SUBS))
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[B FAIL] no CodeUnit @ 0x%08x" % func_int)
            continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[B SKIP] no plate @ 0x%08x" % func_int)
            continue
        if old_s not in plate:
            print("[B WARN] '%s' not found in plate @ 0x%08x -- TREAT AS FAIL (sub not applied)" % (old_s, func_int))
            continue
        if DRY:
            print("[B dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nD += 1
            continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[B ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
        nD += 1

    print("[done] A=%d PLATE_SUBS=%d (DRY=%s)" % (nA, nD, DRY))


main()
