"""
验证 p1-phase-b2-findings.md 的 6bpp 解码公式。

目标卡：DESPAIR FROM THE DARK (card_id=1323, tile_block=1476)
ROM 源地址：0x08BD2140（= 0x08510640 + 1476 × 4800）
ROM 文件偏移：0x00BD2140
6bpp 公式见 findings §3.4。

输出：
- doc/temp/despair_raw_80x80.png    —— 线性排列的 6400 像素，80×80
- doc/temp/despair_tiles_76x64.png  —— 按 8×8 tile 重排，假设 64×76（80 tiles 宽，但截 4864 像素）
"""
import os, struct

ROM_PATH = "roms/2343.gba"
SRC_OFFSET = 0x00BD2140
NUM_ITER = 800  # findings: 800 次循环，每次处理 6 ROM bytes → 8 像素

with open(ROM_PATH, "rb") as f:
    f.seek(SRC_OFFSET)
    rom = f.read(NUM_ITER * 6)

# 6bpp 解码
pixels = bytearray()
for i in range(NUM_ITER):
    off = i * 6
    W0, W1, W2 = struct.unpack_from("<HHH", rom, off)
    p0 = W0 & 0x3F
    p1 = (W0 >> 6) & 0x3F
    p2 = ((W0 >> 12) & 0xF) | ((W1 & 0x3) << 4)
    p3 = (W1 >> 2) & 0x3F
    p4 = (W1 >> 8) & 0x3F
    p5 = ((W1 >> 14) & 0x3) | ((W2 & 0xF) << 2)
    p6 = (W2 >> 4) & 0x3F
    p7 = (W2 >> 10) & 0x3F
    pixels.extend([p0, p1, p2, p3, p4, p5, p6, p7])

print(f"解码了 {len(pixels)} 个 6bit 像素（期望 {NUM_ITER*8}=6400）")

# 6bit → 8bit（×4）做灰度预览
gray = bytes(p << 2 for p in pixels)

def save_pgm(path, w, h, data):
    assert len(data) == w * h
    with open(path, "wb") as f:
        f.write(f"P5\n{w} {h}\n255\n".encode())
        f.write(data)
    print(f"  wrote {path} ({w}x{h})")

os.makedirs("doc/temp", exist_ok=True)

# 版本 A：线性 80×80（简单排列看有没有结构）
save_pgm("doc/temp/despair_linear_80x80.pgm", 80, 80, gray)

# 版本 B：按 8×8 tile 重排
# 假设 tile 宽度 Tw 和 tile 高度 Th，每 tile 64 像素
# 总共 100 tiles。试几种布局：
def tile_arrange(pixels, tile_cols, tile_rows):
    """pixels 是按 tile × 8×8 扫描顺序存储（每 tile 64 像素，行优先）"""
    W = tile_cols * 8
    H = tile_rows * 8
    total_tiles = tile_cols * tile_rows
    need = total_tiles * 64
    if len(pixels) < need:
        pixels = pixels + b'\x00' * (need - len(pixels))
    else:
        pixels = pixels[:need]
    out = bytearray(W * H)
    for tile_idx in range(total_tiles):
        tx = tile_idx % tile_cols
        ty = tile_idx // tile_cols
        for py in range(8):
            for px in range(8):
                src = tile_idx * 64 + py * 8 + px
                dst = (ty * 8 + py) * W + (tx * 8 + px)
                out[dst] = pixels[src]
    return bytes(out), W, H

# 100 tiles: 试 10×10, 20×5, 5×20
for cols, rows in [(10, 10), (20, 5), (5, 20), (8, 10), (10, 8)]:
    data, W, H = tile_arrange(gray, cols, rows)
    save_pgm(f"doc/temp/despair_tiles_{cols}x{rows}.pgm", W, H, data)

print("完成。用图像查看器打开 pgm 文件（VS Code 需装扩展，或转 PNG）。")
