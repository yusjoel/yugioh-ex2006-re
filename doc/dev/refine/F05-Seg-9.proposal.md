# Refine Proposal: F05-Seg-9  [0x08051cc4..0x08052df8)

**Split declaration**: Seg-9 is split into Seg-9a and Seg-9b at function boundary
`check_equip_slot_eligible_by_type_and_card_id_pair` (0x080525d0).

- Seg-9a: 0x08051cc4..0x080525d0, fn 1-13, 55 slots
- Seg-9b: 0x080525d0..0x08052df8, fn 14-24, 62 slots
- Total Seg-9: 117 slots (exceeds 100-slot single-batch threshold, hence split)

---

## Segment Survey

### Function Entries (24 total)

| # | Addr | Name |
|---|------|------|
| 1 | 0x08051cc4 | check_equip_slot_eligible_by_card_id_bst_and_pairs |
| 2 | 0x08051dd8 | check_equip_slot_eligible_by_side_and_slot_vacant |
| 3 | 0x08051e24 | check_equip_slot_eligible_by_field8_and_chain |
| 4 | 0x08051e94 | check_equip_slot_eligible_by_side_mismatch_and_prereqs |
| 5 | 0x08051f04 | check_equip_slot_eligible_by_side_and_type_query |
| 6 | 0x08051f60 | check_equip_slot_eligible_by_type_query_prereqs_and_eligible |
| 7 | 0x08051fd0 | check_equip_slot_eligible_by_prereqs_and_slot8_flag |
| 8 | 0x08052020 | check_equip_slot_eligible_by_chain_node_and_activation |
| 9 | 0x08052080 | check_equip_slot_eligible_by_whitelist_type_and_state |
| 10 | 0x0805214c | check_equip_slot_eligible_by_slot_chain_node |
| 11 | 0x080521a0 | check_equip_slot_eligible_by_setcode_global_and_chain |
| 12 | 0x08052224 | check_equip_slot_eligible_by_card_id_dispatch |
| 13 | 0x08052398 | check_equip_slot_eligible_by_card_id_dispatch_alt |
| 14 | 0x080525d0 | check_equip_slot_eligible_by_type_and_card_id_pair |
| 15 | 0x08052674 | check_equip_slot_eligible_by_prereqs_and_duel_ctx |
| 16 | 0x080526cc | check_equip_slot_eligible_by_setcode_not_field6_17 |
| 17 | 0x08052734 | check_equip_slot_eligible_by_prereqs_and_spell_type |
| 18 | 0x08052790 | check_equip_slot_eligible_by_revival_jam_and_duel_ctx |
| 19 | 0x08052820 | check_equip_slot_eligible_by_owner_bit_and_chain_field |
| 20 | 0x08052884 | check_equip_slot_eligible_by_chain_list_entry |
| 21 | 0x08052954 | check_equip_slot_eligible_by_field6_present_no_field8 |
| 22 | 0x080529a8 | check_equip_slot_eligible_by_type_and_chain_score4 |
| 23 | 0x08052a20 | check_equip_slot_eligible_by_paired_card_zone_match |
| 24 | 0x08052aa8 | check_equip_slot_eligible_by_card_id_dispatch_b |

### Residual Auto-name Slots: 117 total

Value breakdown (all verified via python `struct.unpack_from('<I', rom, addr-0x08000000)`):

| Value | Count | Category |
|-------|-------|----------|
| 0x00000868 | 30 | PLAYER_BLOCK_STRIDE (EQ reuse) |
| 0x0201c510 | 30 | gDuelFieldSlots (EQ reuse) |
| 0x0201bb90 | 2 | gEquipChainSlotRefs (EQ reuse) |
| 0x0201b290 | 1 | gDuelPhaseFlags (EQ reuse) |
| 0x000004cc | 1 | LP_BAR_ANIM_STATE_OFF (EQ reuse) |
| 0x000004d4 | 1 | SPRITE_ROW_ENTRY_DATA_OFF (EQ reuse) |
| 0x000004f4 | 1 | CHAIN_NODE_CARD_ARR_OFF (EQ reuse) |
| 19 existing CID slots | 19 | EQ reuse from card_info.inc (18 unique values; 0x0fc9 x2) |
| 27 new CIDs | 27 | EQ new (new card_info.inc entries) |
| 0x9e380000 | 1 | Packed zone mask (RENAME) |
| 0xa3d00000 | 1 | Packed zone mask (RENAME) |
| 0xc5500000 | 1 | Packed zone mask (RENAME) |
| 0xc5b80000 | 1 | Packed zone mask (RENAME) |
| 0x000013b0 | 1 | Unallocated CID (RENAME) |

Total: 30+30+2+1+1+1+1+19+27+1+1+1+1+1 = **117**. Confirmed.

Breakdown:
- EQ reuse existing CIDs: 0x0fc9 (x2) + 17 others = 19 slots
- EQ new CIDs: 27 slots (one per CID value)
- RENAME (packed masks): 4 slots
- RENAME (unknown CID 0x13b0): 1 slot
- structural: 30+30+2+1+1+1+1 = 66
- 66 structural + 19 existing-CID EQ + 27 new-CID EQ + 5 RENAME = 117. Confirmed.

### ROM_INCBIN / .byte blocks: None

File 05 contains no ROM_INCBIN or .byte blocks. All inter-function space is literal pool (.word entries captured above) or .zero padding (1-2 bytes alignment). No carve or disasm work required.

---

## Data Block Classification (Rule 2/3)

No ROM_INCBIN or .byte blocks in range. Section not applicable.

---

## Symbolization Plan

### EQ_SLOTS (data-equate)

#### Structural globals (reuse existing ewram.inc / duel_field.inc)

All verified: constants from `constants/ewram.inc`.

**PLAYER_BLOCK_STRIDE = 0x00000868** (30 slots, both 9a and 9b):
```
DWORD_08051d20, DWORD_08051d74, DWORD_08051d9c, DWORD_08051dc8,
DWORD_08051e14, DWORD_08051e84, DAT_08051ef4, DAT_08051f50,
DAT_08051fc0, DAT_08052010, DAT_08052070, DAT_080520e8,
DWORD_08052190, DWORD_08052214, DAT_080522b4, DAT_08052420,
DAT_08052634, DWORD_08052724, DWORD_08052780, DWORD_080527e8,
DWORD_08052818, DWORD_08052874, DWORD_080528d8, DWORD_08052998,
DWORD_08052a0c, DWORD_08052a68, DWORD_08052a9c, DAT_08052b38,
DAT_08052d18, DAT_08052d64
```
Note: DWORD_08052e4c, DWORD_08052ebc, DWORD_08052f44 (addr >= 0x08052df8) belong to Seg-10.
Slot labels: `<slot>: .equ PLAYER_BLOCK_STRIDE` (no EOL needed, repeated pattern)

**gDuelFieldSlots = 0x0201c510** (30 slots, both 9a and 9b):
```
DWORD_08051d24, DWORD_08051d78, DWORD_08051da0, DWORD_08051dcc,
DWORD_08051e18, DWORD_08051e88, DAT_08051ef8, DAT_08051f54,
DAT_08051fc4, DAT_08052014, DAT_08052074, DAT_080520ec,
DWORD_08052194, DWORD_08052218, DAT_080522b8, DAT_08052424,
DAT_08052638, DWORD_08052728, DWORD_08052784, DWORD_080527ec,
DWORD_0805281c, DWORD_08052878, DWORD_080528dc, DWORD_0805299c,
DWORD_08052a10, DWORD_08052a6c, DWORD_08052aa0, DAT_08052b3c,
DAT_08052d1c, DAT_08052d68
```
Note: DWORD_08052e50, DWORD_08052ec0, DWORD_08052f48 (addr >= 0x08052df8) belong to Seg-10.

**gEquipChainSlotRefs = 0x0201bb90** (2 slots, Seg-9b only):
```
DWORD_080526b0, DWORD_080527f4
```
Note: DWORD_08052e54, DWORD_08052f04 (addr >= 0x08052df8) belong to Seg-10.
Evidence: ewram.inc line confirmed; used via [+4]=current_player and [+0x20]=current_slot
offsets in check_equip_slot_eligible_by_prereqs_and_duel_ctx (asm line 21293-21300) and
check_equip_slot_eligible_by_revival_jam_and_duel_ctx (asm line 21487-21492).
Confidence: high.

**gDuelPhaseFlags = 0x0201b290** (1 slot, Seg-9b):
```
DWORD_08052944
```
Evidence: ewram.inc confirmed; used as CHAIN_LIST_BASE in
check_equip_slot_eligible_by_chain_list_entry (asm line 21695).
Confidence: high.

**LP_BAR_ANIM_STATE_OFF = 0x000004cc** (1 slot, Seg-9b):
```
DWORD_08052948
```
Evidence: ewram.inc confirmed; used as offset to gDuelPhaseFlags (+0x4cc)
to reach chain count field in check_equip_slot_eligible_by_chain_list_entry.
Confidence: high.

**SPRITE_ROW_ENTRY_DATA_OFF = 0x000004d4** (1 slot, Seg-9b):
```
DWORD_0805294c
```
Evidence: ewram.inc confirmed; used as offset to gDuelPhaseFlags (+0x4d4)
to reach chain entry array in check_equip_slot_eligible_by_chain_list_entry.
Confidence: high.

**CHAIN_NODE_CARD_ARR_OFF = 0x000004f4** (1 slot, Seg-9b):
```
DWORD_08052950
```
Evidence: ewram.inc confirmed; used as offset to gDuelPhaseFlags (+0x4f4)
in check_equip_slot_eligible_by_chain_list_entry (asm line 21701).
Confidence: high.

#### Existing CID constants (19 slots, 18 unique values, reuse card_info.inc)

All verified: constants found via `grep` in `constants/card_info.inc`.

| Slot | Value | Existing Constant | Card Name |
|------|-------|-------------------|-----------|
| DWORD_08051da4 | 0x0fc9 | DARK_MAGICIAN_CID_0FC9 | Dark Magician |
| DAT_08052344 | 0x0fc9 | DARK_MAGICIAN_CID_0FC9 | Dark Magician |
| DWORD_08051d3c | 0x167d | KNIGHTS_TITLE_CID (new) | Knight's Title |
| DWORD_08051d40 | 0x12c5 | MULTIPLY_CID (new) | Multiply |
| DWORD_08051d4c | 0x1768 | NINJITSU_ART_OF_TRANSFORMATION_CID | Ninjitsu Art of Trans. |
| DAT_08052110 | 0x14cd | SHADOW_TAMER_CID (new) | Shadow Tamer |
| DAT_08052114 | 0x13b0 | cid_13b0 (RENAME) | Unallocated |
| DAT_08052120 | 0x14ce | DRAGON_MANIPULATOR_CID (new) | Dragon Manipulator |
| DAT_080522bc | 0x1715 | ULTRA_EVOLUTION_PILL_CID (new) | Ultra Evolution Pill |
| DAT_080522c0 | 0x140b | INSECT_IMITATION_CID (new) | Insect Imitation |
| DAT_080522d4 | 0x15a3 | METAMORPHOSIS_CID (new) | Metamorphosis |
| DAT_080522d8 | 0x1713 | DEDICATION_THROUGH_LIGHT_DARK_CID | Dedication through L&D |
| DAT_080522f0 | 0x1927 | SPIRITUAL_EARTH_ART_CID (new) | Spiritual Earth Art |
| DAT_08052304 | 0x19b1 | PHOTON_GENERATOR_UNIT_CID (new) | Photon Generator Unit |
| DAT_0805236c | 0x13c3 | GEARFRIED_IRON_KNIGHT_CID | Gearfried the Iron Knight |
| DAT_08052388 | 0x18f6 | CYBER_DRAGON_CID | Cyber Dragon |
| DAT_08052428 | 0x16a3 | DARK_SCORPION_COMBO_CID | Dark Scorpion Combination |
| DAT_0805242c | 0x14df | WINGBEAT_GIANT_DRAGON_CID (new) | A Wingbeat of Giant Dragon |
| DAT_08052430 | 0x12cf | GRACEFUL_DICE_CID (new) | Graceful Dice |
| DAT_08052434 | 0x1409 | LIMITER_REMOVAL_CID (new) | Limiter Removal |
| DAT_0805244c | 0x153d | PYRAMID_ENERGY_CID (new) | Pyramid Energy |
| DAT_0805246c | 0x17f9 | BIG_WAVE_SMALL_WAVE_CID (new) | Big Wave Small Wave |
| DAT_08052484 | 0x18cd | KAMINOTE_BLOW_CID (new) | Kaminote Blow |
| DAT_08052494 | 0x18d6 | MINEFIELD_ERUPTION_CID (new) | Minefield Eruption |
| DAT_080524ec | 0x1656 | DARK_SCORPION_CHICK_CID | Don Zaloog etc |
| DAT_080524f0 | 0x1532 | DON_ZALOOG_CID | Don Zaloog (range low) |
| DAT_080524f8 | 0x1686 | DARK_SCORPION_MEANAE_CID | Meanae range high |
| DAT_08052598 | 0x185a | CHU_SKE_MOUSE_FIGHTER_CID | Chu-Ske the Mouse Fighter |
| DAT_0805263c | 0x1957 | ELEMENTAL_HERO_TEMPEST_CID (new) | Elemental Hero Tempest |
| DWORD_08052a44 | 0x146f | CATHEDRAL_OF_NOBLES_CID (new) | Cathedral of Nobles |
| DWORD_08052a48 | 0x1907 | TRANSCENDENT_WINGS_CID (new) | Transcendent Wings |
| DAT_08052b40 | 0x17ff | NINJITSU_ART_OF_DECOY_CID | Ninjitsu Art of Decoy |
| DAT_08052b44 | 0x169b | CHECKMATE_CID | Checkmate |
| DAT_08052b48 | 0x14fc | GRADIUS_OPTION_CID | Gradius' Option |
| DAT_08052b5c | 0x15f7 | FORMATION_UNION_CID (new) | Formation Union |
| DAT_08052b78 | 0x179f | ORDER_TO_CHARGE_CID (new) | Order to Charge |
| DAT_08052b90 | 0x17b8 | ORDER_TO_SMASH_CID (new) | Order to Smash |
| DAT_08052bb8 | 0x18cb | DOUBLE_ATTACK_CID (new) | Double Attack |
| DAT_08052bd0 | 0x1890 | UNION_ATTACK_CID | Union Attack |
| DAT_08052bec | 0x195b | FEATHER_SHOT_CID | Feather Shot |
| DAT_08052c04 | 0x19ab | HERO_HEART_CID (new) | Hero Heart |
| DAT_08052c24 | 0x0fbc | SUMMONED_SKULL_CID (new) | Summoned Skull |
| DAT_08052c34 | 0x1414 | GRADIUS_CID | Gradius |
| DAT_08052c7c | 0x1691 | TERRORKING_ARCHFIEND_CID (new) | Terrorking Archfiend |
| DAT_08052cdc | 0x0ff8 | RED_EYES_B_DRAGON_CID (new) | Red-Eyes B. Dragon |
| DAT_08052dbc | 0x17ee | OJAMA_KING_CARD_ID | Ojama King |
| DAT_08052dcc | 0x18a6 | EHERO_AVIAN_CID | Elemental Hero Avian |

Note: NINJITSU_ART_OF_TRANSFORMATION_CID (0x1768) and DEDICATION_THROUGH_LIGHT_DARK_CID (0x1713)
already existed; DARK_MAGICIAN_CID_0FC9 exists x2. Others marked "(new)" require new card_info.inc entries.

### RENAME_SLOTS

#### Packed zone mask slots (4 slots -- no named constant; raw bitmask identity)

These slots hold packed comparison masks `(CID << 19)`. They are not card_id constants themselves
but post-shift comparison values. They should be renamed with descriptive labels + EOL comments.

| Slot | Value | New label | EOL comment |
|------|-------|-----------|-------------|
| DWORD_080527f0 | 0x9e380000 | `revival_jam_zone_mask` | `Revival Jam (0x13c7) << 19` |
| DWORD_08052a70 | 0xa3d00000 | `cathedral_of_nobles_zone_mask` | `Mystical Beast Serket (0x147a) << 19; Cathedral of Nobles path` |
| DWORD_08052aa4 | 0xc5500000 | `transcendent_wings_zone_mask` | `Winged Kuriboh (0x18aa) << 19; Transcendent Wings path` |
| DAT_080525bc | 0xc5b80000 | `mine_golem_zone_mask` | `Mine Golem (0x18b7) << 19; dispatch_alt Chu-Ske range end` |

Verification (python): `0x9e380000>>19 = 0x13c7` (Revival Jam, card-stats.s line),
`0xa3d00000>>19 = 0x147a` (Mystical Beast Serket), `0xc5500000>>19 = 0x18aa` (Winged Kuriboh),
`0xc5b80000>>19 = 0x18b7` (Mine Golem). All confirmed against card-stats.s.

#### Unallocated CID slot (1 slot)

| Slot | Value | New label | EOL comment | Confidence |
|------|-------|-----------|-------------|------------|
| DAT_08052114 | 0x13b0 | `cid_13b0` | `unallocated slot_id; not found in card-stats.s` | low |

Basis: card-stats.s does not contain any entry with `slot=0x13b0`. The asm comment at line 20413
notes "between 0x13AC Souleater and 0x13B1 Timeater". This is an unallocated game slot with
unknown semantics. Named with neutral `cid_13b0` per methodology for unallocated CIDs.

### FUNC_RENAME

No function renames required. All 24 functions in range have semantically correct names.
Checked: function bodies operate on gDuelFieldSlots + PLAYER_BLOCK_STRIDE consistently
with their existing check_equip_slot_eligible_by_* naming pattern.

### PLATE (R5, C8 stale FUN_ replacements)

Two stale `FUN_` references found via grep pattern `FUN_[0-9a-f]{8}` in lines 19855-22550:

**Plate 1** (asm line 20115, function check_equip_slot_eligible_by_side_mismatch_and_prereqs):
- Current: `...passed to FUN_0809077c as callback...`
- Target: `FUN_0809077c` -> `invoke_count_zone_pair_hits_full_range`
- Replacement: substring `FUN_0809077c` -> `invoke_count_zone_pair_hits_full_range`
- Source: naming-proposals.csv line: `0x0809077c,invoke_count_zone_pair_hits_full_range`

**Plate 2** (asm line 21171, function check_equip_slot_eligible_by_type_and_card_id_pair):
- Current: `...called by FUN_080556f0 (indeg=1)...`
- Target: `FUN_080556f0` -> `check_equip_slot_eligible_by_setcode_activation_and_zone_pair`
- Replacement: substring `FUN_080556f0` -> `check_equip_slot_eligible_by_setcode_activation_and_zone_pair`
- Source: naming-proposals.csv line: `0x080556f0,check_equip_slot_eligible_by_setcode_activation_and_zone_pair`

Both replacements are ASCII-only. No new stale FUN_ plates created in this segment
(all function comments already use named function references).

---

## Carve Plan (R7)

None. No ROM_INCBIN blocks in Seg-9. All inter-function bytes are literal pool slots
(.word) or .zero alignment padding.

## Disasm Plan (R4)

None. No opaque byte blocks in Seg-9. All functions are fully disassembled.

---

## New Constants / Globals

All 27 to be added to `constants/card_info.inc` (C5 verified: none exist there already).

### New CID equates (27 new card_info.inc entries)

```
.equ SUMMONED_SKULL_CID,             0x00000fbc  @ Summoned Skull (pw=70781052, card_0022)
.equ RED_EYES_B_DRAGON_CID,          0x00000ff8  @ Red-Eyes B. Dragon (pw=74677422, card_0082)
.equ MULTIPLY_CID,                   0x000012c5  @ Multiply (pw=40703222); Multiply frog tokens
.equ GRACEFUL_DICE_CID,              0x000012cf  @ Graceful Dice (pw=74137509)
.equ SHADOW_TAMER_CID,               0x000014cd  @ Shadow Tamer (pw=37620434)
.equ DRAGON_MANIPULATOR_CID,         0x000014ce  @ Dragon Manipulator (pw=74701381)
.equ WINGBEAT_GIANT_DRAGON_CID,      0x000014df  @ A Wingbeat of Giant Dragon (pw=28596933)
.equ INSECT_IMITATION_CID,           0x0000140b  @ Insect Imitation (pw=96965364)
.equ LIMITER_REMOVAL_CID,            0x00001409  @ Limiter Removal (pw=23171610)
.equ CATHEDRAL_OF_NOBLES_CID,        0x0000146f  @ Cathedral of Nobles (pw=29732298)
.equ PYRAMID_ENERGY_CID,             0x0000153d  @ Pyramid Energy (pw=76826042)
.equ METAMORPHOSIS_CID,              0x000015a3  @ Metamorphosis (pw=46411259)
.equ FORMATION_UNION_CID,            0x000015f7  @ Formation Union (pw=26708437)
.equ KNIGHTS_TITLE_CID,              0x0000167d  @ Knight's Title (pw=87210505)
.equ TERRORKING_ARCHFIEND_CID,       0x00001691  @ Terrorking Archfiend (pw=55321970)
.equ ULTRA_EVOLUTION_PILL_CID,       0x00001715  @ Ultra Evolution Pill (pw=78418106)
.equ ORDER_TO_CHARGE_CID,            0x0000179f  @ Order to Charge (pw=78986941)
.equ ORDER_TO_SMASH_CID,             0x000017b8  @ Order to Smash (pw=39019325)
.equ BIG_WAVE_SMALL_WAVE_CID,        0x000017f9  @ Big Wave Small Wave (pw=51562916)
.equ DOUBLE_ATTACK_CID,              0x000018cb  @ Double Attack (pw=34187685)
.equ KAMINOTE_BLOW_CID,              0x000018cd  @ Kaminote Blow (pw=97570038)
.equ MINEFIELD_ERUPTION_CID,         0x000018d6  @ Minefield Eruption (pw=85519211)
.equ TRANSCENDENT_WINGS_CID,         0x00001907  @ Transcendent Wings (pw=25573054)
.equ SPIRITUAL_EARTH_ART_CID,        0x00001927  @ Spiritual Earth Art - Kurogane (pw=70156997)
.equ ELEMENTAL_HERO_TEMPEST_CID,     0x00001957  @ Elemental Hero Tempest (pw=...card_2150+)
.equ HERO_HEART_CID,                 0x000019ab  @ Hero Heart (pw=67951831)
.equ PHOTON_GENERATOR_UNIT_CID,      0x000019b1  @ Photon Generator Unit (pw=...card_2205+)
```

Note: CID 0x13b0 is unallocated (not found in card-stats.s), so no named constant is created
for it -- it becomes RENAME slot `cid_13b0` (see RENAME_SLOTS section).

Packed zone masks are raw bitmask values, not CID constants, so they go into RENAME (not new card_info.inc).

### No new globals

All globals (gDuelFieldSlots, gEquipChainSlotRefs, gDuelPhaseFlags, and offsets) already exist
in `constants/ewram.inc`. Verified by grep.

---

## Section 5.1 Registration (Rule 3, 0-reference blocks)

No new Sec5.1 entries from Seg-9. File 05 has no ROM_INCBIN blocks with 0 references in this range.

Existing Sec5.1 entries from earlier segs (carried forward, not changed by Seg-9):
- 0x0804f2cc / 64B (Seg-4, affine-type mapping)
- 0x0804f30c / 128B (Seg-4, dispatch handler table)
- 0x0804fe00 / ?B (Seg-4, modular arithmetic routine)

---

## Consumer Evidence (R6)

### gEquipChainSlotRefs offsets

- `check_equip_slot_eligible_by_prereqs_and_duel_ctx` (0x08052674):
  asm line 21293-21300: `ldr r0, DWORD_080526b0` loads 0x0201bb90; `ldr r1,[r0,#0x4]` reads
  [+4]=current_player; `ldr r0,[r2,#0x20]` reads [+0x20]=current_slot. Confidence: high.

- `check_equip_slot_eligible_by_revival_jam_and_duel_ctx` (0x08052790):
  asm line 21487-21492: same [+4]/[+0x20] offsets to gEquipChainSlotRefs (0x0201bb90).
  Confidence: high.

- `check_equip_slot_eligible_by_owner_match_and_active_ctx` (0x08052ecc... function in Seg-10):
  asm line 22531: `ldr r1, DWORD_08052f04` (= gEquipChainSlotRefs); [+4] vs owner_bit,
  [+0x20] vs slot_idx. Confidence: high. (Note: DWORD_08052f04 is a Seg-10 slot; listed here
  as consumer evidence only — the equate itself is applied by Seg-10 proposal.)

### Revival Jam packed mask

- `check_equip_slot_eligible_by_revival_jam_and_duel_ctx` (0x08052790):
  asm lines 21475-21479: `ldr r0,[r0,#0x0]` reads zone slot word; `lsls r0,r0,#0x13` shifts
  left 19 bits; `ldr r1, DWORD_080527f0` = 0x9e380000; `cmp r0,r1` == test.
  Meaning: slot word bits[12:0] << 19 == 0x9e380000, i.e. card_id == 0x13c7 (Revival Jam).
  Confidence: high (python verified: 0x9e380000 >> 19 = 0x13c7, card-stats.s confirmed Revival Jam).

### Dark Scorpion cluster range (dispatch_alt)

- `check_equip_slot_eligible_by_card_id_dispatch_alt` (0x08052398):
  asm lines 21047-21056: range check uses DAT_080524f0 (0x1532=Don Zaloog) as low bound,
  DAT_080524f8 (0x1686=Meanae) and DAT_080524ec (0x1656) for BST pivots. Card range
  [0x1532..0x1686] maps to Dark Scorpion monster cluster.
  Confidence: high (card-stats.s confirms DON_ZALOOG_CID=0x1532, DARK_SCORPION_MEANAE_CID=0x1686).

### Chu-Ske range (dispatch_alt, Seg-9a)

- asm line 21137: `DAT_08052598 = 0x185a` (CHU_SKE_MOUSE_FIGHTER_CID).
  The range check at LAB_08052578 (asm line 21119) checks `r1 >= 0x185a` and `r1 <= 0x185a+0x5f`
  (= 0x18b9 = Master Monk). This matches the Chu-Ske..Master Monk cluster [0x185a..0x18b9].
  Confidence: high.

---

## Slot Count Reconciliation (C13)

Total unique slot labels in range: 117 (verified by reviewer grep: `sed -n '19855,22390p' asm/05_equip_eligibility_a.s | grep '^DAT_\|^DWORD_' | wc -l` = 117)

Breakdown:
- EQ_SLOTS structural (PLAYER_BLOCK_STRIDE x30, gDuelFieldSlots x30, gEquipChainSlotRefs x2,
  gDuelPhaseFlags x1, LP_BAR_ANIM_STATE_OFF x1, SPRITE_ROW_ENTRY_DATA_OFF x1,
  CHAIN_NODE_CARD_ARR_OFF x1) = 66
- EQ_SLOTS CID reuse: 0x0fc9 appears x2 (DWORD_08051da4 + DAT_08052344) = 2 slots;
  other existing named CIDs (17 unique values, each x1 slot):
  NINJITSU_ART_OF_TRANSFORMATION_CID (0x1768), DEDICATION_THROUGH_LIGHT_DARK_CID (0x1713),
  GEARFRIED_IRON_KNIGHT_CID (0x13c3), CYBER_DRAGON_CID (0x18f6),
  DARK_SCORPION_COMBO_CID (0x16a3), DARK_SCORPION_CHICK_CID (0x1656),
  DON_ZALOOG_CID (0x1532), DARK_SCORPION_MEANAE_CID (0x1686),
  NINJITSU_ART_OF_DECOY_CID (0x17ff), CHECKMATE_CID (0x169b),
  GRADIUS_OPTION_CID (0x14fc), UNION_ATTACK_CID (0x1890),
  FEATHER_SHOT_CID (0x195b), CHU_SKE_MOUSE_FIGHTER_CID (0x185a),
  OJAMA_KING_CARD_ID (0x17ee), EHERO_AVIAN_CID (0x18a6), GRADIUS_CID (0x1414) = 17
  Total existing CID reuse slots: 2 + 17 = **19**
- EQ_SLOTS CID new (27 new constants): **27** slots
- RENAME_SLOTS packed masks: 4
- RENAME_SLOTS unallocated CID: 1

Total: 66 + 19 + 27 + 4 + 1 = **117**. Confirmed.

Note: 8 slots with addr >= 0x08052df8 (PLAYER_BLOCK_STRIDE: DWORD_08052e4c/ebc/f44;
gDuelFieldSlots: DWORD_08052e50/ec0/f48; gEquipChainSlotRefs: DWORD_08052e54/f04)
belong to Seg-10 and are excluded from this proposal.

---

## Seek Help

None. All semantics confirmed by consumer code analysis, card-stats.s lookup, and constants/*.inc
grep. The only unresolved item is CID 0x13b0 (not in card-stats.s), handled as neutral RENAME.

---

## Executor Report: F05-Seg-9

- Slots: EQ=112 (66 structural + 19 CID-reuse + 27 CID-new) REF=0 RENAME=5 FUNC_RENAME=0 PLATE=2
- carve=0 disasm=0 section5_1=0 (no new orphan blocks)
- New constants/globals: 27 new CID equates for card_info.inc (see "New Constants" section)
- Seek help: none
- proposal: doc/dev/refine/F05-Seg-9.proposal.md
