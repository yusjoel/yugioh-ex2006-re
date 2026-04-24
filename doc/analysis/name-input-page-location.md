# 创建角色页（name_input）资产加载分析

**日期**：2026-04-23
**场景**：冷启动（无 .sav 存档 + 无 savestate）→ 标题页按 START → 进入创建角色页（name input keyboard）
**方法论**：`doc/dev/methodology/asset-location.md` §二 动态路径六步

---

## 一、实验条件

为避免 Continue 自动加载存档跳过创建角色页，**临时把 `roms/2343.sav` 移到 `doc/temp/2343.sav.backup`**，分析完再复位。这样：
- State A：冷启后标题页，"Continue" 菜单项不显示，只剩 "New Game"
- 按 START → "Enter your name." 对话框 → 按 A → 键盘输入页（state B）

快照产物（`doc/temp/`）：
| 文件 | 内容 |
|---|---|
| `A_screen.png` / `B_screen.png` | 两态屏幕截图 |
| `A_vram.bin` / `B_vram.bin` | 96 KB VRAM（`0x06000000..0x06018000`）|
| `A_palram.bin` / `B_palram.bin` | 1 KB PALRAM（`0x05000000..0x05000400`）|
| `A_io.bin` / `B_io.bin` | 96 B IO 寄存器（`0x04000000..0x04000060`）|
| `A_oam.bin` / `B_oam.bin` | 1 KB OAM |

分析脚本：`tools/ad-hoc/diff_home_vs_name.py`、`tools/ad-hoc/match_name_input_vram.py`、`tools/ad-hoc/match_gbtn_segments.py`、`tools/ad-hoc/find_name_input_bgcnt.py`

---

## 二、IO 寄存器对比（步骤 ③）

| 寄存器 | State A（title） | State B（name input） | 变化 |
|---|---|---|---|
| DISPCNT | `0x1B40` | **`0x1F40`** | BG2 新开启（4 层全启用 + OBJ + 1D 映射） |
| BG0CNT | `0x1D00` (prio0, CBB0, SBB29, 4bpp) | **`0x1C02`** (prio2, CBB0, SBB28, 4bpp) | 换到 SBB28 |
| BG1CNT | `0x1E01` (prio1, CBB0, SBB30, 4bpp) | **`0x1D8C`** (prio0, CBB3, SBB29, **8bpp**) | 色深+CBB 切换 |
| BG2CNT | `0x1F02` (prio2, CBB0, SBB31, 4bpp) | **`0x1E8D`** (prio1, CBB3, SBB30, **8bpp**) | 色深+CBB 切换 |
| BG3CNT | `0x9B0B` (prio3, CBB2, SBB27, 4bpp, 32×64) | **`0x1F8F`** (prio3, CBB3, SBB31, **8bpp**) | 色深+CBB 切换 |

**关键特征**：BG1/2/3 **三个 8bpp 层共享 CBB=3**（tile 池 `0x0600C000`），tilemap 分别挂 SBB 29/30/31。BG0 保持 4bpp，作为文字 overlay 层。这种"三层共享 8bpp 大图集"是 name_input 页的独特配置，指纹强度极高。

---

## 三、VRAM diff（步骤 ②）

总差异 **34,449 B / 98,304 B (35%)**，合并 gap≤64 的相邻区间：

| VRAM 区间 | 大小 | 归属 |
|---|---|---|
| `0x06000037..0x06002AE5` | 10,926 B | CB0 — BG0 4bpp 新 tile（文字字体） |
| `0x0600326B..0x0600487F` | 5,652 B | CB0 — BG0 tile 后段 |
| `0x0600C040..0x0600DCFC` | 7,356 B | **CB3 — BG1/2/3 共享 8bpp tile 池**（含 tile graphics + SBB27 残留） |
| `0x0600E004..0x0600E2F0` | 748 B | SBB28 — BG0 tilemap |
| `0x0600E800..0x0600ECFB` | 1,275 B | SBB29 — BG1 tilemap |
| `0x0600F000..0x0600F4FC` | 1,276 B | SBB30 — BG2 tilemap |
| `0x0600F800..0x06011324` | 6,948 B | SBB31 BG3 tilemap + **OBJ CB4 tile 池起始** |
| `0x06011379..0x06013149` | 多段散布 | CB4 — OBJ 键盘 sprite tile |

**PALRAM diff**：`0x05000004..0x0500026A`（522 B）——BG 调色板几乎全换（0..0x200 = BG pal 16×16色，第 2 个字节往后到 0x26A），OBJ palette 只有小动。

**OAM diff**：`0x07000000..0x0700019E`（414 B，~52 个 sprite 条目）——keyboard 字符 sprite。

---

## 四、FS 文件反查（步骤 ⑦ 目视 + 字节匹配）

`temp/fs-decompressed/name_input/` 下有 10 个文件，路径表（`data/file-paths.s`）索引 254..263，对应 FS FID 255..264（`path[i] ↔ FID[i+1]`）：

| FID | 路径 | ROM 压缩 | 解压后 | NNS 根 magic | 内部结构 |
|---|---|---|---|---|---|
| 255 | `name_input/name_b_01.LZ5bg` | 476 B | 3,000 B | `NTBG`（自定义）| PALT(524B) + BGDT(2460B, 30×32 tilemap) |
| 256 | `name_input/name_b_02.LZ5bg` | 588 B | 3,304 B | `NTBG` | PALT + BGDT(2764B, 30×20 tilemap + 24 tile) |
| 257 | `name_input/name_b_03.LZ5bg` | 436 B | 2,472 B | `NTBG` | PALT + BGDT(1932B, 30×20 tilemap + 11 tile) |
| 258 | `name_input/name_b_04.LZ5bg` | 504 B | 2,920 B | `NTBG` | PALT + BGDT(2380B, 30×20 tilemap + 18 tile) |
| 259 | `name_input/name_o_01.LZnanr` | 216 B | 353 B | `RNAN` | KNBA + LBAL + TXEU（OBJ 动画） |
| 260 | `name_input/name_o_01.LZncer` | 308 B | 433 B | `RECN` | KBEC + LBAL + TXEU（OBJ cell） |
| 261, 262 | `name_input/name_o_01.LZncgr` × 2 | — | 8,048 B × 2 | `RGCN` | RAHC(8032B)（OBJ 8bpp tile） |
| 263, 264 | `name_input/name_o_01.LZnclr` × 2 | — | 552 B × 2 | `RLCN` | TTLP(536B)（OBJ palette） |

### 4.1 `.LZ5bg` → `.gbtn` 解析结果

NNS 通用头（16 B）+ 2 个 section：
```
offset  magic  size       语义
0x0000  NTBG   (file)     
0x0010  PALT   0x020C     8bpp 调色板：section 头 8B + 4B 子头 + 512B palette
0x021C  BGDT   0x04B0+    BG 数据：section 头 8B + 16B 元数据 + tilemap + tile graphics
```

**BGDT 元数据（16 B）**：
```
0x00  u16 u16    flags (例: 0x01FF 0x0002)
0x04  u32        tilemap byte size (0x780 = 30×32×2 或 0x4B0 = 30×20×2)
0x08  u16 u16    w1, h1 (tile 数, 30×32 或 30×20)
0x0C  u16 u16    w2, h2 (同上——tile 数量和"使用"范围？)
```
后续数据：`[16 B 元数据][tilemap w×h×2 B][tile graphics N×64 B]`（8bpp）。

### 4.2 字节级匹配验证（关键证据）

`name_b_02.gbtn` 的 tile graphics 起点（文件偏移 `0x21C + 8 + 16 + 1200 = 0x6E8`）**逐字节等于** VRAM `0x0600C040` 的 8bpp tile 数据。对比片段（前 64 B）：

```
file@0x6E8:  f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 fd fd fd fd fd fd fd fd ...
VRAM@0x0600C040: f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 fd fd fd fd fd fd fd fd ...
```

说明 `.gbtn` 的 tile graphics 段**线性复制到 CBB3**（无格式转换）。

`name_o_01.ncgr` 数据段（文件 0x30 偏移起）线性复制到 VRAM `0x06010000+`（delta = 0x0600FFD0 ≈ VRAM 起点 − 0x30 NCGR 头）。

`name_o_01.nclr` 调色板数据段线性写入 **OBJ palette `0x05000208+`**。

### 4.3 .gbtn 与 BG 层的对应（尚未严格对号，但可推断）

4 个 `.gbtn` 对应 BG0/1/2/3 四层 tilemap：
- `name_b_01.gbtn`（30×32，较大）→ 可能是滚动/双高地图层，最可能的 BG3（最底 prio=3）
- `name_b_02.gbtn`（30×20 + 24 tile）→ tile 较多，像是复杂图形层（键盘外观底板？）
- `name_b_03.gbtn`（30×20 + 11 tile）→ 稀疏，背景条纹或装饰
- `name_b_04.gbtn`（30×20 + 18 tile）→ 中等

**最终归属需要做 tilemap 反查**（把 VRAM SBB28/29/30/31 与各 `.gbtn` 的 tilemap 段做字节 diff 即可锁定 1:1 映射）——本次未做。

---

## 五、静态 XREF：init 函数定位（步骤 ④⑤⑥）

### 5.1 强指纹搜索

目标：state B 的 BG1/2/3CNT 值 `0x1D8C / 0x1E8D / 0x1F8F` 属于 16-bit 立即数，在 THUMB 里用 `ldr Rx, =val` 从字面量池加载。全 ROM `.word` 次数：

| 立即数 | `.word` 次数 |
|---|---|
| `0x00001D8C` | 14 |
| `0x00001E8D` | 1 |
| `0x00001F8F` | **1**（极强指纹） |
| `0x00001C02` | 2 |

`0x1F8F` 唯一命中：`asm/all.s` 行 7297 @ `0x080175EC`，位于函数 **`FUN_08017574`**（`0x08017574`）字面量池里。

### 5.2 FUN_08017574 解读（name_input 页初始化）

```asm
FUN_08017574:                            @ 0x08017574  IO 初始化入口
  push {r4, lr}
  sub sp, #4
  ldr r1, =0x02029250                   @ r1 = EWRAM 页状态 struct
  movs r4, #0
  str r4, [sp, #0]
  ldr r2, =0x050000C9                   @ r2 = ??（可能是 length 0xC9 或 palette 槽）
  mov r0, sp
  bl FUN_0810E3F8                        @ 很可能是 memcpy/state-init 助手

  bl FUN_08014638                        @ 通用前序

  movs r1, #0x80; lsls #0x13              @ r1 = 0x80 << 19 = 0x04000000 (IO base)
  movs r0, #0xFA; lsls #5                 @ r0 = 0xFA << 5 = 0x1F40
  strh r0, [r1, #0]                       @ *** DISPCNT = 0x1F40 ***

  adds r1, #0x8                          @ r1 = 0x04000008 (BG0CNT)
  ldr r0, =0x1C02; strh r0, [r1, #0]      @ *** BG0CNT = 0x1C02 ***
  adds r1, #0x2; ldr r0, =0x1D8C; strh …  @ *** BG1CNT = 0x1D8C ***
  adds r1, #0x2; ldr r0, =0x1E8D; strh …  @ *** BG2CNT = 0x1E8D ***
  adds r1, #0x2; ldr r0, =0x1F8F; strh …  @ *** BG3CNT = 0x1F8F ***

  movs r1, #0x10; rsbs r1, #0             @ r1 = -0x10
  movs r0, #0x3F
  bl FUN_080146FC                         @ 可能是窗口 / 淡入 alpha 参数

  bl FUN_080148D0                         @ 淡入触发（r0=0x3F duration=8, 见 FUN_080147D8 调用）
  bl FUN_08015138                         @ ???
  bl FUN_080156AC                         @ ??? 可能是资产装载
  movs r0, #0; bl FUN_08019554            @ 状态机前置 tick（state=0）

  strb r4, [0x0202348C]                   @ 清 EWRAM 标志
  movs r0, #1; return
```

**证据等级**：完整拼出了 state B 的所有 IO 值（DISPCNT + BG0~BG3CNT），可一票锁定。

### 5.3 状态机表

FUN_08017574 在 `asm/all.s` 中没有直接 `bl` 调用（0 命中）。搜索 `.word 0x08017575`（THUMB 指针）在原始 ROM 里找到**唯一**一处：ROM `0x01E588B8` = **GBA `0x09E588B8`**。

该位置是一个 **4 项函数指针表**：

```
0x09E588B8:  0x08017575  → FUN_08017574  (init 入口 = state[0])
0x09E588BC:  0x080180AD  → FUN_080180AC  (state[1]——资产/OAM 装载，可能"load assets"阶段)
0x09E588C0:  0x08019495  → FUN_08019494  (state[2]——主循环)
0x09E588C4:  0x080194ED  → FUN_080194EC  (state[3]——exit/finalize)
0x09E588C8:  0x00000000   (sentinel)
```

调度器 `FUN_08019574`（`asm/all.s:11278`）以 `ldr r1, =0x09E588B8`（行 11327）为基址，从 IWRAM 状态字（位 8..15）取 state ID，`table[state]()` 分派。

### 5.4 页面内其它关键数据

表前 8 项（`0x09E58898..0x09E588B8`）是 **ROM 数据指针**（指向 `0x09E3B0XX` 区），解码发现那些地址存储的是 **按 8-byte 条目排列的 XX 编码字符对**（片假名/平假名键位映射）——即这个键盘上显示的字符表。XX 编码见 `doc/dev/xx-encoding-analysis.md`。

---

## 六、端到端加载流水线（推断）

```
┌─ 标题页（state A）─────────────────────────────────────┐
│ 按 START                                              │
└──┬────────────────────────────────────────────────────┘
   ↓
┌─ "Enter your name." 对话框 ───────────────────────────┐
│ （短转场，4 层 + OBJ，DISPCNT 仍为 0x1B40 或类似）    │
│ 按 A                                                  │
└──┬────────────────────────────────────────────────────┘
   ↓
┌─ state_id = 0 → FUN_08017574 ─────────────────────────┐
│ ① 写页状态 struct（0x02029250）                       │
│ ② 配置 IO：DISPCNT=0x1F40 + BG0/1/2/3CNT             │
│ ③ 触发淡入 (FUN_080148D0)                             │
│ ④ 连续 bl 3 个 setup helper                           │
│ ⑤ 推进状态机：FUN_08019554(state=0)                  │
└──┬────────────────────────────────────────────────────┘
   ↓ 下一帧
┌─ state_id = 1 → FUN_080180AC ────────────────────────┐
│ 装载 OBJ 资产（name_o_01.*）+ 初始化 OAM             │
│ 这里应该是 FS loader 真正被调用的地方                │
│   → load_fs(FID=259) → OBJ animation (RNAN)         │
│   → load_fs(FID=260) → OBJ cell (RECN)              │
│   → load_fs(FID=261/262) → OBJ tile (RGCN)          │
│   → load_fs(FID=263/264) → OBJ palette (RLCN)       │
│ 装载 BG 资产：                                        │
│   → load_fs(FID=255..258) → 4 个 .gbtn (NTBG)       │
│   → 拆出 PALT → PALRAM BG pal                        │
│   → 拆出 BGDT → CBB3 tile 池 + SBB28-31 tilemap     │
└──┬────────────────────────────────────────────────────┘
   ↓ 稳态
┌─ state_id = 2 → FUN_08019494 ────────────────────────┐
│ 主循环：处理键盘光标、A/B/START 输入、文字回显       │
└───────────────────────────────────────────────────────┘
```

**未完成部分 / 已解决（2026-04-24 补）**：

### ~~1. 定位通用 FS 装载函数~~ ✓ 已解决
**FS 装载函数 = `FUN_08014FA8` @ `0x08014FA8`**（按**文件路径字符串**查找，不是按 FID 索引）。

调用约定：
```c
uint8_t* fs_load(const char* path, int flag);   // r0=path, r1=flag
```

内部流程：
1. 用 `FUN_08014EB4`（字符串处理，类似 strchr）+ `FUN_0810F090`（类似 strcpy）解析路径（拆 `/` 前后的目录/文件名）
2. 调 `FUN_08014F54` 二级查找定位 FID
3. `r4 = FID`；`r5 = fs_data_base = [fs_header + 0x10] + fs_header`
4. `file_compressed_addr = r5 + offset_table[FID]`（entry 以 u32 存）
5. 调 `FUN_08014600`（**游戏自定义 LZ77/LZ5 解压器**，不是 BIOS SWI 0x11）
6. 返回解压后缓冲指针

**代码内联路径字符串布局**（name_input 页）— ROM `0x09E3B360..0x09E3B434`：
```
0x09E3B360 (27B): "name_input/name_o_01.LZncer"
0x09E3B37C (27B): "name_input/name_o_01.LZnanr"
0x09E3B398 (27B): "name_input/name_o_01.LZncgr"
0x09E3B3B4 (27B): "name_input/name_o_01.LZnclr"
0x09E3B3E0 (26B): "name_input/name_b_01.LZ5bg"
0x09E3B3FC (26B): "name_input/name_b_02.LZ5bg"
0x09E3B418 (26B): "name_input/name_b_04.LZ5bg"
0x09E3B434 (58B): "anmID < IG2D_GetAnmSequencesCount(pThis->pAnimBank[anmID])"  ← NNS debug assert
```
最后一行泄露 **Nintendo NITRO g2d 库** 签名，确认 .LZnanr/.LZncer 走 `IG2D_*` API。

**FS master struct @ `0x09E61178`**（20 B header，紧接 file-paths）：
| Offset | Value | 含义 |
|---|---|---|
| +0x00 | `0x00000153` | file_count = 339 |
| +0x04 | `0x00000014` → `0x09E6118C` | paths 区基址 |
| +0x08 | `0x00002A74` → `0x09E63BEC` | offset_table entry[1]（跳过 sentinel） |
| +0x0C | `0x00002FC0` → `0x09E64138` | size_table entry[1] |
| +0x10 | `0x0000350C` → `0x09E64684` | fs_data 基址 |

**路径字符串直接嵌在代码 DAT 字面量池**：`FUN_080180AC`（name_input 页 state[1]）的 DAT_08018198 / 0x1A0 / 0x1A4 分别是 `"name_input/name_b_01.LZ5bg"` / `"name_input/name_b_02.LZ5bg"` / `"name_input/name_b_04.LZ5bg"` 的 ASCII 内联字符串。代码通过 `ldr r0, =string; bl FUN_08014fa8` 加载。这是**非常自文档化的设计**——逆向时直接 grep ASCII 路径就能定位所有使用点。

### ~~2. 4 个 `.gbtn` ↔ BG 层 1:1 对号~~ ✓ 部分解决

关键踩坑：`.gbtn` 的 BGDT 段 meta 是 **20 B（不是 16 B）**，起始 4 B flags + 4 B tilemap_size + 2×(w,h u16)×2 组 + 4 B extra。之前按 16 B 算导致 tilemap 偏移错 4 字节。修正后：

| .gbtn | dim | tile 数 | BG 层 | VRAM tile 基址偏移 |
|---|---|---|---|---|
| `name_b_01.gbtn` | 30×32 | 8 | **BG3 SBB31 @ `0x0600F800`** | tile_idx + 31 → CBB3 tile #31+ |
| `name_b_02.gbtn` | 30×20 | 24 | **BG2 SBB30 @ `0x0600F000`** | tile_idx + 1 → CBB3 tile #1+ |
| `name_b_03.gbtn` | 30×20 | 11 | 非当前活动 BG | 路径**未在 name_input 代码内联**，但 tile 数据在 VRAM CBB3 tile #8+ — 来源待查（可能其它页加载后残留，或 Ja 版/其它 region 走不同 codepath） |
| `name_b_04.gbtn` | 30×20 | 18 | 非当前活动 BG | 代码内联 `"name_b_04.LZ5bg"`（见 ROM `0x09E3B418`），tile 数据在 VRAM CBB3 tile #61+；tilemap 未激活，推测为**键盘页面切换备用资源** |

验证方式：字节级匹配（`match_gbtn_tilemaps.py`）—— 1 和 2 两个文件的 tilemap 在修正后对目标 SBB 达到 **100% 非零 entry 匹配**（840/840 和 584/584）。所有 4 个 .gbtn 的 tile 图形本体在 CBB3 都能找到（用第一非零 tile 在 CBB3 做字节 search）。

推断：name_b_03 和 name_b_04 是键盘**页面切换**时的替代版本（例：大写/小写/符号 toggle），只改 tilemap 不重上传 tile。

### ~~3. `.LZ5bg` 解压算法~~ ✓ 已解决（2026-04-24，纠正误判）

**真相**：`.LZ*` 全部用 **标准 BIOS SWI 0x11 (LZ77UnCompReadNormalWrite8bit)** 解压，不是游戏自写算法。

原先误把 `FUN_08014600` 当作解压器，实际它是 **`cpu_copy_auto`** — 按大小自动选 SWI 0xB（CpuSet）或 SWI 0xC（CpuFastSet）的 memcpy 包装。真正的解压在 `fs_load (FUN_08014FA8)` 内部分支：
```
LAB_080150BA (asm/all.s:3676+):
    adds r0,r4,#0              @ r0 = compressed src
    adds r1,r5,#0              @ r1 = dst = 0x0200AF20 (EWRAM buffer)
    bl   bios_lz77_uncomp      @ FUN_0810E41C = SWI 0x11
    adds r0,r5,#4              @ *** skip 4 B ***（see below）
    ...
```

**关键陷阱**：LZ77 输出前 4 字节是**压缩工具多塞的前缀**（内容 = LZ77 header 把 type nibble 清零的副本，如 `00 ec 0c 00`），fs_load 用 `add r0, r5, #4` 跳过它。Python 端必须一致 strip 这 4 字节才能 byte-identical。

**Python 解压器**：`tools/fs-decompress.py`（274 行）
- `lz77_decompress(bytes) -> bytes` — 标准 BIOS LZ77 实现
- `decompress_one_fid(rom, fs, fid)` — FID-based 解压 + 自动 strip 前 4 B
- CLI 模式：
  - `python tools/fs-decompress.py <in.LZ*> <out>` 单文件
  - `python tools/fs-decompress.py --all --out fs-decompressed-pyz/` 全 FS 导出
  - `python tools/fs-decompress.py --verify` 与 `temp/fs-decompressed/` 对比

**验证**：**89/89 LZ77 文件与 mGBA runtime dump byte-identical**（对比 250 个非压缩 .ydc/.ydq 直接 passthrough）。

**影响**：`temp/fs-decompressed/` 的依赖彻底消除，**纯静态 `roms/2343.gba + tools/fs-decompress.py` 就能重现任何 FS 文件**，无需再跑 mGBA。

### 4. `temp/fs-decompressed/` 的来源
**该目录由 `FUN_08014FA8` 实时解压产生**，`tools/` 下目前没有对等的 offline 解压脚本——需要补。

### ~~5. init 序列 4 个 helper 命名~~ ✓ 已解决（2026-04-24）

读每个 helper 只要 10-30 行，+ 两条硬证据（ASCII 源文件名 + assert 条件）：

```
name_input_page_init (FUN_08017574):
  ① FUN_0810E3F8           = DMA_memcpy (初始化 page state struct 从 ROM 模板)
  ② gl_clear_vram_palram_scroll (FUN_08014638)
     - memset VRAM 0x06000000 (96 KB), memset PALRAM 0x05000000 (1 KB)
     - 8 个 BGxHOFS/BGxVOFS 寄存器置零
  ③ <5 个 IO register strh: DISPCNT + BG0/1/2/3CNT>
  ④ gl_set_brightness(0x3F, -16)  (FUN_080146FC)  → 全黑
     - 字符串证据：ROM 0x09E398DC = "GL/GL_Common.c"
     - 字符串证据：ROM 0x09E398EC = "bright >= -16 && bright <= 16" assert
  ⑤ gl_fade_in (FUN_080148D0)         → 启动 8 帧渐亮到 bright=0
  ⑥ gl_state_init (FUN_08015138)      → 清 EWRAM GL state @ 0x02023490
  ⑦ gl_clear_frame_callbacks (FUN_080156AC) → 清 IWRAM 动画回调 3 个槽
  ⑧ page_state_dispatcher(state=0)
```

→ **"GL" 前缀 = 游戏自己的 Graphics Library**（非 Nintendo NITRO，而是卡普空/KCEJ 内部的 GameLib 命名空间）。所有 BG/OBJ/palette/fade 的底层抽象都在 `GL_Common.c`（源文件名泄露）。

### ~~6. pass_input 页对称性验证~~ ✓ 已解决（2026-04-24）

`pass_input` 的**完全同构**内联路径字符串块：
```
ROM 0x09E3C5B4  "pass_input/pass_o_01.LZncer"   (27B)
ROM 0x09E3C5D0  "pass_input/pass_o_01.LZnanr"   (27B)
ROM 0x09E3C5EC  "pass_input/pass_o_01.LZncgr"   (27B)
ROM 0x09E3C608  "pass_input/pass_o_01.LZnclr"   (27B)
ROM 0x09E3C634  "pass_input/pass_b_01.LZ5bg"    (26B)
ROM 0x09E3C650  "pass_input/moziire_b_01.LZ5bg" (29B)  ← moziire = "文字入れ" (text entry)
```

与 name_input 布局完全同构，只是文件集合不同：
- pass_input 有 `pass_b_01 + moziire_b_01` 两个 BG（共 2 个 .LZ5bg）
- name_input 有 `name_b_01/02/04` 三个 BG

**pass_input 的代码位于 asm/all.s 未反汇编区** `ROM_INCBIN 0x19C44, 0x858`（位于 FUN_08019b4c 和 FUN_0801a49c 之间）。Ghidra 跳过了这段（FUN_0801a49c 的 DAT 块反向引用了这里，但没自动触发反汇编）。Python 扫描发现至少 13 个 push 函数起点：0x08019C48, 0x08019CA4, 0x08019D14, 0x08019DA4, 0x08019E2C, 0x08019ED4, 0x08019F24, 0x08019F78 等。

**DAT 指针块 @ 0x0801A460..0x0801A47F**（属于该区末尾函数的字面量池）：
```
0x0801A460: .word 0x000005AC           ← length / count
0x0801A464: .word 0x09E3C634           ← "pass_input/pass_b_01.LZ5bg"
0x0801A468: .word 0xFFFFC07F
0x0801A46C: .word 0x09E3C650           ← "pass_input/moziire_b_01.LZ5bg"
0x0801A470: .word 0x09CCD290           ← 共享 ROM 数据（同 name_input FUN_080180AC DAT_08018228）
0x0801A474: .word 0x05000020           ← PALRAM BG offset 0x20
0x0801A478: .word 0x04000008           ← BG0CNT IO
0x0801A47C: .word 0x05000220           ← PALRAM OBJ offset 0x20
```

与 name_input 的 `FUN_080180AC` DAT 块（0x08018228..0x08018244）**使用相同的 4 个共享常量**（0x09CCD290 / 0x05000020 / 0x04000008 / 0x05000220）——强证据说明 **pass_input 和 name_input 是同一代码模板的复制**。

**方法论抽象**：
1. 内联路径字符串块永远紧邻在代码/数据边界，集中放置（name_input 在 `0x09E3B360..`, pass_input 在 `0x09E3C5B4..`，间距约 4 KB）
2. 每组字符串紧跟一小段 DAT（其它 IO 常数 + EWRAM/PALRAM 目标地址），再然后就是**该页面的 init/asset-load 函数**
3. 跨页面共享常量值（如 `0x09CCD290 / 0x05000020 / 0x04000008 / 0x05000220`）是**同一代码模板**的指纹——grep 它们就能枚举所有使用此模板的页面

**遗留**：~~Ghidra 需要一次性把 `ROM_INCBIN 0x19C44..0x1A49C` 的 push 起点作为函数入口 force-disassemble~~ ✓ **已完成（2026-04-24）**

脚本：`tools/ghidra-labeling/DisassembleNameInputRegion.py`（Jython，Ghidra 12.x headless 运行）
- **Phase 1**：8 个 THUMB 函数起点 force-disassemble + `createFunction` → `FUN_08019c48/ca4/d14/da4/e2c/ed4/f24/f78`
- **Phase 1.5**：扫 `0x08013000..0x0801A500` 区间内全部 THUMB 指令 ~9,892 条，收集 772 个 PC-rel 数据目标，对尚未定义的 u32-aligned 地址**批量创建 `Dword`** — 解决 "Ghidra 自动 propagation 创建了 SUB_XXX 函数但忘了定义它们的 DAT 引用"的典型坑（57 个新 DAT 定义）
- **Phase 2**：7 个 spec 数据 label（`fs_master_struct`、`name_input_state_table`、`name_input_path_strings`、`pass_input_path_strings`、`nns_g2d_assert_anmID`、`gl_common_c_filename`、`gl_bright_assert`）

配合第五轮 14 条 `RenameKnownFunctions.py` 追加（`fs_load` / `fs_lz_decompress` / `name_input_page_*` / `gl_*` / `page_state_dispatcher`），再生成的 `asm/all.s`：
- 376,020 → 377,125 行（+1,105 行 = 13 pass_input 函数反汇编 + DAT 定义）
- `bl FUN_08014fa8` → `bl fs_load`（19 处）
- `bl FUN_080146fc` → `bl gl_set_brightness`（25 处）
- `name_input_page_init` 顶层可读，`bl gl_clear_vram_palram_scroll` 等立即显意义

**pass_input 区覆盖情况**：
- 原 `ROM_INCBIN 0x19c44, 0x858`（2136 B）→ **完全消失**
- 新反汇编 13 个 pass_input 函数（FUN_08019c48 / ca4 / d14 / da4 / e2c / ed4 / f24 / f78 / fe4 / FUN_0801a16c / 1ac / 230 / 328）
- 仅剩 234 B 边角料 incbin（`0x19640 0xc0` 预存在 + `0x197ca 0x12` + `0x1a154 0x18`）→ **89% 反汇编覆盖率**

**全 code 范围 DAT 定义**（Phase 1.5 最终版）：扫 `0x080000C0..0x084C7637` 全 294,493 条指令，收集 21,317 个数据引用目标，对 u32-aligned 未定义目标批量创建 Dword → **总共新增 567 个 DAT 定义**（含初次 57 + 全范围 sweep 510）。

**build byte-identical 验证通过** — 两次 `roms/2343.gba` vs `output/2343.gba` 全字节相同（8 函数批 + 13 函数批各一次）。方法论闭环：**`scan_region_define_data()` 可作跨任务通用 helper**。

---

---

## 七、方法论回顾

本次分析走的是 `asset-location.md` §二 **动态路径六步** 的教科书流程，完全照搬成功：

| 步骤 | 本次产出 |
|---|---|
| ① A/B 快照 | 冷启 title + name_input 两态 VRAM/PALRAM/IO/OAM 全采 |
| ② VRAM diff | 21 个区间，最大 10 KB 在 CB0，其次 CB3 7KB |
| ③ IO 解码 | 明确 "三 BG 共享 CBB3 8bpp" 不寻常配置 |
| ③.5 归属 | 4 层 tilemap 分占 SBB28/29/30/31；tile 池在 CBB3 |
| ④ 强指纹 | `0x1F8F` 全 ROM 唯一 .word → FUN_08017574 一击命中 |
| ⑤ 爬升 | 从 init 函数反查找到 4-entry state table @ 0x09E588B8 |
| ⑥ 字面量验证 | FUN_08017574 字面量池含全部 5 个 IO 值（DISPCNT + BG0~3CNT） |
| ⑦ 目视 | byte-for-byte 对齐：name_b_02.gbtn[0x6E8] == VRAM[0x0600C040] ✓ |

**亮点**：`asset-location.md` §二·D "DISPCNT 差异位组合" 方法论完美应用——state A → B 的 DISPCNT 变化 `0x1B40 → 0x1F40`（BG2 位启用）本身是一个页面切换时机指纹；而 BGxCNT 16 位常数的唯一命中（特别是 `0x1F8F`）提供了"一击命中"的强指纹，无需多轮筛选。

---

## 八、本次遗留文件

| 位置 | 内容 | 状态 |
|---|---|---|
| `doc/temp/A_*.bin`, `B_*.bin` | VRAM/PALRAM/IO/OAM 快照（A/B 两态） | gitignored |
| `doc/temp/A_screen.png`, `B_screen.png` | 屏幕截图 | gitignored |
| `tools/ad-hoc/diff_home_vs_name.py` | VRAM/PALRAM/OAM diff 工具 | 入库 |
| `tools/ad-hoc/match_name_input_vram.py` | FS 文件 ↔ VRAM 匹配 | 入库 |
| `tools/ad-hoc/match_gbtn_segments.py` | .gbtn 段切分 + 字节匹配 | 入库 |
| `tools/ad-hoc/find_name_input_bgcnt.py` | asm/all.s BGxCNT 指纹搜索 | 入库 |

`roms/2343.sav` 分析期间曾临时移到 `doc/temp/2343.sav.backup`，分析结束后已复位。
