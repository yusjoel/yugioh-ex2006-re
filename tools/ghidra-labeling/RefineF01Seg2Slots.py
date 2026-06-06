# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg2Slots.py -- p5 file 01 Seg-2 (0x0801d448..0x0801d998)
#   card_info page text rendering (8 functions):
#   card_info_page_enter_with_card_id / card_info_page_init_bg0 /
#   render_card_name_to_line_buf / draw_card_name_label_to_vram /
#   render_atk_def_digits_to_buf / draw_atk_def_label_to_vram /
#   render_card_level_text_to_buf / draw_card_level_label_to_vram
#
# Sections:
#   A. EQ_SLOTS   -- 13 slots (5 reuse + 8 new card_info.inc)
#   B. REF_SLOTS  -- 14 slots (gCardInfoPageState x3 + carve labels x6 + reuse x5)
#   C. CJK_PLATE_REWRITES -- 8 functions CJK->ASCII
#
# REVIEW FIXES APPLIED:
#   #1 (C4): CARD_INFO_NAME_OAM_TILE_BASE -> CARD_INFO_NAME_BG_TILE_VRAM (0x06001840 is BG VRAM)
#   #2 (C4): CARD_INFO_STAT_OBJ_TILE_BASE -> CARD_INFO_STAT_BG_TILE_VRAM (0x06001c00 is BG VRAM)
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
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- gba_mem.inc reuse: BG_CHAR_VRAM_CB2 = 0x06004000 (1 slot) ---
    (0x0801d4e8, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'card_info_page_init_bg0_vram_char_base',
     'BG charblock 2 base: 0x06004000 (GBA_VRAM_BASE + 0x4000)'),

    # --- gba_mem.inc reuse: OBJ_PALRAM_BASE = 0x05000200 (1 slot) ---
    (0x0801d508, 0x05000200, 'OBJ_PALRAM_BASE',
     'card_info_page_init_bg0_obj_palram_base',
     'OBJ palette RAM base: 0x05000200'),

    # --- ewram.inc reuse: gFontJpCtx = 0x02006ed0 (1 slot) ---
    (0x0801d5a8, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_line_buf_font_jp_ctx',
     'JP font render context struct base'),

    # --- gba_mem.inc reuse: EWRAM_BASE = 0x02000000 (1 slot) ---
    (0x0801d5ac, 0x02000000, 'EWRAM_BASE',
     'render_card_name_to_line_buf_ewram_base',
     'EWRAM base: used with GSETTINGS_OFFSET to reach gSettings'),

    # --- name_input.inc reuse: GSETTINGS_OFFSET = 0x00006c2c (1 slot) ---
    (0x0801d5b0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_name_to_line_buf_gsettings_off',
     'gSettings byte offset from EWRAM_BASE (0x6c2c)'),

    # --- card_info.inc NEW: CARD_INFO_BG1CNT_INIT = 0x00004104 (1 slot) ---
    (0x0801d4f4, 0x00004104, 'CARD_INFO_BG1CNT_INIT',
     'card_info_page_init_bg0_bg1cnt',
     'BG1CNT init: pri=0 charbase=1 16col scrbase=0x10 32x32'),

    # --- card_info.inc NEW: CARD_INFO_BG2CNT_INIT = 0x00000407 (1 slot) ---
    (0x0801d4f8, 0x00000407, 'CARD_INFO_BG2CNT_INIT',
     'card_info_page_init_bg0_bg2cnt',
     'BG2CNT init: pri=3 charbase=1 16col scrbase=0 32x32'),

    # --- card_info.inc NEW: CARD_INFO_BG3CNT_INIT = 0x00000305 (1 slot) ---
    (0x0801d4fc, 0x00000305, 'CARD_INFO_BG3CNT_INIT',
     'card_info_page_init_bg0_bg3cnt',
     'BG3CNT init: pri=1 charbase=0 16col scrbase=0 32x32'),

    # --- card_info.inc NEW: CARD_INFO_OBJ_PAL_SLOT = 0x050003e0 (1 slot) ---
    (0x0801d504, 0x050003e0, 'CARD_INFO_OBJ_PAL_SLOT',
     'card_info_page_init_bg0_obj_pal_slot',
     'OBJ palette slot for card info frame (OBJ_PALRAM_BASE + 0x1e0)'),

    # --- card_info.inc NEW: CARD_INFO_NAME_BG_TILE_VRAM = 0x06001840 (1 slot) ---
    # Fix #1: was CARD_INFO_NAME_OAM_TILE_BASE; 0x06001840 < 0x06010000 = BG VRAM not OAM
    (0x0801d704, 0x06001840, 'CARD_INFO_NAME_BG_TILE_VRAM',
     'draw_card_name_label_to_vram_bg_tile_vram',
     'BG screen-map tile-attr write base for card name line (CB0, SB3+0x040)'),

    # --- card_info.inc NEW: CARD_INFO_NAME_SPRITE_VRAM = 0x06008200 (1 slot) ---
    (0x0801d708, 0x06008200, 'CARD_INFO_NAME_SPRITE_VRAM',
     'draw_card_name_label_to_vram_sprite_vram',
     'commit_line_buffer_to_sprite_vram target for card name (BG VRAM CB2+0x200)'),

    # --- card_info.inc NEW: CARD_INFO_STAT_BG_TILE_VRAM = 0x06001c00 (1 slot) ---
    # Fix #2: was CARD_INFO_STAT_OBJ_TILE_BASE; 0x06001c00 < 0x06010000 = BG VRAM not OBJ
    (0x0801d828, 0x06001c00, 'CARD_INFO_STAT_BG_TILE_VRAM',
     'draw_atk_def_label_to_vram_bg_tile_vram',
     'BG screen-map tile-attr write base for ATK/DEF/Level lines (CB0, SB3+0x400)'),

    # --- card_info.inc NEW: CARD_INFO_STAT_SPRITE_VRAM = 0x06008580 (1 slot) ---
    (0x0801d82c, 0x06008580, 'CARD_INFO_STAT_SPRITE_VRAM',
     'draw_atk_def_label_to_vram_sprite_vram',
     'commit_line_buffer_to_sprite_vram target for ATK/DEF/Level (BG VRAM CB2+0x580)'),

    # --- card_info.inc REUSE: CARD_INFO_STAT_BG_TILE_VRAM = 0x06001c00 (draw_card_level_label_to_vram) ---
    (0x0801d94c, 0x06001c00, 'CARD_INFO_STAT_BG_TILE_VRAM',
     'draw_card_level_label_to_vram_bg_tile_vram',
     'BG screen-map tile-attr write base for Level line (CB0, SB3+0x400)'),

    # --- card_info.inc REUSE: CARD_INFO_STAT_SPRITE_VRAM = 0x06008580 (draw_card_level_label_to_vram) ---
    (0x0801d994, 0x06008580, 'CARD_INFO_STAT_SPRITE_VRAM',
     'draw_card_level_label_to_vram_sprite_vram',
     'commit_line_buffer_to_sprite_vram target for Level (BG VRAM CB2+0x580)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gCardInfoPageState = 0x0201afb0 (3 slots) ---
    (0x0801d458, 0x0201afb0, 'gCardInfoPageState',
     'card_info_page_enter_with_card_id_state_ptr',
     'gCardInfoPageState: card info page per-frame state struct base (EWRAM, 20 refs)'),

    (0x0801d4ec, 0x0201afb0, 'gCardInfoPageState',
     'card_info_page_init_bg0_state_ptr', None),

    (0x0801d5b8, 0x0201afb0, 'gCardInfoPageState',
     'render_card_name_to_line_buf_state_ptr', None),

    # --- name_o_palette_data = 0x09ccd290 (1 slot; already carve H label) ---
    (0x0801d500, 0x09ccd290, 'name_o_palette_data',
     'card_info_page_init_bg0_frame_pal',
     'ptr to name_o_palette_data (16 RGB15 colors; carve H in rom.s)'),

    # --- sjis_char_fold_table = 0x09e589c4 (1 slot; carve A in rom.s) ---
    (0x0801d650, 0x09e589c4, 'sjis_char_fold_table',
     'render_card_name_to_line_buf_char_fold',
     'ptr to sjis_char_fold_table: 256B SJIS/ASCII char normalization table'),

    # --- card_label_glyph_buf = 0x0984f59c (2 slots; carve B in rom.s) ---
    (0x0801d7c8, 0x0984f59c, 'card_label_glyph_buf',
     'render_atk_def_digits_to_buf_glyph_buf',
     'ptr to card_label_glyph_buf: label glyph buffer (LEVEL/ATK/DEF JP bitmaps)'),

    (0x0801d89c, 0x0984f59c, 'card_label_glyph_buf',
     'render_card_level_text_to_buf_glyph_buf', None),

    # --- card_digit_glyph_data = 0x0984f54c (3 slots; carve B in rom.s) ---
    (0x0801d7cc, 0x0984f54c, 'card_digit_glyph_data',
     'render_atk_def_digits_to_buf_digit_glyph',
     'ptr to card_digit_glyph_data: 10 decimal digit bitmaps (8B/glyph, 7px wide)'),

    (0x0801d8f8, 0x0984f54c, 'card_digit_glyph_data',
     'render_card_level_text_to_buf_digit_glyph_a', None),

    (0x0801d928, 0x0984f54c, 'card_digit_glyph_data',
     'render_card_level_text_to_buf_digit_glyph_b', None),

    # --- level_signature_table offsets (2 slots; already carve in data/post-banlists-tables.s) ---
    # +2 = rec[0].field_a base (0x09e5f71c + 2 = 0x09e5f71e)
    (0x0801d8a0, 0x09e5f71e, 'level_signature_table_field_a',
     'render_card_level_text_to_buf_lvl_field_a',
     'level_signature_table+2: rec[0].field_a base (stride=20B per record)'),

    # +0xa = rec[0].field_b base (0x09e5f71c + 0xa = 0x09e5f726)
    (0x0801d8fc, 0x09e5f726, 'level_signature_table_field_b',
     'render_card_level_text_to_buf_lvl_field_b',
     'level_signature_table+0xa: rec[0].field_b base (stride=20B per record)'),

]

# ---------------------------------------------------------------------------
# C. CJK_PLATE_REWRITES: (func_addr, new_plate_ascii)
#    Full plate replacement for CJK->ASCII conversion.
#    ALL text must be pure ASCII (no CJK, no non-ASCII characters).
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # card_info_page_enter_with_card_id @ 0x0801d448
    (0x0801d448,
     "p1: called by open_card_info_by_icid; zero-fills gCardInfoPageState (0x30 halfwords=0x60B)."),

    # card_info_page_init_bg0 @ 0x0801d45c
    (0x0801d45c,
     "Initializes BG0-3 control regs, clears VRAM regions, loads card mini-frame tiles and palette to BG/OBJ."),

    # render_card_name_to_line_buf @ 0x0801d510
    (0x0801d510,
     "r0=card_id. Reads card_stats_table type field to detect wide-card (0x16/0x17). "
     "Loads gFontJpCtx from gCardInfoPageState[+8], selects charset (gSettings bits[2:0]) via select_charset_then_load_name, "
     "then iterates SJIS bytes, using sjis_char_fold_table[byte] != byte to detect 2-byte sequences. "
     "Width guard: cumulative width cmp #0x5c stops render. Returns void."),

    # draw_card_name_label_to_vram @ 0x0801d6b4
    (0x0801d6b4,
     "r0=card_id. Calls setup_line_buf_pos_and_font(x=0xe,y=2,base=0x06001c00), "
     "render_card_name_to_line_buf(card_id), commit_line_buffer_to_sprite_vram(0x06008200,0). "
     "Post-commit loop: writes sequential tile-attr halfwords from 0x06001840 across 2 rows x 14 columns "
     "(tile_idx from 0x210, increments). indeg=1; caller card_image_decode_wrapper."),

    # render_atk_def_digits_to_buf @ 0x0801d70c
    (0x0801d70c,
     "r0=atk_val, r1=def_val. Calls blit_glyph_columns_to_buf 4x for ATK label glyphs "
     "(col offsets 0x1a/0x22/0x40/0x48), then loops 4 digits each for ATK/DEF via __umodsi3/__udivsi3 "
     "at col offsets 0x36..0x2e (ATK) and 0x5c..0x54 (DEF). "
     "Glyph buf base=card_label_glyph_buf(0x0984f59c), digit glyph src=card_digit_glyph_data(0x0984f54c, 8B/glyph). "
     "indeg=1; caller draw_atk_def_label_to_vram."),

    # draw_atk_def_label_to_vram @ 0x0801d7d0
    (0x0801d7d0,
     "r0=atk_val, r1=def_val. Calls setup_line_buf_pos_and_font(x=0xe,y=2,base=0x06001c00), "
     "render_atk_def_digits_to_buf(atk,def), commit_line_buffer_to_sprite_vram(0x06008580,0). "
     "Post-commit loop mirrors draw_card_name_label_to_vram pattern. "
     "Symmetric sibling of draw_card_name_label_to_vram. indeg=1; caller card_image_decode_wrapper."),

    # render_card_level_text_to_buf @ 0x0801d830
    (0x0801d830,
     "r0=level_idx (from lookup_level_glyph_index). Blits 4-glyph LEVEL/RANK label (blit_glyph_columns_to_buf x4). "
     "Then reads level_signature_table[r0].field_a and .field_b (stride=20B) for label and rank strings. "
     "Decodes ASCII: 0x3f->glyph_14, 0x58->glyph_15, 0x30..0x39->digit. "
     "Renders each decoded glyph via blit_glyph_columns_to_buf at col offsets 0x36..0x2e and 0x5c..0x54. "
     "Returns void."),

    # draw_card_level_label_to_vram @ 0x0801d92c
    (0x0801d92c,
     "r0=card_id. Calls lookup_level_glyph_index(card_id); returns 0 if -1 (no level: magic/trap). "
     "Otherwise: setup_line_buf_pos_and_font(x=0xe,y=2), render_card_level_text_to_buf(level_idx), "
     "commit_line_buffer_to_sprite_vram(0x06008580,0). "
     "Returns 1 on success, 0 if no level. indeg=1; caller card_image_decode_wrapper."),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
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
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

def _apply_cjk_plate(func_addr, new_plate_text):
    """Full plate rewrite (for CJK->ASCII conversion)."""
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
    print("=== RefineF01Seg2Slots (DRY=%s) ===" % DRY)
    print("  f01 Seg-2: 0x0801d448..0x0801d998, 8 fn, card_info page text rendering")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. CJK plate full rewrites
    print("\n--- C. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineF01Seg2Slots DONE ===")
    print("  EQ=%d  REF=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(CJK_PLATE_REWRITES)))

main()
