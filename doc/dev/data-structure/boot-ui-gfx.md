# 早期 UI 画面图形 (boot-ui, 0xDE30~0x13510)

语言选择图形 (lang-select, 见 [`lang-select-tiles.md`](lang-select-tiles.md)) 之后、第一个代码函数
`reset_display_and_gl_state` (0x13510) 之前的 ~21KB 图形数据。内容为若干早期 UI 画面
(菜单/选择: 窗口框、选择框、★星标、灰度渐变条、5 列网格) 的 tile + tilemap。

## 状态: 灰度预览 (未完全识别)

- **无任何静态代码引用** —— Ghidra 权威引用 + 码区字面量双重确认; 指向本区的"引用"全是
  卡图数据区 (0x09xxxxxx) 里巧合等于 0x080108xx 的字节, 被 Ghidra 误判为指针。
  → 由间接/计算寻址或 RAM 指针加载, 静态分析无法定位消费者。
- **调色板未知** → 用 16 级灰度预览 (index0 视作透明)。
- 要正确上色 + 确定加载画面, 需 **mGBA 动态追踪** (asset-location.md §二): 跑到语言选择
  之后的画面 → dump VRAM/PALRAM → 与本区字节匹配 → 定位加载函数 + 调色板。

## 段结构 (内容粗分类, 0x100 粒度, 近似)

| 段 | 地址 | 类型 | 量 |
|---|---|---|---|
| 1 | 0x0800DE30 | tile (4bpp) | 280 tiles (含窗口框盒 + 渐变条) |
| 2 | 0x08010130 | tilemap (4B) | 256 entries (5 列网格屏幕) |
| 3 | 0x08010530 | tile | 72 tiles |
| 4 | 0x08010E30 | tilemap | 448 entries |
| 5 | 0x08011530 | tile | 255 tiles (★ + 选择框 + 渐变条) |

tilemap entry 格式同 lang-select: `A=(Y<<8)|X`, `B`=GBA BG tilemap 项 (tile&0x3ff + hflip/vflip)。
map 预览暂用相邻 tile 段当 tile bank (真实 bank 待 mGBA 确认)。

## 文件

| 文件 | 内容 | 入库 |
|---|---|---|
| `tools/rom-export/export_boot_ui_gfx.py` | 提取+灰度渲染 (接入 export_all.py) | ✓ |
| `data/boot-ui-gfx.s` | 顺序 `.incbin` (asm 经 SKIP_REGION `.include`) | ✗ (生成) |
| `graphics/bin/boot-ui/tiles/seg_<addr>.bin` | tile 段原始字节 | ✗ (生成) |
| `graphics/bin/boot-ui/tilemaps/seg_<addr>.bin` | tilemap 段原始字节 | ✗ (生成) |
| `graphics/images/boot-ui/{tiles,map}_<addr>.png` | 灰度预览 | ✗ (生成) |

byte-identical: `data/boot-ui-gfx.s` 顺序 incbin 5 段 = 原 ROM 0xDE30..0x13510; SKIP_REGION 改 `.include`。
段边界近似不影响 byte-identical (顺序 incbin)。验证 SHA1 9689337d。
