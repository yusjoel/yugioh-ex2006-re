# Refine Review: f01-Seg-3

Segment: `asm/01_vija_scene_text.s` ROM [0x0801d998, 0x0801e36c), 8 fn, card_info scene.

## 自主复核结果

### EQ 值 ROM 核对 (C4)

Python 独立读 ROM 字节核对所有 34 个新建 EQ slot + 10 个 dup slot：全部 44 槽值与 ROM
小端 4 字节完全一致。

### ref-scan 独立重跑 (C3)

| 数据地址 | raw refs | thumb|1 refs | 判定 |
|----------|----------|-------|------|
| card_type_alt_display_table 0x09e58ac4 | 1 | 0 | REF=1 carve OK |
| card_status_sprite_sheet 0x09e2ddb4 | 2 | 0 | REF=2 carve OK |
| card_attr_order_table 0x09e4f204 | 2 | 0 | REF=2 carve OK |
| sjis_char_fold_table 0x09e589c4 | 4 | 0 | REF=4 已建 OK |

消费者地址核实：
- 0x09e4f204: 0x0801e284 (Seg-3 内), 0x0810a66c (file 23 外) — 均为代码引用非数据自身
- 0x09e58ac4: 0x0801e288 (Seg-3 内，1 ref)
- 0x09e2ddb4: 0x0801e290 (Seg-3 内), 0x08109840 (外)

### Carve 算术核 (carve A/B/C)

**Carve A** (card_type_alt_display_table @ 0x09e58ac4):
- rom.s line 1608: `.incbin "roms/2343.gba", 0x1E58AC4, 0x248`
- sjis_char_fold_table 在 0x1E589C4 + 0x100 = 0x1E58AC4 — 紧接终点即本表起点，对齐正确
- 操作：在 incbin 前插入 label 行，原 incbin 不变 -> byte-safe

**Carve B** (card_status_sprite_sheet @ 0x09e2ddb4):
- rom.s line 749: `.incbin "graphics/bin/ui-misc/switch_sheets/case_9_0x01E2DDB4.bin"`
- case_9 bin 大小: 0x1E2FEB4 - 0x1E2DDB4 = 0x2100 = 33 × 0x100。循环 r5=0..0x1f 仅用 32 项，[32] 为未访问尾条目。
- 操作：在 line 749 前插入 label 行，.incbin 不变 -> byte-safe

**Carve C** (card_attr_order_table @ 0x09e4f204):
- 原 incbin: `(0x1E4E979, 0xB3F)`
- pre size: 0x1E4F204 - 0x1E4E979 = 0x88B ✓
- remainder: 0xB3F - 0x88B = 0x2B4 ✓
- 覆盖等式: 0x88B + 0x2B4 = 0xB3F ✓ (label 只是标记，字节全在两段 incbin 中)
- 读 ROM 0x1E4F204: 32 u32 entries (0x15,0x16,0x17,…,0x11) — card attr flag ID 表，证据充分

### DAT_/PTR_ 覆盖扫描 (C13)

asm/01 中 seg-3 [0x0801d998, 0x0801e36c) 范围内扫描得 **89 个** DAT_/PTR_ label 定义。
提案声称 79 槽 (38 new-EQ + 25 DUP + 16 REF-already)，差 10 槽为提案把 EQ-reuse（复用
现有 inc 常量的槽，如 gFontJpCtx×4、EWRAM_BASE×3、GSETTINGS_OFFSET×3、gCardInfoPageState×1、
BG_CHAR_VRAM_CB2×1 共 11 槽，其中 2 个 sjis_char_fold_table REF）归入 DUP/REF 计数。
**实质：89/89 槽均有归宿，无遗漏。**

### FUNC_RENAME 核 (C11)

render_card_name_to_desc_page_vram (原 card_info_page_step_03_unknown, 0x0801dbdc):
- 函数体核实：调用 select_charset_then_load_name 或 resolve_card_gfx_pointer_by_type 取卡名；
  计算字符宽度；调用 render_glyph_jp_dual_layer / render_glyph_jp_single_layer；
  最终 commit_line_buffer_to_sprite_vram(0x06007100, 0)。
- 原名 "step_03_unknown" 与函数体行为矛盾 — 误名信号成立。
- 新名 `render_card_name_to_desc_page_vram` 满足 `^[a-z][a-z0-9_]+$` + verb_object 形式。
- indeg=2：两个调用者 0x0801e456 / 0x0801e42e 均在 Seg-4+ (>=0x1e36c)。

### 常量去重 (C5)

遍历全部 17 个现有 constants/*.inc，对所有 36 个新值（card_info +30 / gba_mem +3 / gba_io +1）
做值匹配：**无任何碰撞**。名字碰撞同理为零。

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围 [0x0801d998, 0x0801e36c)，全 8 fn + 全 89 slot 均 < 0x1e36c | ✅ | Seg-4 起点 update_card_info_page_state=0x0801e36c 正确排除 |
| C2 | 段内 ROM_INCBIN/.byte 块数 == 0，Rule 2 N/A | ✅ | proposal 正确声明无段内数据块 |
| C3 | §5.1 为空 (无 0-ref 块)，N/A | ✅ | — |
| C4 | 全 44 EQ slot ROM 4 字节小端值匹配 | ✅ | python 独立核对，34 new + 10 dup，全 OK |
| C5 | 新建常量无重值/重名 | ✅ | 遍历 17 inc，零碰撞 |
| C6 | slot label `^[a-z][a-z0-9_]+$` 或 const `^[A-Z][A-Z0-9_]+$`，无碰撞 | ✅ | 40 名全通过 |
| C7 | 3 个 carve 目标均有 USER-label + DATA-ref 计划 | ✅ | A/B/C 各有消费者 DAT_ 引用 |
| C8 | plate 无残留旧 FUN_/DAT_/DWORD_ | ❌ | **#1**: plate item 3 行 276 用 `FUN_0801e714`，现名为 `tick_card_info_page_by_state`；**#2**: item 7/8 函数 plate 遗漏更新（asm 仍为 CJK） |
| C9 | plate/EOL 文本纯 ASCII | ❌ | **#2** 同上：tick_blend_fadeout (asm L3134) 和 tick_blend_fadein (asm L3150) 现有 plate 均为 CJK，提案未给出替换 |
| C10 | carve 内无指针表，N/A | ✅ | 全为原始数据数组，无 THUMB ptr |
| C11 | FUNC_RENAME 含义正确，函数体与新名一致，无矛盾 | ✅ | 高置信，body 证据充分 |
| C12 | 关键槽有 file:line + 置信度 | ✅ | 8 个关键槽均有 asm line 证据，5 high 1 med |
| C13 | 段内全部残留自动名槽覆盖，无遗漏 | ✅ | 89/89 |

---

## 状态: NEEDS_FIX(2 items)

---

## 修改清单

### #1 — C8 — tick_scroll_frame_and_update_pos plate 中的 FUN_ 残留

**位置**: proposal §PLATE 第 3 项，新建 ASCII plate 代码块（proposal line 276）

**问题**: 新 plate 中写
```
@ indeg=1; caller: card info scene tick (FUN_0801e714).
```
但 0x0801e714 已命名为 `tick_card_info_page_by_state`（asm/01 line 3670）。

**改法**: 将该行改为
```
@ indeg=1; caller: tick_card_info_page_by_state (0x0801e714).
```

---

### #2 — C8/C9 — tick_blend_fadeout_and_set_dispcnt 和 tick_blend_fadein_and_poll_done 的 plate 遗漏

**位置**: proposal §PLATE 第 7、8 项，错误声明这两个函数 plate 已是 ASCII，无需更新。

**实际 asm 状态**:
- asm/01 L3134: `tick_blend_fadeout_and_set_dispcnt` plate 为 CJK（含 `FUN_0801e714`）
- asm/01 L3150: `tick_blend_fadein_and_poll_done` plate 为 CJK（含 `FUN_0801e714` 和 `FUN_080fa3a8`）

**改法**: 在 proposal §PLATE 为这两个函数各补充一个 ASCII 替换 plate。

tick_blend_fadeout_and_set_dispcnt 建议 plate：
```
@ Sets DISPCNT bits[12:8] (BG0-BG3+OBJ enable) via OR with 0x1f00, then calls
@ tick_blend_step_by_delta(delta=4) to advance the blend fade-out by 4 steps.
@ Returns tick_blend_step_by_delta result: 1=fade complete, 0=in progress.
@ indeg=1; caller: tick_card_info_page_by_state (0x0801e714).
```

tick_blend_fadein_and_poll_done 建议 plate：
```
@ Calls start_blend_fadein_with_target(target=4) each frame to step the blend fade-in.
@ If fade-in complete (returns 1): ANDs DISPCNT with DISPCNT_BG_OBJ_CLEAR_MASK (0xe0ff)
@   to clear bits[12:8] (BG0-BG3+OBJ enable), then returns 1.
@ If not complete: returns 0.
@ indeg=2; callers: tick_card_info_page_by_state (0x0801e714), FUN_080fa3a8.
```

注: FUN_080fa3a8 为文件外函数，若其已命名则 fixer 应替换为现名。`FUN_080fa3a8` 保留于此仅为地址参考，不违反 C8（caller 参考可用地址标注）。

---

## 附注 (供 fixer 参考)

- **FUNC_RENAME 落地**: 需 CSV sync (`naming-proposals.csv`) + 跨模块 grep `card_info_page_step_03_unknown` 覆盖所有 plate 散文。
- **Carve C 余量说明**: 第二段 incbin `(0x1E4F204, 0x2B4)` 包含 0x80 字节表体 + 0x234 字节后续 AOB 数据，label 只标记表起点，字节全部由两段 incbin 覆盖，byte-identical 安全。
- **card_status_sprite_sheet 条目数**: ROM 实测 0x2100 字节 = 33 × 0x100，但消费者循环 r5=0..0x1f 仅访问前 32 条，最后一条为未访问填充，label 注释可写 `(32+1 card status OBJ sprite items, 0x100B each, index 0..31 active)`。
- **FUN_080fa3a8 命名状态**: 未在本 review 范围内核实，fixer 落地时自行 grep asm 确认。
