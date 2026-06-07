# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg5Slots.py -- f01 Seg-5 (0x0801e714..0x0801f25c)
#   asm/01_vija_scene_text.s: card_info tick + duel/card_info dispatch, 10 functions:
#   tick_card_info_page_by_state / get_card_data_format_id / lookup_card_entry_by_index /
#   load_card_fs_entry_to_struct / fill_card_fs_display_entries /
#   fill_card_fs_display_entries_for_card_list / tick_duel_field_main_frame /
#   dispatch_card_display_op / play_ui_effect / copy_game_text_if_raw
#
# Sections:
#   A. EQ_SLOTS   -- 52 data-equate slots (11 new ewram globals + 11 offset/mask constants + reuse)
#   B. RENAME_SLOTS -- 12 plain renames (10 PTR_/DAT_ + 2 C13 additions: DAT_0801e744/DAT_0801eb3c)
#   C. REF_SLOTS  -- 3 USER-label + DATA-ref (card_deck_fs_path_table + 2 jump table ptrs)
#   D. PLATE_REWRITES -- 1 plate (play_ui_effect CJK -> ASCII)
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
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # === tick_card_info_page_by_state (0x0801e714) ===
    (0x0801e748, 0x02023130, 'gDuelFieldState',
     'tick_card_info_page_by_state_duel_field_state',
     'gDuelFieldState base; [+0x222] bit2=prng-anim active; 170 raw refs'),
    (0x0801e74c, 0x00000222, 'DUEL_FIELD_PRNG_ANIM_FLAG_OFF',
     'tick_card_info_page_by_state_duel_field_prng_anim_flag_off',
     'offset into gDuelFieldState: [gDuelFieldState+0x222] bit2=prng-driven anim active'),

    # === load_card_fs_entry_to_struct (0x0801e7cc) ===
    (0x0801e84c, 0x0201e2b4, 'gCardFsDataBlock',
     'load_card_fs_entry_to_struct_card_fs_data_block',
     'gCardFsDataBlock base; card FS slot data block (stride=0x108); 4 raw refs'),

    # === fill_card_fs_display_entries (0x0801e850) ===
    (0x0801e968, 0x0201e2b4, 'gCardFsDataBlock',
     'fill_card_fs_display_entries_card_fs_data_block',
     None),
    (0x0801e970, 0x0201ff60, 'gCardIdCache',
     'fill_card_fs_display_entries_card_id_cache',
     'gCardIdCache base; EWRAM card id lookup/mapping cache; 5 raw refs'),

    # === fill_card_fs_display_entries_for_card_list (0x0801e974) ===
    (0x0801e980, 0x02001138, 'gCardListDisplayBuf',
     'fill_card_fs_display_entries_for_card_list_display_buf',
     'gCardListDisplayBuf; card list slot display buffer; 12 raw refs'),

    # === tick_duel_field_main_frame (0x0801e984) ===
    (0x0801e9ec, 0x02023130, 'gDuelFieldState',
     'tick_duel_field_main_frame_duel_field_state_a',
     None),
    (0x0801e9f0, 0x0000021e, 'DUEL_FIELD_FADEIN_FLAG_OFF',
     'tick_duel_field_main_frame_fadein_flag_off',
     'offset: [gDuelFieldState+0x21e] bit0=fadein active; 31 raw refs'),
    (0x0801e9f4, 0x00000226, 'DUEL_FIELD_STATE_226_OFF',
     'tick_duel_field_main_frame_state_226_off',
     'offset: [gDuelFieldState+0x226] bit0=scene entry done; 19 raw refs'),
    (0x0801ea40, 0x0201f440, 'gFontState',
     'tick_duel_field_main_frame_font_state_a',
     'gFontState; font rendering global state; 91 raw refs'),
    (0x0801ea44, 0x02020160, 'gDuelCtx',
     'tick_duel_field_main_frame_duel_ctx_a',
     'gDuelCtx base; duel context; 95 raw refs'),
    (0x0801ea48, 0x00002f51, 'DUEL_CTX_ZONE_STATE_OFF',
     'tick_duel_field_main_frame_zone_state_off_a',
     'offset: [gDuelCtx+0x2f51] bit0=zone display active; 25 raw refs'),
    (0x0801eb20, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'tick_duel_field_main_frame_p1lp_block2_off',
     'offset: [gP1LifePoints+0x1d08] duel field LP display field; 35 raw refs'),
    (0x0801eb24, 0x02023360, 'gDuelSceneBase',
     'tick_duel_field_main_frame_duel_scene_base_a',
     'gDuelSceneBase; duel scene/campaign base; 192 raw refs'),
    (0x0801eb28, 0x00000222, 'DUEL_FIELD_PRNG_ANIM_FLAG_OFF',
     'tick_duel_field_main_frame_prng_anim_flag_off_b',
     None),
    (0x0801eb2c, 0x02020160, 'gDuelCtx',
     'tick_duel_field_main_frame_duel_ctx_b',
     None),
    (0x0801eb30, 0x00002f51, 'DUEL_CTX_ZONE_STATE_OFF',
     'tick_duel_field_main_frame_zone_state_off_b',
     None),
    (0x0801eb34, 0x0201ff30, 'gCardCtxSlotData',
     'tick_duel_field_main_frame_card_ctx_slot_data',
     'gCardCtxSlotData; card context slot data base; 29 raw refs'),
    (0x0801eb38, 0x0201f440, 'gFontState',
     'tick_duel_field_main_frame_font_state_b',
     None),
    (0x0801eb44, 0x00001cec, 'P1LP_TIMER_OFF',
     'tick_duel_field_main_frame_p1lp_timer_off',
     'offset: [gP1LifePoints+0x1cec] duel field timer field; 29 raw refs'),
    (0x0801eb74, 0x02023130, 'gDuelFieldState',
     'tick_duel_field_main_frame_duel_field_state_b',
     None),
    (0x0801eb78, 0x00000222, 'DUEL_FIELD_PRNG_ANIM_FLAG_OFF',
     'tick_duel_field_main_frame_prng_anim_flag_off_c',
     None),
    (0x0801eb7c, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_duel_field_main_frame_duel_card_ctx_a',
     'gDuelCardCtxBase; duel card activation context; 442 raw refs'),
    (0x0801ebbc, 0x00000213, 'GPRNG_PRNG_STATE_OFF213',
     'tick_duel_field_main_frame_prng_state_213_a',
     'offset: [gPrng+0x213] bit7=prng-anim state flag; 37 raw refs'),
    (0x0801ebfc, 0x00000213, 'GPRNG_PRNG_STATE_OFF213',
     'tick_duel_field_main_frame_prng_state_213_b',
     None),
    (0x0801ec00, 0x0201e2a0, 'gDuelCardCtxBase',
     'tick_duel_field_main_frame_duel_card_ctx_b',
     None),
    (0x0801ec08, 0x00000217, 'GPRNG_PRNG_STATE_OFF217',
     'tick_duel_field_main_frame_prng_state_217_a',
     'offset: [gPrng+0x217] bit7=prng-anim LP flag; 12 raw refs'),
    (0x0801ec38, 0x00000217, 'GPRNG_PRNG_STATE_OFF217',
     'tick_duel_field_main_frame_prng_state_217_b',
     None),
    (0x0801ec3c, 0x0201f440, 'gFontState',
     'tick_duel_field_main_frame_font_state_c',
     None),
    (0x0801ec58, 0x02020160, 'gDuelCtx',
     'tick_duel_field_main_frame_duel_ctx_c',
     None),
    (0x0801ec5c, 0x00002f51, 'DUEL_CTX_ZONE_STATE_OFF',
     'tick_duel_field_main_frame_zone_state_off_c',
     None),
    (0x0801ec94, 0x00000213, 'GPRNG_PRNG_STATE_OFF213',
     'tick_duel_field_main_frame_prng_state_213_c',
     None),
    (0x0801ec98, 0x00000217, 'GPRNG_PRNG_STATE_OFF217',
     'tick_duel_field_main_frame_prng_state_217_c',
     None),

    # === dispatch_card_display_op (0x0801ec9c) ===
    (0x0801ee5c, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_card_display_op_duel_card_ctx',
     None),
    (0x0801eed4, 0x020230f0, 'gZoneActivTable',
     'dispatch_card_display_op_zone_activ_table',
     'gZoneActivTable; zone activation player table (2-word array [p0,p1]); 1 raw ref (med-conf)'),
    (0x0801eed8, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_card_display_op_duel_card_ctx_b',
     None),
    (0x0801eedc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'dispatch_card_display_op_player_block_stride',
     'player data block stride 0x868=2152 bytes; 2146 raw refs'),
    (0x0801eee0, 0x0201c4ec, 'gP1ZoneHandCount',
     'dispatch_card_display_op_p1_zone_hand_count',
     'gP1ZoneHandCount = gP1LifePoints+0xc; player zone/hand count table base; 23 raw refs'),
    (0x0801ef1c, 0x02023130, 'gDuelFieldState',
     'dispatch_card_display_op_duel_field_state_a',
     None),
    (0x0801ef34, 0x02023130, 'gDuelFieldState',
     'dispatch_card_display_op_duel_field_state_b',
     None),

    # === play_ui_effect (0x0801ef94) ===
    (0x0801f0fc, 0x0201f440, 'gFontState',
     'play_ui_effect_font_state_a',
     None),
    (0x0801f100, 0x02020160, 'gDuelCtx',
     'play_ui_effect_duel_ctx_a',
     None),
    (0x0801f104, 0x00002f51, 'DUEL_CTX_ZONE_STATE_OFF',
     'play_ui_effect_zone_state_off_a',
     None),
    (0x0801f124, 0x02020160, 'gDuelCtx',
     'play_ui_effect_duel_ctx_b',
     None),
    (0x0801f128, 0x00002f51, 'DUEL_CTX_ZONE_STATE_OFF',
     'play_ui_effect_zone_state_off_b',
     None),
    (0x0801f158, 0x0000023f, 'GPRNG_BANNER_FLAG_OFF',
     'play_ui_effect_gprng_banner_flag_off',
     'offset: [gPrng+0x23f] bit0=banner-anim active; 279 raw refs'),
    (0x0801f184, 0x0201f440, 'gFontState',
     'play_ui_effect_font_state_b',
     None),
    (0x0801f188, 0x02020160, 'gDuelCtx',
     'play_ui_effect_duel_ctx_c',
     None),
    (0x0801f18c, 0x00002f51, 'DUEL_CTX_ZONE_STATE_OFF',
     'play_ui_effect_zone_state_off_c',
     None),

    # === copy_game_text_if_raw (0x0801f238) ===
    (0x0801f258, 0xfffe0000, 'GAME_STR_RAW_ID_MASK',
     'copy_game_text_if_raw_raw_id_mask',
     'raw game string ID mask bits[31:17]==0; 485 raw refs'),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # tick_duel_field_main_frame -- PTR_gPrng slots
    (0x0801e9f8, 'tick_duel_field_main_frame_gprng',   None),
    (0x0801eb40, 'tick_duel_field_main_frame_gprng_b', None),
    (0x0801ebb8, 'tick_duel_field_main_frame_gprng_c', None),
    (0x0801ec04, 'tick_duel_field_main_frame_gprng_d', None),
    (0x0801ec34, 'tick_duel_field_main_frame_gprng_e', None),
    (0x0801ec90, 'tick_duel_field_main_frame_gprng_f', None),
    # tick_duel_field_main_frame -- PTR_gP1LifePoints
    (0x0801eb1c, 'tick_duel_field_main_frame_p1lp',    None),
    # play_ui_effect -- already-symbolized DAT_ slots
    (0x0801f0b8, 'play_ui_effect_ui_effect_state',     None),
    (0x0801f1a4, 'play_ui_effect_banner_state',        None),
    (0x0801f154, 'play_ui_effect_gprng',               None),
    # C13 additions (reviewer #1 and #2):
    # #1: DAT_0801e744 = gCardInfoPageState (0x0201afb0), needs slot label rename
    (0x0801e744, 'tick_card_info_page_by_state_card_info_page_state', None),
    # #2: DAT_0801eb3c = gBannerState (already symbolized), needs slot label rename
    (0x0801eb3c, 'tick_duel_field_main_frame_banner_state_b',         None),
]

# ---------------------------------------------------------------------------
# C. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER label at target, DATA ref from slot to target, setPrimary, slot label.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # lookup_card_entry_by_index -- ROM table pointer
    (0x0801e7c8, 0x09e58b08,
     'card_deck_fs_path_table',
     'lookup_card_entry_by_index_card_deck_fs_path_table'),
    # dispatch_card_display_op -- jump table pointer (target already labeled)
    (0x0801ecc0, 0x0801ecc4,
     'switchD_0801ecbc__switchdataD_0801ecc4',
     'dispatch_card_display_op_jt_ptr'),
    # play_ui_effect -- jump table pointer (target already labeled)
    (0x0801efa8, 0x0801efac,
     'switchD_0801efa4__switchdataD_0801efac',
     'play_ui_effect_jt_ptr'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, new_plate_ascii_text)
#    All text pure ASCII -- no CJK.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # play_ui_effect (0x0801ef94) -- CJK -> ASCII rewrite
    (0x0801ef94,
     'UI effect dispatcher (per-frame tick). r0=effect_id [0..0x3d]; dispatches ~28 independent\n'
     'effect handler sub-state-machines; returns busy(0)/done(1). Unrecognized IDs fall through\n'
     'to caseD_7 (returns 0). Known effects: 0x01=banner_anim_state_machine (pack banner enter/exit),\n'
     '0x1a=play_card_zoom_in (small->large zoom transition), 0x3c=play_demo_shuen (ending cinematic).\n'
     'Other cases delegated to play_ui_effect_<id_hex> stubs. cmp upper bound 0x3d; >0x3d -> default.\n'
     'case 0/0x18/0x19 share caseD_0 (state-bit check -> run_ui_effect_card_pair_state_machine or\n'
     'dispatch_ui_effect_by_card_type); case 1: [gPrng+0x23f] bit0 -> banner_anim_state_machine\n'
     'else tick_banner_pack_state_machine; case 2: gBannerState[+4] state [1..3] dispatch.\n'
     'case 0x31/0x32 inline reads (no bl, special readback).'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return 0

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return 1

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return 1

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return 1

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))
    return 1

def _apply_ref(slot_addr, target_addr, gas_label, slot_label):
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)

    if DRY:
        print("[dry] REF  0x%08x -> 0x%08x  gas=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return 1

    # label at target
    existing_t = sym_tbl.getSymbols(a_target)
    tnames = [s.getName() for s in existing_t]
    if gas_label not in tnames:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    # DATA ref slot -> target
    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)

    # set primary on target label
    for sym in sym_tbl.getSymbols(a_target):
        if sym.getName() == gas_label:
            sym.setPrimary()
            break

    # label at slot
    existing_s = sym_tbl.getSymbols(a_slot)
    snames = [s.getName() for s in existing_s]
    if slot_label not in snames:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    print("[REF] 0x%08x -> 0x%08x  (%s / %s)" % (slot_addr, target_addr, gas_label, slot_label))
    return 1

def _apply_plate(func_addr, new_plate_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] PLATE 0x%08x: no code unit" % func_addr)
        return 0
    if DRY:
        print("[dry] PLATE 0x%08x: rewrite (%d chars)" % (func_addr, len(new_plate_text)))
        return 1
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: plate set (%d chars)" % (func_addr, len(new_plate_text)))
    return 1

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF01Seg5Slots (DRY=%s) ===" % DRY)
    print("  f01-Seg-5: 0x0801e714..0x0801f25c, 10 fn, card_info+duel dispatch")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        eq_ok += _apply_eq(slot_addr, value, eq_name, slot_label, eol)
    print("  EQ done: %d / %d" % (eq_ok, len(EQ_SLOTS)))

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        ren_ok += _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d / %d" % (ren_ok, len(RENAME_SLOTS)))

    # C. REF_SLOTS
    print("\n--- C. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        ref_ok += _apply_ref(slot_addr, target_addr, gas_label, slot_label)
    print("  REF done: %d / %d" % (ref_ok, len(REF_SLOTS)))

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plt_ok = 0
    for func_addr, new_plate in PLATE_REWRITES:
        plt_ok += _apply_plate(func_addr, new_plate)
    print("  PLATE done: %d / %d" % (plt_ok, len(PLATE_REWRITES)))

    print("\n=== RefineF01Seg5Slots DONE ===")
    print("  EQ=%d  RENAME=%d  REF=%d  PLATE=%d" % (eq_ok, ren_ok, ref_ok, plt_ok))

main()
