# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg1Slots.py -- p5 file 01 Seg-1 (0x0801cb00..0x0801d448)
#   vija scene state machine (8 functions):
#   run_vija_scene_state_machine / tick_scene_step_by_step_table_b /
#   tick_scene_step_by_step_table_c / write_tile_attr_byte_to_vram /
#   copy_palette_bank_by_slot / write_tile_attr_strip_4wide /
#   apply_palette_and_tile_attr_strips / decode_card_image_6bpp
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (14 reuse + 1 new BG_CHAR_VRAM_CB2)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename (3)
#   C. RENAME_SLOTS -- plain rename + optional EOL (5)
#   D. PLATE_REWRITES -- 2x FUN_->current name (C8 fixes) + 1x CJK->ASCII
#
# REVIEW FIXES APPLIED:
#   #1 (C5): DWORD_0801cfc0/d018 reuse NAME_INPUT_PAGE_STATE_CLEAR (name_input.inc:28)
#             instead of new STEP_ADVANCE_MASK.
#   #2 (C8): write_tile_attr_byte_to_vram plate FUN_0801d174->write_tile_attr_strip_4wide;
#             copy_palette_bank_by_slot plate FUN_0801d208->apply_palette_and_tile_attr_strips.
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
    # --- ewram.inc: gVijaState = 0x02029eb0 (1 slot) ---
    (0x0801cb1c, 0x02029eb0, 'gVijaState',
     'run_vija_scene_state_machine_gvija_state',
     'gVijaState: vija per-frame state struct base (0xc0 bytes @ EWRAM)'),

    # --- rom_region.inc: ROM_REGION_CODE_ADDR = 0x080000ae (2 slots) ---
    (0x0801cbf8, 0x080000ae, 'ROM_REGION_CODE_ADDR',
     'run_vija_scene_state_machine_rom_region_code_addr',
     'ROM header game-code high u16 (ldrh+>>8 gives region char)'),
    (0x0801d424, 0x080000ae, 'ROM_REGION_CODE_ADDR',
     'decode_card_image_6bpp_rom_region_code_addr', None),

    # --- gba_mem.inc: EWRAM_BASE = 0x02000000 (2 slots) ---
    (0x0801cbfc, 0x02000000, 'EWRAM_BASE',
     'run_vija_scene_state_machine_ewram_base',
     'EWRAM base: used with GSETTINGS_OFFSET to reach gSettings'),
    (0x0801d428, 0x02000000, 'EWRAM_BASE',
     'decode_card_image_6bpp_ewram_base', None),

    # --- name_input.inc: GSETTINGS_OFFSET = 0x00006c2c (2 slots) ---
    (0x0801cc00, 0x00006c2c, 'GSETTINGS_OFFSET',
     'run_vija_scene_state_machine_gsettings_offset',
     'gSettings byte offset from EWRAM_BASE (0x6c2c)'),
    (0x0801d42c, 0x00006c2c, 'GSETTINGS_OFFSET',
     'decode_card_image_6bpp_gsettings_offset', None),

    # --- demo_state.inc: DEMO_CLEAR_BITS_12_8 = 0xffffe0ff (4 slots) ---
    (0x0801cc04, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'run_vija_scene_state_machine_dispcnt_obj_en_mask_a',
     'DISPCNT clear bits[12:8] (BG/OBJ enable field)'),
    (0x0801cd9c, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'run_vija_scene_state_machine_dispcnt_obj_en_mask_b', None),
    (0x0801ce3c, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'run_vija_scene_state_machine_dispcnt_obj_en_mask_c', None),
    (0x0801cf08, 0xffffe0ff, 'DEMO_CLEAR_BITS_12_8',
     'run_vija_scene_state_machine_dispcnt_obj_en_mask_d', None),

    # --- name_input.inc: NAME_INPUT_PAGE_STATE_CLEAR = 0xffc03fff (2 slots) ---
    # C5 fix: reuse existing constant (same value+semantics as proposed STEP_ADVANCE_MASK)
    (0x0801cfc0, 0xffc03fff, 'NAME_INPUT_PAGE_STATE_CLEAR',
     'tick_scene_step_by_step_table_b_step_advance_mask',
     'bits[21:14] clear mask for step index field in gPrng+0x204'),
    (0x0801d018, 0xffc03fff, 'NAME_INPUT_PAGE_STATE_CLEAR',
     'tick_scene_step_by_step_table_c_step_advance_mask', None),

    # --- gba_mem.inc NEW: BG_CHAR_VRAM_CB2 = 0x06004000 (2 slots) ---
    (0x0801d158, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'write_tile_attr_byte_to_vram_vram_char_base',
     'BG charblock 2 base: 0x06004000 = GBA_VRAM_BASE + 0x4000'),
    (0x0801d438, 0x06004000, 'BG_CHAR_VRAM_CB2',
     'decode_card_image_6bpp_vram_char_base', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- switch table base ptr at 0x0801cb20 -> switchdataD_0801cb24 ---
    (0x0801cb20, 0x0801cb24, 'switchD_0801cb1a__switchdataD_0801cb24',
     'run_vija_scene_state_machine_switch_table_base',
     'ptr to 10-case switch jump table at switchdataD_0801cb24'),

    # --- vija BG FS path pair at 0x0801cbf4 -> vija_bg_fs_path_pair (rom.s carve) ---
    (0x0801cbf4, 0x09e3da08, 'vija_bg_fs_path_pair',
     'run_vija_scene_state_machine_vija_bg_path_pair',
     'ptr to {JP path, US path} pair for vija BG1 LZ5 file load'),

    # --- vija OBJ slot seq at 0x0801ce00 -> vija_obj_slot_seq (rom.s carve) ---
    (0x0801ce00, 0x09e3da10, 'vija_obj_slot_seq',
     'run_vija_scene_state_machine_vija_obj_slot_seq',
     'ptr to 5-byte OBJ slot index sequence {01 03 00 02 04}'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # ROM step table B base (0x09e589b4): shared by table_b and table_c
    (0x0801cfb8, 'tick_scene_step_by_step_table_b_step_table',
     'ROM step table B base 0x09e589b4: 3 THUMB fn-ptrs +1 NULL'),
    (0x0801d010, 'tick_scene_step_by_step_table_c_step_table',
     'ROM step table B base 0x09e589b4 (shared with table_b)'),

    # decode_card_image_6bpp bitmask slots
    (0x0801d43c, 'decode_card_image_6bpp_tile_x_low_mask',
     '0x31f: low-9-bit tile index mask for BG char addr compute'),
    (0x0801d440, 'decode_card_image_6bpp_tile_xy_6bit_mask',
     '0x3f3f: dual-6-bit mask for tile grid x/y coordinate fields'),
    (0x0801d444, 'decode_card_image_6bpp_attr_packed_mask',
     '0xc7f: packed tile attribute field mask'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Replaces FUN_ references in existing plate comments.
#    Also handles CJK->ASCII plate rewrite.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # C8 fix #1: write_tile_attr_byte_to_vram plate FUN_->current name
    (0x0801d0cc, 'FUN_0801d174', 'write_tile_attr_strip_4wide'),

    # C8 fix #2: copy_palette_bank_by_slot plate FUN_->current name
    (0x0801d15c, 'FUN_0801d208', 'apply_palette_and_tile_attr_strips'),
]

# ---------------------------------------------------------------------------
# CJK_PLATE_REWRITES: (func_addr, new_plate_ascii)
#    Full plate replacement for CJK->ASCII conversion.
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    (0x0801d290,
     "@ 6bpp source -> BG char VRAM tile layout. 6 input bytes -> 8 output pixels\n"
     "@ (3 src halfwords -> 4 dst halfwords). Writes to BG charblock 2 (0x06004000).\n"
     "@ r0/r1: tile coord params; r2: packed tile attribute; operates on card image data.\n"
     "@ Parameters: r5=src_ptr (6bpp card image), r6=VRAM dst tile base.\n"
     "@ Returns void (pop {r0}; bx r0, Sub-case E)."),
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
    print("=== RefineF01Seg1Slots (DRY=%s) ===" % DRY)
    print("  f01 Seg-1: 0x0801cb00..0x0801d448, 8 fn, vija scene state machine")

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

    # E. CJK plate full rewrites
    print("\n--- E. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineF01Seg1Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d  CJK_PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS),
        len(PLATE_REWRITES), len(CJK_PLATE_REWRITES)))

main()
