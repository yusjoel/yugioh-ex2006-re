#!/usr/bin/env python3
"""
检查 0x01000000 区单 entry 的原始字节结构。
用法：python dump_card_list_entry.py <index>
"""
import os, sys, struct

ROM_PATH = 'roms/2343.gba'
BASE = 0x01000000
STRIDE = 2240


def main():
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    script = os.path.dirname(os.path.abspath(__file__))
    proj = os.path.dirname(os.path.dirname(script))
    os.chdir(proj)
    rom = open(ROM_PATH, 'rb').read()
    off = BASE + idx * STRIDE
    print(f'idx={idx}  ROM @ 0x{off:08X}..0x{off+STRIDE:08X}  stride={STRIDE}')

    data = rom[off:off + STRIDE]

    # 首 16 行 × 16 字节
    print('\n前 16 行:')
    for r in range(16):
        hexs = ' '.join(f'{b:02x}' for b in data[r*16:(r+1)*16])
        print(f'  +{r*16:04x}: {hexs}')

    # 按 64 B tile 拆分：5 × 7 = 35 tiles (不是 40*56 = 2240)
    # 但 2240 / 64 = 35 tiles ✓
    print(f'\ntile count (64 B tiles): {STRIDE // 64}')

    # 如果是 5×7 tile 网格且每 tile 8×8 8bpp：
    # 2240 = 5 * 7 * 64 = 2240 ✓
    # 所以布局是 5 tile 宽 × 7 tile 高 = 40×56 像素

    # 看是否有 header / 前 N 字节存调色板之类
    # 尾部字节
    print('\n末 64 字节:')
    tail = data[-64:]
    for r in range(4):
        hexs = ' '.join(f'{b:02x}' for b in tail[r*16:(r+1)*16])
        print(f'  +{STRIDE-64+r*16:04x}: {hexs}')

    # 字节频率
    hist = [0] * 256
    for b in data:
        hist[b] += 1
    nonzero = [(i, h) for i, h in enumerate(hist) if h > 0]
    nonzero.sort(key=lambda x: -x[1])
    print(f'\n最高频 16 字节：')
    for i, h in nonzero[:16]:
        print(f'  0x{i:02x}: {h} ({h/STRIDE*100:.1f}%)')


if __name__ == '__main__':
    main()
