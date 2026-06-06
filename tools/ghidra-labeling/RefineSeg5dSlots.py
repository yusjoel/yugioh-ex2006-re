# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg5dSlots.py -- p5 Seg-5d (0x080171ec..0x0801794c)
#   validate_complement_checksum / decode_char_frame_to_vram / compute_floor_log2 /
#   unpack_bits_to_byte_buf / pack_bytes_to_vram_bits / init_scrollbar_oam_slot_settings /
#   name_input_page_init / dispatch_text_render_by_mode / apply_sprite_gfx_by_type /
#   apply_sprite_gfx_type_zero / setup_font_jp_ctx_bg_vram_fixed /
#   setup_font_jp_ctx_obj_vram_row / fill_bg0_tilemap_name_input /
#   pad_str_to_char_multiple / load_game_str_pair_1004_to_state /
#   (boundary) load_game_str_1006_to_state
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (const_name from inc, slot rename)
#   B. REF_SLOTS -- USER label on target + DATA ref from slot + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (sp-offsets, assert ptrs, etc.)
#   D. PLATE_SUBS -- substring replace FUN_xxxx -> current name in plate comments
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    const_name must already exist in inc (or be created at first ref).
#    All values verified against ROM via python struct.unpack.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # name_input.inc constants
    (0x080172d4, 0x01000168, 'CHAR_FRAME_DECODE_CPUSET_CTRL', 'decode_char_frame_to_vram_cpuset_ctrl'),
    (0x080175dc, 0x050000c9, 'NAME_INPUT_STATE_CPUSET_CTRL',  'name_input_page_init_cpuset_ctrl'),
    (0x080175e0, 0x00001c02, 'NAME_INPUT_BG0CNT_INIT',        'name_input_page_init_bg0cnt'),
    (0x080175e4, 0x00001d8c, 'NAME_INPUT_BG1CNT_INIT',        'name_input_page_init_bg1cnt'),
    (0x080175e8, 0x00001e8d, 'NAME_INPUT_BG2CNT_INIT',        'name_input_page_init_bg2cnt'),
    (0x080175ec, 0x00001f8f, 'NAME_INPUT_BG3CNT_INIT',        'name_input_page_init_bg3cnt'),
    # gfx_resource.inc reuse (Seg-5b built GFX_ATTR_CLEAR_BITS_13_7, same value 0xffffc07f)
    (0x08017784, 0xffffc07f, 'GFX_ATTR_CLEAR_BITS_13_7',      'apply_sprite_gfx_by_type_oam_pal_mask'),
    # oam_attr.inc new entry OAM_ATTR0_HIDDEN
    (0x08017788, 0x0000ffff, 'OAM_ATTR0_HIDDEN',              'apply_sprite_gfx_by_type_attr0_init'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
#    If multiple slots share same target, label is written only once (made set).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gState=0x02029250 (5 slots)
    (0x08017570, 0x02029250, 'gState', 'init_scrollbar_oam_slot_settings_gstate'),
    (0x080175d8, 0x02029250, 'gState', 'name_input_page_init_gstate'),
    (0x08017778, 0x02029250, 'gState', 'apply_sprite_gfx_by_type_gstate'),
    (0x08017930, 0x02029250, 'gState', 'load_game_str_pair_1004_to_state_gstate'),
    (0x08017990, 0x02029250, 'gState', 'load_game_str_1006_to_state_gstate'),
    # gFontJpCtx=0x02006ed0 (2 slots)
    (0x080177d4, 0x02006ed0, 'gFontJpCtx', 'setup_font_jp_ctx_bg_vram_fixed_font_jp_ctx'),
    (0x08017828, 0x02006ed0, 'gFontJpCtx', 'setup_font_jp_ctx_obj_vram_row_font_jp_ctx'),
    # gTextEncodingOverride=0x0202348c (ewram.inc, already defined)
    (0x080175f0, 0x0202348c, 'gTextEncodingOverride', 'name_input_page_init_text_enc_override'),
    # OBJ_TILE_VRAM_BASE=0x06010000 (gba_mem.inc, already defined)
    (0x08017824, 0x06010000, 'OBJ_TILE_VRAM_BASE', 'setup_font_jp_ctx_obj_vram_row_vram_base'),
    # EWRAM_BASE=0x02000000 (2 slots)
    (0x0801793c, 0x02000000, 'EWRAM_BASE', 'load_game_str_pair_1004_to_state_ewram_base'),
    (0x0801799c, 0x02000000, 'EWRAM_BASE', 'load_game_str_1006_to_state_ewram_base'),
    # carve labels: char_frame_decode_lut=0x09e3a660 (1 slot)
    (0x08017410, 0x09e3a660, 'char_frame_decode_lut', 'decode_char_frame_to_vram_lut_ptr'),
    # carve labels: sprite_gfx_type_meta=0x09e3afc8 (1 slot)
    (0x0801777c, 0x09e3afc8, 'sprite_gfx_type_meta', 'apply_sprite_gfx_by_type_meta_ptr'),
    # carve labels: sprite_palette_type_table=0x09e3afd8 (1 slot)
    (0x08017780, 0x09e3afd8, 'sprite_palette_type_table', 'apply_sprite_gfx_by_type_pal_table_ptr'),
]

# GSETTINGS_OFFSET slots -- these are small integer values, not RAM addresses;
# treat as REF to the offset value (plain rename + EOL); handled in C instead.
# (0x02000000 base + 0x6c2c offset = 0x02006c2c gSettings)

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL. All EOL text is pure ASCII (no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # decode_char_frame_to_vram sp-offset slots
    (0x08017264, 'decode_char_frame_to_vram_neg_frame_size',     'neg stack frame alloc: sp -= 0x5b0'),
    (0x08017268, 'decode_char_frame_to_vram_sp_state_ptr_off',   'sp+0x5a4: ptr to r1(state)'),
    (0x080172d8, 'decode_char_frame_to_vram_sp_state_ptr_off_b', 'sp+0x5a4 2nd ref (same value)'),
    (0x08017414, 'decode_char_frame_to_vram_sp_state_ptr_off_c', 'sp+0x5a4 3rd ref (same value)'),
    (0x08017418, 'decode_char_frame_to_vram_sp_packed_cnt_off',  'sp+0x5a2: packed char count'),
    (0x0801741c, 'decode_char_frame_to_vram_sp_state_holder_off','sp+0x5ac: state ptr holder'),
    (0x08017420, 'decode_char_frame_to_vram_vram_step',          '0x3e9c: VRAM bit-field step; med-conf'),
    # assert string ptr slots (points into ROM blob, factual rename + EOL)
    (0x080172dc, 'decode_char_frame_to_vram_assert_prohibit_cs_ptr',  'ptr to "Prohibit CheckSum Error\\n" in ROM blob'),
    (0x080172f8, 'decode_char_frame_to_vram_assert_password_sz_ptr',  'ptr to "PassWord Size Error\\n" in ROM blob'),
    # decode store-base slot (factual: dst=0x201+r10, no semantic claim; function is 0-ref orphan)
    (0x0801740c, 'decode_char_frame_to_vram_store_base_201',
     'byte store base: dst=0x201+r10 (r10=param r2 from prologue mov r10,r2 @0x0801723a); sibling base 0x200 at 0x080173ee'),
    # BG VRAM fixed base (0x06000020 = BG VRAM + 0x20, tile 1 start)
    (0x080177d0, 'setup_font_jp_ctx_bg_vram_fixed_vram_base', '0x06000020 = BG VRAM base + 0x20 (tile 1 start)'),
    # String ID equate slots (small constant values, rename + EOL)
    (0x08017934, 'load_game_str_pair_1004_to_state_str_id_a', 'str ID 0x1004 name-input str A'),
    (0x08017948, 'load_game_str_pair_1004_to_state_str_id_b', 'str ID 0x1005 name-input str B'),
    (0x08017994, 'load_game_str_1006_to_state_str_id',        'str ID 0x1006 name-input str C'),
    # GSETTINGS_OFFSET slots (plain rename; value 0x6c2c = gSettings - EWRAM_BASE)
    (0x08017940, 'load_game_str_pair_1004_to_state_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE; bits[2:0]=language_id'),
    (0x080179a0, 'load_game_str_1006_to_state_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE; bits[2:0]=language_id'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Replace old_substr with new_substr in the PLATE_COMMENT of the function.
#    Pure ASCII. Performed via setComment(PLATE_COMMENT, ...) on the CodeUnit
#    at func_entry_addr.
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # validate_complement_checksum: FUN_0801722c -> decode_char_frame_to_vram
    (0x080171ec, 'FUN_0801722c', 'decode_char_frame_to_vram'),
    # compute_floor_log2: FUN_08017478 and FUN_080174e8 -> current names
    (0x08017464, 'FUN_08017478', 'unpack_bits_to_byte_buf'),
    (0x08017464, 'FUN_080174e8', 'pack_bytes_to_vram_bits'),
    # unpack_bits_to_byte_buf: FUN_0801722c -> decode_char_frame_to_vram
    (0x08017478, 'FUN_0801722c', 'decode_char_frame_to_vram'),
    # pack_bytes_to_vram_bits: FUN_0801722c -> decode_char_frame_to_vram
    (0x080174e8, 'FUN_0801722c', 'decode_char_frame_to_vram'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
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
    print("=== RefineSeg5dSlots (DRY=%s) ===" % DRY)
    rm  = currentProgram.getReferenceManager()
    et  = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = nD = 0
    made = set()

    # --- A. EQ_SLOTS ---
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B. REF_SLOTS ---
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
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
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
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

    print("[done] A=%d B=%d C=%d D=%d (DRY=%s)" % (nA, nB, nC, nD, DRY))


main()
