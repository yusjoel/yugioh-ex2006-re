# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4dSlots.py -- f11 Seg-4d slot symbolization [0x0808a2ac..0x0808ad8c)
#
# 24 named functions (equip zone scan callbacks); all dispatched via table 0x09e5a128
#
# EQ: PLAYER_BLOCK_STRIDE (0x868) slots x25
#     + CID pool values (REUSE or NEW from card_info.inc)
#     + fn24 raw mask slot (0xffff803f, no named constant)
# REF=34 (EWRAM pointer pool slots -- createDWordWithRef):
#   gP1LifePoints x22, gP1FieldArrayCBase x3, gP1HandSlotArray x5,
#   gP1SlotSetCodeArray x2, gP1AltHandSlotArray x1, gP1HandCountBase x1
# FUNC_RENAME=24 (re-apply proposed names for safety)
# PLATE=24 (full ASCII plate comments, all <= 500 chars)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: WARN=FAIL: any failed setComment or value mismatch = FAIL.
# NOTE: fn20 pool corrected: PLAYER_BLOCK_STRIDE at 0x0808ab94 (not 0x0808ab92 -- alignment gap).

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
    (0x0808a370, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a370', None),  # fn01
    (0x0808a3b4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a3b4', None),  # fn02
    (0x0808a3e4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a3e4', None),  # fn03
    (0x0808a43c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a43c', None),  # fn04
    (0x0808a494, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a494', None),  # fn05
    (0x0808a4e8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a4e8', None),  # fn06
    (0x0808a540, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a540', None),  # fn07 loop1
    (0x0808a594, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a594', None),  # fn07 loop2
    (0x0808a5ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a5ec', None),  # fn08
    (0x0808a674, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a674', None),  # fn09
    (0x0808a700, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a700', None),  # fn10
    (0x0808a780, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a780', None),  # fn11
    (0x0808a838, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a838', None),  # fn12
    (0x0808a890, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a890', None),  # fn13
    (0x0808a918, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a918', None),  # fn14
    (0x0808a974, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a974', None),  # fn15 (pool literal, weak entry)
    (0x0808a9b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8a9b0', None),  # fn16
    (0x0808aa30, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8aa30', None),  # fn17
    (0x0808aaac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8aaac', None),  # fn18
    (0x0808ab38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ab38', None),  # fn19
    (0x0808ab94, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ab94', None),  # fn20 (corrected from 0x0808ab92)
    (0x0808abf0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8abf0', None),  # fn21
    (0x0808ac40, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ac40', None),  # fn22
    (0x0808ac9c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ac9c', None),  # fn23
    (0x0808ad7c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'stride_8ad7c', None),  # fn24
]

# =============================================================================
# EQ_SLOTS: CID pool values
# =============================================================================
# Partner CID slots in fn01: EMBLEM_OF_DRAGON_DESTROYER_CID, BUSTER_BLADER_CID, NECROVALLEY_CID
# fn19 threshold: CARD_FIELD3_THRESHOLD_1500
# fn24 raw mask: 0xffff803f (no named constant)
CID_SLOTS = [
    # fn01 -- EMBLEM_OF_DRAGON_DESTROYER_CID (REUSE, dispatched CID)
    (0x0808a364, 0x00001629, 'EMBLEM_OF_DRAGON_DESTROYER_CID', 'cid_8a364',
     'EMBLEM_OF_DRAGON_DESTROYER_CID=0x1629 (Emblem of Dragon Destroyer)'),
    # fn01 -- BUSTER_BLADER_CID (REUSE, partner comparison)
    (0x0808a368, 0x00001377, 'BUSTER_BLADER_CID', 'cid_8a368',
     'BUSTER_BLADER_CID=0x1377 (Buster Blader partner)'),
    # fn01 -- NECROVALLEY_CID (REUSE, partner comparison)
    (0x0808a374, 0x0000159d, 'NECROVALLEY_CID', 'cid_8a374',
     'NECROVALLEY_CID=0x159d (Necrovalley partner)'),
    # fn19 -- CARD_FIELD3_THRESHOLD_1500 (REUSE)
    (0x0808ab40, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500', 'thresh_8ab40',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc (1500 ATK threshold)'),
    # fn24 -- raw mask 0xffff803f (no named constant, med-conf; strips bits 6..14 from slot word)
    (0x0808ad84, 0xffff803f, 'slot_field_mask_ffff803f', 'mask_8ad84',
     'slot field mask 0xffff803f (strips bits 6..14; check_slot_card_eligible_by_card_id arg)'),
]

# =============================================================================
# REF_SLOTS: createDWordWithRef for EWRAM pointer pool slots (REF=34)
# =============================================================================

# gP1LifePoints = 0x0201c4e0 (ewram.inc) -- 22 slots
REF_LP_SLOTS = [
    (0x0808a36c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a36c', None),   # fn01
    (0x0808a3b0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a3b0', None),   # fn02
    (0x0808a3e0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a3e0', None),   # fn03
    (0x0808a438, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a438', None),   # fn04
    (0x0808a490, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a490', None),   # fn05
    (0x0808a53c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a53c', None),   # fn07 loop1
    (0x0808a590, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a590', None),   # fn07 loop2
    (0x0808a5e8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a5e8', None),   # fn08
    (0x0808a670, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a670', None),   # fn09
    (0x0808a6fc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a6fc', None),   # fn10
    (0x0808a77c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a77c', None),   # fn11
    (0x0808a834, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a834', None),   # fn12
    (0x0808a88c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a88c', None),   # fn13
    (0x0808a914, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a914', None),   # fn14
    (0x0808a970, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a970', None),   # fn15
    (0x0808a9ac, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8a9ac', None),   # fn16
    (0x0808aa2c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8aa2c', None),   # fn17
    (0x0808aaa8, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8aaa8', None),   # fn18
    (0x0808ab34, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8ab34', None),   # fn19
    (0x0808abec, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8abec', None),   # fn21
    (0x0808ac98, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8ac98', None),   # fn23
    (0x0808ad78, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_8ad78', None),   # fn24
]

# gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 3 slots
REF_FAC_SLOTS = [
    (0x0808a4ec, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8a4ec', None),  # fn06
    (0x0808ab98, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8ab98', None),  # fn20
    (0x0808ac44, 0x0201c600, 'gP1FieldArrayCBase', 'ptr_fac_8ac44', None),  # fn22
]

# gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 5 slots
REF_HSA_SLOTS = [
    (0x0808a704, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_8a704', None),  # fn10
    (0x0808a784, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_8a784', None),  # fn11
    (0x0808a91c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_8a91c', None),  # fn14
    (0x0808ab3c, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_8ab3c', None),  # fn19
    (0x0808ad80, 0x0201c8f8, 'gP1HandSlotArray', 'ptr_hsa_8ad80', None),  # fn24
]

# gP1SlotSetCodeArray = 0x0201c740 (ewram.inc) -- 2 slots
REF_SCA_SLOTS = [
    (0x0808a678, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_8a678', None),  # fn09
    (0x0808aab0, 0x0201c740, 'gP1SlotSetCodeArray', 'ptr_sca_8aab0', None),  # fn18
]

# gP1AltHandSlotArray = 0x0201cab0 (ewram.inc) -- 1 slot
REF_AHA_SLOTS = [
    (0x0808aa34, 0x0201cab0, 'gP1AltHandSlotArray', 'ptr_aha_8aa34', None),  # fn17
]

# gP1HandCountBase = 0x0201c4f4 (ewram.inc) -- 1 slot
REF_HCB_SLOTS = [
    (0x0808ad88, 0x0201c4f4, 'gP1HandCountBase', 'ptr_hcb_8ad88', None),  # fn24
]

# =============================================================================
# FUNCTION RENAMES + PLATES (24 functions)
# All plate text verified ASCII only, all len <= 500 chars
# =============================================================================
FUNC_RENAMES_AND_PLATES = [
    (0x0808a2ac, 'scan_zone_emblem_of_dragon_destroyer_substate_de',
     'Equip zone scan for Emblem of Dragon Destroyer (EMBLEM_OF_DRAGON_DESTROYER_CID=0x1629, pw=06390406). Two loops via gP1LifePoints: (1) +0x10 monster zone, check_card_pair_allowed gate, write substate_d; (2) +0x14, count_field_copies_of_card + check_card_pair_allowed gate, write substate_e. Partner pool: BUSTER_BLADER_CID=0x1377 + NECROVALLEY_CID=0x159d. Dispatch table entry [131].'),
    (0x0808a378, 'scan_zone_reserved_icid_group_substate_d',
     'Equip zone scan for reserved ICID group: ICID_RESERVED_A(0x162c) + ICID_RESERVED_B(0x184c). Monster zone scan via gP1LifePoints+STRIDE; no filter gate; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entries [132,232].'),
    (0x0808a3b8, 'scan_zone_senri_eye_dark_scorpion_group_substate_d',
     'Equip zone scan for Senri Eye/Dark Scorpion Chick group: Senri Eye (CID=0x1628, pw=60391791), Dark Scorpion - Chick the Yellow (DARK_SCORPION_CHICK_CID=0x1656, pw=61587183). Monster zone scan; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entries [130,139].'),
    (0x0808a3e8, 'scan_zone_fairy_of_the_spring_substate_e',
     'Equip zone scan for Fairy of the Spring (FAIRY_OF_THE_SPRING_CID=0x1664, pw=20188127). Monster zone at gP1LifePoints+0x14; gate: get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [142].'),
    (0x0808a440, 'scan_zone_arsenal_robber_substate_d',
     'Equip zone scan for Arsenal Robber (CID=0x166b, pw=55348096). Monster zone at gP1LifePoints+0x10; gate: get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addrs 0x0808a44c (LDR mid-loop) and 0x0808a450 (MUL mid-loop) are degenerate. Dispatch table entry [143].'),
    (0x0808a498, 'scan_zone_magical_dimension_substate_b',
     'Equip zone scan for Magical Dimension (MAGICAL_DIMENSION_CID=0x1678, pw=28553439). Field spell zone via gP1FieldArrayCBase+0x10; gates: check_card_field5_is_nonzero + get_card_extended_stat_field6 + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [144].'),
    (0x0808a4f0, 'scan_zone_dark_scorpion_meanae_substate_de',
     'Equip zone scan for Dark Scorpion - Meanae the Thorn (DARK_SCORPION_MEANAE_CID=0x1686, pw=74153887). Two loops over gP1LifePoints: (1) monster zone +0x10, is_dark_scorpion_type gate, write substate_d; (2) monster zone +0x14, is_dark_scorpion_type gate, write substate_e. Dispatch table entry [147].'),
    (0x0808a598, 'scan_zone_iron_blacksmith_kotetsu_substate_d',
     'Equip zone scan for Iron Blacksmith Kotetsu (IRON_BLACKSMITH_KOTETSU_CID=0x1689, pw=73431236). Monster zone at gP1LifePoints+0x10; gate: get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [148].'),
    (0x0808a5f0, 'scan_zone_pandemonium_substate_d',
     'Equip zone scan for Pandemonium (PANDEMONIUM_CID=0x169f, pw=94585852). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + check_card_is_archfiend_type + get_card_extended_stat_field5 level compare; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [149].'),
    (0x0808a67c, 'scan_zone_archfiend_roar_substate_e',
     'Equip zone scan for Archfiend\'s Roar (EQUIP_LOCK_A_CID=0x16a4, pw=56246017). Hand zone scan via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_is_archfiend_type + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [150].'),
    (0x0808a708, 'scan_zone_ray_of_hope_substate_e',
     'Equip zone scan for Ray of Hope (RAY_OF_HOPE_CID=0x16a8, pw=82529174). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [151].'),
    (0x0808a788, 'scan_zone_witch_doctor_of_chaos_substate_e',
     'Equip zone scan for Witch Doctor of Chaos (WITCH_DOCTOR_OF_CHAOS_CID=0x16c2, pw=75946257). Two loops via gP1LifePoints; both gate: check_card_field5_is_nonzero; both write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [155].'),
    (0x0808a83c, 'scan_zone_chaosrider_gustaph_substate_e',
     'Equip zone scan for Chaosrider Gustaph (CID=0x16c4, pw=47829960). Monster zone at gP1LifePoints+0x14; gate: get_card_extended_stat_field6==0x16 (Spell type); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [156].'),
    (0x0808a894, 'scan_zone_chaos_envoy_group_substate_e',
     'Equip zone scan for Chaos Envoy group: Chaos Sorcerer (CHAOS_SORCERER_CID=0x16c9, pw=09596126), Black Luster Soldier - Envoy of the Beginning (BLACK_LUSTER_SOLDIER_ENVOY_CID=0x16cb, pw=72989439), Chaos Emperor Dragon - Envoy of the End (CHAOS_EMPEROR_DRAGON_CID=0x16e4, pw=82301904). Hand zone scan; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(2) (Dark attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entries [161,162,166].'),
    (0x0808a920, 'scan_zone_recycle_substate_e',
     'Equip zone scan for Recycle (RECYCLE_CID=0x16d5, pw=96316857). Monster zone at gP1LifePoints+0x14; gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [163].'),
    (0x0808a978, 'scan_zone_primal_seed_substate_f',
     'Equip zone scan for Primal Seed (PRIMAL_SEED_CID=0x16d6, pw=23701465). GY zone scan at gP1LifePoints+0x1c; write_equip_zone_entry_by_substate(player_id, 0xf, slot_idx). Dispatch table entry [164].'),
    (0x0808a9b4, 'scan_zone_dimension_removal_group_substate_f',
     'Equip zone scan for Dimension Removal group (4 CIDs): Dimension Distortion (CID=0x16d8, pw=95194279), Dimension Fusion (DIMENSION_FUSION_CID=0x1712, pw=23557835), Return from DD (CID=0x17be, pw=27174286), D.D.M. (CID=0x191e, pw=82112775). Alt-hand zone via gP1AltHandSlotArray+0x1c; gates: field5_nonzero + equip_eligible_alt + get_zone_card_attribute_by_type; write_equip_zone_entry_by_substate(player_id, 0xf, slot_idx). Dispatch entries [165,171,197,267].'),
    (0x0808aa38, 'scan_zone_manju_of_ten_thousand_hands_substate_d',
     'Equip zone scan for Manju of the Ten Thousand Hands (CID=0x170c, pw=95492061). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: map_field8_to_card_type_category==6 (Ritual) + get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [170].'),
    (0x0808aab4, 'scan_zone_salvage_substate_e',
     'Equip zone scan for Salvage (CID=0x1714, pw=96947648). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field3_raw<=CARD_FIELD3_THRESHOLD_1500(0x5dc, ATK<=1500) + check_card_stat_field7_equals(3) (Water attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [173].'),
    (0x0808ab44, 'scan_zone_ultra_evolution_pill_substate_b',
     'Equip zone scan for Ultra Evolution Pill (ULTRA_EVOLUTION_PILL_CID=0x1715, pw=22431243). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + get_card_extended_stat_field6==0xa (Dinosaur) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [174].'),
    (0x0808ab9c, 'scan_zone_jade_insect_whistle_substate_d',
     'Equip zone scan for Jade Insect Whistle (JADE_INSECT_WHISTLE_CID=0x1717, pw=95214051). Monster zone at gP1LifePoints+0x10; gate: get_card_extended_stat_field6==0xa (Insect race); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [175].'),
    (0x0808abf4, 'scan_zone_abyss_soldier_lady_ninja_group_substate_b',
     'Equip zone scan for Abyss Soldier/Lady Ninja Yae group: Abyss Soldier (ABYSS_SOLDIER_CID=0x1727, pw=18318842), Lady Ninja Yae (CID=0x1754, pw=82005435). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + get_card_extended_stat_field7 + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entries [176,181].'),
    (0x0808ac48, 'scan_zone_arsenal_summoner_substate_d',
     'Equip zone scan for Arsenal Summoner (CID=0x1647, pw=85489096). Monster zone at gP1LifePoints+0x10; gate: check_card_is_guardian_type; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [137].'),
    (0x0808aca0, 'scan_zone_guardian_equip_group_substate_e',
     'Equip zone scan for Guardian equip group: Guardian Elma (GUARDIAN_ELMA_CID=0x164a, pw=74367458), Chopman the Desperate Outlaw (CID=0x16bc, pw=40884383), The Kick Man (THE_KICK_MAN_CID=0x1745, pw=90407382). Hand zone via gP1LifePoints+gP1HandSlotArray; local struct init via memset; gates: get_card_extended_stat_field9 + check_slot_card_eligible_by_card_id (mask 0xffff803f); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entries [138,153,178].'),
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
        print("DRY RUN -- RefineF11Seg4dSlots:")
        print("  STRIDE_SLOTS: %d" % len(STRIDE_SLOTS))
        print("  CID_SLOTS: %d" % len(CID_SLOTS))
        ref_total = (len(REF_LP_SLOTS) + len(REF_FAC_SLOTS) + len(REF_HSA_SLOTS) +
                     len(REF_SCA_SLOTS) + len(REF_AHA_SLOTS) + len(REF_HCB_SLOTS))
        print("  REF_SLOTS: %d (LP=%d + FAC=%d + HSA=%d + SCA=%d + AHA=%d + HCB=%d)" % (
            ref_total, len(REF_LP_SLOTS), len(REF_FAC_SLOTS), len(REF_HSA_SLOTS),
            len(REF_SCA_SLOTS), len(REF_AHA_SLOTS), len(REF_HCB_SLOTS)))
        print("  FUNC_RENAME+PLATE: %d" % len(FUNC_RENAMES_AND_PLATES))
        for addr, name, plate in FUNC_RENAMES_AND_PLATES:
            print("  [dry] FUNC_RENAME 0x%08x -> %s  plate_len=%d" % (addr, name, len(plate)))
        return

    print("=== RefineF11Seg4dSlots [0x0808a2ac..0x0808ad8c) ===")
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

    # --- REF slots (gP1LifePoints) ---
    print("--- REF_LP_SLOTS (%d) ---" % len(REF_LP_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_LP_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1FieldArrayCBase) ---
    print("--- REF_FAC_SLOTS (%d) ---" % len(REF_FAC_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_FAC_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1HandSlotArray) ---
    print("--- REF_HSA_SLOTS (%d) ---" % len(REF_HSA_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_HSA_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1SlotSetCodeArray) ---
    print("--- REF_SCA_SLOTS (%d) ---" % len(REF_SCA_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_SCA_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1AltHandSlotArray) ---
    print("--- REF_AHA_SLOTS (%d) ---" % len(REF_AHA_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_AHA_SLOTS:
        if not _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            fail_count += 1

    # --- REF slots (gP1HandCountBase) ---
    print("--- REF_HCB_SLOTS (%d) ---" % len(REF_HCB_SLOTS))
    for slot_addr, target_val, gas_label, slot_label, eol in REF_HCB_SLOTS:
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
    ref_total = (len(REF_LP_SLOTS) + len(REF_FAC_SLOTS) + len(REF_HSA_SLOTS) +
                 len(REF_SCA_SLOTS) + len(REF_AHA_SLOTS) + len(REF_HCB_SLOTS))
    print("=== RefineF11Seg4dSlots DONE ===")
    print("  STRIDE=%d  CID=%d  REF=%d  RENAME+PLATE=%d  FAIL=%d" % (
        len(STRIDE_SLOTS), len(CID_SLOTS), ref_total,
        len(FUNC_RENAMES_AND_PLATES), fail_count))
    if fail_count > 0:
        print("  *** %d FAIL(s) detected -- check output above ***" % fail_count)
    else:
        print("  All operations PASS")


main()
