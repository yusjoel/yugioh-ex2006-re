# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ExportFunctionInventory.py  (Jython 2.7 / Ghidra script)
#
# 遍历 Ghidra 工程当前 program 内的所有函数, 输出:
#   1) temp/ghidra-functions.csv               全量 (CSV: address,name,source,is_auto,is_thunk,length,namespace)
#   2) temp/ghidra-functions-renamed.txt       仅"已识别"(已 rename) 函数, 按地址升序
#   3) temp/ghidra-functions-auto.txt          仅"未识别"(FUN_/SUB_/thunk_FUN_ 自动命名) 函数
#   4) temp/ghidra-functions-summary.md        按地址段的小结 (BIOS / IWRAM 入口 / ROM main code / ROM data 段等)
#
# 同时往 stdout 打印总数 / 已识别 / 未识别 / 比例.
#
# 命名约定:
#   "auto"   = name 完全匹配 ^FUN_[0-9a-f]{8}$ / ^SUB_[0-9a-f]{8}$ / ^thunk_FUN_[0-9a-f]{8}$
#              (这些都是 Ghidra 自动占位符, 没人改过名)
#   "named"  = 其余一切. 即使是项目里没有提的函数, 只要被 rename 就计入"已识别".
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat ExportFunctionInventory.py

import os
import re

from ghidra.program.model.symbol import SourceType


AUTO_PATTERNS = [
    re.compile(r"^FUN_[0-9a-fA-F]{8}$"),
    re.compile(r"^SUB_[0-9a-fA-F]{8}$"),
    re.compile(r"^thunk_FUN_[0-9a-fA-F]{8}$"),
]


def is_auto_name(name):
    for pat in AUTO_PATTERNS:
        if pat.match(name):
            return True
    return False


def repo_root():
    """ghidra-labeling/ 上面两层就是仓库根."""
    try:
        src = getSourceFile().getAbsolutePath()
        return os.path.dirname(os.path.dirname(os.path.dirname(src)))
    except Exception:
        return os.getcwd()


def safe_csv(s):
    if s is None:
        return ""
    s = str(s)
    if "," in s or '"' in s or "\n" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def main():
    root = repo_root()
    out_dir = os.path.join(root, "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    fm = currentProgram.getFunctionManager()
    funcs = fm.getFunctions(True)  # iterator, ascending by address

    csv_path = os.path.join(out_dir, "ghidra-functions.csv")
    renamed_path = os.path.join(out_dir, "ghidra-functions-renamed.txt")
    auto_path = os.path.join(out_dir, "ghidra-functions-auto.txt")
    summary_path = os.path.join(out_dir, "ghidra-functions-summary.md")

    fcsv = open(csv_path, "w")
    frenamed = open(renamed_path, "w")
    fauto = open(auto_path, "w")

    fcsv.write("address,name,source,is_auto,is_thunk,length,namespace\n")

    total = 0
    auto_count = 0
    named_count = 0
    thunk_count = 0
    by_source = {}             # SourceType -> count
    named_by_source = {}       # SourceType -> count (only 'named')
    auto_by_source = {}        # SourceType -> count (only 'auto')

    # 按地址段做粗分类, 用于 summary.md
    BUCKETS = [
        ("ROM main code  [0x08000000-0x084C7637]", 0x08000000, 0x084C7637),
        ("ROM data area  [0x084C7638-0x09FFFFFF]", 0x084C7638, 0x09FFFFFF),
        ("EWRAM          [0x02000000-0x0203FFFF]", 0x02000000, 0x0203FFFF),
        ("IWRAM          [0x03000000-0x03007FFF]", 0x03000000, 0x03007FFF),
        ("BIOS           [0x00000000-0x00003FFF]", 0x00000000, 0x00003FFF),
    ]
    bucket_total = [0] * len(BUCKETS)
    bucket_named = [0] * len(BUCKETS)

    for f in funcs:
        ep = f.getEntryPoint()
        addr_int = ep.getOffset()
        name = f.getName()
        sym = f.getSymbol()
        src = sym.getSource().toString() if sym is not None else "UNKNOWN"
        ns = f.getParentNamespace().getName() if f.getParentNamespace() is not None else ""
        length = f.getBody().getNumAddresses() if f.getBody() is not None else 0
        thunk = f.isThunk()
        auto = is_auto_name(name)

        total += 1
        if thunk:
            thunk_count += 1
        if auto:
            auto_count += 1
            auto_by_source[src] = auto_by_source.get(src, 0) + 1
        else:
            named_count += 1
            named_by_source[src] = named_by_source.get(src, 0) + 1
        by_source[src] = by_source.get(src, 0) + 1

        for i, (label, lo, hi) in enumerate(BUCKETS):
            if lo <= addr_int <= hi:
                bucket_total[i] += 1
                if not auto:
                    bucket_named[i] += 1
                break

        addr_hex = "0x%08x" % addr_int
        fcsv.write("%s,%s,%s,%d,%d,%d,%s\n" % (
            addr_hex,
            safe_csv(name),
            src,
            1 if auto else 0,
            1 if thunk else 0,
            length,
            safe_csv(ns),
        ))

        line = "%s  %s\n" % (addr_hex, name)
        if auto:
            fauto.write(line)
        else:
            frenamed.write(line)

    fcsv.close()
    frenamed.close()
    fauto.close()

    # --- summary.md ---
    fsum = open(summary_path, "w")
    fsum.write("# Ghidra Function Inventory\n\n")
    fsum.write("Program: `%s`\n\n" % currentProgram.getName())
    pct = (100.0 * named_count / total) if total else 0.0
    fsum.write("- Total functions: **%d**\n" % total)
    fsum.write("- Named (renamed/identified): **%d** (%.2f%%)\n" % (named_count, pct))
    fsum.write("- Auto (`FUN_*` / `SUB_*` / `thunk_FUN_*`): **%d** (%.2f%%)\n" % (
        auto_count, 100.0 - pct))
    fsum.write("- Thunks: %d\n\n" % thunk_count)

    fsum.write("## By symbol source\n\n")
    fsum.write("| Source | Total | Named | Auto |\n")
    fsum.write("|--------|------:|------:|-----:|\n")
    for src in sorted(by_source.keys()):
        fsum.write("| %s | %d | %d | %d |\n" % (
            src,
            by_source.get(src, 0),
            named_by_source.get(src, 0),
            auto_by_source.get(src, 0),
        ))
    fsum.write("\n")

    fsum.write("## By address range\n\n")
    fsum.write("| Range | Total | Named | Named % |\n")
    fsum.write("|-------|------:|------:|--------:|\n")
    for i, (label, lo, hi) in enumerate(BUCKETS):
        bt = bucket_total[i]
        bn = bucket_named[i]
        bp = (100.0 * bn / bt) if bt else 0.0
        fsum.write("| %s | %d | %d | %.2f%% |\n" % (label, bt, bn, bp))
    fsum.write("\n")

    fsum.write("## Outputs\n\n")
    fsum.write("- `temp/ghidra-functions.csv` (full list)\n")
    fsum.write("- `temp/ghidra-functions-renamed.txt` (named only)\n")
    fsum.write("- `temp/ghidra-functions-auto.txt` (auto only)\n")
    fsum.close()

    # --- stdout ---
    print("[done] ExportFunctionInventory.py")
    print("  total       = %d" % total)
    print("  named       = %d  (%.2f%%)" % (named_count, pct))
    print("  auto FUN_*  = %d  (%.2f%%)" % (auto_count, 100.0 - pct))
    print("  thunks      = %d" % thunk_count)
    print("  -> %s" % csv_path)
    print("  -> %s" % renamed_path)
    print("  -> %s" % auto_path)
    print("  -> %s" % summary_path)


main()
