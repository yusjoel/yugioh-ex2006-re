#!/usr/bin/env python3
"""Map each name_b_0X.gbtn tilemap to VRAM SBB.  GBA stores tilemap as 32×32 u16,
but .gbtn is W-wide (W=30).  Also the loader likely adds a base tile offset and/or
palette bank bits when writing entries to VRAM.  Try multiple transformations.
"""
import struct
from pathlib import Path

FS = Path('temp/fs-decompressed/name_input')
TMP = Path('doc/temp')

vram = TMP.joinpath('B_vram.bin').read_bytes()

def extract_gbtn(data: bytes):
    bgdt_off = 0x21C
    bgdt_size = struct.unpack_from('<I', data, bgdt_off + 4)[0]
    bgdt_data = data[bgdt_off + 8 : bgdt_off + bgdt_size]
    tm_size = struct.unpack_from('<I', bgdt_data, 4)[0]
    w, h = struct.unpack_from('<HH', bgdt_data, 8)
    meta = 20  # verified via name_b_02: tile gfx starts at file 0x6E8 = bgdt_data[20+1200]
    tilemap = bgdt_data[meta : meta + tm_size]
    return tilemap, w, h

def reflow(tm: bytes, w: int) -> list:
    """Return list of u16 tilemap entries in 32-wide SBB layout (0..1023)."""
    out = [0] * 1024
    entries = len(tm) // 2
    h = entries // w
    for row in range(min(h, 32)):
        for col in range(w):
            sidx = row * w + col
            didx = row * 32 + col
            out[didx] = struct.unpack_from('<H', tm, sidx * 2)[0]
    return out

def sbb_entries(vram: bytes, off: int) -> list:
    return [struct.unpack_from('<H', vram, off + i * 2)[0] for i in range(1024)]

sbb_offsets = {
    'BG0 SBB28': 0x0E000,
    'BG1 SBB29': 0x0E800,
    'BG2 SBB30': 0x0F000,
    'BG3 SBB31': 0x0F800,
}

def score(gbtn_entries: list, vram_entries: list, base_offset: int = 0, pal_or: int = 0) -> tuple:
    """Count entries matching with: vram = (gbtn + base_offset) | (pal_or << 12).
    Skip entries where gbtn is 0 (treat as blank, expect vram=0 or vram=base_offset)."""
    matches = 0
    nonblank = 0
    for g, v in zip(gbtn_entries, vram_entries):
        if g == 0:
            continue  # blank, skip from scoring both ways
        nonblank += 1
        # transform
        tile_idx = (g & 0x3FF) + base_offset
        flips = g & 0xC00
        transformed = (tile_idx & 0x3FF) | flips | (pal_or << 12)
        if transformed == v:
            matches += 1
    return matches, nonblank

for fname in ['name_b_01.gbtn','name_b_02.gbtn','name_b_03.gbtn','name_b_04.gbtn']:
    data = Path(FS / fname).read_bytes()
    tm, w, h = extract_gbtn(data)
    ge = reflow(tm, w)
    print(f'\n{fname}  ({w}×{h})')
    # Best-of over (sbb × base_offset ∈ [0,50] × pal ∈ [0..15])
    rows = []
    for sbb_name, off in sbb_offsets.items():
        ve = sbb_entries(vram, off)
        best = (0, 0, 0, 0)  # matches, nonblank, base, pal
        for base in range(0, 0x50):
            for pal in range(0, 16):
                m, nb = score(ge, ve, base, pal)
                if m > best[0]:
                    best = (m, nb, base, pal)
        rows.append((best, sbb_name))
    # sort by match count
    rows.sort(key=lambda r: -r[0][0])
    for (m, nb, base, pal), sbb_name in rows:
        pct = 100 * m / nb if nb else 0
        mark = ' ★' if rows[0][0] == (m, nb, base, pal) else '  '
        print(f' {mark} {sbb_name:12s}  base=+{base:3d}  pal={pal:2d}  {m:>4d}/{nb:<4d} non-blank  ({pct:.1f}%)')
