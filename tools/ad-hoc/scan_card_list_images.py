#!/usr/bin/env python3
"""
扫描 0x01000000..0x01463480 的 2054 个 2240 B entry，为每个 entry 计算：
- byte 直方图的熵
- 非零字节比例
- 唯一字节数
- 最高频字节及其比例

用于：
1. 判定 UI 字体 entry 与卡图 entry 的统计差异 → 确认 UI 占用多少 entry（P2-5）
2. 为 P2-3 映射验证和 P2-4 导出做基础数据
"""

import os, struct, math

ROM_PATH = 'roms/2343.gba'
BASE = 0x01000000
STRIDE = 2240
COUNT = 2054


def entropy(hist, n):
    e = 0.0
    for v in hist:
        if v == 0:
            continue
        p = v / n
        e -= p * math.log2(p)
    return e


def main():
    script = os.path.dirname(os.path.abspath(__file__))
    proj = os.path.dirname(os.path.dirname(script))
    os.chdir(proj)
    rom = open(ROM_PATH, 'rb').read()

    print(f'{"idx":>4} {"nzratio":>7} {"uniq":>4} {"top_b":>5} {"top_p":>5} {"H":>6}')
    rows = []
    for i in range(COUNT):
        off = BASE + i * STRIDE
        data = rom[off:off + STRIDE]
        hist = [0] * 256
        for b in data:
            hist[b] += 1
        n = len(data)
        nz = sum(1 for b in data if b)
        uniq = sum(1 for v in hist if v)
        top_byte = max(range(256), key=lambda k: hist[k])
        top_p = hist[top_byte] / n
        H = entropy(hist, n)
        rows.append((i, nz / n, uniq, top_byte, top_p, H))

    # 打印前 50 和后 50，以及熵最低的 100 项
    print('--- 前 50 ---')
    for r in rows[:50]:
        print(f'{r[0]:>4} {r[1]:7.3f} {r[2]:>4} 0x{r[3]:02x} {r[4]:5.2f} {r[5]:6.2f}')

    print('\n--- 熵最低前 30（疑似 UI / 简单图形）---')
    low = sorted(rows, key=lambda r: r[5])[:30]
    for r in low:
        print(f'{r[0]:>4} {r[1]:7.3f} {r[2]:>4} 0x{r[3]:02x} {r[4]:5.2f} {r[5]:6.2f}')

    # 统计熵分布
    import statistics
    Hs = [r[5] for r in rows]
    print('\n=== 熵分布 ===')
    print(f'  min={min(Hs):.2f}  max={max(Hs):.2f}  mean={statistics.mean(Hs):.2f}  median={statistics.median(Hs):.2f}')

    # 检测连续 UI 段：从 idx=0 起，寻找"熵 < 阈值"的连续前缀
    threshold = 5.0  # 典型卡图熵 > 6
    prefix_end = 0
    for i, r in enumerate(rows):
        if r[5] < threshold:
            prefix_end = i + 1
        else:
            break
    print(f'\n熵阈值 {threshold} 下连续低熵前缀长度 = {prefix_end} 个 entry')


if __name__ == '__main__':
    main()
