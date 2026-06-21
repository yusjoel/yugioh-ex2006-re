# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg5aSlots.py -- f10 Seg-5a (0x0807db20..0x0807ec10)
#   6 named functions; 15 residual auto-name slots
#   EQ_SLOTS:    8  (6 REUSE + 2 NEW: TRIGGER_OP_PARAM_10D3, invoke_effect_node_active_fn_ptr)
#   REF_SLOTS:   7  (all REUSE existing globals)
#   RENAME_SLOTS: 1 (DWORD_0807dd5c -> PTR_gP1LifePoints_0807dd5c)
#   FUNC_RENAME: 0
#   PLATE:       0
#
# NOTE: All EOL text is pure ASCII (no CJK).

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
#    8 slots: 6 REUSE + 2 NEW
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # NEW: trigger op param used in tick_equip_oam_activation_text_display
    (0x0807dc04, 0x000010d3, 'TRIGGER_OP_PARAM_10D3',
     'tick_equip_oam_act_text_trig_param',
     'TRIGGER_OP_PARAM_10D3=0x10d3: trigger_card_display_op31_if_not_active 2nd arg'),

    # NEW: THUMB+1 fn-ptr literal pool constant (ROM addr, not EWRAM slot)
    (0x0807dc08, 0x08090625, 'invoke_effect_node_active_fn_ptr',
     'tick_equip_oam_act_text_effect_ptr',
     'invoke_effect_node_active_fn_ptr=0x08090625: THUMB+1 ptr to invoke_effect_node_with_active_flag_3arg; fn at 0x08090624'),

    # REUSE: ELIGIB_SPRITE_CTRL_OFF (ewram.inc line 422)
    (0x0807dc9c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'dispatch_freed_gen_eligib_sprite_off',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68: [gP1LifePoints+0x1d68] eligibility sprite ctrl field'),

    # REUSE: FREED_THE_MATCHLESS_GENERAL_CID (card_info.inc)
    (0x0807dcd4, 0x000014c4, 'FREED_THE_MATCHLESS_GENERAL_CID',
     'dispatch_freed_gen_cid',
     'FREED_THE_MATCHLESS_GENERAL_CID=0x14c4: Freed the Matchless General card ID'),

    # REUSE: LP_ACTIVATION_LINK_FLAG_OFF (ewram.inc line 483)
    (0x0807dd60, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF',
     'submit_monster_equip_lp_act_flag_off',
     'LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: [gP1LifePoints+0x10d0] LP activation link flag'),

    # REUSE: EQUIP_PHASE_FRAME_OFF (ewram.inc line 437)
    (0x0807e2f0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'dispatch_equip_zone_sprite_frame_off_a',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot'),

    # REUSE: PLAYER_BLOCK_STRIDE (ewram.inc line 251)
    (0x0807e38c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_lp_ind_slot_stride',
     'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks'),

    # REUSE: EQUIP_PHASE_FRAME_OFF dup slot (ewram.inc line 437)
    (0x0807e394, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'enqueue_lp_ind_slot_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot (dup)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii, raw)
#    7 slots; all raw=True (direct ptr to EWRAM global, not THUMB+1)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    (0x0807db58, 0x0201e1c8, 'gEquipZoneCountTable',
     'enqueue_equip_zone_sprites_zone_cnt',
     'gEquipZoneCountTable=0x0201e1c8: equip zone count table base', True),

    (0x0807db88, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_oam_act_text_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base', True),

    (0x0807dca0, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_freed_gen_card_ctx',
     'gDuelCardCtxBase=0x0201e2a0: duel card activation context base', True),

    (0x0807dcd0, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_freed_gen_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (dup)', True),

    (0x0807dd64, 0x0201bb90, 'gEquipChainSlotRefs',
     'submit_monster_equip_chain_refs',
     'gEquipChainSlotRefs=0x0201bb90: equip chain slot refs base', True),

    (0x0807e2ec, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_equip_zone_sprite_phase_flags',
     'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (dup)', True),

    (0x0807e390, 0x0201c510, 'gDuelFieldSlots',
     'enqueue_lp_ind_slot_field_slots',
     'gDuelFieldSlots=0x0201c510: duel field zone slot array base', True),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, new_label, eol_ascii)
#    1 rename: DWORD_0807dd5c -> PTR_gP1LifePoints_0807dd5c
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0807dd5c, 'PTR_gP1LifePoints_0807dd5c',
     '.word gP1LifePoints: submit_monster_equip_bitmap_lp_indicator LP base (rename from DWORD_)'),
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
    print("=== RefineF10Seg5aSlots (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    rf = currentProgram.getReferenceManager()
    nA = nB = nC = 0
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
    # B. REF_SLOTS
    # -----------------------------------------------------------------------
    print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for (slot_int, target_int, gas_label, slot_label, eol_text, raw) in REF_SLOTS:
        check_val = target_int if raw else (target_int + 1)
        ok, err = _check(slot_int, check_val)
        if not ok:
            print("[FAIL] REF 0x%08x %s: %s" % (slot_int, gas_label, err))
            fail_count += 1
            continue
        if not DRY:
            slot_a = _addr(slot_int)
            target_a = _addr(target_int)
            sm.createLabel(target_a, gas_label, SourceType.USER_DEFINED)
            rf.addMemoryReference(slot_a, target_a, RefType.DATA, SourceType.USER_DEFINED, 0)
            for ref in rf.getReferencesFrom(slot_a):
                if ref.getToAddress().equals(target_a):
                    rf.setPrimary(ref, True)
                    break
            sm.createLabel(slot_a, slot_label, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[REF ok] 0x%08x -> %s slot=%s" % (slot_int, gas_label, slot_label))
        nB += 1

    # -----------------------------------------------------------------------
    # C. RENAME_SLOTS
    # -----------------------------------------------------------------------
    print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for (slot_int, new_label, eol_text) in RENAME_SLOTS:
        if not DRY:
            slot_a = _addr(slot_int)
            sm.createLabel(slot_a, new_label, SourceType.USER_DEFINED)
            cu = listing.getCodeUnitAt(slot_a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
        print("[RENAME ok] 0x%08x -> %s" % (slot_int, new_label))
        nC += 1

    print("")
    print("=== SUMMARY: EQ=%d REF=%d RENAME=%d FAIL=%d ===" % (nA, nB, nC, fail_count))
    if fail_count > 0:
        print("[ERROR] %d slot(s) FAILED -- see FAIL lines above" % fail_count)
    else:
        print("[OK] All slots applied successfully")


main()
