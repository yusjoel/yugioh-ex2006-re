#!/usr/bin/env python3
"""Diff VRAM/PALRAM/OAM between state A (title screen, no save) and
state B (name input / character creation). Merge runs with gap <= 64.

Also decode IO registers DISPCNT, BG0-3CNT, WIN*, BLD* into human-readable form.
"""
import struct
from pathlib import Path

ROOT = Path('doc/temp')

def load(name):
    return ROOT.joinpath(name).read_bytes()

def diff_runs(a: bytes, b: bytes, base: int, gap: int = 64):
    """Return list of (start, end_exclusive) runs where a[i] != b[i], merging
    adjacent mismatch runs separated by <= `gap` equal bytes."""
    assert len(a) == len(b)
    runs = []
    i = 0
    n = len(a)
    cur_start = None
    last_mismatch = None
    while i < n:
        if a[i] != b[i]:
            if cur_start is None:
                cur_start = i
            last_mismatch = i
            i += 1
        else:
            if cur_start is not None:
                # look ahead up to `gap` bytes to see if another mismatch follows
                j = i
                lookahead = min(n, i + gap + 1)
                found = False
                while j < lookahead:
                    if a[j] != b[j]:
                        found = True
                        last_mismatch = j
                        i = j + 1
                        break
                    j += 1
                if not found:
                    runs.append((base + cur_start, base + last_mismatch + 1))
                    cur_start = None
            else:
                i += 1
    if cur_start is not None:
        runs.append((base + cur_start, base + last_mismatch + 1))
    return runs

def u16(b, off):
    return struct.unpack_from('<H', b, off)[0]

def u32(b, off):
    return struct.unpack_from('<I', b, off)[0]

def decode_dispcnt(v):
    mode = v & 7
    frame = (v >> 4) & 1
    hblank_free = (v >> 5) & 1
    obj_1d = (v >> 6) & 1
    forced_blank = (v >> 7) & 1
    bg0 = (v >> 8) & 1
    bg1 = (v >> 9) & 1
    bg2 = (v >> 10) & 1
    bg3 = (v >> 11) & 1
    obj = (v >> 12) & 1
    win0 = (v >> 13) & 1
    win1 = (v >> 14) & 1
    winobj = (v >> 15) & 1
    return (f'mode={mode} frame={frame} hblank_free={hblank_free} obj_1d={obj_1d} '
            f'forced_blank={forced_blank} BG0={bg0} BG1={bg1} BG2={bg2} BG3={bg3} '
            f'OBJ={obj} win0={win0} win1={win1} winobj={winobj}')

def decode_bgcnt(v):
    prio = v & 3
    cbb = (v >> 2) & 3  # char base block
    mosaic = (v >> 6) & 1
    col256 = (v >> 7) & 1  # 0=4bpp 1=8bpp
    sbb = (v >> 8) & 0x1f  # screen base block
    overflow_wrap = (v >> 13) & 1
    size = (v >> 14) & 3
    size_map = {0: '32x32', 1: '64x32', 2: '32x64', 3: '64x64'}
    cb_base = 0x06000000 + cbb * 0x4000
    sb_base = 0x06000000 + sbb * 0x800
    bpp = '8bpp' if col256 else '4bpp'
    return (f'prio={prio} CBB={cbb}→{cb_base:08X} SBB={sbb}→{sb_base:08X} '
            f'{bpp} mosaic={mosaic} size={size_map[size]}')

def dump_io(label, io):
    dispcnt = u16(io, 0x00)
    bg0cnt = u16(io, 0x08)
    bg1cnt = u16(io, 0x0A)
    bg2cnt = u16(io, 0x0C)
    bg3cnt = u16(io, 0x0E)
    print(f'=== IO ({label}) ===')
    print(f'  DISPCNT  = 0x{dispcnt:04X}  {decode_dispcnt(dispcnt)}')
    print(f'  BG0CNT   = 0x{bg0cnt:04X}  {decode_bgcnt(bg0cnt)}')
    print(f'  BG1CNT   = 0x{bg1cnt:04X}  {decode_bgcnt(bg1cnt)}')
    print(f'  BG2CNT   = 0x{bg2cnt:04X}  {decode_bgcnt(bg2cnt)}')
    print(f'  BG3CNT   = 0x{bg3cnt:04X}  {decode_bgcnt(bg3cnt)}')
    print()

def main():
    a_io = load('A_io.bin')
    b_io = load('B_io.bin')
    dump_io('A title', a_io)
    dump_io('B name_input', b_io)

    # VRAM diff
    a_vram = load('A_vram.bin')
    b_vram = load('B_vram.bin')
    runs = diff_runs(a_vram, b_vram, 0x06000000, gap=64)
    runs.sort(key=lambda r: -(r[1]-r[0]))
    print(f'=== VRAM diff runs (gap<=64), total {len(runs)} ===')
    for start, end in runs[:40]:
        region = ('BG charblock' if start < 0x06010000 else 'OBJ tile (1D map 0x06010000+)')
        # classify by charblock
        cb = (start - 0x06000000) // 0x4000
        print(f'  0x{start:08X}..0x{end:08X}  ({end-start:6d} B)  CB{cb}  {region}')
    total = sum(e-s for s,e in runs)
    print(f'  TOTAL DIFFER: {total} B / 98304 B ({100*total/98304:.1f}%)')
    print()

    # PALRAM diff
    a_pal = load('A_palram.bin')
    b_pal = load('B_palram.bin')
    pal_runs = diff_runs(a_pal, b_pal, 0x05000000, gap=16)
    print(f'=== PALRAM diff runs (gap<=16), total {len(pal_runs)} ===')
    for start, end in pal_runs:
        region = 'BG pal' if start < 0x05000200 else 'OBJ pal'
        print(f'  0x{start:08X}..0x{end:08X}  ({end-start:4d} B)  {region}')
    total = sum(e-s for s,e in pal_runs)
    print(f'  TOTAL DIFFER: {total} B / 1024 B ({100*total/1024:.1f}%)')
    print()

    # OAM diff
    a_oam = load('A_oam.bin')
    b_oam = load('B_oam.bin')
    oam_runs = diff_runs(a_oam, b_oam, 0x07000000, gap=8)
    print(f'=== OAM diff runs (gap<=8), total {len(oam_runs)} ===')
    for start, end in oam_runs[:20]:
        idx = (start - 0x07000000) // 8
        print(f'  0x{start:08X}..0x{end:08X}  ({end-start:4d} B)  sprite#{idx}+')

if __name__ == '__main__':
    main()
