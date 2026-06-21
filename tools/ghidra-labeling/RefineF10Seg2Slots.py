# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg2Slots.py -- f10 Seg-2 (0x0807ae84..0x0807be2c)
#   18 functions; 51 residual slots: 31 EQ + 6 REF + 14 RENAME
#   All constants REUSE (no new .equ creation).
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (31, all REUSE)
#   B. RENAME_SLOTS -- plain rename (gP1LifePoints already-symbolic + ROM_INCBIN base labels)
#   C. REF_SLOTS  -- USER label + DATA ref for fn-ptr (THUMB+1) slots
#   D. FUNC_RENAME -- tick_equip_zone_target_select_display_seq (drop __0807bc48 suffix)
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
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- commit_serial_spell_effect_node ---
    (0x0807ae9c, 0x0000183e, 'SERIAL_SPELL_CID',
     'commit_serial_spell_serial_cid',
     'SERIAL_SPELL_CID=0x183e: Serial Spell card ID guard'),

    # --- update_zone_entry_sprite_by_descriptor ---
    (0x0807b13c, 0x0201bb90, 'gEquipChainSlotRefs',
     'update_zone_entry_chain_refs_base',
     'gEquipChainSlotRefs: equip chain slot reference array'),
    (0x0807b180, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'update_zone_entry_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807b184, 0x0201c600, 'gP1FieldArrayCBase',
     'update_zone_entry_field_array_c_base',
     'gP1FieldArrayCBase: field array C zone slot array base ptr'),

    # --- enqueue_slot_sprite_for_zone_entry_count_range ---
    (0x0807b1dc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_slot_sprite_zone_entry_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807b1e0, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_slot_sprite_zone_entry_slots_base',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- tick_equip_zone_pair_bitmap_display_seq ---
    (0x0807b268, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_pair_bitmap_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807b334, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_pair_bitmap_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807b338, 0x00001cf4, 'FIELD_STATE_OFF',
     'tick_equip_zone_pair_bitmap_field_state_off',
     'FIELD_STATE_OFF=0x1cf4: [gP1LifePoints+0x1cf4] field state field'),
    (0x0807b33c, 0x0000178b, 'PROTECTOR_OF_THE_SANCTUARY_CID',
     'tick_equip_zone_pair_bitmap_protector_cid',
     'PROTECTOR_OF_THE_SANCTUARY_CID=0x178b: Protector of the Sanctuary CID guard'),
    (0x0807b340, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_zone_pair_bitmap_ctx_base',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x0807b380, 0x00000103, 'EQUIP_ACT_SCORE_MODE_103',
     'tick_equip_zone_pair_bitmap_score_op_103',
     'EQUIP_ACT_SCORE_MODE_103=0x103: op-id arg for equip activation score'),

    # --- enqueue_slot_sprite_with_field5_score_on_zone_match ---
    (0x0807b48c, 0x0201bb90, 'gEquipChainSlotRefs',
     'enqueue_slot_sprite_field5_chain_refs',
     'gEquipChainSlotRefs: equip chain slot reference array'),

    # --- tick_equip_prng_sample_or_lp_indicator ---
    (0x0807b6d4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_prng_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807b704, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_prng_ctx_base',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x0807b760, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'tick_equip_prng_lp_track_next_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] LP card tracking next ptr'),

    # --- invoke_equip_oam_for_chain_zone_slot_if_placeable ---
    (0x0807b7d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'invoke_equip_oam_chain_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807b7d8, 0x0201c880, 'gP1ChainZoneArray',
     'invoke_equip_oam_chain_zone_base',
     'gP1ChainZoneArray: P1 chain zone slot array base (EWRAM 0x0201c880)'),

    # --- dispatch_equip_sprite_for_all_zone_slots_by_player ---
    (0x0807bb88, 0x0201e1c8, 'gEquipZoneCountTable',
     'dispatch_equip_sprite_all_zones_count_table',
     'gEquipZoneCountTable=0x0201e1c8: equip zone active count table'),

    # --- tick_draw_counter_lp_display_seq ---
    (0x0807bbe8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_draw_counter_lp_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807bc20, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_draw_counter_lp_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807bc44, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'tick_draw_counter_lp_card_track_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base'),

    # --- tick_equip_zone_target_select_display_seq ---
    (0x0807bc68, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_target_select_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
    (0x0807bcdc, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_target_select_iter_slot_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame iteration slot'),
    (0x0807bce0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_target_select_player_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),
    (0x0807bce4, 0x0201c510, 'gDuelFieldSlots',
     'tick_equip_zone_target_select_slots_base',
     'gDuelFieldSlots: duel field zone slot array base'),
    (0x0807bd24, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_target_select_iter_slot_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in state-0x7f branch'),
    (0x0807bd4c, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_equip_zone_target_select_ctx_base',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x0807bda4, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'tick_equip_zone_target_select_banisher_ctx_off',
     'LP_BANISHER_CTX_OFF=0x1d70: [gP1LifePoints+0x1d70] LP banisher context offset'),
    (0x0807bda8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_target_select_player_stride_b',
     'PLAYER_BLOCK_STRIDE=0x868: dup in banisher path'),

    # --- tick_equip_zone_sprite_display_seq_by_eligibility ---
    (0x0807bddc, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_sprite_eligib_phase_flags',
     'gDuelPhaseFlags: duel phase flags struct base'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii)
#    6 gP1LifePoints symbolic slots + 4 PTR_gP1LifePoints_* slots
#    + 4 ROM_INCBIN base labels (will be replaced by disasm labels)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # --- tick_equip_zone_pair_bitmap_display_seq LP dup slots ---
    (0x0807b330, 'tick_equip_zone_pair_bitmap_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_zone_pair_bitmap state-0x7e path A)'),
    (0x0807b3a4, 'tick_equip_zone_pair_bitmap_lp_base_b',
     '.word gP1LifePoints: LP state struct base (tick_equip_zone_pair_bitmap state-0x7e path B)'),
    (0x0807b3c4, 'tick_equip_zone_pair_bitmap_lp_base_c',
     '.word gP1LifePoints: LP state struct base (tick_equip_zone_pair_bitmap state-0x7f path)'),
    # --- tick_equip_prng_sample_or_lp_indicator LP dup slots ---
    (0x0807b708, 'tick_equip_prng_lp_base',
     '.word gP1LifePoints: LP state struct base (tick_equip_prng path A)'),
    (0x0807b734, 'tick_equip_prng_lp_base_b',
     '.word gP1LifePoints: LP state struct base (tick_equip_prng path B)'),
    (0x0807b75c, 'tick_equip_prng_lp_base_c',
     '.word gP1LifePoints: LP state struct base (tick_equip_prng path C)'),
    # --- ROM_INCBIN base labels (after disasm become first sub-stub labels) ---
    (0x0807afb8, 'lighten_the_load_dispatch_stubs',
     'R4 disasm entry base: BLK2 Lighten the Load dispatch sub-stubs (6 entries)'),
    (0x0807b574, 'hero_kid_hyena_dispatch_stubs',
     'R4 disasm entry base: BLK4 Hero Kid/Hyena dispatch sub-stubs (7 entries)'),
    (0x0807b878, 'equip_sprite_dispatch_stubs_b878',
     'R4 disasm entry base: BLK6 Rescue Cat dispatch sub-stubs (7 entries)'),
    (0x0807ba30, 'equip_sprite_dispatch_stubs_ba30',
     'R4 disasm entry base: BLK8 Gatling Dragon dispatch sub-stubs (5 entries)'),
    # --- PTR_gP1LifePoints_* slots (already-symbolic, wrong label) ---
    (0x0807bc1c, 'tick_draw_counter_lp_lp_base',
     '.word gP1LifePoints: tick_draw_counter_lp_display_seq LP ptr A'),
    (0x0807bc40, 'tick_draw_counter_lp_lp_base_b',
     '.word gP1LifePoints: tick_draw_counter_lp_display_seq LP ptr B'),
    (0x0807bd28, 'tick_equip_zone_target_select_lp_base',
     '.word gP1LifePoints: tick_equip_zone_target_select_display_seq LP ptr A'),
    (0x0807bda0, 'tick_equip_zone_target_select_lp_base_b',
     '.word gP1LifePoints: tick_equip_zone_target_select_display_seq LP ptr B'),
]

# ---------------------------------------------------------------------------
# C. REF_SLOTS: (slot_addr, target_addr, fn_name, slot_label, eol_ascii)
#    fn-ptr THUMB+1 slots: set USER label + DATA ref
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0807b328, 0x080507ac, 'check_equip_slot_eligible_by_type_query',
     'tick_equip_zone_pair_bitmap_zone_pred_fn_a',
     'fn-ptr check_equip_slot_eligible_by_type_query+1 (THUMB+1)'),
    (0x0807b32c, 0x08051abc, 'check_equip_slot_eligible_by_side_and_setcode',
     'tick_equip_zone_pair_bitmap_zone_pred_fn_b',
     'fn-ptr check_equip_slot_eligible_by_side_and_setcode+1 (THUMB+1)'),
    (0x0807b3cc, 0x080507ac, 'check_equip_slot_eligible_by_type_query',
     'tick_equip_zone_pair_bitmap_zone_pred_fn_a_b',
     'fn-ptr check_equip_slot_eligible_by_type_query+1 dup (THUMB+1)'),
    (0x0807b3e4, 0x08051abc, 'check_equip_slot_eligible_by_side_and_setcode',
     'tick_equip_zone_pair_bitmap_zone_pred_fn_b_b',
     'fn-ptr check_equip_slot_eligible_by_side_and_setcode+1 dup (THUMB+1)'),
    (0x0807bd50, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_equip_zone_target_select_activation_fn',
     'fn-ptr check_equip_activation_at_slot11+1 (THUMB+1)'),
    (0x0807bd68, 0x08065990, 'check_equip_activation_at_slot11',
     'tick_equip_zone_target_select_activation_fn_b',
     'fn-ptr check_equip_activation_at_slot11+1 dup (THUMB+1)'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF10Seg2Slots (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    nA = nB = nC = nD = 0

    # ---- A: EQ_SLOTS ----
    for slot_int, value, cname, label, eol in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        listing.setComment(_addr(slot_int), CodeUnit.EOL_COMMENT, eol)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # ---- B: RENAME_SLOTS ----
    for slot_int, label, eol in RENAME_SLOTS:
        if DRY:
            print("[B dry] 0x%08x rename %s" % (slot_int, label)); nB += 1; continue
        a = _addr(slot_int)
        createLabel(a, label, True, SourceType.USER_DEFINED)
        listing.setComment(a, CodeUnit.EOL_COMMENT, eol)
        print("[B ok] 0x%08x -> %s" % (slot_int, label))
        nB += 1

    # ---- C: REF_SLOTS (fn-ptr THUMB+1) ----
    for slot_int, target_int, fn_name, label, eol in REF_SLOTS:
        if DRY:
            print("[C dry] 0x%08x -> %s+1 label=%s" % (slot_int, fn_name, label))
            nC += 1; continue
        slot_addr = _addr(slot_int)
        target_addr = _addr(target_int)
        # Label the target function (ensure it has the canonical name)
        createLabel(target_addr, fn_name, True, SourceType.USER_DEFINED)
        # Label the pool slot
        createLabel(slot_addr, label, True, SourceType.USER_DEFINED)
        # Add DATA ref from slot to target
        refMgr = currentProgram.getReferenceManager()
        refMgr.addMemoryReference(slot_addr, target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        # Set primary
        for ref in refMgr.getReferencesFrom(slot_addr):
            if ref.getToAddress().equals(target_addr):
                refMgr.setPrimary(ref, True)
        listing.setComment(slot_addr, CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s+1 label=%s" % (slot_int, fn_name, label))
        nC += 1

    # ---- D: FUNC_RENAME ----
    old_addr = 0x0807bc48
    old_name = 'tick_equip_zone_target_select_display_seq__0807bc48'
    new_name = 'tick_equip_zone_target_select_display_seq'
    if DRY:
        print("[D dry] FUNC_RENAME 0x%08x: %s -> %s" % (old_addr, old_name, new_name))
        nD += 1
    else:
        fm = currentProgram.getFunctionManager()
        fn = fm.getFunctionAt(_addr(old_addr))
        if fn is None:
            print("[D WARN] no function at 0x%08x, trying getFunctionContaining" % old_addr)
            fn = fm.getFunctionContaining(_addr(old_addr))
        if fn is not None:
            actual_name = fn.getName()
            fn.setName(new_name, SourceType.USER_DEFINED)
            print("[D ok] FUNC_RENAME 0x%08x: %s -> %s" % (old_addr, actual_name, new_name))
        else:
            print("[D WARN] function not found at 0x%08x" % old_addr)
        nD += 1

    print("=== Done: A=%d B=%d C=%d D=%d ===" % (nA, nB, nC, nD))


main()
