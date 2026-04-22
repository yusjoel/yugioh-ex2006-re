#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡牌数据导出脚本

从 roms/2343.gba 中读取以下表，导出为可读汇编文件：

  1. 卡名字符串池 + 指针表（合并到 data/card-names.s）
     字符串池: ROM 0x015BB594..0x015F3A5B  (230,600 B)
              每 master cid 6 个 null 终止字符串，顺序 XX/EN/DE/FR/IT/ES
              XX = JP 自定义编码（每字符 2 字节）
              2 字节对齐：(strlen + 1) 为奇数时补一个 \\0
              cid=0 是占位记录（6 × 空 = 12 B）；alt-art 卡共享 master 标签
     指针表: ROM 0x015F3A5C..0x015FFF0B  (50,352 B = 2098 × 6 × u32)
             Lookup (Data Crystal 0x080EE968):
               name_addr = 0x015BB594 + ptr[card_id*6 + lang_id]
             通过宏 name_offsets <suffix> 展开（与 card-descriptions 的
             desc_offsets 同构）。末卡 cid=2097 = Fluffy Token。

  2. 卡牌属性数据表（ROM 0x018169B6 – 0x01832602）
     每条 22 字节（11 × uint16 LE），共 5170 条。
     字段：zero_0 / slot_id / copy_idx / one /
           atk / def / level / attribute / race / unknown / zero_1

输出文件：
  data/card-names.s     卡名字符串池 + 指针表（合并版）
  data/card-stats.s     卡牌属性数据表

卡名来源：doc/um06-deck-modification-tool/data.md（2036 张，含槽位 ID 与密码）
"""

import os
import re
import struct
import sys

ROM_PATH    = 'roms/2343.gba'
DATA_MD     = 'doc/um06-deck-modification-tool/data.md'
OUT_DIR     = 'data'

# 卡名字符串表起始偏移（真起点 = card_names_pool）
# 参考 refs/datacrystal-um2006/rom-map.md
NAMES_START = 0x015BB594

# 卡牌属性数据表
STATS_START = 0x018169B8         # 首条 zero0 字段与 card-descriptions Section C 最末 u32 字节重叠
STATS_END   = 0x01832601         # 闭区间最后一字节
RECORD_SIZE = 22                 # 字节/条 (首条除外：首条无 zero0 字段, 仅 20 B)
# 首条 20 B + 后续 5169 × 22 B = 113,738 B = STATS_END - STATS_START + 1
STATS_COUNT = 5170

# 每张卡的字符串语言数（XX/EN/DE/FR/IT/ES）
# 顺序通过对比 lang=0 字节模式 (0xF0+ 高字节为主) vs lang=1..5 (Latin 文字) 验证
LANGS_PER_CARD = 6
LANG_NAMES = ['XX', 'EN', 'DE', 'FR', 'IT', 'ES']


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

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
# 导出：卡名字符串表 + 指针表（合并文件）
# ---------------------------------------------------------------------------

# 卡名指针表（紧跟字符串池之后）
NAME_PTR_START = 0x015F3A5C          # = 字符串池结束 = 指针表起点
NAME_PTR_END   = 0x015FFF0C          # 指针表结束 = card-descriptions 起点
N_CARDS_TOTAL  = 2098                # cid=0..2097


def _escape_string_oneline(data: bytes, lang: str) -> str:
    """把字节序列编码为 .ascii 单行字面量内容。
    XX 非打印 ASCII 用 \\NNN 八进制（与 card-descriptions.s 风格一致）；
    其他 lang 优先 CP1252 字面，未定义字节用八进制。
    """
    pieces = []
    for b in data:
        if   b == 0x22: pieces.append('\\"')
        elif b == 0x5C: pieces.append('\\\\')
        elif b == 0x00: pieces.append('\\0')
        elif lang == 'xx':
            if 0x20 <= b < 0x7F:
                pieces.append(chr(b))
            else:
                pieces.append(f'\\{b:03o}')
        else:
            if   0x20 <= b < 0x7F: pieces.append(chr(b))
            elif b == 0x0A: pieces.append('\\n')
            elif b == 0x0D: pieces.append('\\r')
            elif b == 0x09: pieces.append('\\t')
            elif 0xA0 <= b <= 0xFF: pieces.append(chr(b))
            elif 0x80 <= b <= 0x9F:
                try:
                    pieces.append(bytes([b]).decode('cp1252'))
                except (UnicodeDecodeError, ValueError):
                    pieces.append(f'\\{b:03o}')
            else:
                pieces.append(f'\\{b:03o}')
    return ''.join(pieces)


def export_card_names(rom: bytes, out_dir: str) -> int:
    """生成合并版 data/card-names.s（字符串池 + 指针表）。

    结构参照 data/card-descriptions.s，所有 label 均以 4 位十进制 cid 为后缀：
      1. card_names_table        字符串池（master cid × 6 langs，每 lang 独立子标签）
         card_name_<cid>:          @ <EN name>
         card_name_<cid>_<lang>:
             .ascii "..."
      2. card_name_pointer_table 2098 × 6 × u32 偏移（通过 name_offsets 宏展开）
         name_offsets <cid>    @ <EN name>[ (alt-art)]

    返回指针表结束偏移（= card-descriptions 起点）。
    """

    pool_start = NAMES_START
    pool_end   = NAME_PTR_START
    pool_size  = pool_end - pool_start
    ptr_start  = NAME_PTR_START
    ptr_end    = NAME_PTR_END
    ptr_size   = ptr_end - ptr_start

    # 1. 读取指针表：12,588 × u32 = 2098 cards × 6 langs
    ptrs = [struct.unpack_from('<I', rom, ptr_start + i * 4)[0]
            for i in range(N_CARDS_TOTAL * LANGS_PER_CARD)]

    # 2. 以 6-tuple 首次出现判定 master_cid（alt-art 共享 master）
    group_to_master: dict[tuple, int] = {}
    master_of: list[int] = [0] * N_CARDS_TOTAL
    for cid in range(N_CARDS_TOTAL):
        grp = tuple(ptrs[cid * 6:(cid + 1) * 6])
        master_of[cid] = group_to_master.setdefault(grp, cid)

    masters_sorted = sorted(set(master_of))
    n_masters = len(masters_sorted)

    # 3. 直接从 pool 抽取每个 master 的 EN 名字串（去尾 null）
    en_name_of: dict[int, str] = {}
    for idx, mc in enumerate(masters_sorted):
        en_off  = ptrs[mc * 6 + 1]              # EN lang offset
        next_off = ptrs[mc * 6 + 2]             # DE offset 为 EN 段尾
        en_bytes = bytes(rom[pool_start + en_off:pool_start + next_off])
        en_name  = en_bytes.rstrip(b'\0').decode('cp1252', errors='replace')
        en_name_of[mc] = en_name if en_name else '(placeholder)' if mc == 0 else '(unknown)'

    # 4. 生成输出
    out: list[str] = []
    out.append('@ =============================================================================')
    out.append('@ Card Names (merged: name pool + pointer table)')
    out.append(f'@ ROM 0x{pool_start:07X} - 0x{ptr_end:07X}  ({ptr_end - pool_start:,} B)')
    out.append('@')
    out.append(f'@  1. card_names_table         0x{pool_start:07X} - 0x{pool_end:07X}'
               f'  ({pool_size:,} B)')
    out.append(f'@     {n_masters} master entries × 6 langs (XX/EN/DE/FR/IT/ES),'
               f' null-terminated, 2B-aligned')
    out.append(f'@     alt-art cards share master label')
    out.append(f'@  2. card_name_pointer_table  0x{ptr_start:07X} - 0x{ptr_end:07X}'
               f'  ({ptr_size:,} B = {N_CARDS_TOTAL}×6 u32)')
    out.append('@     Lookup (Data Crystal 0x080EE968):')
    out.append('@       name_addr = card_names_table + ptr[card_id*6 + lang_id]')
    out.append('@     lang_id: 0=XX 1=EN 2=DE 3=FR 4=IT 5=ES')
    out.append('@')
    out.append('@ File encoding: CP1252; XX bytes octal-escaped (\\NNN) for readability')
    out.append('@ Labels: card_name_<cid>[_<lang>]; <cid> = master card id, 4-digit decimal')
    out.append('@ Generated by tools/rom-export/export_card_data.py')
    out.append('@ =============================================================================')
    out.append('')

    # 宏：6 lang 偏移（相对 card_names_table）
    out.append('@ Macro: 6 lang offsets for cid (label - card_names_table)')
    out.append('.macro name_offsets cid')
    for lang in LANG_NAMES:
        out.append(f'\t.word card_name_\\cid\\()_{lang.lower()} - card_names_table')
    out.append('.endm')
    out.append('')

    # ---------- 1. 字符串池 ----------
    out.append('@ -----------------------------------------------------------------------------')
    out.append(f'@ 1. Name Pool ({n_masters} masters × 6 langs, null-terminated, 2B-aligned)')
    out.append(f'@    ROM 0x{pool_start:07X} - 0x{pool_end:07X}  ({pool_size:,} B)')
    out.append('@ -----------------------------------------------------------------------------')
    out.append('card_names_table:')

    for idx, mc in enumerate(masters_sorted):
        suffix  = f'{mc:04d}'
        out.append('')
        out.append(f'card_name_{suffix}:  @ {en_name_of[mc]}')
        for lang_idx, lang in enumerate(LANG_NAMES):
            off = ptrs[mc * 6 + lang_idx]
            # 段尾：同 master 下一 lang 的起点；最后一 lang 取下一 master XX 或 pool_size
            if lang_idx < 5:
                next_off = ptrs[mc * 6 + lang_idx + 1]
            elif idx + 1 < n_masters:
                next_mc  = masters_sorted[idx + 1]
                next_off = ptrs[next_mc * 6 + 0]
            else:
                next_off = pool_size
            chunk = bytes(rom[pool_start + off:pool_start + next_off])
            out.append(f'card_name_{suffix}_{lang.lower()}:')
            out.append(f'\t.ascii "{_escape_string_oneline(chunk, lang.lower())}"')

    out.append('')

    # ---------- 2. 指针表 ----------
    out.append('@ -----------------------------------------------------------------------------')
    out.append(f'@ 2. Pointer Table ({N_CARDS_TOTAL} cards × 6 langs × u32)')
    out.append(f'@    ROM 0x{ptr_start:07X} - 0x{ptr_end:07X}  ({ptr_size:,} B)')
    out.append('@ -----------------------------------------------------------------------------')
    out.append('card_name_pointer_table:')
    out.append('')

    for cid in range(N_CARDS_TOTAL):
        mc = master_of[cid]
        suffix = f'{mc:04d}'
        name = en_name_of[mc]
        alt = '' if mc == cid else ' (alt-art)'
        out.append(f'\tname_offsets {suffix}    @ {name}{alt}')

    out.append('')

    content = '\n'.join(out) + '\n'
    out_path = os.path.join(out_dir, 'card-names.s')
    with open(out_path, 'w', encoding='cp1252') as f:
        f.write(content)

    print(f'[NAMES] {out_path}')
    print(f'  Name pool:      ROM 0x{pool_start:08X} ~ 0x{pool_end-1:08X}'
          f'  ({pool_size:,} B, {n_masters} masters)')
    print(f'  Pointer table:  ROM 0x{ptr_start:08X} ~ 0x{ptr_end-1:08X}'
          f'  ({ptr_size:,} B, {N_CARDS_TOTAL} cards)')
    print(f'  Output:         {len(content):,} chars, {content.count(chr(10)):,} lines')
    return ptr_end   # 开区间结束


# ---------------------------------------------------------------------------
# 常量映射表（用于生成带符号名称的注释）
# ---------------------------------------------------------------------------

RACE_NAMES: dict[int, tuple[str, str]] = {
    1:  ('RACE_DRAGON',        '龙'),
    2:  ('RACE_ZOMBIE',        '不死'),
    3:  ('RACE_FIEND',         '恶魔'),
    4:  ('RACE_PYRO',          '炎'),
    5:  ('RACE_SEA_SERPENT',   '海龙'),
    6:  ('RACE_ROCK',          '岩石'),
    7:  ('RACE_MACHINE',       '机械'),
    8:  ('RACE_FISH',          '鱼'),
    9:  ('RACE_DINOSAUR',      '恐龙'),
    10: ('RACE_INSECT',        '昆虫'),
    11: ('RACE_BEAST',         '兽'),
    12: ('RACE_BEAST_WARRIOR', '兽战士'),
    13: ('RACE_PLANT',         '植物'),
    14: ('RACE_AQUA',          '水'),
    15: ('RACE_WARRIOR',       '战士'),
    16: ('RACE_WINGED_BEAST',  '鸟兽'),
    17: ('RACE_FAIRY',         '天使'),
    18: ('RACE_SPELLCASTER',   '魔法使'),
    19: ('RACE_THUNDER',       '雷'),
    20: ('RACE_REPTILE',       '爬虫'),
    21: ('RACE_DIVINE_BEAST',  '幻神兽'),
    22: ('RACE_SPELL',         '魔法卡'),
    23: ('RACE_TRAP',          '陷阱卡'),
}

ATTR_NAMES: dict[int, tuple[str, str]] = {
    1: ('ATTR_LIGHT',  '光'),
    2: ('ATTR_DARK',   '闇'),
    3: ('ATTR_WATER',  '水'),
    4: ('ATTR_FIRE',   '炎'),
    5: ('ATTR_EARTH',  '地'),
    6: ('ATTR_WIND',   '风'),
    7: ('ATTR_DIVINE', '神'),
    8: ('ATTR_SPELL',  '魔法'),
    9: ('ATTR_TRAP',   '陷阱'),
}

SUBTYPE_NAMES: dict[int, tuple[str, str]] = {
    0:  ('SUBTYPE_NORMAL',        '通常'),
    1:  ('SUBTYPE_EFFECT',        '效果'),
    2:  ('SUBTYPE_FUSION',        '融合'),
    3:  ('SUBTYPE_FUSION_EFFECT', '融合/效果'),
    4:  ('SUBTYPE_RITUAL',        '仪式'),
    5:  ('SUBTYPE_RITUAL_EFFECT', '仪式/效果'),
    6:  ('SUBTYPE_TOON',          '动画版'),
    7:  ('SUBTYPE_SPIRIT',        '灵魂'),
    8:  ('SUBTYPE_UNION',         '同盟'),
    9:  ('SUBTYPE_TOKEN',         '代币'),
    13: ('SUBTYPE_SPELL_CARD',    '魔法卡'),
    14: ('SUBTYPE_TRAP_CARD',     '陷阱卡'),
}

SPSUB_NAMES: dict[int, tuple[str, str]] = {
    0: ('SPSUB_NORMAL',     '通常'),
    1: ('SPSUB_COUNTER',    '反击陷阱'),
    2: ('SPSUB_FIELD',      '场地魔法'),
    3: ('SPSUB_EQUIP',      '装备魔法'),
    4: ('SPSUB_CONTINUOUS', '永续'),
    5: ('SPSUB_QUICK_PLAY', '速攻魔法'),
    6: ('SPSUB_RITUAL',     '仪式魔法'),
}


def _sym(table: dict, val: int, default_fmt: str = '0x{:04X}') -> tuple[str, str]:
    """从映射表返回 (符号名, 中文注释)；未命中时返回十六进制字面量。"""
    if val in table:
        return table[val]
    return default_fmt.format(val), '?'


# ---------------------------------------------------------------------------
# 导出：卡牌属性数据表
# ---------------------------------------------------------------------------

def export_card_stats(rom: bytes, slot_info: list, out_dir: str):
    """生成 data/card-stats.s（每字段独占一行 .hword，使用 macros.inc 中的命名常量）。"""

    # slot_id → (en_name, password) 查找表
    slot_lookup: dict[int, tuple[str, int]] = {
        slot: (name, pwd) for slot, name, pwd in slot_info
    }

    header = (
        '@ data/card-stats.s\n'
        '@ 卡牌属性数据表\n'
        f'@ ROM range: 0x{STATS_START:08X} ~ 0x{STATS_END:08X}\n'
        '@ Generated by tools/rom-export/export_card_data.py\n'
        '@\n'
        f'@ 每条 {RECORD_SIZE} 字节（{RECORD_SIZE//2} × uint16 LE），共 {STATS_COUNT} 条\n'
        '@\n'
        '@ 字段说明（详见 include/macros.inc）：\n'
        '@   zero0   (+00) 保留，恒 0（首条记录 = 0x0020）\n'
        '@   slot_id (+02) 卡槽编号\n'
        '@   copy    (+04) 異画索引（0=主图，1/2/3=异画）\n'
        '@   flags   (+06) 标志（通常 1；0=哑元；3=含义待定）\n'
        '@   atk     (+08) 攻击力\n'
        '@   def     (+0A) 守备力\n'
        '@   level   (+0C) 星数\n'
        '@   race    (+0E) 种族（RACE_xxx）\n'
        '@   attr    (+10) 属性（ATTR_xxx）\n'
        '@   subtype (+12) 卡种类（SUBTYPE_xxx）\n'
        '@   spsub   (+14) 魔法/陷阱细分（SPSUB_xxx，怪兽恒 0）\n'
        '\n'
        '@ 使用 .include "include/macros.inc" 获取符号定义\n'
        '\n'
        'card_stats_table:\n'
    )

    lines = [header]

    # 计算每条的 ROM 起点：首条 (i=0) 无 zero0 字段 (20 B)，其余 22 B
    def entry_offset(i):
        if i == 0:
            return STATS_START  # 指向 slot_id 字段 (首条无 zero0)
        return STATS_START + 20 + (i - 1) * RECORD_SIZE  # 首条 20 B + 后续

    for i in range(STATS_COUNT):
        off = entry_offset(i)
        if i == 0:
            # 首条: 无 zero0 字段, 只读 10 hwords (slot_id..spsub)
            zero0 = 0x0020  # 字节重叠值 (由 Section C 最末 u32 的高 2 B 提供), 仅用于注释
            (slot_id, copy_idx, flags,
             atk, def_, level, race, attr, subtype, spsub) = struct.unpack_from('<10H', rom, off)
        else:
            (zero0, slot_id, copy_idx, flags,
             atk, def_, level, race, attr, subtype, spsub) = struct.unpack_from('<11H', rom, off)

        label = f'card_{i:04d}'

        # ── 全零 / 哑元记录（slot_id == 0） ──────────────────────────────────
        if slot_id == 0:
            if i == 0:
                # 首条特殊：zero0 字段与 card-descriptions Section C 最末 u32 字节重叠
                comment = ('@ 哑元记录（slot_id=0）；zero0 字段 (=0x0020) 字节归属'
                           ' card-descriptions Section C 最末 u32')
                lines.append(
                    f'\n{label}:\t{comment}\n'
                    f'\t.hword 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\t'
                    f'@ slot_id, copy, flags, atk, def, level, race, attr, subtype, spsub (20 B)\n'
                )
                continue
            zero0_s = f'0x{zero0:04X}' if zero0 else ''
            comment = f'@ 哑元记录（slot_id=0）'
            if zero0_s:
                lines.append(f'\n{label}:\t{comment}\n\tcard_stat_zero {zero0_s}\n')
            else:
                lines.append(f'\n{label}:\t{comment}\n\tcard_stat_zero\n')
            continue

        # ── 正常记录 ──────────────────────────────────────────────────────────
        race_sym,    race_cn    = _sym(RACE_NAMES,    race)
        attr_sym,    attr_cn    = _sym(ATTR_NAMES,    attr)
        subtype_sym, subtype_cn = _sym(SUBTYPE_NAMES, subtype)
        spsub_sym,   spsub_cn  = _sym(SPSUB_NAMES,   spsub)

        # 构造标题注释
        if slot_id in slot_lookup:
            en_name, pwd = slot_lookup[slot_id]
            title = f'@ {en_name}  slot=0x{slot_id:04X}  pw={pwd:08d}'
        else:
            title = f'@ slot=0x{slot_id:04X}  copy={copy_idx}'
            if copy_idx > 0:
                title += f'  (異画 {copy_idx})'

        # 魔法/陷阱 atk/def 显示为 0（不用 0xFFFF）
        atk_s = str(atk)
        def_s = str(def_)

        # 生成每字段独占一行的 .hword 输出
        entry = (
            f'\n{label}:  {title}\n'
            f'\t.hword  0x{zero0:04X}          @ zero0\n'
            f'\t.hword  0x{slot_id:04X}          @ slot_id\n'
            f'\t.hword  {copy_idx}               @ copy (異画: 0=主图)\n'
            f'\t.hword  {flags}               @ flags\n'
            f'\t.hword  {atk_s:<5}             @ atk (攻击力)\n'
            f'\t.hword  {def_s:<5}             @ def (守备力)\n'
            f'\t.hword  {level}               @ level (星数)\n'
            f'\t.hword  {race_sym:<20} @ race: {race_cn}\n'
            f'\t.hword  {attr_sym:<20} @ attr: {attr_cn}\n'
            f'\t.hword  {subtype_sym:<20} @ subtype: {subtype_cn}\n'
            f'\t.hword  {spsub_sym:<20} @ spsub: {spsub_cn}\n'
        )
        lines.append(entry)

    out_path = os.path.join(out_dir, 'card-stats.s')
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)

    print(f'[STATS] {out_path}  记录数: {STATS_COUNT}  '
          f'ROM: 0x{STATS_START:08X} ~ 0x{STATS_END:08X}')


# ---------------------------------------------------------------------------
# 主函数
# ---------------------------------------------------------------------------

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

    print(f'解析 {DATA_MD} ...')
    slot_info = load_data_md(DATA_MD)
    print(f'  从 data.md 读取 {len(slot_info)} 张卡的槽位信息')

    print(f'导出合并卡名字符串表 + 指针表 → data/card-names.s ...')
    names_table_end = export_card_names(rom, OUT_DIR)

    print(f'导出卡牌属性数据表 → data/card-stats.s ...')
    export_card_stats(rom, slot_info, OUT_DIR)

    print()
    print('完成。下一步：更新 asm/rom.s 并运行 build.bat 验证 byte-identical。')
    print(f'  card-names.s 覆盖：ROM 0x{NAMES_START:08X} ~ 0x{names_table_end-1:08X}')
    print(f'  card-stats.s 覆盖：ROM 0x{STATS_START:08X} ~ 0x{STATS_END:08X}')


if __name__ == '__main__':
    main()
