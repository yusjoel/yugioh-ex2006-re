#!/usr/bin/env python3
"""
导出 card-medium-frame（32×48 带框卡 sprite）tile bin + BG 版本 PNG + data/.s。

== tile 数据 ==
- 基址：ROM 0x00FBC080
- stride：1536 B = 24 tile × 64 B，8bpp tile，4×6 行主布局 = 32×48 像素
- 2331 tile_block（0..2330）；与 card-mini-frame 共享索引表 0x015B5C00
  公式：`tile_block = u16[0x015B5C00 + (card_id*2 + flag)*2]`
- 加载函数 `FUN_080c2d24` @ asm/all.s L230236：stride ×1536 计算
  `tb*3, <<9 = tb*1536`；读索引表 + flag 选 OCG/TCG 同 card-mini-frame 模式
- 用途：OBJ VRAM 0x06010000（第一路径）+ BG VRAM 0x06006340 / 0x06008020
  （FUN_080cb7xx / FUN_080db910，具体屏幕待 runtime 验证，推测对战场大 sprite）

== 调色板 ==
渲染用 card-mini-frame 的 BG 调色板（ROM 0x00510460, 256 B → colors 16-143），
colors 0-15 透明。实际屏幕用哪套调色板需 runtime 抓 PALRAM 确认。

== 产出 ==
  graphics/bin/card-medium-frame/tiles/tb{N:04d}.bin   2331 × 1536 B
  graphics/images/card-medium-frame/card_{cid:04d}[_ocg|_tcg].png  BG 版本 RGBA 32×48
  data/card-medium-frame.s   incbin 引用 tile bin（card_medium_frame_tile_data:）

用法:
    python tools/rom-export/export_card_medium_frame.py
    python tools/rom-export/export_card_medium_frame.py --no-png
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

from PIL import Image

ROM_PATH = Path("roms/2343.gba")

TILE_BASE_ROM   = 0x00FBC080
TILE_STRIDE     = 1536          # 24 tile × 64 B
NUM_TILE_BLOCKS = 2331
TILE_END_ROM    = TILE_BASE_ROM + NUM_TILE_BLOCKS * TILE_STRIDE  # 0x01326280

INDEX_TABLE_ROM = 0x015B5C00
NUM_CARDS       = 2098          # cid 0..2097（sentinel cid 2098 跳过，与 mini-frame 一致）

TILE_COLS = 4
TILE_ROWS = 6
TILE_SIZE = 64

# BG 调色板（与 card-mini-frame 共用）
BG_PAL_ROM  = 0x00510460
BG_PAL_SIZE = 0x100

TILE_DIR    = Path("graphics/bin/card-medium-frame/tiles")
IMAGES_DIR  = Path("graphics/images/card-medium-frame")
TILE_S_PATH = Path("data/card-medium-frame.s")


def bgr555_to_rgb(v: int) -> tuple[int, int, int]:
    r = (v & 0x1F) << 3
    g = ((v >> 5) & 0x1F) << 3
    b = ((v >> 10) & 0x1F) << 3
    return r, g, b


def assemble_bg_palette(rom: bytes) -> list[tuple[int, int, int]]:
    pal = [(0, 0, 0)] * 256
    for i in range(128):
        v = struct.unpack_from("<H", rom, BG_PAL_ROM + i * 2)[0]
        pal[16 + i] = bgr555_to_rgb(v)
    return pal


def render_tile_block(rom: bytes, tile_block: int, palette):
    off = TILE_BASE_ROM + tile_block * TILE_STRIDE
    block = rom[off:off + TILE_STRIDE]
    w, h = TILE_COLS * 8, TILE_ROWS * 8
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for ti in range(TILE_COLS * TILE_ROWS):
        tile = block[ti * TILE_SIZE:(ti + 1) * TILE_SIZE]
        tx, ty = ti % TILE_COLS, ti // TILE_COLS
        for py in range(8):
            for pxo in range(8):
                idx = tile[py * 8 + pxo]
                if idx == 0:
                    continue
                r, g, b = palette[idx]
                px[tx * 8 + pxo, ty * 8 + py] = (r, g, b, 255)
    return img


def get_tile_block(rom: bytes, card_id: int, flag: int) -> int | None:
    off = INDEX_TABLE_ROM + (card_id * 2 + flag) * 2
    tb = struct.unpack_from("<H", rom, off)[0]
    if tb == 0xFFFF or tb >= NUM_TILE_BLOCKS:
        return None
    return tb


def dump_blobs(rom: bytes) -> None:
    TILE_DIR.mkdir(parents=True, exist_ok=True)
    TILE_S_PATH.parent.mkdir(parents=True, exist_ok=True)

    for tb in range(NUM_TILE_BLOCKS):
        off = TILE_BASE_ROM + tb * TILE_STRIDE
        (TILE_DIR / f"tb{tb:04d}.bin").write_bytes(rom[off:off + TILE_STRIDE])

    lines = [
        "@ card-medium-frame tile 数据（由 tools/rom-export/export_card_medium_frame.py 生成）",
        f"@ ROM 范围: 0x{TILE_BASE_ROM:X} - 0x{TILE_END_ROM:X}"
        f"  ({NUM_TILE_BLOCKS} × {TILE_STRIDE} B = {NUM_TILE_BLOCKS * TILE_STRIDE} B)",
        "@ 格式：8bpp GBA tile，4×6 tile 行主 = 32×48 像素，24 tile × 64 B/card",
        "@ 加载函数 FUN_080c2d24 @ asm/all.s L230236；索引表 0x095B5C00 与 card-mini-frame 共享",
        "@ 目标 VRAM：OBJ 0x06010000（FUN_080c2d24）+ BG 0x06006340 (FUN_080cb7xx)",
        "",
        "card_medium_frame_tile_data:",
    ]
    for tb in range(NUM_TILE_BLOCKS):
        lines.append(f'    .incbin "graphics/bin/card-medium-frame/tiles/tb{tb:04d}.bin"')
    TILE_S_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"tile bins: {TILE_DIR}/  ({NUM_TILE_BLOCKS} × {TILE_STRIDE} B = "
          f"{NUM_TILE_BLOCKS * TILE_STRIDE:,} B)")
    print(f"生成: {TILE_S_PATH}")


def dump_png(rom: bytes, only_card_id: int | None) -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    pal = assemble_bg_palette(rom)
    cache: dict[int, Image.Image] = {}

    def save(cid: int, tb: int, suffix: str) -> int:
        if tb not in cache:
            cache[tb] = render_tile_block(rom, tb, pal)
        cache[tb].save(IMAGES_DIR / f"card_{cid:04d}{suffix}.png", optimize=True)
        return 1

    count = 0
    for cid in range(NUM_CARDS):
        if only_card_id is not None and cid != only_card_id:
            continue
        tb0 = get_tile_block(rom, cid, 0)
        tb1 = get_tile_block(rom, cid, 1)
        if tb0 is None and tb1 is None:
            continue
        if tb0 == tb1 and tb0 is not None:
            count += save(cid, tb0, "")
        else:
            if tb0 is not None: count += save(cid, tb0, "_ocg")
            if tb1 is not None: count += save(cid, tb1, "_tcg")
        if count % 500 == 0 and count > 0:
            print(f"  进度 {count}...")
    print(f"PNG: {count} 张 → {IMAGES_DIR}/")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, default=None)
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--no-blobs", action="store_true")
    args = ap.parse_args()

    script = Path(__file__).resolve()
    proj = script.parent.parent.parent
    os.chdir(proj)

    if not ROM_PATH.exists():
        print(f"ERROR: {ROM_PATH}", file=sys.stderr)
        return 1
    rom = ROM_PATH.read_bytes()

    if not args.no_blobs:
        print("=== 导出 tile bin + .s ===")
        dump_blobs(rom)
        print()
    if not args.no_png:
        print("=== 导出 BG 版本 PNG ===")
        dump_png(rom, args.only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
