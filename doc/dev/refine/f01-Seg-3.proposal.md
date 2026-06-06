# Refine Proposal: f01-Seg-3  [0x0801d998..0x0801e36c)

## 段测绘

- 函数入口: 8 fn (全部 < 0x1e36c)

| 地址 | 当前名 | 行号 |
|------|--------|------|
| 0x0801d998 | card_image_decode_wrapper | 1893 |
| 0x0801dbdc | card_info_page_step_03_unknown | 2169 |
| 0x0801dfa0 | tick_scroll_frame_and_update_pos | 2662 |
| 0x0801e000 | render_card_description_text | 2718 |
| 0x0801e100 | card_info_page_finalize | 2847 |
| 0x0801e294 | blit_glyph_2x2_to_bg_vram | 3060 |
| 0x0801e328 | tick_blend_fadeout_and_set_dispcnt | 3135 |
| 0x0801e344 | tick_blend_fadein_and_poll_done | 3151 |

- 残留自动名槽: 79 槽 (38 new-EQ + 25 DUP-reuse + 16 REF-already-named)
  DAT_ 槽分布: card_image_decode_wrapper 22 槽, card_info_page_step_03_unknown 29 槽,
  tick_scroll_frame_and_update_pos 3 槽, render_card_description_text 6 槽,
  card_info_page_finalize 11 槽, blit_glyph_2x2_to_bg_vram 4 槽,
  tick_blend_fadein_and_poll_done 1 槽
- ROM_INCBIN / .byte 块: 0 (路线图正确, 段内无 ROM_INCBIN)

## 数据块分类 (Rule 2/3) -- ref-scan 证据

无段内 ROM_INCBIN 或 .byte 未分化块。Rule 2/3 不适用于本段。

ROM 远端数据被本段引用(在 rom.s 的 incbin 中):

| 数据地址 | raw refs | 判定 | 位置 |
|----------|----------|------|------|
| 0x09e589c4 | 4 | REF-已建 sjis_char_fold_table (rom.s line 1606) | rom.s line 1607 |
| 0x09e58ac4 | 1 | carve: sjis_char_fold_table+0x100, incbin(0x1E58AC4,0x248) 起点 | rom.s line 1608 |
| 0x09e2ddb4 | 2 | carve: switch_sheets/case_9 .bin 起点 (已 .include, 需加 label) | rom.s line 749 |
| 0x09e4f204 | 2 | carve: within incbin(0x1E4E979,0xB3F) off+0x88b | rom.s line 1458 |
| 0x09ccd2d0 | 5 | REF: name_o_palette_data+0x40 (within incbin after palette) | rom.s line 685 |
| 0x0984xxxx (×16) | 1-5 each | EQ in rom.s seg-C blob (0x1832602,0x1CF4A) | rom.s line 124 |
| 0x0985004c | 1 | EQ: card_glyph_table_3+0xa80 | within rom.s line 130 |
| 0x09850934 | 1 | EQ: card_glyph_table_3+0x1368 | within rom.s line 130 |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 复用现有 inc 或新建 card_info.inc)

全部 79 个 DAT_/PTR_ 槽按函数分组。

---

#### Fn-1: card_image_decode_wrapper (0x0801d998)

| 槽 | ROM值 | const名 | 槽label | inc | 操作 |
|----|-------|---------|---------|-----|------|
| PTR_card_stats_table_0801da8c | card_stats_table | - | card_image_decode_wrapper_stats_tbl | - | REF-already 跳过 |
| DAT_0801da90 | 0x0985004c | CARD_TILE_PACK_GLYPH_OFF_A | card_image_decode_wrapper_tile_a | card_info.inc | EQ-新建 |
| DAT_0801da94 | 0x0000020e | CARD_TILE_PACK_MAP_PARAM | card_image_decode_wrapper_map_param | card_info.inc | EQ-新建 |
| DAT_0801da98 | 0x09850934 | CARD_TILE_PACK_GLYPH_OFF_B | card_image_decode_wrapper_tile_b | card_info.inc | EQ-新建 |
| DAT_0801da9c | 0x0984a3fc | CARD_FRAME_TILE_SRC_MONSTER | card_image_decode_wrapper_tile_c | card_info.inc | EQ-新建 |
| DAT_0801daa0 | 0x050000a0 | CARD_FRAME_BG_PAL_BASE | card_image_decode_wrapper_bg_pal | card_info.inc | EQ-新建 |
| DAT_0801daa4 | 0x050003a0 | CARD_FRAME_OBJ_PAL_MONSTER | card_image_decode_wrapper_obj_pal_a | card_info.inc | EQ-新建 |
| DAT_0801daa8 | 0x0984dd6c | CARD_FRAME_PAL_SRC_MONSTER_A | card_image_decode_wrapper_pal_a | card_info.inc | EQ-新建 |
| DAT_0801daac | 0x06017440 | CARD_FRAME_OBJ_TILE_BASE | card_image_decode_wrapper_obj_tile | card_info.inc | EQ-新建 |
| DAT_0801dab0 | 0x0984d8ec | CARD_FRAME_TILE_SRC_MONSTER_A | card_image_decode_wrapper_tile_d | card_info.inc | EQ-新建 |
| DAT_0801dab4 | 0x06010020 | CARD_FRAME_OBJ_TILE_SLOT1 | card_image_decode_wrapper_tile_s1 | card_info.inc | EQ-新建 |
| DAT_0801dab8 | 0x09ccd2d0 | CARD_OVERLAY_TILE_SRC | card_image_decode_wrapper_overlay | card_info.inc | EQ-新建 (name_o+0x40) |
| DAT_0801db10 | 0x0984b994 | CARD_FRAME_TILE_SRC_SPELL | card_image_decode_wrapper_tile_e | card_info.inc | EQ-新建 |
| DAT_0801db14 | 0x050000a0 | CARD_FRAME_BG_PAL_BASE | card_image_decode_wrapper_bg_pal_b | card_info.inc | EQ-复用同值 |
| DAT_0801db18 | 0x050003a0 | CARD_FRAME_OBJ_PAL_MONSTER | card_image_decode_wrapper_obj_pal_b | card_info.inc | EQ-复用同值 |
| DAT_0801db1c | 0x0984de6c | CARD_FRAME_PAL_SRC_SPELL_A | card_image_decode_wrapper_pal_b | card_info.inc | EQ-新建 |
| DAT_0801db20 | 0x06017440 | CARD_FRAME_OBJ_TILE_BASE | card_image_decode_wrapper_obj_tile_b | card_info.inc | EQ-复用同值 |
| DAT_0801db24 | 0x0984dcec | CARD_FRAME_TILE_SRC_SPELL_A | card_image_decode_wrapper_tile_f | card_info.inc | EQ-新建 |
| DAT_0801db28 | 0x050003c0 | CARD_FRAME_OBJ_PAL_SPELL | card_image_decode_wrapper_obj_pal_c | card_info.inc | EQ-新建 |
| DAT_0801db2c | 0x0984f52c | CARD_FRAME_PAL_SRC_STAR_A | card_image_decode_wrapper_pal_c | card_info.inc | EQ-新建 |
| DAT_0801db30 | 0x060174c0 | CARD_LEVEL_OBJ_TILE_BASE | card_image_decode_wrapper_star_tile | card_info.inc | EQ-新建 |
| (db90-dbb4 dup block) | (同上各值dup) | 复用对应 const | card_image_decode_wrapper_pal_d/_tile_g 等 | card_info.inc | EQ-复用 |

注: db90=0x0984b994(同db10), db94=0x050000a0(同daa0), db98=0x050003a0(同daa4),
    db9c=0x0984de4c(新-CARD_FRAME_PAL_SRC_MONSTER_B), dba0=0x06017440(同daac),
    dba4=0x0984dc6c(新-CARD_FRAME_TILE_SRC_STAR), dba8=0x050003c0(同db28),
    dbac=0x0984f52c(同db2c), dbb0=0x060174c0(同db30),
    dbb4=0x0984f46c(新-CARD_FRAME_TILE_SRC_STAR_B)

---

#### Fn-2: card_info_page_step_03_unknown (0x0801dbdc)

所有槽均为已知全局的重复引用:

| 槽 | ROM值 | const名 | 操作 |
|----|-------|---------|------|
| DAT_0801dc28 | 0x02006ed0 | gFontJpCtx | EQ-复用 ewram.inc |
| DAT_0801dc2c | 0x02000000 | EWRAM_BASE | EQ-复用 gba_mem.inc |
| DAT_0801dc30 | 0x00006c2c | GSETTINGS_OFFSET | EQ-复用 name_input.inc |
| DAT_0801dc34 | 0x0201afb0 | gCardInfoPageState | EQ-复用 ewram.inc |
| DAT_0801dc9c | 0x02000000 | EWRAM_BASE | DUP-复用 |
| DAT_0801dca0 | 0x00006c2c | GSETTINGS_OFFSET | DUP-复用 |
| DAT_0801dca4 | 0x02006ed0 | gFontJpCtx | DUP-复用 |
| PTR_font_jp_base_table_0801dca8 | font_jp_base_table | - | REF-already 跳过 |
| DAT_0801dd04 | 0x02006ed0 | gFontJpCtx | DUP-复用 |
| PTR_font_jp_base_table_0801dd08 | font_jp_base_table | - | REF-already 跳过 |
| DAT_0801dd0c | 0x09e589c4 | sjis_char_fold_table | REF-复用 rom.s label |
| DAT_0801dd90 | 0x0201afb0 | gCardInfoPageState | DUP-复用 |
| DAT_0801dd94 | 0x02000000 | EWRAM_BASE | DUP-复用 |
| DAT_0801dd98 | 0x00006c2c | GSETTINGS_OFFSET | DUP-复用 |
| DAT_0801dd9c | 0x02006ed0 | gFontJpCtx | DUP-复用 |
| PTR_font_jp_base_table_0801dda0 | font_jp_base_table | - | REF-already 跳过 |
| DAT_0801ddf0 | 0x00008008 | CARD_DESC_RENDER_PARAM | EQ-新建 card_info.inc |
| DAT_0801de30 | 0x02006ed0 | gFontJpCtx | DUP-复用 |
| PTR_font_jp_base_table_0801de34 | font_jp_base_table | - | REF-already 跳过 |
| DAT_0801de84 | 0x02006ed0 | gFontJpCtx | DUP-复用 |
| PTR_font_jp_base_table_0801de88 | font_jp_base_table | - | REF-already 跳过 |
| DAT_0801de8c | 0x09e589c4 | sjis_char_fold_table | REF-复用 rom.s label |
| DAT_0801df48 | 0x00008008 | CARD_DESC_RENDER_PARAM | DUP-复用 |
| DAT_0801df4c | 0x06007100 | CARD_DESC_LINE_BUF_VRAM | EQ-新建 card_info.inc |
| DAT_0801df50 | 0x0201afb0 | gCardInfoPageState | DUP-复用 |
| PTR_gPrng_0801df54 | gPrng | - | REF-already 跳过 |
| DAT_0801df58 | 0x06000800 | CARD_DESC_BG_VRAM_A | EQ-新建 card_info.inc |
| DAT_0801df94 | 0x06000c80 | CARD_DESC_BG_VRAM_B | EQ-新建 card_info.inc |
| DAT_0801df98 | 0x0201afb0 | gCardInfoPageState | DUP-复用 |
| PTR_gPrng_0801df9c | gPrng | - | REF-already 跳过 |

---

#### Fn-3: tick_scroll_frame_and_update_pos (0x0801dfa0)

| 槽 | ROM值 | const名 | 操作 |
|----|-------|---------|------|
| DAT_0801dfd0 | 0x0201afb0 | gCardInfoPageState | EQ-复用 ewram.inc |
| PTR_gPrng_0801dffc | gPrng | - | REF-already 跳过 |

注: plate comment 中 "VRAM 0x03000240" 描述有误; 实际写入地址 = gPrng + 0x1e2 = 0x03000040+0x1e2 = 0x03000222 (IWRAM BG3VOFS shadow); 需 R5 订正。

---

#### Fn-4: render_card_description_text (0x0801e000)

| 槽 | ROM值 | const名 | 操作 |
|----|-------|---------|------|
| DAT_0801e0e8 | 0x02006ed0 | gFontJpCtx | EQ-复用 ewram.inc |
| DAT_0801e0ec | 0x02000000 | EWRAM_BASE | EQ-复用 gba_mem.inc |
| DAT_0801e0f0 | 0x00006c2c | GSETTINGS_OFFSET | EQ-复用 name_input.inc |
| PTR_font_jp_base_table_0801e0f4 | font_jp_base_table | - | REF-already 跳过 |
| DAT_0801e0f8 | 0x0201afb0 | gCardInfoPageState | EQ-复用 ewram.inc |
| DAT_0801e0fc | 0x06010040 | CARD_DESC_OBJ_TILE_BASE | EQ-新建 card_info.inc |

---

#### Fn-5: card_info_page_finalize (0x0801e100)

| 槽 | ROM值 | const名 | 操作 |
|----|-------|---------|------|
| PTR_card_stats_table_0801e18c | card_stats_table | - | REF-already 跳过 |
| DAT_0801e190 | 0x0201afb0 | gCardInfoPageState | EQ-复用 ewram.inc |
| DAT_0801e194 | 0x05000380 | CARD_FRAME_OBJ_PAL_LEVEL | EQ-新建 card_info.inc |
| DAT_0801e198 | 0x0984f3ac | CARD_FRAME_PAL_SRC_ICON_B | EQ-新建 card_info.inc |
| DAT_0801e19c | 0x06017500 | CARD_SPELL_OBJ_TILE_BASE | EQ-新建 card_info.inc |
| DAT_0801e1a0 | 0x0984f0ac | CARD_FRAME_TILE_SRC_ICON | EQ-新建 card_info.inc |
| DAT_0801e270 | 0x05000380 | CARD_FRAME_OBJ_PAL_LEVEL | DUP-复用 |
| DAT_0801e274 | 0x0984ee2c | CARD_FRAME_PAL_SRC_ICON_A | EQ-新建 card_info.inc |
| DAT_0801e278 | 0x06017500 | CARD_SPELL_OBJ_TILE_BASE | DUP-复用 |
| DAT_0801e27c | 0x0984e42c | CARD_FRAME_TILE_SRC_SPELL_B | EQ-新建 card_info.inc |
| DAT_0801e280 | 0x0201afb0 | gCardInfoPageState | DUP-复用 |
| DAT_0801e284 | 0x09e4f204 | card_attr_order_table | REF-carve (见 carve 计划) |
| DAT_0801e288 | 0x09e58ac4 | card_type_alt_display_table | REF-carve (见 carve 计划) |
| DAT_0801e28c | 0x06017580 | CARD_ICON_OBJ_TILE_BASE | EQ-新建 card_info.inc |
| DAT_0801e290 | 0x09e2ddb4 | card_status_sprite_sheet | REF-carve (见 carve 计划) |

---

#### Fn-6: blit_glyph_2x2_to_bg_vram (0x0801e294)

| 槽 | ROM值 | const名 | 操作 |
|----|-------|---------|------|
| DAT_0801e318 | 0x06004000 | BG_CHAR_VRAM_CB2 | EQ-复用 gba_mem.inc |
| DAT_0801e31c | 0x06000002 | BG_SCREEN_TILE_OFF_1 | EQ-新建 gba_mem.inc |
| DAT_0801e320 | 0x06000040 | BG_SCREEN_ROW1_OFF | EQ-新建 gba_mem.inc |
| DAT_0801e324 | 0x06000042 | BG_SCREEN_ROW1_TILE1 | EQ-新建 gba_mem.inc |

注: BG_CHAR_VRAM_CB2=0x06004000 已在 gba_mem.inc; 其余 3 个 BG screen map offset 常量应放 gba_mem.inc。

---

#### Fn-7: tick_blend_fadeout_and_set_dispcnt (0x0801e328)

无 DAT_ 槽 (仅 inline 立即数 0x1f00 = `movs#0xf8;lsls#5`; 已有 DISPCNT=0x04000000 in gba_io.inc)。

---

#### Fn-8: tick_blend_fadein_and_poll_done (0x0801e344)

| 槽 | ROM值 | const名 | 操作 |
|----|-------|---------|------|
| DAT_0801e368 | 0x0000e0ff | DISPCNT_BG_OBJ_CLEAR_MASK | EQ-新建 gba_io.inc |

---

### REF_SLOTS (USER-label + DATA-ref)

已由 Seg-2 建立并在本段 REF 的全局:
- `gCardInfoPageState` (0x0201afb0): 多次 REF, 已 ewram.inc
- `gFontJpCtx` (0x02006ed0): 多次 REF, 已 ewram.inc
- `card_stats_table`: 已 carve
- `font_jp_base_table`: 已 carve
- `gPrng`: 已 iwram.inc
- `sjis_char_fold_table` (0x09e589c4): 已 carve (rom.s line 1606)
- `card_attr_order_table` (0x09e4f204): 新增 carve (见下)
- `card_type_alt_display_table` (0x09e58ac4): 新增 carve (见下)
- `card_status_sprite_sheet` (0x09e2ddb4): 新增 label (见下)

### RENAME_SLOTS (纯改名 + EOL)

以下 DAT_ 槽改为含义名 (Ghidra rename label + optional EOL):
共约 38 个 new-EQ 槽需要改名。按函数分别在 Ghidra 脚本中执行。
完整列表见 EQ_SLOTS 表格的 `槽label` 列。

关键槽命名规则: `<func>_<semantic>` 形式避免 GAS PC-relative value-too-big 碰撞。

### FUNC_RENAME

| 当前名 | 新名 | indeg | 证据 |
|--------|------|-------|------|
| card_info_page_step_03_unknown | render_card_name_to_desc_page_vram | 2 | asm/01 line 3280, 3302 (bl); plate prose at 3174. 函数体: 调用 select_charset_then_load_name 或 resolve_card_gfx_pointer_by_type 获取卡名字符串, 计算字符宽度, setup_line_buf_pos_and_font + render_glyph_jp_dual_layer/single_layer, 最终 commit_line_buffer_to_sprite_vram(0x06007100, 0); 描述页卡名文字渲染函数. 当前名 "step_03_unknown" 与函数体行为矛盾. (high confidence) |

### PLATE (R5; CJK -> ASCII + 订正错误描述)

共 4 个函数需更新 plate (CJK 或信息有误):

1. **card_image_decode_wrapper** (0x0801d998)
   - 当前: `@ p1: 读卡片属性, 调 decode_card_image_6bpp (r1=0x10 palette offset)` [CJK]
   - 新建 ASCII plate:
   ```
   @ Loads card image tiles and frame graphics for the card info page.
   @ r0=card_id (u16), r1=pal_offset (stored sp+4), r2=atk_stat (stored sp+8).
   @ Reads card_stats_table (stride=11 hwords): field[7]=card_subtype(r4), field[6]=unk,
   @   field[9]=level(r7).
   @ Calls load_pack_tile_and_map_to_vram x2 (bg_vram=0xc000/0x6000000, param=0x020e).
   @ Calls decode_card_image_6bpp(vram=0x06000000<<0x13, pal=0x10, card_id, mode=2).
   @ Branches on r4 (card_subtype): r4<=20 -> monster frame; r4==22 -> spell frame;
   @   r4==23 -> spell-alt frame; else skip frame.
   @ Each frame path: resolve_card_type_icon_ptr(card_id), copy palette+tiles to PALRAM/VRAM,
   @   draw_card_name_label_to_vram, copy ATK/DEF stat glyphs.
   @ Calls draw_atk_def_label_to_vram(pal_offset, atk_stat).
   @ Returns void (Pattern B).
   ```

2. **card_info_page_step_03_unknown** -> **render_card_name_to_desc_page_vram** (0x0801dbdc)
   - 当前: `@ p1/p2: 页面动画/过渡 (非 tile 写入), 待细化` [CJK, misleading]
   - 新建 ASCII plate:
   ```
   @ Renders card name text to the description page glyph line buffer.
   @ Reads gCardInfoPageState+0x0 bit0 to select charset:
   @   bit0==1 -> resolve_card_gfx_pointer_by_type (card_id bits[17:15] field[0xf]);
   @   bit0==0 -> select_charset_then_load_name (card_id, lang bits[2:0] of gSettings).
   @ Calculates total pixel width via char_width_wide_10_or_12 or char_width_narrow_5.
   @ Sets gFontJpCtx[+0x8] mode_flags and gFontJpCtx[+0x4] fn_ptr from font_jp_base_table.
   @ Renders each glyph via render_glyph_jp_dual_layer (wide) or render_glyph_jp_single_layer.
   @ Flushes line buffer: zero_fill_by_halfword(0x06007100, 0x80 hwords),
   @   commit_line_buffer_to_sprite_vram(0x06007100, 0).
   @ If sp[0]!=0 (scrolled page): writes tile-index sequences to BG VRAM 0x06000800
   @   and 0x06000c80 using gPrng+0x1e2 as stride, clears gCardInfoPageState[+0x18/+0x1c].
   @ indeg=2: card_info_page_entry (0x0801e456) + update_card_info_page_state (0x0801e42e).
   @ Returns void (Pattern B).
   ```

3. **tick_scroll_frame_and_update_pos** (0x0801dfa0)
   - 当前: `@ 被 FUN_0801e714... 写 VRAM 0x03000240...` [CJK + error: 0x03000240 is wrong]
   - 新建 ASCII plate:
   ```
   @ Updates card description page scroll position each frame (called by card info scene).
   @ Reads gCardInfoPageState[+0x14] (frame_counter, r1). If r1 > 0xe8:
   @   Increments gCardInfoPageState[+0x1c] (sub_counter) modulo (r1-0xe8)*2+0xd2.
   @   If sub_counter in [0x5a..(r1-0xe8)*2+0x5a]: computes scroll_y = (sub_counter-0x5a)/2.
   @   Writes scroll_y to gCardInfoPageState[+0x18] (scroll_pixel_y_offset).
   @   Writes scroll_y to gPrng+0x1e2 (IWRAM BG3VOFS shadow, hw scroll register).
   @ If r1 <= 0xe8: clears [+0x18] and [+0x1c] (stop scroll).
   @ indeg=1; caller: card info scene tick (FUN_0801e714).
   @ Returns void (Pattern B, pop {r4}; pop {r0}; bx r0).
   ```
   注: 原 plate 误写 "0x03000240"; 正确为 gPrng+0x1e2 = 0x03000040+0x1e2 = 0x03000222。
   evidence: asm/01 line 2705 `movs r2,#0xf1; lsls r2,#0x1 = 0x1e2`; line 2707 `adds r0,r0,r2` (gPrng+0x1e2). (high)

4. **render_card_description_text** (0x0801e000)
   - 当前: `@ p2: 字段/描述绘制入口, 字面量池含 .word 0x06010040` [CJK]
   - 新建 ASCII plate:
   ```
   @ Renders card description text to OBJ VRAM (card info page, description sub-page).
   @ Reads gSettings (EWRAM_BASE+GSETTINGS_OFFSET) bits[2:0] (lang) to select charset.
   @ Sets gFontJpCtx[+0x8] mode_flags and fn_ptr from font_jp_base_table.
   @ Calls setup_line_buf_with_font_and_align(x=0x10, y=0x3a, align=1, font=1).
   @ Sets gFontJpCtx[+0x15] active flag bit5 (0x40).
   @ Calls text_render_wrapper(mode, 2, 7, r3) up to 2 times (normal + overflow path).
   @ Writes scroll fields: gCardInfoPageState[+0x24] = line_count+2,
   @   gCardInfoPageState[+0x20] = 0 (reset scroll).
   @ Calls commit_line_buffer_to_sprite_vram(0x06010040, 0).
   @ Returns void.
   ```

5. **card_info_page_finalize** (0x0801e100) - plate 需更新 (CJK, 且描述较粗糙)
   - 当前: `@ p2: 顶层最后一个 bl, UI 收尾` [CJK]
   - 新建 ASCII plate:
   ```
   @ Loads card frame graphics and card flag icons for the card info page finalize step.
   @ r0=card_id (u16). Reads card_stats_table row (stride=11 hwords):
   @   field[7]=subtype(r4), field[6]=subtype_b(r5), field[9]=level(r6),
   @   field[8]=card_type_index(r0 at entry).
   @ Reads gCardInfoPageState[+0x0] to mask bits[7:2] (clears type/flag fields).
   @ If subtype in [22..23] (Spell/Spell-alt): loads icon palette/tiles to
   @   CARD_FRAME_OBJ_PAL_LEVEL(0x05000380) and CARD_SPELL_OBJ_TILE_BASE(0x06017500).
   @ Otherwise: loads alternate icon palette/tiles.
   @ Loop r5=0..0x1f: reads card_attr_order_table[r5] (card type flag ID),
   @   calls test_card_flag_bit(card_id, flag_id). On match:
   @   loads 0x100 bytes from card_status_sprite_sheet[r5*0x100] to
   @   card_type_alt_display_table offset and CARD_ICON_OBJ_TILE_BASE(0x06017580).
   @   Updates gCardInfoPageState flag nibble bits[5:2].
   @ Returns void (Pattern B).
   ```

6. **blit_glyph_2x2_to_bg_vram** (0x0801e294) - plate 已是 ASCII, 无需更新
   - 现有 plate 引用了 constants (OBJ_CHAR_BASE, BG_SCREEN_BASE, PALRAM_BASE 等) 全部 ASCII 且正确。
   - 仅需将槽内 DAT_ 改为符号名。

7. **tick_blend_fadeout_and_set_dispcnt** (0x0801e328) - plate 已 ASCII
   - 现有 plate 正确且无 CJK。仅需 EQ slot (DAT_0801e368 -> DISPCNT_BG_OBJ_CLEAR_MASK)。

8. **tick_blend_fadein_and_poll_done** (0x0801e344) - plate 已 ASCII
   - 现有 plate 正确且无 CJK。

## carve 计划 (R7) -- rom.s label 添加

### Carve A: card_type_alt_display_table @ 0x09e58ac4

- 位置: rom.s line 1608 incbin 起点 `(0x1E58AC4, 0x248)`
- 操作: 在 line 1608 之前 (紧跟 sjis_char_fold_table incbin) 添加 label
- 分裂等式: incbin(0x1E58AC4, 0x248) 保持不变，仅在 incbin 前加 label 行
- 内容: 推测为卡片类型-显示索引映射表 (u16 pair array), 用于 card_info_page_finalize 中显示元素查找
- 消费者: DAT_0801e288 (asm/01 line 3046), addr calc: `card_type_alt_display_table + codepoint*2`
- ROM 验证: raw=1, 地址 0x1E58AC4 = sjis_char_fold_table(0x1E589C4) + 0x100; asm line 1608 起点对齐 (high)
- GAS label 行: `card_type_alt_display_table:  @ 0x09e58ac4`

### Carve B: card_status_sprite_sheet @ 0x09e2ddb4

- 位置: rom.s line 749 before `.incbin "graphics/bin/ui-misc/switch_sheets/case_9_0x01E2DDB4.bin"`
- 操作: 在 line 749 前插入 label 行
- 内容: switch_sheets case_9, 33 items x 0x100 bytes each = 0x2100 bytes (OBJ sprite tiles)
  用于 card_info_page_finalize: copy_bytes_by_halfword(dst, card_status_sprite_sheet+r5*0x100, 0x100)
- 消费者: DAT_0801e290 (asm/01 line 3051), stride 0x100 * r5 (r5=0..0x1f, conditional)
- ROM 验证: raw=2, file 0x1E2DDB4 = case_9 .bin start; size 0x2100 verified (high)
- GAS label 行: `card_status_sprite_sheet:  @ 0x09e2ddb4 (33 card status OBJ sprite items, 0x100B each)`

### Carve C: card_attr_order_table @ 0x09e4f204

- 位置: rom.s line 1458 incbin(0x1E4E979, 0xB3F), 需在 offset +0x88b 处分裂
- 操作: 分裂为两段:
  ```
  (incbin 0x1E4E979, 0x88b)   @ before table (NitroSDK AOB data)
  card_attr_order_table:      @ 0x09e4f204
  (incbin 0x1E4F204, 0xB3F-0x88b-0x?)  @ remainder
  ```
  需确认表长: 32 entries * 4B = 0x80 bytes. 分裂后:
  ```
  .incbin "roms/2343.gba", 0x1E4E979, 0x88B  @ pre-table AOB data
  card_attr_order_table:  @ 0x09e4f204 (32 u32 card attr flag IDs, indexed by display slot)
  .incbin "roms/2343.gba", 0x1E4F204, 0x2B4  @ remainder (0xB3F - 0x88B = 0x2B4)
  ```
- 内容: u32 array[32] of card attribute/type flag IDs (values: 0x15,0x16,0x17,0x18,0x1a,0x12,0x19,0x03...)
  用于 card_info_page_finalize: `ldr r6, [card_attr_order_table + r5*4]` 再 `test_card_flag_bit`
- 消费者: DAT_0801e284 (asm/01 line 3045), also DAT_0810a66c in 23_sound_cardlist_libc.s line 6194
- ROM 验证: raw=2, 0x1E4F204 within incbin(0x1E4E979, 0xB3F), offset 0x88b confirmed (high)
- 覆盖等式: 0x88B + 0x80 (table) + 0x2B4 = 0xB3F (原 incbin size) -- 待 fixer 精确计算表后 size

## disasm 计划 (R4) -- 无

段内无误标为数据的代码块。所有 .hword 0x46xx 均为正常 THUMB `mov rH,rL` 指令 (高寄存器 transfer)。

## 新增 constants / 全局

### card_info.inc 新增 (已有文件, 追加):

```
@ --- Seg-3 additions (card_image_decode_wrapper + card_info_page_step_03_unknown + card_info_page_finalize) ---

@ Card image tile pack parameters (card_image_decode_wrapper)
.equ CARD_TILE_PACK_GLYPH_OFF_A, 0x0985004c  @ card_glyph_table_3+0xa80 (tile src A, normal card map)
.equ CARD_TILE_PACK_GLYPH_OFF_B, 0x09850934  @ card_glyph_table_3+0x1368 (tile src B)
.equ CARD_TILE_PACK_MAP_PARAM,   0x0000020e  @ load_pack_tile_and_map_to_vram map param (31 ROM refs)
.equ CARD_FRAME_TILE_SRC_MONSTER,0x0984a3fc  @ seg-C blob: monster card frame tile pack source
.equ CARD_FRAME_TILE_SRC_SPELL,  0x0984b994  @ seg-C blob: spell card frame tile pack source (type23)
.equ CARD_FRAME_PAL_SRC_MONSTER_A,0x0984dd6c @ seg-C blob: monster frame OBJ palette A (32B)
.equ CARD_FRAME_TILE_SRC_MONSTER_A,0x0984d8ec@ seg-C blob: monster frame OBJ tile data A (256B)
.equ CARD_FRAME_PAL_SRC_SPELL_A, 0x0984de6c  @ seg-C blob: spell frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_SPELL_A, 0x0984dcec @ seg-C blob: spell frame OBJ tile data A
.equ CARD_FRAME_PAL_SRC_STAR_A,  0x0984f52c  @ seg-C blob: star/level frame OBJ palette A (near card_digit_glyph_data)
.equ CARD_FRAME_TILE_SRC_STAR,   0x0984dc6c  @ seg-C blob: star/level OBJ tile data
.equ CARD_FRAME_TILE_SRC_STAR_B, 0x0984f46c  @ seg-C blob: star/level OBJ tile data B
.equ CARD_FRAME_PAL_SRC_MONSTER_B,0x0984de4c @ seg-C blob: monster frame OBJ palette B
.equ CARD_FRAME_PAL_SRC_ICON_A,  0x0984ee2c  @ seg-C blob: icon frame OBJ palette A (type 0x17)
.equ CARD_FRAME_PAL_SRC_ICON_B,  0x0984f3ac  @ seg-C blob: icon frame OBJ palette B (type 0x16)
.equ CARD_FRAME_TILE_SRC_ICON,   0x0984f0ac  @ seg-C blob: icon frame OBJ tile data (type 0x16)
.equ CARD_FRAME_TILE_SRC_SPELL_B, 0x0984e42c @ seg-C blob: spell frame OBJ tile data B (type 0x17)
.equ CARD_OVERLAY_TILE_SRC,      0x09ccd2d0  @ name_o region+0x40: card overlay nibble-sequence tile (5 refs)

@ Card frame PALRAM/VRAM destinations (card_image_decode_wrapper + card_info_page_finalize)
.equ CARD_FRAME_BG_PAL_BASE,    0x050000a0  @ BG PALRAM row 5 (card frame BG palette base)
.equ CARD_FRAME_OBJ_PAL_MONSTER,0x050003a0  @ OBJ PALRAM slot 13 (monster frame palette, PAL+0x1a0)
.equ CARD_FRAME_OBJ_PAL_SPELL,  0x050003c0  @ OBJ PALRAM slot 14 (spell/star frame palette, PAL+0x1c0)
.equ CARD_FRAME_OBJ_PAL_LEVEL,  0x05000380  @ OBJ PALRAM slot 12 (level/icon frame palette, PAL+0x180)
.equ CARD_FRAME_OBJ_TILE_BASE,  0x06017440  @ OBJ VRAM card frame tile base (OBJ+0x7440)
.equ CARD_LEVEL_OBJ_TILE_BASE,  0x060174c0  @ OBJ VRAM card level star tile base (OBJ+0x74c0)
.equ CARD_SPELL_OBJ_TILE_BASE,  0x06017500  @ OBJ VRAM spell card icon tile base (OBJ+0x7500)
.equ CARD_ICON_OBJ_TILE_BASE,   0x06017580  @ OBJ VRAM card icon/status tile base (OBJ+0x7580)
.equ CARD_FRAME_OBJ_TILE_SLOT1, 0x06010020  @ OBJ_TILE_VRAM_BASE+0x20 (tile slot 1 for card art overlay)
.equ CARD_DESC_OBJ_TILE_BASE,   0x06010040  @ OBJ_TILE_VRAM_BASE+0x40 (tile slot 2 for card desc text)

@ Card description page text VRAM (card_info_page_step_03_unknown + render_card_description_text)
.equ CARD_DESC_LINE_BUF_VRAM,   0x06007100  @ BG VRAM card description text line buffer
.equ CARD_DESC_BG_VRAM_A,       0x06000800  @ BG VRAM desc page tile region A (tile-seq write target A)
.equ CARD_DESC_BG_VRAM_B,       0x06000c80  @ BG VRAM desc page tile region B (tile-seq write target B)
.equ CARD_DESC_RENDER_PARAM,    0x00008008  @ render_glyph_jp layer param for card description
```

### gba_mem.inc 新增:

```
.equ BG_SCREEN_TILE_OFF_1,  0x06000002  @ BG screen map entry 1 (tile row 0 col 1 = map base+2)
.equ BG_SCREEN_ROW1_OFF,    0x06000040  @ BG screen map row 1 base (32 tiles * 2B = 0x40 per row)
.equ BG_SCREEN_ROW1_TILE1,  0x06000042  @ BG screen map row 1 col 1 (0x06000040+2)
```

### gba_io.inc 新增:

```
.equ DISPCNT_BG_OBJ_CLEAR_MASK, 0x0000e0ff  @ DISPCNT AND mask: clear bits[12:8] (BG0-BG3+OBJ enable)
```

## §5.1 登记 (Rule 3) -- 0 引用块

段内无 ROM_INCBIN/`.byte` 块。无新增 §5.1 项。

## 消费者证据 (R6) -- 关键槽语义

| 槽 | 语义 | 证据 file:line | 置信度 |
|----|------|---------------|--------|
| DAT_0801df4c=0x06007100 | BG VRAM card desc line buffer | asm/01 line 2559-2563: `ldr r4, DAT_0801df4c; zero_fill_by_halfword(r4); commit_line_buffer_to_sprite_vram(r4,0)` | high |
| DAT_0801ddf0/df48=0x00008008 | render_glyph_jp layer param | asm/01 line 2424-2425: `ldr r3, DAT_0801ddf0; bl render_glyph_jp_dual_layer(char,x,layer,r3)` | high |
| DAT_0801e368=0x0000e0ff | DISPCNT clear mask | asm/01 line 3163-3165: `ldr r0, DAT_0801e368; ands r0,r1; strh r0,[DISPCNT,0]` | high |
| DAT_0801e284=0x09e4f204 | card attr ordering table | asm/01 line 2963-2967: loop `ldr r6,[card_attr_order_table+r5*4]; bl test_card_flag_bit` | high |
| DAT_0801e290=0x09e2ddb4 | card status sprite sheet | asm/01 line 3001-3007: `lsls r1,r5,#8; adds r1,r1,case9_base; copy_bytes_by_halfword(dst, src, 0x100)` | high |
| DAT_0801e288=0x09e58ac4 | card type display table | asm/01 line 2974-2976: `ldr r0,[card_type_alt_display_table]; ldrh r1,[r0,0]` with cmp r1,r6 (card_id match) | med (1 ref only; exact table structure uncertain) |
| DAT_0801da90=0x0985004c | glyph tile pack src A | asm/01 line 1931-1934: `ldr r3, DAT_0801da90; load_pack_tile_and_map_to_vram(bg_vram,0x80,0,r3)` | high |
| tick_scroll_frame plate fix | gPrng+0x1e2 not 0x03000240 | asm/01 line 2705: `movs r2,#0xf1; lsls #1 = 0x1e2`; line 2707: `adds r0,r0,r2` (r0=gPrng=0x03000040) -> 0x03000222 | high |

## 求助

- `DAT_0801e288` (0x09e58ac4) の具体的な table 構造が不明 (med confidence): 1 raw ref のみ, 関数 card_info_page_finalize で `ldrh r1,[r0,0]; cmp r1,r6 (card_id)` として使用 — 可能は card ID lookup table or mapping table. fixer は ASCII plate にてその旨注記されたい。
- `CARD_OVERLAY_TILE_SRC` (0x09ccd2d0=name_o_palette_data+0x40): copy_bytes_by_halfword の src として使用されるが、具体的な tile 内容は 4bpp pixel data と判断される。別ファイル (15/16/17) での使用も write_nibble_sequence_to_bg_tiles の r2 引数として確認済 (asm/15 line 18183) — card name/number tile overlay source. (high)
