# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg6Slots.py -- f01 Seg-6 symbolization
#   ROM range: [0x0801f25c, 0x08020fa8)
#   16 named functions + (after disasm) 4 blocks
#   puzzle/lp_record scene step machines
#
#   Sections:
#     A. EQ_SLOTS   -- data-equate (reuse existing constants; no new constants)
#     B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#     C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#     D. PLATE_REWRITES -- CJK plate -> ASCII (run_duel_puzzle_scene_state_machine)
#
#   reviewer creat decisions applied:
#     - Block3 fn: tick_lp_record_scene_step (med-conf)
#     - DAT_08020018=0xffffc03f: RENAME-only, EOL "clear bits[13:6] step index field"
#     - No new global constants
#
#   NOTE: All EOL/plate text is pure ASCII (no CJK - Ghidra Jython mojibake prevention).

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
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    All constants reuse existing .equ definitions -- no new constants created.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: GAME_STR_RAW_ID_MASK = 0xfffe0000 (3 slots) ---
    (0x0801f27c, 0xfffe0000, 'GAME_STR_RAW_ID_MASK',
     'append_game_text_if_raw_raw_id_mask',
     'raw game string ID mask: bits[31:17]!=0 means pointer, ==0 means handle'),
    (0x0801f2f8, 0xfffe0000, 'GAME_STR_RAW_ID_MASK',
     'format_game_text_with_text_arg_raw_id_mask', None),
    (0x0801f358, 0xfffe0000, 'GAME_STR_RAW_ID_MASK',
     'format_game_text_with_int_arg_raw_id_mask', None),

    # --- gba_io.inc: SIOCNT = 0x04000128 (1 slot) ---
    (0x0801f3ac, 0x04000128, 'SIOCNT',
     'check_siocnt_link_ready_siocnt',
     'SIOCNT SIO Control Register (link cable status)'),

    # --- ewram.inc: GPRNG_BANNER_FLAG_OFF = 0x0000023f (1 slot) ---
    (0x0801fff4, 0x0000023f, 'GPRNG_BANNER_FLAG_OFF',
     'run_duel_puzzle_scene_banner_flag_off',
     'gPrng+0x23f banner/transition flags offset'),

    # --- ewram.inc: gDuelFieldState = 0x02023130 (1 slot) ---
    (0x0801fff8, 0x02023130, 'gDuelFieldState',
     'run_duel_puzzle_scene_duel_field_state',
     'gDuelFieldState EWRAM address'),

    # --- gl_blend.inc: GL_CLEAR_BITS_17_10 = 0xfffc03ff (1 slot) ---
    (0x0801fffc, 0xfffc03ff, 'GL_CLEAR_BITS_17_10',
     'run_duel_puzzle_scene_oam_char_clear',
     'OAM char-name field clear mask bits[17:10] = GL_CLEAR_BITS_17_10'),

    # --- gl_blend.inc: GL_CLEAR_BITS_9_2 = 0xfffffc03 (1 slot) ---
    (0x08020010, 0xfffffc03, 'GL_CLEAR_BITS_9_2',
     'run_duel_puzzle_scene_blend_clear_a',
     'blend register clear mask bits[9:2] = GL_CLEAR_BITS_9_2'),

    # --- gba_mem.inc: EWRAM_BASE = 0x02000000 (3 slots) ---
    (0x08020138, 0x02000000, 'EWRAM_BASE',
     'run_duel_puzzle_case4_ewram_base', None),
    (0x0802020c, 0x02000000, 'EWRAM_BASE',
     'run_duel_puzzle_case6_ewram_base', None),
    (0x08020f50, 0x02000000, 'EWRAM_BASE',
     'render_lp_record_set_a_ewram_base', None),

    # --- name_input.inc: GSETTINGS_OFFSET = 0x00006c2c (3 slots) ---
    (0x08020148, 0x00006c2c, 'GSETTINGS_OFFSET',
     'run_duel_puzzle_case4_gsettings_off',
     'gSettings offset from EWRAM_BASE (game settings block)'),
    (0x08020210, 0x00006c2c, 'GSETTINGS_OFFSET',
     'run_duel_puzzle_case6_gsettings_off', None),
    (0x08020f54, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_lp_record_set_a_gsettings_off', None),

    # --- ewram.inc: gDuelCardCtxBase = 0x0201e2a0 (5 slots) ---
    (0x0801fea8, 0x0201e2a0, 'gDuelCardCtxBase',
     'poll_fadein_exit_to_duel_state_duel_card_ctx_base',
     'gDuelCardCtxBase: duel card context array base (reads [+0x224] scene state)'),
    (0x08020008, 0x0201e2a0, 'gDuelCardCtxBase',
     'run_duel_puzzle_scene_duel_card_ctx', None),
    (0x08020134, 0x0201e2a0, 'gDuelCardCtxBase',
     'run_duel_puzzle_case4_duel_card_ctx', None),
    (0x0802019c, 0x0201e2a0, 'gDuelCardCtxBase',
     'run_duel_puzzle_case4_duel_card_ctx_b', None),
    (0x080202d0, 0x0201e2a0, 'gDuelCardCtxBase',
     'run_duel_puzzle_case8_duel_card_ctx', None),
    (0x080202e8, 0x0201e2a0, 'gDuelCardCtxBase',
     'run_duel_puzzle_fadein_duel_card_ctx', None),

    # --- ewram.inc: gDuelSceneBase = 0x02023360 (1 slot) ---
    (0x080202cc, 0x02023360, 'gDuelSceneBase',
     'run_duel_puzzle_case8_duel_scene',
     'gDuelSceneBase: duel scene state base address'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target + DATA ref from slot + renames slot.
#    IMPORTANT: slot_label MUST differ from gas_label to avoid GAS PC-relative
#    label collision (exporter emits .word gas_label; GAS resolves to slot addr
#    if slot also named gas_label).
#
#    NOTE: The 2 ROM-table pointer slots (find_card_index_in_rom_table_*)
#    originally planned as REF_SLOTS are moved to RENAME_SLOTS because:
#    1) Targets at 0x098973f6/0x098972f0 are in far ROM data with no carve label
#    2) createLabel at far ROM data may fail or create unwanted side effects
#    3) The slot renaming (RENAME) already improves readability; the DATA ref
#       to uncarved far ROM data provides no additional safety guarantee.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # No REF_SLOTS for this segment (the 2 originally planned REF slots
    # were demoted to RENAME_SLOTS to avoid label collision issues with
    # far ROM data targets that lack carve labels).
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Pure rename + optional EOL comment (pure ASCII only).
#    Covers: DAT_/DWORD_ slots not handled by EQ or REF above.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # find_card_index_in_rom_table: ROM table pointer slots (RENAME only; targets not carved)
    (0x0801f428, 'find_card_index_in_rom_table_count_slot',
     'ROM card table halfword count ptr (0x098973f6)'),
    (0x0801f42c, 'find_card_index_in_rom_table_data_slot',
     'ROM card table data base ptr (0x098972f0)'),

    # read_prng_entry_flag_clear
    (0x0801f3cc, 'read_prng_entry_flag_clear_entry_offset',
     'raw offset 0x584 into gPrng flag entry table'),

    # tick_duel_puzzle_scene_step
    (0x0801f474, 'tick_duel_puzzle_scene_step_step_idx_off',
     'gPrng+0x202 step index halfword offset'),
    (0x0801f478, 'tick_duel_puzzle_scene_step_table_base',
     'step fn-ptr table base (PTR_DAT_0801f47c)'),

    # run_duel_puzzle_scene_state_machine -- gPrng+0x202/0x203 offsets
    (0x0801fef0, 'run_duel_puzzle_scene_step_idx_off',
     'gPrng+0x202 step index halfword offset'),
    (0x0801fef4, 'run_duel_puzzle_scene_table_base',
     'step fn-ptr table base (switchdataD_0801fef8)'),

    # run_duel_puzzle_scene_state_machine -- case 0 init
    (0x0801ffec, 'run_duel_puzzle_scene_puzzle_init_area',
     '0x02029e90 puzzle display init area (EWRAM)'),

    # run_duel_puzzle_scene_state_machine -- puzzle card id / slots
    (0x08020000, 'run_duel_puzzle_scene_puzzle_card_id',
     '0x7530=30000 puzzle starting card ID'),
    (0x08020004, 'run_duel_puzzle_scene_puzzle_card_slot_off',
     'gDuelFieldState+0x213 puzzle card index field offset'),

    # run_duel_puzzle_scene_state_machine -- scenario table
    (0x0802000c, 'run_duel_puzzle_scene_scenario_table',
     '0x09e59c2c puzzle scenario ROM pointer table'),

    # run_duel_puzzle_scene_state_machine -- step index duplicates
    (0x08020014, 'run_duel_puzzle_scene_step_idx_off_b',
     'gPrng+0x202 step index offset (dup for case 1)'),

    # run_duel_puzzle_scene_state_machine -- step field clear mask (0xffffc03f)
    # reviewer: RENAME-only (raw value), EOL explains semantics; no new constant
    (0x08020018, 'run_duel_puzzle_scene_step_field_clear',
     '0xffffc03f: clear bits[13:6] of halfword at gPrng+0x202 (step index field)'),

    # case 2
    (0x08020040, 'run_duel_puzzle_case2_step_idx_off',
     'gPrng+0x202 step index offset (dup case 2)'),

    # case 3
    (0x08020078, 'run_duel_puzzle_case3_fadein_flag_off',
     'gPrng+0x203 fadein flag offset'),

    # case 4 -- puzzle progress / bonus dp / str offsets
    (0x0802013c, 'run_duel_puzzle_case4_puzzle_progress_off',
     '0x6c3c: gDuelPuzzleProgress offset from EWRAM_BASE (= 0x02006c3c)'),
    (0x08020140, 'run_duel_puzzle_case4_bonus_dp',
     '0x1662=5730: puzzle completion bonus DP'),
    (0x08020150, 'run_duel_puzzle_case4_str_off_jp',
     '0x4b4e: JP str offset into game_str_ja'),
    (0x08020154, 'run_duel_puzzle_case4_str_off_en',
     '0x3f66a: EN str offset'),
    (0x08020160, 'run_duel_puzzle_case4_str_off_de',
     '0x339ce: DE str offset'),
    (0x0802016c, 'run_duel_puzzle_case4_str_off_fr',
     '0x27532: FR str offset'),
    (0x08020178, 'run_duel_puzzle_case4_str_off_it',
     '0x1b2a0: IT str offset'),
    (0x0802018c, 'run_duel_puzzle_case4_str_off_es',
     '0xfc06: ES str offset'),

    # case 5
    (0x080201d4, 'run_duel_puzzle_case5_fadein_flag_off',
     'gPrng+0x203 fadein flag offset (dup case 5)'),

    # case 6 -- lp_record str addresses
    (0x08020214, 'run_duel_puzzle_case6_str_jp_base',
     '0x09dc01d8: lp_record str JP base ROM address'),
    (0x08020218, 'run_duel_puzzle_case6_str_en_off',
     '0x3ab80: lp_record EN str offset'),
    (0x08020220, 'run_duel_puzzle_case6_str_de',
     '0x09def19a: lp_record DE str ROM address'),
    (0x08020228, 'run_duel_puzzle_case6_str_fr',
     '0x09de2d00: lp_record FR str ROM address'),
    (0x08020230, 'run_duel_puzzle_case6_str_it',
     '0x09dd6982: lp_record IT str ROM address'),
    (0x0802025c, 'run_duel_puzzle_case6_str_es',
     '0x09dcafac: lp_record ES str ROM address'),

    # case 6 step field management
    (0x08020264, 'run_duel_puzzle_case6_step_idx_off',
     'gPrng+0x202 step index offset (dup case 6)'),
    (0x08020268, 'run_duel_puzzle_case6_step_clear',
     '0xffffc03f: clear bits[13:6] step index field (dup case 6)'),

    # case 7
    (0x080202a4, 'run_duel_puzzle_case7_step_idx_off',
     'gPrng+0x202 step index offset (dup case 7)'),
    (0x080202a8, 'run_duel_puzzle_case7_step_clear',
     '0xffffc03f: clear bits[13:6] step index field (dup case 7)'),

    # render_lp_record_text_set_a -- str addresses
    (0x08020f58, 'render_lp_record_set_a_str_jp_base',
     '0x09dc2e62: lp str JP base ROM address'),
    (0x08020f5c, 'render_lp_record_set_a_str_en_off',
     '0x3ae88: lp str EN offset'),
    (0x08020f64, 'render_lp_record_set_a_str_de',
     '0x09df2086: lp str DE ROM address'),
    (0x08020f6c, 'render_lp_record_set_a_str_fr',
     '0x09de5d9c: lp str FR ROM address'),
    (0x08020f74, 'render_lp_record_set_a_str_it',
     '0x09dd9a36: lp str IT ROM address'),
    (0x08020f98, 'render_lp_record_set_a_str_es',
     '0x09dcda66: lp str ES ROM address'),

    # render_lp_record_text_set_a -- card ID binary search pivot keys
    (0x08020df0, 'render_lp_record_set_a_cid_1788', 'card ID 0x1788 binary search pivot'),
    (0x08020df4, 'render_lp_record_set_a_cid_146e', 'card ID 0x146e pivot'),
    (0x08020df8, 'render_lp_record_set_a_cid_112e', 'card ID 0x112e pivot'),
    (0x08020dfc, 'render_lp_record_set_a_cid_0fe9', 'card ID 0x0fe9 pivot'),
    (0x08020e0c, 'render_lp_record_set_a_cid_111c', 'card ID 0x111c pivot'),
    (0x08020e24, 'render_lp_record_set_a_cid_1388', 'card ID 0x1388 pivot'),
    (0x08020e2c, 'render_lp_record_set_a_cid_138a', 'card ID 0x138a pivot'),
    (0x08020e4c, 'render_lp_record_set_a_cid_15fa', 'card ID 0x15fa pivot'),
    (0x08020e5c, 'render_lp_record_set_a_cid_15b1', 'card ID 0x15b1 pivot'),
    (0x08020e74, 'render_lp_record_set_a_cid_1643', 'card ID 0x1643 pivot'),
    (0x08020e9c, 'render_lp_record_set_a_cid_1954', 'card ID 0x1954 pivot'),
    (0x08020ea0, 'render_lp_record_set_a_cid_183d', 'card ID 0x183d pivot'),
    (0x08020eb0, 'render_lp_record_set_a_cid_17c9', 'card ID 0x17c9 pivot'),
    (0x08020ec4, 'render_lp_record_set_a_cid_1905', 'card ID 0x1905 pivot'),
    (0x08020ed4, 'render_lp_record_set_a_cid_1936', 'card ID 0x1936 pivot'),
    (0x08020ef0, 'render_lp_record_set_a_cid_19a5', 'card ID 0x19a5 pivot'),
    (0x08020f0c, 'render_lp_record_set_a_cid_19d6', 'card ID 0x19d6 pivot'),
    (0x08020f4c, 'render_lp_record_set_a_cid_19ef', 'card ID 0x19ef pivot'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: Full plate replacement for CJK -> ASCII conversion
#    run_duel_puzzle_scene_state_machine @ 0x0801fec0 (asm line 5582)
# ---------------------------------------------------------------------------
# The existing plate at 0x0801fec0 contains CJK text; replace entirely with ASCII.
CJK_PLATE_REWRITES = [
    (0x0801fec0,
     "@ Entry: gMenuState+0x234 fn-ptr (ROM[0x080e1c88]=0x0801fec1 THUMB+1), called each frame\n"
     "@ by scene dispatcher. Reads gPrng+0x202 halfword bits[13:6] (9-case step index [0..8]):\n"
     "@ case 0: init (zero_duel_scene_display_buffers, fs_load puzzle deck,\n"
     "@          init_duel_puzzle_scene_state, init_duel_field_vram_layout, set LP flags);\n"
     "@ case 1: tick_duel_field_fadeout_step;\n"
     "@ case 2: tick_duel_field_main_frame (main duel frame);\n"
     "@ case 3: tick_duel_field_fadein_step, write gPrng+0x23f flags;\n"
     "@ case 4: render_puzzle_lp_digit_sprites, count_cleared_puzzle_stages,\n"
     "@         accrue_money_with_cap, find_expert_challenge_slot_by_id,\n"
     "@         render_card_name_centered_to_sprite_vram, dispatch_puzzle_display_mode;\n"
     "@ case 5: tick_lp_display_and_blend_step;\n"
     "@ case 6: dispatch_puzzle_display_mode (render card name by encoding mode);\n"
     "@ case 7: render_puzzle_lp_digit_sprites, update step field in gPrng+0x202;\n"
     "@ case 8: tick_lp_display_and_fadein_check, accrue_money_with_cap,\n"
     "@         init_puzzle_wram_then_copy.\n"
     "@ All cases share exit LAB_080202ec (movs r0,#0x80; lsls r0,#1 = 0x100) or\n"
     "@ LAB_080202d4 (movs r0,#0).\n"
     "@ Step table: switchD_0801fee8__switchdataD_0801fef8.\n"
     "@ Constants: gPrng=0x03000040; STEP_IDX_OFF=0x202; MAX_STEP=8;\n"
     "@ STEP_TABLE=0x0801fef8."),
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
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
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
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (
            slot_addr, target_vaddr, gas_label, slot_label))
        return

    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))


def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))


def _apply_cjk_plate(func_addr, new_plate_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] cjk_plate 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] CJK_PLATE 0x%08x: rewrite to ASCII" % func_addr)
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: CJK plate replaced with ASCII" % func_addr)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF01Seg6Slots (DRY=%s) ===" % DRY)
    print("  Seg-6: 0x0801f25c..0x08020fa8, 16 fn, puzzle/lp_record scene")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
    print("  EQ done: %d/%d" % (eq_ok, len(EQ_SLOTS)))

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
    print("  REF done: %d" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. CJK plate rewrites
    print("\n--- D. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineF01Seg6Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(CJK_PLATE_REWRITES)))


main()
