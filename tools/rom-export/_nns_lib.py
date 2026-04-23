#!/usr/bin/env python3
"""
NNS 通用加载 / 渲染库（供 export_fs_ui_*.py 等复用）。

提供：
  - parse_nns_header / walk_blocks
  - load_nclr_palette / load_ncgr_tiles / load_ncer_cells / load_nanr_sequences
  - render_cell_rgba / render_grid
  - save_png_rgba

NNS 布局细节见 doc/temp/nns-format-notes.md。
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path


OBJ_SIZE = {
    0: {0: (8, 8), 1: (16, 16), 2: (32, 32), 3: (64, 64)},   # square
    1: {0: (16, 8), 1: (32, 8), 2: (32, 16), 3: (64, 32)},   # wide
    2: {0: (8, 16), 1: (8, 32), 2: (16, 32), 3: (32, 64)},   # tall
}


# ============================================================
# PNG 写入
# ============================================================

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
# NNS 头解析
# ============================================================

def parse_nns_header(data: bytes) -> dict:
    bom = struct.unpack_from("<H", data, 4)[0]
    assert bom == 0xFEFF, f"BOM != FEFF: 0x{bom:04X}"
    return {
        "magic_raw": data[:4],
        "header_size": struct.unpack_from("<H", data, 12)[0],
        "num_blocks": struct.unpack_from("<H", data, 14)[0],
    }


def walk_blocks(data: bytes, hdr_size: int, n_blocks: int):
    cursor = hdr_size
    for _ in range(n_blocks):
        kind = data[cursor : cursor + 4]
        size = struct.unpack_from("<I", data, cursor + 4)[0]
        yield kind, cursor, size
        cursor += size


# ============================================================
# NCLR
# ============================================================

def load_nclr_palette(data: bytes) -> tuple[str, list[tuple[int, int, int]]]:
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind != b"TTLP":
            continue
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
        return {3: "PLTT16", 4: "PLTT256"}.get(fmt, "unknown"), palette
    return "unknown", []


# ============================================================
# NCGR
# ============================================================

def load_ncgr_tiles(data: bytes) -> tuple[str, bytes]:
    """返回 (pixel_fmt, pixels) — pixels 每字节 1 像素（palette index）。"""
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind != b"RAHC":
            continue
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


# ============================================================
# NCER
# ============================================================

def load_ncer_cells(data: bytes) -> list[dict]:
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind != b"KBEC":
            continue
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
# NANR
# ============================================================

def load_nanr_sequences(data: bytes) -> list[dict]:
    """解析 NANR，仅支持 element_type=INDEX (0) 的最简 frame content。

    返回 [{num_frames, loop_start, play_mode, anim_type, frames: [cellIdx, ...]}, ...]
    """
    hdr = parse_nns_header(data)
    for kind, off, _ in walk_blocks(data, hdr["header_size"], hdr["num_blocks"]):
        if kind != b"KNBA":
            continue
        n_seq = struct.unpack_from("<H", data, off + 8)[0]
        # n_total_frames = struct.unpack_from("<H", data, off + 10)[0]
        seq_off = struct.unpack_from("<I", data, off + 12)[0]
        # frm_off, con_off 也有但我们按 sequence 内嵌指针解
        seq_abs = off + 8 + seq_off
        sequences = []
        for i in range(n_seq):
            s_off = seq_abs + i * 16
            nf = struct.unpack_from("<H", data, s_off)[0]
            loop = struct.unpack_from("<H", data, s_off + 2)[0]
            atype = struct.unpack_from("<I", data, s_off + 4)[0]
            pmode = struct.unpack_from("<I", data, s_off + 8)[0]
            p_arr = struct.unpack_from("<I", data, s_off + 12)[0]
            # frame array 相对 sequence struct 起点
            frame_arr_abs = s_off + p_arr
            # element type = atype 的低 8 位；0 = INDEX, 1 = INDEX_SRT, 2 = INDEX_T
            elem_type = atype & 0xFF
            frames = []
            for k in range(nf):
                # 每 NNSG2dAnimFrameData = 8 B: pContent (u32 offset) + frames (u16) + pad (u16)
                f_off = frame_arr_abs + k * 8
                p_content = struct.unpack_from("<I", data, f_off)[0]
                fr_dur = struct.unpack_from("<H", data, f_off + 4)[0]
                content_abs = f_off + p_content  # 相对 frame struct 自身
                if elem_type == 0:  # INDEX
                    cell_idx = struct.unpack_from("<H", data, content_abs)[0]
                    frames.append({"cell": cell_idx, "duration": fr_dur})
                elif elem_type == 2:  # INDEX_T
                    cell_idx = struct.unpack_from("<H", data, content_abs)[0]
                    px = struct.unpack_from("<h", data, content_abs + 4)[0]
                    py = struct.unpack_from("<h", data, content_abs + 6)[0]
                    frames.append({"cell": cell_idx, "duration": fr_dur, "tx": px, "ty": py})
                elif elem_type == 1:  # INDEX_SRT (16 B)
                    cell_idx = struct.unpack_from("<H", data, content_abs)[0]
                    rot = struct.unpack_from("<H", data, content_abs + 2)[0]
                    sx = struct.unpack_from("<i", data, content_abs + 4)[0]
                    sy = struct.unpack_from("<i", data, content_abs + 8)[0]
                    px = struct.unpack_from("<h", data, content_abs + 12)[0]
                    py = struct.unpack_from("<h", data, content_abs + 14)[0]
                    frames.append({
                        "cell": cell_idx, "duration": fr_dur,
                        "rot": rot, "sx_fx32": sx, "sy_fx32": sy, "tx": px, "ty": py,
                    })
                else:
                    frames.append({"cell": -1, "duration": fr_dur, "unknown_type": elem_type})
            sequences.append({
                "num_frames": nf,
                "loop_start": loop,
                "anim_type": f"0x{atype:08X}",
                "element_type": elem_type,
                "play_mode": pmode,
                "frames": frames,
            })
        return sequences
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


def render_cell_rgba(cell: dict, tiles_px: bytes,
                     palette_rgb: list[tuple[int, int, int]],
                     extra_offset: tuple[int, int] = (0, 0)) -> tuple[bytes, int, int, int, int]:
    """把一个 cell 的所有 OAM 渲染到最小包围矩形 RGBA 中。

    extra_offset: 额外叠加到每个 sprite 的 (dx, dy)（如 NANR 的 translate）。

    返回 (rgba_bytes, W, H, origin_x, origin_y)
    """
    if not cell["oams"]:
        return b"", 0, 0, 0, 0

    dx, dy = extra_offset
    sprites = []
    for a0, a1, a2 in cell["oams"]:
        y = a0 & 0xFF
        if y >= 128:
            y -= 256
        x = a1 & 0x1FF
        if x >= 256:
            x -= 512
        w, h = sprite_dims(a0, a1)
        pltt_mode = (a0 >> 13) & 1
        char_name = a2 & 0x3FF
        pal_num = (a2 >> 12) & 0xF
        flip_h = (a1 >> 12) & 1
        flip_v = (a1 >> 13) & 1
        sprites.append((x + dx, y + dy, w, h, pltt_mode, char_name, pal_num, flip_h, flip_v))

    min_x = min(s[0] for s in sprites)
    min_y = min(s[1] for s in sprites)
    max_x = max(s[0] + s[2] for s in sprites)
    max_y = max(s[1] + s[3] for s in sprites)
    W = max_x - min_x
    H = max_y - min_y
    if W <= 0 or H <= 0:
        return b"", 0, 0, 0, 0

    canvas = bytearray(W * H * 4)
    tile_px_bytes = 64  # 8×8 pixels unpacked

    for (sx, sy, sw, sh, pm, char, pn, fh, fv) in sprites:
        tiles_wide = sw // 8
        tiles_tall = sh // 8
        for tile_row in range(tiles_tall):
            for tile_col in range(tiles_wide):
                tidx = char + tile_row * tiles_wide + tile_col
                toff = tidx * tile_px_bytes
                if toff + tile_px_bytes > len(tiles_px):
                    continue
                for yy in range(8):
                    for xx in range(8):
                        pxv = tiles_px[toff + yy * 8 + xx]
                        if pxv == 0:
                            continue
                        out_x = tile_col * 8 + (7 - xx if fh else xx)
                        out_y = tile_row * 8 + (7 - yy if fv else yy)
                        if pm == 0:  # 4bpp: palette group
                            col_idx = pn * 16 + pxv
                        else:
                            col_idx = pxv
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


def render_grid(items: list[tuple[str, bytes, int, int]], per_row: int = 8,
                pad: int = 4, bg_rgba=(32, 32, 40, 255)) -> tuple[bytes, int, int]:
    """把多个 (label, rgba, W, H) 拼成网格 RGBA。"""
    if not items:
        return b"", 0, 0
    max_w = max(s[2] for s in items) + pad * 2
    max_h = max(s[3] for s in items) + pad * 2
    rows = (len(items) + per_row - 1) // per_row
    W = per_row * max_w
    H = rows * max_h
    grid = bytearray(W * H * 4)
    for i in range(0, W * H * 4, 4):
        grid[i] = bg_rgba[0]
        grid[i + 1] = bg_rgba[1]
        grid[i + 2] = bg_rgba[2]
        grid[i + 3] = bg_rgba[3]
    for i, (_, rgba, w, h) in enumerate(items):
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
