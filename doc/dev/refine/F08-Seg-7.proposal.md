# Refine Proposal: F08-Seg-7  [0x0806a118..0x0806ab0c)

## Segment Map

- Function entries: x20 (all named, no FUN_ residue)
  - 0x0806a118 `dispatch_equip_zone_sprite_by_lp_state_with_placement_check`
  - 0x0806a240 `scan_equip_chain_slots_for_zone14_targets`
  - 0x0806a2ec `enqueue_zone_sprite_if_effect_slot_active`
  - 0x0806a334 `dispatch_equip_slot_sprite_by_field6_range_and_zone14`
  - 0x0806a3ec `enqueue_zone14_slot_sprite_from_node_field`
  - 0x0806a424 `dispatch_equip_effect_display_by_state`
  - 0x0806a4bc `apply_equip_activation_if_zone_slot_empty`
  - 0x0806a520 `enqueue_sprite_attr_by_player_bit_select`
  - 0x0806a548 `dispatch_zone_sprite_with_effect_node_and_state`
  - 0x0806a694 `test_equip_target_slot_zone11_from_lp_chain`
  - 0x0806a700 `dispatch_equip_chain_sprite_or_op31_by_subtype`
  - 0x0806a760 `set_player_state_flag_if_unguarded`
  - 0x0806a784 `enqueue_lp_row_type8_if_equippable_slots_nonzero`
  - 0x0806a7c4 `scan_equip_slots_for_activation_with_sprite_feedback`
  - 0x0806a884 `tick_zone_sprite_pipeline_for_lp_shape_enqueue`
  - 0x0806a8bc `dispatch_lp_row_or_banisher_sprite_by_state_and_player`
  - 0x0806a954 `dispatch_lp_row_by_state_if_token_bit_set`
  - 0x0806a9a4 `dispatch_slot_sprite_without_field_intervention_card`
  - 0x0806aa14 `copy_token_halfword_if_zone_slot_occupied`
  - 0x0806aa64 `enqueue_equip_chain_sprite_for_dual_slot`
- Auto-name slots residual: 40x DAT_/DWORD_ (PTR_gP1LifePoints_0806a6f0 is PTR_-prefix, skip per convention)
- ROM_INCBIN / .byte blocks: 1 x 4B @ 0x0806a544 (movs r0,#0; bx lr; orphan stub, 0 refs -> §5.1)
- switchD: 0 (switchD_0806ac1e is Seg-8, outside this range)
- Non-ASCII lines: 0 (verified by python grep over segment lines)
- Stale FUN_ refs: 0 (verified by python grep over segment lines)

## Data Block Classification (Rule 2/3)

One .byte block found at asm/08 L14505 (0x0806a544, 4B: `.byte 0x00,0x20,0x70,0x47`).
Ref-scan: raw=0, THUMB+1=0 -> 0 total refs -> Rule 3: §5.1 registry (留待; no disasm/carve needed).
No ROM_INCBIN / .incbin / switchD in Seg-7.

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

All 40 slots are EQ type (literal pool `.word` -> equate substitution).

| slot | ROM addr | value | constant | inc | status |
|------|----------|-------|----------|-----|--------|
| DWORD_0806a1ec | 0x0806a1ec | 0x0201c4e0 | gP1LifePoints | ewram.inc | reuse |
| DWORD_0806a210 | 0x0806a210 | 0x0201c4e0 | gP1LifePoints | ewram.inc | reuse |
| DWORD_0806a2e0 | 0x0806a2e0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DWORD_0806a2e4 | 0x0806a2e4 | 0x00001cb8 | EQUIP_ZONE_COUNT_TABLE_OFF | duel_field.inc | **new** |
| DWORD_0806a2e8 | 0x0806a2e8 | 0x000012ea | MONSTER_REBORN_CID | card_info.inc | reuse |
| DAT_0806a3e4 | 0x0806a3e4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806a3e8 | 0x0806a3e8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806a440 | 0x0806a440 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806a47c | 0x0806a47c | 0x000012e5 | POLYMERIZATION_CID | card_info.inc | reuse |
| DAT_0806a480 | 0x0806a480 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806a484 | 0x0806a484 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc | reuse |
| DAT_0806a518 | 0x0806a518 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806a51c | 0x0806a51c | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DWORD_0806a540 | 0x0806a540 | 0x0000801c | OAM_EQUIP_SPRITE_TILE_P2_1C | oam_attr.inc | reuse |
| DAT_0806a614 | 0x0806a614 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806a618 | 0x0806a618 | 0x0000184d | MIND_HAXORZ_CID | card_info.inc | reuse |
| DAT_0806a61c | 0x0806a61c | 0x00008028 | OAM_ZONE_SPRITE_PAIR_P2_FIRST | oam_attr.inc | **new** |
| DAT_0806a620 | 0x0806a620 | 0x00008029 | OAM_EQUIP_SLOT_SPRITE_P2 | oam_attr.inc | reuse |
| DAT_0806a624 | 0x0806a624 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806a628 | 0x0806a628 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806a690 | 0x0806a690 | 0x0000184d | MIND_HAXORZ_CID | card_info.inc | reuse |
| DAT_0806a6f4 | 0x0806a6f4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | reuse |
| DAT_0806a6f8 | 0x0806a6f8 | 0x0201bbbc | gDuelEquipCtx | ewram.inc | reuse |
| DAT_0806a6fc | 0x0806a6fc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806a75c | 0x0806a75c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DWORD_0806a7c0 | 0x0806a7c0 | 0x0000ffff | LP_ROW_TYPE8_ALL_SLOTS_MASK | duel_field.inc | **new** |
| DWORD_0806a87c | 0x0806a87c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DWORD_0806a880 | 0x0806a880 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DWORD_0806a8fc | 0x0806a8fc | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DWORD_0806a924 | 0x0806a924 | 0x0201c4e0 | gP1LifePoints | ewram.inc | reuse |
| DWORD_0806a928 | 0x0806a928 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DWORD_0806a94c | 0x0806a94c | 0x0201c4e0 | gP1LifePoints | ewram.inc | reuse |
| DWORD_0806a950 | 0x0806a950 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | reuse |
| DWORD_0806a988 | 0x0806a988 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | reuse |
| DAT_0806aa08 | 0x0806aa08 | 0x0000135d | LIGHT_OF_INTERVENTION_CID | card_info.inc | reuse |
| DAT_0806aa0c | 0x0806aa0c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806aa10 | 0x0806aa10 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806aa5c | 0x0806aa5c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | reuse |
| DAT_0806aa60 | 0x0806aa60 | 0x0201c510 | gDuelFieldSlots | ewram.inc | reuse |
| DAT_0806ab08 | 0x0806ab08 | 0xffff0000 | EQUIP_CHAIN_SENTINEL | duel_field.inc | reuse |

### REF_SLOTS

None. No ROM_INCBIN blocks (no fn-ptr THUMB+1 slots needed). No carve labels.

### RENAME_SLOTS

None required. The 7 already-symbolized slots (gduelphaseflagss_0806a150, equip_phase_frame_off_*,
gduelcardctxbase_0806a1e8, player_block_stride_*) retain current descriptive hex-suffix labels;
EQ plan above replaces only the 40 DAT_/DWORD_ auto-name slots via equate.

### FUNC_RENAME (misnaming corrections)

None. All 20 function names are semantically consistent with observed code behavior:
- dispatch_equip_zone_sprite_by_lp_state_with_placement_check: reads gDuelPhaseFlags[+0x4a0], dispatches 0x7d/0x7e/0x7f/0x80; calls check_card_id_placement_allowed (asm/08 L14:13972). conf: high.
- scan_equip_chain_slots_for_zone14_targets: loops r6=0..1/r5=0..4 calling check_value_in_slot_chain + test_equip_target_slot_zone14 (L14:14117). conf: high.
- dispatch_zone_sprite_with_effect_node_and_state: state 0x7f/0x80 dispatch + MIND_HAXORZ_CID (0x184d) branch (L14:14621). conf: high.
- dispatch_lp_row_or_banisher_sprite_by_state_and_player: [r4+8] bit0=token_player_bit; state 0x80->LP row/type5, state 0x7f->Banisher LP_CARD_TRACK_BASE_OFF path (L14:15066-15131). conf: high.
- enqueue_equip_chain_sprite_for_dual_slot: check_effect_slot_matches_zone_entry x2 + build_equip_chain_slot_entry + find_equip_chain_pair_across_field x2 + enqueue_equip_chain_slot_sprite_with_pair_lookup; EQUIP_CHAIN_SENTINEL gate (L14:15374). conf: high.

### PLATE

None needed. All 20 functions already have complete ASCII plate comments.
No CJK chars and no stale FUN_ refs verified by python grep over segment lines L13881..L15411.

## Carve Plan (R7)

None. No ROM_INCBIN or data-table blocks in Seg-7.

## Disasm Plan (R4)

None. No mislabeled data blocks in Seg-7.

## New Constants / Globals

3 new equates required (all verified against ROM):

### 1. EQUIP_ZONE_COUNT_TABLE_OFF = 0x00001cb8  ->  constants/duel_field.inc

Consumer: `scan_equip_chain_slots_for_zone14_targets` @ 0x0806a240.
asm/08 L14069-14072: `ldr r1, DWORD_0806a2e4; adds r1,r1,r6(gDuelFieldSlots); mov r8,r1`
-> r8 = gDuelFieldSlots+0x1cb8 = 0x0201e1c8 = gEquipZoneCountTable (ewram.inc:395).
Then L14102: `mov r1,r8; ldr r4,[r1,#0]` -> reads word at gEquipZoneCountTable.
C5 domain exception: DUEL_ACTIVE_PLAYER_OFF=0x1cb8 uses base=gP1LifePoints
(0x0201c4e0+0x1cb8=0x0201e198); this slot uses base=gDuelFieldSlots
(0x0201c510+0x1cb8=0x0201e1c8). Different addresses, different global. Per C5 domain
exception rule (same value, different base -> independent constant).
ROM verify: slot 0x06a2e4 -> ROM=0x00001cb8. conf: high (gDuelFieldSlots+0x1cb8 =
gEquipZoneCountTable, named global, 55 ROM refs; reviewer L14098-14099 confirmed base=gDuelFieldSlots).
Placement: after DUEL_ACTIVE_PLAYER_OFF in duel_field.inc with domain-distinction EOL note.

### 2. OAM_ZONE_SPRITE_PAIR_P2_FIRST = 0x00008028  ->  constants/oam_attr.inc

Consumer: `dispatch_zone_sprite_with_effect_node_and_state` @ 0x0806a548.
asm/08 L14573-14582: P2 path (r4!=0) loads `ldr r1, DAT_0806a61c (0x8028)` ->
`enqueue_sprite_attr_record(attr=0x8028, slot_idx, 0, 0)` -- first sprite in zone display pair.
P1 path uses inline `movs r1,#0x28` (not a pool slot).
Sibling: OAM_EQUIP_SLOT_SPRITE_P2=0x8029 (oam_attr.inc L55) is the SECOND sprite in the same
pair in the same function. 0x8028 (first in pair) is not yet defined.
Distinct from: OAM_EQUIP_SLOT_SPRITE_P1=0x8034 and OAM_EQUIP_SPRITE_TILE_P2_1C=0x801c.
ROM verify: 15 raw refs (python ref-scan). Slot 0x06a61c -> ROM=0x00008028. conf: high.
Placement: adjacent to OAM_EQUIP_SLOT_SPRITE_P2 in oam_attr.inc.

### 3. LP_ROW_TYPE8_ALL_SLOTS_MASK = 0x0000ffff  ->  constants/duel_field.inc

Consumer: `enqueue_lp_row_type8_if_equippable_slots_nonzero` @ 0x0806a784.
asm/08 L14873: `ldr r1, DWORD_0806a7c0 (0xffff); movs r2,#0x1; bl set_lp_display_row_type8`
-> r1=slot_mask=all 5 slots selected. Fixed argument.
C5 domain exception: existing 0xffff constants: EQUIP_SLOT_SCORE_CAP (equip score domain),
SLOT_CARD_EMPTY (card sentinel domain), OAM_ATTR0_HIDDEN (OAM attr domain). LP row type8
slot_mask is a distinct domain (LP display all-slots selector). Per domain exception rule:
new constant justified.
ROM verify: slot 0x06a7c0 -> ROM=0x0000ffff. conf: high.
Placement: duel_field.inc LP row type section.

## Section 5.1 Registry (Rule 3) -- 0-ref blocks

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|------|------|----------|----------|------|
| 0x0806a544 | 4B | Seg-7 | movs r0,#0; bx lr (orphan 4B stub, 0 raw+0 THUMB+1 refs) | pending |

## Consumer Evidence (R6) -- key slot semantics

| slot | consumer fn | asm line | evidence | conf |
|------|------------|---------|---------|------|
| DWORD_0806a2e4=0x1cb8 | scan_equip_chain_slots_for_zone14_targets | L14069-14072 | `adds r1,r1,r6(gDuelFieldSlots); mov r8,r1` -> gDuelFieldSlots+0x1cb8=gEquipZoneCountTable(0x0201e1c8); reviewer confirmed | high |
| DAT_0806a61c=0x8028 | dispatch_zone_sprite_with_effect_node_and_state | L14573-14582 | `ldr r1,DAT; enqueue_sprite_attr_record` P2 path, paired with 0x8029 second sprite | high |
| DWORD_0806a7c0=0xffff | enqueue_lp_row_type8_if_equippable_slots_nonzero | L14873-14875 | `ldr r1,(0xffff); bl set_lp_display_row_type8` r1=slot_mask fixed arg | high |
| DAT_0806a6f8=gDuelEquipCtx | test_equip_target_slot_zone11_from_lp_chain | L14710-14712 | `ldr r1,(0x0201bbbc); adds r3,r0,r1` chain_entry_ptr base | high |
| DAT_0806ab08=EQUIP_CHAIN_SENTINEL | enqueue_equip_chain_sprite_for_dual_slot | L15374-15376 | `ldr r1,(0xffff0000); cmp r0,r1; beq exit` list terminator sentinel | high |
| DAT_0806a618=MIND_HAXORZ_CID | dispatch_zone_sprite_with_effect_node_and_state | L14534-14536 | `ldrh r2,[r2,#0]; cmp r2,r0(0x184d)` card_id gate for Mind Haxorz CID branch | high |
| DAT_0806a47c=POLYMERIZATION_CID | dispatch_equip_effect_display_by_state | L14358 | `ldr r1,DAT_0806a47c; bl find_card_pair_in_player_deck_list` card_id arg 0x12e5 | high |

## Help Requested

[Resolved by reviewer] EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8: reviewer confirmed gDuelFieldSlots+0x1cb8=gEquipZoneCountTable(0x0201e1c8, ewram.inc:395, 55 ROM refs). Name updated from ZONE14_CHAIN_SLOT_FLAG_OFF to EQUIP_ZONE_COUNT_TABLE_OFF, conf: high.
