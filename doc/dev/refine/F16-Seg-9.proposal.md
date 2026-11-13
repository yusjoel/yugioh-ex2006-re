# Refine Proposal: F16-Seg-9 [080c9c94..080cad78)

本文为静态语义提案, 等待独立C1-C13审查. 不修改Ghidra/Program、源码流水线、ABI或body; 不自评分, 不声称生产验收.

## 段测绘

范围4324B, 13个既有Function, 167个word, 158个自动数据名(DAT128/PTR30), module raw0. 112个模块Function与1747个module word保留完整保护范围.

| entry | current name | proposed name |
|---|---|---|
| 080c9c94 | advance_card_display_effect_step | tick_card_description_window_effect |
| 080c9eb8 | write_decimal_digits_to_oam | write_decimal_digits_to_oam |
| 080c9f50 | render_card_view_scene_by_lp_time | render_duel_timer_oam |
| 080ca160 | render_lp_zone_digit_oam_row | render_player_zone_count_oam |
| 080ca28c | render_lp_numeric_oam | render_duel_turn_count_oam |
| 080ca348 | render_lp_value_digit_oam | render_duel_phase_highlight_oam |
| 080ca3a4 | render_prng_anim_oam_items | render_duel_result_history_oam |
| 080ca42c | render_lp_zone_oam_full | render_duel_hud_oam |
| 080ca4f4 | upload_player_icon_gfx_to_vram | upload_player_icon_gfx_to_vram |
| 080ca5f8 | write_lp_digit_tiles_to_vram | write_lp_digit_tiles_to_vram |
| 080ca660 | decode_card_image_tiles_to_vram | compose_compared_stat_digit_tiles |
| 080ca8ec | init_duel_field_tile_indices | init_duel_field_hud_tiles_and_palettes |
| 080cace8 | zero_card_display_vram_regions | zero_card_display_vram_regions |

全部167槽和158个自动名的地址/原值/消费者/完整before逐行见F16-Seg-9.slots.tsv. 9个switch CASE word按even地址和原namespace表达式保持.

## 数据块分类 (Rule 2/3)

| 范围 | raw / THUMB+1扫描 | 判定 | 证据 |
|---|---|---|---|
| module [080c9c94,080cad78) | 无ROM_INCBIN/.byte块 | R4/R7均0 | 源测绘及167word字节核对 |
| 13个Function入口 | THUMB+1全部0; 唯一even raw像素偶合 | 非新callback表 | function-pointer-scan-v1.json |

CA28C值的raw命中08511c7b位于已导出的6bpp图像tb0001.bin内部offset891. 4800B资产与ROM整块相等, 无native incoming; 不把像素偶合建立为函数引用. 26个ROM资源目标均做全ROM raw/+1扫描, 见冻结firststage request. 它们落既有graphics/bin容器或结构化指针表, 无新增资源carve. Seg8后的52B独立callback表不由本段读取.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

39个operand0 data-equate. 19种既有常量复用, 11种新常量; 值均独立读原ROM. 同值的历史专用alias不承担不同结构格式的语义.

| slot | value | constant | slot_label |
|---|---|---|---|
| 080c9d3c | 0x000028f0 | VIJA_INTRO_WIN0H_BOUNDS | tick_card_description_window_effect_vija_intro_win0h_bounds_080c9d3c |
| 080c9d40 | 0x00004ccc | CARD_DESCRIPTION_WIN0H_BOUNDS | tick_card_description_window_effect_card_description_win0h_bounds_080c9d40 |
| 080c9d44 | 0x00001878 | FIELD_BACKGROUND_WIN_V_BOUNDS | tick_card_description_window_effect_field_background_win_v_bounds_080c9d44 |
| 080c9d48 | 0x00002f3f | CARD_DESCRIPTION_WININ_FLAGS | tick_card_description_window_effect_card_description_winin_flags_080c9d48 |
| 080c9e64 | 0x00009fff | DISPCNT_WIN0_WIN1_CLEAR_MASK | tick_card_description_window_effect_dispcnt_win0_win1_clear_mask_080c9e64 |
| 080c9eb4 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | tick_card_description_window_effect_duel_field_ui_effect_flags_off_080c9eb4 |
| 080c9fbc | 0x00001d08 | P1LP_BLOCK2_OFF | render_duel_timer_oam_p1lp_block2_off_080c9fbc |
| 080c9fc0 | 0x00660028 | DUEL_TIMER_LOWER_FRAME_POS | render_duel_timer_oam_duel_timer_lower_frame_pos_080c9fc0 |
| 080ca0c8 | 0x0000049a | DUEL_TIMER_FRAME_ATTR2 | render_duel_timer_oam_duel_timer_frame_attr2_080ca0c8 |
| 080ca0d0 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | render_duel_timer_oam_duel_field_prng_anim_flag_off_080ca0d0 |
| 080ca0d8 | 0x00190028 | DUEL_TIMER_UPPER_FRAME_POS | render_duel_timer_oam_duel_timer_upper_frame_pos_080ca0d8 |
| 080ca15c | 0x0000049a | DUEL_TIMER_FRAME_ATTR2 | render_duel_timer_oam_duel_timer_frame_attr2_080ca15c |
| 080ca1f4 | 0x00000868 | PLAYER_BLOCK_STRIDE | render_player_zone_count_oam_player_block_stride_080ca1f4 |
| 080ca1f8 | 0x00008080 | OAM_PACKED_TALL_16X32_ATTR | render_player_zone_count_oam_oam_packed_tall_16x32_attr_080ca1f8 |
| 080ca1fc | 0x0000049e | DUEL_PLAYER_COUNT_LABEL_ATTR2 | render_player_zone_count_oam_duel_player_count_label_attr2_080ca1fc |
| 080ca280 | 0x00008080 | OAM_PACKED_TALL_16X32_ATTR | render_player_zone_count_oam_oam_packed_tall_16x32_attr_080ca280 |
| 080ca284 | 0x0000049e | DUEL_PLAYER_COUNT_LABEL_ATTR2 | render_player_zone_count_oam_duel_player_count_label_attr2_080ca284 |
| 080ca330 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | render_duel_turn_count_oam_p1lp_block2_off_1ce8_080ca330 |
| 080ca334 | 0x00001cec | P1LP_TIMER_OFF | render_duel_turn_count_oam_p1lp_timer_off_080ca334 |
| 080ca344 | 0x00008080 | OAM_PACKED_TALL_16X32_ATTR | render_duel_turn_count_oam_oam_packed_tall_16x32_attr_080ca344 |
| 080ca380 | 0x00001cf4 | DUEL_FIELD_CURSOR_STATE_OFF | render_duel_phase_highlight_oam_duel_field_cursor_state_off_080ca380 |
| 080ca3a0 | 0x00008080 | OAM_PACKED_TALL_16X32_ATTR | render_duel_phase_highlight_oam_oam_packed_tall_16x32_attr_080ca3a0 |
| 080ca3c4 | 0x00000241 | GPRNG_CHALLENGE_SCORE_OFF | render_duel_result_history_oam_gprng_challenge_score_off_080ca3c4 |
| 080ca428 | 0x0000023f | GPRNG_BANNER_FLAG_OFF | render_duel_result_history_oam_gprng_banner_flag_off_080ca428 |
| 080ca4cc | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | render_duel_hud_oam_duel_field_fadein_flag_off_080ca4cc |
| 080ca4d4 | 0x00001d14 | DUEL_TURN_STATE_OFF | render_duel_hud_oam_duel_turn_state_off_080ca4d4 |
| 080ca4dc | 0x0000023f | GPRNG_BANNER_FLAG_OFF | render_duel_hud_oam_gprng_banner_flag_off_080ca4dc |
| 080ca4e8 | 0x00002f51 | DUEL_CTX_ZONE_STATE_OFF | render_duel_hud_oam_duel_ctx_zone_state_off_080ca4e8 |
| 080ca65c | 0x0001869f | ZONE_SCORE_CEILING_99999 | write_lp_digit_tiles_to_vram_zone_score_ceiling_99999_080ca65c |
| 080ca804 | 0x0001869f | ZONE_SCORE_CEILING_99999 | compose_compared_stat_digit_tiles_zone_score_ceiling_99999_080ca804 |
| 080caac8 | 0x0000018d | DUEL_HUD_AUX_BG_FIRST_TILE | init_duel_field_hud_tiles_and_palettes_duel_hud_aux_bg_first_tile_080caac8 |
| 080caad4 | 0xfffff000 | BG_TILE_PALETTE15_EXTENDED_BITS | init_duel_field_hud_tiles_and_palettes_bg_tile_palette15_extended_bits_080caad4 |
| 080caadc | 0x00000147 | CARD_NAME_BG_FIRST_TILE | init_duel_field_hud_tiles_and_palettes_card_name_bg_first_tile_080caadc |
| 080caaec | 0x00000868 | PLAYER_BLOCK_STRIDE | init_duel_field_hud_tiles_and_palettes_player_block_stride_080caaec |
| 080cab0c | 0x0000141e | DUEL_HUD_BG_MAP_DIMENSIONS | init_duel_field_hud_tiles_and_palettes_duel_hud_bg_map_dimensions_080cab0c |
| 080cab20 | 0x00006e57 | DUEL_SCENE_FIELD_OFF_6E57 | init_duel_field_hud_tiles_and_palettes_duel_scene_field_off_6e57_080cab20 |
| 080cab24 | 0x00000213 | GPRNG_PRNG_STATE_OFF213 | init_duel_field_hud_tiles_and_palettes_gprng_prng_state_off213_080cab24 |
| 080cab28 | 0x00000212 | DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | init_duel_field_hud_tiles_and_palettes_duel_field_cursor_group_toggle_off_080cab28 |
| 080cab7c | 0x00000212 | DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | init_duel_field_hud_tiles_and_palettes_duel_field_cursor_group_toggle_off_080cab7c |

### REF_SLOTS

89个新增USER DATA引用, 30个既有DATA引用保持. 45个非USER目标新增USER primary; 33个既有USER全局保持身份. 原有Data_at/containing和typed边界全部保持. switch table基址使用原ANALYSIS名字, 不新增其primary; 其GAS需要精确地址fallback由后续source plan负责.

| slot | target | GAS name | action | slot_label |
|---|---|---|---|---|
| 080c9cb4 | 02023130 | gDuelFieldState | REF_ADD | tick_card_description_window_effect_ptr_g_duel_field_state_080c9cb4 |
| 080c9cb8 | 080c9cbc | switchD_080c9cb2__switchdataD_080c9cbc | REF_ADD | tick_card_description_window_effect_ptr_switch_d_080c9cb2_switchdata_d_080c9cbc_080c9cb8 |
| 080c9d38 | 04000042 | WIN1H | REF_PRESERVE | tick_card_description_window_effect_ptr_w_i_n1_h_080c9d38 |
| 080c9d4c | 04000052 | BLDALPHA | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_a_l_p_h_a_080c9d4c |
| 080c9d50 | 02023130 | gDuelFieldState | REF_ADD | tick_card_description_window_effect_ptr_g_duel_field_state_080c9d50 |
| 080c9d94 | 04000052 | BLDALPHA | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_a_l_p_h_a_080c9d94 |
| 080c9d98 | 04000050 | BLDCNT | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_c_n_t_080c9d98 |
| 080c9dc0 | 04000054 | BLDY | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_y_080c9dc0 |
| 080c9dd8 | 02023130 | gDuelFieldState | REF_ADD | tick_card_description_window_effect_ptr_g_duel_field_state_080c9dd8 |
| 080c9e10 | 04000054 | BLDY | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_y_080c9e10 |
| 080c9e14 | 04000050 | BLDCNT | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_c_n_t_080c9e14 |
| 080c9e50 | 04000052 | BLDALPHA | REF_PRESERVE | tick_card_description_window_effect_ptr_b_l_d_a_l_p_h_a_080c9e50 |
| 080c9e8c | 04000042 | WIN1H | REF_PRESERVE | tick_card_description_window_effect_ptr_w_i_n1_h_080c9e8c |
| 080c9fb8 | 0201c4e0 | gP1LifePoints | REF_PRESERVE | render_duel_timer_oam_ptr_g_p1_life_points_080c9fb8 |
| 080c9fc4 | 03000040 | gPrng | REF_PRESERVE | render_duel_timer_oam_ptr_g_prng_080c9fc4 |
| 080c9fc8 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_duel_timer_oam_ptr_g_duel_card_ctx_base_080c9fc8 |
| 080ca0cc | 02023130 | gDuelFieldState | REF_ADD | render_duel_timer_oam_ptr_g_duel_field_state_080ca0cc |
| 080ca0d4 | 02023360 | gDuelSceneBase | REF_ADD | render_duel_timer_oam_ptr_g_duel_scene_base_080ca0d4 |
| 080ca0dc | 03000040 | gPrng | REF_PRESERVE | render_duel_timer_oam_ptr_g_prng_080ca0dc |
| 080ca1ec | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_player_zone_count_oam_ptr_g_duel_card_ctx_base_080ca1ec |
| 080ca1f0 | 0201c4e0 | gP1LifePoints | REF_PRESERVE | render_player_zone_count_oam_ptr_g_p1_life_points_080ca1f0 |
| 080ca200 | 0201c4fc | gP1AltHandCountBase | REF_ADD | render_player_zone_count_oam_removed_card_count_base_080ca200 |
| 080ca288 | 0201c4fc | gP1AltHandCountBase | REF_ADD | render_player_zone_count_oam_removed_card_count_base_080ca288 |
| 080ca32c | 0201c4e0 | gP1LifePoints | REF_PRESERVE | render_duel_turn_count_oam_ptr_g_p1_life_points_080ca32c |
| 080ca338 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_duel_turn_count_oam_ptr_g_duel_card_ctx_base_080ca338 |
| 080ca33c | 02023130 | gDuelFieldState | REF_ADD | render_duel_turn_count_oam_ptr_g_duel_field_state_080ca33c |
| 080ca340 | 02023360 | gDuelSceneBase | REF_ADD | render_duel_turn_count_oam_ptr_g_duel_scene_base_080ca340 |
| 080ca37c | 0201c4e0 | gP1LifePoints | REF_PRESERVE | render_duel_phase_highlight_oam_ptr_g_p1_life_points_080ca37c |
| 080ca384 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_duel_phase_highlight_oam_ptr_g_duel_card_ctx_base_080ca384 |
| 080ca424 | 03000040 | gPrng | REF_PRESERVE | render_duel_result_history_oam_ptr_g_prng_080ca424 |
| 080ca4c8 | 02023130 | gDuelFieldState | REF_ADD | render_duel_hud_oam_ptr_g_duel_field_state_080ca4c8 |
| 080ca4d0 | 0201c4e0 | gP1LifePoints | REF_PRESERVE | render_duel_hud_oam_ptr_g_p1_life_points_080ca4d0 |
| 080ca4d8 | 03000040 | gPrng | REF_PRESERVE | render_duel_hud_oam_ptr_g_prng_080ca4d8 |
| 080ca4e0 | 02023360 | gDuelSceneBase | REF_ADD | render_duel_hud_oam_ptr_g_duel_scene_base_080ca4e0 |
| 080ca4e4 | 02020160 | gDuelCtx | REF_ADD | render_duel_hud_oam_ptr_g_duel_ctx_080ca4e4 |
| 080ca4ec | 0201f440 | gFontState | REF_ADD | render_duel_hud_oam_ptr_g_font_state_080ca4ec |
| 080ca4f0 | 0201ff30 | gCardCtxSlotData | REF_ADD | render_duel_hud_oam_ptr_g_card_ctx_slot_data_080ca4f0 |
| 080ca558 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | upload_player_icon_gfx_to_vram_ptr_g_duel_card_ctx_base_080ca558 |
| 080ca55c | 0600fb80 | duel_player_icon_bg_map_local | REF_ADD | upload_player_icon_gfx_to_vram_ptr_duel_player_icon_bg_map_local_080ca55c |
| 080ca560 | 0600f840 | duel_player_icon_bg_map_opponent | REF_ADD | upload_player_icon_gfx_to_vram_ptr_duel_player_icon_bg_map_opponent_080ca560 |
| 080ca5b8 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | upload_player_icon_gfx_to_vram_ptr_g_duel_card_ctx_base_080ca5b8 |
| 080ca5bc | 05000180 | BG_PALRAM_SLOT_12_BASE | REF_ADD | upload_player_icon_gfx_to_vram_ptr_b_g_p_a_l_r_a_m_s_l_o_t_12_b_a_s_e_080ca5bc |
| 080ca5c0 | 09896290 | icon_palettes_base | REF_PRESERVE | upload_player_icon_gfx_to_vram_ptr_icon_palettes_base_080ca5c0 |
| 080ca5c4 | 0600bae0 | duel_player_icon_bg_tiles_opponent | REF_ADD | upload_player_icon_gfx_to_vram_ptr_duel_player_icon_bg_tiles_opponent_080ca5c4 |
| 080ca5c8 | 0988cf30 | icon_tiles_base | REF_PRESERVE | upload_player_icon_gfx_to_vram_ptr_icon_tiles_base_080ca5c8 |
| 080ca5f0 | 0600b9c0 | duel_player_icon_bg_tiles_local | REF_ADD | upload_player_icon_gfx_to_vram_ptr_duel_player_icon_bg_tiles_local_080ca5f0 |
| 080ca5f4 | 0988cf30 | icon_tiles_base | REF_PRESERVE | upload_player_icon_gfx_to_vram_ptr_icon_tiles_base_080ca5f4 |
| 080ca618 | 0600f000 | card_display_frame_bg_map | REF_ADD | write_lp_digit_tiles_to_vram_ptr_card_display_frame_bg_map_080ca618 |
| 080ca61c | 0201e2a0 | gDuelCardCtxBase | REF_ADD | write_lp_digit_tiles_to_vram_ptr_g_duel_card_ctx_base_080ca61c |
| 080ca728 | 020232c0 | gDuelNumericTileScratch | REF_ADD | compose_compared_stat_digit_tiles_ptr_g_duel_numeric_tile_scratch_080ca728 |
| 080ca72c | 06008120 | card_stat_digit_bg_tiles_a | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_digit_bg_tiles_a_080ca72c |
| 080ca730 | 060081a0 | card_stat_digit_bg_tiles_b | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_digit_bg_tiles_b_080ca730 |
| 080ca734 | 0985117c | card_stat_equal_digit_tiles | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_equal_digit_tiles_080ca734 |
| 080ca808 | 0985131c | card_stat_greater_digit_tiles | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_greater_digit_tiles_080ca808 |
| 080ca80c | 0985117c | card_stat_equal_digit_tiles | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_equal_digit_tiles_080ca80c |
| 080ca810 | 0985145c | card_stat_less_digit_tiles | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_less_digit_tiles_080ca810 |
| 080ca814 | 020232c0 | gDuelNumericTileScratch | REF_ADD | compose_compared_stat_digit_tiles_ptr_g_duel_numeric_tile_scratch_080ca814 |
| 080ca8e4 | 0985117c | card_stat_equal_digit_tiles | REF_ADD | compose_compared_stat_digit_tiles_ptr_card_stat_equal_digit_tiles_080ca8e4 |
| 080ca8e8 | 020232c0 | gDuelNumericTileScratch | REF_ADD | compose_compared_stat_digit_tiles_ptr_g_duel_numeric_tile_scratch_080ca8e8 |
| 080caac4 | 0600e900 | duel_hud_aux_bg_map_6x4 | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_aux_bg_map_6x4_080caac4 |
| 080caacc | 0600fb00 | card_stat_digit_bg_map_a | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_card_stat_digit_bg_map_a_080caacc |
| 080caad0 | 0600fa80 | card_detail_symbol_bg_map | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_card_detail_symbol_bg_map_080caad0 |
| 080caad8 | 0600fc80 | card_detail_name_bg_map | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_card_detail_name_bg_map_080caad8 |
| 080caae0 | 0600f904 | card_level_bg_map | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_card_level_bg_map_080caae0 |
| 080caae4 | 0600f300 | card_stat_digit_bg_map_b | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_card_stat_digit_bg_map_b_080caae4 |
| 080caae8 | 0201c4e0 | gP1LifePoints | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_g_p1_life_points_080caae8 |
| 080caaf0 | 0985936c | duel_field_outer_palette_pointers | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_duel_field_outer_palette_pointers_080caaf0 |
| 080caaf4 | 02023130 | gDuelFieldState | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_g_duel_field_state_080caaf4 |
| 080caaf8 | 05000120 | BG_PALRAM_SLOT_9_BASE | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_b_g_p_a_l_r_a_m_s_l_o_t_9_b_a_s_e_080caaf8 |
| 080caafc | 06008220 | duel_field_outer_bg_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_field_outer_bg_tiles_080caafc |
| 080cab00 | 09855030 | duel_field_outer_tile_pointers | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_duel_field_outer_tile_pointers_080cab00 |
| 080cab04 | 0600f000 | card_display_frame_bg_map | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_card_display_frame_bg_map_080cab04 |
| 080cab08 | 09859548 | hud_phases_tilemap_pointers | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_hud_phases_tilemap_pointers_080cab08 |
| 080cab10 | 0600e000 | BG_SCREENBLOCK_28_BASE | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_b_g_s_c_r_e_e_n_b_l_o_c_k_28_b_a_s_e_080cab10 |
| 080cab14 | 0985b634 | duel_field_outer_tilemap_pointers | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_duel_field_outer_tilemap_pointers_080cab14 |
| 080cab18 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_g_duel_card_ctx_base_080cab18 |
| 080cab1c | 02000000 | EWRAM_BASE | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_e_w_r_a_m_b_a_s_e_080cab1c |
| 080cab2c | 0985d720 | campaign_inner_image | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_campaign_inner_image_080cab2c |
| 080cab70 | 09867580 | field_spell_background_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_field_spell_background_tiles_080cab70 |
| 080cab74 | 06009000 | field_background_tile_vram | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_field_background_tile_vram_080cab74 |
| 080cab78 | 02023130 | gDuelFieldState | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_g_duel_field_state_080cab78 |
| 080cab80 | 098674a0 | campaign_inner_palette | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_campaign_inner_palette_080cab80 |
| 080cac74 | 09889180 | field_spell_background_palettes | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_field_spell_background_palettes_080cac74 |
| 080cac78 | 05000140 | field_background_palette_ram | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_field_background_palette_ram_080cac78 |
| 080cac7c | 0600e0d4 | field_background_bg_map | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_field_background_bg_map_080cac7c |
| 080cac80 | 09850b1c | hud_life_points_font | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_hud_life_points_font_080cac80 |
| 080cac84 | 0600a680 | duel_lp_digit_bg_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_lp_digit_bg_tiles_080cac84 |
| 080cac88 | 0600b4c0 | duel_hud_number_bg_tiles_a | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_number_bg_tiles_a_080cac88 |
| 080cac8c | 09850c7c | duel_field_aux_obj_tile_data_10x1 | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_field_aux_obj_tile_data_10x1_080cac8c |
| 080cac90 | 0600b6e0 | duel_hud_decimal_bg_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_decimal_bg_tiles_080cac90 |
| 080cac94 | 09850e9c | duel_hud_decimal_bg_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_decimal_bg_tile_data_080cac94 |
| 080cac98 | 0600b820 | duel_hud_number_bg_tiles_b | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_number_bg_tiles_b_080cac98 |
| 080cac9c | 09850fdc | duel_hud_number_bg_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_number_bg_tile_data_080cac9c |
| 080caca0 | 05000200 | OBJ_PALRAM_BASE | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_o_b_j_p_a_l_r_a_m_b_a_s_e_080caca0 |
| 080caca4 | 0985159c | duel_hud_obj_palettes | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_hud_obj_palettes_080caca4 |
| 080caca8 | 05000300 | AOB_CARD_PAL_DST | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_a_o_b_c_a_r_d_p_a_l_d_s_t_080caca8 |
| 080cacac | 08510460 | shared_ui_palette_256 | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_shared_ui_palette_256_080cacac |
| 080cacb0 | 06010280 | duel_phase_label_obj_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_phase_label_obj_tiles_080cacb0 |
| 080cacb4 | 098519fc | hud_phases_highlight | REF_PRESERVE | init_duel_field_hud_tiles_and_palettes_ptr_hud_phases_highlight_080cacb4 |
| 080cacb8 | 060113c0 | duel_player_count_label_obj_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_player_count_label_obj_tiles_080cacb8 |
| 080cacbc | 0985263c | duel_player_count_label_obj_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_player_count_label_obj_tile_data_080cacbc |
| 080cacc0 | 06011340 | duel_timer_frame_obj_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_timer_frame_obj_tiles_080cacc0 |
| 080cacc4 | 0985289c | duel_timer_frame_obj_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_timer_frame_obj_tile_data_080cacc4 |
| 080cacc8 | 060115c0 | duel_decimal_digit_obj_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_decimal_digit_obj_tiles_080cacc8 |
| 080caccc | 0985273c | duel_decimal_digit_obj_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_decimal_digit_obj_tile_data_080caccc |
| 080cacd0 | 06010200 | OBJ_TILE_VRAM_BASE_PAGE2 | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_o_b_j_t_i_l_e_v_r_a_m_b_a_s_e_p_a_g_e2_080cacd0 |
| 080cacd4 | 0985299c | duel_main_phase_timer_obj_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_main_phase_timer_obj_tile_data_080cacd4 |
| 080cacd8 | 06010240 | duel_end_phase_timer_obj_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_end_phase_timer_obj_tiles_080cacd8 |
| 080cacdc | 09852a9c | duel_end_phase_timer_obj_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_end_phase_timer_obj_tile_data_080cacdc |
| 080cace0 | 06011f00 | duel_result_history_obj_tiles | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_result_history_obj_tiles_080cace0 |
| 080cace4 | 09854d90 | duel_result_history_obj_tile_data | REF_ADD | init_duel_field_hud_tiles_and_palettes_ptr_duel_result_history_obj_tile_data_080cace4 |
| 080cad58 | 0600a8e0 | card_detail_name_bg_tiles | REF_ADD | zero_card_display_vram_regions_ptr_card_detail_name_bg_tiles_080cad58 |
| 080cad5c | 02023130 | gDuelFieldState | REF_ADD | zero_card_display_vram_regions_ptr_g_duel_field_state_080cad5c |
| 080cad60 | 06006340 | card_detail_frame_bg_tiles | REF_ADD | zero_card_display_vram_regions_ptr_card_detail_frame_bg_tiles_080cad60 |
| 080cad64 | 06008120 | card_stat_digit_bg_tiles_a | REF_ADD | zero_card_display_vram_regions_ptr_card_stat_digit_bg_tiles_a_080cad64 |
| 080cad68 | 06008020 | PUZZLE_NAME_SPRITE_VRAM | REF_ADD | zero_card_display_vram_regions_ptr_p_u_z_z_l_e_n_a_m_e_s_p_r_i_t_e_v_r_a_m_080cad68 |
| 080cad6c | 0600f904 | card_level_bg_map | REF_ADD | zero_card_display_vram_regions_ptr_card_level_bg_map_080cad6c |
| 080cad70 | 0600fa40 | card_effect_counter_bg_map | REF_ADD | zero_card_display_vram_regions_ptr_card_effect_counter_bg_map_080cad70 |
| 080cad74 | 060081a0 | card_stat_digit_bg_tiles_b | REF_ADD | zero_card_display_vram_regions_ptr_card_stat_digit_bg_tiles_b_080cad74 |

### RENAME_SLOTS / CASE

158槽全部USER语义label和ASCII EOL, 9个CASE不加label/EOL, 不给even CASE加1. EWRAM_BASE与0x6e57保持base/offset两槽, 不合并. 槽名均匹配^[a-z][a-z0-9_]+$.

### FUNC_RENAME

| entry | old | new | native incoming |
|---|---|---|---:|
| 080c9c94 | advance_card_display_effect_step | tick_card_description_window_effect | 2 |
| 080c9f50 | render_card_view_scene_by_lp_time | render_duel_timer_oam | 2 |
| 080ca160 | render_lp_zone_digit_oam_row | render_player_zone_count_oam | 2 |
| 080ca28c | render_lp_numeric_oam | render_duel_turn_count_oam | 1 |
| 080ca348 | render_lp_value_digit_oam | render_duel_phase_highlight_oam | 1 |
| 080ca3a4 | render_prng_anim_oam_items | render_duel_result_history_oam | 1 |
| 080ca42c | render_lp_zone_oam_full | render_duel_hud_oam | 1 |
| 080ca660 | decode_card_image_tiles_to_vram | compose_compared_stat_digit_tiles | 4 |
| 080ca8ec | init_duel_field_tile_indices | init_duel_field_hud_tiles_and_palettes | 1 |

9个Function只改名称和注释. signatures仅文档, 所有parameter/return/storage/calling convention/ABI/body保持完整before. 它们的直接/间接引用来源和真实source owner由Root新API采集固定, 不用nearest label.

### PLATE (R5)

16个全ASCII PLATE全重写, 每条<=500. 13个段内函数加必要context3BC58/CB1CC/CAE84. 后者只订正参数与counter消费者, 不提前重命名下一段Function. registry AST精确12替换4追加; before完整tuple/Function见plates.tsv.

- 080c9c94 tick_card_description_window_effect, high, asm/16_duelfield_zone.s:18174
  `Run the nine-phase card-description window effect using gDuelFieldState+1 and its halfword counter at+2. Initialize the description tiles from card ID at+0x21c, enable WIN0/WIN1, fade into scrolling, wait for tick_card_description_scroll(0), then fade out and clear window bounds. Return0 while active. After phase8, clear field+0x215 bit2 and the card ID, disable blending, reset phase0, and return1. No inputs.`
- 080c9eb8 write_decimal_digits_to_oam, high, asm/16_duelfield_zone.s:18460
  `Append decimal digit sprites right-to-left, spaced4 pixels, through write_oam_entry_from_packed_args. r0=x, r1=y, r2=value, r3=minimum_digits, fifth stack argument=palette. Use tile0xae+digit and palette<<12; emit at least one digit, then pad with leading zero tiles to minimum_digits. Digits use signed division/remainder by10. Writes the active OAM buffer; no destination pointer argument.`
- 080c9f50 render_duel_timer_oam, high, asm/16_duelfield_zone.s:18538
  `Render two MM:SS countdowns from the masked frame counters at gPrng+0x214 and+0x210. Require gP1LifePoints+0x1d08 nonzero. The first has a180-second limit and calls check_card_play_condition_eligible(local_player). The second uses300 times scene+0x37 bits4:2 seconds, unless field+0x224 or scene+0x36 bit6 blocks it. Blink the final minute via gPrng+0x20c bit2. No inputs.`
- 080ca160 render_player_zone_count_oam, high, asm/16_duelfield_zone.s:18796
  `Render both players deck, Graveyard and Removed Cards counts from player-block+0x10,+0x14,+0x1c, with PLAYER_BLOCK_STRIDE. Compare loop index0..1 with gDuelCardCtxBase+4 to select upper/lower positions; use the player low bit for block lookup. Draw a16x32 marker, then the three counts at x236 with y116/108/100 or y41/33/25. No inputs.`
- 080ca28c render_duel_turn_count_oam, high, asm/16_duelfield_zone.s:18954
  `Render the duel turn-count marker and number. Read the turn counter at gP1LifePoints+0x1cec and display count+1 by default. Compare field+0x224 and scene+0x36 bit6 to select the alternate display count-(field_counter-1), tile0x12 and one-pixel vertical shift. Put the marker at x23, y11 or115 according to the turn player, then emit at least two decimal digits at x28. No inputs.`
- 080ca348 render_duel_phase_highlight_oam, high, asm/16_duelfield_zone.s:19063
  `Append the current duel-phase highlight sprite. Read the phase from gP1LifePoints+0x1cf4 and the turn player from+0x1ce8. Use x31,y=8+22*phase, a16x32 shape, and tile0x14+2*phase. Select palette2 when the turn player equals local_player XOR1, otherwise palette1. No inputs; writes the active OAM buffer.`
- 080ca3a4 render_duel_result_history_oam, high, asm/16_duelfield_zone.s:19121
  `Render result-history bytes at gPrng+0x241, including index0 when nonzero. The eight-bit count is(gPrng[0x23f]>>1)|((gPrng[0x240]&1)<<7). Skip state0. For each other state append tiles0xf7+state and0xf7+mapped_state at x8*index,y128 and24. Map1->2,2->1,3->3; other nonzero states map to0. No inputs.`
- 080ca42c render_duel_hud_oam, high, asm/16_duelfield_zone.s:19206
  `Render the duel HUD OAM unless field+0x21e bit0 masks it. With gP1LifePoints+0x1d14 nonzero, draw the phase and turn count, plus result history when enabled and scene+0x36 bit6 is clear. Three further context flags gate the player-counter rows. Render countdown timers only when scene+0x37 bits4:2 is nonzero. No inputs.`
- 080ca4f4 upload_player_icon_gfx_to_vram, high, asm/16_duelfield_zone.s:19306
  `Write a selected player portrait as a3x3 BG tilemap and copy its tiles/palette. r0=player,r1=icon_index; r2 is unused. Opponent comparison selects map0x0600f840 versus0x0600fb80, base tile0x1d7 versus0x1ce, and palette13 versus12. Copy0x120 bytes from icon_tiles_base+0x120*icon_index. Copy0x40 bytes from icon_palettes_base+32*icon_index into the selected BG palette destination. No decompression.`
- 080ca5f8 write_lp_digit_tiles_to_vram, high, asm/16_duelfield_zone.s:19445
  `Write five decimal LP digits into the selected BG tilemap row. r0=player,r1=value; clamp values above99999. Start at card_display_frame_bg_map+8 for local_player XOR1, otherwise+0x448. Store tile0x134+digit and step backward2 bytes, using signed remainder/division by10. No inputs beyond r0/r1; no OAM writes.`
- 080ca660 compose_compared_stat_digit_tiles, high, asm/16_duelfield_zone.s:19505
  `Compose comparison-styled stat digits into four BG tiles. r0=value,r1=baseline,r2=selector; selector chooses VRAM0x06008120 or0x060081a0 and the prefix glyph. Clamp above99999. Use distinct digit banks for value above/equal/below baseline;(-1,-1) uses the unknown-value glyph. Pack the narrow decimal glyphs through gDuelNumericTileScratch and transpose its128 bytes into four8x8 4bpp tiles. No card-image decoding or decompression.`
- 080ca8ec init_duel_field_hud_tiles_and_palettes, high, asm/16_duelfield_zone.s:19843
  `Initialize duel-field HUD BG maps, LP digit tiles, outer-field resources, player portraits, background tiles/palette, and shared OBJ glyph sheets. Select outer resources from the mode in field+0x220 and inner resources from field+0x212. Build the15x12 inner map with palette10. Copy phase labels and count/timer/result glyphs into fixed OBJ regions using tile_2d_row_copy. No inputs.`
- 080cace8 zero_card_display_vram_regions, high, asm/16_duelfield_zone.s:20348
  `Always clear0x800 bytes at0x0600a8e0. When field+8 is nonzero, also clear0x600 bytes at0x06006340 and0x100 bytes at each stat/name region, zero two level-map entries and four adjacent counter-map entries, clear the two stat prefixes, then reset field+8 to0. Calls zero_fill_by_halfword with byte counts; no BIOS fill call. No inputs.`
- 0803bc58 check_card_play_condition_eligible, high, asm/03_equip_chain_hand.s:12932, asm/03_equip_chain_hand.s:12978, asm/03_equip_chain_hand.s:13047
  `Eligibility predicate used by render_duel_timer_oam. r0=player. Reject nonzero display-sequence+0x808/+0x80c. If card-context[8+4*player]==1, require matching turn player and gP1LifePoints+0x1d10 nonzero,+0x1d18 equal3. For the local player, accept nonzero+0x1d4c or successful UI effect0x31/0x32. Otherwise require sprite-state+0x300 bit0 clear and check_player_side_condition nonzero. Return0/1; may trigger UI effects.`
- 080cb1cc render_large_card_display_by_mode, high, asm/16_duelfield_zone.s:20991, asm/16_duelfield_zone.s:21719, asm/16_duelfield_zone.s:21848
  `Render the selected card BG detail panel. r0=internal card ID,r1=card-record pointer,r2=render override. Read type, level, attributes and signed ATK/DEF from card_stats_table and the runtime record. Draw the name, frame, compared stat digits through compose_compared_stat_digit_tiles, level and counter/type glyphs according to record flags. Hidden and non-monster paths clear or replace the relevant fields. Writes fixed BG VRAM/palette regions; no OAM enqueue.`
- 080cae84 write_card_digit_tiles_to_vram, high, asm/16_duelfield_zone.s:20547, asm/16_duelfield_zone.s:20577, asm/16_duelfield_zone.s:20650
  `Render a field-card counter into four BG entries at card_effect_counter_bg_map. r0 low bit selects player,r1 selects a20-byte slot; read its low13-bit card ID and halfword+0xc counter. Reverse the counter as3-count for CID0x1909, clamp above999, and choose a prefix for effect/equip categories. Write decimal tiles based at0x1a6 right-to-left. A nonpositive counter clears all four entries. No source/destination pointer arguments.`

## carve计划 (R7)

无. 不切割已导出的graphics/bin容器, 不重复Seg8已carve的16B表, 不改变后52B.

## disasm计划 (R4)

无. 不改TMode、Function数量、body或flow override. 源.hword是既有Thumb high-register指令表示, 117条静态位域解码用于R6, 不视作raw块.

## 新增constants / 全局

| value/address | name | GNU action | file | meaning |
|---|---|---|---|---|
| 0x00000147 | CARD_NAME_BG_FIRST_TILE | new numeric equate | constants/duel_field.inc | BG tile0x147 starts at0x0600a8e0 and supplies the two30-entry card-name rows. |
| 0x0000018d | DUEL_HUD_AUX_BG_FIRST_TILE | new numeric equate | constants/duel_field.inc | First sequential tile for the six-row by four-column HUD map. |
| 0x0000049a | DUEL_TIMER_FRAME_ATTR2 | new numeric equate | constants/duel_field.inc | Timer marker tile0x9a with priority1; 4x2 OBJ sheet at0x06011340. |
| 0x0000049e | DUEL_PLAYER_COUNT_LABEL_ATTR2 | new numeric equate | constants/duel_field.inc | Player-counter label tile0x9e with priority1;16x32 OBJ sheet at0x060113c0. |
| 0x0000141e | DUEL_HUD_BG_MAP_DIMENSIONS | new numeric equate | constants/duel_field.inc | Packed dimensions lowbyte30 columns, highbyte20 rows. |
| 0x00002f3f | CARD_DESCRIPTION_WININ_FLAGS | new numeric equate | constants/duel_field.inc | WIN0 all layers/effects0x3f; WIN1 flags0x2f exclude OBJ. |
| 0x00004ccc | CARD_DESCRIPTION_WIN0H_BOUNDS | new numeric equate | constants/duel_field.inc | WIN0H left76,right204. |
| 0x00008080 | OAM_PACKED_TALL_16X32_ATTR | new numeric equate | constants/duel_field.inc | Packed attr0/attr1 upper bytes for a16x32 tall OBJ. Existing CARD_IMAGE_RIGHT_COLUMN_OBJ_ATTR names a separate card-image role. |
| 0x00190028 | DUEL_TIMER_UPPER_FRAME_POS | new numeric equate | constants/duel_field.inc | Packed x40,y25 for upper timer marker. |
| 0x00660028 | DUEL_TIMER_LOWER_FRAME_POS | new numeric equate | constants/duel_field.inc | Packed x40,y102 for lower timer marker. |
| 0xfffff000 | BG_TILE_PALETTE15_EXTENDED_BITS | new numeric equate | constants/duel_field.inc | The raw32-bit value ORs palette15 into halfword BG map entries; the existing scene-slot clear mask describes a different operation. |
| 0x020232c0 | gDuelNumericTileScratch | ADD_ADDRESS_EQU | constants/ewram.inc | 128-byte row-major scratch used only by the compared-stat digit compositor. |
| 0x05000120 | BG_PALRAM_SLOT_9_BASE | ADD_ADDRESS_EQU | constants/gba_mem.inc | BG palette bank9 base; outer field second palette destination. |
| 0x05000180 | BG_PALRAM_SLOT_12_BASE | ADD_ADDRESS_EQU | constants/gba_mem.inc | BG palette bank12 base; portrait copy may add32 for opponent bank13. |
| 0x06006340 | card_detail_frame_bg_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | Medium card-frame BG tile destination, copy0x600 bytes. |
| 0x06008020 | PUZZLE_NAME_SPRITE_VRAM | REUSE_EXISTING_ADDRESS_EQU | constants/gba_mem.inc | Reuse the existing GNU address alias; this shared BG charblock2 tile1 address is also used by card-detail symbol paths. No OBJ-type claim. |
| 0x06008120 | card_stat_digit_bg_tiles_a | ADD_ADDRESS_EQU | constants/gba_mem.inc | Four BG tiles for stat selector0. |
| 0x060081a0 | card_stat_digit_bg_tiles_b | ADD_ADDRESS_EQU | constants/gba_mem.inc | Four BG tiles for stat selector1. |
| 0x06008220 | duel_field_outer_bg_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | Outer-field tiles selected through duel_field_outer_tile_pointers. |
| 0x0600a680 | duel_lp_digit_bg_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | Ten LP decimal glyph tiles at BG tile index0x134. |
| 0x0600a8e0 | card_detail_name_bg_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | Card-name BG tile region, always cleared0x800 bytes. |
| 0x0600b4c0 | duel_hud_number_bg_tiles_a | ADD_ADDRESS_EQU | constants/gba_mem.inc | 17-tile BG number/marker strip copied from09850c7c. |
| 0x0600b6e0 | duel_hud_decimal_bg_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | Ten BG decimal glyph tiles from09850e9c. |
| 0x0600b820 | duel_hud_number_bg_tiles_b | ADD_ADDRESS_EQU | constants/gba_mem.inc | 13 BG number glyph tiles from09850fdc. |
| 0x0600b9c0 | duel_player_icon_bg_tiles_local | ADD_ADDRESS_EQU | constants/gba_mem.inc | Local-player portrait3x3 BG tiles. |
| 0x0600bae0 | duel_player_icon_bg_tiles_opponent | ADD_ADDRESS_EQU | constants/gba_mem.inc | Opponent portrait3x3 BG tiles. |
| 0x0600e000 | BG_SCREENBLOCK_28_BASE | ADD_ADDRESS_EQU | constants/gba_mem.inc | Hardware screenblock28 base; broad consumers require a neutral hardware name. |
| 0x0600e0d4 | field_background_bg_map | ADD_ADDRESS_EQU | constants/gba_mem.inc | 15x12 field background map entries with palette10. |
| 0x0600e900 | duel_hud_aux_bg_map_6x4 | ADD_ADDRESS_EQU | constants/gba_mem.inc | Six rows of four sequential BG entries at row stride0x40. |
| 0x0600f300 | card_stat_digit_bg_map_b | ADD_ADDRESS_EQU | constants/gba_mem.inc | Two rows of four BG entries for stat tiles9..16. |
| 0x0600f840 | duel_player_icon_bg_map_opponent | ADD_ADDRESS_EQU | constants/gba_mem.inc | Opponent portrait3x3 BG map with tile0x1d7 and palette13. |
| 0x0600f904 | card_level_bg_map | ADD_ADDRESS_EQU | constants/gba_mem.inc | Two BG level/level-change marker entries. |
| 0x0600fa40 | card_effect_counter_bg_map | ADD_ADDRESS_EQU | constants/gba_mem.inc | Four BG entries for an effect/equip counter and its prefix. |
| 0x0600fa80 | card_detail_symbol_bg_map | ADD_ADDRESS_EQU | constants/gba_mem.inc | Two rows of four BG symbol entries using tile1..8 and palettes14/15. |
| 0x0600fb00 | card_stat_digit_bg_map_a | ADD_ADDRESS_EQU | constants/gba_mem.inc | Two rows of four BG entries for stat tiles9..16. |
| 0x0600fb80 | duel_player_icon_bg_map_local | ADD_ADDRESS_EQU | constants/gba_mem.inc | Local-player portrait3x3 BG map with tile0x1ce and palette12. |
| 0x0600fc80 | card_detail_name_bg_map | ADD_ADDRESS_EQU | constants/gba_mem.inc | Two rows of thirty card-name BG entries, starting at tile0x147. |
| 0x06010200 | OBJ_TILE_VRAM_BASE_PAGE2 | REUSE_EXISTING_ADDRESS_EQU | constants/gba_mem.inc | Reuse existing neutral GNU address alias for OBJ tile memory+0x200. |
| 0x06010240 | duel_end_phase_timer_obj_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | 2x4 end-phase timer marker OBJ tiles. |
| 0x06010280 | duel_phase_label_obj_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | 12x4 OBJ tiles for DP/SP/M1/BP/M2/EP phase labels. |
| 0x06011340 | duel_timer_frame_obj_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | 4x2 OBJ clock/frame tiles. |
| 0x060113c0 | duel_player_count_label_obj_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | 2x4 player deck/Graveyard/Removed Cards label OBJ tiles. |
| 0x060115c0 | duel_decimal_digit_obj_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | 11x1 OBJ glyph strip: decimal0..9 and minus. |
| 0x06011f00 | duel_result_history_obj_tiles | ADD_ADDRESS_EQU | constants/gba_mem.inc | Three OBJ result marks; history states select tile0xf8..0xfa. |
| 0x09850e9c | duel_hud_decimal_bg_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 10 BG decimal glyph tiles; exact loader0x140 bytes. |
| 0x09850fdc | duel_hud_number_bg_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 13 BG number glyph tiles; exact loader0x1a0 bytes. |
| 0x0985117c | card_stat_equal_digit_tiles | ADD_ADDRESS_EQU | constants/rom_data.inc | Equal-baseline digit bank, two prefix glyphs and unknown glyph,13 tiles. |
| 0x0985131c | card_stat_greater_digit_tiles | ADD_ADDRESS_EQU | constants/rom_data.inc | Ten glyphs selected when value is greater than baseline. |
| 0x0985145c | card_stat_less_digit_tiles | ADD_ADDRESS_EQU | constants/rom_data.inc | Ten glyphs selected when value is less than baseline. |
| 0x0985159c | duel_hud_obj_palettes | ADD_ADDRESS_EQU | constants/rom_data.inc | Three16-color palettes loaded by a0x60-byte copy; span two existing graphics/bin containers. |
| 0x0985263c | duel_player_count_label_obj_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 2x4 counter-label OBJ tiles, source0x100 bytes. |
| 0x0985273c | duel_decimal_digit_obj_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 11x1 OBJ glyph strip0..9 and minus, source0x160 bytes. |
| 0x0985289c | duel_timer_frame_obj_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 4x2 clock/frame OBJ tiles, source0x100 bytes. |
| 0x0985299c | duel_main_phase_timer_obj_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 2x4 M/arrow timer marker OBJ tiles. |
| 0x09852a9c | duel_end_phase_timer_obj_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | 2x4 E/arrow timer marker OBJ tiles. |
| 0x09854d90 | duel_result_history_obj_tile_data | ADD_ADDRESS_EQU | constants/rom_data.inc | Three result-history OBJ glyph tiles, source0x60 bytes. |

11个numeric equate和43个address equate, 共54个新GNU定义. 06008020复用PUZZLE_NAME_SPRITE_VRAM、06010200复用OBJ_TILE_VRAM_BASE_PAGE2. 前者仅沿用地址alias, 不把本段BG消费者误认作OBJ/name参数. 0600e000用中性的BG_SCREENBLOCK_28_BASE以兼容跨scene消费者.

既有gP1AltHandCountBase保持原USER身份; +0x1c的本段角色由真实Removed Cards界面路径证明, 新source槽按removed_card_count角色命名. 不扩大为全仓库全局重命名.

## 消费者证据 (R6)

consumer-evidence-v1.json、graphics-evidence-v2.json和highreg-decode-v1.json给出具体PC、file:line和原ROM证据. 全部high. 关键结论:

- 9C94为说明文字窗口九阶段, 无r0输入, active0/完成1; 9EB8实参为x/y/value/min_digits/stack palette.
- 9F50为MM:SS countdown; CA28C为turn counter, CA348为phase highlight(固定x31,y=8+22*phase), CA3A4为result history(8bit count, 跳过state0; index0非零仍绘制).
- CA160的+10/+14/+1c经ROM逻辑ID remap503/505/507与英文Deck/Graveyard/Removed Cards标签交叉证明.
- CA4F4 r1是icon index, 9*32=0x120B步长; 不将r2臆造为tile variant.
- CA660是比较样式数值合成器: 每glyph前4像素, 5px字距, prefix6px,128B scratch转置为4个8x8 tiles; 无卡图解压.
- CAE84读slot+0xc counter并写FA40四格, 原src/dst/tile_count plate必须订正.
- 3BC58旧plate的1d40和bit7应分别为1d18与bit0, player类型表为+8+4*player.

### 指令EOL

52条已存在指令注释和158槽EOL, 共210条. 实际source Function由半开body唯一包含关系给出. EOL before来自完整Function逐地址非null评论集, 有完整state时交叉验证; 不从缺失state假定null.

| PC | actual sourceFn | ASCII EOL |
|---|---|---|
| 080c9c96 | 080c9c94 | Read the global effect phase; r0 is not an input pointer. |
| 080c9d22 | 080c9c94 | Build the card-description scroll tiles from field+0x21c. |
| 080c9d7a | 080c9c94 | Write BLDALPHA EVA=4*counter and EVB=16-4*counter. |
| 080c9dc6 | 080c9c94 | Wait for the description scroll to report completion. |
| 080c9e4a | 080c9c94 | Draw the description rows; r0 controls the additional mosaic copy. |
| 080c9e9c | 080c9c94 | Clear field+0x215 bit2 while preserving all other bits. |
| 080c9eaa | 080c9c94 | Return1 after cleanup; all active phases return0. |
| 080c9ecc | 080c9eb8 | Fifth stack argument supplies the OBJ palette index. |
| 080c9efc | 080c9eb8 | Append the least-significant digit at the current x, then move x left4. |
| 080c9f34 | 080c9eb8 | Pad remaining positions with leading zero glyphs. |
| 080c9f7c | 080c9f50 | Discard the frame counter sign bit before timer arithmetic. |
| 080c9fa4 | 080c9f50 | Gate the first countdown using the local player. |
| 080c9fce | 080c9f50 | Remaining first-timer seconds=180-floor(frames/60). |
| 080ca052 | 080c9f50 | Set field+0x222 bits3:2 to1 only when they were both clear. |
| 080ca05e | 080c9f50 | A nonzero field+0x224 counter suppresses the second countdown. |
| 080ca0bc | 080c9f50 | The second time limit is300 times scene+0x37 bits4:2 seconds. |
| 080ca160 | 080ca160 | Read both players Deck/Graveyard/Removed Cards counts; no LP digit values. |
| 080ca1a4 | 080ca160 | Read the selected player Deck count at block+0x10. |
| 080ca1c0 | 080ca160 | Read the selected player Graveyard count at block+0x14. |
| 080ca1da | 080ca160 | Read the selected player Removed Cards count at block+0x1c. |
| 080ca2aa | 080ca28c | Default displayed turn count is the stored count+1. |
| 080ca2f0 | 080ca28c | Alternate displayed count=turn_count-(field_counter-1). |
| 080ca31a | 080ca28c | Render at least two digits at x28; palette argument0. |
| 080ca35e | 080ca348 | Phase-highlight y=8+22*phase; fixed x31. |
| 080ca396 | 080ca348 | Append the16x32 phase label with palette1 or2. |
| 080ca3ae | 080ca3a4 | Read one result-history byte from gPrng+0x241+index. |
| 080ca3ea | 080ca3a4 | Top history mark uses tile0xf7+state at x8*index,y128. |
| 080ca3fa | 080ca3a4 | Bottom history mark swaps states1/2 and preserves3, at y24. |
| 080ca418 | 080ca3a4 | Reconstruct the eight-bit result-history count from gPrng+0x23f bits7:1 and+0x240 bit0. |
| 080ca43e | 080ca42c | Field+0x21e bit0 masks the entire HUD OAM pass. |
| 080ca472 | 080ca42c | Render completed result-history marks when enabled. |
| 080ca502 | 080ca4f4 | Save r1 icon_index in r10; r2 is not an input to this loader. |
| 080ca58e | 080ca4f4 | Palette source=icon_palettes_base+32*icon_index. |
| 080ca5aa | 080ca4f4 | Tile source offset=9*icon_index*32 bytes. |
| 080ca62e | 080ca5f8 | Clamp values above99999 before writing exactly five LP digits. |
| 080ca674 | 080ca660 | Clear the128-byte number-composition scratch. |
| 080ca688 | 080ca660 | The(-1,-1) pair selects the unknown-value glyph. |
| 080ca746 | 080ca660 | Select the digit bank by value versus baseline. |
| 080ca76a | 080ca660 | Each source digit glyph occupies32 bytes. |
| 080ca7a4 | 080ca660 | Unpack the first four pixels of each glyph row. |
| 080ca7d0 | 080ca660 | Alternate even/odd digit packing with five-pixel spacing. |
| 080ca86e | 080ca660 | Copy the six-pixel prefix from common glyph10+selector. |
| 080ca892 | 080ca660 | Clear exactly128 destination bytes before copying four tiles. |
| 080ca89c | 080ca660 | Transpose eight rows of16 bytes into four8x8 4bpp tiles. |
| 080ca9dc | 080ca8ec | Initialize each player five-digit LP BG row. |
| 080caa4e | 080ca8ec | Copy a30x20 BG map with tile-index offset16. |
| 080cab48 | 080ca8ec | Copy the selected15x12 field background tiles. |
| 080cab92 | 080ca8ec | Copy its selected16-color palette to BG palette10. |
| 080cabca | 080ca8ec | Build the15-column by12-row background map. |
| 080cac12 | 080ca8ec | Copy the six16x32 duel phase labels to OBJ tile memory. |
| 080cacf0 | 080cace8 | Always clear0x800 bytes of card-name BG tiles. |
| 080cad50 | 080cace8 | Reset field+8 only after the conditional detail cleanup. |

## 图形目视核对 (R8)

直接ROM解码PNG glyph-source-view-v2.png. BG数字bank只用合成灰度展示形状, 不命名颜色. OBJ使用loader实际加载的RGB555 palette, index0透明; phase分别展示palette1/2. 确认十进制数字、DP/SP/M1/BP/M2/EP、M/E计时标记和结果标记. 资源尺寸由真实copy/tile_2d_row_copy参数确定.

## typedPointer / DEFAULT闭包

绑定本段完整fresh BEFORE的Core/Properties/Tiny. fresh BEFORE证明两处必要DEFAULT派生: D70CC的/undefined*指向0600e000, 只派生PTR_BG_SCREENBLOCK_28_BASE_080d70cc显示名及其incoming READ拼写, 保持原ID、DEFAULT身份、类型、全部引用和raw0600e000 word RHS, 不增加outside pin. 985117e是DWORD_0985117c+2 offcut, 只随基址新名派生card_stat_equal_digit_tiles+2, 原ID、数据边界及全部refs保持. 两节点不newUSER、不设注释、不从POST接收DEFAULT ID. 仍完整保护全部闭包行/1957旧边/incoming及所有full Function holders; 不构造清空模型.

## §5.1登记 (Rule 3)

无. 不以像素偶合或模块raw0替代引用分类.

## 自检与边界 (R9)

全部167word原ROM值相等; 标签格式与唯一性通过; setter注释ASCII且PLATE<=500. 未启动Ghidra/Program事务/保存, 未运行源码pipeline/build/Git. 实际落地及33554432B ROM逐字节验证由独立PASS后的ModeB和Root完成.

## 求助

无低置信度未决语义. 当前提案等待独立审查, 不自评分.
