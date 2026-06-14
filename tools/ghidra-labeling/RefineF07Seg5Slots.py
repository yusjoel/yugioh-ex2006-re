# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg5Slots.py -- F07 Seg-5 (0x0805fc94..0x08060898)
#   Symbolizes 53 auto-name slots: EQ=53
#   Proposal: doc/dev/refine/F07-Seg-5.proposal.md (iter-2 PASS equivalent)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (53 slots)
#   D. PLATE_SUBS -- 4 stale FUN_ substring replacements
#   E. PLATE_REWRITES -- 6 CJK plate full rewrites to ASCII
#
# Prerequisites:
#   - constants/card_info.inc +8:
#       PEOPLE_RUNNING_ABOUT_CID = 0x000015ca
#       OPPRESSED_PEOPLE_CID = 0x000015cb
#       UNITED_RESISTANCE_CID = 0x000015cc
#       REASONING_CID = 0x0000159a
#       HELPING_ROBO_FOR_COMBAT_CID = 0x000015dc
#       THUNDER_OF_RULER_CID = 0x000015f0
#       METEORAIN_CID = 0x000015f2
#       PINEAPPLE_BLAST_CID = 0x000015f3
#   - constants/ewram.inc +3:
#       LP_SLOT_ACTIVE_OFF = 0x00000010
#       LP_LOOP_CEIL_OFF = 0x0000000c
#       HAND_SLOT_TO_ZONE_COUNT_NEG_OFF = 0xfffffbf4
#   - constants/duel_field.inc +1:
#       ZONE_DETAIL_FIELD_MASK_F88 = 0x00f88000
#   (all added to .inc files before script run)
#
# FUNC_RENAME=0 (all 34 existing functions have correct names)
# carve=0 (all ROM_INCBIN blocks are R4 disasm targets)
# REF_SLOTS=0 (no RAM/ROM pointer REF slots in Seg-5)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-154713-pre-f07seg5

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
#    53 slots total.
#    slot_label != const_name (per convention).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== gP1LifePoints = 0x0201c4e0 (ewram.inc reuse; 17 slots) =====
    (0x0805fddc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805fddc'),
    (0x0805ff34, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805ff34'),
    (0x0805ff8c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0805ff8c'),
    (0x0806007c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806007c'),
    (0x080600f4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080600f4'),
    (0x08060148, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060148'),
    (0x08060188, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060188'),
    (0x0806025c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806025c'),
    (0x0806030c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806030c'),
    (0x08060450, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060450'),
    (0x0806049c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806049c'),
    (0x0806050c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806050c'),
    (0x08060578, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060578'),
    (0x0806067c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806067c'),
    (0x08060700, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060700'),
    (0x080607dc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080607dc'),
    (0x08060874, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060874'),

    # ===== PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc reuse; 14 slots) =====
    (0x0805fd18, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805fd18'),
    (0x0805fde0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805fde0'),
    (0x0805fe84, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805fe84'),
    (0x0805ff38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805ff38'),
    (0x0805ff90, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0805ff90'),
    (0x08060080, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060080'),
    (0x080600f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080600f8'),
    (0x0806014c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0806014c'),
    (0x08060260, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060260'),
    (0x08060510, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060510'),
    (0x0806057c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0806057c'),
    (0x08060680, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060680'),
    (0x080607e0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080607e0'),
    (0x08060878, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060878'),

    # ===== CID and scalar equates (REUSE; 16 slots) =====
    (0x0805fd14, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_0805fd14'),
    (0x0805fd1c, 0x0201c510, 'gDuelFieldSlots',     'gduelfield_ptr_0805fd1c'),
    (0x0805fd20, 0x00001318, 'RING_OF_MAGNETISM_CID', 'ring_of_magnetism_cid_0805fd20'),
    (0x0805fe88, 0x0201c8f8, 'gP1HandSlotArray',    'gp1hand_ptr_0805fe88'),
    (0x0805ffac, 0x0000159d, 'NECROVALLEY_CID',     'necrovalley_cid_0805ffac'),
    (0x080600f0, 0x0000159d, 'NECROVALLEY_CID',     'necrovalley_cid_080600f0'),
    (0x08060150, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_08060150'),
    (0x0806018c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_b2_off_0806018c'),
    (0x08060190, 0x00001cf4, 'FIELD_STATE_OFF',     'field_state_off_08060190'),
    (0x08060310, 0x00001cf4, 'FIELD_STATE_OFF',     'field_state_off_08060310'),
    (0x08060314, 0x000013f2, 'EQUIP_LOCKDOWN_CID',  'equip_lockdown_cid_08060314'),
    (0x08060374, 0x000015d3, 'SECOND_GOBLIN_CID',   'second_goblin_cid_08060374'),
    (0x08060458, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID', 'bewd_cid_08060458'),
    (0x080604a0, 0x00001cf4, 'FIELD_STATE_OFF',     'field_state_off_080604a0'),
    (0x08060704, 0x00001cf4, 'FIELD_STATE_OFF',     'field_state_off_08060704'),
    (0x08060838, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_b2_off_08060838'),

    # ===== CID equates (NEW; 3 slots) =====
    (0x0806054c, 0x000015ca, 'PEOPLE_RUNNING_ABOUT_CID', 'people_running_cid_0806054c'),
    (0x08060550, 0x000015cb, 'OPPRESSED_PEOPLE_CID',     'oppressed_people_cid_08060550'),
    (0x08060554, 0x000015cc, 'UNITED_RESISTANCE_CID',    'united_resistance_cid_08060554'),

    # ===== Scalar NEW equates (2 slots) =====
    (0x0805feac, 0xfffffbf4, 'HAND_SLOT_TO_ZONE_COUNT_NEG_OFF', 'hand_to_zone_neg_off_0805feac'),
    (0x08060264, 0x00f88000, 'ZONE_DETAIL_FIELD_MASK_F88',      'zone_detail_mask_08060264'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (fn_entry_addr, old_substr, new_substr)
#    Fix stale FUN_ references in plate comments.
#    4 fixes in Seg-5 range (asm/07 L10054, L10713, L11271, L11456).
#    Text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # check_equip_slot_eligible_by_zone_type_b0_with_field5 @ 0x0805ffb8
    # plate L10054: "Also called directly by FUN_0806001c (indeg=1)."
    (0x0805ffb8, 'FUN_0806001c',
     'check_equip_slot_eligible_type_b0_with_bit17_and_not_bit14'),

    # check_equip_slot_eligible_neo_daedalus_full_guard @ 0x080603b8
    # plate L10713: "Called exclusively by FUN_0805f9e4 (tags: [duel_field])"
    (0x080603b8, 'FUN_0805f9e4',
     'check_equip_slot_eligible_with_monster_count_gate'),

    # check_equip_slot_eligible_by_slot_value_vs_tier @ 0x08060788
    # plate L11271: "Called exclusively by FUN_080607b4 (indeg=0)"
    (0x08060788, 'FUN_080607b4',
     'check_equip_slot_eligible_by_lp_status_and_slot_value'),

    # check_equip_slot_eligible_by_lp_slot_and_effect_dispatch @ 0x08060898
    # plate L11456: "Called exclusively by FUN_08061660 (tags: [duel_field])"
    (0x08060898, 'FUN_08061660',
     'check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect'),
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (fn_entry_addr, new_plate_text)
#    Full plate rewrite for 6 CJK-containing plates.
#    All new_plate_text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # check_equip_slot_eligible_zone_type_or_neo_daedalus @ 0x0806019c
    # CJK plate at asm/07 L10378; replace with ASCII equivalent
    (0x0806019c,
     'Equip slot activation eligibility predicate, three-way return (0/1/2). '
     'Precondition: check_equip_slot_chain_absent passes (no active chain). '
     'Extracts zone_type from slot[+2] bits[10:6] (ZONE_TYPE_MASK=0xfc0, rshift 1 gives 5-bit zone). '
     'If zone_type <= 4 (monster zone): calls find_first_available_monster_slot_for_player(player_id); '
     'returns 1 if slot available (>= 0). '
     'Else: calls check_neo_daedalus_placement_eligible(slot_ptr, arg); returns 2 if passes. '
     'Any condition fails returns 0. '
     'Constants: ZONE_TYPE_MASK=0xfc0 (0xfc<<4); MONSTER_ZONE_MAX=4; '
     'RET_MONSTER=1; RET_NEO_DAEDALUS=2; ZONE_TYPE_SHIFT=1.'
    ),

    # check_equip_slot_eligible_neo_daedalus_with_zone_field_guard @ 0x080601dc
    # CJK plate at asm/07 L10420; replace with ASCII equivalent
    (0x080601dc,
     'Equip slot activation eligibility predicate, returns 0/1. '
     'Pre-call check_neo_daedalus_placement_eligible; if fails returns 0. '
     'Reads gP1LifePoints[player*0x868+0x10] (player state word); if 0 returns 0. '
     'Extracts zone_type mask 0xfc0 from slot[+2], compares 0x6c0 (0xd8<<3); mismatch returns 0. '
     'Validates detail_word bits[22:19] <= 4 and (detail_word & 0xf88000) == 0x708000. '
     'Reads low 13-bit card_id from gP1LifePoints zone array; '
     'calls check_card_field8_is_9 (9 = fail) and check_card_field5_is_nonzero (0 = fail). '
     'All pass returns 1. '
     'Constants: ZONE_TYPE_MASK=0xfc0; ZONE_TYPE_TARGET=0x6c0 (0xd8<<3); '
     'PLAYER_STRIDE=0x868; LP_STATUS_OFFSET=0x10; DETAIL_4BIT_MAX=4; '
     'FIELD_MASK=0xf88000 (bits[23:11]); FIELD_EXPECT=0x708000 (0xe1<<15).'
    ),

    # check_equip_slot_eligible_spell_zone_with_neo_daedalus @ 0x080602a8
    # CJK plate at asm/07 L10558; replace with ASCII equivalent
    (0x080602a8,
     'Equip slot activation eligibility predicate, returns 0/1. '
     'Three-stage condition chain: '
     '(1) check_spell_zone_slot_placeable(player_id) -- spell zone not placeable returns 0; '
     '(2) dispatch_effect_handler_by_card_id(player_id, card_id, mode=0) -- returns <= 1 returns 0; '
     '(3) check_neo_daedalus_placement_eligible(slot_ptr, arg) -- passes through return value. '
     'Semantic: spell zone available AND effect handler confirms AND Neo Daedalus placement passes. '
     'Constants: MODE_ZERO=0 (dispatch third arg fixed 0); DISPATCH_THRESHOLD=1 (must be > 1 to continue).'
    ),

    # check_equip_slot_eligible_by_duel_phase3_neo_daedalus @ 0x08060484
    # CJK plate at asm/07 L10838; replace with ASCII equivalent
    (0x08060484,
     'Equip slot activation eligibility predicate, returns 0/1. '
     'Reads gP1LifePoints[+0x1cf4] (global duel phase field); '
     'only when value == 3 calls check_neo_daedalus_placement_eligible(slot_ptr, r1_passthrough) '
     'and passes through its return value. '
     'If phase != 3 returns 0 directly. '
     'Semantic: only evaluates Neo Daedalus placement condition at duel phase 3. '
     'Constants: DUEL_PHASE_OFFSET=0x1cf4 (gP1LifePoints global phase field offset); '
     'REQUIRED_PHASE=3 (only phase 3 triggers Neo Daedalus check).'
    ),

    # check_equip_slot_eligible_with_monster_zone_and_neo_daedalus @ 0x08060684
    # CJK plate at asm/07 L11102; replace with ASCII equivalent
    (0x08060684,
     'Equip slot activation eligibility predicate with side effect writes, returns 0/2. '
     'On entry immediately writes strh 1 -> slot[+0xc] (initialize slot state word). '
     'Calls find_first_available_monster_slot_for_player(player_id): '
     'if monster slot available (>= 0) calls count_effect_node_zone_activations(slot_ptr); '
     'if activation count > 0 returns 2. '
     'If no monster slot or activation count == 0: '
     'writes strh 2 -> slot[+0xc] (update slot state to evaluated), '
     'calls check_neo_daedalus_placement_eligible; '
     'if passes and count_effect_node_zone_activations > 0 returns 2. '
     'All conditions fail returns 0. '
     'Constants: SLOT_STATE_INIT=1 (slot[+0xc] initial write); '
     'SLOT_STATE_EVALUATED=2 (slot[+0xc] no-monster-slot value); RETURN_ELIGIBLE=2.'
    ),

    # check_equip_slot_eligible_by_lp_status_and_slot_value @ 0x080607b4
    # CJK plate at asm/07 L11308; replace with ASCII equivalent
    (0x080607b4,
     'Equip slot activation eligibility predicate, returns 0/1. '
     'Reads gP1LifePoints[player*0x868+0x10] (player LP status word); '
     'if 0 returns 0 directly (no LP slot active). '
     'If nonzero calls check_equip_slot_eligible_by_slot_value_vs_tier(slot_ptr, arg) '
     'and passes through its return value. '
     'Semantic: only evaluates slot value vs tier comparison when LP status is nonzero. '
     'Constants: PLAYER_STRIDE=0x868; LP_STATUS_OFFSET=0x10 (gP1LifePoints player block LP status word).'
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
    print("=== RefineF07Seg5Slots (DRY=%s) ===" % DRY)
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nD = nE = 0

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

    # --- E. PLATE_REWRITES (CJK -> ASCII) ---
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

    print("[done] A=%d D=%d E=%d (DRY=%s)" % (nA, nD, nE, DRY))
    print("EQ=%d PLATE_SUB=%d PLATE_REWRITE=%d total_plates=%d (expected 53+4+6)" % (
        nA, nD, nE, nD + nE))


main()
