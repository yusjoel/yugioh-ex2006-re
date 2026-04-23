"""按 8bpp 解码渲染 runs（每字节 1 像素 → 256 色调色板）。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

RUNS = [
    # tag, rom_off, size_bytes, state, bank, cols_of_tile
    ("segC_A_76tile8bpp",  0x0184A42C, 152 * 32, "s0", "bg", 8),   # 76 × 64B
    ("segC_B_49tile8bpp",  0x0184B9C4,  98 * 32, "s0", "bg", 7),
    ("seg1E_246D4_58t8bpp",0x01E246D4, 116 * 32, "s0", "bg", 8),
    # BG 4bpp 引用 cb2 的 runs 暂不复跑（4bpp 结果已导）
    # OBJ: 试 8bpp
    ("seg1E_293B4_4t8bpp", 0x01E293B4,  8 * 32, "s0", "obj", 4),
    ("seg1E_289B4_6t8bpp", 0x01E289B4, 12 * 32, "s0", "obj", 6),
    ("seg1E_271B4_4t8bpp", 0x01E271B4,  8 * 32, "s0", "obj", 4),
]


def decode_full_palette(palram, bank):
    """整 256 色调色板（8bpp 只有 1 个 palbank = 16*16=256）。"""
    base = 0 if bank == "bg" else 0x200
    colors = []
    for c in range(256):
        raw = struct.unpack_from('<H', palram, base + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        colors.append((r, g, b, a))
    return colors


def render_8bpp(rom_off, size_bytes, palette, cols_of_tiles):
    # 每 tile 64B, 8×8
    n_tiles = size_bytes // 64
    rows = (n_tiles + cols_of_tiles - 1) // cols_of_tiles
    img = Image.new("RGBA", (cols_of_tiles * 8, rows * 8), (80, 80, 80, 255))
    px = img.load()
    for t in range(n_tiles):
        col = t % cols_of_tiles
        row = t // cols_of_tiles
        for y in range(8):
            for x in range(8):
                byte = ROM[rom_off + t * 64 + y * 8 + x]
                px[col * 8 + x, row * 8 + y] = palette[byte]
    return img, n_tiles


palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()
outdir = ROOT / "doc/temp/ui_runs_preview"
outdir.mkdir(exist_ok=True)

for tag, rom_off, size, state, bank, cols in RUNS:
    pal = decode_full_palette(palram_s0, bank)
    img, n = render_8bpp(rom_off, size, pal, cols)
    img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    img.save(outdir / f"{tag}_{bank}_8bpp.png")
    print(f"[+] {tag} @0x{rom_off:08X} ({size} B = {n} × 64B)")
