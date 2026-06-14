# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg6Slots.py -- F07 Seg-6 (0x08060898..0x080613b4)
#   Symbolizes 47 auto-name slots: EQ=47
#   Proposal: doc/dev/refine/F07-Seg-6.proposal.md (PASS)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (47 slots)
#   D. PLATE_SUBS -- stale FUN_ substring replacements (if any)
#   E. PLATE_REWRITES -- 6 CJK plate full rewrites to ASCII
#
# Prerequisites (already in constants/card_info.inc):
#   QUEENS_KNIGHT_CID=0x157f, CONTRACT_WITH_EXODIA_CID=0x165b, SAGES_STONE_CID=0x167e
#   OJAMA_YELLOW_CID=0x16b3, FENRIR_CID=0x16c6, CHAOS_END_CID=0x16d1
#   CHAOS_EMPEROR_DRAGON_CID=0x16e4
#   RIGHT_LEG_FORBIDDEN_ONE_CID=0x0fb7, LEFT_LEG_FORBIDDEN_ONE_CID=0x0fb8
#   RIGHT_ARM_FORBIDDEN_ONE_CID=0x0fb9, LEFT_ARM_FORBIDDEN_ONE_CID=0x0fba
#   EXODIA_THE_FORBIDDEN_ONE_CID=0x0fbb
# Already in ewram.inc:
#   gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868, gDuelFieldSlots=0x0201c510
#   gEquipChainSlotRefs=0x0201bb90, P1LP_BLOCK2_OFF_1CE8=0x1ce8
# Already in duel_field.inc:
#   FIELD_STATE_OFF=0x1cf4, ZONE_DETAIL_FIELD_MASK_F88=0x00f88000
# Also in card_info.inc (all reuse):
#   FRIENDSHIP_CID=0x167a, UNITY_CID=0x167b, MUSTERING_DARK_SCORPIONS_CID=0x169e
#   DARK_MAGICIAN_GIRL_CID=0x129e, DON_ZALOOG_CID=0x1532
#   BANISHER_OF_THE_LIGHT_CID=0x1332, TERRORKING_ARCHFIEND_CID=0x1691
#   CLIFF_THE_TRAP_REMOVER_CID=0x161e, DARK_SCORPION_CHICK_CID=0x1656
#   DARK_SCORPION_GORG_THE_STRONG_CID=0x1685, DARK_SCORPION_MEANAE_CID=0x1686
#   CRIMSON_NINJA_CID=0x16b8, BLACK_LUSTER_SOLDIER_ENVOY_CID=0x16cb
#   OJAMA_GREEN_CID=0x1681, OJAMA_BLACK_CID=0x16b4, EXODIA_NECROSS_CID=0x1645
#
# FUNC_RENAME=0, carve=0, REF=0
# PTR_ slots (3x PTR_gP1LifePoints_*) skipped per scope convention (already named)
# Block disasm literal pools handled by DisassembleF07Seg6Blocks.py
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-164740-pre-f07seg6

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values verified against ROM via proposal review.
#    47 slots total. slot_label != const_name per convention.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== gP1LifePoints = 0x0201c4e0 (ewram.inc reuse; 10 slots) =====
    (0x08060954, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060954'),
    (0x08060a50, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060a50'),
    (0x08060bf0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060bf0'),
    (0x08060cf8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060cf8'),
    (0x08060d40, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060d40'),
    (0x08060db8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08060db8'),
    (0x08061294, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061294'),
    (0x080612cc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080612cc'),
    (0x0806130c, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_0806130c'),
    (0x080613b0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080613b0'),

    # ===== PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc reuse; 9 slots) =====
    (0x080608d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080608d4'),
    (0x08060bf4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060bf4'),
    (0x08060d44, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060d44'),
    (0x08060f9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08060f9c'),
    (0x08061100, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061100'),
    (0x080611b4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080611b4'),
    (0x08061298, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061298'),
    (0x080612d0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080612d0'),
    (0x08061310, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061310'),

    # ===== P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (ewram.inc reuse; 2 slots) =====
    (0x08060958, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_b2_off_08060958'),
    (0x08060dbc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_b2_off_08060dbc'),

    # ===== FIELD_STATE_OFF = 0x1cf4 (duel_field.inc reuse; 1 slot) =====
    (0x08060dc0, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_08060dc0'),

    # ===== ZONE_DETAIL_FIELD_MASK_F88 = 0x00f88000 (duel_field.inc reuse; 1 slot) =====
    (0x08060cf4, 0x00f88000, 'ZONE_DETAIL_FIELD_MASK_F88', 'zone_field_mask_08060cf4'),

    # ===== gDuelFieldSlots = 0x0201c510 (ewram.inc reuse; 2 slots) =====
    (0x08060fa0, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_08060fa0'),
    (0x080611b8, 0x0201c510, 'gDuelFieldSlots', 'gduelfield_ptr_080611b8'),

    # ===== gEquipChainSlotRefs = 0x0201bb90 (ewram.inc reuse; 1 slot) =====
    # Note: plate at 0x08060fe8 incorrectly says "DUEL_STATE_PTR" -- plate rewrite corrects this
    (0x08060fd8, 0x0201bb90, 'gEquipChainSlotRefs', 'gequiprefs_ptr_08060fd8'),

    # ===== CID equates -- REUSE (all confirmed in card_info.inc) =====
    (0x08060c20, 0x0000167a, 'FRIENDSHIP_CID',                    'friendship_cid_08060c20'),
    (0x08060c24, 0x0000167b, 'UNITY_CID',                         'unity_cid_08060c24'),
    (0x08060c5c, 0x0000169e, 'MUSTERING_DARK_SCORPIONS_CID',      'mustering_cid_08060c5c'),
    (0x08060c6c, 0x0000129e, 'DARK_MAGICIAN_GIRL_CID',            'dmg_cid_08060c6c'),
    (0x08060c88, 0x00001532, 'DON_ZALOOG_CID',                    'don_zaloog_cid_08060c88'),
    (0x08060cf0, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',         'banisher_cid_08060cf0'),
    (0x08060cfc, 0x00001691, 'TERRORKING_ARCHFIEND_CID',          'terrorking_cid_08060cfc'),
    (0x08060dc4, 0x00001532, 'DON_ZALOOG_CID',                    'don_zaloog_cid_08060dc4'),
    (0x08060dc8, 0x0000161e, 'CLIFF_THE_TRAP_REMOVER_CID',        'cliff_cid_08060dc8'),
    (0x08060dcc, 0x00001656, 'DARK_SCORPION_CHICK_CID',           'ds_chick_cid_08060dcc'),
    (0x08060dd0, 0x00001685, 'DARK_SCORPION_GORG_THE_STRONG_CID', 'ds_gorg_cid_08060dd0'),
    (0x08060dd4, 0x00001686, 'DARK_SCORPION_MEANAE_CID',          'ds_meanae_cid_08060dd4'),
    (0x08060e9c, 0x000016b8, 'CRIMSON_NINJA_CID',                 'crimson_ninja_cid_08060e9c'),
    (0x080611bc, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID',    'bls_envoy_cid_080611bc'),
    (0x08061208, 0x00001681, 'OJAMA_GREEN_CID',                   'ojama_green_cid_08061208'),
    (0x08061210, 0x000016b4, 'OJAMA_BLACK_CID',                   'ojama_black_cid_08061210'),
    (0x080612d4, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID',    'bls_envoy_cid_080612d4'),

    # ===== CID equates -- NEW (verified 0 hits in card_info.inc; added above) =====
    (0x08060c50, 0x0000167e, 'SAGES_STONE_CID',        'sages_stone_cid_08060c50'),
    (0x08060c64, 0x0000157f, 'QUEENS_KNIGHT_CID',      'queens_knight_cid_08060c64'),
    (0x0806120c, 0x000016b3, 'OJAMA_YELLOW_CID',       'ojama_yellow_cid_0806120c'),
    (0x080612d8, 0x000016e4, 'CHAOS_EMPEROR_DRAGON_CID', 'ced_cid_080612d8'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (fn_entry_addr, old_substr, new_substr)
#    Fix stale FUN_ references in plate comments.
#    Text must be pure ASCII.
#    Seg-6 has no known stale FUN_ references in pre-existing named functions.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # None for Seg-6 main named functions
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (fn_entry_addr, new_plate_text)
#    Full plate rewrite for 6 CJK-containing plates + 1 semantic correction.
#    All new_plate_text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. check_equip_slot_eligible_by_effect_sum_vs_tier__08060974 @ 0x08060974
    (0x08060974,
     'Equip slot eligibility predicate. First calls sum_equip_slot_effect_values_for_player(player_id)'
     ' -> r4 (effect sum). Then calls classify_equip_card_id_tier_abcx(slot_ptr) -> r0 (tier).'
     ' If effect_sum < tier: return 0 (effect not yet at tier). Else: call'
     ' dispatch_effect_for_neo_daedalus_eligible_slot(slot_ptr, arg) and return its result.'
     ' Semantics: when cumulative equip effect sum reaches the tier threshold, fires Neo Daedalus'
     ' effect dispatch. Sibling of check_equip_slot_eligible_by_effect_sum_vs_tier (0x080608e0).'
     ' Constants: tier computed dynamically by classify_equip_card_id_tier_abcx (no static constant).'
     ' Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to neo_daedalus dispatch)'
     ' Returns: r0=u32 (0 if effect_sum < tier; else forwarded from neo_daedalus dispatch)'
     ' Callees: sum_equip_slot_effect_values_for_player, classify_equip_card_id_tier_abcx,'
     '          dispatch_effect_for_neo_daedalus_eligible_slot'
    ),

    # 2. check_equip_slot_eligible_chain_present_with_neo_daedalus @ 0x08060a5c
    (0x08060a5c,
     'Equip slot eligibility predicate, returns 0/1. Calls check_value_in_slot_chain(player_id,'
     ' card_id, type=0xb); if target value absent returns 0. On match calls'
     ' check_neo_daedalus_placement_eligible(slot_ptr, arg) and forwards result.'
     ' Semantics: equip chain must contain the target card before Neo Daedalus placement check.'
     ' Sibling of check_equip_slot_eligible_with_chain_absent_and_lp_slot (symmetric branch).'
     ' Constants: CHAIN_TYPE = 0xb (equip node chain search type)'
     ' Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to neo_daedalus check)'
     ' Returns: r0=u32 (0 if chain absent; else forwarded from neo_daedalus check)'
     ' Callees: check_value_in_slot_chain, check_neo_daedalus_placement_eligible'
    ),

    # 3. check_equip_slot_eligible_by_companion_card_and_paired_slot @ 0x08060c30
    (0x08060c30,
     'Equip slot eligibility predicate, returns 0/1. Pre-cond: check_neo_daedalus_placement_eligible;'
     ' on fail returns 0. Reads slot ldrh[+0] card_id, selects companion card via dispatch table:'
     ' card_id == SAGES_STONE_CID (0x167e) -> companion = DARK_MAGICIAN_GIRL_CID (0x129e);'
     ' card_id == SAGES_STONE_CID-0xc8 (0x15b6) -> companion = QUEENS_KNIGHT_CID (0x157f);'
     ' card_id == MUSTERING_DARK_SCORPIONS_CID (0x169e) -> companion = DON_ZALOOG_CID (0x1532).'
     ' Calls count_paired_slots_with_field5_default(player_id, companion_cid); returns 1 if nonzero.'
     ' Constants: SAGES_STONE_CID=0x167e, MUSTERING_DARK_SCORPIONS_CID=0x169e,'
     '            DARK_MAGICIAN_GIRL_CID=0x129e, QUEENS_KNIGHT_CID=0x157f, DON_ZALOOG_CID=0x1532'
     ' Inputs: r0=SlotPtr* slot_ptr (ldrh[+0]=card_id, byte[+2] bit0=player_id)'
     ' Returns: r0=u32 (1 if neo_daedalus ok and companion paired with field5, 0 otherwise)'
     ' Callees: check_neo_daedalus_placement_eligible, count_paired_slots_with_field5_default'
    ),

    # 4. check_equip_slot_eligible_by_field6_guard_and_chain_absent @ 0x08060e24
    (0x08060e24,
     'Equip slot eligibility predicate, returns 0/1. Extracts field6 from slot ldrh[+4] bits[13:6]'
     ' (lsls #0x11; lsrs #0x17). Calls dispatch_equip_slot_scan_with_field6_guard(player_id, field6,'
     ' arg3=1, sp[0]=0); if returns 0 returns 0. On pass calls check_equip_slot_chain_absent(slot_ptr,'
     ' arg) and returns result. Semantics: field6 scan gate before equip chain absent check.'
     ' Constants: FIELD6_SHIFT=lsls #0x11/lsrs #0x17 (net=6-bit field); SCAN_ARG3=1; SCAN_ARG4=0'
     ' Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to chain_absent)'
     ' Returns: r0=u32 (0 if scan fails; else forwarded from chain_absent)'
     ' Callees: dispatch_equip_slot_scan_with_field6_guard, check_equip_slot_chain_absent'
    ),

    # 5. check_equip_slot_eligible_chain_absent_with_spell_zone_and_display @ 0x08060fe8
    # Also corrects semantic error: "DUEL_STATE_PTR" -> "gEquipChainSlotRefs"
    (0x08060fe8,
     'Equip slot eligibility predicate, returns 0 or dispatch result. Three-level check:'
     ' (1) check_equip_slot_chain_absent(slot_ptr) -- if 0 return 0;'
     ' (2) check_spell_zone_slot_placeable(player_id) -- if 0 return 0;'
     ' (3) dispatch_effect_by_card_id_with_display_lookup(slot_ptr, arg) -- return its value.'
     ' Differs from check_equip_slot_eligible_with_chain_absent_and_spell_dispatch (0x08060ea8):'
     ' uses dispatch_effect_by_card_id_with_display_lookup instead of dispatch_effect_handler_by_card_id.'
     ' Global: gEquipChainSlotRefs=0x0201bb90 (NOT DUEL_STATE_PTR -- corrected).'
     ' Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to display lookup)'
     ' Returns: r0=u32 (0 if either guard fails; else forwarded from display dispatch)'
     ' Callees: check_equip_slot_chain_absent, check_spell_zone_slot_placeable,'
     '          dispatch_effect_by_card_id_with_display_lookup'
    ),

    # 6. check_equip_slot_eligible_neo_daedalus_with_hand_empty @ 0x080612e4
    (0x080612e4,
     'Neo Daedalus equip slot eligibility predicate. Guard: when hand alt count field'
     ' gP1LifePoints[player*0x868+0x14] != 0, returns 0 (hand not empty). When count == 0,'
     ' calls dispatch_effect_for_neo_daedalus_eligible_slot(slot_ptr, aux) and returns its bool'
     ' result (1=eligible, 0=rejected). Condition: equip hand count must be zero before dispatching'
     ' Neo Daedalus effect eligibility logic.'
     ' Constants: gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868,'
     '            HAND_COUNT_OFFSET=0x14 (zone occupy count field; count==0 required),'
     '            player_id from slot[+2] bit0'
     ' Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to neo_daedalus dispatch)'
     ' Returns: r0=u32 (0 if hand count != 0; else forwarded from neo_daedalus dispatch)'
     ' Callees: dispatch_effect_for_neo_daedalus_eligible_slot'
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
    print("=== RefineF07Seg6Slots (DRY=%s) ===" % DRY)
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
    print("EQ=%d PLATE_SUB=%d PLATE_REWRITE=%d (expected 47+0+6)" % (nA, nD, nE))


main()
