@ 选择 Unified Assembler Syntax（统一汇编语法）
@ unified 语法让 ARM 与 Thumb 指令在同一套语法规则下书写/解析，更通用。
	.syntax unified

@ 宏定义（deck_entry、banlist_entry、deck_card 等）
	.include "include/macros.inc"

@ 把符号 Start 声明为全局可见，这样链接器在链接阶段就能找到它作为程序入口点。
	.global Start

@ 切换到 .text 代码段，所有后续的指令和数据都会放在这个段中，直到遇到下一个段声明。
	.text

@ 接下来按 ARM state（32-bit ARM 指令） 来汇编，而不是 Thumb（16-bit 为主）。
	.arm

Start:
	.include "asm/crt0.s"

	.include "asm/all.s"

@ 后 16MB 第一段：ROM偏移 0x1000000 - 0x1E58D0D（对手卡值前）
	.incbin "roms/2343.gba", 0x1000000, 0xE58D0E

@ 对手卡值块数据（ROM偏移 0x1E58D0E - 0x1E5906D）
@ 27 个对手条目，每条 32 字节，共 0x360 字节
	.include "data/opponent-card-values.s"

@ 后 16MB 中间段：ROM偏移 0x1E5906E - 0x1E5EF2F（对手卡值后，禁卡表前）
	.incbin "roms/2343.gba", 0x1E5906E, 0x5EC2

@ 禁卡表数据（ROM偏移 0x1E5EF30 - 0x1E5F6CB）
@ 包含 8 个版本共 487 条目，共 0x79C 字节
	.include "data/banlists.s"

@ 后 16MB 中间段：ROM偏移 0x1E5F6CC - 0x1E5F883（禁卡表后，初始卡组前）
	.incbin "roms/2343.gba", 0x1E5F6CC, 0x1B8

@ 初始卡组数据（ROM偏移 0x1E5F884 - 0x1E5F8E9）
@ 50 张牌 + 终止符，共 0x66 字节
	.include "data/starter-deck.s"

@ 后 16MB 中间段：ROM偏移 0x1E5F8EA - 0x1E5FA57（初始卡组后，结构卡组前）
	.incbin "roms/2343.gba", 0x1E5F8EA, 0x16E

@ 结构卡组数据（ROM偏移 0x1E5FA58 - 0x1E5FD83）
@ 包含 6 个结构卡组及其指针表，共 0x32C 字节
	.include "data/struct-decks.s"

@ 后 16MB 剩余部分：ROM偏移 0x1E5FD84 - 0x1E6468D（结构卡组后，对手卡组前）
	.incbin "roms/2343.gba", 0x1E5FD84, 0x490A

@ 对手卡组数据（ROM偏移 0x1E6468E - 0x1E65A45）
@ 25 个对手卡组，各含 40 张牌，共 0x13B8 字节
	.include "data/opponent-decks.s"

@ 尾段：ROM偏移 0x1E65A46 - 0x1FFFF00
	.incbin "roms/2343.gba", 0x1E65A46, 0x19A4BA
