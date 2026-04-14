# Phase B2 分析报告：卡牌大图 ROM 数据定位

**完成日期**：2026-04-14  
**分析对象**：DESPAIR FROM THE DARK（ATK 2800 / DEF 3000）  
**工具**：mGBA MCP（Lua 脚本读取内存）+ `asm/all.s`（Ghidra 导出静态反汇编）

---

## 结论（速查）

| 项目 | 值 |
|------|-----|
| **大卡图 ROM 地址** | **0x08BD2140** |
| **数据格式** | 6bpp 压缩（每 6 ROM bytes → 8 像素） |
| **tile 数据基址** | 0x08510640 |
| **card_id**（游戏内部） | 1323 |
| **tile_block 索引** | 1476 |
| **验证公式** | `0x08510640 + 1476 × 4800 = 0x08BD2140` ✅ |
| **加载函数** | `FUN_0801d290`（`asm/all.s` 行 15429） |
| **调用链** | FUN_0801e440 → FUN_0801d998 → FUN_0801d290 |
| **VRAM 目标** | 0x06004000（BG0 char base block 1） |

---

## 一、VRAM 布局确认（动态读取）

### 1.1 IO 寄存器（卡图详情页）

| 寄存器 | 值 | 含义 |
|--------|-----|------|
| DISPCNT | 0x1F40 | Mode 0，BG0/1/2/3 + OBJ 全开 |
| BG0CNT | 0x0086 | char base 1（tile 数据起于 0x06004000），256色（8bpp），screenblock 0（tilemap @0x06000000） |

### 1.2 BG0 tilemap 扫描结果

扫描 0x06000000 起的 32×32 tilemap，定位大卡图占用区域：

- **行 4–11，列 2–11**（共 80 个 tile entry）
- Tile 编号：1–80（相对 char base 起始编号）
- Tile 1 VRAM 地址：`0x06004040`（= 0x06004000 + 1×64 bytes）

---

## 二、调用链静态分析

```
FUN_0801e440（卡图页顶层入口）
  ↓
FUN_0801d45c（页面初始化：清空 BG0 VRAM，写 BG0CNT=0x0086）
  ↓
FUN_0801d998（卡图加载主函数）
  ├─ 从 0x098169B8 表读取卡片属性（ATK/DEF/type 等）
  ├─ 调用 FUN_080ee010（写 BG palette 等）
  ├─ 传第5参数 r1=0x10（VRAM 偏移量）压栈
  └─ bl FUN_0801d290（唯一调用点 @ 0x0801DA08）
  ↓
FUN_0801dbdc（动画控制器，不写 tile 数据）
FUN_0801e000（UI 元素渲染，无 tile 数据）
FUN_0801e100（UI 元素渲染，无 tile 数据）
```

**关键约束**：
- `FUN_0801d290` 在全 ROM 中**只有一个调用点**（行 16391）
- `FUN_0801d998` 在全 ROM 中**只有一个调用点**（FUN_0801e440 内）
- FUN_0801dbdc / FUN_0801e000 / FUN_0801e100 均不含 tile 数据基址范围的字面量

---

## 三、FUN_0801d290 详细分析

**入口地址**：0x0801D290  
**asm/all.s 行**：15429

### 3.1 字面量池（关键数据地址）

| 符号 | ROM 地址 | 值 | 含义 |
|------|----------|-----|------|
| DAT_0801d420 | 0x0801D420 | 0x095B5C00 | card image index 表基址 |
| DAT_0801d424 | 0x0801D424 | 0x080000AE | ROM 头部版本字节地址 |
| DAT_0801d428 | 0x0801D428 | 0x02000000 | EWRAM 基址 |
| DAT_0801d42c | 0x0801D42C | 0x00006C2C | EWRAM 偏移（卡片 flag 字节） |
| **DAT_0801d430** | 0x0801D430 | **0x084C76C0** | BG 调色板 ROM 基址 |
| **DAT_0801d434** | 0x0801D434 | **0x08510640** | **tile 数据 ROM 基址** |
| **DAT_0801d438** | 0x0801D438 | **0x06004000** | **VRAM 目标地址** |
| DAT_0801d43c | 0x0801D43C | 0x0000031F | = 799（第一循环限值，循环 800 次） |
| DAT_0801d440 | 0x0801D440 | 0x00003F3F | 第二循环掩码 |
| DAT_0801d444 | 0x0801D444 | 0x00000C7F | = 3199（第二循环限值，循环 3200 次） |

### 3.2 card_id 查表流程

```
卡片结构地址：0x0201AFB0
word0 = [0x0201AFB0] = 0x000A2958

card_id 提取公式（FUN_0801e440 @ 0x0801E44A-E44E）：
  lsls r0, r0, #0xf   → r0 = 0x000A2958 << 15（32位）
  lsrs r0, r0, #0x12  → r0 >>= 18
  等价于：(word0 << 15) >> 18 = word0 >> 3 & 0x1FFF

card_id = 1323

flag 判断（@ 0x0801D306）：
  ROM[0x080000AF] 高 8 位 ≠ 0x4A（当前版本为日版）
  → flag = 1

index 计算：
  r2 = card_id × 2 = 2646
  r2 |= flag = 2647
  byte_offset = 2647 × 2 = 5294 = 0x14AE
  lookup_addr = 0x095B5C00 + 0x14AE = 0x095B70AE
  tile_block = [0x095B70AE] = 1476
```

### 3.3 tile 数据源地址计算

```
tile_block × stride 计算（@ 0x0801D352-D366）：
  r2 = tile_block = 1476
  r1 = r2 × 4 + r2 = r2 × 5
  r0 = r1 × 16 - r1 = r2 × 5 × 15 = r2 × 75
  r0 = r0 × 64 = r2 × 75 × 64 = r2 × 4800
  src = DAT_d434 + r2 × 4800
      = 0x08510640 + 1476 × 4800
      = 0x08510640 + 0x6C1B00
      = 0x08BD2140  ✅
```

### 3.4 6bpp 解压格式（第一循环 LAB_0801d37c）

循环 800 次（r9=799，`bls` 条件），每次处理 6 ROM bytes → 8 VRAM bytes：

```
输入：W0=ROM[+0..+1]，W1=ROM[+2..+3]，W2=ROM[+4..+5]（均 LE u16）

p0 =  W0 & 0x3F
p1 = (W0 >> 6) & 0x3F
p2 = ((W0 >> 12) & 0xF) | ((W1 & 0x3) << 4)
p3 = (W1 >> 2) & 0x3F
p4 = (W1 >> 8) & 0x3F
p5 = ((W1 >> 14) & 0x3) | ((W2 & 0xF) << 2)
p6 = (W2 >> 4) & 0x3F
p7 = (W2 >> 10) & 0x3F

ROM 指针 r6 += 6（每次消耗 6 bytes）
VRAM 指针 r5 += 8（每次输出 8 bytes）
```

### 3.5 VRAM 偏移修正（第二循环 LAB_0801d3fa）

循环 3200 次，对 VRAM 已写数据应用：

```
VRAM_final = (vram_raw & 0x3F) + 5th_param
```

第 5 参数（FUN_0801d998 @ 0x0801D9FE-DA00）：`r1 = 0x10`

因此：
```
VRAM_final = raw_6bit + 0x10
```

这使得调色板索引从 0x10 开始，保留 0x00–0x0F 给透明/UI 用途。

---

## 四、调查过程中的误判记录

### 4.1 card_id = 107（错误）

**原因**：早期会话中错误地将 EWRAM 偏移表中的某个中间值误读为 card_id，导致：
- tile_block 误算为 114
- 理论 src = 0x08510640 + 114 × 4800 = **0x08595FC0**（错误）

**影响**：耗费大量时间追查"真实基址 0x08B4C7C0"（此地址为幻象，由 `0x08BD2140 - 114×4800` 反推得出）。

### 4.2 指针表 0x081C0Dxx 调查

调查 `asm/all.s` 行 374221 附近的 `.word 0x08b41fa8` 等条目：
- 这些条目位于 **ROM 数据区**（0x081BDxxx–0x081C0xxx），不是代码字面量
- 它们是动画帧/精灵定义的数据表，与 tile 加载无关

### 4.3 FUN_080ee7ac 调查

该函数根据 card type 字段返回不同格式的卡图数据指针（普通/特殊格式路由器），
最终仍由 FUN_0801d290 统一处理，本身不写 tile 数据。

### 4.4 搜索第二个 6bpp 解压函数

在全 `asm/all.s` 中搜索：
- `0x3f3f` 掩码：仅 FUN_0801d290 使用
- `bl FUN_0801d290`：仅一处调用
- `bl FUN_0801d998`：仅一处调用

确认不存在第二个加载函数。

---

## 五、相关数据地址速查

| 地址 | 内容 |
|------|------|
| **0x08BD2140** | DESPAIR FROM THE DARK 大卡图 6bpp 数据起始 |
| 0x08510640 | 大卡图 tile 数据库基址（tile_block 0 对应位置） |
| 0x095B5C00 | card image index 表（每项 u16，`card_id*2+flag` 索引） |
| 0x084C76C0 | BG 调色板 ROM 基址（卡图页，256色） |
| 0x06004000 | VRAM BG0 char base（大卡图 tile 写入目标） |
| 0x06000000 | VRAM BG0 tilemap（screenblock 0） |
| 0x0201AFB0 | 卡片对象结构体（EWRAM，含 card_id / ATK / DEF） |
| 0x098169B8 | 卡片属性表（ATK/DEF/type 等，stride=11×2 bytes） |

---

## 六、相关文件

| 文件 | 说明 |
|------|------|
| `asm/all.s` 行 15429 | FUN_0801d290 完整反汇编 |
| `asm/all.s` 行 16336 | FUN_0801d998 完整反汇编 |
| `asm/all.s` 行 17711 | FUN_0801e440 完整反汇编 |
| `doc/dev/p1-card-image-location-plan.md` | Phase 总计划 |
| `doc/dev/p1-phase-b2-preparation.md` | mGBA + GDB 启动操作说明 |
| `doc/dev/analysis-card-image-loading-function.md` | 早期静态分析（FUN_08014fa8，BIOS SWI 路径，已证伪） |
