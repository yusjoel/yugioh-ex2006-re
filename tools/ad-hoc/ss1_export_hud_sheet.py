"""导出已识别的 HUD 数字/图标 sheet 到 graphics/bin/ + PNG。

范围：ROM 0x01E246D4 + 3712 B (116 × 32B)，属于 UNKNOWN 段 0x01DFF9D2。
用 s0 BG palette bank 2 渲染（视觉匹配最佳）。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()

ROM_OFF = 0x01E246D4
N_TILES = 116
BYTES = N_TILES * 32


def decode_subpal(palram, bank, subpal):
    base = 0 if bank == "bg" else 0x200
    off = base + subpal * 32
    colors = []
    for c in range(16):
        raw = struct.unpack_from('<H', palram, off + c * 2)[0]
        r = (raw & 0x1F) << 3; g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        colors.append((r, g, b, a))
    return colors


def render_4bpp(rom_off, n_tiles, palette, cols):
    rows = (n_tiles + cols - 1) // cols
    img = Image.new("RGBA", (cols * 8, rows * 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n_tiles):
        c, r = t % cols, t // cols
        for y in range(8):
            for x in range(4):
                byte = ROM[rom_off + t * 32 + y * 4 + x]
                px[c * 8 + x * 2,     r * 8 + y] = palette[byte & 0xF]
                px[c * 8 + x * 2 + 1, r * 8 + y] = palette[(byte >> 4) & 0xF]
    return img


# 导 bin
out_bin = ROOT / "graphics/bin/ui-misc/hud_digits_icons_sheet.bin"
out_bin.parent.mkdir(parents=True, exist_ok=True)
out_bin.write_bytes(ROM[ROM_OFF:ROM_OFF + BYTES])
print(f"[+] wrote {out_bin} ({BYTES} B)")

# 导预览 PNG（pb2 视觉最佳），16 列 × 8 行 tile
pal = decode_subpal(palram_s0, "bg", 2)
img = render_4bpp(ROM_OFF, N_TILES, pal, cols=16)
png_path = ROOT / "graphics/images/ui-misc/hud_digits_icons_sheet.png"
png_path.parent.mkdir(parents=True, exist_ok=True)
# 4x 放大
img.resize((img.width * 4, img.height * 4), Image.NEAREST).save(png_path)
print(f"[+] wrote {png_path}")
