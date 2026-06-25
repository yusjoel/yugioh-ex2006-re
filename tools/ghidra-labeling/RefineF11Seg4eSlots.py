# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4eSlots.py -- f11 Seg-4e slot symbolization [0x0808ad8c..0x0808bb7c)
#
# 25 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ: PLAYER_BLOCK_STRIDE (0x868) slots x25
#     + CID pool values (REUSE or NEW from card_info.inc)
#     + fn21 raw sentinel 0xbc100000 (no named constant)
# REF=46 (EWRAM pointer pool slots -- createDWordWithRef):
#   gP1LifePoints x21, gP1FieldArrayCBase x7, gP1HandSlotArray x6,
#   gP1SlotSetCodeArray x7, gP1ZoneHandCount x2, gP1SlotCountBase x1,
#   gDuelFieldSlots x1, gP1ChainZoneArray x1 = 46 total
# FUNC_RENAME=25 (re-apply proposed names for safety)
# PLATE=25 (full ASCII plate comments, all <= 500 chars)
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
# EQ_SLOTS: PLAYER_BLOCK_STRIDE (0x868) slots -- 25 occurrences
# =============================================================================
STRIDE_SLOTS = [
    (0x0808adc4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8adc4', None),   # fn01
    (0x0808ae44, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ae44', None),   # fn02
    (0x0808ae90, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ae90', None),   # fn03
    (0x0808afe8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8afe8', None),   # fn04
    (0x0808b074, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b074', None),   # fn05
    (0x0808b124, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b124', None),   # fn06
    (0x0808b1a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b1a4', None),   # fn07
    (0x0808b238, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b238', None),   # fn08
    (0x0808b2c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b2c0', None),   # fn09
    (0x0808b348, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b348', None),   # fn10
    (0x0808b3a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b3a4', None),   # fn11
    (0x0808b434, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b434', None),   # fn12
    (0x0808b518, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b518', None),   # fn14
    (0x0808b580, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b580', None),   # fn15
    (0x0808b678, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b678', None),   # fn16
    (0x0808b6dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b6dc', None),   # fn17
    (0x0808b748, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b748', None),   # fn18
    (0x0808b7d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b7d4', None),   # fn19
    (0x0808b86c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b86c', None),   # fn20
    (0x0808b8dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b8dc', None),   # fn21
    (0x0808b93c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b93c', None),   # fn22
    (0x0808b980, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b980', None),   # fn23
    (0x0808b9dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8b9dc', None),   # fn24
    (0x0808bb20, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bb20', None),   # fn25 loop1
    (0x0808bb78, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bb78', None),   # fn25 loop2
]

# =============================================================================
# EQ_SLOTS: CID pool equates
# =============================================================================
CID_SLOTS = [
    # fn01 -- POT_OF_GREED_CID (REUSE, partner comparison)
    (0x0808adcc, 0x000012ec, 'POT_OF_GREED_CID', 'cid_8adcc',
     'POT_OF_GREED_CID=0x12ec (partner for Avatar of The Pot)'),
    # fn04 -- PARASITE_PARACIDE_CID (REUSE, FLIP-check)
    (0x0808aff0, 0x000012a1, 'PARASITE_PARACIDE_CID', 'cid_8aff0',
     'PARASITE_PARACIDE_CID=0x12a1 (find_effect_node FLIP check fn04)'),
    # fn14 -- CARD_FIELD3_THRESHOLD_1500 (REUSE, ATK<=1500 threshold)
    (0x0808b520, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500', 'thresh_8b520',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc (1500) ATK filter fn14'),
    # fn14 -- PARASITE_PARACIDE_CID (REUSE, FLIP-check)
    (0x0808b524, 0x000012a1, 'PARASITE_PARACIDE_CID', 'cid_8b524',
     'PARASITE_PARACIDE_CID=0x12a1 (find_effect_node FLIP check fn14)'),
]

# =============================================================================
# EQ_SLOTS: raw-value sentinels (no named const)
# =============================================================================
RAW_SLOTS = [
    # fn21 -- 0xbc100000 slot sentinel (LSLS #19 compare; hand slot type check)
    (0x0808b8e4, 0xbc100000, 'sentinel_bc100000', 'sentinel_8b8e4',
     'hand slot type sentinel (LSLS #19 compare)'),
]

# =============================================================================
# REF_SLOTS: EWRAM pointer pool slots (createDWordWithRef) -- 46 total
# =============================================================================

# --- gP1LifePoints = 0x0201c4e0 --- 21 slots
REF_P1LP = [
    (0x0808ae40, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8ae40', None),   # fn02
    (0x0808afe4, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8afe4', None),   # fn04
    (0x0808b070, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b070', None),   # fn05
    (0x0808b120, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b120', None),   # fn06
    (0x0808b1a0, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b1a0', None),   # fn07
    (0x0808b234, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b234', None),   # fn08
    (0x0808b2bc, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b2bc', None),   # fn09
    (0x0808b344, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b344', None),   # fn10
    (0x0808b3a0, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b3a0', None),   # fn11
    (0x0808b430, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b430', None),   # fn12
    (0x0808b514, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b514', None),   # fn14
    (0x0808b57c, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b57c', None),   # fn15
    (0x0808b674, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b674', None),   # fn16
    (0x0808b6d8, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b6d8', None),   # fn17
    (0x0808b7d0, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b7d0', None),   # fn19
    (0x0808b868, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b868', None),   # fn20
    (0x0808b8d8, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b8d8', None),   # fn21
    (0x0808b938, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b938', None),   # fn22
    (0x0808b9d8, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8b9d8', None),   # fn24
    (0x0808bb28, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bb28', None),   # fn25 loop1
    (0x0808bb74, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bb74', None),   # fn25 loop2
]

# --- gP1FieldArrayCBase = 0x0201c600 --- 7 slots
REF_P1FAC = [
    (0x0808adc8, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8adc8', None),  # fn01
    (0x0808ae94, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8ae94', None),  # fn03
    (0x0808afec, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8afec', None),  # fn04
    (0x0808b67c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8b67c', None),  # fn16
    (0x0808b74c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8b74c', None),  # fn18
    (0x0808b7d8, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8b7d8', None),  # fn19
    (0x0808b984, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8b984', None),  # fn23
]

# --- gP1HandSlotArray = 0x0201c8f8 --- 6 slots
REF_P1HSA = [
    (0x0808b078, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8b078', None),  # fn05
    (0x0808b128, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8b128', None),  # fn06
    (0x0808b1a8, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8b1a8', None),  # fn07
    (0x0808b23c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8b23c', None),  # fn08
    (0x0808b34c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8b34c', None),  # fn10
    (0x0808b8e0, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8b8e0', None),  # fn21
]

# --- gP1SlotSetCodeArray = 0x0201c740 --- 7 slots
REF_P1SSCA = [
    (0x0808ae48, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8ae48', None),  # fn02
    (0x0808aff8, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8aff8', None),  # fn04
    (0x0808b2c4, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8b2c4', None),  # fn09
    (0x0808b438, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8b438', None),  # fn12
    (0x0808b51c, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8b51c', None),  # fn14
    (0x0808b684, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8b684', None),  # fn16
    (0x0808b870, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8b870', None),  # fn20
]

# --- gP1ZoneHandCount = 0x0201c4ec --- 2 slots
REF_P1ZHC = [
    (0x0808aff4, 0x0201c4ec, 'gP1ZoneHandCount', 'ptr_p1zhc_8aff4', None),  # fn04
    (0x0808b680, 0x0201c4ec, 'gP1ZoneHandCount', 'ptr_p1zhc_8b680', None),  # fn16
]

# --- gP1SlotCountBase = 0x0201c4f0 --- 1 slot
REF_P1SCB = [
    (0x0808b528, 0x0201c4f0, 'gP1SlotCountBase', 'ptr_p1scb_8b528', None),  # fn14
]

# --- gDuelFieldSlots = 0x0201c510 --- 1 slot
REF_DFS = [
    (0x0808bb24, 0x0201c510, 'gDuelFieldSlots', 'ptr_dfs_8bb24', None),  # fn25
]

# --- gP1ChainZoneArray = 0x0201c880 --- 1 slot
REF_P1CZA = [
    (0x0808bb2c, 0x0201c880, 'gP1ChainZoneArray', 'ptr_p1cza_8bb2c', None),  # fn25
]

# =============================================================================
# FUNC_RENAME: 25 functions
# =============================================================================
FUNC_RENAMES = [
    (0x0808ad8c, 'scan_zone_avatar_of_the_pot_substate_b'),
    (0x0808add0, 'scan_zone_monster_gate_substate_d'),
    (0x0808ae4c, 'scan_zone_archlord_zerato_light_group_substate_b'),
    (0x0808ae98, 'scan_zone_ninjitsu_transformation_substate_bd'),
    (0x0808affc, 'scan_zone_beckoning_light_substate_e'),
    (0x0808b07c, 'scan_zone_spirit_of_the_pharaoh_substate_e'),
    (0x0808b12c, 'scan_zone_nubian_guard_substate_e'),
    (0x0808b1ac, 'scan_zone_spirit_caller_substate_e'),
    (0x0808b240, 'scan_zone_emissary_of_the_afterlife_substate_d'),
    (0x0808b2c8, 'scan_zone_night_assailant_substate_e'),
    (0x0808b350, 'scan_zone_soul_reversal_substate_e'),
    (0x0808b3a8, 'scan_zone_human_wave_tactics_substate_d'),
    (0x0808b43c, 'scan_zone_first_sarcophagus_substate_bd'),
    (0x0808b454, 'scan_zone_howling_insect_group_substate_bd'),
    (0x0808b52c, 'scan_zone_dark_factory_mass_prod_substate_e'),
    (0x0808b584, 'scan_zone_abyssal_designator_substate_bd'),
    (0x0808b688, 'scan_zone_graveyard_fourth_dimension_substate_e'),
    (0x0808b6e0, 'scan_zone_two_man_cell_battle_substate_b'),
    (0x0808b750, 'scan_zone_big_wave_small_wave_substate_b'),
    (0x0808b7dc, 'scan_zone_magicians_circle_substate_d'),
    (0x0808b874, 'scan_zone_mokey_mokey_king_substate_e'),
    (0x0808b8e8, 'scan_zone_monster_reincarnation_substate_e'),
    (0x0808b940, 'scan_zone_lighten_the_load_substate_b'),
    (0x0808b988, 'scan_zone_behemoth_king_substate_e'),
    (0x0808b9e0, 'scan_zone_hex_sealed_fusion_group_substate_c'),
]

# =============================================================================
# PLATE: 25 ASCII plate comments
# =============================================================================
PLATES = [
    (0x0808ad8c,
     'Equip zone scan for Avatar of The Pot (AVATAR_OF_THE_POT_CID=0x1748, pw=99284890). Field spell zone via gP1FieldArrayCBase; gate: check_card_pair_allowed (partner=POT_OF_GREED_CID=0x12ec); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [180].'),
    (0x0808add0,
     'Equip zone scan for Monster Gate (MONSTER_GATE_CID=0x175c, pw=43040603). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + check_card_has_equip_placement_type; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [183].'),
    (0x0808ae4c,
     'Equip zone scan for Archlord Zerato/Light of Judgment group: Archlord Zerato (ARCHLORD_ZERATO_CID=0x1758, pw=18378582), Light of Judgment (CID=0x1764, pw=44595286). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entries [182,184].'),
    (0x0808ae98,
     'Equip zone scan for Ninjitsu Art of Transformation (NINJITSU_ART_OF_TRANSFORMATION_CID=0x1768, pw=70861343). Two-loop via gP1FieldArrayCBase (field, +0xc) + gP1SlotSetCodeArray (monster zone); gate: get_card_extended_stat_field6 race (0xa/0xb/0x10) + eval_equip_bonus_for_slot + eval_equip_placement + find_effect_node(PARASITE_PARACIDE_CID=0x12a1); write substate_b (loop1) + substate_d (loop2). Dispatch entry [185].'),
    (0x0808affc,
     'Equip zone scan for Beckoning Light (CID=0x1769, pw=16255442). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [186].'),
    (0x0808b07c,
     'Equip zone scan for Spirit of the Pharaoh (SPIRIT_OF_PHARAOH_CID=0x1788, pw=25343280). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + get_card_extended_stat_field6 x2 + get_card_extended_stat_field5 + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [187].'),
    (0x0808b12c,
     'Equip zone scan for Nubian Guard (NUBIAN_GUARD_CID=0x178c, pw=51616747). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: get_card_extended_stat_field6 + get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [189].'),
    (0x0808b1ac,
     'Equip zone scan for Spirit Caller (CID=0x1795, pw=48659020). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + get_card_extended_stat_field5 + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [190].'),
    (0x0808b240,
     'Equip zone scan for Emissary of the Afterlife (EMISSARY_OF_THE_AFTERLIFE_CID=0x1796, pw=75043725). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + get_card_extended_stat_field5; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [191].'),
    (0x0808b2c8,
     'Equip zone scan for Night Assailant (NIGHT_ASSAILANT_CID=0x179a, pw=16226786). Hand zone via gP1LifePoints+gP1HandSlotArray; gate: get_card_field_summon_restriction; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [192].'),
    (0x0808b350,
     'Equip zone scan for Soul Reversal (CID=0x17a2, pw=78864369). Monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: get_card_field_summon_restriction; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [193].'),
    (0x0808b3a8,
     'Equip zone scan for Human-Wave Tactics (HUMAN_WAVE_TACTICS_CID=0x17b2, pw=30353551). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field5 level + map_field8_to_card_type_category + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [195]. Addr 0x0808b40e is degenerate.'),
    (0x0808b43c,
     'Equip zone scan dispatcher for The First Sarcophagus (THE_FIRST_SARCOPHAGUS_CID=0x17af, pw=31076103). Calls scan_zone_destiny_board_substate_bd if r2!=0, else write_equip_zone_entries_by_lv_card_id. Dispatch table entry [194].'),
    (0x0808b454,
     'Equip zone scan for Howling Insect/Masked Dragon/UFOroid group: Howling Insect (CID=0x17e5, pw=93107608), Masked Dragon (MASKED_DRAGON_CID=0x17e6, pw=39191307), UFOroid (UFOROID_CID=0x18f4, pw=07602840). Monster zone via gP1LifePoints+SlotSetCodeArray; gates: field5_nonzero + field3_raw<=ATK1500 + field6 x2 + eval_placement + find_effect_node(PARASITE_PARACIDE_CID); write substate_b+d. Dispatch entries [210,211,258].'),
    (0x0808b52c,
     'Equip zone scan for Dark Factory of Mass Production (DARK_FACTORY_MASS_PROD_CID=0x17f1, pw=90928333). Monster zone via gP1LifePoints+STRIDE; gate: map_field8_to_card_type_category; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [212].'),
    (0x0808b584,
     'Equip zone scan for Abyssal Designator (ABYSSAL_DESIGNATOR_CID=0x17f4, pw=89801755). Two-loop: loop1 via gP1FieldArrayCBase (field zone, +0xc), gate field6+field7, write substate_b; loop2 via gP1SlotSetCodeArray (monster zone, +0x10), same gates, write substate_d. Dispatch table entry [213].'),
    (0x0808b688,
     'Equip zone scan for The Graveyard in the Fourth Dimension (GRAVEYARD_IN_FOURTH_DIMENSION_CID=0x17f7, pw=88089103). Monster zone via gP1LifePoints+STRIDE; gate: check_card_id_is_effect_monster_type_b; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [215].'),
    (0x0808b6e0,
     'Equip zone scan for Two-Man Cell Battle (CID=0x17f8, pw=25578802). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [216].'),
    (0x0808b750,
     'Equip zone scan for Big Wave Small Wave (BIG_WAVE_SMALL_WAVE_CID=0x17f9, pw=51562916). Field spell zone via gP1LifePoints+gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(3) (WATER attr) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entry [217].'),
    (0x0808b7dc,
     'Equip zone scan for Magicians Circle (MAGICIANS_CIRCLE_CID=0x1818, pw=00050755). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field3_raw>=(0xfa<<3)=0x7d0 (ATK>=2000) + get_card_extended_stat_field6 (race) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [224].'),
    (0x0808b874,
     'Equip zone scan for Mokey Mokey King (MOKEY_MOKEY_KING_CID=0x183d, pw=13803864). Hand zone via gP1LifePoints+gP1HandSlotArray; gate: LSLS slot_word,#19 == 0xbc100000 sentinel + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [229].'),
    (0x0808b8e8,
     'Equip zone scan for Monster Reincarnation (CID=0x1845, pw=74848038). Monster zone via gP1LifePoints+STRIDE; gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [230].'),
    (0x0808b940,
     'Equip zone scan for Lighten the Load (CID=0x1847, pw=37231841). Field spell zone via gP1FieldArrayCBase+STRIDE; gate: eval_equip_bonus_for_slot; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [231]. Addr 0x0808b95a is degenerate.'),
    (0x0808b988,
     'Equip zone scan for Behemoth the King of All Animals (BEHEMOTH_KING_CID=0x1864, pw=22996376). Monster zone via gP1LifePoints+STRIDE; gate: get_card_extended_stat_field6 (race); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [235].'),
    (0x0808b9e0,
     'Equip zone scan for Hex-Sealed Fusion group: Light (CID=0x1870, pw=15717011), Dark (CID=0x1871, pw=52101615), Earth (CID=0x1872, pw=88696724). Chain zone via gP1ChainZoneArray+gDuelFieldSlots; gates: check_slot_card_can_be_equipped + check_card_is_equip_target_eligible + check_card_id_is_equip_excluded_range + equip_display_criteria + check_slot_equip_criteria_by_state; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatch entries [237,238,239].'),
]


def main():
    fail_count = 0
    ok_count = 0

    # --- Step 1: PLAYER_BLOCK_STRIDE EQ slots ---
    print("=== STRIDE EQ (%d slots) ===" % len(STRIDE_SLOTS))
    for args in STRIDE_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 2: CID EQ slots ---
    print("=== CID EQ (%d slots) ===" % len(CID_SLOTS))
    for args in CID_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 3: Raw sentinel EQ slots ---
    print("=== RAW EQ (%d slots) ===" % len(RAW_SLOTS))
    for args in RAW_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 4: REF slots (EWRAM pointers) ---
    all_refs = REF_P1LP + REF_P1FAC + REF_P1HSA + REF_P1SSCA + REF_P1ZHC + REF_P1SCB + REF_DFS + REF_P1CZA
    print("=== REF (%d slots) ===" % len(all_refs))
    for args in all_refs:
        if _apply_ref(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 5: FUNC_RENAME ---
    print("=== FUNC_RENAME (%d fns) ===" % len(FUNC_RENAMES))
    for fn_addr, fn_name in FUNC_RENAMES:
        if _func_rename(fn_addr, fn_name):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 6: PLATE ---
    print("=== PLATE (%d fns) ===" % len(PLATES))
    for fn_addr, plate_text in PLATES:
        if _apply_plate(fn_addr, plate_text):
            ok_count += 1
        else:
            fail_count += 1

    print("")
    print("=== RefineF11Seg4eSlots DONE ===")
    print("  ok=%d  fail=%d" % (ok_count, fail_count))
    print("  EQ(STRIDE)=%d  EQ(CID)=%d  EQ(RAW)=%d  REF=%d  FUNC_RENAME=%d  PLATE=%d" % (
        len(STRIDE_SLOTS), len(CID_SLOTS), len(RAW_SLOTS), len(all_refs),
        len(FUNC_RENAMES), len(PLATES)))
    if fail_count > 0:
        print("  WARN: %d FAIL(s) -- review output above" % fail_count)
    else:
        print("  ALL PASS")


main()
