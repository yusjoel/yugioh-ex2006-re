# Refine Proposal: F11-Seg-3b  [0x080872e4..0x08087d58)

## 段测绘
- 函数入口: 15 函数 (地址序)
  - 0x080872e4 write_equip_zone_entries_by_lv_card_id  (最大, ~49 literal-pool 槽)
  - 0x0808767c populate_equip_zone_entries_substate_e_by_pair
  - 0x080876dc scan_zone_equip_target_eligible_substate_c
  - 0x08087758 write_all_equip_zone_entries_substate_c
  - 0x08087794 scan_zone_gadget_pair_check_substate_d
  - 0x08087870 scan_zone_equip_category_match_substate_e
  - 0x080878c8 scan_zone_field5_atk_bound_substate_d
  - 0x0808796c scan_zone_chimera_pair_check_substate_e
  - 0x08087a20 scan_zone_field6_eq_eval_placement_substate_b
  - 0x08087a80 scan_zone_parasite_node_check_substate_d
  - 0x08087b00 scan_zone_labyrinth_pair_placement_substate_d
  - 0x08087ba8 scan_zone_field6_one_placement_substate_b
  - 0x08087bf4 scan_player_zone_equip_criteria_substate_c
  - 0x08087c4c scan_both_players_field5_eligible_substate_e
  - 0x08087cf0 scan_zone_opponent_field5_substate_e

- 残留自动名槽: 105 slots (92 DAT_ + 13 PTR_gP1LifePoints_*)  x105
- ROM_INCBIN / .byte 块: 0 (大 ROM_INCBIN 从 0x87d58 起, 正好是 Seg-4 起点, 不在本段)
- Stale FUN_: grep asm/*.s FUN_080872e4..FUN_08087cf0 = 0 hits (全已命名)

## 数据块分类 (Rule 2/3)
本段内无 ROM_INCBIN / .byte 块 (均为 literal-pool .word 槽在函数体内)。
不需要 disasm/carve 分析。

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (82 slots total)
#### CID 槽 (67 slots) — 全部是 .word <card_id> literal pools
下表: slot addr / value / const_name / REUSE 或 NEW / slot_label

| slot addr   | value    | const_name                   | status | slot_label                        |
|-------------|----------|------------------------------|--------|-----------------------------------|
| 0x08087338  | 0x17d7   | MYSTIC_SWORDSMAN_LV2_CID     | REUSE  | lv_cid_87338                      |
| 0x0808733c  | 0x10e4   | ELEGANT_EGOTIST_CID          | NEW    | lv_cid_8733c                      |
| 0x08087340  | 0x0fb6   | TIME_WIZARD_CID              | REUSE  | lv_cid_87340                      |
| 0x08087350  | 0x1529   | GREAT_DEZARD_CID             | REUSE  | lv_cid_87350                      |
| 0x0808736c  | 0x165a   | A_DEAL_WITH_DARK_RULER_CID   | REUSE  | lv_cid_8736c                      |
| 0x0808737c  | 0x167e   | SAGES_STONE_CID              | REUSE  | lv_cid_8737c                      |
| 0x080873a4  | 0x17d1   | ULTIMATE_INSECT_LV1_CID      | REUSE  | lv_cid_873a4                      |
| 0x080873ac  | 0x17c9   | THEINEN_THE_GREAT_SPHINX_CID | REUSE  | lv_cid_873ac                      |
| 0x080873c8  | 0x17d3   | HORUS_LV6_CID                | REUSE  | lv_cid_873c8                      |
| 0x080873fc  | 0x1822   | ULTIMATE_INSECT_LV3_CID      | REUSE  | lv_cid_873fc                      |
| 0x08087418  | 0x1814   | SILENT_SWORDSMAN_LV5_CID     | REUSE  | lv_cid_87418                      |
| 0x0808741c  | 0x1812   | SILENT_SWORDSMAN_LV3_CID     | REUSE  | lv_cid_8741c                      |
| 0x0808742c  | 0x1817   | SILENT_MAGICIAN_LV4_CID      | REUSE  | lv_cid_8742c                      |
| 0x08087450  | 0x1907   | TRANSCENDENT_WINGS_CID       | REUSE  | lv_cid_87450                      |
| 0x08087460  | 0x187e   | RELEASE_RESTRAINT_CID        | NEW    | lv_cid_87460                      |
| 0x0808747c  | 0x19b5   | ATTACK_REFLECTOR_UNIT_CID    | REUSE  | lv_cid_8747c                      |
| 0x0808748c  | 0x19d8   | TRIAL_OF_THE_PRINCESSES_CID  | REUSE  | lv_cid_8748c                      |
| 0x08087494  | 0x146e   | DARK_SAGE_CID                | NEW    | lv_cid_87494                      |
| 0x080874a4  | 0x0fe4   | HARPIE_LADY_CID              | REUSE  | lv_cid_874a4                      |
| 0x080874ac  | 0x1534   | FUSHIOH_RICHIE_CID           | REUSE  | lv_cid_874ac                      |
| 0x080874b4  | 0x0fa7   | BLUE_EYES_WHITE_DRAGON_CID   | REUSE  | lv_cid_874b4                      |
| 0x080874bc  | 0x1643   | MIRAGE_KNIGHT_CID            | NEW    | lv_cid_874bc                      |
| 0x080874c4  | 0x1644   | BERSERK_DRAGON_CID           | REUSE  | lv_cid_874c4                      |
| 0x080874cc  | 0x0fc9   | DARK_MAGICIAN_CID_0FC9       | REUSE  | lv_cid_874cc                      |
| 0x080874d4  | 0x173d   | MYSTICAL_SHINE_BALL_CID      | NEW    | lv_cid_874d4                      |
| 0x080874dc  | 0x1788   | SPIRIT_OF_PHARAOH_CID        | NEW    | lv_cid_874dc                      |
| 0x080874e4  | 0x1822   | ULTIMATE_INSECT_LV3_CID      | REUSE  | lv_cid_874e4  (dup value of 873fc)|
| 0x080874ec  | 0x185e   | ULTIMATE_INSECT_LV5_CID      | REUSE  | lv_cid_874ec                      |
| 0x080874f4  | 0x18af   | ULTIMATE_INSECT_LV7_CID      | REUSE  | lv_cid_874f4                      |
| 0x080874fc  | 0x17d4   | HORUS_LV8_CID                | REUSE  | lv_cid_874fc                      |
| 0x08087504  | 0x17d6   | DARK_MIMIC_LV3_CID           | REUSE  | lv_cid_87504                      |
| 0x0808750c  | 0x17d8   | MYSTIC_SWORDSMAN_LV4_CID     | REUSE  | lv_cid_8750c                      |
| 0x08087514  | 0x1823   | MYSTIC_SWORDSMAN_LV6_CID     | REUSE  | lv_cid_87514                      |
| 0x0808751c  | 0x17da   | ARMED_DRAGON_LV5_CID         | REUSE  | lv_cid_8751c                      |
| 0x08087524  | 0x17db   | ARMED_DRAGON_LV7_CID         | REUSE  | lv_cid_87524                      |
| 0x0808753c  | 0x1816   | SILENT_SWORDSMAN_LV7_CID     | REUSE  | lv_cid_8753c                      |
| 0x08087544  | 0x181a   | SILENT_MAGICIAN_LV8_CID      | REUSE  | lv_cid_87544                      |
| 0x0808754c  | 0x185c   | SACRED_PHOENIX_CID           | REUSE  | lv_cid_8754c                      |
| 0x08087554  | 0x186b   | GEARFRIED_SWORDMASTER_CID    | REUSE  | lv_cid_87554                      |
| 0x0808755c  | 0x1906   | WINGED_KURIBOH_LV10_CID      | REUSE  | lv_cid_8755c                      |
| 0x08087568  | 0x19a8   | CYBER_BARRIER_DRAGON_CID     | NEW    | lv_cid_87568                      |
| 0x0808757c  | 0x1757   | WHITE_MAGICIAN_PIKERU_CID    | REUSE  | lv_cid_8757c                      |
| 0x08087580  | 0x191d   | EBON_MAGICIAN_CURRAN_CID     | REUSE  | lv_cid_87580                      |
| 0x08087588  | 0x19cd   | PRINCESS_PIKERU_CID          | REUSE  | lv_cid_87588                      |
| 0x08087668  | 0x19ce   | PRINCESS_CURRAN_CID          | REUSE  | lv_cid_87668                      |
| 0x080876d8  | 0x12e5   | POLYMERIZATION_CID           | REUSE  | poly_cid_876d8                    |
| 0x080877b4  | 0x139d   | BIRDFACE_CID                 | REUSE  | gadget_cid_877b4                  |
| 0x080877b8  | 0x1293   | BERFOMET_CID                 | NEW    | gadget_cid_877b8                  |
| 0x080877d0  | 0x180b   | RED_GADGET_CID               | REUSE  | gadget_cid_877d0                  |
| 0x080877d4  | 0x1807   | GREEN_GADGET_CID             | REUSE  | gadget_cid_877d4                  |
| 0x080877e0  | 0x180c   | YELLOW_GADGET_CID            | REUSE  | gadget_cid_877e0                  |
| 0x080877e8  | 0x12e5   | POLYMERIZATION_CID           | REUSE  | gadget_cid_877e8 (dup 876d8)      |
| 0x080877f0  | 0x1291   | GAZELLE_CID                  | NEW    | gadget_cid_877f0                  |
| 0x080877f8  | 0x0fe4   | HARPIE_LADY_CID              | REUSE  | gadget_cid_877f8                  |
| 0x08087804  | 0x180c   | YELLOW_GADGET_CID            | REUSE  | gadget_cid_87804 (dup 877e0)      |
| 0x0808780c  | 0x1807   | GREEN_GADGET_CID             | REUSE  | gadget_cid_8780c (dup 877d4)      |
| 0x08087964  | 0x05dc   | CARD_STAT_LP_THRESHOLD_1500  | REUSE  | atk_thr_87964                     |
| 0x08087968  | 0x12a1   | zone_query_hand_tag_12a1     | REUSE  | zone_qtag_87968                   |
| 0x08087988  | 0x1294   | CHIMERA_FLYING_MYTHICAL_BEAST_CID | REUSE | chimera_cid_87988             |
| 0x0808798c  | 0x1631   | MIRACLE_RESTORING_CID        | REUSE  | chimera_cid_8798c                 |
| 0x08087998  | 0x1291   | GAZELLE_CID                  | NEW    | chimera_cid_87998 (dup 877f0)     |
| 0x080879c8  | 0x0fc9   | DARK_MAGICIAN_CID_0FC9       | REUSE  | chimera_cid_879c8                 |
| 0x080879cc  | 0x1377   | BUSTER_BLADER_CID            | NEW    | chimera_cid_879cc                 |
| 0x08087afc  | 0x12a1   | PARASITE_PARACIDE_CID        | REUSE  | para_cid_87afc                    |
| 0x08087b18  | 0x1232   | MAGICAL_LABYRINTH_CID        | REUSE  | lab_cid_87b18                     |
| 0x08087b20  | 0x1117   | WALL_SHADOW_CID              | REUSE  | lab_cid_87b20                     |
| 0x08087b98  | 0x0fc9   | DARK_MAGICIAN_CID_0FC9       | REUSE  | lab_cid_87b98 (dup 874cc)         |

#### PLAYER_BLOCK_STRIDE 槽 (15 slots)
所有 .word 0x868 -> PLAYER_BLOCK_STRIDE (REUSE; constants/duel_field.inc)

| slot addr   | value | const_name          | slot_label         |
|-------------|-------|---------------------|--------------------|
| 0x08087670  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87670       |
| 0x080876d4  | 0x868 | PLAYER_BLOCK_STRIDE | stride_876d4       |
| 0x08087750  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87750       |
| 0x08087790  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87790       |
| 0x0808786c  | 0x868 | PLAYER_BLOCK_STRIDE | stride_8786c       |
| 0x080878c4  | 0x868 | PLAYER_BLOCK_STRIDE | stride_878c4       |
| 0x0808795c  | 0x868 | PLAYER_BLOCK_STRIDE | stride_8795c       |
| 0x080879d4  | 0x868 | PLAYER_BLOCK_STRIDE | stride_879d4       |
| 0x08087a78  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87a78       |
| 0x08087af4  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87af4       |
| 0x08087ba0  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87ba0       |
| 0x08087bec  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87bec       |
| 0x08087c48  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87c48       |
| 0x08087ce8  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87ce8       |
| 0x08087d54  | 0x868 | PLAYER_BLOCK_STRIDE | stride_87d54       |

### REF_SLOTS (10 slots) — .word <RAM/ROM addr>

| slot addr   | value      | gas_label           | slot_label         | source               |
|-------------|------------|---------------------|--------------------|----------------------|
| 0x08087674  | 0x0201c600 | gP1FieldArrayCBase  | ref_87674          | duel_field.inc REUSE |
| 0x08087a7c  | 0x0201c600 | gP1FieldArrayCBase  | ref_87a7c          | duel_field.inc REUSE |
| 0x08087bf0  | 0x0201c600 | gP1FieldArrayCBase  | ref_87bf0          | duel_field.inc REUSE |
| 0x08087678  | 0x0201c740 | gP1SlotSetCodeArray | ref_87678          | duel_field.inc REUSE |
| 0x08087960  | 0x0201c740 | gP1SlotSetCodeArray | ref_87960          | duel_field.inc REUSE |
| 0x08087af8  | 0x0201c740 | gP1SlotSetCodeArray | ref_87af8          | duel_field.inc REUSE |
| 0x08087ba4  | 0x0201c740 | gP1SlotSetCodeArray | ref_87ba4          | duel_field.inc REUSE |
| 0x08087754  | 0x0201c880 | gP1ChainZoneArray   | ref_87754          | duel_field.inc REUSE |
| 0x08087a1c  | 0x0201c8f8 | gP1HandSlotArray    | ref_87a1c          | duel_field.inc REUSE |
| 0x08087cec  | 0x0201c8f8 | gP1HandSlotArray    | ref_87cec          | duel_field.inc REUSE |

### RENAME_SLOTS (13 slots) — PTR_gP1LifePoints_xxxx -> already .word gP1LifePoints
These slots contain `.word gP1LifePoints` (already symbolized); only the slot label needs renaming.

| slot addr   | current_label                  | new_slot_label      |
|-------------|--------------------------------|---------------------|
| 0x0808766c  | PTR_gP1LifePoints_0808766c     | ptr_lp_8766c        |
| 0x080876d0  | PTR_gP1LifePoints_080876d0     | ptr_lp_876d0        |
| 0x0808774c  | PTR_gP1LifePoints_0808774c     | ptr_lp_8774c        |
| 0x0808778c  | PTR_gP1LifePoints_0808778c     | ptr_lp_8778c        |
| 0x08087868  | PTR_gP1LifePoints_08087868     | ptr_lp_87868        |
| 0x080878c0  | PTR_gP1LifePoints_080878c0     | ptr_lp_878c0        |
| 0x08087958  | PTR_gP1LifePoints_08087958     | ptr_lp_87958        |
| 0x080879d0  | PTR_gP1LifePoints_080879d0     | ptr_lp_879d0        |
| 0x08087af0  | PTR_gP1LifePoints_08087af0     | ptr_lp_87af0        |
| 0x08087b9c  | PTR_gP1LifePoints_08087b9c     | ptr_lp_87b9c        |
| 0x08087c44  | PTR_gP1LifePoints_08087c44     | ptr_lp_87c44        |
| 0x08087ce4  | PTR_gP1LifePoints_08087ce4     | ptr_lp_87ce4        |
| 0x08087d50  | PTR_gP1LifePoints_08087d50     | ptr_lp_87d50        |

### FUNC_RENAME (误名订正)
None required. All 15 function names are accurate to their body semantics.
- scan_zone_gadget_pair_check_substate_d: also covers Berfomet/Birdface pairs, but Gadget-first
  naming is acceptable shorthand. THUMB indeg=9 (fn-ptr table); high-cost rename. No change.
- scan_zone_labyrinth_pair_placement_substate_d: also covers Dark Magic Curtain (0x12de) family.
  THUMB indeg=2; imprecise but not wrong. No change.

### PLATE (R5 rewrites — all over-500 chars trimmed to <=490 chars; all ASCII)
14 functions need plate rewrites (scan_player_zone_equip_criteria_substate_c is already 487 chars, OK).
3 functions have factual errors corrected in the new plates (marked *CORRECTED*).

**write_equip_zone_entries_by_lv_card_id** (0x080872e4) — current 1162 chars -> new 490:
```
Equip zone entry writer for LV-card pairs. r0=player_id, r1=target_card_id. BST on r1 maps LV-pair cards (Mystic Swordsman LV2/4/6, Ultimate Insect LV1/3/5/7, Horus LV6/8, Armed Dragon LV5/7, Silent Swordsman LV3/5/7, Silent Magician LV4/8, others) to sp[0]=base_cid sp[4]=evo_cid. Elegant Egotist: calls get_card_evolution_target_ids. Phase 2: scans player gP1FieldArrayCBase slots, check_card_pair_allowed(sp[0/4], slot_card), writes substate=0xb. Phase 3: opponent slots, substate=0xd.
```

**populate_equip_zone_entries_substate_e_by_pair** (0x0808767c) *CORRECTED* — current 875 -> 339:
```
Equip zone writer for Polymerization pair. r0=player_id. Reads [gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x14] alt_slot_count. Loops gP1HandSlotArray+player*stride, extracts card_id bits[18:0], calls check_card_pair_allowed(card_id, POLYMERIZATION_CID). Pass -> write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Returns void.
```
CORRECTION: old plate said "gDuelCardPool_alt_base=gP1LifePoints+0x418"; correct name is gP1HandSlotArray.

**scan_zone_equip_target_eligible_substate_c** (0x080876dc) — current 765 -> 412:
```
Equip activation scan callback, substate=0xc. r0=player_id, r8=zone count ptr (fn-ptr frame). Iterates [gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x18] zone list; extracts card_id bits[18:0]; gate 1: check_card_is_equip_target_eligible, gate 2: check_card_id_is_equip_excluded_range. Both pass -> write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Used as fn-ptr via count_zone_pair_hits_with_fn_ptr.
```

**write_all_equip_zone_entries_substate_c** (0x08087758) — current 617 -> 340:
```
Equip write callback, substate=0xc, unconditional path. r0=player_id. Reads [gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x18] zone count. Loops: write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx) for every slot, no eligibility check. Sibling of scan_zone_equip_target_eligible_substate_c (0x080876dc) which filters by eligibility.
```

**scan_zone_gadget_pair_check_substate_d** (0x08087794) — current 912 -> 432:
```
Equip scan callback, substate=0xd, card-pair dispatch. r1=input_card_id selects pair target r6: Green Gadget->Red Gadget; Red Gadget->Green/Yellow Gadget; Yellow Gadget->itself; Polymerization->input; Berfomet->Gazelle; Birdface->Harpie Lady. Iterates [gP1LifePoints+player*PLAYER_BLOCK_STRIDE+0x10] monster zone; check_card_pair_allowed(slot_card, r6). Pass -> write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx).
```

**scan_zone_equip_category_match_substate_e** (0x08087870) *CORRECTED* — current 646 -> 339:
```
Equip scan callback, substate=0xe, field6 category filter. r0=player_id. Iterates gP1HandSlotArray+player*PLAYER_BLOCK_STRIDE (offset 0x14 for zone count). Extracts card_id bits[18:0]; calls get_card_extended_stat_field6(card_id); if == CARD_FIELD6_EQUIP_CONTINUOUS (0x16) -> write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx).
```
CORRECTION: old plate said "MONSTER_ZONE_BASE=0x0201c5d8"; body uses 0x83<<3=0x418 offset from gP1LifePoints = 0x0201c8f8 = gP1HandSlotArray. conf: high (asm lines 5477-5481 verify).

**scan_zone_field5_atk_bound_substate_d** (0x080878c8) — current 732 -> 417:
```
Equip scan callback, substate=0xd, triple gate: field5 nonzero + ATK<=1500 + no Parasite node. r0=player_id, r8=fn-ptr frame. Iterates gP1SlotSetCodeArray+player*stride. Gates: check_card_field5_is_nonzero; get_card_extended_stat_field4_raw<=CARD_STAT_LP_THRESHOLD_1500; find_effect_node_in_zone(player_id, 0xb, zone_query_hand_tag_12a1)==0. All pass -> write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx).
```

**scan_zone_chimera_pair_check_substate_e** (0x0808796c) — current 742 -> 439:
```
Equip scan callback, substate=0xe, Chimera/Miracle Restoring pair check. r0=player_id, r1=input_card_id. Dispatch: CHIMERA_FLYING_MYTHICAL_BEAST_CID->sp[0]=GAZELLE_CID, sp[4]=BERFOMET_CID; MIRACLE_RESTORING_CID->sp[0]=DARK_MAGICIAN_CID_0FC9, sp[4]=BUSTER_BLADER_CID. Iterates gP1HandSlotArray+player*stride; dual-pass (r4 in 0..1): check_card_pair_allowed(slot_card, sp[r4*4]). Pass -> write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx).
```

**scan_zone_field6_eq_eval_placement_substate_b** (0x08087a20) — current 572 -> 402:
```
Equip scan callback, substate=0xb. r0=player_id, r1=target_card_id, r2=zone_slot_idx (saved to r8). Reads gP1FieldArrayCBase+player*stride+slot*4; extracts card_id. Gate 1: get_card_extended_stat_field6(zone_card)==get_card_extended_stat_field6(r1_card). Gate 2: eval_equip_placement_full_check(player_id, zone_card, 0). Both pass -> write_equip_zone_entry_by_substate(player_id, 0xb, zone_slot_idx).
```

**scan_zone_parasite_node_check_substate_d** (0x08087a80) — current 727 -> 353:
```
Equip scan callback, substate=0xd, Parasite Paracide node check. r0=player_id. Iterates gP1SlotSetCodeArray+player*stride+0x10. Per slot: card_id==PARASITE_PARACIDE_CID? If so, extracts zone_type, builds zone_key; find_effect_node_in_zone(player_id, 0xb, zone_key)==0 (no existing node) -> write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx).
```

**scan_zone_labyrinth_pair_placement_substate_d** (0x08087b00) — current 824 -> 451:
```
Equip scan callback, substate=0xd, Labyrinth/Dark Magic Curtain pair + placement. r0=player_id, r1=input_card_id. Dispatch: MAGICAL_LABYRINTH_CID->WALL_SHADOW_CID (r8); DARK_MAGIC_CURTAIN_CID->DARK_MAGICIAN_CID_0FC9 (r8). Iterates gP1SlotSetCodeArray+player*stride+0x10; check_card_pair_allowed(slot_card, r8). Pass: eval_equip_placement_full_check(player_id, zone_card, 1). Both pass -> write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx).
```

**scan_zone_field6_one_placement_substate_b** (0x08087ba8) — current 690 -> 407:
```
Equip scan callback, substate=0xb. r0=player_id, r2=zone_slot_idx. Reads gP1FieldArrayCBase+player*stride+slot*4. Gate 1: get_card_extended_stat_field6(zone_card)==1. Gate 2: eval_equip_placement_full_check(player_id, zone_card, 0). Both pass -> write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Sibling of scan_zone_field6_eq_eval_placement_substate_b: uses constant 1 not target card field6.
```

**scan_both_players_field5_eligible_substate_e** (0x08087c4c) — current 669 -> 390:
```
Equip scan callback, substate=0xe, dual-player loop. r8=player_id (write target). Outer loop r2 in 0..1 (both player sides via eors r5,r2); inner loop r4=0..zone_count-1. Reads gP1HandSlotArray+player*stride+0x14 zone count. Gates: check_card_field5_is_nonzero; check_zone_slot_equip_eligible(r8, player_side, slot_idx). Both pass -> write_equip_zone_entry_by_substate(r8, 0xe, slot_idx).
```

**scan_zone_opponent_field5_substate_e** (0x08087cf0) — current 730 -> 464:
```
Equip scan callback, substate=0xe, opponent-side field5 scan. r0=player_id; opponent=1-player_id. Iterates gP1LifePoints+opponent*PLAYER_BLOCK_STRIDE+0x14 zone count; reads gP1LifePoints+opponent*stride+0x418 (gP1HandSlotArray offset); extracts card_id; check_card_field5_is_nonzero. Pass -> write_equip_zone_entry_by_substate(opponent_id, 0xe, slot_idx). Contrast: scan_both_players_field5_eligible_substate_e (0x08087c4c) scans both sides + checks eligibility.
```

## carve 计划 (R7)
None. No ROM_INCBIN within [0x080872e4, 0x08087d58).

## disasm 计划 (R4)
None. No .byte blocks or mislabeled code regions within range.

## 新增 constants / 全局 (C5 value-grep=0 confirmed)
Add to `constants/card_info.inc` or create new `constants/lv_card_cids.inc` (recommend appending to card_info.inc under a new section heading for LV/evolution card CIDs):

| const_name                | value    | card                                      | ROM raw_refs | card-stats.s ref               |
|---------------------------|----------|-------------------------------------------|--------------|--------------------------------|
| ELEGANT_EGOTIST_CID       | 0x10e4   | Elegant Egotist (pw=90219263)             | 14           | card_0288 slot=0x10E4          |
| DARK_SAGE_CID             | 0x146e   | Dark Sage (pw=...)                        | 15           | card_0882 slot=0x146E (approx) |
| MIRAGE_KNIGHT_CID         | 0x1643   | Mirage Knight (pw=49217579)               | 11           | card_1308 slot=0x1643          |
| MYSTICAL_SHINE_BALL_CID   | 0x173d   | Mystical Shine Ball (pw=39552864)         | 5            | card_1512 slot=0x173D          |
| SPIRIT_OF_PHARAOH_CID     | 0x1788   | Spirit of the Pharaoh (pw=25343280)       | 9            | card_1570 slot=0x1788          |
| RELEASE_RESTRAINT_CID     | 0x187e   | Release Restraint (pw=75417459)           | 10           | card_1791 slot=0x187E          |
| CYBER_BARRIER_DRAGON_CID  | 0x19a8   | Cyber Barrier Dragon (pw=...)             | 7            | card slot=0x19A8               |
| GAZELLE_CID               | 0x1291   | Gazelle the King of Mythical Beasts (pw=05818798) | 11   | card_0607 slot=0x1291          |
| BERFOMET_CID              | 0x1293   | Berfomet (pw=77207191)                    | 14           | card_0609 slot=0x1293          |
| BUSTER_BLADER_CID         | 0x1377   | Buster Blader (pw=78193831)               | 8            | card_0787 slot=0x1377          |

Note: SAGES_STONE_CID (0x167e) already exists in card_info.inc -> REUSE.
Note: MYSTIC_SWORDSMAN_LV2_CID (0x17d7) already exists -> REUSE.

## §5.1 登记 (Rule 3) — 0 引用块
None. All residual slots in this segment are literal pool words within function bodies with direct code references; no orphan data blocks exist.

## 消费者证据 (R6) — 关键槽语义

**gP1FieldArrayCBase (0x0201c600)** — asm/11 L5145: `.word 0x0201c600` @ 0x08087674, used as zone scan base in write_equip_zone_entries_by_lv_card_id Phase 2; matches gP1FieldArrayCBase definition in duel_field.inc (115 ROM raw refs). conf: high.

**gP1SlotSetCodeArray (0x0201c740)** — asm/11 L5147: `.word 0x0201c740` @ 0x08087678, scan base for Phase 3 (opponent zone); matches gP1SlotSetCodeArray in duel_field.inc (82 ROM raw refs). conf: high.

**gP1HandSlotArray (0x0201c8f8)** — asm/11 L5709: `.word 0x0201c8f8` @ 0x08087a1c, used as Chimera pair scan base; matches gP1HandSlotArray in duel_field.inc (97 ROM raw refs). conf: high.

**gP1ChainZoneArray (0x0201c880)** — asm/11 L5272: `.word 0x0201c880` @ 0x08087754, used as scan_zone_equip_target_eligible zone data base; matches gP1ChainZoneArray in duel_field.inc (21 ROM raw refs). conf: high.

**CARD_STAT_LP_THRESHOLD_1500 (0x5dc)** — asm/11 L5596: `.word 0x000005dc` @ 0x08087964, r1 = upper bound for get_card_extended_stat_field4_raw in scan_zone_field5_atk_bound; matches CARD_STAT_LP_THRESHOLD_1500/LP_COST_1500 (both 0x5dc, distinct domains; 35 raw refs). conf: high.

**zone_query_hand_tag_12a1 (0x12a1)** — asm/11 L5598: `.word 0x12a1` @ 0x08087968, passed as r2 (3rd arg) to find_effect_node_in_zone in scan_zone_field5_atk_bound; semantics = zone query tag, not direct card_id compare. Distinct from PARASITE_PARACIDE_CID (0x12a1 @ 0x08087afc) which is used in cmp r2,r0 (direct card_id equality test in scan_zone_parasite_node). Established in Seg-1a; conf: high.

**CARD_FIELD6_EQUIP_CONTINUOUS (0x16)** — asm/11 L5487: `cmp r0,#0x16` in scan_zone_equip_category_match_substate_e; matches existing CARD_FIELD6_EQUIP_CONTINUOUS=0x16 in duel_field.inc. This value is an immediate compare, not a slot — no EQ slot needed; referenced via plate only. conf: high.

**Plate corrections (factual)**:
- populate_equip_zone_entries_substate_e_by_pair: old plate "gDuelCardPool_alt_base" is wrong; body computes gP1LifePoints+0x83<<3=0x418=gP1HandSlotArray. Evidence: asm/11 L5168-5170 `movs r4,#0x83; lsls r4,r4,#0x3; adds r0,r3,r4`. conf: high.
- scan_zone_equip_category_match_substate_e: old plate "MONSTER_ZONE_BASE=0x0201c5d8" is wrong; body computes same 0x83<<3=0x418 offset from gP1LifePoints = 0x0201c8f8. Evidence: asm/11 L5477-5480 `movs r4,#0x83; lsls r4,r4,#0x3; adds r0,r3,r4`. conf: high.
- write_equip_zone_entries_by_lv_card_id: old plate references "gDuelEffectZones" and "gDuelCardPool_alt"; correct names are gP1FieldArrayCBase and gP1SlotSetCodeArray per DAT_08087674/0x08087678 verified values. conf: high.

## 求助
None. All semantic decisions have high-confidence evidence from asm body + existing constant cross-references.
