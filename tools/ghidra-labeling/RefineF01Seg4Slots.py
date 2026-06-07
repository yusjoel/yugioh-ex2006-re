# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg4Slots.py -- f01 Seg-4 (0x0801e36c..0x0801e714)
#   asm/01_vija_scene_text.s: card_info page state machine, 8 functions:
#   update_card_info_page_state / card_info_page_entry /
#   draw_card_stat_digits_to_oam / draw_stat_row_sprites_to_oam /
#   render_card_stats_oam_for_current_card / card_list_on_select_to_info_page /
#   open_card_info_by_icid / open_card_info_page_from_list
#
# Sections:
#   A. EQ_SLOTS   -- 24 data-equate slots (13 new card_info.inc + 11 reuse)
#   B. RENAME_SLOTS -- 2 plain renames with EOL (tile_r1 + no_stat_sentinel)
#   C. PLATE_REWRITES -- 5 plate changes (2 CJK->ASCII + 3 stale FUN_ removal)
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
    # === update_card_info_page_state (0x0801e36c) ===
    (0x0801e3a8, 0x0201afb0, 'gCardInfoPageState',
     'update_card_info_page_state_gcardinfopagestate',
     None),
    (0x0801e438, 0x02000000, 'EWRAM_BASE',
     'update_card_info_page_state_ewram_base',
     None),
    (0x0801e43c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'update_card_info_page_state_gsettings_off',
     None),

    # === card_info_page_entry (0x0801e440) ===
    (0x0801e484, 0x0201afb0, 'gCardInfoPageState',
     'card_info_page_entry_gcardinfopagestate',
     None),
    (0x0801e488, 0x02000000, 'EWRAM_BASE',
     'card_info_page_entry_ewram_base',
     None),
    (0x0801e48c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'card_info_page_entry_gsettings_off',
     None),

    # === draw_card_stat_digits_to_oam (0x0801e490) ===
    (0x0801e4e4, 0x00060056, 'CARD_STAT_ATK_DEF_OAM_XY',
     'draw_card_stat_digits_to_oam_atk_def_oam_xy',
     'ATK/DEF frame OBJ packed_xy: x=86 y=6; 4 ROM refs'),
    (0x0801e4e8, 0x0000d3a2, 'CARD_STAT_ATK_DEF_OAM_ATTR2',
     'draw_card_stat_digits_to_oam_atk_def_attr2',
     'ATK/DEF frame attr2: pal13 tile0x3a2; 2 ROM refs'),
    (0x0801e4ec, 0x00150058, 'CARD_STAT_QPLAY_OAM_XY',
     'draw_card_stat_digits_to_oam_qplay_oam_xy',
     'Quick-Play Spell marker packed_xy: x=88 y=21; 2 ROM refs'),
    (0x0801e4f0, 0x0000e3a6, 'CARD_STAT_QPLAY_OAM_ATTR2',
     'draw_card_stat_digits_to_oam_qplay_attr2',
     'Quick-Play marker attr2: pal14 tile0x3a6; 2 ROM refs'),
    (0x0801e518, 0x0000f001, 'CARD_STAT_DIGIT_OAM_ATTR2',
     'draw_card_stat_digits_to_oam_digit_attr2_a',
     'ATK/DEF digit sprite attr2: pal15 tile1; loop path A'),
    (0x0801e55c, 0x0000f001, 'CARD_STAT_DIGIT_OAM_ATTR2',
     'draw_card_stat_digits_to_oam_digit_attr2_b',
     'ATK/DEF digit sprite attr2: pal15 tile1; loop path B'),
    (0x0801e560, 0x0201afb0, 'gCardInfoPageState',
     'draw_card_stat_digits_to_oam_gcardinfopagestate_a',
     None),
    (0x0801e564, 0x0000c3a8, 'CARD_STAT_FUSION_OAM_ATTR2',
     'draw_card_stat_digits_to_oam_fusion_attr2',
     'Fusion/extra-type marker attr2: pal12 tile0x3a8; 1 ROM ref'),
    (0x0801e590, 0x0201afb0, 'gCardInfoPageState',
     'draw_card_stat_digits_to_oam_gcardinfopagestate_b',
     None),

    # === draw_stat_row_sprites_to_oam (0x0801e594) ===
    (0x0801e610, 0xfffff800, 'CARD_STAT_ROW_ATTR2_BASE_A',
     'draw_stat_row_sprites_to_oam_attr2_base_a',
     'stat row sprite group A attr2 base (row 0)'),
    (0x0801e614, 0xfffff804, 'CARD_STAT_ROW_ATTR2_BASE_B',
     'draw_stat_row_sprites_to_oam_attr2_base_b',
     'stat row sprite group B attr2 base (row 1)'),
    (0x0801e618, 0xfffff808, 'CARD_STAT_ROW_ATTR2_BASE_C',
     'draw_stat_row_sprites_to_oam_attr2_base_c',
     'stat row sprite group C attr2 base (row 2)'),
    (0x0801e61c, 0xfffff80c, 'CARD_STAT_ROW_ATTR2_BASE_D',
     'draw_stat_row_sprites_to_oam_attr2_base_d',
     'stat row sprite group D attr2 base (row 3)'),

    # === render_card_stats_oam_for_current_card (0x0801e620) ===
    (0x0801e63c, 0x0201afb0, 'gCardInfoPageState',
     'render_card_stats_oam_for_current_card_gcardinfopagestate',
     None),

    # === card_list_on_select_to_info_page (0x0801e640) ===
    (0x0801e6b8, 0x0201afb0, 'gCardInfoPageState',
     'card_list_on_select_to_info_page_gcardinfopagestate',
     None),
    (0x0801e6bc, 0x00003fff, 'CARD_INFO_STATE_CARD_ID_MASK',
     'card_list_on_select_to_info_page_card_id_mask',
     '14-bit card_id mask; (card_id & mask) << 3 into word0[16:3]'),
    (0x0801e6c0, 0xfffe0007, 'CARD_INFO_STATE_CARD_ID_CLEAR',
     'card_list_on_select_to_info_page_card_id_clear',
     'AND mask: clears word0 bits[16:3] (card_id field); keeps [17]+[2:0]'),

    # === open_card_info_page_from_list (0x0801e6f4) ===
    (0x0801e710, 0x0201afb0, 'gCardInfoPageState',
     'open_card_info_page_from_list_gcardinfopagestate',
     None),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # draw_stat_row_sprites_to_oam -- tile index 0x40 (71 ROM refs, not equated)
    (0x0801e60c, 'draw_stat_row_sprites_to_oam_tile_r1',
     'tile index 0x40 (=64) for stat row OBJ sprites; 71 ROM refs, not equated'),
    # card_list_on_select_to_info_page -- 0xffff sentinel (7616 ROM refs, not equated)
    (0x0801e6c8, 'card_list_on_select_to_info_page_no_stat_sentinel',
     '0xffff sentinel: ATK/DEF field not applicable (Spell/Trap); 7616 ROM refs, not equated'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, new_plate_ascii_text)
#    All text pure ASCII -- no CJK.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. card_info_page_entry (0x0801e440) -- CJK -> ASCII
    (0x0801e440,
     '@ Top-level card info page init: decodes card image, renders name+description+stats.\n'
     '@ card_id = (state.word0 << 15) >> 18.\n'
     '@ Calls: card_info_page_init_bg0, card_image_decode_wrapper, render_card_name_to_desc_page_vram,\n'
     '@   card_data_query, render_card_description_text, card_info_page_finalize.\n'
     '@ r4 = gCardInfoPageState ptr; card_id from [r4+0x0] bits[17:2].\n'
     '@ r1=[r4+0xc] pal_offset, r2=[r4+0x10] atk_stat passed to card_image_decode_wrapper.\n'
     '@ Returns void (Pattern B: pop {r4}; pop {r0}; bx r0).'),

    # 2. card_list_on_select_to_info_page (0x0801e640) -- CJK -> ASCII
    (0x0801e640,
     '@ Card-list dispatch to card info page on select.\n'
     '@ First bl: card_info_page_enter_with_card_id.\n'
     '@ Encodes card_id into gCardInfoPageState word0 bits[16:3]:\n'
     '@   (card_id & CARD_INFO_STATE_CARD_ID_MASK) << 3, merged via CARD_INFO_STATE_CARD_ID_CLEAR AND.\n'
     '@ Loads ATK (field[3]) and DEF (field[4]) from card_stats_table into gCardInfoPageState[+0xc/+0x10].\n'
     '@ Sentinel: 0xffff in table field means Spell/Trap (no ATK/DEF); stores 0 in that case.\n'
     '@ Also stores origin_page to [+0x6], card_type fields to [+0x28/+0x2c].\n'
     '@ Clears gCardInfoPageState[+0x0] bits[1:0] (flags field).\n'
     '@ r0=card_id (u16), r1=origin_page (u16), r2=ptr, r3=ptr. Returns void.'),

    # 3. draw_card_stat_digits_to_oam (0x0801e490) -- remove stale FUN_ address
    (0x0801e490,
     '@ Called by render_card_stats_oam_for_current_card. Reads card_id (r0 low16), looks up card_stats_table row\n'
     '@ (stride=11 halfwords), reads ATK (offset+6)/DEF (offset+5)/type (offset+9),\n'
     '@ then calls write_oam_entry_from_packed_args to write digit sprites to OAM buffer.\n'
     '@ Skips render if ATK not in 1..20 range (Spell/Trap have no ATK).\n'
     '@ For type 22 (Quick-Play Trap) with field[9]!=0, renders a second digit group.'),

    # 4. draw_stat_row_sprites_to_oam (0x0801e594) -- remove stale FUN_ address
    (0x0801e594,
     '@ Called by render_card_stats_oam_for_current_card. r0=row_count (signed; negative values\n'
     '@ rounded up by +7 before >>3). Folds row_count by 8 to get column/row indices,\n'
     '@ then loops writing 4 sprite entries per row at Y positions 0x70/0x90/0xb0/0xd0 (32px steps)\n'
     '@ via write_oam_entry_from_packed_args. Loop terminates when r6 > 0x8f (GBA screen height-1=143).'),

    # 5. render_card_stats_oam_for_current_card (0x0801e620) -- remove stale FUN_ address
    (0x0801e620,
     '@ Called every frame by tick_card_info_page_by_state. Reads current card_id from\n'
     '@ global state struct 0x0201afb0 (+0x0 bits[17:2]) and row_count (+0x20),\n'
     '@ then calls draw_card_stat_digits_to_oam and draw_stat_row_sprites_to_oam\n'
     '@ to write all card stat sprites to OAM buffer.'),
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

def _apply_plate(func_addr, new_plate_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] PLATE 0x%08x: no code unit" % func_addr)
        return 0
    if DRY:
        print("[dry] PLATE 0x%08x: rewrite (%d chars)" % (func_addr, len(new_plate_text)))
        return 1
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: plate set (%d chars)" % (func_addr, len(new_plate_text)))
    return 1

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF01Seg4Slots (DRY=%s) ===" % DRY)
    print("  f01-Seg-4: 0x0801e36c..0x0801e714, 8 fn, card_info page state machine")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        eq_ok += _apply_eq(slot_addr, value, eq_name, slot_label, eol)
    print("  EQ done: %d / %d" % (eq_ok, len(EQ_SLOTS)))

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        ren_ok += _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d / %d" % (ren_ok, len(RENAME_SLOTS)))

    # C. PLATE_REWRITES
    print("\n--- C. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plt_ok = 0
    for func_addr, new_plate in PLATE_REWRITES:
        plt_ok += _apply_plate(func_addr, new_plate)
    print("  PLATE done: %d / %d" % (plt_ok, len(PLATE_REWRITES)))

    print("\n=== RefineF01Seg4Slots DONE ===")
    print("  EQ=%d  RENAME=%d  PLATE=%d" % (eq_ok, ren_ok, plt_ok))

main()
