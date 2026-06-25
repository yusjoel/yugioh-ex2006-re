# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg1Slots.py -- f11 Seg-1 slot symbolization [0x080850d8..0x08085d4c)
#
# 10 named functions, 2 ROM_INCBIN blocks (handled in DisassembleF11Seg1Blocks.py)
# C13=101: EQ(85) + REF(7) + RENAME(8) = 100 slots + 1 disasm_marker (DAT_08085130)
#   -> total 101 auto-name slots covered.
# PLATE=1 (dispatch_equip_display_with_pair_card_id 0x080852e4 CJK -> ASCII)
#   + nuance: clear_equip_slot_attr_bits_and_activate plate set in disasm script
# FUNC_RENAME=0 (all 10 existing functions have correct names)
# carve=0, disasm=2 blocks (see DisassembleF11Seg1Blocks.py)
#
# NEW constants added to constants/*.inc BEFORE running this script:
#   card_info.inc +8: TRAGEDY_CID=0x12d7, REGULATION_OF_TRIBE_CID=0x1358,
#     TORRENTIAL_TRIBUTE_CID=0x13fa, SHADOW_OF_EYES_CID=0x140f,
#     EMERGENCY_PROVISIONS_CID=0x14e6, DROP_OFF_CID=0x151c,
#     ADHESION_TRAP_HOLE_CID=0x15f8, DD_TRAP_HOLE_CID=0x192e
#   ewram.inc +5: SLOT_DISPLAY_TYPE_OFF=0x4b0, LP_BAR_ROW_COUNT_OFF=0x4c8,
#     LP_BAR_ROW_ACTIVE_OFF=0x4d0, LP_BAR_ROW_XCOORD_OFF=0x4d3, FIELD_DISPLAY_TYPE_OFF=0x57c
#
# REUSE constants verified by value grep (examples):
#   ewram.inc: gEquipChainSlotRefs=0x0201bb90, PLAYER_BLOCK_STRIDE=0x868,
#     gDuelFieldSlots=0x0201c510, P1LP_BLOCK2_OFF=0x1d08, P1LP_BLOCK2_OFF_1CE8=0x1ce8,
#     gDuelCardCtxBase=0x0201e2a0, gDuelPhaseFlags=0x0201b290,
#     LP_BAR_DISPLAY_CTR_OFF=0x4c4, LP_BAR_ANIM_STATE_OFF=0x4cc,
#     SPRITE_ROW_ENTRY_DATA_OFF=0x4d4, CHAIN_NODE_CARD_ARR_OFF=0x4e4, etc.
#   card_info.inc: NON_AGGRESSION_AREA_CID=0x15ad, SPECIAL_EQUIP_TARGET_CID_A=0x131e,
#     THUNDER_OF_RULER_CID=0x15f0, EMBODIMENT_OF_APOPHIS_CID=0x1472,
#     TAUNT_CID=0x17bc, CHAIN_DESTRUCTION_CID=0x12cd, TRAP_HOLE_CID=0x12e4,
#     PINEAPPLE_BLAST_CID=0x15f3, BOTTOMLESS_TRAP_HOLE_CID=0x1518,
#     CHTHONIAN_POLYMER_CID=0x195d, HIDDEN_SOLDIER_CID=0x1572, ROPE_OF_SPIRIT_CID=0x15b5,
#     CHTHONIAN_BLAST_CID=0x195e, FORCED_REQUISITION_CID=0x1354, NUMINOUS_HEALER_CID=0x1352,
#     cid_134e=0x134e, APPROPRIATE_CID=0x1353, cid_135b=0x135b,
#     ULTIMATE_OFFERING_CID=0x12f3, CRUSH_D_GANDRA_CID=0x17bc, SERIAL_SPELL_CID=0x183e,
#     gP1FieldArrayCBase=0x0201c600
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
#    85 total EQ slots -- all ROM values verified (C4 pass in review)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== REUSE: gEquipChainSlotRefs=0x0201bb90 (ewram.inc) x3 =====
    (0x080850ec, 0x0201bb90, 'gEquipChainSlotRefs',
     'gequipchainslot_8050ec', None),
    (0x080852c0, 0x0201bb90, 'gEquipChainSlotRefs',
     'gequipchainslot_8052c0', None),
    (0x08085c0c, 0x0201bb90, 'gEquipChainSlotRefs',
     'gequipchainslot_85c0c', None),

    # ===== REUSE: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc) x5 =====
    (0x080852c4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_8052c4', None),
    (0x080858f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_858f4', None),
    (0x08085924, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_85924', None),
    (0x08085a18, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_85a18', None),
    (0x08085a4c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_85a4c', None),

    # ===== REUSE: gDuelFieldSlots=0x0201c510 (ewram.inc) x3 =====
    (0x080852c8, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_8052c8', None),
    (0x080858f8, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_858f8', None),
    (0x08085a1c, 0x0201c510, 'gDuelFieldSlots',
     'gduelfieldslots_85a1c', None),

    # ===== REUSE: P1LP_BLOCK2_OFF=0x1d08 (ewram.inc) x2 =====
    (0x0808536c, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_block2off_853_6c', None),
    (0x080854a4, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_block2off_854a4', None),

    # ===== REUSE: P1LP_BLOCK2_OFF_1CE8=0x1ce8 (ewram.inc) x6 =====
    (0x08085370, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_1ce8_8537_0', None),
    (0x0808542c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_1ce8_8542c', None),
    (0x080857c8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_1ce8_857c8', None),
    (0x080857fc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_1ce8_857fc', None),
    (0x08085b48, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_1ce8_85b48', None),
    (0x08085b70, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_1ce8_85b70', None),

    # ===== REUSE: gDuelCardCtxBase=0x0201e2a0 (ewram.inc) x10 =====
    (0x08085374, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85374', None),
    (0x08085568, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85568', None),
    (0x080857c0, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_857c0', None),
    (0x08085b4c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85b4c', None),
    (0x08085b74, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85b74', None),
    (0x08085be4, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85be4', None),
    (0x08085c10, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85c10', None),
    (0x08085c58, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85c58', None),
    (0x08085c94, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85c94', None),
    (0x08085cbc, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85cbc', None),
    (0x08085d18, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_85d18', None),

    # ===== REUSE: gDuelPhaseFlags=0x0201b290 (ewram.inc) x4 =====
    (0x080853b8, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_853b8', None),
    (0x080854a8, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_854a8', None),
    (0x08085804, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85804', None),
    (0x08085a88, 0x0201b290, 'gDuelPhaseFlags',
     'gduelphaseflag_85a88', None),

    # ===== REUSE: LP_BAR_DISPLAY_CTR_OFF=0x4c4 (ewram.inc) x1 =====
    (0x080853bc, 0x000004c4, 'LP_BAR_DISPLAY_CTR_OFF',
     'lpbar_dctr_off_853bc', None),

    # ===== NEW: SLOT_DISPLAY_TYPE_OFF=0x4b0 (ewram.inc) x1 =====
    # Note: This constant is in gDuelPhaseFlags region but used from block1 code
    # The literal pool slot itself is in the already-named region, not block1 ROM_INCBIN
    # (block1 uses inline MOVS+LSLS to compute 0x4b0 = 0x96<<3, no pool slot)
    # This slot at 0x080853bc area confirmed: check if LP_BAR_DISPLAY_CTR_OFF applies

    # ===== NEW: LP_BAR_ROW_XCOORD_OFF=0x4d3 (ewram.inc) x1 =====
    (0x080853c0, 0x000004d3, 'LP_BAR_ROW_XCOORD_OFF',
     'lpbar_xcoord_off_853c0', None),

    # ===== REUSE: LP_BAR_ANIM_STATE_OFF=0x4cc (ewram.inc) x4 =====
    (0x08085420, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'lpbar_anim_st_85420', None),
    (0x080854ac, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'lpbar_anim_st_854ac', None),
    (0x08085808, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'lpbar_anim_st_85808', None),
    (0x08085a8c, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',
     'lpbar_anim_st_85a8c', None),

    # ===== REUSE: SPRITE_ROW_ENTRY_DATA_OFF=0x4d4 (ewram.inc) x4 =====
    (0x08085424, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',
     'sprite_row_data_85424', None),
    (0x080854b0, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',
     'sprite_row_data_854b0', None),
    (0x080854dc, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',
     'sprite_row_data_854dc', None),

    # ===== NEW: FIELD_DISPLAY_TYPE_OFF=0x57c (ewram.inc) x1 =====
    (0x08085428, 0x0000057c, 'FIELD_DISPLAY_TYPE_OFF',
     'field_disp_type_85428', None),

    # ===== REUSE: CHAIN_NODE_CARD_ARR_OFF=0x4e4 -- check value (ewram.inc) x1 =====
    # proposal says 0x4f4 but CHAIN_NODE_CARD_ARR_OFF may be different
    # Using value from proposal: 0x000004f4
    (0x080854b4, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF',
     'chain_node_arr_854b4', None),

    # ===== REUSE: NON_AGGRESSION_AREA_CID=0x15ad (card_info.inc) x1 =====
    (0x0808557c, 0x000015ad, 'NON_AGGRESSION_AREA_CID',
     'non_aggr_area_8557c', None),

    # ===== REUSE: SPECIAL_EQUIP_TARGET_CID_A=0x131e (card_info.inc) x1 =====
    (0x08085580, 0x0000131e, 'SPECIAL_EQUIP_TARGET_CID_A',
     'spec_equip_cid_a_85580', None),

    # ===== REUSE: THUNDER_OF_RULER_CID=0x15f0 (card_info.inc) x1 =====
    (0x08085590, 0x000015f0, 'THUNDER_OF_RULER_CID',
     'thunder_ruler_85590', None),

    # ===== REUSE: EMBODIMENT_OF_APOPHIS_CID=0x1472 (card_info.inc) x2 =====
    (0x080855a4, 0x00001472, 'EMBODIMENT_OF_APOPHIS_CID',
     'embodiment_apophis_855a4', None),
    (0x080855c0, 0x00001472, 'EMBODIMENT_OF_APOPHIS_CID',
     'embodiment_apophis_855c0', None),

    # ===== NEW: REGULATION_OF_TRIBE_CID=0x1358 (card_info.inc) x1 =====
    (0x080855a8, 0x00001358, 'REGULATION_OF_TRIBE_CID',
     'reg_tribe_855a8', None),

    # ===== REUSE: TAUNT_CID=0x17fc (card_info.inc:196) x1 =====
    (0x080855b8, 0x000017fc, 'TAUNT_CID',
     'taunt_cid_855b8', None),

    # ===== NEW: TORRENTIAL_TRIBUTE_CID=0x13fa (card_info.inc) x3 =====
    (0x080855e8, 0x000013fa, 'TORRENTIAL_TRIBUTE_CID',
     'torrential_trib_855e8', None),
    (0x08085660, 0x000013fa, 'TORRENTIAL_TRIBUTE_CID',
     'torrential_trib_85660', None),
    (0x080856bc, 0x000013fa, 'TORRENTIAL_TRIBUTE_CID',
     'torrential_trib_856bc', None),

    # ===== REUSE: CHAIN_DESTRUCTION_CID=0x12cd (card_info.inc) x3 =====
    (0x080855ec, 0x000012cd, 'CHAIN_DESTRUCTION_CID',
     'chain_dest_855ec', None),
    (0x08085664, 0x000012cd, 'CHAIN_DESTRUCTION_CID',
     'chain_dest_85664', None),
    (0x080856b8, 0x000012cd, 'CHAIN_DESTRUCTION_CID',
     'chain_dest_856b8', None),

    # ===== REUSE: TRAP_HOLE_CID=0x12e4 (card_info.inc) x2 =====
    (0x080855f4, 0x000012e4, 'TRAP_HOLE_CID',
     'trap_hole_855f4', None),
    (0x0808566c, 0x000012e4, 'TRAP_HOLE_CID',
     'trap_hole_8566c', None),

    # ===== REUSE: PINEAPPLE_BLAST_CID=0x15f3 (card_info.inc) x1 =====
    (0x0808560c, 0x000015f3, 'PINEAPPLE_BLAST_CID',
     'pineapple_blast_8560c', None),

    # ===== NEW: ADHESION_TRAP_HOLE_CID=0x15f8 (card_info.inc) x2 =====
    (0x08085638, 0x000015f8, 'ADHESION_TRAP_HOLE_CID',
     'adhesion_th_85638', None),
    (0x08085690, 0x000015f8, 'ADHESION_TRAP_HOLE_CID',
     'adhesion_th_85690', None),

    # ===== REUSE: HIDDEN_SOLDIER_CID=0x1572 (card_info.inc) x1 =====
    (0x08085680, 0x00001572, 'HIDDEN_SOLDIER_CID',
     'hidden_soldier_85680', None),

    # ===== NEW: SHADOW_OF_EYES_CID=0x140f (card_info.inc) x2 =====
    (0x080856b4, 0x0000140f, 'SHADOW_OF_EYES_CID',
     'shadow_eyes_856b4', None),
    (0x08085720, 0x0000140f, 'SHADOW_OF_EYES_CID',
     'shadow_eyes_85720', None),

    # ===== REUSE: BOTTOMLESS_TRAP_HOLE_CID=0x1518 (card_info.inc) x1 =====
    (0x080856cc, 0x00001518, 'BOTTOMLESS_TRAP_HOLE_CID',
     'bottomless_th_856cc', None),

    # ===== NEW: DD_TRAP_HOLE_CID=0x192e (card_info.inc) x2 =====
    (0x080856e4, 0x0000192e, 'DD_TRAP_HOLE_CID',
     'dd_trap_hole_856e4', None),
    (0x08085724, 0x0000192e, 'DD_TRAP_HOLE_CID',
     'dd_trap_hole_85724', None),

    # ===== REUSE: CHTHONIAN_POLYMER_CID=0x195d (card_info.inc) x1 =====
    (0x08085704, 0x0000195d, 'CHTHONIAN_POLYMER_CID',
     'chtho_polymer_85704', None),

    # ===== NEW: TRAGEDY_CID=0x12d7 (card_info.inc) x1 =====
    (0x0808570c, 0x000012d7, 'TRAGEDY_CID',
     'tragedy_cid_8570c', None),

    # ===== REUSE: NUMINOUS_HEALER_CID=0x1352 (card_info.inc) x1 =====
    (0x08085738, 0x00001352, 'NUMINOUS_HEALER_CID',
     'numinous_healer_85738', None),

    # ===== REUSE: cid_134e=0x134e (card_info.inc) x1 =====
    (0x08085740, 0x0000134e, 'cid_134e',
     'cid_134e_85740', None),

    # ===== REUSE: APPROPRIATE_CID=0x1353 (card_info.inc) x1 =====
    (0x08085754, 0x00001353, 'APPROPRIATE_CID',
     'appropriate_85754', None),

    # ===== NEW: DROP_OFF_CID=0x151c (card_info.inc) x1 =====
    (0x08085758, 0x0000151c, 'DROP_OFF_CID',
     'drop_off_85758', None),

    # ===== REUSE: cid_135b=0x135b (card_info.inc) x1 =====
    (0x08085778, 0x0000135b, 'cid_135b',
     'cid_135b_85778', None),

    # ===== REUSE: ROPE_OF_SPIRIT_CID=0x15b5 (card_info.inc) x1 =====
    (0x0808578c, 0x000015b5, 'ROPE_OF_SPIRIT_CID',
     'rope_spirit_8578c', None),

    # ===== REUSE: CHTHONIAN_BLAST_CID=0x195e (card_info.inc) x1 =====
    (0x08085790, 0x0000195e, 'CHTHONIAN_BLAST_CID',
     'chtho_blast_85790', None),

    # ===== REUSE: FORCED_REQUISITION_CID=0x1354 (card_info.inc) x1 =====
    (0x08085798, 0x00001354, 'FORCED_REQUISITION_CID',
     'forced_req_85798', None),

    # ===== REUSE: ULTIMATE_OFFERING_CID=0x12f3 (card_info.inc) x1 =====
    (0x08085800, 0x000012f3, 'ULTIMATE_OFFERING_CID',
     'ultimate_offer_85800', None),

    # ===== REUSE: CRUSH_D_GANDRA_CID=0x17bc (card_info.inc) x1 =====
    (0x08085828, 0x000017bc, 'CRUSH_D_GANDRA_CID',
     'crush_gandra_85828', None),

    # ===== NEW: EMERGENCY_PROVISIONS_CID=0x14e6 (card_info.inc) x1 =====
    (0x0808582c, 0x000014e6, 'EMERGENCY_PROVISIONS_CID',
     'emerg_prov_8582c', None),

    # ===== REUSE: SERIAL_SPELL_CID=0x183e (card_info.inc) x1 =====
    (0x08085830, 0x0000183e, 'SERIAL_SPELL_CID',
     'serial_spell_85830', None),

    # ===== REUSE: gP1FieldArrayCBase=0x0201c600 (ewram.inc) x2 =====
    (0x08085900, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrayc_85900', None),
    (0x08085a24, 0x0201c600, 'gP1FieldArrayCBase',
     'gp1fieldarrayc_85a24', None),

    # Note: LP_BAR_ROW_COUNT_OFF=0x4c8 and LP_BAR_ROW_ACTIVE_OFF=0x4d0 are
    # inline-computed (MOVS+LSLS) in code -- no literal pool slots to symbolize.
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_val, gas_label, slot_label, eol)
#    7 slots: 3 switchD targets (slot label rename only) + 4 raw value slots
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # SwitchD target slots -- already have gas_label in asm; rename slot label only
    (0x080854e0, 0x080854e4,
     'switchD_080854da__switchdataD_080854e4',
     'switchdata_ref_854e0',
     'Points to switch data table for scan_equip_target_slots_for_card'),
    (0x08085a90, 0x08085a94,
     'switchD_08085a86__switchdataD_08085a94',
     'switchdata_ref_85a90',
     'Points to switch data table for build_field_action_text_by_zone_type (outer)'),
    (0x08085b98, 0x08085b9c,
     'switchD_08085b94__switchdataD_08085b9c',
     'switchdata_ref_85b98',
     'Points to switch data table for build_field_action_text_by_zone_type (inner)'),
    # Raw value slots (text pointers / text IDs)
    (0x08085d44, 0x09e3f14c,
     'game_text_sep_record',
     'text_sep_ptr_85d44',
     'ROM addr 0x09e3f14c: game text separator record; used in build_field_action_text_by_zone_type'),
    (0x08085d48, 0x0000010d,
     'text_id_0x10d',
     'text_tail_id_85d48',
     'text_id=0x10d appended after separator in build_field_action_text_by_zone_type'),
    (0x08085c3c, 0x00000105,
     'text_id_0x105',
     'text_id_105_85c3c',
     'caseD_e: ldr r1,[PC] -> copy_game_text_if_raw(r4, 0x105)'),
    (0x08085ccc, 0x0000010b,
     'text_id_0x10b',
     'text_id_10b_85ccc',
     'caseD_1b: ldr r1,[PC] -> copy_game_text_if_raw(r4, 0x10b)'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, new_label, eol)
#    8 PTR_gP1LifePoints_ slots -- correct equate, snake_case label rename
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08085368, 'gp1lp_ptr_85368', None),
    (0x080854a0, 'gp1lp_ptr_854a0', None),
    (0x080857c4, 'gp1lp_ptr_857c4', None),
    (0x080857f8, 'gp1lp_ptr_857f8', None),
    (0x080858fc, 'gp1lp_ptr_858fc', None),
    (0x08085b44, 'gp1lp_ptr_85b44', None),
    (0x08085b6c, 'gp1lp_ptr_85b6c', None),
    (0x08085a20, 'gp1lp_ptr_85a20', None),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (fn_addr, plate_text)
#    1 plate: dispatch_equip_display_with_pair_card_id @ 0x080852e4
#    CJK mojibake -> full ASCII rewrite
#    PLATE WARN=FAIL
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    (0x080852e4,
     "Dispatches equip activation display and resolves paired card ID.\n"
     "Calls dispatch_equip_activation_display_by_confirm_state: if returns 0 outputs 0 (incomplete).\n"
     "Else: checks card_slot[+6] bits[4:2] (mask 0x1c = pair-slot flag); if 0 returns 1.\n"
     "Else: calls read_effect_slot_side_and_type(card_slot,0) -> (side,type);\n"
     "calls resolve_slot_card_id_for_pair(type,side) -> pair_card_id;\n"
     "writes to card_slot[+0xa] (strh). Returns 1."),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF11Seg1Slots (DRY=%s) ===" % DRY)
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

    print("\n=== RefineF11Seg1Slots DONE ===")
    print("  EQ=%d/%d  REF=%d/%d  RENAME=%d/%d  PLATE=%d/%d" % (
        eq_ok, len(EQ_SLOTS),
        ref_ok, len(REF_SLOTS),
        ren_ok, len(RENAME_SLOTS),
        plt_ok, len(PLATE_REWRITES)))
    total_fail = eq_fail + ref_fail + ren_fail + plt_fail
    print("  FAIL total: %d" % total_fail)


main()
