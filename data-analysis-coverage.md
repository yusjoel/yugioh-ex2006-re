# ROM 数据区分析覆盖报告

> 分析对象：`roms/2343.gba`（BY6E, 33,554,432 B）  
> 代码段：`asm/rom_header.s` + `asm/crt0.s` + `asm/all.s`（结束于 ROM `0x004C7638`）  
> 数据段：`0x004C7638` – `0x02000000`

## 概览

- 数据区总大小：**28,543,432 B**（~27.2 MB）
- 已分析：**21,842,908 B（76.53%）**
- 未分析：**6,700,524 B（23.47%）**

分类规则：
- **已分析** = `asm/rom.s` 中以 `.include "data/*.s"` 或 `.incbin "graphics/bin/..."` / `.incbin "fs/..."` 形式明确拆出的段
- **未分析** = 仍以 `.incbin "roms/2343.gba", off, size` 直接引用原 ROM 的段

## 未分析段（按大小倒序）

| 起址 | 大小 | 字节数 | 备注 |
|---:|---:|---:|---|
| `0x01896730` | `0x279A7C` | 2,595,452 | 小图标调色板后，对手调色板 Copy1 前 |
| `0x01B8FB8C` | `0x13CF04` | 1,298,180 | 后 16MB 第一段剩余，字库前段 |
| `0x01ED49D4` | `0x12B62C` | 1,226,284 | FS 后尾段 |
| `0x01CE822C` | `0xD6DEE` | 880,110 | 字库后段后部 |
| `0x01DFF9D2` | `0x31B82` | 203,650 | 游戏文本后，卡列表调色板前 |
| `0x01E31714` | `0x275FA` | 161,274 | 调色板后，对手卡值前 |
| `0x01867560` | `0x26510` | 156,944 | 内场调色板后，小图标图块前 |
| `0x01832602` | `0x1E51A` | 124,186 | seg-C 前段（属性表后，HUD 图块前） |
| `0x0188F8D0` | `0x6B00` | 27,392 | 小图标 tile 后，小图标调色板前 |
| `0x01E5906E` | `0x1B8E` | 7,054 | 对手卡值后 |
| `0x01CCD290` | `0x16D0` | 5,840 | 字库后段前部 |
| `0x01865E20` | `0x1680` | 5,760 | 未知第 7 内场图块 |
| `0x01E5FD84` | `0x1408` | 5,128 | 预组后，文件路径表前 |
| `0x01E5E618` | `0x918` | 2,328 | 卡包信息表后，禁卡表前 |
| `0x01E5F6CC` | `0x1B8` | 440 | 禁卡表后，初始卡组前 |
| `0x01E5F8EA` | `0x16E` | 366 | 初始卡组后，预组前 |
| `0x004C7638` | `0x88` | 136 | all.s 后 / 大卡图调色板前 |

**合计**：17 段，6,700,524 B（23.47% 数据区）

## 全部段（按 ROM 地址顺序）

| 起址 | 大小 | 字节数 | 状态 | 模块 / 备注 | 源 |
|---:|---:|---:|:-:|---|---|
| `0x004C7638` | `0x88` | 136 | ✗ 未分析 | all.s 后 / 大卡图调色板前 | raw `.incbin roms/2343.gba` |
| `0x004C76C0` | `0x48D80` | 298,368 | ✓ 已分析 | card-image-palettes | `.include data/card-image-palettes.s` |
| `0x00510440` | `0x200` | 512 | ✓ 已分析 | pack-banners (palette, shared) | `.incbin graphics/bin/pack-banners/palettes/pack_banner_palette.bin` |
| `0x00510640` | `0xAABA40` | 11,188,800 | ✓ 已分析 | card-image-tiles | `.include data/card-image-tiles.s` |
| `0x00FBC080` | `0x36A200` | 3,580,416 | ✓ 已分析 | card-medium-frame | `.include data/card-medium-frame.s` |
| `0x01326280` | `0x28F980` | 2,685,312 | ✓ 已分析 | card-mini-frame | `.include data/card-mini-frame.s` |
| `0x015B5C00` | `0x20CC` | 8,396 | ✓ 已分析 | card-image-index | `.include data/card-image-index.s` |
| `0x015B7CCC` | `0x1800` | 6,144 | ✓ 已分析 | cards-ids-array | `.include data/cards-ids-array.s` |
| `0x015B94CC` | `0x20C8` | 8,392 | ✓ 已分析 | card-passcodes (2098×u32, LCG-XOR 加密) | `.include data/card-passcodes.s` |
| `0x015BB594` | `0x44978` | 280,952 | ✓ 已分析 | card-names (pool + 2098×6 u32 指针表, 合并) | `.include data/card-names.s` |
| `0x015FFF0C` | `0x216AAC` | 2,189,996 | ✓ 已分析 | card-descriptions (pool + offset 表, 合并 effect-text) | `.include data/card-descriptions.s` |
| `0x018169B8` | `0x1BC4A` | 113,738 | ✓ 已分析 | card-stats (首条 20B, 其余 5169 × 22B) | `.include data/card-stats.s` |
| `0x01832602` | `0x1E51A` | 124,186 | ✗ 未分析 | seg-C 前段（属性表后，HUD 图块前） | raw `.incbin roms/2343.gba` |
| `0x01850B1C` | `0x4130` | 16,688 | ✓ 已分析 | duel-field HUD (tiles+palettes) | `.incbin graphics/bin/duel-field/{tiles,palettes}/hud_*.bin` |
| `0x018515FC` | `0x400` | 1,024 | ✓ 已分析 | HUD gap tile sheet (稀疏 4bpp) | `.incbin graphics/bin/duel-field/tiles/hud_gap_tiles.bin` |
| `0x0185504C` | `0x3740` | 14,144 | ✓ 已分析 | duel-field outer images (6 modes) | `.incbin graphics/bin/duel-field/tiles/*_outer_image.bin` |
| `0x0185878C` | `0xBFC` | 3,068 | ✓ 已分析 | 外场 extra tiles + 外场调色板指针表 | `.incbin graphics/bin/duel-field/{tiles,tilemaps}/duel_field_outer_{extra_tiles,palette_pointers}.bin` |
| `0x01859388` | `0x180` | 384 | ✓ 已分析 | duel-field outer palettes (6 modes) | `.incbin graphics/bin/duel-field/palettes/*_outer_palette.bin` |
| `0x01859508` | `0x40` | 64 | ✓ 已分析 | duel-field extra palette (2×16 色) | `.incbin graphics/bin/duel-field/palettes/duel_field_extra_palette.bin` |
| `0x01859548` | `0x1C` | 28 | ✓ 已分析 | duel-field HUD tilemap pointers | `.incbin graphics/bin/duel-field/tilemaps/hud_phases_tilemap_pointers.bin` |
| `0x01859564` | `0x1C20` | 7,200 | ✓ 已分析 | duel-field outer LP tilemap (6 modes) | `.incbin graphics/bin/duel-field/tilemaps/*_outer_lp_tilemap.bin` |
| `0x0185B184` | `0x4B0` | 1,200 | ✓ 已分析 | duel-field phases map | `.incbin graphics/bin/duel-field/tiles/hud_phases_map.bin` |
| `0x0185B634` | `0x1C` | 28 | ✓ 已分析 | 外场 Tilemap 指针表 (7 × u32) | `.incbin graphics/bin/duel-field/tilemaps/duel_field_outer_tilemap_pointers.bin` |
| `0x0185B650` | `0x1C20` | 7,200 | ✓ 已分析 | duel-field outer tilemap (6 modes) | `.incbin graphics/bin/duel-field/tilemaps/*_outer_tilemap.bin` |
| `0x0185D270` | `0x4B0` | 1,200 | ✓ 已分析 | 内场公共 Tilemap (30×20, 所有模式共享) | `.incbin graphics/bin/duel-field/tilemaps/duel_field_common_inner_tilemap.bin` |
| `0x0185D720` | `0x8700` | 34,560 | ✓ 已分析 | duel-field inner images (6 modes) | `.incbin graphics/bin/duel-field/tiles/*_inner_image.bin` |
| `0x01865E20` | `0x1680` | 5,760 | ✗ 未分析 | 未知第 7 内场图块 | raw `.incbin roms/2343.gba` |
| `0x018674A0` | `0xC0` | 192 | ✓ 已分析 | duel-field inner palettes (6 modes) | `.incbin graphics/bin/duel-field/palettes/*_inner_palette.bin` |
| `0x01867560` | `0x26510` | 156,944 | ✗ 未分析 | 内场调色板后，小图标图块前 | raw `.incbin roms/2343.gba` |
| `0x0188DA70` | `0x1E60` | 7,776 | ✓ 已分析 | opponent icons tiles (27) | `.incbin graphics/bin/icons/tiles/*_icon_tiles.bin` |
| `0x0188F8D0` | `0x6B00` | 27,392 | ✗ 未分析 | 小图标 tile 后，小图标调色板前 | raw `.incbin roms/2343.gba` |
| `0x018963D0` | `0x360` | 864 | ✓ 已分析 | opponent icons palettes (27) | `.incbin graphics/bin/icons/palettes/*_icon_palette.bin` |
| `0x01896730` | `0x279A7C` | 2,595,452 | ✗ 未分析 | 小图标调色板后，对手调色板 Copy1 前 | raw `.incbin roms/2343.gba` |
| `0x01B101AC` | `0x1E60` | 7,776 | ✓ 已分析 | opponents palette copy1 | `.incbin graphics/bin/opponents/palettes/palette_copy1.bin` |
| `0x01B1200C` | `0x36000` | 221,184 | ✓ 已分析 | opponents top tiles | `.incbin graphics/bin/opponents/tiles/top_tiles_all.bin` |
| `0x01B4800C` | `0x7E90` | 32,400 | ✓ 已分析 | opponents top tilemaps (27) | `.incbin graphics/bin/opponents/tilemaps/*_top_tilemap.bin` |
| `0x01B4FE9C` | `0x1E60` | 7,776 | ✓ 已分析 | opponents palette copy2 | `.incbin graphics/bin/opponents/palettes/palette_copy1.bin (复用)` |
| `0x01B51CFC` | `0x36000` | 221,184 | ✓ 已分析 | opponents bottom tiles | `.incbin graphics/bin/opponents/tiles/bottom_tiles_all.bin` |
| `0x01B87CFC` | `0x7E90` | 32,400 | ✓ 已分析 | opponents bottom tilemaps (27) | `.incbin graphics/bin/opponents/tilemaps/*_bottom_tilemap.bin` |
| `0x01B8FB8C` | `0x13CF04` | 1,298,180 | ✗ 未分析 | 后 16MB 第一段剩余，字库前段 | raw `.incbin roms/2343.gba` |
| `0x01CCCA90` | `0x800` | 2,048 | ✓ 已分析 | font (English 1bpp) | `.include data/font.s` |
| `0x01CCD290` | `0x16D0` | 5,840 | ✗ 未分析 | 字库后段前部 | raw `.incbin roms/2343.gba` |
| `0x01CCE960` | `0x198CC` | 104,652 | ✓ 已分析 | pack-banners (tiles) | `.include data/pack-banners.s` |
| `0x01CE822C` | `0xD6DEE` | 880,110 | ✗ 未分析 | 字库后段后部 | raw `.incbin roms/2343.gba` |
| `0x01DBF01A` | `0x5606` | 22,022 | ✓ 已分析 | deck-strings | `.include data/deck-strings.s` |
| `0x01DC4620` | `0x3B3B2` | 242,610 | ✓ 已分析 | game-strings | `.include data/game-strings.s` |
| `0x01DFF9D2` | `0x31B82` | 203,650 | ✗ 未分析 | 游戏文本后，卡列表调色板前 | raw `.incbin roms/2343.gba` |
| `0x01E31554` | `0x1C0` | 448 | ✓ 已分析 | card-mini-frame-palette | `.include data/card-mini-frame-palette.s` |
| `0x01E31714` | `0x275FA` | 161,274 | ✗ 未分析 | 调色板后，对手卡值前 | raw `.incbin roms/2343.gba` |
| `0x01E58D0E` | `0x360` | 864 | ✓ 已分析 | opponent-card-values | `.include data/opponent-card-values.s` |
| `0x01E5906E` | `0x1B8E` | 7,054 | ✗ 未分析 | 对手卡值后 | raw `.incbin roms/2343.gba` |
| `0x01E5ABFC` | `0x3A1C` | 14,876 | ✓ 已分析 | pack-card-lists | `.include data/pack-card-lists.s` |
| `0x01E5E618` | `0x918` | 2,328 | ✗ 未分析 | 卡包信息表后，禁卡表前 | raw `.incbin roms/2343.gba` |
| `0x01E5EF30` | `0x79C` | 1,948 | ✓ 已分析 | banlists | `.include data/banlists.s` |
| `0x01E5F6CC` | `0x1B8` | 440 | ✗ 未分析 | 禁卡表后，初始卡组前 | raw `.incbin roms/2343.gba` |
| `0x01E5F884` | `0x66` | 102 | ✓ 已分析 | starter-deck | `.include data/starter-deck.s` |
| `0x01E5F8EA` | `0x16E` | 366 | ✗ 未分析 | 初始卡组后，预组前 | raw `.incbin roms/2343.gba` |
| `0x01E5FA58` | `0x32C` | 812 | ✓ 已分析 | struct-decks | `.include data/struct-decks.s` |
| `0x01E5FD84` | `0x1408` | 5,128 | ✗ 未分析 | 预组后，文件路径表前 | raw `.incbin roms/2343.gba` |
| `0x01E6118C` | `0x2A5C` | 10,844 | ✓ 已分析 | file-paths | `.include data/file-paths.s` |
| `0x01E63BE8` | `0xA9C` | 2,716 | ✓ 已分析 | fs-tables | `.include data/fs-tables.s` |
| `0x01E64684` | `0x70350` | 459,600 | ✓ 已分析 | fs-payload (338 files via fs/) | `.include data/fs-payload.s` |
| `0x01ED49D4` | `0x12B62C` | 1,226,284 | ✗ 未分析 | FS 后尾段 | raw `.incbin roms/2343.gba` |

**合计**：63 段（46 已分析 + 17 未分析），28,543,432 B

## 2026-04-22 合并：card-descriptions + card-effect-text

合并前三个相邻表：
- `card-name-pointer-table` (原认为 `0x15F3A5C - 0x15FFF6C`, 12,612 u32)
- `card-effect-text`        (原认为 `0x15FFF6C - 0x1800000`, 2 MB)
- `card-descriptions`       (原认为 `0x1800000 - 0x18169B6`, 92 KB)
- `card-stats`              (原认为 `0x18169B6 - 0x1832602`, 113.7 KB)

发现真实边界如下（含字节重叠）：
- `card-name-pointer-table` 实际 **2098 × 6 = 12,588 u32** (末 `0x15FFF0C`)，末卡 cid=2097 = Fluffy Token
- `card-descriptions` 起点 **`0x15FFF0C`** (原以为 `0x15FFF6C`，往前 96 字节)，合并了原 effect-text + 原 descriptions
- `card-descriptions` 末 u32 (cid=2097 ES offset = `0x0020A532`) 高 2 B 与 `card_stats[0].zero0` (=`0x0020`) **字节重叠** → `card-stats` 起点顺延至 `0x18169B8`，首条少 zero0 字段 (20 B)

结构现在完全统一：`card_name_pointer_table` 与 `card_desc_data` 都是 **per-cid 6-lang offset 表**（都 12,588 u32）。详见 `tools/rom-export/export_card_descriptions.py` 注释。

## 2026-04-22 合并：card-names + card-name-pointer-table

继 card-descriptions 合并之后，把相邻的 **名字池 + 名字指针表** 也合并到单文件 `data/card-names.s`（280,952 B, ROM `0x15BB594 - 0x15FFF0B`）：

- 第 1 段 `card_names_table` 0x15BB594..0x15F3A5B（230,600 B）：2054 个 master 条目 × 6 langs，每 lang 独立子标签 `card_name_<suffix>_<lang>`；alt-art 共享 master 标签
- 第 2 段 `card_name_pointer_table` 0x15F3A5C..0x15FFF0B（50,352 B）：2098 × 6 × u32 偏移，通过宏 `name_offsets <suffix>` 展开（与 `desc_offsets` 同构）

生成器：`export_card_data.py`（接管了原 `export_card_name_pointer_table.py` 的职责，后者已删除）。

## 2026-04-22 小段清理：card-passcodes 破解 + duel-field 5 段结构化

### 0x15B94CC / 8,392 B → 加密卡牌密码表
反编译 `FUN_080ef370` 确认这是 **2098 × u32 加密密码表**：
```
table[cid] XOR key(cid) = passcode_bcd   （hex 数字直接读作十进制 = passcode）
key(cid) = ((cid * 0x343FD + 0x269EC3) >> 16) | 0x9EC30000   （Borland rand LCG）
```
全表验证：2078/2080 与 data.md 一致；cid=0 + 17 张 token 解密出非十进制 → 占位/无密码。
剩 2 张差异为 ROM 选用 Premium Pack 异画版密码：cid=689 Polymerization = 27847700 (PP6)，cid=911 Dark Magician = 36996508 (PP4 潘多拉版)。
新文件 `data/card-passcodes.s`（2098 × `.word`），导出脚本 `tools/rom-export/export_card_passcodes.py`，逆查函数 `FUN_080ef38c` 全表线性扫描。

### Duel-field 5 段 → gfx bin
- `0x18515FC / 0x400` → `hud_gap_tiles.bin`（HUD gap 稀疏 4bpp tile sheet）
- `0x185878C / 0xBFC` → 拆为 `duel_field_outer_extra_tiles.bin`（0xBE0, ~95 tiles）+ `duel_field_outer_palette_pointers.bin`（0x1C, 7 × u32）
- `0x1859508 / 0x40` → `duel_field_extra_palette.bin`（2 × 16 色；第 1 半 primary+half 色板，第 2 半金色渐变）
- `0x185B634 / 0x1C` → `duel_field_outer_tilemap_pointers.bin`（外场 Tilemap 指针表 7 × u32）
- `0x185D270 / 0x4B0` → `duel_field_common_inner_tilemap.bin`（内场公共 Tilemap, 30×20）

未分析段：23 → 17，未分析字节：6,714,300 → 6,700,524（清理 13,776 B；剩 5 段混合表 + 4 个大图形 bundle）。
