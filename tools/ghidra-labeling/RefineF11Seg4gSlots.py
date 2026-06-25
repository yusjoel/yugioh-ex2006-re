# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4gSlots.py -- f11 Seg-4g slot symbolization [0x0808cabc..0x0808d7f4)
#
# 20 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ: PLAYER_BLOCK_STRIDE (0x868) slots x21
#     + CID pool values (5 NEW + 3 REUSE + 2 REUSE misc) x10
#     + CARD_FIELD_STAT_CLEAR_UPPER4_MASK (0x0fffffff, NEW) x1
#     + slot_field_mask_ffff803f (REUSE) x1
#     + CARD_FIELD3_THRESHOLD_1500 (REUSE) x1
#     + PARASITE_PARACIDE_CID (REUSE) x3
#     + SLOT_CARD_SET_CODE_MASK (REUSE) x1
#     + NECROVALLEY_CID (REUSE) x1
# REF=63 (EWRAM pointer pool slots):
#   gP1LifePoints x17, PLAYER_BLOCK_STRIDE-as-ref? No, PLAYER_BLOCK_STRIDE is EQ
#   gP1HandSlotArray x7, gP1SlotSetCodeArray x8, gP1HandCountBase x3,
#   gP1FieldArrayCBase x4, gDuelFieldSlots x1, gEquipEffectZoneBase x2,
#   gP1SlotCountBase x1, gP1FieldArrayCBase already counted
# RENAME=20
# PLATE=20 (full ASCII plate comments, all <= 500 chars)
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
# EQ_SLOTS: PLAYER_BLOCK_STRIDE (0x868) -- 21 slots
# =============================================================================
STRIDE_SLOTS = [
    (0x0808cb4c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_level_modulation_substate_e_pool_stride', None),    # fn01
    (0x0808cbcc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_water_dragon_substate_e_pool_stride', None),         # fn02
    (0x0808cc54, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_scarr_dark_world_substate_d_pool_stride', None),     # fn03
    (0x0808ccb0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_pot_of_avarice_substate_e_pool_stride', None),       # fn04
    (0x0808cd2c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_boss_rush_substate_d_pool_stride', None),            # fn05
    (0x0808cdb8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_gateway_dark_world_substate_e_pool_stride', None),   # fn06
    (0x0808ce34, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_forces_of_darkness_substate_e_pool_stride', None),   # fn07
    (0x0808cea4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_roll_out_substate_e_pool_stride_a', None),           # fn08 pool1
    (0x0808cf28, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_roll_out_substate_e_pool_stride_b', None),           # fn08 pool2a
    (0x0808cf80, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_roll_out_substate_e_pool_stride_c', None),           # fn08 pool2b
    (0x0808d008, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_armed_changer_substate_e_b_pool_stride_a', None),    # fn09 pool1
    (0x0808d04c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_armed_changer_substate_e_b_pool_stride_b', None),    # fn09 pool2
    (0x0808d1a8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_inferno_reckless_summon_substate_d_e_b_pool_stride', None),  # fn11
    (0x0808d220, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_white_horns_dragon_substate_e_pool_stride', None),   # fn12
    (0x0808d28c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_magnet_circle_lv2_substate_b_pool_stride', None),    # fn13
    (0x0808d31c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_ancient_gear_drill_substate_d_pool_stride', None),   # fn14
    (0x0808d3cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_damage_condenser_substate_d_pool_stride', None),     # fn15
    (0x0808d480, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_gokipon_substate_d_pool_stride', None),              # fn16
    (0x0808d5a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_symbol_of_heritage_substate_e_pool_stride', None),   # fn17
    (0x0808d688, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_generation_shift_substate_d_c_pool_stride', None),   # fn18
    (0x0808d6f8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_zone_flute_summoning_kuriboh_substate_d_pool_stride', None),  # fn19
]

# =============================================================================
# EQ_SLOTS: CID pool equates -- 10 slots (5 NEW + 5 REUSE)
# =============================================================================
CID_SLOTS = [
    # fn03 -- SCARR_DARK_WORLD_CID (NEW)
    # (no pool CID slot for fn03; CID used in dispatch table but not in literal pool)
    # fn11 -- NECROVALLEY_CID (REUSE card_info.inc:297)
    (0x0808d1b0, 0x0000159d, 'NECROVALLEY_CID',
     'scan_zone_inferno_reckless_summon_substate_d_e_b_pool_159d',
     'NECROVALLEY_CID=0x159d gate check fn11'),
    # fn15 -- PARASITE_PARACIDE_CID (REUSE)
    (0x0808d3d4, 0x000012a1, 'PARASITE_PARACIDE_CID',
     'scan_zone_damage_condenser_substate_d_pool_12a1',
     'PARASITE_PARACIDE_CID=0x12a1 find_effect_node_in_zone fn15'),
    # fn16 -- CARD_FIELD3_THRESHOLD_1500 (REUSE)
    (0x0808d488, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500',
     'scan_zone_gokipon_substate_d_pool_5dc',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc (1500) ATK threshold fn16'),
    # fn16 -- PARASITE_PARACIDE_CID (REUSE)
    (0x0808d48c, 0x000012a1, 'PARASITE_PARACIDE_CID',
     'scan_zone_gokipon_substate_d_pool_12a1',
     'PARASITE_PARACIDE_CID=0x12a1 find_effect_node_in_zone fn16'),
    # fn18 -- PARASITE_PARACIDE_CID (REUSE)
    (0x0808d690, 0x000012a1, 'PARASITE_PARACIDE_CID',
     'scan_zone_generation_shift_substate_d_c_pool_12a1',
     'PARASITE_PARACIDE_CID=0x12a1 find_effect_node_in_zone fn18'),
    # fn19 -- WINGED_KURIBOH_CID (NEW)
    (0x0808d700, 0x000018aa, 'WINGED_KURIBOH_CID',
     'scan_zone_flute_summoning_kuriboh_substate_d_pool_18aa',
     'WINGED_KURIBOH_CID=0x18aa gate fn19 flute_summoning_kuriboh'),
    # fn20 -- SLOT_CARD_SET_CODE_MASK (REUSE)
    (0x0808d7dc, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',
     'scan_zone_group_handler_multi_card_pool_1fff',
     'SLOT_CARD_SET_CODE_MASK=0x1fff fn20 set-code filter'),
]

# =============================================================================
# EQ_SLOTS: CARD_FIELD_STAT_CLEAR_UPPER4_MASK (0x0fffffff) -- 1 slot (NEW)
# =============================================================================
MASK_SLOTS = [
    (0x0808d00c, 0x0fffffff, 'CARD_FIELD_STAT_CLEAR_UPPER4_MASK',
     'scan_zone_armed_changer_substate_e_b_pool_mask',
     'CARD_FIELD_STAT_CLEAR_UPPER4_MASK=0x0fffffff clear upper4 bits field3 fn09'),
]

# =============================================================================
# EQ_SLOTS: slot_field_mask_ffff803f (0xffff803f) -- 1 slot (REUSE)
# =============================================================================
SLOT_MASK_SLOTS = [
    (0x0808cf30, 0xffff803f, 'slot_field_mask_ffff803f',
     'scan_zone_roll_out_substate_e_pool_mask',
     'slot_field_mask_ffff803f=0xffff803f hand slot field gate fn08'),
]

# =============================================================================
# REF_SLOTS: EWRAM pointer pool slots (63 total)
# Format: (slot_addr, target_val, gas_label, slot_label)
# =============================================================================
REF_SLOTS = [
    # fn01 (0x0808cabc) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ), gP1HandCountBase
    (0x0808cb48, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_level_modulation_substate_e_pool_lp'),
    (0x0808cb50, 0x0201c4f4, 'gP1HandCountBase',   'scan_zone_level_modulation_substate_e_pool_handcnt'),
    # fn02 (0x0808cb54) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ), gP1HandSlotArray
    (0x0808cbc8, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_water_dragon_substate_e_pool_lp'),
    (0x0808cbd0, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_water_dragon_substate_e_pool_hand'),
    # fn03 (0x0808cbd4) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ), gP1SlotSetCodeArray
    (0x0808cc50, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_scarr_dark_world_substate_d_pool_lp'),
    (0x0808cc58, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_scarr_dark_world_substate_d_pool_setcode'),
    # fn04 (0x0808cc5c) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ)
    (0x0808ccac, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_pot_of_avarice_substate_e_pool_lp'),
    # fn05 (0x0808ccb4) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ), gP1SlotSetCodeArray
    (0x0808cd28, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_boss_rush_substate_d_pool_lp'),
    (0x0808cd30, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_boss_rush_substate_d_pool_setcode'),
    # fn06 (0x0808cd34) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ), gP1HandSlotArray
    (0x0808cdb4, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_gateway_dark_world_substate_e_pool_lp'),
    (0x0808cdbc, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_gateway_dark_world_substate_e_pool_hand'),
    # fn07 (0x0808cdc0) -- gP1LifePoints, PLAYER_BLOCK_STRIDE (EQ), gP1HandSlotArray
    (0x0808ce30, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_forces_of_darkness_substate_e_pool_lp'),
    (0x0808ce38, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_forces_of_darkness_substate_e_pool_hand'),
    # fn08 (0x0808ce3c) -- pool1: PLAYER_BLOCK_STRIDE(EQ), gDuelFieldSlots
    #                      pool2: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1HandSlotArray, slot_field_mask(EQ), PLAYER_BLOCK_STRIDE(EQ), gP1HandCountBase
    (0x0808cea8, 0x0201c510, 'gDuelFieldSlots',    'scan_zone_roll_out_substate_e_pool_field'),
    (0x0808cf24, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_roll_out_substate_e_pool_lp'),
    (0x0808cf2c, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_roll_out_substate_e_pool_hand'),
    (0x0808cf84, 0x0201c4f4, 'gP1HandCountBase',   'scan_zone_roll_out_substate_e_pool_handcnt'),
    # fn09 (0x0808cf88) -- pool1: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), mask(EQ), gP1HandSlotArray
    #                      pool2: PLAYER_BLOCK_STRIDE(EQ), gP1FieldArrayCBase
    (0x0808d004, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_armed_changer_substate_e_b_pool_lp'),
    (0x0808d010, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_armed_changer_substate_e_b_pool_hand'),
    (0x0808d050, 0x0201c600, 'gP1FieldArrayCBase', 'scan_zone_armed_changer_substate_e_b_pool_field'),
    # fn10 (0x0808d054) -- no pool slots (12B stub)
    # fn11 (0x0808d060) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1SlotSetCodeArray, NECROVALLEY_CID(EQ), gP1HandSlotArray, gP1FieldArrayCBase
    (0x0808d1a4, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_inferno_reckless_summon_substate_d_e_b_pool_lp'),
    (0x0808d1ac, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_inferno_reckless_summon_substate_d_e_b_pool_setcode'),
    (0x0808d1b4, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_inferno_reckless_summon_substate_d_e_b_pool_hand'),
    (0x0808d1b8, 0x0201c600, 'gP1FieldArrayCBase', 'scan_zone_inferno_reckless_summon_substate_d_e_b_pool_field'),
    # fn12 (0x0808d1bc) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ)
    (0x0808d21c, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_white_horns_dragon_substate_e_pool_lp'),
    # fn13 (0x0808d224) -- pool: PLAYER_BLOCK_STRIDE(EQ), gP1FieldArrayCBase
    (0x0808d290, 0x0201c600, 'gP1FieldArrayCBase', 'scan_zone_magnet_circle_lv2_substate_b_pool_field'),
    # fn14 (0x0808d294) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1SlotSetCodeArray
    (0x0808d318, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_ancient_gear_drill_substate_d_pool_lp'),
    (0x0808d320, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_ancient_gear_drill_substate_d_pool_setcode'),
    # fn15 (0x0808d324) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1SlotSetCodeArray, PARASITE(EQ)
    (0x0808d3c8, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_damage_condenser_substate_d_pool_lp'),
    (0x0808d3d0, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_damage_condenser_substate_d_pool_setcode'),
    # fn16 (0x0808d3d8) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1SlotSetCodeArray, thresh(EQ), PARASITE(EQ), gP1SlotCountBase
    (0x0808d47c, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_gokipon_substate_d_pool_lp'),
    (0x0808d484, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_gokipon_substate_d_pool_setcode'),
    (0x0808d490, 0x0201c4f0, 'gP1SlotCountBase',   'scan_zone_gokipon_substate_d_pool_slotcnt'),
    # fn17 (0x0808d494) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1HandSlotArray, gP1HandCountBase
    (0x0808d5a0, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_symbol_of_heritage_substate_e_pool_lp'),
    (0x0808d5a8, 0x0201c8f8, 'gP1HandSlotArray',   'scan_zone_symbol_of_heritage_substate_e_pool_hand'),
    (0x0808d5ac, 0x0201c4f4, 'gP1HandCountBase',   'scan_zone_symbol_of_heritage_substate_e_pool_handcnt'),
    # fn18 (0x0808d5b0) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1SlotSetCodeArray, PARASITE(EQ)
    (0x0808d684, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_generation_shift_substate_d_c_pool_lp'),
    (0x0808d68c, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_generation_shift_substate_d_c_pool_setcode'),
    # fn19 (0x0808d694) -- pool: gP1LifePoints, PLAYER_BLOCK_STRIDE(EQ), gP1SlotSetCodeArray, WINGED_KURIBOH(EQ)
    (0x0808d6f4, 0x0201c4e0, 'gP1LifePoints',      'scan_zone_flute_summoning_kuriboh_substate_d_pool_lp'),
    (0x0808d6fc, 0x0201c740, 'gP1SlotSetCodeArray', 'scan_zone_flute_summoning_kuriboh_substate_d_pool_setcode'),
    # fn20 (0x0808d704) -- pool1: gEquipEffectZoneBase; pool2: SLOT_CARD_SET_CODE_MASK(EQ), gEquipEffectZoneBase
    (0x0808d7a0, 0x0201e4f0, 'gEquipEffectZoneBase', 'scan_zone_group_handler_multi_card_pool_zonebas_a'),
    (0x0808d7e0, 0x0201e4f0, 'gEquipEffectZoneBase', 'scan_zone_group_handler_multi_card_pool_zonebas_b'),
]

# =============================================================================
# FUNC_RENAME: 20 functions (currently FUN_0808xxxx after disasm)
# =============================================================================
FUNC_RENAMES = [
    (0x0808cabc, 'scan_zone_level_modulation_substate_e'),
    (0x0808cb54, 'scan_zone_water_dragon_substate_e'),
    (0x0808cbd4, 'scan_zone_scarr_dark_world_substate_d'),
    (0x0808cc5c, 'scan_zone_pot_of_avarice_substate_e'),
    (0x0808ccb4, 'scan_zone_boss_rush_substate_d'),
    (0x0808cd34, 'scan_zone_gateway_dark_world_substate_e'),
    (0x0808cdc0, 'scan_zone_forces_of_darkness_substate_e'),
    (0x0808ce3c, 'scan_zone_roll_out_substate_e'),
    (0x0808cf88, 'scan_zone_armed_changer_substate_e_b'),
    (0x0808d054, 'scan_zone_magical_mallet_substate_b'),
    (0x0808d060, 'scan_zone_inferno_reckless_summon_substate_d_e_b'),
    (0x0808d1bc, 'scan_zone_white_horns_dragon_substate_e'),
    (0x0808d224, 'scan_zone_magnet_circle_lv2_substate_b'),
    (0x0808d294, 'scan_zone_ancient_gear_drill_substate_d'),
    (0x0808d324, 'scan_zone_damage_condenser_substate_d'),
    (0x0808d3d8, 'scan_zone_gokipon_substate_d'),
    (0x0808d494, 'scan_zone_symbol_of_heritage_substate_e'),
    (0x0808d5b0, 'scan_zone_generation_shift_substate_d_c'),
    (0x0808d694, 'scan_zone_flute_summoning_kuriboh_substate_d'),
    (0x0808d704, 'scan_zone_group_handler_multi_card'),
]

# =============================================================================
# PLATE: 20 ASCII plate comments (all <= 500 chars)
# =============================================================================
PLATES = [
    (0x0808cabc,
     'Equip zone scan for Level Modulation (LEVEL_MODULATION_CID=0x1944). Hand loop via gP1LifePoints+gP1HandCountBase+gP1HandSlotArray; gate: check_equip_placement_eligible_from_slot_record (0x080313b8)+check_card_id_is_effect_monster_type_b (0x0804b0e4). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1944].'),
    (0x0808cb54,
     'Equip zone scan for Water Dragon (WATER_DRAGON_CID=0x1951). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_zone_slot_equip_eligible (0x08037434). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1951].'),
    (0x0808cbd4,
     'Equip zone scan for Scarr, Scout of Dark World (SCARR_DARK_WORLD_CID=0x196a). SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c)+get_card_extended_stat_field5 (0x080eee50). write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x196a].'),
    (0x0808cc5c,
     'Equip zone scan for Pot of Avarice (POT_OF_AVARICE_CID=0x196f). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: check_equip_placement_eligible_from_slot_record (0x080313b8). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x196f].'),
    (0x0808ccb4,
     'Equip zone scan for Boss Rush (BOSS_RUSH_CID=0x1972). SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: check_card_id_is_bes_type (0x0804b2dc)+eval_equip_placement_full_check (0x0803bba4). write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x1972].'),
    (0x0808cd34,
     'Equip zone scan for Gateway to Dark World (GATEWAY_DARK_WORLD_CID=0x1973). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c)+check_zone_slot_equip_eligible (0x08037434). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1973].'),
    (0x0808cdc0,
     'Equip zone scan for Forces of Darkness (FORCES_OF_DARKNESS_CID=0x1974). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1974].'),
    (0x0808ce3c,
     'Equip zone scan for Roll Out! (ROLL_OUT_CID=0x1979). Phase1: scan gDuelFieldSlots+PLAYER_BLOCK_STRIDE via memset (0x0810e9bc)+check_card_stat_field8_is_8 (0x0804ae2c)+check_slot_card_eligible_by_card_id (0x0804f6c4). Phase2: hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray+slot_field_mask_ffff803f. write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1979].'),
    (0x0808cf88,
     'Equip zone scan for Armed Changer (ARMED_CHANGER_CID=0x197c). Two writes: (1) hand via gP1HandSlotArray+check_card_field5_is_nonzero (0x0804ad48)+get_card_extended_stat_field3_raw (0x080eef44)+CARD_FIELD_STAT_CLEAR_UPPER4_MASK gate; write substate_e. (2) field via gP1FieldArrayCBase+get_card_extended_stat_field9 (0x080eee7c)+CMP r0,#3 gate; write substate_b. Dispatch table entry [CID 0x197c].'),
    (0x0808d054,
     'Equip zone scan for Magical Mallet (MAGICAL_MALLET_CID=0x198d). Stub: push{lr}; MOVS r1,#0xb; BL write_equip_zone_entry_by_substate (0x0808d88c); pop{r0};bx r0. write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x198d].'),
    (0x0808d060,
     'Equip zone scan for Inferno Reckless Summon (INFERNO_RECKLESS_SUMMON_CID=0x198e). Three loops: (1) monster via gP1SlotSetCodeArray+PLAYER_BLOCK_STRIDE; gate: NECROVALLEY_CID+count_field_copies_of_card (0x0803279c)+check_card_pair_allowed (0x0804ab4c)+eval_equip_placement_full_check (0x0803bba4); write substate_d. (2) hand via gP1HandSlotArray+check_zone_slot_equip_eligible (0x08037434); write substate_e. (3) field via gP1FieldArrayCBase; write substate_b. Dispatch table entry [CID 0x198e].'),
    (0x0808d1bc,
     'Equip zone scan for White Horns Dragon (WHITE_HORNS_DRAGON_CID=0x1996). Monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: get_card_extended_stat_field6 (race=0x16 Zombie check). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1996].'),
    (0x0808d224,
     'Equip zone scan for Magnet Circle LV2 (MAGNET_CIRCLE_LV2_CID=0x19ac). Field array via gP1FieldArrayCBase+PLAYER_BLOCK_STRIDE; gate: get_card_extended_stat_field6 (0x080eedf8)+eval_equip_bonus_for_slot (0x080377b0)+eval_equip_placement_full_check (0x0803bba4). write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x19ac].'),
    (0x0808d294,
     'Equip zone scan for Ancient Gear Drill (ANCIENT_GEAR_DRILL_CID=0x19ae). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (0x080eedf8)+check_field_spell_b_placeable (0x080309fc)+find_first_available_monster_slot_for_player (0x08033bf4)+get_card_extended_stat_field9 (0x080eee7c). write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19ae].'),
    (0x0808d324,
     'Equip zone scan for Damage Condenser (DAMAGE_CONDENSER_CID=0x19b6). SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: get_card_extended_stat_field3_raw (0x080eef44)+eval_equip_placement_full_check (0x0803bba4)+find_effect_node_in_zone (0x0802fd60). PARASITE_PARACIDE_CID pool slot. write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19b6].'),
    (0x0808d3d8,
     'Equip zone scan for Gokipon (GOKIPON_CID=0x19c5). SlotSetCode monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (race, x2)+get_card_extended_stat_field3_raw+find_effect_node_in_zone (0x0802fd60). Pool: CARD_FIELD3_THRESHOLD_1500+PARASITE_PARACIDE_CID+gP1SlotCountBase. write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19c5].'),
    (0x0808d494,
     'Equip zone scan for Symbol of Heritage (SYMBOL_OF_HERITAGE_CID=0x19d7). Multi-loop: hand (gP1HandSlotArray+gP1HandCountBase+PLAYER_BLOCK_STRIDE x2) and monster (gP1LifePoints+PLAYER_BLOCK_STRIDE). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x19d7].'),
    (0x0808d5b0,
     'Equip zone scan for Generation Shift+Next to be Lost (GENERATION_SHIFT_CID=0x19dd/NEXT_TO_BE_LOST_CID=0x19dc). Loop1: monster via gP1LifePoints+gP1SlotSetCodeArray+find_effect_node_in_zone (0x0802fd60)+PARASITE_PARACIDE_CID; write substate_d. Loop2: SlotSetCode via gP1SlotSetCodeArray+PLAYER_BLOCK_STRIDE; write substate_c. Dispatch table entries [CID 0x19dc, CID 0x19dd].'),
    (0x0808d694,
     'Equip zone scan for Flute of Summoning Kuriboh (FLUTE_SUMMONING_KURIBOH_CID=0x19ec). SlotSetCode monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: WINGED_KURIBOH_CID=0x18aa check. write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19ec].'),
    (0x0808d704,
     'Equip zone scan group handler (CID=0xfffe sentinel). r8=arg2=substate (variable). Phase1: collect eligible slots via scan_card_type_effect_handler_table (0x08097114) loop into stack buf. Phase2: per buf slot call read_player_field_slot_word_by_zone (0x0803b738)+get_zone_slot_entity_ref_by_type (0x0803b3a8). write_equip_zone_entry_by_substate(player_id, r8, slot_idx). Pool: gEquipEffectZoneBase (x2)+SLOT_CARD_SET_CODE_MASK. Dispatch table entry [CID 0xfffe].'),
]


def main():
    if DRY:
        print("DRY RUN -- RefineF11Seg4gSlots:")
        print("  PLAYER_BLOCK_STRIDE EQ slots: %d" % len(STRIDE_SLOTS))
        print("  CID/misc EQ slots: %d" % (len(CID_SLOTS) + len(MASK_SLOTS) + len(SLOT_MASK_SLOTS)))
        print("  REF slots: %d" % len(REF_SLOTS))
        print("  FUNC_RENAME: %d" % len(FUNC_RENAMES))
        print("  PLATE: %d" % len(PLATES))
        fail = 0
        for s in STRIDE_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3])
        for s in CID_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3], s[4])
        for s in MASK_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3], s[4])
        for s in SLOT_MASK_SLOTS:
            _apply_eq(s[0], s[1], s[2], s[3], s[4])
        for s in REF_SLOTS:
            _apply_ref(s[0], s[1], s[2], s[3])
        for s in FUNC_RENAMES:
            _func_rename(s[0], s[1])
        for s in PLATES:
            _apply_plate(s[0], s[1])
        return

    print("=== RefineF11Seg4gSlots [0x0808cabc..0x0808d7f4) ===")

    fail_count = 0

    # Step 1: PLAYER_BLOCK_STRIDE EQ slots
    print("--- PLAYER_BLOCK_STRIDE EQ (%d slots) ---" % len(STRIDE_SLOTS))
    for s in STRIDE_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3], None if len(s) < 5 else s[4]):
            fail_count += 1

    # Step 2: CID/misc EQ slots
    print("--- CID/misc EQ (%d slots) ---" % (len(CID_SLOTS) + len(MASK_SLOTS) + len(SLOT_MASK_SLOTS)))
    for s in CID_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3], s[4]):
            fail_count += 1
    for s in MASK_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3], s[4]):
            fail_count += 1
    for s in SLOT_MASK_SLOTS:
        if not _apply_eq(s[0], s[1], s[2], s[3], s[4]):
            fail_count += 1

    # Step 3: REF slots
    print("--- REF slots (%d) ---" % len(REF_SLOTS))
    for s in REF_SLOTS:
        if not _apply_ref(s[0], s[1], s[2], s[3]):
            fail_count += 1

    # Step 4: FUNC_RENAME
    print("--- FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))
    for s in FUNC_RENAMES:
        if not _func_rename(s[0], s[1]):
            fail_count += 1

    # Step 5: PLATE
    print("--- PLATE (%d) ---" % len(PLATES))
    for s in PLATES:
        if not _apply_plate(s[0], s[1]):
            fail_count += 1

    print("")
    print("=== RefineF11Seg4gSlots DONE ===")
    print("  EQ_stride=%d  EQ_cid_misc=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(STRIDE_SLOTS),
        len(CID_SLOTS) + len(MASK_SLOTS) + len(SLOT_MASK_SLOTS),
        len(REF_SLOTS),
        len(FUNC_RENAMES),
        len(PLATES)))
    if fail_count > 0:
        print("  FAIL_COUNT=%d (review above FAIL lines)" % fail_count)
    else:
        print("  FAIL_COUNT=0 -- all OK")


main()
