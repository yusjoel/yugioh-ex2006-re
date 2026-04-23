#!/usr/bin/env python3
"""
扫描 ROM 指定区间，按多种静态特征给出语义切分线索。
用于 `doc/dev/methodology/asset-location.md` §三 静态路径阶段 1。

默认扫 0x00FBC080..0x01326280（card-image-tiles 尾 + 后 16MB 段前部共 3.6 MB）。
"""
from __future__ import annotations

import argparse
import math
import re
import struct
import sys
from collections import Counter
from pathlib import Path

DEFAULT_START = 0x00FBC080
DEFAULT_END   = 0x01326280
ROM_PATH = Path("roms/2343.gba")

WINDOW = 512      # 熵/nz 滑窗
STEP   = 512      # 步长（与窗口相同 = 非重叠；设 WINDOW/2 得 50% overlap）


def bgr555_is_plausible(b0: int, b1: int) -> bool:
    v = b0 | (b1 << 8)
    return v != 0  # 粗筛：BGR555 任何非零都是候选


def shannon_entropy(buf: bytes) -> float:
    if not buf:
        return 0.0
    freq = Counter(buf)
    n = len(buf)
    return -sum((c / n) * math.log2(c / n) for c in freq.values() if c > 0)


def nz_ratio(buf: bytes) -> float:
    if not buf:
        return 0.0
    return sum(1 for b in buf if b != 0) / len(buf)


def scan_zero_runs(buf: bytes, min_len: int = 64):
    """长 0x00 运行，输出 (start, length)"""
    out = []
    i = 0
    while i < len(buf):
        if buf[i] != 0:
            i += 1; continue
        j = i
        while j < len(buf) and buf[j] == 0:
            j += 1
        if j - i >= min_len:
            out.append((i, j - i))
        i = j
    return out


def scan_lz77(buf: bytes):
    """GBA BIOS SWI 0x11 LZ77 头：`10 XX XX XX` (size u24 LE)；过滤合理 size"""
    out = []
    i = 0
    while i < len(buf) - 4:
        if buf[i] == 0x10:
            size = buf[i+1] | (buf[i+2] << 8) | (buf[i+3] << 16)
            if 64 <= size <= 2_000_000:
                out.append((i, size))
        i += 1
    return out


def scan_huffman(buf: bytes):
    """GBA SWI 0x13 Huffman 头：`20/24/28 XX XX XX`"""
    out = []
    i = 0
    while i < len(buf) - 4:
        magic = buf[i]
        if magic in (0x20, 0x24, 0x28):
            size = buf[i+1] | (buf[i+2] << 8) | (buf[i+3] << 16)
            if 64 <= size <= 2_000_000:
                out.append((i, magic, size))
        i += 1
    return out


NNS_SIGS = {
    b"RGCN": "NCGR (tile)",
    b"RLCN": "NCLR (palette)",
    b"RECN": "NCER (sprite cell)",
    b"RNAN": "NANR (anim)",
    b"RCSN": "NSCR (screen/tilemap)",
    b"TNFR": "NFTR (font)",
    b"RAMN": "NMAR (multi-anim)",
}


def scan_nns(buf: bytes):
    out = []
    for sig, label in NNS_SIGS.items():
        i = 0
        while True:
            idx = buf.find(sig, i)
            if idx < 0: break
            # 合理性：sig 后 u16 BOM 应为 0xFEFF 或 0xFFFE
            if idx + 6 <= len(buf):
                bom = buf[idx+4] | (buf[idx+5] << 8)
                if bom in (0xFEFF, 0xFFFE):
                    out.append((idx, label))
            i = idx + 1
    out.sort()
    return out


def scan_ascii_strings(buf: bytes, min_len: int = 6):
    out = []
    i = 0
    while i < len(buf):
        b = buf[i]
        if 0x20 <= b < 0x7F:
            j = i
            while j < len(buf) and 0x20 <= buf[j] < 0x7F:
                j += 1
            if j - i >= min_len:
                s = buf[i:j].decode("ascii", errors="replace")
                out.append((i, s))
            i = j
        else:
            i += 1
    return out


def scan_u32_pointers(buf: bytes, region_start: int, region_end: int):
    """连续 u32 LE 形如 0x08/0x09 XX XX XX（ROM 指针）聚簇"""
    ptr_hits = []
    for i in range(0, len(buf) - 3, 4):
        v = struct.unpack_from("<I", buf, i)[0]
        if 0x08000000 <= v < 0x0A000000:
            ptr_hits.append((i, v))
    # 聚类：连续 ≥ 3 个都命中 = 指针表
    clusters = []
    cur = []
    last_i = -4
    for i, v in ptr_hits:
        if i == last_i + 4:
            cur.append((i, v))
        else:
            if len(cur) >= 3:
                clusters.append(cur)
            cur = [(i, v)]
        last_i = i
    if len(cur) >= 3:
        clusters.append(cur)
    return clusters


def windowed_stats(buf: bytes):
    rows = []
    for wstart in range(0, len(buf) - WINDOW + 1, STEP):
        w = buf[wstart:wstart + WINDOW]
        rows.append((wstart, shannon_entropy(w), nz_ratio(w)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=lambda x: int(x, 0), default=DEFAULT_START)
    ap.add_argument("--end",   type=lambda x: int(x, 0), default=DEFAULT_END)
    ap.add_argument("--out",   default="doc/temp/scan_region_report.md")
    args = ap.parse_args()

    rom = ROM_PATH.read_bytes()
    start, end = args.start, args.end
    buf = rom[start:end]
    size = len(buf)

    print(f"扫描 0x{start:08X}..0x{end:08X}  ({size:,} B = 0x{size:X})")

    # 1) zero runs
    zeros = scan_zero_runs(buf)
    print(f"\n长零块（≥ 64B）: {len(zeros)} 段")
    for off, L in sorted(zeros, key=lambda x: -x[1])[:10]:
        print(f"  0x{start+off:08X} +0x{L:X}  ({L:,} B)")

    # 2) LZ77
    lz = scan_lz77(buf)
    print(f"\nLZ77 候选 (`10` magic + 合理 size): {len(lz)} 处")
    for off, sz in lz[:10]:
        print(f"  0x{start+off:08X}  decompressed size = 0x{sz:X} ({sz:,} B)")

    # 3) Huffman
    huf = scan_huffman(buf)
    print(f"\nHuffman 候选 (`20/24/28`): {len(huf)} 处")
    for off, m, sz in huf[:10]:
        print(f"  0x{start+off:08X}  magic=0x{m:02X}  size=0x{sz:X}")

    # 4) NNS
    nns = scan_nns(buf)
    print(f"\nNNS 容器: {len(nns)} 处")
    for off, label in nns[:10]:
        print(f"  0x{start+off:08X}  {label}")

    # 5) ASCII
    strs = scan_ascii_strings(buf, min_len=6)
    print(f"\nASCII 串（≥ 6 字符）: {len(strs)} 条")
    for off, s in strs[:15]:
        print(f"  0x{start+off:08X}  {s[:60]!r}")

    # 6) u32 pointer clusters
    clusters = scan_u32_pointers(buf, start, end)
    print(f"\nu32 ROM 指针簇（连续 ≥ 3 条）: {len(clusters)} 簇")
    for c in clusters[:8]:
        s = c[0][0]; e = c[-1][0]
        pts = [f"0x{v:08X}" for _, v in c[:4]]
        print(f"  0x{start+s:08X}..0x{start+e:08X}  {len(c)} 条:  {', '.join(pts)}{'...' if len(c)>4 else ''}")

    # 7) windowed entropy / nz
    rows = windowed_stats(buf)
    # 摘要：high-entropy / low-entropy 区间
    print(f"\n滑窗统计（窗 {WINDOW}B, 步 {STEP}B）: {len(rows)} 个窗口")
    # 分类：H>7 (compressed/tile)  |  H 3-5 (table)  |  H<3 (sparse)
    bins = {'压缩/tile (H>7)': 0, '中熵 (5<H≤7)': 0, '表/代码 (3<H≤5)': 0, '稀疏 (H≤3)': 0}
    for _, H, _ in rows:
        if H > 7:   bins['压缩/tile (H>7)'] += 1
        elif H > 5: bins['中熵 (5<H≤7)'] += 1
        elif H > 3: bins['表/代码 (3<H≤5)'] += 1
        else:       bins['稀疏 (H≤3)'] += 1
    print("  熵分布:")
    for k, v in bins.items():
        pct = 100*v/len(rows)
        bar = '█' * int(pct/2)
        print(f"    {k:<20} {v:>4} 窗 ({pct:4.1f}%) {bar}")

    # 输出 CSV 供画图/后续分析
    out_csv = Path(args.out).with_suffix('.csv')
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, 'w', encoding='utf-8') as f:
        f.write('window_start_rom,entropy,nz_ratio\n')
        for off, H, nz in rows:
            f.write(f'0x{start+off:08X},{H:.4f},{nz:.4f}\n')
    print(f'\n滑窗 CSV: {out_csv}')

    # 输出完整报告 markdown
    out_md = Path(args.out)
    lines = [f'# ROM 0x{start:08X}..0x{end:08X} 扫描报告',
             f'\n扫描 {size:,} B（0x{size:X}）  窗 {WINDOW}B 步 {STEP}B',
             f'\n## 长零块（≥ 64 B）: {len(zeros)}\n']
    for off, L in zeros:
        lines.append(f'- 0x{start+off:08X} +0x{L:X}  ({L:,} B)')
    lines.append(f'\n## LZ77 候选: {len(lz)}\n')
    for off, sz in lz:
        lines.append(f'- 0x{start+off:08X}  decompressed=0x{sz:X} ({sz:,})')
    lines.append(f'\n## Huffman 候选: {len(huf)}\n')
    for off, m, sz in huf:
        lines.append(f'- 0x{start+off:08X}  magic=0x{m:02X}  size=0x{sz:X}')
    lines.append(f'\n## NNS: {len(nns)}\n')
    for off, label in nns:
        lines.append(f'- 0x{start+off:08X}  {label}')
    lines.append(f'\n## ASCII 串（≥ 6）: {len(strs)}\n')
    for off, s in strs:
        lines.append(f'- 0x{start+off:08X}  `{s}`')
    lines.append(f'\n## u32 指针簇: {len(clusters)}\n')
    for c in clusters:
        s = c[0][0]; e = c[-1][0]
        ptrs = ', '.join(f'0x{v:08X}' for _, v in c[:6])
        tail = '...' if len(c) > 6 else ''
        lines.append(f'- 0x{start+s:08X}..0x{start+e:08X}  {len(c)} 条:  {ptrs}{tail}')
    lines.append(f'\n## 滑窗熵分布\n')
    for k, v in bins.items():
        lines.append(f'- {k}: {v} 窗 ({100*v/len(rows):.1f}%)')
    lines.append(f'\nCSV（地址/熵/nz-ratio）: `{out_csv}`')
    out_md.write_text('\n'.join(lines), encoding='utf-8')
    print(f'完整报告: {out_md}')


if __name__ == "__main__":
    main()
