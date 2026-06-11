# Refine Proposal: F03Seg3  [0x08037128..0x08037904)

## 段测绘

- 函数入口 x13:
  - 0x08037128 count_graveyard_entries_by_card_id
  - 0x08037174 remove_slot_by_index_from_graveyard_arrays
  - 0x0803720c erase_slot_from_graveyard_arrays_by_ptr
  - 0x0803727c remove_slot_from_field_array_by_player
  - 0x0803730c count_hand_cards_with_field5
  - 0x0803735c count_graveyard_normal_summon_cards
  - 0x080373ac count_zone_slots_with_card_field5
  - 0x08037434 check_zone_slot_equip_eligible
  - 0x08037568 check_zone_slot_equip_eligible_alt
  - 0x08037630 place_equip_card_if_type_matches
  - 0x080376a0 erase_slot_from_field_array_c_by_ptr
  - 0x080377b0 eval_equip_bonus_for_slot
  - 0x08037894 find_field_zone_slot_with_fieldspell
  - 注: 0x0803777c 处存在一个无 label 的 THUMB 函数体 (非 push/pop 封装, 以 bx lr 结尾),
    被 eval_equip_bonus_for_slot (0x080377b0) 和 eval_equip_chain_score_for_slot (Seg-4)
    以 fn-ptr (0x0803777d) 引用. Ghidra 未拆分为独立函数, 需在 Seg-3 内补 label.

- 残留自动名槽 x49:
  - DWORD_0803716c = gP1LifePoints (0x0201c4e0)
  - DWORD_08037170 = PLAYER_BLOCK_STRIDE (0x868)
  - DAT_080371f8 = 0x868
  - DAT_08037260 = 0x868
  - DAT_08037308 = 0x868
  - DAT_08037358 = 0x868
  - DAT_080373a8 = 0x868
  - DAT_08037430 = 0x868  (x2 refs in count_zone_slots_with_card_field5)
  - DAT_0803748c = 0x868
  - DAT_08037490 = gP1HandSlotArray (0x0201c8f8)
  - DAT_08037494 = 0x14fc  (Gradius' Option)
  - DAT_080374a4 = 0x1414  (Gradius)
  - DAT_080374dc = 0x868
  - DAT_080374e0 = 0x12f3  (Ultimate Offering)
  - DAT_0803750c = 0x15b4  (XYZ-Dragon Cannon)
  - DAT_08037520 = 0x1571  (Helpoemer)
  - DAT_08037540 = 0x17c8  (Sphinx Teleia)
  - DAT_08037544 = 0x15fa  (YZ-Tank Dragon)
  - DAT_080375c0 = 0x868
  - DAT_080375c4 = gP1AltHandSlotArray (0x0201cab0)
  - DAT_080375c8 = 0x14fc  (Gradius' Option, duplicate of 0x08037494)
  - DAT_080375d8 = 0x1414  (Gradius, duplicate of 0x080374a4)
  - DAT_08037610 = 0x868
  - DAT_08037614 = 0x12f3  (Ultimate Offering, duplicate)
  - DAT_08037688 = 0x868
  - DAT_08037750 = 0x868  (x3 refs in erase_slot_from_field_array_c_by_ptr)
  - DAT_08037754 = 0x0201c600  (gP1LP+0x120 = field array C base, NEW global)
  - DAT_08037758 = 0xfffffeec  (neg offset field_array_C -> count, NEW constant)
  - DAT_080377a8 = 0x18d9  (Level Conversion Lab)
  - DAT_080377ac = 0x0fff  (mask bits[11:0])
  - DAT_08037884 = 0x0803777d  (THUMB fn-ptr to unnamed fn at 0x0803777c)
  - DAT_08037888 = 0x868
  - DAT_0803788c = 0x150b  (A Legendary Ocean -- EXISTING A_LEGENDARY_OCEAN_CARD_ID)
  - DAT_08037890 = 0x15c7  (Cost Down)
  - DAT_080378dc = 0x868
  - DAT_080378e0 = 0x0201c600  (field array C base, duplicate)
  - DAT_08037900 = 0x868
  - PTR_gP1LifePoints_080371f4 = gP1LifePoints
  - PTR_gP1LifePoints_0803725c = gP1LifePoints
  - PTR_gP1LifePoints_08037304 = gP1LifePoints
  - PTR_gP1LifePoints_08037354 = gP1LifePoints
  - PTR_gP1LifePoints_080373a4 = gP1LifePoints
  - PTR_gP1LifePoints_0803742c = gP1LifePoints
  - PTR_gP1LifePoints_080374d8 = gP1LifePoints
  - PTR_gP1LifePoints_0803760c = gP1LifePoints
  - PTR_gP1LifePoints_08037684 = gP1LifePoints
  - PTR_gP1LifePoints_0803774c = gP1LifePoints
  - PTR_gP1LifePoints_080377e0 = gP1LifePoints
  - PTR_gP1LifePoints_080378d8 = gP1LifePoints

- ROM_INCBIN / .byte 块: 0 块 (Seg-3 无 incbin; 仅有 14 处 .zero 0x2 对齐 padding, 无需处理)

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

Seg-3 无 ROM_INCBIN 或 .byte 块, 无需 Rule 2/3 分类. 所有 .zero 0x2 为函数间 2-byte 对齐 pad, 不构成独立数据块.

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|----|--------------------------|------|------|
| (无独立数据块) | N/A | N/A | 无 ROM_INCBIN; .zero 0x2 为对齐 pad |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

所有 EQ 槽按值去重. 消费者证据见 §消费者证据.

**注**: EQ_SLOT 的 Ghidra 槽 label 名须 != `.equ` 常量名, 须用 `<func>_<const>` 式.

#### 复用现有常量 (ewram.inc / duel_field.inc / card_info.inc)

| 槽 | ROM addr | value | 复用 const | slot_label (Ghidra) |
|----|----------|-------|------------|---------------------|
| DWORD_0803716c | 0x0803716c | 0x0201c4e0 | `gP1LifePoints` (ewram.inc) | count_graveyard_entries_by_card_id_lp_ptr |
| DWORD_08037170 | 0x08037170 | 0x00000868 | `PLAYER_BLOCK_STRIDE` (ewram.inc) | count_graveyard_entries_by_card_id_stride |
| DAT_080371f8 | 0x080371f8 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | remove_slot_by_index_from_gy_stride |
| DAT_08037260 | 0x08037260 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | erase_slot_from_gy_by_ptr_stride |
| DAT_08037308 | 0x08037308 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | remove_slot_from_field_arr_stride |
| DAT_08037358 | 0x08037358 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | count_hand_cards_field5_stride |
| DAT_080373a8 | 0x080373a8 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | count_gy_normal_summon_stride |
| DAT_08037430 | 0x08037430 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | count_zone_slots_field5_stride |
| DAT_0803748c | 0x0803748c | 0x00000868 | `PLAYER_BLOCK_STRIDE` | check_zone_slot_equip_elig_stride |
| DAT_08037490 | 0x08037490 | 0x0201c8f8 | `gP1HandSlotArray` (ewram.inc) | check_zone_slot_equip_elig_zone_base |
| DAT_080374dc | 0x080374dc | 0x00000868 | `PLAYER_BLOCK_STRIDE` | check_zone_slot_equip_elig_stride_b |
| DAT_080375c0 | 0x080375c0 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | check_zone_slot_equip_elig_alt_stride |
| DAT_080375c4 | 0x080375c4 | 0x0201cab0 | `gP1AltHandSlotArray` (ewram.inc) | check_zone_slot_equip_elig_alt_zone_base |
| DAT_080375c8 | 0x080375c8 | 0x00014fc  | `GRADIUS_OPTION_CID` (新建, 见下) | check_zone_slot_equip_elig_alt_gradius_opt_cid |
| DAT_080375d8 | 0x080375d8 | 0x00001414 | `GRADIUS_CID` (新建, 见下) | check_zone_slot_equip_elig_alt_gradius_cid |
| DAT_08037610 | 0x08037610 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | check_zone_slot_equip_elig_alt_stride_b |
| DAT_08037614 | 0x08037614 | 0x000012f3 | `ULTIMATE_OFFERING_CID` (新建, 见下) | check_zone_slot_equip_elig_alt_ult_off_cid |
| DAT_08037688 | 0x08037688 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | place_equip_card_if_type_stride |
| DAT_08037750 | 0x08037750 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | erase_slot_from_field_arr_c_stride |
| DAT_08037888 | 0x08037888 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | eval_equip_bonus_for_slot_stride |
| DAT_0803788c | 0x0803788c | 0x0000150b | `A_LEGENDARY_OCEAN_CARD_ID` (card_info.inc) | eval_equip_bonus_for_slot_a_leg_ocean_cid |
| DAT_080378dc | 0x080378dc | 0x00000868 | `PLAYER_BLOCK_STRIDE` | find_field_zone_slot_fieldspell_stride |
| DAT_08037900 | 0x08037900 | 0x00000868 | `PLAYER_BLOCK_STRIDE` | find_field_zone_slot_fieldspell_stride_b |
| DAT_080377ac | 0x080377ac | 0x00000fff | `SCENE_SLOT_MASK_LO` (duel_field.inc) | check_level_conv_lab_node_match_mask |

#### 复用新建 card_info.inc 常量 (Seg-3 多处复用)

| 槽 | ROM addr | value | const_name (card_info.inc) | slot_label |
|----|----------|-------|---------------------------|------------|
| DAT_08037494 | 0x08037494 | 0x000014fc | `GRADIUS_OPTION_CID` | check_zone_slot_equip_elig_gradius_opt_cid |
| DAT_080374a4 | 0x080374a4 | 0x00001414 | `GRADIUS_CID` | check_zone_slot_equip_elig_gradius_cid |
| DAT_080374e0 | 0x080374e0 | 0x000012f3 | `ULTIMATE_OFFERING_CID` | check_zone_slot_equip_elig_ult_off_cid |
| DAT_0803750c | 0x0803750c | 0x000015b4 | `XYZ_DRAGON_CANNON_CID` | check_zone_slot_equip_elig_xyz_cid |
| DAT_08037520 | 0x08037520 | 0x00001571 | `HELPOEMER_CID` | check_zone_slot_equip_elig_helpoemer_cid |
| DAT_08037540 | 0x08037540 | 0x000017c8 | `SPHINX_TELEIA_CID` | check_zone_slot_equip_elig_sphinx_teleia_cid |
| DAT_08037544 | 0x08037544 | 0x000015fa | `YZ_TANK_DRAGON_CID` | check_zone_slot_equip_elig_yz_tank_cid |
| DAT_080377a8 | 0x080377a8 | 0x000018d9 | `LEVEL_CONVERSION_LAB_CID` | check_level_conv_lab_node_match_cid |
| DAT_08037890 | 0x08037890 | 0x000015c7 | `COST_DOWN_CID` | eval_equip_bonus_for_slot_cost_down_cid |

#### 新建 ewram.inc 常量

| 槽 | ROM addr | value | const_name (ewram.inc) | slot_label |
|----|----------|-------|------------------------|------------|
| DAT_08037754 | 0x08037754 | 0x0201c600 | `gP1FieldArrayCBase` | erase_slot_from_field_arr_c_base |
| DAT_080378e0 | 0x080378e0 | 0x0201c600 | `gP1FieldArrayCBase` (复用) | find_field_zone_slot_fieldspell_base |

#### 新建 duel_field.inc 常量

| 槽 | ROM addr | value | const_name (duel_field.inc) | slot_label |
|----|----------|-------|-----------------------------|------------|
| DAT_08037758 | 0x08037758 | 0xfffffeec | `FIELD_ARRAY_C_TO_COUNT_NEG_OFF` | erase_slot_from_field_arr_c_neg_off |

### REF_SLOTS (USER-label + DATA-ref)

#### PTR_gP1LifePoints_* -> gP1LifePoints (ewram.inc)

所有 12 个 PTR_gP1LifePoints_XXXXXXXX 槽均持 gP1LifePoints=0x0201c4e0, ROM 已验证.
RENAME 为 `<func>_lp_ptr` 模式, Ghidra label 使用 `.word gP1LifePoints`.

| 槽 | addr | 所在函数 | slot_label |
|----|------|----------|------------|
| PTR_gP1LifePoints_080371f4 | 0x080371f4 | remove_slot_by_index_from_graveyard_arrays | remove_slot_by_idx_from_gy_lp_ptr |
| PTR_gP1LifePoints_0803725c | 0x0803725c | erase_slot_from_graveyard_arrays_by_ptr | erase_slot_from_gy_by_ptr_lp_ptr |
| PTR_gP1LifePoints_08037304 | 0x08037304 | remove_slot_from_field_array_by_player | remove_slot_from_field_arr_lp_ptr |
| PTR_gP1LifePoints_08037354 | 0x08037354 | count_hand_cards_with_field5 | count_hand_cards_field5_lp_ptr |
| PTR_gP1LifePoints_080373a4 | 0x080373a4 | count_graveyard_normal_summon_cards | count_gy_normal_summon_lp_ptr |
| PTR_gP1LifePoints_0803742c | 0x0803742c | count_zone_slots_with_card_field5 | count_zone_slots_field5_lp_ptr |
| PTR_gP1LifePoints_080374d8 | 0x080374d8 | check_zone_slot_equip_eligible | check_zone_slot_equip_elig_lp_ptr |
| PTR_gP1LifePoints_0803760c | 0x0803760c | check_zone_slot_equip_eligible_alt | check_zone_slot_equip_elig_alt_lp_ptr |
| PTR_gP1LifePoints_08037684 | 0x08037684 | place_equip_card_if_type_matches | place_equip_card_type_lp_ptr |
| PTR_gP1LifePoints_0803774c | 0x0803774c | erase_slot_from_field_array_c_by_ptr | erase_slot_from_field_arr_c_lp_ptr |
| PTR_gP1LifePoints_080377e0 | 0x080377e0 | eval_equip_bonus_for_slot | eval_equip_bonus_lp_ptr |
| PTR_gP1LifePoints_080378d8 | 0x080378d8 | find_field_zone_slot_with_fieldspell | find_field_zone_fieldspell_lp_ptr |

#### 无 label 函数 fn-ptr 槽

| 槽 | ROM addr | value | gas_label | slot_label |
|----|----------|-------|-----------|------------|
| DAT_08037884 | 0x08037884 | 0x0803777d | `check_level_conv_lab_node_match+1` | eval_equip_bonus_for_slot_pred_fn |

函数 0x0803777c 需在 Ghidra 中 createLabel("check_level_conv_lab_node_match", 0x0803777c).
同一 fn-ptr 在 Seg-4 (DAT_0803aa74 @ 0x0803aa74) 中亦有引用, Seg-4 fixer 同步处理.

函数语义 (high-conf, 来自代码静态分析):
- r0 = chain_node_ptr, r1 = search_ctx_ptr (out)
- 检查 node: byte[+2] bits[3:0] <= 5; halfword[+0] == LEVEL_CONVERSION_LAB_CID (0x18d9)
- 检查 node halfword[+4] & SCENE_SLOT_MASK_LO == search_ctx[0]
- 若全部匹配: search_ctx[4] = halfword[+4] >> 12; 返回 0
- 消费者: eval_equip_bonus_for_slot (0x080377f0 bl find_equip_chain_node_by_pred r2=fn)
          eval_equip_chain_score_for_slot (0x0803aa30 bl find_equip_chain_node_by_pred r2=fn)

### RENAME_SLOTS

段内所有自动名槽均通过 EQ 或 REF 处理, 无需独立 RENAME_SLOT 操作.
(DWORD_/DAT_ 全部由 EQ 覆盖; PTR_gP1LifePoints_* 全部由 REF 覆盖)

### FUNC_RENAME

段内 13 个命名函数均名称正确, 无 FUNC_RENAME 需求.

**额外**: 0x0803777c 处无标函数需 createLabel (见 REF_SLOTS 说明).

### PLATE (R5)

13 个函数 plate 全部重写 (修正 stale FUN_ + 更新槽名 + ASCII 验证).

#### C8 stale FUN_ 修正 (4 处)

1. **remove_slot_by_index_from_graveyard_arrays** (0x08037174):
   - `FUN_0803720c` -> `erase_slot_from_graveyard_arrays_by_ptr`

2. **erase_slot_from_graveyard_arrays_by_ptr** (0x0803720c):
   - `FUN_08032194` -> `erase_slot_from_zone_array_by_type`

3. **place_equip_card_if_type_matches** (0x08037630):
   - `FUN_08032280` -> `dispatch_card_placement_by_zone_type`
   - `FUN_08031954` -> `retire_equip_slot_with_relink`

4. **erase_slot_from_field_array_c_by_ptr** (0x080376a0):
   - `FUN_08032194` -> `erase_slot_from_zone_array_by_type`
   - 注释纠错: "assoc_array_base=gP1LP+0xd70 (0x0201c600)" 应为
     "field_array_C_base=gP1LP+0x120 (0x0201c600); count_base=gP1ZoneHandCount via neg_off -0x114"

#### 所有 13 函数 plate (ASCII 重写)

**count_graveyard_entries_by_card_id** (0x08037128):
```
Count entries in player graveyard word array matching target card_id.
Reads gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x1c (alt-hand/GY count).
Traverses word array at gP1LP+0x5d0 (=0xba<<3, stride 4B); extracts bits[12:0] as card_id.
Returns r4=total match count. r0=u8 player_id [0..1]; r1=u16 card_id (16-bit truncated).
indeg=0; referenced via fn-ptr or dead code.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE=0x868; GY_WORD_OFF=0x5d0 (0xba<<3); GY_COUNT_OFF=0x1c.
```

**remove_slot_by_index_from_graveyard_arrays** (0x08037174):
```
Remove one slot by index from graveyard dual arrays (word array gP1LP+0x5d0 and hword array
gP1LP+0x788), decrement count at gP1LP+0x1c. If slot_idx>=count returns 0. Decrements count.
If slot_idx<new_count: shift-left both arrays via write_word_from_deref_src (word) and ldrh/strh (hword).
Returns 1 on success, 0 if out of range.
r0=u8 player_id [0..1]; r1=u32 slot_idx (loaded to r12 at entry via 0x468c=mov r12,r1).
Caller: erase_slot_from_graveyard_arrays_by_ptr (finds match then calls this to delete by index).
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; GY_WORD_OFF=0x5d0; GY_HWORD_OFF=0x788 (0xf1<<3); GY_COUNT_OFF=0x1c.
```

**erase_slot_from_graveyard_arrays_by_ptr** (0x0803720c):
```
Forward-search graveyard word array for element matching r1=slot_ptr (loaded to r8 at entry
via 0x4688=mov r8,r1); on match call remove_slot_by_index_from_graveyard_arrays(player_id, idx).
Returns 1 on success, 0 if not found.
r0=u8 player_id [0..1]; r1=slot_ptr (r8, forwarded as target to check_deref_words_equal).
Caller: erase_slot_from_zone_array_by_type (file02, 0x08032194) on graveyard card removal.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; GY_WORD_OFF=0x5d0; GY_COUNT_OFF=0x1c.
```

**remove_slot_from_field_array_by_player** (0x0803727c):
```
Remove slot by index from player field arrays A (gP1LP+0x260=0x98<<2) and B (gP1LP+0x418=0x83<<3)
using swap-to-tail and decrement. Reads count at gP1LP+0x14 (gP1HandCountBase) and capacity at
gP1LP+0x10 (gP1SlotCountBase). Loops via swap_deref_words from tail toward target; decrements count.
Returns void (pop{r0};bx r0).
r0=u8 player_id (bit0) [0..1]; r1=u32 slot_index (0-based).
Caller: tick_field_clear_display_sequence (0x08040e54) during field clear phase.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; FIELD_CNT_OFF=0x14; CAP_OFF=0x10; ARR_A_OFF=0x260 (0x98<<2); ARR_B_OFF=0x418 (0x83<<3).
```

**count_hand_cards_with_field5** (0x0803730c):
```
Count hand cards where check_card_field5_is_nonzero(card_id) returns true. Reads hand count at
gP1LP+0x14; if 0 returns 0. Iterates hand array at gP1LP+0x418 (0x83<<3), extracts bits[12:0]
as card_id, calls check_card_field5_is_nonzero; increments r6 on nonzero. Returns r6.
r0=u8 player_id [0..1]. Returns u32 count.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; HAND_CNT_OFF=0x14; HAND_ARR_OFF=0x418 (0x83<<3).
```

**count_graveyard_normal_summon_cards** (0x0803735c):
```
Count cards in player graveyard (gP1LP+0x418, count at gP1LP+0x14) matching
check_card_id_is_normal_summon_type. Returns total count.
Called by eval_slot_score_entry_full (0x08037ec0) LP-cost branch; result scaled x5 into r10.
r0=u8 player_id [0..1]. Returns u32 count.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; GY_BASE_OFF=0x418 (0x83<<3); GY_CNT_OFF=0x14.
```

**count_zone_slots_with_card_field5** (0x080373ac):
```
Count zone slots in r9/r8 zone table where flag byte==0x40 or ==0x80 AND
check_card_field5_is_nonzero(card_id) is true. r0=player_side (bit0, saved r5); Non-APCS
r9=player_stride multiplier; r8=zone array base. Inner loop 2-player x count slots; reads flag
byte at gP1LP+0xf1*8 (=0x788) stride; on flag match reads card_id from r9 base; checks field5.
Returns r6=matching slot count.
r0=u8 player_side [0..1]; r9=zone_stride (non-APCS); r8=zone_base (non-APCS).
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; FLAG_BYTE_OFF=0x788 (0xf1<<3); ZONE_FLAG_A=0x40; ZONE_FLAG_B=0x80.
```

**check_zone_slot_equip_eligible** (0x08037434):
```
Check equip eligibility of zone slot at gP1HandSlotArray[player*PLAYER_BLOCK_STRIDE+slot*4].
Extracts card_id (bits[12:0]). Five-step chain: (1) check_card_is_equip_target_eligible;
(2) check_card_has_equip_placement_type -> fail: eval_equip_placement_full_check;
(3) bit21 of slot word set -> fail; (4) check_card_stat_field8_is_6;
(5) check_toon_world_equip_present.
Special: card_id==GRADIUS_OPTION_CID (0x14fc) -> count_paired_slots_with_field5_default(player,0x1414);
card_id==LAVA_GOLEM_CID (0x14fc+0x7c=0x1578) -> read gP1LP+0x8e*2=0x11c bit17; if 0 call
check_value_in_slot_chain(player, ULTIMATE_OFFERING_CID=0x12f3, 0xb); additional range/ID blacklist:
[XYZ_DRAGON_CANNON_CID 0x15b4; TYRANT_DRAGON_CARD_ID 0x14d5->count_slots_equippable_by_state_code;
HELPOEMER_CID 0x1571; XY_DRAGON_CANNON=0x15b1; SPHINX_TELEIA 0x17c8/ANDRO_SPHINX 0x17c7 range;
YZ_TANK_DRAGON 0x15fa/XZ_TANK_CANNON 0x15f9 range; THE_CREATOR=0xc1<<5=0x1820].
indeg=21. r0=u8 player_side; r1=u8 zone_player_id bit0; r2=u8 slot_index [0..4]. Returns bool.
Constants: gP1HandSlotArray=0x0201c8f8; PLAYER_BLOCK_STRIDE; GRADIUS_OPTION_CID=0x14fc;
GRADIUS_CID=0x1414; ULTIMATE_OFFERING_CID=0x12f3; XYZ_DRAGON_CANNON_CID=0x15b4;
HELPOEMER_CID=0x1571; SPHINX_TELEIA_CID=0x17c8; YZ_TANK_DRAGON_CID=0x15fa.
```

**check_zone_slot_equip_eligible_alt** (0x08037568):
```
Alt variant of check_zone_slot_equip_eligible (0x08037434); structure fully symmetric.
Only difference: zone table base=gP1AltHandSlotArray=0x0201cab0 (vs gP1HandSlotArray=0x0201c8f8).
Same five-step check chain and same special card_id handling (GRADIUS_OPTION_CID / Lava Golem /
ULTIMATE_OFFERING_CID / range blacklist). indeg=3.
r0=u8 player_side; r1=u8 zone_player_id bit0; r2=u8 slot_index [0..4]. Returns bool.
Constants: gP1AltHandSlotArray=0x0201cab0; PLAYER_BLOCK_STRIDE; (same card IDs as primary variant).
```

**place_equip_card_if_type_matches** (0x08037630):
```
For zone_type=0xb insert: verifies slot card_type is equip (map_field8_to_card_type_category==3)
and routes to correct array. r0=player_id, r1=slot_ptr (saved r4). Extracts card_type (bits[12:0]
from slot[0]); skips if card_type==0 or check_card_field8_is_9. Calls map_field8_to_card_type_category:
if category==3 (equip): append_slot_ref_to_equip_array; else: write_word_from_deref_src to
gP1LP+0x120 (gP1FieldArrayCBase per player), increments count at gP1LP+0x0c.
Returns void (pop{r0};bx r0).
Callers: dispatch_card_placement_by_zone_type (file02, 0x08032280) case 0xb;
         retire_equip_slot_with_relink (file02, 0x08031954) re-check on field update.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; FIELD_C_ARR_OFF=0x120 (0x90<<1); FIELD_C_CNT_OFF=0x0c.
```

**erase_slot_from_field_array_c_by_ptr** (0x080376a0):
```
Search field array C (gP1FieldArrayCBase=gP1LP+0x120, count at gP1ZoneHandCount=gP1LP+0x0c) for
slot_ptr (r1=r10 via 0x468a=mov r10,r1). On match: count-=1; if r8<new_count: dual left-shift loop
via write_word_from_deref_src; zeros old last entry via zero_fill_by_halfword. Returns 1 on success, 0 if not found.
r0=u8 player_id [0..1]; r1=slot_ptr (r10, target for check_deref_words_equal).
Caller: erase_slot_from_zone_array_by_type (file02, 0x08032194) on field-zone card exit.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; gP1FieldArrayCBase=0x0201c600;
FIELD_ARRAY_C_TO_COUNT_NEG_OFF=0xfffffeec (gP1FieldArrayCBase-0x114=gP1ZoneHandCount per player).
```

**eval_equip_bonus_for_slot** (0x080377b0):
```
Evaluate equip bonus score for slot (r0=player_side, r1=slot_idx). Reads card_id from
gP1LP+slot*4+0x10e0 (zone-chain hword base, 0x87<<5 from gP1LP). Calls get_card_extended_stat_field5(card_id);
if 0 returns 0. Calls find_equip_chain_node_by_pred with pred=check_level_conv_lab_node_match
(fn-ptr 0x0803777d) to locate Level Conversion Lab node (A_LEGENDARY_OCEAN_CARD_ID=0x150b used
for subsequent check_card_stat_field7_equals(card_id, 3)). Two-player bonus loop at gP1LP+0xf8
(=gDuelFieldSlots_p2_base) + gP1LP+0x108 offset; loop for player=0..1, slot=0..count:
reads card_id, checks A_LEGENDARY_OCEAN_CARD_ID (0x150b) match via check_card_matches_active_effect_slot;
adjusts score. Calls count_slot_chain_nodes_by_card_id(COST_DOWN_CID=0x15c7, 0xb); subtracts result*2.
Returns max(score, 1). r0=u8 player_side [0..1]; r1=u8 slot_idx [0..4]. Returns u32 bonus_score.
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; ZONE_CHAIN_HWORD_OFF=0x87<<5=0x10e0;
A_LEGENDARY_OCEAN_CARD_ID=0x150b; COST_DOWN_CID=0x15c7; gDuelFieldSlots_p2_base offset=0xf8.
```

**find_field_zone_slot_with_fieldspell** (0x08037894):
```
Scan field array C (gP1FieldArrayCBase=gP1LP+0x120, count at gP1LP+0x0c) for first card with
extended field6==0x17 (field spell type). Returns 0-based slot index; returns -1 (rsbs r0,r0,#0)
if not found. Skips card_id==0 slots.
Symmetric sibling to find_field_zone_slot_with_equip_type (0x08037904, Seg-4); only difference
is field6 check value (0x17 vs 0x16). Pure read-only.
r0=u8 player_id [0..1]. Returns s32 slot_index (>=0 if found, -1 if not).
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; gP1FieldArrayCBase=0x0201c600;
FIELD_C_CNT_OFF=0x0c; FIELDSPELL_FIELD6=0x17.
```

## carve 计划 (R7, 如有)

无 (Seg-3 无 ROM_INCBIN 块, 无需 carve).

## disasm 计划 (R4, 如有)

**无大块 disasm 需求** (所有 13 个函数已为 THUMB 代码).

**额外**: 0x0803777c 处的无 label 函数 (28 字节) 已是 THUMB 代码, 仅需 createLabel 操作, 不是
disasm (代码已存在). Fixer 在 Ghidra 中 setTMode+createLabel 即可.

## 新增 constants / 全局

### card_info.inc 新增 9 项 (均通过 grep 确认现有 constants/*.inc 无同值)

```
.equ GRADIUS_OPTION_CID,         0x000014fc  @ Gradius' Option (pw=14291024; card-stats.s card_1063 slot=0x14FC); check_zone_slot_equip_eligible special: count_paired_slots_with_field5_default(player,0x1414); 8 raw refs; 2 Seg-3 slots
.equ GRADIUS_CID,                0x00001414  @ Gradius (pw=10992251; card-stats.s card_0895 slot=0x1414); paired with GRADIUS_OPTION_CID in check_zone_slot_equip_eligible count_paired path; 6 raw refs; 2 Seg-3 slots
.equ ULTIMATE_OFFERING_CID,      0x000012f3  @ Ultimate Offering (pw=80604091; card-stats.s card_0678 slot=0x12F3); check_value_in_slot_chain guard in check_zone_slot_equip_eligible; 6 raw refs; 2 Seg-3 slots
.equ XYZ_DRAGON_CANNON_CID,      0x000015b4  @ XYZ-Dragon Cannon (pw=91998119; card-stats.s card_1203 slot=0x15B4); range_base in equip-eligible blacklist; 4 raw refs; 1 Seg-3 slot
.equ HELPOEMER_CID,              0x00001571  @ Helpoemer (pw=76052811; card-stats.s card_1148 slot=0x1571); blacklist single-ID in check_zone_slot_equip_eligible; 4 raw refs; 1 Seg-3 slot
.equ SPHINX_TELEIA_CID,          0x000017c8  @ Sphinx Teleia (pw=51402177; card-stats.s card_1623 slot=0x17C8); range_max in [ANDRO_SPHINX 0x17c7, SPHINX_TELEIA 0x17c8] blacklist; 4 raw refs; 1 Seg-3 slot
.equ YZ_TANK_DRAGON_CID,         0x000015fa  @ YZ-Tank Dragon (pw=25119460; card-stats.s card_1254 slot=0x15FA); range_max in [XZ_TANK_CANNON 0x15f9, YZ_TANK_DRAGON 0x15fa] blacklist; 4 raw refs; 1 Seg-3 slot
.equ LEVEL_CONVERSION_LAB_CID,   0x000018d9  @ Level Conversion Lab (pw=84397023; card-stats.s card_1865 slot=0x18D9); check_level_conv_lab_node_match predicate target; 4 raw refs; 1 Seg-3 slot
.equ COST_DOWN_CID,              0x000015c7  @ Cost Down (pw=23265313; card-stats.s card_1213 slot=0x15C7); eval_equip_bonus_for_slot count_slot_chain_nodes_by_card_id arg; 4 raw refs; 1 Seg-3 slot
```

### ewram.inc 新增 1 项

```
.equ gP1FieldArrayCBase,    0x0201c600  @ gP1LifePoints+0x120 (0x90<<1): field array C base ptr (zone_type=0xb, place_equip_card_if_type_matches); count at gP1ZoneHandCount (gP1LP+0x0c); 115 raw refs; 2 Seg-3 slots (erase_slot_from_field_array_c_by_ptr + find_field_zone_slot_with_fieldspell)
```

### duel_field.inc 新增 1 项

```
.equ FIELD_ARRAY_C_TO_COUNT_NEG_OFF, 0xfffffeec  @ gP1FieldArrayCBase (0x0201c600) + 0xfffffeec = gP1ZoneHandCount (0x0201c4ec); neg delta -0x114 from field array C to count base; used per-player: (gP1FieldArrayCBase+player*0x868) + this = count_ptr; 2 raw refs; 1 Seg-3 slot
```

## §5.1 登记 (Rule 3) -- 0 引用块

Seg-3 无 ROM_INCBIN 块. 无 §5.1 登记.

## 消费者证据 (R6)

| 槽 | 语义 | 证据 (file:line) | 置信度 |
|----|------|-----------------|--------|
| gP1FieldArrayCBase=0x0201c600 | gP1LP+0x120 = field array C base (zone_type=0xb slot array) | asm/03_equip_chain_hand.s:3248 (movs r1,#0x90; lsls r1,#1 -> 0x120 offset) + asm/03:3247 (adds r1,r1,r2 where r2=gP1LP); confirmed by zone_resolver comment: "zone_type 0xb -> 0x0201c600" | high |
| FIELD_ARRAY_C_TO_COUNT_NEG_OFF=0xfffffeec | neg delta from field_array_C_base to count_base | asm/03_equip_chain_hand.s:3316-3317 (DAT_08037754=0x0201c600, DAT_08037758=0xfffffeec); adds r0,r1,r3 -> 0x0201c600+0xfffffeec=0x0201c4ec=gP1ZoneHandCount | high |
| gP1HandSlotArray=0x0201c8f8 | zone P0 slot array base for check_zone_slot_equip_eligible | asm/03:2941 (DAT_08037490=0x0201c8f8); exists in ewram.inc as gP1HandSlotArray | high |
| gP1AltHandSlotArray=0x0201cab0 | zone P1 alt slot array for check_zone_slot_equip_eligible_alt | asm/03:3104 (DAT_080375c4=0x0201cab0); exists in ewram.inc as gP1AltHandSlotArray | high |
| GRADIUS_OPTION_CID=0x14fc | Gradius' Option: check_zone_slot_equip_eligible special path -> count_paired_slots_with_field5_default(player, 0x1414) | asm/03:2944 (DAT_08037494=0x14fc); card-stats.s card_1063 slot=0x14FC; bl count_paired_slots_with_field5_default at 0x0803749c | high |
| GRADIUS_CID=0x1414 | Gradius: paired with GRADIUS_OPTION_CID -> r1=0x1414 passed to count_paired_slots | asm/03:2952 (DAT_080374a4=0x1414); card-stats.s card_0895 slot=0x1414 | high |
| ULTIMATE_OFFERING_CID=0x12f3 | Ultimate Offering: check_value_in_slot_chain guard for Lava Golem check path | asm/03:2983 (DAT_080374e0=0x12f3); card-stats.s card_0678 slot=0x12F3; bl check_value_in_slot_chain(r0,r1=0xb) at 0x080374cc | high |
| LEVEL_CONVERSION_LAB_CID=0x18d9 | Level Conversion Lab: predicate match target in check_level_conv_lab_node_match | asm/03:3361 (DAT_080377a8=0x18d9); card-stats.s card_1865 slot=0x18D9; ldrh r1,[r2,#0] cmp r1,0x18d9 at 0x0803778c-0x0803778e | high |
| COST_DOWN_CID=0x15c7 | Cost Down: count_slot_chain_nodes_by_card_id(COST_DOWN, 0xb) score deduction in eval_equip_bonus_for_slot | asm/03:3453 (DAT_08037890=0x15c7); card-stats.s card_1213 slot=0x15C7; bl count_slot_chain_nodes_by_card_id at 0x08037862 | high |
| A_LEGENDARY_OCEAN_CARD_ID=0x150b | A Legendary Ocean: check_card_stat_field7_equals(card_id, 3) test in eval_equip_bonus_for_slot | asm/03:3479 (DAT_0803788c=0x150b); exists in card_info.inc as A_LEGENDARY_OCEAN_CARD_ID | high |
| check_level_conv_lab_node_match fn-ptr | THUMB predicate passed to find_equip_chain_node_by_pred (r2=0x0803777d) | asm/03:3475 (DAT_08037884=0x0803777d); ref-scan: raw=2 at ROM offsets 0x08037884+0x0803aa74; bl find_equip_chain_node_by_pred at 0x080377f0 | high |

## 求助

1. **eval_equip_bonus_for_slot 内部 0x10e0 偏移**: `0x87<<5 = 0x10e0` 作为区域链 hword 数组偏移,
   是 gP1LP+0x10e0 处的每槽半字 (邻近 ZONE_CHAIN_CARD_ID_OFF=0x10e2). 语义可能是 "zone_chain_card_hword_base"
   但该偏移值在现有 constants 中无对应定义. 该偏移为 inline 计算 (movs r1,#0x87;lsls r1,#5),
   不产生 DAT_ 槽, 本 Seg-3 proposal 不需要处理, 供 Seg-4 参考.

2. **gP1LP+0x788 hword 数组**: remove_slot_by_index_from_graveyard_arrays 使用 `0xf1<<3=0x788`
   作为 GY hword 数组偏移 (inline 计算, 无 DAT_ 槽). ewram.inc 中 `gP1AltHandSlotArray=gP1LP+0x5d0`
   (GY word array) 已定义, 但对应的 hword 并排数组 gP1LP+0x788 尚无全局名. 不影响 Seg-3 槽处理.

---

## Executor Report: F03Seg3

- 槽: EQ=36 (reuse 24 + new 12) / REF=13 (12 PTR_gP1LifePoints + 1 fn-ptr) / RENAME=0 / FUNC_RENAME=0 / PLATE=13
- carve=0 / disasm=0 (无 ROM_INCBIN; 无误标代码块) / §5.1=0
- 新增 constants/全局:
  - card_info.inc +9: GRADIUS_OPTION_CID / GRADIUS_CID / ULTIMATE_OFFERING_CID / XYZ_DRAGON_CANNON_CID / HELPOEMER_CID / SPHINX_TELEIA_CID / YZ_TANK_DRAGON_CID / LEVEL_CONVERSION_LAB_CID / COST_DOWN_CID
  - ewram.inc +1: gP1FieldArrayCBase=0x0201c600
  - duel_field.inc +1: FIELD_ARRAY_C_TO_COUNT_NEG_OFF=0xfffffeec
  - 新 label: check_level_conv_lab_node_match @ 0x0803777c (Ghidra createLabel)
- C8 stale FUN_ 修正: 4 处 (FUN_0803720c / FUN_08032194 x2 / FUN_08032280 / FUN_08031954)
- 求助: none (所有语义有 file:line 证据 + high/med 置信度)
- proposal: doc/dev/refine/F03Seg3.proposal.md
