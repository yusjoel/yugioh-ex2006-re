# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg6bSlots.py -- p5 Seg-6b (0x08017e48..0x08018774)
#   find_name_char_at_idx / render_jp_string_to_bg_row / render_name_input_scroll_row /
#   get/set_name_scroll_step / sync_scrollbar_to_bg_vofs / check_name_char_limit_reached /
#   get_name_input_cursor_tile / name_input_page_load_assets / write_bg3/1_vofs_with_bias /
#   render_obj_slot_cell_anim / build_sprite_oam_row / render_jp_text_to_vram_obj /
#   zero_obj_vram_tiles / tick_name_input_scrollbar_and_anims /
#   advance/retreat_name_input_cursor_slot / render_settings_cursor_cell_anims /
#   read_banlist_char_at_scroll_pos / refresh_selected_char_obj_tile
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (new constants + reuse existing inc)
#   B. REF_SLOTS -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_SUBS -- replace bare address/DAT_ references in plate comments

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value->name) and references it from slot address.
#    Sets USER_DEFINED label on slot with slot_label (MUST differ from eq_name
#    to avoid GAS ldr-vs-equate conflict when the same name is both .equ and label).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- Reuse: oam_attr.inc ---
    # DAT_08018360: OAM_ATTR2_CHARNAME_MASK (build_sprite_oam_row, existing const)
    (0x08018360, 0x000003ff, 'OAM_ATTR2_CHARNAME_MASK',
     'build_sprite_oam_row_attr2_charname_mask', None),
    # DAT_08018364: OAM_ATTR2_CHARNAME_CLEAR
    (0x08018364, 0xfffffc00, 'OAM_ATTR2_CHARNAME_CLEAR',
     'build_sprite_oam_row_attr2_charname_clear', None),
    # DAT_08018368: OAM_HFLIP_VFLIP_PACKED_PATTERN (new in oam_attr.inc)
    (0x08018368, 0x40004000, 'OAM_HFLIP_VFLIP_PACKED_PATTERN',
     'build_sprite_oam_row_hflip_vflip_pattern',
     'bit14 in attr0+attr1 word: hflip+vflip toggle'),
    # DAT_080183c8: OAM_ATTR1_X_MASK
    (0x080183c8, 0x000001ff, 'OAM_ATTR1_X_MASK',
     'build_sprite_oam_row_attr1_x_mask',
     'attr1 bits[8:0] = 9-bit x coordinate'),
    # DAT_080183cc: OAM_ATTR1_X_CLEAR
    (0x080183cc, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',
     'build_sprite_oam_row_attr1_x_clear',
     'clear attr1 bits[8:0] before inserting x-pos'),

    # --- Reuse: gfx_resource.inc ---
    # DAT_0801819c: GFX_ATTR_CLEAR_BITS_13_7 (name_input_page_load_assets)
    (0x0801819c, 0xffffc07f, 'GFX_ATTR_CLEAR_BITS_13_7',
     'name_input_page_load_assets_attr_clear_bits_13_7', None),

    # --- Reuse: gba_mem.inc ---
    # DAT_0801842c: OBJ_TILE_VRAM_BASE (zero_obj_vram_tiles)
    (0x0801842c, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'zero_obj_vram_tiles_obj_tile_vram_base', None),

    # --- New: name_input.inc ---
    # DAT_08017e40: NAME_INPUT_BG0_SCREEN_CLEAR_CTRL (init_banlist_name_input_page_layout)
    (0x08017e40, 0x01000200, 'NAME_INPUT_BG0_SCREEN_CLEAR_CTRL',
     'init_banlist_name_input_page_layout_bg0_clear_ctrl',
     'bios_cpu_fast_set: fill 0x200 halfwords -> BG0 screen VRAM (32x32 tiles)'),
    # DAT_08017e44: NAME_INPUT_CHAR_VRAM_CLEAR_CTRL
    (0x08017e44, 0x01001800, 'NAME_INPUT_CHAR_VRAM_CLEAR_CTRL',
     'init_banlist_name_input_page_layout_char_vram_clear_ctrl',
     'bios_cpu_fast_set: fill 0x1800 halfwords -> char VRAM clear (24576B)'),
    # DAT_08017ef8: NAME_INPUT_BG_ROW_CLEAR_CTRL (render_jp_string_to_bg_row)
    (0x08017ef8, 0x05000160, 'NAME_INPUT_BG_ROW_CLEAR_CTRL',
     'render_jp_string_to_bg_row_bg_row_clear_ctrl',
     'bios_cpu_set: copy 0x160=352 words=1408B -> clear one BG row (44 tiles)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gState=0x02029250 (18 slots, ewram.inc) ---
    (0x08017e7c, 0x02029250, 'gState', 'find_name_char_at_idx_gstate'),
    (0x08017f88, 0x02029250, 'gState', 'render_name_input_scroll_row_gstate'),
    (0x08017f9c, 0x02029250, 'gState', 'get_name_scroll_step_gstate'),
    (0x08017fd4, 0x02029250, 'gState', 'set_name_scroll_step_gstate'),
    (0x08018014, 0x02029250, 'gState', 'sync_scrollbar_to_bg_vofs_gstate'),
    (0x0801807c, 0x02029250, 'gState', 'check_name_char_limit_reached_gstate'),
    (0x08018190, 0x02029250, 'gState', 'name_input_page_load_assets_gstate'),
    (0x080182ac, 0x02029250, 'gState', 'render_obj_slot_cell_anim_gstate'),
    (0x08018488, 0x02029250, 'gState', 'tick_name_input_scrollbar_and_anims_gstate'),
    (0x080184b8, 0x02029250, 'gState', 'advance_name_input_cursor_slot_gstate'),
    (0x08018548, 0x02029250, 'gState', 'retreat_name_input_cursor_slot_gstate'),
    (0x08018658, 0x02029250, 'gState', 'render_settings_cursor_cell_anims_gstate'),
    (0x0801874c, 0x02029250, 'gState', 'read_banlist_char_at_scroll_pos_gstate'),
    # Seg-7 literal pool but processed here per review #6 note
    (0x080187d4, 0x02029250, 'gState', 'refresh_selected_char_obj_tile_gstate'),

    # --- EWRAM_BASE=0x02000000 (10 slots, gba_mem.inc) ---
    (0x08017e80, 0x02000000, 'EWRAM_BASE', 'find_name_char_at_idx_ewram_base'),
    (0x08017efc, 0x02000000, 'EWRAM_BASE', 'render_jp_string_to_bg_row_ewram_base'),
    (0x08018084, 0x02000000, 'EWRAM_BASE', 'check_name_char_limit_reached_ewram_base'),
    (0x08018238, 0x02000000, 'EWRAM_BASE', 'name_input_page_load_assets_ewram_base'),
    (0x080184bc, 0x02000000, 'EWRAM_BASE', 'advance_name_input_cursor_slot_ewram_base'),
    (0x0801854c, 0x02000000, 'EWRAM_BASE', 'retreat_name_input_cursor_slot_ewram_base'),
    (0x0801865c, 0x02000000, 'EWRAM_BASE', 'render_settings_cursor_cell_anims_ewram_base'),
    (0x08018754, 0x02000000, 'EWRAM_BASE', 'read_banlist_char_at_scroll_pos_ewram_base'),

    # --- ROM data address REF slots ---
    # DAT_08017ef8 -> name_o_resource_desc=0x09e3b3d0 (carve F)
    (0x08018194, 0x09e3b3d0, 'name_o_resource_desc', 'name_input_page_load_assets_name_o_resource_desc'),
    # DAT_08018198 -> name_b_01_path=0x09e3b3e0
    (0x08018198, 0x09e3b3e0, 'name_b_01_path', 'name_input_page_load_assets_name_b_01_path'),
    # DAT_080181a0 -> name_b_02_path=0x09e3b3fc
    (0x080181a0, 0x09e3b3fc, 'name_b_02_path', 'name_input_page_load_assets_name_b_02_path'),
    # DAT_080181a4 -> name_b_04_path=0x09e3b418
    (0x080181a4, 0x09e3b418, 'name_b_04_path', 'name_input_page_load_assets_name_b_04_path'),
    # DAT_08018228 -> name_o_palette_data=0x09ccd290 (carve H)
    (0x08018228, 0x09ccd290, 'name_o_palette_data', 'name_input_page_load_assets_name_o_palette_data'),
    # DAT_08018668 -> cursor_anim_data_a=0x09e3b46f (carve G)
    (0x08018668, 0x09e3b46f, 'cursor_anim_data_a', 'render_settings_cursor_cell_anims_anim_data_a'),
    # DAT_0801866c -> cursor_anim_data_b=0x09e3b47c
    (0x0801866c, 0x09e3b47c, 'cursor_anim_data_b', 'render_settings_cursor_cell_anims_anim_data_b'),
    # DAT_0801875c -> line_break_seq=0x09e3b2b4 (reuse existing label from kana pool)
    (0x0801875c, 0x09e3b2b4, 'line_break_seq', 'read_banlist_char_at_scroll_pos_line_break_seq'),
    # DAT_080187d8 -> name_char_tile_slot_table=0x09e587ec (carve A, Seg-7 pool but done here)
    (0x080187d8, 0x09e587ec, 'name_char_tile_slot_table', 'refresh_selected_char_obj_tile_char_tile_slot_table'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL comment. All text pure ASCII.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # find_name_char_at_idx (0x08017e48)
    (0x08017e84, 'find_name_char_at_idx_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE; bits[2:0]=language_id'),

    # render_jp_string_to_bg_row (0x08017e9c)
    (0x08017f00, 'render_jp_string_to_bg_row_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),

    # get_name_scroll_step (0x08017f8c)
    (0x08017fa0, 'get_name_scroll_step_scroll_field_offset',
     'gState+0x31a = scroll_step field (u8)'),

    # set_name_scroll_step (0x08017fa4)
    (0x08017fe0, 'set_name_scroll_step_scroll_field_offset',
     'gState+0x31a = scroll_step field (u8)'),

    # sync_scrollbar_to_bg_vofs (0x08017fe4)
    (0x08018018, 'sync_scrollbar_to_bg_vofs_scroll_field_offset',
     'gState+0x31a (1st ref: read scroll_step)'),
    (0x08018058, 'sync_scrollbar_to_bg_vofs_scroll_field_offset_b',
     'gState+0x31a (2nd ref: update VOFS from scroll_step)'),

    # check_name_char_limit_reached (0x0801805c)
    (0x08018080, 'check_name_char_limit_reached_char_count_offset',
     'gState+0x31f = current char count byte field'),
    (0x08018088, 'check_name_char_limit_reached_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),

    # name_input_page_load_assets (0x080180ac)
    (0x0801823c, 'name_input_page_load_assets_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),
    (0x0801822c, 'name_input_page_load_assets_bg_palette_dst',
     'BG PALRAM+0x20 = BG palette entry 16 (first non-zero palette slot)'),
    (0x08018234, 'name_input_page_load_assets_obj_palette_dst',
     'OBJ PALRAM+0x20 = OBJ palette entry 16'),
    (0x08018240, 'name_input_page_load_assets_gstate_copy_ctrl',
     'bios_cpu_set ctrl: copy 514 words (2056B) from name_o ptr table -> gState+0x2be'),
    (0x08018244, 'name_input_page_load_assets_gstate_ptr_offset',
     'gState+0x2be = name_o animation ptr table base (receives 514-word block copy)'),

    # zero_obj_vram_tiles (0x08018400): 0x001fffff cpuset wordcount mask (RENAME only, same val diff fn)
    (0x08018430, 'zero_obj_vram_tiles_cpuset_wordcount_mask',
     'cpuset word count mask (bits[20:0]) for bios_cpu_set fill; 0x1fffff = 2097151 max words'),

    # advance_name_input_cursor_slot (0x0801848c)
    (0x080184c0, 'advance_name_input_cursor_slot_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),
    (0x080184f4, 'advance_name_input_cursor_slot_scroll_dir_offset',
     'gState+0x31b = scroll direction marker field (advance writes dir=1)'),

    # retreat_name_input_cursor_slot (0x080184f8)
    (0x08018550, 'retreat_name_input_cursor_slot_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),
    (0x08018554, 'retreat_name_input_cursor_slot_scroll_dir_offset',
     'gState+0x31b = scroll direction marker field (retreat writes dir=-1)'),

    # render_settings_cursor_cell_anims (0x08018558)
    (0x08018660, 'render_settings_cursor_cell_anims_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),
    (0x08018664, 'render_settings_cursor_cell_anims_speed_field_offset',
     'gState+0x31b = speed/position correction byte for cursor animation'),

    # read_banlist_char_at_scroll_pos (0x080186f0)
    (0x08018750, 'read_banlist_char_at_scroll_pos_scroll_col_offset',
     'gState+0x315 = scroll column index field (same as encode_str_table scroll_col)'),
    (0x08018758, 'read_banlist_char_at_scroll_pos_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE'),

    # refresh_selected_char_obj_tile (DAT_080187dc, Seg-7 pool processed here)
    (0x080187dc, 'refresh_selected_char_obj_tile_name_buf_offset',
     'gState+0x2c2 = name input byte buffer base (current char index reads from here)'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Replace bare address literals or DAT_ references in plate comments.
#    All text must remain pure ASCII.
#
# CJK plates rewritten as pure ASCII:
#   init_banlist_name_input_page_layout (0x08017d64)
#   refresh_selected_char_obj_tile (0x08018774)
#   read_banlist_char_at_scroll_pos (0x080186f0)
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # read_banlist_char_at_scroll_pos (0x080186f0): bare 0x09e3b2b4 -> line_break_seq
    (0x080186f0, '0x09e3b2b4', 'line_break_seq'),

    # name_input_page_load_assets (0x080180ac): bare palette addr -> symbolic
    (0x080180ac, '0x09ccd290', 'name_o_palette_data'),
    (0x080180ac, '0x09e3b3d0', 'name_o_resource_desc'),
]

# CJK plate rewrites (full replace): these functions have CJK text in plate; rewrite to ASCII
# Format: (func_addr, new_plate_text_ascii)
PLATE_REWRITES = [
    (0x08017d64,
     "init_banlist_name_input_page_layout(u32 page_layout_type) @ 0x08017d64\n"
     "Args: r0 = page_layout_type (0=banlist, 1=name_input)\n"
     "Clears BG0 screen VRAM (NAME_INPUT_BG0_SCREEN_CLEAR_CTRL=0x01000200, 512 words) via bios_cpu_fast_set.\n"
     "Clears char VRAM (NAME_INPUT_CHAR_VRAM_CLEAR_CTRL=0x01001800, 6144 words) via bios_cpu_fast_set.\n"
     "Reads gSettings(EWRAM_BASE+GSETTINGS_OFFSET) to select language mode.\n"
     "Dispatches to banlist or name-input BG layout init based on page_layout_type.\n"
     "Callers: dispatch_banlist_text_by_key (key=0/1), name_input_page_load_assets."),

    (0x08018774,
     "refresh_selected_char_obj_tile(void) @ 0x08018774\n"
     "Reads gState+0x31c (ping-pong buf index 0 or 1) to select OBJ tile slot.\n"
     "Loads tile index from name_char_tile_slot_table[buf_idx] (0x09e587ec).\n"
     "Writes OBJ tile index to gState+0x2c2 name input buffer entry.\n"
     "Ping-pong: buf0=tile 300 (0x012c), buf1=tile 334 (0x014e)."),

    (0x080186f0,
     "read_banlist_char_at_scroll_pos(void) @ 0x080186f0\n"
     "Reads gState+0x315 scroll column index.\n"
     "Returns SJIS char byte from banlist_jp_str_src at scroll position.\n"
     "In EN mode: substitutes line_break_seq (0x09e3b2b4, SJIS full-width space+NUL).\n"
     "Returns char value in r0."),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_val(slot_int, expected_val):
    """Check that 4-byte data at slot contains expected value. Return True if OK."""
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False
    actual = d.getValue()
    if actual is None:
        return False
    # getValue() returns a Scalar or Address; get long value
    try:
        av = actual.getValue() & 0xffffffff
    except Exception:
        try:
            av = actual.getOffset() & 0xffffffff
        except Exception:
            return False
    ev = expected_val & 0xffffffff
    return av == ev


def main():
    print("=== RefineSeg6bSlots (DRY=%s) ===" % DRY)
    rm  = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    et = currentProgram.getEquateTable()
    nA = nB = nC = nD = 0
    made_labels = set()

    # --- A. EQ_SLOTS ---
    for slot_int, val, eq_name, slot_label, eol in EQ_SLOTS:
        if not _check_val(slot_int, val):
            print("[A FAIL] val mismatch or no 4B data @ 0x%08x (expected 0x%08x)" % (slot_int, val))
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%08x label=%s" % (slot_int, eq_name, val, slot_label))
            nA += 1; continue
        # Create equate and reference
        try:
            eq = et.getEquate(eq_name)
            if eq is None:
                eq = et.createEquate(eq_name, val & 0xffffffff if val >= 0 else val)
            eq.addReference(_addr(slot_int), 0)
        except Exception as e:
            print("[A WARN] equate error @ 0x%08x: %s" % (slot_int, e))
        # Set slot label (DISTINCT from eq_name to avoid GAS ldr/equate conflict)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu: cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[A ok] 0x%08x label=%s equate=%s" % (slot_int, slot_label, eq_name)); nA += 1

    # --- B. REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made_labels:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made_labels.add(tgt_int)
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
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu: cu.setComment(CodeUnit.EOL_COMMENT, eol)
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

    # --- D2. PLATE_REWRITES (CJK -> ASCII full rewrite) ---
    for func_int, new_plate in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D2 FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        if DRY:
            print("[D2 dry] 0x%08x plate rewrite (%d chars)" % (func_int, len(new_plate)))
            nD += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D2 ok] 0x%08x plate rewrite" % func_int); nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))


main()
