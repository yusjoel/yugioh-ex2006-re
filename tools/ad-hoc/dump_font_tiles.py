"""Dump first glyph tiles from state3 sprite VRAM as ASCII art."""
import pathlib

v3 = (pathlib.Path(r"E:/Workspace/yugioh-ex2006-re/doc/temp/vram_state3.bin")).read_bytes()
# sprite tile base = 0x06010000 → file offset 0x10000
BASE = 0x10000
# 4bpp: 32B per tile, 8x8 pixels
# tile row layout: 4 bytes/row, each nibble = 1 pixel (low nibble first)

def render_tile(tile_idx):
    off = BASE + tile_idx * 32
    rows = []
    for y in range(8):
        row_bytes = v3[off + y*4 : off + y*4 + 4]
        px = []
        for b in row_bytes:
            px.append(b & 0xF)
            px.append((b >> 4) & 0xF)
        rows.append(''.join('.' if p == 0 else f'{p:X}' for p in px))
    return rows

for t in range(16):
    print(f"--- tile {t} (addr 0x0601{t*32:04X}) ---")
    for r in render_tile(t):
        print(' ', r)
