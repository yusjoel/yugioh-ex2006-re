# ROM 数据区分析覆盖报告

> 分析对象：`roms/2343.gba`（BY6E, 33,554,432 B）  
> 代码段：`asm/rom_header.s` + `asm/crt0.s` + `asm/all.s`（结束于 ROM `0x004C7638`）  
> 数据段：`0x004C7638` – `0x02000000`

## 概览

- 数据区总大小：**28,543,432 B**（~27.2 MB）
- 已分析：**18,248,716 B（63.93%）**
- 未分析：**10,294,716 B（36.07%）**

分类规则：
- **已分析** = `asm/rom.s` 中以 `.include "data/*.s"` 或 `.incbin "graphics/bin/..."` / `.incbin "fs/..."` 形式明确拆出的段
- **未分析** = 仍以 `.incbin "roms/2343.gba", off, size` 直接引用原 ROM 的段

## 未分析段（按大小倒序）

| 起址 | 大小 | 字节数 | 备注 |
|---:|---:|---:|---|
| `0x01000000` | `0x326280` | 3,302,016 | 后 16MB 第一段前半前部（卡列表 tile 前） |
| `0x01896730` | `0x279A7C` | 2,595,452 | 小图标调色板后，对手调色板 Copy1 前 |
| `0x01B8FB8C` | `0x13CF04` | 1,298,180 | 后 16MB 第一段剩余，字库前段 |
| `0x01ED49D4` | `0x12B62C` | 1,226,284 | FS 后尾段 |
| `0x01CE822C` | `0xD6DEE` | 880,110 | 字库后段后部 |
| `0x00FBC080` | `0x43F80` | 278,400 | 大卡图 tile 区后剩余 |
| `0x01DFF9D2` | `0x31B82` | 203,650 | 游戏文本后，卡列表调色板前 |
| `0x01E31714` | `0x275FA` | 161,274 | 调色板后，对手卡值前 |
| `0x01867560` | `0x26510` | 156,944 | 内场调色板后，小图标图块前 |
| `0x01832602` | `0x1E51A` | 124,186 | seg-C 前段（属性表后，HUD 图块前） |
| `0x0188F8D0` | `0x6B00` | 27,392 | 小图标 tile 后，小图标调色板前 |
| `0x015B94CC` | `0x20C8` | 8,392 | cards_ids_array 后至卡名表前 |
| `0x01E5906E` | `0x1B8E` | 7,054 | 对手卡值后 |
| `0x01CCD290` | `0x16D0` | 5,840 | 字库后段前部 |
| `0x01865E20` | `0x1680` | 5,760 | 未知第 7 内场图块 |
| `0x01E5FD84` | `0x1408` | 5,128 | 预组后，文件路径表前 |
| `0x0185878C` | `0xBFC` | 3,068 | 外场图块后（含外场调色板指针表） |
| `0x01E5E618` | `0x918` | 2,328 | 卡包信息表后，禁卡表前 |
| `0x0185D270` | `0x4B0` | 1,200 | 内场公共 Tilemap |
| `0x018515FC` | `0x400` | 1,024 | HUD 未知 gap |
| `0x01E5F6CC` | `0x1B8` | 440 | 禁卡表后，初始卡组前 |
| `0x01E5F8EA` | `0x16E` | 366 | 初始卡组后，预组前 |
| `0x004C7638` | `0x88` | 136 | all.s 后 / 大卡图调色板前 |
| `0x01859508` | `0x40` | 64 | LP/阶段 Tilemap 指针表前未知段 |
| `0x0185B634` | `0x1C` | 28 | 外场 Tilemap 指针表 |

**合计**：25 段，10,294,716 B（36.07% 数据区）

## 全部段（按 ROM 地址顺序）

| 起址 | 大小 | 字节数 | 状态 | 模块 / 备注 | 源 |
|---:|---:|---:|:-:|---|---|
| `0x004C7638` | `0x88` | 136 | ✗ 未分析 | all.s 后 / 大卡图调色板前 | raw `.incbin roms/2343.gba` |
| `0x004C76C0` | `0x48D80` | 298,368 | ✓ 已分析 | card-image-palettes | `.include data/card-image-palettes.s` |
| `0x00510440` | `0x200` | 512 | ✓ 已分析 | pack-banners (palette, shared) | `.incbin graphics/bin/pack-banners/palettes/pack_banner_palette.bin` |
| `0x00510640` | `0xAABA40` | 11,188,800 | ✓ 已分析 | card-image-tiles | `.include data/card-image-tiles.s` |
| `0x00FBC080` | `0x43F80` | 278,400 | ✗ 未分析 | 大卡图 tile 区后剩余 | raw `.incbin roms/2343.gba` |
| `0x01000000` | `0x326280` | 3,302,016 | ✗ 未分析 | 后 16MB 第一段前半前部（卡列表 tile 前） | raw `.incbin roms/2343.gba` |
| `0x01326280` | `0x28F980` | 2,685,312 | ✓ 已分析 | card-mini-frame | `.include data/card-mini-frame.s` |
| `0x015B5C00` | `0x20CC` | 8,396 | ✓ 已分析 | card-image-index | `.include data/card-image-index.s` |
| `0x015B7CCC` | `0x1800` | 6,144 | ✓ 已分析 | cards-ids-array | `.include data/cards-ids-array.s` |
| `0x015B94CC` | `0x20C8` | 8,392 | ✗ 未分析 | cards_ids_array 后至卡名表前 | raw `.incbin roms/2343.gba` |
| `0x015BB594` | `0x384C8` | 230,600 | ✓ 已分析 | card-names | `.include data/card-names.s` |
| `0x015F3A5C` | `0xC510` | 50,448 | ✓ 已分析 | card-name-pointer-table | `.include data/card-name-pointer-table.s` |
| `0x015FFF6C` | `0x200094` | 2,097,300 | ✓ 已分析 | card-effect-text | `.include data/card-effect-text.s` |
| `0x01800000` | `0x169B6` | 92,598 | ✓ 已分析 | card-descriptions | `.include data/card-descriptions.s` |
| `0x018169B6` | `0x1BC4C` | 113,740 | ✓ 已分析 | card-stats | `.include data/card-stats.s` |
| `0x01832602` | `0x1E51A` | 124,186 | ✗ 未分析 | seg-C 前段（属性表后，HUD 图块前） | raw `.incbin roms/2343.gba` |
| `0x01850B1C` | `0x4130` | 16,688 | ✓ 已分析 | duel-field HUD (tiles+palettes) | `.incbin graphics/bin/duel-field/{tiles,palettes}/hud_*.bin` |
| `0x018515FC` | `0x400` | 1,024 | ✗ 未分析 | HUD 未知 gap | raw `.incbin roms/2343.gba` |
| `0x0185504C` | `0x3740` | 14,144 | ✓ 已分析 | duel-field outer images (6 modes) | `.incbin graphics/bin/duel-field/tiles/*_outer_image.bin` |
| `0x0185878C` | `0xBFC` | 3,068 | ✗ 未分析 | 外场图块后（含外场调色板指针表） | raw `.incbin roms/2343.gba` |
| `0x01859388` | `0x180` | 384 | ✓ 已分析 | duel-field outer palettes (6 modes) | `.incbin graphics/bin/duel-field/palettes/*_outer_palette.bin` |
| `0x01859508` | `0x40` | 64 | ✗ 未分析 | LP/阶段 Tilemap 指针表前未知段 | raw `.incbin roms/2343.gba` |
| `0x01859548` | `0x1C` | 28 | ✓ 已分析 | duel-field HUD tilemap pointers | `.incbin graphics/bin/duel-field/tilemaps/hud_phases_tilemap_pointers.bin` |
| `0x01859564` | `0x1C20` | 7,200 | ✓ 已分析 | duel-field outer LP tilemap (6 modes) | `.incbin graphics/bin/duel-field/tilemaps/*_outer_lp_tilemap.bin` |
| `0x0185B184` | `0x4B0` | 1,200 | ✓ 已分析 | duel-field phases map | `.incbin graphics/bin/duel-field/tiles/hud_phases_map.bin` |
| `0x0185B634` | `0x1C` | 28 | ✗ 未分析 | 外场 Tilemap 指针表 | raw `.incbin roms/2343.gba` |
| `0x0185B650` | `0x1C20` | 7,200 | ✓ 已分析 | duel-field outer tilemap (6 modes) | `.incbin graphics/bin/duel-field/tilemaps/*_outer_tilemap.bin` |
| `0x0185D270` | `0x4B0` | 1,200 | ✗ 未分析 | 内场公共 Tilemap | raw `.incbin roms/2343.gba` |
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

**合计**：66 段（41 已分析 + 25 未分析），28,543,432 B
