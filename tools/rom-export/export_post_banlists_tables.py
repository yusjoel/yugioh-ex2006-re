#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post-banlists 段 4 张未结构化数据表导出

ROM 区段: 0x1E5F71C..0x1E5F884 (0x168 = 360 B)
内含:
  level_signature_table  @ 0x1E5F71C, 0x118 (280 B = 14 × 20 B records)
                         字段 {u16 so_code, char field_a[8], char field_b[8], u16 pad}
                         caller: 0x080EF474 (base) / 0x0801D8A0 (rec[0].field_a) / 0x0801D8FC (rec[0].field_b)
                         渲染器逐字节解码 ASCII: '?'(0x3F)→glyph 14, 'X'(0x58)→glyph 15, '0'-'9'→数字
  font_jp_dim_table      @ 0x1E5F834,  32 B (4 × {u32, u32}) 维度配对，含义未确认
  font_jp_base_table     @ 0x1E5F854,  32 B (8 × u32 ptrs) ⭐ 92 直接 ldrs
                         前 4 = alt fallback fonts (state-bits 选择)
                         后 4 = font_jp_main_small/main_large/outline_small/outline_large
  font_jp_stride_table   @ 0x1E5F874,  16 B (4 × u32 = 100/144/144/196 = per-glyph 字节数)

输出:
  data/post-banlists-tables.s
"""

import os
import struct
import sys

ROM_PATH = 'roms/2343.gba'
ASM_OUT = 'data/post-banlists-tables.s'

LEVEL_SIG_OFFSET = 0x1E5F71C
LEVEL_SIG_SIZE = 0x118

# ---- 硬编码表 (与 ROM 字节流 byte-identical, build.bat 验证) ----
DIM_PAIRS = [(10, 12), (5, 6), (10, 12), (10, 12)]

BASES = [
    ('0x09BA3340',                'alt[0] (in 字库前段 gap)'),
    ('0x09C20374',                'alt[1] (in font-jp gap1)'),
    ('0x09CCB490',                'alt[2] (tail gap start)'),
    ('0x09CCBE90',                'alt[3] (within tail gap)'),
    ('font_jp_main_small',        '10×10 / 100 B/glyph'),
    ('font_jp_main_large',        '12×12 / 144 B/glyph'),
    ('font_jp_outline_small',     '12×12 / 144 B/glyph'),
    ('font_jp_outline_large',     '14×14 / 196 B/glyph'),
]

STRIDES = [(100, '10×10'), (144, '12×12'), (144, '12×12'), (196, '14×14')]


def verify_against_rom(rom):
    """启动期 sanity check: 硬编码值是否与 ROM 字节一致, 不一致就早退."""
    # dim_table @ 0x1E5F834
    expected_dim = []
    for a, b in DIM_PAIRS:
        expected_dim.extend([a, b])
    actual_dim = list(struct.unpack_from('<8I', rom, 0x1E5F834))
    assert expected_dim == actual_dim, 'dim_table mismatch: %s vs %s' % (expected_dim, actual_dim)

    # base_table @ 0x1E5F854
    actual_bases = list(struct.unpack_from('<8I', rom, 0x1E5F854))
    expected_bases = [0x09BA3340, 0x09C20374, 0x09CCB490, 0x09CCBE90,
                      0x09BAC9A4, 0x09C2B7EC, 0x09BDB998, 0x09C6F2BC]
    assert expected_bases == actual_bases, 'base_table mismatch'

    # stride_table @ 0x1E5F874
    actual_strides = list(struct.unpack_from('<4I', rom, 0x1E5F874))
    expected_strides = [s for s, _ in STRIDES]
    assert expected_strides == actual_strides, 'stride_table mismatch'


def generate_asm():
    L = []
    L.append('@ =============================================================================')
    L.append('@ post-banlists 4 张未结构化数据表 (banlist_master_table 之后, starter-deck 之前)')
    L.append('@ ROM偏移: 0x1E5F71C - 0x1E5F883 (共 0x168 = 360 B)')
    L.append('@')
    L.append('@   level_signature_table  @ 0x1E5F71C, 0x118 (14 × 20 B records)')
    L.append('@   font_jp_dim_table      @ 0x1E5F834, 0x20  (4 × {u32, u32})')
    L.append('@   font_jp_base_table     @ 0x1E5F854, 0x20  (8 × u32 ptrs) ⭐ HOT 92 ldrs')
    L.append('@   font_jp_stride_table   @ 0x1E5F874, 0x10  (4 × u32 strides)')
    L.append('@')
    L.append('@ 由 tools/rom-export/export_post_banlists_tables.py 生成')
    L.append('@ =============================================================================')
    L.append('')

    # ---- level_signature_table (incbin) ----
    L.append('@ -----------------------------------------------------------------------------')
    L.append('@ Level Signature Table (推测: Limited Duel 难度等级数据)')
    L.append('@ GBA地址: 0x09E5F71C  ROM偏移: 0x1E5F71C')
    L.append('@ 14 条 × 20 字节 = 0x118 = 280 字节')
    L.append('@ 结构 {u16 signal_so_code, char field_a[8], char field_b[8], u16 pad}')
    L.append('@ 渲染器 (FUN_0801D810 area) 逐字节解码 ASCII:')
    L.append('@   0x3F (\'?\') → glyph 14, 0x58 (\'X\') → glyph 15, 0x30..0x39 (\'0\'..\'9\') → 数字')
    L.append('@ caller: base @ 0x080EF474, rec[0].field_a @ 0x0801D8A0, rec[0].field_b @ 0x0801D8FC')
    L.append('@ -----------------------------------------------------------------------------')
    L.append('level_signature_table:')
    # 保留渲染代码已引用的记录内字段标签，避免全量重导后链接失败。
    L.append('    .incbin "roms/2343.gba", 0x%X, 0x2   @ rec[0].so_code field (u16, 2B)' % LEVEL_SIG_OFFSET)
    L.append('level_signature_table_field_a:                 @ 0x09E5F71E: rec[0].field_a base (char[8], stride=20B per rec)')
    L.append('    .incbin "roms/2343.gba", 0x%X, 0x8   @ rec[0].field_a (8B)' % (LEVEL_SIG_OFFSET + 2))
    L.append('level_signature_table_field_b:                 @ 0x09E5F726: rec[0].field_b base (char[8], stride=20B per rec)')
    L.append('    .incbin "roms/2343.gba", 0x%X, 0x%x @ remainder: 0x118 - 0x2 - 0x8 = 0x10e (field_b + rest of table)' % (LEVEL_SIG_OFFSET + 10, LEVEL_SIG_SIZE - 10))
    L.append('')

    # ---- font_jp_dim_table ----
    L.append('@ -----------------------------------------------------------------------------')
    L.append('@ font_jp_dim_table @ 0x09E5F834 (32 B = 4 × {u32, u32})')
    L.append('@ 4 个字体的维度配对 (含义未完全确认; 与 base_table[0..3] 对齐)')
    L.append('@ -----------------------------------------------------------------------------')
    L.append('font_jp_dim_table:')
    for i, (a, b) in enumerate(DIM_PAIRS):
        L.append('    .word %2d, %2d         @ pair[%d]' % (a, b, i))
    L.append('')

    # ---- font_jp_base_table ----
    L.append('@ -----------------------------------------------------------------------------')
    L.append('@ font_jp_base_table @ 0x09E5F854 (32 B = 8 × u32) ⭐ HOT 92 ldrs')
    L.append('@ 访问模式: state_bits → offset {0,4,8,12} → ptr[0..3] (alt fallback fonts)')
    L.append('@           ptr[4..7] (font_jp_*) 也通过外部代码字面量池直接访问')
    L.append('@ -----------------------------------------------------------------------------')
    L.append('font_jp_base_table:')
    name_w = max(len(n) for n, _ in BASES)
    for i, (name, note) in enumerate(BASES):
        L.append('    .word %-*s    @ [%d] %s' % (name_w, name, i, note))
    L.append('')

    # ---- font_jp_stride_table ----
    L.append('@ -----------------------------------------------------------------------------')
    L.append('@ font_jp_stride_table @ 0x09E5F874 (16 B = 4 × u32)')
    L.append('@ 各字体 per-glyph 字节数 (= 像素维度的平方)')
    L.append('@ -----------------------------------------------------------------------------')
    L.append('font_jp_stride_table:')
    for i, (size, dim) in enumerate(STRIDES):
        L.append('    .word %3d            @ [%d] %s' % (size, i, dim))
    L.append('')

    return '\n'.join(L) + '\n'


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)

    if not os.path.exists(ROM_PATH):
        print('ERROR: %s not found' % ROM_PATH, file=sys.stderr)
        sys.exit(1)

    rom = open(ROM_PATH, 'rb').read()
    verify_against_rom(rom)

    asm = generate_asm()
    with open(ASM_OUT, 'w', encoding='utf-8') as f:
        f.write(asm)
    print('汇编文件: %s  (%d bytes)' % (ASM_OUT, len(asm)))
    print('完成。4 张表 (level_signature 280 B + dim 32 B + base 32 B + stride 16 B = 360 B)')


if __name__ == '__main__':
    main()
