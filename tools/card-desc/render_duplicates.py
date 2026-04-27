"""渲染 16 个 duplicate-char idx 的实际 glyph, 验证哪个是 OCR 误识别"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000  # main_large
W, H = 12, 12
SCALE = 16

DUPLICATES = [
    # (char, idx_high_freq, idx_low_freq, hits_high, hits_low)
    ('石', 1151, 1863, 21, 1),
    ('中', 1321, 1324, 81, 2),
    ('自', 919, 405, 988, 2),
    ('オ', 216, 828, 74, 1),
    ('元', 708, 526, 63, 4),
    ('不', 1569, 1361, 12, 1),
    ('馬', 1483, 1258, 2, 1),
    ('波', 1480, 1534, 4, 2),
    ('女', 1014, 1405, 24, 2),
    ('骨', 803, 1657, 2, 1),
    ('開', 455, 1606, 14, 4),
    ('刀', 1410, 1805, 2, 1),
    ('8',  40,   1034, 1,  1),
    ('車', 940, 474, 5, 1),
    ('内', 1453, 1475, 10, 1),
    ('立', 1802, 1801, 4, 1),
]

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_big = ImageFont.truetype(font_path, 36)
font_md = ImageFont.truetype(font_path, 18)
font_sm = ImageFont.truetype(font_path, 14)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


CELL_W = 480
CELL_H = 280
COLS = 4
rows = (len(DUPLICATES) + COLS - 1) // COLS

img_w = CELL_W * COLS + 40
img_h = CELL_H * rows + 80
img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
draw = ImageDraw.Draw(img)

draw.text((20, 10), 'Codetable duplicate idx — 实际 glyph 对比 (左: 高频 idx, 右: 低频 idx)',
          fill=(40, 40, 80), font=font_md)
draw.text((20, 35), '"高频" 通常通过卡名 vote 确认 (准), "低频" 主要靠 PaddleOCR (常误)',
          fill=(80, 80, 100), font=font_sm)

for i, (ch, idx_high, idx_low, h_high, h_low) in enumerate(DUPLICATES):
    row = i // COLS
    col = i % COLS
    x0 = 20 + col * CELL_W
    y0 = 70 + row * CELL_H

    draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)
    draw.text((x0 + 10, y0 + 8), f'codetable[{idx_high}] = codetable[{idx_low}] = {ch!r}',
              fill=(60, 60, 200), font=font_md)

    # left: high-freq glyph
    glyph_box = W * SCALE
    gx0 = x0 + 30
    gy0 = y0 + 50
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(140, 140, 140))
    draw_glyph(img, idx_high, gx0, gy0)
    draw.text((gx0, gy0 + glyph_box + 10), f'idx={idx_high}', fill=(40, 100, 40), font=font_sm)
    draw.text((gx0, gy0 + glyph_box + 28), f'hits={h_high} (高频, 多卡名确认)', fill=(40, 100, 40), font=font_sm)

    # right: low-freq glyph
    gx0 = x0 + 240
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(140, 140, 140))
    draw_glyph(img, idx_low, gx0, gy0)
    draw.text((gx0, gy0 + glyph_box + 10), f'idx={idx_low}', fill=(180, 60, 30), font=font_sm)
    draw.text((gx0, gy0 + glyph_box + 28), f'hits={h_low} (低频, OCR 误识?)', fill=(180, 60, 30), font=font_sm)

OUT = Path('tools/card-desc/duplicates_compare.png')
img.save(OUT)
print(f'wrote {OUT}')
