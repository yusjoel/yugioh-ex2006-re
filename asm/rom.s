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

@ 后 16MB 第一段：ROM偏移 0x1000000 - 0x1B101AB（图形数据前）
	.incbin "roms/2343.gba", 0x1000000, 0xB101AC

@ 调色板块（Copy 1），ROM 0x1B101AC–0x1B1200B，7776 字节（27 个对手，每对手 288 字节）
@ 注意：Copy 2（0x1B4FE9C–0x1B51CFB）与本块内容完全相同，引用同一文件
	.incbin "graphics/opponents/palette_copy1.bin"

@ Top 图块，ROM 0x1B1200C–0x1B4800B，221184 字节（27 × 0x2000，保留 ROM incbin）
@ 注意：第 20 个对手 Elemental Hero Electrum 图块偏移不规则（0x1B3899C），整段统一保留
	.incbin "roms/2343.gba", 0x1B1200C, 0x36000

@ Top Tilemap（27 个对手），ROM 0x1B4800C–0x1B4FE9B，每个 0x4B0 字节
	.incbin "graphics/opponents/kuriboh_top_tilemap.bin"
	.incbin "graphics/opponents/scapegoat_top_tilemap.bin"
	.incbin "graphics/opponents/skull_servant_top_tilemap.bin"
	.incbin "graphics/opponents/watapon_top_tilemap.bin"
	.incbin "graphics/opponents/pikeru_top_tilemap.bin"
	.incbin "graphics/opponents/batteryman_c_top_tilemap.bin"
	.incbin "graphics/opponents/ojama_yellow_top_tilemap.bin"
	.incbin "graphics/opponents/goblin_king_top_tilemap.bin"
	.incbin "graphics/opponents/des_frog_top_tilemap.bin"
	.incbin "graphics/opponents/water_dragon_top_tilemap.bin"
	.incbin "graphics/opponents/redd_top_tilemap.bin"
	.incbin "graphics/opponents/vampire_genesis_top_tilemap.bin"
	.incbin "graphics/opponents/infernal_flame_emperor_top_tilemap.bin"
	.incbin "graphics/opponents/ocean_dragon_lord_top_tilemap.bin"
	.incbin "graphics/opponents/helios_duo_megiste_top_tilemap.bin"
	.incbin "graphics/opponents/gilford_the_legend_top_tilemap.bin"
	.incbin "graphics/opponents/dark_eradicator_warlock_top_tilemap.bin"
	.incbin "graphics/opponents/guardian_exode_top_tilemap.bin"
	.incbin "graphics/opponents/goldd_top_tilemap.bin"
	.incbin "graphics/opponents/elemental_hero_electrum_top_tilemap.bin"
	.incbin "graphics/opponents/raviel_top_tilemap.bin"
	.incbin "graphics/opponents/horus_top_tilemap.bin"
	.incbin "graphics/opponents/stronghold_top_tilemap.bin"
	.incbin "graphics/opponents/sacred_phoenix_top_tilemap.bin"
	.incbin "graphics/opponents/cyber_end_dragon_top_tilemap.bin"
	.incbin "graphics/opponents/mirror_match_top_tilemap.bin"
	.incbin "graphics/opponents/copycat_top_tilemap.bin"

@ 调色板块（Copy 2），ROM 0x1B4FE9C–0x1B51CFB，7776 字节（内容与 Copy 1 完全相同）
	.incbin "graphics/opponents/palette_copy1.bin"

@ Bottom 图块，ROM 0x1B51CFC–0x1B87CFB，221184 字节（27 × 0x2000，保留 ROM incbin）
	.incbin "roms/2343.gba", 0x1B51CFC, 0x36000

@ Bottom Tilemap（27 个对手），ROM 0x1B87CFC–0x1B8FB8B，每个 0x4B0 字节
	.incbin "graphics/opponents/kuriboh_bottom_tilemap.bin"
	.incbin "graphics/opponents/scapegoat_bottom_tilemap.bin"
	.incbin "graphics/opponents/skull_servant_bottom_tilemap.bin"
	.incbin "graphics/opponents/watapon_bottom_tilemap.bin"
	.incbin "graphics/opponents/pikeru_bottom_tilemap.bin"
	.incbin "graphics/opponents/batteryman_c_bottom_tilemap.bin"
	.incbin "graphics/opponents/ojama_yellow_bottom_tilemap.bin"
	.incbin "graphics/opponents/goblin_king_bottom_tilemap.bin"
	.incbin "graphics/opponents/des_frog_bottom_tilemap.bin"
	.incbin "graphics/opponents/water_dragon_bottom_tilemap.bin"
	.incbin "graphics/opponents/redd_bottom_tilemap.bin"
	.incbin "graphics/opponents/vampire_genesis_bottom_tilemap.bin"
	.incbin "graphics/opponents/infernal_flame_emperor_bottom_tilemap.bin"
	.incbin "graphics/opponents/ocean_dragon_lord_bottom_tilemap.bin"
	.incbin "graphics/opponents/helios_duo_megiste_bottom_tilemap.bin"
	.incbin "graphics/opponents/gilford_the_legend_bottom_tilemap.bin"
	.incbin "graphics/opponents/dark_eradicator_warlock_bottom_tilemap.bin"
	.incbin "graphics/opponents/guardian_exode_bottom_tilemap.bin"
	.incbin "graphics/opponents/goldd_bottom_tilemap.bin"
	.incbin "graphics/opponents/elemental_hero_electrum_bottom_tilemap.bin"
	.incbin "graphics/opponents/raviel_bottom_tilemap.bin"
	.incbin "graphics/opponents/horus_bottom_tilemap.bin"
	.incbin "graphics/opponents/stronghold_bottom_tilemap.bin"
	.incbin "graphics/opponents/sacred_phoenix_bottom_tilemap.bin"
	.incbin "graphics/opponents/cyber_end_dragon_bottom_tilemap.bin"
	.incbin "graphics/opponents/mirror_match_bottom_tilemap.bin"
	.incbin "graphics/opponents/copycat_bottom_tilemap.bin"

@ 后 16MB 第一段剩余部分：ROM 0x1B8FB8C–0x1DBF019
	.incbin "roms/2343.gba", 0x1B8FB8C, 0x2C438E

@ 未知语言（XX）卡组名字符串（ROM偏移 0x1DBF01A - 0x1DC461F）
@ 含自定义编码（可能为日语）的预组/初始卡组名和对手卡组名；具体编码未知，待后续研究
	.include "data/deck-strings.s"

@ 游戏文本字符串表（ROM偏移 0x1DC4620 - 0x1DFF9D1）
@ 含 5 种语言（EN/DE/FR/IT/ES）的完整游戏文本，共 242610 字节
	.include "data/game-strings.s"

@ 后 16MB 中间段：ROM偏移 0x1DFF9D2 - 0x1E58D0D（游戏文本后，对手卡值前）
	.incbin "roms/2343.gba", 0x1DFF9D2, 0x5933C

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

@ 后 16MB 中间段：ROM偏移 0x1E5F8EA - 0x1E5FA57（初始卡组后，预组前）
	.incbin "roms/2343.gba", 0x1E5F8EA, 0x16E

@ 预组数据（ROM偏移 0x1E5FA58 - 0x1E5FD83）
@ 包含 6 个预组及其指针表，共 0x32C 字节
	.include "data/struct-decks.s"

@ 后 16MB 剩余部分：ROM偏移 0x1E5FD84 - 0x1E6468D（预组后，对手卡组前）
	.incbin "roms/2343.gba", 0x1E5FD84, 0x490A

@ 对手卡组数据（ROM偏移 0x1E6468E - 0x1E65A45）
@ 25 个对手卡组，各含 40 张牌，共 0x13B8 字节
	.include "data/opponent-decks.s"

@ 尾段：ROM偏移 0x1E65A46 - 0x1FFFF00
	.incbin "roms/2343.gba", 0x1E65A46, 0x19A4BA
