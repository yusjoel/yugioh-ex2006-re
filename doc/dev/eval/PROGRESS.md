# 反汇编命名 — 进度跟踪文档

> 用途: 跨会话续接的项目状态镜像。新会话读完本文档即可继续工作。
> **每完成 1 个 batch (默认 15 函数), fixer 一次性更新本文档** (PROGRESS 字段 + N 行函数列表)

---

## 续接提示词 (新会话直接粘贴)

```
读 doc/dev/eval/PROGRESS.md 续接反汇编命名工作, batch=15 全自动模式。

python tools/ad-hoc/pick_batch.py --max 15 --out temp/batch.json   # ← 改 15 调整 batch 大小

启动 4-agent loop (executor → reviewer → fixer → lesson-keeper) 处理 batch.json 中的全部函数,
单 Ghidra session + 单 build + 单 sha1 verify, byte-identical 通过后自动 commit, 进入下一 batch。

任何函数失败 (byte-identical ❌ / MAX_ITER / agent 求助 / 无法命名) → 不停下询问:
  1. 在 PROGRESS.md "失败追踪" 段记录 (ADDR, reason, date)
  2. 该函数标 ⚠ FAIL 于函数列表对应行
  3. pick_batch.py 自动把"含失败 callee"的函数标 SKIP, 不进入下一 batch
  4. 继续下一批

仅 BLOCKED 但有命名的函数仍走落地 (BLOCKED 是 SB tracking 不阻塞 rename)。
```

---

## 当前状态

| 字段 | 值 |
|------|----|
| **根函数** | `enter_deck_edit_page` (0x08108ac0) |
| **当前步骤** | 函数命名循环进行中, 已完成 122/259 |
| **下一步** | 开始分析 `FUN_080ff41a` (topo=166, L3, indeg=1, E) |
| **上次更新** | 2026-05-03 11:30 |
| **上次 callgraph 刷新** | 2026-05-02 17:52 |
| **callgraph_locked** | `true` (整任务期间禁用 refresh — rename 不改变拓扑结构, 仅手工拆分/合并函数后才需重置 false 并 refresh 一次) |

## 进度

**122 / 259 (47.10%) 已分析** (跳过 A 已命名 + B runtime/invoker)

---

## 函数列表 (按 topo_idx 升序, 跳过 A/B 类)

> 列说明: # 序号 / topo 拓扑序 / depth BFS 深度 / indeg 全 ROM 入度 / class C 高 indeg / D 中 / E 低 / F orphan
> rev = 本函数完成命名所需的 reviewer 轮数 (期望 ≤ 3)

| # | topo | L | indeg | class | 位置 | 分析前 | 分析后 | rev | eval |
|---|------|---|-------|-------|------|--------|--------|-----|------|
| 1 | 1 | L5 | 13 | D | `0x08014470` | FUN_08014470 | copy_str_unbounded | 1 | [eval](08014470.md) |
| 2 | 2 | L5 | 10 | D | `0x0801455c` | FUN_0801455c | count_str_charlen | 2 | [eval](0801455c.md) |
| 3 | 6 | L7 | 1 | E | `0x08014ea0` | FUN_08014ea0 | measure_str_bytelen | 1 | [eval](08014ea0.md) |
| 4 | 7 | L4 | 137 | C | `0x080fa4dc` | FUN_080fa4dc | suppress_assert_report | 2 | [eval](080fa4dc.md) |
| 5 | 8 | L6 | 1 | E | `0x08014eb4` | FUN_08014eb4 | find_substr_offset | 1 | [eval](08014eb4.md) |
| 6 | 16 | L3 | 3 | E | `0x08016afc` | FUN_08016afc | resolve_prhlist_entry_name_ptr | 1 | [eval](08016afc.md) |
| 7 | 17 | L5 | 1 | E | `0x080f1720` | FUN_080f1720 | render_glyph_indexed_dual_layer | 1 | [eval](080f1720.md) |
| 8 | 19 | L5 | 1 | E | `0x080f1440` | FUN_080f1440 | render_glyph_jp_4bpp_dual_layer | 2 | [eval](080f1440.md) |
| 9 | 21 | L6 | 1 | E | `0x080f1070` | FUN_080f1070 | blit_glyph_col_to_buffer | 1 | [eval](080f1070.md) |
| 10 | 22 | L6 | 1 | E | `0x080f1180` | FUN_080f1180 | blit_glyph_row_colored | 1 | [eval](080f1180.md) |
| 11 | 27 | L5 | 2 | E | `0x080f05d0` | FUN_080f05d0 | test_char_kinsoku_head | 1 | [eval](080f05d0.md) |
| 12 | 28 | L5 | 2 | E | `0x080f1bbc` | FUN_080f1bbc | count_word_charlen | 1 | [eval](080f1bbc.md) |
| 13 | 29 | L4 | 3 | E | `0x080f21e8` | FUN_080f21e8 | render_jp_string_glyph_loop | 1 | [eval](080f21e8.md) |
| 14 | 31 | L7 | 3 | E | `0x080175f4` | FUN_080175f4 | dispatch_text_render_by_mode | 2 | [eval](080175f4.md) |
| 15 | 32 | L8 | 6 | D | `0x080f42b4` | FUN_080f42b4 | init_font_jp_render_context | 1 | [eval](080f42b4.md) |
| 16 | 33 | L7 | 1 | E | `0x080177dc` | FUN_080177dc | setup_font_jp_ctx_obj_vram_row | 1 | [eval](080177dc.md) |
| 17 | 34 | L6 | 2 | E | `0x080183d0` | FUN_080183d0 | render_jp_text_to_vram_obj | 3 | [eval](080183d0.md) |
| 18 | 35 | L6 | 2 | E | `0x08018400` | FUN_08018400 | zero_obj_vram_tiles | 1 | [eval](08018400.md) |
| 19 | 36 | L5 | 3 | E | `0x08018774` | FUN_08018774 | refresh_selected_char_obj_tile | 1 | [eval](08018774.md) |
| 20 | 37 | L4 | 1 | E | `0x0801950c` | FUN_0801950c | commit_input_name_to_buf | 1 | [eval](0801950c.md) |
| 21 | 39 | L4 | 9 | D | `0x080fa4d4` | FUN_080fa4d4 | return_void_handler | 1 | [eval](080fa4d4.md) |
| 22 | 41 | L3 | 150 | C | `0x080f4ea4` | FUN_080f4ea4 | copy_bytes_by_halfword | 1 | [eval](080f4ea4.md) |
| 23 | 42 | L8 | 30 | C | `0x080f4f08` | FUN_080f4f08 | copy_memory_dma3_with_cpu_fallback | 1 | [eval](080f4f08.md) |
| 24 | 44 | L2 | 130 | C | `0x080f4e74` | FUN_080f4e74 | zero_fill_by_halfword | 1 | [eval](080f4e74.md) |
| 25 | 46 | L2 | 24 | C | `0x080f42a0` | FUN_080f42a0 | store_ewram_ctx_ptr_and_clear_mode_flags | 2 | [eval](080f42a0.md) |
| 26 | 47 | L8 | 1 | E | `0x080f5a10` | FUN_080f5a10 | reset_bg_hscroll_regs_and_shadows | 1 | [eval](080f5a10.md) |
| 27 | 48 | L8 | 1 | E | `0x080f5a4c` | FUN_080f5a4c | reset_bg_vscroll_regs_and_shadows | 1 | [eval](080f5a4c.md) |
| 28 | 49 | L7 | 24 | C | `0x080f5a88` | FUN_080f5a88 | reset_all_bg_scroll_regs_and_shadows | 1 | [eval](080f5a88.md) |
| 29 | 50 | L3 | 29 | C | `0x080f4e98` | FUN_080f4e98 | zero_fill_halfword_wrapper | 1 | [eval](080f4e98.md) |
| 30 | 51 | L4 | 2 | E | `0x080f5e98` | FUN_080f5e98 | clear_obj_list_entries_range (BLOCKED SB-080f5e98-1) | 2 | [eval](080f5e98.md) |
| 31 | 52 | L3 | 3 | E | `0x080f5ef4` | FUN_080f5ef4 | init_scene_obj_list | 1 | [eval](080f5ef4.md) |
| 32 | 53 | L2 | 22 | C | `0x080f7674` | FUN_080f7674 | reset_display_and_obj_vram | 1 | [eval](080f7674.md) |
| 33 | 56 | L6 | 6 | D | `0x080ee988` | FUN_080ee988 | resolve_card_gfx_pointer_by_type | 1 | [eval](080ee988.md) |
| 34 | 59 | L8 | 2 | E | `0x0801d510` | FUN_0801d510 | render_card_name_to_line_buf | 1 | [eval](0801d510.md) |
| 35 | 60 | L3 | 57 | C | `0x080f0bb4` | FUN_080f0bb4 | setup_line_buf_pos_and_font | 1 | [eval](080f0bb4.md) |
| 36 | 61 | L4 | 3 | E | `0x080f35e8` | FUN_080f35e8 | blit_tile_color_to_vram_region | 3 | [eval](080f35e8.md) |
| 37 | 62 | L4 | 5 | D | `0x080f4ed0` | FUN_080f4ed0 | copy_words_aligned | 1 | [eval](080f4ed0.md) |
| 38 | 64 | L7 | 1 | E | `0x0801d6b4` | FUN_0801d6b4 | draw_card_name_label_to_vram | 1 | [eval](0801d6b4.md) |
| 39 | 66 | L9 | 2 | E | `0x080f1b0c` | FUN_080f1b0c | blit_glyph_columns_to_buf | 2 | [eval](080f1b0c.md) |
| 40 | 68 | L8 | 2 | E | `0x0801d70c` | FUN_0801d70c | render_atk_def_digits_to_buf | 1 | [eval](0801d70c.md) |
| 41 | 69 | L7 | 1 | E | `0x0801d7d0` | FUN_0801d7d0 | draw_atk_def_label_to_vram | 1 | [eval](0801d7d0.md) |
| 42 | 70 | L9 | 22 | C | `0x080f54e0` | FUN_080f54e0 | count_bytes_until_null | 1 | [eval](080f54e0.md) |
| 43 | 72 | L8 | 2 | E | `0x0801d830` | FUN_0801d830 | render_card_level_text_to_buf | 2 | [eval](0801d830.md) |
| 44 | 73 | L8 | 2 | E | `0x080ef454` | FUN_080ef454 | lookup_level_glyph_index | 1 | [eval](080ef454.md) |
| 45 | 74 | L7 | 1 | E | `0x0801d92c` | FUN_0801d92c | draw_card_level_label_to_vram | 1 | [eval](0801d92c.md) |
| 46 | 75 | L7 | 2 | E | `0x080ef2cc` | FUN_080ef2cc | resolve_card_type_icon_ptr | 1 | [eval](080ef2cc.md) |
| 47 | 76 | L8 | 2 | E | `0x080edf00` | FUN_080edf00 | upload_tile_and_palette_from_struct | 2 | [eval](080edf00.md) |
| 48 | 77 | L8 | 2 | E | `0x080edf4c` | FUN_080edf4c | write_tile_row_to_vram | 1 | [eval](080edf4c.md) |
| 49 | 78 | L7 | 10 | D | `0x080ee010` | FUN_080ee010 | load_pack_tile_and_map_to_vram | 2 | [eval](080ee010.md) |
| 50 | 79 | L7 | 2 | E | `0x080ef3bc` | FUN_080ef3bc | check_card_atk_in_valid_range | 2 | [eval](080ef3bc.md) |
| 51 | 82 | L5 | 1 | E | `0x0801dfa0` | FUN_0801dfa0 | tick_scroll_frame_and_update_pos | 2 | [eval](0801dfa0.md) |
| 52 | 83 | L6 | 32 | C | `0x080f0cc0` | FUN_080f0cc0 | setup_line_buf_with_font_and_align | 1 | [eval](080f0cc0.md) |
| 53 | 85 | L7 | 1 | E | `0x080ef488` | FUN_080ef488 | resolve_card_flag_table_ptr | 2 | [eval](080ef488.md) |
| 54 | 86 | L6 | 3 | E | `0x080ef4bc` | FUN_080ef4bc | test_card_flag_bit | 1 | [eval](080ef4bc.md) |
| 55 | 88 | L5 | 26 | C | `0x080f55d4` | FUN_080f55d4 | disable_blend_and_clear_step | 2 | [eval](080f55d4.md) |
| 56 | 89 | L4 | 17 | D | `0x080f58b8` | FUN_080f58b8 | tick_blend_step_by_delta | 1 | [eval](080f58b8.md) |
| 57 | 90 | L5 | 1 | E | `0x0801e328` | FUN_0801e328 | tick_blend_fadeout_and_set_dispcnt | 2 | [eval](0801e328.md) |
| 58 | 91 | L6 | 21 | C | `0x080f5840` | FUN_080f5840 | start_blend_fadein_with_target | 2 | [eval](080f5840.md) |
| 59 | 92 | L5 | 2 | E | `0x0801e344` | FUN_0801e344 | tick_blend_fadein_and_poll_done | 2 | [eval](0801e344.md) |
| 60 | 93 | L4 | 10 | D | `0x0810d150` | FUN_0810d150 | init_sprite_entry_by_id | 1 | [eval](0810d150.md) |
| 61 | 94 | L3 | 77 | C | `0x080f9ab4` | FUN_080f9ab4 | sync_state_and_init_sprite | 1 | [eval](080f9ab4.md) |
| 62 | 95 | L5 | 1 | E | `0x0801e36c` | FUN_0801e36c | update_card_info_page_state | 2 | [eval](0801e36c.md) |
| 63 | 98 | L6 | 16 | D | `0x080f6450` | FUN_080f6450 | write_oam_entry_with_tile_inc | 1 | [eval](eval/080f6450.md) |
| 64 | 99 | L4 | 83 | C | `0x080f616c` | FUN_080f616c | write_oam_entry_from_packed_args | 1 | [eval](eval/080f616c.md) |
| 65 | 100 | L6 | 1 | E | `0x0801e490` | FUN_0801e490 | draw_card_stat_digits_to_oam | 1 | [eval](eval/0801e490.md) |
| 66 | 101 | L6 | 1 | E | `0x0801e594` | FUN_0801e594 | draw_stat_row_sprites_to_oam | 1 | [eval](eval/0801e594.md) |
| 67 | 102 | L5 | 1 | E | `0x0801e620` | FUN_0801e620 | render_card_stats_oam_for_current_card | 1 | [eval](eval/0801e620.md) |
| 68 | 104 | L4 | 6 | D | `0x0801e714` | FUN_0801e714 | tick_card_info_page_by_state | 1 | [eval](eval/0801e714.md) |
| 69 | 105 | L3 | 11 | D | `0x0801e7b8` | FUN_0801e7b8 | get_card_data_format_id | 1 | [eval](eval/0801e7b8.md) |
| 70 | 106 | L4 | 2 | E | `0x0801e7bc` | FUN_0801e7bc | lookup_card_entry_by_index | 1 | [eval](eval/0801e7bc.md) |
| 71 | 107 | L4 | 1 | E | `0x0801e7cc` | FUN_0801e7cc | load_card_fs_entry_to_struct | 1 | [eval](eval/0801e7cc.md) |
| 72 | 108 | L5 | 41 | C | `0x0804ab4c` | FUN_0804ab4c | check_card_pair_allowed | 1 | [eval](eval/0804ab4c.md) |
| 73 | 109 | L4 | 1 | E | `0x080ee050` | FUN_080ee050 | upload_sprite_tiles_and_write_oam | 1 | [eval](eval/080ee050.md) |
| 74 | 110 | L4 | 1 | E | `0x080ee264` | FUN_080ee264 | upload_sprite_tiles_with_palette_blend | 1 | [eval](eval/080ee264.md) |
| 75 | 112 | L5 | 1 | E | `0x080f0cf8` | FUN_080f0cf8 | setup_line_buf_font_align_and_tile_fields | 1 | [eval](eval/080f0cf8.md) |
| 76 | 113 | L4 | 1 | E | `0x080f0d8c` | FUN_080f0d8c | setup_line_buf_font_with_char_index | 1 | [eval](eval/080f0d8c.md) |
| 77 | 114 | L5 | 10 | D | `0x080f506c` | FUN_080f506c | append_text_to_buf_end | 1 | [eval](eval/080f506c.md) |
| 78 | 115 | L6 | 2 | E | `0x080f508c` | FUN_080f508c | format_decimal_halfword_to_buf | 2 | [eval](eval/080f508c.md) |
| 79 | 116 | L6 | 4 | E | `0x080f50f0` | FUN_080f50f0 | format_decimal_byte_to_buf | 1 | [eval](eval/080f50f0.md) |
| 80 | 117 | L4 | 7 | D | `0x080f5148` | FUN_080f5148 | expand_format_text_to_buf | 1 | [eval](eval/080f5148.md) |
| 81 | 118 | L5 | 7 | D | `0x080f5228` | FUN_080f5228 | expand_format_decimal_to_buf | 1 | [eval](eval/080f5228.md) |
| 82 | 119 | L3 | 10 | D | `0x080f57d0` | FUN_080f57d0 | apply_blend_fadeout_flat | 1 | [eval](eval/080f57d0.md) |
| 83 | 121 | L5 | 4 | E | `0x080f5d1c` | FUN_080f5d1c | bsearch_index_by_callback | 2 | [eval](eval/080f5d1c.md) |
| 84 | 122 | L4 | 4 | E | `0x080f61e4` | FUN_080f61e4 | write_obj_attr_packed | 2 | [eval](eval/080f61e4.md) |
| 85 | 123 | L6 | 1 | E | `0x080f6578` | FUN_080f6578 | write_obj_attr_with_priority | 2 | [eval](eval/080f6578.md) |
| 86 | 125 | L4 | 2 | E | `0x0810cf10` | FUN_0810cf10 | init_sound_channel_entry | 1 | [eval](eval/0810cf10.md) |
| 87 | 126 | L3 | 7 | D | `0x0810cf54` | FUN_0810cf54 | reset_sound_channel_entry | 1 | [eval](eval/0810cf54.md) |
| 88 | 127 | L2 | 15 | D | `0x080f9adc` | FUN_080f9adc | set_channel_if_changed | 1 | [eval](eval/080f9adc.md) |
| 89 | 128 | L4 | 1 | E | `0x080f9bc4` | FUN_080f9bc4 | copy_puzzle_seed_to_wram | 1 | [eval](eval/080f9bc4.md) |
| 90 | 129 | L4 | 2 | E | `0x080f9c08` | FUN_080f9c08 | compute_puzzle_checksum | 1 | [eval](eval/080f9c08.md) |
| 91 | 130 | L3 | 12 | D | `0x080f9c68` | FUN_080f9c68 | init_puzzle_wram_and_checksum | 1 | [eval](eval/080f9c68.md) |
| 92 | 131 | L4 | 1 | E | `0x0810e460` | FUN_0810e460 | copy_bytes_with_waitcnt | 1 | [eval](eval/0810e460.md) |
| 93 | 133 | L3 | 1 | E | `0x0810e588` | FUN_0810e588 | copy_with_waitcnt_and_verify_loop | 2 | [eval](eval/0810e588.md) |
| 94 | 134 | L2 | 9 | D | `0x080f9c88` | FUN_080f9c88 | init_puzzle_wram_then_copy | 1 | [eval](eval/080f9c88.md) |
| 95 | 135 | L3 | 8 | D | `0x08103280` | FUN_08103280 | read_card_list_field_by_row_col | 2 | [eval](eval/08103280.md) |
| 96 | 136 | L3 | 8 | D | `0x08103244` | FUN_08103244 | read_card_list_field_by_index | 1 | [eval](eval/08103244.md) |
| 97 | 137 | L4 | 5 | D | `0x08109848` | FUN_08109848 | resolve_card_gfx_row_by_type | 1 | [eval](eval/08109848.md) |
| 98 | 138 | L4 | 4 | E | `0x08109788` | FUN_08109788 | resolve_card_frame_palette_by_type | 1 | [eval](eval/08109788.md) |
| 99 | 139 | L3 | 2 | E | `0x081014fc` | FUN_081014fc | setup_card_list_tile_rows | 1 | [eval](eval/081014fc.md) |
| 100 | 141 | L5 | 1 | E | `0x08100980` | FUN_08100980 | render_card_name_label | 2 | [eval](eval/08100980.md) |
| 101 | 142 | L4 | 1 | E | `0x08100968` | FUN_08100968 | dispatch_render_card_name_with_flags | 1 | [eval](eval/08100968.md) |
| 102 | 143 | L4 | 1 | E | `0x08102494` | FUN_08102494 | search_card_list_subtable_by_key | 2 | [eval](eval/08102494.md) |
| 103 | 144 | L4 | 3 | E | `0x08102914` | FUN_08102914 | read_card_list_type_hi_nibble | 2 | [eval](eval/08102914.md) |
| 104 | 145 | L3 | 3 | E | `0x08100238` | FUN_08100238 | render_card_list_entry_row | 1 | [eval](eval/08100238.md) |
| 105 | 146 | L3 | 2 | E | `0x08100f38` | FUN_08100f38 | render_game_text_centered_label | 1 | [eval](eval/08100f38.md) |
| 106 | 147 | L3 | 3 | E | `0x0810133c` | FUN_0810133c | setup_card_list_bg2_tilemap | 1 | [eval](eval/0810133c.md) |
| 107 | 148 | L3 | 4 | E | `0x080ff9c0` | FUN_080ff9c0 | reset_card_list_scroll_state | 1 | [eval](eval/080ff9c0.md) |
| 108 | 149 | L3 | 1 | E | `0x081016c0` | FUN_081016c0 | load_card_mini_frame_tiles_by_type | 1 | [eval](081016c0.md) |
| 109 | 151 | L3 | 4 | E | `0x08100048` | FUN_08100048 | resolve_card_scroll_offset_by_mode | 2 | [eval](08100048.md) |
| 110 | 152 | L4 | 3 | E | `0x081044ac` | FUN_081044ac | clear_card_list_slot_flag_by_index | 1 | [eval](081044ac.md) |
| 111 | 153 | L3 | 3 | E | `0x081014e4` | FUN_081014e4 | clear_all_card_list_slot_flags | 2 | [eval](081014e4.md) |
| 112 | 154 | L4 | 3 | E | `0x0810445c` | FUN_0810445c | load_card_frame_tile_row_by_index | 1 | [eval](0810445c.md) |
| 113 | 155 | L3 | 5 | D | `0x08101454` | FUN_08101454 | dispatch_card_frame_tile_load_by_type | 1 | [eval](08101454.md) |
| 114 | 156 | L3 | 1 | E | `0x08101068` | FUN_08101068 | load_card_full_frame_tiles_and_palettes | 1 | [eval](08101068.md) |
| 115 | 157 | L3 | 3 | E | `0x08100b70` | FUN_08100b70 | render_card_list_visible_slots | 2 | [eval](08100b70.md) |
| 116 | 158 | L4 | 2 | E | `0x0810a0e8` | FUN_0810a0e8 | format_decimal_with_sign_pos | 1 | [eval](0810a0e8.md) |
| 117 | 159 | L4 | 2 | E | `0x0810a0fc` | FUN_0810a0fc | format_decimal_with_sign_neg | 2 | [eval](0810a0fc.md) |
| 118 | 160 | L3 | 1 | E | `0x08100d70` | FUN_08100d70 | render_deck_count_diff_label | 2 | [eval](08100d70.md) |
| 119 | 161 | L3 | 3 | E | `0x0810017c` | FUN_0810017c | write_card_list_slot_tiles_to_vram | 2 | [eval](0810017c.md) |
| 120 | 163 | L2 | 4 | E | `0x080fe2b4` | FUN_080fe2b4 | reset_card_list_scene_state | 1 | [eval](080fe2b4.md) |
| 121 | 164 | L2 | 6 | D | `0x080fe2e8` | FUN_080fe2e8 | init_card_list_display_and_objs | 2 | [eval](080fe2e8.md) |
| 122 | 165 | L3 | 1 | E | `0x080ff418` | FUN_080ff418 | return_zero_epilogue_stub | 1 | [eval](080ff418.md) |
| 123 | 166 | L3 | 1 | E | `0x080ff41a` | FUN_080ff41a | _(待分析)_ | — | — |
| 124 | 167 | L4 | 3 | E | `0x08102538` | FUN_08102538 | _(待分析)_ | — | — |
| 125 | 168 | L3 | 2 | E | `0x08102620` | FUN_08102620 | _(待分析)_ | — | — |
| 126 | 169 | L4 | 5 | D | `0x081044c0` | FUN_081044c0 | _(待分析)_ | — | — |
| 127 | 170 | L4 | 1 | E | `0x081078f8` | FUN_081078f8 | _(待分析)_ | — | — |
| 128 | 171 | L4 | 3 | E | `0x08107a48` | FUN_08107a48 | _(待分析)_ | — | — |
| 129 | 172 | L4 | 1 | E | `0x0810793c` | FUN_0810793c | _(待分析)_ | — | — |
| 130 | 173 | L3 | 3 | E | `0x08107198` | FUN_08107198 | _(待分析)_ | — | — |
| 131 | 174 | L3 | 1 | E | `0x080ff824` | FUN_080ff824 | _(待分析)_ | — | — |
| 132 | 175 | L4 | 1 | E | `0x0810372c` | FUN_0810372c | _(待分析)_ | — | — |
| 133 | 176 | L4 | 2 | E | `0x08103c3c` | FUN_08103c3c | _(待分析)_ | — | — |
| 134 | 179 | L5 | 2 | E | `0x08104130` | FUN_08104130 | _(待分析)_ | — | — |
| 135 | 180 | L4 | 2 | E | `0x081035f4` | FUN_081035f4 | _(待分析)_ | — | — |
| 136 | 181 | L4 | 2 | E | `0x081038fc` | FUN_081038fc | _(待分析)_ | — | — |
| 137 | 182 | L3 | 9 | D | `0x081031a4` | FUN_081031a4 | _(待分析)_ | — | — |
| 138 | 183 | L3 | 6 | D | `0x08101c40` | FUN_08101c40 | _(待分析)_ | — | — |
| 139 | 184 | L5 | 1 | E | `0x08106d88` | FUN_08106d88 | _(待分析)_ | — | — |
| 140 | 185 | L5 | 1 | E | `0x08106c10` | FUN_08106c10 | _(待分析)_ | — | — |
| 141 | 186 | L5 | 1 | E | `0x08106e38` | FUN_08106e38 | _(待分析)_ | — | — |
| 142 | 187 | L4 | 1 | E | `0x081067e0` | FUN_081067e0 | _(待分析)_ | — | — |
| 143 | 188 | L3 | 1 | E | `0x080ff528` | FUN_080ff528 | _(待分析)_ | — | — |
| 144 | 189 | L4 | 1 | E | `0x08101a88` | FUN_08101a88 | _(待分析)_ | — | — |
| 145 | 190 | L3 | 14 | D | `0x08107b4c` | FUN_08107b4c | _(待分析)_ | — | — |
| 146 | 191 | L4 | 1 | E | `0x08101d0c` | FUN_08101d0c | _(待分析)_ | — | — |
| 147 | 192 | L4 | 1 | E | `0x08101c94` | FUN_08101c94 | _(待分析)_ | — | — |
| 148 | 193 | L4 | 3 | E | `0x08107eb0` | FUN_08107eb0 | _(待分析)_ | — | — |
| 149 | 194 | L4 | 10 | D | `0x080ffaa4` | FUN_080ffaa4 | _(待分析)_ | — | — |
| 150 | 195 | L6 | 2 | E | `0x0810a8e4` | FUN_0810a8e4 | _(待分析)_ | — | — |
| 151 | 196 | L5 | 1 | E | `0x0810a52c` | FUN_0810a52c | _(待分析)_ | — | — |
| 152 | 197 | L4 | 5 | D | `0x0810a8c0` | FUN_0810a8c0 | _(待分析)_ | — | — |
| 153 | 198 | L4 | 1 | E | `0x080ff918` | FUN_080ff918 | _(待分析)_ | — | — |
| 154 | 199 | L4 | 1 | E | `0x081081a0` | FUN_081081a0 | _(待分析)_ | — | — |
| 155 | 200 | L5 | 6 | D | `0x08107b90` | FUN_08107b90 | _(待分析)_ | — | — |
| 156 | 201 | L4 | 1 | E | `0x081016a4` | FUN_081016a4 | _(待分析)_ | — | — |
| 157 | 202 | L4 | 1 | E | `0x08101ba8` | FUN_08101ba8 | _(待分析)_ | — | — |
| 158 | 203 | L4 | 1 | E | `0x08101e2c` | FUN_08101e2c | _(待分析)_ | — | — |
| 159 | 204 | L5 | 1 | E | `0x0810ab90` | FUN_0810ab90 | _(待分析)_ | — | — |
| 160 | 206 | L5 | 1 | E | `0x0810a944` | FUN_0810a944 | _(待分析)_ | — | — |
| 161 | 207 | L4 | 1 | E | `0x0810a22c` | FUN_0810a22c | _(待分析)_ | — | — |
| 162 | 208 | L4 | 1 | E | `0x08100cc4` | FUN_08100cc4 | _(待分析)_ | — | — |
| 163 | 209 | L4 | 2 | E | `0x08107ec4` | FUN_08107ec4 | _(待分析)_ | — | — |
| 164 | 210 | L5 | 1 | E | `0x08107e5c` | FUN_08107e5c | _(待分析)_ | — | — |
| 165 | 211 | L4 | 1 | E | `0x080ff94c` | FUN_080ff94c | _(待分析)_ | — | — |
| 166 | 212 | L4 | 1 | E | `0x0810a8d4` | FUN_0810a8d4 | _(待分析)_ | — | — |
| 167 | 213 | L5 | 1 | E | `0x081083b0` | FUN_081083b0 | _(待分析)_ | — | — |
| 168 | 214 | L5 | 1 | E | `0x081081bc` | FUN_081081bc | _(待分析)_ | — | — |
| 169 | 215 | L6 | 1 | E | `0x0810a190` | FUN_0810a190 | _(待分析)_ | — | — |
| 170 | 216 | L5 | 1 | E | `0x0810823c` | FUN_0810823c | _(待分析)_ | — | — |
| 171 | 217 | L4 | 1 | E | `0x08107bdc` | FUN_08107bdc | _(待分析)_ | — | — |
| 172 | 218 | L4 | 1 | E | `0x080ff9e0` | FUN_080ff9e0 | _(待分析)_ | — | — |
| 173 | 219 | L4 | 1 | E | `0x08101764` | FUN_08101764 | _(待分析)_ | — | — |
| 174 | 220 | L4 | 1 | E | `0x08101574` | FUN_08101574 | _(待分析)_ | — | — |
| 175 | 221 | L3 | 1 | E | `0x080fefaa` | FUN_080fefaa | _(待分析)_ | — | — |
| 176 | 222 | L3 | 1 | E | `0x080ff434` | FUN_080ff434 | _(待分析)_ | — | — |
| 177 | 223 | L3 | 1 | E | `0x080ff4b8` | FUN_080ff4b8 | _(待分析)_ | — | — |
| 178 | 224 | L3 | 1 | E | `0x080fffc4` | FUN_080fffc4 | _(待分析)_ | — | — |
| 179 | 225 | L3 | 1 | E | `0x08106bfc` | FUN_08106bfc | _(待分析)_ | — | — |
| 180 | 226 | L4 | 1 | E | `0x0810796c` | FUN_0810796c | _(待分析)_ | — | — |
| 181 | 227 | L3 | 2 | E | `0x08106ebc` | FUN_08106ebc | _(待分析)_ | — | — |
| 182 | 228 | L3 | 1 | E | `0x080ff8d0` | FUN_080ff8d0 | _(待分析)_ | — | — |
| 183 | 229 | L3 | 2 | E | `0x081078d4` | FUN_081078d4 | _(待分析)_ | — | — |
| 184 | 230 | L3 | 5 | D | `0x0810325c` | FUN_0810325c | _(待分析)_ | — | — |
| 185 | 231 | L5 | 1 | E | `0x08109e08` | FUN_08109e08 | _(待分析)_ | — | — |
| 186 | 232 | L5 | 1 | E | `0x08109a50` | FUN_08109a50 | _(待分析)_ | — | — |
| 187 | 233 | L4 | 1 | E | `0x0810903c` | FUN_0810903c | _(待分析)_ | — | — |
| 188 | 234 | L3 | 1 | E | `0x080ff7e0` | FUN_080ff7e0 | _(待分析)_ | — | — |
| 189 | 235 | L3 | 1 | E | `0x081095e8` | FUN_081095e8 | _(待分析)_ | — | — |
| 190 | 236 | L5 | 1 | E | `0x081099f0` | FUN_081099f0 | _(待分析)_ | — | — |
| 191 | 237 | L4 | 2 | E | `0x081096d4` | FUN_081096d4 | _(待分析)_ | — | — |
| 192 | 238 | L4 | 1 | E | `0x08109300` | FUN_08109300 | _(待分析)_ | — | — |
| 193 | 239 | L4 | 1 | E | `0x08109608` | FUN_08109608 | _(待分析)_ | — | — |
| 194 | 240 | L3 | 1 | E | `0x080ff56c` | FUN_080ff56c | _(待分析)_ | — | — |
| 195 | 241 | L4 | 1 | E | `0x08106b94` | FUN_08106b94 | _(待分析)_ | — | — |
| 196 | 242 | L3 | 1 | E | `0x080ff4f0` | FUN_080ff4f0 | _(待分析)_ | — | — |
| 197 | 243 | L4 | 1 | E | `0x08103b3c` | FUN_08103b3c | _(待分析)_ | — | — |
| 198 | 244 | L3 | 3 | E | `0x08103524` | FUN_08103524 | _(待分析)_ | — | — |
| 199 | 245 | L3 | 2 | E | `0x081026f4` | FUN_081026f4 | _(待分析)_ | — | — |
| 200 | 246 | L4 | 1 | E | `0x08102828` | FUN_08102828 | _(待分析)_ | — | — |
| 201 | 247 | L3 | 1 | E | `0x080ffaf8` | FUN_080ffaf8 | _(待分析)_ | — | — |
| 202 | 248 | L2 | 4 | E | `0x080fe308` | FUN_080fe308 | _(待分析)_ | — | — |
| 203 | 249 | L2 | 4 | E | `0x080ff430` | FUN_080ff430 | _(待分析)_ | — | — |
| 204 | 250 | L4 | 4 | E | `0x08102924` | FUN_08102924 | _(待分析)_ | — | — |
| 205 | 251 | L3 | 4 | E | `0x08103350` | FUN_08103350 | _(待分析)_ | — | — |
| 206 | 252 | L4 | 2 | E | `0x08103820` | FUN_08103820 | _(待分析)_ | — | — |
| 207 | 253 | L3 | 5 | D | `0x0810329c` | FUN_0810329c | _(待分析)_ | — | — |
| 208 | 254 | L3 | 2 | E | `0x081030e0` | FUN_081030e0 | _(待分析)_ | — | — |
| 209 | 255 | L3 | 4 | E | `0x0810322c` | FUN_0810322c | _(待分析)_ | — | — |
| 210 | 256 | L2 | 1 | E | `0x08102034` | FUN_08102034 | _(待分析)_ | — | — |
| 211 | 257 | L3 | 4 | E | `0x081033c4` | FUN_081033c4 | _(待分析)_ | — | — |
| 212 | 258 | L2 | 1 | E | `0x081020e0` | FUN_081020e0 | _(待分析)_ | — | — |
| 213 | 259 | L2 | 1 | E | `0x081021dc` | FUN_081021dc | _(待分析)_ | — | — |
| 214 | 260 | L2 | 1 | E | `0x0810230c` | FUN_0810230c | _(待分析)_ | — | — |
| 215 | 261 | L2 | 8 | D | `0x08104318` | FUN_08104318 | _(待分析)_ | — | — |
| 216 | 262 | L2 | 10 | D | `0x08104328` | FUN_08104328 | _(待分析)_ | — | — |
| 217 | 263 | L3 | 1 | E | `0x081044d4` | FUN_081044d4 | _(待分析)_ | — | — |
| 218 | 264 | L2 | 7 | D | `0x0810432c` | FUN_0810432c | _(待分析)_ | — | — |
| 219 | 265 | L2 | 7 | D | `0x08104458` | FUN_08104458 | _(待分析)_ | — | — |
| 220 | 266 | L3 | 1 | E | `0x081065c0` | FUN_081065c0 | _(待分析)_ | — | — |
| 221 | 267 | L3 | 1 | E | `0x081066fc` | FUN_081066fc | _(待分析)_ | — | — |
| 222 | 268 | L3 | 2 | E | `0x08106130` | FUN_08106130 | _(待分析)_ | — | — |
| 223 | 269 | L4 | 3 | E | `0x081060e4` | FUN_081060e4 | _(待分析)_ | — | — |
| 224 | 270 | L4 | 1 | E | `0x08105d94` | FUN_08105d94 | _(待分析)_ | — | — |
| 225 | 271 | L4 | 1 | E | `0x08105964` | FUN_08105964 | _(待分析)_ | — | — |
| 226 | 272 | L3 | 2 | E | `0x081061d0` | FUN_081061d0 | _(待分析)_ | — | — |
| 227 | 273 | L3 | 2 | E | `0x08105f34` | FUN_08105f34 | _(待分析)_ | — | — |
| 228 | 274 | L3 | 1 | E | `0x08105bfc` | FUN_08105bfc | _(待分析)_ | — | — |
| 229 | 275 | L2 | 4 | E | `0x081045c4` | FUN_081045c4 | _(待分析)_ | — | — |
| 230 | 276 | L2 | 4 | E | `0x081047cc` | FUN_081047cc | _(待分析)_ | — | — |
| 231 | 277 | L3 | 1 | E | `0x08105702` | FUN_08105702 | _(待分析)_ | — | — |
| 232 | 278 | L3 | 1 | E | `0x08106588` | FUN_08106588 | _(待分析)_ | — | — |
| 233 | 279 | L4 | 1 | E | `0x08105948` | FUN_08105948 | _(待分析)_ | — | — |
| 234 | 280 | L4 | 1 | E | `0x081058c8` | FUN_081058c8 | _(待分析)_ | — | — |
| 235 | 281 | L4 | 1 | E | `0x0810672c` | FUN_0810672c | _(待分析)_ | — | — |
| 236 | 282 | L4 | 1 | E | `0x081065fc` | FUN_081065fc | _(待分析)_ | — | — |
| 237 | 284 | L3 | 1 | E | `0x081052aa` | FUN_081052aa | _(待分析)_ | — | — |
| 238 | 285 | L3 | 1 | E | `0x0810573e` | FUN_0810573e | _(待分析)_ | — | — |
| 239 | 286 | L3 | 1 | E | `0x08105740` | FUN_08105740 | _(待分析)_ | — | — |
| 240 | 287 | L2 | 3 | E | `0x081047e8` | FUN_081047e8 | _(待分析)_ | — | — |
| 241 | 288 | L2 | 3 | E | `0x08105754` | FUN_08105754 | _(待分析)_ | — | — |
| 242 | 289 | L2 | 2 | E | `0x08105758` | FUN_08105758 | _(待分析)_ | — | — |
| 243 | 290 | L2 | 2 | E | `0x08105784` | FUN_08105784 | _(待分析)_ | — | — |
| 244 | 291 | L2 | 3 | E | `0x08106eb4` | FUN_08106eb4 | _(待分析)_ | — | — |
| 245 | 292 | L2 | 3 | E | `0x08106eb8` | FUN_08106eb8 | _(待分析)_ | — | — |
| 246 | 293 | L1 | 1 | E | `0x08108da0` | - | _(待分析)_ | — | — |
| 247 | 294 | L1 | 1 | E | `0x08108f80` | FUN_08108f80 | _(待分析)_ | — | — |
| 248 | 295 | L1 | 1 | E | `0x08108da4` | FUN_08108da4 | _(待分析)_ | — | — |
| 249 | 296 | L1 | 1 | E | `0x08108ee8` | - | _(待分析)_ | — | — |
| 250 | 297 | L2 | 3 | E | `0x08109038` | FUN_08109038 | _(待分析)_ | — | — |
| 251 | 298 | L1 | 1 | E | `0x08108c4c` | FUN_08108c4c | _(待分析)_ | — | — |
| 252 | 299 | L1 | 1 | E | `0x08108eec` | FUN_08108eec | _(待分析)_ | — | — |
| 253 | 300 | L1 | 1 | E | `0x08108eb8` | FUN_08108eb8 | _(待分析)_ | — | — |
| 254 | 301 | L1 | 1 | E | `0x08108d70` | FUN_08108d70 | _(待分析)_ | — | — |
| 255 | 302 | L1 | 1 | E | `0x08108fd4` | - | _(待分析)_ | — | — |
| 256 | 303 | L1 | 1 | E | `0x08108fd8` | FUN_08108fd8 | _(待分析)_ | — | — |
| 257 | 304 | L2 | 3 | E | `0x08109034` | FUN_08109034 | _(待分析)_ | — | — |
| 258 | 305 | L1 | 1 | E | `0x08108b38` | FUN_08108b38 | _(待分析)_ | — | — |
| 259 | 306 | L1 | 1 | E | `0x08108cdc` | FUN_08108cdc | _(待分析)_ | — | — |

---

## 历史里程碑

- 2026-05-02 10:30: Step 0 完成, 闭包从 2 → 308 函数 (commit ac61a1e)
- 2026-05-02 11:00: Step 1+2 完成, 拓扑排序 + 分类 (commit 930cccd)
- 2026-05-02 11:55: 装配 refactor-loop 4-agent 体系 (本次 commit)
- 2026-05-02 12:41: 完成 #1 copy_str_unbounded (0x08014470, topo=1, PASSED 45/45, rev=1) — 首函数零缺陷落地
- 2026-05-02 13:14: 0x0801455c PASSED → count_str_charlen (rev=2)
- 2026-05-02 13:28: 0x08014ea0 PASSED → measure_str_bytelen (rev=1) — 首轮零缺陷, 纯字节计数 strlen 变体
- 2026-05-02 13:47: 0x080fa4dc PASSED → suppress_assert_report (rev=2) — 高 indeg=137 / 364 调用点, 发布版空断言回调 (2 字节 bx lr leaf)
- 2026-05-02 14:05: 0x08014eb4 PASSED → find_substr_offset (rev=1) — GL/GL_File.c 朴素 strstr, 字符串泄漏锚三连 (pSrc/pKey/GL_File.c:38-39), 首轮满分
- 2026-05-02 14:16: 0x08016afc PASSED → resolve_prhlist_entry_name_ptr (rev=1) — GL/PRH_Main.c 禁止牌名称查询叶子, 字符串泄漏锚 (pDst->nameID) + 数据 label 反推 (game_str_pointer_table/game_str_ja), 首轮满分
- 2026-05-02 14:31: 0x080f1720 PASSED → render_glyph_indexed_dual_layer (rev=1) — font_jp 渲染族变体, 跳过 char_code_to_glyph_index, 直接以 u8 字形索引查 ROM 字体位图表 4bpp 双写; med 置信度 (3 待运行验证项)
- 2026-05-02 14:53: 0x080f1440 PASSED → render_glyph_jp_4bpp_dual_layer (rev=2, v1 35/45 → v2 45/45) — font_jp 渲染族 4bpp 替代路径, char_code→glyph_index→font_jp_charset/stride 表定位, 4bpp word 双写 (str+adds r4,#0x20), 溢出/单列双分支; 四层证据三角验证 high 置信度
- 2026-05-02 15:08: 0x080f1070 PASSED → blit_glyph_col_to_buffer (rev=1, 45/45) — font_jp 渲染族叶子, blit_glyph_row_to_buffer 列方向对称体; 10 行迭代 (vs 行版 8 列), 4bpp nibble read-modify-write + 8bpp byte write 双路; 三层 high 置信度, 首轮满分落地
- 2026-05-02 15:22: 0x080f1180 PASSED → blit_glyph_row_colored (rev=1, 45/45) — font_jp 渲染族叶子, blit_glyph_row_to_buffer 的显式颜色变体; r3 传入 packed_color nibble (低4位前景/高4位背景), 4bpp nibble read-modify-write + 8bpp byte write 双路, 对应 render_glyph_jp_single_layer sp+0x8 标志非零分支; 首轮满分落地
- 2026-05-02 15:37: 0x080f05d0 PASSED → test_char_kinsoku_head (rev=1, 45/45) — font_jp 禁則处理叶子; char_code→glyph_index→SJIS 码→逐范围比对行頭禁則字符集(小假名/标点/闭括号), 返回 bool; 与 test_char_kinsoku_tail (FUN_080f0720) 构成 JIS X 4051 对称对; 首轮满分落地
- 2026-05-02 15:53: 0x080f1bbc PASSED → count_word_charlen (rev=1, 45/45) — font_jp 换行词元字符数测量叶子; switch 表 179 字符码分支覆盖空白/禁則/转义/句点4类; 三层互证 (word-wrap 调用方 muls×字符宽/数据 label/switch 字符集) high 置信度; 首轮满分落地
- 2026-05-02 16:06: 0x080f21e8 PASSED → render_jp_string_glyph_loop (rev=1, 45/45) — font_jp 模块主字形渲染循环 (topo=29, L4, indeg=3); 被3个薄包装调用, 直调全部4个 render_glyph_* 变体+count_word_charlen+test_char_kinsoku_head; 四层证据互证 (调用图hub+数据label反推+状态机表+兄弟对称体) high 置信度; 首轮满分落地. 里程碑: 已分析 5.02% (13/259), 突破5%.
- 2026-05-02 16:23: 0x080175f4 PASSED → dispatch_text_render_by_mode (rev=2, v1 40/45 → v2 45/45) — name_input 页面族文字渲染分发器 (topo=31, L7, indeg=3); render_mode 三值分支 (0x20 单字符偏移/0x80 8方向描边+中心/其他直接渲染), 最多调用 text_render_wrapper 9 次; v1 因 dispatch_str_render_mode 中 str 与 ARM STORE 助记符歧义被扣R1; v2 改名 dispatch_text_render_by_mode 满分; 已分析 5.41% (14/259).
- 2026-05-02 16:40: 0x080f42b4 PASSED → init_font_jp_render_context (rev=1, 45/45) — font_jp 渲染上下文初始化入口 (topo=32, L8, indeg=6, D); 6 个 text-box setup caller 在页面初始化阶段调用; bios_cpu_set 清零 EWRAM 104 字节上下文结构体, 写入 VRAM 基址/宽高 tiles/函数指针/init-complete bit4; 四层证据互证 (数据label+状态机+调用图hub+IO寄存器簇) high 置信度; 首轮满分落地; 已分析 5.79% (15/259).
- 2026-05-02 17:00: 0x080177dc PASSED → setup_font_jp_ctx_obj_vram_row (rev=1, 45/45) — font_jp OBJ VRAM 行初始化器 (topo=33, L7, indeg=1, E); 唯一 caller FUN_080183d0 (名字输入页面包装层); 以 tile 行索引计算 OBJ VRAM 基址 (0x06010000 + r0×0x20), 调 init_font_jp_render_context 后追加置位 context[+0x15] bit5 + render_flags bit0→bit1 + 重写函数指针; 与 FUN_08017798 (BG VRAM) 形成对称对; med 置信度 (缺 runtime VRAM dump); 首轮满分落地; 已分析 6.18% (16/259).
- 2026-05-02 17:16: 0x080183d0 PASSED → render_jp_text_to_vram_obj (rev=3, 45/45) — name_input 页面文字渲染薄包装 (topo=34, L6, indeg=2, E); 由 FUN_08017b44 (调用 3 次) 和 FUN_08018774 (调用 1 次) 共享; 固化调 setup_font_jp_ctx_obj_vram_row 配置 OBJ VRAM 上下文后以硬编码参数 (r1=1,r2=1,r3=7,arg5=8,arg6=0x80) 调 dispatch_text_render_by_mode; 0x80 模式走 JP 8 行字形 OBJ 渲染路径; v1 NEEDS_FIX 35/45 → v2 40/45 → R7 rubric 放宽 → v3 PASSED 45/45; 已分析 6.56% (17/259).
- 2026-05-02 17:32: 0x08018400 PASSED → zero_obj_vram_tiles (rev=1, 45/45) — render_jp_text_to_vram_obj OBJ tile 清屏前置 (topo=35, L6, indeg=2, E); 两个调用方 (0x08017b44 x3, 0x08018774 x1) 在每次调用 render_jp_text_to_vram_obj 前先调本函数清零目标 tile 区域; BIOS CpuSet SWI 0x0B fill+word 模式将 [0x06010000+tile_idx*32, +num_tiles*32) 填零; 首轮满分落地; 已分析 6.95% (18/259).
- 2026-05-02 17:52: 0x08018774 PASSED → refresh_selected_char_obj_tile (rev=1, 45/45) — name_input 页面双缓冲 OBJ VRAM 字形刷新器 (topo=36, L5, indeg=3, E); 3 个 caller (0x080187e0/0x08018838/0x0801950c) 在字符切换/确认时触发; 读 IWRAM 0x02029564 ping-pong 槽位位域 (bit0 XOR 1), 调 zero_obj_vram_tiles 清空 34 块瓦片后调 render_jp_text_to_vram_obj 写入当前选中假名, 最后 strb 写回翻转槽位完成双缓冲换页; 首轮满分落地; 已分析 7.34% (19/259).
- 2026-05-02 20:17: BATCH=3 PASSED — 0x0801950c→commit_input_name_to_buf / 0x080fa4d4→return_void_handler / 0x080f4ea4→copy_bytes_by_halfword (各 rev=1, 45/45); 单 Ghidra session + 1 build + sha1 9689337d 一致; 已分析 8.49% (22/259).
- 2026-05-02 20:50: BATCH=10 落地 (9 PASSED + 1 BLOCKED) — 0x080f4f08→copy_memory_dma3_with_cpu_fallback (rev=1) / 0x080f4e74→zero_fill_by_halfword (rev=1) / 0x080f42a0→store_ewram_ctx_ptr_and_clear_mode_flags (rev=2) / 0x080f5a10→reset_bg_hscroll_regs_and_shadows (rev=1) / 0x080f5a4c→reset_bg_vscroll_regs_and_shadows (rev=1) / 0x080f5a88→reset_all_bg_scroll_regs_and_shadows (rev=1) / 0x080f4e98→zero_fill_halfword_wrapper (rev=1) / 0x080f5e98→clear_obj_list_entries_range (rev=2, BLOCKED SB-080f5e98-1) / 0x080f5ef4→init_scene_obj_list (rev=1) / 0x080f7674→reset_display_and_obj_vram (rev=1); 单 Ghidra session (10 [ok]) + 1 build + sha1 9689337d 一致; 已分析 12.36% (32/259).
- 2026-05-02 23:00: BATCH=15 落地 #2 (15 PASSED) — 0x080edf4c→write_tile_row_to_vram (rev=1) / 0x080ee010→load_pack_tile_and_map_to_vram (rev=2) / 0x080ef3bc→check_card_atk_in_valid_range (rev=2) / 0x0801dfa0→tick_scroll_frame_and_update_pos (rev=2) / 0x080f0cc0→setup_line_buf_with_font_and_align (rev=1) / 0x080ef488→resolve_card_flag_table_ptr (rev=2) / 0x080ef4bc→test_card_flag_bit (rev=1) / 0x080f55d4→disable_blend_and_clear_step (rev=2) / 0x080f58b8→tick_blend_step_by_delta (rev=1) / 0x0801e328→tick_blend_fadeout_and_set_dispcnt (rev=2) / 0x080f5840→start_blend_fadein_with_target (rev=2) / 0x0801e344→tick_blend_fadein_and_poll_done (rev=2) / 0x0810d150→init_sprite_entry_by_id (rev=1) / 0x080f9ab4→sync_state_and_init_sprite (rev=1) / 0x0801e36c→update_card_info_page_state (rev=2); 单 Ghidra session (15 [ok]) + 1 build + sha1 9689337d 一致; 已分析 23.94% (62/259). 里程碑: 突破 23%, blend/sprite/card_flag 工具簇全落地.
- 2026-05-03 00:00: BATCH=15 落地 #3 (15 PASSED, 15/15 rev=1) — 0x080f6450→write_oam_entry_with_tile_inc / 0x080f616c→write_oam_entry_from_packed_args / 0x0801e490→draw_card_stat_digits_to_oam / 0x0801e594→draw_stat_row_sprites_to_oam / 0x0801e620→render_card_stats_oam_for_current_card / 0x0801e714→tick_card_info_page_by_state / 0x0801e7b8→get_card_data_format_id / 0x0801e7bc→lookup_card_entry_by_index / 0x0801e7cc→load_card_fs_entry_to_struct / 0x0804ab4c→check_card_pair_allowed / 0x080ee050→upload_sprite_tiles_and_write_oam / 0x080ee264→upload_sprite_tiles_with_palette_blend / 0x080f0cf8→setup_line_buf_font_align_and_tile_fields / 0x080f0d8c→setup_line_buf_font_with_char_index / 0x080f506c→append_text_to_buf_end; 单 Ghidra session (15 [ok]) + 1 build + sha1 9689337d 一致; 已分析 29.73% (77/259). 里程碑: 突破 29%, OAM/card_stats/FS/line_buf 工具簇全落地.
- 2026-05-02 23:03: BATCH=15 落地 #4 (15 PASSED, 11 rev=1 + 4 rev=2) — 0x080f508c→format_decimal_halfword_to_buf (rev=2) / 0x080f50f0→format_decimal_byte_to_buf (rev=1) / 0x080f5148→expand_format_text_to_buf (rev=1) / 0x080f5228→expand_format_decimal_to_buf (rev=1) / 0x080f57d0→apply_blend_fadeout_flat (rev=1) / 0x080f5d1c→bsearch_index_by_callback (rev=2) / 0x080f61e4→write_obj_attr_packed (rev=2) / 0x080f6578→write_obj_attr_with_priority (rev=2) / 0x0810cf10→init_sound_channel_entry (rev=1) / 0x0810cf54→reset_sound_channel_entry (rev=1) / 0x080f9adc→set_channel_if_changed (rev=1) / 0x080f9bc4→copy_puzzle_seed_to_wram (rev=1) / 0x080f9c08→compute_puzzle_checksum (rev=1) / 0x080f9c68→init_puzzle_wram_and_checksum (rev=1) / 0x0810e460→copy_bytes_with_waitcnt (rev=1); 单 Ghidra session (15 [ok]) + 1 build + sha1 9689337d 一致; 已分析 35.52% (92/259). 里程碑: 突破 35%, format_decimal/expand_format/bsearch/OBJ_attr/sound_channel/puzzle_seed 工具簇全落地.
- 2026-05-03 10:16: BATCH=15 落地 #5 (15 PASSED, 10 rev=1 + 5 rev=2) — 0x0810e588→copy_with_waitcnt_and_verify_loop (rev=2) / 0x080f9c88→init_puzzle_wram_then_copy (rev=1) / 0x08103280→read_card_list_field_by_row_col (rev=2) / 0x08103244→read_card_list_field_by_index (rev=1) / 0x08109848→resolve_card_gfx_row_by_type (rev=1) / 0x08109788→resolve_card_frame_palette_by_type (rev=1) / 0x081014fc→setup_card_list_tile_rows (rev=1) / 0x08100980→render_card_name_label (rev=2) / 0x08100968→dispatch_render_card_name_with_flags (rev=1) / 0x08102494→search_card_list_subtable_by_key (rev=2) / 0x08102914→read_card_list_type_hi_nibble (rev=2) / 0x08100238→render_card_list_entry_row (rev=1) / 0x08100f38→render_game_text_centered_label (rev=1) / 0x0810133c→setup_card_list_bg2_tilemap (rev=1) / 0x080ff9c0→reset_card_list_scroll_state (rev=1); 单 Ghidra session (15 [ok]) + 1 build + sha1 9689337d 一致; 已分析 41.31% (107/259). 里程碑: 突破 41%, card_list 渲染/查表/tilemap 工具簇全落地.
- 2026-05-03 11:30: BATCH=15 落地 #6 (15 PASSED, 8 rev=1 + 7 rev=2) — 0x081016c0→load_card_mini_frame_tiles_by_type (rev=1) / 0x08100048→resolve_card_scroll_offset_by_mode (rev=2) / 0x081044ac→clear_card_list_slot_flag_by_index (rev=1) / 0x081014e4→clear_all_card_list_slot_flags (rev=2) / 0x0810445c→load_card_frame_tile_row_by_index (rev=1) / 0x08101454→dispatch_card_frame_tile_load_by_type (rev=1) / 0x08101068→load_card_full_frame_tiles_and_palettes (rev=1) / 0x08100b70→render_card_list_visible_slots (rev=2) / 0x0810a0e8→format_decimal_with_sign_pos (rev=1) / 0x0810a0fc→format_decimal_with_sign_neg (rev=2) / 0x08100d70→render_deck_count_diff_label (rev=2) / 0x0810017c→write_card_list_slot_tiles_to_vram (rev=2) / 0x080fe2b4→reset_card_list_scene_state (rev=1) / 0x080fe2e8→init_card_list_display_and_objs (rev=2) / 0x080ff418→return_zero_epilogue_stub (rev=1); 单 Ghidra session (15 [ok]) + 1 build + sha1 9689337d 一致; 已分析 47.10% (122/259). 里程碑: 突破 47%, card_list 帧/tile/slot/scroll 初始化工具簇全落地.
- 2026-05-02 21:40: BATCH=15 落地 (15 PASSED) — 0x080ee988→resolve_card_gfx_pointer_by_type (rev=1) / 0x0801d510→render_card_name_to_line_buf (rev=1) / 0x080f0bb4→setup_line_buf_pos_and_font (rev=1) / 0x080f35e8→blit_tile_color_to_vram_region (rev=3) / 0x080f4ed0→copy_words_aligned (rev=1) / 0x0801d6b4→draw_card_name_label_to_vram (rev=1) / 0x080f1b0c→blit_glyph_columns_to_buf (rev=2) / 0x0801d70c→render_atk_def_digits_to_buf (rev=1) / 0x0801d7d0→draw_atk_def_label_to_vram (rev=1) / 0x080f54e0→count_bytes_until_null (rev=1) / 0x0801d830→render_card_level_text_to_buf (rev=2) / 0x080ef454→lookup_level_glyph_index (rev=1) / 0x0801d92c→draw_card_level_label_to_vram (rev=1) / 0x080ef2cc→resolve_card_type_icon_ptr (rev=1) / 0x080edf00→upload_tile_and_palette_from_struct (rev=2); 单 Ghidra session (15 [ok]) + 1 build + sha1 9689337d 一致; 已分析 18.15% (47/259). 里程碑: 突破 18%, card_image_decode_wrapper 完整子调用簇落地.

## BLOCKED 追踪

| SB 编号 | 日期 | 阻塞原因 | 解除前置条件 |
|---------|------|----------|-------------|
| SB-080fa4dc-1 | 2026-05-02 | r3 assert_type 枚举语义需 debug build 验证 (函数命名本身已 PASSED) | 找到 debug build 或匹配工程的 assert 宏定义 |
| SB-080f5e98-1 | 2026-05-02 | 条目 +5 / +1 的 bit mask 操作语义需 mGBA 在 scene_card_list 初始化时 dump gPrng+0x1bc 所指内存结构 (before/after) 确认 | mGBA 断点 FUN_080f5ef4 入口，dump [gPrng+0x1bc] before/after 各条目的 +5/+1 字节变化 |

> 格式: `SB-<ADDR>-<N> | <YYYY-MM-DD> | <阻塞原因> | <解除前置条件>`

## 失败追踪 (auto-skip)

> fixer 在 byte-identical ❌ / MAX_ITER / agent 求助 / 完全无法命名 时追加。
> pick_batch.py 自动:
>   - 排除 ADDR 在本表的函数 (本身失败)
>   - 排除直接 callee 含本表 ADDR 的函数 (cascade SKIP, 因 R7 无法满足)
>   - 函数列表对应行标 ⚠ FAIL / ⏭ SKIP

| ADDR | 日期 | 失败原因 | 备注 |
|------|------|----------|------|
| _(空)_ | — | — | — |

> 格式: `0x<ADDR> | <YYYY-MM-DD> | BUILD_FAIL/MAX_ITER/AGENT_HELP/UNNAMABLE | <一句话 why>`