# 未结构化大块区勘查记录（2026-04-19）

沿用 `doc/dev/static-data-region-methodology.md` 阶段 1-2 勘查两个大块区，
确认**静态单轮不足以完整结构化**，需要后续专项（runtime 辅证 / 压缩逆向 / 分簇手工解析）。
本文档记录现有线索，避免下次重复扫描。

---

## 一、0x01896730..0x1B101AC（2.6 MB）— 多屏资源 bundle

### 扫描要点（阶段 1）
- 熵分布：中熵 53.9% / 低熵 26.5% / 稀疏 19.5%（**混合内容**）
- 区首 0x01896730 首 bytes `E0 83 00 00 23 10 84 18 ...` — BGR555 palette-like
- 无长零块，无 NNS 签名
- ASCII 高频 `'+++++' '666' 'aaa'` — 4bpp tile 的像素 pattern

### 静态 XREF（阶段 2）
- `asm/all.s` 范围 `0x09896730..0x09B101AC` 命中 **110 个真字面量**
- 聚成 **72 个独立簇**（相邻 <0x400 归一簇）
- 上半 1 MB（0x09897xxx..0x099xxxxx）簇密集，多 2-3 地址 / 簇
- 下半 1.6 MB 有规整 **64 KB bank 结构**：  
  连续 12 条指针 `0x09A31CA8 .. 0x09AE1CA8`（@ ROM 0x081CF038+，步长 0x10000）

### 数据特征抽样
- bank A3 首 4 KB 首 32B：`33 33 A4 18 22 32 A4 14 11 32 74 41 ...` — 典型 4bpp tile nibble-packed
- 用 icons palette 渲染 bank A3 出噪声，**palette 不对**，可能各 bank 自带 palette

### 结论
- **72 个资源簇**，每簇需独立逆向——单轮不现实
- 64 KB bank 区（0x1A30000..0x1AE0000, 11 banks = 704 KB）有清晰结构但需 palette 对位
- **下一步**：mGBA 运行时挂 watchpoint 到特定簇地址，从屏幕变化反查资源归属

---

## 二、0x01ED49D4..0x02000000（1.2 MB）— 次级压缩资源系统

### 扫描要点
- 熵分布：**99.8% 高熵 (>7)** — 典型 **LZ 压缩数据**
- 区首 bytes `10 2C 02 00 00 00 2C 02 00 52 4C 43 4E 00 FF FE ...`
  - `10` = GBA LZ77 magic；`2C 02 00` = decompressed size 0x22C (556 B)
  - 偏移 9 处 `52 4C 43 4E` = "RLCN" = **NCLR 调色板**（NNS）
  - 偏移 25 处 `54 54 4C 50` = "TTLP" = PLTT section of NCLR
- 形态：Konami 自定义包裹 + 标准 NNS container

### 指针表
- `0x01ED4AAC..0x01ED4AB4` — 3 条 u32 指针 `0x09ED4C8C, 0x09ED4CE4, 0x09ED4D3C`  
  （步长 0x58 = 88 B，连续 chunk 索引）
- `0x01ED4DA0..0x01ED519C` — **256 条 u32 指针**（1020 B 表）  
  首几条 `0x09ED4D98, 0x09ED4D98, 0x09ED4DA0` — 有重复，可能含 sentinel

### 结论
- 这是一个**独立于主 FS 的次级资源系统**（不走 `fs-tables.s` 索引）
- 256-entry pointer table + LZ77 / NNS 混合压缩资源
- 整块 **raw 封存**即可，后续用 `tools/ad-hoc/nns_extract.py`（待落地）扫整条
- **下一步**：加 FS 大扫描器时把这 1.2 MB 也纳入，但不强行结构化 ROM 层

---

## 三、0x01B8FB8C..0x01CCCA90（1.3 MB）— 字库前段

### 扫描要点
- 熵分布：**89.3% 稀疏 (≤3)** — 4bpp tile 典型
- ASCII 高频 `'UUUUU'` (0x55) / `'nfff'` (0x6E) / `'lfff'` (0x6C) — 4bpp 像素 pattern
- 指针簇：连续 `0x08311300, 0x08311301, ...` = **BG tilemap 条目**（u16 pair：tile_idx + palbank）

### 静态 XREF
- 21 个真字面量，聚 6 个簇：
  - `0x09B8FB8C..0x09B9119C`（区首紧邻，4 条）@ L23586-23594 — 函数 `FUN_08023b6c` 的一部分
  - `0x09B921D4..0x09B93844`（5 条）@ L26536-26544 — 另一屏 loader
  - `0x09B9487C..0x09B97328`（7 条）@ L21013-21025 — `FUN_08023b6c` literal pool，显式加载
    BG 0x06004000、OBJ 0x06010000、OBJ+0x200、PALRAM 0x05000200 — **完整 screen resource bundle**
  - 尾部 `0x09BA1524..0x09BA2430`、`0x09BC1FA8`、`0x09CCB490/E90` 零散
- 加载函数 `FUN_08023b6c` 是 screen loader（具体屏幕未命名）

### 结论
- 本区是 **多屏 tile + tilemap + palette bundle**
- 至少 3 个屏幕的资源各占几十 KB
- 每屏需单独识别（从 XREF 函数切入）+ 结构化为 `graphics/bin/<screen>/...`
- 单轮结构化不现实，需分屏推进

---

## 四、当前推荐优先级

按工作量 / 收益：

1. **不动**这两个区，保留 raw（文档化后）
2. 优先攻**低复杂度中型区**（300 KB - 1 MB 范围）：
   - `0x01CE822C` 880 KB（字库后段后部，可能含 FS 资产前置数据）
   - `0x01896730..0x01A00000` 1.4 MB 子片（本区前半，非 64 KB bank 部分）
3. 完成 `.LZnclr` 等 NNS 解析器（解掉压缩区的语义）
