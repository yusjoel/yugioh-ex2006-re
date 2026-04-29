#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_label_refs_to_proposals.py  --  方法 3: 数据 label 反向查询 → 命名提案

输入  temp/ghidra-funcs-label-refs.csv      ExportFunctionLabelRefs.py 的输出
       doc/dev/naming-proposals.csv          现有提案
输出  doc/dev/naming-proposals.csv (in-place 覆写)

派生策略:
  1) 每个 label → (module, prefix)  via label_modules.derive_module_from_label
  2) 函数命中的 module 集合, 严格主导:
       - 1 模块, unique label = 1 → score=3 (单锚)
       - 1 模块, unique label >= 2 → score=4 (多锚)
       - >=4 模块 → skip (dispatcher)
       - 2-3 模块, 主导模块 hits >= 第二高 1.5x → 取主导
       - 否则 skip (no dominant)
  3) proposed_name = "<prefix>_<addr8>" (家族级占位)
  4) tags 追加 "<module>"  单 token 简化格式 (与 propagate / rewrite_tags 一致)
  5) 跳过条件:
       - proposed_name 已非空 (尊重既有提案)
       - score >= 5 (FID 强证据)
       - name 列已非 auto (Ghidra 已手工命名, 不用占位名覆盖)

CSV tags 列约定: ;-分隔多 token, 单 token 形式, 无 key:value 无括号.
"""

import csv
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    derive_module_from_label, ALL_MODULES, is_auto_name,
)

LABEL_REFS = os.path.join(REPO_ROOT, "temp", "ghidra-funcs-label-refs.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")

MULTI_MODULE_THRESHOLD = 4
DOMINANCE_RATIO = 1.5


def parse_top_labels(top_str):
    """'a(3)|b(1)|c(1)' → [('a',3),('b',1),('c',1)]"""
    if not top_str:
        return []
    out = []
    for tok in top_str.split("|"):
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r"^(.+?)\((\d+)\)$", tok)
        if not m:
            continue
        out.append((m.group(1), int(m.group(2))))
    return out


def aggregate_to_modules(top_labels):
    """[(label, hits), ...]
       → modules: {module_id: {"prefix": str, "labels": {label: hits}, "total": int}}"""
    modules = {}
    for lbl, hits in top_labels:
        mod, prefix = derive_module_from_label(lbl)
        if mod is None:
            continue
        if mod not in modules:
            modules[mod] = {"prefix": prefix, "labels": {}, "total": 0}
        modules[mod]["labels"][lbl] = modules[mod]["labels"].get(lbl, 0) + hits
        modules[mod]["total"] += hits
    return modules


def decide(top_str):
    """
    返回 (decision, module, prefix, score, used_labels, debug)
       decision ∈ {'tag', 'skip_dispatcher', 'skip_no_module',
                   'skip_assert_only', 'skip_no_dominant'}
    """
    top_labels = parse_top_labels(top_str)
    if not top_labels:
        return ("skip_no_module", None, None, None, [], "no top labels")

    modules = aggregate_to_modules(top_labels)
    if not modules:
        return ("skip_assert_only", None, None, None,
                [l for l, _ in top_labels], "all assert-like or unmatched")

    n_modules = len(modules)
    if n_modules >= MULTI_MODULE_THRESHOLD:
        return ("skip_dispatcher", None, None, None, [],
                "%d modules" % n_modules)

    sorted_mods = sorted(modules.items(),
                         key=lambda kv: (-kv[1]["total"], kv[0]))
    top_mod_id, top_mod = sorted_mods[0]

    if len(sorted_mods) >= 2:
        second_total = sorted_mods[1][1]["total"]
        if top_mod["total"] < second_total * DOMINANCE_RATIO:
            return ("skip_no_dominant", None, None, None, [],
                    "no dominant (%d vs %d)" %
                    (top_mod["total"], second_total))

    n_unique = len(top_mod["labels"])
    score = 4 if n_unique >= 2 else 3
    used_labels = sorted(top_mod["labels"].keys())
    return ("tag", top_mod_id, top_mod["prefix"], score, used_labels, "ok")


def merge_module_into_tags(old_tags, module):
    """
    在 tags 中追加 module 单 token. 删除其它 module token (避免冲突),
    保留 io_/reg_/tramp_/via_/未知 token. 重跑幂等.
    """
    kept = []
    if old_tags:
        for t in old_tags.split(";"):
            t = t.strip()
            if not t:
                continue
            # 删除已有的 module 直接 token (重写)
            if t in ALL_MODULES:
                continue
            # via_<module>: 保留 (扩散结果, 由 propagate 管)
            kept.append(t)
    kept.insert(0, module)  # 模块直接命中放在最前
    return ";".join(kept)


def main():
    if not os.path.isfile(LABEL_REFS):
        sys.stderr.write("ERROR: %s 不存在; 先跑 ExportFunctionLabelRefs.py\n" %
                         LABEL_REFS)
        return 1
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    label_refs = {}
    with open(LABEL_REFS, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            label_refs[r["address"].lower()] = r

    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    if "tags" not in fieldnames:
        fieldnames.append("tags")
        for r in rows:
            r["tags"] = ""

    buckets = {
        "tag_score3": 0,
        "tag_score4": 0,
        "skip_already_proposed": 0,
        "skip_score5_existing": 0,
        "skip_already_named_in_ghidra": 0,
        "skip_dispatcher": 0,
        "skip_assert_only": 0,
        "skip_no_dominant": 0,
        "skip_no_module": 0,
        "skip_not_in_label_refs": 0,
    }
    sample_score3 = []
    sample_score4 = []

    for row in rows:
        addr = row["address"].lower()
        if addr not in label_refs:
            buckets["skip_not_in_label_refs"] += 1
            continue
        existing_proposed = (row.get("proposed_name") or "").strip()
        existing_score = (row.get("score") or "").strip()

        if existing_proposed:
            buckets["skip_already_proposed"] += 1
            continue
        if existing_score == "5":
            buckets["skip_score5_existing"] += 1
            continue
        if not is_auto_name(row.get("name", "")):
            buckets["skip_already_named_in_ghidra"] += 1
            continue

        top_str = label_refs[addr]["top_labels"]
        decision, module, prefix, score, used, dbg = decide(top_str)

        if decision == "skip_dispatcher":
            buckets["skip_dispatcher"] += 1
            continue
        if decision == "skip_assert_only":
            buckets["skip_assert_only"] += 1
            continue
        if decision == "skip_no_dominant":
            buckets["skip_no_dominant"] += 1
            continue
        if decision == "skip_no_module":
            buckets["skip_no_module"] += 1
            continue

        addr_int = int(addr, 16)
        proposed = "%s_%08x" % (prefix, addr_int)
        row["proposed_name"] = proposed
        row["score"] = str(score)
        row["tags"] = merge_module_into_tags(row.get("tags") or "", module)

        if score == 3:
            buckets["tag_score3"] += 1
            if len(sample_score3) < 10:
                sample_score3.append("  %s  %-30s  module=%s" %
                                     (addr, proposed, module))
        else:
            buckets["tag_score4"] += 1
            if len(sample_score4) < 10:
                sample_score4.append("  %s  %-30s  module=%s  labels=%d" %
                                     (addr, proposed, module, len(used)))

    print("=" * 72)
    print("[merge label-refs -> proposals]")
    print("  source: %s (%d funcs)" % (LABEL_REFS, len(label_refs)))
    print("  target: %s (%d rows)" % (PROPOSALS, len(rows)))
    print("-" * 72)
    for k in [
            "tag_score3", "tag_score4",
            "skip_already_proposed", "skip_score5_existing",
            "skip_already_named_in_ghidra",
            "skip_dispatcher", "skip_assert_only", "skip_no_dominant",
            "skip_no_module", "skip_not_in_label_refs"]:
        print("  %-30s = %d" % (k, buckets[k]))
    print("-" * 72)
    if sample_score3:
        print("[sample] score=3 (前 10):")
        for line in sample_score3:
            print(line)
    if sample_score4:
        print("[sample] score=4 (前 10):")
        for line in sample_score4:
            print(line)

    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("\n[wrote] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
