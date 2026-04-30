#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_game_str_module_tags.py

把 44 个 game_str 直接 tag 函数的 *模块 tag* 合并进 doc/dev/naming-proposals.csv 第 5 列.

输入 (read-only):
  - temp/game-str-funcs-strings.csv  (本工具链上一步: 函数 -> 引用的 EN 文本)
  - doc/dev/naming-proposals.csv     (主 5 列 schema 表)

输出:
  - doc/dev/naming-proposals.csv     (原地改, 第 5 列追加新 tag, 保持单 token / 分号分隔)

原则:
  - 第 5 列保持单 token 形式 (不重新引入 'data_label:foo|bar' 旧格式)
  - 新 tag 与现有 'game_str' 共存 (e.g. 'game_str' -> 'game_str;pack')
  - 已存在的 tag 不重复添加
  - score / proposed_name 不动 (本轮只做模块归属)
  - 模块 tag 表手工维护, 基于 EN 文本归类 (见下方 ADDR_TO_NEW_TAGS)

执行:
  python tools/ad-hoc/merge_game_str_module_tags.py [--dry-run]
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CSV_PATH = REPO / "doc" / "dev" / "naming-proposals.csv"


# 每个函数要新增的 module tag 列表 (基于 temp/game-str-funcs-strings.csv 的 EN 内容人工归类).
# 注释里写主要 EN 证据.
ADDR_TO_NEW_TAGS: dict[str, list[str]] = {
    # banlist 编辑器 - 引用 "List - September, 2005" + "Plant" (card type as filter)
    "0x08016afc": ["banlist"],
    # 字符表 (charset) 渲染 - 字母/符号面板, 同时被 password 和 name 输入用
    "0x080178b4": ["text_input"],
    "0x0801794c": ["text_input"],
    # 决斗中行动选择 (Card View / Atk Pos / Def Pos / OK / DEL / Activate / YES / NO)
    "0x08017b44": ["duel_field"],
    "0x08018f7c": ["duel_field"],
    # password 输入界面
    "0x08019964": ["pass_input"],
    "0x080199fc": ["text_input"],  # DEL key (charset 通用)
    # banlist 编辑器 - card type (Quick-Play / Ritual) 过滤
    "0x08019b4c": ["banlist"],
    # 0x0801fec0 已是 duel_puzzle (引用 Aqua/Warrior/LIGHT 等 puzzle 元素)
    # 决斗时机说明 ("It is before damage application" + 类型 + Level)
    "0x08023b6c": ["duel_field"],
    # 决斗结果 / 记录屏 (Best Record / Total damage / Incompletion)
    "0x0802c238": ["result_screen"],
    "0x0802c358": ["result_screen"],
    # 0x080cad78: n=0, 无 EN 证据 -> 不打模块 tag (shared helper)
    # 决斗中区域标签 (Fusion Deck: / Graveyard:)
    "0x080cb998": ["duel_field"],
    # 卡片类型/属性标签 (Dragon)
    "0x080cf7d4": ["card_stats"],
    # 0x080d6290: 已 pack
    # 存档对话 (Saving...Do not turn the power OFF)
    "0x080d8804": ["save"],
    # pack/shop (No more can be exchanged)
    "0x080db7c4": ["pack"],
    # 决斗 chain UI (Missed your chance + DP)
    "0x080dba64": ["duel_field"],
    "0x080dc1f8": ["duel_field"],
    # pack/shop UI 按钮文本
    "0x080dc60c": ["pack"],
    "0x080dc664": ["pack"],
    "0x080dc6bc": ["pack"],
    "0x080dc8d0": ["pack"],
    "0x080dc928": ["pack"],
    "0x080dc980": ["pack"],
    "0x080dc9d8": ["pack"],
    "0x080dca30": ["pack"],
    "0x080dca88": ["pack"],
    # password 输入界面 (Enter the password / DEL)
    "0x080de3e8": ["pass_input"],
    # password 校验 (card password incorrect) - 已是 pack, 追加 pass_input
    "0x080e049c": ["pass_input"],
    # 0x080e0758: 已 pack (3 句都 password / shop), 追加 pass_input
    "0x080e0758": ["pass_input"],
    # 0x080e08a4: 已 pack
    # 0x080e0d40: 已 pack
    # 0x080e5ac8: n=0, shared helper
    # 决斗结果记录 (Best Record / %d turn(s))
    "0x080e5c04": ["result_screen"],
    # 0x080eec54 / 0x080eeca8 / 0x080eed50: n<=0 或 (empty), 无证据 -> shared
    # deck builder (Move %s cards to your Deck / Side Deck)
    "0x08100d70": ["deck"],
    # deck builder (Save Recipe + 改 Forbidden/Limited Card List)
    "0x08105f34": ["deck", "banlist"],
    # 0x08107198 / 0x08109a50: n<=1 或 (empty), 无证据
    # 卡类型 (Dinosaur)
    "0x08109e08": ["card_stats"],
}


def merge_tags(existing: str, additions: list[str]) -> str:
    """existing 是 ';' 分隔的单 token tag 串. additions 是要加的新 tag 列表. 去重保持顺序."""
    cur = [t for t in existing.split(";") if t]
    for t in additions:
        if t not in cur:
            cur.append(t)
    return ";".join(cur)


def main():
    dry_run = "--dry-run" in sys.argv

    rows = []
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)

    n_changed = 0
    changes_preview = []

    for row in rows:
        addr = row[0]
        if addr not in ADDR_TO_NEW_TAGS:
            continue
        existing_tags = row[4] if len(row) >= 5 else ""
        new_tags = ADDR_TO_NEW_TAGS[addr]
        merged = merge_tags(existing_tags, new_tags)
        if merged == existing_tags:
            continue
        n_changed += 1
        changes_preview.append((addr, existing_tags, merged))
        # 确保 row 长度 == 5
        while len(row) < 5:
            row.append("")
        row[4] = merged

    print("[merge] %d rows would be changed" % n_changed)
    for addr, old, new in changes_preview[:25]:
        old_disp = old if old else "(empty)"
        print("  %s   %-30s -> %s" % (addr, old_disp, new))
    if len(changes_preview) > 25:
        print("  ... +%d more" % (len(changes_preview) - 25))

    # 未在 CSV 找到的目标地址 (健康检查)
    csv_addrs = {row[0] for row in rows}
    missing = [a for a in ADDR_TO_NEW_TAGS if a not in csv_addrs]
    if missing:
        print("\n[warn] %d ADDR_TO_NEW_TAGS entries not in CSV:" % len(missing))
        for a in missing:
            print("  %s" % a)

    if dry_run:
        print("\n[dry-run] no file written")
        return

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for row in rows:
            w.writerow(row)
    print("\n[done] wrote %s" % CSV_PATH)


if __name__ == "__main__":
    main()
