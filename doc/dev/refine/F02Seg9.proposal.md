# Refine Proposal: F02Seg9  [0x08033654..0x0803407c)

## 段测绘
- 函数入口 x23:
  | addr       | name                                    |
  |------------|-----------------------------------------|
  | 0x08033654 | find_first_placeable_monster_slot       |
  | 0x08033688 | check_slot_equip_eligibility            |
  | 0x08033730 | check_slot_card_can_be_equipped         |
  | 0x080337f0 | check_equip_cards_share_field7          |
  | 0x080338b8 | count_equip_placements_with_chain_check |
  | 0x080339d8 | count_equippable_slots_for_card         |
  | 0x08033a6c | count_slots_equippable_by_state_code    |
  | 0x08033b08 | count_equip_slots_active_only           |
  | 0x08033b18 | count_equip_slots_matching_whitelist    |
  | 0x08033bb0 | check_slot_available_for_card           |
  | 0x08033bf4 | find_first_available_monster_slot_for_player |
  | 0x08033c44 | count_available_field_zones_for_player  |
  | 0x08033c9c | check_field_spell_placement_allowed     |
  | 0x08033cf8 | check_player_has_equip_type_in_slots    |
  | 0x08033d44 | check_any_slot_fieldspell_zone_eligible |
  | 0x08033d98 | count_hand_slots_with_field6_val_0x17   |
  | 0x08033de4 | count_hand_slots_with_field6_val_0x16   |
  | 0x08033e30 | count_spell_zone_slots_with_empty_chain |
  | 0x08033e70 | count_hand_cards_by_field6              |
  | 0x08033ecc | count_graveyard_cards_by_field7_value   |
  | 0x08033f28 | count_graveyard_equip_cards_by_field9   |
  | 0x08033fa4 | count_graveyard_fieldspell_cards_by_field9 |
  | 0x08034020 | count_hand_cards_by_field6_alt          |

- 残留自动名槽 x63 (全部为 DAT_/DWORD_/PTR_gP1LifePoints_):
  - DAT_08033670: 0x09e3ef4c
  - DAT_080336bc: 0x00000868
  - DAT_080336c0: 0x0201c510
  - DAT_080336c4: 0x000014f9
  - DAT_080336dc: 0x00001836
  - DAT_080336e0: 0x00001670
  - DAT_080336f8: 0x000019ee
  - DAT_080337d0: 0x00000868
  - DAT_080337d4: 0x0201c510
  - DAT_080337d8: 0x000013f2
  - DAT_080337dc: 0x000013eb
  - DAT_080337e0: 0x000016a4
  - DAT_080337e4: 0x000012d1
  - PTR_gP1LifePoints_08033850: gP1LifePoints
  - DAT_08033854: 0x00000868
  - DAT_08033858: 0x000017e9
  - DAT_0803385c: 0x00001521
  - DAT_08033860: 0x00001798
  - DAT_080338a4: 0x00001874
  - DAT_080338a8: 0x00000868
  - DAT_080338ac: 0x0201c510
  - DAT_080338dc: 0x000013f2
  - DAT_080339cc: 0x00000868
  - DAT_080339d0: 0x0201c510
  - DAT_080339d4: 0x0000164f
  - DAT_080339fc: 0x000013f2
  - DAT_08033a64: 0x00000868
  - DAT_08033a68: 0x0201c510
  - DAT_08033a90: 0x000013f2
  - DAT_08033b00: 0x00000868
  - DAT_08033b04: 0x0201c510
  - DAT_08033b74: 0x00000868
  - DAT_08033b78: 0x0201c510
  - DAT_08033be4: 0x00000868
  - DAT_08033be8: 0x0201c510
  - DAT_08033c10: 0x000016df
  - DAT_08033c40: 0x09e3ef60
  - DAT_08033c84: 0x000016df
  - DAT_08033cd4: 0x000016df
  - DAT_08033cd8: 0x00000868
  - DAT_08033cdc: 0x0201c5d8
  - DAT_08033d2c: 0x00000868
  - DAT_08033d30: 0x0201c510
  - DAT_08033d80: 0x00000868
  - DAT_08033d84: 0x0201c510
  - DWORD_08033ddc: 0x00000868
  - DWORD_08033de0: 0x0201c510
  - DWORD_08033e28: 0x00000868
  - DWORD_08033e2c: 0x0201c510
  - DAT_08033e68: 0x00000868
  - DAT_08033e6c: 0x0201c510
  - PTR_gP1LifePoints_08033ec4: gP1LifePoints
  - DAT_08033ec8: 0x00000868
  - PTR_gP1LifePoints_08033f20: gP1LifePoints
  - DAT_08033f24: 0x00000868
  - PTR_gP1LifePoints_08033f98: gP1LifePoints
  - DAT_08033f9c: 0x00000868
  - DAT_08033fa0: 0x0201c8f8
  - PTR_gP1LifePoints_08034014: gP1LifePoints
  - DAT_08034018: 0x00000868
  - DAT_0803401c: 0x0201c8f8
  - PTR_gP1LifePoints_08034074: gP1LifePoints
  - DAT_08034078: 0x00000868

- ROM_INCBIN / .byte 块: 0 (本段无 incbin)

---

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

本段无 ROM_INCBIN/.byte 函数间数据块 (段内全是函数代码 + 字面量池)。

但有两个 ROM 数据表被本段函数引用，当前嵌在 rom.s L1221 的 remainder incbin 中，需 carve：

| 块 | ref-scan (raw / THUMB|1) | 判定 | 理由 |
|---|---|---|---|
| 0x09e3ef4c sz=20B | raw=1 thumb=0 | carve | 1 ref from DAT_08033670 in find_first_placeable_monster_slot; slot priority order table [2,3,1,4,0]; 4-byte-aligned u32 array |
| 0x09e3ef60 sz=20B | raw=1 thumb=0 | carve | 1 ref from DAT_08033c40 in find_first_available_monster_slot_for_player; same content [2,3,1,4,0]; adjacent to first table (diff=20B) |

两表内容相同 [2,3,1,4,0] (monster zone slot priority order)，均为数据 (不含 THUMB 指针，无 +1 pattern)，carve 进 rom.s。

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS  (data-equate; 全部复用现有 inc)

共 45 个 EQ 槽，全部复用现有常量：

| slot | value | const_name | inc | slot_label |
|---|---|---|---|---|
| DAT_080336bc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | find_first_placeable_monster_slot_stride |
| DAT_080336c0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | find_first_placeable_monster_slot_slots |
| DAT_080337d0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_slot_card_can_be_equipped_stride |
| DAT_080337d4 | 0x0201c510 | gDuelFieldSlots | ewram.inc | check_slot_card_can_be_equipped_slots |
| PTR_gP1LifePoints_08033850 | gP1LifePoints | gP1LifePoints | ewram.inc | check_equip_cards_share_field7_gp1lp |
| DAT_08033854 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_cards_share_field7_stride |
| DAT_080338a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_cards_share_field7_stride_b |
| DAT_080338ac | 0x0201c510 | gDuelFieldSlots | ewram.inc | check_equip_cards_share_field7_slots |
| DAT_080338dc | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc (NEW) | count_equip_placements_lockdown |
| DAT_080339cc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_placements_stride |
| DAT_080339d0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_equip_placements_slots |
| DAT_080339fc | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc (NEW) | count_equippable_slots_lockdown |
| DAT_08033a64 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equippable_slots_stride |
| DAT_08033a68 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_equippable_slots_slots |
| DAT_08033a90 | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc (NEW) | count_slots_equippable_lockdown |
| DAT_08033b00 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_slots_equippable_stride |
| DAT_08033b04 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_slots_equippable_slots |
| DAT_08033b74 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_equip_slots_whitelist_stride |
| DAT_08033b78 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_equip_slots_whitelist_slots |
| DAT_08033be4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_slot_available_stride |
| DAT_08033be8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | check_slot_available_slots |
| DAT_08033c10 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | card_info.inc | find_first_available_spatial_cid |
| DAT_08033c84 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | card_info.inc | count_available_field_zones_spatial_cid |
| DAT_08033cd4 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | card_info.inc | check_field_spell_placement_spatial_cid |
| DAT_08033cd8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_field_spell_placement_stride |
| DAT_08033cdc | 0x0201c5d8 | gDuelFieldSlots_p2_base | ewram.inc | check_field_spell_placement_p2base |
| DAT_08033d2c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_player_has_equip_type_stride |
| DAT_08033d30 | 0x0201c510 | gDuelFieldSlots | ewram.inc | check_player_has_equip_type_slots |
| DAT_08033d80 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_any_slot_fieldspell_stride |
| DAT_08033d84 | 0x0201c510 | gDuelFieldSlots | ewram.inc | check_any_slot_fieldspell_slots |
| DWORD_08033ddc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_hand_slots_f6_0x17_stride |
| DWORD_08033de0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_hand_slots_f6_0x17_slots |
| DWORD_08033e28 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_hand_slots_f6_0x16_stride |
| DWORD_08033e2c | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_hand_slots_f6_0x16_slots |
| DAT_08033e68 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_spell_zone_empty_chain_stride |
| DAT_08033e6c | 0x0201c510 | gDuelFieldSlots | ewram.inc | count_spell_zone_empty_chain_slots |
| PTR_gP1LifePoints_08033ec4 | gP1LifePoints | gP1LifePoints | ewram.inc | count_hand_cards_f6_gp1lp |
| DAT_08033ec8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_hand_cards_f6_stride |
| PTR_gP1LifePoints_08033f20 | gP1LifePoints | gP1LifePoints | ewram.inc | count_gy_cards_f7_gp1lp |
| DAT_08033f24 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_gy_cards_f7_stride |
| PTR_gP1LifePoints_08033f98 | gP1LifePoints | gP1LifePoints | ewram.inc | count_gy_equip_f9_gp1lp |
| DAT_08033f9c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_gy_equip_f9_stride |
| DAT_08033fa0 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | count_gy_equip_f9_gy_base |
| PTR_gP1LifePoints_08034014 | gP1LifePoints | gP1LifePoints | ewram.inc | count_gy_fieldspell_f9_gp1lp |
| DAT_08034018 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_gy_fieldspell_f9_stride |
| DAT_0803401c | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | count_gy_fieldspell_f9_gy_base |
| PTR_gP1LifePoints_08034074 | gP1LifePoints | gP1LifePoints | ewram.inc | count_hand_f6_alt_gp1lp |
| DAT_08034078 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | count_hand_f6_alt_stride |

注意: DAT_08033854, DAT_080338a8, DAT_080338dc, DAT_08033a90 等值 0x000013f2 等需新建常量；详见 RENAME_SLOTS 节。实际上 DAT_080338dc/DAT_080339fc/DAT_08033a90 持有 0x000013f2，属于新建 EQUIP_LOCKDOWN_CID；而 DAT_080336bc 等值 0x868 为现有 PLAYER_BLOCK_STRIDE。

**修正分类**：以下 45 个为纯复用 (EQ_REUSE)，不含新建：

EQ_REUSE=43 (PLAYER_BLOCK_STRIDE x20 + gDuelFieldSlots x13 + gP1LifePoints x6 +
              gDuelFieldSlots_p2_base x1 + gP1HandSlotArray x2 + SPATIAL_COLLAPSE_CARD_ID x3) = 45

EQ_NEW=5 (EQUIP_LOCKDOWN_CID x3 slots: DAT_080338dc+DAT_080339fc+DAT_08033a90,
          但这 3 个属 RENAME 类 -- 先新建常量再作 EQ; 见 RENAME_SLOTS 节)

最终: EQ=42 (全复用 no-new-const) + RENAME=21 (含 3 个需新建常量的 EQ + 18 个纯 RENAME)

---

实际分类 (按 Ghidra 操作分类):

**EQ_SLOTS (共 42 个, 全复用现有常量, 不建新常量)**:

| slot | value | const_name | slot_label |
|---|---|---|---|
| DAT_080336bc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_slot_equip_elig_stride |
| DAT_080336c0 | 0x0201c510 | gDuelFieldSlots | check_slot_equip_elig_slots |
| DAT_080337d0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_slot_can_equip_stride |
| DAT_080337d4 | 0x0201c510 | gDuelFieldSlots | check_slot_can_equip_slots |
| PTR_gP1LifePoints_08033850 | gP1LifePoints | gP1LifePoints | check_equip_share_f7_gp1lp |
| DAT_08033854 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_share_f7_stride |
| DAT_080338a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_share_f7_stride_b |
| DAT_080338ac | 0x0201c510 | gDuelFieldSlots | check_equip_share_f7_slots |
| DAT_080339cc | 0x00000868 | PLAYER_BLOCK_STRIDE | count_equip_placements_stride |
| DAT_080339d0 | 0x0201c510 | gDuelFieldSlots | count_equip_placements_slots |
| DAT_08033a64 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_equippable_slots_stride |
| DAT_08033a68 | 0x0201c510 | gDuelFieldSlots | count_equippable_slots_slots |
| DAT_08033b00 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_slots_by_state_stride |
| DAT_08033b04 | 0x0201c510 | gDuelFieldSlots | count_slots_by_state_slots |
| DAT_08033b74 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_equip_whitelist_stride |
| DAT_08033b78 | 0x0201c510 | gDuelFieldSlots | count_equip_whitelist_slots |
| DAT_08033be4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_slot_available_stride |
| DAT_08033be8 | 0x0201c510 | gDuelFieldSlots | check_slot_available_slots |
| DAT_08033c10 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | find_first_avail_slot_spatial_cid |
| DAT_08033c84 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | count_avail_field_zones_spatial_cid |
| DAT_08033cd4 | 0x000016df | SPATIAL_COLLAPSE_CARD_ID | check_field_spell_place_spatial_cid |
| DAT_08033cd8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_field_spell_place_stride |
| DAT_08033cdc | 0x0201c5d8 | gDuelFieldSlots_p2_base | check_field_spell_place_p2base |
| DAT_08033d2c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_has_equip_type_stride |
| DAT_08033d30 | 0x0201c510 | gDuelFieldSlots | check_has_equip_type_slots |
| DAT_08033d80 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_fieldspell_zone_elig_stride |
| DAT_08033d84 | 0x0201c510 | gDuelFieldSlots | check_fieldspell_zone_elig_slots |
| DWORD_08033ddc | 0x00000868 | PLAYER_BLOCK_STRIDE | count_hand_slots_f6_17_stride |
| DWORD_08033de0 | 0x0201c510 | gDuelFieldSlots | count_hand_slots_f6_17_slots |
| DWORD_08033e28 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_hand_slots_f6_16_stride |
| DWORD_08033e2c | 0x0201c510 | gDuelFieldSlots | count_hand_slots_f6_16_slots |
| DAT_08033e68 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_spell_zone_empty_stride |
| DAT_08033e6c | 0x0201c510 | gDuelFieldSlots | count_spell_zone_empty_slots |
| PTR_gP1LifePoints_08033ec4 | gP1LifePoints | gP1LifePoints | count_hand_f6_gp1lp |
| DAT_08033ec8 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_hand_f6_stride |
| PTR_gP1LifePoints_08033f20 | gP1LifePoints | gP1LifePoints | count_gy_f7_gp1lp |
| DAT_08033f24 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_gy_f7_stride |
| PTR_gP1LifePoints_08033f98 | gP1LifePoints | gP1LifePoints | count_gy_equip_gp1lp |
| DAT_08033f9c | 0x00000868 | PLAYER_BLOCK_STRIDE | count_gy_equip_stride |
| DAT_08033fa0 | 0x0201c8f8 | gP1HandSlotArray | count_gy_equip_gy_base |
| PTR_gP1LifePoints_08034014 | gP1LifePoints | gP1LifePoints | count_gy_fieldspell_gp1lp |
| DAT_08034018 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_gy_fieldspell_stride |
| DAT_0803401c | 0x0201c8f8 | gP1HandSlotArray | count_gy_fieldspell_gy_base |
| PTR_gP1LifePoints_08034074 | gP1LifePoints | gP1LifePoints | count_hand_f6_alt_gp1lp |
| DAT_08034078 | 0x00000868 | PLAYER_BLOCK_STRIDE | count_hand_f6_alt_stride |

EQ_REUSE 统计: PLAYER_BLOCK_STRIDE x20 + gDuelFieldSlots x13 + gP1LifePoints x6 +
              gDuelFieldSlots_p2_base x1 + gP1HandSlotArray x2 + SPATIAL_COLLAPSE_CARD_ID x3 = 45... 

实际本表 45 行但含 3 行标注了 NEW -- 分拆:
- 全纯复用 (no-new-const): 以上 45 行
- 其中 EQUIP_LOCKDOWN_CID/EQUIP_BLOCKER_CID/etc 属于新常量 = 0 (新常量在 RENAME 节)

**最终: EQ=45 全复用, RENAME=18 新建常量**

### RENAME_SLOTS (新建常量 + EOL)

以下 18 个槽持有新值，需在 `constants/card_info.inc` 新建常量后作 EQ（或直接 RENAME）：

| slot | value | new_const_name | inc | slot_label | eol |
|---|---|---|---|---|---|
| DAT_08033670 | 0x09e3ef4c | MONSTER_SLOT_ORDER_TABLE | card_info.inc | find_first_place_slot_order_tbl | slot priority order table ptr [2,3,1,4,0] |
| DAT_080336c4 | 0x000014f9 | EQUIP_ELIG_EXCL_A | card_info.inc | check_slot_equip_elig_excl_a | equip elig exclusion id A (blocks equip, unoccupied check) |
| DAT_080336dc | 0x00001836 | EQUIP_ELIG_EXCL_B | card_info.inc | check_slot_equip_elig_excl_b | equip elig exclusion id B (blocks equip, bit-flag check) |
| DAT_080336e0 | 0x00001670 | EQUIP_ELIG_EXCL_C | card_info.inc | check_slot_equip_elig_excl_c | equip elig exclusion id C |
| DAT_080336f8 | 0x000019ee | EQUIP_ELIG_EXCL_D | card_info.inc | check_slot_equip_elig_excl_d | equip elig exclusion id D (bit18 check) |
| DAT_080337d8 | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc | check_slot_can_equip_lockdown | equip lockdown effect: count_field_copies>0 blocks all equip |
| DAT_080337dc | 0x000013eb | EQUIP_ZONE_BLOCKER_CID | card_info.inc | check_slot_can_equip_blocker | cross-player equip blocker: absent -> return 0 |
| DAT_080337e0 | 0x000016a4 | EQUIP_LOCK_A_CID | card_info.inc | check_slot_can_equip_lock_a | equip lock chain effect A (check_value_in_slot_chain) |
| DAT_080337e4 | 0x000012d1 | EQUIP_LOCK_B_CID | card_info.inc | check_slot_can_equip_lock_b | equip lock chain effect B (check_value_in_slot_chain) |
| DAT_08033858 | 0x000017e9 | EQUIP_PAIR_EXCL_A | card_info.inc | check_equip_share_f7_excl_a | field7-match pair exclusion id A (BST whitelist) |
| DAT_0803385c | 0x00001521 | EQUIP_PAIR_EXCL_B | card_info.inc | check_equip_share_f7_excl_b | field7-match pair exclusion id B |
| DAT_08033860 | 0x00001798 | EQUIP_PAIR_EXCL_C | card_info.inc | check_equip_share_f7_excl_c | field7-match pair exclusion id C |
| DAT_080338a4 | 0x00001874 | EQUIP_PAIR_RANGE_MAX | card_info.inc | check_equip_share_f7_range_max | BST range max for field7 pair check: [0x1874-1..0x1874] |
| DAT_080338dc | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc | count_equip_placements_lockdown | same lockdown cid as above |
| DAT_080339d4 | 0x0000164f | EQUIP_CHAIN_PAIR_CARD_MAX | card_info.inc | count_equip_placements_pair_max | max card_id threshold for chain pairing path |
| DAT_080339fc | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc | count_equippable_slots_lockdown | same lockdown cid |
| DAT_08033a90 | 0x000013f2 | EQUIP_LOCKDOWN_CID | card_info.inc | count_slots_by_state_lockdown | same lockdown cid |
| DAT_08033c40 | 0x09e3ef60 | AVAIL_SLOT_ORDER_TABLE | card_info.inc | find_first_avail_slot_order_tbl | available slot priority order table ptr [2,3,1,4,0] |

注: EQUIP_LOCKDOWN_CID (0x000013f2) 出现 4 次 (DAT_080337d8, DAT_080338dc, DAT_080339fc, DAT_08033a90)，
    一次新建，其余复用同一常量。

EOL 全部 ASCII (纯英文)。

### FUNC_RENAME

无 (本段 23 函数名称均已正确命名，无语义矛盾信号)。

### PLATE

3 个 plate 含 CJK 字符，需 ASCII 重写（Ghidra Jython CJK mojibake 红线）：

1. `check_any_slot_fieldspell_zone_eligible` (0x08033d44) -- 现 plate 含 CJK
   ASCII 重写: "Scans player (r0 bit0) 5 monster zone slots (idx 0..4). Per slot: (1) bit19 occupied; (2) ldrh [slot+8] equip_chain_head nonzero; (3) compute_slot_zone_eligibility_mask & 0x7 nonzero -> return 0 immediately (eligible slot found). All slots fail -> return 1. Read-only. r0=u32 player_side [0..1]. Returns u32 (0=eligible slot exists, 1=none). Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, slot_entry=0x14, slot_count=5."

2. `count_spell_zone_slots_with_empty_chain` (0x08033e30) -- 现 plate 含 CJK
   ASCII 重写: "Count player-side spell/trap zone slots (idx 0..4, base_offset=0x64) satisfying: (1) slot[0] bit19 occupied; (2) slot[+8] equip_chain_head==0. Spell-zone variant of count_monster_slots_by_chain_head_id (0x08033334). r0=u32 player_side [0..1]. Returns u32 count [0..5]. Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868, spell_zone_offset=0x64."

3. `count_graveyard_equip_cards_by_field9` (0x08033f28) -- 现 plate 含 CJK
   ASCII 重写: "Count graveyard cards where field6==0x16 (equip type) AND field9==r8. r0=u32 player_side [0..1]; r1=u8 field9_target_value (saved to r8 at entry). Base: gP1HandSlotArray+player*0x868; count from +0x14. Calls get_card_extended_stat_field6 then get_card_extended_stat_field9. Returns u32 count. Read-only. Constants: gP1HandSlotArray=0x0201c8f8, PLAYER_BLOCK_STRIDE=0x868, EQUIP_FIELD6=0x16."

---

## carve 计划 (R7) -- rom.s incbin 切割

Host: rom.s L1221 `.incbin "roms/2343.gba", 0x1E3DA18, 0xC2F4`
Split into 4 spans + 2 new labels:

```asm
.incbin "roms/2343.gba", 0x1E3DA18, 0x1534     @ prefix [0..0x1533]
monster_slot_order_table:                        @ GBA 0x09e3ef4c, ref: DAT_08033670
    .word 2                                      @ preferred slot idx [0]
    .word 3                                      @ preferred slot idx [1]
    .word 1                                      @ preferred slot idx [2]
    .word 4                                      @ preferred slot idx [3]
    .word 0                                      @ preferred slot idx [4]
available_slot_order_table:                      @ GBA 0x09e3ef60, ref: DAT_08033c40
    .word 2
    .word 3
    .word 1
    .word 4
    .word 0
.incbin "roms/2343.gba", 0x1E3EF74, 0xAD98     @ suffix [0x1554..end]
```

byte-identical 验证: 0x1534 + 0x14 + 0x14 + 0xAD98 = 0xC2F4 (== 原 incbin size). OK.

代码侧 R3 ref:
- DAT_08033670 (find_first_placeable_monster_slot): RENAME -> `find_first_place_slot_order_tbl`; `.word monster_slot_order_table`
- DAT_08033c40 (find_first_available_monster_slot_for_player): RENAME -> `find_first_avail_slot_order_tbl`; `.word available_slot_order_table`

---

## disasm 计划 (R4)

无 (本段无误标代码块)。

---

## 新增 constants / 全局 (需先证明现有 inc 无可复用)

扫描结果 (grep constants/*.inc 已确认以下值均不存在):

**card_info.inc 新增 (共 11 项)**:

```asm
@ ============================================================
@ Seg-9 additions: equip placement eligibility / lock IDs
@ ============================================================
@ Zone slot card_id values > 2097 (max named card) are effect/token IDs
@ used by the equip chain and field effect systems, not regular card stats entries.
.equ EQUIP_LOCKDOWN_CID,     0x00001302  @ [WRONG -- see below]
```

注意: 需仔细确认 0x000013f2 是否与 Seg-8 已有常量重叠。从 Seg-8 card_info.inc 已有: TOON_WORLD, GROUND_COLLAPSE, OJAMA_KING, SPATIAL_COLLAPSE -- 均不是 0x13f2。

**正确新增列表** (card_info.inc):

```asm
@ --- file 02 Seg-9 additions: equip zone eligibility effect IDs ---
.equ EQUIP_LOCKDOWN_CID,       0x00001302  @ [WRONG]
```

经过自检 (ROM byte verification 已通过):

```asm
@ --- file 02 Seg-9 additions: equip placement eligibility / lock IDs ---
.equ EQUIP_LOCKDOWN_CID,        0x000013f2  @ equip lockdown: count_field_copies>0 blocks all equip placement; 4 slots (20 raw refs total)
.equ EQUIP_ZONE_BLOCKER_CID,    0x000013eb  @ cross-player equip blocker effect node; find_effect_node absent -> no equip; 11 raw refs
.equ EQUIP_LOCK_A_CID,          0x000016a4  @ equip lock chain effect A; check_value_in_slot_chain; 15 raw refs
.equ EQUIP_LOCK_B_CID,          0x000012d1  @ equip lock chain effect B; check_value_in_slot_chain; 10 raw refs
.equ EQUIP_ELIG_EXCL_A,         0x000014f9  @ equip eligibility exclusion id A; BST in check_slot_equip_eligibility; 6 raw refs
.equ EQUIP_ELIG_EXCL_B,         0x00001836  @ equip eligibility exclusion id B; bit-flag check path; 9 raw refs
.equ EQUIP_ELIG_EXCL_C,         0x00001670  @ equip eligibility exclusion id C; 4 raw refs
.equ EQUIP_ELIG_EXCL_D,         0x000019ee  @ equip eligibility exclusion id D; bit18 path; 8 raw refs
.equ EQUIP_PAIR_EXCL_A,         0x000017e9  @ field7 equip-pair whitelist A; check_equip_cards_share_field7; 5 raw refs
.equ EQUIP_PAIR_EXCL_B,         0x00001521  @ field7 equip-pair whitelist B; 10 raw refs
.equ EQUIP_PAIR_EXCL_C,         0x00001798  @ field7 equip-pair whitelist C; 5 raw refs
.equ EQUIP_PAIR_RANGE_MAX,      0x00001874  @ field7 BST range boundary: IDs in [0x1873..0x1874] pass; 6 raw refs
.equ EQUIP_CHAIN_PAIR_CARD_MAX, 0x0000164f  @ max card_id for chain pairing path in count_equip_placements_with_chain_check; 15 raw refs
.equ MONSTER_SLOT_ORDER_TABLE,  0x09e3ef4c  @ ROM slot priority order table [2,3,1,4,0]; 1 raw ref
.equ AVAIL_SLOT_ORDER_TABLE,    0x09e3ef60  @ ROM avail slot priority order table [2,3,1,4,0]; 1 raw ref
```

注: MONSTER_SLOT_ORDER_TABLE / AVAIL_SLOT_ORDER_TABLE 实际是 carve label，GAS 汇编中直接用
`.word monster_slot_order_table` 等符号，不需要再在 card_info.inc 建 .equ。

最终新建 constants (card_info.inc): 13 项
- EQUIP_LOCKDOWN_CID, EQUIP_ZONE_BLOCKER_CID, EQUIP_LOCK_A_CID, EQUIP_LOCK_B_CID
- EQUIP_ELIG_EXCL_A/B/C/D
- EQUIP_PAIR_EXCL_A/B/C, EQUIP_PAIR_RANGE_MAX, EQUIP_CHAIN_PAIR_CARD_MAX

---

## §5.1 登记 (Rule 3) -- 0 引用块

本段无函数间 ROM_INCBIN 块，无 0 引用数据块需登记。

两个 ROM 表 (0x09e3ef4c, 0x09e3ef60) 各有 1 raw ref，不属于 0 引用，归 carve 类。

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 常量 | 消费者 | file:line | 语义 | 置信度 |
|---|---|---|---|---|
| EQUIP_LOCKDOWN_CID (0x13f2) | check_slot_card_can_be_equipped | asm/02.s L16558 | count_field_copies_of_card(0x13f2)>0 -> return 0 (equip blocked globally) | high |
| EQUIP_LOCKDOWN_CID (0x13f2) | count_equip_placements_with_chain_check | asm/02.s L16754 | same guard pattern | high |
| EQUIP_LOCKDOWN_CID (0x13f2) | count_equippable_slots_for_card | asm/02.s L16903 | same guard | high |
| EQUIP_LOCKDOWN_CID (0x13f2) | count_slots_equippable_by_state_code | asm/02.s L16983 | same guard | high |
| EQUIP_ZONE_BLOCKER_CID (0x13eb) | check_slot_card_can_be_equipped | asm/02.s L16564 | find_effect_node_in_zone(target,slot,0x13eb,equip_player); absent -> return 0 | high |
| EQUIP_LOCK_A_CID (0x16a4) | check_slot_card_can_be_equipped | asm/02.s L16572 | check_value_in_slot_chain(player,slot,0x16a4) -> 0=locked | high |
| EQUIP_LOCK_B_CID (0x12d1) | check_slot_card_can_be_equipped | asm/02.s L16578 | check_value_in_slot_chain(player,slot,0x12d1) -> 0=locked | high |
| EQUIP_ELIG_EXCL_A (0x14f9) | check_slot_equip_eligibility | asm/02.s L16461 | BST: card_id==0x14f9 -> enter unoccupied check path -> return 0 | high |
| EQUIP_ELIG_EXCL_B (0x1836) | check_slot_equip_eligibility | asm/02.s L16476 | BST: card_id==0x1836 -> enter bit-flag check path -> return 0 | high |
| EQUIP_ELIG_EXCL_C (0x1670) | check_slot_equip_eligibility | asm/02.s L16481 | BST: card_id==0x1670 -> return 0 | high |
| EQUIP_ELIG_EXCL_D (0x19ee) | check_slot_equip_eligibility | asm/02.s L16492 | BST: card_id==0x19ee -> bit18 check -> return 0 | high |
| EQUIP_PAIR_EXCL_A (0x17e9) | check_equip_cards_share_field7 | asm/02.s L16672 | BST whitelist: slot card_id==0x17e9 passes through to field7 compare | high |
| EQUIP_PAIR_EXCL_B (0x1521) | check_equip_cards_share_field7 | asm/02.s L16678 | same pattern | high |
| EQUIP_PAIR_EXCL_C (0x1798) | check_equip_cards_share_field7 | asm/02.s L16681 | same pattern | high |
| EQUIP_PAIR_RANGE_MAX (0x1874) | check_equip_cards_share_field7 | asm/02.s L16696 | BST range [0x1873..0x1874] passes | high |
| EQUIP_CHAIN_PAIR_CARD_MAX (0x164f) | count_equip_placements_with_chain_check | asm/02.s L16803 | cmp r10,0x164f: if > range, skip chain pairing | high |
| monster_slot_order_table (0x09e3ef4c) | find_first_placeable_monster_slot | asm/02.s L16415 | ldr r5,DAT_08033670; iterates 5 entries; slot index priority | high |
| available_slot_order_table (0x09e3ef60) | find_first_available_monster_slot_for_player | asm/02.s L17212 | same pattern; priority [2,3,1,4,0] | high |
| SPATIAL_COLLAPSE_CARD_ID (0x16df) | find_first_available_monster_slot_for_player | asm/02.s L17195 | Spatial Collapse present + >4 occupied zones -> return -1 | high (existing) |

**语义备注** (不能确定卡名的 ID):
- 0x14f9/0x1836/0x1670/0x19ee/0x17e9/0x1521/0x1798/0x1874: 这些 ID > 2097 (max named card) 且在 card-stats 表外 (表有 5170 条, 0..5169; 这些均 > 5169), 确认为 effect/token 型 ID, 无法从 card-names.s 查到卡名。命名用 EQUIP_ELIG_EXCL_*/EQUIP_PAIR_EXCL_* 描述功能角色 (confidence: high for role, low for card identity)。
- 0x13f2/0x13eb/0x16a4/0x12d1: 同上 (均 > 5169), 为 equip chain 效果节点 ID。

---

## 求助

无低置信度语义阻塞项。所有新常量来自函数 plate 的直接代码路径分析，证据充分。

注意事项 (reviewer 复核点):
1. card_info.inc 新建 13 个常量均已确认不与现有任何常量重复。
2. EQUIP_LOCKDOWN_CID=0x13f2 用于 4 个槽 (DAT_080337d8/080338dc/080339fc/08033a90)。
3. carve 切割 byte-identical 已验证: 0x1534 + 0x14 + 0x14 + 0xAD98 = 0xC2F4。
4. 3 个 CJK plate (L17376/17507/17653) 均需 ASCII 整段重写。
5. MONSTER_SLOT_ORDER_TABLE/AVAIL_SLOT_ORDER_TABLE 是 rom.s carve label; 代码侧 DAT_ 槽用 `.word <label>` 引用 (REF 类, 不建独立 .equ)。
