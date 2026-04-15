# 字库定位结果（Phase 2 / 2026-04-15）

**方法论**：`locate-rom-asset-from-vram-diff.md` 六步流程
**前置**：卡牌大图定位 `p1-phase-b2-findings.md`
**目标**：定位《游戏王 EX2006》英文字库 ROM 位置、编码、加载函数

---

## 结论

| 项 | 值 |
|---|---|
| **字库 ROM 基址** | `0x09CCCA90`（ROM 文件偏移 `0x01CCCA90`） |
| **编码格式** | 1bpp 8×8，每 glyph 8 字节，MSB-first，行主序 |
| **字符索引** | `glyph_addr = base + char_code * 8`（直接 ASCII 映射） |
| **每字符加载函数** | `FUN_080f1b60`（THUMB） |
| **字符串渲染器** | `FUN_080f2aa8` 主体 / `FUN_080f2a7c` 薄包装 |
| **行位图写入函数** | `FUN_080f0f70`（被 `FUN_080f1b60` 每行调用） |
| **字符宽度函数** | `FUN_080f02a4`（jump table @ `0x080f02d4`），窄字 5px / 宽字 10-12px |
| **VRAM 提交起点** | `0x06010040`（OBJ sprite tile 2，tile 0-1 预留给图标） |

**调用链**：`FUN_0801e440`（卡牌信息页入口，复用了卡图大图页）→ `FUN_0801e000`（字段区绘制）→ `FUN_080f2aa8`（字符串遍历 + 处理 `\n`/`\r`/`\t`/空格）→ `FUN_080f1b60`（单字符位图读取）→ `FUN_080f0f70`（行 blit 到 line buffer）→ `FUN_080f2e4c`（line buffer → sprite tile VRAM）。

---

## 六步复盘

### ① 双状态快照

- **state1**：ss1 = 卡组列表（少量文字）
- **state3**：state1 → A → A，进卡牌信息页（大段英文效果文本）

VRAM/OAM/Palette/IO 均已 dump 到 `doc/temp/vram_state{1,3}.bin`、`palram_state{1,3}.bin`、`font_state{1,3}.png`。

### ② VRAM Diff（`tools/ad-hoc/diff_vram_font.py`）

合并 gap ≤64 的区间后，最大差异：

| VRAM 区间 | 大小 | 区域 | 解释 |
|-----------|------|------|------|
| `0x06008040-0x0600933F` | 4864 B | BG charblock 2 | 卡牌大图 6bpp → 4bpp（与 p1 相同） |
| `0x0600004C-0x06000933` | 2280 B | BG tilemap | 卡图 + 文本 tilemap |
| **`0x06010005-0x060107FC`** | **2040 B** | **OBJ sprite tile** | **字体渲染产物** |
| 其它 OBJ 区间 ×13 | 总 ~5500 B | OBJ | 次要图标/图层 |

### ③ IO 寄存器（state3）

- `DISPCNT = 0x1F40`：mode 0，BG0/1/2/3 + OBJ 全开，OBJ 1D 映射
- `BG0CNT = 0x0086`（8bpp 卡图层，与 p1 相同）
- 其它 BG 4bpp

OAM：indices 12-63 为文本区（52 个 sprite，shape=horizontal, size=32×8，4 tile/sprite，palette F，tile 索引从 2 开始按 4 步进）。文本走 OBJ 而非 BG。

### ③.5 归属

差异区间 `0x06010005-0x060107FC` 落在 **sprite tile VRAM**（`0x06010000+`），**必然归属 OBJ**。tile 起点 0x06010040 / 0x06010020 边界对齐到 tile 2（tile 0 空白，tile 1 是装饰图标，已预装）。

### ④ 指纹选择

- **关键突破**：`FUN_0801e000`（从 `FUN_0801e440` 调用）字面量池含 `.word 0x06010040`——VRAM 字体起点
- `.word 0x06010040` 全 ROM 仅 **4 处**（强指纹）
- 发现 `FUN_080f2aa8` 有典型字符串遍历指纹（比较 `0x0a`/`0x0d`/`0x09`/`0x20`）
- `FUN_080f1b60` 字面量池含 `.word 0x09ccca90`——直接命中字库 ROM 基址

### ⑤ 调用图爬升

```
FUN_0801e440 (卡牌信息页)
 ├─ FUN_0801d45c (BG0=0x86 配置，p1)
 ├─ FUN_0801d998 → FUN_0801d290 (6bpp 卡图解码，p1)
 ├─ FUN_0801dbdc (?)
 ├─ FUN_080eeb54 (卡片数据查询)
 └─ FUN_0801e000 (字段/描述绘制)
      ├─ FUN_080f0cc0 (line buffer 预清)
      ├─ FUN_080f2a7c → FUN_080f21e8 (字符串布局)
      │   └─ FUN_080f2aa8 (逐字符循环)
      │       ├─ FUN_080f02a4 (宽度查询，jump table @ 0x080f02d4)
      │       └─ FUN_080f1b60 (字符位图读取：base=0x09ccca90)
      │           └─ FUN_080f0f70 (每行 8 像素 blit 到 line buffer) × 8 行
      └─ FUN_080f2e4c (line buffer → sprite tile VRAM @ 0x06010040)
```

### ⑥ 字面量池验证

`FUN_080f1b60` @ `0x080f1b60`：
- `.word 0x09ccca90` @ 0x080f1bb8：**字库 ROM 基址**
- 循环计数 `r9 = 4`，每轮 `ldrh` 读 2 字节 → 8 bytes/glyph
- 每字节 `bl FUN_080f0f70`（渲染 1 行），对应 1bpp 8 列

`FUN_0801e000` @ `0x0801e000`：
- `.word 0x06010040` @ 0x0801e0fc：**VRAM 字体起点**
- `.word 0x09e5f854` @ 0x0801e0f4：卡片数据 / 描述字符串表基址（未深挖）

---

## 离线验证

脚本 `tools/ad-hoc/decode_font.py`：从 ROM `0x09ccca90 + char*8` 读 8 字节，MSB-first 按行解码 1bpp 8×8。

```
char 0x41 'A':    char 0x48 'H':    char 0x57 'W':
.#####..          ##...##.          ##.#.##.
##...##.          ##...##.          ##.#.##.
##...##.          ##...##.          ##.#.##.
#######.          #######.          ##.#.##.
##...##.          ##...##.          ##.#.##.
##...##.          ##...##.          .#####..
##...##.          ##...##.          .##.##..

char 0x30 '0':    char 0x65 'e':    char 0x72 'r':
.#####..          ..####..          ..##.#..
##...##.          .##..##.          ..###...
##...##.          .######.          ..##....
##...##.          .##.....          ..##....
##...##.          ..####..          ..##....
##...##.
.#####..
```

所有测试字符清晰可读，结论成立。

---

## 可复用脚本

| 路径 | 用途 |
|------|------|
| `tools/ad-hoc/diff_vram_font.py` | state1/3 VRAM diff + gap 合并 |
| `tools/ad-hoc/dump_font_tiles.py` | 从 VRAM dump 渲染 sprite tile 为 ASCII art |
| `tools/ad-hoc/search_font_bytes.py` | 在 ROM 里搜 tile 原始字节（识别 "是否压缩" 用） |
| `tools/ad-hoc/decode_font.py` | 从 ROM 按 1bpp 8×8 解码 ASCII 字形 |

---

## 启示

1. 文本走 OBJ sprite（而非 BG）——和卡图复用了同一页面顶层函数，但 BG 层只承载卡图，文字 layer 完全独立。
2. 1bpp 8×8 + 比例宽度渲染：字符按"比例宽度"写进 32×8 sprite 行缓冲，再切片为 4 个 tile，最终写到 VRAM。这解释了为何 sprite tile 的原始字节**无法**直接在 ROM 中搜到——它们是合成产物。
3. 识别"合成产物 vs 原始素材"是关键判断：卡图是原始素材（6bpp 解码后 VRAM == ROM 解码结果），字体是合成产物（tile 字节模式不可能在 ROM 中出现）。后续定位其它资源时要先判断是哪一类。
4. 指纹选择的"一击命中"再次得益于 IO/VRAM 地址作为硬编码立即数出现次数低（`0x06010040` 全 ROM 仅 4 处，比 `0x06010000` 59 处强得多）。
