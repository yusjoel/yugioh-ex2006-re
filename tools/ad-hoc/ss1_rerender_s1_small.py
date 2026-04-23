"""重新渲染 FUN_081016c0 state=1 small block (0x01E25674, 22 tiles)。

代码结构：11 次迭代，每次 tile_2d_row_copy(dst, src=0x01E25674+i*0x40, width=1, height=2)
→ 每次 64 B = 2 tiles 垂直叠放（1 列 × 2 行）。
→ 在 ROM 里相邻两个 tile 是 (top, bot) 垂直对，不是 (left, right) 水平对。

正确排布：11 列 × 2 行，tile_k（k=2*i）= 第 i 列上格，tile_{2*i+1} = 第 i 列下格。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()


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


def render_column_major(rom, off, n_columns, rows_per_col, pal):
    """ROM 里按 (col0_row0, col0_row1, ..., col0_rowN, col1_row0, ...) 储存。"""
    img = Image.new("RGBA", (n_columns * 8, rows_per_col * 8), (0, 0, 0, 0))
    px = img.load()
    for col in range(n_columns):
        for rr in range(rows_per_col):
            tile_idx = col * rows_per_col + rr
            tile_off = off + tile_idx * 32
            for y in range(8):
                for x in range(4):
                    byte = rom[tile_off + y * 4 + x]
                    px[col * 8 + x * 2,     rr * 8 + y] = pal[byte & 0xF]
                    px[col * 8 + x * 2 + 1, rr * 8 + y] = pal[(byte >> 4) & 0xF]
    return img


def render_2x2_per_iter(rom, off, n_iters, pal):
    """每 iter 4 tiles 以 (2 宽 × 2 高) 排（tile_2d_row_copy row-major 内顺序 tl, tr, bl, br）。
    整体排布：n_iters 个 2x2 单元水平铺开 → (2*n_iters) cols × 2 rows。
    """
    img = Image.new("RGBA", (2 * n_iters * 8, 2 * 8), (0, 0, 0, 0))
    px = img.load()
    for it in range(n_iters):
        # tl=it*4+0 (col=0,row=0), tr=it*4+1 (col=1,row=0),
        # bl=it*4+2 (col=0,row=1), br=it*4+3 (col=1,row=1)
        for subtile, (sub_col, sub_row) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
            tile_off = off + (it * 4 + subtile) * 32
            ox = it * 2 * 8 + sub_col * 8
            oy = sub_row * 8
            for y in range(8):
                for x in range(4):
                    byte = rom[tile_off + y * 4 + x]
                    px[ox + x * 2,     oy + y] = pal[byte & 0xF]
                    px[ox + x * 2 + 1, oy + y] = pal[(byte >> 4) & 0xF]
    return img


png_dir = ROOT / "graphics/images/ui-misc"

# palette pb11 = 0x01E31594
pal_pb11 = read_subpal(ROM, 0x01E31594)
pal_main = read_subpal(ROM, 0x01E31554)

# s1_small: 11 iter × (1,2) = 列优先
img = render_column_major(ROM, 0x01E25674, n_columns=11, rows_per_col=2, pal=pal_pb11)
img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
img.save(png_dir / "FUN081016c0_s1_small_01E25674.png")
print("[+] re-rendered s1_small (column-major 11×2)")

# 额外：也用 pb10 主色渲染一份备选
img2 = render_column_major(ROM, 0x01E25674, 11, 2, pal_main)
img2 = img2.resize((img2.width * 4, img2.height * 4), Image.NEAREST)
img2.save(png_dir / "FUN081016c0_s1_small_01E25674_pb10.png")

# s3: 6 iter × (2,2) row-major within iter
img3 = render_2x2_per_iter(ROM, 0x01E25C34, n_iters=6, pal=pal_pb11)
img3 = img3.resize((img3.width * 4, img3.height * 4), Image.NEAREST)
img3.save(png_dir / "FUN081016c0_s3_01E25C34.png")
print("[+] re-rendered s3 (2×2 per iter × 6)")

# s1_big: (0xC, 2) = 12 wide × 2 tall 行优先
def render_row_major_rect(rom, off, w, h, pal):
    img = Image.new("RGBA", (w * 8, h * 8), (0, 0, 0, 0))
    px = img.load()
    for r in range(h):
        for c in range(w):
            tile_idx = r * w + c
            tile_off = off + tile_idx * 32
            for y in range(8):
                for x in range(4):
                    byte = rom[tile_off + y * 4 + x]
                    px[c * 8 + x * 2,     r * 8 + y] = pal[byte & 0xF]
                    px[c * 8 + x * 2 + 1, r * 8 + y] = pal[(byte >> 4) & 0xF]
    return img

img4 = render_row_major_rect(ROM, 0x01E25934, w=12, h=2, pal=pal_pb11)
img4 = img4.resize((img4.width * 4, img4.height * 4), Image.NEAREST)
img4.save(png_dir / "FUN081016c0_s1_big_01E25934.png")
print("[+] re-rendered s1_big (row-major 12×2)")
