#!/usr/bin/env python3
"""
从 roms/2343.gba 导出卡包封面条幅图 (pack banner)

ROM 布局:
  0x1CCE960: 指针表 (51 entries × 4B = 0xCC bytes)
  0x1CCEA2C: Pack 0 tile data (0x800 bytes, 8bpp raw)
  0x1CCF22C: Pack 1 tile data
  ...
  0x1CE7A2C: Pack 50 tile data
             End = 0x1CE822C

每个 pack banner 是 32×64 像素, 8bpp (256色) OBJ sprite tile。
ROM 中连续存储 (每行 256B, 8 行)；加载时按 2D OBJ mapping 展开
(dest stride 0x400, src stride 0x100)。

产出:
  graphics/pack-banners/pack_XX_banner.bin   tile 二进制 (0x800B each, 不入库)
  graphics/pack-banners/pack_XX_banner.png   灰阶预览 (不入库)
  data/pack-banners.s                        指针表 + .incbin 汇编 (入库)
"""

import os
import struct
from PIL import Image

ROM_PATH = 'roms/2343.gba'
GFX_DIR  = 'graphics/pack-banners'
ASM_OUT  = 'data/pack-banners.s'

# ROM 布局常量
PTR_TABLE_OFF  = 0x1CCE960
PACK_COUNT     = 51
PACK_TILE_SIZE = 0x800   # 2048 bytes per pack

# 卡包名 (来自 data/game-strings-en.s, game_str_en_01046..01095 + 01096)
PACK_NAMES = [
    "LEGEND OF B.E.W.D.",
    "RED MILLENIUM",
    "BLUE MILLENIUM",
    "BUSTER RANCHER",
    "DARK MAGICIAN GIRL",
    "HERO OF THE WIND",
    "EMPEROR OF DARKNESS",
    "GUARDIAN ANGEL",
    "ARMOR OF LIGHT",
    "DRAGONS OF FIRE",
    "REVIVAL OF THE DEAD",
    "MESSENGER OF PEACE",
    "WARRIORS OF GLORY",
    "CHAOTIC FIEND",
    "DRAGONS OF LEGEND",
    "SOUL OF THE WILD",
    "FORCE OF NATURE",
    "AQUA FORCES",
    "DESTRUCTION KING",
    "STALWART OGRE",
    "LIGHT OF WISDOM",
    "SHADOW OF POWER",
    "DARK ENTITY",
    "DARKNESS OF HELL",
    "SWARM OF LOCUSTS",
    "ANCIENT WEAPONS",
    "ETERNAL WARRIOR",
    "FORBIDDEN BEAST",
    "KEEPER OF THE TOMB",
    "DIMENSION OF CHAOS",
    "MYSTICAL ARTS",
    "THUNDER EMPEROR",
    "INSECT KINGDOM",
    "BLAZE OF FURY",
    "GALE OF THE WIND",
    "TIDAL SURGE",
    "MASTER OF PUPPETS",
    "HEAVENLY LIGHT",
    "WICKED SHADOW",
    "SEALED BEAST",
    "SAVAGE BEAST",
    "IRON FORTRESS",
    "PHANTOM KNIGHT",
    "CRYSTAL DRAGON",
    "PRIMORDIAL FORCE",
    "YU-GI-OH! GX",
    "ELEMENTAL HERO",
    "CHRYSALIS",
    "ALIEN",
    "CYBER LEGACY",
    "ANCIENT GEAR",
]


def render_pack_banner(rom, tile_off):
    """
    渲染 32x64 8bpp pack banner 为灰阶 PIL Image。
    ROM 数据按 GBA 8×8 tile 格式存储:
      4 tiles/row × 8 rows = 32 tiles, 每 tile 64 bytes (8bpp)
      每 tile-row = 4 × 64 = 256 bytes (0x100)
    """
    W, H = 32, 64  # 4 tiles wide × 8 tiles tall
    img = Image.new('L', (W, H), 0)
    pixels = img.load()
    for tile_row in range(8):
        for tile_col in range(4):
            tile_data_off = tile_off + tile_row * 0x100 + tile_col * 64
            for py in range(8):
                for px in range(8):
                    idx = rom[tile_data_off + py * 8 + px]
                    pixels[tile_col * 8 + px, tile_row * 8 + py] = idx
    return img


def generate_asm(rom):
    """生成 data/pack-banners.s 内容。"""
    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 卡包封面条幅图 (Pack Banners)')
    lines.append(f'@ ROM偏移: 0x{PTR_TABLE_OFF:07X} - 0x{PTR_TABLE_OFF + 0x198CC:07X}'
                 f' (共 0x198CC = {0x198CC} 字节)')
    lines.append('@')
    lines.append('@ 格式: 8bpp raw OBJ tile, 32x64 像素 (4x8 tiles), 每 pack 0x800 字节')
    lines.append('@ 加载函数: FUN_080db860 (mode 1, 2D stride copy: src 0x100/row, dest 0x400/row)')
    lines.append('@ 初始化链: FUN_080d971c -> FUN_080d8e98 -> FUN_080d8f48 -> FUN_080db860')
    lines.append('@ 图形文件由 tools/rom-export/export_pack_banners.py 从 ROM 导出 (不入库)')
    lines.append('@ =============================================================================')
    lines.append('')

    # 指针表
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append(f'@ 指针表: {PACK_COUNT} 条目, 每条 4 字节 (GBA 绝对地址)')
    lines.append(f'@ GBA地址: 0x{0x08000000 + PTR_TABLE_OFF:08X}  ROM偏移: 0x{PTR_TABLE_OFF:07X}')
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('pack_banner_ptr_table:')

    for i in range(PACK_COUNT):
        name = PACK_NAMES[i] if i < len(PACK_NAMES) else f'PACK {i}'
        lines.append(f'        .word  pack_banner_{i:02d}                       @ [{i:2d}] {name}')

    lines.append('')

    # 逐 pack tile 数据
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append(f'@ Tile 数据: {PACK_COUNT} x 0x{PACK_TILE_SIZE:X} 字节')
    lines.append('@ -----------------------------------------------------------------------------')

    for i in range(PACK_COUNT):
        ptr = struct.unpack_from('<I', rom, PTR_TABLE_OFF + i * 4)[0]
        rom_off = ptr - 0x08000000
        name = PACK_NAMES[i] if i < len(PACK_NAMES) else f'PACK {i}'
        lines.append(f'pack_banner_{i:02d}:                                     @ {name}')
        lines.append(f'        .incbin "graphics/pack-banners/pack_{i:02d}_banner.bin"')

    return '\n'.join(lines) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    rom = open(ROM_PATH, 'rb').read()
    os.makedirs(GFX_DIR, exist_ok=True)

    # 导出每个 pack 的 tile bin + PNG 预览
    print(f'导出 {PACK_COUNT} 个 pack banner bin + png...')
    for i in range(PACK_COUNT):
        ptr = struct.unpack_from('<I', rom, PTR_TABLE_OFF + i * 4)[0]
        tile_off = ptr - 0x08000000

        bin_path = os.path.join(GFX_DIR, f'pack_{i:02d}_banner.bin')
        with open(bin_path, 'wb') as f:
            f.write(rom[tile_off : tile_off + PACK_TILE_SIZE])

        img = render_pack_banner(rom, tile_off)
        img.save(os.path.join(GFX_DIR, f'pack_{i:02d}_banner.png'))

        name = PACK_NAMES[i] if i < len(PACK_NAMES) else f'PACK {i}'
        print(f'  [{i:2d}] {name}')

    # 生成 .s 文件
    asm_content = generate_asm(rom)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm_content)
    print(f'\n汇编文件: {ASM_OUT}')

    # 清理不再需要的 ptrtable bin
    ptrtable_bin = os.path.join(GFX_DIR, 'pack_banner_ptrtable.bin')
    if os.path.exists(ptrtable_bin):
        os.remove(ptrtable_bin)
        print(f'已删除: {ptrtable_bin}')

    print(f'\n完成。')


if __name__ == '__main__':
    main()
