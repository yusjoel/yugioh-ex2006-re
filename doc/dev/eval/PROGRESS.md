# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> 已命名函数清单见 `doc/dev/naming-proposals.csv` (pick_batch.py 数据源, 不在本文档维护)。

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作, batch=20 全自动模式。

python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json

启动 4-agent loop (executor → reviewer → fixer → lesson-keeper) 处理 batch.json 中的全部函数,
单 Ghidra session + 单 build + 单 sha1 verify, byte-identical 通过后自动 commit, 进入下一 batch。

**强制单 call 模式 (token 经济优先, 不在意 wall-clock)**:
  - executor: 1 个 sub-agent 一次性产出 batch 全部 20 份 proposal (禁止拆分 4×5 并行)
  - reviewer: 1 个 sub-agent 一次性评 20 份 (禁止拆分)
  - fixer iter (NEEDS_FIX): 1 个 sub-agent 处理本批所有 NEEDS_FIX
  - 拆分并行会导致 skill/feedback/asm 上下文重复加载, 实测 ~3× token 浪费, 收益仅 wall-clock

任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:
  1. 在 PROGRESS.md "失败追踪" 段记录 (ADDR, reason, date)
  2. pick_batch.py 自动把"含失败 callee"的函数标 SKIP, 不进入下一 batch
  3. 继续下一批

仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)。
```

---

## 当前状态

| 字段 | 值 |
|------|----|
| **根函数** | `campaign_scene_handler` (FUN_08025c94, 由 enter_campaign_page 写入 gMenuState+0x234, 间接调度) |
| **当前步骤** | Step 1 — executor (batch=20 全自动模式, campaign-75) |
| **下一步** | `python tools/ad-hoc/pick_batch.py --max 20 --out temp/batch.json` → 启动 4-agent loop (campaign-75, 下一候选: topo=1544+) |
| **上次更新** | 2026-05-16 (campaign-74 batch #74, 1389/1526, 91.02%) |
| **上次 callgraph 刷新** | 2026-05-05 (含 +50 新反汇 fns, +131 callgraph 边, +26 manual dispatch 边) |
| **callgraph_locked** | `true` (后续 rename 不动拓扑, 整任务期间不需再 refresh) |

## 进度

**1389 / 1526 = 91.02% 已分析** (campaign_scene_handler 闭包: 1698 functions, 其中 A_named=150 + B_invoker=8 + B_runtime=14 = 172 跳过, 待命名 1526)

> 已命名函数池 (跨根复用): 259 个 (来自上一根 `enter_deck_edit_page` 任务). pick_batch.py 自动跳过已命名函数, 仅处理新根闭包内剩余 `FUN_*` 节点. 闭包内 A_named=150 即来自此池.

### 闭包 class 分布

| class | 数量 | 含义 | 处理 |
|-------|-----:|------|------|
| A_named | 150 | 已命名 (来自跨根池) | 跳过 |
| B_invoker | 8 | 0x0810e5c8..0x0810e5f0 invoker thunks | 跳过 |
| B_runtime | 14 | 0x0810e5c8 起 runtime/libgcc | 跳过 |
| C_util_high | 70 | indeg ≥ 20 的高频工具 | 命名 |
| D_shared_mid | 239 | indeg 5-19 的共享函数 | 命名 |
| E_specific_low | 1216 | indeg 1-4 的 feature-specific | 命名 |
| F_orphan | 1 | indeg=0 的 root (campaign_scene_handler 自身) | 命名 |

非 trivial SCC: 4 个 (size 3/2/6/2), 在 batch 中标记并行命名.

---

## 高 rev 异常 (rev ≥ 3) — 待处理 inbox

> **transient inbox**, 不是历史档案。
> fixer 在某函数 rev ≥ 3 时追加一行。用户看到后会询问 / 处理 (sinks: 升级 methodology / 加 feedback / 标已知噪音), 处理完毕**从本表删除**。
> 表空 = 当前无未消化的高 rev 异常。

| ADDR | rev | 函数名 | 备注 |
|------|-----|--------|------|
| 0x0809bdfc | 3 | scan_equip_chain_slots_for_attr_enqueue | .hword 0x4680/4681 解码错误 + r1 callee-save 误判 (post-rewrite-register-side-effect feedback 复现) |
| 0x080a1658 | 3 | check_equip_target_slot_state | R6 DAT 符号化 + R9 零容忍词残留 ("可能是") |

---

## BLOCKED 追踪

| SB 编号 | 日期 | 阻塞原因 | 解除前置条件 |
|---------|------|----------|-------------|
| SB-080fa4dc-1 | 2026-05-02 | r3 assert_type 枚举语义需 debug build 验证 (函数命名本身已 PASSED) | 找到 debug build 或匹配工程的 assert 宏定义 |
| SB-080f5e98-1 | 2026-05-02 | 条目 +5 / +1 的 bit mask 操作语义需 mGBA 在 scene_card_list 初始化时 dump gPrng+0x1bc 所指内存结构 (before/after) 确认 | mGBA 断点 FUN_080f5ef4 入口，dump [gPrng+0x1bc] before/after 各条目的 +5/+1 字节变化 |

> 格式: `SB-<ADDR>-<N> | <YYYY-MM-DD> | <阻塞原因> | <解除前置条件>`

## 失败追踪 (auto-skip)

> fixer 在 byte-identical ❌ / MAX_ITER / agent 求助 / 完全无法命名 时追加。
> pick_batch.py 自动:
>   - 排除 ADDR 在本表的函数 (本身失败)
>   - 排除直接 callee 含本表 ADDR 的函数 (cascade SKIP, 因 R7 无法满足)

| ADDR | 日期 | 失败原因 | 备注 |
|------|------|----------|------|
| _(空)_ | — | — | — |
