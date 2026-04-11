# 游戏王 EX2006 ROM 数据汇编化计划

## 目标

将 ROM 中已知数据区从 `.incbin` 替换为带结构注释的可读汇编代码，
最终输出与原始 ROM **byte-identical**。

## 数据区总览

| 区块 | ROM 偏移范围 | 大小 | 状态 |
|------|------------|------|------|
| 对手卡值块（27条目×32字节）| `0x1E58D0E – 0x1E5906D` | 864 B | ✅ 已完成（`data/opponent-card-values.s`）|
| 禁卡表（8个版本共487条目）  | `0x1E5EF30 – 0x1E5F6CB` | 1948 B | ✅ 已完成（`data/banlists.s`）|
| 初始卡组（50张+终止符）    | `0x1E5F884 – 0x1E5F8E9` | 102 B | ✅ 已完成（`data/starter-deck.s`）|
| 预组（6套+指针表）     | `0x1E5FA58 – 0x1E5FD83` | 812 B | ✅ 已完成（`data/struct-decks.s`）|
| 对手卡组（25套）           | `0x1E6468E – 0x1E65A45` | ~5300 B | ✅ 已完成（`data/opponent-decks.s`）|

## 数据编码格式

**预组**：每条 4 字节 = `(so_code * 4 | qty)` LE16 + `0x0000` LE16

**禁卡表**：每条 4 字节 = `so_code` LE16 + `limit` LE16（limit: 0禁止/1限制/2准限制）

**初始/对手卡组**：每条 2 字节 = `so_code` LE16，以 `0x0000` 终止

**对手卡值块**：每条 32 字节 = `card_value`(2) + `unk`(2) + 文件路径字符串(20字节null-padded) + padding(8)

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

## 实施步骤

- [x] Phase 0：建立宏系统（`include/macros.inc`）
- [x] Phase 1：重构预组（`data/struct-decks.s`）使用 `deck_entry` + 十进制 so_code
- [x] Phase 2：禁卡表（`data/banlists.s`）8个版本，使用 `banlist_entry`
- [x] Phase 3：初始卡组（`data/starter-deck.s`）50张，使用 `deck_card`
- [x] Phase 4：对手卡值块（`data/opponent-card-values.s`）27条目×32字节
- [x] Phase 5：对手卡组（`data/opponent-decks.s`）25套

## rom.s 最终布局（按 ROM 偏移排序）

```
incbin [0x1000000, 0x1E58D0D]
data/opponent-card-values.s   @ 0x1E58D0E (+864 B)
incbin [0x1E5906E, 0x1E5EF2F]
data/banlists.s               @ 0x1E5EF30 (+1948 B)
incbin [0x1E5F6CC, 0x1E5F883]
data/starter-deck.s           @ 0x1E5F884 (+102 B)
incbin [0x1E5F8EA, 0x1E5FA57]
data/struct-decks.s           @ 0x1E5FA58 (+812 B)  ← 已完成
incbin [0x1E5FD84, 0x1E6468D]
data/opponent-decks.s         @ 0x1E6468E (~+5300 B)
incbin [end, 0x1FFFF00]
```

## 注意事项

- 每个 Phase 完成后必须 `build.bat` 验证 **byte-identical**
- `so_code` 统一用**十进制**整数写入 ASM 源码（如 `4088` 代替 `0x0FF8`）
- 卡牌数据来源：`doc/um06-deck-modification-tool/data.md`
- 对手卡值块中 `unk` 字段（0x1F40 起递增）原因未知，保留为 `.hword` 硬编码

---

## doc/ 文档 ROM 数据落地状态审查（2026-04-11）

### ✅ 已落地（done）

| 文件 | 数据类型 | ROM 地址范围 | 已落地到 |
|------|----------|-------------|---------|
| `um06-deck-modification-tool/home.md` | 结构/初始/对手卡组地址索引 | 多处 | `data/struct-decks.s` / `data/starter-deck.s` / `data/opponent-decks.s` |
| `um06-deck-modification-tool/starter-opponent-paste-tool.md` | 卡组地址索引（与 home.md 重复） | 同上 | 同上 |
| `um06-deck-modification-tool/structure-deck-paste-tool.md` | 预组指针表 | `0x1E5FD54~0x1E5FD84` | `data/struct-decks.s` |
| `um06-romhacking-resource/modifying-banlists.md` | 禁卡表（8版本共 487 条） | `0x1E5EF30~0x1E5F6CA` | `data/banlists.s` |
| `um06-romhacking-resource/tool-development.md` | 预组指针地址（参考） | `0x1E5FD54` 等 | `data/struct-decks.s`（指针已含） |
| `um06-romhacking-resource/opponents-coinflip-screen.md`（部分） | 对手卡值（27 个 × 32 字节） | `0x1E58D0E~0x1E5906D` | `data/opponent-card-values.s` |

### ⚠️ 有 ROM 数据但未落地（pending）

| 优先级 | 文件 | 数据类型 | ROM 地址范围 | 说明 |
|--------|------|----------|-------------|------|
| ⭐⭐⭐ 高 | `um06-romhacking-resource/deck-string-name-tool.md` | **卡组名字符串 + 指针表** | 字符串表基址 `0x1DB9C10`；字符串 `0x1DC9F48~0x1DCC7B2` | 25 个对手卡组名 + 7 个结构/初始卡组名，字符串内容、字节数、指针偏移均有记录。目前在最大 incbin 块（`0x1000000~0x1E58D0D`）内 |
| ⭐⭐⭐ 高 | `um06-romhacking-resource/modifying-decks.md` | **卡组名字符串 + 指针表**（同上） | 同上 | 与 deck-string-name-tool.md 记录相同，以 deck-string-name-tool.md 为主要参考 |
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
  - `game-strings.s`：EN/DE/FR/IT/ES 全部游戏文本，ROM `0x1DC4620~0x1DFF9D1`，8210行
  - 字符编码：Latin-1，非ASCII字节用 `\xNN` 转义写入 `.ascii` 指令
  - byte-identical 已验证

  > ⚠️ **XX 语言待调查**：指针表第2槽（slot2）指向 ROM `0x1DBF01A`，
  > 内容全为 2字节序列（高字节 `0xF0~0xFF`），疑似自定义字体表索引。
  > 猜测为 GBA 日语版（BY7J）残留数据或某亚洲发行版本。
  > 后续任务：调查游戏字体表，对照 BY7J ROM（如有）确认编码。

- [ ] **T2**：提取对手图形地址指针表 → `data/opponent-gfx-pointers.s`
  - 依据：`opponents-coinflip-screen.md`
  - 包含：27 × (大图 Top/Bottom + 小图标) 的图块/Tilemap/调色板地址

- [ ] **T3**：提取决斗场地图形地址表 → `data/duel-field-gfx-pointers.s`
  - 依据：`duel-field.md`

- [ ] **T4**：提取主菜单/禁卡界面图形地址（体量小，可合并一个文件）
  - 依据：`main-menu.md` + `banlist-code-breaking.md`

- [ ] **T5**：标题画面 LZ77 数据（特殊处理，暂缓）
  - 依据：`title-screen.md`，ROM 偏移 `0x1EC33DC`
