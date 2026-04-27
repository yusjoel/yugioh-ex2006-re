"""渲染 1135 (精) vs 1152 vs 1153 对比, 加 hits 数 + 上下文用例"""
import json
import re
from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000
W, H = 12, 12
SCALE = 28


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


# 算 _xx hits 和搜上下文
src = open('data/card-descriptions.s', encoding='latin-1').read()
pat = re.compile(r'card_desc_(\d+)_(xx|ja):\s*\n\s*\.ascii\s+"((?:[^"\\]|\\.)*)"')
hits = Counter()
contexts = {1135: [], 1152: [], 1153: []}
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
        if idx in (1135, 1152, 1153):
            hits[idx] += 1
            if len(contexts[idx]) < 3:
                lo = max(0, pos - 8); hi_e = min(len(seq), pos + 9)
                ctx = ''.join(CT.get(i, '?') if i and i != idx else f'[?{idx}]' for i in seq[lo:hi_e] if i is not None)
                contexts[idx].append(f'cid={cid}: ...{ctx}...')

# 也搜 ROM
def search_rom(target):
    hi = ((target >> 7) & 0xF) | 0xF0
    lo = (target & 0x7F) | 0x80
    pat_b = bytes([hi, lo])
    rom_ctxs = []
    start = 0
    while len(rom_ctxs) < 3:
        p = ROM.find(pat_b, start)
        if p < 0: break
        # 邻居必须像文本
        ok = False
        if p >= 2 and (ROM[p-2] >= 0xF0 or ROM[p-2] in (0,1,2,3,4,5,6,7)):
            if p + 3 < len(ROM) and (ROM[p+2] >= 0xF0 or ROM[p+2] in (0,1,2,3,4,5,6,7)):
                ok = True
        if ok:
            # decode
            ctx_lo = max(0, p - 24)
            ctx_hi = min(len(ROM), p + 26)
            if (ctx_lo) % 2 != 0: ctx_lo += 1
            out = []
            j = ctx_lo
            while j + 1 < ctx_hi:
                b0, b1 = ROM[j], ROM[j+1]
                if j == p:
                    out.append(f'[?{target}]'); j += 2; continue
                idx2 = code_to_idx(b0, b1)
                if idx2 is not None:
                    ch = CT.get(idx2, f'<{idx2}>')
                    out.append(ch if ch else '?')
                elif b0 == 0:
                    out.append('§')
                elif b0 < 8:
                    out.append(f'<c{b0:02X}>')
                else:
                    out.append('?')
                j += 2
            s = ''.join(out)
            valid = sum(1 for ch in s if len(ch) == 1 and ord(ch) > 0x7F)
            if valid >= 4 and 0x015A0000 <= p < 0x01E00000:
                rom_ctxs.append(f'  ROM 0x{p:08X}: {s}')
        start = p + 1
    return rom_ctxs


# 渲染
font_path = 'C:/Windows/Fonts/msgothic.ttc'
font_md = ImageFont.truetype(font_path, 24)
font_sm = ImageFont.truetype(font_path, 18)
font_big = ImageFont.truetype(font_path, 50)


def draw_glyph(img, idx, gx0, gy0, scale=SCALE):
    off = BASE + idx * W * H
    for y in range(H):
        for x in range(W):
            if ROM[off + y * W + x]:
                for dy in range(scale):
                    for dx in range(scale):
                        img.putpixel((gx0 + x * scale + dx, gy0 + y * scale + dy), (0, 0, 0))


CELL_W = 720
CELL_H = 540
img = Image.new('RGB', (CELL_W * 3 + 40, CELL_H + 60), (250, 250, 250))
draw = ImageDraw.Draw(img)
draw.text((20, 12), 'idx 1135 / 1152 / 1153 — 都标 「精/績」 之一, 实际 glyph 对比 (28x)',
          fill=(40, 40, 80), font=font_md)

INFO = [
    (1135, '精 (高频, 22 hits, 米+青)', (40, 130, 40)),
    (1152, '績 (low, 0 hits, 我新设)', (200, 100, 30)),
    (1153, '績 (low, 0 hits, 原 codetable)', (180, 60, 30)),
]
for i, (idx, label, color) in enumerate(INFO):
    x0 = 20 + i * CELL_W
    y0 = 50
    draw.rectangle([x0, y0, x0 + CELL_W - 10, y0 + CELL_H - 10], outline=color, width=2)
    draw.text((x0 + 14, y0 + 8), label, fill=color, font=font_md)
    glyph_box = W * SCALE
    gx0 = x0 + (CELL_W - glyph_box) // 2
    gy0 = y0 + 50
    draw.rectangle([gx0 - 2, gy0 - 2, gx0 + glyph_box + 1, gy0 + glyph_box + 1],
                   fill=(255, 255, 255), outline=(140, 140, 140))
    draw_glyph(img, idx, gx0, gy0)
    # codetable 当前
    draw.text((x0 + 14, y0 + 50 + glyph_box + 20),
              f'codetable[{idx}] = {CT.get(idx)!r}', fill=(60, 60, 60), font=font_sm)
    # _xx 上下文
    y_ctx = y0 + 50 + glyph_box + 50
    draw.text((x0 + 14, y_ctx), '_xx 上下文 (前后 8 字):', fill=(40, 40, 80), font=font_sm)
    if contexts[idx]:
        for j, c in enumerate(contexts[idx][:3]):
            draw.text((x0 + 14, y_ctx + 22 + j * 22), c[:90], fill=(60, 60, 60), font=font_sm)
    else:
        draw.text((x0 + 14, y_ctx + 22), '(0 hits)', fill=(150, 100, 30), font=font_sm)
    # ROM 全文上下文
    rom_ctxs = search_rom(idx)
    y_rom = y_ctx + 100
    draw.text((x0 + 14, y_rom), 'ROM 全文 上下文:', fill=(40, 40, 80), font=font_sm)
    if rom_ctxs:
        for j, c in enumerate(rom_ctxs[:2]):
            draw.text((x0 + 14, y_rom + 22 + j * 22), c[:90], fill=(60, 60, 60), font=font_sm)
    else:
        draw.text((x0 + 14, y_rom + 22), '(0 text-like hits)', fill=(150, 100, 30), font=font_sm)

OUT = Path('tools/card-desc/seki_compare.png')
img.save(OUT)
print(f'wrote {OUT}')
print(f'\nhits in _xx:')
for idx, h in hits.items():
    print(f'  idx={idx}: {h} hits')
