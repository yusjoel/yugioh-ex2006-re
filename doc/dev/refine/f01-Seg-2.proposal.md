# Refine Proposal: f01-Seg-2  [0x0801d448..0x0801d998)

## 段测绘

- 函数入口: x8 (全 < 0x1d998, 严守上界)
  - 0x0801d448  card_info_page_enter_with_card_id  (push {lr})
  - 0x0801d45c  card_info_page_init_bg0            (push {r4,lr})
  - 0x0801d510  render_card_name_to_line_buf        (push {r4,r5,r6,r7,lr})
  - 0x0801d6b4  draw_card_name_label_to_vram        (push {r4,r5,r6,r7,lr})
  - 0x0801d70c  render_atk_def_digits_to_buf        (push {r4,r5,r6,lr})
  - 0x0801d7d0  draw_atk_def_label_to_vram          (push {r4,r5,r6,r7,lr})
  - 0x0801d830  render_card_level_text_to_buf       (push {r4,r5,r6,r7,lr})
  - 0x0801d92c  draw_card_level_label_to_vram       (push {r4,r5,r6,r7,lr})
- 残留自动名槽:
  - DAT_0801d458 = 0x0201afb0   (card_info_page_enter_with_card_id)
  - DAT_0801d4e8 = 0x06004000   (card_info_page_init_bg0)
  - DAT_0801d4ec = 0x0201afb0
  - DAT_0801d4f4 = 0x00004104   (BGxCNT init value)
  - DAT_0801d4f8 = 0x00000407
  - DAT_0801d4fc = 0x00000305
  - DAT_0801d500 = 0x09ccd290   (name_o_palette_data -- already carve label)
  - DAT_0801d504 = 0x050003e0
  - DAT_0801d508 = 0x05000200   (OBJ_PALRAM_BASE)
  - DAT_0801d5a8 = 0x02006ed0   (gFontJpCtx)
  - DAT_0801d5ac = 0x02000000   (EWRAM_BASE)
  - DAT_0801d5b0 = 0x00006c2c   (GSETTINGS_OFFSET)
  - DAT_0801d5b8 = 0x0201afb0
  - DAT_0801d650 = 0x09e589c4   (sjis_char_fold_table -- inside incbin, see carve plan)
  - DAT_0801d704 = 0x06001840   (card_name OAM tile attr base)
  - DAT_0801d708 = 0x06008200   (sprite VRAM commit base for card name)
  - DAT_0801d7c8 = 0x0984f59c   (label glyph buf -- inside large incbin, see carve plan)
  - DAT_0801d7cc = 0x0984f54c   (digit glyph data -- inside large incbin, see carve plan)
  - DAT_0801d828 = 0x06001c00   (OBJ tile VRAM base for ATK/DEF/Level)
  - DAT_0801d82c = 0x06008580   (sprite VRAM commit base for ATK/DEF)
  - DAT_0801d89c = 0x0984f59c   (same label_glyph_buf as d7c8)
  - DAT_0801d8a0 = 0x09e5f71e   (level_signature_table + 0x2 = rec[0].field_a base)
  - DAT_0801d8f8 = 0x0984f54c   (same digit_glyph as d7cc)
  - DAT_0801d8fc = 0x09e5f726   (level_signature_table + 0xa = rec[0].field_b base)
  - DAT_0801d928 = 0x0984f54c   (same digit_glyph as d7cc, 3rd ref)
  - DAT_0801d94c = 0x06001c00   (same OBJ tile VRAM base as d828)
  - DAT_0801d994 = 0x06008580   (same ATK/DEF sprite VRAM as d82c)
- ROM_INCBIN / .byte 块: 0 (路线图确认, 逐行扫描已确认)

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

路线图标注 "Seg-2: (dash)" -- 无段内 ROM_INCBIN。逐行 grep 已确认: 无 ROM_INCBIN / .byte 数据块
在 [0x0801d448, 0x0801d998) 内。

函数体内 .hword 0x46xx (e.g. 0x4657/0x464e/0x4645/0x4682/0x4689) 是合法 THUMB
high-reg-mov 指令 (MOV rHi,rHi), 非数据块。

---

## 远端 ROM 数据表分类 (代码引用 -- 必须 carve 或确认已 carve)

| 地址 | ref-scan (raw/THUMB) | 现状 | 判定 |
|---|---|---|---|
| 0x09e589c4 (256B) | raw=4 thumb=0 | 在 banlist_handler_table 尾 incbin (0x1E589A4+0x368) 偏移 0x20 处 | carve -- 被 4 处代码引用; 需分裂宿主 incbin |
| 0x0984f54c (~0x80B) | raw=6 thumb=0 | 在 seg-C 大 incbin (0x1832602+0x1E51A) 偏移 0x1cf4a 处 | carve -- 6 refs; 需分裂宿主 incbin |
| 0x0984f59c (~0x80B) | raw=3 thumb=0 | 同上 incbin, 偏移 0x1cf9a | carve -- 3 refs; 与 0x0984f54c 同 host |
| 0x09ccd290 (32B) | raw=15 thumb=0 | name_o_palette_data (rom.s 已有 carve H label) | 复用 -- 已 carve |
| 0x09e5f71e | raw=2 thumb=0 | level_signature_table+0x2 (data/post-banlists-tables.s 已 carve) | 复用 -- 已 carve; 槽改 .word level_signature_table+2 |
| 0x09e5f726 | raw=2 thumb=0 | level_signature_table+0xa (同上) | 复用 -- 已 carve; 槽改 .word level_signature_table+0xa |

carve 0x09e589c4 / 0x0984f54c / 0x0984f59c: 宿主 incbin 分裂操作复杂 (涉及 rom.s 中
banlist_handler_table 尾 incbin 以及 seg-C 大 incbin), 详见下方 "carve 计划"。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

| 槽 (addr) | value | const_name | slot_label | 来源 inc |
|---|---|---|---|---|
| DAT_0801d4e8 | 0x06004000 | BG_CHAR_VRAM_CB2 | card_info_page_init_bg0_vram_char_base | gba_mem.inc **复用** |
| DAT_0801d508 | 0x05000200 | OBJ_PALRAM_BASE | card_info_page_init_bg0_obj_palram_base | gba_mem.inc **复用** |
| DAT_0801d5a8 | 0x02006ed0 | gFontJpCtx | render_card_name_to_line_buf_font_jp_ctx | ewram.inc **复用** |
| DAT_0801d5ac | 0x02000000 | EWRAM_BASE | render_card_name_to_line_buf_ewram_base | gba_mem.inc **复用** |
| DAT_0801d5b0 | 0x00006c2c | GSETTINGS_OFFSET | render_card_name_to_line_buf_gsettings_off | name_input.inc **复用** |
| DAT_0801d4f4 | 0x00004104 | CARD_INFO_BG1CNT_INIT | card_info_page_init_bg0_bg1cnt | 新建 card_info.inc |
| DAT_0801d4f8 | 0x00000407 | CARD_INFO_BG2CNT_INIT | card_info_page_init_bg0_bg2cnt | 新建 card_info.inc |
| DAT_0801d4fc | 0x00000305 | CARD_INFO_BG3CNT_INIT | card_info_page_init_bg0_bg3cnt | 新建 card_info.inc |
| DAT_0801d504 | 0x050003e0 | CARD_INFO_OBJ_PAL_SLOT | card_info_page_init_bg0_obj_pal_slot | 新建 card_info.inc |
| DAT_0801d704 | 0x06001840 | CARD_INFO_NAME_OAM_TILE_BASE | draw_card_name_label_to_vram_oam_tile_base | 新建 card_info.inc |
| DAT_0801d708 | 0x06008200 | CARD_INFO_NAME_SPRITE_VRAM | draw_card_name_label_to_vram_sprite_vram | 新建 card_info.inc |
| DAT_0801d828 | 0x06001c00 | CARD_INFO_STAT_OBJ_TILE_BASE | draw_atk_def_label_to_vram_obj_tile_base | 新建 card_info.inc |
| DAT_0801d82c | 0x06008580 | CARD_INFO_STAT_SPRITE_VRAM | draw_atk_def_label_to_vram_sprite_vram | 新建 card_info.inc |

注: DAT_d94c (0x06001c00) 和 DAT_d994 (0x06008580) 复用上方 d828/d82c 常量。

### REF_SLOTS (USER-label + DATA-ref)

| 槽 (addr) | target | gas_label | slot_label |
|---|---|---|---|
| DAT_0801d458 | 0x0201afb0 = gCardInfoPageState | gCardInfoPageState | card_info_page_enter_with_card_id_state_ptr |
| DAT_0801d4ec | 0x0201afb0 = gCardInfoPageState | gCardInfoPageState | card_info_page_init_bg0_state_ptr |
| DAT_0801d500 | 0x09ccd290 = name_o_palette_data | name_o_palette_data | card_info_page_init_bg0_frame_pal |
| DAT_0801d5b8 | 0x0201afb0 = gCardInfoPageState | gCardInfoPageState | render_card_name_to_line_buf_state_ptr |
| DAT_0801d650 | 0x09e589c4 = sjis_char_fold_table | sjis_char_fold_table | render_card_name_to_line_buf_char_fold |
| DAT_0801d7c8 | 0x0984f59c = card_label_glyph_buf | card_label_glyph_buf | render_atk_def_digits_to_buf_glyph_buf |
| DAT_0801d7cc | 0x0984f54c = card_digit_glyph_data | card_digit_glyph_data | render_atk_def_digits_to_buf_digit_glyph |
| DAT_0801d89c | 0x0984f59c = card_label_glyph_buf | card_label_glyph_buf | render_card_level_text_to_buf_glyph_buf |
| DAT_0801d8a0 | level_signature_table+2 | level_signature_table | render_card_level_text_to_buf_lvl_field_a |
| DAT_0801d8f8 | 0x0984f54c = card_digit_glyph_data | card_digit_glyph_data | render_card_level_text_to_buf_digit_glyph_a |
| DAT_0801d8fc | level_signature_table+0xa | level_signature_table | render_card_level_text_to_buf_lvl_field_b |
| DAT_0801d928 | 0x0984f54c = card_digit_glyph_data | card_digit_glyph_data | render_card_level_text_to_buf_digit_glyph_b |
| DAT_0801d94c | 0x06001c00 = CARD_INFO_STAT_OBJ_TILE_BASE | CARD_INFO_STAT_OBJ_TILE_BASE | draw_card_level_label_to_vram_obj_tile_base |
| DAT_0801d994 | 0x06008580 = CARD_INFO_STAT_SPRITE_VRAM | CARD_INFO_STAT_SPRITE_VRAM | draw_card_level_label_to_vram_sprite_vram |

注: PTR_gPrng_d4e4 / PTR_BG0CNT_d4f0 / PTR_card_stats_table_d5a4 /
    PTR_font_jp_base_table_d5b4 / PTR_card_mini_frame_pal_main_d50c
    这 5 个槽已有 USER-label (PTR_xxx 格式), 无需改动。

### RENAME_SLOTS (纯改名 + EOL)

无纯改名槽 (已有 PTR_xxx 槽直接沿用命名规范)。

### FUNC_RENAME

无函数名矛盾信号。8 个函数名与函数体操作完全吻合:
- card_info_page_enter_with_card_id: zero_fill gCardInfoPageState (0x30 halfwords) -- 确认初始化
- card_info_page_init_bg0: 写 BGxCNT / 清 VRAM / 加载 palette -- 确认 BG 初始化
- render_card_name_to_line_buf: 从 card_stats_table 读类型→选 charset→render_glyph_jp -- 确认
- draw_card_name_label_to_vram: setup_line_buf + render_card_name + commit -- 确认
- render_atk_def_digits_to_buf: __umodsi3/__udivsi3 逐位分解 + blit_glyph_columns -- 确认
- draw_atk_def_label_to_vram: setup_line_buf + render_atk_def + commit -- 确认
- render_card_level_text_to_buf: 4×blit_glyph (LEVEL label) + count_bytes_until_null + decode -- 确认
- draw_card_level_label_to_vram: lookup_level_glyph_index + setup_line_buf + render + commit -- 确认

### PLATE (R5)

8 个函数均有 CJK 注释 (@ 风格 plate), 需 ASCII 重写。

| 函数 | 当前 | 新 ASCII plate |
|---|---|---|
| card_info_page_enter_with_card_id | "p1: FUN_0801e640 的首个 bl" (CJK) | "p1: called by open_card_info_by_icid; zero-fills gCardInfoPageState (0x30 halfwords=0x60B)." |
| card_info_page_init_bg0 | "p1: 写 BG0CNT=0x0086, 清 BG0 VRAM" (CJK) | "Initializes BG0-3 control regs, clears VRAM regions, loads card mini-frame tiles and palette to BG/OBJ." |
| render_card_name_to_line_buf | long CJK plate | "r0=card_id. Reads card_stats_table type field to detect wide-card (0x16/0x17). Loads gFontJpCtx from gCardInfoPageState[+8], selects charset (gSettings bits[2:0]) via select_charset_then_load_name, then iterates SJIS bytes, using sjis_char_fold_table[byte] != byte to detect 2-byte sequences. Width guard: cumulative width cmp #0x5c stops render. Returns void." |
| draw_card_name_label_to_vram | long CJK plate | "r0=card_id. Calls setup_line_buf_pos_and_font(x=0xe,y=2,base=0x06001c00), render_card_name_to_line_buf(card_id), commit_line_buffer_to_sprite_vram(0x06008200,0). Post-commit loop: writes sequential tile-attr halfwords from 0x06001840 across 2 rows x 14 columns (tile_idx from 0x210, increments). indeg=1; caller card_image_decode_wrapper." |
| render_atk_def_digits_to_buf | long CJK plate | "r0=atk_val, r1=def_val. Calls blit_glyph_columns_to_buf 4x for ATK label glyphs (col offsets 0x1a/0x22/0x40/0x48), then loops 4 digits each for ATK/DEF via __umodsi3/__udivsi3 at col offsets 0x36..0x2e (ATK) and 0x5c..0x54 (DEF). Glyph buf base=0x0984f59c, digit glyph src=0x0984f54c (8B/glyph). indeg=1; caller draw_atk_def_label_to_vram." |
| draw_atk_def_label_to_vram | long CJK plate | "r0=atk_val, r1=def_val. Calls setup_line_buf_pos_and_font(x=0xe,y=2,base=0x06001c00), render_atk_def_digits_to_buf(atk,def), commit_line_buffer_to_sprite_vram(0x06008580,0). Post-commit loop mirrors draw_card_name_label_to_vram. Symmetric sibling of draw_card_name_label_to_vram. indeg=1; caller card_image_decode_wrapper." |
| render_card_level_text_to_buf | long CJK plate | "r0=level_idx (from lookup_level_glyph_index). Blits 4-glyph LEVEL/RANK label (blit_glyph_columns_to_buf x4). Then reads level_signature_table[r0].field_a and .field_b (stride=20B) for label and rank strings. Decodes ASCII: 0x3f->glyph_14, 0x58->glyph_15, 0x30..0x39->digit. Renders each decoded glyph via blit_glyph_columns_to_buf at col offsets 0x36..0x2e and 0x5c..0x54. Returns void." |
| draw_card_level_label_to_vram | long CJK plate | "r0=card_id. Calls lookup_level_glyph_index(card_id); returns 0 if -1 (no level: magic/trap). Otherwise: setup_line_buf_pos_and_font(x=0xe,y=2), render_card_level_text_to_buf(level_idx), commit_line_buffer_to_sprite_vram(0x06008580,0). Returns 1 on success, 0 if no level. indeg=1; caller card_image_decode_wrapper." |

---

## carve 计划 (R7)

### carve A: sjis_char_fold_table (0x09e589c4, 256B)

宿主 incbin: asm/rom.s 中 banlist_handler_table 尾部 `.incbin "roms/2343.gba", 0x1E589A4, 0x368`

该 256B 表位于 incbin 偏移 0x20 处 (0x09e589c4 = 0x09e589a4 + 0x20)。

分裂方案:
```
@ 宿主 incbin 分裂 (替换 ".incbin roms/2343.gba, 0x1E589A4, 0x368"):
    .incbin "roms/2343.gba", 0x1E589A4, 0x20     @ gap before table (0x20 B)
sjis_char_fold_table:                              @ 0x09e589c4 (256B)
    .incbin "roms/2343.gba", 0x1E589C4, 0x100
    .incbin "roms/2343.gba", 0x1E58AC4, 0x248     @ remainder (0x368 - 0x20 - 0x100 = 0x248)
@ 覆盖等式: 0x20 + 0x100 + 0x248 = 0x368 == 原 size ✓
```

代码侧 DAT_d650 改为 `.word sjis_char_fold_table` (+ slot_label)。

置信度: high (表结构为 256B identity 变体, 4 ROM 代码引用全为 data, no THUMB)

### carve B: card_digit_glyph_data + card_label_glyph_buf (0x0984f54c, seg-C 大 incbin)

宿主 incbin: `.incbin "roms/2343.gba", 0x1832602, 0x1E51A` (covers 0x1832602..0x1850B1C)

- card_digit_glyph_data @ 0x0984f54c (ROM offset 0x184f54c)
  - 在 incbin 偏移: 0x184f54c - 0x1832602 = 0x1CF4A
  - 内容: 10 digits x 8B/glyph (0-9 decimal digit bitmaps, 7px wide)
  - 6 ROM refs (raw), 0 THUMB
- card_label_glyph_buf @ 0x0984f59c (ROM offset 0x184f59c)
  - 在 incbin 偏移: 0x184f59c - 0x1832602 = 0x1CF9A
  - 内容: label glyph buffer (JP kana + misc 7px glyphs, starts at 0x184f59c)
  - 3 ROM refs (raw), 0 THUMB
  - distance: 0x0984f59c - 0x0984f54c = 0x50 (= 10 * 8B, immediately after digit data)

分裂方案 (替换宿主 incbin):
```
    .incbin "roms/2343.gba", 0x1832602, 0x1CF4A   @ pre-segment (to digit glyphs)
card_digit_glyph_data:                              @ 0x0984f54c
    .incbin "roms/2343.gba", 0x184f54c, 0x50       @ 10 digits x 8B
card_label_glyph_buf:                              @ 0x0984f59c
    .incbin "roms/2343.gba", 0x184f59c, ...        @ label glyph data, size TBD
    .incbin "roms/2343.gba", ..., <remainder>       @ rest to 0x1850B1C
@ 覆盖等式: 0x1CF4A + 0x50 + <label_sz> + <remainder> == 0x1E51A ✓
```

BLOCKED: label_sz (0x0984f59c 段结束地址) 需 ref-scan + 内容分析确认边界;
reviewer 请核实或补 size 参数。置信度: high for addresses, med for boundary.

---

## disasm 计划 (R4)

无 -- 段内无被引用的误标数据块。所有函数均已正确 disasm。

---

## 新增 constants / 全局

### 新增 ewram.inc 全局: gCardInfoPageState

```
.equ gCardInfoPageState, 0x0201afb0  @ card info page per-frame state struct (EWRAM)
                                      @ +0x0  = u32 packed: bit0=page_active, bits[17:2]=card_id
                                      @ +0x4  = u16 page_step (0=init, 1/2/3=tick phases)
                                      @ +0x6  = u8  countdown_timer (tick update, non-zero decrements)
                                      @ +0x14 = u32 scroll_frame_counter (>0xe8 triggers scroll)
                                      @ +0x18 = u32 scroll_pixel_y_offset
                                      @ +0x1c = u32 scroll_sub_counter
                                      @ +0x20 = s16 scroll_offset_field (adjusted by display flags)
                                      @ 20 ROM refs in file 01; consumers: card_info_page_enter_with_card_id,
                                      @   card_info_page_init_bg0, render_card_name_to_line_buf,
                                      @   tick_scroll_frame_and_update_pos, update_card_info_page_state,
                                      @   render_card_stats_oam_for_current_card, tick_card_info_page_by_state
```

消费者证据:
- `asm/01_vija_scene_text.s:1207` (DAT_0801d458 = 0x0201afb0, zero_fill target, high)
- `asm/01_vija_scene_text.s:3174` (plate: "读 [0x0201afb0+0x6] 倒计时字段", high)
- `asm/01_vija_scene_text.s:3651` (plate: "设 [0x0201afb0+0x0] bit2 = card_info_page_active_flag", high)
- `asm/01_vija_scene_text.s:3534` (plate: "Reads current card_id from ... 0x0201afb0 (+0x0 bits[17:2])", high)

### 新增 card_info.inc (constants/card_info.inc)

```
@ Card Info Page BG Control Register Initial Values
.equ CARD_INFO_BG1CNT_INIT, 0x00004104  @ BG1CNT: pri=0 charbase=1 16col scrbase=0x10 32x32
.equ CARD_INFO_BG2CNT_INIT, 0x00000407  @ BG2CNT: pri=3 charbase=1 16col scrbase=0 32x32
.equ CARD_INFO_BG3CNT_INIT, 0x00000305  @ BG3CNT: pri=1 charbase=0 16col scrbase=0 32x32

@ OBJ Palette Slot for card info frame (OBJ_PALRAM_BASE + 0x1e0)
.equ CARD_INFO_OBJ_PAL_SLOT, 0x050003e0  @ OBJ palette slot 0xf0 (pal 15 color 0)

@ OAM/VRAM addresses for card info text sprites
.equ CARD_INFO_NAME_OAM_TILE_BASE, 0x06001840  @ OBJ tile attr base for card name line
.equ CARD_INFO_NAME_SPRITE_VRAM,   0x06008200  @ OBJ VRAM commit target for card name
.equ CARD_INFO_STAT_OBJ_TILE_BASE, 0x06001c00  @ OBJ tile base for ATK/DEF/Level sprites
.equ CARD_INFO_STAT_SPRITE_VRAM,   0x06008580  @ OBJ VRAM commit target for ATK/DEF/Level
```

证据:
- CARD_INFO_BG1CNT_INIT: `asm/01_vija_scene_text.s:1280` (.word 0x00004104, written to BG1CNT, high)
- CARD_INFO_BG2CNT_INIT: `asm/01_vija_scene_text.s:1282` (.word 0x00000407, written to BG2CNT, high)
- CARD_INFO_BG3CNT_INIT: `asm/01_vija_scene_text.s:1284` (.word 0x00000305, written to BG3CNT, high)
- CARD_INFO_OBJ_PAL_SLOT: `asm/01_vija_scene_text.s:1288` (copy_bytes_by_halfword dst=0x050003e0, high)
- CARD_INFO_NAME_SPRITE_VRAM: `asm/01_vija_scene_text.s:1556-7` + `asm/02_text_lp_fieldspell.s:2680` (OBJ sprite VRAM base, high)
- CARD_INFO_STAT_SPRITE_VRAM: `asm/01_vija_scene_text.s:1703-4` (commit_line_buf target, high)

注: 0x06001840 和 0x06001c00 仅在 card_info 场景内使用 (4 refs 和 3 refs), 语义为
"draw_card_*_label_to_vram 内 OBJ tile attr 写入基址"; 两处功能基本相同但 OAM tile 起始位置不同
(card name: 0x06001840; ATK/DEF/Level: 0x06001c00)。

---

## §5.1 登记 (Rule 3) -- 0 引用块

无。段内无 ROM_INCBIN 或 .byte 数据块, 不需要登记。

---

## 消费者证据 (R6) -- 关键槽语义

| 槽 | 消费者 file:line | 语义 | 置信度 |
|---|---|---|---|
| gCardInfoPageState | asm/01_vija_scene_text.s:1207, 3174, 3534, 3651 | EWRAM 卡片信息页面状态结构体 base | high |
| name_o_palette_data | asm/rom.s:673 (已 carve H) | 16 RGB15 颜色 name_o OAM/BG 调色板 | high |
| level_signature_table | data/post-banlists-tables.s:22 + 注释 rec[0].field_a @ 0x0801D8A0 | 等级签名表 (14 records x 20B) | high |
| card_digit_glyph_data | asm/01_vija_scene_text.s:1653 (0x0984f54c, blit_glyph_columns_to_buf src) | 10 digit glyph bitmaps (8B each, 7px wide) | high |
| card_label_glyph_buf | asm/01_vija_scene_text.s:1566 (0x0984f59c, blit_glyph_columns_to_buf r0) | label glyph buffer (LEVEL/ATK/DEF JP bitmaps) | high |
| sjis_char_fold_table | asm/01_vija_scene_text.s:1460 (0x09e589c4, ldrb table lookup in card name loop) | 256B SJIS/ascii char normalization table (lowercase->uppercase fold + SJIS lead-byte remap) | high |
| CARD_INFO_NAME_SPRITE_VRAM | asm/01_vija_scene_text.s:1556 + 02_text_lp_fieldspell.s:2680 | commit_line_buffer_to_sprite_vram target for card name line | high |

---

## 求助

1. **BLOCKED: card_label_glyph_buf 边界** (render 表格 carve B)
   - `0x0984f59c` 的结束地址不明 -- 需要确认 seg-C incbin 内该 label glyph 区域的 size
   - 建议: ref-scan 附近地址或查 blit_glyph_row_to_buffer 访问模式确认 stride
   - 置信度: low for size; high for start address

2. **低置信 CARD_INFO_NAME_OAM_TILE_BASE (0x06001840)**
   - draw_card_name_label_to_vram post-commit 循环的语义: 向 0x06001840 开始的地址写入
     递增的 tile index halfword (0x210, 0x211, ...) -- 外观上是"OBJ tile attribute table entries"
   - 但 0x06001840 在 BG VRAM 区 (0x06000000..0x0600FFFF) 而非 OBJ tile 区 (0x06010000+)
   - 可能是 BG tile map entries 或 shadow OAM buffer
   - 置信度 for address: high; for semantic label: med
   - 建议 reviewer 核实: 实际是 BG tile map slot 还是 OBJ attr shadow?

---

## driver 解 BLOCKED + LOW-CONF + host incbin 定位 (静态 ROM 核)

**host incbin (rom.s 已核)**:
- card_digit_glyph_data (0x0984f54c) / card_label_glyph_buf (0x0984f59c) / **第三 ref 0x0984f5cc (2 refs, executor 漏)**: 全在 **rom.s line 121 `incbin 0x1832602, 0x1e51a`** (124KB blob), 偏移 +0x1cf4a / +0x1cf9a / +0x1cfca。
- sjis_char_fold_table (0x09e589c4, 4 refs): 在 **rom.s line 1596 `incbin 0x1e589a4, 0x368`** (Seg-9 remainder), 偏移 +0x20。

**BLOCKED (card_label_glyph_buf size) RESOLVED**: 用 **label+incbin-span** 法无需定 size —— label@0x0984f59c, incbin span 到下一 ref 0x0984f5cc。三个 ref 顺序: 0x0984f54c (digit, 下界 0x59c→size 0x50) → 0x0984f59c (label, →0x5cc, size 0x30) → 0x0984f5cc (第三表, 需 label)。**carve 三个 label** 从 line-121 blob:
```
.incbin 0x1832602, 0x1cf4a              @ 大 pre (到 0x0984f54c)
card_digit_glyph_data:  @0x0984f54c  .incbin 0x184F54C, 0x50
card_label_glyph_buf:   @0x0984f59c  .incbin 0x184F59C, 0x30
card_glyph_table_3:     @0x0984f5cc  .incbin 0x184F5CC, <到 blob 尾>   @ 第三 ref, driver 补 label
.incbin <0x184F5FC>, <余>             @ 余到 0x1832602+0x1e51a=0x1850B1C
```
covered: 0x1cf4a + 0x50 + 0x30 + 余 == 0x1e51a (reviewer 重算精确余 size + 确认 0x0984f5cc 是否真表起点 or digit/label 续)。

**LOW-CONF (0x06001840) RESOLVED**: 0x06001840 < 0x06010000 = **BG VRAM 区** (非 OBJ tile VRAM 0x06010000+)。故 `CARD_INFO_NAME_OAM_TILE_BASE` 是**误名** → 改 `CARD_INFO_NAME_BG_TILE_VRAM` (BG char VRAM tile 地址)。同理核 CARD_INFO_STAT_OBJ_TILE_BASE=0x06001c00 (亦 <0x06010000 = BG VRAM, 改 _BG_)。CARD_INFO_NAME_SPRITE_VRAM=0x06008200 / _STAT_SPRITE_VRAM=0x06008580 (亦 BG VRAM 区, executor 命名 SPRITE 存疑 — reviewer 核语义: 是 BG tile 数据还是 sprite shadow)。

driver 注: 三个 card-glyph carve 从 124KB blob 切出, label+incbin-span byte-identical-safe; reviewer 重算覆盖等式 + 核 0x0984f5cc 表性质 + 0x06001840/1c00 BG-VRAM 命名订正。
