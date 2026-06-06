# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixSeg1bSeg3aEOLAscii.py — 订正 Seg-1b/Seg-3a 2 处 CJK EOL 的 Jython 双重 UTF-8 编码 mojibake
#   覆盖 feedback_jython_unicode_plate_comment.md: Ghidra Jython 写非 ASCII EOL 会双重编码,
#   纯 ASCII 重写避坑。
from ghidra.program.model.listing import CodeUnit

FIX_EOL = {
 # Seg-1b: copy_str_unbounded_len_sentinel (was "无上限哨兵")
 0x0801447c: "= 99,999,999 (0x5f5e0ff) sentinel meaning no upper-bound length",
 # Seg-3a: fs_load_vram_boundary_threshold (was "此值/解压到/否则直接/到")
 0x080150a0: "= 0x06000000-1 (VRAM boundary - 1); dest <= this -> LZ77 decompress to gFsDecompBuf, otherwise direct huff/lz to dest",
}


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    listing = currentProgram.getListing()
    n = 0
    for addr_int, text in FIX_EOL.items():
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu is None:
            print("[FAIL] no CU @ 0x%08x" % addr_int); continue
        cu.setComment(CodeUnit.EOL_COMMENT, text)
        print("[ok] 0x%08x EOL ASCII rewrite" % addr_int); n += 1
    print("[done] %d (DRY=False)" % n)


main()
