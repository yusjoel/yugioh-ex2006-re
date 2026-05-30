# Naming Evaluation: 0x080ffbec

> **版本**: v1 (2026-05-31 00:00)
> **状态**: PASSED
> **proposal**: doc/dev/eval/080ffbec.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `update_card_list_scroll_position` — 全小写下划线; 首词动词 update; 无禁词; 无助记符冲突 | — |
| R2 | plate WHY | 5/5 | 中文 plate 含调用方 (indeg=0, fn-ptr 表入口) + 触发 (compute_card_list_scroll_position + display_mode 分支 + link 模式检查) + 副作用 (通过 update_deck_slot_card_entry 写 EWRAM); 三项齐全; 含具体地址/常数 0x0202f3c0/0x100/0x50 | — |
| R3 | 参数签名 | 5/5 | r0 unused; 返回 s32 (0=无法滚动/早退, 1=正常完成; Sub-case E; 两路径含义明确) | — |
| R4 | 返回值 | 5/5 | s32 (0=无法滚动/早退 movs r0,#0, 1=正常完成 movs r0,#1; Sub-case E pop{r4,r5,r6,r7}; pop{r1}; bx r1); 两路径明确 | — |
| R5 | 副作用 | 5/5 | 通过 update_deck_slot_card_entry 写入 EWRAM 卡片列表状态; 已标注间接副作用来源 | — |
| R6 | 魔数符号化 | 5/5 | CARD_LIST_CTX/CANDIDATE_BUF/LINK_FLAG_OFF/DISPLAY_MODE_OFF/LINK_SCROLL_THRESHOLD/MODE1_THRESHOLD/MODE2_THRESHOLD/MODE3_THRESHOLD 均已命名 | — |
| R7 | caller 锚定 | 5/5 | indeg=0 (grep 独立验证: `,0x080ffbec` = 0 hits); `.word 0x080ffbed` → 0 hits; Sub-type A form(c) 正确 | — |
| R8 | 置信度 | 5/5 | high; L1 (asm 445354-445470) + L2 (CANDIDATE_BUF=0x0202f3c0 + LINK_FLAG_OFF=0x2) + L6 (命名 callee: compute_card_list_scroll_position, count_valid_cards_by_slot_type, update_deck_slot_card_entry) = 3 层 | — |
| R9 | 硬规则 | 5/5 | 零容忍词 grep 全 0; 无弯引号/全角符号/日文假名 | — |

**总分: 45/45**

## 修改清单

无

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-31 00:00 | 45/45 | PASSED | 初评通过 |
