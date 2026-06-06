# 函数/数据细化计划 — `asm/01_vija_scene_text.s`

> 阶段目标: 把 `asm/01_vija_scene_text.s` (ROM `0x0801CB00 ~ 0x0802C238`, vija 场景状态机 +
> 文本渲染 + puzzle 显示派发) **逐段地址序细化完成**, 全程 byte-identical
> (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **2** 个文件 (file 00 已全 10 段完成, 见 `p5-refine-00-system-str-vija.md`)。
> 方法论 + R1-R9 细化清单 + 三条硬规则见 `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00 doc §一 的 **R1-R9** (常量 equate / 灭自动名 / 引用接通 / 误标代码 disasm /
注释订正用现名 / 先读消费者 / 数据 carve 进 rom.s / 图形目视 / byte-identical+备份) +
**三条硬规则** (严格地址序 Seg-1..10 不回头 / 函数间 ROM_INCBIN 必 carve 或 §5.1 / 全 ROM 0 引用→§5.1)。

**跨文件踩坑沿用** (file 00 沉淀):
- EQ_SLOT 的 Ghidra 槽 label 名 **必须 != `.equ` 常量名** (`<func>_<const>` 式; 否则 GAS PC-relative
  "value too big") — 见 memory `carve-eq-label-collision`。
- Ghidra EOL/plate **一律 ASCII** (含 CJK 会 Jython 双重 UTF-8 mojibake), 中文解释走 doc/。
- carve byte-identical: host incbin 覆盖等式 `sum(spans)==原 size`; THUMB fn-ptr 表 `.word <fn>+1`,
  数据指针不 +1; `.asciz` 须含 NUL+对齐 pad (file 00 Seg-8 bg2 路径曾 0x1E→0x20 差 2B); .hword RGB15 注意 bit15。
- **executor 严守段上界** (file 00 Seg-8 executor 曾越界拉入下段 36 项; reviewer C1 逐槽地址裁定) —
  见 memory `refine-executor-segment-boundary`。
- 远端 ROM 数据表被本段代码引用→**当场 carve** (label+incbin-span byte-safe); 复用 file 00 已建 carve
  label (name_char_*/trig_table/rom_password_table 等) 与 constants/*.inc (ewram/gba_mem/oam_attr/
  gfx_resource/name_input/demo_state/gl_*.inc; gVijaState=0x02029eb0 / gDemoState=0x02029ec0)。

---

## 二、落地工作流 (pipeline)

同 file 00 doc §二「代码侧 pipeline」:
```
备份 .rep → Ghidra 脚本 (RefineSeg<N>*.py: equate/label/ref/rename/plate/disasm)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor (proposal) → reviewer (C1-C13 review) → fixer (模式A改proposal / 模式B落地)。

---

## 三、当前进度 (01_vija_scene_text.s)

| Seg | 范围 | 状态 | commit |
|-----|------|------|--------|
| **1** | 0x1cb00..0x1d448 (8fn, incbin 0x1d024/0x1c) | ✅ | 50a40fc |
| **2** | 0x1d448..0x1d998 (8fn) | ✅ | db3325d |
| 3 | 0x1d998..0x1e36c (8fn) | ⬜ | |
| 4 | 0x1e36c..0x1e714 (8fn) | ⬜ | |
| 5 | 0x1e714..0x1f25c (8fn) | ⬜ | |
| 6 | 0x1f25c..0x20fa8 (8fn, incbin 0x1f4d0/0x690, 0x1fb90/0x302, 0x202fe/0x36, 0x20370/0xa44) | ⬜ | |
| 7 | 0x20fa8..0x24868 (8fn, incbin 0x2108e/0xbe, 0x211b4/0xc4, **0x2134c/0x1ae0**, 0x22eb8/0x9a6) | ⬜ | |
| 8 | 0x24868..0x27e44 (8fn, incbin 0x2497c/0x78, 0x258f0/0x230) | ⬜ | |
| 9 | 0x27e44..0x28bdc (8fn, incbin 0x27e50/0x6c) | ⬜ | |
| 10 | 0x28bdc..0x2c238 (12fn, incbin **0x29170/0x22f0**) | ⬜ | |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 四、逐段完成记录

(随各段落地由 fixer 追加: Seg-N 函数列表 + 符号化统计 + carve/disasm/§5.1 + 脚本名 + commit。)

### 4.01 Seg-1 完成记录 (2026-06-07)

- 范围: 0x0801cb00..0x0801d448, 8 fn
- 函数: run_vija_scene_state_machine / tick_scene_step_by_step_table_b / tick_scene_step_by_step_table_c / write_tile_attr_byte_to_vram / copy_palette_bank_by_slot / write_tile_attr_strip_4wide / apply_palette_and_tile_attr_strips / decode_card_image_6bpp
- Ghidra 脚本: RefineF01Seg1Slots.py
- EQ=15 (gVijaState x1, ROM_REGION_CODE_ADDR x2, EWRAM_BASE x2, GSETTINGS_OFFSET x2, DEMO_CLEAR_BITS_12_8 x4, NAME_INPUT_PAGE_STATE_CLEAR x2 [C5 复用], BG_CHAR_VRAM_CB2 x2 [新建 gba_mem.inc])
- REF=3 (switch_table_base / vija_bg_fs_path_pair / vija_obj_slot_seq)
- RENAME=5 (step_table_b/c + 3x decode_card_image_6bpp mask slots)
- FUNC_RENAME=0
- PLATE=3 (decode_card_image_6bpp CJK->ASCII + 2x FUN_->现名 C8)
- carve=1: vija BG/OBJ resource data (rom.s line 1142, 0x1E3D9CF/0xC33D -> 5B+24B+27B+1B+8B+8B+0xC2F4; labels: vija_bg_jp_path / vija_bg_us_path / vija_bg_fs_path_pair / vija_obj_slot_seq)
- disasm=0 (orphan dispatcher 簇 §5.1)
- §5.1=1 cluster (0x0801d024 orphan THUMB dispatcher + jump table 0x1d044 + handlers 0x1d0bc)
- 新增 constants: BG_CHAR_VRAM_CB2=0x06004000 (gba_mem.inc)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: 50a40fc

### 4.02 Seg-2 完成记录 (2026-06-07)

- 范围: 0x0801d448..0x0801d998, 8 fn
- 函数: card_info_page_enter_with_card_id / card_info_page_init_bg0 / render_card_name_to_line_buf / draw_card_name_label_to_vram / render_atk_def_digits_to_buf / draw_atk_def_label_to_vram / render_card_level_text_to_buf / draw_card_level_label_to_vram
- Ghidra 脚本: RefineF01Seg2Slots.py
- EQ=15 (BG_CHAR_VRAM_CB2 x1 reuse / OBJ_PALRAM_BASE x1 reuse / gFontJpCtx x1 reuse / EWRAM_BASE x1 reuse / GSETTINGS_OFFSET x1 reuse / CARD_INFO_BG1CNT_INIT x1 新 / CARD_INFO_BG2CNT_INIT x1 新 / CARD_INFO_BG3CNT_INIT x1 新 / CARD_INFO_OBJ_PAL_SLOT x1 新 / CARD_INFO_NAME_BG_TILE_VRAM x1 新 [Fix#1 OAM->BG] / CARD_INFO_NAME_SPRITE_VRAM x1 新 / CARD_INFO_STAT_BG_TILE_VRAM x2 新+复用 [Fix#2 OBJ->BG] / CARD_INFO_STAT_SPRITE_VRAM x2 新+复用)
- REF=12 (gCardInfoPageState x3 / name_o_palette_data x1 / sjis_char_fold_table x1 / card_label_glyph_buf x2 / card_digit_glyph_data x3 / level_signature_table_field_a x1 / level_signature_table_field_b x1)
- FUNC_RENAME=0
- PLATE=8 (全 8 函数 CJK->ASCII)
- carve=3 (Carve A: sjis_char_fold_table @ rom.s line 1599, 0x1E589A4 0x368 分裂; Carve B: 124KB blob 三表 @ rom.s line 124, 0x1832602 0x1E51A 分裂: card_digit_glyph_data@0x0984f54c/0x50 + card_label_glyph_buf@0x0984f59c/0x30 + card_glyph_table_3@0x0984f5cc/0x1550)
- 新增 constants: card_info.inc (8 常量: BG1/2/3CNT_INIT / OBJ_PAL_SLOT / NAME_BG_TILE_VRAM / NAME_SPRITE_VRAM / STAT_BG_TILE_VRAM / STAT_SPRITE_VRAM)
- 新增全局: gCardInfoPageState=0x0201afb0 (ewram.inc); level_signature_table_field_a/_b offset labels (data/post-banlists-tables.s)
- §5.1=0 (段内无数据块)
- disasm=0
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: db3325d

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 01 范围 `[0x0801cb00, 0x0802c238)` (span 0xF738, ~84 named fn, 13 ROM_INCBIN) 按**函数数**
> 均分 10 段 (~8 fn/段, 边界=函数起点)。两个大数据块 (0x2134c/0x1ae0=6880B 在 Seg-7, 0x29170/0x22f0=8944B
> 在 Seg-10) 处理时先 ref-scan 分类 (carve/disasm/§5.1)。逐段 executor→reviewer→fixer, 地址序不回头。

| Seg | 地址范围 | ~fn | 内含 ROM_INCBIN (必 carve/disasm/或 §5.1) | 备注 |
|---|---|---|---|---|
| Seg-1 | 0x1cb00..0x1d448 | 8 | 0x1d024/0x1c | 含 file 00 边界后首函数 run_vija_scene_state_machine |
| Seg-2 | 0x1d448..0x1d998 | 8 | — | |
| Seg-3 | 0x1d998..0x1e36c | 8 | — | |
| Seg-4 | 0x1e36c..0x1e714 | 8 | — | |
| Seg-5 | 0x1e714..0x1f25c | 8 | — | |
| Seg-6 | 0x1f25c..0x20fa8 | 8 | 0x1f4d0/0x690, 0x1fb90/0x302, 0x202fe/0x36, 0x20370/0xa44 | 4 数据块 (文本/puzzle 资源?) |
| Seg-7 | 0x20fa8..0x24868 | 8 | 0x2108e/0xbe, 0x211b4/0xc4, **0x2134c/0x1ae0**, 0x22eb8/0x9a6 | 大数据区 (~6880B 块, ref-scan 分类) |
| Seg-8 | 0x24868..0x27e44 | 8 | 0x2497c/0x78, 0x258f0/0x230 | |
| Seg-9 | 0x27e44..0x28bdc | 8 | 0x27e50/0x6c | |
| Seg-10 | 0x28bdc..0x2c238 | 12 | **0x29170/0x22f0** | 大数据区 (~8944B 块, ref-scan 分类) |

执行约定同 file 00: 每段走 §二 pipeline; Seg 内可多次提交但地址序不回头; 已干净函数跳过只补 gap;
每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| 0x0801d024 (+ jump table 0x1d044..0x1d0bb + handlers 0x1d0bc/0xc0/0xc4) | 28B (ROM_INCBIN 0x1d024,0x1c) + 30×4B jump table (已 .word) + 16B (.byte 0x1d0bc) | f01 Seg-1 | orphan THUMB tile-attr dispatcher 簇: push{r4,lr}+subs r0,#1+bhi OOB+30-entry jump-table dispatch via mov pc,r0; 入口 0 外部引用 (raw+thumb 全 0; 前函数 0x1d022 bx r1 返回); 簇内互引。同 file 00 Seg-4/Seg-5b orphan dispatcher 模式。 | 留待: 引用到时 R4 disasm + createFunction |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
