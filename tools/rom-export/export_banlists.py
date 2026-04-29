#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禁卡表 (banlists) 导出脚本

从 roms/2343.gba 导出两段：
  1. 0x1E5EF30..0x1E5F6CC: 8 个版本禁卡表 (487 条目 × 4B = 1948 B)
  2. 0x1E5F6CC..0x1E5F71C: banlist master table (10 条 × 8B = 80 B)
     字段 {u32 entries_ptr, u32 count}; banlist_default 被拆 3 段独立查询

每条 banlist_entry 4 字节: [u16 so_code][u16 limit], limit: 0=禁止/1=限制/2=准限制
代码引用: master table 经唯一字面量池 .word 0x09E5F6CC @ FUN_080EF00C

8 个表的边界由 master table 中的 count 字段精确给出（之前是 Data Crystal 推断）。

输出:
  data/banlists.s
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

# Banlist Master Table @ 0x09E5F6CC (10 × 8 B = 80 B)
# 每条: (start_expr, count) — start_expr 用 GAS .word 表达式 (label + 偏移)
# banlist_default 被拆为 3 段（条目 0..2 / 3..16 / 17..43），其余 7 个 banlist 各 1 段
MASTER_TABLE_START = REGION_START + TOTAL_ENTRIES * ENTRY_SIZE  # 0x1E5F6CC
MASTER_TABLE = [
    ('banlist_default',          3),
    ('banlist_default + 0xC',   14),
    ('banlist_default + 0x44',  27),
    ('banlist_no_ban_1',        39),
    ('banlist_no_ban_2',        53),
    ('banlist_no_ban_3',        57),
    ('banlist_sept_03',         62),
    ('banlist_sept_04',         69),
    ('banlist_march_05',        80),
    ('banlist_sept_05',         83),
]
MASTER_ENTRY_SIZE = 8
MASTER_TABLE_BYTES = len(MASTER_TABLE) * MASTER_ENTRY_SIZE  # 80

LIMIT_GROUP_NAMES = {0: '禁止', 1: '限制', 2: '准限制'}

# 注释列宽：@ 后 name 字段宽度（使 "(密码:" 对齐到最长名字 45 后的下一格）
NAME_COL_WIDTH = 46


def load_card_info(project_root):
    """从 doc/um06-deck-modification-tool/data.md 读 slot_id → (name_en, passcode)。"""
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
    file_end_exclusive = MASTER_TABLE_START + MASTER_TABLE_BYTES

    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 禁卡表数据 + Banlist Master Table')
    lines.append(f'@ ROM偏移: 0x{REGION_START:X} - 0x{file_end_exclusive - 1:X}')
    lines.append(f'@   - 0x{REGION_START:X}..0x{MASTER_TABLE_START - 1:X}: 8 个版本禁卡表 ({TOTAL_ENTRIES} 条 × 4B = 0x{total_bytes:X} B)')
    lines.append(f'@   - 0x{MASTER_TABLE_START:X}..0x{file_end_exclusive - 1:X}: banlist_master_table ({len(MASTER_TABLE)} × 8B = 0x{MASTER_TABLE_BYTES:X} B)')
    lines.append('@')
    lines.append('@ 格式 (每条 banlist_entry 4 字节):')
    lines.append('@   字节 0-1: so_code（卡牌内部编号）[小端 16 位]')
    lines.append('@   字节 2-3: limit（限制数量，0禁止/1限制/2准限制）[小端 16 位]')
    lines.append('@')
    lines.append('@ Master Table (每条 8 B): {u32 entries_ptr, u32 count}')
    lines.append('@   banlist_default 被拆为 3 段（3+14+27=44）独立查询，其余 7 个 banlist 各 1 段')
    lines.append('@   代码引用: 字面量池 .word 0x09E5F6CC @ FUN_080EF00C 是唯一入口')
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

    # ---- Banlist Master Table ----
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('@ Banlist Master Table（禁卡表主索引表）')
    lines.append(f'@ GBA地址: 0x{0x08000000 + MASTER_TABLE_START:08X}  ROM偏移: 0x{MASTER_TABLE_START:X}')
    lines.append(f'@ {len(MASTER_TABLE)} 条 × 8 字节 = 0x{MASTER_TABLE_BYTES:X} ({MASTER_TABLE_BYTES}) 字节')
    lines.append('@ 字段: u32 entries_ptr (指向某 banlist 内某段); u32 count (该段条目数)')
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('banlist_master_table:')
    for expr, count in MASTER_TABLE:
        lines.append(f'    .word {expr:<26s}, {count}')
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
