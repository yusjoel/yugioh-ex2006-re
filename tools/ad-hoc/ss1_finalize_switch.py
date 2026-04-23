"""将 8bpp 2×2 OBJ 渲染定为 switch case 的 canonical PNG，清理变体。"""
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


CASES = [
    ("0", 0x01E265B4,  5, "menu action icons"),
    ("1", 0x01E26AB4,  6, "heart HP counters 1-5 + magnifier"),
    ("2", 0x01E270B4, 11, "misc UI icons (sword/shield/gems/star/seal)"),
    ("3", 0x01E27BB4,  5, "heart-up HP counters 1-5"),
    ("4", 0x01E280B4,  9, "card frame color badges"),
    ("5", 0x01E289B4,  4, "star counter badges (1-4, 5-6, 7+)"),
    ("6", 0x01E28DB4, 10, "ATTRIBUTE icons (DARK/WATER/FIRE/LIGHT/WIND/EARTH/SPELL/TRAP/DIVINE + rainbow)"),
    ("a", 0x01E297B4, 10, "ATTRIBUTE icons (dup of case 6)"),
    ("7", 0x01E2A1B4, 22, "RACE icons 22 款"),
    ("b", 0x01E2B7B4, 22, "RACE icons (dup of case 7)"),
    ("8", 0x01E2CDB4,  8, "brown emblems 8 款"),
    ("c", 0x01E2D5B4,  8, "brown emblems (dup of case 8)"),
    ("9", 0x01E2DDB4, 33, "status/achievement icons 33 款 (扩到 item 32)"),
]


def render_2x2_grid(rom, item_base, n_items, pal, ipr=16, gap=4):
    item_w, item_h = 16, 16
    ipr_actual = min(n_items, ipr)
    grows = (n_items + ipr_actual - 1) // ipr_actual
    img_w = ipr_actual * (item_w + gap) - gap
    img_h = grows * (item_h + gap) - gap
    img = Image.new("RGBA", (img_w, img_h), (40, 40, 40, 255))
    px = img.load()
    for i in range(n_items):
        gc, gr = i % ipr_actual, i // ipr_actual
        item_off = item_base + i * 0x100
        ox = gc * (item_w + gap)
        oy = gr * (item_h + gap)
        for t_idx in range(4):            # 4 tile × 8bpp × 64B = 256B/item
            tc, tr = t_idx % 2, t_idx // 2
            tile_off = item_off + t_idx * 64
            for y in range(8):
                for x in range(8):
                    byte = rom[tile_off + y * 8 + x]
                    px[ox + tc * 8 + x, oy + tr * 8 + y] = pal[byte]
    return img


pal_obj = full_256_pal(palram_s0, "obj")

print("=== 设 canonical PNG 为 8bpp 2×2 OBJ 调色板 ===")
for case_tag, rom_start, n_items, desc in CASES:
    img = render_2x2_grid(ROM, rom_start, n_items, pal_obj)
    img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    img.save(png_dir / f"case_{case_tag}.png")
    print(f"  [+] case_{case_tag}: {n_items} items — {desc}")

# 清理所有非 canonical 变体
removed = 0
for p in png_dir.iterdir():
    if p.name.startswith("case_") and "__" in p.name:
        p.unlink()
        removed += 1
print(f"\n[*] 清理 {removed} 张变体 PNG")
