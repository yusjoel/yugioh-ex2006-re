# GBA 4bpp 平铺背景图形格式与导出管线

本文记录对《游戏王 EX2006》对手硬币翻转画面图形数据的调查与导出过程，
涵盖 GBA 4bpp 平铺背景的完整格式规范、本项目中的实际数据布局，
以及可复用的 Python 导出实现。

---

## 一、GBA 4bpp 平铺背景格式

### 基本单位：图块（Tile）

GBA 背景图形的基本单元是 **8×8 像素图块**，使用 4bpp（4 位每像素）编码。

每个图块占 **32 字节**（8×8 × 4bpp / 8 = 32 B）。

**字节排列规则**：每字节存储 2 个像素，低 4 位是左侧像素，高 4 位是右侧像素，
行优先（从左到右、从上到下）：

```
字节 0 → 第0行第0列（低4位）、第0行第1列（高4位）
字节 1 → 第0行第2列（低4位）、第0行第3列（高4位）
...
字节16 → 第1行第0列（低4位）、第1行第1列（高4位）
...
```

Python 解码示例：

```python
def decode_tile(rom, offset):
    """解码单个 4bpp 8×8 图块，返回 64 个色彩索引（行优先）。"""
    indices = []
    for i in range(32):
        byte = rom[offset + i]
        indices.append(byte & 0xF)   # 左像素（低4位）
        indices.append(byte >> 4)    # 右像素（高4位）
    return indices
```

### 调色板（Palette）

GBA 4bpp 背景使用 **子调色板（sub-palette）** 机制：

- 背景调色板区（BG Palette RAM，地址 `0x05000000`）共 512 字节
- 分为 **16 个子调色板**，每个子调色板 **16 色 × 2 字节 = 32 字节**
- 总计 256 色，但每个图块只能引用其中一个子调色板（16 色）

**颜色格式**：BGR555（小端 16 位）

| 位 | 14–10 | 9–5 | 4–0 |
|-----|-------|-----|-----|
| 含义 | B (蓝) | G (绿) | R (红) |

每个通道 5 位，转换为 8 位的公式：`R8 = (R5 << 3)`（低 3 位补零）。

**透明色**：每个子调色板的**第 0 号颜色**（色索引 0）为透明，不渲染。

Python 解码示例：

```python
import struct

def decode_palette(rom, offset, n_subpals=16):
    """读取 n_subpals 个子调色板，返回 list[list[(r,g,b,a)]]。"""
    palettes = []
    for s in range(n_subpals):
        colors = []
        for c in range(16):
            raw = struct.unpack_from('<H', rom, offset + (s * 16 + c) * 2)[0]
            r = (raw & 0x1F) << 3
            g = ((raw >> 5) & 0x1F) << 3
            b = ((raw >> 10) & 0x1F) << 3
            a = 0 if c == 0 else 255   # 色0 透明
            colors.append((r, g, b, a))
        palettes.append(colors)
    return palettes
```

### Tilemap（图块映射表）

Tilemap 描述屏幕上每个格子显示哪个图块、如何翻转、使用哪个子调色板。

GBA 标准屏幕分辨率 **240×160**，以 8×8 格为单位划分为 **30×20 个格子**，
共 600 个 Tilemap 条目，占 **1200 字节（0x4B0）**。

**每个条目为 16 位小端整数**：

| 位 | 15–12 | 11 | 10 | 9–0 |
|----|-------|----|----|-----|
| 含义 | 子调色板编号（0–15） | 垂直翻转 | 水平翻转 | 图块索引（0–1023） |

Python 解码渲染示例：

```python
from PIL import Image

def render_tilemap_image(rom, tiles_off, tilemap_off, palette_off,
                         map_w=30, map_h=20, n_tiles=256):
    palettes = decode_palette(rom, palette_off, n_subpals=16)
    tiles = [decode_tile(rom, tiles_off + t * 32) for t in range(n_tiles)]

    img = Image.new('RGBA', (map_w * 8, map_h * 8), (0, 0, 0, 0))
    pixels = img.load()

    for row in range(map_h):
        for col in range(map_w):
            entry = struct.unpack_from('<H', rom, tilemap_off + (row * map_w + col) * 2)[0]
            tile_idx = entry & 0x3FF
            hflip    = bool(entry & 0x400)
            vflip    = bool(entry & 0x800)
            subpal   = (entry >> 12) & 0xF

            if tile_idx >= n_tiles:
                continue

            tile_data = tiles[tile_idx]
            for ty in range(8):
                src_ty = 7 - ty if vflip else ty
                for tx in range(8):
                    src_tx = 7 - tx if hflip else tx
                    color_idx = tile_data[src_ty * 8 + src_tx]
                    pixels[col * 8 + tx, row * 8 + ty] = palettes[subpal][color_idx]
    return img
```

---

## 二、本项目的数据布局

### 对手大图（27 个对手 × Top/Bottom）

对手硬币翻转画面的大图数据位于 ROM 偏移 `0x1B101AC ~ 0x1B8FB8B`，结构如下：

| 偏移范围 | 内容 | 大小 | 备注 |
|---------|------|------|------|
| `0x1B101AC ~ 0x1B1200B` | 调色板块（Copy 1） | 7776 B | 内部结构不规则（见下文） |
| `0x1B1200C ~ 0x1B4800B` | Top 图块（4bpp） | 221184 B | 27 × 0x2000 B，⚠️ 有例外 |
| `0x1B4800C ~ 0x1B4FE9B` | Top Tilemap | 32400 B | 27 × 0x4B0 B，完全规则 |
| `0x1B4FE9C ~ 0x1B51CFB` | 调色板块（Copy 2） | 7776 B | 与 Copy 1 **完全相同** |
| `0x1B51CFC ~ 0x1B87CFB` | Bottom 图块（4bpp） | 221184 B | 27 × 0x2000 B |
| `0x1B87CFC ~ 0x1B8FB8B` | Bottom Tilemap | 32400 B | 27 × 0x4B0 B，完全规则 |

#### 对手顺序

Tilemap 在 ROM 中的顺序（与 `tools/rom-export/export_gfx.py` 中 `LARGE_GFX` 列表顺序一致）：

| 序号 | 英文 slug | 序号 | 英文 slug |
|------|----------|------|----------|
| 0 | kuriboh | 14 | helios_duo_megiste |
| 1 | scapegoat | 15 | gilford_the_legend |
| 2 | skull_servant | 16 | dark_eradicator_warlock |
| 3 | watapon | 17 | guardian_exode |
| 4 | pikeru | 18 | goldd |
| 5 | batteryman_c | 19 | elemental_hero_electrum |
| 6 | ojama_yellow | 20 | raviel |
| 7 | goblin_king | 21 | horus |
| 8 | des_frog | 22 | stronghold |
| 9 | water_dragon | 23 | sacred_phoenix |
| 10 | redd | 24 | cyber_end_dragon |
| 11 | vampire_genesis | 25 | mirror_match |
| 12 | infernal_flame_emperor | 26 | copycat |
| 13 | ocean_dragon_lord | | |

### 小图标（27 个）

| 偏移范围 | 内容 | 大小 |
|---------|------|------|
| `0x188DA70 ~ 0x188F8CF` | 图标图块（4bpp） | 7776 B = 27 × 9 tiles × 32 B |
| `0x18963D0 ~ 0x189672F` | 图标调色板 | 864 B = 27 × 32 B（1 个子调色板） |

小图标为 **3×3 图块（24×24 像素）**，无 Tilemap，图块按行优先顺序直接排列。

---

## 三、调查中发现的特殊情况

### 1. Elemental Hero Electrum 图块偏移异常

Top 图块区理论上应为 27 × 0x2000 字节完全均匀分布，但第 20 位对手（Electrum）的
图块偏移为 `0x1B3899C`，而不是期望的 `0x1B3800C`，多出 **0x990 = 2448 字节**。

这 2448 字节的额外数据来源未知（可能是一段被覆盖的残留数据）。由于 Top 图块
整段仍是连续的，处理方式是将整段作为**一个 incbin**，不做每对手拆分。

### 2. 调色板块内部结构不规则

调色板区（7776 字节，`0x1B101AC`）并非简单的 27 × 288 字节均匀分布。
相邻对手调色板起始偏移的间距不完全一致：

| 对手 | 间距（到下一对手） | 备注 |
|------|-----------------|------|
| kuriboh → scapegoat | 0x80（4 个子调色板） | 偏小 |
| scapegoat → skull_servant | 0x1C0（14 个子调色板） | 偏大 |
| gilford → guardian_exode | 0x240（18 个子调色板） | 偏大 |
| 大多数其他对手 | 0x120（9 个子调色板） | 正常 |

此外，**dark_eradicator_warlock 与 cyber_end_dragon 共享同一个调色板偏移**
（`0x1B11CAC`），说明两者使用相同的颜色方案。

> **结论**：调色板块的内部结构由游戏代码决定，目前难以按对手拆分为独立文件。
> 当前实现将整块 7776 字节作为单一的 `palette_copy1.bin` 进行 incbin 引用。
> 两份相同拷贝（Copy 1 / Copy 2）均引用同一文件，写回时自动保持同步。

### 3. 调色板有两份完全相同的拷贝

ROM 中调色板区出现了两次，Copy 2（`0x1B4FE9C`）与 Copy 1（`0x1B101AC`）内容
完全一致（逐字节相同）。推测游戏分别在加载 Top 图和 Bottom 图时各使用一份，
或者两份是历史遗留冗余。无论如何，修改时必须**同步更新两份**。

### 4. 地址格式：ROM 偏移 vs GBA 指针

文档（Google Sheets）中使用 **Tile Molester / HxD 工具的文件偏移**（如 `01B1200C`），
不包含 GBA 的 ROM 基址。

换算关系：

```
GBA 指针 = ROM 文件偏移 + 0x08000000
ROM 文件偏移 = GBA 指针 - 0x08000000
```

文档中 `01B1200C` 对应 GBA 指针 `0x09B1200C`（即代码中 `.word 0x09B1200C`）。

在 Python 中读 ROM 时，直接使用**文件偏移**（不加基址）。

---

## 四、导出管线实现（tools/rom-export/export_gfx.py）

### 数据表

所有对手的图块/Tilemap/调色板偏移在脚本顶部以常量和列表定义：

```python
PALETTE_COPY1_OFF  = 0x1B101AC   # 调色板块起始偏移
PALETTE_COPY1_SIZE = 7776        # 0x1E60

TOP_TILEMAP_BASE   = 0x1B4800C   # Top Tilemap 区起始
BOT_TILEMAP_BASE   = 0x1B87CFC   # Bottom Tilemap 区起始
TILEMAP_SIZE       = 0x4B0       # 每个对手的 Tilemap 字节数

LARGE_GFX = [
    # (slug, top_tiles, top_tilemap, palette, bottom_tiles, bottom_tilemap)
    ('kuriboh', 0x1B1200C, 0x1B4800C, 0x1B101AC, 0x1B51CFC, 0x1B87CFC),
    ...
]
```

### 输出文件

运行 `python tools/rom-export/export_gfx.py` 后生成：

| 文件 | 描述 | 大小 |
|------|------|------|
| `graphics/opponents/palette_copy1.bin` | 完整调色板块 | 7776 B |
| `graphics/opponents/<name>_top_tilemap.bin` | Top Tilemap（×27） | 1200 B 每个 |
| `graphics/opponents/<name>_bottom_tilemap.bin` | Bottom Tilemap（×27） | 1200 B 每个 |
| `graphics/opponents/<name>_top.png` | 渲染合成图（240×160 RGBA） | — |
| `graphics/opponents/<name>_bottom.png` | 同上 | — |
| `graphics/icons/<name>_icon.png` | 图标（24×24 RGBA） | — |

所有 `graphics/` 下文件均不纳入 git（`.gitignore`），仅保留脚本。

### asm/rom.s 中的 incbin 拆分

原来的一段大 incbin 被拆成 8 段：

```asm
@ 图形数据前段
.incbin "roms/2343.gba", 0x1000000, 0xB101AC

@ 调色板块（Copy 1）
.incbin "graphics/opponents/palette_copy1.bin"

@ Top 图块（保留 ROM incbin，因 Electrum 偏移异常）
.incbin "roms/2343.gba", 0x1B1200C, 0x36000

@ Top Tilemap（27 个对手各一个文件）
.incbin "graphics/opponents/kuriboh_top_tilemap.bin"
@ ... × 27

@ 调色板块（Copy 2，与 Copy 1 完全相同）
.incbin "graphics/opponents/palette_copy1.bin"

@ Bottom 图块
.incbin "roms/2343.gba", 0x1B51CFC, 0x36000

@ Bottom Tilemap（27 个对手各一个文件）
.incbin "graphics/opponents/kuriboh_bottom_tilemap.bin"
@ ... × 27

@ 剩余段
.incbin "roms/2343.gba", 0x1B8FB8C, 0x2C438E
```

**byte-identical 验证**（差异 = 0）：

```bash
python -c "
a=open('roms/2343.gba','rb').read(0x1FFFF00)
b=open('output/2343.gba','rb').read(0x1FFFF00)
print('差异:', sum(x!=y for x,y in zip(a,b)))
"
```

---

## 五、参考：pokeruby 图形管线对比

调研了 [pokeruby](https://github.com/pret/pokeruby) 反编译项目作为参考。

| 方面 | pokeruby | 本项目 |
|------|----------|--------|
| 源格式 | 图块表 PNG（tile sheet）+ JASC-PAL | 渲染合成图 PNG（仅预览） |
| 中间格式 | `.4bpp`（图块二进制）+ `.gbapal` | `tilemap.bin` + `palette_copy1.bin` |
| 工具 | `gbagfx`（C语言，需编译） | Python + Pillow（脚本即用） |
| 构建集成 | Makefile 规则自动转换 | 需手动运行 `export_gfx.py` |
| Tilemap | 链接器处理偏移 | 固定 ROM 偏移，直接 incbin |
| 导入（改图） | PNG → .4bpp → INCBIN | 待实现（T2.3） |

**pokeruby 的关键设计**：存"图块表 PNG"（tile sheet），而不是渲染后的合成图。
这使导入变为简单的线性流程（读图块表 → 编码 4bpp → 写回 ROM），无需重建 tilemap。
本项目后续实现导入功能时应参考此设计。

---

## 六、后续工作（T2.3）

实现从美术文件重建 ROM 图块数据的导入管线：

```
PNG（修改后的对手图）
  └─ tools/import_gfx.py
      ├─ 量化为 4bpp（最多 16×N 色，受 sub-palette 数量限制）
      ├─ 重建 tilemap（tile dedup，N ≤ 256）
      ├─ 输出 <name>_top_tilemap.bin（更新 tilemap）
      └─ 写回 ROM 图块段（更新 tiles）
```

主要挑战：
- **图块去重**（tile deduplication）：4bpp 大图最多 256 个唯一图块
  （经测试，Kuriboh 使用 253/256，几乎全满，余量极小）
- **调色板量化**：如何最优分配 9 个子调色板的 16 色

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `tools/rom-export/export_gfx.py` | 完整导出实现，含所有对手的 ROM 偏移常量 |
| `asm/rom.s` | 已拆分的 incbin 段，直接引用 `graphics/opponents/*.bin` |
| `doc/um06-romhacking-resource/opponents-coinflip-screen.md` | 原始地址文档（来自 Google Sheets） |
