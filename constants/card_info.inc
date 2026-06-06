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
