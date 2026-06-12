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
