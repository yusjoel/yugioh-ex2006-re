# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateLangSelectGfx.py  (Jython 2.7 / Ghidra 12.x)
#
# 1) 给语言选择 4 个图形块起始地址加 USER_DEFINED label (lang_select_gfx_0..3),
#    并给 render_lang_select 字面量池 .word 加 DATA ref ->
#    ExportRangeToGas.resolve_word_symbol 把 .word 0x0800aa10 等符号化为
#    .word lang_select_gfx_N (定义在 data/lang-select-tiles.s)。
# 2) 更新 write_tile_row_to_vram plate (原注释含旧 FUN_ 名 + map 项格式不准)。
#
# 备份: 调用前已 cp .rep 到 .bak-<ts>-pre-langsel-gfx
# Usage: tools\asm-regen\ghidra-run-script.bat AnnotateLangSelectGfx.py [dry]

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType
from java.lang import Exception as JavaException

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (block 起始地址, label)
GFX = [
    (0x0800aa10, "lang_select_gfx_0"),
    (0x0800b588, "lang_select_gfx_1"),
    (0x0800c240, "lang_select_gfx_2"),
    (0x0800cd18, "lang_select_gfx_3"),
]
# render_lang_select 字面量池 .word (pool_addr -> 目标 block)
POOL_REFS = [
    (0x080ebcb4, 0x0800b588),
    (0x080ebcb8, 0x0800aa10),
    (0x080ebcbc, 0x0800c240),
    (0x080ebcc0, 0x0800cd18),
]

WTR_PLATE = (
    u"由 load_pack_tile_and_map_to_vram 与 init_duel_field_icon_and_bg_vram 调用. "
    u"从 r3 指向的图形块取 map 子块 (在 palette+tile 子块之后, 格式 "
    u"[u16 count][6B][count×4B]), 逐项把 BG tilemap 写入 VRAM. 每项 2×u16: "
    u"A = (Y<<8)|X (X=A&0x3f 列, Y=A>>8 行; X>31 走第二 screenblock; 屏幕位置 = "
    u"X + Y*32 + param0); B = GBA BG tilemap 项 (B&0x3ff = tile 索引 + param2 base, "
    u"B&0x400 = hflip, B&0x800 = vflip, B&0xf000 = 调色板). VRAM 目标 = "
    u"0x06000000 + screenblock + 位置*2. 参数: r0=param0 屏幕位置基址, "
    u"r2=param2 tile 基号, r3=图形块指针."
)


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== AnnotateLangSelectGfx (DRY=%s) ===" % DRY)
    st = currentProgram.getSymbolTable()
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()

    # 1a) labels
    for addr_int, name in GFX:
        a = _addr(addr_int)
        sym = st.getPrimarySymbol(a)
        if sym is not None and sym.getName() == name:
            print("[skip] label %s exists" % name)
            continue
        if DRY:
            print("[dry]  label %s @ 0x%08x" % (name, addr_int))
            continue
        createLabel(a, name, True, SourceType.USER_DEFINED)
        print("[ok]   label %s @ 0x%08x" % (name, addr_int))

    # 1b) pool .word -> block DATA ref
    for from_int, to_int in POOL_REFS:
        fa = _addr(from_int)
        ta = _addr(to_int)
        have = any(r.getToAddress() == ta for r in rm.getReferencesFrom(fa))
        if have:
            print("[skip] ref 0x%08x->0x%08x exists" % (from_int, to_int))
            continue
        if DRY:
            print("[dry]  ref 0x%08x -> 0x%08x" % (from_int, to_int))
            continue
        rm.addMemoryReference(fa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
        print("[ok]   ref 0x%08x -> 0x%08x" % (from_int, to_int))

    # 2) write_tile_row_to_vram plate
    a = _addr(0x080edf4c)
    cu = listing.getCodeUnitAt(a)
    if cu is not None:
        if DRY:
            print("[dry]  update plate @ 0x080edf4c (%d chars)" % len(WTR_PLATE))
        else:
            cu.setComment(CodeUnit.PLATE_COMMENT, WTR_PLATE)
            print("[ok]   plate @ 0x080edf4c (write_tile_row_to_vram)")

    print("[done] AnnotateLangSelectGfx (DRY=%s)" % DRY)


main()
