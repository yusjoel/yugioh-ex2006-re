"""批次 1: 渲染 19 个最可疑 idx, 用户视觉确认实际 glyph"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 24

# (idx, current_char, proposed_correction, reason)
SUSPECTS = [
    (314, '报', '扱', 'atsukau, a-row'),
    (315, '鯰', '鮎', 'ayu, a-row (鮎=魚+占)'),
    (340, '音', '育', 'iku, i-row (亠+月)'),
    (364, '荣', '栄', '简体→shin-jitai'),
    (369, '銳', '鋭', 'kyū→shin-jitai'),
    (373, '閱', '閲', 'kyū→shin-jitai'),
    (385, '绿', '縁', 'en-row (糸+彖)'),
    (392, '橫', '横', 'kyū→shin-jitai'),
    (404, '因', '恩', 'on-row (因+心)'),
    (406, '音', '音', '不动; on-row 位置正确'),
    (422, '筒', '菓', 'ka-row (艸+果)'),
    (468, '冗', '殻', 'kara, ka-row'),
    (491, '喵', '噛', 'kamu, ka-row (口+歯)'),
    (500, '宽', '寛', '简体→kyū-jitai'),
    (682, '决', '決', '简体'),
    (797, '国', '国', '不动; 字形相同'),
    (1096, '凤', '鳳', '简体'),
    (1762, '动', '動', '简体'),
    (1228, '馬', '騒', 'sou (馬+蚤)'),
    (1328, '馬', '駐', 'chū (馬+主)'),
]

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_big = ImageFont.truetype(font_path, 40)
font_md = ImageFont.truetype(font_path, 22)
font_sm = ImageFont.truetype(font_path, 16)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


CELL_W = 480
CELL_H = 380
COLS = 4
rows = (len(SUSPECTS) + COLS - 1) // COLS

img_w = CELL_W * COLS + 40
img_h = CELL_H * rows + 90
img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
draw = ImageDraw.Draw(img)

draw.text((20, 12), 'Codetable 第 2 轮 — 20 个可疑 idx (18 修正 + 2 不动)',
          fill=(40, 40, 80), font=font_md)
draw.text((20, 44), '左: ROM 实际 glyph (24x).  右上红: 当前标注.  右下绿: 提议修正.',
          fill=(80, 80, 100), font=font_sm)

for i, (idx, cur, prop, reason) in enumerate(SUSPECTS):
    row = i // COLS
    col = i % COLS
    x0 = 20 + col * CELL_W
    y0 = 75 + row * CELL_H

    draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)
    draw.text((x0 + 14, y0 + 8), f'idx={idx}', fill=(60, 60, 200), font=font_md)

    glyph_box = W * SCALE
    gx0 = x0 + 14
    gy0 = y0 + 50
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(140, 140, 140))
    draw_glyph(img, idx, gx0, gy0)

    rx0 = gx0 + glyph_box + 30
    draw.text((rx0, gy0 + 8), '当前:', fill=(180, 60, 30), font=font_sm)
    draw.text((rx0, gy0 + 28), cur, fill=(180, 60, 30), font=font_big)
    same = (cur == prop)
    label = '不动:' if same else '提议:'
    color_prop = (100, 100, 100) if same else (40, 130, 40)
    draw.text((rx0, gy0 + 100), label, fill=color_prop, font=font_sm)
    draw.text((rx0, gy0 + 120), prop, fill=color_prop, font=font_big)
    # reason wrap to 2 lines if needed
    draw.text((x0 + 14, y0 + CELL_H - 50), reason[:35], fill=(60, 60, 60), font=font_sm)
    if len(reason) > 35:
        draw.text((x0 + 14, y0 + CELL_H - 30), reason[35:70], fill=(60, 60, 60), font=font_sm)

OUT = Path('tools/card-desc/batch1_fixes.png')
img.save(OUT)
print(f'wrote {OUT}')
