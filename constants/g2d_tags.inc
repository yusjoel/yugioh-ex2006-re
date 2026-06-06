@ =============================================================================
@ NNS G2D 资源块 FourCC tag 常量 (源 GL/IG2D_Main.c; find_gfx_entry_by_tag 用)
@ 资源链表按 4 字节 tag 线性查找; tag 以内存小端读出为 u32 (字节序即 ASCII 顺序)。
@ 经 ExportRangeToGas.resolve_word_equate 导出符号; GAS 用本表 .equ 解析回值 -> byte-identical。
@ =============================================================================

.equ BGDT_TAG, 0x54444742  @ 'BGDT' BG 数据资源块 (char/tile + 尺寸 + inline blob)
.equ OBJD_TAG, 0x444a424f  @ 'OBJD' OBJ/sprite 数据资源块 (header 比 BGDT 大 4B)
.equ PALT_TAG, 0x544c4150  @ 'PALT' 调色板资源块 (条目 2B/色)
