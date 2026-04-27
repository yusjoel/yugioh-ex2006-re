"""
渲染 idx 120..305 字库网格, 标注推断字符 + 已确认字符,
让用户确认 あ行 + ァ + ヴ-α 段规律.
"""
import json
from PIL import Image, ImageDraw, ImageFont
ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12

# Inferred mapping (根据 50 音规律)
inferred = {
    124: ('ぁ', 'inf 小a'),
    125: ('あ', 'inf 大a'),
    126: ('ぃ', 'inf 小i'),
    127: ('い', '✓'),
    128: ('ぅ', 'inf 小u'),
    129: ('う', '✓'),
    130: ('ぇ', 'inf 小e'),
    131: ('え', 'inf 大e'),
    132: ('ぉ', 'inf 小o'),
    133: ('お', 'inf 大o'),
    207: ('ァ', 'inf 小a-kata'),
    290: ('ヴ', '✓'),
    291: ('?',  '?'),
    292: ('α',  '✓'),
}

# Add seed already-known
import sys
sys.path.insert(0, 'tools/jp-decode')
from seed_codetable import build_seed_by_idx
seed = build_seed_by_idx()

font = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 28)
font_sm = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 14)

# Range 120..305: 186 idx
COLS = 10
SCALE = 6
CELL_W = W*SCALE + 14
CELL_H = H*SCALE + 56  # glyph + label + char

def render_range(lo, hi, fname):
    n = hi - lo + 1
    rows = (n + COLS - 1) // COLS
    img = Image.new('RGB', (COLS*CELL_W + 12, rows*CELL_H + 8), (250,250,250))
    draw = ImageDraw.Draw(img)
    for i in range(n):
        idx = lo + i
        x0 = (i % COLS)*CELL_W + 5
        y0 = (i // COLS)*CELL_H + 5
        # idx label
        draw.text((x0+2, y0), f'{idx}', fill=(80,80,80), font=font_sm)
        # glyph
        gx = x0 + 7
        gy = y0 + 18
        draw.rectangle([gx-1, gy-1, gx+W*SCALE, gy+H*SCALE], fill=(255,255,255), outline=(180,180,200))
        for y in range(H):
            for x in range(W):
                if ROM[BASE + idx*W*H + y*W + x]:
                    for dy in range(SCALE):
                        for dx in range(SCALE):
                            img.putpixel((gx+x*SCALE+dx, gy+y*SCALE+dy), (0,0,0))
        # char
        if idx in seed:
            ch = seed[idx]; color = (30, 100, 30); tag = 'seed'
        elif idx in inferred:
            ch, tag = inferred[idx]
            color = (180, 30, 30) if '✓' in tag else (60, 60, 180)
        else:
            ch, tag = '', ''
            color = (200,200,200)
        if ch:
            cw = draw.textlength(ch, font=font)
            draw.text((x0 + (CELL_W-cw)//2, y0 + 14 + H*SCALE + 2), ch, fill=color, font=font)
    img.save(fname)
    print(f'{fname}: {img.size}')

render_range(120, 145, 'tools/jp-decode/review/A_row.png')      # あ行
render_range(200, 215, 'tools/jp-decode/review/kata_start.png') # ん→ァ→ア
render_range(285, 305, 'tools/jp-decode/review/n_to_alpha.png') # ン→ヴ→?→α
