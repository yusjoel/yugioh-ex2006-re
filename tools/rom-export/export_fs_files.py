#!/usr/bin/env python3
"""
把 ROM 内嵌文件系统的 339 个文件按原始路径导出到 fs/。

== FS 布局（正确对齐，见 fix #12）==
- FS 数据区基址：ROM 0x01E64684
- 声称大小 (szs[0])：0x70350 = 459,600 B（= FID 1..338 的 tight-pack 总长）
- **实际大小**：0x70420 = 459,808 B（含 FID 339 orphan palette，位于 FS_SIZE 声称之外 208 B）
- 索引：data/fs-tables.s（339 × u32 offset + 340 × u32 size）
- 路径：data/file-paths.s（339 条 null 终止 ASCII）

== 关键映射：path[i] ↔ FID[i+1] ==
早期 export_fs_files.py 误用 shift=0（path[i] ↔ FID[i]），导致 52/63 个
.LZn* 文件的 fs/ 文件名与内容错位。本脚本按正确映射重建，字节数据和 build
byte-identical 保持不变（FID 顺序没变），只是文件命名修正。

- FID 0：FS 根 meta（off=0, sz=0x70350 覆盖整片），无对应 path
- FID 1..338：tight-pack 在 FS_BASE..FS_BASE+0x70350
- FID 339：orphan palette，`paths[338]` = "titleEx/title_obj_s.LZnclr"
  data @ FS_BASE + 0x70350 = 0x01ED49D4，大小 szs[339] = 208 B（位于 FS_SIZE 外）

== 重名 ==
同名 path 多次出现（OCG/TCG 等变体）时，同名第 N 次（N ≥ 1）追加 `_dup{N}` 后缀。
正确 shift=+1 下，dup 配对为 (奇 FID, 偶 FID)。

== 产出 ==
  fs/<path>                    — 339 个文件原始字节
  data/fs-payload.s            — 单一 label + 339 条 .incbin，按 FID 1..339 顺序

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
FS_MAIN_SIZE  = 0x00070350   # FS 表 szs[0] 声称的 "根 meta" 大小；仅覆盖 FID 1..338
FS_TOTAL_SIZE = 0x00070420   # 含 FID 339 orphan palette 的真实总长（= FS_MAIN_SIZE + 208）
FS_END_MAIN   = FS_BASE + FS_MAIN_SIZE   # 0x01ED49D4 (old)
FS_END        = FS_BASE + FS_TOTAL_SIZE  # 0x01ED4AA4 (new)

FS_TABLES     = 0x01E63BE8          # offset_table (339×u32) + size_table (340×u32)
NUM_PATHS     = 339                 # 路径表与 offset_table 项数
NUM_FIDS      = 339                 # 真实 FID 数（1..339），path[338] 对应 FID 339 orphan

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
    if len(paths) != NUM_PATHS:
        raise RuntimeError(f"expected {NUM_PATHS} paths, got {len(paths)}")
    return paths


def read_fs_tables(rom: bytes) -> tuple[list[int], list[int]]:
    offs = [struct.unpack_from("<I", rom, FS_TABLES + i * 4)[0]
            for i in range(NUM_PATHS)]
    szs = [struct.unpack_from("<I", rom, FS_TABLES + NUM_PATHS * 4 + i * 4)[0]
           for i in range(NUM_PATHS + 1)]
    return offs, szs


def disambiguate(rel: str, counter: dict[str, int]) -> str:
    """重名时给第 N 次出现（N≥1）追加 _dup{N} 后缀。"""
    n = counter.get(rel, 0)
    counter[rel] = n + 1
    if n == 0:
        return rel
    p = Path(rel)
    stem = p.stem
    suffix = p.suffix
    new_name = f"{stem}_dup{n}{suffix}"
    return str(p.parent / new_name).replace("\\", "/")


def fid_offset_size(fid: int, offs: list[int], szs: list[int]) -> tuple[int, int]:
    """FID → (FS-相对 offset, size)。FID 339 (orphan) 特殊处理。"""
    if fid < NUM_PATHS:  # FID 1..338
        return offs[fid], szs[fid]
    # FID 339：紧跟 FID 338 之后，长度 szs[339]
    assert fid == NUM_FIDS, f"unexpected FID {fid}"
    return offs[NUM_PATHS - 1] + szs[NUM_PATHS - 1], szs[NUM_PATHS]


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

    # 验证 FID 0 是 FS 根 meta
    if offs[0] != 0 or szs[0] != FS_MAIN_SIZE:
        raise RuntimeError(f"FID 0 不是 FS 根 meta: off=0x{offs[0]:X} sz=0x{szs[0]:X}")
    # 验证 FID 1..338 tight-pack 到 FS_MAIN_SIZE
    expected = 0
    for fid in range(1, NUM_PATHS):
        if offs[fid] != expected:
            raise RuntimeError(
                f"FID {fid} 布局异常: off=0x{offs[fid]:X} expected=0x{expected:X}")
        expected += szs[fid]
    if expected != FS_MAIN_SIZE:
        raise RuntimeError(
            f"FID 1..338 tight-pack 总长异常: 0x{expected:X} vs 0x{FS_MAIN_SIZE:X}")
    # 验证 szs[339] orphan 段
    orphan_off = FS_MAIN_SIZE  # FID 339 起点（FS-相对）
    orphan_sz = szs[NUM_PATHS]
    if orphan_off + orphan_sz != FS_TOTAL_SIZE:
        raise RuntimeError(
            f"FID 339 布局异常: off=0x{orphan_off:X} sz={orphan_sz} "
            f"expected total=0x{FS_TOTAL_SIZE:X}"
        )

    # 清空旧 fs/（shift=0 产物文件名错位，整树重建更安全）
    if OUT_FS_DIR.exists():
        import shutil
        shutil.rmtree(OUT_FS_DIR)
    OUT_FS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_S_PATH.parent.mkdir(parents=True, exist_ok=True)

    used_counter: dict[str, int] = {}
    export_rows: list[tuple[int, str, int]] = []  # (fid, rel_path, size)
    total_bytes = 0

    # 正确映射：FID 1..339，path = paths[fid-1]
    for fid in range(1, NUM_FIDS + 1):
        rel_orig = paths[fid - 1]
        rel = disambiguate(rel_orig, used_counter)
        off, sz = fid_offset_size(fid, offs, szs)
        data = rom[FS_BASE + off : FS_BASE + off + sz]
        if len(data) != sz:
            raise RuntimeError(f"FID {fid} {rel}: 读取 {len(data)} B ≠ sz {sz}")
        dst = OUT_FS_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        export_rows.append((fid, rel, sz))
        total_bytes += sz

    if total_bytes != FS_TOTAL_SIZE:
        raise RuntimeError(
            f"导出总长 0x{total_bytes:X} ≠ FS_TOTAL 0x{FS_TOTAL_SIZE:X}")

    # 生成 data/fs-payload.s
    lines = [
        "@ ROM 内嵌文件系统数据区（由 tools/rom-export/export_fs_files.py 生成）",
        f"@ ROM 范围: 0x{FS_BASE:X} - 0x{FS_END:X}"
        f"  ({FS_TOTAL_SIZE:,} B = 0x{FS_TOTAL_SIZE:X})",
        f"@   含 FID 1..338 主区 (0x{FS_MAIN_SIZE:X} B) + FID 339 orphan palette ({orphan_sz} B)",
        "@ 339 个文件按 FID 1..339 顺序 tight-pack（FID 0 是 FS 根 meta，被 FID 1..338 bytes 覆盖，不单独导出）",
        "@ 索引：data/fs-tables.s；路径：data/file-paths.s",
        "@ 映射：path[i] ↔ FID[i+1]（见 export_fs_files.py 注释）",
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

    print(f"导出 {len(export_rows)} 个 FS 文件到 {OUT_FS_DIR}/  "
          f"(共 {total_bytes:,} B = 0x{total_bytes:X})")
    print(f"生成 {OUT_S_PATH}")
    print(f"重名经 _dup{{N}} 后缀消歧：{dup_total} 个")
    print("扩展名分布：" + ", ".join(f".{e}:{c}" for e, c in ext_cnt.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
