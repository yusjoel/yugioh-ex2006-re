@ =============================================================================
@ post-banlists 4 张未结构化数据表 (banlist_master_table 之后, starter-deck 之前)
@ ROM偏移: 0x1E5F71C - 0x1E5F883 (共 0x168 = 360 B)
@
@   level_signature_table  @ 0x1E5F71C, 0x118 (14 × 20 B records)
@   font_jp_dim_table      @ 0x1E5F834, 0x20  (4 × {u32, u32})
@   font_jp_base_table     @ 0x1E5F854, 0x20  (8 × u32 ptrs) ⭐ HOT 92 ldrs
@   font_jp_stride_table   @ 0x1E5F874, 0x10  (4 × u32 strides)
@
@ 由 tools/rom-export/export_post_banlists_tables.py 生成
@ =============================================================================

@ -----------------------------------------------------------------------------
@ Level Signature Table (推测: Limited Duel 难度等级数据)
@ GBA地址: 0x09E5F71C  ROM偏移: 0x1E5F71C
@ 14 条 × 20 字节 = 0x118 = 280 字节
@ 结构 {u16 signal_so_code, char field_a[8], char field_b[8], u16 pad}
@ 渲染器 (FUN_0801D810 area) 逐字节解码 ASCII:
@   0x3F ('?') → glyph 14, 0x58 ('X') → glyph 15, 0x30..0x39 ('0'..'9') → 数字
@ caller: base @ 0x080EF474, rec[0].field_a @ 0x0801D8A0, rec[0].field_b @ 0x0801D8FC
@ -----------------------------------------------------------------------------
level_signature_table:
    .incbin "roms/2343.gba", 0x1E5F71C, 0x2   @ rec[0].so_code field (u16, 2B)
level_signature_table_field_a:                 @ 0x09E5F71E: rec[0].field_a base (char[8], stride=20B per rec)
    .incbin "roms/2343.gba", 0x1E5F71E, 0x8   @ rec[0].field_a (8B)
level_signature_table_field_b:                 @ 0x09E5F726: rec[0].field_b base (char[8], stride=20B per rec)
    .incbin "roms/2343.gba", 0x1E5F726, 0x10e @ remainder: 0x118 - 0x2 - 0x8 = 0x10e (field_b + rest of table)

@ -----------------------------------------------------------------------------
@ font_jp_dim_table @ 0x09E5F834 (32 B = 4 × {u32, u32})
@ 4 个字体的维度配对 (含义未完全确认; 与 base_table[0..3] 对齐)
@ -----------------------------------------------------------------------------
font_jp_dim_table:
    .word 10, 12         @ pair[0]
    .word  5,  6         @ pair[1]
    .word 10, 12         @ pair[2]
    .word 10, 12         @ pair[3]

@ -----------------------------------------------------------------------------
@ font_jp_base_table @ 0x09E5F854 (32 B = 8 × u32) ⭐ HOT 92 ldrs
@ 访问模式: state_bits → offset {0,4,8,12} → ptr[0..3] (alt fallback fonts)
@           ptr[4..7] (font_jp_*) 也通过外部代码字面量池直接访问
@ -----------------------------------------------------------------------------
font_jp_base_table:
    .word 0x09BA3340               @ [0] alt[0] (in 字库前段 gap)
    .word 0x09C20374               @ [1] alt[1] (in font-jp gap1)
    .word 0x09CCB490               @ [2] alt[2] (tail gap start)
    .word 0x09CCBE90               @ [3] alt[3] (within tail gap)
    .word font_jp_main_small       @ [4] 10×10 / 100 B/glyph
    .word font_jp_main_large       @ [5] 12×12 / 144 B/glyph
    .word font_jp_outline_small    @ [6] 12×12 / 144 B/glyph
    .word font_jp_outline_large    @ [7] 14×14 / 196 B/glyph

@ -----------------------------------------------------------------------------
@ font_jp_stride_table @ 0x09E5F874 (16 B = 4 × u32)
@ 各字体 per-glyph 字节数 (= 像素维度的平方)
@ -----------------------------------------------------------------------------
font_jp_stride_table:
    .word 100            @ [0] 10×10
    .word 144            @ [1] 12×12
    .word 144            @ [2] 12×12
    .word 196            @ [3] 14×14

