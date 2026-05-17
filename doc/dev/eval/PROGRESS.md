# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> 已命名函数清单见 `doc/dev/naming-proposals.csv` (pick 数据源, 不在本文档维护)。

---

## 总目标 vs 当前目标

- **总目标**: ROM 内所有函数完成分析 (~4539 个 callgraph distinct addresses; 当前已命名 2000 / 全 CSV 3646 行 = 54.85%)
- **当前阶段目标**: 处理 `doc/dev/eval/ready_batches.json` 中**锁定的 766 个就绪函数** (按地址相邻分 20 fns 每批, **单 sub-agent 串行模式**, 已完成批次 #82-#84 (40/批模式, 120 fns), 剩余 33 批 `#85..#117` (20/批))
- **就绪定义**: `unnamed AND (no callees OR all callees named)`
- **锁定策略**: 766 集合不动态刷新; 每批落地后不重新计算 ready, 下一轮再批量找 ready
- **模式切换** (2026-05-16): 4×10 并行 → **20/批单 sub-agent**。Phase 2 内已完成 120 函数 (#82-#84 40/批模式), 剩余 646 函数按 20/批分 33 批 (#85..#117)。

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作。

当前阶段: 把 doc/dev/eval/ready_batches.json 中剩余 486 个就绪函数 (25 批, #93..#117, 每批 20) 全部分析完毕。

20/批 单 sub-agent 串行模式 (不再拆分并行):
  - executor: 1 个 sub-agent 一次性产 20 份 proposal
  - reviewer: 1 个 sub-agent 一次性评 20 份
  - fixer iter (NEEDS_FIX): 1 个 sub-agent 处理本批所有 NEEDS_FIX
  - fixer 落地: 1 个 sub-agent (Ghidra 单 session, 单 build, 单 sha1 verify)
  - lesson-keeper: 1 个 sub-agent

下一批取法:
  python -c "import json; d=json.load(open('doc/dev/eval/ready_batches.json')); \
    idx=<NEXT_BATCH_IDX>-85; b=d['batches'][idx]; print(b['addrs'])"

byte-identical 通过后自动 commit, 进入下一批。

任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:
  1. 在 PROGRESS.md "失败追踪" 段记录 (ADDR, reason, date)
  2. 该 ADDR 在 ready_batches.json 中保持原批次但 fixer 跳过其落地
  3. 继续下一批

仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)。

完成 33 批 (#85..#117) 后: 重新跑 ready 计算脚本, 把 766 之外新就绪的函数纳入下一轮 ready_batches。
```

注意: 旧版 `tools/ad-hoc/pick_batch.py` 是 campaign_scene_handler 闭包专用拓扑序 picker, **不再适用本阶段**; 新阶段从 `temp/ready_batches.json` 直接取批。

---

## 当前状态

| 字段 | 值 |
|------|----|
| **阶段** | Phase 2 — 全 ROM 就绪函数批量推进 |
| **就绪函数集** | `doc/dev/eval/ready_batches.json` 锁定 766 函数 / 已完成 280 + 剩余 486 (25 批 #93..#117 / 20 每批) |
| **下一批** | `#93` (20 fns, 单 sub-agent 串行) |
| **上次更新** | 2026-05-17 (Phase 2 batch #92, 280/766 = 36.55%) |
| **callgraph_locked** | `true` (本阶段不刷新拓扑; 仅每完成完整 ready 轮次后才考虑刷新) |
| **ready_locked** | `true` (766 集合不动态扩张) |

## 进度

### Phase 1 完成 (campaign_scene_handler 闭包)

**1526 / 1526 = 100.00% 已分析** (闭包 1698 functions, 其中 A_named=150 + B_invoker=8 + B_runtime=14 = 172 跳过)

里程碑 commits:
- batch #74 `2970de9` 1389/1526 (91.02%)
- batch #75 `c57e153` 1409/1526 (92.33%)
- batch #76 `dad0649` 1429/1526 (93.64%)
- batch #77 `4746e5f` 1449/1526 (94.95%)
- batch #78 `450e883` 1469/1526 (96.27%)
- batch #79 `6a9d899` 1489/1526 (97.58%)
- batch #80 `a16feae` 1509/1526 (98.89%)
- batch #81 `0cef74d` 1526/1526 (**100.00%**, 含 ROOT campaign_scene_handler)

### Phase 2 进行中 (全 ROM 就绪函数)

**280 / 766 已分析** (36.55%, 剩余 25 批待跑 #93..#117)

里程碑 commits (40/批 4×10 并行阶段, 已结束):
- batch #82 `fd44184` 40/766 (5.22%) — BIOS ISR + GL_Scrollbar cluster + name_input + font_jp ctx + sprite gfx
- batch #83 `c9c5102` 80/766 (10.44%) — banlist input + font_jp ctx + name_input cursor + zone chain ops + field slot counts
- batch #84 `3654958` 120/766 (15.67%) — duel field equip cluster + zone sprite + bitmap update + Nitro Unit activation
- batch #85 `220ef3d` 140/766 (18.28%) — equip zone bitmap chain + lp indicator + zone sprite pipeline cluster
- batch #86 `dbc64c6` 160/766 (20.89%) — equip set BST whitelist cluster + banlist canonical map + zone rank3 compaction
- batch #87 `784c1bf` 180/766 (23.50%) — equip_slot eligibility predicate cluster (20 fns)
- batch #88 `e181488` 200/766 (26.11%) — equip slot eligibility + BST tier classifier + LP sprite cluster
- batch #89 `54cdf59` 220/766 (28.72%) — equip slot eligibility + zone placement + tick display cluster
- batch #90 `60ddde0` 240/766 (31.33%) — equip eligibility + zone field state predicate cluster (form(c) indeg=0 heavy)
- batch #91 `611fdb6` 260/766 (33.94%) — card-effect eligibility predicates + dispatch hub (Neo Daedalus, Light of Intervention, Ojama Trio, Zera Ritual)
- batch #92 `(pending)` 280/766 (36.55%) — equip placeability predicates + LP-delta inline fragment cluster (FUN_08064880)

**模式切换** (2026-05-16): 后续 #85+ 切回 20/批 单 sub-agent 串行模式。

#### Phase 2 ready 集合统计

| 维度 | 数量 |
|------|-----:|
| 就绪函数总数 (锁定) | **766** |
| - 已完成 (Phase 2 #82-#92) | 280 |
| - 剩余 (按 20/批 重组) | 486 |
| 剩余分批数 (20/批) | 25 (`#93..#117`) |
| 末批大小 | 6 (#117) |
| 剩余地址覆盖区段 | 0x08047aa0..0x081141d8 |

#### ROM 全局命名比例

| 范围 | 已命名 | 未命名 (FUN_*) | 占比 |
|------|-------:|--------------:|-----:|
| Phase 1 campaign 闭包 | 1689 (1526 + 跨根 池 163) | 9 (B_invoker/B_runtime) | ~99.5% |
| **全 CSV** | **2200** | **1446** | **60.34%** |
| ROM 总 callgraph 函数 | — | — | ~4539 |

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
> Phase 2 picker 自动:
>   - 排除 ADDR 在本表的函数 (本身失败)
>   - 排除直接 callee 含本表 ADDR 的函数 (cascade SKIP, 因 R7 无法满足)

| ADDR | 日期 | 失败原因 | 备注 |
|------|------|----------|------|
| _(空)_ | — | — | — |
