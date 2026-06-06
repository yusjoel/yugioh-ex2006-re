# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg9Slots.py -- p5 Seg-9 (0x0801a794..0x0801b850)
#   banlist/shuen scene (28 functions):
#   tick_banlist_scrollbar_and_slot_anim / advance_banlist_password_cursor_slot /
#   retreat_banlist_password_cursor_slot / load_banlist_char_by_cursor_slot /
#   get_banlist_scroll_pixel_offset / get_banlist_password_entry_ptr /
#   render_banlist_text_col_cleared / render_banlist_password_chars_to_buf /
#   advance_banlist_password_char_and_render / retreat_banlist_password_char_and_render /
#   tick_banlist_password_backspace_input / advance_banlist_scroll_pos_step /
#   dispatch_banlist_cursor_action / advance_banlist_scroll_column_and_page /
#   retreat_banlist_scroll_column_and_page / tick_banlist_password_frame /
#   tick_banlist_oam_palette_fade / tick_banlist_card_slot_anim_primary /
#   tick_banlist_card_slot_anim_secondary / trigger_banlist_fade_out_exit /
#   tick_banlist_oam_and_card_slots / tick_banlist_scroll_view_by_state /
#   tick_banlist_scene_frame / dispatch_banlist_scene_handler_frame /
#   dispatch_banlist_pass_input_frame / scale_char_width_by_encoding /
#   read_encoded_char_pair_from_state / init_demo_shuen_display_state
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (all reuse existing inc constants)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- FUN_ -> current name in plate comments (pure ASCII)
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
    # --- name_input.inc: NAME_INPUT_MODE_CLEAR = 0xfffffc3f (5 slots) ---
    (0x0801b01c, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_banlist_password_frame_mode_clear_a',
     'bits[9:6] clear mask for mode field in gBanlistPasswordBuffer+0x660'),
    (0x0801b048, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_banlist_password_frame_mode_clear_b', None),
    (0x0801b060, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_banlist_password_frame_mode_clear_c', None),
    (0x0801b11c, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_banlist_password_frame_mode_clear_d', None),
    (0x0801b170, 0xfffffc3f, 'NAME_INPUT_MODE_CLEAR',
     'tick_banlist_password_frame_mode_clear_e', None),

    # --- name_input.inc: NAME_INPUT_PAGE_STATE_CLEAR = 0xffc03fff (1 slot) ---
    (0x0801b710, 0xffc03fff, 'NAME_INPUT_PAGE_STATE_CLEAR',
     'dispatch_banlist_pass_input_frame_page_state_clear',
     'bits[21:14] clear mask for page_state field in gBanlistPasswordBuffer+0x660'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- gBanlistPasswordBuffer (ewram.inc, 0x02029810) -- 24 slots ---
    (0x0801a7c8, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_scrollbar_and_slot_anim_ptr_gbanlistpasswordbuffer', None),
    (0x0801a7fc, 0x02029810, 'gBanlistPasswordBuffer',
     'advance_banlist_password_cursor_slot_ptr_gbanlistpasswordbuffer', None),
    (0x0801a88c, 0x02029810, 'gBanlistPasswordBuffer',
     'retreat_banlist_password_cursor_slot_ptr_gbanlistpasswordbuffer', None),
    (0x0801a904, 0x02029810, 'gBanlistPasswordBuffer',
     'load_banlist_char_by_cursor_slot_ptr_gbanlistpasswordbuffer', None),
    (0x0801a948, 0x02029810, 'gBanlistPasswordBuffer',
     'get_banlist_scroll_pixel_offset_ptr_gbanlistpasswordbuffer', None),
    (0x0801a97c, 0x02029810, 'gBanlistPasswordBuffer',
     'get_banlist_password_entry_ptr_ptr_gbanlistpasswordbuffer', None),
    (0x0801a9ec, 0x02029810, 'gBanlistPasswordBuffer',
     'render_banlist_text_col_cleared_ptr_gbanlistpasswordbuffer', None),
    (0x0801aa14, 0x02029810, 'gBanlistPasswordBuffer',
     'render_banlist_password_chars_to_buf_ptr_gbanlistpasswordbuffer', None),
    (0x0801aa78, 0x02029810, 'gBanlistPasswordBuffer',
     'advance_banlist_password_char_and_render_ptr_gbanlistpasswordbuffer', None),
    (0x0801aba4, 0x02029810, 'gBanlistPasswordBuffer',
     'retreat_banlist_password_char_and_render_ptr_gbanlistpasswordbuffer', None),
    (0x0801ac0c, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_password_backspace_input_ptr_gbanlistpasswordbuffer', None),
    (0x0801ac58, 0x02029810, 'gBanlistPasswordBuffer',
     'advance_banlist_scroll_pos_step_ptr_gbanlistpasswordbuffer', None),
    (0x0801acf0, 0x02029810, 'gBanlistPasswordBuffer',
     'dispatch_banlist_cursor_action_ptr_gbanlistpasswordbuffer', None),
    (0x0801ae74, 0x02029810, 'gBanlistPasswordBuffer',
     'advance_banlist_scroll_column_and_page_ptr_gbanlistpasswordbuffer', None),
    (0x0801af04, 0x02029810, 'gBanlistPasswordBuffer',
     'retreat_banlist_scroll_column_and_page_ptr_gbanlistpasswordbuffer_a', None),
    (0x0801afac, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_password_frame_ptr_gbanlistpasswordbuffer', None),
    (0x0801b194, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_oam_palette_fade_ptr_gbanlistpasswordbuffer', None),
    (0x0801b1e0, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_card_slot_anim_primary_ptr_gbanlistpasswordbuffer', None),
    (0x0801b25c, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_card_slot_anim_secondary_ptr_gbanlistpasswordbuffer', None),
    (0x0801b280, 0x02029810, 'gBanlistPasswordBuffer',
     'trigger_banlist_fade_out_exit_ptr_gbanlistpasswordbuffer', None),
    (0x0801b354, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_oam_and_card_slots_ptr_gbanlistpasswordbuffer', None),
    (0x0801b3b8, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_scroll_view_by_state_ptr_gbanlistpasswordbuffer', None),
    (0x0801b5f0, 0x02029810, 'gBanlistPasswordBuffer',
     'tick_banlist_scene_frame_ptr_gbanlistpasswordbuffer', None),
    (0x0801b70c, 0x02029810, 'gBanlistPasswordBuffer',
     'dispatch_banlist_pass_input_frame_ptr_gbanlistpasswordbuffer', None),

    # --- gPrng (iwram.inc, 0x03000040) -- 5 slots ---
    (0x0801acf4, 0x03000040, 'gPrng',
     'dispatch_banlist_cursor_action_ptr_gprng', None),
    (0x0801afb0, 0x03000040, 'gPrng',
     'tick_banlist_password_frame_ptr_gprng', None),
    (0x0801b67c, 0x03000040, 'gPrng',
     'dispatch_banlist_scene_handler_frame_ptr_gprng', None),
    (0x0801b708, 0x03000040, 'gPrng',
     'dispatch_banlist_pass_input_frame_ptr_gprng', None),
    (0x0801b5c8, 0x03000040, 'gPrng',
     'tick_banlist_scroll_view_by_state_ptr_gprng', None),

    # --- gTextEncodingOverride (ewram.inc, 0x0202348c) -- 2 slots ---
    (0x0801b69c, 0x0202348c, 'gTextEncodingOverride',
     'dispatch_banlist_scene_handler_frame_ptr_text_encoding_override', None),
    (0x0801b778, 0x0202348c, 'gTextEncodingOverride',
     'dispatch_banlist_pass_input_frame_ptr_text_encoding_override', None),

    # --- gDemoState (ewram.inc, 0x02029ec0) -- 1 slot ---
    (0x0801b83c, 0x02029ec0, 'gDemoState',
     'init_demo_shuen_display_state_ptr_gdemostate', None),

    # --- banlist_char_candidate_str (carve label, 0x09e3bcb1) -- 1 slot ---
    (0x0801a908, 0x09e3bcb1, 'banlist_char_candidate_str',
     'load_banlist_char_by_cursor_slot_ptr_banlist_char_candidate_str', None),

    # --- banlist_pass_alt_char (carve label, 0x09e3c040) -- 1 slot ---
    (0x0801a918, 0x09e3c040, 'banlist_pass_alt_char',
     'load_banlist_char_by_cursor_slot_ptr_banlist_pass_alt_char', None),

    # --- banlist_pass_ext_char_group (new carve, 0x09e3be3c) -- 1 slot ---
    (0x0801abb0, 0x09e3be3c, 'banlist_pass_ext_char_group',
     'retreat_banlist_password_char_and_render_ptr_ext_char_group', None),

    # --- banlist_handler_table (new carve, 0x09e58994) -- 2 slots ---
    (0x0801b678, 0x09e58994, 'banlist_handler_table',
     'dispatch_banlist_scene_handler_frame_ptr_handler_table', None),
    (0x0801b704, 0x09e58994, 'banlist_handler_table',
     'dispatch_banlist_pass_input_frame_ptr_handler_table', None),

    # --- banlist_scroll_view_anim_params (new carve, 0x09e3c6ab) -- 1 slot ---
    (0x0801b3c4, 0x09e3c6ab, 'banlist_scroll_view_anim_params',
     'tick_banlist_scroll_view_by_state_ptr_anim_params', None),

    # --- game_str_pointer_table (existing carve label, 0x08000f40) -- 1 slot ---
    (0x0801b42c, 0x08000f40, 'game_str_pointer_table',
     'tick_banlist_scroll_view_by_state_ptr_game_str_pointer_table', None),

    # --- game_str_ja (existing label) -- 1 slot ---
    (0x0801b430, 0x09db9c10, 'game_str_ja',
     'tick_banlist_scroll_view_by_state_ptr_game_str_ja', None),

    # --- EWRAM_BASE (gba_mem.inc, 0x02000000) -- 8 slots ---
    (0x0801a800, 0x02000000, 'EWRAM_BASE',
     'advance_banlist_password_cursor_slot_ewram_base', None),
    (0x0801a890, 0x02000000, 'EWRAM_BASE',
     'retreat_banlist_password_cursor_slot_ewram_base', None),
    (0x0801a910, 0x02000000, 'EWRAM_BASE',
     'load_banlist_char_by_cursor_slot_ewram_base', None),
    (0x0801b3bc, 0x02000000, 'EWRAM_BASE',
     'tick_banlist_scroll_view_by_state_ewram_base', None),
    (0x0801b52c, 0x02000000, 'EWRAM_BASE',
     'tick_banlist_scroll_view_by_state_ewram_base_b', None),
    (0x0801b358, 0x02000000, 'EWRAM_BASE',
     'tick_banlist_oam_and_card_slots_ewram_base', None),
    (0x0801b798, 0x02000000, 'EWRAM_BASE',
     'scale_char_width_by_encoding_ewram_base', None),
    (0x0801b7cc, 0x02000000, 'EWRAM_BASE',
     'read_encoded_char_pair_from_state_ewram_base', None),

    # --- GSETTINGS_OFFSET (name_input.inc, 0x00006c2c) -- 8 slots ---
    (0x0801a804, 0x00006c2c, 'GSETTINGS_OFFSET',
     'advance_banlist_password_cursor_slot_gsettings_offset', None),
    (0x0801a894, 0x00006c2c, 'GSETTINGS_OFFSET',
     'retreat_banlist_password_cursor_slot_gsettings_offset', None),
    (0x0801a914, 0x00006c2c, 'GSETTINGS_OFFSET',
     'load_banlist_char_by_cursor_slot_gsettings_offset', None),
    (0x0801b3c0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'tick_banlist_scroll_view_by_state_gsettings_offset', None),
    (0x0801b530, 0x00006c2c, 'GSETTINGS_OFFSET',
     'tick_banlist_scroll_view_by_state_gsettings_offset_b', None),
    (0x0801b35c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'tick_banlist_oam_and_card_slots_gsettings_offset', None),
    (0x0801b79c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'scale_char_width_by_encoding_gsettings_offset', None),
    (0x0801b7d0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'read_encoded_char_pair_from_state_gsettings_offset', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0801a7cc, 'tick_banlist_scrollbar_and_slot_anim_scrollbar_offset',
     'scrollbar struct offset in gBanlistPasswordBuffer'),
    (0x0801a838, 'advance_banlist_password_cursor_slot_dir_field_offset',
     'direction field byte offset'),
    (0x0801a898, 'retreat_banlist_password_cursor_slot_dir_field_offset',
     'direction field byte offset'),
    (0x0801a90c, 'load_banlist_char_by_cursor_slot_cursor_slot_offset',
     'bits[5:2]=4-bit slot index'),
    (0x0801a94c, 'get_banlist_scroll_pixel_offset_scrollbar_offset',
     'scrollbar struct offset'),
    (0x0801a980, 'get_banlist_password_entry_ptr_cursor_hw_offset',
     'cursor halfword offset'),
    (0x0801a9f0, 'render_banlist_text_col_cleared_font_scale_offset',
     'font height scale byte offset'),
    (0x0801aa18, 'render_banlist_password_chars_to_buf_cursor_hw_offset',
     'cursor halfword'),
    (0x0801aa1c, 'render_banlist_password_chars_to_buf_row_byte_offset',
     'row height byte offset'),
    (0x0801aa74, 'advance_banlist_password_char_and_render_stack_frame_neg',
     'large stack frame -0x5a8 bytes'),
    (0x0801aa7c, 'advance_banlist_password_char_and_render_limit1_offset',
     'current entry count halfword'),
    (0x0801aa80, 'advance_banlist_password_char_and_render_limit2_offset',
     'max entry count halfword'),
    (0x0801aaf8, 'advance_banlist_password_char_and_render_cursor_hw_offset',
     'cursor halfword'),
    (0x0801aafc, 'advance_banlist_password_char_and_render_row_byte_offset',
     'row height byte'),
    (0x0801aba8, 'retreat_banlist_password_char_and_render_cursor_hw_offset',
     'cursor halfword'),
    (0x0801abac, 'retreat_banlist_password_char_and_render_limit_offset',
     'entry count halfword'),
    (0x0801abd8, 'retreat_banlist_password_char_and_render_limit_offset_b',
     'entry count halfword (second ref)'),
    (0x0801ac10, 'tick_banlist_password_backspace_input_limit_offset',
     'entry count halfword'),
    (0x0801ac5c, 'advance_banlist_scroll_pos_step_scroll_halfword_off',
     'cursor halfword'),
    (0x0801ac60, 'advance_banlist_scroll_pos_step_row_byte_off',
     'row height byte'),
    (0x0801ac64, 'advance_banlist_scroll_pos_step_limit_halfword_off',
     'entry count halfword'),
    (0x0801acf8, 'dispatch_banlist_cursor_action_cursor_slot_offset',
     'cursor slot byte (bits[5:2]=slot)'),
    (0x0801acfc, 'dispatch_banlist_cursor_action_jump_table_ptr',
     'ptr to 6-entry jump table at 0x0801ad00'),
    (0x0801ad00, 'dispatch_banlist_cursor_action_jump_table',
     '6-entry handler table (dispatch via mov pc,r0)'),
    (0x0801ae78, 'advance_banlist_scroll_column_and_page_scroll_halfword_off',
     'cursor halfword'),
    (0x0801ae7c, 'advance_banlist_scroll_column_and_page_row_byte_off',
     'row height byte'),
    (0x0801ae80, 'advance_banlist_scroll_column_and_page_limit1_off',
     'entry count'),
    (0x0801ae84, 'advance_banlist_scroll_column_and_page_mask_clear_col',
     'mask ~(0x7f<<2): clear scroll column bits'),
    (0x0801ae88, 'advance_banlist_scroll_column_and_page_limit2_off',
     'max count halfword'),
    (0x0801af08, 'retreat_banlist_scroll_column_and_page_scroll_halfword_off',
     'cursor halfword'),
    (0x0801af0c, 'retreat_banlist_scroll_column_and_page_row_byte_off',
     'row height byte'),
    (0x0801af10, 'retreat_banlist_scroll_column_and_page_mask_clear_col_a',
     'mask ~(0x7f<<2): clear scroll column bits'),
    (0x0801af38, 'retreat_banlist_scroll_column_and_page_mask_clear_col_b',
     'mask ~(0x7f<<2): clear scroll column bits'),
    (0x0801af6c, 'retreat_banlist_scroll_column_and_page_mask_clear_col_c',
     'mask ~(0x7f<<2): clear scroll column bits'),
    (0x0801afb4, 'tick_banlist_password_frame_cursor_slot_offset',
     'cursor slot byte'),
    (0x0801afe8, 'tick_banlist_password_frame_cursor_slot_offset_b',
     'cursor slot byte (second ref)'),
    (0x0801b114, 'tick_banlist_password_frame_limit1_offset',
     'entry count halfword'),
    (0x0801b118, 'tick_banlist_password_frame_limit2_offset',
     'max count halfword'),
    (0x0801b120, 'tick_banlist_password_frame_cursor_slot_offset_c',
     'cursor slot byte (third ref)'),
    (0x0801b174, 'tick_banlist_password_frame_cursor_slot_offset_d',
     'cursor slot byte (fourth ref)'),
    (0x0801b198, 'tick_banlist_oam_palette_fade_oam_palram_plus2',
     'OBJ PALRAM+2 (sprite palette 1 entry 1) = 0x05000202'),
    (0x0801b19c, 'tick_banlist_oam_palette_fade_ref_palette_offset',
     'reference palette offset in gBanlistPasswordBuffer'),
    (0x0801b1e4, 'tick_banlist_card_slot_anim_primary_cursor_slot_offset',
     'cursor slot byte'),
    (0x0801b260, 'tick_banlist_card_slot_anim_secondary_scroll_halfword_off',
     'cursor halfword'),
    (0x0801b360, 'tick_banlist_oam_and_card_slots_sprite_y_offset_a',
     'sprite row Y param byte A'),
    (0x0801b364, 'tick_banlist_oam_and_card_slots_sprite_y_offset_b',
     'sprite row Y param byte B'),
    (0x0801b3c8, 'tick_banlist_scroll_view_by_state_view_state_offset',
     'view_state byte offset bits[7:4]'),
    (0x0801b428, 'tick_banlist_scroll_view_by_state_game_str_id',
     'game string ID 0x103a'),
    (0x0801b448, 'tick_banlist_scroll_view_by_state_state_mode_incr_off_a',
     'view sub-state offset byte'),
    (0x0801b490, 'tick_banlist_scroll_view_by_state_state_mode_incr_off_b',
     'view sub-state offset byte'),
    (0x0801b494, 'tick_banlist_scroll_view_by_state_blend_ctr_offset_a',
     'blend counter byte offset'),
    (0x0801b498, 'tick_banlist_scroll_view_by_state_view_state_offset_b',
     'view_state byte offset'),
    (0x0801b4c4, 'tick_banlist_scroll_view_by_state_blend_ctr_offset_b',
     'blend counter byte offset'),
    (0x0801b534, 'tick_banlist_scroll_view_by_state_state_mode_incr_off_c',
     'view sub-state offset byte'),
    (0x0801b5cc, 'tick_banlist_scroll_view_by_state_prng_rng_mask',
     'gPrng random state mask bits[9:0]+bits[3:0]'),
    (0x0801b5d0, 'tick_banlist_scroll_view_by_state_scene_state_offset_a',
     'scene state byte offset'),
    (0x0801b5d4, 'tick_banlist_scroll_view_by_state_state_mode_incr_off_d',
     'view sub-state offset byte'),
    (0x0801b5f4, 'tick_banlist_scene_frame_scene_state_offset',
     'scene state byte bits[7:6]=sub-mode'),
    (0x0801b680, 'dispatch_banlist_scene_handler_frame_handler_idx_mask',
     'clear bits[13:6] handler index: ~(0xff<<6)'),
    (0x0801b714, 'dispatch_banlist_pass_input_frame_cursor_slot_offset',
     'cursor slot byte'),
    (0x0801b758, 'dispatch_banlist_pass_input_frame_assert_line_6f5',
     'assert line 0x6f5=1781'),
    (0x0801b760, 'dispatch_banlist_pass_input_frame_cursor_slot_offset_b',
     'cursor slot byte (second ref)'),
    (0x0801b764, 'dispatch_banlist_pass_input_frame_cursor_px_offset',
     'cursor pixel position field offset'),
    (0x0801b768, 'dispatch_banlist_pass_input_frame_cursor_pos_base',
     'cursor pixel pos EWRAM base 0x020053f8'),
    (0x0801b840, 'init_demo_shuen_display_state_gdemostate_fill_ctrl',
     'bios_cpu_set: fill 38 words zero for gDemoState'),
    (0x0801b844, 'init_demo_shuen_display_state_bg1cnt_init',
     'BG1CNT init value'),
    (0x0801b848, 'init_demo_shuen_display_state_bg2cnt_init',
     'BG2CNT init value'),
    (0x0801b84c, 'init_demo_shuen_display_state_bg3cnt_init',
     'BG3CNT init value'),
    # advance_banlist_scroll_pos_step mask
    (0x0801aca8, 'advance_banlist_scroll_pos_step_mask_clear_col',
     'mask ~(0x7f<<2): clear scroll column bits'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # C8 fix #1: load_banlist_char_by_cursor_slot plate L15787
    (0x0801a8bc,
     'FUN_0801aa54',
     'advance_banlist_password_char_and_render'),
    # C8 fix #2: dispatch_banlist_cursor_action plate L16343
    (0x0801acac,
     'FUN_0801af70',
     'tick_banlist_password_frame'),
    # C8 fix #3: tick_banlist_oam_palette_fade plate L16883
    (0x0801b178,
     'FUN_0801b1a0',
     'tick_banlist_card_slot_anim_primary'),
    # C8 fix #4: dispatch_banlist_pass_input_frame plate L17599
    (0x0801b6a0,
     'FUN_081089d8',
     'transition_banlist_pass_to_card_list'),
    # C8 fix #5: scale_char_width_by_encoding plate L17732
    (0x0801b77c,
     'FUN_0801a230',
     'render_banlist_title_text_to_bg'),
]

# ---------------------------------------------------------------------------
# CJK PLATE REWRITES (full rewrite for functions with CJK plates)
# format: (func_addr, new_plate_ascii_text)
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # advance_banlist_password_char_and_render (0x0801aa54)
    (0x0801aa54,
     '@ advance_banlist_password_char_and_render: Banlist password input forward commit path.\n'
     '@ Checks current entry count at gBanlistPasswordBuffer+0x66c vs limit at +0x66e;\n'
     '@ returns 0 immediately if at limit. Calls load_banlist_char_by_cursor_slot to fetch\n'
     '@ selected char; if NUL skips. If entry count == limit returns 4 (position=limit).\n'
     '@ Otherwise: increments count (+0x66c), copies char via copy_str_unbounded +\n'
     '@ append_text_to_buf_charlen, writes to entry ptr, calls render_banlist_text_col_cleared\n'
     '@ then advance_banlist_scroll_column_and_page. Returns page-scroll status (0/1/2/3/4).\n'
     '@ Caller: tick_banlist_password_frame (0x0801af70) via dispatch_banlist_cursor_action.\n'
     '@ Stack frame: 0x5a8 bytes (large local char buffer).'),

    # retreat_banlist_password_char_and_render (0x0801ab00)
    (0x0801ab00,
     '@ retreat_banlist_password_char_and_render: Banlist password input backspace path.\n'
     '@ Reads cursor col and row from gBanlistPasswordBuffer+0x66a/66b; if position<=0 and\n'
     '@ scroll_pixel_offset<=0 returns 0. Computes col=pos mod 15, row=pos div 15; calls\n'
     '@ get_banlist_password_entry_ptr; if col<=14 and row<=3 calls render_banlist_text_col_cleared.\n'
     '@ Normal backspace: copies entry +2 forward (shift left), clears trailing byte,\n'
     '@ calls retreat_banlist_scroll_column_and_page, decrements count -1.\n'
     '@ Page backspace: advance_text_ptr_by_charlen clears last byte, retreat_banlist_scroll...,\n'
     '@ decrements count. Calls render_banlist_password_chars_to_buf for full redraw.\n'
     '@ Returns 0=cannot retreat, non-zero=success.'),

    # tick_banlist_password_backspace_input (0x0801abec)
    (0x0801abec,
     '@ tick_banlist_password_backspace_input: Per-frame handler for banlist backspace key.\n'
     '@ Reads gBanlistPasswordBuffer+0x66c (entry count); if 0 calls sync_state_and_init_sprite(2)\n'
     '@ and returns. Otherwise calls retreat_banlist_password_char_and_render; if status==3\n'
     '@ (page-boundary) calls tick_banlist_scroll_input_handler(1) for scroll. Other non-zero\n'
     '@ status: sync_state_and_init_sprite(1). Called by tick_banlist_password_frame.'),

    # tick_banlist_oam_and_card_slots (0x0801b284)
    (0x0801b284,
     '@ tick_banlist_oam_and_card_slots: Banlist scene per-frame OAM and card slot driver.\n'
     '@ Called by tick_banlist_scene_frame when bits[7:6] of gBanlistPasswordBuffer+0x662 == 0.\n'
     '@ Calls tick_banlist_password_frame; then 5x call_tick_banlist_card_slot_anim for fixed\n'
     '@ OAM slots; reads gSettings encoding flag to compute y-offset bias; 2x\n'
     '@ call_setup_banlist_sprite_oam_row; calls tick_banlist_card_slot_anim_primary/secondary +\n'
     '@ tick_banlist_scrollbar_and_slot_anim. Returns void (Pattern B).'),
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

def _apply_plate_fix(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment at func_addr."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

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
    print("=== RefineSeg9Slots (DRY=%s) ===" % DRY)
    print("  Seg-9: 0x0801a794..0x0801b850, 28 fn, banlist/shuen scene")

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

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES (FUN_ substitutions in existing plates)
    print("\n--- D. PLATE_REWRITES: FUN_ fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    # D2. CJK plate full rewrites
    print("\n--- D2. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineSeg9Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d  CJK_PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), len(CJK_PLATE_REWRITES)))

main()
