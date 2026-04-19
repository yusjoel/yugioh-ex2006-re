#!/usr/bin/env python3
"""
把 ROM 内嵌文件系统（339 条路径，FID 0..338）的每个文件按原始路径导出到 fs/。

== FS 布局 ==
- FS 数据区基址：ROM 0x01E64684，大小 0x70350 = 459,600 B
- 索引：data/fs-tables.s（339 × u32 offset + 340 × u32 size，size[339] 未用）
- 路径：data/file-paths.s（339 条 null 终止 ASCII，与 fs-tables 一一对应）
- FID 0 是 FS 根 meta（off=0, sz=0x70350 = 整片 FS，与 FID 1..338 bytes 重叠）
- FID 1..338 tight-pack 0x70350 B，无 gap 无 overlap → 这是 338 个真实文件

== 重名 ==
99 条路径在 FID 1..338 中出现 >1 次（同名，不同 bytes，可能是 OCG/TCG 版本）。
同名第 N 次 (N ≥ 1) 时，在文件名主干后追加 `_dup{N}` 后缀，扩展名保留。

== 产出 ==
  fs/<original path>                        — 338 个文件原始字节（按 FID 1..338）
  data/fs-payload.s                          — 单一 label + 338 条 .incbin，按 FID 顺序

用法:
    python tools/rom-export/export_fs_files.py
"""
from __future__ import annotations

import os
import re
import struct
import sys
from pathlib import Path

ROM_PATH = Path("roms/2343.gba")

FS_BASE       = 0x01E64684
FS_SIZE       = 0x00070350  # = 459,600 B
FS_END        = FS_BASE + FS_SIZE  # 0x01ED49D4

FS_TABLES     = 0x01E63BE8          # offset_table (339×u32) + size_table (340×u32)
NUM_ENTRIES   = 339                 # FID 0..338

PATHS_BASE    = 0x01E6118C
PATHS_END     = 0x01E63BE8

OUT_FS_DIR    = Path("fs")
OUT_S_PATH    = Path("data/fs-payload.s")


def read_paths(rom: bytes) -> list[str]:
    raw = rom[PATHS_BASE:PATHS_END]
    paths: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] == 0:
            i += 1
            continue
        end = raw.find(b"\x00", i)
        if end < 0:
            break
        paths.append(raw[i:end].decode("ascii"))
        i = end + 1
    if len(paths) != NUM_ENTRIES:
        raise RuntimeError(f"expected {NUM_ENTRIES} paths, got {len(paths)}")
    return paths


def read_fs_tables(rom: bytes) -> tuple[list[int], list[int]]:
    offs = [struct.unpack_from("<I", rom, FS_TABLES + i * 4)[0]
            for i in range(NUM_ENTRIES)]
    szs = [struct.unpack_from("<I", rom, FS_TABLES + NUM_ENTRIES * 4 + i * 4)[0]
           for i in range(NUM_ENTRIES + 1)]
    return offs, szs


def disambiguate(rel: str, counter: dict[str, int]) -> str:
    """重名时给第 N 次出现（N≥1）追加 _dup{N} 后缀。"""
    n = counter.get(rel, 0)
    counter[rel] = n + 1
    if n == 0:
        return rel
    # 在扩展名前插入 _dup{N}
    p = Path(rel)
    stem = p.stem
    # 有可能扩展名本身是多段（如 .LZncgr），保留第一个 .
    suffix = p.suffix  # 带点
    new_name = f"{stem}_dup{n}{suffix}"
    return str(p.parent / new_name).replace("\\", "/")


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

    # 验证 FID 0 是 meta + FID 1..338 tight-pack
    if offs[0] != 0 or szs[0] != FS_SIZE:
        raise RuntimeError(f"FID 0 不是 FS 根 meta: off=0x{offs[0]:X} sz=0x{szs[0]:X}")
    expected = 0
    for fid in range(1, NUM_ENTRIES):
        if offs[fid] != expected:
            raise RuntimeError(
                f"FID {fid} 布局异常: off=0x{offs[fid]:X} expected=0x{expected:X}")
        expected += szs[fid]
    if expected != FS_SIZE:
        raise RuntimeError(f"FS tight-pack 总长异常: 0x{expected:X} vs 0x{FS_SIZE:X}")

    # 导出文件 + 收集路径供 .s 使用
    OUT_FS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_S_PATH.parent.mkdir(parents=True, exist_ok=True)

    used_counter: dict[str, int] = {}
    export_rows: list[tuple[int, str, int]] = []  # (fid, rel_path, size)
    total_bytes = 0

    for fid in range(1, NUM_ENTRIES):
        rel_orig = paths[fid]
        rel = disambiguate(rel_orig, used_counter)
        off = offs[fid]
        sz = szs[fid]
        data = rom[FS_BASE + off : FS_BASE + off + sz]
        dst = OUT_FS_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        export_rows.append((fid, rel, sz))
        total_bytes += sz

    if total_bytes != FS_SIZE:
        raise RuntimeError(f"导出总长 0x{total_bytes:X} ≠ FS 0x{FS_SIZE:X}")

    # 生成 data/fs-payload.s
    lines = [
        "@ ROM 内嵌文件系统数据区（由 tools/rom-export/export_fs_files.py 生成）",
        f"@ ROM 范围: 0x{FS_BASE:X} - 0x{FS_END:X}"
        f"  ({FS_SIZE:,} B = 0x{FS_SIZE:X})",
        "@ 338 个文件按 FID 1..338 顺序 tight-pack（FID 0 是 FS 根 meta，被 FID 1..338 bytes 覆盖，不单独导出）",
        "@ 索引：data/fs-tables.s；路径：data/file-paths.s",
        "",
        "fs_payload:",
    ]
    for fid, rel, sz in export_rows:
        lines.append(f'    .incbin "fs/{rel}"  @ FID {fid:3d}, {sz} B')
    OUT_S_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 统计
    from collections import Counter
    ext_cnt: Counter[str] = Counter()
    for _, rel, _ in export_rows:
        m = re.search(r"\.([A-Za-z0-9]+)$", rel)
        ext_cnt[m.group(1) if m else "(none)"] += 1
    dup_total = sum(v - 1 for v in used_counter.values() if v > 1)

    print(f"导出 {len(export_rows)} 个 FS 文件到 {OUT_FS_DIR}/  (共 {total_bytes:,} B = 0x{total_bytes:X})")
    print(f"生成 {OUT_S_PATH}")
    print(f"重名经 _dup{{N}} 后缀消歧：{dup_total} 个")
    print("扩展名分布：" + ", ".join(f".{e}:{c}" for e, c in ext_cnt.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
