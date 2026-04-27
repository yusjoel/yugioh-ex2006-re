"""
渲染 codetable 全部 44 处重复 char, 每对显示两 idx glyph 让我看清.
按 hit 频率分高低 (高频通常正确, 低频是 OCR 错).
"""
import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from PIL import Image, ImageDraw, ImageFont


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
                result.append(int(s[i + 1:j], 8))
                i = j
            elif nxt == 'n': result.append(0x0A); i += 2
            elif nxt == '"': result.append(0x22); i += 2
            elif nxt == '\\': result.append(0x5C); i += 2
            else: i += 2
        else:
            result.append(ord(c))
            i += 1
    return bytes(result)


# 算 _xx 中每个 idx 的实际 hit 数
src = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|ja|en|de|fr|it|es):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
idx_hits = Counter()
for m in pat.finditer(src):
    if m.group(2) not in ('xx', 'ja'):
        continue
    bs = decode_octal_string(m.group(3))
    payload = bs.rstrip(b'\x00')
    i = 0
    while i + 1 < len(payload):
        hi, lo = payload[i], payload[i + 1]
        if hi >= 0xF0:
            idx = ((hi & 0xF) << 7) | (lo & 0x7F)
            idx_hits[idx] += 1
        i += 2

# Codetable
ct = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}

# 找全 codetable 重复
char_idxs = defaultdict(list)
for idx, ch in ct.items():
    if ch:
        char_idxs[ch].append(idx)
duplicates = {ch: idxs for ch, idxs in char_idxs.items() if len(idxs) > 1}

# 排序: 每对按 hit 数降序
DUP_PAIRS = []
for ch, idxs in sorted(duplicates.items()):
    sorted_idxs = sorted(idxs, key=lambda i: -idx_hits.get(i, 0))
    DUP_PAIRS.append((ch, sorted_idxs))

print(f'Total duplicate chars: {len(DUP_PAIRS)}')
total_extra_idxs = sum(len(idxs) - 1 for _, idxs in DUP_PAIRS)
print(f'Total LOW-freq idxs needing fix: {total_extra_idxs}')

# 渲染
ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 22

font_path = 'C:/Windows/Fonts/msgothic.ttc'
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


# Layout: 每行 1 对(主+副), 4 列 × N 行
PAIRS_PER_PAGE = 16
CELL_W = 620
CELL_H = 360
COLS = 3

n_pairs = len(DUP_PAIRS)
n_pages = (n_pairs + PAIRS_PER_PAGE - 1) // PAIRS_PER_PAGE

for page in range(n_pages):
    start = page * PAIRS_PER_PAGE
    end = min(start + PAIRS_PER_PAGE, n_pairs)
    batch = DUP_PAIRS[start:end]
    rows = (len(batch) + COLS - 1) // COLS
    img_w = CELL_W * COLS + 40
    img_h = CELL_H * rows + 80
    img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.text((20, 12), f'Codetable 重复 char 第 {page+1}/{n_pages} 页 — 全 codetable 共 {n_pairs} 对',
              fill=(40, 40, 80), font=font_md)
    draw.text((20, 44), '左 (绿) = 高频 idx (准, 不动). 右 (红) = 低频 idx (OCR 错? 待修)',
              fill=(80, 80, 100), font=font_sm)

    for i, (ch, idxs) in enumerate(batch):
        row = i // COLS
        col = i % COLS
        x0 = 20 + col * CELL_W
        y0 = 70 + row * CELL_H
        draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)
        draw.text((x0 + 14, y0 + 8), f'char = {ch!r}', fill=(60, 60, 200), font=font_md)

        # Glyph 1: high-freq (correct)
        idx_hi = idxs[0]
        gx0 = x0 + 20
        gy0 = y0 + 50
        glyph_box = W * SCALE
        draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                       fill=(255, 255, 255), outline=(40, 130, 40), width=2)
        draw_glyph(img, idx_hi, gx0, gy0)
        draw.text((gx0, gy0 + glyph_box + 6),
                  f'idx={idx_hi} ({idx_hits.get(idx_hi, 0)} hits)',
                  fill=(40, 130, 40), font=font_sm)

        # Glyph 2: low-freq (suspicious)
        idx_lo = idxs[1]
        gx0_2 = gx0 + glyph_box + 30
        draw.rectangle([gx0_2 - 2, gy0 - 2, gx0_2 + glyph_box + 1, gy0 + glyph_box + 1],
                       fill=(255, 255, 255), outline=(180, 60, 30), width=2)
        draw_glyph(img, idx_lo, gx0_2, gy0)
        draw.text((gx0_2, gy0 + glyph_box + 6),
                  f'idx={idx_lo} ({idx_hits.get(idx_lo, 0)} hits)',
                  fill=(180, 60, 30), font=font_sm)

        # Note 3rd idx if exists (e.g. 貝 has 3)
        if len(idxs) >= 3:
            extra = ', '.join(f'idx={i}({idx_hits.get(i, 0)})' for i in idxs[2:])
            draw.text((x0 + 14, y0 + CELL_H - 30),
                      f'还有 idx: {extra}', fill=(180, 60, 30), font=font_sm)

    out = Path(f'tools/card-desc/duplicates_page{page+1}.png')
    img.save(out)
    print(f'wrote {out}')
