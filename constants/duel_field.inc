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

@ =============================================================================
@ Seg-8 additions: campaign scene / card stat render constants
@ =============================================================================

@ Campaign step counter / frame control masks
.equ GPRNG_STEP_CTR_MASK,         0xffffc03f  @ mask clears bits[13:6] of gPrng+0x202 halfword (step counter); 223 ROM refs
.equ SCENE_CTX_ANIM_MASK,         0xffff807f  @ mask clears bits[14:7] of scene_ctx+0x8 (anim frame field); 7 ROM refs
.equ SCENE_CTX_TIMER_CLEAR,       0xff807fff  @ mask clears bits[22:15] of scene_ctx+0x8 word (timer field); 4 ROM refs
.equ GPRNG_FIELD_ANIM_MASK,       0xfffffc1f  @ mask clears bits[7:5] of gPrng field anim state; 5 ROM refs

@ Campaign BG tile/map parameters (load_pack_tile_and_map_to_vram args)
.equ CAMPAIGN_BG_TILE_PARAM_A,    0x00000be5  @ tile param A; 4 ROM refs
.equ CAMPAIGN_BG_TILE_PARAM_B,    0x000007c7  @ tile param B; 7 ROM refs
.equ CAMPAIGN_BG_TILE_PARAM_C,    0x00000bc1  @ tile param C; 4 ROM refs
.equ CAMPAIGN_BG_TILE_PARAM_D,    0x00000bff  @ tile param D; 6 ROM refs
.equ CAMPAIGN_BG_TILE_PARAM_E,    0x00000801  @ tile param E (step2/12/22); 3 ROM refs
.equ CAMPAIGN_BG_TILE_PARAM_F,    0x00000be4  @ tile param F (step11); 1 ROM ref
.equ CAMPAIGN_BG_TILE_PARAM_G,    0x00000707  @ tile param G (step11); 1 ROM ref
.equ CAMPAIGN_BG_TILE_PARAM_H,    0x00000b01  @ tile param H (step11); 1 ROM ref

@ Campaign win/decimal display arg
.equ DRAW_DECIMAL_WIN_LABEL_ARG,  0x0000010f  @ r2 arg to draw_decimal_with_offset for campaign win label; 33 ROM refs

@ Duel scene field offsets
.equ DUEL_SCENE_FIELD_OFF_6E58,   0x00006e58  @ EWRAM+0x6e58 = player name/level field C; 3 ROM refs

@ Duel scene field slot masks
.equ SCENE_SLOT_MASK_LO,          0x00000fff  @ keeps bits[11:0] of slot word; 3 Seg-8 refs (84 total)
.equ SCENE_SLOT_MASK_HI_CLEAR,    0xffe00000  @ clears bits[28:21] of slot word; 3 ROM refs
.equ SCENE_SLOT_FIELD_CLEAR,      0xfffff000  @ clears bits[11:0] of slot word; 3 ROM refs
.equ SCENE_SLOT_FIELD_MASK,       0x000003fe  @ mask bits[8:1] of slot field; 148 ROM refs
.equ SCENE_SLOT_CTR_CLEAR,        0xffc00fff  @ clears bits[21:12] of slot word; 3 ROM refs

@ Campaign duelist name display row parameters (step21)
.equ CAMPAIGN_DUELIST_NAME_ROW_A, 0x0000114f  @ duelist name display row param A (step21); 1 ROM ref
.equ CAMPAIGN_DUELIST_NAME_ROW_B, 0x00001138  @ duelist name display row param B (step21); 1 ROM ref

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
