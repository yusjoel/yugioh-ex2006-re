#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
join_game_str_funcs_with_text.py

把 temp/game-str-funcs-detail.csv 与 ROM remap 表 + en.txt 合并:

输入:
  - temp/game-str-funcs-detail.csv   (44 个函数 + 候选 id 集合)
  - roms/2343.gba                     (0x240 count + 0x250 sorted u16 array)
  - text/game-strings/en.txt          (master row -> EN 文本)
  - data/game-strings.s 或同分布的 master pointer table @ ROM 0xF40
    (用于反查 direct_string_addrs 对应的 master row)

输出: temp/game-str-funcs-strings.csv
  列: address, name, n_resolved_ids, resolved_ids, en_snippets, en_concat
       address    : 函数地址
       name       : Ghidra 当前名
       n_resolved_ids : 通过 remap 反查命中的 id 数 (可能含 direct_addr 反查)
       resolved_ids   : "row=NNN(0xLID)" 列表
       en_snippets    : "row=NNN: <EN 第一行>" 多行 (\n 在 CSV 内 quote)
       en_concat      : 单行拼接 (用于聚类), 多 EN 用 ' || ' 分隔

日志 stdout: 每函数引用了多少 id, 哪几条 EN 文本.
"""

from __future__ import annotations

import csv
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DETAIL_CSV = REPO / "temp" / "game-str-funcs-detail.csv"
ROM = REPO / "roms" / "2343.gba"
EN_TXT = REPO / "text" / "game-strings" / "en.txt"
OUT_CSV = REPO / "temp" / "game-str-funcs-strings.csv"

REMAP_COUNT_OFF = 0x240
REMAP_ARR_OFF = 0x250
MASTER_TABLE_OFF = 0xF40
MASTER_ROW_COUNT = 1642  # master pointer table 实际只覆盖 0..1641 (虽然 remap 表有 1651)
LANG_NAMES = ["ja", "en", "de", "fr", "it", "es"]
STRING_TABLE_BASE = 0x09DB9C10  # = game_str_ja
ROM_BASE = 0x08000000


RE_ROW_HDR = re.compile(r"^=(\d{4})= pad=\d+(?:\s+\(empty\))?\s*(?:@.*)?$")


def load_remap() -> tuple[list[int], dict[int, int]]:
    """返回 (arr, rev) where arr[i]=lid, rev[lid]=i (master_row)."""
    with ROM.open("rb") as f:
        f.seek(REMAP_COUNT_OFF)
        cnt = struct.unpack("<H", f.read(2))[0]
        f.seek(REMAP_ARR_OFF)
        arr = list(struct.unpack("<%dH" % cnt, f.read(cnt * 2)))
    rev = {lid: row for row, lid in enumerate(arr)}
    return arr, rev


def load_master_addr_to_row() -> dict[int, int]:
    """
    读 master pointer table @ ROM 0xF40 的所有 lang offset, 反建 (abs_addr -> row).
    用于 direct_string_addrs 反查.
    每行 24 B = 6 lang × 4 B offset, 绝对地址 = STRING_TABLE_BASE + offset.
    """
    out: dict[int, int] = {}
    with ROM.open("rb") as f:
        f.seek(MASTER_TABLE_OFF)
        data = f.read(MASTER_ROW_COUNT * 24)
    for row in range(MASTER_ROW_COUNT):
        for lang_idx in range(6):
            off_pos = row * 24 + lang_idx * 4
            offset = struct.unpack("<I", data[off_pos : off_pos + 4])[0]
            abs_addr = STRING_TABLE_BASE + offset
            # 第一次写入即可 (同 row 多 lang 可能映射到同一空 \0; 但同地址 vs row 多对一的少)
            if abs_addr not in out:
                out[abs_addr] = row
    return out


def load_en_by_row() -> dict[int, str]:
    out: dict[int, str] = {}
    cur_row = None
    cur_lines: list[str] = []
    with EN_TXT.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = RE_ROW_HDR.match(line)
            if m:
                if cur_row is not None:
                    text = "\n".join(cur_lines).strip()
                    out[cur_row] = (text.split("\n")[0][:200] if text else "(empty)")
                cur_row = int(m.group(1))
                cur_lines = []
                continue
            if cur_row is None:
                continue
            cur_lines.append(line)
        if cur_row is not None:
            text = "\n".join(cur_lines).strip()
            out[cur_row] = (text.split("\n")[0][:200] if text else "(empty)")
    return out


def parse_int_list(s: str) -> list[int]:
    """解析 '|' 分隔的整数列表, 支持 0x..."""
    if not s:
        return []
    out = []
    for tok in s.split("|"):
        tok = tok.strip()
        if not tok or tok == "...":
            continue
        try:
            if tok.startswith("0x") or tok.startswith("0X"):
                out.append(int(tok, 16))
            else:
                out.append(int(tok))
        except ValueError:
            pass
    return out


def main():
    if not DETAIL_CSV.exists():
        print("ERROR: %s missing - run extract_game_str_func_details.py first" % DETAIL_CSV, file=sys.stderr)
        sys.exit(1)

    arr, rev = load_remap()
    print("[remap] %d entries, %d unique logical_ids" % (len(arr), len(rev)))

    addr2row = load_master_addr_to_row()
    print("[master_table] %d unique abs_addrs map to rows" % len(addr2row))

    en_by_row = load_en_by_row()
    print("[en.txt] %d rows" % len(en_by_row))

    out_rows = []
    n_resolved_total = 0
    n_funcs_with_resolved = 0

    with DETAIL_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            addr = r["address"]
            name = r["name"]
            cur_tags = r["tags"]

            # 只用 word literal: mov #imm 8-bit 太常用作偏移/坐标/计数器, 假阳性高
            ids_word = parse_int_list(r.get("all_word_u16", ""))
            direct = parse_int_list(r.get("direct_string_addrs", ""))

            # 候选集合: 合并去重
            cand = []
            for x in ids_word:
                if x not in cand:
                    cand.append(x)

            resolved = []  # [(row, lid_or_None, en, src)]
            seen_rows = set()

            # path 1: 通过 remap rev 反查
            for x in cand:
                if x in rev:
                    row = rev[x]
                    if row in seen_rows:
                        continue
                    seen_rows.add(row)
                    en = en_by_row.get(row, "")
                    resolved.append((row, x, en, "remap"))

            # path 2: direct_string_addrs 反查 master table
            for absa in direct:
                if absa in addr2row:
                    row = addr2row[absa]
                    if row in seen_rows:
                        continue
                    seen_rows.add(row)
                    en = en_by_row.get(row, "")
                    resolved.append((row, None, en, "direct"))

            resolved.sort(key=lambda t: t[0])

            n_resolved_total += len(resolved)
            if resolved:
                n_funcs_with_resolved += 1

            resolved_ids_str = "|".join(
                "row=%d(%s,%s)" % (row, ("0x%x" % lid if lid is not None else "direct"), src)
                for row, lid, en, src in resolved
            )
            en_snippets = "\n".join(
                "row=%d: %s" % (row, en) for row, lid, en, src in resolved
            )
            en_concat = " || ".join(en for row, lid, en, src in resolved if en)

            out_rows.append(
                {
                    "address": addr,
                    "name": name,
                    "tags": cur_tags,
                    "n_resolved_ids": len(resolved),
                    "resolved_ids": resolved_ids_str,
                    "en_snippets": en_snippets,
                    "en_concat": en_concat[:1500],  # CSV 单元格上限
                }
            )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "address",
                "name",
                "tags",
                "n_resolved_ids",
                "resolved_ids",
                "en_snippets",
                "en_concat",
            ],
        )
        w.writeheader()
        for row in out_rows:
            w.writerow(row)

    print("[done] wrote %s (%d funcs)" % (OUT_CSV, len(out_rows)))
    print(
        "[summary] %d funcs with >=1 resolved id  /  %d total resolved ids"
        % (n_funcs_with_resolved, n_resolved_total)
    )

    # stdout 抽样
    print("\n[sample first 8]")
    for r in out_rows[:8]:
        safe_en = r["en_concat"][:200].encode("ascii", "replace").decode("ascii")
        print("  %s %-30s n=%d  %s" % (r["address"], r["name"], r["n_resolved_ids"], safe_en))


if __name__ == "__main__":
    main()
