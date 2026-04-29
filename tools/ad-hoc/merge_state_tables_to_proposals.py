#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_state_tables_to_proposals.py  --  方法 5: 状态机表反推 → 命名提案

输入  temp/ghidra-state-tables.csv     ScanPageStateTables.py 的输出
       doc/dev/naming-proposals.csv     现有提案 (找已 tag 信号)
输出  doc/dev/naming-proposals.csv (in-place)

Module 推断策略 (优先级降序):
    P1. caller 在 CSV 中已直接 tag 为 SCENE module → 表归该 module
    P2. caller 已扩散 tag (via_<scene>) → 候选 module (弱信号)
    P3. entry 中已 tag 为 SCENE module 的多数派 → 表归该 module
    P4. caller 名字前缀派生 (如 'pack_list_page_init') → module
    P5. 都无 → 跳过 (输出 unresolved 列表供人工决定)

每张表的处理:
    - 表起点打 USER_DEFINED label "<module>_state_table" (Ghidra label 由
      ImportProjectLabels 类脚本统一管, 此 merger 只更新 CSV)
    - 表的 caller (dispatcher) 加 module tag (score=4, 强证据: 路由这表)
    - 表的 entries 全部加 module tag (score=4, 强证据: 是表成员)
    - 经典 4-entry 表给 init/load/tick/exit 命名 (score=4):
        entry[0] -> <module>_page_init
        entry[1] -> <module>_page_load_assets
        entry[2] -> <module>_page_tick
        entry[3] -> <module>_page_exit
    - 非 4-entry 表只加 module tag, 不强行命名 (score=3, 家族级)

跳过条件 (entry / caller 不被改名):
    - proposed_name 已非空且非占位 (尊重既有强提案)
    - score == 5 (FID)
    - name 列已是非 auto (Ghidra 已手工命名)
"""

import csv
import os
import re
import sys
from collections import Counter, defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    SCENE_MODULES, UTILITY_MODULES, ALL_MODULES, MODULE_TO_PREFIX,
    derive_module_from_func_name, is_auto_name, is_helper_name,
)

STATE_TABLES = os.path.join(REPO_ROOT, "temp", "ghidra-state-tables.csv")
PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")

PROPAGATE_PROPOSED_RE = re.compile(r"^[a-z_]+_[0-9a-f]{8}$")


def parse_tags(s):
    if not s:
        return []
    return [t.strip() for t in s.split(";") if t.strip()]


def parse_entries_field(s):
    """'0x08017574:name|0x080180ac:?' -> [(0x08017574, 'name'), ...]"""
    if not s:
        return []
    out = []
    for tok in s.split("|"):
        tok = tok.strip()
        if not tok or ":" not in tok:
            continue
        addr_str, nm = tok.split(":", 1)
        try:
            addr_int = int(addr_str, 16)
        except Exception:
            continue
        out.append((addr_int, nm))
    return out


def find_direct_scene_tag(tokens):
    """返回 token 中第一个 SCENE module 直接 tag."""
    for t in tokens:
        if t in SCENE_MODULES:
            return t
    return None


def find_via_scene_tag(tokens):
    """返回 token 中第一个 via_<scene> 扩散 tag 对应的 module."""
    for t in tokens:
        if t.startswith("via_"):
            m = t[4:]
            if m in SCENE_MODULES:
                return m
    return None


def find_cluster_scene_tag(tokens):
    """返回 token 中第一个 scene_<scene> 聚类 tag 对应的 module."""
    for t in tokens:
        if t.startswith("scene_"):
            m = t[6:]
            if m in SCENE_MODULES:
                return m
    return None


def get_func_module_hints(addr_int, rows_by_addr):
    """
    返回 (direct_scene, via_scene, cluster_scene, funcname_module).
    direct_scene:   直接 tag 为 SCENE 模块 (强证据)
    via_scene:      via_<scene> 扩散 tag (中证据)
    cluster_scene:  scene_<scene> 聚类 tag (中证据, 来自 cluster 阶段 1)
    funcname_module: 从 name/proposed_name 前缀派生的 module (弱证据)
    """
    r = rows_by_addr.get(addr_int)
    if r is None:
        return (None, None, None, None)
    tokens = parse_tags(r.get("tags") or "")
    direct = find_direct_scene_tag(tokens)
    via = find_via_scene_tag(tokens)
    cluster = find_cluster_scene_tag(tokens)
    nm = r.get("name") or ""
    pn = r.get("proposed_name") or ""
    fn_mod = (derive_module_from_func_name(nm)
              or derive_module_from_func_name(pn))
    if fn_mod and fn_mod in SCENE_MODULES:
        pass
    elif fn_mod:
        fn_mod = None
    return (direct, via, cluster, fn_mod)


def infer_module_for_table(callers, entries, rows_by_addr):
    """
    返回 (module, confidence_label, reason).
    confidence_label: caller_direct / caller_via / caller_cluster /
                      entry_direct / entry_via / entry_cluster /
                      funcname / None
    """
    caller_direct = []
    caller_via = []
    caller_cluster = []
    caller_funcname = []
    for ca, _ in callers:
        d, v, c, fn = get_func_module_hints(ca, rows_by_addr)
        if d: caller_direct.append(d)
        if v: caller_via.append(v)
        if c: caller_cluster.append(c)
        if fn: caller_funcname.append(fn)

    # P1: caller 直接 tag (强证据)
    if caller_direct:
        m = Counter(caller_direct).most_common(1)[0][0]
        return (m, "caller_direct", "caller has direct %s tag" % m)

    # P2: caller via_ 扩散 tag
    if caller_via:
        m = Counter(caller_via).most_common(1)[0][0]
        return (m, "caller_via", "caller has via_%s tag" % m)

    # P3: caller scene_ 聚类 tag
    if caller_cluster:
        m = Counter(caller_cluster).most_common(1)[0][0]
        return (m, "caller_cluster", "caller has scene_%s tag" % m)

    # P4: entry 直接 tag 主导
    entry_direct = []
    entry_via = []
    entry_cluster = []
    for ep, _ in entries:
        d, v, c, fn = get_func_module_hints(ep, rows_by_addr)
        if d: entry_direct.append(d)
        elif v: entry_via.append(v)
        elif c: entry_cluster.append(c)
    if entry_direct:
        c = Counter(entry_direct)
        top_mod, top_count = c.most_common(1)[0]
        second_count = c.most_common(2)[1][1] if len(c) > 1 else 0
        if top_count > second_count:
            return (top_mod, "entry_direct",
                    "%d entries direct %s (second=%d, size=%d)" %
                    (top_count, top_mod, second_count, len(entries)))

    # P5: entry via_ 主导
    if entry_via:
        c = Counter(entry_via)
        top_mod, top_count = c.most_common(1)[0]
        second_count = c.most_common(2)[1][1] if len(c) > 1 else 0
        if top_count > second_count:
            return (top_mod, "entry_via",
                    "%d entries via_%s (second=%d, size=%d)" %
                    (top_count, top_mod, second_count, len(entries)))

    # P6: entry scene_ 聚类主导
    if entry_cluster:
        c = Counter(entry_cluster)
        top_mod, top_count = c.most_common(1)[0]
        second_count = c.most_common(2)[1][1] if len(c) > 1 else 0
        if top_count > second_count:
            return (top_mod, "entry_cluster",
                    "%d entries scene_%s (second=%d, size=%d)" %
                    (top_count, top_mod, second_count, len(entries)))

    # P7: caller 名字前缀
    if caller_funcname:
        m = Counter(caller_funcname).most_common(1)[0][0]
        return (m, "funcname", "caller name prefix -> %s" % m)

    return (None, None, "no signal")


VTABLE_4ENTRY_NAMES = ["page_init", "page_load_assets", "page_tick", "page_exit"]


def update_func_with_module(row, module, score, proposed_name=None):
    """
    给 row (dict from CSV) 添加 module tag, 设 score, 可选写 proposed_name.
    跳过条件:
      - score=5 (FID)
      - 已 Ghidra 命名 (name 非 auto): 仅加 tag, 不动 proposed_name/score
      - 已有非占位 proposed_name: 仅加 tag
    返回 (action, was_changed)
      action ∈ {'tag', 'tag+rename', 'skip_score5', 'tag_only_named'}
    """
    existing_score = (row.get("score") or "").strip()
    existing_proposed = (row.get("proposed_name") or "").strip()
    nm = row.get("name") or ""

    if existing_score == "5":
        return ("skip_score5", False)

    tokens = parse_tags(row.get("tags") or "")
    changed = False
    if module not in tokens:
        tokens.append(module)
        # 删 via_<module> (升级为直接证据)
        via_tok = "via_" + module
        if via_tok in tokens:
            tokens.remove(via_tok)
        row["tags"] = ";".join(tokens)
        changed = True

    if not is_auto_name(nm):
        return ("tag_only_named", changed)

    # auto name + 强提案 (非占位): 仅加 tag, 不改名
    if existing_proposed and not PROPAGATE_PROPOSED_RE.match(existing_proposed):
        return ("tag", changed)

    # auto name + 弱/无提案: 写命名
    if proposed_name:
        row["proposed_name"] = proposed_name
        row["score"] = str(score)
        return ("tag+rename", True)

    # 没特定 name (家族级), 给占位
    if not existing_proposed:
        prefix = MODULE_TO_PREFIX.get(module, module)
        addr_int = int(row["address"], 16)
        row["proposed_name"] = "%s_%08x" % (prefix, addr_int)
        row["score"] = str(score)
        return ("tag+rename", True)
    # 已是占位, 不动
    return ("tag", changed)


def main():
    if not os.path.isfile(STATE_TABLES):
        sys.stderr.write("ERROR: %s 不存在; 先跑 ScanPageStateTables.py\n" %
                         STATE_TABLES)
        return 1
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    # --- 加载 CSV ---
    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    rows_by_addr = {int(r["address"], 16): r for r in rows}

    # --- 加载状态表 ---
    tables = []  # list of (table_addr, n_entries, [(entry_addr, name)], [(caller_addr, name)])
    with open(STATE_TABLES, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            entries = parse_entries_field(r.get("entries", ""))
            callers = parse_entries_field(r.get("callers", ""))
            tables.append((int(r["table_addr"], 16),
                           int(r["n_entries"]),
                           entries, callers))
    print("[load] %d state table candidates" % len(tables))

    buckets = {
        "inferred": 0,
        "unresolved_no_caller": 0,
        "unresolved_no_signal": 0,
    }
    by_confidence = defaultdict(int)
    by_module = defaultdict(int)

    n_entry_tag = 0
    n_entry_rename_4 = 0
    n_entry_rename_other = 0
    n_caller_tag = 0
    n_skip_score5 = 0
    n_tag_only_named = 0

    unresolved_samples = []
    inferred_samples = []

    for table_addr, n_entries, entries, callers in tables:
        if not callers:
            buckets["unresolved_no_caller"] += 1
            continue
        module, confidence, reason = infer_module_for_table(
            callers, entries, rows_by_addr)
        if module is None:
            buckets["unresolved_no_signal"] += 1
            if len(unresolved_samples) < 10:
                unresolved_samples.append(
                    "  table 0x%08x  size=%d  callers=%s" % (
                        table_addr, n_entries,
                        ",".join("0x%08x" % c[0] for c in callers)))
            continue

        buckets["inferred"] += 1
        by_confidence[confidence] += 1
        by_module[module] += 1
        if len(inferred_samples) < 30:
            inferred_samples.append(
                "  table 0x%08x  size=%d  -> %s  (%s; %s)" %
                (table_addr, n_entries, module, confidence, reason))

        # 给 caller (dispatcher) 加 module tag
        for ca, _ in callers:
            r = rows_by_addr.get(ca)
            if r is None:
                continue
            action, _ = update_func_with_module(r, module, score=4)
            if action == "skip_score5":
                n_skip_score5 += 1
            elif action == "tag_only_named":
                n_tag_only_named += 1
            elif action in ("tag", "tag+rename"):
                n_caller_tag += 1

        # 给 entries 加 module tag
        is_4entry = (n_entries == 4)
        for idx, (ep, _) in enumerate(entries):
            r = rows_by_addr.get(ep)
            if r is None:
                continue
            proposed = None
            if is_4entry and idx < len(VTABLE_4ENTRY_NAMES):
                # 经典 vtable: 套 init/load/tick/exit 命名
                # 命名形式: <module>_<vtable_name>
                # 但 module 如 'pack' / 'demo' / 'duel_field'
                # 结果: pack_page_init, demo_page_init...
                proposed = "%s_%s" % (module, VTABLE_4ENTRY_NAMES[idx])
            action, _ = update_func_with_module(
                r, module, score=4 if is_4entry else 3,
                proposed_name=proposed)
            if action == "skip_score5":
                n_skip_score5 += 1
            elif action == "tag_only_named":
                n_tag_only_named += 1
            elif action == "tag":
                n_entry_tag += 1
            elif action == "tag+rename":
                if is_4entry:
                    n_entry_rename_4 += 1
                else:
                    n_entry_rename_other += 1

    # --- 输出 ---
    print("=" * 72)
    print("[infer] tables:")
    print("  %-32s = %d" % ("inferred", buckets["inferred"]))
    print("  %-32s = %d" % ("unresolved_no_caller", buckets["unresolved_no_caller"]))
    print("  %-32s = %d" % ("unresolved_no_signal", buckets["unresolved_no_signal"]))
    print("[infer] by confidence:")
    for k in sorted(by_confidence.keys()):
        print("  %-20s = %d" % (k, by_confidence[k]))
    print("[infer] by module:")
    for k in sorted(by_module.keys(), key=lambda m: -by_module[m]):
        print("  %-15s = %d 张表" % (k, by_module[k]))

    print("\n[write]")
    print("  caller tagged              = %d" % n_caller_tag)
    print("  entry tagged (no rename)   = %d" % n_entry_tag)
    print("  entry rename (4-entry)     = %d" % n_entry_rename_4)
    print("  entry rename (other)       = %d" % n_entry_rename_other)
    print("  skip score=5               = %d" % n_skip_score5)
    print("  tag-only named func        = %d" % n_tag_only_named)

    if inferred_samples:
        print("\n[sample] inferred (前 30):")
        for line in inferred_samples:
            print(line)
    if unresolved_samples:
        print("\n[sample] unresolved (前 10):")
        for line in unresolved_samples:
            print(line)

    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("\n[wrote] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
