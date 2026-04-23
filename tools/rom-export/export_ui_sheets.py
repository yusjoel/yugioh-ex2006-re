#!/usr/bin/env python3
"""
导出 UI sheet / palette bin + PNG 预览（UNKNOWN seg 0x1DFF9D2 和 0x1E31714 内）。

产物（asm/rom.s 引用）：
  graphics/bin/ui-misc/_MERGED_HUD_sheet_01E246D4_01E25554.bin
  graphics/bin/ui-misc/FUN081016c0_s1_small_01E25674.bin
  graphics/bin/ui-misc/FUN081016c0_s1_big_01E25934.bin
  graphics/bin/ui-misc/FUN081016c0_s3_01E25C34.bin
  graphics/bin/ui-misc/FUN081066fc_obj_01E310B4.bin
  graphics/bin/ui-misc/FUN081058c8_anim_pal_01E31754.bin
  graphics/bin/ui-misc/FUN081066fc_obj_pal_01E31794.bin
  graphics/bin/ui-misc/switch_sheets/case_{0..c,9}_0x01E2xxxx.bin

参考（rom.s 不用，仅视觉参考）：
  graphics/bin/ui-misc/FUN08101068_{bg,obj}_01E2xxxx.bin   （HUD sheet 的 10 个子段）

预览 PNG（各 bin 的可视化，不进入构建）：
  graphics/images/ui-misc/*.png
  graphics/images/ui-misc/switch_sheets/case_{0..c,9}.png

调色板来源：
  card-mini-frame-palette (ROM 0x01E31554) subpal 0/1/2 用于渲染 HUD/state sheets
  s_s0 OBJ palette (doc/temp/ss1_s0_palram.bin) 用于 switch sheets 8bpp 渲染
    —— 此 palram 只在 ss1 存档画面正确；其他画面下 palette 不同，
       仅用于预览视觉识别图标用途，不影响 bin 内容。

参考文档：
  doc/dev/ss1-rom-image-survey.md
  doc/dev/hud-sheet-references-in-code.md
"""
import os
import struct
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

ROM_PATH = 'roms/2343.gba'

# ──────────────────────────────────────────────────────────────────────────────
# bin 导出表：(相对路径, ROM 起址, 字节数)
# ──────────────────────────────────────────────────────────────────────────────

# 主 HUD sheet（FUN_08101068, 116 tiles 4bpp, rom.s 引用）
HUD_MERGED = ('graphics/bin/ui-misc/_MERGED_HUD_sheet_01E246D4_01E25554.bin',
              0x01E246D4, 0x0E80)

# HUD sheet 10 个子段（参考，rom.s 不用）
HUD_SUB_BLOCKS = [
    # (name, rom_off, size)
    ('FUN08101068_bg_01E246D4.bin',  0x01E246D4, 0xE0),
    ('FUN08101068_bg_01E247B4.bin',  0x01E247B4, 0x80),
    ('FUN08101068_bg_01E24834.bin',  0x01E24834, 0x100),
    ('FUN08101068_bg_01E24934.bin',  0x01E24934, 0x1C0),
    # 注：0x01E24AF4 实际整块 0x200（OBJ 用 16 tile），BG 只取前 13 tile = 0x1A0
    ('FUN08101068_bg_01E24AF4.bin',  0x01E24AF4, 0x1A0),
    ('FUN08101068_obj_01E24CF4.bin', 0x01E24CF4, 0x200),
    ('FUN08101068_obj_01E24EF4.bin', 0x01E24EF4, 0x200),
    ('FUN08101068_obj_01E250F4.bin', 0x01E250F4, 0x200),
    ('FUN08101068_obj_01E252F4.bin', 0x01E252F4, 0x120),
    ('FUN08101068_obj_01E25414.bin', 0x01E25414, 0x140),
]

# FUN_081016c0 state sheets
STATE_SHEETS = [
    ('FUN081016c0_s1_small_01E25674.bin', 0x01E25674, 0x2C0),  # 22 tiles (11 iter × 2)
    ('FUN081016c0_s1_big_01E25934.bin',   0x01E25934, 0x300),  # 24 tiles (12×2)
    ('FUN081016c0_s3_01E25C34.bin',       0x01E25C34, 0x300),  # 24 tiles (6 iter × 4)
]

# FUN_081066fc aux
AUX = [
    ('FUN081066fc_obj_01E310B4.bin',    0x01E310B4, 0x200),  # 16 tiles 4bpp OBJ
    ('FUN081058c8_anim_pal_01E31754.bin', 0x01E31754, 0x20),  # 16-color palette
    ('FUN081066fc_obj_pal_01E31794.bin',  0x01E31794, 0x20),  # 16-color palette
]

# FUN_08109788 switch cases (0x100 B/item, 8bpp 2×2 sprite = 16×16 px)
SWITCH_CASES = [
    # (tag, rom_start, item_count, description)
    ('0', 0x01E265B4,  5, 'menu action icons'),
    ('1', 0x01E26AB4,  6, 'heart HP counter 1-5 + magnifier'),
    ('2', 0x01E270B4, 11, 'misc UI icons (sword/shield/gem/star/seal)'),
    ('3', 0x01E27BB4,  5, 'heart-up HP counter 1-5'),
    ('4', 0x01E280B4,  9, 'card frame color badges'),
    ('5', 0x01E289B4,  4, 'star counter badges (1-4, 5-6, 7+)'),
    ('6', 0x01E28DB4, 10, 'ATTRIBUTE icons (10 款)'),
    ('a', 0x01E297B4, 10, 'ATTRIBUTE icons (dup of case 6)'),
    ('7', 0x01E2A1B4, 22, 'RACE icons (22 款)'),
    ('b', 0x01E2B7B4, 22, 'RACE icons (dup of case 7)'),
    ('8', 0x01E2CDB4,  8, 'brown emblems (8 款)'),
    ('c', 0x01E2D5B4,  8, 'brown emblems (dup of case 8)'),
    ('9', 0x01E2DDB4, 33, 'status/achievement icons (真实边界：item 33 起字节突变)'),
]

# ──────────────────────────────────────────────────────────────────────────────
# 渲染辅助
# ──────────────────────────────────────────────────────────────────────────────

def decode_subpal(rom, off):
    pal = []
    for c in range(16):
        raw = struct.unpack_from('<H', rom, off + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        pal.append((r, g, b, a))
    return pal


def full_256_pal_from_bytes(palbytes):
    pal = []
    for c in range(256):
        raw = struct.unpack_from('<H', palbytes, c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        pal.append((r, g, b, a))
    return pal


def render_tile_4bpp(rom, off, pal, img, ox, oy):
    px = img.load()
    for y in range(8):
        for x in range(4):
            byte = rom[off + y * 4 + x]
            px[ox + x * 2,     oy + y] = pal[byte & 0xF]
            px[ox + x * 2 + 1, oy + y] = pal[(byte >> 4) & 0xF]


def render_tile_8bpp(rom, off, pal, img, ox, oy):
    px = img.load()
    for y in range(8):
        for x in range(8):
            byte = rom[off + y * 8 + x]
            px[ox + x, oy + y] = pal[byte]


def render_sheet_4bpp(rom, off, n_tiles, pal, cols, bg=(0, 0, 0, 0)):
    rows = (n_tiles + cols - 1) // cols
    img = Image.new('RGBA', (cols * 8, rows * 8), bg)
    for t in range(n_tiles):
        c, r = t % cols, t // cols
        render_tile_4bpp(rom, off + t * 32, pal, img, c * 8, r * 8)
    return img


def render_vertical_strip_4bpp(rom, off, n_tiles, pal):
    img = Image.new('RGBA', (8, n_tiles * 8), (0, 0, 0, 0))
    for t in range(n_tiles):
        render_tile_4bpp(rom, off + t * 32, pal, img, 0, t * 8)
    return img


def render_col_major_4bpp(rom, off, n_cols, rows_per_col, pal):
    img = Image.new('RGBA', (n_cols * 8, rows_per_col * 8), (0, 0, 0, 0))
    for col in range(n_cols):
        for rr in range(rows_per_col):
            tile_idx = col * rows_per_col + rr
            render_tile_4bpp(rom, off + tile_idx * 32, pal, img,
                             col * 8, rr * 8)
    return img


def render_2x2_per_iter_4bpp(rom, off, n_iters, pal):
    img = Image.new('RGBA', (2 * n_iters * 8, 16), (0, 0, 0, 0))
    for it in range(n_iters):
        for subtile, (sub_col, sub_row) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
            render_tile_4bpp(rom, off + (it * 4 + subtile) * 32, pal, img,
                             it * 16 + sub_col * 8, sub_row * 8)
    return img


def render_case_8bpp_grid(rom, item_base, n_items, pal, ipr=16, gap=4):
    item_w, item_h = 16, 16
    ipr_actual = min(n_items, ipr)
    grows = (n_items + ipr_actual - 1) // ipr_actual
    img = Image.new('RGBA',
                    (ipr_actual * (item_w + gap) - gap,
                     grows * (item_h + gap) - gap),
                    (40, 40, 40, 255))
    for i in range(n_items):
        gc, gr = i % ipr_actual, i // ipr_actual
        item_off = item_base + i * 0x100
        ox = gc * (item_w + gap)
        oy = gr * (item_h + gap)
        for t_idx in range(4):
            tc, tr = t_idx % 2, t_idx // 2
            render_tile_8bpp(rom, item_off + t_idx * 64, pal, img,
                             ox + tc * 8, oy + tr * 8)
    return img


def render_palette_strip(rom, off, n_colors):
    img = Image.new('RGBA', (n_colors * 16, 16), (0, 0, 0, 0))
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


# ──────────────────────────────────────────────────────────────────────────────
# 预存 ss1 OBJ 256 色调色板（硬编码），避免依赖 doc/temp/
# 来自 ss1 存档（卡组构建列表画面），用于 switch sheet 8bpp 预览。
# 仅影响 PNG 视觉，bin 内容不受影响。
# 若将来游戏在其他画面加载不同 OBJ palette，可用别的调色板重渲。
# ──────────────────────────────────────────────────────────────────────────────

def load_ss1_obj_palette():
    """尝试从 doc/temp/ss1_s0_palram.bin 读 OBJ 调色板 (512B, OBJ 部分偏移 0x200)。
    若文件不存在，回退到用 card-mini-frame-palette 前 256 色近似。
    """
    p = Path('doc/temp/ss1_s0_palram.bin')
    if p.exists():
        palram = p.read_bytes()
        return full_256_pal_from_bytes(palram[0x200:0x400])
    # 回退：拼接 card-mini-frame-palette 的多个 subpal 模拟 256 色
    rom = Path(ROM_PATH).read_bytes()
    all_colors = bytearray()
    for i in range(8):
        off = 0x01E31554 + i * 0x20
        all_colors.extend(rom[off:off + 0x20])
    while len(all_colors) < 512:
        all_colors.extend(b'\x00\x00' * 16)
    return full_256_pal_from_bytes(bytes(all_colors))


# ──────────────────────────────────────────────────────────────────────────────
# 主函数
# ──────────────────────────────────────────────────────────────────────────────

def main():
    rom = Path(ROM_PATH).read_bytes()
    assert len(rom) == 0x2000000, f'ROM size 异常: {len(rom)}'

    bin_dir = Path('graphics/bin/ui-misc')
    switch_bin_dir = bin_dir / 'switch_sheets'
    png_dir = Path('graphics/images/ui-misc')
    switch_png_dir = png_dir / 'switch_sheets'
    for d in [bin_dir, switch_bin_dir, png_dir, switch_png_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # ---- 导出 bin (rom.s 会 .incbin 的) ----
    print('[*] 导出 bin ...')
    # HUD 合并包
    name, off, sz = HUD_MERGED
    Path(name).write_bytes(rom[off:off + sz])
    print(f'  [+] {name} ({sz} B)')
    # HUD 子段（参考）
    for fname, off, sz in HUD_SUB_BLOCKS:
        (bin_dir / fname).write_bytes(rom[off:off + sz])
        print(f'  [+] {bin_dir / fname} ({sz} B)')
    # state / aux
    for fname, off, sz in STATE_SHEETS + AUX:
        (bin_dir / fname).write_bytes(rom[off:off + sz])
        print(f'  [+] {bin_dir / fname} ({sz} B)')
    # switch cases
    for tag, rom_start, n_items, desc in SWITCH_CASES:
        fname = f'case_{tag}_0x{rom_start:08X}.bin'
        sz = n_items * 0x100
        (switch_bin_dir / fname).write_bytes(rom[rom_start:rom_start + sz])
        print(f'  [+] {switch_bin_dir / fname} ({sz} B, {n_items} items) — {desc}')

    # ---- 导出预览 PNG（可选，需要 Pillow）----
    if Image is None:
        print('\n[!] PIL/Pillow 未安装，跳过 PNG 预览')
        return

    print('\n[*] 渲染预览 PNG ...')

    # 调色板来源：card-mini-frame-palette[0/1/2]
    pal_main = decode_subpal(rom, 0x01E31554)
    pal_pb9  = decode_subpal(rom, 0x01E31574)
    pal_pb11 = decode_subpal(rom, 0x01E31594)

    def save_png(img, path, scale=4):
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
        img.save(path)

    # HUD 子段 PNG（宽度按代码 tile_2d_row_copy 实际 w 参数）
    hud_layouts = [
        ('FUN08101068_bg_01E246D4',  0x01E246D4,  7, 'row',   7,  pal_main),
        ('FUN08101068_bg_01E247B4',  0x01E247B4,  4, 'row',   4,  pal_main),
        ('FUN08101068_bg_01E24834',  0x01E24834,  8, 'row',   8,  pal_main),
        ('FUN08101068_bg_01E24934',  0x01E24934, 14, 'row',   7,  pal_main),
        ('FUN08101068_bg_01E24AF4',  0x01E24AF4, 13, 'row',  13,  pal_main),
        ('FUN08101068_obj_01E24CF4', 0x01E24CF4, 16, 'row',   8,  pal_pb9),
        ('FUN08101068_obj_01E24EF4', 0x01E24EF4, 16, 'row',   8,  pal_pb9),
        ('FUN08101068_obj_01E250F4', 0x01E250F4, 16, 'row',   8,  pal_pb9),
        ('FUN08101068_obj_01E252F4', 0x01E252F4,  9, 'row',   9,  pal_pb9),
        ('FUN08101068_obj_01E25414', 0x01E25414, 10, 'vstrip', 1, pal_pb9),   # 竖条
    ]
    for tag, off, n, mode, cols, pal in hud_layouts:
        if mode == 'vstrip':
            img = render_vertical_strip_4bpp(rom, off, n, pal)
        else:
            img = render_sheet_4bpp(rom, off, n, pal, cols)
        save_png(img, png_dir / f'{tag}.png', scale=8 if mode == 'vstrip' else 4)
    print(f'  [+] HUD 子段 × {len(hud_layouts)}')

    # state sheets
    save_png(render_col_major_4bpp(rom, 0x01E25674, 11, 2, pal_pb11),
             png_dir / 'FUN081016c0_s1_small_01E25674.png')
    save_png(render_sheet_4bpp(rom, 0x01E25934, 24, pal_pb11, 12),
             png_dir / 'FUN081016c0_s1_big_01E25934.png')
    save_png(render_2x2_per_iter_4bpp(rom, 0x01E25C34, 6, pal_pb11),
             png_dir / 'FUN081016c0_s3_01E25C34.png')
    print('  [+] state sheets × 3')

    # aux
    save_png(render_sheet_4bpp(rom, 0x01E310B4, 16, pal_main, 8),
             png_dir / 'FUN081066fc_obj_01E310B4.png')
    img_pal_anim = render_palette_strip(rom, 0x01E31754, 16)
    img_pal_anim.save(png_dir / 'FUN081058c8_anim_pal_01E31754.png')
    img_pal_aux = render_palette_strip(rom, 0x01E31794, 16)
    img_pal_aux.save(png_dir / 'FUN081066fc_obj_pal_01E31794.png')
    print('  [+] aux tile + 2 palette')

    # HUD ALL preview (116 tiles × pal_main)
    save_png(render_sheet_4bpp(rom, 0x01E246D4, 116, pal_main, 16),
             png_dir / '_ALL_HUD_sheet_preview.png')
    print('  [+] HUD all preview')

    # switch cases (8bpp 2×2)
    pal_obj = load_ss1_obj_palette()
    for tag, rom_start, n_items, desc in SWITCH_CASES:
        img = render_case_8bpp_grid(rom, rom_start, n_items, pal_obj)
        save_png(img, switch_png_dir / f'case_{tag}.png')
    print(f'  [+] switch cases × {len(SWITCH_CASES)}')


if __name__ == '__main__':
    main()
