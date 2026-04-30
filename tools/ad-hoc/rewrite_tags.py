#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rewrite_tags.py  --  把 naming-proposals.csv 的 tags 列从旧格式转新简化格式

旧 → 新 token 映射:
    io_family:bg|win|pal           →  io_bg;io_win;io_pal
    io_reg:DISPCNT|BG0CNT          →  reg_DISPCNT;reg_BG0CNT
    data_label:foo|bar             →  <module>             (折叠为模块名, 单 token)
    data_label_via:m(...)          →  (删除, 由 propagate 重生)
    fid_trampoline:foo|bar         →  tramp_foo;tramp_bar

同时检测由 propagate 写入的扩散行 (proposed_name 形如 <module>_<8hex>
+ score=2 + 含 data_label_via 或新格式 via_ tag) 并重置:
    proposed_name 清空, score 清空
这样下次 propagate 跑时从干净状态出发.

跳过条件: score=5 (FID 强证据, 不动) / score=3,4 (label 直接命中, 保留)

输出: doc/dev/naming-proposals.csv (in-place 覆写, 备份到 .bak-pre-rewrite-tags)
"""

import csv
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import (
    derive_module_from_label, ALL_MODULES,
    IO_FAMILY_RENAME, IO_FAMILY_TAGS, is_auto_name,
)

PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")
BACKUP = PROPOSALS + ".bak-pre-rewrite-tags"

PROPAGATE_PROPOSED_RE = re.compile(r"^[a-z_]+_[0-9a-f]{8}$")


def split_pipe_value(s):
    return [x.strip() for x in s.split("|") if x.strip()]


def rewrite_tags(old_tags):
    """
    返回 (new_tags_str, had_via_tag).
    had_via_tag = True 表示原 tags 含扩散结果 (caller 应被重置).
    """
    if not old_tags:
        return "", False
    new_tokens = []
    had_via = False
    for tok in old_tags.split(";"):
        tok = tok.strip()
        if not tok:
            continue
        # === 旧 key:value 格式 ===
        if tok.startswith("io_family:"):
            for f in split_pipe_value(tok[len("io_family:"):]):
                old = "io_" + f
                # 用语义化 family 名取代 io_<f>
                new_tokens.append(IO_FAMILY_RENAME.get(old, old))
            continue
        if tok.startswith("io_reg:"):
            # reg_* 全部丢弃 (信息冗余于 family, 简化原则)
            continue
        if tok.startswith("data_label:"):
            modules_seen = set()
            ordered = []
            for lbl in split_pipe_value(tok[len("data_label:"):]):
                m, _ = derive_module_from_label(lbl)
                if m and m not in modules_seen:
                    modules_seen.add(m)
                    ordered.append(m)
            for m in ordered:
                if m not in new_tokens:
                    new_tokens.append(m)
            continue
        if tok.startswith("data_label_via:"):
            had_via = True
            continue
        if tok.startswith("fid_trampoline:"):
            for n in split_pipe_value(tok[len("fid_trampoline:"):]):
                new_tokens.append("tramp_" + n)
            continue
        # === 单 token 格式 (新或半新) ===
        if tok.startswith("via_"):
            # multi-tag 体系下 via_<X> 重命名为 <X> (X∈ALL_MODULES); 否则丢弃
            mod = tok[4:]
            if mod in ALL_MODULES:
                new_tokens.append(mod)
            had_via = True
            continue
        # 旧 io_<family> 单 token: 翻译为新名字
        if tok in IO_FAMILY_RENAME:
            new_tokens.append(IO_FAMILY_RENAME[tok])
            continue
        # reg_* 单 token: 丢弃
        if tok.startswith("reg_"):
            continue
        if tok in ALL_MODULES or tok in IO_FAMILY_TAGS:
            new_tokens.append(tok)
            continue
        if tok.startswith("tramp_"):
            new_tokens.append(tok)
            continue
        # 未知 token
        sys.stderr.write("[warn] 未识别 tag: %r (保留原样)\n" % tok)
        new_tokens.append(tok)
    # 去重保序
    seen = set()
    deduped = []
    for t in new_tokens:
        if t in seen:
            continue
        seen.add(t)
        deduped.append(t)
    return ";".join(deduped), had_via


def main():
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    with open(PROPOSALS, "rb") as f, open(BACKUP, "wb") as g:
        g.write(f.read())
    print("[backup] %s" % BACKUP)

    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    print("[load] %d rows; fields=%s" % (len(rows), fieldnames))

    n_rewrite = 0
    n_reset = 0
    for r in rows:
        old_tags = r.get("tags") or ""
        new_tags, had_via = rewrite_tags(old_tags)
        if new_tags != old_tags:
            r["tags"] = new_tags
            n_rewrite += 1
        # 重置由 propagate 写入的扩散行:
        # 触发条件: score=2 + 原 tags 含 via, 且 proposed_name 是占位形式
        if (had_via
                and (r.get("score") or "").strip() == "2"
                and PROPAGATE_PROPOSED_RE.match(r.get("proposed_name") or "")):
            r["proposed_name"] = ""
            r["score"] = ""
            n_reset += 1

    print("[rewrite] tags 行被改写 : %d" % n_rewrite)
    print("[reset  ] propagate 扩散行重置 : %d" % n_reset)

    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("[wrote] %s" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
