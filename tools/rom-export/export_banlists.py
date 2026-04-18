#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禁卡表 (banlists) 导出脚本

从 roms/2343.gba 导出 ROM 0x1E5EF30 ~ 0x1E5F6CC 区域：
8 个版本禁卡表，连续存储，共 487 条目 (1948 字节)。
每条 4 字节: [u16 so_code][u16 limit]，limit: 0=禁止, 1=限制, 2=准限制

8 个表的边界从 Data Crystal + 项目早期手写 .s 文件确定（无 ROM 指针表元数据）。

输出:
  data/banlists.s

来源文档: doc/um06-romhacking-resource/modifying-banlists.md
"""

import os
import re
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/banlists.s'

REGION_START = 0x1E5EF30
ENTRY_SIZE = 4

# (label, 标题注释, 条目数) — 顺序连续存储
BANLISTS = [
    ('banlist_default',  'Default（默认）',         44),
    ('banlist_no_ban_1', 'No Ban 1（无禁卡版本1）', 39),
    ('banlist_no_ban_2', 'No Ban 2（无禁卡版本2）', 53),
    ('banlist_no_ban_3', 'No Ban 3（无禁卡版本3）', 57),
    ('banlist_sept_03',  'Sept 03（2003年9月）',    62),
    ('banlist_sept_04',  'Sept 04（2004年9月）',    69),
    ('banlist_march_05', 'March 05（2005年3月）',   80),
    ('banlist_sept_05',  'Sept 05（2005年9月）',    83),
]
TOTAL_ENTRIES = sum(c for _, _, c in BANLISTS)  # 487

LIMIT_GROUP_NAMES = {0: '禁止', 1: '限制', 2: '准限制'}

# 注释列宽：@ 后 name 字段宽度（使 "(密码:" 对齐到最长名字 45 后的下一格）
NAME_COL_WIDTH = 46


def load_card_info(project_root):
    """从 data/card-names.s 读 slot_id → (name_en, passcode)。"""
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


def parse_entries(rom):
    entries = []
    for i in range(TOTAL_ENTRIES):
        off = REGION_START + i * ENTRY_SIZE
        so_code, limit = struct.unpack_from('<HH', rom, off)
        entries.append((so_code, limit))
    return entries


def fmt_entry(so_code, limit, card_info):
    info = card_info.get(so_code)
    if info:
        name, pw = info
        pw_str = pw.zfill(8) if pw else '?'
    else:
        name = f'SO=0x{so_code:04X}'
        pw_str = '?'
    return (f'    banlist_entry  {so_code}, {limit}    '
            f'@ {name:<{NAME_COL_WIDTH}s}(密码: {pw_str})')


def generate_asm(entries, card_info):
    total_bytes = TOTAL_ENTRIES * ENTRY_SIZE
    region_end_exclusive = REGION_START + total_bytes

    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 禁卡表数据')
    lines.append(f'@ ROM偏移: 0x{REGION_START:X} - 0x{region_end_exclusive - 1:X} (共 {len(BANLISTS)} 个版本)')
    lines.append('@')
    lines.append('@ 格式 (每条 4 字节):')
    lines.append('@   字节 0-1: so_code（卡牌内部编号）[小端 16 位]')
    lines.append('@   字节 2-3: limit（限制数量，0禁止/1限制/2准限制）[小端 16 位]')
    lines.append('@')
    lines.append('@ 来源文档: doc/um06-romhacking-resource/modifying-banlists.md')
    lines.append('@ 由 tools/rom-export/export_banlists.py 生成')
    lines.append('@ =============================================================================')
    lines.append('')

    idx = 0
    current_addr = REGION_START
    for label, title, count in BANLISTS:
        table = entries[idx:idx + count]
        idx += count

        # 分组统计
        counts = {0: 0, 1: 0, 2: 0}
        for _, lim in table:
            counts[lim] = counts.get(lim, 0) + 1

        lines.append('@ -----------------------------------------------------------------------------')
        lines.append(f'@ {title}')
        lines.append(f'@ GBA地址: 0x{0x08000000 + current_addr:08X}  ROM偏移: 0x{current_addr:X}')
        lines.append(f'@ {count} 条目（禁止{counts[0]}、限制{counts[1]}、准限制{counts[2]}）')
        lines.append('@ -----------------------------------------------------------------------------')
        lines.append(f'{label}:')

        last_lim = None
        for so_code, lim in table:
            if lim != last_lim:
                group_name = LIMIT_GROUP_NAMES.get(lim, f'limit={lim}')
                lines.append(f'    @ --- {group_name} ---')
                last_lim = lim
            lines.append(fmt_entry(so_code, lim, card_info))

        lines.append('')
        current_addr += count * ENTRY_SIZE

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

    entries = parse_entries(rom)
    print(f'Banlist 条目: {len(entries)}')
    for label, title, count in BANLISTS:
        print(f'  {label:20s}  {count:3d} 条目')

    asm = generate_asm(entries, card_info)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print(f'\n汇编文件: {ASM_OUT}  ({len(asm)} bytes)')
    print('完成。')


if __name__ == '__main__':
    main()
