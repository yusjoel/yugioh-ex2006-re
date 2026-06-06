@ =============================================================================
@ GL 主状态结构 gGlState (0x02023490) 簇的 bios_cpu_set 控制字常量
@ 用于 0x0801510c..0x0801522c 的 GL palette/OAM 函数簇。
@ 控制字格式: bit24=1 fill(定源) / bit26=1 32-bit(字) 否则 16-bit(半字) / bits[20:0]=单位数。
@ 经 ExportRangeToGas.resolve_word_equate 导出符号; GAS 用本表 .equ 解析回同值 -> byte-identical。
@ =============================================================================

.equ GL_STATE_INIT_FILL_CTRL,  0x0500022b  @ gl_state_init: fill 0x22b 字 (=0x8ac 字节, 全结构清 0)
.equ GL_PALRAM_FILL_CTRL,      0x05000100  @ fill_gl_palram_buf_0xf0: fill 0x100 字 (=0x400 字节)
.equ GL_PALENTRY_ZERO_CTRL,    0x05000002  @ alloc_palette_entry_slot: fill 2 字 (=8 字节, 清 1 个 entry)
