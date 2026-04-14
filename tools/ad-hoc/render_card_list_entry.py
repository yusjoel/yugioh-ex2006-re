#!/usr/bin/env python3
"""
渲染 0x01326280 + idx*1152 处单 entry 为灰度 PNG，测试多种 tile 布局。
"""
import os, sys, struct
from PIL import Image

ROM_PATH = 'roms/2343.gba'
BASE = 0x01326280
STRIDE = 1152


def decode_8bpp_tile(data):
    """返回 8x8 = 64 个索引（行优先）。"""
    return list(data)  # 8bpp = 1 byte/pixel, 64 B per tile


def render_grid(rom_off, cols, rows, out_png):
    off = rom_off
    rom = open(ROM_PATH, 'rb').read()
    block = rom[off:off + cols * rows * 64]
    img = Image.new('P', (cols * 8, rows * 8))
    # 灰度调色板
    pal = []
    for i in range(256):
        pal.extend([i, i, i])
    img.putpalette(pal)

    for ti in range(cols * rows):
        tile = block[ti * 64:(ti + 1) * 64]
        tx = ti % cols
        ty = ti // cols
        for py in range(8):
            for px in range(8):
                img.putpixel((tx * 8 + px, ty * 8 + py), tile[py * 8 + px])
    img.save(out_png)


def render_grid_colmajor(rom_off, cols, rows, out_png):
    """列优先：tile 0 = col 0 row 0, tile 1 = col 0 row 1, ..."""
    off = rom_off
    rom = open(ROM_PATH, 'rb').read()
    block = rom[off:off + cols * rows * 64]
    img = Image.new('P', (cols * 8, rows * 8))
    pal = []
    for i in range(256):
        pal.extend([i, i, i])
    img.putpalette(pal)

    for ti in range(cols * rows):
        tile = block[ti * 64:(ti + 1) * 64]
        tx = ti // rows
        ty = ti % rows
        for py in range(8):
            for px in range(8):
                img.putpixel((tx * 8 + px, ty * 8 + py), tile[py * 8 + px])
    img.save(out_png)


def main():
    script = os.path.dirname(os.path.abspath(__file__))
    proj = os.path.dirname(os.path.dirname(script))
    os.chdir(proj)

    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    off = BASE + idx * STRIDE
    print(f'idx={idx} off=0x{off:08X} stride=0x{STRIDE:x}')

    # 18 tiles total
    # 试 3×6, 6×3, 2×9, 9×2 布局（row-major / column-major）
    out_dir = 'doc/temp'
    os.makedirs(out_dir, exist_ok=True)
    for cols, rows in [(3, 6), (6, 3), (2, 9), (9, 2), (4, 4), (4, 5)]:
        if cols * rows * 64 > STRIDE:
            continue
        render_grid(off, cols, rows, f'{out_dir}/card_list_{idx}_{cols}x{rows}_rm.png')
        render_grid_colmajor(off, cols, rows, f'{out_dir}/card_list_{idx}_{cols}x{rows}_cm.png')

    print(f'  渲染多种布局到 {out_dir}/card_list_{idx}_*.png')


if __name__ == '__main__':
    main()
