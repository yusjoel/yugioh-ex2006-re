@ 选择 Unified Assembler Syntax（统一汇编语法）
@ unified 语法让 ARM 与 Thumb 指令在同一套语法规则下书写/解析，更通用。
	.syntax unified

@ 宏定义（deck_entry、banlist_entry、deck_card 等）
	.include "include/macros.inc"

@ 常量符号（EWRAM/IWRAM 变量地址，依据 Data Crystal RAM map）
	.include "constants/ewram.inc"
	.include "constants/iwram.inc"

@ GBA MMIO 寄存器（依据 refs/gba-ghidra-loader mapIO()）
	.include "constants/gba_io.inc"

@ GBA 内存区基址常量（VRAM/OBJ tile/PALRAM/OAM；BG VRAM 簇 OBJ_TILE_VRAM_BASE 用）
	.include "constants/gba_mem.inc"

@ GBA 中断 IRQ flag/掩码常量（IntrMain 优先级扫描/嵌套掩码用）
	.include "constants/gba_intr.inc"

@ demo scene (gDemoState) 字段掩码/初值常量（0x13510..0x14398 demo 场景簇用）
	.include "constants/demo_state.inc"

@ GL blend/brightness (gGlBlendState) 位掩码/控制字常量（0x14600..0x14a10 GL 簇用）
	.include "constants/gl_blend.inc"

@ GL 主状态 (gGlState) palette/OAM 簇 cpu_set 控制字（0x1510c..0x1522c GL 簇用）
	.include "constants/gl_state.inc"

@ GL_Scrollbar 字段位掩码/控制字（0x15384..0x155f4 scrollbar 簇用）
	.include "constants/gl_scrollbar.inc"

@ NNS G2D 资源块 FourCC tag（0x16140 find_gfx_entry_by_tag 簇用）
	.include "constants/g2d_tags.inc"

@ 硬件 OAM 项字段位掩码（0x15954 cell-anim OAM 构建簇用）
	.include "constants/oam_attr.inc"

@ ROM 区域/语言检测（0x080000ae game-code + gSettings language_id）
	.include "constants/rom_region.inc"

@ GFX 资源 BGDT/OBJD → state struct attr 字段位掩码（0x165bc apply_bgdt 簇用）
	.include "constants/gfx_resource.inc"

@ 名字输入 / banlist 页面常量（BG CNT init / cpuset 控制字 / gSettings offset; 0x171ec 簇用）
	.include "constants/name_input.inc"

@ Card Info Page BG CNT init / OBJ pal slot / BG-VRAM 写入基址（0x1d448 card_info 簇用）
	.include "constants/card_info.inc"

@ Duel Field display constants (init_duel_field_icon_and_bg_vram / render_win_count; f01 Seg-7 0x20fa8 cluster)
	.include "constants/duel_field.inc"

@ ARM CPSR/SPSR 处理器状态位（crt0/IntrMain 模式切换用）
	.include "constants/arm_psr.inc"

@ ROM 数据段 symbol（由 tools/ghidra-labeling/ExportRomLabelsToInc.py 从 Ghidra 导出）
	.include "constants/rom_data.inc"

@ 把符号 Start 声明为全局可见，这样链接器在链接阶段就能找到它作为程序入口点。
	.global Start

@ 切换到 .text 代码段，所有后续的指令和数据都会放在这个段中，直到遇到下一个段声明。
	.text

@ 接下来按 ARM state（32-bit ARM 指令） 来汇编，而不是 Thumb（16-bit 为主）。
	.arm

Start:
	.include "asm/crt0.s"

	.include "asm/includes.inc"

@ ── 大卡图数据段（原在 all.s 末尾，移出以保持 all.s 纯代码）───────────────
@ ROM 偏移 0x4C7638 - 0x1000000，共约 11.5 MB
	.incbin "roms/2343.gba", 0x4C7638, 0x88         @ 0x4C7638..0x4C76C0 未知小段
	.include "data/card-image-palettes.s"           @ 0x4C76C0..0x510440  2331 × 128 B 卡图调色板
pack_banner_obj_palette:
	.incbin "graphics/bin/pack-banners/palettes/pack_banner_palette.bin"  @ 0x510440..0x510640 pack banner OBJ 调色板 (256色, 512B)
	.include "data/card-image-tiles.s"              @ 0x510640..0xFBC080  2331 × 4800 B 6bpp tile 数据

@ card-medium-frame tile 数据（ROM偏移 0x0FBC080 - 0x1326280）
@ 2331 tile_block × 1536 B = 0x36A200；32×48 8bpp 带框卡 sprite
@ 加载函数 FUN_080c2d24；与 card-mini-frame 共享索引表 0x095B5C00
	.include "data/card-medium-frame.s"

@ card-mini-frame tile 数据（ROM偏移 0x1326280 - 0x15B5BFF）
@ 2331 tile_block × 1152 B = 0x28F980，末尾紧接 card-image-index.s
	.include "data/card-mini-frame.s"

@ 卡牌大图索引表（ROM偏移 0x15B5C00 - 0x15B7CCB）
@ 2099 cards × 2 × u16 = 8396 B = 0x20CC（card_id 0..2098）
	.include "data/card-image-index.s"

@ Cards IDs Array（ROM偏移 0x15B7CCC - 0x15B94CB）
@ 3072 × u16 = 6144 B = 0x1800（internal_card_id 4007..7078 → card_id）
@ Data Crystal ROM map function 0x080EE76C 验证
	.include "data/cards-ids-array.s"

@ 卡牌密码表（加密）（ROM偏移 0x15B94CC - 0x15BB593）
@ 2098 × u32 = 8,392 B；table[cid] XOR key(cid) = passcode_bcd
@   key(cid) = ((cid * 0x343FD + 0x269EC3) >> 16) | 0x9EC30000  （Borland rand LCG）
@ 解密器 FUN_080ef370 / 逆查 FUN_080ef38c
	.include "data/card-passcodes.s"

@ 卡牌名称统一区（ROM 偏移 0x15BB594 - 0x15FFF0B，共 280,952 字节）
@ 合并 card-names + card-name-pointer-table:
@   1. card_names_table        0x15BB594 - 0x15F3A5B (230,600 B)
@      2054 master 条目 × 6 langs (XX/EN/DE/FR/IT/ES)，CP1252，2B 对齐；alt-art 共享 master
@   2. card_name_pointer_table 0x15F3A5C - 0x15FFF0B (50,352 B = 2098 × 6 × u32)
@      Lookup: name_addr = card_names_table + ptr[card_id*6 + lang_id]（Data Crystal 0x080EE968）
@ 末 u32 指向 card-descriptions 文本池起点
	.include "data/card-names.s"

@ 卡牌描述统一区（ROM偏移 0x15FFF0C - 0x18169B8，共 2,190,508 字节）
@ 合并 card-effect-text + card-descriptions: text pool (2098 卡 × 6 langs null-terminated)
@ + card_desc_data (cid=0..2052 × 6 u32) + card_desc_ptr_table (cid=2053..2097 × 6 u32)
@ 末 u32 (cid=2097 ES offset) 高 2 B 与 card_stats[0].zero0 字节重叠
	.include "data/card-descriptions.s"

@ 卡牌属性数据表（ROM偏移 0x18169B8 - 0x18325FF）
@ 5170 条记录 (首条 20 B 少 zero0 字段由上游 Section C 提供; 其余 5169 条 × 22 B)
	.include "data/card-stats.s"

@ 后 16MB 第一段前半 seg-C：ROM偏移 0x1832602 - 0x1850B1B（属性表后，HUD 前）
@ 内嵌 HUD 元素 + 外场 tile image 指针表已拆出
	.incbin "roms/2343.gba", 0x1832602, 0x1CF4A     @ seg-C pre-segment (to card_digit_glyph_data @ 0x0984f54c)
card_digit_glyph_data:                               @ 0x0984f54c (0x50 B, 6 ROM refs; 10 decimal digit bitmaps, 8B/glyph, 7px wide)
	.incbin "roms/2343.gba", 0x184F54C, 0x50         @ 10 digits x 8B/glyph
card_label_glyph_buf:                                @ 0x0984f59c (0x30 B, 3 ROM refs; label glyph buffer for LEVEL/ATK/DEF JP bitmaps)
	.incbin "roms/2343.gba", 0x184F59C, 0x30         @ label glyph data
card_glyph_table_3:                                  @ 0x0984f5cc (0x1550 B, 2 ROM refs; glyph table 3, consumed by file-C modules)
	.incbin "roms/2343.gba", 0x184F5CC, 0x1550       @ glyph table 3 body (to blob end 0x1850B1C; 0x1cf4a+0x50+0x30+0x1550=0x1e51a)
hud_life_points_font:
	.incbin "graphics/bin/duel-field/tiles/hud_life_points_font.bin"          @ 0x1850B1C, 0xAC0
hud_phase_highlights_palette:
	.incbin "graphics/bin/duel-field/palettes/hud_phase_highlights_palette.bin"  @ 0x18515DC, 0x20
hud_gap_tiles:
	.incbin "graphics/bin/duel-field/tiles/hud_gap_tiles.bin"                 @ 0x18515FC, 0x400（HUD gap 4bpp tile sheet）
hud_phases_highlight:
	.incbin "graphics/bin/duel-field/tiles/hud_phases_highlight.bin"          @ 0x18519FC, 0x3634（至 0x1855030）
@ 外场 tile image 指针表 @ 0x1855030, 7 × u32 (6 modes + sentinel)
duel_field_outer_tile_pointers:
	.word campaign_outer_image          @ 0x0985504C
	.word link_outer_image              @ 0x09855A2C
	.word puzzle_outer_image            @ 0x0985600C
	.word limited_outer_image           @ 0x098567EC
	.word theme_outer_image             @ 0x098575CC
	.word survival_outer_image          @ 0x09857FAC
	.word duel_field_outer_extra_tiles  @ 0x0985878C (sentinel)

@ ── 外场图块数据（6种决斗模式，大小各异）──────────────────────────────
@ duel_field_outer_tile_pointers @ 0x1855030 已拆出,指向本段 6 个 base + 1 sentinel
@ Campaign（战役）外场图块，ROM 0x185504C，0x9E0 字节（80 图块）
campaign_outer_image:
	.incbin "graphics/bin/duel-field/tiles/campaign_outer_image.bin"
@ Link Duel（联机）外场图块，ROM 0x1855A2C，0x5E0 字节（47 图块）
link_outer_image:
	.incbin "graphics/bin/duel-field/tiles/link_outer_image.bin"
@ Duel Puzzle（谜题）外场图块，ROM 0x185600C，0x7E0 字节（63 图块）
puzzle_outer_image:
	.incbin "graphics/bin/duel-field/tiles/puzzle_outer_image.bin"
@ Limited Duel（限定）外场图块，ROM 0x18567EC，0xDE0 字节（111 图块）
limited_outer_image:
	.incbin "graphics/bin/duel-field/tiles/limited_outer_image.bin"
@ Theme Duel（主题）外场图块，ROM 0x18575CC，0x9E0 字节（80 图块）
theme_outer_image:
	.incbin "graphics/bin/duel-field/tiles/theme_outer_image.bin"
@ Survival Mode（生存）外场图块，ROM 0x1857FAC，0x7E0 字节（63 图块）
survival_outer_image:
	.incbin "graphics/bin/duel-field/tiles/survival_outer_image.bin"

@ 外场 extra tile sheet + 外场调色板指针表
@ ROM 0x185878C - 0x1859388，0xBFC 字节
duel_field_outer_extra_tiles:
	.incbin "graphics/bin/duel-field/tiles/duel_field_outer_extra_tiles.bin"      @ 0x185878C, 0xBE0（~95 tiles 4bpp）

@ 外场调色板指针表 @ 0x185936C, 7 × u32 (6 modes + sentinel)
duel_field_outer_palette_pointers:
	.word campaign_outer_palette        @ 0x09859388
	.word link_outer_palette            @ 0x098593C8
	.word puzzle_outer_palette          @ 0x09859408
	.word limited_outer_palette         @ 0x09859448
	.word theme_outer_palette           @ 0x09859488
	.word survival_outer_palette        @ 0x098594C8
	.word duel_field_extra_palette      @ 0x09859508 (sentinel)

@ ── 外场调色板（6种模式，每个 0x40 字节 = 2个子调色板）────────────────
@ 调色板槽位 9–10 加载进 BG 调色板 RAM；Tilemap 条目主要引用槽位 9
campaign_outer_palette:
	.incbin "graphics/bin/duel-field/palettes/campaign_outer_palette.bin"
link_outer_palette:
	.incbin "graphics/bin/duel-field/palettes/link_outer_palette.bin"
puzzle_outer_palette:
	.incbin "graphics/bin/duel-field/palettes/puzzle_outer_palette.bin"
limited_outer_palette:
	.incbin "graphics/bin/duel-field/palettes/limited_outer_palette.bin"
theme_outer_palette:
	.incbin "graphics/bin/duel-field/palettes/theme_outer_palette.bin"
survival_outer_palette:
	.incbin "graphics/bin/duel-field/palettes/survival_outer_palette.bin"

@ 额外 palette (2×16 色) + LP/阶段 Tilemap 指针表
@ ROM 0x1859508 - 0x1859563，0x5C 字节
duel_field_extra_palette:
	.incbin "graphics/bin/duel-field/palettes/duel_field_extra_palette.bin"      @ 0x1859508, 0x40（2×16 色）

@ LP/阶段 Tilemap 指针表 @ 0x1859548, 7 × u32 (6 modes + sentinel)
hud_phases_tilemap_pointers:
	.word campaign_outer_lp_tilemap     @ 0x09859564
	.word link_outer_lp_tilemap         @ 0x09859A14
	.word puzzle_outer_lp_tilemap       @ 0x09859EC4
	.word limited_outer_lp_tilemap      @ 0x0985A374
	.word theme_outer_lp_tilemap        @ 0x0985A824
	.word survival_outer_lp_tilemap     @ 0x0985ACD4
	.word hud_phases_map                @ 0x0985B184 (sentinel)

@ ── LP/阶段显示区 Tilemap（6种模式，每个 0x4B0 字节 = 30×20 图块）──────
@ 与外场 Tilemap 共用同一套外场图块数据和调色板
campaign_outer_lp_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/campaign_outer_lp_tilemap.bin"
link_outer_lp_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/link_outer_lp_tilemap.bin"
puzzle_outer_lp_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/puzzle_outer_lp_tilemap.bin"
limited_outer_lp_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/limited_outer_lp_tilemap.bin"
theme_outer_lp_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/theme_outer_lp_tilemap.bin"
survival_outer_lp_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/survival_outer_lp_tilemap.bin"

@ "Phases Map?" 图块 + 外场 Tilemap 指针表
@ ROM 0x185B184 - 0x185B650，0x4CC 字节
hud_phases_map:
	.incbin "graphics/bin/duel-field/tiles/hud_phases_map.bin"                   @ 0x185B184, 0x4B0

@ 外场 Tilemap 指针表 @ 0x185B634, 7 × u32 (6 modes + sentinel)
duel_field_outer_tilemap_pointers:
	.word campaign_outer_tilemap        @ 0x0985B650
	.word link_outer_tilemap            @ 0x0985BB00
	.word puzzle_outer_tilemap          @ 0x0985BFB0
	.word limited_outer_tilemap         @ 0x0985C460
	.word theme_outer_tilemap           @ 0x0985C910
	.word survival_outer_tilemap        @ 0x0985CDC0
	.word duel_field_common_inner_tilemap  @ 0x0985D270 (sentinel)

@ ── 外场 Tilemap（6种模式，每个 0x4B0 字节 = 30×20 图块）──────────────
campaign_outer_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/campaign_outer_tilemap.bin"
link_outer_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/link_outer_tilemap.bin"
puzzle_outer_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/puzzle_outer_tilemap.bin"
limited_outer_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/limited_outer_tilemap.bin"
theme_outer_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/theme_outer_tilemap.bin"
survival_outer_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/survival_outer_tilemap.bin"

@ 内场公共 Tilemap（所有模式共享，0x4B0 字节 = 30×20 图块）
@ ROM 0x185D270 - 0x185D71F
duel_field_common_inner_tilemap:
	.incbin "graphics/bin/duel-field/tilemaps/duel_field_common_inner_tilemap.bin"

@ ── 内场图块数据（6种模式，每个 0x1680 字节 = 180 图块）────────────────
@ 数据从 0x185D720 开始（紧接内场公共 Tilemap 后），6 × 0x1680 = 0x8D00 字节
@ 代码用 campaign_inner_image + mode * 0x1680 访问,字面量池只引用 base
campaign_inner_image:
	.incbin "graphics/bin/duel-field/tiles/campaign_inner_image.bin"
link_inner_image:
	.incbin "graphics/bin/duel-field/tiles/link_inner_image.bin"
puzzle_inner_image:
	.incbin "graphics/bin/duel-field/tiles/puzzle_inner_image.bin"
limited_inner_image:
	.incbin "graphics/bin/duel-field/tiles/limited_inner_image.bin"
theme_inner_image:
	.incbin "graphics/bin/duel-field/tiles/theme_inner_image.bin"
survival_inner_image:
	.incbin "graphics/bin/duel-field/tiles/survival_inner_image.bin"

@ 第 7 inner tile 变体（0 代码/指针引用; 5×3 卡槽同构 survival_inner_image; 可能未实装 mode）
@ ROM 0x1865E20 - 0x186749F，0x1680 字节
unused_inner_image:
	.incbin "graphics/bin/duel-field/tiles/unused_inner_image.bin"

@ ── 内场调色板（6种模式，每个 0x20 字节 = 1个子调色板）────────────────
@ 代码用 campaign_inner_palette + mode * 0x20 访问,字面量池只引用 base
campaign_inner_palette:
	.incbin "graphics/bin/duel-field/palettes/campaign_inner_palette.bin"
	.incbin "graphics/bin/duel-field/palettes/link_inner_palette.bin"
	.incbin "graphics/bin/duel-field/palettes/puzzle_inner_palette.bin"
	.incbin "graphics/bin/duel-field/palettes/limited_inner_palette.bin"
	.incbin "graphics/bin/duel-field/palettes/theme_inner_palette.bin"
	.incbin "graphics/bin/duel-field/palettes/survival_inner_palette.bin"

@ 后 16MB 第一段剩余：ROM 0x1867560 - 0x188CF2F（内场调色板后,小图标图块前）
	.incbin "roms/2343.gba", 0x1867560, 0x259D0

@ ── 小图标图块 + 调色板 (131 个 icon, tiles 紧接 palettes)──────────────────
@ tiles    ROM 0x188CF30..0x1896290  (131 × 0x120 = 0x9360 B)
@ palettes ROM 0x1896290..0x18972F0  (131 × 0x20  = 0x1060 B)
@ 玩家 + 对手 + 其他角色,具体语义待逆向 mapping;暂用 icon_NNN 命名
icon_tiles_base:
	.incbin "graphics/bin/icons/tiles/icon_000.bin"
	.incbin "graphics/bin/icons/tiles/icon_001.bin"
	.incbin "graphics/bin/icons/tiles/icon_002.bin"
	.incbin "graphics/bin/icons/tiles/icon_003.bin"
	.incbin "graphics/bin/icons/tiles/icon_004.bin"
	.incbin "graphics/bin/icons/tiles/icon_005.bin"
	.incbin "graphics/bin/icons/tiles/icon_006.bin"
	.incbin "graphics/bin/icons/tiles/icon_007.bin"
	.incbin "graphics/bin/icons/tiles/icon_008.bin"
	.incbin "graphics/bin/icons/tiles/icon_009.bin"
	.incbin "graphics/bin/icons/tiles/icon_010.bin"
	.incbin "graphics/bin/icons/tiles/icon_011.bin"
	.incbin "graphics/bin/icons/tiles/icon_012.bin"
	.incbin "graphics/bin/icons/tiles/icon_013.bin"
	.incbin "graphics/bin/icons/tiles/icon_014.bin"
	.incbin "graphics/bin/icons/tiles/icon_015.bin"
	.incbin "graphics/bin/icons/tiles/icon_016.bin"
	.incbin "graphics/bin/icons/tiles/icon_017.bin"
	.incbin "graphics/bin/icons/tiles/icon_018.bin"
	.incbin "graphics/bin/icons/tiles/icon_019.bin"
	.incbin "graphics/bin/icons/tiles/icon_020.bin"
	.incbin "graphics/bin/icons/tiles/icon_021.bin"
	.incbin "graphics/bin/icons/tiles/icon_022.bin"
	.incbin "graphics/bin/icons/tiles/icon_023.bin"
	.incbin "graphics/bin/icons/tiles/icon_024.bin"
	.incbin "graphics/bin/icons/tiles/icon_025.bin"
	.incbin "graphics/bin/icons/tiles/icon_026.bin"
	.incbin "graphics/bin/icons/tiles/icon_027.bin"
	.incbin "graphics/bin/icons/tiles/icon_028.bin"
	.incbin "graphics/bin/icons/tiles/icon_029.bin"
	.incbin "graphics/bin/icons/tiles/icon_030.bin"
	.incbin "graphics/bin/icons/tiles/icon_031.bin"
	.incbin "graphics/bin/icons/tiles/icon_032.bin"
	.incbin "graphics/bin/icons/tiles/icon_033.bin"
	.incbin "graphics/bin/icons/tiles/icon_034.bin"
	.incbin "graphics/bin/icons/tiles/icon_035.bin"
	.incbin "graphics/bin/icons/tiles/icon_036.bin"
	.incbin "graphics/bin/icons/tiles/icon_037.bin"
	.incbin "graphics/bin/icons/tiles/icon_038.bin"
	.incbin "graphics/bin/icons/tiles/icon_039.bin"
	.incbin "graphics/bin/icons/tiles/icon_040.bin"
	.incbin "graphics/bin/icons/tiles/icon_041.bin"
	.incbin "graphics/bin/icons/tiles/icon_042.bin"
	.incbin "graphics/bin/icons/tiles/icon_043.bin"
	.incbin "graphics/bin/icons/tiles/icon_044.bin"
	.incbin "graphics/bin/icons/tiles/icon_045.bin"
	.incbin "graphics/bin/icons/tiles/icon_046.bin"
	.incbin "graphics/bin/icons/tiles/icon_047.bin"
	.incbin "graphics/bin/icons/tiles/icon_048.bin"
	.incbin "graphics/bin/icons/tiles/icon_049.bin"
	.incbin "graphics/bin/icons/tiles/icon_050.bin"
	.incbin "graphics/bin/icons/tiles/icon_051.bin"
	.incbin "graphics/bin/icons/tiles/icon_052.bin"
	.incbin "graphics/bin/icons/tiles/icon_053.bin"
	.incbin "graphics/bin/icons/tiles/icon_054.bin"
	.incbin "graphics/bin/icons/tiles/icon_055.bin"
	.incbin "graphics/bin/icons/tiles/icon_056.bin"
	.incbin "graphics/bin/icons/tiles/icon_057.bin"
	.incbin "graphics/bin/icons/tiles/icon_058.bin"
	.incbin "graphics/bin/icons/tiles/icon_059.bin"
	.incbin "graphics/bin/icons/tiles/icon_060.bin"
	.incbin "graphics/bin/icons/tiles/icon_061.bin"
	.incbin "graphics/bin/icons/tiles/icon_062.bin"
	.incbin "graphics/bin/icons/tiles/icon_063.bin"
	.incbin "graphics/bin/icons/tiles/icon_064.bin"
	.incbin "graphics/bin/icons/tiles/icon_065.bin"
	.incbin "graphics/bin/icons/tiles/icon_066.bin"
	.incbin "graphics/bin/icons/tiles/icon_067.bin"
	.incbin "graphics/bin/icons/tiles/icon_068.bin"
	.incbin "graphics/bin/icons/tiles/icon_069.bin"
	.incbin "graphics/bin/icons/tiles/icon_070.bin"
	.incbin "graphics/bin/icons/tiles/icon_071.bin"
	.incbin "graphics/bin/icons/tiles/icon_072.bin"
	.incbin "graphics/bin/icons/tiles/icon_073.bin"
	.incbin "graphics/bin/icons/tiles/icon_074.bin"
	.incbin "graphics/bin/icons/tiles/icon_075.bin"
	.incbin "graphics/bin/icons/tiles/icon_076.bin"
	.incbin "graphics/bin/icons/tiles/icon_077.bin"
	.incbin "graphics/bin/icons/tiles/icon_078.bin"
	.incbin "graphics/bin/icons/tiles/icon_079.bin"
	.incbin "graphics/bin/icons/tiles/icon_080.bin"
	.incbin "graphics/bin/icons/tiles/icon_081.bin"
	.incbin "graphics/bin/icons/tiles/icon_082.bin"
	.incbin "graphics/bin/icons/tiles/icon_083.bin"
	.incbin "graphics/bin/icons/tiles/icon_084.bin"
	.incbin "graphics/bin/icons/tiles/icon_085.bin"
	.incbin "graphics/bin/icons/tiles/icon_086.bin"
	.incbin "graphics/bin/icons/tiles/icon_087.bin"
	.incbin "graphics/bin/icons/tiles/icon_088.bin"
	.incbin "graphics/bin/icons/tiles/icon_089.bin"
	.incbin "graphics/bin/icons/tiles/icon_090.bin"
	.incbin "graphics/bin/icons/tiles/icon_091.bin"
	.incbin "graphics/bin/icons/tiles/icon_092.bin"
	.incbin "graphics/bin/icons/tiles/icon_093.bin"
	.incbin "graphics/bin/icons/tiles/icon_094.bin"
	.incbin "graphics/bin/icons/tiles/icon_095.bin"
	.incbin "graphics/bin/icons/tiles/icon_096.bin"
	.incbin "graphics/bin/icons/tiles/icon_097.bin"
	.incbin "graphics/bin/icons/tiles/icon_098.bin"
	.incbin "graphics/bin/icons/tiles/icon_099.bin"
	.incbin "graphics/bin/icons/tiles/icon_100.bin"
	.incbin "graphics/bin/icons/tiles/icon_101.bin"
	.incbin "graphics/bin/icons/tiles/icon_102.bin"
	.incbin "graphics/bin/icons/tiles/icon_103.bin"
	.incbin "graphics/bin/icons/tiles/icon_104.bin"
	.incbin "graphics/bin/icons/tiles/icon_105.bin"
	.incbin "graphics/bin/icons/tiles/icon_106.bin"
	.incbin "graphics/bin/icons/tiles/icon_107.bin"
	.incbin "graphics/bin/icons/tiles/icon_108.bin"
	.incbin "graphics/bin/icons/tiles/icon_109.bin"
	.incbin "graphics/bin/icons/tiles/icon_110.bin"
	.incbin "graphics/bin/icons/tiles/icon_111.bin"
	.incbin "graphics/bin/icons/tiles/icon_112.bin"
	.incbin "graphics/bin/icons/tiles/icon_113.bin"
	.incbin "graphics/bin/icons/tiles/icon_114.bin"
	.incbin "graphics/bin/icons/tiles/icon_115.bin"
	.incbin "graphics/bin/icons/tiles/icon_116.bin"
	.incbin "graphics/bin/icons/tiles/icon_117.bin"
	.incbin "graphics/bin/icons/tiles/icon_118.bin"
	.incbin "graphics/bin/icons/tiles/icon_119.bin"
	.incbin "graphics/bin/icons/tiles/icon_120.bin"
	.incbin "graphics/bin/icons/tiles/icon_121.bin"
	.incbin "graphics/bin/icons/tiles/icon_122.bin"
	.incbin "graphics/bin/icons/tiles/icon_123.bin"
	.incbin "graphics/bin/icons/tiles/icon_124.bin"
	.incbin "graphics/bin/icons/tiles/icon_125.bin"
	.incbin "graphics/bin/icons/tiles/icon_126.bin"
	.incbin "graphics/bin/icons/tiles/icon_127.bin"
	.incbin "graphics/bin/icons/tiles/icon_128.bin"
	.incbin "graphics/bin/icons/tiles/icon_129.bin"
	.incbin "graphics/bin/icons/tiles/icon_130.bin"

icon_palettes_base:
	.incbin "graphics/bin/icons/palettes/icon_000.bin"
	.incbin "graphics/bin/icons/palettes/icon_001.bin"
	.incbin "graphics/bin/icons/palettes/icon_002.bin"
	.incbin "graphics/bin/icons/palettes/icon_003.bin"
	.incbin "graphics/bin/icons/palettes/icon_004.bin"
	.incbin "graphics/bin/icons/palettes/icon_005.bin"
	.incbin "graphics/bin/icons/palettes/icon_006.bin"
	.incbin "graphics/bin/icons/palettes/icon_007.bin"
	.incbin "graphics/bin/icons/palettes/icon_008.bin"
	.incbin "graphics/bin/icons/palettes/icon_009.bin"
	.incbin "graphics/bin/icons/palettes/icon_010.bin"
	.incbin "graphics/bin/icons/palettes/icon_011.bin"
	.incbin "graphics/bin/icons/palettes/icon_012.bin"
	.incbin "graphics/bin/icons/palettes/icon_013.bin"
	.incbin "graphics/bin/icons/palettes/icon_014.bin"
	.incbin "graphics/bin/icons/palettes/icon_015.bin"
	.incbin "graphics/bin/icons/palettes/icon_016.bin"
	.incbin "graphics/bin/icons/palettes/icon_017.bin"
	.incbin "graphics/bin/icons/palettes/icon_018.bin"
	.incbin "graphics/bin/icons/palettes/icon_019.bin"
	.incbin "graphics/bin/icons/palettes/icon_020.bin"
	.incbin "graphics/bin/icons/palettes/icon_021.bin"
	.incbin "graphics/bin/icons/palettes/icon_022.bin"
	.incbin "graphics/bin/icons/palettes/icon_023.bin"
	.incbin "graphics/bin/icons/palettes/icon_024.bin"
	.incbin "graphics/bin/icons/palettes/icon_025.bin"
	.incbin "graphics/bin/icons/palettes/icon_026.bin"
	.incbin "graphics/bin/icons/palettes/icon_027.bin"
	.incbin "graphics/bin/icons/palettes/icon_028.bin"
	.incbin "graphics/bin/icons/palettes/icon_029.bin"
	.incbin "graphics/bin/icons/palettes/icon_030.bin"
	.incbin "graphics/bin/icons/palettes/icon_031.bin"
	.incbin "graphics/bin/icons/palettes/icon_032.bin"
	.incbin "graphics/bin/icons/palettes/icon_033.bin"
	.incbin "graphics/bin/icons/palettes/icon_034.bin"
	.incbin "graphics/bin/icons/palettes/icon_035.bin"
	.incbin "graphics/bin/icons/palettes/icon_036.bin"
	.incbin "graphics/bin/icons/palettes/icon_037.bin"
	.incbin "graphics/bin/icons/palettes/icon_038.bin"
	.incbin "graphics/bin/icons/palettes/icon_039.bin"
	.incbin "graphics/bin/icons/palettes/icon_040.bin"
	.incbin "graphics/bin/icons/palettes/icon_041.bin"
	.incbin "graphics/bin/icons/palettes/icon_042.bin"
	.incbin "graphics/bin/icons/palettes/icon_043.bin"
	.incbin "graphics/bin/icons/palettes/icon_044.bin"
	.incbin "graphics/bin/icons/palettes/icon_045.bin"
	.incbin "graphics/bin/icons/palettes/icon_046.bin"
	.incbin "graphics/bin/icons/palettes/icon_047.bin"
	.incbin "graphics/bin/icons/palettes/icon_048.bin"
	.incbin "graphics/bin/icons/palettes/icon_049.bin"
	.incbin "graphics/bin/icons/palettes/icon_050.bin"
	.incbin "graphics/bin/icons/palettes/icon_051.bin"
	.incbin "graphics/bin/icons/palettes/icon_052.bin"
	.incbin "graphics/bin/icons/palettes/icon_053.bin"
	.incbin "graphics/bin/icons/palettes/icon_054.bin"
	.incbin "graphics/bin/icons/palettes/icon_055.bin"
	.incbin "graphics/bin/icons/palettes/icon_056.bin"
	.incbin "graphics/bin/icons/palettes/icon_057.bin"
	.incbin "graphics/bin/icons/palettes/icon_058.bin"
	.incbin "graphics/bin/icons/palettes/icon_059.bin"
	.incbin "graphics/bin/icons/palettes/icon_060.bin"
	.incbin "graphics/bin/icons/palettes/icon_061.bin"
	.incbin "graphics/bin/icons/palettes/icon_062.bin"
	.incbin "graphics/bin/icons/palettes/icon_063.bin"
	.incbin "graphics/bin/icons/palettes/icon_064.bin"
	.incbin "graphics/bin/icons/palettes/icon_065.bin"
	.incbin "graphics/bin/icons/palettes/icon_066.bin"
	.incbin "graphics/bin/icons/palettes/icon_067.bin"
	.incbin "graphics/bin/icons/palettes/icon_068.bin"
	.incbin "graphics/bin/icons/palettes/icon_069.bin"
	.incbin "graphics/bin/icons/palettes/icon_070.bin"
	.incbin "graphics/bin/icons/palettes/icon_071.bin"
	.incbin "graphics/bin/icons/palettes/icon_072.bin"
	.incbin "graphics/bin/icons/palettes/icon_073.bin"
	.incbin "graphics/bin/icons/palettes/icon_074.bin"
	.incbin "graphics/bin/icons/palettes/icon_075.bin"
	.incbin "graphics/bin/icons/palettes/icon_076.bin"
	.incbin "graphics/bin/icons/palettes/icon_077.bin"
	.incbin "graphics/bin/icons/palettes/icon_078.bin"
	.incbin "graphics/bin/icons/palettes/icon_079.bin"
	.incbin "graphics/bin/icons/palettes/icon_080.bin"
	.incbin "graphics/bin/icons/palettes/icon_081.bin"
	.incbin "graphics/bin/icons/palettes/icon_082.bin"
	.incbin "graphics/bin/icons/palettes/icon_083.bin"
	.incbin "graphics/bin/icons/palettes/icon_084.bin"
	.incbin "graphics/bin/icons/palettes/icon_085.bin"
	.incbin "graphics/bin/icons/palettes/icon_086.bin"
	.incbin "graphics/bin/icons/palettes/icon_087.bin"
	.incbin "graphics/bin/icons/palettes/icon_088.bin"
	.incbin "graphics/bin/icons/palettes/icon_089.bin"
	.incbin "graphics/bin/icons/palettes/icon_090.bin"
	.incbin "graphics/bin/icons/palettes/icon_091.bin"
	.incbin "graphics/bin/icons/palettes/icon_092.bin"
	.incbin "graphics/bin/icons/palettes/icon_093.bin"
	.incbin "graphics/bin/icons/palettes/icon_094.bin"
	.incbin "graphics/bin/icons/palettes/icon_095.bin"
	.incbin "graphics/bin/icons/palettes/icon_096.bin"
	.incbin "graphics/bin/icons/palettes/icon_097.bin"
	.incbin "graphics/bin/icons/palettes/icon_098.bin"
	.incbin "graphics/bin/icons/palettes/icon_099.bin"
	.incbin "graphics/bin/icons/palettes/icon_100.bin"
	.incbin "graphics/bin/icons/palettes/icon_101.bin"
	.incbin "graphics/bin/icons/palettes/icon_102.bin"
	.incbin "graphics/bin/icons/palettes/icon_103.bin"
	.incbin "graphics/bin/icons/palettes/icon_104.bin"
	.incbin "graphics/bin/icons/palettes/icon_105.bin"
	.incbin "graphics/bin/icons/palettes/icon_106.bin"
	.incbin "graphics/bin/icons/palettes/icon_107.bin"
	.incbin "graphics/bin/icons/palettes/icon_108.bin"
	.incbin "graphics/bin/icons/palettes/icon_109.bin"
	.incbin "graphics/bin/icons/palettes/icon_110.bin"
	.incbin "graphics/bin/icons/palettes/icon_111.bin"
	.incbin "graphics/bin/icons/palettes/icon_112.bin"
	.incbin "graphics/bin/icons/palettes/icon_113.bin"
	.incbin "graphics/bin/icons/palettes/icon_114.bin"
	.incbin "graphics/bin/icons/palettes/icon_115.bin"
	.incbin "graphics/bin/icons/palettes/icon_116.bin"
	.incbin "graphics/bin/icons/palettes/icon_117.bin"
	.incbin "graphics/bin/icons/palettes/icon_118.bin"
	.incbin "graphics/bin/icons/palettes/icon_119.bin"
	.incbin "graphics/bin/icons/palettes/icon_120.bin"
	.incbin "graphics/bin/icons/palettes/icon_121.bin"
	.incbin "graphics/bin/icons/palettes/icon_122.bin"
	.incbin "graphics/bin/icons/palettes/icon_123.bin"
	.incbin "graphics/bin/icons/palettes/icon_124.bin"
	.incbin "graphics/bin/icons/palettes/icon_125.bin"
	.incbin "graphics/bin/icons/palettes/icon_126.bin"
	.incbin "graphics/bin/icons/palettes/icon_127.bin"
	.incbin "graphics/bin/icons/palettes/icon_128.bin"
	.incbin "graphics/bin/icons/palettes/icon_129.bin"
	.incbin "graphics/bin/icons/palettes/icon_130.bin"

@ ROM 0x18972F0 - 0x1B101AB (f02 Seg-1 carve Host A: 17 labels)
	.incbin "roms/2343.gba", 0x18972F0, 0x508     @ pre-aob_card_tile_src gap
aob_card_tile_src:                              @ 0x098977F8: AOB card tile data (0x2000B)
	.incbin "roms/2343.gba", 0x18977F8, 0x2000
aob_card_pal_src:                               @ 0x098997F8: AOB card palette (0x40B)
	.incbin "roms/2343.gba", 0x18997F8, 0x40
aob_ptnsect_src:                                @ 0x09899838: ptnsect data for init_aob_ctx
	.incbin "roms/2343.gba", 0x1899838, 0xB3EC4
campaign_bg_pal_src_a:                          @ 0x0994D6FC: campaign BG palette A (0x20B)
	.incbin "roms/2343.gba", 0x194D6FC, 0x20
campaign_bg_pal_src_b:                          @ 0x0994D71C: campaign BG palette B
	.incbin "roms/2343.gba", 0x194D71C, 0x2120
campaign_bg_tile_src:                           @ 0x0994F83C: campaign BG tile data
	.incbin "roms/2343.gba", 0x194F83C, 0x4000
campaign_bg_tilemap_src:                        @ 0x0995383C: campaign BG tilemap
	.incbin "roms/2343.gba", 0x195383C, 0x4B0
pack_deck_b_pal_src:                            @ 0x09953CEC: pack deck_b palette src
	.incbin "roms/2343.gba", 0x1953CEC, 0x2F40
pack_deck_b_tile1_src:                          @ 0x09956C2C: pack deck_b tile 1 src
	.incbin "roms/2343.gba", 0x1956C2C, 0x54000
pack_deck_b_tile3_src:                          @ 0x099AAC2C: pack deck_b tile 3 src
	.incbin "roms/2343.gba", 0x19AAC2C, 0xF420
pack_deck_b_tile2_src:                          @ 0x099BA04C: pack deck_b tile 2 src
	.incbin "roms/2343.gba", 0x19BA04C, 0x54000
pack_deck_b_tilemap_src:                        @ 0x09A0E04C: pack deck_b tilemap src
	.incbin "roms/2343.gba", 0x1A0E04C, 0xC4E0
campaign_bg_pal_src_c:                          @ 0x09A1A52C: campaign BG palette C
	.incbin "roms/2343.gba", 0x1A1A52C, 0x3A80
pack_deck_a_tile1_src:                          @ 0x09A1DFAC: pack deck_a tile 1 src
	.incbin "roms/2343.gba", 0x1A1DFAC, 0x68000
pack_deck_a_tile3_src:                          @ 0x09A85FAC: pack deck_a tile 3 src
	.incbin "roms/2343.gba", 0x1A85FAC, 0x12E40
pack_deck_a_tile2_src:                          @ 0x09A98DEC: pack deck_a tile 2 src
	.incbin "roms/2343.gba", 0x1A98DEC, 0x68000
pack_deck_a_tilemap_src:                        @ 0x09B00DEC: pack deck_a tilemap src
	.incbin "roms/2343.gba", 0x1B00DEC, 0xF3C0  @ tail to host end 0x1B101AB

@ 调色板块（Copy 1），ROM 0x1B101AC–0x1B1200B，7776 字节（27 个对手，每对手 288 字节）
@ 注意：Copy 2（0x1B4FE9C–0x1B51CFB）与本块内容完全相同，引用同一文件
@ 字面量池 0x0802D240 引用本 base（loader 函数指针表 5 项之一）
opponent_palettes_base:
	.incbin "graphics/bin/opponents/palettes/palette_copy1.bin"

@ Top 图块整块，ROM 0x1B1200C–0x1B4800B，221184 字节（27 × 0x2000）
@ 注意：第 20 个对手 Elemental Hero Electrum 图块偏移不规则（0x1B3899C），整段统一保留
@ 字面量池 0x0802D244 引用本 base
opponent_top_tiles_base:
	.incbin "graphics/bin/opponents/tiles/top_tiles_all.bin"

@ Top Tilemap（27 个对手），ROM 0x1B4800C–0x1B4FE9B，每个 0x4B0 字节
@ 字面量池 0x0802D24C 引用本 base
opponent_top_tilemap_base:
	.incbin "graphics/bin/opponents/tilemaps/kuriboh_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/scapegoat_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/skull_servant_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/watapon_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/pikeru_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/batteryman_c_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/ojama_yellow_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/goblin_king_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/des_frog_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/water_dragon_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/redd_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/vampire_genesis_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/infernal_flame_emperor_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/ocean_dragon_lord_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/helios_duo_megiste_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/gilford_the_legend_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/dark_eradicator_warlock_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/guardian_exode_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/goldd_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/elemental_hero_electrum_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/raviel_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/horus_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/stronghold_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/sacred_phoenix_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/cyber_end_dragon_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/mirror_match_top_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/copycat_top_tilemap.bin"

@ 调色板块（Copy 2），ROM 0x1B4FE9C–0x1B51CFB，7776 字节（内容与 Copy 1 完全相同）
@ 全 ROM 0 引用：loader 字面量池只引用 Copy 1，本块为冗余副本（仅文档边界标记，不进 rom_data.inc）
opponent_palettes_copy2_unused:
	.incbin "graphics/bin/opponents/palettes/palette_copy1.bin"

@ Bottom 图块整块，ROM 0x1B51CFC–0x1B87CFB，221184 字节（27 × 0x2000）
@ 字面量池 0x0802D248 引用本 base
opponent_bottom_tiles_base:
	.incbin "graphics/bin/opponents/tiles/bottom_tiles_all.bin"

@ Bottom Tilemap（27 个对手），ROM 0x1B87CFC–0x1B8FB8B，每个 0x4B0 字节
@ 字面量池 0x0802D250 引用本 base
opponent_bottom_tilemap_base:
	.incbin "graphics/bin/opponents/tilemaps/kuriboh_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/scapegoat_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/skull_servant_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/watapon_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/pikeru_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/batteryman_c_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/ojama_yellow_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/goblin_king_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/des_frog_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/water_dragon_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/redd_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/vampire_genesis_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/infernal_flame_emperor_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/ocean_dragon_lord_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/helios_duo_megiste_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/gilford_the_legend_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/dark_eradicator_warlock_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/guardian_exode_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/goldd_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/elemental_hero_electrum_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/raviel_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/horus_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/stronghold_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/sacred_phoenix_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/cyber_end_dragon_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/mirror_match_bottom_tilemap.bin"
	.incbin "graphics/bin/opponents/tilemaps/copycat_bottom_tilemap.bin"

@ 后 16MB 第一段剩余部分：ROM 0x1B8FB8C–0x1DBF019（内嵌英/日字库已拆出）
@ 头段：含 font_jp_sjis_lookup_table @ 0x1BA1524 (3850 B) + count u16 + 其他未识别数据
@ (f02 Seg-1 carve Host B: 8 labels)
	.incbin "roms/2343.gba", 0x1B8FB8C, 0x2648    @ pre-result_screen_pal2_src gap
result_screen_pal2_src:                         @ 0x09B921D4: result screen copy_bytes src (0x20B)
	.incbin "roms/2343.gba", 0x1B921D4, 0x20
result_screen_tile1_src:                        @ 0x09B921F4: result screen tile src 1
	.incbin "roms/2343.gba", 0x1B921F4, 0x800
result_screen_tile2_src:                        @ 0x09B929F4: result screen tile src 2
	.incbin "roms/2343.gba", 0x1B929F4, 0xA90
result_screen_tile3_src:                        @ 0x09B93484: result screen tile src 3
	.incbin "roms/2343.gba", 0x1B93484, 0x3C0
result_screen_tile4_src:                        @ 0x09B93844: result screen tile src 4
	.incbin "roms/2343.gba", 0x1B93844, 0x42E4
pack_default_pal_src:                           @ 0x09B97B28: init_pack_selection default pal src
	.incbin "roms/2343.gba", 0x1B97B28, 0x240
pack_default_tile_src:                          @ 0x09B97D68: init_pack_selection default tile src
	.incbin "roms/2343.gba", 0x1B97D68, 0x4000
pack_default_tilemap_src:                       @ 0x09B9BD68: init_pack_selection default tilemap src
	.incbin "roms/2343.gba", 0x1B9BD68, 0x10C3C  @ tail to host end 0x1BAC9A4

@ 日文字库（4 个 charset 变体，每个 1925 glyph，8bpp 预解码每像素 1 字节）
@ 索引 = (hi & 0xF) << 7 | (lo & 0x7F)；详见 doc/dev/xx-encoding-analysis.md + tools/rom-export/export_font_jp.py
@ ROM 顺序：main_small + outline_small（紧邻配对）→ gap1 → main_large + outline_large → tail gap
font_jp_main_small:                                @ 0x1BAC9A4..0x1BDB998 (192500 B = 1925 × 10×10)
	.incbin "graphics/bin/font-jp/main_small.bin"
font_jp_outline_small:                             @ 0x1BDB998..0x1C1F468 (277200 B = 1925 × 12×12)
	.incbin "graphics/bin/font-jp/outline_small.bin"

@ gap1：未识别数据 50052 B（main_small/outline_small 与 main_large/outline_large 之间）
	.incbin "roms/2343.gba", 0x1C1F468, 0xC384     @ 0x1C1F468..0x1C2B7EC

font_jp_main_large:                                @ 0x1C2B7EC..0x1C6F2BC (277200 B = 1925 × 12×12)
	.incbin "graphics/bin/font-jp/main_large.bin"
font_jp_outline_large:                             @ 0x1C6F2BC..0x1CCB490 (377300 B = 1925 × 14×14)
	.incbin "graphics/bin/font-jp/outline_large.bin"

@ tail gap：未识别数据 5632 B（outline_large 与 font_ascii_8x8 之间）
	.incbin "roms/2343.gba", 0x1CCB490, 0x1600     @ 0x1CCB490..0x1CCCA90

@ 英文字库（1bpp 8×8，256 字符，ASCII 直接索引），ROM 0x1CCCA90–0x1CCD28F，2048 B
@ 加载函数 FUN_080f1b60 @ 0x080f1b60；详见 doc/dev/p2-font-location-findings.md
	.include "data/font.s"

name_o_palette_data:                               @ 0x09ccd290 carve H: name_o OAM/BG palette (16 RGB15 colors, 32B)
	.hword 0x0000, 0x7c00, 0x001f, 0x7c1f, 0x83e0, 0xffe0, 0x83ff, 0xffff  @ entries [0..7]
	.hword 0x2108, 0x6000, 0x0018, 0x6018, 0x0300, 0x6300, 0x0318, 0x5294  @ entries [8..15]
	.incbin "roms/2343.gba", 0x1CCD2B0, 0x16B0      @ remaining to 0x1CCE960

@ 卡包封面条幅图 (ROM 0x1CCE960..0x1CE822C, 0x198CC bytes)
@ 指针表 (.word label) + 51 × 0x800 bytes 8bpp OBJ tile data
	.include "data/pack-banners.s"

	.incbin "roms/2343.gba", 0x1CE822C, 0xD19E4     @ 0x1CE822C..0x1DB9C10 字库后段后部

@ 游戏文本字符串表 6 lang (ROM 偏移 0x1DB9C10 - 0x1DFF9E3, ~286 KB)
@ JA + EN/DE/FR/IT/ES, master pointer table @ ROM 0xF40 (1651 行)
@ 见 data/game-strings.s 的 wrapper 注释 + doc/dev/data-structure/game-strings.md
	.include "data/game-strings.s"

@ 后 16MB 中间段前部：ROM偏移 0x1DFF9E4 - 0x1E31553
@ 已拆分：
@   - 0x1DFF9E4..0x1E246D4 (0x24CF0 B): 剩余未知
@   - 0x1E246D4..0x1E25554 (0xE80 B):   HUD 数字/图标 sheet (FUN_08101068)
@   - 0x1E25554..0x1E25674 (0x120 B):   gap
@   - 0x1E25674..0x1E25F34 (0x8C0 B):   state sheets (FUN_081016c0 s1 small/big + s3)
@   - 0x1E25F34..0x1E265B4 (0x680 B):   gap
@   - 0x1E265B4..0x1E2FEB4 (0x9900 B):  switch sheets 13 cases (FUN_08109788)
@   - 0x1E2FEB4..0x1E310B4 (0x1200 B):  post-case9 未知格式 (FF/AA-dominant)
@   - 0x1E310B4..0x1E312B4 (0x200 B):   aux OBJ 箭头 (FUN_081066fc)
@   - 0x1E312B4..0x1E31554 (0x2A0 B):   剩余未知
	.incbin "roms/2343.gba", 0x1DFF9E4, 0x24CF0

@ HUD 数字/图标 sheet (FUN_08101068, 116 tiles 4bpp, 3712 B)
	.incbin "graphics/bin/ui-misc/_MERGED_HUD_sheet_01E246D4_01E25554.bin"

	.incbin "roms/2343.gba", 0x1E25554, 0x120

@ state=1/3 sheets (FUN_081016c0)
	.incbin "graphics/bin/ui-misc/FUN081016c0_s1_small_01E25674.bin"
	.incbin "graphics/bin/ui-misc/FUN081016c0_s1_big_01E25934.bin"
	.incbin "graphics/bin/ui-misc/FUN081016c0_s3_01E25C34.bin"

	.incbin "roms/2343.gba", 0x1E25F34, 0x680

@ 13 个 switch case sprite sheet (FUN_08109788, 8bpp 16×16 px item)
@ case 0: 5 items 菜单 action
@ case 1: 6 items 心形 HP 1-5
@ case 2: 11 items 杂项 UI
@ case 3: 5 items 心形↑ HP 1-5
@ case 4: 9 items 卡边框色标
@ case 5: 4 items 星计数徽章
@ case 6: 10 items 属性（闇/水/炎/光/風/地/魔/罠/神+彩虹）
@ case a: 10 items 属性 (dup)
@ case 7: 22 items 种族
@ case b: 22 items 种族 (dup)
@ case 8: 8 items 棕印章
@ case c: 8 items 棕印章 (dup)
@ case 9: 33 items 状态/成就
	.incbin "graphics/bin/ui-misc/switch_sheets/case_0_0x01E265B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_1_0x01E26AB4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_2_0x01E270B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_3_0x01E27BB4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_4_0x01E280B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_5_0x01E289B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_6_0x01E28DB4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_a_0x01E297B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_7_0x01E2A1B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_b_0x01E2B7B4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_8_0x01E2CDB4.bin"
	.incbin "graphics/bin/ui-misc/switch_sheets/case_c_0x01E2D5B4.bin"
card_status_sprite_sheet:  @ 0x09e2ddb4 (32+1 card status OBJ sprite items, 0x100B each, index 0..31 active)
	.incbin "graphics/bin/ui-misc/switch_sheets/case_9_0x01E2DDB4.bin"

	.incbin "roms/2343.gba", 0x1E2FEB4, 0x1200

@ aux OBJ 箭头 × 4 (FUN_081066fc, 16 tiles 4bpp)
	.incbin "graphics/bin/ui-misc/FUN081066fc_obj_01E310B4.bin"

	.incbin "roms/2343.gba", 0x1E312B4, 0x2A0

@ card-mini-frame OBJ 调色板（ROM偏移 0x1E31554 - 0x1E31713，0x1C0 B）
	.include "data/card-mini-frame-palette.s"

@ 后 16MB 中间段后部：ROM偏移 0x1E31714 - 0x1E58D0D
@ 已拆分：
@   - 0x1E31714..0x1E31754 (0x40 B): 未知
@   - 0x1E31754..0x1E31774 (0x20 B): 动画调色板 (FUN_081058c8)
@   - 0x1E31774..0x1E31794 (0x20 B): 未知
@   - 0x1E31794..0x1E317B4 (0x20 B): OBJ 辅助调色板 (FUN_081066fc)
@   - 0x1E317B4..0x1E58D0B (0x27558 B): 剩余未知
	.incbin "roms/2343.gba", 0x1E31714, 0x40
	.incbin "graphics/bin/ui-misc/FUN081058c8_anim_pal_01E31754.bin"
	.incbin "roms/2343.gba", 0x1E31774, 0x20
	.incbin "graphics/bin/ui-misc/FUN081066fc_obj_pal_01E31794.bin"
	.incbin "roms/2343.gba", 0x1E317B4, 0x7F04      @ 0x1E317B4..0x1E396B8 demo 资源块前 (SDK 调试串等, 未结构化)
@ demo/exodia 资源块 (0x1E396B8..0x1E398DC, 548B)，生成: tools/rom-export/export_demo_exodia_resources.py
	.include "data/demo-exodia-resources.s"
@ NNS/GL SDK 断言串 carve (0x1E398DC..0x1E58D0C; 仅引用串抽 .asciz, 余 .incbin) —
@ 生成: tools/rom-export/export_assert_strings.py -> assert_carve_block.txt
@ ----------------------------------------------------------------------------
@ NNS/GL SDK 断言串 (suppress_assert_report file/expr 参数) — carve 自 0x1E317B4 blob 的
@ after-demo 段; 仅被代码引用的 156 串抽成带 label 的 .asciz, 其余 (未引用串/二进制/指针表)
@ 仍以 .incbin 原样保留。代码 .word 经 resolve_word_symbol 指向这些 label。byte-identical。
@ ----------------------------------------------------------------------------
gl_common_c_filename:
	.asciz "GL/GL_Common.c"
	.incbin "roms/2343.gba", 0x1E398EB, 0x1
assert_bright_16_bright_16:
	.asciz "bright >= -16 && bright <= 16"
	.incbin "roms/2343.gba", 0x1E3990A, 0x2
assert_blend1_0_blend1_16:
	.asciz "blend1 >= 0 && blend1 <= 16"
assert_blend2_0_blend2_16:
	.asciz "blend2 >= 0 && blend2 <= 16"
assert_u32_psrc_0x3_0:
	.asciz "((u32)pSrc & 0x3) == 0"
	.incbin "roms/2343.gba", 0x1E3995B, 0x1
gl_file_c_filename:
	.asciz "GL/GL_File.c"
	.incbin "roms/2343.gba", 0x1E39969, 0x3
assert_psrc:
	.asciz "pSrc"
	.incbin "roms/2343.gba", 0x1E39971, 0x3
assert_pkey:
	.asciz "pKey"
	.incbin "roms/2343.gba", 0x1E39979, 0x3   @ 3B 对齐填充
@ fs_load 用 3 个路径前缀魔数 (each NUL-terminated, 4B 对齐):
@   ".LZ" = 解压后缀；"#" = 语言占位符 (替换为 j/e/g/f/i/s)；"!" = 区域占位符 (替换为 'J'/'E')
fs_key_lz_suffix:
	.asciz ".LZ"                              @ 0x09e3997c (4B incl NUL)
fs_key_hash:
	.ascii "#\0\0\0"                          @ 0x09e39980 (1 char + 3B pad)
fs_key_excl:
	.ascii "!\0\0\0"                          @ 0x09e39984
fs_lang_char_j:
	.ascii "j\0\0\0"                          @ 0x09e39988 = JP language char
fs_lang_char_e:
	.ascii "e\0\0\0"                          @ 0x09e3998c = EN
fs_lang_char_g:
	.ascii "g\0\0\0"                          @ 0x09e39990 = DE (g for German)
fs_lang_char_f:
	.ascii "f\0\0\0"                          @ 0x09e39994 = FR
fs_lang_char_i:
	.ascii "i\0\0\0"                          @ 0x09e39998 = IT
fs_lang_char_s:
	.ascii "s\0\0\0"                          @ 0x09e3999c = ES
@ 6 ptr 表, gSettings 低 3 位 (language_id) ×4 索引, fs_load 入口 ldmia ×2 复制 24 B 进栈
fs_language_char_ptr_table:                   @ 0x09e399a0
	.word fs_lang_char_j                      @ language_id 0
	.word fs_lang_char_e                      @ language_id 1
	.word fs_lang_char_g                      @ language_id 2
	.word fs_lang_char_f                      @ language_id 3
	.word fs_lang_char_i                      @ language_id 4
	.word fs_lang_char_s                      @ language_id 5
assert_phead_comptype_1:
	.asciz "pHead->compType == 1"
	.incbin "roms/2343.gba", 0x1E399CD, 0x3   @ 0x1E399CD..0x1E399D0 对齐填充 (00 00 00)
@ trig_table: 256 项 s16 cos/sin 查表 (幅值 256 = Q8.8 的 1.0; 全圆 256 步, 1 步≈1.406°)
@   sin(a) = trig_table[a]; cos(a) = trig_table[a+0x40]; compute_bg_affine_matrix_scaled 用
@   trig[0]=0 trig[0x40]=256(sin90) trig[0x80]=0 trig[0xc0]=-256(sin270)
trig_table:
	.hword 0, 6, 12, 18, 25, 31, 37, 43, 49, 56, 62, 68, 74, 80, 86, 92
	.hword 97, 103, 109, 115, 120, 126, 131, 136, 142, 147, 152, 157, 162, 167, 171, 176
	.hword 181, 185, 189, 193, 197, 201, 205, 209, 212, 216, 219, 222, 225, 228, 231, 234
	.hword 236, 238, 241, 243, 244, 246, 248, 249, 251, 252, 253, 254, 254, 255, 255, 255
	.hword 256, 255, 255, 255, 254, 254, 253, 252, 251, 249, 248, 246, 244, 243, 241, 238
	.hword 236, 234, 231, 228, 225, 222, 219, 216, 212, 209, 205, 201, 197, 193, 189, 185
	.hword 181, 176, 171, 167, 162, 157, 152, 147, 142, 136, 131, 126, 120, 115, 109, 103
	.hword 97, 92, 86, 80, 74, 68, 62, 56, 49, 43, 37, 31, 25, 18, 12, 6
	.hword 0, -6, -12, -18, -25, -31, -37, -43, -49, -56, -62, -68, -74, -80, -86, -92
	.hword -97, -103, -109, -115, -120, -126, -131, -136, -142, -147, -152, -157, -162, -167, -171, -176
	.hword -181, -185, -189, -193, -197, -201, -205, -209, -212, -216, -219, -222, -225, -228, -231, -234
	.hword -236, -238, -241, -243, -244, -246, -248, -249, -251, -252, -253, -254, -254, -255, -255, -255
	.hword -256, -255, -255, -255, -254, -254, -253, -252, -251, -249, -248, -246, -244, -243, -241, -238
	.hword -236, -234, -231, -228, -225, -222, -219, -216, -212, -209, -205, -201, -197, -193, -189, -185
	.hword -181, -176, -171, -167, -162, -157, -152, -147, -142, -136, -131, -126, -120, -115, -109, -103
	.hword -97, -92, -86, -80, -74, -68, -62, -56, -49, -43, -37, -31, -25, -18, -12, -6
	.incbin "roms/2343.gba", 0x1E39BD0, 0x80   @ trig_table 之后剩余 blob
gl_oam_c_filename:
	.asciz "GL/GL_Oam.c"
assert_num_32:
	.asciz "num < 32"
	.incbin "roms/2343.gba", 0x1E39C65, 0x3
gl_scrollbar_c_filename:
	.asciz "GL/GL_Scrollbar.c"
	.incbin "roms/2343.gba", 0x1E39C7A, 0x2
assert_pthis:
	.asciz "pThis"
	.incbin "roms/2343.gba", 0x1E39C82, 0x806
ig2d_main_c_filename:
	.asciz "GL/IG2D_Main.c"
	.incbin "roms/2343.gba", 0x1E3A497, 0x1
assert_usedncebuff_ig2d_load_anm_max:
	.asciz "UsedNceBuff < IG2D_LOAD_ANM_MAX"
assert_usednanbuff_ig2d_load_anm_max:
	.asciz "UsedNanBuff < IG2D_LOAD_ANM_MAX"
assert_psequence:
	.asciz "pSequence"
	.incbin "roms/2343.gba", 0x1E3A4E2, 0x2
assert_bg_2_bg_3:
	.asciz "bg == 2 || bg == 3"
	.incbin "roms/2343.gba", 0x1E3A4F7, 0x1   @ 前缀 1B (00)
assert_expr_zero:
	.asciz "0"                                @ resolve_bg_affine_param_offset 的 assert(0) 表达式串
	.incbin "roms/2343.gba", 0x1E3A4FA, 0x2   @ 后缀 2B
assert_pcell_null:
	.asciz "( pCell ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A50E, 0x2
assert_usedcellanm_nelems_cellanmbank:
	.asciz "UsedCellAnm < NELEMS(CellAnmBank)"
	.incbin "roms/2343.gba", 0x1E3A532, 0x2
assert_ppcellbank_null:
	.asciz "( ppCellBank ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A54B, 0x1
assert_pfname_null:
	.asciz "( pFname ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A55F, 0x1
assert_ppanimbank_null:
	.asciz "( ppAnimBank ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A577, 0x1
assert_ppchardata_null:
	.asciz "( ppCharData ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A58F, 0x1
assert_pppltdata_null:
	.asciz "( ppPltData ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A5A6, 0x2
assert_psrcdata:
	.asciz "pSrcData"
	.incbin "roms/2343.gba", 0x1E3A5B1, 0x3
assert_ppltproxt:
	.asciz "pPltProxt"
	.incbin "roms/2343.gba", 0x1E3A5BE, 0x2
assert_false:
	.asciz "FALSE"
	.incbin "roms/2343.gba", 0x1E3A5C6, 0x2
assert_pbuf_null:
	.asciz "( pBuf ) != NULL"
	.incbin "roms/2343.gba", 0x1E3A5D9, 0x3
assert_ppanimbank_numsequences_0:
	.asciz "(*ppAnimBank)->numSequences != 0"
	.incbin "roms/2343.gba", 0x1E3A5FD, 0x3
assert_ppcellanim_null:
	.asciz "( *ppCellAnim ) != NULL"
assert_ppanimbank_psequencearrayhead:
	.asciz "( &((*ppAnimBank)->pSequenceArrayHead[i]) ) != NULL"
isd_draw_c_filename:
	.asciz "GL/ISD_Draw.c"
	.incbin "roms/2343.gba", 0x1E3A65A, 0x2     @ 前缀 2B
assert_expr_zero_65c:
	.asciz "0"                                  @ 0x09e3a65c ISD_Draw 类型 assert(0) 条件串
	.incbin "roms/2343.gba", 0x1E3A65E, 0x2     @ 2B align pad after assert_expr_zero_65c
char_frame_decode_lut:                            @ 0x09e3a660
	.incbin "roms/2343.gba", 0x1E3A660, 0x110   @ 272B: 68 entries x 4B halfword-pair decode LUT
	                                              @ LUT[2*char_idx + encode_mode] -> VRAM halfword
	                                              @ Consumed by: decode_char_frame_to_vram DWORD_08017410
prh_main_c_filename:
	.asciz "GL/PRH_Main.c"
	.incbin "roms/2343.gba", 0x1E3A77E, 0x2
assert_pdst_nameid:
	.asciz "pDst->nameID"
	.incbin "roms/2343.gba", 0x1E3A78D, 0x83B   @ 2107B: up to sprite_gfx_type_meta
sprite_gfx_type_meta:                             @ 0x09e3afc8
	.word 0x031e0000                              @ type0: [tile_start=0x00, tile_count=0x1e, screen_page=0x03, ...]
	.word 0x061e0300                              @ type1
	.word 0x081e0600                              @ type2
	.word 0x0a1e0800                              @ type3 (4 entries x 4B = 16B)
sprite_palette_type_table:                        @ 0x09e3afd8
	.byte 1, 1, 16, 16                            @ palette indices for sprite types 0..3 (4B)
banlist_jp_str_src:
	.incbin "roms/2343.gba", 0x1E3AFDC, 0x7C
name_char_group_47:
	.incbin "roms/2343.gba", 0x1E3B058, 0x8
name_char_group_46:
	.incbin "roms/2343.gba", 0x1E3B060, 0x8
name_char_group_45:
	.incbin "roms/2343.gba", 0x1E3B068, 0x8
name_char_group_44:
	.incbin "roms/2343.gba", 0x1E3B070, 0x8
name_char_group_43:
	.incbin "roms/2343.gba", 0x1E3B078, 0x8
name_char_group_42:
	.incbin "roms/2343.gba", 0x1E3B080, 0x8
name_char_group_41:
	.incbin "roms/2343.gba", 0x1E3B088, 0x8
name_char_group_40:
	.incbin "roms/2343.gba", 0x1E3B090, 0x8
name_char_group_39:
	.incbin "roms/2343.gba", 0x1E3B098, 0xC
name_char_group_37:
	.incbin "roms/2343.gba", 0x1E3B0A4, 0xC
name_char_group_36:
	.incbin "roms/2343.gba", 0x1E3B0B0, 0x4
name_char_group_35:
	.incbin "roms/2343.gba", 0x1E3B0B4, 0xC
name_char_group_34:
	.incbin "roms/2343.gba", 0x1E3B0C0, 0x8
name_char_group_33:
	.incbin "roms/2343.gba", 0x1E3B0C8, 0x8
name_char_group_32:
	.incbin "roms/2343.gba", 0x1E3B0D0, 0x8
name_char_group_31:
	.incbin "roms/2343.gba", 0x1E3B0D8, 0x8
name_char_group_30:
	.incbin "roms/2343.gba", 0x1E3B0E0, 0x8
name_char_group_29:
	.incbin "roms/2343.gba", 0x1E3B0E8, 0x10
name_char_group_28:
	.incbin "roms/2343.gba", 0x1E3B0F8, 0x10
name_char_group_27:
	.incbin "roms/2343.gba", 0x1E3B108, 0x10
name_char_group_26:
	.incbin "roms/2343.gba", 0x1E3B118, 0x10
name_char_group_25:
	.incbin "roms/2343.gba", 0x1E3B128, 0x10
name_char_group_24:
	.incbin "roms/2343.gba", 0x1E3B138, 0x8
name_char_group_23:
	.incbin "roms/2343.gba", 0x1E3B140, 0x8
name_char_group_22:
	.incbin "roms/2343.gba", 0x1E3B148, 0x8
name_char_group_21:
	.incbin "roms/2343.gba", 0x1E3B150, 0x8
name_char_group_20:
	.incbin "roms/2343.gba", 0x1E3B158, 0x8
name_char_group_19:
	.incbin "roms/2343.gba", 0x1E3B160, 0xC
name_char_group_18:
	.incbin "roms/2343.gba", 0x1E3B16C, 0xC
name_char_group_17:
	.incbin "roms/2343.gba", 0x1E3B178, 0x10
name_char_group_16:
	.incbin "roms/2343.gba", 0x1E3B188, 0xC
name_char_group_15:
	.incbin "roms/2343.gba", 0x1E3B194, 0xC
name_char_group_14:
	.incbin "roms/2343.gba", 0x1E3B1A0, 0xC
name_char_group_13:
	.incbin "roms/2343.gba", 0x1E3B1AC, 0xC
name_char_group_12:
	.incbin "roms/2343.gba", 0x1E3B1B8, 0xC
name_char_group_11:
	.incbin "roms/2343.gba", 0x1E3B1C4, 0xC
name_char_group_10:
	.incbin "roms/2343.gba", 0x1E3B1D0, 0xC
name_char_group_09:
	.incbin "roms/2343.gba", 0x1E3B1DC, 0xC
name_char_group_08:
	.incbin "roms/2343.gba", 0x1E3B1E8, 0xC
name_char_group_07:
	.incbin "roms/2343.gba", 0x1E3B1F4, 0xC
name_char_group_06:
	.incbin "roms/2343.gba", 0x1E3B200, 0xC
name_char_group_05:
	.incbin "roms/2343.gba", 0x1E3B20C, 0xC
name_char_group_04:
	.incbin "roms/2343.gba", 0x1E3B218, 0xC
name_char_group_03:
	.incbin "roms/2343.gba", 0x1E3B224, 0xC
name_char_group_02:
	.incbin "roms/2343.gba", 0x1E3B230, 0xC
name_char_group_01:
	.incbin "roms/2343.gba", 0x1E3B23C, 0xC
name_char_group_00:
	.incbin "roms/2343.gba", 0x1E3B248, 0x9
name_char_range_table:
	.incbin "roms/2343.gba", 0x1E3B251, 0x63
line_break_seq:
	.incbin "roms/2343.gba", 0x1E3B2B4, 0x4
name_main_c_filename:
	.asciz "NameInput/Name_main.c"
	.incbin "roms/2343.gba", 0x1E3B2CE, 0x2
assert_cnt_name_mojitbl_width_1_name:
	.asciz "(cnt + NAME_MOJITBL_WIDTH - 1) / NAME_MOJITBL_WIDTH * NAME_MOJITBL_WIDTH < sizeof(pThis->mojiTbl) / 2"
	.incbin "roms/2343.gba", 0x1E3B336, 0x2
assert_table_last_fmt:
	.asciz "TableLast(%d)\n"
	.incbin "roms/2343.gba", 0x1E3B347, 0x1
assert_dir_1_dir_1:
	.asciz "dir == 1 || dir == -1"
	.incbin "roms/2343.gba", 0x1E3B35E, 0x2   @ 2B pad before name_o paths
name_o_ncer_path:                              @ 0x09e3b360
	.asciz "name_input/name_o_01.LZncer"      @ 27+NUL=28B (4B-aligned, no extra pad)
name_o_nanr_path:                              @ 0x09e3b37c
	.asciz "name_input/name_o_01.LZnanr"      @ 27+NUL=28B
name_o_ncgr_path:                              @ 0x09e3b398
	.asciz "name_input/name_o_01.LZncgr"      @ 27+NUL=28B
name_o_nclr_path:                              @ 0x09e3b3b4
	.asciz "name_input/name_o_01.LZnclr"      @ 27+NUL=28B
name_o_resource_desc:                          @ 0x09e3b3d0 carve F: name_o_01 G2D resource desc (4 path ptrs)
	.word name_o_ncer_path
	.word name_o_nanr_path
	.word name_o_ncgr_path
	.word name_o_nclr_path
name_b_01_path:                                @ 0x09e3b3e0
	.asciz "name_input/name_b_01.LZ5bg"       @ 26+NUL=27B + 1B pad = 28B
	.byte 0x00                                 @ 1B align pad
name_b_02_path:                                @ 0x09e3b3fc
	.asciz "name_input/name_b_02.LZ5bg"       @ 26+NUL=27B + 1B pad = 28B
	.byte 0x00                                 @ 1B align pad
name_b_04_path:                                @ 0x09e3b418
	.asciz "name_input/name_b_04.LZ5bg"       @ 26+NUL=27B + 1B pad = 28B
	.byte 0x00                                 @ 1B align pad -> host end 0x1E3B434
assert_anmid_ig2d_getanmsequencescoun:
	.asciz "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"
cursor_anim_data_a:                    @ 0x09e3b46f carve G: cursor anim frame bytes (12B x/y offsets for 5 cursor cells)
	.byte 6, 8, 10, 6, 8, 10, 10, 8, 10, 8, 10, 8
	.incbin "roms/2343.gba", 0x1E3B47B, 0x1   @ 1B gap
cursor_anim_data_b:                    @ 0x09e3b47c carve G: cursor anim coord table (7 s32 values)
	.word 0xffffffc1    @ cell 0: x_start (signed -63)
	.word 0x00000085    @ cell 1
	.word 0x00000019    @ cell 2
	.word 0x00000085    @ cell 3
	.word 0x00000071    @ cell 4
	.word 0x00000085    @ cell 5
	.word 0x000000c9    @ cell 6
	.incbin "roms/2343.gba", 0x1E3B498, 0xC     @ 0x09e3b498..0x09e3b4a4 (3 words: anim coords continued)
name_input_render_param_4b:                    @ 0x09e3b4a4 (4B render param block: 38 84 88 84; memcpy src in tick_name_input_render_by_state)
	.incbin "roms/2343.gba", 0x1E3B4A4, 0x4
name_input_default_name:                       @ 0x09e3b4a8 (SJIS "tesuto" default commit name; dispatch_name_input_confirm_state src)
	.incbin "roms/2343.gba", 0x1E3B4A8, 0x809   @ 0x09e3b4a8..0x09e3bcb1
banlist_char_candidate_str:                    @ 0x09e3bcb1 (90 SJIS pairs + null pair; init_banlist_pass_input_bg0_page)
	.incbin "roms/2343.gba", 0x1E3BCB1, 0xB6    @ 182B
	.incbin "roms/2343.gba", 0x1E3BD67, 0xD5    @ 0xd5 bytes prefix before ext_char_group
banlist_pass_ext_char_group:                   @ 0x09e3be3c (417B SJIS null-padded char groups; retreat_banlist_password_char_and_render)
	.incbin "roms/2343.gba", 0x1E3BE3C, 0x1A1  @ 417B ext char group data
banlist_pass_char_str:                         @ 0x09e3bfdd (99B SJIS char str; encode_pass_table_entry_to_line_buf)
	.incbin "roms/2343.gba", 0x1E3BFDD, 0x63    @ 99B
banlist_pass_alt_char:                         @ 0x09e3c040 (4B SJIS full-width space + null; encode_pass_table_entry_to_line_buf)
	.incbin "roms/2343.gba", 0x1E3C040, 0x4     @ 4B
rom_password_table:                            @ 0x09e3c044 (671x2B LE halfwords; load_banlist_password_table_from_rom)
	.incbin "roms/2343.gba", 0x1E3C044, 0x53E   @ 671*2=1342B
	.incbin "roms/2343.gba", 0x1E3C582, 0x2     @ trailing pad to host end
pass_main_c_filename:
	.asciz "PassInput/Pass_main.c"
	.incbin "roms/2343.gba", 0x1E3C59A, 0x2
assert_dir_1_dir_1_59c:
	.asciz "dir == 1 || dir == -1"
	.incbin "roms/2343.gba", 0x1E3C5B2, 0x2      @ 2B pre-pad
banlist_pass_obj_ncer_path:                    @ 0x09e3c5b4
	.incbin "roms/2343.gba", 0x1E3C5B4, 0x1C    @ "pass_input/pass_o_01.LZncer\0" (28B)
banlist_pass_obj_nanr_path:                    @ 0x09e3c5d0
	.incbin "roms/2343.gba", 0x1E3C5D0, 0x1C    @ "pass_input/pass_o_01.LZnanr\0" (28B)
banlist_pass_obj_ncgr_path:                    @ 0x09e3c5ec
	.incbin "roms/2343.gba", 0x1E3C5EC, 0x1C    @ "pass_input/pass_o_01.LZncgr\0" (28B)
banlist_pass_obj_nclr_path:                    @ 0x09e3c608
	.incbin "roms/2343.gba", 0x1E3C608, 0x1C    @ "pass_input/pass_o_01.LZnclr\0" (28B)
banlist_pass_obj_resource_desc:                @ 0x09e3c624 (4-word ptr struct; load_banlist_pass_input_scene_resources)
	.word banlist_pass_obj_ncer_path
	.word banlist_pass_obj_nanr_path
	.word banlist_pass_obj_ncgr_path
	.word banlist_pass_obj_nclr_path
banlist_pass_bg1_fs_path:                      @ 0x09e3c634
	.incbin "roms/2343.gba", 0x1E3C634, 0x1C    @ "pass_input/pass_b_01.LZ5bg\0" (28B)
banlist_pass_bg2_fs_path:                      @ 0x09e3c650
	.incbin "roms/2343.gba", 0x1E3C650, 0x20    @ "pass_input/moziire_b_01.LZ5bg\0\0\0" (32B)
assert_anmid_ig2d_getanmsequencescoun_670:
	.asciz "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"
banlist_scroll_view_anim_params:               @ 0x09e3c6ab (6B: view-state anim params indexed by gSettings encoding bits; tick_banlist_scroll_view_by_state)
	.byte 0x06, 0x06, 0x07, 0x07, 0x07, 0x07
	.incbin "roms/2343.gba", 0x1E3C6B1, 0x3    @ 3 NUL bytes pad
assert_dstbuffid_0_dstbuffid_def_prhl:
	.asciz "dstBuffID >= 0 && dstBuffID < DEF_PRHLIST_MAX"
	.incbin "roms/2343.gba", 0x1E3C6E2, 0x88E
shu_main_c_filename:
	.asciz "Shuen/SHU_main.c"
	.incbin "roms/2343.gba", 0x1E3CF81, 0x3
assert_anmid_ig2d_getanmsequencescoun_f84:
	.asciz "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"
	.incbin "roms/2343.gba", 0x1E3CFBF, 0x9C5
vij_main_c_filename:
	.asciz "Vija/VIJ_main.c"
assert_anmid_ig2d_getanmsequencescoun_994:
	.asciz "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"
	.incbin "roms/2343.gba", 0x1E3D9CF, 0x5        @ 5B pre-pad (bytes 00 01 02 01 00)
vija_bg_jp_path:                                   @ GBA 0x09e3d9d4
	.asciz "demo/vija/BG1_all.LZ5bg"              @ 24B (23 chars + NUL, 4-byte aligned)
vija_bg_us_path:                                   @ GBA 0x09e3d9ec
	.asciz "demo/vija/BG1_all_US.LZ5bg"           @ 27B (26 chars + NUL)
	.byte  0x0                                     @ 1B alignment pad -> total 28B
vija_bg_fs_path_pair:                              @ GBA 0x09e3da08 (ref: DAT_0801cbf4)
	.word  vija_bg_jp_path                         @ [0] JP FS path ptr
	.word  vija_bg_us_path                         @ [4] US FS path ptr
vija_obj_slot_seq:                                 @ GBA 0x09e3da10 (ref: DAT_0801ce00)
	.byte  0x01, 0x03, 0x00, 0x02, 0x04           @ OBJ slot index sequence [phase 0..4]
	.byte  0x0, 0x0, 0x0                           @ 3B pad
	.incbin "roms/2343.gba", 0x1E3DA18, 0xC2F4    @ remainder
assert_pdst_null:
	.asciz "(pDst) != NULL"
	.incbin "roms/2343.gba", 0x1E49D1B, 0x1
assert_psrc_null:
	.asciz "(pSrc) != NULL"
	.incbin "roms/2343.gba", 0x1E49D2B, 0x1
fx_mtx22_c_filename:
	.asciz "nnsys/g2d/fx_mtx22.c"
	.incbin "roms/2343.gba", 0x1E49D41, 0x3
assert_a_null:
	.asciz "(a) != NULL"
assert_b_null:
	.asciz "(b) != NULL"
assert_ab_null:
	.asciz "(ab) != NULL"
	.incbin "roms/2343.gba", 0x1E49D69, 0x70B
g2d_animation_inline_h_filename:
	.asciz "inc/nnsys/g2d/g2d_Animation_inline.h"
	.incbin "roms/2343.gba", 0x1E4A499, 0x3
assert_panimctrl:
	.asciz "pAnimCtrl"
	.incbin "roms/2343.gba", 0x1E4A4A6, 0x2
g2d_animation_c_filename:
	.asciz "nnsys/g2d/g2d_Animation.c"
	.incbin "roms/2343.gba", 0x1E4A4C2, 0x2
assert_psequence_4c4:
	.asciz "pSequence"
	.incbin "roms/2343.gba", 0x1E4A4CE, 0x2
assert_panimctrl_panimsequence:
	.asciz "pAnimCtrl->pAnimSequence"
	.incbin "roms/2343.gba", 0x1E4A4E9, 0x3
assert_panimctrl_pcurrent:
	.asciz "pAnimCtrl->pCurrent"
assert_pfunctor:
	.asciz "pFunctor"
	.incbin "roms/2343.gba", 0x1E4A509, 0x3
assert_pframe:
	.asciz "pFrame"
	.incbin "roms/2343.gba", 0x1E4A513, 0x1
assert_panimctrl_callbackfunctor_pfun:
	.asciz "pAnimCtrl->callbackFunctor.pFunc"
	.incbin "roms/2343.gba", 0x1E4A535, 0x3
assert_void_panimctrl_pcurrent_pconte:
	.asciz "(void*)pAnimCtrl->pCurrent->pContent"
	.incbin "roms/2343.gba", 0x1E4A55D, 0x3
assert_pnext_pcontent:
	.asciz "pNext->pContent"
assert_frames_0:
	.asciz "frames >= 0"
assert_pcallback:
	.asciz "pCallBack"
	.incbin "roms/2343.gba", 0x1E4A586, 0x2
assert_panimsequence:
	.asciz "pAnimSequence"
	.incbin "roms/2343.gba", 0x1E4A596, 0x2
assert_void_pfunc:
	.asciz "(void*)pFunc"
	.incbin "roms/2343.gba", 0x1E4A5A5, 0x3
assert_type_nns_g2d_anmcallbacktype_s:
	.asciz "type != NNS_G2D_ANMCALLBACKTYPE_SPEC_FRM"
	.incbin "roms/2343.gba", 0x1E4A5D1, 0x3
g2_oam_h_filename:
	.asciz "inc/nitro/g2_oam.h"
	.incbin "roms/2343.gba", 0x1E4A5E7, 0xC5
assert_effect_gx_oam_effect_none_effe:
	.asciz "(effect) == GX_OAM_EFFECT_NONE || (effect) == GX_OAM_EFFECT_FLIP_H || (effect) == GX_OAM_EFFECT_FLIP_V || (effect) == GX_OAM_EFFECT_FLIP_HV || (effect) == GX_OAM_EFFECT_AFFINE || (effect) == GX_OAM_EFFECT_NODISPLAY || (effect) == GX_OAM_EFFECT_AFFINE_DOUBLE"
	.incbin "roms/2343.gba", 0x1E4A7AE, 0x2
assert_rsparam_0_rsparam_31:
	.asciz "(rsParam) >= ( 0) && (rsParam) <= ( 31)"
	.incbin "roms/2343.gba", 0x1E4A7D8, 0x494
g2d_cell_data_h_filename:
	.asciz "inc/nnsys/g2d/fmt/g2d_Cell_data.h"
	.incbin "roms/2343.gba", 0x1E4AC8E, 0x16
assert_pdst:
	.asciz "pDst"
	.incbin "roms/2343.gba", 0x1E4ACA9, 0x33
g2d_animation_inline_h_filename_cdc:
	.asciz "inc/nnsys/g2d/g2d_Animation_inline.h"
	.incbin "roms/2343.gba", 0x1E4AD01, 0x3
assert_panimctrl_d04:
	.asciz "pAnimCtrl"
	.incbin "roms/2343.gba", 0x1E4AD0E, 0x56
assert_pcellanim:
	.asciz "pCellAnim"
	.incbin "roms/2343.gba", 0x1E4AD6E, 0xF2
g2d_cellanimation_c_filename:
	.asciz "nnsys/g2d/g2d_CellAnimation.c"
	.incbin "roms/2343.gba", 0x1E4AE7E, 0x2
assert_pcellanim_pcelldatabank:
	.asciz "pCellAnim->pCellDataBank"
	.incbin "roms/2343.gba", 0x1E4AE99, 0x3
assert_pcellanim_pcurrentcell:
	.asciz "pCellAnim->pCurrentCell"
assert_panimseq:
	.asciz "pAnimSeq"
	.incbin "roms/2343.gba", 0x1E4AEBD, 0x3
assert_pcelldatabank:
	.asciz "pCellDataBank"
	.incbin "roms/2343.gba", 0x1E4AECE, 0x2
assert_nns_g2dgetanimsequenceanimtype:
	.asciz "NNS_G2dGetAnimSequenceAnimType( pAnimSeq ) == NNS_G2D_ANIMATIONTYPE_CELL"
	.incbin "roms/2343.gba", 0x1E4AF19, 0x3
assert_pcellanim_animctrl_panimsequen:
	.asciz "pCellAnim->animCtrl.pAnimSequence"
	.incbin "roms/2343.gba", 0x1E4AF3E, 0x2
assert_nns_g2dgetanimsequenceanimtype_f40:
	.asciz "NNS_G2dGetAnimSequenceAnimType( pCellAnim->animCtrl.pAnimSequence ) == NNS_G2D_ANIMATIONTYPE_CELL"
	.incbin "roms/2343.gba", 0x1E4AFA2, 0x66E
assert_pimgproxy:
	.asciz "pImgProxy"
	.incbin "roms/2343.gba", 0x1E4B61A, 0x2
g2d_image_c_filename:
	.asciz "nnsys/g2d/g2d_Image.c"
	.incbin "roms/2343.gba", 0x1E4B632, 0x2
assert_pvramlocation:
	.asciz "pVramLocation"
	.incbin "roms/2343.gba", 0x1E4B642, 0x2
assert_type_nns_g2d_vram_type_3dmain:
	.asciz "( type ) == NNS_G2D_VRAM_TYPE_3DMAIN || ( type ) == NNS_G2D_VRAM_TYPE_2DMAIN || ( type ) == NNS_G2D_VRAM_TYPE_2DSUB"
assert_psrc_6b8:
	.asciz "pSrc"
	.incbin "roms/2343.gba", 0x1E4B6BD, 0x3
assert_pdst_6c0:
	.asciz "pDst"
	.incbin "roms/2343.gba", 0x1E4B6C5, 0x3
assert_psrc_w_nns_g2d_1d_mapping_char:
	.asciz "(pSrc->W == NNS_G2D_1D_MAPPING_CHAR_SIZE) && (pSrc->H == NNS_G2D_1D_MAPPING_CHAR_SIZE)"
	.incbin "roms/2343.gba", 0x1E4B71F, 0x1
assert_nnsi_g2discharactervramtransfe:
	.asciz "!NNSi_G2dIsCharacterVramTransfered( pSrcData->characterFmt )"
	.incbin "roms/2343.gba", 0x1E4B75D, 0x3
assert_charfmt_nns_g2d_character_fmt:
	.asciz "charFmt == NNS_G2D_CHARACTER_FMT_CHAR"
	.incbin "roms/2343.gba", 0x1E4B786, 0x2
assert_false_788:
	.asciz "FALSE"
	.incbin "roms/2343.gba", 0x1E4B78E, 0x2
assert_psrcdata_790:
	.asciz "pSrcData"
	.incbin "roms/2343.gba", 0x1E4B799, 0x3
assert_psrcdata_fmt_gx_texfmt_pltt256:
	.asciz "pSrcData->fmt == GX_TEXFMT_PLTT256"
	.incbin "roms/2343.gba", 0x1E4B7BF, 0x1
assert_pcmpinfo:
	.asciz "pCmpInfo"
	.incbin "roms/2343.gba", 0x1E4B7C9, 0x3
assert_pimg:
	.asciz "pImg"
	.incbin "roms/2343.gba", 0x1E4B7D1, 0x3
assert_isvalid1dmappingtype_type_psrc:
	.asciz "IsValid1DMappingType_( type, pSrcData->mapingType )"
assert_isvaliddatasize_psrcdata_type:
	.asciz "IsValidDataSize_( pSrcData, type )"
	.incbin "roms/2343.gba", 0x1E4B82B, 0x1
assert_psrcdata_mapingtype_gx_objvram:
	.asciz "pSrcData->mapingType == GX_OBJVRAMMODE_CHAR_2D"
	.incbin "roms/2343.gba", 0x1E4B85B, 0x1
assert_nnsi_g2discharactervramtransfe_85c:
	.asciz "NNSi_G2dIsCharacterVramTransfered( pSrcData->characterFmt )"
assert_ppltproxy:
	.asciz "pPltProxy"
	.incbin "roms/2343.gba", 0x1E4B8A2, 0x73A
g2d_load_c_filename:
	.asciz "nnsys/g2d/g2d_Load.c"
	.incbin "roms/2343.gba", 0x1E4BFF1, 0x3
assert_pbinfileheader:
	.asciz "pBinFileHeader"
	.incbin "roms/2343.gba", 0x1E4C003, 0x1
assert_pcursor:
	.asciz "pCursor"
	.incbin "roms/2343.gba", 0x1E4C00C, 0x708
g2d_nan_load_h_filename:
	.asciz "inc/nnsys/g2d/load/g2d_NAN_load.h"
	.incbin "roms/2343.gba", 0x1E4C736, 0xE
g2d_nan_load_c_filename:
	.asciz "nnsys/g2d/g2d_NAN_load.c"
	.incbin "roms/2343.gba", 0x1E4C75D, 0x3
assert_pnanrfile:
	.asciz "pNanrFile"
	.incbin "roms/2343.gba", 0x1E4C76A, 0x2
assert_ppanimbank:
	.asciz "ppAnimBank"
	.incbin "roms/2343.gba", 0x1E4C777, 0x1
assert_nnsi_g2disbinfilesignaturevali:
	.asciz "NNSi_G2dIsBinFileSignatureValid( pNanrFile, (u32)'NANR' )"
	.incbin "roms/2343.gba", 0x1E4C7B2, 0x2
assert_nnsi_g2disbinfileversionvalid:
	.asciz "NNSi_G2dIsBinFileVersionValid( pNanrFile, NNS_G2dMakeVersionData( 1, 0 ) )"
	.incbin "roms/2343.gba", 0x1E4C7FF, 0x1
assert_nnsi_g2disbinfilesignaturevali_800:
	.asciz "NNSi_G2dIsBinFileSignatureValid( pNanrFile, (u32)'NMAR' )"
	.incbin "roms/2343.gba", 0x1E4C83A, 0x2
assert_pdata:
	.asciz "pData"
	.incbin "roms/2343.gba", 0x1E4C842, 0x2
assert_checkanimsequencevalidity_pseq:
	.asciz "CheckAnimSequenceValidity_( &pSeq[i] )"
	.incbin "roms/2343.gba", 0x1E4C86B, 0x739
g2d_ncg_load_c_filename:
	.asciz "nnsys/g2d/g2d_NCG_load.c"
	.incbin "roms/2343.gba", 0x1E4CFBD, 0x3
assert_pncgrfile:
	.asciz "pNcgrFile"
	.incbin "roms/2343.gba", 0x1E4CFCA, 0x2
assert_ppchardata:
	.asciz "ppCharData"
	.incbin "roms/2343.gba", 0x1E4CFD7, 0x1
assert_nnsi_g2disbinfilesignaturevali_fd8:
	.asciz "NNSi_G2dIsBinFileSignatureValid( pNcgrFile, (u32)'NCGR' )"
	.incbin "roms/2343.gba", 0x1E4D012, 0x2
assert_nnsi_g2disbinfileversionvalid_014:
	.asciz "NNSi_G2dIsBinFileVersionValid( pNcgrFile, NNS_G2dMakeVersionData( (u8)1, (u8)0 ) )"
	.incbin "roms/2343.gba", 0x1E4D067, 0x1
assert_pchardata:
	.asciz "pCharData"
	.incbin "roms/2343.gba", 0x1E4D072, 0x2
assert_pchardata_pixelfmt_gx_texfmt_p:
	.asciz "( pCharData->pixelFmt == GX_TEXFMT_PLTT16 && pCharData->W == 32 ) || ( pCharData->pixelFmt == GX_TEXFMT_PLTT256 && pCharData->W == 16 )"
assert_ppcharposinfo:
	.asciz "ppCharPosInfo"
	.incbin "roms/2343.gba", 0x1E4D10A, 0x2
assert_nnsi_g2disbinfileversionvalid_10c:
	.asciz "NNSi_G2dIsBinFileVersionValid( pNcgrFile, NNS_G2dMakeVersionData( (u8)1, (u8)1 ) )"
	.incbin "roms/2343.gba", 0x1E4D15F, 0x1
assert_nnsi_g2dgetcharacterfmttype_pc:
	.asciz "NNSi_G2dGetCharacterFmtType( pCharData->characterFmt ) == NNS_G2D_CHARACTER_FMT_CHAR"
	.incbin "roms/2343.gba", 0x1E4D1B5, 0x73B
g2d_ncl_load_c_filename:
	.asciz "nnsys/g2d/g2d_NCL_load.c"
	.incbin "roms/2343.gba", 0x1E4D909, 0x3
assert_pplttdata:
	.asciz "pPlttData"
	.incbin "roms/2343.gba", 0x1E4D916, 0x2
assert_pplttdata_prawdata:
	.asciz "pPlttData->pRawData"
	.incbin "roms/2343.gba", 0x1E4D92C, 0x3C
assert_pnclrfile:
	.asciz "pNclrFile"
	.incbin "roms/2343.gba", 0x1E4D972, 0x2
assert_pppltdata:
	.asciz "ppPltData"
	.incbin "roms/2343.gba", 0x1E4D97E, 0x2
assert_pbinfile_signature_u32_nclr_pb:
	.asciz "pBinFile->signature == (u32)'NCLR' || pBinFile->signature == (u32)'NCPR'"
	.incbin "roms/2343.gba", 0x1E4D9C9, 0x3
assert_nnsi_g2disbinfileversionvalid_9cc:
	.asciz "NNSi_G2dIsBinFileVersionValid( pNclrFile, NNS_G2dMakeVersionData( (u8)1, (u8)0 ) )"
	.incbin "roms/2343.gba", 0x1E4DA1F, 0x1
assert_pppltcmpinfo:
	.asciz "ppPltCmpInfo"
	.incbin "roms/2343.gba", 0x1E4DA2D, 0x3
assert_pplttcmpinfo:
	.asciz "pPlttCmpInfo"
	.incbin "roms/2343.gba", 0x1E4DA3D, 0x6BF
assert_pcellbank:
	.asciz "pCellBank"
	.incbin "roms/2343.gba", 0x1E4E106, 0x72
g2d_nob_load_c_filename:
	.asciz "nnsys/g2d/g2d_NOB_load.c"
	.incbin "roms/2343.gba", 0x1E4E191, 0x3
assert_pexdata:
	.asciz "pExData"
assert_pncerfile:
	.asciz "pNcerFile"
	.incbin "roms/2343.gba", 0x1E4E1A6, 0x2
assert_ppcellbank:
	.asciz "ppCellBank"
	.incbin "roms/2343.gba", 0x1E4E1B3, 0x1
assert_nnsi_g2disbinfilesignaturevali_1b4:
	.asciz "NNSi_G2dIsBinFileSignatureValid( pNcerFile, (u32)'NCER' )"
	.incbin "roms/2343.gba", 0x1E4E1EE, 0x2
assert_nnsi_g2disbinfileversionvalid_1f0:
	.asciz "NNSi_G2dIsBinFileVersionValid( pNcerFile, NNS_G2dMakeVersionData( 1, 0 ) )"
	.incbin "roms/2343.gba", 0x1E4E23B, 0x1
assert_pcelldata:
	.asciz "pCellData"
	.incbin "roms/2343.gba", 0x1E4E246, 0x69E
fx_mtx22_h_filename:
	.asciz "inc/nitro/fx_mtx22.h"
	.incbin "roms/2343.gba", 0x1E4E8F9, 0x3
assert_pdst_null_8fc:
	.asciz "(pDst) != NULL"
	.incbin "roms/2343.gba", 0x1E4E90B, 0x11
g2d_srtcontrol_c_filename:
	.asciz "nnsys/g2d/g2d_SRTControl.c"
	.incbin "roms/2343.gba", 0x1E4E937, 0x5
assert_pctrl:
	.asciz "pCtrl"
	.incbin "roms/2343.gba", 0x1E4E942, 0x2
assert_pctrl_type_nns_g2d_srtcontrolt:
	.asciz "( pCtrl->type ) == NNS_G2D_SRTCONTROLTYPE_SRT"
	.incbin "roms/2343.gba", 0x1E4E972, 0x2
assert_pdst_974:
	.asciz "pDst"
	.incbin "roms/2343.gba", 0x1E4E979, 0x88B
card_attr_order_table:  @ 0x09e4f204 (32 u32 card attr flag IDs, indexed by display slot)
	.incbin "roms/2343.gba", 0x1E4F204, 0x2B4
s_opdobj_c_filename:
	.asciz "system/s_opdobj.c"
	.incbin "roms/2343.gba", 0x1E4F4CA, 0x2
assert_ptnno_aob_ptnsect_header_p_ptn:
	.asciz "PtnNo < ((AOB_PTNSECT_HEADER*)p_ptnsect)->PtnNum"
	.incbin "roms/2343.gba", 0x1E4F4FD, 0x3
assert_anmno_aob_anmsect_header_p_anm:
	.asciz "AnmNo < ((AOB_ANMSECT_HEADER*)p_anmsect)->AnmNum"
	.incbin "roms/2343.gba", 0x1E4F531, 0x3
assert_pwork_canmwait_0:
	.asciz "pWork->cAnmWait > 0"
assert_pwork_canmcrntfrm_frmnum:
	.asciz "pWork->cAnmCrntFrm < frmnum"
	.incbin "roms/2343.gba", 0x1E4F564, 0x11C0
titleex_main_c_filename:
	.asciz "titleEx/TitleEx_main.c"
	.incbin "roms/2343.gba", 0x1E5073B, 0x1
assert_anmid_ig2d_getanmsequencescoun_73c:
	.asciz "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"
	.incbin "roms/2343.gba", 0x1E50777, 0x805D   @ 0x1E50777..0x1E587D4
demo_scene_phase_table:                           @ 0x09e587d4 demo 场景阶段分派表 (THUMB fn ptr, addr|1)
	.word reset_display_and_gl_state + 1          @ phase 0: 复位显示/GL 状态
	.word load_demo_obj_resource_slot0 + 1        @ phase 1: 加载 demo OBJ 资源 slot0
	.word tick_demo_scene_state_machine + 1       @ phase 2: tick demo 场景状态机
	.word 0x0                                     @ NULL 终止 (序列结束哨兵)
isd_affine_matrix_ptr_type4:
	.word 0x0                                     @ 0x09e587e4 ISD affine 矩阵指针槽 (type 4=BG2; ROM 内 NULL)
isd_affine_matrix_ptr_type9:
	.word 0x0                                     @ 0x09e587e8 ISD affine 矩阵指针槽 (type 9=BG3; ROM 内 NULL)
name_char_tile_slot_table:                        @ 0x09e587ec carve A: ping-pong OBJ tile indices
	.hword 0x012c                                 @ ping-pong buf0 tile 300
	.hword 0x014e                                 @ ping-pong buf1 tile 334
name_char_group_ptr_table:                        @ 0x09e587f0 carve B: 50-entry kana group ptr table
	.word name_char_group_00             @ [ 0] 0x09e3b248
	.word name_char_group_01             @ [ 1] 0x09e3b23c
	.word name_char_group_02             @ [ 2] 0x09e3b230
	.word name_char_group_03             @ [ 3] 0x09e3b224
	.word name_char_group_04             @ [ 4] 0x09e3b218
	.word name_char_group_05             @ [ 5] 0x09e3b20c
	.word name_char_group_06             @ [ 6] 0x09e3b200
	.word name_char_group_07             @ [ 7] 0x09e3b1f4
	.word name_char_group_08             @ [ 8] 0x09e3b1e8
	.word name_char_group_09             @ [ 9] 0x09e3b1dc
	.word name_char_group_10             @ [10] 0x09e3b1d0
	.word name_char_group_11             @ [11] 0x09e3b1c4
	.word name_char_group_12             @ [12] 0x09e3b1b8
	.word name_char_group_13             @ [13] 0x09e3b1ac
	.word name_char_group_14             @ [14] 0x09e3b1a0
	.word name_char_group_15             @ [15] 0x09e3b194
	.word name_char_group_16             @ [16] 0x09e3b188
	.word name_char_group_17             @ [17] 0x09e3b178
	.word name_char_group_18             @ [18] 0x09e3b16c
	.word name_char_group_19             @ [19] 0x09e3b160
	.word name_char_group_20             @ [20] 0x09e3b158
	.word name_char_group_21             @ [21] 0x09e3b150
	.word name_char_group_22             @ [22] 0x09e3b148
	.word name_char_group_23             @ [23] 0x09e3b140
	.word name_char_group_24             @ [24] 0x09e3b138
	.word name_char_group_25             @ [25] 0x09e3b128
	.word name_char_group_26             @ [26] 0x09e3b118
	.word name_char_group_27             @ [27] 0x09e3b108
	.word name_char_group_28             @ [28] 0x09e3b0f8
	.word name_char_group_29             @ [29] 0x09e3b0e8
	.word name_char_group_30             @ [30] 0x09e3b0e0
	.word name_char_group_31             @ [31] 0x09e3b0d8
	.word name_char_group_32             @ [32] 0x09e3b0d0
	.word name_char_group_33             @ [33] 0x09e3b0c8
	.word name_char_group_34             @ [34] 0x09e3b0c0
	.word name_char_group_35             @ [35] 0x09e3b0b4
	.word name_char_group_36             @ [36] 0x09e3b0b0
	.word name_char_group_37             @ [37] 0x09e3b0a4
	.word name_char_group_36             @ [38] 0x09e3b0b0 (shared target)
	.word name_char_group_39             @ [39] 0x09e3b098
	.word name_char_group_40             @ [40] 0x09e3b090
	.word name_char_group_41             @ [41] 0x09e3b088
	.word name_char_group_42             @ [42] 0x09e3b080
	.word name_char_group_43             @ [43] 0x09e3b078
	.word name_char_group_44             @ [44] 0x09e3b070
	.word name_char_group_45             @ [45] 0x09e3b068
	.word name_char_group_46             @ [46] 0x09e3b060
	.word name_char_group_47             @ [47] 0x09e3b058
	.word name_char_group_36             @ [48] 0x09e3b0b0 (shared target)
	.word name_char_group_36             @ [49] 0x09e3b0b0 (shared target)
name_input_state_table:                        @ 0x09e588b8 (page state fn-ptr table; page_state_dispatcher index)
	.word name_input_page_init+1               @ [0] 0x08017575 THUMB
	.word name_input_page_load_assets+1        @ [1] 0x080180ad THUMB
	.word name_input_page_tick+1               @ [2] 0x08019495 THUMB
	.word name_input_page_exit+1               @ [3] 0x080194ed THUMB
	.word 0                                    @ [4] NULL sentinel
banlist_pass_char_group_ptr_table:             @ 0x09e588cc (8 ROM data ptrs; encode_pass_table_entry_to_line_buf index)
	.word 0x09e3bfd4                           @ [0] char_group_0
	.word 0x09e3bfc8                           @ [1] char_group_1
	.word 0x09e3bfbc                           @ [2] char_group_2
	.word 0x09e3bfb0                           @ [3] char_group_3
	.word 0x09e3bfa4                           @ [4] char_group_4
	.word 0x09e3bf98                           @ [5] char_group_5
	.word 0x09e3bf8c                           @ [6] char_group_6
	.word 0x09e3bf80                           @ [7] char_group_7
	@ banlist_pass_char_group_ptr_table entries [8..49] (42 more .word ptrs, 168B = 0xA8)
	.word 0x09e3bf74                           @ [8]
	.word 0x09e3bf68                           @ [9]
	.word 0x09e3bf5c                           @ [10]
	.word 0x09e3bf50                           @ [11]
	.word 0x09e3bf44                           @ [12]
	.word 0x09e3bf38                           @ [13]
	.word 0x09e3bf2c                           @ [14]
	.word 0x09e3bf20                           @ [15]
	.word 0x09e3bf14                           @ [16]
	.word 0x09e3bf04                           @ [17]
	.word 0x09e3bef8                           @ [18]
	.word 0x09e3beec                           @ [19]
	.word 0x09e3bee4                           @ [20]
	.word 0x09e3bedc                           @ [21]
	.word 0x09e3bed4                           @ [22]
	.word 0x09e3becc                           @ [23]
	.word 0x09e3bec4                           @ [24]
	.word 0x09e3beb4                           @ [25]
	.word 0x09e3bea4                           @ [26]
	.word 0x09e3be94                           @ [27]
	.word 0x09e3be84                           @ [28]
	.word 0x09e3be74                           @ [29]
	.word 0x09e3be6c                           @ [30]
	.word 0x09e3be64                           @ [31]
	.word 0x09e3be5c                           @ [32]
	.word 0x09e3be54                           @ [33]
	.word 0x09e3be4c                           @ [34]
	.word 0x09e3be40                           @ [35]
	.word 0x09e3be3c                           @ [36]
	.word 0x09e3be30                           @ [37]
	.word 0x09e3be3c                           @ [38]
	.word 0x09e3be24                           @ [39]
	.word 0x09e3be1c                           @ [40]
	.word 0x09e3be14                           @ [41]
	.word 0x09e3be0c                           @ [42]
	.word 0x09e3be04                           @ [43]
	.word 0x09e3bdfc                           @ [44]
	.word 0x09e3bdf4                           @ [45]
	.word 0x09e3bdec                           @ [46]
	.word 0x09e3bde4                           @ [47]
	.word 0x09e3be3c                           @ [48]
	.word 0x09e3be3c                           @ [49]
banlist_handler_table:                         @ 0x09e58994 (3 THUMB fn-ptrs +1 + NULL sentinel; dispatch_banlist_scene_handler_frame)
	.word 0x08019661                           @ [0] dispatch_banlist_scene_handler+1 (THUMB)
	.word 0x0801a329                           @ [1] (handler+1, THUMB)
	.word 0x0801b5d9                           @ [2] tick_banlist_scene_frame+1 (THUMB)
	.word 0x00000000                           @ [3] NULL sentinel
	.incbin "roms/2343.gba", 0x1E589A4, 0x20     @ gap before sjis_char_fold_table (0x20 B)
sjis_char_fold_table:                            @ 0x09e589c4 (256B, 4 ROM refs; SJIS/ASCII char normalization: lowercase->uppercase fold + SJIS lead-byte remap)
	.incbin "roms/2343.gba", 0x1E589C4, 0x100   @ sjis_char_fold_table body (256 B)
card_type_alt_display_table:  @ 0x09e58ac4 (card type/display index mapping table, u16 pairs)
	.incbin "roms/2343.gba", 0x1E58AC4, 0x44    @ card_type_alt_display_table u16 pairs (0x44 B)
card_deck_fs_path_table:      @ 0x09e58b08 (deck FS path string pointer array; 100+ entries; 1 raw ref)
	.incbin "roms/2343.gba", 0x1E58B08, 0x204   @ card_deck_fs_path_table body (0x248-0x44=0x204 B)

@ Deck Record Table（原名 opponent_card_values，ROM偏移 0x1E58D0C - 0x1E59C2B）
@ 121 条 × 32 B = 0xF20 B = 3872 B (Opponent 27 + Theme 52 + Limited 42)
@ 代码访问: FUN_0801f3e8 base=0x09E58D0C stride=32 loop r1<=0x78
	.include "data/opponent-card-values.s"

@ 后 16MB 中间段：ROM偏移 0x1E59C2C - 0x1E5ABFB（deck record table 后，卡包卡牌列表前）
@ Carve A-C (Seg-9): campaign_oam_slot_count_table / pack_strip_tile_id_table / pack_card_grid_tile_table
	.incbin "roms/2343.gba", 0x1E59C2C, 0x10C      @ pre-table gap (0x1E59C2C..0x1E59D37)
campaign_oam_slot_count_table:                      @ 0x09e59d38: 29 halfword OAM slot counts (indexed mod-32)
	.incbin "roms/2343.gba", 0x1E59D38, 0x40       @ 29 slot counts + 6B pad
pack_strip_tile_id_table:                           @ 0x09e59d78: 8 halfword tile IDs for pack strip sprites
	.incbin "roms/2343.gba", 0x1E59D78, 0x10       @ 8 strip tile IDs
pack_card_grid_tile_table:                          @ 0x09e59d88: 16 halfword tile offsets for pack card grid
	.incbin "roms/2343.gba", 0x1E59D88, 0x20       @ 16 grid tile offsets
	.incbin "roms/2343.gba", 0x1E59DA8, 0xC        @ pre-aob_phase_table gap (f02 Seg-1 carve Host C)
aob_phase_table:                                @ 0x09E59DB4: AOB phase dispatch table (halfword stride 2, phase [0..7])
	.incbin "roms/2343.gba", 0x1E59DB4, 0x10   @ aob_phase_table body (8 halfwords, phase->offset)
deck_type_table:                                @ 0x09E59DC4: 8-entry u16 deck_type->sprite_tile_offset lookup (f02 Seg-2 carve)
	.incbin "roms/2343.gba", 0x1E59DC4, 0x10   @ deck_type_table (8 halfwords)
scene_scroll_table:                             @ 0x09E59DD4: 0x20-entry u16 symmetric scroll position table (f02 Seg-2 carve)
	.incbin "roms/2343.gba", 0x1E59DD4, 0xE28  @ scene_scroll_table + tail to host end 0x1E5ABFC

@ 卡包卡牌列表 + 信息表（ROM偏移 0x1E5ABFC - 0x1E5E617）
@ 45 个 pack 共 3515 条卡牌条目 + 51 条 pack 信息记录，共 0x3A1C 字节
	.include "data/pack-card-lists.s"

@ 后 16MB 中间段前部：ROM偏移 0x1E5E618 - 0x1E5ECD3（卡包信息表后，主菜单数据前）
@ Carve D-F (Seg-9): standard/expert/puzzle_challenge_record_array
	.incbin "roms/2343.gba", 0x1E5E618, 0x8         @ FS ptr pre-data (2 words: 0x09e495c0, 0x09e495cc)
standard_challenge_record_array:                    @ 0x09e5e620: 41 challenge records (stride 0xc)
	.incbin "roms/2343.gba", 0x1E5E620, 0x1EC       @ 41 x 12B = 0x1EC
expert_challenge_record_array:                      @ 0x09e5e80c: 35 challenge records
	.incbin "roms/2343.gba", 0x1E5E80C, 0x1A4       @ 35 x 12B = 0x1A4
	.incbin "roms/2343.gba", 0x1E5E9B0, 0x1C        @ gap between expert end and puzzle start
puzzle_challenge_record_array:                      @ 0x09e5e9cc: 49 challenge records
	.incbin "roms/2343.gba", 0x1E5E9CC, 0x24C       @ 49 x 12B = 0x24C
	.incbin "roms/2343.gba", 0x1E5EC18, 0xBC        @ remainder (0x1E5E618+0x6BC=0x1E5ECD4)

@ 主菜单 page table + sub-row 数组（ROM偏移 0x1E5ECD4 - 0x1E5EE13, 0x140 字节）
@ 6 子页 + sub-rows 结构化数据
	.include "data/main-menu.s"

@ 后 16MB 中间段后部：ROM偏移 0x1E5EE14 - 0x1E5EF2F（主菜单数据后，禁卡表前）
	.incbin "roms/2343.gba", 0x1E5EE14, 0x11C

@ 禁卡表数据 + Banlist Master Table（ROM偏移 0x1E5EF30 - 0x1E5F71B）
@ 8 个 banlist (487 条 × 4B) + master table (10 × 8B = 80 B), 共 0x7EC 字节
	.include "data/banlists.s"

@ 4 张未结构化数据表（master table 后，starter-deck 前; ROM 0x1E5F71C..0x1E5F883, 0x168 B）
@   level_signature_table 280 B + font_jp_dim/base/stride 80 B
	.include "data/post-banlists-tables.s"

@ 初始卡组数据（ROM偏移 0x1E5F884 - 0x1E5F8E9）
@ 50 张牌 + 终止符，共 0x66 字节
	.include "data/starter-deck.s"

@ 后 16MB 中间段：ROM偏移 0x1E5F8EA - 0x1E5FA57（初始卡组后，预组前）
	.incbin "roms/2343.gba", 0x1E5F8EA, 0x16E

@ 预组数据（ROM偏移 0x1E5FA58 - 0x1E5FD83）
@ 包含 6 个预组及其指针表，共 0x32C 字节
	.include "data/struct-decks.s"

@ 后 16MB 剩余部分：ROM偏移 0x1E5FD84 - 0x1E6468D（预组后，对手卡组前）
	.incbin "roms/2343.gba", 0x1E5FD84, 0x1408     @ 0x1E5FD84..0x1E6118C 文件路径表前

@ 内部文件路径表（ROM偏移 0x1E6118C - 0x1E63BE8）
@ 339 条 null 终止 ASCII 文件路径（deck/*.ydc, titleEx/*.LZncgr 等），共 10,844 字节
	.include "data/file-paths.s"

@ 内嵌文件系统索引表（ROM偏移 0x1E63BE8 - 0x1E64684）
@ offset_table (339 × u32) + size_table (340 × u32)，共 0xA9C 字节
	.include "data/fs-tables.s"

@ ROM 内嵌文件系统数据区（ROM偏移 0x1E64684 - 0x1ED4AA4，0x70420 B = 459,808 B）
@ 339 个文件 tight-pack 顺序：215 .ydc + 35 .ydq + 26 .LZ5bg + 18 .LZnclr + 17 .LZncgr + 14 .LZnanr + 14 .LZncer
@ 含 FID 339 orphan palette (title_obj_s.LZnclr, 208 B @ 0x1ED49D4，位于 szs[0] 声称的 0x70350 外)
@ 索引：data/fs-tables.s；路径：data/file-paths.s；文件体：fs/<原始路径>
@ 映射：path[i] ↔ FID[i+1]（见 tools/rom-export/export_fs_files.py）
	.include "data/fs-payload.s"

@ FS 后尾段：ROM 0x1ED4AA4 - 0x2000000（0x12B55C = 1,225,564 B，分析见 doc/dev/fs-tail-analysis.md）
	.incbin "roms/2343.gba", 0x1ED4AA4, 0x12B55C
