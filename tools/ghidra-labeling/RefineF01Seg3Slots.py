# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg3Slots.py -- f01 Seg-3 (0x0801d998..0x0801e36c)
#   asm/01_vija_scene_text.s: card_info scene, 8 functions:
#   card_image_decode_wrapper / render_card_name_to_desc_page_vram (was card_info_page_step_03_unknown) /
#   tick_scroll_frame_and_update_pos / render_card_description_text /
#   card_info_page_finalize / blit_glyph_2x2_to_bg_vram /
#   tick_blend_fadeout_and_set_dispcnt / tick_blend_fadein_and_poll_done
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (new card_info/gba_mem/gba_io constants)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename (reuse/carve labels)
#   C. RENAME_SLOTS -- plain rename + optional EOL
#   D. FUNC_RENAME -- rename function card_info_page_step_03_unknown -> render_card_name_to_desc_page_vram
#   E. PLATE_REWRITES -- CJK plate replacement with pure ASCII
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
    # === Fn-1: card_image_decode_wrapper (0x0801d998) ===
    # --- card_info.inc new constants ---
    (0x0801da90, 0x0985004c, 'CARD_TILE_PACK_GLYPH_OFF_A',
     'card_image_decode_wrapper_tile_a',
     'card_glyph_table_3+0xa80: tile src A for card info BG map'),
    (0x0801da94, 0x0000020e, 'CARD_TILE_PACK_MAP_PARAM',
     'card_image_decode_wrapper_map_param',
     'load_pack_tile_and_map_to_vram map param (0x020e)'),
    (0x0801da98, 0x09850934, 'CARD_TILE_PACK_GLYPH_OFF_B',
     'card_image_decode_wrapper_tile_b',
     'card_glyph_table_3+0x1368: tile src B for card info BG map'),
    (0x0801da9c, 0x0984a3fc, 'CARD_FRAME_TILE_SRC_MONSTER',
     'card_image_decode_wrapper_tile_c',
     'seg-C blob: monster card frame tile pack source'),
    (0x0801daa0, 0x050000a0, 'CARD_FRAME_BG_PAL_BASE',
     'card_image_decode_wrapper_bg_pal',
     'BG PALRAM row 5 (card frame BG palette base)'),
    (0x0801daa4, 0x050003a0, 'CARD_FRAME_OBJ_PAL_MONSTER',
     'card_image_decode_wrapper_obj_pal_a',
     'OBJ PALRAM slot 13: monster frame palette'),
    (0x0801daa8, 0x0984dd6c, 'CARD_FRAME_PAL_SRC_MONSTER_A',
     'card_image_decode_wrapper_pal_a',
     'seg-C blob: monster frame OBJ palette A (32B)'),
    (0x0801daac, 0x06017440, 'CARD_FRAME_OBJ_TILE_BASE',
     'card_image_decode_wrapper_obj_tile',
     'OBJ VRAM card frame tile base (OBJ+0x7440)'),
    (0x0801dab0, 0x0984d8ec, 'CARD_FRAME_TILE_SRC_MONSTER_A',
     'card_image_decode_wrapper_tile_d',
     'seg-C blob: monster frame OBJ tile data A (256B)'),
    (0x0801dab4, 0x06010020, 'CARD_FRAME_OBJ_TILE_SLOT1',
     'card_image_decode_wrapper_tile_s1',
     'OBJ_TILE_VRAM_BASE+0x20: tile slot 1 for card art overlay'),
    (0x0801dab8, 0x09ccd2d0, 'CARD_OVERLAY_TILE_SRC',
     'card_image_decode_wrapper_overlay',
     'name_o region+0x40: card overlay nibble-sequence tile (5 refs)'),

    (0x0801db10, 0x0984b994, 'CARD_FRAME_TILE_SRC_SPELL',
     'card_image_decode_wrapper_tile_e',
     'seg-C blob: spell card frame tile pack source (type23)'),
    (0x0801db14, 0x050000a0, 'CARD_FRAME_BG_PAL_BASE',
     'card_image_decode_wrapper_bg_pal_b', None),
    (0x0801db18, 0x050003a0, 'CARD_FRAME_OBJ_PAL_MONSTER',
     'card_image_decode_wrapper_obj_pal_b', None),
    (0x0801db1c, 0x0984de6c, 'CARD_FRAME_PAL_SRC_SPELL_A',
     'card_image_decode_wrapper_pal_b',
     'seg-C blob: spell frame OBJ palette A'),
    (0x0801db20, 0x06017440, 'CARD_FRAME_OBJ_TILE_BASE',
     'card_image_decode_wrapper_obj_tile_b', None),
    (0x0801db24, 0x0984dcec, 'CARD_FRAME_TILE_SRC_SPELL_A',
     'card_image_decode_wrapper_tile_f',
     'seg-C blob: spell frame OBJ tile data A'),
    (0x0801db28, 0x050003c0, 'CARD_FRAME_OBJ_PAL_SPELL',
     'card_image_decode_wrapper_obj_pal_c',
     'OBJ PALRAM slot 14: spell/star frame palette'),
    (0x0801db2c, 0x0984f52c, 'CARD_FRAME_PAL_SRC_STAR_A',
     'card_image_decode_wrapper_pal_c',
     'seg-C blob: star/level frame OBJ palette A'),
    (0x0801db30, 0x060174c0, 'CARD_LEVEL_OBJ_TILE_BASE',
     'card_image_decode_wrapper_star_tile',
     'OBJ VRAM card level star tile base (OBJ+0x74c0)'),

    # --- dup block 0xdb90..0xdbb4 ---
    (0x0801db90, 0x0984b994, 'CARD_FRAME_TILE_SRC_SPELL',
     'card_image_decode_wrapper_tile_e2', None),
    (0x0801db94, 0x050000a0, 'CARD_FRAME_BG_PAL_BASE',
     'card_image_decode_wrapper_bg_pal_c', None),
    (0x0801db98, 0x050003a0, 'CARD_FRAME_OBJ_PAL_MONSTER',
     'card_image_decode_wrapper_obj_pal_d', None),
    (0x0801db9c, 0x0984de4c, 'CARD_FRAME_PAL_SRC_MONSTER_B',
     'card_image_decode_wrapper_pal_d',
     'seg-C blob: monster frame OBJ palette B'),
    (0x0801dba0, 0x06017440, 'CARD_FRAME_OBJ_TILE_BASE',
     'card_image_decode_wrapper_obj_tile_c', None),
    (0x0801dba4, 0x0984dc6c, 'CARD_FRAME_TILE_SRC_STAR',
     'card_image_decode_wrapper_tile_g',
     'seg-C blob: star/level OBJ tile data'),
    (0x0801dba8, 0x050003c0, 'CARD_FRAME_OBJ_PAL_SPELL',
     'card_image_decode_wrapper_obj_pal_e', None),
    (0x0801dbac, 0x0984f52c, 'CARD_FRAME_PAL_SRC_STAR_A',
     'card_image_decode_wrapper_pal_e', None),
    (0x0801dbb0, 0x060174c0, 'CARD_LEVEL_OBJ_TILE_BASE',
     'card_image_decode_wrapper_star_tile_b', None),
    (0x0801dbb4, 0x0984f46c, 'CARD_FRAME_TILE_SRC_STAR_B',
     'card_image_decode_wrapper_tile_h',
     'seg-C blob: star/level OBJ tile data B'),

    # === Fn-2: render_card_name_to_desc_page_vram (0x0801dbdc) ===
    # All slots are reuse of existing globals (gFontJpCtx/EWRAM_BASE/GSETTINGS_OFFSET/gCardInfoPageState)
    # handled in REF_SLOTS or RENAME_SLOTS sections
    (0x0801ddf0, 0x00008008, 'CARD_DESC_RENDER_PARAM',
     'render_card_name_to_desc_page_vram_render_param',
     'render_glyph_jp layer param for card description text'),
    (0x0801df4c, 0x06007100, 'CARD_DESC_LINE_BUF_VRAM',
     'render_card_name_to_desc_page_vram_line_buf',
     'BG VRAM card description text line buffer'),
    (0x0801df58, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'render_card_name_to_desc_page_vram_bg_a',
     'BG VRAM desc page tile region A'),
    (0x0801df94, 0x06000c80, 'CARD_DESC_BG_VRAM_B',
     'render_card_name_to_desc_page_vram_bg_b',
     'BG VRAM desc page tile region B'),
    (0x0801df48, 0x00008008, 'CARD_DESC_RENDER_PARAM',
     'render_card_name_to_desc_page_vram_render_param_b', None),

    # === Fn-4: render_card_description_text (0x0801e000) ===
    (0x0801e0fc, 0x06010040, 'CARD_DESC_OBJ_TILE_BASE',
     'render_card_description_text_obj_tile',
     'OBJ_TILE_VRAM_BASE+0x40: tile slot 2 for card desc text'),

    # === Fn-5: card_info_page_finalize (0x0801e100) ===
    (0x0801e194, 0x05000380, 'CARD_FRAME_OBJ_PAL_LEVEL',
     'card_info_page_finalize_obj_pal_level',
     'OBJ PALRAM slot 12: level/icon frame palette (PAL+0x180)'),
    (0x0801e198, 0x0984f3ac, 'CARD_FRAME_PAL_SRC_ICON_B',
     'card_info_page_finalize_pal_src_icon_b',
     'seg-C blob: icon frame OBJ palette B (type 0x16)'),
    (0x0801e19c, 0x06017500, 'CARD_SPELL_OBJ_TILE_BASE',
     'card_info_page_finalize_spell_tile_base',
     'OBJ VRAM spell card icon tile base (OBJ+0x7500)'),
    (0x0801e1a0, 0x0984f0ac, 'CARD_FRAME_TILE_SRC_ICON',
     'card_info_page_finalize_tile_src_icon',
     'seg-C blob: icon frame OBJ tile data (type 0x16)'),
    (0x0801e270, 0x05000380, 'CARD_FRAME_OBJ_PAL_LEVEL',
     'card_info_page_finalize_obj_pal_level_b', None),
    (0x0801e274, 0x0984ee2c, 'CARD_FRAME_PAL_SRC_ICON_A',
     'card_info_page_finalize_pal_src_icon_a',
     'seg-C blob: icon frame OBJ palette A (type 0x17)'),
    (0x0801e278, 0x06017500, 'CARD_SPELL_OBJ_TILE_BASE',
     'card_info_page_finalize_spell_tile_base_b', None),
    (0x0801e27c, 0x0984e42c, 'CARD_FRAME_TILE_SRC_SPELL_B',
     'card_info_page_finalize_tile_src_spell_b',
     'seg-C blob: spell frame OBJ tile data B (type 0x17)'),
    (0x0801e28c, 0x06017580, 'CARD_ICON_OBJ_TILE_BASE',
     'card_info_page_finalize_icon_tile_base',
     'OBJ VRAM card icon/status tile base (OBJ+0x7580)'),

    # === Fn-6: blit_glyph_2x2_to_bg_vram (0x0801e294) ===
    # BG_CHAR_VRAM_CB2 (0x06004000) already in gba_mem.inc
    (0x0801e31c, 0x06000002, 'BG_SCREEN_TILE_OFF_1',
     'blit_glyph_2x2_to_bg_vram_screen_tile_off1',
     'BG screen map entry 1 (tile row 0 col 1 = map base+2)'),
    (0x0801e320, 0x06000040, 'BG_SCREEN_ROW1_OFF',
     'blit_glyph_2x2_to_bg_vram_screen_row1_off',
     'BG screen map row 1 base (32 tiles * 2B = 0x40 per row)'),
    (0x0801e324, 0x06000042, 'BG_SCREEN_ROW1_TILE1',
     'blit_glyph_2x2_to_bg_vram_screen_row1_tile1',
     'BG screen map row 1 col 1 (0x06000040+2)'),

    # === Fn-8: tick_blend_fadein_and_poll_done (0x0801e344) ===
    (0x0801e368, 0x0000e0ff, 'DISPCNT_BG_OBJ_CLEAR_MASK',
     'tick_blend_fadein_and_poll_done_dispcnt_mask',
     'DISPCNT AND mask: clear bits[12:8] (BG0-BG3+OBJ enable)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # === gFontJpCtx (ewram.inc, 0x02006ed0) ===
    (0x0801dc28, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_desc_page_vram_ptr_gfontjpctx_a', None),
    (0x0801dca4, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_desc_page_vram_ptr_gfontjpctx_b', None),
    (0x0801dd04, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_desc_page_vram_ptr_gfontjpctx_c', None),
    (0x0801dd9c, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_desc_page_vram_ptr_gfontjpctx_d', None),
    (0x0801de30, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_desc_page_vram_ptr_gfontjpctx_e', None),
    (0x0801de84, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_to_desc_page_vram_ptr_gfontjpctx_f', None),
    (0x0801e0e8, 0x02006ed0, 'gFontJpCtx',
     'render_card_description_text_ptr_gfontjpctx', None),

    # === EWRAM_BASE (gba_mem.inc, 0x02000000) ===
    (0x0801dc2c, 0x02000000, 'EWRAM_BASE',
     'render_card_name_to_desc_page_vram_ewram_base_a', None),
    (0x0801dc9c, 0x02000000, 'EWRAM_BASE',
     'render_card_name_to_desc_page_vram_ewram_base_b', None),
    (0x0801dd94, 0x02000000, 'EWRAM_BASE',
     'render_card_name_to_desc_page_vram_ewram_base_c', None),
    (0x0801e0ec, 0x02000000, 'EWRAM_BASE',
     'render_card_description_text_ewram_base', None),

    # === GSETTINGS_OFFSET (name_input.inc, 0x00006c2c) ===
    (0x0801dc30, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_name_to_desc_page_vram_gsettings_off_a', None),
    (0x0801dca0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_name_to_desc_page_vram_gsettings_off_b', None),
    (0x0801dd98, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_name_to_desc_page_vram_gsettings_off_c', None),
    (0x0801e0f0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_description_text_gsettings_off', None),

    # === gCardInfoPageState (ewram.inc, 0x0201afb0) ===
    (0x0801dc34, 0x0201afb0, 'gCardInfoPageState',
     'render_card_name_to_desc_page_vram_ptr_gcardinfopagestate_a', None),
    (0x0801dd90, 0x0201afb0, 'gCardInfoPageState',
     'render_card_name_to_desc_page_vram_ptr_gcardinfopagestate_b', None),
    (0x0801df50, 0x0201afb0, 'gCardInfoPageState',
     'render_card_name_to_desc_page_vram_ptr_gcardinfopagestate_c', None),
    (0x0801df98, 0x0201afb0, 'gCardInfoPageState',
     'render_card_name_to_desc_page_vram_ptr_gcardinfopagestate_d', None),
    (0x0801dfd0, 0x0201afb0, 'gCardInfoPageState',
     'tick_scroll_frame_and_update_pos_ptr_gcardinfopagestate', None),
    (0x0801e0f8, 0x0201afb0, 'gCardInfoPageState',
     'render_card_description_text_ptr_gcardinfopagestate', None),
    (0x0801e190, 0x0201afb0, 'gCardInfoPageState',
     'card_info_page_finalize_ptr_gcardinfopagestate_a', None),
    (0x0801e280, 0x0201afb0, 'gCardInfoPageState',
     'card_info_page_finalize_ptr_gcardinfopagestate_b', None),

    # === gPrng (iwram.inc, 0x03000040) ===
    (0x0801dffc, 0x03000040, 'gPrng',
     'tick_scroll_frame_and_update_pos_ptr_gprng', None),
    (0x0801df54, 0x03000040, 'gPrng',
     'render_card_name_to_desc_page_vram_ptr_gprng_a', None),
    (0x0801df9c, 0x03000040, 'gPrng',
     'render_card_name_to_desc_page_vram_ptr_gprng_b', None),

    # === sjis_char_fold_table (carve label, 0x09e589c4) ===
    (0x0801dd0c, 0x09e589c4, 'sjis_char_fold_table',
     'render_card_name_to_desc_page_vram_ptr_sjis_fold_a', None),
    (0x0801de8c, 0x09e589c4, 'sjis_char_fold_table',
     'render_card_name_to_desc_page_vram_ptr_sjis_fold_b', None),

    # === card_attr_order_table (new carve, 0x09e4f204) ===
    (0x0801e284, 0x09e4f204, 'card_attr_order_table',
     'card_info_page_finalize_ptr_card_attr_order_table',
     '32 u32 card attr flag IDs indexed by display slot'),

    # === card_type_alt_display_table (new carve, 0x09e58ac4) ===
    (0x0801e288, 0x09e58ac4, 'card_type_alt_display_table',
     'card_info_page_finalize_ptr_card_type_alt_display_table',
     'card type/display index mapping table (u16 pairs, 1 ref)'),

    # === card_status_sprite_sheet (new carve, 0x09e2ddb4) ===
    (0x0801e290, 0x09e2ddb4, 'card_status_sprite_sheet',
     'card_info_page_finalize_ptr_card_status_sprite_sheet',
     '32+1 card status OBJ sprite items, 0x100B each'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # Fn-6: blit_glyph_2x2_to_bg_vram -- BG_CHAR_VRAM_CB2 already in gba_mem.inc
    (0x0801e318, 'blit_glyph_2x2_to_bg_vram_bg_char_vram_cb2',
     'BG charblock 2 base (GBA_VRAM_BASE+0x4000) = BG_CHAR_VRAM_CB2'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: (func_addr, old_name, new_name)
# ---------------------------------------------------------------------------
FUNC_RENAME = [
    (0x0801dbdc, 'card_info_page_step_03_unknown', 'render_card_name_to_desc_page_vram'),
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (func_addr, new_plate_ascii_text)
#    Full rewrite for CJK->ASCII conversion; all text pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # Fn-1: card_image_decode_wrapper
    (0x0801d998,
     '@ Loads card image tiles and frame graphics for the card info page.\n'
     '@ r0=card_id (u16), r1=pal_offset (stored sp+4), r2=atk_stat (stored sp+8).\n'
     '@ Reads card_stats_table (stride=11 hwords): field[7]=card_subtype(r4), field[6]=unk,\n'
     '@   field[9]=level(r7).\n'
     '@ Calls load_pack_tile_and_map_to_vram x2 (bg_vram=0xc000/0x6000000, param=0x020e).\n'
     '@ Calls decode_card_image_6bpp(vram=0x06000000<<0x13, pal=0x10, card_id, mode=2).\n'
     '@ Branches on r4 (card_subtype): r4<=20 -> monster frame; r4==22 -> spell frame;\n'
     '@   r4==23 -> spell-alt frame; else skip frame.\n'
     '@ Each frame path: resolve_card_type_icon_ptr(card_id), copy palette+tiles to PALRAM/VRAM,\n'
     '@   draw_card_name_label_to_vram, copy ATK/DEF stat glyphs.\n'
     '@ Calls draw_atk_def_label_to_vram(pal_offset, atk_stat).\n'
     '@ Returns void (Pattern B).'),

    # Fn-2: render_card_name_to_desc_page_vram (was card_info_page_step_03_unknown)
    (0x0801dbdc,
     '@ Renders card name text to the description page glyph line buffer.\n'
     '@ Reads gCardInfoPageState+0x0 bit0 to select charset:\n'
     '@   bit0==1 -> resolve_card_gfx_pointer_by_type (card_id bits[17:15] field[0xf]);\n'
     '@   bit0==0 -> select_charset_then_load_name (card_id, lang bits[2:0] of gSettings).\n'
     '@ Calculates total pixel width via char_width_wide_10_or_12 or char_width_narrow_5.\n'
     '@ Sets gFontJpCtx[+0x8] mode_flags and gFontJpCtx[+0x4] fn_ptr from font_jp_base_table.\n'
     '@ Renders each glyph via render_glyph_jp_dual_layer (wide) or render_glyph_jp_single_layer.\n'
     '@ Flushes line buffer: zero_fill_by_halfword(0x06007100, 0x80 hwords),\n'
     '@   commit_line_buffer_to_sprite_vram(0x06007100, 0).\n'
     '@ If sp[0]!=0 (scrolled page): writes tile-index sequences to BG VRAM 0x06000800\n'
     '@   and 0x06000c80 using gPrng+0x1e2 as stride, clears gCardInfoPageState[+0x18/+0x1c].\n'
     '@ indeg=2: card_info_page_entry (0x0801e456) + update_card_info_page_state (0x0801e42e).\n'
     '@ Returns void (Pattern B).'),

    # Fn-3: tick_scroll_frame_and_update_pos
    (0x0801dfa0,
     '@ Updates card description page scroll position each frame (called by card info scene).\n'
     '@ Reads gCardInfoPageState[+0x14] (frame_counter, r1). If r1 > 0xe8:\n'
     '@   Increments gCardInfoPageState[+0x1c] (sub_counter) modulo (r1-0xe8)*2+0xd2.\n'
     '@   If sub_counter in [0x5a..(r1-0xe8)*2+0x5a]: computes scroll_y = (sub_counter-0x5a)/2.\n'
     '@   Writes scroll_y to gCardInfoPageState[+0x18] (scroll_pixel_y_offset).\n'
     '@   Writes scroll_y to gPrng+0x1e2 (IWRAM BG3VOFS shadow, hw scroll register).\n'
     '@ If r1 <= 0xe8: clears [+0x18] and [+0x1c] (stop scroll).\n'
     '@ indeg=1; caller: tick_card_info_page_by_state (0x0801e714).\n'
     '@ Returns void (Pattern B, pop {r4}; pop {r0}; bx r0).'),

    # Fn-4: render_card_description_text
    (0x0801e000,
     '@ Renders card description text to OBJ VRAM (card info page, description sub-page).\n'
     '@ Reads gSettings (EWRAM_BASE+GSETTINGS_OFFSET) bits[2:0] (lang) to select charset.\n'
     '@ Sets gFontJpCtx[+0x8] mode_flags and fn_ptr from font_jp_base_table.\n'
     '@ Calls setup_line_buf_with_font_and_align(x=0x10, y=0x3a, align=1, font=1).\n'
     '@ Sets gFontJpCtx[+0x15] active flag bit5 (0x40).\n'
     '@ Calls text_render_wrapper(mode, 2, 7, r3) up to 2 times (normal + overflow path).\n'
     '@ Writes scroll fields: gCardInfoPageState[+0x24] = line_count+2,\n'
     '@   gCardInfoPageState[+0x20] = 0 (reset scroll).\n'
     '@ Calls commit_line_buffer_to_sprite_vram(0x06010040, 0).\n'
     '@ Returns void.'),

    # Fn-5: card_info_page_finalize
    (0x0801e100,
     '@ Loads card frame graphics and card flag icons for the card info page finalize step.\n'
     '@ r0=card_id (u16). Reads card_stats_table row (stride=11 hwords):\n'
     '@   field[7]=subtype(r4), field[6]=subtype_b(r5), field[9]=level(r6),\n'
     '@   field[8]=card_type_index(r0 at entry).\n'
     '@ Reads gCardInfoPageState[+0x0] to mask bits[7:2] (clears type/flag fields).\n'
     '@ If subtype in [22..23] (Spell/Spell-alt): loads icon palette/tiles to\n'
     '@   CARD_FRAME_OBJ_PAL_LEVEL(0x05000380) and CARD_SPELL_OBJ_TILE_BASE(0x06017500).\n'
     '@ Otherwise: loads alternate icon palette/tiles.\n'
     '@ Loop r5=0..0x1f: reads card_attr_order_table[r5] (card type flag ID),\n'
     '@   calls test_card_flag_bit(card_id, flag_id). On match:\n'
     '@   loads 0x100 bytes from card_status_sprite_sheet[r5*0x100] to\n'
     '@   card_type_alt_display_table offset and CARD_ICON_OBJ_TILE_BASE(0x06017580).\n'
     '@   Updates gCardInfoPageState flag nibble bits[5:2].\n'
     '@ Returns void (Pattern B).'),

    # Fn-7: tick_blend_fadeout_and_set_dispcnt
    (0x0801e328,
     '@ Sets DISPCNT bits[12:8] (BG0-BG3+OBJ enable) via OR with 0x1f00, then calls\n'
     '@ tick_blend_step_by_delta(delta=4) to advance the blend fade-out by 4 steps.\n'
     '@ Returns tick_blend_step_by_delta result: 1=fade complete, 0=in progress.\n'
     '@ indeg=1; caller: tick_card_info_page_by_state (0x0801e714).'),

    # Fn-8: tick_blend_fadein_and_poll_done
    (0x0801e344,
     '@ Calls start_blend_fadein_with_target(target=4) each frame to step the blend fade-in.\n'
     '@ If fade-in complete (returns 1): ANDs DISPCNT with DISPCNT_BG_OBJ_CLEAR_MASK (0xe0ff)\n'
     '@   to clear bits[12:8] (BG0-BG3+OBJ enable), then returns 1.\n'
     '@ If not complete: returns 0.\n'
     '@ indeg=2; callers: tick_card_info_page_by_state (0x0801e714), advance_pack_fadein_to_card_info (0x080fa3a8).'),
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

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return 1

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

def _apply_func_rename(func_addr, old_name, new_name):
    a = _addr(func_addr)
    fn = currentProgram.getFunctionManager().getFunctionAt(a)
    if fn is None:
        print("[WARN] FUNC_RENAME 0x%08x: no function found" % func_addr)
        return 0
    current = fn.getName()
    if DRY:
        print("[dry] FUNC_RENAME 0x%08x  %s -> %s" % (func_addr, current, new_name))
        return 1
    fn.setName(new_name, SourceType.USER_DEFINED)
    print("[FRN] 0x%08x  %s -> %s" % (func_addr, current, new_name))
    return 1

def _apply_plate(func_addr, new_plate_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] PLATE 0x%08x: no code unit" % func_addr)
        return 0
    if DRY:
        print("[dry] PLATE 0x%08x: rewrite to ASCII (%d chars)" % (func_addr, len(new_plate_text)))
        return 1
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: plate set (%d chars)" % (func_addr, len(new_plate_text)))
    return 1

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF01Seg3Slots (DRY=%s) ===" % DRY)
    print("  f01-Seg-3: 0x0801d998..0x0801e36c, 8 fn, card_info scene")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        eq_ok += _apply_eq(slot_addr, value, eq_name, slot_label, eol)
    print("  EQ done: %d / %d" % (eq_ok, len(EQ_SLOTS)))

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        ref_ok += _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
    print("  REF done: %d / %d" % (ref_ok, len(REF_SLOTS)))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        ren_ok += _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d / %d" % (ren_ok, len(RENAME_SLOTS)))

    # D. FUNC_RENAME
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAME))
    frn_ok = 0
    for func_addr, old_name, new_name in FUNC_RENAME:
        frn_ok += _apply_func_rename(func_addr, old_name, new_name)
    print("  FUNC_RENAME done: %d / %d" % (frn_ok, len(FUNC_RENAME)))

    # E. PLATE_REWRITES
    print("\n--- E. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plt_ok = 0
    for func_addr, new_plate in PLATE_REWRITES:
        plt_ok += _apply_plate(func_addr, new_plate)
    print("  PLATE done: %d / %d" % (plt_ok, len(PLATE_REWRITES)))

    print("\n=== RefineF01Seg3Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  FUNC_RENAME=%d  PLATE=%d" % (
        eq_ok, ref_ok, ren_ok, frn_ok, plt_ok))

main()
