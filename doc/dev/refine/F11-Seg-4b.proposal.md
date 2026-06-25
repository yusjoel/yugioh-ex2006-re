# Refine Proposal: F11-Seg-4b  [0x08088904..0x0808962c)

## Segment Survey

- ROM range: `[0x08088904, 0x0808962c)` = 0xD28 bytes (3368 B)
- Source: one-liner `ROM_INCBIN 0x88904, 0x4ef0` (remainder after Seg-4a carved 0x87d58..0x88904)
- Boundary at 0x08088904 = next strong entry after Seg-4a; boundary at 0x0808962c = next segment start
- Functions: **25 real functions** (27 strong entries - 2 degenerate = 25 real)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools

### Function type: equip zone scan callbacks (same pattern as Seg-4a)

All 25 real functions are equip zone scan callbacks dispatched from the 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

---

## Weak Entry Analysis (1 candidate)

| addr | context | ROM bytes | disposition |
|------|---------|-----------|-------------|
| 0x8088ef6 | inside fn11 (0x08088e64..0x08088ed8), offset 0x92 | `2816 d12c` = `cmp r0,#0x16; bne ...` -- mid-loop body | EXCLUDE: mid-instruction code |

fn11 spans 0x08088e64..0x08088ed8 (116 bytes). The byte at 0x8088ef6 is 0x28 (cmp r0,#imm), not
a push prologue. Ref source for this value is in compressed asset data (non-word-aligned).

---

## Degenerate Strong Entries (2 of 27)

| addr | reason | evidence |
|------|--------|---------|
| 0x0808939c | Forward-branch target from fn23 (Last Turn, 0x08089378). ROM halfwords `4690 46a1` = `mov r8,r2; mov r9,r4` -- high-reg loop setup, not a function prologue. bcs at 0x08089398 (opcode d2, offset 0x31) targets 0x0808939c+0x62=0x080893fe, which is inside 0x0808939c..0x0808941c. dispatch table: NO entry points to 0x0808939c+1. | fn23 real span = 0x08089378..0x0808941c (164 B); fn24 is mid-body |
| 0x08089560 | Mid-prologue of fn26 (Pyramid Turtle, 0x08089558). ROM bytes at 0x08089560: `b4e0 1c07 468a 2000` = `push {r5,r6,r7}; mov r7,r0; mov r10,r1; movs r0,#0`. This is the second-push in the high-register save pattern: fn26 starts with `b5f0; mov r7,r10; mov r6,r9; mov r5,r8; push {r5,r6,r7}`. dispatch table: NO entry points to 0x08089560+1. | fn26 real span = 0x08089558..0x0808962c (212 B); fn27 is mid-prologue |

---

## Dispatch Table CID Scan (full scan, 305 entries at 0x09e5a128)

| fn | addr | CID(s) | entry indices | card name(s) |
|----|------|--------|--------------|-------------|
| fn01 | 0x08088904 | 0x1480, 0x183c | [63], [228] | Kycoo the Ghost Destroyer; Dark Blade the Dragon Knight |
| fn02 | 0x0808896c | 0x1482 | [65] | Bazoo the Soul-Eater |
| fn03 | 0x080889c4 | 0x1466, 0x18b4, 0x19ca | [57], [250], [299] | Dark Necrofear; Megarock Dragon; Doom Dozer |
| fn04 | 0x08088a34 | 0x1468 | [58] | Destiny Board |
| fn05 | 0x08088ad4 | 0x146e | [59] | Dark Sage |
| fn06 | 0x08088b2c | 0x146f | [60] | Cathedral of Nobles |
| fn07 | 0x08088c9c | 0x1474 | [61] | Foolish Burial |
| fn08 | 0x08088d2c | 0x1483, 0x1484, 0x1485, 0x1486, 0x1487, 0x15bc, 0x16b9, 0x16c0, 0x16c5, 0x16c6, 0x16c7, 0x16c8, 0x18e0 | [66-70],[117],[152],[154],[157-160],[257] | Soul of Purity; Spirit of Flames; Aqua Spirit; Rock Spirit; Garuda; Lekunga; Strike Ninja; Freed Brave Wanderer; Inferno; Fenrir; Gigantes; Silpheed; Infernal Flame Emperor |
| fn09 | 0x08088db8 | 0x148b | [72] | Supply |
| fn10 | 0x08088e0c | 0x1490 | [73] | Skull Lair |
| fn11 | 0x08088e64 | 0x149e | [75] | Miracle Dig |
| fn12 | 0x08088ed8 | 0x14a7 | [76] | Rope of Life |
| fn13 | 0x08088f7c | 0x135b, 0x14c6 | [39], [78] | cid_135b (unallocated); Marauding Captain |
| fn14 | 0x08088fe0 | 0x14c4, 0x14d0 | [77], [79] | Freed the Matchless General; Reinforcement of the Army |
| fn15 | 0x08089068 | 0x14d2 | [80] | The Warrior Returning Alive |
| fn16 | 0x080890c0 | 0x14d7 | [81] | Spirit Ryu |
| fn17 | 0x08089114 | 0x14ef | [86] | Des Feral Imp |
| fn18 | 0x08089150 | 0x14f6, 0x14f7 | [87], [88] | Agido; Silent Fiend (wait -- [87]=0x14f6 Agido, but fn19 has [88]=0x14f7; see below) |
| fn19 | 0x080891f8 | 0x14f7, 0x17b7 | [88], [196] | Silent Fiend; Soul Resurrection |
| fn20 | 0x08089284 | 0x14fd | [89] | Maharaghi |
| fn21 | 0x080892b4 | 0x1507, 0x1508 | [90], [91] | Super Robolady; Super Roboyarou |
| fn22 | 0x08089338 | 0x14e7, 0x1515, 0x15dd, 0x19c0 | [83], [92], [120], [297] | Keldo; Disappear; Dimension Jar; D.D. Guide |
| fn23 | 0x08089378 | 0x151e | [93] | Last Turn |
| fn25 | 0x0808941c | 0x1522, 0x1746 | [94], [179] | Vampire Lord; Vampire Lady |
| fn26 | 0x08089558 | 0x152f | [96] | Pyramid Turtle |

Note fn18 and fn19 CID re-check: full table scan gives:
- 0x08089150 -> entries [87]=0x14f6 Agido, [88]=0x14f7 Silent Fiend
- 0x080891f8 -> entries [88]=0x14f7 Silent Fiend [196]=0x17b7 Soul Resurrection
Wait -- [88] appears in BOTH. This means [88] = {CID=0x14f7, fn_ptr=0x08089151} 
AND 0x080891f8 also maps to 0x14f7. But the table is one entry per pair. Let me correct:
From CID scan output: `0x08089150: CID=0x14f6 [87]` and `0x080891f8: MULTI-CID 0x14f7[88] 0x17b7[196]`.
So fn18 (0x08089150) = 0x14f6 Agido only; fn19 (0x080891f8) = 0x14f7 Silent Fiend + 0x17b7 Soul Resurrection.

Corrected fn18/fn19:
- fn18 0x08089150: CID=0x14f6 (Agido) only, [entry 87]
- fn19 0x080891f8: CID=0x14f7 (Silent Fiend) + 0x17b7 (Soul Resurrection), [entries 88, 196]

---

## Function Naming Table (25 real functions)

Substate semantics (from existing plate for write_equip_zone_entry_by_substate):
- 0xb = field-spell zone type B
- 0xc = chain zone type C
- 0xd = monster zone type D
- 0xe = hand slot type E
- 0xf = graveyard type F

### fn01: 0x08088904  size=0x068 (104 B)
- CID(s): 0x1480 (Kycoo the Ghost Destroyer), 0x183c (Dark Blade the Dragon Knight)
- Dispatch entries: [63], [228]
- Body: push {r4-r7,lr}; high-reg setup; loop monster zone slots via gP1LifePoints+STRIDE;
  check_card_field5_is_nonzero; write substate_e
- BL targets: 0x0804ad48 (check_card_field5_is_nonzero), 0x0808d88c (write_equip_zone_entry_by_substate)
- Pool dwords: 0x08088964=gP1LifePoints, 0x08088968=PLAYER_BLOCK_STRIDE
- CID status: 0x1480 NEW (0 hits); 0x183c REUSE DARK_BLADE_THE_DRAGON_KNIGHT_CID
- Substate: 0xe
- Proposed name: `scan_zone_kycoo_dark_blade_group_substate_e`
- Confidence: high (body: field5 check + write_e; group: both require monster as equip target)
- ASCII plate: `Equip zone scan callback for Kycoo/Dark Blade group: Kycoo the Ghost Destroyer (CID=0x1480, pw=88240808), Dark Blade the Dragon Knight (DARK_BLADE_THE_DRAGON_KNIGHT_CID=0x183c, pw=86805855). r0=player_id. Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [63,228].`

### fn02: 0x0808896c  size=0x058 (88 B)
- CID: 0x1482 (Bazoo the Soul-Eater)
- Dispatch entry: [65]
- Body: push {r4-r7,lr}; loop hand slots; check_card_field5_is_nonzero; write substate_e
- BL targets: 0x0804ad48, 0x0808d88c
- Pool: 0x080889bc=gP1LifePoints, 0x080889c0=PLAYER_BLOCK_STRIDE
- CID: REUSE BAZOO_THE_SOUL_EATER_CID
- Substate: 0xe
- Proposed name: `scan_zone_bazoo_substate_e`
- Confidence: high
- ASCII plate: `Equip zone scan callback for Bazoo the Soul-Eater (BAZOO_THE_SOUL_EATER_CID=0x1482, pw=40133511). r0=player_id. Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [65].`

### fn03: 0x080889c4  size=0x070 (112 B)
- CID(s): 0x1466 (Dark Necrofear), 0x18b4 (Megarock Dragon), 0x19ca (Doom Dozer)
- Dispatch entries: [57], [250], [299]
- Body: push {r4-r7,lr} + high-reg push; loop monster zone; get_card_extended_stat_field6 (x2);
  compare field6 values; write substate_e
- BL targets: 0x080eedf8 (get_card_extended_stat_field6), 0x0808d88c
- Pool: 0x08088a2c=gP1LifePoints, 0x08088a30=PLAYER_BLOCK_STRIDE
- CID: 0x1466 REUSE DARK_NECROFEAR_CID; 0x18b4 REUSE MEGAROCK_DRAGON_CID; 0x19ca REUSE DOOM_DOZER_CID
- Substate: 0xe
- Proposed name: `scan_zone_removed_accumulator_group_substate_e`
- Confidence: high (body: field6 gate -- all three require removed-from-play accumulation to special-summon; shared removal-accumulator mechanic)
- ASCII plate: `Equip zone scan callback for removed-accumulator group: Dark Necrofear (DARK_NECROFEAR_CID=0x1466, pw=31829185), Megarock Dragon (MEGAROCK_DRAGON_CID=0x18b4, pw=71544954), Doom Dozer (DOOM_DOZER_CID=0x19ca, pw=76039636). Gate: get_card_extended_stat_field6 pair-compare; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [57,250,299].`

### fn04: 0x08088a34  size=0x0a0 (160 B)
- CID: 0x1468 (Destiny Board)
- Dispatch entry: [58]
- Body: push + high-reg; two scan loops (different field offsets: +0xc and +0x10);
  first loop writes substate_b, second writes substate_d; compares slot code vs loaded value
- BL targets: 0x0808d88c (x2)
- Pool: 0x08088acc=gP1LifePoints, 0x08088ad0=PLAYER_BLOCK_STRIDE
- CID: REUSE DESTINY_BOARD_CID
- Substates: 0xb, 0xd
- Proposed name: `scan_zone_destiny_board_substate_bd`
- Confidence: high (body: two distinct scan loops with different substates; Destiny Board activates on field-spell zone and monster zone)
- ASCII plate: `Equip zone scan callback for Destiny Board (DESTINY_BOARD_CID=0x1468, pw=94212438). r0=player_id. Two loops: loop1 scans field at +0xc, write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx); loop2 scans at +0x10, write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [58].`

### fn05: 0x08088ad4  size=0x058 (88 B)
- CID: 0x146e (Dark Sage)
- Dispatch entry: [59]
- Body: push; loop monster zone at offset +0x10; get_card_extended_stat_field6;
  cmp r0,#0x16; write substate_d
- BL targets: 0x080eedf8 (get_card_extended_stat_field6), 0x0808d88c
- Pool: 0x08088b24=gP1LifePoints, 0x08088b28=PLAYER_BLOCK_STRIDE
- CID: REUSE DARK_SAGE_CID
- Substate: 0xd
- Proposed name: `scan_zone_dark_sage_substate_d`
- Confidence: high (body: field6 check; Dark Sage special-summon from deck requires field6 gate)
- ASCII plate: `Equip zone scan callback for Dark Sage (DARK_SAGE_CID=0x146e, pw=92377303). r0=player_id. Gate: get_card_extended_stat_field6 == 0x16; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [59].`

### fn06: 0x08088b2c  size=0x170 (368 B)
- CID: 0x146f (Cathedral of Nobles)
- Dispatch entry: [60]
- Body: push {r4-r7,lr} + high-reg push (full r8-r10 save); two major scan loops:
  loop1 scans gP1FieldArrayCBase slots, check_card_field5_is_nonzero +
  eval_equip_placement_full_check + find_effect_node_in_zone, write substate_b;
  loop2 scans gP1SlotSetCodeArray (zone_query_hand_tag_12a1 filter + check_card_is_equip_target_eligible
  + check_card_id_is_equip_excluded_range), write substate_d; additional write substate_c via
  gP1ChainZoneArray (0x0201c880 = gP1ChainZoneArray)
- BL targets: 0x0804ad48, 0x0803bba4 (eval_equip_placement_full_check), 0x0808d88c,
  0x0802fd60 (find_effect_node_in_zone), 0x0804bb6c (check_card_is_equip_target_eligible),
  0x0804bc58 (check_card_id_is_equip_excluded_range)
- Pool: 0x08088c84=gP1LifePoints, 0x08088c88=PLAYER_BLOCK_STRIDE, 0x08088c8c=gP1FieldArrayCBase,
  0x08088c90=gP1SlotSetCodeArray, 0x08088c94=zone_query_hand_tag_12a1, 0x08088c98=gP1ChainZoneArray
- CID: REUSE CATHEDRAL_OF_NOBLES_CID
- Substates: 0xb, 0xd, 0xc
- Proposed name: `scan_zone_cathedral_of_nobles_substate_bdc`
- Confidence: high (body verified: three distinct substate writes; Cathedral of Nobles is an equip that affects multiple zone types)
- ASCII plate: `Equip zone scan callback for Cathedral of Nobles (CATHEDRAL_OF_NOBLES_CID=0x146f, pw=29762407). r0=player_id. Three-path scan: (1) gP1FieldArrayCBase slots -- field5+eval_equip_placement+find_node gate, substate b; (2) gP1SlotSetCodeArray -- zone_query_hand_tag filter+equip_target_eligible+excl_range gate, substate d; (3) gP1ChainZoneArray -- substate c. Dispatched from write table entry [60].`

### fn07: 0x08088c9c  size=0x090 (144 B)
- CID: 0x1474 (Foolish Burial)
- Dispatch entry: [61]
- Body: push + high-reg; scan gP1SlotSetCodeArray with zone_query_hand_tag_12a1 filter;
  check_card_field5_is_nonzero; find_effect_node_in_zone; write substate_d
- BL targets: 0x0804ad48, 0x0802fd60 (find_effect_node_in_zone), 0x0808d88c
- Pool: 0x08088d1c=gP1LifePoints, 0x08088d20=PLAYER_BLOCK_STRIDE,
  0x08088d24=gP1SlotSetCodeArray, 0x08088d28=zone_query_hand_tag_12a1
- CID: 0x1474 NEW (0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_foolish_burial_substate_d`
- Confidence: high (body: field5 + find_node gate + write_d; Foolish Burial sends card to GY)
- ASCII plate: `Equip zone scan callback for Foolish Burial (CID=0x1474, pw=81439173). r0=player_id. Gate: check_card_field5_is_nonzero + find_effect_node_in_zone via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [61].`

### fn08: 0x08088d2c  size=0x08c (140 B)
- CID(s): 0x1483, 0x1484, 0x1485, 0x1486, 0x1487, 0x15bc, 0x16b9, 0x16c0, 0x16c5, 0x16c6, 0x16c7, 0x16c8, 0x18e0
- Dispatch entries: [66],[67],[68],[69],[70],[117],[152],[154],[157],[158],[159],[160],[257]
- Body: push {r4-r7,lr} + high-reg push; scan gP1HandSlotArray;
  check_card_field5_is_nonzero; get_card_extended_stat_field8 (map type);
  check removed-from-play count; write substate_e
- BL targets: 0x0804ad48, 0x080eee24 (get_card_extended_stat_field8),
  0x08030b70 (check_card_stat_field7_equals), 0x0808d88c
- Pool: 0x08088dac=gP1LifePoints, 0x08088db0=PLAYER_BLOCK_STRIDE, 0x08088db4=gP1HandSlotArray
- CID status: 0x1483 REUSE SOUL_OF_PURITY_CID; 0x1484 NEW (Spirit of Flames); 0x1485 REUSE AQUA_SPIRIT_CID;
  0x1486 REUSE ROCK_SPIRIT_CID; 0x1487 NEW (Garuda the Wind Spirit); 0x15bc NEW (Lekunga);
  0x16b9 REUSE STRIKE_NINJA_CID; 0x16c0 NEW (Freed the Brave Wanderer); 0x16c5 REUSE INFERNO_CID;
  0x16c6 REUSE FENRIR_CID; 0x16c7 NEW (Gigantes); 0x16c8 REUSE SILPHEED_CID; 0x18e0 NEW (Infernal Flame Emperor)
- Substate: 0xe
- Proposed name: `scan_zone_removed_spirit_elemental_group_substate_e`
- Confidence: high (body: field5+field8+field7 type gate; all 13 cards require monsters/spells removed from play; spirit/elemental/removed-play mechanic group)
- ASCII plate: `Equip zone scan callback for removed-from-play spirit/elemental group (13 CIDs): SOUL_OF_PURITY_CID(0x1483), Spirit_of_Flames(0x1484), AQUA_SPIRIT_CID(0x1485), ROCK_SPIRIT_CID(0x1486), Garuda(0x1487), Lekunga(0x15bc), STRIKE_NINJA_CID(0x16b9), Freed_Brave_Wanderer(0x16c0), INFERNO_CID(0x16c5), FENRIR_CID(0x16c6), Gigantes(0x16c7), SILPHEED_CID(0x16c8), Infernal_Flame_Emperor(0x18e0). Gate: field5+field8+field7; write substate e. Dispatched from entries [66-70,117,152,154,157-160,257].`

### fn09: 0x08088db8  size=0x054 (84 B)
- CID: 0x148b (Supply)
- Dispatch entry: [72]
- Body: push; loop hand slots via gP1LifePoints; write substate_e (direct, no gate)
- BL targets: 0x0808d88c
- Pool: 0x08088e04=gP1LifePoints, 0x08088e08=PLAYER_BLOCK_STRIDE
- CID: 0x148b NEW (0 hits)
- Substate: 0xe
- Proposed name: `scan_zone_supply_substate_e`
- Confidence: high
- ASCII plate: `Equip zone scan callback for Supply (CID=0x148b, pw=44072894). r0=player_id. Simple loop over hand slots in gP1LifePoints[player*STRIDE]; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx) for all entries. Dispatched from write table entry [72].`

### fn10: 0x08088e0c  size=0x058 (88 B)
- CID: 0x1490 (Skull Lair)
- Dispatch entry: [73]
- Body: push; loop hand slots; check_card_field5_is_nonzero; write substate_e
- BL targets: 0x0804ad48, 0x0808d88c
- Pool: 0x08088e5c=gP1LifePoints, 0x08088e60=PLAYER_BLOCK_STRIDE
- CID: 0x1490 NEW (0 hits)
- Substate: 0xe
- Proposed name: `scan_zone_skull_lair_substate_e`
- Confidence: high
- ASCII plate: `Equip zone scan callback for Skull Lair (CID=0x1490, pw=06733059). r0=player_id. Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [73].`

### fn11: 0x08088e64  size=0x074 (116 B)
- CID: 0x149e (Miracle Dig)
- Dispatch entry: [75]
- Body: push; loop hand slots; check_card_field5_is_nonzero; eval_equip_bonus_for_slot
  (0x0803b618 = get_zone_card_attribute_by_type); write substate_f; uses gP1AltHandSlotArray
- BL targets: 0x0804ad48, 0x0803b618 (get_zone_card_attribute_by_type), 0x0808d88c
- Pool: 0x08088ecc=gP1LifePoints, 0x08088ed0=PLAYER_BLOCK_STRIDE, 0x08088ed4=gP1AltHandSlotArray
- CID: REUSE MIRACLE_DIG_CID
- Substate: 0xf
- Proposed name: `scan_zone_miracle_dig_substate_f`
- Confidence: high (body: field5 + zone_attr gate; write_f; Miracle Dig targets GY)
- ASCII plate: `Equip zone scan callback for Miracle Dig (MIRACLE_DIG_CID=0x149e, pw=06343408). r0=player_id. Gate: check_card_field5_is_nonzero + get_zone_card_attribute_by_type via gP1AltHandSlotArray; write_equip_zone_entry_by_substate(player_id, 0xf, slot_idx). Dispatched from write table entry [75].`

### fn12: 0x08088ed8  size=0x0a4 (164 B)
- CID: 0x14a7 (Rope of Life)
- Dispatch entry: [76]
- Body: push; loop: load lp_bar_anim_state count at gDuelPhaseFlags+LP_BAR_ANIM_STATE_OFF(0x4cc);
  load sprite_row_entry_data byte at gDuelPhaseFlags+SPRITE_ROW_ENTRY_DATA_OFF(0x4d4)+slot;
  check byte == 0x16 (battle-destroyed indicator); find_hand_slot_idx_by_set_code (0x0803123c);
  check_card_field5_is_nonzero; check_zone_slot_equip_eligible; write substate_e
- BL targets: 0x0803123c (find_hand_slot_idx_by_set_code), 0x0804ad48, 0x08037434 (check_zone_slot_equip_eligible), 0x0808d88c
- Pool: 0x08088f68=gDuelPhaseFlags, 0x08088f6c=LP_BAR_ANIM_STATE_OFF, 0x08088f70=SPRITE_ROW_ENTRY_DATA_OFF,
  0x08088f74=PLAYER_BLOCK_STRIDE, 0x08088f78=gP1HandSlotArray
- CID: REUSE ROPE_OF_LIFE_CID
- Substate: 0xe
- Proposed name: `scan_zone_rope_of_life_substate_e`
- Confidence: high (body: lp-bar row entry byte 0x16 = battle-destroyed slot check; Rope of Life revives battle-destroyed monster)
- ASCII plate: `Equip zone scan callback for Rope of Life (ROPE_OF_LIFE_CID=0x14a7, pw=93382620). r0=player_id. Gate: gDuelPhaseFlags+LP_BAR_ANIM_STATE_OFF(0x4cc) count loop; check sprite_row_entry_data[slot]==0x16 (battle-destroyed marker); find_hand_slot_idx_by_set_code; field5; equip_eligible; write substate e. Dispatched from write table entry [76].`

### fn13: 0x08088f7c  size=0x064 (100 B)
- CID(s): 0x135b (cid_135b, unallocated), 0x14c6 (Marauding Captain)
- Dispatch entries: [39], [78]
- Body: push; loop field slots; check_card_field5_is_nonzero; eval_equip_bonus_for_slot
  (0x080377b0 = eval_equip_bonus_for_slot); eval_equip_placement_full_check; write substate_b
- BL targets: 0x0804ad48, 0x080377b0 (eval_equip_bonus_for_slot), 0x0803bba4 (eval_equip_placement_full_check), 0x0808d88c
- Pool: 0x08088fd8=PLAYER_BLOCK_STRIDE, 0x08088fdc=gP1FieldArrayCBase
- CID: cid_135b REUSE; MARAUDING_CAPTAIN_CID REUSE
- Substate: 0xb
- Proposed name: `scan_zone_marauding_captain_group_substate_b`
- Confidence: high (body: field5 + equip_bonus + placement check + write_b; both require field-spell zone placement; cid_135b is unallocated gap in same range)
- ASCII plate: `Equip zone scan callback for Marauding Captain group: cid_135b (0x135b, unallocated), Marauding Captain (MARAUDING_CAPTAIN_CID=0x14c6, pw=02460565). Gate: check_card_field5_is_nonzero + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from write table entries [39,78].`

### fn14: 0x08088fe0  size=0x088 (136 B)
- CID(s): 0x14c4 (Freed the Matchless General), 0x14d0 (Reinforcement of the Army)
- Dispatch entries: [77], [79]
- Body: push; scan gP1SlotSetCodeArray; get_card_extended_stat_field7 (0x080eee50);
  get_card_extended_stat_field6 (0x080eedf8); field comparison; write substate_d
- BL targets: 0x0804ad48, 0x080eee50 (get_card_extended_stat_field7), 0x080eedf8 (get_card_extended_stat_field6), 0x0808d88c
- Pool: 0x0808905c=gP1LifePoints, 0x08089060=PLAYER_BLOCK_STRIDE, 0x08089064=gP1SlotSetCodeArray
- CID: 0x14c4 REUSE FREED_THE_MATCHLESS_GENERAL_CID; 0x14d0 NEW (Reinforcement of the Army)
- Substate: 0xd
- Proposed name: `scan_zone_warrior_search_group_substate_d`
- Confidence: high (body: field6+field7 gate; both Freed/Reinforcement are warrior search cards)
- ASCII plate: `Equip zone scan callback for warrior search group: Freed the Matchless General (FREED_THE_MATCHLESS_GENERAL_CID=0x14c4, pw=49681811), Reinforcement of the Army (CID=0x14d0, pw=32807846). Gate: check_card_field5_is_nonzero + field7+field6 check via gP1SlotSetCodeArray; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [77,79].`

### fn15: 0x08089068  size=0x058 (88 B)
- CID: 0x14d2 (The Warrior Returning Alive)
- Dispatch entry: [80]
- Body: push; loop hand slots; get_card_extended_stat_field6; field6 check; write substate_e
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x080890b8=gP1LifePoints, 0x080890bc=PLAYER_BLOCK_STRIDE
- CID: REUSE THE_WARRIOR_RETURNING_ALIVE_CID
- Substate: 0xe
- Proposed name: `scan_zone_warrior_returning_alive_substate_e`
- Confidence: high
- ASCII plate: `Equip zone scan callback for The Warrior Returning Alive (THE_WARRIOR_RETURNING_ALIVE_CID=0x14d2, pw=95281259). r0=player_id. Gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [80].`

### fn16: 0x080890c0  size=0x054 (84 B)
- CID: 0x14d7 (Spirit Ryu)
- Dispatch entry: [81]
- Body: push; loop field slots via gP1FieldArrayCBase; check_card_field5_is_nonzero;
  get_card_extended_stat_field6; write substate_b
- BL targets: 0x0804ad48, 0x080eedf8, 0x0808d88c
- Pool: 0x0808910c=PLAYER_BLOCK_STRIDE, 0x08089110=gP1FieldArrayCBase
- CID: REUSE SPIRIT_RYU_CID
- Substate: 0xb
- Proposed name: `scan_zone_spirit_ryu_substate_b`
- Confidence: high (body: field5+field6 gate + write_b; Spirit Ryu discards Dragons to boost ATK)
- ASCII plate: `Equip zone scan callback for Spirit Ryu (SPIRIT_RYU_CID=0x14d7, pw=67957315). r0=player_id. Gate: check_card_field5_is_nonzero + get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx) via gP1FieldArrayCBase scan. Dispatched from write table entry [81].`

### fn17: 0x08089114  size=0x03c (60 B)
- CID: 0x14ef (Des Feral Imp)
- Dispatch entry: [86]
- Body: push {r4,r5,r7,lr}; simple loop hand slots; write substate_e (no gate)
- BL targets: 0x0808d88c
- Pool: 0x08089148=gP1LifePoints, 0x0808914c=PLAYER_BLOCK_STRIDE
- CID: 0x14ef NEW (0 hits)
- Substate: 0xe
- Proposed name: `scan_zone_des_feral_imp_substate_e`
- Confidence: high
- ASCII plate: `Equip zone scan callback for Des Feral Imp (CID=0x14ef, pw=81985784). r0=player_id. Simple loop over hand slots; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx) for all entries. Dispatched from write table entry [86].`

### fn18: 0x08089150  size=0x0a8 (168 B)
- CID: 0x14f6 (Agido)
- Dispatch entry: [87]
- Body: push {r4-r7,lr} + high-reg push; scan gP1HandSlotArray (offset +0x14);
  get_card_extended_stat_field6 (0x080eedf8); check field6==0x11; check_zone_slot_equip_eligible;
  get_card_extended_stat_field7 (x2 -- comparing pair); write substate_e
- BL targets: 0x080eedf8 (x2), 0x08037434 (check_zone_slot_equip_eligible), 0x080eee50 (get_card_extended_stat_field7, x2), 0x0808d88c
- Pool: 0x080891bc=gP1LifePoints, 0x080891c0=PLAYER_BLOCK_STRIDE, 0x080891c4=gP1HandSlotArray, 0x080891f4=PLAYER_BLOCK_STRIDE
- CID: REUSE AGIDO_CID
- Substate: 0xe
- Proposed name: `scan_zone_agido_substate_e`
- Confidence: high (body: field6 == 0x11 is Fairy check; Agido is a Fairy special-summon trigger)
- ASCII plate: `Equip zone scan callback for Agido (AGIDO_CID=0x14f6, pw=16135253). r0=player_id. Gate: get_card_extended_stat_field6==0x11 (Fairy type) + check_zone_slot_equip_eligible + field7 pair compare; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entry [87].`

### fn19: 0x080891f8  size=0x08c (140 B)
- CID(s): 0x14f7 (Silent Fiend), 0x17b7 (Soul Resurrection)
- Dispatch entries: [88], [196]
- Body: push + high-reg; scan gP1HandSlotArray; check_card_field5_is_nonzero;
  map_field8_to_card_type_category (0x0804a9dc); check_zone_slot_equip_eligible; write substate_e
- BL targets: 0x0804ad48, 0x0804a9dc (map_field8_to_card_type_category), 0x08037434, 0x0808d88c
- Pool: 0x08089278=gP1LifePoints, 0x0808927c=PLAYER_BLOCK_STRIDE, 0x08089280=gP1HandSlotArray
- CID: 0x14f7 NEW (Silent Fiend); SOUL_RESURRECTION_CID REUSE
- Substate: 0xe
- Proposed name: `scan_zone_silent_fiend_soul_res_group_substate_e`
- Confidence: high (body: field5 + type category gate + equip_eligible; both are special-summon monsters requiring hand zone)
- ASCII plate: `Equip zone scan callback for Silent Fiend/Soul Resurrection group: Silent Fiend (CID=0x14f7, pw=42534368), Soul Resurrection (SOUL_RESURRECTION_CID=0x17b7, pw=92924317). Gate: check_card_field5_is_nonzero + map_field8_to_card_type_category + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [88,196].`

### fn20: 0x08089284  size=0x030 (48 B)
- CID: 0x14fd (Maharaghi)
- Dispatch entry: [89]
- Body: push {r0,lr}; simple loop monster zone; write substate_d (direct, no gate BL)
- BL targets: 0x0808d88c
- Pool: 0x080892ac=gP1LifePoints, 0x080892b0=PLAYER_BLOCK_STRIDE
- CID: REUSE MAHARAGHI_CID
- Substate: 0xd
- Proposed name: `scan_zone_maharaghi_substate_d`
- Confidence: high (simplest function in segment: loop + write_d)
- ASCII plate: `Equip zone scan callback for Maharaghi (MAHARAGHI_CID=0x14fd, pw=40695128). r0=player_id. Simple loop over monster zone in gP1LifePoints[player*STRIDE+0x18]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entry [89].`

### fn21: 0x080892b4  size=0x084 (132 B)
- CID(s): 0x1507 (Super Robolady), 0x1508 (Super Roboyarou)
- Dispatch entries: [90], [91]
- Body: push + high-reg; compare input CID with SUPER_ROBOLADY_CID (0x1507); branch to load
  SUPER_ROBOYAROU_CID (0x1508) partner; scan monster zone; compare slot CID vs partner CID;
  write substate_c
- BL targets: 0x0808d88c
- Pool: 0x080892cc=0x1507 (SUPER_ROBOLADY, ldr at 0x080892bc), 0x080892d0=0x1508 (SUPER_ROBOYAROU, ldr at 0x080892c2 when CID!=0x1507), 0x080892dc=0x1508 (SUPER_ROBOYAROU, ldr at 0x080892d4 when CID==0x1507), 0x08089330=gP1LifePoints, 0x08089334=PLAYER_BLOCK_STRIDE
- CID: 0x1507 NEW; 0x1508 NEW
- Substate: 0xc
- Proposed name: `scan_zone_super_robo_pair_substate_c`
- Confidence: high (body: pair-check CID 0x1507/0x1508 -- Super Robolady/Roboyarou are a matching pair for chain zone C)
- ASCII plate: `Equip zone scan callback for Super Robolady/Roboyarou pair: Super Robolady (CID=0x1507, pw=75923050), Super Roboyarou (CID=0x1508, pw=01412158). r0=player_id. Pair check: if input_CID==0x1507 seek 0x1508 in zone (or vice versa); write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatched from write table entries [90,91].`
- Note on pool: 0x080892d4 = 0x46804801 is CODE (`4801 ldr r0,[pc,#4]; 4680 mov r8,r0`), reached by beq (d008) from 0x080892c0 when CID==0x1507. 0x080892d8 = 0xe003 is CODE (b +6). NOT pool words. createDWord at: 0x080892cc(SUPER_ROBOLADY), 0x080892d0(SUPER_ROBOYAROU), 0x080892dc(SUPER_ROBOYAROU), 0x08089330(gP1LifePoints), 0x08089334(PLAYER_BLOCK_STRIDE).

### fn22: 0x08089338  size=0x040 (64 B)
- CID(s): 0x14e7 (Keldo), 0x1515 (Disappear), 0x15dd (Dimension Jar), 0x19c0 (D.D. Guide)
- Dispatch entries: [83], [92], [120], [297]
- Body: push {r0,lr}; simple loop hand zone; write substate_e (direct, no gate)
- BL targets: 0x0808d88c
- Pool: 0x08089370=gP1LifePoints, 0x08089374=PLAYER_BLOCK_STRIDE
- CID: KELDO_CID REUSE; DISAPPEAR_CID REUSE; DIMENSION_JAR_CID REUSE; DD_GUIDE_CID REUSE
- Substate: 0xe
- Proposed name: `scan_zone_removed_zone_return_group_substate_e`
- Confidence: high (body: minimal gate + write_e; all four are removed-from-play zone return effects)
- ASCII plate: `Equip zone scan callback for removed-zone return group: Keldo (KELDO_CID=0x14e7, pw=80441106), Disappear (DISAPPEAR_CID=0x1515, pw=24623598), Dimension Jar (DIMENSION_JAR_CID=0x15dd, pw=73414375), D.D. Guide (DD_GUIDE_CID=0x19c0, pw=52702748). Simple loop write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from write table entries [83,92,120,297].`

### fn23: 0x08089378  size=0x0a4 (164 B)  [spans to 0x0808941c; 0x0808939c is degenerate mid-body]
- CID: 0x151e (Last Turn)
- Dispatch entry: [93]
- Body: push {r4-r7,lr} + high-reg push; scan gP1SlotSetCodeArray (hand) + extended loop via
  gP1LifePoints; check find_effect_node_in_zone; write substate_d;
  loop body continues from bcs at 0x08089398 target 0x080893fe (inside 0x0808939c..0x0808941c degenerate span)
- BL targets: 0x0804ad48, 0x0803bba4 (eval_equip_placement_full_check), 0x0802fd60 (find_effect_node_in_zone), 0x0808d88c
- Pool: 0x0808940c=gP1LifePoints, 0x08089410=PLAYER_BLOCK_STRIDE, 0x08089414=gP1SlotSetCodeArray, 0x08089418=zone_query_hand_tag_12a1
- CID: REUSE LAST_TURN_CID
- Substate: 0xd
- Proposed name: `scan_zone_last_turn_substate_d`
- Confidence: high (body: placement check + find_node + write_d; Last Turn is a monster zone trigger)
- ASCII plate: `Equip zone scan callback for Last Turn (LAST_TURN_CID=0x151e, pw=28566710). r0=player_id. Gate: check_card_field5_is_nonzero + eval_equip_placement_full_check + find_effect_node_in_zone via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x0808939c is mid-body loop continuation (degenerate, bcs target). Dispatched from write table entry [93].`

### fn25: 0x0808941c  size=0x13c (316 B)
- CID(s): 0x1522 (Vampire Lord), 0x1746 (Vampire Lady)
- Dispatch entries: [94], [179]
- Body: push {r4-r7,lr}; three scan loops each calling write_equip_zone_entry_by_substate(substate_d);
  uses gP1LifePoints, gP1SlotSetCodeArray, zone_query_hand_tag_12a1; calls check_card_field5_is_nonzero
  and find_effect_node_in_zone for gate checks; multi-path due to Vampire Lord/Lady's various
  monster zone conditions
- BL targets: 0x0804ad48 (x1), 0x0802fd60 (x1), 0x0808d88c (x3), 0x080eedf8 (x2 get_card_extended_stat_field6)
- Pool: 0x080894a4=gP1LifePoints, 0x080894a8=PLAYER_BLOCK_STRIDE, 0x080894ac=gP1SlotSetCodeArray,
  0x080894b0=zone_query_hand_tag_12a1, 0x080894f8=gP1LifePoints, 0x080894fc=PLAYER_BLOCK_STRIDE,
  0x08089550=gP1LifePoints, 0x08089554=PLAYER_BLOCK_STRIDE
- CID: VAMPIRE_LORD_CID REUSE; VAMPIRE_LADY_CID REUSE
- Substate: 0xd (x3)
- Proposed name: `scan_zone_vampire_lord_lady_group_substate_d`
- Confidence: high (body: three write_d calls; Vampire Lord/Lady both affect monster zone)
- ASCII plate: `Equip zone scan callback for Vampire Lord/Lady group: Vampire Lord (VAMPIRE_LORD_CID=0x1522, pw=53839837), Vampire Lady (VAMPIRE_LADY_CID=0x1746, pw=26495087). r0=player_id. Three-loop scan with field5+find_node+field6 gates; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) x3. Dispatched from write table entries [94,179].`

### fn26: 0x08089558  size=0x0d4 (212 B)  [spans to 0x0808962c; 0x08089560 is degenerate mid-prologue]
- CID: 0x152f (Pyramid Turtle)
- Dispatch entry: [96]
- Body: push {r4-r7,lr}; high-reg save (mov r7,r10; mov r6,r9; mov r5,r8; push {r5,r6,r7});
  scan gP1SlotSetCodeArray (zone_query_hand_tag_12a1 filter); check_card_field5_is_nonzero;
  get_card_extended_stat_field8; eval_equip_placement_full_check; find_effect_node_in_zone;
  write substate_d; uses gP1SlotCountBase (0x0201c4f0)
- BL targets: 0x0804ad48, 0x080eef70 (get_card_extended_stat_something), 0x080eedf8, 0x0803bba4, 0x0802fd60, 0x0808d88c
- Pool: 0x08089618=gP1LifePoints, 0x0808961c=PLAYER_BLOCK_STRIDE, 0x08089620=gP1SlotSetCodeArray,
  0x08089624=zone_query_hand_tag_12a1, 0x08089628=gP1SlotCountBase
- CID: 0x152f NEW (Pyramid Turtle, 0 hits)
- Substate: 0xd
- Proposed name: `scan_zone_pyramid_turtle_substate_d`
- Confidence: high (body: full gate chain + write_d; Pyramid Turtle special-summons Zombies on destruction; addr 0x08089560 is mid-prologue degenerate)
- ASCII plate: `Equip zone scan callback for Pyramid Turtle (CID=0x152f, pw=77044671). r0=player_id. Gate: check_card_field5_is_nonzero + field8 + eval_equip_placement_full_check + find_effect_node_in_zone via gP1SlotSetCodeArray[zone_query_hand_tag_12a1]; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addr 0x08089560 is mid-prologue degenerate (second push in high-reg save). Dispatched from write table entry [96].`

---

## REF_SLOTS (createDWordWithRef plan)

Per Seg-4a precedent: every pool DWord holding an EWRAM address gets
createDWordWithRef + RENAME so it exports as `.word gP1LifePoints` etc.

### gP1LifePoints = 0x0201c4e0 (ewram.inc) -- 23 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x08088964 | fn01 | ptr_lp_88964 |
| 0x080889bc | fn02 | ptr_lp_889bc |
| 0x08088a2c | fn03 | ptr_lp_88a2c |
| 0x08088acc | fn04 | ptr_lp_88acc |
| 0x08088b24 | fn05 | ptr_lp_88b24 |
| 0x08088c84 | fn06 | ptr_lp_88c84 |
| 0x08088d1c | fn07 | ptr_lp_88d1c |
| 0x08088dac | fn08 | ptr_lp_88dac |
| 0x08088e04 | fn09 | ptr_lp_88e04 |
| 0x08088e5c | fn10 | ptr_lp_88e5c |
| 0x08088ecc | fn11 | ptr_lp_88ecc |
| 0x08089148 | fn17 | ptr_lp_89148 |
| 0x080891bc | fn18 | ptr_lp_891bc |
| 0x08089278 | fn19 | ptr_lp_89278 |
| 0x080892ac | fn20 | ptr_lp_892ac |
| 0x08089330 | fn21 | ptr_lp_89330 |
| 0x08089370 | fn22 | ptr_lp_89370 |
| 0x0808940c | fn23 | ptr_lp_8940c |
| 0x080894a4 | fn25 | ptr_lp_894a4 |
| 0x080894f8 | fn25 | ptr_lp_894f8 |
| 0x08089550 | fn25 | ptr_lp_89550 |
| 0x08089618 | fn26 | ptr_lp_89618 |
| 0x0808905c | fn14 | ptr_lp_8905c |

REF count gP1LifePoints: **23**

### gP1SlotSetCodeArray = 0x0201c740 (ewram.inc) -- 6 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x08088c90 | fn06 | ptr_sca_88c90 |
| 0x08088d24 | fn07 | ptr_sca_88d24 |
| 0x08089064 | fn14 | ptr_sca_89064 |
| 0x08089414 | fn23 | ptr_sca_89414 |
| 0x080894ac | fn25 | ptr_sca_894ac |
| 0x08089620 | fn26 | ptr_sca_89620 |

REF count gP1SlotSetCodeArray: **6**

### gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 4 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x08088db4 | fn08 | ptr_hsa_88db4 |
| 0x08088f78 | fn12 | ptr_hsa_88f78 |
| 0x080891c4 | fn18 | ptr_hsa_891c4 |
| 0x08089280 | fn19 | ptr_hsa_89280 |

REF count gP1HandSlotArray: **4**

### gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 3 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x08088c8c | fn06 | ptr_fac_88c8c |
| 0x08088fdc | fn13 | ptr_fac_88fdc |
| 0x08089110 | fn16 | ptr_fac_89110 |

REF count gP1FieldArrayCBase: **3**

### gP1ChainZoneArray = 0x0201c880 (ewram.inc line 336) -- 1 slot

| slot addr | fn | label |
|-----------|----|----|
| 0x08088c98 | fn06 | ptr_cza_88c98 |

### gP1AltHandSlotArray = 0x0201cab0 (ewram.inc line 338) -- 1 slot

| slot addr | fn | label |
|-----------|----|----|
| 0x08088ed4 | fn11 | ptr_aha_88ed4 |

### gP1SlotCountBase = 0x0201c4f0 (ewram.inc) -- 1 slot

| slot addr | fn | label |
|-----------|----|----|
| 0x08089628 | fn26 | ptr_scb_89628 |

### gDuelPhaseFlags = 0x0201b290 (ewram.inc) -- 1 slot

| slot addr | fn | label |
|-----------|----|----|
| 0x08088f68 | fn12 | ptr_dpf_88f68 |

Note: fn12 has two ldr instructions that both load gDuelPhaseFlags. First ldr at 0x08088ede
(opcode 0x4922, imm8=0x22): pool = ((0x08088ede+4)&~3) + 0x22*4 = 0x08088f68.
Second ldr at 0x08088f56 (opcode 0x4904, imm8=0x04): pool = ((0x08088f56+4)&~3) + 0x04*4 = 0x08088f68.
Both compute to the same word address. createDWord ONCE at 0x08088f68; do NOT createDWord at 0x08088f56.

REF count gDuelPhaseFlags: **1**

### Total REF count: 23+6+4+3+1+1+1+1 = **40**

---

## EQ_SLOTS (CID equates)

### NEW CIDs to add to card_info.inc (16 entries, individual grep = 0 hits each):

```
.equ KYCOO_THE_GHOST_DESTROYER_CID, 0x00001480  @ Kycoo the Ghost Destroyer (pw=88240808; card_0958 slot=0x1480)
.equ FOOLISH_BURIAL_CID,            0x00001474  @ Foolish Burial (pw=81439173; card_0948 slot=0x1474)
.equ INFERNAL_FLAME_EMPEROR_CID,    0x000018e0  @ Infernal Flame Emperor (pw=19847532; card_1870 slot=0x18E0)
.equ SPIRIT_OF_FLAMES_CID,          0x00001484  @ Spirit of Flames (pw=13522325; card_0962 slot=0x1484)
.equ GARUDA_THE_WIND_SPIRIT_CID,    0x00001487  @ Garuda the Wind Spirit (pw=12800777; card_0965 slot=0x1487)
.equ LEKUNGA_CID,                   0x000015bc  @ Lekunga (pw=62543393; card_1212 slot=0x15BC)
.equ FREED_THE_BRAVE_WANDERER_CID,  0x000016c0  @ Freed the Brave Wanderer (pw=16556849; card_1411 slot=0x16C0)
.equ GIGANTES_CID,                  0x000016c7  @ Gigantes (pw=47606319; card_1417 slot=0x16C7)
.equ SUPPLY_CID,                    0x0000148b  @ Supply (pw=44072894; card_0969 slot=0x148B)
.equ SKULL_LAIR_CID,                0x00001490  @ Skull Lair (pw=06733059; card_0974 slot=0x1490)
.equ REINFORCEMENT_OF_THE_ARMY_CID, 0x000014d0  @ Reinforcement of the Army (pw=32807846; card_1024 slot=0x14D0)
.equ DES_FERAL_IMP_CID,             0x000014ef  @ Des Feral Imp (pw=81985784; card_1055 slot=0x14EF)
.equ SILENT_FIEND_CID,              0x000014f7  @ Silent Fiend (pw=42534368; card_1061 slot=0x14F7)
.equ SUPER_ROBOLADY_CID,            0x00001507  @ Super Robolady (pw=75923050; card_1074 slot=0x1507)
.equ SUPER_ROBOYAROU_CID,           0x00001508  @ Super Roboyarou (pw=01412158; card_1075 slot=0x1508)
.equ PYRAMID_TURTLE_CID,            0x0000152f  @ Pyramid Turtle (pw=77044671; card_1108 slot=0x152F)
```

Count: **16 NEW**

### REUSE CIDs (already in card_info.inc, DO NOT add):
DARK_BLADE_THE_DRAGON_KNIGHT_CID(0x183c), BAZOO_THE_SOUL_EATER_CID(0x1482),
DARK_NECROFEAR_CID(0x1466), MEGAROCK_DRAGON_CID(0x18b4), DOOM_DOZER_CID(0x19ca),
DESTINY_BOARD_CID(0x1468), DARK_SAGE_CID(0x146e), CATHEDRAL_OF_NOBLES_CID(0x146f),
SOUL_OF_PURITY_CID(0x1483), AQUA_SPIRIT_CID(0x1485), ROCK_SPIRIT_CID(0x1486),
STRIKE_NINJA_CID(0x16b9), INFERNO_CID(0x16c5), FENRIR_CID(0x16c6), SILPHEED_CID(0x16c8),
MIRACLE_DIG_CID(0x149e), ROPE_OF_LIFE_CID(0x14a7), MARAUDING_CAPTAIN_CID(0x14c6),
cid_135b(0x135b), FREED_THE_MATCHLESS_GENERAL_CID(0x14c4),
THE_WARRIOR_RETURNING_ALIVE_CID(0x14d2), SPIRIT_RYU_CID(0x14d7), AGIDO_CID(0x14f6),
SOUL_RESURRECTION_CID(0x17b7), MAHARAGHI_CID(0x14fd), KELDO_CID(0x14e7),
DISAPPEAR_CID(0x1515), DIMENSION_JAR_CID(0x15dd), DD_GUIDE_CID(0x19c0),
LAST_TURN_CID(0x151e), VAMPIRE_LORD_CID(0x1522), VAMPIRE_LADY_CID(0x1746)

### Scalar pool equates (existing constants):
- 0x00000868 = PLAYER_BLOCK_STRIDE (existing, ewram.inc)
- 0x000012a1 = zone_query_hand_tag_12a1 (existing label)
- 0x000004cc = LP_BAR_ANIM_STATE_OFF (existing ewram.inc line 405)
- 0x000004d4 = SPRITE_ROW_ENTRY_DATA_OFF (existing ewram.inc line 411)

---

## Literal Pool DWord List (createDWord required)

All pool addresses inside [0x08088904, 0x0808962c) -- correct formula: `((instr_addr+4)&~3)+imm8*4`

**fn01** (0x08088904): 0x08088964, 0x08088968
**fn02** (0x0808896c): 0x080889bc, 0x080889c0
**fn03** (0x080889c4): 0x08088a2c, 0x08088a30
**fn04** (0x08088a34): 0x08088acc, 0x08088ad0
**fn05** (0x08088ad4): 0x08088b24, 0x08088b28
**fn06** (0x08088b2c): 0x08088c84, 0x08088c88, 0x08088c8c, 0x08088c90, 0x08088c94, 0x08088c98
**fn07** (0x08088c9c): 0x08088d1c, 0x08088d20, 0x08088d24, 0x08088d28
**fn08** (0x08088d2c): 0x08088dac, 0x08088db0, 0x08088db4
**fn09** (0x08088db8): 0x08088e04, 0x08088e08
**fn10** (0x08088e0c): 0x08088e5c, 0x08088e60
**fn11** (0x08088e64): 0x08088ecc, 0x08088ed0, 0x08088ed4
**fn12** (0x08088ed8): 0x08088f68(gDuelPhaseFlags), 0x08088f6c(LP_BAR_ANIM_STATE_OFF), 0x08088f70(SPRITE_ROW_ENTRY_DATA_OFF), 0x08088f74, 0x08088f78
  [Note: two ldr ops both resolve to 0x08088f68; 0x08088f56 is NOT a pool address -- createDWord only at 0x08088f68]
**fn13** (0x08088f7c): 0x08088fd8, 0x08088fdc
**fn14** (0x08088fe0): 0x0808905c, 0x08089060, 0x08089064
**fn15** (0x08089068): 0x080890b8, 0x080890bc
**fn16** (0x080890c0): 0x0808910c, 0x08089110
**fn17** (0x08089114): 0x08089148, 0x0808914c
**fn18** (0x08089150): 0x080891bc, 0x080891c0, 0x080891c4, 0x080891f4
**fn19** (0x080891f8): 0x08089278, 0x0808927c, 0x08089280
**fn20** (0x08089284): 0x080892ac, 0x080892b0
**fn21** (0x080892b4): 0x080892cc(SUPER_ROBOLADY), 0x080892d0(SUPER_ROBOYAROU pad), 0x080892dc(SUPER_ROBOYAROU), 0x08089330, 0x08089334
**fn22** (0x08089338): 0x08089370, 0x08089374
**fn23** (0x08089378, combined with 0x0808939c): 0x0808940c, 0x08089410, 0x08089414, 0x08089418
**fn25** (0x0808941c): 0x080894a4, 0x080894a8, 0x080894ac, 0x080894b0, 0x080894f8, 0x080894fc, 0x08089550, 0x08089554
**fn26** (0x08089558, combined with 0x08089560): 0x08089618, 0x0808961c, 0x08089620, 0x08089624, 0x08089628

Total pool dwords: **~75**

---

## disasm Plan (R4)

**Range**: [0x08088904, 0x0808962c)
**Mode**: THUMB

Fixer script steps:
1. clearListing 0x08088904..0x0808962c
2. setTMode THUMB for entire range
3. Per-function DisassembleCommand in address order (25 entries):
   0x08088904, 0x0808896c, 0x080889c4, 0x08088a34, 0x08088ad4,
   0x08088b2c, 0x08088c9c, 0x08088d2c, 0x08088db8, 0x08088e0c,
   0x08088e64, 0x08088ed8, 0x08088f7c, 0x08088fe0, 0x08089068,
   0x080890c0, 0x08089114, 0x08089150, 0x080891f8, 0x08089284,
   0x080892b4, 0x08089338, 0x08089378, 0x0808941c, 0x08089558
4. createFunction at each of the 25 entries above
5. force-createDWord for each pool address (~75 total listed above)
6. Do NOT createFunction at degenerate addresses: 0x0808939c, 0x08089560

**Post-disasm gate**: grep `ROM_INCBIN\|\.byte` in asm/11_effect_slot_puzzletext.s lines
covering 0x08088904..0x0808962c must return 0 matches after export.

---

## carve Plan

None -- no data tables or code needing carve in this segment.

## §5.1 Entries

None -- all bytes in [0x08088904, 0x0808962c) are part of real functions (0 unref orphans).

---

## Consumer Evidence Summary

- All 25 functions called via dispatch table 0x09e5a128 `{CID, fn_ptr+1}`, same caller pattern as Seg-4a.
  Caller: dispatch_equip_zone_write_by_substate_range (0x0808d7f4).
- write_equip_zone_entry_by_substate (0x0808d88c): asm/11_effect_slot_puzzletext.s line ~6189. Confidence: high.
- check_card_field5_is_nonzero (0x0804ad48): asm/05_equip_eligibility_a.s line 3883. Confidence: high.
- eval_equip_placement_full_check (0x0803bba4): asm/03_equip_chain_hand.s line ~12838. Confidence: high.
- find_effect_node_in_zone (0x0802fd60): asm/02_text_lp_fieldspell.s line 8191. Confidence: high.
- find_hand_slot_idx_by_set_code (0x0803123c): asm/02_text_lp_fieldspell.s line 11298. Confidence: high.
- eval_equip_bonus_for_slot (0x080377b0): asm/03_equip_chain_hand.s line 3348. Confidence: high.
- get_zone_card_attribute_by_type (0x0803b618): asm/03_equip_chain_hand.s line 12082. Confidence: high.
- map_field8_to_card_type_category (0x0804a9dc): asm/05_equip_eligibility_a.s line 3518. Confidence: high.
- check_card_is_equip_target_eligible (0x0804bb6c): asm/05_equip_eligibility_a.s line 6066. Confidence: high.
- check_card_id_is_equip_excluded_range (0x0804bc58): asm/05_equip_eligibility_a.s line 6203. Confidence: high.
- LP_BAR_ANIM_STATE_OFF (0x4cc) and SPRITE_ROW_ENTRY_DATA_OFF (0x4d4): ewram.inc lines 405, 411. Confidence: high.
- gP1ChainZoneArray (0x0201c880): ewram.inc line 336. Confidence: high.
- gP1AltHandSlotArray (0x0201cab0): ewram.inc line 338. Confidence: high.

---

## Self-Check (Phase 4)

1. **Pool values (corrected formula)**: all pool addresses re-verified using
   `pool = ((instr_addr+4) & ~3) + imm8*4` (not `(pc+2)&~2+4+imm8*4`); fn18 pool at
   0x080891c4=gP1HandSlotArray confirmed; fn18 mystery 0x280... eliminated.
2. **Degenerate entries**: 2 confirmed (0x0808939c: bcs jump-target mid-fn23; 0x08089560: second-push mid-fn26). Neither in dispatch table.
3. **Plate text**: all ASCII only, no CJK, all <=500 chars (verified by inspection above; longest ~490 chars fn08).
4. **Slot names**: all `^[a-z][a-z0-9_]+$`; multiple gP1LifePoints slots disambiguated by _88964/_889bc/etc.
5. **CID value greps**: 16 NEW confirmed 0 hits via `re.search(r'0x0*%04X\b', content, re.I)` individually; 32 REUSE confirmed present.
6. **fn21 pool note**: 0x080892d4 is CODE bytes (reachable via beq from 0x080892c0); NOT a CID pool dword. Only 0x080892cc and 0x080892dc hold valid CID values (0x1507 and 0x1508 respectively).
7. **fn18 pool verification**: second PLAYER_BLOCK_STRIDE slot at 0x080891f4 -- ldr r3,[pc,#24] at 0x080891da: pool = ((0x080891de)&~3)+24 = 0x080891dc+24 = 0x080891f4. Value at 0x080891f4 = 0x00000868 confirmed.
8. **fn12 gDuelPhaseFlags slots**: fn12 has two ldr instructions loading gDuelPhaseFlags. First: ldr r1 at 0x08088ede (opcode 0x4922, imm8=0x22) -> pool = ((0x08088ede+4)&~3) + 0x22*4 = 0x08088f68 = 0x0201b290. Second: ldr r1 at 0x08088f56 (opcode 0x4904, imm8=0x04) -> pool = ((0x08088f56+4)&~3) + 0x04*4 = 0x08088f68 (SAME slot). createDWord ONCE at 0x08088f68 only. Address 0x08088f56 is a THUMB instruction (not a pool word).
9. **fn14 gP1LifePoints slot**: fn14 pool at 0x0808905c = 0x0201c4e0 (gP1LifePoints). Added to REF table. Total REF count corrected to 40.
