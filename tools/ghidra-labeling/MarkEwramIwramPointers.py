# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# MarkEwramIwramPointers.py  (Jython 2.7 / Ghidra script)
#
# 扫 ROM 代码区 [0x080000C0, 0x084C7637] 所有 4-byte defined data:
#   - 若 data 值 ∈ [0x02000000, 0x03FFFFFF] (EWRAM / IWRAM)
#   - 且目标地址 primary symbol 是 USER_DEFINED (LabelDataCrystalRomMap 刷过)
#   - 且当前类型不是 pointer
#  则 clearCodeUnits + createData(Pointer), 让 Ghidra 自动建 outgoing reference。
#
# 配合 ExportRangeToGas.py 的 resolve_word_symbol() 后,asm/all.s 中这些字面量池
# 的 .word 会自动变成 .word <symbol>,指令侧 ldr 目标 label 变成 PTR_<symbol>_<addr>。
#
# 参数:
#   无参     = 实际应用改动
#   "dry"    = 仅打印候选数量和示例,不改 Ghidra
#
# 白名单与 ExportRangeToGas.py resolve_word_symbol() 保持一致:
#   - 只处理 EWRAM/IWRAM (0x02000000..0x03FFFFFF);
#   - ROM (0x08xxxxxx) 不处理,THUMB 函数 label 缺 |1 位会破坏 byte-identical;
#   - MMIO (0x04xxxxxx)/PALRAM/VRAM/OAM 不处理,Ghidra loader 给的寄存器名在
#     asm 里无 .equ 定义。

from jarray import zeros
from ghidra.program.model.data import PointerDataType
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.address import AddressSet

SCAN_START = 0x080000C0
SCAN_END   = 0x084C7637
EWRAM_LO   = 0x02000000
EWRAM_HI   = 0x03FFFFFF

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def read_u32_le(memory, addr):
    bs = zeros(4, 'b')
    memory.getBytes(addr, bs)
    v = 0
    for i in range(4):
        v |= (bs[i] & 0xff) << (i * 8)
    return v


def main():
    listing = currentProgram.getListing()
    memory = currentProgram.getMemory()
    symtab = currentProgram.getSymbolTable()

    start = toAddr(SCAN_START)
    end = toAddr(SCAN_END)
    scan_set = AddressSet(start, end)

    candidates = []  # (addr, val, symbol_name)
    skipped_already_pointer = 0
    scanned = 0

    for d in listing.getDefinedData(scan_set, True):
        scanned += 1
        if d.getLength() != 4:
            continue

        val = read_u32_le(memory, d.getAddress())
        if not (EWRAM_LO <= val <= EWRAM_HI):
            continue

        target = toAddr(val)
        sym = symtab.getPrimarySymbol(target)
        if sym is None:
            continue
        if sym.getSource() != SourceType.USER_DEFINED:
            continue

        dt = d.getDataType()
        if dt is not None and isinstance(dt, PointerDataType):
            skipped_already_pointer += 1
            continue

        candidates.append((d.getAddress(), val, sym.getName()))

    print("[scan] %d defined-data entries in range" % scanned)
    print("[scan] %d candidates (EWRAM/IWRAM + USER_DEFINED symbol)" % len(candidates))
    print("[scan] %d skipped (already Pointer type)" % skipped_already_pointer)

    for (addr, val, name) in candidates[:5]:
        print("[ex] %s -> 0x%08X = %s" % (addr, val, name))
    if len(candidates) > 5:
        print("[ex] ... (%d more)" % (len(candidates) - 5))

    if RUN_DRY:
        print("[dry] no changes applied")
        return

    applied = 0
    failed = 0
    for (addr, val, name) in candidates:
        try:
            listing.clearCodeUnits(addr, addr.add(3), False)
            createData(addr, PointerDataType.dataType)
            applied += 1
        except Exception as e:
            failed += 1
            print("[fail] %s: %s" % (addr, e))

    print("[done] applied=%d failed=%d" % (applied, failed))


main()
