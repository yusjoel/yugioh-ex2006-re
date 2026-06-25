# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4bSlots.py -- f11 Seg-4b slot symbolization [0x08088904..0x0808962c)
#
# 25 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ: PLAYER_BLOCK_STRIDE (0x868) slots x25 + CID pool values (REUSE or NEW from card_info.inc)
#   + scalar equates (zone_query_hand_tag_12a1, LP_BAR_ANIM_STATE_OFF, SPRITE_ROW_ENTRY_DATA_OFF)
# REF=40 (EWRAM pointer pool slots -- createDWordWithRef):
#   gP1LifePoints x23, gP1SlotSetCodeArray x6, gP1HandSlotArray x4,
#   gP1FieldArrayCBase x3, gP1ChainZoneArray x1, gP1AltHandSlotArray x1,
#   gP1SlotCountBase x1, gDuelPhaseFlags x1
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
    (0x08088968, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88968', None),
    (0x080889c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_889c0', None),
    (0x08088a30, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88a30', None),
    (0x08088ad0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88ad0', None),
    (0x08088b28, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88b28', None),
    (0x08088c88, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88c88', None),
    (0x08088d20, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88d20', None),
    (0x08088db0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88db0', None),
    (0x08088e08, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88e08', None),
    (0x08088e60, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88e60', None),
    (0x08088ed0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88ed0', None),
    (0x08088f74, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88f74', None),
    (0x08088fd8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_88fd8', None),
    (0x08089060, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89060', None),
    (0x080890bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_890bc', None),
    (0x0808910c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8910c', None),
    (0x0808914c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8914c', None),
    (0x080891c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_891c0', None),
    (0x080891f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_891f4', None),
    (0x0808927c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8927c', None),
    (0x080892b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_892b0', None),
    (0x08089334, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89334', None),
    (0x08089374, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89374', None),
    (0x080894a8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_894a8', None),
    (0x080894fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_894fc', None),
    (0x08089554, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_89554', None),
    (0x0808961c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8961c', None),
]

# =============================================================================
# CID_SLOTS: CID pool value equates (REUSE or NEW names from card_info.inc)
# =============================================================================
CID_SLOTS = [
    # fn01 (0x08088904): KYCOO_THE_GHOST_DESTROYER_CID (NEW)
    # No explicit CID pool in fn01 -- CID used inline via dispatch table, not in literal pool
    # (fn01 uses gP1LifePoints+PLAYER_BLOCK_STRIDE only; no CID pool DWord in this fn)

    # fn07 (0x08088c9c): FOOLISH_BURIAL_CID (NEW) -- no CID pool in fn07 body
    # (fn07 uses gP1LifePoints/gP1SlotSetCodeArray/zone_query_hand_tag -- no raw CID pool DWord)

    # fn21 (0x080892b4): SUPER_ROBOLADY_CID + SUPER_ROBOYAROU_CID pool values
    (0x080892cc, 0x00001507, 'SUPER_ROBOLADY_CID',  'cid_robolady_892cc', 'SUPER_ROBOLADY_CID=0x1507; pair check pool in scan_zone_super_robo_pair'),
    (0x080892d0, 0x00001508, 'SUPER_ROBOYAROU_CID', 'cid_roboyarou_892d0', 'SUPER_ROBOYAROU_CID=0x1508; pair check pool (partner B) in scan_zone_super_robo_pair'),
    (0x080892dc, 0x00001508, 'SUPER_ROBOYAROU_CID', 'cid_roboyarou_892dc', 'SUPER_ROBOYAROU_CID=0x1508; pair check pool (partner A swap) in scan_zone_super_robo_pair'),

    # scalar: zone_query_hand_tag_12a1 (fn06, fn07, fn14, fn23, fn26)
    (0x08088c94, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_88c94', None),
    (0x08088d28, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_88d28', None),
    (0x08089418, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_89418', None),
    (0x08089624, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_89624', None),

    # fn12 (0x08088ed8): LP_BAR_ANIM_STATE_OFF + SPRITE_ROW_ENTRY_DATA_OFF
    (0x08088f6c, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',   'lp_bar_anim_88f6c', 'LP_BAR_ANIM_STATE_OFF=0x4cc; gDuelPhaseFlags offset for lp-bar anim state count'),
    (0x08088f70, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF','spr_row_88f70',     'SPRITE_ROW_ENTRY_DATA_OFF=0x4d4; gDuelPhaseFlags offset for sprite row entry data'),
]

EQ_SLOTS = STRIDE_SLOTS + CID_SLOTS

# =============================================================================
# REF_SLOTS: EWRAM pointer pool slots (createDWordWithRef)
# =============================================================================

# gP1LifePoints = 0x0201c4e0 (ewram.inc): 23 slots
LP_SLOTS = [
    (0x08088964, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88964', None),
    (0x080889bc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_889bc', None),
    (0x08088a2c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88a2c', None),
    (0x08088acc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88acc', None),
    (0x08088b24, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88b24', None),
    (0x08088c84, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88c84', None),
    (0x08088d1c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88d1c', None),
    (0x08088dac, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88dac', None),
    (0x08088e04, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88e04', None),
    (0x08088e5c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88e5c', None),
    (0x08088ecc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_88ecc', None),
    (0x08089148, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89148', None),
    (0x080891bc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_891bc', None),
    (0x08089278, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89278', None),
    (0x080892ac, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_892ac', None),
    (0x08089330, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89330', None),
    (0x08089370, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89370', None),
    (0x0808940c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8940c', None),
    (0x080894a4, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_894a4', None),
    (0x080894f8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_894f8', None),
    (0x08089550, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89550', None),
    (0x08089618, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_89618', None),
    (0x0808905c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8905c', None),
]

# gP1SlotSetCodeArray = 0x0201c740 (ewram.inc): 6 slots
SCA_SLOTS = [
    (0x08088c90, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_88c90', None),
    (0x08088d24, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_88d24', None),
    (0x08089064, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89064', None),
    (0x08089414, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89414', None),
    (0x080894ac, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_894ac', None),
    (0x08089620, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_89620', None),
]

# gP1HandSlotArray = 0x0201c8f8 (ewram.inc): 4 slots
HSA_SLOTS = [
    (0x08088db4, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_88db4', None),
    (0x08088f78, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_88f78', None),
    (0x080891c4, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_891c4', None),
    (0x08089280, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_89280', None),
]

# gP1FieldArrayCBase = 0x0201c600 (ewram.inc): 3 slots
FAC_SLOTS = [
    (0x08088c8c, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_88c8c', None),
    (0x08088fdc, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_88fdc', None),
    (0x08089110, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_89110', None),
]

# gP1ChainZoneArray = 0x0201c880 (ewram.inc line 336): 1 slot
CZA_SLOTS = [
    (0x08088c98, 0x0201c880, 'gP1ChainZoneArray', 'ptr_cza_88c98', None),
]

# gP1AltHandSlotArray = 0x0201cab0 (ewram.inc line 338): 1 slot
AHA_SLOTS = [
    (0x08088ed4, 0x0201cab0, 'gP1AltHandSlotArray', 'ptr_aha_88ed4', None),
]

# gP1SlotCountBase = 0x0201c4f0 (ewram.inc): 1 slot
SCB_SLOTS = [
    (0x08089628, 0x0201c4f0, 'gP1SlotCountBase', 'ptr_scb_89628', None),
]

# gDuelPhaseFlags = 0x0201b290 (ewram.inc): 1 slot
# Note: fn12 has two ldr ops that both resolve to 0x08088f68; only one createDWord/REF needed
DPF_SLOTS = [
    (0x08088f68, 0x0201b290, 'gDuelPhaseFlags', 'ptr_dpf_88f68', None),
]

REF_SLOTS = LP_SLOTS + SCA_SLOTS + HSA_SLOTS + FAC_SLOTS + CZA_SLOTS + AHA_SLOTS + SCB_SLOTS + DPF_SLOTS

# =============================================================================
# FUNC_RENAME: 25 functions
# =============================================================================
FUNC_RENAMES = [
    (0x08088904, 'scan_zone_kycoo_dark_blade_group_substate_e'),
    (0x0808896c, 'scan_zone_bazoo_substate_e'),
    (0x080889c4, 'scan_zone_removed_accumulator_group_substate_e'),
    (0x08088a34, 'scan_zone_destiny_board_substate_bd'),
    (0x08088ad4, 'scan_zone_dark_sage_substate_d'),
    (0x08088b2c, 'scan_zone_cathedral_of_nobles_substate_bdc'),
    (0x08088c9c, 'scan_zone_foolish_burial_substate_d'),
    (0x08088d2c, 'scan_zone_removed_spirit_elemental_group_substate_e'),
    (0x08088db8, 'scan_zone_supply_substate_e'),
    (0x08088e0c, 'scan_zone_skull_lair_substate_e'),
    (0x08088e64, 'scan_zone_miracle_dig_substate_f'),
    (0x08088ed8, 'scan_zone_rope_of_life_substate_e'),
    (0x08088f7c, 'scan_zone_marauding_captain_group_substate_b'),
    (0x08088fe0, 'scan_zone_warrior_search_group_substate_d'),
    (0x08089068, 'scan_zone_warrior_returning_alive_substate_e'),
    (0x080890c0, 'scan_zone_spirit_ryu_substate_b'),
    (0x08089114, 'scan_zone_des_feral_imp_substate_e'),
    (0x08089150, 'scan_zone_agido_substate_e'),
    (0x080891f8, 'scan_zone_silent_fiend_soul_res_group_substate_e'),
    (0x08089284, 'scan_zone_maharaghi_substate_d'),
    (0x080892b4, 'scan_zone_super_robo_pair_substate_c'),
    (0x08089338, 'scan_zone_removed_zone_return_group_substate_e'),
    (0x08089378, 'scan_zone_last_turn_substate_d'),
    (0x0808941c, 'scan_zone_vampire_lord_lady_group_substate_d'),
    (0x08089558, 'scan_zone_pyramid_turtle_substate_d'),
]

# =============================================================================
# PLATE_OPS: 25 full ASCII plate comments (<= 500 chars each)
# =============================================================================
PLATE_OPS = [
    (0x08088904,
     "Equip zone scan callback for Kycoo/Dark Blade group: Kycoo the Ghost Destroyer (CID=0x1480, pw=88240808), Dark Blade the Dragon Knight (DARK_BLADE_THE_DRAGON_KNIGHT_CID=0x183c, pw=86805855). r0=player_id. Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [63,228]."),

    (0x0808896c,
     "Equip zone scan callback for Bazoo the Soul-Eater (BAZOO_THE_SOUL_EATER_CID=0x1482, pw=40133511). r0=player_id. Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [65]."),

    (0x080889c4,
     "Equip zone scan callback for removed-accumulator group: Dark Necrofear (DARK_NECROFEAR_CID=0x1466, pw=31829185), Megarock Dragon (MEGAROCK_DRAGON_CID=0x18b4, pw=71544954), Doom Dozer (DOOM_DOZER_CID=0x19ca, pw=76039636). Gate: get_card_extended_stat_field6 pair-compare; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [57,250,299]."),

    (0x08088a34,
     "Equip zone scan callback for Destiny Board (DESTINY_BOARD_CID=0x1468, pw=94212438). r0=player_id. Two loops: loop1 scans field at +0xc, write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx); loop2 scans at +0x10, write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [58]."),

    (0x08088ad4,
     "Equip zone scan callback for Dark Sage (DARK_SAGE_CID=0x146e, pw=92377303). r0=player_id. Gate: get_card_extended_stat_field6 == 0x16; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [59]."),

    (0x08088b2c,
     "Equip zone scan callback for Cathedral of Nobles (CATHEDRAL_OF_NOBLES_CID=0x146f, pw=29762407). r0=player_id. Three-path scan: (1) gP1FieldArrayCBase -- field5+eval_equip_placement+find_node gate, substate b; (2) gP1SlotSetCodeArray -- zone_query_hand_tag filter+equip_target_eligible+excl_range gate, substate d; (3) gP1ChainZoneArray -- substate c. Dispatched from write table entry [60]."),

    (0x08088c9c,
     "Equip zone scan callback for Foolish Burial (CID=0x1474, pw=81439173). r0=player_id. Gate: check_card_field5_is_nonzero + find_effect_node_in_zone via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [61]."),

    (0x08088d2c,
     "Equip zone scan callback for removed-from-play spirit/elemental group (13 CIDs): SOUL_OF_PURITY_CID(0x1483), Spirit_of_Flames(0x1484), AQUA_SPIRIT_CID(0x1485), ROCK_SPIRIT_CID(0x1486), Garuda(0x1487), Lekunga(0x15bc), STRIKE_NINJA_CID(0x16b9), Freed_Brave_Wanderer(0x16c0), INFERNO_CID(0x16c5), FENRIR_CID(0x16c6), Gigantes(0x16c7), SILPHEED_CID(0x16c8), Infernal_Flame_Emperor(0x18e0). Gate: field5+field8+field7; write substate e. Dispatched from entries [66-70,117,152,154,157-160,257]."),

    (0x08088db8,
     "Equip zone scan callback for Supply (CID=0x148b, pw=44072894). r0=player_id. Simple loop over hand slots in gP1LifePoints[player*STRIDE]; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx) for all entries. Dispatched from write table entry [72]."),

    (0x08088e0c,
     "Equip zone scan callback for Skull Lair (CID=0x1490, pw=06733059). r0=player_id. Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [73]."),

    (0x08088e64,
     "Equip zone scan callback for Miracle Dig (MIRACLE_DIG_CID=0x149e, pw=06343408). r0=player_id. Gate: check_card_field5_is_nonzero + get_zone_card_attribute_by_type via gP1AltHandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xf, slot_idx). Dispatched from write table entry [75]."),

    (0x08088ed8,
     "Equip zone scan callback for Rope of Life (ROPE_OF_LIFE_CID=0x14a7, pw=93382620). r0=player_id. Gate: gDuelPhaseFlags+LP_BAR_ANIM_STATE_OFF(0x4cc) count loop; check sprite_row_entry_data[slot]==0x16 (battle-destroyed marker); find_hand_slot_idx_by_set_code; field5; equip_eligible; write substate e. Dispatched from write table entry [76]."),

    (0x08088f7c,
     "Equip zone scan callback for Marauding Captain group: cid_135b (0x135b, unallocated), Marauding Captain (MARAUDING_CAPTAIN_CID=0x14c6, pw=02460565). Gate: check_card_field5_is_nonzero + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entries [39,78]."),

    (0x08088fe0,
     "Equip zone scan callback for warrior search group: Freed the Matchless General (FREED_THE_MATCHLESS_GENERAL_CID=0x14c4, pw=49681811), Reinforcement of the Army (CID=0x14d0, pw=32807846). Gate: check_card_field5_is_nonzero + field7+field6 check via gP1SlotSetCodeArray; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [77,79]."),

    (0x08089068,
     "Equip zone scan callback for The Warrior Returning Alive (THE_WARRIOR_RETURNING_ALIVE_CID=0x14d2, pw=95281259). r0=player_id. Gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [80]."),

    (0x080890c0,
     "Equip zone scan callback for Spirit Ryu (SPIRIT_RYU_CID=0x14d7, pw=67957315). r0=player_id. Gate: check_card_field5_is_nonzero + get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx) via gP1FieldArrayCBase scan. Dispatched from write table entry [81]."),

    (0x08089114,
     "Equip zone scan callback for Des Feral Imp (CID=0x14ef, pw=81985784). r0=player_id. Simple loop over hand slots; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx) for all entries. Dispatched from write table entry [86]."),

    (0x08089150,
     "Equip zone scan callback for Agido (AGIDO_CID=0x14f6, pw=16135253). r0=player_id. Gate: get_card_extended_stat_field6==0x11 (Fairy type) + check_zone_slot_equip_eligible + field7 pair compare; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [87]."),

    (0x080891f8,
     "Equip zone scan callback for Silent Fiend/Soul Resurrection group: Silent Fiend (CID=0x14f7, pw=42534368), Soul Resurrection (SOUL_RESURRECTION_CID=0x17b7, pw=92924317). Gate: check_card_field5_is_nonzero + map_field8_to_card_type_category + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [88,196]."),

    (0x08089284,
     "Equip zone scan callback for Maharaghi (MAHARAGHI_CID=0x14fd, pw=40695128). r0=player_id. Simple loop over monster zone in gP1LifePoints[player*STRIDE+0x18]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [89]."),

    (0x080892b4,
     "Equip zone scan callback for Super Robolady/Roboyarou pair: Super Robolady (CID=0x1507, pw=75923050), Super Roboyarou (CID=0x1508, pw=01412158). r0=player_id. Pair check: if input_CID==0x1507 seek 0x1508 in zone (or vice versa); write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatched from write table entries [90,91]."),

    (0x08089338,
     "Equip zone scan callback for removed-zone return group: Keldo (KELDO_CID=0x14e7, pw=80441106), Disappear (DISAPPEAR_CID=0x1515, pw=24623598), Dimension Jar (DIMENSION_JAR_CID=0x15dd, pw=73414375), D.D. Guide (DD_GUIDE_CID=0x19c0, pw=52702748). Simple loop write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [83,92,120,297]."),

    (0x08089378,
     "Equip zone scan callback for Last Turn (LAST_TURN_CID=0x151e, pw=28566710). r0=player_id. Gate: check_card_field5_is_nonzero + eval_equip_placement_full_check + find_effect_node_in_zone via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x0808939c is mid-body loop continuation (degenerate, bcs target). Dispatched from write table entry [93]."),

    (0x0808941c,
     "Equip zone scan callback for Vampire Lord/Lady group: Vampire Lord (VAMPIRE_LORD_CID=0x1522, pw=53839837), Vampire Lady (VAMPIRE_LADY_CID=0x1746, pw=26495087). r0=player_id. Three-loop scan with field5+find_node+field6 gates; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) x3. Dispatched from write table entries [94,179]."),

    (0x08089558,
     "Equip zone scan callback for Pyramid Turtle (CID=0x152f, pw=77044671). r0=player_id. Gate: check_card_field5_is_nonzero + field8 + eval_equip_placement_full_check + find_effect_node_in_zone via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x08089560 is mid-prologue degenerate (second push in high-reg save). Dispatched from write table entry [96]."),
]


def main():
    print("=== RefineF11Seg4bSlots (DRY=%s) ===" % DRY)
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
    print("--- REF_SLOTS (%d: %d LP + %d SCA + %d HSA + %d FAC + %d CZA + %d AHA + %d SCB + %d DPF) ---" % (
        len(REF_SLOTS), len(LP_SLOTS), len(SCA_SLOTS), len(HSA_SLOTS),
        len(FAC_SLOTS), len(CZA_SLOTS), len(AHA_SLOTS), len(SCB_SLOTS), len(DPF_SLOTS)))
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
