# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg5Slots.py -- f11 Seg-5 slot symbolization [0x0808d7f4..0x0808e8fc)
#
# 18 named functions (equip field scan / sprite enqueue cluster)
# 0 ROM_INCBIN; region C (all pre-existing named functions)
#
# EQ: 14x PTR_gP1LifePoints REUSE (as equate-based RENAME)
#     + 36x PLAYER_BLOCK_STRIDE (0x868) REUSE
#     + 12x gDuelFieldSlots (0x0201c510) REUSE
#     + 5x gDuelFieldSlotState (0x0201c520) REUSE
#     + 7x gEquipEffectZoneBase (0x0201e4f0) REUSE
#     + 6x gEquipZoneCountTable (0x0201e1c8) REUSE
#     + 1x gDuelFieldSlots_p2_base (0x0201c5d8) REUSE
#     + 1x gDuelPhaseFlags (0x0201b290) REUSE
#     + 1x gEffectEntryArray (0x0201b590) REUSE
#     + 1x ACTIVE_EFFECT_CATEGORY_OFF (0x000010d8) REUSE
#     + 1x LP_ACTIVATION_LINK_FLAG_OFF (0x000010d0) REUSE
#     + 1x EQUIP_CHAIN_STEP_OFF (0x00001d28) REUSE
#     + 2x DRAGON_CAPTURE_JAR_CID (0x000010ef) REUSE
#     + 2x INSECT_PRINCESS_CID (0x00001704) REUSE
#     + 2x FINAL_ATTACK_ORDERS_CID (0x000015fb) NEW
#     + 2x LEVEL_LIMIT_AREA_B_CID (0x000017a6) NEW
#     + 2x LEVEL_LIMIT_AREA_A_CID (0x0000197b) NEW
#     + 1x cid_12fb (0x000012fb) REUSE
#     + 1x MONSTER_REBORN_CID (0x000012ea) REUSE
#     + 1x CHAIN_ENERGY_CID (0x0000132c) REUSE
#     + 3x KOTODAMA_CID (0x00001343) NEW
#     + 1x FORCED_REQUISITION_CID (0x00001354) REUSE
#     + 1x MAGICAL_THORN_CID (0x00001306) NEW
#     + 1x SKULL_INVITATION_CID (0x00001361) NEW
#     + 1x MAIDEN_OF_THE_AQUA_CID (0x000013a2) NEW
#     + 2x gEffectHandlerTable (0x09e5a128) NEW
#     + 1x gEquipCandidateInitBase (0x09e3f164) NEW
#     + 4x gEquipCandidateScoreBase (0x09e3f150) NEW
#     + 1x SLOT_ACTIVE_CHECK_CODE (0x0000104c) NEW
#     + 1x P1LP_BLOCK2_OFF_1CE8 (0x00001ce8) REUSE x2
#     + 2x UMI_CARD_ID (0x000010f4) REUSE
#     + 1x PUMPKING_CID (0x00001009) REUSE
#     + 1x CASTLE_OF_DARK_ILLUSIONS_CID (0x00000ff9) REUSE
#     + raw DWORDs (kept as-is): 0x0000fdc, 0x98300000, 0x9b080000, 0x3a200000, 0xffffe358
# RENAME: 14x PTR_gP1LifePoints_0808xxxx -> ptr_lp_* + 1x DAT_0808d8a8 -> switchd_base_d8a8
# REF: 0
# PLATE: 12 functions (C8 stale-FUN_ substitution)
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


def _rename_label(slot_addr, old_prefix, new_label):
    """Rename a label (e.g. PTR_gP1LifePoints_xxxx -> ptr_lp_xxxx)."""
    if DRY:
        print("[dry] RENAME 0x%08x  -> %s" % (slot_addr, new_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    renamed = False
    for s in sym_tbl.getSymbols(a):
        if s.getName().startswith(old_prefix):
            try:
                s.setName(new_label, SourceType.USER_DEFINED)
                s.setPrimary()
                renamed = True
                print("[REN] 0x%08x  %s -> %s" % (slot_addr, old_prefix + '...', new_label))
            except Exception as e:
                print("FAIL RENAME 0x%08x %s: %s (WARN=FAIL)" % (slot_addr, new_label, e))
                return False
            break
    if not renamed:
        # Label may not exist yet; create it
        try:
            sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
            for s in sym_tbl.getSymbols(a):
                if s.getName() == new_label:
                    s.setPrimary()
                    break
            print("[REN_NEW] 0x%08x  -> %s" % (slot_addr, new_label))
        except Exception as e:
            print("FAIL RENAME_NEW 0x%08x %s: %s (WARN=FAIL)" % (slot_addr, new_label, e))
            return False
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


# =============================================================================
# EQ_SLOTS: PTR_gP1LifePoints as equate-based symbolic (gP1LifePoints value = 0x0201c4e0)
# 14 slots -- applying equate for the pointer value 0x0201c4e0
# =============================================================================
LP_PTR_SLOTS = [
    (0x0808d820, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d820', None),
    (0x0808d838, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d838', None),
    (0x0808d850, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d850', None),
    (0x0808d884, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d884', None),
    (0x0808d8fc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d8fc', None),
    (0x0808d940, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d940', None),
    (0x0808d984, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d984', None),
    (0x0808d9c8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_d9c8', None),
    (0x0808da10, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_da10', None),
    (0x0808dc2c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_dc2c', None),
    (0x0808dd50, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_dd50', None),
    (0x0808e2bc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_e2bc', None),
    (0x0808e6b8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_e6b8', None),
    (0x0808ea10, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_ea10', None),
]

# =============================================================================
# EQ_SLOTS: PLAYER_BLOCK_STRIDE (0x00000868) -- 36 slots REUSE
# =============================================================================
STRIDE_SLOTS = [
    (0x0808d824, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d824', None),
    (0x0808d83c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d83c', None),
    (0x0808d854, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d854', None),
    (0x0808d888, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d888', None),
    (0x0808d900, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d900', None),
    (0x0808d944, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d944', None),
    (0x0808d988, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d988', None),
    (0x0808d9cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_d9cc', None),
    (0x0808da14, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_da14', None),
    (0x0808da60, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_da60', None),
    (0x0808dc20, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_dc20', None),
    (0x0808dd54, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_dd54', None),
    (0x0808de30, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_de30', None),
    (0x0808df34, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_df34', None),
    (0x0808e058, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e058', None),
    (0x0808e0f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e0f8', None),
    (0x0808e2c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e2c4', None),
    (0x0808e5b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e5b8', None),
    (0x0808e6cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e6cc', None),
    (0x0808e828, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e828', None),
    (0x0808e8ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e8ec', None),
    (0x0808ea18, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_ea18', None),
    (0x0808e4d0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'seg5_pool_stride_e4d0', None),
]

# Note: DAT_0808e5b0 = 0xffffe358 is a raw signed offset (gDuelFieldSlotState - gEquipZoneCountTable);
# no named constant, left as-is (raw DWORD). No equate applied.

# =============================================================================
# EQ_SLOTS: gDuelFieldSlots (0x0201c510) -- remaining slots not in STRIDE_SLOTS
# =============================================================================
FIELD_SLOTS_SLOTS = [
    (0x0808da64, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_da64', None),
    (0x0808dd58, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_dd58', None),
    (0x0808de34, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_de34', None),
    (0x0808df38, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_df38', None),
    (0x0808e05c, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e05c', None),
    (0x0808e0fc, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e0fc', None),
    (0x0808e2c8, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e2c8', None),
    (0x0808e6d0, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e6d0', None),
    (0x0808e82c, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e82c', None),
    (0x0808e8f4, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e8f4', None),
    (0x0808ea1c, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_ea1c', None),
    (0x0808e4cc, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e4cc', None),
    (0x0808e5bc, 0x0201c510, 'gDuelFieldSlots', 'seg5_pool_field_e5bc', None),
]

# =============================================================================
# EQ_SLOTS: gDuelFieldSlotState (0x0201c520) -- 5 slots REUSE
# =============================================================================
FIELD_STATE_SLOTS = [
    (0x0808de40, 0x0201c520, 'gDuelFieldSlotState', 'seg5_pool_fstate_de40', None),
    (0x0808e064, 0x0201c520, 'gDuelFieldSlotState', 'seg5_pool_fstate_e064', None),
    (0x0808e6d4, 0x0201c520, 'gDuelFieldSlotState', 'seg5_pool_fstate_e6d4', None),
    (0x0808e830, 0x0201c520, 'gDuelFieldSlotState', 'seg5_pool_fstate_e830', None),
    (0x0808e8f0, 0x0201c520, 'gDuelFieldSlotState', 'seg5_pool_fstate_e8f0', None),
]

# =============================================================================
# EQ_SLOTS: gEquipEffectZoneBase (0x0201e4f0) -- 7 slots REUSE
# =============================================================================
EQUIP_ZONE_SLOTS = [
    (0x0808d8f8, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_d8f8', None),
    (0x0808d93c, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_d93c', None),
    (0x0808d980, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_d980', None),
    (0x0808d9c4, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_d9c4', None),
    (0x0808da0c, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_da0c', None),
    (0x0808da5c, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_da5c', None),
    (0x0808dae8, 0x0201e4f0, 'gEquipEffectZoneBase', 'seg5_pool_ezbase_dae8', None),
]

# =============================================================================
# EQ_SLOTS: gEquipZoneCountTable (0x0201e1c8) -- 6 slots REUSE
# =============================================================================
EQ_ZONE_CNT_SLOTS = [
    (0x0808df2c, 0x0201e1c8, 'gEquipZoneCountTable', 'seg5_pool_eqzcnt_df2c', None),
    (0x0808e448, 0x0201e1c8, 'gEquipZoneCountTable', 'seg5_pool_eqzcnt_e448', None),
    (0x0808e5b4, 0x0201e1c8, 'gEquipZoneCountTable', 'seg5_pool_eqzcnt_e5b4', None),
    (0x0808e6c4, 0x0201e1c8, 'gEquipZoneCountTable', 'seg5_pool_eqzcnt_e6c4', None),
    (0x0808e720, 0x0201e1c8, 'gEquipZoneCountTable', 'seg5_pool_eqzcnt_e720', None),
    (0x0808ea24, 0x0201e1c8, 'gEquipZoneCountTable', 'seg5_pool_eqzcnt_ea24', None),
]

# =============================================================================
# EQ_SLOTS: Misc EWRAM globals (single-occurrence)
# =============================================================================
MISC_EWRAM_SLOTS = [
    (0x0808dc18, 0x0201c5d8, 'gDuelFieldSlots_p2_base', 'seg5_pool_p2base_dc18', None),
    (0x0808db70, 0x0201b290, 'gDuelPhaseFlags',         'seg5_pool_dpflags_db70', None),
    (0x0808db74, 0x0201b590, 'gEffectEntryArray',       'seg5_pool_effarr_db74', None),
    (0x0808dc30, 0x000010d8, 'ACTIVE_EFFECT_CATEGORY_OFF', 'seg5_pool_aecoff_dc30', None),
    (0x0808e6bc, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'seg5_pool_lplink_e6bc', None),
    (0x0808e6c0, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF',    'seg5_pool_eqcstep_e6c0', None),
    (0x0808e2c0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',    'seg5_pool_lp2off_e2c0', None),
    (0x0808ea14, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',    'seg5_pool_lp2off_ea14', None),
]

# =============================================================================
# EQ_SLOTS: CID / ROM ptr equates
# =============================================================================
CID_SLOTS = [
    # DRAGON_CAPTURE_JAR_CID (REUSE card_info.inc)
    (0x0808e108, 0x000010ef, 'DRAGON_CAPTURE_JAR_CID', 'seg5_pool_cid_dcj_e108', None),
    (0x0808e2d0, 0x000010ef, 'DRAGON_CAPTURE_JAR_CID', 'seg5_pool_cid_dcj_e2d0', None),
    # INSECT_PRINCESS_CID (REUSE card_info.inc)
    (0x0808e104, 0x00001704, 'INSECT_PRINCESS_CID',    'seg5_pool_cid_ins_e104', None),
    (0x0808e2cc, 0x00001704, 'INSECT_PRINCESS_CID',    'seg5_pool_cid_ins_e2cc', None),
    # FINAL_ATTACK_ORDERS_CID (NEW)
    (0x0808e10c, 0x000015fb, 'FINAL_ATTACK_ORDERS_CID', 'seg5_pool_cid_fao_e10c', None),
    (0x0808e2d4, 0x000015fb, 'FINAL_ATTACK_ORDERS_CID', 'seg5_pool_cid_fao_e2d4', None),
    # LEVEL_LIMIT_AREA_B_CID (NEW)
    (0x0808e120, 0x000017a6, 'LEVEL_LIMIT_AREA_B_CID', 'seg5_pool_cid_lla_e120', None),
    (0x0808e2e8, 0x000017a6, 'LEVEL_LIMIT_AREA_B_CID', 'seg5_pool_cid_lla_e2e8', None),
    # LEVEL_LIMIT_AREA_A_CID (NEW)
    (0x0808e124, 0x0000197b, 'LEVEL_LIMIT_AREA_A_CID', 'seg5_pool_cid_llaa_e124', None),
    (0x0808e2ec, 0x0000197b, 'LEVEL_LIMIT_AREA_A_CID', 'seg5_pool_cid_llaa_e2ec', None),
    # cid_12fb (REUSE card_info.inc)
    (0x0808e440, 0x000012fb, 'cid_12fb',               'seg5_pool_cid_12fb_e440', None),
    # MONSTER_REBORN_CID (REUSE)
    (0x0808e444, 0x000012ea, 'MONSTER_REBORN_CID',     'seg5_pool_cid_mrb_e444', None),
    # CHAIN_ENERGY_CID (REUSE)
    (0x0808e5fc, 0x0000132c, 'CHAIN_ENERGY_CID',       'seg5_pool_cid_che_e5fc', None),
    # KOTODAMA_CID (NEW)
    (0x0808e6c8, 0x00001343, 'KOTODAMA_CID',           'seg5_pool_cid_kod_e6c8', None),
    (0x0808e724, 0x00001343, 'KOTODAMA_CID',           'seg5_pool_cid_kod_e724', None),
    (0x0808e744, 0x00001343, 'KOTODAMA_CID',           'seg5_pool_cid_kod_e744', None),
    # FORCED_REQUISITION_CID (REUSE)
    (0x0808e824, 0x00001354, 'FORCED_REQUISITION_CID', 'seg5_pool_cid_frq_e824', None),
    # MAGICAL_THORN_CID (NEW)
    (0x0808e5c0, 0x00001306, 'MAGICAL_THORN_CID',      'seg5_pool_cid_mth_e5c0', None),
    # SKULL_INVITATION_CID (NEW)
    (0x0808ea20, 0x00001361, 'SKULL_INVITATION_CID',   'seg5_pool_cid_ski_ea20', None),
    # MAIDEN_OF_THE_AQUA_CID (NEW)
    (0x0808dc24, 0x000013a2, 'MAIDEN_OF_THE_AQUA_CID', 'seg5_pool_cid_moa_dc24', None),
    # UMI_CARD_ID (REUSE)
    (0x0808dc28, 0x000010f4, 'UMI_CARD_ID',            'seg5_pool_cid_umi_dc28', None),
    # PUMPKING_CID (REUSE)
    (0x0808de38, 0x00001009, 'PUMPKING_CID',           'seg5_pool_cid_pmk_de38', None),
    # CASTLE_OF_DARK_ILLUSIONS_CID (REUSE)
    (0x0808de3c, 0x00000ff9, 'CASTLE_OF_DARK_ILLUSIONS_CID', 'seg5_pool_cid_cdi_de3c', None),
    # gEffectHandlerTable (NEW duel_field.inc)
    (0x0808da8c, 0x09e5a128, 'gEffectHandlerTable',    'seg5_pool_efftbl_da8c', None),
    (0x0808daec, 0x09e5a128, 'gEffectHandlerTable',    'seg5_pool_efftbl_daec', None),
    # gEquipCandidateInitBase (NEW duel_field.inc)
    (0x0808e054, 0x09e3f164, 'gEquipCandidateInitBase', 'seg5_pool_eqci_e054', None),
    # gEquipCandidateScoreBase (NEW duel_field.inc)
    (0x0808e060, 0x09e3f150, 'gEquipCandidateScoreBase', 'seg5_pool_eqcs_e060', None),
    (0x0808e100, 0x09e3f150, 'gEquipCandidateScoreBase', 'seg5_pool_eqcs_e100', None),
    (0x0808e2b8, 0x09e3f150, 'gEquipCandidateScoreBase', 'seg5_pool_eqcs_e2b8', None),
    (0x0808e36c, 0x09e3f150, 'gEquipCandidateScoreBase', 'seg5_pool_eqcs_e36c', None),
    # SLOT_ACTIVE_CHECK_CODE (NEW duel_field.inc)
    (0x0808df30, 0x0000104c, 'SLOT_ACTIVE_CHECK_CODE', 'seg5_pool_sacc_df30', None),
]

# =============================================================================
# RENAME_SLOTS: PTR_gP1LifePoints_ -> ptr_lp_* (14 renames) + switchd_base_d8a8
# NOTE: _rename_label does label rename only, no equate, no REF
# =============================================================================
RENAMES = [
    (0x0808d820, 'PTR_gP1LifePoints_', 'ptr_lp_d820'),
    (0x0808d838, 'PTR_gP1LifePoints_', 'ptr_lp_d838'),
    (0x0808d850, 'PTR_gP1LifePoints_', 'ptr_lp_d850'),
    (0x0808d884, 'PTR_gP1LifePoints_', 'ptr_lp_d884'),
    (0x0808d8fc, 'PTR_gP1LifePoints_', 'ptr_lp_d8fc'),
    (0x0808d940, 'PTR_gP1LifePoints_', 'ptr_lp_d940'),
    (0x0808d984, 'PTR_gP1LifePoints_', 'ptr_lp_d984'),
    (0x0808d9c8, 'PTR_gP1LifePoints_', 'ptr_lp_d9c8'),
    (0x0808da10, 'PTR_gP1LifePoints_', 'ptr_lp_da10'),
    (0x0808dc2c, 'PTR_gP1LifePoints_', 'ptr_lp_dc2c'),
    (0x0808dd50, 'PTR_gP1LifePoints_', 'ptr_lp_dd50'),
    (0x0808e2bc, 'PTR_gP1LifePoints_', 'ptr_lp_e2bc'),
    (0x0808e6b8, 'PTR_gP1LifePoints_', 'ptr_lp_e6b8'),
    (0x0808ea10, 'PTR_gP1LifePoints_', 'ptr_lp_ea10'),
    # switchD jump table base ptr rename
    (0x0808d8a8, 'DAT_', 'switchd_base_d8a8'),
]

# =============================================================================
# PLATE_SLOTS: 12 functions -- C8 stale-FUN_ substitution (ASCII only)
# Full replacement of current plate with current-name version
# =============================================================================
PLATES = [
    # fn04: 0x0808dab0 -- FUN_0810e5d4 -> invoke_r3
    (0x0808dab0,
     'Look up card_id (r1) in ROM effect record table (gEffectHandlerTable=0x09e5a128); read fn ptr at [+4]; call via invoke_r3 (0x0810e5d4) trampoline. Clears gEffectContext+0xc before call; reads that field as return value after. 100+ callsites; central spell/trap effect dispatch entry. r0=u32 player_side [0..1]; r1=u16 card_id [0..0x1fff]. Returns u32 handler_result (from gEffectContext+0xc). Side-effects: gEffectContext+0xc cleared then written by handler. Constants: effect_table=gEffectHandlerTable, gEffectContext=gEquipEffectZoneBase, result_field_offset=0xc.'),
    # fn05: 0x0808daf0 -- FUN_0808fc78 -> scan_card_placement_for_activation; FUN_0808fbd0 -> scan_field_slots_for_archfiend_equip_bitmap_update
    (0x0808daf0,
     'Called by scan_card_placement_for_activation (0x0808fc78) and scan_field_slots_for_archfiend_equip_bitmap_update (0x0808fbd0). Searches gDuelFieldSlots (base=0x0201c510, stride=0x868) for a slot matching r0=player_id, r1=zone_type (bits[5:3]), r2=card_id (bits[14:8]). Inner loop slot 0..count: reads [slot+2] bit0=player, bits[5:3]=zone_type, [slot+4] bits[14:8]=card_id. On match enters second scan via 0x488-offset array. Returns r0=slot_idx (>=0) on hit, r0<0 on miss. Read-only; no external writes. Params: r0=u32 player_id [0..1], r1=u32 zone_type [0..5], r2=u32 card_id [0..0x1fff].'),
    # fn06: 0x0808db90 -- FUN_08090218 -> dispatch_equip_field_scan_sequence; FUN_08032a6c -> count_equip_eligible_slots_both_players; FUN_080454c0 -> enqueue_effect_zone_pair_sprite_scan
    (0x0808db90,
     'Called by dispatch_equip_field_scan_sequence (0x08090218); combines equip-pair state check and sprite refresh. Scans 2 players (base gDuelFieldSlots_p2_base=0x0201c5d8, stride 0x868), for each slot: reads card_id (bits[12:0]), checks [slot+0x8] availability, [slot+0x10] bit1 equip-bind flag. If slot has card and is unbound: calls count_equip_eligible_slots_both_players (0x08032a6c); if >0 records to r12. After loop: if r8==0 (no target), calls classify_card_effect_category; if category differs from [gP1LifePoints+ACTIVE_EFFECT_CATEGORY_OFF], calls enqueue_effect_zone_pair_sprite_scan (0x080454c0). r0=void. Returns u32 stage_done (0=continue, 1=stage complete).'),
    # fn08: 0x0808dd5c -- FUN_08067ea0 -> dispatch_equip_slot_sprite_with_field6_score; FUN_08090218 -> dispatch_equip_field_scan_sequence; FUN_080a0334 -> dispatch_equip_sprite_update_by_slot_icid
    (0x0808dd5c,
     'Called by dispatch_equip_slot_sprite_with_field6_score (0x08067ea0), dispatch_equip_field_scan_sequence (0x08090218), dispatch_equip_sprite_update_by_slot_icid (0x080a0334) (indeg=3). Double loop 2x5 (player [0..1] x slot [0..4]). Per slot: reads gDuelFieldSlots+player*0x868+slot*20, checks card_id==PUMPKING_CID(0x1009); if chain head [+0x8] nonzero: calls count_paired_slots_both_sides(CASTLE_OF_DARK_ILLUSIONS_CID=0x0ff9). If paired>0: reads paired zone, calls enqueue_sprite_attr_for_zone_card_id_lookup + set_field_slot_bit_with_sprite_update + get_equip_card_set_code_for_slot + enqueue_equip_set_slot_sprite_by_zone_col. If paired==0: calls set_field_slot_bit_with_sprite_update + enqueue_equip_slot_sprite_attr. Returns r0=u32 updated_flag (0=none, 1=at least one slot updated).'),
    # fn10: 0x0808df3c -- FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808df3c,
     'Called by dispatch_equip_field_scan_sequence (0x08090218) (indeg=1). Initializes 10-word work buf from gEquipCandidateInitBase (0x09e3f164) template; then 2x10 double loop (player [0..1] x slot [0..9]) over gDuelFieldSlots+player*0x868. Per slot: reads card_id bits[18:0]; calls find_effect_record_index_by_id; on match reads fn_ptr[+4] and calls it; tracks max ATK from gEquipCandidateScoreBase (0x09e3f150); on match calls apply_equip_activation_with_id_lookup. Returns void.'),
    # fn11: 0x0808e370 -- FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808e370,
     'Called by dispatch_equip_field_scan_sequence (0x08090218) (indeg=1). Scans gDuelFieldSlots for field spell eligible slots: count_field_copies_of_card(cid_12fb=0x12fb); check_value_in_slot_chain(MONSTER_REBORN_CID=0x12ea). Builds eligible bitmap; calls prepare_equip_slot_ctx. Uses gEquipCandidateScoreBase (0x09e3f150). Returns void.'),
    # fn12: 0x0808e45c -- FUN_080440b8 -> dispatch_equip_zone_sprite_and_activation
    (0x0808e45c,
     'Called by dispatch_equip_zone_sprite_and_activation (0x080440b8) (indeg=1). Scans trap zone slots 5..9 over gDuelFieldSlots; state filter mask 0x98300000; bit5/bit1 mvns AND filter; calls enqueue_sprite_attr_with_shape for matching slots. Returns void.'),
    # fn13: 0x0808e4d8 -- FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808e4d8,
     'Called by dispatch_equip_field_scan_sequence (0x08090218) (indeg=1). 2x9 loop over gDuelFieldSlots; state==SKULL_INVITATION_CID (0x1361) filter; calls enqueue_sprite_attr_with_xy_split; calls submit_lp_change_indicator_with_chain_check (opponent side). Returns void.'),
    # fn14: 0x0808e5c4 -- FUN_0804a334 -> render_monster_slot_card_with_lp_bar; FUN_08095ca0 -> trigger_lp_bar_animation_if_ready; FUN_080abbd8 -> init_equip_slot_entry_with_copy_flag_sprite; FUN_080abe54 -> init_equip_slot_entry_with_placement_type_check
    (0x0808e5c4,
     'Called by render_monster_slot_card_with_lp_bar (0x0804a334), trigger_lp_bar_animation_if_ready (0x08095ca0), init_equip_slot_entry_with_copy_flag_sprite (0x080abbd8), init_equip_slot_entry_with_placement_type_check (0x080abe54). count_field_copies_of_card(CHAIN_ENERGY_CID=0x132c); calls enqueue_sprite_attr_by_sign + enqueue_sprite_attr_clamped in a loop. Returns void.'),
    # fn16: 0x0808e770 -- FUN_080440b8 -> dispatch_equip_zone_sprite_and_activation
    (0x0808e770,
     'Called by dispatch_equip_zone_sprite_and_activation (0x080440b8) (indeg=1). count_available_effect_zones(FORCED_REQUISITION_CID=0x1354); scans slots 5..10 over gDuelFieldSlots; bit4==0: set_bit+enqueue_xy+apply_activation; bit4!=0: enqueue_sprite_attr_with_shape. Returns void.'),
    # fn17: 0x0808e85c -- multiple FUN_ -> current names
    (0x0808e85c,
     'Called by dispatch_equip_zone_sprite_and_activation (0x080440b8), handle_card_effect_zone_eligibility_by_field6 (0x08047218), render_slot_card_sprite_from_descriptor (0x08047f50), render_slot_card_sprite_and_effects (0x08048020), render_slot_card_sprite_with_chaos_equip_check (0x08048364). 2x5 loop slots 5..9 over gDuelFieldSlots; state mask 0x9b080000; bit5/bit1 filter; calls enqueue_sprite_attr_with_shape. Returns void.'),
    # fn18: 0x0808e8fc -- FUN_08090218 -> dispatch_equip_field_scan_sequence
    (0x0808e8fc,
     'Called by dispatch_equip_field_scan_sequence (0x08090218) (indeg=1). 2x9 loop over gDuelFieldSlots; SKULL_INVITATION_CID (0x1361) filter; calls enqueue_sprite_attr_with_xy_split; equip bitmap; calls submit_lp_change_indicator x2 (own+eors). Returns void.'),
]


def main():
    fail_count = 0

    if DRY:
        print("DRY RUN -- RefineF11Seg5Slots [0x0808d7f4..0x0808e8fc):")
        total_eq = (len(LP_PTR_SLOTS) + len(STRIDE_SLOTS) + len(FIELD_SLOTS_SLOTS) +
                    len(FIELD_STATE_SLOTS) + len(EQUIP_ZONE_SLOTS) + len(EQ_ZONE_CNT_SLOTS) +
                    len(MISC_EWRAM_SLOTS) + len(CID_SLOTS))
        print("  EQ total: %d" % total_eq)
        print("  RENAME: %d" % len(RENAMES))
        print("  PLATE: %d" % len(PLATES))
        for s in LP_PTR_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in STRIDE_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in FIELD_SLOTS_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in FIELD_STATE_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in EQUIP_ZONE_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in EQ_ZONE_CNT_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in MISC_EWRAM_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in CID_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for r in RENAMES:
            _rename_label(r[0], r[1], r[2])
        for p in PLATES:
            _apply_plate(p[0], p[1])
        return

    print("=== RefineF11Seg5Slots [0x0808d7f4..0x0808e8fc) ===")

    # Step 1: LP PTR equates (also renames happen in RENAMES step)
    print("--- LP PTR EQ (%d slots) ---" % len(LP_PTR_SLOTS))
    for s in LP_PTR_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 2: PLAYER_BLOCK_STRIDE EQ + mixed stride-group slots
    print("--- PLAYER_BLOCK_STRIDE / gDuelFieldSlots stride-group EQ (%d slots) ---" % len(STRIDE_SLOTS))
    for s in STRIDE_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 3: gDuelFieldSlots remaining EQ
    print("--- gDuelFieldSlots EQ (%d slots) ---" % len(FIELD_SLOTS_SLOTS))
    for s in FIELD_SLOTS_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 4: gDuelFieldSlotState EQ
    print("--- gDuelFieldSlotState EQ (%d slots) ---" % len(FIELD_STATE_SLOTS))
    for s in FIELD_STATE_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 5: gEquipEffectZoneBase EQ
    print("--- gEquipEffectZoneBase EQ (%d slots) ---" % len(EQUIP_ZONE_SLOTS))
    for s in EQUIP_ZONE_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 6: gEquipZoneCountTable EQ
    print("--- gEquipZoneCountTable EQ (%d slots) ---" % len(EQ_ZONE_CNT_SLOTS))
    for s in EQ_ZONE_CNT_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 7: Misc EWRAM EQ
    print("--- Misc EWRAM EQ (%d slots) ---" % len(MISC_EWRAM_SLOTS))
    for s in MISC_EWRAM_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 8: CID / ROM ptr EQ
    print("--- CID/ROM ptr EQ (%d slots) ---" % len(CID_SLOTS))
    for s in CID_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 9: RENAME (PTR_gP1LifePoints_ -> ptr_lp_* + switchd_base_d8a8)
    print("--- RENAME (%d) ---" % len(RENAMES))
    for r in RENAMES:
        if not _rename_label(r[0], r[1], r[2]):
            fail_count += 1

    # Step 10: PLATE (12 functions C8 stale-FUN_ subst)
    print("--- PLATE (%d) ---" % len(PLATES))
    for p in PLATES:
        if not _apply_plate(p[0], p[1]):
            fail_count += 1

    total_eq = (len(LP_PTR_SLOTS) + len(STRIDE_SLOTS) + len(FIELD_SLOTS_SLOTS) +
                len(FIELD_STATE_SLOTS) + len(EQUIP_ZONE_SLOTS) + len(EQ_ZONE_CNT_SLOTS) +
                len(MISC_EWRAM_SLOTS) + len(CID_SLOTS))
    print("")
    print("=== RefineF11Seg5Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE=%d" % (total_eq, len(RENAMES), len(PLATES)))
    if fail_count > 0:
        print("  FAIL_COUNT=%d (review above FAIL lines)" % fail_count)
    else:
        print("  FAIL_COUNT=0 -- all OK")


main()
