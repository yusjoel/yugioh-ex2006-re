#!/usr/bin/env python3
"""Render .gbtn (NTBG bundle) to PNG.

Format spec: doc/dev/data-structure/gbtn-format.md

Usage:
    python tools/rom-export/render_gbtn.py <in.gbtn> [out.png]
    python tools/rom-export/render_gbtn.py --all [--decomp-dir <dir>] [--out-dir <dir>]

When --all is given and --decomp-dir is not specified, first runs
`tools/fs-decompress.py --all` into a temp dir, then renders every .gbtn there.
"""
import argparse
import struct
import subprocess
import sys
from pathlib import Path


def bgr555_to_rgb888(c: int) -> tuple[int, int, int]:
    r = (c & 0x1F) << 3
    g = ((c >> 5) & 0x1F) << 3
    b = ((c >> 10) & 0x1F) << 3
    # extend low 3 bits by duplicating top (more accurate than bare shift)
    r |= r >> 5
    g |= g >> 5
    b |= b >> 5
    return (r, g, b)


def parse_gbtn(data: bytes) -> dict:
    """Return dict with keys: palette (list of RGB), tilemap (bytes), tile_gfx (bytes),
    w, h, bpp, tile_count.

    bpp inference: palette_count alone is insufficient — many files have
    palette_count=256 but store tiles in 4bpp form (16×16 sub-palette mode).
    Must also look at the tilemap's max tile index and match against the
    possible tile counts (tile_gfx_size/64 for 8bpp, /32 for 4bpp).
    """
    if data[0:4] != b'NTBG':
        raise ValueError(f'not NTBG: magic={data[0:4]!r}')
    if data[0x10:0x14] != b'PALT':
        raise ValueError('missing PALT')
    palt_size = struct.unpack_from('<I', data, 0x14)[0]
    pal_count = struct.unpack_from('<I', data, 0x18)[0]
    palette = []
    for i in range(pal_count):
        c = struct.unpack_from('<H', data, 0x1C + i * 2)[0]
        palette.append(bgr555_to_rgb888(c))

    bgdt_off = 0x10 + palt_size
    if data[bgdt_off:bgdt_off + 4] != b'BGDT':
        raise ValueError('missing BGDT')
    flags = struct.unpack_from('<I', data, bgdt_off + 8)[0]
    tm_size = struct.unpack_from('<I', data, bgdt_off + 0x0C)[0]
    w1, h1 = struct.unpack_from('<HH', data, bgdt_off + 0x10)
    tile_gfx_size = struct.unpack_from('<I', data, bgdt_off + 0x18)[0]
    tilemap = data[bgdt_off + 0x1C : bgdt_off + 0x1C + tm_size]
    tile_gfx = data[bgdt_off + 0x1C + tm_size : bgdt_off + 0x1C + tm_size + tile_gfx_size]

    # flags[2] (= (flags >> 16) & 0xFF) selects tilemap entry size:
    #   0x02 → 2-byte entries (standard GBA tilemap)
    #   0x04 → 4-byte entries (u16 tile_idx + u16 extended bank/flags)
    entry_bytes = 4 if ((flags >> 16) & 0xFF) == 0x04 else 2
    entry_count = tm_size // entry_bytes

    # Compute max tile index used by tilemap (always in first u16 of entry)
    max_idx = 0
    for i in range(entry_count):
        e = struct.unpack_from('<H', tilemap, i * entry_bytes)[0] & 0x3FF
        if e > max_idx:
            max_idx = e

    count_8bpp = tile_gfx_size // 64
    count_4bpp = tile_gfx_size // 32

    if pal_count == 16:
        bpp = 4
    elif max_idx < count_8bpp:
        bpp = 8
    elif max_idx < count_4bpp:
        bpp = 4
    else:
        bpp = 4

    tile_byte = 64 if bpp == 8 else 32
    tile_count = tile_gfx_size // tile_byte
    return dict(palette=palette, tilemap=tilemap, tile_gfx=tile_gfx,
                w=w1, h=h1, bpp=bpp, tile_count=tile_count,
                flags=flags, tm_size=tm_size, tile_gfx_size=tile_gfx_size,
                pal_count=pal_count, max_tile_idx=max_idx,
                entry_bytes=entry_bytes)


def decode_tile_8bpp(tile: bytes) -> list:
    """Return 8×8 list-of-row-of-index for an 8bpp 64-byte tile."""
    rows = []
    for r in range(8):
        rows.append(list(tile[r * 8:r * 8 + 8]))
    return rows


def decode_tile_4bpp(tile: bytes, palette_bank: int = 0) -> list:
    """Return 8×8 list-of-row of palette index (bank offset applied)."""
    rows = []
    base = palette_bank * 16
    for r in range(8):
        row = []
        for c in range(4):
            b = tile[r * 4 + c]
            row.append((b & 0x0F) + base)
            row.append((b >> 4) + base)
        rows.append(row)
    return rows


def render_tile_pixels(info: dict, tile_index: int, palette_bank: int = 0,
                        oor_rgb: tuple = None) -> list:
    """Return 8×8 RGB tuples for tile `tile_index`.

    When tile_index is out of range for this file's tile_gfx (common: tilemap
    references a shared VRAM tile pool that includes tiles from OTHER .gbtn
    files loaded alongside), render as `oor_rgb` (default = palette[0]
    transparent key color — visually matches how runtime shows "empty" regions).
    """
    if tile_index >= info['tile_count']:
        pal = info['palette']
        default = oor_rgb if oor_rgb is not None else pal[0]
        return [[default] * 8 for _ in range(8)]
    t_bytes_per_tile = 64 if info['bpp'] == 8 else 32
    t = info['tile_gfx'][tile_index * t_bytes_per_tile : (tile_index + 1) * t_bytes_per_tile]
    if info['bpp'] == 8:
        indices = decode_tile_8bpp(t)
    else:
        indices = decode_tile_4bpp(t, palette_bank)
    pal = info['palette']
    return [[pal[i] if i < len(pal) else (255, 0, 255) for i in row] for row in indices]


def render_gbtn_to_pixels(info: dict) -> list:
    """Return 2D list (h*8 rows × w*8 cols) of RGB tuples."""
    w, h = info['w'], info['h']
    tilemap = info['tilemap']
    entry_bytes = info['entry_bytes']
    canvas = [[None] * (w * 8) for _ in range(h * 8)]
    for ty in range(h):
        for tx in range(w):
            idx = ty * w + tx
            # u16[0] always holds tile_idx + flips; for 2-byte entries it also
            # holds palette bank (bits 12-15).  For 4-byte entries, the palette
            # bank lives in u16[1] high nibble.
            e0 = struct.unpack_from('<H', tilemap, idx * entry_bytes)[0]
            tile_i = e0 & 0x3FF
            h_flip = bool(e0 & 0x0400)
            v_flip = bool(e0 & 0x0800)
            if entry_bytes == 4:
                e1 = struct.unpack_from('<H', tilemap, idx * entry_bytes + 2)[0]
                pal_bank = (e1 >> 12) & 0x0F
            else:
                pal_bank = (e0 >> 12) & 0x0F
            pixels = render_tile_pixels(info, tile_i, pal_bank)
            for py in range(8):
                src_y = (7 - py) if v_flip else py
                for px in range(8):
                    src_x = (7 - px) if h_flip else px
                    canvas[ty * 8 + py][tx * 8 + px] = pixels[src_y][src_x]
    return canvas


def save_png(pixels: list, out_path: str):
    """Write PNG using stdlib only (no PIL dependency).  Uses a minimal IDAT encoder."""
    import zlib
    import struct as _s
    h = len(pixels)
    w = len(pixels[0]) if h else 0
    raw = bytearray()
    for row in pixels:
        raw.append(0)  # filter=none
        for (r, g, b) in row:
            raw.append(r)
            raw.append(g)
            raw.append(b)

    def chunk(tag: bytes, data: bytes) -> bytes:
        out = _s.pack('>I', len(data)) + tag + data
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        out += _s.pack('>I', crc)
        return out

    png = b'\x89PNG\r\n\x1a\n'
    ihdr = _s.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)  # 8bit RGB
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    Path(out_path).write_bytes(png)


def render_one(in_path: str, out_path: str):
    data = Path(in_path).read_bytes()
    info = parse_gbtn(data)
    pixels = render_gbtn_to_pixels(info)
    save_png(pixels, out_path)
    return info


def cli_all(decomp_dir: str, out_dir: str, rom_path: str):
    decomp = Path(decomp_dir)
    if not decomp.exists():
        print(f'Decomp dir {decomp} does not exist; running fs-decompress.py --all...')
        subprocess.run([sys.executable, 'tools/fs-decompress.py', '--all',
                        '--out', str(decomp), '--rom', rom_path], check=True)

    gbtn_files = sorted(decomp.rglob('*.gbtn'))
    if not gbtn_files:
        print(f'No .gbtn files found in {decomp}')
        return

    out_root = Path(out_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    for f in gbtn_files:
        rel = f.relative_to(decomp)
        out_fp = out_root / rel.with_suffix('.png')
        out_fp.parent.mkdir(parents=True, exist_ok=True)
        try:
            info = render_one(str(f), str(out_fp))
            print(f'  {rel}  ->  {info["w"]*8}x{info["h"]*8} {info["bpp"]}bpp '
                  f'({info["tile_count"]} tiles)  ->  {out_fp.relative_to(out_root.parent)}')
        except Exception as e:
            print(f'  [err] {rel}: {e}')

    print(f'\nRendered {len(gbtn_files)} files to {out_root}/')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('infile', nargs='?', help='Input .gbtn file')
    ap.add_argument('outfile', nargs='?', help='Output PNG path')
    ap.add_argument('--all', action='store_true', help='Render all .gbtn in decomp dir')
    ap.add_argument('--decomp-dir', default='doc/temp/fs-decomp-all',
                    help='FS decompression output dir (auto-populated if absent)')
    ap.add_argument('--out-dir', default='graphics/images/gbtn-previews',
                    help='PNG output dir for --all')
    ap.add_argument('--rom', default='roms/2343.gba')
    args = ap.parse_args()

    if args.all:
        cli_all(args.decomp_dir, args.out_dir, args.rom)
    elif args.infile:
        out = args.outfile or args.infile.replace('.gbtn', '.png')
        info = render_one(args.infile, out)
        print(f'{args.infile} -> {out}  ({info["w"]*8}x{info["h"]*8} {info["bpp"]}bpp, '
              f'{info["tile_count"]} tiles)')
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
