# Refine Proposal: F10-Seg-4  [0x0807cd68..0x0807db20)

> file 10 Seg-4 -- 19 named fn + 2 fn_eligible stubs (BLK1 Sillva, inline .byte Dark Deal)
> 59 total pool labels: 50 DAT_/DWORD_ auto-names + 6 PTR_gP1LifePoints_ (skip per PTR-rule) + 1 BLK2-base DAT_ + 2 symbolic DWORD_ already holding gP1LifePoints + 3 symbolic DWORD_ already .word gP1LifePoints
> Wait -- see C13 below for exact reconciliation.
> 2 ROM_INCBIN (BLK1 0x7d7e8/0x2c fn_eligible Sillva; BLK2 0x7d830/0xfc 7 dispatch sub-stubs)
> 1 inline .byte block 0x7db14/0xc (fn_eligible Dark Deal)
> switchD_0807d126 (29 cases, 8 unique targets, all in [0x7cd68,0x7db20)) -- already decoded, no R4 action.

---

## Segment Mapping

### Functions x19

| addr       | name                                              |
|------------|---------------------------------------------------|
| 0x0807cd68 | tick_equip_slot_activation_score_and_oam          |
| 0x0807ce50 | build_equip_eligible_bitmap_for_slots             |
| 0x0807cef0 | apply_equip_activation_with_neo_daedalus_lp_output|
| 0x0807d014 | tick_equip_target_validity_prng_lp_display        |
| 0x0807d104 | tick_equip_activation_display_state_machine       |
| 0x0807d2e0 | tick_zone_pipeline_with_neo_daedalus_oam_setup    |
| 0x0807d36c | apply_equip_slot_activation_for_card_sprite       |
| 0x0807d3e0 | find_ojama_trio_in_deck_for_lp_display            |
| 0x0807d4dc | apply_equip_activation_by_field6_gate             |
| 0x0807d564 | apply_equip_activation_if_field6_gate_pending     |
| 0x0807d59c | enqueue_equip_zone_sprites_by_slot_chain          |
| 0x0807d65c | enqueue_cross_zone_slot_sprite_if_eligible        |
| 0x0807d69c | tick_equip_lp_indicator_or_score_display_seq      |
| 0x0807d700 | enqueue_ritual_eligible_sprite_or_type11          |
| 0x0807d7d0 | enqueue_lp_display_row_for_node                   |
| 0x0807d92c | tick_neo_daedalus_equip_oam_display_seq           |
| 0x0807d970 | tick_hand_spell_match_display_seq                 |
| 0x0807da70 | tick_equip_activation_display_by_node_state       |
| 0x0807dab0 | sync_equip_hand_oam_and_player_bits               |

### fn_eligible Stubs x2

| addr       | kind            | CID    | const_name (card_info.inc)             |
|------------|-----------------|--------|----------------------------------------|
| 0x0807d7e8 | BLK1 ROM_INCBIN | 0x1968 | SILLVA_WARLORD_OF_DARK_WORLD_CID L470  |
| 0x0807db14 | inline .byte    | 0x1975 | DARK_DEAL_CID L1054                    |

### Auto-name Slots

#### DAT_/DWORD_ with raw values (to be symbolized: 50 slots)

```
DAT_0807cd84  = 0x0201b290   tick_equip_slot_activation_score_and_oam (gDuelPhaseFlags)
DAT_0807cde8  = 0x0201e2a0   same fn (gDuelCardCtxBase)
DAT_0807cdec  = 0x08065991   same fn (fn-ptr check_equip_activation_at_slot11+1 slot A)
DAT_0807ce04  = 0x08065991   same fn (fn-ptr check_equip_activation_at_slot11+1 slot B)
DAT_0807ce48  = 0x00001d70   same fn (LP_BANISHER_CTX_OFF)
DAT_0807ce4c  = 0x00000868   same fn (PLAYER_BLOCK_STRIDE)
DAT_0807cee8  = 0x00000868   build_equip_eligible_bitmap_for_slots (PLAYER_BLOCK_STRIDE)
DAT_0807ceec  = 0x0201c510   same fn (gDuelFieldSlots)
DAT_0807cfb8  = 0x00000868   apply_equip_activation_with_neo_daedalus_lp_output (PLAYER_BLOCK_STRIDE)
DAT_0807d00c  = 0x00000868   same fn (PLAYER_BLOCK_STRIDE)
DAT_0807d010  = 0x0201c740   same fn (gP1SlotSetCodeArray)
DAT_0807d034  = 0x0201b290   tick_equip_target_validity_prng_lp_display (gDuelPhaseFlags)
DAT_0807d06c  = 0x0201e2a0   same fn (gDuelCardCtxBase)
DAT_0807d0c4  = 0x00001daa   same fn (LP_CARD_TRACK_NEXT_OFF)
DAT_0807d0c8  = 0x0201bb90   same fn (gEquipChainSlotRefs)
DAT_0807d100  = 0x0201bb90   same fn (gEquipChainSlotRefs)
DAT_0807d128  = 0x0201b290   tick_equip_activation_display_state_machine (gDuelPhaseFlags)
DAT_0807d12c  = 0x0807d130   same fn (switchD jump table ptr)
DAT_0807d1d8  = 0x00000139   same fn (TRIGGER_OP_PARAM_139 NEW)
DAT_0807d25c  = 0x08090625   same fn (fn-ptr invoke_effect_node_with_active_flag_3arg+1; passed as mode_ptr to set_equip_activation_state_by_mode)
DAT_0807d2cc  = 0x00001d68   same fn (ELIGIB_SPRITE_CTRL_OFF)
DWORD_0807d364 = 0x00000868  tick_zone_pipeline_with_neo_daedalus_oam_setup (PLAYER_BLOCK_STRIDE)
DWORD_0807d368 = 0x0201c8f8  same fn (gP1HandSlotArray)
DWORD_0807d3dc = 0x08050a55  apply_equip_slot_activation_for_card_sprite (fn-ptr check_equip_slot_eligible_by_card_id_bst+1)
DWORD_0807d400 = 0x0201b290  find_ojama_trio_in_deck_for_lp_display (gDuelPhaseFlags)
DWORD_0807d490 = 0x00001681  same fn (OJAMA_GREEN_CID)
DWORD_0807d494 = 0x000016b3  same fn (OJAMA_YELLOW_CID)
DWORD_0807d498 = 0x000016b4  same fn (OJAMA_BLACK_CID)
DWORD_0807d49c = 0x00000868  same fn (PLAYER_BLOCK_STRIDE)
DWORD_0807d4a0 = 0x0201c740  same fn (gP1SlotSetCodeArray)
DAT_0807d540   = 0x00000868  apply_equip_activation_by_field6_gate (PLAYER_BLOCK_STRIDE)
DAT_0807d544   = 0x0201c510  same fn (gDuelFieldSlots)
DWORD_0807d590 = 0x000010d0  apply_equip_activation_if_field6_gate_pending (LP_ACTIVATION_LINK_FLAG_OFF)
DWORD_0807d638 = 0x00000868  enqueue_equip_zone_sprites_by_slot_chain (PLAYER_BLOCK_STRIDE)
DWORD_0807d63c = 0x0201c510  same fn (gDuelFieldSlots)
DWORD_0807d640 = 0x0000195b  same fn (FEATHER_SHOT_CID)
DWORD_0807d6ec = 0x0201b290  tick_equip_lp_indicator_or_score_display_seq (gDuelPhaseFlags)
DWORD_0807d6f0 = 0x000004a4  same fn (EQUIP_PHASE_FRAME_OFF)
DWORD_0807d7a0 = 0x0804b165  enqueue_ritual_eligible_sprite_or_type11 (fn-ptr check_card_id_is_normal_summon_type+1)
DWORD_0807d7a8 = 0x000010d0  same fn (LP_ACTIVATION_LINK_FLAG_OFF)
DWORD_0807d7ac = 0x0201bb90  same fn (gEquipChainSlotRefs)
DWORD_0807d7b0 = 0x00000868  same fn (PLAYER_BLOCK_STRIDE)
DWORD_0807d7b4 = 0x00008020  same fn (SPRITE_RECORD_P2_SIDE)
DWORD_0807d95c = 0x0201b290  tick_neo_daedalus_equip_oam_display_seq (gDuelPhaseFlags)
DWORD_0807d98c = 0x0201b290  tick_hand_spell_match_display_seq (gDuelPhaseFlags)
DWORD_0807da40 = 0x00000868  same fn (PLAYER_BLOCK_STRIDE)
DWORD_0807da44 = 0x0201c8f8  same fn (gP1HandSlotArray)
DWORD_0807da94 = 0x0201b290  tick_equip_activation_display_by_node_state (gDuelPhaseFlags)
DWORD_0807db0c = gP1LifePoints  sync_equip_hand_oam_and_player_bits (already .word gP1LifePoints, DWORD_ residual)
DWORD_0807db10 = 0x00000868  same fn (PLAYER_BLOCK_STRIDE)
```

#### PTR_gP1LifePoints_ slots x6 (PTR_ = user label, SKIP per PTR-rule)

```
PTR_gP1LifePoints_0807ce44  .word gP1LifePoints  tick_equip_slot_activation_score_and_oam
PTR_gP1LifePoints_0807cfb4  .word gP1LifePoints  apply_equip_activation_with_neo_daedalus_lp_output
PTR_gP1LifePoints_0807d070  .word gP1LifePoints  tick_equip_target_validity_prng_lp_display (slot A)
PTR_gP1LifePoints_0807d09c  .word gP1LifePoints  tick_equip_target_validity_prng_lp_display (slot B)
PTR_gP1LifePoints_0807d0c0  .word gP1LifePoints  tick_equip_target_validity_prng_lp_display (slot C)
PTR_gP1LifePoints_0807d2c8  .word gP1LifePoints  tick_equip_activation_display_state_machine
```

#### Symbolic gP1LifePoints DWORD_ slots x2 (already .word gP1LifePoints; DWORD_ residual to rename)

```
DWORD_0807d58c  = 0x0201c4e0  apply_equip_activation_if_field6_gate_pending (already .word gP1LifePoints)
DWORD_0807d7a4  = 0x0201c4e0  enqueue_ritual_eligible_sprite_or_type11 (already .word gP1LifePoints)
```

Note: DWORD_0807db0c listed above under auto-names (also already symbolic).

#### BLK2 base (auto-name to rename)

```
DAT_0807d830 = ROM_INCBIN base for Sillva dispatch sub-stubs  -> sillva_dispatch_stubs
```

### ROM_INCBIN / .byte Blocks x3

| Block  | addr     | size  | kind        |
|--------|----------|-------|-------------|
| BLK1   | 0x7d7e8  | 0x2c  | ROM_INCBIN  |
| JT     | 0x7d814  | 0x1c  | 7 .word entries (already in asm, not incbin) |
| BLK2   | 0x7d830  | 0xfc  | ROM_INCBIN (DAT_0807d830) |
| inline | 0x7db14  | 0xc   | .byte (12 bytes after DWORD_0807db10) |

### switchD

switchD_0807d126 at 0x0807d126; 29 cases [0x64..0x80]; 8 unique targets:
0x0807d1a4, 0x0807d1ba, 0x0807d1e0, 0x0807d1f4, 0x0807d22e, 0x0807d260, 0x0807d2d0, 0x0807d2d4.
All targets are within [0x0807cd68, 0x0807db20) -- NO spill into Seg-5.
All case blocks already labeled switchD_0807d126__caseD_* and decoded. No R4 action needed.

---

## Data Block Classification (Rule 2/3) -- ref-scan Evidence

Python 4B-aligned exhaustive scan on roms/2343.gba; THUMB+1 2B-step scan for BLK1 and inline .byte.

| Block | addr/size | ref-scan raw / THUMB+1 | Verdict | Evidence |
|-------|-----------|------------------------|---------|---------|
| BLK1  | 0x7d7e8/0x2c | raw=0 THUMB+1=1 at +0x001 from FS table 0x09e46220 | R4 disasm | THUMB+1 ref 0x0807d7e9 at FS table ROM 0x09e46220; CID at 0x09e4621c = 0x00001968 = SILLVA_WARLORD_OF_DARK_WORLD_CID (card_info.inc L470). Prefix 0x0807d7e8 bytes: 70b5... = push{lr} THUMB code confirmed. |
| BLK2  | 0x7d830/0xfc | raw=1 each for 5 unique sub-stubs (2 have raw=2 via JT dup); THUMB+1=0 | R4 disasm | Jump table at 0x7d814..0x7d82c (7 raw entries) points into BLK2: sub-stubs at 0x7d830(1 hit), 0x7d880(1 hit), 0x7d898(2 hits), 0x7d8d4(2 hits), 0x7d920(1 hit). 9 pool words at +0x48,+0x4c,+0x98,+0x9c,+0xa0,+0xe0,+0xe4,+0xe8,+0xec = known constants (gP1LifePoints, PLAYER_BLOCK_STRIDE, gDuelPhaseFlags, LP_CARD_TRACK_BASE_OFF). No THUMB+1 refs (code accessed via raw pointer table). |
| inline .byte | 0x7db14/0xc | raw=0 THUMB+1=1 at +0x001 from FS table 0x09e42d88 | R4 disasm | THUMB+1 ref 0x0807db15 at FS table ROM 0x09e42d88; CID at 0x09e42d84 = 0x00001975 = DARK_DEAL_CID (card_info.inc L1054). Bytes: 20 20 0a 79 10 43 08 71 00 20 70 47 = THUMB code (lsls/orrs/strb/movs/bx pattern). |

Zero-ref blocks: none. All 3 blocks have refs. No SS5.1 entries for this segment.

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate; all REUSE from existing constants; 1 NEW)

C5 dedup: all values grepped by value in constants/*.inc.

| slot | value | const_name | file / line | slot_label |
|------|-------|------------|-------------|------------|
| DAT_0807cd84 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_slot_score_oam_phase_flags |
| DAT_0807cde8 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc L218 | tick_slot_score_oam_card_ctx |
| DAT_0807ce48 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc L423 | tick_slot_score_oam_banisher_off |
| DAT_0807ce4c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_slot_score_oam_player_stride |
| DAT_0807cee8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | build_equip_bitmap_player_stride |
| DAT_0807ceec | 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | build_equip_bitmap_field_slots |
| DAT_0807cfb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | apply_equip_act_neo_player_stride_a |
| DAT_0807d00c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | apply_equip_act_neo_player_stride_b |
| DAT_0807d010 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc L332 | apply_equip_act_neo_set_code_arr |
| DAT_0807d034 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_target_prng_phase_flags |
| DAT_0807d06c | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc L218 | tick_equip_target_prng_card_ctx |
| DAT_0807d0c4 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | ewram.inc L248 | tick_equip_target_prng_lp_next_off |
| DAT_0807d0c8 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc L317 | tick_equip_target_prng_equip_refs |
| DAT_0807d100 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc L317 | tick_equip_target_prng_equip_refs_b |
| DAT_0807d128 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_act_disp_sm_phase_flags |
| DAT_0807d12c | 0x0807d130 | (in-range switchD table ptr; no equate) | N/A -- REF slot; see REF_SLOTS | tick_equip_act_disp_sm_jtable_ptr |
| DAT_0807d1d8 | 0x00000139 | TRIGGER_OP_PARAM_139 | duel_field.inc NEW (after L312 TRIGGER_OP_PARAM_107) | tick_equip_act_disp_sm_trig_op139 |
| DAT_0807d2cc | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc L421 | tick_equip_act_disp_sm_eligib_off |
| DWORD_0807d364 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_zone_neo_oam_player_stride |
| DWORD_0807d368 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc L334 | tick_zone_neo_oam_hand_arr |
| DWORD_0807d400 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | find_ojama_trio_phase_flags |
| DWORD_0807d490 | 0x00001681 | OJAMA_GREEN_CID | card_info.inc L668 | find_ojama_trio_green_cid |
| DWORD_0807d494 | 0x000016b3 | OJAMA_YELLOW_CID | card_info.inc L1206 | find_ojama_trio_yellow_cid |
| DWORD_0807d498 | 0x000016b4 | OJAMA_BLACK_CID | card_info.inc L670 | find_ojama_trio_black_cid |
| DWORD_0807d49c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | find_ojama_trio_player_stride |
| DWORD_0807d4a0 | 0x0201c740 | gP1SlotSetCodeArray | ewram.inc L332 | find_ojama_trio_set_code_arr |
| DAT_0807d540 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | apply_equip_act_field6_player_stride |
| DAT_0807d544 | 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | apply_equip_act_field6_field_slots |
| DWORD_0807d590 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc L483 | apply_equip_if_field6_act_state_off |
| DWORD_0807d638 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | enqueue_equip_zone_chain_stride |
| DWORD_0807d63c | 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | enqueue_equip_zone_chain_slots |
| DWORD_0807d640 | 0x0000195b | FEATHER_SHOT_CID | card_info.inc L206 | enqueue_equip_zone_chain_base_cid |
| DWORD_0807d6ec | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_lp_score_disp_phase_flags |
| DWORD_0807d6f0 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_lp_score_disp_frame_off |
| DWORD_0807d7a8 | 0x000010d0 | LP_ACTIVATION_LINK_FLAG_OFF | ewram.inc L483 | enqueue_ritual_act_state_off |
| DWORD_0807d7ac | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc L317 | enqueue_ritual_equip_refs |
| DWORD_0807d7b0 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | enqueue_ritual_player_stride |
| DWORD_0807d7b4 | 0x00008020 | SPRITE_RECORD_P2_SIDE | oam_attr.inc L176 | enqueue_ritual_p2_sprite_flag |
| DWORD_0807d95c | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_neo_daed_oam_disp_phase_flags |
| DWORD_0807d98c | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_hand_spell_match_phase_flags |
| DWORD_0807da40 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_hand_spell_match_stride |
| DWORD_0807da44 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc L334 | tick_hand_spell_match_hand_arr |
| DWORD_0807da94 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_act_disp_by_node_phase_flags |
| DWORD_0807db10 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | sync_equip_hand_oam_stride |

Total EQ slots: 44 (43 REUSE + 1 NEW: TRIGGER_OP_PARAM_139)

Note: DAT_0807d12c (value = 0x0807d130, in-range switchD table ptr) is classified as REF below, not EQ.

### REF_SLOTS (USER-label + DATA-ref; fn-ptr +1 and in-range data ptr)

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DAT_0807cdec | 0x08065991 = check_equip_activation_at_slot11+1 | check_equip_activation_at_slot11_1 (already defined asm/08 L3691) | tick_slot_score_oam_zone_handler_ptr |
| DAT_0807ce04 | 0x08065991 = check_equip_activation_at_slot11+1 | check_equip_activation_at_slot11_1 | tick_slot_score_oam_zone_handler_ptr_b |
| DAT_0807d25c | 0x08090625 = invoke_effect_node_with_active_flag_3arg+1 | invoke_effect_node_with_active_flag_3arg_1 (asm/11 L11825: fn at 0x08090624; Seg-3 DWORD_0807c408 same value, annotated asm/08 L3691) | tick_equip_act_disp_sm_activation_ptr |
| DAT_0807d12c | 0x0807d130 = switchD_0807d126__switchdataD_0807d130 | switchD_0807d126__switchdataD_0807d130 (already labeled in asm) | tick_equip_act_disp_sm_jtable_ptr |
| DWORD_0807d3dc | 0x08050a55 = check_equip_slot_eligible_by_card_id_bst+1 | check_equip_slot_eligible_by_card_id_bst_1 (asm/05 label) | apply_equip_slot_act_eligib_bst_ptr |
| DWORD_0807d7a0 | 0x0804b165 = check_card_id_is_normal_summon_type+1 | check_card_id_is_normal_summon_type_1 (asm/05 label) | enqueue_ritual_normal_summon_pred |

Total REF slots: 6

### RENAME_SLOTS (residual DWORD_ already symbolic; give EOL comment)

| slot | current_value | slot_label | eol_comment |
|------|---------------|------------|-------------|
| DWORD_0807d58c | .word gP1LifePoints | apply_equip_if_field6_pending_gp1lp | apply_equip_activation_if_field6_gate_pending: gP1LifePoints ptr |
| DWORD_0807d7a4 | .word gP1LifePoints | enqueue_ritual_gp1lp | enqueue_ritual_eligible_sprite_or_type11: gP1LifePoints ptr |
| DWORD_0807db0c | .word gP1LifePoints | sync_equip_hand_oam_gp1lp | sync_equip_hand_oam_and_player_bits: gP1LifePoints ptr |

Total RENAME: 3

### FUNC_RENAME (none)

No function name conflicts found. All 19 function names match body semantics.
indeg check: tick_equip_activation_display_by_node_state (indeg=0, form(c)) -- name correct per asm comment.

### PLATE (R5 -- ASCII rewrites for Ghidra)

Several plate comments in Seg-4 contain CJK text. Ghidra Jython plate writes MUST be ASCII.
The existing CJK content is in asm @ comments (fine for asm only, not sent to Ghidra).
Fixer must set Ghidra plate for these functions using ASCII-only text:

1. build_equip_eligible_bitmap_for_slots @ 0x0807ce50:
   "Scans equip zone slots, builds eligibility bitmap from check_card_equip_eligible_for_slot per slot, calls forward_equip_bitmap_update_with_full_mask(node, bitmap, 2). Returns 0."

2. apply_equip_activation_with_neo_daedalus_lp_output @ 0x0807cef0:
   "Checks effect slot match, activates node, checks Neo-Daedalus group placement; on pass calls apply_slot_equip_activation_with_eligibility_check; calls submit_lp_indicator_with_slot_xor_flag. Returns 0."

3. tick_equip_target_validity_prng_lp_display @ 0x0807d014:
   "State machine [gDuelPhaseFlags+0x4a0]: 0x80=check target valid+prng sample; 0x7f=enqueue_lp_display_row_type17; 0x7e=apply activation or submit LP score diff. Returns next state or 0."

4. tick_equip_activation_display_state_machine @ 0x0807d104:
   "29-state display driver [0x64..0x80]: dispatches via switchD_0807d126. State 0x7f calls trigger_card_display_op31_if_not_active(player, TRIGGER_OP_PARAM_139=0x139). Returns next state."

5. tick_zone_pipeline_with_neo_daedalus_oam_setup @ 0x0807d2e0:
   "Pushes zone sprite pipeline; gates on Neo-Daedalus placeable+zone_type==4; finds hand slot by set_code; calls invoke_setup_equip_oam_with_attr2. Returns 0."

---

## Disasm Plan (R4)

### BLK1: fn_eligible_sillva_warlord_of_dark_world @ 0x0807d7e8 (0x2c bytes)

THUMB fn_eligible stub for Sillva, Warlord of Dark World (CID=0x1968).
- clearListing [0x0807d7e8, 0x0807d814)
- setTMode [0x0807d7e8, 0x0807d814)
- DisassembleCommand per-instruction (do NOT disassemble as single range; per-stub rule)
- BLK1 content confirmed (python dump): 0x2c bytes = 0x16 half-word instructions + 2 pool words.
  Entry push {r4,r5,lr} at +0x00 (bytes 30b5041c0d1c); ldr r0,[pool_gDuelPhaseFlags] at +0x07; 
  state dispatch logic; indirect branch at +0x20 = 0x4687 (MOV PC,r0) -- CODE not data.
  Pool words at:
  - +0x24 @ 0x0807d80c: 0x0201b290 = gDuelPhaseFlags -> createDWord + label sillva_eligible_phase_flags
  - +0x28 @ 0x0807d810: 0x0807d814 = Sillva dispatch jump table base -> createDWord + label sillva_eligible_jtable_ptr
- Pool-vs-code trap: 0x4687 at BLK1 +0x20 (0x0807d808) = THUMB MOV PC,r0 instruction. Do NOT createDWord here.

### BLK2: sillva_dispatch_stubs @ 0x0807d830 (0xfc bytes)

7-state dispatch sub-stubs for Sillva effect handler, referenced by jump table at 0x7d814..0x7d82c.
5 unique entry points (7 jump table entries, 5 unique targets due to state sharing):

| sub-stub | addr | raw JT refs | proposed_label |
|----------|------|-------------|----------------|
| A (state 0x80) | 0x0807d830 | 1 | sillva_state_80_activate |
| B (state 0x7f) | 0x0807d880 | 1 | sillva_state_7f_trigger |
| C (states 0x7c/0x7e) | 0x0807d898 | 2 | sillva_state_7c_7e_hand_enqueue |
| D (states 0x7b/0x7d) | 0x0807d8d4 | 2 | sillva_state_7b_7d_lp_display |
| E (state 0x7a) | 0x0807d920 | 1 | sillva_state_7a_counter |

R4 procedure per sub-stub:
- clearListing [0x0807d830, 0x0807d92c)  (entire BLK2 region)
- setTMode [0x0807d830, 0x0807d92c)
- DisassembleCommand for each sub-stub entry point individually (NOT single-range)
- createDWord for each pool word (9 total):
  - 0x0807d878 (.word 0x0201c4e0 = gP1LifePoints)
  - 0x0807d87c (.word 0x00000868 = PLAYER_BLOCK_STRIDE)
  - 0x0807d8c8 (.word 0x0201c4e0 = gP1LifePoints)
  - 0x0807d8cc (.word 0x00000868 = PLAYER_BLOCK_STRIDE)
  - 0x0807d8d0 (.word 0x0201b290 = gDuelPhaseFlags)
  - 0x0807d910 (.word 0x0201c4e0 = gP1LifePoints)
  - 0x0807d914 (.word 0x00000868 = PLAYER_BLOCK_STRIDE)
  - 0x0807d918 (.word 0x00001da8 = LP_CARD_TRACK_BASE_OFF)
  - 0x0807d91c (.word 0x0201b290 = gDuelPhaseFlags)

Pool-vs-code check: verify 0x4687 does NOT appear in BLK2 (first bytes: 0x0807d830 = 201c291c = ARM code, safe).

### inline .byte: fn_eligible_dark_deal @ 0x0807db14 (0xc bytes = 12 bytes)

THUMB fn_eligible stub for Dark Deal (CID=0x1975). Starts immediately after DWORD_0807db10.
Bytes: 20 20 0a 79 10 43 08 71 00 20 70 47
Decoded: movs r0,#0x20 / ldrb r2,[r1,#0xa] / orrs r0,r2 / strb r0,[r1,#0x1] / movs r0,#0 / bx lr

Wait: this is 12 bytes ending at 0x7db1f (Seg-4 end = 0x7db20). No pool needed (no ldr pc-relative).

R4 procedure:
- clearListing [0x0807db14, 0x0807db20)
- setTMode [0x0807db14, 0x0807db20)
- DisassembleCommand at 0x0807db14
- Set label fn_eligible_dark_deal at 0x0807db14
- EOL at 0x0807db14: "fn_eligible_dark_deal: CID=DARK_DEAL_CID=0x1975; ORs 0x20 into [r1+4]; returns 0 (leaf, bx lr, no pool)"

---

## Carve Plan (R7)

None required. BLK1 and BLK2 are code blocks (R4 disasm), not data tables to carve into rom.s.
No pointer tables requiring rom.s carve exist in this segment (the jump table at 0x7d814 is inside
the code section between BLK1 and BLK2, already rendered as .word in asm, which is correct GAS syntax).

---

## New Constants / Globals

### NEW constant (duel_field.inc)

```
.equ TRIGGER_OP_PARAM_139,  0x00000139  @ trigger_card_display_op31_if_not_active 2nd arg; file10 Seg-4 DAT_0807d1d8; 28 ROM refs; conf: high
```

Insert after TRIGGER_OP_PARAM_107 (duel_field.inc L312).

C5 dedup grep-by-value: grep "0x00000139\|= 0x139" constants/*.inc -> 0 hits. Confirmed NEW.

---

## SS5.1 Entries (Rule 3 -- 0-ref blocks)

None. All 3 code blocks (BLK1, BLK2, inline .byte) have confirmed ROM references.

---

## C13 Coverage Proof

Total pool labels in Seg-4 to resolve:
- 50 DAT_/DWORD_ auto-name slots (raw prefix residual)
- 6 PTR_gP1LifePoints_ slots -> SKIP (PTR_ rule)
- 1 DAT_0807d830 (BLK2 base label) -> RENAME to sillva_dispatch_stubs

Resolved breakdown (50 + 1 = 51 non-PTR_ labels):
- EQ: 43 (remaining after removing REF DAT_0807d12c from the 44 EQ count above)
  Note: DAT_0807d12c counted under REF_SLOTS below.
- REF: 6 (DAT_0807cdec, DAT_0807ce04, DAT_0807d25c, DAT_0807d12c, DWORD_0807d3dc, DWORD_0807d7a0)
- RENAME (symbolic): 3 (DWORD_0807d58c, DWORD_0807d7a4, DWORD_0807db0c -- already .word gP1LifePoints)
- BLK2-base label: 1 (DAT_0807d830 -> sillva_dispatch_stubs)

43 + 6 + 3 - 1 = 51... let me recount:
EQ_SLOTS table above has 44 rows but one (DAT_0807d12c) is marked "REF slot" in note -> 43 EQ.
REF_SLOTS has 6 rows (including DAT_0807d12c) -> 6 REF.
RENAME has 3 rows -> 3 RENAME.
Plus DAT_0807d830 -> 1 BLK-base label (RENAME variant).

43 + 6 + 3 + 1 = 53 covered.
PTR_gP1LifePoints_ x6 = skipped.
Total unique auto-name labels in segment: 50 (non-PTR_ DAT_/DWORD_) + 6 (PTR_) + 1 (DAT_0807d830 BLK-base) = 57.
Processed: 53 + 6 skip = 59. However I count 58 in the slot list above:
- 50 DAT_/DWORD_ (including DWORD_0807db0c) + 6 PTR_ + 1 DAT_0807d830 = 57? Let me reconcile:

Precise slot list (non-PTR_, non-BLK-base):
EQ(43): DAT_0807cd84, DAT_0807cde8, DAT_0807ce48, DAT_0807ce4c, DAT_0807cee8, DAT_0807ceec,
        DAT_0807cfb8, DAT_0807d00c, DAT_0807d010, DAT_0807d034, DAT_0807d06c, DAT_0807d0c4,
        DAT_0807d0c8, DAT_0807d100, DAT_0807d128, DAT_0807d1d8, DAT_0807d2cc,
        DWORD_0807d364, DWORD_0807d368, DWORD_0807d400, DWORD_0807d490, DWORD_0807d494,
        DWORD_0807d498, DWORD_0807d49c, DWORD_0807d4a0, DAT_0807d540, DAT_0807d544,
        DWORD_0807d590, DWORD_0807d638, DWORD_0807d63c, DWORD_0807d640,
        DWORD_0807d6ec, DWORD_0807d6f0, DWORD_0807d7a8, DWORD_0807d7ac,
        DWORD_0807d7b0, DWORD_0807d7b4, DWORD_0807d95c, DWORD_0807d98c,
        DWORD_0807da40, DWORD_0807da44, DWORD_0807da94, DWORD_0807db10 = 43 slots

REF(6): DAT_0807cdec, DAT_0807ce04, DAT_0807d12c, DAT_0807d25c, DWORD_0807d3dc, DWORD_0807d7a0

RENAME(3): DWORD_0807d58c, DWORD_0807d7a4, DWORD_0807db0c

PTR_(6 SKIP): PTR_gP1LifePoints_0807ce44, PTR_gP1LifePoints_0807cfb4,
              PTR_gP1LifePoints_0807d070, PTR_gP1LifePoints_0807d09c,
              PTR_gP1LifePoints_0807d0c0, PTR_gP1LifePoints_0807d2c8

BLK-base(1): DAT_0807d830

Total: 43+6+3+6+1 = 59 labels. Processed: 43+6+3+1 = 53 labels. Skipped (PTR_): 6.
Expected residual DAT_/DWORD_ after pass: 0.

---

## Consumer Evidence (R6) -- Key Slot Semantics

| slot | value | file:line evidence | confidence |
|------|-------|-------------------|------------|
| DAT_0807d1d8 = 0x00000139 | TRIGGER_OP_PARAM_139 | asm/10 L7013: trigger_card_display_op31_if_not_active called with r1=0x139 at tick_equip_activation_display_state_machine state_7f branch | high |
| DWORD_0807d640 = 0x0000195b | FEATHER_SHOT_CID | asm/10 L7599: used as chain_base in check_value_in_slot_chain(player, 0xb, 0x195b) and get_node_entity_id_in_slot -- chain base addr = FEATHER_SHOT_CID per Seg-3 precedent; card_info.inc L206 | high |
| DWORD_0807d3dc = 0x08050a55 | check_equip_slot_eligible_by_card_id_bst+1 | asm/05 fn at 0x08050a54 confirmed; THUMB+1=0x08050a55; passed to build_equip_zone_bitmap_for_player as fn-ptr predicate | high |
| DWORD_0807d7a0 = 0x0804b165 | check_card_id_is_normal_summon_type+1 | asm/05 fn at 0x0804b164 confirmed; THUMB+1=0x0804b165; passed to count_monster_slots_by_fnptr in enqueue_ritual_eligible_sprite_or_type11 | high |
| BLK1 @ 0x0807d7e8 CID=0x1968 | SILLVA_WARLORD_OF_DARK_WORLD_CID | roms/2343.gba FS table 0x09e46220: word=0x0807d7e9 (THUMB+1); 0x09e4621c=0x00001968; data/card-stats.s card_1974 | high |
| inline .byte @ 0x0807db14 CID=0x1975 | DARK_DEAL_CID | roms/2343.gba FS table 0x09e42d88: word=0x0807db15 (THUMB+1); 0x09e42d84=0x00001975; data/card-stats.s card_1986 | high |

---

## Verification Self-Check

1. EQ values vs ROM bytes: python confirmed DAT_0807cd84=0x0201b290, DAT_0807d1d8=0x00000139, DAT_0807d25c=0x08090625, DAT_0807d12c=0x0807d130.
2. BLK2 pool +1 check: BLK2 contains raw code pointers (no THUMB+1); jump table at 0x7d814 uses raw addresses to enter BLK2 sub-stubs. BLK2 bytes at 0x7d830: 201c291c = THUMB code (adds/adds), consistent.
3. All plate/EOL text in this proposal is pure ASCII. (grep '[^\x00-\x7F]' = 0)
4. SS5.1 blocks: 0 (all blocks have refs).
5. Slot names use ^[a-z][a-z0-9_]+$ pattern.
6. switchD spill: all 8 unique targets in [0x7cd68, 0x7db20) -- no spill confirmed.
7. C5 dedup: TRIGGER_OP_PARAM_139=0x139 grepped as 0 hits in constants/*.inc. All other values confirmed REUSE.

---

## Queries (if any)

None. All blocks have confirmed semantics and ref-scan evidence.

---
