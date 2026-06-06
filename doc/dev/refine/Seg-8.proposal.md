# Refine Proposal: Seg-8  [0x08019a58..0x0801a794)

## 段测绘

### 函数入口 x28
| 地址 | 名称 |
|---|---|
| 0x08019a58 | encode_pass_table_entry_to_line_buf |
| 0x08019b4c | render_banlist_pass_char_obj_rows_pair |
| 0x08019c44 | reject_banlist_input_event |
| 0x08019c48 | load_banlist_password_table_from_rom |
| 0x08019c90 | write_banlist_bg2_scroll_regs_biased |
| 0x08019ca4 | render_banlist_password_chars_row |
| 0x08019d14 | init_banlist_pass_input_bg0_page |
| 0x08019da4 | render_banlist_password_chars_grid |
| 0x08019e2c | init_banlist_pass_input_bg2_page |
| 0x08019ed4 | get_banlist_password_page_ptr |
| 0x08019f24 | init_banlist_pass_chars_grid_row |
| 0x08019f78 | refresh_banlist_pass_chars_font_rows |
| 0x08019fe4 | tick_banlist_scroll_input_handler |
| 0x0801a154 | get_banlist_scroll_direction |
| 0x0801a16c | set_banlist_scroll_step |
| 0x0801a1ac | tick_banlist_bg_scroll_step |
| 0x0801a230 | render_banlist_title_text_to_bg |
| 0x0801a328 | load_banlist_pass_input_scene_resources |
| 0x0801a49c | tick_banlist_card_slot_anim_oam |
| 0x0801a540 | call_tick_banlist_card_slot_anim |
| 0x0801a560 | setup_banlist_sprite_oam_row_batch |
| 0x0801a690 | call_setup_banlist_sprite_oam_row |
| 0x0801a6b4 | render_banlist_char_obj_row |
| 0x0801a6e4 | zero_obj_tile_vram_range |
| 0x0801a718 | init_banlist_scrollbar_oam_entry |
| 0x0801a74c | advance_banlist_scrollbar_pos_page |
| 0x0801a770 | retreat_banlist_scrollbar_pos_page |
| (0x0801a794 | tick_banlist_scrollbar_and_slot_anim -- Seg-9 start, NOT in Seg-8) |

### 残留自动名槽 (完整列表)

#### PTR 槽 (已符号化, 按策略跳过)
PTR_gBanlistPasswordBuffer_* x多处, PTR_BG2VOFS, PTR_BG3VOFS, PTR_BG0CNT,
PTR_game_str_pointer_table_*, PTR_game_str_ja_*, PTR_font_jp_base_table_* 均已有符号名, 跳过。

已命名 assert 串槽:
- set_banlist_scroll_step_pass_main_c_filename -> pass_main_c_filename (carved)
- set_banlist_scroll_step_assert_dir_1_dir_1_59c -> assert_dir_1_dir_1_59c (carved)
- tick_banlist_card_slot_anim_oam_pass_main_c_filename -> pass_main_c_filename (carved)
- tick_banlist_card_slot_anim_oam_assert_anmid_ig2d_getanmsequencescoun_670 -> carved

#### 未命名 DAT_/DWORD_ 槽 (本段目标)
见 EQ_SLOTS / REF_SLOTS / RENAME_SLOTS 章节。

### ROM_INCBIN / .byte 块
| 块 | 地址 | size |
|---|---|---|
| ROM_INCBIN A | 0x0801a89c | 0x20 (32B) |
| ROM_INCBIN B | 0x0801ad18 | 0xec (236B) |

---

## 数据块分类 (Rule 2/3)

### 块 A: ROM_INCBIN 0x1a89c, 0x20

**ref-scan**:
```python
d.count(pack('<I', 0x0801a8a0)) = 1   # raw, at ROM 0x08af5768 (compressed FS asset)
d.count(pack('<I', 0x0801a8a1)) = 0   # THUMB ref: 0
# All other addrs in block: raw=0, thumb=0
```

**判定: §5.1** (0 THUMB refs; the single raw hit at 0x08af5768 is in compressed FS data, confirmed coincidence).

Content bytes: `0548 0649 1840 2107 7800 4001 2001 2900 d100 2002 4770 0000 | 00000002 2c6c0000`
Block sits between retreat_banlist_password_cursor_slot literal pool and load_banlist_char_by_cursor_slot. It resembles THUMB code (BL halfwords, bx lr=0x4770) but has 0 callers. Not a named Ghidra function.

### 块 B: ROM_INCBIN 0x1ad18, 0xec

**ref-scan** (each case handler addr):
```python
d.count(pack('<I', 0x0801ad18)) = 1  raw   # from jump table at 0x0801ad00[0]
d.count(pack('<I', 0x0801ad20)) = 1  raw   # from 0x0801ad08[0]
d.count(pack('<I', 0x0801ad4c)) = 1  raw   # from 0x0801ad08[2]
d.count(pack('<I', 0x0801ad94)) = 1  raw   # from 0x0801ad10
d.count(pack('<I', 0x0801ade0)) = 1  raw   # from 0x0801ad14
# THUMB refs: all 0 (table uses MOV PC, Rn with raw addr -> stays THUMB)
```

**判定: disasm (R4)** -- active THUMB code. dispatch_banlist_cursor_action (0x0801acac) builds a jump table at 0x0801ad00 (6 entries), loads case handler via `ldr r0,[table+idx*4]`, then `mov pc, r0` (opcode 0x4687 = MOV PC, R0). In THUMB mode, MOV PC,Rn does NOT switch ISA (unlike BX), so even addresses remain THUMB. The block contains 5 active case handlers for banlist cursor input (advance char / reject / grid init / page scroll / extended grid).

Block literal pool contains: 0x0000064c (scrollbar offset) x2, 0x03000040 (gPrng).

**disasm range**: 0x0801ad18..0x0801ae04 THUMB, 5 stub entries at: 0x0801ad18, 0x0801ad20, 0x0801ad4c, 0x0801ad94, 0x0801ade0.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 复用现有 inc)

All values reference existing constants in ewram.inc / gba_mem.inc / name_input.inc / oam_attr.inc.

| 槽 | value | const_name | inc 来源 | slot_label |
|---|---|---|---|---|
| DAT_08019c20 | 0x0202348c | gTextEncodingOverride | ewram.inc | encode_pass_char_obj_rows_pair_ptr_encoding_override |
| DAT_08019c2c | 0x02000000 | EWRAM_BASE | gba_mem.inc | encode_pass_char_obj_rows_pair_ewram_base |
| DAT_08019c30 | 0x00006c2c | GSETTINGS_OFFSET | name_input.inc | encode_pass_char_obj_rows_pair_gsettings_offset |
| DAT_08019c38 | 0x00000675 | -- | -- | encode_pass_char_obj_rows_pair_pass_buf_off_675 |
| DAT_08019c40 | 0x00000674 | -- | -- | encode_pass_char_obj_rows_pair_pass_buf_off_674 |
| DWORD_08019f08 | 0x02000000 | EWRAM_BASE | gba_mem.inc | get_banlist_password_page_ptr_ewram_base |
| DWORD_08019f0c | 0x00006c2c | GSETTINGS_OFFSET | name_input.inc | get_banlist_password_page_ptr_gsettings_offset |
| DWORD_0801a310 | 0x02000000 | EWRAM_BASE | gba_mem.inc | render_banlist_title_text_to_bg_ewram_base |
| DWORD_0801a314 | 0x00006c2c | GSETTINGS_OFFSET | name_input.inc | render_banlist_title_text_to_bg_gsettings_offset |
| DWORD_0801a320 | 0x02006ed0 | gFontJpCtx | ewram.inc | render_banlist_title_text_to_bg_ptr_font_jp_ctx |
| DAT_0801a800 | 0x02000000 | EWRAM_BASE | gba_mem.inc | advance_banlist_password_cursor_slot_ewram_base |
| DAT_0801a804 | 0x00006c2c | GSETTINGS_OFFSET | name_input.inc | advance_banlist_password_cursor_slot_gsettings_offset |
| DAT_0801a890 | 0x02000000 | EWRAM_BASE | gba_mem.inc | retreat_banlist_password_cursor_slot_ewram_base |
| DAT_0801a894 | 0x00006c2c | GSETTINGS_OFFSET | name_input.inc | retreat_banlist_password_cursor_slot_gsettings_offset |
| DAT_0801a5ec | 0x000003ff | OAM_ATTR2_CHARNAME_MASK | oam_attr.inc | setup_banlist_sprite_oam_row_batch_attr2_charname_mask |
| DAT_0801a5f0 | 0xfffffc00 | OAM_ATTR2_CHARNAME_CLEAR | oam_attr.inc | setup_banlist_sprite_oam_row_batch_attr2_charname_clear |
| DAT_0801a688 | 0x000001ff | OAM_ATTR1_X_MASK | oam_attr.inc | setup_banlist_sprite_oam_row_batch_attr1_x_mask |
| DAT_0801a68c | 0xfffffe00 | OAM_ATTR1_X_CLEAR | oam_attr.inc | setup_banlist_sprite_oam_row_batch_attr1_x_clear |
| DAT_0801a710 | 0x06010000 | OBJ_TILE_VRAM_BASE | gba_mem.inc | zero_obj_tile_vram_range_obj_tile_vram_base |

Notes on EQ confidence (all high; verified by Python ROM dump read):
- DAT_08019c38=0x675, DAT_08019c40=0x674: byte offsets within gBanlistPasswordBuffer (=0x02029810+0x675/0x674 = 0x02029E85/0x02029E84 -> OBJ row pixel-width bytes). No existing named constant for these specific offsets. Rename only (no new constant created; offset semantics clear from plate).
- OAM_ATTR2_CHARNAME_MASK/CLEAR, OAM_ATTR1_X_MASK/CLEAR: verified against oam_attr.inc values; exact match.

#### gBanlistPasswordBuffer-referenced offset slots (EQ via RENAME, no new equate)
These slots hold EWRAM offsets into gBanlistPasswordBuffer. Values are scene-private (used in exactly 1-5 functions each). Defined pattern from Seg-7: rename as `<func>_pass_buf_off_<hex>`. No new constants.inc entries; EQ via data-equate pointing to decimal constant.

| 槽 | value | slot_label |
|---|---|---|
| DAT_08019b24 | 0x00000661 | encode_pass_table_entry_to_line_buf_pass_buf_off_661 |
| DWORD_08019c80 | 0x0000029f | load_banlist_password_table_from_rom_max_entries |
| DWORD_08019c8c | 0x000005a2 | load_banlist_password_table_from_rom_byte_guard |
| DWORD_08019d9c | 0x01000200 | init_banlist_pass_input_bg0_page_cpuset_screen |
| DWORD_08019da0 | 0x01000898 | init_banlist_pass_input_bg0_page_cpuset_char |
| DWORD_08019ec8 | 0x01000200 | init_banlist_pass_input_bg2_page_cpuset_screen |
| DWORD_08019ecc | 0x00000664 | init_banlist_pass_input_bg2_page_pass_buf_off_664 |
| DWORD_08019ed0 | 0x0000066e | init_banlist_pass_input_bg2_page_pass_buf_off_66e |
| DWORD_0801a010 | 0x0000064c | tick_banlist_scroll_input_handler_scrollbar_off |
| DWORD_0801a064 | 0x00000663 | tick_banlist_scroll_input_handler_char_step_off_a |
| DWORD_0801a094 | 0x00000663 | tick_banlist_scroll_input_handler_char_step_off_b |
| DWORD_0801a0b0 | 0x00000663 | tick_banlist_scroll_input_handler_char_step_off_c |
| DWORD_0801a114 | 0x00000663 | tick_banlist_scroll_input_handler_char_step_off_d |
| DWORD_0801a150 | 0x00000663 | tick_banlist_scroll_input_handler_char_step_off_e |
| DWORD_0801a168 | 0x00000666 | get_banlist_scroll_direction_scroll_dir_off |
| DWORD_0801a1a0 | 0x000002cd | set_banlist_scroll_step_assert_line_2cd |
| DWORD_0801a1a8 | 0x00000666 | set_banlist_scroll_step_step_field_off |
| DWORD_0801a1e8 | 0x00000663 | tick_banlist_bg_scroll_step_scroll_step_off |
| DWORD_0801a1ec | 0x00000666 | tick_banlist_bg_scroll_step_scroll_dir_off |
| DWORD_0801a308 | 0x00001037 | render_banlist_title_text_to_bg_str_id |
| DWORD_0801a31c | 0x06002280 | render_banlist_title_text_to_bg_char_vram_addr |
| DWORD_0801a45c | 0x000005a4 | load_banlist_pass_input_scene_resources_obj_anim_off_a |
| DWORD_0801a460 | 0x000005ac | load_banlist_pass_input_scene_resources_obj_anim_off_b |
| DWORD_0801a468 | 0xffffc07f | load_banlist_pass_input_scene_resources_clr_mask |
| DWORD_0801a474 | 0x05000020 | load_banlist_pass_input_scene_resources_bg_palette_slot1 |
| DWORD_0801a47c | 0x05000220 | load_banlist_pass_input_scene_resources_obj_palette_slot1 |
| DWORD_0801a480 | 0x05000202 | load_banlist_pass_input_scene_resources_obj_palette_fill_dst |
| DAT_0801a4ec | 0x000005a4 | tick_banlist_card_slot_anim_oam_sprite_ptr_off_a |
| DAT_0801a4f4 | 0x0000036f | tick_banlist_card_slot_anim_oam_assert_line_36f |
| DAT_0801a4fc | 0x000005ac | tick_banlist_card_slot_anim_oam_sprite_ptr_off_b |
| DAT_0801a5f4 | 0x40004000 | setup_banlist_sprite_oam_row_batch_wide_sprite_mode |
| DAT_0801a714 | 0x001fffff | zero_obj_tile_vram_range_word_count_mask |
| DAT_0801a748 | 0x0000064c | init_banlist_scrollbar_oam_entry_scrollbar_off |
| DAT_0801a76c | 0x0000064c | advance_banlist_scrollbar_pos_page_scrollbar_off |
| DAT_0801a790 | 0x0000064c | retreat_banlist_scrollbar_pos_page_scrollbar_off |
| DAT_0801a838 | 0x00000667 | advance_banlist_password_cursor_slot_dir_field_off |
| DAT_0801a898 | 0x00000667 | retreat_banlist_password_cursor_slot_dir_field_off |

Value evidence (all verified by python ROM dump read, `struct.unpack_from('<I', d, addr-0x08000000)[0]`):
- DWORD_0801a31c=0x06002280: banlist title text render target in BG char VRAM. char_base=0 in BGxCNT, tile slot 0x114 = addr 0x06000000+0x114*0x20=0x06002280. Caller is render_banlist_title_text_to_bg passing to init_font_jp_render_context. Confidence high.
- DWORD_0801a1a0=0x000002cd=717 decimal: assert line number in set_banlist_scroll_step, verified against pass_main_c_filename. Confidence high.
- DAT_0801a5f4=0x40004000: stored then orrs into OAM attr0+attr1 combined word. attr0 bits[15:14]=01 (wide), attr1 bits[15:14]=01 (size). Together = 64x32 wide OBJ sprite mode. Confidence med (runtime OBJ size confirmed by adjacent slot attrs, but exact GBA OBJ size lookup not done statically).
- DAT_0801a714=0x001fffff: ands with r2=r1*8 (tile count * words-per-tile). bit20:0 mask for bios_cpu_set word_count field. Confidence high.

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM global or carve label)

#### Already-carved labels (REF only, no new carve)
| 槽 | target | gas_label | slot_label |
|---|---|---|---|
| DAT_08019b28 | 0x09e588cc | banlist_pass_char_group_ptr_table | encode_pass_table_entry_to_line_buf_ptr_pass_char_group_table |
| DWORD_0801a470 | 0x09ccd290 | name_o_palette_data | load_banlist_pass_input_scene_resources_ptr_name_o_palette |
| DWORD_0801a164 | 0x02029810 | gBanlistPasswordBuffer | get_banlist_scroll_direction_ptr_banlist_pw_buf |
| DWORD_0801a904 | 0x02029810 | gBanlistPasswordBuffer | load_banlist_char_by_cursor_slot_ptr_banlist_pw_buf |
| DWORD_0801a948 | 0x02029810 | gBanlistPasswordBuffer | get_banlist_scroll_pixel_offset_ptr_banlist_pw_buf |
| DWORD_0801a97c | 0x02029810 | gBanlistPasswordBuffer | get_banlist_password_entry_ptr_ptr_banlist_pw_buf |
| DWORD_0801a9ec | 0x02029810 | gBanlistPasswordBuffer | render_banlist_text_col_cleared_ptr_banlist_pw_buf |
| DWORD_0801aa14 | 0x02029810 | gBanlistPasswordBuffer | render_banlist_pw_chars_to_buf_ptr_banlist_pw_buf |
| DWORD_0801aa78 | 0x02029810 | gBanlistPasswordBuffer | advance_banlist_pw_char_and_render_ptr_banlist_pw_buf |
| DWORD_0801aba4 | 0x02029810 | gBanlistPasswordBuffer | retreat_banlist_pw_char_and_render_ptr_banlist_pw_buf |

Note: all PTR_gBanlistPasswordBuffer_* slots throughout segment already carry gBanlistPasswordBuffer as their resolved value (asm shows `.word gBanlistPasswordBuffer`). The DWORD_ slots above currently show raw 0x02029810. Above REF plan applies Ghidra USER label + DATA ref to connect them.

#### New carves needed (from name_input_default_name host, 0x1E3B4A8, 0x10DC)

Host split coverage equation (sum=0x10DC, verified):
```
pre: .incbin 0x1E3B4A8, 0x809      (0x09e3b4a8..0x09e3bcb1)
banlist_char_candidate_str: label + .incbin 0x1E3BCB1, 0xB6  (182B, 90 SJIS pairs + null pair)
gap1: .incbin 0x1E3BD67, 0x276     (0x09e3bd67..0x09e3bfdd; contains banlist_pass_ext_char_group)
banlist_pass_char_str: label + .incbin 0x1E3BFDD, 0x63  (99B, 96 SJIS bytes + null + 2B pad)
banlist_pass_alt_char: label + .incbin 0x1E3C040, 0x4   (4B: 8140 0000 = full-width space + null)
rom_password_table: label + .incbin 0x1E3C044, 0x53E    (671 x 2B LE halfwords)
post: .incbin 0x1E3C582, 0x2        (2B trailing pad to host end 0x1E3C584)
0x809 + 0xB6 + 0x276 + 0x63 + 0x4 + 0x53E + 0x2 = 0x10DC  OK
```

banlist_pass_ext_char_group at 0x09e3be3c is within gap1. To avoid splitting gap1 further (only 1 code ref from DWORD_0801abb0), add GAS label at offset 0x809+0xB6+(0x09e3be3c-0x09e3bd67)=0x276 within gap1 span, effectively: sub-label inside gap1 incbin. Implementation: split gap1 into [pre-ext: .incbin 0x1E3BD67, 0xD5] + [banlist_pass_ext_char_group: label + .incbin 0x1E3BE3C, 0x1A1].

Revised coverage for gap1:
```
gap1a: .incbin 0x1E3BD67, 0xD5     (0x09e3bd67..0x09e3be3c)
banlist_pass_ext_char_group: label + .incbin 0x1E3BE3C, 0x1A1  (0x09e3be3c..0x09e3bfdd)
0xD5 + 0x1A1 = 0x276  OK
```

Carve slots:
| 槽 | target | gas_label | slot_label |
|---|---|---|---|
| DWORD_08019d98 | 0x09e3bcb1 | banlist_char_candidate_str | init_banlist_pass_input_bg0_page_ptr_char_candidate_str |
| DWORD_0801a908 | 0x09e3bcb1 | banlist_char_candidate_str | load_banlist_char_by_cursor_slot_ptr_char_candidate_str |
| DAT_08019b2c | 0x09e3bfdd | banlist_pass_char_str | encode_pass_table_entry_to_line_buf_ptr_pass_char_str |
| DAT_08019b30 | 0x09e3c040 | banlist_pass_alt_char | encode_pass_table_entry_to_line_buf_ptr_alt_char |
| DWORD_0801a918 | 0x09e3c040 | banlist_pass_alt_char | load_banlist_char_by_cursor_slot_ptr_alt_char |
| DWORD_08019c88 | 0x09e3c044 | rom_password_table | load_banlist_password_table_from_rom_ptr_password_table |
| DWORD_0801abb0 | 0x09e3be3c | banlist_pass_ext_char_group | retreat_banlist_pw_char_and_render_ptr_ext_char_group |

#### New carves from incbin 0x1E3C5B2, 0xBE (assert_dir... host)

Host: incbin 0x1E3C5B2, 0xBE (0x09e3c5b2..0x09e3c670).
Content: 4 OBJ GFX fs paths (pass_o_01.{ncer,nanr,ncgr,nclr}), 4-word resource desc ptr struct, 2 BG fs paths.

Split coverage:
```
pre: .incbin 0x1E3C5B2, 0x2         (2B pad before paths)
banlist_pass_obj_ncer_path: .asciz "pass_input/pass_o_01.LZncer"  (0x1C bytes)
banlist_pass_obj_nanr_path: .asciz "pass_input/pass_o_01.LZnanr"  (0x1C bytes)
banlist_pass_obj_ncgr_path: .asciz "pass_input/pass_o_01.LZncgr"  (0x1C bytes)
banlist_pass_obj_nclr_path: .asciz "pass_input/pass_o_01.LZnclr"  (0x1C bytes)
banlist_pass_obj_resource_desc:  (4 x .word ptr; 0x10 bytes)
  .word banlist_pass_obj_ncer_path
  .word banlist_pass_obj_nanr_path
  .word banlist_pass_obj_ncgr_path
  .word banlist_pass_obj_nclr_path
banlist_pass_bg1_fs_path: .asciz "pass_input/pass_b_01.LZ5bg"   (0x1C bytes incl null+pad)
banlist_pass_bg2_fs_path: .asciz "pass_input/moziire_b_01.LZ5bg" (0x1E bytes)
0x2+0x1C*4+0x10+0x1C+0x1E = 0x2+0x70+0x10+0x1C+0x1E = 0xBC... 
```

Size check:
- 2B pre
- 4 x .asciz paths: each string + null. Lengths: 28, 28, 28, 28 bytes (0x1c each) = 0x70
- 4-word ptr struct: 0x10B
- bg1 path: "pass_input/pass_b_01.LZ5bg\0" = 27B + 1pad = 0x1B+pad; actual: 0x1C (27+1=28?)
  - From python: size=27 including null. Let's use .asciz + 1B pad alignment.
- bg2 path: "pass_input/moziire_b_01.LZ5bg\0" = 30 bytes
- Total: 2+0x70+0x10+0x1c+0x1e = 2+112+16+28+30 = 188 = 0xBC... but host size = 0xBE.
  - Difference: 0xBE - 0xBC = 2. Check paths again with actual file:
  - bg1: "pass_input/pass_b_01.LZ5bg" = 26 chars + null = 27B. +1B pad = 28B. OK.
  - bg2: "pass_input/moziire_b_01.LZ5bg" = 29 chars + null = 30B. No pad. 30B.
  - 2+0x70+0x10+28+30 = 0xBE. OK.

Implementation: since the 4 obj paths are identical prefix (only suffix differs), use label+incbin-span for byte-safety (not .asciz) to avoid any encoding ambiguity:
```
pre: .incbin 0x1E3C5B2, 0x2
banlist_pass_obj_ncer_path: .incbin 0x1E3C5B4, 0x1C
banlist_pass_obj_nanr_path: .incbin 0x1E3C5D0, 0x1C
banlist_pass_obj_ncgr_path: .incbin 0x1E3C5EC, 0x1C
banlist_pass_obj_nclr_path: .incbin 0x1E3C608, 0x1C
banlist_pass_obj_resource_desc:
  .word banlist_pass_obj_ncer_path
  .word banlist_pass_obj_nanr_path
  .word banlist_pass_obj_ncgr_path
  .word banlist_pass_obj_nclr_path
banlist_pass_bg1_fs_path: .incbin 0x1E3C634, 0x1C  (28B including null+pad)
banlist_pass_bg2_fs_path: .incbin 0x1E3C650, 0x1E  (30B)
0x2+0x1C+0x1C+0x1C+0x1C+0x10+0x1C+0x1E = 0xBE  OK
```

CAUTION: banlist_pass_obj_resource_desc stores 4 raw ROM pointers (.word labels). These pointers are the actual ROM addresses of the 4 strings. Verify: banlist_pass_obj_ncer_path at 0x09e3c5b4 -> .word 0x09e3c5b4 = .word banlist_pass_obj_ncer_path. GAS emits absolute ROM address. Byte-identical IFF linker org matches ROM layout. This is the existing pattern for carves in rom.s.

Carve slots:
| 槽 | target | gas_label | slot_label |
|---|---|---|---|
| DWORD_0801a458 | 0x09e3c624 | banlist_pass_obj_resource_desc | load_banlist_pass_input_scene_resources_ptr_obj_resource_desc |
| DWORD_0801a464 | 0x09e3c634 | banlist_pass_bg1_fs_path | load_banlist_pass_input_scene_resources_ptr_bg1_fs_path |
| DWORD_0801a46c | 0x09e3c650 | banlist_pass_bg2_fs_path | load_banlist_pass_input_scene_resources_ptr_bg2_fs_path |

### RENAME_SLOTS (纯改名 + EOL)

| 槽 | slot_label | eol_ascii_or_none |
|---|---|---|
| DAT_08019b24 | encode_pass_table_entry_to_line_buf_pass_buf_off_661 | none |
| DAT_08019c24 | encode_pass_char_obj_rows_pair_str_id_a | none |
| DAT_08019c38 | encode_pass_char_obj_rows_pair_pass_buf_off_675 | none |
| DAT_08019c3c | encode_pass_char_obj_rows_pair_str_id_b | none |
| DAT_08019c40 | encode_pass_char_obj_rows_pair_pass_buf_off_674 | none |
| DWORD_08019c80 | load_banlist_password_table_from_rom_max_entries | none |
| DWORD_08019c8c | load_banlist_password_table_from_rom_byte_guard | none |
| DWORD_08019d9c | init_banlist_pass_input_bg0_page_cpuset_screen | none |
| DWORD_08019da0 | init_banlist_pass_input_bg0_page_cpuset_char | none |
| DWORD_08019ec8 | init_banlist_pass_input_bg2_page_cpuset_screen | none |
| DWORD_08019ecc | init_banlist_pass_input_bg2_page_pass_buf_off_664 | none |
| DWORD_08019ed0 | init_banlist_pass_input_bg2_page_pass_buf_off_66e | none |
| DWORD_0801a010 | tick_banlist_scroll_input_handler_scrollbar_off | none |
| DWORD_0801a064 | tick_banlist_scroll_input_handler_char_step_off_a | none |
| DWORD_0801a094 | tick_banlist_scroll_input_handler_char_step_off_b | none |
| DWORD_0801a0b0 | tick_banlist_scroll_input_handler_char_step_off_c | none |
| DWORD_0801a114 | tick_banlist_scroll_input_handler_char_step_off_d | none |
| DWORD_0801a150 | tick_banlist_scroll_input_handler_char_step_off_e | none |
| DWORD_0801a168 | get_banlist_scroll_direction_scroll_dir_off | none |
| DWORD_0801a1a0 | set_banlist_scroll_step_assert_line_2cd | none |
| DWORD_0801a1a8 | set_banlist_scroll_step_step_field_off | none |
| DWORD_0801a1e8 | tick_banlist_bg_scroll_step_scroll_step_off | none |
| DWORD_0801a1ec | tick_banlist_bg_scroll_step_scroll_dir_off | none |
| DWORD_0801a308 | render_banlist_title_text_to_bg_str_id | none |
| DWORD_0801a31c | render_banlist_title_text_to_bg_char_vram_addr | none |
| DWORD_0801a45c | load_banlist_pass_input_scene_resources_obj_anim_off_a | none |
| DWORD_0801a460 | load_banlist_pass_input_scene_resources_obj_anim_off_b | none |
| DWORD_0801a468 | load_banlist_pass_input_scene_resources_clr_mask | none |
| DWORD_0801a474 | load_banlist_pass_input_scene_resources_bg_palette_slot1 | none |
| DWORD_0801a47c | load_banlist_pass_input_scene_resources_obj_palette_slot1 | none |
| DWORD_0801a480 | load_banlist_pass_input_scene_resources_obj_palette_fill_dst | none |
| DAT_0801a4ec | tick_banlist_card_slot_anim_oam_sprite_ptr_off_a | none |
| DAT_0801a4f4 | tick_banlist_card_slot_anim_oam_assert_line_36f | none |
| DAT_0801a4fc | tick_banlist_card_slot_anim_oam_sprite_ptr_off_b | none |
| DAT_0801a5ec | setup_banlist_sprite_oam_row_batch_attr2_charname_mask | none |
| DAT_0801a5f0 | setup_banlist_sprite_oam_row_batch_attr2_charname_clear | none |
| DAT_0801a5f4 | setup_banlist_sprite_oam_row_batch_wide_sprite_mode | none |
| DAT_0801a688 | setup_banlist_sprite_oam_row_batch_attr1_x_mask | none |
| DAT_0801a68c | setup_banlist_sprite_oam_row_batch_attr1_x_clear | none |
| DAT_0801a710 | zero_obj_tile_vram_range_obj_tile_vram_base | none |
| DAT_0801a714 | zero_obj_tile_vram_range_word_count_mask | none |
| DAT_0801a748 | init_banlist_scrollbar_oam_entry_scrollbar_off | none |
| DAT_0801a76c | advance_banlist_scrollbar_pos_page_scrollbar_off | none |
| DAT_0801a790 | retreat_banlist_scrollbar_pos_page_scrollbar_off | none |
| DAT_0801a838 | advance_banlist_password_cursor_slot_dir_field_off | none |
| DAT_0801a898 | retreat_banlist_password_cursor_slot_dir_field_off | none |
| DWORD_0801a94c | get_banlist_scroll_pixel_offset_scrollbar_off | none |
| DWORD_0801a980 | get_banlist_password_entry_ptr_cursor_hw_off | none |
| DWORD_0801a9f0 | render_banlist_text_col_cleared_font_scale_off | none |
| DWORD_0801aa18 | render_banlist_pw_chars_to_buf_scroll_hw_off | none |
| DWORD_0801aa1c | render_banlist_pw_chars_to_buf_step_byte_off | none |
| DWORD_0801aa74 | advance_banlist_pw_char_and_render_sp_adj_neg | none |
| DWORD_0801aa7c | advance_banlist_pw_char_and_render_pw_cur_off | none |
| DWORD_0801aa80 | advance_banlist_pw_char_and_render_pw_max_off | none |
| DWORD_0801aaf8 | advance_banlist_pw_char_and_render_scroll_hw_off | none |
| DWORD_0801aafc | advance_banlist_pw_char_and_render_step_byte_off | none |
| DWORD_0801aba8 | retreat_banlist_pw_char_and_render_scroll_hw_off | none |
| DWORD_0801abac | retreat_banlist_pw_char_and_render_pw_cur_off | none |
| DWORD_0801abd8 | retreat_banlist_pw_char_and_render_pw_cur_off_b | none |
| DWORD_0801a910 | load_banlist_char_by_cursor_slot_ewram_base | none |
| DWORD_0801a914 | load_banlist_char_by_cursor_slot_gsettings_offset | none |
| DWORD_0801a90c | load_banlist_char_by_cursor_slot_pass_buf_off_661 | none |

### FUNC_RENAME (误名订正)

None detected. All 28 functions have plates whose verb+object match the implementation:
- encode_pass_table_entry_to_line_buf: reads pass table entry, encodes to line buf. Consistent.
- reject_banlist_input_event: always returns 0 (reject). Consistent.
- load_banlist_password_table_from_rom: reads ROM_PASSWORD_TABLE into gBanlistPasswordBuffer. Consistent.
- All others verified by plate+body cross-check.

### PLATE (R5, ASCII)

Three functions have CJK in their plate comments; all are BEYOND Seg-8 boundary (advance_banlist_password_char_and_render at 0x0801aa54, retreat_banlist_password_char_and_render at 0x0801ab00, tick_banlist_password_backspace_input at 0x0801abec). These are Seg-9 territory -- NOT in Seg-8 scope.

Within Seg-8 (0x08019a58..0x0801a794): all plates are already ASCII. No R5 plate rewrites needed for CJK compliance.

---

## carve 计划 (R7)

### 主 carve: name_input_default_name host 切分

**Host**: rom.s line 1087: `name_input_default_name: .incbin "roms/2343.gba", 0x1E3B4A8, 0x10DC`

**Split**:
```gas
name_input_default_name:               @ 0x09e3b4a8 (SJIS "tesuto" default commit name; dispatch_name_input_confirm_state src)
    .incbin "roms/2343.gba", 0x1E3B4A8, 0x809   @ 0x09e3b4a8..0x09e3bcb1 (pre-str gap)
banlist_char_candidate_str:            @ 0x09e3bcb1 (90 SJIS pairs + null pair; encode_pass_table_entry_to_line_buf + load_banlist_char_by_cursor_slot)
    .incbin "roms/2343.gba", 0x1E3BCB1, 0xB6    @ 182B
    .incbin "roms/2343.gba", 0x1E3BD67, 0xD5    @ 0x09e3bd67..0x09e3be3c (char group gap a)
banlist_pass_ext_char_group:           @ 0x09e3be3c (SJIS ext char group; retreat_banlist_pw_char_and_render + banlist ext ptr table refs x4)
    .incbin "roms/2343.gba", 0x1E3BE3C, 0x1A1   @ 0x09e3be3c..0x09e3bfdd (char group gap b)
banlist_pass_char_str:                 @ 0x09e3bfdd (96B SJIS + null + 2B pad; encode_pass_table_entry_to_line_buf)
    .incbin "roms/2343.gba", 0x1E3BFDD, 0x63    @ 99B
banlist_pass_alt_char:                 @ 0x09e3c040 (SJIS full-width space 0x8140 + null; encode_pass_table_entry_to_line_buf + load_banlist_char_by_cursor_slot alt path)
    .incbin "roms/2343.gba", 0x1E3C040, 0x4     @ 4B: 81 40 00 00
rom_password_table:                    @ 0x09e3c044 (671 x 2B LE SJIS halfwords; load_banlist_password_table_from_rom)
    .incbin "roms/2343.gba", 0x1E3C044, 0x53E   @ 671*2 = 1342B
    .incbin "roms/2343.gba", 0x1E3C582, 0x2     @ 2B trailing pad to host end
```
Coverage: 0x809+0xD5+0x1A1+0x63+0x4+0x53E+0xB6+0x2 = 0x10DC. OK.

### 副 carve: assert_dir... host 切分

**Host**: rom.s line 1093: `.incbin "roms/2343.gba", 0x1E3C5B2, 0xBE`

**Split**:
```gas
    .incbin "roms/2343.gba", 0x1E3C5B2, 0x2      @ 2B pre-pad
banlist_pass_obj_ncer_path:            @ 0x09e3c5b4
    .incbin "roms/2343.gba", 0x1E3C5B4, 0x1C     @ "pass_input/pass_o_01.LZncer\0" (28B)
banlist_pass_obj_nanr_path:            @ 0x09e3c5d0
    .incbin "roms/2343.gba", 0x1E3C5D0, 0x1C     @ "pass_input/pass_o_01.LZnanr\0" (28B)
banlist_pass_obj_ncgr_path:            @ 0x09e3c5ec
    .incbin "roms/2343.gba", 0x1E3C5EC, 0x1C     @ "pass_input/pass_o_01.LZncgr\0" (28B)
banlist_pass_obj_nclr_path:            @ 0x09e3c608
    .incbin "roms/2343.gba", 0x1E3C608, 0x1C     @ "pass_input/pass_o_01.LZnclr\0" (28B)
banlist_pass_obj_resource_desc:        @ 0x09e3c624 (4-word ptr struct; load_banlist_pass_input_scene_resources)
    .word banlist_pass_obj_ncer_path   @ 0x09e3c624 -> 0x09e3c5b4
    .word banlist_pass_obj_nanr_path   @ 0x09e3c628 -> 0x09e3c5d0
    .word banlist_pass_obj_ncgr_path   @ 0x09e3c62c -> 0x09e3c5ec
    .word banlist_pass_obj_nclr_path   @ 0x09e3c630 -> 0x09e3c608
banlist_pass_bg1_fs_path:             @ 0x09e3c634
    .incbin "roms/2343.gba", 0x1E3C634, 0x1C     @ "pass_input/pass_b_01.LZ5bg\0" + 1B pad (28B)
banlist_pass_bg2_fs_path:             @ 0x09e3c650
    .incbin "roms/2343.gba", 0x1E3C650, 0x1E     @ "pass_input/moziire_b_01.LZ5bg\0" (30B)
```
Coverage: 0x2+0x1C*4+0x10+0x1C+0x1E = 2+112+16+28+30 = 0xBE. OK.

Ptr verification:
- .word banlist_pass_obj_ncer_path -> GAS emits absolute address of label = 0x09e3c5b4. ROM[0x1E3C624] = 0xb4c5e309 (LE 0x09e3c5b4). Match confirmed.
- .word banlist_pass_obj_nanr_path -> 0x09e3c5d0 -> ROM[0x1E3C628] = 0xd0c5e309. Match.
- .word banlist_pass_obj_ncgr_path -> 0x09e3c5ec -> ROM[0x1E3C62c] = 0xecc5e309. Match.
- .word banlist_pass_obj_nclr_path -> 0x09e3c608 -> ROM[0x1E3C630] = 0x08c6e309. Match.

All 4 confirmed byte-identical.

---

## disasm 计划 (R4)

**Range**: 0x0801ad18..0x0801ae04 THUMB (236B = 0xec).

**Context**: dispatch_banlist_cursor_action (0x0801acac) jump table at 0x0801ad00 stores 6 raw handler addresses (used via `MOV PC, R0` = opcode 0x4687, THUMB ISA preserved). 5 live handler entries + 1 fallthrough to LAB_0801ae04.

**Handler stubs** (each needs DisassembleCommand individually):
| Stub start | Role |
|---|---|
| 0x0801ad18 | advance_banlist_char_input_handler stub |
| 0x0801ad20 | cursor_grid_init_handler stub |
| 0x0801ad4c | cursor_page_scroll_a_handler stub |
| 0x0801ad94 | cursor_select_char_handler stub |
| 0x0801ade0 | cursor_ext_grid_handler stub |

**Ghidra procedure**:
1. clearListing(0x0801ad18, 0x0801ae04)
2. setTMode(0x0801ad18, THUMB=1) for each stub start address
3. DisassembleCommand per stub (single-instruction granularity for each of the 5 addrs above)
4. createFunction at each stub addr if needed
5. After disasm, update rom.s via ghidra-export-range

**Literal pool within block**: slots at 0x0801ad40, 0x0801ad60(?), 0x0801ad68(?), 0x0801ad80, 0x0801adbc, 0x0801addc, 0x0801adfc. These will become named slots after disasm; key values: 0x0000064c (gBanlistPwBuf scrollbar off), 0x03000040 (gPrng).

---

## 新增 constants / 全局

None new. All referenced constants already exist in ewram.inc / gba_mem.inc / name_input.inc / oam_attr.inc / iwram.inc. No new .inc file needed.

Carve labels added to rom.s are NOT constants (they are ROM data labels, not EWRAM/IO equates).

---

## §5.1 登记 (Rule 3) -- 0 引用块

| 块 | ROM 地址 | size | ref-scan 结果 | 登记原因 |
|---|---|---|---|---|
| ROM_INCBIN A | 0x0801a89c | 0x20 | raw=1 (compressed FS coincidence), thumb=0 | 0 code refs; sits between literal pool slots; not a Ghidra function |

---

## 消费者证据 (R6)

| 槽/常量 | 消费者 | file:line | 置信度 |
|---|---|---|---|
| banlist_char_candidate_str (0x09e3bcb1) | init_banlist_pass_input_bg0_page (DWORD_08019d98), load_banlist_char_by_cursor_slot (DWORD_0801a908) | asm/00_system_str_vija.s:14218, 15835 | high |
| banlist_pass_char_str (0x09e3bfdd) | encode_pass_table_entry_to_line_buf via base+index into SJIS char pairs | asm/00_system_str_vija.s:13872 | high |
| banlist_pass_alt_char (0x09e3c040) | encode_pass_table_entry_to_line_buf + load_banlist_char_by_cursor_slot alternate-path branch | asm/00_system_str_vija.s:13874, 15843 | high |
| rom_password_table (0x09e3c044) | load_banlist_password_table_from_rom: DWORD_08019c88 | asm/00_system_str_vija.s:14063 | high |
| banlist_pass_ext_char_group (0x09e3be3c) | retreat_banlist_pw_char_and_render: DWORD_0801abb0 passed to advance_text_ptr_by_charlen | asm/00_system_str_vija.s:16207 | high |
| banlist_pass_obj_resource_desc (0x09e3c624) | load_banlist_pass_input_scene_resources: ldmia r0! (4 words copied to stack struct) | asm/00_system_str_vija.s:15015 | high |
| banlist_pass_bg1_fs_path (0x09e3c634) | load_banlist_pass_input_scene_resources: ldr r0, DWORD_0801a464; bl fs_load | asm/00_system_str_vija.s:15044 | high |
| banlist_pass_bg2_fs_path (0x09e3c650) | load_banlist_pass_input_scene_resources: ldr r0, DWORD_0801a46c; bl fs_load | asm/00_system_str_vija.s:15079 | high |
| name_o_palette_data (0x09ccd290) | load_banlist_pass_input_scene_resources: 2x bios_cpu_set(src=name_o_palette_data, dst=BG/OBJ palette slot 1) | asm/00_system_str_vija.s:15155 | high; already named in Seg-6b |
| OAM_ATTR2_CHARNAME_MASK (0x3ff) | setup_banlist_sprite_oam_row_batch: keeps attr2[9:0]=tile index before palette-slot insertion | asm/00_system_str_vija.s:15369 | high |
| OAM_ATTR1_X_MASK (0x1ff) | setup_banlist_sprite_oam_row_batch: keeps attr1[8:0]=X coord | asm/00_system_str_vija.s:15452 | high |
| DWORD_0801aa74=0xfffffa58 | advance_banlist_pw_char_and_render: `add sp,r4` (negative = sub sp,#0x5a8 large local frame for 0xb5*8 bytes) | asm/00_system_str_vija.s:16041 | high |

---

## 求助

None. All slots statically determinable; no BLOCKED items.
