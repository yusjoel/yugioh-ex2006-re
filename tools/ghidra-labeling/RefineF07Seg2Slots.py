# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg2Slots.py -- F07 Seg-2 (0x0805cfec..0x0805e358)
#   Symbolizes 92 auto-name slots: EQ=65, REF=27
#   Proposal: doc/dev/refine/F07-Seg-2.proposal.md (iter-2 PASS)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (65 slots)
#   B. REF_SLOTS -- USER label on target + DATA ref from slot + slot rename (27 slots)
#
# PLATE=3 applied separately in this script (section D)
# FUNC_RENAME=0 (no function name conflicts)
# RENAME_SLOTS=0 (all auto-names cleared by EQ/REF sections)
#
# Prerequisites:
#   - constants/card_info.inc +19 new CIDs (added manually before script)
#   - constants/ewram.inc +1 P2_ZONE1_LP_OFF=0x87c (added manually before script)
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-pre-f07seg2

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
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ----- PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc reuse) x16 -----
    (0x0805d100, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d100'),
    (0x0805d4a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d4a4'),
    (0x0805d720, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d720'),
    (0x0805d7fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d7fc'),
    (0x0805d880, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d880'),
    (0x0805d908, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d908'),
    (0x0805d98c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805d98c'),
    (0x0805db48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805db48'),
    (0x0805df08, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805df08'),
    (0x0805df90, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805df90'),
    (0x0805dffc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805dffc'),
    (0x0805e090, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805e090'),
    (0x0805e148, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805e148'),
    (0x0805e250, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805e250'),
    (0x0805e27c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805e27c'),
    (0x0805e0e0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0805e0e0'),

    # ----- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (ewram.inc reuse) x6 -----
    (0x0805d058, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805d058'),
    (0x0805d640, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805d640'),
    (0x0805d984, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805d984'),
    (0x0805da68, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805da68'),
    (0x0805dff4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805dff4'),
    (0x0805e08c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0805e08c'),

    # ----- FIELD_STATE_OFF = 0x1cf4 (duel_field.inc reuse) x6 -----
    (0x0805d05c, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805d05c'),
    (0x0805d0fc, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805d0fc'),
    (0x0805d3cc, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805d3cc'),
    (0x0805da64, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805da64'),
    (0x0805dff8, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805dff8'),
    (0x0805e088, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_0805e088'),

    # ----- EFFECT_ZONE_BITMASK_OFF = 0x10d0 (duel_field.inc reuse) x1 -----
    (0x0805d988, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF', 'effect_zone_bitmask_off_0805d988'),

    # ----- P2_ZONE1_LP_OFF = 0x87c (ewram.inc new) x1 -----
    (0x0805d798, 0x0000087c, 'P2_ZONE1_LP_OFF', 'p2_zone1_lp_off_0805d798'),

    # ----- CID equates (REUSE card_info.inc) -----
    (0x0805d188, 0x000015f1, 'SPELL_SHIELD_TYPE8_CID',         'spell_shield_type8_cid_0805d188'),
    (0x0805d1a4, 0x000012ff, 'SEVEN_TOOLS_OF_THE_BANDIT_CID',  'seven_tools_cid_0805d1a4'),
    (0x0805d1b4, 0x0000131c, 'cid_131c',                       'cid_131c_0805d1b4'),
    (0x0805d1dc, 0x000014b6, 'DARK_BALTER_THE_TERRIBLE_CID',   'dark_balter_cid_0805d1dc'),
    (0x0805d24c, 0x000017c6, 'SORCERER_OF_DARK_MAGIC_CID',     'sorcerer_dark_magic_cid_0805d24c'),
    (0x0805d250, 0x000016a6, 'SPELL_VANISHING_CID',            'spell_vanishing_cid_0805d250'),
    (0x0805d260, 0x00001634, 'ANTI_SPELL_CID',                 'anti_spell_cid_0805d260'),
    (0x0805d2e0, 0x000019e1, 'GOBLIN_OUT_OF_FRYING_PAN_CID',   'goblin_frying_pan_cid_0805d2e0'),
    (0x0805d2f0, 0x000019e2, 'MALFUNCTION_CID',                'malfunction_cid_0805d2f0'),
    (0x0805d338, 0x000012ea, 'MONSTER_REBORN_CID',             'monster_reborn_cid_0805d338'),
    (0x0805d384, 0x00001246, 'HARPIES_FEATHER_DUSTER_CID',     'harpies_feather_duster_cid_0805d384'),
    (0x0805d510, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',      'banisher_of_light_cid_0805d510'),
    (0x0805d524, 0x000012ec, 'POT_OF_GREED_CID',               'pot_of_greed_cid_0805d524'),
    (0x0805d5f0, 0x000018a6, 'EHERO_AVIAN_CID',                'ehero_avian_cid_0805d5f0'),
    (0x0805d6f0, 0x00001325, 'DELINQUENT_DUO_CID',             'delinquent_duo_cid_0805d6f0'),
    (0x0805d6fc, 0x0000132b, 'THE_FORCEFUL_SENTRY_CID',        'forceful_sentry_cid_0805d6fc'),
    (0x0805dad4, 0x0000135d, 'LIGHT_OF_INTERVENTION_CID',      'light_of_intervention_cid_0805dad4'),
    (0x0805dcc8, 0x0000134d, 'DRIVING_SNOW_CID',               'driving_snow_cid_0805dcc8'),
    (0x0805dd80, 0x00001350, 'cid_1350',                       'cid_1350_0805dd80'),
    (0x0805dd8c, 0x00001351, 'cid_1351',                       'cid_1351_0805dd8c'),

    # ----- CID equates (NEW card_info.inc - added before script run) -----
    (0x0805d18c, 0x0000140d, 'MAGIC_DRAIN_CID',                'magic_drain_cid_0805d18c'),
    (0x0805d190, 0x000012f7, 'cid_12f7',                       'cid_12f7_0805d190'),
    (0x0805d1ec, 0x0000148f, 'RIRYOKU_FIELD_CID',              'riryoku_field_cid_0805d1ec'),
    (0x0805d208, 0x0000153e, 'TUTAN_MASK_CID',                 'tutan_mask_cid_0805d208'),
    (0x0805d218, 0x00001541, 'CURSE_OF_ROYAL_CID',             'curse_of_royal_cid_0805d218'),
    (0x0805d27c, 0x00001721, 'TRAP_JAMMER_CID',                'trap_jammer_cid_0805d27c'),
    (0x0805d28c, 0x0000176b, 'ARMOR_BREAK_CID',                'armor_break_cid_0805d28c'),
    (0x0805d2b4, 0x000018de, 'ROYAL_SURRENDER_CID',            'royal_surrender_cid_0805d2b4'),
    (0x0805d2c4, 0x000018dd, 'SPELL_STOPPING_STATUTE_CID',     'spell_stopping_statute_cid_0805d2c4'),
    (0x0805d314, 0x000010f6, 'DARK_HOLE_CID',                  'dark_hole_cid_0805d314'),
    (0x0805d35c, 0x000010f7, 'RAIGEKI_CID',                    'raigeki_cid_0805d35c'),
    (0x0805dcd4, 0x0000135b, 'cid_135b',                       'cid_135b_0805dcd4'),
    (0x0805e2f8, 0x00001288, 'ALPHA_MAGNET_WARRIOR_CID',       'alpha_magnet_warrior_cid_0805e2f8'),
    (0x0805e2fc, 0x0000129b, 'BETA_MAGNET_WARRIOR_CID',        'beta_magnet_warrior_cid_0805e2fc'),
    (0x0805e300, 0x000012b8, 'GAMMA_MAGNET_WARRIOR_CID',       'gamma_magnet_warrior_cid_0805e300'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # ----- gP1LifePoints = 0x0201c4e0 (ewram.inc) x14 -----
    (0x0805d054, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d054'),
    (0x0805d3c8, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d3c8'),
    (0x0805d63c, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d63c'),
    (0x0805d71c, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d71c'),
    (0x0805d794, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d794'),
    (0x0805d7f8, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d7f8'),
    (0x0805da60, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805da60'),
    (0x0805dcc4, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805dcc4'),
    (0x0805d980, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805d980'),
    (0x0805df04, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805df04'),
    (0x0805dff0, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805dff0'),
    (0x0805e084, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805e084'),
    (0x0805e144, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805e144'),
    (0x0805e278, 0x0201c4e0, 'gP1LifePoints', 'p1lp_ptr_0805e278'),

    # ----- gDuelFieldSlots = 0x0201c510 (ewram.inc) x7 -----
    (0x0805d4a8, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805d4a8'),
    (0x0805d884, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805d884'),
    (0x0805d90c, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805d90c'),
    (0x0805db4c, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805db4c'),
    (0x0805df8c, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805df8c'),
    (0x0805e0e4, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805e0e4'),
    (0x0805e254, 0x0201c510, 'gDuelFieldSlots', 'duel_field_slots_0805e254'),

    # ----- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc) x4 -----
    (0x0805d9c4, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805d9c4'),
    (0x0805e0dc, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805e0dc'),
    (0x0805e1fc, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805e1fc'),
    (0x0805e34c, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_slot_refs_0805e34c'),

    # ----- gDuelPhaseFlags = 0x0201b290 (ewram.inc) x1 -----
    (0x0805db50, 0x0201b290, 'gDuelPhaseFlags', 'duel_phase_flags_0805db50'),

    # ----- check_equip_slot_eligible_by_equip_type+1 = 0x08051319 (fn ptr) x1 -----
    (0x0805df94, 0x08051319, 'check_equip_slot_eligible_by_equip_type+1',
     'equip_type_check_fn_ptr_0805df94'),
]

# ---------------------------------------------------------------------------
# D. PLATE_COMMENTS: (fn_entry_addr, plate_text_ascii)
#    Sets PLATE_COMMENT at function entry. Text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_COMMENTS = [
    (
        0x0805d118,
        'BST gate: reads card_id from [r0+0], performs binary-search-style cmp/branch '
        'over 32 card IDs (range 0x10f6..0x19e2). Each leaf: calls '
        'check_effect_slot_is_equip_activatable then a per-card-set predicate '
        '(check_spell_zone_effect_activatable / check_equip_zone_has_field5_card / '
        'check_monster_slots_nonzero_for_card_player etc). Returns r0=0 or 1.'
    ),
    (
        0x0805dae0,
        'Zone flag guard: r0=effect_node_ptr, r1=player_id_byte, r2=slot_type. '
        'Guards: r0==0 or zone_bit12==0 or side/type already matched '
        '(read_effect_slot_side_and_type) -> return 0. '
        'Sets [gDuelPhaseFlags+0x4c0]=player_id_bit, calls '
        'set_equip_activation_state_by_mode_alt(effect_node, player_id_byte, slot_type), '
        'then clears [gDuelPhaseFlags+0x4c0]=0. '
        'Returns result of set_equip_activation_state_by_mode_alt.'
    ),
    (
        0x0805df60,
        'Outer loop player=[0..1], inner loop slot=[0..4] x stride 0x14: checks '
        'gDuelFieldSlots entry bit19 nonzero AND [+8]=0 AND [+6]!=0 => return 1 '
        'immediately. Fallback: calls invoke_count_zone_pair_hits_full_range('
        'equip_slot_ptr, fn_ptr=check_equip_slot_eligible_by_equip_type); '
        'result>0 => return 1, else return 0.'
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
    print("=== RefineF07Seg2Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nD = 0
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
        # fn-ptr slots: target may be in ROM code space, not EWRAM -- skip re-label for those
        base_gas = gas_label.split('+')[0]
        tgt_a = _addr(tgt_int)
        if base_gas not in made:
            try:
                createLabel(tgt_a, base_gas, True, SourceType.USER_DEFINED)
            except Exception as e:
                print("[B warn] createLabel at 0x%08x: %s" % (tgt_int, e))
            made.add(base_gas)
        ref = rm.addMemoryReference(_addr(slot_int), tgt_a, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- D. PLATE_COMMENTS ---
    print("--- D. PLATE_COMMENTS (%d) ---" % len(PLATE_COMMENTS))
    for fn_int, plate_text in PLATE_COMMENTS:
        # Verify all chars are ASCII
        for c in plate_text:
            if ord(c) > 127:
                print("[D FAIL] non-ASCII char 0x%x in plate for 0x%08x" % (ord(c), fn_int))
                break
        else:
            if DRY:
                print("[D dry] 0x%08x plate (%d chars)" % (fn_int, len(plate_text)))
                nD += 1; continue
            cu = listing.getCodeUnitAt(_addr(fn_int))
            if cu is None:
                print("[D FAIL] no CodeUnit at 0x%08x" % fn_int); continue
            cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
            print("[D ok] 0x%08x plate (%d chars)" % (fn_int, len(plate_text))); nD += 1

    print("[done] A=%d B=%d D=%d (DRY=%s)" % (nA, nB, nD, DRY))
    print("EQ=%d REF=%d PLATE=%d total_slots=%d (expected 65+27=92)" % (nA, nB, nD, nA+nB))


main()
