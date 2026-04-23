# GDB 调试指南（mGBA GDB Stub + GDB MCP）

本文档是本项目使用 `arm-none-eabi-gdb` 通过 mGBA GDB stub 做动态调试的统一参考，涵盖：工具链要求、三种调试方式、Windows 进程管理、断点/watchpoint 能力矩阵、12 个已知坑与 workaround、DMA3 walkthrough PoC、GDB MCP 集成细节。

> **mGBA MCP（Lua bridge）调试**参见 [`mgba-mcp.md`](mgba-mcp.md)。本文只讲 GDB。

---

## 一、工具链要求

### 1.1 GDB 版本：必须 10.2

**必须使用 `tools/arm-none-eabi-gdb.exe`（GDB 10.2）**，不能用 devkitARM 自带的 GDB 14.1。

GDB 14.x 修改了 RSP 协议中的若干细节（vFile、qXfer、multiprocess 等），mGBA 0.10.x stub 未跟进这些变化，握手阶段就会失败或断点/watchpoint 完全无效。GDB 10.2 可直接连接，无需代理。

**常见错误表现**：
- 14.1：连接握手失败，或设置的断点/watchpoint 无效
- **调用 `gdb_init` 时必须指定 `gdbPath="tools/arm-none-eabi-gdb.exe"`，且不能传 `architecture` 参数**，否则 GDB MCP 会走到默认映射的另一条 GDB 路径（通常是 devkitPro 14.1）。

### 1.2 mGBA 必须带 `-g` patch

`-g` 是 mGBA 开启 GDB stub（端口 2345）的开关。**官方版 mGBA 支持 `-g`**，但本项目的 mgba-live-mcp 集成还需要把 `-g` 暴露给 MCP 工具参数：

- 通过 MCP 启动：`mgba_live_start(..., gdb_stub=true)` → 需要本地 fork 的 patch（`live_cli.py :: build_start_command` 新增 `gdb_stub` 参数）。详见 [`mgba-mcp.md`](mgba-mcp.md) §二。
- 纯 PowerShell 启动：`mGBA.exe -g <rom>`，无需 patch。

### 1.3 启动顺序

```
1. 启动 mGBA（带 -g）
2. 等待端口 2345 LISTEN + 8s CPU 热身
3. 运行 GDB（连接 localhost:2345）
```

**端口就绪 ≠ 游戏 CPU 就绪**。mGBA 启动后先绑定端口，但游戏 CPU 还需几秒才进入 RSP 处理循环。过早连接 GDB 会得到 `Connection timed out`。

---

## 二、三种调试方式选型

| 方式 | 启动 | GDB 驱动 | 能否并存 mGBA MCP | 适用场景 |
|---|---|---|---|---|
| **A. GDB MCP 交互模式** | `mgba_live_start(..., gdb_stub=true)` | `gdb_init` + `gdb_connect` + `gdb_evaluate_expression` | ✅ | 快速查寄存器、读内存表达式；**不适合断点调试**（见下文坑 5） |
| **B. GDB batch 脚本**（推荐） | 同 A | `arm-none-eabi-gdb.exe --batch -x script.gdb` | ✅（mGBA MCP 工具可继续用） | 断点、watchpoint、自动化捕获寄存器 |
| **C. 纯 PowerShell + GDB batch** | `pwsh tools/mgba-scripts/start-mgba-gdb-ss1.ps1` + `wait-mgba-ready.ps1` | 同 B | ❌（`mgba_live_attach` 不认脚本启动的 mGBA） | 不需要 mGBA MCP 的纯 GDB 场景 |

### 2.1 为什么 GDB batch 优于 GDB MCP 交互

`gdb_continue` 是异步命令。GDB MCP 的 MI parser 不处理 `*stopped` 异步通知，因此：
1. `gdb_continue` 后，断点命中时 GDB 进入暂停状态，但 MCP 感知不到
2. 后续 `gdb_evaluate_expression` 等命令超时
3. 看似"挂起"，实际断点已触发但 MCP 读不到

**GDB batch 模式**：脚本里的 `continue` 会阻塞等待断点命中，`hook-stop` 自动打印寄存器后 `quit`——一次性捕获、不依赖 MCP 异步处理。

### 2.2 同一 mGBA 进程被两套 MCP 同时控制（2026-04-16 验证）

- 通过 `mgba_live_start(..., gdb_stub=true)` 启动的 mGBA 进程
- GDB stub（端口 2345）和 mGBA Lua bridge（管道）**互不干扰**
- 可以同时用 mGBA MCP 工具（截图/内存读/按键）和 GDB MCP 工具（断点/寄存器）
- **但 `gdb_continue` 后不要再用 GDB MCP**（见上节），改用 mGBA MCP 做按键注入 + 另起 GDB batch 做断点捕获

### 2.3 脚本启动的 mGBA 不能被 MCP 接管

`pwsh -File tools/mgba-scripts/start-mgba-gdb-ss1.ps1` 通过 `cmd /c start mGBA.exe -g -t ...` 直接启动——mgba-live-mcp 的会话注册表（`~/.mgba-live-mcp/runtime/sessions/`）里**没有**此 PID 对应的记录：

```
mgba_live_attach(pid=15452)
→ PID is not a managed live session. Only processes started with mgba_live.py can be live-controlled.
```

脚本启动只适用于纯 GDB 场景；要同时用两套 MCP，必须走 `mgba_live_start` 路径。

---

## 三、Windows 进程管理（Job Object）

### 3.1 问题现象

在工具环境（Claude Code CLI / GitHub Copilot CLI 等）中通过 PowerShell 启动 mGBA 后，mGBA 进程在脚本执行完毕后随即退出，无论用哪种方式：

```powershell
# 方式 A：Start-Process（默认）
Start-Process -FilePath $mgba -ArgumentList "..."

# 方式 B：ProcessStartInfo + UseShellExecute=$true
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.UseShellExecute = $true
[System.Diagnostics.Process]::Start($psi)
```

### 3.2 根本原因：Windows Job Object

Windows Job Object 是一种内核对象，用于将一组进程绑定在一起统一管理。最常见的用途之一是设置 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`——Job Object 关闭时杀死所有关联进程。

工具环境在执行 PowerShell 脚本时，会将 PowerShell 进程本身加入一个 Job Object（用于超时控制、资源隔离）：

```
[工具环境（Job Object 所有者，KILL_ON_JOB_CLOSE=true）]
    └── pwsh.exe（PowerShell 会话）     ← 被加入 Job Object
            └── mGBA.exe                ← 默认继承父进程的 Job Object 关联
```

PowerShell 脚本退出后，Job Object 引用计数归零，系统杀死 Job 内所有进程——包括 mGBA。

### 3.3 为什么 `UseShellExecute=$true` 不够

`UseShellExecute=$true` 设计目的是通过 Shell（Explorer）启动进程，使其不继承父进程的句柄。普通情况下这足以使子进程独立存活。

但当父进程已经被加入一个设置了 `KILL_ON_JOB_CLOSE` 的 Job Object 时，子进程在 Windows Vista+ 默认会**继承同一个 Job Object**（除非父 Job Object 允许嵌套）。即便 Shell 启动也无法绕过这一继承，因为继承发生在内核层面。

### 3.4 解决方案：`cmd /c start`

Windows `cmd.exe` 的 `start` 命令有一个特殊行为：创建进程时会传入 `CREATE_BREAKAWAY_FROM_JOB` 标志（或等效机制），使新进程**脱离当前 Job Object**：

```powershell
# ❌ 错误：子进程继承 Job Object，PS 退出时被杀
Start-Process $mgba -ArgumentList "-g $rom"

# ✅ 正确：cmd /c start 使 mGBA 脱离 Job Object
$args = "/c start `"`" `"$mgba`" -g `"$rom`""
Start-Process -FilePath "cmd.exe" -ArgumentList $args -PassThru
```

启动后的进程关系：

```
[工具环境 Job Object]
    └── pwsh.exe
            └── cmd.exe（/c start，立即退出）
                    └── mGBA.exe   ← 已脱离 Job Object，独立存活 ✅
```

`cmd.exe` 在 `start` 之后立即退出，mGBA 成为独立进程，不再受任何 Job Object 约束。

### 3.5 验证

```powershell
Get-Process -Name "mGBA" -ErrorAction SilentlyContinue | Select-Object Id, Name
(netstat -ano) | Where-Object { $_ -match "2345" }
```

> **规则**：在工具环境的 PowerShell 中启动需要长时间存活的 GUI 进程（如 mGBA），**必须通过 `cmd /c start` 启动**。此规则适用于所有需要在 PowerShell 脚本退出后仍然存活的子进程。

启动脚本还必须**立即退出**，等待端口就绪放到独立的第二条命令（`tools/mgba-scripts/wait-mgba-ready.ps1`）——见 §五坑 1。

---

## 四、断点与监视点能力矩阵

**环境**：GDB 10.2 + mGBA stub 端口 2345 + ss1 存档（卡组编辑界面，静态画面）。

### 4.1 内存区域（来自 `info mem`）

| # | 地址范围 | Stub 标注 | 实际属性 |
|---|----------|-----------|----------|
| 0 | `0x00000000–0x00004000` | ro | BIOS（只读） |
| 1 | `0x02000000–0x02040000` | rw | EWRAM（外部工作 RAM） |
| 2 | `0x03000000–0x03008000` | rw | IWRAM（内部工作 RAM） |
| 3 | `0x04000000–0x04000400` | rw | IO 寄存器 |
| 4 | `0x05000000–0x05000400` | rw | 调色板 RAM |
| 5 | `0x06000000–0x06018000` | rw | VRAM |
| 6 | `0x07000000–0x07000400` | rw | OAM |
| 7 | `0x08000000–0x0A000000` | rw | ROM（物理只读，stub 误标 rw） |
| 8 | `0x0A000000–0x0C000000` | rw | ROM bank2 |

> `monitor help` 返回 `"Target does not support this command"`——stub 不支持 monitor 扩展命令。

### 4.2 断点类型矩阵

| 符号 | 含义 |
|------|------|
| ✅ | 设置成功 + 触发成功 |
| ✅* | 设置成功 + 触发（需特定游戏状态） |
| 🔵 | 设置成功，未触发（游戏状态下无读写活动） |
| 🔵† | 设置成功，skip continue（预计立即触发导致 packet storm） |
| ❌ | stub 报错，不支持 |
| — | 无意义（如 ROM 写监视点） |

| 断点类型 | ROM | EWRAM | IWRAM（代码） | IWRAM（数据） | VRAM | IO |
|----------|-----|-------|--------------|--------------|------|----|
| `break`（软件断点） | ✅ | — | ✅ | — | — | — |
| `hbreak`（硬件断点） | ✅ | — | ✅ | — | — | — |
| `watch`（写监视点） | — | 🔵 | — | 🔵 | ✅* | ✅ |
| `rwatch`（读监视点） | 🔵† | 🔵 | — | 🔵 | 🔵 | ✅ |
| `awatch`（读写监视点） | — | — | — | — | — | ❌ |

### 4.3 关键结论

- **`break` 在 ROM 上可用**：GBA ROM 物理只读，理论上软件断点（BKPT 指令写入）不可行；mGBA stub 在模拟层面拦截执行，无需真正修改 ROM 字节。**真实硬件上不可用**。
- **`hbreak` 推荐用于 ROM 代码断点**：真实硬件也可用。
- **`awatch` 全区域不可用**：stub 返回非 RSP 格式的响应（如字符串 `"not supported"`），GDB 解析报 `Reply contains invalid hex digit 79`，整个 session 退出。
- **VRAM 写监视点需要"正确游戏状态"**：存档加载后 VRAM 已写入完毕，不再触发。用冷启动（nosave 模式）触发卡图加载时可捕获，例如 `watch *(unsigned int*)0x06000040` 在 `PC=0x80f4eb6` 触发。
- **VRAM 读监视点无效**：PPU（图形处理单元）读 VRAM **不经过 ARM CPU 内存总线**，watchpoint 捕获不到。仅当 CPU 代码显式读 VRAM（`ldr *, 0x06xxxxxx`）时才触发。
- **ROM rwatch 不能 continue**：GBA CPU 每条指令都是一次 ROM 读取，watchpoint 每帧触发数万次形成 packet error 风暴。仅可 set-only 验证。
- **EWRAM/IWRAM rwatch 需选择游戏主循环实际访问的地址**：rwatch 机制本身可用（IO 验证通过），但在 deck editor 状态下 `0x02000000`（存档头）、`0x03000808`（函数指针）等地址不被访问，不会触发。

### 4.4 给 P1 阶段的建议

| 调试目标 | 推荐断点类型 |
|----------|------------|
| ROM 函数入口（如 memcpy） | `hbreak *0x080F4EB6` |
| IWRAM 游戏主循环 | `break *0x03004DB4` 或 `hbreak` |
| 监听 VRAM 卡图写入 | `watch *(unsigned int*)0x06000040`（需 nosave 触发卡图加载） |
| 监听 DMA 写入源地址 | `watch *(unsigned int*)0x040000D0`（DMA3SAD） |
| 监听 IO 读取 | `rwatch *(unsigned int*)0x040000D0` |
| EWRAM 存档写入 | `watch *(unsigned int*)0x02000000`（需进入存档流程） |

---

## 五、12 个已知坑与 workaround

### 坑 1：`-g` 不接受端口号

```powershell
# ❌ 错误：2345 被当作 ROM 路径，mGBA 立即退出
Start-Process mGBA.exe -ArgumentList @("-g", "2345", "rom.gba")

# ✅ 正确：端口固定 2345，-g 只是开关
Start-Process mGBA.exe -ArgumentList @("-g", "rom.gba")
```

### 坑 2：端口就绪 ≠ 游戏 CPU 就绪

端口 2345 出现在 netstat 后，mGBA 仍需几秒才进入 RSP 命令循环。过早连接 GDB 会得到 `Connection timed out`。

**解决**：端口出现后再等 5-8 秒（`wait-mgba-ready.ps1` 中实现），或观察游戏画面已正常显示后再连接。

### 坑 3：GDB stub 一次性消耗

GDB 连接后断开（包括 `quit`、`--batch` 脚本结束），stub **永久关闭**，端口停止监听。后续连接一律被拒绝。

**解决**：每次调试前必须完整重启 mGBA（`mgba_live_stop` + `mgba_live_start`）。

> ⚠️ **2026-04-15 踩坑补记**：**任何 TCP 握手都算"连接"**，包括：
> - `Test-NetConnection -ComputerName localhost -Port 2345`
> - `netstat` 之外的主动探测工具
> - 任何访问 `http://localhost:2345` 的浏览器行为
>
> **错误工作流**（会把 stub 消耗掉）：
> ```
> 启 mGBA → Test-NetConnection 验证端口 → 端口"看起来开着" → gdb_connect → 30s 超时
> ```
> 因为 Test-NetConnection 那一步**已经触发了 stub 的唯一一次握手**。
>
> **正确做法**：
> - 只用 `netstat -ano | Select-String ":2345"` 检查 LISTEN（纯被动观察）
> - 或者直接 sleep 5-8s 后直接连 GDB，不做任何主动探测
> - 若必须探测，接受"每次探测 = 一次重启 mGBA"的成本

### 坑 4：PowerShell Job Object 导致 mGBA 被杀死

详见 §三。启动必须用 `cmd /c start` 脱离 Job Object；启动脚本必须立即退出，等待端口就绪放到独立的第二条命令。

### 坑 5：GDB MCP 交互模式下 `gdb_continue` 后所有命令超时

GDB MCP 的 MI parser 不处理 `*stopped` 异步通知，`gdb_continue` 后 MCP 感知不到断点命中，后续 `gdb_evaluate_expression` 等全部超时。

**解决**：改用 GDB batch 脚本模式（见 §二）。

### 坑 6：GDB 脚本 `echo` 中文会乱码

GDB 的 `echo` 命令处理中文字符时显示乱码。

**解决**：GDB 脚本（`.gdb` 文件）里的 `echo` 和注释全部使用英文/ASCII。

### 坑 7：GDB 脚本不能有 UTF-8 BOM

**现象**：GDB 执行时第一行报 `Undefined command: ""`，随后所有命令失败。

**原因**：Windows 记事本和部分编辑器默认保存 UTF-8 with BOM（`EF BB BF`），GDB 无法识别 BOM，将其当作命令解析。

**解决**：写入 GDB 脚本时使用无 BOM 的 UTF-8：
```powershell
$enc = New-Object System.Text.UTF8Encoding $false   # $false = 无 BOM
[System.IO.File]::WriteAllText($path, $content, $enc)
```

### 坑 8：Ghidra 将 GBA SWI 输出为 `svc`，不要搜 `swi`

ARM 架构 v7 起将 SWI 指令重命名为 SVC（SuperVisor Call），编码完全相同。Ghidra 统一使用新助记符，因此在 `asm/all.s` 中：

```bash
# ❌ 找不到任何结果
grep "swi" asm/all.s

# ✅ 正确
grep "svc 0x11" asm/all.s   # LZ77UnCompVram
grep "svc 0x12" asm/all.s   # LZ77UnCompWram
grep "svc 0x13" asm/all.s   # HuffUnCompReadNormal
```

### 坑 9：GDB stub watchpoint 强制 1 字节范围

GDB 协议的 `Z2/Z3/Z4`（watchpoint）命令带有 address 和 size 两个参数。但 mGBA `gdb-stub.c` 的 `_setBreakpoint()` **忽略 size**，始终只监听 1 字节：

```c
struct mWatchpoint watchpoint = {
    .minAddress = address,
    .maxAddress = address + 1   // ← 硬编码，不读 size
};
```

**影响**：`watch *(uint*)0x06000040` 只监 1 字节，而不是 4 字节；宽范围覆盖只能靠大量独立 watchpoint。

**规避**：改用方案 A（ROM 离线搜索），或不依赖 GDB watchpoint 改用 hbreak + 手动读寄存器。

### 坑 10：条件 watchpoint 导致大量 packet error

**现象**：设置 `condition 1 *(unsigned int*)0x040000D0 >= 0x08000000` 后，GDB 输出连续的 `Ignoring packet error, continuing...`，脚本卡住。

**原因**：mGBA GDB stub 实现较简单。每次 watchpoint 触发时，GDB 需要通过 RSP 协议请求 stub 在目标机上对条件表达式求值。在游戏高频触发 DMA3 的情况下，stub 来不及响应求值请求，导致 RSP 包超时堆积。

**解决**：去掉条件，让所有触发都停下，在 GDB 脚本或事后日志中过滤 ROM 地址范围。

### 坑 11：GDB MCP 源码改动未 rebuild → `gdb_connect` 稳定 30s 超时

**现象**：`gdb_connect(target="localhost:2345")` 每次都在 30s 后报错；mGBA 端口 2345 在连接尝试**后**立即关闭（stub 被消耗但 MCP 收不到响应）。

**原因**：`D:\Software\gdb-mcp\src\gdb\mi-parser.ts` 修好了带 token 的 `N^connected` 响应解析（见 §七 Bug 1），但 `dist/index.js` 没重新构建，Claude Code 加载的仍是旧代码。

**排查命令**：
```bash
grep -c "caretIdx" D:/Software/gdb-mcp/dist/gdb/mi-parser.js
# 返回 0 → dist 过期；返回 ≥ 1 → 已同步
```

**修复**：
```bash
cd D:/Software/gdb-mcp && npm run build
# 然后【重启 Claude Code】——MCP server 一次性加载，本会话内无法热重载
```

### 坑 12：uv cache 更新丢失 `live_cli.py` 的 `-g` patch

**旧现象**：`mgba_live_start` 不再超时（直接成功返回 heartbeat），但端口 2345 不 LISTEN，`gdb_connect` 超时。

**根因**：uv cache 创建新 archive 时（包更新 / 环境变动）会从 wheel 重解压，手工打在旧 archive 里的 `-g` patch 无法迁移到新 archive，MCP server 切换后 stub 不启用。

**根治**：改用本地 fork `D:\Software\mgba-live-mcp`（分支 `local-patches`）——见 [`mgba-mcp.md`](mgba-mcp.md) §二。

### 附：加载存档快照的参数格式

ROM 文件和存档快照需分开传，ROM 路径放最后：

```powershell
Start-Process mGBA.exe -ArgumentList @("-g", "-t", "2343.ss1", "2343.gba")
```

---

## 六、工具链验证 PoC（DMA3 walkthrough）

**场景**：纯 PowerShell + GDB batch，不依赖任何 MCP。本节记录 P0 阶段的端到端验证，为后续 GDB batch 脚本调试的模板。

### 6.1 GBA DMA3 寄存器背景

GBA 有 4 个 DMA 通道，DMA3 是通用 DMA：

| 地址 | 名称 | 说明 |
|------|------|------|
| `0x040000D0` | DMA3SAD | 源地址（CPU 在启动 DMA 前写入此寄存器） |
| `0x040000D4` | DMA3DAD | 目标地址 |
| `0x040000D8` | DMA3CNT_L | 传输字数 |
| `0x040000DA` | DMA3CNT_H | 控制寄存器（写入此寄存器触发 DMA） |

**监听 DMA3SAD 的意义**：CPU 设置 DMA 传输时必须先写 SAD，因此 watchpoint 在 DMA 实际发生之前触发，可以读到完整的调用上下文（PC、LR、参数寄存器）。

> `watch *(unsigned int*)0x040000D0` 监听的是 **CPU 写 DMA 设置寄存器**的动作，而不是 DMA 搬运数据本身。

### 6.2 涉及文件

| 文件 | 用途 |
|------|------|
| `tools/mgba-scripts/_preflight-mgba.ps1` | 启动前预检：关闭已有 mGBA、确认端口空闲 |
| `tools/mgba-scripts/start-mgba-gdb-nosave.ps1` | 启动 mGBA（无存档冷启动） |
| `tools/mgba-scripts/start-mgba-gdb-ss1.ps1` | 启动 mGBA（加载 `roms/2343.ss1` 存档） |
| `tools/mgba-scripts/wait-mgba-ready.ps1` | 等待 GDB stub 端口就绪 + CPU 热身 |
| `doc/dev/scripts/gdb_dma_watch.gdb` | GDB 自动化脚本：设置 watchpoint、捕获触发 |
| `tools/arm-none-eabi-gdb.exe` | GDB 10.2 |

### 6.3 完整操作步骤

```powershell
# 步骤 1：启动 mGBA（带存档）
pwsh -File tools/mgba-scripts/start-mgba-gdb-ss1.ps1
# 预期：[preflight] 已关闭旧实例 / 端口空闲
#       [start] mGBA 已启动（通过 cmd /c start）
#       [start] 脚本立即退出（保持 mGBA 独立存活）

# 步骤 2：等待 GDB stub 就绪（独立命令）
pwsh -File tools/mgba-scripts/wait-mgba-ready.ps1
# 预期：[wait] 端口 2345 已就绪 → 等待 8s CPU 热身 → 就绪

# 步骤 3：运行 GDB 脚本
& "tools\arm-none-eabi-gdb.exe" --batch -x "doc\dev\scripts\gdb_dma_watch.gdb"
```

**预期输出**：
```
[GDB] Connected
pc  0x3004fdc

Hardware watchpoint 1: *(unsigned int*)0x040000D0

[GDB] Watching DMA3SAD (0x040000D0)
[GDB] Waiting for first DMA3 trigger...

=== DMA3SAD WRITE CAPTURED ===
pc   0x3004db4
lr   0x3000144
r0   0x40000a0
r1   0x40000a4
r2   0x30055c0
r3   0x30055e0
--- DMA3 registers (D0=SAD D4=DAD D8=CNT) ---
0x40000d0:  0x84400000  0xa101a101  0xa101a101  0x00000000

[GDB] Done - one DMA3 trigger captured.
```

### 6.4 GDB 脚本模板

```gdb
set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

echo \n[GDB] Connected\n
info registers pc

watch *(unsigned int*)0x040000D0

echo \n[GDB] Watching DMA3SAD (0x040000D0)\n
echo [GDB] Waiting for first DMA3 trigger...\n

define hook-stop
  echo \n=== DMA3SAD WRITE CAPTURED ===\n
  info registers pc lr r0 r1 r2 r3
  echo --- DMA3 registers (D0=SAD D4=DAD D8=CNT) ---\n
  x/4xw 0x040000D0
end

continue

echo \n[GDB] Done - one DMA3 trigger captured.\n
quit
```

**要点**：
- `hook-stop`：每次 watchpoint 触发时自动执行，打印寄存器和 DMA3 寄存器组
- `x/4xw 0x040000D0`：连续读取 4 个 32-bit 字（SAD / DAD / CNT_L+H）
- `--batch` 模式：脚本执行完自动退出，适合自动化

### 6.5 捕获结果分析

#### 带存档时的 DMA3SAD 触发（验证 watchpoint 机制）

```
PC  = 0x3004db4   → IWRAM 中的代码（游戏主循环）
LR  = 0x3000144
DMA3SAD = 0x84400000   → 非 ROM 地址，0x8 为 I/O 镜像区
DMA3DAD = 0xa101a101
```

- PC 在 `0x03xxxxxx`（IWRAM），说明是游戏运行时动态调度的 DMA
- `0x84400000` / `0xb6400000` 交替写入，推测是音频或背景图层的循环 DMA
- 此触发**不是卡图 DMA**，但证明 watchpoint 机制完全正常

#### 无存档时的 VRAM watchpoint 触发（卡图 CPU copy）

切换到 `start-mgba-gdb-nosave.ps1` 冷启动，监听 `watch *(unsigned int*)0x06000040`：

```
触发 1:  PC=0x80fb904  LR=0x80fb8ef  r1=0x40     r2=0x3e0
         → 初始化：写入 tile 索引（顺序值 0x40、0x60...），非卡图

触发 2:  PC=0x80f4eb6  LR=0x80fbc9b  r1=0x9dffa4c  r2=0x6000040
         → r1=ROM bank2 地址，r2=VRAM tile1 起始 → 卡图数据 CPU copy！
```

**关键结论**：

> **游戏王 EX2006 的卡图加载不使用 DMA，而是 CPU 直接 memcpy。**
>
> - 调用点 PC：`0x080f4eb6`（推测为 memcpy 内部）
> - 调用方 LR：`0x080fbc9b`（卡图加载函数）
> - 数据来源：ROM bank2 `0x09dffa4c`（ROM 文件偏移 `0x01dffa4c`）
> - 数据目标：VRAM `0x06000040`（tile 1 起始，卡图显示区域）

因此，**定位卡图 ROM 位置应使用 VRAM watchpoint（冷启动），而非 DMA3 watchpoint**。

---

## 七、GDB MCP 集成细节

### 7.1 概述

本节记录 GDB MCP（`D:\Software\gdb-mcp`）集成时发现并修复的 4 个 parser bug，以及工具可用性表。

### 7.2 4 个 parser bug 修复历史

#### Bug 1：token 前缀导致连接超时（主要 bug）

**现象**：`gdb_connect` 超时，30 秒后报错。

**原因**：GDB MI 协议中，发送带 token 的命令（如 `20-target-select remote ...`），GDB 响应为 `20^connected`（token 前缀格式）。`parseMiLine()` 只识别以 `^` 开头的行，`20^connected` 被当作普通 console 输出忽略，命令永远得不到响应。

**修复**：`D:\Software\gdb-mcp\src\gdb\mi-parser.ts` 的 `parseMiLine()`：
```typescript
// 修复前：只检查 line.startsWith("^")
// 修复后：查找 ^ 位置，支持 N^result-class 格式
const caretIdx = line.indexOf("^");
if (caretIdx > 0 && /^\d+$/.test(line.slice(0, caretIdx))) {
  const token = parseInt(line.slice(0, caretIdx), 10);
  const response = parseResultRecord(line.slice(caretIdx));
  response.token = token;
  return response;
}
```

#### Bug 2：`split(",", 2)` 截断值

**现象**：`gdb_set_breakpoint` 返回"断点已设置: undefined"，`bkpt` 为空对象 `{}`。

**原因**：JavaScript 的 `"done,bkpt={n=1,type=bp}".split(",", 2)` 返回 `["done", "bkpt={n"]`（limit 参数继续找到达到 limit），导致 `parseMiTuple` 只收到截断的字符串。

同一问题存在于：`parseResultRecord`、`parseAsyncRecord`、`parseMiTuple` 的 pair 分割。

**修复**：改用 `indexOf(",")` / `indexOf("=")` 只在第一个分隔符处分割：
```typescript
const commaIdx = rest.indexOf(",");
const resultClass = commaIdx >= 0 ? rest.slice(0, commaIdx) : rest;
if (commaIdx >= 0) result = parseMiTuple(rest.slice(commaIdx + 1));
```

#### Bug 3：`parseMiOutput` 按 `\n` 切行导致 bkpt 解析失败

**现象**：即使修复了 Bug 2，`gdb_list_breakpoints` 仍解析不到断点字段。

**原因**：GDB 在 `-break-list` 响应中，`thread-groups=["i1\n"]` 包含**字面换行符**。`parseMiOutput` 直接按 `\n` 切行，把一条完整的 MI 记录切成两段。

**修复**：`parseMiOutput` 改为跟踪括号深度和字符串状态，只在 depth=0 且不在字符串内时才切行：
```typescript
for (let i = 0; i < buffer.length; i++) {
  if (char === '"' && prevChar !== "\\") inString = !inString;
  if (!inString) {
    if ("{[(".includes(char)) depth++;
    else if ("}])".includes(char)) depth--;
    else if (char === "\n" && depth === 0) {
      // 提取完整行，调用 parseMiLine
    }
  }
}
```

#### Bug 4：`parseBreakpointList` 路径错误

**现象**：`gdb_list_breakpoints` 总是显示"当前没有设置断点"。

**原因**：`parseBreakpointList` 读取 `result?.breakpoints`，但 `-break-list` 实际返回结构为：
```
{BreakpointTable: {nr_rows: ..., body: [bkpt={...}]}}
```
另外 `body` 中的元素是 `bkpt={...}` 格式（key=value），`parseMiList` 未处理此格式。

**修复**：
1. `mi-commands.ts`：`parseBreakpointList` 改为读取 `result?.BreakpointTable?.body`
2. `mi-parser.ts`：`parseMiList` 增加对 `key=value` 格式 item 的处理（取 value 部分）

### 7.3 工具可用性表

| 工具 | 状态 | 备注 |
|------|------|------|
| `gdb_init` | ✅ | 必须指定 `gdbPath="tools/arm-none-eabi-gdb.exe"`，**不能传 `architecture` 参数** |
| `gdb_connect` | ✅ | `localhost:2345` |
| `gdb_disconnect` | ✅ | |
| `gdb_set_breakpoint` | ✅ | 返回断点编号和地址 |
| `gdb_list_breakpoints` | ✅ | 正确显示断点地址、状态 |
| `gdb_delete_breakpoint` | ✅ | |
| `gdb_continue` | ✅ | 但 `*stopped` 异步通知不处理，后续命令超时（见坑 5） |
| `gdb_interrupt` | ✅ | |
| `gdb_evaluate_expression` | ✅ | 读取 `*(unsigned int*)0x040000D4` 等表达式成功 |
| `gdb_list_locals` | ✅ | 无符号表时返回空（正常） |
| `gdb_list_frames` | ⚠️ | mGBA THUMB 调试不支持栈回溯（`Reply contains invalid hex digit 83`）|
| `gdb_read_memory` | ⚠️ | `memory.contents.join is not a function`，parser bug 待修；**改用 `gdb_evaluate_expression`** |
| `gdb_read_registers` | ⚠️ | 高层 API 寄存器名→编号转换有问题；**改用** `gdb_command("-data-list-register-values x 0 1 15")` |

### 7.4 MCP 进程生命周期

- GDB MCP dist 修改后，**必须重启 Claude CLI** 才会加载新代码
- 重启顺序：修改源码 → `npm run build` → 重启 CLI → 重启 mGBA → 验证
- **验证命令**：`grep -c "caretIdx" D:/Software/gdb-mcp/dist/gdb/mi-parser.js` 应返回 ≥ 1

### 7.5 mGBA stub 限制摘要

- **一次性连接**：GDB 断开后 stub 永久关闭，每次需重启 mGBA
- `monitor help` 返回 "Target does not support this command"，不支持 monitor 扩展命令
- ROM 区域被标记为 rw（实际只读），不影响使用
- THUMB 代码栈回溯不支持（`-stack-list-frames` 失败）
- Windows GDB 输出 `\r\n` 换行，`parseMiOutput` 的 `.trim()` 会消除 `\r`；但 `thread-groups=["i1\r\n"]` 中内嵌的 `\r\n` 会与 Bug 3 相关

### 7.6 `~/.claude.json` 配置形态

```json
"gdb": {
  "command": "node",
  "args": ["<gdb-mcp dist 目录>\\index.js"]
}
```
gdb-mcp dist 的具体本机路径见 `LOCAL.md`。

---

## 八、相关文档

| 文件 | 说明 |
|------|------|
| [`mgba-mcp.md`](mgba-mcp.md) | mGBA MCP（Lua bridge）调试指南 |
| `CLAUDE.md` §调试工具链 | 顶层场景决策：何时用哪套 MCP / batch 脚本 |
| `doc/dev/locate-rom-asset-from-vram-diff.md` | 从 VRAM 差分定位 ROM 资源的核心方法论（引用本文 §四、§五） |
| `doc/dev/scripts/gdb_*.gdb` | GDB batch 脚本模板集合 |
| `tools/mgba-scripts/*.ps1` | PowerShell 启动脚本 |
