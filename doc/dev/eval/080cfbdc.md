# Naming Evaluation: 0x080cfbdc

> **版本**: v1 (2026-05-10 10:00)
> **状态**: PASSED
> **proposal**: doc/dev/eval/080cfbdc.proposal.md

## P0 检查

- proposal 存在: OK
- 零容忍词 grep: 0 命中
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `render_card_list_oam_row_by_stat_state`: 全小写, verb=render, qualifier=by_stat_state; 无 ARM 助记符冲突 | — |
| R2 | plate WHY | 5/5 | 含 caller (FUN_080c82e4 indeg=1), 触发条件 (gFontState[0x0a18] state_val 四路分派 + gPrng bit flags), 副作用 (OAM x4 + gFontState 字段写 + LP 写) | — |
| R3 | 参数语义 | 5/5 | r0 void; 入口 `.hword 0x4647` 分析: proposal 解释为 callee-save 保存 r8 via r7 的惯用 THUMB 模式 (`mov r7,r8; push {r7}` 将 r8 存栈), 结论合理; 后续 `ldr r2, DAT` 内部加载确认无 APCS 输入 | — |
| R4 | 返回值 | 5/5 | void, 函数无独立 movs r0,#N 赋值路径 | — |
| R5 | 副作用 | 5/5 | write_oam_entry_from_packed_args x4 (state=0 strip 循环) + [gFontState+0x0a0e] nibble 更新 + [gFontState+0x0a18] bits 更新 + [gP1LifePoints+0x148] LP 写入 + sync_state_and_init_sprite 调用; 含地址和写入含义 | — |
| R6 | 魔数符号化 | 5/5 | gPrng_BIT_NEXT_FWD=0x10, gPrng_BIT_NEXT_BWD=0x20, gPrng_BIT_WRAP_BWD=0xc0, gPrng_BIT_LP_WRITE=0x01, WRAP_MODULO=20, ATTR0_STRIP=0x32, OAM_SLOT=0x60, gPrng_FIELD_OFFSET=0x148 全部命名 | — |
| R7 | caller 锚定 | 5/5 | caller addr 0x080c82e4, tags 详尽 (17 个), role: card display master tick | — |
| R8 | 置信度 | 5/5 | high: 5 层证据 (tag + callee 集合 + IO 状态字 + sibling 对称 + caller); 无 med/low 节 (high 函数不需要) | — |
| R9 | 硬规则 | 5/5 | 零容忍词 0; 无禁用符号 | — |

**总分: 45/45**

## 修改清单

无

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-10 10:00 | 45/45 | PASSED | 初评 |
