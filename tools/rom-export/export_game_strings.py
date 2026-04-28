#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
game-strings 导出脚本

从 roms/2343.gba 读取游戏文本字符串，导出为各语言汇编文件。

ROM 范围: 0x1DC4620 ~ 0x1DFF9E3
包含 5 种语言（EN/DE/FR/IT/ES）的游戏文本，Latin-1 编码。
各 lang region_end 已含其自身的 9 行 Death Message tail (18 B \\0) + 必要对齐 pad,
对应 master pointer table rows 1642..1650 的 \\0\\0 槽 (5 lang 无翻译).

指针表结构（位于 ROM 低地址区）：
  字符串表基地址 (STRING_TABLE_BASE) = 0x1DB9C10
  sd  指针表：ROM 文件偏移 0x4CAC，共 7 槽，每槽 0x18 字节
  opp 指针表：ROM 文件偏移 0x815C，共 25 槽，每槽 0x18 字节
  每槽 = [EN指针(4B), DE指针(4B), FR指针(4B), IT指针(4B), ES指针(4B), 其他(4B)]
  指针值 = 字符串地址 - STRING_TABLE_BASE

输出文件：
  data/game-strings-en.s
  data/game-strings-de.s
  data/game-strings-fr.s
  data/game-strings-it.s
  data/game-strings-es.s

注: 本脚本只是初始导出, 真正构建用的 .s 由 tools/game-strings/encode_txt_to_s.py
重写 (走 text/game-strings/*.txt 闭环, master-table-driven, label 对齐 pointer-table).
"""

import os
import struct
import sys

ROM_PATH = 'roms/2343.gba'
OUT_DIR  = 'data'

# 字符串表基地址（指针值的参考点）
STRING_TABLE_BASE = 0x1DB9C10

# 各语言的 ROM 文件偏移范围（闭区间）
LANG_RANGES = {
    'en': (0x1DC4620, 0x1DCF483),
    'de': (0x1DCF484, 0x1DDB7F1),
    'fr': (0x1DDB7F2, 0x1DE7CC9),
    'it': (0x1DE7CCA, 0x1DF3C79),
    'es': (0x1DF3C7A, 0x1DFF9E3),
}

# 各语言在指针表槽中的下标（0=EN, 1=DE, 2=FR, 3=IT, 4=ES）
LANG_IDX = {'en': 0, 'de': 1, 'fr': 2, 'it': 3, 'es': 4}

LANG_NAMES = {
    'en': 'English (EN)',
    'de': 'German (DE)',
    'fr': 'French (FR)',
    'it': 'Italian (IT)',
    'es': 'Spanish (ES)',
}

# SD 指针表：ROM文件偏移 0x4CAC，7槽，每槽0x18字节
SD_TABLE_OFFSET = 0x4CAC
SD_COMMENTS = [
    'Starter Deck',
    "Dragon's Roar",
    'Zombie Madness',
    'Blazing Destruction',
    'Fury From the Deep',
    "Warrior's Triumph",
    "Spellcaster's Judgement",
]

# OPP 指针表：ROM文件偏移 0x815C，25槽，每槽0x18字节
OPP_TABLE_OFFSET = 0x815C
OPP_COMMENTS = [
    'Kuriboh', 'Scapegoat', 'Skull Servant', 'Watapon', 'Pikeru',
    'Batteryman C', 'Ojama Yellow', 'Goblin King', 'Des Frog', 'Water Dragon',
    'Red-Eyes DD', 'Vampire Genesis', 'Infernal FE', 'Ocean Dragon Lord', 'Helios Duo',
    'Gilford', 'Dark Eradicator', 'Guardian Exode', 'Goldd', 'Electrum',
    'Raviel', 'Horus', 'Stronghold', 'Sacred Phoenix', 'Cyber End',
]

SLOT_SIZE = 0x18  # 每槽 24 字节（5语言指针 × 4B + 4B其他）


def read_label_offsets(rom: bytes, lang: str) -> dict:
    """从 ROM 指针表读取各标签的绝对 ROM 文件偏移。
    返回 {rom_offset: (label_name, comment)} 字典。
    """
    idx = LANG_IDX[lang]
    labels = {}

    for i, comment in enumerate(SD_COMMENTS):
        slot_off = SD_TABLE_OFFSET + i * SLOT_SIZE + idx * 4
        ptr_val, = struct.unpack_from('<I', rom, slot_off)
        str_addr = STRING_TABLE_BASE + ptr_val
        labels[str_addr] = (f'deck_str_{lang}_sd_{i:02d}', comment)

    for i, comment in enumerate(OPP_COMMENTS):
        slot_off = OPP_TABLE_OFFSET + i * SLOT_SIZE + idx * 4
        ptr_val, = struct.unpack_from('<I', rom, slot_off)
        str_addr = STRING_TABLE_BASE + ptr_val
        labels[str_addr] = (f'deck_str_{lang}_opp_{i:02d}', comment)

    return labels


def asm_escape(raw: bytes) -> str:
    """将字节序列转换为 GAS .ascii 字面量内容（Latin-1 源文件）。"""
    parts = []
    for b in raw:
        if   b == 0x22: parts.append('\\"')        # 双引号
        elif b == 0x5C: parts.append('\\\\')       # 反斜杠
        elif b == 0x0A: parts.append('\\n')
        elif b == 0x0D: parts.append('\\r')
        elif b == 0x09: parts.append('\\t')
        elif b == 0x00: parts.append('\\0')        # null 终止符
        elif 0x20 <= b < 0x7F:  parts.append(chr(b))           # 可打印 ASCII
        elif 0x80 <= b <= 0x9F:                                # CP1252 扩展字符
            try:    parts.append(bytes([b]).decode('cp1252'))
            except (UnicodeDecodeError, ValueError):
                    parts.append(f'\\x{b:02x}')               # 未定义字节（0x81等）
        elif 0xA0 <= b <= 0xFF: parts.append(chr(b))           # 可打印 Latin-1 / CP1252
        else:                   parts.append(f'\\x{b:02x}')   # 控制字符
    return ''.join(parts)


def export_language(rom: bytes, lang: str, start: int, end: int,
                    labels: dict, out_dir: str):
    """导出单个语言的字符串块为 .s 文件。"""
    data = rom[start:end + 1]  # 闭区间
    lines = []
    i = 0
    str_seq = 1  # 顺序标签计数器

    while i < len(data):
        rom_off = start + i

        # 此位置有标签则先输出（标签始终位于字符串起始处，非 null 字节）
        if rom_off in labels:
            name, comment = labels[rom_off]
            lines.append(f'\n{name}:  @ {comment}\n')

        if data[i] == 0:
            # 连续 null 字节 → .zero N
            j = i
            while j < len(data) and data[j] == 0:
                j += 1
            lines.append(f'\t.zero {j - i}\n')
            i = j
        else:
            # 非 null 字节开始：若无具名标签，分配顺序标签
            if rom_off not in labels:
                lines.append(f'\ngame_str_{lang}_{str_seq:05d}:\n')
                str_seq += 1

            # 读取非 null 字节
            j = i
            while j < len(data) and data[j] != 0:
                j += 1

            # 统计紧随其后的连续 null 字节数
            null_end = j
            while null_end < len(data) and data[null_end] == 0:
                null_end += 1
            null_count = null_end - j

            # .ascii 最多含 2 个 \0，超出部分用 .zero
            nulls_in_ascii = min(null_count, 2)
            string_bytes = data[i:j + nulls_in_ascii]
            lines.append(f'\t.ascii "{asm_escape(string_bytes)}"\n')
            i = j + nulls_in_ascii

            remaining_nulls = null_count - nulls_in_ascii
            if remaining_nulls > 0:
                lines.append(f'\t.zero {remaining_nulls}\n')
                i += remaining_nulls

    out_path = os.path.join(out_dir, f'game-strings-{lang}.s')
    header = (
        f'@ data/game-strings-{lang}.s\n'
        f'@ {LANG_NAMES[lang]} game strings\n'
        f'@ ROM range: 0x{start:07X} ~ 0x{end:07X}\n'
        f'@ Generated by tools/rom-export/export_game_strings.py\n'
        f'@\n'
        f'@ File encoding: CP1252 (Windows-1252)\n'
        f'@   Printable Latin-1 chars (0xA0-0xFF) written directly\n'
        f'@   CP1252 extended chars (0x80-0x9F, e.g. „") written directly\n'
        f'@   Undefined CP1252 bytes and C0 control bytes use \\xNN escape\n'
        f'@ Labels deck_str_{{lang}}_{{sd|opp}}_NN: from pointer table entries\n'
        f'@ Labels game_str_{{lang}}_NNNNN: sequential labels for all other strings\n'
        f'\n'
    )

    with open(out_path, 'w', encoding='cp1252') as f:
        f.write(header)
        f.writelines(lines)

    str_count  = sum(1 for l in lines if l.strip().startswith('.ascii'))
    zero_count = sum(1 for l in lines if l.strip().startswith('.zero'))
    print(f'[{lang.upper()}] {out_path}  字符串: {str_count}  padding块: {zero_count}  字节: {len(data)}')


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print(f'错误：ROM 文件 {ROM_PATH} 不存在', file=sys.stderr)
        sys.exit(1)

    print(f'读取 {ROM_PATH} ...')
    with open(ROM_PATH, 'rb') as f:
        rom = f.read()

    for lang in ['en', 'de', 'fr', 'it', 'es']:
        start, end = LANG_RANGES[lang]
        labels = read_label_offsets(rom, lang)
        export_language(rom, lang, start, end, labels, OUT_DIR)

    # 生成 6 lang 聚合 wrapper (asm/rom.s 引用的是这个)
    # JA 在最前 (ROM 顺序), EN..ES 紧随
    wrapper_path = os.path.join(OUT_DIR, 'game-strings.s')
    with open(wrapper_path, 'w', encoding='utf-8') as f:
        f.write(
            '@ data/game-strings.s\n'
            '@ 游戏文本字符串表 (6 lang wrapper)\n'
            '@ ROM 偏移: 0x1DB9C10 ~ 0x1DFF9E3 (含 JA 区 + 5 lang 区, 各含 9 行 Death Message tail)\n'
            '@\n'
            '@ 6 lang: JA + EN + DE + FR + IT + ES\n'
            '@   JA: 0x1DB9C10 ~ 0x1DC461F  (43,536 B)\n'
            '@   EN: 0x1DC4620 ~ 0x1DCF483  (44,644 B)\n'
            '@   DE: 0x1DCF484 ~ 0x1DDB7F1  (50,030 B)\n'
            '@   FR: 0x1DDB7F2 ~ 0x1DE7CC9  (50,392 B)\n'
            '@   IT: 0x1DE7CCA ~ 0x1DF3C79  (49,072 B)\n'
            '@   ES: 0x1DF3C7A ~ 0x1DFF9E3  (48,490 B)\n'
            '@\n'
            '@ Master pointer table @ ROM 0xF40 (1651 行 × 24 B, 顺序 [JA,EN,DE,FR,IT,ES])\n'
            '@   Rows 0..1641: 共享 6 lang UI 文本\n'
            '@   Rows 1642..1650: Death Message 尾巴 (JA 真实日文; 5 lang 全 \\0\\0)\n'
            '@ 见 doc/dev/data-structure/game-strings.md\n'
            '\n'
            '.include "data/game-strings-ja.s"\n'
            '.include "data/game-strings-en.s"\n'
            '.include "data/game-strings-de.s"\n'
            '.include "data/game-strings-fr.s"\n'
            '.include "data/game-strings-it.s"\n'
            '.include "data/game-strings-es.s"\n'
        )
    print(f'[WRAPPER] {wrapper_path}')

    print('完成。请运行 build.bat 验证 byte-identical。')


if __name__ == '__main__':
    main()
