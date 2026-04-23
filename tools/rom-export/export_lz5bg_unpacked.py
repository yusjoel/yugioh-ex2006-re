#!/usr/bin/env python3
"""
批量解压 26 个 `.LZ5bg` BG 容器文件（任务 A3）。

== 意外发现 ==
`.LZ5bg` 不是 Konami 自研压缩格式。结构和 `.LZn*` 等价：
  1. 外层：BIOS LZ77（magic 0x10）
  2. 4 字节 Konami wrapper：`00 XX XX XX`（XX = u24 LE = 解压后总长）
  3. 内层：NitroSystem 风格二进制文件头 + 3 个数据块
     magic `NTBG`（= C 字面 'GBTN'，疑似 Konami 扩展，非标准 NitroSDK）
     blocks: `PALT` (palette) + `BGDT` (BG tile data) + `DFPL` (screen/layout)

（早期 prompt 称 ".LZ5bg magic 0x01" 源于 `export_fs_files.py` 的 path/FID off-by-one
错位，shift=+1 对齐后 26 个 .LZ5bg 首字节全部 0x10 LZ77。bug #12 已修。）

== 输入 ==
  roms/2343.gba 内 FS 表，shift=+1 对齐读 26 个 .LZ5bg 路径。

== 输出 ==
  fs-decompressed/<orig path>/<stem>.gbtn   NTBG 原始字节（剥 LZ77 + 4B wrapper）
  graphics/fs-lz5bg/_index.json             每文件的 header + 3 个 block 元信息

== NTBG 内部格式（本脚本已识别）==
  [0..4]   magic   = "NTBG" (LE, = 'GBTN' C literal)
  [4..6]   bom     = 0xFEFF
  [6..8]   ver     = (major<<8|minor), 典型 0x0100
  [8..12]  fileSize (NNS 总长, 不含外层 wrapper)
  [12..14] hdrSize = 16
  [14..16] nBlocks = 3

== 块结构 ==
  PALT (palette, 524 B 定长):
    [0..4]   "PALT" LE
    [4..8]   size = 524 (含 8 B 块头)
    [8..12]  u32 color_count (通常 256)
    [12..]   color_count × u16 BGR5
    （相较 NNS PLTT 更简洁，无 fmt/ext/szByte/pRaw 间接寻址）

  BGDT (BG tile data, 可变长):
    [0..4]   "BGDT" LE
    [4..8]   size
    [8..]   （具体 struct 待进一步解，疑似含 tile_count + W/H + raw pixel 数据）

  DFPL (screen/layout, 可变长):
    [0..4]   "DFPL" LE
    [4..8]   size
    [8..]   （可能是 "Dual Frame Palette Layout" 或类似；含常见重复 0x02 pattern）

== 验收 ==
  - 26/26 文件解压成功
  - 每个内层 magic == "NTBG"
  - 每个 PALT 块 size = 524 B（100% 固定）

用法:
    python tools/rom-export/export_lz5bg_unpacked.py
"""
from __future__ import annotations

import json
import os
import struct
import sys
from pathlib import Path


ROM_PATH = Path("roms/2343.gba")
OUT_DIR = Path("fs-decompressed")
INDEX_JSON = Path("graphics/fs-lz5bg/_index.json")

FS_BASE = 0x01E64684
FS_TABLES = 0x01E63BE8
PATHS_BASE = 0x01E6118C
PATHS_END = 0x01E63BE8
NUM_PATHS = 339


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
    offs = [struct.unpack_from("<I", rom, FS_TABLES + i * 4)[0] for i in range(NUM_PATHS)]
    szs = [struct.unpack_from("<I", rom, FS_TABLES + NUM_PATHS * 4 + i * 4)[0]
           for i in range(NUM_PATHS + 1)]
    return offs, szs


def lz77_decompress(data: bytes) -> bytes:
    if not data or data[0] != 0x10:
        raise ValueError(f"非 LZ77: 0x{data[0]:02X}")
    ds = struct.unpack_from("<I", data)[0] >> 8
    out = bytearray()
    pos = 4
    while len(out) < ds:
        if pos >= len(data):
            break
        flags = data[pos]
        pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= ds or pos >= len(data):
                break
            if flags & (1 << bit):
                if pos + 1 >= len(data):
                    break
                b0, b1 = data[pos], data[pos + 1]
                pos += 2
                length = ((b0 >> 4) & 0xF) + 3
                disp = ((b0 & 0xF) << 8) | b1
                start = len(out) - disp - 1
                for i in range(length):
                    out.append(out[start + i])
            else:
                out.append(data[pos])
                pos += 1
    return bytes(out[:ds])


def parse_ntbg(data: bytes) -> dict:
    """解析 NTBG 内层（已剥 4B wrapper）。"""
    magic = data[:4]
    bom = struct.unpack_from("<H", data, 4)[0]
    assert magic == b"NTBG", f"非 NTBG magic: {magic!r}"
    assert bom == 0xFEFF, f"BOM != 0xFEFF: 0x{bom:04X}"
    fs_ = struct.unpack_from("<I", data, 8)[0]
    hs = struct.unpack_from("<H", data, 12)[0]
    nb = struct.unpack_from("<H", data, 14)[0]
    blocks = []
    cur = hs
    for _ in range(nb):
        k = data[cur : cur + 4].decode("ascii", errors="replace")
        sz = struct.unpack_from("<I", data, cur + 4)[0]
        entry: dict = {"kind": k, "offset": cur, "size": sz}
        if k == "PALT":
            cc = struct.unpack_from("<I", data, cur + 8)[0]
            entry["palette"] = {"color_count": cc, "colors_offset": cur + 12}
        elif k == "BGDT":
            entry["body_first_u32s"] = [
                f"0x{x:08X}" for x in struct.unpack_from("<4I", data, cur + 8)
            ]
        elif k == "DFPL":
            entry["body_first_u32s"] = [
                f"0x{x:08X}" for x in struct.unpack_from("<4I", data, cur + 8)
            ]
        blocks.append(entry)
        cur += sz
    return {
        "magic": "NTBG",
        "byte_order": f"0x{bom:04X}",
        "file_size": fs_,
        "header_size": hs,
        "num_blocks": nb,
        "blocks": blocks,
    }


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    rom = ROM_PATH.read_bytes()
    paths = read_paths(rom)
    offs, szs = read_fs_tables(rom)

    lz5bg_indices = [i for i, p in enumerate(paths) if p.endswith(".LZ5bg")]
    if len(lz5bg_indices) != 26:
        print(f"WARN: 预期 26 个 .LZ5bg, 实得 {len(lz5bg_indices)}", file=sys.stderr)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.parent.mkdir(parents=True, exist_ok=True)

    # dup 计数器（path 顺序）
    dup_counter: dict[str, int] = {}
    index: list[dict] = []

    total_comp = 0
    total_decomp = 0

    for pi in lz5bg_indices:
        path = paths[pi]
        fid = pi + 1
        off = offs[fid]
        sz = szs[fid]
        abs_off = FS_BASE + off
        blob = rom[abs_off : abs_off + sz]

        # dup 处理
        n = dup_counter.get(path, 0)
        dup_counter[path] = n + 1
        rel = path
        if n > 0:
            pp = Path(path)
            rel = str(pp.parent / f"{pp.stem}_dup{n}{pp.suffix}").replace("\\", "/")

        d = lz77_decompress(blob)
        if len(d) < 4 or d[0] != 0x00:
            raise ValueError(f"{path}: wrapper byte0={d[0]:#x} 非 0x00")
        total_size_u24 = d[1] | (d[2] << 8) | (d[3] << 16)
        if total_size_u24 != len(d):
            raise ValueError(f"{path}: wrapper total={total_size_u24} ≠ 解压长 {len(d)}")
        ntbg = d[4:]
        parsed = parse_ntbg(ntbg)

        # 写出 .gbtn
        out_rel = rel.replace(".LZ5bg", ".gbtn")
        out_path = OUT_DIR / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(ntbg)

        index.append({
            "path": rel,
            "out": str(out_path.relative_to(OUT_DIR)).replace("\\", "/"),
            "rom_off": f"0x{abs_off:X}",
            "compressed_size": sz,
            "decompressed_size": len(d),
            "ntbg_size": len(ntbg),
            "ntbg": parsed,
        })

        total_comp += sz
        total_decomp += len(ntbg)

    INDEX_JSON.write_text(
        json.dumps({
            "total": len(index),
            "total_compressed": total_comp,
            "total_decompressed": total_decomp,
            "files": index,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    ratio = total_comp / total_decomp if total_decomp else 0
    print(
        f"[export_lz5bg_unpacked] {len(index)}/26 files → {OUT_DIR}/**/*.gbtn  "
        f"— LZ77 {total_comp:,} B → NTBG {total_decomp:,} B (ratio {ratio:.2%})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
