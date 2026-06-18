# Refine Proposal: F08-Seg-8b  [0x0806b56c..0x0806c0cc)

## Seg-8 split reference

Seg-8b is sub-segment 2 of 3 from the Seg-8 split (see F08-Seg-8a.proposal.md header).

| Sub-seg | Range | fn | ROM_INCBIN |
|---------|-------|----|------------|
| Seg-8a | 0x6ab0c..0x6b56c | 6 | 4 (3 disasm + 1 ss5.1) -- DONE |
| Seg-8b | 0x6b56c..0x6c0cc | 4+30(disasm) | 5 (all DISASM) |
| Seg-8c | 0x6c0cc..0x6cbe8 | 9 | 2 (pending) |

---

## Seg Mapping

### Function entries (4 named fn in [0x6b56c, 0x6c0cc))

| Address | Name | Push |
|---------|------|------|
| 0x0806b56c | dispatch_numinous_healer_lp_zone_sprites | push {r4,r5,lr} |
| 0x0806b60c | tick_field_slot_bit_and_lp_display | push {r4,r5,lr} |
| 0x0806b694 | tick_equip_lp_display_seq_with_slot_check | push {r4,lr} |
| 0x0806ba78 | tick_equip_zone_slot_and_lp_indicator_state_machine | push {r4,r5,r6,r7,lr} |

Note: function `dispatch_neo_daedalus_placement_check_by_state` starts at 0x0806c0cc (= Seg-8b exclusive end; first function of Seg-8c). Its plate falls at asm line 17183 between the last ROM_INCBIN and the function label -- includes a stale FUN_ from Seg-8a; addressed in PLATE below.

### Residual auto-name slots (18 DWORD_ / DAT_ / PTR_DAT_)

All fall in [0x6b56c, 0x6c0cc):

| Slot label | Address | Raw value |
|-----------|---------|-----------|
| DWORD_0806b58c | 0x0806b58c | 0x00001352 |
| DWORD_0806b638 | 0x0806b638 | 0x0201b290 |
| DWORD_0806b68c | 0x0806b68c | 0x00000868 |
| DWORD_0806b690 | 0x0806b690 | 0x0201c510 |
| DWORD_0806b6bc | 0x0806b6bc | 0x0201b290 |
| DWORD_0806b6ec | 0x0806b6ec | 0x0201e2a0 |
| DWORD_0806b6f0 | 0x0806b6f0 | 0x0201c4e0 (asm already shows .word gP1LifePoints) |
| DWORD_0806b71c | 0x0806b71c | 0x0201c4e0 (asm already shows .word gP1LifePoints) |
| DWORD_0806b75c | 0x0806b75c | 0x0201c4e0 (asm already shows .word gP1LifePoints) |
| DWORD_0806b760 | 0x0806b760 | 0x00001daa |
| DWORD_0806b764 | 0x0806b764 | 0x00000868 |
| PTR_DAT_0806b7d4 | 0x0806b7d4 | ptr to 10-entry jump table for cid_135b stubs |
| DAT_0806b7fc | 0x0806b7fc | ROM_INCBIN start label |
| DWORD_0806bafc | 0x0806bafc | 0x0201b290 |
| DWORD_0806bb00 | 0x0806bb00 | 0x00000868 |
| DWORD_0806bb04 | 0x0806bb04 | 0x0201e1c8 |
| DWORD_0806bb08 | 0x0806bb08 | 0x0201c510 |
| DWORD_0806bb28 | 0x0806bb28 | 0x08051319 (THUMB+1 fn ptr) |
| DWORD_0806bb2c | 0x0806bb2c | 0x0000135c |
| DWORD_0806bb30 | 0x0806bb30 | 0x00001635 |
| DAT_0806bc2c | 0x0806bc2c | ROM_INCBIN start label |
| DAT_0806bfbc | 0x0806bfbc | ROM_INCBIN start label |

Total residual: 17 DWORD_ + 3 DAT_/PTR_DAT_ = 20 auto-name slots (DWORD_0806b6f0/71c/75c already partially symbolized; still need label rename).

### ROM_INCBIN / .byte blocks (Seg-8b internal, 5 blocks)

| Block | Size | Range |
|-------|------|-------|
| ROM_INCBIN 0x6b784 | 0x4c B | 0x0806b784..0x0806b7d0 |
| ROM_INCBIN 0x6b7fc | 0x27c B | 0x0806b7fc..0x0806ba78 |
| ROM_INCBIN 0x6bb74 | 0x44 B | 0x0806bb74..0x0806bbb8 |
| ROM_INCBIN 0x6bc2c | 0x374 B | 0x0806bc2c..0x0806bfa0 |
| ROM_INCBIN 0x6bfbc | 0x110 B | 0x0806bfbc..0x0806c0cc |

---

## Data Block Classification (Rule 2/3) -- all 5 blocks

### ref-scan summary

```python
import struct
rom = open('roms/2343.gba', 'rb').read()
blocks = [(0x6b784,0x4c),(0x6b7fc,0x27c),(0x6bb74,0x44),(0x6bc2c,0x374),(0x6bfbc,0x110)]
for a,s in blocks:
    raw = rom.count(struct.pack('<I', 0x8000000+a))
    thb = rom.count(struct.pack('<I', 0x8000000+a+1))
    print(hex(a), s, raw, thb)
```

Results:
- 0x6b784  0x4c:  raw=1(unaligned@0x66067f -- compressed data coincidence; offset-3 within word 0x66067c=0x840400c8, NOT a real reference)  THUMB+1=1 @0x1e40448
- 0x6b7fc  0x27c: raw=1 @0x6b7f8  THUMB+1=0
- 0x6bb74  0x44:  raw=0  THUMB+1=1 @0x1e40490
- 0x6bc2c  0x374: raw=1 @0x6bc28  THUMB+1=0
- 0x6bfbc  0x110: raw=1 @0x6bfb8  THUMB+1=0

| Block | sz | ref-scan (real raw / THUMB+1) | Verdict | Evidence |
|-------|----|-------------------------------|---------|---------|
| 0x6b784 | 0x4c | raw=0(real) THUMB+1=1 @0x1e40448 | DISASM R4 | fn_eligible handler for CID=0x135b; entry = 0x0806b785; CID at slot-4: rom[0x1e4044c-4]=rom[0x1e40444]=0x0000135b (python: struct.unpack('<I',rom[0x1e40444:0x1e40448])[0]==0x135b confirmed); first bytes f0b5=push{r4,r5,r6,r7,lr} THUMB; conf: high |
| 0x6b7fc | 0x27c | raw=1 @0x6b7f8 THUMB+1=0 | DISASM R4 | raw ref at 0x6b7f8 = last entry [9] of 10-entry jump table at 0x6b7d4..0x6b7f8 (table pointer at 0x6b7d0 is literal pool inside block 0x6b784); all 10 entries point into this block; first bytes 0x2004 0x793c = movs r0,#4; ldrb r4,[r7,#4] THUMB; conf: high |
| 0x6bb74 | 0x44 | raw=0 THUMB+1=1 @0x1e40490 | DISASM R4 | fn_eligible handler for CID=0x1362 (Magical Hats pw=81210420); entry = 0x0806bb75; CID at slot-4: rom[0x1e4048c]=struct.unpack('<I',rom[0x1e4048c:0x1e40490])[0]==0x1362 confirmed; first bytes f0b5=push{r4,r5,r6,r7,lr} THUMB; conf: high |
| 0x6bc2c | 0x374 | raw=1 @0x6bc28 THUMB+1=0 | DISASM R4 | raw ref at 0x6bc28 = last entry [28] of 29-entry jump table at 0x6bbb8..0x6bc28 (literal pool for table base at 0x6bbb4 inside block 0x6bb74); all 29 entries point into this block; first bytes 0x1c30 0x1c19 = adds r0,r6,#0; adds r1,r3,#0 THUMB; conf: high |
| 0x6bfbc | 0x110 | raw=1 @0x6bfb8 THUMB+1=0 | DISASM R4 | raw ref at 0x6bfb8 = last entry [6] of 7-entry jump table at 0x6bfa0..0x6bfb8 (literal pool for table base at 0x6bf9c, offset 0x370 within block 0x6bc2c, python: struct.unpack('<I',rom[0x6bf9c:0x6bfa0])[0]==0x0806bfa0 confirmed); all 7 entries point into this block; first bytes 0x1c20 0x2100 = adds r0,r4,#0; movs r1,#0 THUMB; conf: high |

Unaligned raw coincidence for 0x6b784: position 0x66067f has byte-offset 3 within word at 0x66067c (value 0x840400c8); value 0x0806b784 spans bytes [0x66067f..0x660682] = inside compressed graphics data; not a real pointer. Confirmed: block 0x6b784 has 0 real raw refs.

Dispatch chain structure:
- 0x6b784 fn_eligible handler (CID=0x135b) -> 10-entry table @0x6b7d4 -> stubs in 0x6b7fc
- 0x6bb74 fn_eligible handler (CID=0x1362 Magical Hats) -> 29-entry table @0x6bbb8 -> stubs in 0x6bc2c
- One stub within 0x6bc2c (offset 0x370 literal pool: 0x0806bfa0) -> 7-entry table @0x6bfa0 -> sub-stubs in 0x6bfbc

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

All ROM byte values verified against python struct.unpack. All labeled C5 reuse confirmed by grep VALUE in constants/*.inc.

| Slot | Address | Value | const_name | Source | slot_label |
|------|---------|-------|------------|--------|-----------|
| DWORD_0806b58c | 0x0806b58c | 0x00001352 | NUMINOUS_HEALER_CID | reuse card_info.inc L1154 | numinous_healer_cid_0806b58c |
| DWORD_0806b638 | 0x0806b638 | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc L351 | gduelphaseflags_0806b638 |
| DWORD_0806b68c | 0x0806b68c | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse ewram.inc L250 | player_block_stride_0806b68c |
| DWORD_0806b690 | 0x0806b690 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc L312 | gduelfieldslotsbase_0806b690 |
| DWORD_0806b6bc | 0x0806b6bc | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc L351 | gduelphaseflags_0806b6bc |
| DWORD_0806b6ec | 0x0806b6ec | 0x0201e2a0 | gDuelCardCtxBase | reuse ewram.inc L218 | gduelcardctxbase_0806b6ec |
| DWORD_0806b6f0 | 0x0806b6f0 | 0x0201c4e0 | gP1LifePoints | reuse ewram.inc L79 (asm already .word gP1LifePoints; label still DWORD_) | gp1lifepoints_0806b6f0 |
| DWORD_0806b71c | 0x0806b71c | 0x0201c4e0 | gP1LifePoints | reuse ewram.inc L79 | gp1lifepoints_0806b71c |
| DWORD_0806b75c | 0x0806b75c | 0x0201c4e0 | gP1LifePoints | reuse ewram.inc L79 | gp1lifepoints_0806b75c |
| DWORD_0806b760 | 0x0806b760 | 0x00001daa | LP_CARD_TRACK_NEXT_OFF | reuse ewram.inc L248 | lp_card_track_next_off_0806b760 |
| DWORD_0806b764 | 0x0806b764 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse ewram.inc L250 | player_block_stride_0806b764 |
| DWORD_0806bafc | 0x0806bafc | 0x0201b290 | gDuelPhaseFlags | reuse ewram.inc L351 | gduelphaseflags_0806bafc |
| DWORD_0806bb00 | 0x0806bb00 | 0x00000868 | PLAYER_BLOCK_STRIDE | reuse ewram.inc L250 | player_block_stride_0806bb00 |
| DWORD_0806bb04 | 0x0806bb04 | 0x0201e1c8 | gEquipZoneCountTable | reuse ewram.inc L395 | gequipzonecounttable_0806bb04 |
| DWORD_0806bb08 | 0x0806bb08 | 0x0201c510 | gDuelFieldSlots | reuse ewram.inc L312 | gduelfieldslotsbase_0806bb08 |
| DWORD_0806bb2c | 0x0806bb2c | 0x0000135c | CEASEFIRE_CID | NEW card_info.inc | ceasefire_cid_0806bb2c |
| DWORD_0806bb30 | 0x0806bb30 | 0x00001635 | SPELL_ABSORBING_LIFE_CID | NEW card_info.inc | spell_absorbing_life_cid_0806bb30 |

EQ total: 17 slots (15 reuse + 2 NEW: CEASEFIRE_CID, SPELL_ABSORBING_LIFE_CID)

C5 verification:
- NUMINOUS_HEALER_CID=0x1352: grep "0x00001352" constants/card_info.inc -> L1154, OK reuse
- gDuelPhaseFlags=0x0201b290: grep "0x0201b290" constants/ewram.inc -> L351, OK reuse
- PLAYER_BLOCK_STRIDE=0x868: grep "0x868" constants/ewram.inc -> L250, OK reuse
- gDuelFieldSlots=0x0201c510: grep "0x0201c510" constants/ewram.inc -> L312, OK reuse
- gDuelCardCtxBase=0x0201e2a0: grep "0x0201e2a0" constants/ewram.inc -> L218, OK reuse
- gP1LifePoints=0x0201c4e0: grep "0x0201c4e0" constants/ewram.inc -> L79, OK reuse (asm already named)
- LP_CARD_TRACK_NEXT_OFF=0x1daa: grep "0x00001daa" constants/ewram.inc -> L248, OK reuse
- gEquipZoneCountTable=0x0201e1c8: grep "0x0201e1c8" constants/ewram.inc -> L395, OK reuse
- CEASEFIRE_CID=0x135c: grep "0x0000135c" constants/ -> 0 hits (only comment mention in cid_135b comment) -> NEW confirmed; card-stats.s card_0764 slot=0x135C pw=36468556 Ceasefire
- SPELL_ABSORBING_LIFE_CID=0x1635: grep "0x00001635" constants/ -> 0 hits -> NEW confirmed; card-stats.s card_1301 slot=0x1635 pw=99517131 The Spell Absorbing Life

### REF_SLOTS (USER-label + DATA-ref)

| Slot | Target | gas_label | slot_label | Note |
|------|--------|-----------|-----------|------|
| DWORD_0806bb28 | 0x08051319 = check_equip_slot_eligible_by_equip_type+1 | check_equip_slot_eligible_by_equip_type+1 | check_equip_slot_eligible_by_equip_type_ptr_0806bb28 | THUMB+1 fn ptr; function at 0x08051318 in asm/05_equip_eligibility_a.s L18412; used as callback to invoke_count_zone_pair_hits_full_range at 0x0806bb0c; conf: high |
| PTR_DAT_0806b7d4 | 0x0806b7d4 (jump table base) | cid_135b_dispatch_jump_table | cid_135b_dispatch_jump_table | Label rename: already shows .word entries; no value change needed; label semantics: 10-entry raw-addr jump table for cid_135b fn_eligible state stubs |

REF total: 2 slots

### RENAME_SLOTS (descriptive label, EOL, no value change)

DAT_0806b7fc, DAT_0806bc2c, DAT_0806bfbc are ROM_INCBIN START labels. After disasm these become function labels (first stub entry). No explicit RENAME needed -- disasm will replace them with function entry labels.

No additional PTR_ slots requiring rename only.

RENAME total: 0 (handled by disasm phase)

### FUNC_RENAME

No FUNC_RENAME for the 4 named functions in Seg-8b [0x6b56c, 0x6c0cc):
- dispatch_numinous_healer_lp_zone_sprites: handles CID 0x1352 AND 0x135a. The name captures the primary card; the shared-handler dual-CID pattern is consistent with Seg-8a convention (e.g. dispatch_germ_momonga_trigger_display_by_state). No contradicting body evidence. No rename.
- tick_field_slot_bit_and_lp_display, tick_equip_lp_display_seq_with_slot_check, tick_equip_zone_slot_and_lp_indicator_state_machine: all names match function bodies. No rename.

Note for Seg-8c: dispatch_neo_daedalus_placement_check_by_state (0x0806c0cc) has "neo_daedalus" in name but functions for Spear Cretin (CID=0x133b). This is a misname to resolve in Seg-8c (outside Seg-8b range).

### PLATE (R5)

| Function | Type | Content |
|----------|------|---------|
| dispatch_neo_daedalus_placement_check_by_state @ 0x0806c0cc (boundary; plate in asm at line 17183) | substring replace | "FUN_0806b53c" -> "dispatch_spear_cretin_activate_if_chain_subtype" (stale FUN_ from Seg-8a); "Neo-Daedalus placement check" -> "Spear Cretin activation placement check" (2 occurrences: title + description) |
| dispatch_numinous_healer_lp_zone_sprites @ 0x0806b56c | EOL/plate update | Symbolize inline constant references: "CARD_ID_Numinous_Healer=0x1352" -> "NUMINOUS_HEALER_CID=0x1352"; "CARD_ID_Attack_and_Receive=0x135a" -> "ATTACK_AND_RECEIVE_CID=0x135a" |

PLATE total: 2 functions

---

## carve plan (R7)

None -- all 5 ROM_INCBIN blocks are THUMB code. No data tables to carve into rom.s.

---

## disasm plan (R4)

All 5 blocks DISASM THUMB. Method: clearListing range -> setTMode -> DisassembleCommand per stub entry (NOT full range at once; Seg-8a lesson: must disasm per-stub to avoid ContextChangeException).

### Block 0x6b784 (0x4c B, fn_eligible CID=0x135b)

Range: 0x0806b784..0x0806b7d0 (THUMB code); literal pool word at 0x6b7d0 is OUTSIDE the ROM_INCBIN (already assembled as .word 0x0806b7d4).

Single function:
- `check_equip_eligible_cid_135b` @ 0x0806b784
  - THUMB+1 fn ptr in dispatch table @0x1e40448; CID=0x135b (unassigned slot; card_info.inc cid_135b already defined)
  - push {r4,r5,r6,r7,lr}; Ghidra mode-switch .hword 0x4657/0x464e/0x4645; push {r5,r6,r7} (high-reg save)
  - Reads state from gDuelPhaseFlags+0x4a0 (computed as 0x94<<3), dispatches via 10-entry table @0x6b7d4
  - Literal pool at 0x6b7cc: .word gDuelPhaseFlags; .word 0x0806b7d4 (at 0x6b7d0, outside block)
  - Name confidence: high (THUMB+1 CID proof; func returns equip eligibility for state machine dispatch)

### Block 0x6b7fc (0x27c B, state stubs for CID=0x135b)

Range: 0x0806b7fc..0x0806ba78

10 stubs dispatched from 10-entry jump table at 0x6b7d4:
(table entry index -> stub address)

| Index | Stub addr | stub_label |
|-------|-----------|-----------|
| 9 (default/entry) | 0x0806b7fc | cid_135b_state_stub_b7fc |
| 8 | 0x0806b8a8 | cid_135b_state_stub_b8a8 |
| 7 | 0x0806b8d4 | cid_135b_state_stub_b8d4 |
| 6 | 0x0806b944 | cid_135b_state_stub_b944 |
| 5 | 0x0806b950 | cid_135b_state_stub_b950 |
| 4 | 0x0806b990 | cid_135b_state_stub_b990 |
| 2 | 0x0806b9f0 | cid_135b_state_stub_b9f0 |
| 1 | 0x0806ba00 | cid_135b_state_stub_ba00 |
| 0 | 0x0806ba28 | cid_135b_state_stub_ba28 |
| 3 | 0x0806ba64 | cid_135b_state_stub_ba64 |

Total: 10 stub functions. All in [0x6b7fc, 0x6ba78).

### Block 0x6bb74 (0x44 B, fn_eligible CID=0x1362 Magical Hats)

Range: 0x0806bb74..0x0806bbb8 (THUMB code); literal pool at 0x6bbb0/0x6bbb4 inside block:
- 0x6bbb0: .word gDuelPhaseFlags (0x0201b290)
- 0x6bbb4: .word 0x0806bbb8 (ptr to 29-entry jump table immediately following)

Single function:
- `check_equip_eligible_magical_hats` @ 0x0806bb74
  - THUMB+1 fn ptr in dispatch table @0x1e40490; CID=0x1362 Magical Hats (pw=81210420; card-stats.s card_0769)
  - push {r4,r5,r6,r7,lr}; Ghidra mode-switch .hword 0x4657/0x464e/0x4645; push {r5,r6,r7}
  - Reads state from gDuelPhaseFlags+0x4a0 (computed inline), dispatches via 29-entry table @0x6bbb8
  - Name confidence: high (THUMB+1 CID=0x1362 confirmed; Magical Hats fn_eligible handler)

### Block 0x6bc2c (0x374 B, state stubs for Magical Hats CID=0x1362)

Range: 0x0806bc2c..0x0806bfa0

29-entry jump table at 0x6bbb8..0x6bc28 dispatches 11 unique stub targets (entries 0..27+default, many pointing to default stub 0x6bf56):

| Entry indices | Stub addr | stub_label |
|--------------|-----------|-----------|
| 28 (block start) | 0x0806bc2c | magical_hats_state_stub_bc2c |
| 26 | 0x0806bc86 | magical_hats_state_stub_bc86 |
| 25 | 0x0806bc96 | magical_hats_state_stub_bc96 |
| 24 | 0x0806bcaa | magical_hats_state_stub_bcaa |
| 23 | 0x0806bd4c | magical_hats_state_stub_bd4c |
| 22 | 0x0806bda8 | magical_hats_state_stub_bda8 |
| 21 | 0x0806bdce | magical_hats_state_stub_bdce |
| 20 | 0x0806bdf2 | magical_hats_state_stub_bdf2 |
| 10 | 0x0806bf3a | magical_hats_state_stub_bf3a |
| 0 | 0x0806bf4c | magical_hats_state_stub_bf4c |
| 1..9,11..19,27 (default) | 0x0806bf56 | magical_hats_state_stub_default_bf56 |

Total: 11 stub functions. All in [0x6bc2c, 0x6bfa0).

Note: stub at 0x6bdf2 or nearby sub-stub accesses 7-entry table via literal pool at 0x6bf9c (python: struct.unpack('<I',rom[0x6bf9c:0x6bfa0])[0]==0x0806bfa0 confirmed). Literal pool at offset 0x370 within block.

### Block 0x6bfbc (0x110 B, sub-dispatch stubs from Magical Hats nested dispatch)

Range: 0x0806bfbc..0x0806c0cc

7-entry jump table at 0x6bfa0..0x6bfb8 dispatches 7 unique stubs (last entry [6] = block start = raw ref):

| Index | Stub addr | stub_label |
|-------|-----------|-----------|
| 6 (entry) | 0x0806bfbc | magical_hats_zone_state_stub_bfbc |
| 5 | 0x0806c050 | magical_hats_zone_state_stub_c050 |
| 4 | 0x0806c066 | magical_hats_zone_state_stub_c066 |
| 3 | 0x0806c080 | magical_hats_zone_state_stub_c080 |
| 2 | 0x0806c08e | magical_hats_zone_state_stub_c08e |
| 1 | 0x0806c0a0 | magical_hats_zone_state_stub_c0a0 |
| 0 | 0x0806c0ae | magical_hats_zone_state_stub_c0ae |

Total: 7 stub functions. All in [0x6bfbc, 0x6c0cc).

**Disasm total new functions: 1 + 10 + 1 + 11 + 7 = 30 new stub functions**

---

## New constants / globals (must first prove no existing inc reuse)

### card_info.inc (2 new entries)

```
.equ CEASEFIRE_CID,              0x0000135c  @ Ceasefire (pw=36468556; card-stats.s card_0764 slot=0x135C); tick_equip_zone_slot_and_lp_indicator_state_machine dispatch by card_id (CID=0x135c path: submit_lp_indicator_with_slot_xor_flag); conf: high
.equ SPELL_ABSORBING_LIFE_CID,   0x00001635  @ The Spell Absorbing Life (pw=99517131; card-stats.s card_1301 slot=0x1635); tick_equip_zone_slot_and_lp_indicator_state_machine dispatch by card_id (CID=0x1635 path: submit_effect_zone_lp_and_shape_sprites); conf: high
```

Also needed (new in this seg but defined from Seg-8a survey; verify still missing):

```
.equ MAGICAL_HATS_CID,           0x00001362  @ Magical Hats (pw=81210420; card-stats.s card_0769 slot=0x1362); fn_eligible handler check_equip_eligible_magical_hats via dispatch table @0x1e40490; conf: high
```

C5 verify: grep "0x00001362" constants/ -> 0 hits -> NEW confirmed.

Placement: adjacent to cid_135b (L1158) and ATTACK_AND_RECEIVE_CID (L1157): insert MAGICAL_HATS_CID after line 1159 (after 0x1362 neighborhood), CEASEFIRE_CID near 0x135c neighborhood, SPELL_ABSORBING_LIFE_CID in 0x16xx range.

Total new equates: 3 (MAGICAL_HATS_CID + CEASEFIRE_CID + SPELL_ABSORBING_LIFE_CID)

---

## ss5.1 registration (Rule 3) -- 0-reference blocks

None in Seg-8b. All 5 ROM_INCBIN blocks have confirmed references (THUMB+1 or real raw refs). No orphan blocks.

---

## Consumer evidence (R6) -- key slot semantics

| Slot | Consumer file:line | Confidence |
|------|--------------------|-----------|
| CEASEFIRE_CID=0x135c | asm/08 L17103-17106 (DWORD_0806bb2c = 0x135c; function tick_equip_zone_slot_and_lp_indicator_state_machine plate L17002 explicitly names "0x135c Ceasefire"); card-stats.s L9947 slot=0x135C | high |
| SPELL_ABSORBING_LIFE_CID=0x1635 | asm/08 L17105-17106 (DWORD_0806bb30 = 0x1635; function plate L17002 explicitly names "0x1635 The Spell Absorbing Life"); card-stats.s L16928 slot=0x1635 | high |
| MAGICAL_HATS_CID=0x1362 | asm/08 L17141 ROM_INCBIN 0x6bb74; dispatch table @0x1e40490: python struct.unpack('<I',rom[0x1e4048c:0x1e40490])[0]==0x1362; card-stats.s L10012 slot=0x1362 Magical Hats pw=81210420 | high |
| cid_135b=0x135b | asm/08 L16986 ROM_INCBIN 0x6b784; dispatch table @0x1e40448: python struct.unpack('<I',rom[0x1e40444:0x1e40448])[0]==0x135b; card_info.inc L1158 cid_135b already defined | high |
| check_equip_slot_eligible_by_equip_type+1 (0x08051319) | asm/08 L17101-17102 (DWORD_0806bb28 = 0x08051319); asm/05_equip_eligibility_a.s L18412 function entry push {r4,lr} @ 0x08051318; asm/07_equip_effect_chain.s L4540 plate lists "FN_PTR = 0x08051319" confirming identity | high |
| gEquipZoneCountTable=0x0201e1c8 | asm/08 L17083-17084 (DWORD_0806bb04 = 0x0201e1c8); ewram.inc L395 confirmed | high |
| NUMINOUS_HEALER_CID=0x1352 | asm/08 L16709-16710 (DWORD_0806b58c = 0x1352); function plate L16685 states "0x1352 (Numinous Healer)"; card_info.inc L1154 confirmed | high |

---

## Seek help

None -- all semantics have file:line + high confidence evidence. No blocked items.

---

## Executor Report: F08-Seg-8b

- Slots: EQ=17 REF=2 RENAME=0 FUNC_RENAME=0 PLATE=2
- disasm=5 blocks (30 new stubs: 1+10+1+11+7) carve=0 ss5.1=0
- New constants: card_info.inc +3 (MAGICAL_HATS_CID=0x1362, CEASEFIRE_CID=0x135c, SPELL_ABSORBING_LIFE_CID=0x1635)
- Seek help: none
- proposal: doc/dev/refine/F08-Seg-8b.proposal.md
