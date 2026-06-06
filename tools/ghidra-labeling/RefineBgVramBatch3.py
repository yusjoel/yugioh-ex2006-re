# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineBgVramBatch3.py — p5 batch-3 (BG VRAM 地址簇 0x14a10..0x14e14, 24 fn)
#   R2: 8 个 auto-name 槽改语义名 (2 scroll-reg DWORD + 1 OBJ base + 5 assert-line DAT)
#   R1: data-equate OBJ_TILE_VRAM_BASE(0x06010000) @0x14c10 -> resolve_word_equate 导出符号
#       (constants/gba_mem.inc .equ 解析回值)
#   R5: 2 plate targeted (get_obj_tile_vram_base / copy_to_obj_tile_vram 的 DAT_/0x06010000 引用)
#   注: PTR_BGxCNT_xxxx 槽按 batch-2 策略跳过 (PTR 不在 R2 列表, 已显寄存器名)
# Usage: tools\asm-regen\ghidra-run-script.bat RefineBgVramBatch3.py [dry]
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# --- A. data-equate (slot_addr, value, const_name, slot_label) ---
EQ_SLOTS = [
 (0x08014c10, 0x06010000, 'OBJ_TILE_VRAM_BASE', 'get_obj_tile_vram_base_obj_tile_vram_base'),
]

# --- B. rename-only 槽 (slot_addr, expect_value_or_None, slot_label) ---
RENAME_ONLY = [
 (0x08014b84, None, 'write_bg_scroll_pair_ptr_bg0hofs'),      # .word BG0HOFS (已 ref)
 (0x08014b88, None, 'write_bg_scroll_pair_ptr_bg0vofs'),      # .word BG0VOFS (已 ref)
 (0x08014c8c, 0x000001e7, 'copy_to_bg1_char_tiles_assert_line'),   # 行 487
 (0x08014d0c, 0x000001f1, 'copy_to_bg3_char_tiles_assert_line'),   # 行 497
 (0x08014d4c, 0x000001f7, 'copy_to_bg0_screen_map_assert_line'),   # 行 503
 (0x08014dcc, 0x00000201, 'copy_to_bg2_screen_map_assert_line'),   # 行 513
 (0x08014e0c, 0x00000206, 'copy_to_bg3_screen_map_assert_line'),   # 行 518
]

# --- C. plate targeted (addr -> [(old, new), ...]) ---
PLATE_REPL = {
 0x08014c0c: [
  (u"Body: ldr r0, DAT_08014c10; bx lr.", u"Body: ldr r0, OBJ_TILE_VRAM_BASE; bx lr."),
 ],
 0x08014e14: [
  (u"0x06010000 = OBJ tile VRAM base.", u"OBJ_TILE_VRAM_BASE (0x06010000) = OBJ tile VRAM base."),
 ],
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    if want is not None:
        try:
            dv = d.getValue()
            iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, "getValue") else (int(dv) & 0xffffffff)
        except Exception:
            iv = None
        if iv is not None and iv != (want & 0xffffffff):
            return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineBgVramBatch3 (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nB = nC = 0

    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label)); nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    for slot_int, want, label in RENAME_ONLY:
        ok, err = _check(slot_int, want)
        if not ok:
            print("[B FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[B dry] 0x%08x rename %s" % (slot_int, label)); nB += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s" % (slot_int, label)); nB += 1

    for addr_int in sorted(PLATE_REPL.keys()):
        cu = listing.getCodeUnitAt(_addr(addr_int))
        txt = cu.getComment(CodeUnit.PLATE_COMMENT) if cu else None
        if txt is None:
            print("[C FAIL] no plate @ 0x%08x" % addr_int); continue
        new = txt
        ok = True
        for old, rep in PLATE_REPL[addr_int]:
            if old not in new:
                print("[C FAIL] 0x%08x pattern not found: %r" % (addr_int, old[:40])); ok = False; continue
            new = new.replace(old, rep)
        if not ok or new == txt:
            continue
        if DRY:
            print("[C dry] 0x%08x plate update" % addr_int); nC += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new)
        print("[C ok] 0x%08x plate updated" % addr_int); nC += 1

    print("[done] A=%d B=%d C=%d (DRY=%s)" % (nA, nB, nC, DRY))


main()
