#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
propagate_label_tags.py  --  方法 3 扩展: data_label tag 沿调用图向上扩散

镜像 tools/ghidra-labeling/PropagateIOTagsViaCallGraph.py 的算法,
但传播的是 method 3 的 data_label module.

输入:
    temp/ghidra-funcs-callgraph.csv      ExportFunctionCallGraph.py 的输出
    doc/dev/naming-proposals.csv         (5 列 schema, 简化 tag 格式)
输出:
    doc/dev/naming-proposals.csv         (in-place 覆写)

种子来源 (Round 0):
    1. CSV 中已有 module tag 的函数 (如 tags 含 'font_jp', 'card_stats')
       这些来自 method 3 直接命中 (merge_label_refs_to_proposals.py 写入)
    2. 已 Ghidra 命名 + 名字前缀能映射 module 的函数
       (如 fs_load → fs, pack_list_bg_setup → pack, card_info_page_init_bg0 → card_info)
       靠 label_modules.derive_module_from_func_name

算法:
    Round N+1: 对每个未 tag 函数 F:
                - 跳过条件: score=5 (FID) 或 proposed_name 已填
                - 收集所有"callee 已 tag 且 c_depth < N+1"的 module 票
                - 严格多数 (winner_count * 2 > total_votes) 才传播
                - 给 F: tag 'via_<module>' (单 token)
                - 若 F 是 auto-name (FUN_xxx):
                    proposed_name = "<prefix>_<addr8>"
                    score = 2  (弱启发, 不主动 apply)
                - 若 F 已 Ghidra 命名:
                    只追加 tag, 不动 proposed_name/score
    重复直到无新增或 MAX_DEPTH 轮.

新格式 tag:
    模块直接命中  -> 'font_jp', 'card_stats', 'game_str' (单 token)
    模块扩散      -> 'via_font_jp', 'via_game_str'
    IO family    -> 'io_bg', 'io_win'
    IO 寄存器     -> 'reg_DISPCNT', 'reg_BG0CNT'
    FID trampoline-> 'tramp_calloc'
"""

import csv
import os
import re
import sys
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    ALL_MODULES, MODULE_TO_PREFIX,
    derive_module_from_func_name, is_auto_name,
)

CALLGRAPH = os.path.join(REPO_ROOT, "temp", "ghidra-funcs-callgraph.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")

MAX_DEPTH = 10


def parse_tags(tags_str):
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(";") if t.strip()]


def find_module_tag(tokens):
    """
    在 token 列表中找模块 tag:
      返回 ('direct', module) 若有 'font_jp' 这种直接命中 token
      返回 ('via', module)    若有 'via_font_jp' 扩散 token
      返回 (None, None)       否则
    direct 优先于 via.
    """
    direct = None
    via = None
    for t in tokens:
        if t in ALL_MODULES:
            direct = t
            break
        if t.startswith("via_"):
            m = t[4:]
            if m in ALL_MODULES and via is None:
                via = m
    if direct:
        return ("direct", direct)
    if via:
        return ("via", via)
    return (None, None)


def remove_via_tags(tokens):
    """删除所有 via_* token, 保留其它. 用于扩散重写."""
    return [t for t in tokens if not t.startswith("via_")]


def main():
    if not os.path.isfile(CALLGRAPH):
        sys.stderr.write("ERROR: %s 不存在; 先跑 ExportFunctionCallGraph.py\n"
                         % CALLGRAPH)
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

    # --- 收集种子 ---
    # tags[ep] = (module_id, depth, votes_winner, votes_total, source)
    tags = {}
    n_seed_from_module_tag = 0
    n_seed_from_func_name = 0
    n_seed_overlap = 0  # 既有 module tag 又有 funcname 派生
    for ep, r in rows_by_addr.items():
        tokens = parse_tags(r.get("tags") or "")
        kind, mod = find_module_tag(tokens)
        if kind == "direct":
            tags[ep] = (mod, 0, 1, 1, "label")
            n_seed_from_module_tag += 1
            continue
        # 从函数名前缀派生 (Ghidra 已命名)
        nm_mod = derive_module_from_func_name(r.get("name") or "")
        if nm_mod:
            tags[ep] = (nm_mod, 0, 1, 1, "name")
            n_seed_from_func_name += 1
            if kind == "via":
                n_seed_overlap += 1
            continue
        # 扩散来的 (kind=='via') 不算种子重新跑一遍 (已在 rewrite_tags 重置)

    n_seeds = len(tags)
    print("[seed] total = %d  (label tag = %d, func name = %d)" %
          (n_seeds, n_seed_from_module_tag, n_seed_from_func_name))

    # --- BFS 扩散 ---
    print("[propagate]")
    for depth in range(1, MAX_DEPTH + 1):
        new_tags = {}
        for ep, r in rows_by_addr.items():
            if ep in tags:
                continue
            # 跳过条件 (注意: 已 Ghidra 命名 不再是 skip)
            if (r.get("proposed_name") or "").strip():
                continue
            if (r.get("score") or "").strip() == "5":
                continue
            cs = callees_of.get(ep)
            if not cs:
                continue
            votes = {}
            for c in cs:
                if c not in tags:
                    continue
                c_mod, c_dep, _, _, _ = tags[c]
                if c_dep >= depth:
                    continue
                votes[c_mod] = votes.get(c_mod, 0) + 1
            if not votes:
                continue
            sorted_v = sorted(votes.items(), key=lambda x: -x[1])
            winner_mod, winner_count = sorted_v[0]
            total_votes = sum(votes.values())
            if winner_count * 2 <= total_votes:
                continue  # 严格多数
            new_tags[ep] = (winner_mod, depth, winner_count, total_votes, "prop")
        tags.update(new_tags)
        print("  round %d  +%-4d  cumulative %d" % (depth, len(new_tags), len(tags)))
        if not new_tags:
            print("  收敛")
            break

    # --- 写回 CSV ---
    n_via_written_unnamed = 0
    n_via_written_named = 0
    n_funcname_seed_tagged = 0
    by_module = defaultdict(int)
    by_depth = defaultdict(int)
    for ep, (mod, dep, w, tot, src) in tags.items():
        r = rows_by_addr[ep]
        tokens = remove_via_tags(parse_tags(r.get("tags") or ""))
        if dep == 0:
            # 种子: label 来源已有 module tag (merge_label_refs 写过, 不重复);
            # funcname 来源还没有 module tag, 给它加上直接 module tag (单 token)
            if src == "name" and mod not in tokens:
                tokens.append(mod)
                r["tags"] = ";".join(tokens)
                n_funcname_seed_tagged += 1
            continue
        # dep > 0: 扩散
        via_tok = "via_" + mod
        if via_tok not in tokens:
            tokens.append(via_tok)
        r["tags"] = ";".join(tokens)
        if is_auto_name(r.get("name") or ""):
            prefix = MODULE_TO_PREFIX.get(mod, mod)
            r["proposed_name"] = "%s_%08x" % (prefix, ep)
            r["score"] = "2"
            n_via_written_unnamed += 1
        else:
            n_via_written_named += 1
        by_module[mod] += 1
        by_depth[dep] += 1

    print("\n[write] propagated tag added : %d total" %
          (n_via_written_unnamed + n_via_written_named))
    print("        new propose_name (unnamed funcs)  : %d" % n_via_written_unnamed)
    print("        tag-only (Ghidra-named funcs)     : %d" % n_via_written_named)
    print("        funcname seeds gained module tag  : %d" % n_funcname_seed_tagged)
    print("        seeds (depth=0) untouched         : %d" % n_seeds)
    print("        total tagged                      : %d" % len(tags))

    print("\n[stats] by depth:")
    for d in sorted(by_depth.keys()):
        print("  depth %d  : %4d" % (d, by_depth[d]))
    print("[stats] propagated by module:")
    for mod in sorted(by_module.keys(), key=lambda k: -by_module[k]):
        print("  %-15s : %4d" % (mod, by_module[mod]))

    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("\n[wrote] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
