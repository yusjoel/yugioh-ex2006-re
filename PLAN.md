# Yu-Gi-Oh! Ultimate Masters: WCT 2006 ROM 数据汇编化计划

---

## 🔴 P1（当前焦点）：卡图 ROM 定位

2054 张卡牌图像的 ROM 存储方式与 ID 映射。Phase B2 动态追溯已完成，结果见 `doc/dev/p1-phase-b2-findings.md`；P1 子项状态待专题审阅后回填。

- [ ] **P1-1**：用 GDB watchpoint 监听 DMA3 搬运，捕获卡图 ROM 源地址
- [ ] **P1-2**：判断源数据是 LZ77（magic `0x10`）还是原始 tiles
- [ ] **P1-3**：确认图像 index 与槽位 ID 的精确映射（参照 `doc/dev/card-data-structure.md`）
- [ ] **P1-4**：确认调色板位置与格式（stride 是否 2752 字节）
- [ ] **P1-5**：输出完整调查文档 + 导出脚本 `tools/rom-export/export_card_images.py`

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

### ⚠️ 有 ROM 数据但未落地

| 优先级 | 文件 | 数据类型 | ROM 地址 | 说明 |
|--------|------|----------|----------|------|
| ⭐⭐ 中 | `um06-romhacking-resource/opponents-coinflip-screen.md`（Coinflip 界面） | Coinflip Top Bar / Coin & Box / Flipping Animation / "Coin Toss Selection" Text | `0x18977F8` / `0x194D71C` / `0x194F83C` + 对应 tilemap/palette | 翻硬币界面的 4 类图形资源 |
| ⭐⭐ 中 | `um06-romhacking-resource/opponents-coinflip-screen.md`（Theme Duel 大图） | 27 对手 × Top/Bottom Large Wallpaper + palette | `0x1A1DFAC` 起（密集） | 主题决斗背景图，结构类似对手大图但属独立区段 |
| ⭐ 低 | `um06-romhacking-resource/duel-field.md`（HUD 元素） | Life Points Font / Phases Highlight / Phase Highlights Palette / Phases Tilemap / Phases Map | `0x1850B1C` / `0x18519FC` / `0x18515DC` / `0x1859548` / `0x185B184` | 决斗界面 HUD 相关图形/调色板，场地主图形已落地但 HUD 未处理 |
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
- [ ] **T-HUD**：决斗 HUD 元素（Life Points Font / Phases Highlight / Phase Highlights Palette / Phases Tilemap / Phases Map）
- [ ] **T4**：主菜单图形（4bpp 背景 + 8bpp 图标）+ 禁卡密码界面图形。需先调查 8bpp 解码与尺寸
- [ ] **T5**：标题画面 LZ77 数据（`0x1EC33DC`，需专门工具解压）

---

## 卡牌数据结构落地

依据：`doc/dev/card-data-structure.md`

- [ ] **T6.1**：确认卡牌图像的调色板位置与 stride（是否 2752 字节）
- [ ] **T6.2**：确认图像 index 与槽位 ID 的精确映射
- [ ] **T6.3**：确认图像区起始的 UI 图形（字体/数字）占用多少 entries
- [ ] **T6.4**：完整属性/种族编码表（对照 `doc/um06-deck-modification-tool/data.md` 验证）

> `data/card-stats.s`（5170 条 × 22 字节）和 `data/card-names.s`（卡名字符串表）已落地并由 `asm/rom.s` 引用，T6.5（属性表汇编化）视为完成。

---

## Ghidra 反向标注

- [ ] **TG.1**：确认 `CardStats` struct 字段布局（对照 T6 调查结果）
- [ ] **TG.2**：编写 `ghidra_scripts/ImportProjectLabels.py`，导入字符串和卡组标签
- [ ] **TG.3**：在 Ghidra 中定义 `CardStats` / `DeckEntry` 并应用到数据区
- [ ] **TG.4**（持续）：利用 XREF 反向命名关键函数
