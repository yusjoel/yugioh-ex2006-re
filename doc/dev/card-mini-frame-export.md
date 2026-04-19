# card-mini-frame（带框小卡图：portrait + landscape）调查报告

**首版**：2026-04-15（P2-1..P2-5，OBJ 路径）  
**更新**：2026-04-19（发现 BG 版本 + 重命名为 card-mini-frame）  
**分析对象**：带卡框的小卡图，含竖版 portrait + 横版 landscape 两个状态；
出现在多个屏幕（card list selection / deck list / 对战场 UI 等）。

---

## 结论（速查）

| 项目 | 值 |
|------|-----|
| tile 基址 | **`0x01326280`** |
| stride | **1152 B** = 上半 576 B (portrait 24×24) + 下半 576 B (landscape 24×24) |
| 格式 | **8bpp tiles**（64 B/tile），每半 9 tile |
| tile_block 数 | **2331**（与大卡图共用） |
| 索引表 | `0x015B5C00`（与大卡图共用） |
| 索引公式 | `tile_block = u16[0x015B5C00 + (card_id*2+flag)*2]` |
| VRAM 目标 | OBJ char base `0x06010000`（card selection 屏）/ BG2 tile base（deck list 屏） |
| 加载函数（OBJ） | `FUN_080c33bc` @ `asm/all.s` L231102 |
| OBJ 调色板 | ROM `0x01E31554..0x01E31713` (4 段, 448 B) |
| BG 调色板 | ROM `0x00510460..0x00510560` (256 B → BG colors 16-143) |
| 导出脚本 | `tools/rom-export/export_card_mini_frame.py` |

## 旧文档 `card-data-structure.md` §三 的错误

旧版本结论基于"区间 `0x01000000..0x01463480`（4.4 MB）/ stride 2240 ≈ 2054"
的表面对齐推测，实际 6 项全错：

| 字段 | 旧 | 实际 |
|------|------|------|
| tile 基址 | `0x01000000` | **`0x01326280`** |
| tile 结束 | `0x01463480` | `~0x015B5400` |
| stride | 2240 | **1152** |
| tile 布局 | 5×7（列优先） | **3×6 行优先** |
| 像素尺寸 | 40×56 | **24×48** |
| tile_block 数 | 2054 | **2331** |

`0x01000000..0x01326280`（3.3 MB）是**其他资产**（疑为字体/UI tile/
主菜单图形等），不是小卡图。

## 调查路径

### 1. 尝试（失败）：mGBA 动态抓 VRAM

mGBA MCP bridge 两次启动均无法初始化（heartbeat 始终 null，read_memory/
screenshot 均超时）。切换至纯静态分析。

### 2. 扫描 `0x01000000` 区字节分布

`tools/ad-hoc/scan_card_list_images.py` 按旧假设 stride 2240 扫描 2054 条目：

- 前半（idx 0..~1500）**无零字节**（nzratio=1.0）、熵 ~4–5
- 后半（idx ≥1500）才有典型 0x00 高频（38%+）和低熵（~3.0）

这种"密度突变"与"8bpp 稀疏 tile"的直觉完全矛盾。
**结论**：旧文档假设的 stride/base 有错。

### 3. 在 `asm/all.s` 搜索 `0x09[0-4]xxxxx` 字面量

目标：找指向 `[0x09000000, 0x09500000)` 的常量。

关键命中：

```
asm/all.s L221746:    .word  0x09326280
asm/all.s L231152:    .word  0x093264c0   (= 0x09326280 + 0x240)
asm/all.s L231191:    .word  0x09326280
asm/all.s L231460:    .word  0x09326280
asm/all.s L323826:    .word  0x09326280
asm/all.s L334286:    .word  0x09326280
asm/all.s L334353:    .word  0x09326280
```

### 4. 分析加载函数 FUN_080c33bc（L231102）

完整字面量池：

| 符号 | 值 | 含义 |
|------|-----|------|
| `DAT_080c3408` | `0x095B5C00` | 索引表（与大卡图共用） |
| `DAT_080c340c` | `0x080000AE` | ROM 头部版本字节 |
| `DAT_080c3410` | `0x02000000` | EWRAM 基址 |
| `DAT_080c3414` | `0x00006C2C` | EWRAM 偏移（flag 字节） |
| **`DAT_080c3418`** | **`0x093264C0`** | tile 基址（第二 slot，`+0x240`） |
| `DAT_080c3450` | `0x095B5C00` | 索引表（第二路径） |
| **`DAT_080c3460`** | **`0x09326280`** | tile 基址（第一 slot） |
| `DAT_080c34F8` | `0x0984FBCC` | 默认/dummy tile 源 |
| **`DAT_080c34FC`** | **`0x06010000`** | **OBJ VRAM char base**（关键！） |

关键指令序列（L231137–L231141，tile_block × 1152 计算）：

```asm
ldrh r2, [r0, #0x0]    @ r2 = tile_block (u16 from index table)
lsls r1, r2, #0x3      @ r1 = tb << 3
adds r1, r1, r2        @ r1 = tb * 9
lsls r1, r1, #0x7      @ r1 = tb * 9 * 128 = tb * 1152
ldr  r0, DAT_080c3418  @ r0 = 0x093264c0 (或 0x09326280)
adds r1, r1, r0        @ r1 = base + tb * 1152
```

`lsls r1, r1, #0x7`（左移 7 位 = ×128）是这个 stride 的关键，与大卡图的
`r1 × 75 × 64 = 4800`（P1 findings §3.3）是**不同的 stride 编码**。

**上半 + 下半双基址布局**：`0x09326280` 与 `0x093264C0` 差 `0x240 = 576 B`。
每个 tile_block 占 1152 B，被视为两个 576 B（= 9 个 64 B tile）半块：
- 上半 9 tile：`0x01326280 + tb × 1152 + [0..576)`
- 下半 9 tile：`0x01326280 + tb × 1152 + [576..1152)`

合起来 18 tile = 3×6 grid = 24×48 像素。

### 5. 渲染验证

`tools/ad-hoc/render_card_list_entry.py` 试多种布局（3×6 / 6×3 / 2×9 / 9×2，
row-major / column-major）渲染灰度 PNG：

- **3×6 row-major** 明显呈卡片轮廓（portrait），上下有 1 tile 高的边框区
- 其他布局均为条纹或错乱图形

Blue-Eyes（tile_block=1）与 DESPAIR（tile_block=1476）灰度渲染可辨识为
白龙/暗属恶魔形象。

### 6. 索引 `card_id ↔ tile_block` 验证

索引表与大卡图完全共用。从 P1 findings 已知：
- card_id 1 = Blue-Eyes → tile_block 1
- card_id 1323 = DESPAIR → tile_block 1476

`tools/rom-export/export_card_mini_frame.py` 通过索引表枚举 card_id → tile_block，
批量导出彩色 RGBA PNG（部分 tile_block 被多个 card_id 共享，走缓存）。

## 调色板：OBJ 与 BG 两套（2026-04-19 确认）

card-mini-frame 在不同屏幕使用不同调色板。两套独立、ROM 源不同。

### (A) OBJ 调色板 — card list selection 屏

**2026-04-15 静态分析结论已被运行时证伪。**

运行时验证（mGBA SS1 卡组构筑界面，读 PALRAM `0x05000200`，dump 存于 `doc/temp/palram_state_cardlist.bin`）：

PALRAM OBJ 调色板（0-127 色，256 字节）精确匹配 ROM 文件偏移 `0x01E31614`（GBA 地址 `0x09E31614`）。
**不来自** `0x084C76C0` 的 per-card 动态 palette。

### 加载函数分析

屏幕初始化函数（内含 `FUN_081011c4` @ `0x081011C4` 的调用路径）在初始化时执行以下 4 次 memcpy（见 `asm/all.s` L334094–L334111）：

| dst（PALRAM） | src（ROM） | 字节数 | 含义 |
|---|---|---|---|
| `0x05000140` | `0x09E31554` | 32 | BG palette colors 160-175 |
| `0x05000300` | `0x09E31554` | 32 | OBJ colors 128-143 |
| `0x05000320` | `0x09E31574` | 32 | OBJ colors 144-159 |
| `0x05000200` | `0x09E31614` | **256** | **OBJ colors 0-127（主调色板）** |

关键汇编片段（L334094–L334111）：
```asm
ldr r0, DAT_081011a8     @ 0x05000140 (BG dst)
ldr r4, DAT_081011ac     @ 0x09E31554 (ROM src)
movs r2, #0x20 / bl FUN_080f4ea4  @ 32B
ldr r0, DAT_081011b0     @ 0x05000300 (OBJ+0x100)
adds r1, r4, #0          @ 同上 src
movs r2, #0x20 / bl FUN_080f4ea4  @ 32B
ldr r0, DAT_081011b4     @ 0x05000320 (OBJ+0x120)
ldr r1, DAT_081011b8     @ 0x09E31574
movs r2, #0x20 / bl FUN_080f4ea4  @ 32B
ldr r0, DAT_081011bc     @ 0x05000200 (OBJ base)
ldr r1, DAT_081011c0     @ 0x09E31614
movs r2,#0x80; lsls r2,r2,#1 / bl FUN_080f4ea4  @ 256B ← 主调色板
```

### 调用链

```
FUN_080fdef4 (卡组构筑界面初始化)
  └─ ... (含调色板加载序列)
  └─ FUN_081011c4  (卡列表 tile 加载主循环)
```

`FUN_080fdef4` 有 4 个调用点：
- `0x080FF4E4`、`0x0810869A`、`0x08108BE6`、`0x08108FA2`

### 重要澄清：`0x084C76C0` 是大卡图专用

`FUN_080bff6c` 中 `0x084C76C0` + card_palette_idx × 128 是**大卡图**（card info page）的 per-card 动态调色板，与卡列表小图无关。

`FUN_080c33bc`（小卡图 tile 加载）只加载 tile，不涉及 palette——小卡图 palette 由上层屏幕初始化统一加载静态调色板 `0x09E31614`。

### ROM 调色板数据布局

| ROM 文件偏移 | GBA 地址 | 大小 | 用途 |
|---|---|---|---|
| `0x01E31554` | `0x09E31554` | 32 B | BG+OBJ 辅助调色板（colors 128-143） |
| `0x01E31574` | `0x09E31574` | 32 B | OBJ 辅助调色板（colors 144-159） |
| `0x01E31614` | `0x09E31614` | 256 B | **OBJ 主调色板（colors 0-127）** |

ROM 区域 `0x09E31xxx` 在 FS_BASE（`0x09E64684`）之前约 0x33070 字节，属于 ROM 后段静态图形/UI 数据区。

### (B) BG 调色板 — deck list 屏（2026-04-19 新增）

deck list 屏使用 BG Mode 0，BG2 以 8bpp 渲染 card-mini-frame（portrait 部分）。
调色板来源完全不同：

- ROM `0x00510460..0x00510560`（256 B）→ PALRAM BG colors 16-143
- colors 0-15 恒为 0（8bpp 透明色）
- colors 144-255 来自 BG pal 9+（0x01E60134 / 0x01E31554 等，与本模块无关）

该 256B 物理位于 `pack_banner_palette`（0x510440..0x510640）**中段**：  
`[0x510440..0x510460) 开头 32B` + `[0x510460..0x510560) 本模块 BG 调色板` +
`[0x510560..0x510640) 尾段 224B`。

两个模块共享物理 ROM 数据；asm/rom.s 由 `pack-banners` 模块的 .incbin 覆盖，
本模块不单独拆出 .s 以免 overlap。

### ROM 调色板数据布局（两套合并）

| ROM 文件偏移 | GBA 地址 | 大小 | 用途 | 归属 |
|---|---|---|---|---|
| `0x00510460` | `0x08510460` | 256 B | BG card-mini-frame（colors 16-143，deck list） | pack-banners 共享 |
| `0x01E31554` | `0x09E31554` | 32 B | BG 160-175 / OBJ 128-143（含 15 种边框色）| card-mini-frame-palette |
| `0x01E31574` | `0x09E31574` | 32 B | OBJ 144-159 | card-mini-frame-palette |
| `0x01E31594` | `0x09E31594` | 128 B | UI gap | card-mini-frame-palette |
| `0x01E31614` | `0x09E31614` | 256 B | **OBJ 主调色板（colors 0-127）** | card-mini-frame-palette |

### 边框色 — 全部预置在调色板中

早期推测"OBJ color 128 运行时按卡类型动态覆写"已证伪（2026-04-19）：
- `pal_128`（16 色）已包含 15 种卡类型的边框色
- 每张卡的 tile 字节在边框像素处使用正确的调色板 index
- 不存在 `BORDER_BY_SUBTYPE` 运行时替换机制

### 结构化汇编

Byte-identical 验证通过：

| 文件 | 内容 |
|------|------|
| `data/card-mini-frame.s` | `card_mini_frame_tile_data` label + 2331 × 1152 B tile bin |
| `data/card-mini-frame-palette.s` | `card_mini_frame_pal_{128,144,gap,main}` 四段 OBJ 调色板 |
| `asm/rom.s` | seg-A-1 接入 tile data；中间段接入 OBJ palette |

## 相关文件

| 文件 | 说明 |
|------|------|
| `asm/all.s` L231102 | `FUN_080c33bc`（OBJ 路径 tile 加载） |
| `asm/all.s` L334094 | OBJ 调色板 4 次 memcpy 序列 |
| `data/card-mini-frame.s` | tile 数据结构化汇编 |
| `data/card-mini-frame-palette.s` | OBJ 调色板结构化汇编 |
| `tools/rom-export/export_card_mini_frame.py` | 批量导出脚本（双版本 PNG） |
| `tools/ad-hoc/scan_card_list_images.py` | 字节分布扫描（历史） |
| `tools/ad-hoc/render_card_list_entry.py` | 多布局渲染测试（历史） |
| `doc/dev/p1-phase-b2-findings.md` | 大卡图分析（方法论参照） |
| `doc/dev/card-data-structure.md` §三 | 精简落地结论 |
