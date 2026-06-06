# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg8Slots.py -- p5 Seg-8 (0x08019a58..0x0801a794)
#   banlist password render cluster (28 functions)
#   - A: EQ_SLOTS  -- data-equate (reuse existing inc constants)
#   - B: REF_SLOTS -- USER label on target + DATA ref + slot rename
#   - C: RENAME_SLOTS -- plain rename (no new constants)
#   - D: PLATE_REWRITES -- replace FUN_<hex> with current names in plate comments
#
# NOTES:
#   * DWORD_08019d9c and DWORD_08019ec8 both hold 0x01000200 = NAME_INPUT_BG0_SCREEN_CLEAR_CTRL
#     (already defined in constants/name_input.inc:21). Reuse equate, do not create duplicate.
#   * banlist_pass_char_group_ptr_table and name_o_palette_data already carved (Seg-7);
#     only add DATA ref + slot rename for the referencing slots.
#   * gBanlistPasswordBuffer (0x02029810) already has USER label; only add DATA ref + slot rename.
#   * All plate/EOL text is pure ASCII.

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
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label)
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: gTextEncodingOverride = 0x0202348c ---
    (0x08019c20, 0x0202348c, 'gTextEncodingOverride',
     'encode_pass_char_obj_rows_pair_ptr_encoding_override'),

    # --- gba_mem.inc: EWRAM_BASE = 0x02000000 ---
    (0x08019c2c, 0x02000000, 'EWRAM_BASE',
     'encode_pass_char_obj_rows_pair_ewram_base'),

    # --- name_input.inc: GSETTINGS_OFFSET = 0x00006c2c ---
    (0x08019c30, 0x00006c2c, 'GSETTINGS_OFFSET',
     'encode_pass_char_obj_rows_pair_gsettings_offset'),

    # --- gba_mem.inc: EWRAM_BASE ---
    (0x08019f08, 0x02000000, 'EWRAM_BASE',
     'get_banlist_password_page_ptr_ewram_base'),

    # --- name_input.inc: GSETTINGS_OFFSET ---
    (0x08019f0c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'get_banlist_password_page_ptr_gsettings_offset'),

    # --- gba_mem.inc: EWRAM_BASE ---
    (0x0801a310, 0x02000000, 'EWRAM_BASE',
     'render_banlist_title_text_to_bg_ewram_base'),

    # --- name_input.inc: GSETTINGS_OFFSET ---
    (0x0801a314, 0x00006c2c, 'GSETTINGS_OFFSET',
     'render_banlist_title_text_to_bg_gsettings_offset'),

    # --- ewram.inc: gFontJpCtx = 0x02006ed0 ---
    (0x0801a320, 0x02006ed0, 'gFontJpCtx',
     'render_banlist_title_text_to_bg_ptr_font_jp_ctx'),

    # --- oam_attr.inc: OAM_ATTR2_CHARNAME_MASK = 0x000003ff ---
    (0x0801a5ec, 0x000003ff, 'OAM_ATTR2_CHARNAME_MASK',
     'setup_banlist_sprite_oam_row_batch_attr2_charname_mask'),

    # --- oam_attr.inc: OAM_ATTR2_CHARNAME_CLEAR = 0xfffffc00 ---
    (0x0801a5f0, 0xfffffc00, 'OAM_ATTR2_CHARNAME_CLEAR',
     'setup_banlist_sprite_oam_row_batch_attr2_charname_clear'),

    # --- oam_attr.inc: OAM_ATTR1_X_MASK = 0x000001ff ---
    (0x0801a688, 0x000001ff, 'OAM_ATTR1_X_MASK',
     'setup_banlist_sprite_oam_row_batch_attr1_x_mask'),

    # --- oam_attr.inc: OAM_ATTR1_X_CLEAR = 0xfffffe00 ---
    (0x0801a68c, 0xfffffe00, 'OAM_ATTR1_X_CLEAR',
     'setup_banlist_sprite_oam_row_batch_attr1_x_clear'),

    # --- gba_mem.inc: OBJ_TILE_VRAM_BASE = 0x06010000 ---
    (0x0801a710, 0x06010000, 'OBJ_TILE_VRAM_BASE',
     'zero_obj_tile_vram_range_obj_tile_vram_base'),

    # --- name_input.inc: NAME_INPUT_BG0_SCREEN_CLEAR_CTRL = 0x01000200 (reuse) ---
    (0x08019d9c, 0x01000200, 'NAME_INPUT_BG0_SCREEN_CLEAR_CTRL',
     'init_banlist_pass_input_bg0_page_cpuset_screen'),

    # --- name_input.inc: NAME_INPUT_BG0_SCREEN_CLEAR_CTRL = 0x01000200 (reuse) ---
    (0x08019ec8, 0x01000200, 'NAME_INPUT_BG0_SCREEN_CLEAR_CTRL',
     'init_banlist_pass_input_bg2_page_cpuset_screen'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Adds DATA memory reference from slot to target; labels both.
#    target_addr must already have a USER label (or we create it if needed).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- Already-carved: banlist_pass_char_group_ptr_table @ 0x09e588cc (Seg-7) ---
    (0x08019b28, 0x09e588cc, 'banlist_pass_char_group_ptr_table',
     'encode_pass_table_entry_to_line_buf_ptr_pass_char_group_table'),

    # --- Already-carved: name_o_palette_data @ 0x09ccd290 (Seg-6b) ---
    (0x0801a470, 0x09ccd290, 'name_o_palette_data',
     'load_banlist_pass_input_scene_resources_ptr_name_o_palette'),

    # --- gBanlistPasswordBuffer @ 0x02029810 (already labeled) ---
    (0x0801a164, 0x02029810, 'gBanlistPasswordBuffer',
     'get_banlist_scroll_direction_ptr_banlist_pw_buf'),

    # --- New carve: banlist_char_candidate_str @ 0x09e3bcb1 (from host1) ---
    (0x08019d98, 0x09e3bcb1, 'banlist_char_candidate_str',
     'init_banlist_pass_input_bg0_page_ptr_char_candidate_str'),

    # --- New carve: banlist_pass_char_str @ 0x09e3bfdd (from host1) ---
    (0x08019b2c, 0x09e3bfdd, 'banlist_pass_char_str',
     'encode_pass_table_entry_to_line_buf_ptr_pass_char_str'),

    # --- New carve: banlist_pass_alt_char @ 0x09e3c040 (from host1) ---
    (0x08019b30, 0x09e3c040, 'banlist_pass_alt_char',
     'encode_pass_table_entry_to_line_buf_ptr_alt_char'),

    # --- New carve: rom_password_table @ 0x09e3c044 (from host1) ---
    (0x08019c88, 0x09e3c044, 'rom_password_table',
     'load_banlist_password_table_from_rom_ptr_password_table'),

    # --- New carve: banlist_pass_obj_resource_desc @ 0x09e3c624 (from host2) ---
    (0x0801a458, 0x09e3c624, 'banlist_pass_obj_resource_desc',
     'load_banlist_pass_input_scene_resources_ptr_obj_resource_desc'),

    # --- New carve: banlist_pass_bg1_fs_path @ 0x09e3c634 (from host2) ---
    (0x0801a464, 0x09e3c634, 'banlist_pass_bg1_fs_path',
     'load_banlist_pass_input_scene_resources_ptr_bg1_fs_path'),

    # --- New carve: banlist_pass_bg2_fs_path @ 0x09e3c650 (from host2) ---
    (0x0801a46c, 0x09e3c650, 'banlist_pass_bg2_fs_path',
     'load_banlist_pass_input_scene_resources_ptr_bg2_fs_path'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename only; no new equate. Covers private offsets into
#    gBanlistPasswordBuffer and other scene-private constants.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # encode_pass_table_entry_to_line_buf (0x08019a58)
    (0x08019b24, 'encode_pass_table_entry_to_line_buf_pass_buf_off_661', None),
    # render_banlist_pass_char_obj_rows_pair (0x08019b4c)
    (0x08019c24, 'encode_pass_char_obj_rows_pair_str_id_a', None),
    (0x08019c38, 'encode_pass_char_obj_rows_pair_pass_buf_off_675', None),
    (0x08019c3c, 'encode_pass_char_obj_rows_pair_str_id_b', None),
    (0x08019c40, 'encode_pass_char_obj_rows_pair_pass_buf_off_674', None),
    # load_banlist_password_table_from_rom (0x08019c48)
    (0x08019c80, 'load_banlist_password_table_from_rom_max_entries', None),
    (0x08019c8c, 'load_banlist_password_table_from_rom_byte_guard', None),
    # init_banlist_pass_input_bg0_page (0x08019d14)
    (0x08019da0, 'init_banlist_pass_input_bg0_page_cpuset_char', None),
    # init_banlist_pass_input_bg2_page (0x08019e2c)
    (0x08019ecc, 'init_banlist_pass_input_bg2_page_pass_buf_off_664', None),
    (0x08019ed0, 'init_banlist_pass_input_bg2_page_pass_buf_off_66e', None),
    # tick_banlist_scroll_input_handler (0x08019fe4)
    (0x0801a010, 'tick_banlist_scroll_input_handler_scrollbar_off', None),
    (0x0801a064, 'tick_banlist_scroll_input_handler_char_step_off_a', None),
    (0x0801a094, 'tick_banlist_scroll_input_handler_char_step_off_b', None),
    (0x0801a0b0, 'tick_banlist_scroll_input_handler_char_step_off_c', None),
    (0x0801a114, 'tick_banlist_scroll_input_handler_char_step_off_d', None),
    (0x0801a150, 'tick_banlist_scroll_input_handler_char_step_off_e', None),
    # get_banlist_scroll_direction (0x0801a154)
    (0x0801a168, 'get_banlist_scroll_direction_scroll_dir_off', None),
    # set_banlist_scroll_step (0x0801a16c)
    (0x0801a1a0, 'set_banlist_scroll_step_assert_line_2cd', None),
    (0x0801a1a8, 'set_banlist_scroll_step_step_field_off', None),
    # tick_banlist_bg_scroll_step (0x0801a1ac)
    (0x0801a1e8, 'tick_banlist_bg_scroll_step_scroll_step_off', None),
    (0x0801a1ec, 'tick_banlist_bg_scroll_step_scroll_dir_off', None),
    # render_banlist_title_text_to_bg (0x0801a230)
    (0x0801a308, 'render_banlist_title_text_to_bg_str_id', None),
    (0x0801a31c, 'render_banlist_title_text_to_bg_char_vram_addr', None),
    # load_banlist_pass_input_scene_resources (0x0801a328)
    (0x0801a45c, 'load_banlist_pass_input_scene_resources_obj_anim_off_a', None),
    (0x0801a460, 'load_banlist_pass_input_scene_resources_obj_anim_off_b', None),
    (0x0801a468, 'load_banlist_pass_input_scene_resources_clr_mask', None),
    (0x0801a474, 'load_banlist_pass_input_scene_resources_bg_palette_slot1', None),
    (0x0801a47c, 'load_banlist_pass_input_scene_resources_obj_palette_slot1', None),
    (0x0801a480, 'load_banlist_pass_input_scene_resources_obj_palette_fill_dst', None),
    # tick_banlist_card_slot_anim_oam (0x0801a49c)
    (0x0801a4ec, 'tick_banlist_card_slot_anim_oam_sprite_ptr_off_a', None),
    (0x0801a4f4, 'tick_banlist_card_slot_anim_oam_assert_line_36f', None),
    (0x0801a4fc, 'tick_banlist_card_slot_anim_oam_sprite_ptr_off_b', None),
    # setup_banlist_sprite_oam_row_batch (0x0801a560)
    (0x0801a5f4, 'setup_banlist_sprite_oam_row_batch_wide_sprite_mode', None),
    # zero_obj_tile_vram_range (0x0801a6e4)
    (0x0801a714, 'zero_obj_tile_vram_range_word_count_mask', None),
    # init_banlist_scrollbar_oam_entry (0x0801a718)
    (0x0801a748, 'init_banlist_scrollbar_oam_entry_scrollbar_off', None),
    # advance_banlist_scrollbar_pos_page (0x0801a74c)
    (0x0801a76c, 'advance_banlist_scrollbar_pos_page_scrollbar_off', None),
    # retreat_banlist_scrollbar_pos_page (0x0801a770)
    (0x0801a790, 'retreat_banlist_scrollbar_pos_page_scrollbar_off', None),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_entry_addr, [(old_fun_str, new_name), ...])
#    Replace FUN_<hex> stubs in plate comments with current function names.
#    FUN_0x0801aec8/af70/b284/b368 are Seg-9+ unnamed -> keep as-is.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # reject_banlist_input_event @ 0x08019c44: FUN_08019d14
    (0x08019c44, [
        ('FUN_08019d14', 'init_banlist_pass_input_bg0_page'),
    ]),
    # write_banlist_bg2_scroll_regs_biased @ 0x08019c90: FUN_08019e2c, FUN_0801a1ac
    (0x08019c90, [
        ('FUN_08019e2c', 'init_banlist_pass_input_bg2_page'),
        ('FUN_0801a1ac', 'tick_banlist_bg_scroll_step'),
    ]),
    # render_banlist_password_chars_row @ 0x08019ca4: FUN_08019d14
    (0x08019ca4, [
        ('FUN_08019d14', 'init_banlist_pass_input_bg0_page'),
    ]),
    # render_banlist_password_chars_grid @ 0x08019da4: FUN_08019f24, FUN_08019f78
    (0x08019da4, [
        ('FUN_08019f24', 'init_banlist_pass_chars_grid_row'),
        ('FUN_08019f78', 'refresh_banlist_pass_chars_font_rows'),
    ]),
    # set_banlist_scroll_step @ 0x0801a16c: FUN_08019fe4
    (0x0801a16c, [
        ('FUN_08019fe4', 'tick_banlist_scroll_input_handler'),
    ]),
    # write_banlist_bg3_vofs_with_bias @ 0x0801a484: FUN_08019e2c, FUN_0801a1ac
    (0x0801a484, [
        ('FUN_08019e2c', 'init_banlist_pass_input_bg2_page'),
        ('FUN_0801a1ac', 'tick_banlist_bg_scroll_step'),
    ]),
    # tick_banlist_card_slot_anim_oam @ 0x0801a49c: FUN_0801a540
    (0x0801a49c, [
        ('FUN_0801a540', 'call_tick_banlist_card_slot_anim'),
    ]),
    # setup_banlist_sprite_oam_row_batch @ 0x0801a560: FUN_0801a690
    (0x0801a560, [
        ('FUN_0801a690', 'call_setup_banlist_sprite_oam_row'),
    ]),
    # render_banlist_char_obj_row @ 0x0801a6b4: FUN_08019b4c
    (0x0801a6b4, [
        ('FUN_08019b4c', 'render_banlist_pass_char_obj_rows_pair'),
    ]),
    # zero_obj_tile_vram_range @ 0x0801a6e4: FUN_08019b4c
    (0x0801a6e4, [
        ('FUN_08019b4c', 'render_banlist_pass_char_obj_rows_pair'),
    ]),
    # init_banlist_scrollbar_oam_entry @ 0x0801a718: FUN_08019e2c
    (0x0801a718, [
        ('FUN_08019e2c', 'init_banlist_pass_input_bg2_page'),
    ]),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineSeg8Slots (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
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
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label))
        nC += 1

    # --- D: PLATE_REWRITES ---
    for func_int, repls in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[D FAIL] no code unit @ 0x%08x" % func_int)
            continue
        txt = cu.getComment(CodeUnit.PLATE_COMMENT)
        if txt is None:
            print("[D FAIL] no plate @ 0x%08x" % func_int)
            continue
        new = txt
        for old, rep in repls:
            if old not in new:
                print("[D WARN] 0x%08x pattern not found: %s" % (func_int, old))
            else:
                new = new.replace(old, rep)
        if DRY:
            print("[D dry] 0x%08x plate update %d repls" % (func_int, len(repls)))
            nD += 1
            continue
        if new != txt:
            cu.setComment(CodeUnit.PLATE_COMMENT, new)
            print("[D ok] 0x%08x plate updated" % func_int)
        else:
            print("[D NOOP] 0x%08x plate unchanged" % func_int)
        nD += 1

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))


main()
