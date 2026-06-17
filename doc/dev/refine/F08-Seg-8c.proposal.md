# Refine Proposal: F08-Seg-8c  [0x0806c0cc..0x0806cbe8)

## Seg-8c Survey

### Function entries (10 fn)

| Address    | Name                                           | Prologue                    |
|------------|------------------------------------------------|-----------------------------|
| 0x0806c0cc | dispatch_neo_daedalus_placement_check_by_state | push {r4,r5,r6,r7,lr}      |
| 0x0806c204 | enqueue_equip_zone_sprite_chain_if_slot_matches| push {r4,r5,r6,r7,lr}      |
| 0x0806c368 | enqueue_paired_zone_sprite_if_slot_matches     | push {r4,r5,r6,r7,lr}      |
| 0x0806c6d8 | enqueue_equip_card_zone_sprites_at_free_slot   | push {r4,r5,r6,r7,lr}      |
| 0x0806c764 | set_opponent_state_bit0_from_node              | push {lr}                   |
| 0x0806c780 | enqueue_graveyard_spell_sprite_from_hand       | push {r4,r5,r6,lr}         |
| 0x0806c808 | enqueue_deck_eligible_sprite_type10_from_node  | push {lr}                   |
| 0x0806c828 | tick_equip_effect_node_display_state_machine   | push {r4,r5,r6,r7,lr}      |
| 0x0806c978 | dispatch_special_card_zone_sprite_by_type_and_state | push {r4,r5,r6,r7,lr} |
| 0x0806cb54 | enqueue_spirit_monster_zone_sprite_otohime     | push {r4,r5,lr}             |

Note: tick_equip_target_query_display_seq at 0x0806cbe8 is first function of Seg-9 (boundary exclusive).

### Residual auto-name slots (39 total, all in [0x0806c10c, 0x0806cbe4])

| Slot                           | Address     | Value       |
|-------------------------------|-------------|-------------|
| DWORD_0806c10c                 | 0x0806c10c  | 0x0201b290  |
| DWORD_0806c110                 | 0x0806c110  | 0x000004a4  |
| DWORD_0806c1ac                 | 0x0806c1ac  | 0x00000868  |
| DWORD_0806c1b0                 | 0x0806c1b0  | 0x0201c8f8  |
| DWORD_0806c1b4                 | 0x0806c1b4  | 0x0000133b  |
| DWORD_0806c35c                 | 0x0806c35c  | 0x00000868  |
| DWORD_0806c360                 | 0x0806c360  | 0x0201c510  |
| DWORD_0806c364                 | 0x0806c364  | 0x00008052  |
| DWORD_0806c3d0                 | 0x0806c3d0  | 0x00000868  |
| DWORD_0806c3d4                 | 0x0806c3d4  | 0x0201c510  |
| DWORD_0806c738                 | 0x0806c738  | 0x0201bb90  |
| DWORD_0806c800                 | 0x0806c800  | 0x00000868  |
| DWORD_0806c804                 | 0x0806c804  | 0x0201c8f8  |
| DWORD_0806c858                 | 0x0806c858  | 0x0201b290  |
| DWORD_0806c8ec                 | 0x0806c8ec  | gP1LifePoints (already sym) |
| DWORD_0806c8f0                 | 0x0806c8f0  | 0x00000868  |
| DWORD_0806c918                 | 0x0806c918  | 0x0201e2a0  |
| DWORD_0806c91c                 | 0x0806c91c  | gP1LifePoints (already sym) |
| DWORD_0806c948                 | 0x0806c948  | gP1LifePoints (already sym) |
| DWORD_0806c970                 | 0x0806c970  | gP1LifePoints (already sym) |
| DWORD_0806c974                 | 0x0806c974  | 0x00001da8  |
| DWORD_0806c9e4                 | 0x0806c9e4  | 0x00000868  |
| DWORD_0806c9e8                 | 0x0806c9e8  | 0x0201c510  |
| DWORD_0806c9ec                 | 0x0806c9ec  | 0x0201b290  |
| DWORD_0806ca5c                 | 0x0806ca5c  | 0x00001881  |
| DWORD_0806ca68                 | 0x0806ca68  | 0x000019d7  |
| DWORD_0806cac4                 | 0x0806cac4  | 0x000017b7  |
| DWORD_0806cac8                 | 0x0806cac8  | 0x0000137d  |
| DWORD_0806cad0                 | 0x0806cad0  | 0x000015e6  |
| DWORD_0806caec                 | 0x0806caec  | 0x000019d7  |
| DWORD_0806cb14                 | 0x0806cb14  | 0x0201e4d0  |
| DWORD_0806cb40                 | 0x0806cb40  | 0x0201e4d0  |
| DAT_0806cb6c                   | 0x0806cb6c  | 0x0000137e  |
| DAT_0806cb70                   | 0x0806cb70  | 0x000014fd  |
| PTR_gP1LifePoints_0806cb98     | 0x0806cb98  | gP1LifePoints (already sym) |
| DAT_0806cb9c                   | 0x0806cb9c  | 0x00001ce8  |
| DAT_0806cba0                   | 0x0806cba0  | 0x00001cf4  |
| PTR_gP1LifePoints_0806cbe0     | 0x0806cbe0  | gP1LifePoints (already sym) |
| DAT_0806cbe4                   | 0x0806cbe4  | 0x00001ce8  |

Python ROM byte-verify (all confirmed correct; values match asm `.word` lines).

### ROM_INCBIN / .byte blocks in Seg-8c

| Block            | Size  | Address range                |
|-----------------|-------|------------------------------|
| ROM_INCBIN 0x6c3d8 | 0x44 B | 0x0806c3d8..0x0806c41b     |
| ROM_INCBIN 0x6c440 | 0x298 B | 0x0806c440..0x0806c6d7    |

Note: the 9-entry jump table at 0x0806c41c..0x0806c43c is ALREADY structured as `.word` entries in the asm file (between the two ROM_INCBINs). It does NOT need carving.

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

### ref-scan

Python command run:
```python
import struct; d=open("roms/2343.gba","rb").read()
for a in [0x0806c3d8, 0x0806c440]:
    for v in (a, a|1):
        print(hex(v), d.count(struct.pack("<I", v)))
```

Results:
- 0x0806c3d8 raw=0, 0x0806c3d9 THUMB+1=1  (hit at 0x9e43760)
- 0x0806c440 raw=1, 0x0806c441 THUMB+1=0  (hit at 0x0806c43c)

| Block      | sz    | ref-scan (raw / THUMB+1) | Judgment | Rationale |
|-----------|-------|--------------------------|----------|-----------|
| 0x6c3d8   | 0x44  | raw=0 THUMB+1=1          | DISASM R4 | THUMB+1 ref at 0x9e43760 (card effect fn_eligible dispatch table); CID=0x1369 at dispatch_entry[fn_eligible_ptr-4]=0x9e4375c; python verify ROM[0x9e4375c]=0x00001369; card-stats.s card_0774 slot=0x1369 Morphing Jar #2 pw=79106360. Block starts 0xb5f0 (push{r4..r7,lr}), confirmed THUMB code. |
| 0x6c440   | 0x298 | raw=1 THUMB+1=0          | DISASM R4 | raw ref at 0x0806c43c (.word 0x0806c440 = entry[8] of 9-entry jump table at 0x0806c41c..0x0806c43c). Jump table body is already structured in asm. Block begins 0x2000 (movs r0,#0), confirmed THUMB code. 8 unique stub entry points within block. |

THUMB+1 hit for 0x6c3d8 context check:
- hit addr 0x9e43760, surrounding bytes: `5d 63 05 08 00 00 00 00 69 13 00 00 d9 c3 06 08 00 00 00 00`
- entry layout: [fn_activate+1=0x0805635d, pad=0, CID=0x1369, fn_eligible+1=0x0806c3d9, pad=0]
- CID is at fn_eligible_ptr - 4 (not -0xc; this dispatch table uses 5-word entry without fn_activate field in standard position)
- CID = 0x1369 = Morphing Jar #2 confirmed (card-stats.s card_0774)

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

| Slot                  | Value       | const_name              | Source        | New slot label                        |
|-----------------------|-------------|-------------------------|---------------|---------------------------------------|
| DWORD_0806c10c        | 0x0201b290  | gDuelPhaseFlags         | reuse ewram.inc L351 | gduelphaseflags_0806c10c         |
| DWORD_0806c110        | 0x000004a4  | EQUIP_PHASE_FRAME_OFF   | reuse ewram.inc L434 | equip_phase_frame_off_0806c110   |
| DWORD_0806c1ac        | 0x00000868  | PLAYER_BLOCK_STRIDE     | reuse ewram.inc L250 | player_block_stride_0806c1ac     |
| DWORD_0806c1b0        | 0x0201c8f8  | gP1HandSlotArray        | reuse ewram.inc L332 | gp1handslotarray_0806c1b0        |
| DWORD_0806c1b4        | 0x0000133b  | SPEAR_CRETIN_CID        | reuse card_info.inc L796 | spear_cretin_cid_0806c1b4    |
| DWORD_0806c35c        | 0x00000868  | PLAYER_BLOCK_STRIDE     | reuse         | player_block_stride_0806c35c     |
| DWORD_0806c360        | 0x0201c510  | gDuelFieldSlots         | reuse ewram.inc L312 | gduelfieldslots_0806c360         |
| DWORD_0806c364        | 0x00008052  | OAM_EQUIP_ZONE_CHAIN_SPRITE_P2 | NEW oam_attr.inc | oam_equip_zone_chain_sprite_p2_0806c364 |
| DWORD_0806c3d0        | 0x00000868  | PLAYER_BLOCK_STRIDE     | reuse         | player_block_stride_0806c3d0     |
| DWORD_0806c3d4        | 0x0201c510  | gDuelFieldSlots         | reuse         | gduelfieldslots_0806c3d4         |
| DWORD_0806c738        | 0x0201bb90  | gEquipChainSlotRefs     | reuse ewram.inc L315 | gequipchainslot_refs_0806c738    |
| DWORD_0806c800        | 0x00000868  | PLAYER_BLOCK_STRIDE     | reuse         | player_block_stride_0806c800     |
| DWORD_0806c804        | 0x0201c8f8  | gP1HandSlotArray        | reuse         | gp1handslotarray_0806c804        |
| DWORD_0806c858        | 0x0201b290  | gDuelPhaseFlags         | reuse         | gduelphaseflags_0806c858         |
| DWORD_0806c8ec        | gP1LifePoints | gP1LifePoints          | already sym   | gp1lifepoints_0806c8ec           |
| DWORD_0806c8f0        | 0x00000868  | PLAYER_BLOCK_STRIDE     | reuse         | player_block_stride_0806c8f0     |
| DWORD_0806c918        | 0x0201e2a0  | gDuelCardCtxBase        | reuse ewram.inc L218 | gduelcardctxbase_0806c918        |
| DWORD_0806c91c        | gP1LifePoints | gP1LifePoints          | already sym   | gp1lifepoints_0806c91c           |
| DWORD_0806c948        | gP1LifePoints | gP1LifePoints          | already sym   | gp1lifepoints_0806c948           |
| DWORD_0806c970        | gP1LifePoints | gP1LifePoints          | already sym   | gp1lifepoints_0806c970           |
| DWORD_0806c974        | 0x00001da8  | LP_CARD_TRACK_BASE_OFF  | reuse ewram.inc L247 | lp_card_track_base_off_0806c974  |
| DWORD_0806c9e4        | 0x00000868  | PLAYER_BLOCK_STRIDE     | reuse         | player_block_stride_0806c9e4     |
| DWORD_0806c9e8        | 0x0201c510  | gDuelFieldSlots         | reuse         | gduelfieldslots_0806c9e8         |
| DWORD_0806c9ec        | 0x0201b290  | gDuelPhaseFlags         | reuse         | gduelphaseflags_0806c9ec         |
| DWORD_0806ca5c        | 0x00001881  | RE_FUSION_CID           | reuse card_info.inc L575 | re_fusion_cid_0806ca5c       |
| DWORD_0806ca68        | 0x000019d7  | SYMBOL_OF_HERITAGE_CID  | reuse card_info.inc L576 | symbol_of_heritage_cid_0806ca68  |
| DWORD_0806cac4        | 0x000017b7  | SOUL_RESURRECTION_CID   | reuse card_info.inc L580 | soul_resurrection_cid_0806cac4   |
| DWORD_0806cac8        | 0x0000137d  | CALL_OF_THE_HAUNTED_CID | reuse card_info.inc L567 | call_of_the_haunted_cid_0806cac8 |
| DWORD_0806cad0        | 0x000015e6  | AUTONOMOUS_ACTION_UNIT_CID | reuse card_info.inc L566 | autonomous_action_unit_cid_0806cad0 |
| DWORD_0806caec        | 0x000019d7  | SYMBOL_OF_HERITAGE_CID  | reuse (dup)   | symbol_of_heritage_cid_0806caec  |
| DWORD_0806cb14        | 0x0201e4d0  | gEquipZoneRankState     | reuse ewram.inc L437 | gequipzonerankstate_0806cb14     |
| DWORD_0806cb40        | 0x0201e4d0  | gEquipZoneRankState     | reuse (dup)   | gequipzonerankstate_0806cb40     |
| DAT_0806cb6c          | 0x0000137e  | SOLOMONS_LAWBOOK_CID    | NEW card_info.inc | solomons_lawbook_cid_0806cb6c  |
| DAT_0806cb70          | 0x000014fd  | MAHARAGHI_CID           | reuse card_info.inc L1016 | maharaghi_cid_0806cb70       |
| PTR_gP1LifePoints_0806cb98 | gP1LifePoints | gP1LifePoints    | already sym (RENAME slot) | gp1lifepoints_0806cb98    |
| DAT_0806cb9c          | 0x00001ce8  | P1LP_BLOCK2_OFF_1CE8    | reuse ewram.inc L275 | p1lp_block2_off_0806cb9c         |
| DAT_0806cba0          | 0x00001cf4  | P2LP_BLOCK2_OFF_1CF4    | NEW ewram.inc | p2lp_block2_off_0806cba0         |
| PTR_gP1LifePoints_0806cbe0 | gP1LifePoints | gP1LifePoints    | already sym (RENAME slot) | gp1lifepoints_0806cbe0    |
| DAT_0806cbe4          | 0x00001ce8  | P1LP_BLOCK2_OFF_1CE8    | reuse (dup)   | p1lp_block2_off_0806cbe4         |

Total EQ slots: 39 (34 reuse + 3 NEW: OAM_EQUIP_ZONE_CHAIN_SPRITE_P2 / SOLOMONS_LAWBOOK_CID / P2LP_BLOCK2_OFF_1CF4 + 2 RENAME for PTR_gP1LifePoints already-sym)

C5 double-check (NEW constants):
- OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052: grep oam_attr.inc "0x8052" => 0 hits; grep oam_attr.inc "0x00008052" => 0 hits. Confirmed NEW. (raw refs in ROM = 4: 0x806c364, 0x80a2328, 0x80a2450, 0x80a268c).
- SOLOMONS_LAWBOOK_CID=0x137e: grep card_info.inc "0x137e" => 0 hits; grep card_info.inc "0x0000137e" => 0 hits. Confirmed NEW. card-stats.s card_0794 slot=0x137E pw=23471572.
- P2LP_BLOCK2_OFF_1CF4=0x1cf4: grep ewram.inc "0x1cf4" => 1 hit (gP1FieldState comment notes "+FIELD_STATE_OFF(0x1cf4)" but as gP1LifePoints base). grep ewram.inc ".equ.*0x00001cf4" => 0 hits. duel_field.inc has FIELD_STATE_OFF=0x1cf4 (base=gDuelFieldSlots, different base); per C5 relaxed-dedup rule (different base = independent constant). Confirmed NEW. (raw refs in ROM = 103; asm/03 x1 + asm/07 x6 + asm/08 x2 = 9 structured uses).

C5 double-check (REUSE):
- SPEAR_CRETIN_CID=0x133b: grep card_info.inc "0x133b" => 1 hit L796 SPEAR_CRETIN_CID. Confirmed reuse.
- RE_FUSION_CID=0x1881: grep card_info.inc "0x1881" => 1 hit L575 RE_FUSION_CID. Confirmed reuse.
- SYMBOL_OF_HERITAGE_CID=0x19d7: grep card_info.inc "0x19d7" => 1 hit L576 SYMBOL_OF_HERITAGE_CID. Confirmed reuse.
- SOUL_RESURRECTION_CID=0x17b7: grep card_info.inc "0x17b7" => 1 hit L580 SOUL_RESURRECTION_CID. Confirmed reuse.
- CALL_OF_THE_HAUNTED_CID=0x137d: grep card_info.inc "0x137d" => 1 hit L567 CALL_OF_THE_HAUNTED_CID. Confirmed reuse.
- AUTONOMOUS_ACTION_UNIT_CID=0x15e6: grep card_info.inc "0x15e6" => 1 hit L566 AUTONOMOUS_ACTION_UNIT_CID. Confirmed reuse.
- MAHARAGHI_CID=0x14fd: grep card_info.inc "0x14fd" => 1 hit L1016 MAHARAGHI_CID. Confirmed reuse.
- gEquipZoneRankState=0x0201e4d0: grep ewram.inc "0x0201e4d0" => 1 hit L437 gEquipZoneRankState. Confirmed reuse.
- gEquipChainSlotRefs=0x0201bb90: grep ewram.inc "0x0201bb90" => 1 hit L315. Confirmed reuse.
- gP1HandSlotArray=0x0201c8f8: grep ewram.inc "0x0201c8f8" => 1 hit L332. Confirmed reuse.

Additionally needed -- MORPHING_JAR_2_CID=0x1369 for the fn_eligible block label (not a slot in named fns, but needed to name the disasm'd function):
- grep card_info.inc "0x1369" => 0 hits; grep card_info.inc "MORPHING_JAR_2" => 0 hits. Confirmed NEW.
- card-stats.s card_0774 slot=0x1369 pw=79106360 Morphing Jar #2.

### REF_SLOTS (USER-label + DATA-ref)

None in Seg-8c. The two PTR_gP1LifePoints slots are handled as EQ (already symbolized, just need label rename).

### RENAME_SLOTS (PTR_ label rename)

| Slot                           | Current label                  | New label             | EOL |
|-------------------------------|-------------------------------|-----------------------|-----|
| PTR_gP1LifePoints_0806cb98     | PTR_gP1LifePoints_0806cb98     | gp1lifepoints_0806cb98 | none |
| PTR_gP1LifePoints_0806cbe0     | PTR_gP1LifePoints_0806cbe0     | gp1lifepoints_0806cbe0 | none |

### FUNC_RENAME (misname correction)

#### 1. dispatch_neo_daedalus_placement_check_by_state @ 0x0806c0cc

Evidence (high confidence):
- DWORD_0806c1b4 = 0x133b = SPEAR_CRETIN_CID (card-stats.s slot=0x133b; already in card_info.inc L796)
- Function body compares card_id slot [r6+0] against 0x133b (Spear Cretin) at line 18313 of asm/08
- Function is Spear Cretin's state machine (state 0x80/7f/7e) for placement check
- The name "neo_daedalus" references the callee check_field_spell_neo_daedalus_group_placeable, NOT this function's card
- Plate comment says "Card constant Spear Cretin (0x133b)" -- plate already knows the correct card
- indeg=1 (only bl caller: dispatch_spear_cretin_activate_if_chain_subtype @ 0x0806b54c, asm/08 L16662)
- No other callers found (grep confirms single bl)

Old name: dispatch_neo_daedalus_placement_check_by_state
New name: tick_spear_cretin_placement_state_machine

PLATE: full rewrite (current plate says "Neo-Daedalus placement check three-step state machine function"):
```
Spear Cretin (CID=0x133b) placement state machine. Three-step state dispatch on gDuelPhaseFlags[+0x4a0]:
state=0x80: checks field spell Neo Daedalus group placeable and finds hand slot by set_code, returns 0x7f.
state=0x7f: checks zone slot equip eligibility, constructs target ptr, dispatches by card_id (0x133b vs 0x133b+0x2a),
  calls invoke_setup_equip_oam_with_attr2 or setup_equip_oam_entry_with_sprite_attr. Returns 0x7e.
state=0x7e: increments internal counter; when >1 returns 0x64. Returns 0x7e.
state=0x64: calls decrement_lp_bar_display_counter. Returns 0.
Called via bl by dispatch_spear_cretin_activate_if_chain_subtype (indeg=1).
Constants: gDuelPhaseFlags=0x0201b290, STATE_OFFSET=0x4a0, SPEAR_CRETIN_CID=0x133b,
PLAYER_BLOCK_STRIDE=0x868, gP1HandSlotArray=0x0201c8f8.
```

ripple checklist:
a. CSV sync: doc/dev/naming-proposals.csv -- update row for 0x0806c0cc: old=dispatch_neo_daedalus_placement_check_by_state -> new=tick_spear_cretin_placement_state_machine
b. Cross-module plate: grep asm/*.s for "dispatch_neo_daedalus_placement_check_by_state" -> found in asm/08 lines 16645/16650/16651 (plate/comments of dispatch_spear_cretin_activate_if_chain_subtype) -> these must be updated to new name after re-export.

### PLATE (R5)

| Function                                              | Type            | Content                                             |
|------------------------------------------------------|-----------------|-----------------------------------------------------|
| tick_spear_cretin_placement_state_machine (renamed)   | full rewrite    | see FUNC_RENAME above; old "Neo-Daedalus" -> Spear Cretin; all ASCII |
| enqueue_spirit_monster_zone_sprite_otohime @ 0x0806cb54 | substring replace | FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id |

Non-ASCII check: grep [^\x00-\x7F] over lines 18193..19346 of asm/08 = 0 hits. No CJK mojibake present.

Stale FUN_ in Seg-8c:
- asm/08 line 19255: `@ Called by FUN_08071d64 (spirit monster dispatcher)...` -> current name = dispatch_spirit_monster_zone_sprite_by_card_id (asm/09 L6819)

---

## carve plan (R7)

None. The 9-entry jump table at 0x0806c41c..0x0806c43c is already structured as `.word` entries in the asm file between the two ROM_INCBINs. No additional carving needed.

---

## disasm plan (R4)

### Block 0x6c3d8 (0x44 B = 68 bytes; fn_eligible handler for Morphing Jar #2)

Range: 0x0806c3d8..0x0806c41b (includes literal pool ending at 0x0806c41b, 4 bytes)

Structure:
- THUMB+1 ref at 0x9e43760 (dispatch table entry fn_eligible+1 for CID=0x1369)
- Block contains 1 function: the fn_eligible handler for Morphing Jar #2
- Internal literal pool at 0x0806c418 contains 0x0806c41c (jump table start pointer used in dispatch)
- Block dispatches internally to the 9-entry jump table at 0x0806c41c (already structured in asm)
- Block end: 0x0806c41b = 0x0806c3d8 + 0x44 - 1

Method: clearListing 0x0806c3d8..0x0806c41b -> setTMode -> DisassembleCommand(0x0806c3d8, 0x44)

New function label: check_equip_eligible_morphing_jar_2 @ 0x0806c3d8
- Naming rationale: fn_eligible handler for Morphing Jar #2 (CID=0x1369); follows pattern of check_equip_eligible_cid_135b / check_equip_eligible_magical_hats from Seg-8b
- Plate: "Morphing Jar #2 (CID=MORPHING_JAR_2_CID=0x1369) fn_eligible handler. Dispatches state by phase code via 9-entry jump table at 0x0806c41c. THUMB+1 ref at dispatch table 0x09e43760."

CSV sync: +1 row (check_equip_eligible_morphing_jar_2 @ 0x0806c3d8)

### Block 0x6c440 (0x298 B = 664 bytes; state machine stubs for Morphing Jar #2)

Range: 0x0806c440..0x0806c6d7

Structure:
- raw ref at 0x0806c43c (jump table entry[8] = 0x0806c440 = block start)
- 9-entry jump table at 0x0806c41c..0x0806c43c: 8 unique stub targets + 1 duplicate (entries[1,2] both -> 0x0806c6c0)
- 8 unique stub entry points:
  - entry[8] -> 0x0806c440  (default / state=0: movs r0,#0 -> init path)
  - entry[7] -> 0x0806c4e8
  - entry[6] -> 0x0806c52c
  - entry[5] -> 0x0806c5f8
  - entry[4] -> 0x0806c63c
  - entry[3] -> 0x0806c65a
  - entry[0] -> 0x0806c69c
  - entry[1]=entry[2] -> 0x0806c6c0  (shared stub)

Method: clearListing 0x0806c440..0x0806c6d7 -> setTMode -> DisassembleCommand per stub (8 stubs)

New function labels (naming pattern: morphing_jar2_state_stub_<hex_addr>):
| Entry | Address    | Label                          |
|-------|------------|-------------------------------|
| [8]   | 0x0806c440 | morphing_jar2_state_stub_c440  |
| [7]   | 0x0806c4e8 | morphing_jar2_state_stub_c4e8  |
| [6]   | 0x0806c52c | morphing_jar2_state_stub_c52c  |
| [5]   | 0x0806c5f8 | morphing_jar2_state_stub_c5f8  |
| [4]   | 0x0806c63c | morphing_jar2_state_stub_c63c  |
| [3]   | 0x0806c65a | morphing_jar2_state_stub_c65a  |
| [0]   | 0x0806c69c | morphing_jar2_state_stub_c69c  |
| [1,2] | 0x0806c6c0 | morphing_jar2_state_stub_c6c0  |

CSV sync: +8 rows (8 new disasm stub functions)

Literal pool handling: after disasm, any literal pool words within the block that appear as `.byte` sequences need DWORD label split (per Seg-8b FixF08Seg8bLiteralPools pattern). Fixer must run createDWord for any unresolved .byte pools in 0x0806c440..0x0806c6d7.

---

## New constants / globals (must verify no existing reuse first)

### card_info.inc

New entries (2):

```asm
.equ MORPHING_JAR_2_CID,             0x00001369  @ Morphing Jar #2 (pw=79106360; card-stats.s slot=0x1369 card_0774); fn_eligible handler check_equip_eligible_morphing_jar_2
.equ SOLOMONS_LAWBOOK_CID,           0x0000137e  @ Solomon's Lawbook (pw=23471572; card-stats.s slot=0x137e card_0794); enqueue_spirit_monster_zone_sprite_otohime Lawbook/Maharaghi special case
```

### oam_attr.inc

New entry (1):

```asm
.equ OAM_EQUIP_ZONE_CHAIN_SPRITE_P2, 0x00008052  @ equip zone chain sprite OAM attr0 P2 (bit15+0x52); enqueue_equip_zone_sprite_chain_if_slot_matches P1=0x52 inline, P2 via literal pool; 4 raw ROM refs (0x806c364, 0x80a2328, 0x80a2450, 0x80a268c)
```

### ewram.inc

New entry (1):

```asm
.equ P2LP_BLOCK2_OFF_1CF4,           0x00001cf4  @ [gP1LifePoints+0x1cf4] P2 LP display block2 field (opponent analog of P1LP_BLOCK2_OFF_1CE8=0x1ce8); enqueue_spirit_monster_zone_sprite_otohime opponent LP compare; distinct from FIELD_STATE_OFF=0x1cf4 (base=gDuelFieldSlots vs gP1LifePoints); 103 raw ROM refs
```

---

## Section 5.1 Registration (Rule 3) -- 0-reference blocks

None in Seg-8c. Both ROM_INCBIN blocks have confirmed references (THUMB+1 and raw respectively).

---

## Consumer evidence (R6)

| Slot / const               | Consumer file:line                                     | Confidence |
|---------------------------|-------------------------------------------------------|-----------|
| SPEAR_CRETIN_CID=0x133b    | asm/08 L18313 (DWORD_0806c1b4); dispatch table 0x9e436d0/0x9e45830 entries CID field (Seg-8a proposal verified) | high |
| MORPHING_JAR_2_CID=0x1369  | dispatch table 0x9e4375c CID field (python verify: ROM[0x9e4375c]=0x00001369); card-stats.s card_0774 | high |
| RE_FUSION_CID=0x1881       | asm/08 L19119 (DWORD_0806ca5c = 0x1881); function plate "Re-Fusion (0x1881)"; card-stats.s card_1177 | high |
| SYMBOL_OF_HERITAGE_CID=0x19d7 | asm/08 L19126/L19198 (DWORD_0806ca68/0806caec); plate; card-stats.s | high |
| SOUL_RESURRECTION_CID=0x17b7 | asm/08 L19175 (DWORD_0806cac4); plate; card-stats.s | high |
| CALL_OF_THE_HAUNTED_CID=0x137d | asm/08 L19177 (DWORD_0806cac8); plate; card-stats.s | high |
| AUTONOMOUS_ACTION_UNIT_CID=0x15e6 | asm/08 L19182 (DWORD_0806cad0); plate; card-stats.s | high |
| SOLOMONS_LAWBOOK_CID=0x137e | asm/08 L19274 (DAT_0806cb6c = 0x137e); plate "CARD_SOLOMONS_LAWBOOK=0x137e"; card-stats.s card_0794 | high |
| MAHARAGHI_CID=0x14fd       | asm/08 L19276 (DAT_0806cb70 = 0x14fd); plate "CARD_MAHARAGHI=0x14fd"; card-stats.s | high |
| P2LP_BLOCK2_OFF_1CF4=0x1cf4 | asm/08 L19300 (DAT_0806cba0 = 0x1cf4); plate "opponent_lp_offset=0x1cf4"; enqueue_spirit_monster_zone_sprite_otohime compares gP1LifePoints+0x1cf4 (opponent LP) against gP1LifePoints+0x1ce8 (P1 LP) | high |
| OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052 | asm/08 L18538 (DWORD_0806c364); plate "SPRITE_OBJ_0x8052=0x8052"; P2 path in enqueue_equip_zone_sprite_chain_if_slot_matches vs P1 inline 0x52 | high |
| gEquipZoneRankState=0x0201e4d0 | asm/08 L19218/L19241 (DWORD_0806cb14/cb40); dispatch_special_card_zone_sprite_by_type_and_state loads gEquipZoneRankState[+0] for zone count dispatch; ewram.inc L437 | high |
| gEquipChainSlotRefs=0x0201bb90 | asm/08 L18669 (DWORD_0806c738); enqueue_equip_card_zone_sprites_at_free_slot loads equip chain node data; ewram.inc L315 | high |

---

## Seek help

None -- all semantics have file:line + confidence level high evidence.

Dispatch table entry format note: CID offset in this dispatch table (0x9e43754 area) is fn_eligible_ptr - 4 (not -0xc). The -0xc rule applies to 6-word entries [CID, fn_activate+1, pad, fn_eligible+1, pad, pad]; here the entry is 5-word [fn_activate+1, pad, CID, fn_eligible+1, pad] (CID is 3rd field = fn_eligible_ptr - 4). CID=0x1369 confirmed regardless of offset formula.
