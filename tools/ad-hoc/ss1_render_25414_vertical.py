"""FUN08101068_obj_01E25414 按 1×10 竖直长条渲染（4bpp）。"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()
png_dir = ROOT / "graphics/images/ui-misc"


def subpal_16(palram, bank, sub):
    base = 0 if bank == "bg" else 0x200
    off = base + sub * 32
    pal = []
    for c in range(16):
        raw = struct.unpack_from('<H', palram, off + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        pal.append((r, g, b, a))
    return pal


def render_vertical(rom, off, n, pal):
    """1 × n 竖直长条：每 tile 8×8，依次 stack 成 8 × (8n)。"""
    img = Image.new("RGBA", (8, n * 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n):
        for y in range(8):
            for x in range(4):
                byte = rom[off + t * 32 + y * 4 + x]
                px[x * 2,     t * 8 + y] = pal[byte & 0xF]
                px[x * 2 + 1, t * 8 + y] = pal[(byte >> 4) & 0xF]
    return img


# 试多个调色板
for sub in [8, 9, 10, 11, 0, 15]:
    pal = subpal_16(palram_s0, "obj", sub)
    img = render_vertical(ROM, 0x01E25414, 10, pal)
    img = img.resize((img.width * 8, img.height * 8), Image.NEAREST)
    img.save(png_dir / f"FUN08101068_obj_01E25414__V_pb{sub:X}.png")

# 用 pb9 作主版
pal = subpal_16(palram_s0, "obj", 9)
img = render_vertical(ROM, 0x01E25414, 10, pal)
img = img.resize((img.width * 8, img.height * 8), Image.NEAREST)
img.save(png_dir / "FUN08101068_obj_01E25414.png")
print("[+] 1×10 vertical strip, main PNG using pb9")
