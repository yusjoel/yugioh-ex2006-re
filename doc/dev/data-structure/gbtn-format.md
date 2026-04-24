# `.gbtn` 文件格式（NTBG bundle）

**magic**: `NTBG`（4 B ASCII）
**用途**: 游戏的 BG 图层资源打包（palette + tilemap + tile graphics 三合一），固件通过 `fs_load` 加载后，代码直接把各子段 DMA 到 PALRAM / VRAM tilemap (SBB) / VRAM tile pool (CBB)。

ROM 里以 **`.LZ5bg`** 扩展名存储（BIOS LZ77 压缩），解压器 `tools/fs-decompress.py` 产出 `.gbtn`。

本 spec 覆盖 **FS 里全部 26 个 `.LZ5bg`** — 结构 100% 统一。

---

## 一、总体结构

```
+0x00  "NTBG" (4B)           文件 magic
+0x04  u16 0xFFFE             BOM（小端序标记）
+0x06  u16 0x0001             version
+0x08  u32 file_size          总字节数
+0x0C  u16 0x0010             header_size（固定 16）
+0x0E  u16 0x0002             section_count（固定 2）
+0x10  PALT section           调色板（长度随 palette_count 变）
+varies BGDT section          BG 数据（tilemap + tile graphics）
```

两个子段之间紧挨，`BGDT` 起点 = `0x10 + PALT.section_size`。

---

## 二、`PALT` section — 调色板

```
+0x00  "PALT" (4B)
+0x04  u32 section_size       = 12 + palette_count × 2
+0x08  u32 palette_count      16（4bpp）或 256（8bpp）
+0x0C  u16[palette_count] palette   BGR555 原始数据
```

**色格式 = GBA 标准 BGR555**（bit15=0，bit14-10=B，bit9-5=G，bit4-0=R）。

颜色 0 固定为 **纯绿 `0x03E0`**（透明键色，游戏不会真的画绿色，是 GBA 透明色约定）。

| palette_count | section_size | bpp 默认 | 备注 |
|---|---|---|---|
| 16 | 0x2C = 44 B | 4bpp | 每 tile 32 B |
| 256 | 0x20C = 524 B | 4bpp **或** 8bpp（需 heuristic） | 256 色 palette **不等于 8bpp** |

**关键陷阱：`palette_count == 256` 并不意味着 tile 是 8bpp。**

很多文件（titleEx、demo 多数）采用 "**256 色 palette 分为 16 个 16 色子调色板**" + **4bpp tile data** 的混合模式。这样渲染时每个 tile 通过 tilemap entry 的 palette bank 位（bit 12-15）选自己的 16 色子集。好处是：tile data 减半（32B vs 64B），但仍能显示丰富颜色。

**自动推断 bpp**（渲染器采用）：
```
count_8bpp = tile_gfx_size / 64
count_4bpp = tile_gfx_size / 32
max_idx    = max(entry & 0x3FF for entry in tilemap)

if palette_count == 16:            → 4bpp  （明确）
elif max_idx < count_8bpp:         → 8bpp  （索引在 8bpp 范围内）
elif max_idx < count_4bpp:         → 4bpp  （索引超 8bpp，必须 4bpp）
else:                              → 4bpp  （fallback）
```

全 26 样本的 bpp 分布：
- **8bpp**: `name_input/*` (4 个) + `demo/vija/BG2_all` (1 个) = **5 个**
- **4bpp**: `titleEx/*` (10 个) + `pass_input/*` (2 个) + `demo/exodia/*` (5 个) + `demo/shuen/*` (2 个) + `demo/vija/BG1_all*` (2 个) = **21 个**

---

## 三、`BGDT` section — BG 数据

```
+0x00  "BGDT" (4B)
+0x04  u32 section_size       = 8 + 20 + tilemap_size + tile_gfx_size
+0x08  u32 flags              取值分析见 §3.1
+0x0C  u32 tilemap_size       tilemap 字节数（= w × h × 2）
+0x10  u16 w1                 tile 宽（tile 单位，= pixels / 8）
+0x12  u16 h1                 tile 高
+0x14  u16 w2                 同 w1（功能待定；所有样本里 w2 == w1）
+0x16  u16 h2                 同 h1
+0x18  u32 tile_gfx_size      tile graphics 字节数（= tile_count × {32,64}）
+0x1C  u16[w1 × h1] tilemap   GBA 标准 tilemap entry
+0x1C + tilemap_size
       u8[] tile_gfx          8bpp: tile_count × 64 B；4bpp: tile_count × 32 B
```

**tile_count** 可由 `tile_gfx_size / (64 if 8bpp else 32)` 推出。

### 3.1 flags 字段取值

全 26 个样本的 flags 有 4 种组合：

| flags (u32 LE) | 样本数 | 含义 |
|---|---|---|
| `0x0002FF00` | 13 | 2B tilemap entry，palette variant A |
| `0x0002FF01` | 5 | 2B tilemap entry，palette variant B |
| `0x0004FF00` | 4 | **4B tilemap entry**（见 §3.2），palette variant A |
| `0x0004FF01` | 2 | **4B tilemap entry**，palette variant B |

字节级解读（u32 LE 展开后）：
- byte[0] = `0x01` 或 `0x00` — palette 变体（用途待反向；`01` 多见于 name_input / vija 大场景）
- byte[1] = `0xFF` — 常数
- byte[2] = **`0x02` 或 `0x04` = tilemap entry 字节宽度**（见 §3.2）
- byte[3] = `0x00` — 常数

### 3.2 tilemap entry：2 字节 vs 4 字节

由 `flags byte[2]` 决定。

**标准 GBA 2-byte entry**（`flags & 0xFF0000 == 0x020000`）：
```
bit  0-9   tile index (0..1023)
bit 10     H-flip
bit 11     V-flip
bit 12-15  palette bank（4bpp 模式下选子调色板）
```

**扩展 4-byte entry**（`flags & 0xFF0000 == 0x040000`）：
```
u16[0]: tile index (bit 0-9) + H-flip (bit 10) + V-flip (bit 11)
u16[1]: palette bank (bit 12-15) + 其它扩展位（待反向）
```

4B entry 格式**不是 GBA 硬件原生 tilemap 格式**，运行时装载器必须重新打包成 2B entry 才能写入 VRAM SBB。好处：允许 tile 索引 + 16 个 palette bank 完全正交，不受 2B entry 的 10+4 位挤压。

用于 **需要大量帧动画 + 高色深**的大 tilemap：`demo/exodia/exodia00_2` / `01` / `02`（各 480~752 px 高的动画帧堆叠）、`demo/vija/BG1_all*`。

### 3.3 tilemap 运行时 base offset

代码不是直接把 `tile[0]` 上传到 VRAM 的 tile slot 0，而是加一个基址（跨页共享 tile 池时避免踩）。例如 `name_b_02` 的 tile 被上传到 CBB3 的 **slot #1+**（base = +1），而 `name_b_01` 上传到 **slot #31+**（base = +31）。tilemap entry 里的 tile index 是**相对**的，上传后的实际 tile_id = entry + base_offset。

base_offset 在上传代码里确定（非 `.gbtn` 文件字段），跨页不同。定位手段：对比 VRAM tilemap 与 .gbtn tilemap，差值即 base。

### 3.4 tile 像素布局

GBA 硬件标准（不是 tileable "MT"/"MP" 复杂打包），直接线性：

**8bpp**（256 色）：8×8 tile = 64 B，每字节 = 1 像素调色板索引。行优先。
```
byte i (i=0..63) → pixel (row=i/8, col=i%8)
```

**4bpp**（16 色）：8×8 tile = 32 B，每字节 = 2 像素（低 4 位 = 左像素，高 4 位 = 右像素）。
```
byte i (i=0..31):
  pixel (row=i/4, col=(i%4)*2)   = byte & 0x0F
  pixel (row=i/4, col=(i%4)*2+1) = byte >> 4
```

---

## 四、字节级证据

文件：`fs-decompressed/name_input/name_b_02.gbtn`（3304 B）

```
offset  bytes (hex)                        meaning
0x0000  4E 54 42 47                        "NTBG"
0x0004  FF FE 00 01                        BOM + version
0x0008  E8 0C 00 00                        file_size = 3304 ✓
0x000C  10 00 02 00                        hdr_size=16, nsec=2
0x0010  50 41 4C 54                        "PALT"
0x0014  0C 02 00 00                        PALT.size = 524
0x0018  00 01 00 00                        palette_count = 256
0x001C  E0 03 ...  (512 B)                 palette u16[] BGR555
0x021C  42 47 44 54                        "BGDT"
0x0220  CC 0A 00 00                        BGDT.size = 2764
0x0224  01 FF 02 00                        flags = 0x0002FF01
0x0228  B0 04 00 00                        tilemap_size = 1200 (= 30×20×2)
0x022C  1E 00 14 00                        w1=30, h1=20
0x0230  1E 00 14 00                        w2=30, h2=20
0x0234  00 06 00 00                        tile_gfx_size = 1536 (= 24×64)
0x0238  00 00 01 00 ...  (1200 B)          tilemap u16[30*20]
0x06E8  F8 F8 F8 F8 ...  (1536 B)          tile_gfx u8[24*64]
0x0CE8  (EOF)
```

相邻 tile bytes 与 mGBA VRAM CBB3 offset `0x40` 逐字节相同（见 `doc/analysis/name-input-page-location.md` §4.2）。

---

## 五、运行时上传流程

`fs_load` 解压 `.LZ5bg` → `.gbtn` 缓冲后，上层代码（例如 `name_input_page_load_assets`）拆出三段：

```
PALT.palette_data   → PALRAM（目标 subpal 由上传代码选定，通常 BG subpal N）
BGDT.tile_gfx       → VRAM CBB x（由 BG?CNT.CBB 决定，可多层共享）
BGDT.tilemap        → VRAM SBB y（由 BG?CNT.SBB 决定），但 tile entry 被
                       翻译成 entry + base_offset 后写入
```

`bios_lz77_uncomp` 解压后目标在 EWRAM `0x0200AF20`，之后 `cpu_copy_auto` (SWI 0xB/0xC) 分段 DMA 到 VRAM/PALRAM。

---

## 六、相关文档

- `tools/fs-decompress.py` — LZ77 解压 + FID 索引
- `tools/rom-export/render_gbtn.py` — .gbtn → PNG 预览渲染器
- `doc/analysis/name-input-page-location.md` §4 — 跨页 .gbtn ↔ BG 层对号实战
- `doc/dev/ghidra-function-names.md` 第五轮 — `fs_load` / `bios_lz77_uncomp` / `cpu_copy_auto` 登记
