#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrate_csv_collapse_io_tags.py  --  把 naming-proposals.csv 的 IO 寄存器列折叠到 tags

旧 schema (10 列):
    address, name, primary_family, all_families, total_refs, unique_regs,
    top_regs, proposed_name, score, tags

新 schema (5 列):
    address, name, proposed_name, score, tags

迁移规则 (新简化格式, 单 token, 仅 family 级语义):
    primary_family + all_families  →  family 语义 tag, 顺序按命中数降序
        "bg:4|display:1|pal:1" → "bg;display;palette"
    top_regs                       →  丢弃 (reg_* 信息冗余于 family)
    total_refs, unique_regs        →  丢弃

family 重命名:
    pal → palette,  win → window,  obj → sprite,  snd → sound,
    bg/vram/display/blend/dma/timer/input/sio/sys → 同名 (去 io_ 前缀)
"""

import csv
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "ad-hoc"))

from label_modules import IO_FAMILY_RENAME, IO_FAMILY_TAGS

PROPOSALS = os.path.join(REPO_ROOT, "doc", "dev", "naming-proposals.csv")
BACKUP = PROPOSALS + ".bak-pre-collapse-io-tags"

OLD_FIELDS = [
    "address", "name", "primary_family", "all_families",
    "total_refs", "unique_regs", "top_regs",
    "proposed_name", "score", "tags",
]
NEW_FIELDS = ["address", "name", "proposed_name", "score", "tags"]


HIT_COUNT_RE = re.compile(r"\((\d+)\)$")


def strip_count(token):
    """'bg:4' -> 'bg';  'DISPCNT(1)' -> 'DISPCNT'."""
    tok = token.strip()
    if not tok:
        return ""
    # family 形式: name:N
    if ":" in tok and HIT_COUNT_RE.search(tok) is None:
        return tok.split(":", 1)[0]
    # reg 形式: NAME(N)
    return HIT_COUNT_RE.sub("", tok)


def derive_family_tokens(primary, all_fams):
    """
    primary_family = "bg"
    all_families   = "bg:4|display:1|pal:1"
    -> ['bg', 'display', 'palette']  (all_families 已按降序; pal→palette 等)
    """
    if all_fams:
        names = [strip_count(t) for t in all_fams.split("|") if t.strip()]
        names = [n for n in names if n]
        if names:
            return [IO_FAMILY_RENAME.get("io_" + n, n) for n in names]
    if primary:
        return [IO_FAMILY_RENAME.get("io_" + primary, primary)]
    return []


def merge_tags(old_tags, family_tokens):
    """
    删除旧 family/reg token (旧 key:value 形式 io_family:* / io_reg:*,
    旧单 token io_*/reg_*, 新单 token palette/vram/bg/...), 拼上新 family token.
    保留模块/扩散/tramp tag.
    """
    kept = []
    if old_tags:
        for tok in old_tags.split(";"):
            tok = tok.strip()
            if not tok:
                continue
            if tok.startswith("io_family:") or tok.startswith("io_reg:"):
                continue
            if tok.startswith("io_") or tok.startswith("reg_"):
                continue
            if tok in IO_FAMILY_TAGS:
                continue
            kept.append(tok)
    return ";".join(list(family_tokens) + kept)


def main():
    if not os.path.isfile(PROPOSALS):
        sys.stderr.write("ERROR: %s 不存在\n" % PROPOSALS)
        return 1

    # 备份
    with open(PROPOSALS, "rb") as fin, open(BACKUP, "wb") as fout:
        fout.write(fin.read())
    print("[backup] %s" % BACKUP)

    # 读旧
    with open(PROPOSALS, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        old_fields = list(reader.fieldnames or [])
        rows = list(reader)
    print("[load  ] %d rows; fields=%s" % (len(rows), old_fields))

    # 检测 schema
    has_old_io_cols = all(c in old_fields for c in
                          ("primary_family", "all_families", "top_regs"))
    if not has_old_io_cols:
        print("[skip  ] 已是新 schema (无 IO 列), 不迁移")
        return 0

    # 迁移
    n_with_family = 0
    for r in rows:
        primary = (r.get("primary_family") or "").strip()
        all_fams = (r.get("all_families") or "").strip()
        family_tokens = derive_family_tokens(primary, all_fams)
        if family_tokens:
            n_with_family += 1
        r["tags"] = merge_tags(r.get("tags") or "", family_tokens)

    print("[merge ] family tokens added : %d rows" % n_with_family)

    # 写新 schema
    with open(PROPOSALS, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=NEW_FIELDS,
                                extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in NEW_FIELDS})

    print("[wrote ] %s (5 cols)" % PROPOSALS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
