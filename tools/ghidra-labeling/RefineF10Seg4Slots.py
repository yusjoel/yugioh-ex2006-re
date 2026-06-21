# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg4Slots.py -- f10 Seg-4 (0x0807cd68..0x0807db20)
#   19 functions; 53 residual slots: 43 EQ + 6 REF + 3 RENAME + 1 BLK-base RENAME
#   PLATE = 5 (pure ASCII, WARN treated as FAIL)
#   FUNC_RENAME = 0
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (43 slots; 42 REUSE + 1 NEW TRIGGER_OP_PARAM_139)
#   B. RENAME_SLOTS -- residual slots already symbolic + BLK-base label (4 total)
#   C. REF_SLOTS  -- USER label + DATA ref for fn-ptr/in-range ptr slots (6)
#   D. PLATE      -- set plate comments (5 functions, pure ASCII)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii)
#    43 slots total; 42 REUSE + 1 NEW (TRIGGER_OP_PARAM_139)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- tick_equip_slot_activation_score_and_oam ---
    (0x0807cd84, 0x0201b290, 'gDuelPhaseFlags',
     'tick_slot_score_oam_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    (0x0807cde8, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_slot_score_oam_card_ctx',
     'gDuelCardCtxBase=0x0201e2a0: duel card activation context base'),
    (0x0807ce48, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'tick_slot_score_oam_banisher_off',
     'LP_BANISHER_CTX_OFF=0x1d70: [gP1LifePoints+0x1d70] LP banisher context offset'),
    (0x0807ce4c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_slot_score_oam_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),

    # --- build_equip_eligible_bitmap_for_slots ---
    (0x0807cee8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_bitmap_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807ceec, 0x0201c510, 'gDuelFieldSlots',
     'build_equip_bitmap_field_slots',
     'gDuelFieldSlots=0x0201c510: duel field zone slot array base'),

    # --- apply_equip_activation_with_neo_daedalus_lp_output ---
    (0x0807cfb8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_equip_act_neo_player_stride_a',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807d00c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_equip_act_neo_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: dup B'),
    (0x0807d010, 0x0201c740, 'gP1SlotSetCodeArray',
     'apply_equip_act_neo_set_code_arr',
     'gP1SlotSetCodeArray=0x0201c740: P1 slot set-code array base'),

    # --- tick_equip_target_validity_prng_lp_display ---
    (0x0807d034, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_target_prng_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    (0x0807d06c, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_target_prng_card_ctx',
     'gDuelCardCtxBase=0x0201e2a0: duel card activation context base'),
    (0x0807d0c4, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'tick_equip_target_prng_lp_next_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] LP card track next field'),
    (0x0807d0c8, 0x0201bb90, 'gEquipChainSlotRefs',
     'tick_equip_target_prng_equip_refs',
     'gEquipChainSlotRefs=0x0201bb90: equip chain slot refs base'),
    (0x0807d100, 0x0201bb90, 'gEquipChainSlotRefs',
     'tick_equip_target_prng_equip_refs_b',
     'gEquipChainSlotRefs=0x0201bb90: dup B'),

    # --- tick_equip_activation_display_state_machine ---
    (0x0807d128, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_disp_sm_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    # NOTE: DAT_0807d12c (0x0807d130) is REF slot -- handled in section C
    (0x0807d1d8, 0x00000139, 'TRIGGER_OP_PARAM_139',
     'tick_equip_act_disp_sm_trig_op139',
     'TRIGGER_OP_PARAM_139=0x139: trigger_card_display_op31_if_not_active 2nd arg; state 0x7f branch'),
    (0x0807d2cc, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'tick_equip_act_disp_sm_eligib_off',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68: [gP1LifePoints+0x1d68] eligibility sprite ctrl field'),

    # --- tick_zone_pipeline_with_neo_daedalus_oam_setup ---
    (0x0807d364, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_zone_neo_oam_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807d368, 0x0201c8f8, 'gP1HandSlotArray',
     'tick_zone_neo_oam_hand_arr',
     'gP1HandSlotArray=0x0201c8f8: P1 hand slot array base'),

    # --- find_ojama_trio_in_deck_for_lp_display ---
    (0x0807d400, 0x0201b290, 'gDuelPhaseFlags',
     'find_ojama_trio_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    (0x0807d490, 0x00001681, 'OJAMA_GREEN_CID',
     'find_ojama_trio_green_cid',
     'OJAMA_GREEN_CID=0x1681: Ojama Green card ID'),
    (0x0807d494, 0x000016b3, 'OJAMA_YELLOW_CID',
     'find_ojama_trio_yellow_cid',
     'OJAMA_YELLOW_CID=0x16b3: Ojama Yellow card ID'),
    (0x0807d498, 0x000016b4, 'OJAMA_BLACK_CID',
     'find_ojama_trio_black_cid',
     'OJAMA_BLACK_CID=0x16b4: Ojama Black card ID'),
    (0x0807d49c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_ojama_trio_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807d4a0, 0x0201c740, 'gP1SlotSetCodeArray',
     'find_ojama_trio_set_code_arr',
     'gP1SlotSetCodeArray=0x0201c740: P1 slot set-code array base'),

    # --- apply_equip_activation_by_field6_gate ---
    (0x0807d540, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'apply_equip_act_field6_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807d544, 0x0201c510, 'gDuelFieldSlots',
     'apply_equip_act_field6_field_slots',
     'gDuelFieldSlots=0x0201c510: duel field zone slot array base'),

    # --- apply_equip_activation_if_field6_gate_pending ---
    (0x0807d590, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF',
     'apply_equip_if_field6_act_state_off',
     'LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: [gP1LifePoints+0x10d0] LP activation link flag'),

    # --- enqueue_equip_zone_sprites_by_slot_chain ---
    (0x0807d638, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_equip_zone_chain_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807d63c, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_equip_zone_chain_slots',
     'gDuelFieldSlots=0x0201c510: duel field zone slot array base'),
    (0x0807d640, 0x0000195b, 'FEATHER_SHOT_CID',
     'enqueue_equip_zone_chain_base_cid',
     'FEATHER_SHOT_CID=0x195b: chain base card ID in check_value_in_slot_chain'),

    # --- tick_equip_lp_indicator_or_score_display_seq ---
    (0x0807d6ec, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_score_disp_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    (0x0807d6f0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_lp_score_disp_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),

    # --- enqueue_ritual_eligible_sprite_or_type11 ---
    (0x0807d7a8, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF',
     'enqueue_ritual_act_state_off',
     'LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: [gP1LifePoints+0x10d0] LP activation link flag'),
    (0x0807d7ac, 0x0201bb90, 'gEquipChainSlotRefs',
     'enqueue_ritual_equip_refs',
     'gEquipChainSlotRefs=0x0201bb90: equip chain slot refs base'),
    (0x0807d7b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_ritual_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807d7b4, 0x00008020, 'SPRITE_RECORD_P2_SIDE',
     'enqueue_ritual_p2_sprite_flag',
     'SPRITE_RECORD_P2_SIDE=0x8020: sprite record P2 side flag'),

    # --- tick_neo_daedalus_equip_oam_display_seq ---
    (0x0807d95c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_neo_daed_oam_disp_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),

    # --- tick_hand_spell_match_display_seq ---
    (0x0807d98c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_hand_spell_match_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),
    (0x0807da40, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_hand_spell_match_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807da44, 0x0201c8f8, 'gP1HandSlotArray',
     'tick_hand_spell_match_hand_arr',
     'gP1HandSlotArray=0x0201c8f8: P1 hand slot array base'),

    # --- tick_equip_activation_display_by_node_state ---
    (0x0807da94, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_act_disp_by_node_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base'),

    # --- sync_equip_hand_oam_and_player_bits ---
    (0x0807db10, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'sync_equip_hand_oam_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii)
#    3 gP1LifePoints already-symbolic + 1 BLK2 base DAT_
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0807d58c, 'apply_equip_if_field6_pending_gp1lp',
     '.word gP1LifePoints: apply_equip_activation_if_field6_gate_pending LP base'),
    (0x0807d7a4, 'enqueue_ritual_gp1lp',
     '.word gP1LifePoints: enqueue_ritual_eligible_sprite_or_type11 LP base'),
    (0x0807db0c, 'sync_equip_hand_oam_gp1lp',
     '.word gP1LifePoints: sync_equip_hand_oam_and_player_bits LP base'),
    # BLK2 base label (renamed to be replaced by disasm pass)
    (0x0807d830, 'sillva_dispatch_stubs',
     'BLK2 R4 disasm base: Sillva dispatch sub-stubs A..E (0xfc bytes, 5 unique entries)'),
]

# ---------------------------------------------------------------------------
# C. REF_SLOTS: (slot_addr, target_addr, fn_name, slot_label, eol_ascii, raw)
#    fn-ptr THUMB+1 slots and in-range data ptr: set USER label + DATA ref
#    raw=True: slot contains target_addr directly (not +1); raw=False: THUMB+1
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DAT_0807cdec: check_equip_activation_at_slot11+1 (slot A)
    (0x0807cdec, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_slot_score_oam_zone_handler_ptr',
     'fn-ptr check_equip_activation_at_slot11+1=0x08065991 (THUMB+1)', False),
    # DAT_0807ce04: check_equip_activation_at_slot11+1 (slot B)
    (0x0807ce04, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_slot_score_oam_zone_handler_ptr_b',
     'fn-ptr check_equip_activation_at_slot11+1=0x08065991 (THUMB+1) dup B', False),
    # DAT_0807d12c: switchD jump table ptr (in-range RAW data ptr, not THUMB+1)
    (0x0807d12c, 0x0807d130, 'switchD_0807d126__switchdataD_0807d130',
     'tick_equip_act_disp_sm_jtable_ptr',
     'switchD_0807d126 jump table base=0x0807d130 (already labeled in asm)', True),
    # DAT_0807d25c: invoke_effect_node_with_active_flag_3arg+1
    (0x0807d25c, 0x08090624, 'invoke_effect_node_with_active_flag_3arg',
     'tick_equip_act_disp_sm_activation_ptr',
     'fn-ptr invoke_effect_node_with_active_flag_3arg+1=0x08090625 (THUMB+1)', False),
    # DWORD_0807d3dc: check_equip_slot_eligible_by_card_id_bst+1
    (0x0807d3dc, 0x08050a54, 'check_equip_slot_eligible_by_card_id_bst',
     'apply_equip_slot_act_eligib_bst_ptr',
     'fn-ptr check_equip_slot_eligible_by_card_id_bst+1=0x08050a55 (THUMB+1)', False),
    # DWORD_0807d7a0: check_card_id_is_normal_summon_type+1
    (0x0807d7a0, 0x0804b164, 'check_card_id_is_normal_summon_type',
     'enqueue_ritual_normal_summon_pred',
     'fn-ptr check_card_id_is_normal_summon_type+1=0x0804b165 (THUMB+1)', False),
]

# ---------------------------------------------------------------------------
# D. PLATE: (fn_addr, plate_text)
#    5 functions; pure ASCII; WARN treated as FAIL
# ---------------------------------------------------------------------------
PLATE_SLOTS = [
    (0x0807ce50,
     "build_equip_eligible_bitmap_for_slots\n"
     "Scans equip zone slots, builds eligibility bitmap from check_card_equip_eligible_for_slot per slot, "
     "calls forward_equip_bitmap_update_with_full_mask(node, bitmap, 2). Returns 0."),
    (0x0807cef0,
     "apply_equip_activation_with_neo_daedalus_lp_output\n"
     "Checks effect slot match, activates node, checks Neo-Daedalus group placement; on pass calls "
     "apply_slot_equip_activation_with_eligibility_check; calls submit_lp_indicator_with_slot_xor_flag. Returns 0."),
    (0x0807d014,
     "tick_equip_target_validity_prng_lp_display\n"
     "State machine [gDuelPhaseFlags+0x4a0]: 0x80=check target valid+prng sample; "
     "0x7f=enqueue_lp_display_row_type17; 0x7e=apply activation or submit LP score diff. Returns next state or 0."),
    (0x0807d104,
     "tick_equip_activation_display_state_machine\n"
     "29-state display driver [0x64..0x80]: dispatches via switchD_0807d126. "
     "State 0x7f calls trigger_card_display_op31_if_not_active(player, TRIGGER_OP_PARAM_139=0x139). Returns next state."),
    (0x0807d2e0,
     "tick_zone_pipeline_with_neo_daedalus_oam_setup\n"
     "Pushes zone sprite pipeline; gates on Neo-Daedalus placeable+zone_type==4; "
     "finds hand slot by set_code; calls invoke_setup_equip_oam_with_attr2. Returns 0."),
]


# ===========================================================================
# Helpers
# ===========================================================================

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data at 0x%08x" % slot_int
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch at 0x%08x: got=0x%x want=0x%x" % (slot_int, iv, want)
    return True, None


def main():
    print("=== RefineF10Seg4Slots (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    rf = currentProgram.getReferenceManager()
    nA = nB = nC = nD = 0
    fail_count = 0

    # -----------------------------------------------------------------------
    # A. EQ_SLOTS
    # -----------------------------------------------------------------------
    print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for (slot_int, value, eq_name, slot_label, eol_text) in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[FAIL] EQ 0x%08x %s: %s" % (slot_int, eq_name, err))
            fail_count += 1
            continue
        if not DRY:
            eq = et.getEquate(eq_name)
            if eq is None:
                eq = et.createEquate(eq_name, value & 0xffffffff)
            slot_a = _addr(slot_int)
            eq.addReference(slot_a, 0)
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[EQ ok] 0x%08x %s -> %s" % (slot_int, eq_name, slot_label))
        nA += 1

    # -----------------------------------------------------------------------
    # B. RENAME_SLOTS
    # -----------------------------------------------------------------------
    print("--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for (slot_int, slot_label, eol_text) in RENAME_SLOTS:
        if not DRY:
            slot_a = _addr(slot_int)
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[RENAME ok] 0x%08x -> %s" % (slot_int, slot_label))
        nB += 1

    # -----------------------------------------------------------------------
    # C. REF_SLOTS
    # -----------------------------------------------------------------------
    print("--- C. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for (slot_int, target_int, fn_name, slot_label, eol_text, raw) in REF_SLOTS:
        # Value check: raw ptr or THUMB+1
        check_val = target_int if raw else (target_int + 1)
        ok, err = _check(slot_int, check_val)
        if not ok:
            print("[FAIL] REF 0x%08x %s: %s" % (slot_int, fn_name, err))
            fail_count += 1
            continue
        if not DRY:
            slot_a = _addr(slot_int)
            target_a = _addr(target_int)
            # Label on target
            sm.createLabel(target_a, fn_name, SourceType.USER_DEFINED)
            # DATA ref from slot to target
            rf.addMemoryReference(slot_a, target_a, RefType.DATA, SourceType.USER_DEFINED, 0)
            # Set primary
            for ref in rf.getReferencesFrom(slot_a):
                if ref.getToAddress().equals(target_a):
                    rf.setPrimary(ref, True)
                    break
            # Slot label
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            # EOL comment
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[REF ok] 0x%08x -> %s slot=%s" % (slot_int, fn_name, slot_label))
        nC += 1

    # -----------------------------------------------------------------------
    # D. PLATE (set plate comments, pure ASCII; WARN = FAIL)
    # -----------------------------------------------------------------------
    print("--- D. PLATE (%d) ---" % len(PLATE_SLOTS))
    for (fn_addr, plate_text) in PLATE_SLOTS:
        fn_a = _addr(fn_addr)
        cu = listing.getCodeUnitAt(fn_a)
        if cu is None:
            print("[FAIL] PLATE 0x%08x: no code unit found" % fn_addr)
            fail_count += 1
            continue
        # ASCII check: no bytes > 0x7F allowed
        for ch in plate_text:
            if ord(ch) > 0x7F:
                print("[FAIL] PLATE 0x%08x: non-ASCII char U+%04x in text" % (fn_addr, ord(ch)))
                fail_count += 1
                break
        else:
            if not DRY:
                cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
            print("[PLATE ok] 0x%08x" % fn_addr)
            nD += 1

    print("")
    print("=== SUMMARY: EQ=%d RENAME=%d REF=%d PLATE=%d FAIL=%d ===" % (
        nA, nB, nC, nD, fail_count))
    if fail_count > 0:
        print("[ERROR] %d slot(s) FAILED -- see FAIL lines above" % fail_count)
    else:
        print("[OK] All slots applied successfully")


main()
