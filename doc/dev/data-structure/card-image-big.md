# 大卡图（详情页 6bpp 80×80）

卡牌详情页显示的主卡图，使用自写 6bpp 压缩格式（非 BIOS SWI）。

---

## 参数

| 项目 | 值 |
|------|-----|
| tile 数据基址 | `0x00510640`（GBA `0x08510640`） |
| tile 数据结束 | `0x00FBC080`（= 0x00510640 + 2331 × 4800） |
| stride | **4800 字节 / 卡** |
| 像素尺寸 | **80 × 80**（10 × 10 tiles） |
| tile 内部格式 | 8×8 像素 × 6bpp（6 ROM 字节 → 8 VRAM 字节） |
| tile_block 数 | 2331（与 medium / mini 共享） |
| 索引表 | `0x015B5C00`（与 medium / mini 共享） |
| 索引表大小 | 6846 × 2 字节 = 13,692 字节（有效 card_id 0–3422） |
| 索引访问 | `tile_block = u16[0x015B5C00 + (card_id × 2 + flag) × 2]` |
| VRAM 目标 | `0x06004000`（BG0 char base block 1，256 色 8bpp） |
| 加载函数 | `FUN_0801d290`（`asm/all.s` L15429） |

### 索引与 card_id

- `card_id` = `data/card-stats.s` 0-indexed 记录序号
- `flag` 由 ROM 头部 `0x080000AE` 高字节判定：`0x4A`（日版）→ flag=0，否则 flag=1
- **本作 BY6E 是非日版**，`flag=1`
- 空条目值 `0xFFFF`（表示该 card_id 在此版本无图）

### 每卡独立调色板

| 项目 | 值 |
|------|-----|
| 调色板基址 | `0x004C76C0` |
| stride | **128 字节 / 卡**（64 色 × BGR555） |
| 访问 | `pal_rom = 0x004C76C0 + tile_block × 128` |
| 占用区间 | `0x004C76C0 – 0x00510440`（~297 KB，紧邻 tile 数据前） |
| 游戏内映射 | 拷贝到 VRAM BG palette `[0x10..0x4F]`（由加载函数第 5 参数 `0x10` 或 `0x82` 决定） |

---

## 6bpp 解码算法

每 6 ROM 字节解压为 8 VRAM 字节（8 个 6bpp 像素）。

### 输入字节

```
W0 = u16_le(ROM[+0..+1])
W1 = u16_le(ROM[+2..+3])
W2 = u16_le(ROM[+4..+5])
```

### 8 个像素提取

```
p0 =  W0        & 0x3F
p1 = (W0 >> 6)  & 0x3F
p2 = ((W0 >> 12) & 0x0F) | ((W1 & 0x03) << 4)
p3 = (W1 >> 2)  & 0x3F
p4 = (W1 >> 8)  & 0x3F
p5 = ((W1 >> 14) & 0x03) | ((W2 & 0x0F) << 2)
p6 = (W2 >> 4)  & 0x3F
p7 = (W2 >> 10) & 0x3F
```

每像素 6 bit，值范围 `0..63`。

### 调色板偏移

解码出的 `p0..p7` 是 **6 bit 原始索引**（0–63）。游戏内再加 `palette_offset` 得到 VRAM 8bpp 最终索引：

```
VRAM_final = raw_6bit + palette_offset
```

已观测的 `palette_offset` 值：`0x10`（映射到 pal[16..79]）、`0x82`（映射到 pal[130..193]）。

**离线导出时**：直接用 `raw_6bit` 索引每卡自身的 64 色调色板（`pal_rom = 0x004C76C0 + tb × 128`），等价效果。

### 循环结构

- 第一循环 800 次：每次 `ROM += 6, VRAM += 8`，共输出 `800 × 8 = 6400` 像素 = **100 tiles × 64 像素**
- 第二循环 3200 次：对已写 VRAM 应用 `VRAM_final = raw & 0x3F + palette_offset`

### Tile 排列

- 100 tiles = **10 × 10 网格**
- 每 tile 内部：8 × 8 像素，**行优先**
- 线性扫描解码后**必须按 10×10 网格重排**，否则显示为条纹

---

## 加载函数签名

```c
// FUN_0801d290 @ 0x0801D290
// r0 = VRAM 目标基址（通常 0x06004000，也见 0x06000000）
// r1 = palette_offset（0x10 或 0x82）
// r2 = card_id
// r3 = flag（0=OCG, 1=TCG, 2=意义待确认）
// [sp+0x28] = 额外参数
void decode_card_image_6bpp(u32 vram_base, u16 pal_offset, u16 card_id, u16 flag, ...);
```

### 调用链

```
card_info_page_entry (0x0801E440)
  ├── card_info_page_init_bg0 (0x0801D45C)         [初始化 BG0，清零 VRAM]
  └── card_image_decode_wrapper (0x0801D998)
         └── decode_card_image_6bpp (0x0801D290)    [6bpp 解码器]
```

`FUN_0801d998` 是 ROM 中**唯一**调用 `FUN_0801d290` 的函数。

### 字面量池（`FUN_0801d290` 内部）

| 符号 | 值 | 含义 |
|------|-----|------|
| DAT_0801d420 | `0x095B5C00` | card image index 表基址 |
| DAT_0801d424 | `0x080000AE` | ROM 头部版本字节地址 |
| DAT_0801d428 | `0x02000000` | EWRAM 基址 |
| DAT_0801d42c | `0x00006C2C` | EWRAM 偏移（卡片 flag 字节） |
| DAT_0801d430 | `0x084C76C0` | per-card 调色板基址 |
| DAT_0801d434 | `0x08510640` | tile 数据 ROM 基址 |
| DAT_0801d438 | `0x06004000` | VRAM 目标地址 |
| DAT_0801d43c | `0x0000031F` | = 799（第一循环限值） |
| DAT_0801d440 | `0x00003F3F` | 第二循环掩码 |
| DAT_0801d444 | `0x00000C7F` | = 3199（第二循环限值） |

---

## card_id ↔ slot_id 映射（已解决）

| card_id | ROM 记录偏移 | slot_id | 卡名 |
|---------|--------------|---------|------|
| 0 | `0x018169B6` | `0x0000` | (占位) |
| 1 | `0x018169CC` | `0x0FA7` | Blue-Eyes White Dragon |
| 672 | `0x0181A606` | `0x12EA` | Monster Reborn |
| 1323 | `0x0181C4E8` | `0x1653` | Despair from the Dark |

EWRAM 卡片对象 `0x0201AFB0` 的 `word0` 提取 `card_id`：

```
card_id = (word0 << 15) >> 18   // 等价于 (word0 >> 3) & 0x1FFF
```

---

## 导出统计（flag=1 / TCG 版全量）

| 项 | 数量 |
|----|------|
| 两版相同（无后缀 PNG） | 1865 |
| 两版不同（_ocg + _tcg 双文件） | 233 |
| 仅单版存在 | 0 |
| 两版都 `0xFFFF` | 0 |
| 写入 PNG 总数 | **2331**（独立 tile_block 0..2330 完整覆盖） |

- card_id 1..2080：正式卡（slot `0x0FA7..0x19FE` 升序）
- card_id 2081..2097：17 张 Token
- card_id 0：`slot=0x0000` 占位记录（象形文字纹理，用途未知）

---

## 已验证示例（DESPAIR FROM THE DARK）

```
card_id      = 1323
slot_id      = 0x1653
tile_block   = 1476
tile 数据地址 = 0x08510640 + 1476 × 4800 = 0x08BD2140
调色板地址    = 0x004C76C0 + 1476 × 128  = 0x004F58C0
配色         = 暗红 + 紫（与游戏内一致）
尺寸         = 80 × 80（10 × 10 tiles，6400 像素）
```

---

## 相关文件

| 文件 | 内容 |
|------|------|
| `data/card-image-tiles.s` | 11.19 MB tile 数据结构化 |
| `data/card-image-palettes.s` | 298 KB 调色板结构化 |
| `data/card-image-index.s` | 索引表 6846 × u16 |
| `tools/rom-export/export_card_images.py` | 批量导出 2331 张 PNG |
| `tools/ad-hoc/decode_card_6bpp.py` | 单卡验证脚本 |
