@ =============================================================================
@ demo scene (Exodia 开场动画) 状态结构 gDemoState 相关常量
@ 用于 0x08013510..0x08014398 的 demo 场景函数簇 (reset_display / setup_demo_* /
@ load_demo_* / tick_demo_* / apply_demo_* / tick_demo_scene_state_machine)。
@ 字面量池里的位掩码/初值常量, 经 ExportRangeToGas.resolve_word_equate 导出为符号;
@ GAS 用本表 .equ 解析回同值 -> byte-identical。
@
@ 命名: DEMO_CLEAR_BITS_<hi>_<lo> = AND 掩码, 清 bits[hi:lo] (该范围位置 0, 其余置 1)。
@       DEMO_KEEP_BITS_<hi>_<lo>  = AND 掩码, 仅保留 bits[hi:lo]。
@ =============================================================================

@ -----------------------------------------------------------------------------
@ gDemoState 打包字段清位 AND 掩码 (各函数据字段偏移在不同 gDemoState 偏移上复用同值)
@ -----------------------------------------------------------------------------
.equ DEMO_CLEAR_BITS_8_1,   0xfffffe01  @ 清 bits[8:1]   (~0x000001fe)
.equ DEMO_CLEAR_BITS_12_8,  0xffffe0ff  @ 清 bits[12:8]  (~0x00001f00)
.equ DEMO_CLEAR_BITS_13_7,  0xffffc07f  @ 清 bits[13:7]  (~0x00003f80)
.equ DEMO_CLEAR_BITS_14_13, 0xffff9fff  @ 清 bits[14:13] (~0x00006000)
.equ DEMO_CLEAR_BITS_15_14, 0xffff3fff  @ 清 bits[15:14] (~0x0000c000)
.equ DEMO_CLEAR_BITS_16_9,  0xfffe01ff  @ 清 bits[16:9]  (~0x0001fe00)
.equ DEMO_KEEP_BITS_8_0,    0x000001ff  @ 仅保留 bits[8:0]

@ -----------------------------------------------------------------------------
@ demo 显示重置 / 资源初值常量
@ -----------------------------------------------------------------------------
@ reset_display_and_gl_state 用 bios_cpu_set 清 gDemoState 的控制字:
@ 0x25=37 字 (=0x94 字节), bit24=fill(定源), bit26=32-bit
.equ DEMO_CPUSET_FILL_CTRL,  0x05000025
@ reset_display_and_gl_state 写 BGnCNT 的初值 (BG0CNT=0x1d00 为内联 0xe8<<5, 无池槽)
.equ DEMO_BG1CNT_INIT,       0x00001e01
.equ DEMO_BG2CNT_INIT,       0x00001f02
.equ DEMO_BG3CNT_INIT,       0x00009b0b
@ load_demo_bg_gfx_set1 第三个 apply 的扩展资源描述符 (内联打包值)
.equ DEMO_EXTRA_RESOURCE_DESC, 0x141e0000

@ 注: FS 资源区指针 (0x09e396b8 等资源描述符/路径/断言串) 已结构化为 data/demo-exodia-resources.s,
@ 代码侧 .word 直接引用其 GAS label (demo_sprite_resource_desc / demo_path_exodia* 等),
@ 经 resolve_word_symbol 导出; 不再用 data-equate 常量 (单一命名源)。
