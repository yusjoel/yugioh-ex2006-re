# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg8Slots.py -- file-05 Seg-8 (0x08050e40..0x08051cc4)
#   check_equip_slot_eligible_with_whitelist_prereqs_2 + by_card_id_tree +
#   by_empty_equip_with_field6 + by_field5_score_no_prereqs + by_prereqs_only +
#   by_lp_zone_and_type + by_equip_type + by_not_field8_9_and_type +
#   by_card_id_pair + by_opposite_side_with_guard + by_opposite_and_slot_guard +
#   by_field5_score + by_opposite_side_and_prereqs + build_equip_chain_for_monster_zone +
#   by_opposite_type_and_prereqs + by_card_id_score + by_field6_type_and_prereqs +
#   by_type_and_unequipped + by_setcode_whitelist + build_equip_chain_for_special_zone +
#   by_side_and_setcode + by_setcode_and_prereqs + by_setcode_only + by_setcode_and_slot8
#
# Sections:
#   A. EQ_SLOTS  -- 25 PLAYER_BLOCK_STRIDE + 24 gDuelFieldSlots +
#                   2 gEquipChainSlotRefs + 4 gDuelPhaseFlags group +
#                   1 P1LP_BLOCK2_OFF_1CE8 + 5 reuse-CID + 1 SLOT_CARD_EMPTY +
#                   1 FIELD5_SCORE_THRESHOLD_1999 + 1 CARD_STAT_LP_THRESHOLD_999 (reuse) +
#                   9 new-CID + 3 SLOT_CARD_TYPE_* +
#                   6 fn-ptr (EQ-style, will need +1 fix post export)
#                   = 82 total EQ slots
#   B. REF_SLOTS -- 1 (gP1LifePoints)
#   C. RENAME_SLOTS -- 1 (0x08051848, value=0x1250 conflict, neutral RENAME + EOL)
#   D. PLATE_SUBS -- 4 subs across 2 functions (2 stale FUN_ + 2 gDuelTurnStruct prose fixes)
#
# carve=0, disasm=0, §5.1=1 (0x08051bfc/0x40)
#
# All EOL/plate text is pure ASCII. No CJK.
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
    """Verify ROM word at addr matches expected value; WARN = FAIL (not skipped)."""
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

def apply_ref_slot(slot_addr, target_addr, gas_label, slot_label):
    """Create USER label at target + DATA ref from slot, label slot."""
    if DRY:
        print("DRY REF 0x%08x -> 0x%08x (%s / %s)" % (slot_addr, target_addr, gas_label, slot_label))
        return True
    try:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(_addr(target_addr), gas_label, SourceType.USER_DEFINED)
        rf = currentProgram.getReferenceManager()
        ref = rf.addMemoryReference(_addr(slot_addr), _addr(target_addr), RefType.DATA, SourceType.USER_DEFINED, 0)
        try:
            ref.setPrimary(True)
        except Exception:
            pass
        sm.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("OK  REF 0x%08x -> 0x%08x (%s)" % (slot_addr, target_addr, slot_label))
        return True
    except Exception as e:
        print("ERR REF 0x%08x: %s" % (slot_addr, str(e)))
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

def apply_fnptr_slot(slot_addr, odd_val, even_target, gas_label, slot_label):
    """For THUMB fn-ptr: check slot contains odd addr, create DATA ref slot->even_target, label slot."""
    if not _check(slot_addr, odd_val, slot_label):
        return False
    if DRY:
        print("DRY FNPTR 0x%08x -> 0x%08x (%s / %s)" % (slot_addr, even_target, gas_label, slot_label))
        return True
    try:
        sm = currentProgram.getSymbolTable()
        # Ensure target fn has the label (it should already be named; createLabel is idempotent)
        sm.createLabel(_addr(even_target), gas_label, SourceType.USER_DEFINED)
        rf = currentProgram.getReferenceManager()
        ref = rf.addMemoryReference(_addr(slot_addr), _addr(even_target), RefType.DATA, SourceType.USER_DEFINED, 0)
        try:
            ref.setPrimary(True)
        except Exception:
            pass
        sm.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("OK  FNPTR 0x%08x -> 0x%08x (%s)" % (slot_addr, even_target, slot_label))
        return True
    except Exception as e:
        print("ERR FNPTR 0x%08x: %s" % (slot_addr, str(e)))
        return False

def apply_plate_sub(func_addr, old_sub, new_sub):
    """Replace old_sub with new_sub in existing plate comment (ASCII only). WARN = FAIL."""
    if DRY:
        print("DRY PLATE_SUB 0x%08x  '%s' -> '%s'" % (func_addr, old_sub, new_sub))
        return True
    try:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(_addr(func_addr))
        if cu is None:
            print("FAIL PLATE_SUB 0x%08x: no code unit" % func_addr)
            return False
        old_text = cu.getComment(CodeUnit.PLATE_COMMENT)
        if old_text is None:
            print("FAIL PLATE_SUB 0x%08x: no plate comment" % func_addr)
            return False
        if old_sub not in old_text:
            print("FAIL PLATE_SUB 0x%08x: substring not found: '%s'" % (func_addr, old_sub))
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

    # --- Group 1: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc) --- 25 slots
    (0x08050e9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_whitelist_prereqs_2_stride'),
    (0x08050f24, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_tree_stride_a'),
    (0x08051108, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_tree_stride_b'),
    (0x080511f0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_empty_equip_with_field6_stride'),
    (0x08051244, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field5_score_no_prereqs_stride'),
    (0x080512b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_only_stride'),
    (0x0805130c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_lp_zone_and_type_stride'),
    (0x08051354, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_equip_type_stride'),
    (0x080513c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_not_field8_9_and_type_stride'),
    (0x0805141c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_pair_stride'),
    (0x08051528, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_with_guard_stride'),
    (0x08051594, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_and_slot_guard_stride'),
    (0x080515e4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field5_score_stride'),
    (0x08051660, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_side_and_prereqs_stride'),
    (0x08051714, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'build_equip_chain_for_monster_zone_stride'),
    (0x080517a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_opposite_type_and_prereqs_stride'),
    (0x08051840, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_score_stride'),
    (0x08051914, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_type_and_prereqs_stride'),
    (0x0805197c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_unequipped_stride'),
    (0x080519f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_whitelist_stride'),
    (0x08051a4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'build_equip_chain_for_special_zone_stride'),
    (0x08051b10, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_and_setcode_stride'),
    (0x08051b8c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_and_prereqs_stride'),
    (0x08051bec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_only_stride'),
    (0x08051ca8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_and_slot8_stride'),

    # --- Group 2: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc) --- 24 slots
    (0x08050ea0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_whitelist_prereqs_2_gdfs'),
    (0x08050f28, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_tree_gdfs_a'),
    (0x0805110c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_tree_gdfs_b'),
    (0x080511f4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_empty_equip_with_field6_gdfs'),
    (0x08051248, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field5_score_no_prereqs_gdfs'),
    (0x080512b4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_only_gdfs'),
    (0x08051358, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_equip_type_gdfs'),
    (0x080513c4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_not_field8_9_and_type_gdfs'),
    (0x08051420, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_pair_gdfs'),
    (0x0805152c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_with_guard_gdfs'),
    (0x08051598, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_and_slot_guard_gdfs'),
    (0x080515e8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field5_score_gdfs'),
    (0x08051664, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_side_and_prereqs_gdfs'),
    (0x08051718, 0x0201c510, 'gDuelFieldSlots', 'build_equip_chain_for_monster_zone_gdfs'),
    (0x080517a8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_opposite_type_and_prereqs_gdfs'),
    (0x08051844, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_score_gdfs'),
    (0x08051918, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_type_and_prereqs_gdfs'),
    (0x08051980, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_unequipped_gdfs'),
    (0x080519fc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_whitelist_gdfs'),
    (0x08051a50, 0x0201c510, 'gDuelFieldSlots', 'build_equip_chain_for_special_zone_gdfs'),
    (0x08051b14, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_and_setcode_gdfs'),
    (0x08051b90, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_and_prereqs_gdfs'),
    (0x08051bf0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_only_gdfs'),
    (0x08051cac, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_and_slot8_gdfs'),

    # --- Group 3: gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc) --- 2 slots
    (0x08051530, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_opposite_side_with_guard_dts'),
    (0x0805159c, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_opposite_and_slot_guard_dts'),

    # --- Group 4: gDuelPhaseFlags group (reuse ewram.inc) --- 4 slots
    (0x08051478, 0x0201b290, 'gDuelPhaseFlags', 'check_equip_slot_eligible_by_card_id_pair_dpf'),
    (0x0805147c, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'check_equip_slot_eligible_by_card_id_pair_count_off'),
    (0x08051480, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'check_equip_slot_eligible_by_card_id_pair_carr_off'),
    (0x08051484, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'check_equip_slot_eligible_by_card_id_pair_earr_off'),

    # --- Group 5: P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 (reuse ewram.inc) --- 1 slot
    (0x08051308, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'check_equip_slot_eligible_by_lp_zone_and_type_lp_off'),

    # --- Group 6: Reuse CIDs from card_info.inc --- 5 slots
    (0x08050f34, 0x0000123b, 'CRUSH_CARD_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_123b'),
    (0x08050f40, 0x000014e4, 'BURST_BREATH_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_14e4'),
    (0x08051428, 0x0000184b, 'RARE_METALMORPH_CID', 'check_equip_slot_eligible_by_card_id_pair_cid_184b'),
    (0x08050f2c, 0x00001835, 'GAIA_SOUL_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1835'),
    (0x080510a0, 0x00001709, 'CANNONBALL_SPEAR_SHELLFISH_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1709'),

    # --- Group 7: SLOT_CARD_EMPTY = 0x0000ffff (reuse card_info.inc) --- 1 slot
    (0x08051ab8, 0x0000ffff, 'SLOT_CARD_EMPTY', 'build_equip_chain_for_special_zone_pair_not_found'),

    # --- Group 8: FIELD5_SCORE_THRESHOLD_1999 = 0x000007cf (new, card_info.inc) --- 1 slot
    (0x08051134, 0x000007cf, 'FIELD5_SCORE_THRESHOLD_1999', 'check_equip_slot_eligible_by_card_id_tree_score_max'),

    # --- Group 9: CARD_STAT_LP_THRESHOLD_999 = 0x000003e7 (reuse card_info.inc C5) --- 1 slot
    (0x08051868, 0x000003e7, 'CARD_STAT_LP_THRESHOLD_999', 'check_equip_slot_eligible_by_card_id_score_trap_threshold'),

    # --- Group 10: New CIDs (card_info.inc) --- 9 slots
    # Note: 0x08051424 CHAIN_DESTRUCTION_CID and 0x08051080 TORPEDO_FISH_CID appear in both
    #   reuse-CID table and new-CID table in proposal; treat as NEW here (not yet in card_info.inc)
    (0x08051080, 0x00001706, 'TORPEDO_FISH_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1706'),
    (0x08050f30, 0x000014ee, 'DE_SPELL_GERM_WEAPON_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_14ee'),
    (0x08050f58, 0x00001708, 'ORCA_MEGA_FORTRESS_OF_DARKNESS_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1708'),
    (0x08050f68, 0x00001753, 'ARCANE_ARCHER_OF_THE_FOREST_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1753'),
    (0x08050f90, 0x00001928, 'SPIRITUAL_WATER_ART_AOI_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1928'),
    (0x08050fa0, 0x0000188d, 'ELEMENTAL_BURST_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_188d'),
    (0x08050fbc, 0x0000192a, 'SPIRITUAL_WIND_ART_MIYABI_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_192a'),
    (0x08051190, 0x0000194f, 'HYDROGEDDON_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_194f'),
    (0x080511a0, 0x00001950, 'OXYGEDDON_CID', 'check_equip_slot_eligible_by_card_id_tree_cid_1950'),
    (0x08051424, 0x000012cd, 'CHAIN_DESTRUCTION_CID', 'check_equip_slot_eligible_by_card_id_pair_cid_12cd'),
    (0x08051864, 0x000012e4, 'TRAP_HOLE_CID', 'check_equip_slot_eligible_by_card_id_score_cid_12e4'),

    # --- Group 11: SLOT_CARD_TYPE_MASK / ELIGIBLE_A / ELIGIBLE_B (new, duel_field.inc) --- 3 slots
    # NOTE: These are inline-computed constants (movs+lsls), NOT literal pool .word slots.
    # They appear as Ghidra inline operand equates only (no .word address).
    # These 3 are handled as equate-only (no slot label needed; inline scalar operand in code).
    # We skip them in the per-slot EQ table since they have no literal pool address.
    # (The Ghidra equate table will have them registered by value from the inline instruction stream.)

]

# ---------------------------------------------------------------------------
# fn-ptr REF slots (DATA ref to even target; GAS exporter -> .word <fn>+1)
# Format: (slot_addr, odd_thumb_val, even_target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
FNPTR_SLOTS = [
    # 6 fn-ptr slots; targets are named THUMB functions; all odd (THUMB) values verified
    (0x08050ff4, 0x080502b1, 0x080502b0, 'eval_equip_slot_score_by_card_state', 'check_equip_slot_eligible_by_card_id_tree_fn_ptr_a'),
    (0x08051020, 0x08050a55, 0x08050a54, 'check_equip_slot_eligible_by_card_id_bst', 'check_equip_slot_eligible_by_card_id_tree_fn_ptr_b'),
    (0x08051058, 0x08052aa9, 0x08052aa8, 'check_equip_slot_eligible_by_card_id_dispatch_b', 'check_equip_slot_eligible_by_card_id_tree_fn_ptr_c'),
    (0x08051084, 0x08050995, 0x08050994, 'check_equip_slot_eligible_by_type_then_prereqs', 'check_equip_slot_eligible_by_card_id_tree_fn_ptr_d'),
    (0x080510a4, 0x08051b21, 0x08051b20, 'check_equip_slot_eligible_by_setcode_and_prereqs', 'check_equip_slot_eligible_by_card_id_tree_fn_ptr_e'),
    (0x080510cc, 0x08051b21, 0x08051b20, 'check_equip_slot_eligible_by_setcode_and_prereqs', 'check_equip_slot_eligible_by_card_id_tree_fn_ptr_f'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gP1LifePoints = 0x0201c4e0 (already named in ewram.inc)
    (0x08051304, 0x0201c4e0, 'gP1LifePoints', 'check_equip_slot_eligible_by_lp_zone_and_type_lp_base'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # 0x1250: value collision with GSETTINGS_TEXT_FIELD_A_OFF (different semantic domain); RENAME only
    (0x08051848, 'check_equip_slot_eligible_by_card_id_score_cid_1250',
     'card_id=0x1250 (not in card-stats.s; equip BST leaf; distinct from GSETTINGS_TEXT_FIELD_A_OFF=0x1250)'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_addr, old_substring, new_substring)
# ---------------------------------------------------------------------------
# check_equip_slot_eligible_by_setcode_and_prereqs (0x08051b20):
#   stale FUN_ replacements
# check_equip_slot_eligible_by_opposite_side_with_guard (0x080514b4):
#   gDuelTurnStruct -> gEquipChainSlotRefs prose fix
# check_equip_slot_eligible_by_opposite_and_slot_guard (0x0805153c):
#   gDuelTurnStruct -> gEquipChainSlotRefs prose fix
PLATE_SUBS = [
    (0x08051b20, 'FUN_08053704', 'dispatch_equip_slot_eligible_by_card_id_tier'),
    (0x08051b20, 'FUN_08054118', 'dispatch_equip_slot_eligible_by_type_prereqs_or_setcode'),
    (0x080514b4, 'gDuelTurnStruct', 'gEquipChainSlotRefs'),
    (0x0805153c, 'gDuelTurnStruct', 'gEquipChainSlotRefs'),
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
eq_ok = eq_fail = 0
ref_ok = ref_fail = 0
fnptr_ok = fnptr_fail = 0
ren_ok = ren_fail = 0
plate_ok = plate_fail = 0

print("=== RefineF05Seg8Slots.py  DRY=%s ===" % DRY)

print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
for (sa, val, cn, sl) in EQ_SLOTS:
    if apply_eq_slot(sa, val, cn, sl):
        eq_ok += 1
    else:
        eq_fail += 1

print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
for (sa, ta, gl, sl) in REF_SLOTS:
    if apply_ref_slot(sa, ta, gl, sl):
        ref_ok += 1
    else:
        ref_fail += 1

print("--- B2. FNPTR_SLOTS (%d) ---" % len(FNPTR_SLOTS))
for (sa, ov, et, gl, sl) in FNPTR_SLOTS:
    if apply_fnptr_slot(sa, ov, et, gl, sl):
        fnptr_ok += 1
    else:
        fnptr_fail += 1

print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
for (sa, sl, eol) in RENAME_SLOTS:
    if apply_rename_slot(sa, sl, eol):
        ren_ok += 1
    else:
        ren_fail += 1

print("--- D. PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
for (fa, old_s, new_s) in PLATE_SUBS:
    if apply_plate_sub(fa, old_s, new_s):
        plate_ok += 1
    else:
        plate_fail += 1

print("=== DONE DRY=%s ===" % DRY)
print("EQ:     ok=%d fail=%d" % (eq_ok, eq_fail))
print("REF:    ok=%d fail=%d" % (ref_ok, ref_fail))
print("FNPTR:  ok=%d fail=%d" % (fnptr_ok, fnptr_fail))
print("REN:    ok=%d fail=%d" % (ren_ok, ren_fail))
print("PLATE:  ok=%d fail=%d" % (plate_ok, plate_fail))
total_fail = eq_fail + ref_fail + fnptr_fail + ren_fail + plate_fail
print("TOTAL_FAIL=%d" % total_fail)
if total_fail > 0:
    print("RESULT: FAIL -- review FAIL/WARN lines above before real run")
else:
    print("RESULT: OK -- all checks passed")
