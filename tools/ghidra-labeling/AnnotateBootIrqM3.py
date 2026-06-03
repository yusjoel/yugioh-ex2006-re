# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AnnotateBootIrqM3.py  (Jython 2.7 / Ghidra 12.x)
#
# 里程碑 3: boot/IRQ 区字面量池指针符号化 + IntrMain 关键行 EOL 注释。
#   1) 建 USER_DEFINED 标签 INTR_VECTOR@0x03007ffc / gIntrTable@0x03000000
#   2) 给字面量池 .word 加 DATA ref (值符号化, 经 ExportRangeToGas.resolve_word_symbol)
#        0x0800022c -> 0x03007ffc ; 0x08000234 -> 0x03000000
#   3) rename 池槽: 0x0800022c->ptr_intr_vector, 0x08000230->ptr_run_game_main,
#        0x08000234->ptr_gIntrTable
#   4) IntrMain 关键行 EOL 注释
# GAS 端靠 constants/iwram.inc 的 INTR_VECTOR/gIntrTable .equ 解析 -> byte-identical。
#
# Usage: tools\asm-regen\ghidra-run-script.bat AnnotateBootIrqM3.py [dry]

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType, SymbolType
from java.lang import Exception as JavaException

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

RAM_LABELS = [
    (0x03007ffc, "INTR_VECTOR"),
    (0x03000000, "gIntrTable"),
]
# (pool_word_addr, target_ram_addr)
POOL_REFS = [
    (0x0800022c, 0x03007ffc),
    (0x08000234, 0x03000000),
]
POOL_RENAMES = [
    (0x0800022c, "ptr_intr_vector"),
    (0x08000230, "ptr_run_game_main"),
    (0x08000234, "ptr_gIntrTable"),
]
EOL = [
    (0x08000104, u"r2 = REG_IF<<16 | REG_IE"),
    (0x0800011c, u"r1 = IE & IF (已使能且挂起的中断)"),
    (0x08000124, u"优先级扫描起点: 槽0 = Serial|Timer3 (0xc0)"),
    (0x080001b8, u"GamePak(卡带拔出) → 关 SOUNDCNT_X (0x4000084)"),
    (0x080001c0, u"REG_IF = r0 (写 1 应答已处理中断)"),
    (0x080001d0, u"REG_IE = 允许嵌套的中断子集 (0x26c0)"),
    (0x080001ec, u"r0 = gIntrTable[槽] = 该中断的 Thumb ISR 指针"),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== AnnotateBootIrqM3 (DRY=%s) ===" % DRY)
    st = currentProgram.getSymbolTable()
    rm = currentProgram.getReferenceManager()
    listing = currentProgram.getListing()

    # 1) RAM 标签
    for addr_int, name in RAM_LABELS:
        a = _addr(addr_int)
        existing = st.getPrimarySymbol(a)
        if existing is not None and existing.getName() == name:
            print("[skip] label %s exists" % name)
            continue
        if DRY:
            print("[dry]  create label %s @ 0x%08x" % (name, addr_int))
            continue
        createLabel(a, name, True, SourceType.USER_DEFINED)
        print("[ok]   label %s @ 0x%08x" % (name, addr_int))

    # 2) 池 .word -> RAM 的 DATA ref
    for from_int, to_int in POOL_REFS:
        fa = _addr(from_int)
        ta = _addr(to_int)
        have = False
        for r in rm.getReferencesFrom(fa):
            if r.getToAddress() == ta:
                have = True
                break
        if have:
            print("[skip] ref 0x%08x->0x%08x exists" % (from_int, to_int))
            continue
        if DRY:
            print("[dry]  ref 0x%08x -> 0x%08x" % (from_int, to_int))
            continue
        rm.addMemoryReference(fa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
        print("[ok]   ref 0x%08x -> 0x%08x" % (from_int, to_int))

    # 3) 池槽 rename
    for addr_int, name in POOL_RENAMES:
        a = _addr(addr_int)
        sym = st.getPrimarySymbol(a)
        if sym is None:
            # 该地址无 symbol (如 M1 定义的 Dword 未带 label) -> 直接建 label
            if DRY:
                print("[dry]  create label %s @ 0x%08x" % (name, addr_int))
                continue
            createLabel(a, name, True, SourceType.USER_DEFINED)
            print("[ok]   create label 0x%08x -> %s" % (addr_int, name))
            continue
        if sym.getName() == name:
            print("[skip] 0x%08x already %s" % (addr_int, name))
            continue
        if DRY:
            print("[dry]  rename 0x%08x %s -> %s" % (addr_int, sym.getName(), name))
            continue
        sym.setName(name, SourceType.USER_DEFINED)
        print("[ok]   rename 0x%08x -> %s" % (addr_int, name))

    # 4) EOL 注释
    for addr_int, text in EOL:
        a = _addr(addr_int)
        cu = listing.getCodeUnitAt(a)
        if cu is None:
            print("[warn] no cu @ 0x%08x" % addr_int)
            continue
        if DRY:
            print("[dry]  eol @ 0x%08x: %s" % (addr_int, text))
            continue
        cu.setComment(CodeUnit.EOL_COMMENT, text)
        print("[ok]   eol @ 0x%08x" % addr_int)

    print("[done] AnnotateBootIrqM3 (DRY=%s)" % DRY)


main()
