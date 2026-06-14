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

@ =============================================================================
@ file 02 Seg-10a additions: slot activation state write offsets
@ =============================================================================
.equ ACTIVATION_STATE_A_OFF,   0x00001d48  @ gP1LifePoints+side*0x868+0x1d48: activation state field A;
                                            @ written 0x3 on bit21-set guard fail; 27 raw refs; 2 Seg-10a slots
.equ ACTIVATION_STATE_B_OFF,   0x00001d78  @ gP1LifePoints+side*0x868+0x1d78: activation state field B;
                                            @ written 0x13 on exit_slot_activation_with_state_write; 41 raw refs; 3 Seg-10a slots
.equ ACTIVE_EFFECT_CATEGORY_OFF, 0x000010d8 @ gP1LifePoints+0x10d8=0x0201D5B8: active effect slot category word;
                                             @ read by check_card_matches_active_effect_slot; 16 raw refs; 1 Seg-10a slot

@ =============================================================================
@ file 02 Seg-10b additions: field5 score activation thresholds
@ =============================================================================
.equ FIELD5_SCORE_ACTIVATION_THRESHOLD, 0x0000076b  @ get_slot_field5_score return > this -> not activatable in eval_slot_activation_eligibility_full; 8 raw refs
.equ FIELD5_SCORE_FIELDSPELL_THRESHOLD, 0x0000063f  @ get_slot_field5_score return <= this -> not activatable in eval_slot_fieldspell_activation_full; 3 raw refs

@ =============================================================================
@ file 03 Seg-1 additions: equip slot / phase lock / node pool offset constants
@ =============================================================================
.equ PHASE_LOCK_FLAG_OFF,           0x000004bc  @ gDuelPhaseFlags+0x4bc = phase lock global inhibit byte; 11 raw refs; check_zone_slot_equip_prerequisites
.equ EQUIP_SLOT_CARD_ID_RANGE_MAX,  0x00001388  @ upper bound for Horus-adjacent equip block card_id range [0x1386..0x1388]; not in card-stats.s; 28 raw refs
.equ NODE_POOL_TO_SLOT_STATE_OFF,   0xffffeb60  @ gEquipNodePool+0xffffeb60 = gDuelFieldSlotState (= gDuelFieldSlots+0x10); distinct from NODE_POOL_NEG_OFFSET=0xffffeb50; 2 raw refs (both Seg-1)

@ =============================================================================
@ file 03 Seg-3 additions: field array C to count neg offset
@ =============================================================================
.equ FIELD_ARRAY_C_TO_COUNT_NEG_OFF, 0xfffffeec  @ gP1FieldArrayCBase (0x0201c600) + 0xfffffeec = gP1ZoneHandCount (0x0201c4ec); neg delta -0x114 from field array C to count base; used per-player: (gP1FieldArrayCBase+player*0x868) + this = count_ptr; 10 raw refs; 1 Seg-3 slot

@ =============================================================================
@ file 03 Seg-4b additions: eval_slot_score_entry_full LP / score delta constants
@ =============================================================================
.equ LP_COST_3000,              0x00000bb8  @ 3000 LP cost threshold; used in eval_slot_score_entry_full LP-cost branch; 3 Seg-4b slots
.equ LP_COST_1500,              0x000005dc  @ 1500 LP cost threshold; used in eval_slot_score_entry_full LP-cost branch; 1 Seg-4b slot
.equ SCORE_DELTA_NEG_300,       0xfffffed4  @ -300 ATK/DEF score delta; apply_slot_score_bonus_by_state / adjust_slot_score_by_chain_and_zone; 2 Seg-4b slots
.equ SCORE_DELTA_NEG_500,       0xfffffe0c  @ -500 ATK/DEF score delta; apply_slot_score_bonus_by_state; 1 Seg-4b slot
.equ SCORE_DELTA_NEG_700,       0xfffffd44  @ -700 ATK/DEF score delta; adjust_slot_score_by_chain_and_zone; 1 Seg-4b slot
.equ FIELD_STATE_OFF,           0x00001cf4  @ gDuelFieldSlots+0x1cf4: equip activation phase/field state code;
                                            @ confirmed: asm/04 INIT_VAL_OFFSET=0x1cf4, asm/06 AUX_OFFSET_CF4, asm/07 STAGE_OFF/FIELD_STATE_OFFSET; 2 Seg-4b slots
.equ CHAIN_LINK_COUNTER_OFF,    0x00001cbc  @ gDuelFieldSlots+0x1cbc: chain link counter in equip chain;
                                            @ confirmed: asm/08 CHAIN_LINK_COUNTER_OFFSET=0x1cbc; 1 Seg-4b slot
.equ EQUIP_PHASE_STATE_OFF,     0x00001cc4  @ gDuelFieldSlots+0x1cc4: equip activation sub-phase state (compared to 2/3/4 in asm/12); med-conf; 1 Seg-4b slot

@ =============================================================================
@ file 03 Seg-7 additions: display sequence state offsets + sprite attr offsets
@ =============================================================================
.equ DISPLAY_SEQ_SLOT_IDX_OFF,      0x00000808  @ [gDuelDisplaySeqState+0x808] sprite write slot index; bounds-checked vs 0xff; 363 raw refs
.equ DISPLAY_SEQ_STEP_LOCK_OFF,     0x0000080c  @ [gDuelDisplaySeqState+0x80c] step lock / state clear flag; written 0 at end of every display seq handler; 178 raw refs
.equ DISPLAY_SEQ_ACTIVE_PLAYER_OFF, 0x00001d10  @ [gP1LifePoints+0x1d10] active player field in display seq; 25 raw refs
.equ DISPATCH_ACTIVE_FLAG_OFF,      0x00001d38  @ [gP1LifePoints+0x1d38] display dispatch in-progress flag; set :=1 at dispatch_duel_event_display_seq entry; 4 raw refs
.equ ACTIVATION_STATE_C_OFF,        0x00001d4c  @ [gP1LifePoints+0x1d4c] activation state field C; checked ==0 before play_ui_effect(0x31/0x32); distinct from A=0x1d48/B=0x1d78; 4 raw refs
.equ SPRITE_ATTR_FIELD1_OFF,        0x00000306  @ [gSpriteAttrBuf+0x306] sprite attr halfword 1; strh write in write_sprite_attr_record_entry; 56 raw refs
.equ SPRITE_ATTR_FIELD3_OFF,        0x0000030a  @ [gSpriteAttrBuf+0x30a] sprite attr halfword 3; strh write in write_sprite_attr_record_entry; 23 raw refs

@ =============================================================================
@ file 03 Seg-8 additions: slot active-bit masks + equip chain offsets + display seq offsets
@ =============================================================================
.equ SLOT_ACTIVE_BIT22_CLR,       0xffbfffff  @ AND mask clearing bit22 of zone slot word (chain-linked flag); tick_equip_chain_slot_ref_scan_seq asm 14365; 413 raw ROM refs
.equ SLOT_ACTIVE_BIT23_CLR,       0xff7fffff  @ AND mask clearing bit23 of zone slot word (chain-type flag); tick_equip_chain_slot_ref_scan_seq asm 14367; 188 raw ROM refs
.equ EQUIP_CHAIN_STEP_OFF,        0x00001d28  @ [gP1LifePoints+player*0x868+0x1d28] equip chain state step field; values: 0x6=activate, 0x9=ai_init, 0xb=ready, 0xc=finalize; 31 raw ROM refs
.equ EQUIP_CHAIN_ACTIVE_OFF,      0x00001d2c  @ [gP1LifePoints+player*0x868+0x1d2c] equip chain active player side flag; 0/1; 95 raw ROM refs
.equ SLOT_ACTIVE_BIT15_CLR,       0xffff7fff  @ AND mask clearing bit15 of zone slot display descriptor word; used in zone placement functions; 188 raw ROM refs
.equ SLOT_ACTIVE_BIT14_CLR,       0xffffbfff  @ AND mask clearing bit14 of zone slot display descriptor word; used alongside SLOT_ACTIVE_BIT15_CLR; 413 raw ROM refs
.equ SLOT_BITS14_15_CLR,          0xfffe7fff  @ AND mask clearing bits 14+15 simultaneously (=SLOT_ACTIVE_BIT14_CLR & SLOT_ACTIVE_BIT15_CLR); 6 raw ROM refs
.equ DISP_SEQ_STEP_LOCK_A_OFF,    0x0000080a  @ [gDuelDisplaySeqState+0x80a] secondary step lock A; cleared at step 2 in tick_zone_card_place_display_seq; 9 raw ROM refs
.equ DISP_SEQ_ALT_CTR_OFF,        0x0000080e  @ [gDuelDisplaySeqState+0x80e] step counter for alt zone-card-place and normal-summon sequences; 14 raw ROM refs
.equ DISP_SEQ_CARD_SET_CTR_OFF,   0x00000818  @ [gDuelDisplaySeqState+0x818] step counter for card-set display sequence; tick_zone_slot_card_set_display_seq; 26 raw ROM refs
.equ SLOT_BIT21_CLR,              0xffdfffff  @ AND mask clearing bit21 of zone slot word (equip-active bit); tick_zone_slot_card_set_display_seq asm 16670; 215 raw ROM refs

@ =============================================================================
@ file 03 Seg-9 additions: display context slot data mask
@ =============================================================================
.equ DISPLAY_CTX_SLOT_DATA_MASK,  0x00007fff  @ masks bit15 (player_id) from [gDuelDisplaySeqState+4] hword to extract slot_data field; write_zone_slot_display_args_by_state; 1 slot

@ =============================================================================
@ file 03 Seg-10 additions: zone slot chain-counter and bit20 clear masks
@ =============================================================================
.equ SLOT_CHAIN_CTR_CLR,          0xc03fffff  @ ~0x3fc00000; clears bits[29:22] chain-counter field in slot display-args word; place_card_to_zone_with_display_state; 1 slot
.equ SLOT_BIT20_CLR,              0xffefffff  @ ~0x00100000; clears bit20 of spell-trap zone slot entry word; place_card_to_zone_with_display_state; 1 slot

@ =============================================================================
@ file 04 Seg-1 additions: display mode variant / set-display state / equip main-phase / hand slot face-status
@ =============================================================================
.equ DISP_SET_VARIANT_OFF,        0x00001cfc  @ [gP1LifePoints+0x1cfc] display mode variant (1=A / 2=B); tick_set_display_mode_seq; asm/12:808 sprite_variant_offset; 19 raw refs
.equ SET_DISPLAY_STATE_SLOT_OFF,  0x00000894  @ [gP1LifePoints+0x894] set-mode display state slot; tick_set_display_mode_seq writes hword[gDuelDisplaySeqState+6]; 7 raw refs
.equ EQUIP_MAIN_PHASE_OFF,        0x00001d18  @ [gP1LifePoints+0x1d18] equip activation main-phase dispatch index; tick_equip_activation_dispatch_hub; asm/12:1490 main_phase_offset; 17 raw refs
.equ HAND_SLOT_FACE_ARRAY_OFF,    0x0000041a  @ gP1LifePoints+0x41a = gP1HandSlotArray+2 (0x0201c8fa): face-status byte-2 in hand slot entry (4B stride); tick_display_slot_flag_clear_seq ORs 0x10; 9 raw refs
.equ ALT_HAND_SLOT_FACE_ARRAY_OFF,0x000005d2  @ gP1LifePoints+0x5d2 = gP1AltHandSlotArray+2 (0x0201cab2): face-status byte-2 in alt-hand slot entry; symmetric; 3 raw refs

@ =============================================================================
@ file 04 Seg-4 additions: equip chain step base offset
@ =============================================================================
.equ EQUIP_CHAIN_STEP_BASE_OFF,     0x00001130  @ [gEquipChainSlotRefs+0x1130] equip chain refs step array base; tick_equip_chain_count_check_sequence passes to replace_equip_chain_slot_refs_by_match; 9 ROM refs; 1 Seg-4 slot

@ =============================================================================
@ file 04 Seg-7 additions: equip multi-slot control word offset
@ =============================================================================
.equ EQUIP_MULTI_SLOT_CTL_OFF,      0x00001ce0  @ [gP1LifePoints+0x1ce0] equip multi-slot selection control word; enqueue_equip_multi_slot_marker_sprite reads display flags r7; computed as 0xe7<<5; 1 raw ROM ref

@ =============================================================================
@ file 04 Seg-8a additions: equip chain slot refs list terminator sentinel
@ =============================================================================
.equ EQUIP_CHAIN_SENTINEL,          0xffff0000  @ gEquipChainSlotRefs list terminator sentinel; cmp rval, EQUIP_CHAIN_SENTINEL; beq exit loop; 3 pool refs in Seg-8a

@ =============================================================================
@ file 04 Seg-8b additions: equip target bitmap control word offset
@ =============================================================================
.equ EQUIP_BITMAP_CTRL_OFF,         0x000010d4  @ [gP1LifePoints+0x10d4] equip target bitmap control word; update_equip_target_bitmap_for_field writes combined sprite flags; 12 ROM refs

@ =============================================================================
@ file 04 Seg-10 additions: field copy count flag + equip zone effect attr OR mask
@ =============================================================================
.equ FIELD_COPY_COUNT_FLAG,          0x00010002  @ bit0=mode2,bit16=field_copy_exists; anded with count_field_copies_of_card return to detect duplicate presence; 740 raw refs
.equ EQUIP_ZONE_EFFECT_ATTR_OR,      0x1e501511  @ packed OR mask for find_effect_node_in_zone hit path; low16=0x1511 type; high16=0x1e50 mode; 1 pool ref; conf LOW

@ =============================================================================
@ file 05 Seg-2 additions: equip zone sprite x-position delta constants
@ Used by enqueue_monster_zone_equip_sprites_and_lp_counters to compute
@ sprite x-coordinates for equip zone rendering in monster zone row.
@ =============================================================================
.equ EQUIP_SPRITE_X_DELTA_A,   0xffffe730  @ neg x-position delta A for equip zone sprite in monster zone row; enqueue_monster_zone_equip_sprites_and_lp_counters; 3 raw ROM refs
.equ EQUIP_SPRITE_X_DELTA_B,   0xffffe32c  @ neg x-position delta B for equip zone sprite in monster zone row (player-stride variant); enqueue_monster_zone_equip_sprites_and_lp_counters; 1 raw ROM ref

@ =============================================================================
@ file 05 Seg-8 additions: equip slot card type field masks
@ Used in check_equip_slot_eligible_by_card_id_score (0x080517b4) type filter:
@ bits[11:6] of card[+2] halfword; (slot_word & 0xfc0) must be 0x180 or 0x1c0
@ =============================================================================
.equ SLOT_CARD_TYPE_MASK,       0x00000fc0  @ bits[11:6] type field in card[+2] halfword; lsls r1,#0xfc<<4=0xfc0; check_equip_slot_eligible_by_card_id_score inner filter; med-conf; 1 Seg-8 slot
.equ SLOT_CARD_TYPE_ELIGIBLE_A, 0x00000180  @ eligible slot type value A; lsls r0,#0xc0<<1=0x180; check_equip_slot_eligible_by_card_id_score; med-conf; 1 Seg-8 slot
.equ SLOT_CARD_TYPE_ELIGIBLE_B, 0x000001c0  @ eligible slot type value B; ELIGIBLE_A+0x40=0x1c0; check_equip_slot_eligible_by_card_id_score; med-conf; 1 Seg-8 slot

@ =============================================================================
@ file 06 Seg-2 additions: equip flag target ICID table offset
@ Source: asm/06_equip_eligibility_b.s, Seg-2 (check_equip_slot_eligible_by_card_specific_activation)
@ =============================================================================
.equ EQUIP_FLAG_TARGET_ICID_TABLE_OFF, 0x000010b0  @ gDuelFieldSlots+0x10b0: u16[] indexed by equip_slot[+0xa] (equip_flag); Roll Out! (0x1979) uses to resolve target card ICID; distinct from SLOT_FACE_STATUS_ARRAY_OFF=0x10b1 (byte array) by 1 byte; med-conf; 1 Seg-2 slot

@ =============================================================================
@ file 06 Seg-4 additions: equip activation step / trigger param / LP cost 5000 / equip zone sprite attr
@ Source: asm/06_equip_eligibility_b.s, Seg-4 (0x08055440..0x080565e8)
@ =============================================================================
.equ EQUIP_ACTIVATION_STEP_OFF, 0x000004ac  @ [gDuelPhaseFlags+0x4ac] equip activation state machine step counter; values 0/1/2 in tick_equip_activation_state_machine; 0xa/0xb in type8_entry wrapper; 4 Seg-4 slots; conf: high
.equ TRIGGER_OP_PARAM_107,      0x00000107  @ trigger_card_display_op31_if_not_active second arg; asm/06 line 6925; 1 Seg-4 slot; conf: med
.equ LP_COST_5000,              0x00001388  @ get_card_lp_cost_by_id return 5000 LP; asm/06 line 5697; distinct from EQUIP_SLOT_CARD_ID_RANGE_MAX=0x1388 (card_id domain) and gap CID 0x1388 (score BST node); conf: high
.equ EQUIP_ZONE_SPRITE_ATTR,    0x00000fb6  @ enqueue_equip_zone_sprite_at_slot r2 arg to enqueue_sprite_attr_with_mode; 4022=0xfb6 sprite attr code; asm/06 line 6873; conf: high

@ Equip score literals (lookup_equip_card_score_by_card_id_and_player BST branch return values)
@ Mooyan Curry player 0/1 and A Rival Appears! player 1 scores:
.equ lookup_equip_score_mooyan_p0,        0x00000197  @ Mooyan Curry player 0 equip score; 1 Seg-4 slot
.equ lookup_equip_score_a_rival_appears_p1, 0x000001c7 @ A Rival Appears! player 1 equip score; 1 Seg-4 slot
.equ lookup_equip_score_mooyan_p1,        0x00000199  @ Mooyan Curry player 1 equip score; 1 Seg-4 slot
@ 22 neutral BST-branch score labels (0x1a5..0x1cf range):
.equ lookup_equip_score_b_0x1a5,          0x000001a5  @ BST branch score 0x1a5; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1a7,          0x000001a7  @ BST branch score 0x1a7; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1a9,          0x000001a9  @ BST branch score 0x1a9; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1ab,          0x000001ab  @ BST branch score 0x1ab; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1ad,          0x000001ad  @ BST branch score 0x1ad; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1af,          0x000001af  @ BST branch score 0x1af; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1b1,          0x000001b1  @ BST branch score 0x1b1; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1b3,          0x000001b3  @ BST branch score 0x1b3; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1b5,          0x000001b5  @ BST branch score 0x1b5; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1b7,          0x000001b7  @ BST branch score 0x1b7; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1b9,          0x000001b9  @ BST branch score 0x1b9; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1bf,          0x000001bf  @ BST branch score 0x1bf; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1c1,          0x000001c1  @ BST branch score 0x1c1; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1c3,          0x000001c3  @ BST branch score 0x1c3; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1c5,          0x000001c5  @ BST branch score 0x1c5; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1c9,          0x000001c9  @ BST branch score 0x1c9; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1cb,          0x000001cb  @ BST branch score 0x1cb; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1cd,          0x000001cd  @ BST branch score 0x1cd; 1 Seg-4 slot
.equ lookup_equip_score_b_0x1cf,          0x000001cf  @ BST branch score 0x1cf; 1 Seg-4 slot

@ =============================================================================
@ file 06 Seg-5 additions: equip sprite card-data constant and activation score mode codes
@ Source: asm/06_equip_eligibility_b.s Seg-5 (0x080565e8..0x08057458)
@ =============================================================================
.equ EQUIP_SPRITE_CARD_DATA,    0x00001119  @ r2 arg to enqueue_sprite_attr_with_mode(mode=3) in enqueue_equip_card_sprite_mode3; fixed card-data field 0x1119; 1 Seg-5 slot; conf: high
.equ EQUIP_ACT_SCORE_MODE_103,  0x00000103  @ set_equip_activation_state_by_mode mode code 0x103; loaded into r8 via mov r8,r0 (.hword 0x4680) in dispatch_equip_activation_score_by_card_id; 1 Seg-5 slot; conf: med
.equ EQUIP_ACT_SCORE_MODE_117,  0x00000117  @ set_equip_activation_state_by_mode mode code 0x117; loaded into r8 via mov r8,r1 (.hword 0x4688) in dispatch_equip_activation_score_by_card_id 0x15cf/Second Goblin path; 1 Seg-5 slot; conf: med

@ =============================================================================
@ file 06 Seg-6 additions: equip activation auxiliary offset + equip zone sprite attr mode1
@ Source: asm/06_equip_eligibility_b.s Seg-6 (0x08057458..0x08058550)
@ =============================================================================
.equ EQUIP_ACTIVATION_AUX_OFF,      0x000004b4  @ [gDuelPhaseFlags+0x4b4] equip activation secondary counter; distinct from EQUIP_ACTIVATION_STEP_OFF=0x4ac; 8 Seg-6 slots in tick_equip_slot_score_fill_display_seq; conf: high
.equ EQUIP_ZONE_SPRITE_ATTR_MODE1,  0x0000152a  @ enqueue_equip_zone_sprite_mode1 r2 arg to enqueue_sprite_attr_with_mode; mode=1 sprite attr code 0x152a; sibling of EQUIP_ZONE_SPRITE_ATTR=0x0fb6 (mode=2); distinct from Swarm of Scarabs CID=0x152a (different domain); 1 Seg-6 slot; conf: high

@ =============================================================================
@ file 06 Seg-7 additions: equip active context slot pointer offset
@ Source: asm/06_equip_eligibility_b.s Seg-7 (0x08058550..0x08058cec)
@ =============================================================================
.equ EQUIP_ACTIVE_CTX_OFF,          0x00000484  @ [gDuelPhaseFlags+0x484] current equip activation context slot ptr; 46 ROM refs; asm/06 L12851 ACTIVATION_OFFSET=0x484; asm/09 L17878 ACTIVE_NODE_OFFSET=0x484; asm/10 L15465 SLOT_SNAPSHOT_OFFSET=0x484; conf: high

@ =============================================================================
@ file 06 Seg-8 additions: OP31 effect node count sub-op code
@ Source: asm/06_equip_eligibility_b.s Seg-8 (0x08058cec..0x08059de0)
@ =============================================================================
.equ OP31_EFFECT_NODE_COUNT_CODE,   0x0000013d  @ invoke_card_display_op_0x31_sub10 first arg (sub-op code 0x13d); tick_equip_effect_node_count_display_seq L14826; distinct from LP_ROW_OFF=0x13e; conf: high

@ =============================================================================
@ file 06 Seg-10 additions: zone summon eligibility value
@ Source: asm/06_equip_eligibility_b.s Seg-10 (0x0805b480..0x0805c2f0)
@ =============================================================================
.equ ZONE_STATUS_SUMMON_ELIGIBLE,  0x0000201c  @ slot[+2] & ZONE_STATUS_MASK(0x303e) == 0x201c tests summon-eligible zone status; check_card_normal/special_summon_eligible_full; conf: med

@ =============================================================================
@ file 07 Seg-5 additions: zone detail field bit-field mask
@ Source: asm/07_equip_effect_chain.s Seg-5 (0x0805fc94..0x08060898)
@ =============================================================================
.equ ZONE_DETAIL_FIELD_MASK_F88, 0x00f88000  @ slot[+0x14] bits[23:11] mask; used with 0x708000 (0xe1<<15) expected value in check_equip_slot_eligible_neo_daedalus_with_zone_field_guard; 1 Seg-5 slot DAT_08060264; conf: high

@ =============================================================================
@ file 07 Seg-8 additions: ATK threshold constant
@ Source: asm/07_equip_effect_chain.s Seg-8 (0x08061eb4..0x08062d28)
@ =============================================================================
.equ ATK_THRESHOLD_2999, 0x00000bb7  @ ATK threshold 2999; cmp halfword[+0x14] vs 0xbb7; bls->fail means ATK must be >2999 (>=3000) to pass; distinct from LP_COST_3000=0xbb8; 4 ROM refs (0x8062084/0x80a0db0/0x80bb1fc/0x89143ac); Seg-8 DWORD_08062084 in check_equip_slot_eligible_zone_type3c0_high_atk_field5; conf: high
