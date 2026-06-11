# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg8Slots.py -- file 03 Seg-8 (0x0803c774..0x0803d91c)
#   tick_equip_chain_slot_ref_scan_seq .. tick_zone_slot_card_set_display_seq
#   EQ=82 (reuse 43 + new 39), REF=53, RENAME=1, FUNC_RENAME=0, PLATE=11
#   carve=0, disasm=0, §5.1=0
#
# New constants added to .inc files before running this script:
#   ewram.inc: gDuelChainStepCounter=0x0201c4d0, gDuelChainDescBase=0x0201c4d8,
#              gDuelDisplaySeqStateAlt=0x0201bcc2
#   duel_field.inc: SLOT_ACTIVE_BIT22_CLR=0xffbfffff, SLOT_ACTIVE_BIT23_CLR=0xff7fffff,
#                   EQUIP_CHAIN_STEP_OFF=0x1d28, EQUIP_CHAIN_ACTIVE_OFF=0x1d2c,
#                   SLOT_ACTIVE_BIT15_CLR=0xffff7fff, SLOT_ACTIVE_BIT14_CLR=0xffffbfff,
#                   SLOT_BITS14_15_CLR=0xfffe7fff, DISP_SEQ_STEP_LOCK_A_OFF=0x80a,
#                   DISP_SEQ_ALT_CTR_OFF=0x80e, DISP_SEQ_CARD_SET_CTR_OFF=0x818,
#                   SLOT_BIT21_CLR=0xffdfffff
#   card_info.inc: BLUE_EYES_WHITE_DRAGON_CID=0x0fa7, eval_gap_cid_0fa6=0x0fa6,
#                  A_DEAL_WITH_DARK_RULER_CID=0x165a, eval_gap_cid_11ed=0x11ed
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
# A. EQ_SLOTS (82 total: 43 reuse + 39 new)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # === tick_equip_chain_slot_ref_scan_seq (0x0803c774) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803c7c0, 0x868, 'PLAYER_BLOCK_STRIDE', 'tick_chain_scan_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868; player data block stride'),

    # new: SLOT_ACTIVE_BIT22_CLR=0xffbfffff
    (0x0803c7c4, 0xffbfffff, 'SLOT_ACTIVE_BIT22_CLR', 'tick_chain_scan_bit22_clr_a',
     'AND mask clearing bit22 of zone slot word (chain-linked flag)'),

    # new: SLOT_ACTIVE_BIT23_CLR=0xff7fffff
    (0x0803c7c8, 0xff7fffff, 'SLOT_ACTIVE_BIT23_CLR', 'tick_chain_scan_bit23_clr_a',
     'AND mask clearing bit23 of zone slot word (chain-type flag)'),

    # reuse: EHERO_AVIAN_CID=0x18a6
    (0x0803c7cc, 0x18a6, 'EHERO_AVIAN_CID', 'tick_chain_scan_avian_cid_a',
     'Elemental Hero Avian (pw=21844576); link_equip_node_by_card_type_check card_type_A'),

    # === setup_equip_chain_for_slot (0x0803c814) ===

    # reuse: CHAIN_THRASHER_CID=0x19c1
    (0x0803c804, 0x19c1, 'CHAIN_THRASHER_CID', 'setup_chain_thrasher_cid_a',
     'Chain Thrasher (pw=88190453); link_equip_node_by_card_type_check card_type_B'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803c810, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'setup_chain_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at setup_equip_chain_for_slot exit'),

    # new: eval_gap_cid_0fa6=0x0fa6
    (0x0803c868, 0x0fa6, 'eval_gap_cid_0fa6', 'setup_chain_gap_cid_0fa6_a',
     'gap CID (not in card-stats.s); lower bound of [0xfa6..0xfa7] card_type range check; low-conf'),

    # new: BLUE_EYES_WHITE_DRAGON_CID=0x0fa7
    (0x0803c86c, 0x0fa7, 'BLUE_EYES_WHITE_DRAGON_CID', 'setup_chain_bewd_cid_a',
     'Blue-Eyes White Dragon (pw=89631139; card_0001 slot=0x0FA7); upper bound of range check'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803c860, 0x868, 'PLAYER_BLOCK_STRIDE', 'setup_chain_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803c8dc, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'setup_chain_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock at invoke_equip_candidate_scan_setup'),

    # new: SLOT_ACTIVE_BIT22_CLR (reuse new)
    (0x0803c8d4, 0xffbfffff, 'SLOT_ACTIVE_BIT22_CLR', 'setup_chain_bit22_clr_a',
     'AND mask clearing bit22 of zone slot word'),

    # === invoke_equip_candidate_scan_setup (0x0803c8e0) ===

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803c900, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'invoke_scan_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock at invoke_equip_candidate_scan_setup exit'),

    # === finalize_equip_chain_removal_state (0x0803c904) ===

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803c994, 0x868, 'PLAYER_BLOCK_STRIDE', 'finalize_chain_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # new: eval_gap_cid_11ed=0x11ed
    (0x0803c998, 0x11ed, 'eval_gap_cid_11ed', 'finalize_chain_gap_cid_11ed_a',
     'gap CID (not in card-stats.s; between 0x11eb=Takuhee and 0x11ee=Binding Chain); sentinel; low-conf'),

    # new: EQUIP_CHAIN_STEP_OFF=0x1d28
    (0x0803c99c, 0x1d28, 'EQUIP_CHAIN_STEP_OFF', 'finalize_chain_step_off_a',
     '[gP1LifePoints+player*0x868+0x1d28] equip chain state step field; :=0xc (chain ready)'),

    # new: EQUIP_CHAIN_ACTIVE_OFF=0x1d2c
    (0x0803c9a0, 0x1d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'finalize_chain_active_off_a',
     '[gP1LifePoints+player*0x868+0x1d2c] equip chain active player side flag; :=0'),

    # reuse: EFFECT_ZONE_BITMASK_OFF=0x10d0
    (0x0803c9a4, 0x10d0, 'EFFECT_ZONE_BITMASK_OFF', 'finalize_chain_effect_mask_off_a',
     '[gDuelFieldSlots+0x10d0] effect zone occupation bitmask; clears bit0'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803c9a8, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'finalize_chain_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at finalize exit'),

    # === tick_equip_chain_activate_state_seq (0x0803c9ac) ===

    # new: EQUIP_CHAIN_STEP_OFF (reuse new)
    (0x0803c9f0, 0x1d28, 'EQUIP_CHAIN_STEP_OFF', 'tick_chain_act_step_off_a',
     '[gP1LifePoints+0x1d28] equip chain step; :=0x6 (activation)'),

    # new: EQUIP_CHAIN_ACTIVE_OFF (reuse new)
    (0x0803c9f4, 0x1d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'tick_chain_act_active_off_a',
     '[gP1LifePoints+0x1d2c] equip chain active; writes player-side bit'),

    # reuse: EFFECT_ZONE_BITMASK_OFF=0x10d0
    (0x0803c9f8, 0x10d0, 'EFFECT_ZONE_BITMASK_OFF', 'tick_chain_act_effect_mask_off_a',
     '[gDuelFieldSlots+0x10d0] effect zone bitmask; OR-sets bit0'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803c9fc, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'tick_chain_act_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === clear_equip_chain_active_state (0x0803ca00) ===

    # reuse: EFFECT_ZONE_BITMASK_OFF=0x10d0
    (0x0803ca28, 0x10d0, 'EFFECT_ZONE_BITMASK_OFF', 'clear_chain_effect_mask_off_a',
     '[gP1LifePoints+0x10d0] EFFECT_ZONE_BITMASK_OFF; clears bit0 via rsbs+ands'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803ca30, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'clear_chain_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at clear_equip_chain_active_state exit'),

    # === init_equip_ai_state (0x0803ca34) ===

    # new: EQUIP_CHAIN_STEP_OFF (reuse new)
    (0x0803ca60, 0x1d28, 'EQUIP_CHAIN_STEP_OFF', 'init_ai_step_off_a',
     '[gP1LifePoints+0x1d28] equip chain step; :=0x9 (ai_init)'),

    # new: EQUIP_CHAIN_ACTIVE_OFF (reuse new)
    (0x0803ca64, 0x1d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'init_ai_active_off_a',
     '[gP1LifePoints+0x1d2c] equip chain active; :=0'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803ca6c, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'init_ai_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === link_equip_node_by_slot_match (0x0803ca70) ===

    # new: EQUIP_CHAIN_STEP_OFF (reuse new)
    (0x0803cadc, 0x1d28, 'EQUIP_CHAIN_STEP_OFF', 'link_slot_step_off_a',
     '[gP1LifePoints+0x1d28] equip chain step; :=0xb (ready)'),

    # new: EQUIP_CHAIN_ACTIVE_OFF (reuse new)
    (0x0803cae0, 0x1d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'link_slot_active_off_a',
     '[gP1LifePoints+0x1d2c] equip chain active; :=0'),

    # reuse: EFFECT_ZONE_BITMASK_OFF=0x10d0
    (0x0803cae4, 0x10d0, 'EFFECT_ZONE_BITMASK_OFF', 'link_slot_effect_mask_off_a',
     '[gDuelFieldSlots+0x10d0] effect zone bitmask'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803cae8, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'link_slot_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # reuse: P1LP_BLOCK2_OFF=0x1d08
    (0x0803cad4, 0x1d08, 'P1LP_BLOCK2_OFF', 'link_slot_lp_block2_a',
     '[gP1LifePoints+0x1d08] LP display block2 field'),

    # === tick_zone_slot_removal_chain_repair_seq (0x0803caec) ===

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803cbe4, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'removal_repair_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f; clears bits[13:6] of state halfword'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803cbe8, 0x868, 'PLAYER_BLOCK_STRIDE', 'removal_repair_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # new: SLOT_ACTIVE_BIT15_CLR=0xffff7fff
    (0x0803cbf0, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'removal_repair_bit15_clr_a',
     'AND mask clearing bit15 of zone slot descriptor word'),

    # new: SLOT_ACTIVE_BIT14_CLR=0xffffbfff
    (0x0803cbf4, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'removal_repair_bit14_clr_a',
     'AND mask clearing bit14 of zone slot descriptor word'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803cc98, 0x868, 'PLAYER_BLOCK_STRIDE', 'removal_repair_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: EFFECT_ZONE_PARTITION_OFF=0x10a4
    (0x0803cca0, 0x10a4, 'EFFECT_ZONE_PARTITION_OFF', 'removal_repair_effect_part_off_a',
     '[gDuelFieldSlots+0x10a4] effect zone slot array base offset'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803cca8, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'removal_repair_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === tick_zone_card_place_alt_display_seq (0x0803ccac) ===

    # new: DISP_SEQ_ALT_CTR_OFF=0x80e
    (0x0803cd10, 0x80e, 'DISP_SEQ_ALT_CTR_OFF', 'alt_place_alt_ctr_off_a',
     '[gDuelDisplaySeqStateAlt+0x80e] step counter for alt zone-card-place sequence'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803cd90, 0x868, 'PLAYER_BLOCK_STRIDE', 'alt_place_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # new: SLOT_BITS14_15_CLR=0xfffe7fff
    (0x0803cf54, 0xfffe7fff, 'SLOT_BITS14_15_CLR', 'alt_place_bits14_15_clr_a',
     'AND mask clearing bits 14+15 simultaneously of slot word'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803cf60, 0x868, 'PLAYER_BLOCK_STRIDE', 'alt_place_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803cf68, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'alt_place_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # new: SLOT_ACTIVE_BIT15_CLR (reuse new)
    (0x0803cf6c, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'alt_place_bit15_clr_a',
     'AND mask clearing bit15 of slot word'),

    # new: SLOT_ACTIVE_BIT14_CLR (reuse new)
    (0x0803cf70, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'alt_place_bit14_clr_a',
     'AND mask clearing bit14 of slot word'),

    # new: SLOT_ACTIVE_BIT15_CLR (reuse new)
    (0x0803d008, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'alt_place_bit15_clr_b',
     'AND mask clearing bit15 of slot word'),

    # new: SLOT_ACTIVE_BIT14_CLR (reuse new)
    (0x0803d00c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'alt_place_bit14_clr_b',
     'AND mask clearing bit14 of slot word'),

    # new: DISP_SEQ_STEP_LOCK_A_OFF=0x80a
    (0x0803d034, 0x80a, 'DISP_SEQ_STEP_LOCK_A_OFF', 'alt_place_step_lock_a_off_a',
     '[gDuelDisplaySeqState+0x80a] secondary step lock A'),

    # new: DISP_SEQ_ALT_CTR_OFF (reuse new)
    (0x0803d0a8, 0x80e, 'DISP_SEQ_ALT_CTR_OFF', 'normal_summon_alt_ctr_off_a',
     '[gDuelDisplaySeqStateAlt+0x80e] step counter for normal_summon'),

    # === tick_normal_summon_zone_state (0x0803d038) ===

    # new: SLOT_BITS14_15_CLR (reuse new)
    (0x0803d20c, 0xfffe7fff, 'SLOT_BITS14_15_CLR', 'normal_summon_bits14_15_clr_a',
     'AND mask clearing bits 14+15 of slot word'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d214, 0x868, 'PLAYER_BLOCK_STRIDE', 'normal_summon_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # new: A_DEAL_WITH_DARK_RULER_CID=0x165a
    (0x0803d218, 0x165a, 'A_DEAL_WITH_DARK_RULER_CID', 'normal_summon_dark_ruler_cid_a',
     'A Deal with Dark Ruler (pw=06850209; card_1330 slot=0x165A); link_equip_node_to_chain chain_type arg'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d254, 0x868, 'PLAYER_BLOCK_STRIDE', 'normal_summon_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d270, 0x868, 'PLAYER_BLOCK_STRIDE', 'normal_summon_player_stride_c',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d28c, 0x868, 'PLAYER_BLOCK_STRIDE', 'normal_summon_player_stride_d',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d390, 0x868, 'PLAYER_BLOCK_STRIDE', 'normal_summon_player_stride_e',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803d394, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'normal_summon_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # new: SLOT_ACTIVE_BIT15_CLR (reuse new)
    (0x0803d398, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'normal_summon_bit15_clr_a',
     'AND mask clearing bit15 of slot word'),

    # new: SLOT_ACTIVE_BIT14_CLR (reuse new)
    (0x0803d39c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'normal_summon_bit14_clr_a',
     'AND mask clearing bit14 of slot word'),

    # new: SLOT_ACTIVE_BIT15_CLR (reuse new)
    (0x0803d454, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'normal_summon_bit15_clr_b',
     'AND mask clearing bit15 of slot word'),

    # new: SLOT_ACTIVE_BIT14_CLR (reuse new)
    (0x0803d458, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'normal_summon_bit14_clr_b',
     'AND mask clearing bit14 of slot word'),

    # new: DISP_SEQ_STEP_LOCK_A_OFF (reuse new)
    (0x0803d474, 0x80a, 'DISP_SEQ_STEP_LOCK_A_OFF', 'normal_summon_step_lock_a_off_a',
     '[gDuelDisplaySeqState+0x80a] secondary step lock A'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d2ac, 0x868, 'PLAYER_BLOCK_STRIDE', 'normal_summon_player_stride_f',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # === tick_zone_card_place_display_seq (0x0803d478) ===

    # new: DISP_SEQ_ALT_CTR_OFF (reuse new)
    (0x0803d4dc, 0x80e, 'DISP_SEQ_ALT_CTR_OFF', 'zone_place_alt_ctr_off_a',
     '[gDuelDisplaySeqStateAlt+0x80e] step counter for zone_place sequence'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d55c, 0x868, 'PLAYER_BLOCK_STRIDE', 'zone_place_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # reuse: DUEL_FIELD_OAM_TILE_IDX_C=0x816
    (0x0803d6c0, 0x816, 'DUEL_FIELD_OAM_TILE_IDX_C', 'zone_place_oam_tile_idx_c_a',
     'DUEL_FIELD_OAM_TILE_IDX_C=0x816; OAM tile index for duel field card sprite'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803d6c4, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'zone_place_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # new: SLOT_ACTIVE_BIT15_CLR (reuse new)
    (0x0803d6c8, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'zone_place_bit15_clr_a',
     'AND mask clearing bit15 of slot word'),

    # new: SLOT_ACTIVE_BIT14_CLR (reuse new)
    (0x0803d6cc, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'zone_place_bit14_clr_a',
     'AND mask clearing bit14 of slot word'),

    # new: DISP_SEQ_STEP_LOCK_A_OFF (reuse new)
    (0x0803d6f0, 0x80a, 'DISP_SEQ_STEP_LOCK_A_OFF', 'zone_place_step_lock_a_off_a',
     '[gDuelDisplaySeqState+0x80a] secondary step lock A cleared at step 2'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803d730, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'zone_place_step_lock_off_a',
     '[gDuelDisplaySeqState+0x80c] step lock cleared at zone_place exit'),

    # reuse: DISPLAY_SEQ_STEP_LOCK_OFF=0x80c
    (0x0803d744, 0x80c, 'DISPLAY_SEQ_STEP_LOCK_OFF', 'zone_place_step_lock_off_b',
     '[gDuelDisplaySeqState+0x80c] step lock'),

    # === tick_zone_slot_card_set_display_seq (0x0803d6f4) ===

    # new: DISP_SEQ_CARD_SET_CTR_OFF=0x818
    (0x0803d8f4, 0x818, 'DISP_SEQ_CARD_SET_CTR_OFF', 'card_set_ctr_off_a',
     '[gDuelDisplaySeqState+0x818] step counter for card-set display sequence'),

    # reuse: GPRNG_STEP_CTR_MASK=0xffffc03f
    (0x0803d8fc, 0xffffc03f, 'GPRNG_STEP_CTR_MASK', 'card_set_step_ctr_mask_a',
     'GPRNG_STEP_CTR_MASK=0xffffc03f'),

    # reuse: PLAYER_BLOCK_STRIDE=0x868
    (0x0803d900, 0x868, 'PLAYER_BLOCK_STRIDE', 'card_set_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868'),

    # new: SLOT_ACTIVE_BIT15_CLR (reuse new)
    (0x0803d908, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR', 'card_set_bit15_clr_a',
     'AND mask clearing bit15 of slot word'),

    # new: SLOT_ACTIVE_BIT14_CLR (reuse new)
    (0x0803d90c, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR', 'card_set_bit14_clr_a',
     'AND mask clearing bit14 of slot word'),

    # reuse: EFFECT_ZONE_PARTITION_OFF=0x10a4
    (0x0803d914, 0x10a4, 'EFFECT_ZONE_PARTITION_OFF', 'card_set_effect_part_off_a',
     '[gDuelFieldSlots+0x10a4] effect zone slot array base offset'),

    # new: SLOT_BIT21_CLR=0xffdfffff
    (0x0803d918, 0xffdfffff, 'SLOT_BIT21_CLR', 'card_set_bit21_clr_a',
     'AND mask clearing bit21 of zone slot word (equip-active bit)'),

    # reuse: P1LP_BLOCK2_OFF=0x1d08 (finalize_equip_chain_removal_state)
    (0x0803c988, 0x1d08, 'P1LP_BLOCK2_OFF', 'finalize_chain_lp_block2_a',
     '[gP1LifePoints+0x1d08] LP display block2 field'),

    # reuse: P1LP_BLOCK2_OFF_1CE8=0x1ce8
    (0x0803c98c, 0x1ce8, 'P1LP_BLOCK2_OFF_1CE8', 'finalize_chain_lp_block2_1ce8_a',
     '[gP1LifePoints+0x1ce8] LP display block2 field'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS (53 total)
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # === tick_equip_chain_slot_ref_scan_seq (0x0803c774) ===
    (0x0803c7b8, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_scan_seq_state_a', None),
    (0x0803c7bc, 0x0201c4e0, 'gP1LifePoints',        'tick_chain_scan_lp_base_a',  None),
    (0x0803c808, 0x0201bb90, 'gEquipChainSlotRefs',  'tick_chain_scan_chain_refs_a', None),
    (0x0803c80c, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_scan_seq_state_b', None),

    # === setup_equip_chain_for_slot (0x0803c814) ===
    (0x0803c85c, 0x0201bcc0, 'gDuelDisplaySeqState', 'setup_chain_seq_state_a',    None),
    (0x0803c864, 0x0201c510, 'gDuelFieldSlots',      'setup_chain_field_slots_a',  None),
    (0x0803c8d8, 0x0201bcc0, 'gDuelDisplaySeqState', 'setup_chain_seq_state_b',    None),

    # === invoke_equip_candidate_scan_setup (0x0803c8e0) ===
    (0x0803c8fc, 0x0201bcc0, 'gDuelDisplaySeqState', 'invoke_scan_seq_state_a',    None),

    # === finalize_equip_chain_removal_state (0x0803c904) ===
    (0x0803c980, 0x0201bcc0, 'gDuelDisplaySeqState', 'finalize_chain_seq_state_a', None),
    (0x0803c984, 0x0201c4e0, 'gP1LifePoints',        'finalize_chain_lp_base_a',   None),
    (0x0803c990, 0x0201e2a0, 'gDuelCardCtxBase',     'finalize_chain_card_ctx_a',  None),

    # === tick_equip_chain_activate_state_seq (0x0803c9ac) ===
    (0x0803c9e8, 0x0201bcc0, 'gDuelDisplaySeqState', 'tick_chain_act_seq_state_a', None),
    (0x0803c9ec, 0x0201c4e0, 'gP1LifePoints',        'tick_chain_act_lp_base_a',   None),

    # === clear_equip_chain_active_state (0x0803ca00) ===
    (0x0803ca24, 0x0201c4e0, 'gP1LifePoints',        'clear_chain_lp_base_a',      None),
    (0x0803ca2c, 0x0201bcc0, 'gDuelDisplaySeqState', 'clear_chain_seq_state_a',    None),

    # === init_equip_ai_state (0x0803ca34) ===
    (0x0803ca5c, 0x0201c4e0, 'gP1LifePoints',        'init_ai_lp_base_a',          None),
    (0x0803ca68, 0x0201bcc0, 'gDuelDisplaySeqState', 'init_ai_seq_state_a',        None),

    # === link_equip_node_by_slot_match (0x0803ca70) ===
    (0x0803cacc, 0x0201bcc0, 'gDuelDisplaySeqState', 'link_slot_match_seq_state_a', None),
    (0x0803cad0, 0x0201c4e0, 'gP1LifePoints',        'link_slot_match_lp_base_a',  None),
    (0x0803cad8, 0x0201e2a0, 'gDuelCardCtxBase',     'link_slot_match_card_ctx_a', None),

    # === tick_zone_slot_removal_chain_repair_seq (0x0803caec) ===
    (0x0803cb18, 0x0201bcc0, 'gDuelDisplaySeqState', 'removal_repair_seq_state_a', None),
    (0x0803cb1c, 0x0201c4d0, 'gDuelChainStepCounter','removal_repair_step_ctr_a',  None),
    (0x0803cbec, 0x0201c510, 'gDuelFieldSlots',      'removal_repair_field_slots_a', None),
    (0x0803cbf8, 0x0201c4d0, 'gDuelChainStepCounter','removal_repair_step_ctr_b',  None),
    (0x0803cc94, 0x0201bc54, 'gDuelEffectChainSlots','removal_repair_effect_slots_a', None),
    (0x0803cc9c, 0x0201c510, 'gDuelFieldSlots',      'removal_repair_field_slots_b', None),
    (0x0803cca4, 0x0201bcc0, 'gDuelDisplaySeqState', 'removal_repair_seq_state_b', None),

    # === tick_zone_card_place_alt_display_seq (0x0803ccac) ===
    (0x0803cd0c, 0x0201bcc2, 'gDuelDisplaySeqStateAlt', 'alt_place_seq_state_a',   None),
    (0x0803cd8c, 0x0201c4e0, 'gP1LifePoints',        'alt_place_lp_base_a',        None),
    (0x0803cd94, 0x0201bcc0, 'gDuelDisplaySeqState', 'alt_place_seq_state_b',      None),
    (0x0803cf58, 0x0201c4d8, 'gDuelChainDescBase',   'alt_place_chain_desc_a',     None),
    (0x0803cf5c, 0x0201c4e0, 'gP1LifePoints',        'alt_place_lp_base_b',        None),
    (0x0803cf64, 0x0201e2a0, 'gDuelCardCtxBase',     'alt_place_card_ctx_a',       None),
    (0x0803d004, 0x0201c4d8, 'gDuelChainDescBase',   'alt_place_chain_desc_b',     None),

    # === tick_normal_summon_zone_state (0x0803d038) ===
    (0x0803d210, 0x0201c4e0, 'gP1LifePoints',        'normal_summon_lp_base_a',    None),
    (0x0803d21c, 0x0201c4d8, 'gDuelChainDescBase',   'normal_summon_chain_desc_a', None),
    (0x0803d220, 0x0201e2a0, 'gDuelCardCtxBase',     'normal_summon_card_ctx_a',   None),
    (0x0803d250, 0x0201c4e0, 'gP1LifePoints',        'normal_summon_lp_base_b',    None),
    (0x0803d26c, 0x0201c4e0, 'gP1LifePoints',        'normal_summon_lp_base_c',    None),
    (0x0803d288, 0x0201c4e0, 'gP1LifePoints',        'normal_summon_lp_base_d',    None),
    (0x0803d38c, 0x0201c4e0, 'gP1LifePoints',        'normal_summon_lp_base_e',    None),
    (0x0803d450, 0x0201c4d8, 'gDuelChainDescBase',   'normal_summon_chain_desc_b', None),
    (0x0803d0a4, 0x0201bcc2, 'gDuelDisplaySeqStateAlt', 'normal_summon_seq_state_alt_a', None),
    (0x0803d2a8, 0x0201c4e0, 'gP1LifePoints',        'normal_summon_lp_base_f',    None),

    # === tick_zone_card_place_display_seq (0x0803d478) ===
    (0x0803d4d8, 0x0201bcc2, 'gDuelDisplaySeqStateAlt', 'zone_place_seq_state_alt_a', None),
    (0x0803d558, 0x0201c4e0, 'gP1LifePoints',        'zone_place_lp_base_a',       None),
    (0x0803d560, 0x0201bcc0, 'gDuelDisplaySeqState', 'zone_place_seq_state_a',     None),
    (0x0803d6d0, 0x0201e2a0, 'gDuelCardCtxBase',     'zone_place_card_ctx_a',      None),
    (0x0803d6d4, 0x0201bcc0, 'gDuelDisplaySeqState', 'zone_place_seq_state_b',     None),

    # === tick_zone_slot_card_set_display_seq (0x0803d6f4) ===
    (0x0803d72c, 0x0201bcc0, 'gDuelDisplaySeqState', 'card_set_seq_state_a',       None),
    (0x0803d8f8, 0x0201e2a0, 'gDuelCardCtxBase',     'card_set_card_ctx_a',        None),
    (0x0803d904, 0x0201c510, 'gDuelFieldSlots',      'card_set_field_slots_a',     None),
    (0x0803d910, 0x0201c4d8, 'gDuelChainDescBase',   'card_set_chain_desc_a',      None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS (1 total)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0803d224, 'DAT_0803d224', 'normal_summon_switch_table_ptr',
     'ptr to switchD_0803d20a__switchdataD_0803d228; 5-entry table for zone types 0xb..0xf'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FIXES (11 total: 2 full rewrites + 9 substring replaces)
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
    # Fix 1: tick_equip_chain_slot_ref_scan_seq @ 0x0803c774
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803c774, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix1")

    # Fix 2: setup_equip_chain_for_slot @ 0x0803c814
    # substring x2: FUN_0803be4c + FUN_08035f54
    _plate_subst(0x0803c814, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix2a")
    _plate_subst(0x0803c814, "FUN_08035f54", "link_equip_node_by_card_type_check", "fix2b")

    # Fix 3: invoke_equip_candidate_scan_setup @ 0x0803c8e0
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803c8e0, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix3")

    # Fix 4: finalize_equip_chain_removal_state @ 0x0803c904
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803c904, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix4")

    # Fix 5: tick_equip_chain_activate_state_seq @ 0x0803c9ac
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803c9ac, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix5")

    # Fix 6: clear_equip_chain_active_state @ 0x0803ca00
    # Full ASCII rewrite: stale FUN_0802eeac + wrong addr 0x0201b290
    ascii_plate_6 = (
        "Called by dispatch_duel_event_display_seq (caseD_1e). Reads gP1LifePoints+0x10d0"
        " (EFFECT_ZONE_BITMASK_OFF), clears bit0 via rsbs+ands pattern (~0x1 AND), writes back."
        " Then calls rebuild_equip_chain_refs for full chain ref rebuild scan."
        " Finally clears [gDuelDisplaySeqState+0x80c] (step lock) to 0."
        " Constants: gP1LifePoints=0x0201c4e0, chain_flag_offset=EFFECT_ZONE_BITMASK_OFF=0x10d0,"
        "   state_base=gDuelDisplaySeqState=0x0201bcc0, step_lock_off=DISPLAY_SEQ_STEP_LOCK_OFF=0x80c."
        " indeg=1 (dispatch_duel_event_display_seq caseD_1e only)."
    )
    if DRY:
        print("DRY PLATE fix6: 0x0803ca00 full ASCII rewrite clear_equip_chain_active_state (%d chars)" % len(ascii_plate_6))
    else:
        _set_plate(0x0803ca00, ascii_plate_6)
        print("PLATE fix6 ok: 0x0803ca00 full rewrite (clear_equip_chain_active_state)")

    # Fix 7: link_equip_node_by_slot_match @ 0x0803ca70
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803ca70, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix7")

    # Fix 8: tick_zone_slot_removal_chain_repair_seq @ 0x0803caec
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803caec, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix8")

    # Fix 9: tick_zone_card_place_alt_display_seq @ 0x0803ccac
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803ccac, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix9")

    # Fix 10: tick_zone_card_place_display_seq @ 0x0803d478
    # substring: FUN_0803be4c -> dispatch_duel_event_display_seq
    _plate_subst(0x0803d478, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix10")

    # Fix 11: tick_zone_slot_card_set_display_seq @ 0x0803d6f4
    # Full ASCII rewrite: stale FUN_0803be4c + FUN_0802f14c + FUN_0802ec80 + offset 0x810->0x818
    ascii_plate_11 = (
        "Called by dispatch_duel_event_display_seq caseD_3d. Zone slot card set-card placement display sequence."
        " Reads from [gDuelDisplaySeqState]: zone_byte ([+2] ldrb), zone_hi ([+2]>>8 r7), slot_byte ([+4] ldrb),"
        " slot_hi ([+4]>>8 r6). Reads step_counter at [gDuelDisplaySeqState+0x818]."
        " Step 0: if zone_hi>0xa or slot_hi>0xa, copies step_ctr to [+0x80c] and exits (boundary guard);"
        "   if in range and zone_hi<=0xa&&slot_hi<=0xa: calls write_card_display_index_with_bit_offset(0x2d,1)."
        "   Returns r0=1 on in-range path."
        " Step 1: calls get_zone_slot_ptr, write_word_from_deref_src, copy_bytes_by_halfword, zero_fill_by_halfword;"
        "   calls update_equip_chain_zone_slot_refs (arg: zone_hi<<8|slot_hi); if slot_hi>4 calls"
        "   clear_chain_refs_for_low_zone_nodes; calls dispatch_card_display_op(0x18); increments step."
        " Step 2+: clears [gDuelDisplaySeqState+0x80c]:=0 and exits."
        " Constants: state_base=gDuelDisplaySeqState=0x0201bcc0; step_ctr_off=DISP_SEQ_CARD_SET_CTR_OFF=0x818;"
        "   step_lock=DISPLAY_SEQ_STEP_LOCK_OFF=0x80c; field_slots=gDuelFieldSlots=0x0201c510;"
        "   chain_desc=gDuelChainDescBase=0x0201c4d8; ctx=gDuelCardCtxBase=0x0201e2a0."
        " Returns void (pop{r0};bx r0)."
    )
    if DRY:
        print("DRY PLATE fix11: 0x0803d6f4 full ASCII rewrite tick_zone_slot_card_set_display_seq (%d chars)" % len(ascii_plate_11))
    else:
        _set_plate(0x0803d6f4, ascii_plate_11)
        print("PLATE fix11 ok: 0x0803d6f4 full rewrite (tick_zone_slot_card_set_display_seq)")


# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

print("=== RefineF03Seg8Slots.py DRY=%s ===" % DRY)

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
print("PLATE done: 11 fixes")

print("=== COMPLETE: EQ=%d REF=%d RENAME=%d PLATE=11 DRY=%s ===" % (
    len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), DRY))
