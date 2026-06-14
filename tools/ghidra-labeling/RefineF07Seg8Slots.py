# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg8Slots.py -- F07 Seg-8 (0x08061eb4..0x08062d28)
#   Symbolizes 55 original auto-name slots: EQ=50 + REF=3 + RENAME=2
#   (14 additional disasm literal-pool slots handled in DisassembleF07Seg8Blocks.py)
#   Total coverage: 69 slots (EQ=64 + REF=3 + RENAME=2)
#   Proposal: doc/dev/refine/F07-Seg-8.proposal.md (PASS iter-2)
#
# Sections:
#   A. EQ_SLOTS  -- 50 slots (49 reuse + 1 new ATK_THRESHOLD_2999)
#   B. REF_SLOTS -- 3 PTR_gP1LifePoints slots (DATA ref -> gP1LifePoints)
#   C. RENAME_SLOTS -- 2 fn-ptr slots (rename + EOL)
#   E. PLATE_REWRITES -- 3 plates (2 FUN_ stale name fix + 1 CJK full rewrite)
#
# Prerequisites added to constants/ before running this script:
#   duel_field.inc +1 NEW: ATK_THRESHOLD_2999=0xbb7
#   card_info.inc +4 NEW: MIND_WIPE_CID=0x17f3, HEAVY_SLUMP_CID=0x1801,
#                         MIND_HAXORZ_CID=0x184d, COVERING_FIRE_CID=0x1853
#   (CID equates are for disasm blocks; not referenced by EQ_SLOTS here but
#    needed by DisassembleF07Seg8Blocks.py)
#
# FUNC_RENAME=0 (no misnames detected in Seg-8)
# carve=0, disasm=5 blocks (6 new fn) -- handled by DisassembleF07Seg8Blocks.py
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_183408-pre-F07Seg8

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
#    50 slots from proposal EQ汇总表.
#    (Note: PTR_gP1LifePoints_08062968 and PTR_gP1LifePoints_080629c0 are
#     EQ not REF because their Ghidra names do not end in a unique "PTR_" pattern
#     that signals a pointer reference; they appear in the EQ list in proposal.)
#    All values C4-verified by reviewer.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== gP1LifePoints = 0x0201c4e0 (ewram.inc REUSE) =====
    # 10 DWORD_ slots + 2 DAT_ + 2 PTR_ (not the 3 REF PTR_s)
    (0x08061f00, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_08061f00'),
    (0x08061fe8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_08061fe8'),
    (0x0806203c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0806203c'),
    (0x08062160, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_08062160'),
    (0x080623e4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_080623e4'),
    (0x080625fc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_080625fc'),
    (0x0806275c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0806275c'),
    (0x0806278c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0806278c'),
    (0x0806284c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_0806284c'),
    (0x08062968, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_08062968'),
    (0x080629c0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_080629c0'),
    (0x08062bd0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ref_08062bd0'),

    # ===== PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc REUSE; 16 slots) =====
    (0x08061f04, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061f04'),
    (0x08061fec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061fec'),
    (0x08062164, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062164'),
    (0x08062208, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062208'),
    (0x080622d8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080622d8'),
    (0x08062310, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062310'),
    (0x080623e8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080623e8'),
    (0x08062600, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062600'),
    (0x080626bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080626bc'),
    (0x08062760, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062760'),
    (0x08062814, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062814'),
    (0x08062850, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062850'),
    (0x08062928, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062928'),
    (0x080629c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080629c4'),
    (0x08062a94, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062a94'),
    (0x08062bd4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08062bd4'),

    # ===== BANISHER_OF_THE_LIGHT_CID = 0x1332 (card_info.inc REUSE; 5 slots) =====
    (0x0806215c, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_0806215c'),
    (0x08062200, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_08062200'),
    (0x08062284, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_08062284'),
    (0x080624cc, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_080624cc'),
    (0x080628e4, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_080628e4'),

    # ===== gEquipChainSlotRefs = 0x0201bb90 (ewram.inc REUSE; 3 slots) =====
    (0x0806230c, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_refs_0806230c'),
    (0x08062758, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_refs_08062758'),
    (0x08062c34, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_refs_08062c34'),

    # ===== gDuelFieldSlots = 0x0201c510 (ewram.inc REUSE; 3 slots) =====
    (0x08062314, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_08062314'),
    (0x080626c0, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_080626c0'),
    (0x08062a98, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_08062a98'),

    # ===== FIELD_STATE_OFF = 0x1cf4 (duel_field.inc REUSE; 3 slots) =====
    (0x08062790, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_08062790'),
    (0x0806296c, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0806296c'),
    (0x08062bd8, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_08062bd8'),

    # ===== PROTECTOR_OF_SANCTUARY_CID = 0x178b (card_info.inc REUSE; 2 slots) =====
    (0x08062970, 0x0000178b, 'PROTECTOR_OF_SANCTUARY_CID', 'protector_cid_08062970'),
    (0x08062bdc, 0x0000178b, 'PROTECTOR_OF_SANCTUARY_CID', 'protector_cid_08062bdc'),

    # ===== gP1FieldArrayCBase = 0x0201c600 (ewram.inc REUSE; 1 slot) =====
    (0x0806220c, 0x0201c600, 'gP1FieldArrayCBase', 'field_array_c_0806220c'),

    # ===== HORUS_LV4_CID = 0x17d2 (card_info.inc REUSE; 1 slot) =====
    (0x080620b4, 0x000017d2, 'HORUS_LV4_CID', 'horus_lv4_cid_080620b4'),

    # ===== SILENT_SWORDSMAN_LV5_CID = 0x1814 (card_info.inc REUSE; 1 slot) =====
    (0x08062634, 0x00001814, 'SILENT_SWORDSMAN_LV5_CID', 'ss_lv5_cid_08062634'),

    # ===== SILENT_MAGICIAN_LV8_CID = 0x181a (card_info.inc REUSE; 1 slot) =====
    (0x080626f0, 0x0000181a, 'SILENT_MAGICIAN_LV8_CID', 'sm_lv8_cid_080626f0'),

    # ===== RING_OF_MAGNETISM_CID = 0x1318 (card_info.inc REUSE; 1 slot) =====
    (0x08062c38, 0x00001318, 'RING_OF_MAGNETISM_CID', 'ring_of_magnetism_cid_08062c38'),

    # ===== ATK_THRESHOLD_2999 = 0xbb7 (duel_field.inc NEW; 1 slot) =====
    (0x08062084, 0x00000bb7, 'ATK_THRESHOLD_2999', 'atk_threshold_2999_08062084'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    3 slots: PTR_gP1LifePoints_* with DATA ref to gP1LifePoints global
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x08062204, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08062204'),
    (0x080622d4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080622d4'),
    (0x08062924, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08062924'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    2 fn-ptr slots: rename + EOL (pure ASCII)
#    Values verified: 0x08062bc8=0x080507ad (check_equip_slot_eligible_by_type_query+1)
#                     0x08062bcc=0x08051abd (check_equip_slot_eligible_by_side_and_setcode+1)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08062bc8, 'zone_pair_pred_07ac_ptr_08062bc8',
     '[fn-ptr] check_equip_slot_eligible_by_type_query+1 (0x080507ac+1)'),
    (0x08062bcc, 'zone_pair_pred_1abc_ptr_08062bcc',
     '[fn-ptr] check_equip_slot_eligible_by_side_and_setcode+1 (0x08051abc+1)'),
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (fn_entry_addr, new_plate_text)
#    3 plates: 2 stale FUN_ substitutions + 1 CJK full ASCII rewrite
#    All new_plate_text is pure ASCII (no characters > 0x7F).
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. check_equip_slot_eligible_field_spell_by_hand_set_code_dispatch @ 0x08061f80
    #    Stale: "called by FUN_08059110 (0x08059110)"
    #    Correct current name (naming-proposals.csv L1373):
    #      tick_equip_activation_if_field_spell_hand_ok
    (0x08061f80,
     'Equip slot activation eligibility predicate for field spell by hand set-code dispatch. '
     'Iterates hand slots; extracts set_code from slot[+4] bits[14:8] and from gP1FieldArrayCBase '
     'zone_idx entry bits[23:16]<<1; dispatches effect handler if set_code matches. '
     'Returns 1 on first matching dispatch, 0 if no match found. '
     'called by tick_equip_activation_if_field_spell_hand_ok (0x08059110).'
    ),

    # 2. check_equip_slot_state_active_with_card_present @ 0x080622dc
    #    Stale: "called by FUN_080619c0 (0x080619c0)"
    #    Correct current name (naming-proposals.csv L1700):
    #      check_equip_slot_eligible_by_active_ctx_score_threshold
    (0x080622dc,
     'Equip slot state predicate: checks gEquipChainSlotRefs[+0x8] chain slot state '
     '(must be nonzero) and slot card_id presence (bits[12:0] of slot[+2] != 0). '
     'Returns 1 if both conditions pass, 0 otherwise. '
     'called by check_equip_slot_eligible_by_active_ctx_score_threshold (0x080619c0).'
    ),

    # 3. check_equip_slot_eligible_horus_lv4_chain_with_banisher @ 0x08062090
    #    CJK mojibake plate (L15515/L15519/L15520) -> full ASCII rewrite
    (0x08062090,
     'Equip slot eligibility predicate, returns 0/1. '
     'Extracts zone_idx (bits[6:2] = lsls #0x1a; lsrs #0x1b) and player_id (bit0) from slot[+2]. '
     'Calls check_value_in_slot_chain(player_id, zone_idx, HORUS_LV4_CID=0x17d2, chain_type=0xb): '
     'if Horus LV4 is in slot chain, calls '
     'check_equip_slot_eligible_banisher_absent_with_dispatch(slot, arg) and returns its result; '
     'else returns 0. '
     'Semantic: equip chain containing Horus LV4 is prerequisite for Banisher-absent dispatch evaluation. '
     'Constants: HORUS_LV4_CID=0x17d2 (Horus the Black Flame Dragon LV4, pw=75830094), '
     'CHAIN_TYPE=0xb (equip chain node type code), '
     'ZONE_IDX_SHIFT=0x1a/0x1b (slot[+2] bits[6:2] extract).'
    ),
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
    print("=== RefineF07Seg8Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nE = 0
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
            print("[C dry] 0x%08x rename %s eol=%s" % (slot_int, label, repr(eol))); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu is not None:
                bad = any(ord(ch) > 127 for ch in eol)
                if bad:
                    print("[C WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_int)
                else:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- E. PLATE_REWRITES ---
    print("--- E. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    for fn_int, new_plate in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(fn_int))
        if cu is None:
            print("[E FAIL] no CodeUnit at 0x%08x" % fn_int); continue
        bad = any(ord(ch) > 127 for ch in new_plate)
        if bad:
            print("[E FAIL] non-ASCII in new_plate @ 0x%08x -- skipping" % fn_int)
            continue
        if DRY:
            existing = cu.getComment(CodeUnit.PLATE_COMMENT)
            has_cjk = existing is not None and any(ord(ch) > 127 for ch in existing)
            print("[E dry] 0x%08x: rewrite plate (%d chars); existing has_cjk=%s" % (
                fn_int, len(new_plate), has_cjk))
            nE += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[E ok] 0x%08x plate rewrite (%d chars)" % (fn_int, len(new_plate))); nE += 1

    print("[done] A=%d B=%d C=%d E=%d (DRY=%s)" % (nA, nB, nC, nE, DRY))
    print("EQ=%d REF=%d RENAME=%d PLATE=%d (expected 50+3+2+3)" % (nA, nB, nC, nE))


main()
