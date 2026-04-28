"""
Decoder: ROM → text/game-strings/{ja,en,de,fr,it,es}.txt

基于 master pointer table @ ROM 0xF40 (1651 行 × 24 B, 顺序 [JA,EN,DE,FR,IT,ES]).
每 row idx 对应 6 lang 的同一 logical entry. 各 lang 的 master 指针在 row 顺序上严格递增.

行区分:
- Rows 0000..1641: 共享 6 lang UI 文本 (1642 行)
- Rows 1642..1650: Death Message 尾巴 (9 行)
  · JA col 是真实日文 (kanji/hiragana 单字 + 长描述)
  · 5 lang col 一律 ptr → \\0\\0 (无翻译, len=0 pad=2)

输出: 6 lang txt, 每 entry 头格式:
    =NNNN= pad=N           # master row idx (0000..1650, 4 数字)
    =NNNN= pad=N (empty)   # 该 lang 此 row 的 ptr → \\0 字节 (无翻译)
SD/OPP 槽 + Death Message 槽附 @ 注释.
"""
import os
import re
import json
import struct
from pathlib import Path

ROM_PATH = 'roms/2343.gba'
OUT_DIR = Path('text/game-strings')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Master pointer table 参数
BASE = 0x1DB9C10
TABLE_START = 0xF40
N_ROWS = 1651              # 1642 共享 + 9 Death Message tail

# (lang_name, master_table_col_idx, region_start, region_end_exclusive)
# 各 lang region_end 已含其自身的 9 行 Death Message tail (18 B \0) + 必要对齐 pad.
LANG_INFO = [
    ('ja', 0, 0x1DB9C10, 0x1DC4620),
    ('en', 1, 0x1DC4620, 0x1DCF484),
    ('de', 2, 0x1DCF484, 0x1DDB7F2),
    ('fr', 3, 0x1DDB7F2, 0x1DE7CCA),
    ('it', 4, 0x1DE7CCA, 0x1DF3C7A),
    ('es', 5, 0x1DF3C7A, 0x1DFF9E4),
]

# SD/OPP slot 在 master 表的起始 row
SD_FIRST_ROW = 655   # SD[0..6] = master row 655..661
OPP_FIRST_ROW = 1217  # OPP[0..24] = master row 1217..1241
DEATH_FIRST_ROW = 1642  # Death Message 尾巴 9 行 (1642..1650), JA-only 内容

SD_NAMES = [
    'Starter Deck', "Dragon's Roar", 'Zombie Madness', 'Blazing Destruction',
    'Fury From the Deep', "Warrior's Triumph", "Spellcaster's Judgement",
]
OPP_NAMES = [
    'Kuriboh', 'Scapegoat', 'Skull Servant', 'Watapon', 'Pikeru',
    'Batteryman C', 'Ojama Yellow', 'Goblin King', 'Des Frog', 'Water Dragon',
    'REDD', 'Vampire Genesis', 'Infernal Flame Emperor', 'Ocean Dragon Lord',
    'Helios Duo Megiste', 'Gilford the Legend', 'Dark Eradicator Warlock',
    'Guardian Exode', 'Goldd', 'Electrum', 'Raviel', 'Horus', 'Stronghold',
    'Sacred Phoenix', 'Cyber End Dragon',
]

DEATH_LABELS = [
    'Death Message description (long)',
    'Death Message kanji 「Ｉ」',
    'Death Message kanji 「Ｎ」',
    'Death Message kanji 「Ａ」',
    'Death Message kanji 「Ｌ」',
    'Death Message hiragana アイ',
    'Death Message hiragana エヌ',
    'Death Message hiragana エー',
    'Death Message hiragana エル',
]

CT = {int(k): v for k, v in json.loads(
    open('tools/jp-decode/codetable.json', encoding='utf-8').read()
)['by_idx'].items()}


def decode_ja(bs):
    """JA 字节流 → UTF-8 字符串.
    规则: byte >= 0xF0 → 2B JA pair (高 nibble = F, idx 来自 codetable),
         byte < 0xF0 → 1B raw 字节 (chr(b)).
    注: ROM JA 区段中 hi byte 几乎全 0xF0-0xFE, 但有 1 个孤例 (0x9E 0x8A = idx 1802 '立',
        在 staff credits row 956 出现 1 次). 此孤例由 0xF0 阈值切成 2 个 raw 字节
        (\\x9e + \\x8a) 透传到 txt; encoder 反向写为 raw bytes 0x9E 0x8A 保 byte-identical.
    """
    out = []
    i = 0
    while i < len(bs):
        b = bs[i]
        if b >= 0xF0 and i + 1 < len(bs):
            idx = ((b & 0xF) << 7) | (bs[i + 1] & 0x7F)
            ch = CT.get(idx)
            if ch is None:
                raise ValueError(f'idx {idx} (bytes {b:02X} {bs[i+1]:02X}) not in codetable')
            out.append(ch)
            i += 2
        else:
            out.append(chr(b))
            i += 1
    return ''.join(out)


def decode_5lang(bs):
    """CP1252 字节流 → UTF-8."""
    return bs.decode('cp1252')


def slot_comment(row_idx, lang_name):
    """某 master row 是否对应 SD/OPP/Death Message 槽; 返回注释字符串 (含前导空格) 或空."""
    if SD_FIRST_ROW <= row_idx <= SD_FIRST_ROW + 6:
        n = row_idx - SD_FIRST_ROW
        return f' @ SD[{n}] {SD_NAMES[n]}'
    if OPP_FIRST_ROW <= row_idx <= OPP_FIRST_ROW + 24:
        n = row_idx - OPP_FIRST_ROW
        return f' @ OPP[{n}] {OPP_NAMES[n]}'
    if DEATH_FIRST_ROW <= row_idx <= DEATH_FIRST_ROW + 8 and lang_name == 'ja':
        return f' @ {DEATH_LABELS[row_idx - DEATH_FIRST_ROW]}'
    if row_idx == 0:
        return ' @ row 0 = empty placeholder'
    return ''


def decode_lang(rom, col_idx, region_end):
    """从 ROM 提取此 lang 全 N_ROWS 个 entry. 1642..1650 为 Death Message tail, 在
    5 lang 一律 ptr → \\0 (空, pad=2). 返回 [(row_idx, data_bytes, pad)]."""
    addrs = []
    for r in range(N_ROWS):
        ptr = struct.unpack_from('<I', rom, TABLE_START + r * 24 + col_idx * 4)[0]
        addrs.append(BASE + ptr)

    entries = []
    for r in range(N_ROWS):
        addr = addrs[r]
        data_end = addr
        while data_end < region_end and rom[data_end] != 0:
            data_end += 1
        data = rom[addr:data_end]
        next_addr = addrs[r + 1] if r + 1 < N_ROWS else region_end
        entries.append((r, data, next_addr - data_end))
    return entries


def write_txt(lang_name, entries, decoder, leading_pad):
    out_path = OUT_DIR / f'{lang_name}.txt'
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        n_real = sum(1 for _, d, _ in entries if len(d) > 0)
        f.write(f'@ text/game-strings/{lang_name}.txt — {N_ROWS} master rows '
                f'({n_real} non-empty)\n')
        f.write('@ 由 master pointer table @ ROM 0xF40 (1651 行 × 24 B) 驱动\n')
        f.write('@ 6 lang 跨语言行号严格对齐: 同 row idx → 同 logical entry\n')
        f.write('@\n')
        f.write('@ Format:\n')
        f.write('@   =PRE= pad=N            区段头 leading pad (在 row 0 ptr 之前的 \\0)\n')
        f.write('@   =NNNN= pad=N           master row idx (0000..1650)\n')
        f.write('@   =NNNN= pad=N (empty)   该 lang 此 row 无翻译 (ptr → \\0)\n')
        f.write('@\n')
        f.write('@ Rows 0000..1641: 共享 6 lang UI 文本 (1642 行)\n')
        f.write('@ Rows 1642..1650: Death Message 尾巴 (9 行) — JA 真实日文; 5 lang 全 (empty)\n')
        f.write('@ pad = trailing \\0 byte count, 可达 next 行 ptr 距离 (含 terminator)\n\n')

        if leading_pad > 0:
            f.write(f'=PRE= pad={leading_pad} @ region 起始未指向 leading \\0 区\n\n')

        for row_idx, data, pad in entries:
            empty_mark = ' (empty)' if len(data) == 0 else ''
            comment = slot_comment(row_idx, lang_name)
            f.write(f'={row_idx:04d}= pad={pad}{empty_mark}{comment}\n')
            if data:
                f.write(decoder(data) + '\n')
            f.write('\n')

    size = os.path.getsize(out_path)
    print(f'  {lang_name}: {N_ROWS} rows ({n_real} non-empty) → {out_path} ({size} B)')


def main():
    rom = open(ROM_PATH, 'rb').read()
    print(f'Decoding 6 lang from master pointer table (ROM 0x{TABLE_START:X}, {N_ROWS} rows)')
    for lang, col, rs, re_ in LANG_INFO:
        decoder = decode_ja if lang == 'ja' else decode_5lang
        entries = decode_lang(rom, col, re_)
        # 区段头 leading pad: row 0 ptr 之前的 \0 字节数
        row0_ptr = struct.unpack_from('<I', rom, TABLE_START + 0*24 + col*4)[0]
        leading_pad = (BASE + row0_ptr) - rs
        write_txt(lang, entries, decoder, leading_pad)


if __name__ == '__main__':
    main()
else:
    main()
