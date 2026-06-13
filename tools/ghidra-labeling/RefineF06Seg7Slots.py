# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg7Slots.py -- F06 Seg-7 (0x08058550..0x08058cec)
#   ROM range: tick_equip_activation_neo_daedalus_gate .. tick_equip_zone_select_display_seq_short
#   22 named functions, 58 residual auto-name slots
#
# Sections:
#   A. EQ_SLOTS  -- 53 data-equate slots
#   B. REF_SLOTS -- 5 fn-ptr REF slots
#   C. PLATE_SET -- 4 full ASCII plate rewrites (CJK mojibake replacement)
#
# New constants added to constants files BEFORE running this script:
#   card_info.inc:  +1 (CRIMSON_NINJA_CID=0x16b8)
#   ewram.inc:      +1 (LP_BANISHER_CTX_OFF=0x1d70)
#   duel_field.inc: +1 (EQUIP_ACTIVE_CTX_OFF=0x484)
#
# Reused constants (must exist in constants/*.inc):
#   ewram.inc:       gDuelPhaseFlags=0x0201b290, gP1LifePoints=0x0201c4e0,
#                    gDuelCardCtxBase=0x0201e2a0, gDuelFieldSlots=0x0201c510,
#                    PLAYER_BLOCK_STRIDE=0x868, ELIGIB_SPRITE_CTRL_OFF=0x1d68,
#                    ELIGIB_ANIM_STATE_OFF=0x1d6c, LP_BAR_ANIM_STATE_OFF=0x4cc,
#                    SPRITE_ROW_ENTRY_DATA_OFF=0x4d4, CHAIN_NODE_CARD_ARR_OFF=0x4f4
#   duel_field.inc:  EQUIP_ACTIVATION_STEP_OFF=0x4ac
#   card_info.inc:   BLACK_LUSTER_SOLDIER_ENVOY_CID=0x16cb
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_124500-pre-F06Seg7

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
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    const_name must already exist in constants/*.inc.
#    slot_label != const_name; all ^[a-z][a-z0-9_]+$
#    Values verified against ROM (proposal self-check + reviewer C4).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==== gDuelPhaseFlags = 0x0201b290 (ewram.inc) x12 ====
    (0x080586a0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_tier_abcx_state_base'),
    (0x0805874c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_tier_abcx_state_base_b'),
    (0x0805881c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_sprite_attr11_state_base'),
    (0x08058850, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_sprite_state_base'),
    (0x080588b0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_effect_act_state_base'),
    (0x080589a4, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_effect_act_state_base_b'),
    (0x08058a88, 0x0201b290, 'gDuelPhaseFlags', 'check_zone_field6_state_base'),
    (0x08058ab4, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_target_state_base'),
    (0x08058b2c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_target_state_base_b'),
    (0x08058ba0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_target_state_base_c'),
    (0x08058c58, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_select_state_base'),
    (0x08058cac, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_select_state_base_b'),

    # ==== EQUIP_ACTIVATION_STEP_OFF = 0x000004ac (duel_field.inc) x12 ====
    (0x080586a4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_tier_abcx_step_off'),
    (0x08058750, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_tier_abcx_step_off_b'),
    (0x08058820, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_sprite_attr11_step_off'),
    (0x08058854, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_sprite_step_off'),
    (0x080588b4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_effect_act_step_off'),
    (0x080589a8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_effect_act_step_off_b'),
    (0x080589f0, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_effect_act_step_off_c'),
    (0x08058ab8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_target_step_off'),
    (0x08058b30, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_target_step_off_b'),
    (0x08058ba4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_target_step_off_c'),
    (0x08058c5c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_select_step_off'),
    (0x08058cb0, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_select_step_off_b'),

    # ==== gP1LifePoints = 0x0201c4e0 (ewram.inc) x9 ====
    (0x0805872c, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_tier_abcx_gp1lp'),
    (0x08058958, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_effect_act_gp1lp'),
    (0x08058980, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_effect_act_gp1lp_b'),
    (0x080589c0, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_effect_act_gp1lp_c'),
    (0x08058af8, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_zone_target_gp1lp'),
    (0x08058b08, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_zone_target_gp1lp_b'),
    (0x08058b48, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_zone_target_gp1lp_c'),
    (0x08058be4, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_zone_target_gp1lp_d'),
    (0x08058cd4, 0x0201c4e0, 'gP1LifePoints', 'tick_equip_zone_select_gp1lp'),

    # ==== ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (ewram.inc) x4 ====
    (0x08058730, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_tier_abcx_lp_off'),
    (0x08058bec, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_zone_target_lp_off'),
    (0x08058c10, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_zone_target_lp_off_b'),
    (0x08058cd8, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_zone_select_lp_off'),

    # ==== gDuelCardCtxBase = 0x0201e2a0 (ewram.inc) x4 ====
    (0x0805897c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_effect_act_ctx_base'),
    (0x08058af4, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_zone_target_ctx_base'),
    (0x08058b7c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_zone_target_ctx_base_b'),
    (0x08058c8c, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_zone_select_ctx_base'),

    # ==== PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) x2 ====
    (0x08058674, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'check_equip_slot_has_stride'),
    (0x08058bf4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_zone_target_stride'),

    # ==== LP_BANISHER_CTX_OFF = 0x00001d70 (ewram.inc, NEW) x2 ====
    (0x08058bf0, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'tick_equip_zone_target_lp_step2_off'),
    (0x08058c14, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'tick_equip_zone_target_lp_step2_off_b'),

    # ==== gDuelFieldSlots = 0x0201c510 (ewram.inc) x1 ====
    (0x08058678, 0x0201c510, 'gDuelFieldSlots', 'check_equip_slot_has_slots_base'),

    # ==== CRIMSON_NINJA_CID = 0x000016b8 (card_info.inc, NEW) x1 ====
    (0x08058824, 0x000016b8, 'CRIMSON_NINJA_CID', 'tick_equip_sprite_attr11_crimson_ninja_cid'),

    # ==== BLACK_LUSTER_SOLDIER_ENVOY_CID = 0x000016cb (card_info.inc) x1 ====
    (0x08058888, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID', 'tick_equip_act_sprite_mode2_bls_data'),

    # ==== LP_BAR_ANIM_STATE_OFF = 0x000004cc (ewram.inc) x1 ====
    (0x0805894c, 0x000004cc, 'LP_BAR_ANIM_STATE_OFF', 'tick_equip_effect_act_node_count_off'),

    # ==== SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4 (ewram.inc) x1 ====
    (0x08058950, 0x000004d4, 'SPRITE_ROW_ENTRY_DATA_OFF', 'tick_equip_effect_act_node_zone_off'),

    # ==== CHAIN_NODE_CARD_ARR_OFF = 0x000004f4 (ewram.inc) x1 ====
    (0x08058954, 0x000004f4, 'CHAIN_NODE_CARD_ARR_OFF', 'tick_equip_effect_act_node_slot_off'),

    # ==== ELIGIB_ANIM_STATE_OFF = 0x00001d6c (ewram.inc) x1 ====
    (0x08058be8, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'tick_equip_zone_target_anim_state_off'),

    # ==== EQUIP_ACTIVE_CTX_OFF = 0x00000484 (duel_field.inc, NEW) x1 ====
    (0x08058a8c, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'check_zone_field6_ctx_off'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    For fn-ptr: stored value = target|1 (THUMB).  Check accepts |1.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # fn-ptr REF x1: check_equip_slot_has_active_effect_value+1 = 0x08058639
    (0x080586f0, 0x08058638, 'check_equip_slot_has_active_effect_value',
     'tick_equip_tier_abcx_mode_fn_ptr'),

    # fn-ptr REF x2: check_zone_entity_field6_in_equip_range+1 = 0x08058a41
    (0x08058b80, 0x08058a40, 'check_zone_entity_field6_in_equip_range',
     'tick_equip_zone_target_pred_ptr'),
    (0x08058b9c, 0x08058a40, 'check_zone_entity_field6_in_equip_range',
     'tick_equip_zone_target_pred_ptr_b'),

    # fn-ptr REF x2: check_equip_activation_at_slot11+1 = 0x08065991
    (0x08058c90, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_equip_zone_select_slot_tbl_ptr'),
    (0x08058ca8, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_equip_zone_select_slot_tbl_ptr_b'),
]

# ---------------------------------------------------------------------------
# C. PLATE_SET: (func_entry_addr, new_plate_text)
#    P1-P4: Full ASCII rewrites of CJK mojibake plates.
#    P3 also replaces stale FUN_0805a1dc -> tick_equip_activation_sprite_mode2_by_type.
#    All text verified pure ASCII (ord<=127).
# ---------------------------------------------------------------------------
PLATE_SET = [
    # P1: dispatch_equip_zone_sprite_by_slot_group @ 0x08058578
    (0x08058578,
     'dispatch_equip_zone_sprite_by_slot_group @ 0x08058578\n'
     'Dispatcher: extracts slot_group = card_entry[+2].bits[6:2] (5-bit, via lsls #0x1a; lsrs #0x1b).\n'
     'If slot_group > 4 calls dispatch_equip_activation_score_by_card_id (special path, slots [5..31]).\n'
     'Else calls enqueue_equip_zone_sprite_at_slot (normal OAM sprite write, slots [0..4]).\n'
     'Pass-through callee return value. indeg=0 (fn-ptr table driven). Exit: pop{r1}; bx r1.\n'
     'Params: r0=card_entry_ptr. Returns: r0=u32 callee return pass-through.'),

    # P2: tick_equip_activation_phase_with_effect_enqueue @ 0x080585e8
    (0x080585e8,
     'tick_equip_activation_phase_with_effect_enqueue @ 0x080585e8\n'
     'Equip activation phase tick with effect sprite enqueue as phase-complete side effect.\n'
     'r0=card_entry_ptr. Calls tick_equip_activation_state_by_phase; if returns 0 (phase\n'
     'not complete) returns 0. If returns nonzero (phase complete): checks card_entry[+3].bits[5:4]\n'
     '(mask 0x30); if ==0 (normal equip type) extracts player_id (bit0) and slot_group (bits[6:2])\n'
     'from [+2], calls enqueue_effect_card_slot_sprite_attr(player_id, slot_group, mode=3); if !=0\n'
     '(special type) skips sprite enqueue. Returns 1 (phase tick complete). indeg=0 (fn-ptr driven).\n'
     'Exit: pop{r4}; pop{r1}; bx r1.'),

    # P3: tick_equip_activation_with_sprite_mode2 @ 0x08058858
    #     Old plate had CJK mojibake + stale FUN_0805a1dc (now tick_equip_activation_sprite_mode2_by_type)
    (0x08058858,
     'tick_equip_activation_with_sprite_mode2 @ 0x08058858\n'
     'Equip activation state machine entry wrapper with mode=2 sprite enqueue.\n'
     'Called by tick_equip_activation_sprite_mode2_by_type when type_code==0x3c0.\n'
     'Calls tick_equip_activation_state_machine; saves result r5. If r5==1 (slot selected):\n'
     'extracts player_id and slot_group from card_entry[+2], calls\n'
     'enqueue_sprite_attr_with_mode(player_id, slot_group, 0x16cb=BLACK_LUSTER_SOLDIER_ENVOY_CID,\n'
     'extra=0, mode=2) to enqueue mode=2 sprite attr. Pass-through r5. indeg=1.\n'
     'Exit: pop{r4,r5}; pop{r1}; bx r1.\n'
     'Params: r0=card_entry_ptr; r1=secondary_ptr. Returns: r0=u32 tick result pass-through.'),

    # P4: tick_equip_activation_if_effect_dispatch_ok @ 0x08058a1c
    (0x08058a1c,
     'tick_equip_activation_if_effect_dispatch_ok @ 0x08058a1c\n'
     'Equip activation state machine conditional entry wrapper with effect dispatch pre-check.\n'
     'indeg=0, Sub-type A. Receives card_entry_ptr(r0) and secondary_ptr(r1).\n'
     'Calls dispatch_effect_by_card_id_with_display_lookup(card_entry, secondary_ptr);\n'
     'if returns 0 (effect unavailable) returns -1. If passes, calls tick_equip_activation_state_machine\n'
     'and pass-through its result. Exit: pop{r4,r5}; pop{r1}; bx r1.\n'
     'Params: r0=card_entry_ptr; r1=secondary_ptr.\n'
     'Returns: r0=i32 (-1=effect dispatch failed, else tick_equip_activation_state_machine result).'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    """Verify 4-byte little-endian value at slot_int == want (or want|1 for THUMB fn-ptr)."""
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data at 0x%08x" % slot_int
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF06Seg7Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm      = currentProgram.getSymbolTable()
    fm      = currentProgram.getFunctionManager()
    nA = nB = nC = 0
    made_targets = set()
    fail_count = 0

    # -------------------------------------------------------------------------
    # A. EQ_SLOTS
    # -------------------------------------------------------------------------
    print("--- A. EQ_SLOTS (%d slots) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s want=0x%x)" % (slot_int, err, cname, value))
            fail_count += 1
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # -------------------------------------------------------------------------
    # B. REF_SLOTS
    # -------------------------------------------------------------------------
    print("--- B. REF_SLOTS (%d slots) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        ok, err = _check(slot_int, tgt_int)
        if not ok:
            # fn-ptr slots store THUMB+1 (odd); also try tgt_int|1
            ok2, _ = _check(slot_int, tgt_int | 1)
            if not ok2:
                print("[B FAIL] 0x%08x: %s (target=%s want=0x%x)" % (
                    slot_int, err, gas_label, tgt_int))
                fail_count += 1
                continue
        if DRY:
            print("[B dry] 0x%08x -> %s (0x%08x) slot_label=%s" % (
                slot_int, gas_label, tgt_int, slot_label))
            nB += 1
            continue
        target_addr = _addr(tgt_int)
        if tgt_int not in made_targets:
            createLabel(target_addr, gas_label, True, SourceType.USER_DEFINED)
            made_targets.add(tgt_int)
        ref = rm.addMemoryReference(
            _addr(slot_int), target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s @ 0x%08x)" % (
            slot_int, slot_label, gas_label, tgt_int))
        nB += 1

    # -------------------------------------------------------------------------
    # C. PLATE_SET (full ASCII rewrite, CJK mojibake replacement)
    # -------------------------------------------------------------------------
    print("--- C. PLATE_SET (%d items) ---" % len(PLATE_SET))
    for func_int, new_text in PLATE_SET:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[C FAIL] no CodeUnit @ 0x%08x" % func_int)
            fail_count += 1
            continue
        if DRY:
            print("[C dry] 0x%08x full plate rewrite (%d chars)" % (func_int, len(new_text)))
            nC += 1
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("[C ok] 0x%08x plate set (%d chars)" % (func_int, len(new_text)))
        nC += 1

    print("[done] A=%d B=%d C=%d FAIL=%d (DRY=%s)" % (
        nA, nB, nC, fail_count, DRY))
    if fail_count > 0:
        print("[WARN] %d FAIL(s) above -- review before using non-dry run" % fail_count)


main()
