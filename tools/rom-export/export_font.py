"""
导出《游戏王 EX2006》(BY6E) 英文字库为 PNG 预览 + bin + .s 引用。

== 数据结构（2026-04-15 调查结果，见 doc/dev/p2-font-location-findings.md）==

- **ROM 地址**：`0x09CCCA90`（文件偏移 `0x01CCCA90`）
- **大小**：256 字符 × 8 字节 = 2048 B（结束于 `0x01CCD290`）
- **格式**：1bpp 8×8，MSB-first，行主序；索引 = ASCII 码
- **加载函数**：`FUN_080f1b60` @ `0x080f1b60`
- **VRAM 提交起点**：`0x06010040`（OBJ sprite tile 2）

输出：
  - graphics/bin/font/tiles/font.bin   （2048 B 原始字库）
  - graphics/images/font/font_preview.png  （16×16 grid 字符预览）
  - data/font.s                      （incbin + 全局标签）
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

ROM_PATH = Path("roms/2343.gba")
FONT_ROM_START = 0x01CCCA90
FONT_ROM_END = 0x01CCD290
FONT_SIZE = FONT_ROM_END - FONT_ROM_START  # 0x800 = 2048
NUM_GLYPHS = 256
GLYPH_BYTES = 8  # 1bpp 8×8

BIN_DIR = Path("graphics/bin/font/tiles")
IMG_DIR = Path("graphics/images/font")
BIN_PATH = BIN_DIR / "font.bin"
PNG_PATH = IMG_DIR / "font_preview.png"
S_PATH = Path("data/font.s")


def render_preview(font_bytes: bytes, scale: int = 2) -> Image.Image:
    """渲染 16×16 字形网格预览 PNG。每字符 8×8，放大 scale 倍，外加 1 px 分隔线。"""
    cell = 8 * scale + 1  # 每格宽/高（含右/下分隔）
    W = 16 * cell + 1
    H = 16 * cell + 1
    img = Image.new("L", (W, H), 64)  # 背景深灰
    px = img.load()
    for ci in range(NUM_GLYPHS):
        gx = ci % 16
        gy = ci // 16
        base = ci * GLYPH_BYTES
        for py in range(8):
            b = font_bytes[base + py]
            for pxo in range(8):
                bit = (b >> (7 - pxo)) & 1
                color = 255 if bit else 0
                # 放大 scale 倍
                for dy in range(scale):
                    for dx in range(scale):
                        x = 1 + gx * cell + pxo * scale + dx
                        y = 1 + gy * cell + py * scale + dy
                        px[x, y] = color
    return img


def write_font_s() -> None:
    lines = [
        "@ 英文字库（1bpp 8×8，256 字符，ASCII 直接索引）",
        "@ ROM 范围: 0x01CCCA90 - 0x01CCD290 (2048 B)",
        "@ 加载函数: FUN_080f1b60 @ 0x080f1b60",
        "@ 详见 doc/dev/p2-font-location-findings.md",
        "@ 由 tools/rom-export/export_font.py 自动生成",
        "",
        "    .section .rodata",
        "    .balign 2",
        "    .global font_ascii_8x8",
        "font_ascii_8x8:",
        '    .incbin "graphics/bin/font/tiles/font.bin"',
        "font_ascii_8x8_end:",
        "",
    ]
    S_PATH.parent.mkdir(parents=True, exist_ok=True)
    S_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()

    if not ROM_PATH.exists():
        print(f"ERROR: ROM not found at {ROM_PATH}", file=sys.stderr)
        return 1

    rom = ROM_PATH.read_bytes()
    font = rom[FONT_ROM_START:FONT_ROM_END]
    assert len(font) == FONT_SIZE, f"got {len(font)} B, expected {FONT_SIZE}"

    BIN_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    BIN_PATH.write_bytes(font)
    print(f"写入 {BIN_PATH} ({len(font)} B)")

    if not args.no_png:
        img = render_preview(font, scale=2)
        img.save(PNG_PATH)
        print(f"写入 {PNG_PATH} ({img.size[0]}×{img.size[1]})")

    write_font_s()
    print(f"写入 {S_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
