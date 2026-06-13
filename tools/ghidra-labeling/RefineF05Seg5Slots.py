# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF05Seg5Slots.py -- file-05 Seg-5 (0x0804c6e8..0x0804d124)
#   submit_slot_card_sprite_row_entry / apply_equip_activation_with_id_lookup /
#   init_card_sprite_row_entry / init_card_sprite_row_entry_alt /
#   submit_slot_card_sprite_row_packed / check_card_slot_activation_eligible /
#   dispatch_card_eligibility_state_machine (body spans to 0x4d1d2)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (67 slots)
#   B. REF_SLOTS -- 0 slots
#   C. RENAME_SLOTS -- 8 slots (plain rename + EOL)
#   D. PLATE_SUBS -- 0 subs
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    All values verified against ROM (reviewer C4: 100% match).
#    const_name must already exist in inc or be new (written to constants/*.inc).
#    slot labels use caseD_ suffix per existing Ghidra convention in asm file.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- switchdataD_0804c6e8 case literal pool (Guardian weapon CIDs) ---
    # card_info.inc NEW: BUTTERFLY_DAGGER_ELMA_CID=0x165c
    (0x0804c704, 0x0000165c, 'BUTTERFLY_DAGGER_ELMA_CID',               'classify_summon_cat_butterfly_dagger_elma_cid'),
    # card_info.inc EXISTS: SHOOTING_STAR_BOW_CID=0x165d
    (0x0804c70c, 0x0000165d, 'SHOOTING_STAR_BOW_CID',                   'classify_summon_cat_shooting_star_bow_cid'),
    # card_info.inc NEW: GRAVITY_AXE_GRARL_CID=0x165e
    (0x0804c714, 0x0000165e, 'GRAVITY_AXE_GRARL_CID',                   'classify_summon_cat_gravity_axe_grarl_cid'),
    # card_info.inc NEW: WICKED_BREAKING_FLAMBERGE_BAOU_CID=0x165f
    (0x0804c71c, 0x0000165f, 'WICKED_BREAKING_FLAMBERGE_BAOU_CID',      'classify_summon_cat_wicked_breaking_flamberge_cid'),
    # card_info.inc NEW: TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID=0x1661
    (0x0804c72c, 0x00001661, 'TWIN_SWORDS_FLASHING_LIGHT_TRYCE_CID',    'classify_summon_cat_twin_swords_tryce_cid'),

    # --- submit_slot_card_sprite_row_entry literal pool ---
    # card_info.inc EXISTS: SLOT_CARD_EMPTY=0xffff
    (0x0804c7e8, 0x0000ffff, 'SLOT_CARD_EMPTY',                         'submit_slot_sprite_id_mask'),
    # ewram.inc EXISTS: P1LP_BLOCK2_OFF=0x1d08
    (0x0804c7f0, 0x00001d08, 'P1LP_BLOCK2_OFF',                         'submit_slot_sprite_lp_block2_off'),
    # ewram.inc EXISTS: P1LP_BLOCK2_OFF_1CE8=0x1ce8
    (0x0804c7f4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',                    'submit_slot_sprite_lp_block2_off_1ce8'),
    # ewram.inc EXISTS: gDuelCardCtxBase=0x0201e2a0
    (0x0804c7f8, 0x0201e2a0, 'gDuelCardCtxBase',                        'submit_slot_sprite_card_ctx_base'),
    # ewram.inc EXISTS: gDuelPhaseFlags=0x0201b290
    (0x0804c81c, 0x0201b290, 'gDuelPhaseFlags',                         'submit_slot_sprite_phase_flags_b'),
    (0x0804c8c0, 0x0201b290, 'gDuelPhaseFlags',                         'submit_slot_sprite_phase_flags_c'),
    # oam_attr.inc NEW: OAM_ATTR2_CLR_BITS_11_6=0xfffff03f
    (0x0804c8c4, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6',                 'submit_slot_sprite_attr2_clr_11_6'),
    # oam_attr.inc EXISTS: OAM_ATTR1_X_MASK=0x1ff
    (0x0804c8c8, 0x000001ff, 'OAM_ATTR1_X_MASK',                       'submit_slot_sprite_attr1_x_mask'),
    # gl_scrollbar.inc EXISTS: SCROLLBAR_CLEAR_BITS_14_6=0xffff803f
    (0x0804c8cc, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',               'submit_slot_sprite_attr2_clr_14_6'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804c90c, 0x0201b290, 'gDuelPhaseFlags',                         'submit_slot_sprite_phase_flags_d'),

    # --- apply_equip_activation_with_id_lookup literal pool ---
    # card_info.inc EXISTS: SLOT_CARD_EMPTY=0xffff
    (0x0804c940, 0x0000ffff, 'SLOT_CARD_EMPTY',                         'apply_equip_activ_id_mask'),

    # --- init_card_sprite_row_entry literal pool ---
    # oam_attr.inc EXISTS: OAM_ATTR1_X_MASK
    (0x0804ca44, 0x000001ff, 'OAM_ATTR1_X_MASK',                       'init_sprite_row_attr1_x_mask'),
    # gl_scrollbar.inc EXISTS: SCROLLBAR_CLEAR_BITS_14_6
    (0x0804ca48, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',               'init_sprite_row_attr2_clr_14_6'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804ca4c, 0x0201b290, 'gDuelPhaseFlags',                         'init_sprite_row_phase_flags'),
    # ewram.inc EXISTS: LP_BAR_ANIM_STATE_OFF=0x4cc
    (0x0804ca50, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',                   'init_sprite_row_slot_count_off'),
    # oam_attr.inc NEW: OAM_ATTR2_CLR_BITS_11_6
    (0x0804ca54, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6',                 'init_sprite_row_attr2_clr_11_6'),
    # ewram.inc NEW: SPRITE_ROW_ENTRY_DATA_OFF=0x4d4
    (0x0804ca58, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',               'init_sprite_row_entry_data_off'),

    # --- init_card_sprite_row_entry_alt literal pool ---
    # oam_attr.inc EXISTS: OAM_ATTR1_X_MASK
    (0x0804cbe0, 0x000001ff, 'OAM_ATTR1_X_MASK',                       'init_sprite_row_alt_attr1_x_mask'),
    # gl_scrollbar.inc EXISTS: SCROLLBAR_CLEAR_BITS_14_6
    (0x0804cbe4, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',               'init_sprite_row_alt_attr2_clr_14_6'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804cbe8, 0x0201b290, 'gDuelPhaseFlags',                         'init_sprite_row_alt_phase_flags'),
    # ewram.inc EXISTS: LP_BAR_ANIM_STATE_OFF
    (0x0804cbec, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF',                   'init_sprite_row_alt_slot_count_off'),
    # oam_attr.inc NEW: OAM_ATTR2_CLR_BITS_11_6
    (0x0804cbf0, 0xfffff03f, 'OAM_ATTR2_CLR_BITS_11_6',                 'init_sprite_row_alt_attr2_clr_11_6'),
    # ewram.inc NEW: SPRITE_ROW_ENTRY_DATA_OFF
    (0x0804cbf4, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF',               'init_sprite_row_alt_entry_data_off'),

    # --- check_card_slot_activation_eligible BST literal pool ---
    # card_info.inc NEW: METALMORPH_CID=0x1238
    (0x0804ce24, 0x00001238, 'METALMORPH_CID',                          'check_slot_activ_bst_metalmorph_cid'),
    # card_info.inc NEW: SWORDS_OF_REVEALING_LIGHT_CID=0x1102
    (0x0804ce28, 0x00001102, 'SWORDS_OF_REVEALING_LIGHT_CID',           'check_slot_activ_bst_swords_reveal_cid'),
    # card_info.inc NEW: COCOON_OF_EVOLUTION_CID=0xfee
    (0x0804ce2c, 0x00000fee, 'COCOON_OF_EVOLUTION_CID',                 'check_slot_activ_bst_cocoon_evol_cid'),
    # card_info.inc EXISTS: KUNAI_WITH_CHAIN_CID=0x1231
    (0x0804ce34, 0x00001231, 'KUNAI_WITH_CHAIN_CID',                    'check_slot_activ_bst_kunai_chain_cid'),
    # card_info.inc EXISTS: BLAST_WITH_CHAIN_CID=0x1514
    (0x0804ce4c, 0x00001514, 'BLAST_WITH_CHAIN_CID',                    'check_slot_activ_bst_blast_chain_cid'),
    # card_info.inc EXISTS: DIFFERENT_DIMENSION_CAPSULE_CID=0x159c
    (0x0804ce60, 0x0000159c, 'DIFFERENT_DIMENSION_CAPSULE_CID',         'check_slot_activ_bst_dif_dim_cap_cid'),

    # --- dispatch_card_eligibility_state_machine literal pool ---
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804ce9c, 0x0201b290, 'gDuelPhaseFlags',                         'dispatch_eligib_phase_flags'),
    # ewram.inc NEW: ELIGIB_STATE_OFF=0x574
    (0x0804cea0, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_state_off'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804cf6c, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_0_state_off'),
    # ewram.inc EXISTS: gDuelCardCtxBase
    (0x0804cf70, 0x0201e2a0, 'gDuelCardCtxBase',                        'dispatch_eligib_caseD_1_card_ctx'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804cf74, 0x0201b290, 'gDuelPhaseFlags',                         'dispatch_eligib_caseD_1_phase_flags'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804cf84, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_1b_state_off'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804d008, 0x0201b290, 'gDuelPhaseFlags',                         'dispatch_eligib_caseD_1c_phase_flags'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d00c, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_1c_state_off'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d038, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_2_state_off'),
    # ewram.inc NEW: ELIGIB_STATE_CTRL_OFF=0x1d54
    (0x0804d03c, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',                   'dispatch_eligib_caseD_2_ctrl_off'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804d054, 0x0201b290, 'gDuelPhaseFlags',                         'dispatch_eligib_caseD_a_phase_flags'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d058, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_a_state_off'),
    # ewram.inc NEW: ELIGIB_STATE_CTRL_OFF
    (0x0804d074, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',                   'dispatch_eligib_caseD_b_ctrl_off'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d078, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_b_state_off'),
    # ewram.inc NEW: ELIGIB_ACT_TYPE_OFF=0x1d5c
    (0x0804d098, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF',                     'dispatch_eligib_caseD_b_act_type_off'),
    # ewram.inc NEW: ELIGIB_ACT_COUNT_OFF=0x1d58
    (0x0804d09c, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF',                    'dispatch_eligib_caseD_b_act_count_off'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d0a0, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_b2_state_off'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d0ac, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_b3_state_off'),
    # ewram.inc NEW: ELIGIB_RESULT_OFF=0x584 (independent constant; not GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF
    #   which is gPrng+0x1c0+0x584; this is gDuelPhaseFlags+0x584; different base, benign numeric collision)
    (0x0804d0e4, 0x00000584, 'ELIGIB_RESULT_OFF',                       'dispatch_eligib_caseD_14_result_off'),
    # ewram.inc EXISTS: gSpriteAttrBuf=0x0201b870
    (0x0804d0e8, 0x0201b870, 'gSpriteAttrBuf',                          'dispatch_eligib_caseD_14_sprite_buf'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d0ec, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_14_state_off'),
    # ewram.inc EXISTS: gSpriteAttrBuf
    (0x0804d118, 0x0201b870, 'gSpriteAttrBuf',                          'dispatch_eligib_caseD_15_sprite_buf'),
    # ewram.inc NEW: ELIGIB_RESULT_OFF
    (0x0804d11c, 0x00000584, 'ELIGIB_RESULT_OFF',                       'dispatch_eligib_caseD_15_result_off'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d120, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_15_state_off'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804d170, 0x0201b290, 'gDuelPhaseFlags',                         'dispatch_eligib_caseD_1e_phase_flags'),
    # ewram.inc NEW: ELIGIB_STATE_OFF
    (0x0804d174, 0x00000574, 'ELIGIB_STATE_OFF',                        'dispatch_eligib_caseD_1e_state_off'),
    # ewram.inc EXISTS: gDuelPhaseFlags
    (0x0804d1dc, 0x0201b290, 'gDuelPhaseFlags',                         'dispatch_eligib_caseD_1f_phase_flags'),
    # ewram.inc NEW: ELIGIB_RESULT_OFF
    (0x0804d1e0, 0x00000584, 'ELIGIB_RESULT_OFF',                       'dispatch_eligib_caseD_1f_result_off'),

    # Additional EQ slots in caseD_1e and caseD_1f body (still within dispatch fn body)
    # ewram.inc NEW: ELIGIB_SPRITE_CTRL_OFF=0x1d68
    (0x0804d168, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',                  'dispatch_eligib_caseD_1e_sprite_ctrl_off'),
    # oam_attr.inc NEW: SPRITE_ATTR_TYPE_HIDDEN_Y97=0x8061
    (0x0804d16c, 0x00008061, 'SPRITE_ATTR_TYPE_HIDDEN_Y97',             'dispatch_eligib_caseD_1e_sprite_hidden'),
    # ewram.inc NEW: ELIGIB_ANIM_STATE_OFF=0x1d6c
    (0x0804d178, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',                   'dispatch_eligib_caseD_1f_anim_state_off'),
    # ewram.inc NEW: ELIGIB_CARD_ID_OFF=0x1d44
    (0x0804d194, 0x00001d44, 'ELIGIB_CARD_ID_OFF',                      'dispatch_eligib_caseD_1f_card_id_off'),
    # ewram.inc NEW: ELIGIB_STATE_CTRL_OFF
    (0x0804d1d8, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF',                   'dispatch_eligib_caseD_1f_ctrl_off'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: 0 slots
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL. All EOL text is pure ASCII (no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_gP1LifePoints_* -> semantic labels with EOL
    (0x0804c7ec, 'submit_slot_sprite_p1lp_ptr',
     '.word gP1LifePoints ; 0x0201c4e0'),
    (0x0804d034, 'dispatch_eligib_caseD_2_p1lp_ptr',
     '.word gP1LifePoints ; 0x0201c4e0'),
    (0x0804d070, 'dispatch_eligib_caseD_b_p1lp_ptr',
     '.word gP1LifePoints ; 0x0201c4e0'),
    (0x0804d164, 'dispatch_eligib_caseD_1e_p1lp_ptr',
     '.word gP1LifePoints ; 0x0201c4e0'),
    (0x0804d1d4, 'dispatch_eligib_caseD_1f_p1lp_ptr',
     '.word gP1LifePoints ; 0x0201c4e0'),
    # PTR_DAT_0804cd90 -> orphan_slot_card_eligible_fn_table
    (0x0804cd90, 'orphan_slot_card_eligible_fn_table',
     'orphan jump table (0 external refs); 7 entries pointing to 0x4cdac/0x4cdb6/0x4cdc2'),
    # DAT_0804cfb4 -> ROM table pointer slot
    (0x0804cfb4, 'dispatch_eligib_caseD_1_ineligible_cid_tbl',
     '.word 0x09e3f118 ; ROM ptr: 10-entry CID array {0x14f9,0x154f,0x1550,0x1551,0x1730,0x1731,0x1670,0x1671,0x1672,0x1288}'),
    # DAT_0804cea4 -> switchdata ptr
    (0x0804cea4, 'dispatch_eligib_switchdata_ptr',
     '.word switchD_0804ce98__switchdataD_0804cea8 ; ptr to 32-entry jump table'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: 0 subs
# ---------------------------------------------------------------------------
PLATE_SUBS = []

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF05Seg5Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
    made = set()

    # --- A. EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value & 0xffffffff)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B. REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- C. RENAME_SLOTS ---
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- D. PLATE_SUBS ---
    for func_int, old_s, new_s in PLATE_SUBS:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        plate = cu.getComment(CodeUnit.PLATE_COMMENT)
        if plate is None:
            print("[D SKIP] no plate @ 0x%08x" % func_int); continue
        if old_s not in plate:
            print("[D SKIP] '%s' not in plate @ 0x%08x" % (old_s, func_int)); continue
        if DRY:
            print("[D dry] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s))
            nD += 1; continue
        new_plate = plate.replace(old_s, new_s)
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate sub '%s'->'%s'" % (func_int, old_s, new_s)); nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))


main()
