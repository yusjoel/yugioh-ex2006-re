#!/usr/bin/env python3
"""
批量导出卡牌列表小图（OBJ 小卡图）为 PNG。

== 数据结构（2026-04-15 调查结果）==

- **tile 基址**：ROM `0x01326280`（**非** `card-data-structure.md` §三 旧文档所述
  的 `0x01000000`，该区实为 UI/其他资产，3.3 MB）
- **stride**：1152 B（**非** 2240）
- **格式**：8bpp GBA tile（64 B/tile），3×6 tile 布局 = **24×48 像素**
- **索引表**：`0x015B5C00`（与大卡图共用），`tile_block = u16[base+(card_id*2+flag)*2]`
- **目标**：OBJ VRAM `0x06010000`（sprite，非 BG）
- **加载函数**：`FUN_080c33bc` @ `asm/all.s` L231102（两个基址
  `0x09326280` 上半 576 B + `0x093264c0` 下半 576 B，各 9 个 8bpp tile）

== 调色板（P2-3 遗留）==

未定位。本脚本默认输出**灰度 PNG**。若 `--palette` 提供自定义 palette bin
（512 B = 256 × BGR555），则使用该 palette 着色。
"""

import os
import sys
import struct
import argparse
from PIL import Image

ROM_PATH = 'roms/2343.gba'
OUT_DIR = 'graphics/card-images-list'

TILE_BASE = 0x01326280
TILE_STRIDE = 1152
INDEX_TABLE = 0x015B5C00
MAX_TILE_BLOCK = 2331  # 与大卡图相同

TILE_COLS = 3
TILE_ROWS = 6
TILE_SIZE = 64  # 8bpp, 8×8


def load_palette_bgr555(pal_bytes):
    """BGR555 → 256 × RGB888 list."""
    pal = []
    for i in range(256):
        raw = struct.unpack_from('<H', pal_bytes, i * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        pal.append((r, g, b))
    return pal


def decode_entry_to_image(rom, tile_block, palette=None):
    """渲染 tile_block 对应的小卡图为 RGBA（如有调色板）或 P 模式灰度 PNG。"""
    off = TILE_BASE + tile_block * TILE_STRIDE
    block = rom[off:off + TILE_STRIDE]

    w = TILE_COLS * 8
    h = TILE_ROWS * 8

    if palette is not None:
        # 调色板模式：index 0 作透明
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
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
    else:
        # 灰度
        img = Image.new('P', (w, h))
        gray = []
        for i in range(256):
            gray.extend([i, i, i])
        img.putpalette(gray)
        for ti in range(TILE_COLS * TILE_ROWS):
            tile = block[ti * TILE_SIZE:(ti + 1) * TILE_SIZE]
            tx = ti % TILE_COLS
            ty = ti // TILE_COLS
            for py in range(8):
                for pxo in range(8):
                    img.putpixel((tx * 8 + pxo, ty * 8 + py), tile[py * 8 + pxo])
        return img


def iter_card_ids(rom, flag=1):
    """枚举 (card_id, tile_block)。flag=1 对应 BY6E（TCG 非日版）。"""
    for card_id in range(MAX_TILE_BLOCK + 1):
        idx_off = INDEX_TABLE + (card_id * 2 + flag) * 2
        tb = struct.unpack_from('<H', rom, idx_off)[0]
        if tb == 0xFFFF:
            continue
        if tb > MAX_TILE_BLOCK:
            continue
        yield card_id, tb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--palette', help='可选：256 色 BGR555 调色板 bin 文件（512 B）')
    ap.add_argument('--flag', type=int, default=1, help='0=日版，1=BY6E 非日版（默认）')
    ap.add_argument('--only', type=int, help='仅导出此 card_id（调试）')
    ap.add_argument('--out', default=OUT_DIR)
    args = ap.parse_args()

    script = os.path.dirname(os.path.abspath(__file__))
    proj = os.path.dirname(os.path.dirname(script))
    os.chdir(proj)

    rom = open(ROM_PATH, 'rb').read()
    palette = None
    if args.palette:
        pal_bytes = open(args.palette, 'rb').read()
        if len(pal_bytes) < 512:
            print(f'警告：调色板文件仅 {len(pal_bytes)} 字节，需 512 B', file=sys.stderr)
            pal_bytes = pal_bytes.ljust(512, b'\x00')
        palette = load_palette_bgr555(pal_bytes[:512])
        print(f'使用调色板：{args.palette}')
    else:
        print('无调色板 → 灰度输出')

    os.makedirs(args.out, exist_ok=True)

    seen_tb = set()
    count = 0
    for card_id, tb in iter_card_ids(rom, args.flag):
        if args.only is not None and card_id != args.only:
            continue
        if tb in seen_tb:
            continue  # 多 card_id 共享同 tile_block，只导一次
        seen_tb.add(tb)

        img = decode_entry_to_image(rom, tb, palette)
        fname = f'card_{card_id:04d}_tb{tb:04d}.png'
        img.save(os.path.join(args.out, fname))
        count += 1

    print(f'完成：{count} 张 PNG → {args.out}/')


if __name__ == '__main__':
    main()
