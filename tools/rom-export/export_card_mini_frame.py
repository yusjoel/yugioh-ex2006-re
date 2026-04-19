#!/usr/bin/env python3
"""
导出 card-mini-frame（带卡框的小卡图，含竖版 portrait + 横版 landscape 两态）的
tile bin、调色板 bin、PNG 预览，并生成结构化汇编 .s。

== tile 数据 ==
- 基址：ROM 0x01326280
- stride：1152 B = 18 tile × 64 B，= 3×3 portrait(576B) + 3×3 landscape(576B)
- 8bpp GBA tile，portrait 24×24，landscape 24×24，两态竖向拼成 24×48
- 2331 tile_block；索引表 0x015B5C00（与大卡图共用）
  公式：tile_block = u16[0x015B5C00 + (card_id*2 + flag)*2]
- 加载函数 FUN_080c33bc @ asm/all.s L231102 → OBJ VRAM 0x06010000

== 调色板（两套，用于不同屏幕）==
(A) OBJ 调色板（card list selection 屏用，4 段拼成完整 256 色）
    pal_128  @ ROM 0x01E31554, 32B  → PALRAM OBJ colors 128-143
    pal_144  @ ROM 0x01E31574, 32B  → PALRAM OBJ colors 144-159
    pal_gap  @ ROM 0x01E31594, 128B → 其他 UI 调色板
    pal_main @ ROM 0x01E31614, 256B → PALRAM OBJ colors 0-127（主）
    由 card_list_screen_init (FUN_080fdef4 → FUN_081011c4) 4 次 memcpy 静态加载。
    边框色（索引 128）已在 pal_128 预置 16 种变体，无运行时替换。

(B) BG 调色板（deck list 屏用，BG2 8bpp 渲染）
    bg_main  @ ROM 0x00510460, 256B → PALRAM BG colors 16-143（32B × 8 sub-pal）
    colors 0-15 永远为 0（透明）。ROM 该 256B 物理位于 pack_banner_palette
    (0x510440..0x510640) 中段，由 pack-banners 模块的 .incbin 覆盖，本脚本
    不单独生成 .s 文件，仅作为 PNG 渲染源。

== 产出 ==
  graphics/bin/card-mini-frame/tiles/tb{N:04d}.bin    2331 × 1152 B
  graphics/bin/card-mini-frame/palettes/pal_128.bin   32 B   OBJ 128-143
  graphics/bin/card-mini-frame/palettes/pal_144.bin   32 B   OBJ 144-159
  graphics/bin/card-mini-frame/palettes/pal_gap.bin   128 B  UI gap
  graphics/bin/card-mini-frame/palettes/pal_main.bin  256 B  OBJ 0-127
  graphics/images/card-mini-frame/card_{cid:04d}[_ocg|_tcg].png  BG 版本 RGBA 24×48
  data/card-mini-frame.s          incbin 引用 tile bin（card_mini_frame_tile_data:）
  data/card-mini-frame-palette.s  incbin 引用 OBJ palette bin（四段）

用法:
    python tools/rom-export/export_card_mini_frame.py
    python tools/rom-export/export_card_mini_frame.py --no-png
    python tools/rom-export/export_card_mini_frame.py --only 1  # 仅 card_id=1
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

from PIL import Image

ROM_PATH = Path("roms/2343.gba")

# tile 数据
TILE_BASE_ROM   = 0x01326280
TILE_STRIDE     = 1152                              # 18 tile × 64 B
NUM_TILE_BLOCKS = 2331                              # tile_block 0..2330
TILE_END_ROM    = TILE_BASE_ROM + NUM_TILE_BLOCKS * TILE_STRIDE  # 0x15B5C00

INDEX_TABLE_ROM  = 0x015B5C00
NUM_CARDS        = 2098   # 索引表物理 2099 条（0..2098），但 cid 2098 是占位（tb 与 1870/1887 重复），实际 2098 张卡：cid 0..2097

TILE_COLS = 3
TILE_ROWS = 6
TILE_SIZE = 64   # 8bpp 8×8

# OBJ 调色板四段（card list selection 屏）
PAL_SEGMENTS = [
    ("pal_128",  0x01E31554, 0x20,
     "OBJ colors 128-143（15 个卡类型边框色 + 1 空）"),
    ("pal_144",  0x01E31574, 0x20,
     "OBJ colors 144-159"),
    ("pal_gap",  0x01E31594, 0x80,
     "其他 UI 调色板数据（0x09e31594 等引用）"),
    ("pal_main", 0x01E31614, 0x100,
     "OBJ colors 0-127（主调色板）"),
]
PAL_ROM_START = 0x01E31554
PAL_ROM_END   = 0x01E31714   # 0x1C0 B 合计

# BG 调色板（deck list 屏，pack_banner_palette 中段 256B）
BG_PAL_ROM     = 0x00510460
BG_PAL_SIZE    = 0x100       # 256B = 128 colors → BG colors 16-143

# 输出路径（新版目录约定：bin/<模块>/{tiles,palettes} + images/<模块>/）
TILE_DIR     = Path("graphics/bin/card-mini-frame/tiles")
PAL_DIR      = Path("graphics/bin/card-mini-frame/palettes")
IMAGES_DIR   = Path("graphics/images/card-mini-frame")

TILE_S_PATH  = Path("data/card-mini-frame.s")
PAL_S_PATH   = Path("data/card-mini-frame-palette.s")


def bgr555_to_rgb(v: int) -> tuple[int, int, int]:
    r = (v & 0x1F) << 3
    g = ((v >> 5) & 0x1F) << 3
    b = ((v >> 10) & 0x1F) << 3
    return r, g, b


def assemble_bg_palette(rom: bytes) -> list[tuple[int, int, int]]:
    """组装 BG 256 色调色板（deck list 屏 BG2 8bpp）。

    colors[0..15]    ← 全零（透明）
    colors[16..143]  ← bg_main (ROM 0x00510460, 256B)
    colors[144..255] ← 全零
    """
    pal = [(0, 0, 0)] * 256
    for i in range(128):
        v = struct.unpack_from("<H", rom, BG_PAL_ROM + i * 2)[0]
        pal[16 + i] = bgr555_to_rgb(v)
    return pal


def render_tile_block(
    rom: bytes,
    tile_block: int,
    palette: list[tuple[int, int, int]],
) -> Image.Image:
    """渲染 tile_block 为 24×48 RGBA 图（palette 索引 0 视为透明）。"""
    off = TILE_BASE_ROM + tile_block * TILE_STRIDE
    block = rom[off:off + TILE_STRIDE]
    w = TILE_COLS * 8
    h = TILE_ROWS * 8
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for ti in range(TILE_COLS * TILE_ROWS):
        tile = block[ti * TILE_SIZE:(ti + 1) * TILE_SIZE]
        tx = ti % TILE_COLS
        ty = ti // TILE_COLS
        for py in range(8):
            for pxo in range(8):
                idx = tile[py * 8 + pxo]
                if idx == 0:
                    continue
                r, g, b = palette[idx]
                px[tx * 8 + pxo, ty * 8 + py] = (r, g, b, 255)
    return img


def get_tile_block(rom: bytes, card_id: int, flag: int) -> int | None:
    """从索引表读取 tile_block；越界或 0xFFFF 返回 None。"""
    idx_off = INDEX_TABLE_ROM + (card_id * 2 + flag) * 2
    tb = struct.unpack_from("<H", rom, idx_off)[0]
    if tb == 0xFFFF or tb >= NUM_TILE_BLOCKS:
        return None
    return tb


def dump_blobs(rom: bytes) -> None:
    """导出 tile bin + OBJ palette bin，生成两个 .s 文件。

    BG palette 不单独导出——其 ROM 物理位置已由 pack_banner_palette 覆盖。
    """
    TILE_DIR.mkdir(parents=True, exist_ok=True)
    PAL_DIR.mkdir(parents=True, exist_ok=True)

    # tile bins
    for tb in range(NUM_TILE_BLOCKS):
        off = TILE_BASE_ROM + tb * TILE_STRIDE
        (TILE_DIR / f"tb{tb:04d}.bin").write_bytes(rom[off:off + TILE_STRIDE])

    # OBJ palette bins
    for label, rom_off, size, _ in PAL_SEGMENTS:
        (PAL_DIR / f"{label}.bin").write_bytes(rom[rom_off:rom_off + size])

    # data/card-mini-frame.s
    tile_lines = [
        "@ card-mini-frame tile 数据（由 tools/rom-export/export_card_mini_frame.py 生成）",
        f"@ ROM 范围: 0x{TILE_BASE_ROM:X} - 0x{TILE_END_ROM:X}"
        f"  ({NUM_TILE_BLOCKS} × {TILE_STRIDE} B = {NUM_TILE_BLOCKS * TILE_STRIDE} B)",
        "@ 格式：8bpp GBA tile，每 1152B 块 = 上半 576B portrait (24×24) + 下半 576B landscape (24×24)",
        "@ 载入函数 FUN_080c33bc：0x09326280（上半）/ 0x093264C0（下半，+0x240）→ OBJ VRAM 0x06010000",
        "",
        "card_mini_frame_tile_data:",
    ]
    for tb in range(NUM_TILE_BLOCKS):
        tile_lines.append(f'    .incbin "graphics/bin/card-mini-frame/tiles/tb{tb:04d}.bin"')
    TILE_S_PATH.write_text("\n".join(tile_lines) + "\n", encoding="utf-8")

    # data/card-mini-frame-palette.s (OBJ palette only)
    pal_lines = [
        "@ card-mini-frame OBJ 调色板（由 tools/rom-export/export_card_mini_frame.py 生成）",
        f"@ ROM 范围: 0x{PAL_ROM_START:X} - 0x{PAL_ROM_END:X}"
        f"  (0x{PAL_ROM_END - PAL_ROM_START:X} = {PAL_ROM_END - PAL_ROM_START} 字节)",
        "@ 由 card_list_screen_init (FUN_080fdef4 → FUN_081011c4) 4 次 memcpy 加载：",
        "@   card_mini_frame_pal_128  → PALRAM 0x05000140 (BG colors 160-175) + 0x05000300 (OBJ 128-143)",
        "@   card_mini_frame_pal_144  → PALRAM 0x05000320 (OBJ colors 144-159)",
        "@   card_mini_frame_pal_main → PALRAM 0x05000200 (OBJ colors 0-127)",
        "@ 注：deck list 屏使用 BG 调色板 (ROM 0x00510460, 256B)，",
        "@     位于 pack_banner_palette 中段，由 pack-banners 模块覆盖。",
        "",
    ]
    for label, _, size, comment in PAL_SEGMENTS:
        pal_lines.append(f"card_mini_frame_{label}:")
        pal_lines.append(
            f'    .incbin "graphics/bin/card-mini-frame/palettes/{label}.bin"'
            f"  @ {comment}"
        )
        pal_lines.append("")
    PAL_S_PATH.write_text("\n".join(pal_lines) + "\n", encoding="utf-8")

    total_tile = NUM_TILE_BLOCKS * TILE_STRIDE
    total_pal = sum(s for _, _, s, _ in PAL_SEGMENTS)
    print(f"tile bins:    {TILE_DIR}/  ({NUM_TILE_BLOCKS} × {TILE_STRIDE} B = {total_tile:,} B)")
    print(f"OBJ pal bins: {PAL_DIR}/  (4 段, {total_pal} B 合计)")
    print(f"生成: {TILE_S_PATH}")
    print(f"生成: {PAL_S_PATH}")


def dump_png(rom: bytes, only_card_id: int | None) -> None:
    """按 card_id 导出 BG 版本 PNG（deck list 屏调色板）。

    命名（与 export_card_images.py 一致）：
      - OCG == TCG tile_block：card_{cid:04d}.png
      - 分开：card_{cid:04d}_ocg.png + card_{cid:04d}_tcg.png
    """
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    bg_pal = assemble_bg_palette(rom)
    cache: dict[int, Image.Image] = {}

    def save(cid: int, tb: int, suffix: str) -> int:
        if tb not in cache:
            cache[tb] = render_tile_block(rom, tb, bg_pal)
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
            if tb0 is not None:
                count += save(cid, tb0, "_ocg")
            if tb1 is not None:
                count += save(cid, tb1, "_tcg")

        if count % 500 == 0 and count > 0:
            print(f"  进度 {count}...")

    print(f"PNG: {count} 张 → {IMAGES_DIR}/")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="导出 card-mini-frame tile bin + palette bin + PNG + .s"
    )
    parser.add_argument("--only", type=int, default=None, metavar="CARD_ID",
                        help="仅导出指定 card_id（调试）")
    parser.add_argument("--no-png", action="store_true",
                        help="跳过 PNG 导出，仅生成 bin + .s")
    parser.add_argument("--no-blobs", action="store_true",
                        help="跳过 bin + .s 生成，仅导出 PNG")
    args = parser.parse_args()

    script = os.path.dirname(os.path.abspath(__file__))
    proj = os.path.dirname(os.path.dirname(script))
    os.chdir(proj)

    if not ROM_PATH.exists():
        print(f"ERROR: ROM 不存在: {ROM_PATH}", file=sys.stderr)
        return 1

    rom = ROM_PATH.read_bytes()

    if not args.no_blobs:
        print("=== 导出 ROM 原始数据块 + .s 文件 ===")
        dump_blobs(rom)
        print()

    if not args.no_png:
        print("=== 导出 PNG 预览（BG 版本）===")
        dump_png(rom, args.only)
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
