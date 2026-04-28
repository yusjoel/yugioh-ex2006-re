#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JA UI 字符串表 (deck-strings, 现 JA 全 UI text) 导出脚本

ROM 0x1DB9C10 ~ 0x1DC4620 = 完整 JA UI 文字 (~1597 条)
- STRING_TABLE_BASE = 0x1DB9C10 (此区起点 = pointer 表 base)
- 与 EN/DE/FR/IT/ES UI text (game-strings 区, 0x1DC4620~0x1DFF9E4) 平行
- 含 7 SD + 25 OPP 名 (slot[5] = JA pointer 指向, 在 0x1DBF02C / 0x1DC1D74 起)

输出: data/deck-strings.s  (全 .byte 形式; 无 .incbin 间隙)
"""
import os
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/game-strings-ja.s'

JA_START = 0x1DB9C10
JA_END   = 0x1DC4620  # exclusive

# Pointer table 中已知的 JA 串 label (从 SD/OPP 槽 slot[5] 解析)
SD_TABLE_OFFSET = 0x4CAC
OPP_TABLE_OFFSET = 0x815C
SLOT_SIZE = 0x18
SD_NAMES = [
    'Starter Deck', "Dragon's Roar", 'Zombie Madness', 'Blazing Destruction',
    'Fury From the Deep', "Warrior's Triumph", "Spellcaster's Judgement",
]
OPP_NAMES = [
    'Kuriboh', 'Scapegoat', 'Skull Servant', 'Watapon', 'Pikeru',
    'Batteryman C', 'Ojama Yellow', 'Goblin King', 'Des Frog', 'Water Dragon',
    'REDD', 'Vampire Genesis', 'Infernal Flame Emperor', 'Ocean Dragon Lord',
    'Helios Duo Megiste', 'Gilford the Legend', 'Dark Eradicator Warlock',
    'Guardian Exode', 'Goldd', 'Electrum', 'Raviel', 'Horus', 'Stronghold',
    'Sacred Phoenix', 'Cyber End Dragon',
]


def read_pointer_labels(rom):
    """从 SD/OPP 指针表读取 slot[5] (JA) 指针, 返回 {addr: label} dict."""
    labels = {}
    for i, name in enumerate(SD_NAMES):
        slot = SD_TABLE_OFFSET + i * SLOT_SIZE
        ja_ptr, = struct.unpack_from('<I', rom, slot + 5*4)
        addr = JA_START + ja_ptr
        labels[addr] = (f'deck_str_xx_sd_{i:02d}', name)
    for i, name in enumerate(OPP_NAMES):
        slot = OPP_TABLE_OFFSET + i * SLOT_SIZE
        ja_ptr, = struct.unpack_from('<I', rom, slot + 5*4)
        addr = JA_START + ja_ptr
        labels[addr] = (f'deck_str_xx_opp_{i:02d}', name)
    return labels


def fmt_byte_line(indent, data):
    return indent + '.byte ' + ', '.join(f'0x{b:02X}' for b in data)


def export(rom):
    labels = read_pointer_labels(rom)
    lines = []
    lines.append('@ JA UI 字符串表 (历史名 deck-strings, 实为 JA 全 UI text)')
    lines.append('@ 由 tools/rom-export/export_deck_strings.py 生成')
    lines.append('@')
    lines.append(f'@ ROM 偏移: 0x{JA_START:X} ~ 0x{JA_END:X}  ({JA_END - JA_START} 字节)')
    lines.append(f'@ STRING_TABLE_BASE = 0x{JA_START:X} (= 起点; 5 lang 平行表在 game-strings.s)')
    lines.append('@')
    lines.append('@ Pointer table 中 SD/OPP slot[5] = JA pointer, 命名 deck_str_xx_{sd|opp}_NN')
    lines.append('@   SD: 0x4CAC, 7 槽 × 24B; OPP: 0x815C, 25 槽 × 24B')
    lines.append('@ 其余 ~1565 条无 pointer-table 引用 (代码内硬编码地址或顺序索引)')
    lines.append('')
    lines.append('@ ============================================================')
    lines.append('deck_str_xx:')
    lines.append('')

    # Pre-scan: 决定哪些 \0 区域是 leading-pad (区段开头), 哪些是 entry-tail-pad,
    # 哪些是 named-label-empty-string (如 OPP[24] 是 0 字节空串).
    # 策略: 顺序扫描; 遇到 label 位置 → 打 label; 之后的非零字节 = data, 之后 \0 = pad
    pos = JA_START
    str_seq = 0
    # 区段开头若是 \0, 视为 leading pad (全局头), 不归任何 entry
    if rom[pos] == 0:
        j = pos
        while j < JA_END and rom[j] == 0 and j not in labels:
            j += 1
        n = j - pos
        if n > 0:
            if n == 1: lines.append('\t.byte 0x00')
            else: lines.append(f'\t.zero {n}')
            pos = j

    while pos < JA_END:
        # 起 label (每次 entry 起点必定打 label)
        if pos in labels:
            lname, comment = labels[pos]
            lines.append(f'\n{lname}:  @ {comment}')
        else:
            lines.append(f'\ndeck_str_xx_{str_seq:05d}:')
            str_seq += 1
        # 移至 data (从此位置往后)
        s = pos
        # 第一步 advance: 至少消费 1 个 byte (data 或 pad), 避免 0-byte 字符串导致死循环
        # 实际: 0-byte 字符串 → data 段长 0, pad 段必须吞掉 \0 否则下一轮重入相同 pos
        # 解法: 数据扫到非零结束, pad 扫到下一 label-or-non-zero, 都不带 'pos in labels' 检查
        while pos < JA_END and rom[pos] != 0:
            pos += 1
        data = rom[s:pos]
        for k in range(0, len(data), 16):
            lines.append(fmt_byte_line('\t', data[k:k+16]))
        # tail pad: 吞 \0 直到 (1) 非零 或 (2) 下一 label 位置 (但不含当前 entry 起点)
        pad_start = pos
        first_pad = True
        while pos < JA_END and rom[pos] == 0:
            # 当前 pos 是 label 位置 + 已不是当前 entry 的起点 → 停 (留给下一 entry)
            if pos in labels and not first_pad:
                break
            # 边界情况: 当前 entry 是 0-byte 数据 (data 段长=0, pad_start == s == 当前 label 位置)
            # 此时 pos == s, pos 是当前 label 位置. 第一个 \0 必须吞 (是当前 entry 的 pad).
            pos += 1
            first_pad = False
        pad_n = pos - pad_start
        if pad_n == 1:
            lines.append('\t.byte 0x00')
        elif pad_n >= 2:
            lines.append(f'\t.zero {pad_n}')

    return '\n'.join(lines) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print(f'ERROR: {ROM_PATH} not found', file=sys.stderr)
        sys.exit(1)

    rom = open(ROM_PATH, 'rb').read()
    asm = export(rom)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print(f'wrote {ASM_OUT}  ({len(asm)} chars)')
    print(f'JA region: 0x{JA_START:X} ~ 0x{JA_END:X}  ({JA_END - JA_START}B)')


if __name__ == '__main__':
    main()
