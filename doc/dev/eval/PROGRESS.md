# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> **每完成 1 个 batch (默认 15 函数), fixer 一次性更新本文档** (PROGRESS 字段 + N 行函数列表)

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作, batch=15 全自动模式。

python tools/ad-hoc/pick_batch.py --max 15 --out temp/batch.json   # ← 改 15 调整 batch 大小

启动 4-agent loop (executor → reviewer → fixer → lesson-keeper) 处理 batch.json 中的全部函数,
单 Ghidra session + 单 build + 单 sha1 verify, byte-identical 通过后自动 commit, 进入下一 batch。

任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:
  1. 在 PROGRESS.md "失败追踪" 段记录 (ADDR, reason, date)
  2. 该函数标 ⚠ FAIL 于函数列表对应行
  3. pick_batch.py 自动把"含失败 callee"的函数标 SKIP, 不进入下一 batch
  4. 继续下一批

仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)。
```

---

## 当前状态

| 字段 | 值 |
|------|----|
| **根函数** | `campaign_scene_handler` (FUN_08025c94, 由 enter_campaign_page 写入 gMenuState+0x234, 间接调度) |
| **当前步骤** | Step 1 — executor (batch=15 模式) |
| **下一步** | `python tools/ad-hoc/pick_batch.py --max 15 --out temp/batch.json` → 启动 4-agent loop |
| **上次更新** | 2026-05-05 |
| **上次 callgraph 刷新** | 2026-05-05 (含 +50 新反汇 fns, +131 callgraph 边, +26 manual dispatch 边) |
| **callgraph_locked** | `true` (后续 rename 不动拓扑, 整任务期间不需再 refresh) |

## 进度

**0 / 1526 已分析** (campaign_scene_handler 闭包: 1698 functions, 其中 A_named=150 + B_invoker=8 + B_runtime=14 = 172 跳过, 待命名 1526)

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

## 函数列表 (按 topo_idx 升序, 跳过 A/B 类)

> 列说明: # 序号 / topo 拓扑序 / depth BFS 深度 / indeg 全 ROM 入度 / class C 高 indeg / D 中 / E 低 / F orphan
> rev = 本函数完成命名所需的 reviewer 轮数 (期望 ≤ 3)

| # | topo | L | indeg | class | 位置 | 分析前 | 分析后 | rev | eval |
|---|------|---|-------|-------|------|--------|--------|-----|------|
| _(待 callgraph 刷新后填充)_ | | | | | | | | | |

---

## 历史里程碑

- 2026-05-05: **Step 0 完成 (campaign_scene_handler root)**: (1) 切换 root: 0x080e7994 enter_campaign_page (静态闭包仅 3 fn) → 0x08025c94 真实状态机入口. (2) Force-disassemble 3 块 .incbin (0x25d58 0x1f20 / 0x27e50 0x6c / 0x27f00 0x518) 中的 42 个 state handlers + 8 个 promoted sub-routines, 共 +50 functions. (3) 新增 `tools/ghidra-labeling/DisassembleCampaignRegion.py` (基于 DisassembleNameInputRegion.py 模板). (4) 新增 `tools/ad-hoc/{manual_dispatch_edges.csv, merge_manual_edges.py}` 处理 `mov pc,r0` 派发模式 (resolve_fnptr_tables.py 仅识别 invoker-thunk 派发). (5) byte-identical SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b 全程保持. 闭包 28 → 1698 functions (A_named=150 已命名 + 1526 待命名).
- 2026-05-05: **🎉 完成 root=`enter_deck_edit_page` (0x08108ac0) 任务: 259/259 函数命名 100%, byte-identical 全程一致 (SHA1=9689337d6aac1ce9699ab60aac73fc2cfdccad9b), 16 batches × ~15 funcs, 全部 45/45 通过. 累计沉淀 27 feedback 文件锁入 agent (待 root 切换后保留所有规则).** Last commit: `c999fa5`.
- 2026-05-04: 切换根函数到 `enter_campaign_page` (0x080e7994). PROGRESS.md 重置 (BLOCKED 段保留). 已命名函数池 259 个跨根复用.

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
>   - 函数列表对应行标 ⚠ FAIL / ⏭ SKIP

| ADDR | 日期 | 失败原因 | 备注 |
|------|------|----------|------|
| _(空)_ | — | — | — |
