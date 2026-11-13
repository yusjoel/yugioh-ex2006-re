# Refine Proposal: F16-Seg-8 [080c8bf0..080c9c94)

本版为静态语义提案, 不自评分. 所有setter after文案ASCII, PLATE<=500. 参数签名仅文档, 既有Function ABI/body/override保持. 独立review通过后由fixer ModeB实现生产脚本及完整POST预测器.

## 段测绘

4260B,16个既有Function,110个池字,95个自动槽. 本模块内无ROM_INCBIN/.byte raw块. 前Seg7已提交00b1ef178cea3670d7248256197700db3d544969, 不重apply.

| entry | before | after | body bytes(保持) |
|---|---|---|---:|
| 080c8bf0 | build_slot_activation_mask_for_player | build_slot_activation_mask_for_player | 84 |
| 080c8c58 | render_aob_zone_slot_oam | render_aob_zone_slot_oam | 180 |
| 080c8d30 | refresh_zone_effect_buff_cache | refresh_equip_target_eligibility_cache | 46 |
| 080c8d68 | render_duel_field_zone_oam_grid | render_duel_field_zone_oam_grid | 240 |
| 080c8e6c | render_field_aob_slot_oam_row | render_field_aob_slot_oam_row | 194 |
| 080c8f48 | init_card_effect_aob_ctx | init_field_background_change_state | 108 |
| 080c8fd8 | init_window_regs_for_campaign_banner | init_field_background_window_regs | 64 |
| 080c9030 | tick_campaign_banner_slide_state_machine | tick_field_background_window_transition | 320 |
| 080c91bc | reset_blend_control_regs | reset_field_background_window_regs | 26 |
| 080c91e0 | play_ui_effect_06 | tick_field_background_change_effect | 48 |
| 080c9218 | render_deck_zone_count_oam | render_zone_list_order_oam | 210 |
| 080c933c | map_card_id_to_digit_tile_offset | get_trap_monster_level_by_card_id | 44 |
| 080c9374 | write_nibble_palette_rows_to_vram | pack_font_buffer_tiles_to_4bpp | 1442 |
| 080c992c | render_card_type_icon_to_vram | init_card_description_scroll_tiles | 196 |
| 080c9a10 | write_oam_card_icon_strip | render_card_description_scroll_oam | 170 |
| 080c9ac8 | tick_card_icon_anim_step | tick_card_description_scroll | 418 |

110个word的完整类型/bytes/primary/references/equates/before与消费者PC逐行见slots.tsv. 所有95个自动槽都有新的USER槽名; 15个既有even CASE值/类型/引用完整保持.

## 数据块分类 (Rule 2/3)

| 外部剩余块 | 全ROM raw / THUMB+1 | 本段处理 | 消费者 |
|---|---|---|---|
| [09e5abb8,09e5abc8),16B | 基址1/0, 内部3候选0/0 | R7 carve | 91e0以状态字节索引3个Thumb callback及null |
| [09e5abc8,09e5abdc),20B | 基址1/0, 内部4候选0/0 | 保留至所属地址段 | CC562通过CC5B0引用独立表 |
| [09e5abdc,09e5abfc),32B | 基址2/0, 内部7候选0/0 | 保留至所属地址段 | D4086/D4184通过各自pool引用独立表 |

全部17个word地址已逐项扫描整个33554432B原ROM的raw/+1, 见firststage-native-requests. 内部候选0引用不代表表项孤儿, indexed-load消费者给出连续元素边界. 后52B有独立消费者, 不归§5.1, 不并入本段carve.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

33槽添加operand0 data-equate, 所有值逐槽等于ROM. 17种既有常量复用, 8种新常量. 同值其他槽不加binding.

| slot | value | constant | slot_label |
|---|---|---|---|
| 080c8c4c | 0x00001cf4 | DUEL_FIELD_CURSOR_STATE_OFF | build_slot_activation_mask_for_player_duel_field_cursor_state_off_080c8c4c |
| 080c8c50 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | build_slot_activation_mask_for_player_p1lp_block2_off_1ce8_080c8c50 |
| 080c8cc4 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | render_aob_zone_slot_oam_duel_field_ui_effect_flags_off_080c8cc4 |
| 080c8e5c | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | render_duel_field_zone_oam_grid_duel_field_ui_effect_flags_off_080c8e5c |
| 080c8e60 | 0x00000868 | PLAYER_BLOCK_STRIDE | render_duel_field_zone_oam_grid_player_block_stride_080c8e60 |
| 080c8f34 | 0x00000a0e | FONT_STATE_SELECTION_INDEX_OFF | render_field_aob_slot_oam_row_font_state_selection_index_off_080c8f34 |
| 080c8f38 | 0x000001a1 | FIELD_CARD_GAUGE_MIDDLE_ATTR2 | render_field_aob_slot_oam_row_field_card_gauge_middle_attr2_080c8f38 |
| 080c8f3c | 0x00004040 | OBJ_SHAPE_SIZE_HORIZONTAL_32X8 | render_field_aob_slot_oam_row_obj_shape_size_horizontal_32x8_080c8f3c |
| 080c8f44 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | render_field_aob_slot_oam_row_duel_field_ui_effect_flags_off_080c8f44 |
| 080c8fbc | 0x00000212 | DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | init_field_background_change_state_duel_field_cursor_group_toggle_off_080c8fbc |
| 080c8fc0 | 0xfffffe01 | EQUIP_STATE_CLEAR_BITS_8_1_MASK | init_field_background_change_state_equip_state_clear_bits_8_1_mask_080c8fc0 |
| 080c8fc8 | 0x00800002 | AOB_MODE_TILE_BASE_128_PAL2 | init_field_background_change_state_aob_mode_tile_base_128_pal2_080c8fc8 |
| 080c8fd0 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | init_field_background_change_state_p1lp_block2_off_1ce8_080c8fd0 |
| 080c901c | 0x000050c8 | FIELD_BACKGROUND_WIN_H_BOUNDS | init_field_background_window_regs_field_background_win_h_bounds_080c901c |
| 080c9020 | 0x00001878 | FIELD_BACKGROUND_WIN_V_BOUNDS | init_field_background_window_regs_field_background_win_v_bounds_080c9020 |
| 080c9028 | 0x00003f1f | FIELD_BACKGROUND_WININ_FLAGS | init_field_background_window_regs_field_background_winin_flags_080c9028 |
| 080c90cc | 0x00000212 | DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | tick_field_background_window_transition_duel_field_cursor_group_toggle_off_080c90cc |
| 080c9120 | 0x00000212 | DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | tick_field_background_window_transition_duel_field_cursor_group_toggle_off_080c9120 |
| 080c9164 | 0x00001878 | FIELD_BACKGROUND_WIN_V_BOUNDS | tick_field_background_window_transition_field_background_win_v_bounds_080c9164 |
| 080c9168 | 0x00008c8c | FIELD_BACKGROUND_WIN_H_COLLAPSED | tick_field_background_window_transition_field_background_win_h_collapsed_080c9168 |
| 080c91d8 | 0x00009fff | DISPCNT_WIN0_WIN1_CLEAR_MASK | reset_field_background_window_regs_dispcnt_win0_win1_clear_mask_080c91d8 |
| 080c9338 | 0x00004040 | OBJ_SHAPE_SIZE_HORIZONTAL_32X8 | render_zone_list_order_oam_obj_shape_size_horizontal_32x8_080c9338 |
| 080c9350 | 0x00001636 | METAL_REFLECT_SLIME_CID | get_trap_monster_level_by_card_id_metal_reflect_slime_cid_080c9350 |
| 080c9354 | 0x00001472 | EMBODIMENT_OF_APOPHIS_CID | get_trap_monster_level_by_card_id_embodiment_of_apophis_cid_080c9354 |
| 080c9368 | 0x0000172f | SKULL_ZOMA_CID | get_trap_monster_level_by_card_id_skull_zoma_cid_080c9368 |
| 080c96e4 | 0x0000ff0f | FONT_4BPP_CLEAR_PIXEL1_MASK | pack_font_buffer_tiles_to_4bpp_font_4bpp_clear_pixel1_mask_080c96e4 |
| 080c96e8 | 0x0000f0ff | FONT_4BPP_CLEAR_PIXEL2_MASK | pack_font_buffer_tiles_to_4bpp_font_4bpp_clear_pixel2_mask_080c96e8 |
| 080c96ec | 0x00000fff | SCENE_SLOT_MASK_LO | pack_font_buffer_tiles_to_4bpp_scene_slot_mask_lo_080c96ec |
| 080c9a04 | 0x00006c2c | GSETTINGS_OFFSET | init_card_description_scroll_tiles_gsettings_offset_080c9a04 |
| 080c9ac0 | 0x00004040 | OBJ_SHAPE_SIZE_HORIZONTAL_32X8 | render_card_description_scroll_oam_obj_shape_size_horizontal_32x8_080c9ac0 |
| 080c9b38 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | tick_card_description_scroll_duel_field_prng_anim_flag_off_080c9b38 |
| 080c9b3c | 0x00000226 | DUEL_FIELD_STATE_226_OFF | tick_card_description_scroll_duel_field_state_226_off_080c9b3c |
| 080c9bd0 | 0xffffc07f | GFX_ATTR_CLEAR_BITS_13_7 | tick_card_description_scroll_gfx_attr_clear_bits_13_7_080c9bd0 |

### REF_SLOTS

48槽新增USER DATA ref,14槽保留原引用身份. 10个非USER目标补USER primary,22个既有USER目标不改. 目标原有Data_at/containing边界完整保持, 只R7另3个NULL word创建/dword.

| slot | target | GAS target | action | slot_label |
|---|---|---|---|---|
| 080c8c44 | 020230c0 | gDuelZoneActivationState | REF_ADD | build_slot_activation_mask_for_player_ptr_g_duel_zone_activation_state_080c8c44 |
| 080c8c48 | 0201c4e0 | gP1LifePoints | REF_PRESERVE | build_slot_activation_mask_for_player_ptr_g_p1_life_points_080c8c48 |
| 080c8c54 | 0201fe60 | gZoneDisplayState | REF_ADD | build_slot_activation_mask_for_player_ptr_g_zone_display_state_080c8c54 |
| 080c8cc0 | 02023130 | gDuelFieldState | REF_ADD | render_aob_zone_slot_oam_ptr_g_duel_field_state_080c8cc0 |
| 080c8cc8 | 0201ff30 | gCardCtxSlotData | REF_ADD | render_aob_zone_slot_oam_ptr_g_card_ctx_slot_data_080c8cc8 |
| 080c8ccc | 0201e1c8 | gEquipZoneCountTable | REF_ADD | render_aob_zone_slot_oam_ptr_g_equip_zone_count_table_080c8ccc |
| 080c8cd0 | 020230c0 | gDuelZoneActivationState | REF_ADD | render_aob_zone_slot_oam_ptr_g_duel_zone_activation_state_080c8cd0 |
| 080c8cd4 | 0201fe60 | gZoneDisplayState | REF_ADD | render_aob_zone_slot_oam_ptr_g_zone_display_state_080c8cd4 |
| 080c8d28 | 020230f8 | gDuelFieldAuxAobCtx | REF_ADD | render_aob_zone_slot_oam_ptr_g_duel_field_aux_aob_ctx_080c8d28 |
| 080c8d2c | 0201fe60 | gZoneDisplayState | REF_ADD | render_aob_zone_slot_oam_ptr_g_zone_display_state_080c8d2c |
| 080c8d60 | 02023130 | gDuelFieldState | REF_ADD | refresh_equip_target_eligibility_cache_ptr_g_duel_field_state_080c8d60 |
| 080c8d64 | 020230c4 | gEquipTargetEligibilityCache | REF_ADD | refresh_equip_target_eligibility_cache_ptr_g_equip_target_eligibility_cache_080c8d64 |
| 080c8e58 | 02023130 | gDuelFieldState | REF_ADD | render_duel_field_zone_oam_grid_ptr_g_duel_field_state_080c8e58 |
| 080c8e64 | 0201c510 | gDuelFieldSlots | REF_ADD | render_duel_field_zone_oam_grid_ptr_g_duel_field_slots_080c8e64 |
| 080c8e68 | 020230c4 | gEquipTargetEligibilityCache | REF_ADD | render_duel_field_zone_oam_grid_ptr_g_equip_target_eligibility_cache_080c8e68 |
| 080c8f30 | 0201f440 | gFontState | REF_ADD | render_field_aob_slot_oam_row_ptr_g_font_state_080c8f30 |
| 080c8f40 | 02023130 | gDuelFieldState | REF_ADD | render_field_aob_slot_oam_row_ptr_g_duel_field_state_080c8f40 |
| 080c8fb4 | 020230c0 | gDuelZoneActivationState | REF_ADD | init_field_background_change_state_ptr_g_duel_zone_activation_state_080c8fb4 |
| 080c8fb8 | 02023130 | gDuelFieldState | REF_ADD | init_field_background_change_state_ptr_g_duel_field_state_080c8fb8 |
| 080c8fc4 | 09889b80 | zone_display_pair_marker_ptnsect | REF_ADD | init_field_background_change_state_ptr_zone_display_pair_marker_ptnsect_080c8fc4 |
| 080c8fcc | 0201c4e0 | gP1LifePoints | REF_PRESERVE | init_field_background_change_state_ptr_g_p1_life_points_080c8fcc |
| 080c8fd4 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | init_field_background_change_state_ptr_g_duel_card_ctx_base_080c8fd4 |
| 080c9018 | 04000040 | WIN0H | REF_PRESERVE | init_field_background_window_regs_ptr_w_i_n0_h_080c9018 |
| 080c9024 | 04000048 | WININ | REF_PRESERVE | init_field_background_window_regs_ptr_w_i_n_i_n_080c9024 |
| 080c902c | 04000050 | BLDCNT | REF_PRESERVE | init_field_background_window_regs_ptr_b_l_d_c_n_t_080c902c |
| 080c9044 | 020230c0 | gDuelZoneActivationState | REF_ADD | tick_field_background_window_transition_ptr_g_duel_zone_activation_state_080c9044 |
| 080c905c | 04000054 | BLDY | REF_PRESERVE | tick_field_background_window_transition_ptr_b_l_d_y_080c905c |
| 080c9098 | 04000044 | WIN0V | REF_PRESERVE | tick_field_background_window_transition_ptr_w_i_n0_v_080c9098 |
| 080c90c8 | 02023130 | gDuelFieldState | REF_ADD | tick_field_background_window_transition_ptr_g_duel_field_state_080c90c8 |
| 080c90d0 | 0985d720 | campaign_inner_image | REF_PRESERVE | tick_field_background_window_transition_ptr_campaign_inner_image_080c90d0 |
| 080c9114 | 09867580 | field_spell_background_tiles | REF_ADD | tick_field_background_window_transition_ptr_field_spell_background_tiles_080c9114 |
| 080c9118 | 06009000 | field_background_tile_vram | REF_ADD | tick_field_background_window_transition_ptr_field_background_tile_vram_080c9118 |
| 080c911c | 02023130 | gDuelFieldState | REF_ADD | tick_field_background_window_transition_ptr_g_duel_field_state_080c911c |
| 080c9124 | 098674a0 | campaign_inner_palette | REF_PRESERVE | tick_field_background_window_transition_ptr_campaign_inner_palette_080c9124 |
| 080c9158 | 09889180 | field_spell_background_palettes | REF_ADD | tick_field_background_window_transition_ptr_field_spell_background_palettes_080c9158 |
| 080c915c | 05000140 | field_background_palette_ram | REF_ADD | tick_field_background_window_transition_ptr_field_background_palette_ram_080c915c |
| 080c9160 | 04000044 | WIN0V | REF_PRESERVE | tick_field_background_window_transition_ptr_w_i_n0_v_080c9160 |
| 080c916c | 020230c0 | gDuelZoneActivationState | REF_ADD | tick_field_background_window_transition_ptr_g_duel_zone_activation_state_080c916c |
| 080c91b0 | 04000040 | WIN0H | REF_PRESERVE | tick_field_background_window_transition_ptr_w_i_n0_h_080c91b0 |
| 080c91dc | 04000050 | BLDCNT | REF_PRESERVE | reset_field_background_window_regs_ptr_b_l_d_c_n_t_080c91dc |
| 080c9208 | 09e5abb8 | field_background_transition_handlers | REF_ADD | tick_field_background_change_effect_ptr_field_background_transition_handlers_080c9208 |
| 080c920c | 020230c0 | gDuelZoneActivationState | REF_ADD | tick_field_background_change_effect_ptr_g_duel_zone_activation_state_080c920c |
| 080c924c | 02023130 | gDuelFieldState | REF_ADD | render_zone_list_order_oam_ptr_g_duel_field_state_080c924c |
| 080c9250 | 080c9254 | switchD_080c924a__switchdataD_080c9254 | REF_ADD | render_zone_list_order_oam_ptr_switch_d_080c924a_switchdata_d_080c9254_080c9250 |
| 080c92c0 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_zone_list_order_oam_ptr_g_duel_card_ctx_base_080c92c0 |
| 080c9334 | 0201e2a0 | gDuelCardCtxBase | REF_ADD | render_zone_list_order_oam_ptr_g_duel_card_ctx_base_080c9334 |
| 080c96e0 | 02006ed0 | gFontJpCtx | REF_ADD | pack_font_buffer_tiles_to_4bpp_ptr_g_font_jp_ctx_080c96e0 |
| 080c9928 | 02006ed0 | gFontJpCtx | REF_ADD | pack_font_buffer_tiles_to_4bpp_ptr_g_font_jp_ctx_080c9928 |
| 080c99f0 | 02023348 | gCardDescriptionScrollState | REF_ADD | init_card_description_scroll_tiles_ptr_g_card_description_scroll_state_080c99f0 |
| 080c99f4 | 02039eb0 | gSceneWorkArea | REF_ADD | init_card_description_scroll_tiles_ptr_g_scene_work_area_080c99f4 |
| 080c99f8 | 06016400 | card_description_scroll_obj_tiles | REF_ADD | init_card_description_scroll_tiles_ptr_card_description_scroll_obj_tiles_080c99f8 |
| 080c99fc | 02006ed0 | gFontJpCtx | REF_ADD | init_card_description_scroll_tiles_ptr_g_font_jp_ctx_080c99fc |
| 080c9a00 | 02000000 | EWRAM_BASE | REF_ADD | init_card_description_scroll_tiles_ptr_e_w_r_a_m_b_a_s_e_080c9a00 |
| 080c9a08 | 09e5f854 | font_jp_base_table | REF_PRESERVE | init_card_description_scroll_tiles_ptr_font_jp_base_table_080c9a08 |
| 080c9a0c | 06016600 | card_description_scroll_obj_tiles_row1 | REF_ADD | init_card_description_scroll_tiles_ptr_card_description_scroll_obj_tiles_row1_080c9a0c |
| 080c9a44 | 02023348 | gCardDescriptionScrollState | REF_ADD | render_card_description_scroll_oam_ptr_g_card_description_scroll_state_080c9a44 |
| 080c9ac4 | 02023348 | gCardDescriptionScrollState | REF_ADD | render_card_description_scroll_oam_ptr_g_card_description_scroll_state_080c9ac4 |
| 080c9b30 | 03000040 | gPrng | REF_PRESERVE | tick_card_description_scroll_ptr_g_prng_080c9b30 |
| 080c9b34 | 02023130 | gDuelFieldState | REF_ADD | tick_card_description_scroll_ptr_g_duel_field_state_080c9b34 |
| 080c9bd4 | 02023348 | gCardDescriptionScrollState | REF_ADD | tick_card_description_scroll_ptr_g_card_description_scroll_state_080c9bd4 |
| 080c9c24 | 06016400 | card_description_scroll_obj_tiles | REF_ADD | tick_card_description_scroll_ptr_card_description_scroll_obj_tiles_080c9c24 |
| 080c9c70 | 06016400 | card_description_scroll_obj_tiles | REF_ADD | tick_card_description_scroll_ptr_card_description_scroll_obj_tiles_080c9c70 |

### RENAME_SLOTS / CASE

95槽均新USER槽名并设EOL, 详slots.tsv. EWRAM_BASE与GSETTINGS_OFFSET按base/offset分开保留, 不合成gSettings指针槽. switch table基址9250指向现有ANALYSIS label, 15个CASE保留even地址; 不增加+1或替换CASE namespace.

### FUNC_RENAME

| entry | old | new | native incoming | 证据及理由 |
|---|---|---|---:|---|
| 080c8d30 | refresh_zone_effect_buff_cache | refresh_equip_target_eligibility_cache | 4 | 3a7f0输出2x11个u16 eligibility codes, 不是ATK/DEF buff; 8e68消费者将该code选OBJ tile. |
| 080c8f48 | init_card_effect_aob_ctx | init_field_background_change_state | 1 | 32358的硬编码CID为Forest/Umi等field spells, 输出背景bank index; 原0x4c halfwords描述与byte helper矛盾. |
| 080c8fd8 | init_window_regs_for_campaign_banner | init_field_background_window_regs | 0 | 原注释banner主题与field-spell背景素材/分类消费者矛盾; DISPCNT实际置0x6000. |
| 080c9030 | tick_campaign_banner_slide_state_machine | tick_field_background_window_transition | 0 | 四阶段先纵向收拢WIN0V, 拷贝field-spell背景, 再横向展开WIN0H; 不是campaign slide. |
| 080c91bc | reset_blend_control_regs | reset_field_background_window_regs | 0 | 91bc读DISPCNT清bits13/14; 91cc和91d0清BLDCNT/BLDY, 原blend_mode/BLDALPHA叙述错误. |
| 080c91e0 | play_ui_effect_06 | tick_field_background_change_effect | 1 | 16B callback表给出init/tick/reset三阶段和NULL终止, 补充原placeholder名字语义. |
| 080c9218 | render_deck_zone_count_oam | render_zone_list_order_oam | 1 | 循环r8由field+0xa减1逐项倒序, 显示r8+1序号; 未读取deck/card count作为数字内容. |
| 080c933c | map_card_id_to_digit_tile_offset | get_trap_monster_level_by_card_id | 1 | 四CID均trap monsters, 返回等级4/10; CB2EE存baseline level, CB8B8用于等级差异tile比较. 无ROM查表. |
| 080c9374 | write_nibble_palette_rows_to_vram | pack_font_buffer_tiles_to_4bpp | 3 | r0为目的, r1截u16起tile, r2截u8行数; 源从gFontJpCtx[0]读取64B/tile, 不写palette RAM. |
| 080c992c | render_card_type_icon_to_vram | init_card_description_scroll_tiles | 1 | EEB54返回localized description字符串, text_render_wrapper绘制正文; 后继14行ring buffer和Up/Down滚动, 无type-icon table lookup. |
| 080c9a10 | write_oam_card_icon_strip | render_card_description_scroll_oam | 3 | 不接收OAM指针/count/XY四参数; r0只用low16作OBJ属性flags, 4x最多14行由共享state驱动. |
| 080c9ac8 | tick_card_icon_anim_step | tick_card_description_scroll | 1 | R按钮持有且Up/Down选择两阶段以4px步进并重填14行环形OBJ tile; 原anim_state_ptr签名错误. |

三个外表callback尚无既有native DATA incoming, ROM中对应Fn+1表项及91e0间接调用消费者证明引用. 改名保持Function symbol ID、ABI、body、参数storage和所有属性.

### PLATE (R5)

18个完整重写: 段内16与必要callee context2. RenameKnownFunctions AST逐tuple绑定: 14条既有替换, 4条缺项追加. 不改历史已提交产品脚本. 完整native/registry before和after见plates.tsv.

- 080c8bf0 build_slot_activation_mask_for_player, high, asm/16_duelfield_zone.s:15907
  `Clear gDuelZoneActivationState+3, then build its five-slot activation mask when gP1LifePoints+0x1cf4 equals3. Use the player stored at gP1LifePoints+0x1ce8 and eval_slot_activation_guard_full(player,slot,1). Independently, if gZoneDisplayState+0xc equals-1, clear bit0 of gZoneDisplayState. The final guard does not clear the activation mask. No inputs.`
- 080c8c58 render_aob_zone_slot_oam, high, asm/16_duelfield_zone.s:15973
  `Render the five slots enabled by gDuelZoneActivationState+3. Abort on field+0x215 bit2 or gCardCtxSlotData bit0. Resolve zone0 coordinates using the player in gEquipZoneCountTable. For the selected slot in gZoneDisplayState+8, bit1 selects its special display: bit0 chooses explicit pair coordinates, otherwise render its AOB at state+0x48. Other slots use gDuelFieldAuxAobCtx. Tick the selected AOB when bit1 is set, and always tick the shared auxiliary AOB.`
- 080c8d30 refresh_equip_target_eligibility_cache, high, asm/16_duelfield_zone.s:16084
  `Refresh gEquipTargetEligibilityCache, a two-player by11-slot u16 table. Decode gDuelFieldState+0x210: player bit7, zone bits6:0, subindex bits14:8. Call build_equip_target_eligibility_table(player,zone+subindex,cache). The cache contains equip-target eligibility codes used to select indicator tiles, rather than ATK/DEF deltas. No inputs or return value.`
- 080c8d68 render_duel_field_zone_oam_grid, high, asm/16_duelfield_zone.s:16124
  `Render cached equip-target indicators for both players and slots0..10. Require a valid selected zone reference, field+0x215 bit2 clear, selected zone+subindex at most10 and a nonzero low13-bit card reference. Each drawn slot must also have a nonzero low13-bit reference and eligibility code. Resolve coordinates, add x3/y4, and use attr2=(2*code+0x110)|0x2400 with shape/size0x40. gEquipTargetEligibilityCache has player stride0x16; slot data uses stride20 and PLAYER_BLOCK_STRIDE.`
- 080c8e6c render_field_aob_slot_oam_row, high, asm/16_duelfield_zone.s:16268
  `Render a horizontal slot-count gauge. Read count bits11:4 from gFontState+0xa0e and save the value from get_duel_field_card_count. Center count eight-pixel entries at x140-4*count,y68. Indices before count-value use palette0, the rest palette3. Append four frame pieces at x100,116,132,148. Set gDuelFieldState+0x215 bit5 when the saved value is0. Emit OAM directly. No inputs.`
- 080c8f48 init_field_background_change_state, high, asm/16_duelfield_zone.s:16379
  `Initialize field-background change state for card ID r0. Clear0x4c bytes at gDuelZoneActivationState, classify the field card, and store its eight-bit background index in field+0x212 bits8:1 while preserving adjacent bits. Initialize gDuelFieldAuxAobCtx at state+0x38 from zone_display_pair_marker_ptnsect, tile base128/palette2. Set ctx+0x13 bit0, select animation0 or1 by the player comparison with gDuelCardCtxBase+4 XOR1, then set ctx+0xe to2.`
- 080c8fd8 init_field_background_window_regs, high, asm/16_duelfield_zone.s:16451
  `Initialize the field-background transition windows. Set both horizontal bounds to0x50c8 and both vertical bounds to0x1878, WININ to0x3f1f and WINOUT to0x1f. Enable WIN0 and WIN1 by ORing DISPCNT with0x6000, then set BLDCNT to0x88. These are bits13 and14, not WIN1 and OBJWIN. Return1 for the phase callback.`
- 080c9030 tick_field_background_window_transition, high, asm/16_duelfield_zone.s:16498
  `Tick field-background transition subphase state+1 and counter state+2. Phase0 sets BLDY=31. Phase1 contracts WIN0V about y72 by six pixels per edge for counter0..8. Phase2 copies0x1680 tile bytes and32 palette bytes from the selected default or field-spell bank, then resets WIN0V and collapses WIN0H at x140. Phase3 opens WIN0H by floor(15*counter/2) per edge for counter0..8. Return0 during phases0..3 and1 afterward.`
- 080c91bc reset_field_background_window_regs, high, asm/16_duelfield_zone.s:16711
  `Finish the field-background transition. AND DISPCNT with0x9fff to disable WIN0 and WIN1 while preserving OBJWIN and the other display bits. Clear BLDCNT and BLDY; BLDALPHA is not written. Return1 for the phase callback.`
- 080c91e0 tick_field_background_change_effect, high, asm/16_duelfield_zone.s:16732
  `Run field_background_transition_handlers using the byte at gDuelZoneActivationState. Invoke the selected Thumb callback through invoke_r0. A nonzero callback result increments the phase byte and clears the subphase byte at+1. Return1 while a callback exists and0 at the fourth null entry. The three callbacks initialize windows, tick the background transition, then reset window registers.`
- 080c9218 render_zone_list_order_oam, high, asm/16_duelfield_zone.s:16773
  `Render list ordinals for the field+0xa zone records at field+0xc, stride4, in reverse order. Each record supplies zone and player; the displayed number is record index+1. Group zone types0..4 and5..9 before coordinate lookup, retain types10..15, and use fixed coordinates for larger types. Draw decimal digits with tile base0x8e and a frame with attr2=0xda. All digits of one ordinal use the same computed x coordinate. No inputs.`
- 080c933c get_trap_monster_level_by_card_id, high, asm/16_duelfield_zone.s:16915
  `Return the trap-monster level override for card ID r0: Metal Reflect Slime gives10; Embodiment of Apophis, Skull Zoma and Stronghold give4; all other IDs give0. render_large_card_display_by_mode uses this as the baseline level for its level-change display. This leaf function performs only immediate comparisons, without reading a digit table.`
- 080c9374 pack_font_buffer_tiles_to_4bpp, high, asm/16_duelfield_zone.s:16951
  `Pack font pixel tiles into contiguous4bpp data at r0. Truncate r1 to the starting tile index and r2 to an eight-bit row count. Process row_count times the tile width in gFontJpCtx+8 bits9:2, reading64 bytes per source tile from ctx[0]+(first_tile+i)*64 and writing32 bytes per tile. Each four source bytes occupy one halfword at shifts0,4,8,12. Destination halfwords start at0; source zeroes remain transparent. Source values are not explicitly masked to four bits.`
- 080c992c init_card_description_scroll_tiles, high, asm/16_duelfield_zone.s:17754
  `Initialize scrolling card-description tiles for internal card index r0. Clear the four-byte scroll state and0x5000 bytes of gSceneWorkArea, and clear seven full OBJ tile rows at card_description_scroll_obj_tiles. Configure the font context with16 tile columns and84 rows, select its language/font flags, and render the localized description from card_data_query. Pack up to13 text rows starting at OBJ row1. Store ceil(rendered_height/8)+1 in scroll-state bits6:0, preserving bit7.`
- 080c9a10 render_card_description_scroll_oam, high, asm/16_duelfield_zone.s:17866
  `Render the14-row circular card-description tile buffer. r0 low16 supplies extra OBJ flags, ORed with shape/size0x4040. Draw at most14 rows, four32x8 sprites per row at x76,108,140,172; y advances by8 and includes the signed scroll offset. Short text is vertically centered; longer text starts at y16. Advance the circular tile-row index modulo14, with attr2 starting at0x320+row*16. No OAM pointer, count or coordinate parameters are accepted.`
- 080c9ac8 tick_card_description_scroll, high, asm/16_duelfield_zone.s:17967
  `Tick card-description scrolling while input bit0x100 at gPrng+0x146 is set and field flags permit it. Up/down bits0x40/0x80 select two-step four-pixel motion; at offset+8 or-8 refill one row of the14-row OBJ tile ring and reset the phase. Scroll-state bits6:0 hold total rows, bits13:7 the text row, bits15:14 the phase; bytes2/3 hold pixel offset and ring index. Always draw normal OAM; argument0x800 also draws a mosaic copy. Return1 when input/field guards block scrolling, otherwise0.`
- 0803a7f0 build_equip_target_eligibility_table, high, asm/03_equip_chain_hand.s:10184, asm/03_equip_chain_hand.s:10202, asm/03_equip_chain_hand.s:10306, asm/03_equip_chain_hand.s:10331
  `Build a two-player by11-slot u16 equip-target eligibility table at r2 for source player r0 and source slot r1. Zero all22 cells first. A source slot above10 or an empty low13-bit source card reference leaves the table zero. For each nonempty target slot, preserve special relation codes7 or6 when found; otherwise try classify_equip_target_eligibility in each direction until nonzero. Output player stride is0x16 bytes. refresh_equip_target_eligibility_cache supplies gEquipTargetEligibilityCache.`
- 080eeb54 card_data_query, high, asm/20_anim_jp_tileblit.s:10313, asm/20_anim_jp_tileblit.s:10385, asm/20_anim_jp_tileblit.s:10392
  `Return a localized card-description string for r0=internal card index and r1=language. Normally read card_desc_pointer_table[index*6+language] and add card_descs_table. For language0 outside regionJ, CID0x1468 uses a fixed localized substitute selected by gSettings. The result is a string pointer consumed by text_render_wrapper, not a numeric ATK/DEF/type query.`

## carve计划 (R7)

将rom.s原.incbin(0x1E5ABB8,0x44)仅切前16B. Header已有/dword原样保持, 后3个word实际data_at=NULL, 创建/dword. 三个非零word新增指向保存odd值的USER DATA引用, NULL不加ref. 不创建odd USER标签.

```asm
.global field_background_transition_handlers
field_background_transition_handlers:
    .word init_field_background_window_regs+1
    .word tick_field_background_window_transition+1
    .word reset_field_background_window_regs+1
    .word 0
.incbin "roms/2343.gba", 0x1E5ABC8, 0x34
```

91e2取bb8基址,91ec indexed LDR,91f2 invoke_r0; 91fc/9200只在callback非零返回时递增阶段,9202清子阶段,91f0在第4项null结束. 后继abc8由CC562和CC570独立索引, abdc由D4086/D4184独立消费者引用. actual API确认CC562 owner=CC528 tick_zone_display_frame, D4184 owner=D4148 sort_zone_slots_by_stat_quicksort; 没有nearest-label推断.

三odd新DEFAULT offcut的public ID/name/namespace及even_function完整before已由Root getter封存. ModeB必须精确投影三个新DEFAULT及全部even_function rich holders, 不接受未知POST动态ID.

## disasm计划 (R4)

无. 不修改TMode,不反汇编,不新建/删除/合并Function,不改body或override.

## 新增constants / 全局

| value | name | 文件 | 依据 |
|---|---|---|---|
| 0x000001a1 | FIELD_CARD_GAUGE_MIDDLE_ATTR2 | constants/duel_field.inc | Middle frame sprite attr2; existing EQUIP_DISPLAY_OP_PARAM_1A1 describes a different operation argument. |
| 0x00001878 | FIELD_BACKGROUND_WIN_V_BOUNDS | constants/duel_field.inc | WIN0V/WIN1V top24 bottom120. |
| 0x00003f1f | FIELD_BACKGROUND_WININ_FLAGS | constants/duel_field.inc | WIN0 layers0x1f and WIN1 layers/effects0x3f. |
| 0x000050c8 | FIELD_BACKGROUND_WIN_H_BOUNDS | constants/duel_field.inc | WIN0H/WIN1H left80 right200. |
| 0x00008c8c | FIELD_BACKGROUND_WIN_H_COLLAPSED | constants/duel_field.inc | WIN0H left140 right140; the window is collapsed horizontally. |
| 0x00009fff | DISPCNT_WIN0_WIN1_CLEAR_MASK | constants/gba_io.inc | Clear bits13/14 in a16-bit DISPCNT value; existing0xffff9fff has different ROM word bits. |
| 0x0000f0ff | FONT_4BPP_CLEAR_PIXEL2_MASK | constants/card_info.inc | Clear halfword bits11:8 before placing source pixel2. |
| 0x0000ff0f | FONT_4BPP_CLEAR_PIXEL1_MASK | constants/card_info.inc | Clear halfword bits7:4 before placing source pixel1. |
| 0x020230c4 | gEquipTargetEligibilityCache | constants/ewram.inc | 2x11 u16 eligibility codes from build_equip_target_eligibility_table, consumed as OBJ indicator tile codes. |
| 0x02023348 | gCardDescriptionScrollState | constants/ewram.inc | Four packed bytes at gDuelFieldState+0x218: total rows, text row, phase, signed pixel offset and tile-ring index. |
| 0x02039eb0 | gSceneWorkArea | constants/ewram.inc | Shared scene workspace: cleared0x5000 bytes here; other scenes use its base as OBJ list storage or link-state flags. Not identified as the font pixel source. |
| 0x05000140 | field_background_palette_ram | constants/gba_mem.inc | BG palette row10,32-byte destination for the selected field-background palette. |
| 0x06009000 | field_background_tile_vram | constants/gba_mem.inc | BG tile destination for a0x1680-byte field-background bank entry. |
| 0x06016400 | card_description_scroll_obj_tiles | constants/gba_mem.inc | 14-row circular OBJ tile buffer,512 bytes per row; source OAM tile index0x320. |
| 0x06016600 | card_description_scroll_obj_tiles_row1 | constants/gba_mem.inc | Initial text starts one512-byte tile row after the circular OBJ buffer base. |
| 0x09867580 | field_spell_background_tiles | constants/rom_data.inc | Field-spell background tile bank, index*0x1680; classification and extracted Forest/Wasteland/Mountain visuals prove the role. |
| 0x09889180 | field_spell_background_palettes | constants/rom_data.inc | Field-spell background palette bank, index*32, paired with field_spell_background_tiles. |
| 0x09e5abb8 | field_background_transition_handlers | rom.s global label | R7 three Thumb phase callbacks plus a null, consumed by tick_field_background_change_effect. |

8个numeric .equ+9个address .equ+1个carve global label. 0x1a1已有EQUIP_DISPLAY_OP_PARAM_1A1是另一操作参数, 不是本处sprite attr2; 0x9fff与既有0xffff9fff原ROM四字节不同. 其余匹配值使用现有inc, 含0xfff/0x4040/CIDs/offsets. 新label名称/值不由图像主题猜测.

## 消费者证据 (R6)

完整证据见consumer-evidence-v1.json, 全部high. 关键链:

- 8d30->3a7f0输出2x11个u16 equip eligibility code,8e68用于OBJ tile选择.
- 8e82调用get_duel_field_card_count,8e86保存结果到r10; 8f08调用OAM helper后,8f0c恢复r0,8f0e/8f10测试保存值. 保存卡数为0时才在8f1e设置gDuelFieldState+0x215 bit5.
- 8f48->32358分类Forest/Umi等field spells,9030按index*0x1680和index*32选择图像/palette. 窗口先纵向收拢再横向展开, 每个计数阶段实际9帧(0..8).
- 933c只比较四CID返回trap-monster baseline level4/10; CB2EE保存, CB8B8与当前level作tile比较. card_stats首记录20B使table+22*i+0xa等于后续record的level字段, 详export_card_data.py.
- 992c->EEB54从card_desc_pointer_table/card_descs_table返回description字符串, 交text_render_wrapper, 不是name/type icon.
- 9374每64B byte-pixel tile写32B 4bpp; 宽度16tile即每行512B. 9a10绘制4个32x8 sprites/行,9ac8循环14行, 上下键每次两步4px重填一行.
- 02039eb0在本函数清0x5000B, 其他scene用于OBJ list或link状态, 故命名共享work area; 没有把它臆定为gFontJpCtx[0] pixel source.

### 指令EOL

80个既有指令EOL按PC/actual sourceFn固定, 另95槽+4外表word EOL, 共179. 其他所有EOL保持.

| PC | actual sourceFn | EOL ASCII |
|---|---|---|
| 080c8bfe | 080c8bf0 | Require the cursor/field state at gP1LifePoints+0x1cf4 to equal3. |
| 080c8c12 | 080c8bf0 | Evaluate activation for player at+0x1ce8, slot0..4, argument r2=1. |
| 080c8c2c | 080c8bf0 | Test gZoneDisplayState+0xc against-1; this address is not gPrng. |
| 080c8c3c | 080c8bf0 | Clear gZoneDisplayState bit0, leaving the slot activation mask intact. |
| 080c8c8e | 080c8c58 | Resolve coordinates for player=gEquipZoneCountTable[0], zone0, subindex=slot. |
| 080c8cb0 | 080c8c58 | Selected slot: bit0 chooses explicit pair coordinates; clear bit0 selects the AOB branch. |
| 080c8ce8 | 080c8c58 | Render the selected AOB at gZoneDisplayState+0x48 with x+4/y+4. |
| 080c8d54 | 080c8d30 | Write two rows of11 equip-target eligibility codes, not ATK/DEF buffs. |
| 080c8dc2 | 080c8d68 | Shift out all but the low13-bit card reference; this is not a bit19 flag test. |
| 080c8e20 | 080c8d68 | Choose indicator tile from twice the eligibility code. |
| 080c8e2e | 080c8d68 | Attribute2=(2*code+0x110)|0x2400. |
| 080c8e80 | 080c8e6c | Extract count bits11:4 from the halfword at gFontState+0xa0e. |
| 080c8e8a | 080c8e6c | Palette split index = displayed count minus the value returned by get_duel_field_card_count. |
| 080c8e98 | 080c8e6c | The computed value is x=140-4*count; y is fixed at68. |
| 080c8eae | 080c8e6c | Indices before count-occupied use palette0; remaining entries use palette3. |
| 080c8ed8 | 080c8e6c | First frame piece at x100,y68 with attr2=0x1a0. |
| 080c8f1e | 080c8e6c | Set gDuelFieldState+0x215 bit5 when the saved get_duel_field_card_count result is0. |
| 080c8f52 | 080c8f48 | Clear0x4c bytes, exactly through the auxiliary AOB context end. |
| 080c8f58 | 080c8f48 | Classify the card for the field-spell background image index. |
| 080c8f70 | 080c8f48 | Store background index in field+0x212 bits8:1, preserving bit0 and upper bits. |
| 080c8f7c | 080c8f48 | Initialize the shared auxiliary AOB: tile base128, palette2, init flag1. |
| 080c8fde | 080c8fd8 | WIN0H=0x50c8: left80,right200. |
| 080c8fe6 | 080c8fd8 | WIN0V=0x1878: top24,bottom120. |
| 080c8fea | 080c8fd8 | WIN1H receives the same horizontal bounds. |
| 080c8fee | 080c8fd8 | WIN1V receives the same vertical bounds. |
| 080c900c | 080c8fd8 | Enable WIN0 and WIN1 with DISPCNT bits13/14 (0x6000). |
| 080c9012 | 080c8fd8 | BLDCNT=0x88; OBJWIN is not enabled by this function. |
| 080c907c | 080c9030 | WIN0V top=24+6*counter,bottom=120-6*counter, counter0..8. |
| 080c908a | 080c9030 | Stay in phase1 through counter8; advance after the ninth call. |
| 080c90b8 | 080c9030 | Fallback background index is field+0x220 word bits17:10. |
| 080c90d6 | 080c9030 | Field-spell background index is field+0x212 bits8:1. |
| 080c90e0 | 080c9030 | Tile-bank entry stride = (3*index*16-3*index)*128 =0x1680*index. |
| 080c90ec | 080c9030 | Copy0x1680 bytes to field_background_tile_vram. |
| 080c9136 | 080c9030 | Copy32 palette bytes to BG palette row10. |
| 080c9140 | 080c9030 | Reset WIN0V to top24,bottom120. |
| 080c9148 | 080c9030 | WIN0H=0x8c8c collapses the horizontal window at x140. |
| 080c9192 | 080c9030 | WIN0H left=(140-floor(15*counter/2))&255,right=(140+floor(15*counter/2))&255. |
| 080c91a0 | 080c9030 | Stay in phase3 through counter8; advance after the ninth call. |
| 080c91c6 | 080c91bc | Disable WIN0/WIN1 by clearing DISPCNT bits13/14, preserving OBJWIN. |
| 080c91cc | 080c91bc | Clear BLDCNT. |
| 080c91d0 | 080c91bc | Clear BLDY at BLDCNT+4; BLDALPHA at+2 is untouched. |
| 080c91ec | 080c91e0 | Read a stored Thumb callback; the three callbacks are followed by null. |
| 080c9200 | 080c91e0 | Advance outer phase only when the callback returns nonzero. |
| 080c9202 | 080c91e0 | Clear transition subphase at state+1 on outer-phase advance. |
| 080c9224 | 080c9218 | Start from list record count-1 and iterate toward0. |
| 080c923c | 080c9218 | Display ordinal = record index+1, not a card count field. |
| 080c92f0 | 080c9218 | Take the ordinal decimal remainder; r7 stays fixed for every digit. |
| 080c933e | 080c933c | Metal Reflect Slime CID selects level10. |
| 080c9348 | 080c933c | Embodiment of Apophis CID selects level4. |
| 080c935e | 080c933c | SKULL_ZOMA_CID+0xda equals STRONGHOLD_CID; both select level4. |
| 080c9398 | 080c9374 | Tile width = (gFontJpCtx halfword+8 >>2)&255. |
| 080c93b4 | 080c9374 | Read64 source bytes per font tile, beginning at first_tile+i. |
| 080c93bc | 080c9374 | Initialize each destination halfword to zero before placing four pixel values. |
| 080c93d6 | 080c9374 | Place source pixel1 at halfword bits7:4. |
| 080c93ec | 080c9374 | Place source pixel2 at halfword bits11:8. |
| 080c9402 | 080c9374 | Place source pixel3 at halfword bits15:12. |
| 080c9902 | 080c9374 | One unrolled tile consumes64 source bytes and writes32 destination bytes. |
| 080c9936 | 080c992c | Clear exactly four bytes of card-description scroll state. |
| 080c9940 | 080c992c | Clear0x5000 bytes of the shared scene work area. |
| 080c994c | 080c992c | Null-source tile copy clears seven rows of32 tiles,0x400 bytes per row. |
| 080c9958 | 080c992c | Configure16 tile columns and84 tile rows with font/alignment arguments1/2. |
| 080c999c | 080c992c | Enable font-context bit6 at+0x15 for this description rendering path. |
| 080c99a4 | 080c992c | Fetch the localized card-description string for internal card index and language. |
| 080c99d4 | 080c992c | Pack up to13 rendered description rows, starting at circular OBJ row1. |
| 080c99e8 | 080c992c | Store ceil(rendered text height/8)+1 in low7 bits; preserve bit7. |
| 080c9a2c | 080c9a10 | Cap the number of visible text rows at14. |
| 080c9a72 | 080c9a10 | Four horizontal32x8 OBJ entries per text row, beginning at x76. |
| 080c9a80 | 080c9a10 | Interpret scroll-state byte2 as a signed pixel offset. |
| 080c9a90 | 080c9a10 | Emit one text-strip OBJ; r1 is shape/size plus extra OBJ flags. |
| 080c9a98 | 080c9a10 | Each visible text row uses four OBJ entries. |
| 080c9ade | 080c9ac8 | Input bit0x100 at gPrng+0x146 enables description scrolling. |
| 080c9b1e | 080c9ac8 | Description scroll phase occupies bits15:14, not a separate state pointer. |
| 080c9b48 | 080c9ac8 | Input bit0x40 requests the previous text row when row offset is nonzero. |
| 080c9b8a | 080c9ac8 | Input bit0x80 requests the next row when offset+13 is below total rows. |
| 080c9c0c | 080c9ac8 | At pixel offset+8, refill the preceding row of the14-row circular OBJ buffer. |
| 080c9c4e | 080c9ac8 | At pixel offset-8, refill the next row of the14-row circular OBJ buffer. |
| 080c9c80 | 080c9ac8 | Argument0x800 draws an extra OBJ-mosaic copy. |
| 080c9c86 | 080c9ac8 | Always draw the normal card-description OAM strip. |
| 080cb2e6 | 080cb1cc | Get the trap-monster baseline level from the card ID stored in the stats record. |
| 080cb8b8 | 080cb1cc | Compare the current level with the trap-monster baseline level for the change marker. |

## DEFAULT / offcut / typedPointer投影

绑定Root完整before:226Fn/1961word/3185slot/3643fullstate, Properties31805, Tiny16998rows/1940edges/3405seeds. 117个primary变化地址逐项见primitives. 实际现有pointer edges指向这些变化节点为0; 非变化地址的DEFAULT派生primary依赖为0. 此事实不是泛化清空策略: 16998行及1940edge完整保护, 所有incoming/rich reference目标显示名按实际primary变化投影. R7另新增3个已知prospective odd DEFAULT, 全部even_function holder一般逻辑仍须保留.

## R8静态图形核对

f16-seg8-field-background-view-v1.png按原ROM4bpp及RGB555 palette直接解码, 每项15x12 tiles. 取默认bank前2项和field-spell bank前4项, 可见颜色底框及Forest/Wasteland/Mountain素材, 与32358的field-card CID分类对应. 本段没有CU/模拟器操作或实际截图.

## Source范围与保护

正式落地涉及asm16本段、外段所有12个新Function名字的BL操作数/必要名引用,03模块及20模块各1处context PLATE,80个精确PC的EOL(其中CB2E6/CB8B8在同模块后段),rom.s精确16B carve及后52B保持,上述constants新增定义,registry逐项替换/追加,两命名CSV各12个name cell. 没有Function body_size变更.

现行resolve_word_symbol不放行VRAM/PALRAM且要求USER目标, 保持原导出器策略;9250的ANALYSIS switch与VRAM/PALRAM指针应由ModeB真实AST解析并生成有界fallback/pin. 全部继承pins保持,1747个模块word表达式完整核对; 不按全局相同value擅改其他池字. source227/DB15/原ROM由Root门禁保护. Executor未执行任何canonical实现、Program写入、save、build或Git.

## §5.1登记 (Rule 3)

无. 模块内raw0; 外部16B有indexed消费者, 后52B属于另两张正引用独立表.

## 求助

无低置信语义或额外native读取缺项. 语义评分等待独立review, 完整生产POST模型留PASS后的ModeB.

## Executor Report: F16-Seg-8

- 槽: EQ=33 REF_ADD=48 REF_PRESERVE=14 CASE_PRESERVE=15 SLOT_USER=95 FUNC_RENAME=12 PLATE=18.
- carve=1(16B),disasm=0,§5.1=0.
- newUSER=105,numeric.equ=8,address.equ=9,global carve label=1.
- 求助:none.
- proposal:doc/dev/refine/F16-Seg-8.proposal.md.
