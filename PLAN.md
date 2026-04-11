# 游戏王 EX2006 ROM 数据汇编化计划

## 目标

将 ROM 中已知数据区从 `.incbin` 替换为带结构注释的可读汇编代码，
最终输出与原始 ROM **byte-identical**。

## 数据区总览

| 区块 | ROM 偏移范围 | 大小 | 状态 |
|------|------------|------|------|
| XX语言卡组名（自定义编码） | `0x1DBF01A – 0x1DC461F` | ~10 KB | ✅ `data/deck-strings.s` |
| 游戏文本（EN/DE/FR/IT/ES） | `0x1DC4620 – 0x1DFF9D1` | ~335 KB | ✅ `data/game-strings.s` |
| 对手卡值块（27条目×32字节）| `0x1E58D0E – 0x1E5906D` | 864 B | ✅ `data/opponent-card-values.s` |
| 禁卡表（8个版本共487条目）  | `0x1E5EF30 – 0x1E5F6CB` | 1948 B | ✅ `data/banlists.s` |
| 初始卡组（50张+终止符）    | `0x1E5F884 – 0x1E5F8E9` | 102 B | ✅ `data/starter-deck.s` |
| 预组（6套+指针表）         | `0x1E5FA58 – 0x1E5FD83` | 812 B | ✅ `data/struct-decks.s` |
| 对手卡组（25套）           | `0x1E6468E – 0x1E65A45` | ~5300 B | ✅ `data/opponent-decks.s` |

## 数据编码格式

**预组**：每条 4 字节 = `(so_code * 4 | qty)` LE16 + `0x0000` LE16

**禁卡表**：每条 4 字节 = `so_code` LE16 + `limit` LE16（limit: 0禁止/1限制/2准限制）

**初始/对手卡组**：每条 2 字节 = `so_code` LE16，以 `0x0000` 终止

**对手卡值块**：每条 32 字节 = `card_value`(2) + `unk`(2) + 文件路径字符串(20字节null-padded) + padding(8)

**游戏文本**：Latin-1 编码，null 终止字符串，用 `.string` 指令；见 `doc/dev/latin1-strings-in-gas.md`

## 宏定义（include/macros.inc）

```asm
deck_entry so_code, qty    @ 预组：(so_code * 4) | qty, 0
banlist_entry so_code, limit  @ 禁卡表：so_code, limit
deck_card so_code          @ 对手/初始卡组：so_code
```

**示例**（真红眼黑龙 SO=4088=0x0FF8）：
```asm
@ 旧格式：.hword 0x3FE1, 0x0000
@ 新格式：deck_entry 4088, 1    @ Red-Eyes B. Dragon (74677422)
```

## asm/rom.s 实际布局（按 ROM 偏移排序）

```
incbin [0x1000000, 0x1DBF019]
data/deck-strings.s           @ 0x1DBF01A  XX语言卡组名 + 间隙
data/game-strings.s           @ 0x1DC4620  EN/DE/FR/IT/ES 全部游戏文本
incbin [0x1DFF9D2, 0x1E58D0D]
data/opponent-card-values.s   @ 0x1E58D0E  (+864 B)
incbin [0x1E5906E, 0x1E5EF2F]
data/banlists.s               @ 0x1E5EF30  (+1948 B)
incbin [0x1E5F6CC, 0x1E5F883]
data/starter-deck.s           @ 0x1E5F884  (+102 B)
incbin [0x1E5F8EA, 0x1E5FA57]
data/struct-decks.s           @ 0x1E5FA58  (+812 B)
incbin [0x1E5FD84, 0x1E6468D]
data/opponent-decks.s         @ 0x1E6468E  (~+5300 B)
incbin [end, 0x1FFFF00]
```

## 注意事项

- 每次修改后必须 `build.bat` 验证 **byte-identical**
- `so_code` 统一用**十进制**整数写入 ASM 源码（如 `4088` 代替 `0x0FF8`）
- 卡牌数据来源：`doc/um06-deck-modification-tool/data.md`
- 对手卡值块中 `unk` 字段（0x1F40 起递增）原因未知，保留为 `.hword` 硬编码
- 游戏文本（`data/game-strings.s`）文件编码为 **Latin-1**，勿以 UTF-8 打开覆盖保存

---

## doc/ 文档 ROM 数据落地状态审查（2026-04-11）

### ✅ 已落地（done）

| 文件 | 数据类型 | ROM 地址范围 | 已落地到 |
|------|----------|-------------|---------|
| `um06-deck-modification-tool/home.md` | 预组/初始/对手卡组地址索引 | 多处 | `data/struct-decks.s` / `data/starter-deck.s` / `data/opponent-decks.s` |
| `um06-deck-modification-tool/starter-opponent-paste-tool.md` | 卡组地址索引（与 home.md 重复） | 同上 | 同上 |
| `um06-deck-modification-tool/structure-deck-paste-tool.md` | 预组指针表 | `0x1E5FD54~0x1E5FD84` | `data/struct-decks.s` |
| `um06-romhacking-resource/modifying-banlists.md` | 禁卡表（8版本共 487 条） | `0x1E5EF30~0x1E5F6CA` | `data/banlists.s` |
| `um06-romhacking-resource/tool-development.md` | 预组指针地址（参考） | `0x1E5FD54` 等 | `data/struct-decks.s`（指针已含） |
| `um06-romhacking-resource/opponents-coinflip-screen.md`（部分） | 对手卡值（27 个 × 32 字节） | `0x1E58D0E~0x1E5906D` | `data/opponent-card-values.s` |
| `um06-romhacking-resource/deck-string-name-tool.md` | 卡组名字符串 + 指针表（EN） | `0x1DC9F48~0x1DCC7BF` | `data/game-strings.s`（含标签） |
| `um06-romhacking-resource/modifying-decks.md` | 卡组名字符串 + 指针表（EN，同上） | 同上 | 同上 |

### ⚠️ 有 ROM 数据但未落地（pending）

| 优先级 | 文件 | 数据类型 | ROM 地址范围 | 说明 |
|--------|------|----------|-------------|------|
| ⭐⭐ 中 | `um06-romhacking-resource/opponents-coinflip-screen.md`（剩余） | **对手图形地址指针表** | `0x1B1200C` 等（27 对手 × Top/Bottom + 27 个小图标） | 可提取为带注释的 `.word` 指针表，方便后续图形替换 |
| ⭐⭐ 中 | `um06-romhacking-resource/starter-deck-images-player-icons.md` | **同上**（与 coinflip-screen.md 完全重复） | 同上 | 重复文档，以 coinflip-screen.md 为准 |
| ⭐ 低 | `um06-romhacking-resource/duel-field.md` | **决斗场地图形地址表** | `0x185D720` 等（前 16MB，6 种模式） | 各模式内场/外场的图块/Tilemap/调色板地址及指针表地址 |
| ⭐ 低 | `um06-romhacking-resource/main-menu.md` | **主菜单图形地址** | `0x1CF009C`（背景）`0x1CF8B94`（图标） | 仅 2 条地址，数据极少 |
| ⭐ 低 | `um06-romhacking-resource/banlist-code-breaking.md` | **禁卡密码界面图形地址** | `0x1E314B4`（调色板）`0x1E22874`（图块） | 共 2 处地址 |
| 🔧 特殊 | `um06-romhacking-resource/title-screen.md` | **LZ77 压缩图形块** | `0x1EC33DC` | 标题画面 LZ77 压缩，需专门工具解压后处理 |

### ⭕ 无 ROM 数据（na）

| 文件 | 说明 |
|------|------|
| `um06-deck-modification-tool/toc.md` | 目录导航文件 |
| `um06-romhacking-resource/toc.md` | 目录导航文件 |
| `um06-deck-modification-tool/data.md` | 4072 条卡牌数据库（密码/卡名），纯查询参考，非 ROM 字节结构 |

### 下一步待办（按优先级）

- [x] **T1**：提取游戏文本字符串表（含卡组名）→ `data/deck-strings.s` + `data/game-strings.s`
  - `deck-strings.s`：未知语言（XX，自定义编码）的卡组名，ROM `0x1DBF01A~0x1DC461F`
  - `game-strings.s`：EN/DE/FR/IT/ES 全部游戏文本，ROM `0x1DC4620~0x1DFF9D1`，8218行，Latin-1编码
  - 字符串用 `.string` 指令，Latin-1 扩展字符直接写出（如 `ü ö ä é`）
  - byte-identical 已验证

  > ⚠️ **XX 语言待调查**：指针表第2槽（slot2）指向 ROM `0x1DBF01A`，
  > 内容全为 2字节序列（高字节 `0xF0~0xFF`），疑似自定义字体表索引。
  > 猜测为 GBA 日语版（BY7J）残留数据或某亚洲发行版本。
  > 后续任务：调查游戏字体表，对照 BY7J ROM（如有）确认编码。

- [ ] **T2**：对手图形导入/导出管线（参考 pokeruby/gbagfx 设计）

  #### 背景（调查结论，2026-04-11）

  调查了 pokeruby 成熟 GBA 反编译项目的图形管线。其核心设计：
  - 源文件为 **图块表 PNG**（tile sheet，非渲染合成图）+ **JASC-PAL 调色板**
  - 构建时 `gbagfx` 将 PNG → `.4bpp` 二进制，再通过 `INCBIN_U8()` 链接进 ROM
  - 优势：导入简单（直接逆向），无需重建 tilemap

  本项目与 pokeruby 的关键不同：数据写回到固定 ROM 偏移（不走链接器），因此流程略有调整。

  #### ROM 数据布局（已验证）

  对手图形数据全部在 ROM `0x1B101AC ~ 0x1B8FB8C`，结构如下：

  | 偏移范围 | 内容 | 大小 | 结构 |
  |---------|------|------|------|
  | `0x1B101AC ~ 0x1B1200B` | 调色板块（Copy 1） | 7776 B | 27 × 288 B |
  | `0x1B1200C ~ 0x1B4800B` | 大图 Top 图块（4bpp） | 221184 B | 27 × 0x2000 B ⚠️ |
  | `0x1B4800C ~ 0x1B4FE9B` | 大图 Top Tilemap | 32400 B | 27 × 0x4B0 B ✅ |
  | `0x1B4FE9C ~ 0x1B51CFB` | 调色板块（Copy 2，与 Copy 1 **完全相同**）| 7776 B | 重复 |
  | `0x1B51CFC ~ 0x1B87CFB` | 大图 Bottom 图块（4bpp） | 221184 B | 27 × 0x2000 B |
  | `0x1B87CFC ~ 0x1B8FB8B` | 大图 Bottom Tilemap | 32400 B | 27 × 0x4B0 B ✅ |

  > ⚠️ Top 图块中第 20 个对手（Elemental Hero Electrum）位于非对齐偏移 `0x1B3899C`（期望 `0x1B3800C`），
  > 故 Top 图块整段作为一个 incbin 保留，不做每对手拆分。
  > ⚠️ 每对手的 288 字节调色板条目内，doc 地址指向条目内特定子调色板偏移（不一定是条目起始），
  > 且调色板有两份完全相同的拷贝；导出时两份均需保存，写回时必须同步。

  此外，小图标数据（也在大 incbin 内）：

  | 偏移 | 内容 | 大小 |
  |------|------|------|
  | `0x188DA70 ~ 0x188F8CF` | 图标图块（4bpp） | 7776 B = 27×9×32 |
  | `0x18963D0 ~ 0x189672F` | 图标调色板 | 864 B = 27×32 |

  #### 文件格式决策（实际实现）

  | 文件 | 格式 | 大小 | 说明 |
  |------|------|------|------|
  | `palette_copy1.bin` | 原始二进制 | 7776 B | 完整调色板块，两份 Copy 引用同一文件 |
  | `*_top_tilemap.bin` | 原始二进制 | 1200 B | 直接 `.incbin` 到 ASM |
  | `*_bottom_tilemap.bin` | 原始二进制 | 1200 B | 同上 |
  | `*_top.png` | 渲染合成图（240×160 RGBA） | — | 供查看/编辑，**不** incbin |
  | `*_bottom.png` | 同上 | — | 同上 |
  | `*_icon.png` | 图标（24×24 RGBA） | — | 同上 |

  > 调色板块内部结构复杂（部分对手共享子调色板，间距不规则），
  > 暂以整块 7776 字节作为单一 bin 文件；JASC-PAL 导出留待后续任务。

  所有 `graphics/` 下文件均 **不提交 git**（已入 `.gitignore`），仅保留生成脚本。

  #### 流程设计（实际实现）

  ```
  ── 导出（tools/export_gfx.py）────────────────────────────────────
  roms/2343.gba  ──►  graphics/opponents/palette_copy1.bin     （7776 字节，整块）
                  ──►  graphics/opponents/<name>_top_tilemap.bin  （1200 字节 × 27）
                  ──►  graphics/opponents/<name>_bottom_tilemap.bin
                  ──►  graphics/opponents/<name>_top.png          （渲染合成，供查看）
                  ──►  graphics/opponents/<name>_bottom.png
                  ──►  graphics/icons/<name>_icon.png

  ── ASM（asm/rom.s 已拆分为 8 段）────────────────────────────────
  incbin(rom, 0x1000000, 0xB101AC)           ← 图形数据前段
  .incbin "graphics/opponents/palette_copy1.bin"   ← Copy 1（7776 B）
  incbin(rom, 0x1B1200C, 0x36000)            ← Top 图块（保留 ROM incbin）
  .incbin "<name>_top_tilemap.bin" × 27      ← Top Tilemap
  .incbin "graphics/opponents/palette_copy1.bin"   ← Copy 2（同一文件）
  incbin(rom, 0x1B51CFC, 0x36000)            ← Bottom 图块（保留 ROM incbin）
  .incbin "<name>_bottom_tilemap.bin" × 27   ← Bottom Tilemap
  incbin(rom, 0x1B8FB8C, 0x2C438E)           ← 剩余段

  ── 导入（tools/import_gfx.py，T2.3 后续）────────────────────────
  <name>_top.png  ──►  4bpp tiles → ROM 图块偏移
  palette_copy1.bin  ──►  可由 JASC-PAL 重建（待实现）
  ```

  #### 子任务

  - [x] **T2.1**：扩展 `tools/export_gfx.py`，新增导出 `palette_copy1.bin`、`*_tilemap.bin`
  - [x] **T2.2**：拆分 `asm/rom.s` 大 incbin 为 8 段，tilemap/palette 改为 `.incbin` 文件引用，byte-identical 验证通过（commit b7a8ef6）
  - [ ] **T2.3**（后续）：实现 `tools/import_gfx.py`，PNG → 4bpp tiles + tilemap.bin → 写回 ROM

  > ⚠️ **构建依赖**：`build.bat` 前须先运行 `python tools/export_gfx.py` 生成 `graphics/opponents/*.bin`，
  > 否则汇编器找不到 incbin 文件。详见 README。

- [ ] **T3**：决斗场地图形导出管线

  依据：`doc/um06-romhacking-resource/duel-field.md`

  #### 数据概况

  6 种决斗模式 × 内场（Inner）+ 外场（Outer）= 最多 12 张背景图。
  外场有完整的 Image + Tilemap + Palette，内场只有 Image + Palette（无 Tilemap，可能以不同方式渲染）。

  | 模式 | 内场图块 | 外场图块 | 外场 Tilemap | 调色板 |
  |------|---------|---------|-------------|--------|
  | Campaign | `0x185D720` | `0x185504C` | `0x185B650` | `0x18674A0` / `0x18593A8` |
  | Link Duel | `0x185EDA0` | `0x185502C`... | `0x185BB00` | `0x18674C0` / `0x18593E8` |
  | Duel Puzzle | `0x1860420` | `0x185600C` | `0x185BFB0` | `0x18674E0` / `0x1859428` |
  | Limited | `0x1861AA0` | `0x18567EC` | `0x185C460` | `0x1867500` / `0x1859468` |
  | Theme | `0x1863120` | `0x18575CC` | `0x185C910` | `0x1867520` / `0x18594A8` |
  | Survival | `0x18647A0` | `0x18457FAC`... | `0x185CDC0` | `0x1867540` / `0x18594E8` |

  此外 ROM 中还有指针表（Inner Field Images/Tilemap/Palette Pointer Table，
  Outer Field 同理），位于 `0x1855030`、`0x185B634`、`0x185936C` 等。

  #### 子任务（参照 T2 流程）

  - [ ] **T3.1**：调查数据格式，确认尺寸（外场 Tilemap 宽高、图块数量）
  - [ ] **T3.2**：扩展 `tools/export_gfx.py`，导出 PNG 预览和 `*.bin` 文件
  - [ ] **T3.3**：拆分 `asm/rom.s` 对应 incbin 段，引用 `graphics/duel-field/*.bin`，byte-identical 验证

  > **注意**：内场无 Tilemap，渲染方式待调查（可能是 BG mode 3/5 的全图模式，或由代码直接索引图块）。

- [ ] **T4**：主菜单及其他杂项图形导出管线

  依据：`doc/um06-romhacking-resource/main-menu.md` + `banlist-code-breaking.md`

  #### 数据概况

  | 资产 | 类型 | 图块偏移 | Tilemap | 调色板 |
  |------|------|---------|---------|--------|
  | 主菜单背景 | 4bpp | `0x1CF009C` | 未知 | 未知 |
  | 主菜单图标 | **8bpp** | `0x1CF8B94` | 未知 | 未知 |
  | 禁卡密码界面 | 4bpp | `0x1E22874` | `0x1E22874`（Tilemap start？） | `0x1E314B4` |

  > **注意**：主菜单图标为 **8bpp**（256色），与大图的 4bpp 格式不同，
  > 解码时每字节对应一个像素（不需要拆半字节），且使用完整的 256 色单一调色板。

  #### 子任务

  - [ ] **T4.1**：调查各资产尺寸与格式（尤其 8bpp 主菜单图标）
  - [ ] **T4.2**：扩展/新建导出脚本，导出 PNG 预览和 `*.bin`
  - [ ] **T4.3**：拆分对应 incbin，byte-identical 验证

- [ ] **T5**：标题画面 LZ77 数据（特殊处理，暂缓）
  - 依据：`title-screen.md`，ROM 偏移 `0x1EC33DC`

