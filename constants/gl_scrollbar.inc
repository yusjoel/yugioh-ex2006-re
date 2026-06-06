@ =============================================================================
@ GL_Scrollbar (源 GL/GL_Scrollbar.c) 字段位掩码 / cpu_set 控制字常量
@ 用于 0x08015384..0x080155f4 的 scrollbar 函数簇 (init/get/set/advance/retreat/update)。
@ GL_Scrollbar* 由 r0 传入 (非全局); 结构字段布局见各函数 plate。
@ 经 ExportRangeToGas.resolve_word_equate 导出符号; GAS 用本表 .equ 解析回同值 -> byte-identical。
@
@ 命名: SCROLLBAR_CLEAR_BITS_<hi>_<lo> = AND 掩码清 bits[hi:lo]; KEEP_BITS = 仅保留。
@ =============================================================================

.equ SCROLLBAR_INIT_FILL_CTRL,  0x05000004  @ init_scrollbar_oam_entry: bios_cpu_set fill 4 字 (清前 16 字节)
.equ SCROLLBAR_KEEP_BITS_8_0,   0x000001ff  @ 9-bit 字段掩码 (保留 bits[8:0])
.equ SCROLLBAR_CLEAR_BITS_14_6, 0xffff803f  @ 清 [pThis+0]w bits[14:6]  (range_param 9-bit 字段)
.equ SCROLLBAR_CLEAR_BITS_23_15,0xff007fff  @ 清 [pThis+0]w bits[23:15] (Y base 9-bit 字段)
.equ SCROLLBAR_CLEAR_BITS_17_9, 0xfffc01ff  @ 清 [pThis+0xc]w bits[17:9] (thumb pos 9-bit 字段)
