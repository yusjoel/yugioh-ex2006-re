"""
渲染 empty idx 的人工确认 PNG, 每 10 个一组:
  Row 1: 编号 01..10
  Row 2: 字库 glyph (放大)
  Row 3: csv pattern-matched 候选字符 (top-1)
  Row 4 (额外): idx 编号 + vote 分布
"""
import json
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

candidates = json.loads(open('tools/jp-decode/empty_candidates.json', encoding='utf-8').read())
ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000  # main_large
W, H = 12, 12

# Find a Japanese font
import os
font_paths = [
    'C:/Windows/Fonts/msgothic.ttc',
    'C:/Windows/Fonts/YuGothM.ttc',
    'C:/Windows/Fonts/meiryo.ttc',
    'C:/Windows/Fonts/YuGothicUI-Regular.ttf',
]
font_path = next((p for p in font_paths if os.path.exists(p)), None)
print(f'Using font: {font_path}')
font_lg = ImageFont.truetype(font_path, 56)
font_md = ImageFont.truetype(font_path, 28)
font_sm = ImageFont.truetype(font_path, 16)

CELL_W = 120
CELL_H = 290  # 4 rows
SCALE = 7  # 12*7 = 84

OUT = Path('tools/jp-decode/review')
OUT.mkdir(parents=True, exist_ok=True)

# Group every 10
for batch_idx in range(0, len(candidates), 10):
    batch = candidates[batch_idx:batch_idx+10]
    n = len(batch)
    img = Image.new('RGB', (CELL_W*n + 20, CELL_H), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    for i, ent in enumerate(batch):
        x0 = i*CELL_W + 10
        # cell border
        draw.rectangle([x0, 5, x0+CELL_W-2, CELL_H-5], outline=(180,180,200), width=1)
        # Row 1: label 01..10
        label = f'{i+1:02d}'
        draw.text((x0 + (CELL_W - draw.textlength(label, font=font_md))//2, 10),
                  label, fill=(60, 60, 200), font=font_md)
        # Row 2: glyph
        gx0 = x0 + (CELL_W - W*SCALE)//2
        gy0 = 50
        # white box
        draw.rectangle([gx0-2, gy0-2, gx0+W*SCALE+1, gy0+H*SCALE+1], fill=(255,255,255), outline=(150,150,150))
        idx = ent['idx']
        off = BASE + idx*W*H
        for y in range(H):
            for x in range(W):
                if ROM[off + y*W + x]:
                    for dy in range(SCALE):
                        for dx in range(SCALE):
                            img.putpixel((gx0+x*SCALE+dx, gy0+y*SCALE+dy), (0,0,0))
        # Row 3: csv candidate top1
        cand = ent['top1']
        cw = draw.textlength(cand, font=font_lg)
        draw.text((x0 + (CELL_W - cw)//2, 150), cand, fill=(150,30,30), font=font_lg)
        # Row 4: idx + votes
        info = f'idx={idx}'
        votes_str = ' '.join(f'{c}({n})' for c, n in ent['all'][:2])
        draw.text((x0 + 5, 230), info, fill=(80,80,80), font=font_sm)
        draw.text((x0 + 5, 252), votes_str[:14], fill=(80,80,80), font=font_sm)
    
    p = OUT / f'group_{batch_idx//10 + 1:02d}.png'
    img.save(p)
    print(f'wrote {p}  ({n} cells)')

# Also generate index/answer template JSON
answers = [{'group': i//10 + 1, 'pos': (i%10) + 1, 'idx': c['idx'],
            'glyph_csv_match_top1': c['top1'], 'all_votes': c['all'],
            'user_confirmed': None} for i, c in enumerate(candidates)]
with open(OUT / 'answers_template.json', 'w', encoding='utf-8') as f:
    json.dump(answers, f, ensure_ascii=False, indent=2)
print(f'\nAnswers template: {OUT / "answers_template.json"}')
print(f'Review {len(candidates)} idx in {(len(candidates)+9)//10} groups')
