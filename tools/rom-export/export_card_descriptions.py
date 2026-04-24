#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡牌描述合并导出 (取代 export_card_descriptions.py + export_card_effect_text.py)

ROM 范围: 0x015FFF0C ~ 0x018169B6 (= 2,190,506 B)

三段:
  1. card_descs_table    ROM 0x15FFF0C ~ 0x180A508  (2,139,644 B)
     2098 cards × 6 langs (cid=0..2097) null-terminated, 顺序 XX/EN/DE/FR/IT/ES
  2. card_desc_pointer_table         ROM 0x180A508 ~ 0x1816580  (49,272 B = 12,318 × u32)
     cid=0..2052 的 offset 表, 每卡用 desc_offsets 宏展开
  3. card_desc_ptr_table    ROM 0x1816580 ~ 0x18169B4  (269 × u32 + 2 B tail)
     cid=2053..2097 的 offset 表 (末卡 cid=2097 缺 ES, 单独 5 × .word 展开)

语义约定:
  - lang 顺序 XX/EN/DE/FR/IT/ES (与 card-names.s 一致)
  - XX lang 所有字节用 \\NNN 八进制转义 (可读性/工具友好)
  - 其他 lang 字符尽量用字面 CP1252, 未定义字节 (0x81/8D/8F/90/9D) 用 \\NNN
  - 每个 lang 字符串单行 .ascii 完整输出
  - 异画卡 (alt-art) 复用 master cid 的 label, pool 里不重复定义
  - cid=2097 ES 物理存在但无 u32 指针; 仍打 label 供 pool 完整
  - 字节重叠: Section B u32[0]=0 同时作 pool 尾 cid 占位 null (Card 38 XX overlap)
"""

import os
import struct
import sys

ROM_PATH = 'roms/2343.gba'
OUT_DIR = 'data'
ASM_OUT = os.path.join(OUT_DIR, 'card-descriptions.s')

POOL_START   = 0x015FFF0C
ET_END       = 0x01800000
SEC_A_END    = 0x0180A508
SEC_B_START  = 0x0180A508
SEC_B_END    = 0x01816580
SEC_C_START  = 0x01816580
AREA_END     = 0x018169B8   # Section C 真实末端 (最末 u32 高 2B 与 card-stats zero0 字节重叠)

N_CARDS_TOTAL = 2098            # cid=0..2097
N_CARDS_B     = 2053            # Section B 覆盖 cid=0..2052
N_B_U32       = N_CARDS_B * 6   # 12,318
N_CARDS_C     = 45              # Section C 覆盖 cid=2053..2097
N_PTRS_C      = N_CARDS_C * 6   # 270 (最末 u32 高 2B 与 card-stats[0].zero0 共享)

LANG_NAMES    = ['xx', 'en', 'de', 'fr', 'it', 'es']

CARD_NAME_BASE = 0x015BB594
CARD_NAME_PTR  = 0x015F3A5C


def emit_string_oneline(data: bytes, lang: str, out: list):
    """把字节序列输出为单行 `.ascii "..."`。
    XX lang 所有非可打印 ASCII 字节用 \\NNN 八进制；其他 lang 尽量 CP1252 字面。"""
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
            if 0x20 <= b < 0x7F:
                pieces.append(chr(b))
            elif b == 0x0A: pieces.append('\\n')
            elif b == 0x0D: pieces.append('\\r')
            elif b == 0x09: pieces.append('\\t')
            elif 0xA0 <= b <= 0xFF:
                pieces.append(chr(b))
            elif 0x80 <= b <= 0x9F:
                try:
                    pieces.append(bytes([b]).decode('cp1252'))
                except (UnicodeDecodeError, ValueError):
                    pieces.append(f'\\{b:03o}')
            else:
                pieces.append(f'\\{b:03o}')
    out.append('\t.ascii "' + ''.join(pieces) + '"')


def load_card_names_en(rom: bytes) -> list[str]:
    names = []
    for cid in range(N_CARDS_TOTAL):
        off = struct.unpack_from('<I', rom, CARD_NAME_PTR + (cid * 6 + 1) * 4)[0]
        addr = CARD_NAME_BASE + off
        j = addr
        while j < CARD_NAME_BASE + 0x5C000 and rom[j] != 0:
            j += 1
        names.append(rom[addr:j].decode('cp1252', errors='replace'))
    return names


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print(f'ERROR: {ROM_PATH} not found', file=sys.stderr)
        sys.exit(1)

    rom = open(ROM_PATH, 'rb').read()

    # 读 Section B (12,318 u32) + Section C (270 u32)
    sec_b = [struct.unpack_from('<I', rom, SEC_B_START + i * 4)[0] for i in range(N_B_U32)]
    sec_c = [struct.unpack_from('<I', rom, SEC_C_START + i * 4)[0] for i in range(N_PTRS_C)]

    pool_size = SEC_A_END - POOL_START

    # 合成完整 offset 表: cid=0..2097 × 6 lang = 12,588 entries
    all_off = list(sec_b) + list(sec_c)
    assert len(all_off) == N_CARDS_TOTAL * 6, f'expected 12588, got {len(all_off)}'

    # 验证每个 offset 的前一字节都是 null (字符串起点)
    for i, off in enumerate(all_off):
        if off == 0:
            continue
        prev = rom[POOL_START + off - 1]
        assert prev == 0, f'offset[{i}]={off} 前一字节 0x{prev:02X} 非 null'

    # master_of: 每 cid 的 6 u32 组首次出现时的 cid
    group_to_master: dict[tuple, int] = {}
    master_of: list[int] = [0] * N_CARDS_TOTAL
    for cid in range(N_CARDS_TOTAL):
        grp = tuple(all_off[cid * 6:(cid + 1) * 6])
        master_of[cid] = group_to_master.setdefault(grp, cid)

    card_names = load_card_names_en(rom)

    # 构建 label_map: offset -> [label 名]
    # 只在 master cid 处打 label, alt-art cid 共享 master 的 label
    label_map: dict[int, list[str]] = {}
    for cid in range(N_CARDS_TOTAL):
        if master_of[cid] != cid:
            continue
        for lang_idx in range(6):
            off = all_off[cid * 6 + lang_idx]
            label_map.setdefault(off, []).append(
                f'card_desc_{cid:04d}_{LANG_NAMES[lang_idx]}'
            )

    assert all(0 <= off <= pool_size for off in label_map)

    # 生成 ASM
    out: list[str] = []
    out.append('@ =============================================================================')
    out.append('@ Card Descriptions (merged: effect-text + special-card text)')
    out.append(f'@ ROM 0x{POOL_START:07X} - 0x{AREA_END:07X}  ({AREA_END - POOL_START:,} B)')
    out.append('@')
    out.append(f'@  1. card_descs_table   0x{POOL_START:07X} - 0x{SEC_A_END:07X}'
               f'  ({pool_size:,} B)')
    out.append(f'@     {N_CARDS_TOTAL} cards x 6 langs (XX/EN/DE/FR/IT/ES), null-terminated')
    out.append(f'@  2. card_desc_pointer_table        0x{SEC_B_START:07X} - 0x{AREA_END:07X}'
               f'  ({AREA_END - SEC_B_START:,} B, cid=0..{N_CARDS_TOTAL-1})')
    out.append(f'@     Last u32 high 2B byte-overlaps with card_stats[0].zero0 (=0x0020).')
    out.append('@')
    out.append('@ File encoding: CP1252')
    out.append('@ Generated by tools/rom-export/export_card_descriptions.py')
    out.append('@ =============================================================================')
    out.append('')

    out.append('@ Macro: 6 lang offsets for cid (label - pool)')
    out.append('.macro desc_offsets cid')
    out.append('\t.word card_desc_\\cid\\()_xx - card_descs_table')
    out.append('\t.word card_desc_\\cid\\()_en - card_descs_table')
    out.append('\t.word card_desc_\\cid\\()_de - card_descs_table')
    out.append('\t.word card_desc_\\cid\\()_fr - card_descs_table')
    out.append('\t.word card_desc_\\cid\\()_it - card_descs_table')
    out.append('\t.word card_desc_\\cid\\()_es - card_descs_table')
    out.append('.endm')
    out.append('')

    # ---------- 1. Pool ----------
    out.append('@ -----------------------------------------------------------------------------')
    out.append(f'@ 1. Text Pool ({N_CARDS_TOTAL} cards x 6 langs, null-terminated, 2-byte aligned)')
    out.append(f'@    ROM 0x{POOL_START:07X} - 0x{SEC_A_END:07X}  ({pool_size:,} B)')
    out.append(f'@    Master cids (unique u32 groups): {len(set(master_of))},'
               f' alt-art cards share labels')
    out.append('@ -----------------------------------------------------------------------------')
    out.append('card_descs_table:')

    # 按 cid 顺序遍历 master，每 lang 单独输出 (单行 .ascii)
    for cid in range(N_CARDS_TOTAL):
        if master_of[cid] != cid:
            continue  # alt-art 跳过
        for lang_idx in range(6):
            lang = LANG_NAMES[lang_idx]
            off = all_off[cid * 6 + lang_idx]
            # 字符串范围: [off, next_off)，next_off 是排序后下一 offset 或 pool_size
            # 为快速查找, 用 sorted_unique_offsets
            pass  # 暂存, 下面统一处理

    # 更高效: 按 sorted unique offset 遍历
    sorted_offsets = sorted(label_map.keys())
    for i, off in enumerate(sorted_offsets):
        labels = label_map[off]
        next_off = sorted_offsets[i + 1] if i + 1 < len(sorted_offsets) else pool_size
        # 打 label
        for lbl in labels:
            out.append(f'{lbl}:')
        # 输出该段字节 (单行 .ascii)
        chunk = bytes(rom[POOL_START + off:POOL_START + next_off])
        # lang 来自 label 名后缀 (所有 label 在同一 offset lang 相同)
        lang = labels[0].rsplit('_', 1)[1]
        emit_string_oneline(chunk, lang, out)

    # ---------- 2. card_desc_pointer_table (Section B + C 连续, 2098 cards x 6 langs) ----------
    out.append('')
    out.append('@ -----------------------------------------------------------------------------')
    out.append(f'@ 2. card_desc_pointer_table: cid=0..{N_CARDS_TOTAL-1} × 6 langs'
               f' = {N_CARDS_TOTAL * 6} × u32')
    out.append(f'@    ROM 0x{SEC_B_START:07X} - 0x{AREA_END:07X}  ({AREA_END - SEC_B_START:,} B)')
    out.append(f'@    Last u32 (cid=2097 ES offset = 0x0020A532) high 2 bytes byte-overlap')
    out.append(f'@    with card_stats[0].zero0 (=0x0020) at ROM 0x{AREA_END-2:07X}..0x{AREA_END-1:07X}.')
    out.append('@ -----------------------------------------------------------------------------')
    out.append('card_desc_pointer_table:')
    for cid in range(N_CARDS_TOTAL):
        mc = master_of[cid]
        name = card_names[cid].strip()
        if not name:
            name = '(dummy)' if cid == 0 else '(empty)'
        alt = '' if mc == cid else ' (alt-art)'
        out.append(f'\tdesc_offsets {mc:04d}    @ card id: {cid}, {name[:48]}{alt}')

    out.append('')

    content = '\n'.join(out) + '\n'
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(ASM_OUT, 'w', encoding='cp1252') as f:
        f.write(content)

    masters = sum(1 for cid in range(N_CARDS_TOTAL) if master_of[cid] == cid)
    print(f'ASM file: {ASM_OUT}')
    print(f'  Pool size:          {pool_size:,} B')
    print(f'  Total cards:        {N_CARDS_TOTAL} (cid=0..{N_CARDS_TOTAL-1})')
    print(f'  Master cids:        {masters}  (alt-art cards share labels)')
    print(f'  Unique label posns: {len(label_map):,}')
    print(f'  Total label defs:   {sum(len(v) for v in label_map.values()):,}')
    print(f'  Output size:        {len(content):,} chars, {content.count(chr(10)):,} lines')


if __name__ == '__main__':
    main()
