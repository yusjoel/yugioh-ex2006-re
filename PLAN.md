# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

---

## ✅ P1：卡图 ROM 定位（已完成 2026-04-15）

成果：`tools/rom-export/export_card_images.py` + `doc/dev/card-image-export.md` + `doc/dev/p1-phase-b2-findings.md`；
2331 张大卡图 PNG（card_id 0..2097，覆盖全部 2331 个独立 tile_block）。

---

## 🟡 P2：卡牌列表小图调查（2026-04-15 静态路径完成，palette 遗留）

卡组构筑界面的**小卡图**实际位置 **`0x01326280`**（旧文档 `0x01000000` 错误），
stride **1152 B**，3×6 tile row-major = **24×48 像素** 8bpp，目标 OBJ VRAM
`0x06010000`。调查详情见 `doc/dev/card-list-image-export.md`。

- [x] **P2-1**：~~mGBA 动态~~ — MCP bridge 反复无法启动，改走纯静态
- [x] **P2-2**：`FUN_080c33bc` @ `asm/all.s` L231102 完整反汇编；tile base +
      index table + VRAM 目标全部定位
- [x] **P2-3**：`card_id ↔ tile_block` 映射与大卡图**完全共享**同一索引表
      `0x015B5C00` 同公式 `tile_block = u16[base+(card_id*2+flag)*2]`
- [x] **P2-4**：`tools/rom-export/export_card_list_images.py`（2108 张灰度 PNG）
- [x] **P2-5**：旧区 `0x01000000..0x01326280`（3.3 MB）**不是卡图**（是 UI/
      字体/其他资产，结构未知）。真正的小卡图区从 0x01326280 起

- [ ] **P2-palette**（遗留）：OBJ 256 色调色板 ROM 源未定位。候选路径
      见 `card-list-image-export.md` §"未解决：调色板"

> 原 T6.1/T6.2（大卡图调色板与 index 映射）已由 P1 完成并覆盖。

---

## doc/ 文档 ROM 数据落地状态审查（2026-04-14 更新）

> 审计范围：`doc/um06-deck-modification-tool/` + `doc/um06-romhacking-resource/` 两目录共 16 份文档。
> 数据点按 doc 中出现的 ROM 地址分类。非 um06 来源的数据（如 `data/card-names.s` / `data/card-stats.s`）不纳入本表。

### ✅ 已落地

| 文件 | 数据类型 | ROM 地址范围 | 已落地到 |
|------|----------|-------------|---------|
| `um06-deck-modification-tool/home.md` | 预组/初始/对手卡组地址索引 | 多处 | `data/struct-decks.s` / `data/starter-deck.s` / `data/opponent-decks.s` |
| `um06-deck-modification-tool/starter-opponent-paste-tool.md` | 卡组地址索引（与 home.md 重复） | 同上 | 同上 |
| `um06-deck-modification-tool/structure-deck-paste-tool.md` | 预组指针表 | `0x1E5FD54~0x1E5FD84` | `data/struct-decks.s` |
| `um06-romhacking-resource/modifying-banlists.md` | 禁卡表（8 版本共 487 条） | `0x1E5EF30~0x1E5F6CA` | `data/banlists.s` |
| `um06-romhacking-resource/tool-development.md` | 预组指针地址（参考） | `0x1E5FD54` 等 | `data/struct-decks.s`（指针已含） |
| `um06-romhacking-resource/opponents-coinflip-screen.md`（对手卡值） | 对手卡值（27 × 32 B） | `0x1E58D0E~0x1E5906D` | `data/opponent-card-values.s` |
| `um06-romhacking-resource/opponents-coinflip-screen.md`（对手大图 + 小图标） | 27 对手 Top/Bottom Tilemap + 两份 palette_copy + top/bottom tiles 整块 + 27 小图标 tiles/palette | `0x1B101AC~0x1B8FB8B`（大图）+ `0x188DA70~0x189672F`（小图标） | `graphics/opponents/*.bin` + `graphics/icons/*.bin`（由 `tools/rom-export/export_gfx.py` 导出，`asm/rom.s` L126–260 完成 incbin 拆分） |
| `um06-romhacking-resource/deck-string-name-tool.md` | 卡组名字符串 + 指针表（EN） | `0x1DC9F48~0x1DCC7BF` | `data/game-strings-en.s`（含标签） |
| `um06-romhacking-resource/modifying-decks.md` | 卡组名字符串 + 指针表（EN，同上） | 同上 | 同上 |
| `um06-romhacking-resource/duel-field.md`（场地主图形） | 6 模式 × Inner/Outer × image/palette/tilemap/lp_tilemap | `0x1855030~0x1867540` | `graphics/duel-field/*.bin`（`asm/rom.s` L43–119 完成 incbin 拆分） |
| `um06-romhacking-resource/duel-field.md`（HUD 元素） | Life Points Font / Phase Highlights Palette / Phases Highlight / Phases Tilemap 指针表 / Phases Map | `0x1850B1C` / `0x18515DC` / `0x18519FC` / `0x1859548` / `0x185B184` | `graphics/duel-field/hud_*.bin`（由 `tools/rom-export/export_gfx.py` 导出，`asm/rom.s` 对应段 incbin 拆分） |

### ⚠️ 有 ROM 数据但未落地

| 优先级 | 文件 | 数据类型 | ROM 地址 | 说明 |
|--------|------|----------|----------|------|
| ⭐⭐ 中 | `um06-romhacking-resource/opponents-coinflip-screen.md`（Coinflip 界面） | Coinflip Top Bar / Coin & Box / Flipping Animation / "Coin Toss Selection" Text | `0x18977F8` / `0x194D71C` / `0x194F83C` + 对应 tilemap/palette | 翻硬币界面的 4 类图形资源 |
| ⭐⭐ 中 | `um06-romhacking-resource/opponents-coinflip-screen.md`（Theme Duel 大图） | 27 对手 × Top/Bottom Large Wallpaper + palette | `0x1A1DFAC` 起（密集） | 主题决斗背景图，结构类似对手大图但属独立区段 |
| ⭐ 低 | `um06-romhacking-resource/main-menu.md` | 主菜单背景（4bpp） + 主菜单图标（8bpp） | `0x1CF009C` / `0x1CF8B94` | 仅 2 条地址，图标为 8bpp 需特殊解码 |
| ⭐ 低 | `um06-romhacking-resource/banlist-code-breaking.md` | 禁卡密码界面图形 | `0x1E22874`（Tilemap） / `0x1E314B4`（调色板） | 2 处地址 |
| 🔧 特殊 | `um06-romhacking-resource/title-screen.md` | 标题画面 LZ77 压缩块 | `0x1EC33DC` | 需专门工具解压后处理 |
| 🔁 重复 | `um06-romhacking-resource/starter-deck-images-player-icons.md` | 与 opponents-coinflip-screen.md 内容 100% 重复 | — | 已由 coinflip-screen 统一管理，本文件不独立处理 |

### ⭕ 无 ROM 数据

| 文件 | 说明 |
|------|------|
| `um06-deck-modification-tool/toc.md` | 目录导航文件 |
| `um06-romhacking-resource/toc.md` | 目录导航文件 |
| `um06-deck-modification-tool/data.md` | 4072 条卡牌数据库（密码/卡名），纯查询参考，非 ROM 字节结构 |

---

## 图形资产管线

- [ ] **T2.3**：实现 `tools/import_gfx.py`（PNG → 4bpp tiles + tilemap.bin → 写回 ROM）。依据 T2.1/T2.2 已完成的导出管线反向实现。
- [ ] **T-COINFLIP**：Coinflip 界面图形（Top Bar / Coin & Box / Flipping Animation / "Coin Toss Selection" Text）管线与 incbin 拆分
- [ ] **T-THEME**：Theme Duel 大图 27 对手 × Top/Bottom + palette，管线与 incbin 拆分
- [x] **T-HUD**：决斗 HUD 元素（Life Points Font / Phases Highlight / Phase Highlights Palette / Phases Tilemap 指针表 / Phases Map）— 2026-04-15 已落地（`graphics/duel-field/hud_*.bin`）
- [ ] **T4**：主菜单图形（4bpp 背景 + 8bpp 图标）+ 禁卡密码界面图形。需先调查 8bpp 解码与尺寸
- [ ] **T5**：标题画面 LZ77 数据（`0x1EC33DC`，需专门工具解压）

---

## 卡牌数据结构落地

依据：`doc/dev/card-data-structure.md`

- [x] **T6.4**：完整属性/种族编码表 — 2026-04-15 已完成（见 `doc/dev/card-data-structure.md` §一；验证脚本 `tools/ad-hoc/verify_card_enums.py`）

> T6.1/T6.2 由 P1 完成（大卡图）；T6.3 并入 P2；T6.5（属性表汇编化）由
> `data/card-stats.s` + `data/card-names.s` 已完成。

---

## Ghidra 反向标注（2026-04-15 首轮落地）

脚本位于 `tools/ghidra-labeling/`，headless 驱动 `tools/asm-regen/ghidra-run-script.bat`。
命名登记表：`doc/dev/ghidra-function-names.md`。

- [x] **TG.1**：`CardStats`(22B) + `DeckEntry`(4B) 结构体 + `AttrCode/RaceCode/SubtypeCode/SpSubCode` 4 个 enum —— `CreateCardStatsType.py`
- [x] **TG.2**：5170 条 `card_XXXX` + 25 对手卡组 + 12 个文件级锚点 —— `ImportProjectLabels.py`
- [x] **TG.3**：`CardStats[5170]` / `DeckEntry[n]×6` / `byte[2048]` / `ushort[7270]` 应用到对应数据区 —— 与 TG.1 同脚本完成
- [x] **TG.4**（首轮 18 项）：p1/p2 findings 里已知函数批量 rename —— `RenameKnownFunctions.py`
- [x] 配套：`VerifyTgRun.py` 回读验证 + `ExportRangeToGas.py` 修了 Thumb BL 识别（路线 B）

> **副产物**：重导出 `asm/all.s` 后 byte-identical 重建（SHA1 `9689337d…cad9b`）。
> TG.4 的 plate comment 也带进了新 `all.s`，方便后续结合 MCP/mGBA 继续跟调用链。

- [ ] **TG.4-next**（候选）：`FUN_080ee010` (`load_bg_palette_for_card`)、`FUN_0801e640`
      (`card_list_on_select_to_info_page`)、`FUN_080f0cc0` (`clear_text_line_buffer`)、
      `FUN_080f21e8` (`layout_string_row`) 等未命名相邻函数，见命名登记表末尾
