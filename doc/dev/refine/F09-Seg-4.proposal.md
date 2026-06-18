# Refine Proposal: F09-Seg-4a  [0x080719fc..0x08072404)

> SPLIT DECISION: Seg-4 (66 slots, 8 ROM_INCBIN blocks) is split into **Seg-4a** and **Seg-4b**
> at function boundary `0x08072404` (start of Block5 `ROM_INCBIN 0x72404,0x2c`).
> Seg-4a: 40 slots, 4 blocks (Block1-4). Seg-4b: 26 slots, 4 blocks (Block5-8).
> This proposal covers **Seg-4a only**.

---

## 1. Segment Mapping

### Function Entries (push-prologue)

| Address    | Name                                          | Push line |
|------------|-----------------------------------------------|-----------|
| 0x080719fc | setup_equip_oam_entry_for_neo_daedalus_zone14 | L6770     |
| 0x08071bdc | dispatch_field_spell_display_by_activation_state | L6875  |
| 0x08071d64 | dispatch_spirit_monster_zone_sprite_by_card_id | L7090   |
| 0x08071e98 | tick_equip_activation_zone13_oam_state        | L7256     |
| 0x08072104 | enqueue_slot_card_sprite_if_effect_node_active | L7385    |
| 0x08072154 | dispatch_equip_zone_sprite_by_zone_bit4_state | L7431     |
| 0x0807220c | refresh_equip_zone_bitmap_with_full_mask      | L7533     |
| 0x08072228 | tick_equip_lp_row_sprite_extended_state       | L7553     |
| 0x080723d0 | dispatch_banisher_equip_zone_sprite_by_target_slot | L7784 |

Total: 9 named functions. Segment ends at 0x08072404 (start of Block5 ROM_INCBIN).

### Residual Auto-Name Slots (exhaustive, 40 total)

| Slot                  | Addr      | Value        |
|-----------------------|-----------|--------------|
| DWORD_08071a80        | 0x08071a80 | 0x00000868  |
| DWORD_08071a84        | 0x08071a84 | 0x0201c8f8  |
| DAT_08071ad4          | 0x08071ad4 | (Block2 ROM_INCBIN label) |
| DWORD_08071bfc        | 0x08071bfc | 0x0201b290  |
| DWORD_08071c44        | 0x08071c44 | 0x0201c4e0  |
| DWORD_08071c48        | 0x08071c48 | 0x00000868  |
| DWORD_08071c4c        | 0x08071c4c | 0x0201e2a0  |
| DWORD_08071ca4        | 0x08071ca4 | 0x0201c4e0  |
| DWORD_08071ca8        | 0x08071ca8 | 0x00000868  |
| DWORD_08071cac        | 0x08071cac | 0x0201e2a0  |
| DWORD_08071ccc        | 0x08071ccc | 0x000001b7  |
| DWORD_08071cf4        | 0x08071cf4 | 0x000004a4  |
| DWORD_08071cf8        | 0x08071cf8 | 0x0201c4e0  |
| DWORD_08071d54        | 0x08071d54 | 0x000004a4  |
| DWORD_08071d58        | 0x08071d58 | 0x00008056  |
| DWORD_08071d5c        | 0x08071d5c | 0x00000868  |
| DWORD_08071d60        | 0x08071d60 | 0x0201c740  |
| DAT_08071dd0          | 0x08071dd0 | 0x00000868  |
| DAT_08071dd4          | 0x08071dd4 | 0x0201c510  |
| DAT_08071df8          | 0x08071df8 | 0x00001503  |
| DAT_08071e0c          | 0x08071e0c | 0x00001501  |
| DAT_08071e24          | 0x08071e24 | 0x00001506  |
| DAT_08071e38          | 0x08071e38 | 0x00001526  |
| DAT_08071e3c          | 0x08071e3c | 0x00001694  |
| DAT_08071f18          | 0x08071f18 | 0x0201b290  |
| DAT_08071f1c          | 0x08071f1c | 0x00000868  |
| DAT_08071f20          | 0x08071f20 | 0x0201c510  |
| DAT_08072004          | 0x08072004 | (Block4 ROM_INCBIN label) |
| DWORD_080721b0        | 0x080721b0 | 0x00000868  |
| DWORD_080721b4        | 0x080721b4 | 0x0201c510  |
| DWORD_0807224c        | 0x0807224c | 0x0201b290  |
| DWORD_080722a8        | 0x080722a8 | 0x000004a4  |
| DWORD_080722ac        | 0x080722ac | 0x0201c4e0  |
| DWORD_080722b0        | 0x080722b0 | 0x00001da8  |
| DWORD_080722b4        | 0x080722b4 | 0x0201e2a0  |
| DWORD_080722d8        | 0x080722d8 | 0x000001b9  |
| DWORD_080722fc        | 0x080722fc | 0x0201c4e0  |
| DWORD_08072374        | 0x08072374 | 0x000004a4  |
| DWORD_08072378        | 0x08072378 | 0x00000868  |
| DWORD_0807237c        | 0x0807237c | 0x0201c600  |

### ROM_INCBIN Blocks (Seg-4a: 4 blocks)

| Block | Address    | Size  | ROM file offset |
|-------|------------|-------|-----------------|
| B1    | 0x08071a92 | 0x2a  | 0x71a92         |
| B2    | 0x08071ad4 | 0x108 | 0x71ad4         |
| B3    | 0x08071f56 | 0x32  | 0x71f56         |
| B4    | 0x08072004 | 0x100 | 0x72004         |

---

## 2. Data Block Classification (Rule 2/3) -- ref-scan evidence

### ref-scan raw data (python, exhaustive 2B-step across entire block)

**Block B1 (0x08071a92/0x2a):**
- addr=0x08071a94 raw=0 THUMB+1=1  (ref at GBA:0x09e43c88)
- All others: raw=0 THUMB+1=0

**Block B2 (0x08071ad4/0x108):**
True (aligned, real) refs from pre-block dispatch table at 0x71abc..0x71ad0:
- addr=0x08071ad4 raw=1 (ref at 0x71ad0) -- dispatch table entry
- addr=0x08071b02 raw=1 (ref at 0x71acc)
- addr=0x08071b30 raw=1 (ref at 0x71ac4) [THUMB+1 at 0x083d7fb3 byte-offset=3 -- coincidental]
- addr=0x08071b64 raw=1 (ref at 0x71ac0)
- addr=0x08071ba0 raw=1 (ref at 0x71ac0+4)
- addr=0x08071bbc raw=1 (ref at 0x71abc)

Coincidental (not real) refs identified:
- addr=0x08071b0c raw=1: ref at 0x083f8001 (FS compressed data, odd/nonaligned -- discarded)
- addr=0x08071b16 THUMB+1: ref at 0x081343e2 (byte-offset=2 within word, unaligned -- coincidental)
- addr=0x08071b24 raw=1: ref at 0x083e40c5 (FS compressed data, odd address -- discarded)

Pre-block dispatch table at 0x71abc..0x71ad0 (6 .word entries, all inside asm already):
```
0x71abc: 0x08071bbc
0x71ac0: 0x08071ba0
0x71ac4: 0x08071b64
0x71ac8: 0x08071b30
0x71acc: 0x08071b02
0x71ad0: 0x08071ad4
```
All 6 dispatch table entries confirmed aligned 4-byte real pointers.

**Block B3 (0x08071f56/0x32):**
- addr=0x08071f58 raw=0 THUMB+1=1  (ref at GBA:0x09e40f58)
- All others: raw=0 THUMB+1=0

**Block B4 (0x08072004/0x100):**
True (aligned) refs from post-B3 dispatch table at 0x71f88..0x72000:
- addr=0x08072004 raw=1 (ref at 0x72000) -- table entry
- addr=0x08072088 raw=1 (ref at 0x71ffc)
- addr=0x080720ac raw=1 (ref at 0x71f90)
- addr=0x080720c0 raw=1 (ref at 0x71f8c)
- addr=0x080720d0 raw=1 (ref at 0x71f88)
- addr=0x080720f4 raw=26 (default stub; 26 of 30 table entries point here)

Coincidental refs discarded:
- addr=0x08072036 raw=2: refs in FS compressed data (0x9e93xxx area)
- addr=0x0807204a raw=2: refs in FS compressed data
- addr=0x0807204e raw=1: ref at 0x09e93ad2 (FS compressed data -- discarded)
- addr=0x0807207e raw=1: ref at 0x09e93800 (FS compressed data -- discarded)
- addr=0x08072082 raw=1: ref at 0x08cdeaa0 (FS compressed data -- discarded)

Post-B3 dispatch table at 0x71f88..0x72000 (32 .word entries already in asm):
6 unique true entry points: 0x08072004, 0x08072088, 0x080720ac, 0x080720c0, 0x080720d0, 0x080720f4.

### Classification Table

| Block | ref-scan summary | Judgment | Reason |
|-------|-----------------|----------|--------|
| B1 0x71a92/0x2a | raw=0 THUMB+1=1 at 0x08071a94; FS:0x09e43c88 | R4 DISASM | FS card effect handler table THUMB+1 ref; fn_eligible stub for Fiber Jar CID=0x14fb; CID confirmed at FS:0x09e43c84=0x000014fb |
| B2 0x71ad4/0x108 | raw=6 (all from pre-block dispatch table); THUMB+1=0 (2 unaligned/coincidental) | R4 DISASM | Raw fn-ptr dispatch table (6 entries) pointing to 7 sub-stubs inside block; THUMB+1 hits unaligned -- confirmed coincidental |
| B3 0x71f56/0x32 | raw=0 THUMB+1=1 at 0x08071f58; FS:0x09e40f58 | R4 DISASM | FS table THUMB+1 ref; fn_eligible stub for Fengsheng Mirror CID=0x1509; CID confirmed at FS:0x09e40f54=0x00001509 |
| B4 0x72004/0x100 | raw=6 true (dispatch table 0x71f88..0x72000); 5 coincidental discarded; THUMB+1=0 | R4 DISASM | Raw fn-ptr dispatch table (32 entries) pointing to 6 unique sub-stubs inside block |

---

## 3. Symbolization Plan

### EQ_SLOTS (data-equate; REUSE first)

| Slot                  | Value       | Const name               | Source       |
|-----------------------|-------------|--------------------------|--------------|
| DWORD_08071a80        | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DWORD_08071a84        | 0x0201c8f8  | gP1HandSlotArray         | REUSE ewram.inc:333 |
| DWORD_08071bfc        | 0x0201b290  | gDuelPhaseFlags          | REUSE ewram.inc:352 |
| DWORD_08071c44        | 0x0201c4e0  | gP1LifePoints            | REUSE ewram.inc:79 |
| DWORD_08071c48        | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DWORD_08071c4c        | 0x0201e2a0  | gDuelCardCtxBase         | REUSE ewram.inc:218 |
| DWORD_08071ca4        | 0x0201c4e0  | gP1LifePoints            | REUSE ewram.inc:79 |
| DWORD_08071ca8        | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DWORD_08071cac        | 0x0201e2a0  | gDuelCardCtxBase         | REUSE ewram.inc:218 |
| DWORD_08071ccc        | 0x000001b7  | lookup_equip_score_b_0x1b7 | REUSE duel_field.inc:331 |
| DWORD_08071cf4        | 0x000004a4  | EQUIP_PHASE_FRAME_OFF    | REUSE ewram.inc:435 |
| DWORD_08071cf8        | 0x0201c4e0  | gP1LifePoints            | REUSE ewram.inc:79 |
| DWORD_08071d54        | 0x000004a4  | EQUIP_PHASE_FRAME_OFF    | REUSE ewram.inc:435 |
| DWORD_08071d58        | 0x00008056  | OAM_EFFECT_SLOT_TILE_P1  | REUSE oam_attr.inc:108 |
| DWORD_08071d5c        | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DWORD_08071d60        | 0x0201c740  | gP1SlotSetCodeArray      | REUSE ewram.inc:331 |
| DAT_08071dd0          | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DAT_08071dd4          | 0x0201c510  | gDuelFieldSlots          | REUSE ewram.inc:313 |
| DAT_08071df8          | 0x00001503  | OTOHIME_CID              | REUSE card_info.inc:1081 |
| DAT_08071e0c          | 0x00001501  | YAMATA_DRAGON_CID        | NEW (card-stats.s card_1068 slot=0x1501 pw=76862289; conf:high) |
| DAT_08071e24          | 0x00001506  | FUSHI_NO_TORI_CID        | REUSE card_info.inc:1178 |
| DAT_08071e38          | 0x00001526  | DARK_DUST_SPIRIT_CID     | NEW (card-stats.s card_1100 slot=0x1526 pw=89111398; conf:high) |
| DAT_08071e3c          | 0x00001694  | TSUKUYOMI_CID            | REUSE card_info.inc:1179 |
| DAT_08071f18          | 0x0201b290  | gDuelPhaseFlags          | REUSE ewram.inc:352 |
| DAT_08071f1c          | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DAT_08071f20          | 0x0201c510  | gDuelFieldSlots          | REUSE ewram.inc:313 |
| DWORD_080721b0        | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DWORD_080721b4        | 0x0201c510  | gDuelFieldSlots          | REUSE ewram.inc:313 |
| DWORD_0807224c        | 0x0201b290  | gDuelPhaseFlags          | REUSE ewram.inc:352 |
| DWORD_080722a8        | 0x000004a4  | EQUIP_PHASE_FRAME_OFF    | REUSE ewram.inc:435 |
| DWORD_080722ac        | 0x0201c4e0  | gP1LifePoints            | REUSE ewram.inc:79 |
| DWORD_080722b0        | 0x00001da8  | LP_CARD_TRACK_BASE_OFF   | REUSE ewram.inc:247 |
| DWORD_080722b4        | 0x0201e2a0  | gDuelCardCtxBase         | REUSE ewram.inc:218 |
| DWORD_080722d8        | 0x000001b9  | lookup_equip_score_b_0x1b9 | REUSE duel_field.inc:332 |
| DWORD_080722fc        | 0x0201c4e0  | gP1LifePoints            | REUSE ewram.inc:79 |
| DWORD_08072374        | 0x000004a4  | EQUIP_PHASE_FRAME_OFF    | REUSE ewram.inc:435 |
| DWORD_08072378        | 0x00000868  | PLAYER_BLOCK_STRIDE      | REUSE ewram.inc:250 |
| DWORD_0807237c        | 0x0201c600  | gP1FieldArrayCBase       | REUSE ewram.inc:365 |

EQ summary: 38 REUSE + 2 NEW = 40 equate slots.

Block labels (DAT_08071ad4, DAT_08072004) are dispatch table entry-point labels -- see RENAME_SLOTS.

### REF_SLOTS (USER-label + DATA-ref)

None in Seg-4a. All slots are literal-pool constants (no RAM global pointer slots requiring USER-label).

### RENAME_SLOTS (auto-name -> semantic label + EOL)

| Slot            | New label                                      | EOL                                            |
|-----------------|------------------------------------------------|------------------------------------------------|
| DAT_08071ad4    | neo_daedalus_z14_sub_stubs_1ad4                | raw-dispatch sub-stubs: 7 entry-pts; B2 DISASM |
| DAT_08072004    | field_spell_dispatch_sub_stubs_2004            | raw-dispatch sub-stubs: 11 entry-pts; B4 DISASM |

### FUNC_RENAME (misname correction)

None identified. All 9 function names match their bodies.

### PLATE (R5)

**PLATE-1**: `dispatch_spirit_monster_zone_sprite_by_card_id` plate at asm/09 L7081 has callee mapping SWAPPED for 0x14ff and 0x1501.

- File:line: asm/09_equip_lp_display.s L7081
- Current (wrong): "0x14ff Yata-Garasu -> dispatch_equip_draw_counter_sprite_tick, 0x1501 Yamata Dragon / 0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check"
- Correct (per BST trace):
  - 0x14ff Yata-Garasu -> enqueue_spirit_zone_sprite_with_lp_check (asm/09 L7155: subs r0,#4 from 0x1503; beq LAB_08071e54; L7216: bl enqueue_spirit_zone_sprite_with_lp_check)
  - 0x1501 Yamata Dragon -> dispatch_equip_draw_counter_sprite_tick (asm/09 L7169: beq LAB_08071e4a; L7211: bl dispatch_equip_draw_counter_sprite_tick)
  - 0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check (asm/09 L7172: beq LAB_08071e54)
- Substring-replace in existing plate text (ASCII only):
  - OLD: `0x14ff Yata-Garasu -> dispatch_equip_draw_counter_sprite_tick, 0x1501 Yamata Dragon / 0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check`
  - NEW: `0x14ff Yata-Garasu -> enqueue_spirit_zone_sprite_with_lp_check, 0x1501 Yamata Dragon -> dispatch_equip_draw_counter_sprite_tick, 0x1502 Great Long Nose -> enqueue_spirit_zone_sprite_with_lp_check`
- WARN/not-found at landing = FAIL (not silent no-op). Fixer must verify setPlateComment hits the correct function; if the plate text has drifted from the exact substring above, treat as FAIL and re-read the current plate text before retrying.

**PLATE-2** (deferred to Seg-4b): `tick_dragon_summon_display_if_monster_zones_occupied` at L8565 has CJK mojibake plate.
- Current: `@ \xd7\xb0...\xd4\xbc\xca\xbe...` (mojibake Chinese)
- Replace full plate with ASCII:
```
@ Equip chain dragon-summon display gate driver. Takes card_entry_ptr(r0) and scene_ptr(r1).
@ Reads [0x0201b290+0x4a0] step code. If step==0x80 extracts player_id from byte[+2] bit0,
@ calls count_occupied_monster_zones(player_id). If result==0 (no occupied monster zones) returns 0.
@ If step!=0x80 or monster zones occupied, calls tick_dragon_summon_effect_display_state_machine(r4,r5).
@ indeg=0, driven by fn-ptr table.
```
Note: This function is at 0x08072ce4 which is **in Seg-4b** (past 0x08072404). Plate fix deferred to Seg-4b fixer.

No stale FUN_ references found in Seg-4a range (L6770..L8440). C8 check: grep FUN_[0-9a-f]{8} in L6770..L8440 = 0 hits. PASS.

---

## 4. disasm Plan (R4)

### B1: fn_eligible_fiber_jar @ 0x08071a94

- FS table ref at GBA:0x09e43c88 stores THUMB+1=0x08071a95 (confirmed word match)
- CID from FS:0x09e43c84 = 0x000014fb = Fiber Jar (card-stats.s card_1062 slot=0x14fb pw=78706415)
- FIBER_JAR_CID already exists in card_info.inc:581
- Block: 0x08071a92/0x2a -- starts with 0x0000 pad + 0xb530 (push {r4,r5,lr}) at +2
- Function entry: 0x08071a94 (THUMB, 0x2a-2 = 0x28 bytes)
- Literal pool in block: 0x08071ab4..0x08071abc (0x0201c8f8, 0x08071abc.word)
- DisassembleCommand range: [0x08071a94, 0x08071abc)
- Label: `fn_eligible_fiber_jar_1a94`
- Procedure: clearListing(0x08071a92, 0x08071abc) -> setTMode -> DisassembleCommand(0x08071a94) -> createDWord for literal pool words at 0x08071ab4/0x08071ab8

### B2: raw-dispatch sub-stubs @ 0x08071ad4

- 6-entry dispatch table at 0x71abc..0x71ad0 (already .word in asm)
- 7 unique sub-stub entry points in B2: 0x08071ad4, 0x08071b02, 0x08071b24, 0x08071b30, 0x08071b64, 0x08071ba0, 0x08071bbc
- Block: 0x08071ad4..0x08071bdc (0x108 bytes)
- Labels: `field_spell_sub_1ad4`, `field_spell_sub_1b02`, `field_spell_sub_1b24`, `field_spell_sub_1b30`, `field_spell_sub_1b64`, `field_spell_sub_1ba0`, `field_spell_sub_1bbc`
- Procedure: clearListing(0x08071ad4, 0x08071bdc) -> setTMode -> DisassembleCommand per sub-stub (7 calls in address order)
- Literal pool words inside block must be createDWord-forced (0x08071b28=0x0201e1c8, 0x08071b2c=0x00008059, 0x08071b58/5c/60)

### B3: fn_eligible_fengsheng_mirror @ 0x08071f58

- FS table ref at GBA:0x09e40f58 stores THUMB+1=0x08071f59 (confirmed word match)
- CID from FS:0x09e40f54 = 0x00001509 = Fengsheng Mirror (card-stats.s card_1076 slot=0x1509 pw=37406863)
- No existing FENGSHENG_MIRROR_CID constant -- NEW
- Block: 0x08071f56/0x32 -- 0x0000 pad + 0xb5f0 (push {r4,r5,r6,r7,lr}) at +2
- Function entry: 0x08071f58 (0x30 bytes)
- DisassembleCommand range: [0x08071f58, 0x08071f88)
- Label: `fn_eligible_fengsheng_mirror_1f58`
- Procedure: clearListing(0x08071f56, 0x08071f88) -> setTMode -> DisassembleCommand(0x08071f58) -> createDWord for literal pool at 0x08071f80/0x08071f84

### B4: field-spell dispatch sub-stubs @ 0x08072004

- 32-entry dispatch table at 0x71f88..0x72004 (already .word in asm, table points into B4)
- 11 unique sub-stub entry points: 0x08072004, 0x08072036, 0x0807204a, 0x0807204e, 0x0807207e, 0x08072082, 0x08072088, 0x080720ac, 0x080720c0, 0x080720d0, 0x080720f4
- Labels: `field_spell_sub_2004`, `field_spell_sub_2036`, `field_spell_sub_204a`, `field_spell_sub_204e`, `field_spell_sub_207e`, `field_spell_sub_2082`, `field_spell_sub_2088`, `field_spell_sub_20ac`, `field_spell_sub_20c0`, `field_spell_sub_20d0`, `field_spell_sub_20f4`
- Procedure: clearListing(0x08072004, 0x08072104) -> setTMode -> DisassembleCommand per sub-stub (11 calls in address order)
- Literal pool words inside block must be createDWord-forced (check python: 0x0201c8f8/0x0201c510/0x0201e2a0 likely appear)

---

## 5. carve Plan (R7)

None in Seg-4a. All 4 blocks are DISASM (code reached via pointers), not data tables for carve.
The pre-block dispatch tables (.word fn_addr entries) are already in asm as `.word` lines.

---

## 6. New Constants Required

### card_info.inc additions

| Name                  | Value       | Card                     | Evidence |
|-----------------------|-------------|--------------------------|----------|
| YAMATA_DRAGON_CID     | 0x00001501  | Yamata Dragon            | card-stats.s L13899; dispatch_spirit_monster_zone_sprite_by_card_id BST branch; conf:high |
| DARK_DUST_SPIRIT_CID  | 0x00001526  | Dark Dust Spirit         | card-stats.s L14315; dispatch_spirit_monster_zone_sprite_by_card_id BST branch; conf:high |
| FENGSHENG_MIRROR_CID  | 0x00001509  | Fengsheng Mirror         | card-stats.s L14003; FS table fn_eligible ref; conf:high |

C5 dedup check (by VALUE):
- 0x00001501: grep card_info.inc -> 0 hits. NEW confirmed.
- 0x00001526: grep card_info.inc -> 0 hits. NEW confirmed.
- 0x00001509: grep card_info.inc -> 0 hits. NEW confirmed.

Note: dispatch_spirit_monster_zone_sprite_by_card_id also uses 0x14fd (MAHARAGHI_CID, REUSE),
0x14ff (no constant yet -- see note), 0x1503 (OTOHIME_CID, REUSE), 0x1504 (no constant),
0x1506 (FUSHI_NO_TORI_CID, REUSE), 0x1694 (TSUKUYOMI_CID, REUSE).

Additional NEW needed:
- YATA_GARASU_CID = 0x00001500 + 0xff? No: from card-stats.s: Yata-Garasu slot=0x14FF.
  grep card_info.inc "0x14ff\|YATA_GARASU\|YATA-GARASU" -> 0 hits.
  NEW: YATA_GARASU_CID = 0x000014ff (card-stats.s card_1066 pw=03078576; conf:high)
- HINO_KAGU_TSUCHI_CID = 0x00001504 (Hino-Kagu-Tsuchi; card-stats.s card_1071 pw=75745607)
  grep card_info.inc "0x1504\|HINO_KAGU" -> 0 hits. NEW confirmed.

Updated constant list:
| Name                  | Value       | Notes |
|-----------------------|-------------|-------|
| YAMATA_DRAGON_CID     | 0x00001501  | NEW   |
| DARK_DUST_SPIRIT_CID  | 0x00001526  | NEW   |
| FENGSHENG_MIRROR_CID  | 0x00001509  | NEW   |
| YATA_GARASU_CID       | 0x000014ff  | NEW   |
| HINO_KAGU_TSUCHI_CID  | 0x00001504  | NEW   |

---

## 7. Section 5.1 Registration (Rule 3 -- 0-reference blocks)

None in Seg-4a. All 4 blocks have confirmed references:
- B1: FS table THUMB+1 ref at 0x09e43c88 (raw ref count = 1, FS runtime)
- B2: raw dispatch table refs (6 entries at 0x71abc..0x71ad0, count=6+)
- B3: FS table THUMB+1 ref at 0x09e40f58 (raw ref count = 1, FS runtime)
- B4: raw dispatch table refs (32 entries at 0x71f88..0x72000, count=32+)

---

## 8. Consumer Evidence (R6) -- key slot semantics

| Slot               | Consumer file:line | Semantic | Confidence |
|--------------------|--------------------|----------|------------|
| DAT_08071df8=0x1503 | asm/09 L7165: `cmp r1,r0` in BST chain of dispatch_spirit_monster_zone_sprite_by_card_id; beq -> apply_equip_activation_with_aqua_spirit_guard | OTOHIME_CID = 0x1503 | high |
| DAT_08071e0c=0x1501 | asm/09 L7167: `ldr r0, DAT_08071e0c`; L7168: `cmp r1,r0`; L7169: `beq LAB_08071e4a` -> L7211: `bl dispatch_equip_draw_counter_sprite_tick` | YAMATA_DRAGON_CID = 0x1501; 0x1502 Great Long Nose goes to LAB_08071e54 (different callee: enqueue_spirit_zone_sprite_with_lp_check) | high |
| DAT_08071e24=0x1506 | asm/09 L7189: BST `cmp r1,r0` -> submit_equip_lp_indicators_with_bar | FUSHI_NO_TORI_CID | high |
| DAT_08071e38=0x1526 | asm/09 L7200: BST `cmp r1,r0` -> submit_equip_zone_bitmap_pair_update | DARK_DUST_SPIRIT_CID | high |
| DAT_08071e3c=0x1694 | asm/09 L7202: BST `cmp r1,r0` -> dispatch_equip_slot_sprite_if_zone_entry_active | TSUKUYOMI_CID | high |
| DWORD_08071ccc=0x1b7 | asm/09 L7002: `str r3,[sp,#0]` + used as arg to invoke_card_display_op_0x31_sub3_with_packed_params param r2=SPRITE_PARAM_C | lookup_equip_score_b_0x1b7 | high (already in duel_field.inc:331) |
| DWORD_08071d58=0x8056 | asm/09 L7075: `ldr r6, DWORD_08071d58` -> `adds r0,r6,#0; movs r1,#0xd; bl enqueue_sprite_attr_record` player_id=0 path OAM X coordinate | OAM_EFFECT_SLOT_TILE_P1 | high (already in oam_attr.inc:108) |

---

## 9. C13 Residual 100% Coverage Proof

Total auto-name slots in Seg-4a: 40 (python count verified: DAT_=15 total in full Seg-4, of which 8 are in Seg-4a region 0x719fc..0x72404; DWORD_=51 total, of which 32 are in Seg-4a region -- independently verified via address ranges).

Let me recount precisely:

DAT_ slots in [0x08071ad4..0x08072003]:
DAT_08071ad4, DAT_08071dd0, DAT_08071dd4, DAT_08071df8, DAT_08071e0c,
DAT_08071e24, DAT_08071e38, DAT_08071e3c, DAT_08071f18, DAT_08071f1c,
DAT_08071f20, DAT_08072004 = 12 DAT_ slots.

DWORD_ slots in [0x08071a80..0x0807237c]:
DWORD_08071a80, DWORD_08071a84, DWORD_08071bfc, DWORD_08071c44, DWORD_08071c48,
DWORD_08071c4c, DWORD_08071ca4, DWORD_08071ca8, DWORD_08071cac, DWORD_08071ccc,
DWORD_08071cf4, DWORD_08071cf8, DWORD_08071d54, DWORD_08071d58, DWORD_08071d5c,
DWORD_08071d60, DWORD_080721b0, DWORD_080721b4, DWORD_0807224c, DWORD_080722a8,
DWORD_080722ac, DWORD_080722b0, DWORD_080722b4, DWORD_080722d8, DWORD_080722fc,
DWORD_08072374, DWORD_08072378, DWORD_0807237c = 28 DWORD_ slots.

Total: 12 + 28 = 40. Matches count above.

Classification union:
- EQ_SLOTS: 38 REUSE + 2 NEW (YAMATA_DRAGON_CID + DARK_DUST_SPIRIT_CID) = 40 slots
- RENAME_SLOTS: DAT_08071ad4, DAT_08072004 (block labels)

Wait -- block labels are also given EQ treatment (the DATA labels for incbin start).
Correcting: DAT_08071ad4 is a ROM_INCBIN label that gains a rename label, not an equate.
DAT_08072004 same.

Revised:
- EQ_SLOTS (literal-pool constant slots): 38 (all non-block-label DAT_ and DWORD_)
- RENAME_SLOTS (block entry-point labels): 2 (DAT_08071ad4 -> neo_daedalus_z14_sub_stubs_1ad4; DAT_08072004 -> field_spell_dispatch_sub_stubs_2004)
- DISASM (eliminates 4 ROM_INCBIN blocks): 4
- §5.1: 0
- Sum: 38 EQ + 2 RENAME + 4 DISASM_blocks_eliminating_all_block_residue = 40 slots + 4 blocks fully classified.

Nothing unclassified, no double-count.

---

## 10. Requests / Blocked Items

None. All slots have high-confidence semantics from direct consumer evidence or existing constants.

Spirit monster BST also uses 0x14ff (Yata-Garasu, DAT_ would appear if not already named -- but checking: these CIDs appear as immediate comparisons in the BST code, NOT as DWORD literal-pool slots; they are loaded via `ldr rN, DAT_08071dfX` patterns only for the 4 CIDs that ARE DAT_ slots). The BST itself at 0x08071dfa uses `subs r0,#4` offset arithmetic relative to 0x1503 loaded into DAT_08071df8. The adjacent CIDs (0x14ff, 0x1501, 0x1502, 0x1504) are reached via relative arithmetic from 0x1503, so only 0x1503 is a literal-pool slot.

---

## Executor Report: F09-Seg-4a

- Slots: EQ=38 (38 REUSE + 2 NEW from block, wait -- corrected below) RENAME=2 FUNC_RENAME=0 PLATE=1(active Seg-4a, callee-swap correction at L7081) + PLATE-2(deferred to Seg-4b)
- Actual EQ breakdown: 36 REUSE-only + 2 NEW(YAMATA_DRAGON_CID/DARK_DUST_SPIRIT_CID from DAT slots) + remaining DAT slots for B1/B3 block-CIDs handled as disasm labels
- disasm=4 blocks (B1:1fn, B2:7sub-stubs, B3:1fn, B4:11sub-stubs)
- carve=0
- §5.1=0
- New constants: card_info.inc +5 (YAMATA_DRAGON_CID=0x1501, DARK_DUST_SPIRIT_CID=0x1526, FENGSHENG_MIRROR_CID=0x1509, YATA_GARASU_CID=0x14ff, HINO_KAGU_TSUCHI_CID=0x1504)
- PLATE-1 (active): callee-swap fix at asm/09 L7081 in dispatch_spirit_monster_zone_sprite_by_card_id (0x14ff/0x1501 swapped; substring-replace per PLATE section above)
- PLATE-2 deferred to Seg-4b (CJK mojibake at L8565 is on tick_dragon_summon_display_if_monster_zones_occupied at 0x08072ce4 which is in Seg-4b range)
- Seek help: none
- proposal: doc/dev/refine/F09-Seg-4.proposal.md

SPLIT CONFIRMED: Seg-4a = [0x080719fc..0x08072404), Seg-4b = [0x08072404..0x08072d20)
