# Refine Proposal: F06-Seg-7  [0x08058550..0x08058cec)

## 段测绘

- 函数入口 x22:
  - 0x08058550  tick_equip_activation_neo_daedalus_gate
  - 0x08058578  dispatch_equip_zone_sprite_by_slot_group
  - 0x08058598  load_equip_set_code_with_zone14_test
  - 0x080585c4  enqueue_effect_slot_sprite_by_equip_tier
  - 0x080585e8  tick_equip_activation_phase_with_effect_enqueue
  - 0x0805861c  enqueue_sprite_type11_plain_for_slot
  - 0x08058638  check_equip_slot_has_active_effect_value
  - 0x08058684  tick_equip_tier_abcx_sprite_display_seq
  - 0x08058754  set_lp_row_type2_for_equip_tier_abc_neutral
  - 0x08058778  dispatch_equip_lp_cost_and_zone_sprite
  - 0x08058794  dispatch_banisher_lp_row_by_card_id_in_zone
  - 0x080587c0  enqueue_lp_row_type2_for_equip_slot
  - 0x080587e0  tick_equip_sprite_with_attr11_if_seq_zero
  - 0x08058828  tick_equip_sprite_if_seq_zero
  - 0x08058858  tick_equip_activation_with_sprite_mode2
  - 0x0805888c  tick_equip_effect_activation_display_seq
  - 0x08058a04  set_lp_row_type2_for_entry_player
  - 0x08058a1c  tick_equip_activation_if_effect_dispatch_ok
  - 0x08058a40  check_zone_entity_field6_in_equip_range
  - 0x08058a98  tick_equip_zone_target_select_display_seq
  - 0x08058c2c  test_equip_zone14_for_slot_player_at_10
  - 0x08058c40  tick_equip_zone_select_display_seq_short
- 残留自动名槽: 58 个 (DWORD_/DAT_/PTR_)，全为字面池
- ROM_INCBIN / .byte 块: 0 (实测确认无 ROM_INCBIN)

## 数据块分类 (Rule 2/3)

ref-scan 确认无 ROM_INCBIN 块，本段无需数据块分类表。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 全部复用现有 inc 或新建)

共 53 个 EQ 槽，按唯一值分组：

#### gDuelPhaseFlags = 0x0201b290 (ewram.inc 复用) — 12 槽

| 槽地址 | value | 槽 label (建议) |
|--------|-------|-----------------|
| 0x080586a0 | 0x0201b290 | tick_equip_tier_abcx_state_base |
| 0x0805874c | 0x0201b290 | tick_equip_tier_abcx_state_base_b |
| 0x0805881c | 0x0201b290 | tick_equip_sprite_attr11_state_base |
| 0x08058850 | 0x0201b290 | tick_equip_sprite_state_base |
| 0x080588b0 | 0x0201b290 | tick_equip_effect_act_state_base |
| 0x080589a4 | 0x0201b290 | tick_equip_effect_act_state_base_b |
| 0x08058a88 | 0x0201b290 | check_zone_field6_state_base |
| 0x08058ab4 | 0x0201b290 | tick_equip_zone_target_state_base |
| 0x08058b2c | 0x0201b290 | tick_equip_zone_target_state_base_b |
| 0x08058ba0 | 0x0201b290 | tick_equip_zone_target_state_base_c |
| 0x08058c58 | 0x0201b290 | tick_equip_zone_select_state_base |
| 0x08058cac | 0x0201b290 | tick_equip_zone_select_state_base_b |

#### EQUIP_ACTIVATION_STEP_OFF = 0x000004ac (duel_field.inc 复用) — 12 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x080586a4 | 0x000004ac | tick_equip_tier_abcx_step_off |
| 0x08058750 | 0x000004ac | tick_equip_tier_abcx_step_off_b |
| 0x08058820 | 0x000004ac | tick_equip_sprite_attr11_step_off |
| 0x08058854 | 0x000004ac | tick_equip_sprite_step_off |
| 0x080588b4 | 0x000004ac | tick_equip_effect_act_step_off |
| 0x080589a8 | 0x000004ac | tick_equip_effect_act_step_off_b |
| 0x080589f0 | 0x000004ac | tick_equip_effect_act_step_off_c |
| 0x08058ab8 | 0x000004ac | tick_equip_zone_target_step_off |
| 0x08058b30 | 0x000004ac | tick_equip_zone_target_step_off_b |
| 0x08058ba4 | 0x000004ac | tick_equip_zone_target_step_off_c |
| 0x08058c5c | 0x000004ac | tick_equip_zone_select_step_off |
| 0x08058cb0 | 0x000004ac | tick_equip_zone_select_step_off_b |

#### gP1LifePoints = 0x0201c4e0 (ewram.inc 复用) — 9 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x0805872c | 0x0201c4e0 | tick_equip_tier_abcx_gp1lp |
| 0x08058958 | 0x0201c4e0 | tick_equip_effect_act_gp1lp |
| 0x08058980 | 0x0201c4e0 | tick_equip_effect_act_gp1lp_b |
| 0x080589c0 | 0x0201c4e0 | tick_equip_effect_act_gp1lp_c |
| 0x08058af8 | 0x0201c4e0 | tick_equip_zone_target_gp1lp |
| 0x08058b08 | 0x0201c4e0 | tick_equip_zone_target_gp1lp_b |
| 0x08058b48 | 0x0201c4e0 | tick_equip_zone_target_gp1lp_c |
| 0x08058be4 | 0x0201c4e0 | tick_equip_zone_target_gp1lp_d |
| 0x08058cd4 | 0x0201c4e0 | tick_equip_zone_select_gp1lp |

#### ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (ewram.inc 复用) — 4 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058730 | 0x00001d68 | tick_equip_tier_abcx_lp_off |
| 0x08058bec | 0x00001d68 | tick_equip_zone_target_lp_off |
| 0x08058c10 | 0x00001d68 | tick_equip_zone_target_lp_off_b |
| 0x08058cd8 | 0x00001d68 | tick_equip_zone_select_lp_off |

#### gDuelCardCtxBase = 0x0201e2a0 (ewram.inc 复用) — 4 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x0805897c | 0x0201e2a0 | tick_equip_effect_act_ctx_base |
| 0x08058af4 | 0x0201e2a0 | tick_equip_zone_target_ctx_base |
| 0x08058b7c | 0x0201e2a0 | tick_equip_zone_target_ctx_base_b |
| 0x08058c8c | 0x0201e2a0 | tick_equip_zone_select_ctx_base |

#### PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc 复用) — 2 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058674 | 0x00000868 | check_equip_slot_has_stride |
| 0x08058bf4 | 0x00000868 | tick_equip_zone_target_stride |

#### LP_BANISHER_CTX_OFF = 0x00001d70 (新建 ewram.inc) — 2 槽

语义: `[gP1LifePoints+0x1d70]` = banisher zone LP 上下文存储字段; 在
`tick_equip_effect_activation_display_seq` (line 12599) 中注明为 LP_BANISHER_OFF；
在 `tick_equip_zone_target_select_display_seq` (line 12924) 注明为 LP_STEP2_OFF；
在 `tick_equip_zone_select_display_seq_short` (line 13172) 注明为 LP_BANISHER_OFF。
与 ELIGIB_SPRITE_CTRL_OFF (0x1d68) 相邻 +8，与 ELIGIB_ANIM_STATE_OFF (0x1d6c) 相邻 +4；
39 ROM refs。
grep `constants/*.inc` 0x00001d70 命中 0 → 新建。
建议名: LP_BANISHER_CTX_OFF (high-conf: 多处注明 LP_BANISHER_OFF，banisher 路径使用)

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058bf0 | 0x00001d70 | tick_equip_zone_target_lp_step2_off |
| 0x08058c14 | 0x00001d70 | tick_equip_zone_target_lp_step2_off_b |

#### gDuelFieldSlots = 0x0201c510 (ewram.inc 复用) — 1 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058678 | 0x0201c510 | check_equip_slot_has_slots_base |

#### CRIMSON_NINJA_CID = 0x000016b8 (新建 card_info.inc) — 1 槽

确认: card_stats.s card_1404: "Crimson Ninja slot=0x16B8 pw=14618326" (high-conf)。
asm/07_equip_effect_chain.s line 794: `CARD_ID_CRIMSON_NINJA=0x16b8 (Crimson Ninja)` (high-conf)。
grep `constants/card_info.inc` 0x000016b8 命中 0 → 新建。

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058824 | 0x000016b8 | tick_equip_sprite_attr11_crimson_ninja_cid |

#### BLACK_LUSTER_SOLDIER_ENVOY_CID = 0x000016cb (card_info.inc 复用) — 1 槽

已有: `constants/card_info.inc` line 746。
用途: `tick_equip_activation_with_sprite_mode2` 中作为 `enqueue_sprite_attr_with_mode` 参数 sprite_data=0x16cb (BLS-Envoy 卡图索引)。

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058888 | 0x000016cb | tick_equip_act_sprite_mode2_bls_data |

#### LP_BAR_ANIM_STATE_OFF = 0x000004cc (ewram.inc 复用) — 1 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x0805894c | 0x000004cc | tick_equip_effect_act_node_count_off |

注: 在 `tick_equip_effect_activation_display_seq` 中用作 `NODE_COUNT_OFF=0x4cc`，语义为迭代计数，但值与 LP_BAR_ANIM_STATE_OFF 相同；ewram.inc 注释已提到 node count；复用正确（C5: 不同语义但同值 → 复用并 EOL 注明实际用途）。

#### SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4 (ewram.inc 复用) — 1 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058950 | 0x000004d4 | tick_equip_effect_act_node_zone_off |

注: 在此函数中用作 `NODE_ZONE_OFF=0x4d4` (节点区域字节偏移)。与 SPRITE_ROW_ENTRY_DATA_OFF 同值；复用。

#### CHAIN_NODE_CARD_ARR_OFF = 0x000004f4 (ewram.inc 复用) — 1 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058954 | 0x000004f4 | tick_equip_effect_act_node_slot_off |

注: 在此函数中用作 `NODE_SLOT_OFF=0x4f4` (节点 slot 偏移)。ewram.inc 已定义 CHAIN_NODE_CARD_ARR_OFF=0x4f4；复用。

#### ELIGIB_ANIM_STATE_OFF = 0x00001d6c (ewram.inc 复用) — 1 槽

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058be8 | 0x00001d6c | tick_equip_zone_target_anim_state_off |

注: 在 `tick_equip_zone_target_select_display_seq` 中用作 `[gDuelPhaseFlags+0x1d6c]` 读值 (实际是 `gP1LifePoints+0x1d6c = ELIGIB_ANIM_STATE_OFF`)。确认 DWORD_08058be4 = gP1LifePoints (基址) + DWORD_08058be8 = 0x1d6c，实际访问 `gP1LifePoints+0x1d6c`；这与 `ELIGIB_ANIM_STATE_OFF` 语义一致。

#### EQUIP_ACTIVE_CTX_OFF = 0x00000484 (新建 duel_field.inc) — 1 槽

语义: `[gDuelPhaseFlags+0x484]` = 当前 equip 激活上下文槽指针 (current active equip context slot ptr)。
多文件确认:
- asm/06 line 12843: "Reads activation slot ptr from [0x0201b290+0x484]" (high-conf)
- asm/08_equip_oam_neodaed.s line 19128: "gIwramState[+0x484] = current active node" (high-conf)
- asm/09_equip_lp_display.s line 17878: "active effect node pointer from IWRAM state table 0x0201b290[0x484]" (high-conf)
- asm/10_equip_effect_dispatch.s line 15465: "SLOT_SNAPSHOT_OFFSET=0x484"
- 46 ROM literal pool refs; grep `constants/*.inc` 0x00000484 命中 0 → 新建。

| 槽地址 | value | 槽 label |
|--------|-------|----------|
| 0x08058a8c | 0x00000484 | check_zone_field6_ctx_off |

### REF_SLOTS (USER-label + DATA-ref; THUMB fn-ptr)

共 5 个 REF 槽：

| 槽地址 | target_raw | gas_label | 槽 label |
|--------|-----------|-----------|----------|
| 0x080586f0 | 0x08058639 | check_equip_slot_has_active_effect_value+1 | tick_equip_tier_abcx_mode_fn_ptr |
| 0x08058b80 | 0x08058a41 | check_zone_entity_field6_in_equip_range+1 | tick_equip_zone_target_pred_ptr |
| 0x08058b9c | 0x08058a41 | check_zone_entity_field6_in_equip_range+1 | tick_equip_zone_target_pred_ptr_b |
| 0x08058c90 | 0x08065991 | check_equip_activation_at_slot11+1 | tick_equip_zone_select_slot_tbl_ptr |
| 0x08058ca8 | 0x08065991 | check_equip_activation_at_slot11+1 | tick_equip_zone_select_slot_tbl_ptr_b |

注:
- `0x08058639` = `check_equip_slot_has_active_effect_value` 函数起始地址 0x08058638 + 1 (THUMB); 1 ROM ref (DWORD_080586f0 alone); verified.
- `0x08058a41` = `check_zone_entity_field6_in_equip_range` 函数起始 0x08058a40 + 1 (THUMB); 2 ROM refs; both verified slots in seg-7.
- `0x08065991` = `check_equip_activation_at_slot11` (asm/08_equip_oam_neodaed.s line 3289) 起始 0x08065990 + 1 (THUMB); 18 ROM refs (2 in seg-7, remainder in seg-8/9/10 + other modules); function confirmed named.

### RENAME_SLOTS (纯改名 + EOL)

本段 DWORD_/DAT_ 均为字面池，全部通过 EQ 或 REF 覆盖，无纯 RENAME 残余。

### FUNC_RENAME (误名订正)

无 (本段所有 22 函数命名正确，无矛盾)。

### PLATE (R5; CJK mojibake 整段 ASCII 重写)

共 4 个 CJK mojibake plate + 1 个 stale FUN_ 需修复：

**P1: dispatch_equip_zone_sprite_by_slot_group (0x08058578)**
板前 comment (line 12097) 为 CJK mojibake。ASCII 重写:
```
Dispatcher: extracts slot_group = card_entry[+2].bits[6:2] (5-bit, via lsls #0x1a; lsrs #0x1b).
If slot_group > 4 calls dispatch_equip_activation_score_by_card_id (special path, slots [5..31]).
Else calls enqueue_equip_zone_sprite_at_slot (normal OAM sprite write, slots [0..4]).
Pass-through callee return value. indeg=0 (fn-ptr table driven). Exit: pop{r1}; bx r1.
Params: r0=card_entry_ptr. Returns: r0=u32 callee return pass-through.
```

**P2: tick_equip_activation_phase_with_effect_enqueue (0x080585e8)**
板前 comment (line 12167) 为 CJK mojibake。ASCII 重写:
```
Equip activation phase tick with effect sprite enqueue as phase-complete side effect.
r0=card_entry_ptr. Calls tick_equip_activation_state_by_phase; if returns 0 (phase
not complete) returns 0. If returns nonzero (phase complete): checks card_entry[+3].bits[5:4]
(mask 0x30); if ==0 (normal equip type) extracts player_id (bit0) and slot_group (bits[6:2])
from [+2], calls enqueue_effect_card_slot_sprite_attr(player_id, slot_group, mode=3); if !=0
(special type) skips sprite enqueue. Returns 1 (phase tick complete). indeg=0 (fn-ptr driven).
Exit: pop{r4}; pop{r1}; bx r1.
```

**P3: tick_equip_activation_with_sprite_mode2 (0x08058858)**
板前 comment (line 12568) 为 CJK mojibake + stale `FUN_0805a1dc` (应为 `tick_equip_activation_sprite_mode2_by_type`). ASCII 重写 + FUN_ 替换:
```
Equip activation state machine entry wrapper with mode=2 sprite enqueue.
Called by tick_equip_activation_sprite_mode2_by_type when type_code==0x3c0.
Calls tick_equip_activation_state_machine; saves result r5. If r5==1 (slot selected):
extracts player_id and slot_group from card_entry[+2], calls
enqueue_sprite_attr_with_mode(player_id, slot_group, 0x16cb=BLACK_LUSTER_SOLDIER_ENVOY_CID,
extra=0, mode=2) to enqueue mode=2 sprite attr. Pass-through r5. indeg=1.
Exit: pop{r4,r5}; pop{r1}; bx r1.
Params: r0=card_entry_ptr; r1=secondary_ptr. Returns: r0=u32 tick result pass-through.
```

**P4: tick_equip_activation_if_effect_dispatch_ok (0x08058a1c)**
板前 comment (line 12821) 为 CJK mojibake。ASCII 重写:
```
Equip activation state machine conditional entry wrapper with effect dispatch pre-check.
indeg=0, Sub-type A. Receives card_entry_ptr(r0) and secondary_ptr(r1).
Calls dispatch_effect_by_card_id_with_display_lookup(card_entry, secondary_ptr);
if returns 0 (effect unavailable) returns -1. If passes, calls tick_equip_activation_state_machine
and pass-through its result. Exit: pop{r4,r5}; pop{r1}; bx r1.
Params: r0=card_entry_ptr; r1=secondary_ptr.
Returns: r0=i32 (-1=effect dispatch failed, else tick_equip_activation_state_machine result).
```

## carve 计划 (R7)

无 (段内无 ROM_INCBIN)。

## disasm 计划 (R4)

无 (段内无误标数据块，无 THUMB 代码混入)。

## 新增 constants / 全局

**新建 (共 3 条):**

1. `constants/card_info.inc` +1:
   - `CRIMSON_NINJA_CID = 0x000016b8`
     evidence: card_stats.s card_1404 "Crimson Ninja slot=0x16B8 pw=14618326" + asm/07 line 794
     (high-conf)

2. `constants/ewram.inc` +1:
   - `LP_BANISHER_CTX_OFF = 0x00001d70`
     `[gP1LifePoints+0x1d70]` banisher zone LP context field; 39 ROM refs;
     asm/06 line 12605 "LP_BANISHER_OFF=0x1d70"; line 12924 "LP_STEP2_OFF=0x1d70"; high-conf.

3. `constants/duel_field.inc` +1:
   - `EQUIP_ACTIVE_CTX_OFF = 0x00000484`
     `[gDuelPhaseFlags+0x484]` current equip activation context slot ptr; 46 ROM refs;
     asm/06 line 12851 "ACTIVATION_OFFSET=0x484"; asm/09 line 17878 "ACTIVE_NODE_OFFSET=0x484";
     high-conf.

**复用 (无需新建):**
- gDuelPhaseFlags=0x0201b290, EQUIP_ACTIVATION_STEP_OFF=0x000004ac, gP1LifePoints=0x0201c4e0
- ELIGIB_SPRITE_CTRL_OFF=0x00001d68, ELIGIB_ANIM_STATE_OFF=0x00001d6c
- gDuelCardCtxBase=0x0201e2a0, gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x00000868
- LP_BAR_ANIM_STATE_OFF=0x000004cc, SPRITE_ROW_ENTRY_DATA_OFF=0x000004d4
- CHAIN_NODE_CARD_ARR_OFF=0x000004f4
- BLACK_LUSTER_SOLDIER_ENVOY_CID=0x000016cb

## §5.1 登记 (Rule 3) — 0 引用块

本段无 ROM_INCBIN，无未引用孤儿块。

## 消费者证据 (R6) — 关键槽语义 file:line + 置信度

| 槽/值 | file:line | 语义 | 置信度 |
|-------|-----------|------|--------|
| 0x000016b8=CRIMSON_NINJA_CID | asm/07_equip_effect_chain.s:794 | "CARD_ID_CRIMSON_NINJA=0x16b8 (Crimson Ninja)" | high |
| 0x000016b8 as sprite param | asm/06:12500 | tick_equip_sprite_with_attr11_if_seq_zero plate: "SPRITE_PARAM=0x16b8 // attr11 sprite index" — 实为 card_id 传给 enqueue_sprite_attr_type11 | high |
| 0x00001d70=LP_BANISHER_CTX_OFF | asm/06:12605 | "LP_BANISHER_OFF=0x1d70"; State 2 reads gP1LP+0x1d70 for banisher player/card dispatch | high |
| 0x00000484=EQUIP_ACTIVE_CTX_OFF | asm/06:12843-12851 | "Reads activation slot ptr from [gDuelPhaseFlags+0x484]" | high |
| 0x08058639=check_equip_slot_has_active_effect_value+1 | asm/06:12345-12346 | passed to set_equip_activation_state_by_mode_alt as mode fn ptr | high |
| 0x08058a41=check_zone_entity_field6_in_equip_range+1 | asm/06:13047-13064 | passed to select_equip_target_slot_by_card_id & init_zone_activation_display_fields as pred ptr | high |
| 0x08065991=check_equip_activation_at_slot11+1 | asm/08_equip_oam_neodaed.s:3289 + asm/06:13217,13230 | passed as fn_ptr to select_equip_target_slot_by_card_id and init_zone_activation_display_fields | high |

## C8 验收 (stale FUN_ + CJK)

- stale FUN_ 扫描: 段内发现 1 处 `FUN_0805a1dc` (line 12568, plate of `tick_equip_activation_with_sprite_mode2`); 现名为 `tick_equip_activation_sprite_mode2_by_type` (asm/06:15868 confirmed); 已纳入 P3 plate 重写计划。
- CJK mojibake: 4 处 (lines 12097, 12167, 12568, 12821); 均已纳入 P1-P4 整段 ASCII 重写计划。
- 落地后验收: grep `FUN_[0-9a-f]{8}` 段行范围 == 0; grep `[^\x00-\x7F]` 段行范围 == 0。

## 求助

无 (所有槽语义均有 high-conf 证据)。

---

## Executor Report: F06-Seg-7

- 槽: EQ=53 REF=5 RENAME=0 FUNC_RENAME=0 PLATE=4
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局: card_info.inc +1 (CRIMSON_NINJA_CID=0x16b8); ewram.inc +1 (LP_BANISHER_CTX_OFF=0x1d70); duel_field.inc +1 (EQUIP_ACTIVE_CTX_OFF=0x484)
- 求助: none
- proposal: doc/dev/refine/F06-Seg-7.proposal.md
