"""渲染 0x01E2DDB4 起 item 28..50 个，看 item 33 处断点视觉表现。"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()

png_dir = ROOT / "graphics/images/ui-misc/switch_sheets"


def full_256_pal(palram, bank):
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


def render_2x2_8bpp(rom, item_off, pal, img, ox, oy):
    px = img.load()
    for t_idx in range(4):
        tc, tr = t_idx % 2, t_idx // 2
        tile_off = item_off + t_idx * 64
        for y in range(8):
            for x in range(8):
                byte = rom[tile_off + y * 8 + x]
                px[ox + tc * 8 + x, oy + tr * 8 + y] = pal[byte]


pal_obj = full_256_pal(palram_s0, "obj")
pal_bg = full_256_pal(palram_s0, "bg")

# item 28..50 = 23 items, 排成 10 col × 3 row (部分)
for pal_tag, pal in [("obj", pal_obj), ("bg", pal_bg)]:
    gap = 4
    cols = 12
    rows = (23 + cols - 1) // cols
    img = Image.new("RGBA", (cols * (16 + gap) - gap, rows * (16 + gap) - gap), (40, 40, 40, 255))
    for i in range(23):
        item_idx = 28 + i
        item_off = 0x01E2DDB4 + item_idx * 0x100
        gc, gr = i % cols, i // cols
        render_2x2_8bpp(ROM, item_off, pal, img, gc * (16 + gap), gr * (16 + gap))
    img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    img.save(png_dir / f"_case9_boundary_items_28-50_{pal_tag}.png")
print("[+] boundary preview written (items 28-50)")
