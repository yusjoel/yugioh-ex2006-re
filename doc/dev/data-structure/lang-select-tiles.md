# 语言选择画面图形块 (lang-select tiles)

游戏启动后的语言/地区选择画面 (6 国旗 UI) 的 tile+palette+map 图形资源。

## 位置

| 项 | 值 |
|---|---|
| ROM 区间 | `0x0800AA10 ~ 0x0800DD90` (4 块, 0x3380 B) |
| 消费者 | `render_lang_select_tiles_and_text` (@0x080ebbxx) → `load_pack_tile_and_map_to_vram` |
| 后续 (0xDD90~0x13510) | 另一段异构数据 (0xDD90/0xDDB0 为 `copy_bytes_by_halfword` 直拷源 + 未结构化数据), 不属本表 |

## 块结构

每块 = **三个同构子块**, 各 `[u16 count][6B 头][count × elem]`:

| 子块 | elem 大小 | 内容 | 目标 |
|---|---|---|---|
| palette | 2 B | u16 BGR555 调色板色 | PALRAM (0x05000000 + slot×2) |
| tile | 32 B | 8×8 4bpp tile | BG VRAM (0x06004000 + slot×32) |
| map | 4 B | 2×u16 (tile_idx + attr) 每行迭代 | BG tilemap (`write_tile_row_to_vram`) |

6 字节头实测为 count 重复 (`[count,count,count]`), 作用未深究; 提取时整块原样保留。

**map entry 格式** (4 B = 2 u16, 据 `write_tile_row_to_vram` @0x080edf4c):
- `A`: X = `A & 0x3f` (列, >31 走第二 screenblock), Y = `A >> 8` (行); 屏幕位置 = X + Y*32 + param0
- `B`: 标准 GBA BG tilemap 项 —— `B & 0x3ff` = tile 索引 (+ param2 tile base), `B & 0x400` =
  hflip, `B & 0x800` = vflip, `B & 0xf000` = 调色板号
- ⚠ 渲染必须用 `B & 0x3ff` 取 tile 并应用 hflip/vflip; 用裸 B 判断会漏掉带翻转位的整行
  (边框上下/左右常用 vflip/hflip 镜像 → 否则缺最后一行)。

| 块 | 地址 | palette | tile | map | 内容 (render_screen 确认) |
|---|---|---|---|---|---|
| 0 | 0x0800AA10 | 16 | 72 | 144 | 6 国旗 (EN=美国旗, NTSC/US 版) |
| 1 | 0x0800B588 | 16 | 82 | 144 | 6 国旗 (EN=英国旗, PAL/EU 版) |
| 2 | 0x0800C240 | 16 | 40 | 360 | 窗口/边框 UI 叠层 (绿黄框, 洋红=透明) |
| 3 | 0x0800CD18 | 16 | 2 | 1024 | 背景平铺 (2 tile × 大 map) |

6 国旗 3×2 排布 = 6 语言区: 日 JA / 英 EN / 德 DE / 法 FR / 意 IT / 西 ES。


## 文件

仿 `graphics/bin/duel-field/` 组织: palettes/tiles/tilemaps 分组纯数据 + images 每 tilemap 一图。
8B 子块 header (实测 = count 重复 4×) 放 `.s` (`.hword`), 纯数据放 `.bin`。

| 文件 | 内容 | 入库 |
|---|---|---|
| `tools/rom-export/export_ui_tile_blocks.py` | 解析+提取+渲染 (接入 export_all.py) | ✓ |
| `data/lang-select-tiles.s` | 各子块 header(.hword) + 分组 `.incbin` (asm 经 SKIP_REGION `.include`) | ✗ (生成) |
| `graphics/bin/lang-select/palettes/block_N.bin` | 纯调色板 (n_pal × u16 BGR555) | ✗ (生成) |
| `graphics/bin/lang-select/tiles/block_N.bin` | 纯 tile (n_tile × 32B 4bpp) | ✗ (生成) |
| `graphics/bin/lang-select/tilemaps/block_N.bin` | 纯 tilemap (n_map × 4B); 无 map 则不生成 | ✗ (生成) |
| `graphics/images/lang-select/block_N.png` | 每 tilemap 还原一图 (无 map → tile sheet) | ✗ (生成) |

byte-identical: `data/lang-select-tiles.s` 顺序 incbin 4 块原字节 = 原 ROM 0xAA10..0xDD90;
`ExportRangeToGas.py` SKIP_REGIONS 跳过该区改 `.include`。验证: SHA1 9689337d。
