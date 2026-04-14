# 文档全量审阅计划

**创建日期**：2026-04-14
**目的**：对项目现有文档进行一轮全量体检，识别过时内容、重复内容、结构问题，产出整改清单。

---

## 一、文档清单（树状，带行数 / 最近 commit 日期）

### 仓库根
```
README.md                                          274 行 | 2026-04-14
PLAN.md                                            374 行 | 2026-04-14
CLAUDE.md                                           67 行 | 2026-04-14
LOCAL.md                                           (gitignored，本地路径)
```

### doc/dev/ （反汇编/调试/工具链笔记，**主检查对象**）
```
doc/dev/
├─ 调试工具链基础
│   ├─ mgba-gdb-stub-pitfalls.md                   153 行 | 2026-04-14
│   ├─ powershell-job-object-mgba.md               112 行 | 2026-04-13
│   ├─ mgba-mcp-setup.md                           393 行 | 2026-04-14  ← 本次刚改
│   ├─ mgba-mcp-comparison.md                      163 行 | 2026-04-13
│   ├─ mgba-mcp-lua-tutorial.md                    517 行 | 2026-04-13
│   ├─ p0-3-mgba-mcp-feature-validation.md         403 行 | 2026-04-14
│   ├─ p0-5-gdb-mcp-integration.md                 200 行 | 2026-04-14  ← 本次刚改
│   ├─ gdb-breakpoint-matrix.md                    267 行 | 2026-04-14
│   └─ p0-1-gdb-dma3-watchpoint-walkthrough.md     281 行 | 2026-04-13
├─ P1 卡图定位（阶段性成果）
│   ├─ plan-card-image-rom-location.md              60 行 | 2026-04-13   ⚠ 疑似过时
│   ├─ p1-card-image-location-plan.md              193 行 | 2026-04-14
│   ├─ analysis-card-image-loading-function.md     218 行 | 2026-04-13
│   ├─ gdb-watchpoint-card-image.md                214 行 | 2026-04-13
│   ├─ p1-phase-b2-preparation.md                  114 行 | 2026-04-14
│   └─ p1-phase-b2-findings.md                     223 行 | 2026-04-14
├─ 数据/格式参考
│   ├─ card-data-structure.md                      328 行 | 2026-04-12
│   ├─ gba-4bpp-tiled-bg-graphics.md               354 行 | 2026-04-14
│   └─ cp1252-strings-in-gas.md                    197 行 | 2026-04-14
└─ 工作流
    └─ asm-regeneration-workflow.md                184 行 | 2026-04-14
```

### doc/analysis/
```
doc/analysis/
├─ card-detail-page.md                             182 行 | 2026-04-13
└─ p1-card-image-location/
   └─ README.md                                    138 行 | 2026-04-14
```

### doc/um06-* （外部参考，Google Sheets 转录）
```
doc/um06-deck-modification-tool/
├─ home.md
├─ toc.md
├─ data.md
├─ starter-opponent-paste-tool.md
└─ structure-deck-paste-tool.md

doc/um06-romhacking-resource/
├─ toc.md
├─ home 对应的入口（title-screen / main-menu / duel-field / ...）
├─ banlist-code-breaking.md
├─ deck-string-name-tool.md
├─ modifying-banlists.md
├─ modifying-decks.md
├─ opponents-coinflip-screen.md
├─ starter-deck-images-player-icons.md
└─ tool-development.md
```
> **不在本轮检查范围**（CLAUDE.md 明确标注为外部参考）。

### doc/temp/ （临时/工作中文档）
```
doc/temp/
├─ next-session-mcp-install.md                      61 行 | (untracked)  ⚠ 任务已完成，可清理
└─ doc-review-plan.md                               (本文件)
```

### refs/ （第三方仓库，不审阅）

---

## 二、疑似问题初步清单

### A. 明显过时候选（优先检查）

| 文件 | 嫌疑 |
|------|------|
| `doc/dev/plan-card-image-rom-location.md` (60 行) | 与 `p1-card-image-location-plan.md`（193 行，更新）重名；旧计划很可能被取代 |
| `doc/temp/next-session-mcp-install.md` | 本次会话已完成 MCP 安装，文件作废 |

### B. 疑似重复/主题重叠（需对比读）

| 分组 | 成员 | 重叠主题 |
|------|------|----------|
| **mGBA MCP** 三件套 | `mgba-mcp-setup.md` / `mgba-mcp-comparison.md` / `mgba-mcp-lua-tutorial.md` | 工具介绍、Lua 用法、环境配置 |
| **mGBA MCP 验证/功能** | `p0-3-mgba-mcp-feature-validation.md` / `mgba-mcp-setup.md` | 工具清单、修复记录 |
| **mGBA 启动踩坑** | `mgba-gdb-stub-pitfalls.md` / `powershell-job-object-mgba.md` / `mgba-mcp-setup.md` 第 4 节 | Job Object、`-g` 限制、一次性 stub |
| **GDB watchpoint** | `p0-1-gdb-dma3-watchpoint-walkthrough.md` / `gdb-watchpoint-card-image.md` / `p1-phase-b2-findings.md` / `gdb-breakpoint-matrix.md` | DMA/VRAM watchpoint 实战、size=1 字节限制 |
| **P1 卡图定位** | `plan-card-image-rom-location.md` / `p1-card-image-location-plan.md` / `analysis-card-image-loading-function.md` / `p1-phase-b2-preparation.md` / `p1-phase-b2-findings.md` / `doc/analysis/p1-card-image-location/README.md` | 同一任务的多阶段文档，需判断谁是 canonical、谁已被吸收 |

### C. 顶层文档交叉引用

- `README.md`、`PLAN.md`、`CLAUDE.md`：需确认彼此信息同步（例如 PLAN 状态是否反映最近进度，README 链接是否有死链）。

---

## 三、逐文件检查维度（统一 checklist）

对每份受检文档应回答以下 6 个问题：

1. **声明的工具/路径/版本是否还正确？**（如 GDB 10.2、mGBA 版本、uv cache 哈希等）
2. **引用的其他文档是否存在、链接是否正确？**（死链 / 路径大小写 / 已删除文件）
3. **描述的流程与当前仓库状态一致？**（`build.bat` 参数、脚本是否改名、`tools/` 目录重组后的位置）
4. **内容是否已被另一份更新的文档取代？**（若是，是否显式注明"已被 X 取代"或可直接删除/归档）
5. **文档内部是否有矛盾？**（如 P0/P1 阶段标签是否混乱）
6. **本地绝对路径是否外泄？**（`D:\...`、`C:\Users\...` 应只出现在 `LOCAL.md`）

---

## 四、检查执行计划（分 5 批，每批一次性读完 + 产出一个 review 报告段落）

### 批次 1：顶层元文档 + 任务登记
- `README.md` / `PLAN.md` / `CLAUDE.md`
- 目标：确认对外描述与当前状态、链接 target、MCP 章节同步。

### 批次 2：MCP / 调试工具链基础（冗余最多）
- `mgba-mcp-setup.md` / `mgba-mcp-comparison.md` / `mgba-mcp-lua-tutorial.md`
- `p0-3-mgba-mcp-feature-validation.md`
- `mgba-gdb-stub-pitfalls.md` / `powershell-job-object-mgba.md`
- `p0-5-gdb-mcp-integration.md`
- 目标：去重，判断 comparison/lua-tutorial 是否合并进 setup；确定 pitfalls / job-object 的边界。

### 批次 3：GDB 实战
- `p0-1-gdb-dma3-watchpoint-walkthrough.md`
- `gdb-watchpoint-card-image.md`
- `gdb-breakpoint-matrix.md`
- 目标：区分 P0 通用走查 vs P1 专项实战的分工，评估 matrix 是否收纳了所有断点记录。

### 批次 4：P1 卡图定位专题（文档最多，需要梳理线性叙事）
- `plan-card-image-rom-location.md` （疑似过时）
- `p1-card-image-location-plan.md`
- `analysis-card-image-loading-function.md`
- `p1-phase-b2-preparation.md` / `p1-phase-b2-findings.md`
- `doc/analysis/p1-card-image-location/README.md`
- `doc/analysis/card-detail-page.md`
- 目标：确定 plan → preparation → findings 的叙事顺序，归档或删除被吸收的过渡文档。

### 批次 5：数据格式 + 工作流 + 清理
- `card-data-structure.md` / `gba-4bpp-tiled-bg-graphics.md` / `cp1252-strings-in-gas.md`
- `asm-regeneration-workflow.md`
- `doc/temp/next-session-mcp-install.md`（清理决策）
- 目标：核对格式文档与 `data/*.s` / `tools/` 现状；决定 temp 下临时文档的去留。

---

## 五、产出物

检查完成后在 `doc/temp/` 产出：

1. **`doc-review-report.md`**：逐文件结论（保留 / 合并到 X / 删除 / 更新），每条带简短理由。
2. **`doc-review-actions.md`**：具体可执行的变更列表（move/delete/rewrite），按批次组织，方便后续一个个落地。

只在用户确认 report 和 actions 之后才真正动手改文档，保持"先计划，再执行"的节奏。

---

## 六、不做的事

- 不改 `doc/um06-*`（外部参考）。
- 不改 `refs/`（第三方仓库）。
- 不改 `LOCAL.md`（本地配置，按需增量即可）。
- 本轮只做文档体检，不回头改代码、不调整 `tools/` 目录结构。
