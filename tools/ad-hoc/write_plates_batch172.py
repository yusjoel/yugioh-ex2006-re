#!/usr/bin/env python3
"""Write plate files for batch #172 (20 functions)."""
import os

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'doc', 'dev', 'eval')

plates = {
    '0801722c': (
        'decode_char_frame_to_vram: Main character-frame decode function in name-input scene. '
        'Takes input buffer ptr (r0), char count (r1), encode mode (r2), VRAM target base (r3). '
        'Completes in ~0x5a0-byte stack frame: '
        '(1) reads 2-byte chars by mode 0/1, calls dispatch_jp_char_handler for conversion, fills internal stack buffer; '
        '(2) calls pack_bytes_to_vram_bits to compress byte sequence into VRAM bitmap format; '
        '(3) calls xor_buf_bytes to XOR-scramble result; '
        '(4) calls validate_complement_checksum -- on fail calls suppress_display_output and returns -1; '
        '(5) runs two-level bit-field decode loop writing char attributes to VRAM target region. '
        'Returns decoded bit-field count on success, -1 on failure.\n\n'
        'Constants:\n'
        '- STACK_FRAME_SIZE = 0x5a0\n'
        '- MODE_IDENTITY = 0\n'
        '- MODE_BYTE_SWAP = 1\n'
        '- BIOS_CPUSET_CTRL = 0x01000168\n'
        '- CHAR_DECODE_LIMIT = 0x86\n'
        '- PACK_COUNT = 0x40'
    ),

    '080178b4': (
        'load_game_str_pair_1004_to_state: Name-input scene init -- loads game strings ID 0x1004 and 0x1005 '
        'into gState+0x8d buffer, calls pad_str_to_char_multiple to align each to 12-char multiple. '
        'Reads game_str_pointer_table and game_str_ja tables. '
        'Called during name_input / banlist BG init flow to pre-fill name display rows.\n\n'
        'Constants:\n'
        '- STR_ID_A = 0x1004\n'
        '- STR_ID_B = 0x1005\n'
        '- PAD_UNIT = 12\n'
        '- STATE_BUF_OFF = 0x8d'
    ),

    '0801794c': (
        'load_game_str_1006_to_state: Name-input scene init -- loads single game string ID 0x1006 '
        'into gState+0x8d buffer, calls pad_str_to_char_multiple to align to 12-char multiple. '
        'Sibling of load_game_str_pair_1004_to_state (0x080178b4); '
        'that function loads IDs 0x1004+0x1005, this one loads only 0x1006. '
        'Both load gState base and string table internally.\n\n'
        'Constants:\n'
        '- STR_ID = 0x1006\n'
        '- PAD_UNIT = 12\n'
        '- STATE_BUF_OFF = 0x8d'
    ),

    '08017a24': (
        'encode_str_table_entry_to_line_buf: Name-input scene -- takes string table entry pointed to by '
        'caller-frame r6, encodes each char via encode_char_to_line_buf into line buffer, '
        'then calls pad_str_to_char_multiple to align to 60 or 12 cols. '
        'No push prologue; r4/r5/r6/r7 are caller-frame registers (inline exit fragment pattern).\n\n'
        'Constants:\n'
        '- PAD_WIDE = 60\n'
        '- PAD_NARROW = 12\n'
        '- STR_TABLE_ENTRY_STRIDE = 8'
    ),

    '08017f04': (
        'render_name_input_scroll_row: Name-input scene scroll-row render. '
        'Takes scroll direction r0; reads current scrollbar state; '
        'if direction==1 calls find_name_char_at_idx to locate target char; '
        'then calls render_jp_string_to_bg_row to render JP string to BG row; '
        'finally calls fill_tilemap_rect_with_palette. '
        'Triggered on user up/down scroll to refresh one BG tile row.\n\n'
        'Constants:\n'
        '- SCROLL_UP = 1\n'
        '- SCROLL_DOWN = 0'
    ),

    '08018434': (
        'tick_name_input_scrollbar_and_anims: Name-input scene per-frame tick. '
        'Three OAM updates: '
        '(1) calls update_scrollbar_thumb_display to refresh scrollbar thumb; '
        '(2) calls render_obj_slot_cell_anim for OBJ slot A cell animation; '
        '(3) calls render_obj_slot_cell_anim for OBJ slot B cell animation. '
        'The two render_obj_slot_cell_anim calls pass different slot params, '
        'typically cursor and selection-box animations.\n\n'
        'Constants:\n'
        '- SCROLLBAR_STRUCT_OFF = 0xc1<<2 = 0x304\n'
        '- LANG_CHECK_OFF = 0xc6<<2 = 0x318\n'
        '- ANIM_SLOT_A_RANGE = 0xe0 = 224\n'
        '- ANIM_SLOT_B_RANGE = 0xe1 = 225\n'
        '- ANIM_SLOT_PARAM = 0x20 = 32'
    ),

    '080187e0': (
        'append_banlist_input_char: Appends one character to the input buffer in the banlist name-input scene. '
        'Checks if current char count (gState+0x31e) has reached the limit (gState+0x31f); '
        'if full, returns 0 (fail). Otherwise calls read_banlist_char_at_scroll_pos to get the char '
        'at scroll position, appends it to the buffer end, calls refresh_selected_char_obj_tile '
        'to refresh the OBJ tile, and returns 1 (success). '
        'Return value preserved via pop {r1}; bx r1 exit (Sub-case E).\n\n'
        'Constants:\n'
        '- CHAR_COUNT_OFF = 0x31e\n'
        '- CHAR_LIMIT_OFF = 0x31f'
    ),

    '08018d60': (
        'tick_name_input_oam_fade: Name-input scene per-frame tick. '
        'Two OAM updates: '
        '(1) calls render_obj_slot_cell_anim to advance an OBJ slot cell-frame animation; '
        '(2) calls tick_oam_palette_fade_settings to advance OAM palette fade. '
        'Sibling of tick_name_input_scrollbar_and_anims (0x08018434); '
        'the two cover scrollbar+dual-anim and single-anim+palette-fade respectively.\n\n'
        'Constants:\n'
        '- LANG_MODE_OFF = 0xc5<<2 = 0x314\n'
        '- LANG_MODE_THRESHOLD = 0xb = 11\n'
        '- CELL_ANIM_SLOT_A = 0xc = 12\n'
        '- CELL_ANIM_SLOT_B = 0xd = 13\n'
        '- CELL_ANIM_PARAM = 0x8 = 8\n'
        '- CURSOR_FIELD_OFF = 0x315'
    ),

    '08018db8': (
        'tick_name_input_cursor_sprite: Name-input scene per-frame tick. '
        'Reads char count field; if at limit (== char_limit) skips tile update. '
        'Otherwise calls get_name_input_cursor_tile to get current cursor tile number, '
        'then calls render_obj_slot_cell_anim to write cursor animation to OBJ slot. '
        'Called each frame by name_input_page_tick to drive cursor blink.\n\n'
        'Constants:\n'
        '- CHAR_COUNT_OFF = 0x31e\n'
        '- CHAR_LIMIT_OFF = 0x31f'
    ),

    '080197d0': (
        'invoke_noop_text_variant_zero: Minimal wrapper -- sets r2=0 then branches to '
        'return_noop_text_variant (0x080197cc). return_noop_text_variant is a no-op text variant stub '
        'in banlist/pass_input region; this function presets r2=0 to select variant=0 path. '
        'indeg=0 leaf, likely an unconnected placeholder wrapper.\n\n'
        'No non-trivial constants (single movs r2,#0 before bl).'
    ),

    '08019964': (
        'load_game_str_pair_1036_to_pass_buf: Banlist password-input scene init -- '
        'loads game strings ID 0x1036 and 0x1037 into gBanlistPasswordBuffer+0x8d, '
        'calls append_col_padded_text_to_buf to align each to 15 cols. '
        'Cross-scene sibling of load_game_str_pair_1004_to_state (0x080178b4); '
        'symmetric structure, differs only in target buffer and string IDs.\n\n'
        'Constants:\n'
        '- STR_ID_A = 0x1036\n'
        '- STR_ID_B = 0x1037\n'
        '- PAD_UNIT = 15\n'
        '- PASS_BUF_OFF = 0x8d'
    ),

    '080199fc': (
        'load_game_str_1038_to_pass_buf: Banlist password-input scene init -- '
        'loads single game string ID 0x1038 into gBanlistPasswordBuffer+0x8d, '
        'calls append_col_padded_text_to_buf to align to 15 cols. '
        'Sibling of load_game_str_pair_1036_to_pass_buf (0x08019964); '
        'that function loads IDs 0x1036+0x1037, this loads only 0x1038. '
        'Symmetric with name-input side load_game_str_1006_to_state (0x0801794c).\n\n'
        'Constants:\n'
        '- STR_ID = 0x1038\n'
        '- PAD_UNIT = 15\n'
        '- PASS_BUF_OFF = 0x8d'
    ),

    '08019a58': (
        'encode_pass_table_entry_to_line_buf: Banlist pass-input scene -- takes password char table entry '
        'pointed to by caller-frame r10, encodes each char via encode_char_to_line_buf into line buffer, '
        'then calls pad_str_to_char_multiple to align to 90 or 15 cols. '
        'Cross-scene sibling of encode_str_table_entry_to_line_buf (0x08017a24); '
        'symmetric structure, only state base and alignment widths differ '
        '(name_input: 60/12, pass_input: 90/15).\n\n'
        'Constants:\n'
        '- PAD_WIDE = 90\n'
        '- PAD_NARROW = 15\n'
        '- PASS_TABLE_ENTRY_STRIDE = 8'
    ),

    '08019b4c': (
        'render_banlist_pass_char_obj_rows_pair: Banlist pass-input scene -- renders two strings '
        '(ID 0x1038 + 0x1039) as OBJ tile rows. Loads each string, measures pixel width, '
        'zeros the corresponding OBJ tile VRAM region, then calls render_banlist_char_obj_row for each. '
        'Called during password-input interface init to generate OBJ display data for two label rows.\n\n'
        'Constants:\n'
        '- STR_ID_A = 0x1038\n'
        '- STR_ID_B = 0x1039'
    ),

    '08019d14': (
        'init_banlist_pass_input_bg0_page: BG0 init for banlist password-input scene. '
        'Steps: (1) get_bg0_screen_vram_addr + bios_cpu_fast_set zeros BG0 tilemap; '
        '(2) get_bg0_char_vram_addr + bios_cpu_fast_set zeros BG0 char VRAM at offset 0x20; '
        '(3) reject_banlist_input_event installs password-input reject event handler; '
        '(4) init_font_jp_ctx_bg_vram_text inits JP font context; '
        '(5) 6-iteration loop calls render_banlist_password_chars_row per row (14 chars/row, step=14); '
        '(6) fill_tilemap_rect_with_palette fills BG0 tilemap 25x11 region at (0,0). '
        'Called as one of the scene init steps when entering the password-input interface.\n\n'
        'Constants:\n'
        '- BIOS_CPUSET_SCREEN = 0x01000200\n'
        '- BIOS_CPUSET_CHAR = 0x01000898\n'
        '- ROW_COUNT = 6\n'
        '- CHARS_PER_ROW = 14\n'
        '- TILEMAP_W = 0x19 = 25\n'
        '- TILEMAP_H = 0xb = 11'
    ),

    '08019e2c': (
        'init_banlist_pass_input_bg2_page: BG2 init for banlist password-input scene. '
        'Steps: (1) get_bg2_screen_vram_addr + bios_cpu_fast_set zeros BG2 tilemap; '
        '(2) computes BG2 char VRAM offset (0xbd<<5=0x17a0*N+0x20), zeros it with bios_cpu_fast_set '
        'fill mode (bit17=1); '
        '(3) writes 0 to gBanlistPasswordBuffer+0x664 (clear scroll flag); '
        '(4) reads gBanlistPasswordBuffer+0x66e to compute initial scrollbar via __divsi3(input+0xe, 0xf); '
        '(5) init_banlist_scrollbar_oam_entry; '
        '(6) write_banlist_bg2_scroll_regs_biased(0) and write_banlist_bg3_vofs_with_bias(0); '
        '(7) fill_tilemap_rect_with_palette(0,0,27,21). '
        'Sibling of init_banlist_pass_input_bg0_page (0x08019d14).\n\n'
        'Constants:\n'
        '- BIOS_CPUSET_SCREEN = 0x01000200\n'
        '- CHAR_VRAM_STRIDE = 0xbd<<5 = 0x17a0 = 6048\n'
        '- FILL_CTRL = 0x80<<0x11 = 0x01000000\n'
        '- PASS_BUF_SCROLL_OFF = 0x664\n'
        '- PASS_BUF_TOTAL_OFF = 0x66e\n'
        '- PAGE_SIZE = 0xf = 15\n'
        '- TILEMAP_W = 0x1b = 27\n'
        '- TILEMAP_H = 0x15 = 21'
    ),

    '08019f24': (
        'init_banlist_pass_chars_grid_row: Banlist pass-input scene -- inits single-row password char '
        'grid display. Takes row index (r1) and password ptr (r0); '
        'calls init_font_jp_ctx_bg2_char_vram to init BG2 font context (col-width 0xc); '
        'then 14 iterations of clear_tile_buf_col_range; '
        'finally calls render_banlist_password_chars_grid to render char grid to that row. '
        'Called per-row during password interface init.\n\n'
        'Constants:\n'
        '- COL_WIDTH = 0xc = 12\n'
        '- ROWS_PER_CALL = 0xe = 14\n'
        '- ITER_COUNT = 0xe = 14'
    ),

    '08019f78': (
        'refresh_banlist_pass_chars_font_rows: Banlist pass-input scene -- refreshes up to 4 rows of '
        'password char font display. First zeros BG2 char VRAM for specified region '
        '(based on row number r6 and stride 0xbd<<5=0x17a0), re-inits BG2 font context; '
        'then loops up to 4 times: for each valid (non-null) password pointer, '
        'computes col offset and calls render_banlist_password_chars_grid. '
        'Called after char append/delete to incrementally refresh display.\n\n'
        'Constants:\n'
        '- MAX_ROWS = 4\n'
        '- CHAR_VRAM_STRIDE = 0xbd<<5 = 0x17a0 = 6048\n'
        '- FILL_CTRL = 0x80<<0x11 = 0x01000000\n'
        '- COL_WIDTH = 0xc = 12'
    ),

    '0801a794': (
        'tick_banlist_scrollbar_and_slot_anim: Banlist pass-input scene per-frame tick. '
        'Three updates: '
        '(1) calls update_scrollbar_thumb_display with gBanlistPasswordBuffer+0x64c to refresh scrollbar thumb; '
        '(2) calls get_scrollbar_range_param to get range, subtracts 1; '
        '(3) calls call_tick_banlist_card_slot_anim(r0=0, r1=2, r2=0xe0, r3=range-1) to advance slot animation. '
        'Cross-scene sibling of tick_name_input_scrollbar_and_anims (0x08018434).\n\n'
        'Constants:\n'
        '- SCROLLBAR_OFFSET = 0x64c\n'
        '- ANIM_R1 = 2\n'
        '- ANIM_R2 = 0xe0 = 224'
    ),

    '0801a950': (
        'get_banlist_password_entry_ptr: Banlist pass-input scene -- computes and returns current password '
        'entry pointer from scroll offset and cursor row/col fields. '
        'Calls get_banlist_scroll_pixel_offset for base; '
        'reads gBanlistPasswordBuffer+0x66a halfword to extract row (bits[8:0] via lsls #0x17; lsrs #0x19) '
        'and col (bits[3:1] via lsrs #0x1); computes row*15 + col offset; '
        'final ptr = gBanlistPasswordBuffer + (scroll_offset + row*15 + col)*2. '
        'Return via Sub-case E (pop {r1}; bx r1).\n\n'
        'Constants:\n'
        '- CURSOR_HW_OFFSET = 0x66a\n'
        '- ENTRY_STRIDE = 15\n'
        '- ENTRY_SIZE = 2'
    ),
}

all_ok = True
for addr, text in plates.items():
    bad = [c for c in text if ord(c) > 0x7f]
    if bad:
        print(f'NON-ASCII in {addr}: {set(bad)}')
        all_ok = False
    else:
        print(f'OK {addr}')

if all_ok:
    print('All plates ASCII-clean')
    for addr, text in plates.items():
        path = os.path.join(BASE, f'{addr}.plate.txt')
        with open(path, 'w', encoding='ascii') as f:
            f.write(text + '\n')
    print(f'Written {len(plates)} plate files to {BASE}')
else:
    print('ABORT: non-ASCII found')
    import sys
    sys.exit(1)
