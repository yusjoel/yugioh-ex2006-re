# Refine Review: F12-Seg-3

Segment [0x08095ba8, 0x08096a4c), file `asm/12_equip_activation_scan.s`.
18 named functions (14 push-prologue + 4 bx-lr leaf), 0 ROM_INCBIN blocks.
Reviewer ran all checks independently.

---

## 独立复核结果

### 独立 ROM_INCBIN / .byte 扫描

Python scan of ASM lines 3563..5547 (Seg-3 range):
- ROM_INCBIN count: 0
- `.byte` code blocks: 0
- `.zero` alignment pads: present (legitimate, not data blocks)

**Proposal 声明 "0 ROM_INCBIN / 0 .byte": 独立确认正确。**

### 独立 C13 槽清点 (独立 python scan)

```
DAT_  slots: 116
DWORD_ slots: 0
PTR_gP1LifePoints_ slots: 28
PTR_PTR_ slots: 0
PTR_DAT_ slots: 0
Other PTR_ slots: 0
Total: 144
```

Proposal 声称 116 DAT_ + 28 PTR_gP1LifePoints_ = 144。与独立清点完全一致。

**EQ + RENAME 并集 = 116 DAT_ (全覆盖) + 28 PTR_ (全覆盖) = 144 / 144 无遗漏。**

注: proposal Group C 有一行 `DAT_08096363b4 | --` 系注释行 (非独立 slot)，实际 slot 为下一行 `DAT_080963b4`，已正确覆盖。独立计数 116 DAT_ 含 DAT_080963b4，proposal EQ 表也覆盖了该槽。无 C13 缺口。

### 独立 ref-scan (C3)

Seg-3 无 §5.1 登记条目（无 ROM_INCBIN），C3 不适用此段。

---

## C4 ROM 字节核对

独立 python 读 ROM (vaddr - 0x08000000) 核对 41 槽，含全部 8 个 NEW 常量首现槽及重要 REUSE 槽：

| 槽地址 | proposal 值 | ROM 实际 | 状态 |
|--------|------------|----------|------|
| 0x08096364 | 0xfffff03f | 0xfffff03f | OK |
| 0x08096368 | 0xffff803f | 0xffff803f | OK |
| 0x08095dd4 | 0x00001d74 | 0x00001d74 | OK |
| 0x08095e18 | 0x00001d74 | 0x00001d74 | OK |
| 0x08095f08 | 0x0000fffe | 0x0000fffe | OK |
| 0x08096050 | 0x00001c58 | 0x00001c58 | OK |
| 0x0809608c | 0x00001bd4 | 0x00001bd4 | OK |
| 0x08095cc8 | 0x00000fee | 0x00000fee | OK |
| 0x080969b8 | 0x00001d7c | 0x00001d7c | OK |
| 0x08095c1c | 0x00001d68 | 0x00001d68 | OK |
| 0x08095c28 | 0x00000868 | 0x00000868 | OK |
| 0x08096028 | 0x0201c600 | 0x0201c600 | OK |
| 0x0809602c | 0x0201e2a0 | 0x0201e2a0 | OK |
| 0x08096634 | 0xfffff03f | 0xfffff03f | OK |
| 0x08096638 | 0xffff803f | 0xffff803f | OK |
| 0x08096504 | 0xfffff03f | 0xfffff03f | OK |
| 0x08096508 | 0xffff803f | 0xffff803f | OK |
| 0x080966e8 | 0x0000131e | 0x0000131e | OK |
| 0x08096260 | 0x00001407 | 0x00001407 | OK |
| 0x08096788 | 0x00001407 | 0x00001407 | OK |
| 0x08096384 | 0x00001cc4 | 0x00001cc4 | OK |
| 0x08096808 | 0x00001d64 | 0x00001d64 | OK |
| 0x08096968 | 0x0000fffe | 0x0000fffe | OK |
| 0x080969b4 | 0x00001d4c | 0x00001d4c | OK |
| 0x08096a3c | 0x00001d7c | 0x00001d7c | OK |
| 0x08096a40 | 0x00001d58 | 0x00001d58 | OK |
| 0x080969f8 | 0x00001d7c | 0x00001d7c | OK |
| 0x08095c9c | 0x00001d54 | 0x00001d54 | OK |
| 0x08095c64 | 0x00001d64 | 0x00001d64 | OK |
| 0x08096834 | 0x000004cc | 0x000004cc | OK |
| 0x08095f88 | 0x00001cec | 0x00001cec | OK |
| ... (+9 more Group B) | | | OK |

41/41 PASS。

---

## C5 按 VALUE grep 核对

独立 grep `constants/*.inc` 精确值匹配结果:

| const_name | value | grep 精确命中 | 裁定 |
|-----------|-------|-------------|------|
| ZONE_PHASE_STATUS_OFF | 0x00001c58 | 0 hits | NEW OK |
| ZONE_EVAL_PHASE_CODE_OFF | 0x00001bd4 | 0 hits (card_info 有误判子串，精确无命中) | NEW OK |
| ACTIVATION_ENTRY_CLR_BITS_11_6 | 0xfffff03f | 1 hit: `OAM_ATTR2_CLR_BITS_11_6` (oam_attr.inc) | 域区分：OAM 属性 vs 装备发动 entry 结构体半字，域不同，新建合法 |
| ACTIVATION_ENTRY_CLR_BITS_14_6 | 0xffff803f | 2 hits: `slot_field_mask_ffff803f` (card_info.inc) + `SCROLLBAR_CLEAR_BITS_14_6` (gl_scrollbar.inc) | 域区分：slot 字段扫描 / 滚动条 vs 装备发动 entry 结构体，域不同，新建合法 |
| ACTIVATION_ENTRY_PTR_OFF | 0x00001d7c | 0 hits | NEW OK (邻近 0x1d7a=LP_DISPLAY_SEQ_PROGRESS_OFF，值不同) |
| LP_ANIM_RESULT_OFF | 0x00001d74 | 0 hits | NEW OK |
| LP_ANIM_TRIGGER_SENTINEL | 0x00000fee | 1 hit: `COCOON_OF_EVOLUTION_CID` (card_info.inc) | 域区分裁定 (见下) |
| EFFECT_ID_GENERIC_WILDCARD | 0x0000fffe | 0 exact hits (其他命中均为高字节掩码如 0xfffe0000/0xfffe0007，精确值 0x0000fffe 无现有常量) | NEW OK |

### LP_ANIM_TRIGGER_SENTINEL (0x0fee) 域裁定

`card_info.inc` 已有 `COCOON_OF_EVOLUTION_CID = 0x00000fee`。

独立读消费者代码 (ASM L3698-L3699):
```
ldr r0, DAT_08095cc8    @ loads 0x0fee
cmp r1,r0               @ r1 = [gP1LifePoints+ELIGIB_CARD_ID_OFF]
bne LAB_08095ccc        @ if not equal, skip LP anim dispatch
```

字段 `[gP1LifePoints+ELIGIB_CARD_ID_OFF]` 通常存储 card_id，但此处 0x0fee 用作 LP bar 动画触发哨兵值。14 处 ROM 引用均在 LP 动画或相关装备发动路径，无 Cocoon of Evolution 卡牌逻辑语境。

裁定：按 `feedback_c5_offset_value_collision_scope`，两者子系统 (card_id 数据层 vs LP 动画触发门控) 不同，新建独立常量合法。Proposal 处置正确。

### ACTIVATION_ENTRY_CLR_BITS_14_6 (0xffff803f) 域裁定

独立验证消费者代码 (ASM L4581-4585, setup_equip_slot_activation_entry):
```
ldr r0, DAT_08096368    @ 0xffff803f
ldrh r3,[r2,#0x4]       @ load halfword from activation entry struct+4
ands r0,r3
strh r0,[r2,#0x4]       @ store back clearing bits[14:6]
```

操作对象是装备发动 entry 结构体的半字字段，与 `slot_field_mask_ffff803f` (card_info.inc, 用于 slot word AND) 和 `SCROLLBAR_CLEAR_BITS_14_6` (滚动条) 均域不同。新建合法。

---

## C8 stale FUN_ 核对

独立扫描 Seg-3 (L3563..5547) FUN_[0-9a-f]{8} 命中:

| 行号 | FUN_ | 所在函数 | 真实名 | proposal 处理 |
|------|------|---------|--------|-------------|
| L3561 | FUN_0804ce78 | init_equip_card_sprite_row_entry 板注释 | dispatch_card_eligibility_state_machine (asm/05 L8783, addr 0x0804ce78 confirmed) | 未被 proposal PLATE 表显式列出，但在 PLATE 的 L3690/L3814 FUN_0804ce78 替换中隐含覆盖 — **见下 Fix#1** |
| L3690 | FUN_0804ce78 | trigger_lp_bar_animation_if_ready 板 | dispatch_card_eligibility_state_machine | PLATE 表覆盖 (substring replace) |
| L3814 | FUN_0804ce78 | dispatch_lp_bar_animation_step 板 | dispatch_card_eligibility_state_machine | PLATE 表覆盖 (substring replace) |
| L4819 | FUN_08096264, FUN_08096b3c | setup_equip_slot_activation_entry_alt 板 (CJK) | setup_equip_slot_activation_entry (0x08096264 ✓) / dispatch_zone_activation_by_state (0x08096b3c, asm/12 L5686 confirmed) | PLATE 表全重写覆盖 |
| L5499 | FUN_08097bec, FUN_08098020 | init_zone_activation_display_state_p1_entry 板 | check_equip_target_slot_eligibility (0x08097bec, asm/12 L7932 confirmed) / 0x08098020 是 BL 指令地址非函数入口 (在 switchD_08097c58__caseD_1 内，asm/12 L8468) | PLATE 表 substring replace 覆盖 |

**重要发现 — C8 FAIL: L3561 的 FUN_0804ce78 未被 proposal PLATE 表覆盖。**

L3561 (`init_equip_card_sprite_row_entry` 的板注释) 包含:
```
"Callers: FUN_0804ce78, dispatch_field_display_state_by_type (equip card display sequence)."
```

Proposal PLATE 表仅列出 L3690 和 L3814 的两处 FUN_0804ce78 substring 替换，**遗漏了 L3561 的第三处**。这意味着落地后 L3561 仍会残留 `FUN_0804ce78`，Gate4 (stale FUN_ grep == 0) 将失败。

---

## C9 ASCII (板/EOL 文本)

ASM 文件 Seg-3 范围内非 ASCII 行: 4 行 (L4471, L4819, L5148, L5396)，全部在 proposal PLATE 表中列为 CJK 重写目标。

Proposal 提供的新板文本 ASCII 验证:
- setup_equip_slot_activation_entry (0x08096264): 480 字符，纯 ASCII — OK
- setup_equip_slot_activation_entry_alt (0x0809650c): **703 字符 — 超出 500 字符限制 (R2)**
- eval_zone_activation_flags_by_type (0x0809678c): **603 字符 — 超出 500 字符限制 (R2)**
- dispatch_zone_effect_by_slot (0x08096954): 297 字符，纯 ASCII — OK

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致，未跳号/回头 | PASS | §五 Seg-3: [0x08095ba8, 0x08096a4c); proposal 精确匹配；Seg-2 已 ✅，Seg-4 未开始，顺序正确 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS | 独立确认 Seg-3 含 0 ROM_INCBIN/code-.byte 块；无分类决策需求 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | Seg-3 无 §5.1 登记条目；检查项不适用 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 独立核对 41 槽含全部 NEW 首现槽，全部匹配 |
| C5 R1 复用 | 新建前确无现有可复用 | PASS | 8 个 NEW 常量逐一按值 grep 复核；0xfffff03f/0xffff803f/0x0fee 有命中但均 domain-distinct，新建合法 |
| C6 R2 名 | 槽名格式 `^[a-z][a-z0-9_]+$`，无碰撞 | PASS | 槽名格式规范；各 NEW 常量仅一处 "NEW" 声明，其余为 REUSE；无重复 label |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | Seg-3 无 carve/全局 ROW 槽；所有 DAT_ 持有整数偏移或 EWRAM 地址，无代码指针需 REF |
| C8 R5 现名 | plate 引用全用现名，无残留 FUN_ | **FAIL** | L3561 (init_equip_card_sprite_row_entry 板) 含 `FUN_0804ce78`，proposal PLATE 表未覆盖；落地后残留 1 处 stale FUN_ |
| C9 ASCII | plate/EOL 文本纯 ASCII，且 ≤500 字符 | **FAIL** | 两条新板文本超 500 字符：0x0809650c=703 字符，0x0809678c=603 字符 |
| C10 carve | 指针表条目 +1 (THUMB) 核对 | N/A | Seg-3 无指针表 carve |
| C11 误名 | 函数体全局 vs 函数名矛盾 | PASS | 14 函数名 + 4 叶函数名经 ASM 板验证均与函数体一致；无矛盾 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据，无零容忍词 | PASS | 20 条消费者证据均有 asm/12 file:line + conf:high；proposal 全文无零容忍词 |
| C13 残留 | 段内所有残留自动名槽都被覆盖，无遗漏 | PASS | 独立清点 144 槽 (116 DAT_ + 28 PTR_gP1LP)；EQ 表覆盖全部 116 DAT_；RENAME 表覆盖全部 28 PTR_ |

---

## 状态: NEEDS_FIX(2 items)

---

## 修改清单 (NEEDS_FIX，逐条可执行)

### Fix #1 — C8 — L3561 FUN_0804ce78 遗漏 PLATE 覆盖

**位置**: PLATE 表 "Additional stale FUN_ references" 节缺少第三处。

**问题**: ASM L3561 (`init_equip_card_sprite_row_entry` 的板注释) 包含:
```
"Callers: FUN_0804ce78, dispatch_field_display_state_by_type (equip card display sequence)."
```
Proposal PLATE 表仅列出 L3690/L3814 两处 FUN_0804ce78 替换，遗漏 L3561 第三处。

**修改**: 在 PLATE 表 "Additional stale FUN_ references" 节新增一行:
```
- L3561 (init_equip_card_sprite_row_entry plate): replace FUN_0804ce78 -> dispatch_card_eligibility_state_machine
```
即 PLATE 操作总数改为: 4 full rewrites + 4 substring FUN_ replacements = 8 plate operations.

### Fix #2 — C9 (R2) — 两条新板文本超出 500 字符

**位置**: PLATE 表 setup_equip_slot_activation_entry_alt (0x0809650c) 和 eval_zone_activation_flags_by_type (0x0809678c) 的替换文本。

**问题**: 
- 0x0809650c 替换文本: 703 字符 (超 500)
- 0x0809678c 替换文本: 603 字符 (超 500)

**修改**: 对两条板文本精简至 ≤500 字符，保留核心语义 (callers、参数说明、关键 constants、返回值)，删减冗余路径细节。建议裁剪后字数:

0x0809650c (目标 ≤500):
```
Structural symmetric variant of setup_equip_slot_activation_entry (indeg=1), called by dispatch_zone_activation_by_state. r0=player_side, r1=slot_idx, r2=zone_slot. If find_paired_zone_entry_for_card finds pair and player==gDuelCardCtxBase+4: writes [gP1LifePoints+ACTIVATION_STATE_A_OFF]:=0x10. Else: checks eligibility, memset(buf,0,0x18), builds activation entry, calls eval_equip_activation_for_slot. Extended path: get_card_extended_stat_field6==0x16/0x17 -> build_zone_activation_entry_blocked / build_zone_activation_entry_equip. Returns 0x8 if activatable, else 0.
```
(约 467 字符)

0x0809678c (目标 ≤500):
```
Evaluates zone_type (r1) activation flags for a single zone (indeg=1). Zone 0xb (FIELD_SPELL_ZONE): LP threshold check via gP1LifePoints[player*0x868+0xc], then setup_equip_context_for_zone_activation; success sets r6|=0x8. Zones 0xc..0xf: check_zone_slot_card_activatable -> dispatch_zone_effect_by_slot, OR into r6; opposite player and zone==0xd: r6|=0x1000. Other: setup_equip_context_for_slot_activation. Returns r6 (combined activation flags).
```
(约 377 字符)

---

## Reviewer Verdict: F12-Seg-3 = NEEDS_FIX(2 items)
