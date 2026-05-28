# Naming Evaluation: 0x080bacfc

> **版本**: v1 (2026-05-29 00:00)
> **状态**: NEEDS_FIX
> **proposal**: doc/dev/eval/080bacfc.proposal.md

## P0 检查

- proposal 存在: ✅
- 零容忍词 grep: ✅ 0
- 结论: P0 通过

## 评分

| R | 主题 | 得分 | 证据 | 清单 |
|---|------|------|------|------|
| R1 | 命名形式 | 0/5 | `get_occupied_monster_zone_count` — 首词 `get` 语义与函数行为矛盾: R4 明确说函数固定返回 0 (movs r0,#0), 并不返回 count; "get" 暗示返回被查询的值, 实际返回固定 0; 命名误导调用者 | #1 |
| R2 | plate WHY | 5/5 | 含触发 (zone_ptr byte[2] bit0) + 副作用 (调用 count_occupied_monster_zones, 结果未用) + 返回固定 0 的说明; ASCII 标点; 字数 <500 | — |
| R3 | 参数语义 | 5/5 | r0: ptr zone_ptr 含类型+含义; 返回 u32 0 (fixed) 说明; 函数无其他参数 | — |
| R4 | 返回值 | 5/5 | `u32 0 (fixed, 调用后固定 movs r0,#0)` 明确说明固定值; Sub-case E 正确识别 | — |
| R5 | 副作用 | 5/5 | "无外部写入" 正确 — count_occupied_monster_zones 是纯读函数, 函数体无 str 指令 | — |
| R6 | 魔数符号化 | 5/5 | "无非平凡字面量" — 函数体仅 lsls/lsrs 和 bl, 无裸 hex 常量 | — |
| R7 | caller 锚定 | 5/5 | form(c): indeg=0, grep `.word 0x080bacfd` -> 0 hits, Sub-type A 结论完整 | — |
| R8 | 置信度 | 5/5 | high; L1 (asm 302536-302543, 5 条指令全静态) + L2 (count_occupied_monster_zones 已命名, 返回语义明确) + L6 (callee 在 naming-proposals.csv 已命名); 3 层独立正向证据 | — |
| R9 | 硬规则 | 5/5 | 零容忍词 grep 0; ASCII 标点; 无弯引号/全角/顿号 | — |

**总分: 40/45**

## 修改清单

### #1 — R1 (优先级: 高)
**位置**: proposal 提案节 `proposed_name`
**问题**: `get_occupied_monster_zone_count` 首词 `get` 语义错误 — 函数 R4 明确固定返回 0 (非 count 值); `get` 动词暗示返回被查询量, 此处返回值与函数名宣称的内容不符; 应改为准确反映"调用 count 函数但忽略返回值, 固定返回 0"的动词
**当前**: `get_occupied_monster_zone_count`
**应改为**: `invoke_count_occupied_monster_zones` (动词 invoke 准确描述"调用后忽略返回") 或 `call_count_occupied_monster_zones` — 须选用一个不暗示本函数自身返回 count 的动词前缀

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | 2026-05-29 | 40/45 | NEEDS_FIX | 初次评审: R1 get 动词与固定返回 0 矛盾 |
