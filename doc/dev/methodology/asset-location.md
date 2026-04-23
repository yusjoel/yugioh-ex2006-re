# 方法论：ROM 资产定位

**用途**：把 ROM 中的未知数据段识别出来，定位加载函数，提炼格式，最终结构化到 `data/*.s` 或 `graphics/bin/`。

本文合并了项目两条互补的定位路径：
- **动态路径**：已知某屏渲染什么，求 ROM 源地址（从 VRAM 反查）
- **静态路径**：已知 ROM 某段未知用途，求语义（从字节 + XREF 反查）

---

## 一、方法论总览：两条互补路径

```
已知起点                方法选择                               产出
─────────────────────────────────────────────────────────────────
屏幕上看见某资源  →  动态路径（§二六步）                →  加载函数 + ROM 地址
某段 ROM 未知     →  静态路径（§三四阶段）              →  子区切分 + 语义
已定位到函数要验证  →  GDB batch（外链 tools/gdb-debugging.md）  →  参数/调用链
```

**何时用动态**：能在游戏里截到资源（卡图、图标、UI），目标是找 ROM 源地址。

**何时用静态**：`asm/rom.s` 里有大段 `.incbin "roms/2343.gba", off, size`，不知道是什么，想拆分。

**两条路径常常互相支撑**：动态路径的步骤 ⑤ 爬升需要 XREF 工具（静态路径阶段 2）；静态路径的阶段 3 可选地用动态 MCP 做运行时对齐。

---

## 二、动态路径：从 VRAM 差异到 ROM 源地址

**方法论一句话**：动态工具确定"写到哪里"，静态工具确定"谁来写"。IO 寄存器配置值或其它强语义指纹做全 ROM 搜索是效率最高的主路径；GDB VRAM watchpoint 是可行的备选（2 次 continue 即可命中解码器），已知函数地址时 GDB hbreak 是最快的参数验证手段。

### 六步流程

```
① 触发前后 VRAM 快照         ─┐
② 定位差异区间             (动态 mGBA MCP)
③ 读 IO 寄存器解码显示模式  ─┘
                                 ↓ 产出"强指纹候选池"
④ 选择强指纹做全 ROM 搜索    ─┐
⑤ 从被定位函数沿调用图爬升   (静态 asm/all.s + grep)
⑥ 字面量池验证           ─┘
                                 ↓ 产出被锁定的目标函数
⑦ 导出 + 目视对比验证         (离线渲染，拦截 tile 格式/bpp 错误)
```

### 步骤 ①：触发前后 VRAM 快照

- 使用 ss1 存档落在资源加载**前**的稳态
- 通过 mGBA MCP 操纵按键进入资源加载**后**的状态
- 前后各做一次 `mgba_live_read_range(0x06000000, 0x18000)`（完整 96 KB VRAM）+ `mgba_live_dump_oam`

### 步骤 ②：定位差异区间

对两份快照做 byte diff，合并间隔 ≤ 64 B 的相邻差异点形成区间列表。按区间大小排序，最大的几段通常对应：

- **BG tile 数据**（charblock 区，4 KB 对齐）
- **BG tilemap**（screenblock 区）
- **Sprite tile**（`0x06010000+`）

区间起始地址就是"资源写入目标 VRAM 地址"——记下它，但**不要**急着对它下 GDB watchpoint（地址可能错，见 §四·A 失败教训）。

### 步骤 ③：读 IO 寄存器解码显示模式

在资源加载后的状态读 `mgba_live_read_range(0x04000000, 0x10)`，得到 DISPCNT / BG0-3 CNT。

**为什么这一步关键**：IO 寄存器里会出现"进入该页面/该资源时**特征性地**配置成某个值"的硬编码立即数——这些立即数就是最好的静态指纹。

典型可用指纹：

| IO 寄存器 | 地址 | 含义 | 作为指纹的特征 |
|-----------|------|------|---------------|
| DISPCNT | `0x04000000` | 显示模式 + 层启用 | 切换模式时必写 |
| **BG0CNT** | `0x04000008` | BG0 tile/map/色深 | **每页面取值近乎唯一** |
| BG1CNT / BG2CNT / BG3CNT | `0x0400000A`+ | 同上 | 同上 |
| WIN0H/V | `0x04000040+` | 窗口裁剪 | 极少页面使用，指纹强 |
| BLDCNT | `0x04000050` | 特效混合 | 淡入淡出页面常见 |

**BGxCNT 位域解码参考**（以 `BG0CNT = 0x0086` 为例，二进制 `0000 0000 1000 0110`）：

| 位 | 值 | 含义 |
|----|----|------|
| 1-0 | `10` | priority = 2 |
| **3-2** | **`01`** | **char base block (CBB) = 1 → tile 池起点 `0x06000000 + 1 × 0x4000` = `0x06004000`** |
| 6 | `0` | mosaic off |
| **7** | **`1`** | **color mode = 8bpp（256 色），每 tile 64 B** |
| 12-8 | `00000` | screen base block = 0 → tilemap 起点 `0x06000000` |
| 15-14 | `00` | size = 32×32 |

CBB（bits 3-2）+ 色深（bit 7）共同决定"该 BG 层的 tile 数据可落在 VRAM 哪些范围"，是步骤 ③.5 做差异归属时的核心输入。

### 步骤 ③.5：差异区间归属到具体 BG 层

步骤 ② 得到的差异区间地址只告诉你"写到了 VRAM 哪里"，但卡图页通常 BG0/1/2/3 同时启用，**光看 VRAM 地址还不能确定是哪一层在写**。必须把步骤 ③ 读到的四个 `BGxCNT` 逐个解码成"该层 tile 可覆盖的 VRAM 范围"，再比对差异区间才能归属。

**每层可达范围 = (CBB 基址) × (色深决定的每 tile 大小) × (最大 tile 编号)**。以卡图页为例：

| 层 | CNT 值 | CBB | 色深 | 每 tile | 可达 VRAM 范围 |
|----|--------|-----|------|---------|---------------|
| BG0 | `0x0086` | 1 | **8bpp（64 B）** | 64 | `0x06004000`–**`0x0600FFFF`**（可越界到 CB2/3） |
| BG1 | `0x4104` | 1 | 4bpp（32 B） | 32 | `0x06004000`–`0x06007FE0`（512 tile 恰填 CB1） |
| BG2 | `0x0407` | 1 | 4bpp | 32 | 同上 |
| BG3 | `0x0305` | 1 | 4bpp | 32 | 同上 |

**关键算术**：
- **4bpp 模式**下一个 charblock 恰好容 `0x4000 / 32 = 512` 个 tile，4bpp 层写入**必然全部落在 CBB 所在 charblock 内**，不会越界。
- **8bpp 模式**下一个 charblock 只容 `0x4000 / 64 = 256` 个 tile，**tile 编号 ≥ 256 会自动延伸到下一个 charblock**（GBA 硬件行为）。

→ 差异区间 `0x06008040` 位于 charblock 2，4bpp 永远不可能到达，**唯一归属于 BG0**（该页面唯一的 8bpp 层）。

**推论**：`BG0CNT = 0x86` 作指纹的强度来源于它**同时编码了 CBB 和色深**两个条件——光有 CBB=1 无法区分四个 BG 层（都用 CBB=1），加上色深位才形成"能触达 charblock 2 且用 8bpp"这一唯一可识别配置。

### 步骤 ④：选择强指纹做全 ROM 搜索

**指纹选择原则**（按强度从高到低）：

1. **"IO 地址 + 特定立即数"组合**（最强）
   - 例：写 BG0CNT = 0x86 → 指纹 = `movs Rx,#0x86` + 紧邻 `strh Rx,[Ry]` + 函数含 `.word 0x04000008`
   - 全 ROM 常命中 ≤ 3 个函数
2. **自定义编码常数**（强）
   - 例：6bpp 解码用 `0x3F3F` 双 6 位掩码
   - 事后验证用，不作初始钩子（此时还不知道编码格式）
3. **ROM 数据表基址字面量**（中）
   - 例：`0x08510640`（tile 数据基址）
   - 定位到加载函数后出现在字面量池，供交叉验证
4. **"基址 + 固定偏移"组合**（强，隐含 layout 约定）
   - 例：`0x06010040`（跳过图标槽的文字起始）比 `0x06010000`（纯基址）强 15 倍
5. **VRAM 基址字面量**（**弱**，不建议作单独钩子）
   - 例：`0x06004000` 在本 ROM 中出现于 18 个函数，信噪比低

**指纹强度实测原则**：开搜前先用 `grep -c` 统计候选指纹在 `asm/all.s` 的出现次数，是几秒钟的廉价评估：

| 出现次数 | 使用建议 |
|---|---|
| 1–5 | 极强指纹，可直接锁定 |
| 5–50 | 可用作主钩子，通常需 1–2 个附加条件收敛 |
| 50+ | 只适合做粗筛或交叉过滤输入 |
| 1000+ | 放弃，换钩子 |

### 步骤 ⑤：从被定位函数沿调用图爬升

初始命中的函数往往是"叶子级"操作（单次 IO 写、单个循环），需要爬升到对业务有意义的层级：

```
grep "bl <被命中函数>" asm/all.s   → 找直接调用者
继续 grep 调用者的调用者         → 直到到达"顶层页面入口"
```

**成功信号**：某层函数内部包含多个 `bl` 依次做"配置显示模式"→"加载资源"→"启动动画"等阶段性工作。

**一般化启示：相邻兄弟分支 = 天然强钩子**

```
FUN_0801e440 (顶层):              ← 卡牌信息页入口
  bl FUN_0801d45c                 ← BG0 初始化
  bl FUN_0801d998 → FUN_0801d290  ← 卡图 6bpp 解码
  bl FUN_0801dbdc                 ← ?
  bl FUN_080eeb54                 ← 卡片数据查询
  bl FUN_0801e000                 ← ★ 描述文本渲染（字库定位入口）
  bl FUN_0801e100                 ← 收尾
```

定位一个资源后，顶层页面函数的相邻 `bl` 往往是同页面其它资源的加载入口。后续任务的优先策略：
1. `grep "bl FUN_<顶层>" asm/all.s` 找到所有调用点
2. 读顶层函数字面量池 + 列出相邻 `bl` 序列
3. 按资源类型筛选（写 VRAM OBJ 区的是文字/图标、写 palette RAM 的是配色、长循环 + 算术的是位图解码）

### 步骤 ⑥：字面量池验证

在锁定的目标函数（可能是最初命中的叶子，也可能是爬升后发现的加载主函数）里读字面量池：

- 是否包含 VRAM 目标地址（与步骤 ② 差异区间吻合）？
- 是否包含 ROM 源数据地址（`0x08xxxxxx` 或 `0x09xxxxxx`）？
- 是否包含索引表基址 + 表项大小算式？

三项齐全 → 定位成功，可据此计算 ROM 源地址并离线解码验证。

**1bpp / Nbpp 编码识别指纹**：看到 `ldr[bh] + 移位 + bl 渲染` 小循环，先算 `总字节 = 循环次数 × 每轮字节`，与资源尺寸反推 bpp：

| 特征 | 定位步骤 |
|------|----------|
| 循环计数常量 | 决定"共多少字节"与"字形总尺寸" |
| 每轮读取字节数 | 决定编码密度（bpp） |
| 每轮输出像素数 | 验证：`每轮字节 × 8 / bpp = 每轮像素` |
| 内层渲染函数 | 最终渲染/解码细节 |

### 步骤 ⑦：导出 + 目视对比验证

定位到 ROM 源地址后，**必须**离线渲染 PNG 并与游戏截图目视对比，确认解码逻辑正确：

1. 编写导出脚本（参考 `tools/rom-export/`），将 ROM 数据按正确的 tile 格式渲染为 PNG
2. 与步骤 ① 的游戏截图逐像素对比：资产在截图中的位置、尺寸、图案轮廓应完全吻合
3. 若不吻合，说明 tile 格式理解有误（常见错误：线性像素 vs 8×8 tile 结构、4bpp vs 8bpp、行列顺序）

这一步成本极低（几秒钟目视），但能拦截 tile 格式、bpp、行列序等类别的错误——这类错误在 byte-identical 构建验证中**不会暴露**（因为 `.incbin` 原始字节本身不涉及渲染逻辑）。

---

## 三、静态路径：从 ROM 未知段到语义切分

**目标**：把一段未知的 ROM 数据区（几十 KB 到几 MB）切成语义子区、识别格式、拆出结构化 `.s` 或 bin 资产、验证 byte-identical。

**适用**：`asm/rom.s` 里还剩 raw `.incbin "roms/2343.gba", off, size"` 的大块。

### 四阶段流程

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

**输出**：带地址轴的"内容类型地图"（熵/nz 折线 + 特征标记）+ 候选子区边界列表。

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
5. **产物**：地址 → 用途 → 加载函数 表，写入 `doc/analysis/<阶段>-xref.md`

### 阶段 3 — 运行时对齐（可选，0.5-1 h）

**何时用**：阶段 1+2 切不干净、XREF 稀疏、剩大段白域时。

工具：mGBA MCP + GDB（场景 C：batch 脚本 + 按键注入，见 [`tools/gdb-debugging.md`](../tools/gdb-debugging.md)）

1. 在阶段 2 找到的候选地址上挂 hbreak / watchpoint（整区 3 MB 挂 watchpoint 太重，只挂**离散候选点**）
2. 进不同屏幕时按键触发 → 捕获 r0 (源) / r1 (目) / r2 (长度)
3. 对照 VRAM / PALRAM 快照变化，按 §二 六步流程锁定资产到屏幕

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

### 产出规范

每次探索留 3 类文件：

1. **扫描脚本** `tools/ad-hoc/scan_<区名>.py`（阶段 1 专用，可复用 + 一次性）
2. **调查日志** `doc/analysis/<区名>-survey.md`（融合阶段 1-3 的发现、子区划分、XREF 表）
3. **正式导出器** `tools/rom-export/export_<模块>.py`（阶段 4 每个识别出的模块一个）

### 风险与退路

| 风险 | 识别信号 | 退路 |
|---|---|---|
| 整块是一个/几个巨大压缩档 | 阶段 1 首字节 `10/20`，覆盖 >90% 区间 | 退化为"拆 bin + 解压工具"，不求结构化 |
| 跨 16 MB 边界的 alignment hole | 大块 `00`/`FF`，`asm/rom.s` 上下游有明显 pad | 保留 raw，仅注释标 alignment-pad |
| 混入 SOUND bank / MIDI / MOD | 扫到 GBA sappy 0x80000000 sig，或 MIDI 头 | 抓 bin 不逆，参考 `refs/awesome-gbadev` 工具 |
| 访问点全是 Ghidra 未命名函数 | 阶段 2 找不到语义 | 阶段 3 动态辅证；实在不通留 `UNIDENTIFIED` |

---

## 四、探索方向对比与经验教训

> **免责声明**：本节结论是**本次具体任务 + 本 ROM**的实测结果。不同 ROM、不同资源、不同 IO 取值下，各方向的强度可能互换。本节意在给出"如何评估一个方向"的框架，而不是给任一指纹打"好/坏"的标签。

### A. GDB watchpoint / hbreak

卡图定位原本设计的 Phase B2 是"对 VRAM 目标地址下 watchpoint，读写指令触发后沿 r0/r1 源寄存器向上追踪"。**本次卡图定位时未走此路**，但后续补充实验证明 **VRAM watchpoint 完全可以定位到解码器**（详见 [`doc/analysis/card-image-location.md`](../../analysis/card-image-location.md) Phase B3）。

**实测（2026-04-16）**：

```
watch *(unsigned char*)0x06004040    ← 解码器首次 VRAM 写入地址

HIT 1 (continue ①): PC=0x080F4E86 (memclear), LR=0x0801D47D (init_bg0)
HIT 2 (continue ②): PC=0x0801D406 (decode_card_image_6bpp 内部!)
                     → 从 PC 向上找 push {r4..lr} 即可定位函数入口 0x0801D290
```

**GDB 工具组合（按场景选择）**：

| 场景 | 工具 | 说明 |
|------|------|------|
| 从零定位未知函数 | **VRAM watchpoint**（GDB batch 脚本） | watch 写入地址 → 2 次 continue → 命中解码器内部 |
| 已知函数，验证参数 | **hbreak**（GDB batch 脚本） | hbreak 函数入口 → 捕获全部寄存器 |
| 暂停态求值/单步 | **GDB MCP 交互** | 不涉及 continue，同步响应正常 |

**操作要点**（完整操作细节见 [`tools/gdb-debugging.md`](../tools/gdb-debugging.md)）：
- 必须使用 GDB batch 脚本而非 GDB MCP 交互式 continue
- GDB batch 后台运行 + mGBA MCP `input_set` 注入按键触发转场
- 每次 GDB `kill`/`quit` 后 stub 永久关闭，需 `mgba_live_stop` + 重新 `mgba_live_start`

**早期失败的真正原因**（非工具限制）：
- 基于"BIOS LZ77"假设在 `0x08015076` 等处下 hbreak 全部未触发——游戏用自写 6bpp 解码，不走 BIOS SWI
- 早期 watchpoint 在 `0x06000000`（tile 0，不是卡图写入位置）设 watchpoint，且使用 ss1 存档（卡图可能已预加载）——地址错 + 状态错，并非 watchpoint 机制本身的限制

**与静态分析的对比**：
- 静态分析（IO 指纹搜索）一步到位，不需要多轮调试循环——仍然是**效率最高的主路径**
- VRAM watchpoint 需要 2 次 continue + 人工分析 PC 地址——可行但慢，适合作为**验证或备选路径**
- 两者最佳搭配：静态分析定位函数 → GDB hbreak 验证参数签名和调用链

### B. VRAM 基址字面量搜索（可用于粗筛）

用脚本 `doc/dev/scripts/find_vram_literal_owners.py` 验证（2026-04-15）：

- `asm/all.s` 中 `.word 0x06004000` 出现 **19 处**，分布在 **18 个函数**
- 其中目标函数 `FUN_0801d290` 在"函数大小 + ROM 字面量数 + 循环跳转数"排序里**仅排第 6**
- "ROM 字面量 ≥ 8 且循环跳转 ≥ 4" 的强候选共 3 个，均不是目标函数

**这不是"失败"**：
- 18 个函数的候选池**远远小于**全 ROM 3,296 个函数，已完成 **99.5% 的剪枝**
- 候选池可作为后续交叉搜索的**输入集**（例如在其中再搜 `0x08510640` / 大循环 / `0x3F` 掩码等辅助特征）
- 即便不是首选主路径，列表里的其它函数将来分析 UI/边框/其它 BG 资源时仍可能是目标

**使用建议**：当没有更强的候选钩子时，这一方向是可靠的起点；主要限制是需要额外的过滤维度（循环数、相邻字面量等）才能收敛到唯一目标。

### C. IO 寄存器"地址 + 立即数"组合（最强路径）

用脚本 `doc/dev/scripts/find_bg0cnt_86_writer.py` 验证：

- 全 ROM `.word 0x04000008` 出现 46 处
- 全 ROM `movs Rx,#0x86` 出现 21 处
- 三条件联合命中**只有 1 个函数**：`FUN_0801d45c`
- 仅两条件（`movs #0x86` + 紧邻 `strh`）也**只命中 1 个**

`FUN_0801d45c` 是卡图页初始化器 → 唯一调用者 `FUN_0801e440`（卡图页顶层入口）→ 相邻 `bl FUN_0801d998` → `FUN_0801d290`。

**这一次的"一击命中"包含运气成分**：
- `0x86` 这个 8 位立即数恰好在本 ROM 中作为 `movs` 立即数极少出现（21 处）
- 若 BG0CNT 取值恰好是游戏代码中**频繁**出现的组合（如 `0x0080 / 0x0084`），指纹强度会下降
- 其它资源若通过 DMA 而非 CPU 写 BG CNT，这一方向完全失效

**使用建议**：当步骤 ③ 观察到的 `BGxCNT` 立即数足够"不常见"（可提前用 `grep -c` 估算密度），这是最高效的钩子；否则退回方向 B 做粗筛并配合 IO 特征做联合过滤。

### D. DISPCNT 差异位组合（进入页面时机指纹）

state1（卡组列表）`DISPCNT = 0x1D00` 与 state3（卡牌信息页）`DISPCNT = 0x1F40` 差异解码显示：同时置位 bit 6（OBJ 1D Mapping）+ bit 9（BG1 显示）。`movs #0x1F40` 或 `.word 0x1F40` 全 ROM 出现次数极低。

**一般化**：**DISPCNT 的差异位组合比 BGxCNT 的全字值更罕见**，是定位"页面切换时机"的首选指纹。

### E. "合成产物 vs 原始素材"判别

有些资源（卡图、图标）是 ROM 字节**直接对应** VRAM 字节（可逆映射），而另一些（文字、HUD 数字、动画插值）是运行时**合成**出来的。

**判别方法**：拿几个显眼的 VRAM tile 原始字节在 ROM 做 byte search。
- 命中 ≥ 1 且字节非全零 → **原始素材**（卡图、图标、地图 tile），可直接搜字节定位
- 全部未命中 → **合成产物**（文本、HUD 数字、动画插值），必须沿"**渲染器 ← OAM / BGxCNT ← 顶层页面入口**"这条代码路径追

**实测（字库）**：tile 1 图标字节→ROM 命中 ✓（原始素材）；tile 2..20 字形字节→0 hit ✗（合成产物）。判定字库走合成路径，放弃字节反搜、改走 IO + 代码字面量。

---

## 五、实战复盘

### 案例 1：卡牌大图（6bpp 80×80 → `FUN_0801d290`）

| 步骤 | 实际产出 |
|------|---------|
| ① 快照 | Phase A 取 state1（卡组列表）/ state3（卡牌信息页）两份 VRAM |
| ② 差异 | 最大区间 `0x06008040–0x0600933F`（4864 B，位于 Charblock 2） |
| ③ IO | 四层全用 CBB=1；BG0 `0x0086` = 8bpp，BG1/2/3 `0x4104/0x0407/0x0305` 均 4bpp |
| ③.5 归属 | 4bpp 层可达 ≤ `0x06007FE0`，不能到 charblock 2；差异落在 `0x06008040` ⇒ **唯一归属 BG0** |
| ④ 指纹 | `movs Rx,#0x86` + `strh Rx,[0x04000008]` → 命中 `FUN_0801d45c`（0x86 同时锁 CBB + 色深） |
| ⑤ 爬升 | `bl FUN_0801d45c` 唯一调用者 → `FUN_0801e440`；相邻 `bl FUN_0801d998` → `FUN_0801d290` |
| ⑥ 验证 | `FUN_0801d290` 字面量池含 `0x08510640`（ROM 基址）/ `0x06004000`（VRAM 基址）/ 800 循环次数 → 归纳出 6bpp 解码公式 |

最终结论见 [`data-structure/card-image-big.md`](../data-structure/card-image-big.md)；完整调研叙事见 [`doc/analysis/card-image-location.md`](../../analysis/card-image-location.md)。

### 案例 2：英文字库（1bpp 8×8 → `FUN_080f1b60`）

| 步骤 | 实际产出 |
|------|---------|
| ① 快照 | 同卡图使用 state1 / state3（卡牌信息页 A→A 进入）；顺带 dump OAM + palette |
| ② 差异 | 最大 BG 差异仍是卡图 4864 B 那段；**OBJ tile 区**出现 `0x06010005–0x060107FC`（2040 B，≈64 tiles）大段连续差异 + 多个散布区间 |
| ③ IO | DISPCNT=`0x1F40`（BG0/1/2/3+OBJ+1D 映射）；BG0CNT 仍是 `0x0086`（卡图层不变）；**文字不走 BG** |
| ③.5 归属 | 差异地址 ≥ `0x06010000` ⇒ **唯一归属 OBJ sprite tile**；OAM 分析发现 indices 12-63 是 32×8 水平条 sprite，tile 索引从 2 起步进 4，palette F ⇒ 正是文字区块 |
| ④ 指纹 | `0x06010040`（OBJ tile 2 起始，跳过图标槽）全 ROM 4 处——**极强**（对比 `0x06010000` 59 处） |
| ⑤ 爬升 | **复用卡图同一顶层** `FUN_0801e440`，走"卡图兄弟分支"`FUN_0801e000` → `FUN_080f2aa8` → `FUN_080f1b60` |
| ⑥ 验证 | Python 离线 1bpp 8×8 解码 ASCII 0x21..0xFF，所有字形清晰可辨 |

### 案例 3：Pack banner（8bpp 32×64 OBJ sprite → `FUN_080db860`）

三方向互补定位：

| 方向 | 指纹 | 命中数 | 定位到 |
|------|------|--------|--------|
| B: VRAM 字面量 | `0x06016000` | 2 | `FUN_080bdfac`（pack UI 状态机） |
| C: IO 指纹 | BG2CNT=`0x1E0D` | 1 | `FUN_080d8d84` → `FUN_080d971c`（页面初始化） |
| A: GDB hbreak | `FUN_080d971c` + `FUN_080db860` | 6 hits | 验证参数和调用链 |

**关键教训**：
- 方向 B 和 C 找到的是**互补的**函数群（运行时状态机 vs 一次性初始化）
- GDB VRAM watchpoint 因 DMA 未触发，改用 hbreak 在已知函数上成功
- `0x06014000` 有 52 处命中太多，改用 `0x06016000`（仅 2 处）作为强指纹
- 初次检查 ROM 数据时只看了前 16-32 字节（恰好是零 padding），误判为"数据全零"——**必须检查完整 block 不只看前几字节**
- 首次渲染时把 8bpp 8×8 tile 数据误当线性像素处理，PNG 是乱码——**目视对比拦截了这类错误**

---

## 六、历史复盘（静态路径应用）

| 区间 | 大小 | 应用结果 |
|---|---|---|
| `0x01326280..0x15B5C00` | 2.6 MB | stride 1152 / 8bpp 3×6，拆出 `card-mini-frame` |
| `0x01463480..0x014E3480` | 512 KB | font 定位；tile 索引 6330 反查 |
| `0x01E64684..0x01ED49D4` | 459 KB | FS 339 文件按路径拆出（见 `fs-export-and-ocg-tcg.md`） |
| `0x00FBC080..0x01326280` | 3.58 MB | stride 1536 / 8bpp 4×6，拆出 `card-medium-frame`；单次覆盖率 +12.55% |

---

## 七、可复用脚本

| 脚本 | 用途 |
|------|------|
| `doc/dev/scripts/find_vram_literal_owners.py` | 扫某个 32 位字面量在 asm/all.s 的归属函数及函数特征（大小/ROM 字面量数/循环数） |
| `doc/dev/scripts/find_bg0cnt_86_writer.py` | 「IO 地址字面量 + movs 立即数 + 紧邻 strh」三条件联合筛选 |
| `tools/ad-hoc/scan_region_3mb.py` | 静态路径阶段 1 全特征扫描（熵/nz/LZ77/NNS/stride） |
| `tools/ad-hoc/diff_vram_font.py` | state1/3 VRAM 二进制 diff + 按 gap ≤64 合并区间 |
| `tools/ad-hoc/dump_font_tiles.py` | 从 VRAM dump 把 sprite tile 渲染为 ASCII art，快速识别是否字形 |
| `tools/ad-hoc/search_font_bytes.py` | 在 ROM 内直接搜 VRAM tile 原始字节（判定"原始素材 vs 合成产物"） |
| `tools/ad-hoc/decode_card_6bpp.py` | 卡图 6bpp 解码单卡验证（离线 ROM 读取 + PGM 输出） |
| `tools/ad-hoc/decode_font.py` | 1bpp 8×8 字形离线解码验证 |

两个通用筛选脚本可直接改常量适配新任务（修改 `TARGET` / `LIT_*` / `MOVS_*` 正则即可）。

---

## 八、相关文档

| 文件 | 关系 |
|------|------|
| [`build-pipeline.md`](build-pipeline.md) | 端到端构建流水线：定位后的结构化 → byte-identical → Ghidra 标注 |
| [`../tools/gdb-debugging.md`](../tools/gdb-debugging.md) | GDB stub + GDB MCP 调试指南（12 个坑、断点矩阵、GDB batch PoC） |
| [`../tools/mgba-mcp.md`](../tools/mgba-mcp.md) | mGBA MCP 使用指南（含 §六典型分析流程：VRAM 差分 Lua 模板） |
| [`../../analysis/card-image-location.md`](../../analysis/card-image-location.md) | 卡图定位完整时间线（Phase A/B0/B1/B2/B3，本文是其方法论提炼） |
| [`../data-structure/`](../data-structure/) | 最终 spec（本方法论的产出目标） |
