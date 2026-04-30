#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dump_string_id_to_en.py

构建 logical_id → master_row → EN text 对照表。

数据流:
  ROM 0x08000240 (u16 count) + 0x08000250 (sorted u16 array, len=count)
    -> arr[i] = logical_id  (用 game 代码内的 ID, 比如 0x1004)
       master_row = i        (master pointer table 的行号)
  text/game-strings/en.txt
    -> 按 =NNNN= pad=N 头切块, NNNN 是 master row, 内容是该行 EN 文本

输出: temp/string-id-en.csv
  列: logical_id (hex), master_row (int), en_first_line (text)
"""

from __future__ import annotations

import csv
import re
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROM = REPO / "roms" / "2343.gba"
EN_TXT = REPO / "text" / "game-strings" / "en.txt"
OUT_CSV = REPO / "temp" / "string-id-en.csv"

REMAP_COUNT_OFF = 0x240
REMAP_ARR_OFF = 0x250


RE_ROW_HDR = re.compile(r"^=(\d{4})= pad=\d+(?:\s+\(empty\))?\s*(?:@.*)?$")


def load_remap() -> list[int]:
    with ROM.open("rb") as f:
        f.seek(REMAP_COUNT_OFF)
        cnt = struct.unpack("<H", f.read(2))[0]
        f.seek(REMAP_ARR_OFF)
        arr = list(struct.unpack("<%dH" % cnt, f.read(cnt * 2)))
    return arr


def load_en_by_row() -> dict[int, str]:
    """Parse en.txt, return {master_row: first_line_of_text}."""
    out: dict[int, str] = {}
    cur_row = None
    cur_lines: list[str] = []
    with EN_TXT.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = RE_ROW_HDR.match(line)
            if m:
                # flush previous
                if cur_row is not None:
                    text = "\n".join(cur_lines).strip()
                    if text:
                        out[cur_row] = text.split("\n")[0][:200]
                    else:
                        out[cur_row] = "(empty)"
                cur_row = int(m.group(1))
                cur_lines = []
                continue
            if cur_row is None:
                continue
            cur_lines.append(line)
        if cur_row is not None:
            text = "\n".join(cur_lines).strip()
            if text:
                out[cur_row] = text.split("\n")[0][:200]
            else:
                out[cur_row] = "(empty)"
    return out


def main():
    arr = load_remap()
    print("[remap] %d entries (master_row 0..%d)" % (len(arr), len(arr) - 1))
    print("  arr[0..5]   = %s" % arr[:5])
    print("  arr[1640..] = %s" % arr[1640:])

    en_by_row = load_en_by_row()
    print("[en.txt] %d rows parsed" % len(en_by_row))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["logical_id_hex", "master_row", "en_first_line"])
        for row, lid in enumerate(arr):
            en = en_by_row.get(row, "")
            w.writerow(["0x%x" % lid, row, en])
    print("[done] wrote %s (%d rows)" % (OUT_CSV, len(arr)))

    # Sanity dump: 已知 logical id 验证
    rev = {lid: row for row, lid in enumerate(arr)}
    samples = [0x1004, 0x1005, 0x1036, 0x13f4, 0x138a, 0x1390, 0x319, 0x6c1]
    print("\n[sanity]")
    for lid in samples:
        if lid in rev:
            row = rev[lid]
            en = en_by_row.get(row, "")
            safe = en[:80].encode("ascii", "replace").decode("ascii")
            print("  0x%-6x -> row %4d  %s" % (lid, row, safe))
        else:
            print("  0x%-6x NOT IN REMAP" % lid)


if __name__ == "__main__":
    main()
