"""
对所有 ROM/ygocdb 字符级差异生成审核 PNG.
对每张 mismatch 卡: 找出差异字符位置, 反推涉及的 idx,
渲染 字库字形 + 当前 codetable 字符 + ygocdb 期望字符 让用户视觉判断.
"""
import sys, json, struct, csv as csv_mod
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
PT, CT = 0x015F3A5C, 0x015BB594
CARDS_IDS_ARRAY = 0x015B7CCC
final = {int(k): v for k, v in json.loads(open('tools/jp-decode/codetable.json', encoding='utf-8').read())['by_idx'].items()}
ygocdb = json.loads(open('refs/ygocdb/cards.json', encoding='utf-8').read())

def cti(c): return ((c & 0xF00) >> 1) | (c & 0x7F)
def read_xx(cid):
    ptr = struct.unpack_from('<I', ROM, PT + cid*24)[0]
    addr = CT + ptr; end = ROM.find(b'\x00', addr)
    return ROM[addr:end]

# ROM cid → ygocdb jp_name
icid_to_cid = defaultdict(list)
for i in range(3072):
    cid = struct.unpack_from('<H', ROM, CARDS_IDS_ARRAY + i*2)[0]
    icid_to_cid[cid].append(4007 + i)

def get_jp_name(cid):
    names = set()
    for icid in icid_to_cid.get(cid, []):
        e = ygocdb.get(str(icid))
        if e and e.get('jp_name'): names.add(e['jp_name'])
    return list(names)

DECO = '　・－「」『』！？.，、 '
def norm_strip(s):
    return [c for c in s if c not in DECO]

# Iterate all cards, find char-level diffs (with ygocdb)
diffs = defaultdict(list)  # idx → list of (cid, current_char, ygocdb_char)
for cid in range(1, 2098):
    xx = read_xx(cid)
    if len(xx) % 2 != 0: continue
    # ROM char list with idx
    rom_seq = []  # list of (idx, char)
    for i in range(0, len(xx), 2):
        c = (xx[i]<<8) | xx[i+1]
        if c <= 0xEFFF: continue
        idx = cti(c)
        rom_seq.append((idx, final.get(idx, '?')))
    if any(ch == '?' for _, ch in rom_seq): continue
    
    # Strip decorations from ROM but keep idx mapping
    rom_clean = [(idx, ch) for idx, ch in rom_seq if ch not in DECO]
    
    jp_names = get_jp_name(cid)
    if not jp_names: continue
    # Pick best length-aligned ygocdb name
    best = None
    for jn in jp_names:
        jn_clean = ''.join(c for c in jn if c not in DECO)
        if len(jn_clean) == len(rom_clean):
            best = jn_clean; break
    if best is None: continue
    
    # Char-level compare
    for (idx, cur_ch), exp_ch in zip(rom_clean, best):
        if cur_ch != exp_ch:
            diffs[idx].append((cid, cur_ch, exp_ch))

# Aggregate: each idx → most common expected char + sample cids
idx_summary = []
for idx in sorted(diffs):
    samples = diffs[idx]
    cur = samples[0][1]
    from collections import Counter
    exp_counter = Counter(s[2] for s in samples)
    top_exp, top_count = exp_counter.most_common(1)[0]
    idx_summary.append({
        'idx': idx, 'current': cur, 'expected': top_exp,
        'count': top_count, 'sample_cids': [s[0] for s in samples[:5]],
    })

print(f'Total idx with diffs: {len(idx_summary)}')

# Render review grid
font_lg = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 36)
font_md = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 22)
font_sm = ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc', 14)

BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 8
CELL_W = 160
CELL_H = 320
COLS = 8

import os
os.makedirs('tools/jp-decode/review', exist_ok=True)

for batch in range(0, len(idx_summary), COLS):
    items = idx_summary[batch:batch+COLS]
    n = len(items)
    img = Image.new('RGB', (CELL_W*n + 16, CELL_H), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    for i, ent in enumerate(items):
        x0 = i*CELL_W + 8
        idx = ent['idx']
        # Border
        draw.rectangle([x0, 5, x0+CELL_W-2, CELL_H-5], outline=(180,180,200), width=1)
        # Pos label
        draw.text((x0 + 5, 10), f'{i+1+batch:02d}', fill=(60,60,200), font=font_md)
        draw.text((x0 + 50, 12), f'idx={idx}', fill=(80,80,80), font=font_sm)
        # Glyph
        gx = x0 + (CELL_W - W*SCALE)//2
        gy = 50
        draw.rectangle([gx-2, gy-2, gx+W*SCALE+1, gy+H*SCALE+1], fill=(255,255,255), outline=(150,150,150))
        for y in range(H):
            for x in range(W):
                if ROM[BASE + idx*W*H + y*W + x]:
                    for dy in range(SCALE):
                        for dx in range(SCALE):
                            img.putpixel((gx+x*SCALE+dx, gy+y*SCALE+dy), (0,0,0))
        # Current vs expected (current=red, expected=blue)
        cy = 170
        draw.text((x0+8, cy), '当前:', fill=(80,80,80), font=font_sm)
        cw = draw.textlength(ent['current'], font=font_lg)
        draw.text((x0 + (CELL_W - cw)//2, cy+18), ent['current'], fill=(180,30,30), font=font_lg)
        draw.text((x0+8, cy+72), 'ygocdb:', fill=(80,80,80), font=font_sm)
        cw2 = draw.textlength(ent['expected'], font=font_lg)
        draw.text((x0 + (CELL_W - cw2)//2, cy+90), ent['expected'], fill=(30,80,180), font=font_lg)
        # Sample cid
        sids = ', '.join(map(str, ent['sample_cids'][:3]))
        draw.text((x0+8, 280), f'cnt={ent["count"]} cid={sids}', fill=(80,80,80), font=font_sm)
    
    p = f'tools/jp-decode/review/diff_{batch//COLS + 1:02d}.png'
    img.save(p)
    print(f'wrote {p}  ({n} cells)')

# Save summary JSON
with open('tools/jp-decode/diff_review.json', 'w', encoding='utf-8') as f:
    json.dump(idx_summary, f, ensure_ascii=False, indent=2)
