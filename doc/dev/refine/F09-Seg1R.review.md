# Refine Review: F09-Seg1R (Remediation)

> Reviewer: independent, self-run ref-scan + ROM byte verification
> Scope: doc/dev/refine/F09-Seg1R.proposal.md

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | Seg-1R 是 Seg-1 (commit 08b3db1) 的事后修补 addendum，路线图 §五 Seg-1 已完成，本提案不改变地址序 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | ❌ | 见 #1 — Seg-1 范围内有 9 个 ROM_INCBIN + 11 个 .byte 体被静默保留，提案仅处理其中 7 块 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | §5.1 = 0；所有 7 块均有引用（B1 THUMB+1 @ 0x1e40958，B2a/b/c/d/B2e/B2f raw @ dispatch table）。自主重跑 ref-scan 确认：7 个块中间地址全部 raw=0, THUMB+1=0 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | ✅ | gduel_phase_f034 @ 0x0806f034: ROM=0x0201b290 == 提案值 OK；equip_disp_tbl_f038 @ 0x0806f038: ROM=0x0806f03c == 提案值 OK |
| C5 R1 复用 | 新建 constants 前确无现有可复用 | ✅ | gDuelPhaseFlags: constants/ewram.inc:352 `.equ gDuelPhaseFlags, 0x0201b290` (676 raw refs)；equip_disp_table_f03c: asm/09 line 1261 现有 label。两个 REF 槽均 REUSE，无新 constant 创建 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`，无碰撞 | ✅ | gduel_phase_f034 / equip_disp_tbl_f038 均符合规则；asm/09 无现有碰撞 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref | ✅ N/A | 无 carve 块；REF 槽为内部 literal pool，被 eligible_creature_swap_f008 内部消费 |
| C8 R5 现名 | plate 引用全用现名，无残留旧 FUN_ | ✅ | 7 块所在区域无 FUN_ plate 引用；PLATE=0 正确。asm/09 line 12436 的 FUN_ 在 Seg-6 范围，与本提案无关 |
| C9 ASCII | 所有 plate/EOL 文本纯 ASCII | ✅ | PLATE=0，无 Ghidra EOL/plate 定义。提案 L467 含 § (U+00A7) 在执行报告散文中（非 plate/EOL 定义），不违反 C9 |
| C10 carve | 指针表条目 `+1` (THUMB)，`.word <fn>+1` | ✅ N/A | 无 carve 块 |
| C11 误名 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | ✅ | equip_disp_sub_f078/f0ac/f0cc/f188 + eligible_creature_swap_f008 均为 body labels（非 Ghidra fn objects）；eligible_sub_stubs_f054 命名不精确（非 fn_eligible）但提案已 documented，FUNC_RENAME=0 合理 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | 两个 EQ 槽均有 asm/09 line 引用 + conf:high；B1 FS handler 证据有 ROM file offset 0x1e40954..0x1e40958 |
| C13 残留 | 段内所有残留自动名槽都被覆盖（无遗漏） | ❌ | 见 #1 — 提案 7 块之外的 9 个 ROM_INCBIN 未处理（同 C2）；DWORD_0806f0a0 (EQUIP_PHASE_FRAME_OFF) 属预存 auto-name，提案未纳入（次要，非本批新引入） |

---

## 独立验证结果

### ref-scan（自主重跑）

7 个块的 ENTRY 地址 ref-scan 结果（raw + THUMB|1）:

| Block | Entry | raw 命中 | THUMB+1 命中 | 判断 |
|-------|-------|---------|------------|------|
| B1 | 0x0806f008 | raw=1 @ 0x806d7 | THUMB+1=1 @ 0x1e40958 | CODE (fn_eligible) |
| B2a | 0x0806f078 | raw=1 @ 0x6f048 | 0 | CODE (dispatch table entry[3]) |
| B2b | 0x0806f0ac | raw=1 @ 0x6f044 | 0 | CODE (dispatch table entry[2]) |
| B2c | 0x0806f0cc | raw=1 @ 0x6f040 | 0 | CODE (dispatch table entry[1]) |
| B2d | 0x0806f188 | raw=1 @ 0x6f03c | 0 | CODE (dispatch table entry[0]) |
| B2e | 0x0806f054 | raw=1 @ 0x6f050 | 0 | CODE (dispatch table entry[5]) |
| B2f | 0x0806f066 | raw=1 @ 0x6f04c | 0 | CODE (dispatch table entry[4]) |

所有 7 个块中间地址 raw=0, THUMB+1=0（已自主验证）。

### dispatch table（自主读 ROM）

ROM @ 0x0806f03c（6 entry .word 表）:
- [0] 0x0806f188 -> equip_disp_sub_f188 (B2d) OK
- [1] 0x0806f0cc -> equip_disp_sub_f0cc (B2c) OK
- [2] 0x0806f0ac -> equip_disp_sub_f0ac (B2b) OK
- [3] 0x0806f078 -> equip_disp_sub_f078 (B2a) OK
- [4] 0x0806f066 -> equip_disp_sub_f066 (B2f) OK
- [5] 0x0806f054 -> eligible_sub_stubs_f054 (B2e) OK

与提案完全一致。

### FS handler table（B1 验证）

ROM file offset 0x1e4094c (GBA addr 0x09e4094c 映射到 ROM[0x1e4094c]):
- [+0x00] 0x08057471 (fn_ptr0)
- [+0x04] 0x00000000 (NULL)
- [+0x08] 0x0000142a (CID = 0x142a = Creature Swap) — constants/card_info.inc:1384 确认
- [+0x0c] 0x0806f009 (eligible_creature_swap_f008+1 = THUMB+1) OK
- [+0x10] 0x080508cd (fn_activate+1)
- [+0x14] 0x0805ec41 (fn_ptr3)

与提案一致。

### 指令级解码验证（ROM 字节直读）

**B1 关键指令 (0x6f00a..0x6f030)**:
- 0x6f00a: 0x4647 = mov r7,r8 OK
- 0x6f018: 0x00db = lsls r3,r3,#3 OK (0x94<<3=0x4a0)
- 0x6f024: 0xd900 = bls +0 -> 0x6f028 OK
- 0x6f026: 0xe0c6 = b -> 0x0806f1b6 (epilogue) OK (手算: offset=0xc6<<1=0x18c, target=0x6f02a+0x18c=0x6f1b6)
- 0x6f030: 0x4687 = mov r15,r0 OK (computed jump)

**B1 pool (自主 PC-relative 验算)**:
- ldr r0,[pc,+0x1c] @ 0x6f014: PC=(0x6f014+4)&~2=0x6f018; pool=0x6f018+0x1c=0x6f034; ROM[0x6f034]=0x0201b290 OK
- ldr r1,[pc,+0xc] @ 0x6f02a: PC=(0x6f02a+4)&~2=0x6f02c; pool=0x6f02c+0xc=0x6f038; ROM[0x6f038]=0x0806f03c OK

**B2a body (0x6f07a..0x6f09b)**:
- 0x6f07a: 0x1821 = adds r1,r4,r0 OK (r4=gDuelPhaseFlags, r0=EQUIP_PHASE_FRAME_OFF from entry)
- 0x6f07c: 0x4809; PC-pool=0x6f0a4=0x0201c4e0=gP1LifePoints OK
- 0x6f07e: 0x4a0a; PC-pool=0x6f0a8=0x00001da8=LP_CARD_TRACK_BASE_OFF OK
- BL @ 0x6f096..0x6f098: target=0x080a1cb4=set_lp_display_row_type9 OK
- 0x6f09a: 0x207d = movs r0,#0x7d OK

**B2b body (0x6f0ae..0x6f0bf)**:
- 0x6f0ae: 0x00c9 = lsls r1,r1,#3 OK
- 0x6f0b2: 0x4904; PC-pool=0x6f0c4=0x0201c4e0=gP1LifePoints OK
- 0x6f0b4: 0x4a04; PC-pool=0x6f0c8=0x00001da8=LP_CARD_TRACK_BASE_OFF OK
- 0x6f0be: 0x207c = movs r0,#0x7c OK

**B2c body start (0x6f0ce..)**:
- 0x6f0ce: 0x07d9 = lsls r1,r3,#31 OK
- 0x6f0d0: 0x0fc9 = lsrs r1,r1,#31 OK
- 0x6f0d2: 0x482c; PC-pool=0x6f184=0x000004a4=EQUIP_PHASE_FRAME_OFF OK
- 0x6f0d4: 0x1900 = adds r0,r0,r4 OK
- 0x6f0d6: 0x4680 = mov r8,r0 OK
- BL @ 0x6f0dc..0x6f0de: target=0x0803670c=query_slot_card_type_eligibility OK
- 0x6f17e: 0x207b = movs r0,#0x7b OK

**B2d body (0x6f18a..0x6f1c2)**:
- 0x6f18a: 0x07d8 = lsls r0,r3,#31 OK
- 0x6f18c: 0x0fc0 = lsrs r0,r0,#31 OK
- 0x6f18e: 0x4a0d; PC-pool=0x6f1c4=0x000004a4=EQUIP_PHASE_FRAME_OFF OK
- BL @ 0x6f198..0x6f19a: target=0x0804a970=set_field_slot_bit_with_sprite_update OK
- 0x6f19c: 0x78ad = ldrb r5,[r5,#2] OK

**共享 epilogue (0x6f1b6..0x6f1c2)**:
- 0x6f1b6: 0x2000 = movs r0,#0 OK
- 0x6f1b8: 0xb001 = add sp,#4 OK
- 0x6f1ba: 0xbc08 = pop {r3} OK
- 0x6f1bc: 0x4698 = mov r8,r3 OK
- 0x6f1be: 0xbcf0 = pop {r4,r5,r6,r7} OK
- 0x6f1c0: 0xbc02 = pop {r1} OK
- 0x6f1c2: 0x4708 = bx r1 OK

**B2e body (0x6f056..0x6f064)**:
- 0x6f056: 0x1c11 = adds r1,r2,#0 OK
- BL @ 0x6f058..0x6f05a: target=0x08090848=dispatch_card_effect_activation OK
- 0x6f05e: 0xd100 = bne -> 0x6f062 OK (offset=0; target=0x6f05e+4=0x6f062)
- 0x6f060: 0xe0a9 = b -> 0x0806f1b6 (return 0) OK
- 0x6f062: 0x207f = movs r0,#0x7f OK
- 0x6f064: 0xe0a8 = b -> 0x0806f1b8 (epilogue skip movs) OK

**B2f body (0x6f068..0x6f076)**:
- 0x6f068: 0x07e2 = lsls r2,**r4**,#31 (**注意**: 提案写 r3，实为 r4；equip_disp_sub_f066 entry 在 0x6f066 = ldrb r4,[r5,#2] 把 flags byte 存入 r4，故正确操作数是 r4，提案描述有误，但不影响 disasm 执行)
- 0x6f06a: 0x0fd0 = lsrs r0,r2,#31 OK
- 0x6f06c: 0x8829 = ldrh r1,[r5,#0] OK
- 0x6f06e: 0x1c02 = adds r2,r0,#0 OK
- BL @ 0x6f070..0x6f072: target=0x080a1cb4=set_lp_display_row_type9 OK
- 0x6f074: 0x207e = movs r0,#0x7e OK
- 0x6f076: 0xe09f = b -> 0x0806f1b8 OK

### b+pad .word 字节核对

- 0x6f09c: ROM=0xe08c -> b+pad 目标 (0x6f09c+4+0x18c=0x6f1b8) = 0x0806f1b8 OK (与 .word 0x0000e08c 字节等价)
- 0x6f0c0: ROM=0xe07a -> 目标 (0x6f0c0+4+0xf4=0x6f1b8) OK — 注意: offset = 0x07a<<1 = 0xf4; target=0x6f0c4+0xf4=0x6f1b8 OK
- 0x6f180: ROM=0xe01a -> 目标 (0x6f180+4+0x34=0x6f1b8) OK

---

## 需修复项

### #1 — C2/C13 — Seg-1 范围内 9 个 ROM_INCBIN + 11 个 .byte 体静默保留

提案标题为 "F09-Seg-1 REMEDIATION [0x0806e76c..0x0806ff50)"，但仅处理 0x6f008..0x6f1c3 子集内的 7 块。Seg-1 全段 [0x6e76c, 0x6ff50) 内仍存在以下未处理残留：

**ROM_INCBIN 块（自主统计，grep asm/09 实测）**:

| 地址 | 大小 | 所属 stub |
|------|------|-----------|
| 0x6f85e | 0x136 | eligible_destiny_board_f85c body |
| 0x6fa0a | 0x36 | eligible_sub_stubs_fa08 body |
| 0x6fa62 | 0x12 | equip_lp_sub_fa5e body |
| 0x6fa78 | 0x8c | equip_lp_sub_fa74 body |
| 0x6fb16 | 0x32 | equip_lp_sub_fb14 body |
| 0x6fdee | 0x26 | eligible_cathedral_of_nobles_fdec body |
| 0x6fe8a | 0x4a | eligible_sub_stubs_fe88 body |
| 0x6fede | 0x12 | equip_chain_act_sub_fedc body |
| 0x6fef2 | 0x18 | equip_chain_act_sub_fef0 body |

**同模式 .byte 体（entry decoded, body .byte）**:

| 地址 | 大小 | 所属 stub |
|------|------|-----------|
| ~0x6fa4e | 0x10 | equip_lp_sub_fa4c body |
| ~0x6fb4e | 0x0a | equip_lp_sub_fb4c body |
| ~0x6fb5a | 0x0a | equip_lp_sub_fb58 body |
| ~0x6fb66 | 0x0a | equip_lp_sub_fb64 body |
| ~0x6fb72 | 0x04 | equip_lp_sub_fb70 body |
| ~0x6fb78 | 0x10 | equip_lp_sub_fb76 body |
| ~0x6ff0c | 0x0e | equip_chain_act_sub_ff0a body |
| ~0x6ff1c | 0x10 | equip_chain_act_sub_ff1a body |
| ~0x6ff2c | 0x0e | equip_chain_act_sub_ff2c body |
| ~0x6ff3e | 0x08 | equip_chain_act_sub_ff3c body |
| ~0x6ff48 | 0x04 | equip_chain_act_sub_ff46 body |

**修复方案 A（推荐）**: 将提案范围重新标注为 "F09-Seg-1R Cluster-1 (0x0806f008..0x0806f1c3)"，明确说明剩余 Cluster-2 (0x6f85e..0x6fb87) 和 Cluster-3 (0x6fdec..0x6ff4f) 待后续 Seg-1R2/Seg-1R3 处理。无需修改 Ghidra 脚本或 disasm 计划本身——仅更正提案文档 scope 标注。

**修复方案 B**: 扩展本提案，纳入 Cluster-2 和 Cluster-3 的 ref-scan + disasm 计划，一次性解决全段残留。

### #2 — C2（描述性） — B2f body 寄存器描述错误

提案 B2f 0x6f068 写"lsls r2,r3,#31"，实际 ROM 字节 0x07e2 解码为 lsls r2,**r4**,#31（r4 在 equip_disp_sub_f066 entry 0x6f066 处被 ldrb r4,[r5,#2] 赋值）。描述性错误，不影响 DisassembleCommand 执行正确性，但应订正提案文档以避免歧义。

---

## 已通过检查汇总

- C3: 7 块 entry ref-scan 独立验证 OK（自主重跑，不信提案结论）。
- C4: 2 个 EQ 槽 ROM 值自主读取确认 OK。
- C5: gDuelPhaseFlags + equip_disp_table_f03c 均为 REUSE，无误建。
- C6: 2 个槽名合法，无碰撞。
- C8: 7 块区域无 stale FUN_ plate。
- C9: 无 plate/EOL 含 CJK；§ 符号在 doc 散文不违规。
- C10/C7: 无 carve，N/A。
- C11: 命名问题已文档化，FUNC_RENAME=0 合理。
- C12: EQ 槽证据完整 (file:ROM offset + conf:high)。
- disasm 计划: B2d-first 顺序正确（epilogue label 先创建供其他块引用）；clearListing 边界均不覆盖 pool DWORDs；b+pad 字节核对 OK；byte-identical 风险低（所有 b 分支编码与 ROM 等价）。

---

## 状态

**C2 #1（9 ROM_INCBIN + 11 .byte 体静默保留）是真实违规**，但性质是"部分覆盖"而非"错误覆盖"——提案对已声明的 7 块的处理方案完全正确，不会引入新的字节错误。

如果调用方接受"增量修补"语义（本次修 Cluster-1，后续再修 Cluster-2/3），则本提案对其自身 7 块可直接落地，仅需订正标题 scope 并登记剩余块。如果要求单次 REMEDIATION 覆盖全 Seg-1 残留，则 NEEDS_FIX。

**裁定采用严格解释（提案标题声明全 Seg-1 范围，必须全覆盖）**:

## Reviewer Verdict: F09-Seg1R = NEEDS_FIX(2 items)
