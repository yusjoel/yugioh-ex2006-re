# Refine Review: F09-Seg-8

Proposal: `doc/dev/refine/F09-Seg-8.proposal.md`
Range: `[0x0807629c, 0x0807738c)`
Reviewer: independent (no proposal conclusions trusted without re-verification)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | OK | Seg-8 [0x7629c, 0x7738c) 与 p5-refine-09 §五 roadmap 完全一致; 未跳号/回头 |
| C2 Rule2 | 每个 ROM_INCBIN 块有归宿 | OK | 独立扫描 asm/09 line 16873..18893 共 4 个 ROM_INCBIN; 全部标 disasm; 无静默保留 |
| C3 Rule3 | §5.1 块确 0 引用 | OK | §5.1=0; B1/B3 THUMB+1 确认: B1@0x9e41a68→0x080765b1, B3@0x9e41b28→0x080767ad; B2 raw@0x80765ec, B4 raw@0x80767f4; 全部非 0 引用 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 自读 40 个槽 (11+29); 全部匹配; 含 0xcc8/0x1531/0x16be/0x16e3/0x18ca/0x0807639c/0x08077150 |
| C5 R1 复用 | 新建前确无现有可复用 | OK | 5 NEW CID (0x1531/0x16be/0x16e3/0x18ca/0x1492) 及 0xcc8 在 constants/*.inc 全部 0 命中; 所有 REUSE 声明值确在 constants 中存在 |
| C6 R2 名 | 槽名合规, 无碰撞 | OK | 8 个 RENAME 槽名全部匹配 `^[a-z][a-z0-9_]+$`; 无重复 label |
| C7 R3 接通 | REF=0 合理 | OK | 所有全局地址值 (gP1LifePoints/gDuelPhaseFlags/gDuelFieldSlots/gP1HandSlotArray 等) 均有现成 equate; 无需新建 USER-label+DATA-ref |
| C8 R5 现名 | 无残留 stale FUN_ | OK | Seg-8 range (line 16873..18893) grep `FUN_[0-9a-f]{8}` = 0 命中; line 12436 处 FUN_ 在 Seg-6 (已落地) |
| C9 ASCII | plate/EOL 纯 ASCII | OK | Seg-8 asm 行内 0 个 non-ASCII 字符; PLATE=0 声明正确 |
| C10 carve | 指针表 THUMB+1 核对 | OK | check_equip_slot_eligible_by_type_query+1=0x080507ad (奇数/THUMB+1 OK); check_equip_slot_eligible_by_side_match+1=0x08053f11 (奇数/THUMB+1 OK); switchD table ptr=0x08077150 (even raw table addr OK) |
| C11 误名 | 函数名无矛盾 | OK | FUNC_RENAME=0; dispatch_equip_effect_node_by_opcode 含 29-entry switchD (案例 0x64..0x80, 符合名); 其余函数名与函数体一致 |
| C12 R6 | 关键槽有 file:line + 置信度 | OK (1 minor) | 5 关键槽均有 file:line 证据; MINOR: DWORD_080769d4 (0xcc8) R6 prose 称"extracts bits[23:22]"但实际是 ldrh + lsls#19+lsrs#19 提取 bits[12:0] (13-bit CID field); 名称 HAND_SPELL_SLOT_CC8_OFF 为中性偏移名, 无红线 |
| C13 残留 | 段内全部残留槽 100% 覆盖 | OK | 独立清点 = 76 槽 (8a:27 + 8b:49); 分类: 63 REUSE + 5 NEW + 8 RENAME = 76; 与穷举吻合; 无遗漏无重计 |

---

## switchD 独立验证

**switchD_0807638c** (在 tick_equip_zone_bitmap_display_seq 内):
- ASM line 17015 起: `switchD_0807638c__switchD` (.hword 0x4687) 存在
- switchdataD_0807639c (6-entry table at 0x7639c..0x763b3) 存在
- Case 标签: caseD_1 (line 17031), caseD_3 (line 17042), caseD_6 (line 17053), default (line 17098)
- 所有 6 个 table 目标 (0x763b4 x2, 0x763cc x3, 0x763e0 x1) 均在 [0x7629c, 0x7738c) 内且已 disasm
- **结论: 已全部解码, 无需额外操作. CORRECT.**

**switchD_08077144** (在 dispatch_equip_effect_node_by_opcode 内):
- ASM line 18598 起: `switchD_08077144__switchD` (.hword 0x4687) 存在
- switchdataD_08077150 (29-entry table at 0x77150..0x771c3) 存在
- Case 标签: caseD_80/7f/7e/78/77/64/65 全部存在
- 所有 29 个 table 目标均在 [0x7629c, 0x7738c) 内 (python 验证)
- **结论: 已全部解码, 无需额外操作. CORRECT.**

---

## ref-scan 独立复核

| 块 | 搜索地址 | raw | THUMB+1 | 判定 |
|----|---------|-----|---------|------|
| B1 0x765b0/0x2c | 0x080765b0 / 0x080765b1 | 0 | 1 (GBA:0x9e41a68) | disasm (fn_eligible stub) CONFIRMED |
| B2 0x765f0/0x19c | 0x080765f0 / 0x080765f1 | 1 (GBA:0x80765ec) | 0 | disasm (sub-stubs) CONFIRMED |
| B3 0x767aa/0x32 | 0x080767ac / 0x080767ad | 0 | 1 (GBA:0x9e41b28) | disasm (fn_eligible stub) CONFIRMED |
| B4 0x767f8/0x110 | 0x080767f8 / 0x080767f9 | 1 (GBA:0x80767f4) | 0 | disasm (sub-stubs) CONFIRMED |

注: B3 incbin 起始 0x767aa 有 2B 零填充; fn_eligible 实从 0x767ac 开始 (ROM byte=0xf0b5 = push {r4-r7,lr}); FS handler table 引用 0x080767ad = fn_eligible+1 (THUMB+1). Proposal 表述正确.

B1 CID 验证: FS entry base = 0x1e41a5c, +0x8 halfword = 0x169e = MUSTERING_DARK_SCORPIONS_CID (REUSE). CORRECT.
B3 CID 验证: FS entry base = 0x1e41b1c, +0x8 halfword = 0x16a6 = SPELL_VANISHING_CID (REUSE). CORRECT.

B2/B4 dispatch table 目标验证: 所有 raw 指针均在对应 incbin 范围内; 全部为偶数地址 (raw code, 非 THUMB+1). CORRECT.

---

## 额外发现 (不阻断 PASS)

**EQ_SLOTS 表头内部不一致**: 提案 EQ_SLOTS 小节表头写 "62 REUSE + 7 NEW = 69 total equate slots", 但正文 + C13 重新清点为 63 REUSE + 5 NEW = 68 EQ slots, 加 8 RENAME = 76 总计. Summary 行写 EQ=68 是正确的. 表头数字仅为文档内部错误, 不影响 fixer 执行 (分类表体正确).

**DEAL_OF_PHANTOM_CID (0x1492)**: 提案将其加入 card_info.inc 作为纯文档常量 (无 literal pool slot). 实际 0x1492 在运行时由 BARK_OF_DARK_RULER_CID(0x14be)-0x2c 计算得出, 无 .word 槽可替换. 添加文档常量可接受 (沿用 file 06..08 有先例).

**R6 prose 小误**: DWORD_080769d4 (0xcc8) 的消费者描述称"reads bits[23:22] of the word", 实际机器码为 ldrh (16-bit load) + lsls#19 + lsrs#19 = 提取 bits[12:0] (13-bit card-id/set_code field). 名称 HAND_SPELL_SLOT_CC8_OFF 为中性偏移名, 不过度声称语义, 可接受.

**0xcc8 引用数验证**: 提案称 9 raw ROM refs. 实际 `rom.count(pack('<I', 0xcc8))` = 9. 早期 2-byte stride 扫描漏掉奇数对齐实例. 提案数字正确.

---

## 状态: PASS

所有 C1-C13 均通过. 无 §5.1 孤儿漏登记. 无 Rule 2/3 违规. 两个 switchD 确认已全解码. 4 个 ROM_INCBIN 块 ref-scan 独立复核匹配 proposal. C4 40 个 ROM 字节验证全通. C5 6 个 NEW 值全部 0 命中. C8/C9 clean.

额外发现均为非阻断性 (内部计数文档错误 / 中性名称 / prose 小误); 不要求修改提案.

Fixer 可直接进入模式 B 落地.

---

## Reviewer Verdict: F09-Seg-8 = PASS
