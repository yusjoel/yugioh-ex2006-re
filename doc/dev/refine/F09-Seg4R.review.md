# Refine Review: F09-Seg4R

**Scope**: file 09 `asm/09_equip_lp_display.s`, Seg-4 remediation [0x080719fc, 0x08072d20).
**Proposal**: `doc/dev/refine/F09-Seg4R.proposal.md`
**ROM**: `roms/2343.gba` (SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b target)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | Seg-4 = 4a [0x719fc,0x72404) + 4b [0x72404,0x72d20); 与 p5-refine-09.md §三 一致; 无跳号/回头 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS | 12 块全部列出: 4 ROM_INCBIN + 4 .byte CODE + 4 .byte DATA; 均有处置计划 |
| C3 Rule3 | 8 个 CODE 块确 0 引用 | PASS | 独立重跑 ref-scan: 全部 raw=0, THUMB+1=0 (详见下方 ref-scan 表) |
| C4 R1 值 | EQ slot 4 字节小端核对 | PASS | 0x72830=a8 1d 00 00=0x1da8 ✓; 0x727b4=b9 01 00 00=0x1b9 ✓ |
| C5 R1 复用 | 无新建常量, 全 REUSE | PASS | LP_CARD_TRACK_BASE_OFF=0x1da8 @ ewram.inc:247 ✓; lookup_equip_score_b_0x1b9=0x1b9 @ duel_field.inc:332 ✓ |
| C6 R2 名 | 槽名格式 + 无碰撞 | PASS | 无新建 label; 所有 CODE 块目标均为现有 LAB_ 延续; EQ 槽用现有常量名 |
| C7 R3 接通 | REF_SLOTS 有 USER-label + DATA-ref 计划 | PASS | 3 REF 槽目标均为现有 label (last_turn_sub_2534/vampire_sub_26bc/equip_zone_sub_2856); createDWord 后 Ghidra 自动引用 |
| C8 R5 现名 | 无 plate/rename; 无残留旧 FUN_ | PASS | 此 remediation 无 PLATE 计划; 无函数改名; 未引入新 FUN_ 引用 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 此 proposal 无任何 Ghidra plate/EOL 文本; doc/ 中 CJK 段落标题不影响 Ghidra |
| C10 carve | 指针表条目 raw (lsb=0), via mov r15,r0 非 BX | PASS | C1/C2/C3 dispatch table 全部条目 lsb=0 (raw addr); 分派代码用 `mov r15,r0` 非 BX -- 在 GBA ARM7TDMI THUMB 模式下 MOV PC,rN 不切换模式, 保持 THUMB ✓ |
| C11 误名 | 无函数改名需求 | PASS | 本 remediation 无 FUNC_RENAME; 含函数均已正确命名 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | NEEDS_FIX | **B1 BL 目标名错误**: 提案称 `set_lp_row_type6_with_value @ 0x080a1c2c`, 实际该地址是 `set_lp_display_row_type5` (asm/13:7899); set_lp_row_type6_with_value 在 0x080a1c48; 提案引用的 consumer 证据 (asm/09:11181 `bl set_lp_row_type6_with_value @ 0807351e`) 也错, 0x807351e BL 目标实际是 0x080a1c48; B4/C4 BL 目标 (0x080933dc/0x08093390) 正确 |
| C13 残留 | 全残留覆盖 | PASS | 4 ROM_INCBIN + 8 .byte = 12 块; 全部有处置; post-state 0 ROM_INCBIN + 0 .byte-code |

---

## 独立 ref-scan 结果

自跑 `rom.count(struct.pack('<I', addr))` + `rom.count(struct.pack('<I', addr|1))`:

| 块 | 地址 | raw | THUMB+1 | 判定 |
|---|---|---|---|---|
| B1 ROM_INCBIN | 0x080720e2 | 0 | 0 | CODE |
| B2 ROM_INCBIN | 0x0807270e | 0 | 0 | CODE |
| B3 ROM_INCBIN | 0x0807276a | 0 | 0 | CODE |
| B4 ROM_INCBIN | 0x08072794 | 0 | 0 | CODE |
| C1 .byte CODE | 0x08071f74 | 0 | 0 | CODE |
| C2 .byte CODE | 0x0807241c | 0 | 0 | CODE |
| C3 .byte CODE | 0x0807256a | 0 | 0 | CODE |
| C4 .byte CODE | 0x08072838 | 0 | 0 | CODE |

---

## 独立字节核对

**Branch instructions (intra-function -> CODE block):**

| 块 | branch addr | ROM hw | 目标 | 核对 |
|---|---|---|---|---|
| B1 | 0x8072062 | 0xd13e (bne imm8=0x3e) | 0x080720e2 | OK |
| B2 | 0x8072704 | 0xd103 (bne imm8=0x03) | 0x0807270e | OK |
| B3 | 0x8072766 | 0xd100 (bne imm8=0x00) | 0x0807276a | OK |
| B4 | 0x8072778 | 0xd10c (bne imm8=0x0c) | 0x08072794 | OK |
| C1 | 0x8071f70 | 0xd900 (bls imm8=0x00) | 0x08071f74 | OK |
| C2 | 0x8072418 | 0xd900 (bls imm8=0x00) | 0x0807241c | OK |
| C3 | 0x8072566 | 0xd900 (bls imm8=0x00) | 0x0807256a | OK |
| C4 | 0x807280e | 0xd013 (beq imm8=0x13) | 0x08072838 | OK |

**BL 目标反算:**

| 块 | BL_hi addr | ROM HI | ROM LO | 计算目标 | 期望 | 核对 |
|---|---|---|---|---|---|---|
| B1 | 0x80720ec | 0xf02f | 0xfd9e | 0x080a1c2c | set_lp_display_row_type5 | OK |
| B4 | 0x80727aa | 0xf020 | 0xfe17 | 0x080933dc | invoke_card_display_op_0x31_sub3_with_packed_params | OK |
| C4 | 0x8072840 | 0xf020 | 0xfda6 | 0x08093390 | trigger_card_display_op31_if_not_active | OK |

**B1 BL target identity** (asm/13 cross-reference):
- 0x080a1c2c = `set_lp_display_row_type5` (asm/13_equip_placement.s:7899, confirmed ROM byte 0xb510=push{r4,lr})
- 0x080a1c48 = `set_lp_row_type6_with_value` (asm/13_equip_placement.s:7917, confirmed ROM byte 0xb500=push{lr})
- Proposal incorrectly labels 0x080a1c2c as `set_lp_row_type6_with_value`.

**DATA .word slots:**

| 槽 | ROM addr | ROM bytes | 值 | 期望 | 核对 |
|---|---|---|---|---|---|
| last_turn_sub_2534 | 0x08072430 | 34 25 07 08 | 0x08072534 | 0x08072534 | OK |
| vampire_sub_26bc | 0x0807257c | bc 26 07 08 | 0x080726bc | 0x080726bc | OK |
| equip_zone_sub_2856 | 0x08072734 | 56 28 07 08 | 0x08072856 | 0x08072856 | OK |
| LP_CARD_TRACK_BASE_OFF | 0x08072830 | a8 1d 00 00 | 0x00001da8 | 0x00001da8 | OK |

**B3 forward branch -> B4 landing:**
- b @ 0x8072784: 0xe013 -> 0x080727ae (inside B4 range [0x72794,0x727b3]) OK
- b @ 0x80727b0: 0xe059 -> epilogue 0x08072866 OK
- B4 b @ 0x80727b0 confirmed (not B3)

**clearListing 范围边界:**

| 块 | 范围 | 大小 | 下一 word | 安全 |
|---|---|---|---|---|
| B1 | 0x80720e2..0x80720f3 | 0x12 | pool at 0x80720f4 (already decoded instr) | OK |
| B2 | 0x807270e..0x807272b | 0x1e | pool_b7_272c @ 0x807272c | OK |
| B3 | 0x807276a..0x8072787 | 0x1e | pool_b8_2788 @ 0x8072788 | OK |
| B4 | 0x8072794..0x80727b3 | 0x20 | pool_b8_27b4 @ 0x80727b4 | OK |
| C1 | 0x8071f74..0x8071f7f | 0x0c | pool_1f80 @ 0x8071f80 | OK |
| C2 | 0x807241c..0x8072427 | 0x0c | pool @ 0x8072428 | OK |
| C3 | 0x807256a..0x8072573 | 0x0a | pool_b6_2574 @ 0x8072574 | OK |
| C4 | 0x8072838..0x8072847 | 0x10 | equip_zone_sub_2848 @ 0x8072848 | OK |

**pc-relative load addresses:**

| 指令 | 地址 | PC align | offset | load_addr | ROM 值 | 期望 |
|---|---|---|---|---|---|---|
| C1 ldr r1,[pc,#12] | 0x8071f76 | 0x8071f78 | 12 | 0x8071f84 | 0x08071f88 (table base) | OK |
| C2 ldr r1,[pc,#12] | 0x807241e | 0x8072420 | 12 | 0x807242c | 0x08072430 (table base) | OK |
| C3 ldr r1,[pc,#8] | 0x807256c | 0x8072570 | 8 | 0x8072578 | 0x0807257c (table base) | OK |
| B2 ldr r0,[pc,#28] | 0x807270e | 0x8072710 | 28 | 0x807272c | 0x0201b290 (gDuelPhaseFlags) | OK |
| B2 ldr r1,[pc,#8] | 0x8072724 | 0x8072728 | 8 | 0x8072730 | 0x08072734 (dispatch table) | OK |
| B3 ldr r0,[pc,#36] | 0x807276a | 0x807276c | 36 | 0x8072790 | 0x0201e2a0 (gDuelCardCtxBase) | OK |
| B4 ldr r2,[pc,#20] | 0x807279c | 0x80727a0 | 20 | 0x80727b4 | 0x000001b9 (lookup_equip_score_b_0x1b9) | OK |

---

## 次要观察 (非 NEEDS_FIX)

**C2 branch 地址引用笔误**: 提案称 "bls LAB_0807241c at asm:8710 (0x807241a 00d9)". 实际 bls 在 0x8072418 (00d9); 0x807241a 是 not-taken 的 b 指令 (0xe08d). asm 行 8709 正确显示 `bls LAB_0807241c @ 08072418 00d9`. 不影响字节一致性 (Ghidra 从 bls 自然引导 DC 到 C2 块).

**C3 第一条指令**: 提案写 `0x7256a [0088]: lsls r0,r1,#2; r0 = r1*4 (r1 = phase_offset; note: r0 used as index NOT r0)` -- 注释中的 "note" 文字混乱但机器码正确: hw=0x0088 = lsls r0,r1,#2 ✓.

---

## 修改清单 (NEEDS_FIX)

### #1 -- C12 -- B1 BL 目标名称错误 (proposal prose 修正)

**地址**: B1 ROM_INCBIN 0x720e2 BL 指令 @ 0x80720ec/0x80720ee

**错误**: 提案 "消費者証拠" 节写:
```
Block1 (0x720e2) BL -> set_lp_row_type6_with_value:
- Consumer: asm/09_equip_lp_display.s:11181 `bl set_lp_row_type6_with_value @ 0807351e`
```

**事实**:
1. ROM bytes 验证: BL @ 0x80720ec target = 0x080a1c2c (verified: HI=0xf02f, LO=0xfd9e)
2. asm/13_equip_placement.s:7899 shows `set_lp_display_row_type5:` @ 0x080a1c2c
3. asm/13_equip_placement.s:7917 shows `set_lp_row_type6_with_value:` @ 0x080a1c48
4. asm/09:11181 `bl set_lp_row_type6_with_value @ 0807351e` -- 此处 BL target 经 ROM 字节反算 = 0x080a1c48, 非 0x080a1c2c

**必须修正**: 提案 "消費者証拠" 节 Block1 改为:
```
Block1 (0x720e2) BL -> set_lp_display_row_type5:
- ROM bytes: HI=0xf02f, LO=0xfd9e -> target = 0x080a1c2c
- asm/13_equip_placement.s:7899 confirms set_lp_display_row_type5 @ 0x080a1c2c
- Params: r0=player_side, r1=card_id, r2=1 -> set_lp_display_row_fields(player, 5, card_id&0xffff, 1)
- Confidence: high (BL encoding verified; asm label confirmed)
```

**字节一致性影响**: NONE. Ghidra 知道 0x080a1c2c 的正确标签 set_lp_display_row_type5, 反汇编导出时自动生成 `bl set_lp_display_row_type5`, 汇编器正确计算相对偏移. 无需更改 Ghidra 脚本.

---

## 状态

**NEEDS_FIX (1 item)**

C12 (#1): B1 BL 目标函数名在 proposal prose 中错误 (set_lp_row_type6_with_value != set_lp_display_row_type5). 修正后所有 12 块分类和脚本计划均正确, 可执行落地.

**其余 12 项 (C1-C11, C13) 全部 PASS.**

**落地就绪性**: fixer 可同步修正提案文字并直接执行 Ghidra 脚本 DisassembleF09Seg4R.py (脚本计划本身完全正确); byte-identical 风险评估为无.

---

## Reviewer Verdict: F09-Seg4R = NEEDS_FIX(1 item)
