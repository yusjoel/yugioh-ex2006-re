"""
渲染 1925 个 glyph 为单字 PNG (用于单字 OCR)。

用 main_large (12×12) 字库；每字放大 8x、白底黑字、加 margin。
输出: tools/jp-decode/glyphs/idx_NNNN.png
"""
from pathlib import Path
from PIL import Image

ROM = Path("roms/2343.gba").read_bytes()
BASE = 0x09C2B7EC - 0x08000000  # font_jp_main_large
W, H = 12, 12
GS = W * H
N = 1925

OUT = Path("tools/jp-decode/glyphs")
OUT.mkdir(parents=True, exist_ok=True)

SCALE = 8
MARGIN = 8

for idx in range(N):
    off = BASE + idx * GS
    out_w = W * SCALE + MARGIN * 2
    out_h = H * SCALE + MARGIN * 2
    img = Image.new('L', (out_w, out_h), 255)
    px = img.load()
    for y in range(H):
        for x in range(W):
            if ROM[off + y*W + x] != 0:
                bx = MARGIN + x * SCALE
                by = MARGIN + y * SCALE
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        px[bx + dx, by + dy] = 0
    img.save(OUT / f'idx_{idx:04d}.png')

print(f'wrote {N} glyph PNGs to {OUT} (size {out_w}x{out_h})')
