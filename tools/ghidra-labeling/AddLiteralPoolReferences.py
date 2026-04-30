# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# AddLiteralPoolReferences.py  (Jython 2.7 / Ghidra script)
#
# 给字面量池 (literal pool) `.word <addr>` 条目添加 DATA reference 指向 <addr>,
# 让 ExportRangeToGas.py 把 raw `.word 0xNNNNNNNN` 符号化为 `.word <label_name>`.
#
# 起因 (2026-04-30):
#   通过 LabelDataCrystalRomMap.py 给 0x08000240 / 0x08000250 加了 USER_DEFINED label
#   (game_str_id_remap_count / game_str_id_remap_table), 但 game_str_id_to_row
#   函数体内字面量池 .word 0x08000240 没自动符号化, 因为没有 from-this-DAT 的 reference.
#
# 通用算法:
#   遍历所有 Defined Data 中 size==4 的 entry (字面量池 .word).
#   读其 32-bit value, 若 value 落在 ROM/EWRAM/IWRAM 范围且对应地址有 USER_DEFINED
#   或 IMPORTED label, 且当前没有 from-this-pool 的 ref -> 加 DATA ref.
#
# 命令行参数:
#   --dry  : 只打印, 不改动
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat AddLiteralPoolReferences.py
#   tools\asm-regen\ghidra-run-script.bat AddLiteralPoolReferences.py --dry

import sys

from ghidra.program.model.symbol import RefType, SourceType, SymbolType


RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


# 接受 ref 目标的地址范围 (要求 label 是 USER_DEFINED / IMPORTED)
ADDR_RANGES = [
    (0x02000000, 0x02040000),  # EWRAM
    (0x03000000, 0x03008000),  # IWRAM
    (0x04000000, 0x04000400),  # IO MMIO
    (0x05000000, 0x05000400),  # PALRAM
    (0x06000000, 0x06018000),  # VRAM
    (0x07000000, 0x07000400),  # OAM
    (0x08000000, 0x0A000000),  # ROM
]


def addr_in_range(v):
    for lo, hi in ADDR_RANGES:
        if lo <= v < hi:
            return True
    return False


def main():
    listing = currentProgram.getListing()
    sym_table = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()
    af = currentProgram.getAddressFactory()
    mem = currentProgram.getMemory()

    n_scanned = 0
    n_added = 0
    n_skip_no_label = 0
    n_skip_already_ref = 0
    n_skip_auto_label = 0
    samples = []

    data_iter = listing.getDefinedData(True)
    while data_iter.hasNext():
        d = data_iter.next()
        if d.getLength() != 4:
            continue
        n_scanned += 1
        from_addr = d.getAddress()
        # 跳过 EWRAM/IWRAM 的 .word entry: 它们是变量定义, 不是字面量池
        from_off = from_addr.getOffset() & 0xFFFFFFFF
        if not (0x08000000 <= from_off < 0x0A000000):
            continue
        try:
            val_bytes = mem.getInt(from_addr) & 0xFFFFFFFF
        except Exception:
            continue
        if not addr_in_range(val_bytes):
            continue
        target_addr = af.getAddress("0x%x" % val_bytes)
        if target_addr is None:
            continue
        # 必须有 USER_DEFINED 或 IMPORTED 的 primary symbol (或任意 USER_DEFINED 别名)
        psym = sym_table.getPrimarySymbol(target_addr)
        if psym is None:
            n_skip_no_label += 1
            continue
        src = psym.getSource()
        if src not in (SourceType.USER_DEFINED, SourceType.IMPORTED):
            n_skip_auto_label += 1
            continue
        # 检查是否已有 from-this-data 的 reference 指向 target
        existing = ref_mgr.getReferencesFrom(from_addr)
        already = False
        for r in existing:
            if r.getToAddress() == target_addr:
                already = True
                break
        if already:
            n_skip_already_ref += 1
            continue

        if not RUN_DRY:
            ref_mgr.addMemoryReference(
                from_addr, target_addr,
                RefType.DATA, SourceType.USER_DEFINED, 0)
        n_added += 1
        if len(samples) < 12:
            samples.append((
                "0x%08x" % from_addr.getOffset(),
                "0x%08x" % val_bytes,
                psym.getName(),
            ))

    mode = "[dry]" if RUN_DRY else "[done]"
    print("%s AddLiteralPoolReferences" % mode)
    print("  4-byte data entries scanned : %d" % n_scanned)
    print("  refs added                  : %d" % n_added)
    print("  skipped (no user label)     : %d" % n_skip_no_label)
    print("  skipped (auto label only)   : %d" % n_skip_auto_label)
    print("  skipped (already has ref)   : %d" % n_skip_already_ref)
    if samples:
        print("  samples (前 12):")
        for f, v, n in samples:
            print("    %s : .word %s -> %s" % (f, v, n))


main()
