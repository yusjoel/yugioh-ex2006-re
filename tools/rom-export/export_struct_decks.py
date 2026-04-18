#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预组 (Structure Decks) 导出脚本

从 roms/2343.gba 导出 ROM 0x1E5FA58 ~ 0x1E5FD84 区域：
6 个预组 + 指针表（末尾 6 × 8 B），共 0x32C = 812 字节。

布局:
  0x1E5FA58 dragons_roar         28 slots × 4 B
  0x1E5FAC8 zombie_madness       28 slots × 4 B
  0x1E5FB38 molten_destruction   31 slots × 4 B
  0x1E5FBB4 fury_from_the_deep   32 slots × 4 B
  0x1E5FC34 warriors_triumph     36 slots × 4 B
  0x1E5FCC4 spellcasters_judgement 36 slots × 4 B
  0x1E5FD54 struct_deck_table    6 × (u32 ptr, u32 size)

每 slot 4 字节: [so_code*4 | qty, 0x0000] LE（通过 deck_entry 宏）
  qty = word & 3
  so_code = word >> 2

输出:
  data/struct-decks.s

来源文档: doc/um06-deck-modification-tool/data.md
"""

import os
import re
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/struct-decks.s'

PTR_TABLE_OFF = 0x1E5FD54
REGION_END    = 0x1E5FD84  # exclusive
NUM_DECKS = 6
GBA_BASE = 0x08000000

# label → display name (顺序跟 ROM 指针表一致)
DECK_LABELS = [
    ('dragons_roar',           "Dragon's Roar"),
    ('zombie_madness',         'Zombie Madness'),
    ('molten_destruction',     'Molten Destruction'),
    ('fury_from_the_deep',     'Fury from the Deep'),
    ('warriors_triumph',       "Warrior's Triumph"),
    ('spellcasters_judgement', "Spellcaster's Judgement"),
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


def fmt_entry(so_code, qty, card_info):
    info = card_info.get(so_code)
    if info:
        name, pw = info
        pw_str = pw.zfill(8) if pw else '?'
    else:
        name = f'SO=0x{so_code:04X}'
        pw_str = '?'
    qty_suffix = f' ×{qty}' if qty > 1 else ''
    return f'        deck_entry  {so_code}, {qty}    @ {name}{qty_suffix} (密码: {pw_str})'


def parse_ptr_table(rom):
    table = []
    for i in range(NUM_DECKS):
        off = PTR_TABLE_OFF + i * 8
        ptr, size = struct.unpack_from('<II', rom, off)
        table.append((ptr, size))
    return table


def parse_deck(rom, rom_off, slot_count):
    entries = []
    for i in range(slot_count):
        word, pad = struct.unpack_from('<HH', rom, rom_off + i * 4)
        if pad != 0:
            raise RuntimeError(f'Unexpected padding 0x{pad:04X} at 0x{rom_off + i * 4:X}')
        qty = word & 3
        so_code = word >> 2
        entries.append((so_code, qty))
    return entries


def generate_asm(rom, card_info):
    ptr_table = parse_ptr_table(rom)
    decks = []
    total_slots = 0
    for (ptr, size), (label, display) in zip(ptr_table, DECK_LABELS):
        rom_off = ptr - GBA_BASE
        entries = parse_deck(rom, rom_off, size)
        total_cards = sum(qty for _, qty in entries)
        decks.append((label, display, ptr, rom_off, size, entries, total_cards))
        total_slots += size

    region_start = decks[0][3]  # first deck's rom_off
    total_size = REGION_END - region_start

    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 预组数据')
    lines.append(f'@ ROM偏移: 0x{region_start:X} - 0x{REGION_END:X}'
                 f' (共 0x{total_size:X} = {total_size} 字节)')
    lines.append('@')
    lines.append('@ 卡牌编码格式 (每条 4 字节):')
    lines.append('@   字节 0-1: so_code * 4 | 副本数量  [小端 16 位]，通过 deck_entry 宏生成')
    lines.append('@   字节 2-3: 0x0000 (填充)')
    lines.append('@')
    lines.append('@ SO_code: 卡牌在游戏内部数据库中的 16 位标识符')
    lines.append('@ 副本数量: 1 = 1张, 2 = 2张, 3 = 3张')
    lines.append('@')
    lines.append('@ 来源文档: doc/um06-deck-modification-tool/data.md')
    lines.append('@ 由 tools/rom-export/export_struct_decks.py 生成')
    lines.append('@ =============================================================================')
    lines.append('')

    for label, display, ptr, rom_off, size, entries, total_cards in decks:
        lines.append('@ -----------------------------------------------------------------------------')
        lines.append(f'@ {display}')
        lines.append(f'@ GBA地址: 0x{ptr:08X}  ROM偏移: 0x{rom_off:X}')
        lines.append(f'@ {size} 种牌型, 共 {total_cards} 张')
        lines.append('@ -----------------------------------------------------------------------------')
        lines.append(f'{label}:')
        for so_code, qty in entries:
            lines.append(fmt_entry(so_code, qty, card_info))
        lines.append('')

    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('@ 预组指针表')
    lines.append(f'@ GBA地址: 0x{GBA_BASE + PTR_TABLE_OFF:08X}  ROM偏移: 0x{PTR_TABLE_OFF:X}')
    lines.append('@ 格式: [卡组GBA地址 LE32][槽位数 LE32]')
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('struct_deck_table:')
    for (label, display, ptr, _, size, _, _) in decks:
        lines.append(f'    .word 0x{ptr:08X}, 0x{size:08X}    @ {display} ({size} 槽)')

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

    asm = generate_asm(rom, card_info)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print(f'汇编文件: {ASM_OUT}  ({len(asm)} bytes)')
    print('完成。')


if __name__ == '__main__':
    main()
