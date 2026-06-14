# Refine Proposal: F07-Seg-1  [0x0805c2f0..0x0805cfec)

## Segment Survey

### Function Entries (34)

| addr | name |
|------|------|
| 0x0805c2f0 | dispatch_effect_by_card_id_with_display_lookup |
| 0x0805c318 | check_equip_lp_delta_nonzero_for_entry |
| 0x0805c33c | check_equip_slot_eligible_with_ctx_player_and_type |
| 0x0805c394 | check_monster_zone_placement_eligible |
| 0x0805c3ec | check_equippable_slots_nonzero_for_player |
| 0x0805c468 | check_equippable_slots_nonzero_with_slot_idx |
| 0x0805c48c | check_equippable_slots_positive_for_player |
| 0x0805c4d4 | dispatch_effect_for_neo_daedalus_paired_slot |
| 0x0805c528 | check_equip_slot_eligible_with_sanga_and_prereqs |
| 0x0805c598 | check_equip_slot_eligible_with_ctx_and_zone_prereqs |
| 0x0805c630 | check_monster_slots_nonzero_for_entry_player |
| 0x0805c660 | check_equip_slot_absent_for_swords_of_light |
| 0x0805c680 | check_effect_zone_multi_activation |
| 0x0805c6b0 | check_equip_slot_eligible_with_type480_or_4c0_and_prereqs |
| 0x0805c724 | check_equip_chain_pair_placement_eligible |
| 0x0805c7a4 | check_equip_slot_eligible_by_scapegoat_or_stray_lambs |
| 0x0805c818 | check_equip_target_zone_validity_by_card_id |
| 0x0805ca50 | check_equip_slot_eligible_with_chain_node_type_d |
| 0x0805ca94 | check_direct_equip_slot_bit4_eligible |
| 0x0805caf0 | check_equip_slot_eligible_by_type80_or_spell500 |
| 0x0805cb1c | check_equip_slot_chain_absent_if_field_state2 |
| 0x0805cb44 | check_zone_slot_type_matches_card_type |
| 0x0805cbcc | check_neo_daedalus_lp_count_eligible |
| 0x0805cc08 | check_toon_equip_chain_zone_eligible |
| 0x0805cd20 | check_equip_slot_eligible_type480_with_active_deck |
| 0x0805cd6c | check_neo_daedalus_placeable_for_entry_player |
| 0x0805cdb0 | dispatch_lord_of_d_effect_by_slot_pair |
| 0x0805cdd8 | check_equip_slot_lp_offset_within_limit |
| 0x0805ce30 | check_equip_slot_eligible_type2c0_with_bit15_14 |
| 0x0805ce70 | check_equip_slot_eligible_with_lp_slot_flag |
| 0x0805cec8 | check_equip_slot_eligible_type480_with_occupied_and_monster |
| 0x0805cf3c | check_dual_zone_effect_activation_count |
| 0x0805cf70 | check_equip_slot_eligible_without_reserved_field_card |
| 0x0805cf98 | check_lp_draw_card_tier_threshold |

### Residual Auto-Name Slots: 66 total
- DAT_/DWORD_ slots: 57
- PTR_gP1LifePoints_* slots: 9

### ROM_INCBIN / .byte Blocks: 5

| addr | size | position |
|------|------|----------|
| 0x0805c40a | 0x5e (94B) | between check_equippable_slots_nonzero_for_player and check_equippable_slots_nonzero_with_slot_idx |
| 0x0805c4aa | 0x2a (42B) | between check_equippable_slots_positive_for_player and dispatch_effect_for_neo_daedalus_paired_slot |
| 0x0805c608 | 0x28 (40B) | between check_equip_slot_eligible_with_ctx_and_zone_prereqs and check_monster_slots_nonzero_for_entry_player |
| 0x0805cd86 | 0x2a (42B) | between check_neo_daedalus_placeable_for_entry_player and dispatch_lord_of_d_effect_by_slot_pair |
| 0x0805cf1c | 0x20 (32B) | between check_equip_slot_eligible_type480_with_occupied_and_monster and check_dual_zone_effect_activation_count |

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

| Block | sub-offset | thumb-ptr value | raw | thumb | Judgment | Evidence |
|-------|-----------|-----------------|-----|-------|----------|----------|
| 0x5c40a (0x5e) | +0x02 -> fn1@0x5c40c | 0x0805c40d | 0 | 4 | disasm R4 | 4 hits in 0x9e43xxx dispatch table: CIDs 0x101e(Dream Clown), 0x1048(unassigned), 0x1197(unassigned), 0x1868(Blade Rabbit); fn_slot=2 in 24B record |
| 0x5c40a (0x5e) | +0x32 -> fn2@0x5c43c | 0x0805c43d | 0 | 21 | disasm R4 | 21 hits in 0x9e4xxxx dispatch table: CIDs include 0x1308(Fusion Sage), 0x1474(Foolish Burial), 0x14d0(Reinforcement of the Army), 0x1562(Toon Table of Contents), 0x159c(Different Dimension Capsule), 0x15a1(Terraforming) and 15 more; fn_slot=2 |
| 0x5c40a (0x5e) | +0x24 -> raw@0x5c42e | 0x0805c42e (raw) | 1 | -- | not fn-ptr | Hit at 0x8327180 in code sequence (bl-like context, not dispatch table); coincidental raw value embedded in instruction word |
| 0x5c4aa (0x2a) | all 2B-step scan | -- | 0 | 0 | Sec5.1 orphan | Full byte-step scan (every sub-offset): 0 raw + 0 thumb refs anywhere in ROM. Confirmed zero-ref. Block begins with .zero 2 then valid THUMB code from 0x5c4ac (ldr r2,[pc,#0x18]; ldrb r0,[r0,#0x2]; lsls/lsrs player_id extraction; gP1LifePoints+player*0x868 load; bcc/movs; bx lr pattern) -- orphaned eligibility predicate. |
| 0x5c608 (0x28) | +0x00 -> fn@0x5c608 | 0x0805c609 | 0 | 1 | disasm R4 | 1 hit in dispatch table at 0x9e46408: CID=0x11a0 (unassigned slot, not in card-stats.s), fn_slot=2 in 24B record (CID@0x9e463fc, fn[0]=0x080672a5, fn[1]=0, fn[2]=0x0805c609, fn[3]=0x0805635d) |
| 0x5cd86 (0x2a) | +0x02 -> fn@0x5cd88 | 0x0805cd89 | 0 | 15 | disasm R4 | 15 hits in 0x9e3f..0x9e45 dispatch tables: CIDs include 0x12c8(Lightforce Sword), 0x12f0(unassigned), 0x1307(Restructer Revolution), 0x1324(Confiscation), 0x1325(Delinquent Duo), 0x132b(The Forceful Sentry) and 9 more; fn_slot=2 |
| 0x5cf1c (0x20) | +0x00 -> fn@0x5cf1c | 0x0805cf1d | 0 | 3 | disasm R4 | 3 hits in dispatch tables at 0x9e3f880, 0x9e3f898, 0x9e3fc10: CIDs 0x124f(House of Adhesive Tape), 0x1250(unassigned), 0x12e4(Trap Hole); fn_slot=2 |

Dispatch table format (confirmed): 24B records at 0x9e3xxxx..0x9e4xxxx: [CID u32][fn[0..4] u32 x5]; fn=0 for unused slots. All THUMB+1 hits verified in this region, not in compressed-asset coincidence range.

---

## Symbolization Plan

### EQ_SLOTS (data-equate -- 54 slots)

**Reuse ewram.inc: PLAYER_BLOCK_STRIDE = 0x868** (ewram.inc confirmed present; 2146 raw refs)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c3e0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c3e0 |
| 0x0805c51c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c51c |
| 0x0805c5fc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c5fc |
| 0x0805c714 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c714 |
| 0x0805c80c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c80c |
| 0x0805c924 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c924 |
| 0x0805c988 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c988 |
| 0x0805c9f0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805c9f0 |
| 0x0805ca34 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805ca34 |
| 0x0805cae4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805cae4 |
| 0x0805cbb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805cbb8 |
| 0x0805cbfc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805cbfc |
| 0x0805ce24 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805ce24 |
| 0x0805cebc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805cebc |
| 0x0805cfe8 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805cfe8 |

**Reuse ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8** (ewram.inc confirmed: 184 ROM refs)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c384 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805c384 |
| 0x0805c5f4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805c5f4 |

**Reuse duel_field.inc: FIELD_STATE_OFF = 0x1cf4** (duel_field.inc confirmed present; comment confirms asm/07 STAGE_OFF/FIELD_STATE_OFFSET)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c388 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805c388 |
| 0x0805c5f8 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805c5f8 |
| 0x0805c6ac | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805c6ac |
| 0x0805cb38 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805cb38 |

**Reuse ewram.inc: gEquipChainSlotRefs = 0x0201bb90** (ewram.inc confirmed; 260 raw refs; comment: "equip chain slot reference array")
Note: function plates use this as "DECK_STRUCT_BASE" or "DECK_BASE" -- the address is gEquipChainSlotRefs. Plates using "0x0201bb90 (gDuelEffectCtx)" in Ghidra should remain ASCII with name gEquipChainSlotRefs.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c58c | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805c58c |
| 0x0805c710 | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805c710 |
| 0x0805cd60 | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805cd60 |
| 0x0805cf10 | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805cf10 |

**Reuse ewram.inc: gDuelFieldSlots = 0x0201c510** (ewram.inc confirmed; 1007 raw refs)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c718 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805c718 |
| 0x0805c928 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805c928 |
| 0x0805c98c | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805c98c |
| 0x0805c9f4 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805c9f4 |
| 0x0805ca38 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805ca38 |
| 0x0805cbbc | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805cbbc |

**Reuse ewram.inc: gDuelPhaseFlags = 0x0201b290** (ewram.inc confirmed; 676 raw refs)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cd04 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_0805cd04 |

**Reuse ewram.inc: LP_BAR_ANIM_STATE_OFF = 0x4cc** (ewram.inc confirmed: ".equ LP_BAR_ANIM_STATE_OFF, 0x000004cc")
Context: DAT_0805cd08 is adjacent to DAT_0805cd04 (gDuelPhaseFlags); consumer check_toon_equip_chain_zone_eligible adds +0x4cc to gDuelPhaseFlags to get node count. asm/07 plate says NODE_COUNT_OFF=0x4cc. ewram.inc LP_BAR_ANIM_STATE_OFF = 0x4cc -- same value, different context. Per C5 rule (scalar strict dedup), same value = same equate; add note to EOL.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cd08 | 0x000004cc | LP_BAR_ANIM_STATE_OFF | lp_bar_anim_state_off_0805cd08 |

**Reuse ewram.inc: SPRITE_ROW_ENTRY_DATA_OFF = 0x4d4** (ewram.inc confirmed: ".equ SPRITE_ROW_ENTRY_DATA_OFF, 0x000004d4")
Context: DAT_0805cd0c; check_toon_equip_chain_zone_eligible adds +0x4d4 to gDuelPhaseFlags for node zone_type array base. ewram.inc comment: "[gDuelPhaseFlags+0x4d4] byte array for card sprite row entry flag data". Same value, reuse per C5 scalar dedup.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cd0c | 0x000004d4 | SPRITE_ROW_ENTRY_DATA_OFF | sprite_row_entry_data_off_0805cd0c |

**Reuse ewram.inc: CHAIN_NODE_CARD_ARR_OFF = 0x4f4** (ewram.inc confirmed: ".equ CHAIN_NODE_CARD_ARR_OFF, 0x000004f4")
Context: DAT_0805cd10; check_toon_equip_chain_zone_eligible adds +0x4f4 to gDuelPhaseFlags for node slot pointer array. ewram.inc comment: "[gDuelPhaseFlags+0x4f4] card pointer array for equip chain node list". Same semantic domain confirmed.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cd10 | 0x000004f4 | CHAIN_NODE_CARD_ARR_OFF | chain_node_card_arr_off_0805cd10 |

**Reuse card_info.inc: SWORDS_OF_REVEALING_LIGHT_CID = 0x1102** (card_info.inc confirmed present)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c67c | 0x00001102 | SWORDS_OF_REVEALING_LIGHT_CID | swords_of_light_cid_0805c67c |

**Reuse card_info.inc: STRAY_LAMBS_CID = 0x1710** (card_info.inc confirmed present)
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c7c0 | 0x00001710 | STRAY_LAMBS_CID | stray_lambs_cid_0805c7c0 |

**NEW card_info.inc: SANGA_OF_THUNDER_CID = 0x1119**
Evidence: card-stats.s grep pattern "@.*slot=0x1119": "Sanga of the Thunder slot=0x1119 pw=..." -- confirmed hit (high conf).
grep card_info.inc "0x1119": 0 hits -- new in card_info.inc.
Cross-file note: duel_field.inc:345 EQUIP_SPRITE_CARD_DATA=0x00001119 -- different domain (sprite attr card_data param, not a CID comparand); domain-distinct ruling retained; see collision scan table below for reviewer confirmation request.
Consumer: check_equip_slot_eligible_with_sanga_and_prereqs plate says "ICID_SANGA=0x1119 (Sanga of the Thunder)". File: asm/07_equip_effect_chain.s line 305.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c588 | 0x00001119 | SANGA_OF_THUNDER_CID | sanga_of_thunder_cid_0805c588 |

**Reuse card_info.inc: WALL_SHADOW_CID = 0x1117** (card_info.inc line 712 confirmed present)
Evidence: card-stats.s "Wall Shadow slot=0x1117" -- confirmed. card_info.inc line 712: `.equ WALL_SHADOW_CID, 0x00001117`.
Consumer: check_equip_chain_pair_placement_eligible plate says "ZONE_CARD_CHECK_ID=0x1117 (Wall Shadow)". asm/07 line 640.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c798 | 0x00001117 | WALL_SHADOW_CID | wall_shadow_cid_0805c798 |

**NEW card_info.inc: SCAPEGOAT_CID = 0x12d2**
Evidence: card-stats.s "Scapegoat slot=0x12d2" -- confirmed. grep card_info.inc "0x12d2": 0 hits -- new.
Consumer: check_equip_slot_eligible_by_scapegoat_or_stray_lambs plate says "SCAPEGOAT_ICID=0x12d2 (Scapegoat)". asm/07 line 706.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c7bc | 0x000012d2 | SCAPEGOAT_CID | scapegoat_cid_0805c7bc |

**Reuse card_info.inc: LORD_OF_D_CID = 0x128b** (card_info.inc line 241 confirmed present)
Evidence: card_info.inc line 241: `.equ LORD_OF_D_CID, 0x0000128b @ Lord of D. (pw=17985575)`.
Consumer: dispatch_lord_of_d_effect_by_slot_pair plate says "CARD_ID_LORD_OF_D=0x128b". asm/07 line 1635.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cdcc | 0x0000128b | LORD_OF_D_CID | lord_of_d_cid_0805cdcc |

**NEW card_info.inc: GRACEFUL_CHARITY_CID = 0x12cc**
Evidence: card-stats.s "Graceful Charity slot=0x12cc" -- confirmed. grep card_info.inc "0x12cc": 0 hits -- new.
Consumer: check_lp_draw_card_tier_threshold plate says "CARD_ID_GRACEFUL_CHARITY=0x12cc". asm/07 line 1961.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cfb0 | 0x000012cc | GRACEFUL_CHARITY_CID | graceful_charity_cid_0805cfb0 |

**NEW card_info.inc: GREENKAPPA_CID = 0x11f0**
Evidence: card-stats.s grep "slot=0x11f0": "Greenkappa slot=0x11f0" -- confirmed. grep card_info.inc "0x11f0": 0 hits -- new.
Consumer: check_equip_target_zone_validity_by_card_id uses 0x11f0 as dispatch branch boundary (DAT_0805c870 cmp). asm/07 line 844. Confidence: high (card-stats confirmed).
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c870 | 0x000011f0 | GREENKAPPA_CID | greenkappa_cid_0805c870 |

**NEW card_info.inc: REAPER_OF_CARDS_CID = 0x0ffa**
Evidence: card-stats.s "Reaper of the Cards slot=0x0ffa" -- confirmed. grep card_info.inc "0x0ffa": 0 hits -- new.
Consumer: check_equip_target_zone_validity_by_card_id plate says "0x0ffa (Reaper of the Cards)". asm/07 line 793. Confidence: high.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c874 | 0x00000ffa | REAPER_OF_CARDS_CID | reaper_of_cards_cid_0805c874 |

**NEW card_info.inc: HARPIES_FEATHER_DUSTER_CID = 0x1246**
Evidence: card-stats.s "Harpie's Feather Duster slot=0x1246" -- confirmed. grep card_info.inc "0x1246": 0 hits -- new.
Consumer: check_equip_target_zone_validity_by_card_id plate says "0x1246 (Harpie's Feather Duster)". asm/07 line 793. Confidence: high.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c884 | 0x00001246 | HARPIES_FEATHER_DUSTER_CID | harpies_feather_duster_cid_0805c884 |

**NEW card_info.inc: DRIVING_SNOW_CID = 0x134d**
Evidence: card-stats.s "Driving Snow slot=0x134d" -- confirmed. grep card_info.inc "0x134d": 0 hits (only "0x134e" unassigned neighbor). New.
Consumer: check_equip_target_zone_validity_by_card_id plate says "0x134d (Driving Snow)". asm/07 line 793. Confidence: high.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c8a0 | 0x0000134d | DRIVING_SNOW_CID | driving_snow_cid_0805c8a0 |

**NEW card_info.inc: NOBLEMAN_OF_EXTERMINATION_CID = 0x1364**
Evidence: card-stats.s "Nobleman of Extermination slot=0x1364" -- confirmed. grep card_info.inc "0x1364": 0 hits -- new.
Consumer: check_equip_target_zone_validity_by_card_id plate says "0x1364 (Nobleman of Extermination)". asm/07 line 793. Confidence: high.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c8bc | 0x00001364 | NOBLEMAN_OF_EXTERMINATION_CID | nobleman_extermination_cid_0805c8bc |

**NEW card_info.inc: BAIT_DOLL_CID = 0x149b**
Evidence: card-stats.s "Bait Doll slot=0x149b" -- confirmed. grep card_info.inc "0x149b": 0 hits -- new.
Consumer: check_equip_target_zone_validity_by_card_id plate says "0x149b (Bait Doll)". asm/07 line 793. Confidence: high.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c8b8 | 0x0000149b | BAIT_DOLL_CID | bait_doll_cid_0805c8b8 |

**Reuse card_info.inc: CRIMSON_NINJA_CID = 0x16b8** (card_info.inc line 744 confirmed present)
Evidence: card_info.inc line 744: `.equ CRIMSON_NINJA_CID, 0x000016b8 @ Crimson Ninja (pw=14618326)`.
Consumer: check_equip_target_zone_validity_by_card_id plate says "0x16b8 (Crimson Ninja)". asm/07 line 793. Confidence: high.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c920 | 0x000016b8 | CRIMSON_NINJA_CID | crimson_ninja_cid_0805c920 |

**NEW card_info.inc: cid_131c = 0x131c (low confidence -- unassigned slot)**
Evidence: card-stats.s: slot 0x131c not present (record scan of 22B stride across card-stats ROM range 0x018169B8..0x01832601 yielded 0 matches for slot_id=0x131c). grep card_info.inc "0x131c": 0 hits.
Consumer: check_equip_target_zone_validity_by_card_id uses 0x131c as dispatch upper boundary ("if cid <= 0x131c"). asm/07 line 842. Name cid_131c (neutral hex label per S1-pitfall rule). Confidence: low.
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c86c | 0x0000131c | cid_131c | cid_131c_0805c86c |

**NEW card_info.inc: cid_12fb = 0x12fb (low confidence -- unassigned slot)**
Evidence: card-stats.s: slot 0x12fb not present (record scan yielded 0 matches). Function plate says "RESERVED_CARD_ID=0x12fb (no released card name, reserved icid)". grep card_info.inc "0x12fb": 0 hits.
Consumer: check_equip_slot_eligible_without_reserved_field_card uses 0x12fb as count_field_copies_of_card arg. asm/07 line 1933. Confidence: low (unassigned).
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805cf8c | 0x000012fb | cid_12fb | cid_12fb_0805cf8c |

**Scalar slots (all 3 resolved to reuse -- 0 new scalars)**

(a) 0x0000fe4 -> HARPIE_LADY_CID reuse (card_info.inc:311)
Consumer: dispatch_effect_for_neo_daedalus_paired_slot calls count_paired_slots_both_sides(0x0fe4); plate says "PAIRED_SLOT_ARG=0xfe4". Grep constants/*.inc "0x0fe4" / "0xfe4": card_info.inc:311 HARPIE_LADY_CID=0x00000fe4 -- confirmed same value. count_paired_slots_both_sides in all other call sites takes CID args (0x128b=Lord_of_D, 0x159d=Necrovalley, 0x13c7=Revival_Jam), so 0xfe4 IS Harpie Lady CID -- reuse mandatory per C5. PAIRED_SLOTS_SEARCH_ARG dropped; reuse HARPIE_LADY_CID.
Confidence: high (same card-ID domain as all other count_paired_slots_both_sides args).
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c514 | 0x00000fe4 | HARPIE_LADY_CID | harpie_lady_cid_0805c514 |

(b) 0x0000ffff -> SLOT_CARD_EMPTY reuse (card_info.inc:386)
Consumer: check_equip_chain_pair_placement_eligible compares result of find_equip_chain_pair_across_field against 0xffff (invalid/not-found sentinel). Plate says "INVALID_PAIR=0xffff". card_info.inc:386 SLOT_CARD_EMPTY=0x0000ffff: "empty slot sentinel: u16 card_id=0xffff means no card" -- semantics match (low-16 of return = 0xffff means no pair found, same as card slot empty sentinel). Reuse mandatory per C5.
EOL note: "SLOT_CARD_EMPTY reuse: 0xffff = no pair found (same sentinel as card slot empty check)"
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805c794 | 0x0000ffff | SLOT_CARD_EMPTY | slot_card_empty_0805c794 |

(c) 0xffff0000 -> EQUIP_CHAIN_SENTINEL reuse (duel_field.inc:270)
Consumer: check_equip_slot_eligible_with_chain_node_type_d: lsls r0,r0,#0x10 then cmp r0,r1 where r1=0xffff0000; if equal -> node not found path. Plate says "INVALID_NODE=0xffff0000". duel_field.inc:270 EQUIP_CHAIN_SENTINEL=0xffff0000: "gEquipChainSlotRefs list terminator sentinel" -- same sentinel pattern. Reuse mandatory per C5.
EOL note: "EQUIP_CHAIN_SENTINEL reuse: post-lsls#16 sentinel check for no-node-found (low-16 of return = 0xffff)"
| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805ca88 | 0xffff0000 | EQUIP_CHAIN_SENTINEL | equip_chain_sentinel_0805ca88 |

### REF_SLOTS (pointer slots for global labels)

These slots load gP1LifePoints (0x0201c4e0) but are labeled with auto-names. All RENAME to ref gP1LifePoints.

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| 0x0805c380 | gP1LifePoints (0x0201c4e0) | gP1LifePoints | gp1lp_ref_0805c380 |
| 0x0805ce20 | gP1LifePoints (0x0201c4e0) | gP1LifePoints | gp1lp_ref_0805ce20 |
| 0x0805ceb8 | gP1LifePoints (0x0201c4e0) | gP1LifePoints | gp1lp_ref_0805ceb8 |

### RENAME_SLOTS (label rename only -- PTR_ auto-names already have correct value gP1LifePoints)

| slot | slot_label | eol_ascii |
|------|------------|-----------|
| 0x0805c3dc | PTR_gP1LifePoints_0805c3dc -> gp1lp_ptr_0805c3dc | none |
| 0x0805c518 | PTR_gP1LifePoints_0805c518 -> gp1lp_ptr_0805c518 | none |
| 0x0805c5f0 | PTR_gP1LifePoints_0805c5f0 -> gp1lp_ptr_0805c5f0 | none |
| 0x0805c6a8 | PTR_gP1LifePoints_0805c6a8 -> gp1lp_ptr_0805c6a8 | none |
| 0x0805c808 | PTR_gP1LifePoints_0805c808 -> gp1lp_ptr_0805c808 | none |
| 0x0805cae0 | PTR_gP1LifePoints_0805cae0 -> gp1lp_ptr_0805cae0 | none |
| 0x0805cb34 | PTR_gP1LifePoints_0805cb34 -> gp1lp_ptr_0805cb34 | none |
| 0x0805cbf8 | PTR_gP1LifePoints_0805cbf8 -> gp1lp_ptr_0805cbf8 | none |
| 0x0805cfe4 | PTR_gP1LifePoints_0805cfe4 -> gp1lp_ptr_0805cfe4 | none |

Note: These PTR_ labels are pre-existing Ghidra auto-names that already reference gP1LifePoints. In the .s file they appear as `.word gP1LifePoints`. The "RENAME" here means giving the label a shorter non-auto name; the .word value stays unchanged.

### FUNC_RENAME (none)

No function name conflicts detected. All 34 function names in Seg-1 accurately describe their semantics based on consumed evidence (asm/07 plates, callee names). No indeg/caller conflicts.

### PLATE (R5)

No plate rewrite needed for Seg-1. No stale FUN_* found in any function plate (grep `FUN_[0-9a-f]{8}` across lines 1..2060 of asm/07_equip_effect_chain.s: 0 hits). No non-ASCII mojibake found in first 2100 lines (only line 2 has UTF-8 CJK in file header comment -- a regular GAS comment prefixed '@', not a Ghidra plate).

---

## Carve Plan (R7) -- none

All 5 ROM_INCBIN blocks are inter-function code fragments (dispatch-table-reached THUMB code or orphan). None contain pointer tables, string tables, or data structures requiring rom.s carve. The disasm plan (R4) handles the 4 referenced blocks in-place; byte count unchanged post-disasm.

---

## Disasm Plan (R4)

4 blocks require R4 disasm (clearListing range -> setTMode -> DisassembleCommand per fn, per file 06 Seg-5c/6 precedent):

**Block 0x5c40a (0x5e B)**: 2 sub-functions
- Range 0x0805c40a..0x0805c467 (0x5e B)
- .zero 2 at 0x5c40a (keep as padding)
- fn1 entry: 0x0805c40c (THUMB|1 = 0x0805c40d), reached via dispatch table 0x9e43xxx, CIDs include Dream Clown(0x101e), Blade Rabbit(0x1868)
- fn2 entry: 0x0805c43c (THUMB|1 = 0x0805c43d), reached via dispatch table 0x9e4xxxx, CIDs include Fusion Sage(0x1308), Foolish Burial(0x1474), Reinforcement of the Army(0x14d0), Toon Table of Contents(0x1562), Terraforming(0x15a1), and 16 others
- Plate (ASCII): "Reached via card effect handler dispatch table 0x9e43xxx. fn1@0x5c40c: CIDs include 0x101e(Dream Clown) x4 tables. fn2@0x5c43c: CIDs include 0x1308(Fusion Sage), 0x1474, 0x14d0, 0x1562, 0x159c, 0x15a1 x21 tables."

**Block 0x5c608 (0x28 B)**: 1 sub-function
- Range 0x0805c608..0x0805c62f (0x28 B)
- fn entry: 0x0805c608 (THUMB|1 = 0x0805c609), reached via dispatch table 0x9e46408
- CID: 0x11a0 (unassigned slot, not in card-stats.s) fn_slot=2 in 24B record at table 0x9e463fc
- Plate (ASCII): "Reached via card effect handler dispatch table. Hit at 0x9e46408: CID=0x11a0 fn_slot=2."

**Block 0x5cd86 (0x2a B)**: 1 sub-function
- Range 0x0805cd86..0x0805cdaf (0x2a B)
- .zero 2 at 0x5cd86 (keep as padding)
- fn entry: 0x0805cd88 (THUMB|1 = 0x0805cd89), reached via dispatch tables
- CIDs: 0x12c8(Lightforce Sword), 0x12f0(unassigned), 0x1307(Restructer Revolution), 0x1324(Confiscation), 0x1325(Delinquent Duo), 0x132b(The Forceful Sentry) + 9 more; 15 total table hits
- Plate (ASCII): "Reached via card effect handler dispatch table x15 tables. CIDs include 0x12c8(Lightforce Sword), 0x1307(Restructer Revolution), 0x1324(Confiscation), 0x1325(Delinquent Duo) and others."

**Block 0x5cf1c (0x20 B)**: 1 sub-function
- Range 0x0805cf1c..0x0805cf3b (0x20 B)
- fn entry: 0x0805cf1c (THUMB|1 = 0x0805cf1d), reached via dispatch tables
- CIDs: 0x124f(House of Adhesive Tape), 0x1250(unassigned), 0x12e4(Trap Hole); 3 total table hits
- Plate (ASCII): "Reached via card effect handler dispatch table x3. CIDs: 0x124f(House of Adhesive Tape), 0x1250(unassigned), 0x12e4(Trap Hole)."

R4 procedure (per file 06 Seg-5c precedent): clearListing(range) -> setTMode(range) -> DisassembleCommand per fn entry (single-entry dispatch, not entire range at once). literal pools already handled by surrounding code context after disasm. createFunction for each entry point.

---

## New Constants / Globals

New equates to add to **constants/card_info.inc** (11 CIDs + 0 new scalars; all scalar slots resolved to existing constants via reuse):

Note: LORD_OF_D_CID (line 241), WALL_SHADOW_CID (line 712), CRIMSON_NINJA_CID (line 744), HARPIE_LADY_CID (line 311) already present in card_info.inc -- reuse, do not re-add.
Note: SLOT_CARD_EMPTY (card_info.inc:386) and EQUIP_CHAIN_SENTINEL (duel_field.inc:270) already present -- reuse, do not re-add.

```
@ F07-Seg-1 new CIDs:
.equ SANGA_OF_THUNDER_CID,       0x00001119  @ Sanga of the Thunder (card-stats.s slot=0x1119); check_equip_slot_eligible_with_sanga_and_prereqs chain node check; conf: high
.equ SCAPEGOAT_CID,              0x000012d2  @ Scapegoat (card-stats.s slot=0x12d2); min_monster_slots=4 threshold in check_equip_slot_eligible_by_scapegoat_or_stray_lambs; conf: high
.equ GRACEFUL_CHARITY_CID,       0x000012cc  @ Graceful Charity (card-stats.s slot=0x12cc); tier-3 LP cost threshold in check_lp_draw_card_tier_threshold; conf: high
.equ GREENKAPPA_CID,             0x000011f0  @ Greenkappa (card-stats.s slot=0x11f0); dispatch branch boundary in check_equip_target_zone_validity_by_card_id; conf: high
.equ REAPER_OF_CARDS_CID,        0x00000ffa  @ Reaper of the Cards (card-stats.s slot=0x0ffa); direct effect slot read path in check_equip_target_zone_validity_by_card_id; conf: high
.equ HARPIES_FEATHER_DUSTER_CID, 0x00001246  @ Harpie's Feather Duster (card-stats.s slot=0x1246); direct effect slot read path; conf: high
.equ DRIVING_SNOW_CID,           0x0000134d  @ Driving Snow (card-stats.s slot=0x134d); dedicated dispatch branch in check_equip_target_zone_validity_by_card_id; conf: high
.equ NOBLEMAN_EXTERMINATION_CID, 0x00001364  @ Nobleman of Extermination (card-stats.s slot=0x1364); dedicated path in check_equip_target_zone_validity_by_card_id; conf: high
.equ BAIT_DOLL_CID,              0x0000149b  @ Bait Doll (card-stats.s slot=0x149b); dedicated path in check_equip_target_zone_validity_by_card_id; conf: high
.equ cid_131c,                   0x0000131c  @ unassigned slot 0x131c (not in card-stats.s); dispatch upper boundary in check_equip_target_zone_validity_by_card_id; conf: low
.equ cid_12fb,                   0x000012fb  @ unassigned slot 0x12fb (not in card-stats.s); count_field_copies_of_card arg in check_equip_slot_eligible_without_reserved_field_card; conf: low

@ F07-Seg-1 new scalars (1 only -- HARPIE_LADY_CID/SLOT_CARD_EMPTY/EQUIP_CHAIN_SENTINEL are reuses):
@ (none -- all former "new scalar" candidates resolved to existing constants above)
```

### Comprehensive constants/*.inc collision scan (post-fix verification)

All "new" CIDs and scalars in this proposal verified against full `grep -rn <value> constants/*.inc`. Rule: new-marked entries must have 0 hits; reuse-marked entries must have exactly 1 hit confirming the named equate.

| value | entry | grep constants/*.inc result | status |
|-------|-------|-----------------------------|--------|
| 0x00001119 | SANGA_OF_THUNDER_CID (new, card_info.inc) | 1 hit: duel_field.inc:345 EQUIP_SPRITE_CARD_DATA=0x00001119 | NOTE: different domain (sprite card-data arg vs card-ID comparand in chain-node check); reviewer did not flag; retained as new CID in card_info.inc. Reviewer to confirm domain-distinct ruling. |
| 0x000012d2 | SCAPEGOAT_CID (new) | 0 hits | OK |
| 0x000012cc | GRACEFUL_CHARITY_CID (new) | 0 hits | OK |
| 0x000011f0 | GREENKAPPA_CID (new) | 0 hits | OK |
| 0x00000ffa | REAPER_OF_CARDS_CID (new) | 0 hits | OK |
| 0x00001246 | HARPIES_FEATHER_DUSTER_CID (new) | 0 hits | OK |
| 0x0000134d | DRIVING_SNOW_CID (new) | 0 hits | OK (only neighbor 0x134e = cid_134e present) |
| 0x00001364 | NOBLEMAN_EXTERMINATION_CID (new) | 0 hits | OK |
| 0x0000149b | BAIT_DOLL_CID (new) | 0 hits | OK |
| 0x0000131c | cid_131c (new) | 0 hits | OK |
| 0x000012fb | cid_12fb (new) | 0 hits | OK |
| 0x00000fe4 | HARPIE_LADY_CID (reuse, card_info.inc:311) | 1 hit: card_info.inc:311 HARPIE_LADY_CID -- correct | OK (reuse) |
| 0x0000ffff | SLOT_CARD_EMPTY (reuse, card_info.inc:386) | 1 hit: card_info.inc:386 SLOT_CARD_EMPTY -- correct | OK (reuse) |
| 0xffff0000 | EQUIP_CHAIN_SENTINEL (reuse, duel_field.inc:270) | 1 hit: duel_field.inc:270 EQUIP_CHAIN_SENTINEL -- correct | OK (reuse) |

One open question flagged for reviewer: SANGA_OF_THUNDER_CID=0x1119 vs duel_field.inc:345 EQUIP_SPRITE_CARD_DATA=0x1119. Reviewer did not flag as C5 in this review pass. Context: in asm/07 the slot at 0x0805c588 loads 0x1119 as an icid arg to check_node_in_slot_chain (card-ID domain); in asm/06 EQUIP_SPRITE_CARD_DATA is passed as a sprite attribute "card_data" field (not a CID comparand). If reviewer confirms domain-distinct, SANGA_OF_THUNDER_CID stands as new; if reviewer rules same-value strict reuse, the slot would need to adopt EQUIP_SPRITE_CARD_DATA (poor fit semantically).

---

## Sec5.1 Registration (Rule 3) -- 0-reference blocks

| addr | size | Seg | judgment | ref-scan evidence |
|------|------|-----|----------|-------------------|
| 0x0805c4aa | 0x2a (42B) | Seg-1 | orphan THUMB code | Full byte-step scan: raw=0, thumb=0 for all 2B-aligned addresses in block. Starts with .zero 2 at 0x5c4aa then valid THUMB code from 0x5c4ac (ldr/ldrb/lsls/lsrs player_id + gP1LifePoints+player*0x868 load + bcc + bx lr). Function pattern matches other eligibility predicates in segment but unreachable via dispatch table. No createFunction record needed. |

---

## Consumer Evidence (R6) -- key slot semantics

| slot | consumer | file:line | confidence |
|------|----------|-----------|------------|
| 0x0805c588 (0x1119) | check_equip_slot_eligible_with_sanga_and_prereqs plate: "ICID_SANGA=0x1119 (Sanga of the Thunder)" | asm/07_equip_effect_chain.s line 305 | high |
| 0x0805c798 (0x1117) | check_equip_chain_pair_placement_eligible plate: "ZONE_CARD_CHECK_ID=0x1117 (Wall Shadow)" | asm/07_equip_effect_chain.s line 640 | high |
| 0x0805c7bc (0x12d2) | check_equip_slot_eligible_by_scapegoat_or_stray_lambs plate: "SCAPEGOAT_ICID=0x12d2 (Scapegoat)" | asm/07_equip_effect_chain.s line 706 | high |
| 0x0805c7c0 (0x1710) | same function: "STRAY_LAMBS_ICID=0x1710 (Stray Lambs)" | asm/07_equip_effect_chain.s line 717 | high (card_info.inc reuse) |
| 0x0805c67c (0x1102) | check_equip_slot_absent_for_swords_of_light plate: "SWORDS_OF_LIGHT_ICID=0x1102 (Swords of Revealing Light)" | asm/07_equip_effect_chain.s line 494 | high (card_info.inc reuse) |
| 0x0805c514 (0xfe4) | dispatch_effect_for_neo_daedalus_paired_slot plate: "PAIRED_SLOT_ARG=0xfe4"; HARPIE_LADY_CID reuse (card_info.inc:311) -- all count_paired_slots_both_sides callers pass CIDs | asm/07_equip_effect_chain.s line 248 | high |
| 0x0805ca88 (0xffff0000) | check_equip_slot_eligible_with_chain_node_type_d plate: "INVALID_NODE=0xffff0000"; EQUIP_CHAIN_SENTINEL reuse (duel_field.inc:270) | asm/07_equip_effect_chain.s line 1110 | high |
| 0x0805c794 (0xffff) | check_equip_chain_pair_placement_eligible plate: "INVALID_PAIR=0xffff"; SLOT_CARD_EMPTY reuse (card_info.inc:386) | asm/07_equip_effect_chain.s line 640 | high |
| 0x0805cd04 (0x0201b290) | check_toon_equip_chain_zone_eligible: ldr r2, DAT_0805cd04 then ldr r7, DAT_0805cd08 (0x4cc); adds r0,r2,r7 -> gDuelPhaseFlags+0x4cc=node_count | asm/07_equip_effect_chain.s lines 1429-1431 | high |
| 0x0805c86c (0x131c) | check_equip_target_zone_validity_by_card_id: cmp r1,r0 (r1=card_id, r0=0x131c) bgt path -- cid <= 0x131c enters read_effect_slot_side_and_type path | asm/07_equip_effect_chain.s line 824 | med (boundary dispatch) |
| 0x0805cf8c (0x12fb) | check_equip_slot_eligible_without_reserved_field_card: ldr r0=0x12fb, bl count_field_copies_of_card -> if >0 block equip | asm/07_equip_effect_chain.s line 1938 | low (unassigned slot) |

---

## Math Self-Check (EOL verification)

- `0x1cf4`: FIELD_STATE_OFF; confirmed by duel_field.inc comment "asm/07 STAGE_OFF/FIELD_STATE_OFFSET". High.
- `0x1ce8`: P1LP_BLOCK2_OFF_1CE8; ewram.inc comment "184 ROM refs". High.
- `0x868`: PLAYER_BLOCK_STRIDE; ewram.inc comment "0x868=2152 bytes; 2146 raw refs". High.
- `0x4cc`: consumer check_toon_equip_chain_zone_eligible at asm/07 line 1430: `ldr r2=0x0201b290; ldr r7=0x000004cc; adds r0,r2,r7; ldr r0,[r0,#0x0]` -> reads gDuelPhaseFlags+0x4cc. ewram.inc LP_BAR_ANIM_STATE_OFF=0x4cc confirmed by value match. Confidence: high (same-value C5 reuse).
- `0x4d4` and `0x4f4`: same function, adjacent adds to r2 (gDuelPhaseFlags base); ewram.inc SPRITE_ROW_ENTRY_DATA_OFF=0x4d4, CHAIN_NODE_CARD_ARR_OFF=0x4f4. High.
- Block 0x5c40a raw hit at +0x24 (addr=0x0805c42e, raw=1 hit at 0x8327180): examined context -- the hit is within a code sequence (machine word 0xfdc00f0 adjacent at -4B, not a dispatch table structure with preceding CID). Confirmed coincidental instruction encoding, not a data table pointer. Not counted as ref.

---

## Asks (low-confidence items)

1. **cid_12fb (0x12fb)** -- slot not in card-stats.s (0 records found in card-stats ROM range). Function plate says "no released card name, reserved icid". Used in check_equip_slot_eligible_without_reserved_field_card to block equip when card is on field. Name `cid_12fb` is neutral per S1-pitfall rule. Confirm correct vs a cut content / debug card? Confidence: low.

2. **cid_131c (0x131c)** -- slot not in card-stats.s (0 records). Used as dispatch boundary in check_equip_target_zone_validity_by_card_id (bgt branch: cid > 0x131c goes to different path). Name `cid_131c` is neutral. Is 0x131c a range boundary or an actual card? Dark Sage (0x131b), Dark Sage is pw=93902008. Confidence: low.

3. **CID 0x11a0** in dispatch table (block 0x5c608) -- single table hit; slot 0x11a0 not found in card-stats.s. The block is confirmed THUMB code reachable via table but the associated card name is unknown. Block can be disassembled without card name for plate.

4. **RESOLVED: 0x0fe4 = HARPIE_LADY_CID** -- formerly listed as PAIRED_SLOTS_SEARCH_ARG. All other count_paired_slots_both_sides call sites pass named CIDs (Lord_of_D=0x128b, Necrovalley=0x159d, Revival_Jam=0x13c7); card_info.inc:311 HARPIE_LADY_CID=0x0fe4 confirmed. Slot 0x0805c514 now uses HARPIE_LADY_CID. No open question remaining.
