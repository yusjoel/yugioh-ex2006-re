# Refine Proposal: F16-Seg-2 [0x080c2544..0x080c36a8)

首次 executor 分析. 本材料只定义最小符号/注释动作和完整 before/after 观察合同. 正式 reviewer 独立复核后由 fixer 落地.

## 基线与执行边界

- 前序: F16-Seg-1 完成并提交 bf0914e50b5805f544cadf02c1265f2bd67ed4cb.
- 范围: asm/16_duelfield_zone.s 的 [0x080c2544,0x080c36a8), 4452 B. 不进入 Seg-3.
- source197 与 DB15 以 root-f16-seg2-initial-baseline.json 和后续只读 context 合并证明绑定. 旧 Seg-1 prestate 不能替代本段 before.
- canonical: output/refine-run-20261028-105948/root-f16-seg2-composite-independent-prestate-v3.json; SHA256 88aacdb65a21a0b298943c828fe739aa3e53dae28f21c77b1ad75fd125213fa2.
- 追加 context: dispatch_card_display_op 和 write_obj_attr_256color_affine 的实际只读完整 Function/state/Instruction 证据. 全部64位 symbol ID 经 Python int 精确处理.
- 不改 Function body/ABI/参数/数据类型/TMode/字节/既有 reference CORE6/ANALYSIS switch namespace 或 alias.
- executor 未操作 Ghidra, 未 build, 未 commit. 生产源与 DB 由 Root 独占.

## 段测绘

- 函数入口: 15. 旧覆盖只保留 blit_card_frame_tile_row_to_vram 的已验收 ASCII plate.
- 残留自动数据名: 118. EQ_ADD=39, REF_ADD=57, REF_PRESERVE=22; 全部获得唯一 USER 槽名.
- 保留 switch words: 27. 首地址保留 ANALYSIS label/namespace/ID, 其余无 symbol 的字继续无 symbol. 全部原类型/引用/alias 保留.
- ROM_INCBIN/.byte: 0. .hword 指令100个仍为真实 InstructionDB, 不按数据处理. Root 独立布局共1851个 InstructionDB, 4452B连续覆盖.

| 入口 | before name | after name | 动作 |
| --- | --- | --- | --- |
| 0x080c2544 | play_ui_effect_3d | play_pack_banner_display_effect | RENAME_PLATE |
| 0x080c25ac | play_ui_effect_10 | play_player_zone_card_refresh_effect | RENAME_PLATE |
| 0x080c2840 | write_field_slot_activation_mask | reset_zone_display_state_from_packed_key | RENAME_PLATE |
| 0x080c2880 | init_field_slot_aob_ctx_b | init_zone_display_pair_aob_context | RENAME_PLATE |
| 0x080c291c | write_zone_oam_entry_with_flip | set_zone_display_pair_values | RENAME_PLATE |
| 0x080c2990 | write_zone_pair_oam_with_coords | write_zone_pair_oam_with_coords | PLATE |
| 0x080c2acc | play_ui_effect_0b | play_zone_pair_oam_transition_effect | RENAME_PLATE |
| 0x080c2d24 | blit_card_frame_tile_row_to_vram | blit_card_frame_tile_row_to_vram | PRESERVE |
| 0x080c2ddc | write_digit_oam_column_with_scroll | write_decimal_oam_column_with_nonzero_marker | RENAME_PLATE |
| 0x080c2e58 | render_decimal_number_to_oam | render_decimal_number_to_oam | PLATE |
| 0x080c2eac | render_card_number_oam_by_player | render_card_number_oam_by_player | PLATE |
| 0x080c305c | render_dual_card_number_oam_columns | render_dual_card_number_oam_columns | PLATE |
| 0x080c3080 | play_ui_effect_0c | play_card_pair_number_window_effect | RENAME_PLATE |
| 0x080c33bc | load_card_list_small_image | load_card_list_small_image | PLATE |
| 0x080c35ac | resolve_zone_oam_base_coords_by_type | resolve_zone_oam_base_coords_by_type | PLATE |

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB\|1) | 判定 | 理由 |
| --- | --- | --- | --- |
| none | none | none | 本段没有 ROM_INCBIN 或 .byte 块; root-f16-seg2-original-layout.json 给出全4452B逐地址覆盖 |

全 ROM 地址扫描保存在 f16-seg2-full-rom-refscan.json. 8个改名函数的 raw/THUMB|1 扫描仅 0x080c3081 有2个数值命中, 都经导出的4800B卡图记录逐字节证明为像素字节. 其余7个函数全0. 这不改变任何代码/数据指针.

| 数值命中 | 资产实证 | 对齐 | 判定 |
| --- | --- | --- | --- |
| 0x0851637c | data/card-image-tiles.s:10, graphics/bin/card-images/tiles/tb0004.bin + 0x123c | 0 | numerical pixel bytes |
| 0x08b0198b | data/card-image-tiles.s:1304, graphics/bin/card-images/tiles/tb1298.bin + 0x1cb | 3 | numerical pixel bytes |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

39槽, 14域. 复用6个既有定义, 新建8个. 不按同值误复用 HAND_COUNT_TO_SLOT_OFF: 0x404在此是OBJ tiled目标偏移, 与手牌数组基址偏移的消费者无关.

| slot | value | const_name | slot_label | 定义 |
| --- | --- | --- | --- | --- |
| 0x080c25a8 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c25a8 | reuse constants/ewram.inc |
| 0x080c2604 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c2604 | reuse constants/ewram.inc |
| 0x080c283c | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c283c | reuse constants/ewram.inc |
| 0x080c2900 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2900 | new constants/duel_field.inc |
| 0x080c2908 | 0x00800002 | AOB_MODE_TILE_BASE_128_PAL2 | aob_mode_tile_base_128_pal2_080c2908 | new constants/duel_field.inc |
| 0x080c2910 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_1ce8_080c2910 | reuse constants/ewram.inc |
| 0x080c2918 | 0xfff807ff | ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | zone_display_subphase_clear_mask_080c2918 | new constants/duel_field.inc |
| 0x080c298c | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c298c | reuse constants/ewram.inc |
| 0x080c2aa8 | 0x00002488 | OAM_ATTR2_ZONE_PAIR_PRIMARY | oam_attr2_zone_pair_primary_080c2aa8 | new constants/oam_attr.inc |
| 0x080c2ac8 | 0x0000248c | OAM_ATTR2_ZONE_PAIR_SECONDARY | oam_attr2_zone_pair_secondary_080c2ac8 | new constants/oam_attr.inc |
| 0x080c2b74 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2b74 | new constants/duel_field.inc |
| 0x080c2b8c | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2b8c | new constants/duel_field.inc |
| 0x080c2bb8 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c2bb8 | reuse constants/ewram.inc |
| 0x080c2c24 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2c24 | new constants/duel_field.inc |
| 0x080c2c28 | 0xfff807ff | ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | zone_display_subphase_clear_mask_080c2c28 | new constants/duel_field.inc |
| 0x080c2cbc | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2cbc | new constants/duel_field.inc |
| 0x080c2cc0 | 0xfff807ff | ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | zone_display_subphase_clear_mask_080c2cc0 | new constants/duel_field.inc |
| 0x080c2cc8 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c2cc8 | reuse constants/ewram.inc |
| 0x080c2cf8 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2cf8 | new constants/duel_field.inc |
| 0x080c2d1c | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c2d1c | new constants/duel_field.inc |
| 0x080c2d20 | 0xfff807ff | ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | zone_display_subphase_clear_mask_080c2d20 | new constants/duel_field.inc |
| 0x080c2d88 | 0x00006c2c | GSETTINGS_OFFSET | gsettings_offset_080c2d88 | reuse constants/name_input.inc |
| 0x080c2e54 | 0x000003c2 | OAM_ATTR2_DECIMAL_NONZERO_MARKER | oam_attr2_decimal_nonzero_marker_080c2e54 | new constants/oam_attr.inc |
| 0x080c31ec | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c31ec | reuse constants/ewram.inc |
| 0x080c3214 | 0x02100003 | AOB_MODE_TILE_BASE_528_PAL3 | aob_mode_tile_base_528_pal3_080c3214 | new constants/duel_field.inc |
| 0x080c321c | 0x000028f0 | VIJA_INTRO_WIN0H_BOUNDS | vija_intro_win0h_bounds_080c321c | reuse constants/duel_field.inc |
| 0x080c3280 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c3280 | new constants/duel_field.inc |
| 0x080c32b4 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c32b4 | new constants/duel_field.inc |
| 0x080c32f0 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c32f0 | new constants/duel_field.inc |
| 0x080c32f4 | 0xfff807ff | ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | zone_display_subphase_clear_mask_080c32f4 | new constants/duel_field.inc |
| 0x080c3318 | 0xfff807ff | ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | zone_display_subphase_clear_mask_080c3318 | new constants/duel_field.inc |
| 0x080c331c | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c331c | new constants/duel_field.inc |
| 0x080c3344 | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c3344 | new constants/duel_field.inc |
| 0x080c3374 | 0x0000dfff | DISPCNT_WIN0_CLEAR_MASK | dispcnt_win0_clear_mask_080c3374 | reuse constants/gba_io.inc |
| 0x080c337c | 0xfffff807 | ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | zone_display_packed_byte_clear_mask_080c337c | new constants/duel_field.inc |
| 0x080c33b8 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c33b8 | reuse constants/ewram.inc |
| 0x080c3414 | 0x00006c2c | GSETTINGS_OFFSET | gsettings_offset_080c3414 | reuse constants/name_input.inc |
| 0x080c345c | 0x00006c2c | GSETTINGS_OFFSET | gsettings_offset_080c345c | reuse constants/name_input.inc |
| 0x080c3558 | 0x00000404 | CARD_MINI_LOWER_HALF_TILE_OFFSET | card_mini_lower_half_tile_offset_080c3558 | new constants/oam_attr.inc |

### REF_SLOTS (USER-label + DATA-ref)

57个 REF_ADD 增加 operand0 USER_DEFINED primary DATA-ref. 22个 REF_PRESERVE 只改源槽名/EOL并保留既有引用的类型/source/primary. 既有 DEFAULT DATA-ref 不升级为 USER. 三个 switch target 继续使用原 ANALYSIS primary symbol, 只新增源槽 USER DATA-ref. target_primary_name 始终使用完整 qualified name.

| slot | target | gas_label | slot_label | 动作 |
| --- | --- | --- | --- | --- |
| 0x080c255c | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c255c | REF_PRESERVE |
| 0x080c2580 | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c2580 | REF_PRESERVE |
| 0x080c25a4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c25a4 | REF_ADD |
| 0x080c25f8 | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c25f8 | REF_PRESERVE |
| 0x080c25fc | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c25fc | REF_ADD |
| 0x080c2600 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c2600 | REF_PRESERVE |
| 0x080c2608 | 0x080c260c | switchD_080c25f4__switchdataD_080c260c | ptr_switch_d_080c25f4_switchdata_d_080c260c_080c2608 | REF_ADD |
| 0x080c2678 | 0x0202317c | gDuelZoneFirstVisibleSlotByPlayer | ptr_g_duel_zone_first_visible_slot_by_player_080c2678 | REF_ADD |
| 0x080c26d8 | 0x0202317c | gDuelZoneFirstVisibleSlotByPlayer | ptr_g_duel_zone_first_visible_slot_by_player_080c26d8 | REF_ADD |
| 0x080c2730 | 0x0202317c | gDuelZoneFirstVisibleSlotByPlayer | ptr_g_duel_zone_first_visible_slot_by_player_080c2730 | REF_ADD |
| 0x080c2734 | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c2734 | REF_PRESERVE |
| 0x080c2788 | 0x0202317c | gDuelZoneFirstVisibleSlotByPlayer | ptr_g_duel_zone_first_visible_slot_by_player_080c2788 | REF_ADD |
| 0x080c278c | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c278c | REF_PRESERVE |
| 0x080c27f0 | 0x0202317c | gDuelZoneFirstVisibleSlotByPlayer | ptr_g_duel_zone_first_visible_slot_by_player_080c27f0 | REF_ADD |
| 0x080c27f4 | 0x02023180 | gDuelZoneSlotData | ptr_g_duel_zone_slot_data_080c27f4 | REF_ADD |
| 0x080c2808 | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c2808 | REF_PRESERVE |
| 0x080c2838 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c2838 | REF_ADD |
| 0x080c287c | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c287c | REF_ADD |
| 0x080c28fc | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c28fc | REF_ADD |
| 0x080c2904 | 0x09889b80 | zone_display_pair_marker_ptnsect | ptr_zone_display_pair_marker_ptnsect_080c2904 | REF_ADD |
| 0x080c290c | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c290c | REF_PRESERVE |
| 0x080c2914 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c2914 | REF_ADD |
| 0x080c296c | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c296c | REF_ADD |
| 0x080c2988 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c2988 | REF_ADD |
| 0x080c2a3c | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c2a3c | REF_ADD |
| 0x080c2afc | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c2afc | REF_ADD |
| 0x080c2bb4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c2bb4 | REF_ADD |
| 0x080c2be0 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c2be0 | REF_ADD |
| 0x080c2c2c | 0x0201fec0 | gBannerState | ptr_g_banner_state_080c2c2c | REF_PRESERVE |
| 0x080c2c48 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c2c48 | REF_ADD |
| 0x080c2cc4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c2cc4 | REF_ADD |
| 0x080c2d7c | 0x095b5c00 | card_image_index | ptr_card_image_index_080c2d7c | REF_PRESERVE |
| 0x080c2d80 | 0x080000ae | ROM_REGION_CODE_ADDR | ptr_rom_region_code_addr_080c2d80 | REF_ADD |
| 0x080c2d84 | 0x02000000 | EWRAM_BASE | ptr_ewram_base_080c2d84 | REF_ADD |
| 0x080c2d8c | 0x08fbc080 | card_medium_frame_tile_data | ptr_card_medium_frame_tile_data_080c2d8c | REF_PRESERVE |
| 0x080c2d90 | 0x06010000 | OBJ_TILE_VRAM_BASE | ptr_obj_tile_vram_base_080c2d90 | REF_ADD |
| 0x080c2ea8 | 0x03000040 | gPrng | ptr_g_prng_080c2ea8 | REF_PRESERVE |
| 0x080c2ef0 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c2ef0 | REF_ADD |
| 0x080c2ef4 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c2ef4 | REF_ADD |
| 0x080c304c | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c304c | REF_ADD |
| 0x080c3050 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c3050 | REF_ADD |
| 0x080c3054 | 0x09e4922c | zone_display_number_jitter_offsets | ptr_zone_display_number_jitter_offsets_080c3054 | REF_ADD |
| 0x080c3058 | 0x03000040 | gPrng | ptr_g_prng_080c3058 | REF_PRESERVE |
| 0x080c30a4 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c30a4 | REF_ADD |
| 0x080c30a8 | 0x080c30ac | switchD_080c30a0__switchdataD_080c30ac | ptr_switch_d_080c30a0_switchdata_d_080c30ac_080c30a8 | REF_ADD |
| 0x080c31f0 | 0x0201c510 | gDuelFieldSlots | ptr_g_duel_field_slots_080c31f0 | REF_ADD |
| 0x080c31f4 | 0x06017800 | ZONE_DISPLAY_DIGIT_TILE_VRAM | ptr_zone_display_digit_tile_vram_080c31f4 | REF_ADD |
| 0x080c31f8 | 0x09851ffc | lp_digit_tile_rows | ptr_lp_digit_tile_rows_080c31f8 | REF_ADD |
| 0x080c31fc | 0x05000260 | OBJ_PALRAM_SLOT_3 | ptr_obj_palram_slot_3_080c31fc | REF_ADD |
| 0x080c3200 | 0x098543dc | zone_display_number_panel_palette | ptr_zone_display_number_panel_palette_080c3200 | REF_ADD |
| 0x080c3204 | 0x06014200 | AOB_DISPLAY_TILE_VRAM_A | ptr_aob_display_tile_vram_a_080c3204 | REF_ADD |
| 0x080c3208 | 0x098533dc | zone_display_number_panel_tiles | ptr_zone_display_number_panel_tiles_080c3208 | REF_ADD |
| 0x080c320c | 0x0201fe80 | gZoneDisplayNumberAobCtx | ptr_g_zone_display_number_aob_ctx_080c320c | REF_ADD |
| 0x080c3210 | 0x098543fc | zone_display_number_ptnsect | ptr_zone_display_number_ptnsect_080c3210 | REF_ADD |
| 0x080c3218 | 0x04000040 | WIN0H | ptr_win0_h_080c3218 | REF_PRESERVE |
| 0x080c3220 | 0x04000044 | WIN0V | ptr_win0_v_080c3220 | REF_PRESERVE |
| 0x080c3224 | 0x04000048 | WININ | ptr_winin_080c3224 | REF_PRESERVE |
| 0x080c3228 | 0x04000054 | BLDY | ptr_bldy_080c3228 | REF_PRESERVE |
| 0x080c3234 | 0x04000054 | BLDY | ptr_bldy_080c3234 | REF_PRESERVE |
| 0x080c3254 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c3254 | REF_ADD |
| 0x080c3340 | 0x04000054 | BLDY | ptr_bldy_080c3340 | REF_PRESERVE |
| 0x080c3378 | 0x0201fe60 | gZoneDisplayState | ptr_g_zone_display_state_080c3378 | REF_ADD |
| 0x080c33b4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c33b4 | REF_ADD |
| 0x080c3408 | 0x095b5c00 | card_image_index | ptr_card_image_index_080c3408 | REF_PRESERVE |
| 0x080c340c | 0x080000ae | ROM_REGION_CODE_ADDR | ptr_rom_region_code_addr_080c340c | REF_ADD |
| 0x080c3410 | 0x02000000 | EWRAM_BASE | ptr_ewram_base_080c3410 | REF_ADD |
| 0x080c3418 | 0x093264c0 | card_mini_frame_second_half_tile_data | ptr_card_mini_frame_second_half_tile_data_080c3418 | REF_ADD |
| 0x080c3450 | 0x095b5c00 | card_image_index | ptr_card_image_index_080c3450 | REF_PRESERVE |
| 0x080c3454 | 0x080000ae | ROM_REGION_CODE_ADDR | ptr_rom_region_code_addr_080c3454 | REF_ADD |
| 0x080c3458 | 0x02000000 | EWRAM_BASE | ptr_ewram_base_080c3458 | REF_ADD |
| 0x080c3460 | 0x09326280 | card_mini_frame_tile_data | ptr_card_mini_frame_tile_data_080c3460 | REF_PRESERVE |
| 0x080c34f8 | 0x0984fbcc | card_mini_frame_fallback_tile_data | ptr_card_mini_frame_fallback_tile_data_080c34f8 | REF_ADD |
| 0x080c34fc | 0x06010000 | OBJ_TILE_VRAM_BASE | ptr_obj_tile_vram_base_080c34fc | REF_ADD |
| 0x080c35e4 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c35e4 | REF_ADD |
| 0x080c35e8 | 0x080c35ec | switchD_080c35e2__switchdataD_080c35ec | ptr_switch_d_080c35e2_switchdata_d_080c35ec_080c35e8 | REF_ADD |
| 0x080c3634 | 0x09e49254 | duel_field_zone_tile_coords | ptr_duel_field_zone_tile_coords_080c3634 | REF_ADD |
| 0x080c3650 | 0x09e49254 | duel_field_zone_tile_coords | ptr_duel_field_zone_tile_coords_080c3650 | REF_ADD |
| 0x080c36a0 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c36a0 | REF_ADD |
| 0x080c36a4 | 0x09e49254 | duel_field_zone_tile_coords | ptr_duel_field_zone_tile_coords_080c36a4 | REF_ADD |

### RENAME_SLOTS

纯改名槽0. 118个自动槽均已归入 EQ_SLOTS 或 REF_SLOTS. 27个 switch words 的 symbol/reference/数据类型保持, 其中3个表首字只获得对应指针新增的入边.

### FUNC_RENAME

| entry | old | new | indeg | 消费者结论 |
| --- | --- | --- | --- | --- | --- |
| 0x080c2544 | play_ui_effect_3d | play_pack_banner_display_effect | 1 | UI dispatcher effect0x3d; banner3d子状态机和cleanup, high |
| 0x080c25ac | play_ui_effect_10 | play_player_zone_card_refresh_effect | 1 | effect0x10; capped7 zone-type11 card refresh, high |
| 0x080c2840 | write_field_slot_activation_mask | reset_zone_display_state_from_packed_key | 1 | dispatch opcode0x09; clear0xb8B and store packed key, activation mask由前一个独立函数建立, high |
| 0x080c2880 | init_field_slot_aob_ctx_b | init_zone_display_pair_aob_context | 1 | opcode0x0b; packed descriptor和同一state+0x48 pair AOB初始化, high |
| 0x080c291c | write_zone_oam_entry_with_flip | set_zone_display_pair_values | 1 | opcode0x0c; state+0x10/+0x14/+0x18 setter, 未发出OAM, high |
| 0x080c2acc | play_ui_effect_0b | play_zone_pair_oam_transition_effect | 1 | effect0x0b; pair position interpolation/banner hold/redraw, high |
| 0x080c2ddc | write_digit_oam_column_with_scroll | write_decimal_oam_column_with_nonzero_marker | 1 | decimal digit loop and every-nonzero marker; 无scroll或PRNG读取, high |
| 0x080c3080 | play_ui_effect_0c | play_card_pair_number_window_effect | 1 | effect0x0c; medium card pair/number columns/WIN0, high |

### PLATE (R5)

本段14条完整ASCII重写, 1条原样保留. 另2条必要C8 context plate完整ASCII重写, 不动段外槽或函数名. 每条<=500字符. 完整旧/新 rich Function 在 plates.tsv 与 function-plan.json, 非 PLATE字段严格闭包.

#### 本段14条

- 0x080c2544 play_pack_banner_display_effect

```text
UI effect0x3d pack-banner display. While gBannerState+0x10 is0, select tick_pack_banner_3d_state_machine for argument0 or its alt variant for arguments1/2; advance phase after it returns0. Return1 while active. Later calls clear banner bit0 and gDuelFieldState+0x215 bit2, preserving its bit0, and return0.
```

- 0x080c25ac play_player_zone_card_refresh_effect

```text
UI effect0x10 player-zone card refresh. Read player from gBannerState+4 and cap its zone count at7. Phases0..4 draw zone-type11 slot OAM; phase1 updates slot tiles; phases2/3 hold using an up/down byte counter. Phase4 clears the zone-slot data buffer, refreshes player tiles and count tags. Phase5 refreshes zone info. Return1 for these phases; default clears banner bit0 and field+0x215 bit2, then returns0.
```

- 0x080c2840 reset_zone_display_state_from_packed_key

```text
Reset gZoneDisplayState by clearing0x5c halfwords. Split u16(r0): bits4:0 go to state byte+3 bits7:3; bits7:5 go to byte+4 bits2:0. These two fields reconstruct the original low byte. Called by dispatch_card_display_op opcode0x09 after rebuilding the separate activation mask; this function stores a packed zone key, not that mask.
```

- 0x080c2880 init_zone_display_pair_aob_context

```text
Initialize gZoneDisplayState pair AOB context. Store u8(r1) in hword+4 bits10:3, r0 at+8 and r2 at+c. Initialize AOB at+0x48 from zone_display_pair_marker_ptnsect, tilebase0x80/palette2, then choose animation2/3 by current-player comparison. Set state bit1 and AOB+0x13 bit0. Clear phase bits10:3, subphase bits18:11 and timer hword+2 bits10:3. Dispatcher opcode0x0b; r1 is a packed descriptor, not a palette slot.
```

- 0x080c291c set_zone_display_pair_values

```text
Set pair values for dispatcher opcode0x0c. Rebuild key=(state[3]>>3)|((state[4]&7)<<5). If key is0 store r0/r1 at+0x10/+0x14 and r2 at+0x18. Otherwise swap the two values and store ((r2&0xff)<<8)|((r2>>8)&0xff) at+0x18. Set gDuelFieldState+0x215 bit2. This setter updates gZoneDisplayState and does not emit OAM entries.
```

- 0x080c2990 write_zone_pair_oam_with_coords

```text
Draw a pair of zone OAM entries. Decode two u16 descriptors as player bit7, zone type bits6:0, and subindex bits14:8. Resolve each position, add4, and adjust the second y by24 for zone types above4. Interpolate the first entry toward the second using signed progress r2/8; the second remains at the first position. Choose flip by player side; tile attrs change at progress8. Two callers supply progress0..8.
```

- 0x080c2acc play_zone_pair_oam_transition_effect

```text
UI effect0x0b zone-pair OAM transition. Decode phase/subphase/timer from gZoneDisplayState. Phase0 saves descriptors and clears the first zone slot. Phase1 draws the pair, advances an8-call interpolation, runs a pack-banner submachine, then holds until timer24 and clears field bit2. A second slot of-1 bypasses phase1. Phase2 redraws the second slot when <=4. Active phases return1; other phases clear packed counters and return0.
```

- 0x080c2ddc write_decimal_oam_column_with_nonzero_marker

```text
Write decimal OAM digits at r0=x,r1=y with palette r3. Render at least one digit from abs(r2), advancing x by-12 per digit; attr2 is0x3c4+2*digit OR palette<<12. For every nonzero original r2, including positive values, draw the extra0x3c2 marker after the digits. No PRNG or scroll input is read. The sole caller negates its displayed value before this call.
```

- 0x080c2e58 render_decimal_number_to_oam

```text
Render one decimal number column: r0 selects column, r1 supplies value, r2 enables palette flicker. Count positive decimal divisions; x=100*column+6*digits+0x52 and y=0x40. Palette is2, or2-((u16(gPrng+0x20c)>>2)&1) when enabled. Call write_decimal_oam_column_with_nonzero_marker with the negated value. Nonpositive input counts as one digit in the positioning loop.
```

- 0x080c2eac render_card_number_oam_by_player

```text
Render a card-number column selected by OBJ tile destination0x200 or0x208. Read paired values/flags from gZoneDisplayState; choose x by player side and draw the number in active subphases. Subphase1 ticks the marker AOB and adds signed x/y jitter from zone_display_number_jitter_offsets using PRNG modulo10. A second AOB flickers on PRNG bit2. Draw the two card-image halves unless the selected flag/subphase suppresses the column. r1 is the packed per-column draw flags.
```

- 0x080c305c render_dual_card_number_oam_columns

```text
Render both card-number columns for play_card_pair_number_window_effect. Preserve r0 as packed draw flags and call render_card_number_oam_by_player with tile destinations0x200 and0x208, passing the same flags as r1. No y-coordinate is supplied to either column.
```

- 0x080c3080 play_card_pair_number_window_effect

```text
UI effect0x0c card-pair number window using gZoneDisplayState. Phase0 uploads two medium card images, digits/panel palette/tiles, initializes two AOBs, and enables WIN0. Phase1 writes BLDY8. Phase2 renders both columns while subphases hold8/24/16 calls; the middle hold triggers sync_state_and_init_sprite(7). Phase3 writes BLDY0. Phase4 disables WIN0 and blending. Active phases return1; default rebuilds the activation mask, clears state bits0..2 and field bit2, and returns0.
```

- 0x080c33bc load_card_list_small_image

```text
Upload a small card image into OBJ VRAM at0x06010000+32*u16(r3). If r1 is nonzero, use card_image_index with the region/language variant and1152-byte records; r2 selects the second576-byte half start. If r1 is0, use one of two fallback576-byte starts selected by r2&1. Clear four0x200-byte rows at stride0x400, then scatter576 source bytes into tiled destinations, adding0x70 modulo256 to each nonzero byte.
```

- 0x080c35ac resolve_zone_oam_base_coords_by_type

```text
Resolve packed pixel coordinates (y<<16)|x for player r0, zone type r1 and subindex r2; subindex0xff becomes0. Read s32 tile-coordinate pairs from duel_field_zone_tile_coords at player stride0xb0, then multiply x/y by8. Types0..10 index type+subindex, types12..15 index type+6. Type11 subtracts the player-oriented field+0x4c scroll origin and clamps indices<=10 to11. Out-of-range types return0. The16 switch words and all case aliases remain intact.
```

#### 必要C8的2条

- 0x080c678c update_zone_oam_card_count_tag

```text
Refresh the zone-type11 count tag in gDuelFieldState+0x210. Decode player from bit7 and read its zone count at gP1LifePoints+player*0x868+0xc. Ignore other zone types or counts above6. Count0 stores only player<<7. Otherwise resolve the descriptor to zone data; when its first word has low13 bits zero, store (player<<7)|11|((count-1)<<8). Called by dispatch_card_display_op, field refresh and play_player_zone_card_refresh_effect.
```

- 0x080f64dc write_obj_attr_256color_affine

```text
Emit256-color OBJ attributes for play_player_zone_card_refresh_effect. r0 packs x/y; r1 supplies shape/size flags, r2 tile/priority and r3 attr1 flags. Get OAM base through gPrng+0x1bc; exit when its slot byte at+0x400 is0x80. attr0=(y&0xff)|(r1&0xff00)|0x2000; attr1=(x&0x1ff)|((r1<<8)&0xfe00)|u16(r3); attr2=(r2&0xc00)|((r2&0x1ff)<<1). Write the selected8-byte entry and increment the slot byte.
```

保留0x080c2d24的现有 plate与所有ABI/body字段. asm/01只有7处给定BL名投影, asm/21只有0x080f64dc plate. asm/16段外只有0x080c678c plate. 禁止泛替换旧名.

## carve 计划 (R7)

none. 本段无可carve块. 不改asm/rom.s.

## disasm 计划 (R4)

none. 27个既有switch words和3组目标继续保留全部代码单元. 不调用disasm/clearListing.

## 新增 constants / 全局

常量复用检索已读全部 constants/*.inc. 精确同值候选仅0x404有异域HAND_COUNT_TO_SLOT_OFF, 消费者排除其复用. 新20个GNU声明来自8个新data-equate和12个新target label, 没有新include文件.

| name | value | file | kind |
| --- | --- | --- | --- |
| ZONE_DISPLAY_PACKED_BYTE_CLEAR_MASK | 0xfffff807 | constants/duel_field.inc | equate |
| ZONE_DISPLAY_SUBPHASE_CLEAR_MASK | 0xfff807ff | constants/duel_field.inc | equate |
| AOB_MODE_TILE_BASE_128_PAL2 | 0x00800002 | constants/duel_field.inc | equate |
| AOB_MODE_TILE_BASE_528_PAL3 | 0x02100003 | constants/duel_field.inc | equate |
| OAM_ATTR2_ZONE_PAIR_PRIMARY | 0x00002488 | constants/oam_attr.inc | equate |
| OAM_ATTR2_ZONE_PAIR_SECONDARY | 0x0000248c | constants/oam_attr.inc | equate |
| OAM_ATTR2_DECIMAL_NONZERO_MARKER | 0x000003c2 | constants/oam_attr.inc | equate |
| CARD_MINI_LOWER_HALF_TILE_OFFSET | 0x00000404 | constants/oam_attr.inc | equate |
| gZoneDisplayState | 0x0201fe60 | constants/ewram.inc | label |
| gZoneDisplayNumberAobCtx | 0x0201fe80 | constants/ewram.inc | label |
| gDuelZoneFirstVisibleSlotByPlayer | 0x0202317c | constants/ewram.inc | label |
| gDuelZoneSlotData | 0x02023180 | constants/ewram.inc | label |
| ZONE_DISPLAY_DIGIT_TILE_VRAM | 0x06017800 | constants/gba_mem.inc | label |
| card_mini_frame_second_half_tile_data | 0x093264c0 | constants/rom_data.inc | label |
| zone_display_number_panel_tiles | 0x098533dc | constants/rom_data.inc | label |
| zone_display_number_panel_palette | 0x098543dc | constants/rom_data.inc | label |
| zone_display_number_ptnsect | 0x098543fc | constants/rom_data.inc | label |
| zone_display_pair_marker_ptnsect | 0x09889b80 | constants/rom_data.inc | label |
| zone_display_number_jitter_offsets | 0x09e4922c | constants/rom_data.inc | label |
| duel_field_zone_tile_coords | 0x09e49254 | constants/rom_data.inc | label |

新target语义与结构:

- gZoneDisplayState=0x0201fe60: 清0xb8B, packed phase/subphase/timer/key, slots+8/+c, values+0x10/+0x14, flags+0x18, 两个数字AOB+0x20/+0x34, pair AOB+0x48.
- gZoneDisplayNumberAobCtx=0x0201fe80: state+0x20的数字显示AOB. 两槽保持base与实际子结构地址各自表达.
- gDuelZoneFirstVisibleSlotByPlayer=0x0202317c: player*2 halfword, 类型11的可见起始slot. refresh_player_field_slot_tiles写入, query_player_slot_activation_bitmask与本段按header+i消费.
- gDuelZoneSlotData=0x02023180: 0x280B清零缓冲; refresh_player_field_slot_tiles按player和slot读取halfword存在值.
- card_mini_frame_second_half_tile_data=card_mini_frame_tile_data+0x240: 同一1152B record的第二576B起点, 由load_card_list_small_image r2!=0分支选择.
- zone_display_number_jitter_offsets=0x09e4922c: s16 x[10]随后s16 y[10], PRNG modulo10索引.
- duel_field_zone_tile_coords=0x09e49254: 两组player stride0xb0, 每条s32 x/y tile coordinate. resolver转pixel时乘8; 相邻BG写入消费者也从该表取tile位置.
- 其余ROM label依据copy/tile-blit/palette-copy/init_aob_ctx_from_ptnsect的具体consumer, 仅命名使用角色, 不改资产数据.

## §5.1 登记 (Rule 3)

none. 没有本段0引用数据块. 不增加§5.1记录.

## 消费者证据 (R6)

145槽每个实际READ消费者的地址/operand/file:line保存在 f16-seg2-semantic-plan.json; 全部high. 关键锚:

| 对象 | file:line | 证据 |
| --- | --- | --- |
| UI opcode0x09/0x0b/0x0c | asm/01_vija_scene_text.s:4645 | rebuild activation mask后调用reset; 其余2路传3参数 |
| packed key | asm/16_duelfield_zone.s:2607 | u16(r0)分拆bits4:0与bits7:5; 0x080c291c反向重建 |
| pair AOB/packed counters | asm/16_duelfield_zone.s:2641 | init_from_ptnsect/state flags/位域clear |
| pair setter | asm/16_duelfield_zone.s:2721 | 条件交换值和低两字节, UI bit2 |
| first visible slot | asm/16_duelfield_zone.s:6090; asm/16_duelfield_zone.s:13803 | +player*2 halfword; 两个独立slot消费循环 |
| decimal marker | asm/16_duelfield_zone.s:3377 | abs数值数字循环; original!=0即绘制marker |
| jitter array | asm/16_duelfield_zone.s:3633 | u16 PRNG %10; ldrsh基址与+0x14 |
| AOB mode | asm/21_font_title_scene.s:8980 | mode高16 tilebase写ctx+0x10; 低4 palette base写ctx+0x12; asm/21_font_title_scene.s:9348送attr2 bits15:12, :9654/:7066写入OAM |
| 必要C8 OAM | asm/21_font_title_scene.s:5353 | 全attr公式经指令重读; plate现名投影 |
| 必要C8 count tag | asm/16_duelfield_zone.s:9238 | count0只存player<<7; 其余条件由low13检验 |

## 完整合同与可复跑证据

- slots.tsv列出145词的完整old/final symbols, refs, Eq refs, comments, data type, instruction与Function owner. 27字保留项也在表中.
- function-plan/full-function-observation-plan冻结selected 19与全 119 Functions, 包含ABI/body/prototype/return/params/所有ref和plate.
- instruction-properties-plan冻结16452PC的完整before/after, 只投影批准改名的Function owner name, text/length/flow/fallthrough/override/id/bytes保持.
- fullstate-observation-plan冻结 3097 states. 全before来自Root冻结canonical, 完整after独立由批准最小原语派生.
- global_equates按严格类型的无序多重集比较refs, 不丢字段/重复项. 2479 -> 2487 Equates, 12686 -> 12725 bindings.
- GNU20个声明独立从EQ/REF原语闭包; native resolver实际AST执行145x2, native 137, 新fallback 8. 继承115 pins精确保留, 新fallback只允许实际不相等的地址.
- f16-seg2-analysis-source-v1.json保存producer/独立validator完整可执行源码与调用路径. executor不创建.py; 后续fixer可按同JSON物化.
- source-scope-plan固定本段/7个dispatcher BL/2个C8 plate/既有16个registry tuple/GNU定义/CSV name-only. 命名CSV每地址只改name列, registry原tuple索引与key保留, new_tuple_count=0.
- Root拥有DB15备份与完整保存/重导/注入/split/export_all/build/33554432B ROM逐字节验证门禁. 本proposal不宣称已落地.

## 求助

none. 所有批准语义high, 无新函数/不确定数据块.

## Executor Report: F16-Seg-2

- 槽: EQ=39 REF_ADD=57 REF_PRESERVE=22 RENAME=0 PRESERVE_SWITCH=27 FUNC_RENAME=8 PLATE=14 + 2 context, PRESERVED_PLATE=1.
- carve=0 disasm=0 range §5.1=0.
- 新增 constants/全局: 8 data-equates + 12 address labels.
- 求助: none.
- proposal: doc/dev/refine/F16-Seg-2.proposal.md


## R5 独立 derived DEFAULT offcut 元数据合同

- 独立 delta review 已批准 `0x093264c0` 的 USER 基名对 `0x093264c2` 动态 DEFAULT `+2` 显示名的精确投影。只改四个既有 rich 引用的 target_primary_name，不新增 label、reference、equate、data 或 mutator。
- 函数计划两处、全函数计划四处、plates TSV after_function_json 两处共八个 after 名称副本更新；全部 before 副本保持原值。其他27个 DEFAULT “+” 引用保持完整 DTO。
- canonical88a 的 core3097/119 Functions/1580 module words/43716 byte units 保持。辅助 `f16-seg2-derived-offcut-plan-v1.json` 独立冻结 standard_c2、tiny_c2、tiny_c4 的 before/after。
- standard_c2 保留显式 null、全部四字节 c2..c5、完整元数据；Tiny 两行保持实际缺省字段，禁止补 null。c4 是独立 c4..c7 dword，其两条完整 rich incoming 与 canonical Function entry/name/staticID 精确保护；c2 四条 owner 同样保护。
- producer 与独立 normal validator 分别推导。fresh-before、managed-before、post、owned-false 完整回滚及独立 saved observer 必须消费该辅助 bundle，严格类型、完整字段、无序引用多重集不丢重复。
- 原145槽动作、39 EQ/57 REF_ADD/22 REF_PRESERVE/27 switch preserve、118 label/EOL、12 target、8 rename、16 plate、native137+fallback8、115继承→123 pins 和15 allowed/13 changed source scope 均不增加。source reverse_assembly 与全 ROM 逐字节验证门禁保持。
- 本轮仅准备分析模型。新 Script/202 snapshot、实际只读完整回滚、唯一保存和源码/ROM落地仍由后续独立门禁处理。
