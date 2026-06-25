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
.equ P1LP_BACKUP_DST_OFF,           0x1cf0  @ [gP1LifePoints+0x1cf0] LP timer backup destination field; tick_card_display_op0b_seq copies gP1LP+0x1cec here when slot_idx==0; 5 aligned ROM refs
@ file 04 Seg-3: LP card-tracking array offsets (gP1LifePoints-relative)
.equ LP_CARD_TRACK_BASE_OFF,  0x00001da8  @ [gP1LifePoints+0x1da8] LP card-ref tracking array base; written by get_zone_slot_card_ref_by_type; cleared by tick_card_display_op2b_lp_clear_seq; 109 raw ROM refs
.equ LP_CARD_TRACK_NEXT_OFF,  0x00001daa  @ [gP1LifePoints+0x1daa] 5-entry hword clear loop base; tick_card_display_op2b_lp_clear_seq strh x5 starting here; 44 raw ROM refs
.equ LP_CARD_TRACK_ALT_OFF,   0x00001dac  @ [gP1LifePoints+0x1dac] LP card-track array alt word at base+4; tick_equip_lp_type18_display_seq 3rd LP-delta summand; 4 raw ROM refs (0x0807cc9c, 0x080a2164, 0x080a21a0, 0x080a21e4)
.equ LP_CARD_TRACK_AUX_OFF,   0x00001db2  @ [gP1LifePoints+0x1db2] auxiliary LP track field cleared separately; 1 raw ROM ref
.equ PLAYER_BLOCK_STRIDE,           0x868   @ player data block stride (0x868=2152 bytes; 2146 raw refs)
.equ P2_ZONE1_LP_OFF,              0x87c   @ [gP1LifePoints+0x87c] P2 zone-1 LP region start; 0x87c = PLAYER_BLOCK_STRIDE(0x868) + 0x14 (one zone slot stride); check_spell_zone_chain_occupied_eligible loads [gP1LifePoints+0x87c]; conf: med
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
.equ P2LP_BLOCK2_OFF_1CF4,           0x1cf4  @ [gP1LifePoints+0x1cf4] P2 LP display block2 field (opponent analog of P1LP_BLOCK2_OFF_1CE8=0x1ce8); enqueue_spirit_monster_zone_sprite_otohime opponent LP compare; distinct from FIELD_STATE_OFF=0x1cf4 (base=gDuelFieldSlots vs gP1LifePoints); 103 raw ROM refs

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
.equ gDuelFieldSlotsEffectZoneBase, 0x0201d5b4  @ gDuelFieldSlots+EFFECT_ZONE_PARTITION_OFF(0x10a4); effect zone partition base; 2 raw ROM refs (0x080478f0, 0x0805b888)
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

@ =============================================================================
@ file 04 Seg-4 additions: LP discard zone tracking + equip chain entry base
@ =============================================================================
.equ LP_DISCARD_ZONE_OFF,           0x000010dc  @ [gP1LifePoints+player*0x868+0x10dc] LP discard zone tracking field; tick_card_discard_display_seq stores zone_type here on seq completion; 11 ROM refs; 1 Seg-4 slot
.equ gEquipChainEntryBase,          0x0201e288  @ EWRAM equip chain entry/depth base (3 ROM refs); tick_equip_attach_display_sequence iterates [0x0201e288+2*i] for chain node depth table

@ =============================================================================
@ file 04 Seg-8a additions: equip bitmap counter offset + equip zone count table
@ =============================================================================
.equ P1LP_EQUIP_BITMAP_CTR_OFF,     0x00001d3c  @ [gP1LP+player*PLAYER_BLOCK_STRIDE+0x1d3c] modulo-10 equip-slot bitmap anim frame counter; 6 ROM refs; update_duel_field_slot_sprite_state
.equ gEquipZoneCountTable,          0x0201e1c8  @ equip zone count tracking table base (EWRAM); 55 ROM refs; apply_nitro_unit_equip_activation loop
.equ gEquipLpActivBitmap,           0x0201e220  @ LP activation zone-hit bitmap base (EWRAM); read as [base+0] u32 zone-occupation word in tick_equip_activation_lp_display_seq state 0x7e; 3 ROM refs (0x08074ab0, 0x0809d690, 0x080a3490); adjacent gEquipZoneCountTable+0x58; conf: med

@ =============================================================================
@ file 05 Seg-2 additions: LP bar animation counter/state offsets
@ Relative to gDuelPhaseFlags (0x0201b290)
@ =============================================================================
.equ LP_BAR_DISPLAY_CTR_OFF,   0x000004c4  @ [gDuelPhaseFlags+0x4c4] LP bar animation display counter; incremented by increment_lp_bar_display_counter/increment_lp_bar_counter_no_player; decremented by decrement_lp_bar_display_counter; 18 raw ROM refs; Seg-2
.equ LP_BAR_ANIM_STATE_OFF,    0x000004cc  @ [gDuelPhaseFlags+0x4cc] LP bar animation state reset field; cleared to 0 when display counter first reaches 1 (initial anim trigger path); 37 raw ROM refs; Seg-2

@ =============================================================================
@ file 05 Seg-5 additions: card sprite row / equip eligibility state machine offsets
@ gDuelPhaseFlags-relative (base=0x0201b290):
@ =============================================================================
.equ SPRITE_ROW_ENTRY_DATA_OFF,  0x000004d4  @ [gDuelPhaseFlags+0x4d4] byte array for card sprite row entry flag data; init_card_sprite_row_entry iterates count(LP_BAR_ANIM_STATE_OFF) entries; 25 ROM refs
.equ ELIGIB_STATE_OFF,           0x00000574  @ [gDuelPhaseFlags+0x574] dispatch_card_eligibility_state_machine state word [0..0x1f]; indexes 32-entry switch table; 18 ROM refs
@ NOTE: ELIGIB_RESULT_OFF=0x584 has same numeric value as GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF in duel_field.inc
@   but they are DIFFERENT fields: ELIGIB_RESULT_OFF is gDuelPhaseFlags+0x584 (eligibility result: 0=pending,1=confirmed),
@   while GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF is gPrng+0x1c0_deref+0x584. Benign numeric collision; independent constants.
.equ ELIGIB_RESULT_OFF,          0x00000584  @ [gDuelPhaseFlags+0x584] eligibility result field; 0=pending, 1=confirmed; written by caseD_14/15/1f; 20 ROM refs
@ gP1LifePoints-relative (base=0x0201c4e0):
.equ ELIGIB_CARD_ID_OFF,         0x00001d44  @ [gP1LifePoints+0x1d44] card_id field accessed in dispatch_card_eligibility_state_machine caseD_1f; 9 ROM refs
.equ ELIGIB_STATE_CTRL_OFF,      0x00001d54  @ [gP1LifePoints+0x1d54] eligibility state control word; written to state values (0, 0xa, 0x1e etc.) by various cases; 33 ROM refs
.equ ELIGIB_ACT_COUNT_OFF,       0x00001d58  @ [gP1LifePoints+0x1d58] activation count field; written r0=1 in caseD_b; 16 ROM refs
.equ ELIGIB_ACT_TYPE_OFF,        0x00001d5c  @ [gP1LifePoints+0x1d5c] activation type flag; cmp r0,#3 in caseD_b determines branch; 17 ROM refs
.equ ELIGIB_SPRITE_CTRL_OFF,     0x00001d68  @ [gP1LifePoints+0x1d68] sprite display control; 0=display 0x61 attr, non-0=use 0x8061 hidden attr for enqueue_sprite_attr_record; 105 ROM refs
.equ ELIGIB_ANIM_STATE_OFF,      0x00001d6c  @ [gP1LifePoints+0x1d6c] animation state index; range check [0..0xf] in caseD_1f with thresholds 0xb/0xf; 56 ROM refs
.equ LP_BANISHER_CTX_OFF,        0x00001d70  @ [gP1LifePoints+0x1d70] banisher zone LP context field; adjacent to ELIGIB_SPRITE_CTRL_OFF(+0x1d68) +8 and ELIGIB_ANIM_STATE_OFF(+0x1d6c) +4; 39 ROM refs; F06 Seg-7 (tick_equip_zone_target_lp_step2_off x2)
.equ LP_ACTIVATION_PENDING_OFF,  0x00001d40  @ [gP1LifePoints+0x1d40] LP activation pending flag; computed inline as movs r1,#0xea; lsls r1,r1,#0x5 = 0xea<<5; written by tick_equip_lamp/dream zone state machines; 9 fns in F10 Seg-9; C5 grep=0 (new); conf: high

@ =============================================================================
@ file 05 Seg-6 additions: sprite row queue/anim subsystem offsets + equip zone rank state
@ Relative to gDuelPhaseFlags (base=0x0201b290):
@ =============================================================================
.equ SPRITE_ROW_WRITE_PTR_OFF,   0x00000480  @ [gDuelPhaseFlags+0x480] write ptr into row buffer (strh); flush_sprite_row_queue_partial; 2 ROM refs Seg-6a
.equ SPRITE_ROW_COUNT_OFF,       0x00000488  @ [gDuelPhaseFlags+0x488] row entry count (halfword); flush_sprite_row_queue_partial count at +0x488; 2 ROM refs Seg-6a
.equ SPRITE_ROW_ANIM_STATE_OFF,  0x0000048c  @ [gDuelPhaseFlags+0x48c] anim-active state flag (str); dispatch_equip_field_update_by_anim_state anim_state_offset=0x48c; 12 ROM refs Seg-6a
.equ SPRITE_ROW_QUEUE_STATE_A_OFF, 0x00000490  @ [gDuelPhaseFlags+0x490] queue phase-A state (cleared by flush); flush_sprite_row_queue_partial clears +0x490; 4 ROM refs Seg-6a
.equ SPRITE_ROW_ANIM_CTL_OFF,   0x00000494  @ [gDuelPhaseFlags+0x494] anim state code (0..0xe); dispatch_sprite_row_anim_by_state reads [base+0x494] as state code; 6 ROM refs Seg-6a
.equ SPRITE_ROW_QUEUE_ACTIVE_OFF, 0x00000498  @ [gDuelPhaseFlags+0x498] queue active flag (str); dispatch_equip_field_update_by_anim_state queue_state_offset=0x498; 4 ROM refs Seg-6a
.equ SPRITE_ROW_QUEUE_STATE_OFF, 0x0000049c  @ [gDuelPhaseFlags+0x49c] queue state code (0..0x67); dispatch_sprite_row_queue_by_state uses [base+0x49c] for index; 5 ROM refs Seg-6a
.equ EQUIP_PHASE_FRAME_OFF,      0x000004a4  @ [gDuelPhaseFlags+0x4a4] dragon-summon/equip effect phase frame counter; adjacent to phase code node +0x4a0 (=0x94<<3); 241 ROM refs; Seg-2 tick_dragon_summon_effect_display_state_machine

@ New global: equip zone rank state struct (EWRAM)
.equ gEquipZoneRankState,   0x0201e4d0  @ EWRAM base for equip zone rank state machine; advance_equip_zone_rank_state reads halfword [+0x14]; 1 ROM ref Seg-6a (DAT_0804f368)

@ =============================================================================
@ file 05 Seg-8 additions: equip chain node card array offset
@ Relative to gDuelPhaseFlags (base=0x0201b290):
@ =============================================================================
.equ CHAIN_NODE_CARD_ARR_OFF,  0x000004f4  @ [gDuelPhaseFlags+0x4f4] card pointer array for equip chain node list; check_equip_slot_eligible_by_card_id_pair (0x080513d0) chain node traversal; Seg-9 comment confirms OFFSET_CARD_ARR=0x4f4; 1 Seg-8 slot

@ =============================================================================
@ file 06 Seg-1 additions: equip chain slot ref struct field offsets
@ Relative to gEquipChainSlotRefs (base=0x0201bb90):
@ =============================================================================
.equ EQUIP_CTX_PLAYER_OFF,    0x00000000  @ [gEquipChainSlotRefs+0x0] activation player id field; check_equip_slot_eligible_by_opposite_side_and_effect_ctx ldr/cmp vs r5(player_id); asm/02 plate confirms activation_player_offset=0; 1 F06 Seg-1 ref
.equ EQUIP_CTX_SLOT_REF_OFF,  0x0000001c  @ [gEquipChainSlotRefs+0x1c] context zone slot reference field; check_equip_slot_eligible_by_opposite_side_and_effect_ctx ldr/cmp vs r4(zone_idx); asm/02 plate confirms context_slot_ref_offset=0x1c; 1 F06 Seg-1 ref

@ =============================================================================
@ file 07 Seg-4 additions: equip dispatch context sub-structure
@ =============================================================================
.equ gDuelEquipCtx,    0x0201bbbc  @ equip dispatch context struct (= gEquipChainSlotRefs+0x2c, stride=0x38 per player); check_equip_slot_at_turn_player_side indexes [+8]/[+1c]; 1 Seg-4 slot

@ =============================================================================
@ file 07 Seg-5 additions: LP slot/hand offset constants
@ =============================================================================
.equ LP_SLOT_ACTIVE_OFF,        0x00000010  @ [gP1LifePoints+player*0x868+0x10] LP slot activation count; nonzero = LP slot active/present; ~10 Seg-5 uses
.equ LP_LOOP_CEIL_OFF,          0x0000000c  @ [gP1LifePoints+player*0x868+0x0c] LP slot count ceiling for loop bounds; ~7 Seg-5 uses
.equ HAND_SLOT_TO_ZONE_COUNT_NEG_OFF, 0xfffffbf4  @ gP1HandSlotArray(0x0201c8f8)+0xfffffbf4=gP1ZoneHandCount(0x0201c4ec); neg delta -0x40c; distinct from HAND_ARRAY_TO_COUNT_NEG_OFF=-0x404; 1 Seg-5 slot DWORD_0805feac

@ =============================================================================
@ file 07 Seg-7 additions: LP gap threshold constant
@ =============================================================================
.equ LP_GAP_THRESHOLD_7000,          0x00001b58  @ LP gap threshold 7000 (0x1b58=7000 decimal); check_equip_slot_eligible_by_lp_gap_7000_vs_opponent: opponent LP must exceed player LP by at least 7000; Seg-7 DWORD_080618b0

@ =============================================================================
@ file 08 Seg-5 additions: equip LP zone entry base + OAM entry attr
@ =============================================================================
.equ gEquipLpZoneEntryBase,  0x0201e500  @ EWRAM base for equip LP zone entry descriptor buffer; dispatch_equip_lp_field_state_by_card_id reads [+0] for card_type bits for sprite_code selection; 28 raw ROM refs across 0x0806xxxx/0807xx/0809xx/080axx/080bxx/080cxx; (Seg-5 name; Seg-6 may refine)
.equ EQUIP_OAM_ENTRY_ATTR_14F8, 0x000014f8  @ OAM entry attr word OR component; dispatch_equip_slot_sprite_by_lp_state_neo_daedalus: lsls r1,r1,#0xd; orrs r1,EQUIP_OAM_ENTRY_ATTR_14F8; sp[0x4] = combined attr; then bl setup_equip_oam_entry_with_sprite_attr; 2 ROM code refs (conf: med; exact OAM attr structure TBD)

@ =============================================================================
@ file 08 Seg-6 additions: LP activation link flag offset (gP1LifePoints domain)
@ Source: asm/08_equip_oam_neodaed.s, Seg-6 (0x080690dc..0x0806a118)
@ Domain exception: same value as EFFECT_ZONE_BITMASK_OFF=0x10d0 (duel_field.inc, base=gDuelFieldSlots)
@ =============================================================================
.equ LP_ACTIVATION_LINK_FLAG_OFF,  0x000010d0  @ [gP1LifePoints+0x10d0] activation link flag; bit0+bit1 tested for LP link status in tick_equip_activation_sprite_with_lp_row_state_machine; asm/08 L12689; domain=gP1LifePoints (distinct from EFFECT_ZONE_BITMASK_OFF=0x10d0 base=gDuelFieldSlots)

@ =============================================================================
@ file 09 Seg-1 additions: LP display field offsets (gP1LifePoints domain)
@ Source: asm/09_equip_lp_display.s, Seg-1 (0x0806e76c..0x0806ff50)
@ =============================================================================
.equ LP_D_TRIBE_BLOCK_OFF,  0x00001ce4  @ [gP1LifePoints+0x1ce4] D.Tribe LP score field; enqueue_slot_sprites_by_card_id_scoring D_TRIBE_CID(0x15ae) path reads dword here as scoring param; adjacent to P1LP_BLOCK2_OFF_1CE8(0x1ce8)-4; 2 aligned ROM refs; conf:med
.equ LP_P2_LOOP_CEIL_OFF,   0x00000874  @ [gP1LifePoints+0x874] P2 LP loop ceiling = PLAYER_BLOCK_STRIDE(0x868) + LP_LOOP_CEIL_OFF(0xc); tick_lp_zone_sprite_display_seq state 0x80 reads P2 ceil at this offset; 7 aligned ROM refs; conf:high

@ =============================================================================
@ file 09 Seg-5a additions: equip chain base offset (gP1FieldArrayCBase domain)
@ Source: asm/09_equip_lp_display.s, Seg-5a (0x08072d20..0x08073a5c)
@ =============================================================================
.equ EQUIP_CHAIN_BASE_OFF, 0x00001c88  @ [gP1FieldArrayCBase(0x0201c600)+0x1c88] = gEquipChainEntryBase(0x0201e288); setup_equip_oam_by_placeable_card_id_and_zone + tick_neo_daedalus_equip_display_seq use offset to reach chain entry array; conf: high

@ =============================================================================
@ file 09 Seg-8 additions: hand spell slot offset (gGraveyardSlots domain)
@ Source: asm/09_equip_lp_display.s, Seg-8 (0x0807629c..0x0807738c)
@ =============================================================================
.equ HAND_SPELL_SLOT_CC8_OFF, 0x00000cc8  @ [gGraveyardSlots+player*PLAYER_BLOCK_STRIDE+slot_idx*4+0xcc8] hand-spell slot set_code subfield; read as ldrh+lsls#19+lsrs#19 = bits[12:0]; 9 raw ROM refs; enqueue_hand_spell_sprite_with_slot_count; conf: med

@ =============================================================================
@ file 10 Seg-5b additions: equip display ROM table base + zone entry offset
@ Source: asm/10_equip_effect_dispatch.s, Seg-5b (0x0807ec10..0x0807f730)
@ find_equip_display_entry_by_card_id / dispatch_equip_zone_sprite_shape_b_by_state
@ C5 grep 0x000005cc in constants/: 0 hits; grep 0x09e59e14 in constants/: 0 hits
@ =============================================================================
.equ ZONE_ENTRY_OFFSET_5CC,       0x000005cc  @ zone slot entry base offset in dispatch_equip_zone_sprite_shape_b_by_state; gP1LifePoints + player*PLAYER_BLOCK_STRIDE + 0x5cc; 5 ROM refs; conf: med
.equ EQUIP_DISPLAY_ROM_TABLE_BASE, 0x09e59e14 @ ROM read-only equip display entry table; 86 entries stride 8B [cid(u16), criteria0..2(u16 x3)]; 1 ROM ref (find_equip_display_entry_by_card_id); conf: high

@ =============================================================================
@ file 10 Seg-6 additions: gDuelPhaseFlags sub-field absolute labels (equip criteria)
@ Source: asm/10_equip_effect_dispatch.s, Seg-6 (0x0807f730..0x08080ba0)
@ All are gDuelPhaseFlags(0x0201b290) + field offset; C5 grep 0x0201b830/38/50: 0 hits each
@ =============================================================================
gDuelPhaseFlags_criteria_count = 0x0201b830  @ gDuelPhaseFlags+0x5a0: equip criteria count for display loop; push_to_effect_slot_array + build_equip_criteria_for_target_slots; x2 slots; conf: high
gDuelPhaseFlags_set_f_flag     = 0x0201b838  @ gDuelPhaseFlags+0x5a8: set-f category flag for equip criteria; build_equip_criteria_for_target_slots + push_to_effect_slot_array; x3 slots; conf: high
gDuelPhaseFlags_criteria_arr_base = 0x0201b850  @ gDuelPhaseFlags+0x5c0: base addr of equip criteria array block; build_equip_slot_criteria_from_card_range; x1 slot; conf: high

@ =============================================================================
@ file 11 Seg-1 additions: gDuelPhaseFlags slot display type / LP bar row fields
@ Source: asm/11_effect_slot_puzzletext.s, Seg-1 (0x080850d8..0x08085d4c)
@ All are gDuelPhaseFlags(0x0201b290) + field offset; C5 grep verified: 0 hits each
@ =============================================================================
.equ SLOT_DISPLAY_TYPE_OFF,   0x000004b0  @ [gDuelPhaseFlags+0x4b0] slot display type selector; dispatch_equip_slot_display_by_type_scarr 0x96<<3=0x4b0; 6-way dispatch cmp r0,#5; 35 ROM refs; C5 grep=0 (new); conf: high
.equ LP_BAR_ROW_COUNT_OFF,    0x000004c8  @ [gDuelPhaseFlags+0x4c8] LP bar row count word; submit_lp_bar_sprite_row_by_type 0x99<<3=0x4c8; incremented up to 0x20; 5 ROM refs; C5 grep=0 (new); conf: high
.equ LP_BAR_ROW_ACTIVE_OFF,   0x000004d0  @ [gDuelPhaseFlags+0x4d0] LP bar row active flag; 0x9a<<3=0x4d0; cmp r1,#0 skip-if-nonzero; adjacent LP_BAR_ANIM_STATE_OFF(0x4cc) and SPRITE_ROW_ENTRY_DATA_OFF(0x4d4); 8 ROM refs; C5 grep=0 (new); conf: high
.equ LP_BAR_ROW_XCOORD_OFF,   0x000004d3  @ [gDuelPhaseFlags+count+0x4d3] per-row x-coord byte array; strb r4,[r0] writes x_coord; adjacent SPRITE_ROW_ENTRY_DATA_OFF(0x4d4); 22 ROM refs; C5 grep=0 (new); conf: high
.equ FIELD_DISPLAY_TYPE_OFF,  0x0000057c  @ [gDuelPhaseFlags+0x57c] field display type code; build_sprite_row_from_zone_state + dispatch_field_display_state_by_type; 7 ROM refs; C5 grep=0 (new); conf: high
