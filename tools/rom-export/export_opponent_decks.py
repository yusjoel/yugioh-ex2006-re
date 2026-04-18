#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对手卡组 (Opponent Decks) 导出脚本

从 roms/2343.gba 导出 ROM 0x1E6468E ~ 0x1E65A46 区域：
25 个对手卡组，共 0x13B8 = 5048 字节。

每个 block 结构:
  main_cards × 2B     (deck_card，连续 u16 LE)
  2 B                 .hword 0 卡组终止符
  [fusion_cards × 2B] 融合卡组（可选）
  padding_bytes       剩余字节（含另一套 deck 数据等未解析结构）

block 大小与 (main, fusion, padding) 从项目早期手工整理的 .s 文件中锁定。

输出:
  data/opponent-decks.s

来源文档: doc/um06-deck-modification-tool/starter-opponent-paste-tool.md
"""

import os
import re
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/opponent-decks.s'

REGION_START = 0x1E6468E
REGION_END   = 0x1E65A46  # exclusive
GBA_BASE     = 0x08000000
NAME_COL_WIDTH = 46

# 25 个对手 block 规格
# (label, display_name, block_size, fusion_cards)
# main_cards 由扫描 terminator 自动得出；padding = block_size - main_cards*2 - 2 - fusion_cards*2
DECK_BLOCKS = [
    ('deck_kuriboh',                    'Kuriboh',                    0xC0,  0),
    ('deck_pikeru',                     'Pikeru',                     0xC0,  0),
    ('deck_scapegoat',                  'Scapegoat',                  0xC0,  0),
    ('deck_skull_servant',              'Skull Servant',              0xC0,  0),
    ('deck_watapon',                    'Watapon',                    0xC0,  0),
    ('deck_batteryman_c',               'Batteryman C',               0xC0,  0),
    ('deck_des_frog',                   'Des Frog',                   0xC0,  1),
    ('deck_goblin_king',                'Goblin King',                0x180, 0),
    ('deck_ojama_yellow',               'Ojama Yellow',               0xC0,  0),
    ('deck_water_dragon',               'Water Dragon',               0xC0,  0),
    ('deck_red_eyes_darkness_dragon',   'Red Eyes Darkness Dragon',   0xC0,  0),
    ('deck_ocean_dragon_lord_neo_d',    'Ocean Dragon Lord Neo D',    0xC0,  0),
    ('deck_infernal_flame_emperor',     'Infernal Flame Emperor',     0xC0,  0),
    ('deck_helios_duo_megiste',         'Helios Duo Megiste',         0xC0,  0),
    ('deck_vampire_genesis',            'Vampire Genesis',            0xC0,  0),
    ('deck_elemental_hero_electrum',    'Elemental Hero Electrum',    0xE0,  9),
    ('deck_goldd_wu_lord_of_dark',      'Goldd Wu-Lord of Dark',      0xC0,  0),
    ('deck_guardian_exode',             'Guardian Exode',             0xC0,  0),
    ('deck_gilford_the_legend',         'Gilford the Legend',         0xC0,  0),
    ('deck_dark_eradicator_warlock',    'Dark Eradicator Warlock',    0xC0,  0),
    ('deck_cyber_end_dragon',           'Cyber End Dragon',           0xD8,  7),
    ('deck_stronghold',                 'Stronghold',                 0xC0,  0),
    ('deck_horus_the_black_flame_d',    'Horus the Black Flame D',    0xC0,  0),
    ('deck_sacred_phoenix_of_n',        'Sacred Phoenix of N',        0xC0,  0),
    ('deck_raviel_lord_of_phantasms',   'Raviel Lord of Phantasms',   0xC0,  0),
]


def load_card_info(project_root):
    path = os.path.join(project_root, 'data', 'card-names.s')
    with open(path, 'r', encoding='cp1252') as f:
        text = f.read()
    mapping = {}
    pattern = re.compile(
        r'card_name_([0-9A-F]{4}):\s+@\s+(.+?)(?:\s+\(pw\s+(\d+)\))?\s*$',
        re.MULTILINE
    )
    for m in pattern.finditer(text):
        slot_id = int(m.group(1), 16)
        name = m.group(2).strip()
        pw = m.group(3) if m.group(3) else None
        mapping[slot_id] = (name, pw)
    return mapping


def fmt_card(so_code, card_info):
    info = card_info.get(so_code)
    if info:
        name, pw = info
        pw_str = pw.zfill(8) if pw else '?'
    else:
        name = f'SO=0x{so_code:04X}'
        pw_str = '?'
    return (f'    deck_card {so_code:>5d}    '
            f'@ {name:<{NAME_COL_WIDTH}s}(密码: {pw_str})')


def fmt_byte_lines(data: bytes, indent: str = '    ') -> list[str]:
    """按 16 B/行输出 .byte"""
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        parts = ', '.join(f'0x{b:02X}' for b in chunk)
        lines.append(f'{indent}.byte {parts}')
    return lines


def generate_asm(rom, card_info):
    lines = []
    total_size = REGION_END - REGION_START

    lines.append('@ =============================================================================')
    lines.append('@ 对手卡组数据（Opponent Decks）')
    lines.append(f'@ ROM偏移: 0x{REGION_START:X} - 0x{REGION_END - 1:X}')
    lines.append('@')
    lines.append('@ 格式: [so_code LE16] 连续排列，以 0x0000 终止，后跟融合卡组数据和填充')
    lines.append('@ 对手卡组均为 40 张牌（重复条目表示多张副本）')
    lines.append('@')
    lines.append('@ 来源文档: doc/um06-deck-modification-tool/starter-opponent-paste-tool.md')
    lines.append('@ 由 tools/rom-export/export_opponent_decks.py 生成')
    lines.append('@ =============================================================================')
    lines.append('')

    cursor = REGION_START
    for label, display, block_size, fusion_cards in DECK_BLOCKS:
        # 扫主卡组结束位置（第一个 0x0000 u16）
        scan_off = cursor
        while scan_off < cursor + block_size:
            if struct.unpack_from('<H', rom, scan_off)[0] == 0:
                break
            scan_off += 2
        else:
            raise RuntimeError(f'No terminator in block {label}')
        main_cards = (scan_off - cursor) // 2
        padding_bytes = block_size - main_cards * 2 - 2 - fusion_cards * 2
        if padding_bytes < 0:
            raise RuntimeError(f'Negative padding for {label}')

        gba_addr = GBA_BASE + cursor

        # 头部注释
        cards_comment = f'{main_cards} 张牌'
        if fusion_cards:
            cards_comment += f'，融合卡组 {fusion_cards} 张'
        lines.append('@ -----------------------------------------------------------------------------')
        lines.append(f'@ {display}')
        lines.append(f'@ GBA地址: 0x{gba_addr:08X}  ROM偏移: 0x{cursor:X}')
        lines.append(f'@ {cards_comment}')
        lines.append('@ -----------------------------------------------------------------------------')
        lines.append(f'{label}:')

        off = cursor

        # 主卡组
        for i in range(main_cards):
            so_code = struct.unpack_from('<H', rom, off + i * 2)[0]
            lines.append(fmt_card(so_code, card_info))
        off += main_cards * 2

        # 终止符
        terminator = struct.unpack_from('<H', rom, off)[0]
        if terminator != 0:
            raise RuntimeError(
                f'Expected 0x0000 terminator at 0x{off:X} for {label}, got 0x{terminator:04X}')
        lines.append('    .hword 0    @ 卡组终止符')
        off += 2

        # 融合卡组
        if fusion_cards:
            lines.append(f'    @ 融合卡组（{fusion_cards} 张）')
            for i in range(fusion_cards):
                so_code = struct.unpack_from('<H', rom, off + i * 2)[0]
                lines.append(fmt_card(so_code, card_info))
            off += fusion_cards * 2

        # 剩余 padding
        if padding_bytes:
            pad_data = rom[off:off + padding_bytes]
            lines.append(f'    @ padding/其他数据（{padding_bytes} 字节）')
            lines.extend(fmt_byte_lines(pad_data))
            off += padding_bytes

        lines.append('')
        cursor += block_size

    if cursor != REGION_END:
        raise RuntimeError(f'Cursor ended at 0x{cursor:X}, expected 0x{REGION_END:X}')

    return '\n'.join(lines) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print(f'ERROR: {ROM_PATH} not found', file=sys.stderr)
        sys.exit(1)

    rom = open(ROM_PATH, 'rb').read()
    card_info = load_card_info(project_root)
    print(f'卡名/密码映射: {len(card_info)} 条')

    # sanity: total block size
    total = sum(bs for _, _, bs, _ in DECK_BLOCKS)
    expected = REGION_END - REGION_START
    print(f'Block 总大小: 0x{total:X} (期望 0x{expected:X})')
    if total != expected:
        print(f'ERROR: size mismatch', file=sys.stderr)
        sys.exit(1)

    asm = generate_asm(rom, card_info)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print(f'汇编文件: {ASM_OUT}  ({len(asm)} bytes)')
    print('完成。')


if __name__ == '__main__':
    main()
