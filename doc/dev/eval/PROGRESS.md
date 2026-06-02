# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> 已命名函数清单见 `doc/dev/naming-proposals.csv` (pick 数据源, 不在本文档维护)。

---

## 总目标 vs 当前目标

- **总目标**: ROM 内所有函数完成分析 (Ghidra 全 ROM main code 范围 4641 函数; 当前已命名 4464 / 全 CSV 4641 行 = **96.19%**)
- **Phase 1 完成**: campaign_scene_handler 闭包 1526/1526 = 100% (batches #1-#81)
- **Phase 2 完成**: 锁定 766 就绪函数 766/766 = 100% (batches #82-#117, 全 byte-identical, zero red-line)
- **Phase 3 完成**: 新一轮 ready 集合 **1069 函数全部落地** (batches #118..#171, 54 批, 末批 9 函数, 2026-05-30 全部 byte-identical)。
- **Phase 4 完成**: 重导后 ready 集合 **465/465 函数** (batches #172..#195, 24 批, 2026-05-31 全部 byte-identical)。
- **Phase 5 完成**: 重导后 ready 集合 **164/164 函数全部落地** (batches #196..#204, 9 批, 2026-05-31 锁定, 2026-06-02 全部 byte-identical)。
- **Phase 6 进行中**: Phase 5 命名 164 后重算 ready 解锁 **83 函数** (batches #205..#209, 5 批, 2026-06-02 锁定)。仍有 94 FUN_* 被更深层未命名 callee 阻塞 → Phase 7 再重算解锁。
- **就绪定义**: `unnamed AND (no callees OR all callees named)`
- **模式**: 20/批 单 sub-agent 串行 (executor → reviewer → fixer iter → fixer 落地 → lesson-keeper)

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作。

当前阶段 (Phase 6 进行中): 处理重算后 ready 集合 83 个函数 (5 批 #205..#209)。
  - 锁定清单: doc/dev/eval/ready_batches_phase6.json (Phase 6, 5 批 #205..#209)
  - 排序策略: 按地址升序 (与 Phase 2/3/4/5 一致, 利于同区段函数复用簇方法论)
  - 高 indeg hub (indeg=11 0x080563cc / indeg=8 0x080b5d98 / indeg=4 0x08017d64 等) 已散在各批中, 不单独提前
  - 说明: rename 不改拓扑, callgraph 复用 Phase 5 锁定版 (13158 边); ready 用最新 ExportFunctionInventory (177 DEFAULT) 重算

下一批取法:
  python -c "import json; d=json.load(open('doc/dev/eval/ready_batches_phase6.json')); \
    idx=<NEXT_BATCH_IDX>-205; b=d['batches'][idx]; print(' '.join(b['addrs']))"  # batch #205 = idx 0

20/批 单 sub-agent 串行模式 (沿用 Phase 2 末期):
  - executor: 1 个 sub-agent 一次性产 20 份 proposal
  - reviewer: 1 个 sub-agent 一次性评 20 份
  - fixer iter (NEEDS_FIX): 1 个 sub-agent 处理本批所有 NEEDS_FIX
  - fixer 落地: 1 个 sub-agent (Ghidra 单 session, 单 build, 单 sha1 verify)
  - lesson-keeper: 1 个 sub-agent

byte-identical 通过后自动 commit, 进入下一批。

任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:
  1. 在 PROGRESS.md "失败追踪" 段记录 (ADDR, reason, date)
  2. 该 ADDR 跳过落地, 继续下一批
  3. 仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)

完成 5 批后: 再次 ExportFunctionInventory + 重算 ready (python tools/ad-hoc/compute_ready_phaseN.py), 进入 Phase 7 (解锁剩余 94 函数; 若出现不可解的递归 SCC 则登记并求助)。
```

---

## 当前状态

| 字段 | 值 |
|------|----|
| **阶段** | Phase 6 进行中 — 5 批 (#205..#209) 锁定; 下一批 #205 |
| **Ghidra 函数总数** | 4641 (ROM main code 范围, ExportFunctionInventory 最新重导含全 Phase 5 rename) |
| **已命名 (USER_DEFINED / ANALYSIS)** | 4464 (96.19%) |
| **未命名 (FUN_*)** | 177 (83 ready Phase 6 / 94 被更深层 callee 阻塞 → Phase 7) |
| **就绪函数集 (Phase 6)** | 83 函数 (5 批 #205..#209), 处理中 (83 剩余) |
| **下一批** | #205 (Phase 6 idx 0) — `ready_batches_phase6.json` |
| **上次更新** | 2026-06-02 batch #204 PASSED — sound engine init/tick + semihost lseek/close wrappers x4 (4464/4641 = 96.19%); Phase 5 COMPLETE; Phase 6 ready 重算 83 解锁 |
| **callgraph 时间戳** | 2026-05-31 (`temp/ghidra-funcs-callgraph.csv`, 13158 edges; rename 不改拓扑, Phase 6 复用) |
| **callgraph_locked** | `true` (拓扑稳定, 复用 Phase 5 版; 全任务只需 refresh 一次) |
| **ready_locked** | `true` (Phase 6 83 集合锁定; Phase 7 前须重算 ready) |

## 进度

### 已完成阶段

- **Phase 1**: 1526/1526 (100.00%) — campaign_scene_handler 闭包
- **Phase 2**: 766/766 (100.00%) — 全 ROM 就绪函数 (锁定 766, batches #82..#117)

### Phase 3 准备 (2026-05-20, 新一轮 ready 集合)

CSV/callgraph 全量重导 + 同步:
- `temp/ghidra-functions.csv` (4641 函数) — ExportFunctionInventory.py 重导
- `temp/ghidra-funcs-callgraph.csv` (13158 边 / 4641 函数) — ExportFunctionCallGraph.py 重导
- `doc/dev/naming-proposals.csv` 扩展 3646 → 4641 行 (追加 995 个 Ghidra-only addr, 全 FUN_*)
- 备份: `*.bak-20260520-120305` / `*.bak-20260520-120318` 等

Phase 3 ready 集合 (1069 函数) indeg 分布:

| indeg | 数量 | 备注 |
|-------|----:|------|
| 0 | 804 | 75% — runtime fn-ptr 入口 / dead code / 罕用工具 |
| 1-2 | 194 | 18% — 普通叶子 |
| 3-5 | 46 | 4% |
| 6-10 | 12 | 1% |
| 11+ | 13 | <2% — 重点 hub |

高 indeg 优先候选 (已散在地址升序的 54 批中, 不单独提前):

| indeg | addr |
|------:|------|
| 78 | 0x08090624 |
| 53 | 0x0805c218 |
| 37 | 0x080abe40 |
| 35 | 0x08090714 |
| 32 | 0x08096a4c |
| 28 | 0x080dd5e4 |
| 23 | 0x08080c9c |

候选源清单: `temp/ready_addrs_2026-05-20.txt` (1069 行升序)。
锁定批次清单: `doc/dev/eval/ready_batches.json` (54 批 #118..#171, Phase 3 进行中不动态扩张)。

#### ROM 全局命名比例

| 范围 | 已命名 | 未命名 (FUN_*) | 占比 |
|------|-------:|--------------:|-----:|
| Phase 1 campaign 闭包 | 1689 (1526 + 跨根 池 163) | 9 (B_invoker/B_runtime) | ~99.5% |
| Phase 2 ready 集合 (锁定 766) | 766 | 0 | 100.00% |
| **全 Ghidra (4641 函数)** | **3895** | **746** | **83.93%** |
| **Phase 3 ready 集合 (新一轮)** | 1069 (54 批全部完成) | **0** | 100.00% |

---

## 高 rev 异常 (rev ≥ 3) — 待处理 inbox

> **transient inbox**, 不是历史档案。
> fixer 在某函数 rev ≥ 3 时追加一行。用户看到后会询问 / 处理 (sinks: 升级 methodology / 加 feedback / 标已知噪音), 处理完毕**从本表删除**。
> 表空 = 当前无未消化的高 rev 异常。

| ADDR | rev | 函数名 | 备注 |
|------|-----|--------|------|
| 0x0809bdfc | 3 | scan_equip_chain_slots_for_attr_enqueue | .hword 0x4680/4681 解码错误 + r1 callee-save 误判 (post-rewrite-register-side-effect feedback 复现) |
| 0x080a1658 | 3 | check_equip_target_slot_state | R6 DAT 符号化 + R9 零容忍词残留 ("可能是") |
| 0x080fa3a8 | 3 | advance_pack_fadein_to_card_info | R2 推测词反复 (v1 "或为辅助函数" -> fixer 引入 "疑为" -> v3 删除) |
| 0x080e0d40 | 3 | (pack_ui_state tick step=1 branch) | R5 fixer-base-bias: iter-2 fixer cited [+0x134] ignoring r9=pack_ui_state+0xc base bias; effective offset = 0xc+0x134 = 0x140; iter-3 corrected; root cause: fixer used bare asm operand without resolving rBase bias (pool entry: fixer-base-register-bias-wrong-offset) |

---

## BLOCKED 追踪

| SB 编号 | 日期 | 阻塞原因 | 解除前置条件 |
|---------|------|----------|-------------|
| SB-080fa4dc-1 | 2026-05-02 | r3 assert_type 枚举语义需 debug build 验证 (函数命名本身已 PASSED) | 找到 debug build 或匹配工程的 assert 宏定义 |
| SB-080f5e98-1 | 2026-05-02 | 条目 +5 / +1 的 bit mask 操作语义需 mGBA 在 scene_card_list 初始化时 dump gPrng+0x1bc 所指内存结构 (before/after) 确认 | mGBA 断点 FUN_080f5ef4 入口，dump [gPrng+0x1bc] before/after 各条目的 +5/+1 字节变化 |

> 格式: `SB-<ADDR>-<N> | <YYYY-MM-DD> | <阻塞原因> | <解除前置条件>`

## 失败追踪 (auto-skip)

> fixer 在 byte-identical ❌ / MAX_ITER / agent 求助 / 完全无法命名 时追加。
> Phase 2 picker 自动:
>   - 排除 ADDR 在本表的函数 (本身失败)
>   - 排除直接 callee 含本表 ADDR 的函数 (cascade SKIP, 因 R7 无法满足)

| ADDR | 日期 | 失败原因 | 备注 |
|------|------|----------|------|
| _(空)_ | — | — | — |
