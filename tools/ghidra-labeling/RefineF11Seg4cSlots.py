# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4cSlots.py -- f11 Seg-4c slot symbolization [0x0808962c..0x0808a2ac)
#
# 23 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ: PLAYER_BLOCK_STRIDE (0x868) slots x23 + CID pool values (REUSE or NEW from card_info.inc)
#   + scalar equates (zone_query_hand_tag_12a1, CARD_FIELD3_THRESHOLD_1500)
#   + fn21 partner CID pool slots (raw labels, some REUSE)
# REF=36 (EWRAM pointer pool slots -- createDWordWithRef):
#   gP1LifePoints x19, gP1SlotSetCodeArray x5, gP1HandSlotArray x5,
#   gP1FieldArrayCBase x5, gP1ChainZoneArray x2
# FUNC_RENAME=23 (re-apply proposed names for safety)
# PLATE=23 (full ASCII plate comments, all <= 500 chars)
#
# Corrections from review applied:
#   fn21 plate: corrected from 574->472 chars (reviewer-supplied replacement)
#   fn08 createFunction addr: 0x08089990 (not 0x08089928)
#   fn03 plate pw: 04861205 (not 04291579)
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
# EQ_SLOTS: PLAYER_BLOCK_STRIDE (0x868) slots -- 23 occurrences
# =============================================================================
STRIDE_SLOTS = [
    (0x08089680, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89680', None),
    (0x080896f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_896f4', None),
    (0x0808975c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8975c', None),
    (0x08089808, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89808', None),
    (0x08089890, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89890', None),
    (0x08089920, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89920', None),
    (0x08089988, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89988', None),
    (0x080899e0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_899e0', None),
    (0x08089a94, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89a94', None),
    (0x08089b50, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89b50', None),
    (0x08089bb4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89bb4', None),
    (0x08089c1c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89c1c', None),
    (0x08089c78, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89c78', None),
    (0x08089d00, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89d00', None),
    (0x08089d8c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89d8c', None),
    (0x08089e38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89e38', None),
    (0x08089ec8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89ec8', None),
    (0x08089f2c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89f2c', None),
    (0x08089fb0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89fb0', None),
    (0x0808a008, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a008', None),
    (0x0808a188, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a188', None),
    (0x0808a21c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a21c', None),
    (0x0808a2a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a2a4', None),
]

# =============================================================================
# EQ_SLOTS: CID pool values
# =============================================================================
# NEW CIDs (not yet in card_info.inc; added by adding to card_info.inc before running)
# REUSE CIDs (already in card_info.inc)
CID_SLOTS = [
    # fn04 -- TOON_TABLE_OF_CONTENTS_CID NEW
    # (pool only has gP1LifePoints + stride; CID is only in dispatch table, no explicit pool slot)
    # fn09 -- MACHINE_DUPLICATION_CID NEW (no explicit CID pool slot in fn09)
    # fn09 -- LEAGUE_UNIFORM_NOMENCLATURE_CID NEW (no explicit CID pool slot)
    # fn10 -- GRAVEKEEPER_SPY_CID NEW (no explicit CID pool slot)
    # fn10 -- CARD_FIELD3_THRESHOLD_1500 REUSE (at 0x08089b58)
    (0x08089b58, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500', 'thresh_89b58',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc (1500 ATK threshold)'),
    # fn09/fn10/fn12/fn16 -- zone_query_hand_tag_12a1 REUSE (4 slots; fn22 has no zone_query pool slot)
    (0x08089a9c, 0x000012a1, 'zone_query_hand_tag_12a1', 'zq_89a9c',
     'zone_query_hand_tag_12a1=0x12a1'),
    (0x08089b5c, 0x000012a1, 'zone_query_hand_tag_12a1', 'zq_89b5c',
     'zone_query_hand_tag_12a1=0x12a1'),
    (0x08089c20, 0x000012a1, 'zone_query_hand_tag_12a1', 'zq_89c20',
     'zone_query_hand_tag_12a1=0x12a1'),
    (0x08089e40, 0x000012a1, 'zone_query_hand_tag_12a1', 'zq_89e40',
     'zone_query_hand_tag_12a1=0x12a1'),
    # fn21 CID dispatch pool -- REUSE entries
    (0x0808a030, 0x0000167d, 'KNIGHTS_TITLE_CID', 'cid_8a030',
     'KNIGHTS_TITLE_CID=0x167d (Knights Title)'),
    (0x0808a048, 0x0000195c, 'BONDING_H2O_CID', 'cid_8a048',
     'BONDING_H2O_CID=0x195c (Bonding - H2O)'),
    (0x0808a04c, 0x00001713, 'DEDICATION_THROUGH_LIGHT_DARK_CID', 'cid_8a04c',
     'DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713'),
    (0x0808a058, 0x000019b1, 'PHOTON_GENERATOR_UNIT_CID', 'cid_8a058',
     'PHOTON_GENERATOR_UNIT_CID=0x19b1'),
    (0x0808a064, 0x00001377, 'BUSTER_BLADER_CID', 'cid_8a064',
     'BUSTER_BLADER_CID=0x1377 (Buster Blader partner check)'),
    (0x0808a06c, 0x00000fc9, 'DARK_MAGICIAN_CID_0FC9', 'cid_8a06c',
     'DARK_MAGICIAN_CID_0FC9=0x0fc9 (Dark Magician alt CID)'),
    # fn21 0x0808a078 = 0x167c = Dark Magician Knight (partner-only, raw label)
    (0x0808a080, 0x000016f8, 'DARK_MAGICIAN_OF_CHAOS_CID', 'cid_8a080',
     'DARK_MAGICIAN_OF_CHAOS_CID=0x16f8 (DM-of-Chaos partner)'),
    (0x0808a08c, 0x00001951, 'WATER_DRAGON_CID', 'cid_8a08c',
     'WATER_DRAGON_CID=0x1951 (Water Dragon partner)'),
    (0x0808a180, 0x000019a9, 'CYBER_LASER_DRAGON_CID', 'cid_8a180',
     'CYBER_LASER_DRAGON_CID=0x19a9 (Cyber Laser Dragon partner)'),
    (0x0808a18c, 0x0000159d, 'NECROVALLEY_CID', 'cid_8a18c',
     'NECROVALLEY_CID=0x159d (Necrovalley CID)'),
]

# fn21 0x0808a078 = 0x167c raw partner CID (Dark Magician Knight, no .equ)
RAW_CID_LABEL_SLOTS = [
    (0x0808a078, 0x0000167c, 'cid_167c_dark_magician_knight',
     'CID=0x167c (Dark Magician Knight; partner-only compare, not dispatched)'),
]

# =============================================================================
# REF_SLOTS: createDWordWithRef for EWRAM pointer pool slots (REF=36)
# =============================================================================
# gP1LifePoints = 0x0201c4e0 (ewram.inc) -- 19 slots
REF_LP_SLOTS = [
    (0x0808967c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8967c', None),
    (0x080896f0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_896f0', None),
    (0x08089758, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89758', None),
    (0x08089804, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89804', None),
    (0x0808988c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8988c', None),
    (0x0808991c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8991c', None),
    (0x08089a90, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89a90', None),
    (0x08089b4c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89b4c', None),
    (0x08089bb0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89bb0', None),
    (0x08089c18, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89c18', None),
    (0x08089c74, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89c74', None),
    (0x08089cfc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89cfc', None),
    (0x08089d88, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89d88', None),
    (0x08089e34, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89e34', None),
    (0x08089ec4, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89ec4', None),
    (0x08089fac, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89fac', None),
    (0x0808a184, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a184', None),
    (0x0808a218, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a218', None),
    (0x0808a2a0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a2a0', None),
]

# gP1SlotSetCodeArray = 0x0201c740 (ewram.inc) -- 5 slots
REF_SCA_SLOTS = [
    (0x08089a98, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89a98', None),
    (0x08089b54, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89b54', None),
    (0x08089e3c, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89e3c', None),
    (0x08089ecc, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89ecc', None),
    (0x0808a220, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_8a220', None),
]

# gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 5 slots
REF_HSA_SLOTS = [
    (0x080896f8, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_896f8', None),
    (0x08089894, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_89894', None),
    (0x08089924, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_89924', None),
    (0x08089d90, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_89d90', None),
    (0x08089fb4, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_89fb4', None),
]

# gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 5 slots
REF_FAC_SLOTS = [
    (0x080897b0, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_897b0', None),
    (0x0808998c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8998c', None),
    (0x080899e4, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_899e4', None),
    (0x08089f30, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_89f30', None),
    (0x0808a00c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8a00c', None),
]

# gP1ChainZoneArray = 0x0201c880 (ewram.inc) -- 2 slots
REF_CZA_SLOTS = [
    (0x08089d04, 0x0201c880, 'gP1ChainZoneArray', 'ptr_cza_89d04', None),
    (0x0808a2a8, 0x0201c880, 'gP1ChainZoneArray', 'ptr_cza_8a2a8', None),
]

# NOTE: fn22 pool = 0x0808a218(gP1LifePoints), 0x0808a21c(STRIDE), 0x0808a220(gP1SlotSetCodeArray=0x0201c740).
# fn22 uses zone_query_hand_tag_12a1 but NOT as a literal pool constant (no slot in fn22 pool).
# 0x0808a220 holds 0x0201c740 (EWRAM ptr) -- handled in REF_SCA_SLOTS only.

# =============================================================================
# FUNCTION RENAMES + PLATES (23 functions)
# All plate text verified ASCII only, all len <= 500 chars
# fn21 plate: reviewer-supplied corrected version (472 chars, within limit)
# fn08 addr: 0x08089990 (corrected from proposal header typo 0x08089928)
# fn03 pw: 04861205 (corrected from proposal 04291579)
# =============================================================================
FUNC_RENAMES_AND_PLATES = [
    (0x0808962c, 'scan_zone_dark_scorpion_burglars_group_substate_d',
     'Equip zone scan callback for Dark Scorpion group: De-Spell Germ Weapon (DE_SPELL_GERM_WEAPON_CID=0x14ee, pw=14571844), Dark Scorpion Burglars (DARK_SCORPION_BURGLARS_CID=0x1531, pw=86148577). r0=player_id. Gate: get_card_extended_stat_field6==0x16 (RACE_SPELL); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [85,97].'),
    (0x08089684, 'scan_zone_book_of_life_substate_e',
     'Equip zone scan callback for Book of Life (BOOK_OF_LIFE_CID=0x1536, pw=02204140). r0=player_id. Two loops: (1) gP1LifePoints+STRIDE monster zone at+0x14 -- field6 + equip_eligible gate; (2) gP1HandSlotArray -- field5 + equip_eligible gate. Both write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [99].'),
    (0x08089760, 'scan_zone_call_of_the_mummy_substate_b',
     'Equip zone scan callback for Call of the Mummy (CALL_OF_THE_MUMMY_CID=0x153b, pw=04861205). r0=player_id. Gate: check_card_has_equip_placement_type + check_card_is_equip_target_eligible + get_card_extended_stat_field6 via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [100].'),
    (0x080897b4, 'scan_zone_toon_table_of_contents_substate_d',
     'Equip zone scan callback for Toon Table of Contents (CID=0x1562, pw=89997728). r0=player_id. Gate: check_card_is_toon_type; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) via gP1LifePoints monster zone scan. Dispatched from write table entry [101].'),
    (0x0808980c, 'scan_zone_fushioh_richie_puppet_master_group_substate_e',
     'Equip zone scan callback for Fushioh Richie/Puppet Master group: Fushioh Richie (FUSHIOH_RICHIE_CID=0x1534, pw=38285847), Puppet Master (PUPPET_MASTER_CID=0x156a, pw=40933827). Gate: get_card_extended_stat_field6 + check_zone_slot_equip_eligible via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x0808985e is degenerate BL mid-loop. Dispatched from write table entries [98,102].'),
    (0x08089898, 'scan_zone_lord_poison_substate_e',
     'Equip zone scan callback for Lord Poison (LORD_POISON_CID=0x156d, pw=02598051). r0=player_id. Gate: get_card_extended_stat_field6 + check_zone_slot_equip_eligible via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [103].'),
    (0x08089928, 'scan_zone_hidden_soldier_substate_b',
     'Equip zone scan callback for Hidden Soldier (HIDDEN_SOLDIER_CID=0x1572, pw=02348149). r0=player_id. Gate: check_card_stat_field7_equals + eval_equip_bonus_for_slot + eval_equip_placement_full_check via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [104].'),
    (0x08089990, 'scan_zone_monster_relief_familiar_knight_group_substate_b',
     'Equip zone scan callback for Monster Relief/Familiar Knight group: Monster Relief (MONSTER_RELIEF_CID=0x1579, pw=72089094), Familiar Knight (FAMILIAR_KNIGHT_CID=0x17c3, pw=00423705). Gate: eval_equip_bonus_for_slot + eval_equip_placement_full_check via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entries [105,198].'),
    (0x080899e8, 'scan_zone_machine_duplication_group_substate_d',
     'Equip zone scan callback for Machine Duplication group: Machine Duplication (CID=0x157a, pw=63995093), League of Uniform Nomenclature (CID=0x1978, pw=55008284). Gate: check_card_field5_is_nonzero + eval_equip_placement + find_effect_node_in_zone + check_card_pair_allowed via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x08089a58 is degenerate fall-through. Dispatched from write table entries [106,285].'),
    (0x08089aa0, 'scan_zone_gravekeeper_spy_substate_d',
     'Equip zone scan callback for Gravekeeper\'s Spy (CID=0x1585, pw=24317029). r0=player_id. Multi-gate: check_card_field5_is_nonzero + get_card_extended_stat_field3_raw<=CARD_FIELD3_THRESHOLD_1500(0x5dc) + find_effect_node_in_zone + eval_equip_placement + check_card_is_gravekeeper via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [107].'),
    (0x08089b60, 'scan_zone_a_cat_of_ill_omen_substate_d',
     'Equip zone scan callback for A Cat of Ill Omen (A_CAT_OF_ILL_OMEN_CID=0x1590, pw=00808676). r0=player_id. Gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) via gP1LifePoints monster zone scan. Dispatched from write table entry [108].'),
    (0x08089bb8, 'scan_zone_different_dimension_capsule_substate_d',
     'Equip zone scan callback for Different Dimension Capsule (DIFFERENT_DIMENSION_CAPSULE_CID=0x159c, pw=68468459). r0=player_id. Gate: find_effect_node_in_zone via gP1LifePoints[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [110].'),
    (0x08089c24, 'scan_zone_owl_of_luck_terraforming_group_substate_d',
     'Equip zone scan callback for Owl of Luck/Terraforming group: An Owl of Luck (CID=0x1593, pw=23927567), Terraforming (CID=0x15a1, pw=73628505). Gate: get_card_extended_stat_field9 via gP1LifePoints monster zone; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [109,111].'),
    (0x08089c7c, 'scan_zone_metamorphosis_substate_c',
     'Equip zone scan callback for Metamorphosis (METAMORPHOSIS_CID=0x15a3, pw=46411259). r0=player_id. Gate: check_card_is_equip_target_eligible + check_card_id_is_equip_excluded_range + get_card_extended_stat_field7 via gP1ChainZoneArray; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatched from write table entry [112].'),
    (0x08089d08, 'scan_zone_rite_of_spirit_substate_e',
     'Equip zone scan callback for Rite of Spirit (RITE_OF_SPIRIT_CID=0x15ac, pw=30450531). r0=player_id. Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible + check_card_is_gravekeeper via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [113].'),
    (0x08089d94, 'scan_zone_rope_of_spirit_substate_d',
     'Equip zone scan callback for Rope of Spirit (ROPE_OF_SPIRIT_CID=0x15b5, pw=47025825). r0=player_id. Gate: check_card_field5_is_nonzero + find_effect_node_in_zone + eval_equip_placement + get_card_extended_stat_field7 via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [114].'),
    (0x08089e44, 'scan_zone_goblin_zombie_substate_d',
     'Equip zone scan callback for Goblin Zombie (CID=0x15b9, pw=63665875). r0=player_id. Gate: check_card_field5_is_nonzero + get_card_extended_stat_field6 + get_card_extended_stat_field4_raw via gP1SlotSetCodeArray; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x08089e78 is degenerate mid-loop bitfield pair. Dispatched from write table entry [116].'),
    (0x08089ed0, 'scan_zone_frontline_base_substate_b',
     'Equip zone scan callback for Frontline Base (CID=0x15e2, pw=46181000). r0=player_id. Gate: eval_equip_bonus_for_slot + eval_equip_placement_full_check + check_card_stat_field8_is_8 (Union type) via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [122].'),
    (0x08089f34, 'scan_zone_autonomous_action_unit_substate_e',
     'Equip zone scan callback for Autonomous Action Unit (AUTONOMOUS_ACTION_UNIT_CID=0x15e6, pw=80256062). r0=player_id. Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [123].'),
    (0x08089fb8, 'scan_zone_tribute_doll_substate_b',
     'Equip zone scan callback for Tribute Doll (CID=0x15ed, pw=02903036). r0=player_id. Gate: eval_equip_bonus_for_slot + eval_equip_placement_full_check via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [124].'),
    # fn21: reviewer-corrected plate (472 chars, was 574 -- removed pw/=0xCID redundancy)
    (0x0808a010, 'scan_zone_magic_evolution_group_substate_deb',
     "Equip zone scan cb: magic evolution group (6 CIDs): Skilled White(SKILLED_WHITE_MAGICIAN_CID), Skilled Dark(SKILLED_DARK_MAGICIAN_CID), Knight's Title(KNIGHTS_TITLE_CID=0x167d), Dedication/Light+Dark(DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713), Bonding-H2O(CID=0x195c), Photon Generator(PHOTON_GENERATOR_UNIT_CID). Partner CID load: DM-Knight=0x167c/DM-of-Chaos=0x16f8/Water-Dragon=0x1951/Cyber-Laser=0x19a9. 3 loops: substate d/e/b. Table entries [125,126,145,172,279,294]."),
    (0x0808a190, 'scan_zone_apprentice_magician_substate_d',
     'Equip zone scan callback for Apprentice Magician (CID=0x1612, pw=09156135). r0=player_id. Gate: check_card_field5_is_nonzero + eval_equip_placement_full_check + get_card_extended_stat_field6 + get_card_extended_stat_field7 via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [127].'),
    (0x0808a224, 'scan_zone_magical_scientist_substate_c',
     "Equip zone scan callback for Magical Scientist (MAGICAL_SCIENTIST_CID=0x1619, pw=34206604). r0=player_id. Gate: check_card_is_equip_target_eligible + check_card_id_is_equip_excluded_range + get_card_extended_stat_field7 via gP1ChainZoneArray; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Addr 0x0808a28e is degenerate mid-loop bcc backward. Dispatched from write table entry [128]."),
]


def _verify_plate_lengths():
    ok = True
    for addr, name, plate in FUNC_RENAMES_AND_PLATES:
        if len(plate) > 500:
            print("FAIL plate len 0x%08x %s: %d chars (>500)" % (addr, name, len(plate)))
            ok = False
        non_ascii = [c for c in plate if ord(c) >= 128]
        if non_ascii:
            print("FAIL plate non-ASCII 0x%08x: %s" % (addr, non_ascii))
            ok = False
    if ok:
        max_len = max(len(p) for _, _, p in FUNC_RENAMES_AND_PLATES)
        print("[verify] All %d plates OK, max_len=%d" % (len(FUNC_RENAMES_AND_PLATES), max_len))
    return ok


def main():
    # Pre-flight: verify all plate lengths and ASCII
    if not _verify_plate_lengths():
        print("ABORT: plate verification failed")
        return

    if DRY:
        print("DRY RUN -- RefineF11Seg4cSlots:")
        print("  STRIDE_SLOTS: %d" % len(STRIDE_SLOTS))
        print("  CID_SLOTS: %d" % len(CID_SLOTS))
        print("  RAW_CID_LABEL_SLOTS: %d" % len(RAW_CID_LABEL_SLOTS))
        ref_total = (len(REF_LP_SLOTS) + len(REF_SCA_SLOTS) + len(REF_HSA_SLOTS) +
                     len(REF_FAC_SLOTS) + len(REF_CZA_SLOTS))
        print("  REF_SLOTS: %d (LP=%d + SCA=%d + HSA=%d + FAC=%d + CZA=%d)" % (
            ref_total, len(REF_LP_SLOTS), len(REF_SCA_SLOTS), len(REF_HSA_SLOTS),
            len(REF_FAC_SLOTS), len(REF_CZA_SLOTS)))
        print("  FUNC_RENAME+PLATE: %d" % len(FUNC_RENAMES_AND_PLATES))
        for addr, name, plate in FUNC_RENAMES_AND_PLATES:
            print("  [dry] FUNC_RENAME 0x%08x -> %s  plate_len=%d" % (addr, name, len(plate)))
        return

    print("=== RefineF11Seg4cSlots [0x0808962c..0x0808a2ac) ===")
    fail_count = 0

    # --- STRIDE equates ---
    print("--- STRIDE_SLOTS (%d) ---" % len(STRIDE_SLOTS))
    for slot_addr, val, eq_name, label, eol in STRIDE_SLOTS:
        if not _apply_eq(slot_addr, val, eq_name, label, eol):
            fail_count += 1

    # --- CID equates ---
    print("--- CID_SLOTS (%d) ---" % len(CID_SLOTS))
    for slot_addr, val, eq_name, label, eol in CID_SLOTS:
        if not _apply_eq(slot_addr, val, eq_name, label, eol):
            fail_count += 1

    # --- Raw CID labels (no equate, just label+EOL) ---
    print("--- RAW_CID_LABEL_SLOTS (%d) ---" % len(RAW_CID_LABEL_SLOTS))
    for slot_addr, expected_val, label, eol in RAW_CID_LABEL_SLOTS:
        if not _check(slot_addr, expected_val, label):
            fail_count += 1
            continue
        a = _addr(slot_addr)
        sym_tbl = currentProgram.getSymbolTable()
        names = [s.getName() for s in sym_tbl.getSymbols(a)]
        if label not in names:
            try:
                sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
            except Exception as e:
                print("FAIL raw label 0x%08x %s: %s" % (slot_addr, label, e))
                fail_count += 1
                continue
        for s in sym_tbl.getSymbols(a):
            if s.getName() == label:
                s.setPrimary()
                break
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None and eol:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[RAW] 0x%08x  -> %s" % (slot_addr, label))

    # --- REF slots (gP1LifePoints) ---
    print("--- REF_LP_SLOTS (%d) ---" % len(REF_LP_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_LP_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1SlotSetCodeArray) ---
    print("--- REF_SCA_SLOTS (%d) ---" % len(REF_SCA_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_SCA_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1HandSlotArray) ---
    print("--- REF_HSA_SLOTS (%d) ---" % len(REF_HSA_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_HSA_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1FieldArrayCBase) ---
    print("--- REF_FAC_SLOTS (%d) ---" % len(REF_FAC_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_FAC_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1ChainZoneArray) ---
    print("--- REF_CZA_SLOTS (%d) ---" % len(REF_CZA_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_CZA_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- FUNC_RENAME + PLATE ---
    print("--- FUNC_RENAME + PLATE (%d) ---" % len(FUNC_RENAMES_AND_PLATES))
    for fn_addr, fn_name, plate_text in FUNC_RENAMES_AND_PLATES:
        if not _func_rename(fn_addr, fn_name):
            fail_count += 1
        if not _apply_plate(fn_addr, plate_text):
            fail_count += 1

    print("")
    ref_total = (len(REF_LP_SLOTS) + len(REF_SCA_SLOTS) + len(REF_HSA_SLOTS) +
                 len(REF_FAC_SLOTS) + len(REF_CZA_SLOTS))
    print("=== RefineF11Seg4cSlots DONE ===")
    print("  STRIDE=%d  CID=%d  RAW=%d  REF=%d  RENAME+PLATE=%d  FAIL=%d" % (
        len(STRIDE_SLOTS), len(CID_SLOTS), len(RAW_CID_LABEL_SLOTS),
        ref_total, len(FUNC_RENAMES_AND_PLATES), fail_count))
    if fail_count > 0:
        print("  *** %d FAIL(s) detected -- check output above ***" % fail_count)
    else:
        print("  All operations PASS")


main()
