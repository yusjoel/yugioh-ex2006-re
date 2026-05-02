---
name: analysis-loop
description: Drive the full function naming analysis loop for a given ROM address (executor → reviewer → fixer → reviewer → ... until 55/55 or BLOCKED → lesson-keeper). Coordinates 4 analysis-* sub-agents. Includes Step 0/1/2 pre-flight (refresh callgraph + closure classification + topo sort if stale) and PROGRESS.md update at the end. Use when the user says "继续命名" / "analyze 0xXXXXXXXX" / "/analysis-loop" / wants to run one function through the full quality gate.
---

# Analysis Loop Driver Skill

本 skill 把单函数命名串成自动收敛循环。4 角色由独立 sub-agent 承担, 主线程只调度。

## 使用方式

```
/analysis-loop                 # 自动选下一个 (从 PROGRESS.md "下一步" 字段)
/analysis-loop 0x08014470      # 显式指定地址
/analysis-loop 0x08014470 max-iter=5  # 自定义上限
```

参数:
- `<ADDR>` (可选) — ROM 地址, 默认从 `doc/dev/eval/PROGRESS.md` "下一步" 读
- `max-iter=N` (可选, 默认 3) — 循环上限

## 角色

| 角色 | Subagent | 输入 | 输出 |
|------|---------|------|------|
| 分析 | `analysis-executor` | ADDR + 上下文 | `doc/dev/eval/<ADDR>.proposal.md` + Executor Report |
| 审核 | `analysis-reviewer` | proposal + asm/all.s | `doc/dev/eval/<ADDR>.md` (R1-R11 + 清单, 通过 analysis-eval skill 写入) |
| 修改 | `analysis-fixer` | eval 修改清单 | 改 proposal; PASSED 时写 Ghidra + byte-identical + CSV 同步 + PROGRESS.md 更新 |
| 总结 | `analysis-lesson-keeper` | loop 完整历史 | observation_pool 加条目, 或 ≥ 2 复现晋升 `memory/feedback_*.md` |

## 评分阈值

| 状态 | 条件 | 行为 |
|------|------|------|
| PASSED | 55/55 无 BLOCKER | 跳 Step 6 lesson-keeper, 提示用户 commit |
| NEEDS_FIX | < 55 无 BLOCKER | 调 fixer → 回 reviewer |
| BLOCKED | 语义需 runtime 验证 | 登记 SB-<ADDR>-N; lesson-keeper 仍要跑; 不强求 55 |
| P0_FAILED | proposal 缺失 / 含零容忍词 | 调 fixer 专门处理 P0, 其他清单延后 |
| MAX_ITER | 达上限仍 < 55 | 停止, 求助用户 |

> **不接受 54/55**。完美主义是设计目标 — 卡住必须走"求助用户 → BLOCKED 或改 rubric"流程, 不允许自行降级。
> BLOCKED 不是失败 — 诚实记录"除阻塞项外已尽力"的状态。

---

## 硬禁区

任一发现违反 → 立即停止求助用户:

1. proposal/eval 出现 `[降级]` / `[跳过]` / `[待补全]` 注释
2. eval 出现零容忍词 (见 analysis-eval 元规则 2)
3. fixer 写"byte-identical 跳过" / "build 跳过"
4. commit message 出现 "豁免" / "特例" / "暂时"
5. 任一 agent 触碰 CLAUDE.md 禁止事项段硬规则

---

## 工作流程

### Step 0: 前置数据刷新 (条件性)

读 PROGRESS.md, 检查"上次刷新 callgraph 时间":

```bash
# 检查 callgraph 是否陈旧 (asm/all.s 比 complete_callgraph.csv 新)
asm_mtime=$(stat -c %Y asm/all.s)
cg_mtime=$(stat -c %Y temp/complete_callgraph.csv 2>/dev/null || echo 0)
if [ "$asm_mtime" -gt "$cg_mtime" ]; then
    echo "callgraph stale, refreshing..."
    tools/asm-regen/ghidra-run-script.bat ExportFunctionCallGraph.py
    python tools/ad-hoc/resolve_fnptr_tables.py
    python tools/ad-hoc/classify_closure.py
    python tools/ad-hoc/topo_sort_closure.py
fi
```

如果 closure_topo_order.csv 不存在或陈旧, 重跑上述 4 个脚本。

### Step 0.5: 选 candidate

读 `doc/dev/eval/PROGRESS.md` "下一步" 字段:
- 字段非空 → 用其中地址作 `<ADDR>`
- 字段空 → 从 `temp/closure_topo_order.csv` 找最小 topo_idx 且 class != A/B 且未在 PROGRESS 已分析列表中的函数

确认 ADDR 后:
- `Bash grep "^<addr decimal>," temp/closure_topo_order.csv` 拿 topo_idx, depth, indeg, class
- 把这些信息打印让用户确认 (1 行)

### Step 1: executor

```
Agent(analysis-executor, {
  ADDR: <addr>,
  context: { topo_idx, depth, indeg, class }
})
```

读 Executor Report:
- 如 executor 求助用户 → 停止, 转 prompt 给用户
- 否则 → Step 2

### Step 2: reviewer

```
Agent(analysis-reviewer, { ADDR: <addr> })
```

读 `doc/dev/eval/<ADDR>.md`:
- 解析总分
- 解析状态 (PASSED / NEEDS_FIX / BLOCKED / P0_FAILED)
- 校验一致性 (analysis-eval 自检)

### Step 3: 迭代判定

```
if state == PASSED:
    goto Step 5  # 跳过 fixer, 直接 lesson-keeper (因为 PASSED 意味着上一轮 fixer 已落地)
elif state == BLOCKED:
    登记 SB-<ADDR>-N 到 doc/dev/eval/PROGRESS.md "BLOCKED 追踪"段
    goto Step 5  # lesson-keeper 仍要跑
elif state == P0_FAILED:
    调 fixer 专门处理 P0 → 跳回 Step 2
elif state == NEEDS_FIX and iter < max-iter:
    调 fixer → 跳回 Step 2 (iter += 1)
else:  # MAX_ITER
    停止求助用户
```

**首轮 reviewer 后**: R1 (CSV 同步) 一定 0 分, 因为 fixer 还没跑过 Phase 3。所以首轮一定走 NEEDS_FIX → fixer → 第 2 轮 reviewer。

### Step 4: fixer

```
Agent(analysis-fixer, { ADDR: <addr> })
```

读 Fixer Report:
- 如 fixer Phase 1 遇"清单项不可执行" → 记录但继续 (下轮 reviewer 重评)
- 如 fixer 求助用户 → 停止
- 如 fixer Phase 3 byte-identical 失败 → 立即 abort + 提示用户回滚 .rep 备份
- 否则 → 回 Step 2

### Step 5: lesson-keeper

```
Agent(analysis-lesson-keeper, {
  ADDR: <addr>,
  final_state: PASSED / BLOCKED,
  eval_versions: [v1, v2, ...],
  proposal_versions: git log,
  fixer_reports: [r1, r2, ...]
})
```

每个函数都跑 (包括 PASSED 和 BLOCKED), 高频但绝大多数只往 observation_pool 加 1 行。

### Step 6: 最终报告

```markdown
## Analysis Loop Complete: 0x<ADDR>

- Final state: PASSED / BLOCKED / MAX_ITER
- Final score: X/55
- Iterations: N (executor 1 + reviewer N + fixer N-1)
- Final name: <new_name>
- byte-identical: ✅ / ❌ / N/A
- PROGRESS.md updated: ✅ / ❌
- Lessons: <observation_pool: +M / promoted to feedback: +K>
- Next candidate (auto-selected): 0x<NEXT_ADDR>

⏸ 待用户操作:
  1. 检查 doc/dev/eval/<ADDR>.md (评分细节) + doc/dev/eval/<ADDR>.proposal.md (final proposal)
  2. 确认 git diff 后 commit (推荐 message): feat(naming): <new_name> (FUN_<ADDR>) + plate
  3. 继续下一个: /analysis-loop  (会自动选 0x<NEXT_ADDR>)
```

**不自动 commit** — commit 是用户决定。每函数 PASSED 必停下提示 commit。

---

## PROGRESS.md 自动更新协议

fixer Phase 4 必须更新以下字段 (用 Edit, 不 Write 整文件):

| 字段 | 更新逻辑 |
|------|---------|
| 顶部"进度" | 已分析数 +1; 百分比重算 |
| 顶部"当前步骤" | 改为下一 candidate 描述 |
| 顶部"下一步" | 从 closure_topo_order.csv 选最小 topo_idx 未分析 |
| 顶部"上次更新" | 当前时间 |
| 函数列表对应行 | "分析后函数名" 填新 name; "rev" +1; "eval" 填链接 |
| 历史里程碑 | 追加 1 行: `<时间>: <ADDR> PASSED → <new_name>` |
| BLOCKED 追踪 (如有) | 追加 SB-<ADDR>-N 一行 |

---

## 设计取舍

### 为什么 4 角色不是 1 个聪明 agent?

角色分离防自欺。1 agent 改 + 评 + 总结会无意识打高分 (reward hacking)。

### 为什么 reviewer 是独立 sub-agent?

隔离 context。reviewer 默认看不到 executor/fixer 的注释和话术, 只看 proposal/asm/diff。

### 为什么每函数 PASSED 都跑 lesson-keeper?

防忘记。lesson-keeper 内含复现门槛 (1 次 → observation pool, 2 次才 feedback), 高频跑不会污染 memory。

### 为什么不自动 commit?

每函数命名是"小可见改动", 用户应该 review proposal + diff 后决定。装配阶段约定: 每函数 PASSED 后用户决定 commit。

### 为什么 max-iter=3?

经验数字。> 3 轮通常说明 rubric 有问题或函数语义需 runtime 验证 (走 BLOCKED 流程)。
