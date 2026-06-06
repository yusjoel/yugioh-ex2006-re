# Refine Proposal: Seg-6  [0x0801794c..0x08018774)

## 段测绘

### 函数入口 (28 fn)

| 地址 | 现名 | asm 行 | 备注 |
|---|---|---|---|
| 0x0801794c | load_game_str_1006_to_state | 9197 | Seg-5d 边界首函数 |
| 0x080179a8 | encode_char_to_line_buf | 9249 | |
| 0x08017a24 | encode_str_table_entry_to_line_buf | 9315 | |
| 0x08017b44 | render_name_input_jp_labels_to_obj | 9475 | |
| 0x08017c7c | dispatch_banlist_text_by_key | 9627 | |
| 0x08017cc4 | write_bg0_vofs_with_bias | 9673 | leaf bx lr |
| 0x08017cd0 | render_jp_string_row | 9687 | |
| 0x08017d64 | init_banlist_name_input_page_layout | 9767 | |
| 0x08017e48 | find_name_char_at_idx | 9878 | |
| 0x08017e9c | render_jp_string_to_bg_row | 9940 | |
| 0x08017f04 | render_name_input_scroll_row | 9996 | |
| 0x08017f8c | get_name_scroll_step | 10070 | leaf bx lr |
| 0x08017fa4 | set_name_scroll_step | 10090 | |
| 0x08017fe4 | sync_scrollbar_to_bg_vofs | 10133 | |
| 0x0801805c | check_name_char_limit_reached | 10201 | leaf bx lr |
| 0x08018098 | get_name_input_cursor_tile | 10243 | push lr tail |
| 0x080180ac | name_input_page_load_assets | 10256 | |
| 0x08018248 | write_bg3_vofs_with_bias | 10455 | leaf bx lr |
| 0x08018254 | write_bg1_vofs_with_bias | 10469 | leaf bx lr |
| 0x08018260 | render_obj_slot_cell_anim | 10483 | |
| 0x080182ec | build_sprite_oam_row | 10559 | |
| 0x080183d0 | render_jp_text_to_vram_obj | 10682 | |
| 0x08018400 | zero_obj_vram_tiles | 10707 | |
| 0x08018434 | tick_name_input_scrollbar_and_anims | 10742 | |
| 0x0801848c | advance_name_input_cursor_slot | 10791 | |
| 0x080184f8 | retreat_name_input_cursor_slot | 10854 | |
| 0x08018558 | render_settings_cursor_cell_anims | 10917 | |
| 0x080186f0 | read_banlist_char_at_scroll_pos | 11128 | |
| 0x08018774 | refresh_selected_char_obj_tile | 11198 | Seg-7 起点 (首指令在段内) |

注: dispatch_name_input_key_by_state (0x08018884), append_banlist_input_char (0x080187e0), delete_banlist_name_last_char (0x08018838), tick_name_input_frame (0x08018938) 均在 Seg-7 (>= 0x08018774)。Seg-6 共 **28 fn** (含 5 个 leaf)。

### 残留自动名槽 (DAT_)

| 槽地址 | 函数 | 值 | 语义 |
|---|---|---|---|
| DAT_08017a20 | encode_char_to_line_buf | 0x09e3b2b4 | line-break 3 字节序列基址 |
| DAT_08017a54 | encode_str_table_entry_to_line_buf | 0x02029250 | gState base |
| DAT_08017a58 | encode_str_table_entry_to_line_buf | 0x00000315 | gState+0x315 scroll col 字段偏移 |
| DAT_08017b14 | encode_str_table_entry_to_line_buf | 0x09e587f0 | name_char_group_ptr_table |
| DAT_08017b18 | encode_str_table_entry_to_line_buf | 0x09e3b251 | name_char_range_table |
| DAT_08017b1c | encode_str_table_entry_to_line_buf | 0x0000e3a9 | SJIS char sentinel/end 值 |
| DAT_08017b20 | encode_str_table_entry_to_line_buf | 0x00000117=279 | assert line 0x117 |
| DAT_08017b28 | encode_str_table_entry_to_line_buf | 0x00000189=393 | assert line 0x189 |
| DAT_08017b30 | encode_str_table_entry_to_line_buf | 0x09e3b338 | suppress_display_output fmt 串 |
| DAT_08017c54 | render_name_input_jp_labels_to_obj | 0x02029250 | gState |
| DAT_08017c58 | render_name_input_jp_labels_to_obj | 0x00001008 | STR_ID_A |
| DAT_08017c60 | render_name_input_jp_labels_to_obj | 0x02000000 | EWRAM_BASE |
| DAT_08017c64 | render_name_input_jp_labels_to_obj | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08017c6c | render_name_input_jp_labels_to_obj | 0x00000321 | gState+0x321 width store A |
| DAT_08017c70 | render_name_input_jp_labels_to_obj | 0x00001007 | STR_ID_B |
| DAT_08017c74 | render_name_input_jp_labels_to_obj | 0x0000100c | STR_ID_C |
| DAT_08017c78 | render_name_input_jp_labels_to_obj | 0x00000322 | gState+0x322 width store C |
| DAT_08017c90 | dispatch_banlist_text_by_key | 0x02029250 | gState |
| DAT_08017ca8 | dispatch_banlist_text_by_key | 0x09e3afdc | banlist_str_src (SJIS JP text) |
| DAT_08017e34 | init_banlist_name_input_page_layout | 0x02029250 | gState |
| DAT_08017e38 | init_banlist_name_input_page_layout | 0x02000000 | EWRAM_BASE |
| DAT_08017e3c | init_banlist_name_input_page_layout | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08017e40 | init_banlist_name_input_page_layout | 0x01000200 | bios_cpu_fast_set BG0 screen clear ctrl |
| DAT_08017e44 | init_banlist_name_input_page_layout | 0x01001800 | bios_cpu_fast_set char VRAM clear ctrl |
| DAT_08017e7c | find_name_char_at_idx | 0x02029250 | gState |
| DAT_08017e80 | find_name_char_at_idx | 0x02000000 | EWRAM_BASE |
| DAT_08017e84 | find_name_char_at_idx | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08017ef8 | render_jp_string_to_bg_row | 0x05000160 | bios_cpu_set clear row ctrl |
| DAT_08017efc | render_jp_string_to_bg_row | 0x02000000 | EWRAM_BASE |
| DAT_08017f00 | render_jp_string_to_bg_row | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08017f88 | render_name_input_scroll_row | 0x02029250 | gState |
| DAT_08017f9c | get_name_scroll_step | 0x02029250 | gState |
| DAT_08017fa0 | get_name_scroll_step | 0x0000031a | gState+0x31a 偏移 |
| DAT_08017fd4 | set_name_scroll_step | 0x02029250 | gState |
| DAT_08017fe0 | set_name_scroll_step | 0x0000031a | gState+0x31a 偏移 |
| DAT_08018014 | sync_scrollbar_to_bg_vofs | 0x02029250 | gState |
| DAT_08018018 | sync_scrollbar_to_bg_vofs | 0x0000031a | gState+0x31a 偏移 |
| DAT_08018058 | sync_scrollbar_to_bg_vofs | 0x0000031a | gState+0x31a 偏移 (2nd slot) |
| DAT_0801807c | check_name_char_limit_reached | 0x02029250 | gState |
| DAT_08018080 | check_name_char_limit_reached | 0x0000031f | gState+0x31f char_count 字段 |
| DAT_08018084 | check_name_char_limit_reached | 0x02000000 | EWRAM_BASE |
| DAT_08018088 | check_name_char_limit_reached | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08018190 | name_input_page_load_assets | 0x02029250 | gState |
| DAT_08018194 | name_input_page_load_assets | 0x09e3b3d0 | name_o_resource_desc |
| DAT_08018198 | name_input_page_load_assets | 0x09e3b3e0 | name_b_01_path |
| DAT_0801819c | name_input_page_load_assets | 0xffffc07f | GFX_ATTR_CLEAR_BITS_13_7 |
| DAT_080181a0 | name_input_page_load_assets | 0x09e3b3fc | name_b_02_path |
| DAT_080181a4 | name_input_page_load_assets | 0x09e3b418 | name_b_04_path |
| DAT_08018228 | name_input_page_load_assets | 0x09ccd290 | name_o_palette_data (15 refs) |
| DAT_0801822c | name_input_page_load_assets | 0x05000020 | BG PALRAM palette dst (+0x20) |
| DAT_08018234 | name_input_page_load_assets | 0x05000220 | OBJ PALRAM palette dst (+0x20) |
| DAT_08018238 | name_input_page_load_assets | 0x02000000 | EWRAM_BASE |
| DAT_0801823c | name_input_page_load_assets | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08018240 | name_input_page_load_assets | 0x05000202 | bios_cpu_set ctrl (copy 514 words) |
| DAT_08018244 | name_input_page_load_assets | 0x000002be | gState+0x2be offset |
| DAT_080182ac | render_obj_slot_cell_anim | 0x02029250 | gState |
| DAT_08018360 | build_sprite_oam_row | 0x000003ff | OAM_ATTR2_CHARNAME_MASK |
| DAT_08018364 | build_sprite_oam_row | 0xfffffc00 | OAM_ATTR2_CHARNAME_CLEAR |
| DAT_08018368 | build_sprite_oam_row | 0x40004000 | OAM hflip/vflip packed pattern |
| DAT_080183c8 | build_sprite_oam_row | 0x000001ff | OAM X_MASK (attr1 bits[8:0]) |
| DAT_080183cc | build_sprite_oam_row | 0xfffffe00 | OAM X_CLEAR |
| DAT_0801842c | zero_obj_vram_tiles | 0x06010000 | OBJ_TILE_VRAM_BASE |
| DAT_08018430 | zero_obj_vram_tiles | 0x001fffff | cpuset_wordcount_mask |
| DAT_08018488 | tick_name_input_scrollbar_and_anims | 0x02029250 | gState |
| DAT_080184b8 | advance_name_input_cursor_slot | 0x02029250 | gState |
| DAT_080184bc | advance_name_input_cursor_slot | 0x02000000 | EWRAM_BASE |
| DAT_080184c0 | advance_name_input_cursor_slot | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_080184f4 | advance_name_input_cursor_slot | 0x0000031b | gState+0x31b scroll_dir 字段 |
| DAT_08018548 | retreat_name_input_cursor_slot | 0x02029250 | gState |
| DAT_0801854c | retreat_name_input_cursor_slot | 0x02000000 | EWRAM_BASE |
| DAT_08018550 | retreat_name_input_cursor_slot | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08018554 | retreat_name_input_cursor_slot | 0x0000031b | gState+0x31b scroll_dir 字段 |
| DAT_08018658 | render_settings_cursor_cell_anims | 0x02029250 | gState |
| DAT_0801865c | render_settings_cursor_cell_anims | 0x02000000 | EWRAM_BASE |
| DAT_08018660 | render_settings_cursor_cell_anims | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_08018664 | render_settings_cursor_cell_anims | 0x0000031b | gState+0x31b 偏移 |
| DAT_08018668 | render_settings_cursor_cell_anims | 0x09e3b46f | cursor_anim_data_a (12B) |
| DAT_0801866c | render_settings_cursor_cell_anims | 0x09e3b47c | cursor_anim_data_b (28B) |
| DAT_0801874c | read_banlist_char_at_scroll_pos | 0x02029250 | gState |
| DAT_08018750 | read_banlist_char_at_scroll_pos | 0x00000315 | gState+0x315 偏移 |
| DAT_08018754 | read_banlist_char_at_scroll_pos | 0x02000000 | EWRAM_BASE |
| DAT_08018758 | read_banlist_char_at_scroll_pos | 0x00006c2c | GSETTINGS_OFFSET |
| DAT_0801875c | read_banlist_char_at_scroll_pos | 0x09e3b2b4 | space_placeholder (EN mode) |
| DAT_080187d4 | refresh_selected_char_obj_tile | 0x02029250 | gState |
| DAT_080187d8 | refresh_selected_char_obj_tile | 0x09e587ec | name_char_tile_slot_table |
| DAT_080187dc | refresh_selected_char_obj_tile | 0x000002c2 | gState+0x2c2 name buf base |

注: PTR_* 已符号化槽 (PTR_gSettings_08017d1c = gSettings, PTR_BG0CNT_*, PTR_BG3VOFS_*, PTR_BG1VOFS_*, PTR_game_str_pointer_table_*, PTR_game_str_ja_* 等) 及 assert 已 carve 槽 (name_main_c_filename / assert_cnt_name_mojitbl_width_1_name / assert_dir_1_dir_1 / assert_anmid_ig2d_getanmsequencescoun) 均已干净, 不重复列。

### ROM_INCBIN / .byte 块

| 地址 | asm 行 | 大小 | 描述 |
|---|---|---|---|
| ROM_INCBIN 0x186ce | 11114 | 34 B (0x22) | refresh_selected_char_obj_tile 之后, Seg-7 起点之前 |

---

## 数据块分类 (Rule 2/3)

### ROM_INCBIN 0x186ce, 0x22 (34 B)

**ref-scan** (python 逐偏移 4B 扫描, raw + THUMB|1):

| 子地址 | raw | THUMB+1 |
|---|---|---|
| 0x080186ce (base) | 0 | 0 |
| 0x080186d0 | 0 | 0 |
| 0x080186d4 | 0 | 0 |
| ... | 0 | 0 |

全 16 个 4B 对齐子地址均 raw=0, thumb=0。

**反汇编预判**: ROM bytes `00 00 05 48 06 49 40 18 07 21 00 78 01 40 01 20 00 29 00 d1 02 20 70 47 00 00 00 00 00 02 2c 6c 00 00`:
- `0x186ce +0x00`: `0x0000` = 2B 对齐填充
- `0x186d0 +0x02`: `4805 4906 1840 2107 7800 4001 2001 2900 00d1 2002 7047` = THUMB 函数 (`ldr r0,[pc,#0x14]; ldr r1,[pc,#0x18]; adds r0,r0,r1; movs r1,#7; ldrb r0,[r0,#0]; ands r1,r0; movs r0,#1; cmp r1,#0; bne +2; movs r0,#2; bx lr`)
  = `u32 get_language_stride(void)` (return 1 if JP, 2 if EN, reads gSettings bits[2:0])
- `0x186e2 +0x14`: `0000 0000` padding
- `0x186e8 +0x1a`: `.word 0x02000000` (EWRAM_BASE literal pool)
- `0x186ec +0x1e`: `.word 0x00006c2c` (GSETTINGS_OFFSET literal pool)

**判定: §5.1 登记 (Rule 3)**

理由: **全 ROM 0 引用** (ref-scan raw=0 thumb=0 for all sub-addresses; the function entry 0x080186d0 THUMB addr = 0x080186d1 also = 0 refs). 该函数是 `render_jp_string_row` 等函数体内 language-stride 计算逻辑的 dead-code 编译变体 (segment 内多个函数直接内联了同等逻辑, 无需调用此 leaf)。留待引用到时按 R4 disasm + createFunction 处理。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

以下值无 ROM GAS label 可用, 需新建 data-equate 或复用现有 inc 常量:

#### 复用现有 inc

| 槽 | 值 | 常量名 | inc 文件 | 使用槽 |
|---|---|---|---|---|
| DAT_08018360 | 0x000003ff | OAM_ATTR2_CHARNAME_MASK | oam_attr.inc | build_sprite_oam_row |
| DAT_08018364 | 0xfffffc00 | OAM_ATTR2_CHARNAME_CLEAR | oam_attr.inc | build_sprite_oam_row |
| DAT_0801819c | 0xffffc07f | GFX_ATTR_CLEAR_BITS_13_7 | gfx_resource.inc | name_input_page_load_assets |
| DAT_0801842c | 0x06010000 | OBJ_TILE_VRAM_BASE | gba_mem.inc | zero_obj_vram_tiles |

#### 新建 EQ (name_input.inc 追加, 全 ASCII)

| 槽 | 值 | const_name | EOL |
|---|---|---|---|
| DAT_08017e40 | 0x01000200 | NAME_INPUT_BG0_SCREEN_CLEAR_CTRL | bios_cpu_fast_set: fill 0x200 halfwords=512 zeros -> BG0 screen VRAM |
| DAT_08017e44 | 0x01001800 | NAME_INPUT_CHAR_VRAM_CLEAR_CTRL | bios_cpu_fast_set: fill 0x1800 halfwords=6144 zeros -> char VRAM |
| DAT_08017ef8 | 0x05000160 | NAME_INPUT_BG_ROW_CLEAR_CTRL | bios_cpu_set: copy 0x160=352 words=1408 bytes -> clear one BG row |

置信度: high. 消费者证据 (R6):
- DAT_08017e40 (0x01000200): asm/00_system_str_vija.s line 9868 -- `init_banlist_name_input_page_layout` calls `bios_cpu_fast_set(sp+0x14, get_bg0_screen_vram_addr(), ctrl=0x01000200)`. bios_cpu_fast_set ctrl: bit[20:0]=count, bit[26]=fill=0(copy), bit[24]=1(32-bit). count=0x200=512 words -> copies 2048B. BG screen VRAM = 32x32 tiles * 2B = 2048B. Exact match.
- DAT_08017e44 (0x01001800): same function, `bios_cpu_fast_set(sp+0x18, get_bg0_char_vram_addr(), ctrl=0x01001800)`. count=0x1800=6144 words -> 24576B = 6144 tiles * 4B. Char VRAM clear.
- DAT_08017ef8 (0x05000160): `render_jp_string_to_bg_row` line 9985 calls `bios_cpu_set(sp+0x4, r1, ctrl=0x05000160)`. 0x05000160: bit[24]=1(32-bit), count=0x160=352 -> 352 words=1408 bytes = 44 tiles * 32B = one BG row. Plate annotation says `CLEAR_CTRL=0x05000160`.

#### 新建 EQ (新文件 name_input_page.inc 或追加)

| 槽 | 值 | const_name | 理由 |
|---|---|---|---|
| DAT_08018368 | 0x40004000 | OAM_HFLIP_VFLIP_PACKED_PATTERN | build_sprite_oam_row: orr'd into OAM 32-bit entry to set hflip+vflip toggle bits; 0x4000 = bit14 in both halfwords (attr0+attr1 combined word). unique value, not in any existing inc |
| DAT_080183c8 | 0x000001ff | OAM_ATTR1_X_MASK | build_sprite_oam_row: ands r1,r0 masks x-pos to low 9 bits. Distinct from SCROLLBAR_KEEP_BITS_8_0 (semantics differ). |
| DAT_080183cc | 0xfffffe00 | OAM_ATTR1_X_CLEAR | build_sprite_oam_row: clear x-pos bits in attr1. Complement of OAM_ATTR1_X_MASK. |
| DAT_08018430 | 0x001fffff | ZERO_OBJ_TILES_CPUSET_MASK | zero_obj_vram_tiles: `ands r2,r0` masks tile count before bios_cpu_set ctrl. Already used in fill_vram_screen_rect_zero_cpuset_wordcount_mask, but that is a RENAME_SLOT (already named). This slot needs equate. |

置信度: high. 消费者证据 (R6):
- 0x40004000: asm line 10623-10624 `DAT_08018368` in `build_sprite_oam_row`. Code: `ldr r1, DAT_08018368` then `orrs r0,r1` on `[r3+0]` (32-bit OAM entry write). GBA OAM: attr1 bit14=hflip, attr0 bit14 is OAM type. 0x40004000 = 0x4000 in both attr0 halfword and attr1 halfword packs HFlip toggle.
- 0x000001ff: line 10677, `ands r1,r0` -> 9-bit X coordinate mask (OAM attr1 bits[8:0]=x_pos).
- 0xfffffe00: line 10679, complement.
- 0x001fffff: line 10731-10732, `ands r2,r0` before bios_cpu_set ctrl in `zero_obj_vram_tiles`. Masks word count to 21 bits (cpuset spec).

Note on OAM_ATTR1_X_MASK: checking oam_attr.inc -- `OAM_ATTR2_CHARNAME_MASK=0x3ff` is NOT the same value (0x3ff vs 0x1ff). Also `SCROLLBAR_KEEP_BITS_8_0=0x1ff` in gl_scrollbar.inc exists but semantics differ (scrollbar field vs OAM X). New equate in oam_attr.inc with distinct name recommended.

### REF_SLOTS (USER-label DATA ref; RAM/ROM 全局或 carve label)

#### gState 槽 (复用 ewram.inc: gState=0x02029250)

| 槽 | 函数 | 语义 |
|---|---|---|
| DAT_08017a54 | encode_str_table_entry_to_line_buf | gState base |
| DAT_08017c54 | render_name_input_jp_labels_to_obj | gState base |
| DAT_08017c90 | dispatch_banlist_text_by_key | gState base |
| DAT_08017e34 | init_banlist_name_input_page_layout | gState base |
| DAT_08017e7c | find_name_char_at_idx | gState base |
| DAT_08017f88 | render_name_input_scroll_row | gState base |
| DAT_08017f9c | get_name_scroll_step | gState base |
| DAT_08017fd4 | set_name_scroll_step | gState base |
| DAT_08018014 | sync_scrollbar_to_bg_vofs | gState base |
| DAT_0801807c | check_name_char_limit_reached | gState base |
| DAT_08018190 | name_input_page_load_assets | gState base |
| DAT_080182ac | render_obj_slot_cell_anim | gState base |
| DAT_08018488 | tick_name_input_scrollbar_and_anims | gState base |
| DAT_080184b8 | advance_name_input_cursor_slot | gState base |
| DAT_08018548 | retreat_name_input_cursor_slot | gState base |
| DAT_08018658 | render_settings_cursor_cell_anims | gState base |
| DAT_0801874c | read_banlist_char_at_scroll_pos | gState base |
| DAT_080187d4 | refresh_selected_char_obj_tile | gState base |

共 **18 个** gState 槽, 复用 ewram.inc gState 的 Ghidra USER label + DATA ref。

#### EWRAM_BASE 槽 (复用 gba_mem.inc: EWRAM_BASE=0x02000000)

| 槽 | 函数 |
|---|---|
| DAT_08017c60 | render_name_input_jp_labels_to_obj |
| DAT_08017e38 | init_banlist_name_input_page_layout |
| DAT_08017e80 | find_name_char_at_idx |
| DAT_08017efc | render_jp_string_to_bg_row |
| DAT_08018084 | check_name_char_limit_reached |
| DAT_08018238 | name_input_page_load_assets |
| DAT_080184bc | advance_name_input_cursor_slot |
| DAT_0801854c | retreat_name_input_cursor_slot |
| DAT_0801865c | render_settings_cursor_cell_anims |
| DAT_08018754 | read_banlist_char_at_scroll_pos |

共 **10 个** EWRAM_BASE 槽。

#### GSETTINGS_OFFSET 槽 (复用 name_input.inc: GSETTINGS_OFFSET=0x00006c2c)

以下槽值均为 0x00006c2c:

| 槽 | 函数 |
|---|---|
| DAT_08017c64 | render_name_input_jp_labels_to_obj |
| DAT_08017e3c | init_banlist_name_input_page_layout |
| DAT_08017e84 | find_name_char_at_idx |
| DAT_08017f00 | render_jp_string_to_bg_row |
| DAT_08018088 | check_name_char_limit_reached |
| DAT_0801823c | name_input_page_load_assets |
| DAT_080184c0 | advance_name_input_cursor_slot |
| DAT_08018550 | retreat_name_input_cursor_slot |
| DAT_08018660 | render_settings_cursor_cell_anims |
| DAT_08018758 | read_banlist_char_at_scroll_pos |

共 **10 个** GSETTINGS_OFFSET 槽。

#### ROM 数据地址槽 (新 carve label REF)

以下槽指向 ROM 数据地址, 需给目标地址打 USER_DEFINED label + 代码槽加 DATA ref + 槽改名:

| 槽 | 函数 | 目标地址 | gas_label | 理由 |
|---|---|---|---|---|
| DAT_08017b14 | encode_str_table_entry_to_line_buf | 0x09e587f0 | name_char_group_ptr_table | 名片输入 JP 字符组指针表 (10+ 项, 每项指向 SJIS 字符对 head); encode_str_table_entry 按 r6 index 读取. raw=1 ref |
| DAT_08017b18 | encode_str_table_entry_to_line_buf | 0x09e3b251 | name_char_range_table | SJIS 字符范围边界表 (偶数字节对, 用于 char start/end 判断); raw=1 thumb=1 refs |
| DAT_08017ca8 | dispatch_banlist_text_by_key | 0x09e3afdc | banlist_jp_str_src | JP banlist 字符串体 (SJIS, key=2 时 copy 到 gState+0x8d); raw=1 ref |
| DAT_08017b30 | encode_str_table_entry_to_line_buf | 0x09e3b338 | assert_table_last_fmt | suppress_display_output 格式串 "TableLast(%d)\n" (已在 incbin 0x1E3B336+2 内); raw=1 ref |
| DAT_08017a20 | encode_char_to_line_buf | 0x09e3b2b4 | line_break_seq | 3B 换行分隔符序列 (encode_char appends every 11 chars); raw=2 refs |
| DAT_0801875c | read_banlist_char_at_scroll_pos | 0x09e3b2b4 | line_break_seq | 同上 (EN mode space substitute); 复用同 label |
| DAT_08018194 | name_input_page_load_assets | 0x09e3b3d0 | name_o_resource_desc | name_o_01 G2D 资源描述符 (4 ptr: ncer/nanr/ncgr/nclr 路径); raw=1 ref |
| DAT_08018198 | name_input_page_load_assets | 0x09e3b3e0 | name_b_01_path | "name_input/name_b_01.LZ5bg" 路径串; raw=1 ref |
| DAT_080181a0 | name_input_page_load_assets | 0x09e3b3fc | name_b_02_path | "name_input/name_b_02.LZ5bg"; raw=1 ref |
| DAT_080181a4 | name_input_page_load_assets | 0x09e3b418 | name_b_04_path | "name_input/name_b_04.LZ5bg"; raw=1 ref |
| DAT_08018228 | name_input_page_load_assets | 0x09ccd290 | name_o_palette_data | name_o OAM/BG 调色板数据块 (raw=15 refs); bios_cpu_set src |
| DAT_08018668 | render_settings_cursor_cell_anims | 0x09e3b46f | cursor_anim_data_a | 光标动画帧数据 A (12B; raw=1 thumb=1 refs; memcpy 12B) |
| DAT_0801866c | render_settings_cursor_cell_anims | 0x09e3b47c | cursor_anim_data_b | 光标动画帧数据 B (28B; raw=1 ref; ldmia 7 words) |
| DAT_080187d8 | refresh_selected_char_obj_tile | 0x09e587ec | name_char_tile_slot_table | ping-pong 双缓冲 OBJ tile 索引表 ([0]=0x012c=300 [1]=0x014e=334, 读为 ldrh); raw=3 refs |

### RENAME_SLOTS (纯改名 + EOL)

以下槽仅需 setName 改名 (Ghidra 无需新建 label/ref, 仅本地语义标注):

| 槽 | 函数 | 值 | slot_label | EOL (ASCII) |
|---|---|---|---|---|
| DAT_08017a58 | encode_str_table_entry_to_line_buf | 0x00000315 | encode_str_table_entry_to_line_buf_scroll_col_offset | gState+0x315 = scroll column index field (bits[5:2]) |
| DAT_08017b1c | encode_str_table_entry_to_line_buf | 0x0000e3a9 | encode_str_table_entry_to_line_buf_char_sentinel | SJIS char sentinel/end value (upper bound check) |
| DAT_08017b20 | encode_str_table_entry_to_line_buf | 0x00000117 | encode_str_table_entry_to_line_buf_assert_line_117 | assert line 0x117=279 (width check) |
| DAT_08017b28 | encode_str_table_entry_to_line_buf | 0x00000189 | encode_str_table_entry_to_line_buf_assert_line_189 | assert line 0x189=393 (column check) |
| DAT_08017c58 | render_name_input_jp_labels_to_obj | 0x00001008 | render_name_input_jp_labels_to_obj_str_id_a | STR_ID_A=0x1008 (1st game_str id) |
| DAT_08017c6c | render_name_input_jp_labels_to_obj | 0x00000321 | render_name_input_jp_labels_to_obj_width_store_a | gState+0x321 = pixel width store for str A |
| DAT_08017c70 | render_name_input_jp_labels_to_obj | 0x00001007 | render_name_input_jp_labels_to_obj_str_id_b | STR_ID_B=0x1007 |
| DAT_08017c74 | render_name_input_jp_labels_to_obj | 0x0000100c | render_name_input_jp_labels_to_obj_str_id_c | STR_ID_C=0x100c |
| DAT_08017c78 | render_name_input_jp_labels_to_obj | 0x00000322 | render_name_input_jp_labels_to_obj_width_store_c | gState+0x322 = pixel width store for str C |
| DAT_08017fa0 | get_name_scroll_step | 0x0000031a | get_name_scroll_step_scroll_field_offset | gState+0x31a = scroll_step field |
| DAT_08017fe0 | set_name_scroll_step | 0x0000031a | set_name_scroll_step_scroll_field_offset | gState+0x31a = scroll_step field |
| DAT_08018018 | sync_scrollbar_to_bg_vofs | 0x0000031a | sync_scrollbar_to_bg_vofs_scroll_field_offset | gState+0x31a (1st ref) |
| DAT_08018058 | sync_scrollbar_to_bg_vofs | 0x0000031a | sync_scrollbar_to_bg_vofs_scroll_field_offset_b | gState+0x31a (2nd ref; distinct slot addr) |
| DAT_08018080 | check_name_char_limit_reached | 0x0000031f | check_name_char_limit_reached_char_count_offset | gState+0x31f = current char count byte |
| DAT_0801822c | name_input_page_load_assets | 0x05000020 | name_input_page_load_assets_bg_palette_dst | BG PALRAM base+0x20 = palette entry 16 |
| DAT_08018234 | name_input_page_load_assets | 0x05000220 | name_input_page_load_assets_obj_palette_dst | OBJ PALRAM base+0x20 = OBJ palette entry 16 |
| DAT_08018240 | name_input_page_load_assets | 0x05000202 | name_input_page_load_assets_gstate_copy_ctrl | bios_cpu_set: copy 514 words from name_o ptr table -> gState+0x2be |
| DAT_08018244 | name_input_page_load_assets | 0x000002be | name_input_page_load_assets_gstate_ptr_offset | gState+0x2be = name_o animation ptr table base |
| DAT_080184f4 | advance_name_input_cursor_slot | 0x0000031b | advance_name_input_cursor_slot_scroll_dir_offset | gState+0x31b = scroll direction marker field |
| DAT_08018554 | retreat_name_input_cursor_slot | 0x0000031b | retreat_name_input_cursor_slot_scroll_dir_offset | gState+0x31b scroll direction marker |
| DAT_08018664 | render_settings_cursor_cell_anims | 0x0000031b | render_settings_cursor_cell_anims_speed_field_offset | gState+0x31b = speed/position correction byte |
| DAT_08018750 | read_banlist_char_at_scroll_pos | 0x00000315 | read_banlist_char_at_scroll_pos_scroll_col_offset | gState+0x315 scroll col index |
| DAT_080187dc | refresh_selected_char_obj_tile | 0x000002c2 | refresh_selected_char_obj_tile_name_buf_offset | gState+0x2c2 = name input byte buffer base |

### FUNC_RENAME

全段 28 函数经 R6 消费者读检:

- **load_game_str_1006_to_state**: 函数体 load game_str 0x1006, 写 gState+0x8d buffer, 调 pad_str_to_char_multiple. 名与操作完全一致。confidence=high. 无误名。
- **encode_char_to_line_buf**: 单字符 SJIS encode + line_break 插入, 操作 gState(通过 r2/r3 传入). 名与操作一致。
- **encode_str_table_entry_to_line_buf**: 按 gState 字符组表 encode 整行. 名一致。
- **render_name_input_jp_labels_to_obj**: render 3 JP strings (STR_ID 1008/1007/100c) to OBJ VRAM tiles. 名一致。
- **dispatch_banlist_text_by_key**: key 0..3 dispatch. 名一致。
- **write_bg0/3/1_vofs_with_bias**: 写 VOFS 寄存器减 bias. 名一致。
- **render_jp_string_row**: 按语言模式逐字 render. 名一致。
- **init_banlist_name_input_page_layout**: 初始化 banlist/name-input 页 layout. 名一致。
- **find_name_char_at_idx**: 返回第 idx 个字符位置指针. 名一致。
- **render_jp_string_to_bg_row**: render JP string to BG row + clear. 名一致。
- **render_name_input_scroll_row**: scroll row render. 名一致。
- **get/set_name_scroll_step**: 读写 gState+0x31a scroll step. 名一致。
- **sync_scrollbar_to_bg_vofs**: 同步滚动条到 BG VOFS. 名一致。
- **check_name_char_limit_reached**: 判断 char count >= max. 名一致。
- **get_name_input_cursor_tile**: 返回 cursor tile index. 名一致。
- **name_input_page_load_assets**: 加载 name_o + name_b 资产, 调 apply_gfx_resource_list/apply_sprite_gfx_type_zero. 名一致。
- **render_obj_slot_cell_anim**: render OBJ slot cell anim. 名一致。
- **build_sprite_oam_row**: 写一行 sprite OAM 属性到 GL slot table. 名一致。
- **render_jp_text_to_vram_obj**: 调 setup_font_jp_ctx_obj_vram_row + dispatch_text_render_by_mode 写 OBJ VRAM. 名一致。
- **zero_obj_vram_tiles**: CpuSet fill-zero OBJ tile region. 名一致。
- **tick_name_input_scrollbar_and_anims**: update scrollbar thumb + 2 cell anim OAM. 名一致。
- **advance/retreat_name_input_cursor_slot**: 3-bit cursor slot cycle. 名一致。
- **render_settings_cursor_cell_anims**: render 5 cursor cell anim slots. 名一致。
- **read_banlist_char_at_scroll_pos**: 从 scrollbar 位置读 banlist char. 名一致。
- **refresh_selected_char_obj_tile**: 双缓冲切换 + 写 OBJ tile. 名一致。

**FUNC_RENAME: 0 (无误名)**

### PLATE (R5)

以下函数 plate 中含过时槽引用 (DAT_/DWORD_) 需更新为新语义名或已知符号:

1. **encode_str_table_entry_to_line_buf** (0x08017a24):
   - plate 现引 `0x09e3b338` 裸值 -> 改为 `assert_table_last_fmt`
   - plate 现引 `0x09e587f0` 裸值 -> 改为 `name_char_group_ptr_table`
   - plate 现引 `0x09e3b251` 裸值 -> 改为 `name_char_range_table`
   - plate 现引 `0x0000e3a9` 裸值 -> 改为 `encode_str_table_entry_to_line_buf_char_sentinel`

2. **encode_char_to_line_buf** (0x080179a8):
   - plate 现引 `0x09e3b2b4` 裸值 -> 改为 `line_break_seq`

3. **render_name_input_jp_labels_to_obj** (0x08017b44):
   - 已有完整 plate; 若含裸地址 `0x02029250` -> 改为 `gState`

4. **init_banlist_name_input_page_layout** (0x08017d64):
   - plate 含中文 (CJK) -- Ghidra EOL/plate 须为 ASCII. 如需重写 plate, 写全 ASCII 版

5. **refresh_selected_char_obj_tile** (0x08018774):
   - plate 含中文 -- 同上, 写 ASCII 版

6. **read_banlist_char_at_scroll_pos** (0x080186f0):
   - plate 含 `0x09e3b2b4` 裸值 -> 改为 `line_break_seq`

---

## carve 计划 (R7)

以下 ROM 数据地址被代码引用, 需 carve 进 rom.s (加 label + 结构化内容):

### carve A: name_char_tile_slot_table (0x09e587ec, 4B)

- 位置: `asm/rom.s` line 1294 incbin `0x1E587EC, 0x520` -- 该 incbin 起点恰好是 0x09e587ec
- 内容: 2 个 u16 OBJ tile indices `[0]=0x012c (300), [1]=0x014e (334)` (ping-pong double-buffer slots)
- carve: 从 incbin 头部切 4B, 剩余 incbin 缩短 4B

```
name_char_tile_slot_table:               @ 0x09e587ec
    .hword 0x012c                        @ ping-pong buffer 0: tile index 300
    .hword 0x014e                        @ ping-pong buffer 1: tile index 334
.incbin "roms/2343.gba", 0x1E587F0, 0x51C   @ remaining (end: 0x1E58D0C)
```

- 代码侧: DAT_080187d8 -> Ghidra DATA ref to `name_char_tile_slot_table` + setName `refresh_selected_char_obj_tile_char_tile_slot_table`
- 其他消费者: 0x08018f70 (Seg-7), 0x08019490 (Seg-8) -- 同 label, 各自槽改名

### carve B: name_char_group_ptr_table (0x09e587f0, ~40B = 10 ptrs)

- 位置: 紧邻 name_char_tile_slot_table 之后 (0x1E587F0, 在 carve A 缩短后的新 incbin 内)
- 内容: 10 个 .word ptrs 指向 JP 字符组 SJIS 串 (0x09e3b248/23c/230/224/218/20c/200/1f4/1e8/1dc)
- carve: 从 carve A 剩余 incbin 头部再切 40B

```
name_char_group_ptr_table:               @ 0x09e587f0
    .word 0x09e3b248     @ char group 0
    .word 0x09e3b23c     @ char group 1
    .word 0x09e3b230     @ char group 2
    .word 0x09e3b224     @ char group 3
    .word 0x09e3b218     @ char group 4
    .word 0x09e3b20c     @ char group 5
    .word 0x09e3b200     @ char group 6
    .word 0x09e3b1f4     @ char group 7
    .word 0x09e3b1e8     @ char group 8
    .word 0x09e3b1dc     @ char group 9
.incbin "roms/2343.gba", 0x1E58818, 0x4F4   @ remaining
```

- 代码侧: DAT_08017b14 -> DATA ref `name_char_group_ptr_table`

### carve C: name_char_range_table (0x09e3b251, ~20B)

- 位置: 在 incbin `0x1E3AFDC, 0x2DC` (line 934) 内, offset = 0x1E3B251 - 0x1E3AFDC = 0x275
- 内容: SJIS char range boundary bytes (偶数字节对: 0x889f 0x88c8 0x8945 0x8960 ...)
- 注意: 该 incbin 极大 (0x2DC=732B), 且该地址有 THUMB ref (raw=1 thumb=1) -> 确有代码引用
- carve: 从大 incbin 切出小块 (前 0x275B + label + N bytes + 后缀 incbin)
- 但 encode_str_table_entry_to_line_buf 使用方式: `ldr r3, DAT_08017b18` then reads pairs of bytes -> 需确定 table 精确大小
- BLOCKED: 无法静态确定 name_char_range_table 精确大小 (取决于字符组数量, 需读 encode_str_table 完整逻辑确认迭代终止条件). 当前读 SJIS bytes 最多 20B = `88 9f 88 c8 89 45 89 60 89 97 89 ba 8a e9 8b e3 8c 54 8c c1`. 置信度: med. 求助见末节.

### carve D: line_break_seq (0x09e3b2b4, 3B+pad)

- 位置: incbin `0x1E3AFDC, 0x2DC` 内, offset = 0x1E3B2B4 - 0x1E3AFDC = 0x2D8
- 内容: `81 40 00` (3B, SJIS full-width space + NUL pad): encode_char_to_line_buf appends as 3-byte line-break delimiter
- raw=2 refs (encode_char + read_banlist)
- carve: 单独切 3B (+ 1B NUL pad = 4B), 但与 name_char_range_table 在同一大 incbin 内
- 建议: 一次性将 incbin 0x1E3AFDC, 0x2DC 按需切分 (name_char_range_table + line_break_seq + banlist_jp_str_src 都在此范围内)
- BLOCKED: 同 carve C, 等待确认 name_char_range_table 大小后统一处理

### carve E: banlist_jp_str_src (0x09e3afdc, N bytes)

- 位置: incbin `0x1E3AFDC, 0x2DC` 头部 (offset=0)
- 内容: SJIS JP text `82 a0 82 a9 82 b3 82 bd 82 c8...` (JP banlist chars for dispatch_banlist key=2)
- raw=1 ref
- BLOCKED: 同上, 等待统一处理

### carve F: name_o_resource_desc (0x09e3b3d0, 16B)

- 位置: incbin `0x1E3B35E, 0xD6` 内, offset = 0x1E3B3D0 - 0x1E3B35E = 0x72
- 内容: 4 ptrs to name_o_01 paths (ncer/nanr/ncgr/nclr paths at 0x09e3b360/37c/398/3b4)
- raw=1 ref; carve 16B
- NOTE: name_o paths 0x09e3b360..0x09e3b3c8 also in same incbin and each has 1 ref
- 建议: 当场 carve 整个 name_o resource block (offset 0..D2 of incbin 0x1E3B35E: paths + desc + file paths)

carve F 结构 (位于 incbin `0x1E3B35E, 0xD6` 内):
```
.incbin "roms/2343.gba", 0x1E3B35E, 0x2   @ 2B pad
name_o_ncer_path:                          @ 0x09e3b360
    .asciz "name_input/name_o_01.LZncer"  @ + align pad
name_o_nanr_path:                          @ 0x09e3b37c
    .asciz "name_input/name_o_01.LZnanr"
name_o_ncgr_path:                          @ 0x09e3b398
    .asciz "name_input/name_o_01.LZncgr"
name_o_nclr_path:                          @ 0x09e3b3b4
    .asciz "name_input/name_o_01.LZnclr"
name_o_resource_desc:                      @ 0x09e3b3d0
    .word name_o_ncer_path
    .word name_o_nanr_path
    .word name_o_ncgr_path
    .word name_o_nclr_path
name_b_01_path:                            @ 0x09e3b3e0
    .asciz "name_input/name_b_01.LZ5bg"
name_b_02_path:                            @ 0x09e3b3fc
    .asciz "name_input/name_b_02.LZ5bg"
name_b_04_path:                            @ 0x09e3b418
    .asciz "name_input/name_b_04.LZ5bg"
.incbin "roms/2343.gba", 0x1E3B434, 0x3B  @ remainder to end (ends 0x1E3B46F)
```

NOTE: 上述 asciz 长度需从 ROM bytes 精确计算 (含 NUL + 4B 对齐 pad). 实际执行时需 byte-identical 验证.

### carve G: cursor_anim_data_a/b (0x09e3b46f+0x09e3b47c, 40B)

- 位置: incbin `0x1E3B46F, 0x1115` 头部 (offset=0 和 +0xd)
- anim_data_a: 12B bytes (`06 08 0a 06 08 0a 0a 08 0a 08 0a 08`)
- anim_data_b: 28B words (`c1 ff ff ff 85 00 00 00 ...` = 7 signed s32 coords)
- raw=1 ref (anim_a also thumb=1)

```
cursor_anim_data_a:                        @ 0x09e3b46f
    .byte 6, 8, 10, 6, 8, 10, 10, 8, 10, 8, 10, 8  @ 12B x/y offsets for 5 cursor cells + pad
.incbin "roms/2343.gba", 0x1E3B47B, 0x1   @ 1B gap
cursor_anim_data_b:                        @ 0x09e3b47c
    .word 0xffffffc1    @ cell 0: x_start (signed -63)
    .word 0x00000085    @ cell 1: x coord
    .word 0x00000019    @ cell 2
    .word 0x00000085    @ cell 3
    .word 0x00000071    @ cell 4
    .word 0x00000085    @ cell 5
    .word 0x000000c9    @ cell 6
.incbin "roms/2343.gba", 0x1E3B498, 0x1087  @ remainder
```

NOTE: `cursor_anim_data_b` at 0x09e3b47c = 0x1E3B47C, offset +0xd from incbin start. 实际切分需精确计算 1B gap (0x1E3B47B).

### carve H: name_o_palette_data (0x09ccd290, 32B)

- 位置: `asm/rom.s` line 673 incbin `0x1CCD290, 0x16D0` -- incbin 起点恰好是 0x09ccd290
- raw=15 refs (多处 caller 加载此 palette)
- 内容: GBA 16-bit 调色板 16 色 (32B): RGB15 颜色值 (基础色 + 暗色变体)
  ```
  [0]=0x0000 [1]=0x7c00 [2]=0x001f [3]=0x7c1f [4]=0x03e0 [5]=0x7fe0 [6]=0x03ff [7]=0x7fff
  [8]=0x2108 [9]=0x6000 [a]=0x0018 [b]=0x6018 [c]=0x0300 [d]=0x6300 [e]=0x0318 [f]=0x5294
  ```
- carve: 从 incbin 头部切 32B

```
name_o_palette_data:                       @ 0x09ccd290 (line 673 region)
    .hword 0x0000, 0x7c00, 0x001f, 0x7c1f, 0x03e0, 0x7fe0, 0x03ff, 0x7fff
    .hword 0x2108, 0x6000, 0x0018, 0x6018, 0x0300, 0x6300, 0x0318, 0x5294
.incbin "roms/2343.gba", 0x1CCD2B0, 0x16B0   @ remaining (end: 0x1CCE960)
```

- 代码侧: DAT_08018228 -> DATA ref `name_o_palette_data` + setName `name_input_page_load_assets_name_o_palette_data`
- 消费者证据: asm line 10432-10433 `DAT_08018228: .word 0x09ccd290` + bios_cpu_set dst=BG PALRAM (0x05000020), ctrl=BG0CNT => copies 16 colors (32B) to BG palette slot 16. 15 refs across name_input / banlist / settings scenes.
- 置信度: high

### carve I: assert_table_last_fmt (0x09e3b338, 14B)

- 位置: incbin `0x1E3B336, 0x12` 内, offset=+2 (前 2B 为 NUL pad)
- 内容: `.asciz "TableLast(%d)\n"` (14B incl NUL)
- raw=1 ref (encode_str_table_entry_to_line_buf suppress_display_output call)

```
.incbin "roms/2343.gba", 0x1E3B336, 0x2   @ 2B NUL pad
assert_table_last_fmt:                     @ 0x09e3b338
    .asciz "TableLast(%d)\n"               @ 14B (ends 0x1E3B346)
.incbin "roms/2343.gba", 0x1E3B346, 0x8   @ remaining to end of original incbin (0x1E3B348)
```

NOTE: 原 incbin 0x1E3B336, 0x12 结尾 = 0x1E3B348. 切后剩余 8B 补 incbin.

---

## disasm 计划 (R4)

Seg-6 内无误标为数据的代码块 (ROM_INCBIN 0x186ce 已判定为 §5.1)。

---

## 新增 constants / 全局

### 追加 name_input.inc

```
.equ NAME_INPUT_BG0_SCREEN_CLEAR_CTRL, 0x01000200
.equ NAME_INPUT_CHAR_VRAM_CLEAR_CTRL,  0x01001800
.equ NAME_INPUT_BG_ROW_CLEAR_CTRL,     0x05000160
```

### 追加 oam_attr.inc

```
.equ OAM_HFLIP_VFLIP_PACKED_PATTERN, 0x40004000
.equ OAM_ATTR1_X_MASK,               0x000001ff
.equ OAM_ATTR1_X_CLEAR,              0xfffffe00
```

注: `0x001fffff` (zero_obj_vram_tiles cpuset mask) -- 与 fill_vram_screen_rect_zero_cpuset_wordcount_mask 同值但不同函数, 单独 RENAME_SLOT 处理 (命名 `zero_obj_vram_tiles_cpuset_wordcount_mask`)。

---

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址 | 大小 | 所在 Seg | 初判内容 | ref-scan 证据 |
|---|---|---|---|---|
| ROM_INCBIN 0x186ce | 34 B | Seg-6 | THUMB leaf fn `get_language_stride()` (returns 1=JP 2=EN, reads gSettings bits[2:0]) + 2B align pad + 4B literal pool. dead-code 编译变体 (同逻辑在多个 caller 内联). | 全 16 个 4B sub-addr raw=0 thumb=0; entry 0x080186d0 THUMB addr=0 |

---

## 消费者证据 (R6) -- 关键槽语义

| 槽/常量 | 消费者 | file:line | 置信度 |
|---|---|---|---|
| gState=0x02029250 (18 slots) | 全段 28 fn 均读/写 gState | asm/00_system_str_vija.s 9230..11246 | high |
| OAM_ATTR2_CHARNAME_MASK=0x3ff | build_sprite_oam_row: `ands r1,r0` on attr2 tile field | asm line 10589-10596 | high |
| OAM_ATTR2_CHARNAME_CLEAR=0xfffffc00 | build_sprite_oam_row: clears tile bits before OR | asm line 10621-10622 | high |
| GFX_ATTR_CLEAR_BITS_13_7=0xffffc07f | name_input_page_load_assets: `ands r0,r1` on sprite attr | asm line 10368 | high |
| OBJ_TILE_VRAM_BASE=0x06010000 | zero_obj_vram_tiles: `adds r3,r3,r0` adds tile_idx*32 to base | asm line 10729-10731 | high |
| 0x09e3b2b4 (line_break_seq) | encode_char_to_line_buf plate "LINE_BREAK_BYTES=0x09e3b2b4" | asm line 9248 plate | high |
| 0x09e587ec (name_char_tile_slot_table) | refresh_selected_char_obj_tile: `ldrh r6,[r0,#0]` reads tile_idx for ping-pong | asm line 11216 | high |
| 0x09e587f0 (name_char_group_ptr_table) | encode_str_table_entry_to_line_buf: `lsls r0,r6,#2; adds r0,r0,r1; ldr r0,[r0,#0]` index | asm line 9349-9351 | high |
| 0x05000020 (bg_palette_dst) | name_input_page_load_assets: bios_cpu_set dst=0x05000020=PALRAM+0x20 (BG pal entry 16) | asm line 10385-10386 | high |
| 0x05000220 (obj_palette_dst) | name_input_page_load_assets: bios_cpu_set dst=0x05000220=OBJ PALRAM+0x20 | asm line 10387-10390 | high |
| 0x09e3b46f (cursor_anim_data_a) | render_settings_cursor_cell_anims: `bl memcpy; r2=sp+0x8; movs r2,#0xc` copies 12B | asm line 10945-10948 | high |
| 0x09e3b47c (cursor_anim_data_b) | render_settings_cursor_cell_anims: `ldmia r0!,...` 7-word block | asm line 10951-10959 | high |

---

## 求助 (低置信度语义) — RESOLVED by driver (static ROM inspection)

### 执行拆分 (driver 决定): Seg-6a / Seg-6b (地址序, 不回头)

Seg-6 命中**大型共享资产** (JP 名字输入假名字符表), carve 体量大。按地址序拆两次落地, 各自 byte-identical 隔离:
- **Seg-6a** [0x1794c..0x08017e48, 5 fn]: load_game_str_1006_to_state / encode_char_to_line_buf /
  encode_str_table_entry_to_line_buf / render_name_input_jp_labels_to_obj / dispatch_banlist_text_by_key。
  含**假名表 carve 簇** (carve B/C/D/E/I + kana 池 + ptr 表) + 这 5 fn 的槽符号化 + R5。
- **Seg-6b** [0x08017e48..0x08018774, 23 fn]: 其余 render/scroll/cursor/load_assets。
  含 carve A/F/G/H + §5.1 块 0x186ce + 大批 gState/EWRAM_BASE/GSETTINGS_OFFSET 符号化 + R5。

### 假名表精确测定 (carve B/C/D/E, 全部 byte-identical-safe, label+incbin-span)

1. **name_char_group_ptr_table (carve B, 0x09e587f0)**: **精确 50 entries × 4B = 200B**, 终址
   0x09e588b8 (第 51 个 word=0x08017575 已是代码地址, 出界)。50 个 .word 指向 kana 池
   (0x09e3b058..0x09e3b248, 降序; 有重复目标如 [36][38][48][49]→0x09e3b0b0)。carve: `name_char_group_ptr_table:`
   + 50 `.word <kana label>` (symbolize 到 kana 池 label) + 余 incbin。host=incbin 0x1E587EC,0x520
   (carve A 在其头 4B, ptr 表在 +4)。

2. **kana 池 + name_char_range_table + line_break_seq + banlist_jp_str_src** 全在
   **host=incbin 0x1E3AFDC, 0x2DC** (0x09e3afdc..0x09e3b2b8, 732B)。该区**51 个 distinct 被引用地址**
   (ref-scan raw/THUMB|1 实测), 即:
   - 0x09e3afdc (+0x0): `banlist_jp_str_src` (SJIS JP, dispatch key=2 copy)
   - 0x09e3b058..0x09e3b248 (47 个 kana group SJIS 串, name_char_group_ptr_table 的目标)
   - 0x09e3b250 (+0x274): THUMB|1 ref (1 个, 待 fixer 核; 紧邻 range_table)
   - 0x09e3b251 (+0x275): `name_char_range_table` (raw+THUMB refs; SJIS 区段边界字节
     `889f 88c8 8945 8960...`, encode_str_table 用 r6 索引读 2B 对)
   - 0x09e3b2b4 (+0x2d8): `line_break_seq` = `81 40 00 00` (SJIS 全角空格 + NUL, 4B 到区尾)
   **carve 法 (byte-identical-safe, 无需定 SJIS 语义)**: 在 51 个被引用 offset 各置一 label,
   相邻 label 间用 `.incbin` span 填原字节 (label 名: banlist_jp_str_src / name_char_group_<offidx>
   或按 ptr 表序 name_char_group_NN / name_char_range_table / line_break_seq)。原字节零改动 →
   byte-identical 保证。fixer 用脚本据 ref 列表程序化生成 carve block (类比 4.0b 断言串 carve 的
   137 incbin + 156 .asciz 内联方式)。

3. **name_char_range_table 精确大小无需确定** (上方 label+incbin-span 法): label 落 0x09e3b251,
   后续字节 incbin 到下一 label (line_break_seq @0x09e3b2b4)。size = 0x2b4-0x251 = 0x63 B 由 incbin
   span 覆盖, **不需语义结构化**。原 BLOCKED (大小未知) 消解。

4. **char_sentinel 0x0000e3a9 (DAT_08017b1c)**: 不是地址 (不在任何 ROM 区), 是 encode_str_table
   循环的 `cmp r4,r5` 上界字面常量。**保持 RENAME_SLOT** (`encode_str_table_entry_to_line_buf_char_sentinel`)
   + ASCII EOL 仅陈述静态事实 (`upper-bound literal 0xe3a9 in char-group scan cmp`), 不臆造哨兵/下界语义。
   非 carve / 非 BLOCK。

5. ~~0x09ccd290 定位~~ 已解决: rom.s line 673 incbin 头部, 32B 调色板 carve H 直接可做。

精确 host incbin 行 (已核 rom.s): 673(0x1CCD290,0x16D0=carve H) / 934(0x1E3AFDC,0x2DC=kana簇)
/ 940(0x1E3B336,0x12=carve I) / 943(0x1E3B35E,0xD6=carve F) / 946(0x1E3B46F,0x1115=carve G)
/ 1294(0x1E587EC,0x520=carve A+B)。所有 carve 区 ref 已 driver 重扫确认 (见会话 ROM dump)。
