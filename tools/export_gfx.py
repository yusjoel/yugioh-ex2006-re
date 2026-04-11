#!/usr/bin/env python3
"""
从 roms/2343.gba 导出对手图形为 PNG 文件

数据来源：doc/um06-romhacking-resource/opponents-coinflip-screen.md
格式：标准 GBA 4bpp 平铺背景，无压缩

输出：
  graphics/opponents/<名称>_top.png     大图上半部分（240×160，RGBA）
  graphics/opponents/<名称>_bottom.png  大图下半部分（240×160，RGBA）
  graphics/icons/<名称>_icon.png        小图标（24×24，RGBA）
"""

import os
import struct
from PIL import Image

ROM_PATH = 'roms/2343.gba'
GFX_DIR  = 'graphics'

# ──────────────────────────────────────────────────────────────────────────────
# 对手大图数据表
# 字段：(slug, top_tiles, top_tilemap, palette, bottom_tiles, bottom_tilemap)
# 所有地址均为 ROM 文件偏移（来自文档 Tile Molester / HxD 地址列）
# ──────────────────────────────────────────────────────────────────────────────
LARGE_GFX = [
    ('kuriboh',                  0x1B1200C, 0x1B4800C, 0x1B101AC, 0x1B51CFC, 0x1B87CFC),
    ('scapegoat',                0x1B1400C, 0x1B484BC, 0x1B1022C, 0x1B53CFC, 0x1B881AC),
    ('skull_servant',            0x1B1600C, 0x1B4896C, 0x1B103EC, 0x1B55CFC, 0x1B8865C),
    ('watapon',                  0x1B1800C, 0x1B48E1C, 0x1B1050C, 0x1B57CFC, 0x1B88B0C),
    ('pikeru',                   0x1B1A00C, 0x1B492CC, 0x1B1062C, 0x1B59CFC, 0x1B88FBC),
    ('batteryman_c',             0x1B1C00C, 0x1B4977C, 0x1B1074C, 0x1B5BCFC, 0x1B8946C),
    ('ojama_yellow',             0x1B1E00C, 0x1B49C2C, 0x1B1086C, 0x1B5DCFC, 0x1B8991C),
    ('goblin_king',              0x1B2000C, 0x1B4A0DC, 0x1B1098C, 0x1B5FCFC, 0x1B89DCC),
    ('des_frog',                 0x1B2200C, 0x1B4A58C, 0x1B10AAC, 0x1B61CFC, 0x1B8A27C),
    ('water_dragon',             0x1B2400C, 0x1B4AA3C, 0x1B10BCC, 0x1B63CFC, 0x1B8A72C),
    ('redd',                     0x1B2600C, 0x1B4AEEC, 0x1B10CEC, 0x1B65CFC, 0x1B8ABDC),
    ('vampire_genesis',          0x1B2800C, 0x1B4B39C, 0x1B10E0C, 0x1B67CFC, 0x1B8B08C),
    ('infernal_flame_emperor',   0x1B2A00C, 0x1B4B84C, 0x1B10F2C, 0x1B69CFC, 0x1B8B53C),
    ('ocean_dragon_lord',        0x1B2C00C, 0x1B4BCFC, 0x1B1104C, 0x1B6BCFC, 0x1B8B9EC),
    ('helios_duo_megiste',       0x1B2E00C, 0x1B4C1AC, 0x1B1116C, 0x1B6DCFC, 0x1B8BE9C),
    ('gilford_the_legend',       0x1B3000C, 0x1B4C65C, 0x1B1128C, 0x1B6FCFC, 0x1B8C34C),
    ('dark_eradicator_warlock',  0x1B3200C, 0x1B4CB0C, 0x1B11CAC, 0x1B71CFC, 0x1B8C7FC),
    ('guardian_exode',           0x1B3400C, 0x1B4CFBC, 0x1B114CC, 0x1B73CFC, 0x1B8CCAC),
    ('goldd',                    0x1B3600C, 0x1B4D46C, 0x1B115EC, 0x1B75CFC, 0x1B8D15C),
    ('elemental_hero_electrum',  0x1B3899C, 0x1B4D91C, 0x1B1170C, 0x1B77CFC, 0x1B8D60C),
    ('raviel',                   0x1B3A00C, 0x1B4DDCC, 0x1B1182C, 0x1B79CFC, 0x1B8DABC),
    ('horus',                    0x1B3C00C, 0x1B4E27C, 0x1B1194C, 0x1B7BCFC, 0x1B8DF6C),
    ('stronghold',               0x1B3E00C, 0x1B4E72C, 0x1B11A6C, 0x1B7DCFC, 0x1B8E41C),
    ('sacred_phoenix',           0x1B4000C, 0x1B4EBDC, 0x1B11B8C, 0x1B7FCFC, 0x1B8E8CC),
    ('cyber_end_dragon',         0x1B4200C, 0x1B4F08C, 0x1B11CAC, 0x1B81CFC, 0x1B8ED7C),
    ('mirror_match',             0x1B4400C, 0x1B4F53C, 0x1B11DCC, 0x1B83CFC, 0x1B8F22C),
    ('copycat',                  0x1B4600C, 0x1B4F9EC, 0x1B11EEC, 0x1B85CFC, 0x1B8F6DC),
]

# ──────────────────────────────────────────────────────────────────────────────
# 小图标数据表
# 字段：(slug, tiles, palette)
# 9 个图块（3×3 排列），1 个 16 色调色板，无 Tilemap
# ──────────────────────────────────────────────────────────────────────────────
ICONS = [
    ('kuriboh',                  0x188DA70, 0x18963D0),
    ('scapegoat',                0x188DB90, 0x18963F0),
    ('skull_servant',            0x188DCB0, 0x1896410),
    ('watapon',                  0x188DDD0, 0x1896430),
    ('pikeru',                   0x188DEF0, 0x1896450),
    ('batteryman_c',             0x188E010, 0x1896470),
    ('ojama_yellow',             0x188E130, 0x1896490),
    ('goblin_king',              0x188E250, 0x18964B0),
    ('des_frog',                 0x188E370, 0x18964D0),
    ('water_dragon',             0x188E490, 0x18964F0),
    ('redd',                     0x188E5B0, 0x1896510),
    ('vampire_genesis',          0x188E6D0, 0x1896530),
    ('infernal_flame_emperor',   0x188E7F0, 0x1896550),
    ('ocean_dragon_lord',        0x188E910, 0x1896570),
    ('helios_duo_megiste',       0x188EA30, 0x1896590),
    ('gilford_the_legend',       0x188EB50, 0x18965B0),
    ('dark_eradicator_warlock',  0x188EC70, 0x18965D0),
    ('guardian_exode',           0x188ED90, 0x18965F0),
    ('goldd',                    0x188EEB0, 0x1896610),
    ('elemental_hero_electrum',  0x188EFD0, 0x1896630),
    ('raviel',                   0x188F0F0, 0x1896650),
    ('horus',                    0x188F210, 0x1896670),
    ('stronghold',               0x188F330, 0x1896690),
    ('sacred_phoenix',           0x188F450, 0x18966B0),
    ('cyber_end_dragon',         0x188F570, 0x18966D0),
    ('mirror_match',             0x188F690, 0x18966F0),
    ('copycat',                  0x188F7B0, 0x1896710),
]

# ──────────────────────────────────────────────────────────────────────────────
# 解码函数
# ──────────────────────────────────────────────────────────────────────────────

def decode_palette(rom, offset, n_subpals=16):
    """
    读取 n_subpals 个 16 色子调色板，返回 list[list[(r,g,b,a)]]。
    每个子调色板 32 字节（16 个 BGR555 颜色）。
    颜色索引 0 视为透明（alpha=0）。
    """
    palettes = []
    for s in range(n_subpals):
        colors = []
        for c in range(16):
            raw = struct.unpack_from('<H', rom, offset + (s * 16 + c) * 2)[0]
            r = (raw & 0x1F) << 3
            g = ((raw >> 5) & 0x1F) << 3
            b = ((raw >> 10) & 0x1F) << 3
            a = 0 if c == 0 else 255   # 色0 透明
            colors.append((r, g, b, a))
        palettes.append(colors)
    return palettes


def decode_tile(rom, offset):
    """
    解码单个 4bpp 8×8 图块（32 字节），返回 64 个色彩索引（list[int]）。
    每字节低 4 位为左像素，高 4 位为右像素。
    """
    indices = []
    for i in range(32):
        byte = rom[offset + i]
        indices.append(byte & 0xF)
        indices.append(byte >> 4)
    return indices  # 64 个 4-bit 索引，行优先排列


def render_tilemap_image(rom, tiles_off, tilemap_off, palette_off,
                         map_w=30, map_h=20, n_tiles=256):
    """
    渲染 Tilemap 图像，返回 RGBA PIL Image（240×160）。

    tilemap 条目格式（16 位）：
      bits  0- 9: 图块索引（0-1023，实际只用 0-255）
      bit    10: 水平翻转
      bit    11: 垂直翻转
      bits 12-15: 子调色板编号（0-15）
    """
    palettes = decode_palette(rom, palette_off, n_subpals=16)

    # 预解码所有图块
    tiles = []
    for t in range(n_tiles):
        tiles.append(decode_tile(rom, tiles_off + t * 32))

    img = Image.new('RGBA', (map_w * 8, map_h * 8), (0, 0, 0, 0))
    pixels = img.load()

    for row in range(map_h):
        for col in range(map_w):
            entry = struct.unpack_from('<H', rom, tilemap_off + (row * map_w + col) * 2)[0]
            tile_idx  = entry & 0x3FF
            hflip     = bool(entry & 0x400)
            vflip     = bool(entry & 0x800)
            subpal    = (entry >> 12) & 0xF

            if tile_idx >= n_tiles:
                continue  # 超出范围跳过（tile 0 为空白是正常的）

            tile_data = tiles[tile_idx]
            for ty in range(8):
                src_ty = 7 - ty if vflip else ty
                for tx in range(8):
                    src_tx = 7 - tx if hflip else tx
                    color_idx = tile_data[src_ty * 8 + src_tx]
                    px = col * 8 + tx
                    py = row * 8 + ty
                    pixels[px, py] = palettes[subpal][color_idx]

    return img


def render_icon(rom, tiles_off, palette_off, cols=3, rows=3):
    """
    渲染小图标（无 Tilemap，图块按行优先顺序排列）。
    返回 RGBA PIL Image（cols*8 × rows*8 = 24×24）。
    单个 16 色子调色板。
    """
    palette = decode_palette(rom, palette_off, n_subpals=1)[0]

    img = Image.new('RGBA', (cols * 8, rows * 8), (0, 0, 0, 0))
    pixels = img.load()

    for t in range(cols * rows):
        tile_data = decode_tile(rom, tiles_off + t * 32)
        col = t % cols
        row = t // cols
        for ty in range(8):
            for tx in range(8):
                color_idx = tile_data[ty * 8 + tx]
                px = col * 8 + tx
                py = row * 8 + ty
                pixels[px, py] = palette[color_idx]

    return img


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def main():
    rom = open(ROM_PATH, 'rb').read()

    opp_dir  = os.path.join(GFX_DIR, 'opponents')
    icon_dir = os.path.join(GFX_DIR, 'icons')
    os.makedirs(opp_dir,  exist_ok=True)
    os.makedirs(icon_dir, exist_ok=True)

    # 导出大图
    print('导出对手大图...')
    for entry in LARGE_GFX:
        slug, top_tiles, top_tm, palette, bot_tiles, bot_tm = entry

        top_img = render_tilemap_image(rom, top_tiles, top_tm, palette)
        top_path = os.path.join(opp_dir, f'{slug}_top.png')
        top_img.save(top_path)

        bot_img = render_tilemap_image(rom, bot_tiles, bot_tm, palette)
        bot_path = os.path.join(opp_dir, f'{slug}_bottom.png')
        bot_img.save(bot_path)

        print(f'  {slug}')

    # 导出小图标
    print('导出小图标...')
    for slug, tiles_off, pal_off in ICONS:
        icon_img = render_icon(rom, tiles_off, pal_off)
        icon_path = os.path.join(icon_dir, f'{slug}_icon.png')
        icon_img.save(icon_path)
        print(f'  {slug}')

    print(f'\n完成。图片保存在 {GFX_DIR}/')


if __name__ == '__main__':
    main()
