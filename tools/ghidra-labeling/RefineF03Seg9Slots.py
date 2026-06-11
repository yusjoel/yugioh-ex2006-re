# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg9Slots.py -- file 03 Seg-9 (0x0803d91c..0x0803efcc)
#   tick_zone_slot_transition_display_seq .. tick_equip_node_chain_link_display_seq
#   EQ=70 (65 reuse + 5 new), REF=76, RENAME=2, FUNC_RENAME=0, PLATE=10
#   carve=0, disasm=0, §5.1=0
#
# New constants added to .inc files before running this script:
#   card_info.inc: UNHAPPY_GIRL_CID_SHIFTED=0xba180000, BACKFIRE_CID=0x1762,
#                  SOUL_ABSORPTION_CID=0x16da, HUMAN_WAVE_TACTICS_CID=0x17b2
#   duel_field.inc: DISPLAY_CTX_SLOT_DATA_MASK=0x7fff
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _addr(val):
    return toAddr(val)

def _check(slot_addr, expected):
    addr = _addr(slot_addr)
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(addr) & 0xffffffff
        if actual != (expected & 0xffffffff):
            print("WARN: slot 0x%08x expected 0x%08x got 0x%08x -- SKIP" % (slot_addr, expected & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("WARN: slot 0x%08x read error: %s" % (slot_addr, e))
        return False

def _eq(slot_addr, value, eq_name, slot_label, eol=None):
    if not _check(slot_addr, value):
        return
    if DRY:
        print("DRY EQ: 0x%08x %s=%s sl=%s" % (slot_addr, eq_name, hex(value & 0xffffffff), slot_label))
        return
    addr = _addr(slot_addr)
    et = currentProgram.getEquateTable()
    eq = et.getEquate(eq_name)
    if eq is None:
        eq = et.createEquate(eq_name, value & 0xffffffff)
    eq.addReference(addr, 0)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(addr, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _ref(slot_addr, target_addr, gas_label, slot_label, eol=None):
    if DRY:
        print("DRY REF: 0x%08x -> 0x%08x gas=%s sl=%s" % (slot_addr, target_addr, gas_label, slot_label))
        return
    tgt = _addr(target_addr)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(tgt, gas_label, SourceType.USER_DEFINED)
    rm = currentProgram.getReferenceManager()
    src = _addr(slot_addr)
    rm.addMemoryReference(src, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_list = rm.getReferencesFrom(src)
    for r in ref_list:
        if r.getToAddress().equals(tgt):
            rm.setPrimary(r, True)
    sm.createLabel(src, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(src)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _rename(slot_addr, old_label, new_label, eol=None):
    if DRY:
        print("DRY RENAME: 0x%08x %s->%s" % (slot_addr, old_label, new_label))
        return
    addr = _addr(slot_addr)
    sm = currentProgram.getSymbolTable()
    syms = list(sm.getSymbols(addr))
    renamed = False
    for sym in syms:
        if sym.getName() == old_label:
            sym.setName(new_label, SourceType.USER_DEFINED)
            renamed = True
            break
    if not renamed:
        sm.createLabel(addr, new_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

# ---------------------------------------------------------------------------
# A. EQ_SLOTS (70 total: 65 reuse + 5 new)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # === tick_zone_slot_transition_display_seq (0x0803d91c) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc)
    (0x0803d990, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_zone_trans_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868; player data block stride'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803d99c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_zone_trans_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at exit'),

    (0x0803d9d0, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_zone_trans_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === tick_flip_summon_state (0x0803dc34) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803dc80, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_flip_summon_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803dc88, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_flip_summon_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at flip_summon exit'),

    # new: UNHAPPY_GIRL_CID_SHIFTED=0xba180000 (card_info.inc NEW)
    (0x0803de78, 0xba180000, 'UNHAPPY_GIRL_CID_SHIFTED', 'tick_flip_summon_unhappy_girl_shifted_a',
     'UNHAPPY_GIRL_CID(0x1743)<<19; lsls r0,r0,#0x13 then cmp 0xba180000; flip-summon gate'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803de70, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_flip_summon_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: FIELD_STATE_OFF=0x1cf4
    (0x0803de80, 0x1cf4, 'FIELD_STATE_OFF', 'tick_flip_summon_field_state_off_a',
     '[gDuelFieldSlots+0x1cf4] equip activation phase/field state code'),

    # reuse: P1LP_BLOCK2_OFF_1CE8=0x1ce8 (ewram.inc)
    (0x0803de84, 0x1ce8, 'P1LP_BLOCK2_OFF_1CE8', 'tick_flip_summon_lp_block2_1ce8_a',
     '[gP1LifePoints+0x1ce8] LP display block2 field'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803de8c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_flip_summon_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === tick_zone_card_remove_display_seq (0x0803de90) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803df04, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_zone_remove_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803df0c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_zone_remove_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at remove exit'),

    # reuse: SLOT_BIT21_CLR=0xffdfffff
    (0x0803da8c, 0xffdfffff, 'SLOT_BIT21_CLR', 'tick_zone_trans_bit21_clr_a',
     'AND mask clearing bit21 of zone slot word'),

    # reuse: DISP_SEQ_CARD_SET_CTR_OFF=0x818
    (0x0803da94, 0x818, 'DISP_SEQ_CARD_SET_CTR_OFF', 'tick_zone_trans_ctr_off_a',
     '[gDuelDisplaySeqState+0x818] step counter for card-set display'),

    # reuse: OAM_ATTR2_TILE_CLEAR=0xffffe000
    (0x0803da98, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR', 'tick_zone_trans_oam_tile_clear_a',
     'OAM attr2 tile index clear mask'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803db84, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'tick_zone_trans_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803db88, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_zone_trans_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: SLOT_ACTIVE_BIT15_CLR=0xffff7fff
    (0x0803db90, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'tick_zone_trans_bit15_clr_a',
     'AND mask clearing bit15 of zone slot descriptor word'),

    # reuse: SLOT_ACTIVE_BIT14_CLR=0xffffbfff
    (0x0803db94, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'tick_zone_trans_bit14_clr_a',
     'AND mask clearing bit14 of zone slot descriptor word'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803dc18, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_flip_summon_player_stride_c',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: SLOT_CARD_SET_CODE_MASK=0x1fff (card_info.inc)
    (0x0803dc20, 0x1fff, 'SLOT_CARD_SET_CODE_MASK', 'tick_flip_summon_set_code_mask_a',
     '13-bit mask for YGO set_code/card_id fields'),

    # reuse: OAM_ATTR2_TILE_CLEAR=0xffffe000
    (0x0803dc28, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR', 'tick_flip_summon_oam_tile_clear_a',
     'OAM attr2 tile index clear mask'),

    # reuse: DISP_SEQ_CARD_SET_CTR_OFF=0x818
    (0x0803dc2c, 0x818, 'DISP_SEQ_CARD_SET_CTR_OFF', 'tick_flip_summon_ctr_off_a',
     '[gDuelDisplaySeqState+0x818] step counter'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803dc30, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_flip_summon_step_lock_off_c',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === tick_equip_chain_node_link_seq (0x0803e0c4) ===

    # reuse: FIELD_SLOT_COUNT_OFF=0x1cb4
    (0x0803e020, 0x1cb4, 'FIELD_SLOT_COUNT_OFF', 'tick_chain_link_slot_count_off_a',
     '[gDuelFieldSlots+0x1cb4] total placed-card count'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e094, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_chain_link_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e0c0, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_chain_link_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_equip_chain_node_link_seq exit'),

    # new: DISPLAY_CTX_SLOT_DATA_MASK=0x7fff (duel_field.inc NEW)
    (0x0803e0f8, 0x7fff, 'DISPLAY_CTX_SLOT_DATA_MASK', 'tick_chain_link_slot_data_mask_a',
     'masks bit15 from [gDuelDisplaySeqState+4] hword to extract slot_data field'),

    # === tick_zone_slot_ref_clear_display_seq (0x0803e130) ===

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e12c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_ref_clear_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_zone_slot_ref_clear exit'),

    # === tick_zone_chain_node_ref_update_seq (0x0803e170) ===

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e16c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_chain_ref_upd_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_zone_chain_node_ref_update_seq exit'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e1b0, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_chain_ref_upd_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    (0x0803e1d8, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_chain_ref_upd_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # === commit_set_card_to_field_slot (0x0803e228) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e218, 0x868, 'PLAYER_BLOCK_STRIDE', 'commit_set_card_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e224, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'commit_set_card_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at commit_set_card_to_field_slot exit'),

    # === write_zone_slot_display_args_by_state (0x0803e298) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e288, 0x868, 'PLAYER_BLOCK_STRIDE', 'write_zone_args_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: FIELD_SLOT_COUNT_OFF=0x1cb4
    (0x0803e290, 0x1cb4, 'FIELD_SLOT_COUNT_OFF', 'write_zone_args_slot_count_off_a',
     '[gDuelFieldSlots+0x1cb4] total placed-card count'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e294, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'write_zone_args_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at write_zone_slot_display_args exit'),

    # === tick_card_effect_index_display_seq (0x0803e318) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e2d0, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_effect_idx_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    (0x0803e308, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_effect_idx_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e314, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_effect_idx_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_card_effect_index_display_seq exit'),

    # === tick_hand_zone_insert_display_seq (0x0803e474) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e364, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_effect_idx_player_stride_c',
     'PLAYER_BLOCK_STRIDE=0x868'),

    (0x0803e410, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_hand_insert_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e448, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_effect_idx_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock at dispatch_op7 exit'),

    (0x0803e470, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_hand_insert_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_hand_zone_insert_display_seq exit'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e524, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_hand_insert_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # === tick_zone_card_place_with_slot_resolve_seq (0x0803e594) ===

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803e590, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_hand_insert_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    (0x0803e6b0, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_zone_slot_resolve_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_zone_card_place_with_slot_resolve exit'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803e9ec, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_zone_slot_resolve_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: A_DEAL_WITH_DARK_RULER_CID=0x165a
    (0x0803e9f0, 0x165a, 'A_DEAL_WITH_DARK_RULER_CID', 'tick_zone_slot_resolve_dark_ruler_a',
     'A Deal with Dark Ruler (pw=06850209; card_1330 slot=0x165A); chain node type arg'),

    # new: BACKFIRE_CID=0x1762 (card_info.inc NEW)
    (0x0803e9f8, 0x1762, 'BACKFIRE_CID', 'tick_zone_slot_resolve_backfire_a',
     'Backfire (pw=82705573; card_1547 slot=0x1762); equip chain gate check'),

    # reuse: BOSS_RUSH_CID=0x1972
    (0x0803e9fc, 0x1972, 'BOSS_RUSH_CID', 'tick_zone_slot_resolve_boss_rush_a',
     'Boss Rush (pw=66947414; card_1983 slot=0x1972); effect zone count gate'),

    # new: SOUL_ABSORPTION_CID=0x16da (card_info.inc NEW)
    (0x0803ea00, 0x16da, 'SOUL_ABSORPTION_CID', 'tick_zone_slot_resolve_soul_abs_a',
     'Soul Absorption (pw=68073522; card_1435 slot=0x16DA); equip chain gate check'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803ea10, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'tick_zone_slot_resolve_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # reuse: SLOT_ACTIVE_BIT15_CLR=0xffff7fff
    (0x0803ea14, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'tick_zone_slot_resolve_bit15_clr_a',
     'AND mask clearing bit15 of zone slot descriptor word'),

    # reuse: SLOT_ACTIVE_BIT14_CLR=0xffffbfff
    (0x0803ea18, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'tick_zone_slot_resolve_bit14_clr_a',
     'AND mask clearing bit14 of zone slot descriptor word'),

    (0x0803eaa0, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'tick_zone_slot_resolve_bit15_clr_b',
     'AND mask clearing bit15 of zone slot descriptor word'),

    (0x0803eaa4, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'tick_zone_slot_resolve_bit14_clr_b',
     'AND mask clearing bit14 of zone slot descriptor word'),

    # === tick_equip_node_chain_link_display_seq (0x0803eb0c) ===

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803eb08, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_zone_slot_resolve_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # reuse: DUEL_FIELD_OAM_TILE_IDX_A=0x814
    (0x0803ebcc, 0x814, 'DUEL_FIELD_OAM_TILE_IDX_A', 'tick_equip_link_oam_tile_a_a',
     'DUEL_FIELD_OAM_TILE_IDX_A=0x814; OAM tile index for duel field card sprite A'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803ee04, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_link_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: A_DEAL_WITH_DARK_RULER_CID=0x165a
    (0x0803ee08, 0x165a, 'A_DEAL_WITH_DARK_RULER_CID', 'tick_equip_link_dark_ruler_a',
     'A Deal with Dark Ruler (pw=06850209; card_1330 slot=0x165A); chain node type arg'),

    # new: BACKFIRE_CID=0x1762 (NEW - second occurrence)
    (0x0803ee10, 0x1762, 'BACKFIRE_CID', 'tick_equip_link_backfire_a',
     'Backfire (pw=82705573; card_1547 slot=0x1762); equip chain gate check'),

    # reuse: BOSS_RUSH_CID=0x1972
    (0x0803ee14, 0x1972, 'BOSS_RUSH_CID', 'tick_equip_link_boss_rush_a',
     'Boss Rush (pw=66947414; card_1983 slot=0x1972); effect zone count gate'),

    # new: SOUL_ABSORPTION_CID=0x16da (NEW - second occurrence)
    (0x0803ee18, 0x16da, 'SOUL_ABSORPTION_CID', 'tick_equip_link_soul_abs_a',
     'Soul Absorption (pw=68073522; card_1435 slot=0x16DA); equip chain gate check'),

    # new: HUMAN_WAVE_TACTICS_CID=0x17b2 (card_info.inc NEW)
    (0x0803ee20, 0x17b2, 'HUMAN_WAVE_TACTICS_CID', 'tick_equip_link_human_wave_a',
     'Human-Wave Tactics (pw=30353551; card_1606 slot=0x17B2); equip chain gate check'),

    # reuse: P1LP_BLOCK2_OFF_1CE8=0x1ce8 (ewram.inc - second occurrence)
    (0x0803ee2c, 0x1ce8, 'P1LP_BLOCK2_OFF_1CE8', 'tick_equip_link_lp_block2_1ce8_a',
     '[gP1LifePoints+0x1ce8] LP display block2 field'),

    # reuse: SLOT_ACTIVE_BIT15_CLR=0xffff7fff
    (0x0803ef68, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'tick_equip_link_bit15_clr_a',
     'AND mask clearing bit15 of zone slot descriptor word'),

    # reuse: SLOT_ACTIVE_BIT14_CLR=0xffffbfff
    (0x0803ef6c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'tick_equip_link_bit14_clr_a',
     'AND mask clearing bit14 of zone slot descriptor word'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803ef74, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'tick_equip_link_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803efc8, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_equip_link_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at tick_equip_node_chain_link_display_seq exit'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS (76 total: 34 gDuelDisplaySeqState + 2 gDuelChainStepCounter
#                + 17 gDuelFieldSlots + 5 gP1LifePoints(PTR_)
#                + 6 gDuelCardCtxBase + 2 gEquipChainSlotRefs
#                + 1 gDuelEffectChainSlots + 2 gDuelFieldSlotState
#                + 7 gDuelChainDescBase)
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # === gDuelDisplaySeqState = 0x0201bcc0 (34 slots) ===

    # tick_zone_slot_transition_display_seq (0x0803d91c)
    (0x0803d954, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_trans_seq_state_a',   None),
    (0x0803d998, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_trans_seq_state_b',   None),
    (0x0803d9cc, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_trans_seq_state_c',   None),
    (0x0803da90, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_trans_seq_state_d',   None),

    # tick_flip_summon_state (0x0803dc34)
    (0x0803db98, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_flip_summon_seq_state_a',  None),
    (0x0803dc24, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_flip_summon_seq_state_b',  None),
    (0x0803dc7c, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_flip_summon_seq_state_c',  None),
    (0x0803dcc8, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_flip_summon_seq_state_d',  None),
    (0x0803dd44, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_flip_summon_seq_state_e',  None),

    # tick_zone_card_remove_display_seq (0x0803de90)
    (0x0803de88, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_remove_seq_state_a',  None),
    (0x0803df00, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_remove_seq_state_b',  None),

    # tick_equip_chain_node_link_seq (0x0803e0c4)
    (0x0803e098, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_link_seq_state_a',   None),
    (0x0803e0f4, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_link_seq_state_b',   None),

    # tick_zone_slot_ref_clear_display_seq (0x0803e130)
    (0x0803e128, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_ref_clear_seq_state_a',    None),

    # tick_zone_chain_node_ref_update_seq (0x0803e170)
    (0x0803e168, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_ref_upd_seq_state_a', None),

    # commit_set_card_to_field_slot (0x0803e228)
    (0x0803e1ac, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_ref_upd_seq_state_b', None),
    (0x0803e220, 0x0201bcc0, 'gDuelDisplaySeqState', 'commit_set_card_seq_state_a',   None),

    # write_zone_slot_display_args_by_state (0x0803e298)
    (0x0803e284, 0x0201bcc0, 'gDuelDisplaySeqState', 'write_zone_args_seq_state_a',   None),
    (0x0803e2cc, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_effect_idx_seq_state_a',   None),

    # tick_card_effect_index_display_seq (0x0803e318)
    (0x0803e310, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_effect_idx_seq_state_b',   None),
    (0x0803e360, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_effect_idx_seq_state_c',   None),

    # tick_hand_zone_insert_display_seq (0x0803e474)
    (0x0803e418, 0x0201bcc0, 'gDuelDisplaySeqState', 'dispatch_op7_seq_state_a',      None),
    (0x0803e46c, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_hand_insert_seq_state_a',  None),
    (0x0803e4a8, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_hand_insert_seq_state_b',  None),

    # tick_zone_card_place_with_slot_resolve_seq (0x0803e594)
    (0x0803e56c, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_hand_insert_seq_state_c',  None),
    (0x0803e5f0, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_slot_resolve_seq_a',  None),
    (0x0803e630, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_slot_resolve_seq_b',  None),
    (0x0803e6ac, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_zone_slot_resolve_seq_c',  None),

    # tick_equip_node_chain_link_display_seq (0x0803eb0c)
    (0x0803eadc, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_equip_link_seq_state_a',   None),
    (0x0803eb04, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_equip_link_seq_state_b',   None),
    (0x0803eb74, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_equip_link_seq_state_c',   None),
    (0x0803ebc8, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_equip_link_seq_state_d',   None),
    (0x0803ebe8, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_equip_link_seq_state_e',   None),
    (0x0803efc4, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_equip_link_seq_state_f',   None),

    # === gDuelChainStepCounter = 0x0201c4d0 (2 slots) ===

    (0x0803d958, 0x0201c4d0, 'gDuelChainStepCounter', 'tick_zone_trans_chain_step_ctr_a', None),
    (0x0803da9c, 0x0201c4d0, 'gDuelChainStepCounter', 'tick_zone_trans_chain_step_ctr_b', None),

    # === gDuelFieldSlots = 0x0201c510 (17 slots) ===

    (0x0803d994, 0x0201c510, 'gDuelFieldSlots', 'tick_zone_trans_field_slots_a',  None),
    (0x0803db8c, 0x0201c510, 'gDuelFieldSlots', 'tick_zone_trans_field_slots_b',  None),
    (0x0803dc1c, 0x0201c510, 'gDuelFieldSlots', 'tick_flip_summon_field_slots_a', None),
    (0x0803dc84, 0x0201c510, 'gDuelFieldSlots', 'tick_flip_summon_field_slots_b', None),
    (0x0803de74, 0x0201c510, 'gDuelFieldSlots', 'tick_flip_summon_field_slots_c', None),
    (0x0803df08, 0x0201c510, 'gDuelFieldSlots', 'tick_zone_remove_field_slots_a', None),
    (0x0803e01c, 0x0201c510, 'gDuelFieldSlots', 'tick_chain_link_field_slots_a',  None),
    (0x0803e1b4, 0x0201c510, 'gDuelFieldSlots', 'tick_chain_ref_upd_field_slots_a', None),
    (0x0803e1dc, 0x0201c510, 'gDuelFieldSlots', 'tick_chain_ref_upd_field_slots_b', None),
    (0x0803e21c, 0x0201c510, 'gDuelFieldSlots', 'commit_set_card_field_slots_a',  None),
    (0x0803e28c, 0x0201c510, 'gDuelFieldSlots', 'write_zone_args_field_slots_a',  None),
    (0x0803e2d4, 0x0201c510, 'gDuelFieldSlots', 'tick_effect_idx_field_slots_a',  None),
    (0x0803e30c, 0x0201c510, 'gDuelFieldSlots', 'tick_effect_idx_field_slots_b',  None),
    (0x0803e368, 0x0201c510, 'gDuelFieldSlots', 'tick_effect_idx_field_slots_c',  None),
    (0x0803e414, 0x0201c510, 'gDuelFieldSlots', 'dispatch_op7_field_slots_a',     None),
    (0x0803ea04, 0x0201c510, 'gDuelFieldSlots', 'tick_zone_slot_resolve_field_a', None),
    (0x0803ee1c, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_link_field_slots_a',  None),

    # === gP1LifePoints = 0x0201c4e0 (5 PTR_ slots) ===
    # These are already auto-labeled PTR_gP1LifePoints_<addr> by Ghidra.
    # _ref adds USER gas_label to target + DATA ref + slot label.

    (0x0803de7c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803de7c', None),
    (0x0803e090, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803e090', None),
    (0x0803e520, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803e520', None),
    (0x0803e9e8, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803e9e8', None),
    (0x0803ee00, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803ee00', None),

    # === gDuelCardCtxBase = 0x0201e2a0 (6 slots) ===

    (0x0803de6c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_flip_summon_card_ctx_a',    None),
    (0x0803e08c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_chain_link_card_ctx_a',     None),
    (0x0803e398, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_effect_idx_card_ctx_a',     None),
    (0x0803e3cc, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_effect_idx_card_ctx_b',     None),
    (0x0803ea0c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_zone_slot_resolve_card_a',  None),
    (0x0803ee28, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_link_card_ctx_a',     None),

    # === gEquipChainSlotRefs = 0x0201bb90 (2 slots) ===

    (0x0803df5c, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_zone_remove_chain_refs_a', None),
    (0x0803ee30, 0x0201bb90, 'gEquipChainSlotRefs', 'tick_equip_link_chain_refs_a',  None),

    # === gDuelEffectChainSlots = 0x0201bc54 (1 slot) ===

    (0x0803eb78, 0x0201bc54, 'gDuelEffectChainSlots', 'tick_equip_link_effect_slots_a', None),

    # === gDuelFieldSlotState = 0x0201c520 (2 slots) ===

    (0x0803e9f4, 0x0201c520, 'gDuelFieldSlotState', 'tick_zone_slot_resolve_slot_state_a', None),
    (0x0803ee0c, 0x0201c520, 'gDuelFieldSlotState', 'tick_equip_link_slot_state_a',        None),

    # === gDuelChainDescBase = 0x0201c4d8 (7 slots) ===

    (0x0803e718, 0x0201c4d8, 'gDuelChainDescBase', 'tick_zone_slot_resolve_chain_desc_a', None),
    (0x0803ea08, 0x0201c4d8, 'gDuelChainDescBase', 'tick_zone_slot_resolve_chain_desc_b', None),
    (0x0803ea9c, 0x0201c4d8, 'gDuelChainDescBase', 'tick_zone_slot_resolve_chain_desc_c', None),
    (0x0803ead8, 0x0201c4d8, 'gDuelChainDescBase', 'tick_zone_slot_resolve_chain_desc_d', None),
    (0x0803ee24, 0x0201c4d8, 'gDuelChainDescBase', 'tick_equip_link_chain_desc_a',        None),
    (0x0803ef70, 0x0201c4d8, 'gDuelChainDescBase', 'tick_equip_link_chain_desc_b',        None),
    (0x0803ef9c, 0x0201c4d8, 'gDuelChainDescBase', 'tick_equip_link_chain_desc_c',        None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS (2 total)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0803e634, 'DAT_0803e634', 'zone_card_place_switch_table_ptr',
     'ptr to switchD_0803e62c__switchdataD_0803e638; tick_zone_card_place_with_slot_resolve_seq'),
    (0x0803eb7c, 'DAT_0803eb7c', 'equip_node_chain_switch_table_ptr',
     'ptr to switchD_0803eb72__switchdataD_0803eb80; tick_equip_node_chain_link_display_seq'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FIXES (10 functions, 12 stale-FUN_ substring occurrences)
# All three stale names:
#   FUN_0803be4c -> dispatch_duel_event_display_seq
#   FUN_0802f0d8 -> clear_zone_slot_card_ref_bits
#   FUN_0802ec3c -> replace_chain_node_ref_by_zone_match
# ---------------------------------------------------------------------------

def _get_plate(addr_int):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        return None
    return cu.getComment(CodeUnit.PLATE_COMMENT)

def _set_plate(addr_int, text):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        print("WARN: no code unit at 0x%08x for plate" % addr_int)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    return True

def _plate_subst(addr_int, old_str, new_str, fix_label):
    old_text = _get_plate(addr_int)
    if old_text is None:
        print("WARN: no plate at 0x%08x (%s)" % (addr_int, fix_label))
        return
    if old_str in old_text:
        new_text = old_text.replace(old_str, new_str)
        if DRY:
            print("DRY PLATE %s: 0x%08x %s->%s" % (fix_label, addr_int, old_str, new_str))
        else:
            _set_plate(addr_int, new_text)
            print("PLATE %s ok: 0x%08x" % (fix_label, addr_int))
    else:
        print("PLATE %s: '%s' not found at 0x%08x (already fixed?)" % (fix_label, old_str, addr_int))

def apply_plate_fixes():
    # Fix 1: tick_zone_slot_transition_display_seq @ 0x0803d91c
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803d91c, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix1")

    # Fix 2: tick_zone_card_remove_display_seq @ 0x0803de90
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803de90, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix2")

    # Fix 3: tick_equip_chain_node_link_seq @ 0x0803e0c4
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e0c4, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix3")

    # Fix 4: tick_zone_slot_ref_clear_display_seq @ 0x0803e130
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e130, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix4a")
    # FUN_0802f0d8 -> clear_zone_slot_card_ref_bits
    _plate_subst(0x0803e130, "FUN_0802f0d8", "clear_zone_slot_card_ref_bits", "fix4b")

    # Fix 5: tick_zone_chain_node_ref_update_seq @ 0x0803e170
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e170, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix5a")
    # FUN_0802ec3c -> replace_chain_node_ref_by_zone_match
    _plate_subst(0x0803e170, "FUN_0802ec3c", "replace_chain_node_ref_by_zone_match", "fix5b")

    # Fix 6: write_zone_slot_display_args_by_state @ 0x0803e298
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e298, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix6")

    # Fix 7: tick_card_effect_index_display_seq @ 0x0803e318
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e318, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix7")

    # Fix 8: tick_hand_zone_insert_display_seq @ 0x0803e474
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e474, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix8")

    # Fix 9: tick_zone_card_place_with_slot_resolve_seq @ 0x0803e594
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803e594, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix9")

    # Fix 10: tick_equip_node_chain_link_display_seq @ 0x0803eb0c
    # FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803eb0c, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix10")


# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

print("=== RefineF03Seg9Slots.py DRY=%s ===" % DRY)

for (sa, val, eqn, sl, eol) in EQ_SLOTS:
    _eq(sa, val, eqn, sl, eol)

print("EQ done: %d slots" % len(EQ_SLOTS))

for (sa, ta, gl, sl, eol) in REF_SLOTS:
    _ref(sa, ta, gl, sl, eol)

print("REF done: %d slots" % len(REF_SLOTS))

for (sa, ol, nl, eol) in RENAME_SLOTS:
    _rename(sa, ol, nl, eol)

print("RENAME done: %d slots" % len(RENAME_SLOTS))

apply_plate_fixes()
print("PLATE done: 10 fixes")

print("=== COMPLETE: EQ=%d REF=%d RENAME=%d PLATE=10 DRY=%s ===" % (
    len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), DRY))
