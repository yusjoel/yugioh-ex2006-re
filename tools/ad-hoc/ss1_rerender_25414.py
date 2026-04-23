"""重试 FUN08101068_obj_01E25414 的排布。"""
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


def render_col_major(rom, off, n_cols, rows_per_col, pal):
    img = Image.new("RGBA", (n_cols * 8, rows_per_col * 8), (0, 0, 0, 0))
    px = img.load()
    for col in range(n_cols):
        for rr in range(rows_per_col):
            tile_idx = col * rows_per_col + rr
            tile_off = off + tile_idx * 32
            for y in range(8):
                for x in range(4):
                    byte = rom[tile_off + y * 4 + x]
                    px[col * 8 + x * 2,     rr * 8 + y] = pal[byte & 0xF]
                    px[col * 8 + x * 2 + 1, rr * 8 + y] = pal[(byte >> 4) & 0xF]
    return img


pal_pb9 = read_subpal(ROM, 0x01E31574)    # 原来用的调色板
pal_main = read_subpal(ROM, 0x01E31554)

# 变体 A: 5×2 row-major（前 5 top 行，后 5 bot 行）
img_a = render_row_major(ROM, 0x01E25414, 10, 5, pal_pb9)
img_a.resize((img_a.width * 4, img_a.height * 4), Image.NEAREST).save(
    png_dir / "FUN08101068_obj_01E25414__A_5x2_rowmajor.png")

# 变体 B: 5×2 col-major（pair-by-pair 垂直）
img_b = render_col_major(ROM, 0x01E25414, 5, 2, pal_pb9)
img_b.resize((img_b.width * 4, img_b.height * 4), Image.NEAREST).save(
    png_dir / "FUN08101068_obj_01E25414__B_5col_pair.png")

# 变体 C: 2×5 row-major（2 tile 每行，5 行）
img_c = render_row_major(ROM, 0x01E25414, 10, 2, pal_pb9)
img_c.resize((img_c.width * 4, img_c.height * 4), Image.NEAREST).save(
    png_dir / "FUN08101068_obj_01E25414__C_2x5_rowmajor.png")

# 变体 D: 2×5 col-major
img_d = render_col_major(ROM, 0x01E25414, 2, 5, pal_pb9)
img_d.resize((img_d.width * 4, img_d.height * 4), Image.NEAREST).save(
    png_dir / "FUN08101068_obj_01E25414__D_2col_5row.png")

# 变体 E: 10×1 (原版)
img_e = render_row_major(ROM, 0x01E25414, 10, 10, pal_pb9)
img_e.resize((img_e.width * 4, img_e.height * 4), Image.NEAREST).save(
    png_dir / "FUN08101068_obj_01E25414__E_10x1_orig.png")

# 用 main 调色板试一次 5×2 row-major
img_f = render_row_major(ROM, 0x01E25414, 10, 5, pal_main)
img_f.resize((img_f.width * 4, img_f.height * 4), Image.NEAREST).save(
    png_dir / "FUN08101068_obj_01E25414__F_5x2_main_pal.png")

print("Rendered 6 variants: A..F")
