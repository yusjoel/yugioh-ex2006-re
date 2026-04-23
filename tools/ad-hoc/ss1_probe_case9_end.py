"""扫描 case 9 之后的 ROM 区域，寻找真正的数据断点。

策略：从 0x01E2DDB4 起每 0x100 字节作为一个 item，分析：
  - 非零字节比例（全 0 = 明显是 padding）
  - 字节直方图熵（高熵 = 压缩/扰乱数据；低熵 = 纯图形）
  - 与 case 8/c/a/b 的 item 比对相似度（同结构 = 继续是 case 9 item）
  - 已知结构：item 为 4 × 64B 8bpp tile = 256B

如果找到一个 item 明显"不像 tile"（全 0 / 纯 ASCII / 高熵 随机），就是 case 9 的尾界。
"""
import pathlib
from collections import Counter

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

START = 0x01E2DDB4
NEXT_REF = 0x01E310B4     # 已知下一个代码引用
MAX_ITEMS = (NEXT_REF - START) // 0x100
print(f"[*] 扫描 0x{START:08X}..0x{NEXT_REF:08X}（max {MAX_ITEMS} items）")

print(f"\n{'item':>4} {'addr':>10} {'non0':>4} {'unique':>6} {'top3':>20} {'notes'}")
for i in range(MAX_ITEMS):
    off = START + i * 0x100
    chunk = ROM[off:off + 0x100]
    non0 = sum(1 for b in chunk if b != 0)
    cnt = Counter(chunk)
    top3 = cnt.most_common(3) + [(0, 0)] * 3
    notes = []
    if non0 == 0:
        notes.append("ALL_ZERO")
    elif non0 < 32:
        notes.append("mostly_blank")
    # 典型 8bpp tile 特征：大部分字节是 palette 索引 0-7 区间 + 少数突出点
    low_idx = sum(chunk.count(b) for b in range(16))
    if low_idx / 256 > 0.7:
        notes.append("low_palette_idx")
    print(f"  {i:3d} 0x{off:08X} {non0:3d} {len(cnt):3d}  "
          f"{top3[0][0]:02X}x{top3[0][1]},{top3[1][0]:02X}x{top3[1][1]},{top3[2][0]:02X}x{top3[2][1]}  "
          f"{' '.join(notes)}")
