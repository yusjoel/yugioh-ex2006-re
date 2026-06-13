# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg7Slots.py -- file-05 Seg-7 (0x0804ffba..0x08050e40)
#   check_slot_zone_bit* + eligible_type_and_card_match resource eligibility cluster
#
# Sections:
#   A. EQ_SLOTS  -- 69 slots (21 PLAYER_BLOCK_STRIDE + 20 gDuelFieldSlots + 6 reuse + 22 new CID)
#   B. RENAME_SLOTS -- 3 slots (conflict/mask values with EOL)
#   C. PLATE_SUBS -- update plate comments (3 stale FUN_ replacements across 2 functions)
#
# All EOL/plate text is pure ASCII. No REF_SLOTS, no carve, no disasm.
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

def _addr(offset):
    return toAddr(offset)

def _check(addr_int, expected_val, label):
    """Verify ROM word at addr matches expected value; return True if ok."""
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xffffffff
        if actual != (expected_val & 0xffffffff):
            print("FAIL value_check %s @0x%08x: expected=0x%08x actual=0x%08x" % (
                label, addr_int, expected_val & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("FAIL value_check %s @0x%08x: exception %s" % (label, addr_int, str(e)))
        return False

def apply_eq_slot(slot_addr, value, const_name, slot_label):
    """Create equate + label at slot_addr."""
    if not _check(slot_addr, value, const_name):
        return False
    if DRY:
        print("DRY EQ 0x%08x %s = %s" % (slot_addr, slot_label, const_name))
        return True
    try:
        eqtbl = currentProgram.getEquateTable()
        eq = eqtbl.getEquate(const_name)
        if eq is None:
            eq = eqtbl.createEquate(const_name, value & 0xffffffff)
        eq.addReference(_addr(slot_addr), 0)
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("OK  EQ 0x%08x %s = %s" % (slot_addr, slot_label, const_name))
        return True
    except Exception as e:
        print("ERR EQ 0x%08x %s: %s" % (slot_addr, slot_label, str(e)))
        return False

def apply_rename_slot(slot_addr, label, eol_ascii):
    """Rename data slot and optionally set EOL comment (ASCII only)."""
    if DRY:
        print("DRY REN 0x%08x %s eol=%s" % (slot_addr, label, repr(eol_ascii)))
        return True
    try:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(slot_addr), label, SourceType.USER_DEFINED)
        if eol_ascii:
            listing = currentProgram.getListing()
            cu = listing.getCodeUnitAt(_addr(slot_addr))
            if cu:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_ascii)
        print("OK  REN 0x%08x %s" % (slot_addr, label))
        return True
    except Exception as e:
        print("ERR REN 0x%08x %s: %s" % (slot_addr, label, str(e)))
        return False

def apply_plate_sub(func_addr, old_sub, new_sub):
    """Replace old_sub with new_sub in existing plate comment (ASCII only)."""
    if DRY:
        print("DRY PLATE_SUB 0x%08x  '%s' -> '%s'" % (func_addr, old_sub, new_sub))
        return True
    try:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(_addr(func_addr))
        if cu is None:
            print("WARN PLATE_SUB 0x%08x: no code unit" % func_addr)
            return False
        old_text = cu.getComment(CodeUnit.PLATE_COMMENT)
        if old_text is None:
            print("WARN PLATE_SUB 0x%08x: no plate comment" % func_addr)
            return False
        if old_sub not in old_text:
            print("WARN PLATE_SUB 0x%08x: substring not found: '%s'" % (func_addr, old_sub))
            return False
        new_text = old_text.replace(old_sub, new_sub)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("OK  PLATE_SUB 0x%08x  '%s' -> '%s'" % (func_addr, old_sub, new_sub))
        return True
    except Exception as e:
        print("ERR PLATE_SUB 0x%08x: %s" % (func_addr, str(e)))
        return False

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- Group A: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc) ---
    # 21 slots: literal pool copies of per-player EWRAM stride
    (0x08050094, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_chain_type_d_node_exists_stride'),
    (0x08050120, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_field6_score_stride'),
    (0x0805017c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_type_only_stride'),
    (0x08050204, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_score_bound_stride_a'),
    (0x080502a0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_field6_and_pair_stride_a'),
    (0x08050354, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_slot_score_by_card_state_stride_a'),
    (0x08050514, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_slot_score_by_card_state_stride_b'),
    (0x080505c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_equip_slot_score_by_card_state_stride_c'),
    (0x0805079c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_type_and_card_match_stride'),
    (0x08050800, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_query_stride'),
    (0x0805085c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_field_match_stride'),
    (0x080508bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_query_with_occupied_stride'),
    (0x08050914, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_whitelist_query_stride'),
    (0x08050970, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_owner_path_split_stride'),
    (0x080509ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_then_prereqs_stride'),
    (0x08050a44, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_then_type_stride'),
    (0x08050ae0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_bst_stride'),
    (0x08050c44, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_bst_filter_stride_a'),
    (0x08050cb8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_bst_filter_stride_b'),
    (0x08050dd4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_whitelist_prereqs_0_stride'),
    (0x08050e30, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_whitelist_prereqs_1_stride'),

    # --- Group B: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc) ---
    # 20 slots: literal pool copies of duel field slots base address
    (0x08050098, 0x0201c510, 'gDuelFieldSlots', 'check_equip_chain_type_d_node_exists_gdfs'),
    (0x08050124, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_field6_score_gdfs'),
    (0x08050180, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_type_only_gdfs'),
    (0x08050208, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_score_bound_gdfs_a'),
    (0x080502a4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_field6_and_pair_gdfs_a'),
    (0x08050358, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_slot_score_by_card_state_gdfs_a'),
    (0x080505c4, 0x0201c510, 'gDuelFieldSlots', 'eval_equip_slot_score_by_card_state_gdfs_b'),
    (0x080507a0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_type_and_card_match_gdfs'),
    (0x08050804, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_query_gdfs'),
    (0x08050860, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_field_match_gdfs'),
    (0x080508c0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_query_with_occupied_gdfs'),
    (0x08050918, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_whitelist_query_gdfs'),
    (0x08050974, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_owner_path_split_gdfs'),
    (0x080509f0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_then_prereqs_gdfs'),
    (0x08050a48, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_then_type_gdfs'),
    (0x08050ae4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_bst_gdfs'),
    (0x08050c48, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_bst_filter_gdfs_a'),
    (0x08050cbc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_bst_filter_gdfs_b'),
    (0x08050dd8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_whitelist_prereqs_0_gdfs'),
    (0x08050e34, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_whitelist_prereqs_1_gdfs'),

    # --- Group C: Reuse existing equates (6 slots) ---
    # duel_field.inc: EQUIP_CHAIN_SENTINEL = 0xffff0000
    (0x080500a0, 0xffff0000, 'EQUIP_CHAIN_SENTINEL', 'check_equip_chain_type_d_node_exists_sentinel'),
    # card_info.inc: SLOT_CARD_EMPTY = 0x0000ffff
    (0x08050518, 0x0000ffff, 'SLOT_CARD_EMPTY', 'eval_equip_slot_score_find_target_sentinel'),
    # card_info.inc: ELEMENTAL_HERO_THUNDER_GIANT_CID = 0x000018c9
    (0x080503b8, 0x000018c9, 'ELEMENTAL_HERO_THUNDER_GIANT_CID', 'eval_equip_slot_score_cid_thunder_giant'),
    # card_info.inc: BLAST_MAGICIAN_CID = 0x0000186a
    (0x080503cc, 0x0000186a, 'BLAST_MAGICIAN_CID', 'eval_equip_slot_score_cid_blast_magician'),
    # card_info.inc: GREAT_SPIRIT_CID = 0x000019f1
    (0x080503f8, 0x000019f1, 'GREAT_SPIRIT_CID', 'eval_equip_slot_score_cid_great_spirit'),
    # card_info.inc: SHIELD_AND_SWORD_CID = 0x000012cb
    (0x08050cc8, 0x000012cb, 'SHIELD_AND_SWORD_CID', 'check_equip_slot_eligible_with_bst_filter_cid_shield_sword'),

    # --- Group D: New CID equates (22 slots, all card_info.inc) ---
    # BST in eval_equip_slot_score_by_card_state (0x080502b0):
    # card_info.inc NEW: INFERNALQUEEN_ARCHFIEND_CID = 0x00001690
    (0x0805035c, 0x00001690, 'INFERNALQUEEN_ARCHFIEND_CID', 'eval_equip_slot_score_cid_infernalqueen'),
    # card_info.inc NEW: THROWSTONE_UNIT_CID = 0x000014c5
    (0x08050360, 0x000014c5, 'THROWSTONE_UNIT_CID', 'eval_equip_slot_score_cid_throwstone'),
    # card_info.inc NEW: DRAGON_SEEKER_CID = 0x0000119a
    (0x08050364, 0x0000119a, 'DRAGON_SEEKER_CID', 'eval_equip_slot_score_cid_dragon_seeker'),
    # card_info.inc NEW: WINGED_MINION_CID = 0x000014b9
    (0x08050368, 0x000014b9, 'WINGED_MINION_CID', 'eval_equip_slot_score_cid_winged_minion'),
    # card_info.inc NEW: COMBINATION_ATTACK_CID = 0x000015e4
    (0x08050390, 0x000015e4, 'COMBINATION_ATTACK_CID', 'eval_equip_slot_score_cid_combination_attack'),
    # card_info.inc NEW: WILD_NATURES_RELEASE_CID = 0x000016ce
    (0x080503bc, 0x000016ce, 'WILD_NATURES_RELEASE_CID', 'eval_equip_slot_score_cid_wild_natures_release'),
    # card_info.inc NEW: CYBER_LASER_DRAGON_CID = 0x000019a9
    (0x080503e8, 0x000019a9, 'CYBER_LASER_DRAGON_CID', 'eval_equip_slot_score_cid_cyber_laser_dragon'),

    # BST in check_equip_slot_eligible_by_card_id_bst (0x08050a54):
    # card_info.inc NEW: cid_1304 = 0x00001304 (unallocated)
    (0x08050ae8, 0x00001304, 'cid_1304', 'check_equip_slot_eligible_by_card_id_bst_cid_1304'),
    # card_info.inc NEW: cid_123d = 0x0000123d (unallocated)
    (0x08050b00, 0x0000123d, 'cid_123d', 'check_equip_slot_eligible_by_card_id_bst_cid_123d'),
    # card_info.inc NEW: cid_123e = 0x0000123e (unallocated)
    (0x08050b0c, 0x0000123e, 'cid_123e', 'check_equip_slot_eligible_by_card_id_bst_cid_123e'),
    # card_info.inc NEW: TRIBE_INFECTING_VIRUS_CID = 0x0000161c
    (0x08050b2c, 0x0000161c, 'TRIBE_INFECTING_VIRUS_CID', 'check_equip_slot_eligible_by_card_id_bst_cid_tribe'),
    # card_info.inc NEW: BURST_BREATH_CID = 0x000014e4
    (0x08050b30, 0x000014e4, 'BURST_BREATH_CID', 'check_equip_slot_eligible_by_card_id_bst_cid_burst_breath'),
    # card_info.inc NEW: cid_1305 = 0x00001305 (unallocated)
    (0x08050b34, 0x00001305, 'cid_1305', 'check_equip_slot_eligible_by_card_id_bst_cid_1305'),
    # card_info.inc NEW: NEEDLE_CEILING_CID = 0x00001542
    (0x08050b40, 0x00001542, 'NEEDLE_CEILING_CID', 'check_equip_slot_eligible_by_card_id_bst_cid_needle_ceiling'),
    # card_info.inc NEW: OJAMUSCLE_CID = 0x00001945
    (0x08050b58, 0x00001945, 'OJAMUSCLE_CID', 'check_equip_slot_eligible_by_card_id_bst_cid_ojamuscle'),
    # card_info.inc NEW: REALLY_ETERNAL_REST_CID = 0x0000166d
    (0x08050b5c, 0x0000166d, 'REALLY_ETERNAL_REST_CID', 'check_equip_slot_eligible_by_card_id_bst_cid_really_eternal'),
    # card_info.inc NEW: WEED_OUT_CID = 0x00001977
    (0x08050b68, 0x00001977, 'WEED_OUT_CID', 'check_equip_slot_eligible_by_card_id_bst_cid_weed_out'),

    # BST in check_equip_slot_eligible_with_bst_filter (0x08050c58):
    # card_info.inc NEW: CURSE_OF_ANUBIS_CID = 0x000017b3
    (0x08050cc0, 0x000017b3, 'CURSE_OF_ANUBIS_CID', 'check_equip_slot_eligible_with_bst_filter_cid_anubis'),
    # card_info.inc NEW: ROULETTE_BARREL_CID = 0x000015df
    (0x08050cc4, 0x000015df, 'ROULETTE_BARREL_CID', 'check_equip_slot_eligible_with_bst_filter_cid_roulette'),
    # card_info.inc NEW: ZERO_GRAVITY_CID = 0x000016e1
    (0x08050cd4, 0x000016e1, 'ZERO_GRAVITY_CID', 'check_equip_slot_eligible_with_bst_filter_cid_zero_gravity'),
    # card_info.inc NEW: BURST_RETURN_CID = 0x00001988
    (0x08050cf4, 0x00001988, 'BURST_RETURN_CID', 'check_equip_slot_eligible_with_bst_filter_cid_burst_return'),
    # card_info.inc NEW: EHERO_BURSTINATRIX_CID = 0x000018a7
    (0x08050d68, 0x000018a7, 'EHERO_BURSTINATRIX_CID', 'check_equip_slot_eligible_with_bst_filter_cid_burstinatrix'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # 0x1281 clashes with RELINQUISHED_CID in card_info.inc; different domain (state_code)
    (0x0805009c, 'check_equip_chain_type_d_node_exists_state_a',
     'equip chain type D active state; value 0x1281 also = RELINQUISHED_CID in card_info.inc (different domain)'),
    # 0x1cb8 as gDuelFieldSlots offset -> gEquipZoneCountTable; DUEL_ACTIVE_PLAYER_OFF=0x1cb8 uses different base
    (0x08050d20, 'check_equip_slot_eligible_with_bst_filter_gdfs_off',
     'gDuelFieldSlots offset to gEquipZoneCountTable (gDuelFieldSlots+0x1cb8=0x0201e1c8); differs from DUEL_ACTIVE_PLAYER_OFF which is gP1LifePoints relative'),
    # 0x7f280000: low-conf sentinel in TRIANGLE_ECSTASY_SPARK branch; exact semantics not decoded
    (0x08050d40, 'check_equip_slot_eligible_with_bst_filter_type_sentinel',
     'low-conf sentinel used in TRIANGLE_ECSTASY_SPARK (0x1840) branch; slot[0]<<19 exact semantics not decoded'),
]

# ---------------------------------------------------------------------------
# C. PLATE_SUBS: (func_addr, old_substring, new_substring)
# ---------------------------------------------------------------------------
# check_equip_slot_eligible_by_card_id_and_prereqs (0x0805000c):
#   FUN_080538e8 -> check_equip_slot_eligible_by_type_and_chain
#   FUN_080af120 -> find_best_equip_target_slot_scored
# eval_equip_slot_score_by_card_state (0x080502b0):
#   FUN_0809078c -> count_zone_pair_hits_with_fn_ptr
#   "known state_code values" -> "known equip card id (card_ptr[+0]) values"
PLATE_SUBS = [
    (0x0805000c, 'FUN_080538e8', 'check_equip_slot_eligible_by_type_and_chain'),
    (0x0805000c, 'FUN_080af120', 'find_best_equip_target_slot_scored'),
    (0x080502b0, 'FUN_0809078c', 'count_zone_pair_hits_with_fn_ptr'),
    (0x080502b0, 'known state_code values', 'known equip card id (card_ptr[+0]) values'),
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
eq_ok = eq_fail = 0
ren_ok = ren_fail = 0
plate_ok = plate_fail = 0

print("=== RefineF05Seg7Slots.py  DRY=%s ===" % DRY)

print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
for (sa, val, cn, sl) in EQ_SLOTS:
    if apply_eq_slot(sa, val, cn, sl):
        eq_ok += 1
    else:
        eq_fail += 1

print("--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
for (sa, sl, eol) in RENAME_SLOTS:
    if apply_rename_slot(sa, sl, eol):
        ren_ok += 1
    else:
        ren_fail += 1

print("--- C. PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
for (fa, old_s, new_s) in PLATE_SUBS:
    if apply_plate_sub(fa, old_s, new_s):
        plate_ok += 1
    else:
        plate_fail += 1

print("")
print("=== SUMMARY ===")
print("EQ:    ok=%d fail=%d" % (eq_ok, eq_fail))
print("REN:   ok=%d fail=%d" % (ren_ok, ren_fail))
print("PLATE: ok=%d fail=%d" % (plate_ok, plate_fail))
total_fail = eq_fail + ren_fail + plate_fail
print("TOTAL FAIL: %d" % total_fail)
if total_fail == 0:
    print("ALL OK -- ready for real run" if DRY else "ALL OK")
else:
    print("FAILURES detected -- fix addresses before real run")
