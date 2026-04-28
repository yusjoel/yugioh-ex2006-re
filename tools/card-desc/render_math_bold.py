"""
渲染 Math Bold 的 7 个占位 idx (修法 A 中, 因全角已被占用 → 用 𝐀-𝐳 / 𝟎-𝟗 唯一替代).
每行: 当前 idx glyph + 已占的全角 idx glyph + Math Bold 替代符号, 让用户对比是否真同形.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 22

# (idx, paddle_orig_half, math_bold_now, occupied_full_idx, occupied_full_ch, hint)
ITEMS = [
    (8,    '1', '𝟏', 63, '１', "paddle 标 '1' (半角); idx 63 已占 '１' (全角)"),
    (40,   '8', '𝟖', 70, '８', "paddle 标 '8' (半角); idx 70 已占 '８' (全角)"),
    (52,   'A', '𝐀', 72, 'Ａ', "paddle 标 'A' (半角); idx 72 已占 'Ａ' (全角)"),
    (620,  'R', '𝐑', 89, 'Ｒ', "paddle 标 'R' (半角); idx 89 已占 'Ｒ' (全角)"),
    (876,  '2', '𝟐', 64, '２', "paddle 标 '2' (半角); idx 64 已占 '２' (全角)"),
    (1465, 'G', '𝐆', 78, 'Ｇ', "paddle 标 'G' (半角); idx 78 已占 'Ｇ' (全角)"),
    (1832, 'T', '𝐓', 91, 'Ｔ', "paddle 标 'T' (半角); idx 91 已占 'Ｔ' (全角)"),
]

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_md = ImageFont.truetype(font_path, 22)
font_sm = ImageFont.truetype(font_path, 16)
font_big = ImageFont.truetype(font_path, 32)
# Math Bold 需要支持 U+1D400+ 的字体 (msgothic 不一定有)
try:
    font_math = ImageFont.truetype('C:/Windows/Fonts/seguisym.ttf', 32)
except OSError:
    try:
        font_math = ImageFont.truetype('C:/Windows/Fonts/Cambria Math.ttf', 32)
    except OSError:
        font_math = font_big


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


# Layout: 每行 1 个 item, 列: 信息 | 当前 glyph | 全角 glyph | Math Bold 字符显示
ROW_H = 360
COLS_PER_ITEM = 3  # 当前 idx glyph, 占用全角 idx glyph, Math Bold 文字
GLYPH_BOX = W * SCALE  # 264
COL_W = GLYPH_BOX + 60
LEFT_INFO_W = 280

img_w = LEFT_INFO_W + COL_W * COLS_PER_ITEM + 40
img_h = ROW_H * len(ITEMS) + 80

img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
draw = ImageDraw.Draw(img)
draw.text((20, 14),
          'Math Bold 占位 7 处 — 修法 A 副产物 (全角已被其他 idx 占, 用 Math Bold 唯一替代避重)',
          fill=(40, 40, 80), font=font_md)
draw.text((20, 44),
          '左: 此处 idx 实际 glyph (字库). 中: 已占该全角的另一 idx glyph. 右: Math Bold 替代字.',
          fill=(80, 80, 100), font=font_sm)

for row, (idx, half, math_ch, occ_idx, occ_full, hint) in enumerate(ITEMS):
    y0 = 80 + row * ROW_H
    # Info 左侧
    draw.text((20, y0 + 30), f'idx {idx}', fill=(60, 60, 200), font=font_md)
    draw.text((20, y0 + 60), f'paddle 原标: {half!r}', fill=(120, 80, 30), font=font_sm)
    draw.text((20, y0 + 85), f'已占: idx {occ_idx} = {occ_full!r}', fill=(40, 130, 40), font=font_sm)
    draw.text((20, y0 + 110), f'当前码表: {math_ch}', fill=(180, 60, 30), font=font_sm)
    draw.text((20, y0 + 145), hint, fill=(60, 60, 60), font=font_sm)

    # 列 0: 当前 idx (此 idx) 的实际 glyph
    cx = LEFT_INFO_W + 20
    draw.rectangle([cx-2, y0+30-2, cx+GLYPH_BOX+1, y0+30+GLYPH_BOX+1],
                   fill=(255, 255, 255), outline=(180, 60, 30), width=2)
    draw_glyph(img, idx, cx, y0 + 30)
    draw.text((cx, y0 + 30 + GLYPH_BOX + 6),
              f'idx {idx} 字库 glyph',
              fill=(180, 60, 30), font=font_sm)

    # 列 1: 已占该全角的 idx glyph
    cx2 = cx + COL_W
    draw.rectangle([cx2-2, y0+30-2, cx2+GLYPH_BOX+1, y0+30+GLYPH_BOX+1],
                   fill=(255, 255, 255), outline=(40, 130, 40), width=2)
    draw_glyph(img, occ_idx, cx2, y0 + 30)
    draw.text((cx2, y0 + 30 + GLYPH_BOX + 6),
              f'idx {occ_idx} = {occ_full!r}',
              fill=(40, 130, 40), font=font_sm)

    # 列 2: Math Bold 字符显示 (用系统字体)
    cx3 = cx2 + COL_W
    draw.rectangle([cx3-2, y0+30-2, cx3+GLYPH_BOX+1, y0+30+GLYPH_BOX+1],
                   fill=(255, 250, 240), outline=(120, 80, 40), width=2)
    # 居中绘 Math Bold 字
    draw.text((cx3 + GLYPH_BOX//2 - 30, y0 + 30 + 80),
              math_ch, fill=(0, 0, 0), font=font_math)
    draw.text((cx3, y0 + 30 + GLYPH_BOX + 6),
              f'{math_ch} (Math Bold)',
              fill=(120, 80, 40), font=font_sm)

OUT = Path('tools/card-desc/math_bold_check.png')
img.save(OUT)
print(f'wrote {OUT}  ({img_w}x{img_h})')
