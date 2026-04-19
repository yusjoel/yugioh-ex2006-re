# 内嵌文件系统导出 + OCG/TCG 变体机制调查

**日期**：2026-04-19  
**范围**：`roms/2343.gba` ROM 0x01E64684..0x01ED49D4（FS 数据区，0x70350 = 459,600 B）  
**产物**：`tools/rom-export/export_fs_files.py`、`data/fs-payload.s`、`fs/<orig path>/*`

---

## 一、FS 布局核实

- 索引表：`data/fs-tables.s` @ ROM `0x01E63BE8`
  - `offset_table`：339 × u32（FID 相对 FS_BASE 偏移）
  - `size_table`：340 × u32（最后一条 `0xD0` 未用 / 占位）
- 路径表：`data/file-paths.s` @ ROM `0x01E6118C..0x01E63BE8`（339 条 null 终止 ASCII）
- FS 数据区：`0x01E64684..0x01ED49D4`（0x70350 B）

### 关键发现

- **FID 0 是 FS 根 meta**：`off=0x00000, sz=0x70350`（覆盖整片 FS）
- **FID 1..338 tight-pack 0x70350 B**，无 gap 无 overlap
- 按扩展名分布：`.ydc` 214 + `.ydq` 35 + `.LZ5bg` 26 + `.LZnclr` 18 + `.LZncgr` 17 + `.LZnanr` 14 + `.LZncer` 14 = **338**（严丝合缝）

FID 0 在导出时跳过（避免与 FID 1..338 的 bytes 重复）；fs-payload.s 仅 .incbin FID 1..338 按顺序，总 0x70350 B，与 ROM 原始区一致。

---

## 二、重名（duplicate path）现象

FID 1..338 中有 **98 条路径出现 >1 次**，共 **198 个 FID**。

- 全部 98 组的 dup FIDs bytes **都不同**（0 组 bytes 完全相同）
- 所以 dup 不是冗余副本，而是真正独立的两份文件

### 重名样例

| 路径 | FID | FS 偏移 | 大小 | 前 8 B |
|---|---|---|---|---|
| `deck/LV1_pikeru.ydc` | 2 | `0x000060` | 96 B | `01 cc cc cc 7f 21 77 41` |
| `deck/LV1_pikeru.ydc` | 3 | `0x0000C0` | 96 B | `01 fc 12 00 4f 57 44 3f` |

96 字节里 **78 字节不同**，header 字节 `0x01` 相同但 body 差异极大——两个独立 .ydc。

---

## 三、OCG/TCG 变体推断

### 证据 1：FID 分布严格 (偶, 奇) 相邻

98 组 dup 中 **96 组** 是相邻 FID 对 `(N, N+1)`，且较小 FID 总是偶数：

| dup 组 | FID | parity |
|---|---|---|
| deck/LV1_pikeru.ydc | [2, 3] | [偶, 奇] |
| deck/LV1_sukego.ydc | [4, 5] | [偶, 奇] |
| deck/LV1_waito.ydc | [6, 7] | [偶, 奇] |
| … | … | … |

剩下 2 组是 3-way（非 2-way flag 模型）：
- `demo/exodia/exodia02_obj.LZncgr` FID [226, 227, 228]
- `demo/exodia/exodia02_obj.LZnclr` FID [229, 230, 231]

这 2 组可能是 3 语言版本（OCG/TCG/EU 或类似）。

### 证据 2：与卡图查表机制同构

`FUN_080c33bc`（card-list-images 小卡图 tile 加载）用的查表公式：

```
tile_block = u16[INDEX_TABLE + (card_id*2 + flag)*2]
```

其中 `flag` 来自 ROM header 区域字节 `0x080000AE`：
- `0x4A`（'J'）→ JP/OCG → `flag = 0`
- 其他 → TCG → `flag = 1`

本作 BY6E 是非日版 → `flag = 1`。

FS 的 dup 分布完美匹配相同模式：若抽象索引 `base_idx = (fid - FIRST_DUP_FID) / 2`，则
`fid = FIRST_DUP_FID + base_idx*2 + flag`，OCG/TCG 选一。

### 证据 3（弱）：asm/all.s 静态 literal 搜索

- `0x080000ae` 在 all.s 有 76 处引用（含 card-list-images 已知 loader + 若干其他）
- 但 FS 三个表 CPU 地址 `0x09E64684` / `0x09E63BE8` / `0x09E6118C` **均未作为 `.word` 字面量出现**
- 推断 FS 表基址是运行时计算（可能 `FS_BASE - sizeof(tables)` 或经全局指针间接访问）

直接硬证需追 `.ydc` 加载器（后续可做），但数据层已足够强。

---

## 四、导出策略：`_dup{N}` 后缀消歧

由于 dup 两侧 bytes 不同，不能去重，必须两份都写到 `fs/`：

- 第 1 次出现：`fs/<orig path>`（如 `fs/deck/LV1_pikeru.ydc`）
- 第 N 次出现（N≥2）：basename 追加 `_dup{N-1}`（如 `fs/deck/LV1_pikeru_dup1.ydc`）

`data/fs-payload.s` 按 FID 1..338 顺序 .incbin 这 338 个文件，byte-identical 构建 ✓。

---

## 五、asm/rom.s 重构

旧版（4 段）：

```
.incbin "roms/2343.gba", 0x1E64684, 0xA      @ .ydc 文件头
.include "data/opponent-decks.s"              @ 25 个对手卡组（结构化）
.incbin "roms/2343.gba", 0x1E65A46, 0x53692  @ FS 中段 raw
.include "data/duel-puzzles.s"                @ 35 个决斗题目（结构化）
.incbin "roms/2343.gba", 0x1EC33D9, 0x13CC27 @ FS 尾 + 尾段 raw
```

新版（单 include）：

```
.include "data/fs-payload.s"                  @ 338 文件 tight-pack
.incbin "roms/2343.gba", 0x1ED49D4, 0x12B62C @ 仅 FS 后尾段（不再混 FS 数据）
```

- `data/opponent-decks.s` / `data/duel-puzzles.s` 从 build 管线剔除（`export_all.py` 同步），
  脚本本身保留用于 ad-hoc 决卡器分析
- `.gitignore` 新增 `fs/`（可从 ROM 完全重建）

### 覆盖率变化

| | 已分析 | 未分析 |
|---|---|---|
| 改前 | 17,835,893 B（62.49%） | 10,707,539 B（37.51%） |
| **改后** | **18,248,716 B（63.93%）** | **10,294,716 B（36.07%）** |
| 净增 | +412,823 B（+1.44%） | — |

---

## 六、后续

- **追 `.ydc` 加载器**：找到实际使用 flag 选 OCG/TCG 的函数，直接证实区域字节控制
- **NNS 资源**：`.LZnclr` / `.LZncgr` / `.LZnanr` / `.LZncer` 63 个（+ 3 组 3-way dup）待做正式 NNS 解析器（`doc/temp/nns_out/` 有临时产物）
- **`.LZ5bg` 压缩格式**：26 个文件格式未逆（Konami 私有 BG 压缩）
- **3-way dup**：`exodia02_obj.LZn{cgr,clr}` 3 路来源待查（可能语言选择不止 2 档）
