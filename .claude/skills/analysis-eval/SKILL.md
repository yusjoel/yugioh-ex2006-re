---
name: analysis-eval
description: Score a function naming proposal against the 9-criteria rubric (R1-R9, total 45) and write a complete doc/dev/eval/<ADDR>.md file with scores, evidence, and a mandatory executable fix list. Use when reviewing function naming proposals, or whenever the user says "评分 X 函数命名" / "review naming proposal X" / "看看这次命名质量". This skill encapsulates BOTH the rubric AND the eval doc format — they are inseparable.
---

# Analysis Evaluation Skill

本 skill 是函数命名质量评估的**单一权威**：评分规则、文档模板、修改清单可执行性校验全在这里。

调用者通常是 `analysis-reviewer` agent，但任何上下文都可以 `Skill(analysis-eval, "<ADDR>")` 复用。

## 输出位置

- 写入：`doc/dev/eval/<ADDR>.md` (覆盖)
- ADDR 格式: `0x08014470` (含 `0x` 前缀, 8 位小写 hex)

---

## 评分边界 (重要)

本 skill 只评 **命名质量** — 即 proposal 文件 (`doc/dev/eval/<ADDR>.proposal.md`) 是否值得被采纳。

**不评的事**:
- Ghidra 是否已 rename / plate comment 是否已写入
- `naming-proposals.csv` 是否同步
- asm/all.s 是否已重导
- ROM 是否 byte-identical

以上 4 项 (Ghidra 同步 + CSV 同步 + asm 重导 + byte-identical 验证) 是 **review PASSED 之后** 由 `analysis-fixer` 在「落地阶段」统一执行的机械动作。它们有自己的 pass/fail (尤其 byte-identical = 红线), 但**不计入 R1-R9 评分**。

理由: executor 不允许触碰 Ghidra (角色边界), 因此第一轮 review 时 Ghidra 必然未同步; 把这件事算进评分等于结构性扣分, 反复一轮没意义。

---

## 元规则 1: 豁免权唯一归属用户 (零容忍)

reviewer / executor / fixer **不得自行协商、申请、接受任何 R1-R9 规则的豁免**。包括但不限于:

- executor 写"// 此处豁免 R3 因为..."
- fixer 在清单项写"加豁免注释说明规避"
- reviewer 看到豁免说辞后打满分
- 任何形式的"特例声明"、"环境限制说明"、"这里确实没办法所以允许"

遇到认为规则不合理 / 无法执行 → **唯一动作是停下来求助用户**。用户可以:

- (a) 显式授权豁免 → **改本 skill** 添加豁免条款 + "用户授权 YYYY-MM-DD"
- (b) 拒绝豁免 → 提供新的命名思路
- (c) 承认规则有问题 → 改 skill 的规则本身

## 元规则 2: 零容忍词检测

eval 文档中出现以下任一词 → 评分作废, 必须重写:

| 词 | 为什么违规 |
|----|----------|
| 我认为 / 我觉得 | 评分基于证据不基于意见 |
| 似乎 / 大概 / 可能是 / 应该是 | 0 或 5 二值, 不接受模糊档 |
| 这次不适用 / 特例 / 暂时 | 元规则 1: 规则适用所有 scope |
| 还行 / 够用 / 凑合 | 不是评分语言 |
| [降级] / [跳过] / [待补全] (在代码或 proposal 中) | 自动扣对应 R 到 0 |

## 元规则 3: BLOCKED 是合法终态

遇到**语义硬阻塞** (例如函数行为需要 runtime mGBA / GDB 验证才能确认):

1. eval 文档顶部用红字标注 `⚠️ BLOCKED`
2. 登记 `SB-<ADDR>-N` 追踪号
3. 阻塞导致的扣分如实扣 0, **不硬凑满分**
4. 在"修改历史"段记录阻塞解除前置条件 (例如 "等 mGBA 跑到 deck-edit page 状态 5 后 dump VRAM 验证")

BLOCKED 与"豁免"区别: 豁免是想绕过规则, BLOCKED 是诚实记录"卡住等外部解除"。

---

## R1-R9 评分规则 (针对函数命名场景定制)

> 每条满分 5 分, 总分 45。**二值评分: 0 或 5, 不接受 3 分中间档** (与原 refactor-loop 模板不同, 命名场景模糊更少, 二值更适合)。
> R9 硬规则只有 0 或 5。

### R1 — 命名形式

**要求**: `proposed_name` 严格符合 `^[a-z][a-z0-9_]+$`, 且语义为 `verb_object[_qualifier]`

**5 分**:
- 全小写 + 下划线
- 首词是动词 (如 `apply` / `commit` / `render` / `dispatch` / `resolve` / `init` / `tick` / `flush` / `decode`)
- 第二段是对象 (如 `_zone_cursor` / `_line_buffer` / `_sprite_vram`)
- 可选第三段是修饰 (如 `_step` / `_loop` / `_async`)
- 例: `apply_zone_cursor_step` / `commit_line_buffer_to_sprite_vram` / `decode_card_6bpp_tile`

**0 分** (任一):
- 含禁词: `helper` / `process_data` / `do_thing` / `func_N` / `handler_N` / `routine_N`
- 含大写或连字符
- 仅 1 个词 (`init` / `tick`) — 缺对象
- 首字母缩写无法理解 (`pStore` / `qStrs` / `ctxMgr`)

**清单生成规则**: 给出符合形式的备选名 (≥ 2 个), 让 fixer 选

### R2 — plate explains WHY (不复述 WHAT)

**要求**: plate comment 不能仅复述指令序列, 必须含 (调用方场景 + 触发条件 + 副作用目的) 中至少 2 项, 且为中文。

**5 分**:
- 例: "由 main_dispatch_loop 在帧间隔调用; 检查 `[gPrng+0x230]` 当前 page handler, 若为 NULL 则注册默认 0x080e7e0d (主菜单状态机) 后继续 loop。这是游戏 main thread 的 page 调度兜底。"
- 含: 调用方 (main_dispatch_loop) + 触发条件 (page handler 为 NULL) + 副作用目的 (注册默认 + 兜底)

**0 分** (任一):
- 仅复述指令: "push lr; ldr r0, =0x080e7e0d; bl FUN_X; pop pc"
- 仅说"功能": "Initializes data" / "Handles input" — 抽象到无信息
- 全英文 (项目要求中文文档)
- 含零容忍词 (元规则 2)
- 长度 < 50 字 或 > 500 字 (前者信息不足, 后者太啰嗦)

**清单生成规则**: 给出符合 5 分要求的 plate 重写

### R3 — 参数语义

**要求**: 函数所有非显然 r0/r1/r2/r3 参数都标 `(类型 + 含义 + 范围/枚举)`

**5 分**:
- 例: `r0: u8 page_idx [0..11]` / `r1: ptr -> card_struct (16B; +0=so_code, +4=qty)` / `r2: u32 vram_offset (BG2 base, 0x06004000+)`

**0 分** (任一):
- 任何非显然参数标 generic ("input" / "flag" / "value")
- 漏标某个参数
- "argument 1" / "param 1" 之类无信息描述

**例外** (5 分): 函数明显是 leaf utility 且只有 1 个 i32 参数, 标"r0: i32 value" 也接受 (信息密度匹配)

**清单生成规则**: 列出每个不合格参数 + 应改为的描述 (基于 asm/all.s 函数体推断)

### R4 — 返回值语义

**要求**: 返回值 (r0) 含义明确, 含成功/失败/output channel

**5 分**:
- 例: "r0 = u32 status (0=success, 1=insufficient_buffer, 2=invalid_card)"
- 例: "r0 = u8 next_state (0..0xb 表 page state idx)"
- 无返回值: "void (无返回, 仅副作用)"

**0 分** (任一):
- "returns 0 or 1" 无具体含义
- 漏说返回值
- "成功返回 0" 但没说失败时返回什么

**清单生成规则**: 基于 asm/all.s 函数体内 movs r0,#X 序列 + caller 对 r0 的使用模式, 推出语义

### R5 — 副作用列表

**要求**: 函数体内所有 str/strh/strb 到外部地址 (非 sp 相对) 都列出, 含 (地址 + 写入值含义)

**5 分**:
- 例:
  ```
  - [gPrng+0x230] := 0x080e7e0d (默认 page handler fn_ptr, 主菜单状态机)
  - [BG0CNT (0x04000008)] := <BG0 控制字>
  - [VRAM 0x06014000+] := <512 B sprite tile>
  ```

**0 分** (任一):
- 任何 str/strh/strb 到外部地址漏列
- 仅列地址不说写入值含义 ("[0x03000230] 写入")
- VRAM/PALRAM/OAM 操作未指明区段用途 (例: BG2 tile / sprite OBJ / scroll)

**例外** (5 分): 纯 leaf utility 无外部副作用 (仅修改入参或局部 sp), 标"无外部副作用"接受

**清单生成规则**: grep asm/all.s 函数体内 str/strh/strb, 对每条列出"应改为"

### R6 — 魔数符号化

**要求**: 不保留 `0x4000400` / `0x8120` / `0x10c0` 等裸字面量未解释。用 `.equ` 名 (如 `BG0CNT`) 或注解 (如 `0x8120 → 0x81*4 = 0x204` 偏移)。

**5 分**:
- 例: `movs r1, #0x80; lsls r1, #2  ; r1 = 0x200 (gPrng+0x200 = gFrameCounter)`
- 例: `ldr r0, =0x4000200  ; IE register`
- 例: `0x09e60a8c` 注明 `(deck_edit page table @ ROM 0x09e60a8c, 12 fn_ptr entries)`

**0 分** (任一):
- 裸 `0x4000400` 未注解为 BG2CNT 等
- IWRAM 偏移裸 `0x230` 未注解为 `gPrng+0x1f0` (即 0x03000230)
- ROM 数据表地址未注解用途

**清单生成规则**: grep proposal 的"行级注释"段, 找出裸 hex 数字, 对每个给出符号化形式

### R7 — caller 上下文锚定

**要求**: plate 至少含 1 条 `调用方: <name>` (已命名的 caller) 或 "通过 <table> entry[N] 间接调用" (indirect)

**5 分**:
- 例: "调用方: main_dispatch_loop (per-frame), enter_deck_edit_page (一次性 init)"
- 例: "通过 `0x09e60a8c` deck_edit page table entry[3] 间接派发, 由 enter_deck_edit_page 触发"

**0 分** (任一):
- plate 完全不提调用方
- 仅说 "called by other functions" 无具体名

**清单生成规则**: 从 `temp/complete_callgraph.csv` grep 该 addr 的 caller, 列出已命名的填入 plate

### R8 — 置信度诚实

**要求**: proposal 必须标 `confidence: high/med/low`, 且置信度与证据匹配

**5 分**:
- high: 6 层方法论中至少 3 层有强证据 (例: IO 簇 + 字符串泄漏 + 调用图 hub 三方互证)
- med: 静态推断无矛盾, 但缺少 runtime 验证 / 字符串锚
- low: 仅靠通用模式推断 (例如"看起来像 init"), **必须列出待 runtime 验证的具体动作**

**0 分** (任一):
- 漏标 confidence
- 标 high 但只有 1 层证据
- 标 low 但没列出"待验证项"

**清单生成规则**: 检查证据数 vs 置信度, 给出应改为的级别

### R9 — 硬规则合规 (零容忍, 0 或 5)

**要求**: 不得违反 `CLAUDE.md` 禁止事项 / 项目硬规则。

R9 = 5 / 0 二值, 无中间档。reviewer 在评 R9 之前必须 grep:

| 违规模式 | grep 命令 (从仓库根) | 触发条件 |
|---------|--------------------|---------|
| 自行降级注释 | `grep -nE "\[降级\]\|\[跳过\]\|\[待补全\]" doc/dev/eval/<ADDR>.proposal.md` | ≥ 1 匹配 → 0 分 |
| 中文 mojibake | `python -c "open('doc/dev/eval/<ADDR>.proposal.md', encoding='utf-8').read()"` 抛 UnicodeDecodeError | 抛错 → 0 分 |
| 自行 commit 痕迹 | proposal/eval 含 "已 commit hash X" / "git commit -m"  | ≥ 1 匹配 → 0 分 |
| 跳过 byte-identical | proposal/eval 提"byte-identical 跳过" / "build 跳过" | ≥ 1 匹配 → 0 分 |
| 非 user 授权改 git config | proposal/fixer 提 "git config" 改动 | ≥ 1 匹配 → 0 分 |

**5 分**: 上述全部 0 匹配。

**清单生成规则**: 列出每个违规位置 + 删除/改写指令; **eval 顶部必加红字** `⚠️ HARD RULE VIOLATION (R9)`

---

## 评分汇总表模板

```markdown
| 编号 | 要求 | 得分 | 证据 (位置) | 对应清单项 |
|------|------|------|------------|----------|
| R1 | 命名形式 | 5/5 | proposal:#proposed_name = render_page_title_text | — |
| R2 | plate WHY | 0/5 | plate 仅复述指令序列, 缺触发条件/调用方场景 | #1 |
| R3 | 参数语义 | 0/5 | r0 标"input", r1 漏标 | #2 |
| R4 | 返回值 | 5/5 | "r0 = void" 明确 | — |
| R5 | 副作用 | 0/5 | str r0,[r4,#0] @ 0x08014482 漏列 | #3 |
| R6 | 魔数符号化 | 0/5 | 0x4000400 未注 BG2CNT | #4 |
| R7 | caller 锚定 | 0/5 | plate 不提 caller | #5 |
| R8 | 置信度 | 0/5 | 漏标 confidence | #6 |
| R9 | 硬规则 | 5/5 | grep 全 0 匹配 | — |

**总分: 15/45**
```

## eval 文档格式

```markdown
# Naming Evaluation: 0x<ADDR>

> **版本**: vN (YYYY-MM-DD HH:MM) — 第 N 轮评分
> **状态**: PASSED / NEEDS_FIX / BLOCKED / P0_FAILED
> **proposal 路径**: doc/dev/eval/<ADDR>.proposal.md

## P0 检查结果

- proposal 文件存在: ✅ / ❌
- proposal 含零容忍词: ✅ 0 / ❌ 列出
- 结论: P0 通过 / P0 失败

(P0 失败时停止评分, 填完本段即可结束)

## 评分详情

(上面的汇总表模板)

## 修改清单

> 每条必须可执行: 位置 + 当前 + 应改为, 全部具体不模糊。

### #1 — Rx (优先级)
**位置**: <proposal 段名 / asm/all.s:行号>

**问题**: <具体违反 Rx 的细节>

**当前**:
<原样引用>

**应改为**:
<具体改成什么>

### #2 — Rx
...

## 修改历史

| 版本 | 日期 | 分数 | 状态 | 变更 |
|------|------|------|------|------|
| v1 | YYYY-MM-DD HH:MM | 15/45 | NEEDS_FIX | 首次评分; 修改清单 #1-#6 |
| v2 | YYYY-MM-DD HH:MM | 40/45 | NEEDS_FIX | fixer 应用 #1-#5, R8 仍未达标 (置信度 evidence 不足) |
| v3 | YYYY-MM-DD HH:MM | 45/45 | PASSED | fixer 补充 R8 evidence, review 通过 |
```

---

## 可执行清单自检

写完 eval 后 skill 必须自检:

1. **位置存在** — 引用 `asm/all.s:行号` 的, 跑 `sed -n '<line>p' asm/all.s` 返回非空
2. **当前内容匹配** — "当前" 段引用的文字在 proposal/asm 中可 grep 到
3. **应改为不模糊** — 不允许 "改善 X" / "提升 Y" 这种不可执行描述
4. **改动范围合理** — "应改为" 不超过原文字 3x 长度

任一不满足 → 该清单条目标 "不可执行", 要求 reviewer 重写。

## 分数与清单的一致性自检

- 总分 = 各 Rx 得分之和 (BLOCKED 项扣 0 不算 N/A)
- 非满分 Rx 必须有 ≥ 1 清单条目对应
- 清单项编号与"对应清单项"列必须一致
- PASSED 必须 45/45

任一不一致 → 重写 eval。

---

## 与 lesson-keeper 的衔接

eval 是 lesson-keeper 的主要输入。为了让 lesson-keeper 能抽教训:

- "修改历史"表必须每轮一行
- 每个清单项的"问题"字段写够具体 (让 lesson-keeper 识别模式)
- BLOCKED 情况明确记录原因
- 每个 R 扣分附带 ≥ 1 行证据 (不要只写 "see #N")

---

## 常见调用方式

```
Skill(skill="analysis-eval", args="0x08014470")
Skill(skill="analysis-eval", args="0x080fa4dc")
```

## 不是什么

- 不是命名生成器 — 只评分 + 写 eval
- 不是 Ghidra 调用工具 — fixer 负责 rename
- 不是 commit 工具 — commit 是用户决定
- 不评 byte-identical / Ghidra 同步 / CSV 同步 — 这些是 fixer 落地阶段的红线动作 (有自己的 pass/fail), 不计入 R1-R9 评分
