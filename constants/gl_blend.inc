@ =============================================================================
@ GL 亮度/混合 (fade/blend) 状态结构 gGlBlendState (0x02023480) 相关常量
@ 用于 0x08014600..0x08014a10 的 GL blend/brightness 函数簇 (gl_set_brightness /
@ gl_set_blend2_level / init_blend_transition_params(_ex) / check/tick_blend_transition_step /
@ reset_gl_blend_transition_state / gl_clear_vram_palram_scroll)。
@ 字面量池里的位掩码/控制字常量, 经 ExportRangeToGas.resolve_word_equate 导出为符号;
@ GAS 用本表 .equ 解析回同值 -> byte-identical。
@
@ 命名: GL_CLEAR_BITS_<hi>_<lo> = AND 掩码, 清 [gGlBlendState+8] 打包字的 bits[hi:lo]。
@ =============================================================================

@ gGlBlendState+0x8 打包控制字清位 AND 掩码
.equ GL_CLEAR_BITS_9_2,    0xfffffc03  @ 清 bits[9:2]   (blend1 step, ~0x000003fc)
.equ GL_CLEAR_BITS_17_10,  0xfffc03ff  @ 清 bits[17:10] (blend2 step, ~0x0003fc00)

@ gl_clear_vram_palram_scroll 的 bios_cpu_fast_set 控制字 (bit24=1 fill, 字数低 24 位)
.equ GL_CLEAR_VRAM_FILL_CTRL,   0x01006000  @ fill 0x6000 字 (=0x18000 字节, 全 VRAM)
.equ GL_CLEAR_PALRAM_FILL_CTRL, 0x01000100  @ fill 0x100 字 (=0x400 字节, 全 PALRAM)
