# GDB Watchpoint 实验记录：卡图 ROM 数据定位

**日期**: 2026-04-13  
**目标**: 确定卡牌大图在 ROM 中的存储位置（压缩块地址）  
**工具**: GDB 10.2（tools/arm-none-eabi-gdb.exe）+ mGBA GDB stub（端口 2345）

> **后续进展**：本文为 P0 阶段的早期探索记录（含若干已证不通路的方案）。
> 卡图定位的最终结论与导出流程见 `p1-phase-b2-findings.md`。

---

## 背景

卡牌详情页加载时，游戏通过 BIOS SWI（LZ77=0x11 或 Huffman=0x13）将 ROM 中的压缩卡图数据解压后写入 VRAM BG2（0x06000000）。需要找到 ROM 中压缩数据块的起始地址。

已知信息（来自 `doc/analysis/card-detail-page.md`）：
- BG2 tile 数据区：`0x06000000`，tiles 1–36，256色，共 2304 字节
- 解压来源：BIOS SWI 0x11（LZ77）或 0x13（Huffman）
- 触发条件：在卡牌列表页按 A 键进入详情页

---

## 实验一：DMA3 源地址 Watchpoint ✅ 技术可行，但卡图不走 DMA

**脚本**: `doc/dev/scripts/gdb_watch_dma3sad.gdb`  
**监听地址**: `0x040000D4`（DMA3SAD，I/O 寄存器）  
**结果**: Watchpoint **成功触发**，I/O 地址（0x04xxxxxx）完全支持

**发现**：
- DMA3 频繁触发，来源均为 ROM 地址 `0x080f4ff0` 附近（VBlank 背景填充）
- 用条件 `$pc != 0x080f4ff0` 过滤后，多次按 A 键仍无新触发
- **结论**：卡牌大图加载不使用 DMA3，走的是 BIOS SWI 解压

**mGBA stub 支持情况**：✅ 支持 I/O 寄存器区域（0x04xxxxxx）的 watchpoint

---

## 实验二：VRAM BG2 Watchpoint ❌ mGBA stub 不支持

**脚本**: `doc/dev/scripts/gdb_watch_vram_bg2.gdb`  
**监听地址**: `0x06000000`（VRAM BG2 tile 起始）  
**结果**: GDB 报告 watchpoint 设置成功，但按 A 键后**从未触发**

**附加问题**：脚本中误写了两次 `target remote`，第二次连接触发 `vMustReplyEmpty` 协议错误（已修复）

**结论**：mGBA GDB stub **不支持** VRAM 地址（0x06xxxxxx）的 watchpoint

---

## 实验三：EWRAM Watchpoint ❌ mGBA stub 不支持

**脚本**: `doc/dev/scripts/gdb_watch_ewram_02000000.gdb`  
**监听地址**: `0x02000000`（EWRAM 起始）  
**结果**: GDB 报告 watchpoint 设置成功，但按 A 键后**从未触发**

**历史数据**（旧版脚本，游戏刚启动时曾触发一次）：
```
pc  = 0x03005720（IWRAM 中的初始化例程）
lr  = 0x080f4db0（ROM 地址，调用方）
r4  = 0x02000000（EWRAM 地址）
new = 89（0x59）
```
此触发属于游戏启动初始化，与卡图无关。

**结论**：mGBA GDB stub **不支持** EWRAM 地址（0x02xxxxxx）的 watchpoint（启动时触发可能是特例或 mGBA 版本差异）

---

## mGBA GDB Stub Watchpoint 支持范围（修订）

> **2026-04-13 修订**：经阅读 mGBA 源码，原先"VRAM/EWRAM 不支持"的结论是**误判**，见下方源码分析。

| 地址范围 | 区域 | Watchpoint 支持 |
|----------|------|----------------|
| 0x04xxxxxx | I/O 寄存器 | ✅ 支持（实验验证） |
| 0x08xxxxxx | ROM | ✅ 支持（hbreak 测试过） |
| 0x06xxxxxx | VRAM | ✅ **理论支持**（失败另有原因，见下） |
| 0x02xxxxxx | EWRAM | ✅ **理论支持**（失败另有原因，见下） |
| 0x03xxxxxx | IWRAM | ✅ 理论支持（未测试） |
| 0x00000008 | BIOS SWI 向量 | ❌ 不支持（hbreak 不工作） |

---

## 源码分析：Watchpoint 实现机制（2026-04-13）

阅读 `src/arm/debugger/memory-debugger.c` 后，watchpoint 的实现方式已确认：

**机制**：通过替换 CPU 的内存访问函数指针（shim）实现，**对所有地址均有效**。

```c
// ARMDebuggerInstallMemoryShim() — 将所有内存访问替换为带 watchpoint 检查的 shim
debugger->cpu->memory.store32 = DebuggerShim_store32;
debugger->cpu->memory.store16 = DebuggerShim_store16;
debugger->cpu->memory.store8  = DebuggerShim_store8;
// ... load 同理
```

每次内存读写都经过 `_checkWatchpoints()`，按地址范围匹配——**无任何区域白名单/黑名单**。  
BIOS LZ77 解压（`src/gba/bios.c` `_unLz77`）同样使用 `cpu->memory.store8/store16`，**也会触发 watchpoint**。

---

## VRAM/EWRAM Watchpoint 失败的真实原因（修订）

之前实验失败不是 mGBA 的限制，而是以下三重问题叠加：

### 原因 1：监听地址错误 ⭐ 最可能

- 之前监听 `0x06000000`（tile 0，背景色/调色板区域）
- 卡图数据从 **tile 1** 开始写入：`0x06000040`
- 如卡图占 tiles 1–36，写入范围是 `0x06000040`–`0x060008FF`

### 原因 2：GDB stub 强制 1 字节范围

阅读 `src/debugger/gdb-stub.c` `_setBreakpoint()` 源码：

```c
struct mWatchpoint watchpoint = {
    .minAddress = address,
    .maxAddress = address + 1   // ← 始终只监 1 字节，忽略 GDB 协议中的 size 参数
};
```

GDB 的 `watch *(uint*)0x06000040` 命令会带 size=4，但 stub **丢弃 size**，只监 1 字节。  
要覆盖 2304 字节的卡图区域，需要设 2304 个 watchpoint，不现实。

### 原因 3：存档预加载

使用 `2343.ss1` 快照启动时，卡图可能已在快照保存前解压到 VRAM，进入游戏后 VRAM 内容直接恢复，按 A 只是切换显示层，不触发新的写入。

---

## 已排除的方案

| 方案 | 状态 | 原因 |
|------|------|------|
| DMA3 watchpoint | ❌ 排除 | 卡图不走 DMA3 |
| BIOS SWI 向量断点（0x8）| ❌ 排除 | mGBA stub 不支持 BIOS 地址 |
| GDB stub 宽范围 VRAM watchpoint | ❌ 实际不可行 | stub 强制 1 字节，无法覆盖 2304 字节卡图区 |
| EWRAM watchpoint | ⚠️ 待重试 | 地址正确性未验证，stub 同样只监 1 字节 |
| Lua memoryWrite 回调 | ❌ 排除 | mGBA Lua API 不可用 |
| mGBA CLI 调试器（--debugCli）| ❌ 无效 | 当前构建版本（0.11-dev）传入后 mGBA 立即退出，该参数可能未编译进去 |

---

## 实验四：ROM 侧静态分析 + hbreak ❌ 断点未触发

**来源**：静态分析 `asm/all.s`，找到唯一一个 `svc 0x11` 包装函数调用点

**尝试过的断点地址**：

| 断点地址 | 说明 | 结果 |
|----------|------|------|
| `0x08015076` | `FUN_08014fa8` 内，VRAM 路径调用 `FUN_0810e418` | ❌ 未触发 |
| `0x08014fa8` | `FUN_08014fa8` 函数入口 | ❌ 未触发 |
| `0x0810e418` | SWI 0x12 包装函数本体 | ❌ 未触发 |
| `0x0810e41c` | SWI 0x11 包装函数本体 | ❌ 未触发 |

**结论**：
- 按 A 打开卡牌详情页时，上述函数均未被调用
- 可能原因：
  1. 游戏使用**软件实现的 LZ77 解压**，不调用 BIOS SWI（不走 0x0810e418/0x0810e41c）
  2. `FUN_08014fa8` 不是卡图加载路径（Ghidra 分析可能误判函数边界）
  3. 卡图数据在按 A **之前**就已经加载完毕（预加载机制）
  4. all.s 的覆盖范围仅到 0x08ffffff，而卡图加载函数位于 ROM 扩展区（0x09xxxxxx）

**待排查**：
- 通过交互式 GDB 中断（Ctrl+C），在按 A 后立即查看 PC 和调用栈，确认游戏实际在哪执行
- 当前交互模式尝试未成功（write_powershell 无法发送 Ctrl+C 信号到 GDB 进程）

---

## 下一步方向

### 方案 A：ROM 离线搜索（推荐，不依赖运行时调试）

LZ77 压缩块头格式：
- 字节 0：`0x10`（LZ77 魔数）
- 字节 1–3：解压大小（24位小端）

BG2 tiles 1–36，256色，64字节/tile → 解压大小 = 36 × 64 = **2304 = 0x000900**  
搜索特征：ROM 中 4 字节对齐的 `10 00 09 00`

```python
# 伪代码
with open("2343.gba", "rb") as f:
    data = f.read()
for i in range(0, len(data)-4, 4):
    if data[i] == 0x10 and int.from_bytes(data[i+1:i+4], 'little') == 0x900:
        print(hex(i))  # 候选卡图压缩块
```

### 方案 B：GDB hbreak 全覆盖 SWI 调用点

在 ROM 二进制中搜索所有 `svc 0x11`/`svc 0x12` 字节序列，对每个地址设 hbreak，**不带存档**启动游戏，操作到卡牌列表页，按 A 触发详情页加载，断点命中时读 r0（ROM 压缩数据地址）。

- SWI 0x11 THUMB 编码：`11 DF`
- SWI 0x12 THUMB 编码：`12 DF`
- **关键**：不加载 ss1 存档，确保卡图加载发生在 GDB 监听期间内

### ⚠️ mgba-sdl -g 的新坑（2026-04-13）

当前 mGBA build-latest-win64 的 `mgba-sdl.exe` 使用 `-g` 时报 `Debugger: Couldn't open socket` 后仍能运行，但端口 2345 **不监听**。原因未明（可能是 Windows socket 权限或编译配置）。

**临时规避**：改用 `mGBA.exe`（Qt 版）+ `-g`，或查明 mgba-sdl socket 失败原因。Qt 版之前成功用过（见 `doc/dev/p0-1-gdb-dma3-watchpoint-walkthrough.md`）。

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `doc/dev/scripts/gdb_watch_dma3sad.gdb` | DMA3 源地址 watchpoint 脚本 |
| `doc/dev/scripts/gdb_watch_vram_bg2.gdb` | VRAM BG2 watchpoint 脚本（已证不可用）|
| `doc/dev/scripts/gdb_watch_ewram_02000000.gdb` | EWRAM watchpoint 脚本（已证不可用）|
| `doc/dev/mgba-gdb-stub-pitfalls.md` | mGBA GDB stub 已知坑汇总 |
| `doc/analysis/card-detail-page.md` | 卡牌详情页 VRAM 布局分析 |
