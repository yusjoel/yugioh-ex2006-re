# Refine Proposal: F16-Seg-1  [0x080c1448..0x080c2544)

## 段测绘

- 范围 4348B：1648 个 InstructionDB 共 3444B（1562 mnemonic + 86 `.hword`），210 个 word 共 840B，32 段 2B 零填充共 64B；连续覆盖且无 raw。

- `0x080c1448` `play_ui_effect_25`
- `0x080c17d4` `play_ui_effect_23`
- `0x080c1ad0` `play_ui_effect_13`
- `0x080c1c60` `play_ui_effect_2e`
- `0x080c1e9c` `play_ui_effect_2f`
- `0x080c1f10` `tick_pack_banner_3d_state_machine`
- `0x080c21a0` `tick_pack_banner_3d_state_machine_alt`

- 字面量词: 210; 自动源名: 155; 动作 EQ_ADD=43 / REF_ADD=58 / REF_PRESERVE=54 / PRESERVE=55。
- ROM_INCBIN / .byte: 0。段内无 raw 块。

## 数据块分类 (Rule 2/3)

本段无 ROM_INCBIN 或 .byte 块，因此 carve=0、disasm=0、§5.1=0。

## 符号化计划 (R1/R2/R3)

完整逐槽 before/after 合同见 `F16-Seg-1.slots.tsv`。155 个自动源名全部由 EQ_ADD、REF_ADD 或 REF_PRESERVE 消除；55 个 ANALYSIS switch 词保持命名空间、静态 ID、Data 类型和引用 CORE6。

### EQ_SLOTS

- `DUEL_FIELD_UI_EFFECT_FLAGS_OFF` = `0x00000215` (reuse `constants/duel_field.inc`): 0x080c17d0, 0x080c1acc, 0x080c1b94, 0x080c1c00, 0x080c1c5c, 0x080c1e44, 0x080c1e98, 0x080c1ed8
- `PLAYER_BLOCK_STRIDE` = `0x00000868` (reuse `constants/ewram.inc`): 0x080c14b4, 0x080c1c2c
- `WINOUT_OUTSIDE_ALL_OBJWIN_NO_EFFECTS` = `0x00001f3f` (reuse `constants/gba_io.inc`): 0x080c1fc4, 0x080c228c
- `VIJA_INTRO_WIN0H_BOUNDS` = `0x000028f0` (reuse `constants/duel_field.inc`): 0x080c1590, 0x080c18cc
- `OAM_ATTR2_TILE_C0_PAL4` = `0x000040c0` (reuse `constants/oam_attr.inc`): 0x080c1dbc, 0x080c205c, 0x080c20d8, 0x080c2140, 0x080c2318, 0x080c238c, 0x080c2408, 0x080c2470, 0x080c2508
- `OAM_ATTR2_TILE_C0_PAL4_PRI1` = `0x000044c0` (new `constants/oam_attr.inc`): 0x080c1d6c, 0x080c1e38
- `OAM_ATTR2_TILE_C0_PAL4_PRI2` = `0x000048c0` (reuse `constants/oam_attr.inc`): 0x080c2058, 0x080c20d4, 0x080c213c, 0x080c2314, 0x080c2388, 0x080c2404, 0x080c246c, 0x080c2504
- `GSETTINGS_OFFSET` = `0x00006c2c` (reuse `constants/name_input.inc`): 0x080c1cec, 0x080c1fb8, 0x080c21dc, 0x080c2218
- `DISPCNT_OBJWIN_CLEAR_MASK` = `0x00007fff` (new `constants/gba_io.inc`): 0x080c218c, 0x080c252c
- `DISPCNT_WIN0_CLEAR_MASK` = `0x0000dfff` (reuse `constants/gba_io.inc`): 0x080c1798, 0x080c1a94
- `AOB_MODE_TILE_BASE_512_PAL5` = `0x02000005` (reuse `constants/duel_field.inc`): 0x080c1b8c
- `SPARK_BLASTER_PACKED_CID_FIELD` = `0xc8480000` (new `constants/card_info.inc`): 0x080c14bc

### REF_SLOTS

- `EWRAM_BASE` = `0x02000000` (reuse `constants/gba_mem.inc`): 0x080c1ce8, 0x080c1fb4, 0x080c21d8, 0x080c2214
- `gDuelFieldSlots` = `0x0201c510` (reuse `constants/ewram.inc`): 0x080c14b8
- `gDuelCardCtxBase` = `0x0201e2a0` (reuse `constants/ewram.inc`): 0x080c1b0c
- `gDuelFieldState` = `0x02023130` (reuse `constants/ewram.inc`): 0x080c17cc, 0x080c1ac8, 0x080c1b90, 0x080c1bfc, 0x080c1c58, 0x080c1e40, 0x080c1e6c, 0x080c1e94, 0x080c1ed4, 0x080c1f0c
- `OBJ_PALRAM_SLOT_3` = `0x05000260` (reuse `constants/gba_mem.inc`): 0x080c1cf4, 0x080c1fa8, 0x080c2280
- `OBJ_PALRAM_SLOT_5` = `0x050002a0` (reuse `constants/gba_mem.inc`): 0x080c1b78
- `AOB_CARD_TILE_VRAM` = `0x06014000` (reuse `constants/gba_mem.inc`): 0x080c1b80, 0x080c1ce4, 0x080c1fb0, 0x080c2284
- `card_effect_count_panel_tile_vram_a` = `0x06014300` (new `constants/gba_mem.inc`): 0x080c1578, 0x080c18b0
- `card_effect_count_panel_tile_vram_b` = `0x06014340` (new `constants/gba_mem.inc`): 0x080c157c, 0x080c18b8
- `card_effect_count_digits_tile_vram` = `0x06014900` (new `constants/gba_mem.inc`): 0x080c1584, 0x080c18c0
- `switchD_080c14ac__switchdataD_080c14c4` = `0x080c14c4` (reuse_analysis `ANALYSIS switch namespace`): 0x080c14c0
- `switchD_080c156c__switchdataD_080c15a0` = `0x080c15a0` (reuse_analysis `ANALYSIS switch namespace`): 0x080c159c
- `switchD_080c180a__switchdataD_080c1814` = `0x080c1814` (reuse_analysis `ANALYSIS switch namespace`): 0x080c1810
- `switchD_080c18ac__switchdataD_080c18dc` = `0x080c18dc` (reuse_analysis `ANALYSIS switch namespace`): 0x080c18d8
- `switchD_080c1c80__switchdataD_080c1c8c` = `0x080c1c8c` (reuse_analysis `ANALYSIS switch namespace`): 0x080c1c88
- `switchD_080c1f2e__switchdataD_080c1f38` = `0x080c1f38` (reuse_analysis `ANALYSIS switch namespace`): 0x080c1f34
- `switchD_080c2210__switchdataD_080c2228` = `0x080c2228` (reuse_analysis `ANALYSIS switch namespace`): 0x080c2224
- `lp_digit_tile_rows` = `0x09851ffc` (reuse `constants/rom_data.inc`): 0x080c1588, 0x080c18c4
- `dual_list_count_panel_frame_tiles` = `0x09908124` (new `constants/rom_data.inc`): 0x080c18b4
- `card_effect_count_panel_frame_tiles_b` = `0x099081a4` (new `constants/rom_data.inc`): 0x080c1574
- `card_effect_count_panel_frame_tiles_a` = `0x09908224` (new `constants/rom_data.inc`): 0x080c1570
- `card_count_panel_label_tiles` = `0x099082a4` (new `constants/rom_data.inc`): 0x080c1580, 0x080c18bc
- `hand_shuffle_card_tile_rows` = `0x09908324` (new `constants/rom_data.inc`): 0x080c1b84
- `hand_shuffle_palette` = `0x09909324` (new `constants/rom_data.inc`): 0x080c1b7c
- `hand_shuffle_ptnsect` = `0x09909344` (new `constants/rom_data.inc`): 0x080c1b88
- `normal_summon_palette` = `0x0990940c` (new `constants/rom_data.inc`): 0x080c1cf8
- `normal_summon_tile_rows` = `0x0990942c` (new `constants/rom_data.inc`): 0x080c1cf0
- `pack_banner_palette_a` = `0x09912e3c` (new `constants/rom_data.inc`): 0x080c1fac, 0x080c2054, 0x080c20d0
- `pack_banner_tile_rows_a` = `0x09912e5c` (new `constants/rom_data.inc`): 0x080c1fbc
- `pack_banner_alt_a_palette` = `0x0991765c` (new `constants/rom_data.inc`): 0x080c21e4
- `pack_banner_alt_a_tile_rows` = `0x0991767c` (new `constants/rom_data.inc`): 0x080c21e0
- `pack_banner_alt_b_palette` = `0x0991be7c` (new `constants/rom_data.inc`): 0x080c2220
- `pack_banner_alt_b_tile_rows` = `0x0991be9c` (new `constants/rom_data.inc`): 0x080c221c
- `attack_flip_debug_format` = `0x09e491fc` (new `constants/rom_data.inc`): 0x080c1f08

### RENAME_SLOTS

54 个 REF_PRESERVE 槽保留既有 DATA 引用并改为语义源名；完整源名、EOL、引用和目标静态身份见 TSV。55 个 PRESERVE switch 词不写 Ghidra。

### FUNC_RENAME

- `0x080c1448` `play_ui_effect_25` -> `play_card_effect_count_delta_window_effect`; indeg=1; full-ROM even/Thumb holds=0/0; high confidence.
- `0x080c17d4` `play_ui_effect_23` -> `play_card_count_increment_window_effect`; indeg=1; full-ROM even/Thumb holds=0/0; high confidence.
- `0x080c1ad0` `play_ui_effect_13` -> `play_hand_shuffle_display_effect`; indeg=1; full-ROM even/Thumb holds=0/0; high confidence.
- `0x080c1c60` `play_ui_effect_2e` -> `play_normal_summon_card_display_effect`; indeg=1; full-ROM even/Thumb holds=0/0; high confidence.
- `0x080c1e9c` `play_ui_effect_2f` -> `play_attack_flip_card_display_effect`; indeg=1; full-ROM even/Thumb holds=0/0; high confidence.

### PLATE

- `0x080c1448` full rewrite (486 ASCII chars): `UI effect 0x25 card-effect count window. Reads side/slot, signed delta and style from gBannerState; gets the zone count. Spark Blaster maps count to3-count and negates delta. Phase0 loads card/panel tiles and enables WIN0. Phase2 draws count-delta for17 calls; phase3 steps toward count using ++u16counter>>4; phase4 holds count for17 calls. Phases1/5 write five BLDY steps. Phase6 disables WIN0 and refreshes UI, returning1. Default clears banner bit0 and field+0x215 bit2, returning0.`
- `0x080c17d4` full rewrite (467 ASCII chars): `UI effect 0x23 card-count increment window. Let b=gBannerState. b+8 supplies count; b+0xc feeds the card cache. Phase0 loads panel/card tiles, selects the slot bucket and enables WIN0. Phase2 draws count-1 for17 calls. Phase3 holds count-1 for31 calls then draws count on call32; phase4 holds count for17 calls. Phases1/5 each write five BLDY steps. Phase6 clears WIN0 and refreshes UI. Phases0..6 return1; default clears banner bit0 and field+0x215 bit2, returning0.`
- `0x080c1ad0` full rewrite (391 ASCII chars): `UI effect 0x13 hand-shuffle display. Phase 0 selects the side-dependent position, uploads the hand-shuffle palette and tiles, initializes the AOB context, sets the duel-field UI flag, and redraws the hand slot. Phase 1 renders and advances the AOB and later clears that flag. Phase 2 redraws the field-zone card tile. Other phases clear banner and UI flags and return 0; phases 0-2 return 1.`
- `0x080c1c60` full rewrite (414 ASCII chars): `UI effect 0x2e normal-summon display. Let b=gBannerState and f=gDuelFieldState. Phase0 loads language-selected tiles/palette and enables alpha blending. Phases1..3 each attempt two OAM writes per call, for9/33/9 calls. Phase3's last call clears f+0x215 bit2. Phase4 increments u8 f+0xa and stores (u8(b+4)<<8)|u8(b+8) at f+0xc+4*(b+0xc-1). Phases0..4 return1; default clears banner bit0 and field bit2, returning0.`
- `0x080c1e9c` full rewrite (368 ASCII chars): `UI effect 0x2f attack-flip display. Phase0 calls suppress_display_output with the debug format, then return_void_noop; it decrements u8 gDuelFieldState+0xa, clears the u32 entry at +0xc+4*(gBannerState+0xc-1), advances phase and returns1. Later calls clear gBannerState bit0 with AND0xfe and gDuelFieldState+0x215 bit2 with AND0xfb, preserving field bit0, and return0.`
- `0x080fa4cc` external full rewrite (352 ASCII chars): `Release-build four-argument display-output stub. Pushes r0-r3, immediately restores sp, and returns without output or side effects. Callers include banlist/settings setup, play_attack_flip_card_display_effect, dump_nclr_palette_entries, and tick_sio_deck_sync_round. This is the parameter-taking output-suppression member of the adjacent no-op cluster.`
- `0x080fa4d8` external full rewrite (319 ASCII chars): `Release-build zero-argument no-op. Executes only bx lr. Four call sites invoke it immediately after suppress_display_output: play_attack_flip_card_display_effect, tick_sio_deck_sync_session, init_system_hardware_and_drivers, and init_anim_state_with_ptnsect. Unlike suppress_assert_report, it has no prepared arguments.`

Registry 持久化合同精确覆盖 7 个既存 `RENAMES` tuple：5 个函数 tuple 同步 name+PLATE，`suppress_display_output`/`return_void_noop` 两个 tuple 仅同步 comment；key/index 保持且不新增 tuple。

两个 pack-banner state machine 的现有 ASCII PLATE 精确保留。外部 `play_ui_effect` 的 PLATE 不含五个旧名，故不写 PLATE；仅投影其五条 BL 文本和 body-reference 派生目标名。`suppress_display_output` 与 `return_void_noop` 的旧 PLATE 各含 `play_ui_effect_2f`，按完整 ASCII 文本订正；Function 名、ID、body、ABI 不变。`return_void_handler@080fa4d4` 经只读查询确认不含旧名，完全排除于写入范围。

## 新增 constants / 全局

- `constants/oam_attr.inc`: `OAM_ATTR2_TILE_C0_PAL4_PRI1 = 0x000044c0`
- `constants/gba_io.inc`: `DISPCNT_OBJWIN_CLEAR_MASK = 0x00007fff`
- `constants/card_info.inc`: `SPARK_BLASTER_PACKED_CID_FIELD = (SPARK_BLASTER_CID << 19)`
- `constants/gba_mem.inc`: `card_effect_count_panel_tile_vram_a = 0x06014300`
- `constants/gba_mem.inc`: `card_effect_count_panel_tile_vram_b = 0x06014340`
- `constants/gba_mem.inc`: `card_effect_count_digits_tile_vram = 0x06014900`
- `constants/rom_data.inc`: `dual_list_count_panel_frame_tiles = 0x09908124`
- `constants/rom_data.inc`: `card_effect_count_panel_frame_tiles_b = 0x099081a4`
- `constants/rom_data.inc`: `card_effect_count_panel_frame_tiles_a = 0x09908224`
- `constants/rom_data.inc`: `card_count_panel_label_tiles = 0x099082a4`
- `constants/rom_data.inc`: `hand_shuffle_card_tile_rows = 0x09908324`
- `constants/rom_data.inc`: `hand_shuffle_palette = 0x09909324`
- `constants/rom_data.inc`: `hand_shuffle_ptnsect = 0x09909344`
- `constants/rom_data.inc`: `normal_summon_palette = 0x0990940c`
- `constants/rom_data.inc`: `normal_summon_tile_rows = 0x0990942c`
- `constants/rom_data.inc`: `pack_banner_palette_a = 0x09912e3c`
- `constants/rom_data.inc`: `pack_banner_tile_rows_a = 0x09912e5c`
- `constants/rom_data.inc`: `pack_banner_alt_a_palette = 0x0991765c`
- `constants/rom_data.inc`: `pack_banner_alt_a_tile_rows = 0x0991767c`
- `constants/rom_data.inc`: `pack_banner_alt_b_palette = 0x0991be7c`
- `constants/rom_data.inc`: `pack_banner_alt_b_tile_rows = 0x0991be9c`
- `constants/rom_data.inc`: `attack_flip_debug_format = 0x09e491fc`

## carve 计划 (R7)

无。

## disasm 计划 (R4)

无。

## §5.1 登记 (Rule 3)

无。

## 消费者证据 (R6)

- `asm/16_duelfield_zone.s:6-461`: effect 0x25 七相窗口、Spark Blaster packed CID、计数差值反转、WIN0/BLDY 清理；high。
- `asm/03_equip_chain_hand.s:18129`: effect 0x25 调用方传入 side/slot/delta/style；窗口显示 count-delta 并收束至 count；high。
- `asm/16_duelfield_zone.s:464-841`: effect 0x23 使用 banner+8 的 count-1→count 七相窗口；high。
- `asm/03_equip_chain_hand.s:21100`: dual-list 调用方的返回值进入 banner+0xc 卡缓存参数；显示量来自独立 banner+8 count；high。
- `asm/16_duelfield_zone.s:844-1047`: effect 0x13 上传 hand-shuffle 资源、初始化 AOB、更新手牌/场地区域显示；high。
- `asm/03_equip_chain_hand.s:22098`: `tick_hand_shuffle_display_seq` 发起 effect 0x13；high。
- `asm/16_duelfield_zone.s:1050-1341`: effect 0x2e language-selected 资源、alpha/OAM 五相流程、独立 u8 count++ 及按 banner+0xc-1 索引写 packed entry；high。
- `asm/04_card_zone_sprite.s:943`: `tick_card_normal_summon_display_state` 发起 effect 0x2e；high。
- `asm/16_duelfield_zone.s:1344-1402`: effect 0x2f suppressed debug、u8 count递减、按 banner+0xc-1 清 packed entry、banner bit0 与 field bit2 分别清理；high。
- `asm/04_card_zone_sprite.s:991`: `tick_flip_attack_display_state` 发起 effect 0x2f；high。
- `asm/21_font_title_scene.s:14761,14773`: two no-op stub PLATEs contain the stale `play_ui_effect_2f` name; high。

## 求助

- none

## Executor Report: F16-Seg-1

- 槽: EQ=43 REF_ADD=58 REF_PRESERVE=54 PRESERVE=55 FUNC_RENAME=5 PLATE_WRITE=7。
- carve=0 disasm=0 §5.1=0。
- 新增 constants/全局: 3 Equates + 19 address labels。
- 求助: none。
- proposal: `doc/dev/refine/F16-Seg-1.proposal.md`。
