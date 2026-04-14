# 卡牌列表小图（OBJ sprite）调查报告

**完成日期**：2026-04-15（P2-1..P2-5 静态路径，mGBA 动态路径未用）  
**分析对象**：卡组构筑界面的小卡图缩略图区  
**工具**：`asm/all.s`（Ghidra 静态反汇编）+ Python ROM 扫描

---

## 结论（速查）

| 项目 | 值 |
|------|-----|
| tile 基址 | **`0x01326280`** |
| stride | **1152 B**（`9 × 128`） |
| 格式 | **8bpp tiles**（64 B/tile） |
| tile 布局 | **3×6 row-major** = 24×48 像素（portrait 缩略图） |
| tile_block 数 | **2331**（与大卡图共用） |
| 索引表 | `0x015B5C00`（与大卡图共用） |
| 索引公式 | `tile_block = u16[0x015B5C00 + (card_id*2+flag)*2]` |
| VRAM 目标 | OBJ char base `0x06010000` |
| 加载函数 | `FUN_080c33bc` @ `asm/all.s` L231102 |
| 导出脚本 | `tools/rom-export/export_card_list_images.py` |

## 旧文档 `card-data-structure.md` §三 的错误

旧版本结论基于"区间 `0x01000000..0x01463480`（4.4 MB）/ stride 2240 ≈ 2054"
的表面对齐推测，实际 6 项全错：

| 字段 | 旧 | 实际 |
|------|------|------|
| tile 基址 | `0x01000000` | **`0x01326280`** |
| tile 结束 | `0x01463480` | `~0x015B5400` |
| stride | 2240 | **1152** |
| tile 布局 | 5×7（列优先） | **3×6 行优先** |
| 像素尺寸 | 40×56 | **24×48** |
| tile_block 数 | 2054 | **2331** |

`0x01000000..0x01326280`（3.3 MB）是**其他资产**（疑为字体/UI tile/
主菜单图形等），不是小卡图。

## 调查路径

### 1. 尝试（失败）：mGBA 动态抓 VRAM

mGBA MCP bridge 两次启动均无法初始化（heartbeat 始终 null，read_memory/
screenshot 均超时）。切换至纯静态分析。

### 2. 扫描 `0x01000000` 区字节分布

`tools/ad-hoc/scan_card_list_images.py` 按旧假设 stride 2240 扫描 2054 条目：

- 前半（idx 0..~1500）**无零字节**（nzratio=1.0）、熵 ~4–5
- 后半（idx ≥1500）才有典型 0x00 高频（38%+）和低熵（~3.0）

这种"密度突变"与"8bpp 稀疏 tile"的直觉完全矛盾。
**结论**：旧文档假设的 stride/base 有错。

### 3. 在 `asm/all.s` 搜索 `0x09[0-4]xxxxx` 字面量

目标：找指向 `[0x09000000, 0x09500000)` 的常量。

关键命中：

```
asm/all.s L221746:    .word  0x09326280
asm/all.s L231152:    .word  0x093264c0   (= 0x09326280 + 0x240)
asm/all.s L231191:    .word  0x09326280
asm/all.s L231460:    .word  0x09326280
asm/all.s L323826:    .word  0x09326280
asm/all.s L334286:    .word  0x09326280
asm/all.s L334353:    .word  0x09326280
```

### 4. 分析加载函数 FUN_080c33bc（L231102）

完整字面量池：

| 符号 | 值 | 含义 |
|------|-----|------|
| `DAT_080c3408` | `0x095B5C00` | 索引表（与大卡图共用） |
| `DAT_080c340c` | `0x080000AE` | ROM 头部版本字节 |
| `DAT_080c3410` | `0x02000000` | EWRAM 基址 |
| `DAT_080c3414` | `0x00006C2C` | EWRAM 偏移（flag 字节） |
| **`DAT_080c3418`** | **`0x093264C0`** | tile 基址（第二 slot，`+0x240`） |
| `DAT_080c3450` | `0x095B5C00` | 索引表（第二路径） |
| **`DAT_080c3460`** | **`0x09326280`** | tile 基址（第一 slot） |
| `DAT_080c34F8` | `0x0984FBCC` | 默认/dummy tile 源 |
| **`DAT_080c34FC`** | **`0x06010000`** | **OBJ VRAM char base**（关键！） |

关键指令序列（L231137–L231141，tile_block × 1152 计算）：

```asm
ldrh r2, [r0, #0x0]    @ r2 = tile_block (u16 from index table)
lsls r1, r2, #0x3      @ r1 = tb << 3
adds r1, r1, r2        @ r1 = tb * 9
lsls r1, r1, #0x7      @ r1 = tb * 9 * 128 = tb * 1152
ldr  r0, DAT_080c3418  @ r0 = 0x093264c0 (或 0x09326280)
adds r1, r1, r0        @ r1 = base + tb * 1152
```

`lsls r1, r1, #0x7`（左移 7 位 = ×128）是这个 stride 的关键，与大卡图的
`r1 × 75 × 64 = 4800`（P1 findings §3.3）是**不同的 stride 编码**。

**上半 + 下半双基址布局**：`0x09326280` 与 `0x093264C0` 差 `0x240 = 576 B`。
每个 tile_block 占 1152 B，被视为两个 576 B（= 9 个 64 B tile）半块：
- 上半 9 tile：`0x01326280 + tb × 1152 + [0..576)`
- 下半 9 tile：`0x01326280 + tb × 1152 + [576..1152)`

合起来 18 tile = 3×6 grid = 24×48 像素。

### 5. 渲染验证

`tools/ad-hoc/render_card_list_entry.py` 试多种布局（3×6 / 6×3 / 2×9 / 9×2，
row-major / column-major）渲染灰度 PNG：

- **3×6 row-major** 明显呈卡片轮廓（portrait），上下有 1 tile 高的边框区
- 其他布局均为条纹或错乱图形

Blue-Eyes（tile_block=1）与 DESPAIR（tile_block=1476）灰度渲染可辨识为
白龙/暗属恶魔形象。

### 6. 索引 `card_id ↔ tile_block` 验证

索引表与大卡图完全共用。从 P1 findings 已知：
- card_id 1 = Blue-Eyes → tile_block 1
- card_id 1323 = DESPAIR → tile_block 1476

`tools/rom-export/export_card_list_images.py` 通过 `iter_card_ids()` 枚举
2331 个 card_id 对应的 tile_block，批量导出唯一的 2108 张灰度 PNG（部分
tile_block 被多个 card_id 共享，重复跳过）。

## 未解决：调色板（palette）

OBJ 8bpp 需 256 色调色板写入 `0x05000200..0x05000400`（512 B）。
源 ROM 地址尚未定位。

**候选方向**（下次 session 推进）：

1. **`[0x01000000, 0x01326280)` 区内嵌** — 3.3 MB 未知区可能含 palette 表
2. **共享大卡图 palette** `0x084C76C0` — 但大卡图是 64 色 per-card，
   小卡图要 256 色，不直接通用；可能有独立全局 palette
3. **调用栈追踪** — 找 `FUN_080c33bc` 的调用者，它通常在调用前初始化 OBJ
   palette。候选调用点：
   - `asm/all.s` L221657 / L221672 / L229309 / L232503 / L232520 / L232778
     / L233667 / L233676 / L254477 / L254486
4. **mGBA 动态 dump `0x05000200..0x05000400`**（卡组构筑界面）

定位后：`export_card_list_images.py --palette <bin>` 即可彩色输出。

## 相关文件

| 文件 | 说明 |
|------|------|
| `asm/all.s` L231102 | `FUN_080c33bc` 完整反汇编 |
| `tools/rom-export/export_card_list_images.py` | 批量导出脚本（灰度 + 可选 palette） |
| `tools/ad-hoc/scan_card_list_images.py` | 字节分布扫描（揭示旧假设错误） |
| `tools/ad-hoc/dump_card_list_entry.py` | 单条目字节转储 |
| `tools/ad-hoc/render_card_list_entry.py` | 多布局渲染测试 |
| `doc/dev/p1-phase-b2-findings.md` | 大卡图分析（方法论参照） |
| `doc/dev/card-data-structure.md` §三 | 精简落地结论 |
