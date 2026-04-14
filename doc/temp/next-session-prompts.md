# 下一次 Session 任务提示词（2026-04-15 交接）

下次开 session 时直接把下面对应任务的 **"提示词"** 区块粘贴给 Claude。
公共约束（所有任务通用）：

- 必读 `CLAUDE.md`；**构建必须保持 byte-identical**（`sha1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`）
- 构建/验证命令：
  ```
  as.exe -mcpu=arm7tdmi -o output/rom.o asm/rom.s
  ld.exe -T ld_script.txt -o output/2343.elf output/rom.o
  objcopy.exe -O binary output/2343.elf output/2343.gba
  # 对比 sha1 或 fc /b roms\2343.gba output\2343.gba
  ```
- ROM 数据拆分范式：
  - 大段纯数据 → `graphics/<subtopic>/*.bin`（gitignore），由 `tools/rom-export/export_*.py` 生成
  - 结构化数据 → `data/*.s`（`.include` 到 `asm/rom.s`）
  - `asm/all.s` 保留纯代码（含 literal pool DAT_*），数据段移至 `asm/rom.s`
- 不主动 commit；简体中文沟通/文档/注释
- 临时脚本 → `tools/ad-hoc/`；临时笔记 → `doc/temp/`
- `LOCAL.md`（未入库）保存本地工具路径，不要硬编码

---

## 任务 1：T-HUD（决斗 HUD 元素 incbin 拆分）

### 目标
把 `doc/um06-romhacking-resource/duel-field.md` 里列出的 HUD 相关 5 条 ROM 地址导出成 bin 并在 `asm/rom.s` 拆分引用。

### 必读
- `doc/um06-romhacking-resource/duel-field.md`（HUD 章节）
- `asm/rom.s` L43-L119（场地主图形 incbin 拆分现成参考范式）
- `tools/rom-export/export_gfx.py`（opponents/duel-field 图形导出脚本，对照其结构扩展）

### 已知地址（从 PLAN.md 抄）
| 资源 | ROM |
|------|-----|
| Life Points Font | 0x1850B1C |
| Phases Highlight | 0x18519FC |
| Phase Highlights Palette | 0x18515DC |
| Phases Tilemap | 0x1859548 |
| Phases Map | 0x185B184 |

### 步骤
1. 读 duel-field.md 对应章节，拿到每项的字节长度 / 格式（4bpp/8bpp/tilemap/palette）
2. 扩展 `tools/rom-export/export_gfx.py` 加一个 HUD 段的切片逻辑，输出 `graphics/duel-field/hud_*.bin`
3. 修改 `asm/rom.s` 对应段（场地主图形之后、当前大 incbin 之前），拆成若干 `.incbin "graphics/duel-field/hud_*.bin"`
4. 验证 byte-identical
5. 更新 PLAN.md：⚠️ 行删掉、T-HUD 勾选

### 陷阱
- HUD 地址夹在场地主图形之间，切片范围要和现有 incbin 精确拼接
- 不确定的段长度先 grep um06 文档取值，不要猜

### 提示词（拷贝给下一个 Claude）
```
按 doc/temp/next-session-prompts.md「任务 1：T-HUD」完成决斗 HUD 元素的
incbin 拆分。参照 asm/rom.s L43-L119（场地主图形）的现成管线实现。

要求：
1. 扩展 tools/rom-export/export_gfx.py 增加 HUD 切片
2. 修改 asm/rom.s 引用新 bin
3. 构建 byte-identical（sha1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b）
4. 更新 PLAN.md（⚠️ 行移除、T-HUD 勾选）
不要主动 commit，完成后等我确认。
```

---

## 任务 2：T6.4（属性/种族编码表补全）

### 目标
把 `doc/dev/card-data-structure.md` §一 的"属性编码（部分确认）"和"种族编码（部分确认）"两张表补全，作为文档 + `include/macros.inc` 或 `data/card-enums.inc` 的常量定义。

### 必读
- `doc/dev/card-data-structure.md` §一（字段布局 + 部分表）
- `doc/um06-deck-modification-tool/data.md`（4072 条卡牌数据库，带属性/种族文本）
- `data/card-stats.s`（5170 条属性记录）
- `data/card-names.s`（slot_id → EN 卡名）

### 方法
写一次性 Python 脚本（`tools/ad-hoc/verify_card_enums.py`）：
1. 读 ROM `0x018169B6` 的 5170 条记录，提取 (slot_id, attribute, race)
2. 读 `data.md`（或其生成源）按 slot_id/密码对齐，得到 (slot_id, attribute_text, race_text)
3. 统计：对每个 attribute 数值，看对应 data.md 里出现的所有 text，应该一致
4. 同理 race
5. 输出完整映射表

### 产出
- 在 `card-data-structure.md` §一 补全两张表（LIGHT/DARK/WATER/FIRE/EARTH/WIND/DIVINE；Dragon/Spellcaster/... 全套）
- 若脚本未来还有用，正式化到 `tools/rom-export/` 下；否则保留在 `ad-hoc/`
- PLAN.md T6.4 勾选

### 陷阱
- `data.md` 是 Google Sheets 转 markdown，编码/格式要稳
- Spell/Trap 卡 attribute 和 race 语义不同（data-structure.md 提到 race=8 是 Spell、9 是 Trap），不要当怪兽处理

### 提示词
```
按 doc/temp/next-session-prompts.md「任务 2：T6.4」补全卡牌属性/种族编码表。

路径：
- 数据源：ROM data/card-stats.s 里的 attribute (+14) 和 race (+16) 字段
- 文本源：doc/um06-deck-modification-tool/data.md
- 输出：更新 doc/dev/card-data-structure.md §一 两张表；写 tools/ad-hoc/verify_card_enums.py

不要主动 commit。完成后等我确认。
```

---

## 任务 3：T-COINFLIP / T-THEME（图形资产管线）

### 目标
复用 opponents 大图和 icons 的 incbin 拆分管线，把 Coinflip 界面 4 类资源和 Theme Duel 27 对手大图接入。

### 必读
- `asm/rom.s` L126-L260（opponents + icons 现成管线，完整可参考）
- `tools/rom-export/export_gfx.py`（opponents 导出脚本）
- `doc/um06-romhacking-resource/opponents-coinflip-screen.md`（两批资源都在这个 md 里）

### T-COINFLIP
4 类界面资源 @ `0x18977F8 / 0x194D71C / 0x194F83C`（+ 每类的 tilemap/palette），见 PLAN ⚠️ 表。

### T-THEME
27 对手 × Top/Bottom Large Wallpaper + palette，起于 `0x1A1DFAC`。结构**类似对手大图**（L126-L260 的对应段），应直接套用。

### 步骤（两个任务流程相同）
1. 从 um06 md 抽取每份资源的 ROM 起止 + 格式 + 字节长度
2. 扩展 `tools/rom-export/export_gfx.py` 增加对应切片
3. 修改 `asm/rom.s` 拆分对应段 incbin
4. 跑 `export_gfx.py` 生成新 bin，构建验证 byte-identical
5. 勾 PLAN.md

### 陷阱
- `0x1B101AC..0x1B8FB8B` 已是 opponents 大图；Theme Duel 大图在更早的 `0x1A1DFAC`，别混淆
- Coinflip 的 "Flipping Animation" 可能是多帧 OAM，格式需仔细对照文档

### 提示词
```
按 doc/temp/next-session-prompts.md「任务 3：T-COINFLIP / T-THEME」完成
两批图形资产的 incbin 拆分。参照 asm/rom.s L126-L260 的 opponents 管线。

先做 T-THEME（结构最直接），再做 T-COINFLIP（格式更杂）。

每完成一个：构建 byte-identical + 勾 PLAN.md。不要主动 commit。
```

---

## 任务 4：P2（卡牌列表小图调查）

### 目标
完整解决 `doc/dev/card-data-structure.md` §三"当前导出状态（未完成）"——2054 张小卡图（40×56，8bpp，2240 B/卡）的调色板定位、index ↔ slot_id/card_id 映射、批量 PNG 导出。

### 必读（**按顺序**）
1. `doc/dev/p1-phase-b2-findings.md`（大卡图调查完整方法论，可直接类比）
2. `doc/dev/card-image-export.md`（大卡图导出脚本设计，P2 要复用多数模式）
3. `doc/dev/card-data-structure.md` §三（小卡图区现状）
4. `CLAUDE.md`（mGBA MCP + GDB MCP 使用说明）

### 已知（勿质疑）
- 小卡图 ROM：`0x01000000..0x01463480`（2054 × 2240 B）
- 格式：8bpp tiles, 5×7 tile 布局 = **40×56 像素**, stride 2240 = 5×7×64
- tile 排列：**列优先**（tile 0..4 第一行，tile 5..9 第二行）—— 注意和大卡图的"行优先 10×10"不同
- 前若干 entry 是 UI 字体/数字（非卡图），实际卡图起始 index 未确认
- 调色板位置**未知**（data-structure.md §三 已列了试过的几个区域）

### 关键未解问题
1. **调色板位置**：§三 列了三个候选（`0xFF0000`、`0x1463480` 之后、stride 2240+512=2752 内嵌），均未验证
2. **UI 图形占用多少 entry**：index 0 开始的若干条是字体/数字（蓝底 0-9 等），到 index=? 才是真正卡图
3. **image_index ↔ slot_id 映射**：§三 推测"顺序索引"（image_index 0 对应按 slot 升序的第 0 张卡），但需要 mGBA 实测验证

### 推荐步骤（P1 方法论照抄）
1. **P2-1（mGBA 动态）**：启动 `pwsh tools/mgba-scripts/start-mgba-gdb-ss1.ps1`，进入卡组构筑/卡典界面，用 Lua 读 DISPCNT + 所有 BGxCNT + tilemap + VRAM char base，定位小卡图在 VRAM 哪个位置被写入
2. **P2-2（静态追）**：从第 1 步找到的 VRAM 地址，在 `asm/all.s` 里搜该立即数，找到写 VRAM 的加载函数；跟着加载函数的字面量池找 ROM 源地址和 palette 基址
3. **P2-3（调色板验证）**：仿照大卡图的发现过程（`0x4C76C0 + tile_block × 128`）——小卡图可能有类似 `palette_base + image_index × stride` 结构
4. **P2-4（脚本）**：新建 `tools/rom-export/export_card_list_images.py`（或扩展现有脚本加 `--list-images` 模式），输出 `graphics/card-images-list/card_NNNN.png`
5. **P2-5（UI entries）**：查明 UI 字体/数字占的 entry 数量，记入文档

### 陷阱
- 大卡图的 6bpp 调色板 `+0x10` 偏移是游戏内 VRAM palette 写法；小图用 8bpp 则是 256 色直接索引，**不要套用偏移**
- tile 排列可能是**列优先**（每列 7 tiles → 7 tiles × 列数 5），验证时要双向尝试
- `0x01000000` 起的数据 Ghidra 已用 `.incbin 0x1000000, 0x5BB5AC` 整块包含在 `asm/rom.s` L23——如果要拆分，参考 P1 拆索引表的做法（rom.s 内部，不在 all.s）
- mGBA GDB stub 坑都在 `doc/dev/mgba-gdb-stub-pitfalls.md`，必读避坑

### 成功标准
- 调色板基址 + stride 确认，含 mGBA/静态两路证据
- 2054 张小图全部彩色 PNG 导出到 `graphics/card-images-list/`
- 新文档 `doc/dev/card-list-image-export.md` 记录整个调查过程
- 若拆 `asm/rom.s` 对应 incbin 段接入 bin/.s 引用，构建 byte-identical
- PLAN.md P2-1..P2-5 全部勾选

### 提示词（最长，因为 P2 信息量大）
```
按 doc/temp/next-session-prompts.md「任务 4：P2」完整调查并落地 2054 张
卡牌列表小图。

先读顺序：
1. doc/dev/p1-phase-b2-findings.md（大卡图调查案例，方法论照抄）
2. doc/dev/card-image-export.md（大卡图导出脚本范式）
3. doc/dev/card-data-structure.md §三（小卡图已知/未知信息）
4. CLAUDE.md（mGBA + GDB 调试工具链、踩坑总结）

已确认不用质疑：
- 小卡图 ROM 0x01000000..0x01463480，2054 × 2240 B，8bpp，40×56 像素
- tile 布局 5×7，列优先（与大卡图 10×10 行优先不同）
- 前若干 entry 是 UI 字体非卡图

本任务要解决：
1. 调色板位置（§三 列了候选，都未验证；参考大卡图的 per-card 128B 独立
   调色板发现思路）
2. UI 字体占多少 entry
3. image_index ↔ slot_id 映射（验证"顺序索引"推测）
4. 批量导出彩色 PNG 到 graphics/card-images-list/
5. 若拆 asm/rom.s L23 的大 incbin 接入 bin/.s 引用，保持构建 byte-identical

步骤建议：
- mGBA + Lua 抓卡选界面 VRAM/DISPCNT/BGxCNT（方法参见 findings §一）
- 静态追加载函数找 ROM 源 + palette 基址（方法参见 findings §二、§三）
- 写 tools/rom-export/export_card_list_images.py
- 新文档 doc/dev/card-list-image-export.md 记录发现
- 勾 PLAN.md P2-1..P2-5

约束：
- 构建 byte-identical（sha1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b）
- 不主动 commit
- 有新发现立刻写 doc/temp/
- 遇到抉择按推荐执行，不用问我
- 上下文到 40% 时写总结然后终止
```

---

## 交接状态摘要（供参考）

**最近一次 commit**：`311abea refactor(asm): 大卡图调色板/tile/索引汇编化，all.s 纯代码化`

**已落地的大卡图管线**（P2 可直接类比）：
- `data/card-image-index.s`（索引表 .hword，带注释）
- `data/card-image-palettes.s`（2331 条 .incbin 调色板）
- `data/card-image-tiles.s`（2331 条 .incbin tile）
- `graphics/card-images-rom/palettes/tb*.bin` + `tiles/tb*.bin`（需 `python tools/rom-export/export_card_images.py --no-png` 生成）
- `tools/rom-export/export_card_images.py`（支持 `--no-png` / `--no-blobs` / `--only` / `--gray`）
- 2331 PNG 全量导出到 `graphics/card-images/`

**关键映射关系**：
- `card_id` = `data/card-stats.s` 的 0-indexed 数组下标
- `flag=0` OCG 日版 / `flag=1` TCG 非日版（BY6E 是 flag=1）
- 每 slot 在 stats 表有 2 条 copy=0 记录（A 表 idx 1..2080 + B 表 idx 2081..5169），**正式卡只认 A 表的 card_id** (1..2097)
