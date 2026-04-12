# mGBA MCP 方案对比分析

本文档对比 mgba-live-mcp 和 pymgba-mcp 两套 MCP 方案的架构与能力，重点调查"是否支持监听内存读取"这一需求。

---

## 一、背景

在动态分析 GBA ROM 时，理想的工作流是：

```
触发游戏动作 → 监听 CPU 从 ROM 读取了哪些地址 → 精确定位数据来源
```

经过对 mgba-live-mcp 的实际测试，发现其无法监听内存读取（详见 §三）。  
本文进一步调查 pymgba-mcp 是否能弥补这一缺口。

---

## 二、架构对比

| | mgba-live-mcp | pymgba-mcp |
|--|--------------|-----------|
| **项目地址** | https://github.com/penandlim/mgba-live-mcp | https://github.com/zenitraM/pymgba-mcp |
| **底层接口** | mGBA **Lua 脚本引擎**（通过 GUI 工具栏加载） | mGBA **原生 Python cffi 绑定**（直接调用 mGBA C API）|
| **运行方式** | 需要 Qt 窗口，mGBA 作为独立进程运行 | 无头模式，Python 进程内嵌持有 mGBA 核心 |
| **打包方式** | pip 安装，兼容 Windows | Nix flake，主要面向 Linux/macOS |
| **Windows 可用性** | ✅ 可用（需少量修复，见 `mgba-mcp-setup.md`）| ⚠️ 困难（需自行编译 mGBA Python 绑定）|

---

## 三、功能对比

### 3.1 已实现工具

| 功能 | mgba-live-mcp | pymgba-mcp |
|------|:---:|:---:|
| 加载 ROM | ✅ | ✅ |
| 截图 | ✅ | ✅ |
| 模拟按键 | ✅ | ✅ |
| 读取内存 | ✅ | ✅ |
| 写入内存 | ✅ | ✅ |
| OAM 查看 | ✅ | ✅ |
| 保存/加载状态 | ✅ | ✅ |
| **执行 Lua 脚本** | ✅ | ❌ |
| **CPU 寄存器读取** | ❌ | ✅ |
| **单步执行（step）** | ❌（注册但无效）| ✅ |
| **设置断点/watchpoint** | ❌ | ❌（README 提及但代码未实现）|
| **监听内存读取** | ❌ | ❌ |

> pymgba-mcp 的 README 写有 "Set breakpoints" 功能，但检查 `emulator.py` 和 `server.py`
> 源码后确认：工具列表中**没有** `set_breakpoint`、`add_watchpoint` 等任何断点相关工具，
> 该功能**未实现**，为 vibecoded 文档遗留描述。

### 3.2 关键差异：step() 和寄存器

pymgba-mcp 通过 cffi 直接调用 `mCore.step(mCore)`，因此 `step()` 真实有效；  
而 mgba-live-mcp 的 `emu:step()` 在 `run_lua` 一次性执行环境中不推进帧，实际无效。

这意味着 pymgba-mcp 更适合**指令级单步调试**场景。

---

## 四、为什么两个方案都无法监听读取

### 4.1 mgba-live-mcp（Lua 路径）

mGBA Lua 脚本引擎的 `callbacks` 对象支持的事件类型（[官方文档](https://mgba.io/docs/scripting.html)）：

> `alarm` / `crashed` / `frame` / `keysRead` / `reset` / `savedataUpdated` / `sleep` / `shutdown` / `start` / `stop`

**`read`、`write`、`exec` 根本不在列表中**，是 mGBA Lua API 本身没有这些功能，与编译标志无关。

| 测试写法 | 结果 |
|---------|------|
| `callbacks:add("read", fn)` | 注册不报错，但**永不触发**（静默失效）|
| `callbacks:add("memory.read", fn, base, size)` | **报错**（参数数量不匹配 C 函数签名）|
| `callbacks:add("frame", fn)` | **有效**，每帧触发 |

### 4.2 pymgba-mcp（Python cffi 路径）

pymgba-mcp 使用 `mgba._pylib`（cffi 直接绑定 mGBA C API），理论上可以调用 mGBA 内部调试器接口：

```python
# 理论上存在的 mGBA C API
lib.mDebuggerAddBreakpoint(debugger, addr, type)
lib.ARMDebugBreakpoint(...)
```

但 pymgba-mcp 的代码中**完全未调用**这些接口，也没有对外暴露断点工具。  
因此同样**无法监听内存读取**。

### 4.3 根本原因

```
mGBA 没有通过任何脚本/绑定接口把"内存访问回调"暴露出来。
```

无论走 Lua 还是 Python cffi，两条路都在 API 层面不支持。  
这不是某个 MCP 实现的能力缺陷，而是 mGBA 设计边界。

---

## 五、要实现监听读取，必须走的路

### 方案 A：mGBA 内置 GUI 调试器（推荐，手动）

菜单 → **Tools → Debugger → Watchpoints**

- 支持读/写/读写三种类型的 watchpoint
- 触发时暂停模拟，显示访问地址和当前 PC
- **缺点**：需要手动交互，无法通过 MCP 自动化

### 方案 B：GDB Remote Stub（可脚本化）

启动 mGBA 时加 `-g <端口>` 开启 GDB stub，然后用 GDB 连接：

```bash
# 启动 mGBA 并监听 GDB 连接
mGBA.exe -g 2345 rom.gba

# GDB 连接
(gdb) target remote :2345
(gdb) rwatch *0x08114A90          # 监听 ROM 某地址的读取
(gdb) watch *0x06000000           # 监听 VRAM 写入
(gdb) commands                    # 触发时自动执行命令
```

- **优点**：完全可脚本化，触发时可自动记录 PC / 寄存器
- **缺点**：需要 GDB，Windows 上需要 arm-none-eabi-gdb（devkitARM 自带）

### 方案 C：扩展 pymgba-mcp（需开发）

基于 pymgba-mcp 的 cffi 架构，添加断点工具：

```python
# 在 emulator.py 中添加
def add_watchpoint(self, address: int, size: int, watch_type: str) -> int:
    debugger = ffi.cast("struct mDebugger*", self._core.debugger)
    bp = ffi.new("struct mDebugBreakpoint*")
    bp.address = address
    bp.type = lib.WATCHPOINT_READ if watch_type == "read" else lib.WATCHPOINT_WRITE
    return lib.mDebuggerAddBreakpoint(debugger, bp)
```

- **优点**：可集成进 MCP，实现全自动化监听
- **缺点**：需要自行开发 + 重新编译 mGBA（Windows 困难）；API 细节需参考 mGBA 源码

---

## 六、结论

| 方案 | 监听读取 | 自动化 | Windows 可用 |
|------|:---:|:---:|:---:|
| mgba-live-mcp（现用）| ❌ | ✅ | ✅ |
| pymgba-mcp（调查）| ❌ | ✅ | ⚠️ |
| mGBA GUI 调试器 | ✅ | ❌（手动）| ✅ |
| GDB stub | ✅ | ✅ | ✅（devkitARM 自带 gdb）|
| 扩展 pymgba-mcp | ✅（需开发）| ✅ | ⚠️ |

**当前项目推荐路径**：
- 日常自动化分析（VRAM 差分、内存轮询）→ 继续使用 mgba-live-mcp
- 需要精确追踪 ROM 读取地址时 → 使用 **mGBA GUI 调试器** 或 **GDB stub（arm-none-eabi-gdb）**
