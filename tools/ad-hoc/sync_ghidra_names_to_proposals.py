#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_ghidra_names_to_proposals.py

把 Ghidra 已 USER_DEFINED 命名的函数名同步回 doc/dev/naming-proposals.csv 的 name 列.

数据流:
  Ghidra (.rep)  --[ExportFunctionInventory.py]-->  temp/ghidra-functions.csv
                                                      |
                                                      v
                                  doc/dev/naming-proposals.csv  <-- (本脚本)

何时用:
  跑完 RenameKnownFunctions.py / ApplyNamingProposals.py / 自定义 Annotate*.py 之后,
  Ghidra 内函数已改名, 但 CSV 的 name 列仍是 FUN_xxxxxxxx. 本脚本把 Ghidra 真名拷回 CSV.

策略:
  对每个 Ghidra source != DEFAULT 的函数 (即 USER_DEFINED 等):
    - 若 CSV name == ghidra name             -> 跳过 (已同步)
    - 若 CSV name 是 FUN_/SUB_/thunk_FUN_     -> 更新 name = ghidra name,
                                                  并清空 proposed_name + score
                                                  (proposal 已落地为现实, 不再是 todo)
    - 若 CSV name 已是其它命名                 -> 警告 (可能 Ghidra 又改了名)

不做的事:
  - 不改 tags 列
  - 不动 score=5 行的 proposed_name (强证据保留)
  - 不动 Ghidra source == DEFAULT 的行

用法:
  python tools/ad-hoc/sync_ghidra_names_to_proposals.py [--dry-run]
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GHIDRA_FUNCS = REPO / "temp" / "ghidra-functions.csv"
PROPOSALS = REPO / "doc" / "dev" / "naming-proposals.csv"

AUTO_NAME_RE = re.compile(r"^(FUN_|SUB_|thunk_FUN_)[0-9a-fA-F]{8}$")


def main():
    dry = "--dry-run" in sys.argv

    if not GHIDRA_FUNCS.exists():
        print("ERROR: %s not found" % GHIDRA_FUNCS, file=sys.stderr)
        print("  先跑: tools\\asm-regen\\ghidra-run-script.bat ExportFunctionInventory.py", file=sys.stderr)
        sys.exit(1)

    # 加载 Ghidra inventory: address -> (name, source)
    ghidra_names = {}
    with GHIDRA_FUNCS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ghidra_names[r["address"]] = (r["name"], r["source"])

    # 加载 proposals
    with PROPOSALS.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    n_synced = 0
    n_proposal_cleared = 0
    n_warn_ghidra_renamed = 0
    n_skipped_already_synced = 0
    samples = []

    for row in rows:
        addr = row[0]
        cur_name = row[1]
        cur_proposed = row[2] if len(row) > 2 else ""
        cur_score = row[3] if len(row) > 3 else ""

        gh = ghidra_names.get(addr)
        if gh is None:
            continue
        gh_name, gh_source = gh
        if gh_source == "DEFAULT":
            continue
        if AUTO_NAME_RE.match(gh_name):
            continue

        if cur_name == gh_name:
            n_skipped_already_synced += 1
            continue

        if not AUTO_NAME_RE.match(cur_name):
            # CSV name 已是非 auto, 但与 Ghidra 不同 -> Ghidra 改名了, 警告
            n_warn_ghidra_renamed += 1
            samples.append("  [warn] %s csv=%s vs ghidra=%s" % (addr, cur_name, gh_name))
            continue

        # 同步: 更新 name 列, 一律清空 proposed/score (proposal 已落地)
        old_proposed = cur_proposed
        old_score = cur_score
        row[1] = gh_name
        had_proposal = bool(cur_proposed) or bool(cur_score)
        if had_proposal:
            row[2] = ""
            row[3] = ""
            n_proposal_cleared += 1

        n_synced += 1
        if len(samples) < 15:
            extra = ""
            if had_proposal:
                extra = "  (cleared proposed='%s' score=%s)" % (old_proposed, old_score)
            samples.append("  %s %s -> %s%s" % (addr, cur_name, gh_name, extra))

    print("[summary] %s%s" % (
        "(dry-run) " if dry else "",
        ""))
    print("  synced (FUN_xxx -> ghidra name)     : %d" % n_synced)
    print("    of which proposed_name cleared    : %d" % n_proposal_cleared)
    print("  already in sync                     : %d" % n_skipped_already_synced)
    print("  warn (ghidra name diverged from CSV): %d" % n_warn_ghidra_renamed)
    if samples:
        print("\n  samples:")
        for s in samples:
            print(s)

    if dry:
        print("\n[dry-run] no file written")
        return

    if n_synced == 0:
        print("\n[noop] nothing to write")
        return

    with PROPOSALS.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for row in rows:
            w.writerow(row)
    print("\n[wrote] %s" % PROPOSALS)


if __name__ == "__main__":
    main()
