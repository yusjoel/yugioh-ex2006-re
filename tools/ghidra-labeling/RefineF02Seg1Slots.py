# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg1Slots.py -- file 02 Seg-1 (0x0802c238..0x0802e108)
#   text decimal render + card name escape/format + scene init (23 fn, 318 slots)
#   render_game_text_decimal_to_line / render_card_name_format_to_line /
#   render_card_name_escape_to_line / init_jp_font_linebuf_for_render /
#   commit_glyph_linebuf_to_sprite_vram_with_index / init_card_name_result_screen /
#   tick_scene_blend_fade{out,in,sequence} / init_campaign_bg_and_obj_vram /
#   init_opponent_card_bg_vram / init_pack_selection_tile_vram_default /
#   init_pack_selection_tile_vram_by_deck_{a,b} / init_duel_scroll_params /
#   tick_opponent_aob_by_phase / draw_card_name_label_to_sprite_vram /
#   render_opponent_card_icon_and_name / render_dual_label_to_bg_vram /
#   setup_label_render_ctx / dispatch_opponent_slot_oam_by_phase /
#   init_opponent_card_display_vram / tick_opponent_aob_display
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (new + reuse existing inc constants)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- FUN_ -> current name in plate comments (pure ASCII)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve labels (aob_card_tile_src etc.) are created in rom.s separately;
#       REF_SLOTS below reference them (Ghidra creates USER label at target addr).

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
#    Creates equate (value->name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- GAME_STR_TEXT_BASE = 0x00000c1c (new: text str base offset) ---
    (0x0802c2f0, 0x00000c1c, 'GAME_STR_TEXT_BASE',
     'render_game_text_decimal_to_line_str_base',
     'str_base_offset=0x0c1c; adds to game_str_id_offset'),

    # --- EWRAM_BASE = 0x02000000 (gba_mem.inc, 4295 refs) ---
    (0x0802c2f8, 0x02000000, 'EWRAM_BASE',
     'render_game_text_decimal_to_line_ewram_base', None),
    (0x0802c3e0, 0x02000000, 'EWRAM_BASE',
     'render_card_name_escape_to_line_ewram_base', None),
    (0x0802cbf8, 0x02000000, 'EWRAM_BASE',
     'init_jp_font_linebuf_for_render_ewram_base', None),
    (0x0802cdc0, 0x02000000, 'EWRAM_BASE',
     'init_card_name_result_screen_ewram_base', None),
    (0x0802ce28, 0x02000000, 'EWRAM_BASE',
     'init_card_name_result_screen_ewram_base_b', None),
    (0x0802ce8c, 0x02000000, 'EWRAM_BASE',
     'init_card_name_result_screen_ewram_base_c', None),
    (0x0802cef0, 0x02000000, 'EWRAM_BASE',
     'init_card_name_result_screen_ewram_base_d', None),
    (0x0802d628, 0x02000000, 'EWRAM_BASE',
     'draw_card_name_label_ewram_base', None),
    (0x0802d964, 0x02000000, 'EWRAM_BASE',
     'render_opponent_card_icon_ewram_base', None),
    (0x0802daac, 0x02000000, 'EWRAM_BASE',
     'render_dual_label_ewram_base', None),
    (0x0802deec, 0x02000000, 'EWRAM_BASE',
     'init_opp_card_display_vram_ewram_base', None),

    # --- GSETTINGS_OFFSET = 0x00006c2c (name_input.inc) ---
    (0x0802c2fc, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_game_text_decimal_to_line_gsettings_off', None),
    (0x0802c3e4, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_name_escape_to_line_gsettings_off', None),
    (0x0802cbfc, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_jp_font_linebuf_for_render_gsettings_off', None),
    (0x0802cdc4, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_card_name_result_screen_gsettings_off', None),
    (0x0802ce2c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_card_name_result_screen_gsettings_off_b', None),
    (0x0802ce90, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_card_name_result_screen_gsettings_off_c', None),
    (0x0802cef4, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_card_name_result_screen_gsettings_off_d', None),
    (0x0802d62c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'draw_card_name_label_gsettings_off', None),
    (0x0802d968, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_opponent_card_icon_gsettings_off', None),
    (0x0802dab0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_dual_label_gsettings_off', None),
    (0x0802def0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_opp_card_display_vram_gsettings_off', None),

    # --- CARD_DESC_RENDER_PARAM = 0x00008008 (card_info.inc, EQ_REUSE) ---
    (0x0802c304, 0x00008008, 'CARD_DESC_RENDER_PARAM',
     'render_game_text_decimal_to_line_render_flag',
     'render_glyph_jp layer param: shadow+8'),
    (0x0802c350, 0x00008008, 'CARD_DESC_RENDER_PARAM',
     'render_card_name_format_to_line_render_flag', None),
    (0x0802c3ec, 0x00008008, 'CARD_DESC_RENDER_PARAM',
     'render_card_name_escape_to_line_render_flag', None),
    (0x0802d634, 0x00008008, 'CARD_DESC_RENDER_PARAM',
     'draw_card_name_label_render_flag', None),

    # --- gFontJpCtx = 0x02006ed0 (ewram.inc) ---
    (0x0802c308, 0x02006ed0, 'gFontJpCtx',
     'render_game_text_decimal_to_line_font_ctx', None),
    (0x0802c354, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_format_to_line_font_ctx', None),
    (0x0802c3f0, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_escape_to_line_font_ctx', None),
    (0x0802cbf4, 0x02006ed0, 'gFontJpCtx',
     'init_jp_font_linebuf_for_render_font_ctx', None),
    (0x0802d624, 0x02006ed0, 'gFontJpCtx',
     'draw_card_name_label_font_ctx', None),
    (0x0802d70c, 0x02006ed0, 'gFontJpCtx',
     'render_opponent_card_icon_font_ctx', None),
    (0x0802d7d4, 0x02006ed0, 'gFontJpCtx',
     'render_opponent_card_icon_font_ctx_b', None),
    (0x0802d8c4, 0x02006ed0, 'gFontJpCtx',
     'render_opponent_card_icon_font_ctx_c', None),
    (0x0802dee8, 0x02006ed0, 'gFontJpCtx',
     'init_opp_card_display_vram_font_ctx', None),
    # Note: 0x0802d73c and 0x0802d958 also == gFontJpCtx (0x02006ed0), treated as EQ_REUSE
    (0x0802d73c, 0x02006ed0, 'gFontJpCtx',
     'render_opponent_card_icon_font_ctx_d', None),
    (0x0802d958, 0x02006ed0, 'gFontJpCtx',
     'render_opponent_card_icon_font_ctx_e', None),
    (0x0802daa8, 0x02006ed0, 'gFontJpCtx',
     'render_dual_label_font_ctx', None),

    # --- CARD_ID_BASE_NEG_ADJ = 0xffffd8ef (new) ---
    (0x0802c3f4, 0xffffd8ef, 'CARD_ID_BASE_NEG_ADJ',
     'render_card_name_escape_to_line_card_id_adj',
     'neg adj: -0x2711 so card_id 0x2711 maps to 0'),
    (0x0802cc78, 0xffffd8ef, 'CARD_ID_BASE_NEG_ADJ',
     'init_card_name_result_screen_card_id_adj', None),

    # --- P1LP_TIMER_OFF = 0x00001cec (ewram.inc) ---
    (0x0802c9a0, 0x00001cec, 'P1LP_TIMER_OFF',
     'switchD_273c_lp_timer_off',
     'gP1LifePoints+0x1cec: duel field timer field'),

    # --- BG_PALRAM_SLOT15_BASE = 0x050001e0 (gba_mem.inc) ---
    (0x0802cc04, 0x050001e0, 'BG_PALRAM_SLOT15_BASE',
     'init_jp_font_linebuf_for_render_pal_base', None),
    (0x0802d190, 0x050001e0, 'BG_PALRAM_SLOT15_BASE',
     'init_campaign_bg_and_obj_vram_pal_dst', None),

    # --- RESULT_SCREEN_TILE_IDX_VRAM = 0x06001080 (new) ---
    (0x0802cc60, 0x06001080, 'RESULT_SCREEN_TILE_IDX_VRAM',
     'commit_glyph_linebuf_tile_idx_vram',
     'BG VRAM tile idx write base for result screen glyph line'),

    # --- PUZZLE_NAME_SPRITE_VRAM = 0x06008020 (gba_mem.inc) ---
    (0x0802cc64, 0x06008020, 'PUZZLE_NAME_SPRITE_VRAM',
     'commit_glyph_linebuf_sprite_vram', None),

    # --- PACK_INFO_DISPCNT_SHADOW_INIT = 0x00000401 (gba_mem.inc) ---
    (0x0802cd84, 0x00000401, 'PACK_INFO_DISPCNT_SHADOW_INIT',
     'init_card_name_result_screen_dispcnt', None),

    # --- gDuelDispCtx = 0x0203eeb0 (ewram.inc) ---
    (0x0802cd88, 0x0203eeb0, 'gDuelDispCtx',
     'init_card_name_result_screen_disp_ctx', None),
    (0x0802d15c, 0x0203eeb0, 'gDuelDispCtx',
     'init_campaign_bg_and_obj_vram_disp_ctx', None),

    # --- gVijaState = 0x02029eb0 (ewram.inc) ---
    (0x0802cd8c, 0x02029eb0, 'gVijaState',
     'init_card_name_result_screen_ctx', None),
    (0x0802d160, 0x02029eb0, 'gVijaState',
     'init_campaign_bg_and_obj_vram_ctx', None),

    # --- RESULT_SCREEN_BG2CNT_INIT = 0x00008208 (new) ---
    (0x0802cd94, 0x00008208, 'RESULT_SCREEN_BG2CNT_INIT',
     'init_card_name_result_screen_bg2cnt',
     'BG2CNT: pri=0 charbase=2 16col scrbase=2 size=0'),

    # --- CARD_INFO_BG2CNT_INIT = 0x00000407 (card_info.inc, EQ_REUSE) ---
    (0x0802cd98, 0x00000407, 'CARD_INFO_BG2CNT_INIT',
     'init_card_name_result_screen_bg3cnt', None),

    # --- BG_CHAR_VRAM_CB2 = 0x06004000 (gba_mem.inc, EQ_REUSE) ---
    (0x0802cd9c, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'init_card_name_result_screen_vram_bg', None),
    (0x0802d170, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'init_campaign_bg_and_obj_vram_vram_bg', None),

    # --- OBJ_TILE_VRAM_BASE = 0x06010000 (gba_mem.inc) ---
    (0x0802cda0, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'init_card_name_result_screen_obj_vram', None),
    (0x0802d174, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'init_campaign_bg_and_obj_vram_obj_vram', None),

    # --- OBJ_PAL_SLOT_1 = 0x05000220 (duel_field.inc) ---
    (0x0802cda4, 0x05000220, 'OBJ_PAL_SLOT_1',
     'init_card_name_result_screen_obj_pal', None),
    (0x0802d178, 0x05000220, 'OBJ_PAL_SLOT_1',
     'init_campaign_bg_and_obj_vram_obj_pal', None),

    # --- JP_LANG5_STR_BASE = 0x09dc0240 (new) ---
    (0x0802cdcc, 0x09dc0240, 'JP_LANG5_STR_BASE',
     'init_card_name_result_screen_jp_str_base',
     'JP card name string table base (lang5=ES)'),
    (0x0802ce30, 0x09dc0240, 'JP_LANG5_STR_BASE',
     'init_card_name_result_screen_jp_str_base_b', None),
    (0x0802ce94, 0x09dc0240, 'JP_LANG5_STR_BASE',
     'init_card_name_result_screen_jp_str_base_c', None),
    (0x0802cef8, 0x09dc0240, 'JP_LANG5_STR_BASE',
     'init_card_name_result_screen_jp_str_base_d', None),

    # --- JP_LANG5_STR_OFFSET_ES = 0x0003ab84 (new) ---
    (0x0802cdd0, 0x0003ab84, 'JP_LANG5_STR_OFFSET_ES',
     'init_card_name_result_screen_jp_str_off_es',
     'ES string offset from JP_LANG5_STR_BASE'),
    (0x0802ce34, 0x0003ab84, 'JP_LANG5_STR_OFFSET_ES',
     'init_card_name_result_screen_jp_str_off_es_b', None),
    (0x0802ce98, 0x0003ab84, 'JP_LANG5_STR_OFFSET_ES',
     'init_card_name_result_screen_jp_str_off_es_c', None),
    (0x0802cefc, 0x0003ab84, 'JP_LANG5_STR_OFFSET_ES',
     'init_card_name_result_screen_jp_str_off_es_d', None),

    # --- JP_LANG4_STR_PTR_DE = 0x09def212 (new) ---
    (0x0802cdd8, 0x09def212, 'JP_LANG4_STR_PTR_DE',
     'init_card_name_result_screen_jp_str_de',
     'DE card name string ptr (lang4)'),
    (0x0802ce3c, 0x09def212, 'JP_LANG4_STR_PTR_DE',
     'init_card_name_result_screen_jp_str_de_b', None),
    (0x0802cea0, 0x09def212, 'JP_LANG4_STR_PTR_DE',
     'init_card_name_result_screen_jp_str_de_c', None),
    (0x0802cf04, 0x09def212, 'JP_LANG4_STR_PTR_DE',
     'init_card_name_result_screen_jp_str_de_d', None),

    # --- JP_LANG3_STR_PTR_FR = 0x09de2d5e (new) ---
    (0x0802cde0, 0x09de2d5e, 'JP_LANG3_STR_PTR_FR',
     'init_card_name_result_screen_jp_str_fr',
     'FR card name string ptr (lang3)'),
    (0x0802ce44, 0x09de2d5e, 'JP_LANG3_STR_PTR_FR',
     'init_card_name_result_screen_jp_str_fr_b', None),
    (0x0802cea8, 0x09de2d5e, 'JP_LANG3_STR_PTR_FR',
     'init_card_name_result_screen_jp_str_fr_c', None),
    (0x0802cf0c, 0x09de2d5e, 'JP_LANG3_STR_PTR_FR',
     'init_card_name_result_screen_jp_str_fr_d', None),

    # --- JP_LANG2_STR_PTR_IT = 0x09dd69ec (new) ---
    (0x0802cde8, 0x09dd69ec, 'JP_LANG2_STR_PTR_IT',
     'init_card_name_result_screen_jp_str_it',
     'IT card name string ptr (lang2)'),
    (0x0802ce4c, 0x09dd69ec, 'JP_LANG2_STR_PTR_IT',
     'init_card_name_result_screen_jp_str_it_b', None),
    (0x0802ceb0, 0x09dd69ec, 'JP_LANG2_STR_PTR_IT',
     'init_card_name_result_screen_jp_str_it_c', None),
    (0x0802cf14, 0x09dd69ec, 'JP_LANG2_STR_PTR_IT',
     'init_card_name_result_screen_jp_str_it_d', None),

    # --- JP_LANG1_STR_PTR_EN = 0x09dcb012 (new) ---
    (0x0802ce24, 0x09dcb012, 'JP_LANG1_STR_PTR_EN',
     'init_card_name_result_screen_jp_str_en',
     'EN card name string ptr (lang1)'),
    (0x0802ce84, 0x09dcb012, 'JP_LANG1_STR_PTR_EN',
     'init_card_name_result_screen_jp_str_en_b', None),
    (0x0802ceec, 0x09dcb012, 'JP_LANG1_STR_PTR_EN',
     'init_card_name_result_screen_jp_str_en_c', None),
    (0x0802cf84, 0x09dcb012, 'JP_LANG1_STR_PTR_EN',
     'init_card_name_result_screen_jp_str_en_d', None),

    # --- TEXT_RENDER_COLOR_MODE_1 = 0x00008001 (duel_field.inc, EQ_REUSE) ---
    (0x0802ce88, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'init_card_name_result_screen_render_flag_b', None),
    (0x0802d8c0, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'render_opponent_card_icon_render_flag_c', None),
    (0x0802d960, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'render_opponent_card_icon_render_flag_d', None),
    (0x0802dab8, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'render_dual_label_render_flag', None),
    (0x0802dfac, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'init_opp_card_display_vram_render_flag', None),

    # --- RESULT_SCREEN_SPRITE_VRAM = 0x06004c80 (new) ---
    (0x0802cf88, 0x06004c80, 'RESULT_SCREEN_SPRITE_VRAM',
     'init_card_name_result_screen_sprite_vram',
     'OBJ VRAM base for result screen sprites'),

    # --- gDuelSceneBase = 0x02023360 (ewram.inc) ---
    (0x0802cf8c, 0x02023360, 'gDuelSceneBase',
     'init_card_name_result_screen_scene_ctx', None),
    (0x0802cff4, 0x02023360, 'gDuelSceneBase',
     'tick_scene_blend_fade_sequence_scene_ctx', None),
    (0x0802d4b8, 0x02023360, 'gDuelSceneBase',
     'init_duel_scroll_params_scene_ctx', None),
    (0x0802d4dc, 0x02023360, 'gDuelSceneBase',
     'tick_opponent_aob_by_phase_scene_ctx', None),
    (0x0802d540, 0x02023360, 'gDuelSceneBase',
     'tick_opponent_aob_by_phase_scene_ctx_b', None),
    (0x0802daa0, 0x02023360, 'gDuelSceneBase',
     'render_dual_label_scene_ctx', None),
    (0x0802db2c, 0x02023360, 'gDuelSceneBase',
     'setup_label_render_ctx_scene_ctx', None),
    (0x0802db64, 0x02023360, 'gDuelSceneBase',
     'dispatch_oam_by_phase_scene_ctx', None),
    (0x0802ddc8, 0x02023360, 'gDuelSceneBase',
     'dispatch_oam_caseD3_scene_ctx', None),
    (0x0802e0e4, 0x02023360, 'gDuelSceneBase',
     'tick_aob_display_scene_ctx', None),

    # --- RESULT_SCREEN_TILEMAP_TARGET = 0x06000806 (new) ---
    (0x0802cf90, 0x06000806, 'RESULT_SCREEN_TILEMAP_TARGET',
     'init_card_name_result_screen_tilemap_target',
     'BG VRAM tilemap write addr for result screen tile row'),

    # --- RESULT_SCREEN_FONT_CTX_OFF = 0x00000119 (new) ---
    (0x0802cf94, 0x00000119, 'RESULT_SCREEN_FONT_CTX_OFF',
     'init_card_name_result_screen_font_ctx_off',
     'JP font direction flag offset in scene_ctx'),

    # --- gPrng = 0x03000040 (iwram.inc) ---
    (0x0802d154, 0x03000040, 'gPrng',
     'init_campaign_bg_and_obj_vram_prng', None),
    (0x0802d4b4, 0x03000040, 'gPrng',
     'init_duel_scroll_params_prng', None),
    (0x0802d538, 0x03000040, 'gPrng',
     'tick_opponent_aob_by_phase_prng', None),
    (0x0802d57c, 0x03000040, 'gPrng',
     'tick_opponent_aob_by_phase_prng_b', None),

    # --- DUEL_FIELD_CTRL_VAL = 0x00000601 (duel_field.inc) ---
    (0x0802d158, 0x00000601, 'DUEL_FIELD_CTRL_VAL',
     'init_campaign_bg_and_obj_vram_dispcnt_shadow', None),

    # --- CAMPAIGN_BG1CNT_INIT = 0x00000107 (new) ---
    (0x0802d168, 0x00000107, 'CAMPAIGN_BG1CNT_INIT',
     'init_campaign_bg_and_obj_vram_bg1cnt',
     'BG1CNT: pri=3 charbase=0 16col scrbase=0'),

    # --- CAMPAIGN_BG2CNT_INIT = 0x00000207 (new) ---
    (0x0802d16c, 0x00000207, 'CAMPAIGN_BG2CNT_INIT',
     'init_campaign_bg_and_obj_vram_bg2cnt',
     'BG2CNT: pri=3 charbase=0 16col scrbase=1'),

    # --- CAMPAIGN_TILEMAP_SEQ_START = 0x0000f210 (new) ---
    (0x0802d198, 0x0000f210, 'CAMPAIGN_TILEMAP_SEQ_START',
     'init_campaign_bg_and_obj_vram_tilemap_seq',
     'campaign BG tilemap seq start param'),

    # --- CAMPAIGN_BG_TILEMAP_BASE = 0x06001800 (new) ---
    (0x0802d19c, 0x06001800, 'CAMPAIGN_BG_TILEMAP_BASE',
     'init_campaign_bg_and_obj_vram_tilemap_base',
     'campaign BG tilemap VRAM base'),

    # --- CARD_DESC_BG_VRAM_A = 0x06000800 (card_info.inc) ---
    (0x0802d254, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'init_opponent_card_bg_vram_tilemap_a', None),
    (0x0802d2f4, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'init_pack_selection_default_vram_a', None),
    (0x0802d3bc, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'init_pack_selection_deck_a_vram_a', None),
    (0x0802d484, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'init_pack_selection_deck_b_vram_a', None),

    # --- OBJ_VRAM_BASE_1000 = 0x06001000 (new) ---
    (0x0802d258, 0x06001000, 'OBJ_VRAM_BASE_1000',
     'init_opponent_card_bg_vram_tilemap_b',
     'VRAM base 0x06001000 (BG tile write target)'),
    (0x0802d2f8, 0x06001000, 'OBJ_VRAM_BASE_1000',
     'init_pack_selection_default_vram_b', None),
    (0x0802d3c0, 0x06001000, 'OBJ_VRAM_BASE_1000',
     'init_pack_selection_deck_a_vram_b', None),
    (0x0802d488, 0x06001000, 'OBJ_VRAM_BASE_1000',
     'init_pack_selection_deck_b_vram_b', None),

    # --- PACK_DECK_A_KEY = 0x00002711 (new) ---
    (0x0802d3a4, 0x00002711, 'PACK_DECK_A_KEY',
     'init_pack_selection_deck_a_key',
     'deck A key 0x2711 = find_deck_record_index_by_key param'),

    # --- CARD_STAT_LP_THRESHOLD_20000 = 0x00004e20 (card_info.inc, EQ_REUSE for deck_b_key) ---
    (0x0802d46c, 0x00004e20, 'CARD_STAT_LP_THRESHOLD_20000',
     'init_pack_selection_deck_b_key', None),

    # --- TEXT_RENDER_FLAG_LAYER2 = 0x00008002 (new) ---
    (0x0802d7d0, 0x00008002, 'TEXT_RENDER_FLAG_LAYER2',
     'render_opponent_card_icon_render_flag',
     'text render layer 2 flag'),
    (0x0802d830, 0x00008002, 'TEXT_RENDER_FLAG_LAYER2',
     'render_opponent_card_icon_render_flag_b', None),

    # --- OBJ_PAL_ICON_BASE = 0x05000240 (new) ---
    (0x0802d6fc, 0x05000240, 'OBJ_PAL_ICON_BASE',
     'render_opponent_card_icon_pal_base',
     'OBJ palette base for card icons (PALRAM+0x40)'),

    # --- OBJ_ICON_TILE_VRAM_BASE = 0x06011100 (new) ---
    (0x0802d704, 0x06011100, 'OBJ_ICON_TILE_VRAM_BASE',
     'render_opponent_card_icon_tile_vram',
     'OBJ tile VRAM icon base (OPP_CARD_LABEL_TILE_VRAM_A+0x100)'),

    # --- OPP_CARD_NAME_TILE_VRAM = 0x06012000 (new) ---
    (0x0802d96c, 0x06012000, 'OPP_CARD_NAME_TILE_VRAM',
     'render_opponent_card_icon_name_vram',
     'OBJ tile VRAM write base for opponent card name'),

    # --- DUAL_LABEL_RENDER_STATE_CLEAR = 0xfffc7fff (new) ---
    (0x0802daa4, 0xfffc7fff, 'DUAL_LABEL_RENDER_STATE_CLEAR',
     'render_dual_label_state_clear_mask',
     'clears bits[17:15] of scene_ctx+0x38 render state'),

    # --- OPP_CARD_LABEL_TILE_VRAM_A = 0x06011000 (new) ---
    (0x0802dabc, 0x06011000, 'OPP_CARD_LABEL_TILE_VRAM_A',
     'render_dual_label_tile_vram_a',
     'OBJ tile VRAM base A for opp card label'),

    # --- OPP_CARD_LABEL_TILE_VRAM_B = 0x06011400 (new) ---
    (0x0802dac0, 0x06011400, 'OPP_CARD_LABEL_TILE_VRAM_B',
     'render_dual_label_tile_vram_b', None),

    # --- OPP_CARD_LABEL_TILE_VRAM_C = 0x06011800 (new) ---
    (0x0802dac4, 0x06011800, 'OPP_CARD_LABEL_TILE_VRAM_C',
     'render_dual_label_tile_vram_c', None),

    # --- OPP_CARD_LABEL_TILE_VRAM_D = 0x06011c00 (new) ---
    (0x0802dac8, 0x06011c00, 'OPP_CARD_LABEL_TILE_VRAM_D',
     'render_dual_label_tile_vram_d', None),

    # --- LABEL_CTX_RENDER_STATE_CLEAR = 0xfffffc7f (new) ---
    (0x0802db30, 0xfffffc7f, 'LABEL_CTX_RENDER_STATE_CLEAR',
     'setup_label_render_ctx_mode_mask',
     'clears 2 bits from slot render state (distinct from CAMPAIGN_CARD_ANIM_STEP_MASK)'),

    # --- LABEL_CTX_DISPLAY_PARAM = 0x00a00030 (new) ---
    (0x0802db34, 0x00a00030, 'LABEL_CTX_DISPLAY_PARAM',
     'setup_label_render_ctx_disp_param',
     'display param for label render ctx init'),

    # --- CAMPAIGN_CARD_ANIM_STEP_MASK = 0xfffffe03 (duel_field.inc, EQ_REUSE) ---
    (0x0802db38, 0xfffffe03, 'CAMPAIGN_CARD_ANIM_STEP_MASK',
     'setup_label_render_ctx_state_clear', None),

    # --- AOB_CARD_TILE_VRAM = 0x06014000 (new) ---
    (0x0802decc, 0x06014000, 'AOB_CARD_TILE_VRAM',
     'init_opp_card_display_vram_tile_vram',
     'AOB card OBJ tile VRAM base'),

    # --- AOB_CARD_PAL_DST = 0x05000300 (new) ---
    (0x0802ded4, 0x05000300, 'AOB_CARD_PAL_DST',
     'init_opp_card_display_vram_pal_dst',
     'AOB card OBJ palette dst (PALRAM+0x100)'),

    # --- AOB_INIT_MODE = 0x02000007 (new) ---
    (0x0802dee4, 0x02000007, 'AOB_INIT_MODE',
     'init_opp_card_display_vram_init_mode',
     'AOB init mode: EWRAM_BASE|7 = 0x02000007'),

    # --- OPP_CARD_NAME_STR_OFF_ES = 0x0003a90c (new) ---
    (0x0802defc, 0x0003a90c, 'OPP_CARD_NAME_STR_OFF_ES',
     'init_opp_card_display_str_off_es',
     'ES offset from game_str_ja_0326 base'),

    # --- OPP_CARD_NAME_STR_OFF_ES_NULL = 0x0003a90e (new) ---
    (0x0802df40, 0x0003a90e, 'OPP_CARD_NAME_STR_OFF_ES_NULL',
     'init_opp_card_display_str_off_es_null',
     'ES offset from game_str_ja_0327 base'),

    # --- AOB_DISPLAY_TILE_VRAM_A = 0x06014200 (new) ---
    (0x0802dfb0, 0x06014200, 'AOB_DISPLAY_TILE_VRAM_A',
     'init_opp_card_display_vram_tile_a',
     'AOB display OBJ tile VRAM A'),

    # --- AOB_DISPLAY_TILE_VRAM_B = 0x06014600 (new) ---
    (0x0802dfb4, 0x06014600, 'AOB_DISPLAY_TILE_VRAM_B',
     'init_opp_card_display_vram_tile_b', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # --- puzzle_challenge_record_array @ 0x09e5e9cc (rom.s line 1647, reuse) ---
    (0x0802ca50, 0x09e5e9cc, 'puzzle_challenge_record_array',
     'switchD_2730_puzzle_slot_tbl',
     'ptr to puzzle_challenge_record_array: 49x12B records'),

    # --- name_o_palette_data @ 0x09ccd290 (rom.s line 685, reuse) ---
    (0x0802d194, 0x09ccd290, 'name_o_palette_data',
     'init_campaign_bg_and_obj_vram_pal_src',
     'BG palette src: name_o_palette_data (32B RGB15)'),

    # --- aob_card_tile_src @ 0x098977f8 (carve Host A) ---
    (0x0802ded0, 0x098977f8, 'aob_card_tile_src',
     'init_opp_card_display_vram_tile_src',
     'AOB card tile data src (0x2000B)'),

    # --- aob_card_pal_src @ 0x098997f8 (carve Host A) ---
    (0x0802ded8, 0x098997f8, 'aob_card_pal_src',
     'init_opp_card_display_vram_pal_src',
     'AOB card palette src (0x40B)'),

    # --- aob_ptnsect_src @ 0x09899838 (carve Host A) ---
    (0x0802dee0, 0x09899838, 'aob_ptnsect_src',
     'init_opp_card_display_vram_ptnsect_src',
     'ptnsect data src for init_aob_ctx_from_ptnsect'),

    # NOTE: slot 0x0802dedc = 0x020233ac (gDuelSceneBase+0x4c) is handled as RENAME_SLOT
    # to preserve the raw value 0x020233ac (setting REF to gDuelSceneBase would assemble
    # to 0x02023360, not +0x4c offset).

    # --- campaign_bg_pal_src_a @ 0x0994d6fc (carve Host A) ---
    (0x0802d17c, 0x0994d6fc, 'campaign_bg_pal_src_a',
     'init_campaign_bg_and_obj_vram_pal_src_a', None),

    # --- campaign_bg_pal_src_b @ 0x0994d71c (carve Host A) ---
    (0x0802d180, 0x0994d71c, 'campaign_bg_pal_src_b',
     'init_campaign_bg_and_obj_vram_pal_src_b', None),

    # --- campaign_bg_pal_src_c @ 0x09a1a52c (carve Host A) ---
    (0x0802d184, 0x09a1a52c, 'campaign_bg_pal_src_c',
     'init_campaign_bg_and_obj_vram_pal_src_c', None),
    (0x0802d3a8, 0x09a1a52c, 'campaign_bg_pal_src_c',
     'init_pack_selection_deck_a_pal_src', None),

    # --- campaign_bg_tile_src @ 0x0994f83c (carve Host A) ---
    (0x0802d188, 0x0994f83c, 'campaign_bg_tile_src',
     'init_campaign_bg_and_obj_vram_tile_src', None),

    # --- campaign_bg_tilemap_src @ 0x0995383c (carve Host A) ---
    (0x0802d18c, 0x0995383c, 'campaign_bg_tilemap_src',
     'init_campaign_bg_and_obj_vram_tilemap_src', None),

    # --- result_screen_pal2_src @ 0x09b921d4 (carve Host B) ---
    (0x0802cda8, 0x09b921d4, 'result_screen_pal2_src',
     'init_card_name_result_screen_pal2_src',
     'result screen copy_bytes_by_halfword src (0x20B)'),

    # --- result_screen_tile1_src @ 0x09b921f4 (carve Host B) ---
    (0x0802cdac, 0x09b921f4, 'result_screen_tile1_src',
     'init_card_name_result_screen_tile1_src', None),

    # --- result_screen_tile2_src @ 0x09b929f4 (carve Host B) ---
    (0x0802cdb0, 0x09b929f4, 'result_screen_tile2_src',
     'init_card_name_result_screen_tile2_src', None),

    # --- result_screen_tile3_src @ 0x09b93484 (carve Host B) ---
    (0x0802cdb4, 0x09b93484, 'result_screen_tile3_src',
     'init_card_name_result_screen_tile3_src', None),

    # --- result_screen_tile4_src @ 0x09b93844 (carve Host B) ---
    (0x0802cdb8, 0x09b93844, 'result_screen_tile4_src',
     'init_card_name_result_screen_tile4_src', None),

    # --- pack_default_pal_src @ 0x09b97b28 (carve Host B) ---
    (0x0802d2e8, 0x09b97b28, 'pack_default_pal_src',
     'init_pack_selection_default_pal', None),

    # --- pack_default_tile_src @ 0x09b97d68 (carve Host B) ---
    (0x0802d2ec, 0x09b97d68, 'pack_default_tile_src',
     'init_pack_selection_default_tile_src', None),

    # --- pack_default_tilemap_src @ 0x09b9bd68 (carve Host B) ---
    (0x0802d2f0, 0x09b9bd68, 'pack_default_tilemap_src',
     'init_pack_selection_default_tilemap', None),

    # --- pack_deck_a_tile1_src @ 0x09a1dfac (carve Host A) ---
    (0x0802d3ac, 0x09a1dfac, 'pack_deck_a_tile1_src',
     'init_pack_selection_deck_a_tile1_src', None),

    # --- pack_deck_a_tile2_src @ 0x09a98dec (carve Host A) ---
    (0x0802d3b0, 0x09a98dec, 'pack_deck_a_tile2_src',
     'init_pack_selection_deck_a_tile2_src', None),

    # --- pack_deck_a_tile3_src @ 0x09a85fac (carve Host A) ---
    (0x0802d3b4, 0x09a85fac, 'pack_deck_a_tile3_src',
     'init_pack_selection_deck_a_tile3_src', None),

    # --- pack_deck_a_tilemap_src @ 0x09b00dec (carve Host A) ---
    (0x0802d3b8, 0x09b00dec, 'pack_deck_a_tilemap_src',
     'init_pack_selection_deck_a_tilemap_src', None),

    # --- pack_deck_b_pal_src @ 0x09953cec (carve Host A) ---
    (0x0802d470, 0x09953cec, 'pack_deck_b_pal_src',
     'init_pack_selection_deck_b_pal_src', None),

    # --- pack_deck_b_tile1_src @ 0x09956c2c (carve Host A) ---
    (0x0802d474, 0x09956c2c, 'pack_deck_b_tile1_src',
     'init_pack_selection_deck_b_tile1_src', None),

    # --- pack_deck_b_tile2_src @ 0x099ba04c (carve Host A) ---
    (0x0802d478, 0x099ba04c, 'pack_deck_b_tile2_src',
     'init_pack_selection_deck_b_tile2_src', None),

    # --- pack_deck_b_tile3_src @ 0x099aac2c (carve Host A) ---
    (0x0802d47c, 0x099aac2c, 'pack_deck_b_tile3_src',
     'init_pack_selection_deck_b_tile3_src', None),

    # --- pack_deck_b_tilemap_src @ 0x09a0e04c (carve Host A) ---
    (0x0802d480, 0x09a0e04c, 'pack_deck_b_tilemap_src',
     'init_pack_selection_deck_b_tilemap_src', None),

    # --- aob_phase_table @ 0x09e59db4 (carve Host C) ---
    (0x0802d53c, 0x09e59db4, 'aob_phase_table',
     'tick_opponent_aob_by_phase_phase_tbl',
     'AOB phase dispatch table: stride 2 halfword, phase [0..7]'),
    (0x0802e0f8, 0x09e59db4, 'aob_phase_table',
     'tick_aob_display_phase_tbl', None),

    # --- game_str_pointer_table @ 0x08000f40 (existing) ---
    # Already PTR_ prefixed in Ghidra; ensure ref exists
    (0x0802c2f4, 0x08000f40, 'game_str_pointer_table',
     'render_game_text_ptr_game_str_pointer_table', None),
    (0x0802c3dc, 0x08000f40, 'game_str_pointer_table',
     'render_card_name_escape_ptr_game_str_pointer_table', None),
    (0x0802c82c, 0x08000f40, 'game_str_pointer_table',
     'switchD_2712_ptr_game_str_pointer_table', None),
    (0x0802c88c, 0x08000f40, 'game_str_pointer_table',
     'switchD_2713_ptr_game_str_pointer_table', None),
    (0x0802c8ec, 0x08000f40, 'game_str_pointer_table',
     'switchD_2714_ptr_game_str_pointer_table', None),
    (0x0802c94c, 0x08000f40, 'game_str_pointer_table',
     'switchD_2715_ptr_game_str_pointer_table', None),
    (0x0802ca40, 0x08000f40, 'game_str_pointer_table',
     'switchD_2730_ptr_game_str_pointer_table', None),
    (0x0802cb88, 0x08000f40, 'game_str_pointer_table',
     'switchD_2744_ptr_game_str_pointer_table', None),

    # --- game_str_ja @ 0x09db9c10 (existing) ---
    (0x0802c300, 0x09db9c10, 'game_str_ja',
     'render_game_text_ptr_game_str_ja', None),
    (0x0802c3e8, 0x09db9c10, 'game_str_ja',
     'render_card_name_escape_ptr_game_str_ja', None),
    (0x0802c838, 0x09db9c10, 'game_str_ja',
     'switchD_2712_ptr_game_str_ja', None),
    (0x0802c898, 0x09db9c10, 'game_str_ja',
     'switchD_2713_ptr_game_str_ja', None),
    (0x0802c8f8, 0x09db9c10, 'game_str_ja',
     'switchD_2714_ptr_game_str_ja', None),
    (0x0802c958, 0x09db9c10, 'game_str_ja',
     'switchD_2715_ptr_game_str_ja', None),
    (0x0802ca4c, 0x09db9c10, 'game_str_ja',
     'switchD_2730_ptr_game_str_ja', None),
    (0x0802cb94, 0x09db9c10, 'game_str_ja',
     'switchD_2744_ptr_game_str_ja', None),

    # --- font_jp_base_table (existing Ghidra label @ 0x09e5f854) ---
    (0x0802cc00, 0x09e5f854, 'font_jp_base_table',
     'init_jp_font_linebuf_ptr_font_jp_base_table', None),
    (0x0802cdc8, 0x09e5f854, 'font_jp_base_table',
     'init_card_name_result_screen_ptr_font_jp_base_table', None),
    (0x0802d630, 0x09e5f854, 'font_jp_base_table',
     'draw_card_name_label_ptr_font_jp_base_table', None),
    (0x0802d710, 0x09e5f854, 'font_jp_base_table',
     'render_opponent_card_icon_ptr_font_jp_base_table_a', None),
    (0x0802d740, 0x09e5f854, 'font_jp_base_table',
     'render_opponent_card_icon_ptr_font_jp_base_table_b', None),
    (0x0802d7d8, 0x09e5f854, 'font_jp_base_table',
     'render_opponent_card_icon_ptr_font_jp_base_table_c', None),
    (0x0802d82c, 0x09e5f854, 'font_jp_base_table',
     'render_opponent_card_icon_ptr_font_jp_base_table_d', None),
    (0x0802d8c8, 0x09e5f854, 'font_jp_base_table',
     'render_opponent_card_icon_ptr_font_jp_base_table_e', None),
    (0x0802d95c, 0x09e5f854, 'font_jp_base_table',
     'render_opponent_card_icon_ptr_font_jp_base_table_f', None),
    (0x0802dab4, 0x09e5f854, 'font_jp_base_table',
     'render_dual_label_ptr_font_jp_base_table', None),
    (0x0802def4, 0x09e5f854, 'font_jp_base_table',
     'init_opp_card_display_vram_ptr_font_jp_base_table', None),

    # --- icon_palettes_base (existing label, file 01 @ 0x09896290) ---
    (0x0802d700, 0x09896290, 'icon_palettes_base',
     'render_opponent_card_icon_icon_pal_base', None),

    # --- icon_tiles_base (existing label, file 01 @ 0x0988cf30) ---
    (0x0802d708, 0x0988cf30, 'icon_tiles_base',
     'render_opponent_card_icon_icon_tile_base', None),

    # --- gP1LifePoints @ 0x0201c4e0 (ewram.inc) ---
    (0x0802c99c, 0x0201c4e0, 'gP1LifePoints',
     'switchD_273c_lp_ptr', None),

    # --- opponent_palettes_base (existing label @ 0x09b101ac) ---
    (0x0802d240, 0x09b101ac, 'opponent_palettes_base',
     'init_opponent_card_bg_vram_opp_pal_base', None),

    # --- opponent_top_tiles_base (existing label @ 0x09b1200c) ---
    (0x0802d244, 0x09b1200c, 'opponent_top_tiles_base',
     'init_opponent_card_bg_vram_opp_top_tiles', None),

    # --- opponent_bottom_tiles_base (existing label @ 0x09b51cfc) ---
    (0x0802d248, 0x09b51cfc, 'opponent_bottom_tiles_base',
     'init_opponent_card_bg_vram_opp_bot_tiles', None),

    # --- opponent_top_tilemap_base (existing label @ 0x09b4800c) ---
    (0x0802d24c, 0x09b4800c, 'opponent_top_tilemap_base',
     'init_opponent_card_bg_vram_opp_top_tilemap', None),

    # --- opponent_bottom_tilemap_base (existing label @ 0x09b87cfc) ---
    (0x0802d250, 0x09b87cfc, 'opponent_bottom_tilemap_base',
     'init_opponent_card_bg_vram_opp_bot_tilemap', None),

    # --- game_str_ja_0326 (data/game-strings-ja.s, reuse) ---
    (0x0802def8, 0x09dbd7e8, 'game_str_ja_0326',
     'init_opp_card_display_str_ja_0326',
     'game_str_ja_0326: JA quiz result str'),

    # --- game_str_it_0326 (data/game-strings-it.s, reuse): 0x09dec2de in IT range ---
    (0x0802df04, 0x09dec2de, 'game_str_it_0326',
     'init_opp_card_display_str_it_0326', None),

    # --- game_str_fr_0326 (data/game-strings-fr.s, reuse): 0x09ddffe0 in FR range ---
    (0x0802df0c, 0x09ddffe0, 'game_str_fr_0326',
     'init_opp_card_display_str_fr_0326', None),

    # --- game_str_de_0326 (data/game-strings-de.s, reuse): 0x09dd3d04 in DE range ---
    (0x0802df14, 0x09dd3d04, 'game_str_de_0326',
     'init_opp_card_display_str_de_0326', None),

    # --- game_str_en_0326 (data/game-strings-en.s, reuse) ---
    (0x0802df1c, 0x09dc8842, 'game_str_en_0326',
     'init_opp_card_display_str_en_0326', None),

    # --- game_str_ja_0327 ---
    (0x0802df3c, 0x09dbd7f2, 'game_str_ja_0327',
     'init_opp_card_display_str_ja_0327', None),

    # --- game_str_it_0327 (IT range: 0x09dec2e6) ---
    (0x0802df48, 0x09dec2e6, 'game_str_it_0327',
     'init_opp_card_display_str_it_0327', None),

    # --- game_str_fr_0327 (FR range: 0x09ddffea) ---
    (0x0802df50, 0x09ddffea, 'game_str_fr_0327',
     'init_opp_card_display_str_fr_0327', None),

    # --- game_str_de_0327 (DE range: 0x09dd3d0e) ---
    (0x0802df58, 0x09dd3d0e, 'game_str_de_0327',
     'init_opp_card_display_str_de_0327', None),

    # --- game_str_en_0327 ---
    (0x0802dfa8, 0x09dc884c, 'game_str_en_0327',
     'init_opp_card_display_str_en_0327', None),

    # --- CARD_INFO_NAME_SPRITE_VRAM = 0x06008200 (card_info.inc) ---
    (0x0802d620, 0x06008200, 'CARD_INFO_NAME_SPRITE_VRAM',
     'draw_card_name_label_sprite_vram', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # switchD caseD literal pool slots
    (0x0802c4e0, 'switchD_2711_pool',
     'game_str offset for case 0x2711'),
    (0x0802c4f0, 'switchD_2712_pool',
     'game_str offset for case 0x2712'),
    (0x0802c500, 'switchD_2713_pool',
     'game_str offset for case 0x2713'),

    # caseD_2714 pool (8 slots)
    (0x0802c538, 'switchD_2714_pool_a', 'game_str ID for case 0x2714 path A'),
    (0x0802c548, 'switchD_2714_pool_b', 'game_str ID for case 0x2714 path B'),
    (0x0802c558, 'switchD_2714_pool_c', 'game_str ID for case 0x2714 path C'),
    (0x0802c568, 'switchD_2714_pool_d', 'game_str ID for case 0x2714 path D'),
    (0x0802c578, 'switchD_2714_pool_e', 'game_str ID for case 0x2714 path E'),
    (0x0802c588, 'switchD_2714_pool_f', 'game_str ID for case 0x2714 path F'),
    (0x0802c598, 'switchD_2714_pool_g', 'game_str ID for case 0x2714 path G'),
    (0x0802c5b8, 'switchD_2714_pool_h', 'game_str ID for case 0x2714 path H'),

    # caseD_2715 pool (8 slots)
    (0x0802c610, 'switchD_2715_pool_a', 'game_str ID for case 0x2715 path A'),
    (0x0802c620, 'switchD_2715_pool_b', 'game_str ID for case 0x2715 path B'),
    (0x0802c630, 'switchD_2715_pool_c', 'game_str ID for case 0x2715 path C'),
    (0x0802c640, 'switchD_2715_pool_d', 'game_str ID for case 0x2715 path D'),
    (0x0802c650, 'switchD_2715_pool_e', 'game_str ID for case 0x2715 path E'),
    (0x0802c660, 'switchD_2715_pool_f', 'game_str ID for case 0x2715 path F'),
    (0x0802c670, 'switchD_2715_pool_extra', 'game_str ID continuation for 0x2715'),

    # caseD_2716 pool
    (0x0802c680, 'switchD_2716_pool', 'game_str ID for case 0x2716'),

    # switchD table ptr
    (0x0802c3f8, 'render_card_name_escape_switch_tbl_ptr',
     'ptr to switchdataD_0802c3fc (81-case table)'),

    # other switchD case pools (representative)
    (0x0802c700, 'switchD_case_pool_c700', 'game_str offset switchD case'),
    (0x0802c730, 'switchD_case_pool_c730', 'game_str offset switchD case'),
    (0x0802c758, 'switchD_case_pool_c758', 'game_str offset switchD case'),
    (0x0802c780, 'switchD_case_pool_c780', 'game_str offset switchD case'),
    (0x0802c798, 'switchD_case_pool_c798', 'game_str offset switchD case'),
    (0x0802c7a8, 'switchD_case_pool_c7a8', 'game_str offset switchD case'),
    (0x0802c7cc, 'switchD_case_pool_c7cc', 'game_str offset switchD case'),
    (0x0802c7d8, 'switchD_case_pool_c7d8', 'game_str offset switchD case'),

    # dispatch_opponent_slot_oam_by_phase OAM constants (7 slots phase 1/2)
    (0x0802dc74, 'dispatch_oam_slot_pool_a', 'OAM tile index for slot phase 1'),
    (0x0802dc78, 'dispatch_oam_slot_pool_b', 'OAM tile index for slot phase 1'),
    (0x0802dc7c, 'dispatch_oam_slot_pool_c', 'OAM tile index for slot phase 2'),
    (0x0802dc80, 'dispatch_oam_slot_pool_d', 'OAM tile index for slot phase 2'),
    (0x0802dc84, 'dispatch_oam_slot_pool_e', 'OAM tile index for slot phase 2'),
    (0x0802dc88, 'dispatch_oam_slot_pool_f', 'OAM tile index for slot phase 2'),
    (0x0802dc8c, 'dispatch_oam_slot_pool_g', 'OAM tile index for slot phase 2'),

    # dispatch_opponent_slot_oam_by_phase caseD_3 OAM constants (15 slots)
    (0x0802dde0, 'dispatch_oam_caseD3_pool_a', 'OAM tile index slot phase 3'),
    (0x0802dde4, 'dispatch_oam_caseD3_pool_b', 'OAM tile index slot phase 3'),
    (0x0802dde8, 'dispatch_oam_caseD3_pool_c', 'OAM tile index slot phase 3'),
    (0x0802ddec, 'dispatch_oam_caseD3_pool_d', 'OAM tile index slot phase 4'),
    (0x0802ddf0, 'dispatch_oam_caseD3_pool_e', 'OAM tile index slot phase 4'),
    (0x0802ddf4, 'dispatch_oam_caseD3_pool_f', 'OAM tile index slot phase 4'),
    (0x0802ddf8, 'dispatch_oam_caseD3_pool_g', 'OAM tile index slot phase 4'),
    (0x0802ddfc, 'dispatch_oam_caseD3_pool_h', 'OAM tile index slot phase 4'),
    (0x0802de00, 'dispatch_oam_caseD3_pool_i', 'OAM tile index slot phase 5'),
    (0x0802de04, 'dispatch_oam_caseD3_pool_j', 'OAM tile index slot phase 5'),
    (0x0802de08, 'dispatch_oam_caseD3_pool_k', 'OAM tile index slot phase 5'),
    (0x0802de0c, 'dispatch_oam_caseD3_pool_l', 'OAM tile index slot phase 5'),
    (0x0802de10, 'dispatch_oam_caseD3_pool_m', 'OAM tile index slot phase 5'),
    (0x0802de14, 'dispatch_oam_default_pool_a', 'OAM tile index default case'),
    (0x0802de18, 'dispatch_oam_default_pool_b', 'OAM tile index default case'),
    (0x0802de1c, 'dispatch_oam_default_pool_c', 'OAM tile index default case'),
    (0x0802de20, 'dispatch_oam_default_pool_d', 'OAM tile index default case'),
    (0x0802de24, 'dispatch_oam_default_pool_e', 'OAM tile index default case'),

    # aob_ctx_sub slot (keep raw value 0x020233ac = gDuelSceneBase+0x4c)
    (0x0802dedc, 'init_opp_card_display_vram_aob_ctx_sub',
     'aob ctx sub-struct ptr: gDuelSceneBase+0x4c = 0x020233ac'),

    # tick_opponent_aob_display OAM packed constants
    (0x0802e0e8, 'tick_aob_display_oam_xy_a',
     'OAM packed xy for 2nd-layer sprite A: y=0x50 x=0x58'),
    (0x0802e0ec, 'tick_aob_display_oam_tile_a',
     'OAM tile index A for 2nd-layer sprite: 0x1210'),
    (0x0802e0f0, 'tick_aob_display_oam_xy_b',
     'OAM packed xy for 2nd-layer sprite B: y=0x50 x=0x78'),
    (0x0802e0f4, 'tick_aob_display_oam_tile_b',
     'OAM tile index B: 0x1214'),
    (0x0802e0fc, 'tick_aob_display_oam_attr1_large',
     'OAM attr1 0x388c: y=0x38 large-size'),
    (0x0802e100, 'tick_aob_display_oam_attr1_b',
     'OAM attr1 0x2888'),
    (0x0802e104, 'tick_aob_display_oam_attr2',
     'OAM attr2 0x40c0: tile=0xc0 pal=4'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces FUN_ references in existing plate comments.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # C8 fix #1: render_card_name_format_to_line plate: FUN_0802c358 -> render_card_name_escape_to_line
    (0x0802c30c,
     'FUN_0802c358',
     'render_card_name_escape_to_line'),

    # C8 fix #2: tick_scene_blend_fadein_step plate: FUN_0802cfd4 -> tick_scene_blend_fade_sequence
    (0x0802cfb4,
     'FUN_0802cfd4',
     'tick_scene_blend_fade_sequence'),

    # C8 fix #3: tick_scene_blend_fadeout_step plate: FUN_0802cfd4 -> tick_scene_blend_fade_sequence
    (0x0802cf98,
     'FUN_0802cfd4',
     'tick_scene_blend_fade_sequence'),

    # C8 fix #4: tick_opponent_aob_by_phase plate: FUN_0802dfb8 -> tick_opponent_aob_display
    (0x0802d4bc,
     'FUN_0802dfb8',
     'tick_opponent_aob_display'),
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

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (
        slot_addr, target_vaddr, gas_label, slot_label))

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

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg1Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-1: 0x0802c238..0x0802e108, 23 fn, 318 slots")

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

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES: FUN_ fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF02Seg1Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

main()
