# Refine Review: F11-Seg-3a

**Segment**: `[0x08086cdc, 0x080872e4)` — 4 functions, 0 ROM_INCBIN, 46 slots (EQ=36, REF=4, RENAME=6)
**Proposal**: `doc/dev/refine/F11-Seg-3a.proposal.md`

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | OK | Seg-2 结束于 0x8086cdc，Seg-3a 从此开始；路线图允许拆 3a/3b；上界 0x080872e4 为 write_equip_zone_entries_by_lv_card_id push-prologue (ROM byte: 0xb5f0 at offset -0x08000000) |
| C2 Rule2 | ROM_INCBIN/.byte 块全有归宿 | OK | 独立 python scan 确认段内 0 处 ROM_INCBIN；无遗留 |
| C3 Rule3 | §5.1 块 0 引用 | N/A | 段内无 §5.1 登记；Rule3 不适用 |
| C4 R1 值 | EQ/REF value 与 ROM 4 字节吻合 | OK | 独立重跑：全 35 个 EQ slot + 4 个 REF slot ROM 读值 100% 吻合；6 个 PTR_gP1LifePoints_ 均 = 0x0201c4e0 |
| C5 R1 复用 | 0 新 equ，全部 REUSE | OK | 按值 grep 确认：gDuelPhaseFlags/EQUIP_PHASE_FRAME_OFF/EARTH_CHANT_CID/END_OF_WORLD_CID/gDuelCardCtxBase/PLAYER_BLOCK_STRIDE/gP1FieldArrayCBase/gEquipEffectZoneTable/LP_BANISHER_CTX_OFF/ELIGIB_ANIM_STATE_OFF/ELIGIB_SPRITE_CTRL_OFF/SAMSARA_CID/gP1SlotSetCodeArray/CARD_FIELD3_THRESHOLD_1500/zone_query_hand_tag_12a1 全部在各自 .inc 中找到匹配值 |
| C6 R2 名 | 46 个 slot 标签符合 `^[a-z][a-z0-9_]+$` | OK | 全部通过正则验证；无碰撞（grep 存在检查通过） |
| C7 R3 接通 | 无全局 carve 槽 | N/A | 无 carve 计划 |
| C8 R5 现名 | plate 无残留 stale FUN_ | FAIL | 见 #1 |
| C9 ASCII | 所有 proposed plate/EOL 文本纯 ASCII | FAIL | 见 #2 和 #3 |
| C10 carve | fn-ptr THUMB+1 值正确 | OK | 0x080869a9 = scan_equip_zones_for_eligible_type11_target (push @0x080869a8=0xb570) \|1；0x08086a39 = eval_equip_zone_score_with_field_card (push @0x08086a38=0xb530) \|1；switchdata 条目为直接代码指针（MOV PC 调度），无需 +1 |
| C11 误名 | 4 函数名与函数体一致 | OK | dispatch_equip_zone_activation_state: jump table 调度; populate_equip_zone_entries_substate_d: bl write_equip_zone_entry_by_substate r1=0xd; populate_equip_zone_entries_substate_e: bl write_equip_zone_entry_by_substate r1=0xe; write_equip_zone_entries_substate_d_range: 循环 r1=0xd。均一致。 |
| C12 R6 | 关键槽有 file:line + 置信度 | FAIL | 见 #4 (Plate 4 R6 证据 line 号错误) |
| C13 残留 | 段内 46 个 DAT_/DWORD_/PTR_ 全覆盖 | OK | 独立 python scan：46 个 slot def；proposal EQ(36)+REF(4)+RENAME(6)=46 精确匹配，无遗漏无重复 |

---

## 状态: NEEDS_FIX (4 items)

---

## 修改清单

### #1 — C8 — Plate 1 (dispatch_equip_zone_activation_state) 中 stale FUN_ 和事实性错误

**位置**: proposal §PLATE plan 第 1 项，拟替换 asm/11 L3829 的主 plate。

**错误 A — 长度超限**: 提案声称 "491 chars"，实测 563 chars（超 500 限 63 字符）。Ghidra 有时截断过长 plate，也与项目 R2 规范冲突。

**错误 B — 5 个 case 索引全部偏移 4**:

提案文本：`0x16=case_0x7c, 0x17=case_0x7d, 0x18=case_0x7e, 0x19=case_0x7f, 0x1a=case_0x80`

jump table 实测（base=0x08086d1c，subs 0x62 后索引）：

| 索引（subs 0x62 result） | 正确 state code | 提案中写的索引 |
|---|---|---|
| 0x1a (26) | 0x7c | 0x16 (WRONG) |
| 0x1b (27) | 0x7d | 0x17 (WRONG) |
| 0x1c (28) | 0x7e | 0x18 (WRONG) |
| 0x1d (29) | 0x7f | 0x19 (WRONG) |
| 0x1e (30) | 0x80 | 0x1a (WRONG) |

正确计算：case_0x7c 对应 index = 0x7c - 0x62 = 0x1a；依此类推到 0x1e。

**错误 C — case_0x7e 描述内容错误**:

提案描述 `0x18=case_0x7e (find_zone_slot_idx_allowed+invoke_setup_equip_oam)` 但实测 case_0x7e (target=0x8086f34, L4117) 调用的是 `invoke_card_display_op_0x31_sub13`，并不调用 `find_zone_slot_idx_allowed`。`find_zone_slot_idx_allowed_for_card + invoke_setup_equip_oam_with_attr2` 实际上在 case_0x64 (index 2，L4356) 中。

**错误 D — case_0x64 遗漏**:

jump table [2]（state_code=0x64）→ 0x808710c，在 asm 中为 `switchD_08086d10__caseD_64`，调用 `find_zone_slot_idx_allowed_for_card` 和 `invoke_setup_equip_oam_with_attr2`，此 case 在 plate 描述中完全缺失。

**修正要求**: fixer 需重写 Plate 1 的提案文本，使其：
- 控制在 500 chars 以内
- 将 5 个 case 索引改为 0x1a..0x1e
- 修正 case_0x7e 描述（invoke_card_display_op_0x31_sub13 路径）
- 补充 case_0x64（index=0x2）的存在（find_zone_slot_idx_allowed+invoke_setup_equip_oam）
- 保持纯 ASCII

示例正确结构（供参考，fixer 可适当裁剪以控制长度）：
```
Equip zone activation state machine frame dispatcher. Fast gate: reads [r7+0x4] bit2; if set returns 0 via caseD_63. Else reads [gDuelPhaseFlags+0x4a0] state, subs 0x62 -> index [0..0x1e], dispatches via table at 0x08086d1c. Key cases: 0x0=caseD_62(count_field_copies_of_card+enqueue_lp_counter_sprite), 0x2=caseD_64(find_zone_slot_idx_allowed+invoke_setup_equip_oam), 0x1a=caseD_7c(check_activation_confirmed+select_equip_target_slot_by_card_id), 0x1b=caseD_7d(init_zone_activation), 0x1c=caseD_7e(invoke_card_display_op_0x31_sub13), 0x1d=caseD_7f(check_confirmed+scan_zones), 0x1e=caseD_80(check_neo_daedalus+eval_equip_bonus), default=caseD_63(return 0).
```

---

### #2 — C9 — Plate 1 现有 L3829 含 CJK mojibake（已知）→ 需确保替换文本可实际落地

这条不是 proposal 新引入的问题——现有 asm/11 L3829 已经是 CJK mojibake 字节。但由于 #1 中的文本错误，提案的替换文本不能直接落地。**本条依附于 #1**：#1 修正后此条自动解决。

---

### #3 — C9 — Plate 1 提案长度 563 > 500（单独列出以免被合并忽视）

即使其他错误修正，长度本身必须压到 ≤500 chars。当前 563 chars 的文本若直接设入 Ghidra，将超出 R2 plate 字数上限。修正方法：缩减 case 描述的文字量（例如去掉括号内的子函数名称列表，保留 case 编号和核心动词）。

---

### #4 — C12 — Plate 4 R6 证据 line 引用错误

**位置**: proposal §消费者证据 (R6) 表，Plate 4 条目。

提案写：`asm/11 L2493 bl write_equip_zone_entry_by_substate @ 0808721a, inside populate_equip_zone_entries_substate_d body`

实测：asm/11 L2493 对应地址 0x0808635e（与 populate 函数毫无关联）。`bl write_equip_zone_entry_by_substate @ 0808721a` 的正确行号是 **L4493**。

地址 0x0808721a 本身是正确的（在 populate_equip_zone_entries_substate_d 体内），但 line number 引用错误 2000 行。fixer 需将证据引用从 `L2493` 改为 `L4493`。

---

## 附：通过检查项确认

- **C4/C5 全量核对**: 36 EQ + 4 REF + 6 RENAME = 46 slots，ROM 字节全部独立重跑，100% 吻合。
- **C13**: 独立 python scan 得到 46 个 slot def，与 proposal 三表并集精确匹配。无 DWORD_ 槽（asm 段内不存在）。
- **gP1SlotSetCodeArray 误名订正**: ewram.inc line 332 确认 `gP1SlotSetCodeArray = 0x0201c740`，asm/11 DAT_08087240 ROM 读值 = 0x0201c740，原 plate 写 "gDuelCardPool" 是错误名（无此常量）。订正有效。
- **gP1HandSlotArray 误名订正**: ewram.inc line 334 确认 `gP1HandSlotArray = 0x0201c8f8 = gP1LifePoints+0x418`；代码 `0x83<<3 = 0x418`，`gP1LifePoints + 0x418 = 0x0201c8f8`。订正有效。
- **zone_query_hand_tag_12a1 语义**: duel_field.inc line 423 确认此值用于 `find_effect_node_in_zone` 的 node-type tag（r2 参数），与 asm/11 L4485-4487 调用形式（r1=0xb zone, r2=DAT_08087248）完全吻合；不是 PARASITE_PARACIDE_CID（不同语义域）。
- **fn-ptr THUMB+1**: scan_equip_zones_for_eligible_type11_target @0x080869a8 push=0xb570 OK；eval_equip_zone_score_with_field_card @0x08086a38 push=0xb530 OK；switchdata 条目为 MOV-PC 调度目标，无需 +1。
- **cross-file plates**: asm/11 L6286 `FUN_080871a8` 确认需替换为 `populate_equip_zone_entries_substate_d`（bl 在 L4493 @0x0808721a）。asm/12 L5378 `FUN_08086e90/FUN_08086fa6` 均为 BL 指令地址（L4028 @0x08086e90, L4176 @0x08086fa6）而非函数入口，替换为 `dispatch_equip_zone_activation_state (caseD_80/caseD_7d)` 正确。
- **disasm=0 验证**: 段内 dispatch_equip_zone_activation_state 的跳转表已在 Ghidra 中完整反汇编（switchD_08086d10__switchdataD_08086d1c 全 0x1f 条目可见于 asm）；无遗留 switchD 未分派代码块。

---

## Reviewer Verdict: F11-Seg-3a = NEEDS_FIX(4 items)
