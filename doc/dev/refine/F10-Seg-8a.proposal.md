# Refine Proposal: F10-Seg-8a  [0x08082290..0x08082b18)

**Split decision**: Seg-8 (113 slots, 2 ROM_INCBIN) is split at function boundary 0x08082b18.
Seg-8a covers [0x08082290..0x08082b18): 7 named fns + 2 ROM_INCBIN blocks + 1 JT. 49 slot defs total.
Seg-8b covers [0x08082b18..0x08083450): 12 fns, 67 slot defs total (3 PTR_ skipped).

---

## Segment Survey

### Function Entries in [0x08082290, 0x08082b18)

| addr | name | asm line |
|------|------|----------|
| 0x08082290 | tick_equip_activation_display_4state | L18116 |
| 0x08082494 (approx) | dispatch_equip_activation_display_if_slot_card_id_ok | L18400 |
| 0x08082510 (approx) | tick_equip_display_4state_with_effect_slot_array | L18457 |
| 0x0808263c (approx) | tick_equip_display_3state_with_effect_node_probe | L18611 |
| 0x08082744 (approx) | enqueue_equip_slot_sprite_with_attr_strip | L18749 |
| 0x08082770 (approx) | check_effect_slot_zone_field_by_type | L18778 |
| 0x080827d4 | ROM_INCBIN BLK1: fn_eligible_two_pronged_attack (entry) | L18836 |
| [0x080828ac] | JT 6x.word (0x18B, decoded in asm) | L18837 |
| 0x080828c4 | ROM_INCBIN BLK2: sub-stubs A/B/C/shared (entry DAT_080828c4) | L18844 |
| 0x080829bc | tick_equip_display_by_card_id_group_a_4state | L18859 |

### Residual Auto-Name Slots in Seg-8a (49 total)

```
L18134: DWORD_080822b0  .word 0x0201b290
L18229: DWORD_08082364  .word 0xfffc7fff
L18231: DWORD_08082368  .word 0x0201bb90
L18233: DWORD_0808236c  .word 0x00000868
L18235: DWORD_08082370  .word 0x0201c510
L18237: DWORD_08082374  .word 0x0201e2a0
L18239: DWORD_08082378  .word gP1LifePoints       [already symbolic]
L18255: DWORD_08082398  .word 0x00000103
L18257: DWORD_0808239c  .word 0x000001a1
L18268: DWORD_080823b0  .word gP1LifePoints       [already symbolic]
L18289: DWORD_080823d4  .word gP1LifePoints       [already symbolic]
L18291: DWORD_080823d8  .word 0x0201b290
L18314: DWORD_08082404  .word gP1LifePoints       [already symbolic]
L18316: DWORD_08082408  .word 0x0201bb90
L18345: DWORD_08082440  .word 0x0201e2a0
L18358: DWORD_0808245c  .word 0x080905e9
L18380: DWORD_08082488  .word gP1LifePoints       [already symbolic]
L18382: DWORD_0808248c  .word 0x00001d68
L18384: DWORD_08082490  .word 0x00001d6c
L18427: DAT_080824d8    .word 0x00000868
L18429: DAT_080824dc    .word 0x0201c510
L18445: DAT_080824fc    .word 0x0201e2a0
L18483: DWORD_08082544  .word 0x0201e2a0
L18485: DWORD_08082548  .word 0x000010d3
L18500: DWORD_08082564  .word 0x0201b290
L18533: DWORD_080825a4  .word 0xfffc7fff
L18535: DWORD_080825a8  .word 0x0805000d
L18556: DWORD_080825d4  .word gP1LifePoints       [already symbolic]
L18558: DWORD_080825d8  .word 0x00001d68
L18577: DWORD_080825fc  .word 0x00000199
L18600: DWORD_0808262c  .word gP1LifePoints       [already symbolic]
L18629: DWORD_0808265c  .word 0x0201b290
L18667: DWORD_080826a8  .word 0xfffc7fff
L18669: DWORD_080826ac  .word 0x0201e2a0
L18682: DWORD_080826c8  .word 0x0000010f
L18684: DWORD_080826cc  .word 0x080905e9
L18746: DWORD_08082740  .word 0x0201b290
L18775: DWORD_0808276c  .word 0xfffc7fff
L18843: DAT_080828c4    ROM_INCBIN entry label    [R4 disasm -> fn label]
L18876: DWORD_080829dc  .word 0x000012ed          [CID]
L18889: DWORD_080829f4  .word 0x0000183c          [CID]
L18891: DWORD_080829f8  .word 0x00001515          [CID]
L18899: DWORD_08082a04  .word 0x00001996          [CID]
L18926: DWORD_08082a30  .word 0x0201b290
L18966: DWORD_08082a80  .word 0xfffc7fff
L18968: DWORD_08082a84  .word gP1LifePoints       [already symbolic]
L18988: DWORD_08082aac  .word gP1LifePoints       [already symbolic]
L18990: DWORD_08082ab0  .word 0x000004b4
L19044: DWORD_08082b14  .word gP1LifePoints       [already symbolic]
```

Totals: 10 gP1LifePoints symbolic (RENAME), 1 DAT_ ROM_INCBIN (R4), 38 hex-value (EQ/REF).

### ROM_INCBIN Blocks

| label | addr | size | disposition |
|-------|------|------|-------------|
| (unlabeled) | 0x08082_7d4 | 0xd8 (216B) | R4 disasm |
| DAT_080828c4 | 0x08082_8c4 | 0xf8 (248B) | R4 disasm |

JT at 0x080828ac (6x.word, 0x18B) is already decoded in asm - no action required.

---

## Data Block Classification (Rule 2/3)

### BLK1: 0x08082_7d4 / 0xd8 [0x827d4..0x828ac)

ref-scan (python, roms/2343.gba):
```
raw   0x080827d4 => 0 hits
THUMB 0x080827d5 => 1 hit  @ 0x09e3fc60  (FS handler table)
raw   0x08082802 => 1 hit  context: FS-loaded compressed blob (coincidental)
raw   0x08082808 => 1 hit  context: compressed asset (coincidental)
```

FS table entry verification:
- ROM[0x09e3fc4c] = 0x000012e7 (CID = Two-Pronged Attack)
- ROM[0x09e3fc60] = 0x080827d5 (fn_eligible+1 = THUMB+1 ref to 0x080827d4)
- Entry format: [CID @+0x0, ..., fn_eligible+1 @+0x14]: 0x09e3fc60 - 0x09e3fc4c = 0x14. Confirmed.

Judgment: **R4 disasm** (1 valid THUMB+1 ref from FS handler table; fn_eligible for CID=0x12e7).

BLK1 structure (from ROM byte inspection):
- 0x080827d4: PUSH b5f0 -> fn_eligible_two_pronged_attack entry (single PUSH in entire block)
- Block contains fn_eligible body + dispatch sub-stubs accessed via JT at 0x828ac
- No additional PUSH within BLK1 -> sub-stubs are inline (no own stack frame)
- JT entries: [0x828c4, 0x82954, 0x828f4, 0x82954, 0x82924, 0x82954] -> 4 unique targets in BLK2

### BLK2: DAT_0x080828c4 / 0xf8 [0x828c4..0x829bc)

ref-scan:
```
raw   0x080828c4 => 1 hit  @ 0x080828ac  (JT entry in decoded asm, already .word 0x080828c4)
THUMB 0x080828c5 => 1 hit  context: 0x08af1... -> compressed data (coincidental, chaotic context)
raw   0x080828f4 => 0 hits
raw   0x08082924 => 0 hits
raw   0x08082954 => 0 hits
THUMB 0x080828cd => coincidental compressed (verified chaotic bytes)
THUMB 0x080828ed => coincidental compressed
THUMB 0x0808297b => coincidental compressed
```

The single valid ref to 0x080828c4 is from the JT at 0x828ac (already decoded in asm). Sub-targets 0x828f4/0x82924/0x82954 have 0 raw refs (inline dispatch from JT, no separate fn-ptr table).

Judgment: **R4 disasm** (JT at 0x828ac directly indexes 4 entry points; 0x82954 is shared exit reached by 3 JT entries [indices 1,3,5]).

---

## Symbolization Plan

### EQ_SLOTS (data-equate; value-grep evidence)

**REUSE existing constants (C5 grep by VALUE -> hit):**

| slot | value | const_name | grep evidence |
|------|-------|-----------|---------------|
| DWORD_080822b0 L18134 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_08082364 L18229 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_08082368 L18231 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc:317 |
| DWORD_0808236c L18233 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 |
| DWORD_08082370 L18235 | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 |
| DWORD_08082374 L18237 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 |
| DWORD_08082398 L18255 | 0x00000103 | EQUIP_ACT_SCORE_MODE_103 | duel_field.inc:350 |
| DWORD_080823d8 L18291 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_08082408 L18316 | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc:317 |
| DWORD_08082440 L18345 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 |
| DWORD_0808248c L18382 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc:422 |
| DWORD_08082490 L18384 | 0x00001d6c | ELIGIB_ANIM_STATE_OFF | ewram.inc:423 |
| DAT_080824d8 L18427 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc:251 |
| DAT_080824dc L18429 | 0x0201c510 | gDuelFieldSlots | ewram.inc:314 |
| DAT_080824fc L18445 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 |
| DWORD_08082544 L18483 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 |
| DWORD_08082548 L18485 | 0x000010d3 | TRIGGER_OP_PARAM_10D3 | duel_field.inc:314 |
| DWORD_08082564 L18500 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_080825a4 L18533 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_080825d8 L18558 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc:422 |
| DWORD_080825fc L18577 | 0x00000199 | lookup_equip_score_mooyan_p1 | duel_field.inc:323 |
| DWORD_0808265c L18629 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_080826a8 L18667 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_080826ac L18669 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc:218 |
| DWORD_080826c8 L18682 | 0x0000010f | DRAW_DECIMAL_WIN_LABEL_ARG | duel_field.inc:50 |
| DWORD_08082740 L18746 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_0808276c L18775 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_08082a30 L18926 | 0x0201b290 | gDuelPhaseFlags | ewram.inc:353 |
| DWORD_08082a80 L18966 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc:134 |
| DWORD_08082ab0 L18990 | 0x000004b4 | EQUIP_ACTIVATION_AUX_OFF | duel_field.inc:357 |

**NEW constants (C5 grep by VALUE -> 0 hits):**

| slot | value | proposed const_name | evidence |
|------|-------|---------------------|---------|
| DWORD_0808245c L18358 | 0x080905e9 | set_equip_activation_state_by_mode_alt_fn_ptr | asm/10 L16830: "set_equip_activation_state_by_mode_alt+1 (THUMB fn-ptr)"; 20 ROM refs; fn at 0x080905e8 (PUSH b570 confirmed); grep constants/\*.inc "0x080905e9" = 0 hits; conf: high |
| DWORD_080826cc L18684 | 0x080905e9 | set_equip_activation_state_by_mode_alt_fn_ptr | same const (2nd occurrence) |
| DWORD_080825a8 L18535 | 0x0805000d | check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr | naming-proposals.csv:1115 "check_equip_slot_eligible_by_card_id_and_prereqs" @ 0x0805000c; THUMB+1=0x0805000d; 114 ROM refs; grep constants/\*.inc "0x0805000d" = 0 hits; conf: high |
| DWORD_0808239c L18257 | 0x000001a1 | EQUIP_DISPLAY_OP_PARAM_1A1 | r2 arg to invoke_card_display_op_0x31_sub3_with_packed_params (asm/10 L18252); sibling to r0=0x103 (EQUIP_ACT_SCORE_MODE_103) + r1=0xd0<<1=0x1a0 + r3=0xd1<<1=0x1a2; 15 ROM refs; grep constants/\*.inc "0x000001a1" = 0 hits; conf: med (domain confirmed, exact op semantic not named) |

**CID slots (Seg-8a):**

| slot | value | disposition | evidence |
|------|-------|-------------|---------|
| DWORD_080829dc L18876 | 0x000012ed | NEW: GRAVEDIGGER_GHOUL_CID | card_info.inc grep "0x000012ed" = 0 hits; card-stats.s card_0675 "Gravedigger Ghoul" pw=82542267; conf: high |
| DWORD_080829f4 L18889 | 0x0000183c | REUSE: DARK_BLADE_THE_DRAGON_KNIGHT_CID | card_info.inc:~500 grep "0x0000183c" -> hit; exact name DARK_BLADE_THE_DRAGON_KNIGHT_CID; conf: high |
| DWORD_080829f8 L18891 | 0x00001515 | NEW: DISAPPEAR_CID | card_info.inc grep "0x00001515" = 0 hits; card-stats.s card_1087 "Disappear" pw=24623598; conf: high |
| DWORD_08082a04 L18899 | 0x00001996 | REUSE: WHITE_HORNS_DRAGON_CID | card_info.inc grep "0x00001996" -> hit; exact name WHITE_HORNS_DRAGON_CID; conf: high |

### REF_SLOTS (USER-label + DATA-ref)

No standalone USER-label REF slots in Seg-8a. All global references go through EQ_SLOTS above.

### RENAME_SLOTS (drop auto-name prefix; keep symbolic value; add EOL)

**gP1LifePoints already-symbolic (10 slots):**

| slot | label_after | eol |
|------|-------------|-----|
| DWORD_08082378 L18239 | gP1LifePoints | gP1LifePoints (EWRAM LP tracking base; ewram.inc) |
| DWORD_080823b0 L18268 | gP1LifePoints | gP1LifePoints |
| DWORD_080823d4 L18289 | gP1LifePoints | gP1LifePoints |
| DWORD_08082404 L18314 | gP1LifePoints | gP1LifePoints |
| DWORD_08082488 L18380 | gP1LifePoints | gP1LifePoints |
| DWORD_080825d4 L18556 | gP1LifePoints | gP1LifePoints |
| DWORD_0808262c L18600 | gP1LifePoints | gP1LifePoints |
| DWORD_08082a84 L18968 | gP1LifePoints | gP1LifePoints |
| DWORD_08082aac L18988 | gP1LifePoints | gP1LifePoints |
| DWORD_08082b14 L19044 | gP1LifePoints | gP1LifePoints |

### FUNC_RENAME

None identified in Seg-8a. All 7 named functions have semantically correct names per asm plates.

### PLATE (R5)

**21 mojibake lines in full Seg-8 (lines 18116..20393). In Seg-8a specifically (18116..19056):**

Functions with non-ASCII plates needing full ASCII rewrite (Ghidra Jython written CJK -> mojibake):

1. **dispatch_equip_activation_display_if_slot_card_id_ok** (L18399):
   ASCII rewrite: "Equip activation display router, card-ID prerequisite. indeg=0, Sub-type A. Receives card_entry_ptr(r0) and secondary_ptr(r1). Extracts player_id(bit0) and slot_idx(bits[5:1]) from card_entry[+2]. Computes target slot card_id at [0x0201c510+player*0x868+slot*0x14]; if mismatch returns -1. Reads confirm_flag at [gDuelCardCtxBase+player*4+8]; if==1 calls select_equip_target_slot_by_effect_strategy; else calls tick_equip_activation_display_3state. Passes result through."

2. **tick_equip_display_4state_with_effect_slot_array** (L18457):
   ASCII rewrite: "Equip display 4-state machine with effect slot array push. indeg=0, Sub-type A. confirm_flag==1 fast path: select_equip_target_slot_by_effect_strategy + push_to_effect_slot_array, return 1. Otherwise 4-state machine at [gDuelState+0x96*8]: state 0: trigger op 0x65 + clear card_entry flags + set_equip_activation_state_by_mode; state 1: check_activation_display_state_is_confirmed, confirmed->enqueue_equip_slot_sprite_with_code_rotation; state 2: invoke sub3(0x7f,0x198,0x199); state 3: push_to_effect_slot_array + set_lp_display_row_type15, return 1. Exit Sub-case E."

3. **tick_equip_display_3state_with_effect_node_probe** (L18611):
   ASCII rewrite: "Equip display 3-state machine with effect node dual-scan. indeg=0, Sub-type A. Reads [gDuelState+0x96*8]: state 0: clear flags; node_count>1 and confirmed->select_equip_target_slot; unconfirmed->trigger op 0x10f + set_equip_activation_state; count<=1->dual loop invoke_effect_node_handler_3arg(slot 0..1, zone 0..4), hit->enqueue_sprite + state:=2. state 1: tick_equip_activation_display_3state. state 2: resolve_slot_card_id_for_pair -> strh card_id to [entry+0xc], return 1. Exit Sub-case E."

4. **enqueue_equip_slot_sprite_with_attr_strip** (L18749, 3 comment lines L18749..18753):
   ASCII rewrite: "Equip slot sprite enqueue helper, clears attr bits first. Receives effect_node_ptr(r0). ANDs [r0+4] with 0xfffc7fff to clear bits[15:14], ANDs [r0+6] with ~0x1d=0xe2 to clear state flag bits. Constants: ATTR_MASK=0xfffc7fff (clears bits[15:14]); FLAG_MASK=~0x1d=0xe2 (clears state bits[4:0]); SLOT_IDX_SHIFT=9 (bits[13:9] extract: lsls#0x12/lsrs#0x17 net shift 5)."

5. **check_effect_slot_zone_field_by_type** (L18778, 2 comment lines L18778..18781):
   ASCII rewrite: "Effect slot zone-field type check. Receives effect_node_ptr(r0), player_id_or_side(r1), slot_type_qualifier(r2). Push {r4,r5,r6,r7,lr}. ZONE_FIELD_BITS=bits[4:3] of [r5+6] (3-case dispatch [0..2])."

6. **tick_equip_display_by_card_id_group_a_4state** (L18846):
   ASCII rewrite: "Equip display 4-state machine routed by card_id group A. card_id BST dispatch: 0x12ed(Gravedigger Ghoul)->type 2, 0x12f9(Soul Release, computed DWORD_080829dc+0xc=0x12ed+0xc)->type 5, 0x1480(Kycoo the Ghost Destroyer, computed 0xa4<<5)->type 2, 0x1515(Disappear)->type 1, 0x183c(Dark Blade the Dragon Knight)->type 3, 0x1996(White Horns Dragon)->type 5. After BST reads IWRAM state at [IWRAM_BASE+0x4b0]. State 0: clear attr_bits + dispatch_card_effect_activation + format_game_text + trigger. State 1: check_confirmed->enqueue_sprite or step-1. State 2: load [IWRAM+0x4b4] as palette_id, call get_effect_slot_entry_ptr_by_palette_id + find_slot_by_palette_id_in_table + pack_equip_slot_sprite_with_code_attr. State>=3: step+1 return 1."

---

## Disasm Plan (R4)

### BLK1: fn_eligible_two_pronged_attack @ 0x08082_7d4

Entry: 0x080827d4 (PUSH b5f0)
Range: [0x080827d4, 0x080828ac) = 0xd8 bytes THUMB

Label plan:
- `fn_eligible_two_pronged_attack` @ 0x080827d4 (fn_eligible body for CID=TWO_PRONGED_ATTACK_CID=0x12e7)
- Sub-dispatch stubs within BLK1 are inlined (no separate PUSH); label as needed by JT targets.
- JT at 0x828ac already decoded; no new labels needed in JT itself.

Note: THUMB+1 ref from FS table at 0x09e3fc60 confirmed: ROM[0x09e3fc60]=0x080827d5.

### BLK2: sub-stubs @ 0x08082_8c4..0x080829bc

Entry points from JT at 0x828ac:
- `equip_sub_stub_a` @ 0x080828c4  (JT[0], JT unique)
- `equip_sub_stub_b` @ 0x080828f4  (JT[2])
- `equip_sub_stub_c` @ 0x08082924  (JT[4])
- `equip_sub_stub_shared_exit` @ 0x08082954  (JT[1,3,5] - shared by 3 entries)

Range: [0x080828c4, 0x080829bc) = 0xf8 bytes THUMB
Label DAT_080828c4 -> `equip_sub_stub_a`

Per-stub naming TBD pending disassembly (use equip_sub_stub_<letter> or functional name from body).

---

## Section 5.1 Registration (Rule 3, 0-reference blocks)

No 0-reference ROM_INCBIN blocks in Seg-8a. Both BLK1 and BLK2 have valid references.

---

## Consumer Evidence (R6)

| slot | consumer | file:line | confidence |
|------|----------|-----------|-----------|
| 0x000012ed (GRAVEDIGGER_GHOUL_CID) | tick_equip_display_by_card_id_group_a_4state BST left leaf | asm/10 L18876 ldr+cmp+beq | high |
| 0x0000183c (DARK_BLADE_THE_DRAGON_KNIGHT_CID) | tick_equip_display_by_card_id_group_a_4state BST right | asm/10 L18889 | high |
| 0x00001515 (DISAPPEAR_CID) | tick_equip_display_by_card_id_group_a_4state BST | asm/10 L18891 | high |
| 0x00001996 (WHITE_HORNS_DRAGON_CID) | tick_equip_display_by_card_id_group_a_4state BST right leaf | asm/10 L18899 | high |
| 0x000004b4 (EQUIP_ACTIVATION_AUX_OFF) | gDuelPhaseFlags+0x4b4 state read in tick_equip_display_by_card_id_group_a_4state | asm/10 L18990 ldr + ldr base=gDuelPhaseFlags | high |
| 0x080905e9 (set_equip_activation_state_by_mode_alt_fn_ptr) | loaded into r2 passed to set_equip_activation_state_by_mode__08096a4c | asm/10 L18358+L18684 | high |
| 0x0805000d (check_equip_slot_eligible_..._fn_ptr) | loaded into r2 passed to set_equip_activation_state_by_mode__08096a4c | asm/10 L18535 | high |
| 0x000001a1 (EQUIP_DISPLAY_OP_PARAM_1A1) | r2 arg to invoke_card_display_op_0x31_sub3_with_packed_params | asm/10 L18252 | med |

---

## C5 Dedup Evidence Summary

**REUSE (by-value grep hit in constants/):**
- 0x0201b290 -> ewram.inc:353 gDuelPhaseFlags
- 0xfffc7fff -> duel_field.inc:134 DUAL_LABEL_RENDER_STATE_CLEAR
- 0x0201bb90 -> ewram.inc:317 gEquipChainSlotRefs
- 0x00000868 -> ewram.inc:251 PLAYER_BLOCK_STRIDE
- 0x0201c510 -> ewram.inc:314 gDuelFieldSlots
- 0x0201e2a0 -> ewram.inc:218 gDuelCardCtxBase
- 0x00000103 -> duel_field.inc:350 EQUIP_ACT_SCORE_MODE_103
- 0x00001d68 -> ewram.inc:422 ELIGIB_SPRITE_CTRL_OFF
- 0x00001d6c -> ewram.inc:423 ELIGIB_ANIM_STATE_OFF
- 0x000010d3 -> duel_field.inc:314 TRIGGER_OP_PARAM_10D3
- 0x00000199 -> duel_field.inc:323 lookup_equip_score_mooyan_p1
- 0x0000010f -> duel_field.inc:50 DRAW_DECIMAL_WIN_LABEL_ARG
- 0x0000183c -> card_info.inc DARK_BLADE_THE_DRAGON_KNIGHT_CID
- 0x00001996 -> card_info.inc WHITE_HORNS_DRAGON_CID
- 0x000004b4 -> duel_field.inc:357 EQUIP_ACTIVATION_AUX_OFF

**NEW (by-value grep -> 0 hits):**
- 0x080905e9 -> set_equip_activation_state_by_mode_alt_fn_ptr (duel_field.inc NEW)
- 0x0805000d -> check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr (duel_field.inc NEW)
- 0x000001a1 -> EQUIP_DISPLAY_OP_PARAM_1A1 (duel_field.inc NEW)
- 0x000012ed -> GRAVEDIGGER_GHOUL_CID (card_info.inc NEW; card_0675 pw=82542267)
- 0x00001515 -> DISAPPEAR_CID (card_info.inc NEW; card_1087 pw=24623598)

---

## C8 Stale FUN_ Scan

```
grep 'FUN_' asm/10_equip_effect_dispatch.s | grep -n '.' | awk -F: 'NR>=18116 && NR<=19056'
```
Result: 0 hits in [L18116..L19056]. No stale FUN_ references in Seg-8a.

---

## C13 Coverage Verification

Seg-8a total slot defs: 49
- gP1LifePoints symbolic (RENAME): 10  (L18239,18268,18289,18314,18380,18556,18600,18968,18988,19044)
- ROM_INCBIN entry label (R4): 1  (DAT_080828c4 L18843)
- Hex-value EQ/REF slots: 38
  - REUSE EQ: 30
  - NEW EQ: 5 (set_equip_activation_state_by_mode_alt_fn_ptr x2 = 1 unique const, check_equip_slot_eligible_fn_ptr x1, EQUIP_DISPLAY_OP_PARAM_1A1 x1, GRAVEDIGGER_GHOUL_CID x1, DISAPPEAR_CID x1)
  - CID REUSE: 2 (DARK_BLADE_THE_DRAGON_KNIGHT_CID, WHITE_HORNS_DRAGON_CID)

Union: 10 + 1 + 38 = 49 = total. COVERAGE 100%.

---

## New Constants Required (Seg-8a)

File: `constants/card_info.inc`
```
.equ GRAVEDIGGER_GHOUL_CID,    0x000012ed  @ Gravedigger Ghoul (pw=82542267; card_0675); tick_equip_display_by_card_id_group_a_4state BST; C5 grep=0 (new); conf: high
.equ DISAPPEAR_CID,            0x00001515  @ Disappear (pw=24623598; card_1087); tick_equip_display_by_card_id_group_a_4state BST; C5 grep=0 (new); conf: high
```

File: `constants/duel_field.inc`
```
.equ set_equip_activation_state_by_mode_alt_fn_ptr, 0x080905e9  @ THUMB+1 ptr to set_equip_activation_state_by_mode_alt (fn at 0x080905e8); 20 ROM refs; asm/10 Seg-8a x2 slots; C5 grep=0 (new); conf: high
.equ check_equip_slot_eligible_by_card_id_and_prereqs_fn_ptr, 0x0805000d  @ THUMB+1 ptr to check_equip_slot_eligible_by_card_id_and_prereqs (fn at 0x0805000c, naming-proposals.csv:1115); 114 ROM refs; asm/10 Seg-8a x1 slot; C5 grep=0 (new); conf: high
.equ EQUIP_DISPLAY_OP_PARAM_1A1, 0x000001a1  @ r2 arg to invoke_card_display_op_0x31_sub3_with_packed_params; sibling to EQUIP_ACT_SCORE_MODE_103(r0=0x103) + r1=0x1a0 + r3=0x1a2 in tick_equip_activation_display_4state; 15 ROM refs; C5 grep=0 (new); conf: med
```
