# Refine Proposal: F03Seg4a  [0x08037904..0x08037ec0)

## 拆分决定

Seg-4 原始范围 [0x08037904..0x0803a7f0) 含 ROM_INCBIN @0x39350 size 0x10ce (4302B)。
incbin 块完整落在 `eval_slot_score_entry_full` (起自 0x08037ec0) 的函数体内部，通过
`dispatch_equip_node_by_type` 的 `mov pc,r0` 13 项跳转表调度进入；块结束在 0x0803a41e。

天然拆分边界：`compute_zone_effect_atk_delta` 函数结束处 0x08037ec0 (Ghidra 对齐 4B)。

| 半段 | 地址范围 | 函数数 | 槽数 | ROM_INCBIN |
|------|----------|--------|------|------------|
| **Seg-4a** | 0x08037904..0x08037ec0 | 12 | 43 | 无 |
| Seg-4b (后续) | 0x08037ec0..0x0803a7f0 | 1+sub-fns | 140+ | **0x39350/0x10ce** |

本 proposal 覆盖 **Seg-4a** 全部 43 个槽。Seg-4b incbin ref-scan 证据见下文。

---

## 段测绘

### 函数入口 x12

| 地址 | 函数名 |
|------|--------|
| 0x08037904 | find_field_zone_slot_with_equip_type |
| 0x08037974 | count_gy_cards_by_field6 |
| 0x080379d0 | count_field_zone_cards_by_field7 |
| 0x08037a2c | count_valid_monster_pair_slots |
| 0x08037a8c | find_zone_slot_idx_allowed_for_card |
| 0x08037ae4 | count_field_zone_cards_with_field5 |
| 0x08037b34 | count_monster_slots_with_field5_ge_threshold |
| 0x08037b90 | get_player_deck_flag_bit1 |
| 0x08037bb4 | check_field_effect_zone_activation_eligible |
| 0x08037c20 | shuffle_hand_by_player_deck_flag |
| 0x08037c9c | compute_zone_effect_atk_delta |
| (Seg-4b start) | eval_slot_score_entry_full @ 0x08037ec0 |

### 残留自动名槽 x43 (定义)

全部 43 个槽均为 literal-pool .word，无 ROM_INCBIN，无残留 .byte 块。

```
PTR_gP1LifePoints_08037948   @ 08037948  = gP1LifePoints
DAT_0803794c                 @ 0803794c  = 0x00000868
DAT_08037950                 @ 08037950  = 0x0201c600
DAT_08037970                 @ 08037970  = 0x00000868
PTR_gP1LifePoints_080379c8   @ 080379c8  = gP1LifePoints
DAT_080379cc                 @ 080379cc  = 0x00000868
PTR_gP1LifePoints_08037a24   @ 08037a24  = gP1LifePoints
DAT_08037a28                 @ 08037a28  = 0x00000868
PTR_gP1LifePoints_08037a84   @ 08037a84  = gP1LifePoints
DAT_08037a88                 @ 08037a88  = 0x00000868
PTR_gP1LifePoints_08037ac8   @ 08037ac8  = gP1LifePoints
DAT_08037acc                 @ 08037acc  = 0x00000868
PTR_gP1LifePoints_08037b2c   @ 08037b2c  = gP1LifePoints
DAT_08037b30                 @ 08037b30  = 0x00000868
PTR_gP1LifePoints_08037b88   @ 08037b88  = gP1LifePoints
DAT_08037b8c                 @ 08037b8c  = 0x00000868
PTR_gP1LifePoints_08037bac   @ 08037bac  = gP1LifePoints
DAT_08037bb0                 @ 08037bb0  = 0x00000868
DAT_08037c04                 @ 08037c04  = 0x0000137b
DAT_08037c08                 @ 08037c08  = 0x000017e7
PTR_gP1LifePoints_08037c0c   @ 08037c0c  = gP1LifePoints (=0x0201c4e0)
DAT_08037c10                 @ 08037c10  = 0x00001ce8
DAT_08037c14                 @ 08037c14  = 0x0000135e
PTR_gP1LifePoints_08037c94   @ 08037c94  = gP1LifePoints
DAT_08037c98                 @ 08037c98  = 0x00000868
DAT_08037cf0                 @ 08037cf0  = 0x00000868
DAT_08037cf4                 @ 08037cf4  = 0x0201c510
DAT_08037d30                 @ 08037d30  = 0x00001346
DAT_08037d34                 @ 08037d34  = 0x000010f5
DAT_08037d48                 @ 08037d48  = 0x00001344
DAT_08037d68                 @ 08037d68  = 0x00001349
DAT_08037d80                 @ 08037d80  = 0x0000159d
DAT_08037d8c                 @ 08037d8c  = 0x0000183f
DAT_08037db8                 @ 08037db8  = 0x00000868
DAT_08037dbc                 @ 08037dbc  = 0x0201c510
DAT_08037ddc                 @ 08037ddc  = 0x09e3ef74
DAT_08037de0                 @ 08037de0  = 0xffffef10
DAT_08037e14                 @ 08037e14  = 0xfffffe70
DAT_08037e2c                 @ 08037e2c  = 0xfffffe70
DAT_08037e44                 @ 08037e44  = 0xfffffe70
DAT_08037e5c                 @ 08037e5c  = 0xfffffe70
DAT_08037eb8                 @ 08037eb8  = 0x00000868
DAT_08037ebc                 @ 08037ebc  = 0x0201c510
```

### ROM_INCBIN / .byte 块

Seg-4a 内无 ROM_INCBIN。

以下为 Seg-4b incbin 块提前 ref-scan (硬规则 2 要求)：

---

## 数据块分类 (Rule 2/3) — incbin @0x39350 ref-scan (Seg-4b 前置)

| 块 | ref-scan (raw / THUMB|1) | 判定 | 理由 |
|----|--------------------------|------|------|
| 0x08039350 sz=0x10ce | raw=4 thumb=0 | **disasm (R4)** | 4 raw refs 全来自同一 jump table (PTR_DAT_0803931c); mov pc,r0 派发，无 THUMB|1 引用; 首 hword 0x4812=ldr r0,[pc,#0x48] THUMB opcode; blocks 0x08039a62/0x08039a7c/0x08039c1c/0x0803a3c4/0x0803a2fc 均为同一 mov pc,r0 table 的 raw 目标 |

详细 ref-scan (python d.count(struct.pack('<I', addr))):

```
0x08039350: raw=4 thumb=0  <-- 4 entries from PTR_DAT_0803931c[0..3]
0x08039a62: raw=1 thumb=0  <-- PTR_DAT_0803931c[4]
0x08039a7c: raw=4 thumb=0  <-- PTR_DAT_0803931c[5..8] (4 entries same addr)
0x08039c1c: raw=2 thumb=0  <-- PTR_DAT_0803931c[9..10]
0x0803a3c4: raw=1 thumb=0  <-- PTR_DAT_0803931c[11]
0x0803a2fc: raw=1 thumb=0  <-- PTR_DAT_0803931c[12]
```

所有 raw 引用仅来自 PTR_DAT_0803931c (13 条目 jump table, 在
dispatch_equip_node_by_type 末尾, 属 eval_slot_score_entry_full 函数体)。
全 ROM 0 THUMB|1 引用确认 mov pc,r0 raw 派发 (非 BX)。

**carve 方案**: PTR_DAT_0803931c (13*4=52B) 需 carve 进 rom.s 作 jump table label，
incbin 块本体交 R4 disasm 处理 (逐 stub 在 Seg-4b proposal 细化)。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS — data-equate

共 43 槽，分为三类：

#### A. 全部复用 PLAYER_BLOCK_STRIDE (0x868) — 15 槽

| 槽 | addr | 复用 |
|----|------|------|
| DAT_0803794c | 0x0803794c | PLAYER_BLOCK_STRIDE |
| DAT_08037970 | 0x08037970 | PLAYER_BLOCK_STRIDE |
| DAT_080379cc | 0x080379cc | PLAYER_BLOCK_STRIDE |
| DAT_08037a28 | 0x08037a28 | PLAYER_BLOCK_STRIDE |
| DAT_08037a88 | 0x08037a88 | PLAYER_BLOCK_STRIDE |
| DAT_08037acc | 0x08037acc | PLAYER_BLOCK_STRIDE |
| DAT_08037b30 | 0x08037b30 | PLAYER_BLOCK_STRIDE |
| DAT_08037b8c | 0x08037b8c | PLAYER_BLOCK_STRIDE |
| DAT_08037bb0 | 0x08037bb0 | PLAYER_BLOCK_STRIDE |
| DAT_08037c98 | 0x08037c98 | PLAYER_BLOCK_STRIDE |
| DAT_08037cf0 | 0x08037cf0 | PLAYER_BLOCK_STRIDE |
| DAT_08037db8 | 0x08037db8 | PLAYER_BLOCK_STRIDE |
| DAT_08037eb8 | 0x08037eb8 | PLAYER_BLOCK_STRIDE |

(以上 13 槽，均值 0x868；另有 2 槽合并到下方 gDuelFieldSlots 组)

#### B. 全部复用 gDuelFieldSlots / gP1FieldArrayCBase — 6 槽

| 槽 | addr | value | 复用 |
|----|------|-------|------|
| DAT_08037950 | 0x08037950 | 0x0201c600 | gP1FieldArrayCBase (ewram.inc) |
| DAT_08037cf4 | 0x08037cf4 | 0x0201c510 | gDuelFieldSlots (ewram.inc) |
| DAT_08037dbc | 0x08037dbc | 0x0201c510 | gDuelFieldSlots (ewram.inc) |
| DAT_08037ebc | 0x08037ebc | 0x0201c510 | gDuelFieldSlots (ewram.inc) |

#### C. 全部复用 gP1LifePoints — 9 PTR_ 槽 (REF, not EQ)

PTR_gP1LifePoints_* x9 均 .word gP1LifePoints (已有 label)，不需新建；归入 REF_SLOTS。

#### D. 复用 P1LP_BLOCK2_OFF_1CE8 / DUEL_ACTIVE_PLAYER_OFF — ewram.inc 已有

| 槽 | addr | value | 复用 |
|----|------|-------|------|
| DAT_08037c10 | 0x08037c10 | 0x1ce8 | P1LP_BLOCK2_OFF_1CE8 (ewram.inc) |

注: DUEL_ACTIVE_PLAYER_OFF=0x1cb8 在 duel_field.inc 已有，但本段不使用该值。

#### E. 新建 card_info.inc CID 常量 — 14 新 CID

消费者证据来自 check_field_effect_zone_activation_eligible 和 compute_zone_effect_atk_delta：

| 槽 | addr | value | 新常量名 | 卡名 | 证据 |
|----|------|-------|---------|------|------|
| DAT_08037c04 | 0x08037c04 | 0x137b | EYE_OF_TRUTH_CID | The Eye of Truth | asm:3966 bl count_available_effect_zones(player=opposite, card=0x137b); card-stats.s card_0791 slot=0x137b; high |
| DAT_08037c08 | 0x08037c08 | 0x17e7 | MIND_ON_AIR_CID | Mind on Air | asm:3967 bl count_available_effect_zones(player=opposite, card=0x17e7); card-stats.s card_1652 slot=0x17e7 L21491; high |
| DAT_08037c14 | 0x08037c14 | 0x135e | RESPECT_PLAY_CID | Respect Play | asm:3973 count_field_copies_of_card(card=0x135e) after gP1LifePoints+0x1ce8 guard; card-stats.s card_0766 slot=0x135e; high |
| DAT_08037d30 | 0x08037d30 | 0x1346 | MOLTEN_DESTRUCTION_CID | Molten Destruction | asm:4139 range upper bound of binary-search card dispatch (MOLTEN_DEST is topmost cmp); card-stats.s card_0747 slot=0x1346; high |
| DAT_08037d34 | 0x08037d34 | 0x10f5 | YAMI_CID | Yami (classic field spell) | asm:4141 lower bound for field-spell ATK delta table lookup (cards <= YAMI_CID go to table path); card-stats.s card_0297 slot=0x10f5 L3876; high |
| DAT_08037d48 | 0x08037d48 | 0x1344 | GAIA_POWER_CID | Gaia Power | asm:4152 exact cmp after binary-search split (0x1344 == 0x1346-2); card-stats.s card_0745 slot=0x1344; high |
| DAT_08037d68 | 0x08037d68 | 0x1349 | MYSTIC_PLASMA_ZONE_CID | Mystic Plasma Zone | asm:4170 exact cmp; card-stats.s card_0750 slot=0x1349; high |
| DAT_08037d80 | 0x08037d80 | 0x159d | NECROVALLEY_CID | Necrovalley | asm:4184 exact cmp, check_card_is_gravekeeper branch; card-stats.s card_1185 slot=0x159d; high |
| DAT_08037d8c | 0x08037d8c | 0x183f | HARPIES_HUNTING_GROUND_CID | Harpies' Hunting Ground | asm:4191 exact cmp; card-stats.s card_1731 slot=0x183f; high |

Note: GRADIUS_OPTION_CID=0x14fc already in card_info.inc (Seg-3); not re-added.

#### F. 新建 card_info.inc CID — find_field_zone_slot_with_equip_type 区域 x5

| 槽 | addr | value | 新常量名 | 卡名 | 证据 |
|----|------|-------|---------|------|------|
| (none in Seg-4a for this fn) | | | | | |

Note: find_field_zone_slot_with_equip_type only holds 3 DAT_ (stride, gP1FieldArrayCBase, stride_b) — all reuse.

#### G. ROM 数据地址 — compute_zone_effect_atk_delta (carve + REF)

DAT_08037ddc (value 0x09e3ef74) 指向 rom.s 内 incbin 起始地址，依用户标准必须 carve，不得 .equ。
改为 REF_SLOTS。DAT_08037de0 (0xffffef10) 是纯数值常量，保留 EQ。

| 槽 | addr | value | 处理 | 含义 | 证据 |
|----|------|-------|------|------|------|
| DAT_08037ddc | 0x08037ddc | 0x09e3ef74 | **REF** (carve label) | base ROM addr of field_spell_atk_bonus_table; 2D table [card_id-0x10f0][field_level] = s16 ATK bonus; 6 rows (card_id 0x10f0-0x10f5); 24 s16 cols; row stride=0x30; 1 ROM ref | asm:4220 ldr r3; formula: addr=r3+field_level*2+(card_id-0x10f0)*0x30; YAMI row(idx=5): col3=+200,col17=-200,col18=+200; python verified; high |
| DAT_08037de0 | 0x08037de0 | 0xffffef10 | EQ FIELD_SPELL_TABLE_IDX_BIAS | -0x10f0 (s32): added to card_id to get 0-based row index; Forest(0x10f0)->0, Yami(0x10f5)->5; high | asm:4222-4223 ldr r0; adds r2,r4,r0 -> r2=row index |

Note: Renamed from EQUIP_ATK_DELTA_TABLE/EQUIP_ATK_TABLE_NEG_IDX_OFF to FIELD_SPELL_ATK_BONUS_TABLE/FIELD_SPELL_TABLE_IDX_BIAS.
Rationale: table covers the 6 classic field spell cards (Forest..Yami), not generic equip AI.
New home: `field_spell_bonus.inc`.

#### H. Score delta constants (s32 negatives) — compute_zone_effect_atk_delta x4 (same value)

| 槽 | addr | value | 新常量名 | 含义 |
|----|------|-------|---------|------|
| DAT_08037e14 | 0x08037e14 | 0xfffffe70 | ZONE_EFFECT_ATK_PENALTY_500 | -500 (s32): ATK penalty for opponent Necrovalley/HHG; asm:4266 ldr r7 -> r7 is DEF delta; assigned after check_card_is_gravekeeper flag; high |
| DAT_08037e2c | 0x08037e2c | 0xfffffe70 | (same value, reuse ZONE_EFFECT_ATK_PENALTY_500) | 3 more slots same value |
| DAT_08037e44 | 0x08037e44 | 0xfffffe70 | (reuse) | |
| DAT_08037e5c | 0x08037e5c | 0xfffffe70 | (reuse) | |

All four slots hold 0xfffffe70 = -500 (s32). Define once in equip_ai.inc, reuse x4.

---

### REF_SLOTS (USER-label + DATA-ref)

11 REF slots total: 10 PTR_gP1LifePoints_* + 1 carve-label pointer (DAT_08037ddc).

PTR_gP1LifePoints_* x10: 全部 .word gP1LifePoints (已有 label)。
Ghidra 设 DATA-ref 指向 gP1LifePoints，GAS label 为 `<func>_lp_ptr` 形式。

DAT_08037ddc: .word field_spell_atk_bonus_table (carve label @ 0x09e3ef74)。
Ghidra: createLabel field_spell_atk_bonus_table @0x09e3ef74 USER + addMemoryReference from 0x08037ddc; 槽改名 compute_zone_effect_atk_delta_table_base。

| 槽 label | addr | target | gas_label | slot_label |
|----------|------|--------|-----------|------------|
| PTR_gP1LifePoints_08037948 | 0x08037948 | gP1LifePoints | find_field_zone_slot_with_equip_type_lp_ptr | find_field_zone_slot_with_equip_type_lp_ptr |
| PTR_gP1LifePoints_080379c8 | 0x080379c8 | gP1LifePoints | count_field_zone_cards_by_field6_lp_ptr | count_field_zone_cards_by_field6_lp_ptr |
| PTR_gP1LifePoints_08037a24 | 0x08037a24 | gP1LifePoints | count_field_zone_cards_by_field7_lp_ptr | count_field_zone_cards_by_field7_lp_ptr |
| PTR_gP1LifePoints_08037a84 | 0x08037a84 | gP1LifePoints | count_valid_monster_pair_slots_lp_ptr | count_valid_monster_pair_slots_lp_ptr |
| PTR_gP1LifePoints_08037ac8 | 0x08037ac8 | gP1LifePoints | find_zone_slot_idx_allowed_for_card_lp_ptr | find_zone_slot_idx_allowed_for_card_lp_ptr |
| PTR_gP1LifePoints_08037b2c | 0x08037b2c | gP1LifePoints | count_field_zone_cards_with_field5_lp_ptr | count_field_zone_cards_with_field5_lp_ptr |
| PTR_gP1LifePoints_08037b88 | 0x08037b88 | gP1LifePoints | count_monster_slots_field5_ge_threshold_lp_ptr | count_monster_slots_field5_ge_threshold_lp_ptr |
| PTR_gP1LifePoints_08037bac | 0x08037bac | gP1LifePoints | get_player_deck_flag_bit1_lp_ptr | get_player_deck_flag_bit1_lp_ptr |
| PTR_gP1LifePoints_08037c0c | 0x08037c0c | gP1LifePoints | check_field_effect_zone_activation_eligible_lp_ptr | check_field_effect_zone_activation_eligible_lp_ptr |
| PTR_gP1LifePoints_08037c94 | 0x08037c94 | gP1LifePoints | shuffle_hand_by_player_deck_flag_lp_ptr | shuffle_hand_by_player_deck_flag_lp_ptr |
| DAT_08037ddc | 0x08037ddc | field_spell_atk_bonus_table @0x09e3ef74 | compute_zone_effect_atk_delta_table_base | compute_zone_effect_atk_delta_table_base |

Note: DAT_08037cf4/dbc/ebc (gDuelFieldSlots 0x0201c510) and DAT_08037950 (gP1FieldArrayCBase)
are EQ (equate via DATA ref) not REF (pointer), since they are address literals used as base
pointers — assign via Ghidra setEquate.

### RENAME_SLOTS (EOL comment 更新)

| 槽 label | slot_label (rename) | eol | note |
|----------|---------------------|-----|------|
| DAT_0803794c | find_field_zone_slot_with_equip_type_stride | PLAYER_BLOCK_STRIDE | val=0x868 |
| DAT_08037950 | find_field_zone_slot_with_equip_type_field_arr_c | gP1FieldArrayCBase | val=0x0201c600 |
| DAT_08037970 | find_field_zone_slot_with_equip_type_stride_b | PLAYER_BLOCK_STRIDE | val=0x868 (loop-end reload) |
| DAT_080379cc | count_field_zone_cards_by_field6_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037a28 | count_field_zone_cards_by_field7_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037a88 | count_valid_monster_pair_slots_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037acc | find_zone_slot_idx_allowed_for_card_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037b30 | count_field_zone_cards_with_field5_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037b8c | count_monster_slots_field5_ge_threshold_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037bb0 | get_player_deck_flag_bit1_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037c04 | check_field_effect_zone_elig_eye_of_truth_cid | EYE_OF_TRUTH_CID | val=0x137b |
| DAT_08037c08 | check_field_effect_zone_elig_mind_on_air_cid | MIND_ON_AIR_CID | val=0x17e7 |
| DAT_08037c10 | check_field_effect_zone_elig_lp_field_off | P1LP_BLOCK2_OFF_1CE8 | val=0x1ce8 |
| DAT_08037c14 | check_field_effect_zone_elig_respect_play_cid | RESPECT_PLAY_CID | val=0x135e |
| DAT_08037c98 | shuffle_hand_by_player_deck_flag_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037cf0 | compute_zone_effect_atk_delta_stride | PLAYER_BLOCK_STRIDE | |
| DAT_08037cf4 | compute_zone_effect_atk_delta_slots | gDuelFieldSlots | val=0x0201c510 |
| DAT_08037d30 | compute_zone_effect_atk_delta_range_max_cid | MOLTEN_DESTRUCTION_CID | val=0x1346 |
| DAT_08037d34 | compute_zone_effect_atk_delta_range_min_cid | YAMI_CID | val=0x10f5 |
| DAT_08037d48 | compute_zone_effect_atk_delta_gaia_power_cid | GAIA_POWER_CID | val=0x1344 |
| DAT_08037d68 | compute_zone_effect_atk_delta_mystic_plasma_cid | MYSTIC_PLASMA_ZONE_CID | val=0x1349 |
| DAT_08037d80 | compute_zone_effect_atk_delta_necrovalley_cid | NECROVALLEY_CID | val=0x159d |
| DAT_08037d8c | compute_zone_effect_atk_delta_harpies_hunt_cid | HARPIES_HUNTING_GROUND_CID | val=0x183f |
| DAT_08037db8 | compute_zone_effect_atk_delta_stride_b | PLAYER_BLOCK_STRIDE | |
| DAT_08037dbc | compute_zone_effect_atk_delta_slots_b | gDuelFieldSlots | val=0x0201c510 |
| DAT_08037ddc | compute_zone_effect_atk_delta_table_base | field_spell_atk_bonus_table (carve label) | val=0x09e3ef74; REF not EQ |
| DAT_08037de0 | compute_zone_effect_atk_delta_table_idx_bias | FIELD_SPELL_TABLE_IDX_BIAS | val=0xffffef10 |
| DAT_08037e14 | compute_zone_effect_atk_delta_penalty_a | ZONE_EFFECT_ATK_PENALTY_500 | val=0xfffffe70 |
| DAT_08037e2c | compute_zone_effect_atk_delta_penalty_b | ZONE_EFFECT_ATK_PENALTY_500 | same val |
| DAT_08037e44 | compute_zone_effect_atk_delta_penalty_c | ZONE_EFFECT_ATK_PENALTY_500 | same val |
| DAT_08037e5c | compute_zone_effect_atk_delta_penalty_d | ZONE_EFFECT_ATK_PENALTY_500 | same val |
| DAT_08037eb8 | compute_zone_effect_atk_delta_stride_c | PLAYER_BLOCK_STRIDE | |
| DAT_08037ebc | compute_zone_effect_atk_delta_slots_c | gDuelFieldSlots | val=0x0201c510 |

### FUNC_RENAME

| 函数地址 | 旧名 | 新名 | 理由 | 置信度 |
|----------|------|------|------|--------|
| 0x08037974 | count_gy_cards_by_field6 | count_field_zone_cards_by_field6 | 函数体读 gP1LP+player*0x868+0x120 (gP1FieldArrayCBase, field zone array C, zone_type=0xb equip区)，count 在 +0x0c；墓地在 +0x5d0 (count +0x1c)，offset 完全不同；"gy" (graveyard) 与函数体矛盾；兄弟 count_field_zone_cards_by_field7 同一 array | high |

落地时需: Ghidra rename + asm 重导 + ExportFunctionInventory + sync_ghidra_names_to_proposals + 手改 naming-proposals.csv 对应行。
同步订正该函数 plate 文本中所有 "graveyard" 及 "gy" 自指措辞为 "field zone array C"。
同步订正 REF_SLOTS 中 PTR_gP1LifePoints_080379c8 的 gas_label/slot_label:
  旧: count_gy_cards_by_field6_lp_ptr
  新: count_field_zone_cards_by_field6_lp_ptr

### PLATE (R5 full rewrite — ASCII)

12 函数全部需要 plate 校验/更新。以下标注 [STALE_FUN] 的需同步修正：

| fn addr | 当前状态 | action |
|---------|---------|--------|
| 0x08037904 find_field_zone_slot_with_equip_type | plate OK, no FUN_ | update EOL for new const names |
| 0x08037974 count_field_zone_cards_by_field6 (renamed) | plate CJK comment present (line 3594) | R5 rewrite plate ASCII, CJK to doc/; rename applied via FUNC_RENAME |
| 0x080379d0 count_field_zone_cards_by_field7 | plate OK | verify no FUN_ |
| 0x08037a2c count_valid_monster_pair_slots | plate OK | verify no FUN_ |
| 0x08037a8c find_zone_slot_idx_allowed_for_card | plate OK | verify |
| 0x08037ae4 count_field_zone_cards_with_field5 | plate OK | verify |
| 0x08037b34 count_monster_slots_with_field5_ge_threshold | **[STALE_FUN]** FUN_080ae050 | replace FUN_080ae050 -> find_empty_slot_for_card_id_dispatch |
| 0x08037b90 get_player_deck_flag_bit1 | **[STALE_FUN]** FUN_08037c20 | replace FUN_08037c20 -> shuffle_hand_by_player_deck_flag |
| 0x08037bb4 check_field_effect_zone_activation_eligible | plate OK | verify |
| 0x08037c20 shuffle_hand_by_player_deck_flag | plate OK | verify |
| 0x08037c9c compute_zone_effect_atk_delta | plate OK | update const refs |

Plate full text (proposed ASCII, for fixer):

**count_field_zone_cards_by_field6 @ 0x08037974** (renamed from count_gy_cards_by_field6):
```
Iterates field zone array C for player (gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x120,
count at +0x0c). Extracts bits[12:0] as card_id per entry, calls
get_card_extended_stat_field6; if field6==r8 (non-APCS, caller-set via mov r8,r1),
increments counter. Returns match count. Symmetric to count_field_zone_cards_by_field7
(same gP1FieldArrayCBase base, different stat field). Pure read-only.
r0=u8 player_id [0..1]; r1 (non-APCS saved r8)=u8 field6_target.
Returns u32 count.
Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.
```

**count_monster_slots_with_field5_ge_threshold @ 0x08037b34** (fix FUN_):
```
Iterates monster zone cards for player (gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x120,
count at +0x0c). Calls get_card_extended_stat_field5; if field5 >= threshold (r8
non-APCS, caller-set via mov r8,r1), increments counter. Returns match count.
Caller: find_empty_slot_for_card_id_dispatch (with r1=7). Pure read-only.
r0=u32 player_side [0..1]; r1=u32 field5_threshold [0..255] (non-APCS saved r8).
Returns u32 count.
Constants: gP1FieldArrayCBase; PLAYER_BLOCK_STRIDE.
```

**get_player_deck_flag_bit1 @ 0x08037b90** (fix FUN_):
```
Returns bit1 of deck status word for specified player. Reads
gP1LifePoints + (r0&1)*PLAYER_BLOCK_STRIDE + 0x11c (=0x8e*2), extracts bit1 via
lsrs #1 & 1. Pure read-only.
Callers: shuffle_hand_by_player_deck_flag (skip-deck-sort guard);
get_zone_card_attribute_by_type case_b (conditional 0/1 return).
r0=u32 packed_player_id (bit0=player index [0..1]).
Returns u32 (0 or 1).
Constants: gP1LifePoints; PLAYER_BLOCK_STRIDE; deck_status_word_offset=0x11c.
```

---

## carve 计划 (R7)

### carve-1: field_spell_atk_bonus_table @ ROM off 0x1E3EF74 (0x120 B)

该表由 DAT_08037ddc 引用 (raw=1)，当前落在 rom.s incbin 起始处，必须 carve。

**目标 rom.s 位置**: line 1236 附近 `.incbin "roms/2343.gba", 0x1E3EF74, 0xAD98`

**拆分方案**:
```asm
field_spell_atk_bonus_table:                    @ GBA 0x09e3ef74; 6x24 s16 ATK bonus table
    .incbin "roms/2343.gba", 0x1E3EF74, 0x120   @ table data (6 rows x 24 s16, stride=0x30)
    .incbin "roms/2343.gba", 0x1E3F094, 0xAC78  @ remainder [0x1E3F094..0x1E4A10B]
```
等式验证: 0x120 + 0xAC78 = 0xAD98 == 原 incbin 大小 (✓)
偏移验证: 0x1E3EF74 + 0x120 = 0x1E3F094 (✓)

**对接说明**: 此表紧接 file02-Seg9 已 carve 的 available_slot_order_table@0x09e3ef60 之后
(0x09e3ef60 + 0x14 = 0x09e3ef74)。落地时 fixer 核实 rom.s 实际行再执行拆分。

**Ghidra**: 同步删除 field_spell_bonus.inc 中的 FIELD_SPELL_ATK_BONUS_TABLE .equ 行；
createLabel field_spell_atk_bonus_table @0x09e3ef74 USER；addMemoryReference from 0x08037ddc。

Seg-4b 的 jump table carve (PTR_DAT_0803931c) 留 F03Seg4b proposal。

---

## disasm 计划 (R4)

Seg-4a 内无 ROM_INCBIN，无 disasm 需求。

Seg-4b incbin @0x39350/0x10ce 需 R4 逐 stub disasm — 留 F03Seg4b proposal：
- 先 clearListing 0x08039350..0x0803a41e
- setTMode(0x08039350..0x0803a41e, THUMB)
- 按 jump table 5 个唯一目标 (0x08039350 / 0x08039a62 / 0x08039a7c / 0x08039c1c /
  0x0803a3c4 / 0x0803a2fc) 逐 stub DisassembleCommand (单次 range 只 disasm 首 stub)

---

## 新增 constants

### field_spell_bonus.inc (新建; 替代之前草案中的 equip_ai.inc)

注: FIELD_SPELL_ATK_BONUS_TABLE 是 ROM 地址，改 carve 进 rom.s，不在此 .inc 中定义。
仅保留两个纯数值常量 (偏置 + 惩罚分)。

```asm
@ =============================================================================
@ Field spell ATK bonus constants
@ Source: asm/03_equip_chain_hand.s Seg-4a (0x08037904..0x08037ec0)
@ =============================================================================

@ Row index bias for field_spell_atk_bonus_table
@ table[card_id + FIELD_SPELL_TABLE_IDX_BIAS][field_level] = s16 ATK bonus
@ 6 rows (card_id 0x10f0..0x10f5 = Forest/Wasteland/Mountain/Sogen/Umi/Yami)
.equ FIELD_SPELL_TABLE_IDX_BIAS,  0xffffef10  @ -0x10f0 (s32): card_id + bias = 0-based row index;
                                               @ Forest(0x10f0)->0, Yami(0x10f5)->5;
                                               @ 1 ROM ref (compute_zone_effect_atk_delta)

@ Necrovalley / Harpies Hunting Ground ATK/DEF penalty (s32)
.equ ZONE_EFFECT_ATK_PENALTY_500, 0xfffffe70  @ -500 (s32): ATK/DEF score penalty for opponent
                                               @ Necrovalley / Harpies' Hunting Ground zone effects;
                                               @ 4 ROM refs (compute_zone_effect_atk_delta)
```

### card_info.inc 追加 (9 新 CID)

```asm
@ file 03 Seg-4a additions (compute_zone_effect_atk_delta + check_field_effect_zone_activation_eligible)

@ Field-effect zone activation eligibility guard cards
.equ EYE_OF_TRUTH_CID,            0x0000137b  @ The Eye of Truth (pw=34694160; card-stats.s card_0791 slot=0x137b);
                                               @ check_field_effect_zone_activation_eligible guard;
                                               @ 2 ROM refs; data.md=0x137B
.equ MIND_ON_AIR_CID,             0x000017e7  @ Mind on Air (pw=66690411; card-stats.s card_1652 slot=0x17e7 L21491);
                                               @ check_field_effect_zone_activation_eligible guard;
                                               @ 2 ROM refs; data.md=0x17E7
.equ RESPECT_PLAY_CID,            0x0000135e  @ Respect Play (pw=08073514; card-stats.s card_0766 slot=0x135e);
                                               @ check_field_effect_zone_activation_eligible gP1LP+0x1ce8 guard;
                                               @ 2 ROM refs; data.md=0x135E

@ ATK delta table card ID range bounds (compute_zone_effect_atk_delta)
.equ YAMI_CID,                    0x000010f5  @ Yami (pw=59197169; card-stats.s card_0297 slot=0x10f5 L3876);
                                               @ lower bound: card_id <= YAMI -> field-spell ATK bonus table path;
                                               @ 2 ROM refs; data.md=0x10F5
.equ MOLTEN_DESTRUCTION_CID,      0x00001346  @ Molten Destruction (pw=19384334; card-stats.s card_0747 slot=0x1346);
                                               @ upper bound of card-dispatch binary-search; card_id > this -> separate branch;
                                               @ 2 ROM refs; data.md=0x1346
.equ GAIA_POWER_CID,              0x00001344  @ Gaia Power (pw=56594520; card-stats.s card_0745 slot=0x1344);
                                               @ compute_zone_effect_atk_delta binary-search node;
                                               @ 2 ROM refs; data.md=0x1344
.equ MYSTIC_PLASMA_ZONE_CID,      0x00001349  @ Mystic Plasma Zone (pw=18161786; card-stats.s card_0750 slot=0x1349);
                                               @ compute_zone_effect_atk_delta exact cmp;
                                               @ 2 ROM refs; data.md=0x1349
.equ NECROVALLEY_CID,             0x0000159d  @ Necrovalley (pw=47355498; card-stats.s card_1185 slot=0x159d);
                                               @ compute_zone_effect_atk_delta gravekeeper-check branch;
                                               @ 2 ROM refs; data.md=0x159D
.equ HARPIES_HUNTING_GROUND_CID,  0x0000183f  @ Harpies' Hunting Ground (pw=75782277; card-stats.s card_1731 slot=0x183f);
                                               @ compute_zone_effect_atk_delta exact cmp;
                                               @ 2 ROM refs; data.md=0x183F
```

---

## §5.1 登记 (Rule 3) — 0 引用块

Seg-4a 无 ROM_INCBIN 块，无 §5.1 登记需要。

---

## 消費者证据 (R6) — 关键槽语义

| 槽 | 语义 | file:line | 置信度 |
|----|------|-----------|--------|
| DAT_08037c04=0x137b | EYE_OF_TRUTH_CID: param to count_available_effect_zones | asm:03_equip_chain_hand.s:3966 (bl addr 0x08037bc6); card-stats.s card_0791 slot=0x137b | high |
| DAT_08037c08=0x17e7 | MIND_ON_AIR_CID: param to count_available_effect_zones | asm:03_equip_chain_hand.s:3968 (bl addr 0x08037be0); card-stats.s card_1652 slot=0x17e7 L21491 | high |
| DAT_08037c14=0x135e | RESPECT_PLAY_CID: param to count_field_copies_of_card | asm:03_equip_chain_hand.s:3974 (bl addr 0x08037bf6); card-stats.s card_0766 slot=0x135e | high |
| DAT_08037ddc=0x09e3ef74 | field_spell_atk_bonus_table (carve label): 2D table; rows=card_id-0x10f0 (Forest..Yami), cols=field_level s16 ATK bonus; stride=0x30; YAMI(idx=5): col3=+200,col17=-200,col18=+200 | asm:03_equip_chain_hand.s:4220 ldr r3; byte formula: r3+field_level*2+(card_id-0x10f0)*0x30; python verified 6 rows | high |
| DAT_08037de0=0xffffef10 | FIELD_SPELL_TABLE_IDX_BIAS: -0x10f0 (s32); card_id+bias=row_idx; Forest->0, Yami->5 | asm:03_equip_chain_hand.s:4222-4223 ldr r0; adds r2,r4,r0 | high |
| DAT_08037e14..e5c=0xfffffe70 x4 | ZONE_EFFECT_ATK_PENALTY_500: -500 (s32) ATK/DEF score penalty for opponent Necrovalley/HHG effects | asm:03_equip_chain_hand.s:4263-4307 ldr r7,DAT_*; r7=DEF delta; .hword 0x4691=mov r9,r2 for ATK delta | high |

---

## 求助

None. All items resolved:

1. **MIND_ON_AIR_CID = 0x17e7**: CONFIRMED card-stats.s card_1652 slot=0x17e7 L21491 (was incorrectly flagged as gap slot). Confidence upgraded to high.

2. **FIELD_SPELL_ATK_BONUS_TABLE stride**: CONFIRMED stride=0x30 per row, 24 s16 columns indexed by field_level [0..23]. Table covers 6 classic field-spell cards (Forest/Wasteland/Mountain/Sogen/Umi/Yami, card_id 0x10f0..0x10f5). Formula verified: addr = table_base + (card_id-0x10f0)*0x30 + field_level*2. Fixer should verify CHORUS_OF_SANCTUARY (0x1323) uses the separate LAB_08037d90 zone-field-lookup path (not the 2D table).

---

## 自检 (Phase 4)

1. **EQ values vs ROM bytes**:
   - 0x0803794c: d[0x3794c..0x3794f] = little-endian 0x00000868 confirmed (PLAYER_BLOCK_STRIDE)
   - 0x08037950: d[0x37950..0x37953] = 0x0201c600 confirmed (gP1FieldArrayCBase)
   - 0x08037d30: d[0x37d30..0x37d33] = 0x00001346 confirmed (MOLTEN_DESTRUCTION_CID)
   - 0x08037ddc: d[0x37ddc..0x37ddf] = 0x09e3ef74 confirmed (field_spell_atk_bonus_table carve label)
   - 0x08037e14: d[0x37e14..0x37e17] = 0xfffffe70 confirmed (ZONE_EFFECT_ATK_PENALTY_500)
   - FIELD_SPELL_ATK_BONUS_TABLE: YAMI row (ROM off 0x1e3f064) col3=200, col17=-200, col18=200 confirmed; stride=0x30; 6 rows card_ids 0x10f0..0x10f5 verified

2. **carve-1 in Seg-4a**: field_spell_atk_bonus_table @0x09e3ef74 is a data table (not fn-ptr), no +1. incbin split: 0x120 + 0xAC78 = 0xAD98 (original size) ✓; 0x1E3EF74 + 0x120 = 0x1E3F094 ✓.

3. **Plate/EOL ASCII**: all proposed plate text above uses ASCII only (no CJK).

4. **§5.1**: 0 incbin blocks in Seg-4a, no §5.1 entries needed.

5. **Slot name format**: all `^[a-z][a-z0-9_]+$`; stride_b / slots_b suffixes avoid collision within same function. Verified above.

---

## Executor Report: F03Seg4a (rev2, post-review fixes)

- 槽: EQ=32 REF=11 RENAME=33 FUNC_RENAME=1 PLATE=11
- carve=1 (field_spell_atk_bonus_table @0x1E3EF74/0x120B) disasm=0 §5.1=0
- 新增 constants/全局: field_spell_bonus.inc (新建, 2 constants: FIELD_SPELL_TABLE_IDX_BIAS / ZONE_EFFECT_ATK_PENALTY_500; FIELD_SPELL_ATK_BONUS_TABLE 改 carve label); card_info.inc +9 CID (EYE_OF_TRUTH / MIND_ON_AIR / RESPECT_PLAY / YAMI / MOLTEN_DESTRUCTION / GAIA_POWER / MYSTIC_PLASMA_ZONE / NECROVALLEY / HARPIES_HUNTING_GROUND)
- 求助: none
- FUNC_RENAME: count_gy_cards_by_field6 → count_field_zone_cards_by_field6 (函数读 gP1FieldArrayCBase +0x120, 非墓地 +0x5d0); 需 ExportFunctionInventory + CSV sync
- C3 card_XXXX 订正: EYE_OF_TRUTH card_0791; RESPECT_PLAY card_0766; NECROVALLEY card_1185; HARPIES_HUNTING_GROUND card_1731
- 订正统计说明: EQ 从 34→32 (DAT_08037ddc 由 EQ 改 REF carve); REF 从 9→11 (加 DAT_08037ddc; 实际 PTR_gP1LifePoints 共 10 项); PLATE 从 12→11 (eval_slot_score_entry_full 属 Seg-4b); FUNC_RENAME 从 0→1
- Seg-4b 边界: 0x08037ec0 (eval_slot_score_entry_full); incbin @0x39350/0x10ce R4 disasm 留 F03Seg4b proposal
- proposal: doc/dev/refine/F03Seg4a.proposal.md
