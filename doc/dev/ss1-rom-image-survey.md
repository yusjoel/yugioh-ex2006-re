# ss1 画面 ROM 图像资产遍历调研

**存档**：`roms/2343.ss1`
**画面**：卡组构建列表（ZOMBIE MADNESS），按 A → 进 Master Kyonshee 详情页
**时间**：2026-04-22

## 一、方法

对 `ss1` 三个 VRAM 快照（s0 列表视图、s1 列表下拉态、s3 Master Kyonshee 详情页），
每 32 B 取为 "tile" 样本，在 ROM (stride-4) 里做 exact byte 匹配；
结果与 `data-analysis-coverage.md` 的 17 个未分析段求交，产出 "VRAM 当前在用 / ROM 存储在未知段" 的 tile 簇。

### 关键假设
- GBA 背景/精灵 tile 存储为 4bpp（32 B/tile）或 8bpp（64 B/tile）；
  stride-4 搜索 32 B 段既命中 4bpp tile 原生，也能命中 8bpp tile 的任意 32 B 子块。
- 过滤"平凡 tile"（单字节重复、双字节 ≤2 次翻转）避免实心填充误报。

### 代码
| 脚本 | 作用 |
|------|------|
| `tools/ad-hoc/ss1_decode_io.py` | 解析 IO (DISPCNT/BGCNT/OAM) 识别活 charblock 和色深 |
| `tools/ad-hoc/ss1_tile_to_rom.py` | stride-32 粗扫（误漏 4 字节偏移的 tile sheet） |
| `tools/ad-hoc/ss1_scan_unknown_segs.py` | 在未知段内 stride-32 对齐扫描 |
| `tools/ad-hoc/ss1_strict_search.py` | VRAM tile × 全 ROM stride-1 穷举搜索 |
| `tools/ad-hoc/ss1_scan_v2.py` | **stride-4 扫描未知段，连续 +32 run 聚类**（主结果） |
| `tools/ad-hoc/ss1_render_clusters.py` | 4bpp 渲染簇预览（每 palette bank 一张） |
| `tools/ad-hoc/ss1_render_v2.py` | 同上，针对 v2 识别的 runs |
| `tools/ad-hoc/ss1_render_8bpp.py` | 8bpp 渲染大 runs（BG2 使用） |

## 二、VRAM 状态概要

| 状态 | 场景 | DISPCNT | 活 BG | OBJ palbank |
|---|---|---|---|---|
| s0 | 卡列表（初态） | mode 0, OBJ2D | BG0/2/3 | 0,8,9,10 |
| s1 | 卡列表（下滚后） | 同 s0 | 同 | 同 |
| s3 | Master Kyonshee 详情页 | mode 0, OBJ1D | BG0/1/2/3 | 12,13,15 |

- **s0/s1 BG0 & BG3** 4bpp @ cb2（0x06008000）
- **s0/s1 BG2** 8bpp @ cb0（0x06000000，高索引扩展到 cb1 = 0x06004000-0x06007FFF）
- **s3 所有 BG** 共享 cb1（BG0 8bpp，BG1/2/3 4bpp）

## 三、发现：未知段内含真实 tile 数据

**合计 26,976 B** 非压缩 tile 数据落在 2 个未知段：

### 段 `0x01832602` / 0x1E51A（124,186 B，seg-C 前段）

| ROM 起止 | tile 数 | 字节 | VRAM 首引用 | 备注 |
|---|---:|---:|---|---|
| `0x0184A42C-0x0184B72C` | 152 | 4,864 | `s0@0x5940` | BG2 8bpp 数据块（= 76 × 64B tile） |
| `0x0184B9C4-0x0184C604` | 98 | 3,136 | `s0@0x5940` | 同上变体 / 相关数据（= 49 × 64B） |
| `0x0184C764-0x0184C7A4` | 2 | 64 | `s0@0x66e0` | 小附件 |
| `0x0184C924-0x0184C964` | 2 | 64 | `s0@0x68a0` | 小附件 |
| `0x0184CAE4-0x0184CCC4` | 15 | 480 | `s0@0x6a60` | 中等尺寸图元 |
| `0x0184DAEC-0x0184DB6C` | 4 | 128 | `s3@0x17440` | OBJ（详情页 sprite） |
| `0x0184E4AC-0x0184E52C` | 4 | 128 | `s3@0x17500` | OBJ（详情页 sprite） |

总覆盖：**0x0184A42C..0x0184E52C ≈ 16,640 B** 里 **≈8,864 B** 是真实 tile（其余 gap 可能为调色板/索引/padding）。
这段紧邻 **已分析的 duel-field HUD 块** （`0x01850B1C`），属于 ROM 布局里的 "HUD / 卡列表共享资产区" 前段。

### 段 `0x01DFF9D2` / 0x31B82（203,650 B，游戏文本后 / 卡列表调色板前）

极其密集的 runs，跨度 `0x01E1C294..0x01E2FD94` ≈ **83 KB**。汇总代表性 runs：

| ROM 起止 | tile 数 | VRAM 首引用 | 估计角色 |
|---|---:|---|---|
| `0x01E1C294-0x01E1C794` 多段 | 46+ | `s0@0x8040..0x8200` | 卡列表 BG 小图元 |
| `0x01E1CCB4-0x01E1D7F4` | 76 | `s0@0x83C0..0x8DE0` | **列表行背景 / 属性贴片**（BG0/3 4bpp cb2） |
| `0x01E1DF34-0x01E1E2D4` | 29 | `s0@0x8DE0` | 同行族重复变体 |
| `0x01E246D4-0x01E25554` | **116** | `s0@0xC3A0` | **最大 BG 资源块**（3,712 B） |
| `0x01E25554-0x01E260F4` | 25 | `s0@0x17280..0x17FC0` | OBJ（HUD 顶部工具栏 sprite） |
| `0x01E271B4-0x01E2D6B4` | 多 × 8 | `s0@0x10000..0x10B80` | **OBJ 精灵**（4-16 tile/run，顶部 HUD 图标簇） |
| `0x01E2DDB4-0x01E2DEB4` | 8 | `s0@0x10B80` | OBJ |
| `0x01E2FD34-0x01E2FD94` | 3 | `s0@0x17600` | OBJ |

**观察**：该段 OBJ 引用集中在 VRAM `0x10000..0x10B80`（= sprite tile 0..92），正是 s0 列表视图**顶部 HUD 工具栏**的 sprite 区域（截图里的 yellow cart / lock / brush / magnify / attribute filter 等彩色图标按钮）。

## 四、为什么 stride-32 漏掉

原 `ss1_scan_unknown_segs.py` 从未知段起点按 32-对齐搜索。`0x0184A42C % 32 = 12`、
`0x01E1C294 % 32 = 20` —— 这些 tile sheet 起点非 32 对齐（但 4 对齐），
说明 ROM 打包时一些 tile sheet 前面紧跟了非 32B 结构（如 header / palette / NCER 偏移），
把 tile 数据推到非对齐位置。**stride-4 扫描是正确做法**。

## 五、保密性 / 正负结论

### 正结论
- **seg-C 前段 + seg `0x01DFF9D2`** 两个未知段**确实含大量未压缩 tile 数据**，非平凡、总计 ~27 KB。
- 这些 tile 被 **s0/s1 卡列表视图** 和 **s3 详情页** 直接使用（非解压产物，直接从 ROM 复制到 VRAM）。
- 段 `0x01DFF9D2` 的 OBJ 部分对应 **顶部 HUD 工具栏按钮**（filter/sort/search 等，每按钮 4-16 tile）。
- 段 `0x01DFF9D2` 的 BG 部分对应 **卡列表行背景 / 属性贴片**（4bpp 小图元，BG0/3）。

### 负结论
- **详情页 (s3) VRAM 几乎全是 LZ77 解压产物** —— 919 个非空 tile 只有 2 个 run（小）匹配 ROM。大卡图 + medium frame 是从 FS `.LZncgr` 解压而来。
- **其余 15 个未知段** 本次覆盖画面内**没有** VRAM 引用：
  - `0x004C7638`、`0x01865E20`、`0x01867560`、`0x0188F8D0` 等
  - 要么不是图像数据，要么是其他画面（决斗中 / 商店 / 卡包 / 开局菜单）的专属资源
  - 需其他 ss 快照覆盖（商店 / 决斗 / 对手选择 / 预组详情 等场景）继续遍历

## 六、VRAM→ROM 映射 CSV

- 全量 stride-32 原始结果：`doc/temp/ss1_tile_hits.csv`
- stride-4 真实 runs：`doc/temp/ss1_unknown_v2.txt`
- 快照产物：`doc/temp/ss1_s{0,1,3}_{vram,palram,io,oam}.bin`
- 截图：`doc/temp/ss1_state0.png`（列表）、`ss1_after_AA.png`（详情页）

## 七、预览渲染

- `doc/temp/ui_cluster_previews/` —— 第一轮（大多为误报的实心填充）
- `doc/temp/ui_runs_preview/` —— **真实 runs 多调色板预览**
  - BG 4bpp runs：各 pb 猜测，`pb0/1/2/8/9/10/15`
  - BG 8bpp runs：`*_bg_8bpp.png`，用完整 256 色板
  - OBJ runs：同上

*注*：由于 BG2 在列表视图为 **8bpp 模式且引用 ~256-511 号 tile 索引**，仅靠单独 tile 预览无法恢复屏上完整图形——需要联同 tilemap (`sb30 @ 0xF000`) 按序排列才能看到正确样貌。

## 七-A、已确认识别：HUD 数字+图标 sheet

**ROM `0x01E246D4` + 3,712 B（116 × 32B，4bpp）**，落在未知段 `0x01DFF9D2`。

以 s0 BG palette bank 2 渲染，视觉内容清晰：

- 顶部：小图标合集（属性/种族/开关/锁/刷子/魔法符号 等，约 12-15 个）
- 红色 `0-12` 数字（含双位）
- 橙色 `0-12` 数字
- 蓝色 `0-12` 数字 + `? /` 符号
- 紫色 `0-12` 数字 + `? /` 符号
- 大字号蓝色 `12345` + 向上箭头、星号、子弹、播放三角、红/绿方块

**用途猜测**：卡列表顶部状态栏 "已收集数 / 总数 / 等级" 数字 + 筛选/排序按钮图标。

**导出产物**：
- `graphics/bin/ui-misc/hud_digits_icons_sheet.bin` (3,712 B raw 4bpp tiles)
- `graphics/images/ui-misc/hud_digits_icons_sheet.png` (放大 4 倍预览)
- 导出脚本 `tools/ad-hoc/ss1_export_hud_sheet.py`

> ⚠ 暂未写入 `asm/rom.s`（需先鉴别相邻结构/调色板/索引表完整边界再做 byte-identical 替换）。

## 八、后续建议

1. **提取 tilemap**：从 `ss1_s0_vram.bin` 读 sb28/sb30/sb31 (`0xE000/0xF000/0xF800`)，
   逐行解析 (tile_idx, palbank, flip) 对，把 VRAM tile 按屏上位置排回原图。
2. **导出 bin**：把 `0x0184A42C-0x0184C604` 和 `0x01E1C294-0x01E2FD94` 两段打包为
   `graphics/bin/ui-misc/seg_c_prefix_tiles.bin` + `seg_text_tail_tiles.bin`，
   替换 `asm/rom.s` 里对应 `.incbin` 区块，验证 byte-identical。
3. **切换画面扫剩余未知段**：
   - 主菜单（可能触发 `0x004C7638`、FS 尾部 `0x01ED49D4` 的动画/徽标）
   - 商店 / 卡包选择（`0x01867560` 的 "内场调色板后，小图标图块前" 疑似卡包封面相关资产）
   - 决斗中 phase UI（`0x01B8FB8C` 大段 1.3 MB）
4. **OBJ HUD 图标单独导出**：`0x01E271B4-0x01E2D6B4` 是顶部工具栏图标合集，
   每按钮 256-512 B、边界清晰，适合先用 tilemap 切分导出（BG 工具栏若使用 sprite 则靠 OAM）。
