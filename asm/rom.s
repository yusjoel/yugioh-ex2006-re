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

@ ── 大卡图数据段（原在 all.s 末尾，移出以保持 all.s 纯代码）───────────────
@ ROM 偏移 0x4C7638 - 0x1000000，共约 11.5 MB
	.incbin "roms/2343.gba", 0x4C7638, 0x88         @ 0x4C7638..0x4C76C0 未知小段
	.include "data/card-image-palettes.s"           @ 0x4C76C0..0x510440  2331 × 128 B 卡图调色板
	.incbin "roms/2343.gba", 0x510440, 0x200        @ 0x510440..0x510640 填充/未用
	.include "data/card-image-tiles.s"              @ 0x510640..0xFBC080  2331 × 4800 B 6bpp tile 数据
	.incbin "roms/2343.gba", 0xFBC080, 0x43F80      @ 0xFBC080..0x1000000 tile 区后剩余

@ 后 16MB 第一段前半 seg-A-1：ROM偏移 0x1000000 - 0x15B5BFF（卡图索引表前）
	.incbin "roms/2343.gba", 0x1000000, 0x5B5C00

@ 卡牌大图索引表（ROM偏移 0x15B5C00 - 0x15B94CB）
@ 7270 × u16 = 14540 B = 0x38CC
@ 引用 graphics/card-images-rom/palettes.bin + tiles.bin（由同脚本从 ROM 导出，未入库）
	.include "data/card-image-index.s"

@ 后 16MB 第一段前半 seg-A-2：ROM偏移 0x15B94CC - 0x15BB5AB（索引表后至卡名表前）
	.incbin "roms/2343.gba", 0x15B94CC, 0x20E0

@ 卡牌名称字符串表（ROM偏移 0x15BB5AC - 0x15F3A5B）
@ 2053 张卡 × 6 种语言（EN/DE/FR/IT/ES/XX），CP1252 编码，2 字节对齐
	.include "data/card-names.s"

@ 后 16MB 第一段前半 seg-B：ROM偏移 0x15F3A5C - 0x18169B5（卡名后，属性表前）
	.incbin "roms/2343.gba", 0x15F3A5C, 0x222F5A

@ 卡牌属性数据表（ROM偏移 0x18169B6 - 0x18325FF）
@ 5170 条记录，每条 22 字节（11 × uint16 LE），含 ATK/DEF/Level/属性/种族等
	.include "data/card-stats.s"

@ 后 16MB 第一段前半 seg-C：ROM偏移 0x1832602 - 0x185504B（属性表后，外场图块前）
@ 含外场图块指针表（0x1855030，7条目28字节），紧接着就是外场图块数据
@ 内嵌 HUD 元素（Life Points Font / Phase Highlights Palette / Phases Highlight）已拆出
	.incbin "roms/2343.gba", 0x1832602, 0x1E51A     @ seg-C 前段 0x1832602..0x1850B1C
	.incbin "graphics/duel-field/hud_life_points_font.bin"          @ 0x1850B1C, 0xAC0
	.incbin "graphics/duel-field/hud_phase_highlights_palette.bin"  @ 0x18515DC, 0x20
	.incbin "roms/2343.gba", 0x18515FC, 0x400       @ 未知 gap（0x18515FC..0x18519FC）
	.incbin "graphics/duel-field/hud_phases_highlight.bin"          @ 0x18519FC, 0x3650（至 0x185504C）

@ ── 外场图块数据（6种决斗模式，大小各异）──────────────────────────────
@ 指针表在 0x1855030（7条目，末条目为终止指针指向 0x185878C），数据从 0x185504C 开始
@ Campaign（战役）外场图块，ROM 0x185504C，0x9E0 字节（80 图块）
	.incbin "graphics/duel-field/campaign_outer_image.bin"
@ Link Duel（联机）外场图块，ROM 0x1855A2C，0x5E0 字节（47 图块）
	.incbin "graphics/duel-field/link_outer_image.bin"
@ Duel Puzzle（谜题）外场图块，ROM 0x185600C，0x7E0 字节（63 图块）
	.incbin "graphics/duel-field/puzzle_outer_image.bin"
@ Limited Duel（限定）外场图块，ROM 0x18567EC，0xDE0 字节（111 图块）
	.incbin "graphics/duel-field/limited_outer_image.bin"
@ Theme Duel（主题）外场图块，ROM 0x18575CC，0x9E0 字节（80 图块）
	.incbin "graphics/duel-field/theme_outer_image.bin"
@ Survival Mode（生存）外场图块，ROM 0x1857FAC，0x7E0 字节（63 图块）
	.incbin "graphics/duel-field/survival_outer_image.bin"

@ 未知图块数据 + 外场调色板指针表（7条目28字节，位于 0x185936C）
@ ROM 0x185878C - 0x185938B，0xBFC 字节
	.incbin "roms/2343.gba", 0x185878C, 0xBFC

@ ── 外场调色板（6种模式，每个 0x40 字节 = 2个子调色板）────────────────
@ 指针表在 0x185936C（7条目），数据从 0x1859388 开始
@ 调色板槽位 9–10 加载进 BG 调色板 RAM；Tilemap 条目主要引用槽位 9
	.incbin "graphics/duel-field/campaign_outer_palette.bin"
	.incbin "graphics/duel-field/link_outer_palette.bin"
	.incbin "graphics/duel-field/puzzle_outer_palette.bin"
	.incbin "graphics/duel-field/limited_outer_palette.bin"
	.incbin "graphics/duel-field/theme_outer_palette.bin"
	.incbin "graphics/duel-field/survival_outer_palette.bin"

@ 未知数据 + LP/阶段 Tilemap 指针表（7条目28字节，位于 0x1859548）
@ ROM 0x1859508 - 0x1859563，0x5C 字节；指针表拆为 HUD bin
	.incbin "roms/2343.gba", 0x1859508, 0x40        @ 未知前段 0x1859508..0x1859548
	.incbin "graphics/duel-field/hud_phases_tilemap_pointers.bin"   @ 0x1859548, 0x1C

@ ── LP/阶段显示区 Tilemap（6种模式，每个 0x4B0 字节 = 30×20 图块）──────
@ 指针表在 0x1859548（7条目），数据从 0x1859564 开始
@ 与外场 Tilemap 共用同一套外场图块数据和调色板
	.incbin "graphics/duel-field/campaign_outer_lp_tilemap.bin"
	.incbin "graphics/duel-field/link_outer_lp_tilemap.bin"
	.incbin "graphics/duel-field/puzzle_outer_lp_tilemap.bin"
	.incbin "graphics/duel-field/limited_outer_lp_tilemap.bin"
	.incbin "graphics/duel-field/theme_outer_lp_tilemap.bin"
	.incbin "graphics/duel-field/survival_outer_lp_tilemap.bin"

@ "Phases Map?" 图块 + 外场 Tilemap 指针表（7条目28字节，位于 0x185B634）
@ ROM 0x185B184 - 0x185B64F，0x4CC 字节；Phases Map 数据拆为 HUD bin
	.incbin "graphics/duel-field/hud_phases_map.bin"                @ 0x185B184, 0x4B0
	.incbin "roms/2343.gba", 0x185B634, 0x1C        @ 外场 Tilemap 指针表（7条目28字节）

@ ── 外场 Tilemap（6种模式，每个 0x4B0 字节 = 30×20 图块）──────────────
@ 指针表在 0x185B634（7条目），数据从 0x185B650 开始
	.incbin "graphics/duel-field/campaign_outer_tilemap.bin"
	.incbin "graphics/duel-field/link_outer_tilemap.bin"
	.incbin "graphics/duel-field/puzzle_outer_tilemap.bin"
	.incbin "graphics/duel-field/limited_outer_tilemap.bin"
	.incbin "graphics/duel-field/theme_outer_tilemap.bin"
	.incbin "graphics/duel-field/survival_outer_tilemap.bin"

@ 内场公共 Tilemap（所有模式共享，0x4B0 字节 = 30×20 图块）
@ ROM 0x185D270 - 0x185D71F
	.incbin "roms/2343.gba", 0x185D270, 0x4B0

@ ── 内场图块数据（6种模式，每个 0x1680 字节 = 180 图块）────────────────
@ 数据从 0x185D720 开始（紧接内场公共 Tilemap 后），6 × 0x1680 = 0x8D00 字节
	.incbin "graphics/duel-field/campaign_inner_image.bin"
	.incbin "graphics/duel-field/link_inner_image.bin"
	.incbin "graphics/duel-field/puzzle_inner_image.bin"
	.incbin "graphics/duel-field/limited_inner_image.bin"
	.incbin "graphics/duel-field/theme_inner_image.bin"
	.incbin "graphics/duel-field/survival_inner_image.bin"

@ 未知第7内场图块数据，ROM 0x1865E20 - 0x186749F，0x1680 字节
	.incbin "roms/2343.gba", 0x1865E20, 0x1680

@ ── 内场调色板（6种模式，每个 0x20 字节 = 1个子调色板）────────────────
@ 数据从 0x18674A0 开始，调色板加载到 BG 调色板槽位 9
	.incbin "graphics/duel-field/campaign_inner_palette.bin"
	.incbin "graphics/duel-field/link_inner_palette.bin"
	.incbin "graphics/duel-field/puzzle_inner_palette.bin"
	.incbin "graphics/duel-field/limited_inner_palette.bin"
	.incbin "graphics/duel-field/theme_inner_palette.bin"
	.incbin "graphics/duel-field/survival_inner_palette.bin"

@ 后 16MB 第一段剩余：ROM 0x1867560 - 0x188DA6F（内场调色板后，小图标图块前）
	.incbin "roms/2343.gba", 0x1867560, 0x26510

@ ── 小图标图块（27 个对手，每个 9 图块 × 32 字节 = 0x120 字节）────────────────
@ ROM 0x188DA70 - 0x188F8CF，共 0x1E60 字节
	.incbin "graphics/icons/kuriboh_icon_tiles.bin"
	.incbin "graphics/icons/scapegoat_icon_tiles.bin"
	.incbin "graphics/icons/skull_servant_icon_tiles.bin"
	.incbin "graphics/icons/watapon_icon_tiles.bin"
	.incbin "graphics/icons/pikeru_icon_tiles.bin"
	.incbin "graphics/icons/batteryman_c_icon_tiles.bin"
	.incbin "graphics/icons/ojama_yellow_icon_tiles.bin"
	.incbin "graphics/icons/goblin_king_icon_tiles.bin"
	.incbin "graphics/icons/des_frog_icon_tiles.bin"
	.incbin "graphics/icons/water_dragon_icon_tiles.bin"
	.incbin "graphics/icons/redd_icon_tiles.bin"
	.incbin "graphics/icons/vampire_genesis_icon_tiles.bin"
	.incbin "graphics/icons/infernal_flame_emperor_icon_tiles.bin"
	.incbin "graphics/icons/ocean_dragon_lord_icon_tiles.bin"
	.incbin "graphics/icons/helios_duo_megiste_icon_tiles.bin"
	.incbin "graphics/icons/gilford_the_legend_icon_tiles.bin"
	.incbin "graphics/icons/dark_eradicator_warlock_icon_tiles.bin"
	.incbin "graphics/icons/guardian_exode_icon_tiles.bin"
	.incbin "graphics/icons/goldd_icon_tiles.bin"
	.incbin "graphics/icons/elemental_hero_electrum_icon_tiles.bin"
	.incbin "graphics/icons/raviel_icon_tiles.bin"
	.incbin "graphics/icons/horus_icon_tiles.bin"
	.incbin "graphics/icons/stronghold_icon_tiles.bin"
	.incbin "graphics/icons/sacred_phoenix_icon_tiles.bin"
	.incbin "graphics/icons/cyber_end_dragon_icon_tiles.bin"
	.incbin "graphics/icons/mirror_match_icon_tiles.bin"
	.incbin "graphics/icons/copycat_icon_tiles.bin"

@ 未知数据：ROM 0x188F8D0 - 0x18963CF，0x6B00 字节
	.incbin "roms/2343.gba", 0x188F8D0, 0x6B00

@ ── 小图标调色板（27 个对手，每个 0x20 字节 = 1 子调色板）────────────────────
@ ROM 0x18963D0 - 0x189672F，共 0x360 字节
	.incbin "graphics/icons/kuriboh_icon_palette.bin"
	.incbin "graphics/icons/scapegoat_icon_palette.bin"
	.incbin "graphics/icons/skull_servant_icon_palette.bin"
	.incbin "graphics/icons/watapon_icon_palette.bin"
	.incbin "graphics/icons/pikeru_icon_palette.bin"
	.incbin "graphics/icons/batteryman_c_icon_palette.bin"
	.incbin "graphics/icons/ojama_yellow_icon_palette.bin"
	.incbin "graphics/icons/goblin_king_icon_palette.bin"
	.incbin "graphics/icons/des_frog_icon_palette.bin"
	.incbin "graphics/icons/water_dragon_icon_palette.bin"
	.incbin "graphics/icons/redd_icon_palette.bin"
	.incbin "graphics/icons/vampire_genesis_icon_palette.bin"
	.incbin "graphics/icons/infernal_flame_emperor_icon_palette.bin"
	.incbin "graphics/icons/ocean_dragon_lord_icon_palette.bin"
	.incbin "graphics/icons/helios_duo_megiste_icon_palette.bin"
	.incbin "graphics/icons/gilford_the_legend_icon_palette.bin"
	.incbin "graphics/icons/dark_eradicator_warlock_icon_palette.bin"
	.incbin "graphics/icons/guardian_exode_icon_palette.bin"
	.incbin "graphics/icons/goldd_icon_palette.bin"
	.incbin "graphics/icons/elemental_hero_electrum_icon_palette.bin"
	.incbin "graphics/icons/raviel_icon_palette.bin"
	.incbin "graphics/icons/horus_icon_palette.bin"
	.incbin "graphics/icons/stronghold_icon_palette.bin"
	.incbin "graphics/icons/sacred_phoenix_icon_palette.bin"
	.incbin "graphics/icons/cyber_end_dragon_icon_palette.bin"
	.incbin "graphics/icons/mirror_match_icon_palette.bin"
	.incbin "graphics/icons/copycat_icon_palette.bin"

@ ROM 0x1896730 - 0x1B101AB
	.incbin "roms/2343.gba", 0x1896730, 0x279A7C

@ 调色板块（Copy 1），ROM 0x1B101AC–0x1B1200B，7776 字节（27 个对手，每对手 288 字节）
@ 注意：Copy 2（0x1B4FE9C–0x1B51CFB）与本块内容完全相同，引用同一文件
	.incbin "graphics/opponents/palette_copy1.bin"

@ Top 图块整块，ROM 0x1B1200C–0x1B4800B，221184 字节（27 × 0x2000）
@ 注意：第 20 个对手 Elemental Hero Electrum 图块偏移不规则（0x1B3899C），整段统一保留
	.incbin "graphics/opponents/top_tiles_all.bin"

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

@ Bottom 图块整块，ROM 0x1B51CFC–0x1B87CFB，221184 字节（27 × 0x2000）
	.incbin "graphics/opponents/bottom_tiles_all.bin"

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

@ 后 16MB 第一段剩余部分：ROM 0x1B8FB8C–0x1DBF019（内嵌英文字库已拆出）
	.incbin "roms/2343.gba", 0x1B8FB8C, 0x13CF04   @ 0x1B8FB8C..0x1CCCA90 字库前段

@ 英文字库（1bpp 8×8，256 字符，ASCII 直接索引），ROM 0x1CCCA90–0x1CCD28F，2048 B
@ 加载函数 FUN_080f1b60 @ 0x080f1b60；详见 doc/dev/p2-font-location-findings.md
	.include "data/font.s"

	.incbin "roms/2343.gba", 0x1CCD290, 0x16D0      @ 0x1CCD290..0x1CCE960 字库后段前部

@ 卡包封面条幅图 (ROM 0x1CCE960..0x1CE822C, 0x198CC bytes)
@ 指针表 (.word label) + 51 × 0x800 bytes 8bpp OBJ tile data
	.include "data/pack-banners.s"

	.incbin "roms/2343.gba", 0x1CE822C, 0xD6DEE     @ 0x1CE822C..0x1DBF01A 字库后段后部

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

@ 尾段：ROM偏移 0x1E65A46 - 0x2000000
	.incbin "roms/2343.gba", 0x1E65A46, 0x19A5BA
