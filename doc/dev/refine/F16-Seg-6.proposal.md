# Refine Proposal: F16-Seg-6 [0x080c699c..0x080c7af8)

本段 4444 字节. 本文是正式静态方案, 不代表 Ghidra 落地或构建已执行. 所有 setter 文本为 ASCII, PLATE 最多 500 字符. 实际 BEFORE 由 Root 新原生采集, 段内现有 Function/body/ABI/数据类型/flow override 完整保持.

## 段测绘

13 个既有 Function, 176 个 word, 98 个自动数据名, 0 个 raw 块. 3688 字节指令 + 704 字节池字 + 52 字节原样零对齐 = 4444 字节. 176 槽分为 EQ_ADD=35, REF_ADD=48, REF_PRESERVE=15, CASE_VECTOR_PRESERVE_CORE=78.

| 入口 | 现名 | 订正后 | indeg | 文档参数 |
|---|---|---|---:|---|
| 080c699c | set_zone_oam_coords_by_player | render_zone_cursor_oam | 4 | r0=player; r1=zone_type; r2=sub_index; r3=palette_bank |
| 080c6a20 | write_zone_slot_oam_descriptor | select_zone_cursor_and_render_info | 5 | r0=player; r1=zone_type; r2=absolute_sub_index |
| 080c6b04 | decode_zone_oam_word_to_slot_fields | move_zone_cursor_vertical | 2 | r0=u16 packed_cursor; r1=down_flag (0=up, 1=down); return r0=u16 packed_cursor |
| 080c6e9c | decode_zone_oam_word_to_cursor_fields | move_zone_cursor_horizontal | 2 | r0=u16 packed_cursor; r1=right_flag (0=left, 1=right); return r0=u16 packed_cursor |
| 080c707c | check_zone_card_id_cache_valid | check_zone_card_id_cache_valid | 2 | r0=u16 packed_cursor; return r0=0 or 1 |
| 080c716c | apply_zone_cursor_step | apply_zone_cursor_step | 2 | r0=u16 packed_cursor |
| 080c7530 | write_card_list_oam_row_strip | render_card_display_text_panel_oam | 13 | r0=x_pixel; r1=y_pixel; r2=starting_attr2; r3=tile_row_count (u16) |
| 080c7638 | dispatch_card_list_oam_row_by_card_type | dispatch_card_display_oam_by_mode | 1 | no input parameters |
| 080c76c0 | render_jp_string_to_tile_line | render_jp_string_to_tile_line | 17 | r0=x_start; r1=y_start; r2=text; r3=cell_advance; stack0=measure_only; return r0=next_line_y |
| 080c786c | zero_card_name_vram_buf | clear_card_display_obj_tiles_mode_11 | 1 | no input parameters |
| 080c7894 | init_bg_vram_for_card_display | clear_card_display_obj_tiles_mode_12 | 2 | no input parameters |
| 080c78bc | init_card_icon_tile_and_palette | init_card_selection_panel_mode_13 | 2 | r0=initial_selection_index (low8) |
| 080c7950 | copy_game_text_to_card_name_vram | init_card_display_mode_with_game_text | 1 | r0=display_mode; r1=game_string_id; r2=mode_specific_argument |

参数仅写文档. 不调用签名、参数存储或类型 setter. 全部入口及 Function body 归属来自本段实际 native Core v2, 不用 nearest-label 推断 owner.

## 数据块分类

段内没有 ROM_INCBIN/.byte 裸块. 26 个双字节零对齐共 52 字节原样保留, 不作为代码或数据重新定义. 全 ROM raw/Thumb 静态搜索见 firststage-full-ROM-refscan-v1.json: 272 个候选地址, 8175 个结果项, 8153 个去重命中地址. 原始字节命中与原生 rich reference 分别保留.

## 符号化计划

### EQ_SLOTS

35 个槽写 operand0 data-equate. 先对现有 6402 条 GNU equate 完整求值复用, 所有值再与原 ROM 小端字逐槽核对. 新建 9 个 Equate, 全局 2503->2512, bindings 12803->12838.

### REF_SLOTS

48 个槽新增 USER_DEFINED/primary/operand0 DATA 引用, 15 个槽保留既有 DEFAULT DATA 引用的所有核心字段. 6 个 switch table 基址保留 ANALYSIS namespace/ID/类型, 不新建 table USER 标签. 仅 5 个目标由 DEFAULT 变为 USER primary: gFontState, gDuelCtx, 两个 OBJ 目的地址及 CARD_OVERLAY_TILE_SRC.

### RENAME_SLOTS

98 个自动名槽各建一个 USER 标签并写一条 ASCII EOL. 与 5 个目标合计 103 个新 USER ID, 其余已有身份保持. 每个槽的完整 before/after、真实 READ 消费者及来源行在 slots.tsv 和 slot-plan-v1.json.

| 槽 | ROM 值 | 动作 | GAS 表达式 | 槽名 |
|---|---|---|---|---|
| 080c6a10 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c6a10 |
| 080c6a14 | 02020160 | REF_ADD | gDuelCtx | ptr_gduelctx_080c6a14 |
| 080c6a18 | 00002f51 | EQ_ADD | DUEL_CTX_ZONE_STATE_OFF | value_duel_ctx_zone_state_off_080c6a18 |
| 080c6a1c | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c6a1c |
| 080c6a40 | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c6a40 |
| 080c6a44 | 080c6a48 | REF_ADD | switchD_080c6a3e__switchdataD_080c6a48 | ptr_switchd_080c6a3e__switchdatad_080c6a48_080c6a44 |
| 080c6a48 | 080c6a88 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a88 | (preserve) |
| 080c6a4c | 080c6a88 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a88 | (preserve) |
| 080c6a50 | 080c6a88 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a88 | (preserve) |
| 080c6a54 | 080c6a88 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a88 | (preserve) |
| 080c6a58 | 080c6a88 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a88 | (preserve) |
| 080c6a5c | 080c6a8e | CASE_VECTOR_PRESERVE_CORE | 0x080c6a8e | (preserve) |
| 080c6a60 | 080c6a8e | CASE_VECTOR_PRESERVE_CORE | 0x080c6a8e | (preserve) |
| 080c6a64 | 080c6a8e | CASE_VECTOR_PRESERVE_CORE | 0x080c6a8e | (preserve) |
| 080c6a68 | 080c6a8e | CASE_VECTOR_PRESERVE_CORE | 0x080c6a8e | (preserve) |
| 080c6a6c | 080c6a8e | CASE_VECTOR_PRESERVE_CORE | 0x080c6a8e | (preserve) |
| 080c6a70 | 080c6a94 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a94 | (preserve) |
| 080c6a74 | 080c6a9a | CASE_VECTOR_PRESERVE_CORE | 0x080c6a9a | (preserve) |
| 080c6a78 | 080c6a94 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a94 | (preserve) |
| 080c6a7c | 080c6a94 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a94 | (preserve) |
| 080c6a80 | 080c6a94 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a94 | (preserve) |
| 080c6a84 | 080c6a94 | CASE_VECTOR_PRESERVE_CORE | 0x080c6a94 | (preserve) |
| 080c6b00 | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c6b00 |
| 080c6b5c | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c6b5c |
| 080c6b60 | 080c6b64 | REF_ADD | switchD_080c6b58__switchdataD_080c6b64 | ptr_switchd_080c6b58__switchdatad_080c6b64_080c6b60 |
| 080c6b64 | 080c6ba4 | CASE_VECTOR_PRESERVE_CORE | 0x080c6ba4 | (preserve) |
| 080c6b68 | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b6c | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b70 | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b74 | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b78 | 080c6bb4 | CASE_VECTOR_PRESERVE_CORE | 0x080c6bb4 | (preserve) |
| 080c6b7c | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b80 | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b84 | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b88 | 080c6e74 | CASE_VECTOR_PRESERVE_CORE | 0x080c6e74 | (preserve) |
| 080c6b8c | 080c6c8a | CASE_VECTOR_PRESERVE_CORE | 0x080c6c8a | (preserve) |
| 080c6b90 | 080c6dca | CASE_VECTOR_PRESERVE_CORE | 0x080c6dca | (preserve) |
| 080c6b94 | 080c6c98 | CASE_VECTOR_PRESERVE_CORE | 0x080c6c98 | (preserve) |
| 080c6b98 | 080c6d20 | CASE_VECTOR_PRESERVE_CORE | 0x080c6d20 | (preserve) |
| 080c6b9c | 080c6db6 | CASE_VECTOR_PRESERVE_CORE | 0x080c6db6 | (preserve) |
| 080c6ba0 | 080c6dc0 | CASE_VECTOR_PRESERVE_CORE | 0x080c6dc0 | (preserve) |
| 080c6bfc | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c6bfc |
| 080c6c00 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6c00 |
| 080c6c18 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6c18 |
| 080c6c68 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c6c68 |
| 080c6c78 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6c78 |
| 080c6d04 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c6d04 |
| 080c6d14 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6d14 |
| 080c6d64 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c6d64 |
| 080c6d68 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6d68 |
| 080c6d80 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6d80 |
| 080c6e14 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c6e14 |
| 080c6e18 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6e18 |
| 080c6e38 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6e38 |
| 080c6ef4 | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c6ef4 |
| 080c6ef8 | 080c6efc | REF_ADD | switchD_080c6ef0__switchdataD_080c6efc | ptr_switchd_080c6ef0__switchdatad_080c6efc_080c6ef8 |
| 080c6efc | 080c6f3c | CASE_VECTOR_PRESERVE_CORE | 0x080c6f3c | (preserve) |
| 080c6f00 | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f04 | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f08 | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f0c | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f10 | 080c6f52 | CASE_VECTOR_PRESERVE_CORE | 0x080c6f52 | (preserve) |
| 080c6f14 | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f18 | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f1c | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f20 | 080c7056 | CASE_VECTOR_PRESERVE_CORE | 0x080c7056 | (preserve) |
| 080c6f24 | 080c6f66 | CASE_VECTOR_PRESERVE_CORE | 0x080c6f66 | (preserve) |
| 080c6f28 | 080c6fb0 | CASE_VECTOR_PRESERVE_CORE | 0x080c6fb0 | (preserve) |
| 080c6f2c | 080c6f70 | CASE_VECTOR_PRESERVE_CORE | 0x080c6f70 | (preserve) |
| 080c6f30 | 080c6f80 | CASE_VECTOR_PRESERVE_CORE | 0x080c6f80 | (preserve) |
| 080c6f34 | 080c6f90 | CASE_VECTOR_PRESERVE_CORE | 0x080c6f90 | (preserve) |
| 080c6f38 | 080c6fa0 | CASE_VECTOR_PRESERVE_CORE | 0x080c6fa0 | (preserve) |
| 080c6fe4 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c6fe4 |
| 080c6fe8 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c6fe8 |
| 080c6fec | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c6fec |
| 080c702c | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c702c |
| 080c7030 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c7030 |
| 080c7034 | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c7034 |
| 080c70cc | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c70cc |
| 080c70d0 | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c70d0 |
| 080c70d4 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c70d4 |
| 080c70d8 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c70d8 |
| 080c7104 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c7104 |
| 080c7108 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c7108 |
| 080c715c | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c715c |
| 080c7160 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c7160 |
| 080c71bc | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c71bc |
| 080c71c0 | 03000040 | REF_PRESERVE | gPrng | ptr_gprng_080c71c0 |
| 080c7224 | 03000040 | REF_PRESERVE | gPrng | ptr_gprng_080c7224 |
| 080c7228 | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c7228 |
| 080c722c | 00000215 | EQ_ADD | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | value_duel_field_ui_effect_flags_off_080c722c |
| 080c729c | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c729c |
| 080c72a0 | 02020160 | REF_ADD | gDuelCtx | ptr_gduelctx_080c72a0 |
| 080c72a4 | 00002f51 | EQ_ADD | DUEL_CTX_ZONE_STATE_OFF | value_duel_ctx_zone_state_off_080c72a4 |
| 080c72a8 | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c72a8 |
| 080c72ac | 00001cf4 | EQ_ADD | DUEL_FIELD_CURSOR_STATE_OFF | value_duel_field_cursor_state_off_080c72ac |
| 080c72b0 | 080c72b4 | REF_ADD | switchD_080c729a__switchdataD_080c72b4 | ptr_switchd_080c729a__switchdatad_080c72b4_080c72b0 |
| 080c72b4 | 080c72cc | CASE_VECTOR_PRESERVE_CORE | 0x080c72cc | (preserve) |
| 080c72b8 | 080c72e0 | CASE_VECTOR_PRESERVE_CORE | 0x080c72e0 | (preserve) |
| 080c72bc | 080c72e0 | CASE_VECTOR_PRESERVE_CORE | 0x080c72e0 | (preserve) |
| 080c72c0 | 080c73c8 | CASE_VECTOR_PRESERVE_CORE | 0x080c73c8 | (preserve) |
| 080c72c4 | 080c72e0 | CASE_VECTOR_PRESERVE_CORE | 0x080c72e0 | (preserve) |
| 080c72c8 | 080c72e0 | CASE_VECTOR_PRESERVE_CORE | 0x080c72e0 | (preserve) |
| 080c72dc | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c72dc |
| 080c7398 | 00000212 | EQ_ADD | DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | value_duel_field_cursor_group_toggle_off_080c7398 |
| 080c739c | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c739c |
| 080c73c0 | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c73c0 |
| 080c73c4 | 00000868 | EQ_ADD | PLAYER_BLOCK_STRIDE | value_player_block_stride_080c73c4 |
| 080c73fc | 0201e2a0 | REF_ADD | gDuelCardCtxBase | ptr_gduelcardctxbase_080c73fc |
| 080c7510 | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c7510 |
| 080c7590 | 00008040 | EQ_ADD | OBJ_SHAPE_SIZE_VERTICAL_8X32 | value_obj_shape_size_vertical_8x32_080c7590 |
| 080c75bc | 00008080 | EQ_ADD | CARD_IMAGE_RIGHT_COLUMN_OBJ_ATTR | value_card_image_right_column_obj_attr_080c75bc |
| 080c7634 | 00004040 | EQ_ADD | OBJ_SHAPE_SIZE_HORIZONTAL_32X8 | value_obj_shape_size_horizontal_32x8_080c7634 |
| 080c7654 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c7654 |
| 080c7658 | 00000a01 | EQ_ADD | FONT_STATE_DISPLAY_MODE_OFF | value_font_state_display_mode_off_080c7658 |
| 080c765c | 080c7660 | REF_ADD | switchD_080c7650__switchdataD_080c7660 | ptr_switchd_080c7650__switchdatad_080c7660_080c765c |
| 080c7660 | 080c7688 | CASE_VECTOR_PRESERVE_CORE | 0x080c7688 | (preserve) |
| 080c7664 | 080c76bc | CASE_VECTOR_PRESERVE_CORE | 0x080c76bc | (preserve) |
| 080c7668 | 080c768e | CASE_VECTOR_PRESERVE_CORE | 0x080c768e | (preserve) |
| 080c766c | 080c769a | CASE_VECTOR_PRESERVE_CORE | 0x080c769a | (preserve) |
| 080c7670 | 080c76a0 | CASE_VECTOR_PRESERVE_CORE | 0x080c76a0 | (preserve) |
| 080c7674 | 080c76a6 | CASE_VECTOR_PRESERVE_CORE | 0x080c76a6 | (preserve) |
| 080c7678 | 080c7694 | CASE_VECTOR_PRESERVE_CORE | 0x080c7694 | (preserve) |
| 080c767c | 080c76ac | CASE_VECTOR_PRESERVE_CORE | 0x080c76ac | (preserve) |
| 080c7680 | 080c76b2 | CASE_VECTOR_PRESERVE_CORE | 0x080c76b2 | (preserve) |
| 080c7684 | 080c76b8 | CASE_VECTOR_PRESERVE_CORE | 0x080c76b8 | (preserve) |
| 080c7728 | 02000000 | REF_ADD | EWRAM_BASE | render_text_ewram_base_080c7728 |
| 080c772c | 00006c2c | EQ_ADD | GSETTINGS_OFFSET | render_text_gsettings_offset_080c772c |
| 080c7860 | 0000821f | EQ_ADD | JP_ASCII_DIGIT_TO_FULLWIDTH_DELTA | value_jp_ascii_digit_to_fullwidth_delta_080c7860 |
| 080c7864 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c7864 |
| 080c7868 | 00000a16 | EQ_ADD | FONT_STATE_FINAL_TEXT_X_OFF | value_font_state_final_text_x_off_080c7868 |
| 080c7888 | 06014000 | REF_ADD | AOB_CARD_TILE_VRAM | ptr_aob_card_tile_vram_080c7888 |
| 080c788c | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c788c |
| 080c7890 | 00000a01 | EQ_ADD | FONT_STATE_DISPLAY_MODE_OFF | value_font_state_display_mode_off_080c7890 |
| 080c78b0 | 06014000 | REF_ADD | AOB_CARD_TILE_VRAM | ptr_aob_card_tile_vram_080c78b0 |
| 080c78b4 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c78b4 |
| 080c78b8 | 00000a01 | EQ_ADD | FONT_STATE_DISPLAY_MODE_OFF | value_font_state_display_mode_off_080c78b8 |
| 080c791c | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c791c |
| 080c7920 | 00000215 | EQ_ADD | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | value_duel_field_ui_effect_flags_off_080c7920 |
| 080c7924 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c7924 |
| 080c7928 | 00000a0e | EQ_ADD | FONT_STATE_SELECTION_INDEX_OFF | value_font_state_selection_index_off_080c7928 |
| 080c792c | fffff00f | EQ_ADD | FONT_STATE_SELECTION_INDEX_CLEAR_MASK | value_font_state_selection_index_clear_mask_080c792c |
| 080c7930 | 06014000 | REF_ADD | AOB_CARD_TILE_VRAM | ptr_aob_card_tile_vram_080c7930 |
| 080c7934 | 06013400 | REF_ADD | card_selection_panel_label_obj_tiles | ptr_card_selection_panel_label_obj_tiles_080c7934 |
| 080c7938 | 099082a4 | REF_ADD | card_count_panel_label_tiles | ptr_card_count_panel_label_tiles_080c7938 |
| 080c793c | 06010800 | REF_ADD | card_selection_panel_overlay_obj_tile | ptr_card_selection_panel_overlay_obj_tile_080c793c |
| 080c7940 | 09ccd2d0 | REF_ADD | CARD_OVERLAY_TILE_SRC | ptr_card_overlay_tile_src_080c7940 |
| 080c7944 | 05000260 | REF_ADD | OBJ_PALRAM_SLOT_3 | ptr_obj_palram_slot_3_080c7944 |
| 080c7948 | 09850c5c | REF_ADD | duel_field_shared_obj_palette | ptr_duel_field_shared_obj_palette_080c7948 |
| 080c794c | 00000a01 | EQ_ADD | FONT_STATE_DISPLAY_MODE_OFF | value_font_state_display_mode_off_080c794c |
| 080c7984 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c7984 |
| 080c79b8 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c79b8 |
| 080c79bc | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c79bc |
| 080c79c0 | 00000215 | EQ_ADD | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | value_duel_field_ui_effect_flags_off_080c79c0 |
| 080c79c4 | 080c79c8 | REF_ADD | switchD_080c79b4__switchdataD_080c79c8 | ptr_switchd_080c79b4__switchdatad_080c79c8_080c79c4 |
| 080c79c8 | 080c7a00 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a00 | (preserve) |
| 080c79cc | 080c7a32 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a32 | (preserve) |
| 080c79d0 | 080c7a10 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a10 | (preserve) |
| 080c79d4 | 080c7a64 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a64 | (preserve) |
| 080c79d8 | 080c7a6a | CASE_VECTOR_PRESERVE_CORE | 0x080c7a6a | (preserve) |
| 080c79dc | 080c7a72 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a72 | (preserve) |
| 080c79e0 | 080c7a7a | CASE_VECTOR_PRESERVE_CORE | 0x080c7a7a | (preserve) |
| 080c79e4 | 080c7a82 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a82 | (preserve) |
| 080c79e8 | 080c7a8a | CASE_VECTOR_PRESERVE_CORE | 0x080c7a8a | (preserve) |
| 080c79ec | 080c7a90 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a90 | (preserve) |
| 080c79f0 | 080c7a98 | CASE_VECTOR_PRESERVE_CORE | 0x080c7a98 | (preserve) |
| 080c79f4 | 080c7aa0 | CASE_VECTOR_PRESERVE_CORE | 0x080c7aa0 | (preserve) |
| 080c79f8 | 080c7ad0 | CASE_VECTOR_PRESERVE_CORE | 0x080c7ad0 | (preserve) |
| 080c79fc | 080c7ad6 | CASE_VECTOR_PRESERVE_CORE | 0x080c7ad6 | (preserve) |
| 080c7a0c | 06014000 | REF_ADD | AOB_CARD_TILE_VRAM | ptr_aob_card_tile_vram_080c7a0c |
| 080c7a38 | 03000040 | REF_PRESERVE | gPrng | ptr_gprng_080c7a38 |
| 080c7a5c | 0201c4e0 | REF_PRESERVE | gP1LifePoints | ptr_gp1lifepoints_080c7a5c |
| 080c7a60 | 00000215 | EQ_ADD | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | value_duel_field_ui_effect_flags_off_080c7a60 |
| 080c7ac4 | 0201f440 | REF_ADD | gFontState | ptr_gfontstate_080c7ac4 |
| 080c7ac8 | 02023130 | REF_ADD | gDuelFieldState | ptr_gduelfieldstate_080c7ac8 |
| 080c7acc | 00000215 | EQ_ADD | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | value_duel_field_ui_effect_flags_off_080c7acc |

### FUNC_RENAME

- 080c699c: set_zone_oam_coords_by_player -> render_zone_cursor_oam; indeg=4. 依据本函数指令与真实调用消费者, confidence high.
- 080c6a20: write_zone_slot_oam_descriptor -> select_zone_cursor_and_render_info; indeg=5. 依据本函数指令与真实调用消费者, confidence high.
- 080c6b04: decode_zone_oam_word_to_slot_fields -> move_zone_cursor_vertical; indeg=2. 依据本函数指令与真实调用消费者, confidence high.
- 080c6e9c: decode_zone_oam_word_to_cursor_fields -> move_zone_cursor_horizontal; indeg=2. 依据本函数指令与真实调用消费者, confidence high.
- 080c7530: write_card_list_oam_row_strip -> render_card_display_text_panel_oam; indeg=13. 依据本函数指令与真实调用消费者, confidence high.
- 080c786c: zero_card_name_vram_buf -> clear_card_display_obj_tiles_mode_11; indeg=1. 依据本函数指令与真实调用消费者, confidence high.
- 080c7894: init_bg_vram_for_card_display -> clear_card_display_obj_tiles_mode_12; indeg=2. 依据本函数指令与真实调用消费者, confidence high.
- 080c78bc: init_card_icon_tile_and_palette -> init_card_selection_panel_mode_13; indeg=2. 依据本函数指令与真实调用消费者, confidence high.
- 080c7950: copy_game_text_to_card_name_vram -> init_card_display_mode_with_game_text; indeg=1. 依据本函数指令与真实调用消费者, confidence high.
- 080c7638: dispatch_card_list_oam_row_by_card_type -> dispatch_card_display_oam_by_mode; indeg=1. 依据本函数指令与真实调用消费者, confidence high.

### PLATE

重写 13 个段内 PLATE, 同步 21 个含旧函数名的必要 context PLATE. 其中 3 个在本模块, 18 个在 asm17; 全部已有 Function, 不改变 body/ABI.

#### 080c4cd4 classify_player_hand_count_threshold

```text
Classify the player hand count against a threshold. r0 bit0 selects player; r1 low16 is threshold. Read u16 at gP1LifePoints+0xc+player*PLAYER_BLOCK_STRIDE, the hand-count field. Return0 for zero count,1 for nonzero count below threshold,2 otherwise. Read-only; seven calls from move_zone_cursor_vertical.
```

#### 080c699c render_zone_cursor_oam

```text
Draw the zone cursor at transform_zone_oam_coords_by_player(player, zone_type, sub_index). Select attr2 base 0x806 for zone 0, otherwise 0x802, and OR palette_bank<<12. Use OAM shape control 0x80. Refresh sorting only for the active player when both display gates are clear and zone is hand-end or zone 0xd.
```

#### 080c6a20 select_zone_cursor_and_render_info

```text
Normalize zones 0..4 to group 0 and zones 5..9 to group 5. Keep r2 as the absolute sub-index; for hand zone 0xb, adjust the first visible index to retain a seven-card window and refresh tiles. Store player bit7, zone bits6:0 and visible sub-index bits15:8 at gDuelFieldState+0x210, then render_duel_field_zone_info(player, original_zone, absolute_sub_index).
```

#### 080c6b04 move_zone_cursor_vertical

```text
Move a packed zone cursor vertically. The low16 input contains player bit7, zone bits6:0 and sub-index bits14:8. r1 selects up(0) or down(1), relative to gDuelCardCtxBase+4. Dispatch 16 zone cases; hand transitions use classify_player_hand_count_threshold and player hand counts. Return the repacked cursor in r0.
```

#### 080c6e9c move_zone_cursor_horizontal

```text
Move a packed zone cursor horizontally. Decode player bit7, zone bits6:0 and sub-index bits14:8 from low16. r1 selects left(0) or right(1), relative to gDuelCardCtxBase+4. Wrap field groups and update the seven-card hand window through refresh_player_field_slot_tiles when required. Return the repacked cursor in r0.
```

#### 080c707c check_zone_card_id_cache_valid

```text
Test whether the packed zone can supply a visible nonzero card ID. Decode player bit7, zone bits6:0 and sub-index bits14:8. Resolve the slot, adjust indices for hand and count-based zones, enforce the active-player or card-attribute guard, then call ensure_card_id_cache_entry with the slot record cache key. Return 1 for an eligible nonzero ID, else 0.
```

#### 080c716c apply_zone_cursor_step

```text
Apply input to a packed zone cursor. Confirmation can write a card ID at gDuelFieldState+0x21c and set UI-effect flag 4. Otherwise use selection-state and directional-input paths, including vertical and horizontal cursor moves. Store the new cursor at +0x210 and draw its OAM. Redraw zone information only when the cursor or hand-window base changes. Input fields are gPrng+0x146/+0x148, or +0x14e for zone 0xd.
```

#### 080c7530 render_card_display_text_panel_oam

```text
Draw a 184-pixel-wide text panel as seven OAM entries per vertical chunk. r0=x, r1=y, r2=starting attr2, r3=tile-row count. Process count-2 rows in chunks of 4, 2 or 1 tiles; use 32-pixel columns followed by 16- and 8-pixel right edges. Encode OAM shape/size in r1 of write_oam_entry_from_packed_args and advance attr2 across each chunk. No draw when count<=2.
```

#### 080c7638 dispatch_card_display_oam_by_mode

```text
Dispatch the current gFontState display mode at +0xa01 after subtracting 1. Accept indices 0..9 for modes 1..10; mode 2 and out-of-range values return without a renderer. The remaining nine modes call their existing OAM row renderers. Preserve switch case numbering and all existing Function boundaries.
```

#### 080c76c0 render_jp_string_to_tile_line

```text
Render or measure localized text at (r0,r1): r2=text, r3=cell advance, stack arg=measure-only. gSettings language bits select single-byte or two-byte decoding. Handle newline, @ ink control, digit conversion and 184-pixel wrapping with kinsoku checks. When drawing, call the matching glyph renderer twice for shadow and foreground. Store final x at gFontState+0xa16; return next line y in r0.
```

#### 080c786c clear_card_display_obj_tiles_mode_11

```text
Clear 0x4000 bytes at AOB_CARD_TILE_VRAM using zero_fill_by_halfword, then set gFontState display mode at +0xa01 to 0x0b. The helper count is in bytes. No input parameters.
```

#### 080c7894 clear_card_display_obj_tiles_mode_12

```text
Clear 0x4000 bytes at AOB_CARD_TILE_VRAM using zero_fill_by_halfword, then set gFontState display mode at +0xa01 to 0x0c. The helper count is in bytes. No input parameters.
```

#### 080c78bc init_card_selection_panel_mode_13

```text
Set UI-effect flag 0x10 at gDuelFieldState+0x215. Store the low8 initial selection index in bits11:4 of gFontState+0xa0e, preserving other bits. Clear 0x4000 OBJ bytes at AOB_CARD_TILE_VRAM, copy four label tiles and one overlay tile, then copy 0x20 palette bytes to OBJ palette slot3. Set gFontState display mode to 0x0d. Only r0 is an input.
```

#### 080c7950 init_card_display_mode_with_game_text

```text
Clear 0xa20 bytes at gFontState and copy a resolved game string to gFontState+1, or write an empty string. Set font-state flag1 and UI-effect flag4, then dispatch display modes 0..13 using the mode-specific r2 argument. Mode2 additionally checks input before falling back to mode1. Mode11 clears the request flags after its initializer; invalid modes clear them directly. Text is staged in EWRAM, not VRAM.
```

#### 080c82e4 tick_card_list_display_master

```text
Tick the card display from gFontState+0xa17/+0xa18 state flags. The zero-state path calls dispatch_card_display_oam_by_mode; state1 calls dispatch_card_display_state_by_mode. Within the zero-state path, read gFontState+0xa01 as the display mode and dispatch through the 14-entry table at 0x080c8384 after input checks. Input and callee results can update the state flags.
```

#### 080c89e8 update_zone_activation_display_state

```text
Update activation display flags for both players and 11 field slot types. dispatch_card_display_op invokes this after select_zone_cursor_and_render_info. Accumulate bit11 results from dispatch_zone_activation_by_state into gDuelZoneCtrl+0x30+player*4 and refresh the player activation bitmask.
```

#### 080cd0dc render_card_list_oam_row_by_cost_bar

```text
Render display mode8 for dispatch_card_display_oam_by_mode. Return if bits2:1 of gFontState+0xa1b exceed1. Form an eight-pixel row offset from gFontState+0xa03. Add u16[gFontState+0xa04+2*u16(gFontState+0xa14)] and1 to obtain Y. Call write_oam_entry_from_packed_args with X=0x34, shape/size0 and attr2=0x60.
```

#### 080cd138 render_card_list_oam_row_by_lp_counter

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Navigation uses gPrng+0x148 mask0xc0; confirmation updates gFontState+0xa14, and later states advance the +0xa1b/+0xa1c counter pair.
```

#### 080cd454 render_card_list_oam_row_by_single_slot

```text
Render display mode9 for dispatch_card_display_oam_by_mode. Let n=(u16[gFontState+0xa0e]>>4)&0xff. Compute Xbase=0x2a+__divsi3(184,2*n) and Xspacing=__divsi3(184,n). Bits2:1 at +0xa1b gate one packed and three checked cursor OBJ writes. Other state fields can add a marker. Then test bits1..6 at +0xa02 and draw one OBJ for each occupied entry.
```

#### 080cd5ec render_card_list_oam_row_by_nibble_rotate

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Navigation rotates the low nibble at gFontState+0xa0e until a permitted slot is found; later paths confirm or advance transition counters.
```

#### 080cd94c render_card_list_oam_row_by_flag_check

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Test bits0/1 of gPrng+0x148. If either is set, call sync_state_and_init_sprite(0x24) and return1; otherwise return0.
```

#### 080cdba8 render_card_list_oam_row_by_dual_slot

```text
Render display mode4 for dispatch_card_display_oam_by_mode. Let n=(u16[gFontState+0xa0e]>>4)&0xff. Compute Xbase=0x1c+__divsi3(200,2*n) and Xspacing=__divsi3(200,n). Bits2:1 at +0xa1b gate one packed and three checked cursor OBJ writes. Then test six occupancy bits at +0xa02; each set bit emits four entries through write_oam_entry_from_packed_args.
```

#### 080cdd70 render_card_list_oam_row_by_lp_nibble

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. State0 handles low-nibble selection, confirmation and cancellation from gPrng+0x148; state1 advances transition counters.
```

#### 080ce2f4 render_card_list_oam_row_by_type_icon

```text
Render display mode6 for dispatch_card_display_oam_by_mode. Form Y from gFontState+0xa03/+0xa04. Mask0x1fe00 in u32[gFontState+0xa18] selects palette bank4 when zero, otherwise3. Bits2:1 at +0xa1b gate the upper indexed-icon loop. Always draw six lower-row entries, using the selected bank when the index equals u16[gFontState+0xa14], and bank3 otherwise. All entries use write_oam_entry_from_packed_args.
```

#### 080ce428 render_card_list_oam_row_by_slot_advance

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Add the gFontState+0xa04 Y offset, draw five cursor sprites, then handle occupied-slot navigation or confirmation from gPrng+0x148.
```

#### 080ced0c render_card_list_oam_row_by_cursor_slot

```text
Render display mode3 for dispatch_card_display_oam_by_mode. Form an eight-pixel Y base from gFontState+0xa03. Return if bits2:1 at +0xa1b exceed1. Bit0 at +0xa17 selects the cursor path, which can call packed and checked OAM writers. The alternate path reads the coordinate at +0xa04+2*u16(gFontState+0xa14) and calls write_oam_entry_from_packed_args once.
```

#### 080cedd0 render_card_list_oam_row_by_jp_type

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. The gFontState+0xa17 bit0 gate controls drawing. Then dispatch the state at +0xa18 through the four existing transition cases.
```

#### 080cf490 render_card_list_oam_row_by_anim_frame

```text
Render display mode10 for dispatch_card_display_oam_by_mode. Draw six strip entries through write_oam_entry_from_packed_args, advancing X by0x20. If bits2:1 of gFontState+0xa1b are0 or1, extract bits3:2 of the halfword at gPrng+0x20c and draw one checked OAM entry plus one packed entry. The row count and Y offset at gFontState+0xa03/+0xa04 position the strip.
```

#### 080cf52c render_card_list_oam_row_by_stat_display

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Navigation updates the selection field and calls render_card_numeric_stat_to_bg. Other states handle confirmation, cancellation and transition counters.
```

#### 080cfad0 render_card_list_oam_row_by_rarity_flag

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Decode the gFontState+0xa18 state flags and draw 20 additional icon entries; division and remainder by10 select row/column coordinates.
```

#### 080d0150 render_card_list_oam_row_by_pack_column

```text
Render display mode7 for dispatch_card_display_oam_by_mode. Read the halfword at gPrng+0x20c. Use __divsi3 and modulo8 arithmetic to form an oscillating Q8 affine scale from this value and the state word at gFontState+0xa18. The halfword at +0xa14 selects between two draw paths. Each calls write_oam_entry_with_tile_inc and write_pack_obj_attr_by_dir_stacked, applying the scale to opposite entries.
```

#### 080d029c render_card_list_oam_row_by_lp_init

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Navigation uses gPrng+0x148 mask0x30, confirmation updates gFontState+0xa14 and sprite state, and later states advance transition counters.
```

#### 080d05e4 render_card_list_oam_row_by_pack_slot

```text
Render display mode1 for dispatch_card_display_oam_by_mode. Return if bits2:1 of gFontState+0xa1b exceed1. Form an eight-pixel row offset from gFontState+0xa03. Add u16[gFontState+0xa04+2*u16(gFontState+0xa14)] and1 to obtain Y. Call write_oam_entry_from_packed_args with X=0x34, shape/size0 and attr2=0x60.
```

#### 080d0640 render_card_list_oam_row_by_slot_nibble

```text
Render the card text panel through render_card_display_text_panel_oam using the global row count and tile attributes. Navigation uses gPrng+0x148 mask0xc0. Later states advance gFontState+0xa1b/+0xa1c, updating counter bit0 and preserving bit1.
```

### 指令 EOL

精确替换 apply_zone_cursor_step 的 58 条已有指令 EOL, 不新增其他指令注释. 旧注释把 gPrng 输入字段写成 gPageState, 以及把 0x146-0x46 的结果写成 0x40; 新文本按原 opcode 订正为 gPrng+0x148 和 0x100.

- 080c7178: `Truncate the packed cursor to low16 before decoding.`
- 080c717c: `Save the original packed cursor at stack+0.`
- 080c7186: `Extract packed cursor player bit7.`
- 080c718e: `r5 = packed cursor zone code, bits6:0.`
- 080c7194: `r7 = packed cursor sub-index, bits14:8.`
- 080c7196: `r2 = gDuelFieldState.`
- 080c71a4: `Save the first visible hand index from gDuelFieldState+0x4c+player*2.`
- 080c71a8: `Zone0xd uses the alternate confirmation input field.`
- 080c71b6: `Zone0xd confirmation mask = 0x100.`
- 080c71b8: `r4 points to the halfword input field gPrng+0x14e.`
- 080c71c4: `Other zones use the halfword input field gPrng+0x146.`
- 080c71cc: `Confirmation mask for other zones = 0x100.`
- 080c71ce: `Read the input halfword; the next AND selects its confirmation bit.`
- 080c71d8: `Hand zone0xb maps the visible sub-index through the first visible index.`
- 080c71e4: `No confirmation bit: continue to selection-state and direction handling.`
- 080c71ea: `check_zone_card_id_cache_valid(packed_cursor).`
- 080c71f0: `An ineligible zone draws its cursor without redrawing information.`
- 080c71f4: `resolve_zone_data_ptr_by_oam_word(packed_cursor) returns the slot record.`
- 080c7206: `ensure_card_id_cache_entry(cache_key) returns the display card ID.`
- 080c7212: `Store the selected card ID at gDuelFieldState+0x21c.`
- 080c721e: `Set UI-effect flag4 at gDuelFieldState+0x215.`
- 080c7220: `Return after recording the card request.`
- 080c7230: `Decode the unchanged cursor for its OAM draw.`
- 080c7248: `render_zone_cursor_oam(player, zone, sub_index, palette0).`
- 080c724c: `Return after the cursor-only draw.`
- 080c724e: `Test input bit0x200 in gPrng+0x148.`
- 080c725e: `No input bit0x200: enter the ordinary directional move path.`
- 080c7260: `gFontState bit0 gates the special selection-state path.`
- 080c7270: `gDuelCtx+0x2f51 bit0 also gates the special selection-state path.`
- 080c728c: `Dispatch u32 gP1FieldState over states0..5.`
- 080c72cc: `State0 reads the active player from gDuelCardCtxBase+4.`
- 080c72d4: `Prepare active-player bit7 for zone0xd.`
- 080c72e0: `Toggle gDuelFieldState+0x212 bit0 and search for a nonempty card.`
- 080c72fa: `Store the toggled group-selection flag.`
- 080c730e: `Search sub-indices0..4 in zone group0 through the card-ID cache.`
- 080c735e: `Search sub-indices0..4 in zone group5 through the card-ID cache.`
- 080c73a0: `Use the active player's hand count to decide zone0xb selection.`
- 080c73ba: `Select zone0xb for the active player.`
- 080c73c8: `State3 searches for a slot accepted by eval_slot_activation_guard_full.`
- 080c73d0: `eval_slot_activation_guard_full(active_player, sub_index, 1).`
- 080c7458: `Read gPrng+0x148 and apply up/down/left/right in sequence.`
- 080c7464: `UP: move_zone_cursor_vertical(packed_cursor, 0).`
- 080c7478: `DOWN: move_zone_cursor_vertical(packed_cursor, 1).`
- 080c748c: `LEFT: move_zone_cursor_horizontal(packed_cursor, 0).`
- 080c74a0: `RIGHT: move_zone_cursor_horizontal(packed_cursor, 1).`
- 080c74ae: `Finalize the selected packed cursor.`
- 080c74b8: `Write the packed cursor at gDuelFieldState+0x210.`
- 080c74c2: `Decode player, zone and visible sub-index from the new packed cursor.`
- 080c74d8: `render_zone_cursor_oam(player, zone, sub_index, palette0).`
- 080c74de: `Compare the new and saved packed cursors.`
- 080c74f0: `Compare current and saved first visible hand indices.`
- 080c74f2: `Neither cursor nor hand-window base changed: return without information redraw.`
- 080c74f4: `Hand zone0xb maps its visible index to the absolute hand index.`
- 080c7502: `r2 = first visible hand index + visible sub-index.`
- 080c7508: `render_duel_field_zone_info(player, 0xb, absolute_hand_index).`
- 080c7514: `Other zones render with the decoded sub-index directly.`
- 080c751a: `render_duel_field_zone_info(player, zone, sub_index).`
- 080c751e: `Restore locals and saved registers, then return.`

## carve 计划

0. 段内无 raw 数据块, 三个 ROM 资产目标均复用现有 GNU 资产定义. 不修改 asm/rom.s.

## disasm 计划

0. 不新建或删除 Function, 不改变 body/TMode/instruction/flow override/数据类型.

## 新增 constants

| 名称 | 值 | 文件 | 复用核对 |
|---|---|---|---|
| DUEL_FIELD_CURSOR_STATE_OFF | 00001cf4 | constants/ewram.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| DUEL_FIELD_CURSOR_GROUP_TOGGLE_OFF | 00000212 | constants/ewram.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| OBJ_SHAPE_SIZE_VERTICAL_8X32 | 00008040 | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| OBJ_SHAPE_SIZE_HORIZONTAL_32X8 | 00004040 | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| JP_ASCII_DIGIT_TO_FULLWIDTH_DELTA | 0000821f | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| FONT_STATE_DISPLAY_MODE_OFF | 00000a01 | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| FONT_STATE_SELECTION_INDEX_OFF | 00000a0e | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| FONT_STATE_FINAL_TEXT_X_OFF | 00000a16 | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| FONT_STATE_SELECTION_INDEX_CLEAR_MASK | fffff00f | constants/card_info.inc | 现有同值名称语义不同或无同值定义; 现有6402条equate完整求值核对. |
| card_selection_panel_label_obj_tiles | 06013400 | constants/gba_mem.inc | 现有6402条equate无同值定义; 78bc的tile_2d_row_copy明确给出OBJ目的地址和tile长度. |
| card_selection_panel_overlay_obj_tile | 06010800 | constants/gba_mem.inc | 现有6402条equate无同值定义; 78bc的tile_2d_row_copy明确给出OBJ目的地址和tile长度. |

同值但不同基址/字段语义的既有 equate 不混用. 0x1cf4 是从 gP1LifePoints 到 gP1FieldState 的偏移; 0x4040 是本 OAM writer 的 shape/size 编码, 与既有 off-screen XY 编码语义不同. EWRAM_BASE 与 GSETTINGS_OFFSET 保持两个独立槽, 不合成 gSettings 单字.

## §5.1 登记

0. 没有将正引用块登记为未引用.

## 消费者证据

- packed_cursor: u16低7位为zone,bit7为player,bits14:8为sub-index; 左移16再右移24是在读取原值bits15:8. confidence high.
  Evidence: asm/16_duelfield_zone.s:11475 @080c6b0c; asm/16_duelfield_zone.s:11485 @080c6b20; asm/16_duelfield_zone.s:11487 @080c6b24; asm/16_duelfield_zone.s:11991 @080c6ea4; asm/16_duelfield_zone.s:12001 @080c6eb8; asm/16_duelfield_zone.s:12003 @080c6ebc.
- input_axes: apply_zone_cursor_step以0x40/0x80调用vertical(0/1),以0x20/0x10调用horizontal(0/1); 各函数均在尾部返回packed cursor. confidence high.
  Evidence: asm/16_duelfield_zone.s:12769 @080c7464; asm/16_duelfield_zone.s:12773 @080c746c; asm/16_duelfield_zone.s:12779 @080c7478; asm/16_duelfield_zone.s:12783 @080c7480; asm/16_duelfield_zone.s:12789 @080c748c; asm/16_duelfield_zone.s:12793 @080c7494; asm/16_duelfield_zone.s:12799 @080c74a0; asm/16_duelfield_zone.s:12803 @080c74a8; asm/16_duelfield_zone.s:11982 @080c6e98; asm/16_duelfield_zone.s:12241 @080c707a.
- hand_window: gDuelFieldState+0x4c+player*2为first-visible hand index,七个可见位置; refresh_player_field_slot_tiles以字为单位写回该index. confidence high.
  Evidence: asm/16_duelfield_zone.s:11418 @080c6aa2; asm/16_duelfield_zone.s:11420 @080c6aa6; asm/16_duelfield_zone.s:11423 @080c6aac; asm/16_duelfield_zone.s:11427 @080c6ab4; asm/16_duelfield_zone.s:11429 @080c6ab8; asm/16_duelfield_zone.s:11440 @080c6aca; asm/16_duelfield_zone.s:12145 @080c6fcc; asm/16_duelfield_zone.s:12148 @080c6fd2; asm/16_duelfield_zone.s:12154 @080c6fde; asm/16_duelfield_zone.s:12209 @080c7042.
- font_state_text: 7950清gFontState 0xa20字节,字符串写gFontState+1,mode在+0xa01; 这是EWRAM staging. confidence high.
  Evidence: asm/16_duelfield_zone.s:13441 @080c795c; asm/16_duelfield_zone.s:13443 @080c7960; asm/16_duelfield_zone.s:13445 @080c7964; asm/16_duelfield_zone.s:13450 @080c7972; asm/16_duelfield_zone.s:13455 @080c797e; asm/16_duelfield_zone.s:13460 @080c7988; asm/16_duelfield_zone.s:13466 @080c7992; asm/16_duelfield_zone.s:13636 @080c7aee.
- clear_byte_count: zero_fill_by_halfword的r1单位为字节; 786c/7894/78bc的0x4000为16KiB. confidence high.
  Evidence: asm/16_duelfield_zone.s:13321 @080c7872; asm/16_duelfield_zone.s:13322 @080c7874; asm/16_duelfield_zone.s:13343 @080c789a; asm/16_duelfield_zone.s:13344 @080c789c; asm/16_duelfield_zone.s:13383 @080c78e6; asm/16_duelfield_zone.s:13384 @080c78e8.
- text_parameters: 76c0入口r2存text,r0存起始X,r1存起始Y,r3存advance; 入口stack0经32字节push+16字节local在sp+0x30取measure_only; 返回next-lineY. confidence high.
  Evidence: asm/16_duelfield_zone.s:13096 @080c76cc; asm/16_duelfield_zone.s:13097 @080c76ce; asm/16_duelfield_zone.s:13098 @080c76d0; asm/16_duelfield_zone.s:13099 @080c76d2; asm/16_duelfield_zone.s:13100 @080c76d4; asm/16_duelfield_zone.s:13170 @080c7756; asm/16_duelfield_zone.s:13260 @080c7802; asm/16_duelfield_zone.s:13296 @080c7846; asm/16_duelfield_zone.s:13297 @080c7848; asm/16_duelfield_zone.s:13298 @080c784a; asm/16_duelfield_zone.s:13299 @080c784c.
- panel_OAM: 7530的r0为X,r1为Y,r2为初始attr2,r3为tile高度; 每块七个对象,最后两列起点X+160/X+176,总宽184px; OAM控制值不是palette. confidence high.
  Evidence: asm/16_duelfield_zone.s:12880 @080c753c; asm/16_duelfield_zone.s:12881 @080c753e; asm/16_duelfield_zone.s:12882 @080c7540; asm/16_duelfield_zone.s:12884 @080c7544; asm/16_duelfield_zone.s:12887 @080c754a; asm/16_duelfield_zone.s:12912 @080c7576; asm/16_duelfield_zone.s:12939 @080c75a2; asm/16_duelfield_zone.s:12965 @080c75ce; asm/16_duelfield_zone.s:12990 @080c75f6; asm/16_duelfield_zone.s:12994 @080c75fe; asm/16_duelfield_zone.s:12999 @080c7608.
- mode13_selection: 78bc只使用r0低8位并存到gFontState+0xa0e的bits11:4; 其外部消费者cfb90..cfb98比较此字段与列表索引,不依赖卡片类型或属性入参. confidence high.
  Evidence: asm/16_duelfield_zone.s:13373 @080c78d2; asm/16_duelfield_zone.s:13374 @080c78d4; asm/16_duelfield_zone.s:13375 @080c78d6; asm/16_duelfield_zone.s:13377 @080c78da; asm/16_duelfield_zone.s:13379 @080c78de; asm/16_duelfield_zone.s:13380 @080c78e0; asm/16_duelfield_zone.s:13401 @080c7912; asm/16_duelfield_zone.s:13402 @080c7914.

OAM 参数的依据是 write_oam_entry_from_packed_args @080f616c: r0 低位构建 attr1 X, r0 高位构建 attr0 Y, r1 编码 shape/size, r2 原样写 attr2. zero_fill_by_halfword @080f4e74 和 copy_bytes_by_halfword @080f4ea4 均以字节计数. mode13 只消费 r0 低8位的 selection index, 不按卡片类型或属性选 ROM 源.

## 新增 R5 context 消费者证据

以下 8 个额外现名依赖使用独立冻结的 semantic-review-r5-supplement-v1.json. 其完整 native Function/body/原 ROM/ASM 证据已绑定, 本文不以旧 PLATE 的寄存器或字段说明替代消费者.

### 080cd0dc render_card_list_oam_row_by_cost_bar

- Display mode8 emits one cursor OBJ when ((u8[gFontState+0xa1b]>>1)&3)<=1; larger encoded states return without an OAM call. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:2406 @080cd0ee; asm/17_duelfield_pack_frame.s:2408 @080cd0f2. Full evidence remains in the bound supplement.
- BaseY=(10-(u8[gFontState+0xa03]>>1))*8; index=u16[gFontState+0xa14]; Y=u16[gFontState+0xa04+2*index]+BaseY+1; X=0x34. Call write_oam_entry_from_packed_args with r1=0,r2=0x60. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:2399 @080cd0e0; asm/17_duelfield_pack_frame.s:2401 @080cd0e4. Full evidence remains in the bound supplement.

### 080cd454 render_card_list_oam_row_by_single_slot

- Display mode9 uses n=(u16[gFontState+0xa0e]>>4)&0xff, computes Xbase=0x2a+__divsi3(184,2*n), and Xspacing=__divsi3(184,n). BaseY adds u16[gFontState+0xa04] to (10-(u8[font+0xa03]>>1))*8. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:2862 @080cd464; asm/17_duelfield_pack_frame.s:2864 @080cd468. Full evidence remains in the bound supplement.
- The cursor-corner path uses state bits2:1 at font+0xa1b, plus bit4 of u16[gPrng+0x20c]; it emits one ordinary and three checked corner OBJ calls. Additional marker rendering tests font+0xa08,+0xa06 and +0xa0a. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:2891 @080cd4a2; asm/17_duelfield_pack_frame.s:2894 @080cd4a8. Full evidence remains in the bound supplement.
- The final loop tests bits1..6 of u8[gFontState+0xa02] and draws occupied entries with shape/size0x40 and generated attr2. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:2991 @080cd572; asm/17_duelfield_pack_frame.s:2993 @080cd574. Full evidence remains in the bound supplement.

### 080cdba8 render_card_list_oam_row_by_dual_slot

- Display mode4 uses n=(u16[0x0201fe4e]>>4)&0xff, computes Xbase=0x1c+__divsi3(200,2*n) and Xspacing=__divsi3(200,n); 0x0201fe4e equals gFontState+0xa0e. BaseY uses row count at +0xa03 and offset +0xa04. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:3832 @080cdbb8; asm/17_duelfield_pack_frame.s:3833 @080cdbba. Full evidence remains in the bound supplement.
- The cursor-corner path is enabled for state bits2:1<=1 at font+0xa1b. Its offset uses bit4 of u16[gPrng+0x20c], then one ordinary and three checked OAM calls. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:3858 @080cdbf0; asm/17_duelfield_pack_frame.s:3861 @080cdbf6. Full evidence remains in the bound supplement.
- The final loop tests six occupancy bits at font+0xa02, emits four OBJ parts for each occupied entry, and advances X by __divsi3(200,n). The old statement limiting the entire path to six additional OBJ entries is incorrect. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:3949 @080cdcaa; asm/17_duelfield_pack_frame.s:3952 @080cdcb0. Full evidence remains in the bound supplement.

### 080ce2f4 render_card_list_oam_row_by_type_icon

- Display mode6 sets BaseY from font+0xa03 and +0xa04. A masked u32[font+0xa18]&0x1fe00 chooses palette bank4 when zero, otherwise3. These palette banks feed the selected lower-row icon, not an icon-count base. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:4788 @080ce306; asm/17_duelfield_pack_frame.s:4791 @080ce30c. Full evidence remains in the bound supplement.
- For encoded state ((u8[font+0xa1b]>>1)&3)<=1, the upper loop draws n=(u16[font+0xa0e]>>4)&0xff entries. Each looks up u16[font+0xa04+2*(index+1)] for icon tile and optional position selection. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:4814 @080ce338; asm/17_duelfield_pack_frame.s:4817 @080ce33e. Full evidence remains in the bound supplement.
- An unconditional lower-row loop draws six OBJ entries at X=0x32+index*0x1e, compares index to u16[0x0201fe54]==u16[font+0xa14], and uses palette4/3 for the selected entry versus palette3 for the other entries. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:4883 @080ce3be; asm/17_duelfield_pack_frame.s:4884 @080ce3c0. Full evidence remains in the bound supplement.

### 080ced0c render_card_list_oam_row_by_cursor_slot

- Display mode3 returns for encoded state bits2:1>1 at font+0xa1b. Its branch gate is font+0xa17 bit0; it does not read that gate from +0xa1c. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:6115 @080ced20; asm/17_duelfield_pack_frame.s:6118 @080ced26. Full evidence remains in the bound supplement.
- With the gate set, u32[font+0xa10] is tested as the current position. Nonzero position draws the upper arrow at X=0x88,Y=BaseY+u16[font+0xa04]. Position below ((u16[font+0xa0e]>>4)&0xff)-1 also draws the lower arrow using the checked helper and r3=0x4000. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:6130 @080ced3e; asm/17_duelfield_pack_frame.s:6131 @080ced40. Full evidence remains in the bound supplement.
- With the gate clear, a simple cursor uses index=u16[font+0xa14], Y=u16[font+0xa04+2*index]+BaseY+2,X=0x34,r1=0,r2=0x60. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:6181 @080ceda4; asm/17_duelfield_pack_frame.s:6182 @080ceda6. Full evidence remains in the bound supplement.

### 080cf490 render_card_list_oam_row_by_anim_frame

- Display mode10 always draws six 32-pixel-wide strip OBJ entries, X starting at0x30 and advancing0x20, with Y from row count at font+0xa03 plus u16[font+0xa04]. Their shape/size is0x4080 and attr2 starts at0x1c0 then advances4 per entry. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:7104 @080cf494; asm/17_duelfield_pack_frame.s:7107 @080cf49a. Full evidence remains in the bound supplement.
- When ((u8[font+0xa1b]>>1)&3)<=1, read delta=(u16[gPrng+0x20c]&0xf)>>2. Emit two cursor pieces at Y=BaseY+4; their X values are0x58-delta and0xbc+delta. r3=0x1000 is passed to the checked helper; ordinary helper r2 remains0x60. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:7133 @080cf4ce; asm/17_duelfield_pack_frame.s:7136 @080cf4d4. Full evidence remains in the bound supplement.

### 080d0150 render_card_list_oam_row_by_pack_column

- Display mode7 reads u16[gPrng+0x20c] and encoded state s=(u32[font+0xa18]>>9)&0xff. It divides the former by2-s and folds the quotient modulo8 into a triangular affine parameter, using the <=3 test on the remainder. No claim of a frame counter or bounded denominator range is needed. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:8785 @080d015e; asm/17_duelfield_pack_frame.s:8786 @080d0160. Full evidence remains in the bound supplement.
- u16[font+0xa14] selects which of two OBJ pieces uses the affine helper. Both branches call write_oam_entry_with_tile_inc and write_pack_obj_attr_by_dir_stacked, with X0x4a/0xae, row-derived Y plus font+0xa04, shape/size0x80 and attr2 0x18c/0x1cc. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:8852 @080d01e0; asm/17_duelfield_pack_frame.s:8854 @080d01e4. Full evidence remains in the bound supplement.

### 080d05e4 render_card_list_oam_row_by_pack_slot

- Display mode1 emits one cursor OBJ only when ((u8[font+0xa1b]>>1)&3)<=1. BaseY=(10-(u8[font+0xa03]>>1))*8; index=u16[font+0xa14]; Y=u16[font+0xa04+2*index]+BaseY+1; X=0x34,r1=0,r2=0x60. confidence high.
  Evidence: asm/17_duelfield_pack_frame.s:9387 @080d05e8; asm/17_duelfield_pack_frame.s:9389 @080d05ec. Full evidence remains in the bound supplement.

新增 080c82e4 context 的直接调用证据为 asm/16_duelfield_zone.s 中 080c8318 -> 080c7638. 该唯一 native incoming、完整 owner ABI/body 和 14 项显示模式表均在原 183 Function BEFORE 内. source-scope 逐地址许可这一个新增段外 BL 显示投影.

080d0150 的 Q8 affine scale 传参证据: asm/17_duelfield_pack_frame.s:8887 @080d0228 和 :8916 @080d0262 将 r9 左移16后送入 r3; asm/21_font_title_scene.s:6510 @080f6d04 保存高半字, :6730 @080f6e92 传给 write_obj_affine_rot_scale. 080f60e6/60e8/60ea 将其乘入正弦表并右移8写 OAM affine 矩阵. 这是 scale 系数, XY 坐标另行构造. confidence high.

## 完整后态与原生核验合同

实际 Core v2 为 183 Function/1933 word holders/2765 slot holders/578 target holders, 3262 去重 fullstates. 所有 holder 字段完整保持, 包含 getFunctionAt(even) 的完整 ABI 或实际 null. 43716 模块字节不变. protected_external_units 容器保留 range/units 两个键, range 为 [0x09e5ab58,0x09e5ab88), units 完整 48 行; 行数取 units 列表长度, 不取容器键数. whole Properties 的 26385 行及 header 全保留, 仅投影批准的 Function owner 名.

whole Tiny 完整保护 14980 行/2765 seeds/1600 typed edges. 15 条既有 typed-pointer 边的 source_primary 随源槽变 USER; 额外 DEFAULT+ 或 pointee-derived 显示名投影 0. 独立 0201f441 undefined1 保持独立. 原有 incoming 9258 加 48 条 DATA 为 9306, 每条完整引用保留 type/source/operand/primary 与身份字段. 原生 JSON 省略字段仍省略, 不补 null.

新 USER ID 只由实际 POST 提供不可预测的 103 个正 int64, 必须互异并与全项目 84196 个 before ID 不相交 (36258 static + 47938 dynamic, 后者有 public API 逐 ID 证明). POST 不提供 expected 的其他字段. Expected 从完整 BEFORE 和最小动作独立推导.

## 源码许可与 GAS

1933 个 word-holder 执行真实 exporter AST. 本段 163 个 native 精确表达式, 13 个明确 fallback; 139 个继承 pins 完整保留且新 13 槽无重叠, 得 152 个有效 pins. 70 个 native 表达式变化均在本段, 外部 word 表达式变化 0. 176 条最终表达式逐地址断言.

跨文件 BL 更名 18 处, 新增本模块段外 080c8318 一处, 按本轮 Root 口径合计 19; 另有原模型已列本模块段外 5 处 BL 按原 scope 保持投影, 所有段外 BL 合计 24. 所有源码 unit、指令 EOL、PLATE、label 和 expression 的具体 PC 在 source-scope-plan-v1.json; 其余源码字节/字段保持. Registry 34 个既有 tuple, 不追加; 两份 CSV 各 10 个 address-keyed name cell. 新 GNU 11 项, 不新增数据文件. source217 加 formal3/review1/Script1 为 runtime222.

不继承前段 R4/R7/NULL decode/body/override 动作. 落地由 Root/fixer 在独立 PASS 后完成 mature atomic claims、真实 ownedFalse 完整 POST/同 Program BEFORE 恢复、唯一保存、新进程 check、独立后验、全汇编导出、资产导出、构建及整个原 ROM byte-identical 验证.

## 求助

none. 无低置信度语义. 本执行器不自评分、不运行 Ghidra、不 build、不 commit.

## Executor Report: F16-Seg-6

- Slots: EQ_ADD=35 REF_ADD=48 REF_PRESERVE=15 CASE_CORE=78.
- USER=103 FUNC_RENAME=10 PLATE=34 EOL=156.
- carve=0 disasm=0 body=0 ABI=0 override=0 §5.1=0.
- New GNU=11, new Equates=9, new bindings=35.
- Help: none.
- proposal: doc/dev/refine/F16-Seg-6.proposal.md

