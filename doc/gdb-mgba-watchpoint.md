# GDB + mGBA watchpoint 调试记录

目标：通过 GDB watchpoint 监听游戏 ROM 内存写入操作。  
工具：mGBA 模拟器内建 GDB stub + devkitARM arm-none-eabi-gdb 14.1 + 自制 RSP 协议代理。

---

## 一、背景与目标

GBA ROM 被映射到地址 `0x08000000`，正常情况下是只读区域。  
EWRAM（扩展工作内存）位于 `0x02000000`，游戏运行期间频繁读写。

**目标**：用 GDB 的硬件 watchpoint 捕获游戏写入这两段内存时的现场（PC、寄存器、调用栈）。

mGBA 通过命令行参数 `-g <端口>` 启动一个 GDB stub（GDB Remote Serial Protocol，RSP）服务，GDB 通过 `target remote` 连接后可设置断点、watchpoint、读写寄存器内存。

---

## 二、GDB stub 与 GDB 14.1 的协议不兼容问题

直接用 `arm-none-eabi-gdb` 连接 mGBA stub，握手阶段就会失败。经过逐包抓取分析，发现以下 7 处不兼容：

| # | 问题 | mGBA 行为 | GDB 14.1 期望 | 修复方式 |
|---|------|-----------|---------------|---------|
| 1 | vMustReplyEmpty | 回复 `$timeout#07` | 回复空包 `$#00` | 代理替换 |
| 2 | 停止回复格式 | `$S02#b5`（无线程信息） | `$T02thread:01;` | 代理替换 |
| 3 | qSupported 能力声明 | 声明了 `qXfer:` 和 `QStartNoAckMode+` 但实际不支持 | 声明的能力必须可用 | 代理过滤掉不支持的能力 |
| 4 | `$g` 寄存器布局 | 68 字节（r0-r15 + cpsr） | 168 字节（r0-r15 + FPA f0-f7 + fps + cpsr） | 代理插入 100 字节 FPA 零占位 |
| 5 | `$?` 初始停止回复 | mGBA 在后台延迟几百毫秒才发出，期间 GDB 超时 | 立即回复 | 代理立即合成 `T02thread:01;` 回复，转发给 mGBA 再吞掉其延迟包 |
| 6 | `qOffsets` | 回复格式不合法 | 标准 `Text=0;Data=0;Bss=0` | 代理拦截并自行回复，吞掉 mGBA 的坏回复 |
| 7 | GDB 流水线 | mGBA 一次只能处理一个 RSP 包 | GDB 会在一个 TCP 包里发多个命令（流水线） | 代理用缓冲区序列化，每次只向 mGBA 发一个完整包 |

---

## 三、gdb_proxy.py 协议代理设计

**架构**：单线程 `select()` 循环，监听 2346 端口，GDB 连接后代理转发到 mGBA 2345 端口。

```
GDB  ←→  :2346 [gdb_proxy.py]  ←→  :2345 mGBA GDB stub
```

**关键函数**：

- `fix_mgba(data, state)` — 修复 mGBA→GDB 方向的所有格式问题
- `handle_gdb_to_mgba(data, gdb_sock, state)` — 拦截 `$?`、`qOffsets`，直接回复 GDB
- `extract_one_packet(buf)` — 从缓冲区提取第一个完整 RSP 包，防止截断包破坏 mGBA 状态机
- `connect_mgba(host, port, timeout)` — 显式 `AF_INET` 连接（绕过 Windows IPv6 解析问题）
- `session(gdb_sock)` — 主会话逻辑，`select()` 双向转发

**suppress_stop_reply 状态机**：

```
发 $?                      ← 拦截，立即合成 T02 回复 GDB
  ↓ 同时转发 $? 给 mGBA
  mGBA 延迟发 S02
  ↓ fix_mgba 检测到 suppress_stop_reply=True
  吞掉 S02，设 swallowed_stop=True
  ↓ session 主循环检测到 swallowed_stop
  清除 waiting，继续处理 gdb_buf 中下一个包
```

---

## 四、调试过程中遇到的坑

### 坑 1：mGBA 每次启动只允许一次 TCP 连接

mGBA GDB stub 采用单连接模式：客户端断开后，stub **永久关闭**，端口停止监听。  
后续任何连接尝试都会被拒绝（`errno 10061 Connection refused`）。

**影响**：
- 每次调试结束后必须完全重启 mGBA
- 任何"试探性连接"（探测端口是否可用）都会消耗唯一的连接槽

**错误示例（已规避）**：

```python
# ❌ 用 TcpClient 探测端口，消耗了唯一连接槽
$t = New-Object System.Net.Sockets.TcpClient
$t.Connect('127.0.0.1', 2345)   # 连接成功后 stub 关闭！
$t.Close()
```

### 坑 2：mGBA GDB stub 接受连接后不立即响应命令

mGBA 接受 TCP 连接后，**必须等游戏 CPU 开始执行**（大约 2-3 秒）才会进入 RSP 命令处理循环。  
如果 GDB 在游戏运行前发送 `$qSupported`，mGBA 不响应，GDB 超时断开。

**解决方案**：启动 mGBA 后等待 5-7 秒，确认游戏已跑起来再连接。

### 坑 3：Windows Python socket — IPv6 解析问题

```python
# ❌ 在 Windows 上可能解析为 IPv6，导致连接超时
socket.create_connection(('127.0.0.1', 2345))

# ✅ 正确做法：显式指定 AF_INET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 2345))
```

### 坑 4：gdb_buf 含截断的第二个包

GDB 在未收到 ACK 时会重传，导致 TCP 缓冲区中出现：

```
+$qSupported:...#xx$qSupported:...#xx   ← 同一命令两次，第二次可能不完整
```

代理若把整个 `gdb_buf` 发给 mGBA，截断的第二包会破坏 mGBA 的 RSP 状态机。

**修复**：`extract_one_packet()` 每次只取第一个完整包，余下保留在缓冲区：

```python
def extract_one_packet(buf):
    # 查找 '$'，找到配对的 '#xx'，提取完整包+前导 ACK
    # 返回 (packet_bytes, remaining_buf)
```

### 坑 5：suppress_stop_reply 死锁

**原始错误代码**：

```python
if b'$?#3f' in data:
    # 立即回复 GDB，不转发给 mGBA
    gdb_sock.sendall(reply)
    state['suppress_stop_reply'] = True
    return b''   # ❌ 不发给 mGBA → mGBA 不发 S02 → flag 永远 True
```

**后果**：`waiting=True` 永远不清除，会话死锁，后续所有包都被丢弃。

**修复**：

```python
return data   # ✅ 转发给 mGBA，让其发 S02；fix_mgba 吞掉 S02 时清除 waiting
```

### 坑 6：mGBA Qt 版单例模式

`mGBA.exe`（Qt 版）同一台机器**只允许运行一个实例**。第二次启动时进程立刻退出（无错误消息）。

**现象**：`Start-Process` 返回成功（PID 分配），但 `$p.HasExited` 在 3 秒后已为 `True`。

**绕过尝试**：改用 `mgba-sdl.exe`（SDL 版，无单例限制）。  
但 `mgba-sdl.exe` 的 `-g` 参数**不接受端口号**（固定用 2345），且若 2345 已被占用则报错 `Couldn't open socket`。

**根本问题**：已有 mgba-live 会话（PID 14176）持续运行，占用了 mGBA 单例名额，且 2345 端口在其他进程释放后也无法被 SDL 版重用。

### 坑 7：代理多实例残留

反复 `Start-Process python gdb_proxy.py` 会留下多个代理进程，全部监听 2346 端口（`SO_REUSEADDR`）。  
GDB 连接到的是**最早启动的旧版本代理**，而非最新修复版。

**排查方式**：

```powershell
netstat -ano | Select-String ":2346"
# 找到所有 PID，逐一 Stop-Process -Id <pid>
```

---

## 五、GDB 脚本必须禁用的远程包

直接连接时 GDB 14.1 会发送 mGBA 不支持的协议包，必须在 `target remote` **之前**禁用：

```gdb
set architecture armv4t
set remote verbose-resume-packet off
set remote verbose-resume-supported-packet off
set remote noack-packet off
set remote target-features-packet off
set remote memory-map-packet off
set remote trace-status-packet off

target remote localhost:2346
```

---

## 六、成功运行记录

以下是完整成功的操作流程（历史上完成过一次）：

```
1. mGBA 以 -g 2345 启动，游戏运行 ~5 秒
2. gdb_proxy.py 启动，监听 2346
3. arm-none-eabi-gdb -batch -x gdb_watch_rom.gdb

握手序列（代理日志）：
  ✓ 已连接 mGBA :2345
  ✓ S02 → T02thread:01 (增强停止包)
  ✓ $? 拦截：立即回复 T02thread:01
  ✓ 过滤 qSupported 能力
  ✓ qOffsets：给 GDB 发正确回复
  ✓ $g 布局修正：68B(mGBA) → 168B(GDB14 armv4t)

GDB 输出：
  info registers → sp=0x03007F00（真实 GBA 寄存器）
  Watchpoint 1: *(int *) 0x2000000
  Watchpoint triggered: Old = 0x0, New = 0x12345678
```

EWRAM（`0x02000000`）watchpoint 成功触发。ROM（`0x08000000`）watchpoint 由于是只读区域，正常情况下不触发。

---

## 七、当前状态与遗留问题

### 已解决

- [x] 所有 RSP 协议不兼容（共 7 处）
- [x] suppress_stop_reply 死锁
- [x] extract_one_packet 防截断包
- [x] Windows IPv6 socket 问题
- [x] 代理多实例残留

### 遗留问题

- [ ] **mGBA 单例限制**：mgba-live 会话（PID 14176）占用单例名额，无法同时启动第二个 Qt 版 mGBA
- [ ] **端口 2345 不可复用**：stub 一旦断开即永久关闭，必须完整重启 mGBA
- [ ] **验证待完成**：最后一轮修复（swallowed_stop 清 waiting + extract_one_packet 路径）尚未完整跑通

### 替代方案（未实施）

若 GDB stub 方案因单例限制无法继续，可考虑：

1. **mGBA Lua 内存回调**：在 mgba-live 会话里注入 Lua 脚本，用 `callbacks:add('memoryRead'/'memoryWrite', ...)` 监听内存访问，不依赖 GDB stub
2. **mGBA Python Scripting API**：mGBA 0.11+ 支持 Python 脚本，可直接访问内存回调

---

## 八、文件清单

| 文件 | 说明 |
|------|------|
| `session-state/.../files/gdb_proxy.py` | RSP 协议代理，修复所有已知不兼容 |
| `session-state/.../files/gdb_watch_rom.gdb` | GDB 批处理脚本（含 watchpoint 设置） |
| `session-state/.../files/test_mgba.py` | mGBA GDB stub 行为诊断脚本 |
| `session-state/.../files/proxy.log` | 代理运行日志 |

---

## 九、参考资料

- [mGBA GDB stub 源码](https://github.com/mgba-emu/mgba/blob/master/src/debugger/gdb-stub.c)
- [GDB Remote Serial Protocol 规范](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Remote-Protocol.html)
- devkitARM `arm-none-eabi-gdb` 14.1，安装于 `<devkitPro安装目录>\devkitARM\bin\`
