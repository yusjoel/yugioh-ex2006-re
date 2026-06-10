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

@ =============================================================================
@ Seg-9 additions: campaign card-select handlers + pack scene init
@ =============================================================================

@ Campaign card-select SIO / display constants
.equ CAMPAIGN_SIO_CMD_MATCH,          0x00002c06  @ SIO link cmd code for card select sync; 4 ROM refs
.equ CAMPAIGN_CARD_STEP_COPY_MASK,    0xffe07fff  @ clears bits[28:15] from display ctx +0x1c word; 1 ROM ref
.equ CAMPAIGN_CARD_ANIM_STEP_MASK,    0xfffffe03  @ clears bits[9:2] of scene_ctx+0x3a halfword; 39 ROM refs
.equ GPRNG_SCENE_CTX_DISPLAY_FLAG_OFF, 0x00000584 @ gPrng+0x1c0 dereference + 0x584: display_ready flag byte; 20 ROM refs

@ Campaign OAM sprite positions (packed 32-bit: y[23:16] | x[7:0] written to write_oam_entry_from_packed_args)
.equ CAMPAIGN_CARD_SPRITE_POS_0,      0x003e0014  @ card sprite 0 xy (x=0x14, y=0x3e)
.equ CAMPAIGN_CARD_SPRITE_POS_1,      0x003e0034  @ card sprite 1 xy
.equ CAMPAIGN_CARD_SPRITE_POS_2,      0x003e0054  @ card sprite 2 xy
.equ CAMPAIGN_CARD_SPRITE_POS_3,      0x003e0084  @ card sprite 3 xy
.equ CAMPAIGN_CARD_SPRITE_POS_4,      0x003e00a4  @ card sprite 4 xy
.equ CAMPAIGN_CARD_SPRITE_POS_5,      0x003e00c4  @ card sprite 5 xy

@ Campaign hand sprite positions
.equ CAMPAIGN_HAND_SPRITE_POS_A,      0x006e0024  @ hand sprite A xy (x=0x24, y=0x6e)
.equ CAMPAIGN_HAND_SPRITE_POS_B,      0x006e0044  @ hand sprite B xy
.equ CAMPAIGN_HAND_SPRITE_POS_C,      0x006e0094  @ hand sprite C xy
.equ CAMPAIGN_HAND_SPRITE_POS_D,      0x006e00b4  @ hand sprite D xy

@ =============================================================================
@ Seg-10 additions: campaign victory / puzzle LP display constants
@ =============================================================================

@ Campaign challenge score / banner offsets
.equ GPRNG_CHALLENGE_SCORE_OFF,       0x00000241  @ gPrng+0x241: per-challenge score/win array offset; 24 ROM refs

@ Text render mode arg
.equ TEXT_RENDER_COLOR_MODE_1,        0x00008001  @ text_render_wrapper r2 arg: shadow=1 color-mode-1; 30 ROM refs

@ Puzzle LP display constants
.equ PUZZLE_LP_DIGIT_TILE_BASE,       0x00001008  @ LP digit OAM tile base index; 71 ROM refs
.equ PUZZLE_LP_MAX,                   0x00002710  @ LP display max cap (+10000); 68 ROM refs
.equ PUZZLE_LP_STEP_1000,             0xfffffc18  @ -1000 (s32): LP step-down per display tick; 16 ROM refs
.equ PUZZLE_LP_NEG_10000,             0xffffd8f0  @ -10000 (s32): LP step-down 10000 single step; 1 ROM ref

@ =============================================================================
@ file 02 Seg-1 additions: label render ctx / dual label / text render flag
@ =============================================================================

.equ TEXT_RENDER_FLAG_LAYER2,         0x00008002  @ text render layer 2 flag; 21 ROM refs
.equ DUAL_LABEL_RENDER_STATE_CLEAR,   0xFFFC7FFF  @ clears bits[17:15] of scene_ctx+0x38 render state; 31 ROM refs
.equ LABEL_CTX_RENDER_STATE_CLEAR,    0xFFFFFC7F  @ clears 2 bits from slot render state (distinct from CAMPAIGN_CARD_ANIM_STEP_MASK); 1 ROM ref
.equ LABEL_CTX_DISPLAY_PARAM,         0x00A00030  @ display param for label render ctx init; 1 ROM ref

@ =============================================================================
@ file 02 Seg-2 additions: equip chain / duel field slot constants
@ =============================================================================

@ Equip chain node pool geometry
.equ EQUIP_NODE_BASE_OFFSET,  0x000014b0  @ positive offset from gDuelFieldSlots to gEquipNodePool (0x1d9c0-0x1c510=0x14b0); 4 refs
.equ NODE_POOL_NEG_OFFSET,    0xffffeb50  @ neg offset (-0x14b0) from gEquipNodePool to gDuelFieldSlots base; 5 refs
.equ EQUIP_CHAIN_LINK_OFFSET, 0xfffffc02  @ chain link sub-array base offset within node (-0x3fe); 1 ref (append_equip_chain_node_at_tail)
.equ FIELD_SLOT_PHASE_MASK,   0xfffffc07  @ clears bits[9:3] of AOB state halfword (scene_ctx+0x60); 3 refs

@ =============================================================================
@ file 02 Seg-5 additions: duel field zone slot / player active index constants
@ =============================================================================
.equ FIELD_SLOT_COUNT_OFF,      0x00001cb4  @ gDuelFieldSlots+0x1cb4: total placed-card count (7 ROM refs; 2 Seg-5 slots)
                                             @ incremented by place_card_into_monster_zone_slot / place_card_into_spelltrap_zone_slot
.equ SLOT_FACE_STATUS_ARRAY_OFF, 0x000010b1 @ gDuelFieldSlots+0x10b1: equip_face_bits status byte array base (16 ROM refs; 2 slots)
.equ FIELD_SPELL_CARD_REF_OFF,  0x00001390  @ card_id 0x1390 field-spell equip trigger guard (10 ROM refs; 1 slot)
.equ DUEL_ACTIVE_PLAYER_OFF,    0x00001cb8  @ gP1LifePoints+0x1cb8: active turn player idx (15 ROM refs; 1 slot)

@ =============================================================================
@ file 02 Seg-6 additions: equip slot active-state tag
@ =============================================================================
.equ EQUIP_SLOT_ACTIVE_TAG,     0xa5600000  @ packed slot word tag: slot[0]<<19==this -> equip slot active/live; 5 raw refs; 1 Seg-6 slot

@ =============================================================================
@ file 02 Seg-7 additions: effect zone offset constants
@ =============================================================================
.equ EFFECT_ZONE_PARTITION_OFF, 0x000010a4  @ gDuelFieldSlots+0x10a4 = effect zone slot array base offset (0x0201d5b4); 18 raw refs
.equ EFFECT_ZONE_BITMASK_OFF,   0x000010d0  @ gDuelFieldSlots+0x10a0 = effect zone occupation bitmask word offset; 45 raw refs
                                             @ (used as: r10=gDuelFieldSlots-0x30; r10+0x10d0=gDuelFieldSlots+0x10a0=0x0201d5b0)
