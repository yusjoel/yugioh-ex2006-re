"""将 FUN08101068_obj_01E25414 恢复为 10×1 长条（代码 tile_2d_row_copy(w=0xA, h=1) 原样）。"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
png_dir = ROOT / "graphics/images/ui-misc"


def read_subpal(rom, off):
    pal = []
    for c in range(16):
        raw = struct.unpack_from('<H', rom, off + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        pal.append((r, g, b, a))
    return pal


def render_row_major(rom, off, n, cols, pal):
    rows = (n + cols - 1) // cols
    img = Image.new("RGBA", (cols * 8, rows * 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n):
        c, r = t % cols, t // cols
        for y in range(8):
            for x in range(4):
                byte = rom[off + t * 32 + y * 4 + x]
                px[c * 8 + x * 2,     r * 8 + y] = pal[byte & 0xF]
                px[c * 8 + x * 2 + 1, r * 8 + y] = pal[(byte >> 4) & 0xF]
    return img


pal_pb9 = read_subpal(ROM, 0x01E31574)
img = render_row_major(ROM, 0x01E25414, 10, 10, pal_pb9)
img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
img.save(png_dir / "FUN08101068_obj_01E25414.png")
print("[+] restored main PNG to 10×1 long strip")
