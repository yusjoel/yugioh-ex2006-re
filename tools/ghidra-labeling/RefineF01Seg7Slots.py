# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg7Slots.py -- f01 Seg-7 (0x08020fa8..0x08024868)
#   render_lp_record_text_set_b / tick_scene_step_by_step_table_d /
#   fetch_duel_next_state_overflow_exit / draw_decimal_with_offset /
#   render_centered_text_to_bg_vram / copy_icon_tile_to_vram_row /
#   init_duel_field_icon_and_bg_vram / render_win_count_digits_to_oam /
#   render_opp_wins_display_oam
#
# Sections:
#   A. EQ_SLOTS   -- 69 data-equate slots
#   B. REF_SLOTS  -- 14 USER-label + DATA-ref
#   C. RENAME_SLOTS -- 48 plain rename + optional EOL
#   D. PLATE      -- 1 PLATE rewrite (draw_decimal_with_offset, pure ASCII)

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
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ---- render_lp_record_text_set_b ----
    # DWORD_08021038: EWRAM_BASE reuse
    (0x08021038, 0x02000000, 'EWRAM_BASE',
     'render_lp_record_set_b_ewram_base', None),
    # DWORD_0802103c: GSETTINGS_OFFSET reuse
    (0x0802103c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_lp_record_set_b_gsettings_offset', None),

    # ---- tick_scene_step_by_step_table_d ----
    # DAT_08022e5c: GPRNG_STEP_IDX_OFF new
    (0x08022e5c, 0x00000202, 'GPRNG_STEP_IDX_OFF',
     'tick_scene_step_by_step_table_d_step_idx_off',
     'gPrng+0x202 halfword bits[13:8] = step index [0..20]'),

    # ---- fetch_duel_next_state_overflow_exit ----
    # DAT_08023878: gDuelCardCtxBase reuse (also REF_SLOT; EQ first)
    (0x08023878, 0x0201e2a0, 'gDuelCardCtxBase',
     'fetch_duel_next_state_overflow_exit_duel_card_ctx_base', None),

    # ---- draw_decimal_with_offset ----
    # DAT_080238c8: gFontJpCtx reuse
    (0x080238c8, 0x02006ed0, 'gFontJpCtx',
     'draw_decimal_with_offset_font_jp_ctx', None),
    # DAT_08023988: gFontJpCtx reuse dup
    (0x08023988, 0x02006ed0, 'gFontJpCtx',
     'draw_decimal_with_offset_font_jp_ctx_b', None),
    # DAT_08023990: OBJ_TILE_VRAM_BASE reuse
    (0x08023990, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'draw_decimal_with_offset_obj_tile_vram_base', None),

    # ---- render_centered_text_to_bg_vram ----
    # DAT_08023b0c: gFontJpCtx reuse
    (0x08023b0c, 0x02006ed0, 'gFontJpCtx',
     'render_centered_text_to_bg_vram_font_jp_ctx', None),
    # DAT_08023b10: EWRAM_BASE reuse
    (0x08023b10, 0x02000000, 'EWRAM_BASE',
     'render_centered_text_to_bg_vram_ewram_base', None),
    # DAT_08023b14: GSETTINGS_OFFSET reuse
    (0x08023b14, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_centered_text_to_bg_vram_gsettings_offset', None),
    # DAT_08023b1c: BG_CHAR_VRAM_CB2 reuse
    (0x08023b1c, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'render_centered_text_to_bg_vram_bg_char_vram_cb2', None),
    # DAT_08023b20: CARD_DESC_BG_VRAM_A reuse
    (0x08023b20, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'render_centered_text_to_bg_vram_card_desc_bg_vram_a', None),

    # ---- copy_icon_tile_to_vram_row ----
    # DAT_08023b64: OBJ_PAL_SLOT_1 new
    (0x08023b64, 0x05000220, 'OBJ_PAL_SLOT_1',
     'copy_icon_tile_to_vram_row_obj_pal_slot_1',
     'OBJ_PALRAM_BASE+0x20 = OBJ palette slot 1; copy dest for icon palette'),
    # DAT_08023b68: OBJ_TILE_VRAM_BASE reuse
    (0x08023b68, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'copy_icon_tile_to_vram_row_obj_tile_vram_base', None),

    # ---- init_duel_field_icon_and_bg_vram ----
    # DAT_08023c78: DUEL_FIELD_CTRL_VAL new
    (0x08023c78, 0x00000601, 'DUEL_FIELD_CTRL_VAL',
     'init_duel_field_icon_bg_ctrl_val',
     'written to gPrng+0x174 at duel field init'),
    # DAT_08023c7c: gDuelDispCtx new global (also REF_SLOT)
    (0x08023c7c, 0x0203eeb0, 'gDuelDispCtx',
     'init_duel_field_icon_bg_disp_ctx', None),
    # DAT_08023c80: gVijaState reuse
    (0x08023c80, 0x02029eb0, 'gVijaState',
     'init_duel_field_icon_bg_vija_state', None),
    # DAT_08023c88: DUEL_FIELD_BGCNT1_INIT new
    (0x08023c88, 0x00000105, 'DUEL_FIELD_BGCNT1_INIT',
     'init_duel_field_icon_bg_bgcnt1_init',
     'BG1CNT init (pri=1 charbase=0 scrbase=0 32x32)'),
    # DAT_08023c8c: DUEL_FIELD_BGCNT2_INIT new
    (0x08023c8c, 0x00000206, 'DUEL_FIELD_BGCNT2_INIT',
     'init_duel_field_icon_bg_bgcnt2_init',
     'BG2CNT init (pri=2 charbase=0 scrbase=0)'),
    # DAT_08023c90: DUEL_FIELD_BGCNT3_INIT new
    (0x08023c90, 0x00000307, 'DUEL_FIELD_BGCNT3_INIT',
     'init_duel_field_icon_bg_bgcnt3_init',
     'BG3CNT init (pri=3 charbase=0 scrbase=0)'),
    # DAT_08023c94: BG_CHAR_VRAM_CB2 reuse
    (0x08023c94, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'init_duel_field_icon_bg_char_vram_cb2', None),
    # DAT_08023c98: OBJ_TILE_VRAM_BASE reuse
    (0x08023c98, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'init_duel_field_icon_bg_obj_tile_vram_base', None),
    # DAT_08023c9c: OBJ_PALRAM_BASE reuse
    (0x08023c9c, 0x05000200, 'OBJ_PALRAM_BASE',
     'init_duel_field_icon_bg_obj_palram_base', None),
    # DAT_08023ca4: OBJ_TILE_VRAM_BASE_PAGE2 new
    (0x08023ca4, 0x06010200, 'OBJ_TILE_VRAM_BASE_PAGE2',
     'init_duel_field_icon_bg_obj_tile_page2',
     'OBJ_TILE_VRAM_BASE+0x200; 16 ROM refs; icon tile base page 2'),
    # DAT_08023d44: EWRAM_BASE reuse
    (0x08023d44, 0x02000000, 'EWRAM_BASE',
     'init_duel_field_icon_bg_ewram_base_a', None),
    # DAT_08023d48: GSETTINGS_OFFSET reuse
    (0x08023d48, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_duel_field_icon_bg_gsettings_off_a', None),
    # DAT_08023da4: DUEL_FIELD_TEXT_TILE_POS_A new
    (0x08023da4, 0x00000507, 'DUEL_FIELD_TEXT_TILE_POS_A',
     'init_duel_field_icon_bg_text_tile_pos_a',
     'render_centered_text r0: col=7 row=5; 34 ROM refs'),
    # DAT_08023da8: DUEL_FIELD_TEXT_BG_WIDTH new
    (0x08023da8, 0x00000f09, 'DUEL_FIELD_TEXT_BG_WIDTH',
     'init_duel_field_icon_bg_text_bg_width_a',
     'render_centered_text r3: BG width=0x0f tile_param=0x09; 14 ROM refs'),
    # DAT_08023dac: DUEL_FIELD_TILE_ROW_ARG_A new
    (0x08023dac, 0x00000901, 'DUEL_FIELD_TILE_ROW_ARG_A',
     'init_duel_field_icon_bg_tile_row_arg_a',
     'write_tile_row tile descriptor A; 35 ROM refs'),
    # DAT_08023de0: EWRAM_BASE reuse
    (0x08023de0, 0x02000000, 'EWRAM_BASE',
     'init_duel_field_icon_bg_ewram_base_b', None),
    # DAT_08023de4: GSETTINGS_OFFSET reuse
    (0x08023de4, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_duel_field_icon_bg_gsettings_off_b', None),
    # DAT_08023e48: DUEL_FIELD_TEXT_TILE_POS_B new
    (0x08023e48, 0x000004a7, 'DUEL_FIELD_TEXT_TILE_POS_B',
     'init_duel_field_icon_bg_text_tile_pos_b',
     'render_centered_text r0: col=7 row=4; 5 ROM refs'),
    # DAT_08023e4c: DUEL_FIELD_TEXT_BG_WIDTH reuse
    (0x08023e4c, 0x00000f09, 'DUEL_FIELD_TEXT_BG_WIDTH',
     'init_duel_field_icon_bg_text_bg_width_b', None),
    # DAT_08023e50: EWRAM_BASE reuse
    (0x08023e50, 0x02000000, 'EWRAM_BASE',
     'init_duel_field_icon_bg_ewram_base_c', None),
    # DAT_08023e54: GSETTINGS_OFFSET reuse
    (0x08023e54, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_duel_field_icon_bg_gsettings_off_c', None),
    # DAT_08023ec0: DUEL_FIELD_TEXT_TILE_POS_C new
    (0x08023ec0, 0x00000567, 'DUEL_FIELD_TEXT_TILE_POS_C',
     'init_duel_field_icon_bg_text_tile_pos_c',
     'render_centered_text r0 variant C; 8 ROM refs'),
    # DAT_08023ec4: DUEL_FIELD_TEXT_BG_WIDTH reuse
    (0x08023ec4, 0x00000f09, 'DUEL_FIELD_TEXT_BG_WIDTH',
     'init_duel_field_icon_bg_text_bg_width_c', None),
    # DAT_08023ec8: DUEL_FIELD_TILE_ROW_ARG_B new
    (0x08023ec8, 0x000008a1, 'DUEL_FIELD_TILE_ROW_ARG_B',
     'init_duel_field_icon_bg_tile_row_arg_b',
     'write_tile_row tile descriptor B; 8 ROM refs'),
    # DAT_08023ed0: DUEL_FIELD_TILE_ROW_ARG_C new
    (0x08023ed0, 0x00000961, 'DUEL_FIELD_TILE_ROW_ARG_C',
     'init_duel_field_icon_bg_tile_row_arg_c',
     'write_tile_row tile descriptor C; 5 ROM refs'),
    # DAT_08023fb4: EWRAM_BASE reuse
    (0x08023fb4, 0x02000000, 'EWRAM_BASE',
     'init_duel_field_icon_bg_ewram_base_d', None),
    # DAT_08023fb8: GSETTINGS_OFFSET reuse
    (0x08023fb8, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_duel_field_icon_bg_gsettings_off_d', None),
    # DAT_08023fc0: DUEL_FIELD_TEXT_BG_WIDTH reuse
    (0x08023fc0, 0x00000f09, 'DUEL_FIELD_TEXT_BG_WIDTH',
     'init_duel_field_icon_bg_text_bg_width_d', None),
    # Note: DAT_08023fd0 = 0xffff807f (flags mask clears field-state bits, 7 refs) is RENAME_SLOT below

    # ---- render_win_count_digits_to_oam ----
    # DAT_080240fc: EWRAM_BASE reuse
    (0x080240fc, 0x02000000, 'EWRAM_BASE',
     'render_win_count_digits_ewram_base', None),
    # DAT_08024100: GWINS_BASE_OFFSET new
    (0x08024100, 0x00006e60, 'GWINS_BASE_OFFSET',
     'render_win_count_digits_wins_base_off',
     'gWinsBase-EWRAM_BASE; win count record table offset'),
    # DAT_08024104: GWINS_BASE_OFF_2 new
    (0x08024104, 0x00006e62, 'GWINS_BASE_OFF_2',
     'render_win_count_digits_wins_base_off2',
     'gWinsBase+2-EWRAM_BASE; second win count field'),
    # DAT_08024108: OPP_WIN_DIGIT_TILE_BASE new
    (0x08024108, 0x00000474, 'OPP_WIN_DIGIT_TILE_BASE',
     'render_win_count_digits_digit_tile_base',
     'OAM digit sprite tile base index for opponent win count'),
    # DAT_0802410c: OPP_WIN_SPRITE_OFFSCREEN_XY new
    (0x0802410c, 0x00004040, 'OPP_WIN_SPRITE_OFFSCREEN_XY',
     'render_win_count_digits_offscreen_xy',
     'OAM attr0[y=0x40]|attr1[x=0x40] off-screen placeholder'),
    # DAT_08024110: OPP_WIN_SEPARATOR_TILE_IDX new
    (0x08024110, 0x00000454, 'OPP_WIN_SEPARATOR_TILE_IDX',
     'render_win_count_digits_sep_tile_idx',
     'first fixed separator sprite tile index'),

    # ---- render_opp_wins_display_oam ----
    # DAT_0802420c: GPRNG_STEP_IDX_OFF reuse
    (0x0802420c, 0x00000202, 'GPRNG_STEP_IDX_OFF',
     'render_opp_wins_display_oam_step_idx_off', None),
    # DAT_08024210: GPRNG_FRAME_CTRL_OFF_203 new
    (0x08024210, 0x00000203, 'GPRNG_FRAME_CTRL_OFF_203',
     'render_opp_wins_display_oam_frame_ctrl_off',
     'gPrng+0x203 byte: frame control field 2'),
    # DAT_0802424c: EWRAM_BASE reuse
    (0x0802424c, 0x02000000, 'EWRAM_BASE',
     'render_opp_wins_display_oam_ewram_base_a', None),
    # DAT_08024250: GSETTINGS_OFFSET reuse
    (0x08024250, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_opp_wins_display_oam_gsettings_off_a', None),
    # DAT_080242b4: GSETTINGS_OFFSET reuse
    (0x080242b4, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_opp_wins_display_oam_gsettings_off_b', None),
    # DAT_080242b8: GUNLOCKED_DUELISTS_OFFSET new
    (0x080242b8, 0x00006e5c, 'GUNLOCKED_DUELISTS_OFFSET',
     'render_opp_wins_display_oam_unlocked_off',
     'gUnlockedDuelists-EWRAM_BASE'),
    # DAT_080242c0: DUEL_SCENE_FIELD_OFF_6E48 new
    (0x080242c0, 0x00006e48, 'DUEL_SCENE_FIELD_OFF_6E48',
     'render_opp_wins_display_oam_scene_field_a',
     'EWRAM+0x6e48 = duel scene record field A; 10 ROM refs'),
    # DAT_080242c4: DUEL_SCENE_FIELD_OFF_6E57 new
    (0x080242c4, 0x00006e57, 'DUEL_SCENE_FIELD_OFF_6E57',
     'render_opp_wins_display_oam_scene_field_b',
     'EWRAM+0x6e57 = duel scene record field B; 19 ROM refs'),
    # DAT_08024440: DUEL_FIELD_OAM_COORDS_A new
    (0x08024440, 0x00830070, 'DUEL_FIELD_OAM_COORDS_A',
     'render_opp_wins_display_oam_coords_a',
     'packed OAM coords row=0x83 x=0x70 (card sprite A); 2 ROM refs'),
    # DAT_0802444c: DUEL_FIELD_OAM_COORDS_B new
    (0x0802444c, 0x00210070, 'DUEL_FIELD_OAM_COORDS_B',
     'render_opp_wins_display_oam_coords_b',
     'packed OAM coords row=0x21 x=0x70 (card sprite B); 1 ref'),
    # DAT_08024450: DUEL_FIELD_OAM_TILE_IDX_A new
    (0x08024450, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',
     'render_opp_wins_display_oam_tile_idx_a',
     'OAM tile index 0x814 for duel field card sprite; 28 ROM refs'),
    # DAT_08024454: DUEL_FIELD_OAM_TILE_IDX_B new
    (0x08024454, 0x00000815, 'DUEL_FIELD_OAM_TILE_IDX_B',
     'render_opp_wins_display_oam_tile_idx_b',
     'OAM tile index 0x815; 6 ROM refs'),
    # DAT_08024458: DUEL_FIELD_OAM_TILE_IDX_C new
    (0x08024458, 0x00000816, 'DUEL_FIELD_OAM_TILE_IDX_C',
     'render_opp_wins_display_oam_tile_idx_c',
     'OAM tile index 0x816; 5 ROM refs'),
    # DAT_0802445c: DUEL_SCENE_FLAGS_MASK_0F00 reuse
    (0x0802445c, 0xffff0f00, 'DUEL_SCENE_FLAGS_MASK_0F00',
     'render_opp_wins_display_oam_flags_mask', None),
    # DAT_08024460: EWRAM_BASE reuse
    (0x08024460, 0x02000000, 'EWRAM_BASE',
     'render_opp_wins_display_oam_ewram_base_b', None),
    # DAT_08024464: GUNLOCKED_DUELISTS_OFFSET reuse
    (0x08024464, 0x00006e5c, 'GUNLOCKED_DUELISTS_OFFSET',
     'render_opp_wins_display_oam_unlocked_off_b', None),
    # DAT_08024710: EWRAM_BASE reuse
    (0x08024710, 0x02000000, 'EWRAM_BASE',
     'render_opp_wins_display_oam_ewram_base_c', None),
    # DAT_08024714: GUNLOCKED_DUELISTS_OFFSET reuse
    (0x08024714, 0x00006e5c, 'GUNLOCKED_DUELISTS_OFFSET',
     'render_opp_wins_display_oam_unlocked_off_c', None),
    # DAT_0802485c: GPRNG_STEP_IDX_OFF reuse
    (0x0802485c, 0x00000202, 'GPRNG_STEP_IDX_OFF',
     'render_opp_wins_display_oam_step_idx_off_b', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gDuelSceneBase = 0x02023360 (10 slots)
    (0x08023cbc, 0x02023360, 'gDuelSceneBase',
     'init_duel_field_icon_and_bg_vram_ptr_duel_scene'),
    (0x08023d18, 0x02023360, 'gDuelSceneBase',
     'init_duel_field_icon_and_bg_vram_ptr_duel_scene_b'),
    (0x08024214, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_a'),
    (0x0802443c, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_b'),
    (0x08024520, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_c'),
    (0x08024864, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_d'),
    (0x080242bc, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_e'),
    (0x080245e8, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_f'),
    (0x0802470c, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_g'),
    (0x08024664, 0x02023360, 'gDuelSceneBase',
     'render_opp_wins_display_oam_ptr_duel_scene_h'),
    (0x08023fc8, 0x02023360, 'gDuelSceneBase',
     'init_duel_field_icon_and_bg_vram_ptr_duel_scene_c'),
    # gDuelCardCtxBase = 0x0201e2a0
    (0x08023878, 0x0201e2a0, 'gDuelCardCtxBase',
     'fetch_duel_next_state_overflow_exit_ptr_duel_card_ctx'),
    # gDuelDispCtx = 0x0203eeb0
    (0x08023c7c, 0x0203eeb0, 'gDuelDispCtx',
     'init_duel_field_icon_and_bg_vram_ptr_duel_disp_ctx'),
    # PTR step table self-ref
    (0x08022e60, 0x08022e64, 'PTR_DAT_08022e64',
     'tick_scene_step_by_step_table_d_ptr_step_table'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # -- render_lp_record_text_set_b --
    (0x08020fc8, 'render_lp_record_set_b_cid_16dc',
     '0x16dc card ID pivot for LP record set_b lookup'),
    (0x08020fd8, 'render_lp_record_set_b_cid_16a3',
     '0x16a3 card ID pivot'),
    (0x08020fec, 'render_lp_record_set_b_cid_17ca',
     '0x17ca card ID pivot'),
    (0x08021034, 'render_lp_record_set_b_cid_184e',
     '0x184e card ID pivot'),
    (0x08021040, 'render_lp_record_set_b_str_jp_base',
     '0x09dc2ea8: lp str JP base ROM address (same offset pattern as set_a)'),
    (0x08021044, 'render_lp_record_set_b_str_en_off',
     '0x3ae88: lp str EN offset (same as set_a)'),
    (0x0802104c, 'render_lp_record_set_b_str_de',
     '0x09df20cc: lp str DE ROM address'),
    (0x08021054, 'render_lp_record_set_b_str_fr',
     '0x09de5e00: lp str FR ROM address'),
    (0x0802105c, 'render_lp_record_set_b_str_it',
     '0x09dd9a86: lp str IT ROM address'),
    (0x08021080, 'render_lp_record_set_b_str_es',
     '0x09dcdaac: lp str ES ROM address'),

    # -- init_duel_field_icon_and_bg_vram gfx src ptrs --
    (0x08023ca0, 'init_duel_field_icon_and_bg_vram_gfx_src_a',
     '0x09b97308: tile/pal src A (1 ref)'),
    (0x08023ca8, 'init_duel_field_icon_and_bg_vram_gfx_src_b',
     '0x09b97328: tile/pal src B (1 ref)'),
    (0x08023cac, 'init_duel_field_icon_and_bg_vram_gfx_src_c',
     '0x09b95acc: tile/pal src C (1 ref)'),
    (0x08023cb0, 'init_duel_field_icon_and_bg_vram_gfx_src_d',
     '0x09b953b4: tile/pal src D (7 refs)'),
    (0x08023cb4, 'init_duel_field_icon_and_bg_vram_gfx_src_e',
     '0x09b96514: tile/pal src E (5 refs)'),
    (0x08023cb8, 'init_duel_field_icon_and_bg_vram_gfx_src_f',
     '0x09b9487c: tile/pal src F (1 ref)'),

    # -- init_duel_field_icon_and_bg_vram LP/BG string ptrs --
    (0x08023d4c, 'init_duel_field_icon_and_bg_vram_lp_str_jp_a',
     '0x09dc00e2: LP record JP string base A (2 refs)'),
    (0x08023d50, 'init_duel_field_icon_and_bg_vram_lp_str_en_a',
     '0x0003ab5e: LP record EN offset A (4 refs)'),
    (0x08023d58, 'init_duel_field_icon_and_bg_vram_lp_str_de_a',
     '0x09def06c: LP record DE string A (2 refs)'),
    (0x08023d60, 'init_duel_field_icon_and_bg_vram_lp_str_fr_a',
     '0x09de2bd2: LP record FR string A (2 refs)'),
    (0x08023d68, 'init_duel_field_icon_and_bg_vram_lp_str_it_a',
     '0x09dd6860: LP record IT string A (2 refs)'),
    (0x08023da0, 'init_duel_field_icon_and_bg_vram_lp_str_es_a',
     '0x09dcaebe: LP record ES string A (2 refs)'),
    (0x08023db0, 'init_duel_field_icon_and_bg_vram_tile_src_d_ptr_a',
     '0x09b953b4: write_tile_row arg (tile src D) call A'),
    (0x08023de8, 'init_duel_field_icon_and_bg_vram_lp_str_jp_b',
     '0x09dc00e2: LP record JP string base B'),
    (0x08023dec, 'init_duel_field_icon_and_bg_vram_lp_str_en_b',
     '0x0003ab5e: LP record EN offset B'),
    (0x08023df4, 'init_duel_field_icon_and_bg_vram_lp_str_de_b',
     '0x09def06c: LP record DE string B'),
    (0x08023dfc, 'init_duel_field_icon_and_bg_vram_lp_str_fr_b',
     '0x09de2bd2: LP record FR string B'),
    (0x08023e04, 'init_duel_field_icon_and_bg_vram_lp_str_it_b',
     '0x09dd6860: LP record IT string B'),
    (0x08023e44, 'init_duel_field_icon_and_bg_vram_lp_str_es_b',
     '0x09dcaebe: LP record ES string B'),
    (0x08023e58, 'init_duel_field_icon_and_bg_vram_lp_str_jp_c',
     '0x09dc00ec: LP record JP string base C (1 ref; variant +0xa offset)'),
    (0x08023e5c, 'init_duel_field_icon_and_bg_vram_lp_str_en_c',
     '0x0003ab5c: LP record EN offset C (1 ref)'),
    (0x08023e64, 'init_duel_field_icon_and_bg_vram_lp_str_de_c',
     '0x09def076: LP record DE string C (1 ref)'),
    (0x08023e6c, 'init_duel_field_icon_and_bg_vram_lp_str_fr_c',
     '0x09de2bdc: LP record FR string C (1 ref)'),
    (0x08023e74, 'init_duel_field_icon_and_bg_vram_lp_str_it_c',
     '0x09dd6868: LP record IT string C (1 ref)'),
    (0x08023ebc, 'init_duel_field_icon_and_bg_vram_lp_str_es_c',
     '0x09dcaec6: LP record ES string C (1 ref)'),
    (0x08023ecc, 'init_duel_field_icon_and_bg_vram_tile_src_d_ptr_b',
     '0x09b953b4: write_tile_row arg B (reuse gfx_src_d value)'),
    (0x08023fc4, 'init_duel_field_icon_and_bg_vram_tile_src_d_ptr_c',
     '0x09b953b4: write_tile_row arg C'),
    (0x08023fd0, 'init_duel_field_icon_and_bg_vram_flags_mask',
     '0xffff807f: mask clears field-state bits in duel scene byte (7 refs)'),

    # -- render_opp_wins_display_oam LP string ptrs --
    (0x08024254, 'render_opp_wins_display_oam_lp_str_jp_a',
     '0x09dbe384: LP record JP string ptr A'),
    (0x08024258, 'render_opp_wins_display_oam_lp_str_en_a',
     '0x0003aad0: LP record EN offset A'),
    (0x08024260, 'render_opp_wins_display_oam_lp_str_de_a',
     '0x09ded174: LP record DE string A'),
    (0x08024268, 'render_opp_wins_display_oam_lp_str_fr_a',
     '0x09de0d2e: LP record FR string A'),
    (0x08024270, 'render_opp_wins_display_oam_lp_str_it_a',
     '0x09dd4a9a: LP record IT string A'),
    (0x080242b0, 'render_opp_wins_display_oam_lp_str_es_a',
     '0x09dc943c: LP record ES string A'),
    (0x08024444, 'render_opp_wins_display_oam_step_lut_ptr',
     '0x09e59ce8: ROM step lookup table ptr (1 ref); passed as base for card icon step'),
    (0x0802465c, 'render_opp_wins_display_oam_iwram_ptr_a',
     '0x03000242: IWRAM duelist record ptr; 2 refs'),
    (0x08024708, 'render_opp_wins_display_oam_iwram_ptr_b',
     '0x03000242: IWRAM addr second slot'),
]

# ---------------------------------------------------------------------------
# D. PLATE rewrites: (func_addr, new_plate_text_ascii)
#    Must be pure ASCII. CJK line 9417 draw_decimal_with_offset fix.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    (0x0802387c,
     "draw_decimal_with_offset: generic decimal digit OAM renderer\n"
     "Args: r0=value(decimal), r1=x_offset, r2=y_offset\n"
     "Renders decimal digits to OAM sprites using gFontJpCtx (0x02006ed0) and OBJ_TILE_VRAM_BASE.\n"
     "Called by render_opp_wins_display_oam and others (>1 callers).\n"
     "Secondary entry point at 0x080242c8."),
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
    print("=== RefineF01Seg7Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    et      = currentProgram.getEquateTable()
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

    # --- D. PLATE rewrites ---
    for func_int, new_text in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no CodeUnit @ 0x%08x" % func_int); continue
        if DRY:
            print("[D dry] plate rewrite @ 0x%08x (%d chars)" % (func_int, len(new_text)))
            nD += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("[D ok] plate rewrite @ 0x%08x" % func_int); nD += 1

    print("=== DONE: EQ=%d REF=%d RENAME=%d PLATE=%d ===" % (nA, nB, nC, nD))


main()
