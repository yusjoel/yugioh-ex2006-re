#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
propagate_label_tags.py  --  module tag 沿调用图扩散 (multi-tag, 无 via_ 前缀)

设计 (v2):
  - **不区分**直接命中 vs 间接调用. 函数 F 调了 game_str 函数 -> F 也获得 'game_str' tag.
  - **multi-tag**. 一个函数同时持有 'font_jp;game_str;card_stats' 是自然事情.
  - **不参与评分**. score / proposed_name 不动. 标 tag 是无副作用操作.
  - **无阈值**. 任意 callee 携带 module tag M -> caller 继承 M.

输入:
    temp/ghidra-funcs-callgraph.csv      ExportFunctionCallGraph.py 输出
    doc/dev/naming-proposals.csv         (5 列 schema)

输出:
    doc/dev/naming-proposals.csv         (in-place 覆写, 仅改 tags 列)

迁移行为:
    - 入口扫一遍 tags, 把 'via_<X>' (单 token) 改名为 '<X>' (X 必须在 ALL_MODULES)
      去重保序. 旧扩散 tag 与现有直接 tag 合并成一个.

种子:
    1. 迁移后 CSV 中已有 module tag (∈ ALL_MODULES) 的函数
    2. funcname 前缀派生 module 的函数 (label_modules.derive_module_from_func_name)

扩散:
    Round N+1: 对每个函数 F (无 skip 条件):
                F 的 module tag 集合 ∪= 各 callee 的 module tag 集合
    重复直到无新增或 MAX_DEPTH 轮.

只传播 ALL_MODULES 中的 tag. IO family / tramp_* / 其它 tag 不参与本脚本扩散.
"""

import csv
import os
import sys
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    ALL_MODULES,
    derive_module_from_func_name,
)

CALLGRAPH = os.path.join(REPO_ROOT, "temp", "ghidra-funcs-callgraph.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")

MAX_DEPTH = 32  # 安全上限; 集合只增不减, 通常几轮就收敛


def parse_tags(tags_str):
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(";") if t.strip()]


def migrate_via_tokens(tokens):
    """把 'via_<X>' (X∈ALL_MODULES) 重写为 '<X>'. 其它 token 原样保留. 去重保序."""
    out = []
    seen = set()
    for t in tokens:
        if t.startswith("via_"):
            mod = t[4:]
            if mod in ALL_MODULES:
                t = mod
            # 否则保留原样 (未识别 via_ tag, 可能将来加新模块)
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


def main():
    if not os.path.isfile(CALLGRAPH):
        sys.stderr.write(
            "ERROR: %s 不存在; 先跑 ExportFunctionCallGraph.py\n" % CALLGRAPH
        )
        return 1
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    # --- 加载 callgraph ---
    callees_of = defaultdict(set)
    n_edges = 0
    with open(CALLGRAPH, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ca = int(r["caller_addr"], 16)
            ce = int(r["callee_addr"], 16)
            callees_of[ca].add(ce)
            n_edges += 1
    print("[load] callgraph: %d edges" % n_edges)

    # --- 加载 CSV ---
    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    rows_by_addr = {int(r["address"], 16): r for r in rows}
    print("[load] proposals: %d rows" % len(rows))

    # --- 第一步: 迁移 via_X -> X ---
    n_via_migrated = 0
    n_rows_changed_in_migration = 0
    for r in rows:
        old_tokens = parse_tags(r.get("tags") or "")
        new_tokens = migrate_via_tokens(old_tokens)
        # 计 via_ 数
        n_via = sum(1 for t in old_tokens if t.startswith("via_") and t[4:] in ALL_MODULES)
        if n_via > 0:
            n_via_migrated += n_via
        if new_tokens != old_tokens:
            r["tags"] = ";".join(new_tokens)
            n_rows_changed_in_migration += 1
    print("[migrate] %d via_<X> tokens flattened across %d rows"
          % (n_via_migrated, n_rows_changed_in_migration))

    # --- 第二步: 收集每个函数的初始 module tag 集合 ---
    # func_mods[ep] = set(module_id, ...)
    func_mods = {}
    n_seed_from_tag = 0
    n_seed_from_name = 0
    n_seed_total = 0
    for ep, r in rows_by_addr.items():
        tokens = parse_tags(r.get("tags") or "")
        mods = set(t for t in tokens if t in ALL_MODULES)
        if mods:
            n_seed_from_tag += 1
        # funcname 派生
        nm_mod = derive_module_from_func_name(r.get("name") or "")
        if nm_mod:
            mods.add(nm_mod)
            if not (set(t for t in tokens if t in ALL_MODULES)):
                # 仅 funcname 派生 (没原 tag)
                n_seed_from_name += 1
        if mods:
            n_seed_total += 1
        func_mods[ep] = mods

    print("[seed] functions with >=1 module tag: %d  (from CSV tag: %d, only-from-name: %d)"
          % (n_seed_total, n_seed_from_tag, n_seed_from_name))

    # --- 第三步: BFS 多 tag 扩散 (callee tags -> caller) ---
    print("[propagate]")
    for depth in range(1, MAX_DEPTH + 1):
        changed = 0
        new_additions = 0
        for ep, r in rows_by_addr.items():
            cs = callees_of.get(ep)
            if not cs:
                continue
            cur = func_mods[ep]
            added = set()
            for c in cs:
                cm = func_mods.get(c)
                if not cm:
                    continue
                for m in cm:
                    if m not in cur and m not in added:
                        added.add(m)
            if added:
                cur |= added
                func_mods[ep] = cur
                changed += 1
                new_additions += len(added)
        print("  round %2d  funcs_changed=%-4d  tags_added=%d" % (depth, changed, new_additions))
        if changed == 0:
            print("  收敛")
            break

    # --- 第四步: 写回 tags 列 ---
    # 保留非 module / 非 via_ 的所有 token (IO family, tramp_, 其它),
    # 用最终 func_mods[ep] 替换 module tag 部分.
    n_rows_changed = 0
    n_module_tags_added = 0
    n_module_tags_removed = 0
    for ep, r in rows_by_addr.items():
        old_tokens = parse_tags(r.get("tags") or "")
        # 拆分: kept (非 module, 非 via_) + old_mods (旧 module tag)
        kept = []
        old_mod_set = set()
        for t in old_tokens:
            if t.startswith("via_"):
                # 迁移后理论上不会再有, 但安全起见跳过
                continue
            if t in ALL_MODULES:
                old_mod_set.add(t)
                continue
            kept.append(t)
        new_mod_set = func_mods[ep]
        # 保序: kept 先, 然后按 ALL_MODULES 字典序追加
        new_tokens = list(kept)
        for m in sorted(new_mod_set):
            if m not in new_tokens:
                new_tokens.append(m)
        # 去重
        seen = set()
        deduped = []
        for t in new_tokens:
            if t in seen:
                continue
            seen.add(t)
            deduped.append(t)
        new_tags_str = ";".join(deduped)
        old_tags_str = r.get("tags") or ""
        if new_tags_str != old_tags_str:
            r["tags"] = new_tags_str
            n_rows_changed += 1
        added_here = new_mod_set - old_mod_set
        removed_here = old_mod_set - new_mod_set
        n_module_tags_added += len(added_here)
        n_module_tags_removed += len(removed_here)

    print("\n[write] tag rows changed: %d" % n_rows_changed)
    print("        module tags added (cumulative): %d" % n_module_tags_added)
    print("        module tags removed (should be 0): %d" % n_module_tags_removed)

    # --- 统计 ---
    by_module_count = defaultdict(int)
    for ep, mods in func_mods.items():
        for m in mods:
            by_module_count[m] += 1
    print("\n[stats] funcs carrying each module tag (top 25):")
    for m in sorted(by_module_count.keys(), key=lambda k: -by_module_count[k])[:25]:
        print("  %-15s : %4d" % (m, by_module_count[m]))

    # 写回
    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("\n[wrote] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
