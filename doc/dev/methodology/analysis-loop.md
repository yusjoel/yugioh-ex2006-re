# 方法论：4-agent 函数命名循环 (analysis-loop)

> 用途：自底向上批量命名 ROM 函数, 角色分离防 reward-hacking, R1-R11 单一权威评分, 经验沉淀。
> 单函数粒度的命名见 [`function-naming.md`](function-naming.md) (6 层方法论); 本文档讲如何把 6 层方法论包装成可大规模运行的 loop。

---

## 何时用

- root 函数闭包 ≥ 50 个待命名 (单函数零散用 `analyze-function` skill 即可)
- 跨会话推进, 需要进度跟踪
- 命名质量要可审计 (rubric + eval 文档留痕)

---

## 体系结构

```
┌──────────────────────────────────────────────────────────┐
│  用户入口                                                 │
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

## 4 角色边界

| 角色 | 输入 | 输出 | 禁区 |
|------|------|------|------|
| **executor** | ADDR + 上下文 (depth/indeg/class/已命名 caller-callee) | `<ADDR>.proposal.md` (name + plate + sig + 行注释 + 6 层证据) | 不打分 / 不动 Ghidra / 不更新 PROGRESS |
| **reviewer** | proposal + asm/all.s + callgraph | `<ADDR>.md` (R1-R11 评分 + 可执行清单) 通过 analysis-eval skill 写 | 不修代码 / 不被 proposal 注释污染 / 不打 54/55 / 不豁免硬规则 |
| **fixer** | eval 清单 | 改 proposal; PASSED 时 → Ghidra rename + plate + asm 重导 + byte-identical + CSV 同步 + PROGRESS 更新 | 不重新打分 / 不顺手优化清单外 / 不迎合 byte-identical 失败 / 不自行降级 / 不 commit |
| **lesson-keeper** | loop 完整历史 (proposal/eval 多版本 + fixer reports) | observation_pool +1 行 (1 次观察); ≥2 次同主题晋升 `memory/feedback_*.md` + 回灌引用到 agent/skill | 不沉淀一次性决策 / 不复制规则到 agent (只插引用) / 不动代码 |

---

## 关键设计

1. **角色边界硬**：executor 不评分; reviewer 不改; fixer 不打分; lesson-keeper 不动代码。
2. **R1-R11 单一权威**：在 `.claude/skills/analysis-eval/SKILL.md`, agent 全部从这里读。改 rubric 只改一处。
3. **每条扣分对应可执行清单** (位置 + 当前 + 应改为), fixer 只按清单改不自由发挥。
4. **每函数 PASSED 后跑 lesson-keeper** (高频, 1 次观察→pool, ≥2 次→feedback)。复现门槛防止把"一次性决策"当通用规则。
5. **BLOCKED 是合法终态** (函数语义需 runtime mGBA/GDB 验证时, 登记 SB-<ADDR>-N, 不硬凑满分)。
6. **不自动 commit** — 单函数 PASSED 后停下提示用户, 用户决定 commit message。

---

## R1-R11 速查表

完整规则与样例见 `.claude/skills/analysis-eval/SKILL.md`。

| ID | 主题 | 0 分 | 5 分 |
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

满分 55 (R2 在 proposal 阶段 N/A 不计)。**不接受 54/55**。**0/5 二值评分** (命名场景模糊更少, 二值更适合)。

---

## 跨会话续接

**关键文件**：`doc/dev/eval/PROGRESS.md`

包含：
- **续接提示词** (新会话顶部直接粘贴, 即可继续工作)
- **当前状态** (根函数 / 当前步骤 / 下一步 candidate)
- **进度** (X / 259 = X.X%)
- **函数列表** (按 topo_idx 升序, 跳过 A 已命名 / B runtime, 共 259 行)
- **历史里程碑**
- **BLOCKED 追踪**

**fixer Phase 4 必须更新本文档** (用 Edit 不 Write, 只改对应行)。

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

## 状态机

| 状态 | 条件 | 行为 |
|------|------|------|
| **PASSED** | 55/55 无 BLOCKER | 跳到 lesson-keeper, 提示用户 commit |
| **NEEDS_FIX** | < 55 无 BLOCKER | 调 fixer → 回 reviewer (iter += 1) |
| **BLOCKED** | 函数语义需 runtime 验证 | 登记 SB-<ADDR>-N; lesson-keeper 仍要跑; 不强求 55 |
| **P0_FAILED** | proposal 缺失 / 含零容忍词 | 调 fixer 专门处理 P0, 其他清单延后 |
| **MAX_ITER** | 达上限仍 < 55 | 停止, 求助用户 (改 rubric 或拆 scope) |

首轮 reviewer 后 R1 (CSV 同步) 一定 0 分 (fixer 还没跑过 Phase 3), 所以首轮一定走 NEEDS_FIX → fixer → 第 2 轮 reviewer。

---

## 与 analyze-function skill 的关系

旧 skill `.claude/skills/analyze-function/SKILL.md` 仍保留 (供"快速一次性分析"场景用)。**批量推进时优先 analysis-loop** (4 角色防自欺 + 经验沉淀 + 进度跟踪)。

迁移建议：当 analyze-function 的产出习惯性出现质量问题时, 把 R1-R11 中触发的扣分模式回灌到 analyze-function skill 的"质量自检"段。

---

## 演化机制

- **rubric 演化**: 修改 `.claude/skills/analysis-eval/SKILL.md` (单一权威, 改一处)
- **经验入库**: lesson-keeper 自动 (≥2 复现门槛)
- **角色边界变更**: 修改对应 `.claude/agents/analysis-*.md` (注意保持"边界硬"原则)
- **PROGRESS.md 自动更新**: fixer Phase 4 (Edit 不 Write)

---

## 失败处理

| 场景 | 处理 |
|------|------|
| **byte-identical 失败** | fixer 立即 abort + 提示用户回滚 .rep 备份 (每函数 fixer Phase 3 必备份) |
| **eval 清单不可执行** | reviewer 重写 (analysis-eval skill 自检会拦截) |
| **MAX_ITER** | 求助用户改 rubric 或拆 scope (≥ 3 轮不收敛通常说明 rubric 有问题或函数语义需 runtime) |
| **proposal 含零容忍词** | reviewer P0_FAILED, fixer 删词重做 |
| **fixer 改完 reviewer 仍卡同条 R** | lesson-keeper 抽取候选教训, 2 次复现后晋升 feedback (rubric 也可能要补) |

---

## FAQ

### Q: 为什么 4 角色不是 1 个 sub-agent?

角色分离防 reward-hacking。1 agent 同时改 + 评 + 总结会无意识打高分。

### Q: 每函数都跑 lesson-keeper 不会污染 memory 吗?

不会。内含复现门槛: 1 次 → observation_pool 不入正式 feedback; ≥2 次同主题才晋升。绝大多数函数只往 pool 加 1 行后退出。

### Q: 为什么 PROGRESS.md 放 doc/dev/eval/ 而非仓库根?

放 `doc/dev/eval/` 内, 与 per-function eval 文档同目录, 续接时一并 cd 到该目录批量 review 方便。

### Q: 为什么不自动 commit?

每函数命名是"小可见改动", 用户应该 review proposal + diff 后决定 commit message 和 stage 范围。

### Q: max-iter=3 太少?

经验数字。> 3 轮不收敛通常说明 rubric 有问题或函数语义需 runtime 验证 (走 BLOCKED 流程而非硬凑分)。
