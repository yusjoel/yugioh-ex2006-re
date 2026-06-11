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
.equ gFsDecompBuf,               0x0200AF20  @ FS 解压暂存缓冲 (LZ77 bios_lz77_uncomp 目标)
                                             @ fs_load 用; dest in VRAM 时直接 huff/lz 写 VRAM, 否则
                                             @ 先解压到此 buf 再 cpu_copy_auto 到最终 dest
.equ gTextEncodingOverride,      0x0202348C  @ 1 B  文字编码覆盖标志 (TCG/OCG override)
                                             @ OCG(JP)模式下非0 → 强制单字节(TCG)计数路径
                                             @ 物理位于 gGlBlendState(0x02023480) 之后, 逻辑独立
                                             @ (blend 结构仅用 +0/+4/+8; 仅文字渲染族读此地址)

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
@ 名字输入 / Banlist 场景状态结构
@ -----------------------------------------------------------------------------
.equ gState,    0x02029250  @ name-input / banlist page state struct (804B cleared by NAME_INPUT_STATE_CPUSET_CTRL)
                             @ +0x8d = name display buffer (14B); +0x304 = scrollbar OAM slot;
                             @ 37 ROM refs; consumers: init_scrollbar_oam_slot_settings,
                             @   name_input_page_init, apply_sprite_gfx_by_type,
                             @   load_game_str_pair_1004_to_state, load_game_str_1006_to_state, ...

.equ gCardInfoPageState,         0x0201afb0  @ card info page per-frame state struct (EWRAM)
                                             @ +0x0  = u32 packed: bit0=page_active, bits[17:2]=card_id
                                             @ +0x4  = u16 page_step (0=init, 1/2/3=tick phases)
                                             @ +0x6  = u8  countdown_timer (tick update, non-zero decrements)
                                             @ +0x14 = u32 scroll_frame_counter (>0xe8 triggers scroll)
                                             @ +0x18 = u32 scroll_pixel_y_offset
                                             @ +0x1c = u32 scroll_sub_counter
                                             @ +0x20 = s16 scroll_offset_field (adjusted by display flags)
                                             @ 20 ROM refs; consumers: card_info_page_enter_with_card_id,
                                             @   card_info_page_init_bg0, render_card_name_to_line_buf,
                                             @   tick_scroll_frame_and_update_pos, update_card_info_page_state,
                                             @   render_card_stats_oam_for_current_card, tick_card_info_page_by_state

.equ gFontJpCtx, 0x02006ed0 @ JP font render context struct (~0x68B based on stride)
                              @ +0x4  = fn_ptr (indexed from font_jp_base_table by mode bits)
                              @ +0x8  = mode_flags (bit1=double-byte, bit2=? used by setup_font_jp_ctx_*)
                              @ +0x15 = active_flag (bit5=0x20 = glyph active)
                              @ 202 ROM refs; consumers: setup_font_jp_ctx_bg_vram_fixed,
                              @   setup_font_jp_ctx_obj_vram_row

@ -----------------------------------------------------------------------------
@ Demo 过场动画 (cinematic; demo/shuen, demo/exodia, demo/vija ...)
@ -----------------------------------------------------------------------------
.equ gVijaState,                 0x02029EB0  @ vija scene (play_ui_effect_3b) per-frame state struct (0xc0 bytes)
                                             @ +0x8c = u8  scroll_phase (vija BG3 horizontal scroll counter)
                                             @ +0x8d = u8  scene_main_state (10-phase state, run_vija_scene_state_machine)
                                             @ +0x90 = u8  bg2_affine_angle_counter (tick_bg2_affine_anim_frame)
                                             @ +0x91 = u8  bg_frame_cycle (mod 4, tick_bg_scroll_anim_frame)
                                             @ +0x98 = u8[5*8] slot_ctrl (5 OBJ anim slots * 8B each, tick_vija_obj_anim_slot)
                                             @ Consumers: reset_gl_display_state, load_vija_bg_gfx_embedded,
                                             @   load_vija_obj_resource_by_region, tick_vija_bg3_scroll_forward,
                                             @   tick_vija_bg3_scroll_backward, drive_vija_obj_cell_anim,
                                             @   tick_bg2_affine_anim_frame, tick_bg_scroll_anim_frame,
                                             @   get_vija_obj_slot_field8, tick_all_vija_obj_anim_slots,
                                             @   run_vija_scene_state_machine (file 01)

@ -----------------------------------------------------------------------------
@ 决斗场 / 卡牌显示 (Duel Field / Card Display) -- f01 Seg-5
@ -----------------------------------------------------------------------------
.equ gDuelFieldState,            0x02023130  @ duel field main state struct (large, ~0x400B; 170 raw refs)
                                             @ +0x21e = u8  fadein active flag (bit0)
                                             @ +0x222 = u8  prng anim flag (bit2 = prng-driven anim active)
                                             @ +0x226 = u8  scene entry complete flag (bit0)
                                             @ +0x220 = u32 OAM cache slot [0x88*4 into struct]
.equ gFontState,                 0x0201f440  @ font rendering global state (91 raw refs)
                                             @ confirmed from eval/080c7638.proposal.md: FONT_STATE_BASE=0x0201f440
.equ gDuelCtx,                   0x02020160  @ duel context base (95 raw refs)
                                             @ +0x2f51 = u8  zone display state flag (bit0)
                                             @ confirmed from eval/080d0c7c.md
.equ gDuelCardCtxBase,           0x0201e2a0  @ duel card activation context base (442 raw refs)
                                             @ +0x4  = u32 current_player (eors with 0/1 in dispatch_card_display_op)
                                             @ confirmed from eval/080566f4.proposal.md: ACTIVATION_STATE_BASE
.equ gCardFsDataBlock,           0x0201e2b4  @ card FS slot data block base (4 raw refs; stride=0x108 per slot)
.equ gCardIdCache,               0x0201ff60  @ EWRAM card id lookup/mapping cache (5 raw refs)
.equ gCardListDisplayBuf,        0x02001138  @ card list slot display buffer (12 raw refs)
@ Seg-9 alias: same address used as campaign handler_10 sprite row prototype source
.equ run_campaign_card_select_handler_10_proto_row, 0x02001138  @ alias for gCardListDisplayBuf (Seg-9 REF slot gas_label)
.equ gZoneActivTable,            0x020230f0  @ zone activation player table (1 ref; 2-word array [player0,player1])
                                             @ med-conf (single ref; semantics from indexing by player 0/1 context)
.equ gDuelSceneBase,             0x02023360  @ duel scene / campaign card-select scene base (192 raw refs)
                                             @ confirmed from eval/08028874.proposal.md: SCENE_BASE=0x02023360
.equ gCardCtxSlotData,           0x0201ff30  @ card context slot data base (29 raw refs)
                                             @ confirmed from eval/080c6240.proposal.md
.equ gP1ZoneHandCount,           0x0201c4ec  @ = gP1LifePoints+0xc; player zone/hand count table base (23 raw refs)
                                             @ confirmed from eval/08077678.md: LIST_A_BASE=0x0201c4ec

@ duel field state offsets
.equ DUEL_FIELD_FADEIN_FLAG_OFF,    0x21e   @ [gDuelFieldState+0x21e] bit0 = fadein active (31 raw refs)
.equ DUEL_FIELD_PRNG_ANIM_FLAG_OFF, 0x222   @ [gDuelFieldState+0x222] bit2 = prng-driven anim (111 raw refs)
.equ DUEL_FIELD_STATE_226_OFF,      0x226   @ [gDuelFieldState+0x226] bit0 = scene entry done (19 raw refs)
.equ DUEL_CTX_ZONE_STATE_OFF,       0x2f51  @ [gDuelCtx+0x2f51] bit0 = zone display active (25 raw refs)
.equ GPRNG_PRNG_STATE_OFF213,       0x213   @ [gPrng+0x213] bit7 = prng-anim state flag (37 raw refs)
.equ GPRNG_PRNG_STATE_OFF217,       0x217   @ [gPrng+0x217] bit7 = prng-anim LP flag (12 raw refs)
.equ GPRNG_BANNER_FLAG_OFF,         0x23f   @ [gPrng+0x23f] bit0 = banner-anim active (279 raw refs)
.equ P1LP_BLOCK2_OFF,               0x1d08  @ [gP1LifePoints+0x1d08] duel field LP display field (35 raw refs)
.equ P1LP_TIMER_OFF,                0x1cec  @ [gP1LifePoints+0x1cec] duel field timer field (29 raw refs)
.equ PLAYER_BLOCK_STRIDE,           0x868   @ player data block stride (0x868=2152 bytes; 2146 raw refs)
.equ GAME_STR_RAW_ID_MASK,     0xfffe0000   @ raw game string ID mask: bits[31:17]==0 (485 raw refs)

.equ gDuelDispCtx,               0x0203eeb0  @ display context struct for duel field / scene rendering
                                             @ passed to reset_display_and_obj_vram as r0 arg; stored at gPrng+0x1bc
                                             @ 8 ROM refs; callers: init_duel_field_icon_and_bg_vram + 7 others
                                             @ confidence: med (structural pattern; runtime fields unconfirmed)

@ =============================================================================
@ Seg-8 additions: campaign / card stats EWRAM globals and offsets
@ =============================================================================

@ gPrng offsets (pack display / challenge entry)
.equ GPRNG_CHALLENGE_ENTRY_OFF,   0x00006c3c  @ EWRAM+0x6c3c = challenge entry array base (4B per entry); 23 ROM refs
.equ GPRNG_PACK_SCROLL_OFF_23D,   0x0000023d  @ gPrng+0x23d pack scroll sync field; 27 ROM refs
.equ GPRNG_PACK_FRAME_OFF_23E,    0x0000023e  @ gPrng+0x23e pack frame control field; 29 ROM refs
@ NOTE: GPRNG_DISPLAY_OFF_226 = 0x226 -> same value as DUEL_FIELD_STATE_226_OFF (ewram.inc); reuse that constant

@ gSettings sub-struct offsets (render_text_with_font_type_select)
.equ GSETTINGS_FONT_TABLE_OFF,    0x000053f0  @ gSettings+0x53f0 = JP font pointer table; 10 ROM refs
.equ GSETTINGS_TEXT_FIELD_A_OFF,  0x00001250  @ gSettings+0x1250 = text render field A; med-conf; 3 ROM refs
.equ GSETTINGS_TEXT_FIELD_B_OFF,  0x00001267  @ gSettings+0x1267 = text render field B; med-conf; 3 ROM refs

@ P1 LP display block field
.equ P1LP_BLOCK2_OFF_1CE8,           0x1ce8  @ [gP1LifePoints+0x1ce8] LP display block2 field; 184 ROM refs

@ Campaign scene globals
.equ gCampaignDisplayState,       0x02029e90  @ campaign display state buffer (0x20 bytes); med-conf; 6 ROM refs
.equ gCampaignSpriteCtxBase,      0x02001250  @ campaign sprite context base; med-conf; 7 ROM refs

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

@ =============================================================================
@ file 02 Seg-1 additions: JP card name string table ptrs / campaign constants
@ =============================================================================

@ JP card name string table (init_card_name_result_screen uses lang-indexed branch)
.equ JP_LANG5_STR_BASE,             0x09DC0240  @ JP card name string table base (lang5=ES); 4 ROM refs
.equ JP_LANG5_STR_OFFSET_ES,        0x0003AB84  @ ES string offset from JP_LANG5_STR_BASE; 7 ROM refs
.equ JP_LANG4_STR_PTR_DE,           0x09DEF212  @ DE card name string ptr (lang4); 4 ROM refs
.equ JP_LANG3_STR_PTR_FR,           0x09DE2D5E  @ FR card name string ptr (lang3); 4 ROM refs
.equ JP_LANG2_STR_PTR_IT,           0x09DD69EC  @ IT card name string ptr (lang2); 4 ROM refs
.equ JP_LANG1_STR_PTR_EN,           0x09DCB012  @ EN card name string ptr (lang1); 4 ROM refs

@ Campaign BG layout constants
.equ CAMPAIGN_BG1CNT_INIT,          0x00000107  @ BG1CNT: pri=3 charbase=0 16col scrbase=0; 2 ROM refs
.equ CAMPAIGN_BG2CNT_INIT,          0x00000207  @ BG2CNT: pri=3 charbase=0 16col scrbase=1; 2 ROM refs
.equ CAMPAIGN_TILEMAP_SEQ_START,    0x0000F210  @ campaign BG tilemap seq start param; 2 ROM refs

@ =============================================================================
@ file 02 Seg-2 additions: duel field equip chain globals
@ =============================================================================
.equ gDuelFieldSlots,        0x0201c510  @ duel field zone slot array; player*0x868 + slot*0x14; 1007 raw refs
.equ gEquipNodePool,         0x0201d9c0  @ equip chain node pool; node_idx*8 stride; 55 raw refs
.equ gEquipChainSlotRefs,    0x0201bb90  @ equip chain slot reference array (replace_slot_chain_ref_by_id); 260 raw refs
.equ gDuelFieldSlotState,    0x0201c520  @ parallel slot state flags at gDuelFieldSlots+0x10; 51 raw refs
.equ gDuelEffectChainSlots,  0x0201bc54  @ effect context chain slot array (2 entries, stride 20B); 17 raw refs
                                         @ gEquipChainSlotRefs(0x0201bb90)+0xc4; distinct semantic domain (effect context chain)

@ =============================================================================
@ file 02 Seg-4 additions: zone-chain card_id table offset
@ =============================================================================
.equ ZONE_CHAIN_CARD_ID_OFF, 0x000010e2  @ offset from gP1LifePoints to zone-chain card_id table base
                                          @ (0x0201c4e0 + 0x10e2 = 0x0201d5c2); 21 raw ROM refs; 6 Seg-4 uses

@ =============================================================================
@ file 02 Seg-5 additions: player zone/hand/chain sub-arrays (find_zone_descriptor_by_slot_id)
@ =============================================================================
.equ gP1SlotCountBase,     0x0201c4f0  @ gP1LifePoints+0x10: slot set_code search count P1 base (12 ROM refs)
.equ gP1SlotSetCodeArray,  0x0201c740  @ gP1LifePoints+0x260: slot set_code data array P1 base (82 ROM refs)
.equ gP1HandCountBase,     0x0201c4f4  @ gP1LifePoints+0x14: hand slot count P1 base (11 ROM refs)
.equ gP1HandSlotArray,     0x0201c8f8  @ gP1LifePoints+0x418: hand slot data array P1 base (97 ROM refs)
.equ gP1ChainZoneCountBase, 0x0201c4f8 @ gP1LifePoints+0x18: chain zone count P1 base (2 ROM refs)
.equ gP1ChainZoneArray,    0x0201c880  @ gP1LifePoints+0x3a0: chain zone data array P1 base (21 ROM refs)
.equ gP1AltHandCountBase,  0x0201c4fc  @ gP1LifePoints+0x1c: alt-hand slot count P1 base (7 ROM refs)
.equ gP1AltHandSlotArray,  0x0201cab0  @ gP1LifePoints+0x5d0: alt-hand slot data array P1 base (15 ROM refs)

@ =============================================================================
@ file 02 Seg-7 additions: duel field slot P2 base
@ =============================================================================
.equ gDuelFieldSlots_p2_base, 0x0201c5d8  @ gDuelFieldSlots+0xc8 = slot[10] base for field9==2 single-slot path; 24 raw refs

@ =============================================================================
@ file 02 Seg-8 additions: field spell zone slot base
@ =============================================================================
.equ gDuelFieldSpellZoneBase, 0x0201c5ec  @ gDuelFieldSlots + 11*0x14 = P0 field-spell zone slot entry base; r10 base in check_slot_placement_blocked_by_field_effect; 6 raw refs

@ =============================================================================
@ file 03 Seg-1 additions: duel phase flags global
@ =============================================================================
.equ gDuelPhaseFlags,       0x0201b290  @ duel phase flags struct base; +0x4bc=phase lock byte, +0x594=effect entry count; 676 raw refs

@ =============================================================================
@ file 03 Seg-2 additions: effect entry array globals and player-block neg offsets
@ =============================================================================
.equ gEffectEntryArray,           0x0201b590  @ effect entry array base (stride=0x18, count at gDuelPhaseFlags+EFFECT_ENTRY_COUNT_OFF); 23 raw refs
.equ EFFECT_ENTRY_COUNT_OFF,      0x00000594  @ gDuelPhaseFlags+0x594 = effect entry count field; 9 raw refs
.equ HAND_ARRAY_TO_COUNT_NEG_OFF, 0xfffffbfc  @ gP1HandSlotArray(0x0201c8f8)+0xfffffbfc=gP1HandCountBase(0x0201c4f4); neg delta=-0x404 from hand slot array to hand count base; 5 raw refs
.equ ALT_HAND_ARRAY_TO_COUNT_NEG_OFF, 0xfffffa4c  @ gP1AltHandSlotArray(0x0201cab0)+0xfffffa4c=gP1AltHandCountBase(0x0201c4fc); neg delta=-0x5b4 from alt-hand slot array to alt-hand count base; 3 raw refs

@ =============================================================================
@ file 03 Seg-3 additions: field array C base global
@ =============================================================================
.equ gP1FieldArrayCBase,    0x0201c600  @ gP1LifePoints+0x120 (0x90<<1): field array C base ptr (zone_type=0xb, place_equip_card_if_type_matches); count at gP1ZoneHandCount (gP1LP+0x0c); 115 raw refs; 2 Seg-3 slots

@ =============================================================================
@ file 03 Seg-4b additions: hand slot offset + gP1FieldState direct address
@ =============================================================================
.equ HAND_COUNT_TO_SLOT_OFF,   0x00000404  @ positive offset from gP1HandCountBase(0x0201c4f4) to gP1HandSlotArray(0x0201c8f8); 1 Seg-4b slot (eval_hand_magicians path)
.equ gP1FieldState,            0x0201e1d4  @ gP1LifePoints(0x0201c4e0) + FIELD_STATE_OFF(0x1cf4) = direct abs addr for field state; 1 ROM ref (DAT_08039198)

@ =============================================================================
@ file 03 Seg-7 additions: duel event display sequence state + sprite attr buffer
@ =============================================================================
.equ gDuelDisplaySeqState,  0x0201bcc0  @ duel field event display sequence state buffer base; +0=event_code hword; +0x808=write_slot_idx; +0x80c=step_lock; 178 raw ROM refs
.equ gSpriteAttrBuf,        0x0201b870  @ sprite attribute buffer base (write_sprite_attr_record_entry); +0x300=filled_flags; +0x304/0x306/0x308/0x30a=attr0..3; 52 raw ROM refs

@ =============================================================================
@ file 03 Seg-8 additions: duel chain step counter + chain desc base + alt display seq state
@ =============================================================================
.equ gDuelChainStepCounter,   0x0201c4d0  @ equip chain removal/placement step counter; 3-state machine (0/1/2+); 8 raw ROM refs
.equ gDuelChainDescBase,      0x0201c4d8  @ equip chain zone slot descriptor / copy buffer base; zone placement and card-set display sequences; 22 raw ROM refs
.equ gDuelDisplaySeqStateAlt, 0x0201bcc2  @ alternate duel display seq state base = gDuelDisplaySeqState+2; used by alt zone-card-place and normal-summon functions; 3 raw ROM refs
