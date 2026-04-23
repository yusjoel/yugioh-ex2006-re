"""导出 FUN_08109788 的 13 个 switch case sheet。

每个 case 的地址 + 到下一个 case 的 stride 可推出 item 数：
  case X 的 items 数 = (next_case - this_case) / 0x100
  每 item = 0x100 字节 = 8 tiles (4bpp)

Case 9 是最后一个，stride 未知，暂按 8 items 导出（与邻居 case 8/c 同规模）。

输出：
  graphics/bin/ui-misc/switch_sheets/case_X_0x01E2xxxx.bin   (每 case 完整 raw)
  graphics/images/ui-misc/switch_sheets/case_X__4x2.png     (4×2 item 布局)
  graphics/images/ui-misc/switch_sheets/case_X__2x4.png     (2×4 item 布局)
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()

bin_dir = ROOT / "graphics/bin/ui-misc/switch_sheets"
png_dir = ROOT / "graphics/images/ui-misc/switch_sheets"
bin_dir.mkdir(parents=True, exist_ok=True)
png_dir.mkdir(parents=True, exist_ok=True)

# (case_tag, rom_start, item_count) —— item_count 由 stride / 0x100 得
CASES = [
    ("0", 0x01E265B4,  5),    # 0x500
    ("1", 0x01E26AB4,  6),    # 0x600
    ("2", 0x01E270B4, 11),    # 0xB00
    ("3", 0x01E27BB4,  5),    # 0x500
    ("4", 0x01E280B4,  9),    # 0x900
    ("5", 0x01E289B4,  4),    # 0x400
    ("6", 0x01E28DB4, 10),    # 0xA00
    ("a", 0x01E297B4, 10),    # 0xA00
    ("7", 0x01E2A1B4, 22),    # 0x1600
    ("b", 0x01E2B7B4, 22),    # 0x1600
    ("8", 0x01E2CDB4,  8),    # 0x800
    ("c", 0x01E2D5B4,  8),    # 0x800
    ("9", 0x01E2DDB4, 33),    # 确认真实边界：item 33 起字节分布断裂为 FF-dominant 非 sprite
]


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


def render_tile(rom, off, pal, img, ox, oy):
    px = img.load()
    for y in range(8):
        for x in range(4):
            byte = rom[off + y * 4 + x]
            px[ox + x * 2,     oy + y] = pal[byte & 0xF]
            px[ox + x * 2 + 1, oy + y] = pal[(byte >> 4) & 0xF]


def render_case_as_grid(rom, item_base, n_items, tile_cols, tile_rows, pal, item_gap=4):
    """每 item = tile_cols × tile_rows tile。items 横向排列，item 之间 gap 像素。"""
    item_w = tile_cols * 8
    item_h = tile_rows * 8
    # 横向排列（若 item 太多则折行）
    items_per_row = min(n_items, 16)
    grid_rows = (n_items + items_per_row - 1) // items_per_row
    img_w = items_per_row * (item_w + item_gap) - item_gap
    img_h = grid_rows * (item_h + item_gap) - item_gap
    img = Image.new("RGBA", (img_w, img_h), (40, 40, 40, 255))
    for i in range(n_items):
        gc, gr = i % items_per_row, i // items_per_row
        item_off = item_base + i * 0x100
        ox = gc * (item_w + item_gap)
        oy = gr * (item_h + item_gap)
        for t_idx in range(tile_cols * tile_rows):
            tc, tr = t_idx % tile_cols, t_idx // tile_cols
            tile_off = item_off + t_idx * 32
            render_tile(rom, tile_off, pal, img,
                        ox + tc * 8, oy + tr * 8)
    return img


# 尝试多套调色板
palettes = {
    "pb8": subpal_16(palram_s0, "obj", 8),
    "pb9": subpal_16(palram_s0, "obj", 9),
    "pb10": subpal_16(palram_s0, "obj", 10),
    "pb11": subpal_16(palram_s0, "obj", 11),
    "pb15": subpal_16(palram_s0, "obj", 15),
    "pbBG2": subpal_16(palram_s0, "bg", 2),
    "pbBG10": subpal_16(palram_s0, "bg", 10),
}

for case_tag, rom_start, n_items in CASES:
    total_bytes = n_items * 0x100
    raw = ROM[rom_start:rom_start + total_bytes]
    (bin_dir / f"case_{case_tag}_0x{rom_start:08X}.bin").write_bytes(raw)
    # 4×2 item 布局（每 item 32×16 px）
    for pal_tag, pal in palettes.items():
        img_42 = render_case_as_grid(ROM, rom_start, n_items, 4, 2, pal)
        img_42 = img_42.resize((img_42.width * 3, img_42.height * 3), Image.NEAREST)
        img_42.save(png_dir / f"case_{case_tag}__4x2__{pal_tag}.png")
        # 2×4
        img_24 = render_case_as_grid(ROM, rom_start, n_items, 2, 4, pal)
        img_24 = img_24.resize((img_24.width * 3, img_24.height * 3), Image.NEAREST)
        img_24.save(png_dir / f"case_{case_tag}__2x4__{pal_tag}.png")
    print(f"[+] case_{case_tag}: 0x{rom_start:08X} + {total_bytes} B ({n_items} items)")

print(f"\nbin → {bin_dir}")
print(f"png → {png_dir}")
