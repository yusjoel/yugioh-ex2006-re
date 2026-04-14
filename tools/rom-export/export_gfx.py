#!/usr/bin/env python3
"""
从 roms/2343.gba 导出图形资产

== 对手图形 ==
数据来源：doc/um06-romhacking-resource/opponents-coinflip-screen.md
格式：标准 GBA 4bpp 平铺背景，无压缩

PNG 输出（供美术查看/编辑）：
  graphics/opponents/<名称>_top.png     大图上半部分（240×160，RGBA）
  graphics/opponents/<名称>_bottom.png  大图下半部分（240×160，RGBA）
  graphics/icons/<名称>_icon.png        小图标（24×24，RGBA）

二进制输出（供 asm/rom.s 通过 .incbin 引用，替代 ROM incbin）：
  graphics/opponents/palette_copy1.bin       调色板块（Copy 1，7776 字节）
  graphics/opponents/top_tiles_all.bin       所有对手 Top 图块整块（0x36000 字节）
  graphics/opponents/bottom_tiles_all.bin    所有对手 Bottom 图块整块（0x36000 字节）
  graphics/opponents/<名称>_top_tilemap.bin    Top Tilemap（0x4B0 字节）
  graphics/opponents/<名称>_bottom_tilemap.bin Bottom Tilemap（0x4B0 字节）

== 决斗场地图形 ==
数据来源：doc/um06-romhacking-resource/duel-field.md
格式：标准 GBA 4bpp 平铺背景，无压缩

PNG 输出（供查看/编辑）：
  graphics/duel-field/<模式>_outer.png       外场背景（240×160，RGBA）
  graphics/duel-field/<模式>_outer_lp.png    LP/阶段布局（同图块，lp tilemap，240×160，RGBA）
  graphics/duel-field/<模式>_inner.png       内场背景（240×160，RGBA）

二进制输出（供 asm/rom.s 通过 .incbin 引用）：
  graphics/duel-field/<模式>_outer_image.bin    外场图块数据（可变大小）
  graphics/duel-field/<模式>_outer_tilemap.bin  外场 Tilemap（0x4B0 字节）
  graphics/duel-field/<模式>_outer_lp_tilemap.bin LP/阶段 Tilemap（0x4B0 字节）
  graphics/duel-field/<模式>_outer_palette.bin  外场调色板（0x40 字节，2个子调色板）
== 小图标二进制 ==

二进制输出：
  graphics/icons/<名称>_icon_tiles.bin    图标图块数据（0x120 字节，9 图块）
  graphics/icons/<名称>_icon_palette.bin  图标调色板（0x20 字节，1 子调色板）
"""


import os
import struct
from PIL import Image

ROM_PATH = 'roms/2343.gba'
GFX_DIR  = 'graphics'

# ──────────────────────────────────────────────────────────────────────────────
# 调色板区块地址（ROM 文件偏移）
# ──────────────────────────────────────────────────────────────────────────────
# 调色板区（Copy 1）：27 × 288 B = 7776 B
PALETTE_COPY1_OFF  = 0x1B101AC
PALETTE_COPY1_SIZE = 7776   # 0x1E60

# Top Tilemap 区：27 × 0x4B0 B = 32400 B
TOP_TILEMAP_BASE   = 0x1B4800C
# Bottom Tilemap 区：27 × 0x4B0 B = 32400 B
BOT_TILEMAP_BASE   = 0x1B87CFC

TILEMAP_SIZE       = 0x4B0  # 每个对手的 tilemap 字节数

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


def export_bin_files(rom, opp_dir):
    """
    导出供 asm/rom.s 使用的二进制文件：
    - palette_copy1.bin：调色板块（7776 字节，Copy 1 和 Copy 2 内容相同，引用同一文件）
    - <name>_top_tilemap.bin：每个对手的 Top Tilemap（0x4B0 字节）
    - <name>_bottom_tilemap.bin：每个对手的 Bottom Tilemap（0x4B0 字节）
    """
    # 导出调色板块（Copy 1）
    pal_bin = os.path.join(opp_dir, 'palette_copy1.bin')
    with open(pal_bin, 'wb') as f:
        f.write(rom[PALETTE_COPY1_OFF : PALETTE_COPY1_OFF + PALETTE_COPY1_SIZE])
    print(f'  → {pal_bin}  ({PALETTE_COPY1_SIZE} 字节)')

    # 导出 Top 图块整块（因 Electrum 偏移不规则，整段保留）
    TOP_TILES_OFF  = 0x1B1200C
    TOP_TILES_SIZE = 0x36000
    top_bin = os.path.join(opp_dir, 'top_tiles_all.bin')
    with open(top_bin, 'wb') as f:
        f.write(rom[TOP_TILES_OFF : TOP_TILES_OFF + TOP_TILES_SIZE])
    print(f'  → {top_bin}  ({TOP_TILES_SIZE} 字节)')

    # 导出 Bottom 图块整块
    BOT_TILES_OFF  = 0x1B51CFC
    BOT_TILES_SIZE = 0x36000
    bot_bin = os.path.join(opp_dir, 'bottom_tiles_all.bin')
    with open(bot_bin, 'wb') as f:
        f.write(rom[BOT_TILES_OFF : BOT_TILES_OFF + BOT_TILES_SIZE])
    print(f'  → {bot_bin}  ({BOT_TILES_SIZE} 字节)')

    # 导出每个对手的 tilemap（按 LARGE_GFX 顺序，与 ROM 排列顺序一致）
    for i, entry in enumerate(LARGE_GFX):
        slug = entry[0]
        top_tm_off = TOP_TILEMAP_BASE + i * TILEMAP_SIZE
        bot_tm_off = BOT_TILEMAP_BASE + i * TILEMAP_SIZE

        top_bin = os.path.join(opp_dir, f'{slug}_top_tilemap.bin')
        bot_bin = os.path.join(opp_dir, f'{slug}_bottom_tilemap.bin')

        with open(top_bin, 'wb') as f:
            f.write(rom[top_tm_off : top_tm_off + TILEMAP_SIZE])
        with open(bot_bin, 'wb') as f:
            f.write(rom[bot_tm_off : bot_tm_off + TILEMAP_SIZE])

    print(f'  → {len(LARGE_GFX)} 个对手 × 2 tilemap（每个 {TILEMAP_SIZE} 字节）')


def export_icon_bins(rom, icon_dir):
    """
    导出小图标二进制文件：
    - <slug>_icon_tiles.bin   图标图块（9 图块 × 32 字节 = 0x120 字节）
    - <slug>_icon_palette.bin 图标调色板（1 子调色板 × 32 字节 = 0x20 字节）
    """
    ICON_TILE_SIZE = 9 * 32  # 0x120
    ICON_PAL_SIZE  = 0x20
    for slug, tiles_off, pal_off in ICONS:
        with open(os.path.join(icon_dir, f'{slug}_icon_tiles.bin'), 'wb') as f:
            f.write(rom[tiles_off : tiles_off + ICON_TILE_SIZE])
        with open(os.path.join(icon_dir, f'{slug}_icon_palette.bin'), 'wb') as f:
            f.write(rom[pal_off : pal_off + ICON_PAL_SIZE])
    print(f'  → {len(ICONS)} 个图标 × 2 bin文件（tiles 0x120 + palette 0x20）')



# 数据来源：doc/um06-romhacking-resource/duel-field.md
# ──────────────────────────────────────────────────────────────────────────────

DUEL_MODES = ['campaign', 'link', 'puzzle', 'limited', 'theme', 'survival']

# 外场图块数据（每个模式独立大小）
# 字段：(模式名, ROM偏移, 字节大小)
# 大小从指针表推算（相邻指针差）：指针表位于 0x1855030，7条目（6+终止）
DUEL_OUTER_IMAGES = [
    ('campaign', 0x185504C, 0x9E0),
    ('link',     0x1855A2C, 0x5E0),
    ('puzzle',   0x185600C, 0x7E0),
    ('limited',  0x18567EC, 0xDE0),
    ('theme',    0x18575CC, 0x9E0),
    ('survival', 0x1857FAC, 0x7E0),
]

# 外场 Tilemap：6 × 0x4B0 字节（30×20 图块，240×160 像素）
# 指针表位于 0x185B634（7条目），数据从 0x185B650 开始
DUEL_OUTER_TILEMAP_BASE = 0x185B650

# LP/阶段 Tilemap（同一模式的外场图块与外场 tilemap 共用）
# 指针表位于 0x1859548（7条目），数据从 0x1859564 开始
DUEL_LP_TILEMAP_BASE = 0x1859564

# 外场调色板：6 × 0x40 字节（2个子调色板，对应 BG 调色板槽位 9–10）
# 指针表位于 0x185936C（7条目），数据从 0x1859388 开始
DUEL_OUTER_PAL_BASE  = 0x1859388
DUEL_OUTER_PAL_SIZE  = 0x40    # 2 × 16色子调色板

# 内场图块数据：6 × 0x1680 字节（180 图块，30×6 排列）
# 使用下方公共 tilemap（0x185D270）渲染
DUEL_INNER_IMAGE_BASE = 0x185D720
DUEL_INNER_IMAGE_SIZE = 0x1680  # 180 图块 × 32 字节

# 内场公共 Tilemap（所有模式共享同一个 tilemap，位于内场图块块前 0x4B0 字节处）
DUEL_INNER_TILEMAP_OFF = 0x185D270

# 内场调色板：6 × 0x20 字节（1个子调色板，对应 BG 调色板槽位 9）
DUEL_INNER_PAL_BASE  = 0x18674A0
DUEL_INNER_PAL_SIZE  = 0x20    # 1 × 16色子调色板

# 公共大小常量
DUEL_TILEMAP_SIZE = 0x4B0      # 30×20 × 2字节 = 1200 字节


def export_duel_field_bins(rom, df_dir):
    """
    导出决斗场地数据的二进制文件（供 asm/rom.s 通过 .incbin 引用）。

    外场：
      <模式>_outer_image.bin      外场图块数据（可变大小）
      <模式>_outer_tilemap.bin    外场 Tilemap（0x4B0 字节）
      <模式>_outer_lp_tilemap.bin LP/阶段 Tilemap（0x4B0 字节，与外场图块共用）
      <模式>_outer_palette.bin    外场调色板（0x40 字节，2个子调色板）

    内场：
      <模式>_inner_image.bin      内场图块数据（0x1680 字节，180 图块）
      <模式>_inner_palette.bin    内场调色板（0x20 字节，1个子调色板）
    """
    for i, (slug, img_off, img_size) in enumerate(DUEL_OUTER_IMAGES):
        # 外场图块
        with open(os.path.join(df_dir, f'{slug}_outer_image.bin'), 'wb') as f:
            f.write(rom[img_off : img_off + img_size])

        # 外场 Tilemap
        tm_off = DUEL_OUTER_TILEMAP_BASE + i * DUEL_TILEMAP_SIZE
        with open(os.path.join(df_dir, f'{slug}_outer_tilemap.bin'), 'wb') as f:
            f.write(rom[tm_off : tm_off + DUEL_TILEMAP_SIZE])

        # LP/阶段 Tilemap
        lp_off = DUEL_LP_TILEMAP_BASE + i * DUEL_TILEMAP_SIZE
        with open(os.path.join(df_dir, f'{slug}_outer_lp_tilemap.bin'), 'wb') as f:
            f.write(rom[lp_off : lp_off + DUEL_TILEMAP_SIZE])

        # 外场调色板
        pal_off = DUEL_OUTER_PAL_BASE + i * DUEL_OUTER_PAL_SIZE
        with open(os.path.join(df_dir, f'{slug}_outer_palette.bin'), 'wb') as f:
            f.write(rom[pal_off : pal_off + DUEL_OUTER_PAL_SIZE])

        # 内场图块
        inner_img_off = DUEL_INNER_IMAGE_BASE + i * DUEL_INNER_IMAGE_SIZE
        with open(os.path.join(df_dir, f'{slug}_inner_image.bin'), 'wb') as f:
            f.write(rom[inner_img_off : inner_img_off + DUEL_INNER_IMAGE_SIZE])

        # 内场调色板
        inner_pal_off = DUEL_INNER_PAL_BASE + i * DUEL_INNER_PAL_SIZE
        with open(os.path.join(df_dir, f'{slug}_inner_palette.bin'), 'wb') as f:
            f.write(rom[inner_pal_off : inner_pal_off + DUEL_INNER_PAL_SIZE])

    print(f'  → {len(DUEL_MODES)} 个模式 × 6种bin文件，共 {len(DUEL_MODES)*6} 个文件')


def render_duel_outer(rom, mode_idx, use_lp_tilemap=False):
    """
    渲染外场背景，返回 RGBA PIL Image（240×160）。

    use_lp_tilemap=False 使用普通外场 tilemap；
    use_lp_tilemap=True  使用 LP/阶段 tilemap（同一图块表和调色板）。

    外场调色板只有 2 个子调色板（0x40 字节），游戏将其加载到 BG 调色板槽位 9–10。
    渲染时在 16 个子调色板槽中将块的两个子调色板放置于槽位 9 和 10。
    """
    _, img_off, img_size = DUEL_OUTER_IMAGES[mode_idx]
    if use_lp_tilemap:
        tm_off = DUEL_LP_TILEMAP_BASE   + mode_idx * DUEL_TILEMAP_SIZE
    else:
        tm_off = DUEL_OUTER_TILEMAP_BASE + mode_idx * DUEL_TILEMAP_SIZE
    pal_off = DUEL_OUTER_PAL_BASE     + mode_idx * DUEL_OUTER_PAL_SIZE

    n_tiles = img_size // 32

    # 构建 16 个子调色板数组；槽 9 = 块子调色板 0，槽 10 = 块子调色板 1
    palettes = [[(0, 0, 0, 0)] * 16 for _ in range(16)]
    for slot_offset, src_subpal_idx in [(9, 0), (10, 1)]:
        src_off = pal_off + src_subpal_idx * 0x20
        for c in range(16):
            raw = struct.unpack_from('<H', rom, src_off + c * 2)[0]
            r = (raw & 0x1F) << 3
            g = ((raw >> 5) & 0x1F) << 3
            b = ((raw >> 10) & 0x1F) << 3
            a = 0 if c == 0 else 255
            palettes[slot_offset][c] = (r, g, b, a)

    # 预解码图块
    tiles = [decode_tile(rom, img_off + t * 32) for t in range(n_tiles)]

    img = Image.new('RGBA', (240, 160), (0, 0, 0, 0))
    pixels = img.load()

    for row in range(20):
        for col in range(30):
            entry   = struct.unpack_from('<H', rom, tm_off + (row * 30 + col) * 2)[0]
            tile_idx = entry & 0x3FF
            hflip    = bool(entry & 0x400)
            vflip    = bool(entry & 0x800)
            subpal   = (entry >> 12) & 0xF

            if tile_idx >= n_tiles:
                continue
            tile_data = tiles[tile_idx]
            for ty in range(8):
                src_ty = 7 - ty if vflip else ty
                for tx in range(8):
                    src_tx = 7 - tx if hflip else tx
                    color_idx = tile_data[src_ty * 8 + src_tx]
                    pixels[col * 8 + tx, row * 8 + ty] = palettes[subpal][color_idx]

    return img


def render_duel_inner(rom, mode_idx):
    """
    渲染内场背景，返回 RGBA PIL Image（240×160）。

    内场使用所有模式共享的 tilemap（0x185D270）和模式专属的图块数据、调色板。
    内场调色板只有 1 个子调色板，游戏将其加载到 BG 调色板槽位 9。
    """
    inner_img_off = DUEL_INNER_IMAGE_BASE + mode_idx * DUEL_INNER_IMAGE_SIZE
    inner_pal_off = DUEL_INNER_PAL_BASE   + mode_idx * DUEL_INNER_PAL_SIZE
    n_tiles = DUEL_INNER_IMAGE_SIZE // 32  # = 180

    # 构建 16 个子调色板数组；槽 9 = 内场调色板
    palettes = [[(0, 0, 0, 0)] * 16 for _ in range(16)]
    src_off = inner_pal_off
    for c in range(16):
        raw = struct.unpack_from('<H', rom, src_off + c * 2)[0]
        r = (raw & 0x1F) << 3
        g = ((raw >> 5) & 0x1F) << 3
        b = ((raw >> 10) & 0x1F) << 3
        a = 0 if c == 0 else 255
        palettes[9][c] = (r, g, b, a)

    # 预解码图块
    tiles = [decode_tile(rom, inner_img_off + t * 32) for t in range(n_tiles)]

    img = Image.new('RGBA', (240, 160), (0, 0, 0, 0))
    pixels = img.load()

    for row in range(20):
        for col in range(30):
            entry    = struct.unpack_from('<H', rom, DUEL_INNER_TILEMAP_OFF + (row * 30 + col) * 2)[0]
            tile_idx = entry & 0x3FF
            hflip    = bool(entry & 0x400)
            vflip    = bool(entry & 0x800)
            subpal   = (entry >> 12) & 0xF

            if tile_idx >= n_tiles:
                continue
            tile_data = tiles[tile_idx]
            for ty in range(8):
                src_ty = 7 - ty if vflip else ty
                for tx in range(8):
                    src_tx = 7 - tx if hflip else tx
                    color_idx = tile_data[src_ty * 8 + src_tx]
                    pixels[col * 8 + tx, row * 8 + ty] = palettes[subpal][color_idx]

    return img


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    rom = open(ROM_PATH, 'rb').read()

    opp_dir  = os.path.join(GFX_DIR, 'opponents')
    icon_dir = os.path.join(GFX_DIR, 'icons')
    df_dir   = os.path.join(GFX_DIR, 'duel-field')
    os.makedirs(opp_dir,  exist_ok=True)
    os.makedirs(icon_dir, exist_ok=True)
    os.makedirs(df_dir,   exist_ok=True)

    # 导出对手二进制文件（供 asm incbin）
    print('导出对手二进制文件...')
    export_bin_files(rom, opp_dir)

    # 导出小图标二进制文件（供 asm incbin）
    print('导出小图标二进制文件...')
    export_icon_bins(rom, icon_dir)

    # 导出对手大图 PNG
    print('导出对手大图 PNG...')
    for entry in LARGE_GFX:
        slug, top_tiles, top_tm, palette, bot_tiles, bot_tm = entry

        top_img = render_tilemap_image(rom, top_tiles, top_tm, palette)
        top_img.save(os.path.join(opp_dir, f'{slug}_top.png'))

        bot_img = render_tilemap_image(rom, bot_tiles, bot_tm, palette)
        bot_img.save(os.path.join(opp_dir, f'{slug}_bottom.png'))

        print(f'  {slug}')

    # 导出小图标 PNG
    print('导出小图标 PNG...')
    for slug, tiles_off, pal_off in ICONS:
        icon_img = render_icon(rom, tiles_off, pal_off)
        icon_img.save(os.path.join(icon_dir, f'{slug}_icon.png'))
        print(f'  {slug}')

    # 导出决斗场地二进制文件（供 asm incbin）
    print('导出决斗场地二进制文件...')
    export_duel_field_bins(rom, df_dir)

    # 导出决斗场地 PNG 预览
    print('导出决斗场地 PNG 预览...')
    for i, mode in enumerate(DUEL_MODES):
        outer_img = render_duel_outer(rom, i)
        outer_img.save(os.path.join(df_dir, f'{mode}_outer.png'))

        outer_lp_img = render_duel_outer(rom, i, use_lp_tilemap=True)
        outer_lp_img.save(os.path.join(df_dir, f'{mode}_outer_lp.png'))

        inner_img = render_duel_inner(rom, i)
        inner_img.save(os.path.join(df_dir, f'{mode}_inner.png'))

        print(f'  {mode}')

    print(f'\n完成。图片保存在 {GFX_DIR}/')


if __name__ == '__main__':
    main()
