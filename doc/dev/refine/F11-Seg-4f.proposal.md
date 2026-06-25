# Refine Proposal: F11-Seg-4f  [0x0808bb7c..0x0808cabc)

## Segment Survey

- ROM range: `[0x0808bb7c, 0x0808cabc)` = 0xF40 bytes (3904 B)
- Source: one-liner `ROM_INCBIN 0x8bb7c, <size>` (giant block, after Seg-4e carved 0x0808ad8c..0x0808bb7c)
- Boundary at 0x0808bb7c = first entry after Seg-4e end (CID 0x1876 Rescue Cat); boundary at 0x0808cabc = next segment start (CID 0x1944)
- Functions: **25 real functions** (27 strong entries - 2 degenerate alt-entry fallthrough = 25 real)
- No ROM_INCBIN sub-blocks or data tables within this range -- pure THUMB code + literal pools

### Function type: equip zone scan callbacks (same pattern as Seg-4a/4b/4c/4d/4e)

All 25 real functions are equip zone scan callbacks dispatched from the 2-word table
`{CID, fn_ptr+1}` at ROM 0x09e5a128 (305 entries). Each callback scans player slot arrays
and calls `write_equip_zone_entry_by_substate` (0x0808d88c) to register eligible equip zone
candidates for a specific card or group of cards.

---

## Degenerate Strong Entry Analysis (2 of 27)

### Alt-entry fallthrough pairs

| addr | reason | evidence |
|------|---------|---------|
| 0x0808be88 | Mid-body continuation of fn07 (0x0808be6c). fn07 body ends at 0x0808be86 with `CMP r0,#0` (2800) and falls through into 0x0808be88. 0x0808be88 starts with `d158` = BNE, which is the branch for fn07's CMP. fn07 prologue is b5f0+4657+464e+4645+b4e0; fn07+fn08 share a single epilogue at 0x0808bfb2 (bc38+4698+46a1+46aa+bcf0+bc01+4700) that restores r8/r9/r10 saved by fn07 prologue. 0x0808be88 is mid-body code. | fn07 bytes at 0x0808be6c: b5f0/4657/464e/4645/b4e0/1c07/4692/LDR/LDR/ADD/LDR/LDRH/MOV r8,r0/CMP r0,#0; 0x0808be88: d158 (BNE +0xb4 to 0x0808bf3c) = direct continuation of CMP; epilogue at 0x0808bfb2 restores r8/r9/r10 saved by fn07 |
| 0x0808c3da | Mid-body continuation of fn17 (0x0808c3d0). fn17 body is 10 bytes (b5f0+4647+b480+1c07+2500) with no epilogue; it falls through to 0x0808c3da. fn17+fn18 share a single epilogue at 0x0808c444 (bc08+4698+bcf0+bc01+4700) that restores r8 saved by fn17 prologue (b480 = push{r7} where r7 was loaded from r8). 0x0808c3da is mid-body code. | fn17 bytes 0x0808c3d0..0x0808c3da: b5f0/4647/b480/1c07/2500 (push r4-r7+lr, save r8, push r7, mov r7=player_id, MOVS r5=0) -- no epilogue; 0x0808c3da: 481d LDR r0,[PC,#116]=gP1LifePoints = loop init = continuation; epilogue bc08+4698 at 0x0808c444 restores r8 |

### Weak Entry Analysis (1 flagged)

| addr | reason | evidence |
|------|---------|---------|
| 0x0808bf4a | Mid-body instruction `1c04` = MOV r4,r0 inside fn07+fn08 combined body. 0x0808bf4a = 0x0808be88+0xe2 (offset +0xe2 into the fn08 portion at 0x0808bf3c, where loop2 starts at 0x0808bf3c and 0x0808bf4a falls at loop2 offset+0xe). No dispatch table entry points here. | bytes 1c04 (MOV r4,r0) at offset+0xe inside fn08 loop2 starting 0x0808bf3c; fn07+fn08 epilogue at 0x0808bfb2; not a function entry |

---

## Dispatch Table CID Scan (all seg-4f entries, table at 0x09e5a128, 305 entries)

| fn | addr | CID(s) | card name(s) |
|----|------|--------|-------------|
| fn01 | 0x0808bb7c | 0x1876 | Rescue Cat |
| fn02 | 0x0808bc10 | 0x187a | A Feather of the Phoenix |
| fn03 | 0x0808bc4c | 0x187f | Centrifugal Field |
| fn04 | 0x0808bd04 | 0x1880 | Fulfillment of the Contract |
| fn05 | 0x0808bd78 | 0x1881 | Re-Fusion |
| fn06 | 0x0808bdec | 0x1889 | Beast Soul Swap |
| fn07+fn08 | 0x0808be6c+0x0808be88 | 0x1895 | Vampire Genesis |
| fn09 | 0x0808bfcc | 0x18c5 | King of the Skull Servants |
| fn10 | 0x0808c058 | 0x18cb | Double Attack |
| fn11 | 0x0808c0c8 | 0x18cc | Battery Charger |
| fn12 | 0x0808c154 | 0x18d4 | Hero Signal |
| fn13 | 0x0808c264 | 0x18d9 | Level Conversion Lab |
| fn14 | 0x0808c2a0 | 0x18da | Rock Bombardment |
| fn15 | 0x0808c2f8 | 0x18f7 | Wroughtweiler |
| fn16 | 0x0808c350 | 0x18fe | Power Bond |
| fn17+fn18 | 0x0808c3d0+0x0808c3da | 0x1900 | Summon Priest |
| fn19 | 0x0808c45c | 0x1908 | Bubble Shuffle |
| fn20 | 0x0808c4a8 | 0x191f | Fusion Recovery |
| fn21 | 0x0808c4fc | 0x1920 | Miracle Fusion |
| fn22 | 0x0808c5ec | 0x1921 | Dragon's Mirror |
| fn23 | 0x0808c6dc | 0x1927 | Spiritual Earth Art - Kurogane |
| fn24 | 0x0808c790 | 0x192b | A Rival Appears! |
| fn25 | 0x0808c808 | 0x1938 | Gilford the Legend |
| fn26 | 0x0808c97c | 0x1939 | Warrior Lady of the Wasteland |
| fn27 | 0x0808ca64 | 0x193a | Divine Sword - Phoenix Blade |

Note: 0x0808be88 and 0x0808c3da are NOT in the dispatch table (confirmed by exhaustive search of all 305 entries); they are degenerate alt-entry continuations of fn07 and fn17 respectively.

Size check: fn01..fn27 sum = 0x94+0x3c+0xb8+0x74+0x74+0x80+(0x1c+0x144)+0x8c+0x70+0x8c+0x110+0x3c+0x58+0x58+0x80+(0x0a+0x82)+0x4c+0x54+0xf0+0xf0+0xb4+0x78+0x174+0xe8+0x58 = 0xF40 = 3904 B. Confirmed.

---

## Function Naming Table (25 real functions)

Substate semantics (from existing plate for write_equip_zone_entry_by_substate):
- 0xb = field-spell zone type B
- 0xc = chain zone type C
- 0xd = monster zone type D
- 0xe = hand slot type E

### fn01: 0x0808bb7c  size=0x094 (148 B)
- CID: 0x1876 (Rescue Cat), dispatch entry [CID 0x1876]
- Body: push {r4..r7,lr} + push {r8}; scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gate: get_card_extended_stat_field6 (0x080eedf8) == 0x6 (Beast race); write substate_d
- BL targets: 0x080eedf8 (get_card_extended_stat_field6), 0x0808d88c (write_equip_zone_entry_by_substate)
- Pool: 0x0808bc04=gP1LifePoints, 0x0808bc08=PLAYER_BLOCK_STRIDE, 0x0808bc0c=gP1SlotSetCodeArray
- CID status: RESCUE_CAT_CID(0x1876) NEW
- Substate: 0xd (MOVS r1,#0xd at 0x0808bbe2 before BL write_equip)
- Proposed name: `scan_zone_rescue_cat_substate_d`
- Confidence: high (body: SlotSetCodeArray monster zone + field6 race-6 gate; Rescue Cat discards itself to SS 2 Beast-type monsters ATK<=1000; write_d = monster zone)
- ASCII plate (len=279): `Equip zone scan for Rescue Cat (RESCUE_CAT_CID=0x1876, pw=14878871). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gate: get_card_extended_stat_field6 (race check, field6=0x6); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x1876].`

### fn02: 0x0808bc10  size=0x03c (60 B)
- CID: 0x187a (A Feather of the Phoenix), dispatch entry [CID 0x187a]
- Body: push {r4,r5,r6,lr}; simple loop via gP1LifePoints+gP1SlotSetCodeArray; direct CMP count + write substate_e; no gate BL beyond write_equip
- BL targets: 0x0808d88c (write_equip_zone_entry_by_substate)
- Pool: 0x0808bc44=gP1LifePoints, 0x0808bc48=PLAYER_BLOCK_STRIDE
- CID status: A_FEATHER_OF_THE_PHOENIX_CID(0x187a) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808bc2e before BL write_equip)
- Proposed name: `scan_zone_a_feather_of_the_phoenix_substate_e`
- Confidence: high (body: simple LP+stride loop, no gate filter; A Feather of the Phoenix discards hand to return LIGHT monsters from GY; write_e = hand slot)
- ASCII plate (len=268): `Equip zone scan for A Feather of the Phoenix (A_FEATHER_OF_THE_PHOENIX_CID=0x187a, pw=49140998). GY+hand zone via gP1LifePoints+PLAYER_BLOCK_STRIDE simple loop; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x187a].`

### fn03: 0x0808bc4c  size=0x0b8 (184 B)
- CID: 0x187f (Centrifugal Field), dispatch entry [CID 0x187f]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7} + b081 (SUB sp,#4); calls get_equip_display_type_code_by_card_id (0x0807f6f0) first; scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_pair_allowed (0x0807f730 -> actually get_equip_display_criteria_code_by_card_and_slot) + check_zone_slot_equip_eligible (0x08037434); write substate_e. Note: BL at 0x0808bcb4 = 0x0807f730 (get_equip_display_criteria_code_by_card_and_slot), BL at 0x0808bcba = 0x0804ab4c (check_card_pair_allowed)
- BL targets: 0x0807f6f0, 0x0807f730, 0x0804ab4c, 0x08037434, 0x0808d88c
- Pool: 0x0808bc9c=gP1LifePoints, 0x0808bca0=PLAYER_BLOCK_STRIDE, 0x0808bca4=gP1HandSlotArray, 0x0808bcfc=PLAYER_BLOCK_STRIDE(loop iter), 0x0808bd00=gP1HandCountBase
- CID status: CENTRIFUGAL_FIELD_CID(0x187f) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808bcd2 before BL write_equip)
- Proposed name: `scan_zone_centrifugal_field_substate_e`
- Confidence: high (body: hand zone + equip_display_criteria + pair_allowed + equip_eligible; Centrifugal Field destroys non-Fusion monsters and SS Fusion from Extra Deck; hand zone eligibility check; write_e = hand slot)
- ASCII plate (len=311): `Equip zone scan for Centrifugal Field (CENTRIFUGAL_FIELD_CID=0x187f, pw=01801154). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: get_equip_display_type_code + get_equip_display_criteria_code + check_card_pair_allowed + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x187f].`

### fn04: 0x0808bd04  size=0x074 (116 B)
- CID: 0x1880 (Fulfillment of the Contract), dispatch entry [CID 0x1880]
- Body: push {r4..r7,lr}; scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_type_is_trap (0x0804addc) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804addc (check_card_type_is_trap), 0x08037434, 0x0808d88c
- Pool: 0x0808bd6c=gP1LifePoints, 0x0808bd70=PLAYER_BLOCK_STRIDE, 0x0808bd74=gP1HandSlotArray
- CID status: FULFILLMENT_CONTRACT_CID(0x1880) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808bd4e before BL write_equip)
- Proposed name: `scan_zone_fulfillment_contract_substate_e`
- Confidence: high (body: hand zone + trap_type gate + equip_eligible; Fulfillment of the Contract SS a Ritual Monster from GY by paying LP; trap zone scan; write_e = hand slot)
- ASCII plate (len=303): `Equip zone scan for Fulfillment of the Contract (FULFILLMENT_CONTRACT_CID=0x1880, pw=48206762). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_type_is_trap + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1880].`

### fn05: 0x0808bd78  size=0x074 (116 B)
- CID: 0x1881 (Re-Fusion), dispatch entry [CID 0x1881]
- Body: push {r4..r7,lr}; scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_type_is_spell (0x0804adc8) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804adc8 (check_card_type_is_spell), 0x08037434, 0x0808d88c
- Pool: 0x0808bde0=gP1LifePoints, 0x0808bde4=PLAYER_BLOCK_STRIDE, 0x0808bde8=gP1HandSlotArray
- CID status: RE_FUSION_CID(0x1881) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808bdc2 before BL write_equip)
- Proposed name: `scan_zone_re_fusion_substate_e`
- Confidence: high (body: hand zone + spell_type gate + equip_eligible; Re-Fusion pays LP to SS a Fusion Monster from GY; hand zone scan; write_e)
- ASCII plate (len=275): `Equip zone scan for Re-Fusion (RE_FUSION_CID=0x1881, pw=74694807). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_type_is_spell + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x1881].`

### fn06: 0x0808bdec  size=0x080 (128 B)
- CID: 0x1889 (Beast Soul Swap), dispatch entry [CID 0x1889]
- Body: push {r4..r7,lr}; scan gP1FieldArrayCBase field spell zone (MOVS r0,#1 loop init); gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field6 (0x080eedf8, cmp r0,#0xb=Beast) + eval_equip_bonus_for_slot (0x080377b0) + eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x0804ad48, 0x080eedf8, 0x080377b0, 0x0803bba4, 0x0808d88c
- Pool: 0x0808be5c=PLAYER_BLOCK_STRIDE, 0x0808be60=gP1FieldArrayCBase, 0x0808be64=gDuelPhaseFlags, 0x0808be68=EQUIP_ACTIVE_CTX_OFF(0x484)
- CID status: BEAST_SOUL_SWAP_CID(0x1889) NEW
- Substate: 0xb (MOVS r1,#0xb at 0x0808be4e before BL write_equip)
- Proposed name: `scan_zone_beast_soul_swap_substate_b`
- Confidence: high (body: field spell zone + field5 + race-Beast + equip_bonus + placement; Beast Soul Swap returns a Beast-type monster from field to hand; uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF for active context; write_b = field spell zone)
- ASCII plate (len=357): `Equip zone scan for Beast Soul Swap (BEAST_SOUL_SWAP_CID=0x1889, pw=35149085). Field spell zone via gP1FieldArrayCBase; gates: check_card_field5_is_nonzero + get_card_extended_stat_field6 (race 0xb) + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write substate_b. Uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF. Dispatch table entry [CID 0x1889].`

### fn07+fn08: 0x0808be6c+0x0808be88  combined size=0x160 (352 B)
- CID: 0x1895 (Vampire Genesis), dispatch entry [CID 0x1895]
- fn07 [0x0808be6c..0x0808be88): prologue only -- push {r4..r7,lr} + mov r7=r10/r6=r9/r5=r8 + push {r5,r6,r7}; saves player_id to r7; loads gDuelPhaseFlags; reads [gDuelPhaseFlags+0] -> LDRH halfword -> saves to r8; CMP r0,#0; FALLS THROUGH to fn08
- fn08 [0x0808be88..0x0808bfcc): continuation; BNE to loop2 path; TWO-LOOP body: loop1 scans gP1FieldArrayCBase field zone, gates: check_card_field5_is_nonzero+get_card_extended_stat_field6+get_card_extended_stat_field5 x2+check_zone_slot_equip_eligible; write substate_b; loop2 scans gP1LifePoints+gP1HandSlotArray, same gates; write substate_e
- BL targets: 0x0804ad48, 0x080eedf8 (x2), 0x080eee50 (x2), 0x08037434, 0x0808d88c
- Pool (fn07 portion at 0x0808bf16..0x0808bf2e): 0x0808bf18=gDuelPhaseFlags, 0x0808bf1c=EQUIP_ACTIVE_CTX_OFF, 0x0808bf20=PLAYER_BLOCK_STRIDE, 0x0808bf24=gP1FieldArrayCBase, 0x0808bf28=0xfffffef4 (raw sentinel offset -0x10c), 0x0808bf2c=gP1HandSlotArray
- Pool (fn08 continuation at 0x0808bfc0..0x0808bfca): 0x0808bfc0=gP1LifePoints, 0x0808bfc4=PLAYER_BLOCK_STRIDE, 0x0808bfc8=gP1HandSlotArray
- CID status: VAMPIRE_GENESIS_CID(0x1895) REUSE
- Substates: 0xb (loop1, MOVS r1,#0xb at 0x0808bf32), 0xe (loop2, MOVS r1,#0xe at 0x0808bf9a)
- Note: 0x0808be88 is a degenerate strong entry (mid-body BNE after fn07's CMP); 0x0808bf4a is a degenerate weak entry (MOV r4,r0 mid-loop2)
- Proposed name: `scan_zone_vampire_genesis_substate_be`
- Confidence: high (body: field + hand dual-loop with field5+field6+field5 gates; Vampire Genesis SS Zombie monsters from GY; uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF; dispatch entry [CID 0x1895]; 0xfffffef4 = raw neg offset used with ADD for gDuelPhaseFlags pointer arithmetic)
- ASCII plate (len=430): `Equip zone scan for Vampire Genesis (VAMPIRE_GENESIS_CID=0x1895, pw=22056710). Two-loop: loop1 field zone (gP1FieldArrayCBase) gate field5+field6+field5 x2+equip_eligible -> substate_b; loop2 hand zone (gP1HandSlotArray) gate field5_nonzero+field6+field5+equip_eligible -> substate_e. Uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF. Dispatch entry [CID 0x1895]. combined fn: fn07 start=0x0808be6c; fn08(0x0808be88)=degenerate excluded.`

### fn09: 0x0808bfcc  size=0x08c (140 B)
- CID: 0x18c5 (King of the Skull Servants), dispatch entry [CID 0x18c5]
- Body: push {r4..r7,lr} + push {r8}; scan gP1LifePoints+gP1HandSlotArray hand zone; gate: card_type field extract (LSLS r1,r1,#4 + LSR #1) then CMP against SKULL_SERVANT_CID(0x0fbe) OR KING_OF_SKULL_SERVANTS_CID(0x18c5); write substate_e
- BL targets: 0x0808d88c
- Pool: 0x0808c044=gP1LifePoints, 0x0808c048=PLAYER_BLOCK_STRIDE, 0x0808c04c=gP1HandSlotArray, 0x0808c050=SKULL_SERVANT_CID(0x0fbe), 0x0808c054=KING_OF_SKULL_SERVANTS_CID(0x18c5)
- CID status: KING_OF_SKULL_SERVANTS_CID(0x18c5) REUSE; SKULL_SERVANT_CID(0x0fbe) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808c022 before BL write_equip)
- Proposed name: `scan_zone_king_skull_servants_substate_e`
- Confidence: high (body: hand zone + two-CID gate SKULL_SERVANT or KING_OF_SKULL_SERVANTS; King of the Skull Servants gains ATK for each Skull Servant in GY; write_e)
- ASCII plate (len=350): `Equip zone scan for King of the Skull Servants (KING_OF_SKULL_SERVANTS_CID=0x18c5, pw=36021814). Hand zone via gP1LifePoints+gP1HandSlotArray; gate: card_type field == SKULL_SERVANT_CID (0x0fbe) OR KING_OF_SKULL_SERVANTS_CID (0x18c5) + equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [CID 0x18c5].`

### fn10: 0x0808c058  size=0x070 (112 B)
- CID: 0x18cb (Double Attack), dispatch entry [CID 0x18cb]
- Body: push {r4,r5,r6,lr}; scan gP1FieldArrayCBase field spell zone (MOVS r0,#1 loop); gates: check_card_field5_is_nonzero (0x0804ad48) + eval_equip_bonus_for_slot (0x080377b0) + count_effect_node_activations_by_zone (0x080907f4); write substate_b; uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF
- BL targets: 0x0804ad48, 0x080377b0, 0x080907f4, 0x0808d88c
- Pool: 0x0808c0b8=PLAYER_BLOCK_STRIDE, 0x0808c0bc=gP1FieldArrayCBase, 0x0808c0c0=gDuelPhaseFlags, 0x0808c0c4=EQUIP_ACTIVE_CTX_OFF
- CID status: DOUBLE_ATTACK_CID(0x18cb) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808c0a8 before BL write_equip)
- Proposed name: `scan_zone_double_attack_substate_b`
- Confidence: high (body: field spell zone + field5 + equip_bonus + count_activations gate; Double Attack discards a Normal Monster to let Warrior attack twice; field spell zone; write_b = field spell zone)
- ASCII plate (len=348): `Equip zone scan for Double Attack (DOUBLE_ATTACK_CID=0x18cb, pw=34187685). Field spell zone via gP1FieldArrayCBase+gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF; gates: check_card_field5_is_nonzero + eval_equip_bonus_for_slot + count_effect_node_activations_by_zone; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entry [CID 0x18cb].`

### fn11: 0x0808c0c8  size=0x08c (140 B)
- CID: 0x18cc (Battery Charger), dispatch entry [CID 0x18cc]
- Body: push {r4..r7,lr} + push {r8}; scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_field5_is_nonzero (0x0804ad48) + check_card_is_batteryman_type (0x0804b250) + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x0804b250 (check_card_is_batteryman_type), 0x08037434, 0x0808d88c
- Pool: 0x0808c148=gP1LifePoints, 0x0808c14c=PLAYER_BLOCK_STRIDE, 0x0808c150=gP1HandSlotArray
- CID status: BATTERY_CHARGER_CID(0x18cc) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808c124 before BL write_equip)
- Proposed name: `scan_zone_battery_charger_substate_e`
- Confidence: high (body: hand zone + field5 + batteryman_type gate + equip_eligible; Battery Charger pays LP to SS a Batteryman from GY; write_e = hand slot)
- ASCII plate (len=323): `Equip zone scan for Battery Charger (BATTERY_CHARGER_CID=0x18cc, pw=61181383). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + check_card_is_batteryman_type + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x18cc].`

### fn12: 0x0808c154  size=0x110 (272 B)
- CID: 0x18d4 (Hero Signal), dispatch entry [CID 0x18d4]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7}; TWO-LOOP:
  loop1 scans gP1FieldArrayCBase field zone (+0xc offset); gates: check_card_id_is_normal_summon_type (0x0804b164) + eval_equip_bonus_for_slot (0x080377b0, cmp r0,#4) + eval_equip_placement_full_check (0x0803bba4); write substate_b;
  loop2 scans gP1SlotSetCodeArray monster zone; gates: check_card_id_is_normal_summon_type (0x0804b164) + get_card_extended_stat_field5 (0x080eee50, cmp r0,#4) + eval_equip_placement_full_check (0x0803bba4); write substate_d
- BL targets: 0x0804b164 (x2), 0x080377b0, 0x080eee50, 0x0803bba4 (x2), 0x0808d88c (x2)
- Pool: 0x0808c254=gP1LifePoints, 0x0808c258=PLAYER_BLOCK_STRIDE, 0x0808c25c=gP1FieldArrayCBase, 0x0808c260=gP1SlotSetCodeArray
- CID status: HERO_SIGNAL_CID(0x18d4) NEW
- Substates: 0xb (MOVS r1,#0xb at 0x0808c1c4), 0xd (MOVS r1,#0xd at 0x0808c22e)
- Proposed name: `scan_zone_hero_signal_substate_bd`
- Confidence: high (body: field+monster dual-loop with normal_summon_type gate; Hero Signal triggers when a monster is destroyed; write_b=field + write_d=monster zone)
- ASCII plate (len=379): `Equip zone scan for Hero Signal (HERO_SIGNAL_CID=0x18d4, pw=22020907). Two-loop: loop1 via gP1FieldArrayCBase (field, +0xc) gate check_card_id_is_normal_summon_type+eval_equip_bonus+eval_equip_placement -> substate_b; loop2 via gP1SlotSetCodeArray (monster) gate normal_summon+field5+eval_placement -> substate_d. Dispatch entry [CID 0x18d4].`

### fn13: 0x0808c264  size=0x03c (60 B)
- CID: 0x18d9 (Level Conversion Lab), dispatch entry [CID 0x18d9]
- Body: push {r4,r5,lr}; scan gP1FieldArrayCBase field spell zone (MOVS r0,#1 loop); gate: check_card_field5_is_nonzero (0x0804ad48); write substate_b
- BL targets: 0x0804ad48, 0x0808d88c
- Pool: 0x0808c298=PLAYER_BLOCK_STRIDE, 0x0808c29c=gP1FieldArrayCBase
- CID status: LEVEL_CONVERSION_LAB_CID(0x18d9) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808c28a before BL write_equip)
- Proposed name: `scan_zone_level_conversion_lab_substate_b`
- Confidence: high (body: field spell zone + field5 gate; Level Conversion Lab pays LP to change a monster's level; field spell zone; write_b)
- ASCII plate (len=262): `Equip zone scan for Level Conversion Lab (LEVEL_CONVERSION_LAB_CID=0x18d9, pw=84397023). Field spell zone via gP1FieldArrayCBase; gate: check_card_field5_is_nonzero; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x18d9].`

### fn14: 0x0808c2a0  size=0x058 (88 B)
- CID: 0x18da (Rock Bombardment), dispatch entry [CID 0x18da]
- Body: push {r4..r7,lr}; inner loop scan gP1LifePoints (stride 0x10, MOVS r4,#0x98 init); gate: get_card_extended_stat_field6 (0x080eedf8, cmp r0,#6=Rock type); write substate_d
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x0808c2f0=gP1LifePoints, 0x0808c2f4=PLAYER_BLOCK_STRIDE
- CID status: ROCK_BOMBARDMENT_CID(0x18da) REUSE
- Substate: 0xd (MOVS r1,#0xd at 0x0808c2d8 before BL write_equip)
- Proposed name: `scan_zone_rock_bombardment_substate_d`
- Confidence: high (body: inner loop with stride 0x10 and MOVS r4,#0x98 init + field6 Rock-race gate; Rock Bombardment discards a Rock from hand to destroy 1 S/T; monster zone; write_d)
- ASCII plate (len=288): `Equip zone scan for Rock Bombardment (ROCK_BOMBARDMENT_CID=0x18da, pw=20781762). Monster zone via gP1LifePoints inner loop (stride 0x10, init=0x98); gate: get_card_extended_stat_field6 == 0x6 (Rock type); write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch table entry [CID 0x18da].`

### fn15: 0x0808c2f8  size=0x058 (88 B)
- CID: 0x18f7 (Wroughtweiler), dispatch entry [CID 0x18f7]
- Body: push {r4..r7,lr}; inner loop scan gP1LifePoints (stride 0x14, MOVS r4,#0x83 init); gate: check_card_id_is_normal_summon_type (0x0804b164); write substate_e
- BL targets: 0x0804b164, 0x0808d88c
- Pool: 0x0808c348=gP1LifePoints, 0x0808c34c=PLAYER_BLOCK_STRIDE
- CID status: WROUGHTWEILER_CID(0x18f7) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808c330 before BL write_equip)
- Proposed name: `scan_zone_wroughtweiler_substate_e`
- Confidence: high (body: inner loop stride 0x14 + normal_summon gate; Wroughtweiler sends itself to GY to search Polymerization or Fusion Substitute; write_e = hand slot)
- ASCII plate (len=271): `Equip zone scan for Wroughtweiler (WROUGHTWEILER_CID=0x18f7, pw=06480253). Monster zone via gP1LifePoints inner loop (stride 0x14, init=0x83); gate: check_card_id_is_normal_summon_type; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x18f7].`

### fn16: 0x0808c350  size=0x080 (128 B)
- CID: 0x18fe (Power Bond), dispatch entry [CID 0x18fe]
- Body: push {r4..r7,lr} + push {r8}; scan gP1ChainZoneArray+gP1LifePoints chain zone; gates: get_card_extended_stat_field6 (0x080eedf8, cmp r0,#7=Machine) + build_equip_slot_criteria_from_card_range (0x0807fb9c); write substate_c
- BL targets: 0x080eedf8, 0x0807fb9c, 0x0808d88c
- Pool: 0x0808c3c4=gP1LifePoints, 0x0808c3c8=PLAYER_BLOCK_STRIDE, 0x0808c3cc=gP1ChainZoneArray
- CID status: POWER_BOND_CID(0x18fe) NEW
- Substate: 0xc (MOVS r1,#0xc at 0x0808c3a0 before BL write_equip)
- Proposed name: `scan_zone_power_bond_substate_c`
- Confidence: high (body: chain zone + Machine-race gate + build_equip_slot_criteria; Power Bond fuses Machine-type monsters; chain zone; write_c = chain zone)
- ASCII plate (len=314): `Equip zone scan for Power Bond (POWER_BOND_CID=0x18fe, pw=37630732). Chain zone via gP1ChainZoneArray+gP1LifePoints; gates: get_card_extended_stat_field6 == 7 (Machine type) + build_equip_slot_criteria_from_card_range; write_equip_zone_entry_by_substate(player_id, 0xc, slot_idx). Dispatch table entry [CID 0x18fe].`

### fn17+fn18: 0x0808c3d0+0x0808c3da  combined size=0x08c (140 B)
- CID: 0x1900 (Summon Priest), dispatch entry [CID 0x1900]
- fn17 [0x0808c3d0..0x0808c3da): prologue push {r4..r7,lr} + push {r8} + saves player_id + MOVS r5,#0; FALLS THROUGH
- fn18 [0x0808c3da..0x0808c45c): continuation; scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field5 (0x080eee50, cmp r0,#4) + eval_equip_placement_full_check (0x0803bba4); write substate_d
- BL targets: 0x0804ad48, 0x080eee50, 0x0803bba4, 0x0808d88c
- Pool: 0x0808c450=gP1LifePoints, 0x0808c454=PLAYER_BLOCK_STRIDE, 0x0808c458=gP1SlotSetCodeArray
- CID status: SUMMON_PRIEST_CID(0x1900) NEW
- Substate: 0xd (MOVS r1,#0xd at 0x0808c42c before BL write_equip)
- Note: 0x0808c3da is a degenerate strong entry (mid-body continuation of fn17 prologue); fn17+fn18 share single epilogue at 0x0808c444
- Proposed name: `scan_zone_summon_priest_substate_d`
- Confidence: high (body: monster zone + field5 + level4 + placement gates; Summon Priest discards a spell to SS a monster from deck; monster zone; write_d; fn17 start=0x0808c3d0; fn18(0x0808c3da) degenerate combined)
- ASCII plate (len=404): `Equip zone scan for Summon Priest (SUMMON_PRIEST_CID=0x1900, pw=00423585). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field5 (level 4) + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xd, slot_idx). Dispatch entry [CID 0x1900]. combined fn: fn17 start=0x0808c3d0; fn18(0x0808c3da)=degenerate excluded.`

### fn19: 0x0808c45c  size=0x04c (76 B)
- CID: 0x1908 (Bubble Shuffle), dispatch entry [CID 0x1908]
- Body: push {r4,r5,r6,lr}; scan gP1FieldArrayCBase field spell zone (MOVS r0,#1 loop); gates: check_card_id_is_normal_summon_type (0x0804b164) + eval_equip_placement_full_check (0x0803bba4); write substate_b
- BL targets: 0x0804b164, 0x0803bba4, 0x0808d88c
- Pool: 0x0808c4a4=gP1FieldArrayCBase
- CID status: BUBBLE_SHUFFLE_CID(0x1908) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808c492 before BL write_equip)
- Proposed name: `scan_zone_bubble_shuffle_substate_b`
- Confidence: high (body: field spell zone + normal_summon + placement; Bubble Shuffle switches an WATER HEROes attack/defense; field spell zone; write_b)
- ASCII plate (len=292): `Equip zone scan for Bubble Shuffle (BUBBLE_SHUFFLE_CID=0x1908, pw=61968753). Field spell zone via gP1FieldArrayCBase; gates: check_card_id_is_normal_summon_type + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch table entry [CID 0x1908].`

### fn20: 0x0808c4a8  size=0x054 (84 B)
- CID: 0x191f (Fusion Recovery), dispatch entry [CID 0x191f]
- Body: push {r4..r7,lr}; inner loop scan gP1LifePoints (stride 0x14, MOVS r4,#0x83 init); gate: check_card_id_is_normal_summon_type (0x0804b164); write substate_e; note: inner loop checks r4,r3 bit field (0x03c0 = field bits)
- BL targets: 0x0804b164, 0x0808d88c
- Pool: 0x0808c4f4=gP1LifePoints, 0x0808c4f8=PLAYER_BLOCK_STRIDE
- CID status: FUSION_RECOVERY_CID(0x191f) NEW
- Substate: 0xe (MOVS r1,#0xe at 0x0808c4dc before BL write_equip)
- Proposed name: `scan_zone_fusion_recovery_substate_e`
- Confidence: high (body: inner loop stride 0x14 + normal_summon gate; Fusion Recovery returns 1 Polymerization and 1 Fusion Material from GY to hand; write_e = hand slot)
- ASCII plate (len=275): `Equip zone scan for Fusion Recovery (FUSION_RECOVERY_CID=0x191f, pw=18511384). Monster zone via gP1LifePoints inner loop (stride 0x14, init=0x83); gate: check_card_id_is_normal_summon_type; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x191f].`

### fn21: 0x0808c4fc  size=0x0f0 (240 B)
- CID: 0x1920 (Miracle Fusion), dispatch entry [CID 0x1920]
- Body: push {r4..r7,lr} + push {r8}; TWO-PATH: if r2!=0 -> scan gP1ChainZoneArray chain zone, gate: check_spell_zone_slot_placeable (0x0803bc24) -> write substate_c; after chain zone path and alternate path, scan gP1LifePoints simple loop gate check_equip_slot_eligible_with_criteria_and_prerequisites (0x08080348) -> write substate_e
- BL targets: 0x0804b164 (check_card_id_is_normal_summon_type in chain-zone inner), 0x0803bc24 (check_spell_zone_slot_placeable), 0x08080348 (check_equip_slot_eligible_with_criteria_and_prerequisites), 0x0808d88c (x2)
- Pool: 0x0808c56c=gP1LifePoints, 0x0808c570=PLAYER_BLOCK_STRIDE, 0x0808c574=gP1ChainZoneArray, 0x0808c5e4=gP1LifePoints(pool2), 0x0808c5e8=PLAYER_BLOCK_STRIDE(pool2)
- CID status: MIRACLE_FUSION_CID(0x1920) NEW
- Substates: 0xc (MOVS r1,#0xc at 0x0808c550), 0xe (MOVS r1,#0xe at 0x0808c5bc (conditional path) and 0x0808c5ca (alternate path))
- Proposed name: `scan_zone_miracle_fusion_substate_ce`
- Confidence: high (body: r2-gated chain zone (substate_c) + hand zone (substate_e); Miracle Fusion banishes HERO monsters to Fusion Summon; chain+hand zones; dispatch [CID 0x1920])
- ASCII plate (len=351): `Equip zone scan for Miracle Fusion (MIRACLE_FUSION_CID=0x1920, pw=45906428). Two-path: if r2!=0 scan chain zone (gP1ChainZoneArray) gate check_spell_zone_slot_placeable -> substate_c; then scan hand zone (gP1LifePoints loop) gate check_equip_slot_eligible_with_criteria_and_prerequisites -> substate_e. Dispatch entry [CID 0x1920].`

### fn22: 0x0808c5ec  size=0x0f0 (240 B)
- CID: 0x1921 (Dragon's Mirror), dispatch entry [CID 0x1921]
- Body: push {r4..r7,lr} + push {r8}; TWO-PATH (same structure as fn21): if r2!=0 -> chain zone gate get_card_extended_stat_field6 (0x080eedf8, cmp r0,#1=DARK type) + check_spell_zone_slot_placeable -> write substate_c; then gP1LifePoints loop gate check_equip_slot_eligible_with_criteria -> write substate_e
- BL targets: 0x080eedf8, 0x0803bc24, 0x08080348, 0x0808d88c (x2)
- Pool: 0x0808c65c=gP1LifePoints, 0x0808c660=PLAYER_BLOCK_STRIDE, 0x0808c664=gP1ChainZoneArray, 0x0808c6d4=gP1LifePoints(pool2), 0x0808c6d8=PLAYER_BLOCK_STRIDE(pool2)
- CID status: DRAGONS_MIRROR_CID(0x1921) REUSE
- Substates: 0xc (MOVS r1,#0xc at 0x0808c640), 0xe (MOVS r1,#0xe at 0x0808c6ac (conditional path) and 0x0808c6ba (alternate path))
- Proposed name: `scan_zone_dragons_mirror_substate_ce`
- Confidence: high (body: r2-gated chain zone DARK-type gate (substate_c) + hand loop (substate_e); Dragon's Mirror banishes Dragon-type monsters to Fusion Summon; structure mirrors fn21/Miracle Fusion; dispatch [CID 0x1921])
- ASCII plate (len=333): `Equip zone scan for Dragons Mirror (DRAGONS_MIRROR_CID=0x1921, pw=71490127). Two-path: if r2!=0 scan chain zone (gP1ChainZoneArray) gate field6==1 (DARK) + check_spell_zone_slot_placeable -> substate_c; then hand zone loop gate check_equip_slot_eligible_with_criteria -> substate_e. Dispatch entry [CID 0x1921].`

### fn23: 0x0808c6dc  size=0x0b4 (180 B)
- CID: 0x1927 (Spiritual Earth Art - Kurogane), dispatch entry [CID 0x1927]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7}; scan gP1LifePoints+gP1HandSlotArray hand zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field5 (0x080eee50, cmp r0,#4=level gate) + check_card_stat_field7_equals (0x08030b70, MOVS r1,#5 -> EARTH attr check) + level-extract bit op + check_zone_slot_equip_eligible (0x08037434); write substate_e
- BL targets: 0x0804ad48, 0x080eee50, 0x08030b70, 0x08037434, 0x0808d88c
- Pool: 0x0808c784=gP1LifePoints, 0x0808c788=PLAYER_BLOCK_STRIDE, 0x0808c78c=gP1HandSlotArray
- CID status: SPIRITUAL_EARTH_ART_CID(0x1927) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808c75c before BL write_equip)
- Proposed name: `scan_zone_spiritual_earth_art_substate_e`
- Confidence: high (body: hand zone + field5 + level4 + EARTH-attr(5) gate + equip_eligible; Spiritual Earth Art tributes an EARTH monster to return another from GY to hand; write_e = hand slot)
- ASCII plate (len=398): `Equip zone scan for Spiritual Earth Art - Kurogane (SPIRITUAL_EARTH_ART_CID=0x1927, pw=70156997). Hand zone via gP1LifePoints+gP1HandSlotArray; gates: check_card_field5_is_nonzero + get_card_extended_stat_field5 (level) + check_card_stat_field7_equals(5) (EARTH attr) + level bit-extract + check_zone_slot_equip_eligible; write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch entry [CID 0x1927].`

### fn24: 0x0808c790  size=0x078 (120 B)
- CID: 0x192b (A Rival Appears!), dispatch entry [CID 0x192b]
- Body: push {r4..r7,lr}; scan gP1FieldArrayCBase field spell zone (MOVS r0,#1 loop); gates: check_card_field5_is_nonzero (0x0804ad48) + eval_equip_bonus_for_slot (0x080377b0) + eval_equip_placement_full_check (0x0803bba4); write substate_b; uses gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF
- BL targets: 0x0804ad48, 0x080377b0, 0x0803bba4, 0x0808d88c
- Pool: 0x0808c7f8=PLAYER_BLOCK_STRIDE, 0x0808c7fc=gP1FieldArrayCBase, 0x0808c800=gDuelPhaseFlags, 0x0808c804=EQUIP_ACTIVE_CTX_OFF
- CID status: A_RIVAL_APPEARS_CID(0x192b) REUSE
- Substate: 0xb (MOVS r1,#0xb at 0x0808c7e8 before BL write_equip)
- Proposed name: `scan_zone_a_rival_appears_substate_b`
- Confidence: high (body: field spell zone + field5 + equip_bonus + placement; A Rival Appears! SSs a monster matching ATK; field spell zone; write_b)
- ASCII plate (len=347): `Equip zone scan for A Rival Appears! (A_RIVAL_APPEARS_CID=0x192b, pw=05728014). Field spell zone via gP1FieldArrayCBase+gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF; gates: check_card_field5_is_nonzero + eval_equip_bonus_for_slot + eval_equip_placement_full_check; write_equip_zone_entry_by_substate(player_id, 0xb, slot_idx). Dispatch entry [CID 0x192b].`

### fn25: 0x0808c808  size=0x174 (372 B)
- CID: 0x1938 (Gilford the Legend), dispatch entry [CID 0x1938]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7} + b08b (SUB sp,#0x2c stack frame); memset (0x0810e9bc) init; TWO-LOOP: loop1 scans gDuelFieldSlots (0x0201c510, stride PLAYER_BLOCK_STRIDE) checking field slots; gate: get_slot_card_state_code (0x0803abf0) + check_slot_card_eligible_by_card_id (0x0804f6c4); loop2 scans gP1LifePoints+gP1HandSlotArray hand zone; gate: get_card_extended_stat_field9 (0x080eee7c) + bit-mask 0xffff803f check + check_slot_card_eligible_by_card_id (0x0804f6c4); write substate_e
- BL targets: 0x0810e9bc (memset), 0x0803abf0, 0x0804f6c4, 0x080eedc78 (typo -- actually 0x080eee7c), 0x0808d88c; NOTE: 0x0808c87e BL=0x0803abf0; 0x0808c93e BL=0x0804f6c4; 0x0808c8e4 BL=0x080eee7c
- Pool loop1: 0x0808c894=PLAYER_BLOCK_STRIDE, 0x0808c898=gDuelFieldSlots
- Pool loop2: 0x0808c918=gP1LifePoints, 0x0808c91c=PLAYER_BLOCK_STRIDE, 0x0808c920=gP1HandSlotArray, 0x0808c924=slot_field_mask_ffff803f(0xffff803f REUSE card_info.inc:1765), 0x0808c974=PLAYER_BLOCK_STRIDE(loop2 iter), 0x0808c978=gP1HandCountBase
- CID status: GILFORD_THE_LEGEND_CID(0x1938) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808c948 before BL write_equip)
- Proposed name: `scan_zone_gilford_the_legend_substate_e`
- Confidence: high (body: dual-loop gDuelFieldSlots+hand zone with field9 + slot_field_mask_ffff803f (0xffff803f) mask; Gilford the Legend equips Swords from GY; write_e = hand slot)
- ASCII plate (len=430): `Equip zone scan for Gilford the Legend (GILFORD_THE_LEGEND_CID=0x1938, pw=69933858). Two-loop: loop1 field (gDuelFieldSlots stride PLAYER_BLOCK_STRIDE) gate get_slot_card_state_code + check_slot_card_eligible_by_card_id; loop2 hand zone (gP1LifePoints+gP1HandSlotArray) gate get_card_extended_stat_field9 + slot_field_mask_ffff803f (0xffff803f) + check_slot_card_eligible_by_card_id; write substate_e. Dispatch entry [CID 0x1938].`

### fn26: 0x0808c97c  size=0x0e8 (232 B)
- CID: 0x1939 (Warrior Lady of the Wasteland), dispatch entry [CID 0x1939]
- Body: push {r4..r7,lr} + push {r8,r9,r10} + push {r5,r6,r7}; scan gP1LifePoints+gP1SlotSetCodeArray monster zone; gates: check_card_field5_is_nonzero (0x0804ad48) + get_card_extended_stat_field3_raw (0x080eef44, CMP against 0x05dc=CARD_FIELD3_THRESHOLD_1500) + get_card_extended_stat_field7 (0x080eee24) x2 + get_card_extended_stat_field6 (0x080eedf8) x2 + eval_equip_placement_full_check (0x0803bba4) + find_effect_node_in_zone (0x0802fd60, PARASITE_PARACIDE_CID=0x12a1, zone_type=0xb); write substate_d only (0xb is zone_type for find_effect_node, not a write_equip substate)
- BL targets: 0x0804ad48, 0x080eef44, 0x080eee24 (x2), 0x080eedf8 (x2), 0x0803bba4, 0x0802fd60, 0x0808d88c
- Pool: 0x0808ca4c=gP1LifePoints, 0x0808ca50=PLAYER_BLOCK_STRIDE, 0x0808ca54=gP1SlotSetCodeArray, 0x0808ca58=CARD_FIELD3_THRESHOLD_1500(0x5dc), 0x0808ca5c=PARASITE_PARACIDE_CID(0x12a1), 0x0808ca60=gP1SlotCountBase
- CID status: WARRIOR_LADY_WASTELAND_CID(0x1939) NEW
- Substate: 0xd (MOVS r1,#0xd at 0x0808ca22 before BL write_equip_zone_entry_by_substate); 0xb is zone_type arg to find_effect_node_in_zone (MOVS r1,#0xb at 0x0808ca14 -> BL find_effect_node_in_zone at 0x0808ca18), not a write_equip substate
- Proposed name: `scan_zone_warrior_lady_wasteland_substate_d`
- Confidence: high (body: SlotSetCodeArray + ATK<=1500 + field7 x2 + field6 x2 + placement + find_effect_node; Warrior Lady of the Wasteland searches a Warrior when destroyed; write_d=monster zone only)
- ASCII plate (len=402): `Equip zone scan for Warrior Lady of the Wasteland (WARRIOR_LADY_WASTELAND_CID=0x1939, pw=05438492). Monster zone via gP1LifePoints+gP1SlotSetCodeArray; gates: field5_nonzero + field3_raw<=0x5dc (ATK<=1500) + field7 x2 + field6 x2 + eval_equip_placement + find_effect_node(PARASITE_PARACIDE_CID=0x12a1); write substate_d; 0xb passed to find_effect_node_in_zone as zone type. Dispatch entry [CID 0x1939].`

### fn27: 0x0808ca64  size=0x058 (88 B)
- CID: 0x193a (Divine Sword - Phoenix Blade), dispatch entry [CID 0x193a]
- Body: push {r4..r7,lr}; inner loop scan gP1LifePoints (stride 0x14, MOVS r4,#0x83 init); gate: get_card_extended_stat_field6 (0x080eedf8, cmp r0,#0xf=Warrior type); write substate_e
- BL targets: 0x080eedf8, 0x0808d88c
- Pool: 0x0808cab4=gP1LifePoints, 0x0808cab8=PLAYER_BLOCK_STRIDE
- CID status: DIVINE_SWORD_PHOENIX_BLADE_CID(0x193a) REUSE
- Substate: 0xe (MOVS r1,#0xe at 0x0808ca9c before BL write_equip)
- Proposed name: `scan_zone_divine_sword_phoenix_blade_substate_e`
- Confidence: high (body: inner loop stride 0x14 + field6 Warrior(0xf) gate; Divine Sword - Phoenix Blade is banished from GY to equip and boost Warrior ATK+300; write_e = hand slot)
- ASCII plate (len=315): `Equip zone scan for Divine Sword - Phoenix Blade (DIVINE_SWORD_PHOENIX_BLADE_CID=0x193a, pw=31423101). Monster zone via gP1LifePoints inner loop (stride 0x14, init=0x83); gate: get_card_extended_stat_field6 == 0xf (Warrior type); write_equip_zone_entry_by_substate(player_id, 0xe, slot_idx). Dispatch table entry [CID 0x193a].`

---

## Group-Handler CID Sets

No multi-CID group handlers in Seg-4f. All 25 real functions handle exactly one CID each. The two fn07+fn08 and fn17+fn18 entries are not group handlers but alt-entry fallthrough pairs for single-CID functions (CID 0x1895 and CID 0x1900 respectively).

---

## EQ_SLOTS (CID pool equates)

### NEW CIDs to add to card_info.inc (10 entries, per-value grep = 0 hits each):

C5 grep results (confirmed 0 hits before marking NEW):
```
.equ RESCUE_CAT_CID,                 0x00001876  @ Rescue Cat (pw=14878871; card-stats.s card_1783 slot=0x1876); grep 0x1876=0 hits
.equ FULFILLMENT_CONTRACT_CID,       0x00001880  @ Fulfillment of the Contract (pw=48206762; card-stats.s card_1793 slot=0x1880); grep 0x1880=0 hits
.equ BEAST_SOUL_SWAP_CID,            0x00001889  @ Beast Soul Swap (pw=35149085; card-stats.s card_1800 slot=0x1889); grep 0x1889=0 hits
.equ HERO_SIGNAL_CID,                0x000018d4  @ Hero Signal (pw=22020907; card-stats.s card_1860 slot=0x18D4); grep 0x18d4=0 hits
.equ WROUGHTWEILER_CID,              0x000018f7  @ Wroughtweiler (pw=06480253; card-stats.s card_1881 slot=0x18F7); grep 0x18f7=0 hits
.equ POWER_BOND_CID,                 0x000018fe  @ Power Bond (pw=37630732; card-stats.s card_1887 slot=0x18FE); grep 0x18fe=0 hits
.equ SUMMON_PRIEST_CID,              0x00001900  @ Summon Priest (pw=00423585; card-stats.s card_1889 slot=0x1900); grep 0x1900=0 hits
.equ FUSION_RECOVERY_CID,            0x0000191f  @ Fusion Recovery (pw=18511384; card-stats.s card_1916 slot=0x191F); grep 0x191f=0 hits
.equ MIRACLE_FUSION_CID,             0x00001920  @ Miracle Fusion (pw=45906428; card-stats.s card_1917 slot=0x1920); grep 0x1920=0 hits
.equ WARRIOR_LADY_WASTELAND_CID,     0x00001939  @ Warrior Lady of the Wasteland (pw=05438492; card-stats.s card_1938 slot=0x1939); grep 0x1939=0 hits
```

Total NEW CIDs: **10**

### REUSE CIDs (already in card_info.inc, DO NOT add):
A_FEATHER_OF_THE_PHOENIX_CID(0x187a), CENTRIFUGAL_FIELD_CID(0x187f), RE_FUSION_CID(0x1881),
VAMPIRE_GENESIS_CID(0x1895), KING_OF_SKULL_SERVANTS_CID(0x18c5), DOUBLE_ATTACK_CID(0x18cb),
BATTERY_CHARGER_CID(0x18cc), LEVEL_CONVERSION_LAB_CID(0x18d9), ROCK_BOMBARDMENT_CID(0x18da),
BUBBLE_SHUFFLE_CID(0x1908), DRAGONS_MIRROR_CID(0x1921), SPIRITUAL_EARTH_ART_CID(0x1927),
A_RIVAL_APPEARS_CID(0x192b), GILFORD_THE_LEGEND_CID(0x1938), DIVINE_SWORD_PHOENIX_BLADE_CID(0x193a),
SKULL_SERVANT_CID(0x0fbe), PARASITE_PARACIDE_CID(0x12a1)

### Scalar pool equates (existing constants, REUSE):
- PLAYER_BLOCK_STRIDE(0x868) -- ewram.inc -- 27+ slots across segment
- CARD_FIELD3_THRESHOLD_1500(0x5dc) -- card_info.inc -- 1 slot (fn26 pool 0x0808ca58)
- EQUIP_ACTIVE_CTX_OFF(0x484) -- duel_field.inc -- 4 slots (fn06/fn07+fn08/fn10/fn24)

---

## Raw-value equate list (new .equ definition required)

These raw literal values appear in pool slots but have no existing named constant. They need a new `.equ` definition added to the appropriate constants file so GAS can resolve `.word <name>` references without link errors:

| pool addr | value | proposed equate name | file | reason |
|-----------|-------|---------------------|------|--------|
| 0x0808bf28 | 0xfffffef4 | `VAMPIRE_GENESIS_GDUELPF_NEG_OFF` | duel_field.inc or card_info.inc | Used in fn07+fn08: `LDR r0,[PC,...]=0xfffffef4; ADD r0,r8,r0` computes gDuelPhaseFlags-relative offset -0x10c; no existing name; confidence: med (structural evidence only -- negative ADD offset from gDuelPhaseFlags base; exact field semantics opaque) |

Note: fn25 pool 0x0808c924 = 0xffff803f REUSE `slot_field_mask_ffff803f` (card_info.inc:1765, established Seg-4d for scan_zone_guardian_equip_group_substate_e fn24). Do NOT add a new equate for this value.

---

## REF_SLOTS (createDWordWithRef plan)

Per Seg-4a/4b/4c/4d/4e precedent: every pool DWord holding an EWRAM address gets createDWordWithRef + RENAME.

### gP1LifePoints = 0x0201c4e0 -- 22 slots
| slot addr | fn |
|-----------|-----|
| 0x0808bc04 | fn01 |
| 0x0808bc44 | fn02 |
| 0x0808bc9c | fn03 |
| 0x0808bd6c | fn04 |
| 0x0808bde0 | fn05 |
| 0x0808bfc0 | fn07+fn08 loop2 |
| 0x0808c044 | fn09 |
| 0x0808c148 | fn11 |
| 0x0808c254 | fn12 |
| 0x0808c2f0 | fn14 |
| 0x0808c348 | fn15 |
| 0x0808c3c4 | fn16 |
| 0x0808c450 | fn17+fn18 |
| 0x0808c4f4 | fn20 |
| 0x0808c56c | fn21 pool1 |
| 0x0808c5e4 | fn21 pool2 |
| 0x0808c65c | fn22 pool1 |
| 0x0808c6d4 | fn22 pool2 |
| 0x0808c784 | fn23 |
| 0x0808c918 | fn25 loop2 |
| 0x0808ca4c | fn26 |
| 0x0808cab4 | fn27 |

REF count gP1LifePoints: **22**

### gP1SlotSetCodeArray = 0x0201c740 -- 4 slots
| slot addr | fn |
|-----------|-----|
| 0x0808bc0c | fn01 |
| 0x0808c260 | fn12 |
| 0x0808c458 | fn17+fn18 |
| 0x0808ca54 | fn26 |

REF count gP1SlotSetCodeArray: **4**

### gP1HandSlotArray = 0x0201c8f8 -- 8 slots
| slot addr | fn |
|-----------|-----|
| 0x0808bca4 | fn03 |
| 0x0808bd74 | fn04 |
| 0x0808bde8 | fn05 |
| 0x0808bf2c | fn07+fn08 loop1 |
| 0x0808bfc8 | fn07+fn08 loop2 |
| 0x0808c04c | fn09 |
| 0x0808c150 | fn11 |
| 0x0808c920 | fn25 loop2 |
| 0x0808c78c | fn23 |

REF count gP1HandSlotArray: **9**

### gP1HandCountBase = 0x0201c4f4 -- 2 slots
| slot addr | fn |
|-----------|-----|
| 0x0808bd00 | fn03 |
| 0x0808c978 | fn25 loop2 |

REF count gP1HandCountBase: **2**

### gP1FieldArrayCBase = 0x0201c600 -- 7 slots
| slot addr | fn |
|-----------|-----|
| 0x0808be60 | fn06 |
| 0x0808bf24 | fn07+fn08 loop1 |
| 0x0808c0bc | fn10 |
| 0x0808c25c | fn12 |
| 0x0808c29c | fn13 |
| 0x0808c4a4 | fn19 |
| 0x0808c7fc | fn24 |

REF count gP1FieldArrayCBase: **7**

### gDuelPhaseFlags = 0x0201b290 -- 4 slots
| slot addr | fn |
|-----------|-----|
| 0x0808be64 | fn06 |
| 0x0808bf18 | fn07+fn08 |
| 0x0808c0c0 | fn10 |
| 0x0808c800 | fn24 |

REF count gDuelPhaseFlags: **4**

### gP1ChainZoneArray = 0x0201c880 -- 3 slots
| slot addr | fn |
|-----------|-----|
| 0x0808c3cc | fn16 |
| 0x0808c574 | fn21 |
| 0x0808c664 | fn22 |

REF count gP1ChainZoneArray: **3**

### gDuelFieldSlots = 0x0201c510 -- 1 slot
| slot addr | fn |
|-----------|-----|
| 0x0808c898 | fn25 |

REF count gDuelFieldSlots: **1**

### gP1SlotCountBase = 0x0201c4f0 -- 1 slot
| slot addr | fn |
|-----------|-----|
| 0x0808ca60 | fn26 |

REF count gP1SlotCountBase: **1**

### Total REF count: 22+4+9+2+7+4+3+1+1 = **53**

---

## Literal Pool DWord List (createDWord required, all addresses in [0x0808bb7c, 0x0808cabc))

All pool addresses verified 4-byte aligned. Misaligned halfwords at 0x0808bc4a, 0x0808c14a (2B pad), 0x0808c29a, 0x0808c34a are epilogue half-words not pool entries (confirmed by byte inspection).

**fn01** (0x0808bb7c): 0x0808bc04, 0x0808bc08, 0x0808bc0c
**fn02** (0x0808bc10): 0x0808bc44, 0x0808bc48
**fn03** (0x0808bc4c): 0x0808bc9c, 0x0808bca0, 0x0808bca4, 0x0808bcfc, 0x0808bd00
**fn04** (0x0808bd04): 0x0808bd6c, 0x0808bd70, 0x0808bd74
**fn05** (0x0808bd78): 0x0808bde0, 0x0808bde4, 0x0808bde8
**fn06** (0x0808bdec): 0x0808be5c, 0x0808be60, 0x0808be64, 0x0808be68
**fn07+fn08** (0x0808be6c): 0x0808bf18, 0x0808bf1c, 0x0808bf20, 0x0808bf24, 0x0808bf28, 0x0808bf2c, 0x0808bfc0, 0x0808bfc4, 0x0808bfc8
**fn09** (0x0808bfcc): 0x0808c044, 0x0808c048, 0x0808c04c, 0x0808c050, 0x0808c054
**fn10** (0x0808c058): 0x0808c0b8, 0x0808c0bc, 0x0808c0c0, 0x0808c0c4
**fn11** (0x0808c0c8): 0x0808c148, 0x0808c14c, 0x0808c150
**fn12** (0x0808c154): 0x0808c254, 0x0808c258, 0x0808c25c, 0x0808c260
**fn13** (0x0808c264): 0x0808c298, 0x0808c29c
**fn14** (0x0808c2a0): 0x0808c2f0, 0x0808c2f4
**fn15** (0x0808c2f8): 0x0808c348, 0x0808c34c
**fn16** (0x0808c350): 0x0808c3c4, 0x0808c3c8, 0x0808c3cc
**fn17+fn18** (0x0808c3d0): 0x0808c450, 0x0808c454, 0x0808c458
**fn19** (0x0808c45c): 0x0808c4a4
**fn20** (0x0808c4a8): 0x0808c4f4, 0x0808c4f8
**fn21** (0x0808c4fc): 0x0808c56c, 0x0808c570, 0x0808c574, 0x0808c5e4, 0x0808c5e8
**fn22** (0x0808c5ec): 0x0808c65c, 0x0808c660, 0x0808c664, 0x0808c6d4, 0x0808c6d8
**fn23** (0x0808c6dc): 0x0808c784, 0x0808c788, 0x0808c78c
**fn24** (0x0808c790): 0x0808c7f8, 0x0808c7fc, 0x0808c800, 0x0808c804
**fn25** (0x0808c808): 0x0808c894, 0x0808c898, 0x0808c918, 0x0808c91c, 0x0808c920, 0x0808c924, 0x0808c974, 0x0808c978
**fn26** (0x0808c97c): 0x0808ca4c, 0x0808ca50, 0x0808ca54, 0x0808ca58, 0x0808ca5c, 0x0808ca60
**fn27** (0x0808ca64): 0x0808cab4, 0x0808cab8

Total pool DWORDs: **93** (all 4-byte aligned, verified by Python; fn21 and fn22 each have 2 additional pool entries vs original proposal)

---

## Disasm Plan (R4)

All 25 real functions are THUMB code. No ROM_INCBIN or .byte blocks remain in this segment -- all bytes are function bodies and literal pools.

Per-function disassembly (25 real functions, 27 strong entries = 25 disasm + 2 degenerate exclusions):

| entry addr | real fn start | end | size | note |
|-----------|--------------|-----|------|------|
| 0x0808bb7c | fn01 | 0x0808bc10 | 0x94 | none |
| 0x0808bc10 | fn02 | 0x0808bc4c | 0x3c | none |
| 0x0808bc4c | fn03 | 0x0808bd04 | 0xb8 | none |
| 0x0808bd04 | fn04 | 0x0808bd78 | 0x74 | none |
| 0x0808bd78 | fn05 | 0x0808bdec | 0x74 | none |
| 0x0808bdec | fn06 | 0x0808be6c | 0x80 | none |
| 0x0808be6c | fn07+fn08 | 0x0808bfcc | 0x160 | exclude 0x0808be88 from entry list; exclude 0x0808bf4a (weak) |
| 0x0808bfcc | fn09 | 0x0808c058 | 0x8c | none |
| 0x0808c058 | fn10 | 0x0808c0c8 | 0x70 | none |
| 0x0808c0c8 | fn11 | 0x0808c154 | 0x8c | none |
| 0x0808c154 | fn12 | 0x0808c264 | 0x110 | none |
| 0x0808c264 | fn13 | 0x0808c2a0 | 0x3c | none |
| 0x0808c2a0 | fn14 | 0x0808c2f8 | 0x58 | none |
| 0x0808c2f8 | fn15 | 0x0808c350 | 0x58 | none |
| 0x0808c350 | fn16 | 0x0808c3d0 | 0x80 | none |
| 0x0808c3d0 | fn17+fn18 | 0x0808c45c | 0x8c | exclude 0x0808c3da from entry list |
| 0x0808c45c | fn19 | 0x0808c4a8 | 0x4c | none |
| 0x0808c4a8 | fn20 | 0x0808c4fc | 0x54 | none |
| 0x0808c4fc | fn21 | 0x0808c5ec | 0xf0 | none |
| 0x0808c5ec | fn22 | 0x0808c6dc | 0xf0 | none |
| 0x0808c6dc | fn23 | 0x0808c790 | 0xb4 | none |
| 0x0808c790 | fn24 | 0x0808c808 | 0x78 | none |
| 0x0808c808 | fn25 | 0x0808c97c | 0x174 | none |
| 0x0808c97c | fn26 | 0x0808ca64 | 0xe8 | none |
| 0x0808ca64 | fn27 | 0x0808cabc | 0x58 | none |

Size sum verified: 0x94+0x3c+0xb8+0x74+0x74+0x80+0x160+0x8c+0x70+0x8c+0x110+0x3c+0x58+0x58+0x80+0x8c+0x4c+0x54+0xf0+0xf0+0xb4+0x78+0x174+0xe8+0x58 = 0xF40. Confirmed.

---

## carve 计划 (R7)

No ROM_INCBIN data blocks requiring carve in this segment. All bytes are THUMB code + literal pools belonging to the 25 real functions. No data tables, incbin regions, or pointer tables exist in this range.

---

## §5.1 登记 (Rule 3) -- 0 引用块

No ROM_INCBIN or .byte blocks in Seg-4f. All code; no orphan data regions.

---

## 消费者证据 (R6) -- 关键槽语义 file:line + 置信度

- `write_equip_zone_entry_by_substate` (0x0808d88c): all 25 fns; established Seg-4a/4b/4c/4d/4e; high confidence
- `check_card_field5_is_nonzero` (0x0804ad48): doc/dev/naming-proposals.csv line (0x0804ad48); high confidence
- `get_card_extended_stat_field6` (0x080eedf8): doc/dev/naming-proposals.csv; high confidence
- `get_card_extended_stat_field5` (0x080eee50): doc/dev/naming-proposals.csv; high confidence
- `get_card_extended_stat_field7` (0x080eee24): doc/dev/naming-proposals.csv; high confidence
- `get_card_extended_stat_field9` (0x080eee7c): doc/dev/naming-proposals.csv; high confidence
- `get_card_extended_stat_field3_raw` (0x080eef44): doc/dev/naming-proposals.csv; high confidence
- `check_card_type_is_trap` (0x0804addc): doc/dev/naming-proposals.csv; high confidence
- `check_card_type_is_spell` (0x0804adc8): doc/dev/naming-proposals.csv; high confidence
- `check_card_id_is_normal_summon_type` (0x0804b164): doc/dev/naming-proposals.csv; high confidence
- `check_card_is_batteryman_type` (0x0804b250): doc/dev/naming-proposals.csv; high confidence
- `eval_equip_bonus_for_slot` (0x080377b0): doc/dev/naming-proposals.csv:699; high confidence
- `eval_equip_placement_full_check` (0x0803bba4): doc/dev/naming-proposals.csv; high confidence
- `check_zone_slot_equip_eligible` (0x08037434): doc/dev/naming-proposals.csv; high confidence
- `check_card_pair_allowed` (0x0804ab4c): doc/dev/naming-proposals.csv; high confidence
- `build_equip_slot_criteria_from_card_range` (0x0807fb9c): doc/dev/naming-proposals.csv; high confidence
- `get_equip_display_type_code_by_card_id` (0x0807f6f0): doc/dev/naming-proposals.csv:2464; high confidence
- `get_equip_display_criteria_code_by_card_and_slot` (0x0807f730): doc/dev/naming-proposals.csv:2465; high confidence
- `check_spell_zone_slot_placeable` (0x0803bc24): doc/dev/naming-proposals.csv; high confidence
- `check_equip_slot_eligible_with_criteria_and_prerequisites` (0x08080348): doc/dev/naming-proposals.csv; high confidence
- `get_slot_card_state_code` (0x0803abf0): doc/dev/naming-proposals.csv; high confidence
- `check_slot_card_eligible_by_card_id` (0x0804f6c4): doc/dev/naming-proposals.csv; high confidence
- `count_effect_node_activations_by_zone` (0x080907f4): doc/dev/naming-proposals.csv; high confidence
- `find_effect_node_in_zone` (0x0802fd60): doc/dev/naming-proposals.csv:508; high confidence
- `memset` (0x0810e9bc): doc/dev/naming-proposals.csv; high confidence
- `check_card_stat_field7_equals` (0x08030b70): doc/dev/naming-proposals.csv; high confidence
- `gDuelPhaseFlags` (0x0201b290): constants/ewram.inc:353; high confidence
- `EQUIP_ACTIVE_CTX_OFF` (0x0000484): constants/duel_field.inc:364; high confidence
- `gP1ChainZoneArray` (0x0201c880): constants/ewram.inc; high confidence
- `gDuelFieldSlots` (0x0201c510): constants/ewram.inc:314; high confidence
- `gP1HandCountBase` (0x0201c4f4): constants/ewram.inc:333; high confidence
- `SKULL_SERVANT_CID` (0x0fbe): constants/card_info.inc:309; high confidence
- `KING_OF_SKULL_SERVANTS_CID` (0x18c5): constants/card_info.inc:361; high confidence
- `CARD_FIELD3_THRESHOLD_1500` (0x5dc): constants/card_info.inc (Seg-4e precedent); high confidence
- `PARASITE_PARACIDE_CID` (0x12a1): constants/card_info.inc; high confidence

---

## 求助 (低置信度语义)

1. fn07+fn08 pool 0x0808bf28 = 0xfffffef4: Used as `LDR r0; ADD r0,r8,r0` where r8=value loaded from gDuelPhaseFlags. Value 0xfffffef4 = -0x10c signed. This is a negative offset from the gDuelPhaseFlags base. The exact field at gDuelPhaseFlags-0x10c is not identified. Confidence: med (structural: negative ADD offset from gDuelPhaseFlags used to index into a field; no callee function named). Action: label as raw EQ `VAMPIRE_GENESIS_GDUELPF_NEG_OFF` with ASCII EOL `@ gDuelPhaseFlags relative negative offset -0x10c`.

2. fn25 pool 0x0808c924 = 0xffff803f: REUSE `slot_field_mask_ffff803f` (card_info.inc:1765, established Seg-4d). Same value already defined; no new equate required. Used as `AND r2,r0` on a halfword from gP1HandSlotArray (clears bits 8-14).
