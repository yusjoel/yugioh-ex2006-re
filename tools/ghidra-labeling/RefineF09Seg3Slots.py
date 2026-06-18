# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg3Slots.py -- F09 Seg-3 (0x0807104c..0x080719fc)
#   dispatch_equip_chain_effect_slot + enqueue_field_slot_overlay +
#   enqueue_eligible_slot + tick_equip_lp + Neo Daedalus OAM (20 fn)
#
#   EQ=35  (33 REUSE + 2 NEW: EQUIP_ZONE_WORD_MASK / FREED_THE_MATCHLESS_GENERAL_CID)
#   REF=0
#   FNPTR=4  (RENAME_SLOTS: 2 fn-ptrs + 1 dispatch-table base + 1 block-start)
#   FUNC_RENAME=0
#   PLATE=2  (L6141 CJK rewrite + L6209 stale FUN_)
#
# NEW constants added to constants/*.inc before running:
#   duel_field.inc: EQUIP_ZONE_WORD_MASK=0x00f0ffff
#   card_info.inc:  FREED_THE_MATCHLESS_GENERAL_CID=0x000014c4
#                   DRAGGED_DOWN_INTO_GRAVE_CID=0x000014e8 (EOL only, no data-slot)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_220254-pre-F09Seg3

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
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    35 slots total (33 REUSE + 2 NEW)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- dispatch_equip_chain_effect_slot_by_state (0x0807104c..0x0807116f) ----
    # gDuelPhaseFlags = 0x0201b290 (reuse ewram.inc)
    (0x0807106c, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_106c', None),

    # ---- enqueue_field_slot_overlay_sprite_if_chain_matches / nearby fns ----
    # (0x08071170..0x0807120f)
    # gP1LifePoints = 0x0201c4e0 (reuse ewram.inc)
    (0x08071138, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_1138', None),
    # LP_CARD_TRACK_BASE_OFF = 0x1da8 (reuse ewram.inc)
    (0x0807113c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_113c', None),
    # PLAYER_BLOCK_STRIDE = 0x868 (reuse ewram.inc)
    (0x08071140, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_1140', None),

    # ---- enqueue_eligible_slot_sprites_for_both_players (0x08071210..0x08071257) ----
    # PLAYER_BLOCK_STRIDE
    (0x08071204, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_1204', None),
    # gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)
    (0x08071208, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_1208', None),
    # BLUE_EYES_SHINING_DRAGON_CID = 0x17c2 (reuse card_info.inc)
    (0x0807120c, 0x000017c2, 'BLUE_EYES_SHINING_DRAGON_CID', 'blue_eyes_shining_cid_120c',
     'BLUE_EYES_SHINING_DRAGON_CID=0x17c2: Blue-Eyes Shining Dragon; enqueue_eligible_slot_sprites_for_both_players CID filter'),

    # ---- check_effect_slot_equip_zone_pattern (0x08071258..0x08071283) ----
    # EQUIP_ZONE_WORD_MASK = 0x00f0ffff (NEW duel_field.inc)
    (0x08071280, 0x00f0ffff, 'EQUIP_ZONE_WORD_MASK', 'equip_zone_mask_1280',
     'EQUIP_ZONE_WORD_MASK=0x00f0ffff: zone_word bitmask; ANDs zone_word then cmp 0xa6<<5=0x14c0 for equip pattern'),

    # ---- dispatch_equip_chain_state_if_tile_count_valid (0x080712a0..0x0807136b) ----
    # PLAYER_BLOCK_STRIDE x3
    (0x08071338, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_1338', None),
    # gDuelFieldSlots
    (0x0807133c, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_133c', None),
    # gDuelPhaseFlags
    (0x08071340, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_1340', None),
    # FREED_THE_MATCHLESS_GENERAL_CID = 0x14c4 (NEW card_info.inc)
    (0x08071344, 0x000014c4, 'FREED_THE_MATCHLESS_GENERAL_CID', 'freed_matchless_cid_1344',
     'FREED_THE_MATCHLESS_GENERAL_CID=0x14c4: Freed the Matchless General (pw=49681811); chain check param'),

    # ---- enqueue_overlay_sprite_if_tile_count_equal / enqueue_equip_sprite_guarded_by_zone_type13 ----
    # (0x0807136c..0x0807142b)
    # PLAYER_BLOCK_STRIDE
    (0x080713ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_13ec', None),
    # gDuelFieldSlots
    (0x080713f0, 0x0201c510, 'gDuelFieldSlots', 'gduel_slots_13f0', None),

    # ---- enqueue_sprite_attr_type11_from_chain_entry / nearby (0x08071488..0x080714ab) ----
    # gP1LifePoints
    (0x080714a4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_14a4', None),
    # P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (reuse ewram.inc)
    (0x080714a8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_14a8', None),

    # ---- dispatch_equip_zone11_target_by_activation_state (0x080714ec..0x0807158b) ----
    # gDuelPhaseFlags
    (0x08071508, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_1508', None),
    # gP1LifePoints
    (0x08071568, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_1568', None),
    # ELIGIB_SPRITE_CTRL_OFF = 0x1d68 (reuse ewram.inc)
    (0x0807156c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_156c', None),
    # ELIGIB_ANIM_STATE_OFF = 0x1d6c (reuse ewram.inc)
    (0x08071570, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_state_1570', None),

    # ---- tick_zone_sprite_pipeline_with_chain_counter (0x08071604..0x08071653) ----
    # gDuelPhaseFlags
    (0x08071644, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_1644', None),
    # EQUIP_PHASE_FRAME_OFF = 0x4a4 (reuse ewram.inc)
    (0x08071648, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_1648', None),

    # ---- dispatch_hand_card_sprite_by_effect_slot_zone (0x08071654..0x080717ef) ----
    # PLAYER_BLOCK_STRIDE
    (0x080716dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_16dc', None),
    # gP1HandSlotArray = 0x0201c8f8 (reuse ewram.inc)
    (0x080716e0, 0x0201c8f8, 'gP1HandSlotArray', 'gp1hand_16e0', None),

    # ---- tick_equip_lp_spell_zone_display_state (0x080717f0..0x080718c3) ----
    # gDuelPhaseFlags
    (0x08071810, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_1810', None),
    # EQUIP_PHASE_FRAME_OFF
    (0x08071850, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_1850', None),
    # gP1LifePoints
    (0x08071888, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_1888', None),
    # LP_CARD_TRACK_BASE_OFF
    (0x0807188c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_188c', None),
    # EQUIP_PHASE_FRAME_OFF
    (0x080718a8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_18a8', None),

    # ---- tick_equip_neo_daedalus_oam_display_state (0x0807190c..0x080719fb) ----
    # gDuelPhaseFlags
    (0x08071928, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_1928', None),
    # gP1LifePoints
    (0x08071998, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_1998', None),
    # LP_CARD_TRACK_BASE_OFF
    (0x0807199c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_199c', None),
    # gDuelCardCtxBase = 0x0201e2a0 (reuse ewram.inc)
    (0x080719a0, 0x0201e2a0, 'gDuelCardCtxBase', 'gduel_card_ctx_19a0', None),
    # gP1LifePoints
    (0x080719d4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_19d4', None),
    # LP_CARD_TRACK_BASE_OFF
    (0x080719d8, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_off_19d8', None),

]

# ---------------------------------------------------------------------------
# B. FNPTR_SLOTS (RENAME_SLOTS): (slot_addr, value, slot_label, eol_ascii)
#    4 entries: 2 fn-ptrs + 1 dispatch-table base + 1 block-start
# ---------------------------------------------------------------------------
FNPTR_SLOTS = [
    # DWORD_0807129c = 0x08071259 = check_effect_slot_equip_zone_pattern+1
    (0x0807129c, 0x08071259, 'check_effect_slot_equip_zone_pattern_ptr',
     'check_effect_slot_equip_zone_pattern+1 (THUMB fn-ptr; passed to find_equip_chain_node_by_pred by scan_equip_chain_for_zone_pattern_sprites)'),
    # DWORD_08071538 = 0x08090625 = invoke_effect_node_with_active_flag_3arg+1
    (0x08071538, 0x08090625, 'invoke_effect_node_with_active_flag_3arg_ptr_1538',
     'invoke_effect_node_with_active_flag_3arg+1 (THUMB fn-ptr; same as invoke_effect_node_with_active_flag_3arg_ptr_0a64 in Seg-2 at 0x08070a64; passed to set_equip_activation_state_by_mode as mode/fn param)'),
    # PTR_DAT_08071740 = 0x080717c4 = dispatch table base [0]
    (0x08071740, 0x080717c4, 'equip_lp_disp_sub_table',
     'dispatch table [0]=equip_lp_sub_7c4/[1]=equip_lp_sub_7a4/[2]=equip_lp_sub_78a/[3]=equip_lp_sub_77c/[4]=equip_lp_sub_754'),
    # DAT_08071754 = ROM_INCBIN block 2 start (first sub-stub entry equip_lp_sub_754)
    (0x08071754, 0x280068d8, 'equip_lp_sub_stubs_754',
     'THUMB dispatch sub-stubs for equip_lp_disp_sub_table (5 entries: 7c4/7a4/78a/77c/754)'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, label):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True


def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- FAIL" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        if bad:
            print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
        else:
            cu = currentProgram.getListing().getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_fnptr(slot_addr, value, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if not _check(slot_addr, value, slot_label):
        print("[SKIP] FNPTR 0x%08x value mismatch -- FAIL" % slot_addr)
        return False

    if DRY:
        print("[dry] FNPTR 0x%08x  0x%08x  label=%s" % (slot_addr, value, slot_label))
        return True

    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in existing:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        if bad:
            print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
        else:
            cu = currentProgram.getListing().getCodeUnitAt(a)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[FNPTR] 0x%08x  0x%08x  -> %s" % (slot_addr, value, slot_label))
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg3Slots (DRY=%s) ===" % DRY)
    print("  Seg-3: 0x0807104c..0x080719fc")
    print("  EQ=%d  FNPTR=%d" % (len(EQ_SLOTS), len(FNPTR_SLOTS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES !!!" % eq_fail)

    # B. FNPTR_SLOTS
    print("\n--- B. FNPTR_SLOTS (%d) ---" % len(FNPTR_SLOTS))
    fnptr_ok = fnptr_fail = 0
    for slot_addr, value, slot_label, eol in FNPTR_SLOTS:
        if _apply_fnptr(slot_addr, value, slot_label, eol):
            fnptr_ok += 1
        else:
            fnptr_fail += 1
    print("  FNPTR done: %d ok, %d fail" % (fnptr_ok, fnptr_fail))
    if fnptr_fail > 0:
        print("  !!! %d FNPTR FAILURES !!!" % fnptr_fail)

    print("\n=== RefineF09Seg3Slots DONE ===")
    print("  EQ=%d/%d ok  FNPTR=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS),
        fnptr_ok, len(FNPTR_SLOTS)))


main()
