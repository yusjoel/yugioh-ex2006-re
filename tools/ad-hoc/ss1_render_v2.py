"""渲染 stride-4 扫到的真实 tile runs。
用 VRAM 引用的文件 offset 判断 BG/OBJ，试多个调色板。
"""
import pathlib, struct
from PIL import Image

ROOT = pathlib.Path(r"E:/Workspace/yugioh-ex2006-re")
ROM = (ROOT / "roms/2343.gba").read_bytes()

# 重点 run（按大小、用途挑）
RUNS = [
    # tag, rom_off, tile_count, state, vram_off, cols
    ("segC_A_152",    0x0184A42C, 152, "s0", 0x5940, 16),
    ("segC_B_98",     0x0184B9C4,  98, "s0", 0x5940, 14),
    ("segC_CAE4_15",  0x0184CAE4,  15, "s0", 0x6A60,  8),
    ("segC_DAEC_s3_4",0x0184DAEC,   4, "s3", 0x17440, 4),
    ("segC_E4AC_s3_4",0x0184E4AC,   4, "s3", 0x17500, 4),
    ("seg1E_1CCB4_34",0x01E1CCB4,  34, "s0", 0x83C0,  8),
    ("seg1E_1DF34_29",0x01E1DF34,  29, "s0", 0x8DE0,  8),
    ("seg1E_246D4_116",0x01E246D4, 116, "s0", 0xC3A0, 16),
    ("seg1E_271B4_8obj",0x01E271B4,  8, "s0", 0x10880, 8),
    ("seg1E_289B4_12obj",0x01E289B4, 12, "s0", 0x10980, 6),
    ("seg1E_28DB4_16obj",0x01E28DB4, 16, "s0", 0x10A00, 8),
    ("seg1E_293B4_8obj",0x01E293B4,  8, "s0", 0x10000, 8),
    ("seg1E_2A9B4_8obj",0x01E2A9B4,  8, "s0", 0x10200, 8),
]


def decode_palram_subpal(palram, bank, subpal):
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


def render_strip(rom_off, n, palette, cols):
    rows = (n + cols - 1) // cols
    img = Image.new("RGBA", (cols * 8, rows * 8), (80, 80, 80, 255))
    px = img.load()
    for t in range(n):
        col = t % cols
        row = t // cols
        for y in range(8):
            for x in range(4):
                byte = ROM[rom_off + t * 32 + y * 4 + x]
                lo = byte & 0xF
                hi = (byte >> 4) & 0xF
                px[col * 8 + x * 2,     row * 8 + y] = palette[lo]
                px[col * 8 + x * 2 + 1, row * 8 + y] = palette[hi]
    return img


palram = {
    "s0": (ROOT / "doc/temp/ss1_s0_palram.bin").read_bytes(),
    "s1": (ROOT / "doc/temp/ss1_s1_palram.bin").read_bytes(),
    "s3": (ROOT / "doc/temp/ss1_s3_palram.bin").read_bytes(),
}
outdir = ROOT / "doc/temp/ui_runs_preview"
outdir.mkdir(exist_ok=True)

for tag, rom_off, n, state, vram_off, cols in RUNS:
    bank = "obj" if vram_off >= 0x10000 else "bg"
    # 每簇只导 4 个调色板（0,1,2,8）节省数量
    for subpal in [0, 1, 2, 3, 4, 8, 9, 10, 15]:
        pal = decode_palram_subpal(palram[state], bank, subpal)
        img = render_strip(rom_off, n, pal, cols)
        img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
        img.save(outdir / f"{tag}__pb{subpal:X}.png")
    print(f"[+] {tag} @0x{rom_off:08X} ({n} tiles, {bank}, state={state})")

print(f"\nout: {outdir}")
