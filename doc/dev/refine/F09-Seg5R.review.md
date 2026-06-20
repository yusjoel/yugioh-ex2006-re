# Refine Review: F09-Seg5R

**Proposal**: `doc/dev/refine/F09-Seg5R.proposal.md`
**Scope**: file 09 Seg-5 REMEDIATION [0x08072d20, 0x08074338)
**Reviewer**: independent (refine-reviewer)
**Date**: 2026-06-20

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与路线图一致 | PASS | Seg-5 [0x72d20, 0x74338) 与 §四 进度表 Seg-5a/5b 一致; 前置 Seg-1/4 已落地 |
| C2 | 所有 ROM_INCBIN/.byte 块都有归宿 | PASS | 2 ROM_INCBIN + 7 .byte CODE + 3 .byte DATA = 12 块全部覆盖; grep asm/09 确认 Seg-5 范围内仅 2 个 ROM_INCBIN (0x73218, 0x73636) 和恰好 10 个 .byte 行 |
| C3 | §5.1 块确 0 引用 | PASS | 无 §5.1 块。所有 CODE 块均有显式 intra-function 分支跳转。A2 (0x7326c) raw=1 来自 dispatch table 是预期行为 (dispatch 表指向它) |
| C4 | EQ value == ROM 4 字节小端 | PASS | pool_b4_368c @ 0x7368c: ROM bytes = 1d 01 00 00 -> 0x0000011d. CARD_DISPLAY_OP31_LP_BAR_SUB=0x011d. 匹配 |
| C5 | 新建 constants 前无现有可复用 | PASS | 唯一 EQ 为 REUSE: card_info.inc:1496 已有 `.equ CARD_DISPLAY_OP31_LP_BAR_SUB, 0x0000011d`. 无新常量 |
| C6 | 槽名规范, 无碰撞 | PASS | pool_b4_368c 标签保持不变 (不重命名为 equate 名, 遵循 Seg-4R lesson) |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 3 个 DATA createDWord 槽目标 (trap_dustshoot_sub_3290 / machine_dup_sub_374c / cat_ill_omen_sub_3a46) 均为现有 asm 标签 (行 10871/11466/11827 确认) |
| C8 | plate 引用全用现名, 无残留 FUN_ | PASS | PLATE=none; 无 plate 变更; 段内无新 stale FUN_ 引入 |
| C9 | plate/EOL 文本纯 ASCII | PASS | 提案无 PLATE/EOL 章节。createEquate 字符串 'CARD_DISPLAY_OP31_LP_BAR_SUB' 纯 ASCII。提案 .md 内 U+00A7 (§) 和 U+2713 (checkmark) 属文档注释, 非 Ghidra 输出 |
| C10 | 指针表条目 `.word <fn>+1` 核对 | PASS | 3 个 DATA 指针均为偶数 (raw code addr, 无+1): 0x08073290/0x0807374c/0x08073a46. 符合 raw dispatch table 惯例 (MOV PC,r0 / bx 调用, 不经 THUMB+1) |
| C11 | 误名已标 FUNC_RENAME | PASS | 无函数改名; 所有含块函数在前序 Seg-5a/5b pass 中已正确命名 |
| C12 | 关键槽有 file:line + 置信度证据 | PASS | EQ REUSE card_info.inc:1496; BL 目标均有 file+asm 引用 (conf: high 6 callee); consumer evidence 节完整 |
| C13 | 段内所有残留自动名槽全覆盖 | PASS | Seg-5 [0x72d20, 0x74338): ROM_INCBIN 仅 2 块 (0x73218/0x12, 0x73636/0x56), .byte 仅 10 行. 提案处理 12 块. 下一个 ROM_INCBIN 为 0x768dc (Seg-8 范围外). 落地后残留 = 0 |

---

## 独立复核证据

### Ref-scan 结果 (独立重跑)

对所有 9 个 CODE 块入口穷举 2B-step ref-scan (raw + THUMB+1), 结果:

| 块 | raw | THUMB+1 | 判定 |
|---|---|---|---|
| A1 0x08073156 | 0 | 0 | CODE OK |
| B1 0x08073218 | 0 | 0 | CODE OK |
| A2 0x0807326c | 1 | 0 | CODE OK (raw hit from dispatch table @ 0x8073170 = 预期) |
| A3 0x0807359e | 0 | 0 | CODE OK |
| B2 0x08073636 | 0 | 0 | CODE OK |
| A4 0x08073732 | 0 | 0 | CODE OK |
| A5 0x0807387a | 0 | 0 | CODE OK |
| A6 0x08073922 | 0 | 0 | CODE OK |
| A7 0x08073d30 | 0 | 0 | CODE OK |

A2 (0x0807326c) raw=1: hit 在 0x8073170 = dispatch table 第 3 项 (entry[2]), 提案所述。这是 computed-indirect jump (MOV PC,r0) 经 raw 指针到达的 sub-stub 入口, 非 FS fn-ptr THUMB+1。判定 CODE-disasm 正确。

### THUMB+1 coincidence @ 0x08073660 (in B2 block)

独立核实: 命中在 ROM offset 0x66dd88 (GBA: 0x0866dd88)。

- 4-byte 对齐: 是
- 周围 +-8 字节内 GBA-range 值: 仅 1 个 (0x08073661 本身), 前后各 4B 均非指针 (0x860f080a / 0x3a58f596)
- 整个 +-0x40 窗口: 仅 3 个 GBA-range 值, 分布稀疏, 非结构化指针表
- 该区域为 ROM 后半段压缩资产流 (0x0866ddXX, 字节序非 THUMB 代码, 非 FS 效果 handler table 范围)
- 卡效果 handler table 在 0x09e3xxxx/0x09e4xxxx (ref: 项目惯例), 0x0866XXXX 非此范围
- 结论: **压缩数据位碰撞, 非真实 fn-ptr 引用**。B2 分类 CODE-disasm 正确

### ROM 字节核对

| 项 | 地址 | 独立读取 | 提案值 | 一致 |
|---|---|---|---|---|
| pool_b4_368c EQ | 0x7368c | 0x0000011d | 0x0000011d | YES |
| DATA 0x73168 | 0x73168 | 0x08073290 (raw) | trap_dustshoot_sub_3290 | YES |
| DATA 0x735b4 | 0x735b4 | 0x0807374c (raw) | machine_dup_sub_374c | YES |
| DATA 0x7388c | 0x7388c | 0x08073a46 (raw) | cat_ill_omen_sub_3a46 | YES |

### 分支指令目标核对 (所有 9 个触发分支)

| 分支 @ | hw | 独立计算目标 | 提案声称 | 一致 |
|---|---|---|---|---|
| bls @ 0x73152 | 0xd900 | 0x08073156 | LAB_08073156 | YES |
| bne @ 0x7320a | 0xd105 | 0x08073218 | LAB_08073218 | YES |
| bls @ 0x7359a | 0xd900 | 0x0807359e | LAB_0807359e | YES |
| bne @ 0x73632 | 0xd100 | 0x08073636 | LAB_08073636 | YES |
| bcs @ 0x7370a | 0xd212 | 0x08073732 | LAB_08073732 | YES |
| bls @ 0x73876 | 0xd900 | 0x0807387a | LAB_0807387a | YES |
| bne @ 0x73910 | 0xd107 | 0x08073922 | LAB_08073922 | YES |
| beq @ 0x73cb8 | 0xd03a | 0x08073d30 | LAB_08073d30 | YES |
| beq @ 0x73cc2 | 0xd035 | 0x08073d30 | LAB_08073d30 | YES |

### BL 目标核对

| BL @ | 独立计算 | 提案 | 一致 |
|---|---|---|---|
| 0x73222 | 0x080a1c2c | set_lp_display_row_type5 | YES |
| 0x73640 | 0x0808dab0 | dispatch_effect_handler_by_card_id | YES |
| 0x73654 | 0x08093390 | trigger_card_display_op31_if_not_active | YES |
| 0x73664 | 0x080335b8 | count_available_monster_slots | YES |
| 0x73676 | 0x080335b8 | count_available_monster_slots | YES |
| 0x73684 | 0x08093390 | trigger_card_display_op31_if_not_active | YES |
| 0x73732 | 0x0804a870 | decrement_lp_bar_display_counter | YES |
| 0x7392a | 0x08093390 | trigger_card_display_op31_if_not_active | YES |
| 0x73d36 | 0x080495fc | enqueue_equip_zone_sprite_attr_full | YES |

### pc-relative pool loads 核对

| ldr @ | 提案 PC 计算 | 独立 load_addr | 加载值 |
|---|---|---|---|
| ldr r1,[pc,#8] @ 0x73682 | PC=0x73684, addr=0x7368c | 0x7368c | 0x0000011d (CARD_DISPLAY_OP31_LP_BAR_SUB) |
| ldr r1,[pc,#12] @ 0x735a0 | PC=0x735a4, addr=0x735b0 | 0x735b0 | 0x080735b4 (machine_dup dispatch table) |
| pool_b3_35b0 @ 0x735b0 | 0x080735b4 (dispatch table base) | confirmed | YES |

---

## 提案注释偏差 (非功能性)

以下几处提案注释描述不精确, 但均为注释错误, 不影响字节正确性或 Ghidra disasm 行为:

1. **B1 b @ 0x73228**: 实际目标 0x080732a2 (pop epilogue), 提案注释写 "trap_dustshoot_default_32a0 @ 0x080732a0". 0x732a0 = `movs r0,#0`; b 跳至 0x732a2 = `pop {r4,r5,r6,r7}` 以保留 r0=0x7f 返回码. Ghidra 将生成 LAB_080732a2 标签; bytes 正确.

2. **B2 b @ 0x7365a / 0x7368a 及 A4 b @ 0x73738**: 实际目标均为 0x08073758 (pop), 提案注释写 "machine_dup_default_3756=0x8073756". 0x73756 = `movs r0,#0` (label 本身); b 跳至 0x73758 以保留各自的返回码 (0x6e / 0x7e / 0x64). 同上模式, bytes 正确.

3. **A6 b @ 0x73930**: 实际目标 0x08073a56, 提案写 "cat_ill_omen_default_3a54=0x8073a54". 同上模式.

4. **A7 b @ 0x73d3c**: 实际目标 0x08073d76, 提案写 "LAB_08073d74". 同上模式.

5. **A7 "7 halfwords decoded"** = 14 bytes 正确; 但同时写 "7 instructions": BL = 2 halfwords = 1 instruction, 故实际指令数为 6. 纯术语偏差.

以上均为只读事实: ROM bytes 固定, Ghidra 的 DisassembleCommand 将从 ROM 字节中正确读取分支偏移并生成正确的 LAB_ 标签, 不依赖提案注释中的目标地址名称.

---

## byte-identity 安全性

- clearListing(0x08073636, 0x0807368c): 终止于 0x7368b, **不覆盖** pool_b4_368c @ 0x7368c. 安全.
- 所有 DisassembleCommand 目标均为纯 THUMB 2B/4B 指令; b/bl 编码来自 ROM, Ghidra 重导出后 GAS 重新汇编产生相同字节.
- DATA createDWord 在 CODE DisassembleCommand 之前执行, 防止 Ghidra 将 dispatch table entry[0] 误当 code.
- A2 (0x7326c): DC 从入口 2 halfwords 起将 fall-through 到 0x73270 的已解码体, 止于 b @ 0x7327e (目标 0x080732a2, 外部已解码). 无重复 clear 风险.
- B2 的双边 bne: Ghidra 追踪 NOT-taken (0x7364c..0x7365a -> b stops) 和 taken (0x7365c..0x7368a -> b stops) 均正确终止. 无 inline pool 在 clearListing 范围内 (pool_b4_368c @ 0x7368c 恰好排除在外).

---

## 状态: PASS

所有 12 块分类正确, ref-scan 独立核实, ROM 字节逐项核对, 分支目标完全计算匹配, EQ REUSE 确认, DATA 指针奇偶性正确, clearListing 范围安全, 提案无 §5.1 误用, C13 post-state = 0 ROM_INCBIN + 0 .byte-code 残留.

提案中的注释偏差 (b 目标地址名称 +2 偏移) 不构成功能问题, 不需要 fixer 修正.

## 修改清单 (NEEDS_FIX)

无. PASS.

---

## Reviewer Verdict: F09-Seg5R = PASS
