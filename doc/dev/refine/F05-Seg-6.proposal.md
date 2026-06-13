# Refine Proposal: F05-Seg-6  [0x0804d124..0x0804ffba)

## Split Recommendation

Seg-6 carries ~128 auto-name slots across 24 functions.  Split into:
- **Seg-6a**: 0x0804d124..0x0804f6c4  (17 fn; sprite-row anim/queue dispatch cluster + eligibility predicate variants; ~67 slots)
- **Seg-6b**: 0x0804f6c4..0x0804ffba  (7 fn; check_slot_card_eligible_by_card_id BST hub + state-code stubs + zone-bit stubs; ~61 slots)

Boundary at 0x0804f6c4 = start of check_slot_card_eligible_by_card_id.

---

## Segment Survey

### Function Entries x24

| addr | name |
|---|---|
| 0x0804d124 | switchD_0804ce98__caseD_1e |
| 0x0804d14c | switchD_0804ce98__caseD_1f |
| 0x0804d1ca | switchD_0804ce98__caseD_3 |
| 0x0804d1e4 | dispatch_sprite_row_anim_by_state |
| 0x0804daf6 | reset_sprite_row_queue_tail |
| 0x0804db50 | dispatch_sprite_row_queue_by_state |
| 0x0804f0c2 | clear_sprite_row_queue_overflow_flag |
| 0x0804f0e4 | flush_sprite_row_queue_partial |
| 0x0804f1dc | compact_equip_zone_rank3_entries |
| 0x0804f2e0 | dispatch_equip_field_update_by_anim_state |
| 0x0804f34c | advance_equip_zone_rank_state |
| 0x0804f440 | check_equip_slot_eligibility_with_whitelist |
| 0x0804f4ec | check_equip_slot_eligible_with_owner_and_type |
| 0x0804f550 | check_equip_slot_eligible_triple_predicate |
| 0x0804f5c4 | check_equip_slot_eligible_by_owner_and_prereqs |
| 0x0804f618 | check_equip_slot_eligible_with_whitelist_and_type |
| 0x0804f688 | check_equip_target_matches_card_owner |
| 0x0804f6c4 | check_slot_card_eligible_by_card_id |
| 0x0804fed6 | return_zero_unconditional |
| 0x0804ff54 | check_card_state_code_eq_15 |
| 0x0804ff72 | check_card_state_code_eq_16 |
| 0x0804ff7c | check_card_state_code_eq_13 |
| 0x0804ff9a | check_card_state_code_eq_11 |
| 0x0804ffa4 | check_card_state_code_eq_3 |

### Residual Auto-Name Slots

**Seg-6a** (~67 slots):

DAT_0804d218=0x0201b290, DAT_0804d21c=0x00000494, DAT_0804d254=0x0804d258,
PTR_DAT_0804d258 (15 entries, 0x4d258..0x4d290: raw jump-table ptrs into ROM_INCBIN 0x4d294),
PTR_DAT_0804d264 (one entry in the same table; aliased by asm as separate label -- single slot),
DAT_0804db44=0x0201b290, DAT_0804db48=0x0000048c, DAT_0804db4c=0x0000049c,
DAT_0804db88=0x0201b290, DAT_0804dbac=0x0201b290, DAT_0804dbb0=0x0000049c,
DAT_0804dbb4=0x0804dbb8 (ptr to PTR_DAT_0804dbb8 jump table),
PTR_DAT_0804dbb8 (104 entries, 0x4dbb8..0x4dd54: raw ptrs into ROM_INCBIN 0x4dd58; 12 unique targets + default 0x0804f0c2),
DAT_0804f0e0=0x0201b290, DAT_0804f1cc=0x0201b290, DAT_0804f1d0=0xfffffd00,
DAT_0804f1d4=0x0000048c, DAT_0804f1d8=0x00000494,
DAT_0804f288=0x0201b290, DAT_0804f28c=0xfffffb80,
DAT_0804f2d4=0x0201b290, DAT_0804f2d8=0x0000048c, DAT_0804f2dc=0x00000494,
DAT_0804f2f4=0x0201b290, DAT_0804f2f8=0x0000048c,
DAT_0804f368=0x0201e4d0,
DAT_0804f3ac=0x0201b290, DAT_0804f3b0=0xfffffe01, DAT_0804f3b4=0x0000048c,
DAT_0804f3e0=0xfffffe01, DAT_0804f3e4=0x0201b290, DAT_0804f3e8=0x0000048c,
DAT_0804f418=0xfffffe01, DAT_0804f41c=0x0201b290, DAT_0804f43c=0xfffffe01,
DAT_0804f49c=0x00000868, DAT_0804f4a0=0x0201c510,
DAT_0804f4cc=0x00000868, DAT_0804f4d0=0x0201c510,
DAT_0804f540=0x00000868, DAT_0804f544=0x0201c510,
DAT_0804f5b4=0x00000868, DAT_0804f5b8=0x0201c510,
DAT_0804f608=0x00000868, DAT_0804f60c=0x0201c510,
DAT_0804f678=0x00000868, DAT_0804f67c=0x0201c510,
DAT_0804f6c0=0x0000ffff

(Total: ~67 unique data-word slots + 2 ROM_INCBIN blocks)

**Seg-6b** (~61 slots):

DAT_0804f71c=0x00000868, DAT_0804f720=0x0201c510,
DAT_0804f7c8=0x00000868, DAT_0804f7cc=0x0201c510,
DAT_0804f7d0=0x00001496, DAT_0804f7d4=0x000010ed,
DAT_0804f7f0=0x000010d4, DWORD_0804f80c=0x000010da,
DAT_0804f834=0x000010e5, DAT_0804f84c=0x000010e2,
DAT_0804f870=0x000010ea, DAT_0804f888=0x000010eb,
DAT_0804f8bc=0x000012ef, DAT_0804f8c0=0x000010ee,
DAT_0804f8d0=0x00001232, DAT_0804f8ec=0x000012c6,
DAT_0804f904=0x000012d3, DAT_0804f938=0x00001366,
DAT_0804f948=0x00001322, DAT_0804f964=0x000013f6,
DAT_0804f97c=0x00001466,
DAT_0804f9c0=0x00001759, DAT_0804f9c4=0x000015cf,
DAT_0804f9d4=0x0000150a, DAT_0804f9f0=0x0000159e,
DAT_0804fa08=0x000015b0, DAT_0804fa0c=0x000015b3,
DAT_0804fa34=0x000015d7, DAT_0804fa38=0x000015d3,
DAT_0804fa50=0x000015d5,
DAT_0804fa74=0x00001693, DAT_0804fa8c=0x0000169a,
DAT_0804fac0=0x00001909, DAT_0804fad8=0x000017fb,
DAT_0804fafc=0x000018d0, DAT_0804fb08=0x000018d1,
DAT_0804fb44=0x0000193a, DAT_0804fb68=0x000019bd,
DAT_0804fb80=0x000019d7,
DAT_0804fbfc=0x000010bc, DAT_0804fc00=0x00000fee,
DAT_0804fc1c=0x00000fe4, DAT_0804fc20=0x00000fe5,
DAT_0804fc2c=0x00001114, DAT_0804fc38=0x00001296,
DAT_0804fc54=0x0000129e, DAT_0804fc58=0x00000fc9,
DAT_0804fc68=0x0000142d, DAT_0804fc74=0x00001414,
DAT_0804fc94=0x00000513,
DAT_0804fd4c=0x0000185a, DAT_0804fd58=0x000018a9,
DAT_0804fd78=0x000005dc, DAT_0804fd88=0x000018f9,
DAT_0804fd9c=0x0000194e, DAT_0804fdb4=0x00001757,
DAT_0804fdb8=0x0000191d,
DAT_0804fdfc=0x000015cd, DAT_0804fe10=0x000015d0,
DAT_0804fe24=0x000015d2, DAT_0804fe38=0x000015d4,
DAT_0804fe5c=0x000015d6, DAT_0804fe64=0x0000160a,
DAT_0804fe6c=0x0000190b,
DAT_0804fedc=0x00000868, DAT_0804fee0=0x0201c510,
DAT_0804fef4=0x00001915, DAT_0804ff14=0x00001947

(Total: ~61 unique data-word slots)

### ROM_INCBIN / .byte blocks

| block | addr | size |
|---|---|---|
| DAT_0804d294 (ROM_INCBIN) | 0x0804d294 | 0x862 (2146 B) |
| DAT_0804dd58 (ROM_INCBIN) | 0x0804dd58 | 0x136a (4970 B) |

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence per block

| block | ref-scan (raw / THUMB+1) | verdict | rationale |
|---|---|---|---|
| 0x0804d294 sz 0x862 | raw=1 @0x0804d258 (PTR_DAT_0804d258[0]); thumb+1=0 | disasm R4 | Jump table PTR_DAT_0804d258 stores 15 raw ptr entries pointing into this block. First halfword = 0xf047 (valid THUMB BL encoding). dispatch_sprite_row_anim_by_state dispatches via `ldr r0,[table+idx*4]; bx r0` -- mode switched by bx, so raw (not THUMB+1) is correct. |
| 0x0804dd58 sz 0x136a | raw=1 @0x0804dbb8 (PTR_DAT_0804dbb8[0]); thumb+1=0 | disasm R4 | Jump table PTR_DAT_0804dbb8 has 104 entries (states 0..103); 12 unique THUMB handler targets inside this block + default 0x0804f0c2. First halfword = 0x4d0a (valid THUMB LDR encoding). Same raw-ptr dispatch via `bx r0` pattern. |

Ref-scan note: raw=1 for block 0x4d294 comes from PTR_DAT_0804d258 entry 0 only (confirmed: ROM search finds exactly one occurrence at 0x0804d258). No THUMB+1 refs exist -- the dispatcher uses `bx r0` with raw addresses.

---

## Symbolization Plan (R1/R2/R3)

### EQ_SLOTS (data-equate)

**Seg-6a** -- gDuelPhaseFlags sprite-row offsets (all NEW in ewram.inc):

| slot | value | const_name | slot_label | source |
|---|---|---|---|---|
| DAT_0804d218 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s | ewram.inc already defined; reuse |
| DAT_0804d21c | 0x00000494 | SPRITE_ROW_ANIM_CTL_OFF | sprite_row_anim_ctl_off_s | NEW ewram.inc; dispatch_sprite_row_anim_by_state state_offset comment |
| DAT_0804db44 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_b | reuse |
| DAT_0804db48 | 0x0000048c | SPRITE_ROW_ANIM_STATE_OFF | sprite_row_anim_state_off_s | NEW ewram.inc; dispatch_equip_field_update_by_anim_state: anim_state_offset=0x48c |
| DAT_0804db4c | 0x0000049c | SPRITE_ROW_QUEUE_STATE_OFF | sprite_row_queue_state_off_s | NEW ewram.inc; dispatch_sprite_row_queue_by_state: state_code_off=0x49c |
| DAT_0804db88 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_c | reuse |
| DAT_0804dbac | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_d | reuse |
| DAT_0804dbb0 | 0x0000049c | SPRITE_ROW_QUEUE_STATE_OFF | sprite_row_queue_state_off_s_b | reuse |
| DAT_0804f0e0 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_e | reuse |
| DAT_0804f1cc | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_f | reuse |
| DAT_0804f1d4 | 0x0000048c | SPRITE_ROW_ANIM_STATE_OFF | sprite_row_anim_state_off_s_b | reuse |
| DAT_0804f1d8 | 0x00000494 | SPRITE_ROW_ANIM_CTL_OFF | sprite_row_anim_ctl_off_s_b | reuse |
| DAT_0804f288 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_g | reuse |
| DAT_0804f2d4 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_h | reuse |
| DAT_0804f2d8 | 0x0000048c | SPRITE_ROW_ANIM_STATE_OFF | sprite_row_anim_state_off_s_c | reuse |
| DAT_0804f2dc | 0x00000494 | SPRITE_ROW_ANIM_CTL_OFF | sprite_row_anim_ctl_off_s_c | reuse |
| DAT_0804f2f4 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_i | reuse |
| DAT_0804f2f8 | 0x0000048c | SPRITE_ROW_ANIM_STATE_OFF | sprite_row_anim_state_off_s_d | reuse |
| DAT_0804f3ac | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_j | reuse |
| DAT_0804f3b0 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | rank_field_mask_s | reuse demo_state.inc; clears bits[8:1] of rank halfword in advance_equip_zone_rank_state |
| DAT_0804f3b4 | 0x0000048c | SPRITE_ROW_ANIM_STATE_OFF | sprite_row_anim_state_off_s_e | reuse |
| DAT_0804f3e0 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | rank_field_mask_s_b | reuse |
| DAT_0804f3e4 | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_k | reuse |
| DAT_0804f3e8 | 0x0000048c | SPRITE_ROW_ANIM_STATE_OFF | sprite_row_anim_state_off_s_f | reuse |
| DAT_0804f418 | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | rank_field_mask_s_c | reuse |
| DAT_0804f41c | 0x0201b290 | gDuelPhaseFlags | gDuelPhaseFlags_s_l | reuse |
| DAT_0804f43c | 0xfffffe01 | DEMO_CLEAR_BITS_8_1 | rank_field_mask_s_d | reuse |
| DAT_0804f49c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_s | ewram.inc already defined; reuse |
| DAT_0804f4a0 | 0x0201c510 | gDuelFieldSlots | gduelfield_slots_s | ewram.inc already defined; reuse |
| DAT_0804f4cc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_s_b | reuse |
| DAT_0804f4d0 | 0x0201c510 | gDuelFieldSlots | gduelfield_slots_s_b | reuse |
| DAT_0804f540 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_s_c | reuse |
| DAT_0804f544 | 0x0201c510 | gDuelFieldSlots | gduelfield_slots_s_c | reuse |
| DAT_0804f5b4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_s_d | reuse |
| DAT_0804f5b8 | 0x0201c510 | gDuelFieldSlots | gduelfield_slots_s_d | reuse |
| DAT_0804f608 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_s_e | reuse |
| DAT_0804f60c | 0x0201c510 | gDuelFieldSlots | gduelfield_slots_s_e | reuse |
| DAT_0804f678 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_s_f | reuse |
| DAT_0804f67c | 0x0201c510 | gDuelFieldSlots | gduelfield_slots_s_f | reuse |
| DAT_0804f6c0 | 0x0000ffff | SLOT_CARD_EMPTY | slot_card_empty_s | card_info.inc; reuse (C5 fix #2) |

Special Seg-6a scalar slots (RENAME not EQ; see below):
- DAT_0804f1d0=0xfffffd00 (compact_equip_zone_rank3_entries stride delta -0x300; no matching constant; RENAME_SLOTS)
- DAT_0804f28c=0xfffffb80 (compact fn DELTA_STRIDE=-0x480; no matching constant; RENAME_SLOTS)
- DAT_0804d254=0x0804d258 (ptr to table; REF_SLOT)
- DAT_0804dbb4=0x0804dbb8 (ptr to queue dispatch table; REF_SLOT)

**Seg-6b** -- CID equates (EQ_SLOTS):

Reuse existing card_info.inc (16 CIDs):

| slot | value | const_name |
|---|---|---|
| DAT_0804fc1c | 0x0fe4 | HARPIE_LADY_CID |
| DAT_0804fc20 | 0x0fe5 | HARPIE_LADY_SISTERS_CID |
| DAT_0804fc00 | 0x0fee | COCOON_OF_EVOLUTION_CID |
| DAT_0804fbfc | 0x10bc | PETIT_MOTH_CID (verify name in card_info.inc) |
| DAT_0804f8d0 | 0x1232 | MAGICAL_LABYRINTH_CID |
| DAT_0804f904 | 0x12d3 | AMPLIFIER_CID |
| DAT_0804f948 | 0x1322 | SNATCH_STEAL_CID |
| DAT_0804f938 | 0x1366 | PREMATURE_BURIAL_CID |
| DAT_0804f964 | 0x13f6 | LIGHTNING_BLADE_CID |
| DAT_0804fc74 | 0x1414 | GRADIUS_CID |
| DAT_0804fc38 | 0x1296 | JINZO_CID |
| DAT_0804fc54 | 0x129e | DARK_MAGICIAN_GIRL_CID |
| DAT_0804fc58 | 0x0fc9 | DARK_MAGICIAN_CID_0FC9 |
| DAT_0804fc68 | 0x142d | DARK_MAGICIAN_CID_142D |
| DAT_0804f97c | 0x1466 | DARK_NECROFEAR_CID |
| DAT_0804f9d4 | 0x150a | HEART_OF_CLEAR_WATER_CID |
| DAT_0804f9c4 | 0x15cf | KIRYU_CID |
| DAT_0804fa34 | 0x15d7 | FREEZING_BEAST_CID |
| DAT_0804fa74 | 0x1693 | METALLIZING_PARASITE_CID |
| DAT_0804fa8c | 0x169a | FALLING_DOWN_CID |
| DAT_0804fa8c | 0x169a | FALLING_DOWN_CID |
| DAT_0804fac0 | 0x1909 | SPARK_BLASTER_CID |
| DAT_0804f9c0 | 0x1759 | OPTI_CAMO_ARMOR_CID |
| DAT_0804fd88 | 0x18f9 | EHERO_BUBBLEMAN_CID |
| DAT_0804fb08 | 0x18d1 | NITRO_UNIT_CID |
| DAT_0804fd9c | 0x194e | EHERO_WILDHEART_CID |
| DAT_0804fb80 | 0x19d7 | SYMBOL_OF_HERITAGE_CID |

Non-CID scalar reuse:

| slot | value | const_name | source |
|---|---|---|---|
| DAT_0804f71c | 0x0868 | PLAYER_BLOCK_STRIDE | ewram.inc; reuse |
| DAT_0804f720 | 0x0201c510 | gDuelFieldSlots | ewram.inc; reuse |
| DAT_0804f7c8 | 0x0868 | PLAYER_BLOCK_STRIDE | reuse |
| DAT_0804f7cc | 0x0201c510 | gDuelFieldSlots | reuse |
| DAT_0804fedc | 0x0868 | PLAYER_BLOCK_STRIDE | reuse |
| DAT_0804fee0 | 0x0201c510 | gDuelFieldSlots | reuse |
| DAT_0804fd78 | 0x05dc | CARD_STAT_LP_THRESHOLD_1500 | card_info.inc; confirmed 1500=score threshold after get_slot_field5_score at asm L11267; high conf |

NEW CIDs to add to card_info.inc (25 named cards + 10 unallocated; HARPIE_LADY_SISTERS_CID removed, already exists):

Named (verify passcode against data/card-stats.s before finalizing):
```
LABYRINTH_WALL_CID          = 0x1114  @ Labyrinth Wall       (pw=67284908; slot=0x1114)
CYCLON_LASER_CID            = 0x1496  @ Cyclon Laser         (pw=05870978; slot=0x1496)
BUSTER_RANCHER_CID          = 0x159e  @ Buster Rancher       (slot=0x159E)
Y_DRAGON_HEAD_CID           = 0x15b0  @ Y-Dragon Head        (pw=68514277; slot=0x15B0)
Z_METAL_TANK_CID            = 0x15b3  @ Z-Metal Tank         (pw=64500000; slot=0x15B3)
DARK_BLADE_CID              = 0x15cd  @ Dark Blade           (slot=0x15CD)
DECAYED_COMMANDER_CID       = 0x15d0  @ Decayed Commander    (slot=0x15D0)
GIANT_ORC_CID               = 0x15d2  @ Giant Orc            (slot=0x15D2)
SECOND_GOBLIN_CID           = 0x15d3  @ Second Goblin        (slot=0x15D3)
VAMPIRE_ORCHIS_CID          = 0x15d4  @ Vampire Orchis       (slot=0x15D4)
DES_DENDLE_CID              = 0x15d5  @ Des Dendle           (slot=0x15D5)
BURNING_BEAST_CID           = 0x15d6  @ Burning Beast        (slot=0x15D6)
AITSU_CID                   = 0x160a  @ Aitsu                (slot=0x160A)
WHITE_MAGICIAN_PIKERU_CID   = 0x1757  @ White Magician Pikeru (slot=0x1757)
RITUAL_WEAPON_CID           = 0x17fb  @ Ritual Weapon        (slot=0x17FB)
CHU_SKE_MOUSE_FIGHTER_CID   = 0x185a  @ Chu-Ske the Mouse Fighter (slot=0x185A)
EHERO_SPARKMAN_CID          = 0x18a9  @ Elemental Hero Sparkman   (pw=20721928; slot=0x18A9)
LEGENDARY_BLACK_BELT_CID    = 0x18d0  @ Legendary Black Belt      (slot=0x18D0)
SOITSU_CID                  = 0x190b  @ Soitsu                (slot=0x190B)
INDOMITABLE_FIGHTER_LEI_LEI_CID = 0x1915  @ Indomitable Fighter Lei Lei (slot=0x1915)
EBON_MAGICIAN_CURRAN_CID    = 0x191d  @ Ebon Magician Curran      (pw=46128076; slot=0x191D)
DIVINE_SWORD_PHOENIX_BLADE_CID = 0x193a @ Divine Sword - Phoenix Blade (slot=0x193A)
V_TIGER_JET_CID             = 0x1947  @ V-Tiger Jet               (pw=51638941; slot=0x1947)
ADHESIVE_EXPLOSIVE_CID      = 0x19bd  @ Adhesive Explosive         (slot=0x19BD)
PETIT_MOTH_CID              = 0x10bc  @ Petit Moth                 (slot=0x10BC)
```

Note: PETIT_MOTH_CID (0x10bc) is in the named category;
confirm it is not already in card_info.inc under a different name before adding.
Note: HARPIE_LADY_SISTERS_CID (0x0fe5) already exists in card_info.inc -- removed from NEW section; EQ reuse at DAT_0804fc20 retained.

Unallocated CIDs (10; use cid_XXXX naming convention, low confidence, no card with that slot_id):
```
cid_10d4 = 0x10d4  @ unallocated slot_id; check_slot_card_eligible_by_card_id BST node
cid_10da = 0x10da  @ unallocated slot_id
cid_10e2 = 0x10e2  @ unallocated slot_id
cid_10e5 = 0x10e5  @ unallocated slot_id
cid_10ea = 0x10ea  @ unallocated slot_id
cid_10eb = 0x10eb  @ unallocated slot_id
cid_10ed = 0x10ed  @ unallocated slot_id
cid_10ee = 0x10ee  @ unallocated slot_id
cid_12c6 = 0x12c6  @ unallocated slot_id
cid_12ef = 0x12ef  @ unallocated slot_id
```

NEW non-CID scalar for Seg-6b:
```
FIELD5_SCORE_THRESHOLD_1299 = 0x00000513
```
Evidence: DAT_0804fc94=0x0513; used at asm L11140 after `bl get_slot_field5_score` in check_slot_card_eligible_by_card_id; `ldr r1,DAT_0804fc94 / b LAB_0804fca6` then `cmp r0,r1; bgt`. Value 1299 is a score bound, not a slot_id (no card_entry with slot=0x513 in card-stats.s). No matching constant found in constants/*.inc. Confidence: high.

### REF_SLOTS (USER-label + DATA-ref)

| slot | target | gas_label | slot_label |
|---|---|---|---|
| DAT_0804d254 | 0x0804d258 | sprite_row_anim_jump_table (USER label at PTR_DAT_0804d258) | sprite_row_anim_jt_ptr_s |
| DAT_0804dbb4 | 0x0804dbb8 | sprite_row_queue_jump_table (USER label at PTR_DAT_0804dbb8) | sprite_row_queue_jt_ptr_s |

Note: PTR_DAT_0804d258 and PTR_DAT_0804dbb8 are themselves the jump table bases. Their internal entries (raw ptrs into the ROM_INCBIN code) will be resolved by R4 disasm -- each target address gets a function label once disassembled.

### RENAME_SLOTS (rename-only + EOL)

Seg-6a scalars with no matching equate:

| slot | value | slot_label | eol |
|---|---|---|---|
| DAT_0804f1d0 | 0xfffffd00 | compact_rank3_stride_delta_s | stride delta -0x300; used in compact_equip_zone_rank3_entries to adjust write_ptr |
| DAT_0804f28c | 0xfffffb80 | compact_rank3_delta_b_s | -0x480 stride adjustment in phase 2 of compact_equip_zone_rank3_entries |

Note: DAT_0804f6c0 = 0x0000ffff reclassified EQ (SLOT_CARD_EMPTY in card_info.inc confirmed). Moved to EQ_SLOTS above (C5 fix #2).

Seg-6b inline state-code stubs: no literal pool slots (all immediates). No RENAME_SLOTS needed for check_card_state_code_eq_N functions.

### FUNC_RENAME (misnomer corrections)

None identified. All 24 function names are semantically consistent with their bodies:
- dispatch_sprite_row_anim_by_state: dispatches based on anim state code -- correct.
- advance_equip_zone_rank_state: 4-phase rank state machine for equip zone animation sequencing -- correct.
- check_equip_target_matches_card_owner: compares found target id with card owner+zone bits -- correct.
- return_zero_unconditional: leaf stub returning 0, called on non-match paths -- correct.
- switchD_0804ce98__caseD_1e/1f/3: continuation dispatch cases -- correct (will be revised when parent switch gets plate update).

### PLATE (R5; full rewrite or substring replacement; all ASCII)

Existing plates are verbose and correct. The switchD_ case functions (at 0x4d124, 0x4d14c, 0x4d1ca) are sub-cases of dispatch_card_eligibility_state_machine (in Seg-5). Their current plates reference the parent function by old auto-name or stale FUN_. Fixer must replace ALL occurrences of each stale FUN_xxxx string within asm/05_equip_eligibility_a.s (Seg-6 range L9000..L11700), not only the specific line numbers listed below. The line numbers are provided as confirmation evidence only; the authoritative action is grep-all-and-replace-all.

Pre-landing occurrence count (exhaustive grep `FUN_[0-9a-f]\{8\}` on L8945..L11663; fixer must verify each count == 0 after replacement):

Unique FUN_ addresses: 9 total; 13 total occurrences.

| stale FUN_ | current name | occurrences in Seg-6 (L8945..L11663) | locations |
|---|---|---|---|
| FUN_0804ce98 | dispatch_card_eligibility_state_machine | 0 (already replaced in asm) | (pre-emptive; grep before skipping) |
| FUN_0804d1e4 | dispatch_sprite_row_anim_by_state | 1 | L9128 (reset_sprite_row_queue_tail plate) |
| FUN_0804f2e0 | dispatch_equip_field_update_by_anim_state | 2 | L9047 (dispatch_sprite_row_anim_by_state plate), L9360 (flush_sprite_row_queue_partial plate) |
| FUN_0804f2ee | (bl site within dispatch_equip_field_update_by_anim_state) | 1 | L9047 (dispatch_sprite_row_anim_by_state plate; call-site rewrite) |
| FUN_0804f34c | advance_equip_zone_rank_state | 1 | L9047 (dispatch_sprite_row_anim_by_state plate) |
| FUN_0804f3da | (bl site within advance_equip_zone_rank_state) | 1 | L9047 (dispatch_sprite_row_anim_by_state plate; call-site rewrite) |
| FUN_0804f6c4 | check_slot_card_eligible_by_card_id | 4 | L11597, L11605, L11619, L11633 (check_card_state_code_eq_* and check_slot_zone_bit* plates) |
| FUN_08094cd4 | tick_equip_activation_main_sequence | 1 | L9629 (dispatch_equip_field_update_by_anim_state plate) |
| FUN_08053d88 | check_equip_slot_eligible_by_opposite_side_zone_chain | 1 | L10029 (check_equip_slot_eligible_triple_predicate plate) |
| FUN_08054d08 | check_equip_slot_eligible_by_whitelist_field7_and_zone_bit | 1 | L10166 (check_equip_slot_eligible_with_whitelist_and_type plate) |

Specific plate update actions (replace ALL occurrences of each stale string):
1. FUN_0804ce98 -> dispatch_card_eligibility_state_machine
   (grep asm/05_equip_eligibility_a.s; 0 occurrences confirmed at time of proposal -- switchD_ case plates already use current name; still run grep to confirm before skipping)
2. FUN_0804d1e4 -> dispatch_sprite_row_anim_by_state
   (1 occurrence: L9128 reset_sprite_row_queue_tail plate "Caller: FUN_0804d1e4 (batch-internal, terminal-state cleanup)")
3. FUN_0804f2e0 -> dispatch_equip_field_update_by_anim_state
   (2 occurrences: L9047 dispatch_sprite_row_anim_by_state plate "Callers: FUN_0804f2e0 ..."; L9360 flush_sprite_row_queue_partial plate "Caller: FUN_0804f2e0 (card_frame/duel_field/game_str)")
4. FUN_0804f34c -> advance_equip_zone_rank_state
   (1 occurrence: L9047 dispatch_sprite_row_anim_by_state plate, same Callers: line as #3)
5. FUN_0804f6c4 -> check_slot_card_eligible_by_card_id
   (4 occurrences: L11597/L11605/L11619/L11633 "In dispatch branch of FUN_0804f6c4 (card state hub)")
6. FUN_0804f2ee and FUN_0804f3da: replace with descriptive call-site references (not LAB_ labels)
   (1 occurrence each: L9047 dispatch_sprite_row_anim_by_state plate "Both known callers FUN_0804f2ee/FUN_0804f3da b after bl")
   These addresses are bl instruction sites within dispatch_equip_field_update_by_anim_state (0x0804f2ee)
   and advance_equip_zone_rank_state (0x0804f3da) respectively -- they are NOT LAB_ labels and no
   LAB_0804f2ee / LAB_0804f3da labels exist in asm. Rewrite the plate fragment to:
   "Both known call sites within dispatch_equip_field_update_by_anim_state (bl at 0x0804f2ee)
   and advance_equip_zone_rank_state (bl at 0x0804f3da) b after bl, so semantically void to caller."
7. FUN_08094cd4 -> tick_equip_activation_main_sequence
   (1 occurrence: L9629 dispatch_equip_field_update_by_anim_state plate
   "Called exclusively by FUN_08094cd4 (top-level equip field frame update)."
   -> "Called exclusively by tick_equip_activation_main_sequence (top-level equip field frame update).")
8. FUN_08053d88 -> check_equip_slot_eligible_by_opposite_side_zone_chain
   (1 occurrence: L10029 check_equip_slot_eligible_triple_predicate plate
   "Called by FUN_08053d88 (checks slot[+0xa] halfword before dispatching)."
   -> "Called by check_equip_slot_eligible_by_opposite_side_zone_chain (checks slot[+0xa] halfword before dispatching).")
9. FUN_08054d08 -> check_equip_slot_eligible_by_whitelist_field7_and_zone_bit
   (1 occurrence: L10166 check_equip_slot_eligible_with_whitelist_and_type plate
   "Called by FUN_08054d08 which continues with field7/zone_bit checks."
   -> "Called by check_equip_slot_eligible_by_whitelist_field7_and_zone_bit which continues with field7/zone_bit checks.")

Post-replacement verification: use exhaustive pattern to confirm zero residual FUN_ in Seg-6 range.
Any hit == replacement missed == do not proceed.

Grep commands for fixer:
- Pre-replacement scan (exhaustive; covers segment-internal + cross-module):
  `awk 'NR>=8945 && NR<=11663' asm/05_equip_eligibility_a.s | grep -oE "FUN_[0-9a-f]{8}" | sort | uniq -c`
  (expected: 9 unique addresses, 13 total occurrences as listed above)
- Post-replacement verification (exhaustive; must return 0 lines):
  `awk 'NR>=8945 && NR<=11663' asm/05_equip_eligibility_a.s | grep -E "FUN_[0-9a-f]{8}"`
  (0 results required; any hit = replacement incomplete = abort)

---

## Carve Plan (R7) -- rom.s incbin splitting

None in this segment. Both ROM_INCBIN blocks (0x4d294/0x862 and 0x4dd58/0x136a) contain THUMB code sub-handlers referenced only by the internal jump tables. They do not contain standalone data structures suitable for carve-style labels in rom.s. They are dispatched via raw ptr jump tables, not via bl from named callers in the wider ROM. Classification: R4 disasm.

---

## Disasm Plan (R4)

### Block 1: ROM_INCBIN 0x4d294, sz 0x862
- Parent dispatcher: dispatch_sprite_row_anim_by_state @ 0x0804d1e4
- Jump table: PTR_DAT_0804d258 @ 0x0804d258 (15 entries, raw ptrs, no THUMB+1)
- 14 unique THUMB sub-handler entry points:
  - 0x0804d294 (table[0], default/state-0 branch), 0x0804d2f0, 0x0804d458, 0x0804d4bc
  - 0x0804d548, 0x0804d5a8, 0x0804d634, 0x0804d7ac, 0x0804d7ee, 0x0804dab4, 0x0804daf6 (= reset_sprite_row_queue_tail already named)
  - 0x0804d868, 0x0804da52, 0x0804da9a
  - Note: 0x0804daf6 is already named reset_sprite_row_queue_tail (function at ROM_INCBIN boundary); the 13 entries inside the block need R4 disasm stubs each.
- Disasm approach: for each entry point in the block (exclusive of 0x0804daf6 which is already a function), apply DisassembleCommand(addr, THUMB). Must setTMode before disassembling; clearListing for full range first. Then assign stub labels:
  - dispatch_sprite_row_anim_case_0 @ 0x0804d294 (or state_init)
  - dispatch_sprite_row_anim_case_1 @ 0x0804d2f0
  - ... (13 case stubs total, named by table index)

### Block 2: ROM_INCBIN 0x4dd58, sz 0x136a
- Parent dispatcher: dispatch_sprite_row_queue_by_state @ 0x0804db50
- Jump table: PTR_DAT_0804dbb8 @ 0x0804dbb8 (104 entries)
- 12 unique THUMB sub-handler entry points (states 0..7 are distinct; states 8..103 default to 0x0804f0c2 = clear_sprite_row_queue_overflow_flag):
  - 0x0804dd58 (table[0]), 0x0804ddac, 0x0804de00, 0x0804de42, 0x0804deb8 (states 0-4)
  - 0x0804e900, 0x0804e9d0, 0x0804ea10 (states 5-7)
  - 0x0804ee74, 0x0804eee4, 0x0804ef1a, 0x0804f070 (states 8..100-range special, last 4 unique entries)
- Default target 0x0804f0c2 = clear_sprite_row_queue_overflow_flag (already named function after block end)
- Disasm approach: same -- clearListing(0x4dd58..0x4f0c2), setTMode, DisassembleCommand per entry point (not full range at once due to Ghidra single-stub limitation). Label each:
  - dispatch_sprite_row_queue_case_0 @ 0x0804dd58
  - dispatch_sprite_row_queue_case_1 @ 0x0804ddac
  - ... (12 stubs total)

---

## New Constants / Globals (if any; must verify no existing reuse)

### ewram.inc -- 7 new SPRITE_ROW offsets + 1 new global

```
@ === Sprite Row Queue / Anim subsystem (gDuelPhaseFlags+0x480..+0x49c) ===
@ Source: asm/05_equip_eligibility_a.s Seg-6a
.equ SPRITE_ROW_WRITE_PTR_OFF,       0x00000480  @ [gDuelPhaseFlags+0x480]: strh write ptr into row buffer
.equ SPRITE_ROW_COUNT_OFF,           0x00000488  @ [gDuelPhaseFlags+0x488]: row entry count (halfword)
.equ SPRITE_ROW_ANIM_STATE_OFF,      0x0000048c  @ [gDuelPhaseFlags+0x48c]: anim-active state flag (str)
.equ SPRITE_ROW_QUEUE_STATE_A_OFF,   0x00000490  @ [gDuelPhaseFlags+0x490]: queue phase-A state (cleared by flush)
.equ SPRITE_ROW_ANIM_CTL_OFF,        0x00000494  @ [gDuelPhaseFlags+0x494]: anim state code (0..0xe)
.equ SPRITE_ROW_QUEUE_ACTIVE_OFF,    0x00000498  @ [gDuelPhaseFlags+0x498]: queue active flag (str)
.equ SPRITE_ROW_QUEUE_STATE_OFF,     0x0000049c  @ [gDuelPhaseFlags+0x49c]: queue state code (0..0x67)

@ New global: equip zone rank state struct (EWRAM)
.equ gEquipZoneRankState,   0x0201e4d0  @ EWRAM base for equip zone rank state machine; advance_equip_zone_rank_state reads halfword [+0x14]
```

Verification:
- 0x480..0x49c: confirmed absent from ewram.inc (grep found no 0x480/0x488/0x48c/0x490/0x494/0x498/0x49c in ewram.inc)
- 0x0201e4d0: confirmed absent from ewram.inc (grep found gEquipZoneCountTable=0x0201e1c8 but not 0x0201e4d0)
- SPRITE_ROW_WRITE_PTR_OFF evidence: flush_sprite_row_queue_partial plate: "write_ptr at +0x480" (asm/05 L9361+); compact_equip_zone_rank3_entries plate: "DST_COUNT_OFFSET=0x90*8=0x480" (L9494); high conf
- SPRITE_ROW_COUNT_OFF evidence: flush_sprite_row_queue_partial: "count at +0x488" (L9361); compact: "SRC_LIST_OFFSET=0x91*8=0x488" (L9494); high conf
- SPRITE_ROW_ANIM_STATE_OFF evidence: dispatch_equip_field_update_by_anim_state: "anim_state_offset=0x48c" (L9629); advance_equip_zone_rank_state: "EQUIP_SPRITE_OFFSET_B=0x48c" (L9704); high conf
- SPRITE_ROW_QUEUE_ACTIVE_OFF evidence: dispatch_equip_field_update_by_anim_state: "queue_state_offset=0x498" (L9629); advance_equip_zone_rank_state: "ACTIVE_FLAG_OFFSET=0x93*8=0x498" (L9703); high conf
- gEquipZoneRankState evidence: advance_equip_zone_rank_state plate: "STRUCT_BASE=0x0201e4d0 (DAT_0804f368)" (L9701); only consumer in Seg-6a; high conf

### card_info.inc -- 25 named CIDs + 10 unallocated CIDs + 1 score threshold

Add to card_info.inc (after existing entries; group with equip-eligibility BST comment):

```
@ === Seg-6b: check_slot_card_eligible_by_card_id BST equip-target CIDs ===
@ Named cards (confirmed via data/card-stats.s slot_id match):
.equ PETIT_MOTH_CID,              0x000010bc  @ Petit Moth (slot=0x10BC); BST node
.equ LABYRINTH_WALL_CID,          0x00001114  @ Labyrinth Wall (slot=0x1114); BST node
.equ CYCLON_LASER_CID,            0x00001496  @ Cyclon Laser (slot=0x1496); BST node
.equ BUSTER_RANCHER_CID,          0x0000159e  @ Buster Rancher (slot=0x159E); BST node
.equ Y_DRAGON_HEAD_CID,           0x000015b0  @ Y-Dragon Head (slot=0x15B0); BST node
.equ Z_METAL_TANK_CID,            0x000015b3  @ Z-Metal Tank (slot=0x15B3); BST node
.equ DARK_BLADE_CID,              0x000015cd  @ Dark Blade (slot=0x15CD); BST node
.equ DECAYED_COMMANDER_CID,       0x000015d0  @ Decayed Commander (slot=0x15D0); BST node
.equ GIANT_ORC_CID,               0x000015d2  @ Giant Orc (slot=0x15D2); BST node
.equ SECOND_GOBLIN_CID,           0x000015d3  @ Second Goblin (slot=0x15D3); BST node
.equ VAMPIRE_ORCHIS_CID,          0x000015d4  @ Vampire Orchis (slot=0x15D4); BST node
.equ DES_DENDLE_CID,              0x000015d5  @ Des Dendle (slot=0x15D5); BST node
.equ BURNING_BEAST_CID,           0x000015d6  @ Burning Beast (slot=0x15D6); BST node
.equ AITSU_CID,                   0x0000160a  @ Aitsu (slot=0x160A); BST node
.equ WHITE_MAGICIAN_PIKERU_CID,   0x00001757  @ White Magician Pikeru (slot=0x1757); BST node
.equ RITUAL_WEAPON_CID,           0x000017fb  @ Ritual Weapon (slot=0x17FB); BST node
.equ CHU_SKE_MOUSE_FIGHTER_CID,   0x0000185a  @ Chu-Ske the Mouse Fighter (slot=0x185A); BST node
.equ EHERO_SPARKMAN_CID,          0x000018a9  @ Elemental Hero Sparkman (pw=20721928; slot=0x18A9); BST node
.equ LEGENDARY_BLACK_BELT_CID,    0x000018d0  @ Legendary Black Belt (slot=0x18D0); BST node
.equ SOITSU_CID,                  0x0000190b  @ Soitsu (slot=0x190B); BST node
.equ INDOMITABLE_FIGHTER_LEI_LEI_CID, 0x00001915 @ Indomitable Fighter Lei Lei (slot=0x1915); BST node
.equ EBON_MAGICIAN_CURRAN_CID,    0x0000191d  @ Ebon Magician Curran (pw=46128076; slot=0x191D); BST node
.equ DIVINE_SWORD_PHOENIX_BLADE_CID, 0x0000193a @ Divine Sword - Phoenix Blade (slot=0x193A); BST node
.equ V_TIGER_JET_CID,             0x00001947  @ V-Tiger Jet (pw=51638941; slot=0x1947); BST node
.equ ADHESIVE_EXPLOSIVE_CID,      0x000019bd  @ Adhesive Explosive (slot=0x19BD); BST node
@ Unallocated slot IDs used in BST (no card in card-stats.s with these slot_ids):
.equ cid_10d4,  0x000010d4  @ unallocated; BST node in check_slot_card_eligible_by_card_id
.equ cid_10da,  0x000010da  @ unallocated; BST node
.equ cid_10e2,  0x000010e2  @ unallocated; BST node
.equ cid_10e5,  0x000010e5  @ unallocated; BST node
.equ cid_10ea,  0x000010ea  @ unallocated; BST node
.equ cid_10eb,  0x000010eb  @ unallocated; BST node
.equ cid_10ed,  0x000010ed  @ unallocated; BST node
.equ cid_10ee,  0x000010ee  @ unallocated; BST node
.equ cid_12c6,  0x000012c6  @ unallocated; BST node
.equ cid_12ef,  0x000012ef  @ unallocated; BST node
@ Score threshold (not a CID):
.equ FIELD5_SCORE_THRESHOLD_1299,  0x00000513  @ field5 score upper bound; check_slot_card_eligible_by_card_id LAB_0804fc94; used after get_slot_field5_score comparison; value 1299 is a score bound not a slot_id
```

Pre-addition C5 dedup checks (must confirm before fixer adds):
- HARPIE_LADY_SISTERS_CID 0x0fe5: EXISTS in card_info.inc -- removed from NEW section (C5 fix #1).
- PETIT_MOTH_CID 0x10bc: not found in card_info.inc (grep showed no 0x10bc); add.
- LABYRINTH_WALL_CID 0x1114: not found; add. (Labyrinth Wall != Wall Shadow 0x1117)
- BURNING_BEAST_CID 0x15d6: not found; distinct from FREEZING_BEAST_CID 0x15d7; add.
- All other named CIDs: checked against full existing list -- none duplicate.

### demo_state.inc -- no changes needed

DEMO_CLEAR_BITS_8_1 = 0xfffffe01 is already defined at demo_state.inc L15. Reuse for 4 rank-field-mask slots in advance_equip_zone_rank_state. No new constant needed.

---

## Sect5.1 Registration (Rule 3) -- 0-reference blocks

None in Seg-6. Both ROM_INCBIN blocks have raw references (raw=1 each from their respective jump tables). No orphan data blocks found in 0x0804d124..0x0804ffba.

---

## Consumer Evidence (R6) -- key slot semantics with file:line + confidence

| slot/global | value | consumer evidence | confidence |
|---|---|---|---|
| SPRITE_ROW_ANIM_STATE_OFF | 0x48c | asm/05_equip_eligibility_a.s L9629: "anim_state_offset=0x48c"; L9704: "EQUIP_SPRITE_OFFSET_B=0x48c" | high |
| SPRITE_ROW_QUEUE_ACTIVE_OFF | 0x498 | asm/05 L9629: "queue_state_offset=0x498"; L9703: "ACTIVE_FLAG_OFFSET=0x93*8=0x498" | high |
| SPRITE_ROW_ANIM_CTL_OFF | 0x494 | asm/05 L9047: "state_offset=0x494 (0x92<<3)"; dispatch_sprite_row_anim_by_state reads [base+0x494] as state code | high |
| SPRITE_ROW_QUEUE_STATE_OFF | 0x49c | asm/05 L9176: "state_code_off=0x49c, limit=0x67"; dispatch_sprite_row_queue_by_state uses [base+0x49c] for index | high |
| SPRITE_ROW_WRITE_PTR_OFF | 0x480 | asm/05 L9361: "write_ptr at +0x480"; L9494: "DST_COUNT_OFFSET=0x90*8=0x480" | high |
| SPRITE_ROW_COUNT_OFF | 0x488 | asm/05 L9361: "count at +0x488"; L9494: "SRC_LIST_OFFSET=0x91*8=0x488" | high |
| gEquipZoneRankState | 0x0201e4d0 | asm/05 L9701: "STRUCT_BASE=0x0201e4d0 (DAT_0804f368)"; advance_equip_zone_rank_state reads [struct+0x14] halfword for rank field; sole consumer in this segment | high |
| DEMO_CLEAR_BITS_8_1 (rank reuse) | 0xfffffe01 | asm/05 L9705: "RANK_FIELD_MASK=0xfffffe01"; `ands r0,r2` before `orrs r0,r1` in advance_equip_zone_rank_state to clear bits[8:1] and OR in new rank | high |
| FIELD5_SCORE_THRESHOLD_1299 | 0x0513 | asm/05 L11140: DAT_0804fc94 used after `bl get_slot_field5_score`; `ldr r1,DAT_0804fc94; b LAB_0804fca6` then `cmp r0,r1; bgt`; no card with slot_id=0x513 in card-stats.s | high |
| CARD_STAT_LP_THRESHOLD_1500 | 0x05dc | asm/05 L11267: DAT_0804fd78 used in LP comparison path after score check; value 1500 matches existing CARD_STAT_LP_THRESHOLD_1500 in card_info.inc | high |
| DAT_0804f6c0 = 0xffff | sentinel | asm/05 L10268: check_equip_target_matches_card_owner: `ldr r0,DAT_0804f6c0; cmp r2,r0; beq LAB_0804f6b4` (returns 1 if no target found); matches SLOT_CARD_EMPTY usage | high |

---

## Help Needed (low-confidence semantics)

1. **DAT_0804f1d0 = 0xfffffd00 (-0x300)** in compact_equip_zone_rank3_entries: the plate says "stride_delta=-0x300" but the exact field semantics are unclear. The value is used as `adds r6,r4,r2` where r2=0xfffffd00 to walk backwards. No matching constant in any .inc file. No BLOCKED -- scalar RENAME with EOL is safe. Low conf on semantic name.

2. **DAT_0804f28c = 0xfffffb80 (-0x480)** in compact_equip_zone_rank3_entries: plate says "DELTA_STRIDE=0xfffffb80=-0x480". Used as `adds r6,r4,r2` for phase 2 compaction stride. No matching constant. Low conf on semantic name.

3. **PTR_DAT_0804d264**: This is one of the 15 entries in PTR_DAT_0804d258 (at offset 3, pointing to 0x0804d4bc which is a handler inside the ROM_INCBIN block). Ghidra auto-labeled it separately because the asm emits a separate `PTR_DAT_0804d264:` label at that address. After R4 disasm the target address will get a stub label. The PTR_DAT_0804d264 slot itself is just entry[3] of the same jump table -- it should merge into the table structure after disasm. No separate REF_SLOT needed; resolved by R4 disasm.

4. **check_slot_card_eligible_by_card_id LAB_0804fe9a code path**: uses gDuelFieldSlots+PLAYER_BLOCK_STRIDE to walk slots. The two slots DAT_0804fedc=0x868 and DAT_0804fee0=0x0201c510 at the tail of this function are the same PLAYER_BLOCK_STRIDE / gDuelFieldSlots constants. EQ plan above covers them. No issues.

---

## Executor Report: F05-Seg-6

- slots: EQ=~68 (Seg-6a; +1 DAT_0804f6c0 SLOT_CARD_EMPTY) + ~61 (Seg-6b) = ~129 total; RENAME=2 scalars (DAT_0804f6c0 reclassified EQ); FUNC_RENAME=0; PLATE=9 stale-FUN_ replace-all (FUN_0804ce98 0-hit pre-emptive + FUN_0804d1e4 x1 + FUN_0804f2e0 x2 + FUN_0804f34c x1 + FUN_0804f6c4 x4 + FUN_0804f2ee/f3da call-site rewrite x2 + FUN_08094cd4 x1 + FUN_08053d88 x1 + FUN_08054d08 x1; total 13 occurrences across 9 unique stale FUN_ addresses; exhaustive-grep pattern FUN_[0-9a-f]{8} confirms no further leakage)
- carve=0; disasm=2 ranges (0x4d294/0x862 + 0x4dd58/0x136a); sect5.1=0
- new constants/globals:
  - ewram.inc: SPRITE_ROW_WRITE_PTR_OFF/COUNT_OFF/ANIM_STATE_OFF/QUEUE_STATE_A_OFF/ANIM_CTL_OFF/QUEUE_ACTIVE_OFF/QUEUE_STATE_OFF (7 offsets) + gEquipZoneRankState
  - card_info.inc: 25 named CIDs + 10 cid_XXXX unallocated + FIELD5_SCORE_THRESHOLD_1299
  - demo_state.inc: none (DEMO_CLEAR_BITS_8_1 reused)
- help: 2 low-conf scalar semantics (DAT_0804f1d0/DAT_0804f28c stride deltas in compact_equip_zone_rank3_entries); both safe to RENAME with EOL
- proposal: doc/dev/refine/F05-Seg-6.proposal.md
