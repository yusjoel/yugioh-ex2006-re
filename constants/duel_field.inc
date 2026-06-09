@ =============================================================================
@ Duel Field display constants (init_duel_field_icon_and_bg_vram / render_win_count / render_opp_wins)
@ File 01 Seg-7 (0x08020fa8..0x08024868)
@ =============================================================================

@ gPrng step index / frame control offsets
.equ GPRNG_STEP_IDX_OFF,          0x00000202  @ gPrng+0x202 halfword: step index field (tick_scene_step_by_step_table_d)
.equ GPRNG_FRAME_CTRL_OFF_203,    0x00000203  @ gPrng+0x203 byte: frame control field 2

@ OBJ palette
.equ OBJ_PAL_SLOT_1,              0x05000220  @ OBJ_PALRAM_BASE+0x20 = OBJ palette slot 1; 12 ROM refs

@ Duel field init values
.equ DUEL_FIELD_CTRL_VAL,         0x00000601  @ written to gPrng+0xba*2=gPrng+0x174 at duel field init
.equ DUEL_FIELD_BGCNT1_INIT,      0x00000105  @ BG1CNT init value for duel field (pri=1 charbase=0 scrbase=0)
.equ DUEL_FIELD_BGCNT2_INIT,      0x00000206  @ BG2CNT init value for duel field (pri=2 charbase=0 scrbase=0)
.equ DUEL_FIELD_BGCNT3_INIT,      0x00000307  @ BG3CNT init value for duel field (pri=3 charbase=0 scrbase=0)

@ Win count display
.equ GWINS_BASE_OFFSET,           0x00006e60  @ gWinsBase - EWRAM_BASE; win count record table offset
.equ GWINS_BASE_OFF_2,            0x00006e62  @ gWinsBase+2 - EWRAM_BASE; second field offset
.equ OPP_WIN_DIGIT_TILE_BASE,     0x00000474  @ OAM digit sprite tile base index for opponent win count
.equ OPP_WIN_SPRITE_OFFSCREEN_XY, 0x00004040  @ OAM attr0[y=0x40]|attr1[x=0x40] off-screen placeholder
.equ OPP_WIN_SEPARATOR_TILE_IDX,  0x00000454  @ First fixed separator sprite tile index

@ Unlocked duelists offset
.equ GUNLOCKED_DUELISTS_OFFSET,   0x00006e5c  @ gUnlockedDuelists - EWRAM_BASE

@ render_centered_text_to_bg_vram args
.equ DUEL_FIELD_TEXT_TILE_POS_A,  0x00000507  @ render_centered_text_to_bg_vram r0 arg: col=7 row=5; 34 refs
.equ DUEL_FIELD_TEXT_BG_WIDTH,    0x00000f09  @ render_centered_text_to_bg_vram r3 arg: BG width 0x0f; 14 refs
.equ DUEL_FIELD_TEXT_TILE_POS_B,  0x000004a7  @ render_centered_text_to_bg_vram r0 arg: col=7 row=4; 5 refs
.equ DUEL_FIELD_TEXT_TILE_POS_C,  0x00000567  @ render_centered_text_to_bg_vram r0 arg variant C; 8 refs

@ write_tile_row_to_vram tile descriptors
.equ DUEL_FIELD_TILE_ROW_ARG_A,   0x00000901  @ write_tile_row_to_vram tile descriptor A; 35 refs
.equ DUEL_FIELD_TILE_ROW_ARG_B,   0x000008a1  @ write_tile_row_to_vram tile descriptor B; 8 refs
.equ DUEL_FIELD_TILE_ROW_ARG_C,   0x00000961  @ write_tile_row_to_vram tile descriptor C; 5 refs

@ OAM duel field card sprite positions/indices
.equ DUEL_FIELD_OAM_COORDS_A,     0x00830070  @ packed OAM coords row=0x83 x=0x70 (duel field card sprite A); 2 refs
.equ DUEL_FIELD_OAM_COORDS_B,     0x00210070  @ packed OAM coords row=0x21 x=0x70 (duel field card sprite B); 1 ref
.equ DUEL_FIELD_OAM_TILE_IDX_A,   0x00000814  @ OAM tile index 0x814 for duel field card sprite; 28 refs
.equ DUEL_FIELD_OAM_TILE_IDX_B,   0x00000815  @ OAM tile index 0x815; 6 refs
.equ DUEL_FIELD_OAM_TILE_IDX_C,   0x00000816  @ OAM tile index 0x816; 5 refs

@ Duel scene flags / fields
.equ DUEL_SCENE_FLAGS_MASK_0F00,  0xffff0f00  @ mask bits[11:8] of duel scene flags word; 10 refs
.equ DUEL_SCENE_FIELD_OFF_6E48,   0x00006e48  @ EWRAM+0x6e48 = duel scene record field A; 10 refs
.equ DUEL_SCENE_FIELD_OFF_6E57,   0x00006e57  @ EWRAM+0x6e57 = duel scene record field B; 19 refs
