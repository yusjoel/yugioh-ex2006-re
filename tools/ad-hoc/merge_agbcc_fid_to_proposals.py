#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_agbcc_fid_to_proposals.py  --  把 agbcc FID 匹配结果合进命名提案 CSV

输入  temp/agbcc-fid-matches.csv         build_agbcc_fid.py 的输出
       doc/dev/naming-proposals.csv      现有提案
输出  doc/dev/naming-proposals.csv (覆写, in-place)

策略:
  1) 过滤 n_matches == 1 的 FID 匹配 (符号→ROM 唯一)
  2) 干净 (address, sym_name) 对 → proposed_name + score=5
  3) "同地址多名" trampoline 组 → tags 列写
       fid_trampoline:name1|name2|...   (proposed_name 不填, score 不填)
     (这些是 newlib 风格 wrapper f() -> _f_r(_REENT,...), 字节模式相同,
      区分需读 ROM 中实际 bl target 反查 _xxx_r 已知归属)
  4) 已经有非空 proposed_name 的行 → 不动 (尊重既有人工提案)
  5) tags 列若不存在则新增; 重跑时 fid_trampoline:* 会被覆写, 其它 tag 保留

tags 格式:  ;-分隔多个 tag, 每个 tag 形如 "<key>:<value>",
            value 内部允许 |  (例如 fid_trampoline:calloc|fopen|...)
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
    trampoline_candidates = {}  # addr -> sorted list of sym_names
    for r in fid_unique:
        if r["address"] in trampoline_addrs:
            trampoline_candidates.setdefault(r["address"], []).append(r["sym_name"])
            continue
        clean_map[r["address"]] = (r["sym_name"], r["archive"], r["object"])
    for addr in trampoline_candidates:
        trampoline_candidates[addr] = sorted(trampoline_candidates[addr])
    # 旧格式 fid_trampoline:foo|bar 已废弃, 改写多 token "tramp_<name>"
    trampoline_tokens = {
        addr: ["tramp_" + n for n in names]
        for addr, names in trampoline_candidates.items()
    }

    print("[fid    ] %d unique-pattern matches" % len(fid_unique))
    print("[trampoline] %d 地址  %d 行候选" % (
        len(trampoline_addrs),
        sum(len(v) for v in trampoline_candidates.values())))
    print("[clean  ] %d 干净 (address, sym_name) 对" % len(clean_map))

    # 读 proposals CSV
    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # 确保 tags 列存在
    if "tags" not in fieldnames:
        fieldnames.append("tags")
        for r in rows:
            r["tags"] = ""

    # 合并
    n_added = 0
    n_already_proposed = 0
    n_tagged_trampoline = 0
    for row in rows:
        addr = row["address"]
        # (a) 干净 FID 命中 -> proposed_name + score=5
        if addr in clean_map:
            sym_name, archive, obj = clean_map[addr]
            if row["proposed_name"]:
                n_already_proposed += 1
            else:
                row["proposed_name"] = sym_name
                row["score"] = "5"
                n_added += 1
        # (b) trampoline -> 写 tags (覆写旧 tramp_*/fid_trampoline:*, 保留其它)
        if addr in trampoline_tokens:
            old_tags = (row.get("tags") or "").split(";")
            kept = [t.strip() for t in old_tags
                    if t.strip()
                    and not t.strip().startswith("tramp_")
                    and not t.strip().startswith("fid_trampoline:")]
            kept.extend(trampoline_tokens[addr])
            row["tags"] = ";".join(kept)
            n_tagged_trampoline += 1

    # 检查 FID 命中但不在 proposals (Ghidra 没把它当成函数)
    proposals_addrs = set([r["address"] for r in rows])
    fid_only = [a for a in clean_map if a not in proposals_addrs]
    if fid_only:
        print("[warn   ] %d 个 FID 命中地址不在 naming-proposals.csv 里 (Ghidra 没识别成函数):" % len(fid_only))
        for a in fid_only[:10]:
            print("           %s -> %s" % (a, clean_map[a][0]))

    print("\n[merge  ] 新增 proposed_name (score=5): %d" % n_added)
    print("           已有 proposal 不动: %d" % n_already_proposed)
    print("           trampoline tag 写入: %d 行" % n_tagged_trampoline)

    # 写回
    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("\n[wrote  ] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
