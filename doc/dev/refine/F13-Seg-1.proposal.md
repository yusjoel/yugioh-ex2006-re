# Refine Proposal: F13-Seg-1 [0x0809d718..0x0809e6f4)

本提案仅覆盖模块13的第1段, 按地址序处理. 活动路线图见 `doc/dev/p5-refine-13-equip-placement.md` 第五节. 规则采用 `doc/dev/methodology/refine-loop.md` 的R1-R9和 `.codex/agents/refine-executor.toml`. executor只做分析和静态自检, 不评分, 不写Ghidra, 不build, 不stage/commit. 后续须经过独立reviewer和fixer.

## 段测绘

- 当前源文件: `asm/13_equip_placement.s`, SHA256 `e473bd1db9d96114f78e5ea8cde07ee83c9003d7a4f6e920ad25887196190671`.
- 半开范围 `[0x0809d718,0x0809e6f4)`, 4060 B. 15个已有Function对象, 无新增独立入口. 真实body/ranges与入口inventory和push观测已交叉核对, 不将CSV length当作连续区间.
- 142个4B自动槽(DAT=110, PTR=32, DWORD=0, UNK=0), 共568 B; 另有52个已结构化switch word, 共208 B. 1751个连续单元完整覆盖: 1486条普通导出指令, 39条已定义Thumb指令的`.hword`表示, 194个word, 32处`.zero 2`对齐. `.hword`不是裸数据.
- 段内ROM_INCBIN=0, `.byte`=0, UNK槽=0. DAT/DWORD/PTR均在下表和机器plan中逐槽覆盖. 0x0809e6f4是下一函数入口, 不进入该函数.
- 两处既有局部共享收尾: 0x0809e066属于0x0809d984并恢复0x120字节栈帧及高寄存器; 0x0809e5da属于0x0809e168. 保留原局部标签和所有跳转, 无新增Function/收尾PLATE.

| 入口 | 当前正式名 | 源行 | Function ID | body字节 |
| --- | --- | --- | --- | --- |
| 0x0809d718 | scan_equip_zone_for_last_turn_activation | asm/13_equip_placement.s:5 | 6746 | 72 |
| 0x0809d764 | scan_equip_zone_for_last_turn_sprite | asm/13_equip_placement.s:43 | 6811 | 50 |
| 0x0809d79c | scan_equip_chain_for_power_bond_sprite_and_lp_indicator | asm/13_equip_placement.s:73 | 6804 | 74 |
| 0x0809d7ec | scan_equip_chain_list_for_sprite_by_card_and_zone | asm/13_equip_placement.s:113 | 6732 | 112 |
| 0x0809d86c | scan_equip_chain_list_for_sprite_crush_card | asm/13_equip_placement.s:182 | 6805 | 14 |
| 0x0809d880 | scan_equip_chain_list_for_sprite_deck_devastation_virus | asm/13_equip_placement.s:194 | 6806 | 14 |
| 0x0809d894 | scan_equip_chain_list_for_sprite_pikeru_second_sight | asm/13_equip_placement.s:206 | 6807 | 14 |
| 0x0809d8a8 | scan_equip_zone_for_final_countdown_sprite | asm/13_equip_placement.s:218 | 6808 | 94 |
| 0x0809d914 | scan_equip_zone_for_infinite_cards_lp_display_update | asm/13_equip_placement.s:275 | 6809 | 94 |
| 0x0809d984 | run_equip_activation_phase_by_counter | asm/13_equip_placement.s:334 | 6810 | 1486 |
| 0x0809e078 | dispatch_field_spell_phase_by_display_state | asm/13_equip_placement.s:1249 | 15805 | 194 |
| 0x0809e168 | tick_duel_field_spell_activation_state | asm/13_equip_placement.s:1376 | 7161 | 772 |
| 0x0809e5e0 | scan_equip_zone_for_toon_card_activation | asm/13_equip_placement.s:1948 | 7243 | 102 |
| 0x0809e654 | find_equip_slot_idx_with_entity_id_one | asm/13_equip_placement.s:2011 | 7244 | 64 |
| 0x0809e6a4 | find_equip_slot_idx_with_entity_id_zero | asm/13_equip_placement.s:2056 | 7245 | 64 |

机器证据: `f13-module-map.json`, `f13-seg1-slots.json`, `f13-seg1-plan.json.coverage`, `root-f13-route-check.json`, `root-f13-seg1-functions-before.json`. 路线图已覆盖模块41412 B; 本提案不展开后续段语义.

## 数据块分类 (Rule 2/3)

段内裸块扫描为空. 下列三个ROM区是本段literal直接引用、固定长度调用循环使用的必要依赖, 当前属于rom.s同一incbin. 全ROM逐字节查找raw/THUMB|1, 对各表内每个2字节候选入口重复扫描, 保留全部命中地址.

| 块/大小 | 全ROM ref-scan | 分类 | 消费者/边界依据 |
| --- | --- | --- | --- |
| 0x09e476b0..0x09e47738 / 136 B | base raw=1 at 0x0809df88, thumb=0; 其余候选raw=0/thumb=0 | carve | phase11; 34个fn\|1; 详见固定界限证据 |
| 0x09e47738..0x09e4779c / 100 B | base raw=1 at 0x0809dfe0, thumb=0; 其余候选raw=0/thumb=0 | carve | phase12; 25个fn\|1; 详见固定界限证据 |
| 0x09e4779c..0x09e477ac / 16 B | base raw=1 at 0x0809e044, thumb=0; 其余候选raw=0/thumb=0 | carve | phase20; 4个fn\|1; 详见固定界限证据 |

两张段内switch早已结构化, 不另计裸块或carve. 0x0809da00有21项, 0x0809e1c4有31项, 共52个偶地址word. 0x0809d9f2与0x0809e1aa机器码均8746, 即Thumb `mov pc,r0`; 不执行BX状态交换, 表项必须保持偶地址, 绝不补1. 每个case目标已经在本段指令清单中, 无逐stub disasm任务.

switch base分别raw=1/THUMB=0; 24个去重case目标全部有表内raw引用. 唯一额外THUMB值扫描命中: case 0x0809e3e0对应0x0809e3e1在0x09e58b99出现1次. 它跨越两个实际word: 0x09e58b98=0x09e3e11c指向`deck/theme_010.ydc`, 0x09e58b9c=0x09e3e108指向`deck/theme_011.ydc`; 原字节`1c e1 e3 09 08 e1 e3 09`. 消费者`asm/01_vija_scene_text.s:3853-3857`执行index<<2后word读取, `asm/rom.s:1820-1821`归属card_deck_fs_path_table. 因此+1跨word窗口是数值偶合, 不新增函数指针引用. 原始raw计数仍保留在`f13-seg1-switches.json`与`f13-seg1-refscan-coincidences.json`, 不修改该段外表. 置信度high.

## 符号化计划 (R1/R2/R3)

以下四元组/三元组是唯一槽清单. 全部slot标签设USER_DEFINED并符合小写命名规则. EOL全文见后面的逐槽消费者表; plan保存同一文字及每个槽真实前态. EQ共93, REF共19, RENAME共30, 并集恰为142. 不向指令操作数新增equate; EQ仅是槽地址operand0 data-equate.

### EQ_SLOTS

85次槽引用复用28个已有equate, 8次槽引用使用8个NEW数值equate. 逐槽NEW/REUSE和目标inc见常量表.

```text
(0x0809d758, 0x0000151e, LAST_TURN_CID, last_turn_cid_9d758)
(0x0809d77c, 0x0000151e, LAST_TURN_CID, last_turn_cid_9d77c)
(0x0809d7b4, 0x000018fe, POWER_BOND_CID, power_bond_cid_9d7b4)
(0x0809d85c, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9d85c)
(0x0809d868, 0x0000803b, OAM_EQUIP_SET_SLOT_P2, sprite_counter_p2_9d868)
(0x0809d87c, 0x0000123b, CRUSH_CARD_CID, crush_card_cid_9d87c)
(0x0809d890, 0x0000188c, DECK_DEVASTATION_VIRUS_CID, deck_devastation_cid_9d890)
(0x0809d8a4, 0x000018d5, PIKERU_SECOND_SIGHT_CID, pikeru_second_sight_cid_9d8a4)
(0x0809d908, 0x0000169c, FINAL_COUNTDOWN_CID, final_countdown_cid_9d908)
(0x0809d910, 0x0000803b, OAM_EQUIP_SET_SLOT_P2, sprite_counter_p2_9d910)
(0x0809d96c, 0x00001401, INFINITE_CARDS_CID, infinite_cards_cid_9d96c)
(0x0809d970, 0x0000159f, HIEROGLYPH_LITHOGRAPH_CID, hieroglyph_cid_9d970)
(0x0809d978, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9d978)
(0x0809d9d0, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, player_off_9d9d0)
(0x0809d9d4, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9d9d4)
(0x0809d9d8, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9d9d8)
(0x0809d9f8, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9d9f8)
(0x0809da8c, 0x00008011, OAM_EQUIP_SPRITE_P2_11, sprite_p2_11_9da8c)
(0x0809da94, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9da94)
(0x0809da98, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9da98)
(0x0809dabc, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9dabc)
(0x0809db40, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9db40)
(0x0809db44, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9db44)
(0x0809db48, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9db48)
(0x0809db4c, 0x00000fee, COCOON_OF_EVOLUTION_CID, cocoon_cid_9db4c)
(0x0809db50, 0x0000150e, SPIRITUAL_ENERGY_SETTLE_CID, spiritual_energy_cid_9db50)
(0x0809dc9c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9dc9c)
(0x0809dca0, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9dca0)
(0x0809dca4, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9dca4)
(0x0809dca8, 0x00001102, SWORDS_OF_REVEALING_LIGHT_CID, swords_cid_9dca8)
(0x0809dd24, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9dd24)
(0x0809dee0, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9dee0)
(0x0809dee8, 0x0000149d, EKIBYO_DRAKMORD_CID, ekibyo_cid_9dee8)
(0x0809def0, 0xffffe000, OAM_ATTR2_TILE_CLEAR, low13_clear_mask_9def0)
(0x0809def8, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9def8)
(0x0809defc, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9defc)
(0x0809df00, 0x00008046, OAM_EQUIP_SPRITE_P2_46, sprite_p2_46_9df00)
(0x0809df84, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9df84)
(0x0809df8c, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9df8c)
(0x0809dfdc, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9dfdc)
(0x0809dfe4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9dfe4)
(0x0809e048, 0x00001d24, EQUIP_ACTIVATION_SCAN_CURSOR_OFF, scan_cursor_off_9e048)
(0x0809e04c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e04c)
(0x0809e098, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, player_off_9e098)
(0x0809e09c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e09c)
(0x0809e0d4, 0x00008002, OAM_EQUIP_SPRITE_P2_02, sprite_p2_02_9e0d4)
(0x0809e154, 0x00001356, GAMBLE_CID, gamble_cid_9e154)
(0x0809e158, 0x00001d04, PUZZLE_READY_FLAG_OFF, timer_notice_gate_off_9e158)
(0x0809e15c, 0x00001cec, P1LP_TIMER_OFF, timer_off_9e15c)
(0x0809e160, 0x0000800b, SPRITE_ATTR_DUEL_PHASE_P2, sprite_phase_p2_9e160)
(0x0809e1b0, 0x00001ce8, P1LP_BLOCK2_OFF_1CE8, player_off_9e1b0)
(0x0809e1b4, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9e1b4)
(0x0809e1b8, 0x000013b1, TIMEATER_CID, timeater_cid_9e1b8)
(0x0809e1bc, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e1bc)
(0x0809e264, 0x00001d30, EQUIP_CHAIN_CANCEL_OFF, chain_cancel_off_9e264)
(0x0809e268, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e268)
(0x0809e290, 0x0000800e, OAM_EQUIP_SPRITE_P2_0E, sprite_p2_0e_9e290)
(0x0809e294, 0x00001d54, ELIGIB_STATE_CTRL_OFF, eligib_state_off_9e294)
(0x0809e298, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e298)
(0x0809e2e4, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e2e4)
(0x0809e300, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e300)
(0x0809e328, 0x00001d54, ELIGIB_STATE_CTRL_OFF, eligib_state_off_9e328)
(0x0809e32c, 0x00001d58, ELIGIB_ACT_COUNT_OFF, eligib_count_off_9e32c)
(0x0809e330, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e330)
(0x0809e348, 0x00001d5c, ELIGIB_ACT_TYPE_OFF, eligib_type_off_9e348)
(0x0809e36c, 0x00001d30, EQUIP_CHAIN_CANCEL_OFF, chain_cancel_off_9e36c)
(0x0809e370, 0x00001d28, EQUIP_CHAIN_STEP_OFF, chain_step_off_9e370)
(0x0809e374, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e374)
(0x0809e38c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e38c)
(0x0809e3b0, 0x00001cf4, P2LP_BLOCK2_OFF_1CF4, field_phase_off_9e3b0)
(0x0809e3dc, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e3dc)
(0x0809e424, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e424)
(0x0809e438, 0x00000135, CARD_DISPLAY_OP31_PARAM_0135, display_op31_param_9e438)
(0x0809e440, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e440)
(0x0809e480, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e480)
(0x0809e4bc, 0x00001d30, EQUIP_CHAIN_CANCEL_OFF, chain_cancel_off_9e4bc)
(0x0809e4c0, 0x00001d28, EQUIP_CHAIN_STEP_OFF, chain_step_off_9e4c0)
(0x0809e4cc, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e4cc)
(0x0809e4e0, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e4e0)
(0x0809e508, 0x00001cf4, P2LP_BLOCK2_OFF_1CF4, field_phase_off_9e508)
(0x0809e50c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e50c)
(0x0809e544, 0x00001d30, EQUIP_CHAIN_CANCEL_OFF, chain_cancel_off_9e544)
(0x0809e548, 0x00008010, OAM_EQUIP_SPRITE_P2_10, sprite_p2_10_9e548)
(0x0809e54c, 0x00001d1c, CARD_PLAY_PHASE_CTR_OFF, phase_off_9e54c)
(0x0809e5c8, 0x00001cf4, P2LP_BLOCK2_OFF_1CF4, field_phase_off_9e5c8)
(0x0809e5cc, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9e5cc)
(0x0809e5d4, 0x00001954, VWXYZ_DRAGON_CATAPULT_CANNON_CID, vwxyz_cid_9e5d4)
(0x0809e638, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9e638)
(0x0809e640, 0x00001954, VWXYZ_DRAGON_CATAPULT_CANNON_CID, vwxyz_cid_9e640)
(0x0809e684, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9e684)
(0x0809e68c, 0x0000151e, LAST_TURN_CID, last_turn_cid_9e68c)
(0x0809e6d4, 0x00000868, PLAYER_BLOCK_STRIDE, player_stride_9e6d4)
(0x0809e6dc, 0x0000151e, LAST_TURN_CID, last_turn_cid_9e6dc)
```

### REF_SLOTS

每项输出`.word gas_label`. 17项添加新的operand0 DATA/USER_DEFINED primary ref; 两项switch精确替换其同目标DEFAULT引用为DATA/USER_DEFINED, 不删除其他operand或其他目标引用. 不借addMemoryReference合并操作推断source提升. RAM不能根据常量.inc的存在推断已有USER对象或DefinedData.

```text
(0x0809d860, 0x0201c5ec, gDuelFieldSpellZoneBase, chain_slot11_base_9d860)
(0x0809d864, 0x0201d9c0, gEquipNodePool, chain_nodes_base_9d864)
(0x0809d90c, 0x0201e1cc, gP1LpTimer, lp_timer_base_9d90c)
(0x0809d9fc, 0x0809da00, switchD_0809d9f2__switchdataD_0809da00, activation_phase_switch_9d9fc)
(0x0809dbcc, 0x0201e2a0, gDuelCardCtxBase, duel_card_ctx_base_9dbcc)
(0x0809dee4, 0x0201c510, gDuelFieldSlots, field_slots_base_9dee4)
(0x0809deec, 0x0201c520, gDuelFieldSlotState, field_slot_state_base_9deec)
(0x0809df88, 0x09e476b0, equip_activation_phase11_callbacks, phase11_callbacks_9df88)
(0x0809dfe0, 0x09e47738, equip_activation_phase12_callbacks, phase12_callbacks_9dfe0)
(0x0809e044, 0x09e4779c, equip_activation_phase20_callbacks, phase20_callbacks_9e044)
(0x0809e0d8, 0x0201e2a0, gDuelCardCtxBase, duel_card_ctx_base_9e0d8)
(0x0809e0dc, 0x0201afe0, gEquipLpScoreBase, lp_score_base_9e0dc)
(0x0809e1c0, 0x0809e1c4, switchD_0809e1aa__switchdataD_0809e1c4, field_phase_switch_9e1c0)
(0x0809e2e8, 0x0201e2a0, gDuelCardCtxBase, duel_card_ctx_base_9e2e8)
(0x0809e404, 0x0201e2a0, gDuelCardCtxBase, duel_card_ctx_base_9e404)
(0x0809e5d0, 0x0201c510, gDuelFieldSlots, field_slots_base_9e5d0)
(0x0809e63c, 0x0201c510, gDuelFieldSlots, field_slots_base_9e63c)
(0x0809e688, 0x0201c510, gDuelFieldSlots, field_slots_base_9e688)
(0x0809e6d8, 0x0201c510, gDuelFieldSlots, field_slots_base_9e6d8)
```

### RENAME_SLOTS

这30槽全部仍为`.word gP1LifePoints`. 原operand0 DATA/DEFAULT/primary引用保持原样; 目标LABEL是USER_DEFINED不能证明引用也是USER_DEFINED. 只改槽名并设下列EOL, 不重建Data/ref/equate.

```text
(0x0809d974, gp1lp_base_9d974, "Player-state base; read the hand-count word at base+(player&1)*PLAYER_BLOCK_STRIDE+0xc.")
(0x0809d9cc, gp1lp_base_9d9cc, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809d9f4, gp1lp_base_9d9f4, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809da90, gp1lp_base_9da90, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809dab8, gp1lp_base_9dab8, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809db3c, gp1lp_base_9db3c, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809dc98, gp1lp_base_9dc98, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809dd20, gp1lp_base_9dd20, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809def4, gp1lp_base_9def4, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809df80, gp1lp_base_9df80, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809dfd8, gp1lp_base_9dfd8, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e040, gp1lp_base_9e040, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e094, gp1lp_base_9e094, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e164, gp1lp_base_9e164, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e1ac, gp1lp_base_9e1ac, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e260, gp1lp_base_9e260, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e2e0, gp1lp_base_9e2e0, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e2fc, gp1lp_base_9e2fc, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e324, gp1lp_base_9e324, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e3ac, gp1lp_base_9e3ac, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e3d8, gp1lp_base_9e3d8, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e408, gp1lp_base_9e408, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e420, gp1lp_base_9e420, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e43c, gp1lp_base_9e43c, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e47c, gp1lp_base_9e47c, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e498, gp1lp_base_9e498, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e4dc, gp1lp_base_9e4dc, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e504, gp1lp_base_9e504, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e540, gp1lp_base_9e540, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
(0x0809e5c4, gp1lp_base_9e5c4, "gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.")
```

### REF目标真实前态及C7守卫

| 地址 | 输出名 | 现有primary LABEL | DefinedData前态 | 动作 |
| --- | --- | --- | --- | --- |
| 0x0201afe0 | gEquipLpScoreBase | 30393 / USER_DEFINED / gEquipLpScoreBase | /undefined4, 4 B | reuse_existing_user_label |
| 0x0201c510 | gDuelFieldSlots | 20369 / USER_DEFINED / gDuelFieldSlots | /undefined4, 4 B | reuse_existing_user_label |
| 0x0201c520 | gDuelFieldSlotState | 20396 / USER_DEFINED / gDuelFieldSlotState | /undefined4, 4 B | reuse_existing_user_label |
| 0x0201c5ec | gDuelFieldSpellZoneBase | 4611686018461058540 / DEFAULT / DAT_0201c5ec | None | create_user_primary_label |
| 0x0201d9c0 | gEquipNodePool | 20380 / USER_DEFINED / gEquipNodePool | None | reuse_existing_user_label |
| 0x0201e1cc | gP1LpTimer | 4611686018461065676 / DEFAULT / DAT_0201e1cc | /undefined4, 4 B | create_user_primary_label |
| 0x0201e2a0 | gDuelCardCtxBase | 18879 / USER_DEFINED / gDuelCardCtxBase | /undefined4, 4 B | reuse_existing_user_label |
| 0x0809da00 | switchD_0809d9f2__switchdataD_0809da00 | 6770 / ANALYSIS / switchD_0809d9f2::switchdataD_0809da00 | /undefined *, 4 B | normalize_existing_symbol_global |
| 0x0809e1c4 | switchD_0809e1aa__switchdataD_0809e1c4 | 7145 / ANALYSIS / switchD_0809e1aa::switchdataD_0809e1c4 | /undefined *, 4 B | normalize_existing_symbol_global |
| 0x09e476b0 | equip_activation_phase11_callbacks | 4611686018593355440 / DEFAULT / PTR_scan_monster_zone_for_equip_activation_spiritual_energy_settle_machine+1_09e476b0 | /undefined *, 4 B | create_user_primary_label |
| 0x09e47738 | equip_activation_phase12_callbacks | 4611686018593355576 / DEFAULT / PTR_scan_spell_trap_zone_slots_for_equip_activation_greed+1_09e47738 | /undefined *, 4 B | create_user_primary_label |
| 0x09e4779c | equip_activation_phase20_callbacks | 4611686018593355676 / DEFAULT / PTR_scan_equip_chain_list_for_sprite_crush_card+1_09e4779c | /undefined *, 4 B | create_user_primary_label |

- Switch两个原LABEL对象id6770/id7145必须原对象改namespace/name/source/primary, 规范到全局完整GAS名`switchD_0809d9f2__switchdataD_0809da00`和`switchD_0809e1aa__switchdataD_0809e1c4`. 禁止创建同址alias; 只改source而不改getName()不能保证导出名. 两表52个word、24个case目标、全部case符号和非相关refs原样.
- 0x0201c5ec当前只有DEFAULT动态LABEL, 新增gDuelFieldSpellZoneBase USER主LABEL但保留DefinedData=None. 0x0201d9c0已有gEquipNodePool USER LABEL但DefinedData同为None, 也不定义RAM Data.
- 0x0201e1cc当前DEFAULT动态LABEL且已有undefined4 Data; 新设gP1LpTimer USER主LABEL. 保留原22条ANALYSIS READ/WRITE incoming, 新增仅池0x0809d90c的DATA/USER_DEFINED ref. 不读取RAM初值, 不声称其值为0.
- 三张表63项原始定义均为undefined*4, outgoing为operand0 DATA/DEFAULT/primary且指向原odd地址的动态LABEL. 保留63条原引用、target primary和Data定义, 不改成偶Function目标、不升级source、不createData. 新增仅三表头USER主LABEL及代码侧三个REF. 0x09e477ac为范围外下一word, 其Data/ref保持原样.
- `tools/asm-regen/ghidra/ExportRangeToGas.py:506-562`只接受ROM USER LABEL目标; ROM FUNCTION被排除且sanitize_label会改写`+`. 本提案的函数指针由rom.s明确`.word fn + 1`输出, 不承诺普通REF自动输出`fn+1`, 不修改全局exporter.

## FUNC_RENAME及正式依赖

```text
(0x0809d7ec, scan_equip_chain_list_for_sprite_by_card_and_zone, enqueue_equip_chain_counter_sprites_by_card)
(0x0809e5e0, scan_equip_zone_for_toon_card_activation, scan_field_slots_for_vwxyz_dragon_catapult_cannon_activation)
```

0x0809d7ec的indegree=3, 实际普通BL来自0x0809d872/0x0809d886/0x0809d89a. `asm/13_equip_placement.s:113-177`: r2保存为counter_base; 0x0809d822..d828以byte[node+2]&15对常数1筛选, 0x0809d838..d840计算(counter_base-(byte[node+2]>>5))&0xffff, 并非由r2给出zone过滤器. 从chain slot11沿8字节node+6链遍历, 所有匹配CID且类型1的节点提交计数sprite, 返回值固定1. 三个wrapper有push/BL/pop, 不是tail-call. 更名准确反映副作用及参数. 置信度high.

0x0809e5e0的indegree=2, BL来自0x08097ac2/0x08097b48. `asm/13_equip_placement.s:1948-2008`: 五个20字节field slot读取低13位CID与0x1954比较, 还要求u16[slot+8]!=0. card-stats/ROM及逻辑CID列均对应VWXYZ-Dragon Catapult Cannon; 旧Toon描述错误. 调用apply_equip_activation_via_packed_attr后仅非零结果才返回0, 否则继续扫描. 保留实际Function ID7243和原body, 更名不改代码. 置信度high.

两函数全ROM even/odd值扫描均0, 没有手工ROM指针项需要同步这两个名称. 三张新增carve的63项也不包含这两个入口, 因而其target导航名无derived例外. 正式旧名命中逐项如下; 历史proposal/review/scripts保持原文, 不作全仓库替换.

#### 0x0809d7ec 正式命中

| 文件/行 | 内容 |
| --- | --- |
| asm/13_equip_placement.s:113 | scan_equip_chain_list_for_sprite_by_card_and_zone: |
| asm/13_equip_placement.s:181 | @ 4-instruction thin wrapper for scan_equip_chain_list_for_sprite_by_card_and_zone, Crush Card variant. r0=player_id [0..1] (pass-through); fixed r1=0x123b (Crush Card), r2=3 (zone_col). Tail-calls scan_equip_chain_list_for_sprite_by_card_and_zone (FUN_0809d7ec). Returns r0=u32 always 1 (pass-through). Side effects: OAM sprite attr buffer via callee -> enqueue_sprite_attr_record. Constants: CARD_ID=0x123b (Crush Card), zone_col=3. |
| asm/13_equip_placement.s:186 | bl scan_equip_chain_list_for_sprite_by_card_and_zone @ 0809d872 fff7bbff |
| asm/13_equip_placement.s:193 | @ Equip chain sprite scan case stub for Deck Devastation Virus (internal_card_id=0x188c, cid=1803). Called by duel_field main dispatch hub (FUN_0809d984). Fixes r1=0x188c, r2=3 (zone=3) then tail-calls scan_equip_chain_list_for_sprite_by_card_and_zone. Side effects: via scan_equip_chain_list_for_sprite_by_card_and_zone on hit. |
| asm/13_equip_placement.s:198 | bl scan_equip_chain_list_for_sprite_by_card_and_zone @ 0809d886 fff7b1ff |
| asm/13_equip_placement.s:205 | @ Equip chain sprite scan case stub for Pikeru's Second Sight (internal_card_id=0x18d5, cid=1861). Called by duel_field main dispatch hub (FUN_0809d984). Fixes r1=0x18d5, r2=2 (zone=2) then tail-calls scan_equip_chain_list_for_sprite_by_card_and_zone. Side effects: via scan_equip_chain_list_for_sprite_by_card_and_zone on hit. |
| asm/13_equip_placement.s:210 | bl scan_equip_chain_list_for_sprite_by_card_and_zone @ 0809d89a fff7a7ff |
| tools/ghidra-labeling/RenameKnownFunctions.py:10990 | ("FUN_0809d7ec", "scan_equip_chain_list_for_sprite_by_card_and_zone", |
| tools/ghidra-labeling/RenameKnownFunctions.py:11005 | "4-instruction thin wrapper for scan_equip_chain_list_for_sprite_by_card_and_zone, Crush Card variant. " |
| tools/ghidra-labeling/RenameKnownFunctions.py:11007 | "Tail-calls scan_equip_chain_list_for_sprite_by_card_and_zone (FUN_0809d7ec). " |
| tools/ghidra-labeling/RenameKnownFunctions.py:11090 | "Fixes r1=0x188c, r2=3 (zone=3) then tail-calls scan_equip_chain_list_for_sprite_by_card_and_zone. " |
| tools/ghidra-labeling/RenameKnownFunctions.py:11091 | "Side effects: via scan_equip_chain_list_for_sprite_by_card_and_zone on hit."), |
| tools/ghidra-labeling/RenameKnownFunctions.py:11109 | "Fixes r1=0x18d5, r2=2 (zone=2) then tail-calls scan_equip_chain_list_for_sprite_by_card_and_zone. " |
| tools/ghidra-labeling/RenameKnownFunctions.py:11110 | "Side effects: via scan_equip_chain_list_for_sprite_by_card_and_zone on hit."), |
| doc/dev/naming-proposals.csv:3105 | 0x0809d7ec,scan_equip_chain_list_for_sprite_by_card_and_zone,,, |

#### 0x0809e5e0 正式命中

| 文件/行 | 内容 |
| --- | --- |
| asm/12_equip_activation_scan.s:7721 | bl scan_equip_zone_for_toon_card_activation @ 08097ac2 06f08dfd |
| asm/12_equip_activation_scan.s:7789 | bl scan_equip_zone_for_toon_card_activation @ 08097b48 06f04afd |
| asm/13_equip_placement.s:1948 | scan_equip_zone_for_toon_card_activation: |
| tools/ghidra-labeling/RenameKnownFunctions.py:13100 | ("FUN_0809e5e0", "scan_equip_zone_for_toon_card_activation", |
| tools/ghidra-labeling/RenameKnownFunctions.py:13172 | "case_3: eval_slot_activation_guard_full / scan_equip_zone_for_toon_card_activation / " |
| doc/dev/naming-proposals.csv:3114 | 0x0809e5e0,scan_equip_zone_for_toon_card_activation,,,duel_field |

实施限界: asm13的2定义、3同段BL和三wrapper PLATE按本提案同步; asm12仅2个BL目标拼写改动, 不写asm12任何Ghidra plate. CSV仅两个地址的name单元格. RenameKnownFunctions.py仅6个既有tuple: d7ec/e5e0改name+全文plate, d86c/d880/d894仅换本提案全文plate; 97828仅将旧Toon函数引用子串换新名一次, 保留该tuple所有其他文字. 当前97828的Ghidra/asm12 plate均不含该旧名, 所以不得将registry旧plate写回Ghidra.

重新导出四份函数inventory: `temp/ghidra-functions.csv`, `temp/ghidra-functions-auto.txt`, `temp/ghidra-functions-renamed.txt`, `temp/ghidra-functions-summary.md`; 所有地址/body/source保持, 仅涉及上述两个正式名称. 无其他生成器、数据导出源或历史脚本改动. `f13-seg1-rename-dependencies.json`保留原始命中全文和raw扫描.

## PLATE (R5, 全文替换)

15个已有函数全部全文替换, 无额外函数plate. 新文本ASCII且最大472字符. 每项保留旧全文SHA256, 旧全文和Function ID/body/ranges/incoming/EOL在plan.expected和只读snapshot中可逐字守卫. 所有原函数体和incoming refs保持, 包括两次改名. 除142个池槽EOL外, 原指令EOL全部保持.

### 0x0809d718 scan_equip_zone_for_last_turn_activation

新长度: 230; 旧全文SHA256: `8246a5394dc0e60e6a3b21ab74e84da278e565e85d93be6509d08df1dbbd32be`.

```text
r0=player. Require LAST_TURN_CID in chain slot11, at least one occupied monster slot for this player, and none for 1-player. On success enqueue the card sprite and type11(player,CID,5,0), then return0. Return1 when any gate fails.
```

### 0x0809d764 scan_equip_zone_for_last_turn_sprite

新长度: 216; 旧全文SHA256: `cd4f296128e3e19760bab84740692322bdec30785a193633ecbabf419f80edf1`.

```text
r0=player. Test LAST_TURN_CID in chain slot11. If absent return1. Otherwise enqueue the equip-zone card sprite and type11(player,CID,5,0), then return0. This path does not test either player's occupied monster count.
```

### 0x0809d79c scan_equip_chain_for_power_bond_sprite_and_lp_indicator

新长度: 263; 旧全文SHA256: `2e21c4dbb64e4f1664f4a6680dd965c5d8515d5286a8448d74eb77b247744d14`.

```text
r0=player. If POWER_BOND_CID is absent from chain slot11, return1. Otherwise read its entity value, enqueue the card sprite, submit the LP indicator as (player,entity,0,CID), and enqueue the equip-slot sprite as (player,11,CID,0). Return0 after these submissions.
```

### 0x0809d7ec enqueue_equip_chain_counter_sprites_by_card

新长度: 391; 旧全文SHA256: `dc00fea5d3444424781777a2d8a626c5c41a7611473079ecf2383fdbfd58f4a6`.

```text
r0=player, r1=CID, r2=counter_base. Require CID in chain slot11. Follow the head at gDuelFieldSpellZoneBase+(player&1)*PLAYER_BLOCK_STRIDE+0xa through 8-byte gEquipNodePool nodes, using next=u16[node+6]. Match u16[node]==CID and (byte[node+2]&15)==1. Submit type0x3b/0x803b with (CID&0xffff,1,(counter_base-(byte[node+2]>>5))&0xffff) for every match. r2 is not a zone filter. Always return1.
```

### 0x0809d86c scan_equip_chain_list_for_sprite_crush_card

新长度: 252; 旧全文SHA256: `504236e468c43b7424f6f584c7eaa07bfbd871528a1f220d5090b1b2f4cf30cf`.

```text
r0=player. Call enqueue_equip_chain_counter_sprites_by_card(player,CRUSH_CARD_CID,3). The third argument is a counter base; the callee fixes the node-type filter to1. Return the callee result, always1. Sprite submissions occur for matching chain nodes.
```

### 0x0809d880 scan_equip_chain_list_for_sprite_deck_devastation_virus

新长度: 234; 旧全文SHA256: `04a44dafc4632c3e22790837c6f203d501b61f9ed5032570980ef6e901db72d5`.

```text
r0=player. Call enqueue_equip_chain_counter_sprites_by_card(player,DECK_DEVASTATION_VIRUS_CID,3). The third argument is a counter base, not a zone index. Return the callee result, always1. Matching chain nodes enqueue counter sprites.
```

### 0x0809d894 scan_equip_chain_list_for_sprite_pikeru_second_sight

新长度: 231; 旧全文SHA256: `e6c3b2ee0b0e3cbe378cc3292230496853a2b9b72ce1eaf80283a80854b01936`.

```text
r0=player. Call enqueue_equip_chain_counter_sprites_by_card(player,PIKERU_SECOND_SIGHT_CID,2). The third argument is a counter base, not a zone index. Return the callee result, always1. Matching chain nodes enqueue counter sprites.
```

### 0x0809d8a8 scan_equip_zone_for_final_countdown_sprite

新长度: 344; 旧全文SHA256: `91a4f0898ff377d3037761cb1925de9c59ea50010d7ff9accadf2920a7416a0b`.

```text
r0=starting player. Visit that player and player^1. For a nonnegative FINAL_COUNTDOWN_CID entity value in chain slot11, compute count=word[gP1LpTimer]-entity+1. Enqueue type0x3b/0x803b with (CID,1,count&0xffff). If signed count>19, also enqueue type11(player,CID,1,1). Always return1 after both sides. The timer is gP1LifePoints+P1LP_TIMER_OFF.
```

### 0x0809d914 scan_equip_zone_for_infinite_cards_lp_display_update

新长度: 403; 旧全文SHA256: `2f2f71710944e6bf95e4b9489e3184dfa27cca1f9fb85b755cc08e683bf41b0d`.

```text
r0=player. Return1 if count_field_copies_of_card(INFINITE_CARDS_CID) is nonzero. Otherwise limit=6, raised to7 by HIEROGLYPH_LITHOGRAPH_CID in chain slot11 and overridden to5 by available Enervating Mist(0x1800) zones for 1-player. Read count at gP1ZoneHandCount+(player&1)*PLAYER_BLOCK_STRIDE. If unsigned count>limit, submit set_lp_display_row_if_nonzero(player,count-limit) and return0; else return1.
```

### 0x0809d984 run_equip_activation_phase_by_counter

新长度: 458; 旧全文SHA256: `7d2fa90b77dd60cb754dcbfd6f0fb12519c843291e2773fd97d138d1b8e65239`.

```text
No inputs. Read player at gP1LifePoints+0x1ce8, bit23 at base+(player&1)*0x868+0x11c, and phase at+0x1d1c. For nonzero phase, a successful Last Turn scan returns0. Phase0..20 selects21 even MOV-pc targets; default/unused phases return1. Active paths update phase/cursors, submit sprites and test slots. Phase11/20 resume34/4 callback tables; phase12 restarts25 callbacks each tick. A callback returning0 yields0. All paths restore the shared0x120-byte frame.
```

### 0x0809e078 dispatch_field_spell_phase_by_display_state

新长度: 414; 旧全文SHA256: `5fc34748e9dc4773f5fdaddf6b555b93cfec45f3fcf38cb3f7aea6869391ba71`.

```text
No inputs. Read player at gP1LifePoints+0x1ce8 and CARD_PLAY_PHASE_CTR_OFF. Phase0 enqueues type2/0x8002, clears0x1cc bytes at gEquipLpScoreBase if the player context word is1, advances phase and returns0. Phase1 tests GAMBLE_CID in chain slot11 and sets player flag0x17 on a hit. It submits timer notices at backup+1 when the +0x1d04 gate is0, and at backup+4 unconditionally. Phase1 and all other phases return1.
```

### 0x0809e168 tick_duel_field_spell_activation_state

新长度: 472; 旧全文SHA256: `c150d59537a4badd3dd22f6778471e4f2f20497b25022a8207ddf5a8ddf93986`.

```text
No inputs. Read player, its flag bit23, TIMEATER_CID chain membership and CARD_PLAY_PHASE_CTR_OFF. Dispatch phase0..30 through31 even MOV-pc targets; unused/default entries return0. Routes display selection, AI progress and equip gates, updating phase and control/cancel fields. Phase30 scans five field slots for VWXYZ_DRAGON_CATAPULT_CANNON_CID in field phases2/4. Return1 on the flag/cancel exit or completed final path; pending work and ordinary phase changes return0.
```

### 0x0809e5e0 scan_field_slots_for_vwxyz_dragon_catapult_cannon_activation

新长度: 387; 旧全文SHA256: `1cc053e27be85dfe3196358d606f10f0f1a7857270e3e9a3db879bfef7e748fa`.

```text
r0=player. Scan five 20-byte entries at gDuelFieldSlots+(player&1)*PLAYER_BLOCK_STRIDE. Require low13 CID=VWXYZ_DRAGON_CATAPULT_CANNON_CID and u16[slot+8]!=0. Call apply_equip_activation_via_packed_attr with (slot_index<<16)|0x600000|(player<<31)|CID, the packed entry flags, and0. Return0 only when that call returns nonzero; otherwise continue scanning and return1 after all five fail.
```

### 0x0809e654 find_equip_slot_idx_with_entity_id_one

新长度: 306; 旧全文SHA256: `c528de7a9c52b3a9705efacb28b983e3a5c4f16b43c5cb968b5191043efa8388`.

```text
r0=player. Scan slot indices0..4 at gDuelFieldSlots+(player&1)*PLAYER_BLOCK_STRIDE with stride20. Skip entries whose low13 CID bits are0. Return the first index where get_node_entity_id_in_slot(player,index,LAST_TURN_CID)==1. Return-1 when no entry matches. The input is a player value, not a slot pointer.
```

### 0x0809e6a4 find_equip_slot_idx_with_entity_id_zero

新长度: 334; 旧全文SHA256: `7df6c0081d0e27ae8afe2ea995fe384478c3065262be1d358a3aeff5d9fa1066`.

```text
r0=player. Scan slot indices0..4 at gDuelFieldSlots+(player&1)*PLAYER_BLOCK_STRIDE with stride20. Skip entries whose low13 CID bits are0. Return the first index where get_node_entity_id_in_slot(player,index,LAST_TURN_CID)==0. Return-1 when no entry matches. A missing node returns-1 from the lookup and does not satisfy the zero test.
```

## carve计划 (R7)

`asm/rom.s:1371`原host为offset0x1e4755c,size0x27b0. 替换后prefix0x154 + 三表0xfc + suffix0x2560 = 原0x27b0. 保留prefix内包括模块12既有表0x09e47680/0x09e47688和所有suffix字节. 本批新增3个ROM USER LABEL, 不新增3个equate.

实际界限: `asm/13_equip_placement.s:1078`附近0x0809df34比较#0x21并以bls继续, 是34项; 0x0809dfb6比较#0x18是25项; 0x0809dff2/0x0809e01c比较#3是4项. phase11与20读取gP1LifePoints+0x1d20持久索引, phase12在每次进入时将局部索引清0. 回调通过`invoke_r1`的BX r1执行(`asm/23_sound_cardlist_libc.s:15338-15339`中的0x0810e5cc), r0=player; 返回0即本帧yield, 非零才清+0x1d24并继续. 表长由循环证明, 不根据相邻word形态猜终止哨兵.

```asm
.incbin "roms/2343.gba", 0x1e4755c, 0x154
equip_activation_phase11_callbacks:
    .word scan_monster_zone_for_equip_activation_spiritual_energy_settle_machine + 1    @ 0x09e476b0 = 0x0809cb79
    .word scan_all_monster_zone_slots_for_equip_activation_mirage_knight + 1    @ 0x09e476b4 = 0x0809c78d
    .word scan_equip_zone_for_interdimensional_matter_transporter + 1    @ 0x09e476b8 = 0x0809c8cd
    .word scan_equip_zone_for_strike_ninja_activation + 1    @ 0x09e476bc = 0x0809c921
    .word scan_zone_f_for_equip_activation_dd_scout_plane + 1    @ 0x09e476c0 = 0x0809c979
    .word scan_equip_slot_for_dd_survivor_activation + 1    @ 0x09e476c4 = 0x0809ca35
    .word scan_monster_zone_slots_for_equip_activation_by_cid_table + 1    @ 0x09e476c8 = 0x0809c7ad
    .word scan_equip_zone_for_super_rejuvenation_activation + 1    @ 0x09e476cc = 0x0809d375
    .word scan_spell_trap_zone_for_two_man_cell_battle_equip + 1    @ 0x09e476d0 = 0x0809d51d
    .word scan_monster_zone_slots_for_equip_activation_solar_flare_dragon + 1    @ 0x09e476d4 = 0x0809c74d
    .word scan_monster_zone_slots_for_equip_activation_satellite_cannon + 1    @ 0x09e476d8 = 0x0809cab5
    .word scan_spell_trap_zone_slots_for_equip_activation_ectoplasmer + 1    @ 0x09e476dc = 0x0809d4dd
    .word scan_monster_zone_slots_for_equip_activation_berserk_dragon + 1    @ 0x09e476e0 = 0x0809cac5
    .word scan_monster_zone_slots_for_equip_activation_reserved_icid_d + 1    @ 0x09e476e4 = 0x0809caa5
    .word scan_equip_zone_for_return_of_the_doomed_activation + 1    @ 0x09e476e8 = 0x0809d1dd
    .word scan_equip_activation_candidates_with_name_display + 1    @ 0x09e476ec = 0x0809d5f5
    .word scan_all_monster_zone_slots_for_equip_activation_insect_queen + 1    @ 0x09e476f0 = 0x0809c75d
    .word scan_equip_zone_for_infinite_dismissal_activation + 1    @ 0x09e476f4 = 0x0809cfc5
    .word scan_equip_zone_chain_for_sprite_and_bitmap_update + 1    @ 0x09e476f8 = 0x0809d0c9
    .word scan_all_monster_zone_slots_for_equip_activation_dd_guide + 1    @ 0x09e476fc = 0x0809c77d
    .word scan_all_zone_slots_for_equip_chain_sprite_karate_man + 1    @ 0x09e47700 = 0x0809ce91
    .word scan_all_zone_slots_for_equip_chain_sprite_wild_natures_release + 1    @ 0x09e47704 = 0x0809cea1
    .word scan_all_zone_slots_for_equip_chain_sprite_limiter_removal + 1    @ 0x09e47708 = 0x0809ce81
    .word scan_spell_trap_zone_for_equip_activation_bottomless_shifting_sand + 1    @ 0x09e4770c = 0x0809d199
    .word scan_spell_trap_zone_for_equip_activation_destiny_board + 1    @ 0x09e47710 = 0x0809d181
    .word scan_spell_trap_zone_for_equip_activation_first_sarcophagus + 1    @ 0x09e47714 = 0x0809d1ad
    .word scan_monster_zone_for_equip_activation_garuda_opponent + 1    @ 0x09e47718 = 0x0809d1c5
    .word scan_equip_zone_for_fox_fire_activation + 1    @ 0x09e4771c = 0x0809d345
    .word scan_spell_trap_zone_slots_for_equip_activation_human_wave_tactics + 1    @ 0x09e47720 = 0x0809d4bd
    .word scan_spell_trap_zone_slots_for_equip_activation_boss_rush + 1    @ 0x09e47724 = 0x0809d4fd
    .word scan_equip_zone_for_helios_duo_megiste_activation + 1    @ 0x09e47728 = 0x0809d355
    .word scan_equip_zone_for_helios_tris_megiste_activation + 1    @ 0x09e4772c = 0x0809d365
    .word scan_monster_zone_slots_for_equip_activation_little_winguard + 1    @ 0x09e47730 = 0x0809d4cd
    .word scan_spell_trap_zone_slots_for_equip_activation_labyrinth_of_nightmare + 1    @ 0x09e47734 = 0x0809d4ed
equip_activation_phase12_callbacks:
    .word scan_spell_trap_zone_slots_for_equip_activation_greed + 1    @ 0x09e47738 = 0x0809d50d
    .word scan_equip_chain_for_power_bond_sprite_and_lp_indicator + 1    @ 0x09e4773c = 0x0809d79d
    .word scan_monster_zone_slots_for_equip_activation_cyber_archfiend + 1    @ 0x09e47740 = 0x0809cad5
    .word scan_field_slots_for_equip_bitmap_update_by_card_range + 1    @ 0x09e47744 = 0x0809cc59
    .word scan_monster_zone_for_equip_activation_spiritual_energy_settle_machine + 1    @ 0x09e47748 = 0x0809cb79
    .word scan_all_monster_zone_slots_for_equip_activation_crush_d_gandra + 1    @ 0x09e4774c = 0x0809c79d
    .word scan_monster_zone_for_equip_sprite_and_bitmap_wicked_worm_beast + 1    @ 0x09e47750 = 0x0809cae5
    .word scan_all_zone_slots_for_equip_chain_sprite_magical_scientist + 1    @ 0x09e47754 = 0x0809cd25
    .word scan_all_monster_zone_slots_for_equip_activation_gaia_soul + 1    @ 0x09e47758 = 0x0809c76d
    .word scan_all_zone_slots_for_equip_chain_sprite_limiter_removal + 1    @ 0x09e4775c = 0x0809ce81
    .word scan_all_zone_slots_for_equip_chain_sprite_summoner_of_illusions + 1    @ 0x09e47760 = 0x0809ceb1
    .word scan_all_zone_slots_for_equip_chain_sprite_archfiends_roar + 1    @ 0x09e47764 = 0x0809cee9
    .word scan_all_zone_slots_for_equip_chain_sprite_rescue_cat + 1    @ 0x09e47768 = 0x0809cef9
    .word scan_all_zone_slots_for_return_from_different_dimension_equip + 1    @ 0x09e4776c = 0x0809cf09
    .word scan_equip_chain_and_slots_for_graverobber_sprite + 1    @ 0x09e47770 = 0x0809d221
    .word scan_equip_zone_for_super_rejuvenation_activation + 1    @ 0x09e47774 = 0x0809d375
    .word scan_equip_slot_for_twin_headed_behemoth_activation + 1    @ 0x09e47778 = 0x0809d439
    .word scan_equip_zone_for_dark_necrofear_activation + 1    @ 0x09e4777c = 0x0809d325
    .word scan_equip_zone_for_interdimensional_matter_transporter + 1    @ 0x09e47780 = 0x0809c8cd
    .word scan_equip_zone_for_strike_ninja_activation + 1    @ 0x09e47784 = 0x0809c921
    .word scan_zone_f_for_equip_activation_dd_scout_plane + 1    @ 0x09e47788 = 0x0809c979
    .word scan_equip_slot_for_dd_survivor_activation + 1    @ 0x09e4778c = 0x0809ca35
    .word scan_equip_zone_for_manticore_of_darkness_activation + 1    @ 0x09e47790 = 0x0809d335
    .word scan_equip_zone_for_infinite_cards_lp_display_update + 1    @ 0x09e47794 = 0x0809d915
    .word scan_equip_zone_for_last_turn_sprite + 1    @ 0x09e47798 = 0x0809d765
equip_activation_phase20_callbacks:
    .word scan_equip_chain_list_for_sprite_crush_card + 1    @ 0x09e4779c = 0x0809d86d
    .word scan_equip_chain_list_for_sprite_deck_devastation_virus + 1    @ 0x09e477a0 = 0x0809d881
    .word scan_equip_chain_list_for_sprite_pikeru_second_sight + 1    @ 0x09e477a4 = 0x0809d895
    .word scan_equip_zone_for_final_countdown_sprite + 1    @ 0x09e477a8 = 0x0809d8a9
.incbin "roms/2343.gba", 0x1e477ac, 0x2560
```

63项均已核对现有inventory的偶Function入口, `fn+1`等于ROM原odd值. 本段只引用后续回调现名与地址, 不分析后段回调语义. 63项原定义/ref及边界原态见`root-f13-seg1-rom-tables-before.json`; 本carve只结构化构建源与增加三个表头LABEL, 不清listing或重建指针.

## disasm计划 (R4)

无. 所有段内代码、39条.hword导出的Thumb指令及52个switch目标word已有定义. 不设新TMode、不清listing、不createFunction、不调整函数body或已有flow.

## 新增constants / 全局与复用证明

本轮按当前22个constants文件扫描实际5989条.equ, 解析所有数值并记录源文件SHA256. 不沿用历史总数. 数据见`f13-seg1-constant-values.json`. 复用35个已有equate符号: EQ28个, RAM地址7个(含RENAME的gP1LifePoints); 另复用2个switch LABEL对象. NEW为8个数值equate和1个RAM地址equate, 共9. 既有名称按当前.inc原样使用, 不重定义同名.

| NEW名称 | 值 | 文件 | 消费者理由/同值检索 |
| --- | --- | --- | --- |
| CARD_DISPLAY_OP31_PARAM_0135 | 0x00000135 | constants/duel_field.inc | Display op0x31 parameter, forwarded from r1 by trigger_card_display_op31_if_not_active. 全库无已有同值equate. |
| GAMBLE_CID | 0x00001356 | constants/card_info.inc | CID passed to check_value_in_slot_chain(player,11,CID). 全库无已有同值equate. |
| INFINITE_CARDS_CID | 0x00001401 | constants/card_info.inc | CID passed to count_field_copies_of_card; nonzero count bypasses the hand-limit row update. 全库无已有同值equate. |
| HIEROGLYPH_LITHOGRAPH_CID | 0x0000159f | constants/card_info.inc | CID passed to check_value_in_slot_chain(player,11,CID); a hit raises the hand limit to7. 全库无已有同值equate. |
| OAM_EQUIP_SPRITE_P2_02 | 0x00008002 | constants/oam_attr.inc | Nonzero-player sprite selector; the zero-player branch uses2. Argument0 of enqueue_sprite_attr_record. 同值已有TEXT_RENDER_FLAG_LAYER2, 详见下文不同域证据. |
| OAM_EQUIP_SPRITE_P2_0E | 0x0000800e | constants/oam_attr.inc | Nonzero-player sprite selector; the zero-player branch uses0xe. Argument0 of enqueue_sprite_attr_record. 全库无已有同值equate. |
| OAM_EQUIP_SPRITE_P2_10 | 0x00008010 | constants/oam_attr.inc | Nonzero-player sprite selector; the zero-player branch uses0x10. Argument0 of enqueue_sprite_attr_record. 全库无已有同值equate. |
| OAM_EQUIP_SPRITE_P2_11 | 0x00008011 | constants/oam_attr.inc | Nonzero-player sprite selector; the zero-player branch uses0x11. Argument0 of enqueue_sprite_attr_record. 全库无已有同值equate. |
| gP1LpTimer | 0x0201e1cc | constants/ewram.inc | Absolute u32 timer address, equal to gP1LifePoints+P1LP_TIMER_OFF; used for Final Countdown progress. 全库无已有同值equate. |

0x8002的TEXT_RENDER_FLAG_LAYER2定义域是text-render flag(`constants/duel_field.inc:133`), 本段0x0809e0a0..e0b2按player选择2/0x8002作为enqueue_sprite_attr_record的r0选择器. 该域已有同类OAM_EQUIP_SPRITE_P2_*常量. 因此新增OAM_EQUIP_SPRITE_P2_02, 不将文本layer flag用于sprite类型. 0x800e/0x8010/0x8011同样是非零player sprite选择器, 参数域均由调用寄存器和零player相邻分支证明.

0x135只命名为CARD_DISPLAY_OP31_PARAM_0135, 消费者0x0809e42c将其装入r1调用trigger_card_display_op31_if_not_active; 该callee0x08093390将输入转交dispatch_card_display_op(0x31,0,param,0), 不以数值臆定字符串/卡号. gP1LpTimer=0x0201c4e0+0x1cec=0x0201e1cc, 与既有P1LP_TIMER_OFF(`constants/ewram.inc:244`)一致; 名称不规定计时单位.

| REUSE名称 | 值 | 定义来源 | 本段次数 |
| --- | --- | --- | --- |
| PLAYER_BLOCK_STRIDE | 0x00000868 | constants/ewram.inc:251 | 11 |
| COCOON_OF_EVOLUTION_CID | 0x00000fee | constants/card_info.inc:852 | 1 |
| SWORDS_OF_REVEALING_LIGHT_CID | 0x00001102 | constants/card_info.inc:853 | 1 |
| CRUSH_CARD_CID | 0x0000123b | constants/card_info.inc:622 | 1 |
| TIMEATER_CID | 0x000013b1 | constants/card_info.inc:1972 | 1 |
| EKIBYO_DRAKMORD_CID | 0x0000149d | constants/card_info.inc:735 | 1 |
| SPIRITUAL_ENERGY_SETTLE_CID | 0x0000150e | constants/card_info.inc:571 | 1 |
| LAST_TURN_CID | 0x0000151e | constants/card_info.inc:1447 | 4 |
| FINAL_COUNTDOWN_CID | 0x0000169c | constants/card_info.inc:747 | 1 |
| DECK_DEVASTATION_VIRUS_CID | 0x0000188c | constants/card_info.inc:629 | 1 |
| PIKERU_SECOND_SIGHT_CID | 0x000018d5 | constants/card_info.inc:630 | 1 |
| POWER_BOND_CID | 0x000018fe | constants/card_info.inc:1795 | 1 |
| VWXYZ_DRAGON_CATAPULT_CANNON_CID | 0x00001954 | constants/card_info.inc:767 | 2 |
| P1LP_BLOCK2_OFF_1CE8 | 0x00001ce8 | constants/ewram.inc:276 | 3 |
| P1LP_TIMER_OFF | 0x00001cec | constants/ewram.inc:244 | 1 |
| P2LP_BLOCK2_OFF_1CF4 | 0x00001cf4 | constants/ewram.inc:277 | 3 |
| PUZZLE_READY_FLAG_OFF | 0x00001d04 | constants/ewram.inc:578 | 1 |
| CARD_PLAY_PHASE_CTR_OFF | 0x00001d1c | constants/ewram.inc:587 | 28 |
| EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 0x00001d24 | constants/duel_field.inc:605 | 7 |
| EQUIP_CHAIN_STEP_OFF | 0x00001d28 | constants/duel_field.inc:229 | 2 |
| EQUIP_CHAIN_CANCEL_OFF | 0x00001d30 | constants/duel_field.inc:566 | 4 |
| ELIGIB_STATE_CTRL_OFF | 0x00001d54 | constants/ewram.inc:419 | 2 |
| ELIGIB_ACT_COUNT_OFF | 0x00001d58 | constants/ewram.inc:420 | 1 |
| ELIGIB_ACT_TYPE_OFF | 0x00001d5c | constants/ewram.inc:421 | 1 |
| SPRITE_ATTR_DUEL_PHASE_P2 | 0x0000800b | constants/duel_field.inc:525 | 1 |
| OAM_EQUIP_SET_SLOT_P2 | 0x0000803b | constants/oam_attr.inc:67 | 2 |
| OAM_EQUIP_SPRITE_P2_46 | 0x00008046 | constants/oam_attr.inc:241 | 1 |
| gEquipLpScoreBase | 0x0201afe0 | constants/ewram.inc:557 | 1 |
| gP1LifePoints | 0x0201c4e0 | constants/ewram.inc:79 | 30 |
| gDuelFieldSlots | 0x0201c510 | constants/ewram.inc:314 | 5 |
| gDuelFieldSlotState | 0x0201c520 | constants/ewram.inc:318 | 1 |
| gDuelFieldSpellZoneBase | 0x0201c5ec | constants/ewram.inc:348 | 1 |
| gEquipNodePool | 0x0201d9c0 | constants/ewram.inc:316 | 1 |
| gDuelCardCtxBase | 0x0201e2a0 | constants/ewram.inc:218 | 4 |
| OAM_ATTR2_TILE_CLEAR | 0xffffe000 | constants/oam_attr.inc:24 | 1 |

基址/单位核对: PLAYER_BLOCK_STRIDE是byte stride, 所有相关field/chain访问为(masked player)*0x868; field entry stride为20 B, chain node stride为8 B. gDuelFieldSlots=LP+0x30, gDuelFieldSlotState=field+0x10, gDuelFieldSpellZoneBase=field+11*20. 节点池gEquipNodePool不加player stride. ctx选择word地址为gDuelCardCtxBase+8+4*player, 不将该地址误写ROM_TABLE.

三个0x1cf4槽复用P2LP_BLOCK2_OFF_1CF4, 定义源明确base=gP1LifePoints; 本段实际读取field phase并比较2/4或构造1<<phase, EOL如实描述. 同值FIELD_STATE_OFF定义base=gDuelFieldSlots, 采用它将文字指向不同绝对地址, 因此不选. 不修改既有P2LP_BLOCK2_OFF_1CF4的跨段定义. 0xfee复用COCOON_OF_EVOLUTION_CID, 不选同值动画sentinel. 0xffffe000复用既有低13位clear mask OAM_ATTR2_TILE_CLEAR; 本消费对象是slot halfword的CID, EOL明确保存/清除/恢复CID, 不把它解释为OAM attr2存储.

0x1d04复用PUZZLE_READY_FLAG_OFF但EOL限定本段事实: 仅阻止backup+1 notice, 不阻止backup+4. 0x1ce8只注明player word; 0x1d1c为本状态phase; 0x1d24是slot/callback scan cursor, 与callback表持久索引+0x1d20不同.

## CID / ROM证据 (R6)

17个去重CID: 15个池内CID值和2个由移位构造的立即数. 本地`data/card-stats.s`共35条对应记录, 每条记录CID均与ROM实读一致, 同时匹配卡名和password; data.md按五列解析, 只比较第四列逻辑Starter/Opponent CID, 不以行内任意匹配或卡表顺序号定位. ROM记录起点为0x098169b6+22*record_index, CID在+2. 下表给主记录和正确md行, 全部副记录见`f13-seg1-cids.json`.

| CID | 卡名 | password | 主record/ROM CID地址 | card-stats行 | data.md行 |
| --- | --- | --- | --- | --- | --- |
| 0x0fee | Cocoon of Evolution | 40240595 | 79 / 0x09817082 | 1042 | 87 |
| 0x1102 | Swords of Revealing Light | 72302403 | 308 / 0x09818430 | 4019 | 313 |
| 0x123b | Crush Card | 57728570 | 541 / 0x09819836 | 7048 | 538 |
| 0x1356 | Gamble | 37313786 | 759 / 0x0981aaf2 | 9882 | 746 |
| 0x13b1 | Timeater | 44913552 | 831 / 0x0981b122 | 10818 | 817 |
| 0x1400 | Nightmare's Steelcage | 58775978 | 875 / 0x0981b4ea | 11390 | 861 |
| 0x1401 | Infinite Cards | 94163677 | 876 / 0x0981b500 | 11403 | 862 |
| 0x149d | Ekibyo Drakmord | 69954399 | 987 / 0x0981be8a | 12846 | 973 |
| 0x150e | Spiritual Energy Settle Machine | 99173029 | 1081 / 0x0981c69e | 14068 | 1066 |
| 0x151e | Last Turn | 28566710 | 1093 / 0x0981c7a6 | 14224 | 1078 |
| 0x159f | Hieroglyph Lithograph | 10248192 | 1187 / 0x0981cfba | 15446 | 1171 |
| 0x169c | Final Countdown | 95308449 | 1384 / 0x0981e0a8 | 18007 | 1364 |
| 0x1800 | Enervating Mist | 26022485 | 1677 / 0x0981f9d6 | 21816 | 1657 |
| 0x188c | Deck Devastation Virus | 35027493 | 1803 / 0x098204aa | 23454 | 1782 |
| 0x18d5 | Pikeru's Second Sight | 58015506 | 1861 / 0x098209a6 | 24208 | 1839 |
| 0x18fe | Power Bond | 37630732 | 1887 / 0x09820be2 | 24546 | 1865 |
| 0x1954 | VWXYZ-Dragon Catapult Cannon | 84243274 | 1955 / 0x098211ba | 25430 | 1933 |

0x0809d938..0x0809d93a构造0xc0<<5=0x1800, 是Enervating Mist而非旧plate的0xc000; 0x1400由0xa0<<5构造, 是Nightmare's Steelcage. 两个仅用于验证即时消费者/plate, 不增加池槽或equate. 0x1954的VWXYZ身份同时支撑phase30与e5e0更名. 所有CID判断置信度high.

## 消费者证据与逐槽EOL (R6)

以下源行均针对baseline asm13. 每项列全部直接literal-load消费者, 配合所属函数全文覆盖数据流; 每项EOL就是fixer写入槽地址的ASCII全文. 所有EQ/REF/RENAME共142项在此再做地址序统一索引, 不增加第二套动作. 各项confidence=high; 新0x135参数名以已证实的op/参数值为边界, 不扩展未知语义.

| slot/旧标签 | 动作/输出名 | 直接消费者行 | EOL ASCII |
| --- | --- | --- | --- |
| 0x0809d758 DAT_0809d758 | EQ LAST_TURN_CID | 8 | CID for the Last Turn chain-membership or entity-value lookup. |
| 0x0809d77c DAT_0809d77c | EQ LAST_TURN_CID | 46 | CID for the Last Turn chain-membership or entity-value lookup. |
| 0x0809d7b4 DAT_0809d7b4 | EQ POWER_BOND_CID | 76 | CID for chain slot11 membership, entity lookup and sprite/LP-indicator submissions. |
| 0x0809d85c DAT_0809d85c | EQ PLAYER_BLOCK_STRIDE | 127 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809d860 DAT_0809d860 | REF gDuelFieldSpellZoneBase | 129 | Chain slot11 base, gDuelFieldSlots+11*20; read u16[base+(player&1)*stride+0xa] as the node-head index. |
| 0x0809d864 DAT_0809d864 | REF gEquipNodePool | 137 | Global 8-byte node pool indexed by chain-head/next indices; no player stride is added to this base. |
| 0x0809d868 DAT_0809d868 | EQ OAM_EQUIP_SET_SLOT_P2 | 151 | Nonzero-player counter-sprite selector; the zero-player branch uses0x3b. |
| 0x0809d87c DAT_0809d87c | EQ CRUSH_CARD_CID | 184 | CID argument for the chain counter-sprite wrapper. |
| 0x0809d890 DAT_0809d890 | EQ DECK_DEVASTATION_VIRUS_CID | 196 | CID argument for the chain counter-sprite wrapper. |
| 0x0809d8a4 DAT_0809d8a4 | EQ PIKERU_SECOND_SIGHT_CID | 208 | CID argument for the chain counter-sprite wrapper. |
| 0x0809d908 DAT_0809d908 | EQ FINAL_COUNTDOWN_CID | 223 | CID for chain slot11 entity lookup and progress-sprite arguments. |
| 0x0809d90c DAT_0809d90c | REF gP1LpTimer | 224 | Absolute u32 timer address, equal to gP1LifePoints+P1LP_TIMER_OFF; used for Final Countdown progress. |
| 0x0809d910 DAT_0809d910 | EQ OAM_EQUIP_SET_SLOT_P2 | 241 | Nonzero-player counter-sprite selector; the zero-player branch uses0x3b. |
| 0x0809d96c DAT_0809d96c | EQ INFINITE_CARDS_CID | 278 | CID passed to count_field_copies_of_card; nonzero count bypasses the hand-limit row update. |
| 0x0809d970 DAT_0809d970 | EQ HIEROGLYPH_LITHOGRAPH_CID | 283 | CID passed to check_value_in_slot_chain(player,11,CID); a hit raises the hand limit to7. |
| 0x0809d974 PTR_gP1LifePoints_0809d974 | RENAME gP1LifePoints | 302 | Player-state base; read the hand-count word at base+(player&1)*PLAYER_BLOCK_STRIDE+0xc. |
| 0x0809d978 DAT_0809d978 | EQ PLAYER_BLOCK_STRIDE | 305 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809d9cc PTR_gP1LifePoints_0809d9cc | RENAME gP1LifePoints | 341 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809d9d0 DAT_0809d9d0 | EQ P1LP_BLOCK2_OFF_1CE8 | 342 | Byte offset from gP1LifePoints to the player word used by this dispatcher. |
| 0x0809d9d4 DAT_0809d9d4 | EQ PLAYER_BLOCK_STRIDE | 348 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809d9d8 DAT_0809d9d8 | EQ CARD_PLAY_PHASE_CTR_OFF | 358 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809d9f4 PTR_gP1LifePoints_0809d9f4 | RENAME gP1LifePoints | 380 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809d9f8 DAT_0809d9f8 | EQ CARD_PLAY_PHASE_CTR_OFF | 381 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809d9fc PTR_switchdataD_0809da00_0809d9fc | REF switchD_0809d9f2__switchdataD_0809da00 | 389 | 21 even-address phase0..20 targets, dispatched by MOV pc,r0 while retaining Thumb state. |
| 0x0809da8c DAT_0809da8c | EQ OAM_EQUIP_SPRITE_P2_11 | 430 | Nonzero-player sprite selector; the zero-player branch uses0x11. Argument0 of enqueue_sprite_attr_record. |
| 0x0809da90 PTR_gP1LifePoints_0809da90 | RENAME gP1LifePoints | 437 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809da94 DAT_0809da94 | EQ CARD_PLAY_PHASE_CTR_OFF | 438 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809da98 DAT_0809da98 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 448 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809dab8 PTR_gP1LifePoints_0809dab8 | RENAME gP1LifePoints | 468 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809dabc DAT_0809dabc | EQ CARD_PLAY_PHASE_CTR_OFF | 469 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809db3c PTR_gP1LifePoints_0809db3c | RENAME gP1LifePoints | 480,495 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809db40 DAT_0809db40 | EQ CARD_PLAY_PHASE_CTR_OFF | 481 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809db44 DAT_0809db44 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 496 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809db48 DAT_0809db48 | EQ PLAYER_BLOCK_STRIDE | 509 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809db4c DAT_0809db4c | EQ COCOON_OF_EVOLUTION_CID | 539 | Compare with the low13 CID bits of a field-slot word; not the same-valued animation sentinel. |
| 0x0809db50 DAT_0809db50 | EQ SPIRITUAL_ENERGY_SETTLE_CID | 542 | CID comparison selecting the multi-step display path for field slots5..9. |
| 0x0809dbcc DAT_0809dbcc | REF gDuelCardCtxBase | 609 | Duel card context base; reads word[base+8+4*player] to select the display/AI route. |
| 0x0809dc98 PTR_gP1LifePoints_0809dc98 | RENAME gP1LifePoints | 679,690,702 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809dc9c DAT_0809dc9c | EQ CARD_PLAY_PHASE_CTR_OFF | 680 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809dca0 DAT_0809dca0 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 685,691 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809dca4 DAT_0809dca4 | EQ PLAYER_BLOCK_STRIDE | 709 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809dca8 DAT_0809dca8 | EQ SWORDS_OF_REVEALING_LIGHT_CID | 721 | CID comparison in the opposite-player slot5..9 scan. |
| 0x0809dd20 PTR_gP1LifePoints_0809dd20 | RENAME gP1LifePoints | 793 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809dd24 DAT_0809dd24 | EQ CARD_PLAY_PHASE_CTR_OFF | 794 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809dee0 DAT_0809dee0 | EQ PLAYER_BLOCK_STRIDE | 826,960 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809dee4 DAT_0809dee4 | REF gDuelFieldSlots | 831 | Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index. |
| 0x0809dee8 DAT_0809dee8 | EQ EKIBYO_DRAKMORD_CID | 837 | CID matched in field slots5..9 before pair lookup and eligibility checks. |
| 0x0809deec DAT_0809deec | REF gDuelFieldSlotState | 861 | Field-slot state-word base, gDuelFieldSlots+0x10; consumer tests bit5 with the same player/slot displacement. |
| 0x0809def0 DAT_0809def0 | EQ OAM_ATTR2_TILE_CLEAR | 887 | AND mask clearing low13 CID bits of a slot halfword before the eligibility call; the saved CID is restored afterward. |
| 0x0809def4 PTR_gP1LifePoints_0809def4 | RENAME gP1LifePoints | 936,947,957,1006,1020 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809def8 DAT_0809def8 | EQ CARD_PLAY_PHASE_CTR_OFF | 937,1007,1021 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809defc DAT_0809defc | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 942,948,1012 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809df00 DAT_0809df00 | EQ OAM_EQUIP_SPRITE_P2_46 | 984 | Nonzero-player sprite selector; the zero-player branch uses0x46. |
| 0x0809df80 PTR_gP1LifePoints_0809df80 | RENAME gP1LifePoints | 1047,1053,1068,1077,1099 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809df84 DAT_0809df84 | EQ CARD_PLAY_PHASE_CTR_OFF | 1048,1054,1100 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809df88 DAT_0809df88 | REF equip_activation_phase11_callbacks | 1075 | 34 Thumb callbacks, indexed by the persistent phase11 cursor; a callback returning0 yields for this tick. |
| 0x0809df8c DAT_0809df8c | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 1078,1110 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809dfd8 PTR_gP1LifePoints_0809dfd8 | RENAME gP1LifePoints | 1122,1144,1149 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809dfdc DAT_0809dfdc | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 1123 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809dfe0 DAT_0809dfe0 | REF equip_activation_phase12_callbacks | 1129 | 25 Thumb callbacks; phase12 restarts the local table index at0 on each tick and yields on callback result0. |
| 0x0809dfe4 DAT_0809dfe4 | EQ CARD_PLAY_PHASE_CTR_OFF | 1145 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e040 PTR_gP1LifePoints_0809e040 | RENAME gP1LifePoints | 1168,1198 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e044 DAT_0809e044 | REF equip_activation_phase20_callbacks | 1175 | 4 Thumb callbacks, indexed by the persistent phase20 cursor; a callback returning0 yields for this tick. |
| 0x0809e048 DAT_0809e048 | EQ EQUIP_ACTIVATION_SCAN_CURSOR_OFF | 1177 | Byte offset from gP1LifePoints to the u32 slot/callback scan cursor. |
| 0x0809e04c DAT_0809e04c | EQ CARD_PLAY_PHASE_CTR_OFF | 1199 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e094 PTR_gP1LifePoints_0809e094 | RENAME gP1LifePoints | 1251 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e098 DAT_0809e098 | EQ P1LP_BLOCK2_OFF_1CE8 | 1252 | Byte offset from gP1LifePoints to the player word used by this dispatcher. |
| 0x0809e09c DAT_0809e09c | EQ CARD_PLAY_PHASE_CTR_OFF | 1255 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e0d4 DAT_0809e0d4 | EQ OAM_EQUIP_SPRITE_P2_02 | 1274 | Nonzero-player sprite selector; the zero-player branch uses2. Argument0 of enqueue_sprite_attr_record. |
| 0x0809e0d8 DAT_0809e0d8 | REF gDuelCardCtxBase | 1280 | Duel card context base; reads word[base+8+4*player] to select the display/AI route. |
| 0x0809e0dc DAT_0809e0dc | REF gEquipLpScoreBase | 1287 | Base of the 0x1cc-byte zero-fill when the selected player context word equals1. |
| 0x0809e154 DAT_0809e154 | EQ GAMBLE_CID | 1304 | CID passed to check_value_in_slot_chain(player,11,CID). |
| 0x0809e158 DAT_0809e158 | EQ PUZZLE_READY_FLAG_OFF | 1315 | Byte offset from gP1LifePoints; a nonzero word suppresses only the backup+1 timer notice. |
| 0x0809e15c DAT_0809e15c | EQ P1LP_TIMER_OFF | 1320,1340 | Byte offset from gP1LifePoints to the u32 timer; offset+4 addresses its backup field. |
| 0x0809e160 DAT_0809e160 | EQ SPRITE_ATTR_DUEL_PHASE_P2 | 1332,1352 | Nonzero-player timer-notice sprite selector; the zero-player branch uses0xb. |
| 0x0809e164 PTR_gP1LifePoints_0809e164 | RENAME gP1LifePoints | 1339 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e1ac PTR_gP1LifePoints_0809e1ac | RENAME gP1LifePoints | 1378 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e1b0 DAT_0809e1b0 | EQ P1LP_BLOCK2_OFF_1CE8 | 1379 | Byte offset from gP1LifePoints to the player word used by this dispatcher. |
| 0x0809e1b4 DAT_0809e1b4 | EQ PLAYER_BLOCK_STRIDE | 1385 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809e1b8 DAT_0809e1b8 | EQ TIMEATER_CID | 1394 | CID passed to check_value_in_slot_chain(player,11,CID); saves its result as a phase gate. |
| 0x0809e1bc DAT_0809e1bc | EQ CARD_PLAY_PHASE_CTR_OFF | 1399 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e1c0 PTR_switchdataD_0809e1c4_0809e1c0 | REF switchD_0809e1aa__switchdataD_0809e1c4 | 1407 | 31 even-address phase0..30 targets, dispatched by MOV pc,r0 while retaining Thumb state. |
| 0x0809e260 PTR_gP1LifePoints_0809e260 | RENAME gP1LifePoints | 1457 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e264 DAT_0809e264 | EQ EQUIP_CHAIN_CANCEL_OFF | 1458 | Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases. |
| 0x0809e268 DAT_0809e268 | EQ CARD_PLAY_PHASE_CTR_OFF | 1468 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e290 DAT_0809e290 | EQ OAM_EQUIP_SPRITE_P2_0E | 1485 | Nonzero-player sprite selector; the zero-player branch uses0xe. Argument0 of enqueue_sprite_attr_record. |
| 0x0809e294 DAT_0809e294 | EQ ELIGIB_STATE_CTRL_OFF | 1491 | Byte offset from gP1LifePoints to the eligibility state-control word. |
| 0x0809e298 DAT_0809e298 | EQ CARD_PLAY_PHASE_CTR_OFF | 1494 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e2e0 PTR_gP1LifePoints_0809e2e0 | RENAME gP1LifePoints | 1508,1537 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e2e4 DAT_0809e2e4 | EQ CARD_PLAY_PHASE_CTR_OFF | 1519,1538 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e2e8 DAT_0809e2e8 | REF gDuelCardCtxBase | 1525 | Duel card context base; reads word[base+8+4*player] to select the display/AI route. |
| 0x0809e2fc PTR_gP1LifePoints_0809e2fc | RENAME gP1LifePoints | 1552 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e300 DAT_0809e300 | EQ CARD_PLAY_PHASE_CTR_OFF | 1553 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e324 PTR_gP1LifePoints_0809e324 | RENAME gP1LifePoints | 1562 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e328 DAT_0809e328 | EQ ELIGIB_STATE_CTRL_OFF | 1563 | Byte offset from gP1LifePoints to the eligibility state-control word. |
| 0x0809e32c DAT_0809e32c | EQ ELIGIB_ACT_COUNT_OFF | 1568 | Byte offset from gP1LifePoints; phase3 writes1 to the eligibility activation-count word. |
| 0x0809e330 DAT_0809e330 | EQ CARD_PLAY_PHASE_CTR_OFF | 1572 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e348 DAT_0809e348 | EQ ELIGIB_ACT_TYPE_OFF | 1587 | Byte offset from gP1LifePoints; phase3 compares activation type against16 and18. |
| 0x0809e36c DAT_0809e36c | EQ EQUIP_CHAIN_CANCEL_OFF | 1604 | Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases. |
| 0x0809e370 DAT_0809e370 | EQ EQUIP_CHAIN_STEP_OFF | 1607 | Byte offset from gP1LifePoints; this path clears the chain-step word before advancing phase. |
| 0x0809e374 DAT_0809e374 | EQ CARD_PLAY_PHASE_CTR_OFF | 1610 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e38c DAT_0809e38c | EQ CARD_PLAY_PHASE_CTR_OFF | 1626 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e3ac PTR_gP1LifePoints_0809e3ac | RENAME gP1LifePoints | 1635 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e3b0 DAT_0809e3b0 | EQ P2LP_BLOCK2_OFF_1CF4 | 1636 | Byte offset from gP1LifePoints; this consumer reads the field-phase word, not a gDuelFieldSlots-relative cursor. |
| 0x0809e3d8 PTR_gP1LifePoints_0809e3d8 | RENAME gP1LifePoints | 1666 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e3dc DAT_0809e3dc | EQ CARD_PLAY_PHASE_CTR_OFF | 1667 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e404 DAT_0809e404 | REF gDuelCardCtxBase | 1678 | Duel card context base; reads word[base+8+4*player] to select the display/AI route. |
| 0x0809e408 PTR_gP1LifePoints_0809e408 | RENAME gP1LifePoints | 1689 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e420 PTR_gP1LifePoints_0809e420 | RENAME gP1LifePoints | 1700 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e424 DAT_0809e424 | EQ CARD_PLAY_PHASE_CTR_OFF | 1707 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e438 DAT_0809e438 | EQ CARD_DISPLAY_OP31_PARAM_0135 | 1716 | Display op0x31 parameter, forwarded from r1 by trigger_card_display_op31_if_not_active. |
| 0x0809e43c PTR_gP1LifePoints_0809e43c | RENAME gP1LifePoints | 1719 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e440 DAT_0809e440 | EQ CARD_PLAY_PHASE_CTR_OFF | 1720 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e47c PTR_gP1LifePoints_0809e47c | RENAME gP1LifePoints | 1753 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e480 DAT_0809e480 | EQ CARD_PLAY_PHASE_CTR_OFF | 1754 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e498 PTR_gP1LifePoints_0809e498 | RENAME gP1LifePoints | 1763 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e4bc DAT_0809e4bc | EQ EQUIP_CHAIN_CANCEL_OFF | 1780 | Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases. |
| 0x0809e4c0 DAT_0809e4c0 | EQ EQUIP_CHAIN_STEP_OFF | 1784 | Byte offset from gP1LifePoints; this path clears the chain-step word before advancing phase. |
| 0x0809e4cc DAT_0809e4cc | EQ CARD_PLAY_PHASE_CTR_OFF | 1796 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e4dc PTR_gP1LifePoints_0809e4dc | RENAME gP1LifePoints | 1803 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e4e0 DAT_0809e4e0 | EQ CARD_PLAY_PHASE_CTR_OFF | 1804 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e504 PTR_gP1LifePoints_0809e504 | RENAME gP1LifePoints | 1814,1827 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e508 DAT_0809e508 | EQ P2LP_BLOCK2_OFF_1CF4 | 1815 | Byte offset from gP1LifePoints; this consumer reads the field-phase word, not a gDuelFieldSlots-relative cursor. |
| 0x0809e50c DAT_0809e50c | EQ CARD_PLAY_PHASE_CTR_OFF | 1828 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e540 PTR_gP1LifePoints_0809e540 | RENAME gP1LifePoints | 1842 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e544 DAT_0809e544 | EQ EQUIP_CHAIN_CANCEL_OFF | 1843 | Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases. |
| 0x0809e548 DAT_0809e548 | EQ OAM_EQUIP_SPRITE_P2_10 | 1851 | Nonzero-player sprite selector; the zero-player branch uses0x10. Argument0 of enqueue_sprite_attr_record. |
| 0x0809e54c DAT_0809e54c | EQ CARD_PLAY_PHASE_CTR_OFF | 1857 | Byte offset from gP1LifePoints to the dispatcher phase word. |
| 0x0809e5c4 PTR_gP1LifePoints_0809e5c4 | RENAME gP1LifePoints | 1870 | gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path. |
| 0x0809e5c8 DAT_0809e5c8 | EQ P2LP_BLOCK2_OFF_1CF4 | 1871 | Byte offset from gP1LifePoints; this consumer reads the field-phase word, not a gDuelFieldSlots-relative cursor. |
| 0x0809e5cc DAT_0809e5cc | EQ PLAYER_BLOCK_STRIDE | 1884 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809e5d0 DAT_0809e5d0 | REF gDuelFieldSlots | 1889 | Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index. |
| 0x0809e5d4 DAT_0809e5d4 | EQ VWXYZ_DRAGON_CATAPULT_CANNON_CID | 1894 | Compare with low13 CID bits of five field-slot words; this CID names VWXYZ-Dragon Catapult Cannon. |
| 0x0809e638 DAT_0809e638 | EQ PLAYER_BLOCK_STRIDE | 1955 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809e63c DAT_0809e63c | REF gDuelFieldSlots | 1960 | Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index. |
| 0x0809e640 DAT_0809e640 | EQ VWXYZ_DRAGON_CATAPULT_CANNON_CID | 1965 | Compare with low13 CID bits of five field-slot words; this CID names VWXYZ-Dragon Catapult Cannon. |
| 0x0809e684 DAT_0809e684 | EQ PLAYER_BLOCK_STRIDE | 2017 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809e688 DAT_0809e688 | REF gDuelFieldSlots | 2021 | Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index. |
| 0x0809e68c DAT_0809e68c | EQ LAST_TURN_CID | 2029 | CID for the Last Turn chain-membership or entity-value lookup. |
| 0x0809e6d4 DAT_0809e6d4 | EQ PLAYER_BLOCK_STRIDE | 2062 | Byte stride of player blocks; the consumer multiplies it by player&1. |
| 0x0809e6d8 DAT_0809e6d8 | REF gDuelFieldSlots | 2066 | Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index. |
| 0x0809e6dc DAT_0809e6dc | EQ LAST_TURN_CID | 2074 | CID for the Last Turn chain-membership or entity-value lookup. |

额外数据流核对: d7ec参数/筛选/计数见0x0809d822..d840; d8a8双方timer-entity+1及signed>19见0x0809d8c8..d8f4; d914低位player stride与hand-count读取见0x0809d94a..d962. d984两持久callback循环及局部循环见0x0809df08..e038. e078的0x1cc由0xe6<<1构造, zero_fill_by_halfword按字节长度处理, 不是0x1cc halfwords. e168两个switch的默认返回不同于d984, phase30经apply_equip_activation_with_id_lookup, e5e0经apply_equip_activation_via_packed_attr, plate不能混写. e654/e6a4仅检测low13 CID非零, 不是旧plate声称的bit9占用标志.

必要callee核对: `asm/02_text_lp_fieldspell.s:8072/8343/14165`内check_value_in_slot_chain/get_node_entity_id_in_slot/count_available_effect_zones; getter未命中返回-1, 不能满足entity==0. `set_lp_display_row_if_nonzero`@0x080a1ae8 (`asm/13_equip_placement.s:7674`)只验证其r0/r1输出契约, 不进入所属后段细化. `zero_fill_by_halfword`@0x080f4e74 (`asm/21_font_title_scene.s:1934`)证明byte长度. `trigger_card_display_op31_if_not_active`@0x08093390 (`asm/11_effect_slot_puzzletext.s:30566`)证明r1参数转交. 本段不改变上述callee的plate或函数名.

## §5.1登记

本段0项. 没有被引用块转入§5.1; 三个有真实base引用的表全部carve, 两个既有switch完整保留. 模块后续段裸块只在所属段评审时分类, 本提案不预登记.

R8: 本段无新增图形资产或调色板提取. sprite常量依据调用寄存器和相邻player分支确定, 不以图形外观推断用途.

## 自检和落地守卫 (R9/C13)

- 直接消费者自检必须拒绝纯注释行，按baseline真实指令地址和ROM Thumb halfword的`(opcode & 0xf800)==0x4800`解码，以`((addr+4)&~3)+((opcode&0xff)<<2)`确定literal目标；逐槽核对完整uses集合，142槽应精确对应170条真实LDR，不接受文本命中替代。Mode A实际运行记录见`f13-seg1-mode-a-check.json`。
- 自检输出`f13-seg1-selfcheck.json`; 静态预计导出见`f13-seg1-projected-segment.s.txt`和`f13-seg1-carve.s.txt`, 它们不是正式构建源. 全部142槽原值和194个word/4060字节完整覆盖对ROM核对; EQ解析值、REF地址、RENAME既有值逐项相同;63个fn+1及host切割前后字节相同.
- 15个旧PLATE按函数标签前连续comment逐字与snapshot比对并校验hash;15个新PLATE/142个新EOL全部ASCII, PLATE<=500. 新槽名合法且唯一, 正式源无同名冲突. 本段预计自动槽0, 裸块0, stale FUN/SUB/旧自动名Ghidra comment0, 所有原指令、32处对齐、52个switch word与段外代码保持.
- 原142槽DefinedData4, 85+8 EQ槽原refs/equates为空; RENAME30维持DEFAULT refs. 两个switch原引用精确升级, 表头同Symbol ID规范化. 63回调word与边界477ac的类型/odd引用原样. 原RAM definedData=None的两个目标始终None. 同址符号清单和每项prestate已写plan, dry必须逐项核对而非只核值.
- 15Function IDs/body/ranges/函数入口、原incoming和指令EOL不变;仅两Function name变化和15PLATE变化. 局部共享收尾标签、所有case Symbol ID、flow均不变. 不调用分析器扩体或createFunction. 目标现有USER LABEL复用, 新增全局先全库查名与同址alias.
- 正式源修改范围严格限定plan.formal_scope. 保留前模块未提交工作及既有export_post_banlists_tables.py修复. 三表carve和六registry tuple之外无额外段外文本; 生成器不改. 构建前后需独立检查asm12仅两个BL名变化, CSV仅两个name单元格.
- fixer在review PASS后实施: 验证备份/只读前态 -> dry -> 精确写入 -> 全量Ghidra导出/inject_modes/split -> export_all.py/build -> SHA1与fc字节验证 -> 保存后只读持久化check -> 原范围asm/ELF/ROM及C13独立验收. SHA1必须为9689337d6aac1ce9699ab60aac73fc2cfdccad9b. executor静态校验不替代build. 本会话禁止stage/commit.

## 求助

无未闭合low-confidence语义. 全部命名以本地消费者和ROM为依据; 状态字段采用已存在的base明确常量, 未知display参数只按已证实op和值命名.

## Executor Report: F13-Seg-1

- 槽: EQ=93 REF=19 RENAME=30 FUNC_RENAME=2 PLATE=15; 新槽EOL=142.
- carve=3 tables /63words /252 B; disasm=0; 段内裸块=0; §5.1=0.
- NEW equates=9; REUSE equate symbols=35; ROM新表头LABEL=3; switch原LABEL规范化=2.
- 求助: none. proposal及plan SHA256见最终selfcheck与executor交接, 避免文件内自引用hash.
