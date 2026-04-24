# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

仅列 pending 工作。已完成项归档到 git log / 各 `doc/dev/*-findings.md`。

---

## 图形资产管线

| 优先级 | ID | 内容 | 备注 |
|---|---|---|---|
| ⭐ | **T2.3** | `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 回写 ROM） | 反向实现现有导出 |

---

## 内嵌文件系统深化

主骨架已全部打通（339 文件全量解包 + byte-identical，详见 `doc/dev/fs-export-and-ocg-tcg.md`）。

**2026-04-24 新增**（`fs_load` + BIOS LZ77 离线解压 + `.gbtn` 渲染；见
`doc/analysis/name-input-page-location.md` + `doc/dev/data-structure/gbtn-format.md`
+ commit `72e19b9`）：
- ✅ `fs_load (FUN_08014FA8)` = `u8* fs_load(const char* path, int flag)`，fs_master_struct @ 0x09E61178 解码
- ✅ BIOS LZ77/Huffman SWI 0x11/0x12 包装命名；`cpu_copy_auto` (SWI 0xB/0xC) 也一并纠正
- ✅ `tools/fs-decompress.py`：Python 离线 LZ77 解压器，**89/89 .LZ* 文件 byte-identical** 于 mGBA 运行时
- ✅ `.gbtn` (NTBG bundle) 完整 spec：PALT + BGDT + 4bpp/8bpp 自动推断 + 2B/4B tilemap entry
- ✅ `tools/rom-export/render_gbtn.py`：**全 26 个 .gbtn 离线渲染为 PNG**（含 title、exodia 动画、name/pass input、vija 漩涡）

余下深化任务按优先级：

| 优先级 | 范围 | 目标 |
|---|---|---|
| ✅ | ~~`.LZ5bg` BGDT/DFPL 内部字段~~（2026-04-24 完成） | NTBG bundle 完整 spec 落在 `doc/dev/data-structure/gbtn-format.md` |
| 🟡 | C1 title 画面 BG 合成 | **单文件已 OK**（bg0_E/J/P/j_tri 各自可见），但多文件合成（bg0 + bg1 + bg3 → 完整标题画面）未做；需建加载清单机制 |
| ⭐ | 其它 NNS 格式 spec + 渲染器 | 63 个 `.ncgr`/`.nclr`/`.ncer`/`.nanr`（OBJ sprite + 动画）未展开 |
| ⭐ | `.ydc` 语义解码（B1 第二阶段） | 解 3 种 4B key（`4f57443f`/`7f217741`/`39a7cf42`）含义、body `so_code*4\|qty` 编码验证、tail 字段用途（LV2_kaeru 等含非零数据）|
| ⭐ | `.ydc` loader 追溯 | 反编译定位 OCG/TCG flag 选 FID 的具体函数。**注意**：`fs_load` 已命名，可从 `grep "bl fs_load"` 19 处 XREF 反查各调用点 |
| — | FS 尾段 B 区 2 KB pointer table | 追 consumer 反推 C struct；覆盖率收益仅 ~0.006% |
| — | `NTBG.BGDT.flags` 字节 0 语义 | `0x00` vs `0x01` 变体功能待反向（palette variant 猜测未验证）|

---

## 后续研究

- **XX 编码反向工程**：每字符 2 字节自定义编码，含义未知。已在 `refs/yugioh-card-search/` 引入日文五十音排序卡表作为对照数据，待解码（可能是 sort key / 假名压缩）。

---

## 文档整理

`doc/dev/` 39 个 + `doc/analysis/` 5 个文档（共 44 个），阶段前缀体系半途而废（P0→P1→P2→P4，跳 P3），`dev/` vs `analysis/` 边界模糊，子系统文档分散。按主题分批合并重组。

| 优先级 | 批次 | 原始文档数 | 目标产出 |
|---|---|---|---|
| ✅ | ~~工具链配置与调试~~（2026-04-23 完成） | 9 → 2 | `doc/dev/tools/mgba-mcp.md`（704 行）+ `doc/dev/tools/gdb-debugging.md`（626 行）|
| ✅ | ~~卡牌系统~~（2026-04-23 完成） | 12 → 7 | `doc/dev/data-structure/` 6 个 spec + `doc/analysis/card-image-location.md` 叙事 |
| 🟡 | 方法论与工作流（部分完成） | 4 → 2 | `doc/dev/methodology/asset-location.md` + `build-pipeline.md`；`ghidra-function-names.md` + `p4-unstructured-regions-survey.md` 延后 |
| — | Pack 系统 | 5 | 待定 |
| — | ROM 整体结构与参考 | 4 | 待定 |
| — | 图像/UI 资源 | 3 | 待定 |
| — | 文件系统 | 2 | 待定 |
| — | 文本/编码 | 2 | 待定 |
| — | 游戏机制研究（T 系列） | 2 | 待定 |

### 批次 1：工具链配置与调试（9 个 → 2 个，**已完成 2026-04-23**）

合并结果：`doc/dev/tools/mgba-mcp.md`（mGBA MCP：setup + lua + comparison + 工具验证）+ `doc/dev/tools/gdb-debugging.md`（GDB：stub pitfalls + matrix + walkthrough + MCP 集成 + Windows 进程）

已合并并删除的源文档：
- [x] ~~`mgba-mcp-setup.md`（471 行）~~ → `tools/mgba-mcp.md` §二 + §七
- [x] ~~`mgba-mcp-lua-tutorial.md`（517 行）~~ → `tools/mgba-mcp.md` §四 + §五 + §六
- [x] ~~`mgba-mcp-comparison.md`（163 行）~~ → `tools/mgba-mcp.md` §一
- [x] ~~`p0-3-mgba-mcp-feature-validation.md`（403 行）~~ → `tools/mgba-mcp.md` §三 + §七
- [x] ~~`mgba-gdb-stub-pitfalls.md`（217 行）~~ → `tools/gdb-debugging.md` §五
- [x] ~~`powershell-job-object-mgba.md`（112 行）~~ → `tools/gdb-debugging.md` §三
- [x] ~~`gdb-breakpoint-matrix.md`（267 行）~~ → `tools/gdb-debugging.md` §四
- [x] ~~`p0-1-gdb-dma3-watchpoint-walkthrough.md`（283 行）~~ → `tools/gdb-debugging.md` §六
- [x] ~~`p0-5-gdb-mcp-integration.md`（214 行）~~ → `tools/gdb-debugging.md` §七

### 批次 2：卡牌系统（12 个 → 7 个，**已完成 2026-04-23**）

**重要原则修订**：放弃原"卡牌系统"顶层分类（卡图只是逆向调研的一个子模块）。重构为：
- **Spec** → `doc/dev/data-structure/`（只写最终确定的数据结构，不写过程/历史/旧版/引用）
- **Narrative** → `doc/analysis/`（按时间线记录逆向调研，保留失败路径与方法论）

合并结果（**12 源 → 7 目标**，压缩 ~50%）：

Spec（`doc/dev/data-structure/`）：
- [x] `card-attributes.md`（134 行）— 5170 × 22B 属性表 + 属性/种族/副类别编码
- [x] `card-names.md`（91 行）— 欧语 CP1252 + 日语 XX 双字节池
- [x] `card-image-big.md`（189 行）— 大卡图 6bpp 80×80 + 解码公式 + 独立调色板
- [x] `card-image-medium.md`（81 行）— 中卡图 8bpp 32×48 × 1536B stride
- [x] `card-image-mini.md`（130 行）— 小带框卡图 8bpp 24×48 + 双调色板（OBJ/BG）
- [x] `card-detail-page.md`（117 行）— 详情页 VRAM 布局（BG2/BG3/OAM/字体）

Narrative（`doc/analysis/`）：
- [x] `card-image-location.md`（495 行）— 卡图加载函数逆向时间线（Phase A/B0/B1/B2/B3）

已合并并删除的源文档（12 个）：
- [x] ~~`card-data-structure.md`~~（§四/五/六/七 非卡牌段落已在 FS/data-analysis-coverage 覆盖，整文件删除）
- [x] ~~`card-image-export.md`~~ → `card-image-big.md`
- [x] ~~`card-mini-frame-export.md`~~ → `card-image-mini.md`
- [x] ~~`card-medium-frame-findings.md`~~ → `card-image-medium.md`
- [x] ~~`analysis-card-image-loading-function.md`~~ → `card-image-location.md` Phase B0 + 附录 THUMB MOV 速查表
- [x] ~~`p1-card-image-location-plan.md`~~ → `card-image-location.md`
- [x] ~~`p1-phase-b2-findings.md`~~ → `card-image-big.md`（spec）+ `card-image-location.md`（叙事）
- [x] ~~`p1-phase-b2-preparation.md`~~（mGBA+GDB 启动步骤，已由 `tools/mgba-mcp.md` + `tools/gdb-debugging.md` 完全覆盖）
- [x] ~~`gdb-watchpoint-card-image.md`~~ → `card-image-location.md` Phase B1
- [x] ~~`gdb-breakpoint-card-image-report.md`~~ → `card-image-location.md` Phase B3
- [x] ~~`doc/analysis/card-detail-page.md`~~ → `data-structure/card-detail-page.md`
- [x] ~~`doc/analysis/p1-card-image-location/`~~ → `card-image-location.md` Phase A + 附录 A

### 批次 3：方法论与工作流（部分完成 2026-04-23）

本轮合并 4 个核心方法论文档为 2 个（`ghidra-function-names.md` 与 `p4-unstructured-regions-survey.md` 延后处理——前者是函数名登记数据不适合方法论目录，后者是方法论的应用结果应迁入 `doc/analysis/`）。

合并结果：`doc/dev/methodology/asset-location.md`（资产定位动态+静态双路径）+ `doc/dev/methodology/build-pipeline.md`（构建 + asm/all.s 再生成）。

已合并并删除的源文档：
- [x] ~~`locate-rom-asset-from-vram-diff.md`（406 行）~~ → `methodology/asset-location.md` §二 动态路径 + §四 方向对比 + §五 实战复盘
- [x] ~~`static-data-region-methodology.md`（120 行）~~ → `methodology/asset-location.md` §三 静态路径
- [x] ~~`workflow-rom-asset-to-structured-asm.md`（214 行）~~ → `methodology/build-pipeline.md` §一 端到端 14 阶段 + §三 checklist + §四 产出模板
- [x] ~~`asm-regeneration-workflow.md`（184 行）~~ → `methodology/build-pipeline.md` §二 Phase 3 子流程

延后处理：
- [ ] `ghidra-function-names.md`（131 行）— 函数名登记数据，不属于"方法论"范畴；未来作为独立模块（或合并至 Ghidra 标注专题）
- [ ] `p4-unstructured-regions-survey.md`（91 行）— 方法论的应用结果（3 个未结构化区域勘查）；未来迁入 `doc/analysis/`

### 批次 4：Pack 系统（5 个）

`doc/dev/` 2 个已结构化分析 + `doc/analysis/pack-analysis/` 3 个动态调研笔记。

- [ ] `pack-banner-static-analysis.md` — 卡包封面资源在 asm/all.s 的引用扫描 + IO 指纹
- [ ] `pack-card-list-analysis.md` — pack_info_table @ 0x09E5E2E8 数据结构解析（51 × 16 B）
- [ ] `doc/analysis/pack-analysis/README.md` — 7 态抽卡流程 + SRAM 存档编码（DP@0x6C38 / 库存 nibble）
- [ ] `doc/analysis/pack-analysis/analysis-summary.md` — 7 态 IO/diff 详表
- [ ] `doc/analysis/pack-analysis/next-steps-progress.md` — pack_cost_table 静态搜索失败记录

### 批次 5：ROM 整体结构与参考（4 个）

- [ ] `ss1-rom-image-survey.md` — ROM 布局概览 + 已分析覆盖率统计
- [ ] `datacrystal-cross-reference.md` — TCRF Wiki 验证的 ROM/RAM 地址 + Ghidra 标签集成
- [ ] `nitrosdk-nnsys-g2d-findings.md` — NitroSDK/NNS 静态链接识别（刚归档）
- [ ] `rom-plaintext-strings-scan.md` — 5 大段明文区扫描（CARD_TEXT/SDK 断言/文件路径等，刚归档）

### 批次 6：图像/UI 资源（3 个）

- [ ] `gba-4bpp-tiled-bg-graphics.md` — 4bpp tile 格式 / tilemap 编码 / 27 对手
- [ ] `hud-sheet-references-in-code.md` — HUD 精灵（116 tile / 3.7KB / 13 sheet）引用扫描
- [ ] `p2-font-location-findings.md` — 阶段 P2：1bpp 8×8 字体定位（8B/char）

### 批次 7：文件系统（2 个）

- [ ] `fs-export-and-ocg-tcg.md` — 339 FS 文件 + 99 重复路径（OCG/TCG 变体）+ off-by-one bug 修复
- [ ] `fs-tail-analysis.md` — FS 尾段 2KB 指针表 + 1.22MB 随机 padding 分析

### 批次 8：文本/编码（2 个）

- [ ] `cp1252-strings-in-gas.md` — 德法特殊字符在 GAS 中的 `.byte` 语法规范
- [ ] `xx-encoding-analysis.md` — 日文/自定义 2 字节编码反向工程与解码器

### 批次 9：游戏机制研究（T 系列，2 个）

与 ROM 逆向主线关系较弱，考虑保留现状或移入独立 `doc/game-mechanics/`。

- [ ] `t-coinflip-research.md` — 掷硬币机制
- [ ] `t-theme-research.md` — 主题/调色板选择机制


