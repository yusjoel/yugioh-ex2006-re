# 内嵌文件系统导出 + OCG/TCG 变体机制调查

**日期**：2026-04-19  
**范围**：`roms/2343.gba` ROM 0x01E64684..0x01ED49D4（FS 数据区，0x70350 = 459,600 B）  
**产物**：`tools/rom-export/export_fs_files.py`、`data/fs-payload.s`、`fs/<orig path>/*`

---

## 一、FS 布局核实

- 索引表：`data/fs-tables.s` @ ROM `0x01E63BE8`
  - `offset_table`：339 × u32（FID 相对 FS_BASE 偏移）
  - `size_table`：**340 × u32**（最后一条 `0xD0 = 208` 是 FID 339 orphan 的大小，**不是占位**）
- 路径表：`data/file-paths.s` @ ROM `0x01E6118C..0x01E63BE8`（339 条 null 终止 ASCII）
- FS 数据区：**`0x01E64684..0x01ED4AA4`（0x70420 B = 459,808 B）**
  - 主区：0x01E64684..0x01ED49D4（0x70350 B）= FID 1..338
  - Orphan：0x01ED49D4..0x01ED4AA4（208 B）= FID 339 (title_obj_s.LZnclr)

### 关键发现（修订版）

- **映射**：`path[i] ↔ FID[i+1]`（`paths[0]` 对应 FID 1，以此类推）
- **FID 0** 是 FS 根 meta：`off=0x00000, sz=0x70350`（覆盖 FID 1..338 那段，无独立路径）
- **FID 1..338** tight-pack 0x70350 B 在 FS_MAIN 区
- **FID 339** orphan：`paths[338] = "titleEx/title_obj_s.LZnclr"`，数据在 szs[0] 声称的
  0x70350 B **之外**，紧跟 FID 338 后（ROM 0x01ED49D4+208 B）
- 按扩展名分布（含 FID 339）：`.ydc` 215 + `.ydq` 35 + `.LZ5bg` 26 + `.LZnclr` 18 +
  `.LZncgr` 17 + `.LZnanr` 14 + `.LZncer` 14 = **339**

### 历史 off-by-one bug（已修，commit 待定）

早期 `export_fs_files.py` 误用 `path[i] ↔ FID[i]`（shift=0），致 52/63 个 .LZn* 文件
的 fs/ 文件名与内容错位，且漏掉 FID 339 orphan palette（被当作 "FS 后尾段" 的起 208 B
打包进 `.incbin`）。修复后：
- fs/ 下 63/63 NNS 文件扩展名和内部 magic 严格对齐（RNAN/RECN/RGCN/RLCN）
- fs/puzzle/*.ydq 全 35 个以 `[DUEL QUESTION]\r\n` 开头
- fs/deck/*.ydc 全 215 个首字节 0x01
- fs/**/*.LZ5bg 全 26 个首字节 0x10（LZ77 magic）
- 新增 fs/titleEx/title_obj_s.LZnclr（208 B，FID 339）

fs-payload.s 由 338 条 `.incbin` 扩到 339 条，asm/rom.s 末尾 `.incbin` 起点从
`0x1ED49D4` 后移到 `0x1ED4AA4`，长度减 208 B；build byte-identical 保持。

---

## 二、重名（duplicate path）现象

FID 1..339 中有 **99 条路径出现 >1 次**（修正后统计），共 **200 个 FID**。

- 全部 99 组的 dup FIDs bytes **都不同**（除 exodia02 3-way 外）
- 所以 2-way dup 不是冗余副本，而是真正独立的两份文件

### 重名样例

| 路径 | FID | FS 偏移 | 大小 | 前 8 B |
|---|---|---|---|---|
| `deck/LV1_kuriboh.ydc` | 1 | `0x000000` | 96 B | `01 cc cc cc 7f 21 77 41` |
| `deck/LV1_kuriboh.ydc` | 2 | `0x000060` | 96 B | `01 fc 12 00 4f 57 44 3f` |

96 字节里 78 字节不同，header `0x01` 共享但 body 差异极大——两个独立 .ydc。

---

## 三、OCG/TCG 变体推断

### 证据 1：相邻 FID 对（修订）

99 组 dup 中 **97 组** 是相邻 FID 对 `(N, N+1)`。在 shift=+1 修正映射下：
- 41 组首 FID 为奇数（path 表开头段 `path[2k]=path[2k+1]` → FID `(2k+1, 2k+2)`）
- 56 组首 FID 为偶数（path 表中段后 dup 起点偏移）

| dup 组 | FID | 首 FID parity |
|---|---|---|
| deck/LV1_kuriboh.ydc | [1, 2] | 奇 |
| deck/LV1_pikeru.ydc  | [3, 4] | 奇 |
| deck/LV1_sukego.ydc  | [5, 6] | 奇 |
| … | … | … |
| （中段）deck/theme_NNN.ydc | [M, M+1] | 混合 |

早期版本（shift=0 误算）声称 "首 FID 严格为偶"，修正后实际是 **奇偶混合**——
dup 配对规律是 path 表上的 **连续两 slot 同串**，映射到 FID 后取决于 slot 索引奇偶。

剩 2 组 3-way（语义见第七节）：
- `demo/exodia/exodia02_obj.LZncgr` FID [227, 228, 229]（shift=+1 后）
- `demo/exodia/exodia02_obj.LZnclr` FID [230, 231, 232]（shift=+1 后）

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

### 证据 3：asm/all.s 代码级确认（任务 D1，2026-04-23）

`0x080000ae` 在 `asm/all.s` **恰好 24 处 `.word` 引用**（原 prompt 的 "76" 是高估）。14 处呈现标准 "区域判定 + OCG 子检查" 五步指令序列：

```asm
; --- 规范模板（见 FUN_0801c50c @ 0x0801c50c，FUN_080c33bc @ 0x080c33bc 等）---
  ldr   rN, DAT_ae          @ rN = 0x080000AE
  ldrh  rN, [rN, #0]        @ rN = *(u16*)0x080000AE  （BY6E → 0x4536）
  lsrs  rN, rN, #8          @ rN = 高字节 = rom[0xAF]（= 区域码 ASCII）
  cmp   rN, #0x4a           @ = 'J' ?
  bne   TCG_SET              @ ≠ 'J' → 直接判 TCG（flag=1）
  ; --- 仅 J ROM 到达此处，检查 IRAM 运行时切换 ---
  ldr   r1, DAT_02000000
  ldr   r0, DAT_00006c2c
  adds  r1, r1, r0          @ r1 = 0x02006c2c (IRAM)
  ldrb  r1, [r1, #0]
  movs  r0, #7
  ands  r0, r1              @ r0 = IRAM[0x02006c2c] & 7
  cmp   r0, #0              @ 低 3 bit 为 0 → 保持 OCG
  beq   OCG_KEEP
TCG_SET:
  movs  rR, #1              @ flag = 1 (TCG)
OCG_KEEP:
  ; flag 留 0 (OCG) 或 1 (TCG)
```

### 24 处引用分类

| 分类 | 数量 | 说明 |
|---|---|---|
| 规范 "J + IRAM" 两级判定 | 8 | 完整 OCG/TCG dual-gate，允许 J ROM 运行时切换到 TCG |
| 简化 "直接 J 判定" | 6 | 只读 0x080000AE，无 IRAM fallback（硬分支，常见于 startup） |
| ARM 模式 / 跨 pool 远引用 | 10 | 指令序列跨越 40+ 行，静态扫描未匹配（需 Ghidra 逐函数验） |

### BY6E 运行时行为（已确证）

- ROM[0x080000AC..0xAF] = `'B' 'Y' '6' 'E'` = 游戏代码 `BY6E`（北美 TCG 版）
- `u16 @ 0x080000AE` = `0x4536`，`lsrs #8` 得 `0x45 = 'E'`
- `cmp #0x4a` 失败 → **flag = 1 (TCG)**，无需 IRAM fallback
- IRAM 0x02006c2c & 7 仅在 J ROM 构建下被读取（开发期的区域切换后门），本作永不触发

### 代表性位置

| 地址 | 函数 | 用途（从上下文推断） |
|---|---|---|
| `0x080c33bc` | FUN_080c33bc | card-list-images 小卡图 tile 选 OCG/TCG 查表（已知） |
| `0x0801c50c` | FUN_0801c50c | 选 0x09e3d964 ROM 配置块的 OCG/TCG 变体（16 B × 2） |
| `0x080136xx`~ | FUN_08013680 | （ARM 模式）早期启动阶段区域判定 |

### FS 表定位问题（未决）

- FS 三表 CPU 地址 `0x09E6118C` / `0x09E63BE8` / `0x09E64684` **均未作为 `.word` 字面量出现**（已确认）
- 推断 FS 表基址是运行时算出（相对全局指针或 `FS_BASE - table_size` 反推）
- 这意味着 `.ydc` loader 的 OCG/TCG 分叉不能仅靠 literal 扫找到，需反编译追调用链（任务 B1）

---

## 四、导出策略：`_dup{N}` 后缀消歧

由于 dup 两侧 bytes 不同，不能去重，必须两份都写到 `fs/`：

- 第 1 次出现：`fs/<orig path>`（如 `fs/deck/LV1_pikeru.ydc`）
- 第 N 次出现（N≥2）：basename 追加 `_dup{N-1}`（如 `fs/deck/LV1_pikeru_dup1.ydc`）

`data/fs-payload.s` 按 FID 1..339 顺序 .incbin 这 339 个文件（含 orphan palette），
byte-identical 构建 ✓。

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

---

## 七、3-way dup 深度调查（任务 A4，2026-04-23）

### 对象

`demo/exodia/exodia02_obj` 系列，FS 中含两组三份：

| 路径 | FID | 绝对偏移 | 压缩大小 | 解压后大小 | 解压 SHA1 |
|---|---|---|---|---|---|
| `exodia02_obj.LZncgr` | 227 | 0x01E7FFCC | 13,324 B | 28,848 B | `b32c4fdb…` |
| `exodia02_obj.LZncgr` | 228 | 0x01E833D8 | 13,324 B | 28,848 B | `b32c4fdb…` |
| `exodia02_obj.LZncgr` | 229 | 0x01E867E4 | 13,324 B | 28,848 B | `b32c4fdb…` |
| `exodia02_obj.LZnclr` | 230 | 0x01E89BF0 | 124 B | 552 B | `a061862b…` |
| `exodia02_obj.LZnclr` | 231 | 0x01E89C6C | 124 B | 552 B | `a061862b…` |
| `exodia02_obj.LZnclr` | 232 | 0x01E89CE8 | 124 B | 552 B | `a061862b…` |

（FID 标号按 "path[i] ↔ FID[i+1]" 正确对齐。任务 #12 的 off-by-one bug 已于
 `export_fs_files.py` 修复；fs/ 下文件名与内容现已严格对齐。）

### 观察

1. **3 份在原始 LZ77 压缩流和解压后 NNS 内容两级都 byte-identical**（SHA1 完全一致）——不是 OCG/TCG/EU 三区域不同数据。
2. **仅 NCGR + NCLR 被三重化**，而同场景的 `.LZnanr` (FID 225) 与 `.LZncer` (FID 226) 都是单份。
3. **其他 demo 场景不存在 3-way dup**：`exodia00/01`、`shuen`、`vija`、`name_input`、`pass_input`、`titleEx` 都没有 `×3` 模式。路径表 `path[226..228]` 与 `path[229..231]` 是仅有的 2 组 "连续 3 次" 重复。
4. **asm/all.s 无 226-232 FID 数字字面量**（`mov rX, #NNN`、`#NNN` in .word 扫描均无命中）——loader 按间接索引/路径字符串查，无法从静态字面量证实访问顺序。

### 推断

排除的可能：

| 假说 | 排除理由 |
|---|---|
| OCG/TCG/EU 3 区域变体 | 3 份 bytes 相同，无法区分区域 |
| 3 关键帧的不同动画数据 | NANR/NCER 单份，动画层无 3 倍冗余 |
| 3 个不同 VRAM 槽的预加载 | NCGR/NCLR 解压结果完全一致，VRAM 载入只需一次 |

最可能（残留证据）：

- **开发流程遗留**：exodia02 在开发过程中经过多次资产迭代，pipeline 将每次"生成版本"都写入 FS（可能 `build_res.exe` 每迭代一次追加一份），最终未去重。
- **浪费**：2 份冗余 × (13,324 + 124) B = **26,896 B = 26.3 KB** 纯浪费。

这一推断与更大范围的 OCG/TCG 2-way dup（96 组，deck/LV*、theme_*.ydc 等）**不同**：2-way 的 dup bytes 在 98/98 组里都不相同，所以 2-way 是真实的区域分叉；3-way 全相同则是发布期 bug。

### 结论

`exodia02_obj` 3 份副本是**发布 ROM 中的重复资产 bug**，非功能性区分。字节无差异 → 无可挖掘的语义信息。任务 A4 结束。

---

## 八、后续

- **追 `.ydc` 加载器**（任务 B1 / D1）：证实 OCG/TCG 2-way dup 的 flag 访问
- **NNS 解析器**（任务 A2 + D3）：`fs-decompressed/` 已就绪
- **`.LZ5bg` 压缩格式**（任务 A3）：26 个，magic `0x10`（LZ77）外壳，内层 NNS magic `NTBG` 格式待逆
- **FS 对齐 bug**（任务 #12）：`export_fs_files.py` 的 `path[i] ↔ FID[i]` 应改为 `path[i] ↔ FID[i+1]`，并将 FID 339（orphan palette `title_obj_s.LZnclr` @ 0x1ED49D4+208B）纳入 FS
- **3-way dup**：已关闭，结论见第七节
