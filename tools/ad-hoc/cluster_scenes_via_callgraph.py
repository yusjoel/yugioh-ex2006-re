#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cluster_scenes_via_callgraph.py  --  阶段 1: 场景大类聚类 (multi-source Voronoi BFS)

V1 (utility-only 阻断双向 BFS) 失败: 9 个 scene 几乎全图覆盖 (overlap=9 占
2794 个函数), 因为静态 utility (492) 不足以阻断, 大量未 tag 中间层联通了所有 scene.

V2 改进:
  1. 静态 utility (label_modules.UTILITY_MODULES tag 的) +
     动态 utility (in-degree 或 out-degree >= DEGREE_THRESHOLD 的) 都作边界.
  2. Multi-source BFS: 所有 scene 种子同时入队, 维护 (distance, owner)
     按 Voronoi 划分领地. 每个节点归属"最近种子"对应的 scene.
  3. 距离上限 K=3, 防止远程污染.
  4. 同距离多 scene 触达 → 重叠 (允许多 tag).

输入:
    temp/ghidra-funcs-callgraph.csv      ExportFunctionCallGraph.py 输出
    doc/dev/naming-proposals.csv         现有 tag (找种子)
输出:
    doc/dev/naming-proposals.csv (in-place, 加 scene_<name> tag)

输出 tag 格式: scene_<name> 单 token (e.g. scene_demo, scene_pack)
"""

import csv
import os
import sys
from collections import defaultdict, deque

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    SCENE_MODULES, UTILITY_MODULES, ALL_MODULES, IO_FAMILY_TAGS,
    is_helper_name,
)

CALLGRAPH = os.path.join(REPO_ROOT, "temp", "ghidra-funcs-callgraph.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")

# 动态 utility: in-degree 或 out-degree >= 此阈值的节点视为 utility 边界.
# fanout 分布 (10136 边): p90=8, p95=14, p99=48.
# 取 10 作阈值 ≈ 排除 ~10% 高调用度节点 (高调用度 ≈ 通用工具).
DEGREE_THRESHOLD = 10

# BFS 距离上限 (跳数)
MAX_DEPTH = 3


def parse_tags(s):
    if not s:
        return []
    return [t.strip() for t in s.split(";") if t.strip()]


def has_any_utility_tag(tokens):
    """tokens 中是否有 utility module tag (multi-tag 体系下不再区分直接/扩散)."""
    for t in tokens:
        if t in UTILITY_MODULES:
            return True
    return False


def find_direct_scene_module(tokens):
    """tokens 中是否有 scene module tag."""
    for t in tokens:
        if t in SCENE_MODULES:
            return t
    return None


def main():
    if not os.path.isfile(CALLGRAPH):
        sys.stderr.write("ERROR: %s 不存在\n" % CALLGRAPH)
        return 1
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    # --- callgraph: 双向邻接 ---
    callees_of = defaultdict(set)
    callers_of = defaultdict(set)
    with open(CALLGRAPH, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ca = int(r["caller_addr"], 16)
            ce = int(r["callee_addr"], 16)
            callees_of[ca].add(ce)
            callers_of[ce].add(ca)
    n_edges = sum(len(v) for v in callees_of.values())
    print("[load] callgraph: %d edges" % n_edges)

    # --- proposals ---
    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    rows_by_addr = {int(r["address"], 16): r for r in rows}
    print("[load] proposals: %d rows" % len(rows))

    # --- 分类节点 ---
    is_static_utility = {}         # ep -> bool (来自 tag)
    is_helper_utility = {}         # ep -> bool (Ghidra 已命名为 gl_*/cpu_/bios_/bg*_/default)
    direct_scene = {}              # ep -> scene_name (or None)
    scene_seeds = defaultdict(set)  # scene -> set of ep

    for ep, r in rows_by_addr.items():
        tokens = parse_tags(r.get("tags") or "")
        is_static_utility[ep] = has_any_utility_tag(tokens)
        # 检查 name 和 proposed_name 双列, 因为 score<5 提案没 apply 到 Ghidra,
        # 真名 (如 bg0_cnt_extract_char_base) 在 proposed_name 列
        nm = r.get("name") or ""
        pn = r.get("proposed_name") or ""
        is_helper_utility[ep] = is_helper_name(nm) or is_helper_name(pn)
        s = find_direct_scene_module(tokens)
        if s:
            direct_scene[ep] = s
            scene_seeds[s].add(ep)

    # 动态 utility: 高 fanout 节点 (无论有没有 tag)
    is_dynamic_utility = {}
    for ep in rows_by_addr:
        in_deg = len(callers_of.get(ep, ()))
        out_deg = len(callees_of.get(ep, ()))
        is_dynamic_utility[ep] = (in_deg >= DEGREE_THRESHOLD or
                                   out_deg >= DEGREE_THRESHOLD)

    is_utility = {ep: (is_static_utility.get(ep, False) or
                        is_dynamic_utility.get(ep, False) or
                        is_helper_utility.get(ep, False))
                   for ep in rows_by_addr}

    n_static_util = sum(1 for v in is_static_utility.values() if v)
    n_dynamic_util = sum(1 for v in is_dynamic_utility.values() if v)
    n_helper_util = sum(1 for v in is_helper_utility.values() if v)
    n_combined_util = sum(1 for v in is_utility.values() if v)
    print("[utility] static (tag-based)        : %d" % n_static_util)
    print("          dynamic (deg >= %d)        : %d" % (DEGREE_THRESHOLD, n_dynamic_util))
    print("          helper (gl_/bg*_/cpu_/...) : %d" % n_helper_util)
    print("          combined                  : %d" % n_combined_util)
    print("[seed] scene seeds:")
    total_seeds = 0
    for s in sorted(scene_seeds.keys()):
        print("  %-15s : %d" % (s, len(scene_seeds[s])))
        total_seeds += len(scene_seeds[s])
    print("  total           : %d" % total_seeds)

    # --- Multi-source Voronoi BFS, 距离上限 MAX_DEPTH ---
    # distance[ep] = 最短距离到任意种子 (BFS 跳数)
    # owners[ep]   = 与最短距离对应的 scene 集 (同距离多种子 → 多 owner)
    distance = {}
    owners = defaultdict(set)
    queue = deque()
    for s, seeds in scene_seeds.items():
        for ep in seeds:
            distance[ep] = 0
            owners[ep] = {s}
            queue.append(ep)

    while queue:
        f = queue.popleft()
        d = distance[f]
        if d >= MAX_DEPTH:
            continue
        f_owners = owners[f]
        neighbors = callees_of.get(f, set()) | callers_of.get(f, set())
        for n in neighbors:
            # 阻断: utility 节点不进入
            if is_utility.get(n, False):
                continue
            # 阻断: 其它 scene 直接种子 (是别人的领地, 不传播)
            other_s = direct_scene.get(n)
            if other_s and other_s not in f_owners:
                # 别的 scene seed, 不入队 (避免互相覆盖种子)
                continue
            new_d = d + 1
            if n not in distance:
                distance[n] = new_d
                owners[n] = set(f_owners)
                queue.append(n)
            elif new_d == distance[n]:
                # 同距离: owner 合并 (重叠)
                before = len(owners[n])
                owners[n] |= f_owners
                if len(owners[n]) > before:
                    # 重叠新增, 不重新入队 (距离没变)
                    pass
            # new_d > distance[n] 时忽略 (已有更短路径)

    # --- 统计与写回 ---
    # 关键规则: 仅 overlap=1 (单 scene 触达) 的函数才打 scene tag.
    # overlap >= 2 被推断为"横切 utility" (gl_fade_out 等漏掉静态/动态阈值的 utility),
    # 不打 tag, 避免污染.
    n_tagged = 0
    n_inferred_utility = 0  # overlap >= 2, 推断为 utility, 不打 tag
    by_scene_count = defaultdict(int)
    by_overlap_size = defaultdict(int)
    by_distance = defaultdict(int)

    seeds_combined = scene_seeds_combined(scene_seeds)
    for ep, owner_scenes in owners.items():
        if ep in seeds_combined:
            continue
        n_owners = len(owner_scenes)
        by_overlap_size[n_owners] += 1
        if n_owners >= 2:
            n_inferred_utility += 1
            continue
        r = rows_by_addr.get(ep)
        if r is None:
            continue
        s = next(iter(owner_scenes))
        tag = "scene_" + s
        tokens = parse_tags(r.get("tags") or "")
        if tag not in tokens:
            tokens.append(tag)
            r["tags"] = ";".join(tokens)
            n_tagged += 1
            by_scene_count[s] += 1
            by_distance[distance[ep]] += 1

    print("\n[BFS] overlap distribution (含被推断为 utility 而丢弃的):")
    for k in sorted(by_overlap_size.keys()):
        print("       overlap=%d : %d 函数" % (k, by_overlap_size[k]))
    print("       (overlap>=2 被丢弃, 推断为横切 utility: %d)" % n_inferred_utility)
    print("[BFS] tagged distance distribution:")
    for d in sorted(by_distance.keys()):
        print("       depth %d : %d" % (d, by_distance[d]))
    print("[BFS] tagged by scene:")
    for s in sorted(by_scene_count.keys()):
        print("       %-15s : %4d" % (s, by_scene_count[s]))
    print("\n[write] scene_<s> tag 新加 (overlap=1): %d 个函数" % n_tagged)

    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("\n[wrote] %s" % PROPOSALS)
    return 0


def scene_seeds_combined(scene_seeds):
    out = set()
    for s, fs in scene_seeds.items():
        out |= fs
    return out


if __name__ == "__main__":
    sys.exit(main())
