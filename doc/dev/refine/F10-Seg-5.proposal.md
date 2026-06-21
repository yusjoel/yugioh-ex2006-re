# Refine Proposal: F10-Seg-5a  [0x0807db20..0x0807ec10)

Split half: Seg-5a covers the first 6 named functions + 6 ROM_INCBIN blocks.
Seg-5b continues at 0x0807ec10 (see F10-Seg-5b.proposal.md).

## Segment Mapping

- Function entries: 6
  - enqueue_equip_zone_sprites_both_players  @ 0x0807db20 (line 8281)
  - tick_equip_oam_activation_text_display   @ 0x0807db5c (line 8325)
  - dispatch_freed_matchless_general_equip_display @ 0x0807dca4 (line 8494)
  - submit_monster_equip_bitmap_lp_indicator @ 0x0807dcf8 (line 8544)
  - dispatch_equip_zone_sprite_by_state_code @ 0x0807e24c (line 8641)
  - enqueue_lp_indicator_and_sprite_for_slot @ 0x0807e5a4 (line 8843)
- ROM_INCBIN blocks: 6
  - BLK1: 0x7dd68, 0x30  (48 B) -- fn_eligible_magical_mallet sub-stub via THUMB+1 ref
  - BLK2: 0x7ddac, 0x16c (364 B) -- Magical Mallet dispatch sub-stubs (R4 disasm)
  - BLK3: 0x7df90, 0x2bc (700 B) -- dispatch_equip_zone_sprite_by_state_code dispatch sub-stubs (R4 disasm)
  - BLK4: 0x7e398, 0x2c  (44 B)  -- fn_eligible_ancient_gear_drill sub-stub via THUMB+1 ref
  - BLK5: 0x7e438, 0x16c (364 B) -- Ancient Gear Drill dispatch sub-stubs (R4 disasm)
  - BLK6: 0x7e5d4, 0x63c (1596 B) -- 5 x fn_eligible stubs (BES Covered Core / D.D. Guide / Disciple / Malice Ascendant / Divine Dragon - Excelion) (R4 disasm x5)
- Auto-name slots: 15 unique addresses (18 total instances; 2 are PTR_NAMED already at 0x7dc00/0x7dc98; 1 DWORD_0807dd5c needs RENAME to PTR_gP1LifePoints_0807dd5c)
- switchD entries: none in Seg-5a

## Data Block Classification (Rule 2/3) -- ref-scan evidence

| Block         | ref-scan (raw / THUMB+1)           | Judgment  | Rationale |
|---------------|------------------------------------|-----------|-----------|
| BLK1 0x7dd68/0x30  | raw=0, thumb+1=1 @ 0x09e4xxxx      | R4 disasm | THUMB fn_eligible code stub; 1 THUMB+1 ref from FS dispatch table; 48B = single fn |
| BLK2 0x7ddac/0x16c | raw=1 @ 0x7dd98 (jump table ptr), thumb+1=0 | R4 disasm | Jump table in preceding .word list points into BLK2; 5 unique sub-stub targets |
| BLK3 0x7df90/0x2bc | raw=1 @ 0x7df8c (jump table .word), thumb+1=0 | R4 disasm | Jump table at PTR_DAT_0807df1c (29 entries, states 0..0x1c, 12 unique targets) points into BLK3; BLK3 ends exactly at 0x0807e24c = dispatch_equip_zone_sprite_by_state_code start |
| BLK4 0x7e398/0x2c  | raw=0, thumb+1=1 @ 0x09e4xxxx      | R4 disasm | THUMB fn_eligible code stub; 1 THUMB+1 ref from FS dispatch table; 44B = single fn |
| BLK5 0x7e438/0x16c | raw=1 @ 0x7e428 (jump table .word), thumb+1=0 | R4 disasm | Jump table in preceding .word list points into BLK5; 7 unique sub-stub targets |
| BLK6 0x7e5d4/0x63c | raw=0, thumb+1=5 @ 0x09e4xxxx      | R4 disasm x5 | 5 independent fn_eligible code stubs; each has exactly 1 THUMB+1 ref from FS dispatch table entries; NOT a monolithic block; ends at 0x0807ec10 |

ref-scan validation script:
```python
import struct
rom = open("roms/2343.gba", "rb").read()
for blk_off, blk_sz, label in [
    (0x7dd68, 0x30, "BLK1"), (0x7ddac, 0x16c, "BLK2"),
    (0x7df90, 0x2bc, "BLK3"), (0x7e398, 0x2c, "BLK4"),
    (0x7e438, 0x16c, "BLK5"), (0x7e5d4, 0x63c, "BLK6"),
]:
    a = blk_off + 0x08000000
    print(f"{label}: raw={rom.count(struct.pack('<I',a))} thumb+1={rom.count(struct.pack('<I',a|1))}")
```
Results (all verified):
- BLK1: raw=0, thumb+1=1; BLK2: raw=1, thumb+1=0; BLK3: raw=1, thumb+1=0
- BLK4: raw=0, thumb+1=1; BLK5: raw=1, thumb+1=0; BLK6: raw=0, thumb+1=5

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

All REUSE -- grep by VALUE confirmed 0 new constants needed for Seg-5a equates:

| slot addr | value       | action | const_name                         | note |
|-----------|-------------|--------|------------------------------------|------|
| 0x7dc9c   | 0x00001d68  | REUSE  | ELIGIB_SPRITE_CTRL_OFF             | ewram.inc line 422 |
| 0x7dcd4   | 0x000014c4  | REUSE  | FREED_THE_MATCHLESS_GENERAL_CID    | card_info.inc line 1413 |
| 0x7dd60   | 0x000010d0  | REUSE  | LP_ACTIVATION_LINK_FLAG_OFF        | ewram.inc line 483 (domain=gP1LifePoints) |
| 0x7e2f0   | 0x000004a4  | REUSE  | EQUIP_PHASE_FRAME_OFF              | ewram.inc line 437 |
| 0x7e38c   | 0x00000868  | REUSE  | PLAYER_BLOCK_STRIDE                | ewram.inc line 251 |
| 0x7e394   | 0x000004a4  | REUSE  | EQUIP_PHASE_FRAME_OFF              | ewram.inc line 437 (dup slot same fn) |

NEW equates needed:

| slot addr | value       | action | const_name                         | note |
|-----------|-------------|--------|------------------------------------|------|
| 0x7dc04   | 0x000010d3  | NEW    | TRIGGER_OP_PARAM_10D3              | trigger_card_display_op31 mode param; 0 grep hits by value in constants/; add to duel_field.inc or equip_display.inc |
| 0x7dc08   | 0x08090625  | NEW    | invoke_effect_node_active_fn_ptr   | THUMB+1 ptr to invoke_effect_node_with_active_flag_3arg (0x08090624); confirmed in asm/10 line 5182+7053+8408; 0 grep hits in constants/; add to equip_display.inc. NOTE: this is a ROM literal-pool THUMB+1 immediate (fn at 0x08090624; value = addr+1), NOT an EWRAM/IWRAM stored fn-ptr slot. The `_fn_ptr` suffix reflects the pointer-nature of the constant (a code pointer, not data); the slot itself is a ROM .word load target, distinguishable from EWRAM storage slots by its ROM address (0x08xxxxxx). |

### REF_SLOTS (USER-label + DATA-ref)

| slot addr | target value  | gas_label              | slot_label                      | note |
|-----------|---------------|------------------------|---------------------------------|------|
| 0x7db58   | 0x0201e1c8    | gEquipZoneCountTable   | DAT_0807db58                    | ewram.inc line 397 |
| 0x7db88   | 0x0201b290    | gDuelPhaseFlags        | DAT_0807db88                    | ewram.inc line 353 |
| 0x7dca0   | 0x0201e2a0    | gDuelCardCtxBase       | DAT_0807dca0                    | ewram.inc line 218 |
| 0x7dcd0   | 0x0201b290    | gDuelPhaseFlags        | DAT_0807dcd0                    | same global reuse |
| 0x7dd64   | 0x0201bb90    | gEquipChainSlotRefs    | DWORD_0807dd64                  | ewram.inc line 317 |
| 0x7e2ec   | 0x0201b290    | gDuelPhaseFlags        | DWORD_0807e2ec                  | same global reuse |
| 0x7e390   | 0x0201c510    | gDuelFieldSlots        | DWORD_0807e390                  | ewram.inc line 314 |

PTR_NAMED slots (already use symbol gP1LifePoints -- skip):
- 0x7dc00 PTR_gP1LifePoints_0807dc00
- 0x7dc98 PTR_gP1LifePoints_0807dc98

NOTE: 0x7dd5c was initially listed here as "PTR_NAMED already" but its LABEL in asm is still DWORD_0807dd5c (not yet renamed to PTR_gP1LifePoints_0807dd5c). It has been moved to RENAME_SLOTS above. Value (.word gP1LifePoints) is already correct; only the label rename is required.

### RENAME_SLOTS (pure rename + EOL)

| slot addr | old label           | new label                        | note |
|-----------|---------------------|----------------------------------|------|
| 0x7dd5c   | DWORD_0807dd5c      | PTR_gP1LifePoints_0807dd5c       | value already resolves to gP1LifePoints (.word gP1LifePoints); only the LABEL is still auto-named DWORD_; rename to match sibling pattern at 0x7dc00/0x7dc98; Ghidra: renameData(0x0807dd5c, "PTR_gP1LifePoints_0807dd5c") |

(1 rename; all other labels in Seg-5a are already correctly named or handled by REF_SLOTS above.)

### FUNC_RENAME (misnomer corrections)

None identified. All 6 named functions have semantics consistent with their names.

### PLATE (R5)

No plate modifications needed in Seg-5a -- the 6 functions' existing plate comments have no stale FUN_ references and no CJK text.

Verify: plates at lines 8312-8323, 8484-8492, 8538-8543, 8640 have no FUN_ strings (confirmed by grep -- 0 hits in line range 8281..8877).

## Disasm Plan (R4)

### BLK1: fn_eligible_magical_mallet  [0x0807dd68..0x0807dd98)  48B

FS entry: 0x09e4xxxx; THUMB+1 ref: 1 (FS table).
CID at entry+12: confirm 0x0000198d = MAGICAL_MALLET_CID (card_info.inc line 842).
Stub contains: push {r4,r5,lr}; reads gDuelPhaseFlags+0x94*8 state; calls MOV PC,r0 dispatch via jump table at 0x0807dd98 (the .word list following BLK1).
Function name: fn_eligible_magical_mallet

Disasm action: DisassembleCommand(addr=0x0807dd68, THUMB) -- single stub.

### BLK2: Magical Mallet dispatch sub-stubs  [0x0807ddac..0x0807df18)  364B

Jump table at 0x0807dd98..0x0807ddac (5 entries, pointing into BLK2):
- 0x0807dd98: .word 0x0807dec8  -> case_stub_0x0807dec8
- 0x0807dd9c: .word 0x0807dea4  -> case_stub_0x0807dea4
- 0x0807dda0: .word 0x0807de20  -> case_stub_0x0807de20
- 0x0807dda4: .word 0x0807ddec  -> case_stub_0x0807ddec
- 0x0807dda8: .word 0x0807ddac  -> case_stub_0x0807ddac (case 0 = entry of BLK2)

All 5 targets are inside BLK2. Entry 0x0807ddac = start of BLK2 directly.
Function names: equip_mallet_case0_0807ddac, equip_mallet_case1_0807ddec, equip_mallet_case2_0807de20, equip_mallet_case3_0807dea4, equip_mallet_case4_0807dec8.

Disasm action: DisassembleCommand for each of the 5 entry points individually (per-stub rule; single range only disassembles first stub due to THUMB context changes).

### BLK3: dispatch_equip_zone_sprite_by_state_code dispatch sub-stubs  [0x0807df90..0x0807e24c)  700B

Jump table at PTR_DAT_0807df1c (29 entries, states 0..0x1c; .word 0x0807df1c): 12 unique targets in BLK3:
- 0x0807df90 (= BLK3 start, entry [0x1c] = state 0x1c = highest index)
- 0x0807dff4, 0x0807e01c, 0x0807e0bc, 0x0807e124, 0x0807e164, 0x0807e1c6, 0x0807e1f0, 0x0807e1fc, 0x0807e208, 0x0807e212, 0x0807e242

BLK3 ends at 0x0807e24c = start of dispatch_equip_zone_sprite_by_state_code. No overlap.

Function names: equip_zone_stub_0807df90, equip_zone_stub_0807dff4, equip_zone_stub_0807e01c, equip_zone_stub_0807e0bc, equip_zone_stub_0807e124, equip_zone_stub_0807e164, equip_zone_stub_0807e1c6, equip_zone_stub_0807e1f0, equip_zone_stub_0807e1fc, equip_zone_stub_0807e208, equip_zone_stub_0807e212, equip_zone_stub_0807e242 (12 stubs).

Disasm action: 12 x DisassembleCommand (one per entry point).

### BLK4: fn_eligible_ancient_gear_drill  [0x0807e398..0x0807e424)  44B

FS entry; THUMB+1 ref: 1. CID at entry+12: confirm 0x000019ae = ANCIENT_GEAR_DRILL_CID (card_info.inc line 695).
Function name: fn_eligible_ancient_gear_drill

Disasm action: DisassembleCommand(addr=0x0807e398, THUMB).

### BLK5: Ancient Gear Drill dispatch sub-stubs  [0x0807e438..0x0807e5a4)  364B

Jump table at 0x0807e3c4..0x0807e438 (7 unique targets listed in asm at lines 8810..8839):
- 0x0807e438 (BLK5 start = case 0)
- 0x0807e46a, 0x0807e47e, 0x0807e538, 0x0807e57c, 0x0807e58e, 0x0807e598 (default)

Function names: ag_drill_case0_0807e438, ag_drill_case1_0807e46a, ag_drill_case2_0807e47e, ag_drill_case3_0807e538, ag_drill_case4_0807e57c, ag_drill_case5_0807e58e, ag_drill_default_0807e598 (7 stubs).

Disasm action: 7 x DisassembleCommand.

### BLK6: 5 x fn_eligible stubs  [0x0807e5d4..0x0807ec10)  1596B

5 independent fn_eligible code stubs, each referenced by exactly 1 THUMB+1 ptr in FS dispatch table:
- 0x0807e5d5 (THUMB+1 for 0x0807e5d4): CID = 0x000019bf = B.E.S. Covered Core  -> fn_eligible_bes_covered_core
- 0x0807e5d4 + offset_stub_1: CID = 0x000019c0 = D.D. Guide                      -> fn_eligible_dd_guide
- 0x0807e5d4 + offset_stub_2: CID = 0x000019c2 = Disciple of the Forbidden Spell  -> fn_eligible_disciple_forbidden_spell
- 0x0807e5d4 + offset_stub_3: CID = 0x000019d0 = Malice Ascendant                 -> fn_eligible_malice_ascendant
- 0x0807e5d4 + offset_stub_4: CID = 0x000019d3 = Divine Dragon - Excelion         -> fn_eligible_divine_dragon_excelion

NOTE: An extra THUMB+1 ref was found at 0x082abd08 -> 0x0807e7c5. This is a code literal pool word in an unrelated function (surrounding bytes are THUMB instruction code, misaligned to 4B boundary), NOT a new fn_eligible entry. Excluded from fn_eligible list.

Each stub is a complete fn_eligible function. Stubs are NOT monolithic -- each has push/pop and independent logic. The 5 stubs together cover the full 1596B.

Disasm action: 5 x DisassembleCommand, one per stub start address (exact boundaries to be determined by Ghidra's fn analysis after first stub disasm; if stubs share code paths they still need per-stub createFunction).

CIDs for new constants (these 4 CIDs not in constants/):
- 0x000019bf = B.E.S. Covered Core: NEW -> BES_COVERED_CORE_CID
- 0x000019c0 = D.D. Guide: NEW -> DD_GUIDE_CID
- 0x000019c2 = Disciple of the Forbidden Spell: NEW -> DISCIPLE_FORBIDDEN_SPELL_CID
- 0x000019d3 = Divine Dragon - Excelion: NEW -> DIVINE_DRAGON_EXCELION_CID
- (0x000019d0 = Malice Ascendant: REUSE MALICE_ASCENDANT_CID from card_info.inc line 1337)

## New Constants / Globals Needed

Add to `constants/equip_display.inc` (new file) or `constants/card_info.inc`:

```asm
@ Seg-5a new equates (equip display / trigger op)
.equ TRIGGER_OP_PARAM_10D3,       0x000010d3  @ trigger_card_display_op31 mode param (tick_equip_oam_activation_text_display); 0 existing hits by value
.equ invoke_effect_node_active_fn_ptr, 0x08090625  @ THUMB+1 ptr to invoke_effect_node_with_active_flag_3arg; fn at 0x08090624; 0 existing hits by value

@ New card CIDs (from BLK6 fn_eligible)
.equ BES_COVERED_CORE_CID,        0x000019bf  @ B.E.S. Covered Core (pw=15317640; card_2034 slot=0x19BF)
.equ DD_GUIDE_CID,                0x000019c0  @ D.D. Guide (pw=52702748; card_2035 slot=0x19C0)
.equ DISCIPLE_FORBIDDEN_SPELL_CID, 0x000019c2 @ Disciple of the Forbidden Spell (pw=15595052; card_2037 slot=0x19C2)
.equ DIVINE_DRAGON_EXCELION_CID,  0x000019d3  @ Divine Dragon - Excelion (pw=10032958; card_2054 slot=0x19D3)
```

C5 dedup proof (all grep by VALUE = 0 hits, confirmed before adding):
- 0x000010d3: grep -rn "0x000010d3" constants/ -> 0 hits
- 0x08090625: grep -rn "0x08090625" constants/ -> 0 hits
- 0x000019bf: grep -rn "0x000019bf" constants/ -> 0 hits
- 0x000019c0: grep -rn "0x000019c0" constants/ -> 0 hits
- 0x000019c2: grep -rn "0x000019c2" constants/ -> 0 hits
- 0x000019d3: grep -rn "0x000019d3" constants/ -> 0 hits

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None. All 6 BLK1-6 have at least 1 reference (THUMB+1 or raw .word jump table pointer). No blocks are eligible for 5.1 deferral.

## Consumer Evidence (R6) -- key slot semantics

| slot          | value      | consumer / evidence                                        | confidence |
|---------------|------------|-------------------------------------------------------------|------------|
| 0x7dc04/10d3  | 0x10d3     | asm/10 line 8398: `bl trigger_card_display_op31_if_not_active` with r1=0x10d3 from this slot; r0=player_id; confirmed trigger mode param | high |
| 0x7dc08/90625 | 0x08090625 | asm/10 lines 5182, 7053, 8408: identical .word value, all comment it as fn-ptr invoke_effect_node_with_active_flag_3arg+1 (THUMB+1); set_equip_activation_state_by_mode__08096a4c uses it as indirect call target | high |
| 0x7dc9c/1d68  | 0x1d68     | asm/10 line 8382: `ldrh r0,[r0,#0x0]` reads [gP1LifePoints + player*0x868 + 0x1d68] -> card_id; ewram.inc line 422 confirms ELIGIB_SPRITE_CTRL_OFF semantics | high |
| 0x7dcd4/14c4  | 0x14c4     | asm/10 line 8484: plate "Freed the Matchless General (card 0x14c4)"; card_info.inc FREED_THE_MATCHLESS_GENERAL_CID | high |
| 0x7dd60/10d0  | 0x10d0     | asm/10 lines 8549-8557: reads [gP1LifePoints+0x10d0]; tests bit0==0 && bit1==1; ewram.inc LP_ACTIVATION_LINK_FLAG_OFF=0x10d0 domain gP1LifePoints | high |
| 0x7e2f0/4a4   | 0x4a4      | asm/10 line 8708: `add r6,r9` then `str r0,[r6,#0x0]`/`ldr r0,[r6,#0x0]` on EQUIP_PHASE_FRAME_OFF slot; ewram.inc EQUIP_PHASE_FRAME_OFF=0x4a4 | high |

## Seek Help / Blocked

None. All blocks have consumers or structural evidence. 0x08090625 has 3 cross-file independent occurrences confirming identity.

---

## Seg-5a Summary Counts

- EQ slots: 8 (6 REUSE + 2 NEW)
- REF slots: 7 (all REUSE existing globals)
- RENAME slots: 1 (DWORD_0807dd5c -> PTR_gP1LifePoints_0807dd5c)
- FUNC_RENAME: 0
- PLATE: 0
- disasm blocks: 6 (BLK1: 1fn, BLK2: 5fn, BLK3: 12fn, BLK4: 1fn, BLK5: 7fn, BLK6: 5fn = 31 fn total)
- carve: 0
- section 5.1: 0
- new constants: 6 (2 equate + 4 CID)
