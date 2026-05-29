# Naming Evaluation: 080fbcac

> **版本**: v2 (2026-05-29 12:00)
> **状态**: PASSED
> **proposal**: doc/dev/eval/080fbcac.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 5/5 | `render_starter_deck_cursor_oam_pair` — 全小写下划线，动词首词，无禁词 | — |
| R2 | plate WHY | 5/5 | 含调用方上下文/触发（步分发链）/副作用（OAM 写）；路径描述主/备路径清晰；无推测词 | — |
| R3 | 参数语义 | 5/5 | void 入口覆盖确认，返回 void Pattern B | — |
| R4 | 返回值 | 5/5 | Pattern B void 正确标注 | — |
| R5 | 副作用 | 5/5 | OAM 写（8 主路径/4 备用路径）通过 write_oam_entry_from_packed_args；目标含义说明 | — |
| R6 | 魔数符号化 | 5/5 | Constants 块存在，含 CURSOR_STATE_ADDR=0x020297e4、X_BASE_OFFSCREEN=0x80<<2=0x200 (0x80*4=0x200 正确)、X_PLAYER_OFFSET=0x40、Y_STEP=0x20、Y_ALT_BASE=0x38、Y_OAM_STEP_PACKED=0x80<<0xb=0x40000 (0x80*0x800=0x40000 正确)；无占位符 | — |
| R7 | caller 锚定 | 5/5 | form(c) Sub-type A：CALLEE-COLUMN GREP + grep ".word 0x080fbcad" => 0 hits | — |
| R8 | 置信度 | 5/5 | med + 独立升级路径节；L1 asm lines 434783-434857，L2 控制字段+双槽循环模式，L3 主/备路径结构；3 层有效 | — |
| R9 | 硬规则 | 5/5 | grep 全 0 | — |

**总分: 45/45**

## 修改清单

无

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-29 | 40/45 | NEEDS_FIX | 初评：R6 无 Constants 块 |
| v2 | 2026-05-29 | 45/45 | PASSED | R6 补 Constants 块 (6 项，shift 算术验证正确) |
