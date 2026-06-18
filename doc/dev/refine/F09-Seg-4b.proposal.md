# Refine Proposal: F09-Seg-4b  [0x08072404..0x08072d20)

> This is the second half of the Seg-4 split.
> Seg-4a: [0x080719fc..0x08072404) -- proposal at F09-Seg-4.proposal.md.
> Seg-4b: [0x08072404..0x08072d20) -- 26 auto-name slots, 4 ROM_INCBIN blocks (B5-B8).

---

## 1. Segment Mapping

### Function Entries (push-prologue)

| Address    | Name                                                   | Push line |
|------------|--------------------------------------------------------|-----------|
| 0x08072870 | check_equip_target_slot_in_chain_context_bitmap        | L7845     |
| 0x08072890 | dispatch_equip_slot_sprite_by_activation_state         | L7877     |
| 0x080728d4 | dispatch_equip_slot_sprite_unconditional               | L7926     |
| 0x080728f0 | forward_equip_bitmap_zone11_with_player_shift          | L7951     |
| 0x0807290c | dispatch_lp_delta_display_by_card_pair_diff            | L7984     |
| 0x080729dc | tick_equip_spell_zone_lp_display_state                 | L8105     |
| 0x08072a74 | dispatch_equip_slot_lp_sprite_by_field_type            | L8201     |
| 0x08072aac | tick_equip_zone_type14_oam_placement_state             | L8239     |
| 0x08072b7c | apply_equip_activation_by_zone_slot_head_check         | L8362     |
| 0x08072bfc | dispatch_equip_sprite_by_zone_side_match               | L8449     |
| 0x08072ce4 | tick_dragon_summon_display_if_monster_zones_occupied   | L8566     |

Total: 11 named functions.
Segment ends at 0x08072d20 (start of next function `enqueue_zone_sprite_attr_type11_from_slot`).

### ROM_INCBIN Blocks (Seg-4b: 4 blocks)

| Block | Address    | Size  | ROM file offset | Preceding dispatch table  |
|-------|------------|-------|-----------------|---------------------------|
| B5    | 0x08072404 | 0x2c  | 0x72404         | none (fn_eligible only)    |
| B6    | 0x08072444 | 0x138 | 0x72444         | 0x72430..0x72444 (5 words) |
| B7    | 0x08072594 | 0x1a0 | 0x72594         | 0x7257c..0x72594 (6 words) |
| B8    | 0x0807274c | 0x124 | 0x7274c         | 0x72734..0x7274c (6 words) |

### Residual Auto-Name Slots (exhaustive, 26 total)

| Slot                           | Addr       | Value       |
|-------------------------------|------------|-------------|
| DAT_08072444                   | 0x08072444 | (B6 ROM_INCBIN entry label) |
| DAT_08072594                   | 0x08072594 | (B7 ROM_INCBIN entry label) |
| DAT_0807274c                   | 0x0807274c | (B8 ROM_INCBIN entry label) |
| DWORD_0807288c                 | 0x0807288c | 0x0201bb90  |
| DWORD_080728bc                 | 0x080728bc | 0x0201b290  |
| DWORD_08072938                 | 0x08072938 | 0x0201c4e0  |
| DWORD_0807293c                 | 0x0807293c | 0x00001ce8  |
| DWORD_08072940                 | 0x08072940 | 0x0201b290  |
| DWORD_08072944                 | 0x08072944 | 0x000004a4  |
| DWORD_08072990                 | 0x08072990 | 0x00001da8  |
| DWORD_080729d8                 | 0x080729d8 | 0x00001770  |
| DWORD_080729f8                 | 0x080729f8 | 0x0201b290  |
| DWORD_08072a40                 | 0x08072a40 | 0x0201c4e0  |
| DWORD_08072a44                 | 0x08072a44 | 0x00001da8  |
| DWORD_08072a48                 | 0x08072a48 | 0x00001daa  |
| DWORD_08072b10                 | 0x08072b10 | 0x0201b290  |
| DWORD_08072b14                 | 0x08072b14 | 0x00000868  |
| DWORD_08072b18                 | 0x08072b18 | 0x0201c8f8  |
| DWORD_08072b6c                 | 0x08072b6c | 0x00000868  |
| DWORD_08072b70                 | 0x08072b70 | 0x0201c8f8  |
| DWORD_08072bdc                 | 0x08072bdc | 0x00000868  |
| DWORD_08072be0                 | 0x08072be0 | 0x0201c510  |
| DWORD_08072cac                 | 0x08072cac | 0x00000868  |
| DWORD_08072cb0                 | 0x08072cb0 | 0x0201c510  |
| DWORD_08072cb4                 | 0x08072cb4 | 0x00001cb8  |
| DWORD_08072d0c                 | 0x08072d0c | 0x0201b290  |

Note: DWORD_08072938 and DWORD_08072a40 already have `.word gP1LifePoints` in the .word line
(Ghidra resolved the symbolic name) but the slot label itself remains auto-named.

---

## 2. Data Block Classification (Rule 2/3) -- ref-scan evidence

### ref-scan raw data (python, exhaustive 2B-step across entire block)

**Block B5 (0x08072404/0x2c = 0x72404..0x72430):**

```python
# python ref-scan results:
# addr=0x08072404 raw=0 thumb+1=1  (FS table at GBA:0x09e41078)
# addr=0x08072408 raw=1 thumb+1=0  (ref at ROM_off=0x806df; 0x806df&3=3 -> unaligned -> coincidental)
```

- 0x08072404 THUMB+1=1: FS dispatch table at GBA:0x09e41078 (0x09e4xxxx confirmed).
  CID at FS[0x09e41074] = 0x0000151d = Fiend Comedian (card-stats.s L14210, pw=81172176).
  FS word: [0x09e41078] = 0x08072405 (= 0x08072404 | 1, THUMB+1 confirmed).
- 0x08072408 raw=1: ref at ROM_off=0x806df, GBA=0x080806df. Alignment: 0x806df&3=3 (not 4-byte aligned). Coincidental compressed data. Discarded.
- All other 2B-aligned positions: raw=0 THUMB+1=0.

B5 bytes 0x72404..0x72406: 0xb570 (push{r4,r5,r6,lr}) -> function starts at byte 0 (no pad).
Literal pool at 0x72428..0x7242f: [0x72428]=0x0201b290 (gDuelPhaseFlags), [0x7242c]=0x08072430 (next addr).

**Block B6 (0x08072444/0x138 = 0x72444..0x7257c):**

```python
# True (aligned) refs from pre-block dispatch table 0x72430..0x72444 (5 entries):
# addr=0x08072444 raw=1 (table[0x72440]=0x08072444)
# addr=0x0807248a raw=1 (table[0x7243c]=0x0807248a)
# addr=0x080724ac raw=1 (table[0x72438]=0x080724ac)
# addr=0x080724b4 raw=1 (table[0x72434]=0x080724b4)
# addr=0x08072534 raw=1 (table[0x72430]=0x08072534)
# addr=0x08072540 raw=0 thumb+1=1  (FS table at GBA:0x09e41090)
#
# Coincidental:
# addr=0x08072510 raw=1: ref at ROM_off=0x9ab0b1, 0x9ab0b1&3=1 -> unaligned -> discarded
```

- 0x08072540 THUMB+1=1: FS dispatch table at GBA:0x09e41090 (0x09e4xxxx confirmed).
  CID at FS[0x09e4108c] = 0x0000151e = Last Turn (card-stats.s L14212, pw=28566710; note: from F09-Seg-4.proposal.md context, card_1093).
  FS word: [0x09e41090] = 0x08072541 (= 0x08072540 | 1, THUMB+1 confirmed).
  fn_eligible for Last Turn at offset +0xfc from B6 start (0x72540 - 0x72444 = 0xfc).
- 5 raw dispatch table refs: true entry points (all aligned, refs from asm .word table at 0x72430).
- 0x08072510 raw=1: unaligned (align=1). Coincidental. Discarded.

**Block B7 (0x08072594/0x1a0 = 0x72594..0x72734):**

```python
# True (aligned) refs from pre-block dispatch table 0x7257c..0x72594 (6 entries):
# addr=0x08072594 raw=1 (table[0x72590]=0x08072594)
# addr=0x080725e8 raw=1 (table[0x7258c]=0x080725e8)
# addr=0x08072624 raw=1 (table[0x72588]=0x08072624)
# addr=0x0807264c raw=1 (table[0x72584]=0x0807264c)
# addr=0x08072678 raw=1 (table[0x72580]=0x08072678)
# addr=0x080726bc raw=1 (table[0x7257c]=0x080726bc)
# addr=0x080726f4 raw=0 thumb+1=3  (FS table: 3 refs)
#
# Coincidental:
# addr=0x08072606 thumb+1=1: ref at ROM_off=0x1837c01; align=1 -> unaligned ->
#   GBA:0x09837c01 is in FS compressed area (0x09800000-range), NOT 0x09e4xxxx dispatch table.
#   CID at-4=0x6c033701 (garbage, not valid CID) -> coincidental. Discarded.
# addr=0x08072628 raw=9: all 9 refs at 0x081c5xxx (align=2 or 1) -> compressed data. Discarded.
# addr=0x08072700 raw=1: ref at ROM_off=0x1e7fc23; align=3 -> unaligned -> discarded.
```

- 0x080726f4 THUMB+1=3: 3 FS dispatch table refs in 0x09e4xxxx area:
  - GBA:0x09e43e08: CID[0x09e43e04]=0x00001522 = Vampire Lord (card_info.inc:L556 VAMPIRE_LORD_CID).
  - GBA:0x09e44930: CID[0x09e4492c]=0x00001746 = Vampire Lady (card-stats.s L14521, pw=26495087).
  - GBA:0x09e45b60: CID[0x09e45b5c]=0x00001522 = Vampire Lord (second FS entry, same fn).
  All 3 FS words: 0x080726f5 (= 0x080726f4 | 1, THUMB+1 confirmed).
  fn_eligible for Vampire Lord / Vampire Lady at offset +0x160 from B7 start.
- 6 raw dispatch table refs: true entry points (all aligned, from 0x7257c table).

**Block B8 (0x0807274c/0x124 = 0x7274c..0x72870):**

```python
# True (aligned) refs from pre-block dispatch table 0x72734..0x7274c (6 entries):
# addr=0x0807274c raw=1 (table[0x72748]=0x0807274c)
# addr=0x080727b8 raw=1 (table[0x72744]=0x080727b8)
# addr=0x080727e4 raw=1 (table[0x72740]=0x080727e4)
# addr=0x08072804 raw=1 (table[0x7273c]=0x08072804)
# addr=0x08072848 raw=1 (table[0x72738]=0x08072848)
# addr=0x08072856 raw=1 (table[0x72734]=0x08072856)
```

- 6 raw dispatch table refs: all true, aligned, from asm .word table at 0x72734 (already in asm as .word lines).
- No THUMB+1 refs.

### Classification Table

| Block | ref-scan summary | Judgment | Reason |
|-------|-----------------|----------|--------|
| B5 0x72404/0x2c | raw=0 THUMB+1=1 at 0x08072404; FS:0x09e41078; raw=1 at 0x08072408 (unaligned, discarded) | R4 DISASM | FS card effect handler table THUMB+1 ref; fn_eligible for Fiend Comedian CID=0x151d; CID confirmed at FS:0x09e41074=0x0000151d |
| B6 0x72444/0x138 | raw=5 (all from pre-block dispatch table); THUMB+1=1 at 0x08072540 (FS:0x09e41090); 1 unaligned discarded | R4 DISASM | 5 raw sub-stubs via dispatch table + fn_eligible for Last Turn CID=0x151e (FS THUMB+1) |
| B7 0x72594/0x1a0 | raw=6 (all from pre-block dispatch table); THUMB+1=3 at 0x080726f4 (FS:x3); 3 coincidental discarded | R4 DISASM | 6 raw sub-stubs via dispatch table + fn_eligible for Vampire Lord (CID=0x1522 x2) + Vampire Lady (CID=0x1746 x1) |
| B8 0x7274c/0x124 | raw=6 (all from pre-block dispatch table); THUMB+1=0 | R4 DISASM | 6 raw sub-stubs via dispatch table; no fn_eligible THUMB+1 refs |

---

## 3. Symbolization Plan

### EQ_SLOTS (data-equate; REUSE first)

| Slot                  | Value       | Const name                  | Source                      |
|-----------------------|-------------|-----------------------------|-----------------------------|
| DWORD_0807288c        | 0x0201bb90  | gEquipChainSlotRefs         | REUSE ewram.inc:316         |
| DWORD_080728bc        | 0x0201b290  | gDuelPhaseFlags             | REUSE ewram.inc:352         |
| DWORD_08072938        | 0x0201c4e0  | gP1LifePoints               | REUSE ewram.inc:79          |
| DWORD_0807293c        | 0x00001ce8  | P1LP_BLOCK2_OFF_1CE8        | REUSE ewram.inc:275         |
| DWORD_08072940        | 0x0201b290  | gDuelPhaseFlags             | REUSE ewram.inc:352         |
| DWORD_08072944        | 0x000004a4  | EQUIP_PHASE_FRAME_OFF       | REUSE ewram.inc:435         |
| DWORD_08072990        | 0x00001da8  | LP_CARD_TRACK_BASE_OFF      | REUSE ewram.inc:247         |
| DWORD_080729d8        | 0x00001770  | LP_DELTA_6000               | NEW (see Section 6; conf:high) |
| DWORD_080729f8        | 0x0201b290  | gDuelPhaseFlags             | REUSE ewram.inc:352         |
| DWORD_08072a40        | 0x0201c4e0  | gP1LifePoints               | REUSE ewram.inc:79          |
| DWORD_08072a44        | 0x00001da8  | LP_CARD_TRACK_BASE_OFF      | REUSE ewram.inc:247         |
| DWORD_08072a48        | 0x00001daa  | LP_CARD_TRACK_NEXT_OFF      | REUSE ewram.inc:248         |
| DWORD_08072b10        | 0x0201b290  | gDuelPhaseFlags             | REUSE ewram.inc:352         |
| DWORD_08072b14        | 0x00000868  | PLAYER_BLOCK_STRIDE         | REUSE ewram.inc:250         |
| DWORD_08072b18        | 0x0201c8f8  | gP1HandSlotArray            | REUSE ewram.inc:333         |
| DWORD_08072b6c        | 0x00000868  | PLAYER_BLOCK_STRIDE         | REUSE ewram.inc:250         |
| DWORD_08072b70        | 0x0201c8f8  | gP1HandSlotArray            | REUSE ewram.inc:333         |
| DWORD_08072bdc        | 0x00000868  | PLAYER_BLOCK_STRIDE         | REUSE ewram.inc:250         |
| DWORD_08072be0        | 0x0201c510  | gDuelFieldSlots             | REUSE ewram.inc:313         |
| DWORD_08072cac        | 0x00000868  | PLAYER_BLOCK_STRIDE         | REUSE ewram.inc:250         |
| DWORD_08072cb0        | 0x0201c510  | gDuelFieldSlots             | REUSE ewram.inc:313         |
| DWORD_08072cb4        | 0x00001cb8  | DUEL_ACTIVE_PLAYER_OFF      | REUSE duel_field.inc:155    |
| DWORD_08072d0c        | 0x0201b290  | gDuelPhaseFlags             | REUSE ewram.inc:352         |

EQ summary: 22 REUSE + 1 NEW (LP_DELTA_6000) = 23 equate slots.

Block entry-point labels (DAT_08072444, DAT_08072594, DAT_0807274c): see RENAME_SLOTS.

### REF_SLOTS (USER-label + DATA-ref)

None in Seg-4b. All slots are literal-pool constants (no RAM global pointer slots requiring USER-label).

### RENAME_SLOTS (auto-name -> semantic label + EOL)

| Slot            | New label                                 | EOL                                                  |
|-----------------|-------------------------------------------|------------------------------------------------------|
| DAT_08072444    | last_turn_dispatch_sub_stubs_2444         | raw-dispatch sub-stubs: 5 entry-pts + fn_eligible B6 |
| DAT_08072594    | vampire_dispatch_sub_stubs_2594           | raw-dispatch sub-stubs: 6 entry-pts + fn_eligible B7 |
| DAT_0807274c    | equip_zone_sub_stubs_274c                 | raw-dispatch sub-stubs: 6 entry-pts B8               |

### FUNC_RENAME (misname correction)

None identified. All 11 function names match their function bodies.

### PLATE (R5 -- CJK mojibake fix)

**PLATE-1**: `tick_dragon_summon_display_if_monster_zones_occupied` @ 0x08072ce4 (asm L8565).

Current plate contains CJK text (mojibake in Ghidra after Jython double-UTF8 encoding).
asm/09 L8565: starts with "@ [CJK characters: equip chain dragon summon display gate driver...]"
The asm file shows the text stored as raw CJK bytes (UTF-8) which will render as mojibake in Ghidra.

Replace full plate with ASCII-only text:
```
@ Equip chain dragon-summon display gate driver.
@ Takes card_entry_ptr(r0), scene_ptr(r1).
@ Reads [gDuelPhaseFlags+0x4a0] step code.
@ If step==0x80: extracts player_id from [r0+2] bit0;
@   calls count_occupied_monster_zones(player_id).
@   If result==0 (no occupied monster zones) returns 0 immediately.
@ If step!=0x80 or monster zones are occupied:
@   calls tick_dragon_summon_effect_display_state_machine(r4,r5).
@ Returns result of tick_dragon_summon_effect_display_state_machine.
@ indeg=0; driven by fn-ptr dispatch table.
```

C8 check: grep FUN_[0-9a-f]{8} in L7809..L8596 (Seg-4b asm lines) = 0 hits.

---

## 4. disasm Plan (R4)

### B5: fn_eligible_fiend_comedian @ 0x08072404

- FS table ref at GBA:0x09e41078 stores THUMB+1=0x08072405 (confirmed).
- CID from FS:0x09e41074 = 0x0000151d = Fiend Comedian (card-stats.s L14210 pw=81172176).
- Block starts at 0x72404 with 0xb570 (push{r4,r5,r6,lr}) -- fn starts at byte 0 (no pad).
- Block ends at 0x72430 (= 0x72404 + 0x2c). Literal pool at 0x72428..0x7242f.
- Function entry: 0x08072404 (THUMB). fn_eligible size: 0x2c - 0 = 0x2c bytes.
- Literal pool in block:
  - [0x72428] = 0x0201b290 (gDuelPhaseFlags)
  - [0x7242c] = 0x08072430 (next function/table start, used as self-referential skip target)
- DisassembleCommand range: [0x08072404, 0x08072428)
- Label: `fn_eligible_fiend_comedian_2404`
- Procedure: clearListing(0x08072404, 0x08072430) -> setTMode(0x08072404) -> DisassembleCommand(0x08072404) -> createDWord for literal pool at 0x72428 and 0x7242c.
- Note: Raw ref at 0x08072408 is unaligned (align=3), not a second entry point. Block has exactly 1 function.

### B6: fn_eligible_last_turn + sub-stubs @ 0x08072444

- Pre-block dispatch table at 0x72430..0x72444 (5 .word entries already in asm):
  ```
  0x72430: 0x08072534  (B6 +0xf0 -> sub_2534)
  0x72434: 0x080724b4  (B6 +0x70 -> sub_24b4)
  0x72438: 0x080724ac  (B6 +0x68 -> sub_24ac)
  0x7243c: 0x0807248a  (B6 +0x46 -> sub_248a)
  0x72440: 0x08072444  (B6 +0x00 -> sub_2444)
  ```
- fn_eligible at 0x08072540 (B6 +0xfc): FS:0x09e41090 THUMB+1=0x08072541, CID=0x151e.
- 5 unique sub-stub entry points in B6: 0x08072444, 0x0807248a, 0x080724ac, 0x080724b4, 0x08072534.
- fn_eligible entry at 0x08072540.
- Total 6 entry points in B6.
- Block: 0x08072444..0x0807257c (0x138 bytes).
- Labels:
  - `last_turn_sub_2444`, `last_turn_sub_248a`, `last_turn_sub_24ac`
  - `last_turn_sub_24b4`, `last_turn_sub_2534`
  - `fn_eligible_last_turn_2540`
- Procedure: clearListing(0x08072444, 0x0807257c) -> setTMode(0x08072444) ->
  DisassembleCommand per entry in address order (6 calls):
  0x08072444, 0x0807248a, 0x080724ac, 0x080724b4, 0x08072534, 0x08072540.
- Literal pool words inside block must be createDWord-forced after disasm
  (check python: expect gDuelPhaseFlags/gDuelFieldSlots/gP1HandSlotArray patterns).
- fn_eligible size: 0x7257c - 0x72540 = 0x3c bytes.
  Literal pool of fn_eligible: [0x72574]=0x0201b290, [0x72578]=0x0807257c.

### B7: fn_eligible_vampire_lord_lady + sub-stubs @ 0x08072594

- Pre-block dispatch table at 0x7257c..0x72594 (6 .word entries already in asm):
  ```
  0x7257c: 0x080726bc  (B7 +0x128 -> sub_26bc)
  0x72580: 0x08072678  (B7 +0xe4 -> sub_2678)
  0x72584: 0x0807264c  (B7 +0xb8 -> sub_264c)
  0x72588: 0x08072624  (B7 +0x90 -> sub_2624)
  0x7258c: 0x080725e8  (B7 +0x54 -> sub_25e8)
  0x72590: 0x08072594  (B7 +0x00 -> sub_2594)
  ```
- fn_eligible at 0x080726f4 (B7 +0x160): FS THUMB+1 x3 (CID=0x1522 x2 + CID=0x1746 x1).
- 6 unique sub-stub entry points + fn_eligible = 7 entry points total.
- Block: 0x08072594..0x08072734 (0x1a0 bytes).
- Labels:
  - `vampire_sub_2594`, `vampire_sub_25e8`, `vampire_sub_2624`
  - `vampire_sub_264c`, `vampire_sub_2678`, `vampire_sub_26bc`
  - `fn_eligible_vampire_lord_lady_26f4`
- Procedure: clearListing(0x08072594, 0x08072734) -> setTMode(0x08072594) ->
  DisassembleCommand per entry in address order (7 calls):
  0x08072594, 0x080725e8, 0x08072624, 0x0807264c, 0x08072678, 0x080726bc, 0x080726f4.
- fn_eligible handles both VAMPIRE_LORD_CID (0x1522) and VAMPIRE_LADY_CID (0x1746).
  These are already/to-be defined in card_info.inc (VAMPIRE_LORD_CID already exists: card_info.inc:L556).
- fn_eligible LP: [0x7272c]=0x0201b290, [0x72730]=0x08072734.

### B8: equip-zone sub-stubs @ 0x0807274c

- Pre-block dispatch table at 0x72734..0x7274c (6 .word entries already in asm):
  ```
  0x72734: 0x08072856  (B8 +0x10a -> sub_2856)
  0x72738: 0x08072848  (B8 +0xfc -> sub_2848)
  0x7273c: 0x08072804  (B8 +0xb8 -> sub_2804)
  0x72740: 0x080727e4  (B8 +0x98 -> sub_27e4)
  0x72744: 0x080727b8  (B8 +0x6c -> sub_27b8)
  0x72748: 0x0807274c  (B8 +0x00 -> sub_274c)
  ```
- No fn_eligible THUMB+1 refs.
- 6 unique sub-stub entry points.
- Block: 0x0807274c..0x08072870 (0x124 bytes).
- Labels:
  - `equip_zone_sub_274c`, `equip_zone_sub_27b8`, `equip_zone_sub_27e4`
  - `equip_zone_sub_2804`, `equip_zone_sub_2848`, `equip_zone_sub_2856`
- Procedure: clearListing(0x0807274c, 0x08072870) -> setTMode(0x0807274c) ->
  DisassembleCommand per entry in address order (6 calls):
  0x0807274c, 0x080727b8, 0x080727e4, 0x08072804, 0x08072848, 0x08072856.
- Literal pool words inside block must be createDWord-forced after disasm.

---

## 5. carve Plan (R7)

None in Seg-4b. All 4 blocks are DISASM (code reached via pointers), not data tables for carve.
The pre-block dispatch tables (.word fn_addr entries) are already in asm as `.word` lines.

---

## 6. New Constants Required

### card_info.inc additions

| Name                  | Value       | Card                | Evidence |
|-----------------------|-------------|---------------------|----------|
| FIEND_COMEDIAN_CID    | 0x0000151d  | Fiend Comedian      | card-stats.s L14210 pw=81172176; FS table fn_eligible B5; conf:high |
| LAST_TURN_CID         | 0x0000151e  | Last Turn           | card-stats.s L14212 pw=28566710; FS table fn_eligible B6; conf:high |

C5 dedup check (by VALUE):
- 0x0000151d: grep constants/ -> 0 hits. NEW confirmed.
- 0x0000151e: grep constants/ -> 0 hits. NEW confirmed.
- 0x00001746: grep constants/ -> card_info.inc:602 VAMPIRE_LADY_CID=0x00001746. REUSE confirmed.

Note: VAMPIRE_LORD_CID=0x00001522 already exists in card_info.inc:L556 (REUSE).
Note: VAMPIRE_LADY_CID=0x00001746 already exists in card_info.inc:602 (REUSE). fixer lands B7 disasm using the existing name directly; no new .equ needed.

### duel_field.inc (or ewram.inc) additions

| Name           | Value       | Domain                     | Evidence |
|----------------|-------------|----------------------------|----------|
| LP_DELTA_6000  | 0x00001770  | LP delta value (not CID)   | dispatch_lp_delta_display_by_card_pair_diff asm/09 L8085: loaded as r2 (LP delta arg) when card count v==6; submit_lp_indicator_with_slot_xor_flag called with r2=0x1770=6000; conf:high |

C5 dedup check (by VALUE):
- 0x00001770: grep constants/ -> card_info.inc:L192 `.equ MARSHMALLON_CID, 0x00001770`. This is a different domain (card ID vs LP delta). Per C5 conventions for same-value different-base/domain: benign collision, create independent constant.
- Placement: `duel_field.inc` (LP domain) or a new `lp_display.inc`. Recommend `duel_field.inc` since other LP-delta offsets live there.

---

## 7. Section 5.1 Registration (Rule 3 -- 0-reference blocks)

None in Seg-4b. All 4 blocks have confirmed references:
- B5: FS table THUMB+1 ref at 0x09e41078 (count=1, 0x09e4xxxx area confirmed).
- B6: raw dispatch table refs (5 entries at 0x72430..0x72444) + FS THUMB+1 at 0x09e41090 (count=1).
- B7: raw dispatch table refs (6 entries at 0x7257c..0x72594) + FS THUMB+1 x3 at 0x09e4xxxx.
- B8: raw dispatch table refs (6 entries at 0x72734..0x7274c).

---

## 8. Consumer Evidence (R6) -- key slot semantics

| Slot                  | Consumer file:line                          | Semantic                        | Confidence |
|-----------------------|---------------------------------------------|---------------------------------|------------|
| DWORD_0807288c=0x0201bb90 | asm/09 L7848: `ldr r2, DWORD_0807288c` in check_equip_target_slot_in_chain_context_bitmap; reads [r2+0x14] chain status | gEquipChainSlotRefs (equip chain slot reference array) | high |
| DWORD_080728bc=0x0201b290 | asm/09 L7881: `ldr r0, DWORD_080728bc`; `movs r1,#0x94; lsls r1,r1,#3` -> r1=0x4a0; reads step code at [base+0x4a0] | gDuelPhaseFlags (scene step base) | high (already in ewram.inc:352) |
| DWORD_08072938=0x0201c4e0 | asm/09 L7988: `ldr r7, DWORD_08072938`; used as base for LP display field reads | gP1LifePoints | high (already in ewram.inc:79) |
| DWORD_0807293c=0x00001ce8 | asm/09 L7990: `ldr r0, DWORD_0807293c`; `adds r1,r7,r0` -> [gP1LifePoints+0x1ce8]; comment LP_FIELD1_OFFSET=0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | high (ewram.inc:275) |
| DWORD_08072990=0x00001da8 | asm/09 L8056: `ldr r3, DWORD_08072990`; `adds r0,r7,r3`; `ldrh r0,[r0,#0]` reads LP card slot | LP_CARD_TRACK_BASE_OFF | high (ewram.inc:247) |
| DWORD_080729d8=0x00001770 | asm/09 L8085: `ldr r2, DWORD_080729d8` in dispatch_lp_delta_display_by_card_pair_diff LAB_080729c4 (v==6 branch); r2=6000 passed to submit_lp_indicator_with_slot_xor_flag as LP delta | LP_DELTA_6000=6000 (fixed LP delta when v=6) | high |
| DWORD_08072a48=0x00001daa | asm/09 L8160: `ldr r2, DWORD_08072a48`; adds with gP1LifePoints -> [gP1LifePoints+0x1daa]; ldrh reads hword; render_spell_zone_sprite call | LP_CARD_TRACK_NEXT_OFF (5-entry hword clear base, ewram.inc:248) | high |
| DWORD_08072cb4=0x00001cb8 | asm/09 L8540: `ldr r0, DWORD_08072cb4`; `add r0,r12` where r12=gP1LifePoints context; read as active turn player idx | DUEL_ACTIVE_PLAYER_OFF (duel_field.inc:155) | high |

---

## 9. C13 Residual 100% Coverage Proof

Total auto-name slots in Seg-4b: 26.
- 3 DAT_ = block entry-point labels (B6, B7, B8 start labels): RENAME_SLOTS (3 entries).
- 23 DWORD_ = literal-pool constant slots: EQ_SLOTS (22 REUSE + 1 NEW = 23 entries).
- Total: 3 + 23 = 26. Matches count above. No double-count, no omission.

ROM_INCBIN blocks: 4. All classified as R4 DISASM (all have refs: B5 THUMB+1, B6 5+THUMB+1, B7 6+THUMB+1x3, B8 6 raw). Sec5.1 = 0.

Note: B5 block (0x72404) does NOT have a DAT_ auto-name label in the asm (no `DAT_08072404:` prefix line before the ROM_INCBIN statement). The block immediately follows `bx r1` at 0x72402 in function `dispatch_banisher_equip_zone_sprite_by_target_slot`. So B5 has no block label to rename -- the fn_eligible entry point label `fn_eligible_fiend_comedian_2404` is created by the disasm step itself.

---

## 10. Requests / Blocked Items

None. All slots have high-confidence semantics from direct consumer evidence or established constants.

The CJK plate fix (PLATE-1) requires a full plate-comment replacement in Ghidra for `tick_dragon_summon_display_if_monster_zones_occupied` (0x08072ce4). The replacement text is pure ASCII (verified: no bytes >0x7F in the proposed text above).

---

## Executor Report: F09-Seg-4b

- Slots: EQ=23 (22 REUSE + 1 NEW) RENAME=3 FUNC_RENAME=0 PLATE=1
- disasm=4 blocks (B5:1fn, B6:5sub-stubs+1fn_eligible, B7:6sub-stubs+1fn_eligible, B8:6sub-stubs)
- carve=0
- sec5.1=0
- New constants: card_info.inc +2 (FIEND_COMEDIAN_CID=0x151d, LAST_TURN_CID=0x151e); duel_field.inc +1 (LP_DELTA_6000=0x1770)
- REUSE: VAMPIRE_LADY_CID=0x1746 (card_info.inc:602), VAMPIRE_LORD_CID=0x1522 (card_info.inc:L556)
- Seek help: none
- proposal: doc/dev/refine/F09-Seg-4b.proposal.md
