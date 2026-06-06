@ =============================================================================
@ GBA 内存区基址常量 (硬件固定地址, 非 MMIO 寄存器)
@ 字面量池里的区基址常量经 ExportRangeToGas.resolve_word_equate 导出为符号;
@ GAS 用本表 .equ 解析回同值 -> byte-identical。
@ 仅被引用 (data-equate) 的常量才会出现在导出 .word; 其余为参考文档。
@ =============================================================================

.equ EWRAM_BASE,          0x02000000  @ External Work RAM base (256KB, 0x02000000..0x0203FFFF)
                                      @ 4295 ROM refs; used in base+offset form for gSettings etc.
.equ GBA_PALRAM_BASE,     0x05000000  @ 调色板 RAM (BG+OBJ, 各 0x200 字节)
.equ OBJ_PALRAM_BASE,     0x05000200  @ OBJ/sprite 调色板 RAM (PALRAM+0x200, 16 调色板 ×16 色)
.equ GBA_VRAM_BASE,       0x06000000  @ VRAM 基址 (BG char/screen map; 0xc0<<0x13 内联值)
.equ OBJ_TILE_VRAM_BASE,  0x06010000  @ OBJ/sprite tile 数据基址 (mode 0-2, VRAM+0x10000)
.equ GBA_OAM_BASE,        0x07000000  @ OAM (sprite 属性, 0x400 字节)
.equ BG_CHAR_VRAM_CB2,    0x06004000  @ BG charblock 2 base (GBA_VRAM_BASE + 0x4000); 43 ROM refs; BG char data start for card image tile writes
.equ BG_VRAM_TEXT_BASE,   0x06000020  @ BG text VRAM base+0x20 (tile slot 1); used by font/text render init
