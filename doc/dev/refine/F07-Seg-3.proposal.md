# Refine Proposal: F07-Seg-3  [0x0805e358..0x0805f1cc)

## 段测绘

- 函数入口: 34 (named; Seg-3 starts at check_monster_slot_field5_score_in_range)
  - L5214 0x0805e358 check_monster_slot_field5_score_in_range
  - L5261 0x0805e3a8 check_equip_slot_eligible_with_pool_and_hand_slot
  - L5303 0x0805e3ec check_equip_slot_eligible_type340_with_effect_node_absent
  - L5364 0x0805e450 check_equip_slot_state_code_equals0f
  - L5424 0x0805e4b0 check_zone_state_pair_matches_card_set_code
  - L5485 0x0805e518 check_equip_slot_eligible_type580_or_neo_daedalus_hand
  - L5546 0x0805e578 check_equip_slot_eligible_with_zone_success_count
  - L5701 0x0805e694 check_equip_slot_eligible_type_range18to20_with_prereqs
  - L5759 0x0805e6f4 check_equip_slot_eligible_without_banisher_mode1
  - L5797 0x0805e734 check_umi_matches_active_effect_slot
  - L5820 0x0805e790 check_revival_jam_equip_paired_field5
  - L5905 0x0805e81c check_field_state2_bit19_equip_eligible
  - L5953 0x0805e864 check_equip_zone_slot_activation_eligible
  - L6063 0x0805e92c check_mask_restrict_absent_daedalus_placeable
  - L6100 0x0805e958 check_facedown_slot_zone_equip_byte_set
  - L6162 0x0805e9bc check_equip_slot_eligible_type240_with_zone_field6_nonzero
  - L6236 0x0805ea3c check_equip_slot_eligible_with_type_e_zone_and_toon
  - L6331 0x0805eae8 check_monster_zone_set_code_equip_eligible
  - L6454 0x0805ebc4 check_equip_slot_eligible_max1_or_byte3_flag
  - L6499 0x0805ec00 check_dark_magician_effect_zone_available
  - L6544 0x0805ec40 check_effect_activations_both_sides
  - L6578 0x0805ec74 check_any_two_monster_slots_accept_card_pair
  - L6618 0x0805eca8 check_equip_or_facedown_slot_eligible_by_dispatch
  - L6693 0x0805ed2c check_equip_count_exceeds_one
  - L6713 0x0805ed74 check_lp_zone_offset_is_zero
  - L6735 0x0805ee20 check_opponent_has_monsters_and_lp_zone_positive
  - L6776 0x0805ee60 check_facedown_slot_with_free_monster_zone_and_matching_set
  - L6820 0x0805ef88 check_neo_daedalus_group_effect_eligible
  - L6852 0x0805efb8 check_spell_zone_placeable_with_chain_or_monster_condition
  - L6925 0x0805f020 check_equip_field_spell_neo_daedalus_and_monster_slots
  - L6973 0x0805f068 dispatch_effect_handler_clamped_to_bool
  - L7013 0x0805f088 scan_both_player_slots5_to_9_for_special_action
  - L7081 0x0805f0d8 eval_spell_zone_equip_eligibility
  - L7207 0x0805f1b0 check_player_has_field5_hand_card

- 残留自动名槽 x45:
  - 24x DAT_ + 16x DWORD_ = 40 auto-name slots (all named constants, see EQ/REF lists below)
  - 5x PTR_gP1LifePoints_* slots (all = 0x0201c4e0, RENAME-only)
  - Total 45 residual slots (matches §三 table: 40 in census + 5 PTR_ not counted as DAT_/DWORD_)

- ROM_INCBIN / .byte 块 x4:
  - L5805 0x0805e744 size 0x4c (76B)  -- Block1
  - L6710 0x0805ed4a size 0x2a (42B)  -- Block2
  - L6728 0x0805ed8e size 0x92 (146B) -- Block3
  - L6807 0x0805ee9c size 0xec (236B) -- Block4

---

## 数据块分类 (Rule 2/3)

All 4 blocks contain THUMB fn_ptr sub-functions referenced from 0x09e4xxxx handler dispatch tables.
Each has at least one confirmed THUMB+1 hit with valid CID word immediately preceding.
Classification: all 4 -> R4 DISASM.

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| Block1 0x0805e744/0x4c | raw=0 thumb=1 (@0x9e43948 CID=0x13f9; fn2: thumb=1 @0x9e407c8 CID=0x13fa) | disasm (R4) | CID 0x13f9 at 0x9e4393c, fn_ptr 0x805e745 at 0x9e43948; CID 0x13fa at 0x9e407bc, multi fn_ptr entry ending 0x805e779 at 0x9e407c8 |
| Block2 0x0805ed4a/0x2a | raw=0 thumb=1 (@0x9e439c0 CID=0x144e) | disasm (R4) | CID 0x144e at 0x9e439b4, fn_ptr 0x805ed4d at 0x9e439c0; next CID 0x144f at 0x9e439cc |
| Block3 0x0805ed8e/0x92 | raw=0 thumb=2/1/1 (fn1/fn2/fn3) | disasm (R4) | fn1: CID 0x1450 @0x9e439e4 + CID 0x1855 @0x9e47014; fn2: CID 0x1451 @0x9e439fc; fn3: CID 0x1460 @0x9e40a2c. raw=1 at 0x24c74a for fn2 is not a handler table (non-4B-aligned, foreign code context) |
| Block4 0x0805ee9c/0xec | raw=0 thumb=1 each (5 sub-fns) | disasm (R4) | CID 0x1468 @0x9e43a2c, 0x146f @0x9e4660c, 0x1472 @0x9e40ad4, 0x1475 @0x9e40b04, 0x147f @0x9e4663c; all confirmed with fn_ptr in THUMB+1 form |

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate; all reuse existing inc constants)

| slot | value | const_name | inc | slot_label |
|---|---|---|---|---|
| L5246 0x0805e398 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_monster_slot_field5_score_in_range_stride |
| L5248 0x0805e39c | 0x0201c510 | -- (gDuelFieldSlots is REF) | -- | (-> REF_SLOTS) |
| L5474 0x0805e510 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_slot_eligible_type580_stride |
| L5532 0x0805e570 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc | check_equip_slot_eligible_type580_fstate_off |
| L5645 0x0805e640 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_slot_eligible_with_zone_stride |
| L5676 0x0805e678 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_slot_eligible_type_range18_stride |
| L5741 0x0805e6e4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_slot_eligible_type_range18_stride_b |
| L5782 0x0805e724 | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | card_info.inc | check_equip_slot_eligible_without_banisher_cid |
| L5803 0x0805e740 | 0x000010f4 | UMI_CARD_ID | card_info.inc | check_umi_matches_active_effect_slot_cid |
| L5882 0x0805e808 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_revival_jam_equip_paired_field5_stride |
| L5886 0x0805e810 | 0x000013c7 | REVIVAL_JAM_CID | card_info.inc (NEW) | check_revival_jam_equip_paired_field5_cid |
| L5934 0x0805e854 | 0x00001cf4 | FIELD_STATE_OFF | duel_field.inc | check_field_state2_bit19_equip_eligible_fstate |
| L5936 0x0805e858 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_field_state2_bit19_equip_eligible_stride |
| L6078 0x0805e94c | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc | check_mask_restrict_absent_daedalus_lockdown_cid |
| L6143 0x0805e9b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_facedown_slot_zone_equip_byte_set_stride |
| L6219 0x0805ea2c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_slot_eligible_with_type_e_stride |
| L6307 0x0805ead8 | 0x00001415 | RED_MOON_BABY_CID | card_info.inc (NEW) | check_equip_or_facedown_dispatch_red_moon_cid |
| L6442 0x0805ebbc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_slot_eligible_max1_stride |
| L6522 0x0805ec30 | 0x00000fc9 | DARK_MAGICIAN_CID_0FC9 | card_info.inc | check_dark_magician_effect_zone_cid_0fc9 |
| L6524 0x0805ec34 | 0x0000142d | DARK_MAGICIAN_CID_142D | card_info.inc | check_dark_magician_effect_zone_cid_142d |
| L6677 0x0805ed1c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | check_equip_count_exceeds_one_off_1ce8 |
| L6679 0x0805ed20 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc | check_equip_count_exceeds_one_bitmask_off |
| L6761 0x0805ee54 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_opponent_has_monsters_stride |
| L7039 0x0805f0b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_spell_zone_equip_eligibility_stride |
| L7175 0x0805f190 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_player_has_field5_hand_card_stride |

Total EQ: 24 (25 entries in table above; L5248 gDuelFieldSlots is a REF not EQ, moved to REF_SLOTS)

### REF_SLOTS (USER-label + DATA-ref; all reuse existing ewram.inc globals)

| slot | target | gas_label | slot_label |
|---|---|---|---|
| L5248 0x0805e39c | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | check_monster_slot_field5_score_in_range_slots |
| L5349 0x0805e444 | 0x0201bb90 gEquipChainSlotRefs | gEquipChainSlotRefs | check_equip_slot_eligible_type340_ctx |
| L5383 0x0805e474 | 0x0201bb90 gEquipChainSlotRefs | gEquipChainSlotRefs | check_equip_slot_eligible_type340_ctx_b |
| L5476 0x0805e514 | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | check_equip_slot_eligible_type580_slots |
| L5678 0x0805e67c | 0x0201c4ec gP1ZoneHandCount | gP1ZoneHandCount | check_equip_slot_eligible_type_range18_zone_cnt |
| L5739 0x0805e6e0 | 0x0201bb90 gEquipChainSlotRefs | gEquipChainSlotRefs | check_equip_slot_eligible_type_range18_ctx |
| L5743 0x0805e6e8 | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | check_equip_slot_eligible_type_range18_slots |
| L5880 0x0805e804 | 0x0201bb90 gEquipChainSlotRefs | gEquipChainSlotRefs | check_revival_jam_equip_paired_field5_ctx |
| L5884 0x0805e80c | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | check_revival_jam_equip_paired_field5_slots |
| L6043 0x0805e91c | 0x0201bb90 gEquipChainSlotRefs | gEquipChainSlotRefs | check_equip_zone_slot_activation_eligible_ctx |
| L6221 0x0805ea30 | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | check_equip_slot_eligible_with_type_e_slots |
| L6444 0x0805ebc0 | 0x0201c4ec gP1ZoneHandCount | gP1ZoneHandCount | check_equip_slot_eligible_max1_zone_cnt |
| L6675 0x0805ed18 | 0x0201c4e0 gP1LifePoints | gP1LifePoints | check_equip_count_exceeds_one_lp_base |
| L6759 0x0805ee50 | 0x0201c4e0 gP1LifePoints | gP1LifePoints | check_opponent_has_monsters_lp_base |
| L7041 0x0805f0bc | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | eval_spell_zone_equip_eligibility_slots |
| L7177 0x0805f194 | 0x0201c510 gDuelFieldSlots | gDuelFieldSlots | check_player_has_field5_hand_card_slots |

Total REF: 16

### RENAME_SLOTS (PTR_gP1LifePoints_* -> gp1lp_ptr_* form per Seg-1 precedent)

| slot | old_label | new_label | value |
|---|---|---|---|
| L5530 0x0805e56c | PTR_gP1LifePoints_0805e56c | gp1lp_ptr_5e56c | 0x0201c4e0 (.word gP1LifePoints) |
| L5643 0x0805e63c | PTR_gP1LifePoints_0805e63c | gp1lp_ptr_5e63c | 0x0201c4e0 (.word gP1LifePoints) |
| L5932 0x0805e850 | PTR_gP1LifePoints_0805e850 | gp1lp_ptr_5e850 | 0x0201c4e0 (.word gP1LifePoints) |
| L6141 0x0805e9ac | PTR_gP1LifePoints_0805e9ac | gp1lp_ptr_5e9ac | 0x0201c4e0 (.word gP1LifePoints) |
| L6440 0x0805ebb8 | PTR_gP1LifePoints_0805ebb8 | gp1lp_ptr_5ebb8 | 0x0201c4e0 (.word gP1LifePoints) |

Total RENAME: 5

### FUNC_RENAME (stale FUN_ in plate comments)

No function rename needed; function names in Seg-3 are all correct.
However 2 stale FUN_ references appear in plate prose:

(These are C8 PLATE fixes, not actual FUNC_RENAME -- see PLATE section below.)

### PLATE (R5 / C8: stale FUN_ substring repair)

| location | stale_text | replacement_text | reason |
|---|---|---|---|
| L6543 check_equip_slot_eligible_max1_or_byte3_flag plate | FUN_080839b4 (equip effect chain dual-side activation check) | tick_equip_placement_bitmap_display_4state (equip effect chain dual-side activation check) | FUN_080839b4 = tick_equip_placement_bitmap_display_4state (asm/10_equip_effect_dispatch.s) |
| L7080 eval_spell_zone_equip_eligibility plate | FUN_08057874 (card_ids/duel_field module, result==2 continues equip effect) | tick_equip_slot_score_fill_display_seq (card_ids/duel_field module, result==2 continues equip effect) | FUN_08057874 = tick_equip_slot_score_fill_display_seq (asm/06_equip_eligibility_b.s) |

Total PLATE: 2 substring replacements

---

## carve 计划 (R7, 如有)

None. All 4 ROM_INCBIN blocks are R4 disasm (contain executable sub-functions, not structured data tables).

---

## disasm 计划 (R4)

All 4 blocks are THUMB handler sub-functions called from 0x09e4xxxx dispatch tables.
Entry convention: r0 = equip slot ptr (slot_ptr[2] = (zone_idx<<1)|player_id, slot_ptr[0..1] = type_bits).
Return convention: bx lr (not pop{r1}/bx r1 in most cases -- these are leaf fns).
No push/pop -- leaf functions using only caller-saved registers.

### Block1: 0x0805e744..0x0805e790 (76B)

2 sub-functions. No .zero2 prefix (fn1 starts at block start 0x5e744).

**fn1: 0x0805e744..0x0805e778 (52B)**
- Proposed name: `check_equip_type480_cross_player_for_cid_13f9`
- CID: 0x13f9 (Fairy Box, card_0870) -- ref at 0x09e4393c (handler table)
- Semantics: type_bits (halfword[2..3]&0xfc0) must == 0x480; slot[+0x14] must be nonzero; gEquipChainSlotRefs[0] (active_player) must != player_id (cross-player equip check). Returns 1 if all pass, 0 otherwise.
- Evidence: ROM bytes 0x1c02/0x20fc/0x0100/0x8851 confirm halfword read + mask 0xfc0 + compare 0x480; lit at 0x5e770 = 0x0201bb90 = gEquipChainSlotRefs (ewram.inc L317). Confidence: high.

**fn2: 0x0805e778..0x0805e790 (24B)**
- Proposed name: `check_equip_type_bits_range6_8_for_cid_13fa`
- CID: 0x13fa (Torrential Tribute, card_0871) -- ref at 0x09e407bc (3-fn_ptr multi-entry; other ptrs: 0x08064661+1 and 0x08050751+1)
- Semantics: extracts bits[11:6] of halfword at slot_ptr[2..3]; returns 1 if type_field in [6..8], else returns 0 (including type_field > 8 which branches to movs r0,#0). Primary predicate: field is in range [6..8].
- Evidence: ROM bytes 0x8840/0x0500/0x0e80 confirm ldrh+lsl20+lsr26 = extract bits[11:6]; bgt@0x805e780->movs r0,#0 (return 0) + blt@0x805e784->movs r0,#0 (return 0) + movs r0,#1@0x805e786 confirm [6..8]->1 else 0. Confidence: high.

### Block2: 0x0805ed4a..0x0805ed74 (42B)

Note: block starts at 0x5ed4a; first 2 bytes = 0x0000 (.zero2 padding), fn1 starts at 0x5ed4c.

**fn1: 0x0805ed4c..0x0805ed74 (40B)**
- Proposed name: `check_slot_count_exceeds_2_for_cid_144e`
- CID: 0x144e (unassigned slot, not in card-stats.s) -- ref at 0x09e439b4; CID 0x144f also appears at 0x09e439cc (immediately after, likely same entry block)
- Semantics: player_id = slot_ptr[2] & 1; reads gP1LifePoints[player_id*0x868 + 0x10] (= gP1SlotCountBase per-player; ewram.inc L328 gP1SlotCountBase=0x0201c4f0); returns 1 if count > 2, else 0.
- Evidence: lit 0x5ed68=0x0201c4e0 (gP1LifePoints), lit 0x5ed6c=0x868 (PLAYER_BLOCK_STRIDE), adds r2,#0x10 at 0x5ed58, cmp r0,#2/bls confirm threshold. Confidence: high.

### Block3: 0x0805ed8e..0x0805ee20 (146B)

First 2 bytes = 0x0000 (.zero2 padding), fn1 starts at 0x5ed90.

**fn1: 0x0805ed90..0x0805edc0 (48B)**
- Proposed name: `check_zone_field6_hw_zero_for_cid_1450`
- CID: 0x1450 (Spirit of the Breeze, card_0917) -- ref at 0x09e439e4; ALSO CID 0x1855 (Castle Gate, card_1751) -- ref at 0x09e47014 (second handler table)
- Semantics: extracts player_id=slot_ptr[2]&1 and zone_idx=slot_ptr[2]>>1; computes addr = gDuelFieldSlots + zone_idx*16 + player_id*(4+0x868); reads halfword at [addr+6]; returns 1 if hw==0 (field6 clear), 0 otherwise.
- Evidence: lit 0x5edb4=0x868, lit 0x5edb8=0x0201c510 (gDuelFieldSlots); byte 0xd1 (BNE) at offset 31 confirms zero->return 1 path. Confidence: high.

**fn2: 0x0805edc0..0x0805edf0 (48B)**
- Proposed name: `check_zone_field6_hw_nonzero_for_cid_1451`
- CID: 0x1451 (Dancing Fairy, card_0918) -- ref at 0x09e439fc
- Semantics: identical structure to fn1 EXCEPT branch condition inverted (BEQ 0xd0 vs BNE 0xd1); returns 1 if halfword[+6] != 0 (field6 set), 0 if hw==0.
- Evidence: fn1 and fn2 are byte-identical except byte offset 31: fn1=0xd1 (BNE) fn2=0xd0 (BEQ). Confidence: high.

**fn3: 0x0805edf0..0x0805ee20 (48B)**
- Proposed name: `check_opponent_lp_above_3000_for_cid_1460`
- CID: 0x1460 (Meteor of Destruction, card_0931) -- ref at 0x09e40a2c
- Semantics: opponent_id = player_id^1; reads gP1LifePoints[opponent_id*0x868+0] = opponent LP value; returns 1 if opponent_LP > 0xBB8 (3000), 0 otherwise.
- Evidence: lit 0x5ee14=0x0201c4e0, lit 0x5ee18=0x868, lit 0x5ee1c=0x0BB8; movs r1,#1; eors r0,r1 confirms opponent_id=player_id^1. Confidence: high.

### Block4: 0x0805ee9c..0x0805ef88 (236B)

No .zero2 prefix (fn1 starts at block start 0x5ee9c). 5 sub-functions separated by bc02/4708 (pop{r1}/bx r1) + .zero2 padding between each.

**fn1: 0x0805ee9c..0x0805eeb8 (28B)**
- Proposed name: `check_free_monster_zone_for_cid_1468`
- CID: 0x1468 (Destiny Board, card_0916, card_info.inc DESTINY_BOARD_CID) -- ref at 0x09e43a2c
- Semantics: player_id = slot_ptr[2]&1; calls find_first_available_monster_slot_for_player(player_id) (0x08033bf4); returns 1 if result >= 0 (free monster zone exists), 0 if < 0. Exit: pop{r1}/bx r1.
- Evidence: BL at 0x5eea4 -> 0x08033bf4 = find_first_available_monster_slot_for_player (asm/02_text_lp_fieldspell.s L17192); blt 0xdb01 at 0x5eeaa + mov r0,#0 path + mov r0,#1 path. Confidence: high.

**fn2: 0x0805eeb8..0x0805eee4 (44B)**
- Proposed name: `check_neo_daedalus_no_banisher_for_cid_146f`
- CID: 0x146f (Cathedral of Nobles, card_0945) -- ref at 0x09e4660c (3-fn_ptr entry; also has 0x806fded+1 and 0x8052a21+1)
- Semantics: player_id = slot_ptr[2]&1; (1) check_field_spell_neo_daedalus_group_placeable(player_id) (BL->0x0803bb7c); if 0 -> return 0; (2) count_field_copies_of_card(BANISHER_CID=0x1332) (BL->0x0803279c); if > 0 -> return 0; else return 1. Exit: pop{r1}/bx r1.
- Evidence: BL 0x5eec0->0x0803bb7c = check_field_spell_neo_daedalus_group_placeable (asm/03_equip_chain_hand.s L12815); BL 0x5eeca->0x0803279c = count_field_copies_of_card (asm/02_text_lp_fieldspell.s L14337); lit 0x5eed8=0x1332. Confidence: high.

**fn3: 0x0805eee4..0x0805ef10 (44B)**
- Proposed name: `check_field_state24_neo_daedalus_for_cid_1472`
- CID: 0x1472 (Embodiment of Apophis, card_0823, card_info.inc EMBODIMENT_OF_APOPHIS_CID) -- ref at 0x09e40ad4
- Semantics: reads gP1LifePoints[0x1cf4] = field_state; if field_state not in {2,4} -> return 0; else calls check_equip_slot_eligible_neo_daedalus_with_monster_placeable(slot_ptr) (BL->0x080609a4) and returns its result. Exit: pop{r1}/bx r1.
- Evidence: lits 0x5eefc=0x0201c4e0, 0x5ef00=0x1cf4; cmp r0,#2/beq + cmp r0,#4/beq confirm field_state check; BL 0x5ef06->0x080609a4 = check_equip_slot_eligible_neo_daedalus_with_monster_placeable (asm/07_equip_effect_chain.s L11238). Confidence: high.

**fn4: 0x0805ef10..0x0805ef4c (60B)**
- Proposed name: `check_chain_match_opponent_for_cid_1475`
- CID: 0x1475 (Makiu, card_0949) -- ref at 0x09e40b04 (3-fn_ptr entry: also 0x080701a5+1 and 0x8052aa9+1)
- Semantics: saves slot_ptr (r1); reads field_state at gP1LP+0x1cf4; if field_state != 2 -> return 0; else extracts player_id = slot_ptr[2]&1; opponent_id = 1-player_id; calls count_slots_with_chain_field_match(opponent_id, 0, 0) (BL->0x08033294); returns 1 if count > 0, else 0. Exit: pop{r1}/bx r1.
- Evidence: lit 0x5ef24=0x0201c4e0, lit 0x5ef28=0x1cf4; BL 0x5ef3a->0x08033294 = count_slots_with_chain_field_match (asm/02_text_lp_fieldspell.s L15873); ble dest after BL + movs r1,#1 confirm >0 test. Confidence: high.

**fn5: 0x0805ef4c..0x0805ef88 (60B)**
- Proposed name: `check_field_0c_nonzero_no_banisher_for_cid_147f`
- CID: 0x147f (Jowgen the Spiritualist, card_0957) -- ref at 0x09e4663c (4-fn_ptr entry: also 0x8064661+1, 0x8053035+1, 0x8057661+1)
- Semantics: player_id = slot_ptr[2]&1; reads gP1LifePoints[player_id*0x868+0x0c] (= per-player field at gP1ZoneHandCount-relative offset 0); if value == 0 -> return 0; calls count_field_copies_of_card(BANISHER_CID=0x1332) (BL->0x0803279c); if count > 0 -> return 0; else return 1. Exit: pop{r1}/bx r1.
- Evidence: lit 0x5ef74=0x0201c4e0, lit 0x5ef78=0x868, adds r2,#0x0c at 0x5ef5a; lit 0x5ef7c=0x1332; BL->0x0803279c = count_field_copies_of_card; bgt/b branch structure confirmed. Confidence: high.
- Note: gP1LP+player*0x868+0xc = gP1ZoneHandCount area (ewram.inc L232 gP1ZoneHandCount=0x0201c4ec=gP1LP+0xc for player 0). No named equate for the scalar offset 0x0c -- use raw literal.

---

## 新增 constants / 全局

Two new card_info.inc entries required (confirmed not present via grep):

1. `REVIVAL_JAM_CID = 0x000013c7`
   - card_0843 = Revival Jam (pw=31709826), slot=0x13C7 (card-stats.s L10973)
   - Used at L5886 0x0805e810 in check_revival_jam_equip_paired_field5 (literal pool); 1 Seg-3 slot
   - grep card_info.inc for 0x13c7: 0 hits (confirmed absent)

2. `RED_MOON_BABY_CID = 0x00001415`
   - card_0896 = Red-Moon Baby (pw=56387350), slot=0x1415 (card-stats.s L11662)
   - Used at L6307 0x0805ead8 in check_equip_or_facedown_slot_eligible_by_dispatch; 1 Seg-3 slot
   - grep card_info.inc for 0x1415: 0 hits (confirmed absent)

No new ewram.inc or duel_field.inc globals needed (all values reuse existing equates).

---

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 4 ROM_INCBIN blocks have confirmed THUMB+1 refs in valid 0x09e4xxxx handler table contexts.

---

## 消費者証据 (R6)

**EQ slot values -- key evidence**

- PLAYER_BLOCK_STRIDE=0x868: ewram.inc L232 (gP1ZoneHandCount=gP1LifePoints+0xc, same block stride), asm/07_equip_effect_chain.s L5247 (.word 0x00000868). Confidence: high.
- gEquipChainSlotRefs=0x0201bb90: ewram.inc L317. Used in Block1 fn1 as active_player source and in multiple Seg-3 functions. Confidence: high.
- gDuelFieldSlots=0x0201c510: ewram.inc L340. Used in Block3 fn1/fn2 zone slot address computation. Confidence: high.
- gP1LifePoints=0x0201c4e0: ewram.inc L232 (gP1ZoneHandCount=0x0201c4ec=gP1LifePoints+0xc). Used in Block3 fn3 and Block4 fn4/fn5. Confidence: high.
- FIELD_STATE_OFF=0x00001cf4: duel_field.inc. Used in Block4 fn3/fn4. Confidence: high.
- BANISHER_OF_THE_LIGHT_CID=0x1332: card_info.inc L452. Used in Block4 fn2/fn5 and check_equip_slot_eligible_without_banisher_mode1 literal pool. Confidence: high.
- REVIVAL_JAM_CID=0x13c7: card-stats.s L10973 (card_0843, pw=31709826). Used in check_revival_jam_equip_paired_field5 (L5886). Confidence: high.
- RED_MOON_BABY_CID=0x1415: card-stats.s L11662 (card_0896, pw=56387350). Used in check_equip_or_facedown_slot_eligible_by_dispatch (L6307). Confidence: high.
- UMI_CARD_ID=0x10f4: card_info.inc L145. Used in check_umi_matches_active_effect_slot literal pool (L5803). Confidence: high.
- EQUIP_LOCKDOWN_CID=0x13f2: card_info.inc L128. Used in check_mask_restrict_absent_daedalus_placeable (L6078). Confidence: high.
- DARK_MAGICIAN_CID_0FC9=0x0fc9: card_info.inc L310. Used in check_dark_magician_effect_zone_available (L6522). Confidence: high.
- DARK_MAGICIAN_CID_142D=0x142d: card_info.inc L329. Used in check_dark_magician_effect_zone_available (L6524). Confidence: high.
- P1LP_BLOCK2_OFF_1CE8=0x1ce8: ewram.inc L275. Used in check_equip_count_exceeds_one (L6677). Confidence: high.
- EFFECT_ZONE_BITMASK_OFF=0x10d0: duel_field.inc. Used in check_equip_count_exceeds_one (L6679). Confidence: high.

**disasm sub-fn semantics -- key callee evidence**

- find_first_available_monster_slot_for_player (0x08033bf4): asm/02_text_lp_fieldspell.s L17192. Confidence: high.
- check_field_spell_neo_daedalus_group_placeable (0x0803bb7c): asm/03_equip_chain_hand.s L12815. Confidence: high.
- count_field_copies_of_card (0x0803279c): asm/02_text_lp_fieldspell.s L14337. Confidence: high.
- count_slots_with_chain_field_match (0x08033294): asm/02_text_lp_fieldspell.s L15873. Confidence: high.
- check_equip_slot_eligible_neo_daedalus_with_monster_placeable (0x080609a4): asm/07_equip_effect_chain.s L11238. Confidence: high.

**stale FUN_ plate fixes -- evidence**

- FUN_080839b4 -> tick_equip_placement_bitmap_display_4state: asm/10_equip_effect_dispatch.s grep confirms entry at that address. Confidence: high.
- FUN_08057874 -> tick_equip_slot_score_fill_display_seq: naming-proposals.csv L1328 + asm/06_equip_eligibility_b.s L10136 confirms. Confidence: high.

---

## 求助

None. All semantics confirmed with file:line evidence and high confidence.

Block1 fn2 (check_equip_type_bits_range6_8_for_cid_13fa): bgt@0x805e780 branches to movs r0,#0 (not a non-zero return); returns 1 only for type_field in [6..8], returns 0 for all other values including >8. Name is accurate. EOL/plate must not use "nonzero if >8" -- correct text: "returns 1 if type_field in [6..8], else 0".

Block2 fn1 (cid_144e): CID 0x144e and 0x144f are both unassigned (absent from card-stats.s), yet appear in the same table entry area. cid_144e is confirmed as the owner of fn1's fn_ptr. CID 0x144f appears at 0x09e439cc (next table word after fn1's entry block); it shares the same fn_ptr (0x805ed4d) in an adjacent slot -- not a different sub-function. Confirmed via ref-scan: only 1 THUMB ref to 0x805ed4c+1.
