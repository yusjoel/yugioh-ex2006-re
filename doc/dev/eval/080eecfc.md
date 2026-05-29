# Naming Evaluation: 0x080eecfc

> **版本**: v1 (2026-05-29 00:00)
> **状态**: NEEDS_FIX
> **proposal**: doc/dev/eval/080eecfc.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0 hits
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `get_game_text_ptr_by_str_type_c` — verb=get, object=game_text_ptr, qualifier=by_str_type_c; 全小写下划线 | — |
| R2 | plate WHY | 5/5 | 调用方 (indeg=0 form(c)), 触发 (string_id 参数 + ID_OFFSET_C 偏移), 副作用 (纯查询) 三项齐全; 含 ID_OFFSET_C=0x226 具体常量和 NULL_STR=0x09e4f348 | — |
| R3 | 参数语义 | 0/5 | r0: `u16 string_id [0..N]` — `[0..N]` 含标识符上界 N, 视同缺失; 须追踪 callsite 或函数体 cmp guard 给出具体整数 | #1 |
| R4 | 返回值 | 5/5 | `r0 = char* 指向对应语言游戏字符串的 ROM 指针` — 含义明确; r0==0 路径 (返回 NULL_STR 0x09e4f348) 在 plate 中已描述 | — |
| R5 | 副作用 | 5/5 | "无外部写" — 纯查询函数; 明确标注 | — |
| R6 | 魔数符号化 | 5/5 | ID_OFFSET_C=0x226/NULL_STR=0x09e4f348/gSettings_LANG 全部命名 | — |
| R7 | caller 锚定 | 5/5 | indeg=0 form(c): grep ".word 0x080eecfd" = 0 hits; Sub-type A 结论 | — |
| R8 | 置信度 | 5/5 | high; L3 (sibling get_game_text_ptr_by_str_type_b + get_game_text_ptr_by_lang_offset 结构对称 + asm line 注释锚) + L2 (game_str_pointer_table/game_str_ja 已命名 + ID_OFFSET_C=0x226 静态) + L1 (asm lines 405893-405936 ~44 行全静态) — 3 层 | — |
| R9 | 硬规则 | 5/5 | 零容忍词 grep 0; ASCII 标点; 无禁忌词 | — |

**总分: 40/45**

## 修改清单

### #1 — R3 (高优先级)
**位置**: `080eecfc.proposal.md` ## 参数签名节, r0 行
**问题**: `[0..N]` 含标识符 N 作为上界, 视同缺失; string_id 的有效范围可从 game_str_pointer_table 大小或 sibling 函数的 callsite cmp guard 推导
**当前**: `r0: u16 string_id - 字符串 ID [0..N] (0 返回空串)`
**应改为**: 追踪 callsite 或 game_str_id_to_row 函数体内 cmp guard 常量, 给出具体整数上界 (如 `[0..0x3ff]` 等); 若无明确上界则引用 sibling 函数的 callsite bit-width 约束

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-29 | 40/45 | NEEDS_FIX | 初始评审: R3 string_id 上界 [0..N] 含标识符 |
