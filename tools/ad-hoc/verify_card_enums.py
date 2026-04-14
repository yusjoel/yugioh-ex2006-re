#!/usr/bin/env python3
"""
验证卡牌属性（attribute）与种族（race）编码表。

从 ROM `0x018169B6` 起的 5170 条 22 字节记录中提取 (slot_id, attribute, race)，
并按卡名表（0x015BB5AC）的槽位顺序对齐 EN 卡名，对每个 (attr, race) 组合输出
记录数 + 若干代表卡名。

用于：
- 验证 include/macros.inc 中 ATTR_* / RACE_* 枚举完整覆盖 ROM 实际取值
- 为 doc/dev/card-data-structure.md §一 补全属性/种族编码表

输出：stdout（表格 + 代表卡）。
"""

import struct
from collections import defaultdict, OrderedDict

ROM_PATH = 'roms/2343.gba'
STATS_OFF = 0x018169B6
STATS_COUNT = 5170
STATS_REC_SIZE = 22

NAMES_OFF = 0x015BB5AC
NAMES_END = 0x015F3A5C  # 0x015F3A5B inclusive

ATTR_NAME = {
    1: 'LIGHT',  2: 'DARK',   3: 'WATER',  4: 'FIRE',
    5: 'EARTH',  6: 'WIND',   7: 'DIVINE', 8: 'SPELL', 9: 'TRAP',
}

RACE_NAME = {
    1:  'DRAGON',         2:  'ZOMBIE',        3:  'FIEND',
    4:  'PYRO',           5:  'SEA_SERPENT',   6:  'ROCK',
    7:  'MACHINE',        8:  'FISH',          9:  'DINOSAUR',
    10: 'INSECT',         11: 'BEAST',         12: 'BEAST_WARRIOR',
    13: 'PLANT',          14: 'AQUA',          15: 'WARRIOR',
    16: 'WINGED_BEAST',   17: 'FAIRY',         18: 'SPELLCASTER',
    19: 'THUNDER',        20: 'REPTILE',       21: 'DIVINE_BEAST',
    22: 'SPELL',          23: 'TRAP',
}


def parse_en_names(rom):
    """扫描卡名表，返回 {slot_id: EN名}；不识别 slot 则跳过。"""
    out = {}
    # 卡名表由 card_names.s 按 stats 表主记录顺序（copy=0）排列 EN/DE/FR/IT/ES/XX。
    # 这里不解析 XX（二进制），只抓 EN：以 stats 表的 slot 顺序读 6 个 null 终止串，
    # 对齐到偶数字节。
    pos = NAMES_OFF
    # 构建 stats 表的 copy=0 槽位顺序
    slots_order = []
    seen = set()
    for i in range(STATS_COUNT):
        rec = rom[STATS_OFF + i * STATS_REC_SIZE:
                  STATS_OFF + (i + 1) * STATS_REC_SIZE]
        slot = struct.unpack_from('<H', rec, 2)[0]
        copy = struct.unpack_from('<H', rec, 4)[0]
        if copy == 0 and slot not in seen and slot != 0:
            seen.add(slot)
            slots_order.append(slot)

    def read_str(p):
        end = rom.find(b'\x00', p)
        s = rom[p:end]
        length = end - p + 1
        if length % 2 == 1:
            length += 1
        return s, p + length

    for slot in slots_order:
        try:
            en, pos = read_str(pos)
            _, pos = read_str(pos)  # DE
            _, pos = read_str(pos)  # FR
            _, pos = read_str(pos)  # IT
            _, pos = read_str(pos)  # ES
            _, pos = read_str(pos)  # XX
        except Exception:
            break
        if pos > NAMES_END:
            break
        try:
            out[slot] = en.decode('cp1252', errors='replace')
        except Exception:
            out[slot] = '<decode-err>'
    return out


def main():
    import os
    script = os.path.dirname(os.path.abspath(__file__))
    proj = os.path.dirname(os.path.dirname(script))
    os.chdir(proj)

    rom = open(ROM_PATH, 'rb').read()
    names = parse_en_names(rom)

    # 收集 (attr, race) → 代表卡
    by_attr = defaultdict(list)
    by_race = defaultdict(list)
    pair_count = defaultdict(int)

    for i in range(STATS_COUNT):
        rec = rom[STATS_OFF + i * STATS_REC_SIZE:
                  STATS_OFF + (i + 1) * STATS_REC_SIZE]
        slot = struct.unpack_from('<H', rec, 2)[0]
        copy = struct.unpack_from('<H', rec, 4)[0]
        race = struct.unpack_from('<H', rec, 14)[0]
        attr = struct.unpack_from('<H', rec, 16)[0]
        if slot == 0 or copy != 0:
            continue
        nm = names.get(slot, f'<slot 0x{slot:04X}>')
        if len(by_attr[attr]) < 3:
            by_attr[attr].append(nm)
        if len(by_race[race]) < 3:
            by_race[race].append(nm)
        pair_count[(attr, race)] += 1

    print('=== 属性（attribute）取值分布 ===')
    for k in sorted(by_attr):
        nm = ATTR_NAME.get(k, '???')
        samples = ', '.join(by_attr[k])
        print(f'  {k:2d} {nm:8s}  样例: {samples}')

    print('\n=== 种族（race）取值分布 ===')
    for k in sorted(by_race):
        nm = RACE_NAME.get(k, '???')
        samples = ', '.join(by_race[k])
        print(f'  {k:2d} {nm:14s} 样例: {samples}')

    print('\n=== (attr, race) 组合计数 ===')
    for k in sorted(pair_count):
        a, r = k
        print(f'  attr={a} race={r:2d}  ({ATTR_NAME.get(a,"?")}, {RACE_NAME.get(r,"?")}) → {pair_count[k]}')

    print('\n=== 未覆盖的枚举值 ===')
    used_attr = set(by_attr.keys())
    used_race = set(by_race.keys())
    unknown_attr = used_attr - set(ATTR_NAME)
    unknown_race = used_race - set(RACE_NAME)
    print(f'  ROM 使用但 macros.inc 未定义: attr={sorted(unknown_attr)}, race={sorted(unknown_race)}')
    print(f'  macros.inc 定义但 ROM 未用:  attr={sorted(set(ATTR_NAME)-used_attr)}, race={sorted(set(RACE_NAME)-used_race)}')


if __name__ == '__main__':
    main()
