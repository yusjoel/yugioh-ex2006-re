#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find_io_clusters.py  --  从 IO tag CSV 挖"地址连号 + 同 family"簇

输入: temp/ghidra-funcs-io-tags.csv (TagFunctionsByIORegs.py 产出)
输出: temp/ghidra-funcs-io-clusters.txt  人类阅读格式

簇定义:
  - 函数按地址升序排
  - 相邻函数之间地址 gap <= MAX_GAP 视为连号
  - 簇内全部同一 primary_family
  - 簇内函数数 >= MIN_CLUSTER

含义: 这种簇大概率是同一类 micro-helper 的连号变体 (典型: BG0/1/2/3 setter,
SOUND1/2/3/4 init, DMA0/1/2/3 setup). 一次起一组名最便宜.
"""

import csv
import os
import sys
from collections import Counter


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT  = os.path.join(REPO_ROOT, "temp", "ghidra-funcs-io-tags.csv")
OUTPUT = os.path.join(REPO_ROOT, "temp", "ghidra-funcs-io-clusters.txt")

MAX_GAP = 0x80           # 相邻函数地址差上限 (bytes)
MIN_CLUSTER = 3          # 最小簇长度
MAX_CLUSTER = 32         # 防止退化为整页扫描


def parse_top_regs(s):
    """'BG0CNT(1)|BG1CNT(2)' -> [('BG0CNT', 1), ('BG1CNT', 2)]."""
    out = []
    if not s:
        return out
    for tok in s.split("|"):
        tok = tok.strip()
        if not tok:
            continue
        if "(" in tok and tok.endswith(")"):
            name, cnt = tok.rsplit("(", 1)
            try:
                out.append((name, int(cnt[:-1])))
            except ValueError:
                out.append((tok, 0))
        else:
            out.append((tok, 0))
    return out


def load_csv():
    rows = []
    with open(INPUT, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r["primary_family"]:
                continue
            rows.append({
                "addr": int(r["address"], 16),
                "name": r["name"],
                "family": r["primary_family"],
                "all_families": r["all_families"],
                "total_refs": int(r["total_refs"]) if r["total_refs"] else 0,
                "unique_regs": int(r["unique_regs"]) if r["unique_regs"] else 0,
                "top_regs": parse_top_regs(r["top_regs"]),
            })
    rows.sort(key=lambda x: x["addr"])
    return rows


def find_clusters(rows):
    """Greedy: 同 family + 相邻 gap <= MAX_GAP 的最长连续段."""
    clusters = []
    i = 0
    n = len(rows)
    while i < n:
        j = i + 1
        while j < n and rows[j]["family"] == rows[i]["family"] \
              and rows[j]["addr"] - rows[j - 1]["addr"] <= MAX_GAP:
            j += 1
            if j - i >= MAX_CLUSTER:
                break
        size = j - i
        if size >= MIN_CLUSTER:
            clusters.append(rows[i:j])
        i = j
    return clusters


def cluster_summary(cluster):
    """生成一段人类阅读的簇报告."""
    fam = cluster[0]["family"]
    n = len(cluster)
    addr_lo = cluster[0]["addr"]
    addr_hi = cluster[-1]["addr"]
    span = addr_hi - addr_lo

    # 内部 gap 分析
    gaps = [cluster[k + 1]["addr"] - cluster[k]["addr"] for k in range(n - 1)]
    gap_counter = Counter(gaps)
    most_common_gap, mc_count = gap_counter.most_common(1)[0]
    uniform = mc_count == n - 1  # 所有 gap 相同 = 严格等距

    # 内部寄存器全集 (top_regs 合并)
    reg_hits = Counter()
    for f in cluster:
        for name, c in f["top_regs"]:
            reg_hits[name] += c
    top_regs_summary = " | ".join(["%s(%d)" % (k, v) for k, v in reg_hits.most_common(8)])

    # 检测 BGxCNT / SOUNDx / DMAx / TMx 这种 N 路扫
    distinct_regs_per_func = []
    for f in cluster:
        names = set([k for k, _ in f["top_regs"]])
        distinct_regs_per_func.append(names)

    # 4 BG-style: 每个函数恰好一个 reg, 4 个函数对应 BG0/1/2/3
    pattern_hint = ""
    each_func_main_reg = []
    for f in cluster:
        if f["top_regs"]:
            each_func_main_reg.append(f["top_regs"][0][0])
        else:
            each_func_main_reg.append("?")
    each_func_main_reg_set = set(each_func_main_reg)

    # 看主 reg 是不是按 0/1/2/3 之类编号的家族
    if n == 4 and len(each_func_main_reg_set) == 4:
        regs_sorted = sorted(each_func_main_reg)
        if all(s.endswith(("0", "1", "2", "3")) for s in regs_sorted) \
           or all(s.endswith(("0CNT", "1CNT", "2CNT", "3CNT")) for s in regs_sorted) \
           or all(s.endswith(("0CNT_L", "1CNT_L", "2CNT_L", "3CNT_L")) for s in regs_sorted):
            pattern_hint = "★ N 路编号家族 (强候选: <reg>_set_xxx)"
    elif len(each_func_main_reg_set) == 1:
        pattern_hint = "▲ 全簇主 reg 同一个 (变体 helper)"

    return {
        "family": fam, "n": n,
        "addr_lo": addr_lo, "addr_hi": addr_hi, "span": span,
        "uniform_gap": (most_common_gap if uniform else None),
        "gap_summary": " ".join(["0x%X" % g for g in gaps]),
        "top_regs": top_regs_summary,
        "each_main_reg": each_func_main_reg,
        "pattern_hint": pattern_hint,
    }


def main():
    if not os.path.isfile(INPUT):
        sys.stderr.write("ERROR: %s 不存在, 先跑 TagFunctionsByIORegs.py\n" % INPUT)
        return 1

    rows = load_csv()
    print("[loaded] %d tagged funcs" % len(rows))

    clusters = find_clusters(rows)
    print("[found ] %d clusters (size>=%d, gap<=0x%X)" % (
        len(clusters), MIN_CLUSTER, MAX_GAP))

    by_family = Counter([c[0]["family"] for c in clusters])
    print("[by family]")
    for fam, count in by_family.most_common():
        print("  %-10s = %d" % (fam, count))

    with open(OUTPUT, "w", encoding="utf-8") as out:
        out.write("# IO tag clusters (size>=%d, gap<=0x%X)\n" % (MIN_CLUSTER, MAX_GAP))
        out.write("# 总簇数: %d\n\n" % len(clusters))

        # 按 family 分组排序
        by_fam = {}
        for c in clusters:
            by_fam.setdefault(c[0]["family"], []).append(c)

        for fam in sorted(by_fam.keys()):
            fam_clusters = by_fam[fam]
            out.write("=" * 72 + "\n")
            out.write("FAMILY: %s   (%d 簇)\n" % (fam, len(fam_clusters)))
            out.write("=" * 72 + "\n\n")

            # 同 family 内, 长簇优先
            fam_clusters.sort(key=lambda c: -len(c))
            for cluster in fam_clusters:
                s = cluster_summary(cluster)
                out.write("[%d 个 @ 0x%08x..0x%08x  span=0x%X" % (
                    s["n"], s["addr_lo"], s["addr_hi"], s["span"]))
                if s["uniform_gap"]:
                    out.write("  gap=0x%X 均匀]" % s["uniform_gap"])
                else:
                    out.write("  gaps=%s]" % s["gap_summary"])
                out.write("\n")
                if s["pattern_hint"]:
                    out.write("  %s\n" % s["pattern_hint"])
                out.write("  top regs (合并): %s\n" % s["top_regs"])
                for k, f in enumerate(cluster):
                    main_reg = f["top_regs"][0][0] if f["top_regs"] else "-"
                    name_disp = f["name"] if not f["name"].startswith("FUN_") else "FUN_*"
                    out.write("    [%d] 0x%08x  refs=%-3d  uniq=%-2d  main=%-12s  %s\n" % (
                        k, f["addr"], f["total_refs"], f["unique_regs"],
                        main_reg, name_disp))
                out.write("\n")

    print("[wrote ] %s" % OUTPUT)


if __name__ == "__main__":
    sys.exit(main() or 0)
