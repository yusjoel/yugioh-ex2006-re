#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deck Record Table 导出脚本（原名 opponent-card-values）

从 roms/2343.gba 导出 ROM 0x1E58D0C..0x1E59C2C 区域：
121 条记录 × 32 字节 = 3872 字节 = 0xF20 字节

每条结构（32 字节）:
  +0x00  u16  deck_id        (in-game deck ID, 3 段连续 + 跳跃)
  +0x02  u16  card_value     (SO code, deck strength signal card)
  +0x04  u16  deck_id_dup    (第二 ID, opponent 段 = deck_id, theme/limited 段独立)
  +0x06  26B  path           (null-padded "deck/LVN_xxx.ydc" / "deck/theme_NNN.ydc" / "deck/limit_NNN.ydc")

3 段（按记录索引连续，但 deck_id 跳跃）:
  rec[  0..26]  Opponent  deck_id 0x1F40..0x1F5A   path deck/LVN_xxx.ydc (含 2 dummy)
  rec[ 27..78]  Theme     deck_id 0x2711..0x2744   path deck/theme_NNN.ydc
  rec[ 79..120] Limited   deck_id 0x4E20..0x4E49   path deck/limit_NNN.ydc

代码访问: 见 FUN_0801f3e8 / FUN_080242c8, base=0x09E58D0C, stride=32, 循环上限 r1<=0x78
（Ghidra label: deck_record_table @ 0x09E58D0C）

输出:
  data/opponent-card-values.s   (label: deck_record_table)
"""

import os
import re
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/opponent-card-values.s'

REGION_START = 0x1E58D0C
ENTRY_SIZE = 32
NUM_ENTRIES = 121
REGION_END = REGION_START + NUM_ENTRIES * ENTRY_SIZE  # 0x1E59C2C

# 27 个 opponent 段显示名（rec[0..26]）
OPPONENT_NAMES = [
    'Kuriboh', 'Scapegoat', 'Skull Servant', 'Watapon', 'Pikeru',
    'Batteryman C', 'Ojama Yellow', 'Goblin King', 'Des Frog', 'Water Dragon',
    'Red Eyes Darkness Dragon', 'Vampire Genesis', 'Infernal Flame Emperor',
    'Ocean Dragon Lord Neo D', 'Helios Duo Megiste',
    'Gilford the Legend', 'Dark Eradicator Warlock', 'Guardian Exode',
    'Goldd Wu-Lord of Dark', 'Elemental Hero Electrum', 'Raviel Lord of Phantasms',
    'Horus the Black Flame D', 'Stronghold', 'Sacred Phoenix of N',
    'Cyber End Dragon', 'Mirror Match', 'Copycat',
]


def load_card_info(project_root):
    """从 doc/um06-deck-modification-tool/data.md 读 SO code → (name, passcode)。"""
    path = os.path.join(project_root, 'doc/um06-deck-modification-tool/data.md')
    mapping = {}
    pattern = re.compile(
        r'\|\s*(\d{7,9})\s*\|([^|]+)\|[^|]*\|\s*([0-9A-Fa-f]{4})\s*\|'
    )
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                pw      = m.group(1)
                name    = m.group(2).strip()
                slot_id = int(m.group(3), 16)
                mapping[slot_id] = (name, pw)
    return mapping


def fmt_byte_list(data):
    return ', '.join(str(b) for b in data)


def category(deck_id):
    if deck_id < 0x2000:
        return 'opponent'
    if deck_id < 0x4000:
        return 'theme'
    return 'limited'


def cv_comment(card_value, name_hint, card_info):
    # Mirror Match 特例: card_value=4007(BEWD) 是占位
    if name_hint == 'Mirror Match':
        return 'card_value: Mirror Match (= BEWD 占位)'
    info = card_info.get(card_value)
    if info:
        cv_name, cv_pw = info
        cv_pw_str = cv_pw.zfill(8) if cv_pw else '?'
        return 'card_value: %s (密码: %s)' % (cv_name, cv_pw_str)
    return 'card_value: SO=0x%04X' % card_value


def path_label(path26):
    null_idx = path26.find(b'\x00')
    if null_idx == -1:
        return path26.decode('ascii', errors='replace')
    return path26[:null_idx].decode('ascii', errors='replace')


def generate_asm(rom, card_info):
    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ Deck Record Table（原名 opponent_card_values）')
    lines.append('@ ROM偏移: 0x%X - 0x%X（共 %d 条记录 × %d 字节 = 0x%X = %d 字节）' % (
        REGION_START, REGION_END - 1, NUM_ENTRIES, ENTRY_SIZE,
        NUM_ENTRIES * ENTRY_SIZE, NUM_ENTRIES * ENTRY_SIZE))
    lines.append('@')
    lines.append('@ 每条记录（32 字节）:')
    lines.append('@   +0x00  u16  deck_id        (in-game deck ID, 三段不连续)')
    lines.append('@   +0x02  u16  card_value     (SO code, deck 实力信号卡)')
    lines.append('@   +0x04  u16  deck_id_dup    (opponent 段 = deck_id, theme/limited 段独立)')
    lines.append('@   +0x06  26B  path           (null-padded ASCII)')
    lines.append('@')
    lines.append('@ 三段（按记录索引连续，deck_id 跳跃）:')
    lines.append('@   rec[  0..26]  Opponent  deck_id 0x1F40..0x1F5A   含 rec[25]/[26] dummy slot')
    lines.append('@   rec[ 27..78]  Theme     deck_id 0x2711..0x2744')
    lines.append('@   rec[ 79..120] Limited   deck_id 0x4E20..0x4E49')
    lines.append('@')
    lines.append('@ 代码 base 引用: FUN_0801f3e8 (查 deck_id 返回索引), FUN_080242c8')
    lines.append('@ Ghidra label: deck_record_table @ 0x09E58D0C; 循环上限 r1<=0x78')
    lines.append('@ 由 tools/rom-export/export_opponent_card_values.py 生成')
    lines.append('@ =============================================================================')
    lines.append('')
    lines.append('deck_record_table:')
    lines.append('opponent_card_values:    @ 历史别名（保留兼容引用）')
    lines.append('')

    last_cat = None
    for i in range(NUM_ENTRIES):
        off = REGION_START + i * ENTRY_SIZE
        deck_id     = struct.unpack_from('<H', rom, off + 0x00)[0]
        card_value  = struct.unpack_from('<H', rom, off + 0x02)[0]
        deck_id_dup = struct.unpack_from('<H', rom, off + 0x04)[0]
        path26      = rom[off + 0x06:off + 0x20]  # 26 bytes

        cat = category(deck_id)
        if cat != last_cat:
            lines.append('    @ ============== %s 段 ==============' % cat.upper())
            last_cat = cat

        path_str = path_label(path26)
        # opponent 段附带 OPPONENT_NAMES，theme/limited 用 path basename
        if cat == 'opponent' and i < len(OPPONENT_NAMES):
            display_name = OPPONENT_NAMES[i]
        else:
            display_name = path_str

        lines.append('    @ rec[%3d] @ 0x%07X (%s)' % (i, off, display_name))
        lines.append('    .hword 0x%04X            @ deck_id' % deck_id)
        lines.append('    .hword %5d              @ %s' % (card_value, cv_comment(card_value, display_name, card_info)))
        lines.append('    .hword 0x%04X            @ deck_id_dup' % deck_id_dup)
        lines.append('    .byte %s    @ path: "%s"' % (fmt_byte_list(path26), path_str))
        lines.append('')

    return '\n'.join(lines) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print('ERROR: %s not found' % ROM_PATH, file=sys.stderr)
        sys.exit(1)

    rom = open(ROM_PATH, 'rb').read()
    card_info = load_card_info(project_root)
    print('卡名/密码映射: %d 条' % len(card_info))

    asm = generate_asm(rom, card_info)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print('汇编文件: %s  (%d bytes)' % (ASM_OUT, len(asm)))
    print('完成。%d 条 record × %d B = 0x%X B' % (NUM_ENTRIES, ENTRY_SIZE, NUM_ENTRIES * ENTRY_SIZE))


if __name__ == '__main__':
    main()
