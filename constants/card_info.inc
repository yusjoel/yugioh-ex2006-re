@ =============================================================================
@ Card Info Page constants (card_info_page_init_bg0 / draw_card_*_label_to_vram)
@ Source: asm/01_vija_scene_text.s, Seg-2 (0x0801d448..0x0801d998)
@ Seg-3 additions: card_image_decode_wrapper / render_card_name_to_desc_page_vram /
@   card_info_page_finalize / blit_glyph_2x2_to_bg_vram / tick_blend_fadein_and_poll_done
@ =============================================================================

@ BG Layer Control Register initial values (written to BG1CNT/BG2CNT/BG3CNT)
.equ CARD_INFO_BG1CNT_INIT, 0x00004104  @ BG1CNT: pri=0 charbase=1 16col scrbase=0x10 32x32
.equ CARD_INFO_BG2CNT_INIT, 0x00000407  @ BG2CNT: pri=3 charbase=1 16col scrbase=0 32x32
.equ CARD_INFO_BG3CNT_INIT, 0x00000305  @ BG3CNT: pri=1 charbase=0 16col scrbase=0 32x32

@ OBJ Palette slot for card info frame (OBJ_PALRAM_BASE + 0x1e0 = pal 15 color 0)
.equ CARD_INFO_OBJ_PAL_SLOT, 0x050003e0  @ OBJ palette slot for card name/stat frame tiles

@ BG VRAM write bases for card info text (all < 0x06010000 = BG VRAM, not OBJ tile VRAM)
.equ CARD_INFO_NAME_BG_TILE_VRAM, 0x06001840  @ BG screen-map tile-attr write base for card name line (CB0, SB3+0x040)
.equ CARD_INFO_NAME_SPRITE_VRAM,  0x06008200  @ commit_line_buffer_to_sprite_vram target for card name
.equ CARD_INFO_STAT_BG_TILE_VRAM, 0x06001c00  @ BG screen-map tile-attr write base for ATK/DEF/Level lines (CB0, SB3+0x400)
.equ CARD_INFO_STAT_SPRITE_VRAM,  0x06008580  @ commit_line_buffer_to_sprite_vram target for ATK/DEF/Level

@ --- Seg-3 additions (card_image_decode_wrapper + render_card_name_to_desc_page_vram + card_info_page_finalize) ---

@ Card image tile pack parameters (card_image_decode_wrapper)
.equ CARD_TILE_PACK_GLYPH_OFF_A,   0x0985004c  @ card_glyph_table_3+0xa80 (tile src A, normal card map)
.equ CARD_TILE_PACK_GLYPH_OFF_B,   0x09850934  @ card_glyph_table_3+0x1368 (tile src B)
.equ CARD_TILE_PACK_MAP_PARAM,     0x0000020e  @ load_pack_tile_and_map_to_vram map param (31 ROM refs)
.equ CARD_FRAME_TILE_SRC_MONSTER,  0x0984a3fc  @ seg-C blob: monster card frame tile pack source
.equ CARD_FRAME_TILE_SRC_SPELL,    0x0984b994  @ seg-C blob: spell card frame tile pack source (type23)
.equ CARD_FRAME_PAL_SRC_MONSTER_A, 0x0984dd6c  @ seg-C blob: monster frame OBJ palette A (32B)
.equ CARD_FRAME_TILE_SRC_MONSTER_A,0x0984d8ec  @ seg-C blob: monster frame OBJ tile data A (256B)
.equ CARD_FRAME_PAL_SRC_SPELL_A,   0x0984de6c  @ seg-C blob: spell frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_SPELL_A,  0x0984dcec  @ seg-C blob: spell frame OBJ tile data A
.equ CARD_FRAME_PAL_SRC_STAR_A,    0x0984f52c  @ seg-C blob: star/level frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_STAR,     0x0984dc6c  @ seg-C blob: star/level OBJ tile data
.equ CARD_FRAME_TILE_SRC_STAR_B,   0x0984f46c  @ seg-C blob: star/level OBJ tile data B
.equ CARD_FRAME_PAL_SRC_MONSTER_B, 0x0984de4c  @ seg-C blob: monster frame OBJ palette B
.equ CARD_FRAME_PAL_SRC_ICON_A,    0x0984ee2c  @ seg-C blob: icon frame OBJ palette A (type 0x17)
.equ CARD_FRAME_PAL_SRC_ICON_B,    0x0984f3ac  @ seg-C blob: icon frame OBJ palette B (type 0x16)
.equ CARD_FRAME_TILE_SRC_ICON,     0x0984f0ac  @ seg-C blob: icon frame OBJ tile data (type 0x16)
.equ CARD_FRAME_TILE_SRC_SPELL_B,  0x0984e42c  @ seg-C blob: spell frame OBJ tile data B (type 0x17)
.equ CARD_OVERLAY_TILE_SRC,        0x09ccd2d0  @ name_o region+0x40: card overlay nibble-sequence tile (5 refs)

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

@ Card description page text VRAM (render_card_name_to_desc_page_vram + render_card_description_text)
.equ CARD_DESC_LINE_BUF_VRAM,   0x06007100  @ BG VRAM card description text line buffer
.equ CARD_DESC_BG_VRAM_A,       0x06000800  @ BG VRAM desc page tile region A (tile-seq write target A)
.equ CARD_DESC_BG_VRAM_B,       0x06000c80  @ BG VRAM desc page tile region B (tile-seq write target B)
.equ CARD_DESC_RENDER_PARAM,    0x00008008  @ render_glyph_jp layer param for card description

@ --- Seg-4 additions (draw_card_stat_digits_to_oam / draw_stat_row_sprites_to_oam) ---

@ OAM packed constants for card stat digit sprites (write_oam_entry_from_packed_args: r0=packed_xy, r1=tile_idx, r2=attr2)
@ packed_xy format: low16=x_coord (9-bit), high16=oam_y
.equ CARD_STAT_ATK_DEF_OAM_XY,    0x00060056  @ ATK/DEF frame OBJ position (x=86, y=6); 4 ROM refs
.equ CARD_STAT_ATK_DEF_OAM_ATTR2, 0x0000d3a2  @ ATK/DEF frame attr2: pal13, tile0x3a2; 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_XY,      0x00150058  @ Quick-Play Spell secondary marker pos (x=88, y=21); 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_ATTR2,   0x0000e3a6  @ Quick-Play marker attr2: pal14, tile0x3a6; 2 ROM refs
.equ CARD_STAT_DIGIT_OAM_ATTR2,   0x0000f001  @ ATK/DEF digit sprite attr2: pal15, tile1; 2 ROM refs
.equ CARD_STAT_FUSION_OAM_ATTR2,  0x0000c3a8  @ Fusion/extra-type marker attr2: pal12, tile0x3a8; 1 ROM ref

@ OAM attr2 base offsets for stat row sprites (draw_stat_row_sprites_to_oam)
@ Added to r5 (col_idx*0x10 + 2) then u16-truncated to produce attr2 per row
.equ CARD_STAT_ROW_ATTR2_BASE_A,  0xfffff800  @ stat row sprite group A attr2 base (row 0, Y=0x70)
.equ CARD_STAT_ROW_ATTR2_BASE_B,  0xfffff804  @ stat row sprite group B attr2 base (row 1, Y=0x90)
.equ CARD_STAT_ROW_ATTR2_BASE_C,  0xfffff808  @ stat row sprite group C attr2 base (row 2, Y=0xb0)
.equ CARD_STAT_ROW_ATTR2_BASE_D,  0xfffff80c  @ stat row sprite group D attr2 base (row 3, Y=0xd0)

@ --- Seg-8 additions: LP threshold constants for render_card_stats_to_line_buf ---

.equ CARD_STAT_LP_THRESHOLD,      0x00000bb8  @ 3000 LP threshold for card stat display branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_999,  0x000003e7  @ 999 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_1500, 0x000005dc  @ 1500 LP threshold (render_card_stats dispatch); 35 ROM refs
.equ CARD_STAT_LP_THRESHOLD_5730, 0x00001662  @ 5730 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_57300,0x0000dfd4  @ 57300 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_572488,0x0008be48 @ 572488 LP threshold (upper range); 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_20000,0x00004e20  @ 20000 LP threshold extended render path; 1 ROM ref

@ gCardInfoPageState.word0 bit-field masks (card_list_on_select_to_info_page)
@ word0 layout: bits[2:0]=flags, bits[16:3]=card_id (14-bit), bit17=active_flag
.equ CARD_INFO_STATE_CARD_ID_MASK,  0x00003fff  @ mask for card_id bits[13:0] before shift-3 into word0
.equ CARD_INFO_STATE_CARD_ID_CLEAR, 0xfffe0007  @ AND mask to clear card_id field bits[16:3], preserve [17]+[2:0]

@ =============================================================================
@ file 02 Seg-1 additions: text render / pack selection / opp card name offsets
@ =============================================================================

.equ GAME_STR_TEXT_BASE,            0x00000C1C  @ str_base_offset=0x0c1c; adds to game_str_id_offset; 15 ROM refs
.equ CARD_ID_BASE_NEG_ADJ,          0xFFFFD8EF  @ neg adj -0x2711 so card_id 0x2711 maps to 0; 5 ROM refs
.equ PACK_DECK_A_KEY,               0x00002711  @ deck A key for find_deck_record_index_by_key; 5 ROM refs
.equ OPP_CARD_NAME_STR_OFF_ES,      0x0003A90C  @ ES offset from game_str_ja_0326 base; 1 ROM ref
.equ OPP_CARD_NAME_STR_OFF_ES_NULL, 0x0003A90E  @ ES offset from game_str_ja_0327 base; 1 ROM ref

@ =============================================================================
@ file 02 Seg-5 additions: field spell type-B effect chain guard
@ =============================================================================
.equ FIELD_SPELL_B_EFFECT_ID, 0x00001407  @ effect chain guard value for field spell type-B placement check; 12 ROM refs

@ =============================================================================
@ file 02 Seg-6 additions: zone slot set_code / card_id mask
@ =============================================================================
.equ SLOT_CARD_SET_CODE_MASK, 0x00001fff  @ 13-bit mask for YGO set_code/card_id fields in zone slot arrays; 101 raw refs; 2 Seg-6 slots

@ =============================================================================
@ file 02 Seg-8 additions: field spell / monster zone card IDs
@ =============================================================================
.equ TOON_WORLD_CARD_ID,             0x000012be  @ Toon World field-magic card id; presence check via equip-zone scan; 9 raw refs
.equ GROUND_COLLAPSE_FIELD_CARD_ID,  0x00001432  @ Ground Collapse field spell card id (data.md line 900, passcode 90502999); placement-block check in check_slot_placement_blocked_by_field_effect; 18 raw refs
.equ OJAMA_KING_CARD_ID,             0x000017ee  @ Ojama King card id (data.md line 1639, passcode 90140980); monster-zone limit effect; placement-block check; 13 raw refs
.equ SPATIAL_COLLAPSE_CARD_ID,       0x000016df  @ Spatial Collapse field spell id; monster zone clamp in count_available_monster_slots; 16 raw refs
