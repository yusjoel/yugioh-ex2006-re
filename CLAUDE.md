# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

GBA ROM 反汇编项目，目标是将《Yu-Gi-Oh! Ultimate Masters: WCT 2006》(`roms/2343.gba`，游戏代码 `BY6E`) 逐步从 `.incbin` 替换为带注释的结构化汇编，最终重新汇编出与原 ROM **byte-identical** 的 `output/2343.gba`（33,554,176 B / `0x1FFFF00`）。进度跟踪在 `PLAN.md`。

## 交流/文档语言

简体中文。所有新文档、代码注释、commit message 默认中文。

## 构建与验证

```bat
build.bat    :: as → ld → objcopy，产出 output/2343.gba
clean.bat
```

- 使用 **devkitARM**（`as.exe`/`ld.exe`/`objcopy.exe` 需在 `PATH`，或改 `build.bat`）
- 构建前必须先运行 `python tools/rom-export/export_all.py` 从 `roms/2343.gba` 导出所有图形/数据文件（不入库）
- 链接脚本 `ld_script.txt`，入口 `asm/rom.s`（`.include` header + crt0，其余 `.incbin`）
- 验证 byte-identical：`fc /b roms\2343.gba output\2343.gba` 或比对 sha1

## 代码布局要点

- `asm/rom_header.s` (0x000–0x0BF) + `asm/crt0.s` (0x0C0–0x0FF) + `asm/rom.s`（主串联文件，引用 `data/*.s` 和 `.incbin`）
- `data/*.s`：已结构化的数据区（见 `PLAN.md` 表格）。新增数据区必须保持 byte-identical——通常流程是：`.incbin` 原始字节 → 脚本生成 `.s` → diff 验证 → 替换。
- `include/macros.inc`：核心宏 `deck_entry so_code, qty` / `banlist_entry so_code, limit` / `deck_card so_code`。`so_code` 用十进制（编码时自动 `so_code*4 | qty` 等运算）。
- `constants/gba_constants.inc`：GBA 硬件寄存器
- `tools/`：Python 数据导出脚本（`export_gfx.py`、`export_card_data.py`、`export_game_strings.py` 等）+ GDB/mGBA 调试辅助
- `doc/dev/`：所有逆向分析、调试笔记、阶段性计划（`p0-*`、`p1-*`）
- `doc/dev/locate-rom-asset-from-vram-diff.md`：**核心方法论**——从 VRAM 差异定位 ROM 资产的六步流程（IO 指纹静态搜索 + GDB watchpoint/hbreak 动态验证），附卡图/字库两份实战复盘
- `doc/um06-*`：外部参考（Google Sheets 转 Markdown）

## 本地机器路径

**不要硬编码工具路径**。机器相关路径（mGBA、devkitARM、PowerShell 7）保存在 `LOCAL.md`（未入库），读它获取实际位置。

## 调试工具链

两套 MCP 并存（同一 mGBA 进程，stub 端口 2345 + Lua bridge 管道），按场景选择组合：

### 场景 A：内存读取 / 截图 / Lua 注入（仅 mGBA MCP）

不需要 GDB。`mgba_live_start` 后直接使用 `read_range` / `run_lua` / `export_screenshot` 等。

### 场景 B：暂停态寄存器检查 / 表达式求值（双 MCP 交互）

1. `mgba_live_start(rom, savestate?)` — 预期超时错误 "Session created but bridge did not become ready before timeout"；session 已创建、stub 已 LISTEN。
2. `gdb_init(gdbPath="tools/arm-none-eabi-gdb.exe")` — **不传 `architecture` 参数**。
3. `gdb_connect(target="localhost:2345")` → `gdb_continue`，游戏放行，Lua bridge 初始化。
4. 用 GDB MCP 读寄存器（`gdb_evaluate_expression`）、单步（`gdb_step`/`gdb_next`）等。
5. ⚠ **不要在 `gdb_continue` 之后用 GDB MCP 发命令**——MI parser 不处理 `*stopped` 异步通知，所有后续命令会超时。

### 场景 C：断点调试（GDB batch 脚本 + mGBA MCP 按键，推荐）

GDB MCP 无法处理断点命中后的状态，改用 batch 脚本：

```
1. mgba_live_start(rom, savestate?)        ← mGBA MCP 启动（-g 暂停）
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
- `-g` 来自本地 fork `D:\Software\mgba-live-mcp` 的 patch（`build_start_command` 里插入 `"-g"`）。见 `doc/dev/mgba-mcp-setup.md` 第八节。
- **stub 一次性消耗**：GDB 断开（含 `kill`/`quit`/`--batch` 结束）后 stub 永久关闭，需 `mgba_live_stop` + 重新 `mgba_live_start`。
- GDB 脚本里 `echo` 只能 ASCII（中文乱码）。
- 已知 GDB MCP 限制：THUMB 代码 `gdb_list_frames` 失败；`gdb_read_memory` 有解析 bug，改用 `gdb_evaluate_expression`。
- 踩坑汇总：`doc/dev/mgba-gdb-stub-pitfalls.md`

## Commit 规则

**任何文件都不要主动 commit**，必须等用户明确指令。可以主动 `git add`（stage）改动，由用户决定何时提交。

## Shell 注意

harness 是 bash（Git Bash / MSYS），但 `build.bat`、`clean.bat`、`tools/*.bat`、`tools/*.ps1` 都是 Windows 脚本——直接调用它们即可（不要移植到 sh）。路径在 bash 命令里用正斜杠。
