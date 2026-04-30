# `naming-proposals.csv` —— 函数命名工作台

`doc/dev/naming-proposals.csv` 是 ROM 全函数（3505 个）的命名跟踪表。本文档说明它的 schema、生命周期、写入工具分工，以及如何用脚本/手工驱动它推进。

**本文档不讲方法论**（"为什么要这样命名"），方法论见 [`methodology/function-naming.md`](methodology/function-naming.md)（6 大方法 + 反模式 + 何时停止）。

---

## 一、目标与现状

**终极目标**：~3505 函数全部命名为语义化名字（消灭 `FUN_xxxxxxxx` 占位符），并补齐 module tag。

**当前进度**（截至 2026-04-30，跑 `ExportFunctionInventory.py` 重新生成 `temp/ghidra-functions-summary.md` 看实时数）：

| 指标 | 数值 | 占比 |
|---|---:|---:|
| 总函数数 | 3505 | 100% |
| 已命名（USER_DEFINED） | 167 | 4.76% |
| 自动占位（FUN_/SUB_/thunk_FUN_） | 3338 | 95.24% |
| 有提案待审/apply（`proposed_name` 非空） | 613 | 17.5% |
| —— 其中 score=4（强证据） | 30 | — |
| —— 其中 score=3（中证据） | 231 | — |
| —— 其中 score=2（弱启发） | 352 | — |

进度查询命令汇总在 `temp/ghidra-functions-summary.md`（`ExportFunctionInventory.py` 输出）。

---

## 二、CSV schema

```
address,name,proposed_name,score,tags
```

| 列 | 含义 | 示例 |
|---|---|---|
| `address` | GBA 视角函数入口地址（小写 8 位 hex，带 `0x` 前缀） | `0x080d6290` |
| `name` | Ghidra 当前函数名（USER_DEFINED 后是真名，否则 `FUN_xxxxxxxx`） | `pack_ui_show_all_opened_done` 或 `FUN_080d6290` |
| `proposed_name` | 待 apply 的命名提案，apply 完成后清空 | `font_jp_080dd53c`（占位提案）或 `decode_card_image_6bpp`（真提案） |
| `score` | 证据强度（1-5，详见下表）；apply 完成后清空 | `5` / `4` / `3` / `2` |
| `tags` | 多 module / IO family / FID trampoline tag，单 token 分号分隔 | `font_jp;game_str;pack;vram` |

### score 等级表

| score | 证据来源 | 是否 auto-apply | 含义 |
|:---:|---|:---:|---|
| **5** | FID（编译器/libc 字节级匹配，method 1） | ✓（`ApplyNamingProposals.py`） | 强：(pattern, ROM addr) 唯一匹配，确定到 byte |
| **4** | 多锚相互印证（path string + label + caller，method 3+4 组合） | 手工审 | 较强：≥2 独立证据指向同一名字 |
| **3** | 单锚 + 模块归属确定（如 game_str 模块 EN 文本锚 + master table ref） | 手工审 | 中：单一证据但语义清晰 |
| **2** | propagate 弱启发（callee tag 多数派投票） | 手工审 | 弱：仅"沾边"，需进一步分析 |
| **1** | 候选地址提升（罕用，方法论反模式段，最后防线） | 手工审 | 极弱：候选名 + 地址，无强证据 |
| 空 | 已 apply（落地为现实） | — | name 列已是真名，proposed/score 已清 |

### tag 形式约定（multi-tag 体系）

- **单 token**：`font_jp` / `pack` / `vram` / `tramp_calloc`
- **分号分隔**：`font_jp;game_str;pack`
- **不分直接/间接**：函数 F 调用 game_str 函数 → F 也获得 `game_str` tag（**无 `via_` 前缀**）。一个函数同时属多个 module 是自然事情。
- **Tag 不参与评分**：tag 只标 module 归属，不动 `score` / `proposed_name`。
- **不重新引入旧 `data_label:foo|bar` 多 token 格式**（已废弃）。

详见 `tools/ad-hoc/label_modules.py` 顶部 tag 形式约定注释。

---

## 三、命名生命周期（状态机）

```
[状态 1] 全空白
  name=FUN_xxx, proposed='', score='', tags=''
       │
       │  自动: tag merge 脚本 (label refs / IO regs / funcname 派生)
       ▼
[状态 2] 有 tag, 无提案
  name=FUN_xxx, proposed='', score='', tags='font_jp;...'
       │
       │  自动: propagate / merge 脚本 (FID / 状态表 / 字符串锚) 写 proposed + score
       ▼
[状态 3] 有提案待审
  name=FUN_xxx, proposed='font_jp_xxx', score='3', tags='font_jp;...'
       │
       │  apply:
       │    - score=5 自动: ApplyNamingProposals
       │    - 手工命名:    RenameKnownFunctions / Annotate*.py
       ▼
[状态 4] Ghidra 已命名, CSV 未同步
  name=FUN_xxx (CSV 滞后), proposed='font_jp_xxx', score='3', tags='font_jp;...'
       │
       │  sync: ExportFunctionInventory + sync_ghidra_names_to_proposals
       ▼
[状态 5] 已落地
  name=font_jp_xxx, proposed='', score='', tags='font_jp;...'
```

**状态 4 → 5 的同步是必跑步骤**（详见 `methodology/build-pipeline.md` Phase 3 ⑭）。漏跑会导致 CSV 的 `name` 列停留在 `FUN_xxxxxxxx`，与 Ghidra 现状不一致，后续基于 CSV name 的分析（如 propagate / cluster）会用旧名。

---

## 四、工具分工

### 4.1 写 CSV 的（生产者）

| 脚本 | 写哪些列 | 触发场景 |
|---|---|---|
| `tools/ad-hoc/merge_label_refs_to_proposals.py` | proposed + score + tags | method 3 数据 label 反推（label refs → 函数所属模块） |
| `tools/ad-hoc/merge_fs_load_strings_to_proposals.py` | proposed + score + tags | method 4 路径字符串锚（`fs_load("demo/...")` → 调用者归 demo 模块） |
| `tools/ad-hoc/merge_state_tables_to_proposals.py` | proposed + score + tags | method 5 状态机表反推（page_state_dispatcher 表入口归一个 scene） |
| `tools/ad-hoc/merge_agbcc_fid_to_proposals.py` | proposed + score=5 + tags | method 1 FID 强匹配（agbcc 编译器字节级特征） |
| `tools/ad-hoc/merge_game_str_module_tags.py` | tags（仅追加 module tag） | game_str 模块业务 tag 合并（pack / banlist / duel_field 等） |
| `tools/ad-hoc/propagate_label_tags.py` | tags（multi-tag 沿 callgraph 扩散） | 重跑 tag 扩散（任何 module tag 改动后） |
| `tools/ad-hoc/sync_ghidra_names_to_proposals.py` | name（清 proposed + score） | Ghidra rename 后回写 |
| `tools/ad-hoc/rewrite_tags.py` | tags（旧格式迁移） | 旧 tag 格式 → 新单 token 形式（一次性，幂等） |

### 4.2 读 CSV 的（消费者）

| 脚本 | 读什么 | 用途 |
|---|---|---|
| `tools/ghidra-labeling/ApplyNamingProposals.py` | proposed + score=5 行 | 把 score=5 提案 apply 到 Ghidra（rename 函数） |
| `tools/ad-hoc/cluster_scenes_via_callgraph.py` | tags（scene module token） | 阶段 1 场景大类聚类（Voronoi BFS） |
| `analyze-function` skill 阶段 A | name + tags | 分析单函数时报告当前 CSV 状态 |

### 4.3 触发表（什么场景跑什么）

| 场景 | 跑哪些脚本 | 顺序 |
|---|---|---|
| 新加批量 FID 匹配 | `merge_agbcc_fid_to_proposals.py` → `ApplyNamingProposals.py` | 提案 → apply |
| 新加 USER_DEFINED label（如 `LabelDataCrystalRomMap.py`） | `AddLiteralPoolReferences.py` → `ExportRomLabelsToInc.py` → `merge_label_refs_to_proposals.py` → `propagate_label_tags.py` | 加 label → 补 ref → 写 .equ → 重抽 module tag → 重扩散 |
| 深入分析单函数后 | 见 `methodology/build-pipeline.md` §三 / `analyze-function` skill | 完整 6 步 |
| 新做一类业务模块归类（如 game_str module） | 写专项 `merge_<module>_tags.py` → `propagate_label_tags.py` | 写业务 tag → 重扩散 |
| 大批量 score=5 落地 | `ApplyNamingProposals.py` → `ExportFunctionInventory.py` → `sync_ghidra_names_to_proposals.py` | apply → 重抽 inventory → sync 回 CSV |
| Ghidra 内手工 rename 后 | `ExportFunctionInventory.py` → `sync_ghidra_names_to_proposals.py` | 重抽 → sync |

---

## 五、手工编辑场景（直接编辑 CSV，不跑脚本）

少数情况下直接编辑 CSV 比写脚本更快：

| 场景 | 操作 | 注意 |
|---|---|---|
| 给单个函数追加业务 tag | tags 列追加 `;<new_tag>` | 单 token，避免重复 |
| 否决 propagate 写的 proposed | 删掉 proposed_name + score 两列内容 | 重跑 propagate 不会再写（会避开已有非空 proposed） |
| 强 apply 弱证据提案 | 把 score=3/4 改成 5 | **仅当人工审过该提案**；之后 `ApplyNamingProposals.py` 会拿走 |
| 修正错误命名 | 改 proposed_name | 已 apply 的（state 4-5）需先 Ghidra 内 rename 再 sync |
| 批量 tag 修正 | 写一次性 `tools/ad-hoc/<task>.py` ad-hoc 脚本 | 不修主 propagate 算法，免影响其它模块 |

**禁忌**：
- 不要手工把 name 列从 `FUN_xxx` 改成真名（这是 Ghidra rename + sync 的职责，手工改 CSV 不会同步到 Ghidra）
- 不要在 tags 里重新引入旧的 `data_label:foo|bar` 多 token 格式
- 不要 commit `naming-proposals.csv.bak-*` 备份文件

---

## 六、方法论参考

本文档只讲"如何用 CSV 跟踪命名工作"。具体**怎么决定一个函数的名字**——证据采集、方法选择、置信度判断——见：

[`methodology/function-naming.md`](methodology/function-naming.md)：
- **方法 1** FID 编译器/libc 静态匹配（score=5）
- **方法 2** 硬件寄存器簇（IO family tag）
- **方法 3** 数据 label 反向查询
- **方法 4** 字符串/源码泄漏锚（路径字符串 / assert / 内联文件名）
- **方法 5** 状态机表反推
- **方法 6** 调用图前 N 手工命名
- 反模式：候选地址提升的最后防线
- 何时停止

[`methodology/build-pipeline.md`](methodology/build-pipeline.md) §三：
- 深入分析单函数 → 写入 Ghidra → byte-identical 校验 → sync CSV 的完整 6 步流程
