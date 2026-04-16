#!/usr/bin/env python3
"""
从 roms/2343.gba 导出卡包卡牌列表 (pack card lists) + 卡包信息表 (pack info table)

ROM 布局:
  0x1E5ABFC: Pack 0 卡牌列表 (u32 数组, 每条 = slot_id(u16) + rarity(u8) + pad(u8))
  ...连续排列...
  0x1E5E2E8: 卡包信息表 (51 条 × 16B = 816B)
  0x1E5E618: 结束

卡包信息表每条 16 字节:
  +0  u16  price       开包价格 (DP)
  +2  u16  cards_per   每次开包获得的卡数 (3 或 5)
  +4  u16  total       本包可开出的卡牌总数
  +6  u16  name_id     包名 string ID
  +8  u16  desc_id     包描述 string ID
  +10 u16  padding     0
  +12 u32  card_list   指向卡牌列表的 ROM 指针 (GBA地址, pack 45-50 为 0)

卡牌列表每条 4 字节:
  +0  u16  slot_id     卡槽编号 (与 card-names.s 标签一致)
  +2  u8   rarity      稀有度 (0x00=Common, 0x04=Secret, 0x05=Secret alt,
                        0x08=Ultra, 0x0C=Super, 0x10=Rare)
  +3  u8   padding     0

产出:
  data/pack-card-lists.s    卡牌列表 + 信息表汇编 (入库)

验证参考: Yugipedia (https://yugipedia.com/wiki/) 玩家整理的卡包内容
"""

import os
import re
import struct

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/pack-card-lists.s'

# ROM 布局常量
PACK_INFO_TABLE_OFF = 0x1E5E2E8  # 51 × 16B
PACK_COUNT = 51
PACK_INFO_SIZE = 16
CARD_ENTRY_SIZE = 4

# 稀有度编码
RARITY_NAMES = {
    0x00: 'Common',
    0x04: 'Secret',
    0x05: 'Secret (alt)',
    0x08: 'Ultra',
    0x0C: 'Super',
    0x10: 'Rare',
}

# 卡包名 (来自 data/game-strings-en.s, game_str_en_01046..01096)
PACK_NAMES = [
    "LEGEND OF B.E.W.D.",       #  0
    "METAL RAIDERS",             #  1
    "PHARAOH'S SERVANT",         #  2
    "PHARAONIC GUARDIAN",        #  3
    "SPELL RULER",               #  4
    "LABYRINTH OF NIGHTMARE",    #  5
    "LEGACY OF DARKNESS",        #  6
    "MAGICIAN'S FORCE",          #  7
    "DARK CRISIS",               #  8
    "INVASION OF CHAOS",         #  9
    "ANCIENT SANCTUARY",         # 10
    "SOUL OF THE DUELIST",       # 11
    "RISE OF DESTINY",           # 12
    "FLAMING ETERNITY",          # 13
    "THE LOST MILLENIUM",        # 14
    "CYBERNETIC REVOLUTION",     # 15
    "ELEMENTAL ENERGY",          # 16
    "SHADOW OF INFINITY",        # 17
    "GAME GIFT COLLECTION",      # 18
    "Special Gift Collection",   # 19
    "Fairy Collection",          # 20
    "Dragon Collection",         # 21
    "Warrior Collection A",      # 22
    "Warrior Collection B",      # 23
    "Fiend Collection A",        # 24
    "Fiend Collection B",        # 25
    "Machine Collection A",      # 26
    "Machine Collection B",      # 27
    "Spellcaster Collection A",  # 28
    "Spellcaster Collection B",  # 29
    "Zombie Collection",         # 30
    "Special Monsters A",        # 31
    "Special Monsters B",        # 32
    "Reverse Collection",        # 33
    "LP Recovery Collection",    # 34
    "Special Summon Collection A", # 35
    "Special Summon Collection B", # 36
    "Special Summon Collection C", # 37
    "Equipment Collection",      # 38
    "Continuous Spell/Trap A",   # 39
    "Continuous Spell/Trap B",   # 40
    "Quick/Counter Collection",  # 41
    "Direct Damage Collection",  # 42
    "Direct Attack Collection",  # 43
    "Monster Destroy Collection", # 44
    "All Normal Monsters",       # 45
    "All Effect Monsters",       # 46
    "All Fusion Monsters",       # 47
    "All Traps",                 # 48
    "All Spells",                # 49
    "All at Random",             # 50
]


def load_card_names(project_root):
    """从 data/card-names.s 加载 slot_id → 卡名(EN) 映射。"""
    path = os.path.join(project_root, 'data', 'card-names.s')
    with open(path, 'r', encoding='cp1252') as f:
        text = f.read()
    mapping = {}
    for m in re.finditer(
        r'card_name_([0-9A-F]{4}):\s+@\s+(.+?)(?:\s+\(pw|\s*$)',
        text, re.MULTILINE
    ):
        slot_id = int(m.group(1), 16)
        name = m.group(2).strip()
        mapping[slot_id] = name
    return mapping


def read_pack_info(rom):
    """读取 51 条 pack 信息记录。"""
    packs = []
    for i in range(PACK_COUNT):
        off = PACK_INFO_TABLE_OFF + i * PACK_INFO_SIZE
        price, cards_per, total, name_id, desc_id, pad = struct.unpack_from('<6H', rom, off)
        card_list_ptr = struct.unpack_from('<I', rom, off + 12)[0]
        packs.append({
            'index': i,
            'price': price,
            'cards_per': cards_per,
            'total': total,
            'name_id': name_id,
            'desc_id': desc_id,
            'card_list_ptr': card_list_ptr,
        })
    return packs


def read_card_list(rom, pack):
    """读取一个 pack 的卡牌列表。"""
    ptr = pack['card_list_ptr']
    if ptr < 0x08000000:
        return []
    base = ptr - 0x08000000
    cards = []
    for i in range(pack['total']):
        off = base + i * CARD_ENTRY_SIZE
        slot_id = struct.unpack_from('<H', rom, off)[0]
        rarity = rom[off + 2]
        cards.append((slot_id, rarity))
    return cards


def generate_asm(rom, packs, card_names):
    """生成 data/pack-card-lists.s。"""
    # 计算数据范围
    valid_packs = [p for p in packs if p['card_list_ptr'] >= 0x08000000]
    first_list = min(p['card_list_ptr'] for p in valid_packs) - 0x08000000
    table_end = PACK_INFO_TABLE_OFF + PACK_COUNT * PACK_INFO_SIZE
    total_size = table_end - first_list
    total_cards = sum(p['total'] for p in valid_packs)

    lines = []
    lines.append('@ =============================================================================')
    lines.append('@ 卡包卡牌列表 + 卡包信息表 (Pack Card Lists + Pack Info Table)')
    lines.append(f'@ ROM偏移: 0x{first_list:07X} - 0x{table_end:07X}'
                 f' (共 0x{total_size:X} = {total_size:,} 字节)')
    lines.append('@')
    lines.append(f'@ 卡牌列表: {len(valid_packs)} 个 pack, 共 {total_cards:,} 条目'
                 f' ({total_cards * 4:,} 字节)')
    lines.append(f'@ 信息表: {PACK_COUNT} 条 x 16 字节 = {PACK_COUNT * 16} 字节')
    lines.append('@')
    lines.append('@ 每条卡牌条目 4 字节: slot_id(u16) + rarity(u8) + pad(u8)')
    lines.append('@ 稀有度: 0x00=Common, 0x04=Secret, 0x05=Secret(alt),')
    lines.append('@         0x08=Ultra, 0x0C=Super, 0x10=Rare')
    lines.append('@')
    lines.append('@ 由 tools/rom-export/export_pack_card_lists.py 生成')
    lines.append('@ 验证参考: Yugipedia (https://yugipedia.com/wiki/)')
    lines.append('@ =============================================================================')
    lines.append('')

    # 卡牌列表 (按 ROM 中的顺序 = pack 0, 1, 2, ...)
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('@ 卡牌列表')
    lines.append('@ -----------------------------------------------------------------------------')

    for p in packs:
        i = p['index']
        cards = read_card_list(rom, p)
        if not cards:
            continue  # pack 45-50 无卡牌列表

        name = PACK_NAMES[i]

        # 按稀有度统计
        rarity_counts = {}
        for _, r in cards:
            rarity_counts[r] = rarity_counts.get(r, 0) + 1
        rarity_summary = ', '.join(
            f'{RARITY_NAMES.get(r, f"0x{r:02X}")}={c}'
            for r, c in sorted(rarity_counts.items())
        )

        lines.append('')
        lines.append(f'@ --- [{i:2d}] {name} ({len(cards)} cards: {rarity_summary}) ---')
        lines.append(f'pack_{i:02d}_card_list:')

        for slot_id, rarity in cards:
            card_name = card_names.get(slot_id, f'???')
            rarity_str = RARITY_NAMES.get(rarity, f'0x{rarity:02X}')
            lines.append(f'    pack_card_entry 0x{slot_id:04X}, 0x{rarity:02X}'
                         f'    @ {card_name} ({rarity_str})')

    lines.append('')

    # 卡包信息表
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('@ 卡包信息表: 51 条 x 16 字节')
    lines.append(f'@ GBA地址: 0x{0x08000000 + PACK_INFO_TABLE_OFF:08X}'
                 f'  ROM偏移: 0x{PACK_INFO_TABLE_OFF:07X}')
    lines.append('@ 字段: price(u16), cards_per(u16), total(u16),'
                 ' name_id(u16), desc_id(u16), pad(u16), card_list_ptr(u32)')
    lines.append('@ -----------------------------------------------------------------------------')
    lines.append('pack_info_table:')

    for p in packs:
        i = p['index']
        name = PACK_NAMES[i]
        has_list = p['card_list_ptr'] >= 0x08000000
        if has_list:
            ptr_str = f'pack_{i:02d}_card_list'
        else:
            ptr_str = '0'
        lines.append(f'    @ [{i:2d}] {name}')
        lines.append(f'    .hword {p["price"]}, {p["cards_per"]}, {p["total"]}'
                     f', {p["name_id"]}, {p["desc_id"]}, 0')
        lines.append(f'    .word  {ptr_str}')

    lines.append('')
    return '\n'.join(lines) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    rom = open(ROM_PATH, 'rb').read()
    card_names = load_card_names(project_root)
    print(f'卡名映射: {len(card_names)} 条')

    packs = read_pack_info(rom)
    valid = [p for p in packs if p['card_list_ptr'] >= 0x08000000]
    print(f'卡包: {len(valid)}/{PACK_COUNT} 个有卡牌列表')

    total_cards = sum(p['total'] for p in valid)
    print(f'卡牌条目总数: {total_cards}')

    asm_content = generate_asm(rom, packs, card_names)
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm_content)
    print(f'\n汇编文件: {ASM_OUT}')
    print('完成。')


if __name__ == '__main__':
    main()
