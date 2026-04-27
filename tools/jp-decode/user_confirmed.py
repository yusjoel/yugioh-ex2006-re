"""
用户视觉/字形确认的 empty idx 字符 (review group 1-6 + zoom 已并入 seed).
优先级仅次于 seed.
"""

USER_CONFIRMED = {
    # Group 1
    3:    '・',  # F0 83 中点 (与 F0 84 ・ 类似但更小, 字库左下点位置)
    10:   '々',  # F0 8A 重复符号
    30:   '－',  # F0 9E 全角连字符
    341:  '一',  # F2 D5
    382:  '炎',  # F2 FE
    402:  '乙',  # F3 92
    # Group 2
    421:  '火',  # F3 A5
    430:  '霞',  # F3 AE
    601:  '凶',  # F4 B9
    623:  '業',  # F4 CF
    629:  '禁',  # F4 F5
    634:  '金',  # F4 FA
    684:  '穴',  # F5 AC
    739:  '護',  # F5 E3
    747:  '口',  # F5 EB
    831:  '災',  # F6 BF
    # Group 3
    835:  '祭',  # F6 C3
    856:  '殺',  # F6 D8
    860:  '三',  # F6 DC
    862:  '山',  # F6 DE
    896:  '紫',  # F7 80
    985:  '渋',  # F7 D9
    1093: '人',  # F8 45
    1100: '図',  # F8 4C
    1136: '聖',  # F8 70
    1193: '然',  # F8 A9
    # Group 4
    1197: '素',  # F8 AD
    1203: '双',  # F8 B3
    1223: '藻',  # F8 C7
    1253: '太',  # F8 E5
    1274: '大',  # F8 FA
    1286: '谷',  # F9 86
    1298: '団',  # F9 92
    1417: '盗',  # FA 89
    1430: '頭',  # FA 96
    1457: '二',  # FA B1
    # Group 5
    1461: '入',  # FA B5
    1470: '燃',  # FA BE
    1472: '之',  # FA C0
    1479: '覇',  # FA C7
    1497: '白',  # FB D9 (青眼の白龍 关键字)
    1508: '八',  # FB E4
    1511: '罰',  # FB E7
    1605: '文',  # FC C5
    1684: '又',  # FD 94
    1702: '霧',  # FD A6
    # Group 6
    1829: '類',  # FE A5
    1835: '零',  # FE AB
    1836: '霊',  # FE AC
    1837: '麗',  # FE AD
    1841: '裂',  # FE B1
    1859: '六',  # FE C3

    # 数字段 + 箭头/音符等符号 (字库视觉确认, idx 56..71)
    56: '※',  # F0 B8
    57: '→',  # F0 B9
    58: '←',  # F0 BA
    59: '↑',  # F0 BB
    60: '↓',  # F0 BC
    61: '♪',  # F0 BD
    62: '０',  # F0 BE
    63: '１',  # F0 BF
    64: '２',  # F0 C0
    65: '３',  # F0 C1
    66: '４',  # F0 C2
    67: '５',  # F0 C3
    68: '６',  # F0 C4
    69: '７',  # F0 C5
    70: '８',  # F0 C6
    71: '９',  # F0 C7

    # B 类 (繁简/古字 修正) + C 类 (真 codetable 错 修正), 来源 ygocdb jp_name
    337: '遺',
    457: '貝',
    527: '顔',
    643: '喰',
    1045: '象',
    1256: '堕',
    1264: '態',
    1289: '単',
    1333: '徴',
    1360: '壷',
    1708: '盟',
    1790: '嵐',
    1881: '帚',
    1892: '棘',
    1911: '蜴',
    1919: '闢',

    # 最后 2 个 codetable 真错修正 (字库字形对应 ygocdb)
    1114: '雀',
    1173: '尖',

    # 最终一波修正: 5 个 unknown 补 ygocdb + 1 个 codetable 错 (idx 1907 E→翡)
    38: '％',
    318: '案',
    911: '慈',
    1454: '謎',
    1907: '翡',
    1913: '蟲',
}


def char_code_to_idx(code):
    """For code > 0xEFFF (XX encoding)."""
    return ((code & 0xF00) >> 1) | (code & 0x7F)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(f'USER_CONFIRMED size: {len(USER_CONFIRMED)} entries')
    # Compute char_code for each
    for idx, ch in sorted(USER_CONFIRMED.items()):
        # idx → (hi, lo): hi = ((idx >> 7) & 0xF) | 0xF0; lo = idx & 0x7F | 0x80
        hi = ((idx >> 7) & 0xF) | 0xF0
        lo = (idx & 0x7F) | 0x80
        print(f'  idx={idx:4d} → 0x{(hi<<8)|lo:04X}  {ch}')
