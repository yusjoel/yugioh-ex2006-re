# refactor-loop 体系适配说明 (analysis-loop)

> 源体系: `E:\Ball\GameBotLab\doc\refactor_loop_portable\README.md`
> 适配目标: GBA Thumb 反汇编逐函数命名 (root = enter_deck_edit_page, 闭包 308 函数)
> 装配日期: 2026-05-02

---

## 体系结构

```
┌──────────────────────────────────────────────────────────┐
│  用户入口 (1 个 skill, 不再用旧 analyze-function 模式)    │
│                                                          │
│  Skill(analysis-loop, "<addr>")                          │
│  → 不传 addr 则从 doc/dev/eval/PROGRESS.md "下一步" 读    │
└──────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────┐
│            Step 0+1+2 前置 (analysis-loop 内嵌)          │
│                                                          │
│  Step 0: callgraph 陈旧检查 + 重跑                       │
│    - ExportFunctionCallGraph.py                          │
│    - resolve_fnptr_tables.py                             │
│  Step 1: classify_closure.py                             │
│  Step 2: topo_sort_closure.py                            │
│                                                          │
│  → 输出最新 closure_topo_order.csv, 选下一 candidate     │
└──────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────┐
│              4 个专职 sub-agent (model: sonnet)           │
│                                                          │
│  analysis-executor      analysis-reviewer                │
│  (产出 proposal)         (评 R1-R11, 写 eval+清单)        │
│                                                          │
│  analysis-fixer         analysis-lesson-keeper           │
│  (按清单改; PASSED 时   (≥2 复现晋升 feedback,           │
│   写 Ghidra+byte-id      回灌 agent/skill)               │
│   +CSV+PROGRESS)                                         │
└──────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────┐
│  产物                                                     │
│                                                          │
│  - asm/all.s (改名+plate 后重导, byte-identical)         │
│  - doc/dev/eval/<ADDR>.proposal.md  (executor 产出)      │
│  - doc/dev/eval/<ADDR>.md           (reviewer 评分历史)   │
│  - doc/dev/eval/PROGRESS.md         (跨会话进度跟踪 ★)   │
│  - doc/dev/eval/observation_pool.md (lesson 待沉淀池)     │
│  - ~/.claude/.../memory/feedback_*.md (≥2 复现的经验)    │
└──────────────────────────────────────────────────────────┘
```

---

## 关键设计

1. **4 角色边界硬**: executor 不评分; reviewer 不改; fixer 不打分; lesson-keeper 不动代码。
2. **R1-R11 单一权威**在 `.claude/skills/analysis-eval/SKILL.md`, agent 全部从这读。
3. **每条扣分对应可执行清单** (位置 + 当前 + 应改为), fixer 只按清单改。
4. **每函数 PASSED 后跑 lesson-keeper** (高频, 1 次观察→pool, ≥2 次→feedback)。
5. **BLOCKED 是合法终态** (函数语义需 runtime 验证时, 登记 SB-<ADDR>-N, 不硬凑满分)。
6. **不自动 commit** — 单函数 PASSED 后停下提示用户, 用户决定 commit message。

---

## 跨会话续接

**关键文件**: `doc/dev/eval/PROGRESS.md`

包含:
- 续接提示词 (新会话顶部直接粘贴, 即可继续工作)
- 当前状态 (根函数 / 当前步骤 / 下一步 candidate)
- 进度 (X / 259 = X.X%)
- 函数列表 (按 topo_idx 升序, 跳过 A 已命名 / B runtime, 共 259 行)
- 历史里程碑
- BLOCKED 追踪

**fixer Phase 4 必须更新本文档** (Edit 不 Write)。

---

## R1-R11 速查表

| ID | 主题 | 0 分判定 | 5 分判定 |
|----|------|---------|---------|
| R1 | CSV+Ghidra 同步 | naming-proposals.csv 仍 FUN_/SUB_ | name 列已新名 + Ghidra 一致 |
| R2 | byte-identical | sha1 不一致 | sha1 一致 (proposal 阶段 N/A) |
| R3 | 命名形式 | 含禁词 / 大写 / 单词 | `verb_object[_qualifier]` 全小写下划线 |
| R4 | plate WHY | 仅复述 WHAT | 含调用方场景+触发条件+副作用目的 ≥2 项 |
| R5 | 参数语义 | 标 generic 或漏标 | 每参数 `(类型+含义+范围)` |
| R6 | 返回值 | 漏 / `0 or 1` 无含义 | 明确成功/失败/output channel |
| R7 | 副作用 | 任一 str 漏列 | 全列 `[<addr>] := <value>` 含义 |
| R8 | 魔数符号化 | 裸 `0x4000400` | 用 `.equ` 名或注解偏移 |
| R9 | caller 锚定 | plate 不提 caller | ≥1 已命名 caller 或 indirect 表说明 |
| R10 | 置信度 | 漏标 / high 无证据 | high/med/low + low 必列待验证项 |
| R11 | 硬规则 (二值) | 含零容忍词/降级注释 | grep 全 0 匹配 |

满分 55 (R2 在 proposal 阶段 N/A 不计)。**不接受 54/55**。

---

## 与原 refactor-loop 模板的差异

| 维度 | 原模板 | 本适配 |
|------|--------|------|
| 评分粒度 | 0/3/5 三档 | 0/5 二值 (命名场景模糊更少) |
| scope 大小 | 模块/feature 级 | 单函数级 (闭包内 1 函数 = 1 scope) |
| max-iter 默认 | 3 | 3 |
| lesson-keeper 触发 | loop 结束跑 1 次 | 每函数 PASSED 后跑 |
| commit 策略 | 不自动, 用户决定 | 同 (每函数停下提示) |
| 进度跟踪 | 无 | PROGRESS.md (跨会话续接 ★) |
| 前置数据 | 无 | Step 0+1+2 (callgraph/closure/topo, 内嵌 analysis-loop) |
| domain 占位符 | `<DOMAIN>` 等 | 已替换为 GBA Thumb 反汇编 |

---

## 入口示例

```
# 自动续接 (从 PROGRESS.md "下一步" 读)
/analysis-loop

# 显式指定地址
/analysis-loop 0x08014470

# 自定义上限 (默认 max-iter=3)
/analysis-loop 0x08014470 max-iter=5
```

---

## 关键路径

| 文件 | 用途 |
|------|------|
| `.claude/agents/analysis-{executor,reviewer,fixer,lesson-keeper}.md` | 4 sub-agent prompt |
| `.claude/skills/analysis-eval/SKILL.md` | R1-R11 单一权威 + eval 文档格式 |
| `.claude/skills/analysis-loop/SKILL.md` | 驱动器 (含 Step 0+1+2 前置) |
| `doc/dev/eval/PROGRESS.md` | 跨会话进度跟踪 |
| `doc/dev/eval/<ADDR>.proposal.md` | executor 产出 (per-function) |
| `doc/dev/eval/<ADDR>.md` | reviewer 评分 (per-function) |
| `doc/dev/eval/observation_pool.md` | lesson-keeper 待沉淀的 1 次观察 |
| `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_*.md` | ≥2 次复现晋升的经验规则 |
| `tools/ad-hoc/{resolve_fnptr_tables,classify_closure,topo_sort_closure,gen_progress_md}.py` | Step 0/1/2/init 工具 |
| `temp/{complete_callgraph,fnptr_tables,closure_classified,closure_topo_order}.csv` | 前置产出 (gitignored) |

---

## 与 analyze-function skill 的关系

旧 skill `.claude/skills/analyze-function/SKILL.md` 仍保留 (供"快速一次性分析"场景用)。但**批量推进 deck_edit 命名时优先用 analysis-loop** (4 角色防自欺 + 经验沉淀)。

迁移建议: 当 analyze-function 的产出习惯性出现质量问题时, 把 R1-R11 中触发的扣分模式回灌到 analyze-function skill 的"质量自检"段。

---

## 演化机制

- rubric 演化: 修改 `.claude/skills/analysis-eval/SKILL.md` (单一权威, 改一处)
- 经验入库: lesson-keeper 自动 (≥2 复现门槛)
- 角色边界变更: 修改对应 agent.md (注意保持"边界硬"原则)
- PROGRESS.md 自动更新: fixer Phase 4 (Edit 不 Write)

---

## FAQ

**Q: 为什么 4 角色不是 1 个 sub-agent?**
A: 角色分离防 reward-hacking。1 agent 同时打分 + 改代码会无意识打高分。

**Q: 每函数都跑 lesson-keeper 不会污染 memory 吗?**
A: 内含复现门槛 (1 次 → observation_pool 不入正式 feedback; ≥2 次同主题才晋升)。绝大多数函数只往 pool 加 1 行后退出。

**Q: 为什么 PROGRESS.md 不放仓库根?**
A: 用户决策。放 `doc/dev/eval/` 内, 与 per-function eval 文档同目录, 便于续接时一并 cd 到该目录批量 review。

**Q: 失败回滚?**
A: byte-identical 失败 → fixer abort + 提示用户回滚 .rep 备份 (每函数 fixer Phase 3 必备份)。eval 不可执行清单 → reviewer 重写。MAX_ITER → 求助用户改 rubric 或拆 scope。
