#!/usr/bin/env python3
"""Match name_input/ FS files to specific VRAM/PALRAM regions using 16-byte
non-trivial windows.
"""
from pathlib import Path

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

def dump_file_matches(name, data):
    hits = []  # (file_off, region, abs_addr)
    for off in range(0, len(data) - 16, 0x10):
        w = data[off:off + 16]
        uniq = len(set(w))
        if uniq < 4:
            continue
        if all(b == 0 for b in w):
            continue
        for h in find_all(vram, w, limit=1):
            hits.append((off, 'VRAM', 0x06000000 + h))
        for h in find_all(palram, w, limit=1):
            hits.append((off, 'PALRAM', 0x05000000 + h))

    # Compute per-region linear run: assume dst_addr = base + (off - start_off)
    # Group by rough region, find longest linear match.
    if not hits:
        print(f'{name}: NO match')
        return

    # Classify into coarse regions for summary
    regions = {}  # region_key -> list of (file_off, abs_addr)
    for off, region, addr in hits:
        # Use 4KB granularity for VRAM, 64B for PALRAM
        if region == 'VRAM':
            key = f'VRAM-CB{(addr - 0x06000000) // 0x4000}-sub{((addr - 0x06000000) % 0x4000) // 0x400:X}'
        else:
            is_bg = addr < 0x05000200
            key = f'{"BGPAL" if is_bg else "OBJPAL"}'
        regions.setdefault(key, []).append((off, addr))

    # Summarize: for each region, give [first, last] file offsets and dst addrs
    print(f'\n{name}:')
    for region, lst in sorted(regions.items()):
        lst.sort()
        n = len(lst)
        first_off, first_addr = lst[0]
        last_off, last_addr = lst[-1]
        delta = first_addr - first_off
        # compute "linear" fraction
        linear_count = sum(1 for off, addr in lst if addr - off == delta)
        print(f'  {region:20s}  {n:4d} hits  file[0x{first_off:04X}..0x{last_off:04X}] → 0x{first_addr:08X}..0x{last_addr:08X}  linear={linear_count}/{n}  delta=0x{delta & 0xFFFFFFFF:08X}')

for f in sorted(FS.iterdir()):
    data = f.read_bytes()
    dump_file_matches(f.name, data)
