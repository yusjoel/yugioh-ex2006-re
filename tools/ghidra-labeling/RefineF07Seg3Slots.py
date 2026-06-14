# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg3Slots.py -- F07 Seg-3 (0x0805e358..0x0805f1cc)
#   Symbolizes 45 auto-name slots: EQ=24, REF=16, RENAME=5
#   Proposal: doc/dev/refine/F07-Seg-3.proposal.md (iter-2 PASS)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (24 slots)
#   B. REF_SLOTS -- USER label on target + DATA ref from slot + slot rename (16 slots)
#   C. RENAME_SLOTS -- PTR_gP1LifePoints_* -> gp1lp_ptr_* (5 slots)
#   D. PLATE_COMMENTS -- stale FUN_ substring replacement (2 plates)
#
# Prerequisites:
#   - constants/card_info.inc +2 new CIDs:
#       REVIVAL_JAM_CID = 0x13c7
#       RED_MOON_BABY_CID = 0x1415
#     (added manually before script run)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-130344-pre-f07seg3

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
#    24 slots total. Note: slot_label != const_name (per proposal convention).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ----- PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc reuse) x10 -----
    (0x0805e398, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_monster_slot_field5_score_in_range_stride'),
    (0x0805e510, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_type580_stride'),
    (0x0805e640, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_zone_stride'),
    (0x0805e678, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_type_range18_stride'),
    (0x0805e6e4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_type_range18_stride_b'),
    (0x0805e808, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_revival_jam_equip_paired_field5_stride'),
    (0x0805e854, 0x00001cf4, 'FIELD_STATE_OFF',     'check_field_state2_bit19_equip_eligible_fstate'),
    (0x0805e858, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_field_state2_bit19_equip_eligible_stride'),
    (0x0805e9b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_facedown_slot_zone_equip_byte_set_stride'),
    (0x0805ea2c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_with_type_e_stride'),
    (0x0805ebbc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_eligible_max1_stride'),
    (0x0805ee54, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_opponent_has_monsters_stride'),
    (0x0805f0b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'eval_spell_zone_equip_eligibility_stride'),
    (0x0805f190, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_player_has_field5_hand_card_stride'),

    # ----- FIELD_STATE_OFF = 0x1cf4 (duel_field.inc reuse) x1 (already counted above) -----
    # check_field_state2_bit19_equip_eligible_fstate already listed above at 0x0805e854

    # ----- FIELD_STATE_OFF x1 more -----
    (0x0805e570, 0x00001cf4, 'FIELD_STATE_OFF',     'check_equip_slot_eligible_type580_fstate_off'),

    # ----- CID equates -----
    # BANISHER_OF_THE_LIGHT_CID = 0x1332 (card_info.inc reuse)
    (0x0805e724, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'check_equip_slot_eligible_without_banisher_cid'),

    # UMI_CARD_ID = 0x10f4 (card_info.inc reuse)
    (0x0805e740, 0x000010f4, 'UMI_CARD_ID',         'check_umi_matches_active_effect_slot_cid'),

    # REVIVAL_JAM_CID = 0x13c7 (card_info.inc NEW)
    (0x0805e810, 0x000013c7, 'REVIVAL_JAM_CID',     'check_revival_jam_equip_paired_field5_cid'),

    # EQUIP_LOCKDOWN_CID = 0x13f2 (card_info.inc reuse)
    (0x0805e94c, 0x000013f2, 'EQUIP_LOCKDOWN_CID',  'check_mask_restrict_absent_daedalus_lockdown_cid'),

    # RED_MOON_BABY_CID = 0x1415 (card_info.inc NEW)
    (0x0805ead8, 0x00001415, 'RED_MOON_BABY_CID',   'check_equip_or_facedown_dispatch_red_moon_cid'),

    # DARK_MAGICIAN_CID_0FC9 = 0x0fc9 (card_info.inc reuse)
    (0x0805ec30, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9', 'check_dark_magician_effect_zone_cid_0fc9'),

    # DARK_MAGICIAN_CID_142D = 0x142d (card_info.inc reuse)
    (0x0805ec34, 0x0000142d, 'DARK_MAGICIAN_CID_142D', 'check_dark_magician_effect_zone_cid_142d'),

    # P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (ewram.inc reuse)
    (0x0805ed1c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'check_equip_count_exceeds_one_off_1ce8'),

    # EFFECT_ZONE_BITMASK_OFF = 0x10d0 (duel_field.inc reuse)
    (0x0805ed20, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF', 'check_equip_count_exceeds_one_bitmask_off'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
#    16 slots total (all reuse existing ewram.inc globals).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # ----- gDuelFieldSlots = 0x0201c510 (ewram.inc) x5 -----
    (0x0805e39c, 0x0201c510, 'gDuelFieldSlots', 'check_monster_slot_field5_score_in_range_slots'),
    (0x0805e514, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_type580_slots'),
    (0x0805e6e8, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_type_range18_slots'),
    (0x0805e80c, 0x0201c510, 'gDuelFieldSlots', 'check_revival_jam_equip_paired_field5_slots'),
    (0x0805ea30, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_eligible_with_type_e_slots'),
    (0x0805f0bc, 0x0201c510, 'gDuelFieldSlots', 'eval_spell_zone_equip_eligibility_slots'),
    (0x0805f194, 0x0201c510, 'gDuelFieldSlots', 'check_player_has_field5_hand_card_slots'),

    # ----- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc) x4 -----
    (0x0805e444, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_type340_ctx'),
    (0x0805e474, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_type340_ctx_b'),
    (0x0805e6e0, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_slot_eligible_type_range18_ctx'),
    (0x0805e804, 0x0201bb90, 'gEquipChainSlotRefs', 'check_revival_jam_equip_paired_field5_ctx'),
    (0x0805e91c, 0x0201bb90, 'gEquipChainSlotRefs', 'check_equip_zone_slot_activation_eligible_ctx'),

    # ----- gP1ZoneHandCount = 0x0201c4ec (ewram.inc) x2 -----
    (0x0805e67c, 0x0201c4ec, 'gP1ZoneHandCount', 'check_equip_slot_eligible_type_range18_zone_cnt'),
    (0x0805ebc0, 0x0201c4ec, 'gP1ZoneHandCount', 'check_equip_slot_eligible_max1_zone_cnt'),

    # ----- gP1LifePoints = 0x0201c4e0 (ewram.inc) x2 -----
    (0x0805ed18, 0x0201c4e0, 'gP1LifePoints', 'check_equip_count_exceeds_one_lp_base'),
    (0x0805ee50, 0x0201c4e0, 'gP1LifePoints', 'check_opponent_has_monsters_lp_base'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, value, old_prefix, new_label)
#    PTR_gP1LifePoints_* -> gp1lp_ptr_* (per Seg-1 precedent)
#    5 slots total. All hold 0x0201c4e0 = gP1LifePoints.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0805e56c, 0x0201c4e0, 'PTR_gP1LifePoints_0805e56c', 'gp1lp_ptr_5e56c'),
    (0x0805e63c, 0x0201c4e0, 'PTR_gP1LifePoints_0805e63c', 'gp1lp_ptr_5e63c'),
    (0x0805e850, 0x0201c4e0, 'PTR_gP1LifePoints_0805e850', 'gp1lp_ptr_5e850'),
    (0x0805e9ac, 0x0201c4e0, 'PTR_gP1LifePoints_0805e9ac', 'gp1lp_ptr_5e9ac'),
    (0x0805ebb8, 0x0201c4e0, 'PTR_gP1LifePoints_0805ebb8', 'gp1lp_ptr_5ebb8'),
]

# ---------------------------------------------------------------------------
# D. PLATE_COMMENTS: (fn_entry_addr, plate_text_ascii)
#    Stale FUN_ substring replacement in existing plate comments.
#    Text must be pure ASCII.
#
#    check_equip_slot_eligible_max1_or_byte3_flag @ L6454 (fn at 0x0805ebc4):
#      FUN_080839b4 -> tick_equip_placement_bitmap_display_4state
#    eval_spell_zone_equip_eligibility @ L7081 (fn at 0x0805f0d8):
#      FUN_08057874 -> tick_equip_slot_score_fill_display_seq
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # (fn_entry_addr, old_substr, new_substr)
    # FUN_080839b4 appears in plate of check_effect_activations_both_sides @ 0x0805ec40
    # (proposal listed L6543 -> @ Caller: line is Ghidra plate at ec40, not at ebc4)
    (0x0805ec40, 'FUN_080839b4', 'tick_equip_placement_bitmap_display_4state'),
    (0x0805f0d8, 'FUN_08057874', 'tick_equip_slot_score_fill_display_seq'),
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
    print("=== RefineF07Seg3Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
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
        tgt_a = _addr(tgt_int)
        if gas_label not in made:
            try:
                createLabel(tgt_a, gas_label, True, SourceType.USER_DEFINED)
            except Exception as e:
                print("[B warn] createLabel at 0x%08x: %s" % (tgt_int, e))
            made.add(gas_label)
        ref = rm.addMemoryReference(_addr(slot_int), tgt_a, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- C. RENAME_SLOTS ---
    print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_int, value, old_label, new_label in RENAME_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[C FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[C dry] 0x%08x %s -> %s" % (slot_int, old_label, new_label))
            nC += 1; continue
        createLabel(_addr(slot_int), new_label, True, SourceType.USER_DEFINED)
        print("[C ok] 0x%08x -> %s" % (slot_int, new_label)); nC += 1

    # --- D. PLATE_SUBS ---
    print("--- D. PLATE_SUBS (%d) ---" % len(PLATE_SUBS))
    for fn_int, old_sub, new_sub in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(fn_int))
        if cu is None:
            print("[D FAIL] no CodeUnit at 0x%08x" % fn_int); continue
        existing = cu.getComment(CodeUnit.PLATE_COMMENT)
        if existing is None:
            existing = ''
        if old_sub not in existing:
            print("[D WARN] 0x%08x: '%s' not found in plate (plate len=%d)" % (fn_int, old_sub, len(existing)))
            continue
        new_plate = existing.replace(old_sub, new_sub)
        # ASCII check
        bad = False
        for ch in new_plate:
            if ord(ch) > 127:
                print("[D FAIL] non-ASCII char U+%04x in plate @ 0x%08x" % (ord(ch), fn_int))
                bad = True; break
        if bad:
            continue
        if DRY:
            print("[D dry] 0x%08x: '%s' -> '%s'" % (fn_int, old_sub, new_sub))
            nD += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub: '%s' -> '%s'" % (fn_int, old_sub, new_sub)); nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))
    print("EQ=%d REF=%d RENAME=%d PLATE_SUB=%d total_slots=%d (expected 24+16+5=45)" % (
        nA, nB, nC, nD, nA + nB + nC))


main()
