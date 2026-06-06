# Refine Review: f01-Seg-2

**段区间**: `[0x0801d448, 0x0801d998)` — 8 fn, card_info 页文字渲染  
**Proposal**: `doc/dev/refine/f01-Seg-2.proposal.md`  
**源文件**: `asm/01_vija_scene_text.s` 行 ~1199..1890  
**复核日期**: 2026-06-07

---

## 自主复核结果 (Phase 1)

### ref-scan 重跑 (不信 proposal)

| 地址 | raw_refs | thumb_refs | proposal 值 | 一致 |
|---|---|---|---|---|
| 0x09e589c4 (sjis_char_fold_table) | 4 | 0 | raw=4 | YES |
| 0x0984f54c (card_digit_glyph_data) | 6 | 0 | raw=6 | YES |
| 0x0984f59c (card_label_glyph_buf) | 3 | 0 | raw=3 | YES |
| 0x0984f5cc (card_glyph_table_3) | 2 | 0 | raw=2 (driver 补) | YES |
| 0x0201afb0 (gCardInfoPageState) | 20 | 0 | ~20 | YES |
| 0x09ccd290 (name_o_palette_data) | 15 | 0 | raw=15 | YES |
| 0x09e5f71e (level_sig+2) | 2 | 0 | raw=2 | YES |
| 0x09e5f726 (level_sig+0xa) | 2 | 0 | raw=2 | YES |

### ROM 字节核对 (全 27 EQ/REF 槽)

全部 27 个 DAT_ 槽逐一读 4 字节，与 proposal 值完全一致。代表性验证：

| 槽地址 | ROM 读值 | Proposal 值 | 一致 |
|---|---|---|---|
| 0x0801d4e8 | 0x06004000 | BG_CHAR_VRAM_CB2 | YES |
| 0x0801d4f4 | 0x00004104 | CARD_INFO_BG1CNT_INIT | YES |
| 0x0801d4f8 | 0x00000407 | CARD_INFO_BG2CNT_INIT | YES |
| 0x0801d4fc | 0x00000305 | CARD_INFO_BG3CNT_INIT | YES |
| 0x0801d504 | 0x050003e0 | CARD_INFO_OBJ_PAL_SLOT | YES |
| 0x0801d704 | 0x06001840 | (CARD_INFO_NAME_OAM_TILE_BASE — 见 Fix #1) | YES (值正确) |
| 0x0801d708 | 0x06008200 | CARD_INFO_NAME_SPRITE_VRAM | YES |
| 0x0801d828 | 0x06001c00 | (CARD_INFO_STAT_OBJ_TILE_BASE — 见 Fix #2) | YES (值正确) |
| 0x0801d82c | 0x06008580 | CARD_INFO_STAT_SPRITE_VRAM | YES |
| 0x0801d650 | 0x09e589c4 | sjis_char_fold_table | YES |
| 0x0801d7cc | 0x0984f54c | card_digit_glyph_data | YES |
| 0x0801d7c8 | 0x0984f59c | card_label_glyph_buf | YES |
| 0x0801d458 | 0x0201afb0 | gCardInfoPageState | YES |

### carve 覆盖等式 (自重算)

**Carve A: sjis_char_fold_table**  
Host: `rom.s line 1596` `.incbin 0x1E589A4, 0x368`  
分裂: `0x20 (pre) + 0x100 (table) + 0x248 (post)`  
验证: `0x20 + 0x100 + 0x248 = 0x368` — **PASS**

**Carve B: 124KB blob 三表**  
Host: `rom.s line 121` `.incbin 0x1832602, 0x1E51A`  
分裂: `0x1cf4a (pre) + 0x50 (digit) + 0x30 (label) + 0x1550 (table3)`  
验证: `0x1cf4a + 0x50 + 0x30 + 0x1550 = 0x1e51a` — **PASS**

table3 span 详细: `0x1850B1C - 0x184F5CC = 0x1550` 字节。

### 第四个 carve label (0x0984f5cc) 性质核

0x0984f5cc 是 blob 内第三个被引用地址，raw_refs=2，refs 来自：
- `0x080cae64` (ROM off 0xcae64, 4-byte aligned)
- `0x080cb6f4` (ROM off 0xcb6f4, 4-byte aligned)

两处均为合法代码字面量槽（4 字节对齐），引用模块在 file-C 区（非 seg-2）。Driver 命名为 `card_glyph_table_3` 合理，是独立字形表起点。

### Blob 内 table3 span 扫描 (0x184f5cc..0x1850b1c)

在 table3 span (0x1550B) 内扫描出以下被引用地址：

| 地址 | raw_refs | 对齐 | 引用来自 |
|---|---|---|---|
| 0x0984f5cc | 2 | YES | 0x080cae64, 0x080cb6f4 (file-C) |
| 0x0984f834 | 1 | NO (misaligned) | 0x09f36dd6 — 数据误命中 |
| 0x0984f958 | 1 | NO | 0x09fdaa61 — 数据误命中 |
| 0x0984fbcc | 4 | YES | 0x080bec34/c34f8/c39f8/c3a38 (file-C 区) |
| 0x0984fc7c | 1 | YES | 0x09fd9f48 (深 ROM 数据区，非 seg-2 asm) |
| 其余 | 各 1 | NO | 数据误命中 |

**关键发现**: `0x0984fbcc` 有 4 个合法代码引用，但不在 seg-2 代码内。该地址在 card_glyph_table_3 incbin 内部，目前无 label。

评估：seg-2 proposal 只负责 seg-2 代码所引用的地址。0x0984fbcc 的 4 refs 全来自 file-C 其他模块（0x080bec34 等），将由这些模块的未来 refine 段处理。seg-2 proposal 提供 `card_glyph_table_3` label 已充分覆盖 seg-2 所需，不违反 Rule 2（Rule 2 约束的是 seg asm 文件内的 ROM_INCBIN，不是 rom.s 批量 blob 内的子地址）。

### BG VRAM 命名分析

GBA VRAM 布局：BG VRAM `0x06000000..0x0600FFFF`；OBJ tile VRAM 从 `0x06010000` 起。

| 地址 | 相对 VRAM | 实际区域 | Proposal 命名 |
|---|---|---|---|
| 0x06001840 | CB0+0x1840, SB3+0x040 | BG VRAM (screen map 区) | CARD_INFO_NAME_**OAM**_TILE_BASE — 错误 |
| 0x06001c00 | CB0+0x1c00, SB3+0x400 | BG VRAM (screen map 区) | CARD_INFO_STAT_**OBJ**_TILE_BASE — 错误 |
| 0x06008200 | CB2+0x0200, SB16+0x200 | BG VRAM | CARD_INFO_NAME_SPRITE_VRAM — 含混 |
| 0x06008580 | CB2+0x0580, SB16+0x580 | BG VRAM | CARD_INFO_STAT_SPRITE_VRAM — 含混 |

结论：
- `OAM_TILE_BASE` 和 `OBJ_TILE_BASE` 命名暗示 `0x06010000+` OBJ 区，实际均在 BG VRAM — **必须改名**。
- `SPRITE_VRAM` 命名来自 callee `commit_line_buffer_to_sprite_vram`，含混但有来源，属边界情况，本次不强制改，后续可跟进。

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 Rule1 | 段范围 [0x1d448, 0x1d998) | PASS | 8 fn 全 <0x1d998; 末槽 DAT_0801d994 占 0x1d994-0x1d997; 下一 fn card_image_decode_wrapper 从 0x1d998 起 |
| C2 Rule2 | 段内 ROM_INCBIN=0 | PASS | 逐行确认无 ROM_INCBIN/.byte; 远端 carve 均有归宿 |
| C3 Rule3 | §5.1 块 0 引用核 | N/A | 段内无 §5.1 块 |
| C4 R1 值 | EQ value == ROM 4 字节 | PASS (值), **FAIL (名)** | 全 27 槽 ROM 字节一致; 但 OAM_TILE_BASE/OBJ_TILE_BASE 命名错误 — 见 Fix #1/#2 |
| C5 R1 复用 | 8 新建 card_info.inc 常量无重值 | PASS | 扫描所有 constants/*.inc，无同值现有常量 |
| C6 R2 名 | 槽名格式 ^[a-z][a-z0-9_]+$ | PASS | 全 27 个 slot_label 均合规; 无碰撞 |
| C7 R3 接通 | carve label 有 USER-label + DATA-ref | PASS | sjis_char_fold_table / card_digit_glyph_data / card_label_glyph_buf / card_glyph_table_3 均有 REF_SLOT 计划 |
| C8 R5 现名 | plate 无残留 FUN_/DAT_/DWORD_ | PASS | 8 个新 plate 文本均无自动名残留 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 8 个新 plate 文本全部 ASCII (Python 逐字节验证) |
| C10 carve | 指针表 THUMB+1 核 | N/A | 三个 carve 均为字形/字符字节表，非指针表 |
| C11 误名 | 函数名与体矛盾 | PASS | 无 FUNC_RENAME 需求; 8 fn 名与体操作吻合 |
| C12 R6 | 关键槽有 file:line 证据 + 置信度 | PASS | gCardInfoPageState/level_signature_table/glyph tables 均有消费者 file:line 引用 + high 置信度 |
| C13 残留 | 段内全 DAT_ 均被覆盖 | PASS | 27 个 DAT_ 槽全有处理 (EQ/REF/PTR 复用); PTR_ 五槽已有 USER-label 不改 |

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### Fix #1 — C4 — CARD_INFO_NAME_OAM_TILE_BASE → CARD_INFO_NAME_BG_TILE_VRAM

**原因**: 0x06001840 位于 BG VRAM (CB0+0x1840 = SB3+0x040)，而非 OAM 区。OAM 基址为 0x07000000。"OAM_TILE_BASE" 误导读者认为是 OAM 属性表地址。

**需要修改的位置**:

1. `EQ_SLOTS` 表第 10 行 (DAT_0801d704):
   - const_name: `CARD_INFO_NAME_OAM_TILE_BASE` → `CARD_INFO_NAME_BG_TILE_VRAM`
   - slot_label: `draw_card_name_label_to_vram_oam_tile_base` → `draw_card_name_label_to_vram_bg_tile_vram`

2. `card_info.inc` 新建内容:
   - `.equ CARD_INFO_NAME_OAM_TILE_BASE, 0x06001840` → `.equ CARD_INFO_NAME_BG_TILE_VRAM, 0x06001840`
   - 注释改为: `@ BG screen-map tile-attr write base for card name line (CB0, SB3+0x040)`

3. `REF_SLOTS` 表 DAT_0801d94c 行 (`draw_card_level_label_to_vram`):
   - DAT_0801d94c 的值是 0x06001c00 (= CARD_INFO_STAT_BG_TILE_VRAM, 见 Fix #2)
   - slot_label: `draw_card_level_label_to_vram_obj_tile_base` → `draw_card_level_label_to_vram_bg_tile_vram`
   - gas_label: `CARD_INFO_STAT_OBJ_TILE_BASE` → `CARD_INFO_STAT_BG_TILE_VRAM`

---

### Fix #2 — C4 — CARD_INFO_STAT_OBJ_TILE_BASE → CARD_INFO_STAT_BG_TILE_VRAM

**原因**: 0x06001c00 位于 BG VRAM (CB0+0x1c00 = SB3+0x400)，而非 OBJ tile VRAM (0x06010000+)。"OBJ_TILE_BASE" 误导读者认为是 sprite tile 数据写入基址。实际是 BG screen map 区域写入目标。

**需要修改的位置**:

1. `EQ_SLOTS` 表第 11 行 (DAT_0801d828):
   - const_name: `CARD_INFO_STAT_OBJ_TILE_BASE` → `CARD_INFO_STAT_BG_TILE_VRAM`
   - slot_label: `draw_atk_def_label_to_vram_obj_tile_base` → `draw_atk_def_label_to_vram_bg_tile_vram`

2. `card_info.inc` 新建内容:
   - `.equ CARD_INFO_STAT_OBJ_TILE_BASE, 0x06001c00` → `.equ CARD_INFO_STAT_BG_TILE_VRAM, 0x06001c00`
   - 注释改为: `@ BG screen-map tile-attr write base for ATK/DEF/Level lines (CB0, SB3+0x400)`

3. `REF_SLOTS` 表 DAT_0801d94c 行已在 Fix #1 中处理 (引用 CARD_INFO_STAT_BG_TILE_VRAM)。

---

## 附录：独立核验数据

### Carve A (sjis_char_fold_table)

```
host: ROM off 0x1e589a4..0x1e58d0c (0x368 B)
pre  = 0x1e589c4 - 0x1e589a4 = 0x20 B
table = 0x100 B (sjis_char_fold_table @ 0x09e589c4)
post = 0x1e58d0c - 0x1e58ac4 = 0x248 B
sum  = 0x20 + 0x100 + 0x248 = 0x368 == 0x368 PASS
First 16B: 000102030405060708090a0b0c0d0e0f (identity bytes)
```

### Carve B (124KB blob 三表)

```
host: ROM off 0x1832602..0x1850b1c (0x1e51a B)
pre              = 0x1cf4a B (到 card_digit_glyph_data @ 0x0984f54c)
card_digit_glyph_data = 0x50 B (10 digits × 8B/glyph)
card_label_glyph_buf  = 0x30 B (label glyphs @ 0x0984f59c)
card_glyph_table_3    = 0x1550 B (@ 0x0984f5cc → blob end 0x1850b1c)
sum = 0x1cf4a + 0x50 + 0x30 + 0x1550 = 0x1e51a == 0x1e51a PASS
```

### gCardInfoPageState 核

- ROM 值: 0x0201afb0 (在 EWRAM, 0x02020000 之前 — 与 gVijaState=0x02029eb0 不同区段)
- 全 ROM raw_refs: 20，thumb_refs: 0
- ewram.inc 扫描：无此地址，无 gCardInfoPageState 名称 — 新建合理

### BG VRAM 地址核

GBA VRAM 分区: BG `0x06000000-0x0600FFFF`; OBJ tile `0x06010000+`  
- 0x06001840 < 0x06010000 → BG VRAM 确认  
- 0x06001c00 < 0x06010000 → BG VRAM 确认  
- 0x06008200 < 0x06010000 → BG VRAM (CB2, SB16+0x200)  
- 0x06008580 < 0x06010000 → BG VRAM (CB2, SB16+0x580)

---

## Reviewer Verdict: f01-Seg-2 = NEEDS_FIX(2 items)
