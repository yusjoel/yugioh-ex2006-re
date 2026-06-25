# Refine Proposal: F11-Seg-4a  [0x08087d58..0x08088904)

## Segment Survey

- ROM range: `[0x08087d58, 0x08088904)` = 0xBAC bytes (2988 B)
- Source: one-liner `ROM_INCBIN 0x87d58, 0x5a9c` at asm/11 line 6089 (Seg-4 giant block)
- Seg-4a is the FIRST sub-segment; boundary at 0x08088904 = next strong entry (Seg-4b start)
- Functions: 21 real functions (27 apparent strong entries - 6 degenerate = 21 real functions)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools

### Function type: equip zone scan callbacks

All 21 real functions are **equip zone scan callbacks** dispatched from a 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

Naming convention matches existing file-11 scan functions:
`scan_zone_<card_or_category>_substate_<x>` where substate x in {b, d, e}.

Substate semantics (from existing write_equip_zone_entry_by_substate plate):
- 0xb = field-spell zone (type B equip placement)
- 0xd = monster zone (zone D entries)
- 0xe = hand slot zone (type E)

---

## Weak Entry Analysis (4 candidates, all EXCLUDED)

The 4 "weak" candidate addresses have their only word-aligned THUMB+1 refs in
**non-word-aligned positions** (offset % 4 == 2) inside compressed asset data
(ROM regions 0x078..0x0ac), not in any code or structured table region.
All 4 are degenerate -- ref is a coincidental byte pattern in LZ-compressed data.

| addr | ref location | ref%4 | ROM region | disposition |
|------|-------------|-------|------------|-------------|
| 0x08088442 | 0x085c6b72 | 2 | compressed data | EXCLUDE: coincidental LZ match |
| 0x08088554 | 0x0879a5d2 | 2 | compressed data | EXCLUDE: coincidental LZ match |
| 0x080885e0 | 0x08a2dc66 | 2 | compressed data | EXCLUDE: coincidental LZ match |
| 0x080887e8 | 0x08ac7f1a | 2 | compressed data | EXCLUDE: coincidental LZ match |

---

## Degenerate Strong Entries (6 of 27 excluded from createFunction)

Six addresses in the "strong entry" list are NOT real function starts:

| addr | reason | evidence |
|------|--------|---------|
| 0x08088354 | Epilogue+pool of fn12 (0x08088304). ROM bytes `01 bc 00 47` = halfwords 0xbc01/0x4700 = pop{r0,pc} + bx r0 (epilogue sequence). Pool words follow: 0x00000868, 0x0201c600. | ref at 0x08f38b54 in compressed data (ROM off 0xf38b54, not code); fn12 spans 0x08088304..0x08088360 |
| 0x08088394 | 2nd halfword of BL instruction at 0x08088392 inside fn14. ROM bytes `c2 f7 d9 fc` = BL pair 0xf7c2/0xfcd9 spanning 0x08088392..0x08088395. BL target = 0x0804ad48 (check_card_field5_is_nonzero, verified by offset decode). | ref at 0x08a6f1e0 in compressed data |
| 0x0808855a | Mid-loop body of fn15 (0x080884f8). ROM halfword 0x005b = lsls r3,r3,#1 -- not a prologue. | fn15 spans 0x080884f8..0x080885a8; ref at 0x086ba9f4 in compressed data |
| 0x0808866c | Mid-loop body of fn18 (0x0808864c). ROM halfword 0x5218 = adds r2,r2,r1 -- not a prologue. | fn18 spans 0x0808864c..0x080886f8; ref at 0x08eb8328 in compressed data |
| 0x080887ec | Post-BL continuation of fn20 (0x080887b0). `2816` = cmp r0,#0x16 immediately after BL pair at 0x080887e8. | fn20 spans 0x080887b0..0x0808882c; ref at 0x08af13f8 in compressed data |
| 0x08088080 | Mid-loop body of fn06 (0x08088058). ROM halfword 0x00c0 = lsls r0,r0,#3 -- not a prologue. | fn06 spans 0x08088058..0x080880c0; ref at 0x0878ab58 in compressed data |

---

## Dispatch Table Structure

Table at 0x09e5a128: 2-word entries `{u32 CID, u32 fn_ptr+1}`, 305 entries.
Multiple CIDs can share the same function pointer (same scan logic for a card category).

All 21 real Seg-4a functions appear in this table. No fn_eligible separate slots exist
for these entries (the table does NOT use the 6-word format used in other dispatch tables).

---

## Function Naming Table (21 real functions)

### fn01: 0x08087d58
- **CID(s)**: 0x12f4 (unallocated -- not in card-stats.s; between cid_12f7 gap and 0x12f3=Ultimate Offering)
- **Dispatch table entry**: [21] CID=0x12f4, fn=0x08087d58+1
- **Body analysis**: push {r4,r5,r6,lr}; scans gP1LifePoints[player*PLAYER_BLOCK_STRIDE+0x10] monster slots; calls write_equip_zone_entry_by_substate with r1=#0xd (substate 0xd). Single BL to 0x0808d88c.
- **Size**: 68 bytes (0x44)
- **Pool DWords**: 0x08087d94 = 0x0201c4e0 (gP1LifePoints), 0x08087d98 = 0x00000868 (PLAYER_BLOCK_STRIDE)
- **CID_REUSE/NEW**: NEW (0x12f4 not in card_info.inc -- value grep returns 0 hits)
- **Proposed name**: `scan_zone_cid_12f4_substate_d`
- **Confidence**: high (body clear: loop + write substate_d; CID unallocated)
- **ASCII plate**: `Equip zone scan callback for unallocated CID 0x12f4. r0=player_id. Scans monster zone slots in gP1LifePoints[player*STRIDE+0x10]; calls write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx) for each matching slot. Dispatched from equip zone write table 0x09e5a128 entry [21].`
- **CSV row**: `0x08087d58,scan_zone_cid_12f4_substate_d,,,`

### fn02: 0x08087d9c
- **CID(s)**: 0x12f9 = Soul Release (pw=05758500, card_0680)
- **Dispatch table entry**: [22] CID=0x12f9, fn=0x08087d9c+1
- **Body analysis**: push {r4,r5,r6,r7,lr}; 2 calls to write_equip_zone_entry_by_substate with r1=#0xe. Loads from gP1LifePoints alt zone base. 108 bytes.
- **Size**: 108 bytes
- **Pool DWords**: 0x08087e00 = 0x0201c4e0, 0x08087e04 = 0x00000868
- **CID_REUSE/NEW**: NEW (0x12f9 not in card_info.inc -- value grep returns 0 hits; neighbor 0x12f7=cid_12f7 exists)
- **Proposed name**: `scan_zone_soul_release_substate_e`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Soul Release (CID=0x12f9, pw=05758500). r0=player_id. Scans hand slot zone; calls write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx) twice on matching entries. Dispatched from equip zone write table 0x09e5a128 entry [22].`
- **CSV row**: `0x08087d9c,scan_zone_soul_release_substate_e,,,`

### fn03: 0x08087e08
- **CID(s)**: 0x1315 = Last Will (pw=85602018, card_0703)
- **Dispatch table entry**: [25] CID=0x1315, fn=0x08087e08+1
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,lr} (b5f0 464f 4646 b4c0); calls check_card_field5_is_nonzero (0x0804ad48), get_card_extended_stat_field9 (0x080eef44), eval_equip_placement_full_check (0x0803bba4), find_effect_node_in_zone (0x0802fd60), write_equip_zone_entry_by_substate (substate=0xd). 180 bytes.
- **Size**: 180 bytes
- **Pool DWords**: 0x08087ea8 = 0x0201c4e0, 0x08087eac = 0x00000868, 0x08087eb0 = 0x0201c740, 0x08087eb4 = 0x000005dc (=1500), 0x08087eb8 = 0x000012a1 (zone_query_hand_tag)
- **CID_REUSE/NEW**: NEW (0x1315 not in card_info.inc -- value grep returns 0 hits)
- **Proposed name**: `scan_zone_last_will_substate_d`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Last Will (CID=0x1315, pw=85602018). r0=player_id. Multi-check: field5, field9>=3, eval_equip_placement_full_check pass, find_effect_node_in_zone condition; then write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table 0x09e5a128 entry [25].`
- **CSV row**: `0x08087e08,scan_zone_last_will_substate_d,,,`

### fn04: 0x08087ebc
- **CID(s)**: 0x132f = Painful Choice (pw=74191942, card_0726)
- **Dispatch table entry**: [26] CID=0x132f, fn=0x08087ebc+1
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,r10,lr}; 2 paths both writing substate 0xd. Uses 0xb as arg to find_effect_node_in_zone check only (not as write substate). 260 bytes.
- **Size**: 260 bytes
- **Pool DWords**: 0x08087f3c = 0x0201c4f0, 0x08087f40 = 0x00000868, 0x08087f44 = 0x0201c740, 0x08087f48 = 0xfffffdb0, 0x08087f4c = 0x00001b38, 0x08087fb4 = 0x0201c4e0, 0x08087fb8 = 0x00000868, 0x08087fbc = 0x000012a1
- **CID_REUSE/NEW**: NEW (0x132f not in card_info.inc -- value grep returns 0 hits)
- **Proposed name**: `scan_zone_painful_choice_substate_d`
- **Confidence**: high (substate 0xd confirmed at both BL write sites; #0xb is find_effect_node arg only)
- **ASCII plate**: `Equip zone scan callback for Painful Choice (CID=0x132f, pw=74191942). r0=player_id. Two-path scan of monster zone; both paths call write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Inner check uses find_effect_node_in_zone. Dispatched from equip zone write table entry [26].`
- **CSV row**: `0x08087ebc,scan_zone_painful_choice_substate_d,,,`

### fn05: 0x08087fc0
- **CID(s)**: 0x1362 = Magical Hats (pw=81210420, card_0769)
- **Dispatch table entry**: [40] CID=0x1362, fn=0x08087fc0+1
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls check_card_field5_is_nonzero, write_equip_zone_entry_by_substate(substate=0xd). Pools include 0x1497 and 0x17ae (two CID-range compare values). 152 bytes.
- **Size**: 152 bytes
- **Pool DWords**: 0x08088044 = 0x0201c4e0, 0x08088048 = 0x00000868, 0x0808804c = 0x0201c740, 0x08088050 = 0x00001497, 0x08088054 = 0x000017ae
- **CID_REUSE/NEW**: REUSE MAGICAL_HATS_CID=0x00001362 (card_info.inc line 1166)
- **Proposed name**: `scan_zone_magical_hats_substate_d`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Magical Hats (MAGICAL_HATS_CID=0x1362, pw=81210420). r0=player_id. Scans monster zone; check_card_field5_is_nonzero filter + CID range [0x1497..0x17ae] check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [40].`
- **CSV row**: `0x08087fc0,scan_zone_magical_hats_substate_d,,,`

### fn06: 0x08088058
- **CID(s)**: 0x1379 = Graverobber (pw=61705417, card_0789)
- **Dispatch table entry**: [44] CID=0x1379, fn=0x08088058+1
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls get_card_extended_stat_field6 (0x080eedf8), write_equip_zone_entry_by_substate(substate=0xe). Spans 0x08088058..0x080880c0 (includes degenerate 0x08088080 mid-loop). 104 bytes total.
- **Size**: 104 bytes (0x08088058..0x080880c0)
- **Pool DWords**: 0x080880b8 = 0x0201c4e0, 0x080880bc = 0x00000868
- **CID_REUSE/NEW**: REUSE GRAVEROBBER_CID=0x00001379 (card_info.inc line 453)
- **Proposed name**: `scan_zone_graverobber_substate_e`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Graverobber (GRAVEROBBER_CID=0x1379, pw=61705417). r0=player_id. Scans zone entries; get_card_extended_stat_field6 filter; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from equip zone write table entry [44]. Note: addr 0x08088080 is mid-loop code, not a separate function (degenerate strong entry, excluded from createFunction).`
- **CSV row**: `0x08088058,scan_zone_graverobber_substate_e,,,`

### fn07: 0x080880c0
- **CID(s)**: 0x1333 (Giant Rat), 0x1335 (UFO Turtle), 0x133c (Shining Angel), 0x133e (Mother Grizzly), 0x133f (Flying Kamakiri #1), 0x1342 (Mystic Tomato)
- **Dispatch table entries**: [27], [29], [33], [34], [35], [37]
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,r10,lr}; calls check_card_field5_is_nonzero, get_card_extended_stat_field8 (0x080eee24), get_card_extended_stat_field9 (0x080eef44), eval_equip_placement_full_check, find_effect_node_in_zone, write_equip_zone_entry_by_substate(substate=0xd). 216 bytes.
- **Size**: 216 bytes
- **Pool DWords**: 0x08088180 = 0x0201c4e0, 0x08088184 = 0x00000868, 0x08088188 = 0x0201c740, 0x0808818c = 0x000005dc (1500), 0x08088190 = 0x000012a1, 0x08088194 = 0x0201c4f0
- **CID_REUSE/NEW**: REUSE GIANT_RAT_CID=0x1333 (card_info.inc line 499), SHINING_ANGEL_CID=0x133c (line 503), NIMBLE_MOMONGA_CID is 0x133a (different), MYSTIC_TOMATO_CID=0x1342 (line 504). NEW needed: UFO_TURTLE_CID=0x1335 (value grep 0x00001335 = 0 hits), MOTHER_GRIZZLY_CID=0x133e, FLYING_KAMAKIRI_1_CID=0x133f (value grep 0x133e, 0x133f = 0 hits each)
- **Proposed name**: `scan_zone_summon_from_deck_group_a_substate_d`
- **Confidence**: high (body: multi-check gate + substate_d write; card group: all flip-destroy summon-from-deck type A)
- **ASCII plate**: `Equip zone scan callback for summon-from-deck group A: Giant Rat(0x1333), UFO Turtle(0x1335), Shining Angel(0x133c), Mother Grizzly(0x133e), Flying Kamakiri#1(0x133f), Mystic Tomato(0x1342). r0=player_id. Gate: field5+field8+field9+eval_placement+find_node; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from write table entries [27,29,33,34,35,37].`
- **CSV row**: `0x080880c0,scan_zone_summon_from_deck_group_a_substate_d,,,`

### fn08: 0x08088198
- **CID(s)**: 0x1334 = Senju of the Thousand Hands (pw=23401839, card_0731)
- **Dispatch table entry**: [28] CID=0x1334, fn=0x08088198+1
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls check_card_field5_is_nonzero (0x0804ad48), check_card_field8_is_normal (0x0804ad70), write_equip_zone_entry_by_substate(substate=0xd). 124 bytes.
- **Size**: 124 bytes
- **Pool DWords**: 0x08088208 = 0x0201c4e0, 0x0808820c = 0x00000868, 0x08088210 = 0x0201c740
- **CID_REUSE/NEW**: NEW (0x1334 not in card_info.inc -- value grep returns 0 hits)
- **Proposed name**: `scan_zone_senju_substate_d`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Senju of the Thousand Hands (CID=0x1334, pw=23401839). r0=player_id. Gate: check_card_field5_is_nonzero + check_card_field8_is_normal; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [28].`
- **CSV row**: `0x08088198,scan_zone_senju_substate_d,,,`

### fn09: 0x08088214
- **CID(s)**: 0x1339 (Giant Germ), 0x133a (Nimble Momonga), 0x136a (Bubonic Vermin), 0x14dd (Troop Dragon), 0x15b6 (King's Knight), 0x1867 (Hyena), 0x194f (Hydrogeddon), 0x19a7 (Hero Kid)
- **Dispatch table entries**: [30], [31], [43], [82], [115], [236], [277], [291]
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; single call to write_equip_zone_entry_by_substate(substate=0xd). Pools include 0x15b6 (King's Knight) and 0x15b7 for special King's Knight pair check. 112 bytes.
- **Size**: 112 bytes
- **Pool DWords**: 0x08088274 = 0x000015b6, 0x08088278 = 0x000015b7, 0x0808827c = 0x0201c4e0, 0x08088280 = 0x00000868
- **CID_REUSE/NEW**: REUSE GIANT_GERM_CID=0x1339 (line 501), NIMBLE_MOMONGA_CID=0x133a (line 502), HERO_KID_CID=0x19a7 (line 1268), BUBONIC_VERMIN_CID=0x136a (line 726), HYDROGEDDON_CID=0x194f (line 943). NEW needed: TROOP_DRAGON_CID=0x14dd, KINGS_KNIGHT_CID=0x15b6, HYENA_CID=0x1867 (value grep 0 hits each)
- **Proposed name**: `scan_zone_summon_from_deck_group_b_substate_d`
- **Confidence**: high (body: single write substate_d; card group: all summon-from-deck triggers including King's Knight pair check)
- **ASCII plate**: `Equip zone scan callback for summon-from-deck group B: Giant Germ(0x1339), Nimble Momonga(0x133a), Bubonic Vermin(0x136a), Troop Dragon(0x14dd), King's Knight(0x15b6), Hyena(0x1867), Hydrogeddon(0x194f), Hero Kid(0x19a7). Special King's Knight(0x15b6)/0x15b7 pair check in pool. Dispatched from write table entries [30,31,43,82,115,236,277,291].`
- **CSV row**: `0x08088214,scan_zone_summon_from_deck_group_b_substate_d,,,`

### fn10: 0x08088284
- **CID(s)**: 0x1341 = Sonic Bird (pw=57617178, card_0742)
- **Dispatch table entry**: [36] CID=0x1341, fn=0x08088284+1
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls get_card_extended_stat_field6 (0x080eedf8), get_card_extended_stat_field9 (0x080eee7c?), write_equip_zone_entry_by_substate(substate=0xd). 128 bytes.
- **Size**: 128 bytes
- **Pool DWords**: 0x080882f8 = 0x0201c4e0, 0x080882fc = 0x00000868, 0x08088300 = 0x0201c740
- **CID_REUSE/NEW**: NEW (0x1341 not in card_info.inc -- 0 hits; note SONIC_BIRD_CID name unused)
- **Proposed name**: `scan_zone_sonic_bird_substate_d`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Sonic Bird (CID=0x1341, pw=57617178). r0=player_id. Gate: get_card_extended_stat_field6 + field9 check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [36].`
- **CSV row**: `0x08088284,scan_zone_sonic_bird_substate_d,,,`

### fn11: 0x08088304
- **CID(s)**: 0x137c = Dust Tornado (pw=60082869, card_0792)
- **Dispatch table entry**: [45] CID=0x137c, fn=0x08088304+1
- **Body analysis**: push {r4,r5,r6,lr}; calls check_card_field5_is_nonzero, check_field_spell_b_placeable (0x080309fc), count_zone_pair_hits (0x0803123c?), eval_equip_placement_full_check (0x08033bf4?), write_equip_zone_entry_by_substate(substate=0xb). Note: 0x08088354 is this function's epilogue (bc01 4700) + pool -- degenerate entry excluded from createFunction. Full span 0x08088304..0x08088360. 92 bytes.
- **Size**: 92 bytes (0x08088304..0x08088360, inclusive of epilogue+pool at 0x08088354)
- **Pool DWords**: 0x08088358 = 0x00000868, 0x0808835c = 0x0201c600
- **CID_REUSE/NEW**: REUSE DUST_TORNADO_CID=0x0000137c (card_info.inc line 1579)
- **Proposed name**: `scan_zone_dust_tornado_substate_b`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Dust Tornado (DUST_TORNADO_CID=0x137c, pw=60082869). r0=player_id. Gate: check_card_field5_is_nonzero; additional field-spell checks; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Addr 0x08088354 is epilogue+pool of this function (degenerate strong entry, excluded from createFunction). Dispatched from write table entry [45].`
- **CSV row**: `0x08088304,scan_zone_dust_tornado_substate_b,,,`

### fn12: 0x08088360
- **CID(s)**: 0x1365 (The Shallow Grave), 0x1366 (Premature Burial), 0x137d (Call of the Haunted), 0x1488 (Gilasaurus), 0x1820 (The Creator), 0x190a (Dark Ruler Vandalgyon)
- **Dispatch table entries**: [41], [42], [46], [71], [225], [264]
- **Body analysis**: push {r4,r5,r6,r7,lr}; calls check_card_field5_is_nonzero (0x0804ad48), check_zone_slot_equip_eligible (0x08037434), write_equip_zone_entry_by_substate(substate=0xe). Full span 0x08088360..0x080883d4 (includes degenerate 0x08088394 at addr BL+2). 116 bytes.
- **Size**: 116 bytes (0x08088360..0x080883d4)
- **Pool DWords**: 0x080883c8 = 0x0201c4e0, 0x080883cc = 0x00000868, 0x080883d0 = 0x0201c8f8 (gP1HandSlotArray)
- **CID_REUSE/NEW**: REUSE DARK_RULER_VANDALGYON_CID=0x190a (card_info.inc line 837), CALL_OF_THE_HAUNTED_CID=0x137d (line 568), PREMATURE_BURIAL_CID=0x1366 (line 569), GILASAURUS_CID=0x1488 (line 732). NEW: THE_SHALLOW_GRAVE_CID=0x1365, THE_CREATOR_CID=0x1820 (value grep 0 hits each)
- **Proposed name**: `scan_zone_graveyard_revival_group_substate_e`
- **Confidence**: high (body: field5 + equip_eligible check + substate_e write; group: all graveyard revival trap/effect cards)
- **ASCII plate**: `Equip zone scan callback for graveyard revival group: Shallow Grave(0x1365), Premature Burial(0x1366), Call of Haunted(0x137d), Gilasaurus(0x1488), The Creator(0x1820), Dark Ruler Vandalgyon(0x190a). Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x08088394 is mid-BL degenerate. Dispatched from write table entries [41,42,46,71,225,264].`
- **CSV row**: `0x08088360,scan_zone_graveyard_revival_group_substate_e,,,`

### fn13: 0x080883d4
- **CID(s)**: 0x133b = Spear Cretin (pw=58551308, card_0737)
- **Dispatch table entry**: [32] CID=0x133b, fn=0x080883d4+1
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,lr}; calls check_card_field5_is_nonzero, check_zone_slot_equip_eligible, write_equip_zone_entry_by_substate(substate=0xe). 152 bytes.
- **Size**: 152 bytes
- **Pool DWords**: 0x08088460 = 0x0201c4e0, 0x08088464 = 0x00000868, 0x08088468 = 0x0201c8f8
- **CID_REUSE/NEW**: REUSE SPEAR_CRETIN_CID=0x0000133b (card_info.inc line 797)
- **Proposed name**: `scan_zone_spear_cretin_substate_e`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Spear Cretin (SPEAR_CRETIN_CID=0x133b, pw=58551308). r0=player_id. Gate: check_card_field5_is_nonzero + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from equip zone write table entry [32].`
- **CSV row**: `0x080883d4,scan_zone_spear_cretin_substate_e,,,`

### fn14: 0x0808846c
- **CID(s)**: 0x1359 = Backup Soldier (pw=36280194, card_0762)
- **Dispatch table entry**: [38] CID=0x1359, fn=0x0808846c+1
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls check_card_field5_is_nonzero (0x0804ad48), get_card_extended_stat_field9 (0x080eef44), check_zone_slot_equip_eligible (0x08037434 = check_zone_slot_equip_eligible alt? 0x0804ad70), write_equip_zone_entry_by_substate(substate=0xe). 140 bytes.
- **Size**: 140 bytes
- **Pool DWords**: 0x080884e8 = 0x0201c4e0, 0x080884ec = 0x00000868, 0x080884f0 = 0x0201c8f8, 0x080884f4 = 0x000005dc (1500)
- **CID_REUSE/NEW**: REUSE BACKUP_SOLDIER_CID=0x00001359 (card_info.inc line 1623)
- **Proposed name**: `scan_zone_backup_soldier_substate_e`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Backup Soldier (BACKUP_SOLDIER_CID=0x1359, pw=36280194). r0=player_id. Gate: check_card_field5_is_nonzero + field9 check + equip eligible; LP threshold 0x5dc (1500); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatched from equip zone write table entry [38].`
- **CSV row**: `0x0808846c,scan_zone_backup_soldier_substate_e,,,`

### fn15: 0x080884f8
- **CID(s)**: 0x13a1 = Serpentine Princess (pw=71829750, card_0818)
- **Dispatch table entry**: [48] CID=0x13a1, fn=0x080884f8+1
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,lr}; calls check_card_field5_is_nonzero (0x0804ad48), get_card_extended_stat_field7 (0x080eee50), eval_equip_placement_full_check (0x0803bba4), find_effect_node_in_zone (0x0802fd60), write_equip_zone_entry_by_substate(substate=0xb). Full span 0x080884f8..0x080885a8 (includes degenerate 0x0808855a mid-loop). 176 bytes.
- **Size**: 176 bytes
- **Pool DWords**: 0x08088598 = 0x0201c4e0, 0x0808859c = 0x00000868, 0x080885a0 = 0x0201c740, 0x080885a4 = 0x000012a1
- **CID_REUSE/NEW**: NEW (0x13a1 not in card_info.inc -- value grep returns 0 hits)
- **Proposed name**: `scan_zone_serpentine_princess_substate_b`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Serpentine Princess (CID=0x13a1, pw=71829750). r0=player_id. Gate: field5 + field7>=3 + eval_equip_placement_full_check + find_effect_node_in_zone; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Addr 0x0808855a is mid-loop degenerate. Dispatched from write table entry [48].`
- **CSV row**: `0x080884f8,scan_zone_serpentine_princess_substate_b,,,`

### fn16: 0x080885a8
- **CID(s)**: 0x13ed = GAP_CID_13ED (unallocated, card_info.inc line 1390)
- **Dispatch table entry**: [49] CID=0x13ed, fn=0x080885a8+1
- **Body analysis**: push {r4,r5,r6,r7,lr}; single call to write_equip_zone_entry_by_substate(substate=0xb). Simple loop over zone array. 40 bytes.
- **Size**: 40 bytes
- **Pool DWords**: 0x080885cc = 0x0201e278 (different zone struct)
- **CID_REUSE/NEW**: REUSE GAP_CID_13ED=0x000013ed (card_info.inc line 1390)
- **Proposed name**: `scan_zone_cid_13ed_substate_b`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for unallocated CID 0x13ed (GAP_CID_13ED). r0=player_id. Simple loop over zone struct at 0x0201e278; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatched from equip zone write table entry [49].`
- **CSV row**: `0x080885a8,scan_zone_cid_13ed_substate_b,,,`

### fn17: 0x080885d0
- **CID(s)**: 0x13f5 (Return of the Doomed), 0x1449 (unallocated), 0x144c (unallocated), 0x1457 (The Forgiving Maiden)
- **Dispatch table entries**: [50], [53], [54], [56]
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls check_card_field5_is_nonzero, write_equip_zone_entry_by_substate(substate=0xe). Full span 0x080885d0..0x0808864c (includes degenerate 0x080885e0 mid-loop). 124 bytes.
- **Size**: 124 bytes
- **Pool DWords**: 0x08088640 = 0x0201c4e0, 0x08088644 = 0x00000868, 0x08088648 = 0x0201c8f8
- **CID_REUSE/NEW**: NEW: RETURN_OF_THE_DOOMED_CID=0x13f5, THE_FORGIVING_MAIDEN_CID=0x1457, cid_1449=0x1449 (0 hits value grep each). REUSE: ICID_RESERVED_D=0x144c (card_info.inc line 1403)
- **Proposed name**: `scan_zone_return_from_grave_group_substate_e`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for return-from-grave group: Return of the Doomed(0x13f5), cid_1449(unallocated), ICID_RESERVED_D(0x144c), The Forgiving Maiden(0x1457). Gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x080885e0 is mid-loop degenerate. Dispatched from write table entries [50,53,54,56].`
- **CSV row**: `0x080885d0,scan_zone_return_from_grave_group_substate_e,,,`

### fn18: 0x0808864c
- **CID(s)**: 0x13fe = De-Fusion (pw=95286165, card_0800)
- **Dispatch table entry**: [51] CID=0x13fe, fn=0x0808864c+1
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,lr}; complex De-Fusion check; uses pool CIDs 0x000010e2 (unallocated variant of Polymerization) and 0x000012e5 (Polymerization CID). Calls check_zone_slot_equip_eligible (0x08037434), write_equip_zone_entry_by_substate(substate=0xe). Full span 0x0808864c..0x080886f8 (includes degenerate 0x0808866c mid-loop). 172 bytes.
- **Size**: 172 bytes
- **Pool DWords**: 0x080886e8 = 0x0201c4e0, 0x080886ec = 0x000010e2, 0x080886f0 = 0x000012e5, 0x080886f4 = 0x00000868
- **CID_REUSE/NEW**: REUSE DE_FUSION_CID=0x000013fe (card_info.inc line 800). Pool vals: POLYMERIZATION_CID=0x12e5 REUSE (card_info.inc line 436); cid_10e2=0x10e2 REUSE (card_info.inc line 888).
- **Proposed name**: `scan_zone_de_fusion_substate_e`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for De-Fusion (DE_FUSION_CID=0x13fe, pw=95286165). r0=player_id. Checks for POLYMERIZATION_CID(0x12e5)/cid_10e2(0x10e2) in zone; check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x0808866c is mid-loop degenerate. Dispatched from write table entry [51].`
- **CSV row**: `0x0808864c,scan_zone_de_fusion_substate_e,,,`

### fn19: 0x080886f8
- **CID(s)**: 0x140b = Insect Imitation (pw=96965364, card_0960)
- **Dispatch table entry**: [52] CID=0x140b, fn=0x080886f8+1
- **Body analysis**: push {r4,r5,r6,r7,r8,r9,lr}; calls get_card_extended_stat_field6 (0x080eedf8), get_card_extended_stat_field7 (0x080eee50), eval_equip_placement_full_check (0x0803bba4), find_effect_node_in_zone (0x0802fd60), write_equip_zone_entry_by_substate(substate=0xd). Full span 0x080886f8..0x080887b0. 184 bytes.
- **Size**: 184 bytes
- **Pool DWords**: 0x080887a0 = 0x0201c4e0, 0x080887a4 = 0x00000868, 0x080887a8 = 0x0201c740, 0x080887ac = 0x000012a1
- **CID_REUSE/NEW**: REUSE INSECT_IMITATION_CID=0x0000140b (card_info.inc line 960)
- **Proposed name**: `scan_zone_insect_imitation_substate_d`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for Insect Imitation (INSECT_IMITATION_CID=0x140b, pw=96965364). r0=player_id. Gate: field6 + field7 + eval_equip_placement + find_effect_node; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatched from equip zone write table entry [52].`
- **CSV row**: `0x080886f8,scan_zone_insect_imitation_substate_d,,,`

### fn20: 0x080887b0
- **CID(s)**: 0x1452 = ICID_RESERVED_E (card_info.inc line 1404; reserved internal CID not in card-stats.s; between Empress Mantis 0x1453 and Bio-Mage 0x1456)
- **Dispatch table entry**: [55] CID=0x1452, fn=0x080887b0+1
- **Body analysis**: push {r4,r5,r6,r7,r8,lr}; calls get_card_extended_stat_field6 (0x080eedf8), write_equip_zone_entry_by_substate(substate=0xe). Full span 0x080887b0..0x0808882c (includes degenerate 0x080887ec post-BL code). 124 bytes.
- **Size**: 124 bytes
- **Pool DWords**: 0x08088820 = 0x0201c4e0, 0x08088824 = 0x00000868, 0x08088828 = 0x0201c8f8
- **CID_REUSE/NEW**: REUSE ICID_RESERVED_E=0x00001452 (card_info.inc line 1404)
- **Proposed name**: `scan_zone_cid_1452_substate_e`
- **Confidence**: high (body clear; CID reserved/unallocated; function name uses cid_ prefix per convention for reserved CIDs)
- **ASCII plate**: `Equip zone scan callback for ICID_RESERVED_E (0x1452, reserved internal CID; gap between Empress Mantis 0x1453 and Bio-Mage 0x1456). r0=player_id. Gate: get_card_extended_stat_field6; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Addr 0x080887ec is post-BL degenerate. Dispatched from write table entry [55].`
- **CSV row**: `0x080887b0,scan_zone_cid_1452_substate_e,,,`

### fn21: 0x0808882c
- **CID(s)**: 0x1476 (Ancient Lamp), 0x15d0 (Decayed Commander), 0x15d4 (Vampire Orchis), 0x165b (Contract with Exodia), 0x16fd (Don Turtle), 0x17dd (Red-Eyes B. Chick), 0x1821 (The Creator Incarnate), 0x189a (Kaibaman)
- **Dispatch table entries**: [62], [118], [119], [141], [169], [209], [226], [249]
- **Body analysis**: push {r4,r5,r6,lr}; BST comparison against CID pool: 0x165b, 0x1476, 0x15d4, 0x17dd, 0x1821, 0x1121, 0x15d1, 0x15d5, 0x1645, 0x0ff8, 0x0fa7. Calls check_card_is_equip_target_eligible (0x0804ab4c), write_equip_zone_entry_by_substate(substate=0xb). 216 bytes.
- **Size**: 216 bytes
- **Pool DWords**: 0x08088868 = 0x00000868, 0x0808886c = 0x0201c600, 0x08088870 = 0x0000165b, 0x08088874 = 0x00001476, 0x08088880 = 0x000015d4, 0x08088898 = 0x000017dd, 0x080888ac = 0x00001821, 0x080888b4 = 0x00001121, 0x080888bc = 0x000015d1, 0x080888c4 = 0x000015d5, 0x080888cc = 0x00001645, 0x080888d8 = 0x00000ff8, 0x08088900 = 0x00000fa7
- **CID_REUSE/NEW**: REUSE ANCIENT_LAMP_CID=0x1476 (card_info.inc line 1211), DECAYED_COMMANDER_CID=0x15d0 (line 867), VAMPIRE_ORCHIS_CID=0x15d4 (line 870), CONTRACT_WITH_EXODIA_CID=0x165b (line 1204), DON_TURTLE_CID=0x16fd (line 1323). NEW: RED_EYES_B_CHICK_CID=0x17dd, THE_CREATOR_INCARNATE_CID=0x1821, KAIBAMAN_CID=0x189a (value grep 0 hits each). Pool exclusion CIDs (not dispatch entries): 0x1121 (La Jinn), 0x15d1 (Zombie Tiger), 0x15d5 (Des Dendle), 0x1645 (Exodia Necross), 0x0ff8 (Red-Eyes B. Dragon), 0x0fa7 (Blue-Eyes White Dragon).
- **Proposed name**: `scan_zone_special_category_equip_group_substate_b`
- **Confidence**: high
- **ASCII plate**: `Equip zone scan callback for special equip category group B: Ancient Lamp(0x1476), Decayed Commander(0x15d0), Vampire Orchis(0x15d4), Contract with Exodia(0x165b), Don Turtle(0x16fd), Red-Eyes B. Chick(0x17dd), The Creator Incarnate(0x1821), Kaibaman(0x189a). BST of 11 CIDs; check_card_is_equip_target_eligible; write_equip_zone_entry_by_substate(0xb). Dispatched from write table entries [62,118,119,141,169,209,226,249].`
- **CSV row**: `0x0808882c,scan_zone_special_category_equip_group_substate_b,,,`

---

## EQ_SLOTS (data-equate plan)

The fixer will createDWord for each pool address (listed in Literal Pool section).
EQ equates to add to card_info.inc for NEW CIDs:

```
.equ cid_12f4,                  0x000012f4  @ unallocated slot (gap in 0x12f3..0x12f8 range); scan_zone_cid_12f4_substate_d
.equ SOUL_RELEASE_CID,          0x000012f9  @ Soul Release (pw=05758500; card_0680 slot=0x12F9)
.equ LAST_WILL_CID,             0x00001315  @ Last Will (pw=85602018; card_0703 slot=0x1315)
.equ PAINFUL_CHOICE_CID,        0x0000132f  @ Painful Choice (pw=74191942; card_0726 slot=0x132F)
.equ UFO_TURTLE_CID,            0x00001335  @ UFO Turtle (pw=60806437; card_0732 slot=0x1335)
.equ MOTHER_GRIZZLY_CID,        0x0000133e  @ Mother Grizzly (pw=57839750; card_0739 slot=0x133E)
.equ FLYING_KAMAKIRI_1_CID,     0x0000133f  @ Flying Kamakiri #1 (pw=84834865; card_0740 slot=0x133F)
.equ SENJU_CID,                 0x00001334  @ Senju of the Thousand Hands (pw=23401839; card_0731 slot=0x1334)
.equ TROOP_DRAGON_CID,          0x000014dd  @ Troop Dragon (pw=55013285; card_1037 slot=0x14DD)
.equ KINGS_KNIGHT_CID,          0x000015b6  @ King's Knight (pw=64788463; card_1207 slot=0x15B6)
.equ HYENA_CID,                 0x00001867  @ Hyena (pw=22873798; card_1768 slot=0x1867)
.equ SONIC_BIRD_CID,            0x00001341  @ Sonic Bird (pw=57617178; card_0742 slot=0x1341)
.equ THE_SHALLOW_GRAVE_CID,     0x00001365  @ The Shallow Grave (pw=43434803; card_0772 slot=0x1365)
.equ THE_CREATOR_CID,           0x00001820  @ The Creator (pw=61505339; card_1701 slot=0x1820)
.equ SERPENTINE_PRINCESS_CID,   0x000013a1  @ Serpentine Princess (pw=71829750; card_0818 slot=0x13A1)
.equ RETURN_OF_THE_DOOMED_CID,  0x000013f5  @ Return of the Doomed (pw=19827717; card_0866 slot=0x13F5)
.equ cid_1449,                  0x00001449  @ unallocated slot (not in card-stats.s; gap between 0x1448 and 0x144b)
.equ THE_FORGIVING_MAIDEN_CID,  0x00001457  @ The Forgiving Maiden (pw=84080938; card_0923 slot=0x1457)
.equ RED_EYES_B_CHICK_CID,      0x000017dd  @ Red-Eyes B. Chick (pw=36262024; card_1643 slot=0x17DD)
.equ THE_CREATOR_INCARNATE_CID, 0x00001821  @ The Creator Incarnate (pw=97093037; card_1702 slot=0x1821)
.equ KAIBAMAN_CID,              0x0000189a  @ Kaibaman (pw=34627841; card_1812 slot=0x189A)
```

REUSE (already in card_info.inc — do NOT add new equates):
- 0x12e5: POLYMERIZATION_CID (line 436) — fn18 pool val; same card, same CID
- 0x10e2: cid_10e2 (line 888) — fn18 pool val; unallocated fusion variant
- 0x136a: BUBONIC_VERMIN_CID (line 726) — fn09
- 0x194f: HYDROGEDDON_CID (line 943) — fn09
- 0x1488: GILASAURUS_CID (line 732) — fn12
- 0x144c: ICID_RESERVED_D (line 1403) — fn17
- 0x1452: ICID_RESERVED_E (line 1404) — fn20
- 0x15d0: DECAYED_COMMANDER_CID (line 867) — fn21
- 0x15d4: VAMPIRE_ORCHIS_CID (line 870) — fn21
- 0x165b: CONTRACT_WITH_EXODIA_CID (line 1204) — fn21
- 0x16fd: DON_TURTLE_CID (line 1323) — fn21

---

## REF_SLOTS (createDWordWithRef plan, REF=36)

Per Seg-3b precedent (commit 793378c): every pool DWord whose value is an EWRAM address
must use createDWordWithRef + RENAME so it exports as `.word gP1LifePoints` not `.word 0x0201c4e0`.

### EWRAM pointer pools (36 slots total)

**gP1LifePoints = 0x0201c4e0** (ewram.inc line 79) — 18 slots:

| slot addr | fn | proposed slot label |
|-----------|----|--------------------|
| 0x08087d94 | fn01 | ptr_lp_87d94 |
| 0x08087e00 | fn02 | ptr_lp_87e00 |
| 0x08087ea8 | fn03 | ptr_lp_87ea8 |
| 0x08087fb4 | fn04 | ptr_lp_87fb4 |
| 0x08088044 | fn05 | ptr_lp_88044 |
| 0x080880b8 | fn06 | ptr_lp_880b8 |
| 0x08088180 | fn07 | ptr_lp_88180 |
| 0x08088208 | fn08 | ptr_lp_88208 |
| 0x0808827c | fn09 | ptr_lp_8827c |
| 0x080882f8 | fn10 | ptr_lp_882f8 |
| 0x080883c8 | fn12 | ptr_lp_883c8 |
| 0x08088460 | fn13 | ptr_lp_88460 |
| 0x080884e8 | fn14 | ptr_lp_884e8 |
| 0x08088598 | fn15 | ptr_lp_88598 |
| 0x08088640 | fn17 | ptr_lp_88640 |
| 0x080886e8 | fn18 | ptr_lp_886e8 |
| 0x080887a0 | fn19 | ptr_lp_887a0 |
| 0x08088820 | fn20 | ptr_lp_88820 |

**gP1SlotSetCodeArray = 0x0201c740** (ewram.inc line 332) — 8 slots:

| slot addr | fn | proposed slot label |
|-----------|----|--------------------|
| 0x08087eb0 | fn03 | ptr_sca_87eb0 |
| 0x08087f44 | fn04 | ptr_sca_87f44 |
| 0x0808804c | fn05 | ptr_sca_8804c |
| 0x08088188 | fn07 | ptr_sca_88188 |
| 0x08088210 | fn08 | ptr_sca_88210 |
| 0x08088300 | fn10 | ptr_sca_88300 |
| 0x080885a0 | fn15 | ptr_sca_885a0 |
| 0x080887a8 | fn19 | ptr_sca_887a8 |

**gP1HandSlotArray = 0x0201c8f8** (ewram.inc line 334) — 5 slots:

| slot addr | fn | proposed slot label |
|-----------|----|--------------------|
| 0x080883d0 | fn12 | ptr_hsa_883d0 |
| 0x08088468 | fn13 | ptr_hsa_88468 |
| 0x080884f0 | fn14 | ptr_hsa_884f0 |
| 0x08088648 | fn17 | ptr_hsa_88648 |
| 0x08088828 | fn20 | ptr_hsa_88828 |

**gP1FieldArrayCBase = 0x0201c600** (ewram.inc line 366) — 2 slots:

| slot addr | fn | proposed slot label |
|-----------|----|--------------------|
| 0x0808835c | fn11 | ptr_fac_8835c |
| 0x0808886c | fn21 | ptr_fac_8886c |

**gP1SlotCountBase = 0x0201c4f0** (ewram.inc line 331) — 2 slots:

| slot addr | fn | proposed slot label |
|-----------|----|--------------------|
| 0x08087f3c | fn04 | ptr_scb_87f3c |
| 0x08088194 | fn07 | ptr_scb_88194 |

**gEquipZoneBase_1d98 = 0x0201e278** (ewram.inc NEW — 1 slot):

| slot addr | fn | proposed slot label |
|-----------|----|--------------------|
| 0x080885cc | fn16 | ptr_ezb_885cc |

ewram.inc NEW entry needed:
```
.equ gEquipZoneBase_1d98,  0x0201e278  @ gP1LifePoints+0x1d98; equip zone scan base for GAP_CID_13ED (0x13ed) simple loop; 1 ROM ref (@0x080885cc, fn16 scan_zone_cid_13ed_substate_b)
```

REF count = 18 + 8 + 5 + 2 + 2 + 1 = **36**.

### Non-EWRAM pool slots (createDWord only, no ref)

Remaining 84 - 36 = 48 pool DWords hold CID values or scalar constants:
- CID values: equate to named CID constant per EQ_SLOTS plan (e.g. `.word GIANT_RAT_CID`)
- Scalar constants (no equate available): raw createDWord + ASCII EOL comment:
  - 0x00000868 = PLAYER_BLOCK_STRIDE (existing constant)
  - 0x000005dc = 1500 LP threshold (raw; no existing named constant)
  - 0x000012a1 = zone_query_hand_tag (existing label from Seg use)
  - 0xfffffdb0 = negative offset scalar (raw)
  - 0x00001b38 = scalar (raw)
  - 0x00001497, 0x000017ae = CID range compare values in fn05 (raw with EOL)

---

## Literal Pool DWord List (createDWord required, 84 addresses)

All pool addresses inside [0x08087d58, 0x08088904) must be force-created as DWords
by the fixer. Listed by function:

**fn01** (0x08087d58): 0x08087d94, 0x08087d98
**fn02** (0x08087d9c): 0x08087e00, 0x08087e04
**fn03** (0x08087e08): 0x08087ea8, 0x08087eac, 0x08087eb0, 0x08087eb4, 0x08087eb8
**fn04** (0x08087ebc): 0x08087f3c, 0x08087f40, 0x08087f44, 0x08087f48, 0x08087f4c, 0x08087fb4, 0x08087fb8, 0x08087fbc
**fn05** (0x08087fc0): 0x08088044, 0x08088048, 0x0808804c, 0x08088050, 0x08088054
**fn06** (0x08088058): 0x080880b8, 0x080880bc
**fn07** (0x080880c0): 0x08088180, 0x08088184, 0x08088188, 0x0808818c, 0x08088190, 0x08088194
**fn08** (0x08088198): 0x08088208, 0x0808820c, 0x08088210
**fn09** (0x08088214): 0x08088274, 0x08088278, 0x0808827c, 0x08088280
**fn10** (0x08088284): 0x080882f8, 0x080882fc, 0x08088300
**fn11** (0x08088304): 0x08088358, 0x0808835c
**fn12** (0x08088360): 0x080883c8, 0x080883cc, 0x080883d0
**fn13** (0x080883d4): 0x08088460, 0x08088464, 0x08088468
**fn14** (0x0808846c): 0x080884e8, 0x080884ec, 0x080884f0, 0x080884f4
**fn15** (0x080884f8): 0x08088598, 0x0808859c, 0x080885a0, 0x080885a4
**fn16** (0x080885a8): 0x080885cc
**fn17** (0x080885d0): 0x08088640, 0x08088644, 0x08088648
**fn18** (0x0808864c): 0x080886e8, 0x080886ec, 0x080886f0, 0x080886f4
**fn19** (0x080886f8): 0x080887a0, 0x080887a4, 0x080887a8, 0x080887ac
**fn20** (0x080887b0): 0x08088820, 0x08088824, 0x08088828
**fn21** (0x0808882c): 0x08088868, 0x0808886c, 0x08088870, 0x08088874, 0x08088880, 0x08088898, 0x080888ac, 0x080888b4, 0x080888bc, 0x080888c4, 0x080888cc, 0x080888d8, 0x08088900

---

## NEW CID Summary (card_info.inc additions)

21 NEW CIDs for this segment (value grep in card_info.inc = 0 hits each, re-verified):

| CID | name | card-stats.s evidence |
|-----|------|-----------------------|
| 0x12f4 | cid_12f4 | not in card-stats.s (gap) |
| 0x12f9 | SOUL_RELEASE_CID | card_0680 slot=0x12F9 line 8855 |
| 0x1315 | LAST_WILL_CID | card_0703 slot=0x1315 line 9154 |
| 0x132f | PAINFUL_CHOICE_CID | card_0726 slot=0x132F line 9453 |
| 0x1335 | UFO_TURTLE_CID | card_0732 slot=0x1335 line 9531 |
| 0x133e | MOTHER_GRIZZLY_CID | card_0739 slot=0x133E line 9622 |
| 0x133f | FLYING_KAMAKIRI_1_CID | card_0740 slot=0x133F line 9635 |
| 0x1334 | SENJU_CID | card_0731 slot=0x1334 line 9518 |
| 0x14dd | TROOP_DRAGON_CID | card_1037 slot=0x14DD line 13496 |
| 0x15b6 | KINGS_KNIGHT_CID | card_1207 slot=0x15B6 line 15706 |
| 0x1867 | HYENA_CID | card_1768 slot=0x1867 line 22999 |
| 0x1341 | SONIC_BIRD_CID | card_0742 slot=0x1341 line 9661 |
| 0x1365 | THE_SHALLOW_GRAVE_CID | card_0772 slot=0x1365 line 10051 |
| 0x1820 | THE_CREATOR_CID | card_1701 slot=0x1820 line 22128 |
| 0x13a1 | SERPENTINE_PRINCESS_CID | card_0818 slot=0x13A1 line 10649 |
| 0x13f5 | RETURN_OF_THE_DOOMED_CID | card_0866 slot=0x13F5 line 11273 |
| 0x1449 | cid_1449 | not in card-stats.s (gap; neighbors 0x144b Amazon Archer, 0x144d Fire Princess) |
| 0x1457 | THE_FORGIVING_MAIDEN_CID | card_0923 slot=0x1457 line 12014 |
| 0x17dd | RED_EYES_B_CHICK_CID | card_1643 slot=0x17DD line 21374 |
| 0x1821 | THE_CREATOR_INCARNATE_CID | card_1702 slot=0x1821 line 22141 |
| 0x189a | KAIBAMAN_CID | card_1812 slot=0x189A line 23571 |

Total: 21 NEW equates to add to card_info.inc.
(Derivation: original 29 table rows - 9 reclassified REUSE from table [BUBONIC_VERMIN, HYDROGEDDON,
GILASAURUS, cid_144c, cid_1452, DECAYED_COMMANDER, VAMPIRE_ORCHIS, CONTRACT_WITH_EXODIA, DON_TURTLE]
+ 1 UFO_TURTLE_CID added = 21. Two additional fn18 pool entries [0x12e5, 0x10e2] were already REUSE
in EQ_SLOTS note, not formal table rows.)

REUSE (already in card_info.inc, value grep confirmed — do NOT add new equates):
- 0x137c: DUST_TORNADO_CID (line 1579)
- 0x133b: SPEAR_CRETIN_CID (line 797)
- 0x1359: BACKUP_SOLDIER_CID (line 1623)
- 0x13ed: GAP_CID_13ED (line 1390)
- 0x13fe: DE_FUSION_CID (line 800)
- 0x140b: INSECT_IMITATION_CID (line 960)
- 0x1333: GIANT_RAT_CID (line 499)
- 0x133c: SHINING_ANGEL_CID (line 503)
- 0x1342: MYSTIC_TOMATO_CID (line 504)
- 0x1339: GIANT_GERM_CID (line 501)
- 0x133a: NIMBLE_MOMONGA_CID (line 502)
- 0x19a7: HERO_KID_CID (line 1268)
- 0x1476: ANCIENT_LAMP_CID (line 1211)
- 0x190a: DARK_RULER_VANDALGYON_CID (line 837)
- 0x137d: CALL_OF_THE_HAUNTED_CID (line 568)
- 0x1366: PREMATURE_BURIAL_CID (line 569)
- 0x136a: BUBONIC_VERMIN_CID (line 726)
- 0x194f: HYDROGEDDON_CID (line 943)
- 0x1488: GILASAURUS_CID (line 732)
- 0x144c: ICID_RESERVED_D (line 1403)
- 0x1452: ICID_RESERVED_E (line 1404)
- 0x15d0: DECAYED_COMMANDER_CID (line 867)
- 0x15d4: VAMPIRE_ORCHIS_CID (line 870)
- 0x165b: CONTRACT_WITH_EXODIA_CID (line 1204) — card_1331 slot=0x165B
- 0x16fd: DON_TURTLE_CID (line 1323)
- 0x12e5: POLYMERIZATION_CID (line 436) — fn18 pool
- 0x10e2: cid_10e2 (line 888) — fn18 pool

---

## disasm Plan (R4)

**Range**: [0x08087d58, 0x08088904)
**Mode**: THUMB

**Fixer script steps**:
1. clearListing 0x08087d58..0x08088904
2. setTMode THUMB for entire range
3. Per-function DisassembleCommand in address order (21 entries):
   0x08087d58, 0x08087d9c, 0x08087e08, 0x08087ebc, 0x08087fc0,
   0x08088058, 0x080880c0, 0x08088198, 0x08088214, 0x08088284,
   0x08088304, 0x08088360, 0x080883d4, 0x0808846c, 0x080884f8,
   0x080885a8, 0x080885d0, 0x0808864c, 0x080886f8, 0x080887b0,
   0x0808882c
4. createFunction at each of the 21 entries above
5. force-createDWord for each pool address (84 total, listed above)
6. Do NOT createFunction at degenerate addresses:
   0x08088354, 0x08088394, 0x0808855a, 0x0808866c, 0x080887ec, 0x08088080

**Post-disasm gate**: grep `ROM_INCBIN\|\.byte` in asm/11_effect_slot_puzzletext.s lines
covering 0x08087d58..0x08088904 must return 0 matches after export.

---

## carve Plan

None -- no data tables or code needing carve in this segment.

## §5.1 Entries

None -- all bytes in [0x08087d58, 0x08088904) are part of real functions (0 unref orphans).

---

## Consumer Evidence Summary

- All 21 functions are called via dispatch table 0x09e5a128 `{CID, fn_ptr+1}` format.
  Caller: `dispatch_equip_zone_write_by_substate_range` (0x0808d7f4), which loops through
  the table and calls each fn_ptr with r0=player_id.
- `write_equip_zone_entry_by_substate` (0x0808d88c) is the callee for zone writes.
  Evidence: asm/11_effect_slot_puzzletext.s line 6189. Confidence: high.
- check_card_field5_is_nonzero (0x0804ad48): asm/05_equip_eligibility_a.s line 3883. Confidence: high.
- check_zone_slot_equip_eligible (0x08037434): asm/03_equip_chain_hand.s line 2880. Confidence: high.
- eval_equip_placement_full_check (0x0803bba4): asm/03_equip_chain_hand.s line 12838. Confidence: high.
- find_effect_node_in_zone (0x0802fd60): asm/02_text_lp_fieldspell.s line 8191. Confidence: high.

---

## Self-Check (Phase 4)

1. **Pool values verified**: all 84 pool addresses decoded via `(PC&~2)+4+imm8*4` formula.
   Key pairs: 0x0201c4e0 = gP1LifePoints (confirmed from Seg-1..3 usage), 0x00000868 = PLAYER_BLOCK_STRIDE.
2. **Degenerate entries**: 6 confirmed as mid-function/epilogue by code-flow analysis (not LZ false positives).
3. **Plate text**: all ASCII only, no CJK. Verified by inspection.
4. **Slot names**: all `^[a-z][a-z0-9_]+$`. Checked.
5. **CID values**: C5 double-check: REUSE CIDs confirmed present by value grep; NEW CIDs confirmed absent.
6. **fn18 body span**: 0x080884f8..0x080885a8 confirmed (fn19 degenerate at 0x0808855a is mid-loop).
7. **fn06 body span**: 0x08088058..0x080880c0 confirmed (fn07 degenerate at 0x08088080 is mid-loop).
