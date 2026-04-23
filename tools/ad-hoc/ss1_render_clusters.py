"""将已识别的未知段 tile 簇渲染为 PNG，多调色板试色。

每个簇遍历 PALRAM 中所有 16 个 BG 子调色板 + 16 个 OBJ 子调色板，
输出 `doc/temp/ss1_preview_<tag>_pb<0-1><0-F>.png`。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

CLUSTERS = [
    # (tag, rom_start, tile_count, state, vram_off)
    ("seg-C_tile5",     0x018387A0,  5, "s3", 0x8140),
    ("seg-2.5MB_2sp",   0x01A3C760,  2, "s0", 0x176A0),
    ("seg-880K_22",     0x01CF2060, 22, "s0", 0x9180),
    ("seg-880K_20",     0x01CF26A0, 20, "s0", 0x92E0),
    ("seg-880K_21",     0x01CF47A0, 21, "s0", 0x8B00),
    ("seg-880K_6",      0x01DAF160,  6, "s3", 0x81A0),
    # 扩展：seg-880K 三个 20+ 簇疑似同属一大张，连带中间/末尾未匹配 tile 一起导出观察
    ("seg-880K_span",   0x01CF2000, 64, "s0", 0x8B00),   # 64 tiles = 2 KB
]


def decode_palette_from_palram(palram: bytes, bank: str, subpal: int):
    """bank = 'bg' or 'obj', subpal 0..15 -> 16 色 RGBA list."""
    base = 0 if bank == "bg" else 0x200
    off = base + subpal * 32
    colors = []
    for c in range(16):
        raw = struct.unpack_from('<H', palram, off + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        colors.append((r, g, b, a))
    return colors


def render_tile_strip(rom_off: int, n_tiles: int, palette: list, cols: int = 8) -> Image.Image:
    rows = (n_tiles + cols - 1) // cols
    img = Image.new("RGBA", (cols * 8, rows * 8), (0, 0, 0, 0))
    px = img.load()
    for t in range(n_tiles):
        col = t % cols
        row = t // cols
        for y in range(8):
            for x in range(4):                    # 4 字节/行
                byte = ROM[rom_off + t * 32 + y * 4 + x]
                lo = byte & 0xF
                hi = (byte >> 4) & 0xF
                px[col * 8 + x * 2,     row * 8 + y] = palette[lo]
                px[col * 8 + x * 2 + 1, row * 8 + y] = palette[hi]
    return img


# 用 s0 的 PALRAM 给列表视图的簇，s3 的给详情视图的簇
palram_s0 = (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes()
palram_s3 = (ROOT / "doc/temp/ss1_s3_palram.bin").read_bytes()

outdir = ROOT / "doc/temp/ui_cluster_previews"
outdir.mkdir(exist_ok=True)

for tag, rom_off, n_tiles, state, vram_off in CLUSTERS:
    palram = palram_s3 if state == "s3" else palram_s0
    # 猜测 bank：VRAM < 0x10000 是 BG，>= 0x10000 是 OBJ
    bank = "obj" if vram_off >= 0x10000 else "bg"
    for subpal in range(16):
        palette = decode_palette_from_palram(palram, bank, subpal)
        img = render_tile_strip(rom_off, n_tiles, palette, cols=min(8, n_tiles))
        # 放大 4 倍便于查看
        img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
        img.save(outdir / f"{tag}__{state}_{bank}_pb{subpal:X}.png")
    print(f"[+] {tag} @0x{rom_off:08X} ({n_tiles} tiles) → {outdir}/{tag}__*.png")

print(f"\n全部预览: {outdir}")
