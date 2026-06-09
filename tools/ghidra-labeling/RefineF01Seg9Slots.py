# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg9Slots.py -- f01 Seg-9 [0x08027e44..0x08028bdc)
#   Campaign card-select handlers (0..15) + pack scene init/render
#   EQ=76 (58 reuse + 18 new) REF=14 RENAME=13 PLATE_STALE=28

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
#    EQ_REUSE (58) -- already defined in constants/*.inc
#    EQ_NEW   (18) -- new, added to constants/duel_field.inc
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- EQ_REUSE: handler_0 ---
    (0x08027f3c, 0x03000040, 'gPrng',                    'run_campaign_card_select_handler_0_gprng'),
    (0x08027f40, 0x00000202, 'GPRNG_STEP_IDX_OFF',       'run_campaign_card_select_handler_0_step_off'),
    (0x08027f44, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'run_campaign_card_select_handler_0_step_mask'),
    # --- EQ_REUSE: handler_1 ---
    (0x08027fb8, 0x03000040, 'gPrng',                    'run_campaign_card_select_handler_1_gprng'),
    (0x08027fbc, 0x02023360, 'gDuelSceneBase',            'run_campaign_card_select_handler_1_scene_base'),
    (0x08027fc4, 0x00000202, 'GPRNG_STEP_IDX_OFF',       'run_campaign_card_select_handler_1_step_off'),
    (0x08027fc8, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'run_campaign_card_select_handler_1_step_mask'),
    # --- EQ_REUSE: handler_2 ---
    (0x08028028, 0x02023360, 'gDuelSceneBase',            'run_campaign_card_select_handler_2_scene_base'),
    (0x08028030, 0x03000040, 'gPrng',                    'run_campaign_card_select_handler_2_gprng'),
    (0x08028034, 0x00000202, 'GPRNG_STEP_IDX_OFF',       'run_campaign_card_select_handler_2_step_off'),
    (0x08028038, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'run_campaign_card_select_handler_2_step_mask'),
    # --- EQ_REUSE: handler_4 ---
    (0x08028088, 0x02023360, 'gDuelSceneBase',            'run_campaign_card_select_handler_4_scene_base'),
    (0x0802808c, 0x0201e2a0, 'gDuelCardCtxBase',          'run_campaign_card_select_handler_4_card_ctx_base'),
    (0x08028090, 0x03000040, 'gPrng',                    'run_campaign_card_select_handler_4_gprng'),
    (0x08028094, 0x00000202, 'GPRNG_STEP_IDX_OFF',       'run_campaign_card_select_handler_4_step_off'),
    (0x080280a4, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'run_campaign_card_select_handler_4_step_mask_a'),
    (0x080280b8, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'run_campaign_card_select_handler_4_step_mask_b'),
    # --- EQ_REUSE: handler_3 ---
    (0x080280cc, 0x02023360, 'gDuelSceneBase',            'run_campaign_card_select_handler_3_scene_base'),
    # --- EQ_REUSE: handler_5 ---
    (0x08028114, 0x02023360, 'gDuelSceneBase',            'run_campaign_card_select_handler_5_scene_base'),
    # --- EQ_REUSE: handler_6 ---
    (0x0802818c, 0x02023360, 'gDuelSceneBase',            'run_campaign_card_select_handler_6_scene_base'),
    # --- EQ_REUSE: handler_7 ---
    (0x080281c8, 0x0201e2a0, 'gDuelCardCtxBase',          'run_campaign_card_select_handler_7_card_ctx_base'),
    (0x080281cc, 0x03000040, 'gPrng',                    'run_campaign_card_select_handler_7_gprng'),
    (0x080281d0, 0x00000202, 'GPRNG_STEP_IDX_OFF',       'run_campaign_card_select_handler_7_step_off'),
    (0x080281d4, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',      'run_campaign_card_select_handler_7_step_mask'),
    # --- EQ_REUSE: handler_9 ---
    (0x08028258, 0x02000000, 'EWRAM_BASE',                'run_campaign_card_select_handler_9_ewram_base'),
    (0x0802825c, 0x000053f0, 'GSETTINGS_FONT_TABLE_OFF',  'run_campaign_card_select_handler_9_chall_bits_off'),
    (0x08028260, 0x00001250, 'GSETTINGS_TEXT_FIELD_A_OFF','run_campaign_card_select_handler_9_sprite_ctx_off'),
    # --- EQ_REUSE: handler_10 ---
    (0x08028298, 0x0000ffff, 'OAM_ATTR0_HIDDEN',          'run_campaign_card_select_handler_10_oam_hidden'),
    # --- EQ_REUSE: handler_14 ---
    (0x080283ac, 0x02000000, 'EWRAM_BASE',                'run_campaign_card_select_handler_14_ewram'),
    (0x080283b8, 0x00006c3c, 'GPRNG_CHALLENGE_ENTRY_OFF', 'run_campaign_card_select_handler_14_challenge_entry_off'),
    # --- EQ_REUSE: render_campaign_text_line_centered ---
    (0x08028554, 0x02006ed0, 'gFontJpCtx',                'render_campaign_text_line_centered_font_ctx'),
    (0x08028558, 0x02000000, 'EWRAM_BASE',                'render_campaign_text_line_centered_ewram'),
    (0x0802855c, 0x00006c2c, 'GSETTINGS_OFFSET',          'render_campaign_text_line_centered_gsettings_off'),
    (0x08028564, 0x06004000, 'BG_CHAR_VRAM_CB2',          'render_campaign_text_line_centered_bg_vram'),
    # --- EQ_REUSE: render_campaign_text_line_with_align ---
    (0x08028680, 0x02006ed0, 'gFontJpCtx',                'render_campaign_text_line_with_align_font_ctx'),
    (0x08028684, 0x02000000, 'EWRAM_BASE',                'render_campaign_text_line_with_align_ewram'),
    (0x08028688, 0x00006c2c, 'GSETTINGS_OFFSET',          'render_campaign_text_line_with_align_gsettings_off'),
    (0x08028690, 0x06004000, 'BG_CHAR_VRAM_CB2',          'render_campaign_text_line_with_align_bg_vram'),
    # --- EQ_REUSE: init_pack_scene_vram_regs ---
    (0x08028704, 0x03000040, 'gPrng',                    'init_pack_scene_vram_regs_gprng'),
    (0x08028708, 0x00000601, 'DUEL_FIELD_CTRL_VAL',       'init_pack_scene_vram_regs_ctrl_val'),
    (0x0802870c, 0x0203eeb0, 'gDuelDispCtx',              'init_pack_scene_vram_regs_disp_ctx'),
    (0x08028710, 0x02029eb0, 'gVijaState',                'init_pack_scene_vram_regs_vija_state'),
    (0x08028714, 0x04000008, 'BG0CNT',                    'init_pack_scene_vram_regs_bg0cnt'),
    (0x08028718, 0x00000105, 'DUEL_FIELD_BGCNT1_INIT',    'init_pack_scene_vram_regs_bgcnt1'),
    (0x0802871c, 0x00000206, 'DUEL_FIELD_BGCNT2_INIT',    'init_pack_scene_vram_regs_bgcnt2'),
    (0x08028720, 0x00000307, 'DUEL_FIELD_BGCNT3_INIT',    'init_pack_scene_vram_regs_bgcnt3'),
    (0x08028724, 0x06004000, 'BG_CHAR_VRAM_CB2',          'init_pack_scene_vram_regs_vram_obj'),
    (0x08028728, 0x06010000, 'OBJ_TILE_VRAM_BASE',        'init_pack_scene_vram_regs_vram_bg'),
    # --- EQ_REUSE: load_pack_tiles_with_palette_init ---
    (0x08028794, 0x05000220, 'OBJ_PAL_SLOT_1',            'load_pack_tiles_with_palette_init_pal_dest'),
    (0x0802879c, 0x06010000, 'OBJ_TILE_VRAM_BASE',        'load_pack_tiles_with_palette_init_vram_bg'),
    (0x080287a4, 0x02023360, 'gDuelSceneBase',            'load_pack_tiles_with_palette_init_scene_base'),
    # --- EQ_REUSE: write_pack_strip_oam_entries ---
    (0x080287f8, 0x03000040, 'gPrng',                    'write_pack_strip_oam_entries_gprng'),
    # --- EQ_REUSE: tick_campaign_card_selector_oam ---
    (0x08028944, 0x03000040, 'gPrng',                    'tick_campaign_card_selector_oam_gprng_1'),
    (0x08028b28, 0x03000040, 'gPrng',                    'tick_campaign_card_selector_oam_gprng_2'),
    (0x08028898, 0x02023360, 'gDuelSceneBase',            'tick_campaign_card_selector_oam_scene_base_a'),
    (0x08028b34, 0x02023360, 'gDuelSceneBase',            'tick_campaign_card_selector_oam_scene_base_b'),
    (0x08028bd8, 0x02023360, 'gDuelSceneBase',            'tick_campaign_card_selector_oam_scene_base_c'),
    # --- EQ_REUSE: handler_2 (GFX_ATTR_CLEAR_BITS_8_7 reuse) ---
    (0x0802802c, 0xfffffe7f, 'GFX_ATTR_CLEAR_BITS_8_7',   'run_campaign_card_select_handler_2_hb7_mask'),

    # --- EQ_NEW (18 new constants in duel_field.inc) ---
    (0x08027f10, 0x00002c06, 'CAMPAIGN_SIO_CMD_MATCH',        'run_campaign_card_select_handler_0_sio_cmd'),
    (0x08027fc0, 0xffe07fff, 'CAMPAIGN_CARD_STEP_COPY_MASK',  'run_campaign_card_select_handler_1_copy_mask'),
    (0x08028190, 0xfffffe03, 'CAMPAIGN_CARD_ANIM_STEP_MASK',  'run_campaign_card_select_handler_6_anim_mask'),
    (0x08028a34, 0x003e0014, 'CAMPAIGN_CARD_SPRITE_POS_0',    'tick_campaign_card_selector_oam_sprite_pos_0'),
    (0x08028a38, 0x003e0034, 'CAMPAIGN_CARD_SPRITE_POS_1',    'tick_campaign_card_selector_oam_sprite_pos_1'),
    (0x08028a3c, 0x003e0054, 'CAMPAIGN_CARD_SPRITE_POS_2',    'tick_campaign_card_selector_oam_sprite_pos_2'),
    (0x08028a40, 0x003e0084, 'CAMPAIGN_CARD_SPRITE_POS_3',    'tick_campaign_card_selector_oam_sprite_pos_3'),
    (0x08028a44, 0x003e00a4, 'CAMPAIGN_CARD_SPRITE_POS_4',    'tick_campaign_card_selector_oam_sprite_pos_4'),
    (0x08028a48, 0x003e00c4, 'CAMPAIGN_CARD_SPRITE_POS_5',    'tick_campaign_card_selector_oam_sprite_pos_5'),
    (0x08028b38, 0x006e0024, 'CAMPAIGN_HAND_SPRITE_POS_A',    'tick_campaign_card_selector_oam_hand_sprite_pos_a'),
    (0x08028b3c, 0x006e0044, 'CAMPAIGN_HAND_SPRITE_POS_B',    'tick_campaign_card_selector_oam_hand_sprite_pos_b'),
    (0x08028b40, 0x006e0094, 'CAMPAIGN_HAND_SPRITE_POS_C',    'tick_campaign_card_selector_oam_hand_sprite_pos_c'),
    (0x08028b44, 0x006e00b4, 'CAMPAIGN_HAND_SPRITE_POS_D',    'tick_campaign_card_selector_oam_hand_sprite_pos_d'),
    (0x08028bc8, 0x006e0024, 'CAMPAIGN_HAND_SPRITE_POS_A',    'tick_campaign_card_selector_oam_hand_sprite_pos_a2'),
    (0x08028bcc, 0x006e0044, 'CAMPAIGN_HAND_SPRITE_POS_B',    'tick_campaign_card_selector_oam_hand_sprite_pos_b2'),
    (0x08028bd0, 0x006e0094, 'CAMPAIGN_HAND_SPRITE_POS_C',    'tick_campaign_card_selector_oam_hand_sprite_pos_c2'),
    (0x08028bd4, 0x006e00b4, 'CAMPAIGN_HAND_SPRITE_POS_D',    'tick_campaign_card_selector_oam_hand_sprite_pos_d2'),
    # GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF is in EQ_DISASM (from disasm literal pool)
    # but we include it here too since the slot may be processed after disasm
    # NOTE: slots 0x08027eac..0x08027eb8 are in the disasm block -- handled by DisassembleF01Seg9Block.py
]

# EQ_DISASM -- literal pool slots inside the disassembled function tick_campaign_card_select_display_state
# These are applied AFTER the disasm block has been decoded (the pool DWORDs already exist).
EQ_DISASM = [
    # slot 0x08027eac = 0xfffffdc4 -> sp_adj (RENAME only -- sp offset, not a named equate)
    (0x08027eb0, 0x03000040, 'gPrng',                       'tick_campaign_card_select_display_state_gprng'),
    (0x08027eb4, 0x00000584, 'GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF', 'tick_campaign_card_select_display_state_flag_off'),
    (0x08027eb8, 0x00000202, 'GPRNG_STEP_IDX_OFF',          'tick_campaign_card_select_display_state_step_off'),
]

# EQ_DISASM RENAME (sp offset slot -- not an equate, just a rename)
EQ_DISASM_RENAME = [
    (0x08027eac, 'tick_campaign_card_select_display_state_sp_adj', '0xfffffdc4: negative sp adjustment for frame setup'),
]


# ---------------------------------------------------------------------------
# B: REF_SLOTS (slot_addr, target_addr, gas_label, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # handler table ptr slot (0x08027ebc holds .word PTR_run_campaign_card_select_handler_0_08027ec0)
    # NOTE: 0x08027ebc is renamed in RENAME_SLOTS; the gas_label here is the table label at 0x08027ec0
    # We handle 0x08027ebc as RENAME_SLOT (already named PTR_run_campaign_card_select_handler_0_08027ec0)
    # and just add data ref to table at 0x08027ec0.
    (0x08027ebc, 0x08027ec0, 'PTR_run_campaign_card_select_handler_0_08027ec0', 'campaign_card_handler_table_ptr'),
    # font_jp_base_table (already labelled in asm/00)
    (0x08028560, 0x09e5f854, 'font_jp_base_table', 'render_campaign_text_line_centered_font_table'),
    (0x0802868c, 0x09e5f854, 'font_jp_base_table', 'render_campaign_text_line_with_align_font_table'),
    # carve labels (new)
    (0x080287f4, 0x09e59d78, 'pack_strip_tile_id_table',              'write_pack_strip_oam_entries_tile_table'),
    (0x08028918, 0x09e59d38, 'campaign_oam_slot_count_table',         'tick_campaign_card_selector_oam_attr_table'),
    (0x0802891c, 0x0300024c, 'tick_campaign_card_selector_oam_attr_buf', 'tick_campaign_card_selector_oam_attr_buf_slot'),
    (0x08028948, 0x0060006e, 'tick_campaign_card_selector_oam_mode1_xy_coord', 'tick_campaign_card_selector_oam_mode1_xy_coord_slot'),
    (0x08028b24, 0x09e59d88, 'pack_card_grid_tile_table',             'write_pack_grid_oam_by_card_slot_tile_table'),
    (0x0802829c, 0x02001138, 'run_campaign_card_select_handler_10_proto_row', 'run_campaign_card_select_handler_10_proto_row_slot'),
    (0x080283c0, 0x09e5e80c, 'expert_challenge_record_array',         'run_campaign_card_select_handler_14_expert_base'),
    (0x080283c4, 0x09e5e620, 'standard_challenge_record_array',       'run_campaign_card_select_handler_14_standard_base'),
    (0x080283c8, 0x09e5e9cc, 'puzzle_challenge_record_array',         'run_campaign_card_select_handler_14_puzzle_base'),
    # tile deltas -- value is literal not a proper ROM/RAM address; REF not applicable
    # NOTE: 0x08028b2c and 0x08028b30 are in RENAME_SLOTS
    # NOTE: 0x08028948 has REF above to itself (packed OAM coord); also RENAME below
]


# ---------------------------------------------------------------------------
# C: RENAME_SLOTS (slot_addr, slot_label, eol)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08027ebc, 'campaign_card_handler_table_ptr',
     'ptr to PTR_run_campaign_card_select_handler_0 jump dispatch table (0x10 entries)'),
    (0x080283b0, 'run_campaign_card_select_handler_14_ewram_neg_off_a',
     '0xfffffc70: negative offset into EWRAM for campaign struct ptr'),
    (0x080283b4, 'run_campaign_card_select_handler_14_ewram_neg_off_b',
     '0xfffffe5c: similar negative EWRAM offset'),
    (0x080283bc, 'run_campaign_card_select_handler_14_challenge_flag_mask',
     '0x0000e0fc: challenge completion/sprite flag bitmask'),
    (0x08028b2c, 'write_pack_grid_oam_by_card_slot_tile_delta_a',
     '0x1006: tile attr delta row A'),
    (0x08028b30, 'write_pack_grid_oam_by_card_slot_tile_delta_b',
     '0x1007: tile attr delta row B'),
    (0x08028948, 'tick_campaign_card_selector_oam_mode1_xy_coord',
     '0x0060006e: packed OAM xy (x=110 y=96) for mode1 sprite'),
    # pack tiles RENAME (Carve G blocked -- asset sizes unknown)
    (0x08028744, 'load_pack_tiles_with_palette_init_tiles_a',
     '0x09b9e6e8: pack tiles A GFX blob'),
    (0x0802878c, 'load_pack_tiles_with_palette_init_tiles_b',
     '0x09ba050c: pack tiles B GFX blob'),
    (0x08028790, 'load_pack_tiles_with_palette_init_tiles_c',
     '0x09b9fa20: pack tiles C GFX blob'),
    (0x08028798, 'load_pack_tiles_with_palette_init_pal_src',
     '0x09b9e6c8: pack palette GFX blob'),
    (0x080287a0, 'load_pack_tiles_with_palette_init_bg_tiles',
     '0x09b9c6c8: pack BG tile GFX blob'),
    # campaign hand OAM array RENAME (Carve H blocked -- auto-gen file)
    (0x080282ec, 'run_campaign_card_select_handler_13_hand_array',
     '0x095b7cca: campaign hand OAM array; target in card-image-index.s'),
]


# ---------------------------------------------------------------------------
# D: PLATE_REPL -- stale name replacement (28 occurrences)
# Each entry: (fn_addr, [(old_str, new_str), ...])
# IMPORTANT: match full string PTR_FUN_08027ec0 (not bare FUN_08027ec0)
# to avoid producing PTR_PTR_run_campaign_card_select_handler_0_...
# ---------------------------------------------------------------------------
PLATE_REPL = {
    0x08027f00: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x08027f48: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x08027fcc: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x0802803c: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080280bc: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080280d0: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x08028118: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x08028194: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080281d8: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x0802826e: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080282a0: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080282ac: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080282c2: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080282f0: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x080283e8: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0'),
                 (u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
    0x08028402: [(u'PTR_FUN_08027ec0', u'PTR_run_campaign_card_select_handler_0_08027ec0')],
    0x08028874: [(u'FUN_08028402',    u'finalize_campaign_card_select_frame')],
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
    print("=== RefineF01Seg9Slots (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = nDisasmEq = nDisasmRen = 0
    made = set()

    # --- A: EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err))
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

    # --- A_DISASM: EQ_DISASM (literal pool slots from disassembled function) ---
    for slot_int, value, cname, label in EQ_DISASM:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[AdISASM FAIL] 0x%08x: %s -- (may need to run disasm script first)" % (slot_int, err))
            continue
        if DRY:
            print("[Adisasm dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nDisasmEq += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[Adisasm ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nDisasmEq += 1

    # --- A_DISASM RENAME ---
    for slot_int, label, eol in EQ_DISASM_RENAME:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[AdisasmREN FAIL] no 4B data @ 0x%08x -- (may need disasm script first)" % slot_int)
            continue
        if DRY:
            print("[AdisasmREN dry] 0x%08x rename %s" % (slot_int, label))
            nDisasmRen += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[AdisasmREN ok] 0x%08x -> %s" % (slot_int, label))
        nDisasmRen += 1

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

    # --- D: PLATE_REPL (stale name fix, 28 occurrences) ---
    # Each pattern replaced independently; missing patterns are skipped (not all
    # handlers reference both stale names in their plate).
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

    print("[done] A=%d AdisasmEq=%d AdisasmRen=%d B=%d C=%d D=%d (DRY=%s)" % (
        nA, nDisasmEq, nDisasmRen, nB, nC, nD, DRY))


main()
