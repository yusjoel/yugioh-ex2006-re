#!/usr/bin/env python3
"""
NNS G2D 资源解析器（任务 A2 + D3）：读 fs-decompressed/ 的 63 个 NNS 文件，
输出结构化 JSON + 可视化 PNG。

== 输入 ==
  fs-decompressed/**/*.{nanr,ncer,ncgr,nclr}（由 A1 export_nns_unpacked.py 产出）

== 解析对象 ==
  - NCLR (Palette)             `RLCN` → PLTT 块
  - NCGR (Character Graphics)  `RGCN` → CHAR 块
  - NCER (Cell Resource)       `RECN` → CEBK 块（+可选 LABL/UEXT）
  - NANR (Cell Animation)      `RNAN` → ABNK 块（+可选 LABL/UEXT）

== 输出 ==
  graphics/fs-nns/<orig path>/<stem>.json                ← 每个文件的结构化 metadata
  graphics/fs-nns/<orig path>/<stem>_palette.png         ← NCLR 的 16×16 色卡
  graphics/fs-nns/<orig path>/<stem>_tiles.png           ← NCGR 用同目录同名 .nclr 渲染的 tile sheet
  graphics/fs-nns/_index.json                            ← 全局摘要（63 条）

== 渲染策略 ==
  - NCLR 单色：每色 16×16 像素；PLTT16 = 16 色单行，PLTT256 = 16 行 × 16 列
  - NCGR：按 8×8 tile 铺平为 32-tile-wide sheet；配对同名 .nclr 的 palette 0；无配对则灰度
  - NCER + NANR：仅 JSON，实际合成帧在 C2/C3 任务中做

== 架构要点 ==
  - NNSG2dBinaryFileHeader (16 B)：magic/byteOrder/version/fileSize/headerSize/dataBlocks
  - NNSG2dBinaryBlockHeader (8 B)：kind/size（含块头）
  - 字段内字节序全 LE；magic 在文件里落盘是反转 ASCII（见 doc/temp/nns-format-notes.md §2）
  - `pRawData` 等 offset 字段 = 相对所在 struct 起点（不是文件头起点）

用法:
    python tools/rom-export/export_nns_parsed.py
"""
from __future__ import annotations

import json
import os
import struct
import sys
import zlib
from pathlib import Path


IN_DIR = Path("fs-decompressed")
OUT_DIR = Path("graphics/fs-nns")
INDEX_JSON = OUT_DIR / "_index.json"


# ============================================================
# PNG 写入（无 Pillow 依赖）
# ============================================================

def _png_chunk(name: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(name + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + name + data + struct.pack(">I", crc)


def save_png_rgb(path: Path, width: int, height: int, pixels: bytes) -> None:
    """RGB888 bytes → PNG (8-bit color type 2)"""
    assert len(pixels) == width * height * 3
    raw = b"".join(
        b"\x00" + pixels[y * width * 3 : (y + 1) * width * 3]
        for y in range(height)
    )
    idat = zlib.compress(raw, 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"IDAT", idat) + _png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def bgr5_to_rgb888(u16: int) -> tuple[int, int, int]:
    r = (u16 & 0x1F) << 3
    g = ((u16 >> 5) & 0x1F) << 3
    b = ((u16 >> 10) & 0x1F) << 3
    # bit 扩展到 8 位（标准 NDS 做法）
    r |= r >> 5
    g |= g >> 5
    b |= b >> 5
    return r, g, b


# ============================================================
# NNS 通用解析
# ============================================================

MAGIC_MAP = {
    b"RLCN": "NCLR",
    b"RGCN": "NCGR",
    b"RECN": "NCER",
    b"RNAN": "NANR",
    b"RAMN": "NMAR",
}


def parse_nns_header(data: bytes) -> dict:
    """解 NNSG2dBinaryFileHeader。"""
    if len(data) < 16:
        raise ValueError("NNS 文件 < 16 B")
    magic_raw = data[:4]
    bom = struct.unpack_from("<H", data, 4)[0]
    ver = struct.unpack_from("<H", data, 6)[0]
    file_size = struct.unpack_from("<I", data, 8)[0]
    hdr_size = struct.unpack_from("<H", data, 12)[0]
    blocks = struct.unpack_from("<H", data, 14)[0]
    if bom != 0xFEFF:
        raise ValueError(f"BOM 不是 0xFEFF: 0x{bom:04X}")
    if file_size != len(data):
        raise ValueError(f"fileSize={file_size} ≠ 实际 {len(data)} B")
    if magic_raw not in MAGIC_MAP:
        raise ValueError(f"不识别 magic: {magic_raw!r}")
    return {
        "magic_raw": magic_raw.decode("ascii"),
        "magic": MAGIC_MAP[magic_raw],
        "version": f"{(ver >> 8) & 0xFF}.{ver & 0xFF}",
        "file_size": file_size,
        "header_size": hdr_size,
        "num_blocks": blocks,
    }


def walk_blocks(data: bytes, hdr_size: int, n_blocks: int) -> list[tuple[str, int, int]]:
    """返回 [(kind_LE, offset_in_file, block_size), ...]。"""
    out = []
    cursor = hdr_size
    for _ in range(n_blocks):
        if cursor + 8 > len(data):
            break
        kind = data[cursor : cursor + 4].decode("ascii", errors="replace")
        size = struct.unpack_from("<I", data, cursor + 4)[0]
        out.append((kind, cursor, size))
        cursor += size
    return out


# ============================================================
# NCLR
# ============================================================

def parse_nclr(data: bytes, hdr: dict) -> dict:
    blocks = walk_blocks(data, hdr["header_size"], hdr["num_blocks"])
    result = {"header": hdr, "blocks": []}
    for kind, off, sz in blocks:
        b = {"kind": kind, "offset": off, "size": sz}
        if kind == "TTLP":  # 'PLTT' LE
            fmt = struct.unpack_from("<I", data, off + 8)[0]
            ext = struct.unpack_from("<I", data, off + 12)[0]
            sz_byte = struct.unpack_from("<I", data, off + 16)[0]
            p_raw = struct.unpack_from("<I", data, off + 20)[0]
            raw_abs = off + 8 + p_raw  # 相对 NNSG2dPaletteData 起点(off+8)
            b["palette"] = {
                "fmt": {3: "PLTT16", 4: "PLTT256"}.get(fmt, f"fmt={fmt}"),
                "extended": bool(ext),
                "size_byte": sz_byte,
                "raw_offset": raw_abs,
                "num_colors": sz_byte // 2,
            }
            colors = []
            for i in range(sz_byte // 2):
                u16 = struct.unpack_from("<H", data, raw_abs + i * 2)[0]
                colors.append(u16)
            b["palette"]["colors_bgr5"] = colors
        result["blocks"].append(b)
    return result


def render_nclr_png(parsed: dict, dst: Path) -> None:
    colors = []
    for b in parsed["blocks"]:
        if b["kind"] == "TTLP":
            colors = b["palette"]["colors_bgr5"]
            break
    if not colors:
        return
    # 16 列，N 行
    n = len(colors)
    cols = 16
    rows = (n + cols - 1) // cols
    sw = 16  # 每色 16px
    W = cols * sw
    H = rows * sw
    pixels = bytearray(W * H * 3)
    for idx, c in enumerate(colors):
        r, g, b = bgr5_to_rgb888(c)
        cx = (idx % cols) * sw
        cy = (idx // cols) * sw
        for yy in range(sw):
            for xx in range(sw):
                p = ((cy + yy) * W + cx + xx) * 3
                pixels[p] = r
                pixels[p + 1] = g
                pixels[p + 2] = b
    save_png_rgb(dst, W, H, bytes(pixels))


# ============================================================
# NCGR
# ============================================================

def parse_ncgr(data: bytes, hdr: dict) -> dict:
    blocks = walk_blocks(data, hdr["header_size"], hdr["num_blocks"])
    result = {"header": hdr, "blocks": []}
    for kind, off, sz in blocks:
        b = {"kind": kind, "offset": off, "size": sz}
        if kind == "RAHC":  # 'CHAR' LE
            h = struct.unpack_from("<H", data, off + 8)[0]
            w = struct.unpack_from("<H", data, off + 10)[0]
            pxf = struct.unpack_from("<I", data, off + 12)[0]
            mt = struct.unpack_from("<I", data, off + 16)[0]
            cf = struct.unpack_from("<I", data, off + 20)[0]
            szb = struct.unpack_from("<I", data, off + 24)[0]
            p_raw = struct.unpack_from("<I", data, off + 28)[0]
            raw_abs = off + 8 + p_raw
            b["char"] = {
                "H_tiles": h if h != 0xFFFF else -1,
                "W_tiles": w if w != 0xFFFF else -1,
                "pixel_fmt": {3: "PLTT16", 4: "PLTT256"}.get(pxf, f"fmt={pxf}"),
                "mapping_type": mt,
                "is_bmp": bool(cf & 0xFF == 1),
                "is_vram_xfer": bool(cf & 0x100),
                "size_byte": szb,
                "raw_offset": raw_abs,
            }
        result["blocks"].append(b)
    return result


def _ncgr_pixels(data: bytes, parsed: dict) -> tuple[bytes, str]:
    """返回 (pixel_indices, pixel_fmt)。pixel_indices 是每字节一像素的 palette index。"""
    for b in parsed["blocks"]:
        if b["kind"] != "RAHC":
            continue
        ch = b["char"]
        raw = data[ch["raw_offset"] : ch["raw_offset"] + ch["size_byte"]]
        if ch["pixel_fmt"] == "PLTT16":
            # 4bpp: 每字节 2 像素，低 nibble 在前
            px = bytearray(len(raw) * 2)
            for i, v in enumerate(raw):
                px[i * 2] = v & 0xF
                px[i * 2 + 1] = (v >> 4) & 0xF
            return bytes(px), "PLTT16"
        elif ch["pixel_fmt"] == "PLTT256":
            return bytes(raw), "PLTT256"
    return b"", "unknown"


def render_ncgr_png(data: bytes, parsed: dict, nclr_parsed: dict | None, dst: Path) -> dict | None:
    """把 NCGR 渲染成 tile sheet PNG；若有 NCLR 用 palette 0，否则灰度。"""
    pixels, fmt = _ncgr_pixels(data, parsed)
    if not pixels:
        return None

    # 估算 tile 数和 sheet 尺寸
    total_px = len(pixels)
    total_tiles = total_px // 64  # 8×8
    if total_tiles == 0:
        return None
    tiles_per_row = 32
    rows_of_tiles = (total_tiles + tiles_per_row - 1) // tiles_per_row
    W = tiles_per_row * 8
    H = rows_of_tiles * 8

    # 准备 palette（RGB888）
    palette_rgb: list[tuple[int, int, int]] = []
    if nclr_parsed:
        for nb in nclr_parsed["blocks"]:
            if nb["kind"] == "TTLP":
                for c in nb["palette"]["colors_bgr5"]:
                    palette_rgb.append(bgr5_to_rgb888(c))
                break
    palette_size = 16 if fmt == "PLTT16" else 256
    if not palette_rgb:
        # 灰度 fallback：idx * (255//palette_size)
        step = 255 // max(palette_size - 1, 1)
        palette_rgb = [(i * step, i * step, i * step) for i in range(palette_size)]
    else:
        # 如果 NCLR 含多组 palette（PLTT16 时 256/16=16 组），只用前 palette_size 个
        palette_rgb = palette_rgb[:palette_size]
        while len(palette_rgb) < palette_size:
            palette_rgb.append((0, 0, 0))

    out = bytearray(W * H * 3)
    # Tile 布局：每 tile = 8×8 像素（按行优先排列 in pixels）
    for ti in range(total_tiles):
        tx = (ti % tiles_per_row) * 8
        ty = (ti // tiles_per_row) * 8
        base = ti * 64
        for yy in range(8):
            for xx in range(8):
                pi = pixels[base + yy * 8 + xx]
                if pi < len(palette_rgb):
                    r, g, bl = palette_rgb[pi]
                else:
                    r = g = bl = 0
                p = ((ty + yy) * W + (tx + xx)) * 3
                out[p] = r
                out[p + 1] = g
                out[p + 2] = bl
    save_png_rgb(dst, W, H, bytes(out))
    return {"tiles": total_tiles, "sheet_wh": [W, H], "palette_used": bool(nclr_parsed)}


# ============================================================
# NCER
# ============================================================

def parse_ncer(data: bytes, hdr: dict) -> dict:
    blocks = walk_blocks(data, hdr["header_size"], hdr["num_blocks"])
    result = {"header": hdr, "blocks": []}
    for kind, off, sz in blocks:
        b = {"kind": kind, "offset": off, "size": sz}
        if kind == "KBEC":  # 'CEBK' LE
            num_cells = struct.unpack_from("<H", data, off + 8)[0]
            attr = struct.unpack_from("<H", data, off + 10)[0]
            cell_arr_off = struct.unpack_from("<I", data, off + 12)[0]
            mapping = struct.unpack_from("<I", data, off + 16)[0]
            has_br = bool(attr & 1)
            cell_arr_abs = off + 8 + cell_arr_off
            cell_size = 16 if has_br else 8
            cells = []
            for i in range(num_cells):
                c_off = cell_arr_abs + i * cell_size
                n_oam = struct.unpack_from("<H", data, c_off)[0]
                c_attr = struct.unpack_from("<H", data, c_off + 2)[0]
                oam_ptr = struct.unpack_from("<I", data, c_off + 4)[0]
                cell = {"num_oam": n_oam, "cell_attr": c_attr, "oam_offset": oam_ptr}
                if has_br:
                    br = list(struct.unpack_from("<4h", data, c_off + 8))
                    cell["bounding_rect"] = br
                # OAM attrs: oam_ptr 相对 CellArrayHead
                oam_abs = cell_arr_abs + oam_ptr
                oams = []
                for k in range(n_oam):
                    a0, a1, a2 = struct.unpack_from("<3H", data, oam_abs + k * 6)
                    oams.append([a0, a1, a2])
                cell["oam_attrs"] = oams
                cells.append(cell)
            b["cellbank"] = {
                "num_cells": num_cells,
                "attr": attr,
                "has_bounding_rect": has_br,
                "mapping_mode": mapping,
                "cells": cells,
            }
        result["blocks"].append(b)
    return result


# ============================================================
# NANR
# ============================================================

def parse_nanr(data: bytes, hdr: dict) -> dict:
    blocks = walk_blocks(data, hdr["header_size"], hdr["num_blocks"])
    result = {"header": hdr, "blocks": []}
    for kind, off, sz in blocks:
        b = {"kind": kind, "offset": off, "size": sz}
        if kind == "KNBA":  # 'ABNK' LE
            n_seq = struct.unpack_from("<H", data, off + 8)[0]
            n_frames = struct.unpack_from("<H", data, off + 10)[0]
            seq_off = struct.unpack_from("<I", data, off + 12)[0]
            frm_off = struct.unpack_from("<I", data, off + 16)[0]
            con_off = struct.unpack_from("<I", data, off + 20)[0]
            seq_abs = off + 8 + seq_off
            frm_abs = off + 8 + frm_off
            sequences = []
            for i in range(n_seq):
                s_off = seq_abs + i * 16
                nf = struct.unpack_from("<H", data, s_off)[0]
                loop = struct.unpack_from("<H", data, s_off + 2)[0]
                atype = struct.unpack_from("<I", data, s_off + 4)[0]
                pmode = struct.unpack_from("<I", data, s_off + 8)[0]
                p_arr = struct.unpack_from("<I", data, s_off + 12)[0]
                sequences.append({
                    "num_frames": nf,
                    "loop_start": loop,
                    "anim_type": f"0x{atype:08X}",
                    "play_mode": pmode,
                    "frame_array_offset": p_arr,
                })
            b["animbank"] = {
                "num_sequences": n_seq,
                "total_frames": n_frames,
                "sequences": sequences,
                "sequence_offset": seq_off,
                "frame_offset": frm_off,
                "contents_offset": con_off,
            }
        result["blocks"].append(b)
    return result


# ============================================================
# 主流程
# ============================================================

PARSERS = {
    "NCLR": parse_nclr,
    "NCGR": parse_ncgr,
    "NCER": parse_ncer,
    "NANR": parse_nanr,
}


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not IN_DIR.is_dir():
        print(f"ERROR: {IN_DIR} 不存在。先跑 export_nns_unpacked.py", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 第一遍：解析所有文件，按目录/stem 分组
    parsed_cache: dict[Path, dict] = {}  # src → parsed
    files_by_stem: dict[tuple[Path, str], dict[str, Path]] = {}  # (dir, stem) → {ext: path}

    all_files = sorted(IN_DIR.rglob("*"))
    for p in all_files:
        if not p.is_file():
            continue
        ext = p.suffix.lower().lstrip(".")
        if ext not in ("nanr", "ncer", "ncgr", "nclr"):
            continue
        data = p.read_bytes()
        hdr = parse_nns_header(data)
        magic = hdr["magic"]
        parsed = PARSERS[magic](data, hdr)
        parsed_cache[p] = parsed
        rel_dir = p.parent.relative_to(IN_DIR)
        stem = p.stem
        files_by_stem.setdefault((rel_dir, stem), {})[ext] = p

    # 第二遍：逐文件输出 JSON + 可视化 PNG
    index: list[dict] = []
    for p, parsed in parsed_cache.items():
        rel = p.relative_to(IN_DIR)
        out_json = OUT_DIR / rel.with_suffix(p.suffix + ".json")
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps(parsed, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        magic = parsed["header"]["magic"]
        render_info: dict = {}

        if magic == "NCLR":
            png = OUT_DIR / rel.with_name(f"{p.stem}_palette.png")
            render_nclr_png(parsed, png)
            render_info["palette_png"] = str(png.relative_to(OUT_DIR)).replace("\\", "/")

        if magic == "NCGR":
            # 找同目录同 stem 的 .nclr
            key = (p.parent.relative_to(IN_DIR), p.stem)
            grp = files_by_stem.get(key, {})
            nclr_path = grp.get("nclr")
            nclr_parsed = parsed_cache.get(nclr_path) if nclr_path else None
            png = OUT_DIR / rel.with_name(f"{p.stem}_tiles.png")
            data = p.read_bytes()
            info = render_ncgr_png(data, parsed, nclr_parsed, png)
            if info:
                render_info["tiles_png"] = str(png.relative_to(OUT_DIR)).replace("\\", "/")
                render_info.update(info)

        index.append({
            "path": str(rel).replace("\\", "/"),
            "magic": magic,
            "file_size": parsed["header"]["file_size"],
            "num_blocks": parsed["header"]["num_blocks"],
            "render": render_info,
        })

    # 总索引
    by_magic: dict[str, int] = {}
    for e in index:
        by_magic[e["magic"]] = by_magic.get(e["magic"], 0) + 1

    INDEX_JSON.write_text(
        json.dumps(
            {
                "total": len(index),
                "by_magic": by_magic,
                "files": sorted(index, key=lambda e: e["path"]),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"[export_nns_parsed] {len(index)} files parsed → {OUT_DIR}/  "
        f"({by_magic})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
