# -*- coding: utf-8 -*-
"""
Step 2: 闭包子图 Tarjan SCC + 反向拓扑排序

输出每个待分析函数的"分析序号":
  序号低 → callee 全是 leaf/已命名/runtime, 可立即分析
  序号高 → 依赖较多未命名 callee, 应等其 callee 命名后再做

环 (mutual recursion / dispatcher 反查) 缩成 SCC, 标记为"批量同时分析"

输入:
  temp/complete_callgraph.csv
  temp/closure_classified.csv

输出:
  temp/closure_topo_order.txt   (按分析序号排, 含 SCC 标记)
  temp/closure_topo_order.csv   (addr, topo_idx, scc_id, scc_size, depth, indeg, class, name)
"""

import csv
import os
import sys
from collections import defaultdict

sys.setrecursionlimit(10000)


CG_PATH = "temp/complete_callgraph.csv"
CLASSIFIED = "temp/closure_classified.csv"
OUT_TXT = "temp/closure_topo_order.txt"
OUT_CSV = "temp/closure_topo_order.csv"


def tarjan_scc(nodes, edges_out):
    """
    Tarjan SCC.
    nodes: list of node ids
    edges_out: dict {node: set(neighbors)}
    返回: list of SCCs (each = list of nodes), 已按反向拓扑序排 (后端 SCC 在前)
    """
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    on_stack = {}
    sccs = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlinks[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in edges_out.get(v, []):
            if w not in nodes_set:
                continue
            if w not in index:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif on_stack.get(w):
                lowlinks[v] = min(lowlinks[v], index[w])

        if lowlinks[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    nodes_set = set(nodes)
    for v in nodes:
        if v not in index:
            strongconnect(v)
    # Tarjan 自然产出反向拓扑序 (sink SCC 先出现) — 这正好是我们要的"叶子优先"
    return sccs


def main():
    # 加载分类
    classified = {}
    with open(CLASSIFIED) as f:
        for r in csv.DictReader(f):
            classified[int(r["addr"], 16)] = r
    print(f"[load] {len(classified)} classified functions in closure")

    # 加载 callgraph, 只保留闭包内边
    closure = set(classified.keys())
    edges_out = defaultdict(set)
    with open(CG_PATH) as f:
        for r in csv.DictReader(f):
            ca = int(r["caller_addr"], 16)
            ce = int(r["callee_addr"], 16)
            if ca in closure and ce in closure:
                edges_out[ca].add(ce)
    print(f"[graph] subgraph has {sum(len(v) for v in edges_out.values())} edges")

    # 跑 Tarjan
    sccs = tarjan_scc(sorted(closure), edges_out)
    print(f"[scc] {len(sccs)} SCCs")
    big_sccs = [s for s in sccs if len(s) > 1]
    print(f"[scc] non-trivial (>1 node): {len(big_sccs)}")
    for s in big_sccs:
        print(f"  size {len(s)}: " + " ".join(f"0x{a:08x}" for a in s[:5])
              + ("..." if len(s) > 5 else ""))

    # 给每个函数分配 (scc_id, topo_idx)
    # Tarjan 输出已是反向拓扑序: sccs[0] 是"最深 sink"
    scc_id_of = {}
    scc_size_of = {}
    topo_idx_of = {}  # 全局序号: 0 = 最深叶, 越大越靠近 root
    for i, comp in enumerate(sccs):
        for n in comp:
            scc_id_of[n] = i
            scc_size_of[n] = len(comp)
            topo_idx_of[n] = i

    # 输出 CSV
    os.makedirs("temp", exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("topo_idx,scc_id,scc_size,addr,depth,indeg,class,name\n")
        # 按 topo_idx 升序 (叶子在前)
        items = list(classified.values())
        items.sort(key=lambda c: (topo_idx_of[int(c["addr"], 16)], int(c["addr"], 16)))
        for c in items:
            a = int(c["addr"], 16)
            f.write(f"{topo_idx_of[a]},{scc_id_of[a]},{scc_size_of[a]},"
                    f"0x{a:08x},{c['depth']},{c['indeg']},{c['class']},{c['name']}\n")
    print(f"[done] -> {OUT_CSV}")

    # 输出 TXT (人类友好)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(f"# campaign_scene_handler (FUN_08025c94) 闭包反向拓扑序\n")
        f.write(f"# 总 {len(classified)} 函数, {len(sccs)} SCC ({len(big_sccs)} non-trivial)\n")
        f.write(f"# topo_idx 升序: 0 = 最深 sink (callee 全是 leaf/已命名/runtime), 越大越靠近 root\n")
        f.write(f"# 推荐流程: 跳过 A/B 类, 按 topo_idx 升序选 C/D/E/F 类做 analyze-function\n")
        f.write(f"# class 含义: A 已命名, B invoker/runtime (skip), C 高 indeg utility, D 中 indeg shared, E 低 indeg specific, F orphan/page handler\n\n")

        items.sort(key=lambda c: (topo_idx_of[int(c["addr"], 16)], int(c["addr"], 16)))
        cur_scc = None
        for c in items:
            a = int(c["addr"], 16)
            if scc_id_of[a] != cur_scc:
                cur_scc = scc_id_of[a]
                if scc_size_of[a] > 1:
                    f.write(f"\n## SCC #{cur_scc} (size {scc_size_of[a]}) — 批量同时分析:\n")
            tag = "[skip]" if c["class"].startswith(("A_", "B_")) else "[分析]"
            sscc = f" SCC#{scc_id_of[a]}" if scc_size_of[a] > 1 else ""
            f.write(f"  topo={topo_idx_of[a]:4d}{sscc}  L{int(c['depth'])}  0x{a:08x}  "
                    f"indeg={int(c['indeg']):3d}  {c['class']:18s}  {c['name']:42s}  {tag}\n")
    print(f"[done] -> {OUT_TXT}")

    # 简报: 前 N 个待分析
    print()
    print("=== 前 10 个待分析叶子 (topo_idx 升序, 跳过 A/B) ===")
    items.sort(key=lambda c: (topo_idx_of[int(c["addr"], 16)], int(c["addr"], 16)))
    n = 0
    for c in items:
        if c["class"].startswith(("A_", "B_")):
            continue
        a = int(c["addr"], 16)
        print(f"  topo={topo_idx_of[a]:4d}  L{int(c['depth'])}  0x{a:08x}  "
              f"indeg={int(c['indeg']):3d}  {c['class']}  {c['name']}")
        n += 1
        if n >= 10:
            break


if __name__ == "__main__":
    main()
