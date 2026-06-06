# Refine Proposal: Seg-7  [0x08018774..0x08019a58)

## 段测绘

- 函数入口: 28 个函数 (全新, 无旧覆盖)

| addr | name |
|---|---|
| 0x08018774 | refresh_selected_char_obj_tile (Seg-6b 已细化, 跳过) |
| 0x080187e0 | append_banlist_input_char |
| 0x08018838 | delete_banlist_name_last_char |
| 0x08018884 | dispatch_name_input_key_by_state |
| 0x08018938 | tick_name_input_frame |
| 0x08018d3c | tick_oam_palette_fade_settings |
| 0x08018d60 | tick_name_input_oam_fade |
| 0x08018db8 | tick_name_input_cursor_sprite |
| 0x08018e30 | signal_name_input_exit |
| 0x08018e50 | tick_name_input_oam_and_scrollbar |
| 0x08018f7c | tick_name_input_render_by_state |
| 0x08019494 | name_input_page_tick |
| 0x080194ec | name_input_page_exit |
| 0x0801950c | commit_input_name_to_buf |
| 0x08019540 | dispatch_name_input_confirm_state |
| 0x08019554 | write_name_input_mode_flag |
| 0x08019574 | page_state_dispatcher |
| 0x080195fc | extract_char_entry_by_lang |
| 0x08019660 | init_banlist_pass_input_scene |
| 0x08019700 | dispatch_text_render_by_mode_banlist |
| 0x080197cc | return_noop_text_variant |
| 0x080197d0 | invoke_noop_text_variant_zero |
| 0x080197dc | init_font_jp_ctx_bg2_char_vram |
| 0x08019820 | init_font_jp_ctx_bg_vram_text |
| 0x08019864 | setup_font_jp_ctx_obj_vram_row_banlist |
| 0x080198d8 | fill_bg0_tilemap_pass_input |
| 0x0801990c | append_col_padded_text_to_buf |
| 0x08019964 | load_game_str_pair_1036_to_pass_buf |
| 0x080199fc | load_game_str_1038_to_pass_buf |
| 0x08019a58 | encode_pass_table_entry_to_line_buf (Seg-8 境界参考函数, 不在本段) |

注: refresh_selected_char_obj_tile (0x08018774) 已在 Seg-6b 完成 (gState/name_char_tile_slot_table 等槽已符号化), 跳过重复处理.
函数总计: 28 (Seg-7 境界内, 含 refresh_selected_char_obj_tile 1 个已完成).

- 残留自动名槽 (DAT_/DWORD_):
  - append_banlist_input_char: DAT_080187fc (gState), DAT_08018800 (0x31e), DAT_08018804 (0x31f), DAT_08018834 (0x2c2)
  - delete_banlist_name_last_char: DAT_08018850 (gState), DAT_08018854 (0x2c2), DAT_08018880 (0x09e3b0b0)
  - dispatch_name_input_key_by_state: DAT_080188c4 (gState), DAT_080188cc (0x315), DAT_0801892c (0x316)
  - tick_name_input_frame: DAT_0801898c (gState), DAT_08018994 (0x315), DAT_08018a24/a30/a5c/a74 (×4, 0xfffffc3f), DAT_08018bb0 (0xfffc3fff), DAT_08018bb4 (0x315), DAT_08018bb8 (0x316), DAT_08018bbc (0xfffffc3f), DAT_08018b40 (0x815b), DAT_08018b50 (0x8160), DAT_08018d2c (0x31e), DAT_08018d30 (0x31f), DAT_08018d34 (0xfffffc3f), DAT_08018d38 (0x316)
  - tick_oam_palette_fade_settings: DAT_08018d54 (gState), DAT_08018d58 (0x2be), DAT_08018d5c (0x05000202)
  - tick_name_input_oam_fade: DAT_08018db0 (gState), DAT_08018db4 (0x315)
  - tick_name_input_cursor_sprite: DAT_08018e1c (gState), DAT_08018e20 (EWRAM_BASE), DAT_08018e24 (GSETTINGS_OFF), DAT_08018e28 (0x31e), DAT_08018e2c (0x31f)
  - signal_name_input_exit: DAT_08018e4c (gState)
  - tick_name_input_oam_and_scrollbar: DAT_08018f68 (gState), DAT_08018f6c (0x31b), DAT_08018f70 (0x09e587ec=name_char_tile_slot_table), DAT_08018f74 (0x321), DAT_08018f78 (0x322)
  - tick_name_input_render_by_state: DAT_08018fa4 (gState), DAT_08018fa8 (0x319), DAT_08019070 (0x01000020), DAT_08019074 (NAME_INPUT_BG0_SCREEN_CLEAR_CTRL 0x01000200), DAT_0801907c (0x31d), DAT_0801908c (0x2878), DAT_08019090 (0xffff9fff), DAT_08019094 (0x323), DAT_080190d0 (0x09e399d0=trig_table), DAT_080190d4 (0x31d), DAT_08019220 (0x06000020=BG_VRAM_TEXT_BASE), DAT_08019224 (0x01000840), DAT_08019228 (0x1009), DAT_0801922c (EWRAM_BASE), DAT_08019230 (GSETTINGS_OFF), DAT_0801923c (0x100a), DAT_08019240 (0x100b), DAT_080192a4 (0x09e3b4a4), DAT_080192a8 (0x323), DAT_08019370 (0x06000020), DAT_08019374 (0x01000840), DAT_08019378 (0x01000040), DAT_0801937c (0x319), DAT_080193bc (0x09e399d0=trig_table), DAT_080193d8 (0x319), DAT_08019480 (0xffff9fff), DAT_08019488 (0x316), DAT_0801948c (0x319), DAT_08019490 (0x09e587ec=name_char_tile_slot_table)
  - name_input_page_tick: DAT_080194ac (gState), DAT_080194b0 (0x316)
  - name_input_page_exit: DAT_08019500 (gState), DAT_08019504 (0x2c2), DAT_08019508 (0x0300025a)
  - commit_input_name_to_buf: DAT_08019534 (gState), DAT_08019538 (0x2c2), DAT_0801953c (0x31e)
  - dispatch_name_input_confirm_state: DAT_08019550 (0x09e3b4a8)
  - write_name_input_mode_flag: DAT_08019570 (0x23a=gPrng+0x23a offset)
  - page_state_dispatcher: DAT_080195dc (gState), DAT_080195e0 (0x31f), DAT_080195e4 (0xffc03fff), DAT_080195f8 (0xffc03fff)
  - extract_char_entry_by_lang: DAT_08019628 (EWRAM_BASE), DAT_0801962c (GSETTINGS_OFF)
  - init_banlist_pass_input_scene: DWORD_080196e8 (0x0500019e), DWORD_080196ec (0x1d0d), DWORD_080196f0 (0x1f0f), DWORD_080196f8 (0x23a=gPrng+0x23a offset), DWORD_080196fc (0x66e=gState+0x66e offset)
  - init_font_jp_ctx_bg2_char_vram: DWORD_08019818 (0x02006ed0=gFontJpCtx)
  - init_font_jp_ctx_bg_vram_text: DWORD_08019858 (0x06000020), DWORD_0801985c (0x02006ed0=gFontJpCtx)
  - setup_font_jp_ctx_obj_vram_row_banlist: DAT_080198c4 (OBJ_TILE_VRAM_BASE), DAT_080198c8 (0x02006ed0=gFontJpCtx), DAT_080198cc (EWRAM_BASE), DAT_080198d0 (GSETTINGS_OFF)
  - fill_bg0_tilemap_pass_input: DAT_08019908 (0x0202348c=gTextEncodingOverride)
  - load_game_str_pair_1036_to_pass_buf: DAT_080199e4 (0x1036), DAT_080199ec (EWRAM_BASE), DAT_080199f0 (GSETTINGS_OFF), DAT_080199f8 (0x1037)
  - load_game_str_1038_to_pass_buf: DAT_08019a44 (0x1038), DAT_08019a4c (EWRAM_BASE), DAT_08019a50 (GSETTINGS_OFF)

  合计 DAT_/DWORD_ 残留: ~75 槽 (含复用已有常量/全局 label 的槽)

- ROM_INCBIN / .byte 块:
  - ROM_INCBIN 0x19640, 0x20 (32B) @ asm line 13162, addr 0x08019640

## 数据块分类 (Rule 2/3) -- 必做 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x08019640 sz=0x20 | raw=0 thumb(entry 0x08019641)=0; 内部 0x08019650 raw=1 (in graphics blob 0x08671310, 偶合) | §5.1 | THUMB 代码体 (push/ldrb/ands/rsbs/bx_lr = get_settings_language_id 变体) + literal pool (EWRAM_BASE/GSETTINGS_OFF), 但函数 entry 0x08019641 count=0; 内部 raw ref at 0x08671310 是 ROM 图形 blob 内的偶合数值, 非真实函数调用; 全 ROM 0 外部引用 |

证据细节:
```
python -c "
import struct; d=open('roms/2343.gba','rb').read()
# entry: 0x08019641 (THUMB)
print(d.count(struct.pack('<I', 0x08019641)))  # -> 0
# raw: 0x08019640
print(d.count(struct.pack('<I', 0x08019640)))  # -> 0
# interior 0x08019650: raw=1 at 0x671310 (graphics blob, not code ptr)
"
```
结论: §5.1 登记 (孤儿 THUMB 叶函数 + literal pool, 无外部调用).

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 标注复用/新建)

| 槽地址 | 值 | const_name | inc 文件 | 备注 |
|---|---|---|---|---|
| DAT_08018a24/a30/a5c/a74 + DAT_08018bbc + DAT_08018d34 (×6) | 0xfffffc3f | NAME_INPUT_MODE_CLEAR | name_input.inc 追加 | 新建: bits[9:6] clear mask for mode field @ gState+0x314 halfword; tick_name_input_frame 多处 ands+orrs 模式 |
| DAT_08018bb0 (×1) | 0xfffc3fff | NAME_INPUT_STATE_FIELD_CLEAR | name_input.inc 追加 | 新建: bits[17:14] clear mask for gState+0x316 bits[17:14] sub-mode field |
| DAT_080195e4/f8 (×2) | 0xffc03fff | NAME_INPUT_PAGE_STATE_CLEAR | name_input.inc 追加 | 新建: bits[21:14] clear mask for page_state field @ gPrng+0x204; page_state_dispatcher 用 |
| DWORD_080196e8 (×1) | 0x0500019e | BANLIST_PASS_BUF_CLEAR_CTRL | name_input.inc 追加 | 新建: bios_cpu_set fill+32bit 0x19e=414 words=1656B, zeros gBanlistPasswordBuffer |
| DWORD_080196ec (×1) | 0x00001d0d | BANLIST_PASS_BG1CNT_VAL | name_input.inc 追加 | 新建: BG1CNT init val for pass_input scene (scrbase=29, charbase=3, 256col) |
| DWORD_080196f0 (×1) | 0x00001f0f | BANLIST_PASS_BG3CNT_VAL | name_input.inc 追加 | 新建: BG3CNT init val for pass_input scene |
| DAT_08019070 (×1) | 0x01000020 | BANLIST_NAME_BG1_SCREEN_CLEAR_CTRL | name_input.inc 追加 | 新建: bios_cpu_fast_set fill 0x20 halfwords (64B) -> BG1 screen partial clear in tick_name_input_render case0 |
| DAT_08019074 (×1) | 0x01000200 | NAME_INPUT_BG0_SCREEN_CLEAR_CTRL | name_input.inc 复用 (Seg-5d 已建) | 复用: 同 Seg-5d 已建常量 |
| DAT_08019224/08019374 (×2) | 0x01000840 | BANLIST_PASS_BG0_SCREEN_CLEAR_CTRL | name_input.inc 追加 | 新建: bios_cpu_fast_set fill 0x840 halfwords (4224B=BG0 screen 32x32 tiles) for pass_input |
| DAT_08019378 (×1) | 0x01000040 | BANLIST_PASS_BG1_SCREEN_PARTIAL_CTRL | name_input.inc 追加 | 新建: bios_cpu_fast_set fill 0x40 halfwords (128B) -> BG1 screen row in case5 |

| DAT_08019220/DAT_08019370/DWORD_08019858 (×3) | 0x06000020 | BG_VRAM_TEXT_BASE | gba_mem.inc 追加 | **reviewer C13 补**: BG VRAM base+0x20 (tile 1), 全 ROM 6 refs; 槽名 `<func>_bg_vram_text_base` (!= 常量名); tick_name_input_render_by_state case2/case5 + init_font_jp_ctx_bg_vram_text |

EQ_SLOTS 合计: 13 槽 / 10 新常量 (1 复用) — (reviewer C13 +3 槽 / +1 常量 BG_VRAM_TEXT_BASE)

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM 全局 or carve label)

| 槽地址 | target | gas_label | slot_label | 证据 file:line |
|---|---|---|---|---|
| DAT_080187fc/08018850/080188c4/0801898c/08018d54/08018db0/08018e1c/08018e4c/08018f68/08018fa4/080194ac/08019500/08019534/080195dc (×14) | 0x02029250 | gState | \<func\>_ptr_gstate | ewram.inc:163 (gState=0x02029250); asm/00_system_str_vija.s 各函数入口处直接读该地址操作名字输入状态结构 |
| DAT_08018e20/DAT_0801922c/DAT_080199ec/DAT_08019a4c/DAT_080198cc/DAT_080198d0(EWRAM_BASE 部分) (×7) | 0x02000000 | EWRAM_BASE | \<func\>_ewram_base | gba_mem.inc (EWRAM_BASE=0x02000000, Seg-5d 追加) |
| DAT_08018e24/DAT_08019230/DAT_080199f0/DAT_08019a50 + DAT_080198d0(GSETTINGS_OFF 部分) (×7) | 0x00006c2c | GSETTINGS_OFFSET | \<func\>_gsettings_offset | name_input.inc (GSETTINGS_OFFSET=0x6c2c, Seg-5d 建) |
| DWORD_08019818/DWORD_0801985c/DAT_080198c8 (×3) | 0x02006ed0 | gFontJpCtx | \<func\>_ptr_font_jp_ctx | ewram.inc:169 (gFontJpCtx=0x02006ed0, Seg-5d 追加) |
| DAT_080198c4 (×1) | 0x06010000 | OBJ_TILE_VRAM_BASE | setup_font_jp_ctx_obj_vram_row_banlist_obj_tile_vram_base | gba_mem.inc (OBJ_TILE_VRAM_BASE=0x06010000, batch-3 建) |
| DAT_08018f70/DAT_08019490 (×2) | 0x09e587ec | name_char_tile_slot_table | \<func\>_ptr_char_tile_slot_table | asm/00_system_str_vija.s Seg-6a carve A label 定义; rom.s 中有 name_char_tile_slot_table: 标签 |
| DAT_080190d0/DAT_080193bc (×2) | 0x09e399d0 | trig_table | \<func\>_ptr_trig_table | asm/00_system_str_vija.s batch-7 carve, rom.s 中有 trig_table: 标签 |
| DAT_08019908 (×1) | 0x0202348c | gTextEncodingOverride | fill_bg0_tilemap_pass_input_ptr_text_enc_override | ewram.inc:18 (gTextEncodingOverride=0x0202348c); fill_bg0_tilemap_pass_input 写 1 = init-complete flag (与 gTextEncodingOverride 同址, 双重语义: TCG/OCG 覆盖 + pass_input init 标志) |
| DAT_080192a4 (×1) | 0x09e3b4a4 | name_input_render_param_4b | tick_name_input_render_by_state_ptr_render_param | **driver 订正**: 0x09e3b4a4 **不是** cursor_anim_data_a (后者 Seg-6b carve 在 0x09e3b46f, 12B, 终 0x09e3b47b)。0x09e3b4a4 是独立 4B 数据块 (ROM 字节 `38 84 88 84`), 落 Seg-6b 余留 incbin 0x1E3B498,0x10EC 内; tick_name_input_render_by_state memcpy 4B src。**新 carve** (见 carve K) |
| DAT_08019550 (×1) | 0x09e3b4a8 | name_input_default_name | dispatch_name_input_confirm_state_ptr_default_name | **driver 解 BLOCKED**: SJIS "\x82\xc4\x82\xb7\x82\xc6" = ていすと→"てすと"(test), commit 源默认名字串; raw=1 ref; 落同一 Seg-6b 余留 incbin。**新 carve** (见 carve K), label+incbin-span byte-safe (语义=默认名, 不需结构化 SJIS) |
| DAT_08018880 (×1) | 0x09e3b0b0 | name_char_group_36 | delete_banlist_name_last_char_ptr_char_group_36 | **driver 解 BLOCKED (item 2)**: 0x09e3b0b0 = **Seg-6a 已 carve 的 name_char_group_36** (rom.s line 959-960 `name_char_group_36: .incbin 0x1E3B0B0,0x4`); raw=5 (4 来自 name_char_group_ptr_table 的重复 entry [36][38][48][49] + 1 code)。Seg-7 仅需 DATA ref 到现有 label, 不重复 carve |
| PTR_name_input_state_table_080195d4 (已 PTR_ 标注) | 0x09e588b8 | name_input_state_table | (保持现名 PTR_name_input_state_table_) | asm/00_system_str_vija.s:13097 已有 PTR_name_input_state_table_ label + .word name_input_state_table; 需 carve 进 rom.s |
| DAT_08019b28 (×1, Seg-8 函数 encode_pass_table_entry_to_line_buf 中) | 0x09e588cc | banlist_pass_char_group_ptr_table | (Seg-8 slot, 提前规划 carve) | 0x09e588cc = name_input_state_table + 0x14, 首个 banlist_pass 字符组指针; encode_pass_table_entry_to_line_buf 直接用 0x09e588cc[0..7] 索引 8 个字符组 ROM 指针 |

REF_SLOTS 合计: ~32 槽

### RENAME_SLOTS (纯改名 + EOL)

以下 DAT_/DWORD_/PTR_ 槽改名为函数特定 label (格式 \<func\>_\<semantic\>):

**gPrng 指针槽** (PTR_gPrng_* 已有 PTR_ 前缀, 改为 \<func\>_ptr_gprng):
| 旧名 | 新名 |
|---|---|
| PTR_gPrng_080188c8 | dispatch_name_input_key_by_state_ptr_gprng |
| PTR_gPrng_08018990 | tick_name_input_frame_ptr_gprng_a |
| PTR_gPrng_08018b3c | tick_name_input_frame_ptr_gprng_b |
| PTR_gPrng_08018b00 | tick_name_input_frame_ptr_gprng_c |
| PTR_gPrng_08018c2c | tick_name_input_frame_ptr_gprng_d |
| PTR_gPrng_08018d28 | tick_name_input_frame_ptr_gprng_e |
| PTR_gPrng_080192ac | tick_name_input_render_by_state_ptr_gprng |
| PTR_gPrng_080195d8 | page_state_dispatcher_ptr_gprng |
| PTR_gPrng_0801956c | write_name_input_mode_flag_ptr_gprng |
| DWORD_080196f4 (=gPrng via DWORD_ label) | init_banlist_pass_input_scene_ptr_gprng |

**gState field offset 槽** (rename to \<func\>_\<field\>_offset):
| 旧名 | 值 | 新名 | EOL |
|---|---|---|---|
| DAT_08018800/0801898c_a | 0x31e | append_banlist_input_char_char_count_offset | gState+0x31e: current char count |
| DAT_08018804 | 0x31f | append_banlist_input_char_char_limit_offset | gState+0x31f: max char limit |
| DAT_08018834/08018854/08019504/08019538 | 0x2c2 | \<func\>_name_buf_offset | gState+0x2c2: name input byte buffer base |
| DAT_08018994/DAT_08018bb4 | 0x315 | tick_name_input_frame_cursor_field_a/b_offset | gState+0x315: cursor pos/type field |
| DAT_0801892c/08018bb8 | 0x316 | \<func\>_input_mode_flag_offset | gState+0x316: input mode flag byte |
| DAT_08018d58 | 0x2be | tick_oam_palette_fade_settings_palette_src_offset | gState+0x2be: source palette data offset |
| DAT_08018db4 | 0x315 | tick_name_input_oam_fade_cursor_field_offset | gState+0x315 |
| DAT_08018e28 | 0x31e | tick_name_input_cursor_sprite_char_count_offset | gState+0x31e |
| DAT_08018e2c | 0x31f | tick_name_input_cursor_sprite_char_limit_offset | gState+0x31f |
| DAT_08018f6c | 0x31b | tick_name_input_oam_and_scrollbar_jp_flag_offset | gState+0x31b: JP mode flag |
| DAT_08018f74 | 0x321 | tick_name_input_oam_and_scrollbar_col_a_offset | gState+0x321: cursor column field a |
| DAT_08018f78 | 0x322 | tick_name_input_oam_and_scrollbar_col_b_offset | gState+0x322: cursor column field b |
| DAT_08018fa8 | 0x319 | tick_name_input_render_by_state_state_field_offset | gState+0x319: render sub-state bits[7:4] |
| DAT_0801907c | 0x31d | tick_name_input_render_by_state_scroll_step_offset | gState+0x31d: BG scroll step counter |
| DAT_08019094 | 0x323 | tick_name_input_render_by_state_lang_cfg_offset_a | gState+0x323: language config byte |
| DAT_080190d4 | 0x31d | tick_name_input_render_by_state_scroll_step_offset_b | same field 2nd ref |
| DAT_08019228 | 0x1009 | tick_name_input_render_by_state_str_id_a | game_str ID 0x1009 |
| DAT_0801923c | 0x100a | tick_name_input_render_by_state_str_id_b | game_str ID 0x100a |
| DAT_08019240 | 0x100b | tick_name_input_render_by_state_str_id_c | game_str ID 0x100b |
| DAT_080192a8 | 0x323 | tick_name_input_render_by_state_lang_cfg_offset_b | gState+0x323 2nd ref |
| DAT_0801937c | 0x319 | tick_name_input_render_by_state_state_field_offset_b | gState+0x319 2nd ref |
| DAT_080193d8 | 0x319 | tick_name_input_render_by_state_state_field_offset_c | gState+0x319 3rd ref |
| DAT_08019488 | 0x316 | tick_name_input_render_by_state_mode_flag_offset | gState+0x316 |
| DAT_0801948c | 0x319 | tick_name_input_render_by_state_state_field_offset_d | gState+0x319 4th ref |
| DAT_080194b0 | 0x316 | name_input_page_tick_mode_flag_offset | gState+0x316 |
| DAT_080195e0 | 0x31f | page_state_dispatcher_char_code_offset | gState+0x31f: writes r5 (char code) here |
| DAT_0801953c | 0x31e | commit_input_name_to_buf_char_count_offset | gState+0x31e |
| DAT_08019570 | 0x23a | write_name_input_mode_flag_prng_mode_offset | gPrng+0x23a: name_input mode flag byte |
| DWORD_080196f8 | 0x23a | init_banlist_pass_input_scene_prng_mode_offset | gPrng+0x23a 2nd ref |
| DWORD_080196fc | 0x66e | init_banlist_pass_input_scene_gstate_total_offset | gState+0x66e: banlist total count field |

**misc 槽**:
| 旧名 | 值 | 新名 | EOL |
|---|---|---|---|
| DAT_08018d5c | 0x05000202 | tick_oam_palette_fade_settings_oam_palram_target | OAM palette RAM slot 1 color 1 address |
| DAT_08018b40 | 0x815b | tick_name_input_frame_sjis_range_lo | SJIS lower boundary for JP input char validation |
| DAT_08018b50 | 0x8160 | tick_name_input_frame_sjis_range_hi | SJIS upper boundary |
| DAT_0801908c | 0x2878 | tick_name_input_render_by_state_win0v_val | WIN0V: top=0x28 bottom=0x78 name-input window |
| DAT_08019090/DAT_08019480 (×2) | 0xffff9fff | \<func\>_dispcnt_bg3_disable_mask | DISPCNT clear bit13 = BG3 off |
| DWORD_080196ec | 0x00001d0d | init_banlist_pass_input_scene_bg1cnt_val | BG1CNT init val (equate 同时改名槽) |
| DWORD_080196f0 | 0x00001f0f | init_banlist_pass_input_scene_bg3cnt_val | BG3CNT init val |
| DAT_08019508 | 0x0300025a | name_input_page_exit_committed_name_buf | IWRAM committed name destination (gPrng+0x21a; only 1 ref) |
| DAT_080199e4 | 0x00001036 | load_game_str_pair_1036_to_pass_buf_str_id_a | game_str ID 0x1036 |
| DAT_080199f8 | 0x00001037 | load_game_str_pair_1036_to_pass_buf_str_id_b | game_str ID 0x1037 |
| DAT_08019a44 | 0x00001038 | load_game_str_1038_to_pass_buf_str_id | game_str ID 0x1038 |
| DAT_08018880 | 0x09e3b0b0 | (改为 REF: delete_banlist_name_last_char_ptr_char_group_36 → name_char_group_36) | driver 解: 见 REF_SLOTS 表 (Seg-6a 已 carve) |

**reviewer C13 补 4 个 gState-offset 残留槽**:
| 旧名 | 值 | 新名 | EOL |
|---|---|---|---|
| DAT_080188cc | 0x315 | dispatch_name_input_key_by_state_key_type_offset | gState+0x315: key type field bits[5:2] |
| DAT_08018d2c | 0x31e | tick_name_input_frame_char_count_offset_f | gState+0x31e: current char count (lit-pool tail) |
| DAT_08018d30 | 0x31f | tick_name_input_frame_char_limit_offset_f | gState+0x31f: max char limit |
| DAT_08018d38 | 0x316 | tick_name_input_frame_mode_flag_offset_c | gState+0x316: input mode flag byte |

RENAME_SLOTS 合计: ~49 槽 (含 reviewer C13 +4; DAT_08018880 移至 REF)

### FUNC_RENAME (误名订正)

0 个候选. 所有函数名与函数体语义一致:
- init_banlist_pass_input_scene: 初始化禁卡密码输入场景 (清 gBanlistPasswordBuffer / GL init / IO 寄存器), 名称准确.
- extract_char_entry_by_lang: 按语言模式提取字符条目 (1 或 2 字节), 名称准确.
- dispatch_name_input_confirm_state: thin wrapper 设置 char_code 后调 page_state_dispatcher, 名称准确.
- page_state_dispatcher: 通用页面状态分派器 (读 gPrng+0x204 page_state 索引 name_input_state_table), 名称准确.
- 其余函数名与体一致, 无误名信号.

### PLATE (R5; 订正过时 FUN_ 或 CJK 文本)

1. tick_name_input_oam_and_scrollbar (0x08018e50):
   - 现 plate 含 CJK 中文 (ASM 末尾注释). 判断: plate 已含 ASCII 大量描述, CJK 为补充说明.
   - 动作: 将 plate 中任何 CJK 字符清除或改写为 ASCII 描述. 置信度: high (文件 asm/00_system_str_vija.s:12140).

2. tick_name_input_frame (0x08018938):
   - 现 plate 含 CJK (gPrng+0x314/0x315/0x316 字段说明). 同样须清除 CJK.
   - 动作: 重写为纯 ASCII, 保留关键字段偏移数值.

3. tick_name_input_render_by_state (0x08018f7c):
   - 现 plate 含 CJK. 同样重写为纯 ASCII.

4. load_banlist_password_table_from_rom (0x08019c48, 在 Seg-8 边界前):
   - plate 已纯 ASCII, 无需修改.

PLATE 合计: 3 函数 plate CJK 清除重写.

## carve 计划 (R7)

### carve J: name_input_state_table + banlist_pass_char_group_ptr_table

- **地址**: 0x09e588b8 (ROM file offset 0x1E588B8)
- **host incbin**: `.incbin 0x1E588B8, 0x454` (Seg-6a carve B 余留 incbin)
  - Seg-6a carve B = name_char_group_ptr_table (0x09e587f0, 200B=0xC8)
  - carve B remainder = `.incbin 0x1E588B8, 0x454` (当前现状)
- **内容**: 13 × 4B = 52B = 0x34
  - [0] 0x08017575 = name_input_page_init+1 (THUMB)
  - [1] 0x080180ad = name_input_page_load_assets+1 (THUMB)
  - [2] 0x08019495 = name_input_page_tick+1 (THUMB)
  - [3] 0x080194ed = name_input_page_exit+1 (THUMB)
  - [4] 0x00000000 = NULL sentinel
  - [5..12] 8 × ROM data ptrs (0x09e3bfd4..0x09e3bf80): banlist_pass_char_group_ptr_table
- **GAS 结构**:
```
name_input_state_table:
    .word name_input_page_init+1       @ 0x09e588b8
    .word name_input_page_load_assets+1
    .word name_input_page_tick+1
    .word name_input_page_exit+1
    .word 0                            @ NULL sentinel
banlist_pass_char_group_ptr_table:
    .word 0x09e3bfd4                   @ 0x09e588cc char_group_0
    .word 0x09e3bfc8                   @ char_group_1
    .word 0x09e3bfbc                   @ char_group_2
    .word 0x09e3bfb0                   @ char_group_3
    .word 0x09e3bfa4                   @ char_group_4
    .word 0x09e3bf98                   @ char_group_5
    .word 0x09e3bf8c                   @ char_group_6
    .word 0x09e3bf80                   @ char_group_7
```
- **覆盖等式**: 0x34 (carve) + 0x420 (remainder) = 0x454 = host incbin size. OK.
- **余留 incbin**: `.incbin 0x1E588EC, 0x420`
- **byte 核对** (python):
  - d[0x1E588B8:0x1E588BC] = struct.pack('<I', 0x08017575) -> 75750108 OK (已上方验证)
  - d[0x1E588CC:0x1E588D0] = 0x09e3bfd4 -> d4bfe309 OK
- **代码侧 R3 ref**: 槽 PTR_name_input_state_table_080195d4 (page_state_dispatcher) 已有 DATA ref + label -> 保持. 新增: DAT_08019b28 (encode_pass_table_entry_to_line_buf, Seg-8) -> 在 Seg-8 处理, 此处仅规划 carve.
- **注**: name_input_state_table 在 Ghidra 中已有 USER_DEFINED label (PTR_ 槽已导出), 但 rom.s 中尚未 carve 入块. banlist_pass_char_group_ptr_table 需新建 Ghidra label + DAT_08019b28 DATA ref (Seg-8 处理).

### carve K: name_input_render_param_4b + name_input_default_name (driver 新增, 解原 2 BLOCKED)

- **host incbin**: Seg-6b 余留 `.incbin "roms/2343.gba", 0x1E3B498, 0x10EC` (cursor_anim_data_b 之后)
- 两个被引用地址在此 incbin 内 (均 raw=1, 已 driver ROM 核): 0x09e3b4a4 (off +0xC) / 0x09e3b4a8 (off +0x10)
- **拆分 (label+incbin-span, byte-identical-safe)**:
```
.incbin "roms/2343.gba", 0x1E3B498, 0xC      @ 0x09e3b498..b4a4 (3 word: 0x85/0x121/0x85 anim coords 续)
name_input_render_param_4b:                    @ 0x09e3b4a4 (4B param block 38 84 88 84; render memcpy src)
.incbin "roms/2343.gba", 0x1E3B4A4, 0x4
name_input_default_name:                       @ 0x09e3b4a8 (SJIS "てすと"=test + NUL; commit default name)
.incbin "roms/2343.gba", 0x1E3B4A8, 0x10DC    @ 余 (到原 incbin 尾 0x1E3C584)
```
- **覆盖等式**: 0xC + 0x4 + 0x10DC = 0x10EC = host incbin size. OK (driver 核)。
- code-ref: DAT_080192a4 → name_input_render_param_4b; DAT_08019550 → name_input_default_name。各槽改名。
- 注: 用 incbin-span 保字节 (不结构化 SJIS / 4B 块), byte-identical 保证; 语义 high-conf (てすと=test 默认名 + render 4B param)。

### 0x09e3b0b0 (item 2, 已解): 见上 REF_SLOTS 表 — Seg-6a 已 carve name_char_group_36, Seg-7 仅 DATA ref。

## disasm 计划 (R4)

无 (本段 ROM_INCBIN 唯一块为 §5.1, 不反汇编).

## 新增 constants / 全局 (如有)

**追加 name_input.inc** (已有文件 constants/name_input.inc, Seg-5d 建):
- NAME_INPUT_MODE_CLEAR = 0xfffffc3f  (新, bits[9:6] clear mask)
- NAME_INPUT_STATE_FIELD_CLEAR = 0xfffc3fff  (新, bits[17:14] clear mask)
- NAME_INPUT_PAGE_STATE_CLEAR = 0xffc03fff  (新, bits[21:14] clear mask for page_state)
- BANLIST_PASS_BUF_CLEAR_CTRL = 0x0500019e  (新, gBanlistPasswordBuffer fill ctrl)
- BANLIST_PASS_BG1CNT_VAL = 0x00001d0d  (新)
- BANLIST_PASS_BG3CNT_VAL = 0x00001f0f  (新)
- BANLIST_NAME_BG1_SCREEN_CLEAR_CTRL = 0x01000020  (新)
- BANLIST_PASS_BG0_SCREEN_CLEAR_CTRL = 0x01000840  (新)
- BANLIST_PASS_BG1_SCREEN_PARTIAL_CTRL = 0x01000040  (新)

合计: 9 新常量 追加到 name_input.inc

**不新建其他 constants 文件**: 所有常量都属 name-input/banlist-pass 系统, 归 name_input.inc 合理.

**全局变量**: 0 新增 (EWRAM/IWRAM 全局已在 ewram.inc/iwram.inc 齐全).

## §5.1 登记 (Rule 3) -- 0 引用块

| 地址 | 大小 | 内容初判 | ref-scan 证据 |
|---|---|---|---|
| 0x08019640 | 0x20 (32B) | THUMB 叶函数 (get_settings_language_id 变体): push/ldrb/ands/rsbs/bx_lr + literal pool (EWRAM_BASE=0x02000000 + GSETTINGS_OFFSET=0x00006c2c) | entry 0x08019641 THUMB count=0; raw 0x08019640 count=0; 内部 0x08019650 raw=1 at 0x08671310 (图形 blob, 偶合非代码引用); confidence high |

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 槽/全局 | 消费者 | file:line | 语义 | 置信度 |
|---|---|---|---|---|
| gState+0x315 bits[5:2] (0x315 偏移) | dispatch_name_input_key_by_state | asm/00_system_str_vija.s:11376 (DAT_080188cc = 0x315, ldrb r0,[r2+r1]; lsls#0x1a; lsrs#0x1c) | 按键类型字段 bits[5:2] (0=null/1=confirm/2=del/3=mode_write/4=set_bit6) | high |
| gState+0x31e (CHAR_COUNT_OFF) | append_banlist_input_char | asm/00_system_str_vija.s:11268 (DAT_08018800=0x31e; ldrb r1,[r5]; cmp r1,r0 = cur<limit) | current char count byte | high |
| 0x09e399d0 (trig_table) | tick_name_input_render_by_state case1/case6 | asm/00_system_str_vija.s:12444 (DAT_080190d0 -> ldrsh r1,[r0,r2]; scroll animation via trig lookup) | cos/sin lookup for BG scroll animation | high |
| 0x09e588b8 (name_input_state_table) | page_state_dispatcher | asm/00_system_str_vija.s:13050 (PTR_name_input_state_table_080195d4 -> ldr r0,[r0+state_idx*4]) | page state fn ptr table (4 THUMB fns + NULL) | high |
| 0x0202348c (gTextEncodingOverride) | fill_bg0_tilemap_pass_input | asm/00_system_str_vija.s:13535 (DAT_08019908; strb r0,[r1] -> writes 1 = init-complete AND encoding override flag) | dual-use: pass_input init flag (written 1) + TCG/OCG encoding mode (read elsewhere) | high |
| 0x09e3b4a4 (cursor_anim_data_a region) | tick_name_input_render_by_state case3 | asm/00_system_str_vija.s:12665 (DAT_080192a4 -> memcpy 4B to sp+0x20, used in cell anim rendering) | 4-byte cursor anim param block | med (memcpy target sp-local, runtime layout confirm needed) |

## 求助 (低置信度语义) — 全部 RESOLVED by driver (静态 ROM 核, 无 mGBA)

1. **DAT_08019550 = 0x09e3b4a8** — RESOLVED: SJIS "てすと"(test) 默认名字串, commit 源。**carve K** 出 label
   `name_input_default_name` (label+incbin-span byte-safe)。非 BLOCK。
2. **DAT_08018880 = 0x09e3b0b0** — RESOLVED: = Seg-6a 已 carve `name_char_group_36` (rom.s 959-960);
   5 refs = 4 ptr-table 重复 entry + 1 code。Seg-7 仅 DATA ref 现有 label。非 BLOCK。
3. **driver 订正 executor 误标**: DAT_080192a4=0x09e3b4a4 被 executor 错映射为 cursor_anim_data_a
   (实在 0x09e3b46f)。0x09e3b4a4 是独立 4B 块, **carve K** 出 label `name_input_render_param_4b`。

---

## Executor Report: Seg-7

- 槽: EQ=10 REF=32 RENAME=45 FUNC_RENAME=0 PLATE=3
- carve=1 (name_input_state_table + banlist_pass_char_group_ptr_table, 52B/0x34) disasm=0 §5.1=1 (0x08019640/0x20)
- 新增 constants/全局: name_input.inc 追加 9 常量 (NAME_INPUT_MODE_CLEAR/STATE_FIELD_CLEAR/PAGE_STATE_CLEAR + BANLIST_PASS_BUF_CLEAR_CTRL/BG1CNT_VAL/BG3CNT_VAL + BANLIST_NAME_BG1_SCREEN_CLEAR_CTRL/PASS_BG0_SCREEN_CLEAR_CTRL/PASS_BG1_SCREEN_PARTIAL_CTRL); 无新 EWRAM/IWRAM 全局
- 求助: (1) DAT_08019550=0x09e3b4a8 SJIS 内容语义 (先 RENAME, 后 mGBA 确认); (2) DAT_08018880=0x09e3b0b0 多重 ROM data ref 来源 (先 RENAME, Seg-8/9 确认)
- proposal: doc/dev/refine/Seg-7.proposal.md
