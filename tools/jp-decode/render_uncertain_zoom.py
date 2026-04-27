"""
对剩余 17 个不确定 idx 高倍渲染（24×=288×288），便于多模态再次视觉识别。
每图一个 cell，留大量空间。每行 4 个 cell。
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 24  # 288×288

UNCERTAIN = [
    9, 12, 16, 17,  # ASCII
    327, 851, 1174, 1281, 1304, 1342, 1510, 1578,
    1742, 1746, 1816, 1839, 1869,  # 汉字
]

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_lg = ImageFont.truetype(font_path, 32)
font_md = ImageFont.truetype(font_path, 24)


def draw_glyph(img, idx, gx0, gy0):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        img.putpixel((gx0 + x * SCALE + dx, gy0 + y * SCALE + dy), (0, 0, 0))


CELL_W = 320
CELL_H = 380
COLS = 4
rows = (len(UNCERTAIN) + COLS - 1) // COLS

img_w = CELL_W * COLS + 40
img_h = CELL_H * rows + 60
img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
draw = ImageDraw.Draw(img)

draw.text((20, 10), f'17 uncertain idx (no text context) — 24x zoom', fill=(40, 40, 80), font=font_md)

for i, idx in enumerate(UNCERTAIN):
    row = i // COLS
    col = i % COLS
    x0 = 20 + col * CELL_W
    y0 = 50 + row * CELL_H

    draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)
    # idx label
    label = f'idx={idx}'
    lw = draw.textlength(label, font=font_lg)
    draw.text((x0 + (CELL_W - lw) // 2, y0 + 10), label, fill=(60, 60, 200), font=font_lg)
    # glyph at 24x
    glyph_box = W * SCALE
    gx0 = x0 + (CELL_W - glyph_box) // 2
    gy0 = y0 + 60
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(140, 140, 140))
    draw_glyph(img, idx, gx0, gy0)

OUT = Path('tools/jp-decode/review/final_uncertain_24x.png')
img.save(OUT)
print(f'wrote {OUT}')
