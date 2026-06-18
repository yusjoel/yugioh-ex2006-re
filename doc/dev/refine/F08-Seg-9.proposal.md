# Refine Proposal: F08-Seg-9  [0x0806cbe8..0x0806d960)

## 段测绘
- 函数入口 x20:
  - 0x0806cbe8 tick_equip_target_query_display_seq
  - 0x0806cd40 dispatch_equip_lp_sprite_by_trap_card_id
  - 0x0806ce68 enqueue_equip_chain_slot_sprite_if_unlinked
  - 0x0806cf40 enqueue_zone_sprite_if_col_sum_equal_and_effect_active
  - 0x0806cfe8 dispatch_zone_sprite_by_slot_type_with_col_gate
  - 0x0806d0cc apply_equip_activation_for_all_player_slots
  - 0x0806d124 dispatch_neo_space_placement_by_card_id_and_state
  - 0x0806d224 submit_ring_of_destruction_lp_indicators_if_zone_matched
  - 0x0806d2d0 submit_effect_zone_sprites_if_unguarded
  - 0x0806d2f0 enqueue_dual_zone_slot_sprites_if_both_occupied
  - 0x0806d3d8 tick_equip_lp_display_state_by_zone_match
  - 0x0806d4a4 setup_equip_slot_oam_if_hand_slot_eligible
  - 0x0806d514 enqueue_zone_equip_sprite_if_slot_matches
  - 0x0806d5b0 set_field_slot_bit_if_zone_col_matches
  - 0x0806d618 enqueue_lp_chain_sprite_if_effect_slot_active
  - 0x0806d680 enqueue_spirit_zone_sprite_with_lp_check
  - 0x0806d6c0 enqueue_zone_equip_sprite_at_matching_slot
  - 0x0806d770 tick_lp_display_seq_spirit_effect
  - 0x0806d810 dispatch_neo_daedalus_or_spirit_sprite_by_field_bits
  - 0x0806d8c0 enqueue_zone_sprite_with_hand_and_monster_slot
- 残留自动名槽 x63:
  - DAT_0806cc1c = 0x0201b290 (gDuelPhaseFlags)
  - PTR_gP1LifePoints_0806cc5c = gP1LifePoints (symbolic)
  - DAT_0806cc60 = 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
  - PTR_gP1LifePoints_0806cc90 = gP1LifePoints (symbolic)
  - DAT_0806cc94 = 0x00001daa (LP_CARD_TRACK_NEXT_OFF)
  - PTR_gP1LifePoints_0806ccb4 = gP1LifePoints (symbolic)
  - DAT_0806ccb8 = 0x00001daa (LP_CARD_TRACK_NEXT_OFF)
  - DAT_0806cd38 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806cd3c = 0x0201c510 (gDuelFieldSlots)
  - PTR_gP1LifePoints_0806cdb0 = gP1LifePoints (symbolic)
  - DAT_0806cdb4 = 0x000010d0 (LP_ACTIVATION_LINK_FLAG_OFF)
  - DAT_0806cdb8 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806cdbc = 0x00001404 (MAGIC_CYLINDER_CID -- NEW)
  - DAT_0806cdc8 = 0x0000176a (DRAINING_SHIELD_CID -- NEW)
  - DAT_0806ce1c = 0x00008020 (SPRITE_RECORD_P2_SIDE -- NEW)
  - DAT_0806ce64 = 0x00008020 (SPRITE_RECORD_P2_SIDE -- NEW)
  - DAT_0806cf34 = 0x0201bb90 (gEquipChainSlotRefs)
  - DAT_0806cf38 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806cf3c = 0x0201c510 (gDuelFieldSlots)
  - DAT_0806cfe0 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806cfe4 = 0x0201c510 (gDuelFieldSlots)
  - DAT_0806d0c4 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d0c8 = 0x0201c510 (gDuelFieldSlots)
  - DAT_0806d120 = 0x0201e1c8 (gEquipZoneCountTable)
  - DAT_0806d138 = 0x0000138a (VALKYRION_THE_MAGNA_WARRIOR_CID)
  - DAT_0806d13c = 0x0000156a (PUPPET_MASTER_CID)
  - DAT_0806d160 = 0x0201b290 (gDuelPhaseFlags)
  - DAT_0806d1d4 = 0x0201b290 (gDuelPhaseFlags)
  - DAT_0806d1d8 = 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
  - DAT_0806d210 = 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
  - DAT_0806d284 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d288 = 0x0201c510 (gDuelFieldSlots)
  - DAT_0806d28c = 0x0000138d (RING_OF_DESTRUCTION_CID -- NEW)
  - DAT_0806d3d0 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d3d4 = 0x0201c510 (gDuelFieldSlots)
  - DAT_0806d3f4 = 0x0201b290 (gDuelPhaseFlags)
  - DAT_0806d44c = 0x0201e2a0 (gDuelCardCtxBase)
  - PTR_gP1LifePoints_0806d450 = gP1LifePoints (symbolic)
  - PTR_gP1LifePoints_0806d47c = gP1LifePoints (symbolic)
  - PTR_gP1LifePoints_0806d494 = gP1LifePoints (symbolic)
  - DAT_0806d498 = 0x00001daa (LP_CARD_TRACK_NEXT_OFF)
  - DAT_0806d50c = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d510 = 0x0201c8f8 (gP1HandSlotArray)
  - DAT_0806d5a8 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d5ac = 0x0201c510 (gDuelFieldSlots)
  - DWORD_0806d610 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DWORD_0806d614 = 0x0201c510 (gDuelFieldSlots)
  - DWORD_0806d678 = gP1LifePoints (symbolic)
  - DWORD_0806d67c = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
  - PTR_gP1LifePoints_0806d6b8 = gP1LifePoints (symbolic)
  - DAT_0806d6bc = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
  - DAT_0806d764 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d768 = 0x0201c510 (gDuelFieldSlots)
  - DAT_0806d76c = 0x00001cb8 (EQUIP_ZONE_COUNT_TABLE_OFF)
  - DAT_0806d78c = 0x0201b290 (gDuelPhaseFlags)
  - PTR_gP1LifePoints_0806d7c8 = gP1LifePoints (symbolic)
  - DAT_0806d7cc = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - PTR_gP1LifePoints_0806d7fc = gP1LifePoints (symbolic)
  - DAT_0806d800 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - PTR_gP1LifePoints_0806d84c = gP1LifePoints (symbolic)
  - DAT_0806d850 = 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8)
  - DAT_0806d8b8 = 0x00000868 (PLAYER_BLOCK_STRIDE)
  - DAT_0806d8bc = 0x0201c8f8 (gP1HandSlotArray)
- ROM_INCBIN / .byte 块: 0 (confirmed: python scan in Seg-9 lines 19719..21596 returns 0)

## 数据块分类 (Rule 2/3) -- 无块可分类
本段无 ROM_INCBIN / .byte 块。ref-scan 不适用。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate; 51 slots)

EQ slots -- 全部 reuse (46) + NEW (5 slots representing 4 distinct NEW constants):

| slot | addr | value | const_name | inc | status |
|------|------|-------|-----------|-----|--------|
| DAT_0806cc1c | 0x0806cc1c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806cc60 | 0x0806cc60 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | reuse |
| DAT_0806cc94 | 0x0806cc94 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | reuse |
| DAT_0806ccb8 | 0x0806ccb8 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | reuse |
| DAT_0806cd38 | 0x0806cd38 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806cd3c | 0x0806cd3c | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806cdb4 | 0x0806cdb4 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc | reuse |
| DAT_0806cdb8 | 0x0806cdb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806cdbc | 0x0806cdbc | 0x00001404 | MAGIC_CYLINDER_CID | card_info.inc | NEW |
| DAT_0806cdc8 | 0x0806cdc8 | 0x0000176a | DRAINING_SHIELD_CID | card_info.inc | NEW |
| DAT_0806ce1c | 0x0806ce1c | 0x00008020 | SPRITE_RECORD_P2_SIDE | oam_attr.inc | NEW |
| DAT_0806ce64 | 0x0806ce64 | 0x00008020 | SPRITE_RECORD_P2_SIDE | oam_attr.inc | NEW (reuse of same) |
| DAT_0806cf34 | 0x0806cf34 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | reuse |
| DAT_0806cf38 | 0x0806cf38 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806cf3c | 0x0806cf3c | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806cfe0 | 0x0806cfe0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806cfe4 | 0x0806cfe4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806d0c4 | 0x0806d0c4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d0c8 | 0x0806d0c8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806d120 | 0x0806d120 | 0x0201e1c8 | gEquipZoneCountTable | ewram.inc | reuse |
| DAT_0806d138 | 0x0806d138 | 0x0000138a | VALKYRION_THE_MAGNA_WARRIOR_CID | card_info.inc | reuse |
| DAT_0806d13c | 0x0806d13c | 0x0000156a | PUPPET_MASTER_CID | card_info.inc | reuse |
| DAT_0806d160 | 0x0806d160 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806d1d4 | 0x0806d1d4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806d1d8 | 0x0806d1d8 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | reuse |
| DAT_0806d210 | 0x0806d210 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | reuse |
| DAT_0806d284 | 0x0806d284 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d288 | 0x0806d288 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806d28c | 0x0806d28c | 0x0000138d | RING_OF_DESTRUCTION_CID | card_info.inc | NEW |
| DAT_0806d3d0 | 0x0806d3d0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d3d4 | 0x0806d3d4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806d3f4 | 0x0806d3f4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806d44c | 0x0806d44c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | reuse |
| DAT_0806d498 | 0x0806d498 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc | reuse |
| DAT_0806d50c | 0x0806d50c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d510 | 0x0806d510 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | reuse |
| DAT_0806d5a8 | 0x0806d5a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d5ac | 0x0806d5ac | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DWORD_0806d610 | 0x0806d610 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DWORD_0806d614 | 0x0806d614 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DWORD_0806d67c | 0x0806d67c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | reuse |
| DAT_0806d6bc | 0x0806d6bc | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | reuse |
| DAT_0806d764 | 0x0806d764 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d768 | 0x0806d768 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806d76c | 0x0806d76c | 0x00001cb8 | EQUIP_ZONE_COUNT_TABLE_OFF | duel_field.inc | reuse |
| DAT_0806d78c | 0x0806d78c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806d7cc | 0x0806d7cc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d800 | 0x0806d800 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d850 | 0x0806d850 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | reuse |
| DAT_0806d8b8 | 0x0806d8b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806d8bc | 0x0806d8bc | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | reuse |

C5 dedup evidence:
- PLAYER_BLOCK_STRIDE=0x868: ewram.inc L250 ".equ PLAYER_BLOCK_STRIDE, 0x868"; 2146 raw refs; reuse x21
- gDuelFieldSlots=0x0201c510: ewram.inc L313; 1007 raw refs; reuse x11
- gDuelPhaseFlags=0x0201b290: ewram.inc L352; 676 raw refs; reuse x7
- LP_CARD_TRACK_BASE_OFF=0x1da8: ewram.inc L247; reuse x1
- LP_CARD_TRACK_NEXT_OFF=0x1daa: ewram.inc L248; reuse x4
- LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: ewram.inc L481 (base=gP1LifePoints); reuse x1
- gEquipChainSlotRefs=0x0201bb90: ewram.inc L316; reuse x1
- gEquipZoneCountTable=0x0201e1c8: ewram.inc L396; reuse x1
- VALKYRION_THE_MAGNA_WARRIOR_CID=0x138a: card_info.inc L726; reuse x1
- PUPPET_MASTER_CID=0x156a: card_info.inc L1021; reuse x1
- EQUIP_PHASE_FRAME_OFF=0x4a4: ewram.inc L435; reuse x2
- gDuelCardCtxBase=0x0201e2a0: ewram.inc L218; reuse x1
- gP1HandSlotArray=0x0201c8f8: ewram.inc L333; reuse x2
- P1LP_BLOCK2_OFF_1CE8=0x1ce8: ewram.inc L275; reuse x3
- EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8: duel_field.inc L156 (base=gDuelFieldSlots); reuse x1
  - Domain note: DAT_0806d76c = 0x1cb8 used as: ldr r0, [0x1cb8]; add r0, r8 (r8=gDuelFieldSlots=0x0201c510)
    => r0 = gDuelFieldSlots+0x1cb8 = 0x0201e1c8 = gEquipZoneCountTable. Base = gDuelFieldSlots.
    Distinct from DUEL_ACTIVE_PLAYER_OFF=0x1cb8 (base=gP1LifePoints). Domain: duel_field.inc.

### REF_SLOTS (USER-label + DATA-ref; 0 slots)
No fn-ptr or data-reference slots in Seg-9 (no ROM_INCBIN, no dispatch table pointers, no switchD).

### RENAME_SLOTS (纯改名; 12 slots)
All PTR_gP1LifePoints_ and DWORD_0806d678 slots contain already-symbolic values.
Per file-08 convention: PTR_gP1LifePoints_<addr> -> gp1lifepoints_<addr>

| slot | addr | new_label | value |
|------|------|-----------|-------|
| PTR_gP1LifePoints_0806cc5c | 0x0806cc5c | gp1lifepoints_0806cc5c | gP1LifePoints |
| PTR_gP1LifePoints_0806cc90 | 0x0806cc90 | gp1lifepoints_0806cc90 | gP1LifePoints |
| PTR_gP1LifePoints_0806ccb4 | 0x0806ccb4 | gp1lifepoints_0806ccb4 | gP1LifePoints |
| PTR_gP1LifePoints_0806cdb0 | 0x0806cdb0 | gp1lifepoints_0806cdb0 | gP1LifePoints |
| PTR_gP1LifePoints_0806d450 | 0x0806d450 | gp1lifepoints_0806d450 | gP1LifePoints |
| PTR_gP1LifePoints_0806d47c | 0x0806d47c | gp1lifepoints_0806d47c | gP1LifePoints |
| PTR_gP1LifePoints_0806d494 | 0x0806d494 | gp1lifepoints_0806d494 | gP1LifePoints |
| PTR_gP1LifePoints_0806d6b8 | 0x0806d6b8 | gp1lifepoints_0806d6b8 | gP1LifePoints |
| PTR_gP1LifePoints_0806d7c8 | 0x0806d7c8 | gp1lifepoints_0806d7c8 | gP1LifePoints |
| PTR_gP1LifePoints_0806d7fc | 0x0806d7fc | gp1lifepoints_0806d7fc | gP1LifePoints |
| PTR_gP1LifePoints_0806d84c | 0x0806d84c | gp1lifepoints_0806d84c | gP1LifePoints |
| DWORD_0806d678 | 0x0806d678 | gp1lifepoints_0806d678 | gP1LifePoints |

### FUNC_RENAME (误名订正; 0)
No confirmed misnaming detected in Seg-9 functions.

Notes on investigated candidates:
- dispatch_neo_space_placement_by_card_id_and_state (0x0806d124): name assigned in analysis phase;
  body dispatches on Valkyrion_the_Magna_Warrior_CID (0x138a) and Puppet_Master_CID (0x156a)
  to set required monster slot count (r7=3/2/0), then calls check_field_spell_neo_daedalus_group_placeable.
  The name "neo_space" describes the field-spell placement eligibility domain (cards requiring
  free monster zones before a Neo-Space-type field spell placement), not a specific card name.
  No card-name vs function-body contradiction found. Confidence: med (no FUNC_RENAME).

### PLATE (R5; CJK mojibake 重写 + stale FUN_ 替换)

Two stale FUN_ references in @ comment lines:

1. asm/08_equip_oam_neodaed.s L20975 (enqueue_zone_equip_sprite_if_slot_matches plate):
   - Old: "Called by FUN_08071404 when zone_type == 0x0d (equip zone 13)."
   - New: "Called by enqueue_equip_sprite_guarded_by_zone_type13 when zone_type == 0x0d (equip zone 13)."
   - Evidence: asm/09_equip_lp_display.s L5724 confirms label enqueue_equip_sprite_guarded_by_zone_type13 @ 0x08071404

2. asm/08_equip_oam_neodaed.s L21181 (enqueue_spirit_zone_sprite_with_lp_check plate):
   - Old: "Called by FUN_08071d64 spirit monster dispatcher in the card_id == 0x1501 (Yamata Dragon) branch."
   - New: "Called by dispatch_spirit_monster_zone_sprite_by_card_id in the card_id == 0x1501 (Yamata Dragon) branch."
   - Evidence: asm/09_equip_lp_display.s L6819 confirms label dispatch_spirit_monster_zone_sprite_by_card_id @ 0x08071d64

One CJK mojibake plate (full ASCII rewrite):

3. asm/08_equip_oam_neodaed.s L20806 (tick_equip_lp_display_state_by_zone_match plate):
   - Current: CJK mojibake 636-char line (106 non-ASCII chars), detected by grep [^\x00-\x7F]
   - ASCII replacement:
     "Equip LP display state machine tick. Reads gDuelPhaseFlags+0x4a0 current step code and dispatches: step=0x80: calls check_effect_slot_matches_zone_entry to verify slot-zone match; on match calls read_effect_slot_side_and_type + invoke_effect_node_with_active_flag_3arg to activate; if activated reads [gDuelCardCtxBase+player*4+8] confirm_flag: if==1 calls sample_prng_scaled(2) and writes result to gP1LifePoints+0x1d40, returns 0x7f; if==0 calls invoke_card_display_op_0x31_sub8(0x38), returns 0x7f. step=0x7f: reads player/slot fields, calls enqueue_lp_display_row_type17, returns 0x7e. step=0x7e: checks gP1LifePoints+0x1daa non-zero gate, calls invoke_equip_slot_eligibility_via_effect_node_bitmap, returns result. Other steps return 0."

## carve 计划 (R7) -- 无
本段 0 ROM_INCBIN 块。carve=0。

## disasm 计划 (R4) -- 无
本段 0 mislabeled 代码块。disasm=0。

## 新增 constants / 全局

### card_info.inc (3 new CIDs)
All verified via data/card-stats.s passcode + ROM byte verification:

1. MAGIC_CYLINDER_CID = 0x00001404
   @ Magic Cylinder (pw=62279055; card-stats.s card_0879 slot=0x1404)
   Evidence: data/card-stats.s L11442; ROM 0x0806cdbc=0x00001404 confirmed

2. DRAINING_SHIELD_CID = 0x0000176a
   @ Draining Shield (pw=43250041; card-stats.s card_1554 slot=0x176A)
   Evidence: data/card-stats.s L20217; ROM 0x0806cdc8=0x0000176a confirmed

3. RING_OF_DESTRUCTION_CID = 0x0000138d
   @ Ring of Destruction (pw=83555666; card-stats.s card_0802 slot=0x138D)
   Evidence: data/card-stats.s L10441; ROM 0x0806d28c=0x0000138d confirmed

C5 dedup: grep -n "0x00001404\|0x0000176a\|0x0000138d" constants/card_info.inc -> 0 hits confirmed

### oam_attr.inc (1 new sprite constant)

4. SPRITE_RECORD_P2_SIDE = 0x00008020
   @ P2-side sprite record attr: bit15=1 (P2 palette select) | 0x20 (default P1 record val);
   used in dispatch_equip_lp_sprite_by_trap_card_id: movs r0,#0x20 (P1); if player==1 load 0x8020 (P2).
   8 aligned ROM refs total (python count). 3 .word slots in asm (08/10/12).
   Evidence: ROM 0x0806ce1c=0x8020 + 0x0806ce64=0x8020 confirmed; asm/08 L20014+L20049
   C5 dedup: grep -n "0x00008020" constants/oam_attr.inc -> 0 hits confirmed;
   existing OAM_SPRITE_COUNT_P2=0x8025 (different value, different semantic domain)

Note: ENCHANTED_JAVELIN_CID=0x1380 is computed in body via `subs r0,#0x84` from MAGIC_CYLINDER_CID=0x1404;
no literal pool slot in Seg-9. Not added as new constant this segment.

## §5.1 登记 (Rule 3) -- 0 引用块

本段无 ROM_INCBIN / .byte 块。§5.1 登记 = 0。

## 消费者证据 (R6) -- 关键槽语义

| slot | 语义 | 消费者 file:line | 置信度 |
|------|------|----------------|--------|
| DAT_0806cdbc (0x1404) | MAGIC_CYLINDER_CID: BST dispatch target in dispatch_equip_lp_sprite_by_trap_card_id | asm/08 L19953-19954 cmp r1,r0 / beq LAB_0806cde4 | high |
| DAT_0806cdc8 (0x176a) | DRAINING_SHIELD_CID: second BST target in same function | asm/08 L19970-19972 ldr r0,DAT/cmp/beq | high |
| DAT_0806d28c (0x138d) | RING_OF_DESTRUCTION_CID: card_id compare in submit_ring_of_destruction_lp_indicators_if_zone_matched | asm/08 L20614 ldrh r1,[r4,#0x0] / cmp r1,r0 beq LAB_0806d290 | high |
| DAT_0806ce1c/ce64 (0x8020) | SPRITE_RECORD_P2_SIDE: player==0 uses 0x20 literal, player==1 loads 0x8020; arg to enqueue_sprite_attr_record | asm/08 L19994+L19997 (ce1c) + L20022+L20025 (ce64) | high |
| DAT_0806d44c (0x0201e2a0) | gDuelCardCtxBase: reads [+player*4+8] confirm_flag in tick_equip_lp_display_state_by_zone_match | asm/08 L20845-20852 ldrb r4,[r4,#0x2]/lsls r1,r4,#0x1f/lsrs r1/lsls r1,r1,#0x2/adds r0,#0x8/adds r1,r1,r0/ldr r0,[r1,#0x0] | high |
| DAT_0806d76c (0x1cb8) | EQUIP_ZONE_COUNT_TABLE_OFF (base=gDuelFieldSlots): ldr r0,[0x1cb8]; add r0,r8 (r8=gDuelFieldSlots); ldr r0,[r0,#0x0] reads gEquipZoneCountTable[0] = active player | asm/08 L21288-21291 enqueue_zone_equip_sprite_at_matching_slot | high |
| DAT_0806d120 (0x0201e1c8) | gEquipZoneCountTable: base for player outer loop (eors r4,r0 at L20394 iterates player 0->1) in apply_equip_activation_for_all_player_slots | asm/08 L20393 ldr r4,[r1,#0x0] (r1=gEquipZoneCountTable) eors r4,r0 | high |

## 求助 (如有低置信度语义)
None. All slot semantics confirmed by consumer evidence (high confidence).

---

## Executor Report: F08-Seg-9
- 槽: EQ=51 REF=0 RENAME=12 FUNC_RENAME=0 PLATE=3
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局: card_info.inc +3 (MAGIC_CYLINDER_CID=0x1404 / DRAINING_SHIELD_CID=0x176a / RING_OF_DESTRUCTION_CID=0x138d) + oam_attr.inc +1 (SPRITE_RECORD_P2_SIDE=0x8020)
- 求助: none
- proposal: doc/dev/refine/F08-Seg-9.proposal.md
