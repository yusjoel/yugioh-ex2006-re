# Yu-Gi-Oh! Ultimate Masters: WCT 2006 反汇编项目

《Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006》（GBA，ROM 编号 2343，游戏代码 `BY6E`）的反汇编与数据提取项目。
目标是将原始 ROM 逐步分解为结构清晰的汇编源文件，最终能重新汇编出与原始 ROM **完全一致**（byte-identical）的二进制文件。

## 环境要求

- **devkitARM**（包含 `as`、`ld`、`objcopy`）  
  安装路径需在 `PATH` 中，或修改 `build.bat` 指向实际路径  
  推荐安装目录：`<devkitPro安装目录>\devkitARM\arm-none-eabi\bin\`
- **原始 ROM**：将未修改的原版 ROM 放置于 `roms/2343.gba`

## 快速开始

> ⚠️ **构建前置步骤**：`asm/rom.s` 引用 `data/*.s` 和 `graphics/*.bin`，两者**均不纳入版本控制**（由 ROM 脚本重新生成）。clone 仓库后必须先跑：
>
> ```bat
> python tools/rom-export/export_all.py   @ 一键导出 data/ (.s) + graphics/ (.bin/.png)
> build.bat                               @ 汇编、链接并生成 output/2343.gba
> ```

```bat
build.bat    @ 汇编、链接并生成 output/2343.gba
clean.bat    @ 清理编译产物
```

构建流水线：`asm/rom.s` → (as) → `output/rom.o` → (ld) → `output/2343.elf` → (objcopy) → `output/2343.gba`

## 目录结构

```
.
├── asm/
│   ├── rom.s             # 主入口文件，串联所有数据段
│   ├── rom_header.s      # GBA ROM 头部（0x000–0x0BF）
│   ├── crt0.s            # 启动代码（0x0C0–0x0FF）
│   └── all.s             # 前 16MB 反汇编代码
├── data/                 # 结构化的数据区（不含于仓库，由 tools/rom-export/export_all.py 从 ROM 生成）
│   ├── opponent-card-values.s  # 27 个对手卡值块（ROM 0x1E58D0E）
│   ├── banlists.s              # 8 个版本禁卡表，487 条目（ROM 0x1E5EF30）
│   ├── starter-deck.s          # 初始卡组，50 张（ROM 0x1E5F884）
│   ├── struct-decks.s          # 6 套预组 + 指针表（ROM 0x1E5FA58）
│   ├── opponent-decks.s        # 25 套对手卡组（ROM 0x1E6468E）
│   ├── pack-banners.s         # 51 张卡包封面指针表 + .incbin tile（ROM 0x1CCE960）
│   ├── pack-card-lists.s      # 45 个 pack 卡牌列表 + 51 条 pack 信息表（ROM 0x1E5ABFC）
│   ├── card-descriptions.s   # 39 张卡效果描述 + 数据表 + 指针表（ROM 0x1800000）
│   ├── card-image-index.s   # 卡牌大图索引（card_id 0..2098, ROM 0x15B5C00）
│   ├── cards-ids-array.s    # internal_card_id → card_id 反向映射表（ROM 0x15B7CCC）
│   ├── card-name-pointer-table.s  # 12,612 × u32 卡名指针表（ROM 0x15F3A5C）
│   ├── card-effect-text.s   # 2014 张卡效果全文 × 6 语言（ROM 0x15FFF6C）
│   ├── file-paths.s         # 339 条内部文件路径（ROM 0x1E6118C）
│   ├── fs-tables.s          # 内嵌 FS 索引表（offset_table+size_table, ROM 0x1E63BE8）
│   └── duel-puzzles.s       # 35 块决斗题目存档模板（ROM 0x1EB90D8）
├── graphics/             # 图形资产（不含于仓库，由 tools/rom-export/export_all.py 生成）
│   ├── bin/              # ROM 原始二进制，asm/rom.s + data/*.s 通过 .incbin 引用
│   │   ├── card-images/    tiles/ + palettes/          (2331 tile_block × 2)
│   │   ├── duel-field/     tiles/ + palettes/ + tilemaps/  (6 模式 + HUD)
│   │   ├── font/           tiles/font.bin               (英文 1bpp 字库)
│   │   ├── icons/          tiles/ + palettes/           (27 对手小图标)
│   │   ├── opponents/      tiles/ + palettes/ + tilemaps/  (27 大图)
│   │   └── pack-banners/   tiles/ + palettes/           (51 卡包封面)
│   └── images/           # PNG 预览
│       ├── card-images/    card_XXXX[_ocg|_tcg].png
│       ├── duel-field/     <模式>_{inner,outer,outer_lp}.png
│       ├── font/           font_preview.png
│       ├── icons/          <对手>_icon.png
│       ├── opponents/      <对手>_{top,bottom}.png
│       └── pack-banners/   pack_XX_banner.png
├── tools/                # 开发工具脚本（详见下文「工具脚本」）
│   ├── arm-none-eabi-gdb.exe   # GDB 10.2（不入库，手动放入）
│   ├── rom-export/       # ROM → data/*.s、graphics/
│   ├── asm-regen/        # 汇编再生成流水线（Ghidra + inject_modes）
│   ├── ghidra-labeling/  # 反向标注 Jython 脚本（CardStats/enum/label/函数名）
│   ├── mgba-scripts/     # mGBA 环境管理脚本（pre-MCP 备选）
│   └── ad-hoc/           # 探索性脚本，不保证稳定
├── include/
│   └── macros.inc        # 汇编宏：deck_entry、banlist_entry、deck_card、card_stat、pack_card_entry
├── constants/
│   ├── ewram.inc         # EWRAM 变量符号常量（gPlayerName/gMoneyDp/gBanlistPasswordBuffer 等）
│   └── iwram.inc         # IWRAM 变量符号常量（gPrng/gFrameCounter）
├── doc/                  # 研究文档（来自 Google Sheets，转存为 Markdown）
│   ├── um06-deck-modification-tool/   # 卡组修改工具数据
│   └── um06-romhacking-resource/      # ROM 破解资源参考
├── roms/                 # 原始 ROM（不含于仓库）
├── output/               # 编译产物（不含于仓库）
├── build.bat             # 构建脚本
├── clean.bat             # 清理脚本
└── PLAN.md               # 数据汇编化进度计划
```

## 工具脚本

### 数据 / 图形导出

| 脚本 | 作用 |
|------|------|
| `tools/rom-export/export_gfx.py` | ROM → `graphics/opponents/*.bin` + PNG + 调色板 + `graphics/icons/*.png`；构建前必跑 |
| `tools/rom-export/export_pack_banners.py` | ROM → `graphics/pack-banners/*.bin` + 彩色 PNG + `data/pack-banners.s`；构建前必跑 |
| `tools/rom-export/export_pack_card_lists.py` | ROM → `data/pack-card-lists.s`（45 个 pack 共 3,515 条卡牌条目 + 51 条 pack 信息） |
| `tools/rom-export/export_card_descriptions.py` | ROM → `data/card-descriptions.s`（39 张卡效果描述 + 数据表 + 指针表） |
| `tools/rom-export/export_card_data.py` | ROM → `data/card-names.s`、`data/card-stats.s`（2053 卡名、5170 统计条目） |
| `tools/rom-export/export_game_strings.py` | ROM → `data/game-strings-{en,de,fr,it,es}.s`（CP1252 编码） |
| `tools/rom-export/export_card_name_pointer_table.py` | ROM → `data/card-name-pointer-table.s`（12,612 × u32 卡名指针表，按 `card_id*6 + lang` 索引） |
| `tools/rom-export/export_card_effect_text.py` | ROM → `data/card-effect-text.s`（2014 张卡效果全文 × 6 语言） |
| `tools/rom-export/export_card_images.py` | ROM → `data/card-image-index.s` + `data/cards-ids-array.s`（含 `internal_card_id → card_id` 反向映射）+ `graphics/card-images-rom/` |
| `tools/rom-export/export_file_paths.py` | ROM → `data/file-paths.s`（339 条内部文件路径） |
| `tools/rom-export/export_fs_tables.py` | ROM → `data/fs-tables.s`（offset_table 339×u32 + size_table 340×u32，FS 索引表） |
| `tools/rom-export/export_banlists.py` | ROM → `data/banlists.s`（8 个版本禁卡表，487 条目） |
| `tools/rom-export/export_starter_deck.py` | ROM → `data/starter-deck.s`（初始卡组 50 张） |
| `tools/rom-export/export_struct_decks.py` | ROM → `data/struct-decks.s`（6 套预组 + 指针表） |
| `tools/rom-export/export_opponent_card_values.py` | ROM → `data/opponent-card-values.s`（27 对手卡值块，32 B×27） |
| `tools/rom-export/export_opponent_decks.py` | ROM → `data/opponent-decks.s`（25 对手卡组，块大小可变，含融合卡组） |
| `tools/rom-export/export_deck_strings.py` | ROM → `data/deck-strings.s`（XX 编码预组/对手卡组名字符串） |
| `tools/rom-export/export_duel_puzzles.py` | ROM → `data/duel-puzzles.s`（35 块决斗题目存档模板） |

### 汇编再生成流水线

| 脚本 | 作用 |
|------|------|
| `tools/asm-regen/ghidra-export-range.bat` | Headless 调 Ghidra 执行 `ExportRangeToGas.py`，把 ROM 指定地址范围导出为 GAS `.s` |
| `tools/asm-regen/ghidra-run-script.bat` | 通用 headless 驱动，跑 `tools/ghidra-labeling/*.py`（非 `-readOnly`，改动自动保存） |
| `tools/asm-regen/ghidra/ExportRangeToGas.py` | Jython 脚本，在 Ghidra 内遍历地址范围输出带 label/XREFS 的 `.s`，做 `ldr`/`adr`/`b/bl` 语法修正和 `DAT_` 合成；headless 通过 `getScriptArgs()` 传参。**Thumb BL 优先按 hex 指纹识别**（解决 ProgramContext 偶发误判）|
| `tools/asm-regen/inject_modes.py` | Python 后处理：注入 `.arm`/`.thumb` 模式切换（基于 hex 宽度判 THUMB/ARM，并跟随上游已发出的 mode 指令避免冗余），补 Thumb-1 设标志指令的 `s` 后缀（≈14 万处），应用少量硬编码补丁。支持 `<in> [out]` 参数 |

完整工作流（含 2026-04-15 Thumb BL 修正踩坑）见 [`doc/dev/ghidra-function-names.md`](doc/dev/ghidra-function-names.md) §与 asm/all.s 重导出的联动。

### Ghidra 反向标注（`tools/ghidra-labeling/`）

Jython 脚本，通过 `ghidra-run-script.bat` 以 headless 模式跑。命名登记：`doc/dev/ghidra-function-names.md`。

| 脚本 | 作用 |
|------|------|
| `CreateCardStatsType.py` | 在 `/ygo_ex2006` category 下建 `CardStats`(22B) / `DeckEntry`(4B) + `AttrCode/RaceCode/SubtypeCode/SpSubCode` enum，并应用到 `0x098169B6`（CardStats[5170]）等数据区（TG.1+TG.3） |
| `ImportProjectLabels.py` | 扫 `data/*.s` 生成 5170 条 `card_XXXX` + 25 对手卡组 + 12 个文件级锚点（TG.2） |
| `RenameKnownFunctions.py` | 30 个 `FUN_xxx` 语义重命名（TG.4：p1/p2 findings + pack-banner 11 个函数） |
| `LabelPackBanners.py` | 53 个数据标签：调色板 + 指针表 + 51 pack tile（从指针表动态读取地址） |
| `LabelPackCardLists.py` | 46 个数据标签：信息表 + 45 个 pack 卡牌列表（从信息表指针动态读取） |
| `LabelCardDescriptions.py` | 3 个数据标签：描述文本表 + 数据表 + 指针表 |
| `VerifyTgRun.py` | 回读验证：types/arrays/labels/函数名抽样 |

每个脚本支持 `dry` 参数预览改动不落盘。脚本首部必须带 `#@runtime Jython`（Ghidra 12 默认 `.py` 走 PyGhidra）。

### mGBA 环境脚本（`tools/mgba-scripts/`）

MCP 接入之前用于手工管理 mGBA + GDB stub 生命周期，现在保留作为环境验证备选。

| 脚本 | 作用 |
|------|------|
| `local-settings.ps1` | 本机路径（`$mgba`、`$projectRoot`），`.gitignore` 忽略；`.example` 是模板 |
| `_preflight-mgba.ps1` | 公共库（dot-source）：加载 `local-settings.ps1`、关残留进程、检查端口 2345 |
| `start-mgba-gdb-ss1.ps1` | 启动 mGBA + GDB stub + 加载 `roms/2343.ss1` 存档 |
| `start-mgba-gdb-nosave.ps1` | 启动 mGBA + GDB stub，冷启动（不加存档） |
| `wait-mgba-ready.ps1` | 等待端口 2345 LISTENING + 8 秒 CPU 热身（见 `mgba-gdb-stub-pitfalls.md` 坑 2） |
| `stop-mgba.ps1` | 关所有 `mGBA.exe` 实例（不影响 `mgba-live-mcp`） |

### 探索性脚本（`tools/ad-hoc/`）

| 脚本 | 作用 |
|------|------|
| `read_card_image.py` | 从 ROM 给定 GBA 地址读取 BIOS 压缩头，LZ77 可解压并输出灰阶 PNG（无调色板集成，仅用于快速 sanity check） |

## 已完成的数据提取

以下数据区已从 `.incbin` 替换为带注释的可读汇编代码，每条目包含卡牌名称和密码：

| 数据区 | ROM 偏移 | 大小 | 说明 |
|--------|---------|------|------|
| 对手卡值块 | `0x1E58D0E` | 864 B | 27 个对手的卡牌实力值 + 内部文件路径 |
| 禁卡表（8版本）| `0x1E5EF30` | 1948 B | Sept03/Sept04/March05/Sept05 等 |
| 初始卡组 | `0x1E5F884` | 102 B | 50 张牌 |
| 预组（6套）| `0x1E5FA58` | 812 B | Dragon's Roar、Zombie Madness 等 |
| 对手卡组（25套）| `0x1E6468E` | 5048 B | Kuriboh～Raviel 全部对手 |
| 卡包封面图（51张）| `0x1CCE960` | 104,652 B | 指针表 + 51×2048 B 8bpp OBJ tile（32×64 像素） |
| 卡包卡牌列表 + 信息表 | `0x1E5ABFC` | 14,876 B | 45 个 pack 共 3,515 条卡牌条目 + 51 条 pack 信息记录 |
| 卡牌描述文本 + 数据表 | `0x1800000` | 92,598 B | 39 张卡效果描述（6 语言）+ u32 数据表 + 269 条指针表 |
| 卡牌大图索引 | `0x15B5C00` | 8,396 B | card_id 0..2098 的 OCG/TCG tile_block 索引 |
| Cards IDs Array | `0x15B7CCC` | 6,144 B | 3072 × u16，`internal_card_id 4007..7078 → card_id` 反向映射 |
| 卡名指针表 | `0x15F3A5C` | 50,448 B | 12,612 × u32，按 `card_id*6 + lang_id` 索引 |
| 卡牌效果全文 | `0x15FFF6C` | 2,097,300 B | 2014 张卡效果描述（6 语言） |
| 内部文件路径表 | `0x1E6118C` | 10,844 B | 339 条 null 终止路径（deck/*.ydc, titleEx/*.LZncgr 等）|
| 文件系统索引表 | `0x1E63BE8` | 2,716 B | offset_table (339×u32) + size_table (340×u32)，path[i]↔table[i+1]；FS 数据起点 `0x1E64684` |
| 决斗题目存档模板 | `0x1EB90D8` | 41,729 B | 35 块 DUEL QUESTION 数据（INI 风格键值对）|

### 数据格式示例

```asm
@ 预组（真红眼黑龙 ×1）
deck_entry 4088, 1    @ Red-Eyes B. Dragon (密码: 74677422)

@ 禁卡表（限制 1 张）
banlist_entry 4088, 1    @ Red-Eyes B. Dragon (密码: 74677422)

@ 对手/初始卡组
deck_card 4088    @ Red-Eyes B. Dragon (密码: 74677422)
```

宏在 `include/macros.inc` 中定义，`so_code` 使用十进制整数（如 `4088` = `0x0FF8`），编译时自动计算编码。

## 图形资产管线

对手图形（27 个对手的大图壁纸和小图标）采用以下管线管理：

```
roms/2343.gba
  └─ tools/rom-export/export_gfx.py ──► graphics/opponents/
  │                              palette_copy1.bin   调色板块（7776 B）
  │                              <name>_top_tilemap.bin   (1200 B × 27)
  │                              <name>_bottom_tilemap.bin
  │                              <name>_top.png      渲染合成图（240×160，仅预览）
  │                              <name>_bottom.png
  │                          graphics/icons/
  │                              <name>_icon.png     图标（24×24）
  └─ build.bat ──► output/2343.gba
      （通过 asm/rom.s 中的 .incbin 引用 graphics/opponents/*.bin）
```

`graphics/` 目录下所有文件均**不纳入版本控制**，须在构建前运行导出脚本生成。

### 卡包封面条幅图

卡包列表页面（Exchange DP to Pack）显示的 51 张卡包封面图（32×64 像素 OBJ sprite）：

```
roms/2343.gba
  └─ tools/rom-export/export_pack_banners.py
       ├──► graphics/pack-banners/
       │        pack_XX_banner.bin   8bpp tile 数据（0x800 B × 51）
       │        pack_XX_banner.png   彩色预览
       └──► data/pack-banners.s      指针表（.word label）+ .incbin
```

ROM 布局：调色板 `0x510440`（512 B，256 色），指针表 `0x1CCE960`（51×4 B），tile 数据 `0x1CCEA2C`（51×0x800 B）。

### 图形数据 ROM 布局

| ROM 偏移 | 内容 | 大小 |
|---------|------|------|
| `0x1B101AC` | 调色板块（Copy 1 & 2，内容相同） | 7776 B |
| `0x1B1200C` | Top 图块（4bpp，27 个对手） | 221184 B |
| `0x1B4800C` | Top Tilemap（27 × 1200 B） | 32400 B |
| `0x1B51CFC` | Bottom 图块（4bpp，27 个对手） | 221184 B |
| `0x1B87CFC` | Bottom Tilemap（27 × 1200 B） | 32400 B |



- GBA ROM 基址：`0x08000000`，入口点：`0x080000C0`
- 指令集：ARM（32 位）与 THUMB（16 位）混合，游戏代码大部分为 THUMB
- ROM 大小：`0x1FFFF00` 字节（33,554,176 B），构建时必须精确
- `roms/2343.gba` 同时作为数据源和校验基准

---

## 调试工具链

项目已完成调试工具链验证（P0），可通过以下两种方式对运行中的游戏进行动态调试。

### mGBA MCP（截图 / 内存读取 / Lua 注入）

通过 [mgba-live-mcp](https://github.com/penandlim/mgba-live-mcp) 提供的 MCP 工具直接控制 mGBA。

**启动**：
```ps1
# 启动 mGBA 并加载存档
pwsh -File tools/mgba-scripts/start-mgba-gdb-ss1.ps1
```

**已验证工具**（详见 `doc/dev/p0-3-mgba-mcp-feature-validation.md`）：

| 工具 | 功能 |
|------|------|
| `mgba_live_start` | 启动 mGBA 会话 |
| `mgba_live_export_screenshot` | 截图 |
| `mgba_live_input_tap` | 模拟按键 |
| `mgba_live_run_lua` | 注入 Lua 脚本 |
| `mgba_live_read_memory` | 读取指定地址 |
| `mgba_live_read_range` | 读取内存范围 |
| `mgba_live_dump_oam` | 转储 OAM 精灵表 |

> **mGBA MCP 与 GDB stub 可同时工作**（已验证）：两者通过不同端口通信，互不干扰。
> `start-mgba-gdb-ss1.ps1` 启动后可直接附加 MCP 会话（`mgba_live_attach`），
> 同时进行截图/内存读取/按键注入，GDB 连接不受影响。

### GDB MCP（断点 / 寄存器 / 单步执行）

通过 [GDB MCP](https://github.com/pansila/gdb-mcp) 工具，以 MI 协议驱动 GDB 连接 mGBA GDB stub。

**启动顺序**：
```ps1
# 1. 启动 mGBA（带 GDB stub，端口 2345）
pwsh -File tools/mgba-scripts/start-mgba-gdb-ss1.ps1
# 2. 等待 stub 就绪（约 9 秒）
pwsh -File tools/mgba-scripts/wait-mgba-ready.ps1
# 3. 通过 MCP 工具连接（在 AI 助手中调用）
# gdb_init(gdbPath: "tools/arm-none-eabi-gdb.exe")
# gdb_connect(target: "localhost:2345")
```

> ⚠️ 必须使用 `tools/arm-none-eabi-gdb.exe`（GDB 10.2），
> `devkitPro` 自带的 GDB 14.1 与 mGBA stub 不兼容。
> 调用 `gdb_init` 时**不要**使用 `architecture` 参数。

> ⚠️ mGBA GDB stub 为一次性连接：GDB 断开后 stub 永久关闭，每次调试需重启 mGBA。

**已验证工具**（详见 `doc/dev/p0-5-gdb-mcp-integration.md`）：

| 工具 | 功能 |
|------|------|
| `gdb_init` / `gdb_connect` / `gdb_disconnect` | 连接管理 |
| `gdb_set_breakpoint` | 设置断点（支持条件断点） |
| `gdb_list_breakpoints` / `gdb_delete_breakpoint` | 断点管理 |
| `gdb_continue` / `gdb_interrupt` | 执行控制 |
| `gdb_evaluate_expression` | 表达式求值（可读取内存/寄存器） |
| `gdb_command` | 直接执行 GDB MI 命令 |

**已知限制**：mGBA THUMB 代码不支持栈回溯（`gdb_list_frames` 失败）；`gdb_read_memory` 存在解析 bug，可用 `gdb_evaluate_expression` 代替。

### 纯 GDB 脚本方式

适合已知流程的批处理场景（如固定 watchpoint 监听），详见 `doc/dev/scripts/`：

```ps1
tools\arm-none-eabi-gdb.exe --batch -x doc\dev\scripts\gdb_dma_watch.gdb
```

---

## 参考文档

项目 `doc/` 目录下保存了以下研究文档（原始 Google Sheets，转存为 Markdown）：

- **[UM06 Deck Modification Tool 1.0](doc/um06-deck-modification-tool/toc.md)**  
  含完整卡牌数据库（4072 条）、卡组地址表、编码工具
- **[UM06 Romhacking Resource Ver 2.0](doc/um06-romhacking-resource/toc.md)**  
  含图形地址、禁卡表解析、卡组修改方法等 10 个 Sheet

---

## 致谢

感谢 **Scrub Busted**（[@scrubbusted](https://www.youtube.com/@scrubbusted)）对《游戏王 EX2006》ROM 破解研究的开创性贡献，其制作的教程视频和共享文档是本项目数据分析的重要基础。

**教程视频系列（Ultimate Masters ROMHACKING TUTORIAL）：**

| # | 标题 | 链接 |
|---|------|------|
| Part 1 | Graphics - Custom Field Playmat, Custom Palettes | [YouTube](https://www.youtube.com/watch?v=BbPcN3r_QIs) |
| Part 2 | Graphics - Deck Images, 64 Color Palettes, 8bpp | [YouTube](https://www.youtube.com/watch?v=_l0UY5goXLM) |
| Part 3 | MODIFYING DECKS - Starter, Structure & Opponents | [YouTube](https://www.youtube.com/watch?v=KsobsJKv4K8) |
| Part 4 | Tilemap Studio Tutorial - Modify Coin Flip Backgrounds | [YouTube](https://www.youtube.com/watch?v=uLpnGkV1lXs) |

**参考文档（Google Sheets）：**

- [UM06 Deck Modification Tool 1.0](https://docs.google.com/spreadsheets/d/1dXa8EyyL2ozM04TpZb_yAsYO7A98CfKIZacchXT2US8/edit)
- [UM06 Romhacking Resource Ver 2.0](https://docs.google.com/spreadsheets/d/1AIXryyGPMKr43SheXUt_zkncmM9kfl_Xy1vZvJ6bQrg/edit)

感谢 **[Yugipedia](https://yugipedia.com/wiki/)** 社区整理的详尽卡牌数据库和卡包内容列表，为本项目的卡包卡牌列表数据验证提供了重要参考。

感谢 **[TCRF Data Crystal](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006)** 维护的本游戏 ROM/RAM 地图与文本编码表，提供了 `internal_card_id`→`card_id` 反向映射表 (`0x15B7CCC`)、卡名指针表 (`0x15F3A5C`)、若干 EWRAM/IWRAM 变量地址（语言、DP、谜题进度、玩家名、Banlist 缓冲、PRNG 等）以及拉丁扩展字符编码表。本项目据此拆出了 `data/cards-ids-array.s`、`data/card-name-pointer-table.s`，并新建了 `constants/ewram.inc` / `constants/iwram.inc`。

参考资源（已抓取至 `refs/datacrystal-um2006/`）：

| 子页面 | 链接 |
|--------|------|
| ROM map | [datacrystal.tcrf.net](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/ROM_map) |
| RAM map | [datacrystal.tcrf.net](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/RAM_map) |
| Text table (TBL) | [datacrystal.tcrf.net](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/TBL) |
| Notes | [datacrystal.tcrf.net](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/Notes) |

感谢 **[ryosbsk/yugioh-card-search](https://github.com/ryosbsk/yugioh-card-search)** 整理的本作日文卡名 + 卡包归属（按五十音排序的 ~2,000 张卡），为 XX 自定义编码反向工程提供关键对照数据：通过将 ROM `card-names.s` 的 `lang=0` (XX) 字节对与已知 JP 卡名按位对齐，本项目识别出 XX 是 2 字节定长编码，确认 F1/F2 完整片假名表 + F1 平假名表 + F0 全角字母表，约 130+ 字符已映射，全 ROM 37.8% 卡名可完全解码。详见 [`doc/dev/xx-encoding-analysis.md`](doc/dev/xx-encoding-analysis.md) 与解码器 [`tools/xx_codec.py`](tools/xx_codec.py)。
