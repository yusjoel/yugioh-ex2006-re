# Refine Proposal: F16-Seg-7 [080c7af8..080c8bf0)

本版是静态语义提案. 运行时预测/独立评分/实际保存尚未执行. Ghidra注释的after文本全部ASCII, PLATE<=500字符. 签名仅文档说明, Function ABI保持.

## 段测绘

范围4344B. 12个既有Function, 223个池字, 151个自动池槽, 另有裸块起始DAT标签1个, 合计152个源码自动名. Seg1..6已提交的动作不重apply.

| 入口 | 当前名 | 计划名 | 当前body bytes |
|---|---|---|---:|
| 080c7af8 | copy_card_frame_tiles_by_type | init_card_display_frame_by_mode | 42 |
| 080c7ba8 | render_card_list_face_row_by_mode | animate_card_display_frame_open | 644 |
| 080c7ea0 | dispatch_card_display_state_by_mode | tick_card_display_transition | 766 |
| 080c82e4 | tick_card_list_display_master | tick_card_list_display_master | 226 |
| 080c841c | render_card_list_face_row_by_mode_alt | animate_card_display_frame_close | 544 |
| 080c8688 | tick_card_list_scene_frame | tick_card_list_scene_frame | 216 |
| 080c879c | init_duel_field_lp_aob_ctx | init_duel_field_lp_aob_ctx | 140 |
| 080c8870 | render_player_zone_active_oam | render_player_zone_active_oam | 124 |
| 080c8904 | refresh_all_zone_slot_tile_display | refresh_all_zone_slot_tile_display | 156 |
| 080c89a8 | query_player_slot_activation_bitmask | query_player_slot_activation_bitmask | 60 |
| 080c89e8 | update_zone_activation_display_state | update_zone_activation_display_state | 178 |
| 080c8aa8 | render_duel_field_slot_oam_grid | render_duel_field_slot_oam_grid | 264 |

223个word及完整before/消费者/类型/引用逐行列于同名slots.tsv. 自动名151槽全部有USER计划; 无名字的72个CASE槽保持无新槽标签.

## 数据块分类 (Rule 2/3)

| 块 | 原ROM raw / THUMB+1 | 判定 | 证据 |
|---|---|---|---|
| [080c7b68,080c7ba2),58B | 十个表入口合计13 /0; 其余19个半字候选0/0 | R4 disasm | 7b18 indexed LDR,7b1a mov pc,r0; 10BL+9B,19指令58B |

完整全ROM扫描见f16-seg7-full-raw-refscan-v1.json. 29个半字候选均扫描, 不能把仅+1为0当作孤儿证据. 14项表保留even地址; mov pc保持Thumb, 不加1. Root detached原生解码逐项与ROM相等. 无新池字/对齐/新Function/flow override.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

73槽添加operand0 data-equate, 值逐项等于原ROM. 复用14个既有常量, 新建11个数值常量. 不修改同值其他槽.

| slot | value | constant | slot_label |
|---|---|---|---|
| 080c7b28 | 0x00000a01 | FONT_STATE_DISPLAY_MODE_OFF | init_card_display_frame_by_mode_font_state_display_mode_off_080c7b28 |
| 080c7bd4 | 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | animate_card_display_frame_open_font_state_display_phases_packed_off_080c7bd4 |
| 080c7c20 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | animate_card_display_frame_open_font_state_display_row_count_off_080c7c20 |
| 080c7c38 | 0x0000013f | CARD_DISPLAY_FRAME_FIRST_ROW_MIDDLE_TILE | animate_card_display_frame_open_card_display_frame_first_row_middle_tile_080c7c38 |
| 080c7c68 | 0x00000145 | CARD_DISPLAY_FRAME_LAST_ROW_MIDDLE_TILE | animate_card_display_frame_open_card_display_frame_last_row_middle_tile_080c7c68 |
| 080c7c8c | 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | animate_card_display_frame_open_card_display_frame_middle_row_left_tile_080c7c8c |
| 080c7cb4 | 0x00000143 | CARD_DISPLAY_FRAME_MIDDLE_ROW_RIGHT_TILE | animate_card_display_frame_open_card_display_frame_middle_row_right_tile_080c7cb4 |
| 080c7cbc | 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | animate_card_display_frame_open_font_state_display_phases_packed_off_080c7cbc |
| 080c7d28 | 0x00000a1b | FONT_STATE_DISPLAY_FRAME_STEP_LO_OFF | animate_card_display_frame_open_font_state_display_frame_step_lo_off_080c7d28 |
| 080c7d2c | 0x00000a1c | FONT_STATE_DISPLAY_FRAME_STEP_HI_OFF | animate_card_display_frame_open_font_state_display_frame_step_hi_off_080c7d2c |
| 080c7d30 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | animate_card_display_frame_open_font_state_display_row_count_off_080c7d30 |
| 080c7d60 | 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | animate_card_display_frame_open_card_display_frame_middle_row_left_tile_080c7d60 |
| 080c7dd8 | 0x00000a1b | FONT_STATE_DISPLAY_FRAME_STEP_LO_OFF | animate_card_display_frame_open_font_state_display_frame_step_lo_off_080c7dd8 |
| 080c7ddc | 0x00000a1c | FONT_STATE_DISPLAY_FRAME_STEP_HI_OFF | animate_card_display_frame_open_font_state_display_frame_step_hi_off_080c7ddc |
| 080c7e18 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | animate_card_display_frame_open_font_state_display_row_count_off_080c7e18 |
| 080c7e48 | 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | animate_card_display_frame_open_card_display_frame_middle_row_left_tile_080c7e48 |
| 080c7e84 | 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | animate_card_display_frame_open_font_state_display_phases_packed_off_080c7e84 |
| 080c7e88 | 0xfffe01ff | EQUIP_STATE_CLEAR_BITS_16_9_MASK | animate_card_display_frame_open_equip_state_clear_bits_16_9_mask_080c7e88 |
| 080c7ec4 | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c7ec4 |
| 080c7f3c | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | tick_card_display_transition_duel_field_ui_effect_flags_off_080c7f3c |
| 080c7f44 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | tick_card_display_transition_font_state_display_row_count_off_080c7f44 |
| 080c7fc8 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_card_display_transition_duel_field_prng_anim_flag_off_080c7fc8 |
| 080c7fd4 | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c7fd4 |
| 080c7fd8 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_display_transition_equip_state_clear_bits_8_1_mask_080c7fd8 |
| 080c8030 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | tick_card_display_transition_duel_field_ui_effect_flags_off_080c8030 |
| 080c8038 | 0x000028f0 | VIJA_INTRO_WIN0H_BOUNDS | tick_card_display_transition_vija_intro_win0h_bounds_080c8038 |
| 080c803c | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c803c |
| 080c8040 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_display_transition_equip_state_clear_bits_8_1_mask_080c8040 |
| 080c806c | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | tick_card_display_transition_font_state_display_row_count_off_080c806c |
| 080c8074 | 0x00000a01 | FONT_STATE_DISPLAY_MODE_OFF | tick_card_display_transition_font_state_display_mode_off_080c8074 |
| 080c8160 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | tick_card_display_transition_duel_field_ui_effect_flags_off_080c8160 |
| 080c8164 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | tick_card_display_transition_font_state_display_row_count_off_080c8164 |
| 080c81c8 | 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | tick_card_display_transition_card_display_frame_middle_row_left_tile_080c81c8 |
| 080c81cc | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c81cc |
| 080c81d0 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_display_transition_equip_state_clear_bits_8_1_mask_080c81d0 |
| 080c81d8 | 0x00000a01 | FONT_STATE_DISPLAY_MODE_OFF | tick_card_display_transition_font_state_display_mode_off_080c81d8 |
| 080c8274 | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c8274 |
| 080c8278 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_display_transition_equip_state_clear_bits_8_1_mask_080c8278 |
| 080c82a0 | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c82a0 |
| 080c82a4 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_display_transition_equip_state_clear_bits_8_1_mask_080c82a4 |
| 080c82d8 | 0x0000dfff | DISPCNT_WIN0_CLEAR_MASK | tick_card_display_transition_dispcnt_win0_clear_mask_080c82d8 |
| 080c82dc | 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | tick_card_display_transition_font_state_display_detail_packed_off_080c82dc |
| 080c82e0 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_display_transition_equip_state_clear_bits_8_1_mask_080c82e0 |
| 080c8314 | 0x00000a17 | FONT_STATE_DISPLAY_MASTER_PACKED_OFF | tick_card_list_display_master_font_state_display_master_packed_off_080c8314 |
| 080c8334 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_card_list_display_master_duel_field_prng_anim_flag_off_080c8334 |
| 080c837c | 0x00000a01 | FONT_STATE_DISPLAY_MODE_OFF | tick_card_list_display_master_font_state_display_mode_off_080c837c |
| 080c8448 | 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | animate_card_display_frame_close_font_state_display_phases_packed_off_080c8448 |
| 080c848c | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | animate_card_display_frame_close_font_state_display_row_count_off_080c848c |
| 080c84b8 | 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | animate_card_display_frame_close_card_display_frame_middle_row_left_tile_080c84b8 |
| 080c853c | 0x00000a1b | FONT_STATE_DISPLAY_FRAME_STEP_LO_OFF | animate_card_display_frame_close_font_state_display_frame_step_lo_off_080c853c |
| 080c8540 | 0x00000a1c | FONT_STATE_DISPLAY_FRAME_STEP_HI_OFF | animate_card_display_frame_close_font_state_display_frame_step_hi_off_080c8540 |
| 080c8544 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | animate_card_display_frame_close_font_state_display_row_count_off_080c8544 |
| 080c8580 | 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | animate_card_display_frame_close_card_display_frame_middle_row_left_tile_080c8580 |
| 080c8604 | 0x00000a1b | FONT_STATE_DISPLAY_FRAME_STEP_LO_OFF | animate_card_display_frame_close_font_state_display_frame_step_lo_off_080c8604 |
| 080c8608 | 0x00000a1c | FONT_STATE_DISPLAY_FRAME_STEP_HI_OFF | animate_card_display_frame_close_font_state_display_frame_step_hi_off_080c8608 |
| 080c8664 | 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | animate_card_display_frame_close_font_state_display_row_count_off_080c8664 |
| 080c866c | 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | animate_card_display_frame_close_font_state_display_phases_packed_off_080c866c |
| 080c8670 | 0xfffe01ff | EQUIP_STATE_CLEAR_BITS_16_9_MASK | animate_card_display_frame_close_equip_state_clear_bits_16_9_mask_080c8670 |
| 080c8744 | 0x00001d08 | P1LP_BLOCK2_OFF | tick_card_list_scene_frame_p1lp_block2_off_080c8744 |
| 080c8750 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_card_list_scene_frame_duel_field_prng_anim_flag_off_080c8750 |
| 080c875c | 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | tick_card_list_scene_frame_font_state_display_phases_packed_off_080c875c |
| 080c8760 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | tick_card_list_scene_frame_equip_state_clear_bits_8_1_mask_080c8760 |
| 080c8764 | 0xfffe01ff | EQUIP_STATE_CLEAR_BITS_16_9_MASK | tick_card_list_scene_frame_equip_state_clear_bits_16_9_mask_080c8764 |
| 080c8768 | 0x00000a1b | FONT_STATE_DISPLAY_FRAME_STEP_LO_OFF | tick_card_list_scene_frame_font_state_display_frame_step_lo_off_080c8768 |
| 080c876c | 0x00000a17 | FONT_STATE_DISPLAY_MASTER_PACKED_OFF | tick_card_list_scene_frame_font_state_display_master_packed_off_080c876c |
| 080c8798 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | tick_card_list_scene_frame_duel_field_ui_effect_flags_off_080c8798 |
| 080c8848 | 0x00800002 | AOB_MODE_TILE_BASE_128_PAL2 | init_duel_field_lp_aob_ctx_aob_mode_tile_base_128_pal2_080c8848 |
| 080c8850 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | init_duel_field_lp_aob_ctx_p1lp_block2_off_1ce8_080c8850 |
| 080c88bc | 0x00000868 | PLAYER_BLOCK_STRIDE | render_player_zone_active_oam_player_block_stride_080c88bc |
| 080c88c4 | 0x00000cc4 | DUEL_ZONE_ACTIVE_HIGH_COUNT_ATTR2 | render_player_zone_active_oam_duel_zone_active_high_count_attr2_080c88c4 |
| 080c89a4 | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | refresh_all_zone_slot_tile_display_duel_field_fadein_flag_off_080c89a4 |
| 080c8aa4 | 0x000007ff | DUEL_ZONE_ACTIVATION_LOW11_MASK | update_zone_activation_display_state_duel_zone_activation_low11_mask_080c8aa4 |
| 080c8bec | 0x00008080 | CARD_IMAGE_RIGHT_COLUMN_OBJ_ATTR | render_duel_field_slot_oam_grid_card_image_right_column_obj_attr_080c8bec |

### REF_SLOTS

68槽新增USER DATA引用, 8槽完整保留既有DATA引用. 20个全局目标补USER primary, 其余14个全局既有USER不改. 新目标17个地址.equ, 两个VRAM地址复用OPP_CARD_LABEL_TILE_VRAM_A/C, 一处回调表由rom.s定义global label.

| slot | target | GAS target | action | slot_label |
|---|---|---|---|---|
| 080c7b1c | 0600a7c0 | card_display_frame_bg_tiles | REF_ADD | init_card_display_frame_by_mode_ptr_card_display_frame_bg_tiles_080c7b1c |
| 080c7b20 | 09889fd8 | card_display_frame_bg_tile_data | REF_ADD | init_card_display_frame_by_mode_ptr_card_display_frame_bg_tile_data_080c7b20 |
| 080c7b24 | 0201f440 | gFontState | REF_ADD | init_card_display_frame_by_mode_ptr_g_font_state_080c7b24 |
| 080c7b2c | 080c7b30 | card_display_frame_mode_call_table | REF_PRESERVE | init_card_display_frame_by_mode_ptr_card_display_frame_mode_call_table_080c7b2c |
| 080c7bd0 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7bd0 |
| 080c7c1c | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7c1c |
| 080c7c24 | 0600f020 | card_display_frame_bg_map_right | REF_ADD | animate_card_display_frame_open_ptr_card_display_frame_bg_map_right_080c7c24 |
| 080c7cb8 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7cb8 |
| 080c7d24 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7d24 |
| 080c7d34 | 0600f000 | card_display_frame_bg_map | REF_ADD | animate_card_display_frame_open_ptr_card_display_frame_bg_map_080c7d34 |
| 080c7dd4 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7dd4 |
| 080c7e14 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7e14 |
| 080c7e1c | 0600f00a | card_display_frame_bg_map_left | REF_ADD | animate_card_display_frame_open_ptr_card_display_frame_bg_map_left_080c7e1c |
| 080c7e80 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_open_ptr_g_font_state_080c7e80 |
| 080c7ec0 | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c7ec0 |
| 080c7ec8 | 080c7ecc | switchD_080c7ebe__switchdataD_080c7ecc | REF_ADD | tick_card_display_transition_ptr_switch_d_080c7ebe_switchdata_d_080c7ecc_080c7ec8 |
| 080c7f38 | 02023130 | gDuelFieldState | REF_ADD | tick_card_display_transition_ptr_g_duel_field_state_080c7f38 |
| 080c7f40 | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c7f40 |
| 080c7f48 | 0600f00a | card_display_frame_bg_map_left | REF_ADD | tick_card_display_transition_ptr_card_display_frame_bg_map_left_080c7f48 |
| 080c7fc0 | 03000040 | gPrng | REF_PRESERVE | tick_card_display_transition_ptr_g_prng_080c7fc0 |
| 080c7fc4 | 02023130 | gDuelFieldState | REF_ADD | tick_card_display_transition_ptr_g_duel_field_state_080c7fc4 |
| 080c7fcc | 02023360 | gDuelSceneBase | REF_ADD | tick_card_display_transition_ptr_g_duel_scene_base_080c7fcc |
| 080c7fd0 | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c7fd0 |
| 080c8034 | 04000040 | WIN0H | REF_PRESERVE | tick_card_display_transition_ptr_w_i_n0_h_080c8034 |
| 080c8070 | 0600f00a | card_display_frame_bg_map_left | REF_ADD | tick_card_display_transition_ptr_card_display_frame_bg_map_left_080c8070 |
| 080c8078 | 080c807c | switchD_080c806a__switchdataD_080c807c | REF_ADD | tick_card_display_transition_ptr_switch_d_080c806a_switchdata_d_080c807c_080c8078 |
| 080c80c0 | 06014000 | AOB_CARD_TILE_VRAM | REF_ADD | tick_card_display_transition_ptr_a_o_b_c_a_r_d_t_i_l_e_v_r_a_m_080c80c0 |
| 080c8158 | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c8158 |
| 080c815c | 02023130 | gDuelFieldState | REF_ADD | tick_card_display_transition_ptr_g_duel_field_state_080c815c |
| 080c81d4 | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c81d4 |
| 080c81dc | 080c81e0 | switchD_080c81c6__switchdataD_080c81e0 | REF_ADD | tick_card_display_transition_ptr_switch_d_080c81c6_switchdata_d_080c81e0_080c81dc |
| 080c8270 | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c8270 |
| 080c829c | 0201f440 | gFontState | REF_ADD | tick_card_display_transition_ptr_g_font_state_080c829c |
| 080c82d4 | 04000048 | WININ | REF_PRESERVE | tick_card_display_transition_ptr_w_i_n_i_n_080c82d4 |
| 080c8310 | 0201f440 | gFontState | REF_ADD | tick_card_list_display_master_ptr_g_font_state_080c8310 |
| 080c8330 | 02023130 | gDuelFieldState | REF_ADD | tick_card_list_display_master_ptr_g_duel_field_state_080c8330 |
| 080c8364 | 03000040 | gPrng | REF_PRESERVE | tick_card_list_display_master_ptr_g_prng_080c8364 |
| 080c8380 | 080c8384 | switchD_080c837a__switchdataD_080c8384 | REF_ADD | tick_card_list_display_master_ptr_switch_d_080c837a_switchdata_d_080c8384_080c8380 |
| 080c8444 | 0201f440 | gFontState | REF_ADD | animate_card_display_frame_close_ptr_g_font_state_080c8444 |
| 080c8490 | 0600f00a | card_display_frame_bg_map_left | REF_ADD | animate_card_display_frame_close_ptr_card_display_frame_bg_map_left_080c8490 |
| 080c8548 | 0600f000 | card_display_frame_bg_map | REF_ADD | animate_card_display_frame_close_ptr_card_display_frame_bg_map_080c8548 |
| 080c85fc | 0201fe5b | gCardDisplayFrameStepLo | REF_ADD | animate_card_display_frame_close_ptr_g_card_display_frame_step_lo_080c85fc |
| 080c8600 | 0201fe5c | gCardDisplayFrameStepHi | REF_ADD | animate_card_display_frame_close_ptr_g_card_display_frame_step_hi_080c8600 |
| 080c8668 | 0600f020 | card_display_frame_bg_map_right | REF_ADD | animate_card_display_frame_close_ptr_card_display_frame_bg_map_right_080c8668 |
| 080c8740 | 0201c4e0 | gP1LifePoints | REF_PRESERVE | tick_card_list_scene_frame_ptr_g_p1_life_points_080c8740 |
| 080c8748 | 03000040 | gPrng | REF_PRESERVE | tick_card_list_scene_frame_ptr_g_prng_080c8748 |
| 080c874c | 02023130 | gDuelFieldState | REF_ADD | tick_card_list_scene_frame_ptr_g_duel_field_state_080c874c |
| 080c8754 | 09e5aba4 | card_display_scene_phase_handlers | REF_ADD | tick_card_list_scene_frame_ptr_card_display_scene_phase_handlers_080c8754 |
| 080c8758 | 0201f440 | gFontState | REF_ADD | tick_card_list_scene_frame_ptr_g_font_state_080c8758 |
| 080c8794 | 02023130 | gDuelFieldState | REF_ADD | tick_card_list_scene_frame_ptr_g_duel_field_state_080c8794 |
| 080c8828 | 06012240 | duel_field_aux_obj_tiles_14x2_a | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tiles_14x2_a_080c8828 |
| 080c882c | 09889480 | duel_field_aux_obj_tile_data_14x2_a | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tile_data_14x2_a_080c882c |
| 080c8830 | 06010140 | duel_field_aux_obj_tiles_6x4 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tiles_6x4_080c8830 |
| 080c8834 | 09889cd8 | duel_field_aux_obj_tile_data_6x4 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tile_data_6x4_080c8834 |
| 080c8838 | 06011000 | OPP_CARD_LABEL_TILE_VRAM_A | REF_ADD | init_duel_field_lp_aob_ctx_ptr_o_p_p_c_a_r_d_l_a_b_e_l_t_i_l_e_v_r_a_m_a_080c8838 |
| 080c883c | 09889800 | duel_field_aux_obj_tile_data_14x2_b | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tile_data_14x2_b_080c883c |
| 080c8840 | 020230f8 | gDuelFieldAuxAobCtx | REF_ADD | init_duel_field_lp_aob_ctx_ptr_g_duel_field_aux_aob_ctx_080c8840 |
| 080c8844 | 09889b80 | zone_display_pair_marker_ptnsect | REF_ADD | init_duel_field_lp_aob_ctx_ptr_zone_display_pair_marker_ptnsect_080c8844 |
| 080c884c | 0201c4e0 | gP1LifePoints | REF_PRESERVE | init_duel_field_lp_aob_ctx_ptr_g_p1_life_points_080c884c |
| 080c8854 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | init_duel_field_lp_aob_ctx_ptr_g_duel_card_ctx_base_080c8854 |
| 080c8858 | 06011b40 | duel_field_aux_obj_tiles_4x1 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tiles_4x1_080c8858 |
| 080c885c | 0990c42c | duel_field_aux_obj_tile_data_4x1 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tile_data_4x1_080c885c |
| 080c8860 | 060111c0 | duel_field_aux_obj_tiles_10x1 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tiles_10x1_080c8860 |
| 080c8864 | 09850c7c | duel_field_aux_obj_tile_data_10x1 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tile_data_10x1_080c8864 |
| 080c8868 | 06011800 | OPP_CARD_LABEL_TILE_VRAM_C | REF_ADD | init_duel_field_lp_aob_ctx_ptr_o_p_p_c_a_r_d_l_a_b_e_l_t_i_l_e_v_r_a_m_c_080c8868 |
| 080c886c | 09854590 | duel_field_aux_obj_tile_data_16x4 | REF_ADD | init_duel_field_lp_aob_ctx_ptr_duel_field_aux_obj_tile_data_16x4_080c886c |
| 080c88b8 | 0201c4f0 | gP1SlotCountBase | REF_ADD | render_player_zone_active_oam_ptr_g_p1_slot_count_base_080c88b8 |
| 080c88c0 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_player_zone_active_oam_ptr_g_duel_card_ctx_base_080c88c0 |
| 080c8900 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_player_zone_active_oam_ptr_g_duel_card_ctx_base_080c8900 |
| 080c89a0 | 02023130 | gDuelFieldState | REF_ADD | refresh_all_zone_slot_tile_display_ptr_g_duel_field_state_080c89a0 |
| 080c89e4 | 0202317c | gDuelZoneFirstVisibleSlotByPlayer | REF_ADD | query_player_slot_activation_bitmask_ptr_g_duel_zone_first_visible_slot_by_player_080c89e4 |
| 080c8a9c | 020230c0 | gDuelZoneActivationState | REF_ADD | update_zone_activation_display_state_ptr_g_duel_zone_activation_state_080c8a9c |
| 080c8aa0 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | update_zone_activation_display_state_ptr_g_duel_card_ctx_base_080c8aa0 |
| 080c8ae8 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_duel_field_slot_oam_grid_ptr_g_duel_card_ctx_base_080c8ae8 |
| 080c8aec | 020230c0 | gDuelZoneActivationState | REF_ADD | render_duel_field_slot_oam_grid_ptr_g_duel_zone_activation_state_080c8aec |
| 080c8af0 | 080c8af4 | switchD_080c8ae4__switchdataD_080c8af4 | REF_ADD | render_duel_field_slot_oam_grid_ptr_switch_d_080c8ae4_switchdata_d_080c8af4_080c8af0 |

VRAM指针及ANALYSIS switch table指针受现行导出器resolve_word_symbol域限制. 后续结构模型必须逐槽调用真实导出器AST并生成有界fallback/pin, 保持全部继承pin. 不全局放开VRAM或任意switch.

### RENAME_SLOTS / CASE

151池槽USER名及EOL完整见slots.tsv; 74CASE保留值/类型/引用, 其中080c7b30命名card_display_frame_mode_call_table, 080c8af8命名render_duel_field_slot_oam_grid_second_monster_vector. 其他72个CASE不新建槽primary.

### FUNC_RENAME

| entry | old | new | native indeg / raw Fn+1 | 理由 |
|---|---|---|---|---|
| 080c7af8 | copy_card_frame_tiles_by_type | init_card_display_frame_by_mode | 0 / 1 | 0x0a01消费者为显示模式, 先复制BG框9tiles再执行模式分支; 原名by_type和OBJ描述矛盾. |
| 080c7ba8 | render_card_list_face_row_by_mode | animate_card_display_frame_open | 0 / 1 | 回调表phase1执行; 三phase逐步从右侧条带扩宽至完整BG框, 与phase3收回逆向对称. |
| 080c7ea0 | dispatch_card_display_state_by_mode | tick_card_display_transition | 1 / 0 | 0x0a1a bits8:1索引7个跨帧状态; 本体写BG/窗口/状态, 不是仅委派callee. |
| 080c841c | render_card_list_face_row_by_mode_alt | animate_card_display_frame_close | 0 / 1 | 回调表phase3执行; 先擦外沿/再收窄两半边框/最后清右侧3列; 原face renderer alt不表达方向. |

### PLATE (R5)

15个完整重写: 段内12个, 必要外部context3个. 14个RenameKnownFunctions既有tuple替换; 8870没有tuple, 新增1条. 只改批准tuple, 不改历史产品脚本. 所有after文本与registry before完整列于plates.tsv.

- 080c7af8 init_card_display_frame_by_mode, confidence high, asm/16_duelfield_zone.s:13644
  `Initialize the card-display frame by copying 0x120 bytes from card_display_frame_bg_tile_data to card_display_frame_bg_tiles. Read gFontState+0xa01 as display mode and dispatch through 14 even-address vectors to ten inline Thumb call stubs. Mode11 and modes above13 skip text rendering. Return1. The copied tiles are BG tiles0x13e..0x146 in character block2, not OBJ tiles.`
- 080c7ba8 animate_card_display_frame_open, confidence high, asm/16_duelfield_zone.s:13695
  `Animate opening of the card-display BG frame on screenblock30. Read phase bits16:9 from gFontState+0xa18 and row count at+0xa03. Phases0..2 draw the right strip, expand the split borders, then finish the outer edges. Phase1 advances the split counter in+0xa1b bits7:1 and+0xa1c bit0, preserving the other bits. Return0 while a valid phase runs, and1 after all three phases.`
- 080c7ea0 tick_card_display_transition, confidence high, asm/16_duelfield_zone.s:14124
  `Tick the seven detail states in gFontState+0xa1a bits8:1. Refresh and clear the BG frame, test input bit0x200 at gPrng+0x146, configure WIN0, initialize the selected display mode, render its text, and advance its effect. Display modes use the separate byte at+0xa01. State5 or an invalid state disables WIN0, clears the detail-state bits and returns0; active paths return1.`
- 080c82e4 tick_card_list_display_master, confidence high, asm/16_duelfield_zone.s:14664
  `Tick the master state packed in gFontState+0xa17 bits7:1 and+0xa18 bit0. State0 calls dispatch_card_display_oam_by_mode, checks field flags at gDuelFieldState+0x222, then tests input bit0x200 at gPrng+0x148 before a14-mode OAM dispatch. State1 calls tick_card_display_transition; its zero result resets the master state while preserving adjacent flag bits. Other states return0.`
- 080c841c animate_card_display_frame_close, confidence high, asm/16_duelfield_zone.s:14816
  `Animate closing of the card-display BG frame on screenblock30. Phase bits16:9 at gFontState+0xa18 select outer-edge erasure, inward motion of the split borders, then clearing of the right strip. Row count is at+0xa03. Phase1 advances the split counter in+0xa1b bits7:1 and+0xa1c bit0, preserving the other bits. Return0 during phases0..2 and1 afterward.`
- 080c8688 tick_card_list_scene_frame, confidence high, asm/16_duelfield_zone.s:15160
  `Run card_display_scene_phase_handlers using gFontState+0xa18 bits8:1. A successful callback advances that phase and resets bits16:9, the split-frame counter and master state. Every non-null callback path sorts OAM. A null callback clears gFontState bit0 and field effect bit2, then returns0. If gP1LifePoints+0x1d08 is nonzero and the masked frame count divided by60 exceeds179, set field+0x222 bits3:2 to01. Active callbacks return1.`
- 080c879c init_duel_field_lp_aob_ctx, confidence high, asm/16_duelfield_zone.s:15302
  `Initialize duel-field auxiliary OBJ tiles with six tile_2d_row_copy calls:14x2,6x4,14x2,4x1,10x1 and16x4 tiles. Each row copies width*32 bytes and uses destination stride0x400. Initialize gDuelFieldAuxAobCtx from zone_display_pair_marker_ptnsect with palette2/tile base128; set ctx+0x13 bit0. Select animation1 when gP1LifePoints+0x1ce8 equals gDuelCardCtxBase+4 XOR1, otherwise0, then set ctx+0xe to2.`
- 080c8870 render_player_zone_active_oam, confidence high, asm/16_duelfield_zone.s:15412
  `Render a zone-type13 indicator for each player using gP1SlotCountBase+player*PLAYER_BLOCK_STRIDE. Counts above24 use attr2 base0xcc4; counts11..24 use0xcc0; other counts draw nothing. Add8 to attr2 for the player equal to gDuelCardCtxBase+4 XOR1. Coordinates come from resolve_zone_oam_base_coords_by_type(player,13,0); write_oam_entry_from_packed_args receives shape/size0x80. There is no LP comparison or coordinate highlight shift.`
- 080c8904 refresh_all_zone_slot_tile_display, confidence high, asm/16_duelfield_zone.s:15491
  `Refresh empty field slots for both players, types0..4 then5..10. Combine gDuelFieldState+0x21e bits15:2 with+0x220 bits1:0. For types0..4, its player*8+type bit selects r2=0xff or0 for get_zone_slot_entity_ref_by_type; types5..10 use r2=0. When the entity reference is0, call update_field_slot_tile_display(player,type,0). No inputs or return value.`
- 080c89a8 query_player_slot_activation_bitmask, confidence high, asm/16_duelfield_zone.s:15578
  `Return a seven-bit activation mask for r0=player. Read its first visible slot from gDuelZoneFirstVisibleSlotByPlayer+player*2. For index0..6 call dispatch_zone_activation_by_state(player,11,first_slot+index), test result bit11, and set the matching output bit. The zone argument is always11; the visible slot number is passed in r2.`
- 080c89e8 update_zone_activation_display_state, confidence high, asm/16_duelfield_zone.s:15614
  `Build two activation-display words at gDuelZoneActivationState+0x30/+0x34. Map players against gDuelCardCtxBase+4 XOR1. For types0..10, test bit11 from dispatch_zone_activation_by_state(mapped_player,type,0). Add the seven visible-slot bits returned by query_player_slot_activation_bitmask(mapped_player) in bits17:11. Preserve only the low11 direct-slot bits before combining. No inputs.`
- 080c8aa8 render_duel_field_slot_oam_grid, confidence high, asm/16_duelfield_zone.s:15718
  `Render activation indicators selected by gDuelZoneActivationState+0x30/+0x34 for both mapped players. Bits0..10 select field slots; group types0..4,5..9 and10 before resolving coordinates. Field6 for types0..4 selects coordinate offsets, shape/size and attr2. Bits11..17 select seven scrolled visible slots using transform_zone_oam_coords_by_player(player,11,index). Append entries with write_oam_entry_from_packed_args. No inputs.`
- 0803b3a8 get_zone_slot_entity_ref_by_type, confidence high, asm/03_equip_chain_hand.s:11743, asm/03_equip_chain_hand.s:11839, asm/03_equip_chain_hand.s:11872
  `Read the low13-bit entity reference from a selected zone slot. r0=player, r1=zone type and r2=subindex; r3 is scratch. Types11..15 select the field-array, chain, set-code, hand or alternate-hand arrays. Other types use type+subindex: indices0..10 address gDuelFieldSlots at stride20, and higher indices select gDuelEffectChainSlots through the current chain context. Per-player arrays use PLAYER_BLOCK_STRIDE. Return the selected word masked with0x1fff.`
- 080f616c write_oam_entry_from_packed_args, confidence high, asm/21_font_title_scene.s:4875, asm/21_font_title_scene.s:4906, asm/21_font_title_scene.s:4911
  `Append one OAM entry to the buffer addressed by gPrng+0x1bc. r0 packs x in low16 and y in high16; r1 packs attr0 upper bits in its high byte and attr1 upper bits in its low byte; r2 supplies attr2. Merge y low8 and x low9, store the three halfwords at stride8, then increment the byte count at buffer+0x400. r1 encodes OBJ shape/size and other upper attribute bits, rather than a tile index.`
- 080f7da4 init_aob_ctx_from_ptnsect, confidence high, asm/21_font_title_scene.s:8991, asm/21_font_title_scene.s:8994, asm/21_font_title_scene.s:9366, asm/21_font_title_scene.s:9523, asm/21_font_title_scene.s:9546
  `Initialize the0x14-byte AOB context r0 from the pattern section r1. r2 high16 supplies the tile base at ctx+0x10; its low4 supplies the palette index in ctx+0x12 bits3:0. Set ctx+0x12 bit7 when u16(r1+u32(r1+8)) exceeds16; render_aob_frame_to_oam maps it to attr0 bit13. Copy r3 bit0 into bit6, set ctx+0xe to1, then resolve pattern0.`

## disasm计划 (R4)

clearListing仅[080c7b68,080c7ba2), setTMode=1同范围, 每stub独立DisassembleCommand, followFlow=false, 不运行analysis. 全部新引用均为原生ordinary CALL/JUMP; 不设置CALL_RETURN. 既有7af8 body从42B扩到100B, 半开范围[7af8,7b1c)+[7b68,7ba8). 排除[7b1c,7b68)池和表. 完整ABI与既有指令属性保持.

| stub | size | callee | USER label |
|---|---:|---|---|
| 080c7b68 | 6 | render_jp_label_row_with_tile_pos (080cd870) | init_card_display_frame_by_mode_label_row |
| 080c7b6e | 6 | render_card_entry_jp_labels_to_bg (080cea50) | init_card_display_frame_by_mode_entry_labels |
| 080c7b74 | 6 | render_card_name_jp_to_bg_tile_vram (080cf9f4) | init_card_display_frame_by_mode_card_name |
| 080c7b7a | 6 | render_card_label_text_to_bg (080ce218) | init_card_display_frame_by_mode_label_text |
| 080c7b80 | 6 | render_jp_label_row_with_tile_count (080cda6c) | init_card_display_frame_by_mode_label_row_count |
| 080c7b86 | 6 | render_duel_zone_card_detail_to_vram (080cffd4) | init_card_display_frame_by_mode_zone_detail |
| 080c7b8c | 6 | render_jp_two_line_text_to_bg_vram (080d04dc) | init_card_display_frame_by_mode_two_line_text |
| 080c7b92 | 6 | render_jp_two_line_text_to_bg_vram_alt (080ccfe4) | init_card_display_frame_by_mode_two_line_text_alt |
| 080c7b98 | 6 | render_card_name_label_to_bg (080cd33c) | init_card_display_frame_by_mode_name_label |
| 080c7b9e | 4 | render_card_stat_label_with_value (080cf3b0) | init_card_display_frame_by_mode_stat_label |

公共7ba2命名init_card_display_frame_by_mode_done. 11个code USER与151槽USER/20目标USER合计182个newUSER, 加4个Function改名共186个primary节点.

## carve计划 (R7)

仅[09e5aba4,09e5abb8),20B. 四个Thumb callback和终止0. 前驱菜单表结束a4, 独立后继表bb8由91e0/91e2/91ec消费者选择. 本表由8688的86c2/86d4/86e0/86e2读取, 86ea..86fe仅在callback成功后递增phase, 86d8检测null终止.

```asm
.global card_display_scene_phase_handlers
card_display_scene_phase_handlers:
    .word init_card_display_frame_by_mode+1
    .word animate_card_display_frame_open+1
    .word tick_card_list_display_master+1
    .word animate_card_display_frame_close+1
    .word 0
.incbin "roms/2343.gba", 0x1E5ABB8, 0x44
```

Ghidra首word已有/dword保持, 后4word实际data_at=NULL, 仅新增/dword四个. 四个非零槽新增USER DATA ref指向保存的odd地址, zero不加ref. 不创建odd USER label. 必须投影odd动态offcut Label/DEFAULT和even_function全ABI. Root已采prospective public ID事实, 结构模型绑定后精确使用, 不从POST接受未知DEFAULT身份.

## 新增constants/全局

| value | name | 文件 | 依据 |
|---|---|---|---|
| 0x0000013f | CARD_DISPLAY_FRAME_FIRST_ROW_MIDDLE_TILE | constants/card_info.inc | First row middle tile in the card-display frame. |
| 0x00000141 | CARD_DISPLAY_FRAME_MIDDLE_ROW_LEFT_TILE | constants/card_info.inc | Middle row left tile; existing EQUIP_CARD_DISPLAY_SUB_ID_141 is a different card-display operation argument. |
| 0x00000143 | CARD_DISPLAY_FRAME_MIDDLE_ROW_RIGHT_TILE | constants/card_info.inc | Middle row right tile in the card-display frame. |
| 0x00000145 | CARD_DISPLAY_FRAME_LAST_ROW_MIDDLE_TILE | constants/card_info.inc | Last row middle tile in the card-display frame. |
| 0x00000a03 | FONT_STATE_DISPLAY_ROW_COUNT_OFF | constants/card_info.inc | Display frame row count byte relative to gFontState. |
| 0x00000a17 | FONT_STATE_DISPLAY_MASTER_PACKED_OFF | constants/card_info.inc | Master-state low byte; state uses bits7:1 plus next byte bit0. |
| 0x00000a18 | FONT_STATE_DISPLAY_PHASES_PACKED_OFF | constants/card_info.inc | Packed scene phase bits8:1 and frame phase bits16:9. |
| 0x00000a1a | FONT_STATE_DISPLAY_DETAIL_PACKED_OFF | constants/card_info.inc | Packed detail state in bits8:1. |
| 0x00000a1b | FONT_STATE_DISPLAY_FRAME_STEP_LO_OFF | constants/card_info.inc | Split-frame step low seven bits in byte bits7:1. |
| 0x00000a1c | FONT_STATE_DISPLAY_FRAME_STEP_HI_OFF | constants/card_info.inc | Split-frame step high bit in byte bit0. |
| 0x00000cc4 | DUEL_ZONE_ACTIVE_HIGH_COUNT_ATTR2 | constants/duel_field.inc | Priority3 and tile0xc4 for active-zone counts above24; add8 for mapped player1. |
| 0x0201fe5b | gCardDisplayFrameStepLo | constants/ewram.inc | gFontState+0xa1b; frame-step bits7:1, preserving detail-state bit0. |
| 0x0201fe5c | gCardDisplayFrameStepHi | constants/ewram.inc | gFontState+0xa1c; frame-step bit0, preserving bits7:1. |
| 0x0600a7c0 | card_display_frame_bg_tiles | constants/gba_mem.inc | BG character block2 tiles0x13e..0x146, 0x120-byte copy destination. |
| 0x0600f000 | card_display_frame_bg_map | constants/gba_mem.inc | BG screenblock30 tilemap origin; frame split-border writes use row stride0x40. |
| 0x0600f00a | card_display_frame_bg_map_left | constants/gba_mem.inc | BG screenblock30 column5 anchor; opening edge finish and closing edge erase. |
| 0x0600f020 | card_display_frame_bg_map_right | constants/gba_mem.inc | BG screenblock30 column16 anchor for the three-tile right strip. |
| 0x06010140 | duel_field_aux_obj_tiles_6x4 | constants/gba_mem.inc | Six-tile-wide/four-row auxiliary OBJ destination with stride0x400. |
| 0x06011000 | OPP_CARD_LABEL_TILE_VRAM_A | REUSE_EXISTING_EQU | Reuse existing GNU address alias; add missing USER primary at the actual DEFAULT target. |
| 0x060111c0 | duel_field_aux_obj_tiles_10x1 | constants/gba_mem.inc | Ten-tile-wide/one-row auxiliary OBJ destination. |
| 0x06011800 | OPP_CARD_LABEL_TILE_VRAM_C | REUSE_EXISTING_EQU | Reuse existing GNU address alias; add missing USER primary at the actual DEFAULT target. |
| 0x06011b40 | duel_field_aux_obj_tiles_4x1 | constants/gba_mem.inc | Four-tile-wide/one-row auxiliary OBJ destination. |
| 0x06012240 | duel_field_aux_obj_tiles_14x2_a | constants/gba_mem.inc | First fourteen-tile-wide/two-row auxiliary OBJ destination. |
| 0x09850c7c | duel_field_aux_obj_tile_data_10x1 | constants/rom_data.inc | Source for the ten-tile-wide/one-row copy to0x060111c0. |
| 0x09854590 | duel_field_aux_obj_tile_data_16x4 | constants/rom_data.inc | Source for the sixteen-tile-wide/four-row copy to OPP_CARD_LABEL_TILE_VRAM_C. |
| 0x09889480 | duel_field_aux_obj_tile_data_14x2_a | constants/rom_data.inc | Source for the first fourteen-tile-wide/two-row copy to0x06012240. |
| 0x09889800 | duel_field_aux_obj_tile_data_14x2_b | constants/rom_data.inc | Source for the second fourteen-tile-wide/two-row copy to OPP_CARD_LABEL_TILE_VRAM_A. |
| 0x09889cd8 | duel_field_aux_obj_tile_data_6x4 | constants/rom_data.inc | Source for the six-tile-wide/four-row copy to0x06010140. |
| 0x09889fd8 | card_display_frame_bg_tile_data | constants/rom_data.inc | Nine 4bpp BG frame tiles copied to0x0600a7c0; raw nibble extraction confirms the border pieces. |
| 0x0990c42c | duel_field_aux_obj_tile_data_4x1 | constants/rom_data.inc | Source for the four-tile-wide/one-row copy to0x06011b40. |
| 0x09e5aba4 | card_display_scene_phase_handlers | DEFINE_GLOBAL_CARVE_LABEL | R7 table: four Thumb callbacks and a null terminator, consumed by tick_card_list_scene_frame. |

0x141的既有EQUIP_CARD_DISPLAY_SUB_ID_141用于不同的操作参数, 不表示frame tile; 新建按本消费者角色命名的alias. 其他所有可复用值均复用现有inc, 不造重复alias.

## 指令EOL与消费者证据 (R6)

63个既有指令EOL+19个新指令EOL逐PC固定如下, 其余既有EOL保持. 另151槽EOL+5个R7 word EOL, 合计238.

| PC | EOL ASCII |
|---|---|
| 080c7b00 | Copy0x120 bytes: nine BG tiles0x13e..0x146 in character block2. |
| 080c7b0c | Read the display-mode byte at gFontState+0xa01. |
| 080c7b1a | Even-address computed goto: retain Thumb state and dispatch through the mode table. |
| 080c7b68 | Display modes0,12,13: call render_jp_label_row_with_tile_pos. |
| 080c7b6c | Join the common success return without creating a Function. |
| 080c7b6e | Display modes3: call render_card_entry_jp_labels_to_bg. |
| 080c7b72 | Join the common success return without creating a Function. |
| 080c7b74 | Display modes5: call render_card_name_jp_to_bg_tile_vram. |
| 080c7b78 | Join the common success return without creating a Function. |
| 080c7b7a | Display modes6: call render_card_label_text_to_bg. |
| 080c7b7e | Join the common success return without creating a Function. |
| 080c7b80 | Display modes4: call render_jp_label_row_with_tile_count. |
| 080c7b84 | Join the common success return without creating a Function. |
| 080c7b86 | Display modes7: call render_duel_zone_card_detail_to_vram. |
| 080c7b8a | Join the common success return without creating a Function. |
| 080c7b8c | Display modes1,2: call render_jp_two_line_text_to_bg_vram. |
| 080c7b90 | Join the common success return without creating a Function. |
| 080c7b92 | Display modes8: call render_jp_two_line_text_to_bg_vram_alt. |
| 080c7b96 | Join the common success return without creating a Function. |
| 080c7b98 | Display modes9: call render_card_name_label_to_bg. |
| 080c7b9c | Join the common success return without creating a Function. |
| 080c7b9e | Display modes10: call render_card_stat_label_with_value. |
| 080c7bbe | Extract frame phase bits16:9 from gFontState+0xa18. |
| 080c7c98 | Write the opening frame strip: first row0x13e..0x140, middle0x141..0x143, last0x144..0x146. |
| 080c7db8 | Store frame-step low7 in bits7:1; preserve bit0 of gCardDisplayFrameStepLo. |
| 080c7dc8 | Store frame-step high bit0; preserve bits7:1 of gCardDisplayFrameStepHi. |
| 080c7e70 | Increment frame phase bits16:9; preserve scene phase and adjacent flags. |
| 080c7eac | Extract detail-state bits8:1, not display mode or bits14:8. |
| 080c7f26 | Clear25 tilemap entries per row at stride0x40. |
| 080c7f5a | Test bit0x200 from the halfword at gPrng+0x146. |
| 080c7f9c | Pass the packed cursor halfword from gDuelFieldState+0x210. |
| 080c7fba | Set detail state6 in bits8:1 while preserving bit0 and higher bits. |
| 080c7fee | WIN0H=0x28f0: horizontal bounds40..240. |
| 080c7ff4 | WIN0V=0x0090: vertical bounds0..144. |
| 080c7ffa | WININ=0x003d. |
| 080c8000 | WINOUT=0x003f. |
| 080c8010 | Enable WIN0 by setting DISPCNT bit13. |
| 080c802a | Advance detail-state bits8:1; preserve bit0 and bits15:9. |
| 080c80ba | Clear0x4000 bytes of AOB card OBJ tiles; the helper count is bytes. |
| 080c811e | Clear gFontState bit0 when display mode11 takes the empty initialization case. |
| 080c8184 | Draw25 frame entries per row using first/middle/last-row border tiles. |
| 080c81b0 | Advance detail-state bits8:1 before falling through to text rendering. |
| 080c826c | Advance detail-state bits8:1 after the selected text renderer. |
| 080c8296 | Effect complete: set detail state2 in bits8:1. |
| 080c82bc | Disable WIN0 by clearing DISPCNT bit13. |
| 080c82c8 | Clear detail-state bits8:1; preserve adjacent flags. |
| 080c8304 | Master state = (byte[a17]>>1) | ((byte[a18]&1)<<7). |
| 080c8346 | Test input bit0x200 at gPrng+0x148. |
| 080c8356 | Set master-state low7 to1 while preserving byte[a17] bit0. |
| 080c840e | Clear master-state high bit0 of byte[a18]; preserve bits7:1. |
| 080c8432 | Extract frame phase bits16:9 from gFontState+0xa18. |
| 080c84e8 | Closing frame uses4-step to reverse the opening split-border motion. |
| 080c85f0 | Store frame-step high bit0 and preserve bits7:1. |
| 080c8634 | Clear the three-tile right strip while closing. |
| 080c865c | Advance frame phase bits16:9; preserve scene phase and adjacent flags. |
| 080c86aa | Timeout when (frame_count&0x7fffffff)/60 exceeds179. |
| 080c86b6 | Negative13 masks byte bits3:2 with0xf3; it does not clear bit0. |
| 080c86c0 | Set gDuelFieldState+0x222 bits3:2 to01; this is not gFontState. |
| 080c86ce | Extract scene callback phase bits8:1 from gFontState+0xa18. |
| 080c86e2 | Invoke the phase callback through invoke_r0; the table stores Thumb address+1. |
| 080c86fe | Successful callback: advance scene phase bits8:1. |
| 080c8706 | Reset frame phase bits16:9 while preserving all other word bits. |
| 080c8714 | Reset frame-step low7 while preserving byte[a1b] bit0. |
| 080c8724 | Reset frame-step high bit0 while preserving byte[a1c] bits7:1. |
| 080c872e | Reset master low7 and preserve byte[a17] bit0. |
| 080c8734 | Reset master high bit0 in byte[a18]. |
| 080c8778 | Null phase callback: clear gFontState bit0. |
| 080c8788 | Null phase callback: clear gDuelFieldState+0x215 bit2. |
| 080c87cc | AOB palette2, tile base128, init flag1 from zone_display_pair_marker_ptnsect. |
| 080c87ea | Compare the orientation player at gP1LifePoints+0x1ce8 with gDuelCardCtxBase+4 XOR1. |
| 080c87f6 | Select animation0 or1 according to the player comparison. |
| 080c8890 | Compare player slot count with24; no LP-field comparison occurs here. |
| 080c88a4 | Attribute2 base0xcc4: priority3 and tile0xc4 for counts above24. |
| 080c88aa | Mapped player selects the next8 tiles through attr2+8. |
| 080c88cc | Unsigned range check accepts counts11..24. |
| 080c88e2 | Attribute2 base0xcc0: priority3 and tile0xc0 for counts11..24. |
| 080c8948 | Selected mask bit supplies r2=0xff to the entity lookup for types0..4. |
| 080c89bc | Use zone type11; r2 receives first_visible_slot+index. |
| 080c89c6 | Test activation result bit11 (0x800), then set the output index bit. |
| 080c8a82 | Pack the seven visible-slot mask bits into bits17:11. |
| 080c8b88 | Attribute2 becomes10 + 2*field6 for field-slot indicators. |
| 080c8bb2 | Visible-slot indicator coordinates use zone11 and the visible index. |

每个池槽consumer_PCs均用204Fn真实半开body归属, CASE使用明确indexed-load PC而非nearest-label. 全部high. 关键格式: a18 word bits8:1是scene phase, bits16:9是frame phase; a1a bits8:1是detail state; a17 bits7:1加a18 bit0是master state; a1b bits7:1加a1c bit0是frame step, 写入保留a1b bit0和a1c bits7:1.

R5必要context: get_zone_slot_entity_ref_by_type在3b49e/3b4a0返回low13; write_oam_entry_from_packed_args在f6176..618e/f61b4..61be用r1高/低byte组合attr0/attr1; init_aob_ctx_from_ptnsect的ctx+10由f8070读取并在f81aa..81c0乘32选OBJ tile目的, ctx+12 low4由f817e..8196放入attr2 palette. ctx+12 bit7由u16(r1+u32(r1+8))>16设置, f8036..8042将它映射到attr0 bit13; pattern count另读u16(r1+u32(r1+0)). 不改任何Function ABI.

## DEFAULT / typedPointer闭包

D70DC是唯一非Function来源的现有4B /undefined* pointer. 它指向0600f000, DATA/DEFAULT原引用保持; USER target命名后派生source primary由PTR_DAT_080d70dc变为PTR_card_display_frame_bg_map_080d70dc, ID/namespace/source均保持. 70ae的READ引用显示名同步投影, actual owner D7064 init_pack_card_info_bg_and_vram已在204Fn. 字节/类型/属性不改. 其他全闭包节点完整保护, 不能泛化清空或只核计数.

## R8静态图形核对

原ROM0x09889fd8的9个4bpp tiles按nibble直接解码为灰阶图f16-seg7-frame-tiles-view-v1.png, 已目视核对frame边框片段. 未断言实际palette颜色. 0x13e..0x146与06008000 character block2中的0600a7c0目的严格对应. 六组aux资源只按真实copy尺寸/消费者命名, 不臆造图像主题.

## Source范围与保护

正式落地由Root/fixer执行. 允许asm16本段/同模块自动符号显示, 外部asm03与asm21三处context PLATE, asm18的D70DC派生pool label及70ae引用, rom.s精确20B carve, 5个constants inc的新11 numeric+17 address equ, 14 registry替换+1追加, 两CSV各4个name cell, ghidra-functions父body_size42->100. 导出器所有继承pin保留; 全模块1747word表达式必须由实际AST逐项预测, 外部同值无refs的CA618/CAB04/CAC8C保持, 不能因全局value相同擅自符号化.

Runtime只涉及73 equate bindings,68段内USER DATA refs+4外表USER DATA refs,182 newUSER,4 rename,15 PLATE,238 EOL,19指令R4,4个DWORD创建及父body精确扩展. 所有原ROM字节/其他Function ABI/body/override/属性、source基线/DB和未许可状态保持. 原生写入/保存/构建/Git没有由executor执行.

## §5.1登记 (Rule 3)

无. 本段唯一raw块13个even真引用, 全部R4; 外部回调表由明确消费者20B R7.

## 求助

无低置信度语义. 独立review尚未执行; Root统一before manifest已冻结并绑定, 含204Fn Core/Properties-v3/Tiny-v2/prospective odd-symbols. 完整native POST预测器与生产脚本留给独立review通过后的fixer ModeB, 本静态提案不宣称actual native/save通过.

## Executor Report: F16-Seg-7

- 槽: EQ=73 REF_ADD=68 REF_PRESERVE=8 CASE_PRESERVE=74 SLOT_USER=151 FUNC_RENAME=4 PLATE=15.
- carve=1(20B), disasm=10stub/19instructions(58B), §5.1=0.
- 新增constants/global definitions: numeric.equ=11, address.equ=17, carve global label=1; USER targets=20.
- 求助: none.
- proposal: doc/dev/refine/F16-Seg-7.proposal.md.
