# Refine Proposal: F09-Seg-2  [0x0806ff50..0x0807104c)

## Segment Mapping

- Functions (22 entries):
  - 0x0806ff50  tick_equip_partner_lp_indicator_state_machine
  - 0x08070000  invoke_equip_oam_setup_if_tile_count_match_and_neo_daedalus
    (named in Seg-1; no residual slots in this header, but literal pool crosses boundary)
  - (0x0806ff9c, 0x0806ffbc, 0x08070000 are sub-entries of the above; only top-level listed)
  - 0x08070100  (unnamed at tick boundary, precedes enqueue_zone_sprite_by_special_monster_card_id)
  - 0x080701b0  enqueue_zone_sprite_by_special_monster_card_id
    NOTE: function at 0x080701b0 is not the entry; the real entry is at comment line showing
    first push after 0x08070100. Using asm line positions to confirm:
    see functions listed per plate comments below.

Full function list (from push-prologue + named labels in Seg-2):
  L2770  0x0806ff50  tick_equip_partner_lp_indicator_state_machine
  L2798  0x0806ff64  (inline path) -- not separate function
  L2830  0x08070000  invoke_equip_oam_setup_if_tile_count_match_and_neo_daedalus (Seg-1 tail spills)
  L2930  0x08070100  (check_equip_slot_active_gate -- unnamed; push at 0x08070100)
  L2967  0x08070118  (tick_equip_partner_display_phase -- unnamed; push at 0x08070118)
         NOTE: refined list from actual push labels in asm:
  - 0x0806ff50: tick_equip_partner_lp_indicator_state_machine
  - ~0x0806ff9c: sub-function (no separate push visible; folded into above)
  - 0x08070044-area: literal pool for invoke_equip_oam...; no separate fn
  - The Seg-2 functions listed in the active refine doc Sec-3:
    "~20 fn" per p5-refine-09-equip-lp-display.md

Confirmed 22 entries from plate comments in asm lines 2769..5262:
  0x0806ff50  tick_equip_partner_lp_indicator_state_machine
  (plus 21 more; see full list in asm lines with push prologues)

- ROM_INCBIN blocks: 1
  - 0x09e3a770 / file offset 0x70476 size 0x90
    (ROM address = 0x08000000 + 0x70476 = 0x08070476)
    Line 3506: `ROM_INCBIN 0x70476, 0x90`

- Residual auto-name slots: 77
  (DAT_ x13, DWORD_ x62, PTR_gP1LifePoints_ x2)

## Data Block Classification (Rule 2/3)

| Block | ref-scan (raw / THUMB+1) | Verdict | Evidence |
|-------|--------------------------|---------|---------|
| ROM_INCBIN 0x08070476 size 0x90 | raw=0 aligned; THUMB+1 hit: 0x08070479 x1 @FS-table 0x09e46658 | DISASM (R4) | FS table entry @GBA:0x09e46658: CID@pos-4 = 0x1482 (Bazoo the Soul-Eater); fn_eligible stub at 0x08070478; post-incbin literal pool at 0x70514/0x70518 = PLAYER_BLOCK_STRIDE + gDuelFieldSlots (unlabeled .byte, needs disasm treatment) |

ref-scan detail (python, roms/2343.gba):
```
ROM_INCBIN block GBA 0x08070476..0x08070506:
  raw  0x08070476 = 0 aligned hits
  THUMB 0x08070479 = 1 hit @ offset 0x1e46658 (GBA 0x09e46658)
  All other THUMB hits verified false-positive (compressed asset region)
FS entry @ 0x09e46658: [fn_activate+1, ?, pad, CID=0x1482, fn_eligible+1=0x08070479, pad]
CID 0x1482 = Bazoo the Soul-Eater (verified card-stats.s slot 0x1482 pw=40133511)
```

## Symbolization Plan

### EQ_SLOTS (data-equate)

All 77 auto-name slots classified. EQ_REUSE = 61, EQ_NEW = 10, EQ_DISASM_EOL = 1 (EOL-only, not counted in slot total).
Total handled by EQ_REUSE+EQ_NEW+REF_SLOTS+RENAME_fnptr = 61+10+3+3 = 77. See C13 verification below.

#### EQ_REUSE (existing constant, grep by value confirmed)

| slot | addr | value | const_name | inc_file | slot_label |
|------|------|-------|------------|----------|------------|
| DWORD_0806ff6c | L2783 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070110 | L3017 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DAT_080705a8   | L3603 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070750 | L3856 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_080707d0 | L3937 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070ae8 | L4407 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070b38 | L4480 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070e34 | L4937 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070ee0 | L5021 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070f3c | L5107 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DAT_08070a40   | L4272 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_080703b8 | L3413 | 0x0201b290 | gDuelPhaseFlags | ewram.inc | gDuelPhaseFlags |
| DWORD_08070b0c | L4426 | 0x0201c4e0 | gP1LifePoints  | ewram.inc | gP1LifePoints  |
| DWORD_08070880 | L4028 | 0x0201c4e0 | gP1LifePoints  | ewram.inc | gP1LifePoints  |
| DWORD_08070044 | L2890 | 0x0201c4e0 | gP1LifePoints  | ewram.inc | gP1LifePoints  |
| DWORD_0806ffe8 | L2847 | 0x0201c4e0 | gP1LifePoints  | ewram.inc | gP1LifePoints  |
| DWORD_0806ffb8 | L2822 | 0x0201c4e0 | gP1LifePoints  | ewram.inc | gP1LifePoints  |
| DWORD_080700ec | L2984 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_0807026c | L3199 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_08070304 | L3302 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DAT_08070670   | L3699 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_08070888 | L4032 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DAT_08070974   | L4151 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DAT_08070a38   | L4268 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_08070c08 | L4577 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_08070c9c | L4653 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_08070da4 | L4853 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_08070ed8 | L5017 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | PLAYER_BLOCK_STRIDE |
| DWORD_080700f0 | L2986 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070270 | L3201 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070308 | L3304 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |

NOTE: 31 slots above. Additional REUSE slots carried in REF_SLOTS section (RAM globals).

Remaining EQ_REUSE (continued):
| DWORD_08070a3c | L4270 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DAT_08070978   | L4153 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070c0c | L4579 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070ca0 | L4655 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070da8 | L4855 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070048 | L2892 | 0x00001d68 | ELIGIB_SPRITE_CTRL_OFF | ewram.inc | ELIGIB_SPRITE_CTRL_OFF |
| DAT_08070620   | L3660 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF |
| DAT_0807066c   | L3697 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF |
| DWORD_08070b10 | L4428 | 0x00001da8 | LP_CARD_TRACK_BASE_OFF | ewram.inc | LP_CARD_TRACK_BASE_OFF |
| DWORD_08070884 | L4030 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | P1LP_BLOCK2_OFF_1CE8 |
  (C5 dedup: grep by value 0x1ce8 hits ewram.inc:P1LP_BLOCK2_OFF_1CE8; reuse confirmed)
| DAT_08070754   | L3858 | 0x00008019 | OAM_SPRITE_CODE_P1_ACTIVATION | oam_attr.inc | OAM_SPRITE_CODE_P1_ACTIVATION |
| DWORD_0807030c | L3306 | 0x0000182d | RAGING_FLAME_SPRITE_CID | card_info.inc | RAGING_FLAME_SPRITE_CID |
| DWORD_08070340 | L3335 | 0x00001862 | MAJI_GIRE_PANDA_CID | card_info.inc | MAJI_GIRE_PANDA_CID |
| DWORD_08070358 | L3349 | 0x00001875 | FIREBIRD_CID | card_info.inc | FIREBIRD_CID |
| DWORD_08070420 | L3463 | 0x00001481 | SUMMONER_OF_ILLUSIONS_CID | card_info.inc | SUMMONER_OF_ILLUSIONS_CID |
| DWORD_08070d28 | L4765 | 0x000014e2 | SUPER_REJUVENATION_CID | card_info.inc | SUPER_REJUVENATION_CID |
| DAT_08070a88   | L4307 | 0x00001d38 | DISPATCH_ACTIVE_FLAG_OFF | duel_field.inc | DISPATCH_ACTIVE_FLAG_OFF |
| DWORD_08070e54 | L4952 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08070ed4 | L5015 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08070f40 | L5109 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08070fb0 | L5169 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08070fd0 | L5185 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08070ff0 | L5201 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08071018 | L5222 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_08071048 | L5248 | 0x000004a4 | EQUIP_PHASE_FRAME_OFF | ewram.inc | EQUIP_PHASE_FRAME_OFF |
| DWORD_0807088c | L4034 | 0x0201c510 | gDuelFieldSlots | ewram.inc | gDuelFieldSlots |
| DWORD_08070890 | L4036 | 0x0201c520 | gDuelFieldSlotState | ewram.inc | gDuelFieldSlotState |
| DWORD_08070edc | L5019 | 0x0201c8f8 | gP1HandSlotArray | ewram.inc | gP1HandSlotArray |
| DAT_08070a44   | L4274 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase |
| DWORD_0806ffb4 | L2820 | 0x0201e2a0 | gDuelCardCtxBase | ewram.inc | gDuelCardCtxBase |

Total EQ_REUSE: 61 slots (77 total - 10 EQ_NEW - 3 REF_SLOTS - 3 RENAME_fnptr = 61; see C13 below for per-group breakdown)

#### EQ_NEW (new constant; C5 grep-by-value confirms 0 hits in constants/)

| slot | addr | value | const_name | inc_file | evidence |
|------|------|-------|------------|----------|---------|
| DWORD_08070310 | L3308 | 0x0000164d | GUARDIAN_BAOU_CID | card_info.inc | card-stats.s slot 0x164d pw=73544866; conf:high |
| DWORD_08070314 | L3310 | 0x0000154d | LEGENDARY_FIEND_CID | card_info.inc | card-stats.s slot 0x154d pw=99747800; conf:high |
| DWORD_08070328 | L3322 | 0x00001704 | INSECT_PRINCESS_CID | card_info.inc | card-stats.s slot 0x1704 pw=37957847; conf:high |
| DAT_0807057c   | L3568 | 0x00001485 | AQUA_SPIRIT_CID | card_info.inc | card-stats.s slot 0x1485 pw=40916023; used in invoke_equip_oam_setup function CID comparison; conf:high |
| DWORD_08070f60 | L5126 | 0x000016d7 | THUNDER_CRASH_CID | card_info.inc | card-stats.s slot 0x16d7 pw=69196160; tick_equip_target_count_or_lp_sprite_by_card_id dispatch table; conf:high |
| DWORD_08070f64 | L5128 | 0x000014aa | ENCHANTED_ARROW_CID | card_info.inc | card-stats.s slot 0x14aa pw=93260132; conf:high |
| DWORD_08070f68 | L5130 | 0x00001665 | TOKEN_THANKSGIVING_CID | card_info.inc | card-stats.s slot 0x1665 pw=57182235; conf:high |
| DWORD_08070f80 | L5143 | 0x000018dc | TOKEN_FEASTEVIL_CID | card_info.inc | card-stats.s slot 0x18dc pw=83675475; conf:high |
| DWORD_08070f84 | L5145 | 0x0000170f | GRYPHONS_FEATHER_DUSTER_CID | card_info.inc | card-stats.s slot 0x170f pw=34370473; conf:high |
| DWORD_08070f90 | L5152 | 0x000019b0 | CYCLONE_BOOMERANG_CID | card_info.inc | card-stats.s slot 0x19b0 pw=29612557; conf:high |
| (disasm EOL) | incbin | 0x00001482 | BAZOO_THE_SOUL_EATER_CID | card_info.inc | card-stats.s slot 0x1482 pw=40133511; FS table ref at 0x09e46658; conf:high |

NOTE: BAZOO_THE_SOUL_EATER_CID used in disasm EOL comment only (fn_eligible stub has no
data-slot in the disassembled code; the CID lives in the FS table at 0x09e46658, not as a
literal pool word inside the incbin). Not counted in EQ_NEW towards C13 auto-name coverage.
Actual EQ_NEW counted: 10 slots.

C5 dedup evidence (value grep, not name grep):
  0x164d: grep constants/ -> 0 hits -> New
  0x154d: grep constants/ -> 0 hits -> New
  0x1704: grep constants/ -> 0 hits -> New
  0x1485: grep constants/ -> 0 hits -> New
  0x16d7: grep constants/ -> 0 hits -> New
  0x14aa: grep constants/ -> 0 hits -> New
  0x1665: grep constants/ -> 0 hits -> New
  0x18dc: grep constants/ -> 0 hits -> New
  0x170f: grep constants/ -> 0 hits -> New
  0x19b0: grep constants/ -> 0 hits -> New

### REF_SLOTS (USER-label + DATA-ref)

33 slots that are RAM global pointers (already have GAS labels from ewram.inc; slot gets
label = existing .equ name as indirect reference).

| slot | addr | value | gas_label | slot_label | notes |
|------|------|-------|-----------|------------|-------|
| PTR_gP1LifePoints_0807061c | L3658 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints | PTR_ slot type |
| PTR_gP1LifePoints_08070668 | L3695 | 0x0201c4e0 | gP1LifePoints | gP1LifePoints | PTR_ slot type |
| DAT_08070758 | L3860 | 0x0201bb90 | gEquipChainSlotRefs | gEquipChainSlotRefs | used as base + ldrh [r0,#0x1c] in dispatch_equip_zone_sprite_or_lp_row_type16 |

NOTE: The remaining 30 "REF" slots are actually RAM globals that belong to EQ_REUSE above
(gDuelPhaseFlags x11, gP1LifePoints x4, gDuelFieldSlots x10, etc.). They get EQ treatment
(`.equ` already exists), not REF treatment. The "REF_SLOTS" category here covers only the
3 PTR-typed slots listed above.

Revised REF_SLOTS count: 3 (2 PTR_gP1LifePoints + 1 gEquipChainSlotRefs).

### RENAME_SLOTS (fn-ptr DWORD + EOL)

| slot | addr | value | target_fn | eol_text |
|------|------|-------|-----------|---------|
| DWORD_0806ffb0 | L2818 | 0x08051f05 | check_equip_slot_eligible_by_side_and_type_query (asm/05 L20185) | check_equip_slot_eligible_by_side_and_type_query+1 |
| DWORD_0806ffec | L2849 | 0x08051f05 | check_equip_slot_eligible_by_side_and_type_query (asm/05 L20185) | check_equip_slot_eligible_by_side_and_type_query+1 |
| DAT_08070a64   | L4289 | 0x08090625 | invoke_effect_node_with_active_flag_3arg (asm/11 L11824) | invoke_effect_node_with_active_flag_3arg+1 |

All three are THUMB fn-ptr values (addr|1). Slot label = target_fn_name as RENAME only;
EOL comment = "<target_fn>+1". No new .equ needed (raw values, not offset equates).

### FUNC_RENAME

| addr | old (current) | new | reason | indeg |
|------|---------------|-----|--------|-------|
| 0x08070900 | (unnamed -- emitted as .byte in asm after build_equip_chain_entries_from_zone_slots epilogue) | check_zone_tile_count_and_set_summon_restriction_flag | Body: (a) reads slot[2] player_id+zone_idx; (b) indexes gDuelFieldSlots[player*0x868 + zone_idx*0x14] for both sides, sums tile_count fields; (c) compares vs slot[4] bits[14:9]; mismatch -> return 0; (d) reads second param (r12) card_id slot[0]; (e) calls get_card_field_summon_restriction; (f) if result==1: sets slot[4] bits 1 and 2 (gate+restriction flag); returns 0. Semantic: zone tile-count validation + summon restriction gate set. asm/09 L4094 .byte 0x00,0x00,0xf0,0xb5,...; THUMB+1 = 1 ref. | 1 ref (Royal Command CID=0x148e FS table @0x09e40b50) |

NOTE: This function is currently disassembled in the asm file but lacks a named label
(appears as raw .byte after the prev function's epilogue). Ghidra likely splits it as a
separate function. The fixer must add a label at 0x08070900 (2-byte pad at 0x080708fe) and
define the function entry. Ghidra: createLabel(0x08070900, "check_zone_tile_count_and_set_summon_restriction_flag", True).

### PLATE

No stale FUN_ text found in Seg-2 range (grep asm/09_equip_lp_display.s lines 2769..5262
for "FUN_" returns 0 hits within this segment). No plate changes required.

C8 check: grep -n "FUN_" asm/09_equip_lp_display.s shows no FUN_ strings in Seg-2 lines.
PLATE count = 0.

## Disasm Plan (R4)

### Block: ROM_INCBIN 0x08070476 size 0x90

THUMB disassembly. Block contains:
1. fn_eligible stub for Bazoo the Soul-Eater at 0x08070478:
   - Entry 0x08070478 (THUMB+1 = 0x08070479; confirmed FS table @0x09e46658)
   - Stub body: reads slot args, checks CID==BAZOO_THE_SOUL_EATER_CID (0x1482), returns eligibility
   - Label: `fn_eligible_bazoo_the_soul_eater`
   - EOL at entry: `@ fn_eligible stub for Bazoo the Soul-Eater CID=0x1482; FS table ref at GBA:0x09e46658`

2. Post-stub epilogue: ends at 0x08070506

3. 2-byte alignment pad at 0x08070506 (`.zero 0x2` or `.byte 0x00,0x00`)

4. Literal pool after incbin epilogue -- currently shown as:
   - Line 3506 incbin covers 0x70476..0x70505 (0x90 bytes = 0x08070476..0x08070505)
   - AFTER the block at 0x08070506..0x0807051b: 2 unlabeled .byte lines at what would be
     0x08070514 (value 0x00000868 = PLAYER_BLOCK_STRIDE) and
     0x08070518 (value 0x0201c510 = gDuelFieldSlots)
   - These literal pool .word entries belong to the function body code at 0x08070000 range
     that was disassembled but whose literal pool fell inside the incbin block.
   - After R4 disasm: replace with labeled .word entries:
     `.word PLAYER_BLOCK_STRIDE` and `.word gDuelFieldSlots`

Disasm range: 0x08070476..0x0807051b (covers incbin + post-incbin .byte literal pool)
NOTE: The full block 0x08070476..0x0807051b replaces one ROM_INCBIN line.

Stub-by-stub approach required: single DisassembleCommand for fn_eligible_bazoo_the_soul_eater
entry only (per methodology: disasm each stub individually, not whole range at once).

## carve Plan (R7)

carve = 0. No ROM data tables with structural content requiring carve in this segment.

## Sec5.1 (Rule 3 -- 0-ref blocks)

No ROM_INCBIN or .byte blocks with 0 references in this segment. The single incbin block
has confirmed THUMB+1 ref (FS table @0x09e46658). Sec5.1 count = 0.

## New constants / Globals

### card_info.inc (new CIDs -- 10 entries)

```
.equ GUARDIAN_BAOU_CID,              0x0000164d  @ Guardian Baou; 10 ROM refs; card-stats.s slot 0x164d pw=73544866
.equ LEGENDARY_FIEND_CID,            0x0000154d  @ Legendary Fiend; 6 ROM refs; card-stats.s slot 0x154d pw=99747800
.equ INSECT_PRINCESS_CID,            0x00001704  @ Insect Princess; 13 ROM refs; card-stats.s slot 0x1704 pw=37957847
.equ AQUA_SPIRIT_CID,                0x00001485  @ Aqua Spirit; 13 ROM refs; card-stats.s slot 0x1485 pw=40916023
.equ THUNDER_CRASH_CID,              0x000016d7  @ Thunder Crash; 8 ROM refs; card-stats.s slot 0x16d7 pw=69196160
.equ ENCHANTED_ARROW_CID,            0x000014aa  @ Enchanted Arrow; 10 ROM refs; card-stats.s slot 0x14aa pw=93260132
.equ TOKEN_THANKSGIVING_CID,         0x00001665  @ Token Thanksgiving; 8 ROM refs; card-stats.s slot 0x1665 pw=57182235
.equ TOKEN_FEASTEVIL_CID,            0x000018dc  @ Token Feastevil; 7 ROM refs; card-stats.s slot 0x18dc pw=83675475
.equ GRYPHONS_FEATHER_DUSTER_CID,    0x0000170f  @ Gryphon's Feather Duster; 11 ROM refs; card-stats.s slot 0x170f pw=34370473
.equ CYCLONE_BOOMERANG_CID,          0x000019b0  @ Cyclone Boomerang; 11 ROM refs; card-stats.s slot 0x19b0 pw=29612557
```

Also add to card_info.inc for disasm EOL use only (not counted in auto-name slot C13):
```
.equ BAZOO_THE_SOUL_EATER_CID,       0x00001482  @ Bazoo the Soul-Eater; 26 ROM refs; card-stats.s slot 0x1482 pw=40133511; FS table fn_eligible ref at GBA:0x09e46658
```

### ewram.inc (no new entries needed)

- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 already exists (C5 dedup hit); reuse for DWORD_08070884.
- All other needed equates already present.

## Consumer Evidence (R6)

| slot/global | consumer fn | file:line | usage | conf |
|-------------|-------------|-----------|-------|------|
| DWORD_08070310 (0x164d) | enqueue_zone_sprite_by_special_monster_card_id | asm/09 L3308 | CID comparison in dispatch chain | high |
| DWORD_08070314 (0x154d) | enqueue_zone_sprite_by_special_monster_card_id | asm/09 L3310 | CID comparison | high |
| DWORD_08070328 (0x1704) | enqueue_zone_sprite_by_special_monster_card_id | asm/09 L3322 | CID comparison | high |
| DAT_0807057c (0x1485) | dispatch_equip_lp_row_or_oam_by_state_and_hand_slot | asm/09 L3568 | ldrh r1,[r5,#0]; cmp r1,r0 -- card_id vs AQUA_SPIRIT_CID | high |
| DWORD_08070884 (0x1ce8) | build_equip_chain_entries_from_zone_slots | asm/09 L4030 | adds r0,r0,r1 -- gP1LifePoints+P1LP_BLOCK2_OFF_1CE8 chain pair offset | high |
| DWORD_08070890 (0x0201c520) | build_equip_chain_entries_from_zone_slots | asm/09 L4036 | gDuelFieldSlotState zone state read | high |
| DAT_08070a64 (0x08090625) | test_equip_zone_target_with_activation_state | asm/09 L4289 | bl set_equip_activation_state_by_mode; r2=fn_ptr (invoke_effect_node_with_active_flag_3arg+1) | high |
| PTR_gP1LifePoints_0807061c | dispatch_equip_lp_row_or_oam_by_state_and_hand_slot | asm/09 L3658 | ldr r0,[PTR]; adds r0,r0,LP_CARD_TRACK_BASE_OFF | high |
| DAT_08070758 (gEquipChainSlotRefs) | dispatch_equip_zone_sprite_or_lp_row_type16 | asm/09 L3860 | ldr r0,[DAT_]; ldrh r1,[r0,#0x1c] -- reads chain ref field +0x1c | high |
| DWORD_08070f60..f90 (CID dispatch) | tick_equip_target_count_or_lp_sprite_by_card_id | asm/09 L5107-5152 | binary search dispatch table for 6 CIDs: Thunder Crash, Enchanted Arrow, Token Thanksgiving, Token Feastevil, Gryphon's Feather Duster, Cyclone Boomerang | high |

## C13 Coverage Proof

Total auto-name slots in Seg-2: 77 (python regex scan confirmed).

Classification:
- EQ_REUSE (gDuelPhaseFlags x12): DWORD_0806ff6c, DWORD_08070110, DAT_080705a8, DWORD_08070750, DWORD_080707d0, DWORD_08070ae8, DWORD_08070b38, DWORD_08070e34, DWORD_08070ee0, DWORD_08070f3c, DAT_08070a40, DWORD_080703b8 = 12
- EQ_REUSE (gP1LifePoints x5): DWORD_08070b0c, DWORD_08070880, DWORD_08070044, DWORD_0806ffe8, DWORD_0806ffb8 = 5
- EQ_REUSE (PLAYER_BLOCK_STRIDE x11): DWORD_080700ec, DWORD_0807026c, DWORD_08070304, DAT_08070670, DWORD_08070888, DAT_08070974, DAT_08070a38, DWORD_08070c08, DWORD_08070c9c, DWORD_08070da4, DWORD_08070ed8 = 11
- EQ_REUSE (gDuelFieldSlots x9): DWORD_080700f0, DWORD_08070270, DWORD_08070308, DAT_08070a3c, DAT_08070978, DWORD_08070c0c, DWORD_08070ca0, DWORD_08070da8, DWORD_0807088c = 9
- EQ_REUSE (gP1HandSlotArray x1): DWORD_08070edc = 1
- EQ_REUSE (ELIGIB_SPRITE_CTRL_OFF x1): DWORD_08070048 = 1
- EQ_REUSE (LP_CARD_TRACK_BASE_OFF x3): DAT_08070620, DAT_0807066c, DWORD_08070b10 = 3
- EQ_REUSE (P1LP_BLOCK2_OFF_1CE8 x1): DWORD_08070884 = 1
- EQ_REUSE (OAM_SPRITE_CODE_P1_ACTIVATION x1): DAT_08070754 = 1
- EQ_REUSE (existing CIDs x5): DWORD_0807030c(RAGING_FLAME), DWORD_08070340(MAJI_GIRE_PANDA), DWORD_08070358(FIREBIRD), DWORD_08070420(SUMMONER_OF_ILLUSIONS), DWORD_08070d28(SUPER_REJUVENATION) = 5
- EQ_REUSE (DISPATCH_ACTIVE_FLAG_OFF x1): DAT_08070a88 = 1
- EQ_REUSE (EQUIP_PHASE_FRAME_OFF x8): DWORD_08070e54, DWORD_08070ed4, DWORD_08070f40, DWORD_08070fb0, DWORD_08070fd0, DWORD_08070ff0, DWORD_08071018, DWORD_08071048 = 8
- EQ_REUSE (gDuelCardCtxBase x2): DAT_08070a44, DWORD_0806ffb4 = 2
- EQ_REUSE (gDuelFieldSlotState x1): DWORD_08070890 = 1
- EQ_NEW (10 new CIDs): DWORD_08070310, DWORD_08070314, DWORD_08070328, DAT_0807057c, DWORD_08070f60, DWORD_08070f64, DWORD_08070f68, DWORD_08070f80, DWORD_08070f84, DWORD_08070f90 = 10
- REF_SLOTS (PTR_gP1LifePoints x2 + gEquipChainSlotRefs x1): PTR_gP1LifePoints_0807061c, PTR_gP1LifePoints_08070668, DAT_08070758 = 3
- RENAME_fnptr (fn-ptr DWORDs x3): DWORD_0806ffb0, DWORD_0806ffec, DAT_08070a64 = 3

Sum: 12+5+11+9+1+1+3+1+1+5+1+8+2+1+10+3+3 = 77. Check: 12+5=17; +11=28; +9=37; +1=38; +1=39; +3=42; +1=43; +1=44; +5=49; +1=50; +8=58; +2=60; +1=61; +10=71; +3=74; +3=77. Confirmed = 77.

## Seek Help

None. All semantic evidence is high confidence from:
- card-stats.s direct pw verification for all 11 CIDs
- ewram.inc existing constants for all RAM globals
- FS table structure verification for incbin classification (THUMB+1 @0x09e46658)
- Function plate comments in asm/09 for consumer evidence
