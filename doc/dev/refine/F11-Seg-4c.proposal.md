# Refine Proposal: F11-Seg-4c  [0x0808962c..0x0808a2ac)

## Segment Survey

- ROM range: `[0x0808962c, 0x0808a2ac)` = 0xC80 bytes (3200 B)
- Source: one-liner `ROM_INCBIN 0x8962c, <size>` (giant block in asm/11, after Seg-4b carved 0x88904..0x8962c)
- Boundary at 0x0808962c = first entry after Seg-4b end; boundary at 0x0808a2ac = next segment start
- Functions: **23 real functions** (27 strong entries - 4 degenerate = 23 real)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools

### Function type: equip zone scan callbacks (same pattern as Seg-4a/4b)

All 23 real functions are equip zone scan callbacks dispatched from the 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

---

## Degenerate Strong Entry Analysis (4 of 27)

| addr | reason | evidence |
|------|--------|---------|
| 0x0808985e | BL instruction at mid-loop in fn05 (0x0808980c..0x08089898). ROM bytes: `f7ad fde9` = BL opcode, not a push prologue. No dispatch table entry points to 0x0808985e+1. fn05 real span = 0x0808980c..0x08089898 (size=0x8c). | bytes f7ad (BL prefix1) + fde9 (BL prefix2); fn05 code continues past without return between fn05_start and 0x0808985e |
| 0x08089a58 | Mid-loop fall-through code inside fn09 (0x080899e8..0x08089aa0). ROM bytes: `1c30 210b` = `mov r0,r6; movs r1,#0xb`. This is the loop continuation after `add r3,r3,r6` at 0x08089a56 -- no branch targets 0x08089a58. No dispatch table entry. | bytes 1c30 (ADD Rd,Rm); fn09 returns at 0x08089a8c (bc01/4700 epilogue); no branch to 0x08089a58 found in scan 0x08089700..0x08089b00 |
| 0x08089e78 | Mid-loop fall-through code inside fn17 (0x08089e44..0x08089ed0). ROM bytes: `04c0 0cc4` = `lsl r0,r0,#19; lsr r4,r0,#19` (bitfield extraction pair). Falls through from `ldr r0,[r3]` at 0x08089e76. No dispatch table entry. fn17 real span = 0x08089e44..0x08089ec4 (code) + pool to 0x08089ed0. | bytes 04c0 0cc4 (bitfield extract pair); fn17 epilogue at 0x08089ebe/ec0 (bc01/4700); pool @0x08089ec4=0x0201c4e0 confirmed |
| 0x0808a28e | Mid-loop code inside fn23 (0x0808a224..0x0808a2ac). ROM bytes: `6800 4285 d3da` = `ldr r0,[r0]; cmp r5,r0; bcc` (backward loop branch). This is the inner-loop ldr+cmp+bcc at end of fn23 loop body. No dispatch table entry. fn23 real span = 0x0808a224..0x0808a29e (code) + pool to 0x0808a2ac. | bytes 6800 (LDR), 4285 (CMP r5,r0), d3da (BCC backward to 0x0808a24a); fn23 epilogue at 0x0808a294..0x0808a29c (bc08/4698/bcf0/bc01/4700) |

---

## Dispatch Table CID Scan (full scan, 305 entries at 0x09e5a128)

| fn | addr | CID(s) | entry indices | card name(s) |
|----|------|--------|--------------|-------------|
| fn01 | 0x0808962c | 0x14ee, 0x1531 | [85], [97] | De-Spell Germ Weapon; Dark Scorpion Burglars |
| fn02 | 0x08089684 | 0x1536 | [99] | Book of Life |
| fn03 | 0x08089760 | 0x153b | [100] | Call of the Mummy |
| fn04 | 0x080897b4 | 0x1562 | [101] | Toon Table of Contents |
| fn05 | 0x0808980c | 0x1534, 0x156a | [98], [102] | Fushioh Richie; Puppet Master |
| fn06 | 0x08089898 | 0x156d | [103] | Lord Poison |
| fn07 | 0x08089928 | 0x1572 | [104] | Hidden Soldier |
| fn08 | 0x08089990 | 0x1579, 0x17c3 | [105], [198] | Monster Relief; Familiar Knight |
| fn09 | 0x080899e8 | 0x157a, 0x1978 | [106], [285] | Machine Duplication; The League of Uniform Nomenclature |
| fn10 | 0x08089aa0 | 0x1585 | [107] | Gravekeeper's Spy |
| fn11 | 0x08089b60 | 0x1590 | [108] | A Cat of Ill Omen |
| fn12 | 0x08089bb8 | 0x159c | [110] | Different Dimension Capsule |
| fn13 | 0x08089c24 | 0x1593, 0x15a1 | [109], [111] | An Owl of Luck; Terraforming |
| fn14 | 0x08089c7c | 0x15a3 | [112] | Metamorphosis |
| fn15 | 0x08089d08 | 0x15ac | [113] | Rite of Spirit |
| fn16 | 0x08089d94 | 0x15b5 | [114] | Rope of Spirit |
| fn17 | 0x08089e44 | 0x15b9 | [116] | Goblin Zombie |
| fn18 | 0x08089ed0 | 0x15e2 | [122] | Frontline Base |
| fn19 | 0x08089f34 | 0x15e6 | [123] | Autonomous Action Unit |
| fn20 | 0x08089fb8 | 0x15ed | [124] | Tribute Doll |
| fn21 | 0x0808a010 | 0x1610, 0x1611, 0x167d, 0x1713, 0x195c, 0x19b1 | [125],[126],[145],[172],[279],[294] | Skilled White Magician; Skilled Dark Magician; Knight's Title; Dedication Through Light and Dark; Bonding - H2O; Photon Generator Unit |
| fn22 | 0x0808a190 | 0x1612 | [127] | Apprentice Magician |
| fn23 | 0x0808a224 | 0x1619 | [128] | Magical Scientist |

Size sanity check: sum of all 23 fn spans = 0x0808a2ac - 0x0808962c = 0xC80 = 3200 B (confirmed).

---

## Function Naming Table (23 real functions)

Substate semantics (from existing plate for write_equip_zone_entry_by_substate):
- 0xb = field-spell zone type B
- 0xc = chain zone type C
- 0xd = monster zone type D
- 0xe = hand slot type E
- 0xf = graveyard type F

### fn01: 0x0808962c  size=0x058 (88 B)
- CID(s): 0x14ee (De-Spell Germ Weapon), 0x1531 (Dark Scorpion Burglars)
- Dispatch entries: [85], [97]
- Body: push {r4,r5,r6,r7,lr}; scan gP1LifePoints monster zone at offset +0x10;
  get_card_extended_stat_field6 (0x080eedf8); cmp r0,#0x16 (RACE_SPELL=22); write substate_d
- BL targets: 0x080eedf8 (get_card_extended_stat_field6), 0x0808d88c
- Pool: 0x0808967c=gP1LifePoints, 0x08089680=PLAYER_BLOCK_STRIDE
- CID status: DE_SPELL_GERM_WEAPON_CID REUSE; DARK_SCORPION_BURGLARS_CID REUSE
- Substate: 0xd
- Proposed name: `scan_zone_dark_scorpion_burglars_group_substate_d`
- Confidence: high (body: field6==0x16 gate; Dark Scorpion Burglars is the primary of the 5-member group; De-Spell Germ Weapon is dispatched alongside all Dark Scorpion members; write_d = monster zone)
- ASCII plate: `Equip zone scan callback for Dark Scorpion group: De-Spell Germ Weapon (DE_SPELL_GERM_WEAPON_CID=0x14ee, pw=14571844), Dark Scorpion Burglars (DARK_SCORPION_BURGLARS_CID=0x1531, pw=86148577). r0=player_id. Gate: get_card_extended_stat_field6==0x16 (RACE_SPELL); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [85,97].`

### fn02: 0x08089684  size=0x0dc (220 B)
- CID: 0x1536 (Book of Life)
- Dispatch entry: [99]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; TWO-LOOP structure:
  loop1 scans gP1LifePoints monster zone at offset +0x14; get_card_extended_stat_field6;
  check field6; check_zone_slot_equip_eligible (0x08037434); write substate_e;
  loop2 scans gP1HandSlotArray; check_card_field5_is_nonzero; check_zone_slot_equip_eligible; write substate_e
- BL targets: 0x080eedf8, 0x08037434 (check_zone_slot_equip_eligible), 0x0804ad48, 0x0808d88c (x2)
- Pool: 0x080896f0=gP1LifePoints, 0x080896f4=PLAYER_BLOCK_STRIDE, 0x080896f8=gP1HandSlotArray,
        0x08089758=gP1LifePoints, 0x0808975c=PLAYER_BLOCK_STRIDE
- CID: REUSE BOOK_OF_LIFE_CID
- Substate: 0xe (both loops)
- Proposed name: `scan_zone_book_of_life_substate_e`
- Confidence: high (body: two-loop hand zone scan + field5/field6/equip_eligible gates; Book of Life targets zombie monsters on field and in hand)
- ASCII plate: `Equip zone scan callback for Book of Life (BOOK_OF_LIFE_CID=0x1536, pw=02204140). r0=player_id. Two loops: (1) gP1LifePoints+STRIDE monster zone at+0x14 -- field6 + equip_eligible gate; (2) gP1HandSlotArray -- field5 + equip_eligible gate. Both write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [99].`

### fn03: 0x08089760  size=0x054 (84 B)
- CID: 0x153b (Call of the Mummy)
- Dispatch entry: [100]
- Body: push {r4,r5,r6,r7,lr}; scan gP1FieldArrayCBase field spell zone;
  check_card_has_equip_placement_type (0x0804ba58);
  check_card_is_equip_target_eligible (0x0804bb6c);
  get_card_extended_stat_field6 (0x080eedf8); write substate_b
- BL targets: 0x0804ba58 (check_card_has_equip_placement_type), 0x0804bb6c, 0x080eedf8, 0x0808d88c
- Pool: 0x080897ac=PLAYER_BLOCK_STRIDE, 0x080897b0=gP1FieldArrayCBase
- CID: REUSE CALL_OF_THE_MUMMY_CID
- Substate: 0xb
- Proposed name: `scan_zone_call_of_the_mummy_substate_b`
- Confidence: high (body: field spell zone scan + equip_placement + equip_eligible + field6 gate; Call of the Mummy special-summons Zombie from hand to field)
- ASCII plate: `Equip zone scan callback for Call of the Mummy (CALL_OF_THE_MUMMY_CID=0x153b, pw=04291579). r0=player_id. Gate: check_card_has_equip_placement_type + check_card_is_equip_target_eligible + get_card_extended_stat_field6 via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [100].`

### fn04: 0x080897b4  size=0x058 (88 B)
- CID: 0x1562 (Toon Table of Contents)
- Dispatch entry: [101]
- Body: push {r4,r5,r6,r7,lr}; scan gP1LifePoints monster zone;
  check_card_is_toon_type (0x0804ae40); write substate_d (no further gate)
- BL targets: 0x0804ae40 (check_card_is_toon_type), 0x0808d88c
- Pool: 0x08089804=gP1LifePoints, 0x08089808=PLAYER_BLOCK_STRIDE
- CID: 0x1562 NEW (0 hits in card_info.inc -- individual grep confirmed below)
- Substate: 0xd
- Proposed name: `scan_zone_toon_table_of_contents_substate_d`
- Confidence: high (body: is_toon_type gate + write_d; Toon Table of Contents fetches a Toon card from deck)
- ASCII plate: `Equip zone scan callback for Toon Table of Contents (CID=0x1562, pw=89997728). r0=player_id. Gate: check_card_is_toon_type; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) via gP1LifePoints monster zone scan. Dispatched from write table entry [101].`

### fn05: 0x0808980c  size=0x08c (140 B)  [spans 0x0808985e degenerate mid-loop]
- CID(s): 0x1534 (Fushioh Richie), 0x156a (Puppet Master)
- Dispatch entries: [98], [102]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints monster zone at +0x14 offset;
  get_card_extended_stat_field6 (0x080eedf8); check_zone_slot_equip_eligible (0x08037434);
  write substate_e; then loops gP1HandSlotArray (second section)
- BL targets: 0x080eedf8, 0x08037434, 0x0808d88c
- Pool: 0x0808988c=gP1LifePoints, 0x08089890=PLAYER_BLOCK_STRIDE, 0x08089894=gP1HandSlotArray
- CID status: FUSHIOH_RICHIE_CID REUSE; PUPPET_MASTER_CID REUSE
- Substate: 0xe
- Proposed name: `scan_zone_fushioh_richie_puppet_master_group_substate_e`
- Confidence: high (body: field6 gate + equip_eligible; both require specific fiend/zombie types in hand zone; addr 0x0808985e is degenerate BL mid-loop)
- ASCII plate: `Equip zone scan callback for Fushioh Richie/Puppet Master group: Fushioh Richie (FUSHIOH_RICHIE_CID=0x1534, pw=38285847), Puppet Master (PUPPET_MASTER_CID=0x156a, pw=40933827). Gate: get_card_extended_stat_field6 + check_zone_slot_equip_eligible via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x0808985e is degenerate BL mid-loop. Dispatched from write table entries [98,102].`

### fn06: 0x08089898  size=0x090 (144 B)
- CID: 0x156d (Lord Poison)
- Dispatch entry: [103]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints + gP1HandSlotArray;
  get_card_extended_stat_field6 (0x080eedf8); check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x080eedf8, 0x08037434, 0x0808d88c
- Pool: 0x0808991c=gP1LifePoints, 0x08089920=PLAYER_BLOCK_STRIDE, 0x08089924=gP1HandSlotArray
- CID: REUSE LORD_POISON_CID
- Substate: 0xe
- Proposed name: `scan_zone_lord_poison_substate_e`
- Confidence: high (body: field6 + equip_eligible + hand zone scan; Lord Poison gains ATK from Zombie in GY)
- ASCII plate: `Equip zone scan callback for Lord Poison (LORD_POISON_CID=0x156d, pw=02598051). r0=player_id. Gate: get_card_extended_stat_field6 + check_zone_slot_equip_eligible via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [103].`

### fn07: 0x08089928  size=0x068 (104 B)
- CID: 0x1572 (Hidden Soldier)
- Dispatch entry: [104]
- Body: push {r4,r5,r6,r7,lr}; scan gP1FieldArrayCBase field spell zone;
  check_card_stat_field7_equals (0x08030b70); eval_equip_bonus_for_slot (0x080377b0);
  eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x08030b70 (check_card_stat_field7_equals), 0x080377b0, 0x0803bba4, 0x0808d88c
- Pool: 0x08089988=PLAYER_BLOCK_STRIDE, 0x0808998c=gP1FieldArrayCBase
- CID: REUSE HIDDEN_SOLDIER_CID
- Substate: 0xb
- Proposed name: `scan_zone_hidden_soldier_substate_b`
- Confidence: high (body: field7 + equip_bonus + placement gates; Hidden Soldier is an equip target in field spell zone)
- ASCII plate: `Equip zone scan callback for Hidden Soldier (HIDDEN_SOLDIER_CID=0x1572, pw=02348149). r0=player_id. Gate: check_card_stat_field7_equals + eval_equip_bonus_for_slot + eval_equip_placement_full_check via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [104].`

### fn08: 0x08089928  [corrected: 0x08089990]  size=0x058 (88 B)
**Note: fn08 starts at 0x08089990.**
- CID(s): 0x1579 (Monster Relief), 0x17c3 (Familiar Knight)
- Dispatch entries: [105], [198]
- Body: push {r4,r5,r6,r7,lr}; scan gP1FieldArrayCBase; eval_equip_bonus_for_slot (0x080377b0);
  eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x080377b0, 0x0803bba4, 0x0808d88c
- Pool: 0x080899e0=PLAYER_BLOCK_STRIDE, 0x080899e4=gP1FieldArrayCBase
- CID status: MONSTER_RELIEF_CID REUSE; FAMILIAR_KNIGHT_CID REUSE
- Substate: 0xb
- Proposed name: `scan_zone_monster_relief_familiar_knight_group_substate_b`
- Confidence: high (body: equip_bonus + placement; field spell zone; both cards swap monsters or have field spell zone conditions)
- ASCII plate: `Equip zone scan callback for Monster Relief/Familiar Knight group: Monster Relief (MONSTER_RELIEF_CID=0x1579, pw=72089094), Familiar Knight (FAMILIAR_KNIGHT_CID=0x17c3, pw=00423705). Gate: eval_equip_bonus_for_slot + eval_equip_placement_full_check via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entries [105,198].`

### fn09: 0x080899e8  size=0x0b8 (184 B)  [spans 0x08089a58 degenerate mid-loop]
- CID(s): 0x157a (Machine Duplication), 0x1978 (The League of Uniform Nomenclature)
- Dispatch entries: [106], [285]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1SlotSetCodeArray (zone_query_hand_tag_12a1 filter);
  check_card_field5_is_nonzero (0x0804ad48); eval_equip_placement_full_check (0x0803bba4);
  find_effect_node_in_zone (0x0802fd60); check_card_pair_allowed (0x0804ab4c); write substate_d;
  addr 0x08089a58 is degenerate (fall-through continuation of loop body, bytes 1c30 210b)
- BL targets: 0x0804ad48, 0x0803bba4, 0x0802fd60, 0x0804ab4c, 0x0808d88c
- Pool: 0x08089a90=gP1LifePoints, 0x08089a94=PLAYER_BLOCK_STRIDE, 0x08089a98=gP1SlotSetCodeArray, 0x08089a9c=zone_query_hand_tag_12a1
- CID status: 0x157a NEW (Machine Duplication, 0 hits); 0x1978 NEW (League of Uniform Nomenclature, 0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_machine_duplication_group_substate_d`
- Confidence: high (body: field5 + placement + pair_allowed gate; Machine Duplication targets machine-type monsters; League of Uniform Nomenclature requires 3 normal monsters of same type; shared check_card_pair_allowed gate)
- ASCII plate: `Equip zone scan callback for Machine Duplication group: Machine Duplication (CID=0x157a, pw=63995093), League of Uniform Nomenclature (CID=0x1978, pw=55008284). Gate: check_card_field5_is_nonzero + eval_equip_placement + find_effect_node_in_zone + check_card_pair_allowed via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x08089a58 is degenerate fall-through. Dispatched from write table entries [106,285].`

### fn10: 0x08089aa0  size=0x0c0 (192 B)
- CID: 0x1585 (Gravekeeper's Spy)
- Dispatch entry: [107]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1SlotSetCodeArray (zone_query_hand_tag_12a1 filter);
  check_card_field5_is_nonzero; get_card_extended_stat_field3_raw (0x080eef44) comparing <= 0x5dc (1500 ATK);
  find_effect_node_in_zone; eval_equip_placement_full_check; check_card_is_gravekeeper (0x0804af60); write substate_d
- BL targets: 0x0804ad48, 0x080eef44, 0x0802fd60, 0x0803bba4, 0x0804af60, 0x0808d88c
- Pool: 0x08089b4c=gP1LifePoints, 0x08089b50=PLAYER_BLOCK_STRIDE, 0x08089b54=gP1SlotSetCodeArray,
        0x08089b58=CARD_FIELD3_THRESHOLD_1500 (0x5dc), 0x08089b5c=zone_query_hand_tag_12a1
- CID status: 0x1585 NEW (Gravekeeper's Spy, 0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_gravekeeper_spy_substate_d`
- Confidence: high (body: gravekeeper check + ATK<=1500 + placement gate; Gravekeeper's Spy flip-summons another Gravekeeper from deck)
- ASCII plate: `Equip zone scan callback for Gravekeeper's Spy (CID=0x1585, pw=24317029). r0=player_id. Multi-gate: check_card_field5_is_nonzero + get_card_extended_stat_field3_raw<=CARD_FIELD3_THRESHOLD_1500(0x5dc) + find_effect_node_in_zone + eval_equip_placement + check_card_is_gravekeeper via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [107].`

### fn11: 0x08089b60  size=0x058 (88 B)
- CID: 0x1590 (A Cat of Ill Omen)
- Dispatch entry: [108]
- Body: push {r4,r5,r6,r7,lr}; scan gP1LifePoints monster zone;
  get_card_extended_stat_field6 (0x080eedf8); write substate_d
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x08089bb0=gP1LifePoints, 0x08089bb4=PLAYER_BLOCK_STRIDE
- CID: REUSE A_CAT_OF_ILL_OMEN_CID
- Substate: 0xd
- Proposed name: `scan_zone_a_cat_of_ill_omen_substate_d`
- Confidence: high (body: field6 gate + write_d; A Cat of Ill Omen places Spell Counter when flipped)
- ASCII plate: `Equip zone scan callback for A Cat of Ill Omen (A_CAT_OF_ILL_OMEN_CID=0x1590, pw=00808676). r0=player_id. Gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) via gP1LifePoints monster zone scan. Dispatched from write table entry [108].`

### fn12: 0x08089bb8  size=0x06c (108 B)
- CID: 0x159c (Different Dimension Capsule)
- Dispatch entry: [110]
- Body: push {r4,r5,r6,r7,lr}; scan gP1LifePoints monster zone via zone_query_hand_tag_12a1;
  find_effect_node_in_zone (0x0802fd60); write substate_d
- BL targets: 0x0802fd60, 0x0808d88c
- Pool: 0x08089c18=gP1LifePoints, 0x08089c1c=PLAYER_BLOCK_STRIDE, 0x08089c20=zone_query_hand_tag_12a1
- CID: REUSE DIFFERENT_DIMENSION_CAPSULE_CID
- Substate: 0xd
- Proposed name: `scan_zone_different_dimension_capsule_substate_d`
- Confidence: high (body: find_effect_node_in_zone gate + write_d; D.D. Capsule removes card from game and retrieves after 2 turns)
- ASCII plate: `Equip zone scan callback for Different Dimension Capsule (DIFFERENT_DIMENSION_CAPSULE_CID=0x159c, pw=68468459). r0=player_id. Gate: find_effect_node_in_zone via gP1LifePoints[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [110].`

### fn13: 0x08089c24  size=0x058 (88 B)
- CID(s): 0x1593 (An Owl of Luck), 0x15a1 (Terraforming)
- Dispatch entries: [109], [111]
- Body: push {r4,r5,r6,r7,lr}; scan gP1LifePoints monster zone;
  get_card_extended_stat_field9 (0x080eee7c); write substate_d
- BL targets: 0x080eee7c (get_card_extended_stat_field9), 0x0808d88c
- Pool: 0x08089c74=gP1LifePoints, 0x08089c78=PLAYER_BLOCK_STRIDE
- CID status: 0x1593 NEW (An Owl of Luck, 0 hits); 0x15a1 NEW (Terraforming, 0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_owl_of_luck_terraforming_group_substate_d`
- Confidence: high (body: field9 gate; An Owl of Luck and Terraforming both search for field spell cards from deck; shared field9 property check)
- ASCII plate: `Equip zone scan callback for Owl of Luck/Terraforming group: An Owl of Luck (CID=0x1593, pw=23927567), Terraforming (CID=0x15a1, pw=73628505). Gate: get_card_extended_stat_field9 via gP1LifePoints monster zone; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [109,111].`

### fn14: 0x08089c7c  size=0x08c (140 B)
- CID: 0x15a3 (Metamorphosis)
- Dispatch entry: [112]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints + gP1ChainZoneArray;
  check_card_is_equip_target_eligible (0x0804bb6c);
  check_card_id_is_equip_excluded_range (0x0804bc58);
  get_card_extended_stat_field7 (0x080eee50); write substate_c
- BL targets: 0x0804bb6c, 0x0804bc58, 0x080eee50, 0x0808d88c
- Pool: 0x08089cfc=gP1LifePoints, 0x08089d00=PLAYER_BLOCK_STRIDE, 0x08089d04=gP1ChainZoneArray
- CID: REUSE METAMORPHOSIS_CID
- Substate: 0xc
- Proposed name: `scan_zone_metamorphosis_substate_c`
- Confidence: high (body: equip_eligible + excl_range + field7 + chain zone scan; Metamorphosis transforms a monster into a Fusion monster)
- ASCII plate: `Equip zone scan callback for Metamorphosis (METAMORPHOSIS_CID=0x15a3, pw=46411259). r0=player_id. Gate: check_card_is_equip_target_eligible + check_card_id_is_equip_excluded_range + get_card_extended_stat_field7 via gP1ChainZoneArray; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatched from write table entry [112].`

### fn15: 0x08089d08  size=0x08c (140 B)
- CID: 0x15ac (Rite of Spirit)
- Dispatch entry: [113]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints + gP1HandSlotArray;
  check_card_field5_is_nonzero (0x0804ad48);
  check_zone_slot_equip_eligible (0x08037434);
  check_card_is_gravekeeper (0x0804af60); write substate_e
- BL targets: 0x0804ad48, 0x08037434, 0x0804af60, 0x0808d88c
- Pool: 0x08089d88=gP1LifePoints, 0x08089d8c=PLAYER_BLOCK_STRIDE, 0x08089d90=gP1HandSlotArray
- CID: REUSE RITE_OF_SPIRIT_CID
- Substate: 0xe
- Proposed name: `scan_zone_rite_of_spirit_substate_e`
- Confidence: high (body: field5 + equip_eligible + gravekeeper check + hand zone scan; Rite of Spirit special-summons a Gravekeeper from GY)
- ASCII plate: `Equip zone scan callback for Rite of Spirit (RITE_OF_SPIRIT_CID=0x15ac, pw=30450531). r0=player_id. Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible + check_card_is_gravekeeper via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [113].`

### fn16: 0x08089d94  size=0x0b0 (176 B)
- CID: 0x15b5 (Rope of Spirit)
- Dispatch entry: [114]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1SlotSetCodeArray (zone_query_hand_tag_12a1 filter);
  check_card_field5_is_nonzero; find_effect_node_in_zone; eval_equip_placement_full_check;
  get_card_extended_stat_field7 (0x080eee50); write substate_d
- BL targets: 0x0804ad48, 0x0802fd60, 0x0803bba4, 0x080eee50, 0x0808d88c
- Pool: 0x08089e34=gP1LifePoints, 0x08089e38=PLAYER_BLOCK_STRIDE, 0x08089e3c=gP1SlotSetCodeArray, 0x08089e40=zone_query_hand_tag_12a1
- CID: REUSE ROPE_OF_SPIRIT_CID
- Substate: 0xd
- Proposed name: `scan_zone_rope_of_spirit_substate_d`
- Confidence: high (body: field5 + find_node + placement + field7 gate; Rope of Spirit special-summons a Spirit monster from hand)
- ASCII plate: `Equip zone scan callback for Rope of Spirit (ROPE_OF_SPIRIT_CID=0x15b5, pw=47025825). r0=player_id. Gate: check_card_field5_is_nonzero + find_effect_node_in_zone + eval_equip_placement + get_card_extended_stat_field7 via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [114].`

### fn17: 0x08089e44  size=0x08c (140 B)  [spans 0x08089e78 degenerate mid-loop]
- CID: 0x15b9 (Goblin Zombie)
- Dispatch entry: [116]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints + gP1SlotSetCodeArray;
  check_card_field5_is_nonzero; get_card_extended_stat_field6 (0x080eedf8);
  get_card_extended_stat_field4_raw (0x080eef70); write substate_d;
  addr 0x08089e78 is degenerate (mid-loop bitfield extraction, bytes 04c0 0cc4)
- BL targets: 0x0804ad48, 0x080eedf8, 0x080eef70, 0x0808d88c
- Pool: 0x08089ec4=gP1LifePoints, 0x08089ec8=PLAYER_BLOCK_STRIDE, 0x08089ecc=gP1SlotSetCodeArray
- CID status: 0x15b9 NEW (Goblin Zombie, 0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_goblin_zombie_substate_d`
- Confidence: high (body: field5 + field6 + field4_raw gates; Goblin Zombie sends a Zombie from deck to GY on destruction; addr 0x08089e78 is degenerate bitfield mid-loop)
- ASCII plate: `Equip zone scan callback for Goblin Zombie (CID=0x15b9, pw=63665875). r0=player_id. Gate: check_card_field5_is_nonzero + get_card_extended_stat_field6 + get_card_extended_stat_field4_raw via gP1SlotSetCodeArray; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x08089e78 is degenerate mid-loop bitfield pair. Dispatched from write table entry [116].`

### fn18: 0x08089ed0  size=0x064 (100 B)
- CID: 0x15e2 (Frontline Base)
- Dispatch entry: [122]
- Body: push {r4,r5,r6,r7,lr}; scan gP1FieldArrayCBase field spell zone;
  eval_equip_bonus_for_slot (0x080377b0); eval_equip_placement_full_check (0x0803bba4);
  check_card_stat_field8_is_8 (0x0804ae2c); write substate_b
- BL targets: 0x080377b0, 0x0803bba4, 0x0804ae2c (check_card_stat_field8_is_8), 0x0808d88c
- Pool: 0x08089f2c=PLAYER_BLOCK_STRIDE, 0x08089f30=gP1FieldArrayCBase
- CID status: 0x15e2 NEW (Frontline Base, 0 hits)
- Substate: 0xb
- Proposed name: `scan_zone_frontline_base_substate_b`
- Confidence: high (body: equip_bonus + placement + field8==8 (Union type) gate; Frontline Base special-summons Union monsters)
- ASCII plate: `Equip zone scan callback for Frontline Base (CID=0x15e2, pw=46181000). r0=player_id. Gate: eval_equip_bonus_for_slot + eval_equip_placement_full_check + check_card_stat_field8_is_8 (Union type) via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [122].`

### fn19: 0x08089f34  size=0x084 (132 B)
- CID: 0x15e6 (Autonomous Action Unit)
- Dispatch entry: [123]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints + gP1HandSlotArray;
  check_card_field5_is_nonzero (0x0804ad48); check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x08037434, 0x0808d88c
- Pool: 0x08089fac=gP1LifePoints, 0x08089fb0=PLAYER_BLOCK_STRIDE, 0x08089fb4=gP1HandSlotArray
- CID: REUSE AUTONOMOUS_ACTION_UNIT_CID
- Substate: 0xe
- Proposed name: `scan_zone_autonomous_action_unit_substate_e`
- Confidence: high (body: field5 + equip_eligible + hand zone scan; Autonomous Action Unit special-summons a monster from opponent's GY)
- ASCII plate: `Equip zone scan callback for Autonomous Action Unit (AUTONOMOUS_ACTION_UNIT_CID=0x15e6, pw=80256062). r0=player_id. Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible via gP1HandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [123].`

### fn20: 0x08089fb8  size=0x058 (88 B)
- CID: 0x15ed (Tribute Doll)
- Dispatch entry: [124]
- Body: push {r4,r5,r6,r7,lr}; scan gP1FieldArrayCBase field spell zone;
  eval_equip_bonus_for_slot (0x080377b0); eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x080377b0, 0x0803bba4, 0x0808d88c
- Pool: 0x0808a008=PLAYER_BLOCK_STRIDE, 0x0808a00c=gP1FieldArrayCBase
- CID status: 0x15ed NEW (Tribute Doll, 0 hits)
- Substate: 0xb
- Proposed name: `scan_zone_tribute_doll_substate_b`
- Confidence: high (body: equip_bonus + placement + field spell zone scan; Tribute Doll special-summons a Level 7+ monster)
- ASCII plate: `Equip zone scan callback for Tribute Doll (CID=0x15ed, pw=02903036). r0=player_id. Gate: eval_equip_bonus_for_slot + eval_equip_placement_full_check via gP1FieldArrayCBase; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entry [124].`

### fn21: 0x0808a010  size=0x180 (384 B)
- CID(s): 0x1610 (Skilled White Magician), 0x1611 (Skilled Dark Magician), 0x167d (Knight's Title), 0x1713 (Dedication Through Light and Dark), 0x195c (Bonding - H2O), 0x19b1 (Photon Generator Unit)
- Dispatch entries: [125],[126],[145],[172],[279],[294]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; CID-dispatch table at start comparing input r1
  against 0x167d/0x195c/0x1713/0x19b1 (KNIGHTS_TITLE / BONDING_H2O / DEDICATION / PHOTON_GEN);
  loads partner CID into r8 (e.g. 0x167d->0x167c DM Knight, 0x1713->0x0fc9 DM alt, 0x195c->0x16f8 DM of Chaos, 0x19b1->0x19a9 Cyber Laser Dragon);
  then scans gP1LifePoints via count_field_copies_of_card (0x0803279c);
  THREE scan loops with different zone offsets (+0x10/+0x14/+0xc), calling write substate_d/e/b
- BL targets: 0x0803279c (count_field_copies_of_card), 0x0804ab4c (check_card_pair_allowed), 0x0808d88c (x3)
- Pool: 0x0808a030=KNIGHTS_TITLE_CID(0x167d), 0x0808a048=BONDING_H2O_CID(0x195c),
        0x0808a04c=DEDICATION_THROUGH_LIGHT_DARK_CID(0x1713), 0x0808a058=PHOTON_GENERATOR_UNIT_CID(0x19b1),
        0x0808a064=BUSTER_BLADER_CID(0x1377), 0x0808a06c=DARK_MAGICIAN_CID_0FC9(0x0fc9),
        0x0808a078=0x167c(Dark Magician Knight), 0x0808a080=DARK_MAGICIAN_OF_CHAOS_CID(0x16f8),
        0x0808a08c=WATER_DRAGON_CID(0x1951), 0x0808a180=CYBER_LASER_DRAGON_CID(0x19a9),
        0x0808a184=gP1LifePoints, 0x0808a188=PLAYER_BLOCK_STRIDE, 0x0808a18c=NECROVALLEY_CID(0x159d)
- CID status: SKILLED_WHITE_MAGICIAN_CID REUSE; SKILLED_DARK_MAGICIAN_CID REUSE;
  KNIGHTS_TITLE_CID REUSE; DEDICATION_THROUGH_LIGHT_DARK_CID REUSE;
  0x195c NEW (Bonding - H2O); PHOTON_GENERATOR_UNIT_CID REUSE
- Substates: 0xd (loop1), 0xe (loop2), 0xb (loop3)
- Proposed name: `scan_zone_magic_evolution_group_substate_deb`
- Confidence: high (body: CID dispatch + partner check via count_field_copies_of_card + three-zone scan; all 6 CIDs are spell/effect cards requiring specific monster evolutions or bonds on field; pool contains their partner monster CIDs as comparison targets)
- ASCII plate: `Equip zone scan callback for magic evolution group (6 CIDs): Skilled White Magician(SKILLED_WHITE_MAGICIAN_CID=0x1610), Skilled Dark Magician(SKILLED_DARK_MAGICIAN_CID=0x1611), Knight's Title(KNIGHTS_TITLE_CID=0x167d), Dedication Through Light+Dark(DEDICATION_THROUGH_LIGHT_DARK_CID=0x1713), Bonding-H2O(CID=0x195c,pw=45898858), Photon Generator Unit(PHOTON_GENERATOR_UNIT_CID=0x19b1). CID-dispatch then partner CID load(DM Knight 0x167c/DM-of-Chaos 0x16f8/Cyber-Laser 0x19a9). Three loops write substate d/e/b. Dispatched from write table entries [125,126,145,172,279,294].`
- Note on plate length: 499 chars (within 500 limit).

### fn22: 0x0808a190  size=0x094 (148 B)
- CID: 0x1612 (Apprentice Magician)
- Dispatch entry: [127]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1SlotSetCodeArray (zone_query_hand_tag_12a1 filter);
  check_card_field5_is_nonzero; eval_equip_placement_full_check (0x0803bba4);
  get_card_extended_stat_field6 (0x080eedf8); get_card_extended_stat_field7 (0x080eee50); write substate_d
- BL targets: 0x0804ad48, 0x0803bba4, 0x080eedf8, 0x080eee50, 0x0808d88c
- Pool: 0x0808a218=gP1LifePoints, 0x0808a21c=PLAYER_BLOCK_STRIDE, 0x0808a220=gP1SlotSetCodeArray
- CID status: 0x1612 NEW (Apprentice Magician, 0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_apprentice_magician_substate_d`
- Confidence: high (body: field5 + placement + field6 + field7 gates; Apprentice Magician places Spell Counter on Spellcaster; monster zone scan)
- ASCII plate: `Equip zone scan callback for Apprentice Magician (CID=0x1612, pw=09156135). r0=player_id. Gate: check_card_field5_is_nonzero + eval_equip_placement_full_check + get_card_extended_stat_field6 + get_card_extended_stat_field7 via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [127].`

### fn23: 0x0808a224  size=0x088 (136 B)  [spans 0x0808a28e degenerate mid-loop]
- CID: 0x1619 (Magical Scientist)
- Dispatch entry: [128]
- Body: push {r4,r5,r6,r7,lr} + high-reg push; scan gP1LifePoints + gP1ChainZoneArray;
  check_card_is_equip_target_eligible (0x0804bb6c);
  check_card_id_is_equip_excluded_range (0x0804bc58);
  get_card_extended_stat_field7 (0x080eee50); write substate_c;
  addr 0x0808a28e is degenerate (mid-loop ldr+cmp+bcc backward, bytes 6800 4285 d3da)
- BL targets: 0x0804bb6c, 0x0804bc58, 0x080eee50, 0x0808d88c
- Pool: 0x0808a2a0=gP1LifePoints, 0x0808a2a4=PLAYER_BLOCK_STRIDE, 0x0808a2a8=gP1ChainZoneArray
- CID: REUSE MAGICAL_SCIENTIST_CID
- Substate: 0xc
- Proposed name: `scan_zone_magical_scientist_substate_c`
- Confidence: high (body: equip_eligible + excl_range + field7 + chain zone; Magical Scientist special-summons Fusion monsters for LP; addr 0x0808a28e is degenerate backward-branch mid-loop)
- ASCII plate: `Equip zone scan callback for Magical Scientist (MAGICAL_SCIENTIST_CID=0x1619, pw=34206604). r0=player_id. Gate: check_card_is_equip_target_eligible + check_card_id_is_equip_excluded_range + get_card_extended_stat_field7 via gP1ChainZoneArray; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Addr 0x0808a28e is degenerate mid-loop bcc backward. Dispatched from write table entry [128].`

---

## REF_SLOTS (createDWordWithRef plan)

Per Seg-4a/4b precedent: every pool DWord holding an EWRAM address gets
createDWordWithRef + RENAME to export as `.word gP1LifePoints` etc.

### gP1LifePoints = 0x0201c4e0 (ewram.inc) -- 19 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x0808967c | fn01 | ptr_lp_8967c |
| 0x080896f0 | fn02 | ptr_lp_896f0 |
| 0x08089758 | fn02 | ptr_lp_89758 |
| 0x08089804 | fn04 | ptr_lp_89804 |
| 0x0808988c | fn05 | ptr_lp_8988c |
| 0x0808991c | fn06 | ptr_lp_8991c |
| 0x08089a90 | fn09 | ptr_lp_89a90 |
| 0x08089b4c | fn10 | ptr_lp_89b4c |
| 0x08089bb0 | fn11 | ptr_lp_89bb0 |
| 0x08089c18 | fn12 | ptr_lp_89c18 |
| 0x08089c74 | fn13 | ptr_lp_89c74 |
| 0x08089cfc | fn14 | ptr_lp_89cfc |
| 0x08089d88 | fn15 | ptr_lp_89d88 |
| 0x08089e34 | fn16 | ptr_lp_89e34 |
| 0x08089ec4 | fn17 | ptr_lp_89ec4 |
| 0x08089fac | fn19 | ptr_lp_89fac |
| 0x0808a184 | fn21 | ptr_lp_8a184 |
| 0x0808a218 | fn22 | ptr_lp_8a218 |
| 0x0808a2a0 | fn23 | ptr_lp_8a2a0 |

REF count gP1LifePoints: **19**

### gP1SlotSetCodeArray = 0x0201c740 (ewram.inc) -- 5 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x08089a98 | fn09 | ptr_sca_89a98 |
| 0x08089b54 | fn10 | ptr_sca_89b54 |
| 0x08089e3c | fn16 | ptr_sca_89e3c |
| 0x08089ecc | fn17 | ptr_sca_89ecc |
| 0x0808a220 | fn22 | ptr_sca_8a220 |

REF count gP1SlotSetCodeArray: **5**

### gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 5 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x080896f8 | fn02 | ptr_hsa_896f8 |
| 0x08089894 | fn05 | ptr_hsa_89894 |
| 0x08089924 | fn06 | ptr_hsa_89924 |
| 0x08089d90 | fn15 | ptr_hsa_89d90 |
| 0x08089fb4 | fn19 | ptr_hsa_89fb4 |

REF count gP1HandSlotArray: **5**

### gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 5 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x080897b0 | fn03 | ptr_fac_897b0 |
| 0x0808998c | fn07 | ptr_fac_8998c |
| 0x080899e4 | fn08 | ptr_fac_899e4 |
| 0x08089f30 | fn18 | ptr_fac_89f30 |
| 0x0808a00c | fn20 | ptr_fac_8a00c |

REF count gP1FieldArrayCBase: **5**

### gP1ChainZoneArray = 0x0201c880 (ewram.inc) -- 2 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x08089d04 | fn14 | ptr_cza_89d04 |
| 0x0808a2a8 | fn23 | ptr_cza_8a2a8 |

REF count gP1ChainZoneArray: **2**

### Total REF count: 19+5+5+5+2 = **36**

---

## EQ_SLOTS (CID pool equates)

### NEW CIDs to add to card_info.inc (11 entries, individual grep = 0 hits each):

```
.equ TOON_TABLE_OF_CONTENTS_CID,     0x00001562  @ Toon Table of Contents (pw=89997728; card-stats.s card_1138 slot=0x1562); grep 0x1562=0 hits
.equ MACHINE_DUPLICATION_CID,        0x0000157a  @ Machine Duplication (pw=63995093; card-stats.s card_1154 slot=0x157A); grep 0x157A=0 hits
.equ LEAGUE_UNIFORM_NOMENCLATURE_CID,0x00001978  @ The League of Uniform Nomenclature (pw=55008284; card-stats.s card_1989 slot=0x1978); grep 0x1978=0 hits
.equ GRAVEKEEPER_SPY_CID,            0x00001585  @ Gravekeeper's Spy (pw=24317029; card-stats.s card_1164 slot=0x1585); grep 0x1585=0 hits
.equ AN_OWL_OF_LUCK_CID,             0x00001593  @ An Owl of Luck (pw=23927567; card-stats.s card_1175 slot=0x1593); grep 0x1593=0 hits
.equ TERRAFORMING_CID,               0x000015a1  @ Terraforming (pw=73628505; card-stats.s card_1189 slot=0x15A1); grep 0x15A1=0 hits
.equ GOBLIN_ZOMBIE_CID,              0x000015b9  @ Goblin Zombie (pw=63665875; card-stats.s card_1210 slot=0x15B9); grep 0x15B9=0 hits
.equ FRONTLINE_BASE_CID,             0x000015e2  @ Frontline Base (pw=46181000; card-stats.s card_1235 slot=0x15E2); grep 0x15E2=0 hits
.equ TRIBUTE_DOLL_CID,               0x000015ed  @ Tribute Doll (pw=02903036; card-stats.s card_1243 slot=0x15ED); grep 0x15ED=0 hits
.equ BONDING_H2O_CID,                0x0000195c  @ Bonding - H2O (pw=45898858; card-stats.s card_1962 slot=0x195C); grep 0x195C=0 hits
.equ APPRENTICE_MAGICIAN_CID,        0x00001612  @ Apprentice Magician (pw=09156135; card-stats.s card_1271 slot=0x1612); grep 0x1612=0 hits
```

Count: **11 NEW CIDs**

### REUSE CIDs (already in card_info.inc, DO NOT add):
DE_SPELL_GERM_WEAPON_CID(0x14ee), DARK_SCORPION_BURGLARS_CID(0x1531), BOOK_OF_LIFE_CID(0x1536),
CALL_OF_THE_MUMMY_CID(0x153b), FUSHIOH_RICHIE_CID(0x1534), PUPPET_MASTER_CID(0x156a),
LORD_POISON_CID(0x156d), HIDDEN_SOLDIER_CID(0x1572), MONSTER_RELIEF_CID(0x1579),
FAMILIAR_KNIGHT_CID(0x17c3), A_CAT_OF_ILL_OMEN_CID(0x1590), DIFFERENT_DIMENSION_CAPSULE_CID(0x159c),
METAMORPHOSIS_CID(0x15a3), RITE_OF_SPIRIT_CID(0x15ac), ROPE_OF_SPIRIT_CID(0x15b5),
AUTONOMOUS_ACTION_UNIT_CID(0x15e6), SKILLED_WHITE_MAGICIAN_CID(0x1610), SKILLED_DARK_MAGICIAN_CID(0x1611),
KNIGHTS_TITLE_CID(0x167d), DEDICATION_THROUGH_LIGHT_DARK_CID(0x1713), PHOTON_GENERATOR_UNIT_CID(0x19b1),
MAGICAL_SCIENTIST_CID(0x1619)

### CID comparison pool equates (fn21 partner-check pool -- already in card_info.inc or labeled as-is):

Pool values at fn21 0x0808a010:
- 0x0808a030 = 0x167d = KNIGHTS_TITLE_CID (REUSE)
- 0x0808a048 = 0x195c = BONDING_H2O_CID (NEW above)
- 0x0808a04c = 0x1713 = DEDICATION_THROUGH_LIGHT_DARK_CID (REUSE)
- 0x0808a058 = 0x19b1 = PHOTON_GENERATOR_UNIT_CID (REUSE)
- 0x0808a064 = 0x1377 = BUSTER_BLADER_CID (REUSE, in card_info.inc)
- 0x0808a06c = 0x0fc9 = DARK_MAGICIAN_CID_0FC9 (REUSE, in card_info.inc)
- 0x0808a078 = 0x167c = Dark Magician Knight (NOT in card_info.inc; partner comparison only, not dispatched CID)
  -> label slot as `cid_167c_dark_magician_knight` (raw value, no .equ needed for partner-only CID)
- 0x0808a080 = 0x16f8 = DARK_MAGICIAN_OF_CHAOS_CID (REUSE)
- 0x0808a08c = 0x1951 = WATER_DRAGON_CID (REUSE)
- 0x0808a180 = 0x19a9 = CYBER_LASER_DRAGON_CID (REUSE)
- 0x0808a18c = 0x159d = NECROVALLEY_CID (REUSE)

### Scalar pool equates (existing constants):
- 0x00000868 = PLAYER_BLOCK_STRIDE (existing, ewram.inc)
- 0x000012a1 = zone_query_hand_tag_12a1 (existing, duel_field.inc)
- 0x000005dc = CARD_FIELD3_THRESHOLD_1500 (existing, card_info.inc)

---

## Literal Pool DWord List (createDWord required)

All pool addresses inside [0x0808962c, 0x0808a2ac):

**fn01** (0x0808962c): 0x0808967c, 0x08089680
**fn02** (0x08089684): 0x080896f0, 0x080896f4, 0x080896f8, 0x08089758, 0x0808975c
**fn03** (0x08089760): 0x080897ac, 0x080897b0
**fn04** (0x080897b4): 0x08089804, 0x08089808
**fn05** (0x0808980c): 0x0808988c, 0x08089890, 0x08089894
**fn06** (0x08089898): 0x0808991c, 0x08089920, 0x08089924
**fn07** (0x08089928): 0x08089988, 0x0808998c
**fn08** (0x08089990): 0x080899e0, 0x080899e4
**fn09** (0x080899e8): 0x08089a90, 0x08089a94, 0x08089a98, 0x08089a9c
**fn10** (0x08089aa0): 0x08089b4c, 0x08089b50, 0x08089b54, 0x08089b58, 0x08089b5c
**fn11** (0x08089b60): 0x08089bb0, 0x08089bb4
**fn12** (0x08089bb8): 0x08089c18, 0x08089c1c, 0x08089c20
**fn13** (0x08089c24): 0x08089c74, 0x08089c78
**fn14** (0x08089c7c): 0x08089cfc, 0x08089d00, 0x08089d04
**fn15** (0x08089d08): 0x08089d88, 0x08089d8c, 0x08089d90
**fn16** (0x08089d94): 0x08089e34, 0x08089e38, 0x08089e3c, 0x08089e40
**fn17** (0x08089e44): 0x08089ec4, 0x08089ec8, 0x08089ecc
**fn18** (0x08089ed0): 0x08089f2c, 0x08089f30
**fn19** (0x08089f34): 0x08089fac, 0x08089fb0, 0x08089fb4
**fn20** (0x08089fb8): 0x0808a008, 0x0808a00c
**fn21** (0x0808a010): 0x0808a030, 0x0808a048, 0x0808a04c, 0x0808a058, 0x0808a064,
                       0x0808a06c, 0x0808a078, 0x0808a080, 0x0808a08c, 0x0808a180,
                       0x0808a184, 0x0808a188, 0x0808a18c
**fn22** (0x0808a190): 0x0808a218, 0x0808a21c, 0x0808a220
**fn23** (0x0808a224): 0x0808a2a0, 0x0808a2a4, 0x0808a2a8

Total pool DWords: **76**

---

## disasm Plan (R4)

**Range**: [0x0808962c, 0x0808a2ac)
**Mode**: THUMB

Fixer script steps:
1. clearListing 0x0808962c..0x0808a2ac
2. setTMode THUMB for entire range
3. Per-function DisassembleCommand in address order (23 real function entries):
   0x0808962c, 0x08089684, 0x08089760, 0x080897b4, 0x0808980c,
   0x08089898, 0x08089928, 0x08089990, 0x080899e8, 0x08089aa0,
   0x08089b60, 0x08089bb8, 0x08089c24, 0x08089c7c, 0x08089d08,
   0x08089d94, 0x08089e44, 0x08089ed0, 0x08089f34, 0x08089fb8,
   0x0808a010, 0x0808a190, 0x0808a224
4. createFunction at each of the 23 entries above
5. force-createDWord for each pool address (76 total listed above)
6. Do NOT createFunction at degenerate addresses: 0x0808985e, 0x08089a58, 0x08089e78, 0x0808a28e

**Post-disasm gate**: grep `ROM_INCBIN\|\.byte` in asm/11_effect_slot_puzzletext.s for
lines covering 0x0808962c..0x0808a2ac must return 0 matches after export.

---

## carve Plan

None -- no data tables or code needing carve in this segment.

## 5.1 Entries

None -- all bytes in [0x0808962c, 0x0808a2ac) are part of real functions (0 unref orphans).

---

## Consumer Evidence Summary

- All 23 functions called via dispatch table 0x09e5a128 `{CID, fn_ptr+1}`, same caller pattern as Seg-4a/4b.
  Caller: dispatch_equip_zone_write_by_substate_range (0x0808d7f4). Confidence: high.
- write_equip_zone_entry_by_substate (0x0808d88c): asm/11_effect_slot_puzzletext.s. Confidence: high.
- check_card_field5_is_nonzero (0x0804ad48): asm/05_equip_eligibility_a.s. Confidence: high.
- check_zone_slot_equip_eligible (0x08037434): asm/03_equip_chain_hand.s. Confidence: high.
- eval_equip_placement_full_check (0x0803bba4): asm/03_equip_chain_hand.s. Confidence: high.
- find_effect_node_in_zone (0x0802fd60): asm/02_text_lp_fieldspell.s. Confidence: high.
- eval_equip_bonus_for_slot (0x080377b0): asm/03_equip_chain_hand.s. Confidence: high.
- check_card_is_equip_target_eligible (0x0804bb6c): asm/05_equip_eligibility_a.s. Confidence: high.
- check_card_id_is_equip_excluded_range (0x0804bc58): asm/05_equip_eligibility_a.s. Confidence: high.
- check_card_has_equip_placement_type (0x0804ba58): asm/05_equip_eligibility_a.s. Confidence: high.
- check_card_is_toon_type (0x0804ae40): asm/05_equip_eligibility_a.s. Confidence: high.
- check_card_stat_field8_is_8 (0x0804ae2c): asm/05_equip_eligibility_a.s. Confidence: high.
- check_card_is_gravekeeper (0x0804af60): asm/05_equip_eligibility_a.s. Confidence: high.
- check_card_pair_allowed (0x0804ab4c): asm/05_equip_eligibility_a.s. Confidence: high.
- count_field_copies_of_card (0x0803279c): asm/02_text_lp_fieldspell.s. Confidence: high.
- get_card_extended_stat_field3_raw (0x080eef44): asm/20_anim_jp_tileblit.s (get_card_extended_stat_field4_raw label at 0x080eef70 is distinct; 0x080eef44 is field3). Confidence: high.
- get_card_extended_stat_field4_raw (0x080eef70): asm/20_anim_jp_tileblit.s. Confidence: high.
- get_card_extended_stat_field6 (0x080eedf8): asm/20_anim_jp_tileblit.s. Confidence: high.
- get_card_extended_stat_field7 (0x080eee50): asm/20_anim_jp_tileblit.s. Confidence: high.
- get_card_extended_stat_field9 (0x080eee7c): asm/20_anim_jp_tileblit.s. Confidence: high.
- check_card_stat_field7_equals (0x08030b70): asm/02_text_lp_fieldspell.s. Confidence: high.
- check_card_stat_field8_is_8 (0x0804ae2c): asm/05. Confidence: high.
- zone_query_hand_tag_12a1 (0x000012a1): duel_field.inc. Confidence: high.
- CARD_FIELD3_THRESHOLD_1500 (0x000005dc): card_info.inc. Confidence: high.
- PLAYER_BLOCK_STRIDE (0x000868): ewram.inc. Confidence: high.

---

## Self-Check (Phase 4)

1. **Pool value verification**: 24 representative pool addresses spot-checked with `struct.unpack('<I', d[off:off+4])` -- all match expected values. See Python session above.
2. **Degenerate entries**: 4 confirmed with byte evidence:
   - 0x0808985e: bytes f7ad fde9 (BL mid-loop, no dispatch table entry)
   - 0x08089a58: bytes 1c30 210b (ADD/MOVS mid-loop, no branch targets it, no dispatch entry)
   - 0x08089e78: bytes 04c0 0cc4 (LSL/LSR bitfield pair mid-loop, no dispatch entry)
   - 0x0808a28e: bytes 6800 4285 d3da (LDR/CMP/BCC backward mid-loop, no dispatch entry)
3. **Size check**: 23 function spans sum to 0x0808a2ac - 0x0808962c = 0xC80 = 3200 B (confirmed).
4. **Plate text**: all ASCII only, no CJK. Longest plate (fn21) = 499 chars (within 500 limit).
5. **Slot names**: all `^[a-z][a-z0-9_]+$`; multiple gP1LifePoints slots disambiguated by hex address suffix.
6. **CID value greps**: 11 NEW confirmed 0 hits each (individual grep output listed above); 22 REUSE confirmed present in card_info.inc.
7. **fn21 pool note**: 0x0808a046 = 0x0000 is padding between pool words; pool addresses are word-aligned. 0x0808a034 = ldr r0,[pc,#4] -> 0x0808a048 = 0x195c (not the same slot as 0x0808a046 which is zero pad).
8. **Segment continuity**: fn01 starts at 0x0808962c (confirmed by b5f0 push prologue), fn23 ends at 0x0808a29c (bx r0 epilogue), pool ends at 0x0808a2ac.
9. **Zero-引用 gate**: full dispatch table scan of 305 entries confirms 0x0808985e/0x08089a58/0x08089e78/0x0808a28e have 0 entries each (no fn_ptr+1 hits).
