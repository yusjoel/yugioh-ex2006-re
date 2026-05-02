# -*- coding: utf-8 -*-
"""
Step 1: 对 enter_deck_edit_page 的 308 函数闭包打分类标签

类别:
  A 已命名 (有语义名)              skip 递归
  B invoker thunk / runtime / libgcc skip 递归 (单独命名后视为黑盒)
  C 高 indeg utility (≥20)         单独命名, 不向下递归
  D 中 indeg shared (5-19)         命名 + 简短 plate
  E 低 indeg feature-specific (1-4) 重点分析 (深入 plate)
  F 入度 0 (page handler 入口)      重点分析 + page state idx 命名

输入:
  temp/complete_callgraph.csv
  doc/dev/naming-proposals.csv
  temp/enter_deck_edit_page_closure.txt (用其中地址)

输出:
  temp/closure_classified.csv (addr, name, class, indeg, depth, kind)
"""

import csv
import os
import re
from collections import Counter, defaultdict


CG_PATH = "temp/complete_callgraph.csv"
PROPOSALS = "doc/dev/naming-proposals.csv"
CLOSURE_TXT = "temp/enter_deck_edit_page_closure.txt"
OUT_CSV = "temp/closure_classified.csv"

ROOT = 0x08108ac0

# Runtime/libgcc 段起点 (FUN_0810e5c8 起为 invoker thunks + libgcc + libc)
RUNTIME_LO = 0x0810e5c8

# Invoker thunk 范围 (bx r0..r10, 每 4 字节)
INVOKERS = set(range(0x0810e5c8, 0x0810e5f4, 4))

# indeg 阈值
HIGH_INDEG = 20
MID_INDEG = 5


def main():
    # 加载 callgraph
    edges = []  # (caller, callee, kind)
    with open(CG_PATH) as f:
        for r in csv.DictReader(f):
            edges.append((int(r["caller_addr"], 16),
                          int(r["callee_addr"], 16),
                          r["kind"]))
    print(f"[load] {len(edges)} edges")

    # 计算全 ROM indeg (所有边, 不仅闭包)
    indeg = Counter()
    for ca, ce, _ in edges:
        indeg[ce] += 1

    # 构建 caller -> [callee] 映射
    calls = defaultdict(set)
    edge_kind = {}
    for ca, ce, k in edges:
        calls[ca].add(ce)
        # 同一对边可能有多 kind (direct + indirect), 记最强的
        cur = edge_kind.get((ca, ce), "")
        if cur != "direct":
            edge_kind[(ca, ce)] = k

    # BFS 闭包 + depth
    visited = {ROOT: 0}
    queue = [ROOT]
    while queue:
        nxt = []
        for f in queue:
            for callee in calls.get(f, []):
                if callee not in visited:
                    visited[callee] = visited[f] + 1
                    nxt.append(callee)
        queue = nxt
    print(f"[closure] {len(visited)} functions")

    # 加载已命名
    known = {}
    with open(PROPOSALS) as f:
        for r in csv.DictReader(f):
            known[int(r["address"], 16)] = r["name"]

    # 分类
    classified = []
    for addr, depth in sorted(visited.items(), key=lambda x: (x[1], x[0])):
        name = known.get(addr, "")
        is_named = name and not name.startswith("FUN_") and not name.startswith("SUB_")
        deg = indeg[addr]

        if addr in INVOKERS:
            cls = "B_invoker"
        elif addr >= RUNTIME_LO:
            cls = "B_runtime"
        elif is_named:
            cls = "A_named"
        elif deg == 0:
            cls = "F_orphan"  # 入度 0 但被间接调用 (page handler)
        elif deg >= HIGH_INDEG:
            cls = "C_util_high"
        elif deg >= MID_INDEG:
            cls = "D_shared_mid"
        else:
            cls = "E_specific_low"

        classified.append({
            "addr": addr,
            "depth": depth,
            "indeg": deg,
            "name": name or "-",
            "class": cls,
        })

    # 输出
    os.makedirs("temp", exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("addr,depth,indeg,class,name\n")
        for c in classified:
            f.write(f"0x{c['addr']:08x},{c['depth']},{c['indeg']},{c['class']},{c['name']}\n")
    print(f"[done] -> {OUT_CSV}")

    # 简报
    by_class = Counter(c["class"] for c in classified)
    print()
    print("=== 分类简报 (308 函数闭包) ===")
    for cls in sorted(by_class):
        print(f"  {cls:18s} : {by_class[cls]:3d}")
    print()
    needs_analysis = [c for c in classified if c["class"] in ("C_util_high", "D_shared_mid", "E_specific_low", "F_orphan")]
    print(f"待分析 (C/D/E/F): {len(needs_analysis)}")
    print()
    # 按 class 列前几个最高深度的
    print("=== 各类前 3 深度示例 ===")
    for cls_name in ["F_orphan", "E_specific_low", "D_shared_mid", "C_util_high"]:
        items = [c for c in classified if c["class"] == cls_name]
        items.sort(key=lambda c: -c["depth"])
        if items:
            print(f"  -- {cls_name} (n={len(items)}) --")
            for it in items[:3]:
                print(f"    L{it['depth']} 0x{it['addr']:08x}  indeg={it['indeg']:3d}  name={it['name']}")


if __name__ == "__main__":
    main()
