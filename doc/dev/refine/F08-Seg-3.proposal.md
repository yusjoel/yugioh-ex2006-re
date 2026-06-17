# Refine Proposal: F08-Seg-3  [0x08066448..0x08067160)

## Section Survey
- Functions: 20 named entries
- Auto-name slots: 56 (all DWORD_/DAT_ definitions, lines 4853-6497)
- ROM_INCBIN blocks: 1 (DAT_080668c0, size=0x1cc)
- switchD tables: 1 (switchD_08066f02 already disassembled inline)
- Non-ASCII / stale FUN_: 0 non-ASCII; 2 stale FUN_ in plate text

---

## Function Entry Map
| addr | name |
|------|------|
| 0x08066448 | dispatch_equip_zone_sprite_by_slot_state |
| 0x08066530 | enqueue_graveyard_sprite_via_hand_slot_zone |
| 0x080665a4 | apply_lp_delta_for_slot_player |
| 0x080665c0 | enqueue_lp_counter_sprite_for_slot |
| 0x080665d4 | dispatch_zone_state_for_reserved_icid_slot |
| 0x08066698 | dispatch_lp_counter_or_sprite_by_zone_state |
| 0x080666f4 | render_equip_zone_sprites_both_players |
| 0x0806678c | enqueue_equip_zone_sprite_with_chain_check |
| 0x0806683c | enqueue_hand_spell_sprite_for_slot |
| 0x08066858 | dispatch_equip_zone_sprite_by_effect_type |
| 0x08066a94 | apply_equip_activation_for_slot_with_chain_branch |
| 0x08066b10 | apply_equip_activation_across_slots |
| 0x08066bf0 | apply_effect_node_sprites_all_zones |
| 0x08066c40 | enqueue_equip_zone_sprite_with_spell_card_mode |
| 0x08066d04 | enqueue_equip_zone_sprite_mode4_for_slot |
| 0x08066d68 | enqueue_graveyard_sprite_for_polymerization_pair |
| 0x08066dac | evaluate_equip_zone_nodes_into_bitmap |
| 0x08066e0c | dispatch_equip_oam_by_zone_state_with_cyberstein |
| 0x08066ee0 | tick_equip_activation_display_seq |
| 0x080670a0 | tick_equip_activation_display_state |

---

## Residual Auto-Name Slots (56 total)
All definition lines 4853-6497.

| slot addr | value | function context | semantic |
|-----------|-------|-----------------|---------|
| DWORD_080664b8 | 0x117b | dispatch_equip_zone_sprite_by_slot_state: ldrh r1,[r7,#0] cmp r1,r0 | ARMED_NINJA_CID -- reuse |
| DWORD_080664bc | 0x12eb | same fn: second card_id check | DE_SPELL_CID -- new |
| DWORD_080664c0 | 0x868 | same fn: muls r1,r2 (player stride) | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_080664c4 | 0x0201c510 | same fn: gDuelFieldSlots base | gDuelFieldSlots -- reuse |
| DWORD_08066594 | 0x868 | enqueue_graveyard_sprite_via_hand_slot_zone: player stride | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066598 | 0x0201c8f8 | same fn: hand slot array base | gP1HandSlotArray -- reuse |
| DWORD_080665f0 | 0x162c | dispatch_zone_state_for_reserved_icid_slot: ldrh r3,[r2,#0] cmp r3,r0 | ICID_RESERVED_A -- new (cid=0xFFFF, plate confirms reserved) |
| DWORD_080665f4 | 0x1051 | same fn: second reserved icid branch (r1=5) | ICID_RESERVED_C -- new (cid=0xFFFF) |
| DWORD_08066600 | 0x184c | same fn: third reserved icid (r1=3, same branch as 0x162c) | ICID_RESERVED_B -- new (cid=0xFFFF) |
| DWORD_08066624 | 0x0201b290 | same fn: gDuelPhaseFlags (EQUIP_STATE dispatch) | gDuelPhaseFlags -- reuse |
| DWORD_08066660 | 0x0201c4e0 | dispatch_zone_state_for_reserved_icid_slot state=0x80 path | gP1LifePoints -- reuse (slot already uses named label; DWORD_ not replaced yet) |
| DWORD_08066664 | 0x868 | same fn: player stride | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066668 | 0x0201e2a0 | same fn: gDuelCardCtxBase | gDuelCardCtxBase -- reuse |
| DWORD_080666b4 | 0x0201b290 | dispatch_lp_counter_or_sprite_by_zone_state | gDuelPhaseFlags -- reuse |
| DWORD_080666e0 | 0x8059 | same fn: OAM attr for player2 sprite | OAM_ATTR_P2_SPRITE -- new |
| DWORD_08066730 | 0x0201c4e0 | render_equip_zone_sprites_both_players: ldr r0 -> mov r8 | gP1LifePoints -- reuse (slot) |
| DWORD_08066734 | 0x1ce8 | same fn: zone-15 state sub-struct offset | P1LP_BLOCK2_OFF_1CE8 -- reuse |
| DWORD_08066738 | 0x0201bbbc | same fn: gDuelEquipCtx base | gDuelEquipCtx -- reuse |
| DWORD_08066788 | 0x868 | same fn: player stride for zone entry | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066830 | 0x868 | enqueue_equip_zone_sprite_with_chain_check | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066834 | 0x0201c510 | same fn: gDuelFieldSlots | gDuelFieldSlots -- reuse |
| DWORD_08066838 | 0x19a5 | same fn: card_id Raviel check | RAVIEL_LORD_CID -- reuse |
| DWORD_08066888 | 0x0201b290 | dispatch_equip_zone_sprite_by_effect_type | gDuelPhaseFlags -- reuse |
| DWORD_0806688c | 0x08066890 | same fn: raw-addr jump table pointer | dispatch_equip_zone_by_effect_type_jump_table -- R2 label |
| DWORD_08066af0 | 0x868 | apply_equip_activation_for_slot_with_chain_branch | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066af4 | 0x0201c510 | same fn: gDuelFieldSlots | gDuelFieldSlots -- reuse |
| DWORD_08066be8 | 0x868 | apply_equip_activation_across_slots | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066bec | 0x0201c510 | same fn: gDuelFieldSlots | gDuelFieldSlots -- reuse |
| DWORD_08066c3c | 0x0201e1c8 | apply_effect_node_sprites_all_zones | gEquipZoneCountTable -- reuse |
| DWORD_08066cbc | 0x868 | enqueue_equip_zone_sprite_with_spell_card_mode | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066cc0 | 0x0201c510 | same fn: gDuelFieldSlots | gDuelFieldSlots -- reuse |
| DWORD_08066cc4 | 0x16a2 | same fn: card_id BATTLE_SCARRED | BATTLE_SCARRED_CID -- reuse |
| DWORD_08066cc8 | 0x1243 | same fn: card_id SHADOW_SPELL | SHADOW_SPELL_CID -- reuse |
| DWORD_08066d00 | 0x17ff | same fn: card_id NINJITSU_ART_OF_DECOY | NINJITSU_ART_OF_DECOY_CID -- reuse |
| DWORD_08066d5c | 0x868 | enqueue_equip_zone_sprite_mode4_for_slot | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066d60 | 0x0201c510 | same fn: gDuelFieldSlots | gDuelFieldSlots -- reuse |
| DWORD_08066d64 | 0x1119 | same fn: card_id SANGA_OF_THUNDER | SANGA_OF_THUNDER_CID -- reuse |
| DWORD_08066da0 | 0x12e5 | enqueue_graveyard_sprite_for_polymerization_pair | POLYMERIZATION_CID -- reuse |
| DWORD_08066da4 | 0x868 | same fn: player stride | PLAYER_BLOCK_STRIDE -- reuse |
| DWORD_08066da8 | 0x0201c8f8 | same fn: hand slot array base | gP1HandSlotArray -- reuse |
| DAT_08066e2c | 0x0201b290 | dispatch_equip_oam_by_zone_state_with_cyberstein | gDuelPhaseFlags -- reuse |
| DAT_08066ebc | 0x114a | same fn: card_id Cyber-Stein | CYBER_STEIN_CID -- new |
| DAT_08066f04 | 0x0201b290 | tick_equip_activation_display_seq | gDuelPhaseFlags -- reuse |
| DAT_08066f08 | 0x08066f0c | same fn: switchD table pointer | switchD_08066f02__switchdataD_08066f0c (already named label) -- R2 label |
| DAT_08066f90 | 0x1919 | switchD caseD_80: card_id T.A.D.P.O.L.E. | TADPOLE_CID -- reuse |
| DAT_08066f94 | 0x4a4 | switchD caseD_80: EQUIP_PHASE_FRAME_OFF (gDuelPhaseFlags+0x4a4) | EQUIP_PHASE_FRAME_OFF -- reuse |
| DAT_08066fa4 | 0x4a4 | switchD caseD_80: second use of 0x4a4 | EQUIP_PHASE_FRAME_OFF -- reuse |
| DAT_08066fec | 0x868 | switchD caseD_7f: player stride | PLAYER_BLOCK_STRIDE -- reuse |
| DAT_08066ff0 | 0x0201c740 | switchD caseD_7f: gP1SlotSetCodeArray (hand slot base for flip) | gP1SlotSetCodeArray -- reuse |
| DAT_08066ff4 | 0x0201b290 | switchD caseD_7f: gDuelPhaseFlags for [+0x4a4] decrement | gDuelPhaseFlags -- reuse |
| DAT_08066ff8 | 0x4a4 | switchD caseD_7f: EQUIP_PHASE_FRAME_OFF | EQUIP_PHASE_FRAME_OFF -- reuse |
| DAT_08067044 | 0x0201e2a0 | switchD caseD_7e: gDuelCardCtxBase | gDuelCardCtxBase -- reuse |
| DAT_080670c8 | 0x0201b290 | tick_equip_activation_display_state | gDuelPhaseFlags -- reuse |
| DAT_080670f8 | 0x0201e2a0 | same fn: gDuelCardCtxBase | gDuelCardCtxBase -- reuse |
| DAT_08067150 | 0x1daa | tick_equip_activation_display_state: ldr r4 for enqueue_sprite_attr_with_mode | LP_CARD_TRACK_NEXT_OFF -- reuse |

Note: DWORD_08066660 and DWORD_08066730 use `gP1LifePoints` as value but the slot currently has a raw `.word 0x0201c4e0` label rather than a named reference. These need REF_SLOT treatment (not EQ).

---

## Data Block Classification (Rule 2/3)

### ROM_INCBIN block: DAT_080668c0, addr=0x080668c0, size=0x1cc

ref-scan (python `rom.count(struct.pack('<I', v))`):

| candidate | v (raw) | v|1 (THUMB) | count | kind |
|-----------|---------|-----------|-------|------|
| 0x080668c0 | 0x080668c0 | 0x080668c1 | raw=1, THUMB=0 | raw ref only |
| 0x0806691c | raw=1, THUMB=0 | raw ref only |
| 0x08066934 | raw=1, THUMB=0 | raw ref only |
| 0x08066a58 | raw=1, THUMB=0 | raw ref only |
| 0x08066a62 | raw=1, THUMB=0 | raw ref only (entry[3] @ 0x0806689c) |
| 0x08066a6e | raw=1, THUMB=0 | raw ref only (entry[2] @ 0x08066898) |
| 0x08066a7a | raw=1, THUMB=0 | raw ref only (entry[1] @ 0x08066894) |
| 0x08066a86 | raw=1, THUMB=0 | raw ref only (entry[0] @ 0x08066890) |
| all others | raw=0, THUMB=0 | no ref |

All 8 refs are raw (no +1). Source: lines 5497-5508 (DWORD_0806688c jump table, 12 entries, 8 distinct targets + 4 fall-through to 0x08066a8c).
Dispatch mechanism: `ldr r0,[r0,#0]; .hword 0x4687 (MOV PC,r0)` -- raw-addr computed branch staying in THUMB mode (CPU remains in THUMB since processor state is inherited from calling context, not from address bit0).

**Judgment: R4 DISASM** -- THUMB code stubs dispatched via raw-pointer table (MOV PC,r0). Block starts with valid THUMB opcodes: `1c30`=adds r0,r6,0; `f7f5 fca8`=bl; etc. (machine-code verified).

Active entry points within block (table base 0x08066890, index = state - 0x75):
| offset | addr | state case | evidence |
|--------|------|-----------|---------|
| +0x00 | 0x080668c0 | state=0x80 | table entry[11] at 0x080668bc |
| +0x5c | 0x0806691c | state=0x7f | table entry[10] at 0x080668b8 |
| +0x74 | 0x08066934 | state=0x7e | table entry[9] at 0x080668b4 |
| +0x198 | 0x08066a58 | state=0x7d | table entry[8] at 0x080668b0 |
| +0x1c6 | 0x08066a86 | state=0x75 | table entry[0] at 0x08066890 |
| +0x1ba | 0x08066a7a | state=0x76 | table entry[1] at 0x08066894 |
| +0x1ae | 0x08066a6e | state=0x77 | table entry[2] at 0x08066898 |
| +0x1a2 | 0x08066a62 | state=0x78 | table entry[3] at 0x0806689c |

States 0x79..0x7c fall through to LAB_08066a8c (first instruction after block) -- these 4 cases (entries[4..7] at 0x080668a0..0x080668ac) store 0x08066a8c and have no entries within the block itself.

---

## Symbolization Plan

### EQ_SLOTS (data-equate)

| slot | value | const_name | src | slot_label |
|------|-------|-----------|-----|-----------|
| DWORD_080664b8 | 0x117b | ARMED_NINJA_CID | constants/card_info.inc:656 (reuse) | dispatch_equip_zone_by_slot_state_cid_a |
| DWORD_080664bc | 0x12eb | DE_SPELL_CID | NEW: pw=19159413 card_0673 (reuse value grep=0) | dispatch_equip_zone_by_slot_state_cid_b |
| DWORD_080664c0 | 0x868 | PLAYER_BLOCK_STRIDE | constants/ewram.inc:250 (reuse) | dispatch_equip_zone_player_stride |
| DWORD_080664c4 | 0x0201c510 | gDuelFieldSlots | constants/ewram.inc:312 (reuse) | dispatch_equip_zone_field_slots |
| DWORD_08066594 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | enqueue_gyd_hand_slot_stride |
| DWORD_08066598 | 0x0201c8f8 | gP1HandSlotArray | constants/ewram.inc:332 (reuse) | enqueue_gyd_hand_slots |
| DWORD_080665f0 | 0x162c | ICID_RESERVED_A | NEW (not in any .inc; cid=0xFFFF per plate) | dispatch_reserved_icid_a |
| DWORD_080665f4 | 0x1051 | ICID_RESERVED_C | NEW (not in any .inc; cid=0xFFFF per plate) | dispatch_reserved_icid_c |
| DWORD_08066600 | 0x184c | ICID_RESERVED_B | NEW (not in any .inc; cid=0xFFFF per plate) | dispatch_reserved_icid_b |
| DWORD_08066624 | 0x0201b290 | gDuelPhaseFlags | constants/ewram.inc:351 (reuse) | dispatch_reserved_icid_phase_flags |
| DWORD_08066664 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | dispatch_reserved_icid_state_stride |
| DWORD_08066668 | 0x0201e2a0 | gDuelCardCtxBase | constants/ewram.inc:218 (reuse) | dispatch_reserved_icid_display_ctx |
| DWORD_080666b4 | 0x0201b290 | gDuelPhaseFlags | reuse | dispatch_lp_ctr_phase_flags |
| DWORD_080666e0 | 0x8059 | OAM_ATTR_P2_SPRITE | NEW (not in any .inc; 0x8027=P1 in oam_attr.inc:147) | dispatch_lp_ctr_p2_sprite_attr |
| DWORD_08066734 | 0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | constants/ewram.inc:275 (reuse) | render_equip_zone_zone_state_off |
| DWORD_08066738 | 0x0201bbbc | gDuelEquipCtx | constants/ewram.inc:455 (reuse) | render_equip_zone_equip_ctx |
| DWORD_08066788 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | render_equip_zone_player_stride |
| DWORD_08066830 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | enqueue_equip_zone_chain_stride |
| DWORD_08066834 | 0x0201c510 | gDuelFieldSlots | reuse | enqueue_equip_zone_chain_field_slots |
| DWORD_08066838 | 0x19a5 | RAVIEL_LORD_CID | constants/card_info.inc:552 (reuse) | enqueue_equip_zone_chain_raviel_cid |
| DWORD_08066888 | 0x0201b290 | gDuelPhaseFlags | reuse | dispatch_equip_zone_effect_type_phase_flags |
| DWORD_08066af0 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | apply_equip_act_chain_stride |
| DWORD_08066af4 | 0x0201c510 | gDuelFieldSlots | reuse | apply_equip_act_chain_field_slots |
| DWORD_08066be8 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | apply_equip_act_slots_stride |
| DWORD_08066bec | 0x0201c510 | gDuelFieldSlots | reuse | apply_equip_act_slots_field_slots |
| DWORD_08066c3c | 0x0201e1c8 | gEquipZoneCountTable | constants/ewram.inc:395 (reuse) | apply_effect_node_zone_count_tbl |
| DWORD_08066cbc | 0x868 | PLAYER_BLOCK_STRIDE | reuse | enqueue_equip_zone_spell_stride |
| DWORD_08066cc0 | 0x0201c510 | gDuelFieldSlots | reuse | enqueue_equip_zone_spell_field_slots |
| DWORD_08066cc4 | 0x16a2 | BATTLE_SCARRED_CID | constants/card_info.inc:572 (reuse) | enqueue_equip_zone_spell_cid_a |
| DWORD_08066cc8 | 0x1243 | SHADOW_SPELL_CID | constants/card_info.inc:1089 (reuse) | enqueue_equip_zone_spell_cid_b |
| DWORD_08066d00 | 0x17ff | NINJITSU_ART_OF_DECOY_CID | constants/card_info.inc:530 (reuse) | enqueue_equip_zone_spell_cid_c |
| DWORD_08066d5c | 0x868 | PLAYER_BLOCK_STRIDE | reuse | enqueue_equip_zone_mode4_stride |
| DWORD_08066d60 | 0x0201c510 | gDuelFieldSlots | reuse | enqueue_equip_zone_mode4_field_slots |
| DWORD_08066d64 | 0x1119 | SANGA_OF_THUNDER_CID | constants/card_info.inc:1125 (reuse) | enqueue_equip_zone_mode4_cid |
| DWORD_08066da0 | 0x12e5 | POLYMERIZATION_CID | constants/card_info.inc:436 (reuse) | enqueue_gyd_poly_pair_cid |
| DWORD_08066da4 | 0x868 | PLAYER_BLOCK_STRIDE | reuse | enqueue_gyd_poly_pair_stride |
| DWORD_08066da8 | 0x0201c8f8 | gP1HandSlotArray | reuse | enqueue_gyd_poly_pair_hand_slots |
| DAT_08066e2c | 0x0201b290 | gDuelPhaseFlags | reuse | dispatch_equip_oam_cyberstein_phase_flags |
| DAT_08066ebc | 0x114a | CYBER_STEIN_CID | NEW: pw=69015963 card_0361 slot=0x114A (reuse value grep=0) | dispatch_equip_oam_cyberstein_cid |
| DAT_08066f04 | 0x0201b290 | gDuelPhaseFlags | reuse | tick_equip_act_disp_seq_phase_flags |
| DAT_08066f90 | 0x1919 | TADPOLE_CID | constants/card_info.inc:369 (reuse) | tick_equip_act_disp_seq_tadpole_cid |
| DAT_08066f94 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | constants/ewram.inc:434 (reuse) | tick_equip_act_disp_seq_frame_off_a |
| DAT_08066fa4 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | reuse | tick_equip_act_disp_seq_frame_off_b |
| DAT_08066fec | 0x868 | PLAYER_BLOCK_STRIDE | reuse | tick_equip_act_disp_seq_stride |
| DAT_08066ff0 | 0x0201c740 | gP1SlotSetCodeArray | constants/ewram.inc:330 (reuse) | tick_equip_act_disp_seq_hand_slots |
| DAT_08066ff4 | 0x0201b290 | gDuelPhaseFlags | reuse | tick_equip_act_disp_seq_phase_flags_b |
| DAT_08066ff8 | 0x4a4 | EQUIP_PHASE_FRAME_OFF | reuse | tick_equip_act_disp_seq_frame_off_c |
| DAT_08067044 | 0x0201e2a0 | gDuelCardCtxBase | reuse | tick_equip_act_disp_seq_card_ctx |
| DAT_080670c8 | 0x0201b290 | gDuelPhaseFlags | reuse | tick_equip_act_disp_state_phase_flags |
| DAT_080670f8 | 0x0201e2a0 | gDuelCardCtxBase | reuse | tick_equip_act_disp_state_card_ctx |
| DAT_08067150 | 0x1daa | LP_CARD_TRACK_NEXT_OFF | constants/ewram.inc:248 (reuse) | tick_equip_act_disp_state_lp_track_off |

### REF_SLOTS (USER-label + DATA-ref)

| slot | value | note | gas_label | slot_label |
|------|-------|------|-----------|-----------|
| DWORD_08066660 | 0x0201c4e0 | gP1LifePoints base addr; function dispatch_zone_state_for_reserved_icid_slot; used as muls r0,r2 base then adds r1,r0 -- already has named symbol in asm but raw DWORD_ label | gP1LifePoints | dispatch_reserved_icid_lp_base |
| DWORD_08066730 | 0x0201c4e0 | render_equip_zone_sprites_both_players; ldr r0 -> mov r8 | gP1LifePoints | render_equip_zone_lp_base |
| DWORD_0806688c | 0x08066890 | dispatch_equip_zone_sprite_by_effect_type raw-addr jump table ptr | dispatch_equip_zone_by_effect_type_jump_table | dispatch_equip_zone_effect_type_jump_tbl_ptr |
| DAT_08066f08 | 0x08066f0c | tick_equip_activation_display_seq switchD table ptr; target already has label switchD_08066f02__switchdataD_08066f0c | switchD_08066f02__switchdataD_08066f0c | tick_equip_act_disp_seq_switch_tbl_ptr |

Note: PTR_gP1LifePoints_08067048 / PTR_gP1LifePoints_08067078 / PTR_gP1LifePoints_08067128 / PTR_gP1LifePoints_0806714c are already labeled (not auto-name slots).

### RENAME_SLOTS (descriptive slot label + EOL)

| slot | current | new_label | eol |
|------|---------|-----------|-----|
| dispatch_equip_zone_player_stride | DWORD_080664c0 | dispatch_equip_zone_player_stride | PLAYER_BLOCK_STRIDE |
| dispatch_equip_zone_field_slots | DWORD_080664c4 | dispatch_equip_zone_field_slots | gDuelFieldSlots |

(All other slots get new labels as listed above; no additional rename needed beyond EQ plan.)

### FUNC_RENAME

None detected. All 20 function names are consistent with function bodies. (No function-name/body contradiction observed.)

### PLATE (R5 -- full rewrite or substring replace)

1. `apply_lp_delta_for_slot_player` (0x080665a4):
   - Stale FUN_ in plate: `FUN_08073428` -> `apply_lp_delta_for_slot_by_series_code` (asm/09_equip_lp_display.s:9288)
   - Stale FUN_ in plate: `FUN_08074770` -> `dispatch_dragon_summon_or_lp_delta_by_slot_type` (asm/09_equip_lp_display.s:11076)
   - Action: substring replace both FUN_ occurrences in plate text (ASCII-safe)

---

## Disasm Plan (R4)

### ROM_INCBIN at 0x080668c0/0x1cc -> R4 DISASM

8 active entry stubs; 4 cases (0x79..0x7c) fall through to LAB_08066a8c (outside block).

Disasm sequence (clearListing 0x080668c0..0x08066a8c -> setTMode -> per-stub DisassembleCommand):

| entry addr | state | proposed label |
|-----------|-------|---------------|
| 0x080668c0 | 0x80 | dispatch_equip_effect_type_stub_80 |
| 0x0806691c | 0x7f | dispatch_equip_effect_type_stub_7f |
| 0x08066934 | 0x7e | dispatch_equip_effect_type_stub_7e |
| 0x08066a58 | 0x7d | dispatch_equip_effect_type_stub_7d |
| 0x08066a62 | 0x78 | dispatch_equip_effect_type_stub_78 |
| 0x08066a6e | 0x77 | dispatch_equip_effect_type_stub_77 |
| 0x08066a7a | 0x76 | dispatch_equip_effect_type_stub_76 |
| 0x08066a86 | 0x75 | dispatch_equip_effect_type_stub_75 |

After disasm: label each stub entry, add plate describing the state dispatched and callee.
The first instruction at each entry must be verified against ROM bytes (machine-code self-check):
- 0x080668c0: `1c30` = adds r0,r6,#0 (confirmed)
- 0x0806691c: `8834` = ldrh r4,[r6,#0] (confirmed)
- 0x08066934: `2400` = movs r4,#0 (confirmed)
- 0x08066a58: `1c28` = adds r0,r5,#0 (confirmed)
- 0x08066a62: `2001` = movs r0,#1 (ROM byte: e015 1c28; at 0x08066a60: e015=b LAB; 0x08066a62: 1c28=adds r0,r5,#0 wait let me recheck)

Machine-code verification for 0x08066a62:
ROM at 0x66a62: from dump line `0x08066a60: e015 1c28`, so 0x08066a62 = `1c28` = `adds r0,r5,#0`.
0x08066a6e: from `0x08066a6c: e00f 2001`, so 0x08066a6e = `2001` = `movs r0,#1`.
Hmm - let me re-read: at offset 0x08066a6e, looking at dump:
```
0x08066a6c: e00f 2001  -> 0x08066a6c=e00f=b +15, 0x08066a6e=2001=movs r0,#1
0x08066a70: 1b40 f03b  -> 0x08066a70=1b40=subs r0,r0,r1
```
So:
- 0x08066a6e: `2001` = movs r0,#1 (neg-delta setup?)
- 0x08066a7a: ROM bytes at 0x08066a7a = `28 1c` = `0x1c28` = `adds r0,r5,#0` (note: 0x08066a7c contains `2100`=movs r1,#0 which is the second instruction, not the first)
- 0x08066a86: at 0x08066a84=e003, so 0x08066a86=`1c28`=adds r0,r5,#0

The stubs at the later addresses are shorter (often 2-4 instructions ending in a bl and then the fall-through to LAB_08066a8c). Standard file 08 disasm pattern applies.

### switchD_08066f02

Already **fully disassembled inline** within `tick_equip_activation_display_seq`. Case labels (`switchD_08066f02__caseD_80` through `caseD_65`) are all present in asm (lines 6248-6396). No additional disasm action needed.

---

## carve plan (R7)

None. Block at 0x080668c0 is code (R4 disasm), not data table.

---

## New Constants / Globals Required

Must create in `constants/card_info.inc` (new equates):

| name | value | evidence |
|------|-------|---------|
| DE_SPELL_CID | 0x12eb | card_0673 slot=0x12EB pw=19159413 (card-stats.s:8764); used in dispatch_equip_zone_sprite_by_slot_state cmp card_id; value grep in card_info.inc = 0 hits (conf: high) |
| CYBER_STEIN_CID | 0x114a | card_0361 slot=0x114A pw=69015963 (card-stats.s:4708); used in dispatch_equip_oam_by_zone_state_with_cyberstein state=0x7e path cmp r1,r0; value grep in card_info.inc = 0 hits (conf: high) |
| ICID_RESERVED_A | 0x162c | function plate: "cid=0xFFFF, reserved" (asm line 5032); no card-stats.s slot entry; value grep = 0 hits (conf: high) |
| ICID_RESERVED_B | 0x184c | function plate: "cid=0xFFFF, reserved" (asm line 5033); no card-stats.s slot entry; value grep = 0 hits (conf: high) |
| ICID_RESERVED_C | 0x1051 | function plate: "cid=0xFFFF, reserved" (asm line 5034); no card-stats.s slot entry; value grep = 0 hits (conf: high) |

Must create in `constants/oam_attr.inc` (new equate):

| name | value | evidence |
|------|-------|---------|
| OAM_ATTR_P2_SPRITE | 0x8059 | dispatch_lp_counter_or_sprite_by_zone_state: player_id==1 path `ldr r1, DWORD_080666e0` instead of `movs r1,#0x59`; sibling of OAM_ATTR_P1_SPRITE=0x8027 (oam_attr.inc:147); 0x8059 = 0x8000 | 0x59 (OBJ palette bit | tile index 0x59); value grep in all constants = 0 hits (conf: high) |

No new gDuelPhaseFlags-relative offsets needed: EQUIP_STATE_NODE at 0x4a0 is already documented inline via EQUIP_PHASE_FRAME_OFF comment ("adjacent to phase code node +0x4a0"); and 0x1d40 appears only in the switchD caseD_7e inline as `lsls r2,#0x1f; movs r3,#0xea; lsls r3,#5` -- this is `0xea<<5=0x1d40` and only occurs once in this segment; low reuse -- new constant LP_FLAG_1D40_OFF in ewram.inc if repeated, but here it appears only in tick_equip_activation_display_state (line 6444-6448); BLOCKED pending frequency check below.

Frequency check for 0x1d40:
- ROM raw refs to 0x1d40 as a 4-byte value would be indirect (it's constructed via `movs r3,#0xea; lsls r3,#5`), so no direct slot for it in this segment. DAT/DWORD containing 0x1d40 not present; skip new constant.

---

## §5.1 Unref Register (Rule 3)

None. The single ROM_INCBIN block has 8 confirmed raw refs -- it is R4 disasm, not §5.1.

---

## Consumer Evidence (R6) -- Key Semantic Slots

| slot | semantic | file:line evidence | confidence |
|------|---------|-------------------|-----------|
| DWORD_080664b8=0x117b | ARMED_NINJA_CID | asm/08_equip_oam_neodaed.s:4805 `ldrh r1,[r7,#0]; ldr r0, DWORD_080664b8; cmp r1,r0` + card_info.inc:656 | high |
| DWORD_080664bc=0x12eb | DE_SPELL_CID | asm/08_equip_oam_neodaed.s:4808 second cmp | high (card-stats.s:8764 De-Spell) |
| DWORD_080665f0=0x162c | ICID_RESERVED_A | asm/08_equip_oam_neodaed.s:5029-5034 plate "cid=0xFFFF reserved" | high |
| DWORD_080665f4=0x1051 | ICID_RESERVED_C | asm/08_equip_oam_neodaed.s:5034 same plate | high |
| DWORD_08066600=0x184c | ICID_RESERVED_B | asm/08_equip_oam_neodaed.s:5033 same plate | high |
| DWORD_080666e0=0x8059 | OAM_ATTR_P2_SPRITE | asm/08_equip_oam_neodaed.s:5202 player_id==1 path vs movs r1,#0x59 player_id==0; sibling of OAM_ATTR_P1_SPRITE=0x8027 | high |
| DWORD_0806688c=0x08066890 | raw-addr jump table | asm/08_equip_oam_neodaed.s:5495-5508; 12 entries dispatching to sub-stubs via MOV PC,r0 | high |
| DAT_08066ebc=0x114a | CYBER_STEIN_CID | asm/08_equip_oam_neodaed.s:6146-6162; function named dispatch_equip_oam_by_zone_state_with_cyberstein; state=0x7e ldrh r1,[r6,#0]; ldr r0,DAT_08066ebc; cmp r1,r0 | high |
| DAT_08067150=0x1daa | LP_CARD_TRACK_NEXT_OFF | asm/08_equip_oam_neodaed.s:6487; adds r3,r3,r4; ldrh r3,[r3,#0] -- loads LP track hword via base+offset for sprite enqueue arg | high |

---

## Stale FUN_ Plate Text (C8)

Segment lines 4796-6506, grep for `FUN_[0-9a-f]{8}`:

| asm line | fn in | stale FUN_ | current name | source file |
|----------|-------|-----------|-------------|------------|
| 4987 | apply_lp_delta_for_slot_player plate | FUN_08073428 | apply_lp_delta_for_slot_by_series_code | asm/09_equip_lp_display.s:9288 |
| 4987 | apply_lp_delta_for_slot_player plate | FUN_08074770 | dispatch_dragon_summon_or_lp_delta_by_slot_type | asm/09_equip_lp_display.s:11076 |

Action: substring replace in plate comment for apply_lp_delta_for_slot_player.

---

## Executor Report: F08-Seg-3

- Slots: EQ=50 REF=4 RENAME=2 FUNC_RENAME=0 PLATE=1 (stale FUN_ fix)
- ROM_INCBIN: 1 block (0x080668c0/0x1cc) -> R4 disasm (8 stubs, states 0x75..0x80 except 0x79..0x7c fall-thru)
- switchD: 1 (switchD_08066f02) already disassembled inline -- no action needed
- carve=0 disasm=1 (0x080668c0..0x08066a8c) §5.1=0
- New constants: card_info.inc +5 (DE_SPELL_CID/CYBER_STEIN_CID/ICID_RESERVED_A/B/C); oam_attr.inc +1 (OAM_ATTR_P2_SPRITE)
- Reuse: PLAYER_BLOCK_STRIDE x14; gDuelFieldSlots x9; gP1HandSlotArray x2; gDuelPhaseFlags x9; gP1LifePoints x2(REF); gDuelCardCtxBase x3; EQUIP_PHASE_FRAME_OFF x3; RAVIEL_LORD_CID/TADPOLE_CID/POLYMERIZATION_CID/BATTLE_SCARRED_CID/SHADOW_SPELL_CID/NINJITSU_ART_OF_DECOY_CID/SANGA_OF_THUNDER_CID/ARMED_NINJA_CID/gDuelEquipCtx/gEquipZoneCountTable/gP1SlotSetCodeArray/P1LP_BLOCK2_OFF_1CE8/LP_CARD_TRACK_NEXT_OFF each x1
- Seek help: none (all slots fully resolved with high confidence)
- proposal: doc/dev/refine/F08-Seg-3.proposal.md
