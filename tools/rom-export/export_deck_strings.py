#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡组名字符串表 (Deck Strings) 导出脚本

从 roms/2343.gba 导出 ROM 0x1DBF01A ~ 0x1DC4620 区域：
含 XX 自定义编码的 SD 预组名 (7 条) + OPP 对手卡组名 (25 条)，
两段之间及尾部是其它语言字符串 / 代码的 .incbin 间隙。

XX 编码: 每字符 2 字节 (字节范围 0xF0-0xFF)，非 ASCII，含义未解码。
终止符 0x00；除 block 末条外每条 data 后再 pad 一字节 0x00 (2字节对齐)。

输出:
  data/deck-strings.s

来源文档: doc/um06-romhacking-resource/deck-string-name-tool.md
          doc/um06-romhacking-resource/modifying-decks.md
"""

import os
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/deck-strings.s'

# XX SD: 7 条预组/初始卡组名
SD_START = 0x1DBF01A
SD_END   = 0x1DBF081  # exclusive
SD_NAMES = [
    'Starter Deck',
    "Dragon's Roar",
    'Zombie Madness',
    'Blazing Destruction',
    'Fury From the Deep',
    "Warrior's Triumph",
    "Spellcaster's Judgement",
]

# XX SD 后 incbin 间隙
SD_GAP_START = SD_END
SD_GAP_LEN   = 0x2CDF  # → 0x1DC1D60

# XX OPP: 25 条对手卡组名
OPP_START = 0x1DC1D60
OPP_END   = 0x1DC1EF1  # exclusive
OPP_NAMES = [
    'Kuriboh', 'Scapegoat', 'Skull Servant', 'Watapon', 'Pikeru',
    'Batteryman C', 'Ojama Yellow', 'Goblin King', 'Des Frog', 'Water Dragon',
    'REDD', 'Vampire Genesis', 'Infernal Flame Emperor', 'Ocean Dragon Lord',
    'Helios Duo Megiste', 'Gilford the Legend', 'Dark Eradicator Warlock',
    'Guardian Exode', 'Goldd', 'Electrum', 'Raviel', 'Horus', 'Stronghold',
    'Sacred Phoenix', 'Cyber End Dragon',
]

# XX OPP 后 incbin 间隙（游戏文本 0x1DC4620 前）
OPP_GAP_START = OPP_END
OPP_GAP_LEN   = 0x272F  # → 0x1DC4620


def parse_strings(rom, start, end, expected_count):
    """按 0x00 切分字符串。
    返回 [(data_bytes, pad_len)]，pad_len 为 data 之后的 0x00 字节数 (1 或 2)。"""
    pos = start
    strings = []
    while pos < end:
        data_start = pos
        while pos < end and rom[pos] != 0:
            pos += 1
        data = rom[data_start:pos]
        # count trailing 0x00 run
        pad = 0
        while pos < end and rom[pos] == 0 and pad < 2:
            pad += 1
            pos += 1
        strings.append((data, pad))
    if len(strings) != expected_count:
        raise RuntimeError(f'Expected {expected_count} strings in [0x{start:X},0x{end:X}), got {len(strings)}')
    return strings


def fmt_byte_line(indent: str, data: bytes) -> str:
    return indent + '.byte ' + ', '.join(f'0x{b:02X}' for b in data)


def generate_asm(rom):
    sd_strings  = parse_strings(rom, SD_START,  SD_END,  len(SD_NAMES))
    opp_strings = parse_strings(rom, OPP_START, OPP_END, len(OPP_NAMES))

    lines = []
    lines.append('@ 卡组名字符串表')
    lines.append('@ 来源: doc/um06-romhacking-resource/deck-string-name-tool.md')
    lines.append('@        doc/um06-romhacking-resource/modifying-decks.md')
    lines.append('@ 由 tools/rom-export/export_deck_strings.py 生成')
    lines.append('@')
    lines.append(f'@ ROM 文件偏移范围: 0x{SD_START:X} ~ 0x1DFC852')
    lines.append('@ 字符串表基址（文件偏移）: 0x1DB9C10  (GBA地址 0x9DB9C10)')
    lines.append('@')
    lines.append('@ 游戏包含 6 种语言的卡组名字符串：')
    lines.append('@   XX（自定义编码）、EN（英语）、DE（德语）、FR（法语）、IT（意大利语）、ES（西班牙语）')
    lines.append('@ 各语言分两组：SD（预组/初始卡组名 7条）、OPP（对手卡组名 25条）')
    lines.append('@')
    lines.append('@ 指针表位置（代码区，文件偏移）：')
    lines.append('@   对手卡组名指针表: 0x8150，步长 24 字节，EN槽偏移 +0xC')
    lines.append('@   预组/初始卡组名指针表: 0x4CA0，步长 24 字节，EN槽偏移 +0xC')
    lines.append('')
    lines.append('@ ========================================================')
    lines.append('@ 未知（自定义编码） - 预组/初始卡组名')
    lines.append(f'@ ROM 偏移: 0x{SD_START:X} ~ 0x{SD_END:X}'
                 f'  ({SD_END - SD_START} 字节)')
    lines.append('@ ========================================================')
    lines.append('deck_str_xx_sd:')
    lines.append('')

    for (data, pad), name in zip(sd_strings, SD_NAMES):
        lines.append(f'\t@ {name}')
        if data:
            lines.append(fmt_byte_line('\t', data))
        lines.append(fmt_byte_line('\t', b'\0' * pad))
        lines.append('')

    lines.append(f'\t.incbin "roms/2343.gba", 0x{SD_GAP_START:X}, 0x{SD_GAP_LEN:X}')
    lines.append('')
    lines.append('@ ========================================================')
    lines.append('@ 未知（自定义编码） - 对手卡组名')
    lines.append(f'@ ROM 偏移: 0x{OPP_START:X} ~ 0x{OPP_END:X}'
                 f'  ({OPP_END - OPP_START} 字节)')
    lines.append('@ ========================================================')
    lines.append('deck_str_xx_opp:')
    lines.append('')

    for i, ((data, pad), name) in enumerate(zip(opp_strings, OPP_NAMES)):
        lines.append(f'\t@ {name}')
        if data:
            lines.append(fmt_byte_line('\t', data))
        lines.append(fmt_byte_line('\t', b'\0' * pad))
        if i < len(OPP_NAMES) - 1:
            lines.append('')

    lines.append(f'\t.incbin "roms/2343.gba", 0x{OPP_GAP_START:X}, 0x{OPP_GAP_LEN:X}'
                 f'  @ 间隙：直到游戏文本开始（0x{OPP_GAP_START + OPP_GAP_LEN - 1:X}）')
    lines.append('')
    lines.append('@ 后续内容见 data/game-strings.s（0x1DC4620 起）')

    return '\n'.join(lines) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print(f'ERROR: {ROM_PATH} not found', file=sys.stderr)
        sys.exit(1)

    rom = open(ROM_PATH, 'rb').read()
    asm = generate_asm(rom)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print(f'汇编文件: {ASM_OUT}  ({len(asm)} bytes)')
    print('完成。')


if __name__ == '__main__':
    main()
