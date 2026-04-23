"""根据 asm/all.s 里的代码引用，导出代码明确使用的 UI sheet + palette。

每块都独立验证：
  - 起点 = 代码里 DAT_ 指针地址
  - 长度 = 代码里 tile_2d_row_copy / FUN_080f4ea4 的 size 参数 +
           循环迭代次数 × 单次 size
  - 边界对齐到下一个 DAT_ 指针

只导 "code 明确引用" 的段，不包括推测。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

# 统一使用 card-mini-frame-palette 第 1 子调色板渲染（已知 ROM 0x01E31554, 16 色）
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


def render_4bpp_sheet(rom, off, n_tiles, pal, cols):
    rows = (n_tiles + cols - 1) // cols
    img = Image.new("RGBA", (cols * 8, rows * 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n_tiles):
        c, r = t % cols, t // cols
        for y in range(8):
            for x in range(4):
                byte = rom[off + t * 32 + y * 4 + x]
                px[c * 8 + x * 2,     r * 8 + y] = pal[byte & 0xF]
                px[c * 8 + x * 2 + 1, r * 8 + y] = pal[(byte >> 4) & 0xF]
    return img


def render_palette_strip(rom, off, n_colors):
    img = Image.new("RGBA", (n_colors * 16, 16), (0, 0, 0, 0))
    px = img.load()
    for c in range(n_colors):
        raw = struct.unpack_from('<H', rom, off + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        for y in range(16):
            for x in range(16):
                px[c * 16 + x, y] = (r, g, b, 255)
    return img


bin_dir = ROOT / "graphics/bin/ui-misc"
png_dir = ROOT / "graphics/images/ui-misc"
bin_dir.mkdir(parents=True, exist_ok=True)
png_dir.mkdir(parents=True, exist_ok=True)

# === 通用调色板 ===
# pb10 (BG)/pb8 (OBJ) 都用 card-mini-frame-palette[0] = ROM 0x01E31554
pal_main = read_subpal(ROM, 0x01E31554)
# pb9 用 ROM 0x01E31574
pal_pb9 = read_subpal(ROM, 0x01E31574)
# pb11 用 ROM 0x01E31594
pal_pb11 = read_subpal(ROM, 0x01E31594)

# === Export 1: FUN_08101068 完整 HUD sheet (ROM 0x01E246D4..0x01E25554) ===
# 含 BG 前段 (0x01E246D4..0x01E24CF4, 49 tiles) + OBJ 尾段 (0x01E24CF4..0x01E25554, 67 tiles)
# 总共 116 tiles / 3712 B

blocks = [
    # (name, rom_off, n_tiles, cols, pal_for_preview, subsection, comment)
    # FUN_08101068 -- BG tile 组
    ("FUN08101068_bg_01E246D4",  0x01E246D4,  7, 7,  pal_main,  "bg",  "dest BG 0x0600C3A0 (FUN_08101068 #6)"),
    ("FUN08101068_bg_01E247B4",  0x01E247B4,  4, 4,  pal_main,  "bg",  "dest BG 0x0600C480 (FUN_08101068 #7)"),
    ("FUN08101068_bg_01E24834",  0x01E24834,  8, 8,  pal_main,  "bg",  "dest BG 0x0600C500 (FUN_08101068 #8)"),
    ("FUN08101068_bg_01E24934",  0x01E24934, 14, 7,  pal_main,  "bg",  "dest BG 0x0600C040 (FUN_08101068 #1, 同源亦拷 OBJ)"),
    ("FUN08101068_bg_01E24AF4",  0x01E24AF4, 13, 13, pal_main,  "bg",  "dest BG 0x0600C200 (FUN_08101068 #3, BG 13/16 tile)"),
    # FUN_08101068 -- OBJ tile 组（部分与 BG 复用起点）
    ("FUN08101068_obj_01E24CF4", 0x01E24CF4, 16, 8,  pal_pb9,   "obj", "dest OBJ 0x06016C00 (#12)"),
    ("FUN08101068_obj_01E24EF4", 0x01E24EF4, 16, 8,  pal_pb9,   "obj", "dest OBJ 0x06017000 (#13)"),
    ("FUN08101068_obj_01E250F4", 0x01E250F4, 16, 8,  pal_pb9,   "obj", "dest OBJ 0x06017400 (#14)"),
    ("FUN08101068_obj_01E252F4", 0x01E252F4,  9, 9,  pal_pb9,   "obj", "dest OBJ 0x06017800 (#15)"),
    ("FUN08101068_obj_01E25414", 0x01E25414, 10, 10, pal_pb9,   "obj", "dest OBJ 0x06017C00 (#16)"),
    # FUN_081016c0 -- state=1 subset
    ("FUN081016c0_s1_small_01E25674", 0x01E25674, 22, 11, pal_pb11, "obj",
     "11 iter × 2 tiles, dest OBJ 0x060162A0+"),
    ("FUN081016c0_s1_big_01E25934",   0x01E25934, 24, 12, pal_pb11, "obj",
     "(0xC, 2) = 24 tiles, dest OBJ 0x06016A80"),
    # FUN_081016c0 -- state=3
    ("FUN081016c0_s3_01E25C34",       0x01E25C34, 24, 12, pal_pb11, "obj",
     "6 iter × 4 tiles, dest OBJ 0x06016A80+"),
    # FUN_081066fc
    ("FUN081066fc_obj_01E310B4",      0x01E310B4, 16, 8,  pal_main,  "obj",
     "(0x8, 2) = 16 tiles, dest OBJ 0x06016300"),
]

print("=== 导出 tile 块 ===")
for name, rom_off, n_tiles, cols, pal, kind, comment in blocks:
    size = n_tiles * 32
    raw = ROM[rom_off:rom_off + size]
    bin_path = bin_dir / f"{name}.bin"
    bin_path.write_bytes(raw)
    img = render_4bpp_sheet(ROM, rom_off, n_tiles, pal, cols)
    img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    img.save(png_dir / f"{name}.png")
    print(f"  [+] {name}: 0x{rom_off:08X} + {size} B ({n_tiles} tiles {kind})  // {comment}")

# === Export 2: 调色板块（UNKNOWN seg 0x01E31714 内） ===
palettes = [
    ("FUN081058c8_anim_pal_01E31754", 0x01E31754, 16, "动画调色板（rows 11-14 帧循环）"),
    ("FUN081066fc_obj_pal_01E31794",  0x01E31794, 16, "OBJ pb8 单 subpal"),
]
print("\n=== 导出 palette 块 ===")
for name, off, n_colors, comment in palettes:
    raw = ROM[off:off + n_colors * 2]
    bin_path = bin_dir / f"{name}.bin"
    bin_path.write_bytes(raw)
    img = render_palette_strip(ROM, off, n_colors)
    img.save(png_dir / f"{name}.png")
    print(f"  [+] {name}: 0x{off:08X} + {n_colors * 2} B  // {comment}")

# === 额外 1：把 HUD sheet 作为 "整块合并" bin 也导一份（方便后续 .incbin 替换）
hud_full_raw = ROM[0x01E246D4:0x01E25554]
(bin_dir / "_MERGED_HUD_sheet_01E246D4_01E25554.bin").write_bytes(hud_full_raw)
print(f"\n[+] MERGED: 0x01E246D4-0x01E25554, {len(hud_full_raw)} B")

# === 额外 2：一张 "全 HUD sheet 连续展示图"（116 tiles, 16 列）
img_full = render_4bpp_sheet(ROM, 0x01E246D4, 116, pal_main, 16)
img_full = img_full.resize((img_full.width * 4, img_full.height * 4), Image.NEAREST)
img_full.save(png_dir / "_ALL_HUD_sheet_preview.png")
print(f"[+] preview png: _ALL_HUD_sheet_preview.png")

# 也用 pb9 / pb11 备份渲染一份
for pb_name, pal in [("pb9", pal_pb9), ("pb11", pal_pb11)]:
    img_alt = render_4bpp_sheet(ROM, 0x01E246D4, 116, pal, 16)
    img_alt = img_alt.resize((img_alt.width * 4, img_alt.height * 4), Image.NEAREST)
    img_alt.save(png_dir / f"_ALL_HUD_sheet_preview_{pb_name}.png")

print(f"\nbin → {bin_dir}")
print(f"png → {png_dir}")
