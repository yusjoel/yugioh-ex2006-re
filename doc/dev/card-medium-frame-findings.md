# card-medium-frame（32×48 卡 sprite）探索报告

**日期**：2026-04-19  
**方法论**：`doc/dev/static-data-region-methodology.md` 四阶段流程  
**目标区间**：ROM `0x00FBC080..0x01326280`（3,580,416 B = 3.58 MB）

---

## 结论（速查）

| 项目 | 值 |
|---|---|
| 基址 | `0x00FBC080`（CPU `0x08FBC080`） |
| stride | **1536 B** = 24 tile × 64 B |
| 格式 | 8bpp，**4×6 tile 行主 = 32×48 像素** |
| tile_block 数 | 2331（0..2330，与 card-mini-frame 共享） |
| 索引表 | `0x015B5C00`（与 card-mini-frame 共用） |
| 索引公式 | `tile_block = u16[0x015B5C00 + (card_id*2 + flag)*2]`，flag 同 OCG/TCG |
| 加载函数 | `FUN_080c2d24` @ `asm/all.s` L230236 |
| VRAM 目标 | OBJ `0x06010000`（主路径）+ BG `0x06006340` / `0x06008020`（多屏使用） |
| 命名根据 | 与 `card-mini-frame`（24×48, 1152 B）对位，"medium" 反映更大尺寸 |

---

## 方法论实录

### 阶段 1：静态特征扫描

脚本：`tools/ad-hoc/scan_region_3mb.py`

输出（3.58 MB，窗 512 B 步 512 B）：

| 扫描 | 结果 | 解读 |
|---|---|---|
| 长零块 ≥ 64B | **0 段** | 密集数据，无 padding gap |
| LZ77 `10` magic | 70k 噪声命中 | 纯 false positive（任何 0x10 字节都中） |
| Huffman `20` magic | 7k 噪声 | 同上 |
| NNS 签名 | **0** | 非 Nintendo g2d 资源 |
| ASCII `aaaaaa` / `666666` | 高频 | 实为 8bpp tile 中的纯色像素索引 0x61 / 0x36 |
| 滑窗熵 | **89% 落在 3-5 区间** | 典型"表/代码/索引"分布，**不是**压缩数据 |

top5 字节：`0x80, 0x8D, 0x61, 0x1B, 0x21` — 与 `card-mini-frame` top5 `0x00, 0x80, 0x8D, 0x1B, 0x36` **高度重合**，线索指向同家族 8bpp tile。

### 阶段 2：asm/all.s 静态 XREF

穷举 `.word 0x090FC000..0x09326280` literal：

- **命中 5 个**，全部是 u16 排序表的噪声（bytes 0x09 xx 0x09 xx 看起来像 0x09XXXXXX 指针）
- 真指针 **0 个**

扩展到 `0x08F00000..0x09010000`：

- **`0x08FBC080` × 3 次真命中** @ L230291（`FUN_080c2d24`）/ L245406 / L271018

前 3 处是 literal pool，`FUN_080c2d24` 反汇编完全解锁了数据结构。

### 阶段 2.5：反汇编 `FUN_080c2d24` 结构分析

```
FUN_080c2d24(card_id [u16], oam_slot [u16]):
    ldr  r6, =0x095B5C00    ; INDEX_TABLE
    lsls r2, r3, #0x1       ; r2 = card_id * 2
    ldr  r0, =0x080000AE    ; region byte
    ldrh r0, [r0]
    lsrs r0, r0, #0x8       ; 取高字节
    cmp  r0, #0x4A          ; 'J' ?
    ...                      ; 日版走 flag=0 分支（含 EWRAM 0x02006C2C 位 7 检查）
    ...                      ; 非日版走 flag=1
    orrs r2, r4             ; r2 = card_id*2 | flag
    lsls r0, r2, #0x1
    adds r0, r6, r0         ; 索引表字节偏移
    ldrh r2, [r0]           ; tile_block = u16[INDEX_TABLE + (card_id*2+flag)*2]
    lsls r1, r2, #0x1
    adds r1, r1, r2         ; r1 = tb * 3
    lsls r1, r1, #0x9       ; r1 = tb * 3 * 512 = tb * 1536  ← STRIDE
    ldr  r0, =0x08FBC080    ; TILE_BASE
    adds r4, r1, r0         ; tile_ptr = base + tb * 1536
    lsls r0, r5, #0x5       ; r0 = oam_slot * 32
    ldr  r1, =0x06010000    ; OBJ VRAM
    adds r5, r0, r1         ; vram_dst
    ; ... 复制 24 tile 到 OBJ
```

**stride 1536 B = `tb * 3 * 512`** 是解锁关键（对比 `card-mini-frame` stride 1152 = `tb * 9 * 128`）。

### 阶段 3：渲染验证

测试：`0xFBC080` 起 stride 1536，4×6 tile 行主，用 card-mini-frame BG 调色板
（ROM `0x00510460`）。

渲染 4×4 = 16 张卡：**全部清晰可辨认**（黄框 + 彩色卡图），byte-identical 重建通过。

### 阶段 4：拆分落地

| 产物 | 路径 |
|---|---|
| 导出脚本 | `tools/rom-export/export_card_medium_frame.py` |
| 结构化汇编 | `data/card-medium-frame.s`（label + 2331 条 `.incbin`） |
| tile bin | `graphics/bin/card-medium-frame/tiles/tb{0000..2330}.bin` |
| PNG 预览 | `graphics/images/card-medium-frame/card_{0000..2097}[_ocg|_tcg].png` |
| asm/rom.s | 单一 `.include "data/card-medium-frame.s"` 替换原 2 段 raw |
| 导出管线 | `export_all.py` 加入 `export_card_medium_frame.py` |

Byte-identical 验证通过（SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`）。

---

## 与同族数据的对照

| 名称 | ROM 基址 | stride | 格式 | 像素 | 加载函数 | 主用途（推断） |
|---|---|---|---|---|---|---|
| card-image-tiles | `0x510640` | 4800 B | 6bpp | ~40×56 | （未单独命名） | 卡信息页全尺寸大图 |
| **card-medium-frame** | `0x0FBC080` | **1536 B** | **8bpp** | **32×48** | `FUN_080c2d24` | 对战场 OBJ + BG 中等 sprite |
| card-mini-frame | `0x1326280` | 1152 B | 8bpp | 24×48 | `FUN_080c33bc` | 卡组构筑界面小缩略 (24×24×2) |

三种数据**共享同一索引表** `0x015B5C00`，同一 OCG/TCG flag 机制。

---

## 覆盖率影响

| | 已分析 | 未分析 |
|---|---|---|
| 改前 | 18,248,716 B（63.93%） | 10,294,716 B（36.07%） |
| **改后** | **21,829,132 B（76.48%）** | **6,714,300 B（23.52%）** |
| 净增 | **+3,580,416 B（+12.55%）** | — |

**单此一次探索直接 +12.55% 覆盖率**，是目前单次最大拆分收益。

---

## 未确认事项

- **精确用途**：推断对战场 sprite，但具体哪个屏幕/帧使用尚未 runtime 验证
- **调色板**：渲染用 card-mini-frame 的 BG 调色板得到合理结果，但该 sprite 在 OBJ 路径下可能用另一套
  （L245408 目标为 BG 0x06006340，L231102 mini-frame 目标为 OBJ 0x06010000 用 OBJ 调色板）。
  若 PNG 预览与游戏实际色差大，需另找 OBJ 调色板源。
- **FUN_080cb7xx / FUN_080db910 调用链**：命名待定，阶段 3 动态分析跟进
