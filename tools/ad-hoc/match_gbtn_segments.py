#!/usr/bin/env python3
"""Break each name_b_0X.gbtn BGDT into [meta][tilemap][tile graphics] and
match each portion to VRAM SBB (tilemap) and CBB (tile graphics) regions."""
from pathlib import Path
import struct

FS = Path('temp/fs-decompressed/name_input')
TMP = Path('doc/temp')

vram = TMP.joinpath('B_vram.bin').read_bytes()
palram = TMP.joinpath('B_palram.bin').read_bytes()

def find_all(hay: bytes, needle: bytes, limit=3):
    out, i = [], 0
    while len(out) < limit:
        j = hay.find(needle, i)
        if j < 0:
            break
        out.append(j)
        i = j + 1
    return out

def scan_segment(seg: bytes, vram: bytes, window=16):
    """Return unique VRAM destination base addresses where this segment appears."""
    hits = set()
    for off in range(0, len(seg) - window, window):
        w = seg[off:off + window]
        if len(set(w)) < 4:
            continue
        for h in find_all(vram, w, limit=1):
            hits.add(0x06000000 + h - off)  # base where seg[0] would be
    return hits

for fname in ['name_b_01.gbtn','name_b_02.gbtn','name_b_03.gbtn','name_b_04.gbtn']:
    data = Path(FS / fname).read_bytes()
    # Sections already parsed: PALT @ 0x10 size 0x20C, BGDT @ 0x21C size varies
    palt_off, palt_size = 0x10, 0x20C
    bgdt_off = 0x21C
    bgdt_size = struct.unpack_from('<I', data, bgdt_off + 4)[0]
    bgdt_data = data[bgdt_off + 8 : bgdt_off + bgdt_size]  # skip 8B section header

    # BGDT meta header (from earlier peek at 0x224 — 16 bytes):
    # flags(2) + 0x02(2) + tile_map_size_u32 + w_u16 + h_u16 + w_u16 + h_u16
    meta = bgdt_data[0:16]
    flags = struct.unpack_from('<HH', meta, 0)
    tm_bytesize = struct.unpack_from('<I', meta, 4)[0]
    w1, h1, w2, h2 = struct.unpack_from('<HHHH', meta, 8)
    print(f'\n=== {fname} (BGDT data={len(bgdt_data)} B) ===')
    print(f'  meta: flags={flags} tm_size=0x{tm_bytesize:X} w1={w1} h1={h1} w2={w2} h2={h2}')

    tilemap = bgdt_data[16:16 + tm_bytesize]
    tiles = bgdt_data[16 + tm_bytesize:]
    print(f'  tilemap: {len(tilemap)} B')
    print(f'  tiles:   {len(tiles)} B  = {len(tiles)//64} × 64 B (8bpp tiles)')
    # Palette from PALT section (skip 8B section header + maybe 4B sub-header)
    palt = data[palt_off + 8 : palt_off + palt_size]
    print(f'  palt:    {len(palt)} B')

    # Match tilemap against VRAM
    tm_hits = scan_segment(tilemap, vram, window=16)
    print(f'  tilemap → VRAM candidate bases: {sorted(hex(h) for h in tm_hits)}')

    # Match tiles
    tl_hits = scan_segment(tiles, vram, window=32) if len(tiles) > 0 else set()
    print(f'  tiles   → VRAM candidate bases: {sorted(hex(h) for h in tl_hits)}')

    # Match palt (16-B windows)
    pal_hits = set()
    for off in range(0, len(palt) - 16, 2):
        w = palt[off:off + 16]
        if len(set(w)) < 4:
            continue
        for h in find_all(palram, w, limit=1):
            pal_hits.add(0x05000000 + h - off)
    print(f'  palt    → PALRAM candidate bases: {sorted(hex(h) for h in pal_hits)}')
