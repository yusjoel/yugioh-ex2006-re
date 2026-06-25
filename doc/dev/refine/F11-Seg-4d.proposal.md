# Refine Proposal: F11-Seg-4d  [0x0808a2ac..0x0808ad8c)

## Segment Survey

- ROM range: `[0x0808a2ac, 0x0808ad8c)` = 0xAE0 bytes (2784 B)
- Source: one-liner `ROM_INCBIN 0x8a2ac, <size>` (giant block in asm/11, after Seg-4c carved 0x0808962c..0x0808a2ac)
- Boundary at 0x0808a2ac = first entry after Seg-4c end; boundary at 0x0808ad8c = next segment start
- Functions: **24 real functions** (27 strong entries - 3 degenerate = 24 real)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools

### Function type: equip zone scan callbacks (same pattern as Seg-4a/4b/4c)

All 24 real functions are equip zone scan callbacks dispatched from the 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

---

## Degenerate Strong Entry Analysis (3 of 27)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808a44c | Mid-loop LDR instruction at offset+0xc inside fn05 (0x0808a440..0x0808a498). ROM bytes: `4911` = LDR r1,[PC+#68], not a push prologue. No dispatch table entry points here. fn05 real span = 0x0808a440..0x0808a498 (size=0x58). | bytes 4911 (LDR PC-relative); fn05 code continues at 0x0808a44e without gap; first `d215` branch at 0x0808a45c closes original loop started at 0x0808a440 |
| 0x0808a450 | Mid-loop code at offset+0x10 inside fn05. ROM bytes: `434a` = MUL r2,r1 (THUMB format). Not a push prologue. Falls through from LDR r1 at 0x0808a44c. No dispatch table entry. | bytes 434a (MUL Rd,Rm); fn05 epilogue at 0x0808a48a/8c/8e (bcf0/bc01/4700) confirms fn05 ends at 0x0808a498 |
| 0x0808a996 | Mid-body instruction at offset+0x1e inside fn16 (0x0808a978..0x0808a9b4). ROM bytes: `210f` = MOVS r1,#0xf. This is the `movs r1,#0xf` arg-set before the write_equip BL at 0x0808a99a, not a function entry. No dispatch table entry. | bytes 210f (MOVS r1,imm8); fn16 starts at 0x0808a978 (b570 push {r4,r5,r6,r7,lr}); 0x0808a996 = 0x978+0x1e falls inside the body before the sole BL |

### Weak Entry Analysis (3 flagged)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808a974 | Literal pool value `0x00000868` = PLAYER_BLOCK_STRIDE inside fn15 pool area (0x0808a920..0x0808a978). h16=`0868`. | 0x0808a970=gP1LifePoints pool, 0x0808a974=PLAYER_BLOCK_STRIDE pool, both trailing after fn15 epilogue bc01/4700 at 0x0808a96c/6e |
| 0x0808a9c2 | Mid-code `1c11` = MOV r1,r2 inside fn17 body (0x0808a9b4..0x0808aa38). Not a push prologue. | fn17 prologue at 0x0808a9b4 b5f0; 0x0808a9c2 = 0x9b4+0xe is inside the loop body; no dispatch entry |
| 0x0808ab2c | Epilogue bytes `bcf0 bc01 0047` inside fn19 body (0x0808aab4..0x0808ab44). h16=`bcf0`. | fn19 epilogue at 0x0808ab2c..0x0808ab32 (bc70/bc01/4700) is the fn19 POP+BX; fn19 ends at 0x0808ab44 |

---

## Dispatch Table CID Scan (all seg-4d entries, table at 0x09e5a128, 305 entries)

| fn | addr | CID(s) | entry indices | card name(s) |
|----|------|--------|---------------|-------------|
| fn01 | 0x0808a2ac | 0x1629 | [131] | Emblem of Dragon Destroyer |
| fn02 | 0x0808a378 | 0x162c, 0x184c | [132], [232] | ICID_RESERVED_A, ICID_RESERVED_B |
| fn03 | 0x0808a3b8 | 0x1628, 0x1656 | [130], [139] | Senri Eye; Dark Scorpion - Chick the Yellow |
| fn04 | 0x0808a3e8 | 0x1664 | [142] | Fairy of the Spring |
| fn05 | 0x0808a440 | 0x166b | [143] | Arsenal Robber |
| fn06 | 0x0808a498 | 0x1678 | [144] | Magical Dimension |
| fn07 | 0x0808a4f0 | 0x1686 | [147] | Dark Scorpion - Meanae the Thorn |
| fn08 | 0x0808a598 | 0x1689 | [148] | Iron Blacksmith Kotetsu |
| fn09 | 0x0808a5f0 | 0x169f | [149] | Pandemonium |
| fn10 | 0x0808a67c | 0x16a4 | [150] | Archfiend's Roar |
| fn11 | 0x0808a708 | 0x16a8 | [151] | Ray of Hope |
| fn12 | 0x0808a788 | 0x16c2 | [155] | Witch Doctor of Chaos |
| fn13 | 0x0808a83c | 0x16c4 | [156] | Chaosrider Gustaph |
| fn14 | 0x0808a894 | 0x16c9, 0x16cb, 0x16e4 | [161],[162],[166] | Chaos Sorcerer; Black Luster Soldier - Envoy of the Beginning; Chaos Emperor Dragon - Envoy of the End |
| fn15 | 0x0808a920 | 0x16d5 | [163] | Recycle |
| fn16 | 0x0808a978 | 0x16d6 | [164] | Primal Seed |
| fn17 | 0x0808a9b4 | 0x16d8, 0x1712, 0x17be, 0x191e | [165],[171],[197],[267] | Dimension Distortion; Dimension Fusion; Return from the Different Dimension; D.D.M. - Different Dimension Master |
| fn18 | 0x0808aa38 | 0x170c | [170] | Manju of the Ten Thousand Hands |
| fn19 | 0x0808aab4 | 0x1714 | [173] | Salvage |
| fn20 | 0x0808ab44 | 0x1715 | [174] | Ultra Evolution Pill |
| fn21 | 0x0808ab9c | 0x1717 | [175] | Jade Insect Whistle |
| fn22 | 0x0808abf4 | 0x1727, 0x1754 | [176],[181] | Abyss Soldier; Lady Ninja Yae |
| fn23 | 0x0808ac48 | 0x1647 | [137] | Arsenal Summoner |
| fn24 | 0x0808aca0 | 0x164a, 0x16bc, 0x1745 | [138],[153],[178] | Guardian Elma; Chopman the Desperate Outlaw; The Kick Man |

Size check: fn01 starts 0x0808a2ac, fn24 ends 0x0808ad8c; total = 0xAE0 = 2784 B. Confirmed.

---

## Function Naming Table (24 real functions)

Substate semantics (from existing plate for write_equip_zone_entry_by_substate):
- 0xb = field-spell zone type B
- 0xc = chain zone type C
- 0xd = monster zone type D
- 0xe = hand slot type E
- 0xf = graveyard type F

### fn01: 0x0808a2ac  size=0x0cc (204 B)
- CID(s): 0x1629 (Emblem of Dragon Destroyer), pool partner: 0x1377 (BUSTER_BLADER_CID), 0x159d (NECROVALLEY_CID)
- Dispatch entries: [131]
- Body: push {r4..r7,lr} + extra push; TWO-LOOP structure:
  loop1 scans gP1LifePoints monster zone at +0x10; check_card_pair_allowed(0x804ab4c); write substate_d;
  loop2 scans gP1LifePoints at +0x14; count_field_copies_of_card(0x803279c); check_card_pair_allowed; write substate_e
- BL targets: 0x0804ab4c (check_card_pair_allowed), 0x0808d88c (x2), 0x0803279c (count_field_copies_of_card)
- Pool: 0x0808a364=EMBLEM_OF_DRAGON_DESTROYER_CID(0x1629), 0x0808a368=BUSTER_BLADER_CID(0x1377), 0x0808a36c=gP1LifePoints, 0x0808a370=PLAYER_BLOCK_STRIDE, 0x0808a374=NECROVALLEY_CID(0x159d)
- CID status: EMBLEM_OF_DRAGON_DESTROYER_CID REUSE; BUSTER_BLADER_CID REUSE; NECROVALLEY_CID REUSE (all in card_info.inc)
- Substates: 0xd (loop1), 0xe (loop2)
- Proposed name: `scan_zone_emblem_of_dragon_destroyer_substate_de`
- Confidence: high (body: two partner-CID pool values + check_card_pair_allowed + count_copies gate; Emblem of Dragon Destroyer equips to Buster Blader + Necrovalley; dispatch table entry [131])
- ASCII plate (len=449): `Equip zone scan for Emblem of Dragon Destroyer (EMBLEM_OF_DRAGON_DESTROYER_CID=0x1629, pw=06390406). Two loops via gP1LifePoints: (1) +0x10 monster zone, check_card_pair_allowed gate, write substate_d; (2) +0x14, count_field_copies_of_card + check_card_pair_allowed gate, write substate_e. Partner pool: BUSTER_BLADER_CID=0x1377 + NECROVALLEY_CID=0x159d. Dispatch table entry [131].`

### fn02: 0x0808a378  size=0x040 (64 B)
- CID(s): 0x162c (ICID_RESERVED_A), 0x184c (ICID_RESERVED_B)
- Dispatch entries: [132], [232]
- Body: push {r4,r5,lr}; scan gP1LifePoints monster zone; no filter gate; write substate_d; simple single loop
- BL targets: 0x0808d88c (write_equip_zone_entry_by_substate only)
- Pool: 0x0808a3b0=gP1LifePoints, 0x0808a3b4=PLAYER_BLOCK_STRIDE
- CID status: ICID_RESERVED_A(0x162c) REUSE; ICID_RESERVED_B(0x184c) REUSE
- Substate: 0xd
- Proposed name: `scan_zone_reserved_icid_group_substate_d`
- Confidence: high (body: no-filter monster zone scan; both CIDs are reserved internal ICIDs per existing card_info.inc definitions; write_d only)
- ASCII plate (len=290): `Equip zone scan for reserved ICID group: ICID_RESERVED_A(0x162c) + ICID_RESERVED_B(0x184c). Monster zone scan via gP1LifePoints+STRIDE; no filter gate; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entries [132,232].`

### fn03: 0x0808a3b8  size=0x030 (48 B)
- CID(s): 0x1628 (Senri Eye), 0x1656 (Dark Scorpion - Chick the Yellow)
- Dispatch entries: [130], [139]
- Body: push {lr}; scan gP1LifePoints monster zone; no filter gate; write substate_d; tiny single-loop (LDR r2=gP1LifePoints from pool, loop over slots, BL write_equip)
- BL targets: 0x0808d88c only
- Pool: 0x0808a3e0=gP1LifePoints, 0x0808a3e4=PLAYER_BLOCK_STRIDE
- CID status: 0x1628 NEW (Senri Eye, grep=0 hits); DARK_SCORPION_CHICK_CID(0x1656) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808a3d4 before BL; MOVS r1,#1 at 0x0808a3bc = loop init decrement, not substate)
- Proposed name: `scan_zone_senri_eye_dark_scorpion_group_substate_d`
- Confidence: high (body: no-filter monster zone write_d; both cards are Dark Scorpion support; shared dispatch entry range [130,139])
- ASCII plate (len=308): `Equip zone scan for Senri Eye/Dark Scorpion Chick group: Senri Eye (CID=0x1628, pw=60391791), Dark Scorpion - Chick the Yellow (DARK_SCORPION_CHICK_CID=0x1656, pw=61587183). Monster zone scan; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entries [130,139].`

### fn04: 0x0808a3e8  size=0x058 (88 B)
- CID: 0x1664 (Fairy of the Spring)
- Dispatch entry: [142]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x14; get_card_extended_stat_field9 (0x080eee7c) gate (cmp>3, d104 branch); write substate_e
- BL targets: 0x080eee7c (get_card_extended_stat_field9), 0x0808d88c
- Pool: 0x0808a438=gP1LifePoints, 0x0808a43c=PLAYER_BLOCK_STRIDE
- CID status: FAIRY_OF_THE_SPRING_CID(0x1664) REUSE
- Substate: 0xe
- Proposed name: `scan_zone_fairy_of_the_spring_substate_e`
- Confidence: high (body: field9 gate + monster zone +0x14 + write_e; Fairy of the Spring targets equippable spellcasters)
- ASCII plate (len=286): `Equip zone scan for Fairy of the Spring (FAIRY_OF_THE_SPRING_CID=0x1664, pw=20188127). Monster zone at gP1LifePoints+0x14; gate: get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [142].`

### fn05: 0x0808a440  size=0x058 (88 B)  [spans 0x0808a44c and 0x0808a450 degenerate]
- CID: 0x166b (Arsenal Robber)
- Dispatch entry: [143]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x10; get_card_extended_stat_field9 (0x080eee7c) gate (cmp>3, d104 branch); write substate_d
- BL targets: 0x080eee7c, 0x0808d88c
- Pool: 0x0808a490=gP1LifePoints, 0x0808a494=PLAYER_BLOCK_STRIDE
- CID status: 0x166b NEW (Arsenal Robber, grep=0 hits)
- Substate: 0xd
- Note: 0x0808a44c (LDR r1,[PC+#n], mid-loop) and 0x0808a450 (MUL r2,r1) are degenerate strong entries falling inside the fn05 body
- Proposed name: `scan_zone_arsenal_robber_substate_d`
- Confidence: high (body: field9 gate + write_d; Arsenal Robber steals equip from opponent; addr 0x0808a44c/0x0808a450 are degenerate mid-loop)
- ASCII plate (len=315): `Equip zone scan for Arsenal Robber (CID=0x166b, pw=55348096). Monster zone at gP1LifePoints+0x10; gate: get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Addrs 0x0808a44c (LDR mid-loop) and 0x0808a450 (MUL mid-loop) are degenerate. Dispatch table entry [143].`

### fn06: 0x0808a498  size=0x058 (88 B)
- CID: 0x1678 (Magical Dimension)
- Dispatch entry: [144]
- Body: push {r4,r5,lr}; scan gP1FieldArrayCBase field spell zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field6 (0x080eedf8) + eval_equip_placement_full_check (0x0803bba4); cmp r0,#0x12 (d10b); write substate_b
- BL targets: 0x0804ad48, 0x080eedf8, 0x0803bba4, 0x0808d88c
- Pool: 0x0808a4e8=PLAYER_BLOCK_STRIDE, 0x0808a4ec=gP1FieldArrayCBase
- CID status: MAGICAL_DIMENSION_CID(0x1678) REUSE
- Substate: 0xb
- Proposed name: `scan_zone_magical_dimension_substate_b`
- Confidence: high (body: field5 + field6 + placement gates on field spell zone +0x10; Magical Dimension special-summons and destroys monsters; write_b = field spell zone)
- ASCII plate (len=330): `Equip zone scan for Magical Dimension (MAGICAL_DIMENSION_CID=0x1678, pw=28553439). Field spell zone via gP1FieldArrayCBase+0x10; gates: check_card_field5_is_nonzero + get_card_extended_stat_field6 + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [144].`

### fn07: 0x0808a4f0  size=0x0a8 (168 B)
- CID: 0x1686 (Dark Scorpion - Meanae the Thorn)
- Dispatch entry: [147]
- Body: push {r4..r7,lr}; TWO-LOOP structure over gP1LifePoints:
  loop1 scans monster zone at +0x10; check_card_is_dark_scorpion_type (0x0804b004) gate; write substate_d (MOVS r1,#0xd at 0x0808a528);
  `e026` branch forward (skips loop2 when loop1 continues); loop2 scans at +0x14; same check_card_is_dark_scorpion_type; write substate_e (MOVS r1,#0xe at 0x0808a578)
- BL targets: 0x0804b004 (x2), 0x0808d88c (x2)
- Pool: 0x0808a53c=gP1LifePoints(loop1), 0x0808a540=PLAYER_BLOCK_STRIDE(loop1); 0x0808a590=gP1LifePoints(loop2), 0x0808a594=PLAYER_BLOCK_STRIDE(loop2)
- CID status: DARK_SCORPION_MEANAE_CID(0x1686) REUSE
- Substates: 0xd (loop1), 0xe (loop2)
- Proposed name: `scan_zone_dark_scorpion_meanae_substate_de`
- Confidence: high (body: two separate gP1LifePoints loops both gated by is_dark_scorpion_type; Meanae the Thorn is a Dark Scorpion member equip; dual zone write d+e)
- ASCII plate (len=356): `Equip zone scan for Dark Scorpion - Meanae the Thorn (DARK_SCORPION_MEANAE_CID=0x1686, pw=74153887). Two loops over gP1LifePoints: (1) monster zone +0x10, is_dark_scorpion_type gate, write substate_d; (2) monster zone +0x14, is_dark_scorpion_type gate, write substate_e. Dispatch table entry [147].`

### fn08: 0x0808a598  size=0x058 (88 B)
- CID: 0x1689 (Iron Blacksmith Kotetsu)
- Dispatch entry: [148]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x10; get_card_extended_stat_field9 (0x080eee7c) gate (cmp>3, d104); write substate_d
- BL targets: 0x080eee7c, 0x0808d88c
- Pool: 0x0808a5e8=gP1LifePoints, 0x0808a5ec=PLAYER_BLOCK_STRIDE
- CID status: IRON_BLACKSMITH_KOTETSU_CID(0x1689) REUSE
- Substate: 0xd
- Proposed name: `scan_zone_iron_blacksmith_kotetsu_substate_d`
- Confidence: high (body: field9 gate + write_d; Iron Blacksmith Kotetsu lets player add an equip from deck)
- ASCII plate (len=271): `Equip zone scan for Iron Blacksmith Kotetsu (IRON_BLACKSMITH_KOTETSU_CID=0x1689, pw=73431236). Monster zone at gP1LifePoints+0x10; gate: get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [148].`

### fn09: 0x0808a5f0  size=0x08c (140 B)
- CID: 0x169f (Pandemonium)
- Dispatch entry: [149]
- Body: push {r4..r7,lr} + extra push (r8,r9); scan gP1LifePoints+gP1SlotSetCodeArray;
  gates: check_card_field5_is_nonzero (0x0804ad48) + check_card_is_archfiend_type (0x0804aea0) + get_card_extended_stat_field5 (0x080eee50) [cmp r0,r3 = Lv comparison]; write substate_d
- BL targets: 0x0804ad48, 0x0804aea0, 0x080eee50, 0x0808d88c
- Pool: 0x0808a670=gP1LifePoints, 0x0808a674=PLAYER_BLOCK_STRIDE, 0x0808a678=gP1SlotSetCodeArray
- CID status: PANDEMONIUM_CID(0x169f) REUSE
- Substate: 0xd
- Proposed name: `scan_zone_pandemonium_substate_d`
- Confidence: high (body: is_archfiend_type gate + field5_nonzero + field5 level compare; Pandemonium is a field spell supporting Archfiend monsters; zone scan via SlotSetCodeArray)
- ASCII plate (len=338): `Equip zone scan for Pandemonium (PANDEMONIUM_CID=0x169f, pw=94585852). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + check_card_is_archfiend_type + get_card_extended_stat_field5 level compare; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [149].`

### fn10: 0x0808a67c  size=0x08c (140 B)
- CID: 0x16a4 (Archfiend's Roar)
- Dispatch entry: [150]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1HandSlotArray;
  gates: check_card_field5_is_nonzero (0x0804ad48) + check_card_is_archfiend_type (0x0804aea0) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x0804aea0, 0x08037434, 0x0808d88c
- Pool: 0x0808a6fc=gP1LifePoints, 0x0808a700=PLAYER_BLOCK_STRIDE, 0x0808a704=gP1HandSlotArray
- CID status: EQUIP_LOCK_A_CID(0x16a4) REUSE
- Substate: 0xe
- Proposed name: `scan_zone_archfiend_roar_substate_e`
- Confidence: high (body: is_archfiend_type + equip_eligible + hand zone; Archfiend's Roar special-summons an Archfiend from GY; write_e = hand slot)
- ASCII plate (len=320): `Equip zone scan for Archfiend's Roar (EQUIP_LOCK_A_CID=0x16a4, pw=56246017). Hand zone scan via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_is_archfiend_type + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [150].`

### fn11: 0x0808a708  size=0x080 (128 B)
- CID: 0x16a8 (Ray of Hope)
- Dispatch entry: [151]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1HandSlotArray;
  gates: check_card_field5_is_nonzero (0x0804ad48) + check_card_stat_field7_equals (0x08030b70, arg=1) + write substate_e
- BL targets: 0x0804ad48, 0x08030b70, 0x0808d88c
- Pool: 0x0808a77c=gP1LifePoints, 0x0808a780=PLAYER_BLOCK_STRIDE, 0x0808a784=gP1HandSlotArray
- CID status: RAY_OF_HOPE_CID(0x16a8) REUSE
- Substate: 0xe (MOVS r1,#0x1 at 0x0808a74c is arg to check_stat_field7; MOVS r1,#0xe at 0x0808a758 is write_equip arg)
- Proposed name: `scan_zone_ray_of_hope_substate_e`
- Confidence: high (body: field5 + stat_field7==1 (Light attribute) + hand zone; Ray of Hope returns a Light monster from GY to deck)
- ASCII plate (len=299): `Equip zone scan for Ray of Hope (RAY_OF_HOPE_CID=0x16a8, pw=82529174). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [151].`

### fn12: 0x0808a788  size=0x0b4 (180 B)
- CID: 0x16c2 (Witch Doctor of Chaos)
- Dispatch entry: [155]
- Body: push {r4..r7,lr} + extra push (r8,r9); TWO-LOOP structure via gP1FieldArrayCBase:
  loop1 scans zone at +0x10 (field); check_card_field5_is_nonzero gate; write substate_e;
  loop2 scans zone at +0x14 (second pass); check_card_field5_is_nonzero gate; write substate_e
- BL targets: 0x0804ad48 (x2), 0x0808d88c (x2)
- Pool: 0x0808a834=gP1LifePoints, 0x0808a838=PLAYER_BLOCK_STRIDE
- CID status: WITCH_DOCTOR_OF_CHAOS_CID(0x16c2) REUSE
- Substates: 0xe (both loops, MOVS r1,#0xe at 0x0808a7d0 and 0x0808a816)
- Note: MOVS r1,#0x1 at 0x0808a796 is initial loop control, not a substate arg
- Proposed name: `scan_zone_witch_doctor_of_chaos_substate_e`
- Confidence: high (body: two-pass field5_nonzero gate + write_e; Witch Doctor of Chaos is a DARK Spellcaster targeting monsters; two-loop structure covers field + extra slot range)
- ASCII plate (len=316): `Equip zone scan for Witch Doctor of Chaos (WITCH_DOCTOR_OF_CHAOS_CID=0x16c2, pw=75946257). Two loops via gP1LifePoints; both gate: check_card_field5_is_nonzero; both write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [155].`

### fn13: 0x0808a83c  size=0x058 (88 B)
- CID: 0x16c4 (Chaosrider Gustaph)
- Dispatch entry: [156]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x14; get_card_extended_stat_field6 (0x080eedf8) gate (cmp r0,#0x16, d104); write substate_e
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x0808a88c=gP1LifePoints, 0x0808a890=PLAYER_BLOCK_STRIDE
- CID status: 0x16c4 NEW (Chaosrider Gustaph, grep=0 hits)
- Substate: 0xe
- Proposed name: `scan_zone_chaosrider_gustaph_substate_e`
- Confidence: high (body: field6==0x16 (RACE_SPELL=22) gate + monster zone +0x14 + write_e; Chaosrider Gustaph is a DARK Warrior that removes Spells from GY)
- ASCII plate (len=271): `Equip zone scan for Chaosrider Gustaph (CID=0x16c4, pw=47829960). Monster zone at gP1LifePoints+0x14; gate: get_card_extended_stat_field6==0x16 (Spell type); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [156].`

### fn14: 0x0808a894  size=0x08c (140 B)
- CID(s): 0x16c9 (Chaos Sorcerer), 0x16cb (Black Luster Soldier - Envoy of the Beginning), 0x16e4 (Chaos Emperor Dragon - Envoy of the End)
- Dispatch entries: [161], [162], [166]
- Body: push {r4..r7,lr} + extra push (r8,r9); scan gP1LifePoints+gP1HandSlotArray;
  BL check_card_field5_is_nonzero (0x0804ad48); d00e branch on zero;
  MOVS r1,#1: d000; MOVS r1,#2: BL check_card_stat_field7_equals (0x08030b70, arg=2 = Dark attribute);
  MOVS r1,#0xe; BL write_equip(e)
- BL targets: 0x0804ad48, 0x08030b70, 0x0808d88c
- Pool: 0x0808a914=gP1LifePoints, 0x0808a918=PLAYER_BLOCK_STRIDE, 0x0808a91c=gP1HandSlotArray
- CID status: CHAOS_SORCERER_CID(0x16c9) REUSE; BLACK_LUSTER_SOLDIER_ENVOY_CID(0x16cb) REUSE; CHAOS_EMPEROR_DRAGON_CID(0x16e4) REUSE
- Substate: 0xe
- Note: MOVS r1,#1 at 0x0808a8da + d000 branch; MOVS r1,#2 at 0x0808a8e2 = arg to check_stat_field7 = Dark attribute check
- Proposed name: `scan_zone_chaos_envoy_group_substate_e`
- Confidence: high (body: field5 + stat_field7==2 (Dark attr) + hand zone; all 3 cards are Chaos Envoys requiring LIGHT+DARK in GY; write_e = hand slot; group dispatch entries [161,162,166])
- ASCII plate (len=484): `Equip zone scan for Chaos Envoy group: Chaos Sorcerer (CHAOS_SORCERER_CID=0x16c9, pw=09596126), Black Luster Soldier - Envoy of the Beginning (BLACK_LUSTER_SOLDIER_ENVOY_CID=0x16cb, pw=72989439), Chaos Emperor Dragon - Envoy of the End (CHAOS_EMPEROR_DRAGON_CID=0x16e4, pw=82301904). Hand zone scan; gates: check_card_field5_is_nonzero + check_card_stat_field7_equals(2) (Dark attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entries [161,162,166].`

### fn15: 0x0808a920  size=0x058 (88 B)
- CID: 0x16d5 (Recycle)
- Dispatch entry: [163]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x14; get_card_extended_stat_field6 (0x080eedf8) gate (d104); write substate_e
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x0808a970=gP1LifePoints, 0x0808a974=PLAYER_BLOCK_STRIDE
- Note: 0x0808a974 is a weak entry candidate -- it is the pool literal for PLAYER_BLOCK_STRIDE (0x00000868), correctly identified as pool data, not a function entry
- CID status: RECYCLE_CID(0x16d5) REUSE
- Substate: 0xe
- Proposed name: `scan_zone_recycle_substate_e`
- Confidence: high (body: field6 gate + monster zone +0x14 + write_e; Recycle places monsters back to deck from GY)
- ASCII plate (len=261): `Equip zone scan for Recycle (RECYCLE_CID=0x16d5, pw=96316857). Monster zone at gP1LifePoints+0x14; gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [163].`

### fn16: 0x0808a978  size=0x03c (60 B)  [spans 0x0808a996 degenerate]
- CID: 0x16d6 (Primal Seed)
- Dispatch entry: [164]
- Body: push {r4,r5,lr}; scan gP1LifePoints GY zone at +0x1c offset; no filter gate beyond slot compare; write substate_f (MOVS r1,#0xf at 0x0808a996 inside body, confirmed as arg to write_equip not a fn entry)
- BL targets: 0x0808d88c only
- Pool: 0x0808a9ac=gP1LifePoints, 0x0808a9b0=PLAYER_BLOCK_STRIDE
- CID status: PRIMAL_SEED_CID(0x16d6) REUSE
- Substate: 0xf (MOVS r1,#0xf at 0x0808a996 = write arg; degenerate entry excluded)
- Proposed name: `scan_zone_primal_seed_substate_f`
- Confidence: high (body: GY zone scan at +0x1c + write_f; Primal Seed retrieves removed-from-game BLS+CED cards)
- ASCII plate (len=222): `Equip zone scan for Primal Seed (PRIMAL_SEED_CID=0x16d6, pw=23701465). GY zone scan at gP1LifePoints+0x1c; write_equip_zone_entry_by_substate(player_id, 0xf, slot_idx). Dispatch table entry [164].`

### fn17: 0x0808a9b4  size=0x084 (132 B)
- CID(s): 0x16d8 (Dimension Distortion), 0x1712 (Dimension Fusion), 0x17be (Return from the Different Dimension), 0x191e (D.D.M. - Different Dimension Master)
- Dispatch entries: [165], [171], [197], [267]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1AltHandSlotArray (0x0201cab0) at offset +0x1c;
  gates: check_card_field5_is_nonzero (0x0804ad48) + check_zone_slot_equip_eligible_alt (0x08037568) + get_zone_card_attribute_by_type (0x0803b618); write substate_f (MOVS r1,#0xf at 0x0808aa0c before final write_equip)
- BL targets: 0x0804ad48, 0x08037568 (check_zone_slot_equip_eligible_alt), 0x0803b618 (get_zone_card_attribute_by_type), 0x0808d88c
- Pool: 0x0808aa2c=gP1LifePoints, 0x0808aa30=PLAYER_BLOCK_STRIDE, 0x0808aa34=gP1AltHandSlotArray(0x0201cab0)
- CID status: 0x16d8 NEW (Dimension Distortion, grep=0 hits); DIMENSION_FUSION_CID(0x1712) REUSE; 0x17be NEW (Return from the Different Dimension, grep=0 hits); 0x191e NEW (D.D.M., grep=0 hits)
- Substate: 0xf (MOVS r1,#0xf at 0x0808a9fe before get_zone_card_attribute = possible field6 arg; MOVS r1,#0xf at 0x0808aa0c before write_equip = substate arg)
- Note: 0x0808a9c2 is mid-code MOV r1,r2 inside loop body -- degenerate weak entry
- Proposed name: `scan_zone_dimension_removal_group_substate_f`
- Confidence: high (body: alt-hand slot array + equip_eligible_alt + attribute gate + write_f; all 4 cards are Different Dimension removal/return spells; gP1AltHandSlotArray confirmed in ewram.inc at 0x0201cab0)
- ASCII plate (len=490): `Equip zone scan for Dimension Removal group (4 CIDs): Dimension Distortion (CID=0x16d8, pw=95194279), Dimension Fusion (DIMENSION_FUSION_CID=0x1712, pw=23557835), Return from DD (CID=0x17be, pw=27174286), D.D.M. (CID=0x191e, pw=82112775). Alt-hand zone via gP1AltHandSlotArray+0x1c; gates: field5_nonzero + equip_eligible_alt + get_zone_card_attribute_by_type; write_equip_zone_entry_by_substate(player_id, 0xf, slot_idx). Dispatch entries [165,171,197,267].`

### fn18: 0x0808aa38  size=0x07c (124 B)
- CID: 0x170c (Manju of the Ten Thousand Hands)
- Dispatch entry: [170]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1SlotSetCodeArray;
  gates: check_card_field5_is_nonzero (0x0804a9dc? -- actually: 0x0804a9dc = map_field8_to_card_type_category); get_card_extended_stat_field9 (0x080eee7c); cmp r0,#6 (d104); write substate_d
- BL targets: 0x0804a9dc (map_field8_to_card_type_category), 0x080eee7c (get_card_extended_stat_field9), 0x0808d88c
- Pool: 0x0808aaa8=gP1LifePoints, 0x0808aaac=PLAYER_BLOCK_STRIDE, 0x0808aab0=gP1SlotSetCodeArray
- CID status: 0x170c NEW (Manju of the Ten Thousand Hands, grep=0 hits)
- Substate: 0xd (MOVS r1,#0xd at 0x0808aa86 before write_equip)
- Note: cmp r0,#6 (2806): checks map_field8 result == 6 (Ritual type) -- Manju adds Ritual monsters/spells
- Proposed name: `scan_zone_manju_of_ten_thousand_hands_substate_d`
- Confidence: high (body: map_field8 result==6 (Ritual type) + field9 gate via gP1SlotSetCodeArray; Manju of the Ten Thousand Hands adds Ritual monster/spell from deck to hand; write_d = monster zone)
- ASCII plate (len=338): `Equip zone scan for Manju of the Ten Thousand Hands (CID=0x170c, pw=95492061). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: map_field8_to_card_type_category==6 (Ritual) + get_card_extended_stat_field9; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [170].`

### fn19: 0x0808aab4  size=0x090 (144 B)
- CID: 0x1714 (Salvage)
- Dispatch entry: [173]
- Body: push {r4..r7,lr} + extra push (r8); scan gP1LifePoints+gP1HandSlotArray;
  gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field3_raw (0x080eef44) cmp <=0x5dc (ATK<=1500) + check_card_stat_field7_equals (0x08030b70, arg=3 = Water attribute); write substate_e
- BL targets: 0x0804ad48, 0x080eef44, 0x08030b70, 0x0808d88c
- Pool: 0x0808ab34=gP1LifePoints, 0x0808ab38=PLAYER_BLOCK_STRIDE, 0x0808ab3c=gP1HandSlotArray, 0x0808ab40=CARD_FIELD3_THRESHOLD_1500(0x5dc)
- CID status: 0x1714 NEW (Salvage, grep=0 hits)
- Substate: 0xe (MOVS r1,#0xe at 0x0808ab10 before write_equip)
- Note: 0x0808ab2c is weak entry -- it is the POP+BX epilogue bytes (bcf0 bc01 0047) of fn19, not a function entry
- Note: MOVS r1,#3 at 0x0808ab04 = arg to check_stat_field7 (Water attribute); MOVS r1,#0xe = write_equip arg
- Proposed name: `scan_zone_salvage_substate_e`
- Confidence: high (body: field5 + ATK<=1500 + stat_field7==3 (WATER attr) + hand zone; Salvage returns Water monsters with ATK<=1500 from GY to hand; write_e = hand slot)
- ASCII plate (len=365): `Equip zone scan for Salvage (CID=0x1714, pw=96947648). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field3_raw<=CARD_FIELD3_THRESHOLD_1500(0x5dc, ATK<=1500) + check_card_stat_field7_equals(3) (Water attr); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [173].`

### fn20: 0x0808ab44  size=0x058 (88 B)
- CID: 0x1715 (Ultra Evolution Pill)
- Dispatch entry: [174]
- Body: push {r4,r5,lr}; scan gP1FieldArrayCBase field spell zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field6 (0x080eedf8) cmp r0,#0xa (=10 = DINOSAUR race check); eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x0804ad48, 0x080eedf8, 0x0803bba4, 0x0808d88c
- Pool: 0x0808ab98=gP1FieldArrayCBase, 0x0808ab94=PLAYER_BLOCK_STRIDE (via gP1FieldArrayCBase scan)
- Note: from pool scan: 0x0808ab94=PLAYER_BLOCK_STRIDE, 0x0808ab98=gP1FieldArrayCBase
- CID status: ULTRA_EVOLUTION_PILL_CID(0x1715) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808ab84 before write_equip)
- Proposed name: `scan_zone_ultra_evolution_pill_substate_b`
- Confidence: high (body: field5 + field6==0xa (Dinosaur race) + placement + field spell zone; Ultra Evolution Pill special-summons Dinosaurs)
- ASCII plate (len=326): `Equip zone scan for Ultra Evolution Pill (ULTRA_EVOLUTION_PILL_CID=0x1715, pw=22431243). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + get_card_extended_stat_field6==0xa (Dinosaur) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [174].`

### fn21: 0x0808ab9c  size=0x058 (88 B)
- CID: 0x1717 (Jade Insect Whistle)
- Dispatch entry: [175]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x10; get_card_extended_stat_field6 (0x080eedf8) gate (cmp r0,#0xa=10, d104); write substate_d
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x0808abec=gP1LifePoints, 0x0808abf0=PLAYER_BLOCK_STRIDE
- CID status: JADE_INSECT_WHISTLE_CID(0x1717) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808abd4 before write_equip)
- Proposed name: `scan_zone_jade_insect_whistle_substate_d`
- Confidence: high (body: field6==0xa (Insect race) gate + monster zone +0x10 + write_d; Jade Insect Whistle forces opponent to return Insects to deck)
- ASCII plate (len=273): `Equip zone scan for Jade Insect Whistle (JADE_INSECT_WHISTLE_CID=0x1717, pw=95214051). Monster zone at gP1LifePoints+0x10; gate: get_card_extended_stat_field6==0xa (Insect race); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [175].`

### fn22: 0x0808abf4  size=0x054 (84 B)
- CID(s): 0x1727 (Abyss Soldier), 0x1754 (Lady Ninja Yae)
- Dispatch entries: [176], [181]
- Body: push {r4..r7,lr}; scan gP1FieldArrayCBase field spell zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field7 (0x080eee24) + check_card_stat_field7_equals (0x08030b70, arg=1 = Light attribute); write substate_b
- BL targets: 0x0804ad48, 0x080eee24 (get_card_extended_stat_field7), 0x08030b70, 0x0808d88c
- Pool: 0x0808ac40=PLAYER_BLOCK_STRIDE, 0x0808ac44=gP1FieldArrayCBase
- CID status: ABYSS_SOLDIER_CID(0x1727) REUSE; 0x1754 NEW (Lady Ninja Yae, grep=0 hits)
- Substate: 0xb (MOVS r1,#0xb at 0x0808ac30 before write_equip)
- Note: MOVS r1,#1 before BL 0x08030b70 = arg to check_stat_field7 (Light attribute check); 0x080eee24 = get_card_extended_stat_field7 (naming-proposals.csv line 4222)
- Proposed name: `scan_zone_abyss_soldier_lady_ninja_group_substate_b`
- Confidence: high (body: field5 + stat_field7_raw getter + stat_field7==1 (Light attr) + field spell zone; Abyss Soldier is WATER and Lady Ninja Yae is WIND both need a Light-attr monster on field; write_b = field spell zone; dispatch entries [176,181])
- ASCII plate (len=362): `Equip zone scan for Abyss Soldier/Lady Ninja Yae group: Abyss Soldier (ABYSS_SOLDIER_CID=0x1727, pw=18318842), Lady Ninja Yae (CID=0x1754, pw=82005435). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + get_card_extended_stat_field7 + check_card_stat_field7_equals(1) (Light attr); write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entries [176,181].`

### fn23: 0x0808ac48  size=0x058 (88 B)
- CID: 0x1647 (Arsenal Summoner)
- Dispatch entry: [137]
- Body: push {r4..r7,lr}; scan gP1LifePoints at +0x10; check_card_is_guardian_type (0x0804af88) gate (cmp r0!=0, d004); write substate_d
- BL targets: 0x0804af88 (check_card_is_guardian_type), 0x0808d88c
- Pool: 0x0808ac98=gP1LifePoints, 0x0808ac9c=PLAYER_BLOCK_STRIDE
- CID status: 0x1647 NEW (Arsenal Summoner, grep=0 hits)
- Substate: 0xd (MOVS r1,#0xd at 0x0808ac80 before write_equip)
- Proposed name: `scan_zone_arsenal_summoner_substate_d`
- Confidence: high (body: is_guardian_type gate + monster zone +0x10 + write_d; Arsenal Summoner adds a Guardian to hand from deck)
- ASCII plate (len=273): `Equip zone scan for Arsenal Summoner (CID=0x1647, pw=85489096). Monster zone at gP1LifePoints+0x10; gate: check_card_is_guardian_type; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [137].`

### fn24: 0x0808aca0  size=0x0ec (236 B)
- CID(s): 0x164a (Guardian Elma), 0x16bc (Chopman the Desperate Outlaw), 0x1745 (The Kick Man)
- Dispatch entries: [138], [153], [178]
- Body: push {r4..r7,lr} + extra push (r8,r9,r10) + push extra (0xe0) + SUB sp,sp,#0x18 (local frame 6 words);
  BL memset (0x0810e9bc) to zero local stack struct;
  MOVS r1,#0 + MOVS r2,#0x18 = args to memset;
  init local struct fields: r0=1, r0=2, r1=0x3f, r1=0x16, r0=0x31 (struct initialization);
  scan gP1LifePoints + gP1HandSlotArray at +0x14; BL get_card_extended_stat_field9 (0x080eee7c);
  apply mask 0xffff803f; BL check_slot_card_eligible_by_card_id (0x0804f6c4);
  write substate_e
- BL targets: 0x0810e9bc (memset), 0x080eee7c, 0x0804f6c4 (check_slot_card_eligible_by_card_id), 0x0808d88c
- Pool: 0x0808ad78=gP1LifePoints, 0x0808ad7c=PLAYER_BLOCK_STRIDE, 0x0808ad80=gP1HandSlotArray, 0x0808ad84=0xffff803f(slot-field mask), 0x0808ad88=gP1HandCountBase(0x0201c4f4)
- CID status: GUARDIAN_ELMA_CID(0x164a) REUSE; 0x16bc NEW (Chopman the Desperate Outlaw, grep=0 hits); THE_KICK_MAN_CID(0x1745) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808ad4e before write_equip)
- Note: 0xffff803f mask strips bits 6..14 from a slot word; gP1HandCountBase referenced for count check
- Proposed name: `scan_zone_guardian_equip_group_substate_e`
- Confidence: high (body: memset local struct + field9 gate + slot_id_eligible check + hand zone; Guardian Elma/Chopman/Kick Man all require specific equip weapons on field; write_e = hand slot; dispatch entries [138,153,178])
- ASCII plate (len=482): `Equip zone scan for Guardian equip group: Guardian Elma (GUARDIAN_ELMA_CID=0x164a, pw=74367458), Chopman the Desperate Outlaw (CID=0x16bc, pw=40884383), The Kick Man (THE_KICK_MAN_CID=0x1745, pw=90407382). Hand zone via gP1LifePoints+gP1HandSlotArray; local struct init via memset; gates: get_card_extended_stat_field9 + check_slot_card_eligible_by_card_id (mask 0xffff803f); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entries [138,153,178].`

---

## REF_SLOTS (createDWordWithRef plan)

Per Seg-4a/4b/4c precedent: every pool DWord holding an EWRAM address gets
createDWordWithRef + RENAME to export as `.word gP1LifePoints` etc.

### gP1LifePoints = 0x0201c4e0 (ewram.inc) -- 22 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x0808a36c | fn01 | ptr_lp_8a36c |
| 0x0808a3b0 | fn02 | ptr_lp_8a3b0 |
| 0x0808a3e0 | fn03 | ptr_lp_8a3e0 |
| 0x0808a438 | fn04 | ptr_lp_8a438 |
| 0x0808a490 | fn05 | ptr_lp_8a490 |
| 0x0808a53c | fn07 loop1 | ptr_lp_8a53c |
| 0x0808a590 | fn07 loop2 | ptr_lp_8a590 |
| 0x0808a5e8 | fn08 | ptr_lp_8a5e8 |
| 0x0808a670 | fn09 | ptr_lp_8a670 |
| 0x0808a6fc | fn10 | ptr_lp_8a6fc |
| 0x0808a77c | fn11 | ptr_lp_8a77c |
| 0x0808a834 | fn12 | ptr_lp_8a834 |
| 0x0808a88c | fn13 | ptr_lp_8a88c |
| 0x0808a914 | fn14 | ptr_lp_8a914 |
| 0x0808a970 | fn15 | ptr_lp_8a970 |
| 0x0808a9ac | fn16 | ptr_lp_8a9ac |
| 0x0808aa2c | fn17 | ptr_lp_8aa2c |
| 0x0808aaa8 | fn18 | ptr_lp_8aaa8 |
| 0x0808ab34 | fn19 | ptr_lp_8ab34 |
| 0x0808abec | fn21 | ptr_lp_8abec |
| 0x0808ac98 | fn23 | ptr_lp_8ac98 |
| 0x0808ad78 | fn24 | ptr_lp_8ad78 |

REF count gP1LifePoints: **22**

### gP1FieldArrayCBase = 0x0201c600 (ewram.inc) -- 3 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x0808a4ec | fn06 | ptr_fac_8a4ec |
| 0x0808ab98 | fn20 | ptr_fac_8ab98 |
| 0x0808ac44 | fn22 | ptr_fac_8ac44 |

REF count gP1FieldArrayCBase: **3**

### gP1HandSlotArray = 0x0201c8f8 (ewram.inc) -- 5 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x0808a704 | fn10 | ptr_hsa_8a704 |
| 0x0808a784 | fn11 | ptr_hsa_8a784 |
| 0x0808a91c | fn14 | ptr_hsa_8a91c |
| 0x0808ab3c | fn19 | ptr_hsa_8ab3c |
| 0x0808ad80 | fn24 | ptr_hsa_8ad80 |

REF count gP1HandSlotArray: **5**

### gP1SlotSetCodeArray = 0x0201c740 (ewram.inc) -- 2 slots

| slot addr | fn | label |
|-----------|----|----|
| 0x0808a678 | fn09 | ptr_sca_8a678 |
| 0x0808aab0 | fn18 | ptr_sca_8aab0 |

REF count gP1SlotSetCodeArray: **2**

### gP1AltHandSlotArray = 0x0201cab0 (ewram.inc) -- 1 slot

| slot addr | fn | label |
|-----------|----|----|
| 0x0808aa34 | fn17 | ptr_aha_8aa34 |

REF count gP1AltHandSlotArray: **1**

### gP1HandCountBase = 0x0201c4f4 (ewram.inc) -- 1 slot

| slot addr | fn | label |
|-----------|----|----|
| 0x0808ad88 | fn24 | ptr_hcb_8ad88 |

REF count gP1HandCountBase: **1**

### Total REF count: 22+3+5+2+1+1 = **34**

---

## EQ_SLOTS (CID pool equates)

### NEW CIDs to add to card_info.inc (10 entries, individual grep = 0 hits each):

```
.equ SENRI_EYE_CID,                    0x00001628  @ Senri Eye (pw=60391791; card-stats.s card_1291 slot=0x1628); grep 0x1628=0 hits
.equ ARSENAL_ROBBER_CID,               0x0000166b  @ Arsenal Robber (pw=55348096; card-stats.s card_1345 slot=0x166B); grep 0x166b=0 hits
.equ CHAOSRIDER_GUSTAPH_CID,           0x000016c4  @ Chaosrider Gustaph (pw=47829960; card-stats.s card_1414 slot=0x16C4); grep 0x16c4=0 hits
.equ DIMENSION_DISTORTION_CID,         0x000016d8  @ Dimension Distortion (pw=95194279; card-stats.s card_1433 slot=0x16D8); grep 0x16d8=0 hits
.equ RETURN_FROM_DD_CID,               0x000017be  @ Return from the Different Dimension (pw=27174286; card-stats.s card_1615 slot=0x17BE); grep 0x17be=0 hits
.equ DDM_DIFF_DIM_MASTER_CID,          0x0000191e  @ D.D.M. - Different Dimension Master (pw=82112775; card-stats.s card_1915 slot=0x191E); grep 0x191e=0 hits
.equ MANJU_TEN_THOUSAND_HANDS_CID,     0x0000170c  @ Manju of the Ten Thousand Hands (pw=95492061; card-stats.s card_1476 slot=0x170C); grep 0x170c=0 hits
.equ SALVAGE_CID,                      0x00001714  @ Salvage (pw=96947648; card-stats.s card_1484 slot=0x1714); grep 0x1714=0 hits
.equ LADY_NINJA_YAE_CID,               0x00001754  @ Lady Ninja Yae (pw=82005435; card-stats.s card_1535 slot=0x1754); grep 0x1754=0 hits
.equ ARSENAL_SUMMONER_CID,             0x00001647  @ Arsenal Summoner (pw=85489096; card-stats.s card_1312 slot=0x1647); grep 0x1647=0 hits
```

Missing from NEW list: 0x16bc (Chopman the Desperate Outlaw) used in fn24:
```
.equ CHOPMAN_THE_DESPERATE_OUTLAW_CID, 0x000016bc  @ Chopman the Desperate Outlaw (pw=40884383; card-stats.s card_1407 slot=0x16BC); grep 0x16bc=0 hits
```

Total NEW CIDs: **11**

### REUSE CIDs (already in card_info.inc, DO NOT add):
EMBLEM_OF_DRAGON_DESTROYER_CID(0x1629), ICID_RESERVED_A(0x162c), ICID_RESERVED_B(0x184c),
DARK_SCORPION_CHICK_CID(0x1656), FAIRY_OF_THE_SPRING_CID(0x1664), MAGICAL_DIMENSION_CID(0x1678),
DARK_SCORPION_MEANAE_CID(0x1686), IRON_BLACKSMITH_KOTETSU_CID(0x1689), PANDEMONIUM_CID(0x169f),
EQUIP_LOCK_A_CID(0x16a4), RAY_OF_HOPE_CID(0x16a8), WITCH_DOCTOR_OF_CHAOS_CID(0x16c2),
CHAOS_SORCERER_CID(0x16c9), BLACK_LUSTER_SOLDIER_ENVOY_CID(0x16cb), CHAOS_EMPEROR_DRAGON_CID(0x16e4),
RECYCLE_CID(0x16d5), PRIMAL_SEED_CID(0x16d6), DIMENSION_FUSION_CID(0x1712),
ULTRA_EVOLUTION_PILL_CID(0x1715), JADE_INSECT_WHISTLE_CID(0x1717),
ABYSS_SOLDIER_CID(0x1727), GUARDIAN_ELMA_CID(0x164a), THE_KICK_MAN_CID(0x1745)

### Partner/comparison CID equates in pool (fn01 only):
- 0x0808a364 = EMBLEM_OF_DRAGON_DESTROYER_CID(0x1629) -- dispatched CID (REUSE)
- 0x0808a368 = BUSTER_BLADER_CID(0x1377) -- partner comparison (REUSE, in card_info.inc)
- 0x0808a374 = NECROVALLEY_CID(0x159d) -- partner comparison (REUSE, in card_info.inc)

### Scalar pool equates (existing constants, REUSE):
- 0x00000868 = PLAYER_BLOCK_STRIDE (ewram.inc) -- 25 slots across Seg-4d
- 0x000005dc = CARD_FIELD3_THRESHOLD_1500 (card_info.inc) -- 1 slot (fn19 pool 0x0808ab40)

---

## Literal Pool DWord List (createDWord required, all addresses in [0x0808a2ac, 0x0808ad8c))

**fn01** (0x0808a2ac): 0x0808a364, 0x0808a368, 0x0808a36c, 0x0808a370, 0x0808a374
**fn02** (0x0808a378): 0x0808a3b0, 0x0808a3b4
**fn03** (0x0808a3b8): 0x0808a3e0, 0x0808a3e4
**fn04** (0x0808a3e8): 0x0808a438, 0x0808a43c
**fn05** (0x0808a440): 0x0808a490, 0x0808a494
**fn06** (0x0808a498): 0x0808a4e8, 0x0808a4ec
**fn07** (0x0808a4f0): 0x0808a53c, 0x0808a540, 0x0808a590, 0x0808a594
**fn08** (0x0808a598): 0x0808a5e8, 0x0808a5ec
**fn09** (0x0808a5f0): 0x0808a670, 0x0808a674, 0x0808a678
**fn10** (0x0808a67c): 0x0808a6fc, 0x0808a700, 0x0808a704
**fn11** (0x0808a708): 0x0808a77c, 0x0808a780, 0x0808a784
**fn12** (0x0808a788): 0x0808a834, 0x0808a838
**fn13** (0x0808a83c): 0x0808a88c, 0x0808a890
**fn14** (0x0808a894): 0x0808a914, 0x0808a918, 0x0808a91c
**fn15** (0x0808a920): 0x0808a970, 0x0808a974
**fn16** (0x0808a978): 0x0808a9ac, 0x0808a9b0
**fn17** (0x0808a9b4): 0x0808aa2c, 0x0808aa30, 0x0808aa34
**fn18** (0x0808aa38): 0x0808aaa8, 0x0808aaac, 0x0808aab0
**fn19** (0x0808aab4): 0x0808ab34, 0x0808ab38, 0x0808ab3c, 0x0808ab40
**fn20** (0x0808ab44): 0x0808ab94, 0x0808ab98
**fn21** (0x0808ab9c): 0x0808abec, 0x0808abf0
**fn22** (0x0808abf4): 0x0808ac40, 0x0808ac44
**fn23** (0x0808ac48): 0x0808ac98, 0x0808ac9c
**fn24** (0x0808aca0): 0x0808ad78, 0x0808ad7c, 0x0808ad80, 0x0808ad84, 0x0808ad88

Note: 0x0808ab94 holds PLAYER_BLOCK_STRIDE (0x0000_0868); 0x0808ab98 holds gP1FieldArrayCBase.
Note: fn22 pool: 0x0808ac40 = PLAYER_BLOCK_STRIDE (4B-aligned), 0x0808ac44 = gP1FieldArrayCBase (4B-aligned).

---

## Disasm Plan (R4)

All 24 real functions are THUMB code. No ROM_INCBIN or .byte blocks remain in this segment -- all bytes are part of the function bodies and literal pools.

Per-function disassembly (24 functions + degenerate exclusions):

| fn | start | end | size | degenerate exclusion |
|----|-------|-----|------|---------------------|
| fn01 | 0x0808a2ac | 0x0808a378 | 0xcc | none |
| fn02 | 0x0808a378 | 0x0808a3b8 | 0x40 | none |
| fn03 | 0x0808a3b8 | 0x0808a3e8 | 0x30 | none |
| fn04 | 0x0808a3e8 | 0x0808a440 | 0x58 | none |
| fn05 | 0x0808a440 | 0x0808a498 | 0x58 | exclude 0x0808a44c, 0x0808a450 from entry list |
| fn06 | 0x0808a498 | 0x0808a4f0 | 0x58 | none |
| fn07 | 0x0808a4f0 | 0x0808a598 | 0xa8 | none |
| fn08 | 0x0808a598 | 0x0808a5f0 | 0x58 | none |
| fn09 | 0x0808a5f0 | 0x0808a67c | 0x8c | none |
| fn10 | 0x0808a67c | 0x0808a708 | 0x8c | none |
| fn11 | 0x0808a708 | 0x0808a788 | 0x80 | none |
| fn12 | 0x0808a788 | 0x0808a83c | 0xb4 | none |
| fn13 | 0x0808a83c | 0x0808a894 | 0x58 | none |
| fn14 | 0x0808a894 | 0x0808a920 | 0x8c | none |
| fn15 | 0x0808a920 | 0x0808a978 | 0x58 | none; 0x0808a974 is pool data not fn entry |
| fn16 | 0x0808a978 | 0x0808a9b4 | 0x3c | exclude 0x0808a996 from entry list |
| fn17 | 0x0808a9b4 | 0x0808aa38 | 0x84 | none; 0x0808a9c2 is mid-code not fn entry |
| fn18 | 0x0808aa38 | 0x0808aab4 | 0x7c | none |
| fn19 | 0x0808aab4 | 0x0808ab44 | 0x90 | none; 0x0808ab2c is epilogue bytes not fn entry |
| fn20 | 0x0808ab44 | 0x0808ab9c | 0x58 | none |
| fn21 | 0x0808ab9c | 0x0808abf4 | 0x58 | none |
| fn22 | 0x0808abf4 | 0x0808ac48 | 0x54 | none |
| fn23 | 0x0808ac48 | 0x0808aca0 | 0x58 | none |
| fn24 | 0x0808aca0 | 0x0808ad8c | 0xec | none |

Size sum: 0xcc+0x40+0x30+0x58+0x58+0x58+0xa8+0x58+0x8c+0x8c+0x80+0xb4+0x58+0x8c+0x58+0x3c+0x84+0x7c+0x90+0x58+0x58+0x54+0x58+0xec = 0xAE0 = 2784 B. Confirmed matches segment size.

---

## carve 计划 (R7)

No ROM_INCBIN data blocks requiring carve in this segment. All bytes are THUMB code + literal pools belonging to the 24 real functions. No data tables, incbin regions, or pointer tables exist in this range.

---

## §5.1 登记 (Rule 3) -- 0 引用块

No ROM_INCBIN or .byte blocks in Seg-4d. All code; no orphan data regions.

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

- `write_equip_zone_entry_by_substate` (0x0808d88c): referenced from all 24 fns; function name established in Seg-4a/4b/4c; high confidence
- `check_card_pair_allowed` (0x0804ab4c): doc/dev/naming-proposals.csv:line check_card_pair_allowed; high confidence
- `count_field_copies_of_card` (0x0803279c): doc/dev/naming-proposals.csv; high confidence
- `check_card_is_archfiend_type` (0x0804aea0): doc/dev/naming-proposals.csv; high confidence
- `check_card_is_dark_scorpion_type` (0x0804b004): doc/dev/naming-proposals.csv; high confidence
- `check_card_is_guardian_type` (0x0804af88): doc/dev/naming-proposals.csv; high confidence
- `check_slot_card_eligible_by_card_id` (0x0804f6c4): doc/dev/naming-proposals.csv; high confidence
- `map_field8_to_card_type_category` (0x0804a9dc): doc/dev/naming-proposals.csv; high confidence
- `get_zone_card_attribute_by_type` (0x0803b618): doc/dev/naming-proposals.csv; high confidence
- `check_zone_slot_equip_eligible_alt` (0x08037568): doc/dev/naming-proposals.csv; high confidence
- `gP1AltHandSlotArray` (0x0201cab0): constants/ewram.inc REUSE; high confidence
- `gP1HandCountBase` (0x0201c4f4): constants/ewram.inc REUSE; high confidence
- `memset` (0x0810e9bc): doc/dev/naming-proposals.csv; high confidence
- `get_card_extended_stat_field7` (0x080eee24): doc/dev/naming-proposals.csv line 4222; high confidence

---

## 求助 (低置信度语义)

fn24 mask 0xffff803f: strips bits 6..14 from slot word. Semantics = slot attribute/flag mask. No existing constant found in constants/. Label as raw EQ_SLOT with value 0xffff803f; do not create a named constant without finding a consumer doc string. Confidence: med (structural evidence from instruction sequence only).
