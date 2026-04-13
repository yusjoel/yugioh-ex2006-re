# P0-1：纯命令行 GDB + DMA3 Watchpoint 完整流程记录

## 目标

验证以下工具链可端到端跑通，不依赖任何 MCP 工具：

1. 通过 PowerShell 脚本启动 mGBA（GDB stub 模式），进程可持久存活
2. 用 `arm-none-eabi-gdb` 连接 mGBA stub
3. 设置 DMA3 源地址寄存器 watchpoint，成功捕获一次中断

---

## 涉及文件

| 文件 | 用途 |
|------|------|
| `tools/_preflight-mgba.ps1` | 启动前预检：关闭已有 mGBA、确认端口空闲 |
| `tools/start-mgba-gdb-nosave.ps1` | 启动 mGBA（无存档冷启动） |
| `tools/start-mgba-gdb-ss1.ps1` | 启动 mGBA（加载 `roms/2343.ss1` 存档） |
| `tools/wait-mgba-ready.ps1` | 等待 GDB stub 端口就绪 + CPU 热身 |
| `doc/dev/scripts/gdb_dma_watch.gdb` | GDB 自动化脚本：设置 watchpoint、捕获触发 |
| `tools/arm-none-eabi-gdb.exe` | GDB 10.2，唯一兼容 mGBA stub 的版本 |

---

## GBA DMA3 寄存器背景

GBA 有 4 个 DMA 通道，DMA3 是通用 DMA：

| 地址 | 名称 | 说明 |
|------|------|------|
| `0x040000D0` | DMA3SAD | 源地址（CPU 在启动 DMA 前写入此寄存器） |
| `0x040000D4` | DMA3DAD | 目标地址 |
| `0x040000D8` | DMA3CNT_L | 传输字数 |
| `0x040000DA` | DMA3CNT_H | 控制寄存器（写入此寄存器触发 DMA） |

**监听 DMA3SAD（`0x040000D0`）的意义**：CPU 设置 DMA 传输时必须先写 SAD，因此 watchpoint 在 DMA 实际发生之前触发，此时可以读到完整的调用上下文（PC、LR、参数寄存器）。

**注意**：`watch *(unsigned int*)0x040000D0` 监听的是 **CPU 写 DMA 设置寄存器**的动作，而不是 DMA 搬运数据本身。

---

## 完整操作步骤

### 步骤 1：启动 mGBA（带存档）

```powershell
# 必须使用 PowerShell 7 执行（系统自带 PS 5.1 对中文脚本有编码问题）
& "D:\Program Files\PowerShell\7\pwsh.exe" -File tools\start-mgba-gdb-ss1.ps1
```

预期输出：
```
[preflight] 发现 1 个 mGBA 实例正在运行：
  PID 8008
[preflight] 正在关闭...
[preflight] mGBA 已关闭
[preflight] 端口 2345 未被占用，OK
[start] mGBA 已启动（+ss1 存档，通过 cmd /c start），启动器 PID: 7864
[start] 脚本立即退出（保持 mGBA 独立存活）
[start] 下一步（新命令）：& tools\wait-mgba-ready.ps1
```

### 步骤 2：等待 GDB stub 就绪

```powershell
& "D:\Program Files\PowerShell\7\pwsh.exe" -File tools\wait-mgba-ready.ps1
```

预期输出：
```
[wait] 等待端口 2345 LISTENING（最多 20s）...
[wait] 端口 2345 已就绪（1s）
[wait] 等待 8s，让游戏 CPU 进入 RSP 循环...
[wait] 就绪！现在可以连接 GDB：
  tools\arm-none-eabi-gdb.exe --batch -x doc\dev\scripts\gdb_dma_watch.gdb
```

### 步骤 3：运行 GDB 脚本

```powershell
& "tools\arm-none-eabi-gdb.exe" --batch -x "doc\dev\scripts\gdb_dma_watch.gdb"
```

预期输出（成功）：
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

---

## GDB 脚本内容（`doc/dev/scripts/gdb_dma_watch.gdb`）

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

---

## 遇到的坑

### 坑 1：mGBA 进程被 PowerShell Job Object 杀死

**现象**：运行启动脚本后 mGBA 窗口立即关闭，或端口 2345 从未出现。

**原因**：Copilot CLI 将 PowerShell 运行在 Windows Job Object 中，设置了 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`。脚本退出时 Job Object 关闭，所有子进程被强制终止。`UseShellExecute=$true` 在 Vista+ 上**不能**阻止 Job Object 继承。

**解决方案**：使用 `cmd /c start` 启动 mGBA：

```powershell
$args = "/c start `"`" `"$mgba`" -g `"$rom`""
Start-Process -FilePath "cmd.exe" -ArgumentList $args -PassThru
```

`cmd start` 内部调用 `CreateProcess` 时带有 `CREATE_BREAKAWAY_FROM_JOB` 标志，使子进程完全脱离父 Job Object。脚本退出后 mGBA 独立存活。

详见：`doc/dev/powershell-job-object-mgba.md`

---

### 坑 2：端口就绪 ≠ GDB 可连接

**现象**：`netstat` 显示 2345 LISTENING，但 GDB 立即报 `Connection timed out`。

**原因**：mGBA 启动后先绑定端口，但游戏 CPU 还未进入 RSP 处理循环，GDB 握手失败。

**解决方案**：端口就绪后额外等待 8 秒（`wait-mgba-ready.ps1` 中实现）。

---

### 坑 3：GDB 脚本不能有 UTF-8 BOM

**现象**：GDB 执行时第一行报 `Undefined command: ""`，随后所有命令失败。

**原因**：Windows 记事本和部分编辑器默认保存 UTF-8 with BOM（`EF BB BF`），GDB 无法识别 BOM，将其当作命令解析。

**解决方案**：写入 GDB 脚本时使用无 BOM 的 UTF-8：

```powershell
$enc = New-Object System.Text.UTF8Encoding $false   # $false = 无 BOM
[System.IO.File]::WriteAllText($path, $content, $enc)
```

---

### 坑 4：条件 watchpoint 导致大量 packet error

**现象**：设置 `condition 1 *(unsigned int*)0x040000D0 >= 0x08000000` 后，GDB 输出连续的 `Ignoring packet error, continuing...`，脚本卡住无输出。

**原因**：mGBA GDB stub 实现较简单。每次 watchpoint 触发时，GDB 需要通过 RSP 协议请求 stub 在目标机上对条件表达式求值（读取 0x040000D0 内存）。在游戏高频触发 DMA3 的情况下，stub 来不及响应求值请求，导致 RSP 包超时堆积。

**解决方案**：去掉条件，让所有触发都停下，在 GDB 脚本或事后日志中过滤 ROM 地址范围。

---

### 坑 5：devkitARM GDB 14.1 不兼容 mGBA stub

**现象**：使用 `devkitARM\bin\arm-none-eabi-gdb.exe`（GDB 14.1）连接，握手失败或断点/watchpoint 完全无效。

**原因**：GDB 14.x 修改了 RSP 协议中的若干细节（如 vFile、qXfer、multiprocess 等），mGBA 0.10.x stub 未跟进这些变化，导致协议不兼容。

**解决方案**：只使用项目自带的 `tools/arm-none-eabi-gdb.exe`（GDB 10.2），此版本与 mGBA stub 完全兼容。

---

### 坑 6：存档模式下 VRAM watchpoint 不触发

**现象**：使用 `start-mgba-gdb-ss1.ps1` 带存档启动，设置 VRAM `0x06000040` watchpoint，50 次 continue 无触发。

**原因**：存档（savestate）是游戏运行到卡片列表界面后的快照，VRAM 内卡图数据此时已经写入完毕，恢复存档后游戏不再重写这块内存。

**解决方案**：
- 若要捕获**卡图写入 VRAM**的过程 → 改用 `start-mgba-gdb-nosave.ps1`（冷启动）
- 若只需验证 **DMA3 watchpoint 能否触发** → 存档模式即可（游戏主循环中有高频 DMA3 调用）

---

## 捕获结果分析

### 带存档时的 DMA3SAD 触发（验证 watchpoint 机制）

```
PC  = 0x3004db4   → IWRAM 中的代码（游戏主循环）
LR  = 0x3000144
DMA3SAD = 0x84400000   → 非 ROM 地址（高 4 位为 0x8，但位于 I/O 镜像区）
DMA3DAD = 0xa101a101
```

- PC 在 `0x03xxxxxx`（IWRAM），说明是游戏运行时动态调度的 DMA
- `0x84400000` / `0xb6400000` 交替写入，推测是音频或背景图层的循环 DMA
- 此触发**不是卡图 DMA**，但证明 watchpoint 机制完全正常

### 无存档时的 VRAM watchpoint 触发（卡图 CPU copy）

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

## 小结：工具链已验证功能

| 功能 | 状态 | 备注 |
|------|------|------|
| `cmd /c start` 启动 mGBA，进程存活 | ✅ | 解决 Job Object 问题 |
| 预检脚本关闭旧实例、确认端口空闲 | ✅ | `_preflight-mgba.ps1` |
| `wait-mgba-ready.ps1` 端口+热身等待 | ✅ | 8s warmup 必要 |
| GDB 10.2 连接 mGBA stub（无存档） | ✅ | |
| GDB 10.2 连接 mGBA stub（带存档） | ✅ | |
| DMA3SAD hardware watchpoint 触发 | ✅ | `watch *(unsigned int*)0x040000D0` |
| VRAM hardware watchpoint 触发 | ✅ | `watch *(unsigned int*)0x06000040` |
| `hook-stop` 自动打印寄存器 | ✅ | |
| 无 BOM GDB 脚本正常执行 | ✅ | `UTF8Encoding($false)` |

---

## 下一步

P0-1 完成后，下一阶段为 **P0-2：通过 mGBA MCP 重走上述流程**，验证 MCP 工具的截图、按键模拟、内存读取等功能。
