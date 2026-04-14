# 文档审阅报告

**配套文件**：`doc-review-plan.md`（检查计划）、`doc-review-actions.md`（最终整改清单，待批次结束后产出）

审阅使用统一 checklist（见 plan 第三节）：工具版本 / 链接死活 / 流程同步 / 是否被取代 / 内部矛盾 / 本地路径外泄。

---

## 批次 1：顶层元文档（`README.md` / `PLAN.md` / `CLAUDE.md`）

### 🔴 跨文档一致性问题

#### 1. 游戏代码标注与 ROM 实际不符

- **证据**：smoke test 直接读 ROM `0x080000AC`（16 字节 header 末段）得到 `BY6E`。
- **错误位置**：
  - `CLAUDE.md:7`：「游戏代码 `BY7E`」
  - `README.md:3`：「游戏代码 `BY7E`」
- **连带风险**：`PLAN.md:143` 在调查 XX 语言时假设项目 ROM 是 BY?E，推断"BY7J 日版残留"。若项目 ROM 实际为 `BY6E`，则该推断依赖的区域映射需重新验证。
- **整改**：全局替换 `BY7E` → `BY6E`，同时在 PLAN L143 备注中标记"此前假设基于错误的游戏码，需要重新核实区域映射"。

#### 2. `tools/` 重组后路径引用未同步

2026-04-13 `tools/` 目录重组（commit `50d5f82`）将 mGBA 管理脚本移到 `tools/mgba-scripts/`，但以下引用仍写旧路径：

| 文件:行 | 旧引用 | 正确路径 |
|---------|--------|----------|
| `CLAUDE.md:43` | `tools\start-mgba-gdb-ss1.ps1` | `tools/mgba-scripts/start-mgba-gdb-ss1.ps1` |
| `CLAUDE.md:49` | `tools\wait-mgba-ready.ps1` | `tools/mgba-scripts/wait-mgba-ready.ps1` |
| `README.md:184` | 同上 | 同上 |
| `README.md:212` | 同上 | 同上 |

其他 `tools/` 引用（`arm-none-eabi-gdb.exe`、`rom-export/export_gfx.py`、`asm-regen/*.py`）**正确**，不动。

#### 3. MCP 上游链接错误

- `README.md:179`：`[mGBA MCP](https://github.com/souldzin/mGBA-http)` —— 链接到的是不同项目 `mGBA-http`。
- 实际使用 `penandlim/mgba-live-mcp`（见 `mgba-mcp-setup.md:27`）。
- `README.md:205` `[GDB MCP](https://github.com/pansila/gdb-mcp)` —— 待批次 2 / 3 时顺带核实。

### 🟡 PLAN.md 状态过时

- `PLAN.md:6–23` P1 任务全是 `[ ]`，但 `doc/dev/p1-phase-b2-findings.md`（2026-04-14）已落地 Phase B2 成果；至少 P1-1（DMA3 watchpoint 捕获加载）、P1-2（判断 LZ77/raw）的结论已出。**需在批次 4 完成 P1 专题审阅后回填 PLAN 状态**（不在批次 1 改，避免和批次 4 矛盾）。
- `PLAN.md:318`：引用脚本 `ExportRangeToGasS_v6.py`，实际文件名是 `ExportRangeToGas.py`（`tools/asm-regen/ghidra/`）。

### 🟢 已确认正确的引用

- `doc/dev/scripts/<name>.gdb`（CLAUDE.md:58 / README.md:242）—— 目录存在且含脚本。
- `tools/arm-none-eabi-gdb.exe`（多处）—— 路径正确。
- `tools/asm-regen/`、`tools/rom-export/`、`tools/ad-hoc/`、`tools/mgba-scripts/` 目录结构与 README:L46–53 描述一致。
- CLAUDE.md 中 MCP 两条硬约束（GDB 10.2、不传 architecture）与 `p0-5-gdb-mcp-integration.md` 本次新增章节**一致**。

### 🔍 批次 1 结论

- `CLAUDE.md`：✅ 已修（游戏码 BY6E、tools 路径 2 处）。
- `README.md`：✅ 已修（游戏码 BY6E、tools 路径 4 处、mGBA MCP 上游链接）。
- `PLAN.md`：✅ 审计表已更新（2026-04-14）、整体精简至 88 行；`ExportRangeToGasS_v6.py` 等过时引用随精简一并移除。P1 子项状态仍待批次 4 回填。

---

---

## 批次 2：MCP / 调试工具链基础

### 审阅范围
`mgba-mcp-setup.md` / `mgba-mcp-comparison.md` / `mgba-mcp-lua-tutorial.md` / `p0-3-mgba-mcp-feature-validation.md` / `mgba-gdb-stub-pitfalls.md` / `powershell-job-object-mgba.md` / `p0-5-gdb-mcp-integration.md`

### 🔴 修复项

#### 1. tools/ 路径缺 `mgba-scripts/` 子目录（4 处）
| 文件:行 | 修正 |
|---------|------|
| `mgba-gdb-stub-pitfalls.md:68` | `tools\wait-mgba-ready.ps1` → `tools/mgba-scripts/wait-mgba-ready.ps1` |
| `powershell-job-object-mgba.md:109-111` | 3 个脚本路径全部补 `mgba-scripts/` |
| `p0-5-gdb-mcp-integration.md:19` | `tools/start-mgba-gdb-ss1.ps1` → `tools/mgba-scripts/start-mgba-gdb-ss1.ps1` |

#### 2. 死链（`mgba-gdb-stub-pitfalls.md`）
- L11 / L149：引用 `doc/gdb-mgba-watchpoint.md`（不存在）→ 删除引用，结论在本文即可。
- L151：`output/gdb_watch_dma.gdb`（不存在）→ 实际路径 `doc/dev/scripts/gdb_dma_watch.gdb`。

### 🟢 冗余判断：无需合并或删除

| 文档组 | 结论 |
|--------|------|
| `mgba-gdb-stub-pitfalls.md` + `powershell-job-object-mgba.md` | 互补关系（坑 4 引用 job-object.md 深入原理），不重复。 |
| `mgba-mcp-setup.md`（安装 + 5 个 Python bug 修复）| 唯一 |
| `mgba-mcp-comparison.md`（mgba-live-mcp vs pymgba-mcp 选型依据）| 唯一 |
| `mgba-mcp-lua-tutorial.md`（Lua API 教学）| 唯一，内容稳定 |
| `p0-3-mgba-mcp-feature-validation.md`（13 工具功能验证 + 6 个踩坑）| 唯一，是验证记录而非 setup |
| `p0-5-gdb-mcp-integration.md`（GDB MCP 四个 parser bug + Claude Code 注册）| 唯一 |

### 🔍 遗留（待后续批次处理）
- `doc/dev/gdb-watchpoint-card-image.md:202` 也引用 `doc/gdb-mgba-watchpoint.md` 死链，归批次 3（GDB 实战）处理。
- `p1-card-image-location-plan.md:75,76` 和 `p1-phase-b2-preparation.md:41` 有 tools 路径未同步（属 P1 专题，归批次 4）。
- `p0-1-gdb-dma3-watchpoint-walkthrough.md` 有 4 处 tools 路径未同步（属批次 3）。

### 🔍 批次 2 结论
所有 4 个文件已修复（+死链 2 处 + 路径 4 处 = 6 个 edit 操作）。本批次无架构性改动。

---

---

## 批次 3：GDB 实战（3 份）

### 审阅范围
`p0-1-gdb-dma3-watchpoint-walkthrough.md` / `gdb-watchpoint-card-image.md` / `gdb-breakpoint-matrix.md`

### 🔴 修复项

#### p0-1-gdb-dma3-watchpoint-walkthrough.md
- L17–20 表、L61/L76 示例输出：4+2 处 `tools/` 路径补 `mgba-scripts/` 子目录
- L49, L67 硬编码 `D:\Program Files\PowerShell\7\pwsh.exe` → 去除绝对路径，注明"见 LOCAL.md"
- L281 "下一步：P0-2" 过时 → 改为指向 P0-3 / P0-5 / P1 Phase B2

#### gdb-watchpoint-card-image.md
- 文档顶部加一条导航："本文为 P0 阶段早期探索，最终结论见 `p1-phase-b2-findings.md`"
- L202 死链 `doc/gdb-mgba-watchpoint.md` → 改指向 `p0-1-gdb-dma3-watchpoint-walkthrough.md`

#### gdb-breakpoint-matrix.md
无需改动，干净。

### 🟢 冗余判断：**三份互补不重复**
- p0-1 = 端到端工具链走通
- matrix = 断点类型 × 内存区域矩阵
- card-image = 卡图定位专项实验（带历史结论修订）

### 🔍 批次 3 结论
修复 2 个文件共 7 处（p0-1 × 6 + card-image × 2）。matrix 不动。

---

---

## 批次 4：P1 卡图定位专题（7 份）

### 审阅范围
`plan-card-image-rom-location.md` / `p1-card-image-location-plan.md` / `analysis-card-image-loading-function.md` / `p1-phase-b2-preparation.md` / `p1-phase-b2-findings.md` / `doc/analysis/p1-card-image-location/README.md` / `doc/analysis/card-detail-page.md`

### 🔴 执行的处理

#### 删除
- **`plan-card-image-rom-location.md`**：60 行，2026-04-13，基于 BIOS SWI 0x11/0x12 断点的早期计划。4 个断点全部未触发，整个路径已证伪，且被 findings（FUN_0801d290 真实路径）完全取代。

#### 顶部加导航（负面结果归档）
- **`analysis-card-image-loading-function.md`**：主体 FUN_08014fa8 分析已证伪。顶部加导航指向 findings，并说明保留理由（负面结果 + 附录 THUMB MOV 速查表）。

#### 路径修复
- `p1-card-image-location-plan.md:75-76`：2 处 `tools/` 补 `mgba-scripts/`
- `p1-phase-b2-preparation.md:41`：1 处 `tools/` 补 `mgba-scripts/`

#### 验证结果补充
- **`p1-phase-b2-findings.md` 加「验证状态」节**（§六）：
  - 用 `tools/ad-hoc/decode_card_6bpp.py` 实测 DESPAIR FROM THE DARK
  - card_id→tile_block 查表 `c4 05` = 1476 ✅
  - 6bpp 公式 + 基址 ✅（灰度 PNG 可清晰辨认蝙蝠/恶魔轮廓）
  - **真实尺寸 10×10 tiles = 80×80 像素**（纠正 Phase A 的 76 tiles 推测）
  - 列出导出失败的 4 个常见坑：tile 重排缺失 / 尺寸误判 / 调色板偏移 / card_id vs slot_id 映射

### 🟢 保留（互补不冲突）
- `p1-card-image-location-plan.md`：作为 Phase A/B2 + 前置知识的索引。
- `p1-phase-b2-preparation.md`：调试环境搭建 SOP（live_cli.py -g patch 等）。
- `p1-phase-b2-findings.md`：核心成果文档。
- `doc/analysis/p1-card-image-location/README.md`：Phase A VRAM diff 分析（验证基准）。
- `doc/analysis/card-detail-page.md`：2026-04-12 基线，含字体 tile 位置（独立于卡图）。

### 🔍 批次 4 结论
- 删除 1 个、修改 4 个、新增验证脚本 1 个（`tools/ad-hoc/decode_card_6bpp.py`）。
- **验证成果**：findings 公式链路通过单卡实测，卡图导出失败的问题范围被大幅收窄到 4 个工程细节。

---

---

## 批次 5：数据格式 + 工作流（4 份）+ 清理

### 审阅范围
`card-data-structure.md` / `gba-4bpp-tiled-bg-graphics.md` / `cp1252-strings-in-gas.md` / `asm-regeneration-workflow.md` + `doc/temp/next-session-mcp-install.md`

### 🔴 修复项

#### card-data-structure.md
- "卡牌图像"章节描述的 `0x01000000~0x01463480` 区（8bpp，40×56，2240B/卡）与 Phase B2 findings 验证的大卡图（6bpp，80×80，4800B/卡，起于 `0x00510640`）是**两批独立数据**——补充了 §3.2 描述详情页大图数据。
- ROM 布局总览表补充 `0x00510640` 起的大卡图条目，并把 `0x01000000` 区重新描述为"列表小图等"。
- 删除死引用：`output/cards_8bpp_grid.png` / `output/card_0000.png` / `output/card_0002.png`（文件不存在），改指向 `p1-phase-b2-findings.md` 和 `tools/ad-hoc/decode_card_6bpp.py`。

#### doc/temp/next-session-mcp-install.md
- **删除**。该文件是上次 session 留给本次的提示词，目的已达成（批次 1 MCP 已装并验证），文件本身 L61 也要求用完删除。

### 🟢 无需改动
- `gba-4bpp-tiled-bg-graphics.md`（354 行）：完整格式规范 + 本项目数据布局，独立价值高。
- `cp1252-strings-in-gas.md`（197 行）：CP1252 + GAS + Python 规范，独立价值明确。
- `asm-regeneration-workflow.md`（184 行）：2026-04-14 最近更新，文档本身已记录 4 个待办（不在本次审阅范围）。

### 🔍 批次 5 结论
- 修改 1 份（card-data-structure）、删除 1 份临时文件。
- `card-data-structure.md` 与 `p1-phase-b2-findings.md` 之间建立了明确的双向引用。

---

## 🎯 全部批次汇总

| 批次 | 审阅数 | 修改 | 删除 | 新增 |
|------|--------|------|------|------|
| 1 | 3（顶层） | 3 | 0 | 0 |
| 2 | 7（MCP） | 4 | 0 | 0 |
| 3 | 3（GDB 实战） | 2 | 0 | 0 |
| 4 | 7（P1 专题） | 4 | 1 | 1（`tools/ad-hoc/decode_card_6bpp.py`） |
| 5 | 4（数据+工作流） | 1 | 1（`doc/temp/next-session-mcp-install.md`） | 0 |
| **合计** | **24** | **14** | **2** | **1** |

### 跨批次发现汇总
- 游戏代码纠正 `BY7E` → `BY6E`（ROM smoke test 实读）
- `tools/` 重组后路径同步（多处 `mgba-scripts/` 子目录漏写）
- 死链清理（`doc/gdb-mgba-watchpoint.md`、`output/gdb_watch_dma.gdb`、多张 PNG）
- 过时路径名（`ExportRangeToGasS_v6.py` → `ExportRangeToGas.py`）
- 6bpp 公式通过单卡实测（验证 findings 的核心结论）
- PLAN.md 精简 374→88 行，doc/ 审计表更新
- 关键事实：**详情页大卡图 vs 列表小图是两批独立数据**，之前的 card-data-structure 仅覆盖后者
