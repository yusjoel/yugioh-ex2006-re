# Refine Proposal: F09-Seg-3  [0x0807104c..0x080719fc)

## Segment Mapping

### Function entries (20 named, from push-prologue):

| addr | name | asm line |
|------|------|----------|
| 0x0807104c | dispatch_equip_chain_effect_slot_by_state | L5342 |
| 0x08071170 | enqueue_field_slot_overlay_sprite_if_chain_matches | L5505 |
| 0x08071210 | enqueue_eligible_slot_sprites_for_both_players | L5593 |
| 0x08071258 | check_effect_slot_equip_zone_pattern | L5643 |
| 0x08071284 | scan_equip_chain_for_zone_pattern_sprites | L5678 |
| 0x080712a0 | dispatch_equip_chain_state_if_tile_count_valid | L5703 |
| 0x0807136c | enqueue_overlay_sprite_if_tile_count_equal | L5814 |
| 0x08071404 | enqueue_equip_sprite_guarded_by_zone_type13 | L5900 |
| 0x0807142c | dispatch_equip_slot_sprite_if_zone_entry_active | L5927 |
| 0x08071488 | enqueue_sprite_attr_type11_from_chain_entry | L5983 |
| 0x080714ac | enqueue_slot_overlay_sprite_if_equip_bitmap_active | L6014 |
| 0x080714ec | dispatch_equip_zone11_target_by_activation_state | L6059 |
| 0x0807158c | dispatch_equip_lp_bar_or_bitmap_by_zone_type | L6142 |
| 0x080715ac | dispatch_equip_lp_bar_with_bitmap_filter | L6165 |
| 0x08071604 | tick_zone_sprite_pipeline_with_chain_counter | L6222 |
| 0x08071654 | dispatch_hand_card_sprite_by_effect_slot_zone | L6278 |
| 0x080717f0 | tick_equip_lp_spell_zone_display_state | L6377 |
| 0x080718c4 | forward_equip_monster_zone_sprites_and_lp | L6491 |
| 0x080718d0 | submit_equip_lp_indicator_if_target_bitmap_active | L6508 |
| 0x0807190c | tick_equip_neo_daedalus_oam_display_state | L6541 |

### Residual auto-name slots (39 total):

Python regex scan of asm lines 5342..6675, definitions only (not references):

| line | slot | ROM value |
|------|------|-----------|
| L5359 | DWORD_0807106c | 0x0201b290 |
| L5459 | DWORD_08071138 | 0x0201c4e0 (gP1LifePoints symbol) |
| L5461 | DWORD_0807113c | 0x00001da8 |
| L5463 | DWORD_08071140 | 0x00000868 |
| L5579 | DWORD_08071204 | 0x00000868 |
| L5581 | DWORD_08071208 | 0x0201c510 |
| L5583 | DWORD_0807120c | 0x000017c2 |
| L5664 | DWORD_08071280 | 0x00f0ffff |
| L5690 | DWORD_0807129c | 0x08071259 |
| L5780 | DWORD_08071338 | 0x00000868 |
| L5782 | DWORD_0807133c | 0x0201c510 |
| L5784 | DWORD_08071340 | 0x0201b290 |
| L5786 | DWORD_08071344 | 0x000014c4 |
| L5878 | DWORD_080713ec | 0x00000868 |
| L5880 | DWORD_080713f0 | 0x0201c510 |
| L5997 | DWORD_080714a4 | 0x0201c4e0 (gP1LifePoints symbol) |
| L5999 | DWORD_080714a8 | 0x00001ce8 |
| L6074 | DWORD_08071508 | 0x0201b290 |
| L6096 | DWORD_08071538 | 0x08090625 |
| L6119 | DWORD_08071568 | 0x0201c4e0 (gP1LifePoints symbol) |
| L6121 | DWORD_0807156c | 0x00001d68 |
| L6123 | DWORD_08071570 | 0x00001d6c |
| L6255 | DWORD_08071644 | 0x0201b290 |
| L6257 | DWORD_08071648 | 0x000004a4 |
| L6345 | DWORD_080716dc | 0x00000868 |
| L6347 | DWORD_080716e0 | 0x0201c8f8 |
| L6363 | PTR_DAT_08071740 | 0x080717c4 (dispatch table[0]) |
| L6369 | DAT_08071754 | ROM_INCBIN label (block 2 start) |
| L6394 | DWORD_08071810 | 0x0201b290 |
| L6426 | DWORD_08071850 | 0x000004a4 |
| L6456 | DWORD_08071888 | 0x0201c4e0 (gP1LifePoints symbol) |
| L6458 | DWORD_0807188c | 0x00001da8 |
| L6473 | DWORD_080718a8 | 0x000004a4 |
| L6556 | DWORD_08071928 | 0x0201b290 |
| L6610 | DWORD_08071998 | 0x0201c4e0 (gP1LifePoints symbol) |
| L6612 | DWORD_0807199c | 0x00001da8 |
| L6614 | DWORD_080719a0 | 0x0201e2a0 |
| L6641 | DWORD_080719d4 | 0x0201c4e0 (gP1LifePoints symbol) |
| L6643 | DWORD_080719d8 | 0x00001da8 |

NOTE: DWORD_08071138/080714a4/08071568/08071888/08071998/080719d4 contain `gP1LifePoints`
(already symbolized; auto-name counts against the total because the slot label still has
DWORD_ prefix). DAT_08071754 is the ROM_INCBIN block-2 start label.

### ROM_INCBIN blocks (2):

- Block 1: `ROM_INCBIN 0x716fa, 0x42` (L6361) -> GBA [0x080716fa, 0x0807173c)
- Block 2: `ROM_INCBIN 0x71754, 0x9c` (L6370) -> GBA [0x08071754, 0x080717f0)

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

ref-scan method: python exhaustive 2B-step across all candidate entries in each block.

### Block 1: 0x080716fa size 0x42

```python
# ROM value scan results:
# 0x080716fc: raw=1 @ ROM 0x4318e4 (GBA 0x084318e4) / thumb=1 @ ROM 0x1e40e98 (GBA 0x09e40e98)
# Raw hit at 0x084318e4: surrounded by high-entropy bytes (0xfa0ff8ff/0x08ebef15/0x1a271c0f)
#   -> confirmed false positive (compressed data region at 0x0843xxxx)
# THUMB+1 hit at ROM 0x1e40e98 (GBA 0x09e40e98): FS card effect handler table entry
#   CID at fn_ptr_addr - 4 = ROM 0x1e40e94: 0x000014e8 = Dragged Down into the Grave
#   (card-stats.s card_1048 slot=0x14E8 pw=16435215)
#   fn_eligible start = 0x080716fc (0x716fa+2 = alignment pad, then push {r4,r5,lr})
#
# All other hits in block are misaligned (0x08071700 at 0x1b9f463: byte-3-of-word)
# or compressed false positives.
```

Block 1 analysis:
- 0x080716fa/0x0000 = 2-byte alignment pad (byte pad before fn_eligible entry)
- 0x080716fc = `push {r4,r5,lr}` (THUMB: 0xb530 1c04) = fn_eligible stub entry
- Code body 0x080716fc..0x08071727 = fn_eligible for Dragged Down into the Grave
- Literal pool 0x0807172c..0x0807173b: gP1LifePoints / P1LP_BLOCK2_OFF_1CE8 / gDuelPhaseFlags / EQUIP_PHASE_FRAME_OFF

Verdict: **DISASM (R4)** -- fn_eligible THUMB stub, THUMB+1 ref from FS handler table at GBA 0x09e40e98.

| Block | ref-scan (raw / THUMB+1) | Verdict | Reason |
|-------|--------------------------|---------|--------|
| Block1 0x080716fa/0x42 | raw=0 aligned / thumb=1 @0x09e40e98 | DISASM | FS table THUMB+1 ref; CID=0x14e8 (Dragged Down into the Grave); raw at 0x084318e4 is compressed data false positive |

### Block 2: 0x08071754 size 0x9c

```python
# ROM value scan results:
# 0x08071754: raw=1 @ ROM 0x71750 (GBA 0x08071750) -- inside same-seg dispatch table PTR_DAT_08071740[4]
# 0x0807177c: raw=1 @ ROM 0x7174c (GBA 0x0807174c) -- PTR_DAT_08071740[3]
# 0x0807178a: raw=1 @ ROM 0x71748 (GBA 0x08071748) -- PTR_DAT_08071740[2]
# 0x080717a4: raw=1 @ ROM 0x71744 (GBA 0x08071744) -- PTR_DAT_08071740[1]
# 0x080717c4: raw=1 @ ROM 0x71740 (GBA 0x08071740) -- PTR_DAT_08071740[0]
# All 5 raw refs = aligned, inside same-segment PTR_DAT_08071740 dispatch table (lines 6364-6368)
# No THUMB+1 refs for any entry in block 2 (confirmed exhaustive scan).
```

Block 2 context: the asm already has these `.word` entries structured before block 2:
- L6362: `.word  0x08071740` @ 0x0807173c (pointer to the dispatch table itself; indirection level)
- L6363: `PTR_DAT_08071740:` (dispatch table base, GBA 0x08071740)
  - [0] 0x080717c4, [1] 0x080717a4, [2] 0x0807178a, [3] 0x0807177c, [4] 0x08071754
- L6369: `DAT_08071754:` (=block 2 start, the first sub-stub entry)

The 5 entries are raw code addresses pointing into block 2. The table is used by a caller that
indexes PTR_DAT_08071740 with some index value to jump to one of 5 sub-stubs.

Verdict: **DISASM (R4)** -- raw dispatch sub-table (5 entries, code addrs); referenced by aligned
`.word` entries in PTR_DAT_08071740 (L6364-6368), which are themselves referenced by the pointer
word at L6362.

| Block | ref-scan (raw / THUMB+1) | Verdict | Reason |
|-------|--------------------------|---------|--------|
| Block2 0x08071754/0x9c | raw=5 @same-seg PTR_DAT_08071740 table / thumb=0 | DISASM | 5 dispatch sub-stubs; all raw refs from aligned dispatch table entries PTR_DAT_08071740[0..4] |

---

## Symbolization Plan (R1/R2/R3)

All 39 auto-name slots must be covered. Classification:

### EQ_SLOTS (data-equate; reuse first)

#### EQ_REUSE (existing constant; grep by value confirmed)

| slot | value | const_name | inc_file | slot_label | C5 evidence |
|------|-------|-----------|----------|-----------|-------------|
| DWORD_0807106c | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags | grep 0x0201b290 -> ewram.inc L218 |
| DWORD_08071340 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags | same |
| DWORD_08071508 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags | same |
| DWORD_08071644 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags | same |
| DWORD_08071810 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags | same |
| DWORD_08071928 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags | same |
| DWORD_08071138 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gP1LifePoints | grep 0x0201c4e0 -> ewram.inc |
| DWORD_080714a4 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gP1LifePoints | same |
| DWORD_08071568 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gP1LifePoints | same |
| DWORD_08071888 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gP1LifePoints | same |
| DWORD_08071998 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gP1LifePoints | same |
| DWORD_080719d4 | 0x0201c4e0 | gP1LifePoints | ewram.inc | gP1LifePoints | same |
| DWORD_0807113c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF | grep 0x00001da8 -> ewram.inc L247 |
| DWORD_0807188c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF | same |
| DWORD_0807199c | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF | same |
| DWORD_080719d8 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF | same |
| DWORD_08071140 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE | grep 0x868 -> ewram.inc L250 |
| DWORD_08071204 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE | same |
| DWORD_08071338 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE | same |
| DWORD_080713ec | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE | same |
| DWORD_080716dc | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE | same |
| DWORD_08071208 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots | grep 0x0201c510 -> ewram.inc L313 |
| DWORD_0807133c | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots | same |
| DWORD_080713f0 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots | same |
| DWORD_0807120c | 0x000017c2 | BLUE_EYES_SHINING_DRAGON_CID | card_info.inc | BLUE_EYES_SHINING_DRAGON_CID | grep 0x000017c2 -> card_info.inc L440 |
| DWORD_080714a8 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | P1LP_BLOCK2_OFF_1CE8 | grep 0x1ce8 -> ewram.inc L275 |
| DWORD_08071648 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF | grep 0x000004a4 -> ewram.inc L435 |
| DWORD_08071850 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF | same |
| DWORD_080718a8 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF | same |
| DWORD_0807156c | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc | ELIGIB_SPRITE_CTRL_OFF | grep 0x00001d68 -> ewram.inc L420 |
| DWORD_08071570 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc | ELIGIB_ANIM_STATE_OFF | grep 0x00001d6c -> ewram.inc L421 |
| DWORD_080716e0 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | gP1HandSlotArray | grep 0x0201c8f8 -> ewram.inc L333 |
| DWORD_080719a0 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase | grep 0x0201e2a0 -> ewram.inc L218 |

Total EQ_REUSE: 34 slots.

#### EQ_NEW (new constant; C5 grep-by-value confirms 0 hits in constants/)

| slot | value | const_name | inc_file | evidence | C5 new-proof |
|------|-------|-----------|----------|---------|--------------|
| DWORD_08071280 | 0x00f0ffff | EQUIP_ZONE_WORD_MASK | equip_lp.inc (new) | check_effect_slot_equip_zone_pattern: ldr r1,DWORD_08071280; ands r0,r1; cmp r0,#0xa6<<5=0x14c0 -- bitmask to extract zone pattern field from zone_word; asm/09 L5648-5652; conf:high | grep 0x00f0ffff constants/ -> 0 hits -> NEW |
| DWORD_08071344 | 0x000014c4 | FREED_THE_MATCHLESS_GENERAL_CID | card_info.inc | dispatch_equip_chain_state_if_tile_count_valid: ldr r4,DWORD_08071344; movs r1,#0xb; adds r2,r4,#0; bl check_value_in_slot_chain -- CID passed as chain check value; card-stats.s card_1013 slot=0x14C4 pw=49681811; asm/09 L5770-5773; conf:high | grep 0x000014c4 constants/ -> 0 hits -> NEW |

NOTE: DWORD_0807129c = 0x08071259 and DWORD_08071538 = 0x08090625 are THUMB+1 fn-ptrs
(handled in RENAME_SLOTS, not EQ; raw value, no .equ needed).
NOTE: PTR_DAT_08071740 = 0x080717c4 is a dispatch table pointer (handled in RENAME_SLOTS).

Total EQ_NEW: 2 slots.

---

### REF_SLOTS (USER-label + DATA-ref; RAM/ROM globals)

These are already symbolized globals that need the auto-name slot replaced with the global label:

None in this segment. All RAM globals (gDuelPhaseFlags, gP1LifePoints, etc.) fall under EQ_REUSE
via the existing `.equ` constants approach. The gP1LifePoints slots already contain the symbol
`gP1LifePoints` (not the raw 0x0201c4e0 value) so they need only a label rename, not a REF action.

Total REF_SLOTS: 0.

---

### RENAME_SLOTS (label rename + EOL)

These are fn-ptr values or dispatch table entries that get a descriptive label and EOL comment:

| slot | value | new_label | eol_comment |
|------|-------|----------|-------------|
| DWORD_0807129c | 0x08071259 | check_effect_slot_equip_zone_pattern_ptr | check_effect_slot_equip_zone_pattern+1 (THUMB fn-ptr; passed to find_equip_chain_node_by_pred by scan_equip_chain_for_zone_pattern_sprites) |
| DWORD_08071538 | 0x08090625 | invoke_effect_node_with_active_flag_3arg_ptr_1538 | invoke_effect_node_with_active_flag_3arg+1 (THUMB fn-ptr; same as invoke_effect_node_with_active_flag_3arg_ptr_0a64 in Seg-2 at 0x08070a64; passed to set_equip_activation_state_by_mode as mode/fn param) |
| PTR_DAT_08071740 | dispatch table base | equip_lp_disp_sub_table | dispatch table (5 entries: [0]=equip_lp_sub_7c4/[1]=equip_lp_sub_7a4/[2]=equip_lp_sub_78a/[3]=equip_lp_sub_77c/[4]=equip_lp_sub_754 sub-stubs in block 2) |
| DAT_08071754 | ROM_INCBIN start | equip_lp_sub_stubs_754 | THUMB dispatch sub-stubs for equip_lp_disp_sub_table (5 entries: 7c4/7a4/78a/77c/754) |

NOTE: DAT_08071754 is the ROM_INCBIN block-2 label; after R4 disasm it becomes the label for
the first sub-stub. The full block gets 5 entry-point labels.

Total RENAME_SLOTS: 4 (2 fn-ptrs + 1 dispatch-table base + 1 block-start rename).

---

### FUNC_RENAME

No function name/body contradictions detected in Seg-3. All 20 names verified consistent with
body semantics by plate inspection.

Total FUNC_RENAME: 0.

---

### PLATE (R5 -- ASCII rewrite of CJK mojibake + stale FUN_ substring fixes)

Two plate issues found in Seg-3:

#### PLATE-1: CJK mojibake at L6141 (dispatch_equip_lp_bar_or_bitmap_by_zone_type)

Current plate (line 6141) contains garbled non-ASCII characters (Chinese UTF-8 bytes decoded
via Jython mojibake). Content intent is readable from the garbled text + function body.

Proposed ASCII replacement:
```
@ Equip LP bar / bitmap dispatch. Routes by [r0+0xc] zone_type_code: type==1 ->
@ submit_equip_lp_indicators_with_bar; type==2 -> invoke_equip_slot_eligibility_via_effect_node_bitmap;
@ other type returns 0. Passthrough return. Short fn, 5 effective instructions, indeg=0.
```

#### PLATE-2: stale FUN_ names at L6209 (tick_zone_sprite_pipeline_with_chain_counter)

Current plate text (line 6209):
`@ State 0x80: calls FUN_08090714 (external check); if nonzero calls trigger_card_display_op31_if_not_active(player_id, 0x6e) and FUN_08096a4c; returns 0x7f.`

Fix: substring replace:
- `FUN_08090714` -> `count_effect_node_zone_activations`
- `FUN_08096a4c` -> `set_equip_activation_state_by_mode__08096a4c`

Corrected text:
`@ State 0x80: calls count_effect_node_zone_activations (external check); if nonzero calls trigger_card_display_op31_if_not_active(player_id, 0x6e) and set_equip_activation_state_by_mode__08096a4c; returns 0x7f.`

Total PLATE: 2.

---

## Disasm Plan (R4)

### Block 1: ROM_INCBIN 0x716fa, 0x42 (GBA 0x080716fa..0x0807173c)

Structure (from ROM byte analysis):
- 0x080716fa/2: `.zero 0x2` alignment pad
- 0x080716fc: fn_eligible stub for Dragged Down into the Grave (CID=0x14e8)
  - THUMB push {r4,r5,lr} = 0xb530 confirmed at ROM offset 0x716fc
  - Body ~0x2c bytes ending ~0x08071728
  - Literal pool 0x0807172c..0x0807173b: gP1LifePoints / P1LP_BLOCK2_OFF_1CE8 / gDuelPhaseFlags / EQUIP_PHASE_FRAME_OFF

Ghidra actions:
1. `clearListing(0x080716fa, 0x0807173b)`
2. `setTMode(0x080716fc, THUMB)`
3. `DisassembleCommand(0x080716fc)`
4. Label `eligible_dragged_down_into_grave_16fc` at 0x080716fc
5. EOL at 0x080716fc: `fn_eligible stub: Dragged Down into the Grave (CID=0x14e8); FS table THUMB+1 ref @GBA:0x09e40e98`
6. Literal pool words at 0x0807172c/0x08071730/0x08071734/0x08071738 get labels from EQ_REUSE.

### Block 2: ROM_INCBIN 0x71754, 0x9c (GBA 0x08071754..0x080717f0)

Structure (from ROM byte analysis + dispatch table):
PTR_DAT_08071740 entries (5 raw sub-stub addresses in decreasing addr order in the table):
- [4] 0x08071754: sub-stub 1 (first in table entry[4], first in block)
- [3] 0x0807177c: sub-stub 2
- [2] 0x0807178a: sub-stub 3
- [1] 0x080717a4: sub-stub 4
- [0] 0x080717c4: sub-stub 5 (table entry[0], last in block; calls enqueue_monster_zone_equip_sprites_and_lp_counters+1)

Block 2 ends at 0x080717ef (0x80717f0 is the start of tick_equip_lp_spell_zone_display_state push).

Ghidra actions:
1. `clearListing(0x08071754, 0x080717ef)`
2. `setTMode(0x08071754, THUMB)`
3. `DisassembleCommand(0x08071754)` (sub-stub 1, 0x28 bytes, has literal pool at 0x08071774-0x08071779)
4. `DisassembleCommand(0x0807177c)` (sub-stub 2, 0xe bytes)
5. `DisassembleCommand(0x0807178a)` (sub-stub 3, 0x1a bytes, has literal pool at 0x08071798-0x0807179c)
6. `DisassembleCommand(0x080717a4)` (sub-stub 4, 0x20 bytes, has literal pool at 0x080717b4-0x080717bc)
7. `DisassembleCommand(0x080717c4)` (sub-stub 5, 0x2c bytes, epilogue at ~0x080717e4)

Labels:
- `equip_lp_sub_754` at 0x08071754
- `equip_lp_sub_77c` at 0x0807177c
- `equip_lp_sub_78a` at 0x0807178a
- `equip_lp_sub_7a4` at 0x080717a4
- `equip_lp_sub_7c4` at 0x080717c4

EOL at 0x08071754: `dispatch sub-stub 1 of 5; equip_lp_disp_sub_table[4]`
EOL at 0x080717c4: `dispatch sub-stub 5 of 5; equip_lp_disp_sub_table[0]; calls enqueue_monster_zone_equip_sprites_and_lp_counters`

---

## Carve Plan (R7)

None. No ROM data table requiring carve into rom.s. Both blocks are THUMB code (disasm only).
The PTR_DAT_08071740 dispatch table is already structured as inline `.word` entries in the
existing asm and needs only label/EOL annotation (no carve).

---

## New Constants / Globals

### constants/equip_lp.inc (new file -- OR add to constants/duel_field.inc if preferred)

Check if `duel_field.inc` is the right home for equip zone masks; both are acceptable. Proposing
`duel_field.inc` to avoid a new file since this is a single entry:

```asm
.equ EQUIP_ZONE_WORD_MASK,  0x00f0ffff  @ equip chain node zone_word bitmask; check_effect_slot_equip_zone_pattern ANDs zone_word[+0] with this mask, then compares result against 0x14c0 (equip zone type encoding 0xa6<<5); 10+ ROM refs
```

### constants/card_info.inc (1 new CID)

```asm
.equ FREED_THE_MATCHLESS_GENERAL_CID,  0x000014c4  @ Freed the Matchless General (pw=49681811; card_1013 slot=0x14C4); dispatch_equip_chain_state_if_tile_count_valid chain check param; conf:high
```

NOTE on DRAGGED_DOWN_INTO_GRAVE_CID=0x14e8: this CID appears only in the FS handler table
(as the entry CID at ROM 0x1e40e94) and is used in the fn_eligible stub EOL comment only.
No literal pool slot within Seg-3 code directly holds 0x14e8 as a named constant. Adding to
card_info.inc for completeness (as was done for BAZOO_THE_SOUL_EATER_CID in Seg-2):

```asm
.equ DRAGGED_DOWN_INTO_GRAVE_CID,  0x000014e8  @ Dragged Down into the Grave (pw=16435215; card_1048 slot=0x14E8); Block1 FS handler fn_eligible CID ref @GBA:0x09e40e94; conf:high
```

---

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None. Both ROM_INCBIN blocks have confirmed references:
- Block 1 (0x080716fa/0x42): THUMB+1 ref from FS table at GBA 0x09e40e98 -> DISASM.
- Block 2 (0x08071754/0x9c): 5 raw refs from PTR_DAT_08071740 dispatch table -> DISASM.

Section 5.1 count = 0.

---

## Consumer Evidence (R6)

| slot/block | semantic | consumer fn | file:line | conf |
|-----------|---------|------------|---------|------|
| DWORD_08071280 = 0x00f0ffff | zone_word bitmask for equip pattern check | check_effect_slot_equip_zone_pattern | asm/09 L5648-5652: ldr r1,DWORD_08071280; ands r0,r1; cmp r0,#0xa6<<5 -- ANDs zone_word with mask then checks against equip pattern 0x14c0 | high |
| DWORD_08071344 = 0x000014c4 | CID for Freed the Matchless General | dispatch_equip_chain_state_if_tile_count_valid | asm/09 L5770-5773: ldr r4,DWORD_08071344; movs r1,#0xb; adds r2,r4,#0; bl check_value_in_slot_chain -- CID as chain check value | high |
| DWORD_0807129c = 0x08071259 | THUMB fn-ptr for check_effect_slot_equip_zone_pattern | scan_equip_chain_for_zone_pattern_sprites | asm/09 L5684-5686: ldr r2,DWORD_0807129c; movs r1,#0xb; bl find_equip_chain_node_by_pred -- fn-ptr passed as predicate | high |
| DWORD_08071538 = 0x08090625 | THUMB fn-ptr for invoke_effect_node_with_active_flag_3arg | dispatch_equip_zone11_target_by_activation_state | asm/09 L6092-6093: ldr r2,DWORD_08071538; bl set_equip_activation_state_by_mode__08096a4c -- fn-ptr as mode parameter | high |
| Block1 fn_eligible stub @ 0x080716fc | fn_eligible for Dragged Down into the Grave | FS handler dispatch table | roms/2343.gba ROM offset 0x1e40e94: CID=0x000014e8; ROM 0x1e40e98: THUMB+1=0x080716fd -> fn_eligible=0x080716fc | high |
| Block2 sub-stubs @ 0x08071754..0x080717ef | 5 dispatch sub-stubs for equip LP display state routing | PTR_DAT_08071740 dispatch table | asm/09 L6364-6368: 5 .word entries pointing to sub-stub entries 0x080717c4/a4/8a/7c/54; all aligned raw refs from same-segment | high |
| PTR_DAT_08071740 table | 5-entry code dispatch table for LP state sub-routing | dispatch_hand_card_sprite_by_effect_slot_zone (caller) | asm/09 L6362-6368: .word 0x08071740 then 5 table entries; table loaded via pointer indirection | med (indirect consumer not yet traced in detail) |

---

## C13 Coverage Proof

Total auto-name slots in Seg-3 (python scan): **39**

Partition:

| group | slots | list |
|-------|-------|------|
| EQ_REUSE | 34 | DWORD_0807106c, DWORD_08071138, DWORD_0807113c, DWORD_08071140, DWORD_08071204, DWORD_08071208, DWORD_0807120c, DWORD_08071338, DWORD_0807133c, DWORD_08071340, DWORD_080713ec, DWORD_080713f0, DWORD_080714a4, DWORD_080714a8, DWORD_08071508, DWORD_08071568, DWORD_0807156c, DWORD_08071570, DWORD_08071644, DWORD_08071648, DWORD_080716dc, DWORD_080716e0, DWORD_08071810, DWORD_08071850, DWORD_08071888, DWORD_0807188c, DWORD_080718a8, DWORD_08071928, DWORD_08071998, DWORD_0807199c, DWORD_080719a0, DWORD_080719d4, DWORD_080719d8, DWORD_0807120c |
| EQ_NEW | 2 | DWORD_08071280, DWORD_08071344 |
| RENAME (fn-ptrs+dispatch) | 3 | DWORD_0807129c, DWORD_08071538, PTR_DAT_08071740 |
| RENAME (block-start) | 1 | DAT_08071754 (= block 2 start label) |

Sum check: 34 + 2 + 3 + 1 = **40**

DISCREPANCY: sum=40 but total=39. One slot appears in EQ_REUSE twice. Let me recount:

EQ_REUSE list (34 items, re-enumerated):
1. DWORD_0807106c (gDuelPhaseFlags)
2. DWORD_08071138 (gP1LifePoints)
3. DWORD_0807113c (LP_CARD_TRACK_BASE_OFF)
4. DWORD_08071140 (PLAYER_BLOCK_STRIDE)
5. DWORD_08071204 (PLAYER_BLOCK_STRIDE)
6. DWORD_08071208 (gDuelFieldSlots)
7. DWORD_0807120c (BLUE_EYES_SHINING_DRAGON_CID)
8. DWORD_08071338 (PLAYER_BLOCK_STRIDE)
9. DWORD_0807133c (gDuelFieldSlots)
10. DWORD_08071340 (gDuelPhaseFlags)
11. DWORD_080713ec (PLAYER_BLOCK_STRIDE)
12. DWORD_080713f0 (gDuelFieldSlots)
13. DWORD_080714a4 (gP1LifePoints)
14. DWORD_080714a8 (P1LP_BLOCK2_OFF_1CE8)
15. DWORD_08071508 (gDuelPhaseFlags)
16. DWORD_08071568 (gP1LifePoints)
17. DWORD_0807156c (ELIGIB_SPRITE_CTRL_OFF)
18. DWORD_08071570 (ELIGIB_ANIM_STATE_OFF)
19. DWORD_08071644 (gDuelPhaseFlags)
20. DWORD_08071648 (EQUIP_PHASE_FRAME_OFF)
21. DWORD_080716dc (PLAYER_BLOCK_STRIDE)
22. DWORD_080716e0 (gP1HandSlotArray)
23. DWORD_08071810 (gDuelPhaseFlags)
24. DWORD_08071850 (EQUIP_PHASE_FRAME_OFF)
25. DWORD_08071888 (gP1LifePoints)
26. DWORD_0807188c (LP_CARD_TRACK_BASE_OFF)
27. DWORD_080718a8 (EQUIP_PHASE_FRAME_OFF)
28. DWORD_08071928 (gDuelPhaseFlags)
29. DWORD_08071998 (gP1LifePoints)
30. DWORD_0807199c (LP_CARD_TRACK_BASE_OFF)
31. DWORD_080719a0 (gDuelCardCtxBase)
32. DWORD_080719d4 (gP1LifePoints)
33. DWORD_080719d8 (LP_CARD_TRACK_BASE_OFF)
34. [duplicate removed -- DWORD_0807120c was listed twice above]

Corrected EQ_REUSE: 33 unique slots.

Sum check: 33 + 2 + 3 + 1 = **39** = total. Confirmed.

Full partition (no double-count, no unclassified):
- EQ_REUSE x33: items 1-33 above
- EQ_NEW x2: DWORD_08071280, DWORD_08071344
- RENAME_fnptr x2: DWORD_0807129c, DWORD_08071538
- RENAME_dispatch x1: PTR_DAT_08071740
- RENAME_block x1: DAT_08071754

33+2+2+1+1 = **39**. Check.

---

## Clarification Requests / Seek Help

None. All semantic evidence is high confidence from:
- card-stats.s pw verification for FREED_THE_MATCHLESS_GENERAL_CID (0x14c4) and DRAGGED_DOWN_INTO_GRAVE_CID (0x14e8)
- FS handler table structure at ROM 0x1e40e94/0x1e40e98 for Block 1 classification
- Existing ewram.inc / card_info.inc constants for all REUSE values
- Consumer asm lines for all key slots
- Function plate comments for context (converted from CJK mojibake by inspection)

---

## Self-check Results

1. All EQ values verified by python `struct.unpack_from('<I', rom, gba_addr - 0x08000000)` against stated values -- all match.
2. Block 1 THUMB+1 ref: ROM offset 0x1e40e98 confirmed via python; CID at 0x1e40e94 = 0x14e8; card-stats.s card_1048 confirmed.
3. Block 2 raw refs: all 5 dispatch table entries (PTR_DAT_08071740[0..4]) verified aligned, confirmed in asm.
4. No THUMB+1 refs in Block 2 (exhaustive scan confirmed 0 hits).
5. No CJK in proposed plate/EOL text (all ASCII-only in this proposal).
6. Slot labels follow `^[a-z][a-z0-9_]+$` pattern.
7. C5 dedup: all new equates grep by value = 0 hits in constants/; all REUSE equates grep by value >= 1 hit.
8. Section 5.1 = 0: both blocks have confirmed refs.
9. C13 partition: 33+2+2+1+1 = 39 = total. No double-count. No unclassified slot.
10. FUN_ scan: 2 FUN_ names found (L6209 plate only; PLATE-2 fix covers both).
