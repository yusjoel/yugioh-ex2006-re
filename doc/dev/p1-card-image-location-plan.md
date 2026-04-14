# P1：卡牌信息页面内容定位——调试方案

## 进度总览

| Phase | 状态 | 完成日期 | 产出 |
|-------|------|---------|------|
| Phase A：VRAM 布局定位 | ✅ 已完成 | 2026-04-14 | [分析报告](../analysis/p1-card-image-location/README.md) |
| Phase B2：静态分析 + 动态验证 | ✅ 已完成 | 2026-04-14 | [详细分析](p1-phase-b2-findings.md) |

---

## 概述

目标：通过 mGBA MCP（截图/内存读取）+ GDB MCP（VRAM 写监视点）联合调试，
定位**卡牌信息页面**中各类显示内容在 ROM 中的存储位置。

**页面组成**（待定位的目标）：
- 卡牌大图
- 卡牌图标（小图标，属性/种族等）
- UI 框架（边框、背景底图）
- 文本信息（卡名、攻防数值、效果描述）

**最低目标**：定位其中任意一项的 ROM 地址与数据格式。  
**最高目标**：全部内容逐一定位。

**选定方案**：
- Phase A：mGBA MCP 读取 IO 寄存器 + VRAM diff，确定各显示内容写入的 VRAM 偏移
- Phase B2：GDB 对 Phase A 确定的 VRAM 偏移下 watchpoint，追溯写入来源（ROM 地址）

---

## 前置知识

### GBA 图形渲染架构

卡牌大图、UI 底图通过 **BG 图层**（Background）渲染；图标、数字等小元素可能走 OAM：

| 区域 | VRAM 地址 | 说明 |
|------|----------|------|
| Charblock 0 | `0x06000000–0x06004000` | BG tile 数据（16KB） |
| Charblock 1 | `0x06004000–0x06008000` | BG tile 数据（16KB） |
| Charblock 2 | `0x06008000–0x0600C000` | BG tile 数据（16KB） |
| Charblock 3 | `0x0600C000–0x06010000` | BG tile 数据（16KB） |
| Sprite tiles | `0x06010000–0x06018000` | OAM 精灵 tile（32KB）|
| Tilemap | `0x06000000+screenblock×2KB` | BG 图层 tilemap |

读 IO 寄存器可确认当前 BG 配置：

| 寄存器 | 地址 | 内容 |
|--------|------|------|
| DISPCNT | `0x04000000` | 显示模式、BG 层启用状态 |
| BG0CNT | `0x04000008` | BG0 charblock、tilemap 偏移、size |
| BG1CNT | `0x0400000A` | BG1 同上 |
| BG2CNT | `0x0400000C` | BG2 同上 |
| BG3CNT | `0x0400000E` | BG3 同上 |

BGxCNT 格式（16 位）：
- bit 2-3：charblock 选择（0-3，对应 `0x06000000` 起每 16KB 一块）
- bit 8-12：tilemap 起始 screenblock 号（每 screenblock = 2KB）

### mGBA GDB Stub 关键特性

- **坑 3**：stub 为**一次性连接**，GDB 断开后 stub 永久关闭，需重启 mGBA
- **坑 8**：`watch *(uint*)addr` 实际只监 1 字节（stub 忽略 size 参数）
  → 触发率足够，但需理解此限制
- **MCP 与 GDB stub 可同时运行**（已验证）：两者通过不同端口通信，互不干扰

---

## 工具准备

整个流程使用 ss1 存档启动（已在卡组列表界面），mGBA MCP 与 GDB stub 同时工作：

```ps1
pwsh -File tools\start-mgba-gdb-ss1.ps1
pwsh -File tools\wait-mgba-ready.ps1
```

启动后：
- 通过 `mgba_live_attach(pid=<PID>)` 附加 MCP 会话
- 通过 `gdb_init` / `gdb_connect("localhost:2345")` 连接 GDB

---

## Phase A：mGBA MCP——读取 VRAM 布局　✅ 已完成

> **分析报告**：[doc/analysis/p1-card-image-location/README.md](../analysis/p1-card-image-location/README.md)

**目标**：拍摄三个状态的截图，并通过 VRAM diff 确定卡牌信息页各元素写入的 VRAM 偏移区间。

```
✅ 步骤 A1. 截图确认状态1（卡组列表）
  → mgba_live_export_screenshot

✅ 步骤 A2. 读取状态1的 VRAM + OAM 快照
  → mgba_live_read_range(start=0x06000000, length=0x18000)  ← 完整 VRAM（96KB）
  → mgba_live_dump_oam                                      ← OAM 精灵状态
  → 保存为 vram_state1

✅ 步骤 A3. 模拟按键 A → 状态2（子菜单）
  → mgba_live_input_tap(key="A", wait_frames=10)
  → mgba_live_export_screenshot  ← 确认放大镜子菜单出现

✅ 步骤 A4. 模拟按键 A → 状态3（卡牌信息页）
  → mgba_live_input_tap(key="A", wait_frames=30)
  → mgba_live_export_screenshot  ← 确认卡牌信息页面

✅ 步骤 A5. 状态3：读取 IO 寄存器
  → mgba_live_read_range(start=0x04000000, length=0x10)  ← DISPCNT + BG0-3 CNT
  结果：
    - DISPCNT = 0x1F40：mode=0，BG0+BG1+BG2+BG3+OBJ 全部启用
    - BG0CNT = 0x0086：charblock=1（tile@0x06004000），sblk=0（map@0x06000000），256色
    - BG1CNT = 0x4104：charblock=1（tile@0x06004000），sblk=1（map@0x06000800），16色
    - BG2CNT = 0x0407：charblock=1（tile@0x06004000），sblk=4（map@0x06002000），16色
    - BG3CNT = 0x0305：charblock=1（tile@0x06004000），sblk=3（map@0x06001800），16色

✅ 步骤 A6. 状态3：读取 VRAM + OAM 快照
  → mgba_live_read_range(start=0x06000000, length=0x18000)
  → mgba_live_dump_oam
  → 保存为 vram_state3

✅ 步骤 A7. 对比 vram_state1 vs vram_state3
  结果（总变化 11,746 字节，合并后 16 个区间）：
    - 0x06008040–0x0600933F  4,864B → 卡牌大图 tile 数据（Charblock 2）★ B2 首选目标
    - 0x0600004C–0x06000933  2,280B → BG0/BG1 tilemap 全量重绘
    - 0x06010005–0x060107FC  2,040B → Sprite tile（UI/图标，最大段）
    - 0x06017260+  多段各 320–927B → 其余 sprite tile（星级/数字图标等）
```

---

## Phase B2：GDB VRAM 写监视点——追溯 ROM 地址　🔲 待执行

**目标**：对 Phase A 确定的 VRAM 地址下写监视点，捕获写入时的 PC 和源地址寄存器。

```
步骤 B1. 连接 GDB（mGBA 已运行，状态1）
  → gdb_init(gdbPath="tools/arm-none-eabi-gdb.exe")
  → gdb_connect(target="localhost:2345")

步骤 B2. 设置 VRAM 写监视点
  对 Phase A 确定的某个 VRAM 偏移（优先选卡牌大图区间起始）：
  → gdb_command("watch *(unsigned char*)0x06008040")  ← Phase A 已确认的卡图 tile 起始

步骤 B3. 放行游戏执行
  → gdb_continue()

步骤 B4. 通过 mGBA MCP 触发卡牌信息页加载
  → mgba_live_input_tap(key="A", wait_frames=5)   ← 进子菜单
  → mgba_live_input_tap(key="A", wait_frames=30)  ← 进卡牌信息页

步骤 B5. watchpoint 触发后读取寄存器
  → gdb_command("-data-list-register-values x 0 1 2 3 13 14 15")
  关注：
    - pc（r15）：执行写入的指令地址（ROM 代码）
    - r0/r1/r2：可能含数据源地址
    - 若 r0/r1 在 ROM 范围（0x08000000–0x0A000000）→ 直接 ROM 地址 ✅
    - 若在 EWRAM/IWRAM → 数据经过中间缓存，需再追一层

步骤 B6. 查看写入指令上下文
  → gdb_command("-data-disassemble -a <pc> -n 20 -- 0")
  判断：memcpy 循环体？DMA 触发代码？单次写入？

步骤 B7. 若源在 EWRAM（中间缓存）
  → 对 EWRAM 源地址再设 watchpoint，向上追踪
  → 最终目标：找到 r0/r1 指向 0x09xxxxxx（ROM）的调用点

步骤 B8. 重复 B2–B7，对其他内容类型（图标、UI、文本）分别追溯
```

---

## 可能遇到的问题与预案

| 问题 | 原因 | 预案 |
|------|------|------|
| watchpoint 没触发 | 该元素在进入页面时不重新加载 | 换另一个 diff 偏移；尝试切换不同卡牌触发重绘 |
| watchpoint 触发太频繁 | UI 动画/帧循环持续写该地址 | 换 diff 区间中段；缩小到卡图 tile 区而非 tilemap 区 |
| 源地址在 IWRAM/EWRAM | 游戏先解压/处理到 RAM 再写 VRAM | 对 RAM 源地址再设 watchpoint 向上追溯 |
| 源地址在 `0x09xxxxxx` | 正常：ROM mirror（bank 2） | 减去 `0x08000000` 得文件偏移 |
| GDB stub 断开后不可重连 | 坑 3（stub 一次性） | 重启 mGBA，重新执行启动脚本 |

---

## 参考文档

| 文档 | 关联内容 |
|------|---------|
| `doc/dev/gdb-breakpoint-matrix.md` | T08：VRAM 写监视点可用；T09：VRAM 读监视点无效 |
| `doc/dev/mgba-gdb-stub-pitfalls.md` | 坑 3（stub 一次性）、坑 8（watchpoint 只监 1 字节）|
| `doc/dev/p0-3-mgba-mcp-feature-validation.md` | mGBA MCP 全部 13 个工具能力清单 |
| `doc/dev/p0-5-gdb-mcp-integration.md` | GDB MCP 工具用法及 MI 解析器已知限制 |
| `doc/dev/p0-1-gdb-dma3-watchpoint-walkthrough.md` | DMA3 watchpoint 方法参考（备选路线） |
