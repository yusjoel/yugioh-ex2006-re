# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4fSlots.py -- f11 Seg-4f slot symbolization [0x0808bb7c..0x0808cabc)
#
# 25 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ: PLAYER_BLOCK_STRIDE (0x868) slots x26 (incl fn17+fn18 pool stride)
#     + EQUIP_ACTIVE_CTX_OFF (0x484) x4 (fn06, fn07+fn08, fn10, fn24)
#     + CARD_FIELD3_THRESHOLD_1500 (0x5dc) x1 (fn26)
#     + CID pool values (REUSE or NEW from card_info.inc) x20
#     + slot_field_mask_ffff803f (REUSE card_info.inc:1765) x1 (fn25)
#     + VAMPIRE_GENESIS_GDUELPF_NEG_OFF (0xfffffef4, NEW) x1 (fn07+fn08)
# REF=53 (EWRAM pointer pool slots -- createDWordWithRef):
#   gP1LifePoints x22, gP1SlotSetCodeArray x4, gP1HandSlotArray x9,
#   gP1HandCountBase x2, gP1FieldArrayCBase x7, gDuelPhaseFlags x4,
#   gP1ChainZoneArray x3, gDuelFieldSlots x1, gP1SlotCountBase x1 = 53 total
# FUNC_RENAME=25
# PLATE=25 (full ASCII plate comments, all <= 500 chars)
#
# Critical notes:
#   - fn25 pool 0x0808c924=0xffff803f REUSE slot_field_mask_ffff803f (card_info.inc:1765)
#   - fn21 has TWO pools: pool1 (0x0808c56c..0x0808c574) + pool2 (0x0808c5e4..0x0808c5e8)
#   - fn22 has TWO pools: pool1 (0x0808c65c..0x0808c664) + pool2 (0x0808c6d4..0x0808c6d8)
#   - fn26 name: scan_zone_warrior_lady_wasteland_substate_d (NOT _bd)
#   - NO new GILFORD_HAND_SLOT_MASK -- use existing slot_field_mask_ffff803f
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
# EQ_SLOTS: PLAYER_BLOCK_STRIDE (0x868) -- 26 slots
# =============================================================================
STRIDE_SLOTS = [
    (0x0808bc08, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bc08', None),   # fn01
    (0x0808bc48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bc48', None),   # fn02
    (0x0808bca0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bca0', None),   # fn03 pool1
    (0x0808bcfc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bcfc', None),   # fn03 pool2
    (0x0808bd70, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bd70', None),   # fn04
    (0x0808bde4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bde4', None),   # fn05
    (0x0808be5c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8be5c', None),   # fn06
    (0x0808bf20, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bf20', None),   # fn07+fn08 pool1
    (0x0808bfc4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8bfc4', None),   # fn07+fn08 pool2
    (0x0808c048, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c048', None),   # fn09
    (0x0808c0b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c0b8', None),   # fn10
    (0x0808c14c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c14c', None),   # fn11
    (0x0808c258, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c258', None),   # fn12
    (0x0808c298, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c298', None),   # fn13
    (0x0808c2f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c2f4', None),   # fn14
    (0x0808c34c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c34c', None),   # fn15
    (0x0808c3c8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c3c8', None),   # fn16
    (0x0808c454, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c454', None),   # fn17+fn18
    (0x0808c570, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c570', None),   # fn21 pool1
    (0x0808c5e8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c5e8', None),   # fn21 pool2
    (0x0808c660, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c660', None),   # fn22 pool1
    (0x0808c6d8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c6d8', None),   # fn22 pool2
    (0x0808c788, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c788', None),   # fn23
    (0x0808c7f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c7f8', None),   # fn24
    (0x0808c91c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c91c', None),   # fn25 loop2
    (0x0808c974, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8c974', None),   # fn25 loop2 iter
    (0x0808ca50, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ca50', None),   # fn26
]

# =============================================================================
# EQ_SLOTS: EQUIP_ACTIVE_CTX_OFF (0x484) -- 4 slots
# =============================================================================
CTX_OFF_SLOTS = [
    (0x0808be68, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'ctx_off_8be68', None),  # fn06
    (0x0808bf1c, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'ctx_off_8bf1c', None),  # fn07+fn08
    (0x0808c0c4, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'ctx_off_8c0c4', None),  # fn10
    (0x0808c804, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'ctx_off_8c804', None),  # fn24
]

# =============================================================================
# EQ_SLOTS: CARD_FIELD3_THRESHOLD_1500 (0x5dc) -- 1 slot
# =============================================================================
THRESH_SLOTS = [
    (0x0808ca58, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500', 'thresh_8ca58',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc (1500) ATK filter fn26'),
]

# =============================================================================
# EQ_SLOTS: CID pool equates -- 20 slots (REUSE or NEW)
# =============================================================================
CID_SLOTS = [
    # fn09 -- SKULL_SERVANT_CID (REUSE)
    (0x0808c050, 0x00000fbe, 'SKULL_SERVANT_CID', 'cid_8c050',
     'SKULL_SERVANT_CID=0x0fbe (gate fn09 king_skull_servants)'),
    # fn09 -- KING_OF_SKULL_SERVANTS_CID (REUSE)
    (0x0808c054, 0x000018c5, 'KING_OF_SKULL_SERVANTS_CID', 'cid_8c054',
     'KING_OF_SKULL_SERVANTS_CID=0x18c5 (gate fn09 self)'),
    # fn26 -- PARASITE_PARACIDE_CID (REUSE)
    (0x0808ca5c, 0x000012a1, 'PARASITE_PARACIDE_CID', 'cid_8ca5c',
     'PARASITE_PARACIDE_CID=0x12a1 (find_effect_node_in_zone zone_type=0xb fn26)'),
]

# =============================================================================
# EQ_SLOTS: slot_field_mask_ffff803f (REUSE, card_info.inc:1765) -- 1 slot (fn25)
# =============================================================================
MASK_SLOTS = [
    (0x0808c924, 0xffff803f, 'slot_field_mask_ffff803f', 'mask_8c924',
     'slot_field_mask_ffff803f=0xffff803f clears bits 6..14; REUSE card_info.inc:1765 (fn25)'),
]

# =============================================================================
# EQ_SLOTS: VAMPIRE_GENESIS_GDUELPF_NEG_OFF (0xfffffef4, NEW) -- 1 slot
# =============================================================================
RAW_SLOTS = [
    (0x0808bf28, 0xfffffef4, 'VAMPIRE_GENESIS_GDUELPF_NEG_OFF', 'negoff_8bf28',
     'gDuelPhaseFlags relative negative offset -0x10c'),
]

# =============================================================================
# REF_SLOTS: EWRAM pointer pool slots (createDWordWithRef) -- 53 total
# =============================================================================

# --- gP1LifePoints = 0x0201c4e0 --- 22 slots
REF_P1LP = [
    (0x0808bc04, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bc04', None),   # fn01
    (0x0808bc44, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bc44', None),   # fn02
    (0x0808bc9c, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bc9c', None),   # fn03
    (0x0808bd6c, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bd6c', None),   # fn04
    (0x0808bde0, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bde0', None),   # fn05
    (0x0808bfc0, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8bfc0', None),   # fn07+fn08 pool2
    (0x0808c044, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c044', None),   # fn09
    (0x0808c148, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c148', None),   # fn11
    (0x0808c254, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c254', None),   # fn12
    (0x0808c2f0, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c2f0', None),   # fn14
    (0x0808c348, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c348', None),   # fn15
    (0x0808c3c4, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c3c4', None),   # fn16
    (0x0808c450, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c450', None),   # fn17+fn18
    (0x0808c4f4, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c4f4', None),   # fn20
    (0x0808c56c, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c56c', None),   # fn21 pool1
    (0x0808c5e4, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c5e4', None),   # fn21 pool2
    (0x0808c65c, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c65c', None),   # fn22 pool1
    (0x0808c6d4, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c6d4', None),   # fn22 pool2
    (0x0808c784, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c784', None),   # fn23
    (0x0808c918, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8c918', None),   # fn25 loop2
    (0x0808ca4c, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8ca4c', None),   # fn26
    (0x0808cab4, 0x0201c4e0, 'gP1LifePoints', 'ptr_p1lp_8cab4', None),   # fn27
]

# --- gP1SlotSetCodeArray = 0x0201c740 --- 4 slots
REF_P1SSCA = [
    (0x0808bc0c, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8bc0c', None),  # fn01
    (0x0808c260, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8c260', None),  # fn12
    (0x0808c458, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8c458', None),  # fn17+fn18
    (0x0808ca54, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_p1ssca_8ca54', None),  # fn26
]

# --- gP1HandSlotArray = 0x0201c8f8 --- 9 slots
REF_P1HSA = [
    (0x0808bca4, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8bca4', None),  # fn03
    (0x0808bd74, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8bd74', None),  # fn04
    (0x0808bde8, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8bde8', None),  # fn05
    (0x0808bf2c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8bf2c', None),  # fn07+fn08 loop1
    (0x0808bfc8, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8bfc8', None),  # fn07+fn08 loop2
    (0x0808c04c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8c04c', None),  # fn09
    (0x0808c150, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8c150', None),  # fn11
    (0x0808c920, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8c920', None),  # fn25 loop2
    (0x0808c78c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_p1hsa_8c78c', None),  # fn23
]

# --- gP1HandCountBase = 0x0201c4f4 --- 2 slots
REF_P1HCB = [
    (0x0808bd00, 0x0201c4f4, 'gP1HandCountBase', 'ptr_p1hcb_8bd00', None),  # fn03
    (0x0808c978, 0x0201c4f4, 'gP1HandCountBase', 'ptr_p1hcb_8c978', None),  # fn25 loop2
]

# --- gP1FieldArrayCBase = 0x0201c600 --- 7 slots
REF_P1FAC = [
    (0x0808be60, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8be60', None),  # fn06
    (0x0808bf24, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8bf24', None),  # fn07+fn08 loop1
    (0x0808c0bc, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8c0bc', None),  # fn10
    (0x0808c25c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8c25c', None),  # fn12
    (0x0808c29c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8c29c', None),  # fn13
    (0x0808c4a4, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8c4a4', None),  # fn19
    (0x0808c7fc, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_p1fac_8c7fc', None),  # fn24
]

# --- gDuelPhaseFlags = 0x0201b290 --- 4 slots
REF_DPF = [
    (0x0808be64, 0x0201b290, 'gDuelPhaseFlags', 'ptr_dpf_8be64', None),  # fn06
    (0x0808bf18, 0x0201b290, 'gDuelPhaseFlags', 'ptr_dpf_8bf18', None),  # fn07+fn08
    (0x0808c0c0, 0x0201b290, 'gDuelPhaseFlags', 'ptr_dpf_8c0c0', None),  # fn10
    (0x0808c800, 0x0201b290, 'gDuelPhaseFlags', 'ptr_dpf_8c800', None),  # fn24
]

# --- gP1ChainZoneArray = 0x0201c880 --- 3 slots
REF_P1CZA = [
    (0x0808c3cc, 0x0201c880, 'gP1ChainZoneArray', 'ptr_p1cza_8c3cc', None),  # fn16
    (0x0808c574, 0x0201c880, 'gP1ChainZoneArray', 'ptr_p1cza_8c574', None),  # fn21
    (0x0808c664, 0x0201c880, 'gP1ChainZoneArray', 'ptr_p1cza_8c664', None),  # fn22
]

# --- gDuelFieldSlots = 0x0201c510 --- 1 slot
REF_DFS = [
    (0x0808c898, 0x0201c510, 'gDuelFieldSlots', 'ptr_dfs_8c898', None),  # fn25
]

# --- gP1SlotCountBase = 0x0201c4f0 --- 1 slot
REF_P1SCB = [
    (0x0808ca60, 0x0201c4f0, 'gP1SlotCountBase', 'ptr_p1scb_8ca60', None),  # fn26
]

# =============================================================================
# FUNC_RENAME: 25 functions
# =============================================================================
FUNC_RENAMES = [
    (0x0808bb7c, 'scan_zone_rescue_cat_substate_d'),
    (0x0808bc10, 'scan_zone_a_feather_of_the_phoenix_substate_e'),
    (0x0808bc4c, 'scan_zone_centrifugal_field_substate_e'),
    (0x0808bd04, 'scan_zone_fulfillment_contract_substate_e'),
    (0x0808bd78, 'scan_zone_re_fusion_substate_e'),
    (0x0808bdec, 'scan_zone_beast_soul_swap_substate_b'),
    (0x0808be6c, 'scan_zone_vampire_genesis_substate_be'),
    (0x0808bfcc, 'scan_zone_king_skull_servants_substate_e'),
    (0x0808c058, 'scan_zone_double_attack_substate_b'),
    (0x0808c0c8, 'scan_zone_battery_charger_substate_e'),
    (0x0808c154, 'scan_zone_hero_signal_substate_bd'),
    (0x0808c264, 'scan_zone_level_conversion_lab_substate_b'),
    (0x0808c2a0, 'scan_zone_rock_bombardment_substate_d'),
    (0x0808c2f8, 'scan_zone_wroughtweiler_substate_e'),
    (0x0808c350, 'scan_zone_power_bond_substate_c'),
    (0x0808c3d0, 'scan_zone_summon_priest_substate_d'),
    (0x0808c45c, 'scan_zone_bubble_shuffle_substate_b'),
    (0x0808c4a8, 'scan_zone_fusion_recovery_substate_e'),
    (0x0808c4fc, 'scan_zone_miracle_fusion_substate_ce'),
    (0x0808c5ec, 'scan_zone_dragons_mirror_substate_ce'),
    (0x0808c6dc, 'scan_zone_spiritual_earth_art_substate_e'),
    (0x0808c790, 'scan_zone_a_rival_appears_substate_b'),
    (0x0808c808, 'scan_zone_gilford_the_legend_substate_e'),
    (0x0808c97c, 'scan_zone_warrior_lady_wasteland_substate_d'),
    (0x0808ca64, 'scan_zone_divine_sword_phoenix_blade_substate_e'),
]

# =============================================================================
# PLATE: 25 ASCII plate comments (all <= 500 chars)
# =============================================================================
PLATES = [
    (0x0808bb7c,
     'Equip zone scan for Rescue Cat (RESCUE_CAT_CID=0x1876, pw=14878871). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (race check, field6=0x6); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x1876].'),
    (0x0808bc10,
     'Equip zone scan for A Feather of the Phoenix (A_FEATHER_OF_THE_PHOENIX_CID=0x187a, pw=49140998). GY+hand zone via gP1LifePoints+PLAYER_BLOCK_STRIDE simple loop; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x187a].'),
    (0x0808bc4c,
     'Equip zone scan for Centrifugal Field (CENTRIFUGAL_FIELD_CID=0x187f, pw=01801154). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: get_equip_display_type_code + get_equip_display_criteria_code + check_card_pair_allowed + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x187f].'),
    (0x0808bd04,
     'Equip zone scan for Fulfillment of the Contract (FULFILLMENT_CONTRACT_CID=0x1880, pw=48206762). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_type_is_trap + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1880].'),
    (0x0808bd78,
     'Equip zone scan for Re-Fusion (RE_FUSION_CID=0x1881, pw=74694807). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_type_is_spell + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1881].'),
    (0x0808bdec,
     'Equip zone scan for Beast Soul Swap (BEAST_SOUL_SWAP_CID=0x1889, pw=35149085). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + get_card_extended_stat_field6 (race 0xb) + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write substate_b. Uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF. Dispatch table entry [CID 0x1889].'),
    (0x0808be6c,
     'Equip zone scan for Vampire Genesis (VAMPIRE_GENESIS_CID=0x1895, pw=22056710). Two-loop: loop1 field zone (gP1FieldArrayCBase) gate field5+field6+field5 x2+equip_eligible -> substate_b; loop2 hand zone (gP1HandSlotArray) gate field5_nonzero+field6+field5+equip_eligible -> substate_e. Uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF. Dispatch entry [CID 0x1895]. combined fn: fn07 start=0x0808be6c; fn08(0x0808be88)=degenerate excluded.'),
    (0x0808bfcc,
     'Equip zone scan for King of the Skull Servants (KING_OF_SKULL_SERVANTS_CID=0x18c5, pw=36021814). Hand zone via gP1LifePoints+gP1HandSlotArray; gate: card_type field == SKULL_SERVANT_CID (0x0fbe) OR KING_OF_SKULL_SERVANTS_CID (0x18c5) + equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [CID 0x18c5].'),
    (0x0808c058,
     'Equip zone scan for Double Attack (DOUBLE_ATTACK_CID=0x18cb, pw=34187685). Field spell zone via gP1FieldArrayCBase+gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF; gates: check_card_field5_is_nonzero + eval_equip_bonus_for_slot + count_effect_node_activations_by_zone; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entry [CID 0x18cb].'),
    (0x0808c0c8,
     'Equip zone scan for Battery Charger (BATTERY_CHARGER_CID=0x18cc, pw=61181383). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_is_batteryman_type + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x18cc].'),
    (0x0808c154,
     'Equip zone scan for Hero Signal (HERO_SIGNAL_CID=0x18d4, pw=22020907). Two-loop: loop1 via gP1FieldArrayCBase (field, +0xc) gate check_card_id_is_normal_summon_type+eval_equip_bonus+eval_equip_placement -> substate_b; loop2 via gP1SlotSetCodeArray (monster) gate normal_summon+field5+eval_placement -> substate_d. Dispatch entry [CID 0x18d4].'),
    (0x0808c264,
     'Equip zone scan for Level Conversion Lab (LEVEL_CONVERSION_LAB_CID=0x18d9, pw=84397023). Field spell zone via gP1FieldArrayCBase; gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x18d9].'),
    (0x0808c2a0,
     'Equip zone scan for Rock Bombardment (ROCK_BOMBARDMENT_CID=0x18da, pw=20781762). Monster zone via gP1LifePoints inner loop (stride 0x10, init=0x98); gate: get_card_extended_stat_field6 == 0x6 (Rock type); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x18da].'),
    (0x0808c2f8,
     'Equip zone scan for Wroughtweiler (WROUGHTWEILER_CID=0x18f7, pw=06480253). Monster zone via gP1LifePoints inner loop (stride 0x14, init=0x83); gate: check_card_id_is_normal_summon_type; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x18f7].'),
    (0x0808c350,
     'Equip zone scan for Power Bond (POWER_BOND_CID=0x18fe, pw=37630732). Chain zone via gP1ChainZoneArray+gP1LifePoints; gates: get_card_extended_stat_field6 == 7 (Machine type) + build_equip_slot_criteria_from_card_range; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatch table entry [CID 0x18fe].'),
    (0x0808c3d0,
     'Equip zone scan for Summon Priest (SUMMON_PRIEST_CID=0x1900, pw=00423585). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field5 (level 4) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [CID 0x1900]. combined fn: fn17 start=0x0808c3d0; fn18(0x0808c3da)=degenerate excluded.'),
    (0x0808c45c,
     'Equip zone scan for Bubble Shuffle (BUBBLE_SHUFFLE_CID=0x1908, pw=61968753). Field spell zone via gP1FieldArrayCBase; gates: check_card_id_is_normal_summon_type + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x1908].'),
    (0x0808c4a8,
     'Equip zone scan for Fusion Recovery (FUSION_RECOVERY_CID=0x191f, pw=18511384). Monster zone via gP1LifePoints inner loop (stride 0x14, init=0x83); gate: check_card_id_is_normal_summon_type; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x191f].'),
    (0x0808c4fc,
     'Equip zone scan for Miracle Fusion (MIRACLE_FUSION_CID=0x1920, pw=45906428). Two-path: if r2!=0 scan chain zone (gP1ChainZoneArray) gate check_spell_zone_slot_placeable -> substate_c; then scan hand zone (gP1LifePoints loop) gate check_equip_slot_eligible_with_criteria_and_prerequisites -> substate_e. Dispatch entry [CID 0x1920].'),
    (0x0808c5ec,
     'Equip zone scan for Dragons Mirror (DRAGONS_MIRROR_CID=0x1921, pw=71490127). Two-path: if r2!=0 scan chain zone (gP1ChainZoneArray) gate field6==1 (DARK) + check_spell_zone_slot_placeable -> substate_c; then hand zone loop gate check_equip_slot_eligible_with_criteria -> substate_e. Dispatch entry [CID 0x1921].'),
    (0x0808c6dc,
     'Equip zone scan for Spiritual Earth Art - Kurogane (SPIRITUAL_EARTH_ART_CID=0x1927, pw=70156997). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field5 (level) + check_card_stat_field7_equals(5) (EARTH attr) + level bit-extract + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [CID 0x1927].'),
    (0x0808c790,
     'Equip zone scan for A Rival Appears! (A_RIVAL_APPEARS_CID=0x192b, pw=05728014). Field spell zone via gP1FieldArrayCBase+gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF; gates: check_card_field5_is_nonzero + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entry [CID 0x192b].'),
    (0x0808c808,
     'Equip zone scan for Gilford the Legend (GILFORD_THE_LEGEND_CID=0x1938, pw=69933858). Two-loop: loop1 field (gDuelFieldSlots stride PLAYER_BLOCK_STRIDE) gate get_slot_card_state_code + check_slot_card_eligible_by_card_id; loop2 hand zone (gP1LifePoints+gP1HandSlotArray) gate get_card_extended_stat_field9 + slot_field_mask_ffff803f (0xffff803f) + check_slot_card_eligible_by_card_id; write substate_e. Dispatch entry [CID 0x1938].'),
    (0x0808c97c,
     'Equip zone scan for Warrior Lady of the Wasteland (WARRIOR_LADY_WASTELAND_CID=0x1939, pw=05438492). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: field5_nonzero + field3_raw<=0x5dc (ATK<=1500) + field7 x2 + field6 x2 + eval_equip_placement + find_effect_node(PARASITE_PARACIDE_CID=0x12a1); write substate_d; 0xb passed to find_effect_node_in_zone as zone type. Dispatch entry [CID 0x1939].'),
    (0x0808ca64,
     'Equip zone scan for Divine Sword - Phoenix Blade (DIVINE_SWORD_PHOENIX_BLADE_CID=0x193a, pw=31423101). Monster zone via gP1LifePoints inner loop (stride 0x14, init=0x83); gate: get_card_extended_stat_field6 == 0xf (Warrior type); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x193a].'),
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

    # --- Step 2: EQUIP_ACTIVE_CTX_OFF EQ slots ---
    print("=== CTX_OFF EQ (%d slots) ===" % len(CTX_OFF_SLOTS))
    for args in CTX_OFF_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 3: CARD_FIELD3_THRESHOLD_1500 EQ slots ---
    print("=== THRESH EQ (%d slots) ===" % len(THRESH_SLOTS))
    for args in THRESH_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 4: CID EQ slots ---
    print("=== CID EQ (%d slots) ===" % len(CID_SLOTS))
    for args in CID_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 5: slot_field_mask_ffff803f (REUSE) ---
    print("=== MASK EQ (%d slots) ===" % len(MASK_SLOTS))
    for args in MASK_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 6: RAW value EQ slots ---
    print("=== RAW EQ (%d slots) ===" % len(RAW_SLOTS))
    for args in RAW_SLOTS:
        if _apply_eq(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 7: REF slots (EWRAM pointers) ---
    all_refs = REF_P1LP + REF_P1SSCA + REF_P1HSA + REF_P1HCB + REF_P1FAC + REF_DPF + REF_P1CZA + REF_DFS + REF_P1SCB
    print("=== REF (%d slots) ===" % len(all_refs))
    for args in all_refs:
        if _apply_ref(*args):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 8: FUNC_RENAME ---
    print("=== FUNC_RENAME (%d fns) ===" % len(FUNC_RENAMES))
    for fn_addr, fn_name in FUNC_RENAMES:
        if _func_rename(fn_addr, fn_name):
            ok_count += 1
        else:
            fail_count += 1

    # --- Step 9: PLATE ---
    print("=== PLATE (%d fns) ===" % len(PLATES))
    for fn_addr, plate_text in PLATES:
        if _apply_plate(fn_addr, plate_text):
            ok_count += 1
        else:
            fail_count += 1

    print("")
    print("=== RefineF11Seg4fSlots DONE ===")
    print("  ok=%d  fail=%d" % (ok_count, fail_count))
    total_eq = len(STRIDE_SLOTS) + len(CTX_OFF_SLOTS) + len(THRESH_SLOTS) + len(CID_SLOTS) + len(MASK_SLOTS) + len(RAW_SLOTS)
    print("  EQ(STRIDE)=%d  EQ(CTX_OFF)=%d  EQ(THRESH)=%d  EQ(CID)=%d  EQ(MASK)=%d  EQ(RAW)=%d  REF=%d  FUNC_RENAME=%d  PLATE=%d" % (
        len(STRIDE_SLOTS), len(CTX_OFF_SLOTS), len(THRESH_SLOTS), len(CID_SLOTS), len(MASK_SLOTS), len(RAW_SLOTS),
        len(all_refs), len(FUNC_RENAMES), len(PLATES)))
    if fail_count > 0:
        print("  WARN: %d FAIL(s) -- review output above" % fail_count)
    else:
        print("  ALL PASS")


main()
