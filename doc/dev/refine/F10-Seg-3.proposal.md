# Refine Proposal: F10-Seg-3  [0x0807be2c..0x0807cd68)

> file 10 Seg-3 -- 19 fn, 55 DWORD_/DAT_ auto-name slots + 12 gP1LifePoints-symbolic DWORD_ + 1 BLK2-base DAT_ = 68 total pool labels.
> 2 ROM_INCBIN blocks: BLK1 (0x7c87a/0x3e) fn_eligible stub, BLK2 (0x7c92c/0x158) 9 dispatch sub-stubs.
> No prior coverage (new segment).

---

## Segment Mapping

### Functions x19

| addr       | name                                               |
|------------|----------------------------------------------------|
| 0x0807be2c | tick_lp_sign_flag_display_seq                      |
| 0x0807bf64 | tick_equip_chain_dual_slot_activation_seq          |
| 0x0807c088 | enqueue_sprite_attr_mode6_on_zone_count_hit        |
| 0x0807c158 | enqueue_multi_slot_marker_sprite_for_node          |
| 0x0807c16c | enqueue_equip_sprite_type11_by_equip_flag          |
| 0x0807c1a8 | tick_zone_activation_lp_indicator_seq              |
| 0x0807c1f8 | tick_equip_zone_sprite_activation_by_node          |
| 0x0807c388 | tick_equip_activation_display_state__0807c388      |
| 0x0807c474 | tick_equip_lp_bar_display_two_step                 |
| 0x0807c510 | submit_equip_zone_score_lp_indicator               |
| 0x0807c590 | tick_equip_activation_zone_scan_2state             |
| 0x0807c660 | apply_equip_slot_node_activation_on_zone_match     |
| 0x0807c750 | dispatch_equip_oam_by_zone_type_and_eligibility    |
| 0x0807c7f0 | dispatch_equip_slot_update_by_type_gate            |
| 0x0807ca84 | tick_equip_spell_zone_placement_scan               |
| 0x0807cb80 | tick_equip_activation_face_down_display_seq        |
| 0x0807cc2c | tick_equip_lp_type18_display_seq                   |
| 0x0807cca0 | tick_banisher_equip_zone_sprite_dispatch           |
| 0x0807cd28 | apply_equip_slot_activation_for_cross_zone_sprite  |

Note: Seg-4 starts at 0x0807cd68 (tick_equip_slot_activation_score_and_oam).

### Auto-name Slots x55 (DWORD_/DAT_ with raw .word values)

```
DWORD_0807beec = 0x00001ce8   tick_lp_sign_flag_display_seq pool
DWORD_0807bef0 = 0x0201b734   same fn pool (gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF)
DWORD_0807bef4 = 0x00000868   same fn pool (PLAYER_BLOCK_STRIDE)
DWORD_0807bef8 = 0x0201b290   same fn pool (gDuelPhaseFlags)
DWORD_0807bf30 = 0x0201b734   same fn pool dup (gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF)
DWORD_0807bf34 = 0x00000868   same fn pool dup
DWORD_0807bf4c = 0x0201b734   same fn pool dup (gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF)
DWORD_0807bf84 = 0x0201b290   tick_equip_chain_dual_slot_activation_seq pool
DWORD_0807bfc0 = 0x000004a4   same fn pool (EQUIP_PHASE_FRAME_OFF)
DWORD_0807bfc8 = 0x00001da8   same fn pool (LP_CARD_TRACK_BASE_OFF)
DWORD_0807c084 = 0x000004a4   same fn pool dup
DAT_0807c150  = 0x00000868    enqueue_sprite_attr_mode6_on_zone_count_hit pool
DAT_0807c154  = 0x0201c510    same fn pool (gDuelFieldSlots)
DWORD_0807c1a4 = 0x00001ce8   enqueue_equip_sprite_type11_by_equip_flag pool
DWORD_0807c1e4 = 0x0201b290   tick_zone_activation_lp_indicator_seq pool
DWORD_0807c214 = 0x0201b290   tick_equip_zone_sprite_activation_by_node pool
DWORD_0807c250 = 0x0201e2a0   same fn pool (gDuelCardCtxBase)
DWORD_0807c254 = 0x08065991   same fn pool (fn-ptr check_equip_activation_at_slot11+1)
DWORD_0807c26c = 0x08065991   same fn pool dup
DWORD_0807c2c0 = 0x000004a4   same fn pool (EQUIP_PHASE_FRAME_OFF)
DWORD_0807c2c8 = 0x00001d70   same fn pool (LP_BANISHER_CTX_OFF)
DWORD_0807c2cc = 0x00000868   same fn pool
DWORD_0807c320 = 0x00001da8   same fn pool (LP_CARD_TRACK_BASE_OFF)
DWORD_0807c324 = 0x00000868   same fn pool
DWORD_0807c328 = 0x000004a4   same fn pool
DWORD_0807c380 = 0x000004a4   same fn pool
DWORD_0807c384 = 0x00000868   same fn pool
DWORD_0807c3a8 = 0x0201b290   tick_equip_activation_display_state__0807c388 pool
DWORD_0807c3e4 = 0x000004a4   same fn pool
DWORD_0807c408 = 0x08090625   same fn pool (fn-ptr invoke_effect_node_with_active_flag_3arg+1)
DWORD_0807c454 = 0x00001d68   same fn pool (ELIGIB_SPRITE_CTRL_OFF)
DWORD_0807c458 = 0x000004a4   same fn pool
DWORD_0807c49c = 0x0201b290   tick_equip_lp_bar_display_two_step pool
DWORD_0807c4d4 = 0x00000868   same fn pool
DWORD_0807c5ac = 0x0201b290   tick_equip_activation_zone_scan_2state pool
DWORD_0807c748 = 0x00000868   apply_equip_slot_node_activation_on_zone_match pool
DWORD_0807c74c = 0x0201c510   same fn pool (gDuelFieldSlots)
DAT_0807c7b0  = 0x00000868    dispatch_equip_oam_by_zone_type_and_eligibility pool
DAT_0807c7b4  = 0x0201c600    same fn pool (gP1FieldArrayCBase)
DWORD_0807c854 = 0x00000868   dispatch_equip_slot_update_by_type_gate pool
DWORD_0807c858 = 0x0201c510   same fn pool (gDuelFieldSlots)
DWORD_0807caa8 = 0x0201b290   tick_equip_spell_zone_placement_scan pool
DWORD_0807cb44 = 0x00000868   same fn pool
DWORD_0807cb9c = 0x0201b290   tick_equip_activation_face_down_display_seq pool
DWORD_0807cbcc = 0x000004a4   same fn pool
DWORD_0807cc08 = gP1LifePoints  (already symbolic; see Rename)
DWORD_0807cc0c = 0x00001da8   same fn pool
DWORD_0807cc10 = 0x000004a4   same fn pool
DWORD_0807cc58 = 0x0201b290   tick_equip_lp_type18_display_seq pool
DWORD_0807cc98 = 0x00001da8   same fn pool
DWORD_0807cc9c = 0x00001dac   same fn pool (NEW: LP_CARD_TRACK_ALT_OFF)
DWORD_0807cce0 = 0x0201b290   tick_banisher_equip_zone_sprite_dispatch pool
DWORD_0807cce8 = 0x00000868   same fn pool
DWORD_0807cd1c = 0x00000868   same fn pool
DWORD_0807cd20 = 0x0201c600   same fn pool (gP1FieldArrayCBase)
DWORD_0807cd24 = 0x00001c88   same fn pool (EQUIP_CHAIN_BASE_OFF)
```

Note: DWORD_0807cc08 (gP1LifePoints symbolic) counted under gP1LifePoints-symbolic group below.

### gP1LifePoints-symbolic Slots x12 (DWORD_ with .word gP1LifePoints)

```
DWORD_0807bee8  = 0x0201c4e0  tick_lp_sign_flag_display_seq pool
DWORD_0807bf38  = 0x0201c4e0  same fn pool
DWORD_0807bfc4  = 0x0201c4e0  tick_equip_chain_dual_slot_activation_seq pool
DWORD_0807c1a0  = 0x0201c4e0  enqueue_equip_sprite_type11_by_equip_flag pool
DWORD_0807c2c4  = 0x0201c4e0  tick_equip_zone_sprite_activation_by_node pool
DWORD_0807c31c  = 0x0201c4e0  same fn pool
DWORD_0807c450  = 0x0201c4e0  tick_equip_activation_display_state__0807c388 pool
DWORD_0807c4d0  = 0x0201c4e0  tick_equip_lp_bar_display_two_step pool
DWORD_0807cb40  = 0x0201c4e0  tick_equip_spell_zone_placement_scan pool
DWORD_0807cc08  = 0x0201c4e0  tick_equip_activation_face_down_display_seq pool
DWORD_0807cc94  = 0x0201c4e0  tick_equip_lp_type18_display_seq pool
DWORD_0807cce4  = 0x0201c4e0  tick_banisher_equip_zone_sprite_dispatch pool
```

### ROM_INCBIN Blocks x2

| BLK | ROM_INCBIN addr/size | raw refs (4B-aligned) | THUMB+1 refs | verdict |
|-----|---------------------|----------------------|--------------|---------|
| 1   | 0x7c87a/0x3e (62B)  | 0                    | 1 at +0x002  | R4 disasm (fn_eligible stub for Des Frog CID=0x1918) |
| 2   | 0x7c92c/0x158 (344B)| 9 unique sub-stubs (base raw=1 each; default raw=21) | 0 | R4 disasm (dispatch sub-stubs x9) |

---

## Data Block Classification (Rule 2/3) -- ref-scan Evidence

Python exhaustive 4B-aligned scan on roms/2343.gba; 2B-step scan run on BLK1 for THUMB+1 detection.

| BLK | ref-scan (4B-aligned raw / THUMB+1) | Verdict | Evidence |
|-----|-------------------------------------|---------|----------|
| 0x7c87a/0x3e | raw=0, THUMB+1=1 at +0x002 (ROM 0x09e45290) | R4 disasm | fn_eligible stub CID=DES_FROG_CID=0x1918; THUMB+1 ref 0x0807c87d at FS table ROM 0x09e45290; word at 0x09e4528c=0x00001918=DES_FROG_CID; push{r4..r7,lr} at +0x02 confirms THUMB code; pool: +0x36=gDuelPhaseFlags(0x0201b290), +0x3a=dispatch_table_base(0x0807c8b8); +0x32 = 0x4687 = MOV PC,r0 CODE not data (pool-vs-code trap: NOT createDWord) |
| 0x7c92c/0x158 | raw=1 each for 8 unique sub-stubs; default (0x0807ca7a) raw=21; THUMB+1=0 for all | R4 disasm | 29-entry dispatch pointer table at 0x7c8b8..0x7c928 (already .word in asm, lines 5781-5809) points into this block; 9 unique targets confirmed by 4B-aligned ref-scan; default sub-stub I at +0x14e (raw=21=29-8); all entries are raw (no THUMB+1), consistent with code-pointer table accessed via indirect jump |

**Zero-ref blocks: none.** Both blocks have refs. No SS5.1 entries.

**Pool-vs-code trap confirmation**: At BLK1 +0x32 (ROM 0x0807c8ac): 0x4687 = THUMB `MOV PC,r0` instruction. This is code, NOT a data word. Do NOT createDWord at this address.

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate; all REUSE except 2 NEW; grep-by-value evidence)

| slot | value | const_name | file | slot_label |
|------|-------|-----------|------|------------|
| DWORD_0807beec | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc L275 | tick_lp_sign_flag_type_select_off |
| DWORD_0807bef0 | 0x0201b734 | (GAS expr) | ewram.inc: gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF | tick_lp_sign_flag_phase_counter |
| DWORD_0807bef4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_lp_sign_flag_player_stride |
| DWORD_0807bef8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_lp_sign_flag_phase_flags |
| DWORD_0807bf30 | 0x0201b734 | (GAS expr) | ewram.inc: gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF | tick_lp_sign_flag_phase_counter_b |
| DWORD_0807bf34 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_lp_sign_flag_player_stride_b |
| DWORD_0807bf4c | 0x0201b734 | (GAS expr) | ewram.inc: gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF | tick_lp_sign_flag_phase_counter_c |
| DWORD_0807bf84 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_chain_dual_slot_phase_flags |
| DWORD_0807bfc0 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_chain_dual_slot_frame_off |
| DWORD_0807bfc8 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc L247 | tick_equip_chain_dual_slot_lp_track_off |
| DWORD_0807c084 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_chain_dual_slot_frame_off_b |
| DAT_0807c150  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | enqueue_mode6_zone_count_player_stride |
| DAT_0807c154  | 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | enqueue_mode6_zone_count_slots_base |
| DWORD_0807c1a4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc L275 | enqueue_equip_sprite_type11_type_sel_off |
| DWORD_0807c1e4 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_zone_act_lp_indicator_phase_flags |
| DWORD_0807c214 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_zone_sprite_act_phase_flags |
| DWORD_0807c250 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc L218 | tick_equip_zone_sprite_act_ctx_base |
| DWORD_0807c2c0 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_zone_sprite_act_frame_off |
| DWORD_0807c2c8 | 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc L423 | tick_equip_zone_sprite_act_banisher_off |
| DWORD_0807c2cc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_equip_zone_sprite_act_player_stride |
| DWORD_0807c320 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc L247 | tick_equip_zone_sprite_act_lp_track_off |
| DWORD_0807c324 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_equip_zone_sprite_act_player_stride_b |
| DWORD_0807c328 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_zone_sprite_act_frame_off_b |
| DWORD_0807c380 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_zone_sprite_act_frame_off_c |
| DWORD_0807c384 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_equip_zone_sprite_act_player_stride_c |
| DWORD_0807c3a8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_act_display_state_phase_flags |
| DWORD_0807c3e4 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_act_display_state_frame_off |
| DWORD_0807c454 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc L421 | tick_equip_act_display_state_eligib_off |
| DWORD_0807c458 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_act_display_state_frame_off_b |
| DWORD_0807c49c | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_lp_bar_two_step_phase_flags |
| DWORD_0807c4d4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_equip_lp_bar_two_step_player_stride |
| DWORD_0807c5ac | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_act_zone_scan_phase_flags |
| DWORD_0807c748 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | apply_equip_slot_node_act_player_stride |
| DWORD_0807c74c | 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | apply_equip_slot_node_act_slots_base |
| DAT_0807c7b0  | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | dispatch_equip_oam_zone_player_stride |
| DAT_0807c7b4  | 0x0201c600 | gP1FieldArrayCBase | ewram.inc L365 | dispatch_equip_oam_zone_field_array_c |
| DWORD_0807c854 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | dispatch_equip_slot_update_player_stride |
| DWORD_0807c858 | 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | dispatch_equip_slot_update_slots_base |
| DWORD_0807caa8 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_spell_zone_scan_phase_flags |
| DWORD_0807cb44 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_equip_spell_zone_scan_player_stride |
| DWORD_0807cb9c | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_act_face_down_phase_flags |
| DWORD_0807cbcc | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_act_face_down_frame_off |
| DWORD_0807cc0c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc L247 | tick_equip_act_face_down_lp_track_off |
| DWORD_0807cc10 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | tick_equip_act_face_down_frame_off_b |
| DWORD_0807cc58 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_equip_lp_type18_phase_flags |
| DWORD_0807cc98 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc L247 | tick_equip_lp_type18_lp_track_off |
| DWORD_0807cc9c | 0x00001dac | LP_CARD_TRACK_ALT_OFF | ewram.inc (NEW) | tick_equip_lp_type18_lp_track_alt_off |
| DWORD_0807cce0 | 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | tick_banisher_zone_sprite_phase_flags |
| DWORD_0807cce8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_banisher_zone_sprite_player_stride |
| DWORD_0807cd1c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | tick_banisher_zone_sprite_player_stride_b |
| DWORD_0807cd20 | 0x0201c600 | gP1FieldArrayCBase | ewram.inc L365 | tick_banisher_zone_sprite_field_array_c |
| DWORD_0807cd24 | 0x00001c88 | EQUIP_CHAIN_BASE_OFF | ewram.inc L495 | tick_banisher_zone_sprite_chain_base_off |

EQ count: 52 slots (50 REUSE + 1 NEW [LP_CARD_TRACK_ALT_OFF] + 1 GAS-expr [0x0201b734 x3]).

Note: 0x0201b734 = gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF = 0x0201b290 + 0x4a4 (verified: Python `0x0201b290 + 0x4a4 == 0x0201b734`). No standalone constant exists. Slots use `.word gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF` GAS expression (evaluates at assemble time; byte-identical). No new named constant needed.

**C5 dedup evidence (REUSE values, grep-by-value confirmed):**

| value | existing name | file:line | NEW slots count |
|-------|---------------|-----------|-----------------|
| 0x0201c4e0 | gP1LifePoints | ewram.inc L79 | 12 (RENAME group, all symbolic) |
| 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc L275 | 2 |
| 0x0201b734 | (computed) | expr: gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF | 3 |
| 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc L250 | 14 |
| 0x0201b290 | gDuelPhaseFlags | ewram.inc L352 | 11 |
| 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc L436 | 8 |
| 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc L247 | 4 |
| 0x0201c510 | gDuelFieldSlots | ewram.inc L313 | 3 |
| 0x0201e2a0 | gDuelCardCtxBase | ewram.inc L218 | 1 |
| 0x00001d70 | LP_BANISHER_CTX_OFF | ewram.inc L423 | 1 |
| 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc L421 | 1 |
| 0x0201c600 | gP1FieldArrayCBase | ewram.inc L365 | 2 |
| 0x00001dac | LP_CARD_TRACK_ALT_OFF | ewram.inc (NEW) | 1 |
| 0x00001c88 | EQUIP_CHAIN_BASE_OFF | ewram.inc L495 | 1 |

New constants (1): LP_CARD_TRACK_ALT_OFF = 0x00001dac; 4 raw ROM refs (ROM 0x0807cc9c, 0x080a2164, 0x080a21a0, 0x080a21e4). Semantic: [gP1LifePoints+0x1dac] LP card-track array word at offset +4 from LP_CARD_TRACK_BASE_OFF (0x1da8); used by tick_equip_lp_type18_display_seq as the third summand in LP-delta accumulation (alongside 0x1da8 and 0x1daa). File: ewram.inc (add after LP_CARD_TRACK_NEXT_OFF).

### REF_SLOTS (USER-label + DATA-ref; fn-ptr ROM addresses)

| slot | value | fn name | slot_label |
|------|-------|---------|------------|
| DWORD_0807c254 | 0x08065991 | check_equip_activation_at_slot11+1 | tick_equip_zone_sprite_act_zone_handler_fn |
| DWORD_0807c26c | 0x08065991 | check_equip_activation_at_slot11+1 | tick_equip_zone_sprite_act_zone_handler_fn_b |
| DWORD_0807c408 | 0x08090625 | invoke_effect_node_with_active_flag_3arg+1 | tick_equip_act_display_state_effect_node_fn |

Evidence:
- check_equip_activation_at_slot11 at 0x08065990 confirmed: asm/08_equip_oam_neodaed.s L3334; alias `check_equip_activation_at_slot11_1` defined in asm/rom.s L73 as `.equ check_equip_activation_at_slot11_1, check_equip_activation_at_slot11+1`; used as THUMB fn-ptr at asm/08 L3691/L3700. Use `.word check_equip_activation_at_slot11_1` in GAS.
- invoke_effect_node_with_active_flag_3arg at 0x08090624 confirmed: asm/11_effect_slot_puzzletext.s L11824; 0x08090625 = fn+1 (THUMB); asm/09 plate comment at L4951 "invoke_effect_node_with_active_flag_3arg+1 (THUMB+1=0x08090625)"; asm/08 L12944 "invoke_effect_node_with_active_flag_3arg+1". Use `.word invoke_effect_node_with_active_flag_3arg+1` in GAS.

REF count: 3 slots.

### RENAME_SLOTS (label rename + EOL note)

All gP1LifePoints-symbolic DWORD_ slots and BLK2 base DAT_:

| slot | current .word | slot_label | EOL |
|------|--------------|-----------|-----|
| DWORD_0807bee8 | gP1LifePoints | tick_lp_sign_flag_lp_base | already symbolic |
| DWORD_0807bf38 | gP1LifePoints | tick_lp_sign_flag_lp_base_b | already symbolic |
| DWORD_0807bfc4 | gP1LifePoints | tick_equip_chain_dual_slot_lp_base | already symbolic |
| DWORD_0807c1a0 | gP1LifePoints | enqueue_equip_sprite_type11_lp_base | already symbolic |
| DWORD_0807c2c4 | gP1LifePoints | tick_equip_zone_sprite_act_lp_base | already symbolic |
| DWORD_0807c31c | gP1LifePoints | tick_equip_zone_sprite_act_lp_base_b | already symbolic |
| DWORD_0807c450 | gP1LifePoints | tick_equip_act_display_state_lp_base | already symbolic |
| DWORD_0807c4d0 | gP1LifePoints | tick_equip_lp_bar_two_step_lp_base | already symbolic |
| DWORD_0807cb40 | gP1LifePoints | tick_equip_spell_zone_scan_lp_base | already symbolic |
| DWORD_0807cc08 | gP1LifePoints | tick_equip_act_face_down_lp_base | already symbolic |
| DWORD_0807cc94 | gP1LifePoints | tick_equip_lp_type18_lp_base | already symbolic |
| DWORD_0807cce4 | gP1LifePoints | tick_banisher_zone_sprite_lp_base | already symbolic |
| DAT_0807c92c | ROM_INCBIN | des_frog_dispatch_stubs | BLK2 block label after disasm |

RENAME count: 13 slots.

### FUNC_RENAME (misnomer correction)

| addr | old name | new name | indeg | reason |
|------|---------|---------|-------|--------|
| 0x0807c388 | tick_equip_activation_display_state__0807c388 | tick_equip_activation_display_state | 0 | Trailing __0807c388 suffix is naming-phase auto-deconflict residue; indeg=0 confirmed (grep `tick_equip_activation_display_state__0807c388` in asm/*.s callee column: 0 direct bl callers); the name without suffix is unique (grep returns 0 other hits); suffix not needed |

FUNC_RENAME count: 1.

### PLATE (R5)

| fn addr | action | plate text |
|---------|--------|------------|
| 0x0807c388 | substring replace: `tick_equip_activation_display_state__0807c388` -> `tick_equip_activation_display_state` | (already has correct plate at asm L5105-L5115; update fn name reference in plate to drop __0807c388 suffix if present) |

---

## disasm Plan (R4)

### BLK1: fn_eligible stub for Des Frog

**Range**: 0x0807c87a..0x0807c8b8 (0x3e bytes = 62 bytes)

**Entry points**: 
- 0x0807c87a: 2B pad (0x0000) -- disasm as .hword 0x0000 or pad
- 0x0807c87c: fn_eligible_des_frog (THUMB stub, push {r4..r7,lr} at +0x02)

**THUMB stub anatomy** (from ROM byte scan):
- +0x00..+0x01: `00 00` = 2B pad
- +0x02: THUMB code begins (`f0 b5` = push {r4,r5,r6,r7,lr})
- +0x14: `46 40` = .hword 0x4046 (MOV r0,r8 high-reg transfer)
- +0x32: `87 46` = .hword 0x4687 = THUMB MOV PC,r0 (tail-call via r0; NOT a data word -- pool-vs-code trap)
- +0x34..+0x35: `00 00` = pad
- +0x36..+0x39: `0x0201b290` = gDuelPhaseFlags (literal pool createDWord)
- +0x3a..+0x3d: `0x0807c8b8` = dispatch_table_base (literal pool createDWord)

**createDWord list for BLK1**:
- ROM 0x0807c8b0 (+0x36): `gDuelPhaseFlags` (0x0201b290)
- ROM 0x0807c8b4 (+0x3a): `0x0807c8b8` (dispatch table base; use raw value or new label)

**fn_eligible function naming**:
- `fn_eligible_des_frog` @ 0x0807c87c (THUMB+1 ref = 0x0807c87d from FS table 0x09e45290; CID = 0x00001918 = DES_FROG_CID at 0x09e4528c; CID verified: card_info.inc L1247 `.equ DES_FROG_CID, 0x00001918`; high confidence)

**Disasm procedure**:
1. clearListing 0x0807c87a..0x0807c8b8
2. setTMode 0x0807c87c (THUMB mode)
3. DisassembleCommand 0x0807c87c (single stub, includes pool at +0x36/+0x3a)
4. createDWord at ROM 0x0807c8b0 and 0x0807c8b4
5. createLabel 0x0807c87a "des_frog_fn_eligible_pad" (for the 2B pad before stub)
6. createLabel 0x0807c87c "fn_eligible_des_frog"

### BLK2: dispatch sub-stubs for Des Frog card effect dispatch

**Range**: 0x0807c92c..0x0807ca84 (0x158 bytes = 344 bytes)

**Dispatch table** (already in asm at lines 5781-5809, .word entries at 0x0807c8b8..0x0807c928):
- 29 entries; 9 unique targets; default sub-stub I (0x0807ca7a) has raw=21 refs (29-8=21 non-unique table entries)

**Sub-stub entry points and sizes**:

| sub-stub | addr | offset in BLK2 | raw refs | BL targets (confirmed) | exit pattern |
|----------|------|----------------|----------|----------------------|--------------|
| A | 0x0807c92c | +0x000 | 1 | check_neo_daedalus_placement_eligible(0x0805c218), count_extra_deck_cards_by_id(0x080370dc), count_monster_slots_for_player(0x0805c17c) | branch to sub-stub B epilogue area |
| B | 0x0807c9c0 | +0x094 | 1 | trigger_card_display_op31_if_not_active(0x08093390), init_effect_slot_display_context(0x080941c4) | branch |
| C | 0x0807c9ec | +0x0c0 | 1 | increment_lp_bar_display_counter(0x0804a76c) | returns 0x7d |
| D | 0x0807ca18 | +0x0ec | 1 | get_effect_slot_entry_ptr_by_palette_id(0x080945f4), lookup_slot_display_value_by_card_id(0x080819cc), invoke_setup_equip_oam_with_attr2(0x080abe40) | returns 0x7d |
| E | 0x0807ca50 | +0x124 | 1 | check_zone_eligible_with_deck_flag(0x0804a4cc) | movs r0,#0x77; b I+2 (shared epilogue) |
| F | 0x0807ca5c | +0x130 | 1 | set_lp_row_type2_with_sign_flag_only(via BL 0x080a1cd0? no: BL at +0x134=0x0804a4cc? -- see below) | movs r0,#0x76; b I+2 |
| G | 0x0807ca68 | +0x13c | 1 | decrement_lp_bar_display_counter(0x0804a870) | movs r0,#0x64; b I+2 |
| H | 0x0807ca74 | +0x148 | 1 | enqueue_lp_counter_sprite_by_player(0x0804a540) | movs r0,#0x0; (falls through to I) |
| I | 0x0807ca7a | +0x14e | 21 | (none) | movs r0,#0; pop {r4..r7}; pop {r1}; bx r1; .hword 0 |

Sub-stub BL decode (from Python exhaustive scan of BLK2):
- +0x004 (0x0807c930): BL -> 0x0805c218 = check_neo_daedalus_placement_eligible
- +0x012 (0x0807c93e): BL -> 0x080370dc = count_extra_deck_cards_by_id
- +0x024 (0x0807c950): BL -> 0x0805c17c = count_monster_slots_for_player
- +0x044 (0x0807c970): BL -> 0x0805c17c = count_monster_slots_for_player (2nd call)
- +0x05c (0x0807c988): BL -> 0x080819cc = lookup_slot_display_value_by_card_id
- +0x066 (0x0807c992): BL -> 0x0808dab0 = dispatch_effect_handler_by_card_id
- +0x074 (0x0807c9a0): BL -> 0x08093390 = trigger_card_display_op31_if_not_active
- +0x088 (0x0807c9b4): BL -> 0x08093390 = trigger_card_display_op31_if_not_active (2nd)
- +0x0a8 (0x0807c9d4): BL -> 0x080819cc = lookup_slot_display_value_by_card_id (2nd)
- +0x0b4 (0x0807c9e0): BL -> 0x080941c4 = init_effect_slot_display_context
- +0x0c0 (0x0807c9ec): BL -> 0x0804a76c = increment_lp_bar_display_counter
- +0x0fa (0x0807ca26): BL -> 0x080945f4 = get_effect_slot_entry_ptr_by_palette_id
- +0x108 (0x0807ca34): BL -> 0x080abe40 = invoke_setup_equip_oam_with_attr2
- +0x11c (0x0807ca48): BL -> 0x0804a870 = decrement_lp_bar_display_counter
- +0x128 (0x0807ca54): BL -> 0x0804a4cc = check_zone_eligible_with_deck_flag
- +0x134 (0x0807ca60): BL -> 0x080a1cd0 = set_lp_row_type7_if_opponent_linked
- +0x140 (0x0807ca6c): BL -> 0x0804a4cc = check_zone_eligible_with_deck_flag (2nd)
- +0x14a (0x0807ca76): BL -> 0x0804a540 = enqueue_lp_counter_sprite_by_player

Sub-stubs E/F/G share epilogue: each sets return code then `b 0x0807ca7c` (= I+2, skipping `movs r0,#0`).

**createDWord list for BLK2** (literal pool words; NOT instruction pairs):
- ROM 0x0807c960 (+0x034): 0x00001919 = TADPOLE_CID (card_info.inc L369; adjacent CID to DES_FROG used as reference card-id in sub-stub A)
- ROM 0x0807c964 (+0x038): 0x0201b290 = gDuelPhaseFlags
- ROM 0x0807c968 (+0x03c): 0x000004a4 = EQUIP_PHASE_FRAME_OFF
- ROM 0x0807c9a8 (+0x07c): 0x0201b290 = gDuelPhaseFlags (dup)
- ROM 0x0807c9ac (+0x080): 0x000004a4 = EQUIP_PHASE_FRAME_OFF (dup)
- ROM 0x0807c9bc (+0x090): 0x0000011d = CARD_DISPLAY_OP31_LP_BAR_SUB (card_info.inc L1498)
- ROM 0x0807c9e8 (+0x0bc): 0x000004a4 = EQUIP_PHASE_FRAME_OFF (dup)
- ROM 0x0807ca0c (+0x0e0): 0x0201c4e0 = gP1LifePoints
- ROM 0x0807ca10 (+0x0e4): 0x0201b290 = gDuelPhaseFlags (dup)
- ROM 0x0807ca14 (+0x0e8): 0x000004a4 = EQUIP_PHASE_FRAME_OFF (dup)
- ROM 0x0807ca44 (+0x118): 0x000004a4 = EQUIP_PHASE_FRAME_OFF (dup)

Pool-vs-code exclusions (NOT createDWord):
- ROM 0x0807c95c (+0x030): 0x0000e00a = THUMB `b +0x14` + `00 00` pad -- instruction, not pool
- ROM 0x0807ca08 (+0x0dc): 0x0000e038 = THUMB branch -- instruction, not pool

Total createDWord calls in BLK2: 11.

**Disasm procedure for BLK2**:
1. clearListing 0x0807c92c..0x0807ca84
2. setTMode 0x0807c92c (all THUMB)
3. For each sub-stub entry: DisassembleCommand individually (do NOT use single-range disasm; it only disassembles first stub)
   - DisassembleCommand 0x0807c92c (sub-stub A)
   - DisassembleCommand 0x0807c9c0 (sub-stub B)
   - DisassembleCommand 0x0807c9ec (sub-stub C)
   - DisassembleCommand 0x0807ca18 (sub-stub D)
   - DisassembleCommand 0x0807ca50 (sub-stub E)
   - DisassembleCommand 0x0807ca5c (sub-stub F)
   - DisassembleCommand 0x0807ca68 (sub-stub G)
   - DisassembleCommand 0x0807ca74 (sub-stub H)
   - DisassembleCommand 0x0807ca7a (sub-stub I = default)
4. createDWord at each of the 11 pool locations listed above
5. createLabel for each sub-stub:
   - 0x0807c92c: "des_frog_stub_a_zone_check"
   - 0x0807c9c0: "des_frog_stub_b_display_init"
   - 0x0807c9ec: "des_frog_stub_c_incr_counter"
   - 0x0807ca18: "des_frog_stub_d_oam_setup"
   - 0x0807ca50: "des_frog_stub_e_ret77"
   - 0x0807ca5c: "des_frog_stub_f_ret76"
   - 0x0807ca68: "des_frog_stub_g_ret64"
   - 0x0807ca74: "des_frog_stub_h_enqueue_lp"
   - 0x0807ca7a: "des_frog_stub_i_default_exit"

---

## carve Plan (R7)

None. BLK1 and BLK2 are THUMB code blocks (fn_eligible + dispatch sub-stubs), not data to be carved into rom.s. The dispatch table at 0x0807c8b8..0x0807c928 is already rendered as `.word` entries in the asm and needs only the REF target labels.

---

## New Constants / Globals

### New in ewram.inc (after LP_CARD_TRACK_NEXT_OFF line ~248):

```
.equ LP_CARD_TRACK_ALT_OFF,   0x00001dac  @ [gP1LifePoints+0x1dac] LP card-track array alt word at base+4; tick_equip_lp_type18_display_seq 3rd LP-delta summand (alongside 0x1da8 and 0x1daa); 4 raw ROM refs (0x0807cc9c, 0x080a2164, 0x080a21a0, 0x080a21e4)
```

Verification: ROM byte at 0x0807cc9c = `ac 1d 00 00` = 0x00001dac (confirmed by Python). grep-by-value in ewram.inc: 0 existing hits for `0x00001dac` or `0x1dac` -- confirmed NEW.

### Note on 0x0201b734:

Value is `gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF` (GAS expression). All three slots (DWORD_0807bef0, DWORD_0807bf30, DWORD_0807bf4c) use `.word gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF`. No new standalone constant needed.

---

## SS5.1 Register (Rule 3)

None. Both ROM_INCBIN blocks have confirmed refs (BLK1: THUMB+1=1; BLK2: raw=1..21 per sub-stub). No zero-reference blocks in Seg-3.

---

## Consumer Evidence (R6) -- Key Slot Semantics

| slot | value | consumer fn | file:line | evidence | confidence |
|------|-------|------------|-----------|----------|------------|
| DWORD_0807bef0 | 0x0201b734 | tick_lp_sign_flag_display_seq | asm/10 L4347 plate "XOR_BASE=0x0201b734: State 0x80: clears [0x0201b734]; State 0x7e: reads+1 into [0x0201b734]" | Phase counter/accumulator word at gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF; all 4 ROM refs are in tick_lp_sign_flag or Seg-4+ state machines | high |
| DWORD_0807c250 | 0x0201e2a0 | tick_equip_zone_sprite_activation_by_node | asm/10 L4946 .word; L4077 plate "EFFECT_CTX_BASE=0x0201e2a0" | gDuelCardCtxBase; ewram.inc L218 | high |
| DWORD_0807c254 | 0x08065991 | tick_equip_zone_sprite_activation_by_node | asm/10 L4948 .word; L4212 EOL "fn-ptr check_equip_activation_at_slot11+1 (THUMB+1)"; asm/08 L3334 label check_equip_activation_at_slot11 | check_equip_activation_at_slot11+1 THUMB fn-ptr; used as zone-handler callback | high |
| DWORD_0807c408 | 0x08090625 | tick_equip_activation_display_state__0807c388 | asm/10 L5182 .word; asm/09 L4951 "invoke_effect_node_with_active_flag_3arg+1 (THUMB+1=0x08090625)"; asm/11 L11824 function label | invoke_effect_node_with_active_flag_3arg+1; passed as mode/fn param to set_equip_activation_state_by_mode | high |
| DWORD_0807cc9c | 0x00001dac | tick_equip_lp_type18_display_seq | asm/10 L6113 .word; function plate L6048-L6054 "合计 LP 变化量(从 gP1LifePoints+0x1da8/0x1dac 偏移读取)"; adjacent to LP_CARD_TRACK_BASE_OFF(0x1da8) and LP_CARD_TRACK_NEXT_OFF(0x1daa) | LP card-track alt word at +4 from base; 4 ROM refs confirmed; distinct from 0x1da8 (base) and 0x1daa (next) | high |
| DAT_0807c7b4 | 0x0201c600 | dispatch_equip_oam_by_zone_type_and_eligibility | asm/10 L5671 .word; ewram.inc L365 gP1FieldArrayCBase; function plate L5622 "ldr r2, DAT_0807c7b4" with player*0x868 indexing | gP1FieldArrayCBase base for zone slot indexing | high |
| DWORD_0807cd24 | 0x00001c88 | tick_banisher_equip_zone_sprite_dispatch | asm/10 L6194 .word; ewram.inc L495 EQUIP_CHAIN_BASE_OFF=0x00001c88 "[gP1FieldArrayCBase(0x0201c600)+0x1c88]"; function plate L6116 "ZONE_COORD_OFFSET=0x1c88" | EQUIP_CHAIN_BASE_OFF offset from gP1FieldArrayCBase | high |

---

## C8 Stale FUN_ Scan

Grep for stale `FUN_` references in plate/EOL comments within Seg-3 range:

- asm/10 L4358..L6231 plate comments: 0 occurrences of `FUN_` in non-trivial positions.
- FUNC_RENAME candidate `tick_equip_activation_display_state__0807c388` at L5116: plate at L5105-L5115 does NOT contain `FUN_` -- uses semantic name already. Suffix `__0807c388` in the function label itself is the issue; plate is clean.

C8 stale FUN_ count: 0.

---

## C13 Coverage Proof (100%)

Total Seg-3 pool labels: 68

Distribution:
- EQ_SLOTS: 52 (all have slot_label assignments above)
- REF_SLOTS: 3 (DWORD_0807c254, DWORD_0807c26c, DWORD_0807c408)
- RENAME_SLOTS: 13 (12 gP1LifePoints-symbolic + 1 BLK2 base DAT_)
- FUNC_RENAME: 1 (not a pool slot; function label only)

52 + 3 + 13 = 68 = total slot count. Coverage = 100%.

BLK1 and BLK2 ROM_INCBIN ranges: both assigned R4 disasm with sub-stub labels and createDWord lists. Zero residual incbin after disasm.

---

## Help Requests

None. All slot semantics and BL targets have high-confidence consumer evidence. Sub-stub function identities confirmed via Python BL decode + asm/*.s function label lookup.

---

## Executor Report: F10-Seg-3

- Slots: EQ=52 REF=3 RENAME=13 FUNC_RENAME=1 PLATE=1
- carve=0 disasm=BLK1(fn_eligible_des_frog)+BLK2(sub-stubs-A..I) SS5.1=0
- New constants/globals: LP_CARD_TRACK_ALT_OFF=0x00001dac (ewram.inc, after LP_CARD_TRACK_NEXT_OFF)
- Help: none
- proposal: doc/dev/refine/F10-Seg-3.proposal.md
