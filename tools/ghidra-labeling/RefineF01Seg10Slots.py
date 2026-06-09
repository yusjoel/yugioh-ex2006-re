# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg10Slots.py -- f01 Seg-10 [0x08028bdc..0x0802c238)
#   Campaign victory / puzzle LP / pack card info display (13 functions)
#   EQ=82 (66 reuse + 16 new) REF=1 RENAME=48 PLATE=13
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (66 reuse + 16 new)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename
#   C. RENAME_SLOTS -- plain rename (no EOL needed; ASCII)
#   D. PLATE_REPL -- stale FUN_ -> current name in plate comments (pure ASCII)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython UTF-8 red line.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass


# ---------------------------------------------------------------------------
# A: EQ_SLOTS (slot_addr, value, const_name, slot_label)
#    EQ_REUSE (66) -- already defined in constants/*.inc
#    EQ_NEW   (16) -- new, added to constants/duel_field.inc and gba_mem.inc
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- EQ_REUSE: evaluate_campaign_victory_state ---
    (0x08028c24, 0x0201e2a0, 'gDuelCardCtxBase',
     'evaluate_campaign_victory_state_ctx_base'),
    (0x08028c28, 0x02023360, 'gDuelSceneBase',
     'evaluate_campaign_victory_state_scene_base'),
    (0x08028c64, 0x03000040, 'gPrng',
     'evaluate_campaign_victory_state_gprng'),
    (0x08028c68, 0x0000023f, 'GPRNG_BANNER_FLAG_OFF',
     'evaluate_campaign_victory_state_win_count_off'),
    (0x08028d0c, 0x0000023f, 'GPRNG_BANNER_FLAG_OFF',
     'evaluate_campaign_victory_state_win_count_off_b'),

    # --- EQ_NEW: evaluate_campaign_victory_state ---
    (0x08028c6c, 0x00000241, 'GPRNG_CHALLENGE_SCORE_OFF',
     'evaluate_campaign_victory_state_score_off'),
    (0x08028d10, 0x00000241, 'GPRNG_CHALLENGE_SCORE_OFF',
     'evaluate_campaign_victory_state_score_off_b'),

    # --- EQ_REUSE: dispatch_campaign_scene_by_prng_state ---
    (0x08028d6c, 0x03000040, 'gPrng',
     'dispatch_campaign_scene_by_prng_state_gprng'),
    (0x08028d70, 0x00000202, 'GPRNG_STEP_IDX_OFF',
     'dispatch_campaign_scene_by_prng_state_step_idx_off'),

    # --- EQ_REUSE: load_campaign_state_post_sio ---
    (0x0802b480, 0x0201e2a0, 'gDuelCardCtxBase',
     'load_campaign_state_post_sio_ctx_base'),

    # --- EQ_REUSE: render_card_name_centered_to_sprite_vram ---
    (0x0802b578, 0x02006ed0, 'gFontJpCtx',
     'render_card_name_centered_to_sprite_vram_font_ctx'),
    (0x0802b57c, 0x02000000, 'EWRAM_BASE',
     'render_card_name_centered_to_sprite_vram_ewram_base'),
    (0x0802b580, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_card_name_centered_to_sprite_vram_settings_off'),

    # --- EQ_NEW: render_card_name_centered_to_sprite_vram ---
    (0x0802b588, 0x060053c0, 'PACK_CARD_INFO_SPRITE_VRAM',
     'render_card_name_centered_to_sprite_vram_commit_tgt'),
    (0x0802b58c, 0x06000812, 'PACK_CARD_INFO_TILEMAP_ADDR',
     'render_card_name_centered_to_sprite_vram_tilemap'),

    # --- EQ_REUSE: init_pack_card_info_screen_vram gprng ---
    (0x0802b6c8, 0x03000040, 'gPrng',
     'init_pack_card_info_screen_vram_gprng'),

    # --- EQ_NEW: init_pack_card_info_screen_vram ---
    (0x0802b6cc, 0x00000401, 'PACK_INFO_DISPCNT_SHADOW_INIT',
     'init_pack_card_info_screen_vram_dispcnt_shadow'),

    # --- EQ_REUSE: init_pack_card_info_screen_vram ---
    (0x0802b6d0, 0x0203eeb0, 'gDuelDispCtx',
     'init_pack_card_info_screen_vram_disp_ctx'),
    (0x0802b6d4, 0x02029eb0, 'gVijaState',
     'init_pack_card_info_screen_vram_vija_state'),

    # --- EQ_NEW: init_pack_card_info_screen_vram ---
    (0x0802b6dc, 0x0000820a, 'PACK_INFO_BG2CNT_INIT',
     'init_pack_card_info_screen_vram_bg2cnt_init'),

    # --- EQ_REUSE: init_pack_card_info_screen_vram ---
    (0x0802b6e0, 0x00000407, 'CARD_INFO_BG2CNT_INIT',
     'init_pack_card_info_screen_vram_bg3cnt_init'),
    (0x0802b6e4, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'init_pack_card_info_screen_vram_obj_vram_clr'),
    (0x0802b6e8, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'init_pack_card_info_screen_vram_bg_tile_clr'),
    (0x0802b6ec, 0x05000220, 'OBJ_PAL_SLOT_1',
     'init_pack_card_info_screen_vram_pal_src'),

    # --- EQ_NEW: init_pack_card_info_screen_vram text_mode a ---
    (0x0802b714, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'init_pack_card_info_screen_vram_text_mode_a'),

    # --- EQ_REUSE: init_pack_card_info_screen_vram font_ctx_a ---
    (0x0802b704, 0x02006ed0, 'gFontJpCtx',
     'init_pack_card_info_screen_vram_font_ctx_a'),
    (0x0802b708, 0x02000000, 'EWRAM_BASE',
     'init_pack_card_info_screen_vram_ewram_base'),
    (0x0802b70c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_pack_card_info_screen_vram_settings_off'),

    # --- EQ_REUSE: init_pack_card_info_screen_vram font_ctx_b ---
    (0x0802b800, 0x02006ed0, 'gFontJpCtx',
     'init_pack_card_info_screen_vram_font_ctx_b'),
    (0x0802b804, 0x02000000, 'EWRAM_BASE',
     'init_pack_card_info_screen_vram_ewram_base_b'),
    (0x0802b808, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_pack_card_info_screen_vram_settings_off_b'),

    # --- EQ_NEW: init_pack_card_info_screen_vram text_mode_b + sprite_vram_b ---
    (0x0802b810, 0x00008001, 'TEXT_RENDER_COLOR_MODE_1',
     'init_pack_card_info_screen_vram_text_mode_b'),
    (0x0802b814, 0x06004c40, 'PACK_INFO_NAME_SPRITE_VRAM_B',
     'init_pack_card_info_screen_vram_sprite_vram_b'),

    # --- EQ_REUSE: init_pack_card_info_screen_vram scene_base + bg_vram_a ---
    (0x0802b818, 0x02023360, 'gDuelSceneBase',
     'init_pack_card_info_screen_vram_scene_base'),
    (0x0802b81c, 0x06000800, 'CARD_DESC_BG_VRAM_A',
     'init_pack_card_info_screen_vram_bg_vram_a'),

    # --- EQ_REUSE: render_puzzle_lp_digit_sprites ---
    (0x0802b8b0, 0x02023360, 'gDuelSceneBase',
     'render_puzzle_lp_digit_sprites_scene_base'),
    (0x0802b8b4, 0x03000040, 'gPrng',
     'render_puzzle_lp_digit_sprites_gprng'),

    # --- EQ_NEW: render_puzzle_lp_digit_sprites ---
    (0x0802b8b8, 0x00001008, 'PUZZLE_LP_DIGIT_TILE_BASE',
     'render_puzzle_lp_digit_sprites_tile_base'),

    # --- EQ_REUSE: init_puzzle_card_name_line_buf ---
    (0x0802b928, 0x02006ed0, 'gFontJpCtx',
     'init_puzzle_card_name_line_buf_font_ctx'),
    (0x0802b92c, 0x02000000, 'EWRAM_BASE',
     'init_puzzle_card_name_line_buf_ewram_base'),
    (0x0802b930, 0x00006c2c, 'GSETTINGS_OFFSET',
     'init_puzzle_card_name_line_buf_settings_off'),

    # --- EQ_NEW: init_puzzle_card_name_line_buf ---
    (0x0802b938, 0x050001e0, 'BG_PALRAM_SLOT15_BASE',
     'init_puzzle_card_name_line_buf_pal_clear_base'),

    # --- EQ_REUSE: init_puzzle_card_name_line_buf scene_base ---
    (0x0802b93c, 0x02023360, 'gDuelSceneBase',
     'init_puzzle_card_name_line_buf_scene_base'),

    # --- EQ_REUSE: render_game_string_with_number ---
    (0x0802b9b0, 0x02023360, 'gDuelSceneBase',
     'render_game_string_with_number_scene_base'),
    (0x0802b9b4, 0x02006ed0, 'gFontJpCtx',
     'render_game_string_with_number_font_ctx'),
    (0x0802b9e8, 0x02000000, 'EWRAM_BASE',
     'render_game_string_with_number_ewram_base'),
    (0x0802b9ec, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_game_string_with_number_settings_off'),
    (0x0802ba58, 0x02023360, 'gDuelSceneBase',
     'render_game_string_with_number_scene_base_b'),
    (0x0802ba5c, 0x02000000, 'EWRAM_BASE',
     'render_game_string_with_number_ewram_base_b'),
    (0x0802ba60, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_game_string_with_number_settings_off_b'),
    (0x0802babc, 0x02000000, 'EWRAM_BASE',
     'render_game_string_with_number_ewram_base_c'),
    (0x0802bac0, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_game_string_with_number_settings_off_c'),
    (0x0802bb2c, 0x02023360, 'gDuelSceneBase',
     'render_game_string_with_number_scene_base_c'),
    (0x0802bb30, 0x02000000, 'EWRAM_BASE',
     'render_game_string_with_number_ewram_base_d'),
    (0x0802bb34, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_game_string_with_number_settings_off_d'),
    (0x0802bc60, 0x02023360, 'gDuelSceneBase',
     'render_game_string_with_number_scene_base_d'),
    (0x0802bc6c, 0x02006ed0, 'gFontJpCtx',
     'render_game_string_with_number_font_ctx_e'),
    (0x0802bc80, 0x02000000, 'EWRAM_BASE',
     'render_game_string_with_number_ewram_base_e'),
    (0x0802bc84, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_game_string_with_number_settings_off_e'),

    # --- EQ_REUSE: render_card_stat_with_number_alt ---
    (0x0802bd58, 0x02023360, 'gDuelSceneBase',
     'render_card_stat_with_number_alt_scene_base'),
    (0x0802bd5c, 0x02006ed0, 'gFontJpCtx',
     'render_card_stat_with_number_alt_font_ctx'),

    # --- EQ_REUSE: dispatch_puzzle_display_mode ---
    (0x0802be54, 0x02023360, 'gDuelSceneBase',
     'dispatch_puzzle_display_mode_scene_base_a'),
    (0x0802bf14, 0x02023360, 'gDuelSceneBase',
     'dispatch_puzzle_display_mode_scene_base_b'),
    (0x0802bf18, 0xfffffc1f, 'GPRNG_FIELD_ANIM_MASK',
     'dispatch_puzzle_display_mode_mode_clear_mask_a'),
    (0x0802bfe4, 0xfffffc1f, 'GPRNG_FIELD_ANIM_MASK',
     'dispatch_puzzle_display_mode_mode_clear_mask_b'),
    (0x0802c1bc, 0x02023360, 'gDuelSceneBase',
     'dispatch_puzzle_display_mode_scene_base_c'),
    (0x0802be40, 0x03000040, 'gPrng',
     'dispatch_puzzle_display_mode_gprng_a'),
    (0x0802be44, 0x00000203, 'GPRNG_FRAME_CTRL_OFF_203',
     'dispatch_puzzle_display_mode_frame_ctrl_off_a'),
    (0x0802bf1c, 0x03000040, 'gPrng',
     'dispatch_puzzle_display_mode_gprng_b'),
    (0x0802bf20, 0x00000203, 'GPRNG_FRAME_CTRL_OFF_203',
     'dispatch_puzzle_display_mode_frame_ctrl_off_b'),
    (0x0802bfe8, 0x03000040, 'gPrng',
     'dispatch_puzzle_display_mode_gprng_c'),
    (0x0802bfec, 0x00000203, 'GPRNG_FRAME_CTRL_OFF_203',
     'dispatch_puzzle_display_mode_frame_ctrl_off_c'),
    (0x0802c06c, 0x00000203, 'GPRNG_FRAME_CTRL_OFF_203',
     'dispatch_puzzle_display_mode_frame_ctrl_off_d'),
    (0x0802c19c, 0x03000040, 'gPrng',
     'dispatch_puzzle_display_mode_gprng_d'),
    (0x0802c1a0, 0x00000203, 'GPRNG_FRAME_CTRL_OFF_203',
     'dispatch_puzzle_display_mode_frame_ctrl_off_e'),
    (0x0802c1e8, 0x03000040, 'gPrng',
     'dispatch_puzzle_display_mode_gprng_e'),

    # --- EQ_NEW: dispatch_puzzle_display_mode LP constants ---
    (0x0802c0d4, 0x00002710, 'PUZZLE_LP_MAX',
     'dispatch_puzzle_display_mode_lp_max'),
    (0x0802c0d8, 0xffffd8f0, 'PUZZLE_LP_NEG_10000',
     'dispatch_puzzle_display_mode_lp_neg_10000'),
    (0x0802c0f8, 0xfffffc18, 'PUZZLE_LP_STEP_1000',
     'dispatch_puzzle_display_mode_lp_step_1000'),

    # --- EQ_NEW: zero_sprite_vram_with_tile_seq ---
    (0x0802bdbc, 0x06001440, 'PUZZLE_TILEMAP_SCRATCH',
     'zero_sprite_vram_with_tile_seq_tilemap_scratch'),
    (0x0802bdc0, 0x06008020, 'PUZZLE_NAME_SPRITE_VRAM',
     'zero_sprite_vram_with_tile_seq_sprite_vram'),
]

# ---------------------------------------------------------------------------
# B: REF_SLOTS (slot_addr, target_vaddr, gas_label, slot_label)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- dispatch table pointer ---
    (0x08028d74, 0x08028d78, 'campaign_scene_prng_dispatch_table',
     'dispatch_campaign_scene_by_prng_state_table_ptr'),
]

# ---------------------------------------------------------------------------
# C: RENAME_SLOTS (slot_addr, label, eol_or_None)
#    Plain rename + optional EOL (ASCII only).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # dispatch_campaign_scene_by_prng_state
    (0x08028d78, 'campaign_scene_prng_dispatch_table', None),

    # render_card_name_centered_to_sprite_vram
    (0x0802b584, 'render_card_name_centered_to_sprite_vram_font_table', None),

    # init_pack_card_info_screen_vram
    (0x0802b6d8, 'init_pack_card_info_screen_vram_bg0cnt', None),
    (0x0802b6f0, 'init_pack_card_info_screen_vram_pack_pal_src', None),
    (0x0802b6f4, 'init_pack_card_info_screen_vram_pack_tile_a', None),
    (0x0802b6f8, 'init_pack_card_info_screen_vram_pack_tile_b', None),
    (0x0802b6fc, 'init_pack_card_info_screen_vram_pack_tile_c', None),
    (0x0802b700, 'init_pack_card_info_screen_vram_pack_tile_d', None),
    (0x0802b710, 'init_pack_card_info_screen_vram_font_table_a', None),
    (0x0802b80c, 'init_pack_card_info_screen_vram_font_table_b', None),
    (0x0802b820, 'init_pack_card_info_screen_vram_font_gfx_base', None),
    (0x0802b824, 'init_pack_card_info_screen_vram_font_gfx_off', None),
    (0x0802b82c, 'init_pack_card_info_screen_vram_str_lang4', None),
    (0x0802b834, 'init_pack_card_info_screen_vram_str_lang3', None),
    (0x0802b83c, 'init_pack_card_info_screen_vram_str_lang2', None),
    (0x0802b850, 'init_pack_card_info_screen_vram_str_lang1', None),

    # init_puzzle_card_name_line_buf
    (0x0802b934, 'init_puzzle_card_name_line_buf_font_table', None),

    # render_game_string_with_number
    (0x0802b9f0, 'render_game_string_with_number_str_b_base', None),
    (0x0802b9f4, 'render_game_string_with_number_str_b_off', None),
    (0x0802b9fc, 'render_game_string_with_number_str_lang4', None),
    (0x0802ba04, 'render_game_string_with_number_str_lang3', None),
    (0x0802ba0c, 'render_game_string_with_number_str_lang2', None),
    (0x0802ba54, 'render_game_string_with_number_str_lang1', None),
    (0x0802ba64, 'render_game_string_with_number_str_b_base_b', None),
    (0x0802ba68, 'render_game_string_with_number_str_b_off_b', None),
    (0x0802ba70, 'render_game_string_with_number_str_lang4_b', None),
    (0x0802ba78, 'render_game_string_with_number_str_lang3_b', None),
    (0x0802ba80, 'render_game_string_with_number_str_lang2_b', None),
    (0x0802ba90, 'render_game_string_with_number_str_lang1_b', None),
    (0x0802bac4, 'render_game_string_with_number_str_c_base', None),
    (0x0802bac8, 'render_game_string_with_number_str_c_off', None),
    (0x0802bad0, 'render_game_string_with_number_str_c_lang4', None),
    (0x0802bad8, 'render_game_string_with_number_str_c_lang3', None),
    (0x0802bae0, 'render_game_string_with_number_str_c_lang2', None),
    (0x0802bb28, 'render_game_string_with_number_str_c_lang1', None),
    (0x0802bb38, 'render_game_string_with_number_str_d_base', None),
    (0x0802bb3c, 'render_game_string_with_number_str_d_off', None),
    (0x0802bb44, 'render_game_string_with_number_str_d_lang4', None),
    (0x0802bb4c, 'render_game_string_with_number_str_d_lang3', None),
    (0x0802bb54, 'render_game_string_with_number_str_d_lang2', None),
    (0x0802bb64, 'render_game_string_with_number_str_d_lang1', None),
    (0x0802bc64, 'render_game_string_with_number_line_pos_ptr', None),
    (0x0802bc68, 'render_game_string_with_number_glyph_spc_tbl', None),
    (0x0802bc70, 'render_game_string_with_number_font_table', None),
    (0x0802bc74, 'render_game_string_with_number_str_id_off', None),
    (0x0802bc78, 'render_game_string_with_number_str_ptr_tbl', None),
    (0x0802bc7c, 'render_game_string_with_number_str_ja_base', None),

    # render_card_stat_with_number_alt
    (0x0802bd60, 'render_card_stat_with_number_alt_line_pos_ptr', None),
]

# ---------------------------------------------------------------------------
# D: PLATE_REPL -- stale FUN_ -> current name (13 functions, pure ASCII)
#    Each entry: fn_addr -> [(old_str, new_str), ...]
#    IMPORTANT: Use exact substrings. FUN_0802bb74/bb68 are LAB_ internal
#    branches mis-labelled as functions; replace with LAB_ form.
# ---------------------------------------------------------------------------
PLATE_REPL = {
    0x0802b484: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
    0x0802b590: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
    0x0802b854: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
        (u'FUN_0802bdc4', u'tick_lp_display_and_blend_step'),
        (u'FUN_0802bde4', u'tick_lp_display_and_fadein_check'),
    ],
    0x0802b940: [
        (u'FUN_0802bb74', u'LAB_0802bb74'),
        (u'FUN_0802bb68', u'LAB_0802bb68'),
    ],
    0x0802bc88: [
        (u'FUN_0802b940', u'render_game_string_with_number'),
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
    0x0802bd64: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
    0x0802bdc4: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
    0x0802bde4: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
    0x0802be08: [
        (u'FUN_0801fec0', u'run_duel_puzzle_scene_state_machine'),
    ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF01Seg10Slots (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
    made = set()

    # --- A: EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (equate=%s)" % (slot_int, err, cname))
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # --- B: REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int)
            continue
        if DRY:
            print("[B dry] 0x%08x ref->%s rename %s" % (slot_int, gas_label, slot_label))
            nB += 1
            continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s" % (slot_int, slot_label))
        nB += 1

    # --- C: RENAME_SLOTS ---
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int)
            continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label))
            nC += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label))
        nC += 1

    # --- D: PLATE_REPL (stale name fix) ---
    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[D FAIL] no plate @ 0x%08x" % addr_int)
            continue
        new = txt
        n_applied = 0
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[D skip] 0x%08x pattern not present (ok): %r" % (addr_int, old[:40]))
                continue
            new = new.replace(old, rep)
            n_applied += 1
        if n_applied == 0 or new == txt:
            print("[D noop] 0x%08x no replacements applied" % addr_int)
            continue
        if DRY:
            print("[D dry] 0x%08x plate update (%d repl)" % (addr_int, n_applied))
            nD += 1
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[D ok] 0x%08x plate updated (%d repl)" % (addr_int, n_applied))
        nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))


main()
