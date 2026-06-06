# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg6aSlots.py -- p5 Seg-6a (0x0801794c..0x08017e48)
#   load_game_str_1006_to_state (boundary; slots already done in Seg-5d)
#   encode_char_to_line_buf / encode_str_table_entry_to_line_buf /
#   render_name_input_jp_labels_to_obj / dispatch_banlist_text_by_key
#
# Sections:
#   A. EQ_SLOTS  -- (none in Seg-6a; all EQ are in Seg-6b functions)
#   B. REF_SLOTS -- USER label on target + DATA ref from slot + slot rename
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_SUBS -- replace bare address/DAT_ references in plate comments

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
#    If multiple slots share same target, label is written only once.
#
# Seg-6a covered slots:
#   encode_char_to_line_buf          (0x080179a8): DAT_08017a20
#   encode_str_table_entry_to_line_buf (0x08017a24): DAT_08017a54/b14/b18/b30
#   render_name_input_jp_labels_to_obj (0x08017b44): DAT_08017c54/c60/c64
#   dispatch_banlist_text_by_key     (0x08017c7c): DAT_08017c90/ca8
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- encode_char_to_line_buf ---
    # DAT_08017a20: line_break_seq=0x09e3b2b4 (carve label from kana pool)
    (0x08017a20, 0x09e3b2b4, 'line_break_seq', 'encode_char_to_line_buf_line_break_seq'),

    # --- encode_str_table_entry_to_line_buf ---
    # DAT_08017a54: gState=0x02029250 (ewram.inc)
    (0x08017a54, 0x02029250, 'gState', 'encode_str_table_entry_to_line_buf_gstate'),
    # DAT_08017b14: name_char_group_ptr_table=0x09e587f0 (carve B label)
    (0x08017b14, 0x09e587f0, 'name_char_group_ptr_table', 'encode_str_table_entry_to_line_buf_group_ptr_table'),
    # DAT_08017b18: name_char_range_table=0x09e3b251 (kana pool label)
    (0x08017b18, 0x09e3b251, 'name_char_range_table', 'encode_str_table_entry_to_line_buf_range_table'),
    # DAT_08017b30: assert_table_last_fmt=0x09e3b338 (carve I label)
    (0x08017b30, 0x09e3b338, 'assert_table_last_fmt', 'encode_str_table_entry_to_line_buf_assert_fmt'),

    # --- render_name_input_jp_labels_to_obj ---
    # DAT_08017c54: gState=0x02029250
    (0x08017c54, 0x02029250, 'gState', 'render_name_input_jp_labels_to_obj_gstate'),
    # DAT_08017c60: EWRAM_BASE=0x02000000 (gba_mem.inc)
    (0x08017c60, 0x02000000, 'EWRAM_BASE', 'render_name_input_jp_labels_to_obj_ewram_base'),
    # DAT_08017c64: GSETTINGS_OFFSET -- value 0x6c2c is an integer offset, not a RAM addr;
    # treat as RENAME_SLOT (plain rename + EOL). Handled in section C below.

    # --- dispatch_banlist_text_by_key ---
    # DAT_08017c90: gState=0x02029250
    (0x08017c90, 0x02029250, 'gState', 'dispatch_banlist_text_by_key_gstate'),
    # DAT_08017ca8: banlist_jp_str_src=0x09e3afdc (kana pool label)
    (0x08017ca8, 0x09e3afdc, 'banlist_jp_str_src', 'dispatch_banlist_text_by_key_jp_str_src'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    Plain rename + optional EOL comment. All text pure ASCII (no CJK).
#
# Slots handled: GSETTINGS_OFFSET refs (plain integer offsets, not RAM addrs),
# char sentinel, assert lines, str IDs, width stores, scroll col offset.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # encode_str_table_entry_to_line_buf
    (0x08017a58, 'encode_str_table_entry_to_line_buf_scroll_col_offset',
     'gState+0x315 = scroll column index field; bits[5:2] select column group'),
    (0x08017b1c, 'encode_str_table_entry_to_line_buf_char_sentinel',
     'upper-bound literal 0xe3a9 in char-group scan cmp; not an address'),
    (0x08017b20, 'encode_str_table_entry_to_line_buf_assert_line_117',
     'assert line 0x117=279 (char width range check)'),
    (0x08017b28, 'encode_str_table_entry_to_line_buf_assert_line_189',
     'assert line 0x189=393 (column group boundary check)'),

    # render_name_input_jp_labels_to_obj
    (0x08017c58, 'render_name_input_jp_labels_to_obj_str_id_a',
     'STR_ID_A=0x1008: first game_str label id rendered to OBJ VRAM'),
    (0x08017c64, 'render_name_input_jp_labels_to_obj_gsettings_offset',
     '= 0x6c2c; gSettings(0x02006c2c) - EWRAM_BASE; bits[2:0]=language_id'),
    (0x08017c6c, 'render_name_input_jp_labels_to_obj_width_store_a',
     'gState+0x321 = pixel width store for str A result'),
    (0x08017c70, 'render_name_input_jp_labels_to_obj_str_id_b',
     'STR_ID_B=0x1007: second game_str label id'),
    (0x08017c74, 'render_name_input_jp_labels_to_obj_str_id_c',
     'STR_ID_C=0x100c: third game_str label id'),
    (0x08017c78, 'render_name_input_jp_labels_to_obj_width_store_c',
     'gState+0x322 = pixel width store for str C result'),
]

# ---------------------------------------------------------------------------
# D. PLATE_SUBS: (func_entry_addr, old_substr, new_substr)
#    Replace bare address literals or DAT_ references in plate comments.
#    All text pure ASCII.
#
# Seg-6a plate updates (R5):
#   encode_char_to_line_buf: 0x09e3b2b4 -> line_break_seq
#   encode_str_table_entry_to_line_buf: 4 bare values -> symbolic names
#   render_name_input_jp_labels_to_obj: 0x02029250 -> gState (if present)
# ---------------------------------------------------------------------------
PLATE_SUBS = [
    # encode_char_to_line_buf (0x080179a8): replace bare 0x09e3b2b4 -> line_break_seq
    (0x080179a8, '0x09e3b2b4', 'line_break_seq'),

    # encode_str_table_entry_to_line_buf (0x08017a24): 4 replacements
    (0x08017a24, '0x09e3b338', 'assert_table_last_fmt'),
    (0x08017a24, '0x09e587f0', 'name_char_group_ptr_table'),
    (0x08017a24, '0x09e3b251', 'name_char_range_table'),
    (0x08017a24, '0x0000e3a9', 'encode_str_table_entry_to_line_buf_char_sentinel'),

    # render_name_input_jp_labels_to_obj (0x08017b44): bare gState addr -> gState
    (0x08017b44, '0x02029250', 'gState'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RefineSeg6aSlots (DRY=%s) ===" % DRY)
    rm  = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    nB = nC = nD = 0
    made = set()

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

    print("[done] B=%d C=%d D=%d (DRY=%s)" % (nB, nC, nD, DRY))


main()
