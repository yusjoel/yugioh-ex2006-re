---
name: analysis-loop
description: Drive the function naming analysis loop for a ROM address (single or batch). Coordinates 4 analysis-* sub-agents (executor → reviewer → fixer → lesson-keeper). Use when the user says "继续命名" / "analyze 0xXXXXXXXX" / "/analysis-loop" / wants to run one or more functions through the quality gate.
---

# Analysis Loop Driver Skill (slim)

驱动函数命名循环。本 skill 仅给主线程一个调度纲领；详细方法论在 `doc/dev/methodology/analysis-loop.md`，rubric 在 `.claude/skills/analysis-eval/SKILL.md`。

## 入口

```
/analysis-loop                   # 自动选下一个 (PROGRESS.md "下一步" 字段)
/analysis-loop 0x08014470        # 显式地址
/analysis-loop batch=15          # 批量模式 (拓扑闭合子树, 详见 batch 节)
```

## Step 0: 前置 (一次性)

读 PROGRESS.md "callgraph_locked" 字段:
- `true` → 跳过 refresh
- `false` / 缺失 → 仅当 closure_topo_order.csv 不存在时强制 refresh 一次:
  ```bash
  tools/asm-regen/ghidra-run-script.bat ExportFunctionCallGraph.py
  python tools/ad-hoc/{resolve_fnptr_tables,classify_closure,topo_sort_closure}.py
  ```

> 设计: rename 不改拓扑结构, 整任务只需 refresh 一次。lock 默认应该 true。

## Step 1-5: 单函数模式

```
1. executor   →  doc/dev/eval/<ADDR>.proposal.md
2. reviewer   →  doc/dev/eval/<ADDR>.md (R1-R9, max 45)
3. 状态判定:
     PASSED   → fixer 落地 → lesson-keeper → commit (用户已授权 auto-commit)
     NEEDS_FIX→ fixer 改 proposal → 回 step 2 (max-iter=3)
     BLOCKED  → 登记 SB-<ADDR>-N → lesson-keeper
     P0_FAILED→ fixer 删零容忍词 → 回 step 2
4. fixer 落地 phase: Ghidra rename + plate + asm regen + build + byte-identical 验证 + CSV sync + PROGRESS update
5. lesson-keeper: pool +1 / ≥2 复现晋升 feedback
```

byte-identical = 红线; 失败立即 abort 并提示用户回滚 .rep。

## Batch 模式 (高效)

`batch=N` (推荐 N≤15) 时，主线程一次处理 N 个函数:

1. **batch picker**: `python tools/ad-hoc/pick_batch.py [--root <addr>] [--max <N>]` 选拓扑闭合子树
2. **executor batch**: 一次调用产出 N 份 `<addr>.proposal.md`
3. **reviewer batch**: 一次调用产出 N 份 `<addr>.md` (R1-R9 严格逐函数评)
4. **fixer batch 落地**: 单次 Ghidra session 处理 N 个 rename + plate + 单次 asm regen + 单次 build + 单次 byte-identical
5. **lesson-keeper batch**: 一次处理 N 个 loop 历史，pool 内部去重晋升
6. **commit batch**: 1 个 commit 含 N 个函数的命名

收益 vs 单函数: ~4-5x 加速, ~70% token 节约。byte-identical 红线失败 → 回退单函数模式逐个验证。

## 评分阈值

| 状态 | 条件 | 行为 |
|------|------|------|
| PASSED | 45/45 | fixer 落地 → lesson-keeper |
| NEEDS_FIX | < 45 | fixer 改 → 回 reviewer (iter < max-iter) |
| BLOCKED | runtime 验证需求 | SB-<ADDR>-N + lesson-keeper |
| P0_FAILED | proposal 缺失 | fixer 专项处理 |
| MAX_ITER | ≥ max-iter 不收敛 | 求助用户 |

不接受 44/45。完美主义 = 设计目标。

## 红线 (任一触发 → abort 求助用户)

1. proposal/eval 出现 `[降级]` / `[跳过]` / `[待补全]`
2. fixer 写"byte-identical 跳过" / "build 跳过"
3. byte-identical SHA1 不一致
4. commit message 出现"豁免" / "特例" / "暂时"

## auto-commit (用户已授权)

每函数 PASSED + 落地完成后, 主线程自动 commit (格式: `feat(naming): <name> (FUN_<ADDR>) + plate`)。仅 4 种情况停下询问:
- agent 主动求助 (低置信度 / 无法判定 / 硬规则违反)
- byte-identical ❌
- MAX_ITER
- BLOCKED 登记后

详见 `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_analysis_loop_autonomous.md`。

## PROGRESS.md 更新协议

PROGRESS.md 已瘦身为 ~3K tokens 的状态镜像 (不再含 1000+ 行函数表)。已命名清单由 `doc/dev/naming-proposals.csv` 承载, fixer Phase 4 用 Edit (不 Write) 修改:
- 顶部"进度": 已分析数 +N (N = 本 batch PASSED 数) / 百分比
- 顶部"当前步骤" / "下一步" / "上次更新"
- 高 rev 异常段 (transient inbox): 仅本批某函数 rev >= 3 时追加 `| 0x<ADDR> | <rev> | <name> | <反复扣分原因> |` (用户审阅后删行, fixer 只管追加)
- BLOCKED 追踪 (如有): SB-<ADDR>-N
- 失败追踪 (如有): `0x<ADDR> | <YYYY-MM-DD> | <reason> | <一句 why>`

## 关键路径 (一次性参考)

| 文件 | 用途 |
|------|------|
| `.claude/agents/analysis-{executor,reviewer,fixer,lesson-keeper}.md` | 4 sub-agent prompt |
| `.claude/skills/analysis-eval/SKILL.md` | R1-R9 rubric + eval doc 模板 |
| `doc/dev/methodology/analysis-loop.md` | 完整方法论与设计取舍 (按需读) |
| `doc/dev/eval/PROGRESS.md` | 跨会话进度 |
| `temp/closure_topo_order.csv` | 拓扑序候选清单 |
| `tools/ad-hoc/pick_batch.py` | batch picker (TODO: 待第 2 阶段实现) |
