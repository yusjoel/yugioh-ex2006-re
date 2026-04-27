"""
跑 PaddleOCR (triple-copy 策略) 单字 OCR 全 1925 个 glyph。

triple-copy: 把单字水平复制 3 份强制 PaddleOCR detection 触发,
然后取识别结果中的众数字符。

输出: tools/jp-decode/ocr_paddle.json
"""
import os, sys, json, time, warnings
os.environ['FLAGS_use_mkldnn'] = '0'
warnings.filterwarnings('ignore')
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
from PIL import Image
from collections import Counter
from paddleocr import PaddleOCR

ROM = open('roms/2343.gba', 'rb').read()
BASE = 0x09C2B7EC - 0x08000000   # font_jp_main_large
W, H = 12, 12
GS = W * H
N = 1925

print('Loading PaddleOCR...')
ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False,
                use_textline_orientation=False, lang='japan',
                enable_mkldnn=False)
print('OK ready.')


def render_triple(idx, scale=8, margin=4, gap=2):
    out_w = (W*scale + gap) * 3 - gap + margin*2
    out_h = H*scale + margin*2
    img = Image.new('L', (out_w, out_h), 255)
    px = img.load()
    for r in range(3):
        for y in range(H):
            for x in range(W):
                if ROM[BASE + idx*GS + y*W + x]:
                    bx = margin + r*(W*scale + gap) + x*scale
                    by = margin + y*scale
                    for dy in range(scale):
                        for dx in range(scale):
                            px[bx+dx, by+dy] = 0
    return np.array(img.convert('RGB'))


def ocr_glyph(idx):
    arr = render_triple(idx)
    res = ocr.predict(arr)
    text = ''
    if res and res[0]:
        rec = res[0].get('rec_texts') or []
        text = ''.join(rec)
    most = Counter(text).most_common(1)[0][0] if text else ''
    return text, most


results_by_idx = {}
empties = []
t0 = time.time()
for idx in range(N):
    raw, picked = ocr_glyph(idx)
    results_by_idx[idx] = {'raw': raw, 'pick': picked}
    if not picked:
        empties.append(idx)
    if (idx + 1) % 50 == 0:
        elapsed = time.time() - t0
        rate = (idx + 1) / elapsed
        eta = (N - idx - 1) / rate
        empty_rate = len(empties) / (idx + 1)
        print(f'  {idx+1:4d}/{N}  {rate:.1f}/s  ETA {eta/60:.1f}m  empty={empty_rate*100:.1f}%')

elapsed = time.time() - t0

# Build by_charcode dict (using inverse formula path: code > 0xEFFF)
by_charcode = {}
for idx, d in results_by_idx.items():
    hi = ((idx >> 7) & 0xF) | 0xF0
    lo = (idx & 0x7F) | 0x80
    code = (hi << 8) | lo
    by_charcode[f'{code:04X}'] = d['pick']

OUT = 'tools/jp-decode/ocr_paddle.json'
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({
        'by_idx': {str(k): v for k, v in results_by_idx.items()},
        'by_charcode': by_charcode,
        '_meta': {
            'engine': 'paddleocr (PP-OCRv5 server, lang=japan)',
            'render': 'triple-copy 12×12→8x scale, margin=4, gap=2',
            'count': N,
            'empty_count': len(empties),
            'empty_rate': len(empties) / N,
            'elapsed_sec': elapsed,
        },
    }, f, ensure_ascii=False, indent=2)
print(f'\nDone. {N} in {elapsed:.0f}s. Empty: {len(empties)}/{N} = {len(empties)/N*100:.1f}%')
print(f'Output: {OUT}')
