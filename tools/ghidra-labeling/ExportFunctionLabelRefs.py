# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# ExportFunctionLabelRefs.py  (Jython 2.7 / Ghidra script)
#
# 方法 3 - 数据 label 反向查询 (function-naming.md §五).
# 只读: 不 createFunction / 不 setName / 不动 program.
#
# 思路: 已落地的语义化 data label (USER_DEFINED) 标记了模块边界. 引用这些
# label 的函数大概率属于该模块. 一次性扫所有 label -> ref -> 包含函数,
# 给每个函数累计 "命中了哪些 label / 每个 label 命中几次", 落 CSV 给后续
# Python merger 派生 family 前缀和 score.
#
# 过滤 (与 prompt 一致):
#   - SymbolType == LABEL                (排除 FUNCTION / NAMESPACE / 等)
#   - SourceType in {USER_DEFINED, IMPORTED}
#   - 名字不以 DAT_/LAB_/PTR_/SUB_/FUN_/thunk_FUN_/UNK_/SWITCH_ 开头
#   - 地址在 [0x08000000, 0x09FFFFFF]    (跳过 EWRAM/IWRAM/MMIO)
#
# 输出: temp/ghidra-funcs-label-refs.csv
#   columns: address, name, total_hits, unique_labels, top_labels
#   top_labels = "label1(N)|label2(N)|..."  最多 5 条 (按命中数降序)
#
# 用法:
#   tools\asm-regen\ghidra-run-script.bat ExportFunctionLabelRefs.py

import os
import re

from ghidra.program.model.symbol import SymbolType, SourceType


LABEL_RANGE_LO = 0x08000000
LABEL_RANGE_HI = 0x09FFFFFF

AUTO_PREFIXES = ("DAT_", "LAB_", "PTR_", "SUB_", "FUN_", "thunk_FUN_",
                 "UNK_", "SWITCH_", "EXT_", "OFF_")

TOP_K = 5  # CSV top_labels 列保留前 K 条


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


def is_auto_name(name):
    for p in AUTO_PREFIXES:
        if name.startswith(p):
            return True
    return False


def main():
    root = repo_root()
    out_dir = os.path.join(root, "temp")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    symtab = currentProgram.getSymbolTable()
    rm = currentProgram.getReferenceManager()
    fm = currentProgram.getFunctionManager()

    # func_addr_int -> {label_name: hit_count}
    func_to_labels = {}
    func_to_name = {}

    n_labels_total = 0
    n_labels_kept = 0
    n_refs_total = 0
    n_refs_in_func = 0
    n_refs_outside = 0

    # 分布统计 (粗分桶)
    bucket_counts = {
        "rom_main_code [0x080000C0-0x084C7637]": 0,
        "rom_data      [0x084C7638-0x09FFFFFF]": 0,
    }

    for sym in symtab.getDefinedSymbols():
        n_labels_total += 1
        if sym.getSymbolType() != SymbolType.LABEL:
            continue
        src = sym.getSource()
        if src not in (SourceType.USER_DEFINED, SourceType.IMPORTED):
            continue
        name = sym.getName()
        if is_auto_name(name):
            continue
        addr_int = sym.getAddress().getOffset() & 0xFFFFFFFF
        if not (LABEL_RANGE_LO <= addr_int <= LABEL_RANGE_HI):
            continue

        n_labels_kept += 1
        if 0x080000C0 <= addr_int <= 0x084C7637:
            bucket_counts["rom_main_code [0x080000C0-0x084C7637]"] += 1
        else:
            bucket_counts["rom_data      [0x084C7638-0x09FFFFFF]"] += 1

        for ref in rm.getReferencesTo(sym.getAddress()):
            n_refs_total += 1
            from_addr = ref.getFromAddress()
            f = fm.getFunctionContaining(from_addr)
            if f is None:
                n_refs_outside += 1
                continue
            n_refs_in_func += 1
            ep = f.getEntryPoint().getOffset() & 0xFFFFFFFF
            d = func_to_labels.get(ep)
            if d is None:
                d = {}
                func_to_labels[ep] = d
                func_to_name[ep] = f.getName()
            d[name] = d.get(name, 0) + 1

    # --- 写 CSV ---
    csv_path = os.path.join(out_dir, "ghidra-funcs-label-refs.csv")
    fcsv = open(csv_path, "w")
    fcsv.write("address,name,total_hits,unique_labels,top_labels\n")

    rows = sorted(func_to_labels.items(), key=lambda kv: kv[0])
    for ep, labels in rows:
        total_hits = sum(labels.values())
        unique = len(labels)
        # 按命中降序, 同命中按名字升序
        sorted_labels = sorted(labels.items(), key=lambda kv: (-kv[1], kv[0]))
        top = sorted_labels[:TOP_K]
        top_str = "|".join("%s(%d)" % (n, c) for n, c in top)
        fcsv.write("0x%08x,%s,%d,%d,%s\n" % (
            ep,
            safe_csv(func_to_name.get(ep, "")),
            total_hits,
            unique,
            safe_csv(top_str),
        ))
    fcsv.close()

    # --- stdout ---
    print("[done] ExportFunctionLabelRefs.py")
    print("  defined symbols total scanned : %d" % n_labels_total)
    print("  labels kept (USER_DEFINED/IMPORTED, in ROM, non-auto): %d" % n_labels_kept)
    for k in sorted(bucket_counts.keys()):
        print("    %s : %d" % (k, bucket_counts[k]))
    print("  references found : %d" % n_refs_total)
    print("    in func body  : %d" % n_refs_in_func)
    print("    outside func  : %d  (data->data refs / 跳过)" % n_refs_outside)
    print("  functions touched : %d" % len(func_to_labels))
    print("  -> %s" % csv_path)


main()
