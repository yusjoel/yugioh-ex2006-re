# 卡图加载函数逆向调研（时间线）

本文记录卡图加载函数 `FUN_0801d290` 的逆向过程——从 VRAM diff 识别目标区间，到排除 BIOS SWI 假设，再到 watchpoint 失败教训，最终通过静态字面量池分析锁定解码器。

**最终结论已提炼到**：
- [`doc/dev/data-structure/card-image-big.md`](../dev/data-structure/card-image-big.md) — 6bpp 解码完整规范
- [`doc/dev/data-structure/card-detail-page.md`](../dev/data-structure/card-detail-page.md) — 详情页 VRAM 布局

本文保留作为**调研叙事与失败路径归档**，对日后类似任务有方法论参考价值。

---

## Phase A：VRAM 布局识别（mGBA MCP）

**日期**：2026-04-14

从 `ss1` 存档（卡组列表界面）出发，按 A → A 进入卡牌信息页面，捕获前后 VRAM 快照并对比差异。测试卡：**DESPAIR FROM THE DARK**（ATK/2800 DEF/3000）。

### IO 寄存器（状态 3 / 详情页）

```
原始: 40 1F 00 00 19 00 A0 00 86 00 04 41 07 04 05 03
```

| 寄存器 | 值 | 含义 |
|--------|-----|------|
| DISPCNT | `0x1F40` | mode=0，BG0+BG1+BG2+BG3+OBJ 全部启用 |
| BG0CNT | `0x0086` | pri=2，charblock=1（tile@`0x06004000`），sblk=0（map@`0x06000000`），256 色 |
| BG1CNT | `0x4104` | pri=0，charblock=1，sblk=1（map@`0x06000800`），16 色，size=1 |
| BG2CNT | `0x0407` | pri=3，charblock=1，sblk=4（map@`0x06002000`），16 色 |
| BG3CNT | `0x0305` | pri=1，charblock=1，sblk=3（map@`0x06001800`），16 色 |

所有 BG 层的 tile 数据基址均为 `0x06004000`（charblock=1）。tile 编号超过 charblock 1 容量时自动延伸至 charblock 2（`0x06008000`）。

### VRAM Diff 结果

**总变化**：11,746 字节，合并后 16 区间（gap 容限 64 B）。

| 排名 | VRAM 地址范围 | 大小 | VRAM 区域 | 推断内容 |
|------|--------------|------|-----------|---------|
| 1 | `0x06008040–0x0600933F` | **4,864 B** | Charblock 2 | **卡牌大图 tile 数据** |
| 2 | `0x0600004C–0x06000933` | 2,280 B | Charblock 0 / Screenblock 0–1 | BG0/BG1 tilemap 更新 |
| 3 | `0x06010005–0x060107FC` | 2,040 B | Sprite tile 区 | UI 元素 / 图标 tile |
| 4 | `0x06017260–0x060175FE` | 927 B | Sprite tile 区 | 图标或文字 sprite |
| 5 | `0x06010882–0x06010BFE` | 893 B | Sprite tile 区 | 图标 |
| 6 | `0x06010C81–0x06010FF6` | 886 B | Sprite tile 区 | 图标 |
| 7–16 | 其余 Sprite tile 区 | 116–499 B 各 | Sprite tile 区 | 各类小图标 |

### Phase A 产出

**卡牌大图 VRAM 起始**：`0x06008040`。Phase A 当时推测 4864 B ÷ 64 B/tile = **76 tiles**，后在 Phase B2 被修正为**实际 100 tiles × 8×8 = 6400 像素**（部分 tile 与状态 1 相同未被 diff 计入）。

**Phase B2 首选 watchpoint 目标**：`0x06008040`。

---

## Phase B0：BIOS SWI 假设排除（失败路径）

**日期**：2026-04-13

### 工作假设（错误）

认为卡图加载走 BIOS SWI 解压路径（LZ77=0x11 或 Huffman=0x13）：
1. 在 `asm/all.s` 中搜 `svc` 指令（注意：ARMv7 起 SWI 改名为 SVC，**grep `swi` 返回 0 条**）
2. 找到唯一 `svc 0x11` 包装函数 `FUN_0810e41c @ 0x0810e41c`（`FUN_0810e418` 对应 `svc 0x12`）
3. 追上层调用者 `FUN_08014fa8 @ 0x08014fa8`

### `FUN_08014fa8` 静态分析

函数入口保存高寄存器（Ghidra 输出 `.hword 0x46XX`，需手动解码——见末尾附录 THUMB 高寄存器 MOV 速查表）：

| 地址 | 编码 | 解码 | 含义 |
|------|------|------|------|
| 0x08014faa | `0x4657` | MOV r7, r10 | 保存 r10 |
| 0x08014fac | `0x464e` | MOV r6, r9  | 保存 r9 |
| 0x08014fae | `0x4645` | MOV r5, r8  | 保存 r8 |
| 0x08014fb4 | `0x4688` | MOV r8, r1  | **r8 = 第 2 参数（目标地址）** |

加载数据结构根指针 `DAT_08015084 = 0x09e61178`（ROM 扩展区），读取 4 个偏移：

| 栈偏移 | 内容 |
|--------|------|
| sp+0x58 | 相对指针→绝对 ROM 地址 |
| sp+0x5c | 卡图指针表基址 |
| sp+0x60 | 另一偏移表基址 |
| sp+0x64 | 卡图数据区基址 |

用卡牌 ID 索引卡图指针表：
```asm
lsls r1, r4, #0x2      @ r1 = 卡牌 ID × 4（表项字节偏移）
ldr  r3, [sp, #0x5c]   @ r3 = 指针表基址
ldr  r2, [r2, #0x0]    @ r2 = 指针表[卡牌 ID]（相对偏移）
ldr  r5, [sp, #0x64]   @ r5 = 数据区基址
adds r4, r5, r2        @ r4 = 压缩数据 ROM 地址
```

### 实验：hbreak 全部未触发

对 4 个候选地址设 hbreak，按 A 打开详情页：

| 断点地址 | 说明 | 结果 |
|----------|------|------|
| `0x08015076` | VRAM 路径 BL 指令 | ❌ 未触发 |
| `0x08014fa8` | `FUN_08014fa8` 函数入口 | ❌ 未触发 |
| `0x0810e418` | SWI 0x12 包装函数本体 | ❌ 未触发 |
| `0x0810e41c` | SWI 0x11 包装函数本体 | ❌ 未触发 |

### Phase B0 教训

**BIOS SWI 假设完全错误**。后来（Phase B2）查明：游戏使用**自写 6bpp 解码器**（`FUN_0801d290`），不调 BIOS SWI。

`FUN_08014fa8` 是另一种 LZ77 解压路径（其它资源用），不是卡图路径。

---

## Phase B1：GDB Watchpoint 失败教训

**日期**：2026-04-13

### 实验一：DMA3SAD Watchpoint ✅ 技术可行但卡图不走 DMA

监听 `0x040000D4`（DMA3SAD）：
- Watchpoint **成功触发**（I/O 地址完全支持）
- DMA3 频繁触发，来源均为 ROM `0x080f4ff0` 附近（VBlank 背景填充）
- 加条件过滤 ROM 范围后，多次按 A 键仍无新触发
- **结论**：卡牌大图加载不使用 DMA3

### 实验二：VRAM BG2 Watchpoint（当时判定）❌ 不工作

监听 `0x06000000`（BG2 tile 起始，256 色），按 A 键后**从未触发**。

### 实验三：EWRAM Watchpoint（当时判定）❌ 不工作

监听 `0x02000000`，按 A 键后**从未触发**。

### 源码分析（2026-04-13）：原结论是误判

阅读 `src/arm/debugger/memory-debugger.c`：watchpoint 通过替换 CPU 的内存访问函数指针（shim）实现，**对所有地址均有效**，无区域白名单/黑名单。

```c
debugger->cpu->memory.store32 = DebuggerShim_store32;
// ...
```

每次内存读写都经过 `_checkWatchpoints()`。BIOS LZ77 解压（`src/gba/bios.c` `_unLz77`）同样使用 `cpu->memory.store8/store16`，**也会触发 watchpoint**。

### 失败的真实原因（三重叠加）

**原因 1：监听地址错误（⭐ 最可能）**
- 监听了 `0x06000000`（tile 0，背景色/调色板）
- 卡图数据从 **tile 1** 开始写入：`0x06000040`
- 4864 B 区间是 `0x06000040..0x060008FF`

**原因 2：GDB stub 强制 1 字节范围**

阅读 `src/debugger/gdb-stub.c` `_setBreakpoint()`：

```c
struct mWatchpoint watchpoint = {
    .minAddress = address,
    .maxAddress = address + 1   // ← 始终只监 1 字节，忽略 GDB 协议中的 size 参数
};
```

GDB 的 `watch *(uint*)0x06000040` 命令带 size=4，但 stub **丢弃 size**，只监 1 字节。要覆盖 2304 字节的卡图区域需 2304 个 watchpoint，不现实。

**原因 3：存档预加载**
- 使用 `2343.ss1` 快照启动时，卡图可能已在快照保存前解压到 VRAM
- 进入游戏后 VRAM 内容直接恢复，按 A 只是切换显示层，不触发新的写入

### Phase B1 教训

mGBA GDB stub 的 watchpoint 功能**理论支持 VRAM/EWRAM**（原先的"区域不支持"结论是误判），但：
- 必须监听**正确的数据地址**（非全零 tile 0 区）
- 只监 1 字节，宽范围覆盖困难
- 存档预加载会掩盖实际写入时机

**替代方案**：改用 ROM 离线搜索（方案 A）或 hbreak 全覆盖 SWI 调用点（方案 B）。

---

## Phase B2：静态分析锁定 `FUN_0801d290`（成功）

**日期**：2026-04-14

### 路径：从 VRAM 布局反推调用函数

从 Phase A 已知：
- 卡图写入 VRAM `0x06008040`（BG0 charblock=1 + tile 编号 ≥256 延伸到 charblock 2）
- 实际解码后的 VRAM 基址是 `0x06004000 + 64 = 0x06004040`（tile 1）

### 调用链静态追踪

从 `FUN_0801d45c`（BG0 初始化，写 `BG0CNT=0x0086`）出发，查全 ROM 中**唯一**调用方 `FUN_0801e440`：

```
FUN_0801e440（卡图页顶层入口）
  ↓
FUN_0801d45c（页面初始化：清空 BG0 VRAM，写 BG0CNT=0x0086）
  ↓
FUN_0801d998（卡图加载主函数）
  ├─ 从 0x098169B8 表读取卡片属性
  ├─ 调用 FUN_080ee010（写 BG palette）
  ├─ 传第5参数 r1=0x10（VRAM 偏移量）压栈
  └─ bl FUN_0801d290（唯一调用点 @ 0x0801DA08）
```

**关键约束**：
- `FUN_0801d290` 在全 ROM 中**只有一个调用点**
- `FUN_0801d998` 在全 ROM 中**只有一个调用点**
- 其他分支函数（`FUN_0801dbdc / FUN_0801e000 / FUN_0801e100`）均不含 tile 数据基址范围的字面量

### `FUN_0801d290` 字面量池

| 符号 | 值 | 含义 |
|------|-----|------|
| DAT_0801d420 | `0x095B5C00` | card image index 表基址 |
| DAT_0801d424 | `0x080000AE` | ROM 头部版本字节地址 |
| DAT_0801d428 | `0x02000000` | EWRAM 基址 |
| DAT_0801d42c | `0x00006C2C` | EWRAM 偏移（卡片 flag 字节） |
| **DAT_0801d430** | **`0x084C76C0`** | **BG 调色板 ROM 基址** |
| **DAT_0801d434** | **`0x08510640`** | **tile 数据 ROM 基址** |
| **DAT_0801d438** | **`0x06004000`** | **VRAM 目标地址** |
| DAT_0801d43c | `0x0000031F` | = 799（第一循环限值，循环 800 次）|
| DAT_0801d440 | `0x00003F3F` | 第二循环掩码 |
| DAT_0801d444 | `0x00000C7F` | = 3199（第二循环限值，循环 3200 次）|

### card_id 查表流程

```
卡片结构地址：0x0201AFB0
word0 = [0x0201AFB0] = 0x000A2958

card_id 提取公式（FUN_0801e440 @ 0x0801E44A-E44E）：
  lsls r0, r0, #0xf   → r0 <<= 15
  lsrs r0, r0, #0x12  → r0 >>= 18
  等价于：(word0 << 15) >> 18 = (word0 >> 3) & 0x1FFF

card_id = 1323

flag 判断（@ 0x0801D306）：
  ROM[0x080000AF] 高 8 位 ≠ 0x4A（非日版）
  → flag = 1

index 计算：
  byte_offset = (card_id × 2 + flag) × 2 = (1323 × 2 + 1) × 2 = 5294 = 0x14AE
  lookup_addr = 0x095B5C00 + 0x14AE = 0x095B70AE
  tile_block = [0x095B70AE] = 1476
```

### tile 数据源地址计算

```
tile_block × stride 计算（@ 0x0801D352-D366）：
  r2 = tile_block = 1476
  r1 = r2 × 4 + r2 = r2 × 5
  r0 = r1 × 16 - r1 = r2 × 5 × 15 = r2 × 75
  r0 = r0 × 64 = r2 × 75 × 64 = r2 × 4800
  src = DAT_d434 + r2 × 4800
      = 0x08510640 + 1476 × 4800
      = 0x08BD2140  ✅
```

验证：`xxd -s 0x15B70AE -l 2 roms/2343.gba` 返回 `c4 05` = 1476 ✅

### 6bpp 解码算法（已提炼到 `card-image-big.md`）

第一循环 800 次，每次处理 6 ROM bytes → 8 VRAM bytes：

```
p0 =  W0 & 0x3F
p1 = (W0 >> 6) & 0x3F
p2 = ((W0 >> 12) & 0xF) | ((W1 & 0x3) << 4)
p3 = (W1 >> 2) & 0x3F
p4 = (W1 >> 8) & 0x3F
p5 = ((W1 >> 14) & 0x3) | ((W2 & 0xF) << 2)
p6 = (W2 >> 4) & 0x3F
p7 = (W2 >> 10) & 0x3F
```

第二循环 3200 次，对已写 VRAM 应用 `VRAM_final = raw & 0x3F + pal_offset`（pal_offset=0x10，即拷到 palette[0x10..0x4F]）。

### Phase B2 误判记录

#### card_id = 107（早期错误）
误将 EWRAM 偏移表中的中间值读为 card_id，导致 tile_block = 114，src = `0x08595FC0`（错误）。耗费大量时间追查"真实基址 `0x08B4C7C0`"（幻象，由 `0x08BD2140 - 114×4800` 反推得出）。

#### 指针表 `0x081C0Dxx`
调查 `asm/all.s` 行 374221 附近的 `.word 0x08b41fa8` 等条目，后确认这些是**动画帧/精灵定义的数据表**（ROM 数据区 `0x081BDxxx–0x081C0xxx`），不是代码字面量，与 tile 加载无关。

#### `FUN_080ee7ac`
该函数根据 card type 字段返回不同格式的卡图数据指针（普通/特殊格式路由器），最终仍由 `FUN_0801d290` 统一处理，本身不写 tile 数据。

#### 搜索第二个 6bpp 解压函数
在全 `asm/all.s` 中搜 `0x3f3f` 掩码 / `bl FUN_0801d290` / `bl FUN_0801d998`：
- `0x3f3f` 掩码：仅 `FUN_0801d290` 使用
- `bl FUN_0801d290`：仅一处调用
- `bl FUN_0801d998`：仅一处调用

**不存在第二个加载函数**。

### 调色板策略修正（批量导出时发现）

findings §3.1 原本将 `DAT_0801d430 = 0x084C76C0` 标注为"256 色 BG 共享调色板"。试用 512 字节共享后 DESPAIR 呈现错误的蓝灰色调。分析前 512 字节发现约半数 BGR555 项带 bit15=1，不符合 GBA 惯例。改按 `base + tile_block × 128` 当 64 色/卡读取：

- DESPAIR 立即呈现正确的暗红紫配色
- card_0010=红龙、card_0500=蓝色昆虫、card_3098=蓝龙等颜色均合理
- 确认：**每卡独立 64 色调色板，stride 128 B**

---

## Phase B3：GDB hbreak 补充验证（2026-04-16）

在卡图导出完成后，验证"**从已知函数地址出发**，GDB 硬件断点完全可以断到有用的代码"。之前失败的原因是断错了函数（BIOS SWI 路径 vs 实际 6bpp 解码路径）。

### 实验方法

- mGBA MCP `mgba_live_start` + GDB MCP 双 MCP 并用
- GDB batch 脚本（`--batch -x script.gdb`）绕过 GDB MCP 的异步通知限制
- mGBA MCP `input_set` 注入按键触发卡牌详情页转场

### 调用链验证

```
card_info_page_entry (0x0801E440)      ← 按 A 触发
  ├── bl card_info_page_init_bg0 (0x0801D45C)   [HIT 1]
  └── bl card_image_decode_wrapper (0x0801D998)  [HIT 2]
         └── bl decode_card_image_6bpp (0x0801D290)  [HIT 3]
```

LR 寄存器验证：
- HIT 1 的 LR = `0x0801E447`（`card_info_page_entry + 0x07`）✅
- HIT 2 的 LR = `0x0801E457`（`card_info_page_entry + 0x17`）✅
- HIT 3 的 LR = `0x0801DA0D`（`card_image_decode_wrapper + 0x75`）✅

### 参数签名新发现（HIT 3）

```
PC = 0x0801D290
r0 = 0x06000000  （VRAM 目标基址，注意**不是** 0x06004000）
r1 = 0x0082 = 130（调色板偏移）
r2 = 0x052B = 1323（card_id）
r3 = 0x0002（flag，含义待确认）
```

**r1 = 0x82 的发现**：
- 之前 `p1-phase-b2-findings.md` 记录 r1=0x10（从 pal[16:80]）
- 本次实测 r1=0x82=130（从 pal[130:193]）
- 意味着 BG palette 前 128 色留给 UI/BG1-3，卡图使用 pal[130:193]（64 色）
- 两个值可能是不同调用路径（详情页 vs 其他）

**r3 = 2 的含义**：
- 之前文档 `flag=0` OCG, `flag=1` TCG
- 实测 `flag=2`，可能是第三种变体或编码方式不同
- 需在不同卡上断点对比验证

### VRAM Watchpoint 追加实验

追加验证：**纯 watchpoint 路径**是否能在不知道函数地址的前提下定位解码器。

设 watchpoint `0x06004040` + hbreak `0x0801D290` 对照：

| 命中 | 类型 | PC | 函数 | 说明 |
|-----|------|-----|------|------|
| HIT 1 | **watchpoint** | `0x080F4E86` | memset/memclear | VRAM 清零（Old=16→New=0），LR=`0x0801D47D`（init_bg0）|
| HIT 2 | **hbreak** | `0x0801D290` | decode_card_image_6bpp | 紧接清零之后 |

**分析**：第一个 watchpoint 命中不是解码器，而是 **VRAM 清零函数**（`FUN_080F4E74`）。清零函数的 **LR=`0x0801D47D`** 指向 `card_info_page_init_bg0`，向上追溯 1-2 步即可到达 `card_info_page_entry` 和 `decode_card_image_6bpp`。

**纯 watchpoint 路径（仅 watchpoint，无 hbreak）**：

```
watch *(unsigned char*)0x06004040

HIT 1 (continue ①):
  PC = 0x080F4E86 (memclear), LR = 0x0801D47D (init_bg0)
  Old=16 → New=0 (清零)

HIT 2 (continue ②):
  PC = 0x0801D406 (decode_card_image_6bpp 内部, 第二循环 palette offset 调整)
  Old=0 → New=16 (解码后像素索引)
  r4 = 0x06004042 (VRAM 写指针, 刚写完 0x06004040)
  LR = 0x0801D331 (函数体内跳转点)
```

**2 次 continue 即可直接命中解码器内部**。从 PC=`0x0801D406` 向上找 `push {r4,r5,r6,r7,lr}` 即可定位函数入口 `0x0801D290`。

之前 Phase B1 未能断到写入，是因为 hbreak 在解码器**入口**就拦截了——解码器尚未执行到 VRAM 写指令。去掉 hbreak 后，watchpoint 自然在第二次 continue 时命中解码器的 `strh`。

### 操作要点（ss1 存档）

- ss1 存档在**卡组编辑列表页**
- **需要按两次 A**：第一次 A 选中卡牌，第二次 A 打开详情页
- `input_set(["A"])` → `sleep 2` → `input_clear` → `sleep 2` → 再次 `input_set(["A"])`

---

## 方法论修正

### 首选路径

**静态分析**（VRAM diff → IO 指纹 → 全 ROM 搜索 → 字面量池）效率最高，一步到位。

### 三种场景各有最佳工具

| 场景 | 推荐方法 |
|------|---------|
| 从零定位未知资产的加载函数 | **静态分析** + 字面量池（本次 B2 路径） |
| 同上，备选路径 | **VRAM watchpoint**（watch 写入地址 → 2 次 continue → 直接命中解码器内部） |
| 已知函数地址，验证参数/调用链 | **GDB hbreak**（batch 脚本，一次性捕获全部寄存器） |

### GDB batch 最佳实践

```
1. mgba_live_start (rom + savestate, gdb_stub=true) → 游戏暂停
2. GDB --batch -x script.gdb（后台运行）：
   - target remote localhost:2345
   - hbreak *<addr1> / hbreak *<addr2> / ...
   - continue（阻塞等待）
3. mGBA MCP input_set 触发转场
4. 断点命中 → info registers / x/Ni $pc / x/Nx <addr> → kill + quit
5. 读 GDB 输出文件提取数据
```

**注意**：GDB batch 的 `kill` 会消耗 stub（mGBA 不再接受 GDB 连接），需要 `mgba_live_stop` + 重新 `mgba_live_start` 才能开始下一轮调试。

---

## 附录 A：Phase A VRAM diff 原始数据

### OAM 对比

**状态 1（卡组列表）**：
```
精灵 0-6：  attr0=0x4074(y=116), attr1=0x00D0/0x0070..., attr2=0xA43D  — 横排排列
精灵 7-8：  attr0=0x805C, attr2=0xA39C/E                               — 纵向边框
精灵 9-21： attr0=0x405C(y=92),  attr2=0xA39D                          — ATK/DEF 装饰
精灵 28-35：attr0=0x0089 系列,   attr2=0x9BE0 系列                      — 数字精灵
精灵 38-39：attr0=0x2030/0x8057                                         — 光标/特效
```

**状态 3（卡牌信息页）**：
```
精灵 0：    attr0=0x0006(y=6),   attr1=0x4056, attr2=0xD3A2            — 卡片框上角装饰
精灵 1-8：  attr0=0x0016(y=22),  attr1=0x005C..0x0024（X 依次减小）     — 星级图标（8 颗）
精灵 9-10： attr0=0x2000/0x2000, attr1=0x40F0/0x4100, attr2=0x03AC/B4  — ATK/DEF 标签
精灵 12-27：attr0=0x4010 系列,   attr1=0x40F0 系列, attr2=0xF802 系列   — ATK/DEF 数字（4×4 组）
```

### Phase A 截图

- `doc/analysis/p1-card-image-location/screenshots/state1-deck-list.png`
- `doc/analysis/p1-card-image-location/screenshots/state2-submenu.png`
- `doc/analysis/p1-card-image-location/screenshots/state3-card-info.png`

---

## 附录 B：THUMB 高寄存器 MOV 速查

Ghidra 有时将 THUMB 高寄存器 MOV 输出为 `.hword 0xXXXX`，解码方法：

```
格式: 0100 0110 D Rm Rdn  (16 位 little-endian)
      ^^^^ ^^^^           固定前缀 0x46xx

D   = bit 7 of byte 1
Rm  = bits [6:3] of byte 1
Rdn = bits [2:0] of byte 1
目标寄存器 = D*8 + Rdn
```

常见示例：

| 编码 | 二进制 | 解码 |
|------|--------|------|
| `0x4688` | `0100 0110 1000 1000` | MOV r8, r1  (D=1, Rm=r1, Rdn=r0+8=r8) |
| `0x4641` | `0100 0110 0100 0001` | MOV r1, r8  (D=0, Rm=r8, Rdn=r1) |
| `0x4657` | `0100 0110 0101 0111` | MOV r7, r10 (D=0, Rm=r10, Rdn=r7) |

---

## 相关文件

| 文件 | 内容 |
|------|------|
| [`doc/dev/data-structure/card-image-big.md`](../dev/data-structure/card-image-big.md) | 6bpp 解码规范 + ROM 地址 + 索引公式（最终结论） |
| [`doc/dev/data-structure/card-detail-page.md`](../dev/data-structure/card-detail-page.md) | 详情页 UI VRAM 布局 |
| [`doc/dev/locate-rom-asset-from-vram-diff.md`](../dev/locate-rom-asset-from-vram-diff.md) | 从 VRAM 差分到 ROM 资源定位的方法论（本文是其实战案例） |
| [`doc/dev/tools/gdb-debugging.md`](../dev/tools/gdb-debugging.md) | GDB stub + GDB MCP 调试指南 |
| `asm/all.s` 行 15429 | `FUN_0801d290` 完整反汇编 |
| `asm/all.s` 行 16336 | `FUN_0801d998` |
| `asm/all.s` 行 17711 | `FUN_0801e440` |
| `tools/ad-hoc/decode_card_6bpp.py` | 6bpp 解码验证脚本（单卡） |
| `tools/rom-export/export_card_images.py` | 批量导出脚本（2331 张 PNG） |
| `doc/dev/scripts/gdb_card_bp_full.gdb` | GDB batch 脚本（Phase B3 实验） |
