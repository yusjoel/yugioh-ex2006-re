#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始卡组 (Starter Deck) 导出脚本

从 roms/2343.gba 导出 ROM 0x1E5F884 ~ 0x1E5F8EA 区域：
50 张牌 + 终止符 0x0000，共 102 字节 (0x66)。

格式: [so_code u16 LE] 连续排列，以 0x0000 终止。

输出:
  data/starter-deck.s

来源文档: doc/um06-deck-modification-tool/starter-opponent-paste-tool.md
"""

import os
import re
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/starter-deck.s'

REGION_START = 0x1E5F884
MAX_ENTRIES = 50
NAME_COL_WIDTH = 46


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


def generate_asm(rom, card_info):
    entries = []
    for i in range(MAX_ENTRIES):
        so_code = struct.unpack_from('<H', rom, REGION_START + i * 2)[0]
        entries.append(so_code)
    term_off = REGION_START + MAX_ENTRIES * 2
    terminator = struct.unpack_from('<H', rom, term_off)[0]
    if terminator != 0:
        raise RuntimeError(f'Expected 0x0000 terminator at 0x{term_off:X}, got 0x{terminator:04X}')

    total_bytes = (MAX_ENTRIES + 1) * 2

    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 初始卡组数据（Starter Deck）')
    lines.append(f'@ ROM偏移: 0x{REGION_START:X} - 0x{REGION_START + total_bytes - 1:X}'
                 f'（共 {total_bytes} 字节）')
    lines.append('@')
    lines.append('@ 格式: [so_code LE16] 连续排列，以 0x0000 终止')
    lines.append('@ 重复相同 so_code 表示多张副本')
    lines.append('@')
    lines.append('@ 来源文档: doc/um06-deck-modification-tool/starter-opponent-paste-tool.md')
    lines.append('@ 由 tools/rom-export/export_starter_deck.py 生成')
    lines.append('@ =============================================================================')
    lines.append('')
    lines.append('starter_deck:')
    for so_code in entries:
        lines.append(fmt_card(so_code, card_info))
    lines.append('    .hword 0    @ 卡组终止符')
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
