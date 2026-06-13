# Refine Review: F05-Seg-6

Reviewer: refine-reviewer (independent)
Proposal: `doc/dev/refine/F05-Seg-6.proposal.md`
Segment: ROM `0x0804d124..0x0804ffba` (~24 fn), `asm/05_equip_eligibility_a.s`
ROM: `roms/2343.gba` (base 0x08000000)
Review iteration: iter-4 (final re-review after fixer mode-A iter-3; exhaustive FUN_ closure)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | Seg-6 = 0x4d124..0x4ffba, 路线图完全匹配 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块有归宿 | OK | 2 块均归 R4 disasm; 无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | 无 §5.1 块; 两块均 raw=1, THUMB+1=0 (独立 ref-scan 验证) |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 独立 python 核对 117 个槽地址全部匹配 (iter-1 结论维持) |
| C5 R1 复用 | 新建常量前无同值碰撞 | OK | 两项碰撞均已修复 (HARPIE_LADY_SISTERS_CID + SLOT_CARD_EMPTY; iter-2 验证维持) |
| C6 R2 名 | 槽名规范无碰撞 | OK | 函数名均 `^[a-z][a-z0-9_]+$`; switchD_/caseD_ 免 regex 约束 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | OK | 无 carve; REF_SLOTS 有 jump table USER-label 计划 |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | OK | iter-4 穷举 grep 确认: 9 unique FUN_, 13 occurrences, proposal 全覆盖 (含 3 跨模块); 见下方详细结果 |
| C9 ASCII | plate/EOL 文本纯 ASCII | OK | 段内现有 asm 0 非 ASCII; proposal 文本纯 ASCII |
| C10 carve | 指针表条目正确 | OK | 无 carve 块; jump table 用 raw addr (bx r0 dispatch) 非 THUMB+1, 符合实际 |
| C11 误名 | 函数体/函数名无矛盾 | OK | 24 函数名语义与函数体一致 (抽查通过) |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | OK | 7 个 SPRITE_ROW 偏移、gEquipZoneRankState、FIELD5_SCORE_THRESHOLD_1299 均有 asm 行号 + high-conf 标注 |
| C13 残留 | 段内所有残留自动名槽均覆盖 | OK | 117 个标签定义全覆盖; RENAME→EQ 变动不减少覆盖率 |

---

## iter-4: C8 穷举 grep 独立复核结果

### 执行命令

```
awk 'NR>=8945 && NR<=11663' asm/05_equip_eligibility_a.s | grep -oE "FUN_[0-9a-f]{8}" | sort | uniq -c
```

### 结果 (9 unique FUN_, 13 total occurrences)

| count | FUN_ 地址 | proposal 条目 | 状态 |
|---|---|---|---|
| 1 | FUN_0804d1e4 | item 2 -> dispatch_sprite_row_anim_by_state | 覆盖 ✓ |
| 2 | FUN_0804f2e0 | item 3 -> dispatch_equip_field_update_by_anim_state | 覆盖 ✓ |
| 1 | FUN_0804f2ee | item 6 -> call-site rewrite (bl at 0x0804f2ee) | 覆盖 ✓ |
| 1 | FUN_0804f34c | item 4 -> advance_equip_zone_rank_state | 覆盖 ✓ |
| 1 | FUN_0804f3da | item 6 -> call-site rewrite (bl at 0x0804f3da) | 覆盖 ✓ |
| 4 | FUN_0804f6c4 | item 5 -> check_slot_card_eligible_by_card_id | 覆盖 ✓ |
| 1 | FUN_08094cd4 | item 7 -> tick_equip_activation_main_sequence | 覆盖 ✓ |
| 1 | FUN_08053d88 | item 8 -> check_equip_slot_eligible_by_opposite_side_zone_chain | 覆盖 ✓ |
| 1 | FUN_08054d08 | item 9 -> check_equip_slot_eligible_by_whitelist_field7_and_zone_bit | 覆盖 ✓ |

FUN_0804ce98: 0 occurrences confirmed (pre-emptive item 1 pass) ✓

总计: 13 occurrences, 9 unique FUN_, 与 proposal 声明完全一致。

### 跨模块 3 项现名独立核实

| stale FUN_ | 现名 | 所在文件 | 定义行 | 独立确认 |
|---|---|---|---|---|
| FUN_08094cd4 | tick_equip_activation_main_sequence | asm/12_equip_activation_scan.s | L1570 | confirmed via grep |
| FUN_08053d88 | check_equip_slot_eligible_by_opposite_side_zone_chain | asm/06_equip_eligibility_b.s | L853 | confirmed via grep |
| FUN_08054d08 | check_equip_slot_eligible_by_whitelist_field7_and_zone_bit | asm/06_equip_eligibility_b.s | L3209 | confirmed via grep |

3 处实际 stale FUN_ 行号核实 (asm 文件独立查验):

| 绝对行 | stale FUN_ | 行内容摘要 |
|---|---|---|
| L9629 | FUN_08094cd4 | `@ Called exclusively by FUN_08094cd4 (top-level equip field frame update).` |
| L10029 | FUN_08053d88 | `@ All pass returns 1. Called by FUN_08053d88 (checks slot[+0xa] halfword before dispatching).` |
| L10166 | FUN_08054d08 | `@ Called by FUN_08054d08 which continues with field7/zone_bit checks. indeg=1, pure predicate.` |

### awk 行边界核实

- L8945: `switchD_0804ce98__caseD_1e:` (= 0x0804d124 段起点) ✓
- L11663 boundary note: awk range NR<=11663 包含 L11619-11663 (check_slot_zone_bit3_eligible 等, 属 Seg-7 地址 >=0x4ffba), 但这些行不含任何 FUN_ 引用 (独立验证: 0 hits)。FUN_0804f6c4 的 4 次出现中 2 次 (L11619/L11633) 属于 Seg-7 函数 plate, proposal item 5 已全覆盖。后置验证命令覆盖这 2 处, 无遗漏。

### 后置验证命令充分性

post-replacement 命令:
```
awk 'NR>=8945 && NR<=11663' asm/05_equip_eligibility_a.s | grep -E "FUN_[0-9a-f]{8}"
```
- 模式 `FUN_[0-9a-f]{8}` 匹配所有小写十六进制 FUN_ (独立核实: 段内无大写 FUN_[A-F] 变体)
- 覆盖全部 9 个 unique FUN_ 地址
- 落地后须返回 0 行; 任何命中 = 替换未完成 = abort ✓

---

## iter-3 已解决项 (维持 PASS)

### C8 #5 三处跨模块 stale FUN_ — RESOLVED ✓

proposal 已加入 items 7/8/9:
- item 7: FUN_08094cd4 → tick_equip_activation_main_sequence (L9629) ✓
- item 8: FUN_08053d88 → check_equip_slot_eligible_by_opposite_side_zone_chain (L10029) ✓
- item 9: FUN_08054d08 → check_equip_slot_eligible_by_whitelist_field7_and_zone_bit (L10166) ✓

---

## iter-2 维持项 (PASS)

### C5 #1: HARPIE_LADY_SISTERS_CID — RESOLVED ✓
### C5 #2: DAT_0804f6c0 EQ 复用 SLOT_CARD_EMPTY — RESOLVED ✓
### iter-2 #4: FUN_0804f2e0 第 2 处 (L9360) 已加入 proposal item 3 — RESOLVED ✓
### iter-3 #3: FUN_0804f2ee/FUN_0804f3da call-site 改写 — RESOLVED ✓

---

## Ref-scan 独立结果 (维持 iter-1)

| 块 | raw refs | THUMB+1 refs | 分类 |
|---|---|---|---|
| 0x0804d294 (sz 0x862) | 1 @0x0804d258 (PTR_DAT_0804d258[0]) | 0 | R4 disasm (有引用) |
| 0x0804dd58 (sz 0x136a) | 1 @0x0804dbb8 (PTR_DAT_0804dbb8[0]) | 0 | R4 disasm (有引用) |

---

## 状态: PASS

所有 C1-C13 检查通过。proposal FUN_ 穷举闭合: 9 unique addresses, 13 total occurrences, 全部有对应替换计划, 后置验证命令充分。

---

## 修改清单

无。所有先前 NEEDS_FIX 项均已解决。

---

## 备注 (非阻断)

- **awk 上界含 Seg-7 spillover (L11619-11663)**: 边界比真实 Seg-6 末尾 (L11618) 多取 45 行; 这些行不含任何 FUN_ 引用, 对 C8 无影响。其中 FUN_0804f6c4 的 2 次 Seg-7 plate 出现 (L11619/L11633) 已在 proposal item 5 统计并覆盖。
- **ROM_INCBIN 判为 disasm 非 carve**: Block1/Block2 内部多个 THUMB sub-handler 互相跳转且无外部 bl 调用者; Jump table 用 raw addr + bx r0 dispatch, 不适用 fn-ptr +1 规则。
- **FUN_0804f6c4 已有现名 check_slot_card_eligible_by_card_id**: 4 处 plate 替换后无残留。

---

## Reviewer Verdict: F05-Seg-6 = PASS
