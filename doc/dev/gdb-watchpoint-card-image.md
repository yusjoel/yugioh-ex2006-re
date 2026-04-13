# GDB Watchpoint 实验记录：卡图 ROM 数据定位

**日期**: 2026-04-13  
**目标**: 确定卡牌大图在 ROM 中的存储位置（压缩块地址）  
**工具**: GDB 10.2（tools/arm-none-eabi-gdb.exe）+ mGBA GDB stub（端口 2345）

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

## mGBA GDB Stub Watchpoint 支持范围（总结）

| 地址范围 | 区域 | Watchpoint 支持 |
|----------|------|----------------|
| 0x04xxxxxx | I/O 寄存器 | ✅ 支持 |
| 0x08xxxxxx | ROM | ✅ 支持（hbreak 测试过） |
| 0x06xxxxxx | VRAM | ❌ 不支持 |
| 0x02xxxxxx | EWRAM | ❌ 不支持（疑似） |
| 0x03xxxxxx | IWRAM | 未测试 |
| 0x00000008 | BIOS SWI 向量 | ❌ 不支持（hbreak 不工作） |

---

## 已排除的方案

| 方案 | 状态 | 原因 |
|------|------|------|
| DMA3 watchpoint | ❌ 排除 | 卡图不走 DMA3 |
| BIOS SWI 向量断点（0x8）| ❌ 排除 | mGBA stub 不支持 BIOS 地址 |
| VRAM watchpoint | ❌ 排除 | mGBA stub 不支持 |
| EWRAM watchpoint | ❌ 排除 | mGBA stub 不支持 |
| Lua memoryWrite 回调 | ❌ 排除 | mGBA Lua API 不可用 |

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

### 方案 A：ROM 离线搜索（推荐）

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

### 方案 B：ROM 中搜索 SWI 调用点

在 ROM 中找到调用 SWI 且 r1=0x06000000 的代码段，对这些 ROM 地址设 hbreak，按 A 触发后读 r0（ROM 压缩数据地址）。

SWI 0x11 THUMB 编码：`11 DF`（字节序列）

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `doc/dev/scripts/gdb_watch_dma3sad.gdb` | DMA3 源地址 watchpoint 脚本 |
| `doc/dev/scripts/gdb_watch_vram_bg2.gdb` | VRAM BG2 watchpoint 脚本（已证不可用）|
| `doc/dev/scripts/gdb_watch_ewram_02000000.gdb` | EWRAM watchpoint 脚本（已证不可用）|
| `doc/dev/mgba-gdb-stub-pitfalls.md` | mGBA GDB stub 已知坑汇总 |
| `doc/analysis/card-detail-page.md` | 卡牌详情页 VRAM 布局分析 |
