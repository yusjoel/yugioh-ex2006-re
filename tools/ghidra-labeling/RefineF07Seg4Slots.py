# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg4Slots.py -- F07 Seg-4 (0x0805f1cc..0x0805fc94)
#   Symbolizes 47 auto-name slots: EQ=44, RENAME=1, REF=2
#   Proposal: doc/dev/refine/F07-Seg-4.proposal.md (iter-2 PASS)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (44 slots: 35 DWORD + 9 DAT)
#   B. RENAME_SLOTS -- DWORD_0805f28c (fn-ptr) -> check_card_is_amazoness_type_ptr (1 slot)
#   C. REF_SLOTS -- USER label on target + DATA ref from slot (2 PTR slots)
#   D. PLATE_SUBS -- stale FUN_ substring replacement in 3 plates
#
# Prerequisites:
#   - constants/ewram.inc +1:
#       gDuelEquipCtx = 0x0201bbbc
#   - constants/card_info.inc +4:
#       FUSHI_NO_TORI_CID = 0x00001506
#       TSUKUYOMI_CID = 0x00001694
#       SWARM_OF_SCARABS_CID = 0x0000152a
#       LIFE_ABSORBING_MACHINE_CID = 0x000014c0  (documentation only, no literal pool slot)
#   (added to .inc files before script run)
#
# FUNC_RENAME=0 (all 34 existing functions have correct names)
# carve=0 (all 5 ROM_INCBIN blocks are R4 disasm targets, no carve needed)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-141354-pre-f07seg4

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
#    44 slots total: 35 DWORD + 9 DAT.
#    slot_label != const_name (per convention).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== DWORD slots (35 entries) =====

    # ----- gP1LifePoints = 0x0201c4e0 (ewram.inc reuse) -----
    (0x0805f228, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805f228'),
    (0x0805f4fc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805f4fc'),
    (0x0805f540, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805f540'),
    (0x0805f920, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805f920'),
    (0x0805fb1c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805fb1c'),
    (0x0805fbb0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805fbb0'),

    # ----- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (ewram.inc reuse) -----
    (0x0805f22c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'field_state_off_0805f22c'),
    (0x0805f500, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'curr_turn_off_0805f500'),
    (0x0805fb20, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'curr_turn_off_0805fb20'),

    # ----- gDuelEquipCtx = 0x0201bbbc (ewram.inc NEW) -----
    (0x0805f230, 0x0201bbbc, 'gDuelEquipCtx', 'gdueleqctx_ptr_0805f230'),

    # ----- BANISHER_OF_THE_LIGHT_CID = 0x1332 (card_info.inc reuse) -----
    (0x0805f260, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_0805f260'),

    # ----- PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc reuse) -----
    (0x0805f328, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805f328'),
    (0x0805f41c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805f41c'),
    (0x0805f5c8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805f5c8'),
    (0x0805f770, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805f770'),
    (0x0805f924, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805f924'),
    (0x0805f9d8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805f9d8'),
    (0x0805fb24, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805fb24'),
    (0x0805fbb4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805fbb4'),
    (0x0805fc84, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805fc84'),

    # ----- gDuelFieldSlots = 0x0201c510 (ewram.inc reuse) -----
    (0x0805f32c, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_0805f32c'),
    (0x0805f420, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_0805f420'),
    (0x0805f5cc, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_0805f5cc'),
    (0x0805f774, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_0805f774'),
    (0x0805f9dc, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_0805f9dc'),
    (0x0805fc88, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_0805fc88'),

    # ----- SLOT_CARD_EMPTY = 0xffff (card_info.inc reuse) -----
    (0x0805f330, 0x0000ffff, 'SLOT_CARD_EMPTY', 'slot_empty_0805f330'),

    # ----- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc reuse) -----
    (0x0805f398, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805f398'),
    (0x0805f440, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805f440'),
    (0x0805f504, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805f504'),
    (0x0805f76c, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805f76c'),
    (0x0805f9d4, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805f9d4'),
    (0x0805fc80, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805fc80'),

    # ----- FIELD_STATE_OFF = 0x1cf4 (duel_field.inc reuse) -----
    (0x0805f544, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805f544'),

    # ----- FIELD5_SCORE_THRESHOLD_1999 = 0x7cf (card_info.inc reuse) -----
    (0x0805f8a8, 0x000007cf, 'FIELD5_SCORE_THRESHOLD_1999', 'atk_thresh_0805f8a8'),

    # ===== DAT_ slots (9 entries) =====

    # DAT_0805f68c = 0x868 (PLAYER_BLOCK_STRIDE reuse)
    (0x0805f68c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_dat_0805f68c'),

    # DAT_0805f7b0 = 0x1506 (FUSHI_NO_TORI_CID NEW)
    (0x0805f7b0, 0x00001506, 'FUSHI_NO_TORI_CID', 'fushi_no_tori_cid_0805f7b0'),

    # DAT_0805f7b4 = 0x1694 (TSUKUYOMI_CID NEW)
    (0x0805f7b4, 0x00001694, 'TSUKUYOMI_CID', 'tsukuyomi_cid_0805f7b4'),

    # DAT_0805f83c = 0x868 (PLAYER_BLOCK_STRIDE reuse)
    (0x0805f83c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_dat_0805f83c'),

    # DAT_0805fa14 = 0x868 (PLAYER_BLOCK_STRIDE reuse)
    (0x0805fa14, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_dat_0805fa14'),

    # DAT_0805fa18 = 0x0201c510 (gDuelFieldSlots reuse)
    (0x0805fa18, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_dat_0805fa18'),

    # DAT_0805fa4c = 0x135d (LIGHT_OF_INTERVENTION_CID reuse)
    (0x0805fa4c, 0x0000135d, 'LIGHT_OF_INTERVENTION_CID', 'loi_cid_0805fa4c'),

    # DAT_0805fa50 = 0x152a (SWARM_OF_SCARABS_CID NEW)
    (0x0805fa50, 0x0000152a, 'SWARM_OF_SCARABS_CID', 'swarm_cid_0805fa50'),

    # DAT_0805fae0 = 0x135d (LIGHT_OF_INTERVENTION_CID reuse)
    (0x0805fae0, 0x0000135d, 'LIGHT_OF_INTERVENTION_CID', 'loi_cid_0805fae0'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, value, old_label, new_label, eol_ascii)
#    DWORD_0805f28c = 0x0804b049 = check_card_is_amazoness_type(0x0804b048)+1 (THUMB fn-ptr)
#    No equate (fn-ptr, not a data constant); rename only + EOL comment.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0805f28c, 0x0804b049, 'DWORD_0805f28c', 'check_card_is_amazoness_type_ptr',
     'check_card_is_amazoness_type THUMB fn-ptr (+1); used by count_monster_slots_by_fnptr; conf: high'),
]

# ---------------------------------------------------------------------------
# C. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
#    2 PTR slots (PTR_gP1LifePoints_0805f688, PTR_gP1LifePoints_0805f838).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0805f688, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805f688'),
    (0x0805f838, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805f838'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (fn_entry_addr, old_substr, new_substr)
#    Fix stale FUN_ references in plate comments.
#    3 fixes in Seg-4 range (asm/07 L8320, L8647, L9101).
#    Text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # check_player_has_active_monster plate: FUN_0805f614 -> check_player_has_active_monster_return2
    # fn at 0x0805f628; plate L8286; EOL line L8320
    (0x0805f628, 'FUN_0805f614', 'check_player_has_active_monster_return2'),

    # check_slot_zone_type_facedown_flip plate: FUN_0805f784 -> dispatch_slot_placement_check_by_card_id
    # fn at 0x0805f7d0; plate L8632; EOL line L8647
    (0x0805f7d0, 'FUN_0805f784', 'dispatch_slot_placement_check_by_card_id'),

    # check_light_of_intervention_absent plate: FUN_0805f784 -> dispatch_slot_placement_check_by_card_id
    # fn at 0x0805fad0; plate L9091; EOL line L9101
    (0x0805fad0, 'FUN_0805f784', 'dispatch_slot_placement_check_by_card_id'),
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
    print("=== RefineF07Seg4Slots (DRY=%s) ===" % DRY)
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

    # --- B. RENAME_SLOTS ---
    print("--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_int, value, old_label, new_label, eol_text in RENAME_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[B FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[B dry] 0x%08x %s -> %s [EOL=%d chars]" % (slot_int, old_label, new_label, len(eol_text)))
            nB += 1; continue
        createLabel(_addr(slot_int), new_label, True, SourceType.USER_DEFINED)
        cu = listing.getCodeUnitAt(_addr(slot_int))
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol_text)
            if bad:
                print("[B FAIL] non-ASCII in EOL @ 0x%08x" % slot_int)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[B ok] 0x%08x -> %s" % (slot_int, new_label)); nB += 1

    # --- C. REF_SLOTS ---
    print("--- C. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nC += 1; continue
        tgt_a = _addr(tgt_int)
        if gas_label not in made:
            try:
                createLabel(tgt_a, gas_label, True, SourceType.USER_DEFINED)
            except Exception as e:
                print("[C warn] createLabel at 0x%08x: %s" % (tgt_int, e))
            made.add(gas_label)
        ref = rm.addMemoryReference(_addr(slot_int), tgt_a, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[C ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nC += 1

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
        bad = any(ord(ch) > 127 for ch in new_plate)
        if bad:
            print("[D FAIL] non-ASCII in plate after sub @ 0x%08x" % fn_int)
            continue
        if DRY:
            print("[D dry] 0x%08x: '%s' -> '%s'" % (fn_int, old_sub, new_sub))
            nD += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub: '%s' -> '%s'" % (fn_int, old_sub, new_sub)); nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))
    print("EQ=%d RENAME=%d REF=%d PLATE_SUB=%d total_slots=%d (expected 44+1+2=47)" % (
        nA, nB, nC, nD, nA + nB + nC))


main()
