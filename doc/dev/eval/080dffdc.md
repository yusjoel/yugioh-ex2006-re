# Naming Evaluation: 0x080dffdc

> **版本**: v2 (2026-06-03 10:00)
> **状态**: PASSED
> **proposal**: doc/dev/eval/0x080dffdc.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `tick_pack_card_select_overlay_scroll_step` 全小写下划线; `tick` 首词动词; `overlay_scroll_step` 名词修饰语; 无 ARM 助记符冲突 | — |
| R2 | plate WHY | 5/5 | 481 字 <= 500 硬限; 含 (1) dispatch_pack_card_select_substep + step-table 0x09e495f4 触发, (2) gPrng+0x148 bit0 + 帧计数递减归零机制, (3) 副作用 +0x1c0 bit3 / +0x30+0xe / +0x110/+0x112 | — |
| R3 | 参数语义 | 5/5 | r0: void 有入口 ldr r5,DAT 立即覆盖证据; 返回 r6 含义 [0=继续, 1=步骤完成] | — |
| R4 | 返回值 | 5/5 | r0 = u8 step_done [0=继续, 1=步骤完成]; 路径 adds r0,r6 明确 | — |
| R5 | 副作用 | 5/5 | [pack_ui_state+0x1c0] bit3 / [+0x30+0xe] 帧计数 / [+0x30+0x4..+0xc] 批量清零 / [+0x4] := 2 / [+0x110] := 5 / [+0x112] := 5 全部列出 | — |
| R6 | 魔数符号化 | 5/5 | OVERLAY_FLAG_BIT=0x8 / FRAME_COUNTER_OFFSET=0x30+0xe 在 Constants 块 | — |
| R7 | caller 锚定 | 5/5 | CALLEE-COLUMN GREP: `grep ,0x080dffdc temp/ghidra-funcs-callgraph.csv \| tr -d '\r' \| wc -l` = 0; Sub-type B: 经 ROM step-table 0x09e495f4 由 dispatch_pack_card_select_substep (0x080e0fb8) 间接分派; form(c) Sub-type B 合法 | — |
| R8 | 置信度 | 5/5 | high; L1 asm 行范围 382817-382893 + L2 IO/IWRAM pack_ui_state 多字段 + L6 sibling tick_pack_slot_cover_fadein 同表 = 3 独立正向层 | — |
| R9 | 硬规则 | 5/5 | grep `[^\x00-\x7F]` 无 CJK 标点; 零容忍词 0 | — |

**总分: 45/45**

## 修改清单

无

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-06-03 | 30/45 | NEEDS_FIX | 初始评审; R2 plate 超 500 字 + R7 indirect_table 误作直接 caller |
| v2 | 2026-06-03 | 45/45 | PASSED | R2 压缩至 481 字; R7 改 form(c) Sub-type B (callgraph indeg=0 验证) |
