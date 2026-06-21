# Refine Proposal: F10-Seg-6  [0x0807f730..0x08080ba0)

## Segment Survey

**Functions (18):**
| Addr       | Name                                                            |
|------------|-----------------------------------------------------------------|
| 0x0807f730 | get_equip_display_criteria_code_by_card_and_slot                |
| 0x0807f7bc | fill_equip_criteria_display_code_array                          |
| 0x0807f800 | check_equip_slot_criteria_by_ext_field6_any                     |
| 0x0807f848 | check_equip_slot_criteria_by_state_code_any                     |
| 0x0807f89c | clear_equip_slot_criteria_on_ext_field6_match                   |
| 0x0807f8f0 | find_first_equip_slot_criteria_by_state_code                    |
| 0x0807f974 | check_equip_slot_eligible_with_criteria_and_target              |
| 0x0807fad8 | check_equip_slot_eligible_by_node_player                        |
| 0x0807fb14 | find_equip_eligible_slot_entry_for_player                       |
| 0x0807fb9c | build_equip_slot_criteria_from_card_range                       |
| 0x0807fcc0 | build_equip_set_f_criteria_state                                |
| 0x0807fd84 | activate_field_spell_neo_daedalus_group_if_placeable            |
| 0x0807fde8 | dispatch_equip_criteria_display_by_type_code  (switchD_0807fe22)|
| 0x08080348 | check_equip_slot_eligible_with_criteria_and_prerequisites       |
| 0x080804c8 | build_equip_eligibility_state_for_category3_card               |
| 0x08080690 | tick_equip_slot_sprite_display_6state  (switchD_080806cc)       |
| 0x08080944 | build_equip_criteria_for_target_slots                           |
| 0x08080b74 | push_to_effect_slot_array                                       |

**Residual auto-name slots: 123**
- DAT_  slots: 110
- DWORD_ slots: 13  (at 0x08080a78..0x08080a94 and 0x08080b44..0x08080b54)
- PTR_gP1LifePoints_ slots (already symbolized, not counted): 6

**ROM_INCBIN in range: 0**

**switchD blocks: 2**
- switchD_0807fe22 (inside dispatch_equip_criteria_display_by_type_code): already decoded as .word table; DAT_0807fe28 holds pointer 0x0807fe2c (ROM-verified). No R4 action needed.
- switchD_080806cc (inside tick_equip_slot_sprite_display_6state): already decoded as .word table; DAT_080806d4 holds pointer 0x080806d8 (ROM-verified). No R4 action needed.
- Note: `.hword 0x4687` appearing in related code is MOV PC,r0 (THUMB opcode), not switch data.

---

## Data Block Classification (Rule 2/3)

No ROM_INCBIN or .byte blocks exist in [0x0807f730, 0x08080ba0). Section N/A.

---

## Symbolization Plan

### Slot Value Inventory (C13 basis)

Python scan (asm/10_equip_effect_dispatch.s, range [0x0807f730, 0x08080ba0)) confirmed:
- 123 total auto-name slots (110 DAT_ + 13 DWORD_)
- Classified: EQ=66 instances + REF=57 instances = 123  (zero unclassified)

---

### EQ_SLOTS  (data-equate)

**24 unique constant values; 15 REUSE + 9 NEW**

**REUSE (grep by VALUE confirms existing equate):**

| Value      | Equate Name               | Inc File         | Instance Count | Evidence |
|------------|---------------------------|------------------|----------------|----------|
| 0x00000484 | EQUIP_ACTIVE_CTX_OFF      | duel_field.inc   | x2             | asm/10 L12494, L13655 |
| 0x00000868 | PLAYER_BLOCK_STRIDE       | ewram.inc        | x13            | asm/10 L12346 etc. |
| 0x000012e5 | POLYMERIZATION_CID        | card_info.inc    | x2             | asm/10 L13313, L13454 |
| 0x0000149c | FUSION_GATE_CID           | card_info.inc    | x2             | asm/10 L13317, L13458 |
| 0x0000157e | FGD_CID                   | card_info.inc    | x2             | asm/10 L11943, L14175 |
| 0x000018a6 | EHERO_AVIAN_CID           | card_info.inc    | x1             | asm/10 L11967 |
| 0x000018a7 | EHERO_BURSTINATRIX_CID    | card_info.inc    | x1             | asm/10 L11972 |
| 0x000018a8 | EHERO_CLAYMAN_CID         | card_info.inc    | x1             | asm/10 L11977 |
| 0x000018f9 | EHERO_BUBBLEMAN_CID       | card_info.inc    | x1             | asm/10 L11982 |
| 0x000018fb | UFOROID_FIGHTER_CID       | card_info.inc    | x3             | asm/10 L13362, L13409, L13499 |
| 0x000019ef | EHERO_ERIKSHIELER_CID     | card_info.inc    | x1             | asm/10 L11945 |
| 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF    | ewram.inc        | x1             | asm/10 L13138 |
| 0x00001d6c | ELIGIB_ANIM_STATE_OFF     | ewram.inc        | x1             | asm/10 L13140 |
| 0x00001d70 | LP_BANISHER_CTX_OFF       | ewram.inc        | x1             | asm/10 L13142 |
| 0x00001d78 | ACTIVATION_STATE_B_OFF    | duel_field.inc   | x1             | asm/10 L12895 |

**NEW (grep by value = 0 hits in all constants/*.inc):**

| Value      | Proposed Name                      | Inc File         | Count | Semantic Evidence |
|------------|------------------------------------|------------------|-------|-------------------|
| 0x0000059c | EQUIP_ZONE_ATTR_COMPOSITE_OFF      | duel_field.inc   | x4    | asm/10 L13060: loads base+0x59c before calling zone-entry checks; field holds composite zone+player attr; conf: high |
| 0x000005a4 | EQUIP_CRITERIA_TARGETED_FLAG_OFF   | duel_field.inc   | x11   | asm/10 L12457: [gDuelPhaseFlags+0x5a4] written as targeted-card flag in equip eligibility logic; conf: high |
| 0x000005ac | EQUIP_CRITERIA_DISPLAY_ARR_OFF     | duel_field.inc   | x9    | asm/10 L12057-12065: fill_equip_criteria_display_code_array writes criteria codes to [gDuelPhaseFlags+0x5ac+i*4]; same offset at L12251, L12971; conf: high |
| 0x00001921 | DRAGONS_MIRROR_CID                 | card_info.inc    | x1    | card-stats.s card_1918: pw=71490127, name Dragons Mirror; asm/10 L13460; conf: high |
| 0x0000197a | NON_FUSION_AREA_CID                | card_info.inc    | x2    | card-stats.s card_1991: pw=27581098, name Non-Fusion Area; asm/10 L12889, L14515; conf: high |
| 0x0000804a | OAM_EQUIP_ZONE_SPRITE_P2_4A        | oam_attr.inc     | x1    | asm/10 L13308: passed to enqueue_equip_zone_sprite_direct as P2 sprite attr0 (bit15=1, grp 0x4a); sibling of OAM_EQUIP_ZONE_SPRITE_P1=0x8033; 96 raw ROM refs; conf: high |
| 0x0000804b | OAM_EQUIP_ZONE_SPRITE_P2_4B        | oam_attr.inc     | x3    | asm/10 L13316, L13404, L13456: P2 equip zone sprite variant 0x4b; 38 raw ROM refs; conf: high |
| 0x0000804c | OAM_EQUIP_ZONE_SPRITE_P2_4C        | oam_attr.inc     | x1    | asm/10 L13558: P2 equip zone sprite variant 0x4c; 7 raw ROM refs; conf: high |
| 0xfffffa54 | EQUIP_CRITERIA_ARR_NEG_OFF         | duel_field.inc   | x1    | asm/10 L12235-12236: ldr r0,DAT_0807f950 (=0xfffffa54); adds r1,r4,r0 where r4=gDuelPhaseFlags+0x5ac; result r1=gDuelPhaseFlags (base recovered by negating +0x5ac); verified: 0xfffffa54 = -0x5ac mod 2^32; conf: high |

---

### REF_SLOTS  (USER-label + DATA-ref)

**15 unique address values; all REUSE existing labels (except 3 NEW abs-addr labels for IWRAM fields):**

| Value      | Label / Action                              | Count | Evidence |
|------------|---------------------------------------------|-------|----------|
| 0x0201b290 | gDuelPhaseFlags (REUSE, ewram.inc)          | x31   | asm/10 L12057 etc.; dominant global in segment |
| 0x0201b830 | NEW abs label: gDuelPhaseFlags_criteria_count | x2  | gDuelPhaseFlags+0x5a0; asm/10 L14001, L14623: [0x201b830] = criteria count for effect-slot push loop; ewram.inc add |
| 0x0201b838 | NEW abs label: gDuelPhaseFlags_set_f_flag   | x3    | gDuelPhaseFlags+0x5a8; asm/10 L13995, L14527, L14619: read/written as set-f category presence flag; ewram.inc add |
| 0x0201b850 | NEW abs label: gDuelPhaseFlags_criteria_arr_base | x1 | gDuelPhaseFlags+0x5c0; asm/10 L12690: base addr of criteria array block; ewram.inc add |
| 0x0201c4e0 | gP1LifePoints (REUSE, ewram.inc)            | x1    | asm/10 L14525 (DWORD_08080a90 already symbolized) |
| 0x0201c4f4 | gP1HandCountBase (REUSE, ewram.inc)         | x1    | asm/10 L14003 |
| 0x0201c510 | gDuelFieldSlots (REUSE, ewram.inc)          | x4    | asm/10 L12348, L12574, L13651, L13993 |
| 0x0201c520 | gDuelFieldSlotState (REUSE, ewram.inc)      | x1    | asm/10 L14617 (DWORD_08080b48) |
| 0x0201c600 | gP1FieldArrayCBase (REUSE, ewram.inc)       | x3    | asm/10 L12400, L13321, L13358 |
| 0x0201c880 | gP1ChainZoneArray (REUSE, ewram.inc)        | x2    | asm/10 L13563, L14521 |
| 0x0201c8f8 | gP1HandSlotArray (REUSE, ewram.inc)         | x3    | asm/10 L13407, L13705, L13999 |
| 0x0201e2a0 | gDuelCardCtxBase (REUSE, ewram.inc)         | x2    | asm/10 L12891, L13064 |
| 0x0807fad9 | check_equip_slot_eligible_by_node_player+1  | x1    | asm/10 L13082: DAT_0807ff88; THUMB fn-ptr (addr+1); fn @ 0x0807fad8; ROM-verified: 0x0807fad9 |
| 0x0807fe2c | switchD_0807fe22__switchdataD_0807fe2c      | x1    | asm/10 L12940: DAT_0807fe28; switchD table ptr; ROM-verified |
| 0x080806d8 | switchD_080806cc__switchdataD_080806d8      | x1    | asm/10 L14055: DAT_080806d4; switchD table ptr; ROM-verified |

---

### RENAME_SLOTS  (DWORD_ label rename + EQ/REF value symbolization)

All 13 DWORD_ slots are in two adjacent literal pools. Fixer action: replace raw .word value with symbolic name AND rename the DWORD_ label.

**build_equip_criteria_for_target_slots literal pool (0x08080a78..0x08080a94):**

| Slot addr  | Raw value  | Kind | Symbolic value                       | New label                                  |
|------------|------------|------|--------------------------------------|--------------------------------------------|
| 0x08080a78 | 0x0201b290 | REF  | gDuelPhaseFlags                      | build_equip_criteria_gdf_base_a78          |
| 0x08080a7c | 0x0000197a | EQ   | NON_FUSION_AREA_CID                  | build_equip_criteria_nfa_cid_a7c           |
| 0x08080a80 | 0x0000059c | EQ   | EQUIP_ZONE_ATTR_COMPOSITE_OFF        | build_equip_criteria_zone_attr_off_a80     |
| 0x08080a84 | 0x00000868 | EQ   | PLAYER_BLOCK_STRIDE                  | build_equip_criteria_stride_a84            |
| 0x08080a88 | 0x0201c880 | REF  | gP1ChainZoneArray                    | build_equip_criteria_chain_zone_arr_a88    |
| 0x08080a8c | 0x000005a4 | EQ   | EQUIP_CRITERIA_TARGETED_FLAG_OFF     | build_equip_criteria_targeted_off_a8c      |
| 0x08080a90 | 0x0201c4e0 | REF  | gP1LifePoints                        | PTR_gP1LifePoints_08080a90 (REAL RENAME: current label is DWORD_08080a90; fixer must renameData it) |
| 0x08080a94 | 0x0201b838 | REF  | gDuelPhaseFlags_set_f_flag           | build_equip_criteria_set_f_flag_a94        |

**push_to_effect_slot_array literal pool (0x08080b44..0x08080b54):**

| Slot addr  | Raw value  | Kind | Symbolic value                       | New label                                  |
|------------|------------|------|--------------------------------------|--------------------------------------------|
| 0x08080b44 | 0x00000868 | EQ   | PLAYER_BLOCK_STRIDE                  | push_effect_slot_stride_b44                |
| 0x08080b48 | 0x0201c520 | REF  | gDuelFieldSlotState                  | push_effect_slot_dfs_state_b48             |
| 0x08080b4c | 0x0201b838 | REF  | gDuelPhaseFlags_set_f_flag           | push_effect_slot_set_f_flag_b4c            |
| 0x08080b50 | 0x0201b290 | REF  | gDuelPhaseFlags                      | push_effect_slot_gdf_base_b50              |
| 0x08080b54 | 0x0201b830 | REF  | gDuelPhaseFlags_criteria_count       | push_effect_slot_criteria_cnt_b54          |

---

### PLATE  (R5; mojibake rewrite + C8 stale FUN_ fixes)

**Mojibake plates (11 corrupted lines across 6 functions -- Jython double-UTF-8):**

All non-ASCII bytes confirmed by grep `[^\x00-\x7F]` on asm/10 lines 12017, 12018, 12274, 12277-12279, 12587, 12904, 13566, 13570, 14361.

| Fn addr    | Fn name                                                         | Lines  | Action |
|------------|-----------------------------------------------------------------|--------|--------|
| 0x0807f730 | get_equip_display_criteria_code_by_card_and_slot                | L12017-12018 | Full ASCII rewrite (2 lines) |
| 0x0807f8f0 | find_first_equip_slot_criteria_by_state_code                    | L12274, 12277-12279 | Full ASCII rewrite (4 lines) |
| 0x0807fb14 | find_equip_eligible_slot_entry_for_player                       | L12587 | Full ASCII rewrite (1 line) |
| 0x0807fd84 | activate_field_spell_neo_daedalus_group_if_placeable            | L12904 | Full ASCII rewrite (1 line) |
| 0x08080348 | check_equip_slot_eligible_with_criteria_and_prerequisites       | L13566, L13570 | Full ASCII rewrite (2 lines) |
| 0x08080944 | build_equip_criteria_for_target_slots                           | L14361 | Full ASCII rewrite (1 line) |

**Proposed ASCII plate text (replace full lines):**

```
L12017: @ get_equip_display_criteria_code_by_card_and_slot: returns u16 criteria_code for (card_id, slot_idx). FGD_CID(0x157e)->1; EHERO_ERIKSHIELER(0x19ef)->slot0=AVIAN,slot1=BURSTINATRIX,slot2=CLAYMAN,slot3=BUBBLEMAN; other->find_equip_display_entry_by_card_id->slot0=+2,1=+4,2=+6; slot>=3->0.
L12018: @ Called by fill_equip_criteria_display_code_array to write criteria_code to [gDuelPhaseFlags+EQUIP_CRITERIA_DISPLAY_ARR_OFF+idx*4]. No side effects. Void return (bx r1, Sub-case E via pop{r1}).

L12274: @ check_equip_slot_eligible_with_criteria_and_target: equip eligibility composite check. Args: effect_node_ptr(r0), player_id(r1), slot_idx(r2). slot_idx<=4 path: check_equip_slot_criteria_by_state_code_any, check_card_id_is_equip_set_e, get_first_placeable_monster_slot, check_slot_placement_blocked_by_field_effect. slot_idx==0xb: find_paired_zone_entry_for_card. Returns 0=ineligible, 1=eligible. Direct callers: 0x0807fad8, 0x0807fb14.
L12277: @ Constants: SLOT_IDX_MAX=4 (standard zone upper bound)
L12278: @ ZONE_IDX_PAIR=0xb (paired zone index)
L12279: @ ATTR_MASK=0xfffc7fff (AND mask clearing bits[14:15])

L12587: @ find_equip_eligible_slot_entry_for_player: iterates equip eligibility state array and calls check_equip_slot_eligible_with_criteria_and_target per entry; returns first matching slot entry ptr or NULL. indeg=2.

L12904: @ activate_field_spell_neo_daedalus_group_if_placeable: field-spell activation entry point. Called by dispatch_equip_criteria_display_by_type_code switchD caseD_80 (case index 0x80-0x63=0x1d). Checks Neo Daedalus group placeable and triggers field-spell effect.

L13566: @ check_equip_slot_eligible_with_criteria_and_prerequisites: equip slot eligibility composite check; near-symmetric sibling of check_equip_slot_eligible_with_criteria_and_target. Args: effect_node_ptr(r0), player_id(r1), slot_idx(r2). slot_idx<=4: check_equip_slot_criteria_by_state_code_any + check_card_id_is_equip_set_e + get_first_placeable_monster_slot + check_slot_placement_blocked_by_field_effect + check_zone_slot_equip_prerequisites. slot_idx==0xe: extended path. Returns 0/1.
L13570: @ ZONE_IDX_EXT=0xe (extended zone index)

L14361: @ build_equip_criteria_for_target_slots: builds equip target candidate slots. indeg=0, fn-ptr table driven (THUMB+1 ref @ DAT_0807ff88). Extracts effective_player=player_id XOR team_flag; checks [gDuelPhaseFlags+0x4a0*8]==0x80; prereqs: Neo Daedalus placeable + no field duplicate + chain zone slot exists. Writes card_id/zone_attr/display_type to gDuelPhaseFlags+0x598..0x5a8; calls fill_equip_criteria_display_code_array. Loops: per effect_slot validates zone_entry+criteria match, calls push_to_effect_slot_array. Returns 0x64 if count>0 or blocked_flag==1, else 0.
```

**C8 stale FUN_ fixes (plate/EOL updates):**

| Stale ref              | Current name                                                    | File / Line   |
|------------------------|-----------------------------------------------------------------|---------------|
| FUN_0807f7bc           | fill_equip_criteria_display_code_array                          | asm/10 L11931 (plate) |
| FUN_0807f974           | check_equip_slot_eligible_with_criteria_and_target              | asm/10 L12062 (plate) |
| FUN_08080348           | check_equip_slot_eligible_with_criteria_and_prerequisites       | asm/10 L12062 (plate) |
| FUN_0807fde8           | dispatch_equip_criteria_display_by_type_code                    | asm/10 L12847 (plate); asm/11 L7484 (plate) |
| FUN_08080944           | build_equip_criteria_for_target_slots                           | asm/10 L12904 (plate) |
| FUN_08081ce8           | tick_equip_effect_slot_display_state                            | asm/10 L14644 (plate of push_to_effect_slot_array, 0x08080b74, in-seg) |

---

## Carve Plan (R7)

None. Zero ROM_INCBIN in [0x0807f730, 0x08080ba0).

---

## Disasm Plan (R4)

None. Both switchD blocks are already decoded as .word jump tables. The `.hword 0x4687` instances in this segment are MOV PC,r0 THUMB opcode (not switch data). No bare-THUMB blocks requiring R4 disassembly.

---

## New Constants / Globals

**card_info.inc** (2 new CID equates):
```
.equ NON_FUSION_AREA_CID,    0x0000197a  @ Non-Fusion Area (card 1991, pw=27581098); dispatch_equip_criteria_display_by_type_code caseD + build_equip_criteria_for_target_slots; x2 slots
.equ DRAGONS_MIRROR_CID,     0x00001921  @ Dragon's Mirror (card 1918, pw=71490127); build_equip_set_f_criteria_state branch; x1 slot
```

**duel_field.inc** (4 new offset equates):
```
.equ EQUIP_CRITERIA_DISPLAY_ARR_OFF,   0x000005ac  @ gDuelPhaseFlags+0x5ac: criteria display code array base; fill_equip_criteria_display_code_array writes [base+i*4]; x9 slots
.equ EQUIP_CRITERIA_TARGETED_FLAG_OFF, 0x000005a4  @ gDuelPhaseFlags+0x5a4: targeted-card criteria flag; check_equip_slot_eligible_with_criteria_and_target; x11 slots
.equ EQUIP_ZONE_ATTR_COMPOSITE_OFF,    0x0000059c  @ gDuelPhaseFlags+0x59c: composite zone+player attribute field; x4 slots
.equ EQUIP_CRITERIA_ARR_NEG_OFF,       0xfffffa54  @ negated EQUIP_CRITERIA_DISPLAY_ARR_OFF (-0x5ac); used to recover gDuelPhaseFlags base from array ptr in find_first_equip_slot_criteria_by_state_code; x1 slot
```

**oam_attr.inc** (3 new P2 equip zone sprite attr0 equates):
```
.equ OAM_EQUIP_ZONE_SPRITE_P2_4A, 0x0000804a  @ P2 equip zone sprite OAM attr0 variant 0x4a (bit15+0x4a); build_equip_eligibility_state_for_category3_card; sibling of OAM_EQUIP_ZONE_SPRITE_P1=0x8033; 96 raw ROM refs; x1 slot
.equ OAM_EQUIP_ZONE_SPRITE_P2_4B, 0x0000804b  @ P2 equip zone sprite OAM attr0 variant 0x4b (bit15+0x4b); build_equip_eligibility_state_for_category3_card + check_equip_slot_eligible_with_criteria_and_prerequisites; 38 raw ROM refs; x3 slots
.equ OAM_EQUIP_ZONE_SPRITE_P2_4C, 0x0000804c  @ P2 equip zone sprite OAM attr0 variant 0x4c (bit15+0x4c); check_equip_slot_eligible_with_criteria_and_prerequisites; 7 raw ROM refs; x1 slot
```

**ewram.inc** (3 new absolute IWRAM field labels):
```
gDuelPhaseFlags_criteria_count = 0x0201b830  @ gDuelPhaseFlags+0x5a0: equip criteria count for display loop; push_to_effect_slot_array + build_equip_criteria_for_target_slots; x2 slots
gDuelPhaseFlags_set_f_flag     = 0x0201b838  @ gDuelPhaseFlags+0x5a8: set-f category flag for equip criteria; build_equip_criteria_for_target_slots + push_to_effect_slot_array; x3 slots
gDuelPhaseFlags_criteria_arr_base = 0x0201b850  @ gDuelPhaseFlags+0x5c0: base addr of equip criteria array block; build_equip_slot_criteria_from_card_range; x1 slot
```

---

## Section 5.1 Registration (Rule 3) -- Zero-ref blocks

None. Segment contains 0 ROM_INCBIN / .byte blocks. All 123 slots are literal-pool entries in named functions.

---

## Consumer Evidence (R6) -- Key slot semantics

| Slot / Value | Consumer | file:line | Confidence |
|---|---|---|---|
| 0x000005ac EQUIP_CRITERIA_DISPLAY_ARR_OFF | fill_equip_criteria_display_code_array: str r0,[base+5ac+i*4] | asm/10 L12057-12065 | high |
| 0x000005a4 EQUIP_CRITERIA_TARGETED_FLAG_OFF | check_equip_slot_eligible_with_criteria_and_target: loads [gDuelPhaseFlags+5a4] as targeted flag | asm/10 L12457 | high |
| 0x0000059c EQUIP_ZONE_ATTR_COMPOSITE_OFF | build_equip_criteria_for_target_slots: ldr r3,[base+59c] before zone-attr check | asm/10 L14080 (DAT_08080a80 ref) | high |
| 0xfffffa54 EQUIP_CRITERIA_ARR_NEG_OFF | find_first_equip_slot_criteria_by_state_code: adds r1,r4,r0 (r4=base+5ac, r0=-5ac) -> r1=base | asm/10 L12235-12236 | high |
| 0x0201b830 gDuelPhaseFlags_criteria_count | push_to_effect_slot_array: ldr rN,[0x201b830] as loop count | asm/10 L14623 (DWORD_08080b54) | high |
| 0x0201b838 gDuelPhaseFlags_set_f_flag | build_equip_set_f_criteria_state writes flag; push_to_effect_slot_array reads it | asm/10 L13995 write, L14619 read | high |
| 0x0201b850 gDuelPhaseFlags_criteria_arr_base | build_equip_slot_criteria_from_card_range: ldr rN,[0x201b850] | asm/10 L12690 | high |
| 0x0000197a NON_FUSION_AREA_CID | dispatch_equip_criteria_display_by_type_code: cmp r0,NON_FUSION_AREA_CID; card-stats.s card_1991 pw=27581098 | asm/10 L12889 | high |
| 0x00001921 DRAGONS_MIRROR_CID | build_equip_set_f_criteria_state: cmp against DRAGONS_MIRROR_CID; card-stats.s card_1918 pw=71490127 | asm/10 L13460 | high |
| 0x0807fad9 THUMB fn-ptr | build_equip_eligibility_state_for_category3_card: .word check_equip_slot_eligible_by_node_player+1 | asm/10 L13082; ROM 0x0807ff88=0x0807fad9 verified | high |

---

## C13 Coverage Proof

Independent Python count (addr range scan of asm/10 lines in [0x0807f730, 0x08080ba0)):

```
Total DAT_ + DWORD_ slots in range: 123
EQ slot instances (24 unique constant values): 66
REF slot instances (15 unique address values): 57
EQ + REF = 123
ROM_INCBIN blocks: 0
section-5.1 blocks: 0
disasm ranges: 0
carve ranges: 0
Unclassified: 0
```

All 123 residual auto-name slots are classified. No double-count. Coverage = 100%.

---

## Executor Report: F10-Seg-6

- Slots: EQ=66 (24 unique values, 15 REUSE + 9 NEW) REF=57 (15 unique addrs, 12 REUSE + 3 NEW abs labels) RENAME=13 (DWORD_ literal-pool relabeling; values already counted in EQ/REF) FUNC_RENAME=0 PLATE=11 lines in 6 functions
- carve=0 disasm=0 (switchD already decoded) section5.1=0
- New constants/globals: card_info.inc +2 (NON_FUSION_AREA_CID, DRAGONS_MIRROR_CID); duel_field.inc +4 (EQUIP_CRITERIA_DISPLAY_ARR_OFF, EQUIP_CRITERIA_TARGETED_FLAG_OFF, EQUIP_ZONE_ATTR_COMPOSITE_OFF, EQUIP_CRITERIA_ARR_NEG_OFF); oam_attr.inc +3 (OAM_EQUIP_ZONE_SPRITE_P2_4A/4B/4C); ewram.inc +3 (gDuelPhaseFlags_criteria_count, gDuelPhaseFlags_set_f_flag, gDuelPhaseFlags_criteria_arr_base)
- C8 stale FUN_: 6 occurrences in asm/10 + 1 in asm/11 (FUN_0807fde8 -> dispatch_equip_criteria_display_by_type_code at asm/11 L7484); includes FUN_08081ce8 -> tick_equip_effect_slot_display_state at asm/10 L14644 (push_to_effect_slot_array plate)
- Split: NO SPLIT -- 18 fn, all pre-named, 0 ROM_INCBIN, purely literal-pool symbolization
- Seek-help: none
- proposal: doc/dev/refine/F10-Seg-6.proposal.md
