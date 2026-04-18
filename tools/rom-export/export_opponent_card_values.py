#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对手卡值块 (Opponent Card Values) 导出脚本

从 roms/2343.gba 导出 ROM 0x1E58D0E ~ 0x1E5906E 区域：
27 条目 × 32 字节 = 864 字节

每条结构:
  +0x00  u16  card_value（卡牌实力值，SO code）
  +0x02  u16  unk（0x1F40 起递增）
  +0x04  20B  path 字符串（ASCII，null-pad）
  +0x18  6B   零填充（path 超长时溢出到此区）
  +0x1E  u16  unk_b（= unk + 1）

输出:
  data/opponent-card-values.s

来源文档: doc/um06-romhacking-resource/opponents-coinflip-screen.md
"""

import os
import re
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/opponent-card-values.s'

REGION_START = 0x1E58D0E
ENTRY_SIZE = 32
NUM_ENTRIES = 27

# 27 个对手显示名，按 ROM 顺序
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


def fmt_byte_list(data: bytes) -> str:
    return ', '.join(str(b) for b in data)


def path_comment(first20: bytes) -> str:
    """根据前 20B 构造 path 注释。"""
    # 找第一个 null 截断
    null_idx = first20.find(b'\0')
    if null_idx == -1:
        # path 占满 20B，可能还跨到后 6B (脚本不在此判断)
        return f'@ "{first20.decode("ascii")}"'
    # path < 20B，有 null-pad
    path_str = first20[:null_idx].decode('ascii')
    return f'@ "{path_str}" + null-pad'


def generate_asm(rom, card_info):
    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 对手卡值块数据（Opponent Card Values）')
    lines.append(f'@ ROM偏移: 0x{REGION_START:X} - 0x{REGION_START + NUM_ENTRIES * ENTRY_SIZE - 1:X}'
                 f'（共 {NUM_ENTRIES} 条目 × {ENTRY_SIZE} 字节 = {NUM_ENTRIES * ENTRY_SIZE} 字节）')
    lines.append('@')
    lines.append('@ 每条目结构（32 字节）:')
    lines.append('@   +0x00  2字节  card_value（卡牌实力值，SO code）')
    lines.append('@   +0x02  2字节  unk（0x1F40 起递增，用途不明）')
    lines.append('@   +0x04  20字节 文件路径字符串（null-padded，如 deck/LV1_kuriboh.ydc）')
    lines.append('@   +0x18  6字节  全零填充')
    lines.append('@   +0x1E  2字节  unk_b（= unk + 1）')
    lines.append('@')
    lines.append('@ 来源文档: doc/um06-romhacking-resource/opponents-coinflip-screen.md')
    lines.append('@ 由 tools/rom-export/export_opponent_card_values.py 生成')
    lines.append('@ =============================================================================')
    lines.append('')
    lines.append('opponent_card_values:')

    for i in range(NUM_ENTRIES):
        off = REGION_START + i * ENTRY_SIZE
        card_value = struct.unpack_from('<H', rom, off + 0x00)[0]
        unk        = struct.unpack_from('<H', rom, off + 0x02)[0]
        path20     = rom[off + 0x04:off + 0x18]  # 20 bytes
        pad6       = rom[off + 0x18:off + 0x1E]  # 6 bytes
        unk_b      = struct.unpack_from('<H', rom, off + 0x1E)[0]

        name_display = OPPONENT_NAMES[i]

        # Mirror Match 特例：card_value=4007(BEWD) 只是占位，实际对手是镜像——
        # 注释用对手名而非 BEWD 卡名。
        if name_display == 'Mirror Match':
            cv_comment = f'card_value: {name_display}'
        else:
            info = card_info.get(card_value)
            if info:
                cv_name, cv_pw = info
                cv_pw_str = cv_pw.zfill(8) if cv_pw else '?'
                cv_comment = f'card_value: {cv_name} (密码: {cv_pw_str})'
            else:
                cv_comment = f'card_value: SO=0x{card_value:04X}'

        lines.append(f'    @ --- {name_display} ---')
        lines.append(f'    .hword {card_value:5d}    @ {cv_comment}')
        lines.append(f'    .hword 0x{unk:04X}    @ unk')
        lines.append(f'    .byte {fmt_byte_list(path20)}    {path_comment(path20)}')
        lines.append(f'    .byte {fmt_byte_list(pad6)}    @ 6字节填充')
        lines.append(f'    .hword 0x{unk_b:04X}    @ unk_b')
        lines.append('')

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
