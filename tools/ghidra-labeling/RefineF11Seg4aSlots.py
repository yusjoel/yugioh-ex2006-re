# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4aSlots.py -- f11 Seg-4a slot symbolization [0x08087d58..0x08088904)
#
# 21 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ=48 (CID values + scalar constants in pool slots)
#   - 21 NEW CID equates (added to card_info.inc)
#   - REUSEd CID equates (from card_info.inc existing)
#   - PLAYER_BLOCK_STRIDE (0x868) slots
#   - Scalar pool values (zone_query_hand_tag, 1500 threshold, etc.)
# REF=36 (EWRAM pointer pool slots -- createDWordWithRef)
#   - gP1LifePoints x18, gP1SlotSetCodeArray x8, gP1HandSlotArray x5
#   - gP1FieldArrayCBase x2, gP1SlotCountBase x2, gEquipZoneBase_1d98 x1
# FUNC_RENAME=21 (proposed names already applied by disasm script via createFunction)
#   - but we call fn.setName again here to be safe
# PLATE=21 (full ASCII plate comments, all <= 500 chars)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any failed setComment or value mismatch = FAIL.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.address import AddressSet

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, name='?'):
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(_addr(slot_addr)) & 0xFFFFFFFF
        if actual != (expected_val & 0xFFFFFFFF):
            print("FAIL value @0x%08x %s: expected=0x%08x actual=0x%08x" % (
                slot_addr, name, expected_val & 0xFFFFFFFF, actual))
            return False
    except Exception as e:
        print("FAIL read @0x%08x %s: %s" % (slot_addr, name, e))
        return False
    return True


def _apply_eq(slot_addr, value, eq_name, slot_label, eol=None):
    if not _check(slot_addr, value, eq_name):
        return False
    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_val, gas_label, slot_label, eol=None):
    if not _check(slot_addr, target_val, gas_label):
        return False
    if DRY:
        print("[dry] REF 0x%08x  target=0x%08x  gas=%s  label=%s" % (
            slot_addr, target_val, gas_label, slot_label))
        return True
    a = _addr(slot_addr)
    t = _addr(target_val)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    # Create label at target (global) if not present
    tgt_syms = sym_tbl.getSymbols(t)
    if not any(s.getName() == gas_label for s in tgt_syms):
        sym_tbl.createLabel(t, gas_label, SourceType.USER_DEFINED)
    # Create slot label
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    # Add DATA reference from slot -> target
    ref_mgr.addMemoryReference(a, t, RefType.DATA, SourceType.USER_DEFINED, 0)
    # Set primary on new ref
    for ref in ref_mgr.getReferencesFrom(a):
        if ref.getToAddress() == t:
            ref_mgr.setPrimary(ref, True)
            break
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REF] 0x%08x  target=0x%08x  -> %s" % (slot_addr, target_val, slot_label))
    return True


def _apply_plate(fn_addr, plate_text):
    if DRY:
        print("[dry] PLATE 0x%08x  len=%d" % (fn_addr, len(plate_text)))
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLT] 0x%08x OK  len=%d" % (fn_addr, len(plate_text)))
        return True
    except Exception as e:
        print("FAIL PLATE 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


def _func_rename(fn_addr, new_name):
    if DRY:
        print("[dry] FUNC_RENAME 0x%08x -> %s" % (fn_addr, new_name))
        return True
    fn = getFunctionAt(_addr(fn_addr))
    if fn is None:
        print("FAIL FUNC_RENAME 0x%08x: no function (WARN=FAIL)" % fn_addr)
        return False
    try:
        fn.setName(new_name, SourceType.USER_DEFINED)
        print("[REN_FN] 0x%08x -> %s" % (fn_addr, new_name))
        return True
    except Exception as e:
        print("FAIL FUNC_RENAME 0x%08x %s: %s (WARN=FAIL)" % (fn_addr, new_name, e))
        return False


# =============================================================================
# EQ_SLOTS: CID values and scalar constants in pool slots
# Format: (slot_addr, value, eq_name, slot_label, eol_or_None)
# =============================================================================

# --- PLAYER_BLOCK_STRIDE (0x868) slots: 21 occurrences across all functions ---
STRIDE_SLOTS = [
    (0x08087d98, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87d98', None),
    (0x08087e04, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87e04', None),
    (0x08087eac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87eac', None),
    (0x08087f40, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87f40', None),
    (0x08087fb8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_87fb8', None),
    (0x08088048, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88048', None),
    (0x080880bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_880bc', None),
    (0x08088184, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88184', None),
    (0x0808820c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8820c', None),
    (0x08088280, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88280', None),
    (0x080882fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_882fc', None),
    (0x080883cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_883cc', None),
    (0x08088464, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88464', None),
    (0x080884ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_884ec', None),
    (0x0808859c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8859c', None),
    (0x08088644, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88644', None),
    (0x080886f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_886f4', None),
    (0x08088824, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88824', None),
    (0x08088868, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88868', None),
]

# --- CID equate slots ---
CID_SLOTS = [
    # fn05 (0x08087fc0): Magical Hats + CID range compare values 0x1497/0x17ae
    (0x08088050, 0x00001497, 'cid_1497_range_lo',    'cid_range_lo_88050', 'CID range lo for magical_hats scan: 0x1497 (raw; no named equate)'),
    (0x08088054, 0x000017ae, 'cid_1497_range_hi',    'cid_range_hi_88054', 'CID range hi for magical_hats scan: 0x17ae (raw; no named equate)'),

    # fn09 (0x08088214): King's Knight pair CID values in pool
    (0x08088274, 0x000015b6, 'KINGS_KNIGHT_CID',     'cid_kk_88274', None),
    (0x08088278, 0x000015b7, 'cid_15b7_kk_pair',     'cid_kkpair_88278', "King's Knight pair CID 0x15b7 (raw compare val; no named equate)"),

    # fn11 (0x08088304): PLAYER_BLOCK_STRIDE (already in STRIDE_SLOTS is 0x08088358 below excluded)
    # fn11 pools: 0x08088358=0x00000868 (stride), 0x0808835c=gP1FieldArrayCBase (REF)
    (0x08088358, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88358', None),

    # fn18 (0x0808864c): POLYMERIZATION_CID + cid_10e2 pool values
    (0x080886ec, 0x000010e2, 'cid_10e2',             'cid_defusion_e2_886ec', 'cid_10e2=0x10e2 unallocated fusion variant; De-Fusion eligibility check pool'),
    (0x080886f0, 0x000012e5, 'POLYMERIZATION_CID',   'cid_poly_886f0', 'POLYMERIZATION_CID=0x12e5; De-Fusion checks for active Polymerization'),

    # fn21 (0x0808882c): BST CID pool values
    (0x08088870, 0x0000165b, 'CONTRACT_WITH_EXODIA_CID', 'bst_cid_88870', None),
    (0x08088874, 0x00001476, 'ANCIENT_LAMP_CID',     'bst_cid_88874', None),
    (0x08088880, 0x000015d4, 'VAMPIRE_ORCHIS_CID',   'bst_cid_88880', None),
    (0x08088898, 0x000017dd, 'RED_EYES_B_CHICK_CID', 'bst_cid_88898', None),
    (0x080888ac, 0x00001821, 'THE_CREATOR_INCARNATE_CID', 'bst_cid_888ac', None),
    (0x080888b4, 0x00001121, 'cid_1121_la_jinn',      'bst_cid_888b4', 'La Jinn CID=0x1121 exclusion check in special equip BST (no named equate; raw val)'),
    (0x080888bc, 0x000015d1, 'cid_15d1_zombie_tiger', 'bst_cid_888bc', 'Zombie Tiger CID=0x15d1 exclusion check in special equip BST (no named equate; raw val)'),
    (0x080888c4, 0x000015d5, 'DES_DENDLE_CID',       'bst_cid_888c4', 'DES_DENDLE_CID=0x15d5 in special equip BST'),
    (0x080888cc, 0x00001645, 'EXODIA_NECROSS_CID',   'bst_cid_888cc', 'EXODIA_NECROSS_CID=0x1645 in special equip BST'),
    (0x080888d8, 0x00000ff8, 'RED_EYES_B_DRAGON_CID','bst_cid_888d8', 'RED_EYES_B_DRAGON_CID=0x0ff8 in special equip BST'),
    (0x08088900, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID', 'bst_cid_88900', 'BLUE_EYES_WHITE_DRAGON_CID=0x0fa7 in special equip BST'),

    # scalar: 1500 LP threshold (fn03, fn04 duplicate, fn14)
    (0x08087eb4, 0x000005dc, 'CARD_STAT_LP_THRESHOLD_1500', 'lp_thr_87eb4', None),
    (0x080884f4, 0x000005dc, 'CARD_STAT_LP_THRESHOLD_1500', 'lp_thr_884f4', None),

    # scalar: zone_query_hand_tag 0x12a1 (fn03, fn04, fn07, fn15, fn19)
    (0x08087eb8, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_87eb8', None),
    (0x08087fbc, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_87fbc', None),
    (0x08088190, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_88190', None),
    (0x080885a4, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_885a4', None),
    (0x080887ac, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_887ac', None),

    # fn04 raw scalars (no equate): 0xfffffdb0 / 0x00001b38
    # These are raw negative offset / scalar; no named equate available, so createDWord only (no EQ apply)
]

# Note: fn21 BST exclusion CIDs that REUSE existing equates but are not yet in card_info.inc:
# LA_JINN_CID=0x1121, ZOMBIE_TIGER_CID=0x15d1, DES_DENDLE_CID=0x15d5,
# EXODIA_NECROSS_CID=0x1645, RED_EYES_B_DRAGON_CID=0x0ff8, BLUE_EYES_WHITE_DRAGON_CID=0x0fa7
# These are assumed to exist in card_info.inc -- if they don't, the EQ will use raw values with EOL.
# Using raw equate creation as fallback (createEquate works even if not in .inc file).

EQ_SLOTS = STRIDE_SLOTS + CID_SLOTS

# =============================================================================
# REF_SLOTS: EWRAM pointer pool slots (createDWordWithRef)
# Format: (slot_addr, target_val, gas_label, slot_label, eol_or_None)
# =============================================================================

# gP1LifePoints = 0x0201c4e0 (ewram.inc line 79): 18 slots
LP_SLOTS = [
    (0x08087d94, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_87d94', None),
    (0x08087e00, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_87e00', None),
    (0x08087ea8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_87ea8', None),
    (0x08087fb4, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_87fb4', None),
    (0x08088044, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88044', None),
    (0x080880b8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_880b8', None),
    (0x08088180, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88180', None),
    (0x08088208, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88208', None),
    (0x0808827c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8827c', None),
    (0x080882f8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_882f8', None),
    (0x080883c8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_883c8', None),
    (0x08088460, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88460', None),
    (0x080884e8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_884e8', None),
    (0x08088598, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88598', None),
    (0x08088640, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88640', None),
    (0x080886e8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_886e8', None),
    (0x080887a0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_887a0', None),
    (0x08088820, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88820', None),
]

# gP1SlotSetCodeArray = 0x0201c740 (ewram.inc line 332): 8 slots
SCA_SLOTS = [
    (0x08087eb0, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_87eb0', None),
    (0x08087f44, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_87f44', None),
    (0x0808804c, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_8804c', None),
    (0x08088188, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_88188', None),
    (0x08088210, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_88210', None),
    (0x08088300, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_88300', None),
    (0x080885a0, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_885a0', None),
    (0x080887a8, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_887a8', None),
]

# gP1HandSlotArray = 0x0201c8f8 (ewram.inc line 334): 5 slots
HSA_SLOTS = [
    (0x080883d0, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_883d0', None),
    (0x08088468, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_88468', None),
    (0x080884f0, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_884f0', None),
    (0x08088648, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_88648', None),
    (0x08088828, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_88828', None),
]

# gP1FieldArrayCBase = 0x0201c600 (ewram.inc line 366): 2 slots
FAC_SLOTS = [
    (0x0808835c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8835c', None),
    (0x0808886c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8886c', None),
]

# gP1SlotCountBase = 0x0201c4f0 (ewram.inc line 331): 2 slots
SCB_SLOTS = [
    (0x08087f3c, 0x0201c4f0, 'gP1SlotCountBase', 'ptr_scb_87f3c', None),
    (0x08088194, 0x0201c4f0, 'gP1SlotCountBase', 'ptr_scb_88194', None),
]

# gEquipZoneBase_1d98 = 0x0201e278 (ewram.inc NEW): 1 slot
EZB_SLOTS = [
    (0x080885cc, 0x0201e278, 'gEquipZoneBase_1d98', 'ptr_ezb_885cc', None),
]

REF_SLOTS = LP_SLOTS + SCA_SLOTS + HSA_SLOTS + FAC_SLOTS + SCB_SLOTS + EZB_SLOTS

# =============================================================================
# FUNC_RENAME: 21 functions -- rename to proposed names (re-apply for safety)
# =============================================================================
FUNC_RENAMES = [
    (0x08087d58, 'scan_zone_cid_12f4_substate_d'),
    (0x08087d9c, 'scan_zone_soul_release_substate_e'),
    (0x08087e08, 'scan_zone_last_will_substate_d'),
    (0x08087ebc, 'scan_zone_painful_choice_substate_d'),
    (0x08087fc0, 'scan_zone_magical_hats_substate_d'),
    (0x08088058, 'scan_zone_graverobber_substate_e'),
    (0x080880c0, 'scan_zone_summon_from_deck_group_a_substate_d'),
    (0x08088198, 'scan_zone_senju_substate_d'),
    (0x08088214, 'scan_zone_summon_from_deck_group_b_substate_d'),
    (0x08088284, 'scan_zone_sonic_bird_substate_d'),
    (0x08088304, 'scan_zone_dust_tornado_substate_b'),
    (0x08088360, 'scan_zone_graveyard_revival_group_substate_e'),
    (0x080883d4, 'scan_zone_spear_cretin_substate_e'),
    (0x0808846c, 'scan_zone_backup_soldier_substate_e'),
    (0x080884f8, 'scan_zone_serpentine_princess_substate_b'),
    (0x080885a8, 'scan_zone_cid_13ed_substate_b'),
    (0x080885d0, 'scan_zone_return_from_grave_group_substate_e'),
    (0x0808864c, 'scan_zone_de_fusion_substate_e'),
    (0x080886f8, 'scan_zone_insect_imitation_substate_d'),
    (0x080887b0, 'scan_zone_cid_1452_substate_e'),
    (0x0808882c, 'scan_zone_special_category_equip_group_substate_b'),
]

# =============================================================================
# PLATE_OPS: 21 full ASCII plate comments (<= 500 chars each)
# =============================================================================
PLATE_OPS = [
    (0x08087d58,
     "Equip zone scan callback for unallocated CID 0x12f4. r0=player_id. Scans monster zone slots in gP1LifePoints[player*STRIDE+0x10]; calls write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) for each matching slot. Dispatched from equip zone write table 0x09e5a128 entry [21]."),

    (0x08087d9c,
     "Equip zone scan callback for Soul Release (SOUL_RELEASE_CID=0x12f9, pw=05758500). r0=player_id. Scans hand slot zone; calls write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx) twice on matching entries. Dispatched from equip zone write table 0x09e5a128 entry [22]."),

    (0x08087e08,
     "Equip zone scan callback for Last Will (LAST_WILL_CID=0x1315, pw=85602018). r0=player_id. Multi-check: field5, field9>=3, eval_equip_placement_full_check pass, find_effect_node_in_zone condition; then write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table 0x09e5a128 entry [25]."),

    (0x08087ebc,
     "Equip zone scan callback for Painful Choice (PAINFUL_CHOICE_CID=0x132f, pw=74191942). r0=player_id. Two-path scan of monster zone; both paths call write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Inner check uses find_effect_node_in_zone. Dispatched from equip zone write table entry [26]."),

    (0x08087fc0,
     "Equip zone scan callback for Magical Hats (MAGICAL_HATS_CID=0x1362, pw=81210420). r0=player_id. Scans monster zone; check_card_field5_is_nonzero filter + CID range [0x1497..0x17ae] check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [40]."),

    (0x08088058,
     "Equip zone scan callback for Graverobber (GRAVEROBBER_CID=0x1379, pw=61705417). r0=player_id. Scans zone entries; get_card_extended_stat_field6 filter; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from equip zone write table entry [44]. Note: addr 0x08088080 is mid-loop code, not a separate function (degenerate strong entry)."),

    (0x080880c0,
     "Equip zone scan callback for summon-from-deck group A: Giant Rat(0x1333), UFO Turtle(0x1335), Shining Angel(0x133c), Mother Grizzly(0x133e), Flying Kamakiri#1(0x133f), Mystic Tomato(0x1342). r0=player_id. Gate: field5+field8+field9+eval_placement+find_node; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [27,29,33,34,35,37]."),

    (0x08088198,
     "Equip zone scan callback for Senju of the Thousand Hands (SENJU_CID=0x1334, pw=23401839). r0=player_id. Gate: check_card_field5_is_nonzero + check_card_field8_is_normal; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [28]."),

    (0x08088214,
     "Equip zone scan callback for summon-from-deck group B: Giant Germ(0x1339), Nimble Momonga(0x133a), Bubonic Vermin(0x136a), Troop Dragon(0x14dd), King's Knight(0x15b6), Hyena(0x1867), Hydrogeddon(0x194f), Hero Kid(0x19a7). Special King's Knight(0x15b6)/0x15b7 pair check in pool. Dispatched from write table entries [30,31,43,82,115,236,277,291]."),

    (0x08088284,
     "Equip zone scan callback for Sonic Bird (SONIC_BIRD_CID=0x1341, pw=57617178). r0=player_id. Gate: get_card_extended_stat_field6 + field9 check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [36]."),

    (0x08088304,
     "Equip zone scan callback for Dust Tornado (DUST_TORNADO_CID=0x137c, pw=60082869). r0=player_id. Gate: check_card_field5_is_nonzero; additional field-spell checks; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Addr 0x08088354 is epilogue+pool of this function (degenerate strong entry). Dispatched from write table entry [45]."),

    (0x08088360,
     "Equip zone scan callback for graveyard revival group: Shallow Grave(0x1365), Premature Burial(0x1366), Call of Haunted(0x137d), Gilasaurus(0x1488), The Creator(0x1820), Dark Ruler Vandalgyon(0x190a). Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x08088394 is mid-BL degenerate. Dispatched from write table entries [41,42,46,71,225,264]."),

    (0x080883d4,
     "Equip zone scan callback for Spear Cretin (SPEAR_CRETIN_CID=0x133b, pw=58551308). r0=player_id. Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from equip zone write table entry [32]."),

    (0x0808846c,
     "Equip zone scan callback for Backup Soldier (BACKUP_SOLDIER_CID=0x1359, pw=36280194). r0=player_id. Gate: check_card_field5_is_nonzero + field9 check + equip eligible; LP threshold 0x5dc (1500); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from equip zone write table entry [38]."),

    (0x080884f8,
     "Equip zone scan callback for Serpentine Princess (SERPENTINE_PRINCESS_CID=0x13a1, pw=71829750). r0=player_id. Gate: field5 + field7>=3 + eval_equip_placement_full_check + find_effect_node_in_zone; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Addr 0x0808855a is mid-loop degenerate. Dispatched from write table entry [48]."),

    (0x080885a8,
     "Equip zone scan callback for unallocated CID 0x13ed (GAP_CID_13ED). r0=player_id. Simple loop over zone struct at gEquipZoneBase_1d98 (0x0201e278); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from equip zone write table entry [49]."),

    (0x080885d0,
     "Equip zone scan callback for return-from-grave group: Return of the Doomed(0x13f5), cid_1449(unallocated), ICID_RESERVED_D(0x144c), The Forgiving Maiden(0x1457). Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x080885e0 is mid-loop degenerate (weak ref). Dispatched from write table entries [50,53,54,56]."),

    (0x0808864c,
     "Equip zone scan callback for De-Fusion (DE_FUSION_CID=0x13fe, pw=95286165). r0=player_id. Checks for POLYMERIZATION_CID(0x12e5)/cid_10e2(0x10e2) in zone; check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x0808866c is mid-loop degenerate. Dispatched from write table entry [51]."),

    (0x080886f8,
     "Equip zone scan callback for Insect Imitation (INSECT_IMITATION_CID=0x140b, pw=96965364). r0=player_id. Gate: field6 + field7 + eval_equip_placement + find_effect_node; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [52]."),

    (0x080887b0,
     "Equip zone scan callback for ICID_RESERVED_E (0x1452, reserved internal CID; gap between Empress Mantis 0x1453 and Bio-Mage 0x1456). r0=player_id. Gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x080887ec is post-BL degenerate. Dispatched from write table entry [55]."),

    (0x0808882c,
     "Equip zone scan callback for special equip category group B: Ancient Lamp(0x1476), Decayed Commander(0x15d0), Vampire Orchis(0x15d4), Contract with Exodia(0x165b), Don Turtle(0x16fd), Red-Eyes B. Chick(0x17dd), The Creator Incarnate(0x1821), Kaibaman(0x189a). BST of 11 CIDs; check_card_is_equip_target_eligible; write_equip_zone_entry_by_substate(0xb). Dispatched from write table entries [62,118,119,141,169,209,226,249]."),
]


def main():
    print("=== RefineF11Seg4aSlots (DRY=%s) ===" % DRY)
    nEQ = nREF = nREN = nPLT = 0
    fails = []

    # Validate plate lengths pre-run
    for fn_addr, plate_text in PLATE_OPS:
        if len(plate_text) > 500:
            print("FAIL PLATE_LEN 0x%08x: %d chars > 500" % (fn_addr, len(plate_text)))
            fails.append("PLT_LEN 0x%08x" % fn_addr)

    if fails:
        print("ABORT: %d pre-run plate length failures" % len(fails))
        return

    # EQ_SLOTS
    print("--- EQ_SLOTS (%d: %d stride + %d CID/scalar) ---" % (
        len(EQ_SLOTS), len(STRIDE_SLOTS), len(CID_SLOTS)))
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            nEQ += 1
        else:
            fails.append("EQ 0x%08x" % slot_addr)

    # REF_SLOTS
    print("--- REF_SLOTS (%d: %d LP + %d SCA + %d HSA + %d FAC + %d SCB + %d EZB) ---" % (
        len(REF_SLOTS), len(LP_SLOTS), len(SCA_SLOTS), len(HSA_SLOTS),
        len(FAC_SLOTS), len(SCB_SLOTS), len(EZB_SLOTS)))
    for entry in REF_SLOTS:
        slot_addr, target_val, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            nREF += 1
        else:
            fails.append("REF 0x%08x" % slot_addr)

    # FUNC_RENAME
    print("--- FUNC_RENAME (%d functions) ---" % len(FUNC_RENAMES))
    for fn_addr, fn_name in FUNC_RENAMES:
        if _func_rename(fn_addr, fn_name):
            nREN += 1
        else:
            fails.append("REN_FN 0x%08x" % fn_addr)

    # PLATE_OPS
    print("--- PLATE_OPS (%d) ---" % len(PLATE_OPS))
    for fn_addr, plate_text in PLATE_OPS:
        if _apply_plate(fn_addr, plate_text):
            nPLT += 1
        else:
            fails.append("PLT 0x%08x" % fn_addr)

    print("")
    print("=== SUMMARY ===")
    print("EQ=%d/%d  REF=%d/%d  REN_FN=%d/%d  PLT=%d/%d" % (
        nEQ, len(EQ_SLOTS), nREF, len(REF_SLOTS),
        nREN, len(FUNC_RENAMES), nPLT, len(PLATE_OPS)))
    if fails:
        print("FAILURES (%d): %s" % (len(fails), ", ".join(fails)))
    else:
        print("ALL PASS (0 failures)")


main()
