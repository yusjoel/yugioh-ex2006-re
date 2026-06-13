@ =============================================================================
@ OAM attribute (硬件 OAM 项) 字段位掩码常量
@ 用于 cell-anim OAM 构建簇 (setup_isd_cell_anim_oam_entry 0x08015954) 对暂存缓冲
@ gOamAttrBuildBuf 内每个 OAM 项的 attr2 char-name 字段做 tile-base 重映射。
@ 经 ExportRangeToGas.resolve_word_equate 导出符号; GAS 用本表 .equ 解析回同值 -> byte-identical。
@
@ OAM attr2 格式: bits[9:0]=char name (tile index) / bits[11:10]=priority / bits[15:12]=palette。
@ =============================================================================

.equ OAM_ATTR2_CHARNAME_MASK,  0x000003ff  @ 保留 attr2 bits[9:0] (char name = tile index)
.equ OAM_ATTR2_CHARNAME_CLEAR, 0xfffffc00  @ 清 attr2 bits[9:0] (插入 tile-base 重映射前)

.equ OAM_ATTR0_HIDDEN,         0x0000ffff  @ attr0 all-bits-set: OBJ disabled/hidden mode
                                             @ used by apply_sprite_gfx_by_type for initial hide

.equ OAM_HFLIP_VFLIP_PACKED_PATTERN, 0x40004000  @ bit14 set in both attr0 and attr1 halfwords (packed as 32-bit word)
                                                   @ ORed into 32-bit OAM entry to toggle hflip+vflip
.equ OAM_ATTR1_X_MASK,  0x000001ff  @ attr1 bits[8:0] = x coordinate (9-bit x-pos field)
.equ OAM_ATTR1_X_CLEAR, 0xfffffe00  @ clear attr1 bits[8:0] before inserting x-pos

@ =============================================================================
@ file 02 Seg-6 additions: OAM attr2 tile-field clear mask
@ =============================================================================
.equ OAM_ATTR2_TILE_CLEAR, 0xffffe000  @ AND mask clearing OAM attr2 bits[12:0] before inserting new tile/set_code; 31 raw refs; 3 Seg-6 slots

@ =============================================================================
@ file 04 Seg-4 additions: OAM sprite palette selector P1
@ =============================================================================
.equ OAM_SPRITE_PAL_P1,            0x00008036  @ OAM sprite attr0 palette selector for player 1 (bit15=1, group 0x36+bit15); enqueue_sprite_attr_with_mode + enqueue_slot_card_sprite_if_eligible; 258 ROM refs; 1 Seg-4 slot

@ =============================================================================
@ file 04 Seg-5 additions: OAM palette selectors + sprite attr-word clear masks
@ =============================================================================
.equ OAM_EQUIP_CHAIN_SPRITE_P1,     0x00008037  @ equip chain node OAM attr0 P1 (bit15+0x37); 11 raw ROM refs; enqueue_equip_chain_slot_sprite_attr
.equ OAM_CHAIN_MATCH_SPRITE_P1,     0x00008038  @ chain match OAM attr0 P1 (bit15+0x38); 82 raw ROM refs; enqueue_equip_chain_sprite_by_side
.equ OAM_ZONE_TYPE_SPRITE_P1,       0x00008042  @ zone card-type OAM attr0 P1 (bit15+0x42); 48 raw ROM refs; enqueue_zone_slot_sprite_attr_by_card_type
.equ OAM_ZONE_CARD_SPRITE_P1,       0x00008035  @ zone occupied card OAM attr0 P1 (bit15+0x35); 8 raw ROM refs; enqueue_slot_sprite_by_state_and_type
.equ OAM_SPRITE_ATTR_CLR_BIT9,      0xfffffdff  @ AND mask clears bit9 (player_side) of OAM sprite attr word; 480 raw ROM refs; enqueue_slot_sprite_attr_by_card_type_and_state
.equ OAM_SPRITE_ATTR_CLR_BITS13_10, 0xffffc3ff  @ AND mask clears bits[13:10] (slot_idx 4-bit field); 27 raw ROM refs; enqueue_slot_sprite_attr_by_card_type_and_state
.equ OAM_SPRITE_ATTR_CLR_BIT16,     0xfffeffff  @ AND mask clears bit16 (flip flag) of OAM sprite attr word; 1475 raw ROM refs; enqueue_slot_sprite_attr_by_card_type_and_state
.equ OAM_SPRITE_ATTR_CLR_BIT17,     0xfffdffff  @ AND mask clears bit17 (composite sprite flag); 448 raw ROM refs; enqueue_slot_sprite_attr_by_card_type_and_state

@ =============================================================================
@ file 04 Seg-6 additions: OAM equip/zone sprite palette selectors P1
@ =============================================================================
.equ OAM_EQUIP_SLOT_SPRITE_P1,      0x00008034  @ equip slot activation OAM attr0 P1 (bit15+0x34); apply_slot_equip_activation_with_sprite; P0 path=0x34; 19 raw ROM refs
.equ OAM_EQUIP_ZONE_SPRITE_P1,      0x00008033  @ equip zone sprite OAM attr0 P1 (bit15+0x33); enqueue_equip_zone_sprite_direct + dispatch_equip_zone_sprite_and_activation; P0=0x33; 40 raw ROM refs
.equ OAM_EQUIP_CHAIN_PAIR_SPRITE_P1, 0x0000803d @ equip chain pair sprite OAM attr0 P1 (bit15+0x3d); enqueue_equip_chain_pair_sprite_if_eligible; P0=0x3d; 76 raw ROM refs
.equ OAM_EQUIP_CHAIN_DUAL_SPRITE_P1, 0x0000803e @ equip chain dual-slot sprite OAM attr0 P1 (bit15+0x3e); enqueue_equip_chain_dual_slot_sprite_with_activation_scan; P0=0x3e; 121 raw ROM refs
.equ OAM_ZONE_EQUIP_SPRITE_P1,      0x00008045  @ zone equip shape sprite OAM attr0 P1 (bit15+0x45); dispatch_equip_zone_sprite_and_activation; P0=0x45; 166 raw ROM refs

@ =============================================================================
@ file 04 Seg-7 additions: P2 equip/zone sprite palette selectors
@ =============================================================================
.equ OAM_EQUIP_SLOT_SPRITE_P2,      0x00008029  @ OAM attr0 P2 for equip slot sprite (bit15+0x29; P1=0x8034); 5 slots in Seg-7; 121 raw ROM refs
.equ OAM_MULTI_SLOT_MARKER_P2,      0x00008048  @ OAM attr0 P2 for multi-slot selection marker sprite (bit15+0x48; P1=0x48 inline); enqueue_equip_multi_slot_marker_sprite; 12 raw ROM refs
.equ OAM_FIELD_SLOT_SPRITE_P2,      0x00008043  @ OAM attr0 P2 for duel field slot sprite (bit15+0x43; P1=0x43 inline); enqueue_field_slot_sprite_with_state_update; 35 raw ROM refs

@ =============================================================================
@ file 04 Seg-8a additions: xy-split / equip-set-slot / effect-card-slot sprite attr1 pairs
@ bit15=H-flip = player-2 indicator; P1 variants encoded inline as imm (0x3a/0x3b/0x3c)
@ =============================================================================
.equ OAM_XY_SPLIT_SPRITE_P1,        0x0000003a  @ xy-split sprite OAM attr1; player 1 (no H-flip); inline imm
.equ OAM_XY_SPLIT_SPRITE_P2,        0x0000803a  @ xy-split sprite OAM attr1; player 2 (bit15=H-flip); 2 pool refs in Seg-8a
.equ OAM_EQUIP_SET_SLOT_P1,         0x0000003b  @ equip-set slot sprite OAM attr1; player 1; inline imm
.equ OAM_EQUIP_SET_SLOT_P2,         0x0000803b  @ equip-set slot sprite OAM attr1; player 2; 2 pool refs in Seg-8a
.equ OAM_EFFECT_CARD_SLOT_P1,       0x0000003c  @ effect-card slot sprite OAM attr1; player 1; inline imm
.equ OAM_EFFECT_CARD_SLOT_P2,       0x0000803c  @ effect-card slot sprite OAM attr1; player 2; 4 pool refs in Seg-8a
.equ EQUIP_PAIR_SPRITE_EXTRA,        0x00000101  @ equip pair sprite attr extra field: type=1, mode=1; r3 arg to enqueue_sprite_attr_record in enqueue_equip_card_sprite_attr_for_slot; 1 pool ref

@ =============================================================================
@ file 04 Seg-8b additions: zone effect / equip zone OAM clear masks + effect sprite attr
@ =============================================================================
.equ OAM_SPRITE_ATTR_CLR_BIT18,     0xfffbffff  @ AND mask clearing bit18 (zone effect flag) of OAM sprite attr word; 687 raw ROM refs; handle_card_effect_zone_eligibility_by_field6
.equ OAM_SPRITE_ATTR_CLR_BITS22_19, 0xff87ffff  @ AND mask clearing OAM sprite attr bits[22:19] (equip zone shape field); 14 raw ROM refs
.equ OAM_EFFECT_ZONE_SPRITE_P1,     0x00008031  @ OAM attr0 P1 for zone effect card sprite (bit15+0x31); handle_card_effect_zone_eligibility_by_field6 field8==9 path; 55 raw ROM refs

@ =============================================================================
@ file 04 Seg-10 additions: P2 OAM attr0 palette selectors + sprite-word clear masks
@ =============================================================================
.equ OAM_SLOT_SPRITE_P2,             0x00008032  @ P2 duel slot sprite attr0 (bit15+0x32; P1=0x32 inline); render_slot_card_sprite_from_descriptor; 42 raw refs
.equ OAM_ZONE_CARD_ID_SPRITE_P2,     0x0000802e  @ P2 zone card-id sprite attr0 (bit15+0x2e; P1=0x2e inline); enqueue_sprite_attr_for_zone_card_id_lookup; 3 raw refs
.equ OAM_SIGN_SPRITE_P2,             0x00008030  @ P2 sign/palette sprite attr0 (bit15+0x30; P1=0x30 inline); enqueue_sprite_attr_by_sign; 113 raw refs
.equ OAM_EQUIP_ZONE_SIDE_P2,         0x0000802f  @ P2 equip zone side sprite attr0 (bit15+0x2f; P1=0x2f inline); enqueue_equip_zone_sprite_by_side; 142 raw refs
.equ OAM_SLOT_INDICATOR_P2,          0x0000802b  @ P2 slot occupied-indicator sprite attr0 (bit15+0x2b; P1=0x2b inline); enqueue_sprite_attr_for_slot_indicator; 13 raw refs
.equ OAM_POSITION_ATTR_P2,           0x00008026  @ P2 LP position sprite attr0 (bit15+0x26; P1=0x26 inline); enqueue_sprite_attr_position_by_player; 315 raw refs
.equ OAM_SPRITE_COUNT_P2,            0x00008025  @ P2 sprite count extended mode attr0 (bit15+0x25); enqueue_sprite_attr_clamped + enqueue_sprite_attr_record_with_cap + submit_lp_change_indicator; 4 raw refs
.equ OAM_SPRITE_ATTR_CLR_BITS20_17,  0xffe1ffff  @ AND mask clearing OAM attr bits[20:17] (equip_state 4-bit field); setup_equip_slot_sprite_attr_by_card; 5 raw refs
.equ OAM_SPRITE_ATTR_CLR_BITS25_22,  0xfc3fffff  @ AND mask clearing OAM attr bits[25:22] (mode 4-bit field); setup_equip_slot_sprite_attr_by_card; 6 raw refs
.equ OAM_SPRITE_ATTR_CLR_BIT26,      0xfbffffff  @ AND mask clearing OAM attr bit26; setup_equip_slot_sprite_attr_by_card; 1559 raw refs

@ =============================================================================
@ file 05 Seg-1 additions: LP/zone/equip/effect slot sprite P1 tile attr0 values
@ Y-coordinate encodes sprite group; bit15 set = OBJ_DIS (P1 convention)
@ Source: asm/05_equip_eligibility_a.s, Seg-1 (0x08049014..0x0804a5b8)
@ =============================================================================
@ Sprite tile attr0 P2/P1 pairs (bit15=OBJ_DISABLE for P1 odd convention)
.equ OAM_LP_ZONE_SPRITE_P2,           0x00000024  @ LP zone sprite tile P2 (Y=0x24)
.equ OAM_LP_ZONE_SPRITE_P1,           0x00008024  @ LP zone sprite tile P1 (Y=0x24 | OBJ_DIS)
.equ OAM_LP_COUNTER_P2,               0x00000053  @ LP counter sprite P2 (Y=0x53)
.equ OAM_LP_COUNTER_P1,               0x00008053  @ LP counter sprite P1 (Y=0x53 | OBJ_DIS)
.equ OAM_ZONE_UPDATE_SPRITE_P2,       0x00000054  @ Zone update sprite tile P2 (Y=0x54)
.equ OAM_ZONE_UPDATE_SPRITE_P1,       0x00008054  @ Zone update sprite tile P1 (Y=0x54 | OBJ_DIS)
.equ OAM_EQUIP_SLOT_TILE_P2,          0x00000055  @ Equip slot tile P2 (Y=0x55)
.equ OAM_EQUIP_SLOT_TILE_P1,          0x00008055  @ Equip slot tile P1 (Y=0x55 | OBJ_DIS)
.equ OAM_EFFECT_SLOT_TILE_P2,         0x00000056  @ Effect slot tile P2 (Y=0x56)
.equ OAM_EFFECT_SLOT_TILE_P1,         0x00008056  @ Effect slot tile P1 (Y=0x56 | OBJ_DIS)
.equ OAM_LP_FIELD_STATE_P2,           0x00000057  @ LP field state sprite P2 (Y=0x57)
.equ OAM_LP_FIELD_STATE_P1,           0x00008057  @ LP field state sprite P1 (Y=0x57 | OBJ_DIS)
.equ OAM_DUEL_CARD_SLOT_P2,           0x0000004d  @ Duel card slot sprite P2 (Y=0x4d)
.equ OAM_DUEL_CARD_SLOT_P1,           0x0000804d  @ Duel card slot sprite P1 (Y=0x4d | OBJ_DIS)
.equ OAM_SLOT_SPRITE_BY_PLAYER_P2,    0x0000004f  @ Slot sprite by player P2 (Y=0x4f)
.equ OAM_SLOT_SPRITE_BY_PLAYER_P1,    0x0000804f  @ Slot sprite by player P1 (Y=0x4f | OBJ_DIS)
.equ OAM_SPRITE_TYPE_SEL_P2,          0x00000050  @ Sprite type select P2 (Y=0x50)
.equ OAM_SPRITE_TYPE_SEL_P1,          0x00008050  @ Sprite type select P1 (Y=0x50 | OBJ_DIS)
.equ OAM_ZONE_ELIGIBLE_P2,            0x00000051  @ Zone eligible sprite P2 (Y=0x51)
.equ OAM_ZONE_ELIGIBLE_P1,            0x00008051  @ Zone eligible sprite P1 (Y=0x51 | OBJ_DIS)
.equ OAM_CARD_SLOT_SPRITE,            0x00000058  @ Card slot sprite (Y=0x58; enqueue_sprite_attr_for_card_slot)
@ Bit-clear masks (complement existing OAM_SPRITE_ATTR_CLR_BIT* series)
.equ OAM_SPRITE_ATTR_CLR_BIT11,       0xfffff7ff  @ AND mask clearing bit11 of OAM sprite attr word
.equ OAM_SPRITE_ATTR_CLR_BIT10,       0xfffffbff  @ AND mask clearing bit10 of OAM sprite attr word
.equ OAM_ATTR2_PAL_CLEAR,             0xffff0fff  @ AND mask clearing OAM attr2 bits[15:12] (palette field)
@ attr2 OR masks for sprite palette/shape configuration (hi16 applied as OR mask)
.equ OAM_ATTR2_OR_0X3250,             0x32500000  @ OAM attr2 packed OR mask hi16=0x3250
.equ OAM_ATTR2_OR_0X3220,             0x32200000  @ OAM attr2 packed OR mask hi16=0x3220
.equ OAM_ATTR2_OR_0X384E,             0x384e0000  @ OAM attr2 packed OR mask hi16=0x384e
.equ OAM_ATTR2_OR_0X3C4E,             0x3c4e0000  @ OAM attr2 packed OR mask hi16=0x3c4e

@ =============================================================================
@ file 05 Seg-2 additions: player-state and field-slot sprite bit P1 attr0 values
@ bit15 set = OBJ_DIS (P1 convention); low byte = OAM Y coordinate
@ Source: asm/05_equip_eligibility_a.s, Seg-2 (0x0804a5b8..0x0804ad48)
@ =============================================================================
.equ OAM_PLAYER_STATE_BIT_SPRITE_P1,  0x00008022  @ P1 OAM attr0 Y-coord for player-level state bit change sprite (bit15+0x22); set_player_state_bit_with_sprite_update; P2=0x22 inline; 29 raw ROM refs
.equ OAM_FIELD_SLOT_BIT_SPRITE_P1,    0x0000802a  @ P1 OAM attr0 Y-coord for field slot bit change sprite (bit15+0x2a); set_field_slot_bit_with_sprite_update; P2=0x2a inline; 233 raw ROM refs

@ =============================================================================
@ file 05 Seg-5 additions: OAM attr2 tile-field clear mask + hidden sprite attr
@ =============================================================================
.equ OAM_ATTR2_CLR_BITS_11_6,  0xfffff03f  @ AND mask clearing bits[11:6]; used to clear OAM char-name tile index field in sprite row packing (submit_slot_card_sprite_row_entry + init variants); 14 ROM refs
.equ SPRITE_ATTR_TYPE_HIDDEN_Y97, 0x00008061 @ OBJ disabled (bit15=1) | Y=0x61 (97); passed to enqueue_sprite_attr_record when eligib_sprite_ctrl [gP1LP+ELIGIB_SPRITE_CTRL_OFF] != 0; contrast 0x0061 (OBJ enabled) when field==0; 81 ROM refs
