# mGBA GDB Stub 调试经验

记录通过 GDB 连接 mGBA GDB stub 过程中踩过的坑，供后续调试参考。

---

## 工具选择

**必须使用 `tools/arm-none-eabi-gdb.exe`（GDB 10.2）**，不能用 devkitARM 自带的 GDB 14.1。

GDB 14.1 与 mGBA stub 之间存在 RSP 协议不兼容，握手阶段就会失败。GDB 10.2 可直接连接，无需代理。

---

## 正确的启动流程

**首选：通过 mGBA MCP 启动 mGBA**（`mgba_live_start`，见 `mgba-mcp-setup.md`）——同一个 mGBA 进程可同时被 GDB MCP（stub:2345）和 mGBA MCP（Lua bridge 管道）控制。

**仅使用 GDB 时**可走 PowerShell 脚本路径（`tools/mgba-scripts/start-mgba-gdb-ss1.ps1`）。⚠ 这种方式启动的 mGBA **无法**被 `mgba_live_attach` 接管（会报 "PID is not a managed live session"）。

脚本路径仍需分步操作，不能把启动、等待、GDB 连接全写在同一个 PowerShell 命令块里：

```
1. 手动启动 mGBA（单独执行一条命令）
2. 等待 netstat 显示 :2345 LISTENING
3. 再额外等待 5-8 秒（游戏 CPU 需要时间进入 RSP 循环）
4. 运行 GDB
```

---

## 已知坑

### 坑 1：`-g` 不接受端口号

```powershell
# ❌ 错误：2345 被当作 ROM 路径，mGBA 立即退出
Start-Process mGBA.exe -ArgumentList @("-g", "2345", "rom.gba")

# ✅ 正确：端口固定 2345，-g 只是开关
Start-Process mGBA.exe -ArgumentList @("-g", "rom.gba")
```

### 坑 2：端口就绪 ≠ 游戏 CPU 就绪

端口 2345 出现在 netstat 后，mGBA 仍需几秒才进入 RSP 命令循环。过早连接 GDB 会得到 `Connection timed out`。

**解决**：端口出现后再等 5-8 秒，或观察游戏画面已正常显示后再连接。

### 坑 3：GDB stub 一次性消耗

GDB 连接后断开（包括 `quit`、`--batch` 脚本结束），stub **永久关闭**，端口停止监听。后续连接一律被拒绝。

**解决**：每次调试前必须完整重启 mGBA。

> ⚠️ **2026-04-15 踩坑补记**：**任何 TCP 握手都算"连接"**，包括：
> - `Test-NetConnection -ComputerName localhost -Port 2345`
> - `netstat` 之外的主动探测工具
> - 任何访问 `http://localhost:2345` 的浏览器行为
>
> **错误工作流**（会把 stub 消耗掉）：
> ```
> 启 mGBA → Test-NetConnection 验证端口 → 端口"看起来开着" → gdb_connect → 30s 超时
> ```
> 因为 Test-NetConnection 那一步**已经触发了 stub 的唯一一次握手**，随后 GDB MCP 连到的是空端口。
>
> **正确做法**：
> - 只用 `netstat -ano | Select-String ":2345"` 检查 LISTEN 状态（纯被动观察）
> - 或者直接 `sleep 5-8`（依靠 `wait-mgba-ready.ps1` 的延时约定）后直接连 GDB，**不做任何主动探测**
> - 若必须探测，接受"每次探测 = 一次重启 mGBA"的成本

### 坑 4：PowerShell Job Object 导致 mGBA 被杀死

在工具环境（Copilot CLI 等）中，PowerShell 进程本身被加入了一个设置了
`KILL_ON_JOB_CLOSE` 的 Windows Job Object。无论使用 `Start-Process` 还是
`UseShellExecute=$true`，子进程都会继承该 Job Object，在 PS 会话退出时被杀死。

**解决**：通过 `cmd /c start` 启动 mGBA，使其脱离 Job Object：

```powershell
# ❌ 错误：子进程继承 Job Object，PS 退出时被杀
Start-Process $mgba -ArgumentList "-g $rom"

# ✅ 正确：cmd /c start 使 mGBA 脱离 Job Object
Start-Process "cmd.exe" -ArgumentList "/c start `"`" `"$mgba`" -g `"$rom`""
```

此外，启动脚本必须立即退出，等待端口就绪放到独立的第二条命令中执行（`tools/mgba-scripts/wait-mgba-ready.ps1`）。

> 详细原理见 `doc/dev/powershell-job-object-mgba.md`

### 坑 5：GDB 脚本 `echo` 中文会乱码

GDB 的 `echo` 命令处理中文字符时显示乱码。

**解决**：GDB 脚本（`.gdb` 文件）里的 `echo` 和注释全部使用英文/ASCII。

### 坑 6：Ghidra 将 GBA SWI 输出为 `svc`，不要搜 `swi`

ARM 架构 v7 起将 SWI 指令重命名为 SVC（SuperVisor Call），编码完全相同。Ghidra 统一使用新助记符，因此在 `asm/all.s` 中：

```
# ❌ 找不到任何结果
grep "swi" all.s

# ✅ 正确
grep "svc 0x11" all.s   # LZ77UnCompVram
grep "svc 0x12" all.s   # LZ77UnCompWram
grep "svc 0x13" all.s   # HuffUnCompReadNormal
```

### 坑 8：GDB stub watchpoint 强制 1 字节范围

GDB 协议的 `Z2/Z3/Z4`（watchpoint）命令带有 address 和 size 两个参数。但 mGBA `gdb-stub.c` 的 `_setBreakpoint()` **忽略 size**，始终只监听 1 字节：

```c
struct mWatchpoint watchpoint = {
    .minAddress = address,
    .maxAddress = address + 1   // ← 硬编码，不读 size
};
```

**影响**：`watch *(uint*)0x06000040` 只监 1 字节，而不是 4 字节；宽范围覆盖只能靠大量独立 watchpoint。

**规避**：改用方案 A（ROM 离线搜索）；或不依赖 GDB watchpoint，改用 hbreak + 手动读寄存器。

### 坑 10：GDB MCP 源码改动未 rebuild → `gdb_connect` 稳定 30s 超时

**现象**：`gdb_connect(target="localhost:2345")` 每次都在 30s 后报错；
mGBA 端口 2345 在连接尝试**后**立即关闭（stub 被消耗，但 MCP 收不到响应）。

**原因**：`D:\Software\gdb-mcp\src\gdb\mi-parser.ts` 修好了带 token 的
`N^connected` 响应解析（见 [`p0-5-gdb-mcp-integration.md`](p0-5-gdb-mcp-integration.md)
Bug 1），但 `dist/index.js` 没重新构建，Claude Code 加载的仍是旧代码。

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

2026-04-15 复现并修复。

### 坑 9：VRAM/EWRAM watchpoint 失败是地址错，不是区域限制

mGBA watchpoint 通过 CPU 内存访问 shim 实现，**理论上覆盖所有地址**，包括 VRAM（0x06xxxxxx）和 EWRAM（0x02xxxxxx）。过去实验失败的真实原因：

1. 监听了 `0x06000000`（tile 0 / 背景色），而卡图从 `0x06000040`（tile 1）开始写
2. 使用了存档快照（ss1），卡图在快照时已加载完毕，按 A 不触发新写入

**规避**：不加载存档，从游戏启动重新进入；同时监听正确的地址范围。

### 坑 7：加载存档快照的参数格式

ROM 文件和存档快照需分开传，ROM 路径放最后：

```powershell
Start-Process mGBA.exe -ArgumentList @("-g", "-t", "2343.ss1", "2343.gba")
```

---

## GDB 脚本模板

```gdb
set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

info registers pc sp

# 示例：监听 DMA3 源地址寄存器（捕获从 ROM 搬运数据的时机）
watch *(unsigned int*)0x040000D8

continue
```

---

### 坑 11：`mgba_live_attach` 只接管 managed session

`tools/mgba-scripts/start-mgba-gdb-ss1.ps1` 通过 `cmd /c start mGBA.exe -g -t ...` 直接启动模拟器——mgba-live-mcp 的会话注册表（`~/.mgba-live-mcp/runtime/sessions/`）里**没有**此 PID 对应的记录。

```
mgba_live_attach(pid=15452)
→ PID is not a managed live session. Only processes started with mgba_live.py can be live-controlled.
```

**影响**：脚本启动的 mGBA 只能被 GDB MCP 控制；若要同时使用 mGBA MCP 工具（Lua / 截图 / 内存 dump / 按键），**必须**改走 `mgba_live_start`。2026-04-16 已验证。

### 坑 12：uv cache 更新丢失 `live_cli.py` 的 `-g` patch（2026-04-16 已由 fork 根治）

**旧现象**：`mgba_live_start` 不再超时（直接成功返回 heartbeat），但端口 2345 不 LISTEN，`gdb_connect` 超时。

**根因**：uv cache 创建新 archive 时（包更新 / 环境变动）会从 wheel 重解压，手工打在旧 archive 里的 `-g` patch 无法迁移到新 archive，MCP server 切换后 stub 不启用。

**根治**：改用本地 fork `D:\Software\mgba-live-mcp`（分支 `local-patches`），`~/.claude.json` 里 mgba server 改为 `uvx --from D:\Software\mgba-live-mcp mgba-live-mcp`。见 `mgba-mcp-setup.md` 第八节"本地 fork 方案"。

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `tools/arm-none-eabi-gdb.exe` | GDB 10.2（可直连 mGBA stub） |
| `doc/dev/scripts/gdb_dma_watch.gdb` | DMA3 watchpoint 脚本 |
| `tools/mgba-scripts/start-mgba-gdb-ss1.ps1` | 脚本启动路径（仅 GDB 场景，`mgba_live_attach` 不可用） |


