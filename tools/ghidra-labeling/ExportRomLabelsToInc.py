# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ExportRomLabelsToInc.py  (Jython 2.7 / Ghidra script)
#
# 扫 Ghidra symbol table,把 ROM 段 [0x084C7638, 0x09FFFFFF] 所有 USER_DEFINED
# SymbolType.LABEL 写到 constants/rom_data.inc (每条一行 .equ)。
#
# 范围下界 0x084C7638 = asm/all.s 导出范围的上界 + 1:
#   - asm/all.s 范围 [0x080000C0, 0x084C7637] 内的 label 由 asm 源自身 label: 提供
#     (asm/all.s 里的 FUN_*/LAB_*/DAT_* 由 GAS 在汇编阶段 resolve)
#   - 0x084C7638+ 是纯 data 段 (data/*.s 用 .incbin 引入,不含 asm label)
#     这部分 symbol 必须靠 .equ 才能被 .word <name> 引用
#
# 排除:
#   - Ghidra auto-gen 前缀 (DAT_/LAB_/FUN_/PTR_/SUB_/UNK_/SWITCH_)
#   - SymbolType.FUNCTION (只在 ROM 数据段扫,函数入口不应出现在此范围)
#
# 触发 asm/rom.s 接入:
#   .include "constants/rom_data.inc"  (紧跟 ewram/iwram/gba_io)
#
# 无参数: 生成并写文件; "dry" 参数则只打印统计不写文件。

import codecs
import os
import re
from ghidra.program.model.symbol import SymbolType, SourceType

RANGE_LO = 0x084C7638
RANGE_HI = 0x09FFFFFF

AUTO_PREFIXES = ("DAT_", "LAB_", "FUN_", "PTR_", "SUB_", "UNK_", "SWITCH_")

RUN_DRY = False
try:
    _args = list(getScriptArgs())
    if _args and _args[0].lower() in ("dry", "--dry", "1", "true"):
        RUN_DRY = True
except Exception:
    pass


def scan_existing_asm_labels(repo_root):
    """
    扫 data/*.s 和 asm/*.s 里已有的 `^name:` label,返回 set。
    这些 label 已由 asm 源自身定义,rom_data.inc 不应重复 .equ (否则 GAS 会报
    symbol redefinition)。典型: data/card-stats.s 的 5170 个 card_XXXX:。
    """
    label_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")
    existing = set()
    for sub in ("data", "asm"):
        d = os.path.join(repo_root, sub)
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if not fname.endswith(".s"):
                continue
            p = os.path.join(d, fname)
            try:
                f = open(p, "r")
            except IOError:
                continue
            try:
                for line in f:
                    m = label_re.match(line)
                    if m:
                        existing.add(m.group(1))
            finally:
                f.close()
    return existing


def main():
    symtab = currentProgram.getSymbolTable()

    repo_root = os.environ.get("REPO_ROOT") or os.getcwd()
    existing = scan_existing_asm_labels(repo_root)
    print("[scan] existing asm labels in data/*.s + asm/*.s: %d" % len(existing))

    rows = []
    seen_names = set()
    skipped_asm_defined = 0
    for s in symtab.getAllSymbols(True):
        if s.getSymbolType() != SymbolType.LABEL:
            continue
        if s.getSource() != SourceType.USER_DEFINED:
            continue

        addr = s.getAddress().getOffset()
        if not (RANGE_LO <= addr <= RANGE_HI):
            continue

        name = s.getName()
        if any(name.startswith(p) for p in AUTO_PREFIXES):
            continue
        if name in existing:
            skipped_asm_defined += 1
            continue
        if name in seen_names:
            continue
        seen_names.add(name)

        rows.append((addr, name))

    rows.sort()

    print("[scan] %d ROM LABEL symbols in [0x%08X, 0x%08X]" %
          (len(rows), RANGE_LO, RANGE_HI))
    print("[scan] %d skipped (already defined as label in asm/*.s or data/*.s)" %
          skipped_asm_defined)
    for addr, name in rows[:5]:
        print("  0x%08X = %s" % (addr, name))
    if len(rows) > 5:
        print("  ... (%d more)" % (len(rows) - 5))

    if RUN_DRY:
        print("[dry] not writing file")
        return

    # 写 constants/rom_data.inc
    # 通过环境变量或 Ghidra 当前目录判断 repo root;保守用绝对路径重建
    repo_root = os.environ.get("REPO_ROOT")
    if not repo_root:
        # headless bat 脚本的 CWD 是 repo 根
        repo_root = os.getcwd()
    out_path = os.path.join(repo_root, "constants", "rom_data.inc")

    w = max([len(n) for _, n in rows]) if rows else 12
    lines = [
        "@ =============================================================================",
        "@ ROM data-section USER_DEFINED LABEL symbols",
        "@ Source: Ghidra symbol table (refs/gba-ghidra-loader + project scripts)",
        "@ Generator: tools/ghidra-labeling/ExportRomLabelsToInc.py",
        "@",
        "@ Range: [0x%08X, 0x%08X] (past asm/all.s upper bound)" % (RANGE_LO, RANGE_HI),
        "@ Usage: .word <name> in asm; GAS substitutes via .equ",
        "@ =============================================================================",
        "",
    ]
    for addr, name in rows:
        lines.append(".equ %-*s 0x%08X" % (w, name + ",", addr))

    f = open(out_path, "w")
    try:
        f.write("\n".join(lines) + "\n")
    finally:
        f.close()

    print("[done] wrote %s" % out_path)


main()
