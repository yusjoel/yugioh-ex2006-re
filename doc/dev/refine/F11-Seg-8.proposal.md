# Refine Proposal: F11-Seg-8  [0x08090a78..0x08091888)

## Segment Survey

### Function Entries (3)
| Address    | Name                                   | Size (approx) |
|------------|----------------------------------------|---------------|
| 0x08090a78 | build_equip_candidate_score_table      | ~0xc48 B      |
| 0x080916c0 | invoke_build_equip_candidate_score_table | ~0xc B      |
| 0x080916cc | write_equip_target_score_entry         | ~0x1bc B      |

### Residual Auto-Name Slots: 73 total DAT_ labels
(All listed in EQ/REF tables below; seg7_pool_chainrefs_0af0 is pre-named, not counted.)

### ROM_INCBIN / .byte blocks: 0
Grep confirmed: zero `.ROM_INCBIN`, `.incbin`, or `.byte` code blocks in [0x08090a78, 0x08091888).
No hidden callback stubs found (unlike Seg-7).

---

## Data Block Classification (Rule 2/3)

No ROM_INCBIN or .byte blocks exist in Seg-8. All 73 residual labels are inline literal-pool
slots within named code functions; no standalone data block ref-scan needed.

Ref-scan run as a precaution for the 3 new address globals (see below):

| Address     | raw refs | THUMB+1 | Judgment        | Reason                                 |
|-------------|----------|---------|-----------------|----------------------------------------|
| 0x0201afe0  | 68       | 0       | REF global (new)| Wide EWRAM use; not function pointer   |
| 0x0201bc38  | 2        | 0       | REF global (new)| Sub-field of gEquipChainSlotRefs struct|
| 0x0201bc3c  | 2        | 0       | REF global (new)| Sub-field of gEquipChainSlotRefs struct|

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

Format: (slot_addr, value, const_name, disposition)

All ROM-verified (python struct.unpack_from, 0 mismatches on all 73 slots).

#### REUSE (36 slots -- existing constants, 0 new .equ needed)

| Slot addr  | Value      | Constant name                     | Source file        |
|------------|------------|-----------------------------------|--------------------|
| 0x08090cb0 | 0x00000868 | PLAYER_BLOCK_STRIDE               | ewram.inc          |
| 0x08090cb8 | -- REF --  | (gEquipChainSlotRefs - REF below) |                    |
| 0x08090cbc | 0x00001381 | MIRROR_WALL_CID                   | card_info.inc      |
| 0x08090cc0 | 0x00001905 | DARK_DREADROUTE_CID               | card_info.inc      |
| 0x08090cc4 | 0x00001951 | WATER_DRAGON_CID                  | card_info.inc      |
| 0x08090cc8 | 0x00001955 | CYBER_BLADER_CID                  | card_info.inc      |
| 0x08090ccc | 0x000014d7 | SPIRIT_RYU_CID                    | card_info.inc      |
| 0x08090cf8 | 0x00001643 | MIRAGE_KNIGHT_CID                 | card_info.inc      |
| 0x08090d04 | 0x00001956 | EHERO_RAMPART_BLASTER_CARD_ID     | card_info.inc      |
| 0x08090d24 | 0x00000bb8 | LP_COST_3000                      | card_info.inc      |
| 0x08090e50 | 0x00001846 | BALLISTA_OF_RAMPART_SMASHING_CID  | card_info.inc      |
| 0x08090e58 | 0x000005dc | LP_COST_1500                      | card_info.inc      |
| 0x08090e5c | 0x00000868 | PLAYER_BLOCK_STRIDE               | ewram.inc          |
| 0x08090e64 | 0x000013a7 | INJECTION_FAIRY_LILY_CID          | card_info.inc      |
| 0x08090e68 | 0x000014b0 | EQUIP_NODE_BASE_OFFSET            | card_info.inc      |
| 0x08090e6c | 0x00001119 | SANGA_OF_THUNDER_CID              | card_info.inc      |
| 0x08090ea8 | 0x00000bb8 | LP_COST_3000                      | card_info.inc      |
| 0x08091040 | 0x00001257 | REVERSE_TRAP_CID                  | card_info.inc      |
| 0x08091048 | 0x00001381 | MIRROR_WALL_CID                   | card_info.inc      |
| 0x0809104c | 0x00001905 | DARK_DREADROUTE_CID               | card_info.inc      |
| 0x08091050 | 0x00001951 | WATER_DRAGON_CID                  | card_info.inc      |
| 0x08091054 | 0x00001955 | CYBER_BLADER_CID                  | card_info.inc      |
| 0x08091058 | 0x00000868 | PLAYER_BLOCK_STRIDE               | ewram.inc          |
| 0x08091064 | 0x000013a7 | INJECTION_FAIRY_LILY_CID          | card_info.inc      |
| 0x08091078 | 0x00001643 | MIRAGE_KNIGHT_CID                 | card_info.inc      |
| 0x080910a8 | 0x00000bb8 | LP_COST_3000                      | card_info.inc      |
| 0x08091348 | 0xfffffe0c | LP_EQUIP_DELTA_NEG_500            | equip_lp_delta.inc |
| 0x08091350 | 0x00001853 | COVERING_FIRE_CID                 | card_info.inc      |
| 0x08091354 | 0x00001238 | METALMORPH_CID                    | card_info.inc      |
| 0x0809135c | 0x00000868 | PLAYER_BLOCK_STRIDE               | ewram.inc          |
| 0x08091368 | 0x0000159e | BUSTER_RANCHER_CID                | card_info.inc      |
| 0x080914f4 | 0x0000159e | BUSTER_RANCHER_CID                | card_info.inc      |
| 0x080916ac | 0x0000159e | BUSTER_RANCHER_CID                | card_info.inc      |
| 0x080916b4 | 0x00000513 | FIELD5_SCORE_THRESHOLD_1299       | card_info.inc      |
| 0x080916b8 | 0x0000150a | HEART_OF_CLEAR_WATER_CID          | card_info.inc      |
| 0x080917d4 | 0x00001639 | TOKEN_1639_CID                    | card_info.inc      |
| 0x080917d8 | 0x00000868 | PLAYER_BLOCK_STRIDE               | ewram.inc          |

C5 dedup evidence (REUSE): each constant value-grep in constants/*.inc returns >=1 hit as documented.

#### NEW (16 slots -- 8 unique new constants needed)

File: `constants/card_info.inc` (all 8 new equates).

| Slot addr(s)                               | Value      | Proposed .equ name              | Evidence                                                   |
|--------------------------------------------|------------|---------------------------------|------------------------------------------------------------|
| 0x08090cd0, 0x08090e80                     | 0x000013aa | KINETIC_SOLDIER_CID             | card-stats.s card_0827: Kinetic Soldier slot=0x13AA pw=79853073; grep 0x000013aa constants/*.inc = 0 hits; conf: high |
| 0x08090cdc, 0x08090e84, 0x08091060         | 0x000014cc | HUNTER_7_WEAPONS_CID            | card-stats.s card_1020: The Hunter with 7 Weapons slot=0x14CC pw=01525329; grep 0x000014cc = 0 hits; conf: high (3 occurrences) |
| 0x08090cf4, 0x0809107c                     | 0x000018f2 | STEAMROID_CID                   | card-stats.s card_1876: Steamroid slot=0x18F2 pw=44729197; grep 0x000018f2 = 0 hits; conf: high |
| 0x08091358                                 | 0x000018ff | SKYSCRAPER_CID                  | card-stats.s card_1888: Skyscraper slot=0x18FF pw=63035430; grep 0x000018ff = 0 hits; conf: high |
| 0x08091388, 0x080914ec, 0x08091520, 0x080916a4 | 0x000009c3 | EQUIP_ATK_SCORE_HI_2499    | Score gate: cmp score, 0x9c3; bgt proceed; 4 slots; grep 0x000009c3 constants/*.inc = 0 hits; equip ATK score threshold at 2499 (== 2500-1); conf: high |
| 0x080914f8, 0x080916b0                     | 0x000009c4 | EQUIP_ATK_SCORE_HI_2500         | Score gate: cmp score, 0x9c4; ble skip; complement of 2499; grep 0x000009c4 = 0 hits; conf: high |
| 0x080917d0                                 | 0x000014a4 | AMAZONESS_SWORDS_WOMAN_CID      | card-stats.s card_0990: Amazoness Swords Woman slot=0x14A4 pw=94004268; grep 0x000014a4 = 0 hits; conf: high |
| 0x08091850                                 | 0x00001930 | DIMENSION_WALL_CID              | card-stats.s card_1933: Dimension Wall slot=0x1930 pw=67095270; grep 0x00001930 = 0 hits; note: plate comment erroneously says "Viser Des check" -- Viser Des CID differs; conf: high |

### REF_SLOTS (USER-label + DATA-ref)

#### REUSE (16 slots -- existing globals, only label rename needed)

| Slot addr  | Value      | Global name           | New slot label                   | Source file   |
|------------|------------|-----------------------|----------------------------------|---------------|
| 0x08090cb4 | 0x0201c510 | gDuelFieldSlots       | ptr_gDuelFieldSlots_0cb4         | rom_data.inc  |
| 0x08090cb8 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_0cb8     | rom_data.inc  |
| 0x08090e54 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_0e54     | rom_data.inc  |
| 0x08090e60 | 0x0201c510 | gDuelFieldSlots       | ptr_gDuelFieldSlots_0e60         | rom_data.inc  |
| 0x08091044 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_1044     | rom_data.inc  |
| 0x0809105c | 0x0201c510 | gDuelFieldSlots       | ptr_gDuelFieldSlots_105c         | rom_data.inc  |
| 0x08091100 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_1100     | rom_data.inc  |
| 0x0809134c | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_134c     | rom_data.inc  |
| 0x08091360 | 0x0201c510 | gDuelFieldSlots       | ptr_gDuelFieldSlots_1360         | rom_data.inc  |
| 0x08091364 | 0x0201d9c0 | gEquipNodePool        | ptr_gEquipNodePool_1364          | rom_data.inc  |
| 0x080914f0 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_14f0     | rom_data.inc  |
| 0x080916a8 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_16a8     | rom_data.inc  |
| 0x080916bc | 0x0201e2a0 | gDuelCardCtxBase      | ptr_gDuelCardCtxBase_16bc        | rom_data.inc  |
| 0x08091730 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_1730     | rom_data.inc  |
| 0x080917dc | 0x0201c520 | gDuelFieldSlotState   | ptr_gDuelFieldSlotState_17dc     | rom_data.inc  |
| 0x08091884 | 0x0201bb90 | gEquipChainSlotRefs   | ptr_gEquipChainSlotRefs_1884     | rom_data.inc  |

#### NEW (5 slots -- 3 new globals needed)

Add to `constants/ewram.inc` under gEquipChainSlotRefs section:

```
.equ gEquipLpScoreBase,    0x0201afe0
    @ equip LP-score candidate work buffer; 9-word records, stride 0xb4 per player;
    @ zeroed at puzzle init (clear_region_8, 0x198 B); 68 raw ROM refs;
    @ build_equip_candidate_score_table uses as copy source;
    @ asm/13 LP_SCORE_BASE. C5 grep=0 (new). conf: high

.equ gEquipCandidateSlotA, 0x0201bc38
    @ = gEquipChainSlotRefs + 0xa8; first candidate slot activation array;
    @ indexed by activation_slot_idx*4; write_equip_target_score_entry reads [base+idx*4];
    @ 2 raw ROM refs. C5 grep=0 (new). conf: high

.equ gEquipCandidateSlotB, 0x0201bc3c
    @ = gEquipChainSlotRefs + 0xac; second (parallel) candidate slot array;
    @ write_equip_target_score_entry [base+idx*4] written at score match;
    @ 2 raw ROM refs. C5 grep=0 (new). conf: high
```

| Slot addr  | Value      | New global name       | New slot label                   |
|------------|------------|-----------------------|----------------------------------|
| 0x08090b34 | 0x0201afe0 | gEquipLpScoreBase     | ptr_gEquipLpScoreBase_0b34       |
| 0x080917cc | 0x0201bc38 | gEquipCandidateSlotA  | ptr_gEquipCandidateSlotA_17cc    |
| 0x0809184c | 0x0201bc38 | gEquipCandidateSlotA  | ptr_gEquipCandidateSlotA_184c    |
| 0x080917e0 | 0x0201bc3c | gEquipCandidateSlotB  | ptr_gEquipCandidateSlotB_17e0    |
| 0x08091848 | 0x0201bc3c | gEquipCandidateSlotB  | ptr_gEquipCandidateSlotB_1848    |

### RENAME_SLOTS (label + EOL)

The 16 REF_REUSE and 5 REF_NEW slots above require label renames (DAT_ -> ptr_<global>_<hex>).
No standalone pure-rename residual slots beyond the EQ/REF tables above.

### FUNC_RENAME (misnomer corrections)

None identified. build_equip_candidate_score_table, invoke_build_equip_candidate_score_table,
and write_equip_target_score_entry names are consistent with function bodies. Conf: high.

### PLATE (R5 -- full rewrite, ASCII)

#### build_equip_candidate_score_table (0x08090a78)

Current plate (line 24988): 554 chars, contains CJK. FUN_ stale refs:
FUN_080afcb4 -> eval_equip_spell_placement_with_score (asm/14 L13860).
FUN_080b04a8 -> eval_fieldspell_equip_placement_full (asm/14 L14939).

Proposed plate (ASCII, 417 chars):
```
Called by eval_equip_spell_placement_with_score + eval_fieldspell_equip_placement_full (indeg>=2, r1=1). Entry: r7=player_side, r9=mode_flag. Reads gEquipChainSlotRefs (0x0201bb90) context; outer loop r6=[0..1]: r6==r9 copies 9-word candidate entry via ldmia/stmia x3; r6!=r9 calls eval_slot_score_entry_full. Zeroes slot_b[+0x10/+1c/+20]. Writes gEquipChainSlotRefs score table. entry_size=0x38, player_stride=0x868.
```

#### invoke_build_equip_candidate_score_table (0x080916c0)

Current plate (line 26641): 564 chars, ASCII but over 500. FUN_08099314 is still unnamed
(in Seg-9+ range, not yet refined); leave as FUN_08099314 in plate.

Proposed plate (ASCII, 300 chars):
```
Thunk: sets r0=0, calls build_equip_candidate_score_table, returns via pop {r0}; bx r0. Called from tick_equip_zone_activation_display_state and FUN_08099314 (case_0 path) + 5 other callsites (7 total) at equip activation init. Returns pass-through from build_equip_candidate_score_table (0=success).
```

#### write_equip_target_score_entry (0x080916cc)

Current plate (line 26649): 775 chars, contains CJK. FUN_08091888 = eval_field_equip_activation_candidates
(Seg-9, line 26885). Plate note "Viser Des check" is incorrect -- CID 0x1930 = Dimension Wall.

Proposed plate (ASCII, 446 chars):
```
Called by eval_field_equip_activation_candidates (indeg=6). r0=player_id, r1=duel_zone_ptr, r2=score_entry_ptr, r8=target_slot_idx (non-APCS). Reads gEquipChainSlotRefs[+0x9c] (is_activated); writes [+0x2c+idx*4], [+0xa0+idx*4], [+0xa4+idx*4]. If r1==0: writes [+0xa8]=(1-r2[0]), [+0xac]=5; else r1[0]/r1[4]. Checks DIMENSION_WALL_CID=0x1930 via check_value_in_slot_chain; if found writes [+0xac]=5. Toggles zone[+0x38+idx*4] (activation toggle).
```

---

## carve plan (R7)

None. No ROM_INCBIN or function-between-function data blocks found in [0x08090a78, 0x08091888).

---

## disasm plan (R4)

None. No .byte code stubs or mislabeled code blocks found.

---

## New constants / globals

### New EQ (add to constants/card_info.inc)

```asm
.equ KINETIC_SOLDIER_CID,         0x000013aa  @ Kinetic Soldier (pw=79853073; card_0827 slot=0x13AA); F11 Seg-8 BST node; C5 grep=0; conf: high
.equ HUNTER_7_WEAPONS_CID,        0x000014cc  @ The Hunter with 7 Weapons (pw=01525329; card_1020 slot=0x14CC); F11 Seg-8 BST node; C5 grep=0; conf: high
.equ AMAZONESS_SWORDS_WOMAN_CID,  0x000014a4  @ Amazoness Swords Woman (pw=94004268; card_0990 slot=0x14A4); F11 Seg-8 BST pivot; C5 grep=0; conf: high
.equ STEAMROID_CID,               0x000018f2  @ Steamroid (pw=44729197; card_1876 slot=0x18F2); F11 Seg-8 BST node; C5 grep=0; conf: high
.equ SKYSCRAPER_CID,              0x000018ff  @ Skyscraper (pw=63035430; card_1888 slot=0x18FF); F11 Seg-8 BST node; C5 grep=0; conf: high
.equ DIMENSION_WALL_CID,          0x00001930  @ Dimension Wall (pw=67095270; card_1933 slot=0x1930); F11 Seg-8 check_value_in_slot_chain param; C5 grep=0; conf: high
.equ EQUIP_ATK_SCORE_HI_2499,     0x000009c3  @ Equip ATK score gate 2499 (2500-1); cmp score,0x9c3; bgt => scan bitmap; F11 Seg-8 build+write fns x4; C5 grep=0; conf: high
.equ EQUIP_ATK_SCORE_HI_2500,     0x000009c4  @ Equip ATK score gate 2500; cmp score,0x9c4; ble => skip; complement of 2499 gate; F11 Seg-8 x2; C5 grep=0; conf: high
```

### New REF globals (add to constants/ewram.inc)

```asm
.equ gEquipLpScoreBase,    0x0201afe0  @ equip LP-score candidate work buffer (clear_region_8, 0x198 B); 9-word records stride 0xb4/player; 68 raw refs; C5 grep=0; conf: high
.equ gEquipCandidateSlotA, 0x0201bc38  @ = gEquipChainSlotRefs+0xa8; first candidate slot activation array; write_equip_target_score_entry; 2 raw refs; C5 grep=0; conf: high
.equ gEquipCandidateSlotB, 0x0201bc3c  @ = gEquipChainSlotRefs+0xac; second candidate slot array (parallel); 2 raw refs; C5 grep=0; conf: high
```

---

## C13 Coverage Statement

Total DAT_ labels in [0x08090a78, 0x08091888): **73**

- EQ_REUSE: 36 slots (no new .equ; existing constants reused)
- EQ_NEW: 16 slots (8 unique new .equ entries)
- REF_REUSE: 16 slots (no new globals; label rename only)
- REF_NEW: 5 slots (3 new globals; label rename)

36 + 16 + 16 + 5 = **73** -- matches full current-label count. C13: 100% coverage.

Additional named pool: `seg7_pool_chainrefs_0af0` (pre-existing, holds gEquipChainSlotRefs,
no action needed).

---

## Section 5.1 Register (Rule 3)

No 0-reference blocks in Seg-8 (no ROM_INCBIN/.byte data blocks).

---

## Consumer Evidence (R6)

| Slot / global          | Semantic evidence                                                          | File:line        | Conf |
|------------------------|----------------------------------------------------------------------------|------------------|------|
| gEquipLpScoreBase      | asm/13 L11707: "LP_SCORE_BASE = 0x0201afe0"; asm/11 L30909 "clear_region_8=0x0201afe0"; asm/11 L25077-25087 ldmia/stmia x3 9-word copy source | asm/13:11707; asm/11:30909 | high |
| DIMENSION_WALL_CID     | card-stats.s L25144: Dimension Wall slot=0x1930 pw=67095270; corrects erroneous "Viser Des" in plate | card-stats.s:25144 | high |
| EQUIP_ATK_SCORE_HI_2499 | asm/11 L26199-26200: ldr r0,DAT_08091388; cmp r1,r0; bgt LAB_0809139e (score>2499 triggers scan); 4 occurrences | asm/11:26199 | high |
| EQUIP_ATK_SCORE_HI_2500 | asm/11 L26380-26384: ldr r0,DAT_080914ec; cmp r1,r0; ble skip (score<=2500 skips); 2 occurrences | asm/11:26380 | high |
| gEquipCandidateSlotA   | asm/11 L26730: base for candidate activation array indexed r4=slot_idx*4; write_equip_target_score_entry | asm/11:26730 | high |
| gEquipCandidateSlotB   | asm/11 L26778: parallel array base; write_equip_target_score_entry if gEquipCandidateSlotA != gEquipCandidateSlotB entry | asm/11:26778 | high |
| DIMENSION_WALL (plate fix) | write_equip_target_score_entry plate says "Viser Des check" but DAT_08091850=0x1930=Dimension Wall per card-stats.s; Viser Des CID is different | asm/11:26852; card-stats.s:25144 | high |

---

## Ask for Help

None. All semantics confirmed with file:line evidence.

---

## Slot Label Rename Reference (for fixer)

The complete list of 73 rename operations (DAT_<hex> -> new label):

**EQ slots** -- replace `ldr rN, DAT_<hex>` with `ldr rN, =<CONST>` or inline constant:
All 52 EQ slots (36 REUSE + 16 NEW) use `.equ` constants from the tables above.

**REF slots** -- rename label only:

```
DAT_08090b34  -> ptr_gEquipLpScoreBase_0b34
DAT_08090cb4  -> ptr_gDuelFieldSlots_0cb4
DAT_08090cb8  -> ptr_gEquipChainSlotRefs_0cb8
DAT_08090e54  -> ptr_gEquipChainSlotRefs_0e54
DAT_08090e60  -> ptr_gDuelFieldSlots_0e60
DAT_08091044  -> ptr_gEquipChainSlotRefs_1044
DAT_0809105c  -> ptr_gDuelFieldSlots_105c
DAT_08091100  -> ptr_gEquipChainSlotRefs_1100
DAT_0809134c  -> ptr_gEquipChainSlotRefs_134c
DAT_08091360  -> ptr_gDuelFieldSlots_1360
DAT_08091364  -> ptr_gEquipNodePool_1364
DAT_080914f0  -> ptr_gEquipChainSlotRefs_14f0
DAT_080916a8  -> ptr_gEquipChainSlotRefs_16a8
DAT_080916bc  -> ptr_gDuelCardCtxBase_16bc
DAT_08091730  -> ptr_gEquipChainSlotRefs_1730
DAT_080917cc  -> ptr_gEquipCandidateSlotA_17cc
DAT_080917dc  -> ptr_gDuelFieldSlotState_17dc
DAT_080917e0  -> ptr_gEquipCandidateSlotB_17e0
DAT_08091848  -> ptr_gEquipCandidateSlotB_1848
DAT_0809184c  -> ptr_gEquipCandidateSlotA_184c
DAT_08091884  -> ptr_gEquipChainSlotRefs_1884
```
