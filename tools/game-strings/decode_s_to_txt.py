"""
Decoder: ROM → text/game-strings/{ja,en,de,fr,it,es}.txt

基于 master pointer table @ ROM 0xF40 (1642 行 × 24 B, 顺序 [JA,EN,DE,FR,IT,ES]).
每 row idx 对应 6 lang 的同一 logical entry. 各 lang 的 master 指针在 row 顺序上严格递增.

输出: 6 lang txt, 每 entry 头格式:
    =NNNN= pad=N           # master row idx (0001..1641, 4 数字), 4 位
    =0000= pad=N (empty)   # row 0 = 全 lang 起始空 placeholder
    =NNNN= pad=N (empty)   # 该 lang 此 row 的 ptr → \\0 字节 (此 slot 在该 lang 无翻译)
    =JA_EXTRA_NN= pad=N    # 仅 ja.txt: master 表外 9 条 JA-only (Death Message 尾巴)
SD/OPP 槽附 @ 注释 (来自 master 表特定 row).
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
N_ROWS = 1642

# (lang_name, master_table_col_idx, region_start, region_end_exclusive)
LANG_INFO = [
    ('ja', 0, 0x1DB9C10, 0x1DC4620),
    ('en', 1, 0x1DC4620, 0x1DCF471),
    ('de', 2, 0x1DCF471, 0x1DDB7DE),
    ('fr', 3, 0x1DDB7DE, 0x1DE7CB7),
    ('it', 4, 0x1DE7CB7, 0x1DF3C66),
    ('es', 5, 0x1DF3C66, 0x1DFF9D2),
]

# SD/OPP slot 在 master 表的起始 row
SD_FIRST_ROW = 655   # SD[0..6] = master row 655..661
OPP_FIRST_ROW = 1217  # OPP[0..24] = master row 1217..1241

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

JA_EXTRA_LABELS = [
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


def slot_comment(row_idx):
    """某 master row 是否对应 SD/OPP 槽; 返回注释字符串 (含前导空格) 或空."""
    if SD_FIRST_ROW <= row_idx <= SD_FIRST_ROW + 6:
        n = row_idx - SD_FIRST_ROW
        return f' @ SD[{n}] {SD_NAMES[n]}'
    if OPP_FIRST_ROW <= row_idx <= OPP_FIRST_ROW + 24:
        n = row_idx - OPP_FIRST_ROW
        return f' @ OPP[{n}] {OPP_NAMES[n]}'
    if row_idx == 0:
        return ' @ row 0 = empty placeholder'
    if row_idx == N_ROWS - 1:
        return ' @ last shared entry'
    return ''


def decode_lang(rom, lang_name, col_idx, region_start, region_end):
    """从 ROM 提取此 lang 的所有 entry. 返回 (master_entries, ja_extras)."""
    addrs = []
    for r in range(N_ROWS):
        ptr = struct.unpack_from('<I', rom, TABLE_START + r * 24 + col_idx * 4)[0]
        addrs.append(BASE + ptr)

    # master entries
    master_entries = []  # (row_idx, data_bytes, pad)
    for r in range(N_ROWS):
        addr = addrs[r]
        # data = bytes from addr until first \0 (within region)
        data_end = addr
        while data_end < region_end and rom[data_end] != 0:
            data_end += 1
        data = rom[addr:data_end]
        master_entries.append((r, data, data_end))  # 暂存 data_end, 之后算 pad

    # 计算 pad: pad[r] = addrs[r+1] - data_end[r]; 末 row 在 JA 中需特殊处理
    final = []
    for i, (r, data, de) in enumerate(master_entries):
        if i + 1 < N_ROWS:
            next_addr = addrs[i + 1]
        else:
            # 末 row
            if lang_name == 'ja':
                # 后面有 JA-only extras, pad 到第一个 extra 的 addr
                # 先扫: data_end 后所有 \\0 跳过, 第一个非 \\0 = 第一 extra
                k = de
                while k < region_end and rom[k] == 0:
                    k += 1
                next_addr = k if k < region_end else region_end
            else:
                next_addr = region_end
        pad = next_addr - de
        final.append((r, data, pad))

    # JA extras: 末 master row 数据后的 9 条
    extras = []
    if lang_name == 'ja':
        last_addr = addrs[-1]
        last_de = last_addr
        while last_de < region_end and rom[last_de] != 0:
            last_de += 1
        # 跳过 master-row last entry 的 pad, 走到第一个 extra
        i = last_de
        while i < region_end and rom[i] == 0:
            i += 1
        extra_idx = 0
        while i < region_end:
            es = i
            while i < region_end and rom[i] != 0:
                i += 1
            ed = i
            extra_data = rom[es:ed]
            # extra pad: \\0 数到下一 extra 起点 (或 region 末)
            j = i
            while j < region_end and rom[j] == 0:
                j += 1
            extras.append((extra_idx, extra_data, j - ed))
            i = j
            extra_idx += 1

    return final, extras


def write_txt(lang_name, master_entries, extras, decoder, leading_pad):
    out_path = OUT_DIR / f'{lang_name}.txt'
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        n_real = sum(1 for _, d, _ in master_entries if len(d) > 0)
        f.write(f'@ text/game-strings/{lang_name}.txt — {N_ROWS} master rows '
                f'({n_real} non-empty)')
        if extras:
            f.write(f' + {len(extras)} JA-only extras\n')
        else:
            f.write('\n')
        f.write('@ 由 master pointer table @ ROM 0xF40 (1642 行 × 24 B) 驱动\n')
        f.write('@ 6 lang 跨语言行号严格对齐: 同 row idx → 同 logical entry\n')
        f.write('@\n')
        f.write('@ Format:\n')
        f.write('@   =PRE= pad=N            区段头 leading pad (在 row 0 ptr 之前的 \\0)\n')
        f.write('@   =NNNN= pad=N           master row idx (0000..1641)\n')
        f.write('@   =NNNN= pad=N (empty)   该 lang 此 row 无翻译 (ptr → \\0)\n')
        if lang_name == 'ja':
            f.write('@   =JA_EXTRA_NN= pad=N    master 表外, JA-only Death Message 尾巴\n')
        f.write('@ pad = trailing \\0 byte count, 可达 next 行 ptr 距离 (含 terminator)\n\n')

        if leading_pad > 0:
            f.write(f'=PRE= pad={leading_pad} @ region 起始未指向 leading \\0 区\n\n')

        for row_idx, data, pad in master_entries:
            empty_mark = ' (empty)' if len(data) == 0 else ''
            comment = slot_comment(row_idx)
            f.write(f'={row_idx:04d}= pad={pad}{empty_mark}{comment}\n')
            if data:
                f.write(decoder(data) + '\n')
            f.write('\n')

        if extras:
            f.write('@ === JA-only extras (master 表外) ===\n')
            f.write('@ 在 JA 区 0x1DC3xxx 之后, 通过非 master 表代码路径访问\n\n')
            for extra_idx, data, pad in extras:
                label = JA_EXTRA_LABELS[extra_idx] if extra_idx < len(JA_EXTRA_LABELS) else ''
                comment = f' @ {label}' if label else ''
                f.write(f'=JA_EXTRA_{extra_idx:02d}= pad={pad}{comment}\n')
                f.write(decoder(data) + '\n\n')

    size = os.path.getsize(out_path)
    n_master_real = sum(1 for _, d, _ in master_entries if len(d) > 0)
    print(f'  {lang_name}: {N_ROWS} master ({n_master_real} non-empty)'
          f' + {len(extras)} extras → {out_path} ({size} B)')


def main():
    rom = open(ROM_PATH, 'rb').read()
    print(f'Decoding 6 lang from master pointer table (ROM 0x{TABLE_START:X}, {N_ROWS} rows)')
    for lang, col, rs, re_ in LANG_INFO:
        decoder = decode_ja if lang == 'ja' else decode_5lang
        master_entries, extras = decode_lang(rom, lang, col, rs, re_)
        # 区段头 leading pad: row 0 ptr 之前的 \0 字节数
        row0_ptr = struct.unpack_from('<I', rom, TABLE_START + 0*24 + col*4)[0]
        leading_pad = (BASE + row0_ptr) - rs
        write_txt(lang, master_entries, extras, decoder, leading_pad)


if __name__ == '__main__':
    main()
else:
    main()
