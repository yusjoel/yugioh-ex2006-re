@ =============================================================================
@ EWRAM 变量符号常量
@ 数据来源: refs/datacrystal-um2006/ram-map.md
@           （TCRF Data Crystal wiki 的反汇编结论）
@
@ 用法: 在汇编里改写裸 .word 0x02029810 → ldr rN, =gBanlistPasswordBuffer
@      （或新代码里直接 ldr rN, =符号名）
@ =============================================================================

@ -----------------------------------------------------------------------------
@ 系统设置
@ -----------------------------------------------------------------------------
.equ gSettings,                  0x02006C2C  @ 1 B  各种设置；低 3 位为语言 ID
                                             @ language_id: 0=JP 1=EN 2=DE 3=FR 4=IT 5=ES

@ -----------------------------------------------------------------------------
@ 进度 / 数据
@ -----------------------------------------------------------------------------
.equ gMoneyDp,                   0x02006C38  @ 4 B  Money (DP)

.equ gDuelPuzzleProgress,        0x02006C3C  @ 140 B  35 × 4B
                                             @ byte0 bit1=Completed bit2=Failed
                                             @ 全 0 = sentinel 0x34BB13 (未完成)

.equ gLimitedDuelProgress,       0x02006CC8  @ 164 B  41 × 4B
                                             @ 0 = 未解锁；其余同上

.equ gThemeDuelScores,           0x02006D6C  @ 200 B  50 × 4B
                                             @ byte0 低 2 位为完成标志，其他位 + byte1..3 = high score

@ -----------------------------------------------------------------------------
@ 玩家 / 对手
@ -----------------------------------------------------------------------------
.equ gPlayerName,                0x02006E48  @ 14 B  玩家名（CP1252）
.equ gPlayerIcon,                0x02006E57  @ 1 B   玩家图标 ID（见 refs Notes）

.equ gUnlockedDuelists,          0x02006E5C  @ 8 B   已解锁对手位图

@ 对各 CPU 胜场（4 B 各，连续 27 项 = 108 B 总长，从 0x02006E60）
.equ gWinsBase,                  0x02006E60
.equ gWinsKuriboh,               0x02006E60
.equ gWinsScapegoat,             0x02006E64
.equ gWinsSkullServant,          0x02006E68
.equ gWinsWatapon,               0x02006E6C
.equ gWinsWhiteMagicianPikeru,   0x02006E70
.equ gWinsBatterymanC,           0x02006E74
.equ gWinsOjamaYellow,           0x02006E78
.equ gWinsGoblinKing,            0x02006E7C
.equ gWinsDesFrog,               0x02006E80
.equ gWinsWaterDragon,           0x02006E84
.equ gWinsRedEyesDarknessDragon, 0x02006E88
.equ gWinsVampireGenesis,        0x02006E8C
.equ gWinsInfernalFlameEmperor,  0x02006E90
.equ gWinsOceanDragonLord,       0x02006E94
.equ gWinsHeliosDuoMegiste,      0x02006E98
.equ gWinsGilfordTheLegend,      0x02006E9C
.equ gWinsDarkEradicatorWarlock, 0x02006EA0
.equ gWinsGuardianExode,         0x02006EA4
.equ gWinsGoldd,                 0x02006EA8
.equ gWinsElementalHeroErikshieler, 0x02006EAC
.equ gWinsRavielLordOfPhantasms, 0x02006EB0
.equ gWinsHorusLv8,              0x02006EB4
.equ gWinsStronghold,            0x02006EB8
.equ gWinsSacredPhoenix,         0x02006EBC
.equ gWinsCyberEndDragon,        0x02006EC0
.equ gWinsPlayer,                0x02006EC4
.equ gWinsCopycat,               0x02006EC8

@ -----------------------------------------------------------------------------
@ 决斗运行时
@ -----------------------------------------------------------------------------
.equ gP1LifePoints,              0x0201C4E0  @ 2 B  P1 LP
.equ gP2LifePoints,              0x0201CD48  @ 2 B  P2 LP

@ -----------------------------------------------------------------------------
@ Banner 动画 (出/入场 overlay)
@ -----------------------------------------------------------------------------
.equ gBannerState,               0x0201FEC0  @ banner 出/入场动画状态结构
                                             @ +0x0  = u8  flag (default 路径清 bit 1)
                                             @ +0x10 = u8  main state (0..6 → default)
                                             @ +0x11 = u8  sub-counter (帧计数)
                                             @ 共用者: banner_anim_state_machine (7-state 主体)
                                             @          FUN_080be600 (5-state 配对模式)

@ -----------------------------------------------------------------------------
@ UI 特效派发器 (play_ui_effect / FUN_0801ef94)
@ -----------------------------------------------------------------------------
.equ gUIEffectState,             0x02023110  @ UI 特效派发器状态结构
                                             @ +0x0  = u16 step (主状态机步数)
                                             @ +0x4  = u32 packed param (常 = card_ref)
                                             @ +0x8  = u32 mode flag
                                             @ +0x18 = u8  sub_tick (帧计数, case 内 4-tick 子循环)
                                             @ +0x19 = u8  cleanup bit field
                                             @ 共用者: play_ui_effect (FUN_0801ef94) ~28 个 effect handler
                                             @ 注: gPageState @ +0x20 (0x02023130) 是相邻另一结构

@ -----------------------------------------------------------------------------
@ GL 亮度/混合 (fade/blend) 状态结构 (源 GL/GL_Common.c)
@ -----------------------------------------------------------------------------
.equ gGlBlendState,              0x02023480  @ GL 屏幕亮度/alpha-blend 淡入淡出控制块
                                             @ +0x0  = s8  blend1 当前系数 (history)
                                             @ +0x1  = s8  blend1 目标系数 [-16..16]
                                             @ +0x2  = u8  blend 模式位 (BLDCNT 目标, 常 0x3f)
                                             @ +0x4  = s8  blend2 当前系数 (history)
                                             @ +0x5  = s8  blend2 目标系数 [0..16]
                                             @ +0x6  = u8  blend2 模式位
                                             @ +0x8  = u32 打包控制字:
                                             @         bits[1:0]   = 标志 (bit0 active / bit1 fade)
                                             @         bits[9:2]   = blend1 step (当前帧步)
                                             @         bits[17:10] = blend2 step (目标帧步)
                                             @ 共用者: gl_set_brightness / gl_set_blend2_level /
                                             @         init_blend_transition_params(_ex) /
                                             @         check/tick_blend_transition_step
                                             @ 注: 紧邻 GL 调色板管理区 (0x02023490, gl_state_init 用)

@ -----------------------------------------------------------------------------
@ GL 主状态结构 (palette/OAM manager; 源 GL/GL_Oam.c, GL/IG2D_Main.c)
@ -----------------------------------------------------------------------------
.equ gGlState,                   0x02023490  @ GL 子系统主状态结构 (0x8ac B; gl_state_init 清 0)
                                             @ +0x000 = OAM/affine 条目区 (0x20 B/条, get_gl_oam_entry_ptr)
                                             @          兼 fill_gl_palram_buf_0xf0 填充区 (+0..+0x400)
                                             @ +0x400 = palette entry 区 (8 B/条, alloc_palette_entry_slot)
                                             @ +0x800 = slot_record[ ] (1 B/条; slot_idx->prev)
                                             @ +0x880 = palette_map[ ] (1 B/条; palette_entry->slot, 初值 0xff)
                                             @ +0x8a0 = s8 slot 分配计数器
                                             @ 共用者: get_gl_oam_entry_ptr / gl_state_init /
                                             @         init_gl_palette_slot_flags / fill_gl_palram_buf_0xf0 /
                                             @         assign_palette_slot_entry / alloc_palette_entry_slot /
                                             @         copy_sprite_attr_table_to_oam
                                             @ 注: 各 consumer 对 +0x880 等偏移语义解读略有出入, 待运行时核实

@ NNS G2D cell animation bank (源 GL/IG2D_Main.c; alloc_cell_anim_slot 分配)
.equ gIg2dCellAnmBank,           0x02027D40  @ CellAnmBank: 0x40 条 × 0x54 B (slot=base+count*0x54)

@ -----------------------------------------------------------------------------
@ 输入 / Banlist
@ -----------------------------------------------------------------------------
.equ gPlayerNameEntry,           0x02029512  @ 14 B  名字输入缓冲

.equ gBanlistPasswordBuffer,     0x02029810  @ 1440 B  禁卡密码输入
                                             @ 每 2 B 一项: [charset][character_id]

@ -----------------------------------------------------------------------------
@ 主菜单 (main menu page state)
@ -----------------------------------------------------------------------------
.equ gMenuState,                 0x02029590  @ 主菜单状态结构
                                             @ +0x0  = u32 ptr 到 main_menu_page_table (ROM 0x09E5ED24)
                                             @ +0xb  = u8 bits[6:4] = current page idx (0..5)
                                             @ 服务者: FUN_080e7e0c (主菜单 page state machine)
                                             @ 6 子页: Deck Edit / Free Duel / Challenge! /
                                             @         Get Cards / Forb-Ltd Card Lists / Options

@ -----------------------------------------------------------------------------
@ Demo 过场动画 (cinematic; demo/shuen, demo/exodia, demo/vija ...)
@ -----------------------------------------------------------------------------
.equ gDemoState,                 0x02029EC0  @ demo 过场动画状态结构
                                             @ +0x88 = u32 fs_load 返回的解压数据指针
                                             @ +0x8c = u32 packed bitfield
                                             @         bit 0      = done flag
                                             @         bits 9..16 = main state (0..6)
                                             @ +0x8e = u16 sub-state (low byte 频繁用)
                                             @ +0x90 = u8  bit field
                                             @ +0x94 = u32 frame counter
                                             @ 已知用户: demo_shuen_state_machine
                                             @ (其它 demo/exodia, demo/vija 等可能复用)
