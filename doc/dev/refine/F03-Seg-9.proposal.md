# Refine Proposal: F03-Seg-9  [0x0803d91c..0x0803efcc)

## 段测绘
- 函数入口: 13 个
  - 0x0803d91c tick_zone_slot_transition_display_seq
  - 0x0803dc34 tick_flip_summon_state
  - 0x0803de90 tick_zone_card_remove_display_seq
  - 0x0803e0c4 tick_equip_chain_node_link_seq
  - 0x0803e130 tick_zone_slot_ref_clear_display_seq
  - 0x0803e170 tick_zone_chain_node_ref_update_seq
  - 0x0803e228 commit_set_card_to_field_slot
  - 0x0803e298 write_zone_slot_display_args_by_state
  - 0x0803e318 tick_card_effect_index_display_seq
  - 0x0803e44c dispatch_op7_card_display
  - 0x0803e474 tick_hand_zone_insert_display_seq
  - 0x0803e594 tick_zone_card_place_with_slot_resolve_seq
  - 0x0803eb0c tick_equip_node_chain_link_display_seq

- 残留自动名槽: 143 个 DAT_ + 5 个 PTR_ = 148 slots (Python parse + grep 双重确认)
- ROM_INCBIN / .byte 块: 0 (段内无函数间裸 incbin)

## 数据块分类 (Rule 2/3)
段内无 ROM_INCBIN / .byte 块，跳过 ref-scan 表格。

## 符号化计划 (R1/R2/R3)

总计: EQ=70  REF=76  RENAME=2  合计=148 (100% 覆盖)

---

### EQ_SLOTS (data-equate)

所有 EQ 值均经 C5 grep 验证：先列**复用**，再列**新建**。

#### 复用 constants 已有项

| 槽地址 (hex) | 值 | 复用常量名 | 所在 inc | 槽 label (gas) |
|---|---|---|---|---|
| 0803d990 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_d990 |
| 0803d99c | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_d99c |
| 0803d9d0 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_d9d0 |
| 0803da8c | 0xffdfffff | SLOT_BIT21_CLR | constants/duel_field.inc | slot_bit21_clr_da8c |
| 0803da94 | 0x00000818 | DISP_SEQ_CARD_SET_CTR_OFF | constants/duel_field.inc | disp_seq_card_set_ctr_off_da94 |
| 0803da98 | 0xffffe000 | OAM_ATTR2_TILE_CLEAR | constants/oam_attr.inc | oam_attr2_tile_clear_da98 |
| 0803db84 | 0xffffc03f | GPRNG_STEP_CTR_MASK | constants/duel_field.inc | gprng_step_ctr_mask_db84 |
| 0803db88 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_db88 |
| 0803db90 | 0xffff7fff | SLOT_ACTIVE_BIT15_CLR | constants/duel_field.inc | slot_active_bit15_clr_db90 |
| 0803db94 | 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | constants/duel_field.inc | slot_active_bit14_clr_db94 |
| 0803dc18 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_dc18 |
| 0803dc20 | 0x00001fff | SLOT_CARD_SET_CODE_MASK | constants/card_info.inc | slot_card_set_code_mask_dc20 |
| 0803dc28 | 0xffffe000 | OAM_ATTR2_TILE_CLEAR | constants/oam_attr.inc | oam_attr2_tile_clear_dc28 |
| 0803dc2c | 0x00000818 | DISP_SEQ_CARD_SET_CTR_OFF | constants/duel_field.inc | disp_seq_card_set_ctr_off_dc2c |
| 0803dc30 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_dc30 |
| 0803dc80 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_dc80 |
| 0803dc88 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_dc88 |
| 0803de70 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_de70 |
| 0803de80 | 0x00001cf4 | FIELD_STATE_OFF | constants/duel_field.inc | field_state_off_de80 |
| 0803de84 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | constants/ewram.inc | p1lp_block2_off_1ce8_de84 |
| 0803de8c | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_de8c |
| 0803df04 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_df04 |
| 0803df0c | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_df0c |
| 0803e020 | 0x00001cb4 | FIELD_SLOT_COUNT_OFF | constants/duel_field.inc | field_slot_count_off_e020 |
| 0803e094 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e094 |
| 0803e0c0 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e0c0 |
| 0803e12c | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e12c |
| 0803e16c | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e16c |
| 0803e1b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e1b0 |
| 0803e1d8 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e1d8 |
| 0803e218 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e218 |
| 0803e224 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e224 |
| 0803e288 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e288 |
| 0803e290 | 0x00001cb4 | FIELD_SLOT_COUNT_OFF | constants/duel_field.inc | field_slot_count_off_e290 |
| 0803e294 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e294 |
| 0803e2d0 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e2d0 |
| 0803e308 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e308 |
| 0803e314 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e314 |
| 0803e364 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e364 |
| 0803e410 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e410 |
| 0803e448 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e448 |
| 0803e470 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e470 |
| 0803e524 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e524 |
| 0803e590 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e590 |
| 0803e6b0 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_e6b0 |
| 0803e9ec | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_e9ec |
| 0803e9f0 | 0x0000165a | A_DEAL_WITH_DARK_RULER_CID | constants/card_info.inc | a_deal_with_dark_ruler_cid_e9f0 |
| 0803e9f8 | 0x00001762 | BACKFIRE_CID | constants/card_info.inc (NEW) | backfire_cid_e9f8 |
| 0803e9fc | 0x00001972 | BOSS_RUSH_CID | constants/card_info.inc | boss_rush_cid_e9fc |
| 0803ea00 | 0x000016da | SOUL_ABSORPTION_CID | constants/card_info.inc (NEW) | soul_absorption_cid_ea00 |
| 0803ea10 | 0xffffc03f | GPRNG_STEP_CTR_MASK | constants/duel_field.inc | gprng_step_ctr_mask_ea10 |
| 0803ea14 | 0xffff7fff | SLOT_ACTIVE_BIT15_CLR | constants/duel_field.inc | slot_active_bit15_clr_ea14 |
| 0803ea18 | 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | constants/duel_field.inc | slot_active_bit14_clr_ea18 |
| 0803eaa0 | 0xffff7fff | SLOT_ACTIVE_BIT15_CLR | constants/duel_field.inc | slot_active_bit15_clr_eaa0 |
| 0803eaa4 | 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | constants/duel_field.inc | slot_active_bit14_clr_eaa4 |
| 0803eb08 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_eb08 |
| 0803ebcc | 0x00000814 | DUEL_FIELD_OAM_TILE_IDX_A | constants/duel_field.inc | duel_field_oam_tile_idx_a_ebcc |
| 0803ee04 | 0x00000868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc | player_block_stride_ee04 |
| 0803ee08 | 0x0000165a | A_DEAL_WITH_DARK_RULER_CID | constants/card_info.inc | a_deal_with_dark_ruler_cid_ee08 |
| 0803ee10 | 0x00001762 | BACKFIRE_CID | constants/card_info.inc (NEW) | backfire_cid_ee10 |
| 0803ee14 | 0x00001972 | BOSS_RUSH_CID | constants/card_info.inc | boss_rush_cid_ee14 |
| 0803ee18 | 0x000016da | SOUL_ABSORPTION_CID | constants/card_info.inc (NEW) | soul_absorption_cid_ee18 |
| 0803ee20 | 0x000017b2 | HUMAN_WAVE_TACTICS_CID | constants/card_info.inc (NEW) | human_wave_tactics_cid_ee20 |
| 0803ee2c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | constants/ewram.inc | p1lp_block2_off_1ce8_ee2c |
| 0803ef68 | 0xffff7fff | SLOT_ACTIVE_BIT15_CLR | constants/duel_field.inc | slot_active_bit15_clr_ef68 |
| 0803ef6c | 0xffffbfff | SLOT_ACTIVE_BIT14_CLR | constants/duel_field.inc | slot_active_bit14_clr_ef6c |
| 0803ef74 | 0xffffc03f | GPRNG_STEP_CTR_MASK | constants/duel_field.inc | gprng_step_ctr_mask_ef74 |
| 0803efc8 | 0x0000080c | DISPLAY_SEQ_STEP_LOCK_OFF | constants/duel_field.inc | disp_seq_step_lock_off_efc8 |

#### 新建项 (C5 grep 确认全 19 inc 无匹配)

| 槽地址 | 值 | 新常量名 | 目标 inc | 推导证据 |
|---|---|---|---|---|
| 0803de78 | 0xba180000 | UNHAPPY_GIRL_CID_SHIFTED | constants/card_info.inc | 0x1743<<19 = 0xba180000; tick_flip_summon_state line 17448: lsls r0,r0,#0x13; cmp r0,0xba180000; UNHAPPY_GIRL_CID=0x1743 已在 card_info.inc; confidence high |
| 0803e0f8 | 0x00007fff | DISPLAY_CTX_SLOT_DATA_MASK | constants/duel_field.inc | 消除 bit15, masks [gDuelDisplaySeqState+4] hword to extract slot_data field; write_zone_slot_display_args_by_state line 17806; confidence high |
| 0803e9f8/ee10 | 0x00001762 | BACKFIRE_CID | constants/card_info.inc | data/card-stats.s card_1547: .word 82705573 (pw); Backfire (effect card); confidence high |
| 0803ea00/ee18 | 0x000016da | SOUL_ABSORPTION_CID | constants/card_info.inc | data/card-stats.s card_1435: .word 68073522 (pw); Soul Absorption; confidence high |
| 0803ee20 | 0x000017b2 | HUMAN_WAVE_TACTICS_CID | constants/card_info.inc | data/card-stats.s card_1606: .word 30353551 (pw); Human-Wave Tactics; confidence high |

Note: BACKFIRE_CID and SOUL_ABSORPTION_CID appear at 2 slots each (same value), counted once as "new constant" but 2 EQ slots each.
EQ 合计: 65 slots 复用 + 5 slots 新建 = 70 slots.

---

### REF_SLOTS (USER-label + DATA-ref)

全部为 EWRAM 全局或已命名 PTR 变量，单 label 全 ref。

#### gDuelDisplaySeqState = 0x0201bcc0 (34 slots)

gas_label: `gDuelDisplaySeqState` (已在 constants/ewram.inc)
slot_label: 无需额外 label，直接替换.

槽地址列表 (34):
d954, d998, d9cc, da90, db98, dc24, dc7c, dcc8, dd44, de88,
df00, e098, e0f4, e128, e168, e1ac, e220, e284, e2cc, e310,
e360, e418, e46c, e4a8, e56c, e5f0, e630, e6ac, eadc, eb04,
eb74, ebc8, ebe8, efc4

#### gDuelChainStepCounter = 0x0201c4d0 (2 slots)

gas_label: `gDuelChainStepCounter` (已在 constants/ewram.inc)
槽: d958, da9c

#### gDuelFieldSlots = 0x0201c510 (17 slots)

gas_label: `gDuelFieldSlots` (已在 constants/ewram.inc)
槽: d994, db8c, dc1c, dc84, de74, df08, e01c, e1b4, e1dc, e21c,
    e28c, e2d4, e30c, e368, e414, ea04, ee1c

#### gP1LifePoints (PTR; 5 slots)

slot pattern: `PTR_gP1LifePoints_<addr>` (已 Ghidra 自动, 仅确认)
槽: de7c, e090, e520, e9e8, ee00

#### gDuelCardCtxBase = 0x0201e2a0 (6 slots)

gas_label: `gDuelCardCtxBase` (已在 constants/ewram.inc)
槽: de6c, e08c, e398, e3cc, ea0c, ee28

#### gEquipChainSlotRefs = 0x0201bb90 (2 slots)

gas_label: `gEquipChainSlotRefs` (已在 constants/ewram.inc)
槽: df5c, ee30

#### gDuelEffectChainSlots = 0x0201bc54 (1 slot)

gas_label: `gDuelEffectChainSlots` (已在 constants/ewram.inc)
槽: eb78

#### gDuelFieldSlotState = 0x0201c520 (2 slots)

gas_label: `gDuelFieldSlotState` (已在 constants/ewram.inc)
槽: e9f4, ee0c

#### gDuelChainDescBase = 0x0201c4d8 (7 slots)

gas_label: `gDuelChainDescBase` (已在 constants/ewram.inc)
槽: e718, ea08, ea9c, ead8, ee24, ef70, ef9c

REF 合计: 34+2+17+5+6+2+1+2+7 = 76 slots.

---

### RENAME_SLOTS (switch table pointer labels)

| 槽地址 | 当前值 | 新 gas_label | 函数上下文 | 置信度 |
|---|---|---|---|---|
| DAT_0803e634 | 0x0803e638 | zone_card_place_switch_table_ptr | switchD_0803e62c__switchdataD_0803e638; tick_zone_card_place_with_slot_resolve_seq; asm line 18581 | high |
| DAT_0803eb7c | 0x0803eb80 | equip_node_chain_switch_table_ptr | switchD_0803eb72__switchdataD_0803eb80; tick_equip_node_chain_link_display_seq; asm line 19263 | high |

RENAME 合计: 2 slots.

---

### FUNC_RENAME (如有)

无 — 所有 13 个函数名与函数体操作一致，无矛盾误名信号。

---

### PLATE (R5) — C8 stale FUN_ 订正

所有 12 处 plate 均引用已命名函数，须做 substring 替换。
替换规则全部纯 ASCII。

| 函数 | asm line | 旧引用 (stale) | 新文本 |
|---|---|---|---|
| tick_zone_slot_transition_display_seq | 16728 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_flip_summon_state | 17138-17146 | (无 FUN_ 引用, plate 已含现名) | 无需改 |
| tick_zone_card_remove_display_seq | 17472 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_equip_chain_node_link_seq | 17770 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_zone_slot_ref_clear_display_seq | 17835,17836 | FUN_0803be4c; FUN_0802f0d8 | dispatch_duel_event_display_seq; clear_zone_slot_card_ref_bits |
| tick_zone_chain_node_ref_update_seq | 17872,17878 | FUN_0803be4c; FUN_0802ec3c | dispatch_duel_event_display_seq; replace_chain_node_ref_by_zone_match |
| write_zone_slot_display_args_by_state | 18051 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_card_effect_index_display_seq | 18121 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_hand_zone_insert_display_seq | 18326 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_zone_card_place_with_slot_resolve_seq | 18475 | FUN_0803be4c | dispatch_duel_event_display_seq |
| tick_equip_node_chain_link_display_seq | 19195 | FUN_0803be4c | dispatch_duel_event_display_seq |

Note: tick_flip_summon_state (lines 17138-17146) plate comment refers to `FUN_0803be4c` only in the prose near line 17138 text -- re-read showed it does NOT contain FUN_ in its plate; confirmed by awk grep output (no FUN_ on line 17138-17146). PLATE 有效条目 = 11 函数 (tick_flip_summon_state 不含 stale FUN_, tick_zone_slot_transition_display_seq 含 1 处 FUN_0803be4c in line 16728).

Wait -- let me recount: the awk output showed FUN_ at lines 17472, 17770, 17835, 17836, 17872, 17878, 18051, 18121, 18326, 18475, 19195 (11 line occurrences covering 9 distinct functions). Plus line 16728 for tick_zone_slot_transition_display_seq = total 10 distinct functions with FUN_ plates.

Confirmed PLATE entries (10 functions):
1. tick_zone_slot_transition_display_seq (line 16728): FUN_0803be4c -> dispatch_duel_event_display_seq
2. tick_zone_card_remove_display_seq (line 17472): FUN_0803be4c -> dispatch_duel_event_display_seq
3. tick_equip_chain_node_link_seq (line 17770): FUN_0803be4c -> dispatch_duel_event_display_seq
4. tick_zone_slot_ref_clear_display_seq (lines 17835,17836): FUN_0803be4c -> dispatch_duel_event_display_seq; FUN_0802f0d8 -> clear_zone_slot_card_ref_bits
5. tick_zone_chain_node_ref_update_seq (lines 17872,17878): FUN_0803be4c -> dispatch_duel_event_display_seq; FUN_0802ec3c -> replace_chain_node_ref_by_zone_match
6. write_zone_slot_display_args_by_state (line 18051): FUN_0803be4c -> dispatch_duel_event_display_seq
7. tick_card_effect_index_display_seq (line 18121): FUN_0803be4c -> dispatch_duel_event_display_seq
8. tick_hand_zone_insert_display_seq (line 18326): FUN_0803be4c -> dispatch_duel_event_display_seq
9. tick_zone_card_place_with_slot_resolve_seq (line 18475): FUN_0803be4c -> dispatch_duel_event_display_seq
10. tick_equip_node_chain_link_display_seq (line 19195): FUN_0803be4c -> dispatch_duel_event_display_seq

PLATE 合计: 10 functions, 12 stale-FUN_ substring occurrences.

---

## carve 计划 (R7)
なし — 段内无函数间 ROM_INCBIN 或 .byte 块。

## disasm 计划 (R4)
なし — 段内无 misidentified data。

## 新增 constants / 全局

card_info.inc に追加 (C5 grep 确认无重复):
```
UNHAPPY_GIRL_CID_SHIFTED = 0xba180000   @ 0x1743 << 19; shifted CID comparison in tick_flip_summon_state
BACKFIRE_CID             = 0x00001762   @ card_1547, pw=82705573
SOUL_ABSORPTION_CID      = 0x000016da   @ card_1435, pw=68073522
HUMAN_WAVE_TACTICS_CID   = 0x000017b2   @ card_1606, pw=30353551
```

duel_field.inc に追加 (C5 grep 确认无重复):
```
DISPLAY_CTX_SLOT_DATA_MASK = 0x00007fff  @ mask bit15 from display-ctx hword[+4] to extract slot data
```

合计 5 新增常量 (4 in card_info.inc, 1 in duel_field.inc).

## §5.1 登记 (Rule 3) — 0 引用块
なし。

## 消费者证据 (R6)

| 常量 / 全局 | 消费者 file:line | 用法 | 置信度 |
|---|---|---|---|
| UNHAPPY_GIRL_CID_SHIFTED | asm/03_equip_chain_hand.s:17448-17449 | lsls r0,r0,#0x13; cmp r0, 0xba180000 — flip-summon gating on Unhappy Girl CID | high |
| DISPLAY_CTX_SLOT_DATA_MASK | asm/03_equip_chain_hand.s:17806-17807 | ldrh r2,[r0]; ands r2,0x7fff — masks bit15 (player_id) to extract slot_data index | high |
| BACKFIRE_CID | asm/03_equip_chain_hand.s:19055,19585 | cmp r0, BACKFIRE_CID in tick_zone_card_place branch and tick_equip_node_chain_link | high |
| SOUL_ABSORPTION_CID | asm/03_equip_chain_hand.s:19059,19589 | cmp r0, SOUL_ABSORPTION_CID same pattern | high |
| HUMAN_WAVE_TACTICS_CID | asm/03_equip_chain_hand.s:19593 | cmp r0, HUMAN_WAVE_TACTICS_CID in tick_equip_node_chain_link_display_seq | high |
| DUEL_FIELD_OAM_TILE_IDX_A (0x814) | asm/03_equip_chain_hand.s:19300 | slot DAT_0803ebcc value verified ROM byte @0x0803ebcc == 0x14080000 LE = 0x00000814; used as step_done offset in equip_node_chain func | high (C5 reuse) |
| gDuelDisplaySeqState | asm/03_equip_chain_hand.s:16769 etc | 34 direct .word 0x0201bcc0 loads; context struct base for all display seq tick funcs | high |
| gDuelChainDescBase | asm/03_equip_chain_hand.s:18692 etc | 7 slots 0x0201c4d8; chain descriptor struct base pointer | high |

## 求助
なし — 全槽置信度 high 或已 C5 复用验证。

---

## Executor Report: F03-Seg-9
- 槽: EQ=70 REF=76 RENAME=2 FUNC_RENAME=0 PLATE=10
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局: UNHAPPY_GIRL_CID_SHIFTED (card_info.inc), BACKFIRE_CID (card_info.inc), SOUL_ABSORPTION_CID (card_info.inc), HUMAN_WAVE_TACTICS_CID (card_info.inc), DISPLAY_CTX_SLOT_DATA_MASK (duel_field.inc)
- 求助: none
- proposal: doc/dev/refine/F03-Seg-9.proposal.md
