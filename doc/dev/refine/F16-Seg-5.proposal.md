# Refine Proposal: F16-Seg-5 [0x080c57c4..0x080c699c)

Status: UNREVIEWED. Executor analysis only. All names and mutations require independent review.

## 段测绘

段长4568B. 原11函数, 139源word, 79自动数据名. 三个raw块共1224B. 细化覆盖段内242word和外部R7表8word, 共250槽.

| Entry | Before | Proposed | Native incoming | Documented signature |
|--|--|--|--:|--|
| 0x080c57c4 | compute_card_sprite_oam_coords_by_zone | render_duel_action_menu_oam | 3 | `void render_duel_action_menu_oam(void)` |
| 0x080c5b78 | dispatch_duel_field_zone_oam_by_type | render_duel_action_menu_labels | 1 | `void render_duel_action_menu_labels(void)` |
| 0x080c6184 | init_duel_field_card_sprite_vram | init_duel_action_menu_vram | 0 | `u32 init_duel_action_menu_vram(void)` |
| 0x080c6240 | tick_card_sprite_oam_step_a | tick_duel_action_menu_open_step | 0 | `u32 tick_duel_action_menu_open_step(void)` |
| 0x080c6268 | tick_card_sprite_oam_step_b | tick_duel_action_menu_input_step | 0 | `u32 tick_duel_action_menu_input_step(void)` |
| 0x080c6490 | tick_card_sprite_oam_step_c | tick_duel_action_menu_close_step | 0 | `u32 tick_duel_action_menu_close_step(void)` |
| 0x080c64b8 | dispatch_duel_zone_pair_to_oam | run_duel_action_menu_card_info_transition | 1 | `u32 run_duel_action_menu_card_info_transition(void)` |
| 0x080c65b0 | tick_card_sprite_oam_phase_dispatch | tick_duel_action_menu_state_machine | 1 | `u32 tick_duel_action_menu_state_machine(void)` |
| 0x080c6638 | resolve_zone_data_ptr_by_oam_word | resolve_zone_data_ptr_by_oam_word | 12 | `void *resolve_zone_data_ptr_by_oam_word(u16 packed_selection)` |
| 0x080c678c | update_zone_oam_card_count_tag | repair_hand_zone_cursor_after_card_update | 4 | `void repair_hand_zone_cursor_after_card_update(void)` |
| 0x080c6800 | transform_zone_oam_coords_by_player | transform_zone_oam_coords_by_player | 4 | `u32 transform_zone_oam_coords_by_player(u32 player, u32 zone, u32 index)` |

文档签名用于解释寄存器消费者. 本段不修改Parameter/Return/storage/calling-convention/flags/identity. 9误名订正, 11ASCII PLATE. 既有gCardCtxSlotData用于菜单状态, packed选择来自field+0x210, 不是各函数APCS输入.

完整自动名槽及before/after见 `F16-Seg-5.slots.tsv`. 每行包含来源路径和完整原生DTO; 非本段word holder保留在全量1755word模型中.

## 数据块分类 (Rule 2/3)

| Block | Full ROM raw / THUMB counts | Classification | Evidence |
|--|--|--|--|
| 080c5c3c+1102 | raw=17, thumb=2 | disasm + pool definition + zero padding | All interior byte/even-Thumb candidates, all positions recorded in initial-full-rom-refscan-v1. |
| 080c60f4+4 | raw=0, thumb=0 | pool definition, no code | All interior byte/even-Thumb candidates, all positions recorded in initial-full-rom-refscan-v1. |
| 080c63e0+118 | raw=9, thumb=0 | disasm + pool definition + zero padding | All interior byte/even-Thumb candidates, all positions recorded in initial-full-rom-refscan-v1. |

5c3c块17个even raw匹配中14个为本函数case表实引用; 63e0块9个中8个为选择case表实引用. 其它raw/Thumb匹配位置完整登记, 不作为新增CFG入口; 实际覆盖由case表、分支流和原生指令验证确定. 有效入口按CFG逐stub覆盖. 60f4块虽然无绝对值持有者, PC6088的PC-relative LDR真实读取它, 不能登记为无引用. 其值09dc93c8复用game_str_en_0484, 文本Draw.

三个块精确分区: 395条指令794B, 103个pool word412B, 9个2B零对齐18B. 任何字节都不跨分区; 本段无未处理raw块.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS

37槽, 16等值域. 先复用7域28bindings, 新建9域9bindings.

| Slot | ROM value | Constant | GNU policy/file | Slot label |
|--|--|--|--|--|
| 0x080c5bf8 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5bf8 |
| 0x080c5c60 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5c60 |
| 0x080c5cac | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5cac |
| 0x080c5d04 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5d04 |
| 0x080c5d0c | 0x0003aac4 | DUEL_ACTION_LABEL_ES_JA_DELTA_0491 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0491_080c5d0c |
| 0x080c5d60 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5d60 |
| 0x080c5d68 | 0x0003aab8 | DUEL_ACTION_LABEL_ES_JA_DELTA_0487 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0487_080c5d68 |
| 0x080c5db0 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5db0 |
| 0x080c5dfc | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5dfc |
| 0x080c5e54 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5e54 |
| 0x080c5e5c | 0x0003aaae | DUEL_ACTION_LABEL_ES_JA_DELTA_0479 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0479_080c5e5c |
| 0x080c5ea4 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5ea4 |
| 0x080c5efc | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5efc |
| 0x080c5f04 | 0x0003aaac | DUEL_ACTION_LABEL_ES_JA_DELTA_0478 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0478_080c5f04 |
| 0x080c5f58 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5f58 |
| 0x080c5f60 | 0x0003aaa8 | DUEL_ACTION_LABEL_ES_JA_DELTA_0476_0477 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0476_0477_080c5f60 |
| 0x080c5fb4 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c5fb4 |
| 0x080c5fbc | 0x0003aab2 | DUEL_ACTION_LABEL_ES_JA_DELTA_0480_0481_0483_0485 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0480_0481_0483_0485_080c5fbc |
| 0x080c600c | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c600c |
| 0x080c6014 | 0x0003aa7e | DUEL_ACTION_LABEL_ES_JA_DELTA_0960 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0960_080c6014 |
| 0x080c6064 | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c6064 |
| 0x080c606c | 0x0003aab4 | DUEL_ACTION_LABEL_ES_JA_DELTA_0482_0484 | new constants/duel_field.inc | duel_action_label_es_ja_delta_0482_0484_080c606c |
| 0x080c60fc | 0x00006c2c | GSETTINGS_OFFSET | reuse constants/name_input.inc | gsettings_offset_080c60fc |
| 0x080c617c | 0x00008008 | CARD_DESC_RENDER_PARAM | reuse constants/card_info.inc | card_desc_render_param_080c617c |
| 0x080c6238 | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | reuse constants/ewram.inc | duel_field_fadein_flag_off_080c6238 |
| 0x080c62b4 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | reuse constants/ewram.inc | duel_field_prng_anim_flag_off_080c62b4 |
| 0x080c6618 | 0x00000222 | DUEL_FIELD_PRNG_ANIM_FLAG_OFF | reuse constants/ewram.inc | duel_field_prng_anim_flag_off_080c6618 |
| 0x080c66e8 | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | reuse constants/ewram.inc | duel_field_fadein_flag_off_080c66e8 |
| 0x080c6700 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse constants/ewram.inc | player_block_stride_080c6700 |
| 0x080c6724 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse constants/ewram.inc | player_block_stride_080c6724 |
| 0x080c673c | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse constants/ewram.inc | player_block_stride_080c673c |
| 0x080c6754 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse constants/ewram.inc | player_block_stride_080c6754 |
| 0x080c675c | 0xfffffbfc | HAND_ARRAY_TO_COUNT_NEG_OFF | reuse constants/ewram.inc | hand_array_to_count_neg_off_080c675c |
| 0x080c6780 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse constants/ewram.inc | player_block_stride_080c6780 |
| 0x080c6788 | 0xfffffa4c | ALT_HAND_ARRAY_TO_COUNT_NEG_OFF | reuse constants/ewram.inc | alt_hand_array_to_count_neg_off_080c6788 |
| 0x080c67d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse constants/ewram.inc | player_block_stride_080c67d4 |
| 0x080c6910 | 0x0000ffe8 | ZONE_COORD_X_NEG24_U16 | new constants/duel_field.inc | zone_coord_x_neg24_u16_080c6910 |

00008008复用CARD_DESC_RENDER_PARAM, 相同glyph-render API参数域有消费者证据. 8个JA到ES标量delta保留base+offset两槽结构, 不合成为无来源指针. u16(-24)保留原值0000ffe8. 完整常量搜索和78路径语言执行证据绑定在stage2 manifest.

### REF_SLOTS

143槽: 139新增USER DATA operand0, 4保留既有引用. 目标Ghidra主标签与源码GNU表达式分别列入graph和AST计划. 不覆盖既有ANALYSIS符号/namespace.

| Slot | Target | GAS expression | Action | Slot label |
|--|--|--|--|--|
| 0x080c5810 | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c5810 |
| 0x080c583c | 0x0201e2a0 | gDuelCardCtxBase | REF_ADD | ptr_g_duel_card_ctx_base_080c583c |
| 0x080c5880 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c5880 |
| 0x080c590c | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c590c |
| 0x080c594c | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c594c |
| 0x080c5978 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c5978 |
| 0x080c5990 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c5990 |
| 0x080c59b4 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c59b4 |
| 0x080c59d4 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c59d4 |
| 0x080c59fc | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c59fc |
| 0x080c5a14 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c5a14 |
| 0x080c5a38 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c5a38 |
| 0x080c5ad0 | 0x0201ff5a | gDuelActionMenuAnimStep | REF_ADD | ptr_g_duel_action_menu_anim_step_080c5ad0 |
| 0x080c5bec | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c5bec |
| 0x080c5bf0 | 0x02006ed0 | gFontJpCtx | REF_ADD | ptr_g_font_jp_ctx_080c5bf0 |
| 0x080c5bf4 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5bf4 |
| 0x080c5bfc | 0x09e5f854 | font_jp_base_table | REF_PRESERVE | ptr_font_jp_base_table_080c5bfc |
| 0x080c5c00 | 0x080c5c04 | duel_action_menu_label_case_table | REF_ADD | ptr_duel_action_menu_label_case_table_080c5c00 |
| 0x080c5c5c | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5c5c |
| 0x080c5c64 | 0x09dbe2d0 | game_str_ja_0476 | REF_ADD | ptr_game_str_ja_0476_080c5c64 |
| 0x080c5c6c | 0x09ded094 | game_str_it_0476 | REF_ADD | ptr_game_str_it_0476_080c5c6c |
| 0x080c5c74 | 0x09de0c4a | game_str_fr_0476 | REF_ADD | ptr_game_str_fr_0476_080c5c74 |
| 0x080c5c7c | 0x09dd49ba | game_str_de_0476 | REF_ADD | ptr_game_str_de_0476_080c5c7c |
| 0x080c5c84 | 0x09dc9380 | game_str_en_0476 | REF_ADD | ptr_game_str_en_0476_080c5c84 |
| 0x080c5ca8 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5ca8 |
| 0x080c5cb0 | 0x09dbe310 | game_str_ja_0483 | REF_ADD | ptr_game_str_ja_0483_080c5cb0 |
| 0x080c5cb8 | 0x09ded0ec | game_str_it_0483 | REF_ADD | ptr_game_str_it_0483_080c5cb8 |
| 0x080c5cc0 | 0x09de0c92 | game_str_fr_0483 | REF_ADD | ptr_game_str_fr_0483_080c5cc0 |
| 0x080c5cc8 | 0x09dd4a12 | game_str_de_0483 | REF_ADD | ptr_game_str_de_0483_080c5cc8 |
| 0x080c5cd0 | 0x09dc93c0 | game_str_en_0483 | REF_ADD | ptr_game_str_en_0483_080c5cd0 |
| 0x080c5d00 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5d00 |
| 0x080c5d08 | 0x09dbe34e | game_str_ja_0491 | REF_ADD | ptr_game_str_ja_0491_080c5d08 |
| 0x080c5d14 | 0x09ded134 | game_str_it_0491 | REF_ADD | ptr_game_str_it_0491_080c5d14 |
| 0x080c5d1c | 0x09de0cf6 | game_str_fr_0491 | REF_ADD | ptr_game_str_fr_0491_080c5d1c |
| 0x080c5d24 | 0x09dd4a5c | game_str_de_0491 | REF_ADD | ptr_game_str_de_0491_080c5d24 |
| 0x080c5d2c | 0x09dc9402 | game_str_en_0491 | REF_ADD | ptr_game_str_en_0491_080c5d2c |
| 0x080c5d5c | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5d5c |
| 0x080c5d64 | 0x09dbe32a | game_str_ja_0487 | REF_ADD | ptr_game_str_ja_0487_080c5d64 |
| 0x080c5d70 | 0x09ded10e | game_str_it_0487 | REF_ADD | ptr_game_str_it_0487_080c5d70 |
| 0x080c5d78 | 0x09de0cb8 | game_str_fr_0487 | REF_ADD | ptr_game_str_fr_0487_080c5d78 |
| 0x080c5d80 | 0x09dd4a36 | game_str_de_0487 | REF_ADD | ptr_game_str_de_0487_080c5d80 |
| 0x080c5d88 | 0x09dc93e0 | game_str_en_0487 | REF_ADD | ptr_game_str_en_0487_080c5d88 |
| 0x080c5dac | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5dac |
| 0x080c5db4 | 0x09dbe306 | game_str_ja_0482 | REF_ADD | ptr_game_str_ja_0482_080c5db4 |
| 0x080c5dbc | 0x09ded0e0 | game_str_it_0482 | REF_ADD | ptr_game_str_it_0482_080c5dbc |
| 0x080c5dc4 | 0x09de0c8a | game_str_fr_0482 | REF_ADD | ptr_game_str_fr_0482_080c5dc4 |
| 0x080c5dcc | 0x09dd4a06 | game_str_de_0482 | REF_ADD | ptr_game_str_de_0482_080c5dcc |
| 0x080c5dd4 | 0x09dc93b6 | game_str_en_0482 | REF_ADD | ptr_game_str_en_0482_080c5dd4 |
| 0x080c5df8 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5df8 |
| 0x080c5e00 | 0x09dbe300 | game_str_ja_0481 | REF_ADD | ptr_game_str_ja_0481_080c5e00 |
| 0x080c5e08 | 0x09ded0d4 | game_str_it_0481 | REF_ADD | ptr_game_str_it_0481_080c5e08 |
| 0x080c5e10 | 0x09de0c80 | game_str_fr_0481 | REF_ADD | ptr_game_str_fr_0481_080c5e10 |
| 0x080c5e18 | 0x09dd49fa | game_str_de_0481 | REF_ADD | ptr_game_str_de_0481_080c5e18 |
| 0x080c5e20 | 0x09dc93ae | game_str_en_0481 | REF_ADD | ptr_game_str_en_0481_080c5e20 |
| 0x080c5e50 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5e50 |
| 0x080c5e58 | 0x09dbe2ee | game_str_ja_0479 | REF_ADD | ptr_game_str_ja_0479_080c5e58 |
| 0x080c5e64 | 0x09ded0ba | game_str_it_0479 | REF_ADD | ptr_game_str_it_0479_080c5e64 |
| 0x080c5e6c | 0x09de0c6a | game_str_fr_0479 | REF_ADD | ptr_game_str_fr_0479_080c5e6c |
| 0x080c5e74 | 0x09dd49e4 | game_str_de_0479 | REF_ADD | ptr_game_str_de_0479_080c5e74 |
| 0x080c5e7c | 0x09dc939e | game_str_en_0479 | REF_ADD | ptr_game_str_en_0479_080c5e7c |
| 0x080c5ea0 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5ea0 |
| 0x080c5ea8 | 0x09dbe2f8 | game_str_ja_0480 | REF_ADD | ptr_game_str_ja_0480_080c5ea8 |
| 0x080c5eb0 | 0x09ded0c8 | game_str_it_0480 | REF_ADD | ptr_game_str_it_0480_080c5eb0 |
| 0x080c5eb8 | 0x09de0c78 | game_str_fr_0480 | REF_ADD | ptr_game_str_fr_0480_080c5eb8 |
| 0x080c5ec0 | 0x09dd49f2 | game_str_de_0480 | REF_ADD | ptr_game_str_de_0480_080c5ec0 |
| 0x080c5ec8 | 0x09dc93aa | game_str_en_0480 | REF_ADD | ptr_game_str_en_0480_080c5ec8 |
| 0x080c5ef8 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5ef8 |
| 0x080c5f00 | 0x09dbe2e4 | game_str_ja_0478 | REF_ADD | ptr_game_str_ja_0478_080c5f00 |
| 0x080c5f0c | 0x09ded0ae | game_str_it_0478 | REF_ADD | ptr_game_str_it_0478_080c5f0c |
| 0x080c5f14 | 0x09de0c60 | game_str_fr_0478 | REF_ADD | ptr_game_str_fr_0478_080c5f14 |
| 0x080c5f1c | 0x09dd49d6 | game_str_de_0478 | REF_ADD | ptr_game_str_de_0478_080c5f1c |
| 0x080c5f24 | 0x09dc9394 | game_str_en_0478 | REF_ADD | ptr_game_str_en_0478_080c5f24 |
| 0x080c5f54 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5f54 |
| 0x080c5f5c | 0x09dbe2da | game_str_ja_0477 | REF_ADD | ptr_game_str_ja_0477_080c5f5c |
| 0x080c5f68 | 0x09ded0a2 | game_str_it_0477 | REF_ADD | ptr_game_str_it_0477_080c5f68 |
| 0x080c5f70 | 0x09de0c56 | game_str_fr_0477 | REF_ADD | ptr_game_str_fr_0477_080c5f70 |
| 0x080c5f78 | 0x09dd49c8 | game_str_de_0477 | REF_ADD | ptr_game_str_de_0477_080c5f78 |
| 0x080c5f80 | 0x09dc938a | game_str_en_0477 | REF_ADD | ptr_game_str_en_0477_080c5f80 |
| 0x080c5fb0 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c5fb0 |
| 0x080c5fb8 | 0x09dbe31e | game_str_ja_0485 | REF_ADD | ptr_game_str_ja_0485_080c5fb8 |
| 0x080c5fc4 | 0x09ded100 | game_str_it_0485 | REF_ADD | ptr_game_str_it_0485_080c5fc4 |
| 0x080c5fcc | 0x09de0ca2 | game_str_fr_0485 | REF_ADD | ptr_game_str_fr_0485_080c5fcc |
| 0x080c5fd4 | 0x09dd4a24 | game_str_de_0485 | REF_ADD | ptr_game_str_de_0485_080c5fd4 |
| 0x080c5fdc | 0x09dc93ce | game_str_en_0485 | REF_ADD | ptr_game_str_en_0485_080c5fdc |
| 0x080c6008 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c6008 |
| 0x080c6010 | 0x09dc05dc | game_str_ja_0960 | REF_ADD | ptr_game_str_ja_0960_080c6010 |
| 0x080c601c | 0x09def4d0 | game_str_it_0960 | REF_ADD | ptr_game_str_it_0960_080c601c |
| 0x080c6024 | 0x09de3006 | game_str_fr_0960 | REF_ADD | ptr_game_str_fr_0960_080c6024 |
| 0x080c602c | 0x09dd6c9e | game_str_de_0960 | REF_ADD | ptr_game_str_de_0960_080c602c |
| 0x080c6034 | 0x09dcb280 | game_str_en_0960 | REF_ADD | ptr_game_str_en_0960_080c6034 |
| 0x080c6060 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c6060 |
| 0x080c6068 | 0x09dbe316 | game_str_ja_0484 | REF_ADD | ptr_game_str_ja_0484_080c6068 |
| 0x080c6074 | 0x09ded0f4 | game_str_it_0484 | REF_ADD | ptr_game_str_it_0484_080c6074 |
| 0x080c607c | 0x09de0c9c | game_str_fr_0484 | REF_ADD | ptr_game_str_fr_0484_080c607c |
| 0x080c6084 | 0x09dd4a1c | game_str_de_0484 | REF_ADD | ptr_game_str_de_0484_080c6084 |
| 0x080c60f4 | 0x09dc93c8 | game_str_en_0484 | REF_ADD | ptr_game_str_en_0484_080c60f4 |
| 0x080c60f8 | 0x02000000 | EWRAM_BASE | REF_ADD | ptr_ewram_base_080c60f8 |
| 0x080c6100 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6100 |
| 0x080c6104 | 0x06010000 | OBJ_TILE_VRAM_BASE | REF_ADD | ptr_obj_tile_vram_base_080c6104 |
| 0x080c6108 | 0x098532bc | duel_action_menu_row_frame_left_tiles | REF_ADD | ptr_duel_action_menu_row_frame_left_tiles_080c6108 |
| 0x080c6178 | 0x098532dc | duel_action_menu_row_frame_middle_tiles | REF_ADD | ptr_duel_action_menu_row_frame_middle_tiles_080c6178 |
| 0x080c6180 | 0x06010000 | OBJ_TILE_VRAM_BASE | REF_ADD | ptr_obj_tile_vram_base_080c6180 |
| 0x080c621c | 0x06013800 | VIJA_INTRO_TILE_VRAM | REF_ADD | ptr_vija_intro_tile_vram_080c621c |
| 0x080c6220 | 0x09852b9c | duel_action_menu_oam_tiles | REF_ADD | ptr_duel_action_menu_oam_tiles_080c6220 |
| 0x080c6224 | 0x05000280 | OBJ_PALRAM_SLOT_4 | REF_ADD | ptr_obj_palram_slot_4_080c6224 |
| 0x080c6228 | 0x0985329c | duel_field_panel_obj_palette | REF_ADD | ptr_duel_field_panel_obj_palette_080c6228 |
| 0x080c622c | 0x050002a0 | OBJ_PALRAM_SLOT_5 | REF_ADD | ptr_obj_palram_slot_5_080c622c |
| 0x080c6230 | 0x09850c5c | duel_field_shared_obj_palette | REF_ADD | ptr_duel_field_shared_obj_palette_080c6230 |
| 0x080c6234 | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c6234 |
| 0x080c623c | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c623c |
| 0x080c625c | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c625c |
| 0x080c62b0 | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c62b0 |
| 0x080c6360 | 0x03000040 | gPrng | REF_PRESERVE | ptr_g_prng_080c6360 |
| 0x080c6364 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6364 |
| 0x080c6398 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6398 |
| 0x080c639c | 0x080c63a0 | duel_action_menu_selection_case_table | REF_ADD | ptr_duel_action_menu_selection_case_table_080c639c |
| 0x080c63fc | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c63fc |
| 0x080c6418 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6418 |
| 0x080c6448 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6448 |
| 0x080c644c | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c644c |
| 0x080c6474 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6474 |
| 0x080c6478 | 0x020230c0 | gDuelZoneActivationState | REF_ADD | ptr_g_duel_zone_activation_state_080c6478 |
| 0x080c64ac | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c64ac |
| 0x080c6530 | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c6530 |
| 0x080c6534 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6534 |
| 0x080c6568 | 0x0203eeb0 | gDuelDispCtx | REF_ADD | ptr_g_duel_disp_ctx_080c6568 |
| 0x080c656c | 0x02029eb0 | gVijaState | REF_ADD | ptr_g_vija_state_080c656c |
| 0x080c6610 | 0x03000040 | gPrng | REF_PRESERVE | ptr_g_prng_080c6610 |
| 0x080c6614 | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c6614 |
| 0x080c661c | 0x09e5ab84 | duel_action_menu_phase_handlers | REF_ADD | ptr_duel_action_menu_phase_handlers_080c661c |
| 0x080c6620 | 0x0201ff30 | gCardCtxSlotData | REF_ADD | ptr_g_card_ctx_slot_data_080c6620 |
| 0x080c6664 | 0x080c6668 | switchD_080c6662__switchdataD_080c6668 | REF_ADD | ptr_switch_d_080c6662_switchdata_d_080c6668_080c6664 |
| 0x080c66e4 | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c66e4 |
| 0x080c6704 | 0x0201c510 | gDuelFieldSlots | REF_ADD | ptr_g_duel_field_slots_080c6704 |
| 0x080c6728 | 0x0201c600 | gP1FieldArrayCBase | REF_ADD | ptr_g_p1_field_array_c_base_080c6728 |
| 0x080c672c | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c672c |
| 0x080c6740 | 0x0201c740 | gP1SlotSetCodeArray | REF_ADD | ptr_g_p1_slot_set_code_array_080c6740 |
| 0x080c6758 | 0x0201c8f8 | gP1HandSlotArray | REF_ADD | ptr_g_p1_hand_slot_array_080c6758 |
| 0x080c6784 | 0x0201cab0 | gP1AltHandSlotArray | REF_ADD | ptr_g_p1_alt_hand_slot_array_080c6784 |
| 0x080c67cc | 0x02023130 | gDuelFieldState | REF_ADD | ptr_g_duel_field_state_080c67cc |
| 0x080c67d0 | 0x0201c4e0 | gP1LifePoints | REF_PRESERVE | ptr_g_p1_life_points_080c67d0 |
| 0x080c6838 | 0x0201e2a0 | gDuelCardCtxBase | REF_ADD | ptr_g_duel_card_ctx_base_080c6838 |
| 0x080c683c | 0x080c6840 | switchD_080c6834__switchdataD_080c6840 | REF_ADD | ptr_switch_d_080c6834_switchdata_d_080c6840_080c683c |

### RENAME_SLOTS

62个even case-vector核心保持字节/类型/引用不变, 仅批准的目标USER标签自然投影到rich target metadata/GAS表达式. 表值不加1, 不新增computed jump case refs.

| Slot | Original even value | GAS expression |
|--|--|--|
| 0x080c5c04 | 0x080c5c3c | duel_action_label_card_view_select_language |
| 0x080c5c08 | 0x080c5c88 | duel_action_label_attack_select_language |
| 0x080c5c0c | 0x080c5cd4 | duel_action_label_list_select_language |
| 0x080c5c10 | 0x080c5d30 | duel_action_label_special_summon_select_language |
| 0x080c5c14 | 0x080c5d8c | duel_action_label_activate_select_language |
| 0x080c5c18 | 0x080c5dd8 | duel_action_label_summon_select_language |
| 0x080c5c1c | 0x080c5e24 | duel_action_label_flip_summon_select_language |
| 0x080c5c20 | 0x080c5e80 | duel_action_label_set_select_language |
| 0x080c5c24 | 0x080c5e80 | duel_action_label_set_select_language |
| 0x080c5c28 | 0x080c5ecc | duel_action_label_attack_position_select_language |
| 0x080c5c2c | 0x080c5f28 | duel_action_label_defense_position_select_language |
| 0x080c5c30 | 0x080c5f84 | duel_action_label_surrender_select_language |
| 0x080c5c34 | 0x080c5fe0 | duel_action_label_ok_select_language |
| 0x080c5c38 | 0x080c6038 | duel_action_label_draw_select_language |
| 0x080c63a0 | 0x080c63e0 | duel_action_menu_prepare_field_target |
| 0x080c63a4 | 0x080c6456 | 0x080c6456 |
| 0x080c63a8 | 0x080c6456 | 0x080c6456 |
| 0x080c63ac | 0x080c6456 | 0x080c6456 |
| 0x080c63b0 | 0x080c6456 | 0x080c6456 |
| 0x080c63b4 | 0x080c63e0 | duel_action_menu_prepare_field_target |
| 0x080c63b8 | 0x080c6456 | 0x080c6456 |
| 0x080c63bc | 0x080c6456 | 0x080c6456 |
| 0x080c63c0 | 0x080c6456 | 0x080c6456 |
| 0x080c63c4 | 0x080c6456 | 0x080c6456 |
| 0x080c63c8 | 0x080c63e0 | duel_action_menu_prepare_field_target |
| 0x080c63cc | 0x080c641c | duel_action_menu_prepare_hand_target |
| 0x080c63d0 | 0x080c6400 | duel_action_menu_prepare_special_zone_target |
| 0x080c63d4 | 0x080c6400 | duel_action_menu_prepare_special_zone_target |
| 0x080c63d8 | 0x080c6400 | duel_action_menu_prepare_special_zone_target |
| 0x080c63dc | 0x080c6400 | duel_action_menu_prepare_special_zone_target |
| 0x080c6668 | 0x080c66a8 | 0x080c66a8 |
| 0x080c666c | 0x080c66a8 | 0x080c66a8 |
| 0x080c6670 | 0x080c66a8 | 0x080c66a8 |
| 0x080c6674 | 0x080c66a8 | 0x080c66a8 |
| 0x080c6678 | 0x080c66a8 | 0x080c66a8 |
| 0x080c667c | 0x080c66ec | 0x080c66ec |
| 0x080c6680 | 0x080c66ec | 0x080c66ec |
| 0x080c6684 | 0x080c66ec | 0x080c66ec |
| 0x080c6688 | 0x080c66ec | 0x080c66ec |
| 0x080c668c | 0x080c66ec | 0x080c66ec |
| 0x080c6690 | 0x080c66ec | 0x080c66ec |
| 0x080c6694 | 0x080c6708 | 0x080c6708 |
| 0x080c6698 | 0x080c6778 | 0x080c6778 |
| 0x080c669c | 0x080c6730 | 0x080c6730 |
| 0x080c66a0 | 0x080c6744 | 0x080c6744 |
| 0x080c66a4 | 0x080c6760 | 0x080c6760 |
| 0x080c6840 | 0x080c6880 | 0x080c6880 |
| 0x080c6844 | 0x080c6992 | 0x080c6992 |
| 0x080c6848 | 0x080c6992 | 0x080c6992 |
| 0x080c684c | 0x080c6992 | 0x080c6992 |
| 0x080c6850 | 0x080c6992 | 0x080c6992 |
| 0x080c6854 | 0x080c689e | 0x080c689e |
| 0x080c6858 | 0x080c6992 | 0x080c6992 |
| 0x080c685c | 0x080c6992 | 0x080c6992 |
| 0x080c6860 | 0x080c6992 | 0x080c6992 |
| 0x080c6864 | 0x080c6992 | 0x080c6992 |
| 0x080c6868 | 0x080c68c4 | 0x080c68c4 |
| 0x080c686c | 0x080c68da | 0x080c68da |
| 0x080c6870 | 0x080c6914 | 0x080c6914 |
| 0x080c6874 | 0x080c693a | 0x080c693a |
| 0x080c6878 | 0x080c6964 | 0x080c6964 |
| 0x080c687c | 0x080c697a | 0x080c697a |

### USER-label graph

共333地址: literal180, code-block79, case-table2, existing-GNU strings65, RAM byte1, ROM assets5, R7 tablebase1. 65字符串直接复用已有GNU标签, 不新carve文本. 名称及理由逐地址如下.

| Address | Name | Kind |
|--|--|--|
| 0x0201ff5a | gDuelActionMenuAnimStep | RAM |
| 0x080c5810 | ptr_g_duel_field_state_080c5810 | literal |
| 0x080c583c | ptr_g_duel_card_ctx_base_080c583c | literal |
| 0x080c5880 | ptr_g_card_ctx_slot_data_080c5880 | literal |
| 0x080c590c | ptr_g_card_ctx_slot_data_080c590c | literal |
| 0x080c594c | ptr_g_card_ctx_slot_data_080c594c | literal |
| 0x080c5978 | ptr_g_duel_action_menu_anim_step_080c5978 | literal |
| 0x080c5990 | ptr_g_duel_action_menu_anim_step_080c5990 | literal |
| 0x080c59b4 | ptr_g_duel_action_menu_anim_step_080c59b4 | literal |
| 0x080c59d4 | ptr_g_duel_action_menu_anim_step_080c59d4 | literal |
| 0x080c59fc | ptr_g_duel_action_menu_anim_step_080c59fc | literal |
| 0x080c5a14 | ptr_g_duel_action_menu_anim_step_080c5a14 | literal |
| 0x080c5a38 | ptr_g_duel_action_menu_anim_step_080c5a38 | literal |
| 0x080c5ad0 | ptr_g_duel_action_menu_anim_step_080c5ad0 | literal |
| 0x080c5bec | ptr_g_card_ctx_slot_data_080c5bec | literal |
| 0x080c5bf0 | ptr_g_font_jp_ctx_080c5bf0 | literal |
| 0x080c5bf4 | ptr_ewram_base_080c5bf4 | literal |
| 0x080c5bf8 | gsettings_offset_080c5bf8 | literal |
| 0x080c5bfc | ptr_font_jp_base_table_080c5bfc | literal |
| 0x080c5c00 | ptr_duel_action_menu_label_case_table_080c5c00 | literal |
| 0x080c5c04 | duel_action_menu_label_case_table | source_case_table |
| 0x080c5c3c | duel_action_label_card_view_select_language | code_block |
| 0x080c5c5c | ptr_ewram_base_080c5c5c | literal |
| 0x080c5c60 | gsettings_offset_080c5c60 | literal |
| 0x080c5c64 | ptr_game_str_ja_0476_080c5c64 | literal |
| 0x080c5c68 | duel_action_label_card_view_it | code_block |
| 0x080c5c6c | ptr_game_str_it_0476_080c5c6c | literal |
| 0x080c5c70 | duel_action_label_card_view_fr | code_block |
| 0x080c5c74 | ptr_game_str_fr_0476_080c5c74 | literal |
| 0x080c5c78 | duel_action_label_card_view_de | code_block |
| 0x080c5c7c | ptr_game_str_de_0476_080c5c7c | literal |
| 0x080c5c80 | duel_action_label_card_view_en | code_block |
| 0x080c5c84 | ptr_game_str_en_0476_080c5c84 | literal |
| 0x080c5c88 | duel_action_label_attack_select_language | code_block |
| 0x080c5ca8 | ptr_ewram_base_080c5ca8 | literal |
| 0x080c5cac | gsettings_offset_080c5cac | literal |
| 0x080c5cb0 | ptr_game_str_ja_0483_080c5cb0 | literal |
| 0x080c5cb4 | duel_action_label_attack_it | code_block |
| 0x080c5cb8 | ptr_game_str_it_0483_080c5cb8 | literal |
| 0x080c5cbc | duel_action_label_attack_fr | code_block |
| 0x080c5cc0 | ptr_game_str_fr_0483_080c5cc0 | literal |
| 0x080c5cc4 | duel_action_label_attack_de | code_block |
| 0x080c5cc8 | ptr_game_str_de_0483_080c5cc8 | literal |
| 0x080c5ccc | duel_action_label_attack_en | code_block |
| 0x080c5cd0 | ptr_game_str_en_0483_080c5cd0 | literal |
| 0x080c5cd4 | duel_action_label_list_select_language | code_block |
| 0x080c5cf8 | duel_action_label_es_delta_0491 | code_block |
| 0x080c5d00 | ptr_ewram_base_080c5d00 | literal |
| 0x080c5d04 | gsettings_offset_080c5d04 | literal |
| 0x080c5d08 | ptr_game_str_ja_0491_080c5d08 | literal |
| 0x080c5d0c | duel_action_label_es_ja_delta_0491_080c5d0c | literal |
| 0x080c5d10 | duel_action_label_list_it | code_block |
| 0x080c5d14 | ptr_game_str_it_0491_080c5d14 | literal |
| 0x080c5d18 | duel_action_label_list_fr | code_block |
| 0x080c5d1c | ptr_game_str_fr_0491_080c5d1c | literal |
| 0x080c5d20 | duel_action_label_list_de | code_block |
| 0x080c5d24 | ptr_game_str_de_0491_080c5d24 | literal |
| 0x080c5d28 | duel_action_label_list_en | code_block |
| 0x080c5d2c | ptr_game_str_en_0491_080c5d2c | literal |
| 0x080c5d30 | duel_action_label_special_summon_select_language | code_block |
| 0x080c5d54 | duel_action_label_es_delta_0487 | code_block |
| 0x080c5d5c | ptr_ewram_base_080c5d5c | literal |
| 0x080c5d60 | gsettings_offset_080c5d60 | literal |
| 0x080c5d64 | ptr_game_str_ja_0487_080c5d64 | literal |
| 0x080c5d68 | duel_action_label_es_ja_delta_0487_080c5d68 | literal |
| 0x080c5d6c | duel_action_label_special_summon_it | code_block |
| 0x080c5d70 | ptr_game_str_it_0487_080c5d70 | literal |
| 0x080c5d74 | duel_action_label_special_summon_fr | code_block |
| 0x080c5d78 | ptr_game_str_fr_0487_080c5d78 | literal |
| 0x080c5d7c | duel_action_label_special_summon_de | code_block |
| 0x080c5d80 | ptr_game_str_de_0487_080c5d80 | literal |
| 0x080c5d84 | duel_action_label_special_summon_en | code_block |
| 0x080c5d88 | ptr_game_str_en_0487_080c5d88 | literal |
| 0x080c5d8c | duel_action_label_activate_select_language | code_block |
| 0x080c5dac | ptr_ewram_base_080c5dac | literal |
| 0x080c5db0 | gsettings_offset_080c5db0 | literal |
| 0x080c5db4 | ptr_game_str_ja_0482_080c5db4 | literal |
| 0x080c5db8 | duel_action_label_activate_it | code_block |
| 0x080c5dbc | ptr_game_str_it_0482_080c5dbc | literal |
| 0x080c5dc0 | duel_action_label_activate_fr | code_block |
| 0x080c5dc4 | ptr_game_str_fr_0482_080c5dc4 | literal |
| 0x080c5dc8 | duel_action_label_activate_de | code_block |
| 0x080c5dcc | ptr_game_str_de_0482_080c5dcc | literal |
| 0x080c5dd0 | duel_action_label_activate_en | code_block |
| 0x080c5dd4 | ptr_game_str_en_0482_080c5dd4 | literal |
| 0x080c5dd8 | duel_action_label_summon_select_language | code_block |
| 0x080c5df8 | ptr_ewram_base_080c5df8 | literal |
| 0x080c5dfc | gsettings_offset_080c5dfc | literal |
| 0x080c5e00 | ptr_game_str_ja_0481_080c5e00 | literal |
| 0x080c5e04 | duel_action_label_summon_it | code_block |
| 0x080c5e08 | ptr_game_str_it_0481_080c5e08 | literal |
| 0x080c5e0c | duel_action_label_summon_fr | code_block |
| 0x080c5e10 | ptr_game_str_fr_0481_080c5e10 | literal |
| 0x080c5e14 | duel_action_label_summon_de | code_block |
| 0x080c5e18 | ptr_game_str_de_0481_080c5e18 | literal |
| 0x080c5e1c | duel_action_label_summon_en | code_block |
| 0x080c5e20 | ptr_game_str_en_0481_080c5e20 | literal |
| 0x080c5e24 | duel_action_label_flip_summon_select_language | code_block |
| 0x080c5e48 | duel_action_label_es_delta_0479 | code_block |
| 0x080c5e50 | ptr_ewram_base_080c5e50 | literal |
| 0x080c5e54 | gsettings_offset_080c5e54 | literal |
| 0x080c5e58 | ptr_game_str_ja_0479_080c5e58 | literal |
| 0x080c5e5c | duel_action_label_es_ja_delta_0479_080c5e5c | literal |
| 0x080c5e60 | duel_action_label_flip_summon_it | code_block |
| 0x080c5e64 | ptr_game_str_it_0479_080c5e64 | literal |
| 0x080c5e68 | duel_action_label_flip_summon_fr | code_block |
| 0x080c5e6c | ptr_game_str_fr_0479_080c5e6c | literal |
| 0x080c5e70 | duel_action_label_flip_summon_de | code_block |
| 0x080c5e74 | ptr_game_str_de_0479_080c5e74 | literal |
| 0x080c5e78 | duel_action_label_flip_summon_en | code_block |
| 0x080c5e7c | ptr_game_str_en_0479_080c5e7c | literal |
| 0x080c5e80 | duel_action_label_set_select_language | code_block |
| 0x080c5ea0 | ptr_ewram_base_080c5ea0 | literal |
| 0x080c5ea4 | gsettings_offset_080c5ea4 | literal |
| 0x080c5ea8 | ptr_game_str_ja_0480_080c5ea8 | literal |
| 0x080c5eac | duel_action_label_set_it | code_block |
| 0x080c5eb0 | ptr_game_str_it_0480_080c5eb0 | literal |
| 0x080c5eb4 | duel_action_label_set_fr | code_block |
| 0x080c5eb8 | ptr_game_str_fr_0480_080c5eb8 | literal |
| 0x080c5ebc | duel_action_label_set_de | code_block |
| 0x080c5ec0 | ptr_game_str_de_0480_080c5ec0 | literal |
| 0x080c5ec4 | duel_action_label_set_en | code_block |
| 0x080c5ec8 | ptr_game_str_en_0480_080c5ec8 | literal |
| 0x080c5ecc | duel_action_label_attack_position_select_language | code_block |
| 0x080c5ef0 | duel_action_label_es_delta_0478 | code_block |
| 0x080c5ef8 | ptr_ewram_base_080c5ef8 | literal |
| 0x080c5efc | gsettings_offset_080c5efc | literal |
| 0x080c5f00 | ptr_game_str_ja_0478_080c5f00 | literal |
| 0x080c5f04 | duel_action_label_es_ja_delta_0478_080c5f04 | literal |
| 0x080c5f08 | duel_action_label_attack_position_it | code_block |
| 0x080c5f0c | ptr_game_str_it_0478_080c5f0c | literal |
| 0x080c5f10 | duel_action_label_attack_position_fr | code_block |
| 0x080c5f14 | ptr_game_str_fr_0478_080c5f14 | literal |
| 0x080c5f18 | duel_action_label_attack_position_de | code_block |
| 0x080c5f1c | ptr_game_str_de_0478_080c5f1c | literal |
| 0x080c5f20 | duel_action_label_attack_position_en | code_block |
| 0x080c5f24 | ptr_game_str_en_0478_080c5f24 | literal |
| 0x080c5f28 | duel_action_label_defense_position_select_language | code_block |
| 0x080c5f46 | duel_action_label_test_es_0476_0477 | code_block |
| 0x080c5f4c | duel_action_label_es_delta_0476_0477 | code_block |
| 0x080c5f54 | ptr_ewram_base_080c5f54 | literal |
| 0x080c5f58 | gsettings_offset_080c5f58 | literal |
| 0x080c5f5c | ptr_game_str_ja_0477_080c5f5c | literal |
| 0x080c5f60 | duel_action_label_es_ja_delta_0476_0477_080c5f60 | literal |
| 0x080c5f64 | duel_action_label_defense_position_it | code_block |
| 0x080c5f68 | ptr_game_str_it_0477_080c5f68 | literal |
| 0x080c5f6c | duel_action_label_defense_position_fr | code_block |
| 0x080c5f70 | ptr_game_str_fr_0477_080c5f70 | literal |
| 0x080c5f74 | duel_action_label_defense_position_de | code_block |
| 0x080c5f78 | ptr_game_str_de_0477_080c5f78 | literal |
| 0x080c5f7c | duel_action_label_defense_position_en | code_block |
| 0x080c5f80 | ptr_game_str_en_0477_080c5f80 | literal |
| 0x080c5f84 | duel_action_label_surrender_select_language | code_block |
| 0x080c5fa2 | duel_action_label_test_es_0480_0481_0483_0485 | code_block |
| 0x080c5fa8 | duel_action_label_es_delta_0480_0481_0483_0485 | code_block |
| 0x080c5fb0 | ptr_ewram_base_080c5fb0 | literal |
| 0x080c5fb4 | gsettings_offset_080c5fb4 | literal |
| 0x080c5fb8 | ptr_game_str_ja_0485_080c5fb8 | literal |
| 0x080c5fbc | duel_action_label_es_ja_delta_0480_0481_0483_0485_080c5fbc | literal |
| 0x080c5fc0 | duel_action_label_surrender_it | code_block |
| 0x080c5fc4 | ptr_game_str_it_0485_080c5fc4 | literal |
| 0x080c5fc8 | duel_action_label_surrender_fr | code_block |
| 0x080c5fcc | ptr_game_str_fr_0485_080c5fcc | literal |
| 0x080c5fd0 | duel_action_label_surrender_de | code_block |
| 0x080c5fd4 | ptr_game_str_de_0485_080c5fd4 | literal |
| 0x080c5fd8 | duel_action_label_surrender_en | code_block |
| 0x080c5fdc | ptr_game_str_en_0485_080c5fdc | literal |
| 0x080c5fe0 | duel_action_label_ok_select_language | code_block |
| 0x080c6008 | ptr_ewram_base_080c6008 | literal |
| 0x080c600c | gsettings_offset_080c600c | literal |
| 0x080c6010 | ptr_game_str_ja_0960_080c6010 | literal |
| 0x080c6014 | duel_action_label_es_ja_delta_0960_080c6014 | literal |
| 0x080c6018 | duel_action_label_ok_it | code_block |
| 0x080c601c | ptr_game_str_it_0960_080c601c | literal |
| 0x080c6020 | duel_action_label_ok_fr | code_block |
| 0x080c6024 | ptr_game_str_fr_0960_080c6024 | literal |
| 0x080c6028 | duel_action_label_ok_de | code_block |
| 0x080c602c | ptr_game_str_de_0960_080c602c | literal |
| 0x080c6030 | duel_action_label_ok_en | code_block |
| 0x080c6034 | ptr_game_str_en_0960_080c6034 | literal |
| 0x080c6038 | duel_action_label_draw_select_language | code_block |
| 0x080c6056 | duel_action_label_test_es_0482_0484 | code_block |
| 0x080c6060 | ptr_ewram_base_080c6060 | literal |
| 0x080c6064 | gsettings_offset_080c6064 | literal |
| 0x080c6068 | ptr_game_str_ja_0484_080c6068 | literal |
| 0x080c606c | duel_action_label_es_ja_delta_0482_0484_080c606c | literal |
| 0x080c6070 | duel_action_label_draw_it | code_block |
| 0x080c6074 | ptr_game_str_it_0484_080c6074 | literal |
| 0x080c6078 | duel_action_label_draw_fr | code_block |
| 0x080c607c | ptr_game_str_fr_0484_080c607c | literal |
| 0x080c6080 | duel_action_label_draw_de | code_block |
| 0x080c6084 | ptr_game_str_de_0484_080c6084 | literal |
| 0x080c6088 | duel_action_label_draw_en | code_block |
| 0x080c60f4 | ptr_game_str_en_0484_080c60f4 | literal |
| 0x080c60f8 | ptr_ewram_base_080c60f8 | literal |
| 0x080c60fc | gsettings_offset_080c60fc | literal |
| 0x080c6100 | ptr_g_card_ctx_slot_data_080c6100 | literal |
| 0x080c6104 | ptr_obj_tile_vram_base_080c6104 | literal |
| 0x080c6108 | ptr_duel_action_menu_row_frame_left_tiles_080c6108 | literal |
| 0x080c6178 | ptr_duel_action_menu_row_frame_middle_tiles_080c6178 | literal |
| 0x080c617c | card_desc_render_param_080c617c | literal |
| 0x080c6180 | ptr_obj_tile_vram_base_080c6180 | literal |
| 0x080c621c | ptr_vija_intro_tile_vram_080c621c | literal |
| 0x080c6220 | ptr_duel_action_menu_oam_tiles_080c6220 | literal |
| 0x080c6224 | ptr_obj_palram_slot_4_080c6224 | literal |
| 0x080c6228 | ptr_duel_field_panel_obj_palette_080c6228 | literal |
| 0x080c622c | ptr_obj_palram_slot_5_080c622c | literal |
| 0x080c6230 | ptr_duel_field_shared_obj_palette_080c6230 | literal |
| 0x080c6234 | ptr_g_duel_field_state_080c6234 | literal |
| 0x080c6238 | duel_field_fadein_flag_off_080c6238 | literal |
| 0x080c623c | ptr_g_card_ctx_slot_data_080c623c | literal |
| 0x080c625c | ptr_g_card_ctx_slot_data_080c625c | literal |
| 0x080c62b0 | ptr_g_duel_field_state_080c62b0 | literal |
| 0x080c62b4 | duel_field_prng_anim_flag_off_080c62b4 | literal |
| 0x080c6360 | ptr_g_prng_080c6360 | literal |
| 0x080c6364 | ptr_g_card_ctx_slot_data_080c6364 | literal |
| 0x080c6398 | ptr_g_card_ctx_slot_data_080c6398 | literal |
| 0x080c639c | ptr_duel_action_menu_selection_case_table_080c639c | literal |
| 0x080c63a0 | duel_action_menu_selection_case_table | source_case_table |
| 0x080c63e0 | duel_action_menu_prepare_field_target | code_block |
| 0x080c63fc | ptr_g_card_ctx_slot_data_080c63fc | literal |
| 0x080c6400 | duel_action_menu_prepare_special_zone_target | code_block |
| 0x080c640e | duel_action_menu_commit_target_refs | code_block |
| 0x080c6418 | ptr_g_card_ctx_slot_data_080c6418 | literal |
| 0x080c641c | duel_action_menu_prepare_hand_target | code_block |
| 0x080c6448 | ptr_g_card_ctx_slot_data_080c6448 | literal |
| 0x080c644c | ptr_g_duel_field_state_080c644c | literal |
| 0x080c6450 | duel_action_menu_route_card_info | code_block |
| 0x080c6474 | ptr_g_card_ctx_slot_data_080c6474 | literal |
| 0x080c6478 | ptr_g_duel_zone_activation_state_080c6478 | literal |
| 0x080c64ac | ptr_g_card_ctx_slot_data_080c64ac | literal |
| 0x080c6530 | ptr_g_duel_field_state_080c6530 | literal |
| 0x080c6534 | ptr_g_card_ctx_slot_data_080c6534 | literal |
| 0x080c6568 | ptr_g_duel_disp_ctx_080c6568 | literal |
| 0x080c656c | ptr_g_vija_state_080c656c | literal |
| 0x080c6610 | ptr_g_prng_080c6610 | literal |
| 0x080c6614 | ptr_g_duel_field_state_080c6614 | literal |
| 0x080c6618 | duel_field_prng_anim_flag_off_080c6618 | literal |
| 0x080c661c | ptr_duel_action_menu_phase_handlers_080c661c | literal |
| 0x080c6620 | ptr_g_card_ctx_slot_data_080c6620 | literal |
| 0x080c6664 | ptr_switch_d_080c6662_switchdata_d_080c6668_080c6664 | literal |
| 0x080c66e4 | ptr_g_duel_field_state_080c66e4 | literal |
| 0x080c66e8 | duel_field_fadein_flag_off_080c66e8 | literal |
| 0x080c6700 | player_block_stride_080c6700 | literal |
| 0x080c6704 | ptr_g_duel_field_slots_080c6704 | literal |
| 0x080c6724 | player_block_stride_080c6724 | literal |
| 0x080c6728 | ptr_g_p1_field_array_c_base_080c6728 | literal |
| 0x080c672c | ptr_g_duel_field_state_080c672c | literal |
| 0x080c673c | player_block_stride_080c673c | literal |
| 0x080c6740 | ptr_g_p1_slot_set_code_array_080c6740 | literal |
| 0x080c6754 | player_block_stride_080c6754 | literal |
| 0x080c6758 | ptr_g_p1_hand_slot_array_080c6758 | literal |
| 0x080c675c | hand_array_to_count_neg_off_080c675c | literal |
| 0x080c6780 | player_block_stride_080c6780 | literal |
| 0x080c6784 | ptr_g_p1_alt_hand_slot_array_080c6784 | literal |
| 0x080c6788 | alt_hand_array_to_count_neg_off_080c6788 | literal |
| 0x080c67cc | ptr_g_duel_field_state_080c67cc | literal |
| 0x080c67d0 | ptr_g_p1_life_points_080c67d0 | literal |
| 0x080c67d4 | player_block_stride_080c67d4 | literal |
| 0x080c6838 | ptr_g_duel_card_ctx_base_080c6838 | literal |
| 0x080c683c | ptr_switch_d_080c6834_switchdata_d_080c6840_080c683c | literal |
| 0x080c6910 | zone_coord_x_neg24_u16_080c6910 | literal |
| 0x09850c5c | duel_field_shared_obj_palette | ROM_alias |
| 0x09852b9c | duel_action_menu_oam_tiles | ROM_alias |
| 0x0985329c | duel_field_panel_obj_palette | ROM_alias |
| 0x098532bc | duel_action_menu_row_frame_left_tiles | ROM_alias |
| 0x098532dc | duel_action_menu_row_frame_middle_tiles | ROM_alias |
| 0x09dbe2d0 | game_str_ja_0476 | string_reuse_GNU |
| 0x09dbe2da | game_str_ja_0477 | string_reuse_GNU |
| 0x09dbe2e4 | game_str_ja_0478 | string_reuse_GNU |
| 0x09dbe2ee | game_str_ja_0479 | string_reuse_GNU |
| 0x09dbe2f8 | game_str_ja_0480 | string_reuse_GNU |
| 0x09dbe300 | game_str_ja_0481 | string_reuse_GNU |
| 0x09dbe306 | game_str_ja_0482 | string_reuse_GNU |
| 0x09dbe310 | game_str_ja_0483 | string_reuse_GNU |
| 0x09dbe316 | game_str_ja_0484 | string_reuse_GNU |
| 0x09dbe31e | game_str_ja_0485 | string_reuse_GNU |
| 0x09dbe32a | game_str_ja_0487 | string_reuse_GNU |
| 0x09dbe34e | game_str_ja_0491 | string_reuse_GNU |
| 0x09dc05dc | game_str_ja_0960 | string_reuse_GNU |
| 0x09dc9380 | game_str_en_0476 | string_reuse_GNU |
| 0x09dc938a | game_str_en_0477 | string_reuse_GNU |
| 0x09dc9394 | game_str_en_0478 | string_reuse_GNU |
| 0x09dc939e | game_str_en_0479 | string_reuse_GNU |
| 0x09dc93aa | game_str_en_0480 | string_reuse_GNU |
| 0x09dc93ae | game_str_en_0481 | string_reuse_GNU |
| 0x09dc93b6 | game_str_en_0482 | string_reuse_GNU |
| 0x09dc93c0 | game_str_en_0483 | string_reuse_GNU |
| 0x09dc93c8 | game_str_en_0484 | string_reuse_GNU |
| 0x09dc93ce | game_str_en_0485 | string_reuse_GNU |
| 0x09dc93e0 | game_str_en_0487 | string_reuse_GNU |
| 0x09dc9402 | game_str_en_0491 | string_reuse_GNU |
| 0x09dcb280 | game_str_en_0960 | string_reuse_GNU |
| 0x09dd49ba | game_str_de_0476 | string_reuse_GNU |
| 0x09dd49c8 | game_str_de_0477 | string_reuse_GNU |
| 0x09dd49d6 | game_str_de_0478 | string_reuse_GNU |
| 0x09dd49e4 | game_str_de_0479 | string_reuse_GNU |
| 0x09dd49f2 | game_str_de_0480 | string_reuse_GNU |
| 0x09dd49fa | game_str_de_0481 | string_reuse_GNU |
| 0x09dd4a06 | game_str_de_0482 | string_reuse_GNU |
| 0x09dd4a12 | game_str_de_0483 | string_reuse_GNU |
| 0x09dd4a1c | game_str_de_0484 | string_reuse_GNU |
| 0x09dd4a24 | game_str_de_0485 | string_reuse_GNU |
| 0x09dd4a36 | game_str_de_0487 | string_reuse_GNU |
| 0x09dd4a5c | game_str_de_0491 | string_reuse_GNU |
| 0x09dd6c9e | game_str_de_0960 | string_reuse_GNU |
| 0x09de0c4a | game_str_fr_0476 | string_reuse_GNU |
| 0x09de0c56 | game_str_fr_0477 | string_reuse_GNU |
| 0x09de0c60 | game_str_fr_0478 | string_reuse_GNU |
| 0x09de0c6a | game_str_fr_0479 | string_reuse_GNU |
| 0x09de0c78 | game_str_fr_0480 | string_reuse_GNU |
| 0x09de0c80 | game_str_fr_0481 | string_reuse_GNU |
| 0x09de0c8a | game_str_fr_0482 | string_reuse_GNU |
| 0x09de0c92 | game_str_fr_0483 | string_reuse_GNU |
| 0x09de0c9c | game_str_fr_0484 | string_reuse_GNU |
| 0x09de0ca2 | game_str_fr_0485 | string_reuse_GNU |
| 0x09de0cb8 | game_str_fr_0487 | string_reuse_GNU |
| 0x09de0cf6 | game_str_fr_0491 | string_reuse_GNU |
| 0x09de3006 | game_str_fr_0960 | string_reuse_GNU |
| 0x09ded094 | game_str_it_0476 | string_reuse_GNU |
| 0x09ded0a2 | game_str_it_0477 | string_reuse_GNU |
| 0x09ded0ae | game_str_it_0478 | string_reuse_GNU |
| 0x09ded0ba | game_str_it_0479 | string_reuse_GNU |
| 0x09ded0c8 | game_str_it_0480 | string_reuse_GNU |
| 0x09ded0d4 | game_str_it_0481 | string_reuse_GNU |
| 0x09ded0e0 | game_str_it_0482 | string_reuse_GNU |
| 0x09ded0ec | game_str_it_0483 | string_reuse_GNU |
| 0x09ded0f4 | game_str_it_0484 | string_reuse_GNU |
| 0x09ded100 | game_str_it_0485 | string_reuse_GNU |
| 0x09ded10e | game_str_it_0487 | string_reuse_GNU |
| 0x09ded134 | game_str_it_0491 | string_reuse_GNU |
| 0x09def4d0 | game_str_it_0960 | string_reuse_GNU |
| 0x09e5ab84 | duel_action_menu_phase_handlers | ROM_phase_table |

### FUNC_RENAME / PLATE

9个更名均源自真实读写/调用表与旧名语义冲突, indegree与完整before ABI见上表和plates.tsv. 两个保留名函数6638/6800只更新PLATE. 所有PLATE/EOL纯ASCII, 每PLATE<=500字符.

#### 0x080c57c4 render_duel_action_menu_oam

```text
Render OAM for action-menu rows selected by ctx+4 bits 0..13. Decode the current packed field selection from field+0x210 and resolve its anchor coordinates. Use ctx+0x26 and row widths at +0xa to position and clip each row. Phase 1 uses the opening step; phases 3/5 use the closing step at ctx+0x2a. Emit row and highlight OAM entries. Inputs come from global state; callers ignore the return value.
```

#### 0x080c5b78 render_duel_action_menu_labels

```text
Render up to 14 action-menu labels selected by ctx+4. The even case table selects localized game-string rows from language bits 0..2 at EWRAM_BASE+GSETTINGS_OFFSET; language 5 adds a reviewed JA-to-ES delta. Measure each string, cache tile widths, copy left/middle/right frame columns to OBJ VRAM and render the text twice with glyph styles 0x8008/7. No APCS input.
```

#### 0x080c6184 init_duel_action_menu_vram

```text
Initialize action-menu graphics: copy 28 by 2 tiles from duel_action_menu_oam_tiles to VIJA_INTRO_TILE_VRAM, then 32 bytes each of panel/shared palettes to OBJ palette banks 4/5. Render localized labels. Update the ctx+8 selected-index nibble to an active ctx+4 bit, optionally advancing first according to field+0x21e bit 1. Return 1. Phase 0 handler; no player argument is read.
```

#### 0x080c6240 tick_duel_action_menu_open_step

```text
Opening action-menu step. Render menu OAM, increment the u8 animation step at ctx+0x2a, and return 1 if the updated byte exceeds 3; otherwise return 0. Phase 1 handler. Global state input; no APCS parameters. The state-machine driver resets the step when advancing phases.
```

#### 0x080c6268 tick_duel_action_menu_input_step

```text
Handle action-menu input after rendering its OAM. Decode player bit 7, zone bits 6:0 and index bits 14:8 from field+0x210. Field+0x222 bits 0xc complete this step. Navigation bits 0x20/0x10 scan previous/next active menu entries. Confirmation prepares target-slot refs with selection-1. Selection 0 instead sets phase 4; the driver increments it to 5 for close-and-card-info phases. Return 0 while active or 1 on completion.
```

#### 0x080c6490 tick_duel_action_menu_close_step

```text
Closing action-menu step used at phases 3 and 5. Render menu OAM, increment the u8 step at ctx+0x2a, and return 1 if the updated byte exceeds 3; otherwise return 0. The operation sequence matches the opening step with relocated operands; the renderer chooses closing geometry from the phase.
```

#### 0x080c64b8 run_duel_action_menu_card_info_transition

```text
Run the card-info transition for the selected zone record. Extract the card-info key, apply the zone 11 visible-index adjustment, and use ctx+0x29 substates to fade in, open/tick the card-info page, rebuild field VRAM and render the zone, then fade out. Return 0 while waiting and 1 when done. This is primary menu phase 6.
```

#### 0x080c65b0 tick_duel_action_menu_state_machine

```text
Tick action-menu phases via the 8-entry handler table. Normal path: 0 initialize, 1 open, 2 input, 3 close, 4 NULL. Card-view path writes phase 4 during input, then driver increment reaches 5 close, 6 card-info, 7 NULL. Nonzero handler results increment phase and clear ctx+0x29/+0x2a; NULL clears valid bit 0 and returns 1. Active handlers return 0. If (u32[gPrng+0x214]&0x7fffffff)/60>179, set field+0x222 bit 2 and clear bit 3.
```

#### 0x080c6638 resolve_zone_data_ptr_by_oam_word

```text
Resolve a card-record pointer from r0 low 16 packed selection: player bit 7, zone bits 6:0 and index bits 14:8. For zones 0..4, the packed chain-render mask can substitute index 0xff for get_zone_slot_ptr. Other cases address per-player field/hand arrays or fixed special-zone records. Return the selected pointer or 0 for unsupported cases. Reads global tables.
```

#### 0x080c678c repair_hand_zone_cursor_after_card_update

```text
Repair the packed hand-zone cursor in field+0x210 after a card update. Only zone 11 is handled. Read the u32 count at gP1LifePoints+0xc+player*PLAYER_BLOCK_STRIDE. Count 0 selects zone 0 for that player. For count 1..6, an empty selected low13-bit card ID moves the cursor to hand index count-1; larger counts remain unchanged. No APCS input; callers ignore the return value.
```

#### 0x080c6800 transform_zone_oam_coords_by_player

```text
Resolve packed zone coordinates from r0=player, r1=zone and r2=index. Compare player with gDuelCardCtxBase+4 XOR1 to choose mirrored anchor coordinates, then apply the 16-case zone layout and indexed spacing. Return (y<<16)|x with wrapped u16 coordinates. No external writes. Register r3 is scratch.
```

## carve计划 (R7)

`asm/rom.s:2080` 唯一incbin `[0x1e5ab84,0x1e5abfc)` 内前32B结构化. 后88B严格保持, 从0x1e5aba4继续, 原末端0x1e5abfc不变. 前方旧callback table/end/NULL不变.

```asm
.global duel_action_menu_phase_handlers
duel_action_menu_phase_handlers:
    .word init_duel_action_menu_vram+1
    .word tick_duel_action_menu_open_step+1
    .word tick_duel_action_menu_input_step+1
    .word tick_duel_action_menu_close_step+1
    .word 0
    .word tick_duel_action_menu_close_step+1
    .word run_duel_action_menu_card_info_transition+1
    .word 0
.incbin "roms/2343.gba", 0x1E5ABA4, 0x58
```

8项原值6185/6241/6269/6491/0/6491/64b9/0. 6个THUMB指针用批准后函数名+1, 6490重复两次, 2个NULL. selected0分支6450..6454写phase4, handler6470返回1, driver65fa..6600增到5; renderer57c4有phase3/5闭合分支, handler64b8处理phase6, phase7 NULL终止. 因此边界不是首NULL后的ab98. 下一aba4已被独立literal8754及86c2/86d4/86e0引用, 原生下一表身份/类型保持.

首cell现有/dword保持, 后7cell从原生NULL定义DWordDataType(/dword). 禁止PointerDataType/自动分析. 八项references_from原生全空并严格保持空. 只代码侧661c->base新增USER DATA operand0. 五个function+1节点原生primary/symbols/refsTo为空, 全量Std/Tiny中继续保持空, 不为源码可读性制造DEFAULT节点.

第一阶段20B/5项是历史边界推论, 已由冻结boundary-correction证据和fresh core-v5明确订正; 原12records字节保持.

## disasm计划 (R4)

Code/pool/padding范围全部取冻结CFG和395条原生detached decode. 以下69代码span均独立seed所有heads; 不按连续大块盲扫.

| Code start | Code end exclusive | Parent |
|--|--|--|
| 0x080c5c3c | 0x080c5c5c | 080c5b78 |
| 0x080c5c68 | 0x080c5c6c | 080c5b78 |
| 0x080c5c70 | 0x080c5c74 | 080c5b78 |
| 0x080c5c78 | 0x080c5c7c | 080c5b78 |
| 0x080c5c80 | 0x080c5c84 | 080c5b78 |
| 0x080c5c88 | 0x080c5ca8 | 080c5b78 |
| 0x080c5cb4 | 0x080c5cb8 | 080c5b78 |
| 0x080c5cbc | 0x080c5cc0 | 080c5b78 |
| 0x080c5cc4 | 0x080c5cc8 | 080c5b78 |
| 0x080c5ccc | 0x080c5cd0 | 080c5b78 |
| 0x080c5cd4 | 0x080c5cfe | 080c5b78 |
| 0x080c5d10 | 0x080c5d14 | 080c5b78 |
| 0x080c5d18 | 0x080c5d1c | 080c5b78 |
| 0x080c5d20 | 0x080c5d24 | 080c5b78 |
| 0x080c5d28 | 0x080c5d2c | 080c5b78 |
| 0x080c5d30 | 0x080c5d5a | 080c5b78 |
| 0x080c5d6c | 0x080c5d70 | 080c5b78 |
| 0x080c5d74 | 0x080c5d78 | 080c5b78 |
| 0x080c5d7c | 0x080c5d80 | 080c5b78 |
| 0x080c5d84 | 0x080c5d88 | 080c5b78 |
| 0x080c5d8c | 0x080c5dac | 080c5b78 |
| 0x080c5db8 | 0x080c5dbc | 080c5b78 |
| 0x080c5dc0 | 0x080c5dc4 | 080c5b78 |
| 0x080c5dc8 | 0x080c5dcc | 080c5b78 |
| 0x080c5dd0 | 0x080c5dd4 | 080c5b78 |
| 0x080c5dd8 | 0x080c5df8 | 080c5b78 |
| 0x080c5e04 | 0x080c5e08 | 080c5b78 |
| 0x080c5e0c | 0x080c5e10 | 080c5b78 |
| 0x080c5e14 | 0x080c5e18 | 080c5b78 |
| 0x080c5e1c | 0x080c5e20 | 080c5b78 |
| 0x080c5e24 | 0x080c5e4e | 080c5b78 |
| 0x080c5e60 | 0x080c5e64 | 080c5b78 |
| 0x080c5e68 | 0x080c5e6c | 080c5b78 |
| 0x080c5e70 | 0x080c5e74 | 080c5b78 |
| 0x080c5e78 | 0x080c5e7c | 080c5b78 |
| 0x080c5e80 | 0x080c5ea0 | 080c5b78 |
| 0x080c5eac | 0x080c5eb0 | 080c5b78 |
| 0x080c5eb4 | 0x080c5eb8 | 080c5b78 |
| 0x080c5ebc | 0x080c5ec0 | 080c5b78 |
| 0x080c5ec4 | 0x080c5ec8 | 080c5b78 |
| 0x080c5ecc | 0x080c5ef6 | 080c5b78 |
| 0x080c5f08 | 0x080c5f0c | 080c5b78 |
| 0x080c5f10 | 0x080c5f14 | 080c5b78 |
| 0x080c5f18 | 0x080c5f1c | 080c5b78 |
| 0x080c5f20 | 0x080c5f24 | 080c5b78 |
| 0x080c5f28 | 0x080c5f52 | 080c5b78 |
| 0x080c5f64 | 0x080c5f68 | 080c5b78 |
| 0x080c5f6c | 0x080c5f70 | 080c5b78 |
| 0x080c5f74 | 0x080c5f78 | 080c5b78 |
| 0x080c5f7c | 0x080c5f80 | 080c5b78 |
| 0x080c5f84 | 0x080c5fae | 080c5b78 |
| 0x080c5fc0 | 0x080c5fc4 | 080c5b78 |
| 0x080c5fc8 | 0x080c5fcc | 080c5b78 |
| 0x080c5fd0 | 0x080c5fd4 | 080c5b78 |
| 0x080c5fd8 | 0x080c5fdc | 080c5b78 |
| 0x080c5fe0 | 0x080c6008 | 080c5b78 |
| 0x080c6018 | 0x080c601c | 080c5b78 |
| 0x080c6020 | 0x080c6024 | 080c5b78 |
| 0x080c6028 | 0x080c602c | 080c5b78 |
| 0x080c6030 | 0x080c6034 | 080c5b78 |
| 0x080c6038 | 0x080c6060 | 080c5b78 |
| 0x080c6070 | 0x080c6074 | 080c5b78 |
| 0x080c6078 | 0x080c607c | 080c5b78 |
| 0x080c6080 | 0x080c6084 | 080c5b78 |
| 0x080c6088 | 0x080c608a | 080c5b78 |
| 0x080c63e0 | 0x080c63fa | 080c6268 |
| 0x080c6400 | 0x080c6416 | 080c6268 |
| 0x080c641c | 0x080c6446 | 080c6268 |
| 0x080c6450 | 0x080c6456 | 080c6268 |

调用DisassembleCommand(all395HeadSingletons, exact69CodeAddressSet794B, false), enableCodeAnalysis(false). 每条完整native length必须包含于codeSet; 只有794code字节TMode=1. 103pool用Undefined4DataType(/undefined4), word与对齐保持TMode0. 9对齐run保持undefined, 实际Exporter emit_undef_run输出9条`.zero 0x2`, 不新增dtype.

仅修改两父Function.body: 原AddressSet与各自新code字节求并后规范化相邻range. 5b78为1028B/67ranges, 6268为430B/8ranges. 6088与既有608a相接, 6450..6456与既有6456相接. 所有其它Function体/ABI/flags固定; Function create/delete/merge=0, FlowOverride=0.

自动引用240项严格来自prototype representationList内Address及RefTypeFactory: READ103, UNCONDITIONAL_JUMP73, CONDITIONAL_JUMP62, UNCONDITIONAL_CALL2. source=DEFAULT, 原生operand/primary字段完整. 不用字符串或opObjects推测, 不对computed case表添加flow. 新两个BL到096e14同步其完整incoming, 外部137Fns闭包全部保护.

## 新增constants / globals

| Name | Value | File |
|--|--|--|
| DUEL_ACTION_LABEL_ES_JA_DELTA_0960 | 0x0003aa7e | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0476_0477 | 0x0003aaa8 | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0478 | 0x0003aaac | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0479 | 0x0003aaae | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0480_0481_0483_0485 | 0x0003aab2 | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0482_0484 | 0x0003aab4 | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0487 | 0x0003aab8 | constants/duel_field.inc |
| DUEL_ACTION_LABEL_ES_JA_DELTA_0491 | 0x0003aac4 | constants/duel_field.inc |
| ZONE_COORD_X_NEG24_U16 | 0x0000ffe8 | constants/duel_field.inc |
| gDuelActionMenuAnimStep | 0x0201ff5a | constants/ewram.inc |
| duel_field_shared_obj_palette | 0x09850c5c | constants/rom_data.inc |
| duel_action_menu_oam_tiles | 0x09852b9c | constants/rom_data.inc |
| duel_field_panel_obj_palette | 0x0985329c | constants/rom_data.inc |
| duel_action_menu_row_frame_left_tiles | 0x098532bc | constants/rom_data.inc |
| duel_action_menu_row_frame_middle_tiles | 0x098532dc | constants/rom_data.inc |

两palette采用shared/panel语义, 因17库多个消费者共享. 菜单tile来源28x2 tiles, frame helper按src stride3 tiles与dest stride0x400复制left/middle/right列. RAM动画step保留真实/undefined1及NULL ROM值, 不填0.

## §5.1登记

None. 无引用60f4说法已由PC-relative6088消费者反证. 三raw全部有实证处理, 不以0绝对指针扫描替代所有引用分析.

## 消费者证据 (R6)

| Entry | Evidence | Confidence |
|--|--|--|
| 0x080c57c4 | asm/16_duelfield_zone.s:8861; reads packed field+0x210, not APCS r0/r1/r2 coordinates; PC5922..5b64 loops bits0..13 of gCardCtxSlotData+4 and emits OAM for selected rows; context+0x28 phase1 and3/5 branches alter per-row coordinates using+0x2a step; uses cached menu character width values at+0xa+2*index | high |
| 0x080c5b78 | asm/16_duelfield_zone.s:9376; loops14 selected bits, reads font_jp_base_table and gFontJpCtx; 69-spans CFG has14 even case words,13unique roots, language select via EWRAM_BASE+GSETTINGS_OFFSET andmask7; PC608a measures chosen string; PC613e/614a text render wrappers; PC6154 writes text rows into OBJ_TILE_VRAM_BASE+offset | high |
| 0x080c6184 | asm/16_duelfield_zone.s:9595; copies menu tiles/palettes, calls5b78, then advances ctx+8 selection nibble until ctx+4 mask has matching bit; phase table09e5ab84[0]=entry+1, handler returns1 | high |
| 0x080c6240 | asm/16_duelfield_zone.s:9691; calls57c4 and increments ctx+0x2a, returns1 if updated u8>3; phase table index1 and57c4 phase1 geometry bind opening step | high |
| 0x080c6268 | asm/16_duelfield_zone.s:9715; decodes field+0x210 as player bit7/zone7bits/index7bits, calls57c4; input bits atgPrng+0x148 select previous/next active menu bit; confirmed path raw6410/6440 calls096e14 with player,zone,index,selection-1; PC62a4 checksfield+0x222 bits0xc, completion/close path; selected0 raw6450 sets ctx+0x28=4 | high |
| 0x080c6490 | asm/16_duelfield_zone.s:9932; same34B operation sequence as6240 with relocated PC-relative operand bytes: render57c4, increment ctx+0x2a, returnupdated>3; phase table index3 and57c4 phase3 geometry bind closing step | high |
| 0x080c64b8 | asm/16_duelfield_zone.s:9956; resolves same packed card record twice to extract cached card-id fields, not pointer inequality; ctx+0x29 stages: fadein, open/tick card-info, rebuildfield, fadeout; calls open_card_info_page_from_list@655a and tick_card_info_page_by_state@6570 | high |
| 0x080c65b0 | asm/16_duelfield_zone.s:10084; (u32[gPrng+0x214]&0x7fffffff)/60>179 changesfield+0x222 flags; ctx+0x28 indexes09e5ab84 handler array through invoke_r0; nonzero handler result incrementsphase andzeros+0x29/+0x2a; NULL tableentry clearsctxbit0 andreturns1, activehandler returns0 | high |
| 0x080c6638 | asm/16_duelfield_zone.s:10157; inputr0 low16 is packedref; doesnotreadgPrng+0x210; decodesplayerbit7,zonebits6:0,indexbits14:8; zone0..4 chainmask maypass0xff snapshot index to get_zone_slot_ptr; otherzone branches choose fixed/per-player slot arrays | high |
| 0x080c678c | asm/16_duelfield_zone.s:10326; onlyzone11, reads32bitgP1LifePoints+0xc+player*0x868 count; count0 selectszone0; count1..6 with empty selected low13 cardID moves selection to last hand index count-1; count>6 unchanged | high |
| 0x080c6800 | asm/16_duelfield_zone.s:10388; r0=player,r1=zone,r2=index, not r2=x/r3=y; gDuelCardCtxBase+4 currentplayer^1 selects base coordinates; 16zone cases apply row/column spacing and return(y<<16)/x without external writes | high |

完整英文/日文/德法意西13label路径, ROM字节/原始Thumb子集实执行78条结果, 8个offset组, palette全消费者范围见绑定localization/firststage证据. native core全部before由Root getter实际采集, 不从ASM伪造Function.owner/NULL.

## 完整模型与来源合同

Root native-before-complete-v1 SHA256 6e1fbaf952604ff65efd9a418f4225fc6dabe589a4469fd69bfc4b43c57792c2. 唯一核心v5 SHA256 6aab066769000c66e19de104496544d5e87319841df2085d09216af60183ff53. 137Fn/7218slot rows/7295去重fullstates/1755word holders/578targets含5个真实even_function/43716module units/48外部unit. 保留所有holder字段和重复引用袋. properties完整header+20264rows, Tiny2441rows/46typedPointerEdges.

Expected只能由BEFORE+最小动作+原生detached事实构建, 不读取未来POST作为oracle. POST仅提供333个新USER ID, 必须为严格正int64/互异且不在全项目83960旧ID集合中(35925static+48035dynamic). 其它ID/type/source/namespace/dynamic字段完整保持. 本次没有原生DEFAULT+或未覆盖pointer自动显示投影, before-null保持null.

Global EQ2494->2503, bindings12766->12803. Tiny incoming211->532=原211+83新DATA+238自动; 其余56DATA+2auto由完整std/Fn保护. source actualAST242表达式235native+7fallback; 全132旧pins逐地址sourceCAS, 其中38纳入真实AST before/after, 其余94无本段依赖且不捏造原生DTO. 最终139pins.

源码scope: asm16主段与asm/rom.s32B carve, 外部仅asm01@0801ef10/asm15@080beec6/asm17@080cccc4,080ccd26四BL更名. 外部word AST变化0. gUI/palette共享函数080ce078/080cf7d4完整before保护. Registry11既有tuple精确同步name/plate, naming-proposals.csv9行只改name; temp函数清单9name加两body长度. 新GNU15. 原source212, runtime预期217=212+formal4+Script1, 无新data文件.

模型校验不等于落地成功. Review后由Root/fixer完成ownedFalse全回滚观测, 唯一保存, 独立原生后验, source49assets/export/build, 原ROM33554432B逐字节验证及单段提交.

## 求助

None. 所有候选语义置信度high; 等独立review裁决.

## Executor Report: F16-Seg-5

- Slots: EQ=37 REF_ADD=139 REF_PRESERVE=4 CASE_CORE=62 R7_TYPE_PRESERVE=1 R7_DEFINE=7.
- FUNC_RENAME=9 PLATE=11 USER_labels=333.
- carve=1(32B), disasm=69 code ranges(794B), pools=103(412B), zero=9(18B), §5.1=0.
- New GNU definitions=15, new Equates=9, total new bindings=37.
- Help: none.
- proposal: doc/dev/refine/F16-Seg-5.proposal.md

