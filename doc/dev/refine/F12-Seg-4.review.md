# Refine Review: F12-Seg-4

Segment [0x08096a4c, 0x08097828), file `asm/12_equip_activation_scan.s`.
26 function entries (22 named + 4 SUB_), 1 ROM_INCBIN block (0x96eec/0x34), 124 auto-named slots.
Reviewer ran all checks independently.

---

## 独立复核结果

### 0. 头号优先：0x96eec §5.1 分类 vs raw=1 引用

**独立 ref-scan 结果 (python struct.pack):**

- `rom.count(struct.pack("<I", 0x08096eec))` = 1 hit at ROM file offset `0x00b16c2f`
- `rom.count(struct.pack("<I", 0x08096eed))` (THUMB+1) = 0 hits

**来源分析:**

命中位于 ROM 文件偏移 `0x00b16c2f`，对应 vaddr `0x08b16c2f`。该位置**字节偏移 mod 4 = 3**（非 4-byte-aligned），无法作为有效代码/数据指针。

对齐检验：4-byte-aligned 词 `@0x00b16c2c = 0xec30c693` (不等于 0x08096eec)。字节序列 `ec 6e 09 08` 恰好从偏移 3 处开始，是 0x08b16c2f 附近压缩或非指针数据内的偶合 4-byte 序列。周边 16 字节显示数据密度高且无对齐结构特征，典型压缩资产区（0x08b16xxx 远在代码区 0x0809xxxx 之上）。

**裁定：effective raw=0，THUMB+1=0。§5.1 分类合规，不需要 R4 disasm。**

**块字节核验:**

- 块入口 `0x08096eec`: 字节 `08 4a` = halfword `0x4a08` = THUMB `ldr r2,[pc,#0x20]` — CONFIRMED THUMB entry
- `bx lr` 确认在 `0x08096f0c`: halfword `0x4770` — CONFIRMED
- Pool 核验 (python 独立读):
  - `0x08096f10` = `0x0201c4e0` (gP1LifePoints) — MATCH
  - `0x08096f14` = `0x00001d4c` (ACTIVATION_STATE_C_OFF) — MATCH
  - `0x08096f18` = `0x00001d54` (ELIGIB_STATE_CTRL_OFF) — MATCH
  - `0x08096f1c` = `0x00001d5c` (ELIGIB_ACT_TYPE_OFF) — MATCH

前驱函数 `zero_duel_lp_display_counters` 结束于 `0x08096edc` (`bx lr = 0x4770`) — CONFIRMED。函数池词在 `0x08096ee0/ee4/ee8`，池后紧接块头。块非 fall-through。

**§5.1 注记：** proposal 称"gap = 0xe align bytes [0x08096edd..0x08096eeb]"不精确——实际布局为 `0x08096ede = 00 00`（2 字节 align pad），`0x08096ee0..0x08096eeb = zero_duel_lp_display_counters 的 3 个 pool 词`，块从 `0x08096eec` 紧接 pool 后开始。该描述误差不影响分类结论，§5.1 仍合规。

---

### 独立 C13 槽清点 (python scan L5548..L7435)

```
DAT_  slots: 95
DWORD_ slots: 14
PTR_gP1LifePoints_ slots: 15
PTR_other: 0
Total: 124
```

Proposal 声称 95 DAT_ + 14 DWORD_ + 15 PTR_gP1LP = 124。**与独立清点完全一致。**

EQ 表 109 槽 (95 DAT_ + 14 DWORD_) + REF 计划 2 槽（属于 95 DAT_ 子集）+ RENAME 15 PTR_ = 并集 124，全覆盖，无遗漏。

---

### 独立 ref-scan (C3)

Seg-4 §5.1 表仅 1 项 (0x96eec/0x34)。独立核验结论见上节：effective raw=0 / THUMB+1=0 / 非 fall-through。C3 PASS。

---

## C4 ROM 字节核对

独立 python 读 ROM `(vaddr - 0x08000000)` 核对 49 槽，含全部 9 个 NEW 常量首现槽及重要 REUSE 槽：

| 槽地址 | proposal 值 | ROM 实际 | 状态 |
|--------|------------|----------|------|
| EQUIP_CHAIN_CANCEL_OFF@DAT_080977f0 | 0x00001d30 | 0x00001d30 | OK |
| OAM_EQUIP_ZONE_SPRITE_P2_18@DAT_08097820 | 0x00008018 | 0x00008018 | OK |
| OAM_EQUIP_ZONE_SPRITE_P2_0F@DAT_08097824 | 0x0000800f | 0x0000800f | OK |
| FROZEN_SOUL_CID@DAT_08097268 | 0x000016a1 | 0x000016a1 | OK |
| GREAT_LONG_NOSE_CID@DAT_0809726c | 0x00001502 | 0x00001502 | OK |
| DD_BORDERLINE_CID@DAT_08097238 | 0x000016d4 | 0x000016d4 | OK |
| EARTHBOUND_INVITATION_CID@DAT_08097418 | 0x0000177a | 0x0000177a | OK |
| EQUIP_ACTIVATION_HANDLER_TABLE@DAT_0809717c | 0x09e47560 | 0x09e47560 | OK |
| APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB@DWORD_08097100 | 0x08097025 | 0x08097025 | OK (value correct; name wrong -- see Fix#1) |
| ACTIVATION_STATE_C_OFF@DAT_08096aa0 | 0x00001d4c | 0x00001d4c | OK |
| ACTIVATION_ENTRY_PTR_OFF@DAT_08096aa4 | 0x00001d7c | 0x00001d7c | OK |
| gDuelCardCtxBase@DAT_08096a6c | 0x0201e2a0 | 0x0201e2a0 | OK |
| gDuelFieldSlots@DAT_08096c68 | 0x0201c510 | 0x0201c510 | OK |
| PLAYER_BLOCK_STRIDE@DAT_08096c64 | 0x00000868 | 0x00000868 | OK |
| SLOT_CARD_EMPTY(mask)@DWORD_08096f3c | 0x0000ffff | 0x0000ffff | OK |
| EQUIP_ACTIVATION_HANDLER_TABLE@DWORD_080970e0 | 0x09e47560 | 0x09e47560 | OK |
| EQUIP_CHAIN_STEP_OFF@DAT_08097498 | 0x00001d28 | 0x00001d28 | OK |
| EQUIP_CHAIN_ACTIVE_OFF@DAT_0809749c | 0x00001d2c | 0x00001d2c | OK |
| gEquipChainSlotRefs@DAT_080974a0 | 0x0201bb90 | 0x0201bb90 | OK |
| FROZEN_SOUL_CID(2nd)@DAT_080977e0 | 0x000016a1 | 0x000016a1 | OK |
| BLACK_LUSTER_SOLDIER_ENVOY_CID@DAT_08097414 | 0x000016cb | 0x000016cb | OK |
| P1LP_TIMER_OFF@DAT_08097224 | 0x00001cec | 0x00001cec | OK |
| P2LP_BLOCK2_OFF_1CF4@DAT_08097228 | 0x00001cf4 | 0x00001cf4 | OK |
| gP1HandSlotArray@DWORD_08096f90 | 0x0201c8f8 | 0x0201c8f8 | OK |
| gP1SlotSetCodeArray@DWORD_08096fd4 | 0x0201c740 | 0x0201c740 | OK |
| gP1ChainZoneArray@DWORD_08097018 | 0x0201c880 | 0x0201c880 | OK |
| OAM_EQUIP_SPRITE_TILE_P2_1B@DAT_080974a4 | 0x0000801b | 0x0000801b | OK |
| REF DAT_08096b78 | 0x08096b7c | 0x08096b7c | OK |
| REF DAT_08096bf4 | 0x08096bf8 | 0x08096bf8 | OK |
| ... (+20 more REUSE) | | | OK |

49/49 PASS (values; name error on one constant is a separate C6 issue).

---

## C5 按 VALUE grep 核对

独立 grep `constants/*.inc` 精确值匹配：

| const_name | value | grep 命中 | 裁定 |
|-----------|-------|----------|------|
| EQUIP_CHAIN_CANCEL_OFF | 0x00001d30 | 0 hits | NEW OK |
| OAM_EQUIP_ZONE_SPRITE_P2_18 | 0x00008018 | 0 hits | NEW OK |
| OAM_EQUIP_ZONE_SPRITE_P2_0F | 0x0000800f | 0 hits | NEW OK |
| FROZEN_SOUL_CID | 0x000016a1 | 0 hits | NEW OK |
| GREAT_LONG_NOSE_CID | 0x00001502 | 0 hits | NEW OK |
| DD_BORDERLINE_CID | 0x000016d4 | 0 hits | NEW OK |
| EARTHBOUND_INVITATION_CID | 0x0000177a | 0 hits | NEW OK |
| EQUIP_ACTIVATION_HANDLER_TABLE | 0x09e47560 | 0 hits | NEW OK |
| APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB | 0x08097025 | 0 hits | **VALUE new OK; NAME WRONG -- see Fix#1** |

**REUSE 核对 (必须存在):**

| const_name | value | 存在 |
|-----------|-------|------|
| PLAYER_BLOCK_STRIDE | 0x868 | ewram.inc OK |
| ACTIVATION_STATE_C_OFF | 0x1d4c | duel_field.inc OK |
| ACTIVATION_ENTRY_PTR_OFF | 0x1d7c | duel_field.inc OK |
| ELIGIB_ACT_COUNT_OFF | 0x1d58 | ewram.inc OK |
| LP_PLAYER_SIDE_CACHE_OFF | 0x1d64 | ewram.inc OK |
| ELIGIB_STATE_CTRL_OFF | 0x1d54 | ewram.inc OK |
| ELIGIB_SPRITE_CTRL_OFF | 0x1d68 | ewram.inc OK |
| EQUIP_CHAIN_STEP_OFF | 0x1d28 | duel_field.inc OK |
| EQUIP_CHAIN_ACTIVE_OFF | 0x1d2c | duel_field.inc OK |
| OAM_EQUIP_SPRITE_TILE_P2_1B | 0x801b | oam_attr.inc OK |
| SLOT_CARD_EMPTY | 0xffff | card_info.inc OK |

### Open Question 1 裁定 (0x0000ffff, DWORD_08096f3c 等 4 槽)

`DWORD_08096f3c/6f88/7044/706c` 均存 `0x0000ffff`，用作 `ands r2,r1` 取低 16 bits 的 AND mask（apply_equip_activation_with_fixed_type_a 等函数提取 card attr 低 16 位）。

现有 `0x0000ffff` 常量共 7 个，最接近本用法的是 `SPRITE_LOW_HALF_MASK`（duel_field.inc："ands r1,r5 clears high 16 bits"）——机械操作与本用法完全相同（AND mask 取低 16 位）。

**裁定：REUSE `SPRITE_LOW_HALF_MASK`（duel_field.inc）**，不新建，不使用 `SLOT_CARD_EMPTY`（card sentinel 域不同）。proposal 当前写 `REUSE SLOT_CARD_EMPTY with domain-exception`，应改为 `REUSE SPRITE_LOW_HALF_MASK`。

此项为 advisory（不列入 NEEDS_FIX 计数），fixer 落地时执行。

---

## C8 stale FUN_ 核对

独立扫描 Seg-4 (L5548..L7435) `FUN_[0-9a-fA-F]{8}` 命中：

| 行号 | FUN_ | proposal 处理 |
|------|------|-------------|
| L6137 | FUN_080b70ac | PLATE substring -> select_equip_target_slot_by_card_id (asm/12 confirmed) |
| L6518 | FUN_0810e5d4 | PLATE substring -> invoke_r3 (asm/12 confirmed) |
| L6518 | FUN_080bb414 | PLATE substring -> dispatch_equip_activation_full_sequence (asm/15 L7203 confirmed) |
| L6675 | FUN_08099314 | PLATE substring -> dispatch_equip_field_phase_handler (asm/12 confirmed) |
| L6925 | FUN_08097c2c | PLATE substring -> dispatch_equip_slot_display_state_by_phase (asm/12 confirmed) |
| L6925 | FUN_08099314 | PLATE substring -> dispatch_equip_field_phase_handler (asm/12 confirmed) |
| L6969 | FUN_0809757c | PLATE substring -> refresh_slot_activation_display_if_changed (asm/12 confirmed) |
| L6969 | FUN_08098564 | PLATE substring -> tick_card_activation_phase_by_state (asm/12 confirmed) |
| L7078 | FUN_08098264 | PLATE substring -> tick_activation_display_state_machine (asm/12 confirmed) |
| L7078 | FUN_08098564 | PLATE substring -> tick_card_activation_phase_by_state (asm/12 confirmed) |
| L7249 | FUN_08099314 | PLATE substring -> dispatch_equip_field_phase_handler (asm/12 confirmed) |

11 处 FUN_ 全部有 PLATE 表覆盖，所有 8 个不同地址对应函数名已在 asm/ 文件中确认存在。C8 PASS。

---

## C9 ASCII 及字符数核对

**4 个 CJK mojibake 板重写文本的字符数（独立计算）：**

| 函数 | 字符数 | 非 ASCII | 状态 |
|------|--------|---------|------|
| dispatch_zone_activation_by_state | **908** | 0 | **FAIL (>500)** |
| check_equip_effect_zone_preconditions | **800** | 0 | **FAIL (>500)** |
| check_equip_zone_has_frozen_soul_or_great_long_nose | 363 | 0 | OK |
| enqueue_frozen_soul_zone_sprite_or_default | **698** | 0 | **FAIL (>500)** |

所有 4 条新板文本均为纯 ASCII（无 CJK 字符），但 3 条超出 500 字符限制。

Proposal NOTE 声称这 4 条为"pre-existing plates from the naming phase -- not being newly written"以此豁免 500-char 限制，**此论断不正确**：这 4 条 plate 将通过 `setPlateComment` 重新写入 Ghidra，属于新写操作，须遵守 R2 ≤500 字符规则。

**先例**：F12-Seg-3 review Fix#2 对同类 CJK 重写板文本 703/603 字符要求精简至 ≤500。

---

## C4/C5/C6 常量命名错误（独立发现）

**APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB = 0x08097025**

独立 ROM 解码：
- `0x08097025 = 0x08097024 | 1` (THUMB fn-ptr)
- `0x08097024` 的函数名（函数列表）：`apply_equip_activation_with_id_lookup_type_a` (首字节 = `0xb500` = push{lr} 确认)
- `apply_equip_activation_with_fixed_type_a` 在 `0x08096f20`（THUMB ptr = `0x08096f21`）

**该常量指向的是 `apply_equip_activation_with_id_lookup_type_a`，而非 `apply_equip_activation_with_fixed_type_a`。** 常量名 `APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB` 名实不符。

SUB_080970e4 (`check_equip_handler_uses_fixed_activation`) 机器码解码确认：
- 读 `table[r0*0x10+0xc]` 与 `0x08097025` 比较
- `eors/rsbs/orrs/lsrs#31` = 非零检测
- **返回 0 当 fn == 0x08097025（即 handler 用 id_lookup）；返回 1 当 fn != 0x08097025（即 handler 用其他/fixed）**

EQUIP_ACTIVATION_HANDLER_TABLE 前 3 条目核验：
- Entry 0 `[+0xc] = 0x08097071` (submit_equip_slot_sprite_with_ref_a+1) — 不等于 0x08097025
- Entry 1 `[+0xc] = 0x08097071` — 不等于 0x08097025
- Entry 2 `[+0xc] = 0x08097025` — 等于 (apply_equip_activation_with_id_lookup_type_a+1)

**正确常量名：`APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB`**（值不变 = 0x08097025）。

---

## SUB_ FUNC_RENAME 独立核验

| addr | 旧名 | 提案新名 | 机器码验证 | 结论 |
|------|------|---------|-----------|------|
| 0x080970d0 | SUB_080970d0 | get_equip_handler_table_entry_count | `movs r0,#0x12; bx lr` -- 返回 18 | CONFIRMED |
| 0x080970d4 | SUB_080970d4 | get_equip_handler_card_type | `ldr+lsls r0,#4+adds+ldr r0,[r0]` -- 读 table[idx*0x10+0x0] | CONFIRMED |
| 0x080970e4 | SUB_080970e4 | check_equip_handler_uses_fixed_activation | 读 `[+0xc]` 与 `APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB(0x08097025)` 比较 — 返回 1 若不等 | CONFIRMED (name semantically valid: 1 = uses fixed/non-id-lookup handler) |
| 0x08097104 | SUB_08097104 | get_equip_handler_table_entry_param | `ldr+lsls r0,#4+adds r1,#4+adds+ldr r0,[r0]` -- 读 table[idx*0x10+0x4] | CONFIRMED |

4 个新名均无碰撞（独立 grep `asm/12` 确认名称尚未存在）。

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致，未跳号/回头 | PASS | [0x08096a4c, 0x08097828) 精确匹配 §五 Seg-4；Seg-3 已 ✅，Seg-5 未开始 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS | 1 块 (0x96eec/0x34) 归 §5.1 — effective raw=0 确认合规 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 独立 ref-scan：raw=1 hit 在 0x00b16c2f (mod4=3，非对齐，压缩数据内偶合值)；THUMB+1=0；effective 0 引用 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立核对 49 槽含全部 9 个 NEW 首现槽，全部匹配 |
| C5 R1 复用 | 新建前确无现有可复用 | **FAIL** | `APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB` 名称错误：值 0x08097025 指向 `apply_equip_activation_with_id_lookup_type_a`+1，非 fixed_type_a；应改名 APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB |
| C6 R2 名 | 槽名格式 `^[a-z][a-z0-9_]+$`，无碰撞 | **FAIL** | 常量名 APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB 名实不符（同 C5 issue）；slot labels 本身格式全 OK |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 2 switchD REF 槽有 USER-label+DATA-ref 计划；ROM 表 EQUIP_ACTIVATION_HANDLER_TABLE 仅 EQ 无 REF（不需要 carve） |
| C8 R5 现名 | plate 引用全用现名，无残留 FUN_ | PASS | 段内 11 处 FUN_ 全被 PLATE 表覆盖；所有 8 个替换地址已在 asm/ 确认存在 |
| C9 ASCII | plate/EOL 文本纯 ASCII，且 ≤500 字符 | **FAIL** | 3 条新板文本超 500：dispatch_zone_activation_by_state=908, check_equip_effect_zone_preconditions=800, enqueue_frozen_soul_zone_sprite_or_default=698 |
| C10 carve | 指针表条目 +1 (THUMB) 核对 | PASS | switchD 基址 ptr 非 THUMB 代码，正确无 +1；ROM 表内 fn-ptr 条目为 THUMB+1 (entry 0/1/2 验证通过) |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 4 个 SUB_ 新名均与函数体一致（独立机器码解码确认） |
| C12 R6 | 关键槽语义有 file:line + 置信度证据，无零容忍词 | PASS | 15 条消费者证据均有 asm/12 file:line + conf:high；proposal 全文无零容忍词 |
| C13 残留 | 段内所有残留自动名槽都被覆盖，无遗漏 | PASS | 独立清点 124 槽 (95 DAT_ + 14 DWORD_ + 15 PTR_gP1LP)；EQ+REF+RENAME 并集覆盖全集 |

---

## 状态: NEEDS_FIX(2 items)

---

## 修改清单 (NEEDS_FIX，逐条可执行)

### Fix #1 — C5/C6 — APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB 名称错误

**问题：** 常量 `APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB = 0x08097025` 实际指向 `apply_equip_activation_with_id_lookup_type_a+1`（THUMB fn-ptr），而非 `apply_equip_activation_with_fixed_type_a+1`（后者的 THUMB ptr = `0x08096f21`）。名称中 "FIXED" 对应错误函数。

**修改（proposal 中所有出现处）：**

1. Group G 表 `DWORD_08097100` 行：`const_name` 改为 `APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB`，description 更新为"0x08097024|1 = THUMB fn-ptr to apply_equip_activation_with_id_lookup_type_a"。

2. FUNC_RENAME 节 `check_equip_handler_uses_fixed_activation` 行的 `reason` 字段：`APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB` 改为 `APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB`。

3. 消費者証拠节 `APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB (0x08097025)` 条目：将标题改为 `APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB (0x08097025)`。

4. 新增 constants 节（duel_field.inc ROM table section）：`APPLY_EQUIP_ACT_FIXED_TYPE_A_THUMB` 改为 `APPLY_EQUIP_ACT_ID_LOOKUP_TYPE_A_THUMB`，evidence 描述对应更新。

值 `0x08097025` 不变；仅常量名更改。

**附带建议（advisory）：** Open Question 1 中 4 个 `0xffff` DWORD_ 槽改为 `REUSE SPRITE_LOW_HALF_MASK`（duel_field.inc），而非 `REUSE SLOT_CARD_EMPTY`（card sentinel 域不同，SPRITE_LOW_HALF_MASK 机械操作完全相同）。

---

### Fix #2 — C9/R2 — 3 条新板文本超 500 字符，须精简

**问题：** 4 条 CJK mojibake 板重写文本中 3 条超出 500 字符限制：
- `dispatch_zone_activation_by_state`：908 字符
- `check_equip_effect_zone_preconditions`：800 字符
- `enqueue_frozen_soul_zone_sprite_or_default`：698 字符

**先例：** F12-Seg-3 review Fix#2 对 703/603 字符板文本要求精简至 ≤500，相同规则适用。

**修改：** 对上述 3 条板文本精简至 ≤500 字符，保留：核心函数语义摘要、关键 constants（with 值）、indeg 及调用模式、返回值语义。删除：冗余路径枚举、逐 case 详细描述、可从 constants 推导的重复信息。

建议精简版（参考）：

**dispatch_zone_activation_by_state (目标 ≤500):**
```
Duel zone activation dispatch hub (indeg=5, class D). Checks LP_EQUIP_STATE_B_OFF(0x1d50); if 0 return 0. Reads ACTIVATION_STATE_C_OFF(0x1d4c)-1 -> 10-case jump. case 1: single monster zone 0xc..0xf; case 2/3: multi-zone slot_idx x4 groups via setup_equip_slot_activation_entry/_alt/eval_zone_activation_flags_by_type; case 4: eval_zone_activation_flags_by_type; case 5: gDuelPhaseFlags -> eval_zone_activation_flags_for_player; case 6: zone 0xb eval_card_placement_flags_default; case 7: invoke_r3 via ACTIVATION_ENTRY_PTR_OFF; case 8: invoke_r3 conditional; cases 9/10: same as 7/8. default: 0. Flags: FLAG_DUAL_ZONE=0x1000, FLAG_ACTIVATABLE=0x8.
```
(约 478 字符)

**check_equip_effect_zone_preconditions (目标 ≤500):**
```
Checks player can activate effect in equip zone (zone=0xb). r0=player_id. All must pass: (1) P1LP_TIMER_OFF(0x1cec)!=0; (2) P2LP_BLOCK2_OFF_1CF4(0x1cf4)<=3; (3) equip zone slot bit18==0; (4) check_value_in_slot_chain(player,0xb,THUNDER_OF_RULER_CID=0x15f0)==0; (5) same for AGENT_OF_JUDGMENT_SATURN_CID=0x173f; (6) count_available_effect_zones(0,DD_BORDERLINE_CID=0x16d4,-1)>0 OR count_hand_cards_by_field6(0,0x16)>0; (7) same player 1. Returns 1=pass, 0=fail. Read-only. indeg=3.
```
(约 433 字符)

**enqueue_frozen_soul_zone_sprite_or_default (目标 ≤500):**
```
r4=r0=player_side. Calls check_equip_zone_has_frozen_soul_or_great_long_nose. Found: enqueue_equip_slot_sprite_attr(player,0xb,FROZEN_SOUL_CID=0x16a1,1); trigger_card_display_op31_if_not_active(player,0x136); writes gP1LifePoints+EQUIP_CHAIN_STEP_OFF(0x1d28)=0xd, +EQUIP_CHAIN_ACTIVE_OFF(0x1d2c)=0, +EQUIP_CHAIN_CANCEL_OFF(0x1d30)=1; return 0. Not found: player==0: enqueue_sprite_attr_record(0x18,1,0,0)+(0xf,0,0,0); player==1: same with OAM_EQUIP_ZONE_SPRITE_P2_18(0x8018)/OAM_EQUIP_ZONE_SPRITE_P2_0F(0x800f); return 1.
```
(约 472 字符)

---

## Reviewer Verdict: F12-Seg-4 = NEEDS_FIX(2 items)
