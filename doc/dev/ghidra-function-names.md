# Ghidra 函数命名登记表

本文件登记《Yu-Gi-Oh! EX2006》(BY6E) 工程中从 `FUN_xxxxxxxx` 重命名后的**已知语义**函数。
批量 rename 脚本：`tools/ghidra-labeling/RenameKnownFunctions.py`（TG.4）。

- 运行后效果：Ghidra 里 `FUN_xxxxxxxx` 会被替换成下表 `新名称`。
- 来源文档以 p1/p2 findings 为主；后续每轮 TG.4 应在此表追加新条目。
- 验证口径：rename 后在 Decompiler 里看调用关系；Plate comment 会同步一条一行说明。

## 本轮（2026-04-15）已命名函数（17 项）

| 原名 (FUN_*) | 新名称 | 地址 | 功能 | 来源 |
|--------------|--------|------|------|------|
| `FUN_0801d290` | `decode_card_image_6bpp` | `0x0801D290` | 6bpp 解码卡牌大图 → BG0 VRAM（800 次循环，每 6 ROM → 8 像素） | p1 §3 |
| `FUN_0801d45c` | `card_info_page_init_bg0` | `0x0801D45C` | 卡牌信息页 BG0 初始化（写 `BG0CNT=0x0086`） | p1 §2 |
| `FUN_0801d998` | `card_image_decode_wrapper` | `0x0801D998` | 读卡片属性 + 调 `decode_card_image_6bpp`（r1=0x10 palette 偏移） | p1 §2 |
| `FUN_0801e440` | `card_info_page_entry` | `0x0801E440` | **卡牌信息页顶层入口**。`card_id = (word0 << 15) >> 18` | p1/p2 |
| `FUN_0801d448` | `card_info_page_enter_with_card_id` | `0x0801D448` | `FUN_0801e640` 首个 `bl` 的目标（带 card_id 参数进入） | p1 推断 |
| `FUN_0801dbdc` | `card_info_page_step_03_unknown` | `0x0801DBDC` | 页面过渡/动画（不写 tile 数据）；细节待 TG.4 后续确认 | p1/p2 |
| `FUN_080eeb54` | `card_data_query` | `0x080EEB54` | 按 `card_id` 查 0x098169B6 卡片属性表；返回 ATK/DEF/type 等 | p2 待细化 |
| `FUN_0801e000` | `render_card_description_text` | `0x0801E000` | 字段区/描述绘制入口；字面量池含 `.word 0x06010040` | p2 §⑤ |
| `FUN_0801e100` | `card_info_page_finalize` | `0x0801E100` | 卡牌信息页最后一个 `bl`，UI 收尾 | p2 §⑤ |
| `FUN_080f2a7c` | `text_render_wrapper` | `0x080F2A7C` | `render_string_to_line_buffer` 的薄包装 | p2 §⑤ |
| `FUN_080f2aa8` | `render_string_to_line_buffer` | `0x080F2AA8` | 逐字符遍历字符串，处理 `\n` `\r` `\t` 空格 | p2 §⑤ |
| `FUN_080f1b60` | `load_glyph_row_pair` | `0x080F1B60` | 从 `0x09CCCA90 + ch*8` 读字形，4 轮 × 2 bytes blit | p2 §⑥ |
| `FUN_080f0f70` | `blit_glyph_row_to_buffer` | `0x080F0F70` | 每字形行 8-bit blit 到 line buffer | p2 §⑤ |
| `FUN_080f02a4` | `get_char_width_class` | `0x080F02A4` | jump table @ `0x080F02D4`，返回字符宽度类别 | p2 §⑤ |
| `FUN_080f0200` | `char_width_narrow_5` | `0x080F0200` | 窄字宽度 5 px | p2 |
| `FUN_080f0210` | `char_width_wide_10_or_12` | `0x080F0210` | 宽字宽度 10 或 12 px | p2 |
| `FUN_080c33bc` | `load_card_list_small_image` | `0x080C33BC` | 卡牌列表小图加载（OBJ 8bpp, 1152 B / 条, 24×48） | card-data-structure §三 |
| `FUN_080f2e4c` | `commit_line_buffer_to_sprite_vram` | `0x080F2E4C` | line buffer → `0x06010040+` sprite tile VRAM | p2 §⑤ |

> 表里 18 行是因为 `load_card_list_small_image` 在 p1 表里未列出、实际为独立小图路径。

## 第二轮（2026-04-15）TG.4-next

| 原名 (FUN_*) | 新名称 | 地址 | 功能 | 证据 |
|--------------|--------|------|------|------|
| `FUN_0801e640` | `card_list_on_select_to_info_page` | `0x0801E640` | 卡列表界面按 A 键进入卡牌详情页的派发函数 | 入参 u16 card_id；函数首 `bl` 目标 = `card_info_page_enter_with_card_id`（距入口 22 字节处）|

> **未命名候选（调查后放弃本轮）**：`FUN_080ee010` / `FUN_080f0cc0` / `FUN_080f21e8` 都是通用的状态/bit 字段 setter（写 EWRAM `0x02006ED0` 附近的 struct），在全代码里被调用 40+ 次，不是特定功能的包装，留待更细的逆向。

## 第三轮（2026-04-16）pack-banner

| 原名 (FUN_*) | 新名称 | 地址 | 功能 | 证据 |
|--------------|--------|------|------|------|
| `FUN_080d971c` | `pack_list_page_init` | `0x080D971C` | 卡包列表页初始化（函数指针表 `0x09E4948C[11]`） | 方向 C: BG2CNT=0x1E0D 唯一命中 → 调用图爬升 |
| `FUN_080d8d84` | `pack_list_bg_setup` | `0x080D8D84` | BG 配置（BG0CNT=0x1C00, BG2CNT=0x1E0D）+ 清空 VRAM | 方向 C 直接命中 |
| `FUN_080d8f08` | `pack_list_tilemap_load` | `0x080D8F08` | 从 `0x09CCE2B0/C0/D0` 加载 BG tilemap + BG palette | page_init 第二个 bl |
| `FUN_080d8e98` | `pack_entry_init` | `0x080D8E98` | 逐 pack 初始化（banner tile + name text + detail） | page_init 循环体, hbreak 验证 |
| `FUN_080d8f48` | `pack_banner_obj_setup` | `0x080D8F48` | 按 slot 计算 OBJ VRAM 地址，调 `pack_banner_tile_copy` | 字面量 `0x06014000` |
| `FUN_080db860` | `pack_banner_tile_copy` | `0x080DB860` | ROM 指针表 `0x09CCE960[id]` → OBJ VRAM，mode 1=2D stride | hbreak 验证 5 次调用 |
| `FUN_080dbbc0` | `pack_name_text_render` | `0x080DBBC0` | ROM `0x09E5E2E8` 查包名，`text_render_wrapper` ×2 | 调用 commit_line_buffer |
| `FUN_080bdfac` | `pack_ui_state_machine` | `0x080BDFAC` | 卡包 UI 运行时状态机（7 路 switch），overlay/动画 | 方向 B: `0x06016000` 命中 |
| `FUN_080d8ddc` | `pack_visible_count` | `0x080D8DDC` | 返回当前可见 pack 数（clamp 1..5） | page_init 循环上界 |
| `FUN_080d8f84` | `pack_detail_bg_tile_load` | `0x080D8F84` | EWRAM 记录 → BG VRAM `0x06000240`，含 pack cost | pack_entry_init 后续调用 |
| `FUN_080f74d4` | `tile_2d_row_copy` | `0x080F74D4` | 按行拷贝 tile 到 2D OBJ VRAM（dest stride 0x400），130 次调用 | overlay 加载器使用 |

## 第四轮（2026-04-18）card-list-palette

| 原名 (FUN_*) | 新名称 | 地址 | 功能 | 证据 |
|--------------|--------|------|------|------|
| `FUN_080fdef4` | `card_list_screen_init` | `0x080FDEF4` | 卡列表屏幕初始化序列；4 次 memcpy 加载静态 OBJ 调色板（ROM `0x09E31554/74/14`）；调 `card_list_tile_renderer` | asm/all.s L334094-L334111 静态分析 + PALRAM dump 全字节比对 |
| `FUN_081011c4` | `card_list_tile_renderer` | `0x081011C4` | 卡列表小图 tile 渲染主函数；字面量池含 `0x09326280`（tile 基址）+ `0x095B5C00`（index 表） | 字面量池 DAT_08101290=0x09326280 静态识别 |

## 后续 TG.4 待定项（未命名占位）

从已命名函数的 XREF 继续爬图时，期望命名的候选（优先度高→低）：

- `FUN_080ee010`：`card_image_decode_wrapper` 内部调用，负责**把 64 色卡图 palette 从 ROM 拷到 BG palette VRAM**（参考 p1 §八）。候选名 `load_bg_palette_for_card`。
- `FUN_0801e640`：`card_info_page_enter_with_card_id` 的**外部调用者**（卡牌信息页的真正 caller），应是卡牌列表界面按 A 键进入详情的状态机。候选名 `card_list_on_select_to_info_page`。
- `FUN_080f0cc0`：`render_card_description_text` 内调用，**line buffer 预清**。候选名 `clear_text_line_buffer`。
- `FUN_080f21e8`：`text_render_wrapper` 内唯一调用目标，层数 = 1 的字符串布局辅助。候选名 `layout_string_row`。
- `FUN_0801d290` 的 caller `FUN_0801d998` 还会调 `FUN_0801d860` 之类的小函数（待 Ghidra XREF 面板看）——把它们命名。

## 使用方式（headless，无需打开 Ghidra GUI）

```bat
:: 1) TG.1 + TG.3: 新建类型 (CardStats/DeckEntry + 4 个 enum) 并应用到数据区
tools\asm-regen\ghidra-run-script.bat CreateCardStatsType.py

:: 2) TG.2: 5170 card_XXXX + 25 对手卡组 + 文件级锚点
tools\asm-regen\ghidra-run-script.bat ImportProjectLabels.py

:: 3) TG.4: 18 个已知 FUN_xxx -> 语义名
tools\asm-regen\ghidra-run-script.bat RenameKnownFunctions.py

:: 4) 回读验证 (types / 数组 / label / 函数名抽样)
tools\asm-regen\ghidra-run-script.bat VerifyTgRun.py
```

每个脚本支持 `dry` 参数（`... ImportProjectLabels.py dry`）预览改动不落盘。
驱动脚本基于 `analyzeHeadless.bat`，默认非 `-readOnly`，改动由 Ghidra 自动 `Save succeeded`。

**前置约束**：

- Ghidra 12.0.3 默认把 `.py` 当 PyGhidra，Jython 脚本首部必须带 `#@runtime Jython` 头
- 所有脚本使用 `SourceType.USER_DEFINED`，不会被 Ghidra 自动分析覆盖
- 运行前建议把 `ghidra/Yu-Gi-Oh WCT 2006.rep/` 复制一份（`.bak` 后缀）兜底

## 与 asm/all.s 重导出的联动

TG 改动完成后，重新导出 `asm/all.s` 就能把新函数名/label/类型带到汇编源里：

```bat
:: 范围 084c7637 = all.s 约定上界 (卡图数据段归 rom.s 管理, 不能越界)
tools\asm-regen\ghidra-export-range.bat 080000c0 084c7637 asm\all.s 0
python tools\asm-regen\inject_modes.py
build.bat
```

典型输出：`inject_modes` 注入 0 处模式切换 + 修 140975 处 s 后缀 + 1 处手动补丁，
构建后 `output/2343.gba` 与 `roms/2343.gba` SHA1 一致。

> **历史踩坑**：2026-04-15 首次做 TG 后重导出 `asm/all.s`，GAS 报一堆
> `misaligned branch destination`。根因是 Ghidra ProgramContext 把若干 4 字节
> Thumb BL（`f0 xx yy fd` 等）标成 ARM，`ExportRangeToGas.determine_thumb_mode`
> 盲从 context 返回 False，于是多插了错误的 `.arm`。修法（路线 B）：在
> `determine_thumb_mode` 里把 hex-bytes 指纹识别**放在 ProgramContext 之前**，
> 匹配 `first_hw & 0xF800 == 0xF000` 且 `second_hw & 0xF800 ∈ {0xF800, 0xE800}`
> 直接硬判 Thumb。副效应：`inject_modes.py` 需要修的 s-suffix 从 141015 降到
> 140975，且可以丢掉上游已发出的重复 `.arm`/`.thumb`（inject_modes 内部
> tracker 跟随上游指令，避免 `.thumb\n.thumb` 冗余）。

## 参考

- `doc/dev/p1-phase-b2-findings.md`
- `doc/dev/p2-font-location-findings.md`
- `doc/dev/card-data-structure.md` §一、§三
- `doc/temp/next-session-ghidra-labeling.md`（本轮任务单）
