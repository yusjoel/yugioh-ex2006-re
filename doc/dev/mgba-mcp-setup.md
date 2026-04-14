# mGBA MCP 动态调试环境搭建

本文记录为《游戏王 EX2006》反汇编项目配置 mGBA MCP 动态调试环境的过程。

---

## 一、背景

静态反汇编分析遇到瓶颈时，需要借助模拟器进行动态分析，验证内存布局、寄存器状态、
函数调用流程等。通过 [mgba-live-mcp](https://github.com/penandlim/mgba-live-mcp)，
可以将 mGBA 模拟器接入 MCP（Model Context Protocol），使 AI 工具能够直接控制模拟器
进行动态分析。

---

## 二、工具说明

### mGBA

- **版本要求**：**0.11+ 开发版**（`--script` 参数从 0.11 开始支持）
- **实际使用版本**：mGBA build-latest-win64（2026-04-09）
- **安装路径**：`<mGBA安装目录>\mGBA.exe`（见 `LOCAL.md`）
- **注意**：官方正式版 0.10.5 **不支持** `--script` 参数，无法与 mgba-live-mcp 配合

### mgba-live-mcp

- **项目地址**：https://github.com/penandlim/mgba-live-mcp
- **运行方式**：通过 `uvx` 启动，以 stdio 模式运行的 MCP 服务器
- **依赖**：[uv](https://docs.astral.sh/uv/)（Python 包管理器）

### 提供的 MCP 工具（共 15 个）

| 类别 | 工具名 | 说明 |
|------|--------|------|
| 会话管理 | `mgba_live_start` | 启动 mGBA 并加载 ROM |
| | `mgba_live_start_with_lua` | 启动并立即执行 Lua 脚本 |
| | `mgba_live_attach` | 连接已有会话 |
| | `mgba_live_status` | 查看会话状态（含截图） |
| | `mgba_live_stop` | 停止会话 |
| 输入控制 | `mgba_live_input_tap` | 模拟按键（A/B/START 等） |
| | `mgba_live_input_set` | 持续按住按键 |
| | `mgba_live_input_clear` | 释放按键 |
| 内存读取 | `mgba_live_read_memory` | 读取指定地址列表 |
| | `mgba_live_read_range` | 读取连续内存区间 |
| | `mgba_live_dump_pointers` | 转储指针表 |
| | `mgba_live_dump_oam` | 转储 OAM 精灵表 |
| | `mgba_live_dump_entities` | 转储实体结构 |
| Lua 脚本 | `mgba_live_run_lua` | 在运行中的会话执行 Lua |
| 截图 | `mgba_live_export_screenshot` | 导出截图到文件 |

---

## 三、安装步骤

### 前提条件

- 已安装 mGBA **0.11+ 开发版**（`--script` 参数必须支持）
- 已安装 `uv`（验证：`uv --version`）

### 1. 将 mGBA 加入 PATH

mgba-live-mcp 通过 `shutil.which("mGBA")` 自动查找 mGBA，**必须将 mGBA 目录加入系统 PATH**：

```powershell
# PowerShell（永久写入用户 PATH）
$current = (Get-ItemProperty "HKCU:\Environment" -Name "Path").Path
Set-ItemProperty "HKCU:\Environment" -Name "Path" -Value "<mGBA安装目录>;$current"
```

或手动在「系统属性 → 环境变量 → 用户变量 → Path」中添加 `<mGBA安装目录>`。

> 修改后需**重启 Copilot CLI**（及所有终端窗口）使 PATH 生效。

### 2. 配置 MCP 服务器

GitHub Copilot CLI 从 `~/.copilot/mcp-config.json` 读取 MCP 服务器配置。
创建该文件（若已存在则合并 `mcpServers` 字段）：

**`C:\Users\<用户名>\.copilot\mcp-config.json`**

```json
{
  "mcpServers": {
    "mgba": {
      "command": "uvx",
      "args": ["mgba-live-mcp"]
    }
  }
}
```

配置完成后**重启 Copilot CLI** 使其生效。

---

## 四、Windows 排障记录

本节记录配置过程中遇到的所有问题及解决方案，供日后参考。

---

### 问题 1：mGBA 0.10.5 不支持 `--script` 参数

**现象**：启动 MCP 工具后，mGBA 进程异常退出，日志显示不认识 `--script` 参数。

**原因**：`--script`（Lua 脚本注入）从 mGBA **0.11** 开始才支持，官方预编译的
0.10.5 不包含此功能。

**解决方案**：下载 mGBA 开发版（nightly build）替换旧版本。

- 下载地址：https://mgba.io/downloads.html → "Development Builds"
- 使用版本：`mGBA-build-latest-win64.zip`（2026-04-09，含 `mGBA.exe` 和 `mgba-sdl.exe`）
- 安装路径：`<mGBA安装目录>\`（见 `LOCAL.md`）

验证是否支持 `--script`：
```powershell
& "<mGBA安装目录>\mGBA.exe" --help | Select-String "script"
# 输出：--script FILE  Run a script on start. Can be passed multiple times
```

---

### 问题 2：mGBA 不在 PATH 中导致 CLI 无法启动

**现象**：MCP 工具 `mgba_live_start` 调用后返回超时错误（20 秒），或
`Command failed (exit 1): No mGBA binary found in PATH`。

**原因**：`mgba-live-mcp` 的 `detect_mgba_binary()` 函数通过 `shutil.which()` 在
系统 PATH 中查找 `mGBA`/`mgba`/`mgba-qt`，找不到时立即退出。

MCP 工具的 `mgba_path` 参数为**可选项**，缺省时依赖 PATH，不会自动使用上次指定的路径。

**解决方案**：将 mGBA 目录永久加入用户 PATH：

```powershell
$current = (Get-ItemProperty "HKCU:\Environment" -Name "Path").Path
Set-ItemProperty "HKCU:\Environment" -Name "Path" `
    -Value "<mGBA安装目录>;$current" `
    -Type ExpandString
```

> PATH 写入注册表后，需重启 Copilot CLI 使 MCP 服务器进程继承新 PATH。

---

### 问题 3：`pid_alive()` 在 Windows 下误判进程状态

**现象**：调用 `mgba_live_status` 时，已死亡的会话仍被识别为"存活"，
导致旧会话无法清理，后续 `start` 命令报告会话冲突。

**原因**：原始代码使用 `os.kill(pid, 0)` 检测进程：
- 在 Unix 上：向进程发送信号 0（测试信号），进程不存在则抛 `ProcessLookupError`
- 在 Windows 上：行为不一致——Python 的 Popen 对象持有已退出进程的句柄时，
  `os.kill(pid, 0)` 对该 PID 仍可能返回成功，造成误判

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
            return False  # 进程不存在或无权限
        try:
            exit_code = ctypes.wintypes.DWORD()
            if ctypes.windll.kernel32.GetExitCodeProcess(
                    handle, ctypes.byref(exit_code)):
                return exit_code.value == STILL_ACTIVE
            return False
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    # Unix fallback
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
```

**修改位置**：uv 缓存中的 `live_cli.py`。
由于 uv 使用**硬链接**在两个 archive 之间共享文件，修改一处即同时生效：

```
C:\Users\<username>\AppData\Local\uv\cache\archive-v0\
  <hash1>\Lib\site-packages\mgba_live_mcp\live_cli.py  ← 已修改
  <hash2>\mgba_live_mcp\live_cli.py                     ← 硬链接，自动同步
```

> **注意**：uv 缓存文件会在 `uv cache clean` 或包更新时被覆盖，届时需重新应用此修复。

---

### 问题 4：MCP server 进程未继承注册表新增的 PATH

**现象**：将 mGBA 加入用户 PATH 注册表后，手动在终端运行 live_cli 成功，但 MCP 工具
调用仍然超时（`No mGBA binary found`）。

**原因**：Copilot CLI 及其 MCP server 子进程在启动时一次性读取环境变量。后续对注册表
PATH 的修改对**已运行的 MCP server 进程不生效**，只有下次启动时才会读到新 PATH。
但如果 PATH 变更与 Copilot CLI 安装/更新时机不同步，server 进程可能仍然使用旧 PATH。

**解决方案**：在 `mcp-config.json` 的 `env` 字段中显式指定 PATH，确保 MCP server
启动时一定能看到 mGBA 路径：

**`C:\Users\<用户名>\.copilot\mcp-config.json`**

```json
{
  "mcpServers": {
    "mgba": {
      "command": "uvx",
      "args": ["mgba-live-mcp"],
      "env": {
        "PATH": "D:\\Software\\mGBA-build-latest-win64;<其余 PATH 内容>"
      }
    }
  }
}
```

> 将 mGBA 路径放在 PATH 最前面，修改后重启 Copilot CLI 生效。

---

### 问题 5：`live_controller.py` 子进程继承 MCP stdin 管道导致挂起

**现象**：`mgba_live_start` 等工具调用持续超时（20 秒），STDOUT/STDERR 均为空，
重启后手动执行 live_cli 正常。

**原因**：`live_controller.py` 使用 `asyncio.create_subprocess_exec` 启动 live_cli
子进程时，未指定 `stdin`，子进程默认**继承父进程（MCP server）的 stdin**。
MCP server 的 stdin 是与 Copilot CLI 通信的 JSON-RPC 管道——live_cli 子进程继承后
尝试从管道读取而永久阻塞，永远无法输出结果。

**修复**：在 `live_controller.py` 的 `asyncio.create_subprocess_exec` 调用中
添加 `stdin=asyncio.subprocess.DEVNULL`：

```python
proc = await asyncio.create_subprocess_exec(
    *proc_args,
    stdin=asyncio.subprocess.DEVNULL,   # ← 新增，防止继承 MCP 管道
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    env={**os.environ},
)
```

**修改位置**：uv 缓存中的 `live_controller.py`（约第 39 行）：

```
C:\Users\<username>\AppData\Local\uv\cache\archive-v0\<hash>\
  Lib\site-packages\mgba_live_mcp\live_controller.py
```

> 此文件运行在 MCP server 持久进程中，修改后需重启 Copilot CLI 才能生效。

---

### 附：uv 缓存文件修改的注意事项

mgba-live-mcp 通过 `uvx` 运行时，代码存放在 uv 缓存目录：

```
C:\Users\<username>\AppData\Local\uv\cache\archive-v0\<hash>\
```

有两个相关 archive：
- `H-avPZ5DfJEF8r9VXxrqe\`：完整 venv（含 Python 解释器、site-packages）
- `5zGOx6CDrJNGtKdrIueX5\`：仅包文件（wheel 格式，与前者通过硬链接共享源码）

MCP 服务器进程（持久运行）加载代码后驻留内存，**修改磁盘文件不影响已启动的服务器**。
对 `live_controller.py`、`server.py` 的修改需重启 Copilot CLI 才能生效；
对 `live_cli.py` 的修改在下次工具调用时由新的子进程加载，**无需重启**。

---

## 五、使用方法

### 启动 ROM

mGBA 已加入 PATH 后，无需手动指定路径：

```json
{
  "rom": "E:\\Workspace\\yugioh-ex2006-re\\roms\\2343.gba"
}
```

### 读取内存

```json
{
  "session": "<session_id>",
  "start": 134217728,
  "length": 256
}
```

> GBA ROM 基址为 `0x08000000`（十进制 `134217728`）。
> IWRAM 基址为 `0x03000000`，EWRAM 基址为 `0x02000000`。

### 执行 Lua 脚本

```lua
-- 示例：读取当前帧号
return emu:currentFrame()
```

```lua
-- 示例：读取指定地址的 32 位值
return emu:read32(0x03001234)
```

### 快速运行（加速模式）

```json
{
  "rom": "E:\\Workspace\\yugioh-ex2006-re\\roms\\2343.gba",
  "fast": true
}
```

`fast: true` 等同于 `fps_target: 600`，适合快速跳过片头等场景。

---

## 六、运行时说明

- 会话文件存储于 `~/.mgba-live-mcp/runtime/`
- 崩溃的会话自动归档到 `~/.mgba-live-mcp/runtime/archived_sessions/`
- 大多数工具调用会自动返回截图（内嵌于响应中）
- 需要持久化截图时使用 `mgba_live_export_screenshot` 并指定 `out` 路径

---

## 七、Claude Code CLI 注册（2026-04-14）

Claude Code CLI 的 MCP 配置不走 `settings.json`，而是写入 `~/.claude.json`（全局或项目级）。
本项目使用 **project scope**，配置块位于 `~/.claude.json` → `projects` → `E:/Workspace/yugioh-ex2006-re` → `mcpServers`。

### 配置片段

本机具体路径见 `LOCAL.md`（mGBA 目录、gdb-mcp dist 路径）。配置形态：

```json
"mcpServers": {
  "mgba": {
    "command": "uvx",
    "args": ["mgba-live-mcp"],
    "env": { "PATH": "<mGBA 目录>;<其余系统 PATH>" }
  },
  "gdb": {
    "command": "node",
    "args": ["<gdb-mcp dist 目录>\\index.js"]
  }
}
```

写入后 **必须退出并重启 Claude Code CLI**，MCP server 进程才会加载。

### Smoke test（2026-04-14 验证通过）

| 步骤 | 工具 | 结果 |
|------|------|------|
| 1 | `mgba_live_start(rom="roms/2343.gba")` | 超时报错（预期，因 `-g` patch 让游戏启动时暂停），但 session PID 已创建 |
| 2 | `mgba_live_status` | `alive=true`, `heartbeat=null`（游戏待 GDB 放行） |
| 3 | `gdb_init(gdbPath="tools/arm-none-eabi-gdb.exe")` | 初始化成功（**不传 `architecture` 参数**） |
| 4 | `gdb_connect(target="localhost:2345")` | 连接成功 |
| 5 | `gdb_evaluate_expression("$pc")` | `$pc = 0x0`（reset vector） |
| 6 | `gdb_continue` | 游戏开始运行 |
| 7 | `mgba_live_read_range(0x080000A0, 16)` | 返回 `YUGIOHWCT06\0BY6E` ✅ |
| 8 | `mgba_live_status` | 有截图，标题画面 ✅ |

### 与 Copilot CLI 并存

两份配置各自独立：Copilot 读 `~/.copilot/mcp-config.json`，Claude Code 读 `~/.claude.json`。
共用 uv cache（mgba-live-mcp 的 patches）和 `D:\Software\gdb-mcp\dist\`（GDB MCP 的 dist），
无冲突。

### 重要约束重申

- **GDB 版本必须 10.2**（`tools/arm-none-eabi-gdb.exe`），devkitPro 14.1 与 mGBA stub 协议不兼容。
- `gdb_init` **不要传 `architecture` 参数**，否则 GDB MCP 会用默认 aarch64 或走到 devkitPro 14.1。
- mGBA `-g` stub **一次性**，GDB 断开后永久关闭，每次调试循环需 `mgba_live_stop` + 重新 `start`。
- 本机 uv cache 中的 `live_cli.py` 包含手工插入的 `-g` 参数（在 `build_start_command`），
  使 `mgba_live_start` 启动时自带 GDB stub；因此 `mgba_live_start` 总会超时（游戏被暂停），
  需要 `gdb_connect` + `gdb_continue` 才能让 Lua bridge 初始化。如果只用 mGBA 不用 GDB，
  仍需走一遍 GDB 放行流程，或回退 `live_cli.py` 的 patch。

