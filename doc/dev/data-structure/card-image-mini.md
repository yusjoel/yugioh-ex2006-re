# 小带框卡图（card-mini-frame，24×48 8bpp）

带卡框的小卡图，含竖版 portrait + 横版 landscape 两个状态。出现在卡组构筑界面、deck list、对战场 UI 等。

---

## 参数

| 项目 | 值 |
|------|-----|
| tile 数据基址 | `0x01326280`（GBA `0x09326280`） |
| tile 数据结束 | `~0x015B5400`（= 0x01326280 + 2331 × 1152） |
| stride | **1152 字节 / 卡** = 上半 576 B（portrait 24×24）+ 下半 576 B（landscape 24×24） |
| 像素尺寸 | **24 × 48**（3 × 6 tiles 行优先，上下各 9 tile） |
| tile 内部格式 | 8×8 像素 × 8bpp（64 字节 / tile，未压缩） |
| tile_block 数 | 2331（与 big / medium 共享） |
| 索引表 | `0x015B5C00`（与 big / medium 共享） |
| 索引访问 | `tile_block = u16[0x015B5C00 + (card_id × 2 + flag) × 2]` |
| 加载函数（OBJ 路径） | `FUN_080c33bc`（`asm/all.s` L231102） |

### 双基址布局

tile 数据在加载函数中按"上/下半"分成两个基址：

```
0x09326280  ← portrait 半（上 9 tile）
0x093264C0  ← landscape 半（下 9 tile，= 0x09326280 + 0x240 = +576 B）
```

单个 tile_block 的完整 1152 字节：

```
上半 9 tile：0x01326280 + tb × 1152 + [0..576)
下半 9 tile：0x01326280 + tb × 1152 + [576..1152)
```

---

## 双调色板（OBJ / BG 两套）

小带框卡图在不同屏幕使用不同调色板，**两套独立、ROM 源不同**。

### (A) OBJ 调色板 — card list selection 屏

用于卡组构筑界面。

| ROM 偏移 | GBA 地址 | 大小 | 用途 |
|---|---|---|---|
| `0x01E31554` | `0x09E31554` | 32 B | BG colors 160-175 / OBJ colors 128-143 |
| `0x01E31574` | `0x09E31574` | 32 B | OBJ colors 144-159 |
| `0x01E31594` | `0x09E31594` | 128 B | UI gap |
| `0x01E31614` | `0x09E31614` | **256 B** | **OBJ 主调色板（colors 0-127）** |

VRAM 目标：OBJ char base `0x06010000`（作为 sprite tile）。

### (B) BG 调色板 — deck list 屏

deck list 屏使用 BG Mode 0，BG2 以 8bpp 渲染同一 tile 数据。

| ROM 偏移 | GBA 地址 | 大小 | 用途 |
|---|---|---|---|
| `0x00510460` | `0x08510460` | 256 B | BG colors 16-143（deck list） |

- colors 0-15 恒为 0（8bpp 透明色）
- colors 144-255 来自其他 BG palette 源（与本模块无关）

**物理位置**：该 256B 位于 `pack_banner_palette`（0x510440..0x510640）**中段**，两个模块共享物理 ROM 数据。`asm/rom.s` 由 `pack-banners` 模块的 `.incbin` 覆盖，本模块不单独拆出 `.s`。

---

## 边框色全部预置

15 种卡类型边框色**全部预置**在调色板中：
- `pal_128`（16 色）包含 15 种卡类型的边框色
- 每张卡的 tile 字节在边框像素处使用正确的调色板 index
- **不存在**"运行时按卡类型动态覆写 OBJ color 128"的机制

---

## 加载函数（`FUN_080c33bc` 摘要）

### 字面量池

| 符号 | 值 | 含义 |
|------|-----|------|
| `DAT_080c3408` | `0x095B5C00` | 索引表 |
| `DAT_080c340c` | `0x080000AE` | ROM 版本字节 |
| `DAT_080c3410` | `0x02000000` | EWRAM 基址 |
| `DAT_080c3414` | `0x00006C2C` | EWRAM 偏移（flag 字节） |
| `DAT_080c3418` | `0x093264C0` | tile 基址（下半 slot） |
| `DAT_080c3460` | `0x09326280` | tile 基址（上半 slot） |
| `DAT_080c34F8` | `0x0984FBCC` | 默认/dummy tile 源 |
| `DAT_080c34FC` | `0x06010000` | OBJ VRAM char base |

### tile 偏移计算

```asm
ldrh r2, [r0, #0x0]    @ r2 = tile_block (u16)
lsls r1, r2, #0x3      @ r1 = tb << 3
adds r1, r1, r2        @ r1 = tb * 9
lsls r1, r1, #0x7      @ r1 = tb * 9 * 128 = tb * 1152
ldr  r0, DAT_080c3418  @ base address
adds r1, r1, r0        @ r1 = base + tb * 1152
```

### 调色板加载（屏幕初始化）

OBJ 调色板由屏幕初始化序列（`FUN_080fdef4` → `FUN_081011c4`）执行 4 次 memcpy：

| dst（PALRAM） | src（ROM） | 字节数 | 含义 |
|---|---|---|---|
| `0x05000140` | `0x09E31554` | 32 | BG palette colors 160-175 |
| `0x05000300` | `0x09E31554` | 32 | OBJ colors 128-143 |
| `0x05000320` | `0x09E31574` | 32 | OBJ colors 144-159 |
| `0x05000200` | `0x09E31614` | **256** | **OBJ colors 0-127（主调色板）** |

参见 `asm/all.s` L334094–L334111。

`FUN_080c33bc` 本身**只加载 tile，不涉及 palette**——palette 由上层屏幕初始化统一加载。

---

## 相关文件

| 文件 | 内容 |
|------|------|
| `data/card-mini-frame.s` | tile 数据结构化汇编（2331 × 1152 B）|
| `data/card-mini-frame-palette.s` | OBJ 调色板结构化汇编（四段）|
| `graphics/images/card-mini-frame/{obj,bg}/card_NNNN[_ocg\|_tcg].png` | 彩色 RGBA PNG（OBJ + BG 两套各一份） |
| `tools/rom-export/export_card_mini_frame.py` | 导出脚本 |
