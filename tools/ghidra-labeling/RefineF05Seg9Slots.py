# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg9Slots.py -- file-05 Seg-9 (0x08051cc4..0x08052df8)
#   Combined Seg-9a (0x08051cc4..0x080525d0) + Seg-9b (0x080525d0..0x08052df8)
#   24 functions: check_equip_slot_eligible_by_*
#
# Sections:
#   A. EQ_SLOTS:
#      Group 1: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc) -- 30 slots
#      Group 2: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)     -- 30 slots
#      Group 3: gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc) --  2 slots
#      Group 4: gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)     --  1 slot
#      Group 5: LP_BAR_ANIM_STATE_OFF = 0x000004cc (reuse ewram.inc) -- 1 slot
#      Group 6: SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4 (reuse ewram.inc) -- 1 slot
#      Group 7: CHAIN_NODE_CARD_ARR_OFF = 0x000004f4 (reuse ewram.inc) -- 1 slot
#      Group 8: CID reuse (19 slots, 18 unique values)
#      Group 9: CID new (27 slots, 27 new constants)
#      Total EQ: 66+19+27 = 112 slots
#   B. RENAME_SLOTS:
#      4 packed zone masks + 1 unallocated CID = 5 slots
#   C. PLATE_SUBS:
#      2 stale FUN_ replacements
#
# carve=0, disasm=0, section5_1=0
# All EOL/plate text is pure ASCII. No CJK.
#
# Boundary: only slots with addr < 0x08052df8 (Seg-9).
# Seg-10 slots (0x08052e4c/e50/e54/ebc/ec0/f04/f44/f48) are NOT processed here.

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

    # --- Group 1: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc) --- 30 slots
    # Seg-9a (18 slots)
    (0x08051d20, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_stride'),
    (0x08051d74, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_stride_b'),
    (0x08051d9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_and_slot_vacant_stride'),
    (0x08051dc8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field8_and_chain_stride_a'),
    (0x08051e14, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field8_and_chain_stride_b'),
    (0x08051e84, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_mismatch_and_prereqs_stride'),
    (0x08051ef4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_side_and_type_query_stride'),
    (0x08051f50, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_query_prereqs_and_eligible_stride'),
    (0x08051fc0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_slot8_flag_stride'),
    (0x08052010, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_chain_node_and_activation_stride'),
    (0x08052070, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_whitelist_type_and_state_stride'),
    (0x080520e8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_slot_chain_node_stride'),
    (0x08052190, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_global_and_chain_stride'),
    (0x08052214, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_stride'),
    (0x080522b4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_stride_b'),
    (0x08052420, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_stride_c'),
    (0x08052634, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_alt_stride'),
    # Seg-9b (12 slots)
    (0x08052724, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_card_id_pair_stride'),
    (0x08052780, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_duel_ctx_stride'),
    (0x080527e8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_setcode_not_field6_17_stride'),
    (0x08052818, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_prereqs_and_spell_type_stride'),
    (0x08052874, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_revival_jam_and_duel_ctx_stride'),
    (0x080528d8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_owner_bit_and_chain_field_stride'),
    (0x08052998, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_chain_list_entry_stride'),
    (0x08052a0c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_field6_present_no_field8_stride'),
    (0x08052a68, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_type_and_chain_score4_stride'),
    (0x08052a9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_paired_card_zone_match_stride'),
    (0x08052b38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_b_stride'),
    (0x08052d18, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_b_stride_b'),
    (0x08052d64, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_by_card_id_dispatch_b_stride_c'),

    # --- Group 2: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc) --- 30 slots
    # Seg-9a (18 slots)
    (0x08051d24, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_dfs'),
    (0x08051d78, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_dfs_b'),
    (0x08051da0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_and_slot_vacant_dfs'),
    (0x08051dcc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field8_and_chain_dfs_a'),
    (0x08051e18, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field8_and_chain_dfs_b'),
    (0x08051e88, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_mismatch_and_prereqs_dfs'),
    (0x08051ef8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_side_and_type_query_dfs'),
    (0x08051f54, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_query_prereqs_and_eligible_dfs'),
    (0x08051fc4, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_slot8_flag_dfs'),
    (0x08052014, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_chain_node_and_activation_dfs'),
    (0x08052074, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_whitelist_type_and_state_dfs'),
    (0x080520ec, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_slot_chain_node_dfs'),
    (0x08052194, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_global_and_chain_dfs'),
    (0x08052218, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_dfs'),
    (0x080522b8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_dfs_b'),
    (0x08052424, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_dfs_c'),
    (0x08052638, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_alt_dfs'),
    # Seg-9b (13 slots -- note: offset 0x08052728 is the 18th Seg-9a pair +1 for 9b start)
    (0x08052728, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_card_id_pair_dfs'),
    (0x08052784, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_duel_ctx_dfs'),
    (0x080527ec, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_setcode_not_field6_17_dfs'),
    (0x0805281c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_prereqs_and_spell_type_dfs'),
    (0x08052878, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_revival_jam_and_duel_ctx_dfs'),
    (0x080528dc, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_owner_bit_and_chain_field_dfs'),
    (0x0805299c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_chain_list_entry_dfs'),
    (0x08052a10, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_field6_present_no_field8_dfs'),
    (0x08052a6c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_type_and_chain_score4_dfs'),
    (0x08052aa0, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_paired_card_zone_match_dfs'),
    (0x08052b3c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_b_dfs'),
    (0x08052d1c, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_b_dfs_b'),
    (0x08052d68, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_by_card_id_dispatch_b_dfs_c'),

    # --- Group 3: gEquipChainSlotRefs = 0x0201bb90 (reuse ewram.inc) --- 2 slots (Seg-9b only)
    (0x080526b0, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_prereqs_and_duel_ctx_ecsr'),
    (0x080527f4, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_by_revival_jam_and_duel_ctx_ecsr'),

    # --- Group 4: gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc) --- 1 slot (Seg-9b)
    (0x08052944, 0x0201b290, 'gDuelPhaseFlags', 'check_equip_slot_eligible_by_chain_list_entry_dpf'),

    # --- Group 5: LP_BAR_ANIM_STATE_OFF = 0x000004cc (reuse ewram.inc) --- 1 slot (Seg-9b)
    (0x08052948, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'check_equip_slot_eligible_by_chain_list_entry_chain_cnt_off'),

    # --- Group 6: SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4 (reuse ewram.inc) --- 1 slot (Seg-9b)
    (0x0805294c, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'check_equip_slot_eligible_by_chain_list_entry_chain_arr_off'),

    # --- Group 7: CHAIN_NODE_CARD_ARR_OFF = 0x000004f4 (reuse ewram.inc) --- 1 slot (Seg-9b)
    (0x08052950, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'check_equip_slot_eligible_by_chain_list_entry_card_arr_off'),

    # --- Group 8: CID reuse (19 slots, 18 unique values from card_info.inc) ---
    # DARK_MAGICIAN_CID_0FC9 = 0x0fc9 (x2 slots)
    (0x08051da4, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_dm_cid'),
    (0x08052344, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9', 'check_equip_slot_eligible_by_card_id_dispatch_alt_dm_cid'),
    # NINJITSU_ART_OF_TRANSFORMATION_CID = 0x1768
    (0x08051d4c, 0x00001768, 'NINJITSU_ART_OF_TRANSFORMATION_CID', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_nat_cid'),
    # DEDICATION_THROUGH_LIGHT_DARK_CID = 0x1713
    (0x080522d8, 0x00001713, 'DEDICATION_THROUGH_LIGHT_DARK_CID', 'check_equip_slot_eligible_by_card_id_dispatch_dedtld_cid'),
    # GEARFRIED_IRON_KNIGHT_CID = 0x13c3
    (0x0805236c, 0x000013c3, 'GEARFRIED_IRON_KNIGHT_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_gik_cid'),
    # CYBER_DRAGON_CID = 0x18f6
    (0x08052388, 0x000018f6, 'CYBER_DRAGON_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_cd_cid'),
    # DARK_SCORPION_COMBO_CID = 0x16a3
    (0x08052428, 0x000016a3, 'DARK_SCORPION_COMBO_CID', 'check_equip_slot_eligible_by_card_id_dispatch_dsc_cid'),
    # DARK_SCORPION_CHICK_CID = 0x1656
    (0x080524ec, 0x00001656, 'DARK_SCORPION_CHICK_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_dschick_cid'),
    # DON_ZALOOG_CID = 0x1532
    (0x080524f0, 0x00001532, 'DON_ZALOOG_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_dz_cid'),
    # DARK_SCORPION_MEANAE_CID = 0x1686
    (0x080524f8, 0x00001686, 'DARK_SCORPION_MEANAE_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_dsmeanae_cid'),
    # CHU_SKE_MOUSE_FIGHTER_CID = 0x185a
    (0x08052598, 0x0000185a, 'CHU_SKE_MOUSE_FIGHTER_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_chuske_cid'),
    # NINJITSU_ART_OF_DECOY_CID = 0x17ff
    (0x08052b40, 0x000017ff, 'NINJITSU_ART_OF_DECOY_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_nad_cid'),
    # CHECKMATE_CID = 0x169b
    (0x08052b44, 0x0000169b, 'CHECKMATE_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_cm_cid'),
    # GRADIUS_OPTION_CID = 0x14fc
    (0x08052b48, 0x000014fc, 'GRADIUS_OPTION_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_go_cid'),
    # UNION_ATTACK_CID = 0x1890
    (0x08052bd0, 0x00001890, 'UNION_ATTACK_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_ua_cid'),
    # FEATHER_SHOT_CID = 0x195b
    (0x08052bec, 0x0000195b, 'FEATHER_SHOT_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_fs_cid'),
    # GRADIUS_CID = 0x1414
    (0x08052c34, 0x00001414, 'GRADIUS_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_gradius_cid'),
    # OJAMA_KING_CARD_ID = 0x17ee
    (0x08052dbc, 0x000017ee, 'OJAMA_KING_CARD_ID', 'check_equip_slot_eligible_by_card_id_dispatch_b_ok_cid'),
    # EHERO_AVIAN_CID = 0x18a6
    (0x08052dcc, 0x000018a6, 'EHERO_AVIAN_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_ea_cid'),

    # --- Group 9: CID new (27 slots, all new constants added to card_info.inc) ---
    # KNIGHTS_TITLE_CID = 0x167d
    (0x08051d3c, 0x0000167d, 'KNIGHTS_TITLE_CID', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_kt_cid'),
    # MULTIPLY_CID = 0x12c5
    (0x08051d40, 0x000012c5, 'MULTIPLY_CID', 'check_equip_slot_eligible_by_card_id_bst_and_pairs_mul_cid'),
    # SHADOW_TAMER_CID = 0x14cd
    (0x08052110, 0x000014cd, 'SHADOW_TAMER_CID', 'check_equip_slot_eligible_by_slot_chain_node_st_cid'),
    # DRAGON_MANIPULATOR_CID = 0x14ce
    (0x08052120, 0x000014ce, 'DRAGON_MANIPULATOR_CID', 'check_equip_slot_eligible_by_slot_chain_node_dm_cid'),
    # ULTRA_EVOLUTION_PILL_CID = 0x1715
    (0x080522bc, 0x00001715, 'ULTRA_EVOLUTION_PILL_CID', 'check_equip_slot_eligible_by_card_id_dispatch_uep_cid'),
    # INSECT_IMITATION_CID = 0x140b
    (0x080522c0, 0x0000140b, 'INSECT_IMITATION_CID', 'check_equip_slot_eligible_by_card_id_dispatch_ii_cid'),
    # METAMORPHOSIS_CID = 0x15a3
    (0x080522d4, 0x000015a3, 'METAMORPHOSIS_CID', 'check_equip_slot_eligible_by_card_id_dispatch_meta_cid'),
    # SPIRITUAL_EARTH_ART_CID = 0x1927
    (0x080522f0, 0x00001927, 'SPIRITUAL_EARTH_ART_CID', 'check_equip_slot_eligible_by_card_id_dispatch_sea_cid'),
    # PHOTON_GENERATOR_UNIT_CID = 0x19b1
    (0x08052304, 0x000019b1, 'PHOTON_GENERATOR_UNIT_CID', 'check_equip_slot_eligible_by_card_id_dispatch_pgu_cid'),
    # WINGBEAT_GIANT_DRAGON_CID = 0x14df
    (0x0805242c, 0x000014df, 'WINGBEAT_GIANT_DRAGON_CID', 'check_equip_slot_eligible_by_card_id_dispatch_wgd_cid'),
    # GRACEFUL_DICE_CID = 0x12cf
    (0x08052430, 0x000012cf, 'GRACEFUL_DICE_CID', 'check_equip_slot_eligible_by_card_id_dispatch_gd_cid'),
    # LIMITER_REMOVAL_CID = 0x1409
    (0x08052434, 0x00001409, 'LIMITER_REMOVAL_CID', 'check_equip_slot_eligible_by_card_id_dispatch_lr_cid'),
    # PYRAMID_ENERGY_CID = 0x153d
    (0x0805244c, 0x0000153d, 'PYRAMID_ENERGY_CID', 'check_equip_slot_eligible_by_card_id_dispatch_pe_cid'),
    # BIG_WAVE_SMALL_WAVE_CID = 0x17f9
    (0x0805246c, 0x000017f9, 'BIG_WAVE_SMALL_WAVE_CID', 'check_equip_slot_eligible_by_card_id_dispatch_bwsw_cid'),
    # KAMINOTE_BLOW_CID = 0x18cd
    (0x08052484, 0x000018cd, 'KAMINOTE_BLOW_CID', 'check_equip_slot_eligible_by_card_id_dispatch_kb_cid'),
    # MINEFIELD_ERUPTION_CID = 0x18d6
    (0x08052494, 0x000018d6, 'MINEFIELD_ERUPTION_CID', 'check_equip_slot_eligible_by_card_id_dispatch_me_cid'),
    # ELEMENTAL_HERO_TEMPEST_CID = 0x1957
    (0x0805263c, 0x00001957, 'ELEMENTAL_HERO_TEMPEST_CID', 'check_equip_slot_eligible_by_card_id_dispatch_alt_eht_cid'),
    # CATHEDRAL_OF_NOBLES_CID = 0x146f
    (0x08052a44, 0x0000146f, 'CATHEDRAL_OF_NOBLES_CID', 'check_equip_slot_eligible_by_type_and_chain_score4_con_cid'),
    # TRANSCENDENT_WINGS_CID = 0x1907
    (0x08052a48, 0x00001907, 'TRANSCENDENT_WINGS_CID', 'check_equip_slot_eligible_by_type_and_chain_score4_tw_cid'),
    # FORMATION_UNION_CID = 0x15f7
    (0x08052b5c, 0x000015f7, 'FORMATION_UNION_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_fu_cid'),
    # ORDER_TO_CHARGE_CID = 0x179f
    (0x08052b78, 0x0000179f, 'ORDER_TO_CHARGE_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_otc_cid'),
    # ORDER_TO_SMASH_CID = 0x17b8
    (0x08052b90, 0x000017b8, 'ORDER_TO_SMASH_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_ots_cid'),
    # DOUBLE_ATTACK_CID = 0x18cb
    (0x08052bb8, 0x000018cb, 'DOUBLE_ATTACK_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_da_cid'),
    # HERO_HEART_CID = 0x19ab
    (0x08052c04, 0x000019ab, 'HERO_HEART_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_hh_cid'),
    # SUMMONED_SKULL_CID = 0x0fbc
    (0x08052c24, 0x00000fbc, 'SUMMONED_SKULL_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_ss_cid'),
    # TERRORKING_ARCHFIEND_CID = 0x1691
    (0x08052c7c, 0x00001691, 'TERRORKING_ARCHFIEND_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_ta_cid'),
    # RED_EYES_B_DRAGON_CID = 0x0ff8
    (0x08052cdc, 0x00000ff8, 'RED_EYES_B_DRAGON_CID', 'check_equip_slot_eligible_by_card_id_dispatch_b_rebd_cid'),

]  # end EQ_SLOTS (total: 66 structural + 19 CID-reuse + 27 CID-new = 112)

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, label, eol_comment)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # 4 packed zone masks (post-shift CID << 19 comparison values)
    (0x080527f0, 'revival_jam_zone_mask',           'Revival Jam (0x13c7) << 19'),
    (0x08052a70, 'cathedral_of_nobles_zone_mask',    'Mystical Beast Serket (0x147a) << 19; Cathedral of Nobles path'),
    (0x08052aa4, 'transcendent_wings_zone_mask',     'Winged Kuriboh (0x18aa) << 19; Transcendent Wings path'),
    (0x080525bc, 'mine_golem_zone_mask',             'Mine Golem (0x18b7) << 19; dispatch_alt Chu-Ske range end'),
    # 1 unallocated CID
    (0x08052114, 'cid_13b0',                         'unallocated slot_id; not found in card-stats.s'),
]

# ---------------------------------------------------------------------------
# C. PLATE_SUBS: (func_addr, old_substring, new_substring)
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # Plate 1: check_equip_slot_eligible_by_side_mismatch_and_prereqs (0x08051e94)
    (0x08051e94, 'FUN_0809077c', 'invoke_count_zone_pair_hits_full_range'),
    # Plate 2: check_equip_slot_eligible_by_type_and_card_id_pair (0x080525d0)
    (0x080525d0, 'FUN_080556f0', 'check_equip_slot_eligible_by_setcode_activation_and_zone_pair'),
]

# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
def main():
    eq_ok = 0; eq_fail = 0
    ren_ok = 0; ren_fail = 0
    plate_ok = 0; plate_fail = 0

    print("=== RefineF05Seg9Slots %s ===" % ("DRY RUN" if DRY else "LIVE"))

    print("--- EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for (sa, val, cname, slabel) in EQ_SLOTS:
        # Boundary guard: must be within Seg-9 range [0x08051cc4, 0x08052df8)
        if sa >= 0x08052df8:
            print("FAIL BOUNDARY 0x%08x >= 0x08052df8 (Seg-10 territory)" % sa)
            eq_fail += 1
            continue
        if apply_eq_slot(sa, val, cname, slabel):
            eq_ok += 1
        else:
            eq_fail += 1

    print("--- RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for (sa, label, eol) in RENAME_SLOTS:
        if sa >= 0x08052df8:
            print("FAIL BOUNDARY 0x%08x >= 0x08052df8 (Seg-10 territory)" % sa)
            ren_fail += 1
            continue
        if apply_rename_slot(sa, label, eol):
            ren_ok += 1
        else:
            ren_fail += 1

    print("--- PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
    for (fa, old_s, new_s) in PLATE_SUBS:
        if apply_plate_sub(fa, old_s, new_s):
            plate_ok += 1
        else:
            plate_fail += 1

    print("=== SUMMARY: EQ %d/%d  REN %d/%d  PLATE %d/%d  FAIL=%d ===" % (
        eq_ok, len(EQ_SLOTS),
        ren_ok, len(RENAME_SLOTS),
        plate_ok, len(PLATE_SUBS),
        eq_fail + ren_fail + plate_fail))
    if eq_fail + ren_fail + plate_fail > 0:
        print("RESULT: FAIL -- %d error(s)" % (eq_fail + ren_fail + plate_fail))
    else:
        print("RESULT: OK")

main()
