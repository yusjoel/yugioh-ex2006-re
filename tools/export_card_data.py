#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡牌数据导出脚本

从 roms/2343.gba 中读取以下两张表，导出为可读汇编文件：

  1. 卡名字符串表（ROM 0x015BB5AC）
     每张卡 6 个 null 终止字符串，顺序：EN / DE / FR / IT / ES / XX
     XX 语言使用自定义字节编码（0xF0-0xFF 等），用途待考证。
     2 字节对齐：(strlen + 1) 为奇数时补一个 \\0。

  2. 卡牌属性数据表（ROM 0x018169B6 – 0x01832602）
     每条 22 字节（11 × uint16 LE），共 5170 条。
     字段：zero_0 / slot_id / copy_idx / one /
           atk / def / level / attribute / race / unknown / zero_1

输出文件：
  data/card-names.s     卡名字符串表
  data/card-stats.s     卡牌属性数据表

卡名来源：doc/um06-deck-modification-tool/data.md（2037 张，含槽位 ID 与密码）
"""

import os
import re
import struct
import sys

ROM_PATH    = 'roms/2343.gba'
DATA_MD     = 'doc/um06-deck-modification-tool/data.md'
OUT_DIR     = 'data'

# 卡名字符串表起始偏移（含义见 doc/dev/card-data-structure.md）
NAMES_START = 0x015BB5AC

# 卡牌属性数据表
STATS_START = 0x018169B6
STATS_END   = 0x01832601         # 闭区间最后一字节（5170 × 22 = 113740 字节）
RECORD_SIZE = 22                 # 字节/条
STATS_COUNT = (STATS_END - STATS_START + 1) // RECORD_SIZE  # 5170

# 每张卡的字符串语言数（EN/DE/FR/IT/ES/XX）
LANGS_PER_CARD = 6
LANG_NAMES = ['EN', 'DE', 'FR', 'IT', 'ES', 'XX']


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def asm_escape(raw: bytes) -> str:
    """将字节序列转换为 GAS .ascii 字面量内容（CP1252 源文件）。"""
    parts = []
    for b in raw:
        if   b == 0x22: parts.append('\\"')
        elif b == 0x5C: parts.append('\\\\')
        elif b == 0x0A: parts.append('\\n')
        elif b == 0x0D: parts.append('\\r')
        elif b == 0x09: parts.append('\\t')
        elif b == 0x00: parts.append('\\0')
        elif 0x20 <= b < 0x7F:  parts.append(chr(b))
        elif 0x80 <= b <= 0x9F:
            try:    parts.append(bytes([b]).decode('cp1252'))
            except (UnicodeDecodeError, ValueError):
                    parts.append(f'\\x{b:02x}')
        elif 0xA0 <= b <= 0xFF: parts.append(chr(b))
        else:                   parts.append(f'\\x{b:02x}')
    return ''.join(parts)


def read_null_str(rom: bytes, pos: int, limit: int) -> tuple[bytes, int]:
    """读取一个 null 终止字符串，返回 (字节串, 下一个字符串的起始位置)。
    下一个起始位置已对齐到 2 字节边界（含结尾 null 和可能的填充 null）。
    """
    j = pos
    while j < limit and rom[j] != 0:
        j += 1
    s = rom[pos:j]
    end = j + 1           # 跳过 null
    if end % 2 == 1:      # 对齐到偶数地址
        end += 1
    return s, end


def load_data_md(path: str) -> list[tuple[int, str, int]]:
    """解析 data.md，返回按出现顺序排列的 [(slot_id, en_name, password)] 列表。"""
    result = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            # 匹配数据行：| 密码 | 卡名 | ... | 4位Hex槽位 | ...
            # 注意：Starter/Opponent 列前后有空格
            m = re.match(
                r'\|\s*(\d{7,9})\s*\|([^|]+)\|[^|]*\|\s*([0-9A-Fa-f]{4})\s*\|',
                line
            )
            if m:
                pwd  = int(m.group(1))
                name = m.group(2).strip()
                slot = int(m.group(3), 16)
                result.append((slot, name, pwd))
    return result


# ---------------------------------------------------------------------------
# 卡名字符串表扫描
# ---------------------------------------------------------------------------

def scan_card_names(rom: bytes) -> tuple[list, int]:
    """扫描卡名字符串表，返回 (cards, end_offset)。
    cards = [(card_rom_off, [lang0_bytes, lang1_bytes, ...]), ...]
    end_offset = 表结束后第一个字节的偏移（下一个数据结构起始）。

    停止条件：EN 字符串（第0个）为空，或含控制字符（< 0x20）。
    """
    p = NAMES_START
    limit = STATS_START   # 不跨越属性表
    cards = []

    while p < limit:
        card_start = p
        strs = []
        ok = True
        for _ in range(LANGS_PER_CARD):
            s, p = read_null_str(rom, p, limit)
            strs.append(s)
            if p > limit:
                ok = False
                break
        if not ok:
            break
        en_str = strs[0]
        # EN 为空 → 已到表末尾的哑元或其他数据
        if len(en_str) == 0:
            break
        # EN 含控制字符 → 已离开字符串表
        if any(b < 0x20 for b in en_str):
            break
        cards.append((card_start, strs))

    # end_offset = 当前 p（上一次成功扫描后的位置），即下一个数据结构的起始
    # 回退到最后一张有效卡结束后的对齐位置
    if cards:
        last_off, last_strs = cards[-1]
        p2 = last_off
        for s in last_strs:
            a = len(s) + 1
            if a % 2 == 1:
                a += 1
            p2 += a
        return cards, p2
    return cards, p


# ---------------------------------------------------------------------------
# 导出：卡名字符串表
# ---------------------------------------------------------------------------

def export_card_names(rom: bytes, cards: list, slot_info: list, out_dir: str) -> int:
    """生成 data/card-names.s。返回表结束偏移（最后一个字节之后）。"""

    # 建立 index → (slot_id, en_name, password) 映射
    slot_map = {}
    for i, (slot, name, pwd) in enumerate(slot_info):
        slot_map[i] = (slot, name, pwd)

    lines = []

    # 计算精确结束偏移（最后一张卡的最后一字节+1）
    last_card_off, last_strs = cards[-1]
    p = last_card_off
    for s in last_strs:
        aligned_len = len(s) + 1
        if aligned_len % 2 == 1:
            aligned_len += 1
        p += aligned_len
    end_off = p - 1  # 闭区间

    header = (
        f'@ data/card-names.s\n'
        f'@ ROM range: 0x{NAMES_START:08X} ~ 0x{end_off:08X}\n'
        f'@ Generated by tools/export_card_data.py\n'
        f'@\n'
        f'@ {LANGS_PER_CARD} strings per card: {" / ".join(LANG_NAMES)}\n'
        f'@ XX: custom byte encoding (0xF0-0xFF range)\n'
        f'@ File encoding: CP1252\n'
        f'@ 2-byte alignment: (strlen+1) odd -> pad with one extra \\0\n'
        f'@\n'
        f'@ Labels: card_name_XXXX (XXXX = slot_id hex, uppercase)\n'
        f'@   Tokens/unknowns use card_name_idx_NNNN\n'
        f'\n'
        f'card_names_table:\n'
    )

    for i, (card_off, strs) in enumerate(cards):
        # 槽位信息
        if i < len(slot_info):
            slot_id, en_name, pwd = slot_info[i]
            label = f'card_name_{slot_id:04X}'
            comment = f'{en_name}  (pw {pwd:08d})'
        else:
            label = f'card_name_idx_{i:04d}'
            comment = f'(index {i}, no data.md entry)'

        lines.append(f'\n{label}:  @ {comment}\n')

        for lang_idx, s in enumerate(strs):
            lang = LANG_NAMES[lang_idx]
            # 计算对齐后的 null 数量
            null_count = 1
            if (len(s) + 1) % 2 == 1:
                null_count = 2
            content = asm_escape(s) + '\\0' * null_count
            lines.append(f'\t.ascii "{content}"  @ {lang}\n')

    out_path = os.path.join(out_dir, 'card-names.s')
    with open(out_path, 'w', encoding='cp1252') as f:
        f.write(header)
        f.writelines(lines)

    print(f'[NAMES] {out_path}  卡数: {len(cards)}  '
          f'ROM: 0x{NAMES_START:08X} ~ 0x{end_off:08X}')
    return end_off + 1   # 开区间结束


# ---------------------------------------------------------------------------
# 导出：卡牌属性数据表
# ---------------------------------------------------------------------------

def export_card_stats(rom: bytes, slot_info: list, out_dir: str):
    """生成 data/card-stats.s。"""

    # slot_id → (en_name, password) 查找表（用于注释）
    slot_lookup: dict[int, tuple[str, int]] = {}
    for slot, name, pwd in slot_info:
        slot_lookup[slot] = (name, pwd)

    lines = []
    header = (
        f'@ data/card-stats.s\n'
        f'@ 卡牌属性数据表\n'
        f'@ ROM range: 0x{STATS_START:08X} ~ 0x{STATS_END:08X}\n'
        f'@ Generated by tools/export_card_data.py\n'
        f'@\n'
        f'@ 每条 {RECORD_SIZE} 字节（{RECORD_SIZE//2} × uint16 LE），共 {STATS_COUNT} 条\n'
        f'@ 字段（按偏移）：\n'
        f'@   +00  zero_0     恒 0\n'
        f'@   +02  slot_id    卡槽编号\n'
        f'@   +04  copy_idx   副本索引（0=主记录，1/2/3=副本）\n'
        f'@   +06  one        恒 1\n'
        f'@   +08  atk        攻击力（Spell/Trap 为 0xFFFF）\n'
        f'@   +10  def        守备力（Spell/Trap 为 0xFFFF）\n'
        f'@   +12  level      星数\n'
        f'@   +14  attribute  属性代码\n'
        f'@   +16  race       种族代码\n'
        f'@   +18  unknown    大部分为 0\n'
        f'@   +20  zero_1     恒 0\n'
        f'\n'
        f'card_stats_table:\n'
    )

    for i in range(STATS_COUNT):
        off = STATS_START + i * RECORD_SIZE
        fields = struct.unpack_from('<11H', rom, off)
        (zero_0, slot_id, copy_idx, one,
         atk, def_, level, attr, race, unknown, zero_1) = fields

        # 注释
        if copy_idx == 0 and slot_id in slot_lookup:
            en_name, pwd = slot_lookup[slot_id]
            comment = f'slot=0x{slot_id:04X} copy={copy_idx}  {en_name} (密码 {pwd:08d})'
        elif copy_idx == 0:
            comment = f'slot=0x{slot_id:04X} copy={copy_idx}'
        else:
            comment = f'slot=0x{slot_id:04X} copy={copy_idx}'

        # ATK/DEF 用 0xFFFF 表示 Spell/Trap
        atk_s  = f'0xFFFF' if atk  == 0xFFFF else str(atk)
        def_s  = f'0xFFFF' if def_ == 0xFFFF else str(def_)

        line = (
            f'\t.hword 0x{zero_0:04X}, 0x{slot_id:04X}, 0x{copy_idx:04X}, 0x{one:04X}, '
            f'{atk_s}, {def_s}, {level}, '
            f'0x{attr:04X}, 0x{race:04X}, 0x{unknown:04X}, 0x{zero_1:04X}'
            f'  @ {comment}\n'
        )
        lines.append(line)

    out_path = os.path.join(out_dir, 'card-stats.s')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.writelines(lines)

    print(f'[STATS] {out_path}  记录数: {STATS_COUNT}  '
          f'ROM: 0x{STATS_START:08X} ~ 0x{STATS_END:08X}')


# ---------------------------------------------------------------------------
# 主函数
# ---------------------------------------------------------------------------

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print(f'错误：ROM 文件 {ROM_PATH} 不存在', file=sys.stderr)
        sys.exit(1)

    print(f'读取 {ROM_PATH} ...')
    with open(ROM_PATH, 'rb') as f:
        rom = f.read()

    print(f'解析 {DATA_MD} ...')
    slot_info = load_data_md(DATA_MD)
    print(f'  从 data.md 读取 {len(slot_info)} 张卡的槽位信息')

    print(f'扫描卡名字符串表（ROM 0x{NAMES_START:08X}）...')
    cards, names_table_end = scan_card_names(rom)
    print(f'  找到 {len(cards)} 张卡，'
          f'表结束于 ROM 0x{names_table_end - 1:08X}（含）')

    print(f'导出卡名字符串表 → data/card-names.s ...')
    export_card_names(rom, cards, slot_info, OUT_DIR)

    print(f'导出卡牌属性数据表 → data/card-stats.s ...')
    export_card_stats(rom, slot_info, OUT_DIR)

    print()
    print('完成。下一步：更新 asm/rom.s 并运行 build.bat 验证 byte-identical。')
    print(f'  card-names.s 覆盖：ROM 0x{NAMES_START:08X} ~ 0x{names_table_end-1:08X}')
    print(f'  card-stats.s 覆盖：ROM 0x{STATS_START:08X} ~ 0x{STATS_END:08X}')


if __name__ == '__main__':
    main()
