# P0-3：mGBA MCP 功能验证报告

> 目标：系统性验证 mgba-live-mcp 提供的全部 13 个工具，确认哪些可用、哪些有 Bug、哪些需要绕过方案，为后续卡图 ROM 定位任务（P1 阶段）建立可靠的调试工具链基础。

---

## 测试环境

| 项目 | 值 |
|------|----|
| ROM | `roms/2343.gba`（遊戲王 EX2006，32 MB）|
| mGBA 版本 | mGBA-qt（Windows x64）|
| MCP 工具包 | `mgba-live-mcp`（uv cache `H-avPZ5...`）|
| 存档 | 无（测试 t11、t12 时使用了带存档启动，进入主菜单状态）|
| 操作系统 | Windows 11 |
| Python | 3.12（uv venv）|

---

## 工具总览

| # | 工具名 | 分类 | 测试结果 |
|---|--------|------|----------|
| t01 | `mgba_live_start` | 生命周期 | ✅ 正常 |
| t02 | `mgba_live_export_screenshot` | 截图 | ⚠️ 修复后可用 |
| t03 | `mgba_live_input_tap` | 输入 | ✅ 正常 |
| t04 | `mgba_live_input_set` | 输入 | ✅ 正常 |
| t05 | `mgba_live_input_clear` | 输入 | ✅ 正常 |
| t06 | `mgba_live_status` | 状态 | ✅ 正常 |
| t07 | `mgba_live_read_memory` | 内存 | ✅ 正常 |
| t08 | `mgba_live_read_range` | 内存 | ✅ 正常 |
| t09 | `mgba_live_run_lua` | Lua | ✅ 正常 |
| t10 | `mgba_live_start_with_lua` | 生命周期+Lua | ✅ 正常 |
| t11 | `mgba_live_dump_oam` | 调试 | ✅ 正常 |
| t12 | `mgba_live_dump_entities` | 调试 | ✅ 正常 |
| t13 | `mgba_live_stop` | 生命周期 | ✅ 修复后正常 |

---

## 各工具详细说明

### t01 — `mgba_live_start`

**作用**：启动一个 mGBA 实例，建立受控 session（带 Lua 脚本桥接），返回 PID 和 session 目录。

**调用示例**：
```python
mgba_live_start(rom="E:/Workspace/yugioh-ex2006-re/roms/2343.gba", session_id="p03")
```

**返回**：
```json
{"status":"started","session_id":"p03","pid":1580,"fps_target":120,"session_dir":"C:\\Users\\yushj\\.mgba-live-mcp\\runtime\\sessions\\p03"}
```

**要点**：
- `fps_target` 默认 120；传 `fast=true` 等价于 600（快进模式）
- session 目录下有 `session.json`（含 PID）、`scripts/mgba_live_bridge.lua`（核心桥接脚本）
- 底层使用 `cmd /c start` 规避 Windows Job Object（`KILL_ON_JOB_CLOSE`）限制

---

### t02 — `mgba_live_export_screenshot`

**作用**：将当前帧画面导出为 PNG 文件，并在响应中附带内联 base64 截图。

**调用示例**：
```python
mgba_live_export_screenshot(session="p03", out="C:\\temp\\screen.png")
```

**遇到的坑：Windows 绝对路径 Bug** ⚠️

`bridge.lua` 中的 `resolve_output_path` 函数只检查 Unix 绝对路径（`/` 开头），Windows 路径（`C:\...`）被误判为相对路径，拼接上 session 目录前缀，导致写入路径错误。

**错误行为**：
```lua
-- 原代码（有问题）
if string.sub(path, 1, 1) == "/" then
    return path   -- Unix 绝对路径走这里
end
-- C:\temp\screen.png 落到 else 分支，变成：
-- C:\Users\yushj\.mgba-live-mcp\runtime\sessions\p03\C:\temp\screen.png
```

**修复**（在两处 `bridge.lua` 同步修改）：
```lua
-- 新增 Windows 绝对路径检查
if string.sub(path, 1, 1) == "/" or string.match(path, "^%a:[/\\]") then
    return path
end
```

修复位置：
1. session 运行时副本：`~/.mgba-live-mcp/runtime/sessions/p03/scripts/mgba_live_bridge.lua`
2. uv cache 模板（新 session 来源）：`C:\Users\yushj\AppData\Local\uv\cache\archive-v0\5zGOx6CDrJNGtKdrIueX5\mgba_live_mcp\resources\mgba_live_bridge.lua`

> **注意**：两个路径是硬链接关系，修改任一个另一个同步变更。

**绕过方案**（不依赖 `out` 参数时）：截图通过 `mgba_live_status` 或 `mgba_live_input_tap` 的返回值内联获取更稳定。

---

### t03 — `mgba_live_input_tap`

**作用**：按下并释放一个按键（持续 N 帧），可选在释放后等待额外帧数，然后返回截图。

**按键名**：`A` / `B` / `START` / `SELECT` / `UP` / `DOWN` / `LEFT` / `RIGHT` / `L` / `R`

**调用示例**（按 START 进入主菜单，等待 120 帧稳定）：
```python
mgba_live_input_tap(key="START", frames=1, wait_frames=120, session="p03")
```

**验证**：返回截图可直接确认画面变化，用于验证按键是否生效。按下 START 后截图显示已进入主菜单（「DUEL」选项高亮）✅

---

### t04 — `mgba_live_input_set`

**作用**：持续按住一组按键（不释放），适合需要长按的场景（如菜单滚动）。

**调用示例**：
```python
mgba_live_input_set(keys=["DOWN"], session="p03")
```

**验证**：持续按住 DOWN，主菜单光标从「DUEL」向下滚动，截图可见光标移至「OPTIONS」✅

---

### t05 — `mgba_live_input_clear`

**作用**：释放指定按键（不传 `keys` 则释放全部）。

**调用示例**：
```python
mgba_live_input_clear(session="p03")  # 释放所有键
```

**验证**：释放 DOWN 后光标停止移动 ✅

---

### t06 — `mgba_live_status`

**作用**：返回 session 存活状态、当前帧号、内联截图（base64 PNG）。

**调用示例**：
```python
mgba_live_status(session="p03")
```

**返回示例**：
```json
{"alive":true,"pid":1580,"frame":6042,"screenshot":{"frame":6042,"data":"iVBOR..."}}
```

**要点**：截图数据嵌在返回 JSON 内，是查看实时画面最便捷的方式，无需额外参数。

---

### t07 — `mgba_live_read_memory`

**作用**：读取若干离散地址的字节值（每次一字节）。

**调用示例**（读 ROM header 游戏标题首 4 字节）：
```python
mgba_live_read_memory(addresses=[0x080000A0, 0x080000A1, 0x080000A2, 0x080000A3], session="p03")
```

**返回**：`[89, 85, 71, 73]` → ASCII `Y U G I` ✅

**适用场景**：监控少量散布的关键变量（如血量、手牌数等）。

---

### t08 — `mgba_live_read_range`

**作用**：读取连续内存范围，返回字节数组。

**调用示例**（读 ROM 标题区 16 字节）：
```python
mgba_live_read_range(start=0x080000A0, length=16, session="p03")
```

**返回**：`[89,85,71,73,79,72,87,67,84,48,54,0,0,0,0,0]` → `"YUGIOHWCT06\0\0\0\0\0"` ✅

游戏码位于 `0x080000AC`：`[66,89,54,69]` → `"BY6E"` ✅

**适用场景**：读取结构体、数组、字符串等连续数据块。

---

### t09 — `mgba_live_run_lua`

**作用**：在已运行的 mGBA 实例中执行任意 Lua 代码，返回 stdout 输出。

**调用示例**：
```python
mgba_live_run_lua(code='print(emu:currentFrame())', session="p03")
```

**验证的特性**：

| 特性 | 结果 |
|------|------|
| 读帧号 `emu:currentFrame()` | ✅ |
| 读寄存器 `emu:getRegister("r0")` | ✅ |
| 读内存 `emu:read8(addr)` | ✅ |
| `_G` 全局变量跨调用持久 | ✅（下次调用仍能访问上次设置的变量）|
| `callbacks:add("frame", fn)` 跨调用持久 | ✅（帧计数器在多次 run_lua 之间持续递增）|
| `callbacks:remove(id)` 移除回调 | ✅ |
| `emu:runFrame()` 主动推进帧 | ❌（"Function called from invalid context"）|
| `emu:screenshot(abs_path)` 截图 | ✅（Windows 绝对路径直接传入）|

**注意**：`_G` 全局状态在同一 session 的生命周期内持久。如需隔离，应启动新 session。

---

### t10 — `mgba_live_start_with_lua`

**作用**：启动 mGBA 的同时立即执行 Lua 代码（在 GBA 启动画面阶段就运行）。

**调用示例**：
```python
mgba_live_start_with_lua(
    rom="E:/Workspace/.../2343.gba",
    code='print("frame="..emu:currentFrame())',
    session_id="p03-lua-test"
)
```

**返回**：`frame=27`（GBA 启动动画阶段）✅

**适用场景**：需要从游戏启动时就开始监控（如初始化时的内存布局、早期寄存器状态）。

---

### t11 — `mgba_live_dump_oam`

**作用**：读取 OAM（Object Attribute Memory，`0x07000000`）中的前 N 个精灵条目，返回 `attr0` / `attr1` / `attr2` 三个属性字及 `bytes` 原始数据。

**调用示例**：
```python
mgba_live_dump_oam(count=20, session="p03")
```

**返回片段**（主菜单状态，20 个精灵）：
```json
{"index":14,"addr":7340084,"attr0":8300,"attr1":49248,"attr2":3136}
```

**解码规则**（GBA OAM 格式）：
```
attr0 低 8 位 = Y 坐标
attr1 低 9 位 = X 坐标
attr0 bit8-9  = 旋转/缩放标志
attr0 bit10-11= OBJ 模式（00=Normal, 01=Semi-transparent）
attr1 bit14-15= 尺寸（配合 attr0 bit14-15 决定宽高）
attr2 低 10 位 = 起始 tile 索引
attr2 bit10-11= 优先级
attr2 bit12-15= 调色板号（4bpp 模式下）
```

**验证**：精灵 14 Y=`0x6C`=108，对应主菜单底部图标行位置，与截图一致 ✅

---

### t12 — `mgba_live_dump_entities`

**作用**：从指定基址读取 N 个等长结构体，以字节数组形式返回，不做解释（由调用方解码）。

**调用示例**（Dragon's Roar 预组，GBA 地址 `0x09E5FA58`，每项 4 字节，共 28 项）：
```python
mgba_live_dump_entities(
    base=0x09E5FA58,  # = 166066776 十进制
    size=4,
    count=28,
    session="p03"
)
```

**deck_entry 解码规则**（`data/struct-decks.s` 中定义）：
```
16-bit LE 值 = so_code * 4 | copies
所以：
  so_code = value >> 2
  copies  = value & 0x3
后 2 字节 = 0x0000 填充
```

**验证结果**（前 3 项）：

| index | bytes | 16-bit LE | so_code | copies | 卡名 |
|-------|-------|-----------|---------|--------|------|
| 0 | `[225,63,0,0]` | 0x3FE1 | 4088 | 1 | Red-Eyes B. Dragon ×1 ✅ |
| 1 | `[9,68,0,0]` | 0x4409 | 4354 | 1 | Swords of Revealing Light ×1 ✅ |
| 7 | `[142,77,0,0]` | 0x4D8E | 4963 | 2 | Nobleman of Crossout ×2 ✅ |

28 条全部与 `data/struct-decks.s` 源码吻合 ✅

**适用场景**：调试时快照任意内存结构体数组（卡组、卡牌列表、怪物区域等）。

---

### t13 — `mgba_live_stop`

**作用**：终止指定 session 的 mGBA 进程，清理 active session 标记。

**遇到的坑：Windows `os.getpgid` Bug** ⚠️

```
AttributeError: module 'os' has no attribute 'getpgid'. Did you mean: 'getpid'?
```

`terminate_session_process` 使用了 Unix 专属的 `os.getpgid` + `os.killpg` 组合，Windows 不支持。

**修复**（`live_cli.py`，`terminate_session_process` 函数）：
```python
def terminate_session_process(pid: int, grace: float = 1.0) -> None:
    if sys.platform == "win32":
        import ctypes
        PROCESS_TERMINATE = 0x0001
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, 0, pid)
        if handle:
            ctypes.windll.kernel32.TerminateProcess(handle, 1)
            ctypes.windll.kernel32.CloseHandle(handle)
        return
    # ... 原 Unix 逻辑不变 ...
```

**修复位置**：
```
C:\Users\yushj\AppData\Local\uv\cache\archive-v0\H-avPZ5DfJEF8r9VXxrqe\Lib\site-packages\mgba_live_mcp\live_cli.py
```

**验证**：修复后 `mgba_live_stop` 返回 `alive_before=true, alive_after=false, stopped=true` ✅

---

## 遇到的坑汇总

### 坑 1：`resolve_output_path` 不识别 Windows 绝对路径

- **文件**：`mgba_live_bridge.lua`
- **现象**：`export_screenshot(out="C:\\temp\\x.png")` 写入到 `session_dir\C:\temp\x.png`
- **根因**：只检查 `/` 前缀，未处理 Windows `C:\` 路径
- **修复**：加 `string.match(path, "^%a:[/\\]")` 判断
- **影响**：每次新建 session 都会从 uv cache 复制 bridge.lua，已修复模板

### 坑 2：`terminate_session_process` 使用 Unix 专属 API

- **文件**：`live_cli.py`
- **现象**：调用 `mgba_live_stop` 时抛出 `AttributeError: os.getpgid`
- **根因**：`os.getpgid` / `os.killpg` 是 POSIX 进程组 API，Windows 无对应实现
- **修复**：`sys.platform == "win32"` 时改用 `ctypes.windll.kernel32.TerminateProcess`

### 坑 3：`pid_alive` 检查不可靠（先前 session 遗留）

- **现象**：session PID 对应的进程已死，但 `pid_alive` 仍返回 True
- **根因**：`live_cli.py` 中 `pid_alive` 只检查 PID 文件，未确认进程实际存在
- **修复**：已在先前 session（P0-2）中修复

### 坑 4：stdin 继承导致 mGBA 子进程意外退出

- **现象**：mGBA 启动后立即退出
- **根因**：`live_controller.py` 启动子进程时未设置 `stdin=subprocess.DEVNULL`，mGBA 尝试读 stdin 失败
- **修复**：已在先前 session 中修复

### 坑 5：`emu:runFrame()` 不能在脚本回调上下文中调用

- **现象**：`run_lua` 执行 `emu:runFrame()` 时报 `"Function called from invalid context"`
- **根因**：mGBA Lua 脚本运行在帧回调上下文中，不允许递归触发帧推进
- **绕过**：用 `fps_target` 参数（如 `fast=true`）控制速度，或直接等待帧回调积累

### 坑 6：mGBA Lua API 无内存写入回调

- **现象**：`emu:addMemoryWatchpoint` 返回 nil；`callbacks` 无内存变更事件
- **根因**：mGBA Lua API 只暴露帧/重置/按键等事件，不提供内存访问断点
- **影响**：P0-2 中无法用 Lua 监听 DMA，需回退到 GDB watchpoint 方案

---

## 结论

13 个工具全部验证通过（2 个经修复后通过）。修复均已写入 uv cache 模板，后续新 session 直接可用。

推荐使用组合：
- **启动 + 快速到达游戏内状态**：`mgba_live_start` → `input_tap(START)` → `mgba_live_status`（确认截图）
- **读取大块数据**：`mgba_live_read_range`
- **监控少量关键地址**：`mgba_live_read_memory`
- **任意调试逻辑**：`mgba_live_run_lua`（全局状态持久，可注册帧回调）
- **需要 GDB 级别的监控**（内存写入、断点）：配合 P0-1 方案，mGBA `-g 2345` + GDB watchpoint

---

## 相关文档

- [P0-1 GDB DMA3 Watchpoint 走查文档](p0-1-gdb-dma3-watchpoint-walkthrough.md)
- [mGBA MCP 设置指南](mgba-mcp-setup.md)
- [mGBA MCP Lua 教程](mgba-mcp-lua-tutorial.md)
- [mGBA GDB Stub 已知问题](mgba-gdb-stub-pitfalls.md)
