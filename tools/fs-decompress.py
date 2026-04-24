#!/usr/bin/env python3
"""Offline BIOS LZ77 decompressor for Yu-Gi-Oh! EX2006 FS payload.

FS 证据来源: doc/analysis/name-input-page-location.md §5 ~ fs_load 实际分支
- fs_load (FUN_08014FA8) 读 [compressed[0] & 0xF0] >> 4:
    == 1  -> bios_lz77_uncomp (FUN_0810E41C = SWI 0x11)
    == 2  -> bios_huff_uncomp (FUN_0810E418 = SWI 0x12)
  .LZ5bg / .LZncgr / .LZnclr / .LZnanr / .LZncer 全部是 LZ77 (首字节 0x10)

BIOS SWI 0x11 (LZ77UnCompReadNormalWrite8bit) 格式:
  header (4B):
    byte 0: 0x10  (type nibble 0x1 = LZ77, mode nibble 0x0 = normal)
    byte 1-3: decompressed_size (u24 LE)
  body: 迭代直到 decompressed buffer 填满
    每轮读 1 B flag byte (8 bit, MSB first)
    每个 bit:
      0 -> 1 B 直写
      1 -> 2 B (big-endian), 高 4 bit = length-3 (实际 length ∈ [3, 18])
                             低 12 bit = offset-1 (实际 offset ∈ [1, 4096])
           → 从 dst - offset - 1 处拷贝 length 字节到 dst

Usage:
    # 解压单个文件
    python tools/fs-decompress.py <in.LZ*> <out>

    # 批量解压 FS payload -> temp/fs-decompressed/ 同构目录
    python tools/fs-decompress.py --all

    # 与 mGBA 运行时产物逐字节对比
    python tools/fs-decompress.py --verify
"""
import argparse
import struct
import sys
from pathlib import Path


def lz77_decompress(data: bytes) -> bytes:
    """BIOS SWI 0x11 LZ77UnCompReadNormalWrite8bit.

    Returns decompressed buffer. Input's first 4 bytes are the standard header.
    """
    if len(data) < 4:
        raise ValueError(f"data too short ({len(data)} B)")
    magic = data[0]
    if magic != 0x10:
        raise ValueError(f"expected LZ77 magic 0x10, got 0x{magic:02X}")
    decomp_size = data[1] | (data[2] << 8) | (data[3] << 16)

    out = bytearray()
    src_idx = 4
    while len(out) < decomp_size:
        if src_idx >= len(data):
            raise ValueError(f"input exhausted before decomp_size reached "
                             f"(src={src_idx}, have {len(out)}/{decomp_size})")
        flag = data[src_idx]
        src_idx += 1
        for bit_i in range(8):
            if len(out) >= decomp_size:
                break
            if (flag & (0x80 >> bit_i)) == 0:
                # literal byte
                if src_idx >= len(data):
                    raise ValueError("EOF in literal")
                out.append(data[src_idx])
                src_idx += 1
            else:
                # back-reference (2 bytes BE)
                if src_idx + 1 >= len(data):
                    raise ValueError("EOF in back-ref")
                hi = data[src_idx]
                lo = data[src_idx + 1]
                src_idx += 2
                length = (hi >> 4) + 3
                offset = (((hi & 0x0F) << 8) | lo) + 1
                src_pos = len(out) - offset
                if src_pos < 0:
                    raise ValueError(f"back-ref offset out of range "
                                     f"(dst_pos={len(out)}, offset={offset})")
                for _ in range(length):
                    out.append(out[src_pos])
                    src_pos += 1
    return bytes(out)


def read_fs_master(rom: bytes) -> dict:
    """Parse FS master struct at ROM 0x1E61178."""
    base = 0x1E61178
    file_count = struct.unpack_from('<I', rom, base + 0x00)[0]
    paths_off = struct.unpack_from('<I', rom, base + 0x04)[0]
    offtab_entry1_off = struct.unpack_from('<I', rom, base + 0x08)[0]
    szt_entry1_off = struct.unpack_from('<I', rom, base + 0x0C)[0]
    fsdata_off = struct.unpack_from('<I', rom, base + 0x10)[0]

    paths_base = base + paths_off
    # offtab has 339 u32 entries + sentinel at [0], entry1 starts at offtab_entry1_off
    offtab_base = base + offtab_entry1_off - 4  # back up to include sentinel[0]
    szt_base = base + szt_entry1_off - 4  # similar
    fsdata_base = base + fsdata_off

    return {
        'file_count': file_count,
        'paths_base': paths_base,
        'offtab_base': offtab_base,
        'szt_base': szt_base,
        'fsdata_base': fsdata_base,
    }


def read_paths(rom: bytes, paths_base: int, count: int) -> list:
    """Read `count` null-terminated ASCII paths from paths_base.

    Each path is padded with \\x00 to keep alignment (varies, we scan null-term)."""
    paths = []
    pos = paths_base
    for _ in range(count):
        end = rom.index(0, pos)
        paths.append(rom[pos:end].decode('ascii'))
        pos = end + 1
        while pos < len(rom) and rom[pos] == 0:
            pos += 1
    return paths


def decompress_one_fid(rom: bytes, fs: dict, fid: int) -> tuple[bytes, int, int]:
    """Decompress file with FS-FID (1-based).  Returns (data, comp_size, decomp_size).

    fs_load (asm/all.s:08014fa8) after calling bios_lz77_uncomp does `add r0, r5, #4`
    — skipping the first 4 bytes of the decompressed buffer (compressor tool's extra
    header, redundant copy of LZ77 header with type nibble zeroed).  Match that here.
    """
    offtab = fs['offtab_base']
    szt = fs['szt_base']
    file_offset = struct.unpack_from('<I', rom, offtab + fid * 4)[0]
    file_size = struct.unpack_from('<I', rom, szt + fid * 4)[0]
    src = rom[fs['fsdata_base'] + file_offset : fs['fsdata_base'] + file_offset + file_size]
    if src[:1] == b'\x10':
        decomp = lz77_decompress(src)
        # Skip the first 4 bytes (fs_load does `r0 += 4` after SWI 0x11)
        return decomp[4:], file_size, len(decomp) - 4
    return src, file_size, len(src)  # non-LZ files (.ydc, .ydq) passed through


def cli_single(in_path: str, out_path: str):
    data = Path(in_path).read_bytes()
    out = lz77_decompress(data)
    Path(out_path).write_bytes(out)
    print(f'{in_path}: {len(data)} B -> {out_path}: {len(out)} B')


def cli_all(out_dir: str = 'fs-decompressed-pyz', rom_path: str = 'roms/2343.gba'):
    """Decompress every FS file to <out_dir>/<orig path stripped of .LZ prefix>."""
    rom = Path(rom_path).read_bytes()
    fs = read_fs_master(rom)
    paths = read_paths(rom, fs['paths_base'], fs['file_count'])

    out_root = Path(out_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    stats = {'lz77': 0, 'passthrough': 0, 'skipped_dup': 0, 'err': 0}
    seen_paths = set()
    for i, p in enumerate(paths):
        fid = i + 1  # path[i] ↔ FID[i+1]
        # Derive decompressed filename: "foo.LZncgr" -> "foo.ncgr"; "foo.LZ5bg" -> "foo.gbtn"
        decomp_path = p.replace('.LZ5bg', '.gbtn').replace('.LZ', '.')
        if decomp_path in seen_paths:
            # Duplicate path: append _dup1, _dup2
            base, _, ext = decomp_path.rpartition('.')
            n = 1
            while f'{base}_dup{n}.{ext}' in seen_paths:
                n += 1
            decomp_path = f'{base}_dup{n}.{ext}'
        seen_paths.add(decomp_path)

        out_fp = out_root / decomp_path
        out_fp.parent.mkdir(parents=True, exist_ok=True)
        try:
            data, cs, ds = decompress_one_fid(rom, fs, fid)
            out_fp.write_bytes(data)
            if cs != ds:
                stats['lz77'] += 1
            else:
                stats['passthrough'] += 1
        except Exception as e:
            stats['err'] += 1
            print(f'[err] FID {fid} ({p}): {e}')

    print(f'Stats: LZ77 decomp {stats["lz77"]}, passthrough {stats["passthrough"]}, errors {stats["err"]}')
    print(f'Output: {out_root}/')


def cli_verify(reference_dir: str = 'temp/fs-decompressed', rom_path: str = 'roms/2343.gba'):
    """Decompress in-memory and compare to reference_dir (mGBA runtime dump)."""
    rom = Path(rom_path).read_bytes()
    fs = read_fs_master(rom)
    paths = read_paths(rom, fs['paths_base'], fs['file_count'])

    ref_root = Path(reference_dir)
    if not ref_root.exists():
        print(f'ERROR: reference dir {ref_root} not found')
        sys.exit(1)

    stats = {'match': 0, 'differ': 0, 'missing_ref': 0, 'err': 0, 'passthrough': 0}
    differ_list = []
    seen_paths = {}
    for i, p in enumerate(paths):
        fid = i + 1
        decomp_path = p.replace('.LZ5bg', '.gbtn').replace('.LZ', '.')
        # Dedup (reference dir uses _dup1, _dup2 suffix)
        count = seen_paths.get(decomp_path, 0)
        seen_paths[decomp_path] = count + 1
        if count > 0:
            base, _, ext = decomp_path.rpartition('.')
            decomp_path_check = f'{base}_dup{count}.{ext}'
        else:
            decomp_path_check = decomp_path

        ref_fp = ref_root / decomp_path_check
        if not ref_fp.exists():
            stats['missing_ref'] += 1
            continue

        try:
            data, cs, ds = decompress_one_fid(rom, fs, fid)
            if cs == ds:
                stats['passthrough'] += 1
                continue  # reference may not include passthrough files anyway
            ref = ref_fp.read_bytes()
            if data == ref:
                stats['match'] += 1
            else:
                stats['differ'] += 1
                differ_list.append((fid, p, len(data), len(ref),
                                    next((k for k in range(min(len(data), len(ref))) if data[k] != ref[k]), -1)))
        except Exception as e:
            stats['err'] += 1
            print(f'[err] FID {fid} ({p}): {e}')

    print(f'\n=== Verify against {ref_root} ===')
    print(f'LZ77 match:           {stats["match"]}')
    print(f'LZ77 differ:          {stats["differ"]}')
    print(f'Missing reference:    {stats["missing_ref"]}')
    print(f'Passthrough (no LZ):  {stats["passthrough"]}')
    print(f'Errors:               {stats["err"]}')
    if differ_list:
        print(f'\nDiffer detail (first 10):')
        for fid, p, dl, rl, first_diff in differ_list[:10]:
            print(f'  FID {fid} ({p}): ours={dl}B ref={rl}B first_diff@0x{first_diff:X}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('infile', nargs='?', help='Input .LZ* file')
    ap.add_argument('outfile', nargs='?', help='Output decompressed file')
    ap.add_argument('--all', action='store_true', help='Decompress all FS files from ROM')
    ap.add_argument('--verify', action='store_true', help='Verify against reference dir')
    ap.add_argument('--rom', default='roms/2343.gba')
    ap.add_argument('--ref', default='temp/fs-decompressed')
    ap.add_argument('--out', default='fs-decompressed-pyz', help='Output dir for --all')
    args = ap.parse_args()

    if args.all:
        cli_all(args.out, args.rom)
    elif args.verify:
        cli_verify(args.ref, args.rom)
    elif args.infile and args.outfile:
        cli_single(args.infile, args.outfile)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
