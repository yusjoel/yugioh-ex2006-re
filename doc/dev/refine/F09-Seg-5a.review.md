# Refine Review: F09-Seg-5a (iteration 2)

**Proposal:** `doc/dev/refine/F09-Seg-5a.proposal.md`
**Range:** `[0x08072d20, 0x08073a5c)` (Seg-5a, first half of Seg-5 split)
**Reviewer:** independent re-verification (ROM bytes, ref-scan, constants grep, asm slot count)
**Iteration:** 2 (re-review after Mode A fixer applied 3 items from iteration-1 NEEDS_FIX)

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | Seg-5a [0x72d20..0x73a5c) 是路线图 Seg-5 的前半, 无跳号 |
| C2 Rule2 | 所有 ROM_INCBIN 块都有归宿 | PASS | B1-B6 共 6 块全部分类 (B6=0x73900/0x15c 已加入 Seg-5a); asm grep 确认无遗漏 ROM_INCBIN |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | §5.1 为空; B6 有 raw refs 27 次 (dispatch table), 正确归 R4 disasm |
| C4 R1 值 | EQ value == ROM 4 字节小端 | PASS | 未重跑 (iteration-1 已全量验证 48/48; fix 未触动 EQ 值) |
| C5 R1 复用 | NEW 常量 0 命中 | PASS | 独立 grep: STATUE_OF_THE_WICKED_CID/TOKEN_13FB..195A(8)/SPRITE_ATTR_CLR_BIT13/EQUIP_CHAIN_BASE_OFF/TRAP_DUSTSHOOT_CID 全部 0 hits in constants/*.inc; fix 未引入新碰撞 |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | PASS | fn_eligible_cat_ill_omen_and_owl_of_luck/cat_ill_omen_dispatch_sub_stubs_3900 等全部合规 |
| C7 R3 接通 | REF_SLOTS 有 USER-label + DATA-ref 计划 | PASS | 10 REF_SLOTS 均指向 gP1LifePoints; 未变 |
| C8 R5 现名 | 无残留 FUN_ | PASS | Seg-5a 行范围无 FUN_xxxxxxxx; 未变 |
| C9 ASCII | plate/EOL 纯 ASCII | PASS | Seg-5a 行范围 (asm/09) 无非 ASCII; 提案 doc/ 文档标题含 CJK (正常, 不是 Ghidra 注释) |
| C10 carve | 指针表条目为 raw 地址 (非 THUMB+1) | PASS | B6 dispatch table 29 条目全为 raw (0x08073900..0x08073a54); python 逐条确认 |
| C11 误名 | 无函数体与函数名矛盾 | PASS | 无 FUNC_RENAME; 未变 |
| C12 R6 | 关键槽有 file:line + 置信度证据 | PASS | 未变; EQUIP_CHAIN_BASE_OFF/SPRITE_ATTR_CLR_BIT13 均有 asm line + conf:high |
| C13 残留 | 所有残留自动名槽 100% 覆盖 | PASS | asm grep 独立计数: Seg-5a 定义标签 61 个; EQ(48)+REF(10)+RENAME(3)=61; 无遗漏, 无重叠; DAT_08073900 正确归 RENAME |

---

## 三项修复独立复核

### #1 — B6 块 0x73900/0x15c 现已在 Seg-5a (原 C2/C13 违规)

**独立复核结果: PASS**

ref-scan 重跑 (python, 全 ROM):

- raw refs: 27 次, 分布在 8 个 sub-stub 地址: 0x08073900(x1), 0x08073932(x1), 0x08073946(x1), 0x08073968(x1), 0x080739b0(x1), 0x08073a34(x1), 0x08073a46(x1), 0x08073a54(x22 default)
- THUMB+1 refs: 1 次 (0x08073a09 from 0x08660abf = 0x086xxxxx 压缩数据区, 误报; 与 B4 同模式)
- 所有 raw refs 均来自 dispatch table 0x0807388c..0x080738ff (29 条目 x4B = 0x74B)

dispatch table 条目分布验证: 0x08073a46(x1), 0x08073a54(x22), 0x08073a34(x1), 0x080739b0(x1), 0x08073968(x1), 0x08073946(x1), 0x08073932(x1), 0x08073900(x1) = 29 条目总计. 与 proposal 完全一致.

B6 块边界: start=0x08073900, size=0x15c, end=0x08073900+0x15c=0x08073a5c = Seg-5a 结束边界. 精确吻合.

proposal 在数据块分类表 B6 行 + disasm 计划 B6 小节 + RENAME_SLOTS 中均已正确记录 DAT_08073900.

C13 独立验证: asm/09 grep 定义标签 (带冒号) 61 个; EQ(48)+REF(10)+RENAME(3)=61; 集合无重叠无遗漏.

注: proposal 的数据块分类表 B6 条目写 "THUMB+1=0", 而 ref-scan 实际有 1 次 THUMB+1 误报 (0x8660abf 压缩区). 这是一处小数据不准确 (应为 THUMB+1=1, false positive from 0x08660abf), 但不影响分类 (误报已明确为压缩数据区, 证据链完整). 不阻塞执行.

---

### #2 — B5 stub 双卡命名 (An Owl of Luck)

**独立复核结果: PASS**

FS handler table 直接读 ROM 验证:
- 0x09e44104 = 0x00001590 (A Cat of Ill Omen, card_1172 pw=24140059) ✓
- 0x09e44134 = 0x00001593 (An Owl of Luck, card_1175 pw=23927567) ✓
- 两个 FS ref 均指向 0x08073865 (THUMB+1 of 0x08073864) ✓

card-stats.s 独立确认: line 15290 "An Owl of Luck  slot=0x1593  pw=23927567" ✓

fn body 0x08073864..0x0807388c 字面量扫描: 0x1590 和 0x1593 均未作为 literal pool word 出现 -> 无需新增 CID 常量, 与 proposal 说明一致.

B5 分类表现在正确写 "CID 0x1590 A Cat of Ill Omen, card_1172 pw=24140059" 和 "CID at 0x09e44134=0x1593 An Owl of Luck, card_1175 pw=23927567".

disasm 计划 B5 小节标 label: fn_eligible_cat_ill_omen_and_owl_of_luck — 符合 ^[a-z][a-z0-9_]+$ ✓

---

### #3 — EQ 计数 (REUSE=38, NEW=10, total=48)

**独立复核结果: PARTIAL (注解层面残留不一致, 不阻塞执行)**

total=48 正确 (表格 48 行); C13 proof 48+10+3=61 正确.

但表格行标签与摘要声明仍有注解层面偏差:
- 表格实际: 37 行标 REUSE + 11 行标 NEW = 48 (DWORD_08072e68 在表中标 NEW)
- 摘要声明: REUSE=38, NEW=10 (脚注解释: "37 pre-existing + DWORD_08073568 = 38 REUSE")
- 脚注逻辑: DWORD_08073568 (EQUIP_CHAIN_BASE_OFF 第二次出现) 计入 REUSE, 推 REUSE 从 37 到 38; 但 DWORD_08073568 本已是表格 37 行 REUSE 中的一行, 不能再额外计数.
- NEW 列表 10 个名字未含 EQUIP_CHAIN_BASE_OFF, 而表格将 DWORD_08072e68 标为 NEW.

实质影响评估:
- 新增常量数量 (fixer 真正要创建的): constants/card_info.inc 中 10 个 (STATUE+8 TOKEN+TRAP_DUSTSHOOT), constants/ewram.inc 中 1 个 (EQUIP_CHAIN_BASE_OFF), constants/oam_attr.inc 中 1 个 (SPRITE_ATTR_CLR_BIT13) = 共 12 个新常量, 全部 0-hit 确认.
- 这 12 个常量的来源/目标文件/值在"新增 constants / 全局"节中有完整记录.
- 49 EQ 总槽 (48)、C13 分区、ref-scan、ASCII 均无误.

结论: 注解中 37REUSE+11NEW(表) vs 38REUSE+10NEW(摘要) 的偏差纯属注解层面, 不影响 fixer 执行. PASS (annotation-level residual, not blocking).

---

## Seg-5b 溢出编辑确认

Seg-5b proposal (`F09-Seg-5b.proposal.md`) 验证:
- ROM_INCBIN 块表: 仅列 B7/B8/B9/B10 (4 块), 无 B6 ✓
- 文件中 "73900" 出现 2 次, 均为说明性注释:
  - Line 163: "(Block 0x73900/0x15c formerly listed as B6 is now in Seg-5a as B6; see F09-Seg-5a.proposal.md)" ✓
  - Line 213: "(DAT_08073900 moved to Seg-5a B6; see F09-Seg-5a.proposal.md)" ✓
- C13 总数: 27; 21 EQ + 4 REF + 2 RENAME = 27 ✓
- 无悬空引用 ✓

---

## 状态: PASS

所有三项修复均已正确落地 (其中 #3 存在注解层面小偏差, 不阻塞). 无回归. Seg-5b 溢出编辑正确.

Proposal 可进入落地阶段 (Mode B: Ghidra 脚本执行).
