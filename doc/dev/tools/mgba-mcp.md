# mGBA MCP 使用指南

本文档是本项目使用 [mgba-live-mcp](https://github.com/penandlim/mgba-live-mcp) 进行动态调试的统一参考，涵盖：工具选型、安装与 fork 配置、15 个 MCP 工具参考、Lua 脚本教程、GBA 内存速查，以及全部 Windows 特殊修复记录。

> **看完这里还要 GDB？** 参见 [`gdb-debugging.md`](gdb-debugging.md)。mGBA MCP 无法监听 ROM/VRAM 内存读取，断点相关能力需走 GDB stub。

---

## 一、工具选型：mgba-live-mcp vs pymgba-mcp

在动态分析 GBA ROM 时，理想的工作流是：

```
触发游戏动作 → 监听 CPU 从 ROM 读取了哪些地址 → 精确定位数据来源
```

调研过 [mgba-live-mcp](https://github.com/penandlim/mgba-live-mcp) 与 [pymgba-mcp](https://github.com/zenitraM/pymgba-mcp) 两套方案，**两者都无法监听内存读取**——这是 mGBA API 设计边界，与 MCP 实现无关。

### 架构对比

| | mgba-live-mcp（本项目使用） | pymgba-mcp |
|--|--------------|-----------|
| 底层接口 | mGBA **Lua 脚本引擎**（通过 `--script`） | mGBA **原生 Python cffi 绑定** |
| 运行方式 | 需要 Qt 窗口，mGBA 独立进程 | 无头模式，Python 进程内嵌 mGBA 核心 |
| 打包方式 | pip / uvx，兼容 Windows | Nix flake，主要面向 Linux/macOS |
| Windows 可用性 | ✅ 可用（需少量修复，见 §八）| ⚠️ 困难（需自行编译 mGBA Python 绑定）|

### 功能对比

| 功能 | mgba-live-mcp | pymgba-mcp |
|------|:---:|:---:|
| 加载 ROM / 截图 / 按键 / 读写内存 / OAM / savestate | ✅ | ✅ |
| 执行 Lua 脚本 | ✅ | ❌ |
| CPU 寄存器读取 | ❌ | ✅ |
| 单步执行（step） | ❌（注册但无效）| ✅ |
| **设置断点/watchpoint** | ❌ | ❌（README 提及但代码未实现）|
| **监听内存读取** | ❌ | ❌ |

pymgba-mcp 的 README 写有 "Set breakpoints" 功能，但检查 `emulator.py` / `server.py` 源码确认：工具列表中**没有** `set_breakpoint`、`add_watchpoint` 等，该功能**未实现**，是 vibecoded 文档遗留描述。

### 为什么两套方案都无法监听读取

mGBA Lua `callbacks` 对象官方支持的事件类型（[官方文档](https://mgba.io/docs/scripting.html)）：

> `alarm` / `crashed` / `frame` / `keysRead` / `reset` / `savedataUpdated` / `sleep` / `shutdown` / `start` / `stop`

**`read`、`write`、`exec` 根本不在列表中**——这不是编译标志缺失的问题，是 mGBA Lua API 本身没有这些功能。

pymgba-mcp 虽能通过 cffi 直接调用 mGBA C API（理论上可调 `mDebuggerAddBreakpoint`），但代码完全未实现。根本原因：**mGBA 没有通过任何脚本/绑定接口把"内存访问回调"暴露出来**。

### 要监听内存读取/断点，必须走的路

| 方案 | 监听读取 | 自动化 | Windows 可用 |
|------|:---:|:---:|:---:|
| mgba-live-mcp（本项目）| ❌ | ✅ | ✅ |
| pymgba-mcp | ❌ | ✅ | ⚠️ |
| mGBA GUI 调试器（Tools → Debugger → Watchpoints） | ✅ | ❌（手动） | ✅ |
| **GDB stub**（`-g` 开关 + `arm-none-eabi-gdb`）| ✅ | ✅ | ✅ |
| 扩展 pymgba-mcp | ✅（需开发） | ✅ | ⚠️ |

**当前项目推荐路径**：
- 日常自动化分析（VRAM 差分、内存轮询）→ **mgba-live-mcp**（本文档）
- 需要精确追踪 ROM 读取、硬件断点、watchpoint → **GDB stub**（[`gdb-debugging.md`](gdb-debugging.md)）

---

## 二、安装与 Claude Code CLI 注册

### 前提条件

| 组件 | 要求 |
|---|---|
| **mGBA** | **0.11+ 开发版**（`--script` 参数必须支持）。官方正式版 0.10.5 **不支持** `--script`，无法与 mgba-live-mcp 配合。下载 `mGBA-build-latest-win64.zip`（nightly），见 `LOCAL.md` |
| **uv** | Python 包管理器（`uv --version` 验证） |
| **GDB 10.2** | `tools/arm-none-eabi-gdb.exe`（如需 GDB 调试，见 [`gdb-debugging.md`](gdb-debugging.md)） |

### 本地 fork 方案（推荐，**2026-04-16 启用**）

为避免 uv cache 刷新反复丢 patch，`mgba-live-mcp` 已 fork 到本地，所有 patch 直接落在源码里，`uvx --from <本地路径>` 每次从该目录构建 wheel。

**目录与分支**：
```
D:\Software\mgba-live-mcp\       # git clone https://github.com/penandlim/mgba-live-mcp
  branch: local-patches           # 所有 patch 都提交在这一支
```

**Patch 列表**（均在 `local-patches` 分支，单 squash commit `af7dbc3`）：

| # | 位置 | 改动 | 作用 |
|---|------|------|------|
| 1 | `live_cli.py :: build_start_command` | 新增 `gdb_stub: bool = False` 参数（默认关闭），为真时追加 `"-g"`；`cmd_start` 从 `args.gdb_stub` 读取；argparse 暴露 `--gdb-stub`；MCP server `_build_start_command_args` 同步转发，`mgba_live_start` / `mgba_live_start_with_lua` 工具 schema 暴露 `gdb_stub: boolean` | 可配置 GDB stub（端口 2345），默认不开 |
| 2 | `live_cli.py :: pid_alive` | Windows 分支改走 `GetExitCodeProcess` / `STILL_ACTIVE`；补 `import sys` | 修复 Windows 下死会话无法回收 |
| 3 | `live_cli.py :: terminate_session_process` | Windows 分支改走 `taskkill /F /T /PID`（树杀） | 修复 `os.getpgid` / `os.killpg` 在 Windows 不存在导致 `mgba_live_stop` 崩溃 |
| 4 | `live_controller.py :: _run_command` | `create_subprocess_exec` 添加 `stdin=asyncio.subprocess.DEVNULL` | 防止子进程继承 MCP JSON-RPC stdin 管道导致挂起 |
| 5 | `live_cli.py + mgba_live_bridge.lua :: resolve_output_path` | 增加 Windows 绝对路径检查 `string.match(path, "^%a:[/\\]")` | 修复截图等工具的 `out` 参数拒识 `C:\...` |
| 6 | `pyproject.toml` | version bump 至 `0.3.2+local.N`（每次改源码递增） | 触发 uv 缓存重建（uv 在版本号不变时会复用旧 wheel） |

### `~/.claude.json` 配置形态

Claude Code CLI 的 MCP 配置不走 `settings.json`，而是写入 `~/.claude.json`。本项目使用 **project scope**，配置位于 `projects["E:/Workspace/yugioh-ex2006-re"].mcpServers`。本机具体路径（mGBA 目录、gdb-mcp dist 路径）见 `LOCAL.md`。

```json
"mcpServers": {
  "mgba": {
    "command": "uvx",
    "args": ["--reinstall", "--from", "D:\\Software\\mgba-live-mcp", "mgba-live-mcp"],
    "env": { "PATH": "<mGBA 目录>;<其余系统 PATH>" }
  },
  "gdb": {
    "command": "node",
    "args": ["<gdb-mcp dist 目录>\\index.js"]
  }
}
```

- **不再走 PyPI `uvx mgba-live-mcp`**：避免 uv cache 更新丢失 `gdb_stub` / Windows `pid_alive` / stdin DEVNULL / Windows 绝对路径四处 patch。
- **PATH 显式指定**：MCP server 一次性读取环境变量，注册表 PATH 修改对已运行 server 不生效；在 `env` 里显式指定可确保每次启动都能看到 mGBA。
- 写入后 **必须退出并重启 Claude Code CLI**，MCP server 进程才会加载。

### 与 Copilot CLI 并存

两份配置各自独立：Copilot 读 `~/.copilot/mcp-config.json`，Claude Code 读 `~/.claude.json`。共用 uv cache（fork 的 patches）和 `D:\Software\gdb-mcp\dist\`（GDB MCP 的 dist），无冲突。

### Smoke test（**2026-04-16 验证通过**）

| 步骤 | 工具 | 结果 |
|------|------|------|
| 1 | `mgba_live_start(rom="roms/2343.gba", savestate="roms/2343.ss1", gdb_stub=true)` | **报错** "Session created but bridge did not become ready before timeout"（预期，`gdb_stub=true` 下 `-g` 让 CPU 暂停在 reset vector）；session/PID 已创建，端口 2345 已 LISTEN。**默认 `gdb_stub=false` 不会报错、也不开 stub**。 |
| 2 | `mgba_live_status(all=true)` | `alive=true`, `heartbeat=null`（Lua bridge 未启动） |
| 3 | `gdb_init(gdbPath="tools/arm-none-eabi-gdb.exe")` | 初始化成功（**不传 `architecture` 参数**） |
| 4 | `gdb_connect(target="localhost:2345")` | 连接成功 |
| 5 | `gdb_evaluate_expression("$pc")` | `$pc = 0x3004fdc`（已加载 ss1 存档，不是 reset vector） |
| 6 | `gdb_continue` | 游戏继续执行 |
| 7 | `mgba_live_status` | `heartbeat.frame > 0`，截图正常 ✅ |

### 验证 fork 已生效

```bash
uvx --from "D:\Software\mgba-live-mcp" --with-editable "D:\Software\mgba-live-mcp" python -c "
from mgba_live_mcp import live_cli; import inspect
print('GDB_STUB PATCH:', 'gdb_stub' in inspect.getsource(live_cli.build_start_command))
print('WIN32 PATCH:', 'GetExitCodeProcess' in inspect.getsource(live_cli.pid_alive))
print('TASKKILL PATCH:', 'taskkill' in inspect.getsource(live_cli.terminate_session_process))
"
```
三项都应为 `True`。

### 迭代 patch 时的约束

- **修改源码后必须 bump 版本号**：`pyproject.toml` 中 `version = "0.3.2+local.N"` 的 `N` 递增。`uvx --reinstall` 在版本号不变时可能复用旧 wheel 缓存，bump 版本是唯一可靠的触发重建手段。
- 改 `live_controller.py` / `server.py`：这些代码运行在 MCP server 常驻进程内，bump 版本后还需**重启 Claude Code CLI** 才能加载。
- 改 `live_cli.py`：bump 版本 + 重启后生效（live_cli 作为子进程被 server 每次调用时 spawn）。
- 紧急热修：如需不重启立即生效，可直接 patch 当前 uv cache archive 里的 `live_cli.py`（通过错误信息中暴露的 Python 路径定位）。`live_cli.py` 改动由下次工具调用触发的新子进程加载，**无需重启**；`live_controller.py` 改动则必须重启。
- 拉上游更新：`git fetch && git rebase origin/main` 到 `local-patches` 分支，冲突手工解决，bump 版本号。

### 脚本启 mGBA 不能被 MCP 接管

`pwsh -File tools/mgba-scripts/start-mgba-gdb-ss1.ps1` 启动的 mGBA **无法**被 `mgba_live_attach` 接管：
```
PID is not a managed live session. Only processes started with mgba_live.py can be live-controlled.
```
脚本启动只适用于纯 GDB 场景（不需要 mGBA MCP 工具）；要同时用两套 MCP，**必须走 `mgba_live_start` 路径**。

---

## 三、MCP 工具参考（15 个）

全部 13 个核心工具已功能验证（**2026-04-13**），修复均已落在 fork 里。

| # | 工具 | 分类 | 状态 | 简述 |
|---|------|------|------|------|
| 1 | `mgba_live_start` | 会话 | ✅ | 启动 mGBA 并加载 ROM，建立受控 session（带 Lua bridge） |
| 2 | `mgba_live_start_with_lua` | 会话 | ✅ | 启动时立即执行 Lua（可在启动动画阶段监控） |
| 3 | `mgba_live_attach` | 会话 | ⚠️ | 仅接管 managed session（`mgba_live_start` 启动的） |
| 4 | `mgba_live_status` | 状态 | ✅ | 返回 `alive` / `frame` / 内联 base64 截图 |
| 5 | `mgba_live_stop` | 会话 | ✅ | 终止 session（fork 已修 Windows `os.getpgid` bug） |
| 6 | `mgba_live_input_tap` | 输入 | ✅ | 按下并释放一个按键（可选等待帧数，返回截图）|
| 7 | `mgba_live_input_set` | 输入 | ✅ | 持续按住按键（菜单滚动用）|
| 8 | `mgba_live_input_clear` | 输入 | ✅ | 释放按键（不传 `keys` 则释放全部）|
| 9 | `mgba_live_read_memory` | 内存 | ✅ | 读取一组离散地址的字节值 |
| 10 | `mgba_live_read_range` | 内存 | ✅ | 读取连续内存范围（返回字节数组）|
| 11 | `mgba_live_dump_oam` | 调试 | ✅ | 转储前 N 个精灵的 `attr0/1/2` + 原始字节 |
| 12 | `mgba_live_dump_entities` | 调试 | ✅ | 读取 N 个等长结构体（字节数组，由调用方解码）|
| 13 | `mgba_live_dump_pointers` | 调试 | ✅ | 转储指针表 |
| 14 | `mgba_live_run_lua` | Lua | ✅ | 在会话中执行任意 Lua，返回 `return` 值 |
| 15 | `mgba_live_export_screenshot` | 截图 | ✅ | 导出 PNG 到指定路径 + 内联 base64（fork 已修 Windows 绝对路径 bug）|

### 启动参数要点

- `fps_target`：默认 120；`fast=true` 等价于 600（快进模式）
- `gdb_stub`：默认 `false`；`true` 时在 mGBA 命令行追加 `-g`，stub 在端口 2345 LISTEN，但 **CPU 会暂停在 reset vector，必须 `gdb_connect` + `gdb_continue` 才能让 Lua bridge 初始化**（见 §一 Smoke test）
- `savestate`：加载快照（`.ss1` 等），启动后即跳到快照状态

### 典型调用

**启动 + 读 ROM header**：
```python
mgba_live_start(rom="roms/2343.gba", session_id="work")
mgba_live_read_range(start=0x080000A0, length=16, session="work")
# 返回: [89,85,71,73,79,72,87,67,84,48,54,0,0,0,0,0] → "YUGIOHWCT06\0\0\0\0\0"
```

**按键 + 等帧**：
```python
mgba_live_input_tap(key="START", frames=1, wait_frames=120, session="work")
# 返回内联截图，确认已进入主菜单
```

**Dump 结构体**（Dragon's Roar 预组，GBA 地址 `0x09E5FA58`）：
```python
mgba_live_dump_entities(base=0x09E5FA58, size=4, count=28, session="work")
# 返回 28 项 4B 数组，按 deck_entry 规则解码（so_code=value>>2, copies=value&3）
```

### 会话运行时

- 会话文件存储于 `~/.mgba-live-mcp/runtime/sessions/<session_id>/`
- `session.json`（含 PID）、`scripts/mgba_live_bridge.lua`（核心桥接）
- 崩溃的会话自动归档到 `runtime/archived_sessions/`
- `_G` 全局状态在同一 session 生命周期内持久；重启 session 清零

---

## 四、Lua 脚本教程

### 执行环境

每次 `mgba_live_run_lua` 调用在 mGBA Lua 解释器中**一次性执行**，但全局变量（`_G` 表）在多次调用之间**持久保留**：

```lua
-- 第一次调用：存储数据
_G._my_data = {frame = emu:currentFrame(), value = 42}
return "saved"

-- 第二次调用：读取数据
return _G._my_data.frame  -- 返回之前存的帧号
```

> ⚠️ MCP server 重启后全局变量清零。

### 常用 API

```lua
-- 读取内存（字节/16位/32位）
local b  = emu:read8(addr)
local hw = emu:read16(addr)
local w  = emu:read32(addr)

-- 写入内存
emu:write8(addr, value)
emu:write16(addr, value)
emu:write32(addr, value)

-- 当前帧号
emu:currentFrame()

-- 读寄存器
emu:getRegister("r0")   -- "r0"-"r15" / "pc" / "lr" / "sp" / "cpsr"

-- 按键模拟（bitmask：A=1, B=2, SELECT=4, START=8, RIGHT=16, LEFT=32, UP=64, DOWN=128, R=256, L=512）
emu:setKeys(bitmask)

-- 截图（可传绝对路径）
emu:screenshot("C:\\temp\\frame.png")

-- 注册帧回调（有效！每帧触发）
callbacks:add("frame", function()
    _G._frame_count = (_G._frame_count or 0) + 1
end)
```

### 回调系统的设计限制

mGBA Lua 只支持：`alarm` / `crashed` / **`frame`** / `keysRead` / `reset` / `savedataUpdated` / `sleep` / `shutdown` / `start` / `stop`。

**`read`、`write`、`exec` 根本不在此列**。

| 行为 | 原因 |
|------|------|
| `callbacks:add("read", fn)` 注册不报错但从不触发 | `callbacks:add` 接受任意字符串，注册了一个永远不会触发的事件，静默失效 |
| `callbacks:add("memory.read", fn, base, size)` 报错 | 参数数量不匹配 C 函数签名，直接抛出异常 |
| `callbacks:add("frame", fn)` 有效 | 在官方支持列表中 |

> **关于 CMake 标志**：mgba-live-mcp 文档要求的 `-DENABLE_SCRIPTING=ON -DUSE_LUA=ON` 是启用 Lua **运行环境**的前提条件，不加这些标志根本无法运行任何 Lua 脚本。但即使正确编译，内存读写回调也不是 mGBA Lua API 的功能，标志不影响这一限制。

### 回调有效性汇总（实测）

| 回调类型 | 注册时报错 | 实际触发 | 说明 |
|---------|-----------|---------|------|
| `frame` | 否 | **有效** | 每帧触发，是唯一可靠的回调类型 |
| `write` | 否 | 无效 | GBA DMA 写 VRAM 不经过 CPU 内存回调系统 |
| `read` | 否 | 无效 | 即使 Lua 主动调用 `emu:read8()` 也不触发 |
| `memory.read` | 否 | 无效 | 同上 |
| `memory.write` | 否 | 无效 | 同上 |
| `exec` | 否 | 无效 | 指令执行回调注册成功但不触发 |
| `crashed` / `reset` | 否 | 未验证 | - |

> **规律**：所有回调类型均可注册（不报错），但只有 `frame` 实际有效。

### `emu:runFrame()` 在脚本中无效

```
Function called from invalid context
```
mGBA Lua 脚本运行在帧回调上下文中，不允许递归触发帧推进。用 `input_tap` 的 `frames` / `wait_frames` 参数或 `fast=true` 推进帧。

---

## 五、GBA 内存地址速查

| 地址 | 区域 | 说明 |
|------|------|------|
| `0x04000000` | IO | DISPCNT（显示控制） |
| `0x04000008` | IO | BG0CNT（+2=BG1, +4=BG2, +6=BG3） |
| `0x040000D0` | IO | DMA3SAD（DMA3 源地址） |
| `0x040000D4` | IO | DMA3DAD（DMA3 目标） |
| `0x040000D8` | IO | DMA3CNT_L（传输字数） |
| `0x040000DA` | IO | DMA3CNT_H（控制，写入此寄存器触发 DMA） |
| `0x05000000` | Palette RAM | BG 调色板（0x200 字节） |
| `0x05000200` | Palette RAM | OBJ 调色板（0x200 字节） |
| `0x06000000` | VRAM | 视显存（96 KB，char/map/bitmap） |
| `0x07000000` | OAM | 精灵属性内存（1 KB，128 个精灵） |
| `0x02000000` | EWRAM | 外部工作 RAM（256 KB，游戏状态） |
| `0x03000000` | IWRAM | 内部工作 RAM（32 KB，栈/临时数据） |
| `0x08000000` | ROM | 游戏 ROM（镜像，只读）|

### VRAM 布局（BG 模式 0 下）

计算公式：
- `tile_base = 0x06000000 + char_block × 0x4000`
- `map_base  = 0x06000000 + map_block × 0x800`

| char_block | 地址 | map_block | 地址 |
|-----------|------|-----------|------|
| 0 | `0x06000000` | 0 | `0x06000000` |
| 1 | `0x06004000` | 8 | `0x06010000`（危险：与 char_block 2 重叠） |
| 2 | `0x06008000` | 28 | `0x06037000` |
| 3 | `0x0600C000` | 30 | `0x0600F000` |
| - | - | 31 | `0x0600F800` |

### BG Map 条目格式（16 位）

```
Bits 15-14: 纵向/横向翻转标志
Bits 13-12: 调色板编号（16 色模式）
Bits  9-0 : tile 编号
```

### OAM 条目解码（`attr0/1/2` 三个 u16）

```
attr0: Y (8) | rot/scale (2) | mode (2) | mosaic (1) | 256-color (1) | shape (2)
attr1: X (9) | rot/scale param (5) | size (2)
attr2: tile name (10) | priority (2) | palette number (4)
```

### GBA BIOS 压缩块头

所有通过 BIOS SWI 解压的数据块都以固定 4 字节头部开始：

```
字节 +0：压缩类型魔数
    0x10 = LZ77（BIOS SWI 0x11）
    0x20 = Huffman（BIOS SWI 0x13）
    0x30 = RLE（BIOS SWI 0x14）
字节 +1~+3：解压后大小（24 位小端整数）
```

> ⚠️ 在 `asm/all.s` 中 **grep `svc`，不要搜 `swi`**。ARM 从 v7 起 SWI 指令重命名为 SVC，Ghidra 统一使用新助记符。

---

## 六、典型分析流程（Lua 脚本模板）

### 6.1 分析页面切换时的 VRAM 变化

**目标**：按下 A 键进入卡牌详情页时，记录 VRAM 发生了什么变化。

**步骤 1：读取 DISPCNT 确定显示模式**
```lua
local dispcnt = emu:read16(0x04000000)
local mode = dispcnt & 0x7
local bg_enable = (dispcnt >> 8) & 0xF
return string.format("DISPCNT=0x%04X mode=%d BG(0-3)=%s%s%s%s",
    dispcnt, mode,
    (bg_enable&1)>0 and "0" or "-",
    (bg_enable&2)>0 and "1" or "-",
    (bg_enable&4)>0 and "2" or "-",
    (bg_enable&8)>0 and "3" or "-")
```

**步骤 2：快照按键前 BG map**
```lua
_G._before_map = {}
for i = 0, 8191 do
    _G._before_map[i] = emu:read16(0x06000000 + i * 2)
end
return "快照已保存"
```

**步骤 3**：通过 `mgba_live_input_tap(key="A", frames=1, wait_frames=120)` 按键等帧。

**步骤 4：对比差异**
```lua
local changes = {bg0=0, bg1=0, bg2=0, bg3=0}
local samples = {}
for i = 0, 8191 do
    local addr = 0x06000000 + i * 2
    local after = emu:read16(addr)
    if after ~= _G._before_map[i] then
        local region = math.floor(i / 2048)
        local keys = {"bg0","bg1","bg2","bg3"}
        changes[keys[region+1]] = changes[keys[region+1]] + 1
        if #samples < 5 then
            table.insert(samples, string.format("0x%08X: %04X->%04X", addr, _G._before_map[i], after))
        end
    end
end
return string.format("BG0:%d BG1:%d BG2:%d BG3:%d\nSamples: %s",
    changes.bg0, changes.bg1, changes.bg2, changes.bg3,
    table.concat(samples, "\n"))
```

### 6.2 读取 BG 控制寄存器

```lua
local result = {}
local bgnames = {"BG0","BG1","BG2","BG3"}
for i = 0, 3 do
    local bgcnt = emu:read16(0x04000008 + i * 2)
    local priority   = bgcnt & 0x3
    local char_block = (bgcnt >> 2) & 0x3   -- 每块 16 KB，tile 数据起始
    local color256   = (bgcnt >> 7) & 0x1   -- 0=16 色, 1=256 色
    local map_block  = (bgcnt >> 8) & 0x1F  -- 每块 2 KB，地图数据起始
    local size       = (bgcnt >> 14) & 0x3
    local tile_base = 0x06000000 + char_block * 0x4000
    local map_base  = 0x06000000 + map_block * 0x800
    table.insert(result, string.format(
        "%s CNT=0x%04X pri=%d tiles@0x%08X map@0x%08X %s size=%d",
        bgnames[i+1], bgcnt, priority, tile_base, map_base,
        color256==1 and "256色" or "16色", size))
end
return table.concat(result, "\n")
```

### 6.3 读取 BG 地图并可视化

```lua
-- 读取 BG3 地图（30 列×20 行，分析文字布局）
local map_base = 0x0600F800
local result = {"BG3 Map (tile index, rows 0-19):"}
for row = 0, 19 do
    local tiles = {}
    for col = 0, 29 do
        local entry = emu:read16(map_base + (row * 32 + col) * 2)
        local tile_idx = entry & 0x3FF
        table.insert(tiles, string.format("%3d", tile_idx))
    end
    table.insert(result, string.format("row%02d: %s", row, table.concat(tiles, " ")))
end
return table.concat(result, "\n")
```

### 6.4 读取 tile 像素数据（4bpp）

```lua
-- 读取 BG3 tile 16，16 色（32 字节/tile），每字节存 2 像素（低 nibble 在前）
local function read_tile_4bpp(tile_idx, char_block_addr)
    local addr = char_block_addr + tile_idx * 32
    local rows = {}
    for row = 0, 7 do
        local pixels = {}
        for b = 0, 3 do
            local byte = emu:read8(addr + row * 4 + b)
            table.insert(pixels, string.format("%X%X", byte & 0xF, (byte >> 4) & 0xF))
        end
        table.insert(rows, table.concat(pixels))
    end
    return table.concat(rows, "|")
end

local result = {}
for i = 16, 27 do
    table.insert(result, string.format("tile%d: %s", i, read_tile_4bpp(i, 0x06008000)))
end
return table.concat(result, "\n")
```

### 6.5 分析 OAM（精灵）

```lua
-- 读取前 32 个精灵的 OAM 条目
local result = {"OAM Entries:"}
for i = 0, 31 do
    local base = 0x07000000 + i * 8
    local attr0 = emu:read16(base)
    local attr1 = emu:read16(base + 2)
    local attr2 = emu:read16(base + 4)

    local y      = attr0 & 0xFF
    local mode   = (attr0 >> 8) & 0x3   -- 0=正常 2=隐藏
    local shape  = (attr0 >> 14) & 0x3
    local x      = attr1 & 0x1FF
    local size   = (attr1 >> 14) & 0x3
    local tile   = attr2 & 0x3FF
    local pal    = (attr2 >> 12) & 0xF

    if mode ~= 2 then
        table.insert(result, string.format(
            "spr%02d: y=%3d x=%3d tile=%4d pal=%d shape=%d size=%d",
            i, y, x, tile, pal, shape, size))
    end
end
return table.concat(result, "\n")
```

### 6.6 搜索 ROM 中的原始字节（未压缩数据）

```lua
local function search_rom(pattern, start_addr, length)
    local plen = #pattern
    local results = {}
    local rom_base = 0x08000000
    for offset = 0, length - plen, 2 do
        local addr = rom_base + start_addr + offset
        local match = true
        for i = 1, plen do
            if emu:read8(addr + i - 1) ~= pattern[i] then
                match = false
                break
            end
        end
        if match then
            table.insert(results, string.format("ROM+0x%X (GBA 0x%08X)", start_addr + offset, addr))
            if #results >= 5 then break end
        end
    end
    return #results > 0 and table.concat(results, "\n") or "未找到"
end

-- 示例：搜索某 tile 前 4 字节
return search_rom({0x22, 0x22, 0x22, 0x22}, 0, 0x200000)
```

### 6.7 枚举 ROM 中的 GBA BIOS 压缩块

当 tile 数据搜索失败（原始字节在 ROM 中找不到），说明数据是压缩存储的。扫描 BIOS 压缩头：

```lua
local function find_compressed_blocks(scan_start, scan_len, min_size, max_size)
    local rom_base = 0x08000000
    local magic_names = {[0x10]="LZ77", [0x20]="Huffman", [0x30]="RLE"}
    local results = {}
    for offset = scan_start, scan_start + scan_len - 4, 4 do
        local b0 = emu:read8(rom_base + offset)
        local magic = magic_names[b0]
        if magic then
            local sz = emu:read8(rom_base + offset + 1)
                     + emu:read8(rom_base + offset + 2) * 0x100
                     + emu:read8(rom_base + offset + 3) * 0x10000
            if sz >= min_size and sz <= max_size then
                table.insert(results, string.format(
                    "ROM+0x%X  type=%-7s  decomp=%d bytes (%.1fKB)",
                    offset, magic, sz, sz / 1024))
            end
        end
    end
    return #results > 0 and table.concat(results, "\n") or "未找到符合条件的压缩块"
end

-- 示例：在 ROM 前 2 MB 中找所有解压后 > 32 KB 的压缩块
return find_compressed_blocks(0, 0x200000, 0x8000, 0x200000)
```

**实际发现**（本项目）：

| ROM 偏移 | 类型 | 解压大小 | 推测内容 |
|---------|------|---------|---------|
| `0x114A90` | Huffman | ~528 KB | 日文字体 tile 集（528 KB ÷ 32 字节/tile ≈ 16,512 字符）|

---

## 七、Windows 特殊修复历史

所有修复已落入本地 fork（见 §二），以下是每个 bug 的根因分析，供未来排错参考。

### 7.1 `pid_alive()` 在 Windows 下误判进程状态

**现象**：调用 `mgba_live_status` 时，已死亡的 session 仍被识别为"存活"，后续 `start` 报告会话冲突。

**原因**：原始代码使用 `os.kill(pid, 0)` 检测进程：
- Unix：向进程发送信号 0，进程不存在抛 `ProcessLookupError`
- Windows：行为不一致——Python 的 Popen 对象持有已退出进程的句柄时，`os.kill(pid, 0)` 对该 PID 仍可能返回成功

**修复**：改用 Win32 API 的 `GetExitCodeProcess`，检查退出码是否为 `STILL_ACTIVE (259)`：

```python
def pid_alive(pid: int) -> bool:
    if sys.platform == "win32":
        import ctypes, ctypes.wintypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
        if handle == 0:
            return False
        try:
            exit_code = ctypes.wintypes.DWORD()
            if ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                return exit_code.value == STILL_ACTIVE
            return False
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
```

### 7.2 `terminate_session_process` 使用 Unix 专属 API

**现象**：调用 `mgba_live_stop` 抛 `AttributeError: module 'os' has no attribute 'getpgid'`。

**原因**：`os.getpgid` / `os.killpg` 是 POSIX 进程组 API，Windows 不支持。

**修复**：`sys.platform == "win32"` 分支改走 `taskkill /F /T /PID`（树杀）或 `TerminateProcess`。

### 7.3 MCP server 子进程继承 stdin 管道导致挂起

**现象**：`mgba_live_start` 等工具调用持续超时（20 秒），STDOUT/STDERR 均为空。

**原因**：`live_controller.py` 的 `asyncio.create_subprocess_exec` 未指定 `stdin`，子进程默认**继承父进程（MCP server）的 stdin**。MCP server 的 stdin 是与 CLI 通信的 JSON-RPC 管道——子进程继承后尝试从管道读取而永久阻塞。

**修复**：添加 `stdin=asyncio.subprocess.DEVNULL`：
```python
proc = await asyncio.create_subprocess_exec(
    *proc_args,
    stdin=asyncio.subprocess.DEVNULL,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    env={**os.environ},
)
```

### 7.4 `resolve_output_path` 不识别 Windows 绝对路径

**现象**：`export_screenshot(out="C:\\temp\\screen.png")` 写入到 `session_dir\C:\temp\screen.png`。

**原因**：`mgba_live_bridge.lua` 只检查 Unix 绝对路径（`/` 前缀），Windows 路径被误判为相对路径，拼接上 session 目录前缀。

**修复**：
```lua
-- 新增 Windows 绝对路径检查
if string.sub(path, 1, 1) == "/" or string.match(path, "^%a:[/\\]") then
    return path
end
```

### 7.5 MCP server 进程未继承注册表新 PATH

**现象**：将 mGBA 加入用户 PATH 注册表后，手动运行 live_cli 成功，但 MCP 工具仍超时 `No mGBA binary found`。

**原因**：Copilot CLI / Claude Code CLI 的 MCP server 子进程在启动时一次性读取环境变量，后续对注册表 PATH 的修改对**已运行的 server 进程不生效**。

**修复**：在 `mcp-config.json` / `~/.claude.json` 的 `env` 字段中显式指定 PATH（见 §二配置形态）。

### 7.6 `-g` patch 回归问题（旧坑，已由本地 fork 根治）

**旧现象**：`mgba_live_start` 成功返回，但 `netstat :2345` 无 LISTEN，`gdb_connect` 报 `Connection timed out`。

**根因**：uv 缓存更新后，`archive-v0/` 下出现新的 archive，MCP server 切换使用新 archive 的 `live_cli.py`——**不再是打过 `-g` patch 的旧版本**。

**根治**：改用本地 fork（见 §二），patch 直接落到本地源码仓库。

### 7.7 uv 缓存 archive 位置与硬链接共享

```
C:\Users\<username>\AppData\Local\uv\cache\archive-v0\<hash>\
```
有两个相关 archive：
- `H-avPZ5DfJEF8r9VXxrqe\`：完整 venv（含 Python 解释器、site-packages）
- `5zGOx6CDrJNGtKdrIueX5\`：仅包文件（wheel 格式，与前者通过硬链接共享源码）

MCP 服务器进程（持久运行）加载代码后驻留内存。两个 archive 通过硬链接共享同一份源码，**修改任一个另一个同步变更**。但新建 session 时 `mgba_live_bridge.lua` 也会复制到 session 目录，该副本需单独修改。

### 7.8 `emu:runFrame()` 在 Lua 回调上下文中无效

**现象**：`run_lua` 执行 `emu:runFrame()` 报 `Function called from invalid context`。

**原因**：mGBA Lua 脚本运行在帧回调上下文中，不允许递归触发帧推进。

**绕过**：用 `input_tap` 的 `frames` / `wait_frames` 参数，或 `fast=true` 控制速度。

---

## 八、相关文档

| 文件 | 说明 |
|------|------|
| [`gdb-debugging.md`](gdb-debugging.md) | GDB stub + GDB MCP 调试指南（断点/watchpoint） |
| `CLAUDE.md` §调试工具链 | 顶层场景决策：何时用 mGBA MCP / GDB / batch 脚本 |
| `LOCAL.md` | 本机路径（mGBA 目录、gdb-mcp dist 路径，未入库） |
| `D:\Software\mgba-live-mcp\` | 本地 fork 仓库（分支 `local-patches`） |
