# -*- coding: utf-8 -*-
"""
merge_manual_edges.py — 把 tools/ad-hoc/manual_dispatch_edges.csv 中的边合并进
temp/complete_callgraph.csv (kind=indirect_manual).

用途: resolve_fnptr_tables.py 只识别 invoker-thunk 模式 (`bl FUN_0810e5cX`); 对
mov pc,rN / 写函数指针到全局后从全局调 / 局部跳表等模式无能为力. 把这些边手工
标注后由本脚本注入到 callgraph, 让 BFS 闭包包含它们.

输入:
  temp/complete_callgraph.csv          (resolve_fnptr_tables.py 的产出)
  tools/ad-hoc/manual_dispatch_edges.csv (手工标注 + 注释)

输出:
  temp/complete_callgraph.csv (in-place 追加, 已存在的 (caller, callee) 组合不重复)
"""

import csv
import os
import sys

CG_PATH = "temp/complete_callgraph.csv"
MANUAL_PATH = "tools/ad-hoc/manual_dispatch_edges.csv"


def main():
    if not os.path.exists(CG_PATH):
        sys.exit(f"missing {CG_PATH} -- run resolve_fnptr_tables.py first")
    if not os.path.exists(MANUAL_PATH):
        sys.exit(f"missing {MANUAL_PATH}")

    existing = set()
    rows = []
    with open(CG_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ca = int(r["caller_addr"], 16)
            ce = int(r["callee_addr"], 16)
            kind = r["kind"]
            existing.add((ca, ce))
            rows.append((ca, ce, kind))

    added = 0
    skipped = 0
    with open(MANUAL_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("caller_addr"):
                continue
            parts = line.split(",", 3)
            if len(parts) < 3:
                continue
            ca = int(parts[0], 16)
            ce = int(parts[2], 16)
            if (ca, ce) in existing:
                skipped += 1
                continue
            rows.append((ca, ce, "indirect_manual"))
            existing.add((ca, ce))
            added += 1

    rows.sort()
    with open(CG_PATH, "w", encoding="utf-8") as f:
        f.write("caller_addr,callee_addr,kind\n")
        for ca, ce, k in rows:
            f.write(f"0x{ca:08x},0x{ce:08x},{k}\n")

    print(f"[merge_manual_edges] added={added} skipped(dup)={skipped} total={len(rows)}")
    print(f"[merge_manual_edges] -> {CG_PATH}")


if __name__ == "__main__":
    main()
