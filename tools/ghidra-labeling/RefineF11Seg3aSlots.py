# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg3aSlots.py -- f11 Seg-3a slot symbolization [0x08086cdc..0x080872e4)
#
# 4 named functions: dispatch_equip_zone_activation_state / populate_equip_zone_entries_substate_d
#   / populate_equip_zone_entries_substate_e / write_equip_zone_entries_substate_d_range
#
# C13=46: EQ(36) + REF(4) + RENAME(6) = 46 slots (100% coverage)
# PLATE=5:
#   1. dispatch_equip_zone_activation_state @ 0x08086cdc -- CJK mojibake -> full ASCII rewrite (497 chars)
#   2. populate_equip_zone_entries_substate_d @ 0x080871a8 -- substring replace (gDuelCardPool/gDuelZoneData)
#   3. populate_equip_zone_entries_substate_e @ 0x0808724c -- substring replace (gDuelCardPool_alt_base)
#   4. write_equip_zone_entry_by_substate @ 0x0808d88c (asm/11) -- substring replace FUN_080871a8
#   5. init_zone_activation_display_state_p1_entry @ 0x08096a08 (asm/12) -- substring replace FUN_08086e90/FUN_08086fa6
# FUNC_RENAME=0, carve=0, disasm=0
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: PLATE WARN=FAIL: if setComment fails or pattern not found, report FAIL.
# NOTE: All 36 EQ slots are REUSE (0 new constants needed).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

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
    """Apply USER label to slot + add memory reference to target."""
    if not _check(slot_addr, target_val, gas_label):
        return False
    if DRY:
        print("[dry] REF 0x%08x  target=0x%08x  gas_label=%s  slot_label=%s" % (
            slot_addr, target_val, gas_label, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
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
    print("[REF] 0x%08x  target=0x%08x  -> %s" % (slot_addr, target_val, slot_label))
    return True


def _apply_rename(slot_addr, slot_label, eol=None):
    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return True
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
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
    print("[REN] 0x%08x  -> %s" % (slot_addr, slot_label))
    return True


def _apply_plate_full(fn_addr, plate_text):
    """Full plate overwrite (for CJK mojibake rewrite)."""
    if DRY:
        print("[dry] PLATE_FULL 0x%08x  len=%d" % (fn_addr, len(plate_text)))
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE_FULL 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLT_FULL] 0x%08x OK  len=%d" % (fn_addr, len(plate_text)))
        return True
    except Exception as e:
        print("FAIL PLATE_FULL 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


def _apply_plate_subst(fn_addr, substitutions):
    """Substring replace in existing plate. substitutions = list of (old, new).
    FAIL if any old string not found in current plate (WARN=FAIL policy)."""
    if DRY:
        for old, new in substitutions:
            print("[dry] PLATE_SUBST 0x%08x  old=%r -> new=%r" % (fn_addr, old, new))
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE_SUBST 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    current = cu.getComment(CodeUnit.PLATE_COMMENT)
    if current is None:
        current = ""
    ok = True
    for old, new in substitutions:
        if old not in current:
            print("FAIL PLATE_SUBST 0x%08x: pattern not found: %r (WARN=FAIL)" % (fn_addr, old))
            ok = False
        else:
            current = current.replace(old, new)
    if not ok:
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, current)
        print("[PLT_SUBST] 0x%08x OK" % fn_addr)
        return True
    except Exception as e:
        print("FAIL PLATE_SUBST 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label, eol_or_None)
#    36 total EQ slots -- all REUSE from existing constants
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== dispatch_equip_zone_activation_state (0x08086cdc) =====
    # REUSE: gDuelPhaseFlags=0x0201b290 (ewram.inc)
    (0x08086d14, 0x0201b290, 'gDuelPhaseFlags',        'gduelphaseflag_86d14', None),
    # REUSE: EQUIP_PHASE_FRAME_OFF=0x000004a4 (ewram.inc)
    (0x08086dc4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',  'equip_phase_frame_86dc4', None),
    # REUSE: EARTH_CHANT_CID=0x00001716 (card_info.inc)
    (0x08086dc8, 0x00001716, 'EARTH_CHANT_CID',        'earth_chant_cid_86dc8', None),
    # REUSE: END_OF_WORLD_CID=0x000019d9 (card_info.inc)
    (0x08086e50, 0x000019d9, 'END_OF_WORLD_CID',       'end_of_world_cid_86e50', None),
    # REUSE: gDuelCardCtxBase=0x0201e2a0 (ewram.inc)
    (0x08086e54, 0x0201e2a0, 'gDuelCardCtxBase',       'gduelcardctx_86e54', None),
    # REUSE: PLAYER_BLOCK_STRIDE=0x00000868 (ewram.inc)
    (0x08086e5c, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_86e5c', None),
    # REUSE: gP1FieldArrayCBase=0x0201c600 (ewram.inc)
    (0x08086e60, 0x0201c600, 'gP1FieldArrayCBase',     'gp1fieldarrayc_86e60', None),
    # REUSE: gEquipEffectZoneTable=0x09e5a0c4 (card_info.inc)
    (0x08086e64, 0x09e5a0c4, 'gEquipEffectZoneTable',  'gequipeffzone_86e64', None),
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x08086e80, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_86e80', None),
    # REUSE: gEquipEffectZoneTable
    (0x08086eac, 0x09e5a0c4, 'gEquipEffectZoneTable',  'gequipeffzone_86eac', None),
    # REUSE: LP_BANISHER_CTX_OFF=0x00001d70 (ewram.inc)
    (0x08086f24, 0x00001d70, 'LP_BANISHER_CTX_OFF',    'lp_banisher_ctx_86f24', None),
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x08086f28, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_86f28', None),
    # REUSE: gEquipEffectZoneTable
    (0x08086f2c, 0x09e5a0c4, 'gEquipEffectZoneTable',  'gequipeffzone_86f2c', None),
    # REUSE: EQUIP_PHASE_FRAME_OFF
    (0x08086f70, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',  'equip_phase_frame_86f70', None),
    # REUSE: gEquipEffectZoneTable
    (0x08086f74, 0x09e5a0c4, 'gEquipEffectZoneTable',  'gequipeffzone_86f74', None),
    # REUSE: gDuelCardCtxBase
    (0x08086f78, 0x0201e2a0, 'gDuelCardCtxBase',       'gduelcardctx_86f78', None),
    # REUSE: gDuelCardCtxBase
    (0x08086f9c, 0x0201e2a0, 'gDuelCardCtxBase',       'gduelcardctx_86f9c', None),
    # REUSE: ELIGIB_ANIM_STATE_OFF=0x00001d6c (ewram.inc)
    (0x0808704c, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',  'eligib_anim_state_8704c', None),
    # REUSE: LP_BANISHER_CTX_OFF
    (0x08087050, 0x00001d70, 'LP_BANISHER_CTX_OFF',    'lp_banisher_ctx_87050', None),
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x08087054, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_87054', None),
    # REUSE: ELIGIB_SPRITE_CTRL_OFF=0x00001d68 (ewram.inc)
    (0x080870f4, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_870f4', None),
    # REUSE: LP_BANISHER_CTX_OFF
    (0x080870f8, 0x00001d70, 'LP_BANISHER_CTX_OFF',    'lp_banisher_ctx_870f8', None),
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x080870fc, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_870fc', None),
    # REUSE: gDuelPhaseFlags
    (0x08087100, 0x0201b290, 'gDuelPhaseFlags',        'gduelphaseflag_87100', None),
    # REUSE: EQUIP_PHASE_FRAME_OFF
    (0x08087104, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',  'equip_phase_frame_87104', None),
    # REUSE: gEquipEffectZoneTable
    (0x0808715c, 0x09e5a0c4, 'gEquipEffectZoneTable',  'gequipeffzone_8715c', None),
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x08087160, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_87160', None),
    # REUSE: gP1FieldArrayCBase
    (0x08087164, 0x0201c600, 'gP1FieldArrayCBase',     'gp1fieldarrayc_87164', None),
    # REUSE: gDuelCardCtxBase
    (0x08087168, 0x0201e2a0, 'gDuelCardCtxBase',       'gduelcardctx_87168', None),

    # ===== populate_equip_zone_entries_substate_d (0x080871a8) =====
    # REUSE: SAMSARA_CID=0x000019da (card_info.inc)
    (0x080871a4, 0x000019da, 'SAMSARA_CID',            'samsara_cid_871a4', None),

    # ===== populate_equip_zone_entries_substate_e (0x0808724c) =====
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x0808723c, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_8723c', None),
    # REUSE: gP1SlotSetCodeArray=0x0201c740 (ewram.inc)
    (0x08087240, 0x0201c740, 'gP1SlotSetCodeArray',    'gp1slotsetcode_87240', None),
    # REUSE: CARD_FIELD3_THRESHOLD_1500=0x000005dc (card_info.inc)
    (0x08087244, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500', 'field3_thresh_87244', None),
    # REUSE: zone_query_hand_tag_12a1=0x000012a1 (duel_field.inc)
    (0x08087248, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_hand_tag_87248', None),

    # ===== write_equip_zone_entries_substate_d_range (0x080872a4) =====
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x080872a0, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_872a0', None),
    # REUSE: PLAYER_BLOCK_STRIDE
    (0x080872e0, 0x00000868, 'PLAYER_BLOCK_STRIDE',    'player_stride_872e0', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_val, gas_label, slot_label, eol_or_None)
#    4 slots: 1 switchdata base + 3 fn-ptr THUMB+1 slots
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # switchdata base: DAT_08086d18 -> 0x08086d1c (switchD_08086d10 dispatch table)
    (0x08086d18, 0x08086d1c,
     'switchD_08086d10__switchdataD_08086d1c',
     'switchdata_86d18', None),
    # fn-ptr: scan_equip_zones_for_eligible_type11_target THUMB+1
    (0x08086e98, 0x080869a9,
     'scan_equip_zones_for_eligible_type11_target+1',
     'scan_equip_zone11_fnptr_86e98', None),
    # fn-ptr: eval_equip_zone_score_with_field_card THUMB+1 (caseD_7d path)
    (0x08086fa0, 0x08086a39,
     'eval_equip_zone_score_with_field_card+1',
     'eval_equip_score_fnptr_86fa0', None),
    # fn-ptr: eval_equip_zone_score_with_field_card THUMB+1 (caseD_80 path)
    (0x08086fb0, 0x08086a39,
     'eval_equip_zone_score_with_field_card+1',
     'eval_equip_score_fnptr_86fb0', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: PTR_gP1LifePoints_ -> gp1lp_ptr_<hex> with EOL
#    6 slots (all hold value 0x0201c4e0 = gP1LifePoints)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08086e58, 'gp1lp_ptr_86e58', 'gP1LifePoints'),
    (0x08086f20, 'gp1lp_ptr_86f20', 'gP1LifePoints'),
    (0x08087048, 'gp1lp_ptr_87048', 'gP1LifePoints'),
    (0x08087238, 'gp1lp_ptr_87238', 'gP1LifePoints'),
    (0x0808729c, 'gp1lp_ptr_8729c', 'gP1LifePoints'),
    (0x080872dc, 'gp1lp_ptr_872dc', 'gP1LifePoints'),
]

# ---------------------------------------------------------------------------
# D. PLATE operations
#    Plate 1: full rewrite (CJK mojibake -> ASCII), 497 chars
#    Plates 2-5: substring substitution on existing plates (WARN=FAIL if not found)
# ---------------------------------------------------------------------------

# Plate 1: full ASCII rewrite (497 chars, all ASCII verified)
PLATE1_TEXT = (
    "Equip zone activation state dispatcher. Gate: [r7+0x4] bit2 set -> return 0. "
    "Else reads [gDuelPhaseFlags+0x4a0] state, subs 0x62 -> index [0..0x1e], "
    "dispatches via table at 0x08086d1c (0x1f entries). Notable: "
    "idx0=caseD_62(count_field_copies+enqueue_lp_sprite), "
    "idx2=caseD_64(find_zone_slot_allowed+setup_equip_oam), "
    "idx0x1a=caseD_7c(select_equip_target), "
    "idx0x1b=caseD_7d(init_zone_activation), "
    "idx0x1c=caseD_7e(invoke_card_display_op_sub13), "
    "idx0x1d=caseD_7f, idx0x1e=caseD_80, default=caseD_63."
)

# Plate 2 substitutions: gDuelCardPool -> gP1SlotSetCodeArray, gDuelZoneData -> zone_query_hand_tag_12a1
PLATE2_SUBSTS = [
    ("gDuelCardPool=0x0201c740", "gP1SlotSetCodeArray=0x0201c740"),
    ("gDuelZoneData (key=0x12a1)", "zone_query_hand_tag_12a1=0x12a1"),
]

# Plate 3 substitution: gDuelCardPool_alt_base=gP1LifePoints+0x418 (0x83<<3)
PLATE3_SUBSTS = [
    ("gDuelCardPool_alt_base=gP1LifePoints+0x418 (0x83<<3)",
     "gP1HandSlotArray=0x0201c8f8 (gP1LifePoints+0x418, 0x83<<3)"),
]

# Plate 4 substitution: FUN_080871a8 -> populate_equip_zone_entries_substate_d
PLATE4_SUBSTS = [
    ("FUN_080871a8", "populate_equip_zone_entries_substate_d"),
]

# Plate 5 substitution: FUN_08086e90/FUN_08086fa6 -> dispatch_equip_zone_activation_state (caseD_80/caseD_7d)
PLATE5_SUBSTS = [
    ("FUN_08086e90/FUN_08086fa6",
     "dispatch_equip_zone_activation_state (caseD_80/caseD_7d)"),
]


def main():
    print("=== RefineF11Seg3aSlots (DRY=%s) ===" % DRY)
    nEQ = nREF = nREN = nPLT = 0
    fails = []

    print("--- EQ_SLOTS (36) ---")
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            nEQ += 1
        else:
            fails.append("EQ 0x%08x" % slot_addr)

    print("--- REF_SLOTS (4) ---")
    for entry in REF_SLOTS:
        slot_addr, target_val, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            nREF += 1
        else:
            fails.append("REF 0x%08x" % slot_addr)

    print("--- RENAME_SLOTS (6) ---")
    for slot_addr, slot_label, eol in RENAME_SLOTS:
        if _apply_rename(slot_addr, slot_label, eol):
            nREN += 1
        else:
            fails.append("REN 0x%08x" % slot_addr)

    print("--- PLATE ops (5) ---")
    # Plate 1: full rewrite of CJK mojibake
    if _apply_plate_full(0x08086cdc, PLATE1_TEXT):
        nPLT += 1
    else:
        fails.append("PLT_FULL 0x08086cdc")

    # Plate 2: substring replace in populate_equip_zone_entries_substate_d
    if _apply_plate_subst(0x080871a8, PLATE2_SUBSTS):
        nPLT += 1
    else:
        fails.append("PLT_SUBST 0x080871a8")

    # Plate 3: substring replace in populate_equip_zone_entries_substate_e
    if _apply_plate_subst(0x0808724c, PLATE3_SUBSTS):
        nPLT += 1
    else:
        fails.append("PLT_SUBST 0x0808724c")

    # Plate 4: substring replace in write_equip_zone_entry_by_substate (asm/11 L6286)
    if _apply_plate_subst(0x0808d88c, PLATE4_SUBSTS):
        nPLT += 1
    else:
        fails.append("PLT_SUBST 0x0808d88c")

    # Plate 5: substring replace in init_zone_activation_display_state_p1_entry (asm/12 L5378)
    if _apply_plate_subst(0x08096a08, PLATE5_SUBSTS):
        nPLT += 1
    else:
        fails.append("PLT_SUBST 0x08096a08")

    print("")
    print("=== SUMMARY ===")
    print("EQ=%d/36  REF=%d/4  REN=%d/6  PLT=%d/5" % (nEQ, nREF, nREN, nPLT))
    if fails:
        print("FAILURES (%d): %s" % (len(fails), ", ".join(fails)))
    else:
        print("ALL PASS (0 failures)")


main()
