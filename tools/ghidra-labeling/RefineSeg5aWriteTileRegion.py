# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg5aWriteTileRegion.py — p5 Seg-5a (write_tile_region_to_bg_screen 0x16344..0x165b8)
#   med-conf 函数 (r6 struct +0x14/+0x15/+0x16 layout 待 runtime), 仅做槽符号化, 不重写 plate。
#   5 槽: 4 plain rename + 1 carve label ref
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. carve label ref (already-carved label from prior batch)
REF_SLOTS = [
 (0x08016518, 0x09e3a65c, 'assert_expr_zero_65c', 'write_tile_region_to_bg_screen_assert_expr_zero'),
]

# B. plain rename + EOL
RENAME_SLOTS = [
 (0x080163e0, 'write_tile_region_to_bg_screen_ptr_screen_map_staging_buf',
  '= 0x02023d40; only 1 ROM ref (here); med-conf: likely BG screen map staging buffer; gGlState+0x8b0 (just past gGlState end 0x8ac); awaits runtime verify'),
 (0x08016440, 'write_tile_region_to_bg_screen_tile_name_mask',
  '= 0x3ff; 10-bit BG screen-map entry tile_name field (low 10 bits)'),
 (0x080164dc, 'write_tile_region_to_bg_screen_field_16_bitmask',
  '= 0x407f; tests [r6+0x16] bits[14]+bits[6:0]; cmp r0,#0x20 path branches'),
 (0x08016514, 'write_tile_region_to_bg_screen_assert_line_16b',
  '0x16b = 363 (GL/ISD_Draw.c line)'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RefineSeg5aWriteTileRegion (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()
    nA = nB = 0
    made = set()

    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[A FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[A dry] 0x%08x ref->%s rename %s" % (slot_int, gas_label, slot_label)); nA += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED); made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[A ok] 0x%08x -> %s" % (slot_int, slot_label)); nA += 1

    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x rename %s%s" % (slot_int, label, " +EOL" if eol else "")); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[B ok] 0x%08x -> %s" % (slot_int, label)); nB += 1

    print("[done] A=%d B=%d (DRY=%s)" % (nA, nB, DRY))


main()
