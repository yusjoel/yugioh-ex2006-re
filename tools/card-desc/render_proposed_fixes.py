"""
渲染 16 个 paddle OCR 误识别 idx 的高清 glyph + 提议修正字符,
让用户视觉确认。
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 24  # 24x = 288×288 高清

# (idx, current_wrong_char, proposed_correct_char, hint)
PROPOSED = [
    (405,  '自', '温', '温 = 氵 + 日 + 皿'),
    (474,  '車', '軟', '軟 = 車 + 欠'),
    (526,  '元', '頑', '頑 = 元 + 頁'),
    (828,  'オ', '才', '才 (汉字, 不是片假名)'),
    (1034, '8', '晶', '晶 = 三个口字'),
    (1258, '馬', '駄', '駄 = 馬 + 太'),
    (1324, '中', '忠', '忠 = 中 + 心'),
    (1361, '不', '爪', '爪 (claw)'),
    (1405, '女', '奴', '奴 = 女 + 又'),
    (1475, '内', '納', '納 = 糸 + 内'),
    (1534, '波', '彼', '彼 = 彳 + 皮'),
    (1606, '開', '閃', '閃 = 門 + 人'),
    (1657, '骨', '冒', '冒 = 冂 + 二 + 目'),
    (1801, '立', '率', '率'),
    (1805, '刀', '習', '習 = 羽 + 白'),
    (1863, '石', '話', '話 = 言 + 舌'),
]

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_big = ImageFont.truetype(font_path, 48)
font_md = ImageFont.truetype(font_path, 24)
font_sm = ImageFont.truetype(font_path, 18)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


CELL_W = 460
CELL_H = 380
COLS = 4
rows = (len(PROPOSED) + COLS - 1) // COLS

img_w = CELL_W * COLS + 40
img_h = CELL_H * rows + 90
img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
draw = ImageDraw.Draw(img)

draw.text((20, 12), 'Codetable 16 处 OCR 误识别 — 提议修正',
          fill=(40, 40, 80), font=font_md)
draw.text((20, 44), '左: ROM 实际 glyph (24x).  右上: 当前错误标注 (红).  右下: 提议修正 (绿).',
          fill=(80, 80, 100), font=font_sm)

for i, (idx, wrong, correct, hint) in enumerate(PROPOSED):
    row = i // COLS
    col = i % COLS
    x0 = 20 + col * CELL_W
    y0 = 75 + row * CELL_H

    draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)

    # idx label
    draw.text((x0 + 14, y0 + 8), f'idx={idx}', fill=(60, 60, 200), font=font_md)

    # left: glyph
    glyph_box = W * SCALE
    gx0 = x0 + 14
    gy0 = y0 + 50
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(140, 140, 140))
    draw_glyph(img, idx, gx0, gy0)

    # right: comparison
    rx0 = gx0 + glyph_box + 30
    # current wrong
    draw.text((rx0, gy0 + 8), '当前 (错):', fill=(180, 60, 30), font=font_sm)
    draw.text((rx0, gy0 + 30), wrong, fill=(180, 60, 30), font=font_big)
    # proposed correct
    draw.text((rx0, gy0 + 110), '提议 (修正):', fill=(40, 130, 40), font=font_sm)
    draw.text((rx0, gy0 + 132), correct, fill=(40, 130, 40), font=font_big)
    # hint
    draw.text((rx0, gy0 + 215), hint, fill=(60, 60, 60), font=font_sm)

OUT = Path('tools/card-desc/proposed_fixes.png')
img.save(OUT)
print(f'wrote {OUT}')
