#!/usr/bin/env python3
"""
合成渲染 name/pass input UI 的 sprite cells（任务 C2）。

== 输入（A1 + A2 产物）==
  fs-decompressed/name_input/name_o_01.{nanr,ncer,ncgr,nclr}
  fs-decompressed/name_input/name_o_01_dup1.{ncgr,nclr}
  fs-decompressed/pass_input/pass_o_01.{nanr,ncer,ncgr,nclr}

== 任务范围 ==
用 NCGR (tiles) + NCLR (palette) + NCER (cell = 多 OAM 组合) 合成每个 cell 对应的
sprite 图像。BG 层依赖 .LZ5bg（任务 A3 未解），此处只渲染前景 sprite。

== 输出 ==
  graphics/images/fs-ui/<asset-name>_cell_NN.png   每个 cell 一张（合成后的 RGBA）
  graphics/images/fs-ui/<asset-name>_all_cells.png 所有 cell 拼成网格（概览）
  graphics/images/fs-ui/_cell_index.json           每个 cell 的 OAM 元数据

== NCER OAM 解码 ==
  attr0 bit 14-15 = shape (0 square, 1 wide, 2 tall)
  attr1 bit 14-15 = size
  shape+size → 像素 W×H:
    square: 8x8 / 16x16 / 32x32 / 64x64
    wide:   16x8 / 32x8 / 32x16 / 64x32
    tall:   8x16 / 8x32 / 16x32 / 32x64
  attr0 bit 13 = palette mode (0 = 16 色，1 = 256 色)
  attr2 bit 0-9  = char name（tile index, 对 4bpp 是 2-tile 对齐）
  attr2 bit 12-15 = palette number（4bpp 时选哪组 16 色）
  attr0 bit 8 = rot/scale 启用
  attr1 bit 12-13 = flip H/V（无 rot/scale 时）
  位置：attr0 bit 0-7 = Y (s8); attr1 bit 0-8 = X (s9)

用法:
    python tools/rom-export/export_fs_ui_name_pass.py
"""
from __future__ import annotations

import json
import os
import struct
import sys
import zlib
from pathlib import Path


IN_DIR = Path("fs-decompressed")
OUT_DIR = Path("graphics/images/fs-ui")

# (cell-asset-group, NCGR 文件, NCLR 文件, NCER 文件)
ASSETS = [
    ("name_o_01", "name_input/name_o_01.ncgr", "name_input/name_o_01.nclr", "name_input/name_o_01.ncer"),
    ("name_o_01_dup1", "name_input/name_o_01_dup1.ncgr", "name_input/name_o_01_dup1.nclr", "name_input/name_o_01.ncer"),
    ("pass_o_01", "pass_input/pass_o_01.ncgr", "pass_input/pass_o_01.nclr", "pass_input/pass_o_01.ncer"),
]

OBJ_SIZE = {
    0: {0: (8, 8), 1: (16, 16), 2: (32, 32), 3: (64, 64)},   # square
    1: {0: (16, 8), 1: (32, 8), 2: (32, 16), 3: (64, 32)},   # wide
    2: {0: (8, 16), 1: (8, 32), 2: (16, 32), 3: (32, 64)},   # tall
}


def _png_chunk(n: bytes, d: bytes) -> bytes:
    crc = zlib.crc32(n + d) & 0xFFFFFFFF
    return struct.pack(">I", len(d)) + n + d + struct.pack(">I", crc)


def save_png_rgba(path: Path, width: int, height: int, pixels: bytes) -> None:
    assert len(pixels) == width * height * 4
    raw = b"".join(
        b"\x00" + pixels[y * width * 4 : (y + 1) * width * 4]
        for y in range(height)
    )
    idat = zlib.compress(raw, 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # RGBA
    png = b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"IDAT", idat) + _png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


# ============================================================
# 复用 A2 parser（内嵌简化版）
# ============================================================

def parse_nns_header(data: bytes) -> dict:
    magic_raw = data[:4]
    bom = struct.unpack_from("<H", data, 4)[0]
    hdr_size = struct.unpack_from("<H", data, 12)[0]
    blocks = struct.unpack_from("<H", data, 14)[0]
    assert bom == 0xFEFF
    return {"magic_raw": magic_raw, "header_size": hdr_size, "num_blocks": blocks}


def walk_blocks(data: bytes, hdr_size: int, n_blocks: int):
    cursor = hdr_size
    for _ in range(n_blocks):
        kind = data[cursor : cursor + 4]
        size = struct.unpack_from("<I", data, cursor + 4)[0]
        yield kind, cursor, size
        cursor += size


def load_nclr_palette(data: bytes) -> tuple[str, list[tuple[int, int, int]]]:
    """返回 ('PLTT16'|'PLTT256', [(r,g,b), ...])。BGR5 → RGB888。"""
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind == b"TTLP":
            fmt = struct.unpack_from("<I", data, off + 8)[0]
            sz_byte = struct.unpack_from("<I", data, off + 16)[0]
            p_raw = struct.unpack_from("<I", data, off + 20)[0]
            raw_abs = off + 8 + p_raw
            palette = []
            for i in range(sz_byte // 2):
                u = struct.unpack_from("<H", data, raw_abs + i * 2)[0]
                r = (u & 0x1F) << 3
                g = ((u >> 5) & 0x1F) << 3
                b = ((u >> 10) & 0x1F) << 3
                palette.append((r | r >> 5, g | g >> 5, b | b >> 5))
            fmt_name = {3: "PLTT16", 4: "PLTT256"}.get(fmt, "unknown")
            return fmt_name, palette
    return "unknown", []


def load_ncgr_tiles(data: bytes) -> tuple[str, bytes]:
    """返回 (pixel_fmt, raw_pixels)。raw_pixels 每字节 1 像素（palette index）。"""
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind == b"RAHC":
            pxf = struct.unpack_from("<I", data, off + 12)[0]
            szb = struct.unpack_from("<I", data, off + 24)[0]
            p_raw = struct.unpack_from("<I", data, off + 28)[0]
            raw_abs = off + 8 + p_raw
            raw = data[raw_abs : raw_abs + szb]
            if pxf == 3:  # 4bpp
                px = bytearray(len(raw) * 2)
                for i, v in enumerate(raw):
                    px[i * 2] = v & 0xF
                    px[i * 2 + 1] = (v >> 4) & 0xF
                return "PLTT16", bytes(px)
            return "PLTT256", bytes(raw)
    return "unknown", b""


def load_ncer_cells(data: bytes) -> list[dict]:
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind == b"KBEC":
            num_cells = struct.unpack_from("<H", data, off + 8)[0]
            attr = struct.unpack_from("<H", data, off + 10)[0]
            cell_arr_off = struct.unpack_from("<I", data, off + 12)[0]
            has_br = bool(attr & 1)
            cell_arr_abs = off + 8 + cell_arr_off
            cell_size = 16 if has_br else 8
            cells = []
            for i in range(num_cells):
                c_off = cell_arr_abs + i * cell_size
                n_oam = struct.unpack_from("<H", data, c_off)[0]
                c_attr = struct.unpack_from("<H", data, c_off + 2)[0]
                oam_ptr = struct.unpack_from("<I", data, c_off + 4)[0]
                oam_abs = cell_arr_abs + oam_ptr
                oams = [struct.unpack_from("<3H", data, oam_abs + k * 6) for k in range(n_oam)]
                cells.append({"num_oam": n_oam, "cell_attr": c_attr, "oams": oams})
            return cells
    return []


# ============================================================
# Sprite 合成
# ============================================================

def sprite_dims(a0: int, a1: int) -> tuple[int, int]:
    shape = (a0 >> 14) & 3
    size = (a1 >> 14) & 3
    if shape not in OBJ_SIZE:
        return 8, 8
    return OBJ_SIZE[shape][size]


def render_cell_rgba(cell: dict, tiles_px: bytes, palette_rgb: list[tuple[int, int, int]],
                     pltt_mode_fmt: str) -> tuple[bytes, int, int, int, int]:
    """把一个 cell 的所有 OAM 渲染到最小包围矩形 RGBA 中。

    返回 (rgba_bytes, W, H, origin_x, origin_y)
    origin_x/y 是矩形左上角对应的 "cell 空间" 坐标（用于对齐）。
    """
    # 先收集每个 OAM 的 (abs_x, abs_y, w, h, sprite_data)
    sprites = []
    for a0, a1, a2 in cell["oams"]:
        y = a0 & 0xFF
        if y >= 128:
            y -= 256
        x = a1 & 0x1FF
        if x >= 256:
            x -= 512
        w, h = sprite_dims(a0, a1)
        pltt_mode = (a0 >> 13) & 1  # 0: 16 色, 1: 256 色
        char_name = a2 & 0x3FF
        pal_num = (a2 >> 12) & 0xF
        flip_h = (a1 >> 12) & 1
        flip_v = (a1 >> 13) & 1
        sprites.append((x, y, w, h, pltt_mode, char_name, pal_num, flip_h, flip_v))

    if not sprites:
        return b"", 0, 0, 0, 0

    min_x = min(s[0] for s in sprites)
    min_y = min(s[1] for s in sprites)
    max_x = max(s[0] + s[2] for s in sprites)
    max_y = max(s[1] + s[3] for s in sprites)
    W = max_x - min_x
    H = max_y - min_y
    if W <= 0 or H <= 0:
        return b"", 0, 0, 0, 0

    canvas = bytearray(W * H * 4)  # RGBA all 0 (transparent)

    # Tile size: 4bpp = 32 bytes/tile (8*8*4/8), 8bpp = 64 bytes/tile
    # But our tiles_px is unpacked (1 byte/pixel = 64 bytes/tile regardless)
    tile_px_bytes = 64  # 8×8 pixels, unpacked

    for (sx, sy, sw, sh, pm, char, pn, fh, fv) in sprites:
        # 4bpp 的 char_name 单位是 "2-tile block"（0x20 字节），8bpp 单位是 1 tile（0x40 字节）
        # 但 NitroSystem 1D mapping 下常量解释就是 "从 idx*tile_bytes 开始"
        # 4bpp 模式: 每个 char name = 0x20 字节 in ROM → 1 tile (8x8) in unpacked pixels
        # 8bpp 模式: 每个 char name = 0x40 字节 → 1 tile in unpacked pixels
        # 实际：4bpp 时 char_name 乘 2 (因为 4bpp 里 'char' 单位是 32 字节, 1 tile 是 32 字节 raw)
        #       但 NCGR 的 mappingType=1D_* 往往 char_name 已是 tile 下标
        # 以最简单假设: char_name = tile index（已是 unpacked 空间）
        tiles_wide = sw // 8
        tiles_tall = sh // 8
        for tile_row in range(tiles_tall):
            for tile_col in range(tiles_wide):
                tidx = char + tile_row * tiles_wide + tile_col
                toff = tidx * tile_px_bytes
                if toff + tile_px_bytes > len(tiles_px):
                    continue
                # 绘制此 tile 到 canvas
                for yy in range(8):
                    for xx in range(8):
                        pxv = tiles_px[toff + yy * 8 + xx]
                        # flip
                        out_x = tile_col * 8 + (7 - xx if fh else xx)
                        out_y = tile_row * 8 + (7 - yy if fv else yy)
                        # 调色板选择
                        if pm == 0:  # 4bpp
                            col_idx = pn * 16 + pxv
                        else:
                            col_idx = pxv
                        # 透明：palette index 0 (PLTT16 & PLTT256 通用约定)
                        if pxv == 0:
                            continue
                        if col_idx >= len(palette_rgb):
                            continue
                        r, g, b = palette_rgb[col_idx]
                        dst_x = sx - min_x + out_x
                        dst_y = sy - min_y + out_y
                        if 0 <= dst_x < W and 0 <= dst_y < H:
                            p = (dst_y * W + dst_x) * 4
                            canvas[p] = r
                            canvas[p + 1] = g
                            canvas[p + 2] = b
                            canvas[p + 3] = 255
    return bytes(canvas), W, H, min_x, min_y


def render_grid(sprites: list[tuple[str, bytes, int, int]], per_row: int, pad: int = 4) -> tuple[bytes, int, int]:
    """把多个 (label, rgba, W, H) 拼成网格 RGBA。label 当前只用于统计，不绘制文字。"""
    if not sprites:
        return b"", 0, 0
    max_w = max(s[2] for s in sprites) + pad * 2
    max_h = max(s[3] for s in sprites) + pad * 2
    rows = (len(sprites) + per_row - 1) // per_row
    W = per_row * max_w
    H = rows * max_h
    grid = bytearray(W * H * 4)
    # 浅灰底便于观察
    for i in range(0, W * H * 4, 4):
        grid[i] = 32
        grid[i + 1] = 32
        grid[i + 2] = 40
        grid[i + 3] = 255
    for i, (_, rgba, w, h) in enumerate(sprites):
        cx = (i % per_row) * max_w + pad + (max_w - 2 * pad - w) // 2
        cy = (i // per_row) * max_h + pad + (max_h - 2 * pad - h) // 2
        for yy in range(h):
            for xx in range(w):
                src = (yy * w + xx) * 4
                if rgba[src + 3] == 0:
                    continue
                dst = ((cy + yy) * W + (cx + xx)) * 4
                grid[dst] = rgba[src]
                grid[dst + 1] = rgba[src + 1]
                grid[dst + 2] = rgba[src + 2]
                grid[dst + 3] = 255
    return bytes(grid), W, H


def main() -> int:
    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not IN_DIR.is_dir():
        print(f"ERROR: {IN_DIR} 不存在（先跑 export_nns_unpacked.py）", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_out: list[dict] = []

    for asset_name, ncgr_rel, nclr_rel, ncer_rel in ASSETS:
        ncgr_p = IN_DIR / ncgr_rel
        nclr_p = IN_DIR / nclr_rel
        ncer_p = IN_DIR / ncer_rel
        if not all(p.exists() for p in (ncgr_p, nclr_p, ncer_p)):
            print(f"  SKIP {asset_name}: 缺少 NNS 文件", file=sys.stderr)
            continue

        fmt, palette = load_nclr_palette(nclr_p.read_bytes())
        pxfmt, tiles_px = load_ncgr_tiles(ncgr_p.read_bytes())
        cells = load_ncer_cells(ncer_p.read_bytes())

        cell_images: list[tuple[str, bytes, int, int]] = []
        per_cell_meta = []
        for i, cell in enumerate(cells):
            rgba, W, H, ox, oy = render_cell_rgba(cell, tiles_px, palette, pxfmt)
            if W == 0 or H == 0:
                per_cell_meta.append({"cell": i, "empty": True, "num_oam": cell["num_oam"]})
                continue
            out = OUT_DIR / f"{asset_name}_cell_{i:02d}.png"
            save_png_rgba(out, W, H, rgba)
            cell_images.append((f"c{i}", rgba, W, H))
            per_cell_meta.append({
                "cell": i,
                "png": str(out.relative_to(OUT_DIR)).replace("\\", "/"),
                "num_oam": cell["num_oam"],
                "WxH": [W, H],
                "origin": [ox, oy],
            })

        # grid overview
        if cell_images:
            grid_rgba, GW, GH = render_grid(cell_images, per_row=8)
            grid_out = OUT_DIR / f"{asset_name}_all_cells.png"
            save_png_rgba(grid_out, GW, GH, grid_rgba)
            grid_rel = str(grid_out.relative_to(OUT_DIR)).replace("\\", "/")
        else:
            grid_rel = None

        index_out.append({
            "asset": asset_name,
            "ncgr": ncgr_rel,
            "nclr": nclr_rel,
            "ncer": ncer_rel,
            "palette_fmt": fmt,
            "tile_fmt": pxfmt,
            "num_cells": len(cells),
            "grid_png": grid_rel,
            "cells": per_cell_meta,
        })
        print(f"  [{asset_name}] {len(cells)} cells, palette={fmt}, tiles={pxfmt}, "
              f"{len(cell_images)} rendered")

    (OUT_DIR / "_cell_index.json").write_text(
        json.dumps(index_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[export_fs_ui_name_pass] {len(index_out)} assets → {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
