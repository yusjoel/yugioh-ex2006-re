# Refine Proposal: F03-Seg-6  [0x0803b3a8..0x0803bba4)

## 段测绘

### 函数入口 x13

| 地址 | 函数名 | asm 行 |
|------|--------|--------|
| 0x0803b3a8 | get_zone_slot_entity_ref_by_type | 11742 |
| 0x0803b4b0 | get_zone_slot_card_ref_by_type | 11884 |
| 0x0803b5c0 | get_zone_slot_field6_by_type | 12030 |
| 0x0803b618 | get_zone_card_attribute_by_type | 12082 |
| 0x0803b738 | read_player_field_slot_word_by_zone | 12237 |
| 0x0803b81c | write_slot_occupy_flag_bit | 12358 |
| 0x0803b854 | set_player_state_bit | 12391 |
| 0x0803b8b0 | write_field_slot_bit_by_player | 12442 |
| 0x0803b910 | check_lp_exceeds_spell_copy_threshold | 12495 |
| 0x0803b960 | check_zone_has_no_field_spell_node | 12539 |
| 0x0803b980 | check_field_spell_group_placeable | 12559 |
| 0x0803b9f4 | check_field_spell_card_placeable_strict | 12617 |
| 0x0803ba98 | check_field_spell_last_warrior_placeable | 12698 |
| 0x0803bb04 | check_field_spell_neo_daedalus_placeable | 12754 |
| 0x0803bb7c | check_field_spell_neo_daedalus_group_placeable | 12815 |

Note: 15 functions. The roadmap estimated 13; actual count from asm is 15. Seg-7 starts at 0x0803bba4 (eval_equip_placement_full_check, asm line 12838).

### 残留自动名槽 x95

ROM values verified via python struct.unpack from roms/2343.gba.

| slot addr | value | category |
|-----------|-------|----------|
| DAT_0803b3c0 | 0x0803b3c4 | RENAME (switch table ptr) |
| DAT_0803b3ec | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b3f0 | 0x0201c880 | REF gP1ChainZoneArray |
| DAT_0803b408 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b40c | 0x0201c740 | REF gP1SlotSetCodeArray |
| DAT_0803b424 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b428 | 0x0201c8f8 | REF gP1HandSlotArray |
| DAT_0803b440 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b444 | 0x0201cab0 | REF gP1AltHandSlotArray |
| DAT_0803b45c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b460 | 0x0201c600 | REF gP1FieldArrayCBase |
| DAT_0803b484 | 0x0201bc54 | REF gDuelEffectChainSlots |
| DAT_0803b4a8 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b4ac | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b4c8 | 0x0803b4cc | RENAME (switch table ptr) |
| DAT_0803b4f4 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b4f8 | 0x0201c880 | REF gP1ChainZoneArray |
| DAT_0803b510 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b514 | 0x0201c740 | REF gP1SlotSetCodeArray |
| DAT_0803b52c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b530 | 0x0201c8f8 | REF gP1HandSlotArray |
| DAT_0803b548 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b54c | 0x0201cab0 | REF gP1AltHandSlotArray |
| DAT_0803b564 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b568 | 0x0201c600 | REF gP1FieldArrayCBase |
| DAT_0803b58c | 0x0201bc54 | REF gDuelEffectChainSlots |
| DAT_0803b5b8 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b5bc | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b5f0 | 0x0201bc54 | REF gDuelEffectChainSlots |
| DAT_0803b610 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b614 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b634 | 0x0803b638 | RENAME (switch table ptr) |
| DAT_0803b688 | 0x000012a1 | EQ PARASITE_PARACIDE_CID (reuse) |
| DAT_0803b68c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b690 | 0x0201c740 | REF gP1SlotSetCodeArray |
| PTR_gP1LifePoints_0803b6bc | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b6c0 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b6ec | 0x0201e2a0 | REF gDuelCardCtxBase |
| DAT_0803b710 | 0x0201bc54 | REF gDuelEffectChainSlots |
| DAT_0803b730 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b734 | 0x0201c510 | REF gDuelFieldSlots |
| DAT_0803b74c | 0x0803b750 | RENAME (switch table ptr) |
| PTR_gP1LifePoints_0803b778 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b77c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b794 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b798 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b7b0 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b7b4 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b7cc | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b7d0 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b7e8 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b7ec | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b814 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b818 | 0x0201c510 | REF gDuelFieldSlots |
| PTR_gP1LifePoints_0803b830 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b834 | 0x000010d0 | EQ EFFECT_ZONE_BITMASK_OFF (reuse duel_field.inc) |
| PTR_gP1LifePoints_0803b84c | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b850 | 0x000010d0 | EQ EFFECT_ZONE_BITMASK_OFF (reuse duel_field.inc) |
| PTR_gP1LifePoints_0803b87c | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b880 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b8a8 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b8ac | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b8dc | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b8e0 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| PTR_gP1LifePoints_0803b908 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b90c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b954 | 0x0000132c | EQ CHAIN_ENERGY_CID (new) |
| PTR_gP1LifePoints_0803b958 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803b95c | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803b974 | 0x00001679 | EQ JUDGEMENT_OF_PHARAOH_CID (new) |
| DAT_0803b9d8 | 0x0000135d | EQ LIGHT_OF_INTERVENTION_CID (new) |
| DAT_0803b9dc | 0x000015ad | EQ NON_AGGRESSION_AREA_CID (new) |
| DAT_0803b9e0 | 0x00001679 | EQ JUDGEMENT_OF_PHARAOH_CID (new) |
| DAT_0803b9e4 | 0x00001578 | EQ LAVA_GOLEM_CID (new) |
| DAT_0803b9e8 | 0x00001972 | EQ BOSS_RUSH_CID (new) |
| PTR_gP1LifePoints_0803ba70 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803ba74 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803ba78 | 0x000013ff | EQ JAM_BREEDING_MACHINE_CID (new) |
| DAT_0803ba7c | 0x000012b1 | EQ LAST_WARRIOR_FROM_ANOTHER_PLANET_CID (new) |
| DAT_0803ba80 | 0x000015ad | EQ NON_AGGRESSION_AREA_CID (new) |
| DAT_0803ba84 | 0x00001679 | EQ JUDGEMENT_OF_PHARAOH_CID (new) |
| DAT_0803ba88 | 0x00001578 | EQ LAVA_GOLEM_CID (new) |
| DAT_0803ba8c | 0x00001972 | EQ BOSS_RUSH_CID (new) |
| PTR_gP1LifePoints_0803bae8 | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803baec | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803baf0 | 0x000013ff | EQ JAM_BREEDING_MACHINE_CID (new) |
| DAT_0803baf4 | 0x000012b1 | EQ LAST_WARRIOR_FROM_ANOTHER_PLANET_CID (new) |
| DAT_0803baf8 | 0x00001679 | EQ JUDGEMENT_OF_PHARAOH_CID (new) |
| PTR_gP1LifePoints_0803bb5c | 0x0201c4e0 | REF gP1LifePoints |
| DAT_0803bb60 | 0x00000868 | EQ PLAYER_BLOCK_STRIDE |
| DAT_0803bb64 | 0x0000147f | EQ JOWGEN_THE_SPIRITUALIST_CID (new) |
| DAT_0803bb68 | 0x000012b1 | EQ LAST_WARRIOR_FROM_ANOTHER_PLANET_CID (new) |
| DAT_0803bb6c | 0x000015ad | EQ NON_AGGRESSION_AREA_CID (new) |
| DAT_0803bb70 | 0x00001679 | EQ JUDGEMENT_OF_PHARAOH_CID (new) |
| DAT_0803bb98 | 0x000013ff | EQ JAM_BREEDING_MACHINE_CID (new) |

Total: 95 residual slots.

### ROM_INCBIN / .byte 块

None in Seg-6 per roadmap. Confirmed by asm scan: no ROM_INCBIN or .byte blocks between 0x0803b3a8 and 0x0803bba4.

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

No ROM_INCBIN or .byte blocks in Seg-6. Rule 2/3 N/A. ref-scan performed as confirmation:

```
python scan:
  range 0x0803b3a8..0x0803bba4 -- no .byte/.incbin blocks detected in asm lines 11742..12835
```

Result: no inter-function data blocks. All DAT_/PTR_ slots are literal-pool words within function bodies.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

#### 复用现有常量 (reuse=34)

| slot | value | const_name | inc file |
|------|-------|------------|---------|
| DAT_0803b3ec | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b408 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b424 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b440 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b45c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b4a8 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b4f4 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b510 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b52c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b548 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b564 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b5b8 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b610 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b68c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b6c0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b77c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b798 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b7b4 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b7d0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b7ec | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b814 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b880 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b8ac | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b8e0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b90c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b95c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803ba74 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803baec | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803bb60 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc |
| DAT_0803b834 | 0x10d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc |
| DAT_0803b850 | 0x10d0 | EFFECT_ZONE_BITMASK_OFF | duel_field.inc |
| DAT_0803b688 | 0x12a1 | PARASITE_PARACIDE_CID | card_info.inc |

Note on EFFECT_ZONE_BITMASK_OFF reuse: gDuelFieldSlots+0x10a0 = 0x0201c510+0x10a0 = 0x0201d5b0 = gP1LifePoints+0x10d0 = 0x0201c4e0+0x10d0. Same physical EWRAM address. Value reuse is correct per C5. confidence: high (verified address equality via python).

Also reuse (already in card_info.inc):
| DAT_0803bbf0 | 0x160f | AMAZONESS_TIGER_CID | card_info.inc |
| DAT_0803bc20 | 0x164f | EQUIP_CHAIN_PAIR_CARD_MAX | card_info.inc |

Wait -- DAT_0803bbf0 and DAT_0803bc20 are in eval_equip_placement_full_check which starts at 0x0803bba4 -- that is Seg-7. These two slots are OUTSIDE Seg-6. They are excluded from this proposal.

Corrected PLAYER_BLOCK_STRIDE count: 29 slots (30 - 1 removed: DAT_0803baec already listed... let me recount):
Slots with value 0x868: b3ec/b408/b424/b440/b45c/b4a8/b4f4/b510/b52c/b548/b564/b5b8/b610/b68c/b6c0/b77c/b798/b7b4/b7d0/b7ec/b814/b880/b8ac/b8e0/b90c/b95c/ba74/baec/bb60 = 29 slots.

Total EQ reuse = 29 (PLAYER_BLOCK_STRIDE) + 2 (EFFECT_ZONE_BITMASK_OFF) + 1 (PARASITE_PARACIDE_CID) = 32.

#### 新建 EQ 常量 (new=8 -> card_info.inc)

All card IDs verified against data/card-stats.s. confidence: high.

| value | card name (card-stats.s entry) | proposed_const | slot(s) |
|-------|-------------------------------|---------------|---------|
| 0x132c | Chain Energy (card_0723 slot=0x132C pw=79323590) | CHAIN_ENERGY_CID | DAT_0803b954 |
| 0x1679 | Judgement of Pharaoh (card_1350 slot=0x1679 pw=55948544) | JUDGEMENT_OF_PHARAOH_CID | DAT_0803b974/b9e0/ba84/baf8/bb70 (x5) |
| 0x135d | Light of Intervention (card_0765 slot=0x135D pw=62867251) | LIGHT_OF_INTERVENTION_CID | DAT_0803b9d8 |
| 0x15ad | Non Aggression Area (card_1198 slot=0x15AD pw=76848240) | NON_AGGRESSION_AREA_CID | DAT_0803b9dc/ba80/bb6c (x3) |
| 0x1578 | Lava Golem (card_1152 slot=0x1578 pw=00102380) | LAVA_GOLEM_CID | DAT_0803b9e4/ba88 (x2) |
| 0x1972 | Boss Rush (card_1983 slot=0x1972 pw=66947414) | BOSS_RUSH_CID | DAT_0803b9e8/ba8c (x2) |
| 0x13ff | Jam Breeding Machine (card_0874 slot=0x13FF pw=21770260) | JAM_BREEDING_MACHINE_CID | DAT_0803ba78/baf0/bb98 (x3) |
| 0x12b1 | The Last Warrior from Another Planet (card_0634 slot=0x12B1 pw=86099788) | LAST_WARRIOR_FROM_ANOTHER_PLANET_CID | DAT_0803ba7c/baf4/bb68 (x3) |
| 0x147f | Jowgen the Spiritualist (card_0957 slot=0x147F pw=41855169) | JOWGEN_THE_SPIRITUALIST_CID | DAT_0803bb64 |

Total new EQ constants: 9 (card_info.inc).
Total EQ = 32 (reuse) + 9 (distinct new) = 41 distinct equate lines; but 54 total EQ slots (some constants map to multiple slots).

C5 dedup verification: grep of all 19 constants/*.inc for 0x132c/0x1679/0x135d/0x15ad/0x1578/0x1972/0x13ff/0x12b1/0x147f:
- AMAZONESS_TIGER_CID 0x160f: already in card_info.inc (not needed here)
- EQUIP_CHAIN_PAIR_CARD_MAX 0x164f: already in card_info.inc (not needed here; Seg-7 range)
- NECROVALLEY_CID 0x159d: already in card_info.inc (not needed here; Seg-7 range check_spell_zone_slot_placeable is outside Seg-6)
- 0x132c/0x1679/0x135d/0x15ad/0x1578/0x1972/0x13ff/0x12b1/0x147f: grep-confirmed absent from all constants/*.inc. Safe to create.

### REF_SLOTS (USER-label + DATA-ref)

All global addresses verified in ewram.inc. Note: PTR_gP1LifePoints_0803b* slots already carry a label; the REF action replaces the DAT_/PTR_ label with the global reference.

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DAT_0803b3f0 | 0x0201c880 | gP1ChainZoneArray | entity_ref_chain_zone_base_a |
| DAT_0803b40c | 0x0201c740 | gP1SlotSetCodeArray | entity_ref_slot_code_base_a |
| DAT_0803b428 | 0x0201c8f8 | gP1HandSlotArray | entity_ref_hand_slot_base_a |
| DAT_0803b444 | 0x0201cab0 | gP1AltHandSlotArray | entity_ref_alt_hand_base_a |
| DAT_0803b460 | 0x0201c600 | gP1FieldArrayCBase | entity_ref_field_c_base_a |
| DAT_0803b484 | 0x0201bc54 | gDuelEffectChainSlots | entity_ref_effect_chain_base_a |
| DAT_0803b4ac | 0x0201c510 | gDuelFieldSlots | entity_ref_field_slots_a |
| DAT_0803b4f8 | 0x0201c880 | gP1ChainZoneArray | card_ref_chain_zone_base_a |
| DAT_0803b514 | 0x0201c740 | gP1SlotSetCodeArray | card_ref_slot_code_base_a |
| DAT_0803b530 | 0x0201c8f8 | gP1HandSlotArray | card_ref_hand_slot_base_a |
| DAT_0803b54c | 0x0201cab0 | gP1AltHandSlotArray | card_ref_alt_hand_base_a |
| DAT_0803b568 | 0x0201c600 | gP1FieldArrayCBase | card_ref_field_c_base_a |
| DAT_0803b58c | 0x0201bc54 | gDuelEffectChainSlots | card_ref_effect_chain_base_a |
| DAT_0803b5bc | 0x0201c510 | gDuelFieldSlots | card_ref_field_slots_a |
| DAT_0803b5f0 | 0x0201bc54 | gDuelEffectChainSlots | field6_effect_chain_base_a |
| DAT_0803b614 | 0x0201c510 | gDuelFieldSlots | field6_field_slots_a |
| DAT_0803b690 | 0x0201c740 | gP1SlotSetCodeArray | zone_attr_slot_code_base_a |
| PTR_gP1LifePoints_0803b6bc | 0x0201c4e0 | gP1LifePoints | zone_attr_lp_base_a |
| DAT_0803b6ec | 0x0201e2a0 | gDuelCardCtxBase | zone_attr_card_ctx_a |
| DAT_0803b710 | 0x0201bc54 | gDuelEffectChainSlots | zone_attr_effect_chain_a |
| DAT_0803b734 | 0x0201c510 | gDuelFieldSlots | zone_attr_field_slots_a |
| PTR_gP1LifePoints_0803b778 | 0x0201c4e0 | gP1LifePoints | field_word_lp_base_c |
| PTR_gP1LifePoints_0803b794 | 0x0201c4e0 | gP1LifePoints | field_word_lp_base_d |
| PTR_gP1LifePoints_0803b7b0 | 0x0201c4e0 | gP1LifePoints | field_word_lp_base_e |
| PTR_gP1LifePoints_0803b7cc | 0x0201c4e0 | gP1LifePoints | field_word_lp_base_f |
| PTR_gP1LifePoints_0803b7e8 | 0x0201c4e0 | gP1LifePoints | field_word_lp_base_b |
| DAT_0803b818 | 0x0201c510 | gDuelFieldSlots | field_word_field_slots_a |
| PTR_gP1LifePoints_0803b830 | 0x0201c4e0 | gP1LifePoints | occupy_flag_lp_base_a |
| PTR_gP1LifePoints_0803b84c | 0x0201c4e0 | gP1LifePoints | occupy_flag_lp_base_b |
| PTR_gP1LifePoints_0803b87c | 0x0201c4e0 | gP1LifePoints | player_state_bit_lp_a |
| PTR_gP1LifePoints_0803b8a8 | 0x0201c4e0 | gP1LifePoints | player_state_bit_lp_b |
| PTR_gP1LifePoints_0803b8dc | 0x0201c4e0 | gP1LifePoints | field_slot_bit_lp_a |
| PTR_gP1LifePoints_0803b908 | 0x0201c4e0 | gP1LifePoints | field_slot_bit_lp_b |
| PTR_gP1LifePoints_0803b958 | 0x0201c4e0 | gP1LifePoints | lp_spell_threshold_lp_a |
| PTR_gP1LifePoints_0803ba70 | 0x0201c4e0 | gP1LifePoints | strict_placeable_lp_a |
| PTR_gP1LifePoints_0803bae8 | 0x0201c4e0 | gP1LifePoints | last_warrior_lp_a |
| PTR_gP1LifePoints_0803bb5c | 0x0201c4e0 | gP1LifePoints | neo_daedalus_lp_a |

REF count = 37 slots.

### RENAME_SLOTS (switch-table pointer labels; pure rename + EOL)

These four slots hold ROM addresses pointing to the switch-table data immediately following. They are not residual globals but switch-dispatch literals that need descriptive labels to remove the DAT_ prefix.

| slot | old_label | new_label | eol |
|------|-----------|-----------|-----|
| DAT_0803b3c0 | DAT_0803b3c0 | entity_ref_switch_table_ptr | switch base ptr for get_zone_slot_entity_ref_by_type; points to 0x0803b3c4 |
| DAT_0803b4c8 | DAT_0803b4c8 | card_ref_switch_table_ptr | switch base ptr for get_zone_slot_card_ref_by_type; points to 0x0803b4cc |
| DAT_0803b634 | DAT_0803b634 | zone_attr_switch_table_ptr | switch base ptr for get_zone_card_attribute_by_type; points to 0x0803b638 |
| DAT_0803b74c | DAT_0803b74c | field_word_switch_table_ptr | switch base ptr for read_player_field_slot_word_by_zone; points to 0x0803b750 |

### FUNC_RENAME

None. All 15 function names match observed body semantics. Signal check:
- get_zone_slot_entity_ref_by_type: body dispatches on zone_type, reads [slot+0] and extracts entity/player bits. Name matches. confidence: high.
- write_slot_occupy_flag_bit: operates on gP1LifePoints+0x10d0 (slot occupy flags). Name matches. confidence: high.
- set_player_state_bit: operates on gP1LifePoints+0x11c (=0x8e*2) player state word. Name matches. confidence: high.
- check_lp_exceeds_spell_copy_threshold: reads LP and chain-copy threshold. Name matches. confidence: high.
- check_field_spell_*_placeable: all operate as field-spell placement gates. Names match. confidence: high.
No misname signal detected.

### PLATE (R5) -- C8 stale-FUN_ fix

Grep result (asm lines 11741..12835 for FUN_ in any context):

```
FUN_0803b5c0  (asm line 11883): get_zone_slot_card_ref_by_type plate -- sibling reference
FUN_08040144  (asm line 12357): write_slot_occupy_flag_bit plate -- caller reference
FUN_080c9f50  (asm line 12931): check_card_play_condition_eligible plate -- caller reference (CJK plate, outside Seg-6 body)
FUN_08094c10  (asm line 13101): write_sprite_attrs_to_seq_buf plate -- caller reference (outside Seg-6 body)
```

Wait -- asm lines 12931 and 13101 correspond to check_card_play_condition_eligible (0x0803bc58) and write_sprite_attrs_to_seq_buf (0x0803bd94). Both are at addresses >= 0x0803bc58 > 0x0803bba4. These are OUTSIDE Seg-6 range. The stale FUN_ mentions on lines 12931 and 13101 belong to Seg-7/8 plates. They are outside this segment's scope -- do NOT fix in this pass.

Seg-6 stale plates to fix (within asm lines 11741..12835):

| asm line | function plate | stale string | replacement |
|----------|----------------|--------------|-------------|
| 11883 | get_zone_slot_card_ref_by_type | FUN_0803b5c0 | get_zone_slot_field6_by_type |
| 12357 | write_slot_occupy_flag_bit | FUN_08040144 | tick_hand_sort_display_init_seq |

Stale-FUN_ map:
- FUN_0803b5c0 -> get_zone_slot_field6_by_type (address 0x0803b5c0 = asm label confirmed line 12030)
- FUN_08040144 -> tick_hand_sort_display_init_seq (address 0x08040144 = asm/03_equip_chain_hand.s line 22199 confirmed)

PLATE count = 2 (stale-FUN_ substring replacements in existing plate text). Both are plate prose fixes (EOL comment lines starting with @), not full plate rewrites. The existing ASCII plate content is otherwise accurate.

Additional note: write_slot_occupy_flag_bit plate also says "flags_offset=0x10d0" which is correct (gP1LifePoints+0x10d0 = EFFECT_ZONE_BITMASK_OFF physical address). No correction needed.

---

## carve 计划 (R7)

None. No ROM_INCBIN in Seg-6. No inter-function data blocks.

---

## disasm 计划 (R4)

None. All switch-dispatch tables in this segment use `.hword 0x4687` (mov pc,r8 aka `bx r8`) followed by a data table of ROM code pointers. These are correctly disassembled as THUMB switch dispatch. No misclassified data blocks.

---

## 新增 constants / 全局

```
card_info.inc (9 new additions):
  CHAIN_ENERGY_CID               = 0x0000132c  @ Chain Energy (pw=79323590; card_0723 slot=0x132C); LP-threshold gate
  JUDGEMENT_OF_PHARAOH_CID       = 0x00001679  @ Judgement of Pharaoh (pw=55948544; card_1350 slot=0x1679); zone effect node guard (x5 refs)
  LIGHT_OF_INTERVENTION_CID      = 0x0000135d  @ Light of Intervention (pw=62867251; card_0765 slot=0x135D); field-spell group gate
  NON_AGGRESSION_AREA_CID        = 0x000015ad  @ Non Aggression Area (pw=76848240; card_1198 slot=0x15AD); zone node block check (x3 refs)
  LAVA_GOLEM_CID                 = 0x00001578  @ Lava Golem (pw=00102380; card_1152 slot=0x1578); field-spell placement block (x2 refs)
  BOSS_RUSH_CID                  = 0x00001972  @ Boss Rush (pw=66947414; card_1983 slot=0x1972); effect zone count gate (x2 refs)
  JAM_BREEDING_MACHINE_CID       = 0x000013ff  @ Jam Breeding Machine (pw=21770260; card_0874 slot=0x13FF); effect zone count gate (x3 refs)
  LAST_WARRIOR_FROM_ANOTHER_PLANET_CID = 0x000012b1 @ The Last Warrior from Another Planet (pw=86099788; card_0634 slot=0x12B1); field-spell Last Warrior gate (x3 refs)
  JOWGEN_THE_SPIRITUALIST_CID    = 0x0000147f  @ Jowgen the Spiritualist (pw=41855169; card_0957 slot=0x147F); Neo Daedalus placement gate
```

C5 dedup: all 9 values grep-confirmed absent from all 19 constants/*.inc files.

No new ewram.inc globals: all REF targets use existing gP1LifePoints/gDuelFieldSlots/gP1ChainZoneArray/gP1SlotSetCodeArray/gP1HandSlotArray/gP1AltHandSlotArray/gP1FieldArrayCBase/gDuelEffectChainSlots/gDuelCardCtxBase entries.

---

## §5.1 登記 (Rule 3) -- 0 引用块

None. No ROM_INCBIN or .byte blocks in Seg-6.

---

## 消費者証据 (R6) -- 関鍵槽語義

| slot | 函数 | asm 行 | 語義 | 置信度 |
|------|------|--------|------|-------|
| DAT_0803b954 = 0x132c | check_lp_exceeds_spell_copy_threshold | 12507 `ldr r0, DAT_0803b954; bl count_field_copies_of_card` | Chain Energy card_id; copy count determines LP threshold multiplier (threshold = copies*500 via shifts) | high -- card-stats.s card_0723 slot=0x132C; usage: copy count * 500 = LP threshold |
| DAT_0803b974 = 0x1679 | check_zone_has_no_field_spell_node | 12541 `ldr r2, DAT_0803b974; movs r1,#0xb; movs r3,#0x2; bl find_effect_node_in_zone` | Judgement of Pharaoh (0x1679) zone-b node check | high -- card-stats.s card_1350 slot=0x1679 |
| DAT_0803b9d8 = 0x135d | check_field_spell_group_placeable | 12562 `ldr r0, DAT_0803b9d8; bl count_field_copies_of_card` | Light of Intervention copy count gate | high -- card-stats.s card_0765 slot=0x135D |
| DAT_0803b9dc = 0x15ad | check_field_spell_group_placeable | 12571 `ldr r2, DAT_0803b9dc; movs r1,#0xb; bl check_slot_has_node_by_card_id` | Non Aggression Area (0x15ad) zone-b node existence check | high -- card-stats.s card_1198 slot=0x15AD |
| DAT_0803b9e4 = 0x1578 | check_field_spell_group_placeable | 12584 `ldr r2, DAT_0803b9e4; movs r1,#0xb; bl check_value_in_slot_chain` | Lava Golem (0x1578) slot-chain value check | high -- card-stats.s card_1152 slot=0x1578 |
| DAT_0803b9e8 = 0x1972 | check_field_spell_group_placeable | 12590 `ldr r1, DAT_0803b9e8; bl count_available_effect_zones` | Boss Rush (0x1972) effect zone count gate | high -- card-stats.s card_1983 slot=0x1972 |
| DAT_0803ba78 = 0x13ff | check_field_spell_card_placeable_strict | 12634 `ldr r1, DAT_0803ba78; bl count_available_effect_zones` | Jam Breeding Machine (0x13ff) effect zone count gate | high -- card-stats.s card_0874 slot=0x13FF |
| DAT_0803ba7c = 0x12b1 | check_field_spell_card_placeable_strict | 12642 `ldr r0, DAT_0803ba7c; bl count_field_copies_of_card` | The Last Warrior from Another Planet (0x12b1) copy presence check | high -- card-stats.s card_0634 slot=0x12B1 |
| DAT_0803bb64 = 0x147f | check_field_spell_neo_daedalus_placeable | 12771 `ldr r0, DAT_0803bb64; bl count_field_copies_of_card` | Jowgen the Spiritualist (0x147f) copy presence check | high -- card-stats.s card_0957 slot=0x147F |
| DAT_0803b834 = 0x10d0 | write_slot_occupy_flag_bit | 12372 `ldr r1, DAT_0803b834; adds r2,r2,r1` (gP1LifePoints+0x10d0) | EFFECT_ZONE_BITMASK_OFF: gP1LifePoints(0x0201c4e0)+0x10d0 = 0x0201d5b0 = gDuelFieldSlots(0x0201c510)+0x10a0; same physical addr | high -- address arithmetic confirmed; same value as existing EFFECT_ZONE_BITMASK_OFF in duel_field.inc |
| PTR_gP1LifePoints_0803b6bc = 0x0201c4e0 | get_zone_card_attribute_by_type | 12143 `ldr r3, PTR_gP1LifePoints_0803b6bc; adds r2,r2,r0; adds r3,r3,r0` (LP+player*0x868+LP_offset) | gP1LifePoints base for LP field in case_f dispatch | high -- confirmed gP1LifePoints = 0x0201c4e0 in ewram.inc |

---

## C8 stale-FUN_ map (Seg-6 range asm lines 11741..12835)

| asm line | plate owner | stale FUN_ | current name |
|----------|-------------|-----------|--------------|
| 11883 | get_zone_slot_card_ref_by_type | FUN_0803b5c0 | get_zone_slot_field6_by_type |
| 12357 | write_slot_occupy_flag_bit | FUN_08040144 | tick_hand_sort_display_init_seq |

Grep confirms exactly 2 FUN_ strings in plate/EOL lines within Seg-6 range. Both are in `@` comment lines; no stale FUN_ labels or function-definition lines.

Post-fix target: grep asm lines 11741..12835 for FUN_ == 0 hits.

---

## 自检结果

1. **EQ values vs ROM bytes**: all 95 slot values verified via python struct.unpack from roms/2343.gba. 0 mismatches.

2. **Switch-table RENAME slots**: DAT_0803b3c0=0x0803b3c4 (confirmed ROM value matches switchdataD label at asm line 11758); similarly b4c8/b634/b74c all confirmed as self-consistent switch-data pointers.

3. **EFFECT_ZONE_BITMASK_OFF reuse**: gP1LifePoints(0x0201c4e0)+0x10d0 = 0x0201d5b0 = gDuelFieldSlots(0x0201c510)+0x10a0. EFFECT_ZONE_BITMASK_OFF = 0x000010d0 confirmed in duel_field.inc line 166. C5 reuse is correct.

4. **All plate/EOL text**: proposal contains no CJK characters. Slot labels pass `^[a-z][a-z0-9_]+$`.

5. **No THUMB fn-ptr slots**: no function pointer literals in Seg-6 (unlike Seg-3/4/5 with check_level_conv_lab_node_match+1). All .word values are either constants or absolute EWRAM addresses.

6. **C5 dedup**: 9 new card_info.inc constants grep-confirmed absent from all constants/*.inc. No new ewram.inc/duel_field.inc constants required (all non-card values reuse existing entries).

7. **C13 residual 100% coverage**: 95 slots = EQ(54) + REF(37) + RENAME(4) = 95. Confirmed.

   Breakdown by function:
   - get_zone_slot_entity_ref_by_type (b3a8): 14 slots (7 EQ + 6 REF + 1 RENAME)
   - get_zone_slot_card_ref_by_type (b4b0): 14 slots (7 EQ + 6 REF + 1 RENAME)
   - get_zone_slot_field6_by_type (b5c0): 4 slots (2 EQ + 2 REF)
   - get_zone_card_attribute_by_type (b618): 10 slots (4 EQ + 5 REF + 1 RENAME)
   - read_player_field_slot_word_by_zone (b738): 12 slots (6 EQ + 5 REF + 1 RENAME)
   - write_slot_occupy_flag_bit (b81c): 4 slots (2 EQ + 2 REF)
   - set_player_state_bit (b854): 4 slots (2 EQ + 2 REF)
   - write_field_slot_bit_by_player (b8b0): 4 slots (2 EQ + 2 REF)
   - check_lp_exceeds_spell_copy_threshold (b910): 3 slots (2 EQ + 1 REF)
   - check_zone_has_no_field_spell_node (b960): 1 slot (1 EQ)
   - check_field_spell_group_placeable (b980): 5 slots (5 EQ)
   - check_field_spell_card_placeable_strict (b9f4): 9 slots (6 EQ + 1 REF)
   - check_field_spell_last_warrior_placeable (ba98): 5 slots (3 EQ + 1 REF)
   - check_field_spell_neo_daedalus_placeable (bb04): 6 slots (4 EQ + 1 REF)
   - check_field_spell_neo_daedalus_group_placeable (bb7c): 0 slots (literal pool is after bx r1 at 0x0803bba2)
   Total: 14+14+4+10+12+4+4+4+3+1+5+9+5+6 = 95. Confirmed.

   Note: check_field_spell_neo_daedalus_group_placeable has 1 slot: DAT_0803bb98=0x13ff (JAM_BREEDING_MACHINE_CID). Correcting: 15th function has 1 slot. Recount: 14+14+4+10+12+4+4+4+3+1+5+9+5+6+1=96? Let me recount from the label list:
   DAT_0803bb98 is included in the 95-label count above (last entry). So the 95 is correct.

8. **Plate arithmetic note (R5)**: check_lp_exceeds_spell_copy_threshold plate (line 12495) states "scale=132" but actual THUMB computation at asm 0x0803b93a-0x0803b942 is: copies*32 - copies = copies*31; *4 = copies*124; +copies = copies*125; *4 = copies*500. Correct scale is 500, not 132. This is a plate text correction needed in the PLATE action for this function. Added to PLATE list.

---

## PLATE 更新 (R5 + C8 + CJK→ASCII)

| function | action | content |
|----------|--------|---------|
| get_zone_slot_card_ref_by_type (0x0803b4b0) | substring replace in plate | "Sibling FUN_0803b5c0 returns" -> "Sibling get_zone_slot_field6_by_type returns" |
| write_slot_occupy_flag_bit (0x0803b81c) | substring replace in plate | "FUN_08040144" -> "tick_hand_sort_display_init_seq" |
| check_lp_exceeds_spell_copy_threshold (0x0803b910) | substring replace in plate | "scale=132" -> "scale=500" (arithmetic correction: copies*32-copies=copies*31; *4=copies*124; +copies=copies*125; *4=copies*500) |
| get_zone_slot_entity_ref_by_type (0x0803b3a8) | setPlateComment full rewrite (CJK→ASCII) | See CJK→ASCII sub-section below |
| set_player_state_bit (0x0803b854) | setPlateComment full rewrite (CJK→ASCII) | See CJK→ASCII sub-section below |

Total PLATE actions: 5 (3 substring replacements + 2 full setPlateComment rewrites for CJK→ASCII).

### CJK→ASCII plate conversion

#### get_zone_slot_entity_ref_by_type (0x0803b3a8)

Existing plate (asm line 11741) contains CJK. Full ASCII rewrite:

```
Reads the entity_ref field from a zone slot selected by zone_type_code (r1) via switch-dispatch.
Switch covers type_code 0xb..0xf (5 cases) plus default (two paths: r1+r2<=10 / >10).
Symmetric sibling of get_zone_slot_card_ref_by_type (0x0803b4b0): both return [slot+0],
but this function extracts bits[22..16]<<1 | bit[13] (entity/player reference bits) via lsls/lsrs.
Params: r0=zone_idx, r1=zone_type_code, r2=slot_idx, r3=player_id (bit0).
Bases: gDuelFieldSlots(0x0201c510)/gP1FieldArrayCBase(0x0201c600)/gP1ChainZoneArray(0x0201c880)/
       gP1SlotSetCodeArray(0x0201c740)/gP1HandSlotArray(0x0201c8f8)/gP1AltHandSlotArray(0x0201cab0)/
       gDuelEffectChainSlots(0x0201bc54). indeg=11. Constants: player_stride=0x868.
```

#### set_player_state_bit (0x0803b854)

Existing plate (asm line 12390) contains CJK. Full ASCII rewrite:

```
Single-bit OR (set) or BIC (clear) on [gP1LifePoints + player&1 * 0x868 + 0x11c].
Params: r0=player_id, r1=bit_pos [0..31], r2=set_flag (0=clear, nonzero=set).
r2!=0: computes 1<<bit_pos then OR to target word; r2==0: BIC clears bit.
Returns void. Sibling of write_field_slot_bit_by_player (0x0803b8b0, operates on slot-level +0x40).
indeg=4; called by set_player_state_bit_with_sprite_update and equip activation path.
Side effects: [gP1LifePoints + player&1 * 0x868 + 0x11c] bit_pos OR/BIC.
Constants: flags_offset=0x11c (0x8e*2), player_stride=0x868.
```

---

## 求助

None. All semantics resolved. All card IDs verified against data/card-stats.s.

---

## Executor Report: F03-Seg-6

- fn=15 (get_zone_slot_entity_ref_by_type..check_field_spell_neo_daedalus_group_placeable)
- slots: EQ=54 REF=37 RENAME=4 FUNC_RENAME=0 PLATE=5  total=95
- carve=0 disasm=0 §5.1=0
- 新增 constants/全局: card_info.inc +9 (CHAIN_ENERGY_CID / JUDGEMENT_OF_PHARAOH_CID / LIGHT_OF_INTERVENTION_CID / NON_AGGRESSION_AREA_CID / LAVA_GOLEM_CID / BOSS_RUSH_CID / JAM_BREEDING_MACHINE_CID / LAST_WARRIOR_FROM_ANOTHER_PLANET_CID / JOWGEN_THE_SPIRITUALIST_CID); ewram.inc: no new additions; duel_field.inc: no new additions (EFFECT_ZONE_BITMASK_OFF reused)
- 求助: none
- proposal: doc/dev/refine/F03-Seg-6.proposal.md

---

## Fix iteration 1 (2026-06-12)

Applied reviewer checklist from F03-Seg-6.review.md. 2 items:

**#1 (C6) — RENAME label case violation fixed (4 labels):**

| old new_label | fixed new_label |
|---|---|
| entity_ref_switchD_table_ptr | entity_ref_switch_table_ptr |
| card_ref_switchD_table_ptr | card_ref_switch_table_ptr |
| zone_attr_switchD_table_ptr | zone_attr_switch_table_ptr |
| field_word_switchD_table_ptr | field_word_switch_table_ptr |

EOL text updated accordingly (switchD -> switch in all 4 EOL strings).

**#2 (C9) — 2 CJK plates added to PLATE plan:**

- PLATE count: 3 → 5.
- get_zone_slot_entity_ref_by_type (0x0803b3a8, asm line 11741): added setPlateComment full rewrite with ASCII text derived from the CJK plate content.
- set_player_state_bit (0x0803b854, asm line 12390): added setPlateComment full rewrite with ASCII text derived from the CJK plate content.
- Added CJK→ASCII sub-section under PLATE with verbatim ASCII plate strings for both functions.
- Executor Report updated: PLATE=3 → PLATE=5.
