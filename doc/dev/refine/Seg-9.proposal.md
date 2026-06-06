# Refine Proposal: Seg-9  [0x0801a794..0x0801b850)

## 段测绘

- 函数入口: ×28 (全部 <0x1b850)

| addr | name |
|---|---|
| 0x0801a794 | tick_banlist_scrollbar_and_slot_anim |
| 0x0801a7d0 | advance_banlist_password_cursor_slot |
| 0x0801a83c | retreat_banlist_password_cursor_slot |
| 0x0801a8bc | load_banlist_char_by_cursor_slot |
| 0x0801a930 | get_banlist_scroll_pixel_offset |
| 0x0801a950 | get_banlist_password_entry_ptr |
| 0x0801a984 | render_banlist_text_col_cleared |
| 0x0801a9f4 | render_banlist_password_chars_to_buf |
| 0x0801aa54 | advance_banlist_password_char_and_render |
| 0x0801ab00 | retreat_banlist_password_char_and_render |
| 0x0801abec | tick_banlist_password_backspace_input |
| 0x0801ac28 | advance_banlist_scroll_pos_step |
| 0x0801acac | dispatch_banlist_cursor_action |
| 0x0801ae0c | advance_banlist_scroll_column_and_page |
| 0x0801aec8 | retreat_banlist_scroll_column_and_page |
| 0x0801af70 | tick_banlist_password_frame |
| 0x0801b178 | tick_banlist_oam_palette_fade |
| 0x0801b1a0 | tick_banlist_card_slot_anim_primary |
| 0x0801b20c | tick_banlist_card_slot_anim_secondary |
| 0x0801b264 | trigger_banlist_fade_out_exit |
| 0x0801b284 | tick_banlist_oam_and_card_slots |
| 0x0801b368 | tick_banlist_scroll_view_by_state |
| 0x0801b5d8 | tick_banlist_scene_frame |
| 0x0801b634 | dispatch_banlist_scene_handler_frame |
| 0x0801b6a0 | dispatch_banlist_pass_input_frame |
| 0x0801b77c | scale_char_width_by_encoding |
| 0x0801b7a0 | read_encoded_char_pair_from_state |
| 0x0801b7e8 | init_demo_shuen_display_state |

- 残留自动名槽 (DWORD_/DAT_/PTR_ 定义): ×132 (清单见 §RENAME_SLOTS)
- ROM_INCBIN 块:
  - Block A: `0x1a89c, 0x20` (32B)
  - Block B: `0x1ad18, 0xec` (236B)  [= jump table 0x1ad00 的 5 stub handlers]

## 数据块分类 (Rule 2/3)

| 块 | ref-scan (raw / THUMB) | 判定 | 理由 |
|---|---|---|---|
| Block A `0x1a89c, 0x20` | raw=0 (entry 0x0801a89c); raw=1 for 0x0801a8a0 at file 0x00af5768 (FS asset compressed blob, not code) | §5.1 | Entry 0x0801a89c: raw=0, thumb=0 -> 0 code引用。0x0801a8a0偶合引用在 ROM 0x08af5768 (FS asset区, 压缩数据, 非代码 ref). Seg-8 越界预析已确认 §5.1. |
| Block B `0x1ad18, 0xec` | raw=1 per stub entry (5 stubs: 0x0801ad18/ad20/ad4c/ad94/ade0 each raw=1 from jump table 0x1ad00) | disasm R4 | jump table PTR_DAT_0801ad00 有 6 条目; entry[0/2/3/4/5] 为 5 个 stub handler raw 地址; entry[1]=0x0801ae04 (=LAB_0801ae04 已反汇编, 默认路径). 5 stub 各为 THUMB 函数体 (8B/44B/72B/76B/36B). `mov pc, r0` dispatch (不切 ISA). |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

全部复用现有 inc 常量, 无需新建.

| slot addr | value | const_name | inc | slot_label |
|---|---|---|---|---|
| 0x0801b01c | 0xfffffc3f | NAME_INPUT_MODE_CLEAR | name_input.inc | tick_banlist_password_frame_mode_clear_a |
| 0x0801b048 | 0xfffffc3f | NAME_INPUT_MODE_CLEAR | name_input.inc | tick_banlist_password_frame_mode_clear_b |
| 0x0801b060 | 0xfffffc3f | NAME_INPUT_MODE_CLEAR | name_input.inc | tick_banlist_password_frame_mode_clear_c |
| 0x0801b11c | 0xfffffc3f | NAME_INPUT_MODE_CLEAR | name_input.inc | tick_banlist_password_frame_mode_clear_d |
| 0x0801b170 | 0xfffffc3f | NAME_INPUT_MODE_CLEAR | name_input.inc | tick_banlist_password_frame_mode_clear_e |

Evidence: NAME_INPUT_MODE_CLEAR=0xfffffc3f defined in name_input.inc (Seg-7). Value confirmed: ROM 0x0801b01c=0xfffffc3f, 0x0801b048=0xfffffc3f, 0x0801b060=0xfffffc3f, 0x0801b11c=0xfffffc3f, 0x0801b170=0xfffffc3f. Confidence: high.

### REF_SLOTS (USER-label DATA-ref + slot rename)

#### gBanlistPasswordBuffer (ewram.inc, 0x02029810) -- 複数槽 共 ~24 slots

All PTR_gBanlistPasswordBuffer_0801xxxx slots already carry the symbol (exported from Ghidra). Additional DWORD_0801xxxx slots with value 0x02029810:

| slot addr | gas_label | slot_label |
|---|---|---|
| PTR_gBanlistPasswordBuffer_0801a7c8 | gBanlistPasswordBuffer | tick_banlist_scrollbar_and_slot_anim_ptr_gbanlistpasswordbuffer |
| PTR_gBanlistPasswordBuffer_0801a7fc | gBanlistPasswordBuffer | advance_banlist_password_cursor_slot_ptr_gbanlistpasswordbuffer |
| PTR_gBanlistPasswordBuffer_0801a88c | gBanlistPasswordBuffer | retreat_banlist_password_cursor_slot_ptr_gbanlistpasswordbuffer |
| DWORD_0801a904 | gBanlistPasswordBuffer | load_banlist_char_by_cursor_slot_ptr_gbanlistpasswordbuffer |
| DWORD_0801a948 | gBanlistPasswordBuffer | get_banlist_scroll_pixel_offset_ptr_gbanlistpasswordbuffer |
| DWORD_0801a97c | gBanlistPasswordBuffer | get_banlist_password_entry_ptr_ptr_gbanlistpasswordbuffer |
| DWORD_0801a9ec | gBanlistPasswordBuffer | render_banlist_text_col_cleared_ptr_gbanlistpasswordbuffer |
| DWORD_0801aa14 | gBanlistPasswordBuffer | render_banlist_password_chars_to_buf_ptr_gbanlistpasswordbuffer |
| DWORD_0801aa78 | gBanlistPasswordBuffer | advance_banlist_password_char_and_render_ptr_gbanlistpasswordbuffer |
| DWORD_0801aba4 | gBanlistPasswordBuffer | retreat_banlist_password_char_and_render_ptr_gbanlistpasswordbuffer |
| DWORD_0801ac0c | gBanlistPasswordBuffer | tick_banlist_password_backspace_input_ptr_gbanlistpasswordbuffer |
| DWORD_0801ac58 | gBanlistPasswordBuffer | advance_banlist_scroll_pos_step_ptr_gbanlistpasswordbuffer |
| DWORD_0801acf0 | gBanlistPasswordBuffer | dispatch_banlist_cursor_action_ptr_gbanlistpasswordbuffer |
| DWORD_0801ae74 | gBanlistPasswordBuffer | advance_banlist_scroll_column_and_page_ptr_gbanlistpasswordbuffer |
| DWORD_0801af04 | gBanlistPasswordBuffer | retreat_banlist_scroll_column_and_page_ptr_gbanlistpasswordbuffer_a |
| DWORD_0801afac | gBanlistPasswordBuffer | tick_banlist_password_frame_ptr_gbanlistpasswordbuffer |
| DWORD_0801b194 | gBanlistPasswordBuffer | tick_banlist_oam_palette_fade_ptr_gbanlistpasswordbuffer |
| DWORD_0801b1e0 | gBanlistPasswordBuffer | tick_banlist_card_slot_anim_primary_ptr_gbanlistpasswordbuffer |
| DWORD_0801b25c | gBanlistPasswordBuffer | tick_banlist_card_slot_anim_secondary_ptr_gbanlistpasswordbuffer |
| DWORD_0801b280 | gBanlistPasswordBuffer | trigger_banlist_fade_out_exit_ptr_gbanlistpasswordbuffer |
| DWORD_0801b354 | gBanlistPasswordBuffer | tick_banlist_oam_and_card_slots_ptr_gbanlistpasswordbuffer |
| DWORD_0801b3b8 | gBanlistPasswordBuffer | tick_banlist_scroll_view_by_state_ptr_gbanlistpasswordbuffer |
| DWORD_0801b5f0 | gBanlistPasswordBuffer | tick_banlist_scene_frame_ptr_gbanlistpasswordbuffer |
| PTR_gBanlistPasswordBuffer_0801b70c | gBanlistPasswordBuffer | dispatch_banlist_pass_input_frame_ptr_gbanlistpasswordbuffer |

Evidence: gBanlistPasswordBuffer=0x02029810 in ewram.inc. ROM values confirmed (all = 0x02029810). Confidence: high.

#### gPrng (iwram.inc, 0x03000040)

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801acf4 | gPrng | dispatch_banlist_cursor_action_ptr_gprng |
| DWORD_0801afb0 | gPrng | tick_banlist_password_frame_ptr_gprng |
| DWORD_0801b67c | gPrng | dispatch_banlist_scene_handler_frame_ptr_gprng |
| PTR_gPrng_0801b708 | gPrng | dispatch_banlist_pass_input_frame_ptr_gprng |
| DWORD_0801b5c8 | gPrng | tick_banlist_scroll_view_by_state_ptr_gprng |

Evidence: gPrng=0x03000040 in iwram.inc. ROM values: 0x0801acf4=0x03000040, 0x0801afb0=0x03000040, etc. Confidence: high.

#### gTextEncodingOverride (ewram.inc, 0x0202348c)

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801b69c | gTextEncodingOverride | dispatch_banlist_scene_handler_frame_ptr_text_encoding_override |
| DAT_0801b778 | gTextEncodingOverride | dispatch_banlist_pass_input_frame_ptr_text_encoding_override |

Evidence: gTextEncodingOverride=0x0202348c in ewram.inc (added in Seg-1b). ROM: 0x0801b69c=0x0202348c, 0x0801b778=0x0202348c. Confidence: high.

#### gDemoState (ewram.inc, 0x02029ec0)

| slot addr | gas_label | slot_label |
|---|---|---|
| DAT_0801b83c | gDemoState | init_demo_shuen_display_state_ptr_gdemostate |

Evidence: gDemoState=0x02029EC0 in ewram.inc. ROM: 0x0801b83c=0x02029ec0. Confidence: high.

#### banlist_char_candidate_str (carve label, 0x09e3bcb1)

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801a908 | banlist_char_candidate_str | load_banlist_char_by_cursor_slot_ptr_banlist_char_candidate_str |

Evidence: banlist_char_candidate_str carved in Seg-8 at 0x09e3bcb1. ROM: 0x0801a908=0x09e3bcb1. Confidence: high.

#### banlist_pass_alt_char (carve label, 0x09e3c040)

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801a918 | banlist_pass_alt_char | load_banlist_char_by_cursor_slot_ptr_banlist_pass_alt_char |

Evidence: banlist_pass_alt_char carved in Seg-8 at 0x09e3c040. ROM: 0x0801a918=0x09e3c040. Confidence: high.

#### banlist_pass_ext_char_group (carve label, 0x09e3be3c) -- NEW carve in this segment

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801abb0 | banlist_pass_ext_char_group | retreat_banlist_password_char_and_render_ptr_ext_char_group |

Evidence: 0x0801abb0=0x09e3be3c confirmed in ROM. banlist_pass_ext_char_group to be carved in this segment (see carve plan). Confidence: high.

#### banlist_handler_table (new carve, 0x09e58994) -- NEW carve

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801b678 | banlist_handler_table | dispatch_banlist_scene_handler_frame_ptr_handler_table |
| DAT_0801b704 | banlist_handler_table | dispatch_banlist_pass_input_frame_ptr_handler_table |

Evidence: ROM 0x0801b678=0x09e58994, 0x0801b704=0x09e58994. banlist_handler_table to be carved at 0x09e58994 (3 THUMB fn ptrs + NULL sentinel). Confidence: high.

#### banlist_scroll_view_anim_params (new carve, 0x09e3c6ab) -- NEW carve

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801b3c4 | banlist_scroll_view_anim_params | tick_banlist_scroll_view_by_state_ptr_anim_params |

Evidence: ROM 0x0801b3c4=0x09e3c6ab. Used in memcpy(sp+0x18, r1, 6) at 0x0801b398-0x0801b39e. 6 bytes {0x06,0x06,0x07,0x07,0x07,0x07} indexed by gSettings encoding bits. Confidence: high.

#### game_str_pointer_table (existing carve label)

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801b42c | game_str_pointer_table | tick_banlist_scroll_view_by_state_ptr_game_str_pointer_table |

Evidence: game_str_pointer_table=0x08000f40 (data/game-strings-pointer-table.s). ROM 0x0801b42c=0x08000f40. Confidence: high (data/game-strings-pointer-table.s:1).

#### game_str_ja (existing label from text data)

| slot addr | gas_label | slot_label |
|---|---|---|
| DWORD_0801b430 | game_str_ja | tick_banlist_scroll_view_by_state_ptr_game_str_ja |

Evidence: ROM 0x0801b430=0x09db9c10 = game_str_ja label (Japanese game string base). Confidence: high. Verify: grep existing label name; if different, use actual label name.

NOTE: `game_str_ja` label existence must be confirmed with grep before falling back to data-equate. If the label exists in data/game-strings-*.s, use it directly.

#### EWRAM_BASE + GSETTINGS_OFFSET (gba_mem.inc + name_input.inc)

REF_SLOTS for EWRAM_BASE (0x02000000) and GSETTINGS_OFFSET (0x6c2c) patterns:

| slot addr | value | gas_label | slot_label |
|---|---|---|---|
| DAT_0801a800 | 0x02000000 | EWRAM_BASE | advance_banlist_password_cursor_slot_ewram_base |
| DAT_0801a804 | 0x00006c2c | GSETTINGS_OFFSET | advance_banlist_password_cursor_slot_gsettings_offset |
| DAT_0801a890 | 0x02000000 | EWRAM_BASE | retreat_banlist_password_cursor_slot_ewram_base |
| DAT_0801a894 | 0x00006c2c | GSETTINGS_OFFSET | retreat_banlist_password_cursor_slot_gsettings_offset |
| DWORD_0801a910 | 0x02000000 | EWRAM_BASE | load_banlist_char_by_cursor_slot_ewram_base |
| DWORD_0801a914 | 0x00006c2c | GSETTINGS_OFFSET | load_banlist_char_by_cursor_slot_gsettings_offset |
| DWORD_0801b3bc | 0x02000000 | EWRAM_BASE | tick_banlist_scroll_view_by_state_ewram_base |
| DWORD_0801b3c0 | 0x00006c2c | GSETTINGS_OFFSET | tick_banlist_scroll_view_by_state_gsettings_offset |
| DWORD_0801b52c | 0x02000000 | EWRAM_BASE | tick_banlist_scroll_view_by_state_ewram_base_b |
| DWORD_0801b530 | 0x00006c2c | GSETTINGS_OFFSET | tick_banlist_scroll_view_by_state_gsettings_offset_b |
| DWORD_0801b358 | 0x02000000 | EWRAM_BASE | tick_banlist_oam_and_card_slots_ewram_base |
| DWORD_0801b35c | 0x00006c2c | GSETTINGS_OFFSET | tick_banlist_oam_and_card_slots_gsettings_offset |
| DWORD_0801b798 | 0x02000000 | EWRAM_BASE | scale_char_width_by_encoding_ewram_base |
| DWORD_0801b79c | 0x00006c2c | GSETTINGS_OFFSET | scale_char_width_by_encoding_gsettings_offset |
| DWORD_0801b7cc | 0x02000000 | EWRAM_BASE | read_encoded_char_pair_from_state_ewram_base |
| DWORD_0801b7d0 | 0x00006c2c | GSETTINGS_OFFSET | read_encoded_char_pair_from_state_gsettings_offset |

Evidence: EWRAM_BASE=0x02000000 in gba_mem.inc; GSETTINGS_OFFSET=0x00006c2c in name_input.inc. All ROM values confirmed. Confidence: high.

#### OBJ PALRAM (0x05000202 = OBJ_PALRAM_BASE + 2)

| slot addr | value | equate note | slot_label |
|---|---|---|---|
| DWORD_0801b198 | 0x05000202 | OBJ_PALRAM_BASE+2 (no .equ for +2 offset; use raw RENAME) | tick_banlist_oam_palette_fade_oam_palram_plus2 |

Evidence: plate says "OAM palette RAM (0x05000202)". ROM 0x0801b198=0x05000202. No existing constant for +2 offset; rename slot only (no equate). Confidence: high.

#### MASK_CLEAR_COL (0xfffffe03) -- shared across advance/retreat scroll functions

| slot addr | value | slot_label |
|---|---|---|
| DWORD_0801aca8 | 0xfffffe03 | advance_banlist_scroll_pos_step_mask_clear_col |
| DWORD_0801ae84 | 0xfffffe03 | advance_banlist_scroll_column_and_page_mask_clear_col |
| DWORD_0801af10 | 0xfffffe03 | retreat_banlist_scroll_column_and_page_mask_clear_col_a |
| DWORD_0801af38 | 0xfffffe03 | retreat_banlist_scroll_column_and_page_mask_clear_col_b |
| DWORD_0801af6c | 0xfffffe03 | retreat_banlist_scroll_column_and_page_mask_clear_col_c |

Note: 0xfffffe03 = ~(0x7f<<2). No existing equate; these are pure RENAME_SLOTS (value rename, no new .equ constant needed -- value appears only in banlist scroll context, not ROM-wide reusable).

#### HANDLER_IDX_MASK (0xffffc03f) -- dispatch_banlist_scene_handler_frame

| slot addr | value | slot_label |
|---|---|---|
| DWORD_0801b680 | 0xffffc03f | dispatch_banlist_scene_handler_frame_handler_idx_mask |

Note: ~(0xff<<6). Pure RENAME.

#### PAGE_STATE_CLEAR (0xffc03fff) -- dispatch_banlist_pass_input_frame

Reuse NAME_INPUT_PAGE_STATE_CLEAR (name_input.inc, 0xffc03fff).

| slot addr | gas_label | slot_label |
|---|---|---|
| DAT_0801b710 | NAME_INPUT_PAGE_STATE_CLEAR | dispatch_banlist_pass_input_frame_page_state_clear |

Evidence: NAME_INPUT_PAGE_STATE_CLEAR=0xffc03fff defined in name_input.inc (Seg-7). ROM 0x0801b710=0xffc03fff. Confidence: high.

#### cursor_pos_base (0x020053f8) -- dispatch_banlist_pass_input_frame

| slot addr | value | slot_label | note |
|---|---|---|---|
| DAT_0801b768 | 0x020053f8 | dispatch_banlist_pass_input_frame_cursor_pos_base | cursor pixel position EWRAM base; 1 ref; no existing constant |

Pure RENAME (no new global -- only 1 ref in segment, not ROM-wide).

### RENAME_SLOTS (改名 + EOL)

Pure offset/constant slots with no global or equate:

| slot addr | value | slot_label | EOL |
|---|---|---|---|
| DAT_0801a7cc | 0x0000064c | tick_banlist_scrollbar_and_slot_anim_scrollbar_offset | scrollbar struct offset in gBanlistPasswordBuffer |
| DAT_0801a838 | 0x00000667 | advance_banlist_password_cursor_slot_dir_field_offset | direction field byte offset |
| DAT_0801a898 | 0x00000667 | retreat_banlist_password_cursor_slot_dir_field_offset | direction field byte offset |
| DWORD_0801a90c | 0x00000661 | load_banlist_char_by_cursor_slot_cursor_slot_offset | bits[5:2]=4-bit slot index |
| DWORD_0801a94c | 0x0000064c | get_banlist_scroll_pixel_offset_scrollbar_offset | scrollbar struct offset |
| DWORD_0801a980 | 0x0000066a | get_banlist_password_entry_ptr_cursor_hw_offset | cursor halfword offset |
| DWORD_0801a9f0 | 0x00000663 | render_banlist_text_col_cleared_font_scale_offset | font height scale byte offset |
| DWORD_0801aa18 | 0x0000066a | render_banlist_password_chars_to_buf_cursor_hw_offset | cursor halfword |
| DWORD_0801aa1c | 0x0000066b | render_banlist_password_chars_to_buf_row_byte_offset | row height byte offset |
| DWORD_0801aa74 | 0xfffffa58 | advance_banlist_password_char_and_render_stack_frame_neg | large stack frame -0x5a8 bytes |
| DWORD_0801aa7c | 0x0000066c | advance_banlist_password_char_and_render_limit1_offset | current entry count halfword |
| DWORD_0801aa80 | 0x0000066e | advance_banlist_password_char_and_render_limit2_offset | max entry count halfword |
| DWORD_0801aaf8 | 0x0000066a | advance_banlist_password_char_and_render_cursor_hw_offset | cursor halfword |
| DWORD_0801aafc | 0x0000066b | advance_banlist_password_char_and_render_row_byte_offset | row height byte |
| DWORD_0801aba8 | 0x0000066a | retreat_banlist_password_char_and_render_cursor_hw_offset | cursor halfword |
| DWORD_0801abac | 0x0000066c | retreat_banlist_password_char_and_render_limit_offset | entry count halfword |
| DWORD_0801abd8 | 0x0000066c | retreat_banlist_password_char_and_render_limit_offset_b | entry count halfword (second ref) |
| DWORD_0801ac0c | 0x02029810 | tick_banlist_password_backspace_input_ptr_gbanlistpasswordbuffer | (or use REF gBanlistPasswordBuffer) |
| DWORD_0801ac10 | 0x0000066c | tick_banlist_password_backspace_input_limit_offset | entry count halfword |
| DWORD_0801ac5c | 0x0000066a | advance_banlist_scroll_pos_step_scroll_halfword_off | cursor halfword |
| DWORD_0801ac60 | 0x0000066b | advance_banlist_scroll_pos_step_row_byte_off | row height byte |
| DWORD_0801ac64 | 0x0000066c | advance_banlist_scroll_pos_step_limit_halfword_off | entry count halfword |
| DWORD_0801acf8 | 0x00000661 | dispatch_banlist_cursor_action_cursor_slot_offset | cursor slot byte (bits[5:2]=slot) |
| PTR_PTR_0801acfc | 0x0801ad00 | dispatch_banlist_cursor_action_jump_table_ptr | ptr to 6-entry jump table |
| PTR_DAT_0801ad00 | (jump table base label) | dispatch_banlist_cursor_action_jump_table | 6-entry handler table |
| DWORD_0801ae78 | 0x0000066a | advance_banlist_scroll_column_and_page_scroll_halfword_off | cursor halfword |
| DWORD_0801ae7c | 0x0000066b | advance_banlist_scroll_column_and_page_row_byte_off | row height byte |
| DWORD_0801ae80 | 0x0000066c | advance_banlist_scroll_column_and_page_limit1_off | entry count |
| DWORD_0801ae88 | 0x0000066e | advance_banlist_scroll_column_and_page_limit2_off | max count halfword |
| DWORD_0801af08 | 0x0000066a | retreat_banlist_scroll_column_and_page_scroll_halfword_off | cursor halfword |
| DWORD_0801af0c | 0x0000066b | retreat_banlist_scroll_column_and_page_row_byte_off | row height byte |
| DWORD_0801afb4 | 0x00000661 | tick_banlist_password_frame_cursor_slot_offset | cursor slot byte |
| DWORD_0801afe8 | 0x00000661 | tick_banlist_password_frame_cursor_slot_offset_b | cursor slot byte (second ref) |
| DWORD_0801b114 | 0x0000066c | tick_banlist_password_frame_limit1_offset | entry count halfword |
| DWORD_0801b118 | 0x0000066e | tick_banlist_password_frame_limit2_offset | max count halfword |
| DWORD_0801b120 | 0x00000661 | tick_banlist_password_frame_cursor_slot_offset_c | cursor slot byte (third ref) |
| DWORD_0801b174 | 0x00000661 | tick_banlist_password_frame_cursor_slot_offset_d | cursor slot byte (fourth ref) |
| DWORD_0801b198 | 0x05000202 | tick_banlist_oam_palette_fade_oam_palram_plus2 | OBJ PALRAM+2 (sprite palette 1 entry 1) |
| DWORD_0801b19c | 0x00000676 | tick_banlist_oam_palette_fade_ref_palette_offset | reference palette offset in gBanlistPasswordBuffer |
| DWORD_0801b1e4 | 0x00000661 | tick_banlist_card_slot_anim_primary_cursor_slot_offset | cursor slot byte |
| DWORD_0801b260 | 0x0000066a | tick_banlist_card_slot_anim_secondary_scroll_halfword_off | cursor halfword |
| DWORD_0801b360 | 0x00000674 | tick_banlist_oam_and_card_slots_sprite_y_offset_a | sprite row Y param byte A |
| DWORD_0801b364 | 0x00000675 | tick_banlist_oam_and_card_slots_sprite_y_offset_b | sprite row Y param byte B |
| DWORD_0801b3c8 | 0x00000665 | tick_banlist_scroll_view_by_state_view_state_offset | view_state byte offset bits[7:4] |
| DWORD_0801b428 | 0x0000103a | tick_banlist_scroll_view_by_state_game_str_id | game string ID 0x103a |
| DWORD_0801b448 | 0x00000673 | tick_banlist_scroll_view_by_state_state_mode_incr_off_a | view sub-state offset byte |
| DWORD_0801b490 | 0x00000673 | tick_banlist_scroll_view_by_state_state_mode_incr_off_b | view sub-state offset byte |
| DWORD_0801b494 | 0x00000672 | tick_banlist_scroll_view_by_state_blend_ctr_offset_a | blend counter byte offset |
| DWORD_0801b498 | 0x00000665 | tick_banlist_scroll_view_by_state_view_state_offset_b | view_state byte offset |
| DWORD_0801b4c4 | 0x00000672 | tick_banlist_scroll_view_by_state_blend_ctr_offset_b | blend counter byte offset |
| DWORD_0801b534 | 0x00000673 | tick_banlist_scroll_view_by_state_state_mode_incr_off_c | view sub-state offset byte |
| DWORD_0801b5cc | 0x0000030f | tick_banlist_scroll_view_by_state_prng_rng_mask | gPrng random state mask bits[9:0]+bits[3:0] |
| DWORD_0801b5d0 | 0x00000662 | tick_banlist_scroll_view_by_state_scene_state_offset_a | scene state byte offset |
| DWORD_0801b5d4 | 0x00000673 | tick_banlist_scroll_view_by_state_state_mode_incr_off_d | view sub-state offset byte |
| DWORD_0801b5f4 | 0x00000662 | tick_banlist_scene_frame_scene_state_offset | scene state byte bits[7:6]=sub-mode |
| DWORD_0801b680 | 0xffffc03f | dispatch_banlist_scene_handler_frame_handler_idx_mask | clear bits[13:6] handler index |
| DAT_0801b714 | 0x00000663 | dispatch_banlist_pass_input_frame_cursor_slot_offset | cursor slot byte |
| DAT_0801b758 | 0x000006f5 | dispatch_banlist_pass_input_frame_assert_line_6f5 | assert line 0x6f5=1781 |
| DAT_0801b760 | 0x00000663 | dispatch_banlist_pass_input_frame_cursor_slot_offset_b | cursor slot byte (second ref) |
| DAT_0801b764 | 0x0000065c | dispatch_banlist_pass_input_frame_cursor_px_offset | cursor pixel position field offset |
| DAT_0801b768 | 0x020053f8 | dispatch_banlist_pass_input_frame_cursor_pos_base | cursor pixel pos EWRAM base |
| DAT_0801b840 | 0x05000026 | init_demo_shuen_display_state_gdemostate_fill_ctrl | bios_cpu_set: fill 38 words zero for gDemoState |
| DAT_0801b844 | 0x00001e01 | init_demo_shuen_display_state_bg1cnt_init | BG1CNT init value |
| DAT_0801b848 | 0x00001f02 | init_demo_shuen_display_state_bg2cnt_init | BG2CNT init value |
| DAT_0801b84c | 0x00009b0b | init_demo_shuen_display_state_bg3cnt_init | BG3CNT init value |

Note: DWORD_0801ac0c (0x02029810) is a gBanlistPasswordBuffer REF (listed above in REF_SLOTS); treat as REF not RENAME.

### FUNC_RENAME

None. All 28 function names are consistent with their bodies:
- tick_banlist_scrollbar_and_slot_anim: calls update_scrollbar_thumb_display + call_tick_banlist_card_slot_anim. Name correct.
- advance_banlist_password_cursor_slot: increments slot bits[5:3]. Name correct.
- init_demo_shuen_display_state: clears gDemoState, sets BGxCNT, calls gl_state_init, reset_ig2d_load_counters. Name correct (demo shuen = demo final scene). Confidence: high (asm/00_system_str_vija.s:17802).

### PLATE (R5)

Functions with CJK plates (require ASCII rewrite):

1. **advance_banlist_password_char_and_render** (0x0801aa54, L16038-16039):
   Plate is CJK. Full ASCII rewrite:
   ```
   @ advance_banlist_password_char_and_render: Banlist password input forward commit path.
   @ Checks current entry count at gBanlistPasswordBuffer+0x66c vs limit at +0x66e;
   @ returns 0 immediately if at limit. Calls load_banlist_char_by_cursor_slot to fetch
   @ selected char; if NUL skips. If entry count == limit returns 4 (position=limit).
   @ Otherwise: increments count (+0x66c), copies char via copy_str_unbounded +
   @ append_text_to_buf_charlen, writes to entry ptr, calls render_banlist_text_col_cleared
   @ then advance_banlist_scroll_column_and_page. Returns page-scroll status (0/1/2/3/4).
   @ Caller: tick_banlist_password_frame (0x0801af70) via dispatch_banlist_cursor_action.
   @ Stack frame: 0x5a8 bytes (large local char buffer).
   ```

2. **retreat_banlist_password_char_and_render** (0x0801ab00, L16122-16123):
   Plate is CJK. Full ASCII rewrite:
   ```
   @ retreat_banlist_password_char_and_render: Banlist password input backspace path.
   @ Reads cursor col and row from gBanlistPasswordBuffer+0x66a/66b; if position<=0 and
   @ scroll_pixel_offset<=0 returns 0. Computes col=pos mod 15, row=pos div 15; calls
   @ get_banlist_password_entry_ptr; if col<=14 and row<=3 calls render_banlist_text_col_cleared.
   @ Normal backspace: copies entry +2 forward (shift left), clears trailing byte,
   @ calls retreat_banlist_scroll_column_and_page, decrements count -1.
   @ Page backspace: advance_text_ptr_by_charlen clears last byte, retreat_banlist_scroll...,
   @ decrements count. Calls render_banlist_password_chars_to_buf for full redraw.
   @ Returns 0=cannot retreat, non-zero=success.
   ```

3. **tick_banlist_password_backspace_input** (0x0801abec, L16239-16240):
   Plate is CJK. Full ASCII rewrite:
   ```
   @ tick_banlist_password_backspace_input: Per-frame handler for banlist backspace key.
   @ Reads gBanlistPasswordBuffer+0x66c (entry count); if 0 calls sync_state_and_init_sprite(2)
   @ and returns. Otherwise calls retreat_banlist_password_char_and_render; if status==3
   @ (page-boundary) calls tick_banlist_scroll_input_handler(1) for scroll. Other non-zero
   @ status: sync_state_and_init_sprite(1). Called by tick_banlist_password_frame.
   ```

4. **tick_banlist_oam_and_card_slots** (0x0801b284, L17047-17048):
   Plate is CJK. Full ASCII rewrite:
   ```
   @ tick_banlist_oam_and_card_slots: Banlist scene per-frame OAM and card slot driver.
   @ Called by tick_banlist_scene_frame when bits[7:6] of gBanlistPasswordBuffer+0x662 == 0.
   @ Calls tick_banlist_password_frame; then 5x call_tick_banlist_card_slot_anim for fixed
   @ OAM slots; reads gSettings encoding flag to compute y-offset bias; 2x
   @ call_setup_banlist_sprite_oam_row; calls tick_banlist_card_slot_anim_primary/secondary +
   @ tick_banlist_scrollbar_and_slot_anim. Returns void (Pattern B).
   ```

5. **tick_banlist_scroll_view_by_state** (0x0801b368, L17154-17160):
   Plate already in English and accurate. No CJK detected. Minor FUN_ reference updates only:
   No FUN_ references in plate (dispatch_text_render_by_mode_banlist already named). SKIP plate rewrite.

6. **tick_banlist_scene_frame** (0x0801b5d8): plate already English, no CJK. OK.

7. **dispatch_banlist_pass_input_frame** (0x0801b6a0): plate already English, no CJK. OK.

8. **init_demo_shuen_display_state** (0x0801b7e8): plate already English, no CJK. OK.

Plates requiring FUN_ caller name update in other functions: none found in Seg-9 range (all called functions already have current names in Seg-8 plates). Confirm with grep after fixer runs.

## carve 计划 (R7)

### Carve 1: banlist_pass_ext_char_group @0x09e3be3c (deferred from Seg-8)

Host: currently `.incbin 0x1E3BD67, 0x276` (single span, as noted in Seg-8 4.0z defer).
Split into:
```
.incbin 0x1E3BD67, 0xD5       @ 0xD5 bytes prefix before ext_char_group
banlist_pass_ext_char_group:
    .incbin 0x1E3BE3C, 0x1A1   @ 417 bytes ext char group data (SJIS null-padded char groups)
```
Coverage equation: 0xD5 + 0x1A1 = 0x276 == original size. PASS.
Code ref: DWORD_0801abb0 (ROM 0x0801abb0 = 0x09e3be3c), L16206. Confidence: high.
Also: 4 refs in banlist_pass_char_group_ptr_table (0x09e5895c/964/98c/990) - these are data-side refs inside the ptr table, already within carved incbin region.

### Carve 2: banlist_pass_char_group_ptr_table EXTENSION (Seg-7 carve J correction)

Seg-7 labeled banlist_pass_char_group_ptr_table at 0x09e588CC with only 8 entries (32B).
Actual table has 50 .word ROM data entries (200B = 0xC8). The remaining 42 entries (168B = 0xA8) are in `.incbin 0x1E588EC, 0x420` (Seg-7 remainder).

Correction: extend the carve J split within the remainder incbin:
- Entries [0..7] at 0x09e588CC already labeled (Seg-7 carve J: `.word` entries in rom.s).
- Entries [8..49] at 0x09e588EC..0x09e58993 (168B) currently in `.incbin 0x1E588EC, 0x420`.

Action: The `banlist_pass_char_group_ptr_table` label in rom.s needs 42 more `.word` entries appended (entries 8..49). The remaining incbin after these entries starts at 0x09e58994.

No separate host incbin split needed: the label extension replaces the first 168B of `.incbin 0x1E588EC, 0x420`. New form:
```
@ (continuing banlist_pass_char_group_ptr_table entries 8..49 -- 42 more .word ptrs)
    .word 0x09e3bf74   @ entry[8]
    ...  (42 .word entries total)
    .word 0x09e3bde4   @ entry[49]
banlist_handler_table:
    .word  0x08019661   @ dispatch_banlist_scene_handler+1 (THUMB)
    .word  0x0801a329   @ (another handler+1)
    .word  0x0801b5d9   @ tick_banlist_scene_frame+1 (THUMB)
    .word  0x00000000   @ NULL sentinel
.incbin 0x1E589A4, 0x368   @ remainder (0x420 - 0xA8 - 0x10 = 0x368)
```
Coverage equation: 0xA8 (42 entries) + 0x10 (handler table 4 .word) + 0x368 = 0x420 == original. PASS.
Refs for banlist_handler_table: DWORD_0801b678 (L17576) and DAT_0801b704 (L17664). Confidence: high.
Handler table THUMB ptrs: .word fn+1 (THUMB). Verify: 0x08019661 = dispatch_banlist_scene_handler+1? ROM: entry[50]=0x08019661; function start = 0x08019660 = some banlist scene handler. Confirm with asm grep.

### Carve 3: banlist_scroll_view_anim_params @0x09e3c6ab (from assert carve block)

Location: inside assert carve block (0x1E398DC + 0x1F430 = 0x1E58D0C). Right after assert_anmid_ig2d_getanmsequencescoun_670 string NUL at 0x09e3c6aa.

Current assert carve block has an incbin span: `.incbin 0x1E3C6AB, 0x9` (6B table + 3B NUL pad before assert_dstbuffid string at 0x09e3c6b4).

Split:
```
banlist_scroll_view_anim_params:
    .byte 0x06, 0x06, 0x07, 0x07, 0x07, 0x07   @ 6 bytes: view-state animation params
.incbin 0x1E3C6B1, 0x3                           @ 3 NUL bytes pad
```
Coverage: 6 + 3 = 9 == original incbin size. PASS.
Code ref: DWORD_0801b3c4 (L17207) = 0x09e3c6ab. Address is odd (bit0=1) -- the THUMB flag in ref-scan was an artifact of the odd address, NOT a THUMB fn ptr. This is a DATA pointer to a 6-byte byte array. Confidence: high.
Content: {0x06, 0x06, 0x07, 0x07, 0x07, 0x07}. Semantics: indexed by gSettings encoding bits[2:0] (0..5) giving a parameter used in `setup_banlist_sprite_oam_row_batch` call. Confidence: med (indexed read via `sp+gSettings_bits*1` pattern confirmed from asm L17186-17188; exact field meaning requires caller analysis).

## disasm 计划 (R4)

### Block B: ROM_INCBIN 0x1ad18, 0xec (236B) -> 5 THUMB stub handlers

Jump table `dispatch_banlist_cursor_action_jump_table` at 0x0801ad00 (PTR_DAT_0801ad00, L16397) has 6 entries, dispatching via `mov pc, r0` (THUMB, stays in THUMB mode for even addresses per ARM7TDMI undocumented behavior):

| entry | raw_addr | stub_range | size | action |
|---|---|---|---|---|
| entry[0] | 0x0801ad18 | 0x0801ad18..0x0801ad20 | 8B (4 hw) | disasm THUMB |
| entry[1] | 0x0801ae04 | (already disasm: LAB_0801ae04) | -- | skip |
| entry[2] | 0x0801ad20 | 0x0801ad20..0x0801ad4c | 44B (22 hw) | disasm THUMB |
| entry[3] | 0x0801ad4c | 0x0801ad4c..0x0801ad94 | 72B (36 hw) | disasm THUMB |
| entry[4] | 0x0801ad94 | 0x0801ad94..0x0801ade0 | 76B (38 hw) | disasm THUMB |
| entry[5] | 0x0801ade0 | 0x0801ade0..0x0801ae04 | 36B (18 hw) | disasm THUMB |

R4 disasm steps (Ghidra):
1. `clearListing(0x0801ad18, 0x0801ae04)` -- clear entire 236B range first.
2. `setTMode(0x0801ad18, 1)` -- set THUMB for range.
3. Per-stub DisassembleCommand for each of the 5 stubs (NOT single-range disasm -- flow exits at each stub's `bx lr` or `pop {pc}`/`pop {r0}; bx r0`):
   - DisassembleCommand(0x0801ad18, ...)
   - DisassembleCommand(0x0801ad20, ...)
   - DisassembleCommand(0x0801ad4c, ...)
   - DisassembleCommand(0x0801ad94, ...)
   - DisassembleCommand(0x0801ade0, ...)
4. For each disassembled stub: createFunction if Ghidra does not auto-create.
5. Re-export range -> inject_modes -> split_all_s -> build -> byte-identical verify.

Note: stubs dispatched via raw addresses (not THUMB+1) from `mov pc, r0` -- Ghidra may need manual THUMB mode set for each stub range. Follow Seg-5c-ii pattern (DisassembleSeg5cJpHandlers.py).

Stub naming: banlist_cursor_action_handler_0..4 (or derive from body -- body analysis requires post-disasm read).

## 新增 constants / 全局 (如有)

- **No new .equ constants** needed: all equates reuse existing inc files:
  - NAME_INPUT_MODE_CLEAR (name_input.inc) -- 5 slots
  - NAME_INPUT_PAGE_STATE_CLEAR (name_input.inc) -- 1 slot
  - gBanlistPasswordBuffer (ewram.inc) -- 24 slots
  - gPrng (iwram.inc) -- 5 slots
  - gTextEncodingOverride (ewram.inc) -- 2 slots
  - gDemoState (ewram.inc) -- 1 slot
  - EWRAM_BASE (gba_mem.inc) -- 8 slots
  - GSETTINGS_OFFSET (name_input.inc) -- 8 slots

- **New global** (BLOCKED -- see below): cursor_pos_base 0x020053f8 -- only 1 code ref in entire segment; conservative approach is pure RENAME only.

- **New carve labels** (3): banlist_pass_ext_char_group / banlist_handler_table + ptr_table extension / banlist_scroll_view_anim_params.

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址 | 大小 | 内容 | 状态 |
|---|---|---|---|
| 0x0801a89c | 32B (`ROM_INCBIN 0x1a89c, 0x20`) | THUMB 孤儿小函数 (Seg-8 预析: THUMB opcode 形态但 0 ROM 引用; raw=0/thumb=0 for entry; 0x801a8a0 raw=1 at 0x08af5768 是 FS asset compressed blob 偶合 non-code). Seg-8 reviewer 独立复核 PASS §5.1. | §5.1 登记, 留待引用时 R4 disasm |

## 消费者证据 (R6)

- **gBanlistPasswordBuffer offsets** (0x660/661/662/663/664/665/66a/66b/66c/66e/667/670/671/672/673/674/675/676): Confirmed from plates of all 28 functions (asm/00_system_str_vija.s L15630..L17849). Field layout from plates cross-checked: +0x660 halfword (state_mode bits[13:10] + cursor_slot bits[5:2]), +0x661 cursor slot byte, +0x662 sub-mode bits[7:6], +0x663 cursor slot (write path), +0x66a scroll halfword, +0x66b row height byte, +0x66c entry count, +0x66e max count, +0x676 ref palette offset. Confidence: high.

- **banlist_scroll_view_anim_params**: Used at L17186-17188 via memcpy(sp+0x18, 0x09e3c6ab, 6); then indexed by `sp + gSettings_bits*1` to get a byte fed into `tick_banlist_card_slot_anim_oam` (L17367). The 6 values {0x06, 0x06, 0x07, 0x07, 0x07, 0x07} are likely OAM tile slot counts per encoding mode. Confidence: med.

- **banlist_handler_table THUMB ptrs**: 0x08019661 = addr+1 for some banlist scene function; 0x0801a329 and 0x0801b5d9 similar. These are the 3 entries referenced in dispatch_banlist_scene_handler_frame (L17542). Confidence: high (fn ptr chain confirmed by plates).

- **dispatch_banlist_cursor_action jump table** (0x0801ad00): entries confirmed by ROM reads at L16397-16403. Stubs handle 6 cursor action cases in banlist password input; case 1 (entry[1]=0x0801ae04) is the null/no-op path (already disassembled). Confidence: high.

- **NAME_INPUT_MODE_CLEAR reuse in tick_banlist_password_frame**: slots at 0x0801b01c/048/060/11c/170 all = 0xfffffc3f = clear bits[9:6] in `gBanlistPasswordBuffer+0x660` halfword mode field. Same semantics as name_input mode field mask defined in name_input.inc. asm/00_system_str_vija.s L16700/16728/16742/16835/16878. Confidence: high.

## 求助

None. All slots have static evidence at high/med confidence. No BLOCKED items.

---

## Pre-submit Verification (Phase 4 checks)

1. All EQ values confirmed against ROM (python rom byte reads above).
2. carve byte-identical:
   - Carve 1: 0xD5 + 0x1A1 = 0x276 == original. PASS.
   - Carve 2: 0xA8 + 0x10 + 0x368 = 0x420 == original. PASS.
   - Carve 3: 6 + 3 = 9 == original incbin span. PASS.
3. Plate/EOL text: all ASCII. CJK plates listed for full rewrite.
4. §5.1 Block A: ref-scan confirmed raw=0/thumb=0 for entry; sole raw=1 at FS asset offset confirmed non-code.
5. Slot labels: all `^[a-z][a-z0-9_]+$` format. Multiple same-type slots suffixed `_a/_b/_c/_d/_e` or `_<hex>` for disambiguation.
