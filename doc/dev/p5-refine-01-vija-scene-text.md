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
| **3** | 0x1d998..0x1e36c (8fn) | ✅ | 1b683a0 |
| **4** | 0x1e36c..0x1e714 (8fn) | ✅ | 3edab63 |
| **5** | **0x1e714..0x1f25c (10fn)** | **✅** | **a13983b** |
| **6** | **0x1f25c..0x20fa8 (16fn, incbin 0x1f4d0/0x690, 0x1fb90/0x302, 0x202fe/0x36, 0x20370/0xa44)** | **✅** | **316bbe7** |
| **7** | **0x20fa8..0x24868 (8fn+68 disasm stubs, incbin 0x2108e/0xbe->disasm, 0x211b4/0xc4, 0x2134c/0x1ae0, 0x22eb8/0x9a6)** | **✅** | **005143e** |
| **8** | **0x24868..0x27e44 (11fn, incbin 0x2497c/0x78->disasm, 0x258f0/0x230->disasm)** | **✅** | **5266f72** |
| **9** | **0x27e44..0x28bdc (8fn+1 disasm, incbin 0x27e50/0x6c->disasm)** | **✅** | **af08e97** |
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

### 4.03 Seg-3 完成记录 (2026-06-07)

- 范围: 0x0801d998..0x0801e36c, 8 fn
- 函数: card_image_decode_wrapper / render_card_name_to_desc_page_vram (误名 card_info_page_step_03_unknown 订正) / tick_scroll_frame_and_update_pos / render_card_description_text / card_info_page_finalize / blit_glyph_2x2_to_bg_vram / tick_blend_fadeout_and_set_dispcnt / tick_blend_fadein_and_poll_done
- Ghidra 脚本: RefineF01Seg3Slots.py (主) + RefineF01Seg3PlateFix.py (邻函数 plate 修正)
- EQ=49 (新建 34 槽: card_info.inc +30, gba_mem.inc +3, gba_io.inc +1; dup 复用 15 槽)
- REF=31 (gFontJpCtx x7 / EWRAM_BASE x4 / GSETTINGS_OFFSET x4 / gCardInfoPageState x8 / gPrng x3 / sjis_char_fold_table x2 / card_attr_order_table x1 / card_type_alt_display_table x1 / card_status_sprite_sheet x1)
- RENAME=1 (blit_glyph_2x2_to_bg_vram_bg_char_vram_cb2 BG_CHAR_VRAM_CB2 复用)
- FUNC_RENAME=1: card_info_page_step_03_unknown -> render_card_name_to_desc_page_vram (误名订正, indeg=2, 函数体=渲染卡名文字到描述页字形行缓冲)
- PLATE=8 (7 个段内函数 CJK->ASCII + 1 个邻函数 update_card_info_page_state 旧名引用订正)
- carve=3: Carve A card_type_alt_display_table@0x09e58ac4 (incbin 前插 label); Carve B card_status_sprite_sheet@0x09e2ddb4 (case_9.bin 前插 label); Carve C card_attr_order_table@0x09e4f204 (分裂 incbin 0x1E4E979/0xB3F -> 0x88B + label + 0x2B4)
- disasm=0 (段内无误标代码)
- §5.1=0 (段内无 ROM_INCBIN 块, ROM 远端数据全 carve)
- 新增 constants: card_info.inc +30 (CARD_TILE_PACK_*/CARD_FRAME_*/CARD_DESC_*/CARD_LEVEL_*/CARD_SPELL_*/CARD_ICON_*/CARD_OVERLAY_TILE_SRC) / gba_mem.inc +3 (BG_SCREEN_TILE_OFF_1/BG_SCREEN_ROW1_OFF/BG_SCREEN_ROW1_TILE1) / gba_io.inc +1 (DISPCNT_BG_OBJ_CLEAR_MASK)
- CSV sync: ExportFunctionInventory (4642 named) + naming-proposals.csv 0x0801dbdc 行更新
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: 1b683a0

### 4.04 Seg-4 完成记录 (2026-06-07)

- 范围: 0x0801e36c..0x0801e714, 8 fn
- 函数: update_card_info_page_state / card_info_page_entry / draw_card_stat_digits_to_oam / draw_stat_row_sprites_to_oam / render_card_stats_oam_for_current_card / card_list_on_select_to_info_page / open_card_info_by_icid / open_card_info_page_from_list
- Ghidra 脚本: RefineF01Seg4Slots.py
- EQ=24 (gCardInfoPageState x7 复用 / EWRAM_BASE x2 复用 / GSETTINGS_OFFSET x2 复用 / 13 新建: CARD_STAT_ATK_DEF_OAM_XY/ATTR2 / CARD_STAT_QPLAY_OAM_XY/ATTR2 / CARD_STAT_DIGIT_OAM_ATTR2 x2 / CARD_STAT_FUSION_OAM_ATTR2 / CARD_STAT_ROW_ATTR2_BASE_A..D / CARD_INFO_STATE_CARD_ID_MASK / CARD_INFO_STATE_CARD_ID_CLEAR)
- REF=0 (无新 carve/全局槽; PTR_ 已符号化)
- RENAME=2 (draw_stat_row_sprites_to_oam_tile_r1 / card_list_on_select_to_info_page_no_stat_sentinel)
- FUNC_RENAME=0 (全 8 函数名准确)
- PLATE=5 (2 CJK->ASCII: card_info_page_entry/card_list_on_select_to_info_page; 3 stale FUN_ 删除: draw_card_stat_digits_to_oam/draw_stat_row_sprites_to_oam/render_card_stats_oam_for_current_card)
- carve=0 / disasm=0 / §5.1=0
- 新增 constants: card_info.inc +13 (CARD_STAT_*/CARD_INFO_STATE_*)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: 3edab63

### 4.06 Seg-6 完成记录 (2026-06-07)

- 范围: 0x0801f25c..0x08020fa8, 16 fn + 4 ROM_INCBIN disasm
- 函数: append_game_text_if_raw / format_int_to_decimal_text / format_game_text_with_text_arg / format_game_text_with_int_arg / check_siocnt_link_ready / read_prng_entry_flag_clear / return_void_noop_stub / return_zero_leaf / return_noop_leaf / return_one_leaf / find_deck_record_index_by_key / find_card_index_in_rom_table / tick_duel_puzzle_scene_step / poll_fadein_exit_to_duel_state / run_duel_puzzle_scene_state_machine / render_lp_record_text_set_a
- Ghidra 脚本: DisassembleF01Seg6Blocks.py + FixF01Seg6LiteralPools.py + FixF01Seg6RestoreCode.py + RefineF01Seg6Slots.py + FixF01Seg6BadRefLabels.py
- disasm R4: 4 blocks
  - Block1 (0x1f4d0/0x690): 596 instructions, 8 case entries (tick_duel_puzzle_scene_step cases 0..7)
  - Block2 (0x1fb90/0x302): 283 instructions, 13 entry points (cases 8..13,20 + sub-dispatch cluster)
  - Block3 (0x202fe/0x36): 20 instructions, fn tick_lp_record_scene_step @ 0x08020300 (med-conf, reviewer decision)
  - Block4 (0x20370/0xa44): 901 instructions, 14 case entries (tick_lp_record_scene_step cases 0..13)
  - Total: 1800 instructions disassembled
- literal pool fix: FixF01Seg6LiteralPools.py (334 createDWord entries) + FixF01Seg6RestoreCode.py (restore 0x0801fbc0 = code+data dual-purpose)
- EQ=21 (GAME_STR_RAW_ID_MASK x3, SIOCNT x1, GPRNG_BANNER_FLAG_OFF x1, gDuelFieldState x1, GL_CLEAR_BITS_17_10 x1, GL_CLEAR_BITS_9_2 x1, EWRAM_BASE x3, GSETTINGS_OFFSET x3, gDuelCardCtxBase x6, gDuelSceneBase x1)
- REF=0 (demoted to RENAME; far ROM targets at 0x098973f6/0x098972f0 lack carve labels)
- RENAME=58 (2 count/data slot renames + 3 tick_duel_puzzle_scene_step + 1 poll_fadein + 50 run_duel_puzzle_scene/render_lp_record_text_set_a including 18 card ID pivots)
- FUNC_RENAME=0 (no existing function renamed)
- PLATE=1 (run_duel_puzzle_scene_state_machine CJK->ASCII, 0x0801fec0)
- carve=0 / §5.1=0 (all 4 blocks have 86-110 refs each, fully disassembled)
- 新建函数: tick_lp_record_scene_step @ 0x08020300 (函数总数 4641->4643)
- 踩坑: flow-based disasm decoded literal pool entries as THUMB instructions; fixed via FixF01Seg6LiteralPools.py (334 DWORDs); 0x0801fbc0 = dual code+data (branch target AND ldr literal), restored as code
- REF label collision: gas_label==slot_label caused .word self-reference; fixed by demoting to RENAME_SLOTS + FixF01Seg6BadRefLabels.py cleanup
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b OK
- commit: 316bbe7

### 4.05 Seg-5 完成记录 (2026-06-07)

- 范围: 0x0801e714..0x0801f25c, 10 fn
- 函数: tick_card_info_page_by_state / get_card_data_format_id / lookup_card_entry_by_index / load_card_fs_entry_to_struct / fill_card_fs_display_entries / fill_card_fs_display_entries_for_card_list / tick_duel_field_main_frame / dispatch_card_display_op / play_ui_effect / copy_game_text_if_raw
- Ghidra 脚本: RefineF01Seg5Slots.py
- EQ=50 (11 新全局: gDuelFieldState/gFontState/gDuelCtx/gDuelCardCtxBase/gCardFsDataBlock/gCardIdCache/gCardListDisplayBuf/gZoneActivTable[med]/gDuelSceneBase/gCardCtxSlotData/gP1ZoneHandCount; 11 偏移常量: DUEL_FIELD_FADEIN_FLAG_OFF/DUEL_FIELD_PRNG_ANIM_FLAG_OFF/DUEL_FIELD_STATE_226_OFF/DUEL_CTX_ZONE_STATE_OFF/GPRNG_PRNG_STATE_OFF213/GPRNG_PRNG_STATE_OFF217/GPRNG_BANNER_FLAG_OFF/P1LP_BLOCK2_OFF/P1LP_TIMER_OFF/PLAYER_BLOCK_STRIDE/GAME_STR_RAW_ID_MASK; 28 reuse)
- RENAME=12 (6 PTR_gPrng + PTR_gP1LifePoints + DAT_0801f0b8/f1a4/f154 + 2 C13: DAT_0801e744/DAT_0801eb3c)
- REF=3 (card_deck_fs_path_table + 2 jump table base ptrs)
- FUNC_RENAME=0
- PLATE=1 (play_ui_effect CJK->ASCII, 789 chars)
- carve=1: card_deck_fs_path_table@0x09e58b08 (rom.s card_type_alt_display_table incbin 拆 0x44+label+0x204=0x248; byte-identical)
- disasm=0 / §5.1=0 (段内无 ROM_INCBIN 块)
- 新增 constants: ewram.inc +11 全局 + 11 偏移/掩码常量
- 命名裁定: gDuelFieldState=0x02023130 (不改 gDuelFieldCtx; driver 裁定; reviewer 指出 asm/07 plate 非正式用同名于 0x0201bb90/0x0201b290, 但该地址无 .equ 定义; 0x02023130 用 gDuelFieldState 与现有 ewram.inc 无碰撞)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: a13983b

### 4.07 Seg-7 完成记录 (2026-06-10)

- 范围: 0x08020fa8..0x08024868, 9 named fn + 68 disasm stubs (FUN_08021090 + block2/3/4)
- 函数 (named): render_lp_record_text_set_b / tick_scene_step_by_step_table_d / fetch_duel_next_state_overflow_exit / draw_decimal_with_offset / render_centered_text_to_bg_vram / copy_icon_tile_to_vram_row / init_duel_field_icon_and_bg_vram / render_win_count_digits_to_oam / render_opp_wins_display_oam
- Ghidra 脚本: RefineF01Seg7Slots.py + DisassembleF01Seg7Blocks.py + FixF01Seg7OrphanBlock.py + FixF01Seg7LiteralPools.py + FixF01Seg7LiteralPools2.py + FixF01Seg7AllLiteralPools.py
- EQ=67 (EWRAM_BASE x10 reuse / GSETTINGS_OFFSET x9 reuse / gFontJpCtx x3 reuse / gVijaState x1 reuse / OBJ_TILE_VRAM_BASE x3 reuse / BG_CHAR_VRAM_CB2 x2 reuse / OBJ_PALRAM_BASE x1 reuse + CARD_DESC_BG_VRAM_A x1 reuse; new: GPRNG_STEP_IDX_OFF/GPRNG_FRAME_CTRL_OFF_203/OBJ_PAL_SLOT_1/DUEL_FIELD_CTRL_VAL/DUEL_FIELD_BGCNT1/2/3_INIT/OBJ_TILE_VRAM_BASE_PAGE2/GWINS_BASE_OFFSET/GWINS_BASE_OFF_2/OPP_WIN_DIGIT_TILE_BASE/OPP_WIN_SPRITE_OFFSCREEN_XY/OPP_WIN_SEPARATOR_TILE_IDX/GUNLOCKED_DUELISTS_OFFSET/DUEL_FIELD_TEXT_TILE_POS_A/B/C/DUEL_FIELD_TEXT_BG_WIDTH/DUEL_FIELD_TILE_ROW_ARG_A/B/C/DUEL_FIELD_OAM_COORDS_A/B/DUEL_FIELD_OAM_TILE_IDX_A/B/C/DUEL_SCENE_FLAGS_MASK_0F00/DUEL_SCENE_FIELD_OFF_6E48/DUEL_SCENE_FIELD_OFF_6E57/gDuelDispCtx)
- REF=14 (gDuelSceneBase x11 + gDuelCardCtxBase x1 + gDuelDispCtx x1 + PTR_DAT_08022e64 x1)
- RENAME=47 (10 render_lp_record_set_b cid/str ptrs + 6 gfx_src + 6+1+6+6 LP str init_duel A/tile_d/B/C + 3 tile_src_d ptrs + 1 flags_mask + 6 LP str render_opp + 1 step_lut + 2 iwram_ptr)
- FUNC_RENAME=0
- PLATE=1 (draw_decimal_with_offset CJK->ASCII @0x0802387c)
- carve=0 (no rom.s incbin cuts needed)
- disasm=3 ranges: block2 (0x080211b4/0xc4, 2 entry pts) + block3 (0x0802134c/0x1ae0, 51 unique entry pts) + block4 (0x08022eb8/0x9a6, 15 unique entry pts); FUN_08021090 auto-disassembled (was "orphan" but has caller FUN_08023614)
- §5.1=0 (all 4 incbin blocks resolved: orphan disassembled + block2/3/4 R4 disasm; NO zero-ref blocks remain)
- literal pool fix: 997 DWORDs total (FixF01Seg7LiteralPools.py 167 + FixF01Seg7LiteralPools2.py 189 + FixF01Seg7AllLiteralPools.py 997 comprehensive scan; multiple passes required due to interleaved code/data in large block3)
- 新增 constants: constants/duel_field.inc (28 equates: GPRNG_STEP_IDX_OFF/frame_ctrl/OBJ_PAL_SLOT_1/DUEL_FIELD_CTRL_VAL/BGCNT1/2/3_INIT/GWINS_BASE_OFFSET/OFF_2/OPP_WIN_*/GUNLOCKED_DUELISTS_OFFSET/DUEL_FIELD_TEXT_TILE_POS_A/B/C/TEXT_BG_WIDTH/TILE_ROW_ARG_A/B/C/OAM_COORDS_A/B/OAM_TILE_IDX_A/B/C/DUEL_SCENE_FLAGS_MASK/FIELD_OFF_6E48/6E57); gba_mem.inc +1 OBJ_TILE_VRAM_BASE_PAGE2; ewram.inc +1 gDuelDispCtx (med-conf)
- 踩坑: FUN_08021090 was auto-disassembled by Ghidra flow from block4 (not true orphan); block3 (6880B) has 51 stubs with interleaved code+literal-pool requiring 3-pass DWORD fix (FixLiteralPools + FixLiteralPools2 + FixAllLiteralPools comprehensive scan)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: 005143e

### 4.08 Seg-8 完成记录 (2026-06-10)

- 范围: 0x08024868..0x08027e44, 11 named fn
- 函数: check_scene_slot_all_entries_meet_threshold / get_total_challenge_cleared_count / build_field_slot_bitmask / render_text_with_font_type_select / render_card_stats_to_line_buf / render_game_text_with_font_type_a / render_game_text_with_font_type_b / campaign_scene_handler / exit_campaign_scene_with_next_handler / build_campaign_sprite_row_by_type / invoke_build_campaign_sprite_row_type5
- Ghidra 脚本: RefineF01Seg8Slots.py + DisassembleF01Seg8Blocks.py + RefineF01Seg8Block2Pools.py
- EQ=289 (reuse: EWRAM_BASE x65, GSETTINGS_OFFSET x56, GPRNG_STEP_IDX_OFF x26, gDuelSceneBase->REF, gDuelCardCtxBase->REF; new: duel_field.inc +21 GPRNG_STEP_CTR_MASK/SCENE_CTX_ANIM_MASK/CAMPAIGN_BG_TILE_PARAM_A..H/SCENE_CTX_TIMER_CLEAR/GPRNG_FIELD_ANIM_MASK/SCENE_SLOT_*/CAMPAIGN_DUELIST_NAME_ROW_A/B/DRAW_DECIMAL_WIN_LABEL_ARG/DUEL_SCENE_FIELD_OFF_6E58; gba_mem.inc +6 CAMPAIGN_VRAM_BG_TILE_BASE_*/; ewram.inc +9 GPRNG_CHALLENGE_ENTRY_OFF/GSETTINGS_FONT_TABLE_OFF/GSETTINGS_TEXT_FIELD_A/B_OFF/P1LP_BLOCK2_OFF_1CE8/GPRNG_PACK_SCROLL/FRAME_OFF_23D/E/gCampaignDisplayState/gCampaignSpriteCtxBase; card_info.inc +8 LP 阈值常量; iwram.inc +1 IWRAM_OBJ_SCRATCH_BUF)
- REF=36 (gDuelSceneBase x18 + gDuelCardCtxBase x9 + gP1LifePoints x5 + switch table x3 + campaign_step_dispatch_table x1)
- RENAME=353+12 (353 main: 7 render_text_font_select font ptrs + 22 render_game_text_a/b font ptrs + campaign step font ptrs + ~75 render_card_stats 26-pass font ptrs + 1 lp_tier_a_stub label + ~246 campaign step misc slots; 12 block2 pool: rcs_blk2_b0..b5 font5_base/off)
- FUNC_RENAME=0 (全 11 函数名准确)
- PLATE=0 (段内无 CJK plate 残留)
- carve=0
- disasm=2 ranges (block1 0x0802497c/0x78: 15 unique entry pts FUN_08024982..FUN_080249e8; block2 0x080258f0/0x230: 6 unique entry pts FUN_080258f0..FUN_08025ac8) + block2 literal pool guards (6 regions, 24 DWORDs)
- §5.1=0 (两块均有引用: block1 raw=1 from jump table; block2 raw=1 from dispatch table)
- 新增 constants: duel_field.inc +21 / gba_mem.inc +6 / ewram.inc +9 (含 2 globals) / card_info.inc +8 / iwram.inc +1 = 45 total
- 踩坑: block2 (0x080258f0/0x230) 6 stubs 内各有 3-4 DWORD literal pool 嵌在 .byte inline block; 初次 disasm 后 Ghidra 未将其导出为 DWORD 标签 -> GAS "invalid offset, value too big (0xFFFFFFFC)"; 修复: DisassembleF01Seg8Blocks.py 加 _guard_literal_pool(6 regions, 24 DWORDs) 后重跑 disasm + 补 RefineF01Seg8Block2Pools.py 命名; byte-identical 保持不变
- CSV sync: no (FUNC_RENAME=0)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: 5266f72

### 4.09 Seg-9 完成记录 (2026-06-10)

- 范围: 0x08027e44..0x08028bdc, 8 named fn + 1 disasm (tick_campaign_card_select_display_state)
- 函数: invoke_build_campaign_sprite_row_type6 / tick_campaign_card_select_display_state (disasm new) / run_campaign_card_select_handler_0..15 (16 inline fragments) / finalize_campaign_card_select_frame / render_campaign_text_line_centered / render_campaign_text_line_with_align / init_pack_scene_vram_regs / load_pack_tiles_with_palette_init / write_pack_strip_oam_entries / write_pack_grid_oam_by_card_slot / tick_campaign_card_selector_oam
- Ghidra 脚本: DisassembleF01Seg9Block.py (R4 disasm) + RefineF01Seg9Slots.py (EQ/REF/RENAME/PLATE)
- EQ=76+3 disasm = 79 (58 reuse: gPrng x8 / GPRNG_STEP_IDX_OFF x6 / GPRNG_STEP_CTR_MASK x8 / gDuelSceneBase x14 / gDuelCardCtxBase x3 / EWRAM_BASE x6 / GSETTINGS_OFFSET x4 / GSETTINGS_FONT_TABLE_OFF x1 / GSETTINGS_TEXT_FIELD_A_OFF x1 / GPRNG_CHALLENGE_ENTRY_OFF x1 / OAM_ATTR0_HIDDEN x1 / BG_CHAR_VRAM_CB2 x3 / OBJ_TILE_VRAM_BASE x2 / OBJ_PAL_SLOT_1 x1 / DUEL_FIELD_BGCNT1/2/3_INIT x3 / DUEL_FIELD_CTRL_VAL x1 / gFontJpCtx x2 / gVijaState x1 / gDuelDispCtx x1 / BG0CNT x1 / GFX_ATTR_CLEAR_BITS_8_7 x1; 18 new: CAMPAIGN_SIO_CMD_MATCH / CAMPAIGN_CARD_STEP_COPY_MASK / CAMPAIGN_CARD_ANIM_STEP_MASK / GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF / CAMPAIGN_CARD_SPRITE_POS_0..5 / CAMPAIGN_HAND_SPRITE_POS_A..D x2; 3 disasm pool: gPrng/GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF/GPRNG_STEP_IDX_OFF)
- REF=12 (font_jp_base_table x2 / pack_strip_tile_id_table / campaign_oam_slot_count_table / pack_card_grid_tile_table / IWRAM attr buf 0x0300024c / OAM xy coord 0x0060006e / proto_row 0x02001138 / expert/standard/puzzle_challenge_record_array / handler_table_ptr 0x08027ec0)
- RENAME=13 (campaign_card_handler_table_ptr + neg_off_a/b + flag_mask + tile_delta_a/b + mode1_xy_coord + 5x pack_tiles RENAME [Carve G blocked] + campaign_hand_oam RENAME [Carve H blocked] + sp_adj)
- FUNC_RENAME=0
- PLATE=16 (stale name fixes: 16 handler functions updated; PTR_FUN_08027ec0 -> PTR_run_campaign_card_select_handler_0_08027ec0 x19 occurrences / FUN_08028402 -> finalize_campaign_card_select_frame x9 occurrences across 16 handlers)
- carve=6: A: campaign_oam_slot_count_table@0x09e59d38 (0x40B); B: pack_strip_tile_id_table@0x09e59d78 (0x10B); C: pack_card_grid_tile_table@0x09e59d88 (0x20B) [host 0x1E59C2C/0xFD0 -> 5-split]; D: standard_challenge_record_array@0x09e5e620 (0x1ECB); E: expert_challenge_record_array@0x09e5e80c (0x1A4B); F: puzzle_challenge_record_array@0x09e5e9cc (0x24CB) [host 0x1E5E618/0x6BC -> 6-split]
- Carve G/H降级 RENAME: G (pack GFX 5 blobs, asset sizes unknown, host rom.s line 660); H (campaign_hand_oam_array 0x095b7cca, auto-gen file card-image-index.s)
- disasm=1: block 0x08027e50/0x6c -> tick_campaign_card_select_display_state (18 BL callers); literal pool guard 4 DWORDs @0x08027eac..0x08027eb8
- §5.1=0
- 新增 constants: duel_field.inc +14 (CAMPAIGN_SIO_CMD_MATCH/CAMPAIGN_CARD_STEP_COPY_MASK/CAMPAIGN_CARD_ANIM_STEP_MASK/GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF/CAMPAIGN_CARD_SPRITE_POS_0..5/CAMPAIGN_HAND_SPRITE_POS_A..D)
- 新增全局别名: ewram.inc +alias run_campaign_card_select_handler_10_proto_row (=gCardListDisplayBuf=0x02001138); iwram.inc +tick_campaign_card_selector_oam_attr_buf=0x0300024c
- CSV sync: yes (new fn tick_campaign_card_select_display_state @ 0x08027e50 added to naming-proposals.csv)
- byte-identical: SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b ✅
- commit: af08e97

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 01 范围 `[0x0801cb00, 0x0802c238)` (span 0xF738, ~84 named fn, 13 ROM_INCBIN) 按**函数数**
> 均分 10 段 (~8 fn/段, 边界=函数起点)。两个大数据块 (0x2134c/0x1ae0=6880B 在 Seg-7, 0x29170/0x22f0=8944B
> 在 Seg-10) 处理时先 ref-scan 分类 (carve/disasm/§5.1)。逐段 executor→reviewer→fixer, 地址序不回头。

| Seg | 地址范围 | ~fn | 内含 ROM_INCBIN (必 carve/disasm/或 §5.1) | 备注 |
|---|---|---|---|---|
| Seg-1 | 0x1cb00..0x1d448 | 8 | 0x1d024/0x1c | 含 file 00 边界后首函数 run_vija_scene_state_machine |
| Seg-2 | 0x1d448..0x1d998 | 8 | — | |
| Seg-3 | 0x1d998..0x1e36c | 8 | — | ✅ |
| Seg-4 | 0x1e36c..0x1e714 | 8 | — | ✅ |
| Seg-5 | 0x1e714..0x1f25c | 10 | — | ✅ |
| Seg-6 | 0x1f25c..0x20fa8 | 16 | 0x1f4d0/0x690, 0x1fb90/0x302, 0x202fe/0x36, 0x20370/0xa44 | ✅ 4 ROM_INCBIN disasm R4; tick_lp_record_scene_step 新建 |
| Seg-7 | 0x20fa8..0x24868 | 8 | 0x2108e/0xbe, 0x211b4/0xc4, **0x2134c/0x1ae0**, 0x22eb8/0x9a6 | 大数据区 (~6880B 块, ref-scan 分类) |
| Seg-8 | 0x24868..0x27e44 | 11 | 0x2497c/0x78->disasm R4 (15 entries), 0x258f0/0x230->disasm R4 (6 entries) | ✅ |
| Seg-9 | 0x27e44..0x28bdc | 8+1 disasm | 0x27e50/0x6c->disasm R4 | ✅ carve A-F (6 data arrays) |
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
