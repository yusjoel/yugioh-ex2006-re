# Refine Review: F08-Seg-3

**Segment**: `0x08066448..0x08067160`  
**File**: `asm/08_equip_oam_neodaed.s` lines 4796-6506  
**Proposal**: `doc/dev/refine/F08-Seg-3.proposal.md`  
**Reviewer**: independent (自主复核, 不信 proposal 结论)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 路线图 Seg-3=0x66448..0x67160, proposal 完全一致; 前接 Seg-2 ✅ 末地址 |
| C2 Rule2 | 所有 ROM_INCBIN / .byte 块有归宿 | ✅ | 1 块 DAT_080668c0/0x1cc → R4 disasm; 无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | 本段无 §5.1 块; ROM_INCBIN 块有 8 个 raw 引用 → 正确判 R4 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | ✅ | 全部 51 个 EQ 槽逐一 python 核对无误 |
| C5 R1 复用 | NEW 常量按值 grep = 0 命中; REUSE 有效 | ✅ | 6 个 NEW (DE_SPELL/CYBER_STEIN/ICID_RESERVED_A/B/C/OAM_ATTR_P2_SPRITE) 全在 constants/*.inc 值 grep 0 命中; 21 个 reuse 均存在且值匹配 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | 64 个新标签全通 regex; 与现有 labels 无碰撞 |
| C7 R3 接通 | REF_SLOTS 有 USER-label + DATA-ref 计划 | ✅ | 4 个 REF 槽均有目标 label 计划 (gP1LifePoints x2 已存在, dispatch_equip_zone_by_effect_type_jump_table NEW, switchD_..._08066f0c 已存在) |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 FUN_ | ✅ | 段内仅 1 处 FUN_ (line 4987): FUN_08073428 + FUN_08074770; 两者现名经 grep asm/ 确认: apply_lp_delta_for_slot_by_series_code (09:9288) + dispatch_dragon_summon_or_lp_delta_by_slot_type (09:11076); proposal 列出并规划替换 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | proposal 文件 3 处非 ASCII 均为 § (U+00A7) 在 proposal 文档标题 (非 Ghidra 待写内容); proposal 明确标 "0 non-ASCII" |
| C10 carve | 指针表条目验证 | ⚠ | 见 NEEDS_FIX #1: ref-scan 报 4 个 raw 引用但实际 8 个; 表条目地址描述有误 |
| C11 误名 | 函数体全局 vs 函数名矛盾 | ✅ | 20 个函数名抽查无矛盾; proposal 无 FUNC_RENAME 正确 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | 9 个关键槽均有 asm 行号 + card-stats.s 坐实 + high 置信度; ICID_RESERVED 有 plate 明确描述 |
| C13 残留 | 段内所有残留自动名槽被覆盖 | ✅ | python 精确清点 56 个 (51 EQ + 4 REF + 1 DISASM); 全部在 [0x08066448, 0x08067160) 内; 无漏槽越界 |

---

## 状态: NEEDS_FIX(1 item)

---

## 修改清单

### #1 — C10/C3 — ref-scan 数量错误 + 跳转表条目地址描述错误

**问题**: proposal 的 ref-scan 表格称 "4 refs are raw" 并只列出 4 个地址
(0x080668c0 / 0x0806691c / 0x08066934 / 0x08066a58) 有 raw=1, 其余 "raw=0, THUMB=0"。
但自主重跑 ref-scan (python `rom.count(struct.pack('<I', a))`) 显示有 **8 个**地址各有 raw=1:
- 0x080668c0: raw=1 (entry[11] @ 0x080668bc)
- 0x0806691c: raw=1 (entry[10] @ 0x080668b8)
- 0x08066934: raw=1 (entry[9] @ 0x080668b4)
- 0x08066a58: raw=1 (entry[8] @ 0x080668b0)
- 0x08066a62: raw=1 (entry[3] @ 0x0806689c) ← proposal 漏报
- 0x08066a6e: raw=1 (entry[2] @ 0x08066898) ← proposal 漏报
- 0x08066a7a: raw=1 (entry[1] @ 0x08066894) ← proposal 漏报
- 0x08066a86: raw=1 (entry[0] @ 0x08066890) ← proposal 漏报

**连带错误**: proposal 在 "Active entry points" 表中对 state=0x75/76/77/78 的 "table entry at" 列出错:
- 声明 state=0x78 entry @ 0x080668ac, 实际 0x080668ac 存储 0x08066a8c (fall-through)
- 声明 state=0x77 entry @ 0x080668a8, 实际 0x080668a8 存储 0x08066a8c (fall-through)
- 声明 state=0x76 entry @ 0x080668a4, 实际 0x080668a4 存储 0x08066a8c (fall-through)
- 声明 state=0x75 entry @ 0x080668a0, 实际 0x080668a0 存储 0x08066a8c (fall-through)

**正确映射** (dispatch: index = state - 0x75, table base 0x08066890):
| state | index | entry addr | target |
|-------|-------|------------|--------|
| 0x75 | 0 | 0x08066890 | 0x08066a86 (stub_75) |
| 0x76 | 1 | 0x08066894 | 0x08066a7a (stub_76) |
| 0x77 | 2 | 0x08066898 | 0x08066a6e (stub_77) |
| 0x78 | 3 | 0x0806689c | 0x08066a62 (stub_78) |
| 0x79..0x7c | 4..7 | 0x080668a0..0x080668ac | 0x08066a8c (fall-through) |
| 0x7d | 8 | 0x080668b0 | 0x08066a58 (stub_7d) |
| 0x7e | 9 | 0x080668b4 | 0x08066934 (stub_7e) |
| 0x7f | 10 | 0x080668b8 | 0x0806691c (stub_7f) |
| 0x80 | 11 | 0x080668bc | 0x080668c0 (stub_80) |

**附带机器码错误**: proposal 在 stub_76 (0x08066a7a) 的机器码核中声称 `2100=movs r1,#0`, 实际 ROM 字节 28 1c = 0x1c28 = `adds r0,r5,#0`。proposal 将 0x08066a7c 处的 `2100` 误读为 0x08066a7a 的首指令 (off-by-2)。

**影响评估**: 这些错误均在 proposal 的**描述性文本**中, 不影响核心操作:
- 8 个 stub 的标签名和 state 编号均正确
- disasm 计划 (clearListing 0x080668c0..0x08066a8c → setTMode → 8 × DisassembleCommand) 正确
- R4 disasm 分类正确 (8 个 raw 引用, 0 个 THUMB+1)
- fall-through states (0x79..0x7c) 判定正确

**修改动作**: fixer 在 proposal 中更正 ref-scan 表 (4→8 个 raw refs) 及 state=0x75/76/77/78 的 table entry 地址, 更正 stub_76 机器码描述。disasm 操作计划本身无需改动。

---

## 附: 独立验证摘要

**EQ 值核对**: 用 python `struct.unpack_from('<I', rom, addr-0x08000000)` 逐一核对 51 个 EQ 槽, 全部与 proposal 一致。

**ref-scan 自主复核**: 对 ROM_INCBIN 块 [0x080668c0, 0x08066a8c) 内所有可能地址逐 byte 扫描 `rom.count(struct.pack('<I', a))`, 发现 8 个地址各有 raw=1 (均来自跳转表 0x08066890 的 12 个条目中的 8 个), 0 个 THUMB+1。spurious collision (0x08066a6b/6a, hit 在 0x08ead08e FS 压缩数据区) 已排除。

**C5 双向核**: 6 个 NEW 常量在全部 constants/*.inc 中按 `.equ` + 精确值 grep 均 0 命中; 21 个 reuse 常量均找到对应 `.equ` 且值匹配。card_info.inc/ewram.inc/oam_attr.inc 均通过。

**passcode 核对**: DE_SPELL pw=19159413 (card-stats.s:8764 card_0673 slot=0x12EB); CYBER_STEIN pw=69015963 (card-stats.s:4708 card_0361 slot=0x114A)。ICID 0x1051/0x162c/0x184c 均无 card-stats.s 条目 (reserved gaps)。

**C13 残留**: python 精确从 lines 4853-6497 提取 56 个 auto-name 定义; 逐一校验地址 [0x08066448, 0x08067160); 全部覆盖 (51 EQ + 4 REF + 1 DISASM = 56)。

**C8 stale FUN_**: 段内 grep 恰好 1 处 (line 4987); 两个 FUN_ 现名经 grep 确认无误。

**EQ count typo**: executor report 末尾写 "EQ=50" 但 EQ 表实际 51 条; 不影响正确性 (51+4+1=56=全量)。

---

## Reviewer Verdict: F08-Seg-3 = NEEDS_FIX(1 items)
