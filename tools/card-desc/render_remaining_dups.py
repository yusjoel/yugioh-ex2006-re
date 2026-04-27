"""渲染剩余 6 处 codetable 重复 char, 并附 _xx hits + 上下文用例"""
import json
import re
from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 20


def decode_octal_string(s):
    result = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt.isdigit():
                j = i + 1
                while j < len(s) and j < i + 4 and s[j].isdigit():
                    j += 1
                result.append(int(s[i + 1:j], 8)); i = j
            elif nxt == 'n': result.append(0x0A); i += 2
            elif nxt == '"': result.append(0x22); i += 2
            elif nxt == '\\': result.append(0x5C); i += 2
            else: i += 2
        else:
            result.append(ord(c)); i += 1
    return bytes(result)


CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


def code_to_idx(hi, lo):
    if hi >= 0xF0:
        return ((hi & 0xF) << 7) | (lo & 0x7F)
    return None


# 算 _xx hits + 上下文
TARGETS = [698, 1102, 1390, 1748, 1808, 1856, 621, 1444, 1424, 1904, 852, 858]
src = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|ja):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
hits = Counter()
contexts = {t: [] for t in TARGETS}
for m in pat.finditer(src):
    cid = int(m.group(1))
    bs = decode_octal_string(m.group(3))
    payload = bs.rstrip(b'\x00')
    seq = []
    i = 0
    while i + 1 < len(payload):
        idx = code_to_idx(payload[i], payload[i + 1])
        seq.append(idx)
        i += 2
    for pos, idx in enumerate(seq):
        if idx in TARGETS:
            hits[idx] += 1
            if len(contexts[idx]) < 2:
                lo = max(0, pos - 6); hi_e = min(len(seq), pos + 7)
                ctx = ''.join(
                    CT.get(i, '?') if i and i != idx else f'[?{idx}]'
                    for i in seq[lo:hi_e] if i is not None
                )
                contexts[idx].append(f'cid={cid}: ...{ctx}...')


# 6 对
PAIRS = [
    ('推', 698, 1102),
    ('田', 1390, 1748),
    ('竜', 1808, 1856),
    ('篤', 621, 1444),
    ('藤', 1424, 1904),
    ('錯', 852, 858),
]

font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_md = ImageFont.truetype(font_path, 22)
font_sm = ImageFont.truetype(font_path, 16)
font_big = ImageFont.truetype(font_path, 36)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


# Layout: 2 列 × 3 行, 每格显示 char + 两 idx glyph + hits + ctx
COLS = 2
ROWS = 3
CELL_W = 560
CELL_H = 340
img_w = CELL_W * COLS + 40
img_h = CELL_H * ROWS + 70
img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
draw = ImageDraw.Draw(img)
draw.text((20, 14), 'Codetable 剩余 6 处重复 — 字形变体 / defer 确认',
          fill=(40, 40, 80), font=font_md)
draw.text((20, 40), '左 (绿) = 高频 idx (准, 不动). 右 (橙) = 低频 idx. 下方为 _xx 上下文',
          fill=(80, 80, 100), font=font_sm)

for i, (ch, idx_a, idx_b) in enumerate(PAIRS):
    row = i // COLS
    col = i % COLS
    x0 = 20 + col * CELL_W
    y0 = 60 + row * CELL_H
    draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)

    # 排序: hit 多的在左 (绿)
    a_hits = hits.get(idx_a, 0)
    b_hits = hits.get(idx_b, 0)
    if a_hits < b_hits:
        idx_a, idx_b = idx_b, idx_a
        a_hits, b_hits = b_hits, a_hits

    draw.text((x0 + 14, y0 + 8), f'char = {ch!r}', fill=(60, 60, 200), font=font_md)

    glyph_box = W * SCALE  # 288
    gx0 = x0 + 20
    gy0 = y0 + 44
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(40, 130, 40), width=2)
    draw_glyph(img, idx_a, gx0, gy0)
    draw.text((gx0, gy0 + glyph_box + 4),
              f'idx={idx_a} ({a_hits} hits)', fill=(40, 130, 40), font=font_sm)

    gx0_2 = gx0 + glyph_box + 30
    draw.rectangle([gx0_2 - 2, gy0 - 2, gx0_2 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(200, 130, 30), width=2)
    draw_glyph(img, idx_b, gx0_2, gy0)
    draw.text((gx0_2, gy0 + glyph_box + 4),
              f'idx={idx_b} ({b_hits} hits)', fill=(200, 130, 30), font=font_sm)

    # 上下文 (低频 idx, 帮判定)
    y_ctx = gy0 + glyph_box + 28
    if contexts[idx_b]:
        for j, c in enumerate(contexts[idx_b][:2]):
            draw.text((x0 + 14, y_ctx + j * 20), c[:60], fill=(80, 80, 80), font=font_sm)
    else:
        draw.text((x0 + 14, y_ctx), f'idx={idx_b}: 0 hits in _xx', fill=(150, 100, 30), font=font_sm)

OUT = Path('tools/card-desc/remaining_dups.png')
img.save(OUT)
print(f'wrote {OUT}  ({img_w}x{img_h})')
print('\nhits:')
for ch, a, b in PAIRS:
    print(f"  '{ch}': idx={a}({hits.get(a,0)}) idx={b}({hits.get(b,0)})")
