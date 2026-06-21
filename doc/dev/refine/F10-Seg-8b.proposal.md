# Refine Proposal: F10-Seg-8b  [0x08082b18..0x08083450)

**Split context**: Seg-8 (113 slots, 2 ROM_INCBIN) split at 0x08082b18. Seg-8b = [0x08082b18..0x08083450). 12 fns, 67 slot defs (3 PTR_gP1LifePoints_ skipped per scope convention), 0 ROM_INCBIN.

---

## Segment Survey

### Function Entries in [0x08082b18, 0x08083450)

| addr | name | asm line |
|------|------|----------|
| 0x08082b18 | invoke_effect_node_handler_if_slot_in_range | L19057 |
| 0x08082b2c | invoke_effect_node_handler_if_slot_type_ok | L19080 (approx) |
| 0x08082b5c | invoke_effect_node_handler_if_slot_whitelisted | L19110 (approx) |
| 0x08082b88 | tick_equip_display_with_fn_ptr_routing_3state | L19140 |
| 0x08082c8c | build_equip_chain_pair_slot_entry | L19289 |
| 0x08082d0c | tick_equip_chain_pair_display_4state | L19353 |
| 0x08082e98 | tick_equip_lp_display_by_node_state | L19640 (approx) |
| 0x08082f44 | tick_equip_display_by_card_id_group_b_3state | L19658 |
| 0x08083170 | tick_equip_lp_display_by_node_state_4state | L19980 |
| 0x08083280 | advance_equip_slot_display_state | L20170 (approx) |
| 0x080833a8 | dispatch_equip_display_if_confirm_state_one | L20295 |
| 0x080833bc | enqueue_equip_slot_sprites_for_pair_loop | L20309 |

### Residual Auto-Name Slots in Seg-8b (67 total; 3 PTR_ skipped; 64 actionable)

```
L19167: DWORD_08082ba8  .word 0x0000140a          [CID]
L19174: DWORD_08082bb4  .word 0x00001719          [CID]
L19179: DWORD_08082bbc  .word 0x08082b19          [fn-ptr RENAME]
L19184: DWORD_08082bc4  .word 0x08082b2d          [fn-ptr RENAME]
L19202: DWORD_08082be4  .word 0x08082b5d          [fn-ptr RENAME]
L19204: DWORD_08082be8  .word 0x0201b290
L19239: DWORD_08082c30  .word 0x00000484
L19260: DWORD_08082c5c  .word gP1LifePoints        [already symbolic]
L19262: DWORD_08082c60  .word 0x00001d68
L19276: DWORD_08082c78  .word 0x00000484
L19340: DWORD_08082cf8  .word 0x0000ffff
L19381: DWORD_08082d2c  .word 0x0201b290
L19408: DWORD_08082d60  .word 0x080905e9           [fn-ptr EQ - same as Seg-8a new const]
L19455: DWORD_08082dbc  .word 0x08082c8d           [fn-ptr RENAME]
L19457: DWORD_08082dc0  .word 0x0201e2a0
L19502: DWORD_08082e20  .word 0x00000868
L19504: DWORD_08082e24  .word 0x0201c510
L19531: DWORD_08082e5c  .word gP1LifePoints        [already symbolic]
L19533: DWORD_08082e60  .word 0x00001d68
L19535: DWORD_08082e64  .word 0x00001d6c
L19537: DWORD_08082e68  .word 0x0201b290
L19551: DWORD_08082e80  .word 0x0201b290
L19582: DAT_08082eb4    .word 0x0201b290
L19605: DAT_08082ee0    .word 0xfffc7fff
L19622: PTR_gP1LifePoints_08082f04 .word gP1LifePoints  [SKIP per scope]
L19624: DAT_08082f08    .word 0x00001da8
L19645: DAT_08082f30    .word 0x00001357           [CID]
L19647: PTR_gP1LifePoints_08082f34 .word gP1LifePoints  [SKIP per scope]
L19649: DAT_08082f38    .word 0x00001da8
L19708: DAT_08082f7c    .word 0x000016d6           [CID]
L19710: DAT_08082f80    .word 0x000014e7           [CID]
L19712: DAT_08082f84    .word 0x00001359           [CID]
L19719: DAT_08082f90    .word 0x0000149e           [CID]
L19732: DAT_08082fa8    .word 0x00001630           [CID]
L19739: DAT_08082fb4    .word 0x000016a8           [CID]
L19754: DAT_08082fd0    .word 0x000017f7           [CID]
L19759: DAT_08082fd8    .word 0x000017f1           [CID]
L19772: DAT_08082ff0    .word 0x0000196f           [CID]
L19774: DAT_08082ff4    .word 0x00001864           [CID]
L19782: DAT_08083000    .word 0x00001974           [CID]
L19793: DAT_08083010    .word 0x0000011d           [display op]
L19833: DAT_08083054    .word 0x0000011d           [display op - same val]
L19863: DAT_08083088    .word 0x0201b290
L19898: DAT_080830d0    .word 0xfffc7fff
L19918: DAT_080830f8    .word 0x000004b4
L19957: DAT_0808314c    .word 0x000004b4
L19959: PTR_gP1LifePoints_08083150 .word gP1LifePoints  [SKIP per scope]
L20012: DWORD_0808319c  .word gP1LifePoints        [already symbolic]
L20014: DWORD_080831a0  .word 0x00001ce8
L20016: DWORD_080831a4  .word 0x0201b290
L20018: DWORD_080831a8  .word 0x000004b4
L20038: DWORD_080831cc  .word 0xfffc7fff
L20076: DWORD_0808321c  .word 0x0201b290
L20107: DWORD_0808325c  .word 0x00001da8
L20109: DWORD_08083260  .word 0x00000868
L20150: DWORD_0808329c  .word 0x0201b290
L20175: DWORD_080832cc  .word 0xfffc7fff
L20192: DWORD_080832ec  .word 0x000015de           [CID]
L20194: DWORD_080832f0  .word 0x00001368           [CID]
L20196: DWORD_080832f4  .word 0x00001568           [CID neutral]
L20207: DWORD_08083308  .word 0x000016d3           [CID neutral]
L20215: DWORD_08083314  .word 0x00001803           [CID neutral]
L20252: DWORD_08083358  .word 0x0201b290
L20276: DWORD_08083388  .word gP1LifePoints        [already symbolic]
L20343: DAT_080833f0    .word 0x00000868
L20345: DAT_080833f4    .word 0x0201c8f8
L20347: DAT_080833f8    .word 0x09e3f140
```

Totals: 4 already-symbolic gP1LifePoints (RENAME), 3 PTR_ (SKIP), 4 fn-ptr (RENAME), 56 EQ/REF.

---

## Data Block Classification (Rule 2/3)

No ROM_INCBIN blocks in Seg-8b. Not applicable.

---

## Symbolization Plan

### EQ_SLOTS (data-equate)

**REUSE existing constants (C5 grep by VALUE -> hit):**

| slot | value | const_name | grep evidence |
|------|-------|-----------|---------------|
| DWORD_08082be8 L19204 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_08082c30 L19239 | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc:364 |
| DWORD_08082c60 L19262 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc:422 |
| DWORD_08082c78 L19276 | 0x00000484 | EQUIP_ACTIVE_CTX_OFF | duel_field.inc:364 |
| DWORD_08082cf8 L19340 | 0x0000ffff | LP_ROW_TYPE8_ALL_SLOTS_MASK | duel_field.inc:394 |
| DWORD_08082d2c L19381 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_08082d60 L19408 | 0x080905e9 | set_equip_activation_state_by_mode_alt_fn_ptr | NEW in Seg-8a; same const (3rd occurrence) |
| DWORD_08082dc0 L19457 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 |
| DWORD_08082e20 L19502 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 |
| DWORD_08082e24 L19504 | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 |
| DWORD_08082e60 L19533 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc:422 |
| DWORD_08082e64 L19535 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc:423 |
| DWORD_08082e68 L19537 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_08082e80 L19551 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DAT_08082eb4 L19582 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DAT_08082ee0 L19605 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DAT_08082f08 L19624 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc:247 |
| DAT_08082f38 L19649 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc:247 |
| DAT_08083088 L19863 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DAT_080830d0 L19898 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DAT_080830f8 L19918 | 0x000004b4 | EQUIP_ACTIVATION_AUX_OFF | duel_field.inc:357 |
| DAT_0808314c L19957 | 0x000004b4 | EQUIP_ACTIVATION_AUX_OFF | duel_field.inc:357 |
| DWORD_080831a4 L20016 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_080831a8 L20018 | 0x000004b4 | EQUIP_ACTIVATION_AUX_OFF | duel_field.inc:357 |
| DWORD_080831cc L20038 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_0808321c L20076 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_0808325c L20107 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc:247 |
| DWORD_08083260 L20109 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 |
| DWORD_0808329c L20150 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_080832cc L20175 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_08083358 L20252 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DAT_080833f0 L20343 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 |
| DAT_080833f4 L20345 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc:334 |

**CID slots - REUSE (C5 grep by VALUE -> hit):**

| slot | value | const_name | evidence |
|------|-------|-----------|---------|
| DWORD_08082ba8 L19167 | 0x0000140a | (no existing SHIFT_CID) | card_info.inc grep "0x0000140a" = 0 hits -> NEW |
| DAT_08082f30 L19645 | 0x00001357 | DNA_SURGERY_CID | card_info.inc:391 (value hit) |
| DAT_08082fb4 L19739 | 0x000016a8 | RAY_OF_HOPE_CID | card_info.inc grep "0x000016a8" -> hit |
| DAT_08082fd8 L19759 | 0x000017f1 | DARK_FACTORY_MASS_PROD_CID | card_info.inc grep "0x000017f1" -> hit |
| DAT_08082ff4 L19774 | 0x00001864 | BEHEMOTH_KING_CID | card_info.inc grep "0x00001864" -> hit |
| DAT_08082ff0 L19772 | 0x0000196f | POT_OF_AVARICE_CID | card_info.inc grep "0x0000196f" -> hit |
| DWORD_080832ec L20192 | 0x000015de | equip_cid_15de_08048a68 | card_info.inc:600 grep "0x000015de" -> hit |
| DWORD_080832f0 L20194 | 0x00001368 | SPELL_ZONE_TARGET_CARD_ID | card_info.inc:147 grep "0x00001368" -> hit |

**CID slots - NEW (C5 grep by VALUE -> 0 hits):**

| slot | value | proposed name | evidence |
|------|-------|--------------|---------|
| DWORD_08082ba8 L19167 | 0x0000140a | SHIFT_CID | card_info.inc grep "0x0000140a"=0 hits; card-stats.s card_0885 "Shift" pw=59560625; asm/10 L19140 plate names this CID explicitly; conf: high |
| DWORD_08082bb4 L19174 | 0x00001719 | FIENDS_HAND_MIRROR_CID | card_info.inc grep "0x00001719"=0 hits; card-stats.s card_1489 "Fiend's Hand Mirror" pw=58607704; asm/10 L19140 plate; conf: high |
| DAT_08082f7c L19708 | 0x000016d6 | PRIMAL_SEED_CID | card_info.inc grep "0x000016d6"=0 hits; card-stats.s card_1431 "Primal Seed" pw=23701465; conf: high |
| DAT_08082f80 L19710 | 0x000014e7 | KELDO_CID | card_info.inc grep "0x000014e7"=0 hits; card-stats.s card_1047 "Keldo" pw=80441106; conf: high |
| DAT_08082f84 L19712 | 0x00001359 | BACKUP_SOLDIER_CID | card_info.inc grep "0x00001359"=0 hits; card-stats.s card_0762 "Backup Soldier" pw=36280194; conf: high |
| DAT_08082f90 L19719 | 0x0000149e | MIRACLE_DIG_CID | card_info.inc grep "0x0000149e"=0 hits; card-stats.s card_0988 "Miracle Dig" pw=06343408; conf: high |
| DAT_08082fa8 L19732 | 0x00001630 | HIDDEN_BOOK_OF_SPELL_CID | card_info.inc grep "0x00001630"=0 hits; card-stats.s card_1297 "Hidden Book of Spell" pw=21840375; conf: high |
| DAT_08082fd0 L19754 | 0x000017f7 | GRAVEYARD_IN_FOURTH_DIMENSION_CID | card_info.inc grep "0x000017f7"=0 hits; card-stats.s card_1668 "The Graveyard in the Fourth Dimension" pw=88089103; conf: high |
| DAT_08083000 L19782 | 0x00001974 | FORCES_OF_DARKNESS_CID | card_info.inc grep "0x00001974"=0 hits; card-stats.s card_1985 "The Forces of Darkness" pw=29826127; conf: high |

**CID slots - NEUTRAL (not in card-stats.s -> cid_<hex>):**

| slot | value | proposed name | evidence |
|------|-------|--------------|---------|
| DWORD_080832f4 L20196 | 0x00001568 | cid_1568 | card_info.inc grep=0; card-stats.s: no slot 0x1568 found (slot range checked 0x1560..0x1570 = unassigned); conf: high (unassigned) |
| DWORD_08083308 L20207 | 0x000016d3 | cid_16d3 | card_info.inc grep=0; card-stats.s: no slot 0x16d3 found; conf: high (unassigned) |
| DWORD_08083314 L20215 | 0x00001803 | cid_1803 | card_info.inc grep=0; card-stats.s: no slot 0x1803 found; conf: high (unassigned) |

**Other NEW EQ constants:**

| slot | value | proposed name | evidence |
|------|-------|--------------|---------|
| DWORD_080831a0 L20014 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc:276 grep "0x00001ce8" -> hit: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8; REUSE |
| DAT_08083010 L19793 | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB | card_info.inc:1502 grep "0x0000011d" -> hit; REUSE |
| DAT_08083054 L19833 | 0x0000011d | CARD_DISPLAY_OP31_LP_BAR_SUB | same const (2nd occurrence) |
| DAT_080833f8 L20347 | 0x09e3f140 | EQUIP_PAIR_ENTRY_TABLE_BASE | grep constants/*.inc "0x09e3f140"=0 hits; ROM ref count=1; asm/10 L20312 plate "PAIR_TABLE_BASE=0x09e3f140 (ROM pair data table base address)"; base of ROM equip-pair entry table read by enqueue_equip_slot_sprites_for_pair_loop (r7=base, loop r6=0..2, ldr [r7+r6*4]=card_pair_ptr); conf: high |

Wait - P1LP_BLOCK2_OFF_1CE8 is already in ewram.inc. Let me correct the table:

Corrected:
- DWORD_080831a0 L20014: 0x00001ce8 -> REUSE P1LP_BLOCK2_OFF_1CE8 (ewram.inc:276)
- DAT_08083010 L19793: 0x0000011d -> REUSE CARD_DISPLAY_OP31_LP_BAR_SUB (card_info.inc:1502)
- DAT_08083054 L19833: 0x0000011d -> REUSE CARD_DISPLAY_OP31_LP_BAR_SUB (2nd occurrence)
- DAT_080833f8 L20347: 0x09e3f140 -> NEW EQUIP_PAIR_ENTRY_TABLE_BASE

### REF_SLOTS (USER-label + DATA-ref)

No standalone USER-label REF slots in Seg-8b. All globals go through EQ_SLOTS.

### RENAME_SLOTS

**gP1LifePoints already-symbolic (4 slots):**

| slot | label_after | eol |
|------|-------------|-----|
| DWORD_08082c5c L19260 | gP1LifePoints | gP1LifePoints |
| DWORD_08082e5c L19531 | gP1LifePoints | gP1LifePoints |
| DWORD_0808319c L20012 | gP1LifePoints | gP1LifePoints |
| DWORD_08083388 L20276 | gP1LifePoints | gP1LifePoints |

**fn-ptr RENAME slots (4 slots; raw .word values are THUMB+1 fn addresses):**

| slot | stored value | points to fn | slot_label | eol |
|------|-------------|-------------|-----------|-----|
| DWORD_08082bbc L19179 | 0x08082b19 | invoke_effect_node_handler_if_slot_in_range (0x08082b18) | invoke_effect_node_handler_if_slot_in_range_fn_ptr | .word invoke_effect_node_handler_if_slot_in_range+1 |
| DWORD_08082bc4 L19184 | 0x08082b2d | invoke_effect_node_handler_if_slot_type_ok (0x08082b2c) | invoke_effect_node_handler_if_slot_type_ok_fn_ptr | .word invoke_effect_node_handler_if_slot_type_ok+1 |
| DWORD_08082be4 L19202 | 0x08082b5d | invoke_effect_node_handler_if_slot_whitelisted (0x08082b5c) | invoke_effect_node_handler_if_slot_whitelisted_fn_ptr | .word invoke_effect_node_handler_if_slot_whitelisted+1 |
| DWORD_08082dbc L19455 | 0x08082c8d | build_equip_chain_pair_slot_entry (0x08082c8c) | build_equip_chain_pair_slot_entry_fn_ptr | .word build_equip_chain_pair_slot_entry+1 |

Rationale: These are within-segment THUMB fn-ptrs. The label name uses the target function name + `_fn_ptr` suffix for searchability. Keep raw .word (GAS cannot use `fn+1` syntax for forward refs if used before definition, but these targets are all defined before the slots in address order). Actually all 4 targets (0x82b18, 0x82b2c, 0x82b5c, 0x82c8c) appear earlier in Seg-8b code so `.word invoke_effect_node_handler_if_slot_in_range+1` is valid.

### PTR_gP1LifePoints_ slots (SKIP per scope convention):
- PTR_gP1LifePoints_08082f04 L19622 -> SKIP
- PTR_gP1LifePoints_08082f34 L19647 -> SKIP
- PTR_gP1LifePoints_08083150 L19959 -> SKIP

### FUNC_RENAME

None identified in Seg-8b. All 12 named functions have semantically correct names per existing asm plates.

### PLATE (R5)

**Mojibake lines in Seg-8b (lines 19057..20393):**

14 non-ASCII comment lines requiring ASCII plate rewrites:

1. **tick_equip_display_with_fn_ptr_routing_3state** (L19140):
   ASCII rewrite: "Equip display 3-state machine with fn-ptr routing. Receives effect_node_ptr(r0). card_id BST: 0x1327(Fairy's Hand Mirror,computed=0x140a-0xe3), 0x140a(Shift), 0x1719(Fiend's Hand Mirror) each mapped to different display op fn-ptr (loaded into r7). Then reads IWRAM state [IWRAM_BASE+0x4b0]. State 0: clear attr_bits + format_game_text_with_int_arg + trigger + set_equip_activation_state_by_mode, step+1, return 0. State 1: check_activation_display_state_is_confirmed->enqueue_equip_slot_sprite_with_code_rotation, step+1. State 2: write [IWRAM+0x484]:=r5 (store activation slot snapshot), step+1."

2. **build_equip_chain_pair_slot_entry** (L19289):
   ASCII rewrite: "Build equip chain pair slot entry. Receives effect_node_ptr(r0). Reads effect slot side/type via read_effect_slot_side_and_type. Iterates find_equip_chain_pair_slot to locate matching pair entry. Updates entry data fields on match. Returns 1 on match, 0 on no match."

3. **tick_equip_display_by_card_id_group_b_3state** (L19658, 2 comment lines L19658..L19663):
   ASCII rewrite: "Equip display 3-state machine routed by card_id group B. card_id BST dispatches 11 card slots: 0x1359(Backup Soldier), 0x149e(Miracle Dig), 0x14e7(Keldo), 0x1630(Hidden Book of Spell), 0x16a8(Ray of Hope), 0x16d6(Primal Seed), 0x17f1(Dark Factory of Mass Production), 0x17f7(Graveyard in the Fourth Dimension), 0x1864(Behemoth the King of All Animals), 0x196f(Pot of Avarice), 0x1974(The Forces of Darkness). STATE_OFFSET=0x4b0 (same offset as fn1). SLOT_PALETTE_OFFSET=0x4b4 (zeroed in state 1, palette count in state 2)."

4. **tick_equip_lp_display_by_node_state_4state** (L19980, 2 comment lines L19980..L19984):
   ASCII rewrite: "Equip LP display 4-state machine. Receives effect_node_ptr(r0). XORs [gP1LifePoints+0x1ce8] with [gDuelPhaseFlags+0x4b4] to derive r4 value. STATE_OFFSET=0x4b0 (subs r2,#0x4 from 0x4b4 -> state at gDuelPhaseFlags+0x4b0). XOR_OPERAND_OFF=0x4b4 ([gDuelPhaseFlags+0x4b4] XORd with [gP1LifePoints+0x1ce8] to compute r4). State 0: invokes first LP display step."

5. **dispatch_equip_display_if_confirm_state_one** (L20295):
   ASCII rewrite: "Equip display dispatcher, conditional on confirm_state=1. Reads card_slot[+0xc] halfword (ldrh [r0,#0xc]) as confirm_state; if confirm_state==1 calls dispatch_equip_card_display_op_by_card_id and returns result; else returns 0."

6. **enqueue_equip_slot_sprites_for_pair_loop** (L20309, 4 comment lines L20309..L20315):
   ASCII rewrite: "Enqueue equip slot sprites for pair loop. Receives effect_node_ptr(r0). Initializes loop counter r6=0, loads ROM pair data base address 0x09e3f140 into r7. Loop r6=0..2 (inclusive): loads card_pair_ptr=[r7+r6*4], then invokes enqueue_equip_slot_sprite_with_code_rotation for the sprite. PAIR_TABLE_BASE=0x09e3f140 (ROM pair data table base address). PAIR_STEP=0x868 (per-player stride). OP_CODE=0xe (pair enqueue operation param)."

---

## Section 5.1 Registration (Rule 3, 0-reference blocks)

No ROM_INCBIN blocks in Seg-8b. No orphan registration needed.

---

## Consumer Evidence (R6)

| slot | consumer | file:line | confidence |
|------|----------|-----------|-----------|
| 0x0000140a (SHIFT_CID) | tick_equip_display_with_fn_ptr_routing_3state BST root | asm/10 L19167 + L19140 plate explicit | high |
| 0x00001719 (FIENDS_HAND_MIRROR_CID) | tick_equip_display_with_fn_ptr_routing_3state BST right | asm/10 L19174 + L19140 plate explicit | high |
| 0x08082b19 (fn-ptr) | tick_equip_display_with_fn_ptr_routing_3state dispatch table | asm/10 L19179 (loaded into r7 dispatch path) | high |
| 0x08082b2d (fn-ptr) | tick_equip_display_with_fn_ptr_routing_3state | asm/10 L19184 | high |
| 0x08082b5d (fn-ptr) | tick_equip_display_with_fn_ptr_routing_3state | asm/10 L19202 | high |
| 0x08082c8d (fn-ptr) | tick_equip_chain_pair_display_4state dispatch | asm/10 L19455 | high |
| 0x080905e9 (set_equip_activation_state_by_mode_alt_fn_ptr) | r2 arg to set_equip_activation_state_by_mode__08096a4c | asm/10 L19408 | high |
| 0x00001da8 (LP_CARD_TRACK_BASE_OFF) | gP1LifePoints+0x1da8 LP card-ref tracking base (tick_equip_lp_display_by_node_state) | asm/10 L19624+L19649+L20107 | high |
| 0x00001357 (DNA_SURGERY_CID) | tick_equip_lp_display_by_node_state set_lp_display_row_type15 arg | asm/10 L19645 | high |
| 0x000016d6 (PRIMAL_SEED_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19708 | high |
| 0x000014e7 (KELDO_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19710 | high |
| 0x00001359 (BACKUP_SOLDIER_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19712 | high |
| 0x0000149e (MIRACLE_DIG_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19719 | high |
| 0x00001630 (HIDDEN_BOOK_OF_SPELL_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19732 | high |
| 0x000016a8 (RAY_OF_HOPE_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19739 | high |
| 0x000017f7 (GRAVEYARD_IN_FOURTH_DIMENSION_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19754 | high |
| 0x000017f1 (DARK_FACTORY_MASS_PROD_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19759 | high |
| 0x0000196f (POT_OF_AVARICE_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19772 | high |
| 0x00001864 (BEHEMOTH_KING_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19774 | high |
| 0x00001974 (FORCES_OF_DARKNESS_CID) | tick_equip_display_by_card_id_group_b_3state BST | asm/10 L19782 | high |
| 0x0000011d (CARD_DISPLAY_OP31_LP_BAR_SUB) | tick_equip_lp_display_by_node_state_4state LP-bar sub-op | asm/10 L19793+L19833 | med |
| 0x00001ce8 (P1LP_BLOCK2_OFF_1CE8) | [gP1LifePoints+0x1ce8] XOR'd with [IWRAM+0x4b4] in tick_equip_lp_display_by_node_state_4state | asm/10 L20014 | high |
| 0x000015de (equip_cid_15de_08048a68) | advance_equip_slot_display_state card_id dispatch | asm/10 L20192 | low |
| 0x00001368 (SPELL_ZONE_TARGET_CARD_ID) | advance_equip_slot_display_state card_id check | asm/10 L20194 | high |
| 0x00001568 (cid_1568) | advance_equip_slot_display_state card_id check | asm/10 L20196 | high (unassigned CID) |
| 0x000016d3 (cid_16d3) | advance_equip_slot_display_state card_id check | asm/10 L20207 | high (unassigned CID) |
| 0x00001803 (cid_1803) | advance_equip_slot_display_state card_id check | asm/10 L20215 | high (unassigned CID) |
| 0x09e3f140 (EQUIP_PAIR_ENTRY_TABLE_BASE) | enqueue_equip_slot_sprites_for_pair_loop base address | asm/10 L20347 + L20312 plate | high |
| 0x0201c8f8 (gP1HandSlotArray) | enqueue_equip_slot_sprites_for_pair_loop pair loop ptr | asm/10 L20345 | high |

---

## C5 Dedup Evidence Summary

**REUSE (by-value grep hit):**
- 0x0201b290 -> ewram.inc:353 gDuelPhaseFlags (x9 slots)
- 0xfffc7fff -> duel_field.inc:134 DUAL_LABEL_RENDER_STATE_CLEAR (x5 slots)
- 0x00000484 -> duel_field.inc:364 EQUIP_ACTIVE_CTX_OFF (x2)
- 0x0000ffff -> duel_field.inc:394 LP_ROW_TYPE8_ALL_SLOTS_MASK (x1)
- 0x0201e2a0 -> ewram.inc:218 gDuelCardCtxBase (x1)
- 0x00000868 -> ewram.inc:251 PLAYER_BLOCK_STRIDE (x3)
- 0x0201c510 -> ewram.inc:314 gDuelFieldSlots (x1)
- 0x00001d68 -> ewram.inc:422 ELIGIB_SPRITE_CTRL_OFF (x2)
- 0x00001d6c -> ewram.inc:423 ELIGIB_ANIM_STATE_OFF (x1)
- 0x00001da8 -> ewram.inc:247 LP_CARD_TRACK_BASE_OFF (x3)
- 0x000004b4 -> duel_field.inc:357 EQUIP_ACTIVATION_AUX_OFF (x3)
- 0x00001ce8 -> ewram.inc:276 P1LP_BLOCK2_OFF_1CE8 (x1)
- 0x0000011d -> card_info.inc:1502 CARD_DISPLAY_OP31_LP_BAR_SUB (x2)
- 0x00001357 -> card_info.inc:391 DNA_SURGERY_CID (x1)
- 0x000016a8 -> card_info.inc RAY_OF_HOPE_CID (x1)
- 0x000017f1 -> card_info.inc DARK_FACTORY_MASS_PROD_CID (x1)
- 0x00001864 -> card_info.inc BEHEMOTH_KING_CID (x1)
- 0x0000196f -> card_info.inc POT_OF_AVARICE_CID (x1)
- 0x000015de -> card_info.inc:600 equip_cid_15de_08048a68 (x1)
- 0x00001368 -> card_info.inc:147 SPELL_ZONE_TARGET_CARD_ID (x1)
- 0x0201c8f8 -> ewram.inc:334 gP1HandSlotArray (x1)
- 0x080905e9 -> set_equip_activation_state_by_mode_alt_fn_ptr (NEW from Seg-8a; 3rd occurrence here)

**NEW (by-value grep -> 0 hits):**
- 0x0000140a -> SHIFT_CID (card_info.inc NEW; card_0885)
- 0x00001719 -> FIENDS_HAND_MIRROR_CID (card_info.inc NEW; card_1489)
- 0x000016d6 -> PRIMAL_SEED_CID (card_info.inc NEW; card_1431)
- 0x000014e7 -> KELDO_CID (card_info.inc NEW; card_1047)
- 0x00001359 -> BACKUP_SOLDIER_CID (card_info.inc NEW; card_0762)
- 0x0000149e -> MIRACLE_DIG_CID (card_info.inc NEW; card_0988)
- 0x00001630 -> HIDDEN_BOOK_OF_SPELL_CID (card_info.inc NEW; card_1297)
- 0x000017f7 -> GRAVEYARD_IN_FOURTH_DIMENSION_CID (card_info.inc NEW; card_1668)
- 0x00001974 -> FORCES_OF_DARKNESS_CID (card_info.inc NEW; card_1985)
- 0x00001568 -> cid_1568 (not in card-stats.s)
- 0x000016d3 -> cid_16d3 (not in card-stats.s)
- 0x00001803 -> cid_1803 (not in card-stats.s)
- 0x09e3f140 -> EQUIP_PAIR_ENTRY_TABLE_BASE (duel_field.inc NEW; 1 ROM ref)

---

## C8 Stale FUN_ Scan

grep of asm/10_equip_effect_dispatch.s lines 19057..20393 for 'FUN_' pattern: 0 hits. No stale FUN_ references in Seg-8b.

---

## C13 Coverage Verification

Seg-8b total slot defs: 67
- 3 PTR_gP1LifePoints_ -> SKIP (scope convention)
- 4 gP1LifePoints already-symbolic -> RENAME
- 4 fn-ptr DWORD_ -> RENAME
- 56 hex-value -> EQ (REUSE + NEW including CIDs and neutral cid_<hex>)

Union: 3 (skip, not counted) + 4 (RENAME gP1LP) + 4 (RENAME fn-ptr) + 56 (EQ) = 64 actionable = 67 total - 3 skipped.
Check: 64 + 3 = 67 = total defs. COVERAGE 100%.

---

## New Constants Required (Seg-8b)

File: `constants/card_info.inc`
```
.equ TWO_PRONGED_ATTACK_CID,    0x000012e7  @ Two-Pronged Attack (pw=83887306; card_0671); fn_eligible_two_pronged_attack in BLK1 FS table; C5 grep=0 (new); conf: high
@ (GRAVEDIGGER_GHOUL_CID and DISAPPEAR_CID already listed in Seg-8a new constants)
.equ SHIFT_CID,                 0x0000140a  @ Shift (pw=59560625; card_0885); tick_equip_display_with_fn_ptr_routing_3state BST; C5 grep=0 (new); conf: high
.equ FIENDS_HAND_MIRROR_CID,    0x00001719  @ Fiend's Hand Mirror (pw=58607704; card_1489); tick_equip_display_with_fn_ptr_routing_3state BST; C5 grep=0 (new); conf: high
.equ BACKUP_SOLDIER_CID,        0x00001359  @ Backup Soldier (pw=36280194; card_0762); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ MIRACLE_DIG_CID,           0x0000149e  @ Miracle Dig (pw=06343408; card_0988); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ KELDO_CID,                 0x000014e7  @ Keldo (pw=80441106; card_1047); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ HIDDEN_BOOK_OF_SPELL_CID,  0x00001630  @ Hidden Book of Spell (pw=21840375; card_1297); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ PRIMAL_SEED_CID,           0x000016d6  @ Primal Seed (pw=23701465; card_1431); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ GRAVEYARD_IN_FOURTH_DIMENSION_CID, 0x000017f7  @ The Graveyard in the Fourth Dimension (pw=88089103; card_1668); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ FORCES_OF_DARKNESS_CID,    0x00001974  @ The Forces of Darkness (pw=29826127; card_1985); tick_equip_display_by_card_id_group_b_3state BST; C5 grep=0 (new); conf: high
.equ cid_1568,                  0x00001568  @ unassigned CID 0x1568; advance_equip_slot_display_state dispatch; not in card-stats.s; conf: high (unassigned)
.equ cid_16d3,                  0x000016d3  @ unassigned CID 0x16d3; advance_equip_slot_display_state dispatch; not in card-stats.s; conf: high (unassigned)
.equ cid_1803,                  0x00001803  @ unassigned CID 0x1803; advance_equip_slot_display_state dispatch; not in card-stats.s; conf: high (unassigned)
```

File: `constants/duel_field.inc`
```
.equ EQUIP_PAIR_ENTRY_TABLE_BASE, 0x09e3f140  @ ROM equip pair entry table base; enqueue_equip_slot_sprites_for_pair_loop loads r7=base, loop r6=0..2 reads [r7+r6*4]; 1 ROM ref; C5 grep=0 (new); conf: high
```

Note: TWO_PRONGED_ATTACK_CID should also be added to card_info.inc (used in Seg-8a BLK1 as fn_eligible target). Listed here for completeness; place in card_info.inc before GRAVEDIGGER_GHOUL_CID for numerical order.
