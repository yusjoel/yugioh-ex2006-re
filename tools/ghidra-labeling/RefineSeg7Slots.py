# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg7Slots.py -- p5 Seg-7 (0x08018774..0x08019a58)
#   append_banlist_input_char / delete_banlist_name_last_char /
#   dispatch_name_input_key_by_state / tick_name_input_frame /
#   tick_oam_palette_fade_settings / tick_name_input_oam_fade /
#   tick_name_input_cursor_sprite / signal_name_input_exit /
#   tick_name_input_oam_and_scrollbar / tick_name_input_render_by_state /
#   name_input_page_tick / name_input_page_exit / commit_input_name_to_buf /
#   dispatch_name_input_confirm_state / write_name_input_mode_flag /
#   page_state_dispatcher / extract_char_entry_by_lang /
#   init_banlist_pass_input_scene / dispatch_text_render_by_mode_banlist /
#   return_noop_text_variant / invoke_noop_text_variant_zero /
#   init_font_jp_ctx_bg2_char_vram / init_font_jp_ctx_bg_vram_text /
#   setup_font_jp_ctx_obj_vram_row_banlist / fill_bg0_tilemap_pass_input /
#   append_col_padded_text_to_buf / load_game_str_pair_1036_to_pass_buf /
#   load_game_str_1038_to_pass_buf
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (new constants + reuse existing inc)
#   B. REF_SLOTS -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- CJK plate full rewrite to ASCII

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
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- name_input.inc: NAME_INPUT_MODE_CLEAR = 0xfffffc3f (6 slots) ---
    (0x08018a24, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_name_input_frame_mode_clear_a',
     'bits[9:6] clear mask for mode field in gState+0x314 halfword'),
    (0x08018a30, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_name_input_frame_mode_clear_b', None),
    (0x08018a5c, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_name_input_frame_mode_clear_c', None),
    (0x08018a74, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_name_input_frame_mode_clear_d', None),
    (0x08018bbc, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_name_input_frame_mode_clear_e', None),
    (0x08018d34, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_name_input_frame_mode_clear_f', None),

    # --- name_input.inc: NAME_INPUT_STATE_FIELD_CLEAR = 0xfffc3fff (1 slot) ---
    (0x08018bb0, 0xfffc3fff, 'NAME_INPUT_STATE_FIELD_CLEAR',
     'tick_name_input_frame_state_field_clear',
     'bits[17:14] clear mask for gState+0x316 sub-mode field'),

    # --- name_input.inc: NAME_INPUT_PAGE_STATE_CLEAR = 0xffc03fff (2 slots) ---
    (0x080195e4, 0xffc03fff, 'NAME_INPUT_PAGE_STATE_CLEAR',
     'page_state_dispatcher_page_state_clear_a',
     'bits[21:14] clear mask for page_state field at gPrng+0x204'),
    (0x080195f8, 0xffc03fff, 'NAME_INPUT_PAGE_STATE_CLEAR',
     'page_state_dispatcher_page_state_clear_b', None),

    # --- name_input.inc: BANLIST_PASS_BUF_CLEAR_CTRL = 0x0500019e (1 slot) ---
    (0x080196e8, 0x0500019e, 'BANLIST_PASS_BUF_CLEAR_CTRL',
     'init_banlist_pass_input_scene_buf_clear_ctrl',
     'bios_cpu_set fill+32bit 0x19e words=1656B; zeros gBanlistPasswordBuffer'),

    # --- name_input.inc: BANLIST_PASS_BG1CNT_VAL = 0x00001d0d (1 slot) ---
    (0x080196ec, 0x00001d0d, 'BANLIST_PASS_BG1CNT_VAL',
     'init_banlist_pass_input_scene_bg1cnt_val',
     'BG1CNT init val for pass_input scene (scrbase=29, charbase=3, 256col)'),

    # --- name_input.inc: BANLIST_PASS_BG3CNT_VAL = 0x00001f0f (1 slot) ---
    (0x080196f0, 0x00001f0f, 'BANLIST_PASS_BG3CNT_VAL',
     'init_banlist_pass_input_scene_bg3cnt_val',
     'BG3CNT init val for pass_input scene'),

    # --- name_input.inc: BANLIST_NAME_BG1_SCREEN_CLEAR_CTRL = 0x01000020 (1 slot) ---
    (0x08019070, 0x01000020, 'BANLIST_NAME_BG1_SCREEN_CLEAR_CTRL',
     'tick_name_input_render_by_state_bg1_screen_clear_ctrl',
     'bios_cpu_fast_set fill 0x20 halfwords (64B) -> BG1 screen partial clear, case0'),

    # --- name_input.inc: NAME_INPUT_BG0_SCREEN_CLEAR_CTRL = 0x01000200 (1 slot, reuse) ---
    (0x08019074, 0x01000200, 'NAME_INPUT_BG0_SCREEN_CLEAR_CTRL',
     'tick_name_input_render_by_state_bg0_screen_clear_ctrl', None),

    # --- name_input.inc: BANLIST_PASS_BG0_SCREEN_CLEAR_CTRL = 0x01000840 (2 slots) ---
    (0x08019224, 0x01000840, 'BANLIST_PASS_BG0_SCREEN_CLEAR_CTRL',
     'tick_name_input_render_by_state_pass_bg0_clear_ctrl_a',
     'bios_cpu_fast_set fill 0x840 halfwords (4224B=BG0 screen 32x32 tiles), case2'),
    (0x08019374, 0x01000840, 'BANLIST_PASS_BG0_SCREEN_CLEAR_CTRL',
     'tick_name_input_render_by_state_pass_bg0_clear_ctrl_b', None),

    # --- name_input.inc: BANLIST_PASS_BG1_SCREEN_PARTIAL_CTRL = 0x01000040 (1 slot) ---
    (0x08019378, 0x01000040, 'BANLIST_PASS_BG1_SCREEN_PARTIAL_CTRL',
     'tick_name_input_render_by_state_pass_bg1_partial_ctrl',
     'bios_cpu_fast_set fill 0x40 halfwords (128B) -> BG1 screen row partial, case5'),

    # --- gba_mem.inc: BG_VRAM_TEXT_BASE = 0x06000020 (3 slots) ---
    (0x08019220, 0x06000020, 'BG_VRAM_TEXT_BASE',
     'tick_name_input_render_by_state_bg_vram_text_base_a',
     'GBA_VRAM_BASE+0x20: BG text VRAM base (tile slot 1), case2'),
    (0x08019370, 0x06000020, 'BG_VRAM_TEXT_BASE',
     'tick_name_input_render_by_state_bg_vram_text_base_b',
     'GBA_VRAM_BASE+0x20: BG text VRAM base, case5'),
    (0x08019858, 0x06000020, 'BG_VRAM_TEXT_BASE',
     'init_font_jp_ctx_bg_vram_text_bg_vram_text_base',
     'GBA_VRAM_BASE+0x20: BG text VRAM base for gFontJpCtx bg_vram field'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gState=0x02029250 (14 slots, ewram.inc) ---
    (0x080187fc, 0x02029250, 'gState', 'append_banlist_input_char_ptr_gstate'),
    (0x08018850, 0x02029250, 'gState', 'delete_banlist_name_last_char_ptr_gstate'),
    (0x080188c4, 0x02029250, 'gState', 'dispatch_name_input_key_by_state_ptr_gstate'),
    (0x0801898c, 0x02029250, 'gState', 'tick_name_input_frame_ptr_gstate'),
    (0x08018d54, 0x02029250, 'gState', 'tick_oam_palette_fade_settings_ptr_gstate'),
    (0x08018db0, 0x02029250, 'gState', 'tick_name_input_oam_fade_ptr_gstate'),
    (0x08018e1c, 0x02029250, 'gState', 'tick_name_input_cursor_sprite_ptr_gstate'),
    (0x08018e4c, 0x02029250, 'gState', 'signal_name_input_exit_ptr_gstate'),
    (0x08018f68, 0x02029250, 'gState', 'tick_name_input_oam_and_scrollbar_ptr_gstate'),
    (0x08018fa4, 0x02029250, 'gState', 'tick_name_input_render_by_state_ptr_gstate'),
    (0x080194ac, 0x02029250, 'gState', 'name_input_page_tick_ptr_gstate'),
    (0x08019500, 0x02029250, 'gState', 'name_input_page_exit_ptr_gstate'),
    (0x08019534, 0x02029250, 'gState', 'commit_input_name_to_buf_ptr_gstate'),
    (0x080195dc, 0x02029250, 'gState', 'page_state_dispatcher_ptr_gstate'),

    # --- EWRAM_BASE=0x02000000 (7 slots, gba_mem.inc) ---
    (0x08018e20, 0x02000000, 'EWRAM_BASE', 'tick_name_input_cursor_sprite_ewram_base'),
    (0x0801922c, 0x02000000, 'EWRAM_BASE', 'tick_name_input_render_by_state_ewram_base_a'),
    (0x08019628, 0x02000000, 'EWRAM_BASE', 'extract_char_entry_by_lang_ewram_base'),
    (0x080199ec, 0x02000000, 'EWRAM_BASE', 'load_game_str_pair_1036_to_pass_buf_ewram_base'),
    (0x08019a4c, 0x02000000, 'EWRAM_BASE', 'load_game_str_1038_to_pass_buf_ewram_base'),
    (0x080198cc, 0x02000000, 'EWRAM_BASE', 'setup_font_jp_ctx_obj_vram_row_banlist_ewram_base'),

    # --- GSETTINGS_OFFSET=0x6c2c (name_input.inc) ---
    (0x08018e24, 0x00006c2c, 'GSETTINGS_OFFSET', 'tick_name_input_cursor_sprite_gsettings_offset'),
    (0x08019230, 0x00006c2c, 'GSETTINGS_OFFSET', 'tick_name_input_render_by_state_gsettings_offset_a'),
    (0x0801962c, 0x00006c2c, 'GSETTINGS_OFFSET', 'extract_char_entry_by_lang_gsettings_offset'),
    (0x080199f0, 0x00006c2c, 'GSETTINGS_OFFSET', 'load_game_str_pair_1036_to_pass_buf_gsettings_offset'),
    (0x08019a50, 0x00006c2c, 'GSETTINGS_OFFSET', 'load_game_str_1038_to_pass_buf_gsettings_offset'),
    (0x080198d0, 0x00006c2c, 'GSETTINGS_OFFSET', 'setup_font_jp_ctx_obj_vram_row_banlist_gsettings_offset'),

    # --- gFontJpCtx=0x02006ed0 (3 slots, ewram.inc) ---
    (0x08019818, 0x02006ed0, 'gFontJpCtx', 'init_font_jp_ctx_bg2_char_vram_ptr_font_jp_ctx'),
    (0x0801985c, 0x02006ed0, 'gFontJpCtx', 'init_font_jp_ctx_bg_vram_text_ptr_font_jp_ctx'),
    (0x080198c8, 0x02006ed0, 'gFontJpCtx', 'setup_font_jp_ctx_obj_vram_row_banlist_ptr_font_jp_ctx'),

    # --- OBJ_TILE_VRAM_BASE=0x06010000 (1 slot, gba_mem.inc) ---
    (0x080198c4, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'setup_font_jp_ctx_obj_vram_row_banlist_obj_tile_vram_base'),

    # --- name_char_tile_slot_table=0x09e587ec (2 slots, carve A) ---
    (0x08018f70, 0x09e587ec, 'name_char_tile_slot_table',
     'tick_name_input_oam_and_scrollbar_ptr_char_tile_slot_table'),
    (0x08019490, 0x09e587ec, 'name_char_tile_slot_table',
     'tick_name_input_render_by_state_ptr_char_tile_slot_table'),

    # --- trig_table=0x09e399d0 (2 slots, batch-7 carve) ---
    (0x080190d0, 0x09e399d0, 'trig_table',
     'tick_name_input_render_by_state_ptr_trig_table_a'),
    (0x080193bc, 0x09e399d0, 'trig_table',
     'tick_name_input_render_by_state_ptr_trig_table_b'),

    # --- gTextEncodingOverride=0x0202348c (1 slot, ewram.inc) ---
    (0x08019908, 0x0202348c, 'gTextEncodingOverride',
     'fill_bg0_tilemap_pass_input_ptr_text_enc_override'),

    # --- name_input_render_param_4b=0x09e3b4a4 (1 slot, carve K) ---
    (0x080192a4, 0x09e3b4a4, 'name_input_render_param_4b',
     'tick_name_input_render_by_state_ptr_render_param'),

    # --- name_input_default_name=0x09e3b4a8 (1 slot, carve K) ---
    (0x08019550, 0x09e3b4a8, 'name_input_default_name',
     'dispatch_name_input_confirm_state_ptr_default_name'),

    # --- name_char_group_36=0x09e3b0b0 (1 slot, Seg-6a carve, reuse label) ---
    (0x08018880, 0x09e3b0b0, 'name_char_group_36',
     'delete_banlist_name_last_char_ptr_char_group_36'),

    # --- name_input_state_table=0x09e588b8 (already PTR_ label via Seg-6b; ensure label+ref) ---
    # page_state_dispatcher slot PTR_name_input_state_table_080195d4 already has ref
    # banlist_pass_char_group_ptr_table=0x09e588cc for Seg-8; label only here
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL comment. All text pure ASCII.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # --- gPrng pointer slots (10 slots) ---
    (0x080188c8, 'dispatch_name_input_key_by_state_ptr_gprng', None),
    (0x08018990, 'tick_name_input_frame_ptr_gprng_a', None),
    (0x08018b3c, 'tick_name_input_frame_ptr_gprng_b', None),
    (0x08018b00, 'tick_name_input_frame_ptr_gprng_c', None),
    (0x08018c2c, 'tick_name_input_frame_ptr_gprng_d', None),
    (0x08018d28, 'tick_name_input_frame_ptr_gprng_e', None),
    (0x080192ac, 'tick_name_input_render_by_state_ptr_gprng', None),
    (0x080195d8, 'page_state_dispatcher_ptr_gprng', None),
    (0x0801956c, 'write_name_input_mode_flag_ptr_gprng', None),
    (0x080196f4, 'init_banlist_pass_input_scene_ptr_gprng', None),

    # --- gState field offset slots ---
    # append_banlist_input_char
    (0x08018800, 'append_banlist_input_char_char_count_offset',
     'gState+0x31e: current char count byte'),
    (0x08018804, 'append_banlist_input_char_char_limit_offset',
     'gState+0x31f: max char limit byte'),
    (0x08018834, 'append_banlist_input_char_name_buf_offset',
     'gState+0x2c2: name input byte buffer base'),

    # delete_banlist_name_last_char
    (0x08018854, 'delete_banlist_name_last_char_name_buf_offset',
     'gState+0x2c2: name input byte buffer base'),

    # dispatch_name_input_key_by_state
    (0x080188cc, 'dispatch_name_input_key_by_state_key_type_offset',
     'gState+0x315 bits[5:2]: key-type field (0=null 1=confirm 2=del 3=mode_write 4=set_bit6)'),

    # tick_name_input_frame
    (0x08018994, 'tick_name_input_frame_cursor_field_a_offset',
     'gState+0x315: cursor pos/type field (1st ref)'),
    (0x08018bb4, 'tick_name_input_frame_cursor_field_b_offset',
     'gState+0x315: cursor pos/type field (2nd ref)'),
    (0x0801892c, 'tick_name_input_frame_input_mode_flag_offset_a',
     'gState+0x316: input mode flag byte (1st ref)'),
    (0x08018bb8, 'tick_name_input_frame_input_mode_flag_offset_b',
     'gState+0x316: input mode flag byte (2nd ref)'),
    (0x08018b40, 'tick_name_input_frame_sjis_range_lo',
     'SJIS lower boundary 0x815b for JP input char validation'),
    (0x08018b50, 'tick_name_input_frame_sjis_range_hi',
     'SJIS upper boundary 0x8160 for JP input char validation'),
    (0x08018d2c, 'tick_name_input_frame_char_count_offset_f',
     'gState+0x31e: current char count (end-of-lit-pool ref)'),
    (0x08018d30, 'tick_name_input_frame_char_limit_offset_f',
     'gState+0x31f: max char limit (end-of-lit-pool ref)'),
    (0x08018d38, 'tick_name_input_frame_mode_flag_offset_c',
     'gState+0x316: input mode flag byte (3rd ref, lit-pool tail)'),

    # tick_oam_palette_fade_settings
    (0x08018d58, 'tick_oam_palette_fade_settings_palette_src_offset',
     'gState+0x2be: source palette data offset'),
    (0x08018d5c, 'tick_oam_palette_fade_settings_oam_palram_target',
     'OAM palette RAM slot 1 color 1: 0x05000202'),

    # tick_name_input_oam_fade
    (0x08018db4, 'tick_name_input_oam_fade_cursor_field_offset',
     'gState+0x315: cursor pos/type field'),

    # tick_name_input_cursor_sprite
    (0x08018e28, 'tick_name_input_cursor_sprite_char_count_offset',
     'gState+0x31e: current char count byte'),
    (0x08018e2c, 'tick_name_input_cursor_sprite_char_limit_offset',
     'gState+0x31f: max char limit byte'),

    # tick_name_input_oam_and_scrollbar
    (0x08018f6c, 'tick_name_input_oam_and_scrollbar_jp_flag_offset',
     'gState+0x31b: JP mode flag'),
    (0x08018f74, 'tick_name_input_oam_and_scrollbar_col_a_offset',
     'gState+0x321: cursor column field a'),
    (0x08018f78, 'tick_name_input_oam_and_scrollbar_col_b_offset',
     'gState+0x322: cursor column field b'),

    # tick_name_input_render_by_state
    (0x08018fa8, 'tick_name_input_render_by_state_state_field_offset',
     'gState+0x319: render sub-state bits[7:4]'),
    (0x0801907c, 'tick_name_input_render_by_state_scroll_step_offset',
     'gState+0x31d: BG scroll step counter'),
    (0x0801908c, 'tick_name_input_render_by_state_win0v_val',
     'WIN0V: top=0x28 bottom=0x78 name-input window rect'),
    (0x08019090, 'tick_name_input_render_by_state_dispcnt_bg3_disable_mask_a',
     'DISPCNT clear bit13: BG3 off'),
    (0x08019094, 'tick_name_input_render_by_state_lang_cfg_offset_a',
     'gState+0x323: language config byte'),
    (0x080190d4, 'tick_name_input_render_by_state_scroll_step_offset_b',
     'gState+0x31d: BG scroll step counter (2nd ref)'),
    (0x08019228, 'tick_name_input_render_by_state_str_id_a',
     'game_str ID 0x1009'),
    (0x0801923c, 'tick_name_input_render_by_state_str_id_b',
     'game_str ID 0x100a'),
    (0x08019240, 'tick_name_input_render_by_state_str_id_c',
     'game_str ID 0x100b'),
    (0x080192a8, 'tick_name_input_render_by_state_lang_cfg_offset_b',
     'gState+0x323: language config byte (2nd ref)'),
    (0x0801937c, 'tick_name_input_render_by_state_state_field_offset_b',
     'gState+0x319: render sub-state (2nd ref)'),
    (0x080193d8, 'tick_name_input_render_by_state_state_field_offset_c',
     'gState+0x319: render sub-state (3rd ref)'),
    (0x08019480, 'tick_name_input_render_by_state_dispcnt_bg3_disable_mask_b',
     'DISPCNT clear bit13: BG3 off (2nd ref)'),
    (0x08019488, 'tick_name_input_render_by_state_mode_flag_offset',
     'gState+0x316: input mode flag byte'),
    (0x0801948c, 'tick_name_input_render_by_state_state_field_offset_d',
     'gState+0x319: render sub-state (4th ref)'),

    # name_input_page_tick
    (0x080194b0, 'name_input_page_tick_mode_flag_offset',
     'gState+0x316: input mode flag byte'),

    # name_input_page_exit
    (0x08019504, 'name_input_page_exit_name_buf_offset',
     'gState+0x2c2: name input byte buffer base'),
    (0x08019508, 'name_input_page_exit_committed_name_buf',
     'IWRAM committed name destination: gPrng+0x21a = 0x0300025a (1 ref only)'),

    # commit_input_name_to_buf
    (0x08019538, 'commit_input_name_to_buf_name_buf_offset',
     'gState+0x2c2: name input byte buffer base'),
    (0x0801953c, 'commit_input_name_to_buf_char_count_offset',
     'gState+0x31e: current char count byte'),

    # page_state_dispatcher
    (0x080195e0, 'page_state_dispatcher_char_code_offset',
     'gState+0x31f: writes r5 (char code entry) here'),

    # write_name_input_mode_flag
    (0x08019570, 'write_name_input_mode_flag_prng_mode_offset',
     'gPrng+0x23a: name_input mode flag byte'),

    # init_banlist_pass_input_scene
    (0x080196f8, 'init_banlist_pass_input_scene_prng_mode_offset',
     'gPrng+0x23a: name_input mode flag byte (2nd ref)'),
    (0x080196fc, 'init_banlist_pass_input_scene_gstate_total_offset',
     'gState+0x66e: banlist total count field'),

    # load_game_str_pair_1036_to_pass_buf
    (0x080199e4, 'load_game_str_pair_1036_to_pass_buf_str_id_a',
     'game_str ID 0x1036'),
    (0x080199f8, 'load_game_str_pair_1036_to_pass_buf_str_id_b',
     'game_str ID 0x1037'),

    # load_game_str_1038_to_pass_buf
    (0x08019a44, 'load_game_str_1038_to_pass_buf_str_id',
     'game_str ID 0x1038'),

    # carve J: Ghidra label for banlist_pass_char_group_ptr_table (for Seg-8 ref)
    # (handled via REF_SLOTS target label creation; no rename slot needed)
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_entry_addr, new_plate_text_ascii)
#    CJK plate full rewrite to pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    (0x08018e50,
     "tick_name_input_oam_and_scrollbar(void) @ 0x08018e50\n"
     "Reads gState+0x31b (JP mode flag) to select char tile slot table entry.\n"
     "Loads name_char_tile_slot_table[gState+0x31b] (0x09e587ec) -> OBJ tile index.\n"
     "Updates gState+0x321 (col_a) and gState+0x322 (col_b) column cursor fields.\n"
     "Calls scrollbar update and OAM write routines.\n"
     "Called from tick_name_input_frame (main name-input per-frame update)."),

    (0x08018938,
     "tick_name_input_frame(void) @ 0x08018938\n"
     "Main per-frame tick for name-input page. Reads gPrng+0x314 (mode halfword).\n"
     "gState+0x314: mode halfword bits[9:6]=input_mode; NAME_INPUT_MODE_CLEAR=0xfffffc3f.\n"
     "gState+0x315: cursor pos/type field bits[5:2]=key_type.\n"
     "gState+0x316: input mode flag byte; NAME_INPUT_STATE_FIELD_CLEAR=0xfffc3fff.\n"
     "Validates SJIS range [0x815b, 0x8160] for JP mode char input.\n"
     "Dispatches to append/delete/mode-switch handlers based on key type.\n"
     "Callers: name_input_page_tick (0x08019494)."),

    (0x08018f7c,
     "tick_name_input_render_by_state(void) @ 0x08018f7c\n"
     "Render dispatcher for name-input page, 7 cases (gState+0x319 bits[7:4]).\n"
     "case0: BG1 partial clear (BANLIST_NAME_BG1_SCREEN_CLEAR_CTRL=0x01000020, 64B).\n"
     "       BG0 full clear (NAME_INPUT_BG0_SCREEN_CLEAR_CTRL=0x01000200, 2048B).\n"
     "case1/6: trig_table (0x09e399d0) lookup for BG scroll animation (cos/sin).\n"
     "case2: BG0 clear (BANLIST_PASS_BG0_SCREEN_CLEAR_CTRL=0x01000840, 4224B).\n"
     "       BG text VRAM (BG_VRAM_TEXT_BASE=0x06000020). game_str 0x1009/0x100a/0x100b.\n"
     "case3: render_param memcpy 4B from name_input_render_param_4b (0x09e3b4a4).\n"
     "case5: BG0 clear again + BG1 row partial (BANLIST_PASS_BG1_SCREEN_PARTIAL_CTRL=0x01000040).\n"
     "       BG text VRAM (BG_VRAM_TEXT_BASE=0x06000020).\n"
     "WIN0V=0x2878 (top=0x28 bottom=0x78) for name-input window.\n"
     "DISPCNT bit13 (BG3) toggled via 0xffff9fff mask.\n"
     "gState+0x31d: scroll step counter. gState+0x323: language config byte."),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_val(slot_int, expected_val):
    """Check that 4-byte data at slot contains expected value."""
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False
    actual = d.getValue()
    if actual is None:
        return False
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
    print("=== RefineSeg7Slots (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    et = currentProgram.getEquateTable()
    nA = nB = nC = nD = 0
    made_labels = set()
    fails = 0

    # --- A. EQ_SLOTS ---
    for slot_int, val, eq_name, slot_label, eol in EQ_SLOTS:
        if not _check_val(slot_int, val):
            print("[A FAIL] val mismatch or no 4B data @ 0x%08x (expected 0x%08x)" % (slot_int, val))
            fails += 1; continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%08x label=%s" % (slot_int, eq_name, val, slot_label))
            nA += 1; continue
        try:
            eq = et.getEquate(eq_name)
            if eq is None:
                eq = et.createEquate(eq_name, val & 0xffffffff if val >= 0 else val)
            eq.addReference(_addr(slot_int), 0)
        except Exception as e:
            print("[A WARN] equate error @ 0x%08x: %s" % (slot_int, e))
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu: cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[A ok] 0x%08x label=%s equate=%s" % (slot_int, slot_label, eq_name)); nA += 1

    # --- B. REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); fails += 1; continue
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
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); fails += 1; continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label)); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu: cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- D. PLATE_REWRITES (CJK -> ASCII full rewrite) ---
    for func_int, new_plate in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int); fails += 1; continue
        if DRY:
            print("[D dry] 0x%08x plate rewrite (%d chars)" % (func_int, len(new_plate)))
            nD += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[D ok] 0x%08x plate rewrite" % func_int); nD += 1

    # Also set Ghidra USER label on name_input_state_table and banlist_pass_char_group_ptr_table
    # (carve J labels; needed so resolve_word_symbol exports the GAS label name)
    for vaddr, label in [
        (0x09e588b8, 'name_input_state_table'),
        (0x09e588cc, 'banlist_pass_char_group_ptr_table'),
        (0x09e3b4a4, 'name_input_render_param_4b'),
        (0x09e3b4a8, 'name_input_default_name'),
    ]:
        if not DRY:
            createLabel(_addr(vaddr), label, True, SourceType.USER_DEFINED)
            print("[label] 0x%08x -> %s" % (vaddr, label))
        else:
            print("[label dry] 0x%08x -> %s" % (vaddr, label))

    print("[done] A=%d B=%d C=%d D=%d fails=%d (DRY=%s)" % (nA, nB, nC, nD, fails, DRY))


main()
