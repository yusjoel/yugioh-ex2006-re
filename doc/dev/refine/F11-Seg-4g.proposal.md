# Refine Proposal: F11-Seg-4g  [0x0808cabc..0x0808d7f4)

## Segment Survey

- ROM range: `[0x0808cabc, 0x0808d7f4)` = 0xD38 bytes (3384 B)
- Source: one-liner `ROM_INCBIN 0x8cabc, 0xd38` at asm/11_effect_slot_puzzletext.s line 16402
- Boundary at 0x0808cabc = first entry after Seg-4f end (CID 0x193a Divine Sword - Phoenix Blade); boundary at 0x0808d7f4 = dispatch table terminator fn_ptr (CID 0xffff sentinel entry)
- Functions: **20 real functions** (24 strong entries - 3 degenerate - 1 weak = 20 real)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools
- **This is the LAST sub-segment of the giant block [0x08087d58, 0x0808d7f4). Landing eliminates the sole remaining ROM_INCBIN in the Seg-4 block.**

### Function type: equip zone scan callbacks (same pattern as Seg-4a/4b/4c/4d/4e/4f)

All 20 real functions are equip zone scan callbacks dispatched from the 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305+1 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

---

## Degenerate Strong Entry Analysis (3 of 24)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808d20e | Mid-body of fn12 (0x0808d1bc..0x0808d224). The 4 bytes at 0x0808d20e are 4285 = CMP r2,r1 inside fn12 loop body. fn12 has a contiguous body from prologue (b5f0) at 0x0808d1bc through epilogue (bc01/4700) at 0x0808d21e..0x0808d222. 0x0808d20e falls at offset +0x52 inside fn12. Confirmed: 0x0808d1bc <= 0x0808d20e < 0x0808d224. | ROM bytes @0x0808d20e: 4285 (CMP r2,r1); fn12 prologue at 0x0808d1bc: f0b5; dispatch table has no entry with fn_ptr = 0x0808d20f |
| 0x0808d21e | Upper half of pool word `gP1LifePoints=0x0201c4e0` at pool slot 0x0808d21c inside fn12. Word @0x0808d21c = 0x0201c4e0; upper halfword @0x0808d21e = 0x0201. This is a literal pool slot, not a function entry. | ROM word @0x0808d21c: 0x0201c4e0 (= gP1LifePoints); half @0x0808d21e: 0x0201; fn12 pool confirmed by LDR r6,[PC,...] at 0x0808d1c4 -> pool@0x0808d21c; dispatch table has no entry fn_ptr=0x0808d21f |
| 0x0808d7de | Alignment pad byte within pool of fn20 (0x0808d704..0x0808d7f4). Word @0x0808d7dc = 0x00001fff (SLOT_CARD_SET_CODE_MASK, accessed by LDR r2 at 0x0808d7a4 -> pool@0x0808d7dc). The upper halfword 0x0000 at 0x0808d7de is the high half of that pool word, not a function. | ROM word @0x0808d7dc: 0x00001fff; half @0x0808d7de: 0x0000; dispatch table terminator entry CID=0xffff at ROM after fn20 end; no dispatch entry fn_ptr=0x0808d7df |

### Weak Entry Analysis (1 flagged)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808d58c | Mid-body instruction inside fn17 (0x0808d494..0x0808d5b0). ROM bytes @0x0808d58c = 0x4281 = CMP r1,r0 (falls inside fn17 body at offset +0xf8). fn17 has contiguous prologue (b5f0) at 0x0808d494. | ROM half @0x0808d58c: 0x4281 (CMP r1,r0); fn17 range [0x0808d494..0x0808d5b0) confirmed; dispatch table has no entry fn_ptr=0x0808d58d |

---

## Dispatch Table CID Scan (all seg-4g entries, table at 0x09e5a128, 305+1 entries)

| fn  | addr       | CID(s)          | card name(s)                                    |
|-----|------------|-----------------|-------------------------------------------------|
| fn01 | 0x0808cabc | 0x1944          | Level Modulation                                |
| fn02 | 0x0808cb54 | 0x1951          | Water Dragon                                    |
| fn03 | 0x0808cbd4 | 0x196a (NEW)    | Scarr, Scout of Dark World                      |
| fn04 | 0x0808cc5c | 0x196f          | Pot of Avarice                                  |
| fn05 | 0x0808ccb4 | 0x1972          | Boss Rush                                       |
| fn06 | 0x0808cd34 | 0x1973 (NEW)    | Gateway to Dark World                           |
| fn07 | 0x0808cdc0 | 0x1974          | Forces of Darkness                              |
| fn08 | 0x0808ce3c | 0x1979          | Roll Out!                                       |
| fn09 | 0x0808cf88 | 0x197c (NEW)    | Armed Changer                                   |
| fn10 | 0x0808d054 | 0x198d          | Magical Mallet                                  |
| fn11 | 0x0808d060 | 0x198e          | Inferno Reckless Summon                         |
| fn12 | 0x0808d1bc | 0x1996          | White Horns Dragon                              |
| fn13 | 0x0808d224 | 0x19ac          | Magnet Circle LV2                               |
| fn14 | 0x0808d294 | 0x19ae          | Ancient Gear Drill                              |
| fn15 | 0x0808d324 | 0x19b6          | Damage Condenser                                |
| fn16 | 0x0808d3d8 | 0x19c5          | Gokipon                                         |
| fn17 | 0x0808d494 | 0x19d7          | Symbol of Heritage                              |
| fn18 | 0x0808d5b0 | 0x19dc+0x19dd (multi) | Next to be Lost + Generation Shift        |
| fn19 | 0x0808d694 | 0x19ec          | Flute of Summoning Kuriboh                      |
| fn20 | 0x0808d704 | 0xfffe (sentinel) | multi-card group handler (last real entry)    |

Note: 0x0808d20e, 0x0808d21e, and 0x0808d7de are NOT in the dispatch table (confirmed); they are degenerate
mid-body/mid-pool bytes inside fn12 and fn20 respectively.

Size check: fn01..fn20 sizes:
0x98+0x80+0x88+0x58+0x80+0x8c+0x7c+0x14c+0xcc+0x0c+0x15c+0x68+0x70+0x90+0xb4+0xbc+0x11c+0xe4+0x70+0xf0
= 0xd38 = 3384 B. Confirmed.

---

## Function Naming Table (20 real functions)

Substate semantics (from plate at write_equip_zone_entry_by_substate):
- 0xb = field-spell zone type B
- 0xc = chain zone type C
- 0xd = monster zone type D
- 0xe = hand slot type E

Substate rule: value is the `N` in `MOVS r1,#N` at offset -4 from the `BL write_equip_zone_entry_by_substate` instruction.

### fn01: 0x0808cabc  size=0x098 (152 B)
- CID: 0x1944 (Level Modulation), dispatch entry [CID 0x1944]
- Body: push {r4-r7,lr}+push {r8}; hand loop via gP1LifePoints+gP1HandCountBase+gP1HandSlotArray; gate: check_equip_placement_eligible_from_slot_record (0x080313b8) + check_card_id_is_effect_monster_type_b (0x0804b0e4); write substate_e
- BL targets: 0x080313b8, 0x0804b0e4, 0x0808d88c
- Pool: @0x0808cb48=0x0201c4e0 (gP1LifePoints), @0x0808cb4c=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808cb50=0x0201c4f4 (gP1HandCountBase)
- CID status: LEVEL_MODULATION_CID(0x1944) REUSE (card_info.inc line found)
- Substate: 0xe (MOVS r1,#0xe at 0x0808cb20, BL at 0x0808cb24)
- Proposed name: `scan_zone_level_modulation_substate_e`
- Confidence: high (hand loop, effect-monster gate; Level Modulation changes monster level, write_e = hand slot)
- ASCII plate (len=347): `Equip zone scan for Level Modulation (LEVEL_MODULATION_CID=0x1944). Hand loop via gP1LifePoints+gP1HandCountBase+gP1HandSlotArray; gate: check_equip_placement_eligible_from_slot_record (0x080313b8)+check_card_id_is_effect_monster_type_b (0x0804b0e4). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1944].`
- CSV row: `0x0808cabc,scan_zone_level_modulation_substate_e`

### fn02: 0x0808cb54  size=0x080 (128 B)
- CID: 0x1951 (Water Dragon), dispatch entry [CID 0x1951]
- Body: push {r4-r7,lr}+push {r8}; hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ab4c (check_card_pair_allowed), 0x08037434 (check_zone_slot_equip_eligible), 0x0808d88c
- Pool: @0x0808cbc8=0x0201c4e0 (gP1LifePoints), @0x0808cbcc=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808cbd0=0x0201c8f8 (gP1HandSlotArray)
- CID status: WATER_DRAGON_CID(0x1951) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808cba6, BL at 0x0808cbaa)
- Proposed name: `scan_zone_water_dragon_substate_e`
- Confidence: high (hand loop + zone_eligible gate; Water Dragon: equip to WATER monsters in hand)
- ASCII plate (len=273): `Equip zone scan for Water Dragon (WATER_DRAGON_CID=0x1951). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_zone_slot_equip_eligible (0x08037434). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1951].`
- CSV row: `0x0808cb54,scan_zone_water_dragon_substate_e`

### fn03: 0x0808cbd4  size=0x088 (136 B)
- CID: 0x196a (Scarr, Scout of Dark World), dispatch entry [CID 0x196a] -- NEW
- Body: push {r4-r7,lr}+push {r8}; SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c) + get_card_extended_stat_field5 (0x080eee50); write substate_d
- BL targets: 0x0804ad48 (check_card_field5_is_nonzero), 0x0804b26c (check_card_id_is_dark_world_range_type), 0x080eee50 (get_card_extended_stat_field5), 0x0808d88c
- Pool: @0x0808cc50=0x0201c4e0 (gP1LifePoints), @0x0808cc54=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808cc58=0x0201c740 (gP1SlotSetCodeArray)
- CID status: SCARR_DARK_WORLD_CID(0x196a) NEW (C5 grep: 0 hits in card_info.inc)
- Substate: 0xd (MOVS r1,#0xd at 0x0808cc2c, BL at 0x0808cc30)
- Proposed name: `scan_zone_scarr_dark_world_substate_d`
- Confidence: high (monster zone + dark_world_range_type gate; Scarr is a DARK Dark World; write_d = monster zone)
- ASCII plate (len=360): `Equip zone scan for Scarr, Scout of Dark World (SCARR_DARK_WORLD_CID=0x196a). SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c)+get_card_extended_stat_field5 (0x080eee50). write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x196a].`
- CSV row: `0x0808cbd4,scan_zone_scarr_dark_world_substate_d`

### fn04: 0x0808cc5c  size=0x058 (88 B)
- CID: 0x196f (Pot of Avarice), dispatch entry [CID 0x196f]
- Body: push {r4-r7,lr}; hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: check_equip_placement_eligible_from_slot_record (0x080313b8 via 0x0804ad48); write substate_e
- BL targets: 0x0804ad48 (check_card_field5_is_nonzero), 0x0808d88c
- Pool: @0x0808ccac=0x0201c4e0 (gP1LifePoints), @0x0808ccb0=0x00000868 (PLAYER_BLOCK_STRIDE)
- CID status: POT_OF_AVARICE_CID(0x196f) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808cc94, BL at 0x0808cc98)
- Proposed name: `scan_zone_pot_of_avarice_substate_e`
- Confidence: high (hand loop; Pot of Avarice shuffles 5 monsters from GY, write_e = hand)
- ASCII plate (len=277): `Equip zone scan for Pot of Avarice (POT_OF_AVARICE_CID=0x196f). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: check_equip_placement_eligible_from_slot_record (0x080313b8). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x196f].`
- CSV row: `0x0808cc5c,scan_zone_pot_of_avarice_substate_e`

### fn05: 0x0808ccb4  size=0x080 (128 B)
- CID: 0x1972 (Boss Rush), dispatch entry [CID 0x1972]
- Body: push {r4-r7,lr}+push {r8}; SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: check_card_id_is_bes_type (0x0804b2dc) + eval_equip_placement_full_check (0x0803bba4); write substate_d
- BL targets: 0x0804b2dc (check_card_id_is_bes_type), 0x0803bba4 (eval_equip_placement_full_check), 0x0808d88c
- Pool: @0x0808cd28=0x0201c4e0 (gP1LifePoints), @0x0808cd2c=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808cd30=0x0201c740 (gP1SlotSetCodeArray)
- CID status: BOSS_RUSH_CID(0x1972) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808cd06, BL at 0x0808cd0a)
- Proposed name: `scan_zone_boss_rush_substate_d`
- Confidence: high (BES-type gate + monster zone; Boss Rush equips to B.E.S. monsters)
- ASCII plate (len=325): `Equip zone scan for Boss Rush (BOSS_RUSH_CID=0x1972). SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: check_card_id_is_bes_type (0x0804b2dc)+eval_equip_placement_full_check (0x0803bba4). write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x1972].`
- CSV row: `0x0808ccb4,scan_zone_boss_rush_substate_d`

### fn06: 0x0808cd34  size=0x08c (140 B)
- CID: 0x1973 (Gateway to Dark World), dispatch entry [CID 0x1973] -- NEW
- Body: push {r4-r7,lr}+push {r8}; hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x0804b26c (check_card_id_is_dark_world_range_type), 0x08037434, 0x0808d88c
- Pool: @0x0808cdb4=0x0201c4e0 (gP1LifePoints), @0x0808cdb8=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808cdbc=0x0201c8f8 (gP1HandSlotArray)
- CID status: GATEWAY_DARK_WORLD_CID(0x1973) NEW (C5 grep: 0 hits in card_info.inc)
- Substate: 0xe (MOVS r1,#0xe at 0x0808cd90, BL at 0x0808cd94)
- Proposed name: `scan_zone_gateway_dark_world_substate_e`
- Confidence: high (hand loop + dark_world_range_type gate; Gateway to Dark World: continuous spell for Dark World monsters in hand)
- ASCII plate (len=340): `Equip zone scan for Gateway to Dark World (GATEWAY_DARK_WORLD_CID=0x1973). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c)+check_zone_slot_equip_eligible (0x08037434). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1973].`
- CSV row: `0x0808cd34,scan_zone_gateway_dark_world_substate_e`

### fn07: 0x0808cdc0  size=0x07c (124 B)
- CID: 0x1974 (Forces of Darkness), dispatch entry [CID 0x1974]
- Body: push {r4-r7,lr}+push {r8}; hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c); write substate_e
- BL targets: 0x0804ad48, 0x0804b26c, 0x0808d88c
- Pool: @0x0808ce30=0x0201c4e0 (gP1LifePoints), @0x0808ce34=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808ce38=0x0201c8f8 (gP1HandSlotArray)
- CID status: FORCES_OF_DARKNESS_CID(0x1974) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808ce0e, BL at 0x0808ce12)
- Proposed name: `scan_zone_forces_of_darkness_substate_e`
- Confidence: high (hand loop + dark_world gate; Forces of Darkness: add 2 DARK monsters from GY to hand, write_e = hand slot)
- ASCII plate (len=293): `Equip zone scan for Forces of Darkness (FORCES_OF_DARKNESS_CID=0x1974). Hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray; gate: check_card_id_is_dark_world_range_type (0x0804b26c). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1974].`
- CSV row: `0x0808cdc0,scan_zone_forces_of_darkness_substate_e`

### fn08: 0x0808ce3c  size=0x14c (332 B)
- CID: 0x1979 (Roll Out!), dispatch entry [CID 0x1979]
- Body: push {r4-r7,lr}+push {r8,r9}; two-phase: phase1 scans gDuelFieldSlots+PLAYER_BLOCK_STRIDE via memset (0x0810e9bc) + check_card_stat_field8_is_8 (0x0804ae2c) + check_slot_card_eligible_by_card_id (0x0804f6c4); phase2 hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray+slot_field_mask_ffff803f gate; write substate_e
- BL targets: 0x0810e9bc (memset), 0x0804ae2c (check_card_stat_field8_is_8), 0x0804f6c4 (check_slot_card_eligible_by_card_id), 0x0808d88c
- Pool (2 sections): @0x0808cea4=0x00000868, @0x0808cea8=0x0201c510 (gDuelFieldSlots); @0x0808cf24=0x0201c4e0, @0x0808cf28=0x00000868, @0x0808cf2c=0x0201c8f8 (gP1HandSlotArray), @0x0808cf30=0xffff803f (slot_field_mask_ffff803f), @0x0808cf80=0x00000868, @0x0808cf84=0x0201c4f4 (gP1HandCountBase)
- CID status: ROLL_OUT_CID(0x1979) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808cf54, BL at 0x0808cf58)
- Proposed name: `scan_zone_roll_out_substate_e`
- Confidence: high (two-phase scan with field-slot + hand; Roll Out! equips to union monsters in hand/field)
- ASCII plate (len=412): `Equip zone scan for Roll Out! (ROLL_OUT_CID=0x1979). Phase1: scan gDuelFieldSlots+PLAYER_BLOCK_STRIDE via memset (0x0810e9bc)+check_card_stat_field8_is_8 (0x0804ae2c)+check_slot_card_eligible_by_card_id (0x0804f6c4). Phase2: hand loop via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1HandSlotArray+slot_field_mask_ffff803f. write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1979].`
- CSV row: `0x0808ce3c,scan_zone_roll_out_substate_e`

### fn09: 0x0808cf88  size=0x0cc (204 B)
- CID: 0x197c (Armed Changer), dispatch entry [CID 0x197c] -- NEW
- Body: push {r4-r7,lr}+push {r8,r9}; two write calls: (1) hand via gP1HandSlotArray+check_card_field5_is_nonzero (0x0804ad48)+get_card_extended_stat_field3_raw (0x080eef44)+CARD_FIELD_STAT_CLEAR_UPPER4_MASK gate; write substate_e. (2) field via gP1FieldArrayCBase+get_card_extended_stat_field9 (0x080eee7c)+CMP r0,#3 gate; write substate_b
- BL targets: 0x0804ad48 (check_card_field5_is_nonzero), 0x080eef44 (get_card_extended_stat_field3_raw), 0x0808d88c (x2), 0x080eee7c (get_card_extended_stat_field9)
- Pool (2 sections): @0x0808d004=0x0201c4e0, @0x0808d008=0x00000868, @0x0808d00c=0x0fffffff (CARD_FIELD_STAT_CLEAR_UPPER4_MASK), @0x0808d010=0x0201c8f8 (gP1HandSlotArray); @0x0808d04c=0x00000868, @0x0808d050=0x0201c600 (gP1FieldArrayCBase)
- CID status: ARMED_CHANGER_CID(0x197c) NEW (C5 grep: 0 hits in card_info.inc; data/card-stats.s line 25924)
- Substate: 0xe first write (MOVS r1,#0xe at 0x0808cfea, BL at 0x0808cfee); 0xb second write (MOVS r1,#0xb at 0x0808d036, BL at 0x0808d03a)
- Proposed name: `scan_zone_armed_changer_substate_e_b`
- Confidence: high (two-zone: hand + field-spell; Armed Changer equips to monsters destroyed this turn -- body checks field3/field9 attributes)
- ASCII plate (len=395): `Equip zone scan for Armed Changer (ARMED_CHANGER_CID=0x197c). Two writes: (1) hand via gP1HandSlotArray+check_card_field5_is_nonzero (0x0804ad48)+get_card_extended_stat_field3_raw (0x080eef44)+CARD_FIELD_STAT_CLEAR_UPPER4_MASK gate; write substate_e. (2) field via gP1FieldArrayCBase+get_card_extended_stat_field9 (0x080eee7c)+CMP r0,#3 gate; write substate_b. Dispatch table entry [CID 0x197c].`
- CSV row: `0x0808cf88,scan_zone_armed_changer_substate_e_b`

### fn10: 0x0808d054  size=0x00c (12 B)
- CID: 0x198d (Magical Mallet), dispatch entry [CID 0x198d]
- Body: push {lr}; MOVS r1,#0xb; BL write_equip_zone_entry_by_substate (0x0808d88c); pop {r0}; bx r0
- BL targets: 0x0808d88c
- Pool: none
- CID status: MAGICAL_MALLET_CID(0x198d) REUSE (card_info.inc:842)
- Substate: 0xb (MOVS r1,#0xb at 0x0808d056, BL at 0x0808d058; confirmed)
- Proposed name: `scan_zone_magical_mallet_substate_b`
- Confidence: high (12B standalone dispatch handler; 1 ROM ref @0x9e5aa2c = dispatch table entry 288; writes substate=0xb (field zone B) for Magical Mallet)
- ASCII plate (len=208): `Equip zone scan for Magical Mallet (MAGICAL_MALLET_CID=0x198d). Stub: push{lr}; MOVS r1,#0xb; BL write_equip_zone_entry_by_substate (0x0808d88c); pop{r0};bx r0. write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x198d].`
- CSV row: `0x0808d054,scan_zone_magical_mallet_substate_b`

### fn11: 0x0808d060  size=0x15c (348 B)
- CID: 0x198e (Inferno Reckless Summon), dispatch entry [CID 0x198e]
- Body: push {r4-r7,lr}+push {r8,r9}; three loops: (1) monster via gP1SlotSetCodeArray+PLAYER_BLOCK_STRIDE; gate: NECROVALLEY_CID (0x0000159d) + count_field_copies_of_card (0x0803279c) + check_card_pair_allowed (0x0804ab4c) + eval_equip_placement_full_check (0x0803bba4); write substate_d. (2) hand via gP1HandSlotArray + check_zone_slot_equip_eligible (0x08037434); write substate_e. (3) field via gP1FieldArrayCBase; write substate_b
- BL targets: 0x0804ab4c (check_card_pair_allowed, x3), 0x0803bba4 (eval_equip_placement_full_check, x2), 0x08037434, 0x0803279c (count_field_copies_of_card), 0x0808d88c (x3)
- Pool: @0x0808d1a4=0x0201c4e0, @0x0808d1a8=0x00000868, @0x0808d1ac=0x0201c740 (gP1SlotSetCodeArray), @0x0808d1b0=0x0000159d (NECROVALLEY_CID), @0x0808d1b4=0x0201c8f8 (gP1HandSlotArray), @0x0808d1b8=0x0201c600 (gP1FieldArrayCBase)
- CID status: INFERNO_RECKLESS_SUMMON_CID(0x198e) REUSE (card_info.inc:1613)
- Substate: 0xd first (MOVS r1,#0xd at 0x0808d0b4, BL at 0x0808d0b8); 0xe second (MOVS r1,#0xe at 0x0808d120, BL at 0x0808d124); 0xb third (MOVS r1,#0xb at 0x0808d182, BL at 0x0808d186)
- Proposed name: `scan_zone_inferno_reckless_summon_substate_d_e_b`
- Confidence: high (three-loop body with NECROVALLEY gate; dispatch table entry 289 CID=0x198e confirmed; substates d/e/b ROM-verified)
- ASCII plate (len=492): `Equip zone scan for Inferno Reckless Summon (INFERNO_RECKLESS_SUMMON_CID=0x198e). Three loops: (1) monster via gP1SlotSetCodeArray+PLAYER_BLOCK_STRIDE; gate: NECROVALLEY_CID+count_field_copies_of_card (0x0803279c)+check_card_pair_allowed (0x0804ab4c)+eval_equip_placement_full_check (0x0803bba4); write substate_d. (2) hand via gP1HandSlotArray+check_zone_slot_equip_eligible (0x08037434); write substate_e. (3) field via gP1FieldArrayCBase; write substate_b. Dispatch table entry [CID 0x198e].`
- CSV row: `0x0808d060,scan_zone_inferno_reckless_summon_substate_d_e_b`

### fn12: 0x0808d1bc  size=0x068 (104 B)
- CID: 0x1996 (White Horns Dragon), dispatch entry [CID 0x1996]
- Body: push {r4-r7,lr}+push {r8}; monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: get_card_extended_stat_field6 (race check, 0x080eedf8, result CMP 0x16 = Zombie race); write substate_e
- BL targets: 0x080eedf8 (get_card_extended_stat_field6), 0x0808d88c
- Pool: @0x0808d21c=0x0201c4e0 (gP1LifePoints), @0x0808d220=0x00000868 (PLAYER_BLOCK_STRIDE)
- CID status: WHITE_HORNS_DRAGON_CID(0x1996) REUSE (card_info.inc:553)
- Substate: 0xe (MOVS r1,#0xe at 0x0808d200, BL at 0x0808d204)
- Proposed name: `scan_zone_white_horns_dragon_substate_e`
- Confidence: high (Zombie race gate; White Horns Dragon removes Zombie monsters from opponent GY; dispatch table entry 290 CID=0x1996 confirmed)
- ASCII plate (len=280): `Equip zone scan for White Horns Dragon (WHITE_HORNS_DRAGON_CID=0x1996). Monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: get_card_extended_stat_field6 (race=0x16 Zombie check). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1996].`
- CSV row: `0x0808d1bc,scan_zone_white_horns_dragon_substate_e`

### fn13: 0x0808d224  size=0x070 (112 B)
- CID: 0x19ac (Magnet Circle LV2), dispatch entry [CID 0x19ac]
- Body: push {r4,r5,r6,lr}; field array via gP1FieldArrayCBase+PLAYER_BLOCK_STRIDE; gate: get_card_extended_stat_field6 (0x080eedf8) + eval_equip_bonus_for_slot (0x080377b0) + eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x0804ad48, 0x080eedf8, 0x080377b0 (eval_equip_bonus_for_slot), 0x0803bba4, 0x0808d88c
- Pool: @0x0808d28c=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808d290=0x0201c600 (gP1FieldArrayCBase)
- CID status: MAGNET_CIRCLE_LV2_CID(0x19ac) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808d27c, BL at 0x0808d280)
- Proposed name: `scan_zone_magnet_circle_lv2_substate_b`
- Confidence: high (field array + race gate; Magnet Circle LV2 adds Magnet Warrior from deck, write_b = field zone)
- ASCII plate (len=356): `Equip zone scan for Magnet Circle LV2 (MAGNET_CIRCLE_LV2_CID=0x19ac). Field array via gP1FieldArrayCBase+PLAYER_BLOCK_STRIDE; gate: get_card_extended_stat_field6 (0x080eedf8)+eval_equip_bonus_for_slot (0x080377b0)+eval_equip_placement_full_check (0x0803bba4). write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x19ac].`
- CSV row: `0x0808d224,scan_zone_magnet_circle_lv2_substate_b`

### fn14: 0x0808d294  size=0x090 (144 B)
- CID: 0x19ae (Ancient Gear Drill), dispatch entry [CID 0x19ae]
- Body: push {r4-r7,lr}+push {r8}; monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (race) + check_field_spell_b_placeable (0x080309fc) + find_first_available_monster_slot_for_player (0x08033bf4) + get_card_extended_stat_field9 (0x080eee7c); write substate_d
- BL targets: 0x080eedf8 (get_card_extended_stat_field6), 0x080309fc, 0x08033bf4, 0x080eee7c, 0x0808d88c
- Pool: @0x0808d318=0x0201c4e0 (gP1LifePoints), @0x0808d31c=0x00000868 (PLAYER_BLOCK_STRIDE), @0x0808d320=0x0201c740 (gP1SlotSetCodeArray)
- CID status: ANCIENT_GEAR_DRILL_CID(0x19ae) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808d2f6, BL at 0x0808d2fa)
- Proposed name: `scan_zone_ancient_gear_drill_substate_d`
- Confidence: high (monster zone + multi-gate; Ancient Gear Drill: place spell/trap from deck, monster target must exist; write_d = monster zone)
- ASCII plate (len=414): `Equip zone scan for Ancient Gear Drill (ANCIENT_GEAR_DRILL_CID=0x19ae). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (0x080eedf8)+check_field_spell_b_placeable (0x080309fc)+find_first_available_monster_slot_for_player (0x08033bf4)+get_card_extended_stat_field9 (0x080eee7c). write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19ae].`
- CSV row: `0x0808d294,scan_zone_ancient_gear_drill_substate_d`

### fn15: 0x0808d324  size=0x0b4 (180 B)
- CID: 0x19b6 (Damage Condenser), dispatch entry [CID 0x19b6]
- Body: push {r4-r7,lr}+push {r8,r9}; SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: get_card_extended_stat_field3_raw (0x080eef44) + eval_equip_placement_full_check (0x0803bba4) + find_effect_node_in_zone (0x0802fd60); PARASITE_PARACIDE_CID (0x000012a1) pool slot used in filter; write substate_d
- BL targets: 0x0804ad48, 0x080eef44, 0x0803bba4, 0x0802fd60 (find_effect_node_in_zone), 0x0808d88c
- Pool: @0x0808d3c8=0x0201c4e0, @0x0808d3cc=0x00000868, @0x0808d3d0=0x0201c740 (gP1SlotSetCodeArray), @0x0808d3d4=0x000012a1 (PARASITE_PARACIDE_CID)
- CID status: DAMAGE_CONDENSER_CID(0x19b6) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808d3a2, BL at 0x0808d3a6)
- Proposed name: `scan_zone_damage_condenser_substate_d`
- Confidence: high (SlotSetCode monster zone + field3_raw gate; Damage Condenser: special summon monster when taking damage; write_d = monster zone)
- ASCII plate (len=418): `Equip zone scan for Damage Condenser (DAMAGE_CONDENSER_CID=0x19b6). SlotSetCode monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE+gP1SlotSetCodeArray; gate: get_card_extended_stat_field3_raw (0x080eef44)+eval_equip_placement_full_check (0x0803bba4)+find_effect_node_in_zone (0x0802fd60). PARASITE_PARACIDE_CID pool slot. write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19b6].`
- CSV row: `0x0808d324,scan_zone_damage_condenser_substate_d`

### fn16: 0x0808d3d8  size=0x0bc (188 B)
- CID: 0x19c5 (Gokipon), dispatch entry [CID 0x19c5]
- Body: push {r4-r7,lr}+push {r8,r9}; SlotSetCode monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (race, x2) + get_card_extended_stat_field3_raw + find_effect_node_in_zone (0x0802fd60); pool: CARD_FIELD3_THRESHOLD_1500 (0x000005dc) + PARASITE_PARACIDE_CID + gP1SlotCountBase; write substate_d
- BL targets: 0x080eedf8 (x2), 0x080eef44, 0x0802fd60, 0x0808d88c
- Pool: @0x0808d47c=0x0201c4e0, @0x0808d480=0x00000868, @0x0808d484=0x0201c740 (gP1SlotSetCodeArray), @0x0808d488=0x000005dc (CARD_FIELD3_THRESHOLD_1500), @0x0808d48c=0x000012a1 (PARASITE_PARACIDE_CID), @0x0808d490=0x0201c4f0 (gP1SlotCountBase)
- CID status: GOKIPON_CID(0x19c5) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808d452, BL at 0x0808d456)
- Proposed name: `scan_zone_gokipon_substate_d`
- Confidence: high (race x2 + field3_raw threshold gate; Gokipon: recruit insect-type ATK<=1000 from deck; write_d = monster zone)
- ASCII plate (len=403): `Equip zone scan for Gokipon (GOKIPON_CID=0x19c5). SlotSetCode monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (race, x2)+get_card_extended_stat_field3_raw+find_effect_node_in_zone (0x0802fd60). Pool: CARD_FIELD3_THRESHOLD_1500+PARASITE_PARACIDE_CID+gP1SlotCountBase. write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19c5].`
- CSV row: `0x0808d3d8,scan_zone_gokipon_substate_d`

### fn17: 0x0808d494  size=0x11c (284 B)
- CID: 0x19d7 (Symbol of Heritage), dispatch entry [CID 0x19d7]
- Body: push {r4-r7,lr}+push {r8,r9}; multi-loop: hand (gP1HandSlotArray+gP1HandCountBase+PLAYER_BLOCK_STRIDE x2) and monster (gP1LifePoints+PLAYER_BLOCK_STRIDE); write substate_e
- BL targets: 0x0808d88c
- Pool: @0x0808d5a0=0x0201c4e0, @0x0808d5a4=0x00000868, @0x0808d5a8=0x0201c8f8 (gP1HandSlotArray), @0x0808d5ac=0x0201c4f4 (gP1HandCountBase)
- CID status: SYMBOL_OF_HERITAGE_CID(0x19d7) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808d56a, BL at 0x0808d56c)
- Proposed name: `scan_zone_symbol_of_heritage_substate_e`
- Confidence: high (hand + monster loop; Symbol of Heritage: equip to monster with 3 same-name in GY; write_e = hand slot)
- ASCII plate (len=293): `Equip zone scan for Symbol of Heritage (SYMBOL_OF_HERITAGE_CID=0x19d7). Multi-loop: hand (gP1HandSlotArray+gP1HandCountBase+PLAYER_BLOCK_STRIDE x2) and monster (gP1LifePoints+PLAYER_BLOCK_STRIDE). write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x19d7].`
- CSV row: `0x0808d494,scan_zone_symbol_of_heritage_substate_e`

### fn18: 0x0808d5b0  size=0x0e4 (228 B)  [multi-CID: 0x19dc + 0x19dd]
- CID: 0x19dc (Next to be Lost) + 0x19dd (Generation Shift), dispatch entries [CID 0x19dc, CID 0x19dd]
- Body: push {r4-r7,lr}+push {r8,r9}; two loops: (1) monster via gP1LifePoints+gP1SlotSetCodeArray+find_effect_node_in_zone (0x0802fd60)+PARASITE_PARACIDE_CID gate; write substate_d. (2) SlotSetCode via gP1SlotSetCodeArray+PLAYER_BLOCK_STRIDE; write substate_c
- BL targets: 0x0804ab4c (check_card_pair_allowed), 0x0802fd60 (find_effect_node_in_zone), 0x0808d88c (x2)
- Pool: @0x0808d684=0x0201c4e0, @0x0808d688=0x00000868, @0x0808d68c=0x0201c740 (gP1SlotSetCodeArray), @0x0808d690=0x000012a1 (PARASITE_PARACIDE_CID)
- CID status: GENERATION_SHIFT_CID(0x19dd) REUSE; NEXT_TO_BE_LOST_CID(0x19dc) NEW (C5 grep: 0 hits in card_info.inc; data/card-stats.s line 26834)
- Substate: 0xd first (MOVS r1,#0xd at 0x0808d618, BL at 0x0808d61c); 0xc second (MOVS r1,#0xc at 0x0808d662, BL at 0x0808d666)
- Proposed name: `scan_zone_generation_shift_substate_d_c`
- Confidence: high (two CIDs confirmed in dispatch table via fn_ptr+1 scan; both point to 0x0808d5b1; write_d = monster zone, write_c = chain zone)
- ASCII plate (len=373): `Equip zone scan for Generation Shift+Next to be Lost (GENERATION_SHIFT_CID=0x19dd/NEXT_TO_BE_LOST_CID=0x19dc). Loop1: monster via gP1LifePoints+gP1SlotSetCodeArray+find_effect_node_in_zone (0x0802fd60)+PARASITE_PARACIDE_CID; write substate_d. Loop2: SlotSetCode via gP1SlotSetCodeArray+PLAYER_BLOCK_STRIDE; write substate_c. Dispatch table entries [CID 0x19dc, CID 0x19dd].`
- CSV row: `0x0808d5b0,scan_zone_generation_shift_substate_d_c`

### fn19: 0x0808d694  size=0x070 (112 B)
- CID: 0x19ec (Flute of Summoning Kuriboh), dispatch entry [CID 0x19ec]
- Body: push {r4,r5,r6,r7,lr}; SlotSetCode monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: WINGED_KURIBOH_CID=0x000018aa check; write substate_d
- BL targets: 0x0808d88c
- Pool: @0x0808d6f4=0x0201c4e0, @0x0808d6f8=0x00000868, @0x0808d6fc=0x0201c740 (gP1SlotSetCodeArray), @0x0808d700=0x000018aa (WINGED_KURIBOH_CID)
- CID status: FLUTE_SUMMONING_KURIBOH_CID(0x19ec) REUSE; WINGED_KURIBOH_CID(0x18aa) NEW (C5 grep: 0 hits for 0x18aa in card_info.inc; data/card-stats.s line 23636)
- Substate: 0xd (MOVS r1,#0xd at 0x0808d6d6, BL at 0x0808d6da)
- Proposed name: `scan_zone_flute_summoning_kuriboh_substate_d`
- Confidence: high (monster zone + WINGED_KURIBOH_CID filter; Flute of Summoning Kuriboh SS Kuriboh when Winged Kuriboh present; write_d = monster zone)
- ASCII plate (len=284): `Equip zone scan for Flute of Summoning Kuriboh (FLUTE_SUMMONING_KURIBOH_CID=0x19ec). SlotSetCode monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: WINGED_KURIBOH_CID=0x18aa check. write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x19ec].`
- CSV row: `0x0808d694,scan_zone_flute_summoning_kuriboh_substate_d`

### fn20: 0x0808d704  size=0x0f0 (240 B)  [CID=0xfffe group sentinel]
- CID: 0xfffe (multi-card group sentinel, LAST real entry before CID=0xffff terminator)
- Body: push {r4-r7,lr}+push {r8,r9}+SUB sp,#0x80; r8=arg2=substate (variable, set by dispatch caller at r2); phase1 loop: collect eligible slot indices via scan_card_type_effect_handler_table (0x08097114) into stack buf; phase2: per buf slot call read_player_field_slot_word_by_zone (0x0803b738) + get_zone_slot_entity_ref_by_type (0x0803b3a8); write substate=r8
- BL targets: 0x08097104 (unnamed, ROM_INCBIN 0x970d0), 0x080970d4 (unnamed, x2), 0x08097114 (scan_card_type_effect_handler_table), 0x080970d0 (unnamed), 0x080970e4 (unnamed), 0x0803b738 (read_player_field_slot_word_by_zone), 0x0803b3a8 (get_zone_slot_entity_ref_by_type), 0x0808d88c
- Pool: @0x0808d7a0=0x0201e4f0 (gEquipEffectZoneBase), @0x0808d7dc=0x00001fff (SLOT_CARD_SET_CODE_MASK), @0x0808d7e0=0x0201e4f0 (gEquipEffectZoneBase)
- CID status: n/a (sentinel)
- Substate: r8=arg2 (variable; confirmed by MOV r1,r8 at 0x0808d770, 0x0808d780, 0x0808d78e before BL@0x0808d792); no hardcoded MOVS r1 for this write call
- Proposed name: `scan_zone_group_handler_multi_card`
- Confidence: high (CID=0xfffe is the standard multi-card group sentinel in this table; scan_card_type_effect_handler_table confirms it iterates across card type categories; substate passed from caller)
- ASCII plate (len=461): `Equip zone scan group handler (CID=0xfffe sentinel). r8=arg2=substate (variable). Phase1: collect eligible slots via scan_card_type_effect_handler_table (0x08097114) loop into stack buf. Phase2: per buf slot call read_player_field_slot_word_by_zone (0x0803b738)+get_zone_slot_entity_ref_by_type (0x0803b3a8). write_equip_zone_entry_by_substate(player_id, r8, slot_idx). Pool: gEquipEffectZoneBase (x2)+SLOT_CARD_SET_CODE_MASK. Dispatch table entry [CID 0xfffe].`
- CSV row: `0x0808d704,scan_zone_group_handler_multi_card`

---

## Group-Handler CID Sets

| fn  | CIDs handled | card names |
|-----|-------------|------------|
| fn18 | 0x19dc, 0x19dd | Next to be Lost, Generation Shift |
| fn20 | 0xfffe sentinel | multi-card group (all cards dispatched by scan_card_type_effect_handler_table) |

Both entries for fn18 in the dispatch table (ROM 0x09e5a128) point to fn_ptr=0x0808d5b1 (fn18 addr + 1 THUMB).

---

## Symbols Plan

### EQ_SLOTS (data-equate)

All CID-value equates go into `constants/card_info.inc`. One raw-value equate to `constants/card_info.inc`.

| slot addr | value | const_name | slot_label | new/reuse |
|-----------|-------|------------|-----------|-----------|
| pool@0x0808d700 | 0x000018aa | WINGED_KURIBOH_CID | scan_zone_flute_summoning_kuriboh_substate_d_pool_18aa | NEW |
| pool@0x0808d1b0 | 0x0000159d | NECROVALLEY_CID | scan_zone_inferno_reckless_summon_substate_d_e_b_pool_159d | REUSE (card_info.inc line 297) |
| pool@0x0808d3d4 | 0x000012a1 | PARASITE_PARACIDE_CID | scan_zone_damage_condenser_substate_d_pool_12a1 | REUSE |
| pool@0x0808d48c | 0x000012a1 | PARASITE_PARACIDE_CID | scan_zone_gokipon_substate_d_pool_12a1 | REUSE |
| pool@0x0808d690 | 0x000012a1 | PARASITE_PARACIDE_CID | scan_zone_generation_shift_substate_d_c_pool_12a1 | REUSE |
| pool@0x0808d488 | 0x000005dc | CARD_FIELD3_THRESHOLD_1500 | scan_zone_gokipon_substate_d_pool_5dc | REUSE |
| pool@0x0808d7dc | 0x00001fff | SLOT_CARD_SET_CODE_MASK | scan_zone_group_handler_multi_card_pool_1fff | REUSE (card_info.inc) |

Raw-value equate (not a CID, goes to constants/card_info.inc or a new constants file):

| slot addr | value | const_name | new/reuse |
|-----------|-------|------------|-----------|
| pool@0x0808d00c | 0x0fffffff | CARD_FIELD_STAT_CLEAR_UPPER4_MASK | NEW (0 hits in all constants/*.inc by value grep) |

### CID-value pool equates (NEW CIDs, to add to constants/card_info.inc)

| const_name | value | card name | evidence |
|-----------|-------|-----------|---------|
| SCARR_DARK_WORLD_CID | 0x0000196a | Scarr, Scout of Dark World | data/card-stats.s line 25703; C5 grep 0 hits |
| GATEWAY_DARK_WORLD_CID | 0x00001973 | Gateway to Dark World | data/card-stats.s line 25807; C5 grep 0 hits |
| ARMED_CHANGER_CID | 0x0000197c | Armed Changer | data/card-stats.s line 25924; C5 grep 0 hits |
| WINGED_KURIBOH_CID | 0x000018aa | Winged Kuriboh | data/card-stats.s line 23636; C5 grep 0 hits |
| NEXT_TO_BE_LOST_CID | 0x000019dc | Next to be Lost | data/card-stats.s line 26834; C5 grep 0 hits |

### REF_SLOTS (USER-label + DATA-ref)

| slot addr | target | gas_label | slot_label |
|-----------|--------|-----------|-----------|
| pool@0x0808cb48 | 0x0201c4e0 | gP1LifePoints | scan_zone_level_modulation_substate_e_pool_lp |
| pool@0x0808cb4c | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_level_modulation_substate_e_pool_stride |
| pool@0x0808cb50 | 0x0201c4f4 | gP1HandCountBase | scan_zone_level_modulation_substate_e_pool_handcnt |
| pool@0x0808cbc8 | 0x0201c4e0 | gP1LifePoints | scan_zone_water_dragon_substate_e_pool_lp |
| pool@0x0808cbcc | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_water_dragon_substate_e_pool_stride |
| pool@0x0808cbd0 | 0x0201c8f8 | gP1HandSlotArray | scan_zone_water_dragon_substate_e_pool_hand |
| pool@0x0808cc50 | 0x0201c4e0 | gP1LifePoints | scan_zone_scarr_dark_world_substate_d_pool_lp |
| pool@0x0808cc54 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_scarr_dark_world_substate_d_pool_stride |
| pool@0x0808cc58 | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_scarr_dark_world_substate_d_pool_setcode |
| pool@0x0808ccac | 0x0201c4e0 | gP1LifePoints | scan_zone_pot_of_avarice_substate_e_pool_lp |
| pool@0x0808ccb0 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_pot_of_avarice_substate_e_pool_stride |
| pool@0x0808cd28 | 0x0201c4e0 | gP1LifePoints | scan_zone_boss_rush_substate_d_pool_lp |
| pool@0x0808cd2c | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_boss_rush_substate_d_pool_stride |
| pool@0x0808cd30 | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_boss_rush_substate_d_pool_setcode |
| pool@0x0808cdb4 | 0x0201c4e0 | gP1LifePoints | scan_zone_gateway_dark_world_substate_e_pool_lp |
| pool@0x0808cdb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_gateway_dark_world_substate_e_pool_stride |
| pool@0x0808cdbc | 0x0201c8f8 | gP1HandSlotArray | scan_zone_gateway_dark_world_substate_e_pool_hand |
| pool@0x0808ce30 | 0x0201c4e0 | gP1LifePoints | scan_zone_forces_of_darkness_substate_e_pool_lp |
| pool@0x0808ce34 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_forces_of_darkness_substate_e_pool_stride |
| pool@0x0808ce38 | 0x0201c8f8 | gP1HandSlotArray | scan_zone_forces_of_darkness_substate_e_pool_hand |
| pool@0x0808cea4 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_roll_out_substate_e_pool_stride_a |
| pool@0x0808cea8 | 0x0201c510 | gDuelFieldSlots | scan_zone_roll_out_substate_e_pool_field |
| pool@0x0808cf24 | 0x0201c4e0 | gP1LifePoints | scan_zone_roll_out_substate_e_pool_lp |
| pool@0x0808cf28 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_roll_out_substate_e_pool_stride_b |
| pool@0x0808cf2c | 0x0201c8f8 | gP1HandSlotArray | scan_zone_roll_out_substate_e_pool_hand |
| pool@0x0808cf30 | 0xffff803f | slot_field_mask_ffff803f | scan_zone_roll_out_substate_e_pool_mask |
| pool@0x0808cf80 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_roll_out_substate_e_pool_stride_c |
| pool@0x0808cf84 | 0x0201c4f4 | gP1HandCountBase | scan_zone_roll_out_substate_e_pool_handcnt |
| pool@0x0808d004 | 0x0201c4e0 | gP1LifePoints | scan_zone_armed_changer_substate_e_b_pool_lp |
| pool@0x0808d008 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_armed_changer_substate_e_b_pool_stride_a |
| pool@0x0808d010 | 0x0201c8f8 | gP1HandSlotArray | scan_zone_armed_changer_substate_e_b_pool_hand |
| pool@0x0808d04c | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_armed_changer_substate_e_b_pool_stride_b |
| pool@0x0808d050 | 0x0201c600 | gP1FieldArrayCBase | scan_zone_armed_changer_substate_e_b_pool_field |
| pool@0x0808d1a4 | 0x0201c4e0 | gP1LifePoints | scan_zone_inferno_reckless_summon_substate_d_e_b_pool_lp |
| pool@0x0808d1a8 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_inferno_reckless_summon_substate_d_e_b_pool_stride |
| pool@0x0808d1ac | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_inferno_reckless_summon_substate_d_e_b_pool_setcode |
| pool@0x0808d1b4 | 0x0201c8f8 | gP1HandSlotArray | scan_zone_inferno_reckless_summon_substate_d_e_b_pool_hand |
| pool@0x0808d1b8 | 0x0201c600 | gP1FieldArrayCBase | scan_zone_inferno_reckless_summon_substate_d_e_b_pool_field |
| pool@0x0808d21c | 0x0201c4e0 | gP1LifePoints | scan_zone_white_horns_dragon_substate_e_pool_lp |
| pool@0x0808d220 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_white_horns_dragon_substate_e_pool_stride |
| pool@0x0808d28c | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_magnet_circle_lv2_substate_b_pool_stride |
| pool@0x0808d290 | 0x0201c600 | gP1FieldArrayCBase | scan_zone_magnet_circle_lv2_substate_b_pool_field |
| pool@0x0808d318 | 0x0201c4e0 | gP1LifePoints | scan_zone_ancient_gear_drill_substate_d_pool_lp |
| pool@0x0808d31c | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_ancient_gear_drill_substate_d_pool_stride |
| pool@0x0808d320 | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_ancient_gear_drill_substate_d_pool_setcode |
| pool@0x0808d3c8 | 0x0201c4e0 | gP1LifePoints | scan_zone_damage_condenser_substate_d_pool_lp |
| pool@0x0808d3cc | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_damage_condenser_substate_d_pool_stride |
| pool@0x0808d3d0 | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_damage_condenser_substate_d_pool_setcode |
| pool@0x0808d47c | 0x0201c4e0 | gP1LifePoints | scan_zone_gokipon_substate_d_pool_lp |
| pool@0x0808d480 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_gokipon_substate_d_pool_stride |
| pool@0x0808d484 | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_gokipon_substate_d_pool_setcode |
| pool@0x0808d490 | 0x0201c4f0 | gP1SlotCountBase | scan_zone_gokipon_substate_d_pool_slotcnt |
| pool@0x0808d5a0 | 0x0201c4e0 | gP1LifePoints | scan_zone_symbol_of_heritage_substate_e_pool_lp |
| pool@0x0808d5a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_symbol_of_heritage_substate_e_pool_stride |
| pool@0x0808d5a8 | 0x0201c8f8 | gP1HandSlotArray | scan_zone_symbol_of_heritage_substate_e_pool_hand |
| pool@0x0808d5ac | 0x0201c4f4 | gP1HandCountBase | scan_zone_symbol_of_heritage_substate_e_pool_handcnt |
| pool@0x0808d684 | 0x0201c4e0 | gP1LifePoints | scan_zone_generation_shift_substate_d_c_pool_lp |
| pool@0x0808d688 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_generation_shift_substate_d_c_pool_stride |
| pool@0x0808d68c | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_generation_shift_substate_d_c_pool_setcode |
| pool@0x0808d6f4 | 0x0201c4e0 | gP1LifePoints | scan_zone_flute_summoning_kuriboh_substate_d_pool_lp |
| pool@0x0808d6f8 | 0x00000868 | PLAYER_BLOCK_STRIDE | scan_zone_flute_summoning_kuriboh_substate_d_pool_stride |
| pool@0x0808d6fc | 0x0201c740 | gP1SlotSetCodeArray | scan_zone_flute_summoning_kuriboh_substate_d_pool_setcode |
| pool@0x0808d7a0 | 0x0201e4f0 | gEquipEffectZoneBase | scan_zone_group_handler_multi_card_pool_zonebas_a |
| pool@0x0808d7e0 | 0x0201e4f0 | gEquipEffectZoneBase | scan_zone_group_handler_multi_card_pool_zonebas_b |

### RENAME_SLOTS

All 20 functions are currently auto-named (FUN_0808xxxx). All rename to proposed names above via Ghidra setName.

| addr | old_name (FUN_) | new_name | EOL |
|------|-----------------|----------|-----|
| 0x0808cabc | FUN_0808cabc | scan_zone_level_modulation_substate_e | none |
| 0x0808cb54 | FUN_0808cb54 | scan_zone_water_dragon_substate_e | none |
| 0x0808cbd4 | FUN_0808cbd4 | scan_zone_scarr_dark_world_substate_d | none |
| 0x0808cc5c | FUN_0808cc5c | scan_zone_pot_of_avarice_substate_e | none |
| 0x0808ccb4 | FUN_0808ccb4 | scan_zone_boss_rush_substate_d | none |
| 0x0808cd34 | FUN_0808cd34 | scan_zone_gateway_dark_world_substate_e | none |
| 0x0808cdc0 | FUN_0808cdc0 | scan_zone_forces_of_darkness_substate_e | none |
| 0x0808ce3c | FUN_0808ce3c | scan_zone_roll_out_substate_e | none |
| 0x0808cf88 | FUN_0808cf88 | scan_zone_armed_changer_substate_e_b | none |
| 0x0808d054 | FUN_0808d054 | scan_zone_magical_mallet_substate_b | none |
| 0x0808d060 | FUN_0808d060 | scan_zone_inferno_reckless_summon_substate_d_e_b | none |
| 0x0808d1bc | FUN_0808d1bc | scan_zone_white_horns_dragon_substate_e | none |
| 0x0808d224 | FUN_0808d224 | scan_zone_magnet_circle_lv2_substate_b | none |
| 0x0808d294 | FUN_0808d294 | scan_zone_ancient_gear_drill_substate_d | none |
| 0x0808d324 | FUN_0808d324 | scan_zone_damage_condenser_substate_d | none |
| 0x0808d3d8 | FUN_0808d3d8 | scan_zone_gokipon_substate_d | none |
| 0x0808d494 | FUN_0808d494 | scan_zone_symbol_of_heritage_substate_e | none |
| 0x0808d5b0 | FUN_0808d5b0 | scan_zone_generation_shift_substate_d_c | none |
| 0x0808d694 | FUN_0808d694 | scan_zone_flute_summoning_kuriboh_substate_d | none |
| 0x0808d704 | FUN_0808d704 | scan_zone_group_handler_multi_card | none |

### FUNC_RENAME
None. All 20 are currently FUN_0808xxxx with no previously-assigned semantic names to correct.

### PLATE (R5)
All 20 functions require new plate comments. See per-function entries above for exact ASCII text (all <= 500 chars, max=476 for fn11, all ASCII-only confirmed by re.findall('[^\\x00-\\x7f]') == []).

---

## carve plan (R7) -- none

No data tables or ROM_INCBIN sub-blocks inside [0x0808cabc, 0x0808d7f4). Pure THUMB code + literal pools only.

---

## disasm plan (R4)

The entire block is one ROM_INCBIN: `ROM_INCBIN 0x8cabc, 0xd38` (asm/11_effect_slot_puzzletext.s line 16402).

Disassemble all 20 functions as a single THUMB range [0x0808cabc, 0x0808d7f4).

| range | mode | notes |
|-------|------|-------|
| [0x0808cabc, 0x0808d7f4) | THUMB | 20 real functions, 3384 B total |

Exclusion notes:
- 0x0808d20e, 0x0808d21e: degenerate; will be part of fn12 body/pool naturally after DisassembleCommand on fn12 range
- 0x0808d7de: part of fn20 pool (word at 0x0808d7dc), will be part of fn20 literal pool naturally
- 0x0808d58c: degenerate weak entry; will be part of fn17 body naturally

All 4 addresses at 0x08097104, 0x080970d4, 0x080970d0, 0x080970e4 (BL targets from fn20) are inside `ROM_INCBIN 0x970d0, 0x44` (asm/12_equip_activation_scan.s line 6312) -- they are unnamed helpers in a separate incbin block; not part of this segment, not renamed here.

---

## Residue Gate

**Before Seg-4g landing**: `asm/11_effect_slot_puzzletext.s` line 16402 contains:
```
ROM_INCBIN 0x8cabc, 0xd38
```
This is the ONLY ROM_INCBIN in the address range [0x08087d58, 0x0808d7f4) (the entire Seg-4 giant block). Verified by: grep confirms exactly one `ROM_INCBIN 0x8cabc` line; all earlier sub-segments (Seg-4a..4f) have already been replaced with disassembled functions.

**After Seg-4g landing**: The disassembly of [0x0808cabc, 0x0808d7f4) will replace this ROM_INCBIN. The result is:
- Zero ROM_INCBIN remaining in the Seg-4 block [0x08087d58, 0x0808d7f4) -- BLOCK FULLY ELIMINATED.

---

## New Equates / Globals Required

### constants/card_info.inc (5 NEW CIDs + 1 NEW mask)

```asm
.equ SCARR_DARK_WORLD_CID,         0x0000196a  @ Scarr, Scout of Dark World (card-stats.s line 25703)
.equ GATEWAY_DARK_WORLD_CID,       0x00001973  @ Gateway to Dark World (card-stats.s line 25807)
.equ ARMED_CHANGER_CID,            0x0000197c  @ Armed Changer (card-stats.s line 25924)
.equ WINGED_KURIBOH_CID,           0x000018aa  @ Winged Kuriboh (card-stats.s line 23636)
.equ NEXT_TO_BE_LOST_CID,          0x000019dc  @ Next to be Lost (card-stats.s line 26834)
.equ CARD_FIELD_STAT_CLEAR_UPPER4_MASK, 0x0fffffff  @ clear upper 4 bits of field3 stat word
```

### ewram.inc (1 NEW global)

```asm
.equ gEquipEffectZoneBase,         0x0201e4f0  @ equip effect zone base; pool@fn20 0x0808d7a0+0x0808d7e0; STR r0,[r1] at 0x0808d74c clears it
```

---

## Pool DWord Verification Summary

All pool addresses are word-aligned (all end in 0/4/8/c). No missed second-pool sections:
- fn08 has 2 pool sections (first at 0x0808cea4, second at 0x0808cf24) -- both captured.
- fn09 has 2 pool sections (first at 0x0808d004, second at 0x0808d04c) -- both captured.
- fn20 has 2 pool sections (first at 0x0808d7a0, second at 0x0808d7dc) -- both captured.

All other functions have a single contiguous pool section.

Python ref-scan verification of all pool word values was performed by direct `struct.unpack_from('<I', rom, addr - 0x08000000)` reads; all values match known globals/constants.

---

## Sec5.1 Registration (Rule 3)

None. Every function in this segment is referenced by at least one dispatch table entry (fn_ptr+1 THUMB format in ROM 0x09e5a128). fn10 (0x0808d054) has exactly 1 ROM ref @0x9e5aa2c (dispatch table entry 288, CID=0x198d). No 0-reference blocks.

---

## Consumer Evidence (R6)

- `write_equip_zone_entry_by_substate` (0x0808d88c): substate semantics confirmed by plate comment in `asm/11_effect_slot_puzzletext.s`; verified 0xb=field, 0xc=chain, 0xd=monster, 0xe=hand. Confidence: high.
- Dispatch table at ROM 0x09e5a128: all CID-to-fn_ptr mappings cross-verified against `doc/dev/refine/F11-Seg4-cid-map.json`. fn18 dual-CID confirmed by scanning all 306 table entries for fn_ptr values 0x0808d5b1. Confidence: high.
- `CARD_FIELD_STAT_CLEAR_UPPER4_MASK=0x0fffffff`: consumed in fn09 at 0x0808cfbc-0x0808cfc2 as `AND r7,MASK; LSR r1; ADD r1,r9 -> loop` -- clears upper 4 bits of field3 stat read from card slot. Confidence: high (`asm/11_effect_slot_puzzletext.s` pool@0x0808d00c = 0x0fffffff).
- `gEquipEffectZoneBase=0x0201e4f0`: consumed in fn20 at 0x0808d74c (`STR r0,[r1]` clears base), and 0x0808d7b0..0x0808d7d4 (second section writes indexed entries). Existing plate at `write_equip_zone_entry_by_substate` (asm/11) already cites EFFECT_ZONE_BASE=0x0201e4f0. Confidence: high.

---

## Pending Clarification

None. All semantics resolved by consumer evidence or direct body decode.

---

## Executor Report: F11-Seg-4g
- Slots: EQ=10 (5 NEW CID + 1 NEW mask + 4 REUSE CID/const) REF=63 (pool ptr slots) RENAME=20 FUNC_RENAME=0 PLATE=20
- carve=0 disasm=1 range [0x0808cabc, 0x0808d7f4) sec5.1=0
- New constants/globals: SCARR_DARK_WORLD_CID(0x196a), GATEWAY_DARK_WORLD_CID(0x1973), ARMED_CHANGER_CID(0x197c), WINGED_KURIBOH_CID(0x18aa), NEXT_TO_BE_LOST_CID(0x19dc), CARD_FIELD_STAT_CLEAR_UPPER4_MASK(0x0fffffff), gEquipEffectZoneBase(0x0201e4f0)
- fn10 REUSE MAGICAL_MALLET_CID(0x198d, card_info.inc:842); fn11 REUSE INFERNO_RECKLESS_SUMMON_CID(0x198e, card_info.inc:1613); fn12 REUSE WHITE_HORNS_DRAGON_CID(0x1996, card_info.inc:553)
- Max plate len=492 (fn11), all 20 plates ASCII-only and <=500 chars
- Degenerate excluded=3 (0x0808d20e mid-body, 0x0808d21e mid-pool, 0x0808d7de align-pad), weak excluded=1 (0x0808d58c mid-body CMP r1,r0 inside fn17)
- Multi-CID: fn18 handles CID 0x19dc+0x19dd; fn20 is CID=0xfffe group sentinel
- Residue gate: landing eliminates LAST ROM_INCBIN in giant block [0x08087d58, 0x0808d7f4) -- Seg-4 COMPLETE
- Seek help: none
- proposal: doc/dev/refine/F11-Seg-4g.proposal.md
