# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11PoolRemediation.py -- f11 residual DAT_/DWORD_ pool label symbolization
#
# 41 auto-named pool labels created by disasm landings but never equated/labeled.
# Distribution: 0x85xxx:1, 0x86xxx:24, 0x87xxx:2, 0x88xxx:2, 0x89xxx:4,
#                0x8cxxx:3, 0x8dxxx:1, 0x8exxx:4 = 41 total
#
# Dispositions:
#   EQ (equate): slots with known named scalar/global constants
#   RENAME (label override): derived offsets and mask values with no standalone constant
#   REF (fn-ptr): DAT_080851d0 = 0x08081de5 THUMB+1 ptr to check_effect_node_handler_for_slot
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: _check() value mismatch -> skip that slot and report FAIL (do not abort all).

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


def _apply_ref_fnptr(slot_addr, target_addr, target_func_name, slot_label, eol=None):
    """Apply THUMB+1 fn-ptr slot: label the slot, add memory reference to target."""
    thumb_ptr = (target_addr + 1) & 0xFFFFFFFF
    if not _check(slot_addr, thumb_ptr, slot_label):
        return False
    if DRY:
        print("[dry] FNPTR 0x%08x -> %s (+1 THUMB ptr to 0x%08x)" % (slot_addr, slot_label, target_addr))
        return True
    a = _addr(slot_addr)
    tgt_a = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    # Label the target if not already named
    target_syms = [s.getName() for s in sym_tbl.getSymbols(tgt_a)]
    if target_func_name not in target_syms:
        sym_tbl.createLabel(tgt_a, target_func_name, SourceType.USER_DEFINED)
    # Rename slot label
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break
    # Add memory reference slot -> target (THUMB fn-ptr)
    ref_mgr.addMemoryReference(a, tgt_a, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref = ref_mgr.getReference(a, tgt_a, 0)
    if ref is not None:
        ref_mgr.setPrimary(ref, True)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[FNP] 0x%08x  -> %s (fn=0x%08x THUMB+1)" % (slot_addr, slot_label, target_addr))
    return True


fail_count = 0
ok_count = 0

def _do(result):
    global fail_count, ok_count
    if result:
        ok_count += 1
    else:
        fail_count += 1


# ---------------------------------------------------------------------------
# 1. DAT_080851d0: THUMB+1 fn-ptr to check_effect_node_handler_for_slot (0x08081de4)
# ---------------------------------------------------------------------------
print("=== Fn-ptr ===")
_do(_apply_ref_fnptr(
    0x080851d0, 0x08081de4,
    'check_effect_node_handler_for_slot',
    'ptr_check_effect_node_handler_for_slot',
    eol='THUMB+1 fn-ptr to check_effect_node_handler_for_slot (0x08081de4)'
))

# ---------------------------------------------------------------------------
# 2. EQUIP_SLOT_SUBSTATE_OFF = 0x58c  (9 slots in Seg-2 DWORD pool)
# ---------------------------------------------------------------------------
print("=== EQUIP_SLOT_SUBSTATE_OFF (x9) ===")
EQ_SUBSTATE = [
    (0x080861dc, 'substate_off_861dc'),
    (0x08086200, 'substate_off_86200'),
    (0x08086240, 'substate_off_86240'),
    (0x080862e8, 'substate_off_862e8'),
    (0x08086330, 'substate_off_86330'),
    (0x0808638c, 'substate_off_8638c'),
    (0x080863b4, 'substate_off_863b4'),
    (0x080863c8, 'substate_off_863c8'),
    (0x0808636c, 'substate_off_8636c'),
]
for (sa, sl) in EQ_SUBSTATE:
    _do(_apply_eq(sa, 0x0000058c, 'EQUIP_SLOT_SUBSTATE_OFF', sl))

# ---------------------------------------------------------------------------
# 3. gDuelPhaseFlags = 0x0201b290  (5 slots in Seg-2 DWORD pool)
# ---------------------------------------------------------------------------
print("=== gDuelPhaseFlags (x5) ===")
EQ_GDUELPF = [
    (0x08086244, 'gduelpf_86244'),
    (0x080862e4, 'gduelpf_862e4'),
    (0x08086314, 'gduelpf_86314'),
    (0x08086350, 'gduelpf_86350'),
    (0x08086368, 'gduelpf_86368'),
]
for (sa, sl) in EQ_GDUELPF:
    _do(_apply_eq(sa, 0x0201b290, 'gDuelPhaseFlags', sl))

# ---------------------------------------------------------------------------
# 4. 0x080862b4 = 0x09e3f14c  game text separator record ptr
#    Already symbolized in other slots as text_sep_ptr_85d44 / game_text_sep_ptr;
#    this instance needs a consistent semantic rename.
# ---------------------------------------------------------------------------
print("=== game_text_sep ptr (0x09e3f14c) ===")
_do(_apply_rename(
    0x080862b4,
    'game_text_sep_ptr_862b4',
    eol='ROM addr 0x09e3f14c: game text separator record (append_game_text_if_raw)'
))

# ---------------------------------------------------------------------------
# 5. gP1LifePoints = 0x0201c4e0  (4 slots: 3 in Seg-2 + 1 in 0x89xxx)
# ---------------------------------------------------------------------------
print("=== gP1LifePoints ptr slots (x4) ===")
EQ_P1LP = [
    (0x08086310, 'ptr_lp_86310'),
    (0x08086384, 'ptr_lp_86384'),
    (0x080863f4, 'ptr_lp_863f4'),
    (0x080890b8, 'ptr_lp_890b8'),
]
for (sa, sl) in EQ_P1LP:
    _do(_apply_eq(sa, 0x0201c4e0, 'gP1LifePoints', sl))

# ---------------------------------------------------------------------------
# 6. LP_BAR_ANIM_STATE_OFF = 0x4cc  (1 slot)
# ---------------------------------------------------------------------------
print("=== LP_BAR_ANIM_STATE_OFF ===")
_do(_apply_eq(0x08086318, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'lp_bar_anim_st_86318'))

# ---------------------------------------------------------------------------
# 7. ELIGIB_STATE_CTRL_OFF = 0x1d54  (2 slots)
# ---------------------------------------------------------------------------
print("=== ELIGIB_STATE_CTRL_OFF (x2) ===")
_do(_apply_eq(0x08086334, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_ctrl_86334'))
_do(_apply_eq(0x08086388, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_ctrl_86388'))

# ---------------------------------------------------------------------------
# 8. ELIGIB_ACT_TYPE_OFF = 0x1d5c  (1 slot)
# ---------------------------------------------------------------------------
print("=== ELIGIB_ACT_TYPE_OFF ===")
_do(_apply_eq(0x080863ac, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_act_type_863ac'))

# ---------------------------------------------------------------------------
# 9. ELIGIB_ACT_COUNT_OFF = 0x1d58  (1 slot)
# ---------------------------------------------------------------------------
print("=== ELIGIB_ACT_COUNT_OFF ===")
_do(_apply_eq(0x080863b0, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_act_cnt_863b0'))

# ---------------------------------------------------------------------------
# 10. ELIGIB_ANIM_STATE_OFF = 0x1d6c  (1 slot)
# ---------------------------------------------------------------------------
print("=== ELIGIB_ANIM_STATE_OFF ===")
_do(_apply_eq(0x080863fc, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_st_863fc'))

# ---------------------------------------------------------------------------
# 11-12. 0x87xxx: derived offsets relative to gP1SlotSetCodeArray
#   0x08087f48 = 0xfffffdb0 = gP1SlotCountBase - gP1SlotSetCodeArray = -0x250
#   0x08087f4c = 0x00001b38 = gEquipZoneBase_1d98 - gP1SlotSetCodeArray
# ---------------------------------------------------------------------------
print("=== 0x87xxx derived offsets ===")
_do(_apply_rename(
    0x08087f48,
    'slot_count_sca_neg_off',
    eol='0xfffffdb0 = gP1SlotCountBase-gP1SlotSetCodeArray (-0x250); addr: gP1SlotCountBase'
))
_do(_apply_rename(
    0x08087f4c,
    'equip_zone_sca_off',
    eol='0x1b38 = gEquipZoneBase_1d98-gP1SlotSetCodeArray; addr: gEquipZoneBase_1d98=0x201e278'
))

# ---------------------------------------------------------------------------
# 13. 0x0808818c = 0x5dc = CARD_FIELD3_THRESHOLD_1500
#     get_card_extended_stat_field3_raw(cid) bgt 0x5dc -> skip (ATK<=1500 gate)
# ---------------------------------------------------------------------------
print("=== CARD_FIELD3_THRESHOLD_1500 ===")
_do(_apply_eq(0x0808818c, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500', 'field3_thresh_1500_818c'))

# ---------------------------------------------------------------------------
# 14. PLAYER_BLOCK_STRIDE = 0x868  (6 slots)
# ---------------------------------------------------------------------------
print("=== PLAYER_BLOCK_STRIDE (x6) ===")
EQ_STRIDE = [
    (0x080887a4, 'stride_887a4'),
    (0x08089410, 'stride_89410'),
    (0x080897ac, 'stride_897ac'),
    (0x0808c4f8, 'stride_8c4f8'),
    (0x0808c894, 'stride_8c894'),
    (0x0808cab8, 'stride_cab8'),
]
for (sa, sl) in EQ_STRIDE:
    _do(_apply_eq(sa, 0x00000868, 'PLAYER_BLOCK_STRIDE', sl))

# ---------------------------------------------------------------------------
# 15. zone_query_hand_tag_12a1 = 0x12a1  (1 slot)
# ---------------------------------------------------------------------------
print("=== zone_query_hand_tag_12a1 ===")
_do(_apply_eq(0x080894b0, 0x000012a1, 'zone_query_hand_tag_12a1', 'zone_qtag_894b0'))

# ---------------------------------------------------------------------------
# 16. DAT_0808dc1c = 0x0fdc: offset gDuelFieldSlots_p2_base -> gDuelFieldSlotsEffectZoneBase
#     gDuelFieldSlots_p2_base(0x201c5d8) + 0xfdc = 0x201d5b4 = gDuelFieldSlotsEffectZoneBase
#     No standalone constant exists; rename label.
# ---------------------------------------------------------------------------
print("=== DAT_0808dc1c: effect zone p2 stride offset ===")
_do(_apply_rename(
    0x0808dc1c,
    'effect_zone_p2_off',
    eol='0xfdc = gDuelFieldSlotsEffectZoneBase-gDuelFieldSlots_p2_base; yields 0x201d5b4'
))

# ---------------------------------------------------------------------------
# 17-20. 0x8exxx mask/offset values
#   DAT_0808e4d4 = 0x98300000 = MAGICAL_THORN_CID(0x1306) << 19
#   DAT_0808e5b0 = 0xffffe358 = gEquipZoneCountTable - gDuelFieldSlotState = -0x1ca8
#   DAT_0808e834 = 0x3a200000 = Forced Requisition equip sprite attr OR-in base mask
#   DAT_0808e8f8 = 0x9b080000 = SKULL_INVITATION_CID(0x1361) << 19
# ---------------------------------------------------------------------------
print("=== 0x8exxx mask/offset values ===")
_do(_apply_rename(
    0x0808e4d4,
    'magical_thorn_cid_shifted',
    eol='0x98300000 = MAGICAL_THORN_CID(0x1306)<<19; cmp after lsls card-word #19'
))
_do(_apply_rename(
    0x0808e5b0,
    'equip_zone_to_field_state_neg_off',
    eol='0xffffe358 = gEquipZoneCountTable-gDuelFieldSlotState (-0x1ca8)'
))
_do(_apply_rename(
    0x0808e834,
    'equip_sprite_attr_base_frq',
    eol='0x3a200000: Forced Requisition equip slot sprite attr OR-in mask'
))
_do(_apply_rename(
    0x0808e8f8,
    'skull_inv_cid_shifted',
    eol='0x9b080000 = SKULL_INVITATION_CID(0x1361)<<19; state cmp after lsls card-word #19'
))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("")
print("=== RefineF11PoolRemediation DONE ===")
print("OK=%d  FAIL=%d  DRY=%s" % (ok_count, fail_count, DRY))
if fail_count > 0:
    print("WARNING: %d slot(s) failed -- review FAIL lines above" % fail_count)
