@ 选择 Unified Assembler Syntax（统一汇编语法）
@ unified 语法让 ARM 与 Thumb 指令在同一套语法规则下书写/解析，更通用。
	.syntax unified

@ 把符号 Start 声明为全局可见，这样链接器在链接阶段就能找到它作为程序入口点。
	.global Start

@ 切换到 .text 代码段，所有后续的指令和数据都会放在这个段中，直到遇到下一个段声明。
	.text

@ 接下来按 ARM state（32-bit ARM 指令） 来汇编，而不是 Thumb（16-bit 为主）。
	.arm

Start:
	.include "asm/crt0.s"

	.include "asm/all.s"

@ 后 16MB（GBA 地址 09000000-09FFFFFF），暂未反汇编，直接 incbin
	.incbin "roms/2343.gba", 0x1000000, 0x1000000
