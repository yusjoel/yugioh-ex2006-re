#!/usr/bin/env python3
"""
`.ydc` 决斗卡组文件结构化导出（任务 B1 - 第一阶段）。

== 进度说明 ==
B1 任务分为"基础结构化"与"语义解码"两部分。本脚本完成**第一阶段**：
  ✓ 从 ROM 按 path[i]↔FID[i+1] 正确对齐读 215 个 .ydc
  ✓ 识别 10 字节 header（magic=0x01 + 3B metadata + 4B key + u16 count）
  ✓ 按 header.count 切出 body（u16 数组）和 tail（尾部可变字节）
  ✓ 生成 byte-identical 可重建的 data/ydc-all.s
  ✗ 语义解码：so_code × qty 编码、3 种 4-byte key 的含义（4f57443f/7f217741/39a7cf42）
    尾部字段（多为 0，但 LV2_kaeru 等含非零数据）的用途

未来 B1 延续需要追 .ydc loader 函数（FS 表基址不是 literal，需反编译追调用链）。

== 头部结构（10 B）==
  +0   u8   magic  = 0x01（全部 215 文件）
  +1   3B   meta   = "CC CC CC"（LV1_*, 若干 SD*）或 "FC 12 00"（其余）
  +4   4B   key    = 4f 57 44 3f ("OWD?") | 7f 21 77 41 | 39 a7 cf 42
                    （共 3 种，按文件名前缀 LV/SD/theme/limit 分布）
  +8   u16  count  = body 中 u16 条目数（常见 40, 41, 45, 60, 80）

== 体（body, count × u16）==
  每个 u16 是 `(so_code*4) | qty` 或裸 `so_code`（取决于上下文，待更详细解码）
  参照 include/macros.inc: deck_entry / deck_card

== 尾（tail, 变长 0..38 B）==
  多数为全 0 填充。少数含 u16 + u16 对（如 LV2_kaeru: 01 00 d6 19 = 1, 0x19D6）。

== 输入 ==
  roms/2343.gba 内 FS 表，shift=+1 对齐读取 215 个 .ydc

== 输出 ==
  data/ydc-all.s                  215 个标签，对应 215 个 .ydc 全字节
  data/ydc-index.json             头部元信息（magic/meta/key/count/size 每文件）

== byte-identical ==
  本 .s 按顺序汇编后 == 215 个 .ydc 文件字节串联（已验证）。
  **不接入 fs-payload.s**：需先修复 FS path/FID off-by-one（任务 #12）。

用法:
    python tools/rom-export/export_ydc_structured.py
"""
from __future__ import annotations

import json
import os
import struct
import sys
from pathlib import Path


ROM_PATH = Path("roms/2343.gba")
OUT_S = Path("data/ydc-all.s")
OUT_INDEX = Path("data/ydc-index.json")

FS_BASE = 0x01E64684
FS_TABLES = 0x01E63BE8
PATHS_BASE = 0x01E6118C
PATHS_END = 0x01E63BE8
NUM_PATHS = 339

KNOWN_KEYS = {
    bytes.fromhex("4f57443f"): "OWD?",     # ASCII "OWD?" — 最常见，theme/limit/LV 多数
    bytes.fromhex("7f217741"): "K_7F",     # 未知，LV1_kuriboh 等
    bytes.fromhex("39a7cf42"): "K_39",     # 未知，SD1-4/SD6
}


def read_paths(rom: bytes) -> list[str]:
    raw = rom[PATHS_BASE:PATHS_END]
    paths: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] == 0:
            i += 1
            continue
        end = raw.find(b"\x00", i)
        paths.append(raw[i:end].decode("ascii"))
        i = end + 1
    return paths


def read_fs_tables(rom: bytes) -> tuple[list[int], list[int]]:
    offs = [struct.unpack_from("<I", rom, FS_TABLES + i * 4)[0]
            for i in range(NUM_PATHS)]
    szs = [struct.unpack_from("<I", rom, FS_TABLES + NUM_PATHS * 4 + i * 4)[0]
           for i in range(NUM_PATHS + 1)]
    return offs, szs


def sanitize(name: str, counter: dict[str, int]) -> str:
    """把 path 变成合法 label，重名追加 _dupN。"""
    base = "ydc_" + name.replace("deck/", "").replace(".ydc", "").replace("/", "_")
    n = counter.get(base, 0)
    counter[base] = n + 1
    if n == 0:
        return base
    return f"{base}_dup{n}"


def emit_ydc_asm(label: str, rom_off: int, blob: bytes) -> list[str]:
    lines = []
    magic = blob[0]
    meta = blob[1:4].hex(" ")
    key = blob[4:8]
    key_name = KNOWN_KEYS.get(key, "KEY_?")
    count = struct.unpack_from("<H", blob, 8)[0]
    body_end = 10 + count * 2

    lines.append("")
    lines.append(
        f"@ ---- {label} @ ROM 0x{rom_off:07X} sz={len(blob)} "
        f"key={key_name} count={count} ----"
    )
    lines.append(f"{label}:")
    # header
    lines.append(f"\t.byte 0x{magic:02X}  @ magic")
    lines.append(
        f"\t.byte 0x{blob[1]:02X}, 0x{blob[2]:02X}, 0x{blob[3]:02X}  @ meta (= {meta})"
    )
    lines.append(
        f"\t.byte 0x{blob[4]:02X}, 0x{blob[5]:02X}, 0x{blob[6]:02X}, 0x{blob[7]:02X}  @ key ({key_name})"
    )
    lines.append(f"\t.hword {count}  @ body count (entries)")

    # body: count × u16
    lines.append(f"@ body ({count} × u16):")
    for i in range(count):
        u = struct.unpack_from("<H", blob, 10 + i * 2)[0]
        # 尝试显示 so_code*4|qty 解码（仅注释，非权威）
        so = u >> 2
        qty = u & 3
        lines.append(f"\t.hword 0x{u:04X}  @ [{i:2d}] so={so} qty={qty}")

    # tail: 任意字节
    tail = blob[body_end:]
    if tail:
        lines.append(f"@ tail ({len(tail)} B):")
        # 按 16 B 每行组一批
        for start in range(0, len(tail), 16):
            chunk = tail[start : start + 16]
            bytes_str = ", ".join(f"0x{b:02X}" for b in chunk)
            lines.append(f"\t.byte {bytes_str}")

    return lines


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not ROM_PATH.exists():
        print(f"ERROR: ROM 不存在: {ROM_PATH}", file=sys.stderr)
        return 1
    rom = ROM_PATH.read_bytes()
    paths = read_paths(rom)
    offs, szs = read_fs_tables(rom)

    ydc_indices = [i for i, p in enumerate(paths) if p.endswith(".ydc")]

    out_lines: list[str] = [
        "@ ============================================================",
        "@ YDC (Duel Deck) Files — Structured Dump",
        f"@ {len(ydc_indices)} files from FS, shift=+1 alignment",
        "@",
        "@ Header (10 B):",
        "@   +0  u8   magic = 0x01",
        "@   +1  3B   meta  (CC CC CC | FC 12 00)",
        "@   +4  4B   key   (OWD? | 7f217741 | 39a7cf42)",
        "@   +8  u16  count (body 中 u16 条目数)",
        "@ Body: count × u16 (so_code*4|qty style, 待解码)",
        "@ Tail: 变长 0..38 B (多为 0x00 填充)",
        "@",
        "@ Generated by tools/rom-export/export_ydc_structured.py",
        "@ ============================================================",
        "",
        "ydc_all_data:",
    ]

    label_counter: dict[str, int] = {}
    index_entries = []
    total_bytes = 0

    for pi in ydc_indices:
        fid = pi + 1
        off = offs[fid]
        sz = szs[fid]
        abs_off = FS_BASE + off
        blob = rom[abs_off : abs_off + sz]
        label = sanitize(paths[pi], label_counter)
        out_lines.extend(emit_ydc_asm(label, abs_off, blob))

        count = struct.unpack_from("<H", blob, 8)[0]
        key = blob[4:8]
        index_entries.append({
            "path": paths[pi],
            "label": label,
            "rom_off": f"0x{abs_off:X}",
            "size": sz,
            "header": {
                "magic": blob[0],
                "meta_hex": blob[1:4].hex(),
                "key_hex": key.hex(),
                "key_name": KNOWN_KEYS.get(key, "unknown"),
                "count": count,
            },
            "body_bytes": count * 2,
            "tail_bytes": sz - 10 - count * 2,
        })
        total_bytes += sz

    out_lines.append("")
    out_lines.append(
        f"@ Total: {len(ydc_indices)} YDC files, {total_bytes:,} B"
    )
    out_lines.append("")

    OUT_S.parent.mkdir(parents=True, exist_ok=True)
    OUT_S.write_text("\n".join(out_lines), encoding="utf-8")

    # JSON 索引
    OUT_INDEX.write_text(
        json.dumps(
            {
                "total": len(index_entries),
                "total_bytes": total_bytes,
                "entries": index_entries,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"[export_ydc_structured] {len(index_entries)} YDC files, {total_bytes:,} B "
        f"→ {OUT_S} + {OUT_INDEX}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
