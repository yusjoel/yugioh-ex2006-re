#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XX 编码解码器 (data/card-names.s lang=0 槽)

依据 doc/dev/xx-encoding-analysis.md 的码表实现。

用法:
    from tools.xx_codec import decode_xx
    decode_xx(b'\\xf8\\xf7\\xf4\\x8c\\xf1\\xa9\\xfb\\xd9\\xfe\\x91')
    # → '[F8F7][F48C]の[FBD9][FE91]'  (青眼の白龍, kanji 未识别)

或命令行:
    python tools/xx_codec.py 1 5 16 22 37     # 解码若干 cid 的 XX

覆盖率: 平假名 + 片假名 ~99% (假说), 汉字仅 ~20 个手工对齐。
"""
from __future__ import annotations
import struct
import sys

# ---------------------------------------------------------------------------
# 码表
# ---------------------------------------------------------------------------

# 片假名 HI=F1 LO=D0..FF (48 字, 完全验证)
F1_KATA = "アィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパ"

# 片假名 HI=F2 LO=80..A1 (34 字, 完全验证)
F2_KATA = "ヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲン"

# 平假名 HI=F1 LO=80..CE (假说基于 50-音表 + 已确认锚点)
HIRA = {
    # 80..85: 未确定 (可能 a-行变体)
    0x86: 'か', 0x87: 'が', 0x88: 'き', 0x89: 'ぎ',
    0x8A: 'く', 0x8B: 'ぐ', 0x8C: 'け', 0x8D: 'げ',
    0x8E: 'こ', 0x8F: 'ご',
    0x90: 'さ', 0x91: 'ざ', 0x92: 'し', 0x93: 'じ',
    0x94: 'す', 0x95: 'ず', 0x96: 'せ', 0x97: 'ぜ',
    0x98: 'そ', 0x99: 'ぞ',
    0x9A: 'た', 0x9B: 'だ', 0x9C: 'ち', 0x9D: 'ぢ',
    0x9E: 'っ', 0x9F: 'つ', 0xA0: 'づ',
    0xA1: 'て', 0xA2: 'で', 0xA3: 'と', 0xA4: 'ど',
    0xA5: 'な', 0xA6: 'に', 0xA7: 'ぬ', 0xA8: 'ね', 0xA9: 'の',
    0xAA: 'は', 0xAB: 'ば', 0xAC: 'ぱ',
    0xAD: 'ひ', 0xAE: 'び', 0xAF: 'ぴ',
    0xB0: 'ふ', 0xB1: 'ぶ', 0xB2: 'ぷ',
    0xB3: 'へ', 0xB4: 'べ', 0xB5: 'ぺ',
    0xB6: 'ほ', 0xB7: 'ぼ', 0xB8: 'ぽ',
    0xB9: 'ま', 0xBA: 'み', 0xBB: 'む', 0xBC: 'め', 0xBD: 'も',
    0xBE: 'ゃ', 0xBF: 'や', 0xC0: 'ゅ', 0xC1: 'ゆ', 0xC2: 'ょ', 0xC3: 'よ',
    0xC4: 'ら', 0xC5: 'り', 0xC6: 'る', 0xC7: 'れ', 0xC8: 'ろ',
    0xC9: 'ゎ', 0xCA: 'わ', 0xCB: 'ゐ', 0xCC: 'ゑ', 0xCD: 'を', 0xCE: 'ん',
}

# F0 特殊符号 + 全角拉丁字母 (HI=F0)
# 由 cid=2000 "E・HERO スチーム・ヒーラー" 解码定位 A=F0C8, E=F0CC, O=F0D6, R=F0D9 等 → A..Z 连续
F0_SPECIAL = {
    0x80: ' ',     # 全角空格 (出现 131 次, 高频)
    0x84: '・',
    0x8B: 'ー',
}
# 全角 A..Z @ F0 C8..E1
for _i, _ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    F0_SPECIAL[0xC8 + _i] = _ch
# 全角 a..z 推测在某段 (尚未确认范围)

# 汉字 (手工对齐 19 个)
KANJI = {
    (0xF2, 0xD8): '印',
    (0xF2, 0xE0): '右',
    (0xF3, 0xF1): '喚',
    (0xF4, 0x8C): '眼',
    (0xF5, 0xB5): '剣',
    (0xF6, 0xAF): '左',
    (0xF6, 0xEE): '士',
    (0xF6, 0xF4): '師',
    (0xF7, 0x91): '時',
    (0xF7, 0xAA): '者',
    (0xF7, 0xE3): '術',
    (0xF7, 0xFD): '召',
    (0xF8, 0xF7): '青',
    (0xF9, 0xD7): '足',
    (0xFB, 0xD9): '白',
    (0xFC, 0xB1): '封',
    (0xFD, 0x8B): '魔',     # 时の魔術師
    (0xFE, 0x91): '龍',
    (0xFE, 0xCC): '腕',
}


def decode_xx(xx: bytes) -> str:
    """解码 XX 字节序列 → 字符串. 未识别 byte-pair 显示为 [HHLL]."""
    if len(xx) % 2 != 0:
        return f'<bad length {len(xx)}: {xx.hex()}>'
    out = []
    for i in range(0, len(xx), 2):
        hi, lo = xx[i], xx[i+1]
        ch = decode_pair(hi, lo)
        out.append(ch)
    return ''.join(out)


def decode_pair(hi: int, lo: int) -> str:
    """解码单个 byte-pair → 单字符或占位符."""
    if hi == 0xF1:
        if 0xD0 <= lo <= 0xFF:
            idx = lo - 0xD0
            if idx < len(F1_KATA):
                return F1_KATA[idx]
        elif lo in HIRA:
            return HIRA[lo]
    elif hi == 0xF2:
        if 0x80 <= lo <= 0xA1:
            idx = lo - 0x80
            if idx < len(F2_KATA):
                return F2_KATA[idx]
        # F2 A2..FF: kanji
        if (hi, lo) in KANJI:
            return KANJI[(hi, lo)]
    elif hi == 0xF0:
        if lo in F0_SPECIAL:
            return F0_SPECIAL[lo]
    elif (hi, lo) in KANJI:
        return KANJI[(hi, lo)]
    return f'[{hi:02X}{lo:02X}]'


def main():
    """命令行: 给定若干 cid，输出对应 XX 解码."""
    import os, io
    # Force UTF-8 output for Windows GBK consoles
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    ROM_PATH = 'roms/2343.gba'
    PTR_TABLE = 0x015F3A5C
    NAMES_BASE = 0x015BB594

    if len(sys.argv) < 2:
        print('用法: python tools/xx_codec.py <cid1> [cid2 ...]', file=sys.stderr)
        print('   或: python tools/xx_codec.py all              (解码全 ROM)', file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(ROM_PATH):
        print(f'错误: {ROM_PATH} 不存在 (请在项目根目录运行)', file=sys.stderr)
        sys.exit(1)

    with open(ROM_PATH, 'rb') as f:
        rom = f.read()

    def get_xx(cid: int) -> bytes:
        ptr = struct.unpack_from('<I', rom, PTR_TABLE + cid * 6 * 4)[0]
        off = NAMES_BASE + ptr
        end = off
        while end < len(rom) and rom[end] != 0:
            end += 1
        return rom[off:end]

    def get_en(cid: int) -> str:
        ptr = struct.unpack_from('<I', rom, PTR_TABLE + (cid * 6 + 1) * 4)[0]
        off = NAMES_BASE + ptr
        end = off
        while end < len(rom) and rom[end] != 0:
            end += 1
        return rom[off:end].decode('cp1252', errors='replace')

    if sys.argv[1] == 'all':
        cids = range(1, 2102)
    else:
        cids = [int(x) for x in sys.argv[1:]]

    full = 0; total = 0
    for cid in cids:
        xx = get_xx(cid)
        if not xx: continue
        total += 1
        en = get_en(cid)
        dec = decode_xx(xx)
        if '[' not in dec: full += 1
        print(f'cid={cid:>4}  EN={en:<35}  XX={dec}')

    if total > 1:
        print(f'\n完全解码: {full}/{total} ({100*full/total:.1f}%)')


if __name__ == '__main__':
    main()
