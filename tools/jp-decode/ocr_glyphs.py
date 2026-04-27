"""
对 1925 个单字 PNG 跑 manga-ocr，输出 JSON 码表 + 进度。

输出: tools/jp-decode/ocr_raw.json
   {"by_idx": {"0": "...", "1": "...", ...},
    "by_charcode": {"F8F7": "...", ...}}
"""
import json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

GLYPH_DIR = Path("tools/jp-decode/glyphs")
OUT = Path("tools/jp-decode/ocr_raw.json")
N = 1925

print('Loading manga-ocr...')
from manga_ocr import MangaOcr
mocr = MangaOcr()
print('Ready, OCR start.')

results_by_idx = {}
t0 = time.time()
for idx in range(N):
    p = GLYPH_DIR / f'idx_{idx:04d}.png'
    r = mocr(p)
    results_by_idx[idx] = r
    if (idx + 1) % 50 == 0:
        elapsed = time.time() - t0
        rate = (idx + 1) / elapsed
        eta = (N - idx - 1) / rate
        print(f'  {idx+1:4d}/{N}  {rate:.1f} /s  ETA {eta/60:.1f} min')

# Build by-charcode dict (using inverse formula path: code > 0xEFFF)
# idx → (hi, lo): hi = ((idx >> 7) & 0xF) | 0xF0; lo = (idx & 0x7F) | 0x80
results_by_charcode = {}
for idx, ch in results_by_idx.items():
    hi = ((idx >> 7) & 0xF) | 0xF0
    lo = (idx & 0x7F) | 0x80
    code = (hi << 8) | lo
    results_by_charcode[f'{code:04X}'] = ch

OUT.write_text(json.dumps({
    'by_idx': {str(k): v for k, v in results_by_idx.items()},
    'by_charcode': results_by_charcode,
    '_meta': {
        'engine': 'manga-ocr',
        'font_source': 'font_jp_main_large @ 0x09C2B7EC',
        'glyph_geom': '12×12 8bpp, scaled 8x with margin 8',
        'count': N,
        'elapsed_sec': time.time() - t0,
    },
}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'\nDone. {N} glyphs in {time.time()-t0:.0f} sec → {OUT}')
