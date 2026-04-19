# 静态数据区探索方法论

**用途**：把一段未知的 ROM 数据区（几十 KB 到几 MB）切成语义子区、识别格式、
拆出结构化 `.s` 或 bin 资产、验证 byte-identical。

**适用**：`asm/rom.s` 里还剩 raw `.incbin "roms/2343.gba", off, size"` 的大块。

**补充文档**：
- `doc/dev/locate-rom-asset-from-vram-diff.md` — 动态路径（IO 指纹 + GDB 断点
  从 VRAM 反查 ROM），适用于"已知某屏渲染什么"求源地址。
- 本文是**静态路径**——适用于"已知 ROM 某段未知用途"求语义。

---

## 四阶段流程

### 阶段 1 — 静态特征扫描（机械活，1-2 h）

**目标**：把区间切成语义边界清晰的子区间，不求语义，只求**切分**。

按机器模式匹配的 7 种特征：

| 扫描 | 信号 | 解读 |
|---|---|---|
| **零字节 run-length** | `00` 连续 ≥ 32 B | padding / 未用 gap / 子区边界 |
| **滑动熵** | 512 B 窗，`H = -Σ p·log₂p` | > 7 压缩/tile；3-5 代码/table；< 3 稀疏结构 |
| **nz-ratio** | 非零字节占比 | < 20% 典型 sparse table；> 80% 典型 tile/压缩 |
| **GBA LZ77 头** | `10 XX XX XX`，u24 size 合理（< 1 MB） | BIOS SWI 0x11 解压块 |
| **GBA Huffman 头** | `20 XX XX XX` 或 `28 ...` | SWI 0x13 解压块 |
| **NNS 签名** | `RGCN/RLCN/RECN/RNAN/RCSN/TNFR` LE | Nintendo g2d 资源 |
| **ASCII 串** | printable ≥ 4 连续 | 路径 / 调试 / 文件名表 |
| **u32 指针簇** | 连续 `0x08XXXXXX / 0x09XXXXXX` LE | pointer table，指向本区或外部 |
| **stride 自相关** | stride ∈ {16, 32, 64, 128, 256, 512, 1024, 1152, 2048, 2240, 2560, 4096, 4800}，检 `(i, i+stride)` 首字节统计 | 周期化 tile 块 / 数据表 |

**输出**：带地址轴的"内容类型地图"（熵/nz 折线 + 特征标记）+ 候选子区边界
列表。

**实用工具模板**：`tools/ad-hoc/scan_region.py <start> <end>`（可复用于多个区）。

### 阶段 2 — asm/all.s 静态 XREF（高价值，1 h）

**目标**：每个代码访问点 = "这段数据是什么用途"的硬证据。

1. **穷举字面量**：在 `asm/all.s` 搜索目标地址范围内的 `.word 0x09XXXXXX`
2. **聚类**：相近地址（±256 B 内）通常是同一表不同 offset，归为一组
3. **上下文分析**：每簇取前后 20 行汇编
   - `ldr rN, =0xXXX` → 源/目标地址
   - `ldrh / ldrb / ldr` 元素宽度 → 数据单元大小
   - `lsls / adds` 索引计算 → stride、flag 公式
   - `bl FUN_XXX` → 加载函数；若已由 Ghidra 命名（`doc/dev/ghidra-function-names.md`）直接读语义
4. **未命名函数处理**：用参数类型 + 调用链取临时名（如 `maybe_tile_loader_at_0xXXX`）
5. **产物**：地址 → 用途 → 加载函数 表，写入 `doc/dev/<阶段>-xref.md`

### 阶段 3 — 运行时对齐（可选，0.5-1 h）

**何时用**：阶段 1+2 切不干净、XREF 稀疏、剩大段白域时。

工具：mGBA MCP + GDB（场景 C：batch 脚本 + 按键注入，见 `CLAUDE.md`）

1. 在阶段 2 找到的候选地址上挂 hbreak / watchpoint（整区 3 MB 挂 watchpoint 太
   重，只挂**离散候选点**）
2. 进不同屏幕时按键触发 → 捕获 r0 (源) / r1 (目) / r2 (长度)
3. 对照 VRAM / PALRAM 快照变化，按六步流程（见 `locate-rom-asset-from-vram-diff.md`）
   锁定资产到屏幕

### 阶段 4 — 拆分落地（2-4 h）

对每个识别出的子区按形态决策：

| 形态 | 处理 |
|---|---|
| tile 数据（固定 stride） | `.incbin graphics/bin/<module>/tiles/*.bin` |
| palette | `.incbin graphics/bin/<module>/palettes/*.bin` |
| tilemap | `.incbin graphics/bin/<module>/tilemaps/*.bin` |
| u32 指针表 | 结构化 `.s`，用 `.word <label>` |
| 固定格式 struct 数组 | 结构化 `.s`，用宏或 `.word / .hword / .byte` |
| LZ77/Huffman 压缩块 | `.incbin` 保留；单独写解压脚本（不回塞） |
| 真·未识别 | 保留 raw `.incbin roms/2343.gba`，注释标 `UNIDENTIFIED` + 已知事实 |

每段拆完：

```bat
python tools/rom-export/export_<新模块>.py
build.bat
fc /b roms\2343.gba output\2343.gba
```

必须 byte-identical。更新 `data-analysis-coverage.md`。

---

## 产出规范

每次探索留 3 类文件：

1. **扫描脚本** `tools/ad-hoc/scan_<区名>.py`（阶段 1 专用，可复用 + 一次性）
2. **调查日志** `doc/dev/<区名>-findings.md`（融合阶段 1-3 的发现、子区划分、XREF 表）
3. **正式导出器** `tools/rom-export/export_<模块>.py`（阶段 4 每个识别出的模块一个）

---

## 风险与退路

| 风险 | 识别信号 | 退路 |
|---|---|---|
| 整块是一个/几个巨大压缩档 | 阶段 1 首字节 `10/20`，覆盖 >90% 区间 | 退化为"拆 bin + 解压工具"，不求结构化 |
| 跨 16 MB 边界的 alignment hole | 大块 `00`/`FF`，`asm/rom.s` 上下游有明显 pad | 保留 raw，仅注释标 alignment-pad |
| 混入 SOUND bank / MIDI / MOD | 扫到 GBA sappy 0x80000000 sig，或 MIDI 头 | 抓 bin 不逆，参考 `refs/awesome-gbadev` 工具 |
| 访问点全是 Ghidra 未命名函数 | 阶段 2 找不到语义 | 阶段 3 动态辅证；实在不通留 `UNIDENTIFIED` |

---

## 历史复盘（示例）

| 区间 | 大小 | 应用本方法论 |
|---|---|---|
| `0x01326280..0x15B5C00` | 2.6 MB | P2-1..P2-5：stride 1152 / 8bpp 3×6，拆出 `card-mini-frame` |
| `0x01463480..0x014E3480` | 512 KB | font 定位；tile 索引 6330 反查 |
| `0x01E64684..0x01ED49D4` | 459 KB | FS 339 文件按路径拆出（见 `fs-export-and-ocg-tcg.md`） |
| `0x01000000..0x01326280` | 3.3 MB | **待做**（见 `p3-unknown-region-3mb-*.md`） |
