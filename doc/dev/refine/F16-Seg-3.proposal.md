# Refine Proposal: F16-Seg-3 [0x080c36a8..0x080c4350)

状态: 首版分析冻结, 等独立 reviewer 审查. 本稿没有运行 Ghidra, 没有构建或提交. 上一段已经提交 `6dcda7ccfb73b8bd487d8f13f6eb260d2411991e`.
原生 before: `output/refine-run-20261028-105948/root-f16-seg3-independent-prestate-v2.json`, SHA256 `0ce1a03fa217373404c81b6da27622376616fe5d11bf58dcd148f15f399a177e`. 直接原生观测162个 Function, 3837个完整状态, 模块1580个池字/505个目标/43716个逐字节单位/48个外部保护单位. 全 Program Function 数5414保持. 指令属性25823个真实 PC, 不是按THUMB半字推算.

## 段测绘

- 范围3240B, 本段12个既有 Function, 98个池字, 76个残留自动名, 原始块0. 按当前活动文档第五节严格接续Seg-2, 不提前处理Seg-4的数据块.
- 所有98个池字在 slots.tsv 和 slot-plan.json 完整列出 old/final symbols, data/instruction, bytes/value, tmode, references, Equates, owners 和全部五类注释. 22个 ANALYSIS switch字严格保留, 没有data重建.
| entry | name before -> after | true body bytes | indeg | source |
|---|---|---:|---:|---|
| 0x080c36a8 | `write_palette_tile_row_to_vram` -> `initialize_duel_field_slot_tilemap` | 212 | 1 | asm/16_duelfield_zone.s:4551 |
| 0x080c3790 | `get_field_slot_tile_vram_addr` -> `get_field_slot_tile_vram_addr` | 92 | 6 | asm/16_duelfield_zone.s:4676 |
| 0x080c3840 | `blit_field_slot_tile_with_palette_hi` -> `copy_field_slot_bg_tile_pattern` | 58 | 1 | asm/16_duelfield_zone.s:4760 |
| 0x080c3880 | `update_field_slot_tile_display` -> `update_field_slot_tile_display` | 74 | 11 | asm/16_duelfield_zone.s:4796 |
| 0x080c38cc | `render_field_slot_card_tile` -> `render_field_slot_card_tile` | 258 | 8 | asm/16_duelfield_zone.s:4835 |
| 0x080c39fc | `render_field_zone_card_tile_by_type` -> `render_field_zone_card_tile_by_type` | 282 | 7 | asm/16_duelfield_zone.s:4998 |
| 0x080c3b50 | `render_field_zone_mini_card_tiles` -> `render_zone_list_scroll_arrows` | 396 | 2 | asm/16_duelfield_zone.s:5180 |
| 0x080c3d00 | `init_field_slot_ctx_zoom` -> `init_field_slot_ctx_zoom` | 26 | 1 | asm/16_duelfield_zone.s:5417 |
| 0x080c3d20 | `play_card_zoom_in` -> `play_card_zoom_in` | 870 | 1 | asm/16_duelfield_zone.s:5435 |
| 0x080c40e0 | `init_field_slot_aob_ctx_d` -> `init_field_slot_render_request` | 62 | 1 | asm/16_duelfield_zone.s:5932 |
| 0x080c412c | `render_field_slot_card_tile_by_id` -> `render_field_slot_card_tile_by_id` | 224 | 1 | asm/16_duelfield_zone.s:5972 |
| 0x080c4220 | `refresh_player_field_slot_tiles` -> `refresh_player_field_slot_tiles` | 268 | 8 | asm/16_duelfield_zone.s:6089 |

### 全部98个池字及自动名槽

| slot | before symbol | raw value | action | final label | expression | READ consumers |
|---|---|---|---|---|---|---|
| 0x080c36f8 | `DAT_080c36f8` | 0x0600e800 | REF_ADD | `ptr_bg_screenblock_29_base_080c36f8` | `BG_SCREENBLOCK_29_BASE` | asm/16_duelfield_zone.s:4557 |
| 0x080c36fc | `DAT_080c36fc` | 0x09e49254 | REF_ADD | `ptr_duel_field_zone_tile_coords_080c36fc` | `duel_field_zone_tile_coords` | asm/16_duelfield_zone.s:4570 |
| 0x080c3700 | `DAT_080c3700` | 0x09e49258 | REF_ADD | `ptr_duel_field_zone_tile_y_coords_080c3700` | `duel_field_zone_tile_y_coords` | asm/16_duelfield_zone.s:4573 |
| 0x080c3788 | `DAT_080c3788` | 0x05000020 | REF_ADD | `ptr_bg_palram_slot_1_080c3788` | `BG_PALRAM_SLOT_1` | asm/16_duelfield_zone.s:4658 |
| 0x080c378c | `DAT_080c378c` | 0x08510460 | REF_ADD | `ptr_shared_ui_palette_256_080c378c` | `shared_ui_palette_256` | asm/16_duelfield_zone.s:4661 |
| 0x080c37b4 | `DAT_080c37b4` | 0x080c37b8 | REF_ADD | `ptr_switch_d_080c37b2_switchdata_d_080c37b8_080c37b4` | `switchD_080c37b2__switchdataD_080c37b8` | asm/16_duelfield_zone.s:4692 |
| 0x080c37b8 | `switchD_080c37b2::switchdataD_080c37b8` | 0x080c37fc | PRESERVE | `switchD_080c37b2::switchdataD_080c37b8` | `0x080c37fc` |  |
| 0x080c37bc | `(none)` | 0x080c37fc | PRESERVE | `None` | `0x080c37fc` |  |
| 0x080c37c0 | `(none)` | 0x080c37fc | PRESERVE | `None` | `0x080c37fc` |  |
| 0x080c37c4 | `(none)` | 0x080c37fc | PRESERVE | `None` | `0x080c37fc` |  |
| 0x080c37c8 | `(none)` | 0x080c37fc | PRESERVE | `None` | `0x080c37fc` |  |
| 0x080c37cc | `(none)` | 0x080c3802 | PRESERVE | `None` | `0x080c3802` |  |
| 0x080c37d0 | `(none)` | 0x080c3802 | PRESERVE | `None` | `0x080c3802` |  |
| 0x080c37d4 | `(none)` | 0x080c3802 | PRESERVE | `None` | `0x080c3802` |  |
| 0x080c37d8 | `(none)` | 0x080c3802 | PRESERVE | `None` | `0x080c3802` |  |
| 0x080c37dc | `(none)` | 0x080c3802 | PRESERVE | `None` | `0x080c3802` |  |
| 0x080c37e0 | `(none)` | 0x080c380e | PRESERVE | `None` | `0x080c380e` |  |
| 0x080c37e4 | `(none)` | 0x080c380e | PRESERVE | `None` | `0x080c380e` |  |
| 0x080c37e8 | `(none)` | 0x080c3808 | PRESERVE | `None` | `0x080c3808` |  |
| 0x080c37ec | `(none)` | 0x080c3808 | PRESERVE | `None` | `0x080c3808` |  |
| 0x080c37f0 | `(none)` | 0x080c3808 | PRESERVE | `None` | `0x080c3808` |  |
| 0x080c37f4 | `(none)` | 0x080c3808 | PRESERVE | `None` | `0x080c3808` |  |
| 0x080c37f8 | `(none)` | 0x080c380c | PRESERVE | `None` | `0x080c380c` |  |
| 0x080c3828 | `DAT_080c3828` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c3828` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:4735 |
| 0x080c382c | `DAT_080c382c` | 0x060031c0 | REF_ADD | `ptr_duel_field_opp_slot_tile_vram_080c382c` | `DUEL_FIELD_OPP_SLOT_TILE_VRAM` | asm/16_duelfield_zone.s:4742 |
| 0x080c383c | `DAT_080c383c` | 0x06000040 | REF_ADD | `ptr_bg_screen_row1_off_080c383c` | `BG_SCREEN_ROW1_OFF` | asm/16_duelfield_zone.s:4750 |
| 0x080c387c | `DAT_080c387c` | 0x09854df0 | REF_ADD | `ptr_field_slot_bg_tile_pattern_080c387c` | `field_slot_bg_tile_pattern` | asm/16_duelfield_zone.s:4769 |
| 0x080c3954 | `PTR_card_image_index_080c3954` | 0x095b5c00 | REF_PRESERVE | `ptr_card_image_index_080c3954` | `card_image_index` | asm/16_duelfield_zone.s:4877 |
| 0x080c3958 | `DAT_080c3958` | 0x080000ae | REF_ADD | `ptr_rom_region_code_addr_080c3958` | `ROM_REGION_CODE_ADDR` | asm/16_duelfield_zone.s:4880 |
| 0x080c395c | `DAT_080c395c` | 0x02000000 | REF_ADD | `ptr_ewram_base_080c395c` | `EWRAM_BASE` | asm/16_duelfield_zone.s:4885 |
| 0x080c3960 | `DAT_080c3960` | 0x00006c2c | EQ_ADD | `gsettings_offset_080c3960` | `GSETTINGS_OFFSET` | asm/16_duelfield_zone.s:4886 |
| 0x080c3964 | `DAT_080c3964` | 0x093264c0 | REF_ADD | `ptr_card_mini_frame_second_half_tile_data_080c3964` | `card_mini_frame_second_half_tile_data` | asm/16_duelfield_zone.s:4903 |
| 0x080c39a0 | `PTR_card_image_index_080c39a0` | 0x095b5c00 | REF_PRESERVE | `ptr_card_image_index_080c39a0` | `card_image_index` | asm/16_duelfield_zone.s:4916 |
| 0x080c39a4 | `DAT_080c39a4` | 0x080000ae | REF_ADD | `ptr_rom_region_code_addr_080c39a4` | `ROM_REGION_CODE_ADDR` | asm/16_duelfield_zone.s:4920 |
| 0x080c39a8 | `DAT_080c39a8` | 0x02000000 | REF_ADD | `ptr_ewram_base_080c39a8` | `EWRAM_BASE` | asm/16_duelfield_zone.s:4925 |
| 0x080c39ac | `DAT_080c39ac` | 0x00006c2c | EQ_ADD | `gsettings_offset_080c39ac` | `GSETTINGS_OFFSET` | asm/16_duelfield_zone.s:4926 |
| 0x080c39b0 | `PTR_card_mini_frame_tile_data_080c39b0` | 0x09326280 | REF_PRESERVE | `ptr_card_mini_frame_tile_data_080c39b0` | `card_mini_frame_tile_data` | asm/16_duelfield_zone.s:4943 |
| 0x080c39f8 | `DAT_080c39f8` | 0x0984fbcc | REF_ADD | `ptr_card_mini_frame_fallback_tile_data_080c39f8` | `card_mini_frame_fallback_tile_data` | asm/16_duelfield_zone.s:4963 |
| 0x080c3a38 | `DAT_080c3a38` | 0x0984fbcc | REF_ADD | `ptr_card_mini_frame_fallback_tile_data_080c3a38` | `card_mini_frame_fallback_tile_data` | asm/16_duelfield_zone.s:5029 |
| 0x080c3a6c | `DAT_080c3a6c` | 0x02023130 | REF_ADD | `ptr_g_duel_field_state_080c3a6c` | `gDuelFieldState` | asm/16_duelfield_zone.s:5036 |
| 0x080c3a70 | `DAT_080c3a70` | 0x00000215 | EQ_ADD | `duel_field_ui_effect_flags_off_080c3a70` | `DUEL_FIELD_UI_EFFECT_FLAGS_OFF` | asm/16_duelfield_zone.s:5037 |
| 0x080c3a74 | `DAT_080c3a74` | 0x00000868 | EQ_ADD | `player_block_stride_080c3a74` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:5053 |
| 0x080c3a78 | `DAT_080c3a78` | 0x0201c740 | REF_ADD | `ptr_g_p1_slot_set_code_array_080c3a78` | `gP1SlotSetCodeArray` | asm/16_duelfield_zone.s:5055 |
| 0x080c3a90 | `DAT_080c3a90` | 0x00000868 | EQ_ADD | `player_block_stride_080c3a90` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:5071 |
| 0x080c3a94 | `DAT_080c3a94` | 0x0201c8f4 | REF_ADD | `ptr_g_p1_zone14_card_word_base_080c3a94` | `gP1Zone14CardWordBase` | asm/16_duelfield_zone.s:5075 |
| 0x080c3b24 | `DAT_080c3b24` | 0x00000868 | EQ_ADD | `player_block_stride_080c3b24` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:5092 |
| 0x080c3b28 | `DAT_080c3b28` | 0x0201caac | REF_ADD | `ptr_g_p1_zone15_card_word_base_080c3b28` | `gP1Zone15CardWordBase` | asm/16_duelfield_zone.s:5096 |
| 0x080c3b2c | `PTR_card_image_index_080c3b2c` | 0x095b5c00 | REF_PRESERVE | `ptr_card_image_index_080c3b2c` | `card_image_index` | asm/16_duelfield_zone.s:5107 |
| 0x080c3b30 | `DAT_080c3b30` | 0x080000ae | REF_ADD | `ptr_rom_region_code_addr_080c3b30` | `ROM_REGION_CODE_ADDR` | asm/16_duelfield_zone.s:5110 |
| 0x080c3b34 | `DAT_080c3b34` | 0x02000000 | REF_ADD | `ptr_ewram_base_080c3b34` | `EWRAM_BASE` | asm/16_duelfield_zone.s:5115 |
| 0x080c3b38 | `DAT_080c3b38` | 0x00006c2c | EQ_ADD | `gsettings_offset_080c3b38` | `GSETTINGS_OFFSET` | asm/16_duelfield_zone.s:5116 |
| 0x080c3b3c | `PTR_card_mini_frame_tile_data_080c3b3c` | 0x09326280 | REF_PRESERVE | `ptr_card_mini_frame_tile_data_080c3b3c` | `card_mini_frame_tile_data` | asm/16_duelfield_zone.s:5133 |
| 0x080c3c38 | `DAT_080c3c38` | 0x02023130 | REF_ADD | `ptr_g_duel_field_state_080c3c38` | `gDuelFieldState` | asm/16_duelfield_zone.s:5187, asm/16_duelfield_zone.s:5240 |
| 0x080c3c3c | `DAT_080c3c3c` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c3c3c` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:5203, asm/16_duelfield_zone.s:5266 |
| 0x080c3c40 | `DAT_080c3c40` | 0x00000868 | EQ_ADD | `player_block_stride_080c3c40` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:5213, asm/16_duelfield_zone.s:5254 |
| 0x080c3c44 | `DAT_080c3c44` | 0x0201c4ec | REF_ADD | `ptr_g_p1_zone_hand_count_080c3c44` | `gP1ZoneHandCount` | asm/16_duelfield_zone.s:5215, asm/16_duelfield_zone.s:5256 |
| 0x080c3c48 | `DAT_080c3c48` | 0x0300024c | REF_ADD | `ptr_tick_campaign_card_selector_oam_attr_buf_080c3c48` | `tick_campaign_card_selector_oam_attr_buf` | asm/16_duelfield_zone.s:5228 |
| 0x080c3c4c | `DAT_080c3c4c` | 0x03000186 | REF_ADD | `ptr_g_key_input_held_080c3c4c` | `gKeyInputHeld` | asm/16_duelfield_zone.s:5296 |
| 0x080c3c64 | `DAT_080c3c64` | 0x03000186 | REF_ADD | `ptr_g_key_input_held_080c3c64` | `gKeyInputHeld` | asm/16_duelfield_zone.s:5319 |
| 0x080c3cfc | `DAT_080c3cfc` | 0x03000186 | REF_ADD | `ptr_g_key_input_held_080c3cfc` | `gKeyInputHeld` | asm/16_duelfield_zone.s:5358 |
| 0x080c3d1c | `DAT_080c3d1c` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c3d1c` | `gUIEffectState` | asm/16_duelfield_zone.s:5421 |
| 0x080c3e04 | `DAT_080c3e04` | 0x02023114 | REF_ADD | `ptr_g_ui_effect_args_080c3e04` | `gUIEffectArgs` | asm/16_duelfield_zone.s:5442 |
| 0x080c3e08 | `DAT_080c3e08` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c3e08` | `gUIEffectState` | asm/16_duelfield_zone.s:5443, asm/16_duelfield_zone.s:5539 |
| 0x080c3e0c | `DAT_080c3e0c` | 0x00000868 | EQ_ADD | `player_block_stride_080c3e0c` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:5457 |
| 0x080c3e10 | `DAT_080c3e10` | 0x0201c510 | REF_ADD | `ptr_g_duel_field_slots_080c3e10` | `gDuelFieldSlots` | asm/16_duelfield_zone.s:5462 |
| 0x080c3e14 | `DAT_080c3e14` | 0x080c3e18 | REF_ADD | `ptr_switch_d_080c3e02_switchdata_d_080c3e18_080c3e14` | `switchD_080c3e02__switchdataD_080c3e18` | asm/16_duelfield_zone.s:5546 |
| 0x080c3e18 | `switchD_080c3e02::switchdataD_080c3e18` | 0x080c3e2c | PRESERVE | `switchD_080c3e02::switchdataD_080c3e18` | `0x080c3e2c` |  |
| 0x080c3e1c | `(none)` | 0x080c3e5c | PRESERVE | `None` | `0x080c3e5c` |  |
| 0x080c3e20 | `(none)` | 0x080c3ecc | PRESERVE | `None` | `0x080c3ecc` |  |
| 0x080c3e24 | `(none)` | 0x080c4030 | PRESERVE | `None` | `0x080c4030` |  |
| 0x080c3e28 | `(none)` | 0x080c40a8 | PRESERVE | `None` | `0x080c40a8` |  |
| 0x080c3ec8 | `DAT_080c3ec8` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c3ec8` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:5596 |
| 0x080c3f00 | `DAT_080c3f00` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c3f00` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:5659 |
| 0x080c3f04 | `DAT_080c3f04` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c3f04` | `gUIEffectState` | asm/16_duelfield_zone.s:5673 |
| 0x080c3f2c | `DAT_080c3f2c` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c3f2c` | `gUIEffectState` | asm/16_duelfield_zone.s:5684 |
| 0x080c3f84 | `DAT_080c3f84` | 0x09e493b4 | REF_PRESERVE | `ptr_rom_card_zoom_anim_curve_080c3f84` | `rom_card_zoom_anim_curve` | asm/16_duelfield_zone.s:5708 |
| 0x080c3f88 | `DAT_080c3f88` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c3f88` | `gUIEffectState` | asm/16_duelfield_zone.s:5712 |
| 0x080c3f8c | `DAT_080c3f8c` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c3f8c` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:5723 |
| 0x080c4028 | `DAT_080c4028` | 0x09e5f8f0 | REF_PRESERVE | `ptr_rom_sin_table_q8_080c4028` | `rom_sin_table_q8` | asm/16_duelfield_zone.s:5760 |
| 0x080c402c | `DAT_080c402c` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c402c` | `gUIEffectState` | asm/16_duelfield_zone.s:5762, asm/16_duelfield_zone.s:5821 |
| 0x080c40a4 | `DAT_080c40a4` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c40a4` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:5853 |
| 0x080c40c8 | `DAT_080c40c8` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c40c8` | `gUIEffectState` | asm/16_duelfield_zone.s:5909 |
| 0x080c4120 | `DAT_080c4120` | 0x02023110 | REF_PRESERVE | `ptr_g_ui_effect_state_080c4120` | `gUIEffectState` | asm/16_duelfield_zone.s:5939 |
| 0x080c4124 | `DAT_080c4124` | 0x02023130 | REF_ADD | `ptr_g_duel_field_state_080c4124` | `gDuelFieldState` | asm/16_duelfield_zone.s:5951 |
| 0x080c4128 | `DAT_080c4128` | 0x00000215 | EQ_ADD | `duel_field_ui_effect_flags_off_080c4128` | `DUEL_FIELD_UI_EFFECT_FLAGS_OFF` | asm/16_duelfield_zone.s:5952 |
| 0x080c4198 | `DAT_080c4198` | 0x0201ff60 | REF_ADD | `ptr_g_card_id_cache_080c4198` | `gCardIdCache` | asm/16_duelfield_zone.s:6000 |
| 0x080c4214 | `PTR_gP1LifePoints_080c4214` | 0x0201c4e0 | REF_PRESERVE | `ptr_g_p1_life_points_080c4214` | `gP1LifePoints` | asm/16_duelfield_zone.s:6026 |
| 0x080c4218 | `DAT_080c4218` | 0x00001d08 | EQ_ADD | `p1lp_block2_off_080c4218` | `P1LP_BLOCK2_OFF` | asm/16_duelfield_zone.s:6027 |
| 0x080c421c | `DAT_080c421c` | 0x0201ff60 | REF_ADD | `ptr_g_card_id_cache_080c421c` | `gCardIdCache` | asm/16_duelfield_zone.s:6035 |
| 0x080c427c | `PTR_gP1LifePoints_080c427c` | 0x0201c4e0 | REF_PRESERVE | `ptr_g_p1_life_points_080c427c` | `gP1LifePoints` | asm/16_duelfield_zone.s:6100 |
| 0x080c4280 | `DAT_080c4280` | 0x00000868 | EQ_ADD | `player_block_stride_080c4280` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:6103 |
| 0x080c4284 | `DAT_080c4284` | 0x0201e2a0 | REF_ADD | `ptr_g_duel_card_ctx_base_080c4284` | `gDuelCardCtxBase` | asm/16_duelfield_zone.s:6127 |
| 0x080c4338 | `DAT_080c4338` | 0x02023180 | REF_ADD | `ptr_g_duel_zone_slot_data_080c4338` | `gDuelZoneSlotData` | asm/16_duelfield_zone.s:6149 |
| 0x080c433c | `DAT_080c433c` | 0x00000868 | EQ_ADD | `player_block_stride_080c433c` | `PLAYER_BLOCK_STRIDE` | asm/16_duelfield_zone.s:6159 |
| 0x080c4340 | `DAT_080c4340` | 0x0201c600 | REF_ADD | `ptr_g_p1_field_array_c_base_080c4340` | `gP1FieldArrayCBase` | asm/16_duelfield_zone.s:6163 |
| 0x080c4344 | `DAT_080c4344` | 0x02023130 | REF_ADD | `ptr_g_duel_field_state_080c4344` | `gDuelFieldState` | asm/16_duelfield_zone.s:6203 |
| 0x080c4348 | `DAT_080c4348` | 0x020230c0 | REF_ADD | `ptr_g_duel_zone_activation_state_080c4348` | `gDuelZoneActivationState` | asm/16_duelfield_zone.s:6209 |
| 0x080c434c | `DAT_080c434c` | 0x000007ff | EQ_ADD | `duel_zone_activation_low11_mask_080c434c` | `DUEL_ZONE_ACTIVATION_LOW11_MASK` | asm/16_duelfield_zone.s:6213 |

## 数据块分类 (Rule 2/3)

| block | raw / THUMB ref-scan | classification | evidence |
|---|---|---|---|
| none | no raw block in the3240B segment | no carve/disasm/registration | Current ASM and native byte/unit layout;98 typed words retained. |
完整 ROM ref-scan 仍对4个改名函数逐字节扫描raw和THUMB|1两种值, 各项命中均0. 全部引用调用来自原生 Function incoming 和全程序闭包, 不以字符串出现次数代替 indeg.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

- 复用 `constants/name_input.inc`: GSETTINGS_OFFSET =0x00006c2c, 3 slots.
  - (0x080c3960, 0x00006c2c, GSETTINGS_OFFSET, gsettings_offset_080c3960)
  - (0x080c39ac, 0x00006c2c, GSETTINGS_OFFSET, gsettings_offset_080c39ac)
  - (0x080c3b38, 0x00006c2c, GSETTINGS_OFFSET, gsettings_offset_080c3b38)
- 复用 `constants/ewram.inc`: DUEL_FIELD_UI_EFFECT_FLAGS_OFF =0x00000215, 2 slots.
  - (0x080c3a70, 0x00000215, DUEL_FIELD_UI_EFFECT_FLAGS_OFF, duel_field_ui_effect_flags_off_080c3a70)
  - (0x080c4128, 0x00000215, DUEL_FIELD_UI_EFFECT_FLAGS_OFF, duel_field_ui_effect_flags_off_080c4128)
- 复用 `constants/ewram.inc`: PLAYER_BLOCK_STRIDE =0x00000868, 7 slots.
  - (0x080c3a74, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c3a74)
  - (0x080c3a90, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c3a90)
  - (0x080c3b24, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c3b24)
  - (0x080c3c40, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c3c40)
  - (0x080c3e0c, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c3e0c)
  - (0x080c4280, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c4280)
  - (0x080c433c, 0x00000868, PLAYER_BLOCK_STRIDE, player_block_stride_080c433c)
- 复用 `constants/ewram.inc`: P1LP_BLOCK2_OFF =0x00001d08, 1 slots.
  - (0x080c4218, 0x00001d08, P1LP_BLOCK2_OFF, p1lp_block2_off_080c4218)
- 新建 `constants/duel_field.inc`: DUEL_ZONE_ACTIVATION_LOW11_MASK =0x000007ff, 1 slots.
  - (0x080c434c, 0x000007ff, DUEL_ZONE_ACTIVATION_LOW11_MASK, duel_zone_activation_low11_mask_080c434c)

### REF_SLOTS

45个 REF_ADD 均新增 operand0 / DATA / USER_DEFINED / primary=true 引用;17个 REF_PRESERVE 保持原引用所有字段及重复数量. USER label和DATA-ref一起接通. GNU已定义与Ghidra已有USER是两个独立判断.

- (0x080c36f8, 0x0600e800, BG_SCREENBLOCK_29_BASE, ptr_bg_screenblock_29_base_080c36f8), symbol=create_user_primary, GNU=new constants/gba_mem.inc.
- (0x080c36fc, 0x09e49254, duel_field_zone_tile_coords, ptr_duel_field_zone_tile_coords_080c36fc), symbol=reuse_user, GNU=reuse constants/rom_data.inc.
- (0x080c3700, 0x09e49258, duel_field_zone_tile_y_coords, ptr_duel_field_zone_tile_y_coords_080c3700), symbol=create_user_primary, GNU=new constants/rom_data.inc.
- (0x080c3788, 0x05000020, BG_PALRAM_SLOT_1, ptr_bg_palram_slot_1_080c3788), symbol=create_user_primary, GNU=new constants/gba_mem.inc.
- (0x080c378c, 0x08510460, shared_ui_palette_256, ptr_shared_ui_palette_256_080c378c), symbol=reuse_user, GNU=reuse constants/rom_data.inc.
- (0x080c37b4, 0x080c37b8, switchD_080c37b2::switchdataD_080c37b8, ptr_switch_d_080c37b2_switchdata_d_080c37b8_080c37b4), symbol=preserve_analysis, GNU=reuse asm/16_duelfield_zone.s.
- (0x080c3828, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c3828), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c382c, 0x060031c0, DUEL_FIELD_OPP_SLOT_TILE_VRAM, ptr_duel_field_opp_slot_tile_vram_080c382c), symbol=create_user_primary, GNU=new constants/gba_mem.inc.
- (0x080c383c, 0x06000040, BG_SCREEN_ROW1_OFF, ptr_bg_screen_row1_off_080c383c), symbol=create_user_primary, GNU=reuse constants/gba_mem.inc.
- (0x080c387c, 0x09854df0, field_slot_bg_tile_pattern, ptr_field_slot_bg_tile_pattern_080c387c), symbol=create_user_primary, GNU=new constants/rom_data.inc.
- (0x080c3958, 0x080000ae, ROM_REGION_CODE_ADDR, ptr_rom_region_code_addr_080c3958), symbol=reuse_user, GNU=reuse constants/rom_region.inc.
- (0x080c395c, 0x02000000, EWRAM_BASE, ptr_ewram_base_080c395c), symbol=reuse_user, GNU=reuse constants/gba_mem.inc.
- (0x080c3964, 0x093264c0, card_mini_frame_second_half_tile_data, ptr_card_mini_frame_second_half_tile_data_080c3964), symbol=reuse_user, GNU=reuse constants/rom_data.inc.
- (0x080c39a4, 0x080000ae, ROM_REGION_CODE_ADDR, ptr_rom_region_code_addr_080c39a4), symbol=reuse_user, GNU=reuse constants/rom_region.inc.
- (0x080c39a8, 0x02000000, EWRAM_BASE, ptr_ewram_base_080c39a8), symbol=reuse_user, GNU=reuse constants/gba_mem.inc.
- (0x080c39f8, 0x0984fbcc, card_mini_frame_fallback_tile_data, ptr_card_mini_frame_fallback_tile_data_080c39f8), symbol=reuse_user, GNU=reuse constants/rom_data.inc.
- (0x080c3a38, 0x0984fbcc, card_mini_frame_fallback_tile_data, ptr_card_mini_frame_fallback_tile_data_080c3a38), symbol=reuse_user, GNU=reuse constants/rom_data.inc.
- (0x080c3a6c, 0x02023130, gDuelFieldState, ptr_g_duel_field_state_080c3a6c), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3a78, 0x0201c740, gP1SlotSetCodeArray, ptr_g_p1_slot_set_code_array_080c3a78), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3a94, 0x0201c8f4, gP1Zone14CardWordBase, ptr_g_p1_zone14_card_word_base_080c3a94), symbol=create_user_primary, GNU=new constants/ewram.inc.
- (0x080c3b28, 0x0201caac, gP1Zone15CardWordBase, ptr_g_p1_zone15_card_word_base_080c3b28), symbol=create_user_primary, GNU=new constants/ewram.inc.
- (0x080c3b30, 0x080000ae, ROM_REGION_CODE_ADDR, ptr_rom_region_code_addr_080c3b30), symbol=reuse_user, GNU=reuse constants/rom_region.inc.
- (0x080c3b34, 0x02000000, EWRAM_BASE, ptr_ewram_base_080c3b34), symbol=reuse_user, GNU=reuse constants/gba_mem.inc.
- (0x080c3c38, 0x02023130, gDuelFieldState, ptr_g_duel_field_state_080c3c38), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3c3c, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c3c3c), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3c44, 0x0201c4ec, gP1ZoneHandCount, ptr_g_p1_zone_hand_count_080c3c44), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3c48, 0x0300024c, tick_campaign_card_selector_oam_attr_buf, ptr_tick_campaign_card_selector_oam_attr_buf_080c3c48), symbol=reuse_user, GNU=reuse constants/iwram.inc.
- (0x080c3c4c, 0x03000186, gKeyInputHeld, ptr_g_key_input_held_080c3c4c), symbol=create_user_primary, GNU=new constants/iwram.inc.
- (0x080c3c64, 0x03000186, gKeyInputHeld, ptr_g_key_input_held_080c3c64), symbol=create_user_primary, GNU=new constants/iwram.inc.
- (0x080c3cfc, 0x03000186, gKeyInputHeld, ptr_g_key_input_held_080c3cfc), symbol=create_user_primary, GNU=new constants/iwram.inc.
- (0x080c3e04, 0x02023114, gUIEffectArgs, ptr_g_ui_effect_args_080c3e04), symbol=create_user_primary, GNU=new constants/ewram.inc.
- (0x080c3e10, 0x0201c510, gDuelFieldSlots, ptr_g_duel_field_slots_080c3e10), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3e14, 0x080c3e18, switchD_080c3e02::switchdataD_080c3e18, ptr_switch_d_080c3e02_switchdata_d_080c3e18_080c3e14), symbol=preserve_analysis, GNU=reuse asm/16_duelfield_zone.s.
- (0x080c3ec8, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c3ec8), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3f00, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c3f00), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c3f8c, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c3f8c), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c40a4, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c40a4), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c4124, 0x02023130, gDuelFieldState, ptr_g_duel_field_state_080c4124), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c4198, 0x0201ff60, gCardIdCache, ptr_g_card_id_cache_080c4198), symbol=create_user_primary, GNU=reuse constants/ewram.inc.
- (0x080c421c, 0x0201ff60, gCardIdCache, ptr_g_card_id_cache_080c421c), symbol=create_user_primary, GNU=reuse constants/ewram.inc.
- (0x080c4284, 0x0201e2a0, gDuelCardCtxBase, ptr_g_duel_card_ctx_base_080c4284), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c4338, 0x02023180, gDuelZoneSlotData, ptr_g_duel_zone_slot_data_080c4338), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c4340, 0x0201c600, gP1FieldArrayCBase, ptr_g_p1_field_array_c_base_080c4340), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c4344, 0x02023130, gDuelFieldState, ptr_g_duel_field_state_080c4344), symbol=reuse_user, GNU=reuse constants/ewram.inc.
- (0x080c4348, 0x020230c0, gDuelZoneActivationState, ptr_g_duel_zone_activation_state_080c4348), symbol=create_user_primary, GNU=new constants/ewram.inc.

### RENAME_SLOTS

76个池字获得唯一 USER 标签及完整ASCII EOL, 包含14 EQ +45 REF_ADD +17 REF_PRESERVE. final_label及全部before/after DTO见上表和TSV. 22个switch数据字既有 namespace, ID, source, labels, refs, dtype, comments全部保持.

### FUNC_RENAME

- (0x080c36a8, write_palette_tile_row_to_vram, initialize_duel_field_slot_tilemap), indeg=1. 写双方22个3x3 BG tilemap块并拷贝256B调色板, 不是逐行palette tiles. Evidence: asm/16_duelfield_zone.s:4552, all native incoming preserved. Confidence high.
- (0x080c3840, blit_field_slot_tile_with_palette_hi, copy_field_slot_bg_tile_pattern), indeg=1. 288次halfword原样复制576B, OR只重组原high/low字节, 没有改palette位. Evidence: asm/16_duelfield_zone.s:4761, all native incoming preserved. Confidence high.
- (0x080c3b50, render_field_zone_mini_card_tiles, render_zone_list_scroll_arrows), indeg=2. 只写列表滚动箭头OAM, 无卡图数据读取或BG VRAM写入. Evidence: asm/16_duelfield_zone.s:5181, all native incoming preserved. Confidence high.
- (0x080c40e0, init_field_slot_aob_ctx_d, init_field_slot_render_request), indeg=1. 只清28B状态, 存3个参数并设标志;没有AOB初始化调用. Evidence: asm/16_duelfield_zone.s:5933, all native incoming preserved. Confidence high.

### PLATE

12个本段PLATE完整重写, 3个必要上下文PLATE订正. 所有after均ASCII且<=500字符. 本段8个未改名函数保持名称. 注册表只更新14个既有tuple, 不新建tuple;外部080ccdf4原本无tuple, 仅同步其实际Ghidra/ASM PLATE.

#### 0x080c2840 reset_zone_display_state_from_packed_key

Before: "Reset gZoneDisplayState by clearing0x5c halfwords. Split u16(r0): bits4:0 go to state byte+3 bits7:3; bits7:5 go to byte+4 bits2:0. These two fields reconstruct the original low byte. Called by dispatch_card_display_op opcode0x09 after rebuilding the separate activation mask; this function stores a packed zone key, not that mask."

After:
```text
Reset gZoneDisplayState by clearing0x5c bytes (92). Split u16(r0): bits4:0 go to state byte+3 bits7:3; bits7:5 go to byte+4 bits2:0. These two fields reconstruct the original low byte. Called by dispatch_card_display_op opcode0x09 after rebuilding the separate activation mask; this function stores a packed zone key, not that mask.
```

#### 0x080c33bc load_card_list_small_image

Before: "Upload a small card image into OBJ VRAM at0x06010000+32*u16(r3). If r1 is nonzero, use card_image_index with the region/language variant and1152-byte records; r2 selects the second576-byte half start. If r1 is0, use one of two fallback576-byte starts selected by r2&1. Clear four0x200-byte rows at stride0x400, then scatter576 source bytes into tiled destinations, adding0x70 modulo256 to each nonzero byte."

After:
```text
Upload a small card image into OBJ VRAM at0x06010000+32*u16(r3). If r1 is nonzero, use card_image_index with the region/language variant and1152-byte records; r2 selects the second576-byte half start. If r1 is0, use one of two fallback576-byte starts selected by r2&1. Clear four0x100-byte rows at stride0x400, then scatter576 source bytes into tiled destinations, adding0x70 modulo256 to each nonzero byte.
```

#### 0x080c36a8 initialize_duel_field_slot_tilemap

Before: "\u5f53 duel field \u663e\u793a\u521d\u59cb\u5316\u6216\u573a\u5730 BG \u91cd\u5efa\u65f6\u8c03\u7528 (indeg=1, tags: vram palette scene_duel_field). \u51fd\u6570\u4ece ROM \u6570\u636e\u8868 (0x09e49254/0x09e49258) \u548c VRAM base 0x0600e800 \u5f00\u59cb, \u4ee5 r7=0..1 (\u4e24\u884c\u6216\u4e24\u5c42) / r2=0..0x15 (\u5217, 22 \u5217) \u7684\u53cc\u5c42\u5faa\u73af, \u6bcf\u6b21\u8bfb\u53d6\u4e24\u4e2a ROM word (palette_index \u548c tile_index), \u5c06 tile_index<<5 | palette_offset \u5408\u6210 halfword \u5199\u5165 VRAM BG tile map. \u5916\u5c42 r7==1 \u65f6, tile_index \u5728 0..8 \u8303\u56f4\u5185\u52a0 0xC00 \u4ee5\u9009\u62e9\u7b2c\u4e8c\u5957 tile \u96c6. \u5faa\u73af\u7ed3\u675f\u540e\u4ee5 copy_bytes_by_halfword \u5c06 palette \u6570\u636e (0x100 halfwords, 0x200 bytes) \u4ece ROM (0x08510460) \u590d\u5236\u5230 BG palette (0x05000020). Constants: VRAM_BG_TILE_MAP=0x0600e800, BG_PALETTE_VRAM=0x05000020, ROM_PALETTE_SRC=0x08510460, ROM_TILE_TABLE_A=0x09e49254, ROM_TILE_TABLE_B=0x09e49258, TILE_SET_MASK=0xC00, col_count=0x15 (22 cols), row_count=2, palette_copy_size=0x100 halfwords=0x200 bytes."

After:
```text
Initialize the two-player field-slot BG tilemap at BG_SCREENBLOCK_29_BASE. For each player and22 coordinate pairs, write a3x3 tile block using x+32*y from duel_field_zone_tile_coords and its y field. Player0 advances tile numbers; player1 reverses each block and ORs0xc00 for horizontal/vertical flip. Copy256 bytes from shared_ui_palette_256 to BG_PALRAM_SLOT_1. No inputs.
```

#### 0x080c3790 get_field_slot_tile_vram_addr

Before: "Compute the BG tile VRAM address for a duel field zone slot position. r0: player_side [0..1]; r1: zone_slot_idx [0..9]. Returns ptr to BG tile VRAM position for the slot. Pure address compute; no side effects. Constants: field_tile_map_base, slot_x/y layout table in ROM."

After:
```text
Return the BG tile-data address for u16 player r0, zone type r1 and subindex r2. Treat subindex0xff as0. Types0..9 use the type as index; types12..15 use type+6; type16 uses16; other types use type+subindex. Return base+576*index, with base0x060031c0 when player equals gDuelCardCtxBase+4 XOR1, else0x06000040. The17-entry switch and all case aliases are preserved.
```

#### 0x080c3840 copy_field_slot_bg_tile_pattern

Before: "Blit field slot tile VRAM with high-palette data. Calls get_field_slot_tile_vram_addr(player_id,row,col); if addr==0 returns. Reads ROM palette table 0x09854df0 (0x90 halfwords), OR-merges hi/lo bytes, writes to VRAM. r0=u16 player_id [0..1], r1=u16 row, r2=u16 col. Returns void. Side-effects: VRAM [tile_addr..+0x120] overwritten. Constants: palette_table=0x09854df0, tile_count=0x90."

After:
```text
Copy576 bytes of field_slot_bg_tile_pattern into the address from get_field_slot_tile_vram_addr(r0,r1,r2), if nonzero. The loop count is0x120 halfwords. Its ldrh/ldrb/OR sequence reconstructs each original halfword unchanged; it does not alter a palette field. All three input selectors are truncated to u16.
```

#### 0x080c3880 update_field_slot_tile_display

Before: "Update field slot tile display: blit palette or zero-fill based on placement block check. Calls get_field_slot_tile_vram_addr, stores addr in r7. slot_idx [0..0xa] and check_slot_placement_blocked_by_field_effect==0: calls blit_field_slot_tile_with_palette_hi. slot_idx > 0xa or blocked: if VRAM addr valid, calls zero_fill_by_halfword (0x90 halfwords). r0=u16 player_id [0..1], r1=u16 slot_idx [0..0xa], r2=u16 extra. Returns void. Side-effects: VRAM [tile_addr..+0x120] written or zeroed. Constants: slot_range_max=0xa, tile_size=0x120."

After:
```text
Refresh one BG slot using u16 player/type/subindex r0-r2. Compute its tile address. If type<=10 and check_slot_placement_blocked_by_field_effect(player,type+subindex) returns0, call copy_field_slot_bg_tile_pattern. Otherwise clear576 bytes at the computed address when nonzero. The zero-fill helper takes a byte count, while the pattern-copy loop counts halfwords.
```

#### 0x080c38cc render_field_slot_card_tile

Before: "\u5f53 duel field \u9700\u8981\u5728 BG tile map \u4e0a\u6e32\u67d3\u4e00\u4e2a\u5361\u69fd\u7684\u5361\u724c\u5c0f\u56fe\u6807\u65f6\u8c03\u7528 (indeg=5, class D). \u51fd\u6570\u53c2\u6570\u901a\u8fc7\u975e APCS \u9ad8\u5bc4\u5b58\u5668\u4f20\u9012 (r8=player_side \u7b49), \u6808 sp[0x24]=card_mini_frame_flag, sp[0x28]=use_card_image_flag. \u9996\u5148\u8c03\u7528 get_field_slot_tile_vram_addr \u53d6\u76ee\u6807 VRAM \u5730\u5740. \u82e5 use_card_image_flag==0, \u8c03\u7528 update_field_slot_tile_display \u76f4\u63a5\u6e05\u7a7a\u69fd. \u5426\u5219\u6309 card_mini_frame_flag \u51b3\u5b9a\u6570\u636e\u6e90; \u8bfb\u53d6 tile_data \u540e\u5faa\u73af\u4ee5 halfword \u5f62\u5f0f\u590d\u5236 0x120 \u5b57\u8282 (144 \u4e2a halfword = \u5361\u724c\u7f29\u7565\u56fe) \u5230 VRAM \u76ee\u6807\u5730\u5740. Constants: tile_copy_count=0x90=144 halfwords, ROM_VERSION_BYTE_ADDR=0x080000ae, EWRAM_FLAGS=0x02000000+0x6c2c."

After:
```text
Render BG slot tiles using r0=player,r1=zone type,r2=subindex,r3=face flag, stack0=half selector,stack1=cached card ID; all are truncated to u16. Card ID0 refreshes the empty slot. A zero face flag selects a fallback half; otherwise select the first or second576-byte half of a1152-byte mini-card record through the region/language index. Copy576 bytes to the slot if its address is nonzero. Inputs use r0-r3 plus two stack words, not high-register arguments.
```

#### 0x080c39fc render_field_zone_card_tile_by_type

Before: "\u5f53\u9700\u8981\u6839\u636e zone_type (slot_idx r1 = 0xc/0xd/0xe/0xf \u7684\u7279\u6b8a zone) \u6e32\u67d3\u5bf9\u5e94\u7684\u5361\u724c\u5c0f\u56fe\u6807 tile \u65f6\u8c03\u7528 (indeg=4, tags: card_frame card_ids). \u51fd\u6570\u83b7\u53d6 get_field_slot_tile_vram_addr \u5b9a\u4f4d VRAM \u76ee\u6807; \u7136\u540e\u6309 zone_type \u5206\u652f: zone 0xc -> \u82e5 card_id (r4) \u975e\u96f6\u4ece gDuelFieldSlots[player][FUSION_ZONE?] \u8bfb\u5361\u5c5e\u6027 (\u542b JP flag \u68c0\u67e5) \u540e\u786e\u5b9a tile \u6e90; zone 0xd -> \u82e5\u6709\u5361\u8bfb gDuelSpecialZone_0x0201c740 (magic slot \u6570\u7ec4) \u786e\u5b9a mini frame tile; zone 0xe -> \u4e0e 0xd \u7c7b\u4f3c, \u8bfb gDuelSpecialZone2_0x0201c8f4; zone 0xf -> \u5148\u8c03 get_zone_card_attribute_by_type \u53d6\u5c5e\u6027, \u518d\u8bfb gDuelSpecialZone3_0x0201caac; \u82e5\u65e0\u5361(r4==0)\u5219\u8c03 update_field_slot_tile_display \u6e05\u7a7a. Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, gDuelSpecialZone_0xc=0x0201c740, gDuelSpecialZone_0xe=0x0201c8f4, gDuelSpecialZone_0xf=0x0201caac, ROM_VERSION_BYTE=0x080000ae, EWRAM_FLAGS=0x02000000+0x6c2c, JP_FLAG_BYTE=0x4a."

After:
```text
Render BG tiles for u16 player r0, special zone type r1 and presence/index r2. Type12 with nonzero input uses fallback tiles. Type13 checks the field reveal flag or zone attribute before reading gP1SlotSetCodeArray; type14 reads its4-byte word base at index r2; type15 first checks the attribute at r2-1 then reads its word base at r2. Decode the card word through ensure_card_id_cache_entry and region/language index. Copy576 bytes, or refresh the empty slot when no source is selected.
```

#### 0x080c3b50 render_zone_list_scroll_arrows

Before: "Render mini card tile data for a duel field zone slot into BG tile VRAM. Reads zone slot card_id, looks up mini card tile source from ROM table, copies tile data to BG VRAM at the zone position. r0: player_side [0..1]; r1: zone_slot_idx [0..9]; r2: bg_tile_dest ptr. Returns void. Side effects: BG tile VRAM written with mini card tile data. Constants: mini_card_tile_table_base in ROM."

After:
```text
Draw zone-list scroll-arrow OAM for both players when their zone/hand count exceeds7. Omit the backward arrow at origin0 and the forward arrow when origin>=count-7. Read the visible origin from gDuelFieldState+0x4c+2*player. Use tile0x20, side-dependent positions/flip, phase jitter from u16(0x0300024c), and palette cycling0..2 when the selected type11 list has the matching held direction key. This renderer reads no card tile data and writes no BG VRAM.
```

#### 0x080c3d00 init_field_slot_ctx_zoom

Before: "Initialises duel_field card zoom display context (DAT_080c3d1c, 0x1c halfwords=0x38 bytes) for dispatch_card_display_op case 0x1a (card zoom-in scene). Calls zero_fill_by_halfword(base, 0x1c), then writes r0 to [base+4] and r1 to [base+8]. r0=ptr ctx_src (zoom source descriptor); r1=ptr ctx_dst (zoom target descriptor). Returns void. Constants: base_struct=DAT_080c3d1c, zero_len=0x1c halfwords (0x38 bytes)."

After:
```text
Initialize the zoom context at gUIEffectState. Clear28 bytes, then store r0 at+4 and r1 at+8. These are interpreter arguments: the zoom renderer decodes the first as a packed slot reference. Called by dispatch_card_display_op opcode0x1a. zero_fill_by_halfword receives bytes, so0x1c clears28 bytes.
```

#### 0x080c3d20 play_card_zoom_in

Before: "\u5361\u724c\u5c0f\u56fe\u2192\u5927\u56fe\u7f29\u653e/\u65cb\u8f6c\u8fc7\u6e21\u52a8\u753b (5-step on gUIEffectState[+0x0]). \u8bfb packed card_ref @ gUIEffectState[+0x4] (bit 0=side / [5:1]=row(5b) / [13:6]=col(8b) / bit 16,17=mode flag). \u7d22\u5f15 EWRAM \u5361\u724c\u4fe1\u606f\u6570\u7ec4 0x0201c510 + (row+col)*0x14 + side*0x868. step 0 = load_card_list_small_image x2 \u88c5\u8f7d\u5c0f\u56fe. step 1 = \u8d77\u59cb\u5e27 (FUN_080f6ccc + FUN_080c3880 stats overlay). step 2 = 4-tick affine \u8fc7\u6e21: \u7528 rom_sin_table_q8 \u7b97 PA/PB/PC/PD, angle index \u2208 rom_card_zoom_anim_curve {0,1,8,15}, scale = sin*5 + 0x100, \u63d0\u4ea4 OAM affine \u77e9\u9635 via FUN_080f72e8; sub_tick @ gUIEffectState[+0x18] \u6ee1 4 \u540e\u4e3b step++. step 3 = \u88c5\u7b2c\u4e8c\u5f20\u56fe + FUN_080c38cc \u5168 bit-field stats. step 4 = \u5207\u5927\u56fe\u6a21\u5f0f (FUN_080cb1cc, BG VRAM/palette \u91cd\u78c5\u4e0a\u4f20). \u8fd4\u56de 1=busy / 0=done. \u552f\u4e00 caller: play_ui_effect (FUN_0801ef94) case 0x1a (effect_id=0x1a)."

After:
```text
Play the field-card zoom transition using gUIEffectState. Decode arg0 as player bit0,type bits5:1,subindex bits13:6 and flags14/15. Cache the card and load paired OBJ images. Step1 draws the source and refreshes its BG slot. Step2 performs five slide or affine calls using curve0,1,8,15,16; advance after the old tick exceeds3. Step3 restores BG card tiles, step4 conditionally calls render_large_card_display_by_mode. Steps0..4 return1; other steps return0.
```

#### 0x080c40e0 init_field_slot_render_request

Before: "Initialises fourth variant of duel_field slot AOB context (DAT_080c4120, 0x1c halfwords=0x38 bytes) for dispatch_card_display_op case 0x18. Calls zero_fill_by_halfword(base, 0x1c), writes r0->[base+4], r1->[base+8], r2 (via mov r8,r2 / mov r0,r8)->[base+c]. Sets [base+0x19] bit0 (init_flag=0x1). Reads gP1LifePoints player bit, ORs 0x4, writes to external ctrl byte. r0=ptr arg_data; r1=ptr arg_target; r2=ptr arg_extra (three-arg variant via r8). Returns void. Constants: base_struct=DAT_080c4120, zero_len=0x1c halfwords, init_flag=0x1."

After:
```text
Initialize a three-argument field-slot render request in gUIEffectState. Clear28 bytes, store r0/r1/r2 at+4/+8/+c, set byte+0x19 bit0 and gDuelFieldState+0x215 bit2. Called by dispatch_card_display_op opcode0x18. No AOB initializer is called. The zero-fill argument0x1c is a byte count.
```

#### 0x080c412c render_field_slot_card_tile_by_id

Before: "Decodes packed slot descriptor (r0) to player_id/zone_type/sub_idx, calls get_field_slot_tile_vram_addr to find VRAM slot, reads cached card_id at +0x120. If cache empty: calls internal_card_id_to_card_id(r1) and writes result to cache, then calls ensure_card_id_cache_entry. Finally calls render_field_slot_card_tile. Corresponds to dispatch_card_display_op case 0x1b. r0=u32 slot_descriptor (bit0=player_id, bits[5:1]=zone_type, bits[13:6]=sub_idx); r1=u16 card_id_raw [0..0x1fff]. Returns void. Constants: VRAM_cache_offset=0x120 (0x90*2)."

After:
```text
Decode packed r0: player bit0,type bits5:1,subindex bits13:6,flags14/15. r1 is an internal card ID and r2 a card-cache index. Compute the BG slot and inspect its halfword at+0x120. If zero, convert/store the ID in gCardIdCache and render the slot; if nonzero, rerender only when gP1LifePoints+0x1d08 is nonzero, using current zone attributes. A valid-slot path then refreshes buff and activation caches. The tested VRAM halfword is separate from the EWRAM card-ID cache.
```

#### 0x080c4220 refresh_player_field_slot_tiles

Before: "\u5f53 duel field \u573a\u5730\u9700\u8981\u6574\u4f53\u5237\u65b0\u67d0\u73a9\u5bb6\u6240\u6709\u5361\u69fd\u7684 BG tile \u663e\u793a\u65f6\u8c03\u7528 (indeg=6, class D). \u51fd\u6570\u63a5\u53d7 player_side (r0) \u548c\u4e00\u4e2a halfword (r1, \u4f20\u5165\u69fd header \u503c), \u9996\u5148\u8bfb\u53d6 gP1LifePoints[player*0x868+0xc] \u7684 zone count (max 7). \u5916\u5c42\u5faa\u73af r4=0..r8 (max slot count), \u5bf9\u6bcf\u69fd: \u68c0\u67e5 gDuelState[+0x4] (\u5bf9\u4fa7 player) \u6216\u8c03 get_player_deck_flag_bit1 \u786e\u8ba4\u662f\u5426\u5bf9\u4fa7; \u82e5\u662f\u5bf9\u4fa7\u5219 r6=1 (\u6709\u5361), \u5426\u5219\u4ece gDuelZoneSlotData (0x02023180) \u8bfb zone halfword \u5224\u65ad\u662f\u5426\u6709\u5361. \u7136\u540e\u8c03\u7528 render_field_slot_card_tile (FUN_080c38cc) \u6e32\u67d3\u6bcf\u69fd. \u5185\u5c42\u7ed3\u675f\u540e\u7ee7\u7eed\u5bf9 slot [4..6] \u8c03 update_field_slot_tile_display \u6e05\u7a7a\u9b54\u6cd5/\u9677\u9631\u69fd. \u6700\u540e\u5199\u5165 gDuelZoneSlotHeader (0x02023130+0x4c+player*2) \u4e00\u4e2a halfword, \u5e76\u8c03\u7528 query_player_slot_activation_bitmask (FUN_080c89a8) \u53d6\u6fc0\u6d3b\u63a9\u7801\u5199\u5165\u8f85\u52a9\u533a\u57df. Constants: gDuelState=0x0201e2a0, gP1LifePoints LP_ZONE_COUNT_OFFSET=0xc, gDuelZoneSlotData=0x02023180, gDuelZoneSlotHeader=0x02023130, gDuelFieldSlots=0x0201c600, player_stride=0x868, ACTIVATABLE_MASK_SHIFT=5."

After:
```text
Refresh a player zone/hand list from r0=player,r1=visible origin. Cap count at7. For each visible slot, choose face visibility from current-player/deck flags or gDuelZoneSlotData, read the4-byte card word from gP1FieldArrayCBase+player*0x868+4*(origin+i), cache its ID, and render type11 slot i. Refresh remaining slots through6. Store origin at field+0x4c+2*player, then replace activation bits11..17 of the control word at gDuelZoneActivationState+0x30+4*player while preserving low11 bits.
```

#### 0x080ccdf4 render_duel_field_oam_all

Before: "Called by tick_duel_field_main_frame (0x0801e984). Top-level dispatch for duel field OAM rendering. Reads [0x02023130+0x215] bits 1 and 0: if bit1 nonzero and bit0 zero, checks bit4 to conditionally call render_field_aob_slot_oam_row (FUN_080c8e6c). Reads [0x02023130+0x215] bit0 and 0x0201ff30 bit0 as dual guard; if both zero continues. Reads gP1LifePoints+0x1cf4: if==3 calls render_aob_zone_slot_oam (FUN_080c8c58). Unconditionally calls render_duel_field_zone_oam_grid (FUN_080c8d68) and render_lp_zone_oam_full (FUN_080ca42c). Checks bit0 on two flags: if both zero calls render_field_zone_mini_card_tiles. Checks bit3: if zero calls render_player_zone_active_oam (FUN_080c8870). Exit: void (push {lr} only).\n\nConstants:\n- BASE=0x02023130 (IWRAM duel field state)\n- RENDER_FLAG_OFFSET=0x215 (multi-purpose flag byte)\n- BIT0=mask LP/AOB render\n- BIT1=mask LP render\n- BIT2=mask AOB zone\n- BIT3=mask player zone active indicator\n- BIT4=enable AOB slot row render\n- SECOND_GUARD=0x0201ff30 (bit0=global mask)\n- LP_STATE_FIELD=gP1LifePoints+0x1cf4 (value==3 -> AOB zone)"

After:
```text
Render duel-field OAM only when gDuelFieldState+0x215 bit1 is set. Render the slot-row AOB when bit4 is set and bit0 at0x0201f440/0x0201ff30 is clear. A field phase value3 renders zone AOB. With field bit2 clear and count+0xa nonzero, draw the deck count. Always draw the zone grid and LP. Call render_zone_list_scroll_arrows when bit0 at0x0201f440/0x020230b1 is clear; bit3 clear draws player activation OAM.
```

必要上下文范围精确为: c2840仅`clearing0x5c halfwords` -> `clearing0x5c bytes (92)`;c33bc仅`four0x200-byte rows` -> `four0x100-byte rows`;ccdf4完整ASCII重写实际守卫及3b50调用名. c2880/c291c编号不改, Seg-2其它payload不重跑.

### 84个指令 EOL

play_card_zoom_in原有84个EOL全量ASCII重写, 同时投影标准state.eol, Function.eol_comments和module_comments;不保留CJK子串. 纠正flags为14/15, curve为5个u16, transition为5次调用, r0-r3加stack参数ABI与坐标含义.

| PC | file:line | complete ASCII after |
|---|---|---|
| 0x080c3d2c | asm/16_duelfield_zone.s:5442 | `r7 = gUIEffectArgs, the first interpreter argument at state+4.` |
| 0x080c3d2e | asm/16_duelfield_zone.s:5443 | `r0 = gUIEffectState.` |
| 0x080c3d32 | asm/16_duelfield_zone.s:5445 | `Save state+8 mode argument for later flag selection.` |
| 0x080c3d34 | asm/16_duelfield_zone.s:5446 | `Load the packed slot reference from arg0.` |
| 0x080c3d36 | asm/16_duelfield_zone.s:5447 | `Begin extracting packed bit0, the player selector.` |
| 0x080c3d3c | asm/16_duelfield_zone.s:5450 | `r1 = packed bits5:1, the zone type.` |
| 0x080c3d40 | asm/16_duelfield_zone.s:5452 | `r0 = packed bits13:6, the subindex.` |
| 0x080c3d48 | asm/16_duelfield_zone.s:5456 | `r0 = 20*(zone type+subindex).` |
| 0x080c3d4a | asm/16_duelfield_zone.s:5457 | `r1 = PLAYER_BLOCK_STRIDE.` |
| 0x080c3d50 | asm/16_duelfield_zone.s:5460 | `r1 = 0x868*player.` |
| 0x080c3d54 | asm/16_duelfield_zone.s:5462 | `r6 = gDuelFieldSlots.` |
| 0x080c3d56 | asm/16_duelfield_zone.s:5463 | `Address the20-byte slot record for player and type+subindex.` |
| 0x080c3d58 | asm/16_duelfield_zone.s:5464 | `Read the packed card word; following shifts extract its cache key.` |
| 0x080c3d76 | asm/16_duelfield_zone.s:5479 | `Reload the packed card word to extract bit13.` |
| 0x080c3d7c | asm/16_duelfield_zone.s:5482 | `Combine card-word bits29:22 shifted by1 with bit13.` |
| 0x080c3d7e | asm/16_duelfield_zone.s:5483 | `Resolve the packed key with ensure_card_id_cache_entry.` |
| 0x080c3d96 | asm/16_duelfield_zone.s:5494 | `Resolve packed pixel x/y for the player/type/subindex.` |
| 0x080c3da0 | asm/16_duelfield_zone.s:5498 | `Save u16(x-4), not a width.` |
| 0x080c3daa | asm/16_duelfield_zone.s:5503 | `Save u16(y-4), not a height.` |
| 0x080c3dc4 | asm/16_duelfield_zone.s:5516 | `Read slot-record halfword+6 for transition flag comparison.` |
| 0x080c3dde | asm/16_duelfield_zone.s:5529 | `r4 = slot-record halfword+8, the initial face selector.` |
| 0x080c3de4 | asm/16_duelfield_zone.s:5532 | `Test the state+8 mode argument before overriding the face selector.` |
| 0x080c3dee | asm/16_duelfield_zone.s:5537 | `When mode is nonzero, face selector = 1-packed bit14.` |
| 0x080c3df0 | asm/16_duelfield_zone.s:5539 | `r2 = gUIEffectState.` |
| 0x080c3df2 | asm/16_duelfield_zone.s:5540 | `r0 = u16 main step.` |
| 0x080c3df4 | asm/16_duelfield_zone.s:5541 | `Only steps0..4 dispatch; other steps return0.` |
| 0x080c3dfa | asm/16_duelfield_zone.s:5545 | `r0 = 4*step.` |
| 0x080c3dfc | asm/16_duelfield_zone.s:5546 | `r1 = the preserved five-entry step table.` |
| 0x080c3e02 | asm/16_duelfield_zone.s:5550 | `Load PC from the selected even-address THUMB switch target.` |
| 0x080c3e2c | asm/16_duelfield_zone.s:5568 | `Step0 loads the source OBJ mini-card image.` |
| 0x080c3e36 | asm/16_duelfield_zone.s:5573 | `load_card_list_small_image(cached ID,face selector,0,0x200).` |
| 0x080c3e3a | asm/16_duelfield_zone.s:5574 | `Reload packed arg0; the next shifts extract bit14.` |
| 0x080c3e40 | asm/16_duelfield_zone.s:5577 | `Compare the face selector with packed bit14.` |
| 0x080c3e4c | asm/16_duelfield_zone.s:5584 | `Choose the opposite binary face selector when another image is needed.` |
| 0x080c3e56 | asm/16_duelfield_zone.s:5590 | `Load the opposite-face OBJ image at tile destination0x208.` |
| 0x080c3e5a | asm/16_duelfield_zone.s:5591 | `Advance the main step through the common exit.` |
| 0x080c3e5c | asm/16_duelfield_zone.s:5593 | `Step1 draws the initial source-card OAM.` |
| 0x080c3e6e | asm/16_duelfield_zone.s:5602 | `Add0x40 to the orientation parameter when player==current player XOR1.` |
| 0x080c3e72 | asm/16_duelfield_zone.s:5605 | `Test slot-record halfword+6 before adding0x20 to orientation.` |
| 0x080c3e8e | asm/16_duelfield_zone.s:5620 | `Draw via write_pack_obj_attr_by_dir_stacked using saved x/y.` |
| 0x080c3e98 | asm/16_duelfield_zone.s:5624 | `Zone types above10 take the completion exit after this draw.` |
| 0x080c3eae | asm/16_duelfield_zone.s:5637 | `Refresh the BG slot pattern/clear state for player,type,subindex.` |
| 0x080c3eb8 | asm/16_duelfield_zone.s:5641 | `If face selector equals packed bit14, advance without the event call.` |
| 0x080c3ec0 | asm/16_duelfield_zone.s:5646 | `Call sync_state_and_init_sprite with event argument3.` |
| 0x080c3ecc | asm/16_duelfield_zone.s:5652 | `Step2 performs the five-call transition.` |
| 0x080c3ed2 | asm/16_duelfield_zone.s:5655 | `Compare face with bit14; BNE selects the affine path, equality slides.` |
| 0x080c3ee6 | asm/16_duelfield_zone.s:5665 | `Add0x40 to orientation for player==current player XOR1.` |
| 0x080c3eee | asm/16_duelfield_zone.s:5670 | `Test packed bit15 to select the slide direction.` |
| 0x080c3f08 | asm/16_duelfield_zone.s:5684 | `The set-bit15 slide path adds8*old tick to orientation.` |
| 0x080c3f26 | asm/16_duelfield_zone.s:5700 | `Draw the sliding sprite using the adjusted orientation.` |
| 0x080c3f2a | asm/16_duelfield_zone.s:5701 | `Advance the shared transition tick.` |
| 0x080c3f30 | asm/16_duelfield_zone.s:5705 | `The unequal-face path starts from tile destination0x200.` |
| 0x080c3f3c | asm/16_duelfield_zone.s:5711 | `Copy all five u16 curve entries, ten bytes, to the stack.` |
| 0x080c3f42 | asm/16_duelfield_zone.s:5713 | `r1 = u8 transition tick at state+0x18.` |
| 0x080c3f44 | asm/16_duelfield_zone.s:5714 | `Ticks2..4 select tile destination0x208; ticks0..1 use0x200.` |
| 0x080c3f96 | asm/16_duelfield_zone.s:5760 | `Load the signed Q8 sine table base.` |
| 0x080c3fa4 | asm/16_duelfield_zone.s:5767 | `Read curve[tick], whose five values are0,1,8,15,16.` |
| 0x080c3faa | asm/16_duelfield_zone.s:5770 | `angle index = (curve[tick]*4)&0x7f.` |
| 0x080c3fb0 | asm/16_duelfield_zone.s:5773 | `Read the curve-selected sine sample as u16.` |
| 0x080c3fba | asm/16_duelfield_zone.s:5778 | `Scale parameter = 5*sine sample+0x100.` |
| 0x080c3fc6 | asm/16_duelfield_zone.s:5784 | `Read signed sine[orientation&0x7f].` |
| 0x080c3fca | asm/16_duelfield_zone.s:5786 | `Multiply the signed orientation sample by the scale parameter.` |
| 0x080c3fd8 | asm/16_duelfield_zone.s:5793 | `Read signed sine[(orientation+0x20)&0x7f].` |
| 0x080c3fdc | asm/16_duelfield_zone.s:5795 | `Multiply the quarter-period sample by the scale parameter.` |
| 0x080c3fde | asm/16_duelfield_zone.s:5796 | `Advance orientation by0x40 before the final sample.` |
| 0x080c4006 | asm/16_duelfield_zone.s:5816 | `Read the opposite-phase sine sample for the packed draw arguments.` |
| 0x080c400c | asm/16_duelfield_zone.s:5819 | `Draw via write_oam_sprite_entry_by_flip_mode with packed coefficients.` |
| 0x080c4010 | asm/16_duelfield_zone.s:5821 | `Load the state base for shared tick advancement.` |
| 0x080c4012 | asm/16_duelfield_zone.s:5822 | `r0 = the old u8 transition tick.` |
| 0x080c4014 | asm/16_duelfield_zone.s:5823 | `Form old tick+1; the following strb stores it.` |
| 0x080c401e | asm/16_duelfield_zone.s:5828 | `Old ticks0..3 remain in step2; old tick4 advances, giving five calls.` |
| 0x080c4020 | asm/16_duelfield_zone.s:5829 | `After the old tick exceeds3, load the main step for increment.` |
| 0x080c4030 | asm/16_duelfield_zone.s:5838 | `Step3 restores the BG card image and conditionally reloads OBJ tiles.` |
| 0x080c4044 | asm/16_duelfield_zone.s:5848 | `Reload OBJ image0x200 when the chosen face differs from bit14.` |
| 0x080c407e | asm/16_duelfield_zone.s:5879 | `Draw the final card OAM at the saved x/y.` |
| 0x080c409e | asm/16_duelfield_zone.s:5894 | `Render BG card tiles with face bit14,half bit15 and the cached ID.` |
| 0x080c40a8 | asm/16_duelfield_zone.s:5899 | `Step4 conditionally refreshes the large card display.` |
| 0x080c40ae | asm/16_duelfield_zone.s:5902 | `Equality of face selector and bit14 skips the large-display refresh.` |
| 0x080c40b8 | asm/16_duelfield_zone.s:5907 | `render_large_card_display_by_mode(cached ID,gUIEffectArgs,0).` |
| 0x080c40bc | asm/16_duelfield_zone.s:5909 | `Common main-step advancement.` |
| 0x080c40c2 | asm/16_duelfield_zone.s:5912 | `Store main step+1 as a halfword.` |
| 0x080c40c4 | asm/16_duelfield_zone.s:5914 | `Return1 for an active dispatched step.` |
| 0x080c40cc | asm/16_duelfield_zone.s:5919 | `Return0 for the default/completed path.` |
| 0x080c40d0 | asm/16_duelfield_zone.s:5922 | `Restore preserved registers without changing the return value.` |

## carve 计划 (R7)

none; segment raw0. asm/rom.s保持.

## disasm 计划 (R4)

none; existing Functions和THUMB模式保持. 两组17+5 switch字及每个stub的真实body边界不变.

## 新增 constants / 全局

现有inc按名称/精确数值及当前ELF ABS符号核对. 新增11个GNU定义=10个地址别名+1个mask. 两个既有GNU别名BG_SCREEN_ROW1_OFF/gCardIdCache复用, 同时在Ghidra新建USER primary. 另2个switch目标保留ANALYSIS及namespace, 不升级来源.

- constants/duel_field.inc: `DUEL_ZONE_ACTIVATION_LOW11_MASK = 0x000007ff` (equate).
- constants/gba_mem.inc: `BG_SCREENBLOCK_29_BASE = 0x0600e800` (label).
- constants/rom_data.inc: `duel_field_zone_tile_y_coords = 0x09e49258` (label).
- constants/gba_mem.inc: `BG_PALRAM_SLOT_1 = 0x05000020` (label).
- constants/gba_mem.inc: `DUEL_FIELD_OPP_SLOT_TILE_VRAM = 0x060031c0` (label).
- constants/rom_data.inc: `field_slot_bg_tile_pattern = 0x09854df0` (label).
- constants/ewram.inc: `gP1Zone14CardWordBase = 0x0201c8f4` (label).
- constants/ewram.inc: `gP1Zone15CardWordBase = 0x0201caac` (label).
- constants/iwram.inc: `gKeyInputHeld = 0x03000186` (label).
- constants/ewram.inc: `gUIEffectArgs = 0x02023114` (label).
- constants/ewram.inc: `gDuelZoneActivationState = 0x020230c0` (label).

## 全项目名称及派生符号闭包

88个新label bases=76池字+12target. 新增45条DATA严格分区为17条进入Tiny闭包,28条由标准core保护;Tiny incoming400 ->417,固定366行.  Root真实getter对366个地址观测400个incoming, 390个源完整state均在3837核心中;新增受影响外部Function恰39个, 合并原123后162. Source hints不是scope依据. 4个改名的BL闭包按原生incoming覆盖.

RAM定义数据内部仅0x02023115和0x02023116具有受本次基址变更影响的DEFAULT动态offcut派生符号, 共7个READ引用. DAT_02023114+1/+2变为gUIEffectArgs+1/+2. ID4611686018461085973/5974, DEFAULT/Label, primary, Global namespace ID0, dynamic/API, operand/ref core全部保持. 不是新增USER标签动作. 完整366行before/after见label-closure-plan-v1.json.

RAM02023114..17实际/undefined4, 23115/16 data_at=null且data_containing精确同基址. 标准bytes/rom_word保持实际null, 不按ROM填0. 02023118..1b为独立/undefined4, 保持全部身份/边界/引用. 其它236 typed interiors及全部独立边界保留, 其它DEFAULT加号符号不normalize. 两处null-owner literal080d70d4/080ec4c8的bytes/dtype/owner与数字word表达式保持;d4仅增加批准的DEFAULT pointer显示名及其READ显示投影,ec4c8完整元数据保持. ASM18限定label/LDR投影,ASM20保持.

引用比较为严格类型/完整字段/重复数量保留的无序多重集. 新USER ID使用DYNAMIC_USER_ID:name占位, fixer原生创建后逐地址建立唯一实ID映射;旧symbol ID绝不变化. 每个before必须逐typed字段等实际canonical, after独立从canonical和最小原语派生, 不能用待验after作expected.

## GNU/native与源码范围

真实ExportRangeToGas AST对98槽及2个段外literal实跑:92个native精确,6个fallback. fallback只对应4个PALRAM/VRAM值和2个ANALYSIS switch目标, 不改原生符号来源或dtype. 继承123个有效pins, 本段新增6个, 共129. 98个完整表达式断言. 每条fallback地址和值在gas-projections.json冻结.

v1源码范围15路径, v2追加第16条asm/18_pack_card_info.s精确pointer/ldr投影;见source-scope-plan.json:本段ASM16及c2840/c33bc PLATE, later BL c7f90;ASM01仅BL1edbe;ASM17仅BLcc9c2/cce7c与ccdf4完整PLATE;registry14 existing tuples;4个name-only CSV cell及temp导出;5个constants文件;全量中间asm/all.s. 其它文件和历史快照按原字节保护. Source baseline202逐文件SHA核对, fixer建立含本段4份正式材料+新Script的207文件事务基线.

## 消费者证据 (R6)

| function | semantics | evidence | confidence |
|---|---|---|---|
| 0x080c36a8 | 双方22个coordinate对及3x3 BG map, palette memcpy r2=0x100 bytes. | asm/16_duelfield_zone.s:4552, asm/17_duelfield_pack_frame.s:1457 | high |
| 0x080c3790 | 17项地址选择表和base+576*index, subindex0xff归0. | asm/16_duelfield_zone.s:4677, asm/16_duelfield_zone.s:4686 | high |
| 0x080c3840 | 手工0x120 halfword loop=576B. | asm/16_duelfield_zone.s:4761, asm/16_duelfield_zone.s:4779 | high |
| 0x080c3880 | helper入参r1=0x90<<2=576 bytes. | asm/16_duelfield_zone.s:4797, asm/16_duelfield_zone.s:4827 | high |
| 0x080c38cc | r0-r3+stack0/1, mini-card的576B half, 手工0x120 halfwords. | asm/16_duelfield_zone.s:4836, asm/16_duelfield_zone.s:4862 | high |
| 0x080c39fc | type14/15精确word base及4B index, presence/index不是CID. | asm/16_duelfield_zone.s:4999, asm/16_duelfield_zone.s:5099 | high |
| 0x080c3b50 | count>7/origin边界/held LR/palette0..2箭头OAM. | asm/16_duelfield_zone.s:5181, asm/17_duelfield_pack_frame.s:2023 | high |
| 0x080c3d00 | r1=0x1c bytes清28B, opcode1a. | asm/16_duelfield_zone.s:5418, asm/01_vija_scene_text.s:4627 | high |
| 0x080c3d20 | 两个LSL/LSR得到bits14/15;5 u16 ROM curve;oldtick>3. | asm/16_duelfield_zone.s:5436, asm/16_duelfield_zone.s:5656 | high |
| 0x080c40e0 | 清28B存3参并设flags, opcode18. | asm/16_duelfield_zone.s:5933, asm/01_vija_scene_text.s:4609 | high |
| 0x080c412c | slot VRAM+0x120测试与EWRAM gCardIdCache分开. | asm/16_duelfield_zone.s:5973, asm/01_vija_scene_text.s:4622 | high |
| 0x080c4220 | cap7, 保存origin, 更新activation高7位并保留低11位. | asm/16_duelfield_zone.s:6090, asm/16_duelfield_zone.s:6236 | high |

helper字节ABI直接证据: asm/21_font_title_scene.s:1935 和 asm/21_font_title_scene.s:1967, 原生完整body和25823PC属性覆盖. gKeyInputHeld由update_key_input_state(asm/21_font_title_scene.s:972)从KEYINPUT取反后写03000186. gUIEffectArgs使用跨处理器共享arg0语义, 不只按zoom单一用途命名.

dispatch_card_display_op: SUB r0,#1后取61项ROM表, Ghidra caseD_N已经是原始inputN. 真实映射index8/10/11 -> input09/0b/0c -> c2840/c2880/c291c; index23/25/26 -> input18/1a/1b -> c40e0/c3d00/c412c. 详细tableword/stub/BL/native incoming证据f16-seg3-dispatcher-case-input-evidence-v1.json. 不据标签再加1.

## v2 DEFAULT pointer display delta

v1真实fullrollback出现5项差异, 全部源于080d70d4的DEFAULT pointer显示名随0600e800新USER标签自动派生. ID4611686018562486484, DEFAULT/Label, Global namespace ID0, dynamic/API, /undefined *长度4, bytes00e80006, 原refcore全部保持. 仅name/qualified由PTR_DAT_080d70d4派生为PTR_BG_SCREENBLOCK_29_BASE_080d70d4;关联PC080d709e READ operand1/sourceDEFAULT和Fn080d7064的引用显示名同步. 该动作没有新增label, renameSymbol, ref, Equate或注释setter.

独立pointer Tiny1/1作为第21辅助合同, 原162Fn/3837states/25823PC/65额外PC/366Tiny及RAM2/7保持. 受影响原20产物仅fullstate/fullFunction/primaryGraph/nativeResolver外literal.after/sourceScope;其它15要求与冻结v1真实逐字节相同. ASM18_pack_card_info.s仅2361行label和PC080d709e LDR名称自然投影, word表达式仍raw0x0600e800. Source scope15 ->16. 精确实际exporter AST同时验证label/LDR/word两态, 不是源文本泛替换.

完整Root native before/post/restored证据及新的USER ID绑定只有88个, 新expected全部由canonical/真实before加批准最小动作独立派生. 原生post未知字段不作oracle. v2实际结果见版本化replay和native-prediction报告. 旧207仅不可变snapshot历史证据, 原baseline202保持current+copy权威;fixer建立新5份formal/Script对应的新207生产事务基线.

## 自检与交接

纯内存producer和独立validator源码及完整调用路径保存在f16-seg3-analysis-source-v2.json. v2两次确定性重放覆盖原20和pointer辅助共21产物. 仅新增此pointer规则必要反例/正例, 不重跑无关旧矩阵. v1原19项及额外65指令保护实际证据按原SHA继承. 具体实际执行结果以analysis-manifest和replay/negative evidence为准. 此纯模型PASS不等于原生事务/保存/ROM验证通过, 后续由reviewer和fixer依顺序执行.

## §5.1 登记 (Rule 3)

none; raw0.

## 求助

none. Root所需真实before补证已完整提供.

## Executor Report: F16-Seg-3

- 槽: EQ=14 REF_ADD=45 REF_PRESERVE=17 PRESERVE=22 FUNC_RENAME=4 PLATE=15 (main12/context3), instruction EOL=84.
- carve=0 disasm=0 range §5.1=0.
- 新增constants/全局:GNU11, USER symbols88, virtual derived symbols2仅显示投影.
- 求助:none. proposal:doc/dev/refine/F16-Seg-3.proposal.md.
