# Refine Proposal: F11-Seg-4e  [0x0808ad8c..0x0808bb7c)

## Segment Survey

- ROM range: `[0x0808ad8c, 0x0808bb7c)` = 0xDF0 bytes (3568 B)
- Source: one-liner `ROM_INCBIN 0x8ad8c, <size>` (giant block, after Seg-4d carved 0x0808a2ac..0x0808ad8c)
- Boundary at 0x0808ad8c = first entry after Seg-4d end; boundary at 0x0808bb7c = next segment start (0x0808bb7c -> CID 0x1876 in dispatch table)
- Functions: **25 real functions** (27 strong entries - 2 degenerate = 25 real)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools

### Function type: equip zone scan callbacks (same pattern as Seg-4a/4b/4c/4d)

All 25 real functions are equip zone scan callbacks dispatched from the 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

---

## Degenerate Strong Entry Analysis (2 of 27)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808b40e | Mid-body code `210d` = MOVS r1,#0xd inside fn12 (0x0808b3a8..0x0808b43c). Falls at offset +0x66 inside fn12 body, after check gates at 0x0808b3e2..0x0808b40c. Epilogue of fn12 is at 0x0808b426 (bc08/4698/bcf0/bc01/4700). No dispatch table entry points here. | bytes 210d (MOVS r1,imm8); fn12 prologue at 0x0808b3a8 (b5f0 push {r4..r7,lr}); 0x0808b40e = 0x3a8+0x66 is inside write_equip arg-set sequence before BL 0x0808b412; fn12 epilogue confirmed at 0x0808b426 |
| 0x0808b95a | Mid-body code `0e09` = LSRS r1,r1,#24 inside fn25 (0x0808b940..0x0808b988). Falls at offset +0x1a inside fn25 body, part of bit-extraction sequence on a loaded GY-zone field. Epilogue of fn25 is at 0x0808b978 (bc30/bc01/4700). No dispatch table entry points here. | bytes 0e09 (LSRS, mid-loop shift); fn25 prologue at 0x0808b940 (b530 push {r4,r5,lr}); 0x0808b95a = 0x940+0x1a is inside the body before BL write_equip at 0x0808b966; fn25 epilogue confirmed at 0x0808b978 |

### Weak Entry Analysis (2 flagged)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808b58a | Second halfword (`4645`) of fn16 prologue high-register save sequence. fn16 starts at 0x0808b584 (b5f0 PUSH {r4..r7,lr}) followed by 4657/464e/4645 = MOV r7,r10 / MOV r6,r9 / MOV r5,r8. 0x0808b58a is 6 bytes into the prologue, not a function entry. | bytes 4645 = MOV r5,r8; fn16 prologue at 0x0808b584 b5f0; 0x0808b58a = 0x584+0x06 = mid-prologue high-reg save; no dispatch entry |
| 0x0808b798 | Upper halfword (`f9eb`) of 32-bit BL instruction at 0x0808b796..0x0808b79a inside fn19 body (0x0808b750..0x0808b7dc). fn19 starts at b5f0; 0x0808b798 = 0x750+0x48 = inside the outer loop before BL write_equip. | bytes f9eb = upper half of BL@0x0808b796 (2103 f7a5/f9eb = MOVS r1,#3 then BL 0x08030b70); fn19 epilogue at 0x0808b7c6 (bc08/4698/bcf0/bc01/4700) |

---

## Dispatch Table CID Scan (all seg-4e entries, table at 0x09e5a128, 305 entries)

| fn | addr | CID(s) | entry indices | card name(s) |
|----|------|--------|---------------|-------------|
| fn01 | 0x0808ad8c | 0x1748 | [180] | Avatar of The Pot |
| fn02 | 0x0808add0 | 0x175c | [183] | Monster Gate |
| fn03 | 0x0808ae4c | 0x1758, 0x1764 | [182], [184] | Archlord Zerato; Light of Judgment |
| fn04 | 0x0808ae98 | 0x1768 | [185] | Ninjitsu Art of Transformation |
| fn05 | 0x0808affc | 0x1769 | [186] | Beckoning Light |
| fn06 | 0x0808b07c | 0x1788 | [187] | Spirit of the Pharaoh |
| fn07 | 0x0808b12c | 0x178c | [189] | Nubian Guard |
| fn08 | 0x0808b1ac | 0x1795 | [190] | Spirit Caller |
| fn09 | 0x0808b240 | 0x1796 | [191] | Emissary of the Afterlife |
| fn10 | 0x0808b2c8 | 0x179a | [192] | Night Assailant |
| fn11 | 0x0808b350 | 0x17a2 | [193] | Soul Reversal |
| fn12 | 0x0808b3a8 | 0x17b2 | [195] | Human-Wave Tactics |
| fn13 | 0x0808b43c | 0x17af | [194] | The First Sarcophagus |
| fn14 | 0x0808b454 | 0x17e5, 0x17e6, 0x18f4 | [210],[211],[258] | Howling Insect; Masked Dragon; UFOroid |
| fn15 | 0x0808b52c | 0x17f1 | [212] | Dark Factory of Mass Production |
| fn16 | 0x0808b584 | 0x17f4 | [213] | Abyssal Designator |
| fn17 | 0x0808b688 | 0x17f7 | [215] | The Graveyard in the Fourth Dimension |
| fn18 | 0x0808b6e0 | 0x17f8 | [216] | Two-Man Cell Battle |
| fn19 | 0x0808b750 | 0x17f9 | [217] | Big Wave Small Wave |
| fn20 | 0x0808b7dc | 0x1818 | [224] | Magician's Circle |
| fn21 | 0x0808b874 | 0x183d | [229] | Mokey Mokey King |
| fn22 | 0x0808b8e8 | 0x1845 | [230] | Monster Reincarnation |
| fn23 | 0x0808b940 | 0x1847 | [231] | Lighten the Load |
| fn24 | 0x0808b988 | 0x1864 | [235] | Behemoth the King of All Animals |
| fn25 | 0x0808b9e0 | 0x1870, 0x1871, 0x1872 | [237],[238],[239] | The Light / Dark / Earth - Hex-Sealed Fusion |

Note: fn03 (group 0x1758+0x1764), fn14 (group 0x17e5+0x17e6+0x18f4), fn25 (group 0x1870+0x1871+0x1872) are group handlers. All others are single-CID.

Size check: fn01 starts 0x0808ad8c, fn25 ends 0x0808bb7c; total = 0xDF0 = 3568 B. Confirmed.

---

## Function Naming Table (25 real functions)

Substate semantics (from existing plate for write_equip_zone_entry_by_substate):
- 0xb = field-spell zone type B
- 0xc = chain zone type C
- 0xd = monster zone type D
- 0xe = hand slot type E
- 0xf = graveyard type F

### fn01: 0x0808ad8c  size=0x044 (68 B)
- CID: 0x1748 (Avatar of The Pot), dispatch entry [180]
- Body: push {r4,r5,lr}; scan gP1FieldArrayCBase field spell zone; gate: check_card_pair_allowed (0x0804ab4c) with partner POT_OF_GREED_CID; write substate_b
- BL targets: 0x0804ab4c (check_card_pair_allowed), 0x0808d88c
- Pool: 0x0808adc4=PLAYER_BLOCK_STRIDE, 0x0808adc8=gP1FieldArrayCBase, 0x0808adcc=POT_OF_GREED_CID(0x12ec)
- CID status: AVATAR_OF_THE_POT_CID(0x1748) REUSE; POT_OF_GREED_CID(0x12ec) REUSE
- Substate: 0xb
- Proposed name: `scan_zone_avatar_of_the_pot_substate_b`
- Confidence: high (body: field spell zone + check_card_pair_allowed partner=POT_OF_GREED; Avatar of The Pot equips to monsters when Pot of Greed is on field)
- ASCII plate (len=276): `Equip zone scan for Avatar of The Pot (AVATAR_OF_THE_POT_CID=0x1748, pw=99284890). Field spell zone via gP1FieldArrayCBase; gate: check_card_pair_allowed (partner=POT_OF_GREED_CID=0x12ec); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [180].`

### fn02: 0x0808add0  size=0x07c (124 B)
- CID: 0x175c (Monster Gate), dispatch entry [183]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + check_card_has_equip_placement_type (0x0804ba58); write substate_d
- BL targets: 0x0804ad48 (check_card_field5_is_nonzero), 0x0804ba58 (check_card_has_equip_placement_type), 0x0808d88c
- Pool: 0x0808ae40=gP1LifePoints, 0x0808ae44=PLAYER_BLOCK_STRIDE, 0x0808ae48=gP1SlotSetCodeArray
- CID status: MONSTER_GATE_CID(0x175c) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808ae1e before BL write_equip)
- Proposed name: `scan_zone_monster_gate_substate_d`
- Confidence: high (body: SlotSetCodeArray monster zone + equip_placement_type gate; Monster Gate sends card from deck to GY by coin flip; write_d = monster zone)
- ASCII plate (len=287): `Equip zone scan for Monster Gate (MONSTER_GATE_CID=0x175c, pw=43040603). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + check_card_has_equip_placement_type; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [183].`

### fn03: 0x0808ae4c  size=0x04c (76 B)
- CID(s): 0x1758 (Archlord Zerato), 0x1764 (Light of Judgment), dispatch entries [182], [184]
- Body: push {r4,r5,r6,lr}; scan gP1FieldArrayCBase field spell zone; MOVS r0,#1 (loop init); gates: check_card_field5_is_nonzero (0x0804ad48) + MOVS r1,#1 + check_card_stat_field7_equals (0x08030b70, arg=1=Light attr); write substate_b
- BL targets: 0x0804ad48, 0x08030b70, 0x0808d88c
- Pool: 0x0808ae90=PLAYER_BLOCK_STRIDE, 0x0808ae94=gP1FieldArrayCBase
- CID status: ARCHLORD_ZERATO_CID(0x1758) REUSE; 0x1764 (Light of Judgment) NEW
- Substate: 0xb (MOVS r1,#0xb at 0x0808ae80 before BL write_equip)
- Note: MOVS r1,#1 at 0x0808ae74 = arg to check_card_stat_field7_equals (Light attribute check)
- Proposed name: `scan_zone_archlord_zerato_light_group_substate_b`
- Confidence: high (body: field5_nonzero + Light-attr gate on field spell zone; both cards are LIGHT + require Light LIGHT monsters on field; dispatch entries [182,184])
- ASCII plate (len=380): `Equip zone scan for Archlord Zerato/Light of Judgment group: Archlord Zerato (ARCHLORD_ZERATO_CID=0x1758, pw=18378582), Light of Judgment (CID=0x1764, pw=44595286). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entries [182,184].`

### fn04: 0x0808ae98  size=0x164 (356 B)
- CID: 0x1768 (Ninjitsu Art of Transformation), dispatch entry [185]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7}; TWO-LOOP structure:
  loop1 scans gP1FieldArrayCBase field spell zone at +0xc; get_card_extended_stat_field6 (0x080eedf8) gate (cmp r0,#0xa/0xb/0x10 = race); eval_equip_bonus_for_slot (0x080377b0); eval_equip_placement_full_check (0x0803bba4); find_effect_node_in_zone (0x0802fd60, PARASITE_PARACIDE_CID=0x12a1); write substate_b;
  loop2 scans gP1SlotSetCodeArray monster zone at +0x14; same gate sequence; write substate_d
- BL targets: 0x080eedf8, 0x080377b0, 0x0803bba4, 0x0802fd60, 0x0808d88c
- Pool: 0x0808afe4=gP1LifePoints, 0x0808afe8=PLAYER_BLOCK_STRIDE, 0x0808afec=gP1FieldArrayCBase, 0x0808aff0=PARASITE_PARACIDE_CID(0x12a1), 0x0808aff4=gP1ZoneHandCount(0x0201c4ec), 0x0808aff8=gP1SlotSetCodeArray
- CID status: NINJITSU_ART_OF_TRANSFORMATION_CID(0x1768) REUSE; PARASITE_PARACIDE_CID(0x12a1) REUSE
- Substates: 0xb (loop1, MOVS r1,#0xb at 0x0808af1e), 0xd (loop2, MOVS r1,#0xd at 0x0808afbc)
- Proposed name: `scan_zone_ninjitsu_transformation_substate_bd`
- Confidence: high (body: dual-zone scan with FLIP-effect check via find_effect_node+PARASITE_PARACIDE_CID + race filter; Ninjitsu Art of Transformation activates on FLIP monster being attacked; write_b=field + write_d=monster)
- ASCII plate (len=445): `Equip zone scan for Ninjitsu Art of Transformation (NINJITSU_ART_OF_TRANSFORMATION_CID=0x1768, pw=70861343). Two-loop via gP1FieldArrayCBase (field, +0xc) + gP1SlotSetCodeArray (monster zone); gate: get_card_extended_stat_field6 race (0xa/0xb/0x10) + eval_equip_bonus_for_slot + eval_equip_placement + find_effect_node(PARASITE_PARACIDE_CID=0x12a1); write substate_b (loop1) + substate_d (loop2). Dispatch entry [185].`

### fn05: 0x0808affc  size=0x080 (128 B)
- CID: 0x1769 (Beckoning Light), dispatch entry [186]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_field5_is_nonzero (0x0804ad48) + MOVS r1,#1 + check_card_stat_field7_equals (0x08030b70, arg=1=Light attr); write substate_e
- BL targets: 0x0804ad48, 0x08030b70, 0x0808d88c
- Pool: 0x0808b070=gP1LifePoints, 0x0808b074=PLAYER_BLOCK_STRIDE, 0x0808b078=gP1HandSlotArray
- CID status: 0x1769 (Beckoning Light) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808b04c before BL write_equip)
- Note: MOVS r1,#1 at 0x0808b040 = arg to check_card_stat_field7_equals (Light attribute check)
- Proposed name: `scan_zone_beckoning_light_substate_e`
- Confidence: high (body: hand zone + field5_nonzero + Light-attr gate; Beckoning Light discards hand and returns LIGHT monsters from GY; write_e = hand slot)
- ASCII plate (len=281): `Equip zone scan for Beckoning Light (CID=0x1769, pw=16255442). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [186].`

### fn06: 0x0808b07c  size=0x0b0 (176 B)
- CID: 0x1788 (Spirit of the Pharaoh), dispatch entry [187]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7}; scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_field5_is_nonzero (0x0804ad48) + map_field8_to_card_type_category (0x0804a9dc) + get_card_extended_stat_field6 (0x080eedf8) x2 + get_card_extended_stat_field5 (0x080eee50) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x0804a9dc, 0x080eedf8 (x2), 0x080eee50, 0x08037434, 0x0808d88c
- Pool: 0x0808b120=gP1LifePoints, 0x0808b124=PLAYER_BLOCK_STRIDE, 0x0808b128=gP1HandSlotArray
- CID status: SPIRIT_OF_PHARAOH_CID(0x1788) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b0fa before BL write_equip)
- Proposed name: `scan_zone_spirit_of_the_pharaoh_substate_e`
- Confidence: high (body: hand zone + field8 category + dual field6 race gates + equip_eligible; Spirit of the Pharaoh SS 4 Normal Monsters from GY; write_e = hand slot)
- ASCII plate (len=392): `Equip zone scan for Spirit of the Pharaoh (SPIRIT_OF_PHARAOH_CID=0x1788, pw=25343280). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + get_card_extended_stat_field6 x2 + get_card_extended_stat_field5 + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [187].`

### fn07: 0x0808b12c  size=0x080 (128 B)
- CID: 0x178c (Nubian Guard), dispatch entry [189]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1HandSlotArray hand zone; gates: get_card_extended_stat_field6 (0x080eedf8) + get_card_extended_stat_field9 (0x080eee7c); write substate_e
- BL targets: 0x080eedf8, 0x080eee7c, 0x0808d88c
- Pool: 0x0808b1a0=gP1LifePoints, 0x0808b1a4=PLAYER_BLOCK_STRIDE, 0x0808b1a8=gP1HandSlotArray
- CID status: NUBIAN_GUARD_CID(0x178c) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b17c before BL write_equip)
- Proposed name: `scan_zone_nubian_guard_substate_e`
- Confidence: high (body: hand zone + field6/field9 gate; Nubian Guard retrieves a DARK Spellcaster from GY when destroyed; write_e = hand slot)
- ASCII plate (len=267): `Equip zone scan for Nubian Guard (NUBIAN_GUARD_CID=0x178c, pw=51616747). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: get_card_extended_stat_field6 + get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [189].`

### fn08: 0x0808b1ac  size=0x094 (148 B)
- CID: 0x1795 (Spirit Caller), dispatch entry [190]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_field5_is_nonzero (0x0804ad48) + map_field8_to_card_type_category (0x0804a9dc) + get_card_extended_stat_field5 (0x080eee50) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x0804a9dc, 0x080eee50, 0x08037434, 0x0808d88c
- Pool: 0x0808b234=gP1LifePoints, 0x0808b238=PLAYER_BLOCK_STRIDE, 0x0808b23c=gP1HandSlotArray
- CID status: 0x1795 (Spirit Caller) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808b212 before BL write_equip)
- Proposed name: `scan_zone_spirit_caller_substate_e`
- Confidence: high (body: hand zone + field8 category + field5_level + equip_eligible; Spirit Caller is a Spirit-type support; write_e = hand slot)
- ASCII plate (len=287): `Equip zone scan for Spirit Caller (CID=0x1795, pw=48659020). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + get_card_extended_stat_field5 + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [190].`

### fn09: 0x0808b240  size=0x088 (136 B)
- CID: 0x1796 (Emissary of the Afterlife), dispatch entry [191]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + map_field8_to_card_type_category (0x0804a9dc) + get_card_extended_stat_field5 (0x080eee50); write substate_d
- BL targets: 0x0804ad48, 0x0804a9dc, 0x080eee50, 0x0808d88c
- Pool: 0x0808b2bc=gP1LifePoints, 0x0808b2c0=PLAYER_BLOCK_STRIDE, 0x0808b2c4=gP1SlotSetCodeArray
- CID status: EMISSARY_OF_THE_AFTERLIFE_CID(0x1796) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808b298 before BL write_equip)
- Proposed name: `scan_zone_emissary_of_the_afterlife_substate_d`
- Confidence: high (body: SlotSetCodeArray monster zone + category + level gate; Emissary of the Afterlife adds a Normal Monster from deck when sent to GY; write_d = monster zone)
- ASCII plate (len=306): `Equip zone scan for Emissary of the Afterlife (EMISSARY_OF_THE_AFTERLIFE_CID=0x1796, pw=75043725). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + get_card_extended_stat_field5; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [191].`

### fn10: 0x0808b2c8  size=0x088 (136 B)
- CID: 0x179a (Night Assailant), dispatch entry [192]
- Body: push {r4..r7,lr} + extra push (r8,r9); scan gP1LifePoints+gP1HandSlotArray hand zone; gate: get_card_field_summon_restriction (0x0804b4f4); cmp r1 check; write substate_e
- BL targets: 0x0804b4f4 (get_card_field_summon_restriction), 0x0808d88c
- Pool: 0x0808b344=gP1LifePoints, 0x0808b348=PLAYER_BLOCK_STRIDE, 0x0808b34c=gP1HandSlotArray
- CID status: NIGHT_ASSAILANT_CID(0x179a) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b320 before BL write_equip)
- Proposed name: `scan_zone_night_assailant_substate_e`
- Confidence: high (body: hand zone + summon_restriction gate; Night Assailant is a DARK FLIP Warrior that returns a FLIP from GY to hand; write_e = hand slot)
- ASCII plate (len=247): `Equip zone scan for Night Assailant (NIGHT_ASSAILANT_CID=0x179a, pw=16226786). Hand zone via gP1LifePoints+gP1HandSlotArray; gate: get_card_field_summon_restriction; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [192].`

### fn11: 0x0808b350  size=0x058 (88 B)
- CID: 0x17a2 (Soul Reversal), dispatch entry [193]
- Body: push {r4,r5,lr}; scan gP1LifePoints monster zone via LDR+MUL loop (MOVS r0,#1 init); gate: get_card_field_summon_restriction (0x0804b4f4); write substate_e
- BL targets: 0x0804b4f4, 0x0808d88c
- Pool: 0x0808b3a0=gP1LifePoints, 0x0808b3a4=PLAYER_BLOCK_STRIDE
- CID status: 0x17a2 (Soul Reversal) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808b388 before BL write_equip)
- Proposed name: `scan_zone_soul_reversal_substate_e`
- Confidence: high (body: monster zone via LP+STRIDE loop + summon_restriction gate; Soul Reversal returns a removed-from-play Normal Monster to hand; write_e = hand slot)
- ASCII plate (len=244): `Equip zone scan for Soul Reversal (CID=0x17a2, pw=78864369). Monster zone via gP1LifePoints+PLAYER_BLOCK_STRIDE; gate: get_card_field_summon_restriction; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [193].`

### fn12: 0x0808b3a8  size=0x094 (148 B)  [spans 0x0808b40e degenerate]
- CID: 0x17b2 (Human-Wave Tactics), dispatch entry [195]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field5 (0x080eee50) level check + map_field8_to_card_type_category (0x0804a9dc) + eval_equip_placement_full_check (0x0803bba4); write substate_d
- BL targets: 0x0804ad48, 0x080eee50, 0x0804a9dc, 0x0803bba4, 0x0808d88c
- Pool: 0x0808b430=gP1LifePoints, 0x0808b434=PLAYER_BLOCK_STRIDE, 0x0808b438=gP1SlotSetCodeArray
- CID status: HUMAN_WAVE_TACTICS_CID(0x17b2) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808b40e -- degenerate entry -- then BL 0x0808b412 = write_equip)
- Note: 0x0808b40e (210d = MOVS r1,#0xd) is a degenerate strong entry falling inside fn12 body at offset+0x66; fn12 epilogue at 0x0808b426 (bc08/4698/bcf0/bc01/4700)
- Proposed name: `scan_zone_human_wave_tactics_substate_d`
- Confidence: high (body: SlotSetCodeArray + level + category + placement gates; Human-Wave Tactics SS multiple Normal Monsters from deck; write_d = monster zone; 0x0808b40e is degenerate mid-body)
- ASCII plate (len=351): `Equip zone scan for Human-Wave Tactics (HUMAN_WAVE_TACTICS_CID=0x17b2, pw=30353551). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field5 level + map_field8_to_card_type_category + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [195]. Addr 0x0808b40e is degenerate.`

### fn13: 0x0808b43c  size=0x018 (24 B)
- CID: 0x17af (The First Sarcophagus), dispatch entry [194]
- Body: push {lr}; CMP r2,#0; BEQ +4 (skip to MOVS r2,#0 + BL write_equip_zone_entries_by_lv_card_id); if r2!=0: BL scan_zone_destiny_board_substate_bd (0x08088a34) + B over second BL; POP {PC}
- BL targets: 0x08088a34 (scan_zone_destiny_board_substate_bd), 0x080872e4 (write_equip_zone_entries_by_lv_card_id)
- Pool: none (no LDR PC-relative loads)
- CID status: THE_FIRST_SARCOPHAGUS_CID(0x17af) REUSE
- Substates: b+d (via callee scan_zone_destiny_board_substate_bd when r2!=0); level-based (via write_equip_zone_entries_by_lv_card_id when r2==0)
- Proposed name: `scan_zone_first_sarcophagus_substate_bd`
- Confidence: high (body: r2-conditioned dispatch; r2!=0 path calls bd-substate scanner; r2==0 path calls lv-card-id writer; The First Sarcophagus is a continuous trap that targets specific monster zone conditions; dispatch entry [194])
- ASCII plate (len=224): `Equip zone scan dispatcher for The First Sarcophagus (THE_FIRST_SARCOPHAGUS_CID=0x17af, pw=31076103). Calls scan_zone_destiny_board_substate_bd if r2!=0, else write_equip_zone_entries_by_lv_card_id. Dispatch table entry [194].`

### fn14: 0x0808b454  size=0x0d8 (216 B)
- CID(s): 0x17e5 (Howling Insect), 0x17e6 (Masked Dragon), 0x18f4 (UFOroid), dispatch entries [210],[211],[258]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7} + b092 (SUB sp,#0x48 stack frame); MOVS r0,#0 + LDR gP1LifePoints; scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field3_raw (0x080eef44) cmp <=CARD_FIELD3_THRESHOLD_1500 (ATK<=1500) + get_card_extended_stat_field6 (0x080eedf8) x2 + eval_equip_placement_full_check (0x0803bba4) + find_effect_node_in_zone (0x0802fd60, PARASITE_PARACIDE_CID=0x12a1); write substate_b then substate_d
- BL targets: 0x0804ad48, 0x080eef44, 0x080eedf8 (x2), 0x0803bba4, 0x0802fd60, 0x0808d88c
- Pool: 0x0808b514=gP1LifePoints, 0x0808b518=PLAYER_BLOCK_STRIDE, 0x0808b51c=gP1SlotSetCodeArray, 0x0808b520=CARD_FIELD3_THRESHOLD_1500(0x5dc), 0x0808b524=PARASITE_PARACIDE_CID(0x12a1), 0x0808b528=gP1SlotCountBase(0x0201c4f0)
- CID status: 0x17e5 (Howling Insect) NEW; MASKED_DRAGON_CID(0x17e6) REUSE; UFOROID_CID(0x18f4) REUSE; PARASITE_PARACIDE_CID(0x12a1) REUSE
- Substates: 0xb (MOVS r1,#0xb at 0x0808b4da before BL find_effect_node), 0xd (MOVS r1,#0xd at 0x0808b4e8 before BL write_equip)
- Proposed name: `scan_zone_howling_insect_group_substate_bd`
- Confidence: high (body: ATK<=1500 gate + race check + FLIP-effect check; all 3 cards have ATK<=1800 and use destroy-to-search effects; dispatch entries [210,211,258])
- ASCII plate (len=420): `Equip zone scan for Howling Insect/Masked Dragon/UFOroid group: Howling Insect (CID=0x17e5, pw=93107608), Masked Dragon (MASKED_DRAGON_CID=0x17e6, pw=39191307), UFOroid (UFOROID_CID=0x18f4, pw=07602840). Monster zone via gP1LifePoints+SlotSetCodeArray; gates: field5_nonzero + field3_raw<=ATK1500 + field6 x2 + eval_placement + find_effect_node(PARASITE_PARACIDE_CID); write substate_b+d. Dispatch entries [210,211,258].`

### fn15: 0x0808b52c  size=0x058 (88 B)
- CID: 0x17f1 (Dark Factory of Mass Production), dispatch entry [212]
- Body: push {r4,r5,lr}; scan gP1LifePoints monster zone via MOVS r0,#1 + LDR+MUL loop; gate: map_field8_to_card_type_category (0x0804a9dc); write substate_e
- BL targets: 0x0804a9dc (map_field8_to_card_type_category), 0x0808d88c
- Pool: 0x0808b57c=gP1LifePoints, 0x0808b580=PLAYER_BLOCK_STRIDE
- CID status: DARK_FACTORY_MASS_PROD_CID(0x17f1) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b564 before BL write_equip)
- Proposed name: `scan_zone_dark_factory_mass_prod_substate_e`
- Confidence: high (body: monster zone loop + category gate; Dark Factory of Mass Production returns 2 Normal Monsters from GY to hand; write_e = hand-equiv substate)
- ASCII plate (len=258): `Equip zone scan for Dark Factory of Mass Production (DARK_FACTORY_MASS_PROD_CID=0x17f1, pw=90928333). Monster zone via gP1LifePoints+STRIDE; gate: map_field8_to_card_type_category; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [212].`

### fn16: 0x0808b584  size=0x104 (260 B)
- CID: 0x17f4 (Abyssal Designator), dispatch entry [213]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7}; TWO-LOOP structure:
  loop1 scans gP1FieldArrayCBase field spell zone at +0xc; gates: get_card_extended_stat_field6 (0x080eedf8) + get_card_extended_stat_field7 (0x080eee24); write substate_b;
  loop2 scans gP1SlotSetCodeArray monster zone at +0x10; same gates; write substate_d
- BL targets: 0x080eedf8 (x2), 0x080eee24 (x2), 0x0808d88c (x2)
- Pool: 0x0808b674=gP1LifePoints, 0x0808b678=PLAYER_BLOCK_STRIDE, 0x0808b67c=gP1FieldArrayCBase, 0x0808b680=gP1ZoneHandCount(0x0201c4ec), 0x0808b684=gP1SlotSetCodeArray
- CID status: ABYSSAL_DESIGNATOR_CID(0x17f4) REUSE
- Substates: 0xb (loop1, MOVS r1,#0xb at 0x0808b5e4), 0xd (loop2, MOVS r1,#0xd at 0x0808b64e)
- Note: 0x0808b58a (4645 = MOV r5,r8) is a degenerate weak entry -- mid-prologue high-register save inside fn16; excluded
- Proposed name: `scan_zone_abyssal_designator_substate_bd`
- Confidence: high (body: two-loop field+monster zones both gated by field6+field7 getters; Abyssal Designator declares type+attribute then destroys matching; dual zone write b+d)
- ASCII plate (len=329): `Equip zone scan for Abyssal Designator (ABYSSAL_DESIGNATOR_CID=0x17f4, pw=89801755). Two-loop: loop1 via gP1FieldArrayCBase (field zone, +0xc), gate field6+field7, write substate_b; loop2 via gP1SlotSetCodeArray (monster zone, +0x10), same gates, write substate_d. Dispatch table entry [213].`

### fn17: 0x0808b688  size=0x058 (88 B)
- CID: 0x17f7 (The Graveyard in the Fourth Dimension), dispatch entry [215]
- Body: push {r4,r5,lr}; scan gP1LifePoints monster zone via MOVS r0,#1 + LDR+MUL loop; gate: check_card_id_is_effect_monster_type_b (0x0804b0e4); write substate_e
- BL targets: 0x0804b0e4 (check_card_id_is_effect_monster_type_b), 0x0808d88c
- Pool: 0x0808b6d8=gP1LifePoints, 0x0808b6dc=PLAYER_BLOCK_STRIDE
- CID status: GRAVEYARD_IN_FOURTH_DIMENSION_CID(0x17f7) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b6c0 before BL write_equip)
- Proposed name: `scan_zone_graveyard_fourth_dimension_substate_e`
- Confidence: high (body: monster zone + effect_monster_type_b gate; Graveyard in the 4th Dimension returns a removed FLIP Effect Monster to GY; write_e)
- ASCII plate (len=277): `Equip zone scan for The Graveyard in the Fourth Dimension (GRAVEYARD_IN_FOURTH_DIMENSION_CID=0x17f7, pw=88089103). Monster zone via gP1LifePoints+STRIDE; gate: check_card_id_is_effect_monster_type_b; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [215].`

### fn18: 0x0808b6e0  size=0x070 (112 B)
- CID: 0x17f8 (Two-Man Cell Battle), dispatch entry [216]
- Body: push {r4,r5,lr}; scan gP1FieldArrayCBase field spell zone; MOVS r0,#1 (loop init); gates: check_card_field5_is_nonzero (0x0804ad48) + map_field8_to_card_type_category (0x0804a9dc) + eval_equip_bonus_for_slot (0x080377b0) + eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x0804ad48, 0x0804a9dc, 0x080377b0, 0x0803bba4, 0x0808d88c
- Pool: 0x0808b748=PLAYER_BLOCK_STRIDE, 0x0808b74c=gP1FieldArrayCBase
- CID status: 0x17f8 (Two-Man Cell Battle) NEW
- Substate: 0xb (MOVS r1,#0xb at 0x0808b738 before BL write_equip)
- Proposed name: `scan_zone_two_man_cell_battle_substate_b`
- Confidence: high (body: field spell zone + category + equip_bonus + placement gates; Two-Man Cell Battle lets Warrior-type attack twice; write_b = field spell zone)
- ASCII plate (len=329): `Equip zone scan for Two-Man Cell Battle (CID=0x17f8, pw=25578802). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + map_field8_to_card_type_category + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [216].`

### fn19: 0x0808b750  size=0x08c (140 B)
- CID: 0x17f9 (Big Wave Small Wave), dispatch entry [217]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1FieldArrayCBase; gates: check_card_field5_is_nonzero (0x0804ad48) + MOVS r1,#3 + check_card_stat_field7_equals (0x08030b70, arg=3=WATER attr) + eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x0804ad48, 0x08030b70, 0x0803bba4, 0x0808d88c
- Pool: 0x0808b7d0=gP1LifePoints, 0x0808b7d4=PLAYER_BLOCK_STRIDE, 0x0808b7d8=gP1FieldArrayCBase
- CID status: BIG_WAVE_SMALL_WAVE_CID(0x17f9) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808b7ae before BL write_equip)
- Note: 0x0808b798 (f9eb = upper half of BL instruction) is a degenerate weak entry inside fn19 body; excluded
- Proposed name: `scan_zone_big_wave_small_wave_substate_b`
- Confidence: high (body: field spell zone + field5 + WATER-attr gate + placement; Big Wave Small Wave SS 2 WATER monsters at ATK-halved; write_b = field spell zone)
- ASCII plate (len=310): `Equip zone scan for Big Wave Small Wave (BIG_WAVE_SMALL_WAVE_CID=0x17f9, pw=51562916). Field spell zone via gP1LifePoints+gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(3) (WATER attr) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entry [217].`

### fn20: 0x0808b7dc  size=0x098 (152 B)
- CID: 0x1818 (Magician's Circle), dispatch entry [224]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field3_raw (0x080eef44) >= (MOVS r1,#0xfa then LSLS by 3 = 0x7d0 = ATK>=2000) + get_card_extended_stat_field6 (0x080eedf8) race check + eval_equip_placement_full_check (0x0803bba4); write substate_d
- BL targets: 0x0804ad48, 0x080eef44, 0x080eedf8, 0x0803bba4, 0x0808d88c
- Pool: 0x0808b868=gP1LifePoints, 0x0808b86c=PLAYER_BLOCK_STRIDE, 0x0808b870=gP1SlotSetCodeArray
- CID status: MAGICIANS_CIRCLE_CID(0x1818) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808b846 before BL write_equip)
- Note: MOVS r1,#0xfa at 0x0808b824 + `00c9` LSLS r1,r1,#3 = ATK compare value 0x7d0 (2000); no existing const for this threshold
- Proposed name: `scan_zone_magicians_circle_substate_d`
- Confidence: high (body: SlotSetCodeArray + ATK>=2000 + race gate; Magician's Circle SS a Spellcaster ATK<=2000 from deck when a Spellcaster attacks; write_d = monster zone)
- ASCII plate (len=407): `Equip zone scan for Magicians Circle (MAGICIANS_CIRCLE_CID=0x1818, pw=00050755). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field3_raw>=(0xfa<<3)=0x7d0 (ATK>=2000) + get_card_extended_stat_field6 (race) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [224].`

### fn21: 0x0808b874  size=0x074 (116 B)
- CID: 0x183d (Mokey Mokey King), dispatch entry [229]
- Body: push {r4,r5,lr}; MOVS r0,#1 + scan gP1LifePoints+gP1HandSlotArray hand zone at +0x14 offset; gate: LDR r1,[PC,...]=0xbc100000 sentinel comparison (LSLS slot_word,#19 == 0xbc100000); BL check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x08037434 (check_zone_slot_equip_eligible), 0x0808d88c
- Pool: 0x0808b8d8=gP1LifePoints, 0x0808b8dc=PLAYER_BLOCK_STRIDE, 0x0808b8e0=gP1HandSlotArray, 0x0808b8e4=0xbc100000 (slot sentinel value)
- CID status: MOKEY_MOKEY_KING_CID(0x183d) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b8ba before BL write_equip)
- Note: pool 0x0808b8e4=0xbc100000 is a raw slot-type sentinel value; the LSLS r0,r0,#19 before the CMP extracts specific bit-fields from the hand slot entry; no existing const for 0xbc100000
- Proposed name: `scan_zone_mokey_mokey_king_substate_e`
- Confidence: high (body: hand zone at +0x14 + slot sentinel check + equip_eligible; Mokey Mokey King buffs Mokey Mokeys; hand slot scan confirms zone eligibility; write_e)
- ASCII plate (len=303): `Equip zone scan for Mokey Mokey King (MOKEY_MOKEY_KING_CID=0x183d, pw=13803864). Hand zone via gP1LifePoints+gP1HandSlotArray; gate: LSLS slot_word,#19 == 0xbc100000 sentinel + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [229].`

### fn22: 0x0808b8e8  size=0x058 (88 B)
- CID: 0x1845 (Monster Reincarnation), dispatch entry [230]
- Body: push {r4,r5,lr}; scan gP1LifePoints monster zone via MOVS r0,#1 + LDR+MUL loop; gate: check_card_field5_is_nonzero (0x0804ad48); write substate_e
- BL targets: 0x0804ad48, 0x0808d88c
- Pool: 0x0808b938=gP1LifePoints, 0x0808b93c=PLAYER_BLOCK_STRIDE
- CID status: 0x1845 (Monster Reincarnation) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808b920 before BL write_equip)
- Proposed name: `scan_zone_monster_reincarnation_substate_e`
- Confidence: high (body: monster zone + field5_nonzero gate; Monster Reincarnation discards 1 monster to return another from GY to hand; write_e = hand slot)
- ASCII plate (len=224): `Equip zone scan for Monster Reincarnation (CID=0x1845, pw=74848038). Monster zone via gP1LifePoints+STRIDE; gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [230].`

### fn23: 0x0808b940  size=0x048 (72 B)  [spans 0x0808b95a degenerate]
- CID: 0x1847 (Lighten the Load), dispatch entry [231]
- Body: push {r4,r5,lr}; MOVS r0,#1 + scan gP1FieldArrayCBase field spell zone at +0x14; gate: eval_equip_bonus_for_slot (0x080377b0); write substate_b
- BL targets: 0x080377b0 (eval_equip_bonus_for_slot), 0x0808d88c
- Pool: 0x0808b980=PLAYER_BLOCK_STRIDE, 0x0808b984=gP1FieldArrayCBase
- CID status: 0x1847 (Lighten the Load) NEW
- Substate: 0xb (MOVS r1,#0xb at 0x0808b970 before BL write_equip)
- Note: 0x0808b95a (0e09 = LSRS r1,r1,#24) is a degenerate strong entry at offset+0x1a inside fn23 body, mid bit-extraction; epilogue at 0x0808b978 (bc30/bc01/4700)
- Proposed name: `scan_zone_lighten_the_load_substate_b`
- Confidence: high (body: field spell zone at +0x14 + equip_bonus gate; Lighten the Load returns a Level 7 monster from hand to deck to draw 1 card; write_b = field spell zone)
- ASCII plate (len=225): `Equip zone scan for Lighten the Load (CID=0x1847, pw=37231841). Field spell zone via gP1FieldArrayCBase+STRIDE; gate: eval_equip_bonus_for_slot; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [231]. Addr 0x0808b95a is degenerate.`

### fn24: 0x0808b988  size=0x058 (88 B)
- CID: 0x1864 (Behemoth the King of All Animals), dispatch entry [235]
- Body: push {r4,r5,lr}; scan gP1LifePoints monster zone via MOVS r0,#1 + LDR+MUL loop; gate: get_card_extended_stat_field6 (0x080eedf8) race check (cmp r0,#0xb = DINOSAUR?); write substate_e
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x0808b9d8=gP1LifePoints, 0x0808b9dc=PLAYER_BLOCK_STRIDE
- CID status: BEHEMOTH_KING_CID(0x1864) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808b9c0 before BL write_equip)
- Proposed name: `scan_zone_behemoth_king_substate_e`
- Confidence: high (body: monster zone + field6 race gate; Behemoth the King of All Animals returns Beast monsters from GY when destroyed; write_e = hand-equiv)
- ASCII plate (len=250): `Equip zone scan for Behemoth the King of All Animals (BEHEMOTH_KING_CID=0x1864, pw=22996376). Monster zone via gP1LifePoints+STRIDE; gate: get_card_extended_stat_field6 (race); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [235].`

### fn25: 0x0808b9e0  size=0x19c (412 B)
- CID(s): 0x1870 (The Light - Hex-Sealed Fusion), 0x1871 (The Dark - Hex-Sealed Fusion), 0x1872 (The Earth - Hex-Sealed Fusion), dispatch entries [237],[238],[239]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7} + b092 (SUB sp,#0x48 = 18-word stack frame); STR r0,[sp,#0x34] (player_id); STR r1,[sp,#0x38]; MOVS r0,#0+STR [sp,#0x3c]; scan gP1ChainZoneArray (0x0201c880)+gDuelFieldSlots (0x0201c510) chain zone; gates: check_slot_card_can_be_equipped (0x08033730) + check_card_is_equip_target_eligible (0x0804bb6c) + check_card_id_is_equip_excluded_range (0x0804bc58) + get_card_extended_stat_field7 (0x080eee24) + check_card_stat_field7_equals (0x08030b70) + get_equip_display_type_code_by_card_id (0x0807f6f0) + get_equip_display_criteria_code_by_card_and_slot (0x0807f730) + check_slot_card_equip_criteria_by_state_code (0x0807f618); MOVS r1,#0x0c + BL write_equip (substate_c)
- BL targets: 0x08033730, 0x0804bb6c, 0x0804bc58, 0x080eee24, 0x08030b70, 0x0807f6f0, 0x0807f730, 0x0807f618, 0x0808d88c
- Pool: 0x0808bb20=PLAYER_BLOCK_STRIDE, 0x0808bb24=gDuelFieldSlots(0x0201c510), 0x0808bb28=gP1LifePoints, 0x0808bb2c=gP1ChainZoneArray(0x0201c880), 0x0808bb74=gP1LifePoints(loop2), 0x0808bb78=PLAYER_BLOCK_STRIDE(loop2)
- CID status: 0x1870, 0x1871, 0x1872 all NEW
- Substate: 0xc (MOVS r1,#0xc at 0x0808bb46 before BL write_equip)
- Proposed name: `scan_zone_hex_sealed_fusion_group_substate_c`
- Confidence: high (body: chain zone scan with comprehensive equip eligibility checks; all 3 Hex-Sealed Fusion cards substitute as a fusion material in chain zone; substate_c = chain zone; dispatch entries [237,238,239])
- ASCII plate (len=466): `Equip zone scan for Hex-Sealed Fusion group: Light (CID=0x1870, pw=15717011), Dark (CID=0x1871, pw=52101615), Earth (CID=0x1872, pw=88696724). Chain zone via gP1ChainZoneArray+gDuelFieldSlots; gates: check_slot_card_can_be_equipped + check_card_is_equip_target_eligible + check_card_id_is_equip_excluded_range + equip_display_criteria + check_slot_equip_criteria_by_state; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatch entries [237,238,239].`

---

## Group-Handler CID Sets

| fn | addr | CID count | CIDs | note |
|----|------|-----------|------|------|
| fn03 | 0x0808ae4c | 2 | 0x1758 (ARCHLORD_ZERATO_CID), 0x1764 (NEW) | Light-attr field spell gate |
| fn14 | 0x0808b454 | 3 | 0x17e5 (NEW), 0x17e6 (MASKED_DRAGON_CID), 0x18f4 (UFOROID_CID) | ATK<=1500 + FLIP-effect gate |
| fn25 | 0x0808b9e0 | 3 | 0x1870 (NEW), 0x1871 (NEW), 0x1872 (NEW) | chain zone comprehensive gate |

---

## REF_SLOTS (createDWordWithRef plan)

Per Seg-4a/4b/4c/4d precedent: every pool DWord holding an EWRAM address gets
createDWordWithRef + RENAME to export as `.word gP1LifePoints` etc.

### gP1LifePoints = 0x0201c4e0 (ewram.inc) -- 19 slots

| slot addr | fn |
|-----------|-----|
| 0x0808ae40 | fn02 |
| 0x0808afe4 | fn04 |
| 0x0808b070 | fn05 |
| 0x0808b120 | fn06 |
| 0x0808b1a0 | fn07 |
| 0x0808b234 | fn08 |
| 0x0808b2bc | fn09 |
| 0x0808b344 | fn10 |
| 0x0808b3a0 | fn11 |
| 0x0808b430 | fn12 |
| 0x0808b514 | fn14 |
| 0x0808b57c | fn15 |
| 0x0808b674 | fn16 |
| 0x0808b6d8 | fn17 |
| 0x0808b7d0 | fn19 |
| 0x0808b868 | fn20 |
| 0x0808b8d8 | fn21 |
| 0x0808b938 | fn22 |
| 0x0808b9d8 | fn24 |
| 0x0808bb28 | fn25 loop1 |
| 0x0808bb74 | fn25 loop2 |

REF count gP1LifePoints: **21**

### gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 7 slots

| slot addr | fn |
|-----------|-----|
| 0x0808adc8 | fn01 |
| 0x0808ae94 | fn03 |
| 0x0808afec | fn04 |
| 0x0808b67c | fn16 |
| 0x0808b74c | fn18 |
| 0x0808b7d8 | fn19 |
| 0x0808b984 | fn23 |

REF count gP1FieldArrayCBase: **7**

### gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 6 slots

| slot addr | fn |
|-----------|-----|
| 0x0808b078 | fn05 |
| 0x0808b128 | fn06 |
| 0x0808b1a8 | fn07 |
| 0x0808b23c | fn08 |
| 0x0808b34c | fn10 |
| 0x0808b8e0 | fn21 |

REF count gP1HandSlotArray: **6**

### gP1SlotSetCodeArray = 0x0201c740 (ewram.inc) -- 7 slots

| slot addr | fn |
|-----------|-----|
| 0x0808ae48 | fn02 |
| 0x0808aff8 | fn04 |
| 0x0808b2c4 | fn09 |
| 0x0808b438 | fn12 |
| 0x0808b51c | fn14 |
| 0x0808b684 | fn16 |
| 0x0808b870 | fn20 |

REF count gP1SlotSetCodeArray: **7**

### gP1ZoneHandCount = 0x0201c4ec (ewram.inc) -- 2 slots

| slot addr | fn |
|-----------|-----|
| 0x0808aff4 | fn04 |
| 0x0808b680 | fn16 |

REF count gP1ZoneHandCount: **2**

### gP1SlotCountBase = 0x0201c4f0 (ewram.inc) -- 1 slot

| slot addr | fn |
|-----------|-----|
| 0x0808b528 | fn14 |

REF count gP1SlotCountBase: **1**

### gDuelFieldSlots = 0x0201c510 (ewram.inc) -- 1 slot

| slot addr | fn |
|-----------|-----|
| 0x0808bb24 | fn25 |

REF count gDuelFieldSlots: **1**

### gP1ChainZoneArray = 0x0201c880 (ewram.inc) -- 1 slot

| slot addr | fn |
|-----------|-----|
| 0x0808bb2c | fn25 |

REF count gP1ChainZoneArray: **1**

### Total REF count: 21+7+6+7+2+1+1+1 = **46**

---

## EQ_SLOTS (CID pool equates)

### NEW CIDs to add to card_info.inc (11 entries, individual grep = 0 hits each):

```
.equ LIGHT_OF_JUDGMENT_CID,              0x00001764  @ Light of Judgment (pw=44595286; card-stats.s card_1549 slot=0x1764); grep 0x1764=0 hits
.equ BECKONING_LIGHT_CID,               0x00001769  @ Beckoning Light (pw=16255442; card-stats.s card_1553 slot=0x1769); grep 0x1769=0 hits
.equ SPIRIT_CALLER_CID,                 0x00001795  @ Spirit Caller (pw=48659020; card-stats.s card_1581 slot=0x1795); grep 0x1795=0 hits
.equ SOUL_REVERSAL_CID,                 0x000017a2  @ Soul Reversal (pw=78864369; card-stats.s card_1593 slot=0x17A2); grep 0x17a2=0 hits
.equ HOWLING_INSECT_CID,                0x000017e5  @ Howling Insect (pw=93107608; card-stats.s card_1650 slot=0x17E5); grep 0x17e5=0 hits
.equ TWO_MAN_CELL_BATTLE_CID,           0x000017f8  @ Two-Man Cell Battle (pw=25578802; card-stats.s card_1669 slot=0x17F8); grep 0x17f8=0 hits
.equ MONSTER_REINCARNATION_CID,         0x00001845  @ Monster Reincarnation (pw=74848038; card-stats.s card_1737 slot=0x1845); grep 0x1845=0 hits
.equ LIGHTEN_THE_LOAD_CID,              0x00001847  @ Lighten the Load (pw=37231841; card-stats.s card_1739 slot=0x1847); grep 0x1847=0 hits
.equ LIGHT_HEX_SEALED_FUSION_CID,       0x00001870  @ The Light - Hex-Sealed Fusion (pw=15717011; card-stats.s card_1777 slot=0x1870); grep 0x1870=0 hits
.equ DARK_HEX_SEALED_FUSION_CID,        0x00001871  @ The Dark - Hex-Sealed Fusion (pw=52101615; card-stats.s card_1778 slot=0x1871); grep 0x1871=0 hits
.equ EARTH_HEX_SEALED_FUSION_CID,       0x00001872  @ The Earth - Hex-Sealed Fusion (pw=88696724; card-stats.s card_1779 slot=0x1872); grep 0x1872=0 hits
```

Total NEW CIDs: **11**

### REUSE CIDs (already in card_info.inc, DO NOT add):
AVATAR_OF_THE_POT_CID(0x1748), MONSTER_GATE_CID(0x175c), ARCHLORD_ZERATO_CID(0x1758),
NINJITSU_ART_OF_TRANSFORMATION_CID(0x1768), SPIRIT_OF_PHARAOH_CID(0x1788),
NUBIAN_GUARD_CID(0x178c), EMISSARY_OF_THE_AFTERLIFE_CID(0x1796), NIGHT_ASSAILANT_CID(0x179a),
THE_FIRST_SARCOPHAGUS_CID(0x17af), HUMAN_WAVE_TACTICS_CID(0x17b2), MASKED_DRAGON_CID(0x17e6),
UFOROID_CID(0x18f4), DARK_FACTORY_MASS_PROD_CID(0x17f1), ABYSSAL_DESIGNATOR_CID(0x17f4),
GRAVEYARD_IN_FOURTH_DIMENSION_CID(0x17f7), BIG_WAVE_SMALL_WAVE_CID(0x17f9),
MAGICIANS_CIRCLE_CID(0x1818), MOKEY_MOKEY_KING_CID(0x183d), BEHEMOTH_KING_CID(0x1864),
POT_OF_GREED_CID(0x12ec), PARASITE_PARACIDE_CID(0x12a1)

### Partner/comparison CID equates in pool:
- 0x0808adcc = POT_OF_GREED_CID(0x12ec) -- fn01 partner (REUSE, in card_info.inc)
- 0x0808aff0 = PARASITE_PARACIDE_CID(0x12a1) -- fn04 FLIP-check (REUSE, in card_info.inc)
- 0x0808b524 = PARASITE_PARACIDE_CID(0x12a1) -- fn14 FLIP-check (REUSE, same slot)

### Scalar pool equates (existing constants, REUSE):
- 0x00000868 = PLAYER_BLOCK_STRIDE (ewram.inc) -- 21 slots across Seg-4e
- 0x000005dc = CARD_FIELD3_THRESHOLD_1500 (card_info.inc) -- 1 slot (fn14 pool 0x0808b520)

### Raw-value pool (no existing const, EOL label only):
- 0x0808b8e4 = 0xbc100000 (fn21 slot sentinel: LSLS slot_word,#19 compare; no named const found in constants/; label raw EQ)

---

## Literal Pool DWord List (createDWord required, all addresses in [0x0808ad8c, 0x0808bb7c))

All pool addresses verified 4-byte aligned (no misalignment issues).

**fn01** (0x0808ad8c): 0x0808adc4, 0x0808adc8, 0x0808adcc
**fn02** (0x0808add0): 0x0808ae40, 0x0808ae44, 0x0808ae48
**fn03** (0x0808ae4c): 0x0808ae90, 0x0808ae94
**fn04** (0x0808ae98): 0x0808afe4, 0x0808afe8, 0x0808afec, 0x0808aff0, 0x0808aff4, 0x0808aff8
**fn05** (0x0808affc): 0x0808b070, 0x0808b074, 0x0808b078
**fn06** (0x0808b07c): 0x0808b120, 0x0808b124, 0x0808b128
**fn07** (0x0808b12c): 0x0808b1a0, 0x0808b1a4, 0x0808b1a8
**fn08** (0x0808b1ac): 0x0808b234, 0x0808b238, 0x0808b23c
**fn09** (0x0808b240): 0x0808b2bc, 0x0808b2c0, 0x0808b2c4
**fn10** (0x0808b2c8): 0x0808b344, 0x0808b348, 0x0808b34c
**fn11** (0x0808b350): 0x0808b3a0, 0x0808b3a4
**fn12** (0x0808b3a8): 0x0808b430, 0x0808b434, 0x0808b438
**fn13** (0x0808b43c): (none -- no LDR PC-relative)
**fn14** (0x0808b454): 0x0808b514, 0x0808b518, 0x0808b51c, 0x0808b520, 0x0808b524, 0x0808b528
**fn15** (0x0808b52c): 0x0808b57c, 0x0808b580
**fn16** (0x0808b584): 0x0808b674, 0x0808b678, 0x0808b67c, 0x0808b680, 0x0808b684
**fn17** (0x0808b688): 0x0808b6d8, 0x0808b6dc
**fn18** (0x0808b6e0): 0x0808b748, 0x0808b74c
**fn19** (0x0808b750): 0x0808b7d0, 0x0808b7d4, 0x0808b7d8
**fn20** (0x0808b7dc): 0x0808b868, 0x0808b86c, 0x0808b870
**fn21** (0x0808b874): 0x0808b8d8, 0x0808b8dc, 0x0808b8e0, 0x0808b8e4
**fn22** (0x0808b8e8): 0x0808b938, 0x0808b93c
**fn23** (0x0808b940): 0x0808b980, 0x0808b984
**fn24** (0x0808b988): 0x0808b9d8, 0x0808b9dc
**fn25** (0x0808b9e0): 0x0808bb20, 0x0808bb24, 0x0808bb28, 0x0808bb2c, 0x0808bb74, 0x0808bb78

Total pool DWORDs: **76** (all 4-byte aligned, verified via Python)

Note: fn21 pool at 0x0808b8e4 = 0xbc100000 is a legitimate 4-byte pool entry at [fn21_end-4]; bytes 00 00 10 bc (LE32 = 0xbc100000).

---

## Disasm Plan (R4)

All 25 real functions are THUMB code. No ROM_INCBIN or .byte blocks remain in this segment -- all bytes are function bodies and literal pools.

Per-function disassembly (25 functions + degenerate exclusions):

| fn | start | end | size | degenerate exclusion |
|----|-------|-----|------|---------------------|
| fn01 | 0x0808ad8c | 0x0808add0 | 0x44 | none |
| fn02 | 0x0808add0 | 0x0808ae4c | 0x7c | none |
| fn03 | 0x0808ae4c | 0x0808ae98 | 0x4c | none |
| fn04 | 0x0808ae98 | 0x0808affc | 0x164 | none |
| fn05 | 0x0808affc | 0x0808b07c | 0x80 | none |
| fn06 | 0x0808b07c | 0x0808b12c | 0xb0 | none |
| fn07 | 0x0808b12c | 0x0808b1ac | 0x80 | none |
| fn08 | 0x0808b1ac | 0x0808b240 | 0x94 | none |
| fn09 | 0x0808b240 | 0x0808b2c8 | 0x88 | none |
| fn10 | 0x0808b2c8 | 0x0808b350 | 0x88 | none |
| fn11 | 0x0808b350 | 0x0808b3a8 | 0x58 | none |
| fn12 | 0x0808b3a8 | 0x0808b43c | 0x94 | exclude 0x0808b40e from entry list |
| fn13 | 0x0808b43c | 0x0808b454 | 0x18 | none |
| fn14 | 0x0808b454 | 0x0808b52c | 0xd8 | none |
| fn15 | 0x0808b52c | 0x0808b584 | 0x58 | none |
| fn16 | 0x0808b584 | 0x0808b688 | 0x104 | exclude 0x0808b58a from entry list |
| fn17 | 0x0808b688 | 0x0808b6e0 | 0x58 | none |
| fn18 | 0x0808b6e0 | 0x0808b750 | 0x70 | none |
| fn19 | 0x0808b750 | 0x0808b7dc | 0x8c | none; 0x0808b798 is mid-BL upper-half not fn entry |
| fn20 | 0x0808b7dc | 0x0808b874 | 0x98 | none |
| fn21 | 0x0808b874 | 0x0808b8e8 | 0x74 | none |
| fn22 | 0x0808b8e8 | 0x0808b940 | 0x58 | none |
| fn23 | 0x0808b940 | 0x0808b988 | 0x48 | exclude 0x0808b95a from entry list |
| fn24 | 0x0808b988 | 0x0808b9e0 | 0x58 | none |
| fn25 | 0x0808b9e0 | 0x0808bb7c | 0x19c | none |

Size sum: 0x44+0x7c+0x4c+0x164+0x80+0xb0+0x80+0x94+0x88+0x88+0x58+0x94+0x18+0xd8+0x58+0x104+0x58+0x70+0x8c+0x98+0x74+0x58+0x48+0x58+0x19c = 0xDF0 = 3568 B. Confirmed matches segment size.

---

## carve 计划 (R7)

No ROM_INCBIN data blocks requiring carve in this segment. All bytes are THUMB code + literal pools belonging to the 25 real functions. No data tables, incbin regions, or pointer tables exist in this range.

---

## §5.1 登记 (Rule 3) -- 0 引用块

No ROM_INCBIN or .byte blocks in Seg-4e. All code; no orphan data regions.

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

- `write_equip_zone_entry_by_substate` (0x0808d88c): referenced from all 25 fns; function name established in Seg-4a/4b/4c/4d; high confidence
- `check_card_pair_allowed` (0x0804ab4c): doc/dev/naming-proposals.csv:line (check_card_pair_allowed); high confidence
- `check_card_has_equip_placement_type` (0x0804ba58): doc/dev/naming-proposals.csv:1062; high confidence
- `check_card_id_is_effect_monster_type_b` (0x0804b0e4): doc/dev/naming-proposals.csv:1051; high confidence
- `get_card_field_summon_restriction` (0x0804b4f4): doc/dev/naming-proposals.csv:1060; high confidence
- `eval_equip_bonus_for_slot` (0x080377b0): doc/dev/naming-proposals.csv:699; high confidence
- `scan_zone_destiny_board_substate_bd` (0x08088a34): doc/dev/naming-proposals.csv:2687; high confidence
- `write_equip_zone_entries_by_lv_card_id` (0x080872e4): doc/dev/naming-proposals.csv:2648; high confidence
- `check_slot_card_can_be_equipped` (0x08033730): doc/dev/naming-proposals.csv:624; high confidence
- `check_card_is_equip_target_eligible` (0x0804bb6c): doc/dev/naming-proposals.csv:1065; high confidence
- `check_card_id_is_equip_excluded_range` (0x0804bc58): doc/dev/naming-proposals.csv:1066; high confidence
- `check_slot_card_equip_criteria_by_state_code` (0x0807f618): doc/dev/naming-proposals.csv:2462; high confidence
- `get_equip_display_type_code_by_card_id` (0x0807f6f0): doc/dev/naming-proposals.csv:2464; high confidence
- `get_equip_display_criteria_code_by_card_and_slot` (0x0807f730): doc/dev/naming-proposals.csv:2465; high confidence
- `gP1ZoneHandCount` (0x0201c4ec): constants/ewram.inc line 232; high confidence
- `gP1SlotCountBase` (0x0201c4f0): constants/ewram.inc line 331; high confidence
- `gDuelFieldSlots` (0x0201c510): constants/ewram.inc line 314; high confidence
- `gP1ChainZoneArray` (0x0201c880): constants/ewram.inc line 336; high confidence
- `find_effect_node_in_zone` (0x0802fd60): doc/dev/naming-proposals.csv:508; high confidence
- `CARD_FIELD3_THRESHOLD_1500` (0x5dc=1500): constants/card_info.inc (fn19 of Seg-4d precedent); high confidence

---

## 求助 (低置信度语义)

fn21 pool 0x0808b8e4 = 0xbc100000: raw slot sentinel value used in `LSLS r0,r0,#19; CMP r0,r1` sequence scanning gP1HandSlotArray. Value 0xbc100000 checks specific bit-fields within a hand slot 32-bit entry. No existing named constant found in constants/. Confidence: med (structural evidence only -- bit-field comparison against sentinel value; card effect semantics of Mokey Mokey King do not reveal what bit pattern 0xbc100000 represents after left-shift-19).

Action: label as raw EQ with ASCII EOL `@ hand slot type sentinel (LSLS #19 compare)`. Do not fabricate a semantic name.
