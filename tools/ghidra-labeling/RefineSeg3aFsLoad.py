# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineSeg3aFsLoad.py — p5 Seg-3a (fs_load 0x14fa8..0x1510a)
#   R7 carve in rom.s: fs_key_lz_suffix/hash/excl + 6 fs_lang_char_* + fs_language_char_ptr_table
#   (rom.s 已切, incbin 0x3F → labeled .ascii + .word table)
#   9 pool 槽:
#   - 4 carve label ref+rename (hash/excl/lz/ptr_table)
#   - 1 equate ROM_REGION_CODE_ADDR (Seg-1a 复用)
#   - 1 global ref gFsDecompBuf (新 ewram.inc)
#   - 2 EWRAM base+offset (gSettings pattern, 同 Seg-1a/1b)
#   - 1 VRAM 边界阈值常量槽改名 (0x05ffffff, 保守命名 _vram_boundary)
# Usage: tools\asm-regen\ghidra-run-script.bat RefineSeg3aFsLoad.py [dry]
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# A. carve-label/global ref + rename (slot_addr, target_addr, gas_label, slot_label)
REF_SLOTS = [
 (0x0801507c, 0x09e39980, 'fs_key_hash',                'fs_load_ptr_key_hash'),
 (0x08015080, 0x09e399a0, 'fs_language_char_ptr_table', 'fs_load_ptr_language_char_table'),
 (0x08015090, 0x09e39984, 'fs_key_excl',                'fs_load_ptr_key_excl'),
 (0x08015098, 0x09e3997c, 'fs_key_lz_suffix',           'fs_load_ptr_key_lz_suffix'),
 (0x0801509c, 0x0200af20, 'gFsDecompBuf',               'fs_load_ptr_decomp_buf'),
]

# B. data-equate (slot_addr, value, const_name, slot_label) — ROM_REGION_CODE_ADDR 复用 Seg-1a
EQ_SLOTS = [
 (0x08015094, 0x080000ae, 'ROM_REGION_CODE_ADDR', 'fs_load_rom_region_code_addr'),
]

# C. plain slot rename (slot_addr, slot_label, eol_or_None)
RENAME_SLOTS = [
 (0x08015088, 'fs_load_ewram_base', None),
 (0x0801508c, 'fs_load_gsettings_offset', '= gSettings(0x02006c2c) - EWRAM base; bits[2:0]=language_id'),
 (0x080150a0, 'fs_load_vram_boundary_threshold', '= 0x06000000-1; dest <= 此值 -> LZ77 解压到 gFsDecompBuf, 否则直接 huff 到 dest'),
]


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
    print("=== RefineSeg3aFsLoad (DRY=%s) ===" % DRY)
    rm = currentProgram.getReferenceManager()
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = 0
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
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, slot_label, gas_label)); nA += 1

    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[B FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[B dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[B ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nB += 1

    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s%s" % (slot_int, label, " +EOL" if eol else "")); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))


main()
