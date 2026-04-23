"""测试 8bpp 解码 —— 10×32B = 5×64B 8bpp tile，40×8 strip。"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()
png_dir = ROOT / "graphics/images/ui-misc"


def render_8bpp_strip(rom, off, n_tiles, pal):
    """8bpp 每字节 1 像素，每 tile 64B → 8×8 px。"""
    img = Image.new("RGBA", (n_tiles * 8, 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n_tiles):
        for y in range(8):
            for x in range(8):
                byte = rom[off + t * 64 + y * 8 + x]
                px[t * 8 + x, y] = pal[byte]
    return img


def full_256_palette(palram, bank):
    base = 0 if bank == "bg" else 0x200
    pal = []
    for c in range(256):
        raw = struct.unpack_from('<H', palram, base + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        pal.append((r, g, b, a))
    return pal


# 5 tiles × 64B 8bpp，OBJ 调色板（8bpp sprite 用整 256 色 OBJ palram）
pal_obj_256 = full_256_palette(palram_s0, "obj")
pal_bg_256 = full_256_palette(palram_s0, "bg")

img_obj = render_8bpp_strip(ROM, 0x01E25414, 5, pal_obj_256)
img_obj = img_obj.resize((img_obj.width * 8, img_obj.height * 8), Image.NEAREST)
img_obj.save(png_dir / "FUN08101068_obj_01E25414__8bpp_obj_pal.png")

img_bg = render_8bpp_strip(ROM, 0x01E25414, 5, pal_bg_256)
img_bg = img_bg.resize((img_bg.width * 8, img_bg.height * 8), Image.NEAREST)
img_bg.save(png_dir / "FUN08101068_obj_01E25414__8bpp_bg_pal.png")

# 也试 40 tile 横向的 4bpp 版（若宽得多）—— 只是对比
def render_4bpp_strip(rom, off, n, pal):
    img = Image.new("RGBA", (n * 8, 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n):
        for y in range(8):
            for x in range(4):
                byte = rom[off + t * 32 + y * 4 + x]
                px[t * 8 + x * 2,     y] = pal[byte & 0xF]
                px[t * 8 + x * 2 + 1, y] = pal[(byte >> 4) & 0xF]
    return img


# 用 card-mini-frame-palette[0] 作 4bpp 调色板
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


pal_pb9 = subpal_16(palram_s0, "obj", 9)
img_4bpp = render_4bpp_strip(ROM, 0x01E25414, 10, pal_pb9)
img_4bpp = img_4bpp.resize((img_4bpp.width * 8, img_4bpp.height * 8), Image.NEAREST)
img_4bpp.save(png_dir / "FUN08101068_obj_01E25414__4bpp_10x1.png")

print("Rendered 8bpp variants + 4bpp reference")
