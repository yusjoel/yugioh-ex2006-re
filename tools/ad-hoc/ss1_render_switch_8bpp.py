"""按 8bpp 解码 switch sheet 的 items（每 item 0x100 B = 4 × 64B tile = 16×16 px）。
对比 4bpp：每 item 4×2 → 32×16 px。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()

png_dir = ROOT / "graphics/images/ui-misc/switch_sheets"
png_dir.mkdir(parents=True, exist_ok=True)


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


def render_8bpp_tile(rom, off, pal, img, ox, oy):
    px = img.load()
    for y in range(8):
        for x in range(8):
            byte = rom[off + y * 8 + x]
            px[ox + x, oy + y] = pal[byte]


def render_case_8bpp(rom, item_base, n_items, tile_cols, tile_rows, pal, items_per_row=16, gap=4):
    """每 item = tile_cols × tile_rows tile（8bpp）。"""
    item_w = tile_cols * 8
    item_h = tile_rows * 8
    ipr = min(n_items, items_per_row)
    grows = (n_items + ipr - 1) // ipr
    img_w = ipr * (item_w + gap) - gap
    img_h = grows * (item_h + gap) - gap
    img = Image.new("RGBA", (img_w, img_h), (40, 40, 40, 255))
    for i in range(n_items):
        gc, gr = i % ipr, i // ipr
        item_off = item_base + i * 0x100
        ox = gc * (item_w + gap)
        oy = gr * (item_h + gap)
        for t_idx in range(tile_cols * tile_rows):
            tc, tr = t_idx % tile_cols, t_idx // tile_cols
            render_8bpp_tile(rom, item_off + t_idx * 64, pal, img,
                             ox + tc * 8, oy + tr * 8)
    return img


CASES = [
    ("0", 0x01E265B4,  5),
    ("1", 0x01E26AB4,  6),
    ("2", 0x01E270B4, 11),
    ("3", 0x01E27BB4,  5),
    ("4", 0x01E280B4,  9),
    ("5", 0x01E289B4,  4),
    ("6", 0x01E28DB4, 10),
    ("a", 0x01E297B4, 10),
    ("7", 0x01E2A1B4, 22),
    ("b", 0x01E2B7B4, 22),
    ("8", 0x01E2CDB4,  8),
    ("c", 0x01E2D5B4,  8),
    ("9", 0x01E2DDB4,  8),
]

pal_obj = full_256_pal(palram_s0, "obj")
pal_bg = full_256_pal(palram_s0, "bg")

for case_tag, rom_start, n_items in CASES:
    # 8bpp: 每 item 4 tiles, 试 2×2 / 4×1 / 1×4
    for layout_tag, tc, tr in [("2x2", 2, 2), ("4x1", 4, 1), ("1x4", 1, 4)]:
        for pal_tag, pal in [("obj", pal_obj), ("bg", pal_bg)]:
            img = render_case_8bpp(ROM, rom_start, n_items, tc, tr, pal)
            img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
            img.save(png_dir / f"case_{case_tag}__8bpp_{layout_tag}_{pal_tag}.png")
    print(f"[+] case_{case_tag} 8bpp variants")
