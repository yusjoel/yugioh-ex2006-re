#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_fs_load_strings_to_proposals.py  --  方法 4: 字符串泄漏锚

输入  temp/ghidra-fs-load-strings-recursive.csv  ScanFsLoadStringsRecursive.py 的输出
       (回退到 ghidra-fs-load-strings.csv 若 recursive 不存在)
       doc/dev/naming-proposals.csv               现有提案
输出  doc/dev/naming-proposals.csv (in-place)

派生策略:
    每个 fs_load caller 加载的多个 path 共享一级目录 (demo / titleEx / ...) →
    映射到 module (PATH_PREFIX_TO_MODULE).
    若 caller 加载的 path 全在同一 module → 给 caller tag = <module> (直接证据)
    score 设定:
        N >= 2 个 path 同模块 → score = 4
        N == 1 个 path        → score = 3
    多模块混合 (caller 加载横跨多 path 前缀) → 跳过 (罕见)

跳过条件 (caller 不被 tag):
    - proposed_name 已非空 (尊重既有提案; 但如果是 method 3 propagate 占位
      "<prefix>_<8hex>" + score=2, 视为弱提案, 允许 method 4 升级覆盖)
    - score == 5 (FID 强证据)
    - 已 Ghidra 命名: 只追加 module tag, 不动 proposed_name/score

附加清理:
    若 caller 因路径锚定到模块 M, 同时 tags 含 'via_fs' (来自 method 3 扩散),
    删除 via_fs (path 锚是 fs 调用关系的精确化, via_fs 已冗余).

CSV tag 格式: 单 token, 无 key:value, 无括号.
"""

import csv
import os
import re
import sys
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    derive_module_from_path,
    MODULE_TO_PREFIX, ALL_MODULES,
    is_auto_name,
)

FS_STRINGS_RECURSIVE = os.path.join(
    REPO_ROOT, "temp", "ghidra-fs-load-strings-recursive.csv")
FS_STRINGS_LEGACY = os.path.join(
    REPO_ROOT, "temp", "ghidra-fs-load-strings.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")

FS_LOAD_ADDR = "0x08014fa8"

# 占位提案模式: <prefix>_<8hex> (来自 propagate 扩散), 视为弱提案可被 method 4 覆盖
PROPAGATE_PROPOSED_RE = re.compile(r"^[a-z_]+_[0-9a-f]{8}$")


def parse_tags(s):
    if not s:
        return []
    return [t.strip() for t in s.split(";") if t.strip()]


def main():
    # 优先用 recursive 输出, fallback 到 legacy
    if os.path.isfile(FS_STRINGS_RECURSIVE):
        fs_csv = FS_STRINGS_RECURSIVE
        is_recursive = True
    elif os.path.isfile(FS_STRINGS_LEGACY):
        fs_csv = FS_STRINGS_LEGACY
        is_recursive = False
    else:
        sys.stderr.write("ERROR: 没找到 fs-load-strings CSV; 先跑 "
                         "ScanFsLoadStringsRecursive.py 或 ScanFsLoadStrings.py\n")
        return 1
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1
    print("[load] using %s" % fs_csv)

    # caller_addr -> [(string_addr, string_value), ...]
    caller_paths = defaultdict(list)
    # wrapper_addr -> set(模块) (chain 中间节点, 透传具体模块的 path)
    wrapper_modules = defaultdict(set)
    with open(fs_csv, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ca = r["caller_addr"].lower()
            caller_paths[ca].append((r["string_addr"], r["string_value"]))
            # 若是 recursive 输出, target_addr ≠ fs_load 时 target 是 wrapper
            if is_recursive:
                ta = r.get("target_addr", "").lower()
                if ta and ta != FS_LOAD_ADDR.lower():
                    m = derive_module_from_path(r["string_value"])
                    if m:
                        wrapper_modules[ta].add(m)
    print("[load] %d unique callers from fs-load-strings" % len(caller_paths))
    if wrapper_modules:
        print("[load] %d wrapper functions identified (透传 path)" %
              len(wrapper_modules))

    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    rows_by_addr = {r["address"].lower(): r for r in rows}

    buckets = {
        "tag_score3": 0,
        "tag_score4": 0,
        "skip_already_proposed_strong": 0,
        "skip_score5": 0,
        "tag_only_named_func": 0,
        "skip_multi_module": 0,
        "skip_no_module": 0,
        "skip_caller_not_in_csv": 0,
        "via_fs_removed": 0,
    }
    samples = []

    for caller, items in sorted(caller_paths.items()):
        if caller not in rows_by_addr:
            buckets["skip_caller_not_in_csv"] += 1
            continue
        row = rows_by_addr[caller]

        # 派生每个 path 的 module
        modules = set()
        path_strs = []
        for _, sv in items:
            m = derive_module_from_path(sv)
            if m:
                modules.add(m)
            path_strs.append(sv)
        if not modules:
            buckets["skip_no_module"] += 1
            continue
        if len(modules) > 1:
            buckets["skip_multi_module"] += 1
            samples.append("  [multi] %s  paths=%s  modules=%s" %
                           (caller, "|".join(path_strs[:3]), modules))
            continue

        module = list(modules)[0]
        n_paths = len(path_strs)
        score = 4 if n_paths >= 2 else 3

        # 检查 caller skip 条件
        existing_proposed = (row.get("proposed_name") or "").strip()
        existing_score = (row.get("score") or "").strip()

        if existing_score == "5":
            buckets["skip_score5"] += 1
            continue
        # 强提案 (非 propagate 占位): 跳过
        if existing_proposed and not PROPAGATE_PROPOSED_RE.match(existing_proposed):
            # 不动 proposed_name; 但仍可加 module tag 作为补充证据
            tokens = parse_tags(row.get("tags") or "")
            if module not in tokens:
                tokens.append(module)
            # 路径锚已精确化 fs 关系, 删 via_fs
            if "via_fs" in tokens:
                tokens.remove("via_fs")
                buckets["via_fs_removed"] += 1
            row["tags"] = ";".join(tokens)
            buckets["skip_already_proposed_strong"] += 1
            continue
        # 已 Ghidra 命名: 只加 tag, 不动 proposed_name/score
        if not is_auto_name(row.get("name") or ""):
            tokens = parse_tags(row.get("tags") or "")
            if module not in tokens:
                tokens.append(module)
            if "via_fs" in tokens:
                tokens.remove("via_fs")
                buckets["via_fs_removed"] += 1
            row["tags"] = ";".join(tokens)
            buckets["tag_only_named_func"] += 1
            samples.append("  [named ] %s  %-30s  module=%s  paths=%d" %
                           (caller, row["name"], module, n_paths))
            continue

        # auto name (FUN_xxx) + 无强提案 → 写 proposed_name + score + tag
        prefix = MODULE_TO_PREFIX.get(module, module)
        addr_int = int(caller, 16)
        proposed = "%s_%08x" % (prefix, addr_int)

        tokens = parse_tags(row.get("tags") or "")
        # 删 via_fs (路径锚精确化了 fs 关系)
        if "via_fs" in tokens:
            tokens.remove("via_fs")
            buckets["via_fs_removed"] += 1
        # 删旧的 via_<module> (升级为直接 module tag)
        via_tok = "via_" + module
        if via_tok in tokens:
            tokens.remove(via_tok)
        if module not in tokens:
            tokens.append(module)
        row["tags"] = ";".join(tokens)
        row["proposed_name"] = proposed
        row["score"] = str(score)

        if score == 4:
            buckets["tag_score4"] += 1
        else:
            buckets["tag_score3"] += 1
        samples.append("  [tag   ] %s  %-30s  module=%-12s  score=%d  paths=%s" %
                       (caller, proposed, module, score, "|".join(path_strs[:2])))

    # --- wrapper tagging: 中间 wrapper 函数也属于 path 模块 ---
    wrapper_tagged = 0
    wrapper_skipped = 0
    for wrapper_addr, mods in wrapper_modules.items():
        if wrapper_addr not in rows_by_addr:
            wrapper_skipped += 1
            continue
        if len(mods) != 1:
            # wrapper 透传多个 module 的 path → 不打 tag (是真通用 wrapper, 如 fs_load 本身)
            wrapper_skipped += 1
            continue
        module = list(mods)[0]
        row = rows_by_addr[wrapper_addr]
        existing_score = (row.get("score") or "").strip()
        if existing_score == "5":
            continue
        tokens = parse_tags(row.get("tags") or "")
        if module not in tokens:
            tokens.append(module)
        if "via_fs" in tokens:
            tokens.remove("via_fs")
        row["tags"] = ";".join(tokens)
        # 仅当 auto name + 无强提案才写 proposed_name
        existing_proposed = (row.get("proposed_name") or "").strip()
        if (is_auto_name(row.get("name") or "")
                and (not existing_proposed
                     or PROPAGATE_PROPOSED_RE.match(existing_proposed))):
            prefix = MODULE_TO_PREFIX.get(module, module)
            addr_int = int(wrapper_addr, 16)
            row["proposed_name"] = "%s_%08x" % (prefix, addr_int)
            row["score"] = "3"  # wrapper 间接证据, 比 caller 直接弱一档
        wrapper_tagged += 1

    print("=" * 72)
    print("[merge fs-load-strings -> proposals]")
    print("-" * 72)
    for k in [
            "tag_score4", "tag_score3", "tag_only_named_func",
            "skip_already_proposed_strong", "skip_score5",
            "skip_multi_module", "skip_no_module", "skip_caller_not_in_csv",
            "via_fs_removed"]:
        print("  %-32s = %d" % (k, buckets[k]))
    if wrapper_modules:
        print("  wrapper_tagged                   = %d" % wrapper_tagged)
        print("  wrapper_skipped                  = %d" % wrapper_skipped)
    print("-" * 72)
    print("[samples]")
    for line in samples:
        print(line)

    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("\n[wrote] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
