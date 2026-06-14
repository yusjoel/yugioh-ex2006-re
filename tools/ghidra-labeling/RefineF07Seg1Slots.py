# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg1Slots.py -- F07 Seg-1 (0x0805c2f0..0x0805cfec)
#   Symbolizes 66 auto-name slots: EQ=54, REF=3, RENAME=9
#   Proposal: doc/dev/refine/F07-Seg-1.proposal.md (iter-2 PASS)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (54 slots)
#   B. REF_SLOTS -- USER label on target + DATA ref from slot + slot rename (3 slots)
#   C. RENAME_SLOTS -- plain rename, no EOL needed (9 PTR_ slots)
#
# Note: PLATE=0 (no stale FUN_ in Seg-1 plates; C8 verified by reviewer)
#       FUNC_RENAME=0 (no function name conflicts)

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
#    All values verified against ROM via proposal iter-2 review.
#    const_name is a pre-existing .equ in constants/*.inc (no new equates here --
#    new CIDs are added to card_info.inc manually before this script runs).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ----- PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc) x15 -----
    (0x0805c3e0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c3e0'),
    (0x0805c51c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c51c'),
    (0x0805c5fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c5fc'),
    (0x0805c714, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c714'),
    (0x0805c80c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c80c'),
    (0x0805c924, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c924'),
    (0x0805c988, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c988'),
    (0x0805c9f0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805c9f0'),
    (0x0805ca34, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805ca34'),
    (0x0805cae4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805cae4'),
    (0x0805cbb8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805cbb8'),
    (0x0805cbfc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805cbfc'),
    (0x0805ce24, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805ce24'),
    (0x0805cebc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805cebc'),
    (0x0805cfe8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805cfe8'),

    # ----- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (ewram.inc) x2 -----
    (0x0805c384, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805c384'),
    (0x0805c5f4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805c5f4'),

    # ----- FIELD_STATE_OFF = 0x1cf4 (duel_field.inc) x4 -----
    (0x0805c388, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805c388'),
    (0x0805c5f8, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805c5f8'),
    (0x0805c6ac, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805c6ac'),
    (0x0805cb38, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805cb38'),

    # ----- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc) x4 -----
    (0x0805c58c, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805c58c'),
    (0x0805c710, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805c710'),
    (0x0805cd60, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805cd60'),
    (0x0805cf10, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805cf10'),

    # ----- gDuelFieldSlots = 0x0201c510 (ewram.inc) x6 -----
    (0x0805c718, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805c718'),
    (0x0805c928, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805c928'),
    (0x0805c98c, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805c98c'),
    (0x0805c9f4, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805c9f4'),
    (0x0805ca38, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805ca38'),
    (0x0805cbbc, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805cbbc'),

    # ----- gDuelPhaseFlags = 0x0201b290 (ewram.inc) x1 -----
    (0x0805cd04, 0x0201b290, 'gDuelPhaseFlags', 'duel_phase_flags_0805cd04'),

    # ----- LP_BAR_ANIM_STATE_OFF = 0x4cc (ewram.inc) x1 -----
    # EOL note: same value as NODE_COUNT_OFF in this consumer; C5 strict scalar dedup
    (0x0805cd08, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_state_off_0805cd08'),

    # ----- SPRITE_ROW_ENTRY_DATA_OFF = 0x4d4 (ewram.inc) x1 -----
    (0x0805cd0c, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'sprite_row_entry_data_off_0805cd0c'),

    # ----- CHAIN_NODE_CARD_ARR_OFF = 0x4f4 (ewram.inc) x1 -----
    (0x0805cd10, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'chain_node_card_arr_off_0805cd10'),

    # ----- SWORDS_OF_REVEALING_LIGHT_CID = 0x1102 (card_info.inc reuse) x1 -----
    (0x0805c67c, 0x00001102, 'SWORDS_OF_REVEALING_LIGHT_CID', 'swords_of_light_cid_0805c67c'),

    # ----- STRAY_LAMBS_CID = 0x1710 (card_info.inc reuse) x1 -----
    (0x0805c7c0, 0x00001710, 'STRAY_LAMBS_CID', 'stray_lambs_cid_0805c7c0'),

    # ----- SANGA_OF_THUNDER_CID = 0x1119 (card_info.inc new) x1 -----
    (0x0805c588, 0x00001119, 'SANGA_OF_THUNDER_CID', 'sanga_of_thunder_cid_0805c588'),

    # ----- WALL_SHADOW_CID = 0x1117 (card_info.inc reuse) x1 -----
    (0x0805c798, 0x00001117, 'WALL_SHADOW_CID', 'wall_shadow_cid_0805c798'),

    # ----- SCAPEGOAT_CID = 0x12d2 (card_info.inc new) x1 -----
    (0x0805c7bc, 0x000012d2, 'SCAPEGOAT_CID', 'scapegoat_cid_0805c7bc'),

    # ----- LORD_OF_D_CID = 0x128b (card_info.inc reuse) x1 -----
    (0x0805cdcc, 0x0000128b, 'LORD_OF_D_CID', 'lord_of_d_cid_0805cdcc'),

    # ----- GRACEFUL_CHARITY_CID = 0x12cc (card_info.inc new) x1 -----
    (0x0805cfb0, 0x000012cc, 'GRACEFUL_CHARITY_CID', 'graceful_charity_cid_0805cfb0'),

    # ----- GREENKAPPA_CID = 0x11f0 (card_info.inc new) x1 -----
    (0x0805c870, 0x000011f0, 'GREENKAPPA_CID', 'greenkappa_cid_0805c870'),

    # ----- REAPER_OF_CARDS_CID = 0x0ffa (card_info.inc new) x1 -----
    (0x0805c874, 0x00000ffa, 'REAPER_OF_CARDS_CID', 'reaper_of_cards_cid_0805c874'),

    # ----- HARPIES_FEATHER_DUSTER_CID = 0x1246 (card_info.inc new) x1 -----
    (0x0805c884, 0x00001246, 'HARPIES_FEATHER_DUSTER_CID', 'harpies_feather_duster_cid_0805c884'),

    # ----- DRIVING_SNOW_CID = 0x134d (card_info.inc new) x1 -----
    (0x0805c8a0, 0x0000134d, 'DRIVING_SNOW_CID', 'driving_snow_cid_0805c8a0'),

    # ----- NOBLEMAN_EXTERMINATION_CID = 0x1364 (card_info.inc new) x1 -----
    (0x0805c8bc, 0x00001364, 'NOBLEMAN_EXTERMINATION_CID', 'nobleman_extermination_cid_0805c8bc'),

    # ----- BAIT_DOLL_CID = 0x149b (card_info.inc new) x1 -----
    (0x0805c8b8, 0x0000149b, 'BAIT_DOLL_CID', 'bait_doll_cid_0805c8b8'),

    # ----- CRIMSON_NINJA_CID = 0x16b8 (card_info.inc reuse) x1 -----
    (0x0805c920, 0x000016b8, 'CRIMSON_NINJA_CID', 'crimson_ninja_cid_0805c920'),

    # ----- cid_131c = 0x131c (card_info.inc new, low conf) x1 -----
    (0x0805c86c, 0x0000131c, 'cid_131c', 'cid_131c_0805c86c'),

    # ----- cid_12fb = 0x12fb (card_info.inc new, low conf) x1 -----
    (0x0805cf8c, 0x000012fb, 'cid_12fb', 'cid_12fb_0805cf8c'),

    # ----- HARPIE_LADY_CID = 0x0fe4 (card_info.inc reuse) x1 -----
    # All count_paired_slots_both_sides callers pass CID args; 0xfe4=Harpie Lady confirmed
    (0x0805c514, 0x00000fe4, 'HARPIE_LADY_CID', 'harpie_lady_cid_0805c514'),

    # ----- SLOT_CARD_EMPTY = 0xffff (card_info.inc reuse) x1 -----
    # EOL: SLOT_CARD_EMPTY reuse: 0xffff = no pair found (same sentinel as card slot empty check)
    (0x0805c794, 0x0000ffff, 'SLOT_CARD_EMPTY', 'slot_card_empty_0805c794'),

    # ----- EQUIP_CHAIN_SENTINEL = 0xffff0000 (duel_field.inc reuse) x1 -----
    # EOL: EQUIP_CHAIN_SENTINEL reuse: post-lsls#16 sentinel check for no-node-found (low-16 of return = 0xffff)
    (0x0805ca88, 0xffff0000, 'EQUIP_CHAIN_SENTINEL', 'equip_chain_sentinel_0805ca88'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
#    Target: gP1LifePoints = 0x0201c4e0 (ewram.inc)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0805c380, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0805c380'),
    (0x0805ce20, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0805ce20'),
    (0x0805ceb8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0805ceb8'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    PTR_gP1LifePoints_* auto-names already reference gP1LifePoints.
#    Just give them shorter non-auto names; .word value stays unchanged.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0805c3dc, 'gp1lp_ptr_0805c3dc', None),
    (0x0805c518, 'gp1lp_ptr_0805c518', None),
    (0x0805c5f0, 'gp1lp_ptr_0805c5f0', None),
    (0x0805c6a8, 'gp1lp_ptr_0805c6a8', None),
    (0x0805c808, 'gp1lp_ptr_0805c808', None),
    (0x0805cae0, 'gp1lp_ptr_0805cae0', None),
    (0x0805cb34, 'gp1lp_ptr_0805cb34', None),
    (0x0805cbf8, 'gp1lp_ptr_0805cbf8', None),
    (0x0805cfe4, 'gp1lp_ptr_0805cfe4', None),
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
    print("=== RefineF07Seg1Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = 0
    made = set()

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B. REF_SLOTS ---
    print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- C. RENAME_SLOTS ---
    print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))
    print("EQ=%d REF=%d RENAME=%d total=%d (expected 54+3+9=66)" % (nA, nB, nC, nA+nB+nC))


main()
