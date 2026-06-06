# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

GBA ROM 反汇编项目，目标是将《Yu-Gi-Oh! Ultimate Masters: WCT 2006》(`roms/2343.gba`，游戏代码 `BY6E`) 逐步从 `.incbin` 替换为带注释的结构化汇编，最终重新汇编出与原 ROM **byte-identical** 的 `output/2343.gba`（33,554,176 B / `0x1FFFF00`）。进度跟踪在 `PLAN.md`。

## 交流/文档语言

简体中文。所有新文档、代码注释、commit message 默认中文。

## 构建与验证

```bat
build.bat        :: 纯汇编 (as → ld → objcopy)，产出 output/2343.gba。前置: data/*.s 必须已就绪
clean.bat        :: 删 output/ 构建产物
clean-all.bat    :: 5 个导出目录 (data fs fs-decompressed graphics text) → temp/ + clean.bat
build-all.bat    :: export_all.py → build.bat → ROM 校验 → temp 比对 (round-trip)
```

- 使用 **devkitARM**（`as.exe`/`ld.exe`/`objcopy.exe` 需在 `PATH`，或改 `build.bat`）
- 构建前必须先运行 `python tools/rom-export/export_all.py`：从 `roms/2343.gba` 导出 graphics/data/fs，并跑 text↔data 闭环 (decoder + 多 dataset encoder)。`build.bat` 不再含 encoder 步骤——全部统一到 `export_all.py`
- 链接脚本 `ld_script.txt`，入口 `asm/rom.s`（`.include` header + crt0，其余 `.incbin`）
- 单层验证 byte-identical：`fc /b roms\2343.gba output\2343.gba` 或比对 sha1
- **完整 round-trip 验证**：`clean-all.bat` → `build-all.bat`，除 ROM byte-identical 外还逐文件 SHA1 对比 `temp/<dir>/` 与重导出的 5 个目录（约 18,159 文件）。验证脚本 `tools/rom-export/verify_against_temp.py`。
- `build.bat` 末尾 `pause` 受 `NOPAUSE=1` env 控制（`build-all.bat` 内部 setlocal 自动设）

## 代码布局要点

- `asm/rom_header.s` (0x000–0x0BF) + `asm/crt0.s` (0x0C0–0x0FF) + `asm/rom.s`（主串联文件，引用 `data/*.s` 和 `.incbin`）
- `asm/NN_*.s`（25 个反汇编代码模块，原 `asm/all.s` 单体按子系统连续地址区间拆分；由 `tools/asm-regen/split_all_s.py` 据 `split_manifest.tsv` 生成）+ `asm/includes.inc`（有序 `.include` 清单，被 `rom.s` 引用）。`asm/all.s`/`.raw`/`.raw.nomode` 均为可删中间产物（已 gitignore）。Ghidra 再生成后须补跑 `split_all_s.py`；调边界见 `doc/dev/methodology/build-pipeline.md` §七。
- `data/*.s`：已结构化的数据区（见 `PLAN.md` 表格）。新增数据区必须保持 byte-identical——通常流程是：`.incbin` 原始字节 → 脚本生成 `.s` → diff 验证 → 替换。
- `include/macros.inc`：核心宏 `deck_entry so_code, qty` / `banlist_entry so_code, limit` / `deck_card so_code`。`so_code` 用十进制（编码时自动 `so_code*4 | qty` 等运算）。
- `constants/gba_constants.inc`：GBA 硬件寄存器
- `tools/`：Python 数据导出脚本（`export_gfx.py`、`export_card_data.py`、`export_game_strings.py` 等）+ GDB/mGBA 调试辅助
- `doc/dev/`：所有逆向分析、调试笔记、阶段性计划（`p0-*`、`p1-*`）
- `doc/dev/methodology/asset-location.md`：**核心方法论**——ROM 资产定位（动态路径六步流程 + 静态路径四阶段流程 + 卡图/字库/pack-banner 三份实战复盘）；`doc/dev/methodology/build-pipeline.md`：构建流水线 + asm/all.s 再生成；`doc/dev/methodology/symbolization.md`：字面量池符号化（Ghidra↔asm 三方同步、白名单策略、ROM 段边界三连击验证、131 icon 修正案例）；`doc/dev/methodology/font-glyph-ocr.md`：12×12 像素字库 OCR 流程（PaddleOCR 选型 + 多 pass 投票 + 形近字人工复核）；`doc/dev/methodology/function-naming.md`：FUN_xxxxxxxx → 语义名 6 层方法论（FID / IO 寄存器簇 / 数据 label 反推 / 字符串泄漏锚 / 状态表 / 调用图 hub）+ pointer-scan 与 AAIF 反模式
- `doc/um06-*`：外部参考（Google Sheets 转 Markdown）

## 本地机器路径

**不要硬编码工具路径**。机器相关路径（mGBA、devkitARM、PowerShell 7）保存在 `LOCAL.md`（未入库），读它获取实际位置。

## 调试工具链

两套 MCP 并存（同一 mGBA 进程，stub 端口 2345 + Lua bridge 管道），按场景选择组合：

### 场景 A：内存读取 / 截图 / Lua 注入（仅 mGBA MCP）

不需要 GDB。`mgba_live_start` 后直接使用 `read_range` / `run_lua` / `export_screenshot` 等。

### 场景 B：暂停态寄存器检查 / 表达式求值（双 MCP 交互）

1. `mgba_live_start(rom, savestate?, gdb_stub=true)` — **必须显式传 `gdb_stub=true`**（默认关闭 `-g`）。预期超时错误 "Session created but bridge did not become ready before timeout"；session 已创建、stub 已 LISTEN。
2. `gdb_init(gdbPath="tools/arm-none-eabi-gdb.exe")` — **不传 `architecture` 参数**。
3. `gdb_connect(target="localhost:2345")` → `gdb_continue`，游戏放行，Lua bridge 初始化。
4. 用 GDB MCP 读寄存器（`gdb_evaluate_expression`）、单步（`gdb_step`/`gdb_next`）等。
5. ⚠ **不要在 `gdb_continue` 之后用 GDB MCP 发命令**——MI parser 不处理 `*stopped` 异步通知，所有后续命令会超时。

### 场景 C：断点调试（GDB batch 脚本 + mGBA MCP 按键，推荐）

GDB MCP 无法处理断点命中后的状态，改用 batch 脚本：

```
1. mgba_live_start(rom, savestate?, gdb_stub=true)  ← mGBA MCP 启动（-g 暂停；需显式开启）
2. tools\arm-none-eabi-gdb.exe --batch -x script.gdb &   ← 后台运行
   脚本内容: target remote → hbreak *<addr> → continue（阻塞等待命中）
   命中后: info registers / x/Ni $pc / x/Nx <addr> → kill + quit
3. mgba_live_input_set(["A"])              ← mGBA MCP 注入按键触发转场
4. GDB batch 自动捕获断点，打印寄存器后退出
5. 读 GDB 输出文件提取数据
```

示例脚本：`doc/dev/scripts/gdb_card_bp_full.gdb`（卡图加载函数链全捕获）。

### 场景 D：仅用 GDB（无 mGBA MCP 控制）

- `pwsh -File tools/mgba-scripts/start-mgba-gdb-ss1.ps1` → `wait-mgba-ready.ps1` → `gdb_init` → `gdb_connect`。
- ⚠ 此方式启动的 mGBA **不是 managed session**，`mgba_live_attach` 会报错。

### 通用要点

- **GDB 必须使用 `tools/arm-none-eabi-gdb.exe`（10.2）**，devkitPro 14.1 与 mGBA stub 协议不兼容。
- `-g` 来自本地 fork `D:\Software\mgba-live-mcp` 的 patch：`build_start_command` 支持 `gdb_stub` 开关，对应 MCP 工具参数 `gdb_stub`（默认 `false`），CLI 参数 `--gdb-stub`。只在需要 GDB 时显式开启；场景 A 保持默认关闭以避免 stub 端口冲突。见 `doc/dev/tools/mgba-mcp.md` §二。
- **stub 一次性消耗**：GDB 断开（含 `kill`/`quit`/`--batch` 结束）后 stub 永久关闭，需 `mgba_live_stop` + 重新 `mgba_live_start`。
- GDB 脚本里 `echo` 只能 ASCII（中文乱码）。
- 已知 GDB MCP 限制：THUMB 代码 `gdb_list_frames` 失败；`gdb_read_memory` 有解析 bug，改用 `gdb_evaluate_expression`。
- 踩坑汇总：`doc/dev/tools/gdb-debugging.md` §五（12 个坑）

## Commit 规则

**任何文件都不要主动 commit**，必须等用户明确指令。可以主动 `git add`（stage）改动，由用户决定何时提交。

## 反汇编命名 4-agent 体系 (analysis-loop)

**用途**: 自底向上递归命名 ROM 函数。完整文档 `doc/dev/methodology/analysis-loop.md`，进度跟踪 `doc/dev/eval/PROGRESS.md`。

**组件**:
- 4 sub-agent: `analysis-{executor,reviewer,fixer,lesson-keeper}` (位于 `.claude/agents/`)
- 2 skill: `analysis-eval` (R1-R9 评分单一权威, 满分 45) + `analysis-loop` (驱动器, 含 Step 0+1+2 前置 + 落地 phase)
- 经验沉淀: `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_*.md`

**入口**: `Skill: analysis-loop [<addr>]`（不传 addr 则从 PROGRESS.md "下一步"字段读）

**评分 vs 落地分离**: R1-R9 (45 分) 只评 proposal 命名质量。Ghidra rename / asm 重导 / build / byte-identical 验证 / CSV 同步 是 review PASSED 后 fixer 在「落地 phase」执行的红线动作 (byte-identical 失败 = abort + 回滚 .rep), 不计入评分。

## 反汇编细化体系 (refine-loop)

**用途**: 在**已命名**基础上对一个模块文件做**内部细化**——立即数符号化 / 消灭 `DAT_` 自动名 / 误标数据反汇编 / 函数间 `ROM_INCBIN` carve / 注释订正, 全程 byte-identical。与命名互补。**总目标**: `asm/` 下 25 个模块全部细化。完整方法论 `doc/dev/methodology/refine-loop.md`, **跨文件总进度 `doc/dev/refine-progress.md`** (当前文件 00, 自动推进到下一文件: 先按地址拆 ~10 段, 再逐批)。

**组件**:
- 3 sub-agent: `refine-{executor,reviewer,fixer}` (位于 `.claude/agents/`; executor 测绘+ref-scan分类+计划 → reviewer C1-C13 自主复核 → fixer 模式A改proposal/模式B落地)
- 1 skill `refine-loop` (驱动器) + `doc/dev/methodology/refine-loop.md` (R1-R9 细化清单 + 三条硬规则 + carve/disasm/符号化技法)
- 每段留痕: `doc/dev/refine/<Seg-N>.{proposal,review}.md`

**入口**: `Skill: refine-loop [Seg-N | <addr>]`（不传则从活动 refine 文档 §五 选下一未完成段）。轻量段 (纯 §5.1 登记) 主线程可直接处理, 不必起全 3-agent。

**三条硬规则**: ①严格地址序 (文件均分 ~10 段 Seg-1..10, 边界=函数结束处, 不回头不跳号) ②函数间数据必处理 (被引用→carve/disasm, 不留 `ROM_INCBIN`) ③全 ROM 0 引用→§5.1 登记留待。

**Ghidra 注释红线**: 设的 EOL/plate 一律 **ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。

### 反汇编命名零容忍词

eval 文档 / proposal / commit message / agent 输出中出现以下任一 → analysis-eval skill 自动扣 R9 到 0:

| 词 | 替代 |
|----|------|
| 似乎 / 大概 / 应该是 / 可能是 | 给 file:line 证据 + 标置信度 (high/med/low) |
| 我认为 / 我觉得 | 同上 |
| 这次不适用 / 特例 / 暂时 | 走 BLOCKED 流程登记 SB-<ADDR>-N |
| 还行 / 够用 / 凑合 | 不是评分语言 |
| `[降级]` / `[跳过]` / `[待补全]` | 立即 abort, 求助用户 |

### 命名形式硬约束 (R1)

`proposed_name` 必须 `^[a-z][a-z0-9_]+$` 形式, 且语义 `verb_object[_qualifier]`:
- ✓ `apply_zone_cursor_step` / `commit_line_buffer_to_sprite_vram`
- ✗ `helper` / `process_data` / `do_thing` / `func_N` / `handler_N`

## Shell 注意

harness 是 bash（Git Bash / MSYS），但 `build.bat`、`clean.bat`、`tools/*.bat`、`tools/*.ps1` 都是 Windows 脚本——直接调用它们即可（不要移植到 sh）。路径在 bash 命令里用正斜杠。
