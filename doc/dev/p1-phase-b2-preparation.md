# Phase B2 准备阶段操作说明

本文描述执行 Phase B2（GDB VRAM 写监视点追溯）前的环境准备流程。

---

## 前置条件：live_cli.py 需已修改

`mgba_live_start` 默认不传 `-g` 参数，需手动修改 mgba_live_mcp 的源码，
在 `build_start_command` 中插入 `-g`：

**文件**：`C:\Users\<用户名>\AppData\Local\uv\cache\archive-v0\<hash>\Lib\site-packages\mgba_live_mcp\live_cli.py`

```python
# build_start_command 函数中，将：
cmd = [
    mgba_path,
    "-C",
    f"fpsTarget={fps_target:g}",
    ...
]
# 改为：
cmd = [
    mgba_path,
    "-g",  # 启用 GDB stub（端口 2345）
    "-C",
    f"fpsTarget={fps_target:g}",
    ...
]
```

修改后**必须重启 Claude CLI**（MCP server 随 CLI 重启重新加载代码）。

---

## 第一步：清理残留进程

执行停止脚本，确保环境干净：

```powershell
pwsh -File tools/mgba-scripts/stop-mgba.ps1
```

同时确认端口 2345 未被占用：

```powershell
netstat -ano | Select-String ":2345"
```

若有占用，等待其自动释放或手动 `Stop-Process -Id <PID>`。

---

## 第二步：通过 MCP 启动 mGBA

```
mgba_live_start(
    rom="roms/2343.gba",
    savestate="roms/2343.ss1",
    session_id="yugioh-b2"
)
```

> ⚠️ **预期行为**：此调用会**超时报错**（20 秒内收不到 Lua bridge 心跳）。  
> 这是正常现象——因为 `-g` 模式下 mGBA 启动后游戏处于暂停状态，  
> Lua bridge 在游戏运行前无法初始化。**忽略超时错误，继续下一步。**

验证 mGBA 进程和端口均已就绪：

```powershell
Get-Process -Name mGBA   # 应有进程
netstat -ano | Select-String ":2345"  # 应显示 LISTENING
```

---

## 第三步：连接 GDB 并放行游戏

```
gdb_init(gdbPath="tools/arm-none-eabi-gdb.exe")
gdb_connect(target="localhost:2345")
gdb_continue()
```

`gdb_continue()` 让游戏开始运行，Lua bridge 随即初始化，心跳文件出现：

```powershell
# 等待约 5 秒后检查心跳
Get-Content "C:\Users\<用户名>\.mgba-live-mcp\runtime\sessions\yugioh-b2\heartbeat.json"
# 应输出类似：{"frame":1350,"keys":0,"unix_time":...}
```

---

## 第四步：验证 MCP 会话可用

```
mgba_live_export_screenshot(session="yugioh-b2")
```

截图应显示卡组列表界面（ss1 存档状态）。

> ⚠️ GDB stub 是**一次性连接**，断开后不可重连，必须重启 mGBA 才能再次使用。

---

## 完成状态

准备阶段完成后：
- mGBA 处于**卡组列表界面**（ss1 存档状态）
- mGBA MCP 会话可用（`session_id="yugioh-b2"`），可使用截图/内存读取/按键
- GDB 已连接并 continue，游戏正在运行，可随时中断设置监视点

下一步：执行 Phase B2 核心追溯流程（见 `p1-card-image-location-plan.md`）。
