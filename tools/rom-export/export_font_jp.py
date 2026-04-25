"""
导出《游戏王 EX2006》(BY6E) 日文双字节字库（4 个 charset 变体）。

== 数据结构（2026-04-25 调查结果）==

4 个 charset 是同一字符集的 4 个渲染变体（main 主字形 + outline 描边层，各 small/large 两种字号）。
所有变体均含精确 1925 个 glyph，按相同 index 一一对应（实际渲染时 outline+main 双层叠加）。

| Charset            | GBA 地址      | Stride | 几何      | 角色                  |
|--------------------|---------------|--------|-----------|-----------------------|
| main_small (10×10) | 0x09BAC9A4    | 100 B  | 192500 B  | narrow main 主字形    |
| outline_small (12) | 0x09BDB998    | 144 B  | 277200 B  | wide outline 描边     |
| main_large (12×12) | 0x09C2B7EC    | 144 B  | 277200 B  | narrow main 大号      |
| outline_large (14) | 0x09C6F2BC    | 196 B  | 377300 B  | wide outline 大号     |

**格式**：8bpp 预解码（每像素 1 字节，值 0/1），无 packing 无 header；stride = w × h。

**索引**：FUN_080F0188 (char_code_to_glyph_index) 把 16-bit char_code 转 11-bit index：
 - code > 0xEFFF (XX 自定义编码)：(hi & 0xF) << 7 | (lo & 0x7F)
 - code ≤ 0xEFFF (Shift_JIS)    ：二分查找 font_jp_sjis_lookup_table[1925]

**渲染**：FUN_080F1884 (render_glyph_jp_dual_layer) 按 char hi-bit + ctx flag bit1
查 font_jp_charset_table[(hi << 1) | flag1] 选 (base, stride)，8bpp 预解码 strb 到 OBJ tile。

**验证**：cid=1 青眼の白龍 XX 字节 F8F7/F48C/F1A9/FBD9/FE91 → glyph 1143/524/169/1497/1809
（见 doc/temp/font_charsets/blue_eyes_white_dragon_all4.png）

输出：
  - graphics/bin/font-jp/{main,outline}_{small,large}.bin   （4 × charset 原始字节）
  - graphics/images/font-jp/{main,outline}_{small,large}_preview.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

ROM_PATH = Path("roms/2343.gba")
NUM_GLYPHS = 1925

# (name, gba_addr, w, h)
CHARSETS = [
    ("main_small",    0x09BAC9A4, 10, 10),
    ("main_large",    0x09C2B7EC, 12, 12),
    ("outline_small", 0x09BDB998, 12, 12),
    ("outline_large", 0x09C6F2BC, 14, 14),
]

BIN_DIR = Path("graphics/bin/font-jp")
IMG_DIR = Path("graphics/images/font-jp")

PREVIEW_COLS = 32  # 32 列 × ~61 行 = 1952 槽 (>1925)
BG = (40, 40, 50)
FG = (240, 240, 240)


def render_preview(data: bytes, w: int, h: int, count: int) -> Image.Image:
    cell_w = w + 1
    cell_h = h + 1
    rows = (count + PREVIEW_COLS - 1) // PREVIEW_COLS
    img = Image.new("RGB", (PREVIEW_COLS * cell_w + 1, rows * cell_h + 1), BG)
    px = img.load()
    glyph_size = w * h
    for i in range(count):
        gx = (i % PREVIEW_COLS) * cell_w + 1
        gy = (i // PREVIEW_COLS) * cell_h + 1
        base = i * glyph_size
        for y in range(h):
            row_base = base + y * w
            for x in range(w):
                if data[row_base + x] != 0:
                    px[gx + x, gy + y] = FG
    return img


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()

    if not ROM_PATH.exists():
        print(f"ERROR: ROM not found at {ROM_PATH}", file=sys.stderr)
        return 1

    rom = ROM_PATH.read_bytes()

    BIN_DIR.mkdir(parents=True, exist_ok=True)
    if not args.no_png:
        IMG_DIR.mkdir(parents=True, exist_ok=True)

    for name, gba, w, h in CHARSETS:
        off = gba - 0x08000000
        size = w * h * NUM_GLYPHS
        data = rom[off:off + size]
        assert len(data) == size, f"{name}: got {len(data)} B, expected {size}"

        bin_path = BIN_DIR / f"{name}.bin"
        bin_path.write_bytes(data)
        print(f"写入 {bin_path} ({len(data)} B = {NUM_GLYPHS} × {w}×{h})")

        if not args.no_png:
            img = render_preview(data, w, h, NUM_GLYPHS)
            png_path = IMG_DIR / f"{name}_preview.png"
            img.save(png_path)
            print(f"写入 {png_path} ({img.size[0]}×{img.size[1]})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
