# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg2Slots.py -- f11 Seg-2 slot symbolization [0x08085d4c..0x08086cdc)
#
# 12 named functions, 1 ROM_INCBIN block 0x861a0/0x27a -> R4 DISASM (see DisassembleF11Seg2.py)
# C13=92: EQ(80) + REF(4) + RENAME(8) = 92 slots (100% coverage)
# PLATE=12 (7 in-segment + 5 cross-file asm/11 L18359 + asm/12 L3440/3569/3693/3867)
# FUNC_RENAME=0 (all 12 existing functions have correct names)
# carve=0, disasm=1 block with 6 sub-case labels (see DisassembleF11Seg2.py)
#
# NEW constants added to constants/*.inc BEFORE running this script:
#   ewram.inc +1: EQUIP_SLOT_SUBSTATE_OFF=0x58c
#   card_info.inc +4: CONTRACT_WITH_ABYSS_CID=0x1698, EARTH_CHANT_CID=0x1716,
#     END_OF_WORLD_CID=0x19d9, gEquipEffectZoneTable=0x09e5a0c4
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.
# NOTE: PLATE WARN=FAIL: if setComment fails or code unit missing, report FAIL.

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
    """Apply USER label to slot + optional EOL. Raw value slots (text IDs, ptrs)."""
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


def _apply_plate(fn_addr, plate_text):
    if DRY:
        print("[dry] PLATE 0x%08x" % fn_addr)
        return True
    a = _addr(fn_addr)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE 0x%08x: no code unit (WARN=FAIL)" % fn_addr)
        return False
    try:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLT] 0x%08x OK" % fn_addr)
        return True
    except Exception as e:
        print("FAIL PLATE 0x%08x: %s (WARN=FAIL)" % (fn_addr, e))
        return False


# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label, eol_or_None)
#    80 total EQ slots -- all ROM values verified (C4 pass in review)
#
#    79 explicit pool slots + 1 disasm-block-internal (0x080863f8 ELIGIB_SPRITE_CTRL_OFF)
#    = 80 total EQ
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== dispatch_field_display_state_by_type (0x08085d4c) -- 25 slots =====
    # REUSE: gDuelPhaseFlags=0x0201b290 (ewram.inc) x7
    (0x08085d74, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85d74', None),
    (0x08085ea0, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85ea0', None),
    (0x08085ebc, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85ebc', None),
    (0x08085f28, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85f28', None),
    (0x08085f70, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85f70', None),
    (0x08085ff8, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85ff8', None),
    (0x080860c0, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_860c0', None),

    # REUSE: FIELD_DISPLAY_TYPE_OFF=0x0000057c (ewram.inc) x2
    (0x08085d78, 0x0000057c, 'FIELD_DISPLAY_TYPE_OFF',
     'field_disp_type_85d78', None),
    (0x080860f4, 0x0000057c, 'FIELD_DISPLAY_TYPE_OFF',
     'field_disp_type_860f4', None),

    # REUSE: ELIGIB_RESULT_OFF=0x00000584 (ewram.inc) x4
    (0x08085ea4, 0x00000584, 'ELIGIB_RESULT_OFF',
     'eligib_result_85ea4', None),
    (0x08085ffc, 0x00000584, 'ELIGIB_RESULT_OFF',
     'eligib_result_85ffc', None),
    (0x0808602c, 0x00000584, 'ELIGIB_RESULT_OFF',
     'eligib_result_8602c', None),
    (0x080860c4, 0x00000584, 'ELIGIB_RESULT_OFF',
     'eligib_result_860c4', None),

    # REUSE: gDuelCardCtxBase=0x0201e2a0 (ewram.inc) x1
    (0x08085ea8, 0x0201e2a0, 'gDuelCardCtxBase',
     'gdueleardctx_85ea8', None),

    # REUSE: ELIGIB_STATE_CTRL_OFF=0x00001d54 (ewram.inc) x3
    (0x08085f58, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',
     'eligib_state_ctrl_85f58', None),
    (0x08085f90, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',
     'eligib_state_ctrl_85f90', None),
    (0x080860bc, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',
     'eligib_state_ctrl_860bc', None),

    # REUSE: ELIGIB_ACT_TYPE_OFF=0x00001d5c (ewram.inc) x1
    (0x08085fb4, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF',
     'eligib_act_type_85fb4', None),

    # REUSE: ELIGIB_ACT_COUNT_OFF=0x00001d58 (ewram.inc) x1
    (0x08085fb8, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF',
     'eligib_act_cnt_85fb8', None),

    # REUSE: gSpriteAttrBuf=0x0201b870 (ewram.inc) x2
    (0x08086000, 0x0201b870, 'gSpriteAttrBuf',
     'gspriteattrb_86000', None),
    (0x08086028, 0x0201b870, 'gSpriteAttrBuf',
     'gspriteattrb_86028', None),

    # REUSE: ELIGIB_ANIM_STATE_OFF=0x00001d6c (ewram.inc) x1
    (0x08086064, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_st_86064', None),

    # REUSE: ELIGIB_CARD_ID_OFF=0x00001d44 (ewram.inc) x1
    (0x08086080, 0x00001d44, 'ELIGIB_CARD_ID_OFF',
     'eligib_card_id_86080', None),

    # REUSE: P1LP_BLOCK2_OFF_1CE8=0x00001ce8 (ewram.inc) x1
    (0x080860fc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_1ce8_860fc', None),

    # REUSE: LP_BAR_ANIM_STATE_OFF=0x000004cc (ewram.inc) x1
    (0x08086100, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'lp_bar_anim_st_86100', None),

    # ===== dispatch_equip_slot_state_by_index (0x0808611c) -- 4 slots =====
    # REUSE: gDuelCardCtxBase=0x0201e2a0 x1
    (0x08086160, 0x0201e2a0, 'gDuelCardCtxBase',
     'gdueleardctx_86160', None),
    # REUSE: gDuelPhaseFlags=0x0201b290 x1
    (0x08086164, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_86164', None),
    # REUSE: EFFECT_ENTRY_COUNT_OFF=0x00000594 (ewram.inc) x1
    (0x08086168, 0x00000594, 'EFFECT_ENTRY_COUNT_OFF',
     'effect_entry_cnt_86168', None),
    # NEW: EQUIP_SLOT_SUBSTATE_OFF=0x0000058c (ewram.inc) x1
    (0x0808616c, 0x0000058c, 'EQUIP_SLOT_SUBSTATE_OFF',
     'equip_slot_subst_8616c', None),

    # ===== check_equip_target_slot_by_card_id (0x08086430) -- 2 slots =====
    # NEW: gEquipEffectZoneTable=0x09e5a0c4 (card_info.inc) x1
    (0x08086448, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86448', None),
    # NEW: CONTRACT_WITH_ABYSS_CID=0x00001698 (card_info.inc) x1
    (0x0808645c, 0x00001698, 'CONTRACT_WITH_ABYSS_CID',
     'contract_abyss_cid_8645c', None),

    # ===== find_equip_target_in_effect_zones (0x0808647c) -- 4 slots =====
    # REUSE: PLAYER_BLOCK_STRIDE=0x00000868 (ewram.inc) x2
    (0x080864dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_864dc', None),
    (0x08086504, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86504', None),
    # REUSE: gEquipEffectZoneTable=0x09e5a0c4 x1
    (0x080864e0, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_864e0', None),
    # REUSE: gP1FieldArrayCBase=0x0201c600 (ewram.inc) x1
    (0x080864e4, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrc_864e4', None),

    # ===== sum_equip_zone_bonus_scores_for_player (0x08086508) -- 4 slots =====
    # REUSE: PLAYER_BLOCK_STRIDE x2
    (0x08086564, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86564', None),
    (0x080865a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_865a4', None),
    # REUSE: gP1FieldArrayCBase x1
    (0x08086568, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrc_86568', None),
    # REUSE: gP1ZoneHandCount=0x0201c4ec (ewram.inc) x1
    (0x080865a8, 0x0201c4ec, 'gP1ZoneHandCount',
     'gp1zonehandcnt_865a8', None),

    # ===== sum_equip_chain_scores_for_card (0x080865ac) -- 2 slots =====
    # REUSE: PLAYER_BLOCK_STRIDE x1
    (0x0808662c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_8662c', None),
    # REUSE: gDuelFieldSlots=0x0201c510 (ewram.inc) x1
    (0x08086630, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_86630', None),

    # ===== eval_equip_slot_score_in_range (0x08086634) -- 13 slots =====
    # REUSE: gDuelPhaseFlags x1
    (0x080866dc, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_866dc', None),
    # REUSE: EQUIP_PHASE_FRAME_OFF=0x000004a4 (ewram.inc) x1
    (0x080866e0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frm_866e0', None),
    # REUSE: gEquipEffectZoneTable x1
    (0x080866e4, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_866e4', None),
    # REUSE: PLAYER_BLOCK_STRIDE x3
    (0x080866e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_866e8', None),
    (0x08086790, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86790', None),
    (0x0808683c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_8683c', None),
    (0x080868f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_868f8', None),
    # REUSE: gP1FieldArrayCBase x1
    (0x080866ec, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrc_866ec', None),
    # REUSE: gDuelFieldSlots x2
    (0x08086794, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_86794', None),
    (0x08086950, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_86950', None),
    # NEW: EARTH_CHANT_CID=0x00001716 (card_info.inc) x1
    (0x08086798, 0x00001716, 'EARTH_CHANT_CID',
     'earth_chant_cid_86798', None),
    # NEW: END_OF_WORLD_CID=0x000019d9 (card_info.inc) x1
    (0x080867b8, 0x000019d9, 'END_OF_WORLD_CID',
     'end_of_world_cid_867b8', None),
    # REUSE: gP1ZoneHandCount x1
    (0x080868fc, 0x0201c4ec, 'gP1ZoneHandCount',
     'gp1zonehandcnt_868fc', None),

    # ===== scan_equip_zones_for_eligible_type11_target (0x080869a8) -- 6 slots =====
    # REUSE: gDuelPhaseFlags x1
    (0x08086a08, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_86a08', None),
    # REUSE: EQUIP_ACTIVE_CTX_OFF=0x00000484 (duel_field.inc) x1
    (0x08086a0c, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'equip_actctx_86a0c', None),
    # REUSE: gEquipEffectZoneTable x2
    (0x08086a10, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86a10', None),
    (0x08086a34, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86a34', None),
    # REUSE: PLAYER_BLOCK_STRIDE x1
    (0x08086a14, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86a14', None),
    # REUSE: gP1FieldArrayCBase x1
    (0x08086a18, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrc_86a18', None),

    # ===== eval_equip_zone_score_with_field_card (0x08086a38) -- 2 slots =====
    # REUSE: gDuelPhaseFlags x1
    (0x08086a58, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_86a58', None),
    # REUSE: EQUIP_ACTIVE_CTX_OFF x1
    (0x08086a5c, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'equip_actctx_86a5c', None),

    # ===== eval_equip_zone_activation_eligible (0x08086a80) -- 15 slots =====
    # REUSE: gDuelPhaseFlags x2
    (0x08086a78, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_86a78', None),
    (0x08086b20, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_86b20', None),
    # REUSE: EQUIP_PHASE_FRAME_OFF x2
    (0x08086a7c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frm_86a7c', None),
    (0x08086b24, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frm_86b24', None),
    # REUSE: gEquipEffectZoneTable x3
    (0x08086b28, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86b28', None),
    (0x08086c00, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86c00', None),
    (0x08086c6c, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86c6c', None),
    # REUSE: PLAYER_BLOCK_STRIDE x3
    (0x08086b2c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86b2c', None),
    (0x08086c04, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86c04', None),
    (0x08086c34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_86c34', None),
    # REUSE: gDuelFieldSlots x2
    (0x08086b30, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_86b30', None),
    (0x08086c08, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_86c08', None),
    # REUSE: EARTH_CHANT_CID x1
    (0x08086b48, 0x00001716, 'EARTH_CHANT_CID',
     'earth_chant_cid_86b48', None),
    # REUSE: END_OF_WORLD_CID x1
    (0x08086bfc, 0x000019d9, 'END_OF_WORLD_CID',
     'end_of_world_cid_86bfc', None),
    # REUSE: gP1FieldArrayCBase x1
    (0x08086c0c, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrc_86c0c', None),

    # ===== check_neo_daedalus_equip_zone_eligible (0x08086c80) -- 2 slots =====
    # REUSE: MASK_OF_RESTRICT_CID=0x000013f2 (card_info.inc) x1
    (0x08086ca0, 0x000013f2, 'MASK_OF_RESTRICT_CID',
     'mask_restrict_cid_86ca0', None),
    # REUSE: gEquipEffectZoneTable x1
    (0x08086cd8, 0x09e5a0c4, 'gEquipEffectZoneTable',
     'gequipeffzone_86cd8', None),

    # ===== disasm-block internal literal pool: equip_slot_casea_body (0x080863cc) =====
    # REUSE: ELIGIB_SPRITE_CTRL_OFF=0x00001d68 (ewram.inc L422) x1
    # pool slot at 0x080863f8 inside ROM_INCBIN block (disasm will createDWord it)
    (0x080863f8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_spr_ctrl_863f8', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_val, gas_label, slot_label, eol_or_None)
#    4 total
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # dispatch_field_display_state_by_type: internal switchdata ptr
    (0x08085d7c, 0x08085d80,
     'switchD_08085d70__switchdataD_08085d80',
     'dispatch_field_switchdata_base_ptr',
     'dispatch_field_display_state_by_type switch data base ptr'),

    # dispatch_field_display_state_by_type: game_text_sep_record ptr
    (0x08085ef8, 0x09e3f14c,
     'game_text_sep_record',
     'game_text_sep_ptr',
     'ptr to game_text_sep_record (0x09e3f14c)'),

    # dispatch_equip_slot_state_by_index: pointer-to-pointer for jump table
    (0x08086170, 0x08086174,
     'equip_slot_state_jt_base',
     'equip_slot_state_jt_ptr_ptr',
     'ptr-to-ptr for equip slot state jump table (11 entries)'),

    # dispatch_equip_slot_state_by_index: first jump table entry ptr
    (0x08086174, 0x080861a0,
     'equip_slot_case0_body',
     'equip_slot_state_case0_base',
     'jump table entry [0]: equip_slot_case0_body @ 0x080861a0'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, new_label, eol)
#    8 PTR_gP1LifePoints_ slots -- snake_case label rename
# ---------------------------------------------------------------------------
_LP_EOL = 'gP1LifePoints pool (dispatch_field_display_state_by_type / dispatch_equip_slot_state_by_index / eval_equip_slot_score_in_range)'
RENAME_SLOTS = [
    (0x08085f44, 'gp1lp_ptr_08085f44', _LP_EOL),
    (0x08085f8c, 'gp1lp_ptr_08085f8c', _LP_EOL),
    (0x08086060, 'gp1lp_ptr_08086060', _LP_EOL),
    (0x080860b8, 'gp1lp_ptr_080860b8', _LP_EOL),
    (0x080860f8, 'gp1lp_ptr_080860f8', _LP_EOL),
    (0x080864d8, 'gp1lp_ptr_080864d8', _LP_EOL),
    (0x08086560, 'gp1lp_ptr_08086560', _LP_EOL),
    (0x08086838, 'gp1lp_ptr_08086838', _LP_EOL),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (fn_addr, plate_text)
#    12 total: 7 in-segment + 5 cross-file
#    All text ASCII only.
#    PLATE WARN=FAIL
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # ---- In-segment plates (7) ----

    # 1. dispatch_equip_slot_state_by_index @ 0x0808611c
    #    Fix: FUN_080a0a8c -> route_equip_slot_tick_by_flag
    (0x0808611c,
     "Called by route_equip_slot_tick_by_flag (equip slot flag router) when bit4 check passes"
     " and bit2 sub-branch hits. Reads current equip slot index from gP1LifePoints+0x594,"
     " reads auxiliary data at 0x0201b290+slot*0x18+0xba*4. Dispatches to sub-state handler"
     " via jump table (PTR_PTR_08086170, 11 entries [0..0xa]) using slot index as key."
     " Out-of-range index (>0xa) returns r0=1 (LAB_0808641a: movs r0,#0x1)."
     " Sub-function writes handled by jump table targets.\n"
     "\n"
     "Constants: gP1LifePoints=0x0201b290, slot_index_offset=0x594,"
     " aux_base_offset=0x58c, jump_table=0x08086174 (11 entries [0..0xa])."),

    # 2. check_equip_target_slot_by_card_id @ 0x08086430
    #    Fix: FUN_08086a80 -> eval_equip_zone_activation_eligible
    (0x08086430,
     "Equip target slot eligibility check by card_id: r0=card_id, r1=effect_record_index."
     " Reads a DWORD from the ROM effect record table (0x09e5a0c4) at r1*4 offset,"
     " extracts bits[25..13] as the record's card_id; if equal to r0 returns 1 (exact match)."
     " If r0==0x1698 (Contract with the Abyss), validates via check_card_stat_field7_equals(card_id, 2);"
     " if r0==0x1716 (Earth Chant), validates field7==5. All other cases return 0."
     " Called by eval_equip_zone_activation_eligible (equip zone activation scan) as a pre-check"
     " for 'does the equip target satisfy special card rules'.\n"
     "Side effects: none.\n"
     "Constants: CONTRACT_WITH_ABYSS=0x1698, EARTH_CHANT=0x1716, EFFECT_TABLE_BASE=0x09e5a0c4."),

    # 3. find_equip_target_in_effect_zones @ 0x0808647c
    #    Fix: FUN_08086a80 -> eval_equip_zone_activation_eligible
    (0x0808647c,
     "Scan effect zones for a valid equip target: r0=player_id (bit0), r1=target_card_id."
     " Computes player_stride=(player_id&1)*0x868, reads zone count from gP1LifePoints+0xc."
     " Outer loop r4=[0..zone_count-1]; for each zone reads card_id from ROM effect table"
     " 0x09e5a0c4+player_stride+zone_idx*4, compares bits[12..0] against r1 (target_card_id);"
     " on match calls check_card_targeted_by_spell_zone_effect and returns 1 (found) if it"
     " returns 0 (not already targeted). Returns 0 if no eligible target found."
     " Called by eval_equip_zone_activation_eligible (equip zone activation scan).\n"
     "Side effects: none.\n"
     "Constants: gP1LifePoints=0x0201c4e0, PLAYER_STRIDE=0x868, EFFECT_TABLE=0x09e5a0c4."),

    # 4. sum_equip_zone_bonus_scores_for_player @ 0x08086508
    #    Fix: FUN_08086c80 -> check_neo_daedalus_equip_zone_eligible
    #         FUN_08086634 -> eval_equip_slot_score_in_range
    (0x08086508,
     "Sum equip zone bonus scores for a player: r0=player_id (bit0, saved via r8/r9),"
     " r1=equip_card_id (r9). Uses player_stride=r1&1*0x868+gDuelEffectZones(0x0201c600)"
     " as base, iterates over zone_count effect zone slots. For each slot: reads card_field5"
     " (bits[12..0]); if check_card_field5_is_nonzero returns nonzero and card_field5!=player_id,"
     " calls eval_equip_bonus_for_slot and accumulates result into r10. Caller reads total from r10."
     " Called by check_neo_daedalus_equip_zone_eligible (equip scoring chain)"
     " and eval_equip_slot_score_in_range.\n"
     "Side effects: none (read-only; computation via eval_equip_bonus_for_slot).\n"
     "Constants: gDuelEffectZones=0x0201c600, PLAYER_STRIDE=0x868."),

    # 5. sum_equip_chain_scores_for_card @ 0x080865ac
    #    Fix: FUN_08086c80 -> check_neo_daedalus_equip_zone_eligible
    (0x080865ac,
     "Sum equip chain scores for a card as equip target: r0=card_slot_ptr (r7)."
     " Double loop: outer r5=[0..1] (player), inner r4=[0..4] (slot_idx)."
     " For each (player, slot): calls check_slot_card_can_be_equipped(r7, r5, r4);"
     " if equippable, calls query_slot_effect_eligibility_nonzero(r5, r4, 0) to confirm"
     " effect eligibility (returns 0=eligible); if both pass and target is not self (r7!=r5),"
     " checks gDuelCardSlots[offset+8]!=0, then calls eval_equip_chain_score_for_slot(r5, r4)"
     " and accumulates into r9. Caller reads total from r9."
     " Called by check_neo_daedalus_equip_zone_eligible (equip chain scoring).\n"
     "Side effects: none.\n"
     "Constants: gDuelCardSlots=0x0201c510, PLAYER_STRIDE=0x868."),

    # 6. check_sorted_array_value_in_range @ 0x08086954
    #    Fix: FUN_08086634 -> eval_equip_slot_score_in_range
    (0x08086954,
     "Recursive range membership test on a sorted array: checks whether the sorted array"
     " (r0=base, r1=count) contains any element E satisfying r2 <= E < r2+r3."
     " Algorithm: iterates from index r1 toward 0; if arr[i] >= r2, checks arr[i] < r2+r3"
     " (r3 can be narrowed by min(arr[i], r6)); if arr[i] < r2, recurses with r1-1;"
     " any match returns 1, exhausted scan returns 0."
     " Called by eval_equip_slot_score_in_range (equip target eligibility evaluation):"
     " caller first pushes qualifying slot word values onto stack, then calls this function"
     " to check whether any stack array value falls in [r2..r2+r3).\n"
     "Side effects: none.\n"
     "Constants: none."),

    # 7. eval_equip_zone_activation_eligible @ 0x08086a80
    #    Fix: FUN_080869a8 -> scan_equip_zones_for_eligible_type11_target
    #         FUN_08086c80 -> check_neo_daedalus_equip_zone_eligible
    (0x08086a80,
     "Determines whether equip zone activation meets eligibility requirements."
     " Runs multiple equip card condition checks: check_equip_target_slot_by_card_id,"
     " find_equip_target_in_effect_zones, eval_equip_slot_score_in_range,"
     " sum_equip_zone_bonus_scores_for_player, sum_equip_chain_scores_for_card,"
     " and special card checks for Earth Chant (0x1716) and End of the World (0x19d9).\n"
     "Compares accumulated equip_score against threshold (slot_byte[+3]>>2);"
     " returns 1 if score >= threshold (eligible), 0 otherwise.\n"
     "Called by scan_equip_zones_for_eligible_type11_target ([equip, zone_scan])"
     " and check_neo_daedalus_equip_zone_eligible ([equip, chain_score]).\n"
     "\n"
     "Constants:\n"
     "- CARD_ID_EARTH_CHANT = 0x1716 (Earth Chant)\n"
     "- CARD_ID_END_OF_WORLD = 0x19d9 (End of the World)"),

    # ---- Cross-file plates (5) ----

    # 8. invoke_card_display_op_0x31_with_params @ asm/11 L18359 (0x080933c8)
    #    Fix: FUN_08085d4c -> dispatch_field_display_state_by_type
    (0x080933c8,
     "4-instruction thunk: reorders r0/r1 as dispatch_card_display_op args."
     " Fixed op=0x31 (copy_game_text_to_card_name_vram), sub1=0x2."
     " Actual call: dispatch_card_display_op(0x31, 0x2, r0_in, r1_in)."
     " Sibling of invoke_card_display_op_0x31 (0x0809355c) which uses fixed 4-arg form."
     " r0=ptr card_slot_ptr (becomes dispatch r2); r1=u32 sub_param (becomes dispatch r3)."
     " Callers: FUN_0804ce78 (card name display), dispatch_field_display_state_by_type"
     " (effect slot render)."),

    # 9. init_equip_card_sprite_row_entry @ asm/12 L3441 (0x08095ba8)
    #    Fix: FUN_08085d4c -> dispatch_field_display_state_by_type
    (0x08095ba8,
     "Initializes OAM sprite row entry for an equip card."
     " Reads player_bit from [gP1LifePoints+0x1d68], base_slot_a from [+0x1d6c],"
     " slot_b from [+0x1d70]; slot_idx = slot_a + slot_b."
     " If slot[+0x38]==0 (not yet rendered): calls enqueue_zone_card_sprite_attr_by_slot."
     " Else: builds OAM attr0 word and calls init_card_sprite_row_entry_alt or"
     " init_card_sprite_row_entry (fallback). Clears [gP1LifePoints+0x1d54]=0 at end."
     " r0=u32 context_extra (saved to r8 via .hword 0x4680=mov r8,r0). Returns void."
     " Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_stride=0x14,"
     " slot_rendered_offset=0x38; gP1LifePoints offsets 0x1d44/0x1d48/0x1d54/0x1d68/0x1d6c/0x1d70."
     " Callers: FUN_0804ce78, dispatch_field_display_state_by_type (equip card display sequence)."),

    # 10. trigger_lp_bar_animation_if_ready @ asm/12 L3570 (0x08095ca0)
    #     Fix: FUN_08085d4c -> dispatch_field_display_state_by_type
    (0x08095ca0,
     "Gate function for LP bar animation."
     " Reads gP1LifePoints+0x1d44; if equal to 0x0fee, calls dispatch_lp_bar_animation_step"
     "(r0=1, r1=0, r2=0) and jumps to shared tail LAB_08095d32."
     " Otherwise (LAB_08095ccc): writes 1 to 0x0201b290+0x9a*8 (sprite buffer flag);"
     " reads [gP1LifePoints+0x1d68], calls render_field_card_copy_count;"
     " if r0!=0 calls init_card_sprite_row_entry_alt else init_card_sprite_row_entry;"
     " writes 0 to [gP1LifePoints+0x1d54] (pending flag clear)."
     " r0=u32 player_bit_field (bit0=player_id [0..1]). Returns void."
     " Callers: FUN_0804ce78, dispatch_field_display_state_by_type."
     " Constants: trigger_sentinel=0x0fee, sprite_buf_flag_addr=0x0201b290+0x4d0."),

    # 11. dispatch_lp_bar_animation_step @ asm/12 L3694 (0x08095d84)
    #     Fix: FUN_08085d4c -> dispatch_field_display_state_by_type
    (0x08095d84,
     "LP bar animation state machine single-frame dispatcher."
     " Reads state word at gP1LifePoints+0x1d60 (offset 0xeb<<5) and dispatches:"
     " state=0: calls render_monster_slot_card_with_lp_bar, writes result to +0x1d74, advances state;"
     " state=1: sets state to 2, skips render;"
     " other: r3!=0 -> init_card_sprite_row_entry_alt, r1==0 -> init_card_sprite_row_entry."
     " Clears pending flag at gP1LifePoints+0x1d54 on exit."
     " r0=u32 anim_mode [0..2]; r1=u32 use_alt_entry [0..1]; r2=ptr row_entry_ptr. Returns void."
     " Callers: FUN_0804ce78, dispatch_field_display_state_by_type,"
     " trigger_lp_bar_animation_if_ready (r0=1,r1=0,r2=0)."
     " Constants: state_offset=0x1d60, result_offset=0x1d74, pending_flag_offset=0x1d54."),

    # 12. dispatch_effect_slot_by_display_state @ asm/12 L3868 (0x08095ec4)
    #     Fix: FUN_08085d4c -> dispatch_field_display_state_by_type
    (0x08095ec4,
     "Reads [gP1LifePoints+0x1d60] (0xeb<<5) display state; dispatches 0/1/2:"
     " state==0: trigger_card_display_op31_if_not_active(r6, 0x114);"
     " state==1: init_effect_slot_display_context(r6, 6, r7) then state++;"
     " state==2: reads monster slot fields via get_monster_slot_entry_ptr x3,"
     " calls dispatch_to_effect_handler_by_card_type, clears [gP1LifePoints+0x1d54]=0."
     " r1=u32 context_ptr (saved as r6); r2=u32 sub_param. Returns void."
     " Side effects: [gP1LifePoints+0x1d60]+=1 (state 0/1); [gP1LifePoints+0x1d54]=0 (state 2)."
     " Caller: dispatch_field_display_state_by_type (effect slot display update driver)."),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF11Seg2Slots (DRY=%s) ===" % DRY)
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    eq_ok = eq_fail = 0
    ref_ok = ref_fail = 0
    ren_ok = ren_fail = 0
    plt_ok = plt_fail = 0

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    seen = set()
    for (slot_addr, value, eq_name, slot_label, eol) in EQ_SLOTS:
        if slot_addr in seen:
            print("[SKIP dup] 0x%08x" % slot_addr)
            continue
        seen.add(slot_addr)
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for (slot_addr, target_val, gas_label, slot_label, eol) in REF_SLOTS:
        if _apply_ref(slot_addr, target_val, gas_label, slot_label, eol):
            ref_ok += 1
        else:
            ref_fail += 1

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for (slot_addr, slot_label, eol) in RENAME_SLOTS:
        if _apply_rename(slot_addr, slot_label, eol):
            ren_ok += 1
        else:
            ren_fail += 1

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    for (fn_addr, plate_text) in PLATE_REWRITES:
        if _apply_plate(fn_addr, plate_text):
            plt_ok += 1
        else:
            plt_fail += 1

    print("\n=== RefineF11Seg2Slots DONE ===")
    print("  EQ=%d/%d  REF=%d/%d  RENAME=%d/%d  PLATE=%d/%d" % (
        eq_ok, len(EQ_SLOTS),
        ref_ok, len(REF_SLOTS),
        ren_ok, len(RENAME_SLOTS),
        plt_ok, len(PLATE_REWRITES)))
    total_fail = eq_fail + ref_fail + ren_fail + plt_fail
    print("  FAIL total: %d" % total_fail)


main()
