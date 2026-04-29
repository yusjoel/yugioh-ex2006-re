#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_agbcc_fid_to_proposals.py  --  把 agbcc FID 匹配结果合进命名提案 CSV

输入  temp/agbcc-fid-matches.csv         build_agbcc_fid.py 的输出
       doc/dev/naming-proposals.csv      现有提案
输出  doc/dev/naming-proposals.csv (覆写, in-place)

策略:
  1) 过滤 n_matches == 1 的 FID 匹配 (符号→ROM 唯一)
  2) 排除 "同地址多名" 的 trampoline 组 (一个地址被 >= 2 个 sym_name 命中,
     纯 byte 区分不出, 跳过)
  3) 对每个干净的 (address, sym_name): 在 proposals CSV 里写 proposed_name,
     score=5
  4) 已经在 proposals 里有非空 proposed_name 的行 → 不动 (尊重既有提案)
"""

import csv
import os
import sys
from collections import Counter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FID_CSV = os.path.join(REPO_ROOT, "temp", "agbcc-fid-matches.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")


def main():
    if not os.path.isfile(FID_CSV):
        sys.stderr.write("ERROR: %s 不存在; 先跑 build_agbcc_fid.py\n" % FID_CSV)
        return 1
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    # 收集 FID 唯一匹配 (n_matches == 1)
    fid_unique = []
    with open(FID_CSV, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["n_matches"] == "1":
                fid_unique.append(r)

    # 检测 trampoline (同地址多名)
    addr_count = Counter([r["address"] for r in fid_unique])
    trampoline_addrs = set([a for a, c in addr_count.items() if c > 1])

    clean_map = {}  # addr -> (sym_name, archive, obj)
    for r in fid_unique:
        if r["address"] in trampoline_addrs:
            continue
        clean_map[r["address"]] = (r["sym_name"], r["archive"], r["object"])

    print("[fid    ] %d unique-pattern matches" % len(fid_unique))
    print("[skip   ] %d trampoline 地址 (%d 行不可区分)" % (
        len(trampoline_addrs),
        sum(c for a, c in addr_count.items() if c > 1)))
    print("[clean  ] %d 干净 (address, sym_name) 对" % len(clean_map))

    # 读 proposals CSV
    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # 合并
    n_added = 0
    n_already_proposed = 0
    n_not_in_proposals = 0
    for row in rows:
        addr = row["address"]
        if addr not in clean_map:
            continue
        sym_name, archive, obj = clean_map[addr]
        if row["proposed_name"]:
            n_already_proposed += 1
            continue
        row["proposed_name"] = sym_name
        row["score"] = "5"
        n_added += 1

    # 检查 FID 命中但不在 proposals (Ghidra 没把它当成函数)
    proposals_addrs = set([r["address"] for r in rows])
    fid_only = [a for a in clean_map if a not in proposals_addrs]
    if fid_only:
        print("[warn   ] %d 个 FID 命中地址不在 naming-proposals.csv 里 (Ghidra 没识别成函数):" % len(fid_only))
        for a in fid_only[:10]:
            print("           %s -> %s" % (a, clean_map[a][0]))

    print("\n[merge  ] 新增 proposal: %d" % n_added)
    print("           已有 proposal 不动: %d" % n_already_proposed)

    # 写回
    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("\n[wrote  ] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
