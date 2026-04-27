"""
渲染最终 68 个 empty idx 的视觉审核 PNG。

每组 10 cell（最后一组 8 cell），每 cell 显示：
  - 位置编号 01..10 (蓝色, 顶部)
  - 字库 glyph 12×12 放大 12x = 144×144 像素
  - idx 编号
  - char_code (hi lo)
"""
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000  # main_large
W, H = 12, 12
SCALE = 12  # 12*12 = 144 像素 (高清)

# 68 个 empty idx (来自 codetable.json 的实际空缺)
final = {int(k): v for k, v in json.loads(open('tools/jp-decode/codetable.json', encoding='utf-8').read())['by_idx'].items()}
EMPTY_IDX = [i for i in range(1925) if not final.get(i)]
assert len(EMPTY_IDX) == 68, f'Expected 68 empty, got {len(EMPTY_IDX)}'

font_paths = [
    'C:/Windows/Fonts/msgothic.ttc',
    'C:/Windows/Fonts/YuGothM.ttc',
    'C:/Windows/Fonts/meiryo.ttc',
]
font_path = next((p for p in font_paths if os.path.exists(p)), None)
font_lg = ImageFont.truetype(font_path, 28)  # 位置编号
font_md = ImageFont.truetype(font_path, 22)  # idx 编号
font_sm = ImageFont.truetype(font_path, 18)  # char_code

CELL_W = 180
CELL_H = 280
PAD = 12

OUT = Path('tools/jp-decode/review')
OUT.mkdir(parents=True, exist_ok=True)


def idx_to_xx_code(idx):
    """idx → char_code: hi=0xF0|(idx>>7&0xF), lo=0x80|(idx&0x7F)"""
    hi = ((idx >> 7) & 0xF) | 0xF0
    lo = (idx & 0x7F) | 0x80
    return hi, lo


def draw_glyph(img, idx, gx0, gy0):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        img.putpixel((gx0 + x * SCALE + dx, gy0 + y * SCALE + dy), (0, 0, 0))


def render_group(group_idx, idxs):
    n = len(idxs)
    img_w = CELL_W * n + PAD * 2
    img_h = CELL_H + 60
    img = Image.new('RGB', (img_w, img_h), (250, 250, 250))
    draw = ImageDraw.Draw(img)

    # 标题
    title = f'final_empty group {group_idx:02d}  ({n} cells, idx range {idxs[0]}..{idxs[-1]})'
    draw.text((PAD, 8), title, fill=(40, 40, 80), font=font_md)

    for i, idx in enumerate(idxs):
        x0 = PAD + i * CELL_W
        y0 = 50
        # cell 边框
        draw.rectangle([x0 + 4, y0, x0 + CELL_W - 4, y0 + CELL_H - 10], outline=(180, 180, 200), width=1)
        # 位置编号
        label = f'{i + 1:02d}'
        lw = draw.textlength(label, font=font_lg)
        draw.text((x0 + (CELL_W - lw) // 2, y0 + 8), label, fill=(60, 60, 200), font=font_lg)
        # glyph
        glyph_box = W * SCALE  # 144
        gx0 = x0 + (CELL_W - glyph_box) // 2
        gy0 = y0 + 50
        draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                       fill=(255, 255, 255), outline=(140, 140, 140))
        draw_glyph(img, idx, gx0, gy0)
        # idx 编号
        info = f'idx={idx}'
        iw = draw.textlength(info, font=font_md)
        draw.text((x0 + (CELL_W - iw) // 2, gy0 + glyph_box + 8), info, fill=(80, 80, 80), font=font_md)
        # char_code
        hi, lo = idx_to_xx_code(idx)
        code_str = f'XX={hi:02X} {lo:02X}'
        cw = draw.textlength(code_str, font=font_sm)
        draw.text((x0 + (CELL_W - cw) // 2, gy0 + glyph_box + 36), code_str, fill=(120, 80, 30), font=font_sm)

    out_path = OUT / f'final_empty_{group_idx:02d}.png'
    img.save(out_path)
    print(f'wrote {out_path}  ({n} cells: idx {idxs[0]}..{idxs[-1]})')


# 按"自然分组"切分，每组 ≤10：
# ASCII 区前段 (1..20)             13 → 拆 7 + 6
# ASCII 区中段 (31..55)            14 → 拆 7 + 7
# ASCII 区末段 (99..122)            6
# 汉字 326..740                     7
# 汉字 806..922                     5
# 汉字 1056..1174                   6
# 汉字 1205..1578                   8
# 汉字 1742..1888                   9
groups = []
ascii_front = [i for i in EMPTY_IDX if i <= 20]      # 13 个
ascii_mid   = [i for i in EMPTY_IDX if 31 <= i <= 55]  # 14 个
ascii_late  = [i for i in EMPTY_IDX if 99 <= i <= 127]  # 6 个
kanji_a     = [i for i in EMPTY_IDX if 256 <= i <= 800]   # 7
kanji_b     = [i for i in EMPTY_IDX if 800 <= i <= 1000]  # 5
kanji_c     = [i for i in EMPTY_IDX if 1000 <= i <= 1200]  # 6
kanji_d     = [i for i in EMPTY_IDX if 1200 <= i <= 1700]  # 8
kanji_e     = [i for i in EMPTY_IDX if 1700 <= i <= 1925]  # 9

# 拆分超过 10 的组
def chunked(lst, size=10):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def chunk_to_seven(lst):
    """长度 13/14 切成 7+6 / 7+7"""
    if len(lst) <= 10:
        return [lst]
    half = (len(lst) + 1) // 2
    return [lst[:half], lst[half:]]


groups.extend(chunk_to_seven(ascii_front))
groups.extend(chunk_to_seven(ascii_mid))
groups.append(ascii_late)
groups.append(kanji_a)
groups.append(kanji_b)
groups.append(kanji_c)
groups.append(kanji_d)
groups.append(kanji_e)

# 渲染 + 写 answer template
all_meta = []
for g_i, g in enumerate(groups, start=1):
    render_group(g_i, g)
    for pos, idx in enumerate(g, start=1):
        hi, lo = idx_to_xx_code(idx)
        all_meta.append({
            'group': g_i,
            'pos': pos,
            'idx': idx,
            'char_code_hi': f'0x{hi:02X}',
            'char_code_lo': f'0x{lo:02X}',
            'user_confirmed': None,
        })

with open(OUT / 'final_empty_template.json', 'w', encoding='utf-8') as f:
    json.dump(all_meta, f, ensure_ascii=False, indent=2)

total = sum(len(g) for g in groups)
print(f'\nTotal {total} idx across {len(groups)} groups')
print(f'Template: {OUT / "final_empty_template.json"}')
