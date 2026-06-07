# Refine Proposal: f01-Seg-4  [0x0801e36c..0x0801e714)

## 段测绘

- 函数入口 x8 (全部 < 0x1e714):
  | addr     | name                                  |
  |----------|---------------------------------------|
  | 0x1e36c  | update_card_info_page_state           |
  | 0x1e440  | card_info_page_entry                  |
  | 0x1e490  | draw_card_stat_digits_to_oam          |
  | 0x1e594  | draw_stat_row_sprites_to_oam          |
  | 0x1e620  | render_card_stats_oam_for_current_card|
  | 0x1e640  | card_list_on_select_to_info_page      |
  | 0x1e6cc  | open_card_info_by_icid                |
  | 0x1e6f4  | open_card_info_page_from_list         |

- 残留自动名槽 x20 (DAT_):
  All values verified via python against ROM (all OK).

  | addr     | current_label                         | value      |
  |----------|---------------------------------------|------------|
  | 0x1e3a8  | DAT_0801e3a8                          | 0x0201afb0 |
  | 0x1e438  | DAT_0801e438                          | 0x02000000 |
  | 0x1e43c  | DAT_0801e43c                          | 0x00006c2c |
  | 0x1e484  | DAT_0801e484                          | 0x0201afb0 |
  | 0x1e488  | DAT_0801e488                          | 0x02000000 |
  | 0x1e48c  | DAT_0801e48c                          | 0x00006c2c |
  | 0x1e4e4  | DAT_0801e4e4                          | 0x00060056 |
  | 0x1e4e8  | DAT_0801e4e8                          | 0x0000d3a2 |
  | 0x1e4ec  | DAT_0801e4ec                          | 0x00150058 |
  | 0x1e4f0  | DAT_0801e4f0                          | 0x0000e3a6 |
  | 0x1e518  | DAT_0801e518                          | 0x0000f001 |
  | 0x1e55c  | DAT_0801e55c                          | 0x0000f001 |
  | 0x1e560  | DAT_0801e560                          | 0x0201afb0 |
  | 0x1e564  | DAT_0801e564                          | 0x0000c3a8 |
  | 0x1e590  | DAT_0801e590                          | 0x0201afb0 |
  | 0x1e60c  | DAT_0801e60c                          | 0x00004040 |
  | 0x1e610  | DAT_0801e610                          | 0xfffff800 |
  | 0x1e614  | DAT_0801e614                          | 0xfffff804 |
  | 0x1e618  | DAT_0801e618                          | 0xfffff808 |
  | 0x1e61c  | DAT_0801e61c                          | 0xfffff80c |
  | 0x1e63c  | DAT_0801e63c                          | 0x0201afb0 |
  | 0x1e6b8  | DAT_0801e6b8                          | 0x0201afb0 |
  | 0x1e6bc  | DAT_0801e6bc                          | 0x00003fff |
  | 0x1e6c0  | DAT_0801e6c0                          | 0xfffe0007 |
  | 0x1e6c8  | DAT_0801e6c8                          | 0x0000ffff |
  | 0x1e710  | DAT_0801e710                          | 0x0201afb0 |

- 已符号化 PTR_ 槽 x3 (已有 .word <name>, 无需 EQ 操作):
  | addr     | label                                 | symbol           |
  |----------|---------------------------------------|------------------|
  | 0x1e38c  | PTR_gPrng_0801e38c                    | gPrng            |
  | 0x1e4e0  | PTR_card_stats_table_0801e4e0         | card_stats_table |
  | 0x1e6c4  | PTR_card_stats_table_0801e6c4         | card_stats_table |

- ROM_INCBIN / .byte 块: 0 (段内无)
- §5.1 登记: 0 (段内无未引用数据块)

---

## 数据块分类 (Rule 2/3)

段内无 ROM_INCBIN / .byte 数据块。跳过。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

EQ = 24 slots total. 按函数分组:

#### update_card_info_page_state (0x1e36c)

| slot_addr | slot_label (new)                                          | value      | const_name            | 来源 .inc           |
|-----------|-----------------------------------------------------------|------------|-----------------------|---------------------|
| 0x1e3a8   | update_card_info_page_state_gcardinfopagestate            | 0x0201afb0 | gCardInfoPageState    | ewram.inc (复用)    |
| 0x1e438   | update_card_info_page_state_ewram_base                    | 0x02000000 | EWRAM_BASE            | gba_mem.inc (复用)  |
| 0x1e43c   | update_card_info_page_state_gsettings_off                 | 0x00006c2c | GSETTINGS_OFFSET      | name_input.inc (复用)|

Evidence (R6): 0x1e3a8 — `ldr r0, DAT_0801e3a8; ldrh r1,[r0,#0x6]` reads countdown halfword from gCardInfoPageState+0x6, confirmed gCardInfoPageState=0x0201afb0 (ewram.inc:169). 0x1e438/0x1e43c — pattern `ldr r1,DAT_438; ldr r0,DAT_43c; adds r1,r1,r0` computes EWRAM_BASE + GSETTINGS_OFFSET = 0x02006c2c = gSettings; then `ldrb r1,[r1,#0x0]; ands r0,r1; ... bits[2:0]` reads gSettings settings byte, confirmed by name_input.inc:18 (GSETTINGS_OFFSET). Confidence: high (asm/01_vija_scene_text.s:3273-3356, ref Seg-2/Seg-3 identical pattern).

#### card_info_page_entry (0x1e440)

| slot_addr | slot_label (new)                                          | value      | const_name            | 来源 .inc           |
|-----------|-----------------------------------------------------------|------------|-----------------------|---------------------|
| 0x1e484   | card_info_page_entry_gcardinfopagestate                   | 0x0201afb0 | gCardInfoPageState    | ewram.inc (复用)    |
| 0x1e488   | card_info_page_entry_ewram_base                           | 0x02000000 | EWRAM_BASE            | gba_mem.inc (复用)  |
| 0x1e48c   | card_info_page_entry_gsettings_off                        | 0x00006c2c | GSETTINGS_OFFSET      | name_input.inc (复用)|

Evidence: 0x1e484 — `ldr r4,DAT_0801e484; ldr r0,[r4,#0x0]; lsls r0,r0,#0xf; lsrs r0,r0,#0x12` extracts card_id from gCardInfoPageState+0x0 bits[17:2] (asm:3362-3365). 0x1e488/0x1e48c — `ldr r1,DAT_488; ldr r2,DAT_48c; adds r1,r1,r2` = EWRAM_BASE+GSETTINGS_OFFSET, then `ldrb r1,[r1,#0x0]; ... bits[2:0]` reads gSettings (asm:3373-3376). Confidence: high.

#### draw_card_stat_digits_to_oam (0x1e490)

| slot_addr | slot_label (new)                                                | value      | const_name                   | 来源 .inc          |
|-----------|-----------------------------------------------------------------|------------|------------------------------|--------------------|
| 0x1e4e4   | draw_card_stat_digits_to_oam_atk_def_oam_xy                    | 0x00060056 | CARD_STAT_ATK_DEF_OAM_XY    | card_info.inc (新) |
| 0x1e4e8   | draw_card_stat_digits_to_oam_atk_def_attr2                     | 0x0000d3a2 | CARD_STAT_ATK_DEF_OAM_ATTR2 | card_info.inc (新) |
| 0x1e4ec   | draw_card_stat_digits_to_oam_qplay_oam_xy                      | 0x00150058 | CARD_STAT_QPLAY_OAM_XY      | card_info.inc (新) |
| 0x1e4f0   | draw_card_stat_digits_to_oam_qplay_attr2                       | 0x0000e3a6 | CARD_STAT_QPLAY_OAM_ATTR2   | card_info.inc (新) |
| 0x1e518   | draw_card_stat_digits_to_oam_digit_attr2_a                     | 0x0000f001 | CARD_STAT_DIGIT_OAM_ATTR2   | card_info.inc (新) |
| 0x1e55c   | draw_card_stat_digits_to_oam_digit_attr2_b                     | 0x0000f001 | CARD_STAT_DIGIT_OAM_ATTR2   | card_info.inc (复用 同上)|
| 0x1e560   | draw_card_stat_digits_to_oam_gcardinfopagestate_a              | 0x0201afb0 | gCardInfoPageState           | ewram.inc (复用)   |
| 0x1e564   | draw_card_stat_digits_to_oam_fusion_attr2                      | 0x0000c3a8 | CARD_STAT_FUSION_OAM_ATTR2  | card_info.inc (新) |
| 0x1e590   | draw_card_stat_digits_to_oam_gcardinfopagestate_b              | 0x0201afb0 | gCardInfoPageState           | ewram.inc (复用)   |

Evidence: 0x1e4e4/0x1e4e8 — first `write_oam_entry_from_packed_args(r0=0x00060056, r1=0x40, r2=0x0000d3a2)` call at asm:3415-3418; writes ATK/DEF frame OBJ at position (x=0x56=86, y=6). r2=0xd3a2 = attr2: pal=bits[15:12]=0xd=13 (matches CARD_FRAME_OBJ_PAL_MONSTER / slot 13), tile=bits[9:0]=0x3a2=930. ROM ref-scan: 0x00060056 appears 4× total (4 code slots: 0x801e4e4, 0x80def98, 0x80defd0, 0x80df028 — shared with deck info pages, confirming it is a common card-display constant worth naming). Confidence: high (asm:3395-3444).

0x1e4ec/0x1e4f0 — second `write_oam_entry_from_packed_args(r0=0x00150058, r1=0x0, r2=0x0000e3a6)` at asm:3429-3432; rendered only when card type==0x16 (Quick-Play Spell) AND field[9]!=0. (x=0x58=88, y=0x15=21). attr2 pal=14, tile=0x3a6=934. ROM scan: 0x00150058 appears 2× (0x1e4ec, 0x80df03c). Confidence: high.

0x1e518/0x1e55c — `r2=0x0000f001` passed to `write_oam_entry_from_packed_args` in two loop paths (asm:3460-3461, 3473-3474). attr2: pal=15, tile=1. Only 2 ROM occurrences, both in this function. Confidence: high.

0x1e564 — `r2=0x0000c3a8` for ATK/DEF icon write at asm:3488-3491 (path when `card_type & 0x2 != 0`). attr2: pal=12, tile=0x3a8=936. Only 1 ROM occurrence. Confidence: high (asm:01_vija_scene_text.s:3488-3491).

0x1e560 / 0x1e590 — both `0x0201afb0` = gCardInfoPageState (ewram.inc:169). Evidence: used to read `[gCardInfoPageState+0x2]` (type byte) at asm:3484 and `[gCardInfoPageState+0x2]` at asm:3517. Confidence: high.

#### draw_stat_row_sprites_to_oam (0x1e594)

| slot_addr | slot_label (new)                                           | value      | const_name                    | 来源 .inc          |
|-----------|------------------------------------------------------------|------------|-------------------------------|--------------------|
| 0x1e610   | draw_stat_row_sprites_to_oam_attr2_base_a                  | 0xfffff800 | CARD_STAT_ROW_ATTR2_BASE_A    | card_info.inc (新) |
| 0x1e614   | draw_stat_row_sprites_to_oam_attr2_base_b                  | 0xfffff804 | CARD_STAT_ROW_ATTR2_BASE_B    | card_info.inc (新) |
| 0x1e618   | draw_stat_row_sprites_to_oam_attr2_base_c                  | 0xfffff808 | CARD_STAT_ROW_ATTR2_BASE_C    | card_info.inc (新) |
| 0x1e61c   | draw_stat_row_sprites_to_oam_attr2_base_d                  | 0xfffff80c | CARD_STAT_ROW_ATTR2_BASE_D    | card_info.inc (新) |

Evidence: 0x1e610..0x1e61c — four consecutive slots, each used as `r2 = r5 + DAT`, then `lsls r2,r2,#0x10; lsrs r2,r2,#0x10` (u16-truncate) to produce attr2 for write_oam_entry_from_packed_args. With r5 = col_idx*0x10 + 2, the result encodes `(col*0x10 + 2 + offset) & 0xffff` as OAM attr2. Offsets differ by 4 = consecutive sprite tile groups for 4 sprite rows per display column. ROM ref-scan: 0xfffff800 appears 34× total but 33 refs are in compressed data regions (>0x09000000); only 1 code literal at 0x1e610. Confidence: med (semantics established from call pattern; exact tile-base layout requires mGBA render verification, but byte pattern is clear). New equates avoid raw hex in 4 symmetric slot labels.

#### render_card_stats_oam_for_current_card (0x1e620)

| slot_addr | slot_label (new)                                               | value      | const_name         | 来源 .inc        |
|-----------|----------------------------------------------------------------|------------|--------------------|-----------------|
| 0x1e63c   | render_card_stats_oam_for_current_card_gcardinfopagestate      | 0x0201afb0 | gCardInfoPageState | ewram.inc (复用)|

Evidence: `ldr r4,DAT_0801e63c; ldr r0,[r4,#0x0]; lsls r0,r0,#0xf; lsrs r0,r0,#0x12` — reads card_id from gCardInfoPageState+0x0 bits[17:2] (asm:3604-3607). Confidence: high.

#### card_list_on_select_to_info_page (0x1e640)

| slot_addr | slot_label (new)                                                    | value      | const_name                   | 来源 .inc          |
|-----------|---------------------------------------------------------------------|------------|------------------------------|--------------------|
| 0x1e6b8   | card_list_on_select_to_info_page_gcardinfopagestate                 | 0x0201afb0 | gCardInfoPageState           | ewram.inc (复用)   |
| 0x1e6bc   | card_list_on_select_to_info_page_card_id_mask                       | 0x00003fff | CARD_INFO_STATE_CARD_ID_MASK | card_info.inc (新) |
| 0x1e6c0   | card_list_on_select_to_info_page_card_id_clear                      | 0xfffe0007 | CARD_INFO_STATE_CARD_ID_CLEAR| card_info.inc (新) |

Evidence: 0x1e6b8 — `ldr r3,DAT_0801e6b8; ldr r0,[r3,#0x0]` reads gCardInfoPageState word0 (asm:3632-3636). Confidence: high.
0x1e6bc — `ldr r1,DAT_0801e6bc; ands r1,r4; lsls r1,r1,#0x3` extracts card_id field: `(card_id & 0x3fff) << 3` → places card_id into bits[16:3] of gCardInfoPageState word0. 0x3fff = mask for 14-bit card ID. ROM scan: 0x00003fff appears 46× total; code occurrences need checking (likely shared). Confidence: high (asm:3633-3635, pattern clear).
0x1e6c0 — `ldr r2,DAT_0801e6c0; ands r0,r2; orrs r0,r1` clears existing card_id field before writing new one: keeps bits[2:0] (flags) and bit17, clears bits[16:3] (card_id field). 0xfffe0007 = ~(0x1fff8) = preserve [17] and [2:0]. ROM scan: 0xfffe0007 appears 6×. Confidence: high (asm:3637-3639, R3 pattern).

#### open_card_info_page_from_list (0x1e6f4)

| slot_addr | slot_label (new)                                               | value      | const_name         | 来源 .inc        |
|-----------|----------------------------------------------------------------|------------|--------------------|-----------------|
| 0x1e710   | open_card_info_page_from_list_gcardinfopagestate               | 0x0201afb0 | gCardInfoPageState | ewram.inc (复用)|

Evidence: `ldr r1,DAT_0801e710; movs r0,#0x4; ldrb r2,[r1,#0x0]; orrs r0,r2; strb r0,[r1,#0x0]` — sets bit2 (0x4) in gCardInfoPageState+0x0 byte to mark card_info_page_active_flag (asm:3726-3730). Confidence: high.

---

### REF_SLOTS

No new REF_SLOTS needed. The three PTR_ pointer slots are already symbolized (`.word gPrng`, `.word card_stats_table` x2). Slot label renames for PTR_ slots are optional cosmetic changes not required.

---

### RENAME_SLOTS (raw value, no equate; just rename slot label)

| slot_addr | old_label       | new_label                                              | eol_ascii                                                                |
|-----------|-----------------|--------------------------------------------------------|--------------------------------------------------------------------------|
| 0x1e60c   | DAT_0801e60c    | draw_stat_row_sprites_to_oam_tile_r1                   | tile index 0x40 (=64) for stat row OBJ sprites; 71 ROM refs, not equated |
| 0x1e6c8   | DAT_0801e6c8    | card_list_on_select_to_info_page_no_stat_sentinel      | 0xffff sentinel: ATK/DEF field not applicable (Spell/Trap); 7616 ROM refs, not equated |

---

### FUNC_RENAME

None. All 8 function names accurately reflect their operation:
- `update_card_info_page_state`: reads input flags, adjusts scroll, toggles toggle bit — state update. indeg=1 (tick_card_info_page_by_state). Name accurate.
- `card_info_page_entry`: init + load + render full card page on enter. indeg=2. Name accurate.
- `draw_card_stat_digits_to_oam`: writes digit OBJ sprites for ATK/DEF/Level numbers. indeg=1. Name accurate.
- `draw_stat_row_sprites_to_oam`: writes 4-per-row OBJ sprites for stat display rows. indeg=1. Name accurate.
- `render_card_stats_oam_for_current_card`: calls both draw functions per frame. indeg=1. Name accurate.
- `card_list_on_select_to_info_page`: opens card info page from list select event. Name accurate.
- `open_card_info_by_icid`: adapter icid->cid then open. Name accurate.
- `open_card_info_page_from_list`: direct cid entry for card list dispatchers. Name accurate.

---

### PLATE (R5)

Five plate changes needed:

#### 1. card_info_page_entry (line 3358) — CJK -> ASCII
Old (line 3358): `@ p1/p2: 卡牌信息页顶层, card_id=(word0<<15)>>18`
New: `@ Top-level card info page init: decodes card image, renders name+description+stats. card_id = (state.word0 << 15) >> 18.`
Reason: CJK present (R5 zero-tolerance). Content: accurate ASCII description of function body (card_image_decode_wrapper + render_card_name_to_desc_page_vram + card_data_query + render_card_description_text + card_info_page_finalize, asm:3360-3387). Confidence: high.

#### 2. card_list_on_select_to_info_page (line 3618) — CJK -> ASCII
Old (line 3618): `@ TG.4-next: 卡列表按 A 进详情页的派发, 首 bl 即 card_info_page_enter_with_card_id`
New: `@ Card-list dispatch to card info page on select. First bl: card_info_page_enter_with_card_id. Encodes card_id into gCardInfoPageState word0 bits[16:3]; loads ATK/DEF from card_stats_table.`
Reason: CJK present. Updated with accurate field descriptions. Confidence: high (asm:3619-3690).

#### 3. draw_card_stat_digits_to_oam (line 3395) — remove stale FUN_ address
Old: `@ Called by render_card_stats_oam_for_current_card (FUN_0801e620).`
New: `@ Called by render_card_stats_oam_for_current_card.`
Reason: parenthetical FUN_ address is stale since function is named. Confidence: high.

#### 4. draw_stat_row_sprites_to_oam (line 3529) — remove stale FUN_ address
Old: `@ Called by render_card_stats_oam_for_current_card (FUN_0801e620).`
New: `@ Called by render_card_stats_oam_for_current_card.`
Reason: same as above. Confidence: high.

#### 5. render_card_stats_oam_for_current_card (line 3601) — remove stale FUN_ address
Old: `@ Called every frame by tick_card_info_page_by_state (FUN_0801e714).`
New: `@ Called every frame by tick_card_info_page_by_state.`
Reason: function at 0x1e714 is now named. Confidence: high.

---

## carve 计划 (R7)

无段内 ROM_INCBIN / .byte 数据块。无 carve 动作。

---

## disasm 计划 (R4)

无误标代码块。`.hword 0x46xx` 项均为合法 THUMB 高寄存器 MOV 指令 (mov ip,r2 / mov r9,r1 / mov r8,r8 / mov r0,r8 / mov r1,r8 / mov ip,r0 / mov r1,r9)，由 Ghidra 未解码的高寄存器传递，保持原样。

---

## 新增 constants (card_info.inc 追加)

核实现有 card_info.inc 无同值条目 (grep 验证: 0x00060056 / 0x0000d3a2 / 0x00150058 / 0x0000e3a6 / 0x0000f001 / 0x0000c3a8 / 0xfffff800 / 0xfffff804 / 0xfffff808 / 0xfffff80c / 0x00003fff / 0xfffe0007 均不在 constants/ 中)。

```
@ --- Seg-4 additions (draw_card_stat_digits_to_oam / draw_stat_row_sprites_to_oam) ---

@ OAM packed constants for card stat digit sprites (write_oam_entry_from_packed_args: r0=packed_xy, r1=tile_idx, r2=attr2)
@ packed_xy format: low16=x_coord (9-bit), high16=oam_y
.equ CARD_STAT_ATK_DEF_OAM_XY,    0x00060056  @ ATK/DEF frame OBJ position (x=86, y=6)
.equ CARD_STAT_ATK_DEF_OAM_ATTR2, 0x0000d3a2  @ ATK/DEF frame attr2: pal13, tile0x3a2; 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_XY,      0x00150058  @ Quick-Play Spell secondary marker pos (x=88, y=21)
.equ CARD_STAT_QPLAY_OAM_ATTR2,   0x0000e3a6  @ Quick-Play marker attr2: pal14, tile0x3a6; 2 ROM refs
.equ CARD_STAT_DIGIT_OAM_ATTR2,   0x0000f001  @ ATK/DEF digit sprite attr2: pal15, tile1; 2 ROM refs (both in draw_card_stat_digits_to_oam)
.equ CARD_STAT_FUSION_OAM_ATTR2,  0x0000c3a8  @ Fusion/extra-type marker attr2: pal12, tile0x3a8; 1 ROM ref

@ OAM attr2 base offsets for stat row sprites (draw_stat_row_sprites_to_oam)
@ Added to r5 (col_idx*0x10 + 2) then u16-truncated to produce attr2 per row
.equ CARD_STAT_ROW_ATTR2_BASE_A,  0xfffff800  @ stat row sprite group A attr2 base (row 0, Y=0x70)
.equ CARD_STAT_ROW_ATTR2_BASE_B,  0xfffff804  @ stat row sprite group B attr2 base (row 1, Y=0x90)
.equ CARD_STAT_ROW_ATTR2_BASE_C,  0xfffff808  @ stat row sprite group C attr2 base (row 2, Y=0xb0)
.equ CARD_STAT_ROW_ATTR2_BASE_D,  0xfffff80c  @ stat row sprite group D attr2 base (row 3, Y=0xd0)

@ gCardInfoPageState.word0 bit-field masks (card_list_on_select_to_info_page)
@ word0 layout: bits[2:0]=flags, bits[16:3]=card_id (14-bit), bit17=active_flag
.equ CARD_INFO_STATE_CARD_ID_MASK,  0x00003fff  @ mask for card_id bits[13:0] before shift-3 into word0
.equ CARD_INFO_STATE_CARD_ID_CLEAR, 0xfffe0007  @ AND mask to clear card_id field bits[16:3], preserve [17]+[2:0]
```

---

## §5.1 登记 (Rule 3)

なし。段内無未引用數據塊。

---

## 消費者証據 (R6)

已在各 EQ_SLOT 条目内给出 file:line。关键全局:
- `gCardInfoPageState` = 0x0201afb0: ewram.inc:169, confirmed by asm/01_vija_scene_text.s:3274 (DAT_0801e3a8 in Seg-3 end context), 3389 (Seg-4 card_info_page_entry), all slot reads for field extractions. Confidence: high.
- `EWRAM_BASE` + `GSETTINGS_OFFSET` pattern: confirmed by asm:3273-3276, 3329-3333 — identical to Seg-2/Seg-3 pattern where gSettings = 0x02000000 + 0x00006c2c = 0x02006c2c. Confidence: high.
- `card_stats_table`: already symbolized (PTR_ slots show `.word card_stats_table`). Confidence: high.
- OAM packed constants: verified via write_oam_entry_from_packed_args call signature (asm/21_font_title_scene.s:4868-4869 function body); r0=packed_xy, r1=tile_idx, r2=attr2. Confidence: high.

---

## 求助

None. All slots have high/med confidence with file:line evidence.

Note (med confidence): CARD_STAT_ROW_ATTR2_BASE_A..D semantics (stat row tile groups per display column) inferred from loop structure — mGBA screenshot would confirm tile layout but byte pattern is unambiguous. Flagged as med confidence but does not block EQ action since the equate names accurately reflect usage (base offset for attr2 per row).
