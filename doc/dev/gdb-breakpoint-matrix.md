# P0-4：GDB 断点类型矩阵验证报告

> 目标：系统验证 mGBA GDB stub（端口 2345）支持哪些断点/监视点类型，以及在各 GBA 内存区域的可用性，为后续 P1 卡图定位调试提供参考。

---

## 测试环境

| 项目 | 值 |
|------|----|
| GDB 版本 | `arm-none-eabi-gdb` 10.2（`tools/arm-none-eabi-gdb.exe`）|
| mGBA GDB stub | 端口 2345，`-g 2345` 启动 |
| 存档状态 | ss1（卡组编辑界面，静态画面）|
| 脚本 | `doc/dev/scripts/gdb_matrix_probe.gdb` |

---

## 内存区域（来自 `info mem`）

| # | 地址范围 | Stub 标注 | 实际属性 |
|---|----------|-----------|----------|
| 0 | `0x00000000–0x00004000` | ro | BIOS（只读）|
| 1 | `0x02000000–0x02040000` | rw | EWRAM（外部工作 RAM）|
| 2 | `0x03000000–0x03008000` | rw | IWRAM（内部工作 RAM）|
| 3 | `0x04000000–0x04000400` | rw | IO 寄存器 |
| 4 | `0x05000000–0x05000400` | rw | 调色板 RAM |
| 5 | `0x06000000–0x06018000` | rw | VRAM |
| 6 | `0x07000000–0x07000400` | rw | OAM |
| 7 | `0x08000000–0x0A000000` | rw | ROM（物理只读，stub 误标 rw）|
| 8 | `0x0A000000–0x0C000000` | rw | ROM bank2 |

> **注意**：`monitor help` 返回 `"Target does not support this command"`，stub 不支持 monitor 命令。

---

## 断点类型矩阵

### 图例

| 符号 | 含义 |
|------|------|
| ✅ | 设置成功 + 触发成功 |
| ✅* | 设置成功 + 触发（需特定游戏状态）|
| 🔵 | 设置成功，未触发（游戏状态下无读写活动）|
| 🔵† | 设置成功，skip continue（预计立即触发导致 packet storm）|
| ❌ | stub 报错，不支持 |
| — | 无意义（如 ROM 写监视点）|

### 结果矩阵

| 断点类型 | ROM | EWRAM | IWRAM（代码） | IWRAM（数据） | VRAM | IO |
|----------|-----|-------|--------------|--------------|------|----|
| `break`（软件断点）| ✅ T01 | — | ✅ T03 | — | — | — |
| `hbreak`（硬件断点）| ✅ T02 | — | ✅ T04 | — | — | — |
| `watch`（写监视点）| — | 🔵 T11 | — | 🔵 | ✅* P0-1 | ✅ T05 |
| `rwatch`（读监视点）| 🔵† T13 | 🔵 T10 | — | 🔵 T12 | 🔵 T09 | ✅ T06 |
| `awatch`（读写监视点）| — | — | — | — | — | ❌ T07 |

---

## 各测试详细结果

### T01 — `break` on ROM `0x080F4EB6` ✅

```
Breakpoint 1 at 0x80f4eb6
Breakpoint 1, 0x080f4eb6 in ?? ()
pc = 0x80f4eb6   lr = 0x80f5f49
```

**结论**：软件断点在 ROM 上**可以设置并触发**。  
**说明**：GBA ROM 物理只读，理论上软件断点（BKPT 指令写入）不可行。mGBA stub 在模拟层面拦截执行，无需真正修改 ROM 字节，因此有效。**真实硬件上不可用**。

---

### T02 — `hbreak` on ROM `0x080F4EB6` ✅

```
Hardware assisted breakpoint 2 at 0x80f4eb6
Breakpoint 2, 0x080f4eb6 in ?? ()
pc = 0x80f4eb6   lr = 0x80f5f49
```

**结论**：硬件断点在 ROM 有效，推荐用于 ROM 代码断点（真实硬件也可用）。

---

### T03 — `break` on IWRAM `0x03004DB4` ✅

```
Breakpoint 3 at 0x3004db4
Breakpoint 3, 0x03004db4 in ?? ()
pc = 0x3004db4   lr = 0x3000144
```

**结论**：IWRAM 可写，软件断点正常工作。触发后 lr = `0x3000144`（调用者地址）。

---

### T04 — `hbreak` on IWRAM `0x03004DB4` ✅

```
Hardware assisted breakpoint 4 at 0x3004db4
Breakpoint 4, 0x03004db4 in ?? ()
pc = 0x3004db4   lr = 0x3000144
```

**结论**：硬件断点在 IWRAM 同样有效。

---

### T05 — `watch` on IO `0x040000D0`（DMA3SAD）✅

```
Hardware watchpoint 5: *(unsigned int*)0x040000D0
Old value = 2218786816   (0x84400000)
New value = 3057647616   (0xB6400000)
pc = 0x3004ddc
```

**结论**：IO 写监视点立即触发（音频 DMA 持续更新 DMA3SAD）。与 P0-1 一致。

---

### T06 — `rwatch` on IO `0x040000D0`（DMA3SAD）✅

```
Hardware read watchpoint 6: *(unsigned int*)0x040000D0
Value = <unreadable>
pc = 0x3004db4
```

**结论**：IO 读监视点可用。`Value = <unreadable>` 是 GDB 在无符号表时的正常显示，不影响触发。

---

### T07 — `awatch` on IO `0x040000D0` ❌

```
Hardware access (read/write) watchpoint 7: *(unsigned int*)0x040000D0
Error: Reply contains invalid hex digit 79
```

**结论**：mGBA GDB stub **不支持 `awatch`**。`0x79` = ASCII `'y'`，stub 返回了人类可读字符串（如 `"yes"` 或 `"type not supported"`），GDB 解析时报错。

---

### T08 — `watch` on VRAM `0x06000000` 🔵（游戏状态依赖）

未触发。deck editor 静态界面不写 BG tile data。

**参考 P0-1**：`watch *(unsigned int*)0x06000040` 在 nosave 模式（游戏主循环加载卡图时）可触发，PC = `0x80f4eb6`。

**结论**：VRAM 写监视点**可用**，但需要正确游戏状态（画面渲染/卡图加载中）。

---

### T09 — `rwatch` on VRAM `0x06000000` 🔵（PPU 读不计入）

未触发（等待超过 3 分钟）。

**结论**：VRAM 的"读取"主要由 PPU（图形处理单元）执行，**不经过 ARM CPU 内存总线**，GDB watchpoint 无法捕获。仅当 CPU 代码显式读取 VRAM（如 `ldr` 指令读 `0x06xxxxxx`）时才触发，正常渲染流程下不触发。

---

### T10 — `rwatch` on EWRAM `0x02000000` 🔵（游戏状态依赖）

未触发（等待超过 3 分钟）。

**EWRAM 内容**（预调研扫描）：`0x02000000` 为存档头 `YWCT2006`，游戏在 deck editor 中不频繁读取。

**结论**：EWRAM 读监视点**可以设置**，需要游戏主动读取该地址时才触发（如进入存档读取流程）。

---

### T11 — `watch` on EWRAM `0x02000000`（set only）🔵

```
Hardware watchpoint 1: *(unsigned int*)0x02000000
T11 SET OK
```

**结论**：EWRAM 写监视点可以设置。仅在游戏执行存档写入时触发，deck editor 不触发。

---

### T12 — `rwatch` on IWRAM `0x03000808` 🔵（地址选取问题）

未触发（等待超过 2 分钟）。

地址 `0x03000808` 预调研显示为 ROM 函数指针（`0x8050607C`），游戏在 deck editor 中不经此地址。

**结论**：需选择游戏主循环实际读取的 IWRAM 数据地址。`rwatch` 机制本身可用（参见 T06 IO 验证）。

---

### T13 — `rwatch` on ROM `0x08000000`（set only）🔵†

```
Hardware read watchpoint 1: *(unsigned int*)0x08000000
T13 SET OK
```

**结论**：ROM 读监视点**可以设置**，但**不能 continue**——CPU 每次取指（instruction fetch）都从 ROM 读取，watchpoint 会在每个指令周期触发，形成与 P0-1 条件监视点相同的 `Ignoring packet error` 风暴。

---

## 汇总与关键结论

### 支持情况总结

| 断点类型 | 支持情况 | 备注 |
|----------|----------|------|
| `break` | ✅ ROM + IWRAM | mGBA 模拟层实现，真实硬件 ROM 不可用 |
| `hbreak` | ✅ ROM + IWRAM | 推荐用于 ROM 代码断点 |
| `watch`（写）| ✅ IO + VRAM；🔵 EWRAM（可设置）| VRAM 需加载状态，EWRAM 需存档状态 |
| `rwatch`（读）| ✅ IO；🔵 EWRAM/IWRAM（可设置，需正确地址）；🔵† ROM（不能 continue）；🔵 VRAM（PPU 读不计）| |
| `awatch`（读写）| ❌ stub 报错 | 全区域不可用 |

### 给 P1 阶段的建议

| 调试目标 | 推荐断点类型 |
|----------|------------|
| ROM 函数入口（如 memcpy）| `hbreak *0x080F4EB6` |
| IWRAM 游戏主循环 | `break *0x03004DB4` 或 `hbreak` |
| 监听 VRAM 卡图写入 | `watch *(unsigned int*)0x06000040`（需 nosave 触发卡图加载）|
| 监听 DMA 写入源地址 | `watch *(unsigned int*)0x040000D0`（DMA3SAD）|
| 监听 IO 读取 | `rwatch *(unsigned int*)0x040000D0` |
| EWRAM 存档写入 | `watch *(unsigned int*)0x02000000`（需进入存档流程）|

---

## 遇到的坑

### 坑 1：VRAM watch 在静态画面不触发

- **现象**：`watch *(unsigned int*)0x06000040` 在 deck editor 中挂起超过 4 分钟
- **根因**：卡图 `0x06000040` 只在卡图加载时写入；deck editor 静态画面不触发
- **解法**：使用 nosave 模式（游戏从头运行，主菜单渲染卡图时触发），或改用 `0x06000000`（BG tile data，但 deck editor 仍不触发）
- **结论**：VRAM 写监视点需要"正确的游戏状态"，P0-1 nosave 模式已确认可用

### 坑 2：`awatch` 导致 stub 错误退出

- **现象**：`awatch *(unsigned int*)0x040000D0` → `Reply contains invalid hex digit 79`，整个 GDB session 退出
- **根因**：stub 返回非 RSP 格式的响应（可能是字符串 `"not supported"` 之类），GDB 解析失败
- **影响**：脚本在 T07 处中断，后续测试需要重启 mGBA 续跑
- **结论**：`awatch` 全区域不可用，GDB 脚本中不要使用

### 坑 3：ROM rwatch 会触发 packet error 风暴

- **现象**：预期 rwatch on ROM 会在每次取指时触发
- **根因**：GBA CPU 从 ROM 执行时，每条指令都是一次 ROM 读取；watchpoint 每帧触发数万次，mGBA stub RSP 响应跟不上，形成 `Ignoring packet error` 连锁
- **结论**：ROM rwatch 仅可 set-only 验证，不能 continue

### 坑 4：EWRAM/IWRAM rwatch 需要匹配游戏状态

- **现象**：`rwatch *(unsigned int*)0x02000000` 和 `rwatch *(unsigned int*)0x03000808` 均未触发
- **根因**：选取的地址（存档头、函数指针表）在 deck editor 状态下不被 CPU 读取
- **结论**：rwatch 机制本身可用（IO 验证），需选择游戏循环实际访问的地址

---

## 相关文档

- [P0-1 GDB DMA3 Watchpoint 走查文档](p0-1-gdb-dma3-watchpoint-walkthrough.md)
- [mGBA GDB Stub 已知问题](mgba-gdb-stub-pitfalls.md)
- GDB 脚本：`doc/dev/scripts/gdb_matrix_probe.gdb`
