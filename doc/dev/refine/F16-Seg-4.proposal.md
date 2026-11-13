# Refine Proposal: F16-Seg-4 [0x080c4350..0x080c57c4)

状态: FIRST PROPOSAL, 等待独立 reviewer. 本文不构成 Ghidra 写入、ROM 验证或提交成功声明.

## 段测绘

- 严格地址序: F16 已完成 Seg-1..3; 本段5236B, 下一段从0x080c57c4开始.
- 8个既有 Function, 139个既有 word, 61个源码自动数据名, 4个 ROM_INCBIN 共2128B.
- 原始区恢复64个4B literal 后, 本段全部 word=203. 1838B为884条 THUMB 指令; 34B为17个2B零对齐.
- 193个 USER label =120个 literal+4个 table+4个 RAM global+65个 code label. Code label 是块名, 不创建 Function.

| Entry | Before name | Actual body bytes | Incoming | Action |
|---|---|---:|---:|---|
| 0x080c4350 | dispatch_ui_effect_by_card_type | 56 | 1 | rename+PLATE+body |
| 0x080c4ca0 | clear_ui_effect_state_flags | 44 | 1 | PLATE |
| 0x080c4cd4 | check_lp_threshold_for_zone_slot | 40 | 7 | rename+PLATE |
| 0x080c4d04 | redraw_all_field_slot_tiles | 388 | 1 | PLATE |
| 0x080c4ea0 | init_field_slot_aob_ctx_c | 48 | 1 | rename+PLATE |
| 0x080c4edc | run_ui_effect_card_pair_state_machine | 1278 | 1 | PLATE |
| 0x080c5444 | setup_zone_oam_entry_by_field_slot | 318 | 1 | PLATE |
| 0x080c55dc | init_zone_oam_ctx_by_type | 364 | 1 | PLATE |

所有既有 body/prototype/parameters/return/storage/namespace/flags/incoming/bodyrefs 都在完整 before/after DTO 中. 只扩4350的 body56->1894B; 其余140个完整观测 Function的结构、ABI和flags保持原值. 本段8个均保留原 Function身份, create/delete/merge=0.

## 数据块分类 (Rule 2/3)

对全部1064个半字内部候选地址执行全33554432B ROM非对齐LE32 raw和THUMB|1扫描. 同时保留所有0命中和所有命中位置. 有效入口只采用实际四个 even computed-PC 表的消费者证据. 资产/代码字节中的巧合命中不升级为代码入口.

| Block | raw / THUMB occurrences over all internal candidates | Verified vector refs / roots | Decision | Code / literal / zero-align |
|---|---|---|---|---|
| 0x080c43a4 +272 | 4 / 0 | 1 / 1 | disasm + typed literal recovery | 240 / 32 / 0 B |
| 0x080c44dc +528 | 13 / 2 | 10 / 4 | disasm + typed literal recovery | 474 / 48 / 6 B |
| 0x080c472c +940 | 24 / 1 | 18 / 8 | disasm + typed literal recovery | 822 / 104 / 14 B |
| 0x080c4b1c +388 | 18 / 0 | 17 / 7 | disasm + typed literal recovery | 302 / 72 / 14 B |

四块有效入口共20个, 合46条真实表引用. 所有case指针为偶地址; mov pc,r0 不切换THUMB状态, 不添加+1. 本段无独立资产 carve, 无零引用 raw块送入5.1. 每个池和2B对齐的边界由CFG+原生884条精确length交叉证明.

## 符号化计划 (R1/R2/R3)

以下203行与 slots-draft-v1.tsv 逐地址相同. EQ_ADD27, REF_ADD80, REF_PRESERVE13, CASE_VECTOR_PRESERVE_CORE83. 对既有83个DATA/DEFAULT/operand0/primary引用保完整六字段及目标元数据; 只投影明确新USER目标显示.

### EQ_SLOTS

| Slot | ROM value | After GAS expression | After label | Consumer PCs |
|---|---|---|---|---|
| 0x080c4430 | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | duel_field_fadein_flag_off_080c4430 | 080c43b6 |
| 0x080c4438 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c4438 | 080c4416 |
| 0x080c44ac | 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | duel_field_fadein_flag_off_080c44ac | 080c444a |
| 0x080c44b0 | 0x00003fff | DUEL_CHAIN_RENDER_MASK_LOW14 | duel_chain_render_mask_low14_080c44b0 | 080c447c |
| 0x080c456c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c456c | 080c4520 |
| 0x080c4628 | 0xffffc03f | UI_SLOT_REF_SUBINDEX_CLEAR_MASK | ui_slot_ref_subindex_clear_mask_080c4628 | 080c4600 |
| 0x080c475c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c475c | 080c4746 |
| 0x080c4790 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c4790 | 080c4762 |
| 0x080c4798 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4798 | 080c4778 |
| 0x080c47bc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c47bc | 080c47a4 |
| 0x080c47e0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c47e0 | 080c47c8 |
| 0x080c4874 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4874 | 080c47f0 |
| 0x080c4b68 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4b68 | 080c4b4c |
| 0x080c4b90 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4b90 | 080c4b78 |
| 0x080c4bb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4bb8 | 080c4b9c |
| 0x080c4be4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4be4 | 080c4bc8 |
| 0x080c4c98 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c4c98 | 080c4c5a |
| 0x080c4cd0 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c4cd0 | 080c4cac |
| 0x080c4cf4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4cf4 | 080c4cde |
| 0x080c4e94 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c4e94 | 080c4e1e |
| 0x080c4ed8 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c4ed8 | 080c4ebe |
| 0x080c5440 | 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | duel_field_ui_effect_flags_off_080c5440 | 080c541c |
| 0x080c55d0 | 0x000070fb | OAM_ATTR2_TILE_FB_PAL7 | oam_attr2_tile_fb_pal7_080c55d0 | 080c557a |
| 0x080c55d4 | 0x000070fc | OAM_ATTR2_TILE_FC_PAL7 | oam_attr2_tile_fc_pal7_080c55d4 | 080c5596 |
| 0x080c55d8 | 0x000070fd | OAM_ATTR2_TILE_FD_PAL7 | oam_attr2_tile_fd_pal7_080c55d8 | 080c55b2 |
| 0x080c56d8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_080c56d8 | 080c5686 |
| 0x080c56e4 | 0x00001cd0 | FIELD_SLOT_OAM_FLAG1_GATE_OFF | field_slot_oam_flag1_gate_off_080c56e4 | 080c56a8 |

### REF_SLOTS - add DATA

| Slot | ROM value | After GAS expression | After label | Consumer PCs |
|---|---|---|---|---|
| 0x080c438c | 0x080c4390 | ui_card_render_phase_table | ptr_ui_card_render_phase_table_080c438c | 080c4380 |
| 0x080c4428 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4428 | 080c43aa,080c43d6 |
| 0x080c442c | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c442c | 080c43b4 |
| 0x080c4434 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4434 | 080c440a |
| 0x080c44a8 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c44a8 | 080c4448 |
| 0x080c4560 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4560 | 080c44de,080c450a,080c4516,080c454a |
| 0x080c4564 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4564 | 080c44f4 |
| 0x080c4568 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4568 | 080c4514 |
| 0x080c4570 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4570 | 080c4530 |
| 0x080c45cc | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c45cc | 080c4580 |
| 0x080c45d0 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c45d0 | 080c45a2 |
| 0x080c4684 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4684 | 080c4640 |
| 0x080c4688 | 0x0201fedc | gVijaIntroAobCtxA | ptr_g_vija_intro_aob_ctx_a_080c4688 | 080c465e |
| 0x080c46e4 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c46e4 | 080c4694 |
| 0x080c46e8 | 0x080c46ec | ui_card_render_phase1_zone_table | ptr_ui_card_render_phase1_zone_table_080c46e8 | 080c46dc |
| 0x080c4758 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4758 | 080c4742 |
| 0x080c478c | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c478c | 080c4760 |
| 0x080c4794 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4794 | 080c4774 |
| 0x080c47b8 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c47b8 | 080c47a0 |
| 0x080c47dc | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c47dc | 080c47c4 |
| 0x080c4870 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4870 | 080c47e4 |
| 0x080c4878 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4878 | 080c47fe |
| 0x080c487c | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c487c | 080c4854 |
| 0x080c4910 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4910 | 080c48a2 |
| 0x080c4914 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4914 | 080c48b6 |
| 0x080c4918 | 0x0201fedc | gVijaIntroAobCtxA | ptr_g_vija_intro_aob_ctx_a_080c4918 | 080c48e6 |
| 0x080c4990 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c4990 | 080c4952 |
| 0x080c4994 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4994 | 080c4976 |
| 0x080c49d0 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c49d0 | 080c49a6 |
| 0x080c49d4 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c49d4 | 080c49ac |
| 0x080c4a20 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4a20 | 080c4a04 |
| 0x080c4ac8 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4ac8 | 080c4a24,080c4a54,080c4a6c,080c4aa0 |
| 0x080c4acc | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4acc | 080c4a48 |
| 0x080c4ad0 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c4ad0 | 080c4a5c |
| 0x080c4ad4 | 0x098169b8 | card_stats_table | ptr_card_stats_table_080c4ad4 | 080c4a90 |
| 0x080c4b40 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4b40 | 080c4b3a |
| 0x080c4b64 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4b64 | 080c4b48 |
| 0x080c4b6c | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4b6c | 080c4b5c |
| 0x080c4b8c | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4b8c | 080c4b74 |
| 0x080c4bb4 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4bb4 | 080c4b98 |
| 0x080c4bbc | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4bbc | 080c4bac |
| 0x080c4be0 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4be0 | 080c4bc4 |
| 0x080c4be8 | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4be8 | 080c4bd8 |
| 0x080c4c3c | 0x0202311c | gUIEffectArg2 | ptr_g_ui_effect_arg2_080c4c3c | 080c4bec,080c4c0c,080c4c24 |
| 0x080c4c40 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4c40 | 080c4bf4 |
| 0x080c4c54 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4c54 | 080c4c48 |
| 0x080c4c94 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4c94 | 080c4c58 |
| 0x080c4c9c | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4c9c | 080c4c7e |
| 0x080c4ccc | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4ccc | 080c4caa |
| 0x080c4e8c | 0x0202334e | gDuelFieldChainRenderBitsPackedLo | ptr_g_duel_field_chain_render_bits_packed_lo_080c4e8c | 080c4d28,080c4d5a,080c4d82 |
| 0x080c4e90 | 0x02023350 | gDuelFieldChainRenderBitsPackedHi | ptr_g_duel_field_chain_render_bits_packed_hi_080c4e90 | 080c4d30,080c4d62,080c4d8a |
| 0x080c4e98 | 0x0201c4fc | gP1AltHandCountBase | ptr_g_p1_alt_hand_count_base_080c4e98 | 080c4e54 |
| 0x080c4e9c | 0x0202317c | gDuelZoneFirstVisibleSlotByPlayer | ptr_g_duel_zone_first_visible_slot_by_player_080c4e9c | 080c4e64 |
| 0x080c4ed4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4ed4 | 080c4ebc |
| 0x080c4f04 | 0x02023114 | gUIEffectArgs | ptr_g_ui_effect_args_080c4f04 | 080c4ee8 |
| 0x080c4f08 | 0x080c4f0c | switchD_080c4f02__switchdataD_080c4f0c | ptr_switch_d_080c4f02_switchdata_d_080c4f0c_080c4f08 | 080c4efc |
| 0x080c4ff4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c4ff4 | 080c4f34,080c4f74 |
| 0x080c4ff8 | 0x02023118 | gUIEffectArg1 | ptr_g_ui_effect_arg1_080c4ff8 | 080c4f60,080c4fd8 |
| 0x080c50fc | 0x02023118 | gUIEffectArg1 | ptr_g_ui_effect_arg1_080c50fc | 080c5014,080c5078,080c509c,080c50b4 |
| 0x080c5100 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c5100 | 080c5040,080c50a4 |
| 0x080c5190 | 0x02023118 | gUIEffectArg1 | ptr_g_ui_effect_arg1_080c5190 | 080c5154,080c516c |
| 0x080c5194 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c5194 | 080c515c |
| 0x080c5248 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c5248 | 080c5216 |
| 0x080c53f4 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c53f4 | 080c52ea,080c5396 |
| 0x080c53f8 | 0x02023118 | gUIEffectArg1 | ptr_g_ui_effect_arg1_080c53f8 | 080c533e,080c538e,080c53a6,080c53ca |
| 0x080c543c | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c543c | 080c541a |
| 0x080c54a4 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c54a4 | 080c5450 |
| 0x080c54a8 | 0x080c54ac | switchD_080c54a0__switchdataD_080c54ac | ptr_switch_d_080c54a0_switchdata_d_080c54ac_080c54a8 | 080c549a |
| 0x080c55cc | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c55cc | 080c54fc |
| 0x080c5630 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c5630 | 080c55e4 |
| 0x080c5634 | 0x0201ff30 | gCardCtxSlotData | ptr_g_card_ctx_slot_data_080c5634 | 080c560c |
| 0x080c5638 | 0x080c563c | switchD_080c562c__switchdataD_080c563c | ptr_switch_d_080c562c_switchdata_d_080c563c_080c5638 | 080c5626 |
| 0x080c56dc | 0x0201c510 | gDuelFieldSlots | ptr_g_duel_field_slots_080c56dc | 080c568c |
| 0x080c56e0 | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c56e0 | 080c569a |
| 0x080c56e8 | 0x0201ff30 | gCardCtxSlotData | ptr_g_card_ctx_slot_data_080c56e8 | 080c56b2 |
| 0x080c578c | 0x0201e2a0 | gDuelCardCtxBase | ptr_g_duel_card_ctx_base_080c578c | 080c5710 |
| 0x080c5794 | 0x0201ff30 | gCardCtxSlotData | ptr_g_card_ctx_slot_data_080c5794 | 080c577a,080c5730 |
| 0x080c5798 | 0x02023130 | gDuelFieldState | ptr_g_duel_field_state_080c5798 | 080c573a |
| 0x080c579c | 0x020230c0 | gDuelZoneActivationState | ptr_g_duel_zone_activation_state_080c579c | 080c5772 |
| 0x080c57c0 | 0x0201ff30 | gCardCtxSlotData | ptr_g_card_ctx_slot_data_080c57c0 | 080c57a2 |

### REF_SLOTS - preserve DATA

| Slot | ROM value | After GAS expression | After label | Consumer PCs |
|---|---|---|---|---|
| 0x080c4388 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4388 | 080c435c |
| 0x080c44b4 | 0x080c44b8 | ui_card_render_phase0_mode_table | ptr_ui_card_render_phase0_mode_table_080c44b4 | 080c44a0 |
| 0x080c4ad8 | 0x080c4adc | ui_card_render_phase3_zone_table | ptr_ui_card_render_phase3_zone_table_080c4ad8 | 080c4ac0 |
| 0x080c4cf0 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4cf0 | 080c4cd8 |
| 0x080c4e88 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c4e88 | 080c4d12 |
| 0x080c4ed0 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c4ed0 | 080c4ea6 |
| 0x080c50f8 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c50f8 | 080c5010 |
| 0x080c518c | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c518c | 080c5108 |
| 0x080c5244 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c5244 | 080c51c2 |
| 0x080c528c | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c528c | 080c5270 |
| 0x080c53f0 | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c53f0 | 080c52ce |
| 0x080c540c | 0x02023110 | gUIEffectState | ptr_g_ui_effect_state_080c540c | 080c5400 |
| 0x080c5790 | 0x0201c4e0 | gP1LifePoints | ptr_g_p1_life_points_080c5790 | 080c5722 |

### RENAME_SLOTS - case vector core preservation

| Slot | ROM value | After GAS expression | After label | Consumer PCs |
|---|---|---|---|---|
| 0x080c4390 | 0x080c43a4 | ui_card_render_phase0_prepare | ui_card_render_phase_table |  |
| 0x080c4394 | 0x080c462c | ui_card_render_phase1_draw_source | (preserve) |  |
| 0x080c4398 | 0x080c48a2 | ui_card_render_phase2_interpolate | (preserve) |  |
| 0x080c439c | 0x080c4a24 | ui_card_render_phase3_draw_destination | (preserve) |  |
| 0x080c43a0 | 0x080c4c58 | ui_card_render_phase4_finish | (preserve) |  |
| 0x080c44b8 | 0x080c44dc | ui_card_render_phase0_mode0 | ui_card_render_phase0_mode_table |  |
| 0x080c44bc | 0x080c4508 | ui_card_render_phase0_common_mode | (preserve) |  |
| 0x080c44c0 | 0x080c4508 | ui_card_render_phase0_common_mode | (preserve) |  |
| 0x080c44c4 | 0x080c4508 | ui_card_render_phase0_common_mode | (preserve) |  |
| 0x080c44c8 | 0x080c4508 | ui_card_render_phase0_common_mode | (preserve) |  |
| 0x080c44cc | 0x080c4574 | ui_card_render_phase0_modes5_7_8 | (preserve) |  |
| 0x080c44d0 | 0x080c4508 | ui_card_render_phase0_common_mode | (preserve) |  |
| 0x080c44d4 | 0x080c4574 | ui_card_render_phase0_modes5_7_8 | (preserve) |  |
| 0x080c44d8 | 0x080c4574 | ui_card_render_phase0_modes5_7_8 | (preserve) |  |
| 0x080c46ec | 0x080c472c | ui_card_render_phase1_default_zone | ui_card_render_phase1_zone_table |  |
| 0x080c46f0 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c46f4 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c46f8 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c46fc | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c4700 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c4704 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c4708 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c470c | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c4710 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c4714 | 0x080c472c | ui_card_render_phase1_default_zone | (preserve) |  |
| 0x080c4718 | 0x080c47e4 | ui_card_render_phase1_zone11 | (preserve) |  |
| 0x080c471c | 0x080c473e | ui_card_render_phase1_zone12 | (preserve) |  |
| 0x080c4720 | 0x080c4760 | ui_card_render_phase1_zone13 | (preserve) |  |
| 0x080c4724 | 0x080c479c | ui_card_render_phase1_zone14 | (preserve) |  |
| 0x080c4728 | 0x080c47c0 | ui_card_render_phase1_zone15 | (preserve) |  |
| 0x080c4adc | 0x080c4b1c | ui_card_render_phase3_default_zone | ui_card_render_phase3_zone_table |  |
| 0x080c4ae0 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4ae4 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4ae8 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4aec | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4af0 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4af4 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4af8 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4afc | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4b00 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4b04 | 0x080c4b1c | ui_card_render_phase3_default_zone | (preserve) |  |
| 0x080c4b08 | 0x080c4bec | ui_card_render_phase3_zone11 | (preserve) |  |
| 0x080c4b0c | 0x080c4b44 | ui_card_render_phase3_zone12 | (preserve) |  |
| 0x080c4b10 | 0x080c4b70 | ui_card_render_phase3_zone13 | (preserve) |  |
| 0x080c4b14 | 0x080c4b94 | ui_card_render_phase3_zone14 | (preserve) |  |
| 0x080c4b18 | 0x080c4bc0 | ui_card_render_phase3_zone15 | (preserve) |  |
| 0x080c4f0c | 0x080c4f20 | 0x080c4f20 | (preserve) |  |
| 0x080c4f10 | 0x080c4ffc | 0x080c4ffc | (preserve) |  |
| 0x080c4f14 | 0x080c5104 | 0x080c5104 | (preserve) |  |
| 0x080c4f18 | 0x080c5290 | 0x080c5290 | (preserve) |  |
| 0x080c4f1c | 0x080c53fc | 0x080c53fc | (preserve) |  |
| 0x080c54ac | 0x080c54ec | 0x080c54ec | (preserve) |  |
| 0x080c54b0 | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54b4 | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54b8 | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54bc | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54c0 | 0x080c54ec | 0x080c54ec | (preserve) |  |
| 0x080c54c4 | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54c8 | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54cc | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54d0 | 0x080c5512 | 0x080c5512 | (preserve) |  |
| 0x080c54d4 | 0x080c54ec | 0x080c54ec | (preserve) |  |
| 0x080c54d8 | 0x080c54fc | 0x080c54fc | (preserve) |  |
| 0x080c54dc | 0x080c54f4 | 0x080c54f4 | (preserve) |  |
| 0x080c54e0 | 0x080c54f4 | 0x080c54f4 | (preserve) |  |
| 0x080c54e4 | 0x080c54f4 | 0x080c54f4 | (preserve) |  |
| 0x080c54e8 | 0x080c54f4 | 0x080c54f4 | (preserve) |  |
| 0x080c563c | 0x080c567c | 0x080c567c | (preserve) |  |
| 0x080c5640 | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c5644 | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c5648 | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c564c | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c5650 | 0x080c567c | 0x080c567c | (preserve) |  |
| 0x080c5654 | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c5658 | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c565c | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c5660 | 0x080c576c | 0x080c576c | (preserve) |  |
| 0x080c5664 | 0x080c567c | 0x080c567c | (preserve) |  |
| 0x080c5668 | 0x080c5710 | 0x080c5710 | (preserve) |  |
| 0x080c566c | 0x080c56ec | 0x080c56ec | (preserve) |  |
| 0x080c5670 | 0x080c56ec | 0x080c56ec | (preserve) |  |
| 0x080c5674 | 0x080c56ec | 0x080c56ec | (preserve) |  |
| 0x080c5678 | 0x080c56ec | 0x080c56ec | (preserve) |  |

### FUNC_RENAME

| Entry | Before | After | Native indeg | Evidence |
|---|---|---|---:|---|
| 0x080c4350 | dispatch_ui_effect_by_card_type | run_ui_effect_card_render_state_machine | 1 | UIState.u16[0] self-increments through five phases; fields0x4/0x6 arecached-card/mode inputs; callerselectsUIflag0 |
| 0x080c4cd4 | check_lp_threshold_for_zone_slot | classify_player_hand_count_threshold | 7 | u16 readgP1LifePoints+0xc+player*0x868 isexisting gP1ZoneHandCount; empty/less/ge return0/1/2 |
| 0x080c4ea0 | init_field_slot_aob_ctx_c | init_ui_effect_card_pair_request | 1 | clear28B/store2args/setUIbit1+fieldbit2; caller1f0a4 selects pair machine4edc withbit1; noAOB initializer |

4350由play_ui_effect@1f0c6的UI flag0路径调用, UI+0自增0..4是phase, UI+6才是mode. 4cd4读的是gP1LifePoints+0xc的手牌计数, 非LP; 七条调用均为native owner6b04. 4ea0零28字节并写UI+4/+8, 设置flag1供pair state machine, 无AOB初始化. 名称因此按实际数据流订正.

### PLATE - full ASCII rewrite

8个本段PLATE+1个必要直接消费者context6b04. 6b04原文误称LP并引用旧threshold名, 与本段订正构成同一调用语义闭包; 不修改其任何指令/槽/body. 每项完整before/after Function在plates-draft-v1.tsv.

- 0x080c4350, 468 ASCII chars
```text
Run the single-card UI render request selected by UI flag0. Cache the card at UI+4; UI+6 is mode. Phase0 prepares masks, images and AOB graphics; phase1 draws the source; phase2 advances AOB or five interpolation steps; phase3 draws the destination; phase4 refreshes the field and advances. Active phases return1. Out-of-range phase calls the shared frame cleanup and returns0. Packed refs are UI+8 and UI+0xc. BL at437a and4424 exits through the original saved frame.
```

- 0x080c4ca0, 439 ASCII chars
```text
Shared-frame cleanup for run_ui_effect_card_render_state_machine. With r4=UI state, clear UI+0x19 bit0 and field+0x215 bit2. Entry4ca0 sets r0=2 for the mask;4cba sets return0;4cbc releases12 local bytes, restores r8-r10 and r4-r7, then returns through the saved caller PC. This tail consumes the parent frame rather than the BL link register. Keep the existing Function body and flags; local CALL_RETURN is set at the two parent BL sites.
```

- 0x080c4cd4, 315 ASCII chars
```text
Classify the player hand count against a threshold. r0 bit0 selects player; r1 low16 is threshold. Read u16 at gP1LifePoints+0xc+player*PLAYER_BLOCK_STRIDE, the hand-count field. Return0 for zero count,1 for nonzero count below threshold,2 otherwise. Read-only; seven calls from decode_zone_oam_word_to_slot_fields.
```

- 0x080c4d04, 421 ASCII chars
```text
Redraw both players field tiles. For slots0..4, combine (u16[gDuelFieldChainRenderBitsPackedLo]>>2) with (u8[gDuelFieldChainRenderBitsPackedHi]&3)<<14; bit(player*8+slot) selects the0xff chain-snapshot getter mode. Draw slots5..10 normally, then zones12..15 from per-player counts. Cache card IDs and pass card, face and field6 data to the tile renderers. Refresh each player list using gDuelZoneFirstVisibleSlotByPlayer.
```

- 0x080c4ea0, 348 ASCII chars
```text
Initialize a paired-card UI render request. Save r0/r1, zero28 bytes of gUIEffectState, then write the two packed arguments at UI+4 and UI+8. Set UI+0x19 bit1 and field+0x215 bit2. The UI dispatcher selects run_ui_effect_card_pair_state_machine while bit1 is set. The zero helper takes a byte count; this initializer does not create an AOB context.
```

- 0x080c4edc, 423 ASCII chars
```text
Run the paired-card UI request selected by UI flag1. UI+0 is phase0..4; UI+4 and UI+8 hold packed player/zone/index references. Phase0 resolves coordinates, loads two small images and builds masks. Later phases draw paired sprites/backgrounds, advance interpolation and refresh field tiles. Active phases return1. Default clears UI+0x19 bit1 and field+0x215 bit2, returning0. The entry does not require an r1 flag argument.
```

- 0x080c5444, 373 ASCII chars
```text
Set up zone OAM from u16[gDuelFieldState+0x210]. Decode player bit7, zone bits6:0 and index bits14:8, transform coordinates, then dispatch over16 zone cases. Emit up to three entries with write_oam_entry_from_packed_args. Values0x70fb/0x70fc/0x70fd are attr2: tile0xfb/0xfc/0xfd and palette bank7, with priority0. They are written at OAM entry+4, not used as entry indices.
```

- 0x080c55dc, 439 ASCII chars
```text
Initialize the zone OAM context at gCardCtxSlotData. Zero44 bytes, set header valid bit0 and decode u16[field+0x210] into player/zone/index. Zone cases set conditional flag1 from record availability, current player, record+8 and gDuelFieldSlots+0x1cd0. Activation checks update context data. Flagged zone11 clears activation+0x30/+0x34, stores context+0x28=4 and invokes sync_state_and_init_sprite with code24. The zero helper takes bytes.
```

- 0x080c6b04, 424 ASCII chars
```text
Decode a packed zone descriptor: player bit7, zone bits6:0 and sub-index bits31:24. Save r1 as secondary control and use gDuelCardCtxBase+4 for the player-flip flag. Dispatch over16 zone cases to compute slot fields. Seven branches call classify_player_hand_count_threshold with zone-specific thresholds. Other branches read the corresponding slot records and flags. Keep the existing Function body, ABI and return behavior.
```

### USER code labels

43个内部flow目标均显式USER, 另20个case root+2个shared tail. 所有名称只描述该块直接指令操作; 真实函数归属保留.

| Address | Label | Evidence |
|---|---|---|
| 0x080c43a4 | ui_card_render_phase0_prepare | native detached instruction+CFG block at same address |
| 0x080c443c | ui_card_render_check_source_ref | native detached instruction+CFG block at same address |
| 0x080c4498 | ui_card_render_check_mode_limit | native detached instruction+CFG block at same address |
| 0x080c449e | ui_card_render_dispatch_mode | native detached instruction+CFG block at same address |
| 0x080c44dc | ui_card_render_phase0_mode0 | native detached instruction+CFG block at same address |
| 0x080c4508 | ui_card_render_phase0_common_mode | native detached instruction+CFG block at same address |
| 0x080c454a | ui_card_render_prepare_small_image | native detached instruction+CFG block at same address |
| 0x080c4574 | ui_card_render_phase0_modes5_7_8 | native detached instruction+CFG block at same address |
| 0x080c45a2 | ui_card_render_limit_destination_index | native detached instruction+CFG block at same address |
| 0x080c45d4 | ui_card_render_clamp_index_six | native detached instruction+CFG block at same address |
| 0x080c45e4 | ui_card_render_clamp_index_zero | native detached instruction+CFG block at same address |
| 0x080c45fa | ui_card_render_store_destination_index | native detached instruction+CFG block at same address |
| 0x080c462c | ui_card_render_phase1_draw_source | native detached instruction+CFG block at same address |
| 0x080c467e | ui_card_render_return_active | native detached instruction+CFG block at same address |
| 0x080c468c | ui_card_render_unpack_source_player | native detached instruction+CFG block at same address |
| 0x080c46a2 | ui_card_render_apply_source_flag15 | native detached instruction+CFG block at same address |
| 0x080c46b0 | ui_card_render_emit_source_sprite | native detached instruction+CFG block at same address |
| 0x080c46ca | ui_card_render_select_source_zone | native detached instruction+CFG block at same address |
| 0x080c46da | ui_card_render_dispatch_source_zone | native detached instruction+CFG block at same address |
| 0x080c472c | ui_card_render_phase1_default_zone | native detached instruction+CFG block at same address |
| 0x080c473e | ui_card_render_phase1_zone12 | native detached instruction+CFG block at same address |
| 0x080c4760 | ui_card_render_phase1_zone13 | native detached instruction+CFG block at same address |
| 0x080c479c | ui_card_render_phase1_zone14 | native detached instruction+CFG block at same address |
| 0x080c47c0 | ui_card_render_phase1_zone15 | native detached instruction+CFG block at same address |
| 0x080c47e4 | ui_card_render_phase1_zone11 | native detached instruction+CFG block at same address |
| 0x080c4838 | ui_card_render_refresh_source_list | native detached instruction+CFG block at same address |
| 0x080c4854 | ui_card_render_select_source_feedback | native detached instruction+CFG block at same address |
| 0x080c4880 | ui_card_render_check_feedback_modes | native detached instruction+CFG block at same address |
| 0x080c488a | ui_card_render_emit_feedback_six | native detached instruction+CFG block at same address |
| 0x080c4892 | ui_card_render_emit_feedback_five | native detached instruction+CFG block at same address |
| 0x080c489a | ui_card_render_emit_feedback_four | native detached instruction+CFG block at same address |
| 0x080c48a2 | ui_card_render_phase2_interpolate | native detached instruction+CFG block at same address |
| 0x080c4906 | ui_card_render_advance_after_aob | native detached instruction+CFG block at same address |
| 0x080c491c | ui_card_render_interpolate_delta | native detached instruction+CFG block at same address |
| 0x080c492e | ui_card_render_divide_x_delta | native detached instruction+CFG block at same address |
| 0x080c4942 | ui_card_render_divide_y_delta | native detached instruction+CFG block at same address |
| 0x080c4960 | ui_card_render_read_source_flag15 | native detached instruction+CFG block at same address |
| 0x080c4974 | ui_card_render_compare_destination_flag15 | native detached instruction+CFG block at same address |
| 0x080c4998 | ui_card_render_subtract_step8 | native detached instruction+CFG block at same address |
| 0x080c499c | ui_card_render_compare_player_bits | native detached instruction+CFG block at same address |
| 0x080c49ba | ui_card_render_select_step_half | native detached instruction+CFG block at same address |
| 0x080c49d8 | ui_card_render_scale_early_step | native detached instruction+CFG block at same address |
| 0x080c49de | ui_card_render_emit_interpolated_sprite | native detached instruction+CFG block at same address |
| 0x080c4a16 | ui_card_render_advance_interpolation | native detached instruction+CFG block at same address |
| 0x080c4a24 | ui_card_render_phase3_draw_destination | native detached instruction+CFG block at same address |
| 0x080c4a6a | ui_card_render_read_destination_flag15 | native detached instruction+CFG block at same address |
| 0x080c4a78 | ui_card_render_emit_destination_sprite | native detached instruction+CFG block at same address |
| 0x080c4a90 | ui_card_render_check_card_stats_type | native detached instruction+CFG block at same address |
| 0x080c4ab4 | ui_card_render_select_destination_zone | native detached instruction+CFG block at same address |
| 0x080c4abe | ui_card_render_dispatch_destination_zone | native detached instruction+CFG block at same address |
| 0x080c4b1c | ui_card_render_phase3_default_zone | native detached instruction+CFG block at same address |
| 0x080c4b44 | ui_card_render_phase3_zone12 | native detached instruction+CFG block at same address |
| 0x080c4b70 | ui_card_render_phase3_zone13 | native detached instruction+CFG block at same address |
| 0x080c4b94 | ui_card_render_phase3_zone14 | native detached instruction+CFG block at same address |
| 0x080c4bc0 | ui_card_render_phase3_zone15 | native detached instruction+CFG block at same address |
| 0x080c4bec | ui_card_render_phase3_zone11 | native detached instruction+CFG block at same address |
| 0x080c4c0c | ui_card_render_refresh_destination_list | native detached instruction+CFG block at same address |
| 0x080c4c24 | ui_card_render_load_destination_ref | native detached instruction+CFG block at same address |
| 0x080c4c28 | ui_card_render_update_destination_oam | native detached instruction+CFG block at same address |
| 0x080c4c44 | ui_card_render_refresh_zone_info | native detached instruction+CFG block at same address |
| 0x080c4c48 | ui_card_render_advance_phase | native detached instruction+CFG block at same address |
| 0x080c4c58 | ui_card_render_phase4_finish | native detached instruction+CFG block at same address |
| 0x080c4c76 | ui_card_render_rebuild_field_caches | native detached instruction+CFG block at same address |
| 0x080c4cba | ui_card_render_return_complete | native detached instruction+CFG block at same address |
| 0x080c4cbc | ui_card_render_restore_saved_frame | native detached instruction+CFG block at same address |

## carve 计划 (R7)

独立数据carve=0. 不改asm/rom.s; 四块全部由本模块内THUMB代码、64个undefined4 literal与17条.zero 0x2替换.

## disasm 计划 (R4)

仅下列25个half-open代码span的1838B设TMode=1. 64个literal及34B零对齐保持TMode=0. 全部884个head为原生Listing NULL, 段内无数据结构覆盖这些字节.

- 0x080c43a4 code: [0x080c43a4,0x080c4428), [0x080c443c,0x080c44a8)
  literal: [0x080c4428,0x080c443c), [0x080c44a8,0x080c44b4)
  zero-align: none
- 0x080c44dc code: [0x080c44dc,0x080c4560), [0x080c4574,0x080c45ca), [0x080c45d4,0x080c4626), [0x080c462c,0x080c4682), [0x080c468c,0x080c46e4)
  literal: [0x080c4560,0x080c4574), [0x080c45cc,0x080c45d4), [0x080c4628,0x080c462c), [0x080c4684,0x080c468c), [0x080c46e4,0x080c46ec)
  zero-align: [0x080c45ca,0x080c45cc), [0x080c4626,0x080c4628), [0x080c4682,0x080c4684)
- 0x080c472c code: [0x080c472c,0x080c4758), [0x080c4760,0x080c478a), [0x080c479c,0x080c47b6), [0x080c47c0,0x080c47da), [0x080c47e4,0x080c486e), [0x080c4880,0x080c4910), [0x080c491c,0x080c498e), [0x080c4998,0x080c49ce), [0x080c49d8,0x080c4a1e), [0x080c4a24,0x080c4ac8)
  literal: [0x080c4758,0x080c4760), [0x080c478c,0x080c479c), [0x080c47b8,0x080c47c0), [0x080c47dc,0x080c47e4), [0x080c4870,0x080c4880), [0x080c4910,0x080c491c), [0x080c4990,0x080c4998), [0x080c49d0,0x080c49d8), [0x080c4a20,0x080c4a24), [0x080c4ac8,0x080c4ad8)
  zero-align: [0x080c478a,0x080c478c), [0x080c47b6,0x080c47b8), [0x080c47da,0x080c47dc), [0x080c486e,0x080c4870), [0x080c498e,0x080c4990), [0x080c49ce,0x080c49d0), [0x080c4a1e,0x080c4a20)
- 0x080c4b1c code: [0x080c4b1c,0x080c4b40), [0x080c4b44,0x080c4b62), [0x080c4b70,0x080c4b8a), [0x080c4b94,0x080c4bb2), [0x080c4bc0,0x080c4bde), [0x080c4bec,0x080c4c3a), [0x080c4c44,0x080c4c52), [0x080c4c58,0x080c4c92)
  literal: [0x080c4b40,0x080c4b44), [0x080c4b64,0x080c4b70), [0x080c4b8c,0x080c4b94), [0x080c4bb4,0x080c4bc0), [0x080c4be0,0x080c4bec), [0x080c4c3c,0x080c4c44), [0x080c4c54,0x080c4c58), [0x080c4c94,0x080c4ca0)
  zero-align: [0x080c4b62,0x080c4b64), [0x080c4b8a,0x080c4b8c), [0x080c4bb2,0x080c4bb4), [0x080c4bde,0x080c4be0), [0x080c4c3a,0x080c4c3c), [0x080c4c52,0x080c4c54), [0x080c4c92,0x080c4c94)

Driver API: DisassembleCommand(all884HeadSingletons, exact25CodeAddressSet1838B, false); enableCodeAnalysis(false); applyTo(program, monitor). restrictedSet只检查起始PC, 落地守卫必须逐条核完整native length包含在codeSet中. followFlow=false阻止callee no_return/callFixup或外段follow引入额外改动.

然后只对437a和4424设置CALL_RETURN. Detached native projection证明instruction.flow_type=CALL_TERMINATOR, fallthrough=null; direct BL ref依RefTypeFactory仍为UNCONDITIONAL_CALL, source DEFAULT. 不把instruction flow_type复制到ref.type. 不从computed-PC派发补造20条jump flow.

parent4350.setBody(old[4350,4388) UNION raw1838codebytes), 合1894B/26ranges. 不并入4ca0既有44B body或4cba/4cbc共享tail, 不改其no_return/inline/thunk. 437a去cleanup, 4424去4cba, 两条BL均消费4350原始saved frame而非返回BL后的地址. 4428是literal而非fallthrough.

64个新literal逐项定义undefined4, 不把它们设Pointer. 17个2B全零alignment保原undefined数据状态和TMode0; 实际ExportRangeToGas.emit_undef_run已对ROM原字节运行, 恰输出17条.zero 0x2, 不残留ROM_INCBIN/.byte.

新指令自动refs185=75READ+41CONDITIONAL_JUMP+35UNCONDITIONAL_CALL+34UNCONDITIONAL_JUMP, source全部DEFAULT. 取真实prototype.getOpRepresentationList的Address及RefTypeFactory事实, 不是opObjects/文本猜测. 所有flow Address均被operand消费, 无需MNEMONIC=-1新ref.

## 新增 constants / 全局

先扫描所有现有GNU ABS与Ghidra2488个equate. 重用DUEL_FIELD_UI_EFFECT_FLAGS_OFF=0x215, DUEL_FIELD_FADEIN_FLAG_OFF=0x21e, PLAYER_BLOCK_STRIDE=0x868; 三者GNU/Ghidra皆存在, 全部复用constants/ewram.inc:693/236/251. 新增6个不同语义常量及4个RAM标签, GNU共10. 4个ROM表与65个code标签在asm16内定义, 不重复.equ.

| Value | Name | GNU status | Native Equate status |
|---|---|---|---|
| 0x00000215 | DUEL_FIELD_UI_EFFECT_FLAGS_OFF | reuse | reuse |
| 0x0000021e | DUEL_FIELD_FADEIN_FLAG_OFF | reuse | reuse |
| 0x00000868 | PLAYER_BLOCK_STRIDE | reuse | reuse |
| 0x00003fff | DUEL_CHAIN_RENDER_MASK_LOW14 | new | new |
| 0xffffc03f | UI_SLOT_REF_SUBINDEX_CLEAR_MASK | new | new |
| 0x00001cd0 | FIELD_SLOT_OAM_FLAG1_GATE_OFF | new | new |
| 0x000070fb | OAM_ATTR2_TILE_FB_PAL7 | new | new |
| 0x000070fc | OAM_ATTR2_TILE_FC_PAL7 | new | new |
| 0x000070fd | OAM_ATTR2_TILE_FD_PAL7 | new | new |
| 0x02023118 | gUIEffectArg1 | new ewram.inc | USER label, preserve actual dtype |
| 0x0202311c | gUIEffectArg2 | new ewram.inc | USER label, preserve actual dtype |
| 0x0202334e | gDuelFieldChainRenderBitsPackedLo | new ewram.inc | USER label, preserve actual dtype |
| 0x02023350 | gDuelFieldChainRenderBitsPackedHi | new ewram.inc | USER label, preserve actual dtype |

0x3fff既存card-ID/DISPCNT常量与本链渲染mask域不同; 0xffffc03f既存PRNG常量与本packed slot-ref域不同, 故不复用误域名字. 0x1cd0是gDuelFieldSlots的flag1 gate偏移. 0x70fb/fc/fd是实际OAM attr2值: palette7/tileFB..FD/priority0.

## 5.1 登记 (Rule 3)

本段0项. 有引用四raw均按R4完整处理, 不送入零引用登记.

## 消费者证据 (R6)

| Scope | Evidence | Confidence |
|---|---|---|
| single/pair request | asm/01_vija_scene_text.s:4846, PCs1f0a4..1f0c6; asm16:6247, phase0raw43a4 and4ea0 initializer | high |
| threshold counter | asm/16_duelfield_zone.s:6369; gP1LifePoints+0xc; constants/ewram.inc:232 gP1ZoneHandCount; 7native calls owner6b04 | high |
| chain snapshot mask | asm/16_duelfield_zone.s:6399; asm/03_equip_chain_hand.s:11981-12027 and12194-12234; sub-index255 chooses gDuelEffectChainSlots snapshot | high |
| OAM attr2 | asm/16_duelfield_zone.s:7334; asm/21_font_title_scene.s:4911 strh r2,[entry+4] at080f61be | high |
| zero helper byte units | asm/21_font_title_scene.s:1934 zero_fill_by_halfword; asm16:6600/7533 r1=0x1c/0x2c, actual clear28/44B | high |
| card_stats_table | raw literal080c4ad4->098169b8, actual existing USER card_stats_table; consumer4a90 index*22 reads record+16 compares9 | high |
| packed chain globals | redraw4d04 shiftsLo16>>2 andHi8&3<<14; producer validates nativeRAMdtype Lo undefined2/Hi undefined4 and preserves null bytes | high |
| code labels | asm/16_duelfield_zone.s raw blocks lines6286/6299/6317/6337 plus exact raw offset; native884 instruction texts and CFG block address, label operation documented inline | high |

精确line/PC/value/consumer集合以203个slot records为准; 原始块内代码没有旧源码行, 用原ROM块行+字节偏移及原生instruction PC标识, 不伪造现有汇编行.

## 完整模型与原生显示派生闭包

- Final BEFORE: native-before-complete-v1绑定25records; canonical v5 SHA a09a962479de938b7d49c8c38e530c628b950aa81101f9a81e6d511cf23e8471.
- 141Fn, 4440slots, 1644words, 508target records, 去重4876fullstates; 22359指令属性含884真实NULL; 43716moduleunits与48external保持. 全原生query holder形状另建完整before/after计划, 包含targets[].even_function.
- Tiny2618rows/2190seeds/60typedPointerEdges; before270incoming -> after443, 分区22新增DATA+151自动ref在Tiny, 58DATA+34auto在标准/Function完整图.
- 只有23119与23352两个DEFAULT offcut显示名变化, 保ID/source/type/namespace/dynamic/dtype/bytes, 对应3+28个实际refs仅target_primary_name改变.
- 60typedPointerEdges逐条保护. 已被193USER接管的sources按动作更新; 其余DEFAULT候选无primary, 不创建PTR显示名; ANALYSIS switch source身份/namespace保持.
- 全局Equate2488/12739bindings ->2494/12766. 引用采用严格带类型、完整字段、重复数量保留的无序袋.
- 所有未知native after字段均从真实before保留或由最小动作独立派生. 实际POST只准绑定193个新USER ID; 不可拿POST字段填expected.

## GNU / source / registry 同步合同

真实导出器AST: 对1644个after及1580个defined-before word分别执行symbol/equate解析, 各3224次. 本段203=200native+3地址pin(4f08/54a8/5638保ANALYSIS switch表GAS显示); 继承129->132pins. 193labels/884新指令的LDR/branch operand及17个zero-run也实际调用导出器AST核对.

源码精确scope: asm01两处BL@1edca/1f0c6, asm16本段和context6b04. 15/17的ANALYSIS rich-ref显示变化不导致真实导出器word/指令文本变化, 不授权这些文件修改. registry精确9个既有tuple; naming CSV仅3个name单元; temp inventory额外4350 length56->1894, 其余列保持. 运行snapshot=原207+本段formal4+Script1=212files.

## 求助

none. 无未决低置信度语义. R4 Driver方案和命名仍待正式独立review, 本executor不执行写入/构建/提交.

## Executor Report: F16-Seg-4

- EQ=27, REF_ADD=80, REF_PRESERVE=13, CASE_PRESERVE=83, FUNC_RENAME=3, PLATE=9, USER labels=193.
- carve=0, disasm=25ranges/884instructions/1838B, newdata64words, zeroalign17x2B, 5.1=0.
- constants/global new=6EQ+4RAM. 求助=none.
- proposal: doc/dev/refine/F16-Seg-4.proposal.md

