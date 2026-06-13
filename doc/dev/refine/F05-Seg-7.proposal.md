# Refine Proposal: F05-Seg-7  [0x0804ffba..0x08050e40)

## 段测绘

- 函数入口 (24):
  - 0x0804ffba  check_slot_zone_bit3_eligible
  - 0x0804ffd2  check_slot_zone_bit1_eligible
  - 0x0804ffea  check_slot_zone_bit2_eligible
  - 0x0804fffc  return_true_unconditional
  - 0x0805000c  check_equip_slot_eligible_by_card_id_and_prereqs
  - 0x08050038  check_equip_chain_type_d_node_exists
  - 0x080500ac  check_card_ptr_equippable_by_owner_bit
  - 0x080500c8  check_equip_slot_eligible_with_field6_score
  - 0x08050130  check_equip_slot_eligible_type_only
  - 0x0805018c  check_equip_slot_eligible_with_score_bound
  - 0x08050214  check_equip_slot_eligible_with_field6_and_pair
  - 0x080502b0  eval_equip_slot_score_by_card_state
  - 0x08050750  check_equip_slot_eligible_type_and_card_match
  - 0x080507ac  check_equip_slot_eligible_by_type_query
  - 0x08050810  check_equip_slot_eligible_by_prereqs_and_field_match
  - 0x0805086c  check_equip_slot_eligible_by_type_query_with_occupied
  - 0x080508cc  check_equip_slot_eligible_by_whitelist_query
  - 0x08050924  check_equip_slot_eligible_by_owner_path_split
  - 0x08050994  check_equip_slot_eligible_by_type_then_prereqs
  - 0x080509fc  check_equip_slot_eligible_by_prereqs_then_type
  - 0x08050a54  check_equip_slot_eligible_by_card_id_bst
  - 0x08050c58  check_equip_slot_eligible_with_bst_filter
  - 0x08050d78  check_equip_slot_eligible_with_whitelist_prereqs_0
  - 0x08050de4  check_equip_slot_eligible_with_whitelist_prereqs_1

- 残留自动名槽 (73 total; 1 PTR already named):
  - PTR_gP1LifePoints_08050510 = gP1LifePoints  [already named, skip]
  - 21x PLAYER_BLOCK_STRIDE slots (0x00000868): see EQ_SLOTS below
  - 20x gDuelFieldSlots slots (0x0201c510): see EQ_SLOTS below
  - 22x new CID slots: DAT_0805035c..DAT_08050d68 range
  - 6x reuse existing equates
  - 3x RENAME_SLOT (conflict/mask values)

- ROM_INCBIN / .byte 块: 0 (none in Seg-7; file 05 is pure code + literal pools)

## 数据块分类 (Rule 2/3) -- ref-scan 证据

No ROM_INCBIN or .byte data blocks in Seg-7. All data is function-internal literal pool
.word entries embedded within THUMB function bodies. No carve or disasm needed.

| 块 | ref-scan | 判定 | 理由 |
|---|---|---|---|
| N/A | N/A | N/A | No inter-function data blocks |

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

**Group A: PLAYER_BLOCK_STRIDE = 0x00000868 (reuse ewram.inc)**
21 slots all holding value 0x00000868 (ROM verified). Each is a literal pool copy
of the per-player EWRAM stride used in slot address calculation.

| slot | ROM addr | value | const_name | slot_label |
|---|---|---|---|---|
| DAT_08050094 | 0x08050094 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_chain_type_d_node_exists_stride |
| DWORD_08050120 | 0x08050120 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_field6_score_stride |
| DWORD_0805017c | 0x0805017c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_type_only_stride |
| DAT_08050204 | 0x08050204 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_score_bound_stride_a |
| DAT_080502a0 | 0x080502a0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_field6_and_pair_stride_a |
| DAT_08050354 | 0x08050354 | 0x00000868 | PLAYER_BLOCK_STRIDE | eval_equip_slot_score_by_card_state_stride_a |
| DAT_08050514 | 0x08050514 | 0x00000868 | PLAYER_BLOCK_STRIDE | eval_equip_slot_score_by_card_state_stride_b |
| DAT_080505c0 | 0x080505c0 | 0x00000868 | PLAYER_BLOCK_STRIDE | eval_equip_slot_score_by_card_state_stride_c |
| DWORD_0805079c | 0x0805079c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_type_and_card_match_stride |
| DAT_08050800 | 0x08050800 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_query_stride |
| DAT_0805085c | 0x0805085c | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_prereqs_and_field_match_stride |
| DAT_080508bc | 0x080508bc | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_query_with_occupied_stride |
| DAT_08050914 | 0x08050914 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_whitelist_query_stride |
| DAT_08050970 | 0x08050970 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_owner_path_split_stride |
| DAT_080509ec | 0x080509ec | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_type_then_prereqs_stride |
| DAT_08050a44 | 0x08050a44 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_prereqs_then_type_stride |
| DAT_08050ae0 | 0x08050ae0 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_by_card_id_bst_stride |
| DAT_08050c44 | 0x08050c44 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_bst_filter_stride_a |
| DAT_08050cb8 | 0x08050cb8 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_bst_filter_stride_b |
| DAT_08050dd4 | 0x08050dd4 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_whitelist_prereqs_0_stride |
| DAT_08050e30 | 0x08050e30 | 0x00000868 | PLAYER_BLOCK_STRIDE | check_equip_slot_eligible_with_whitelist_prereqs_1_stride |

**Group B: gDuelFieldSlots = 0x0201c510 (reuse ewram.inc)**
20 slots all holding 0x0201c510 (ROM verified). Each is a literal pool copy of the
duel field slots base address used to compute per-player per-slot EWRAM addresses.

| slot | ROM addr | value | const_name | slot_label |
|---|---|---|---|---|
| DAT_08050098 | 0x08050098 | 0x0201c510 | gDuelFieldSlots | check_equip_chain_type_d_node_exists_gdfs |
| DWORD_08050124 | 0x08050124 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_field6_score_gdfs |
| DWORD_08050180 | 0x08050180 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_type_only_gdfs |
| DAT_08050208 | 0x08050208 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_score_bound_gdfs_a |
| DAT_080502a4 | 0x080502a4 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_field6_and_pair_gdfs_a |
| DAT_08050358 | 0x08050358 | 0x0201c510 | gDuelFieldSlots | eval_equip_slot_score_by_card_state_gdfs_a |
| DAT_080505c4 | 0x080505c4 | 0x0201c510 | gDuelFieldSlots | eval_equip_slot_score_by_card_state_gdfs_b |
| DWORD_080507a0 | 0x080507a0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_type_and_card_match_gdfs |
| DAT_08050804 | 0x08050804 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_query_gdfs |
| DAT_08050860 | 0x08050860 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_prereqs_and_field_match_gdfs |
| DAT_080508c0 | 0x080508c0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_query_with_occupied_gdfs |
| DAT_08050918 | 0x08050918 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_whitelist_query_gdfs |
| DAT_08050974 | 0x08050974 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_owner_path_split_gdfs |
| DAT_080509f0 | 0x080509f0 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_type_then_prereqs_gdfs |
| DAT_08050a48 | 0x08050a48 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_prereqs_then_type_gdfs |
| DAT_08050ae4 | 0x08050ae4 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_by_card_id_bst_gdfs |
| DAT_08050c48 | 0x08050c48 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_bst_filter_gdfs_a |
| DAT_08050cbc | 0x08050cbc | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_bst_filter_gdfs_b |
| DAT_08050dd8 | 0x08050dd8 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_whitelist_prereqs_0_gdfs |
| DAT_08050e34 | 0x08050e34 | 0x0201c510 | gDuelFieldSlots | check_equip_slot_eligible_with_whitelist_prereqs_1_gdfs |

**Group C: Reuse existing equates (6 slots)**

| slot | ROM addr | value | const_name | source | slot_label |
|---|---|---|---|---|---|
| DAT_080500a0 | 0x080500a0 | 0xffff0000 | EQUIP_CHAIN_SENTINEL | duel_field.inc | check_equip_chain_type_d_node_exists_sentinel |
| DAT_08050518 | 0x08050518 | 0x0000ffff | SLOT_CARD_EMPTY | card_info.inc | eval_equip_slot_score_find_target_sentinel |
| DAT_080503b8 | 0x080503b8 | 0x000018c9 | ELEMENTAL_HERO_THUNDER_GIANT_CID | card_info.inc | eval_equip_slot_score_cid_thunder_giant |
| DAT_080503cc | 0x080503cc | 0x0000186a | BLAST_MAGICIAN_CID | card_info.inc | eval_equip_slot_score_cid_blast_magician |
| DAT_080503f8 | 0x080503f8 | 0x000019f1 | GREAT_SPIRIT_CID | card_info.inc | eval_equip_slot_score_cid_great_spirit |
| DAT_08050cc8 | 0x08050cc8 | 0x000012cb | SHIELD_AND_SWORD_CID | card_info.inc | check_equip_slot_eligible_with_bst_filter_cid_shield_sword |

Evidence: ROM byte reads at all 6 addresses match expected values (high confidence).
EQUIP_CHAIN_SENTINEL=0xffff0000 used in check_equip_chain_type_d_node_exists to test
node_exists return value (lsls r0,r0,#0x10 / cmp r0,r1). SLOT_CARD_EMPTY=0x0000ffff
used in eval_equip_slot_score_by_card_state: eors r0,r1 where r1=0xffff checks if
find_equip_target_for_card_slot returned the no-target sentinel.

**Group D: New CID equates (22 slots, all card_info.inc)**

All used in eval_equip_slot_score_by_card_state (0x080502b0) or check_equip_slot_eligible_by_card_id_bst
(0x08050a54) as card_id dispatch BST nodes. In eval_equip_slot_score_by_card_state, dispatch
variable r1 = ldrh [r7,#0] = card_ptr[+0] = equip card slot_id (halfword). ROM values verified.
Card names confirmed via card-stats.s slot_id lookup (high confidence for named cards).

Top-level BST in eval_equip_slot_score_by_card_state (0x080502b0 / func plate calls these "state_code
values" -- note: the BST key is actually card_ptr[+0] = card_id; state_code is secondary r2):

| slot | ROM addr | value | const_name (new) | card name |
|---|---|---|---|---|
| DAT_0805035c | 0x0805035c | 0x00001690 | INFERNALQUEEN_ARCHFIEND_CID | Infernalqueen Archfiend |
| DAT_08050360 | 0x08050360 | 0x000014c5 | THROWSTONE_UNIT_CID | Throwstone Unit |
| DAT_08050364 | 0x08050364 | 0x0000119a | DRAGON_SEEKER_CID | Dragon Seeker |
| DAT_08050368 | 0x08050368 | 0x000014b9 | WINGED_MINION_CID | Winged Minion |
| DAT_08050390 | 0x08050390 | 0x000015e4 | COMBINATION_ATTACK_CID | Combination Attack |
| DAT_080503bc | 0x080503bc | 0x000016ce | WILD_NATURES_RELEASE_CID | Wild Nature's Release |
| DAT_080503e8 | 0x080503e8 | 0x000019a9 | CYBER_LASER_DRAGON_CID | Cyber Laser Dragon |

BST in check_equip_slot_eligible_by_card_id_bst (0x08050a54):
Note: 0x14e0 (Dragon's Gunfire, 0xa7<<5), 0x123a, 0x1233, 0x1236 (Eternal Rest)
are computed at runtime via inline arithmetic -- no DAT_ literal pool slots for these.

| slot | ROM addr | value | const_name (new) | card name |
|---|---|---|---|---|
| DAT_08050ae8 | 0x08050ae8 | 0x00001304 | cid_1304 | unalloc (low-conf RENAME per CID rule) |
| DAT_08050b00 | 0x08050b00 | 0x0000123d | cid_123d | unalloc (low-conf RENAME) |
| DAT_08050b0c | 0x08050b0c | 0x0000123e | cid_123e | unalloc (low-conf RENAME) |
| DAT_08050b2c | 0x08050b2c | 0x0000161c | TRIBE_INFECTING_VIRUS_CID | Tribe-Infecting Virus |
| DAT_08050b30 | 0x08050b30 | 0x000014e4 | BURST_BREATH_CID | Burst Breath |
| DAT_08050b34 | 0x08050b34 | 0x00001305 | cid_1305 | unalloc (low-conf RENAME) |
| DAT_08050b40 | 0x08050b40 | 0x00001542 | NEEDLE_CEILING_CID | Needle Ceiling |
| DAT_08050b58 | 0x08050b58 | 0x00001945 | OJAMUSCLE_CID | Ojamuscle |
| DAT_08050b5c | 0x08050b5c | 0x0000166d | REALLY_ETERNAL_REST_CID | Really Eternal Rest |
| DAT_08050b68 | 0x08050b68 | 0x00001977 | WEED_OUT_CID | Weed Out |

BST in check_equip_slot_eligible_with_bst_filter (0x08050c58):
Note: 0x1840 (Triangle Ecstasy Spark, 0xc2<<5) computed inline, no DAT_ slot.

| slot | ROM addr | value | const_name (new) | card name |
|---|---|---|---|---|
| DAT_08050cc0 | 0x08050cc0 | 0x000017b3 | CURSE_OF_ANUBIS_CID | Curse of Anubis |
| DAT_08050cc4 | 0x08050cc4 | 0x000015df | ROULETTE_BARREL_CID | Roulette Barrel |
| DAT_08050cd4 | 0x08050cd4 | 0x000016e1 | ZERO_GRAVITY_CID | Zero Gravity |
| DAT_08050cf4 | 0x08050cf4 | 0x00001988 | BURST_RETURN_CID | Burst Return |
| DAT_08050d68 | 0x08050d68 | 0x000018a7 | EHERO_BURSTINATRIX_CID | Elemental Hero Burstinatrix |

### REF_SLOTS (USER-label + DATA-ref)

None. No RAM/ROM global pointer slots with non-PTR labels; PTR_gP1LifePoints_08050510 is
already named and correct (value 0x0201c4e0 = gP1LifePoints confirmed).

### RENAME_SLOTS (改名 + EOL)

3 slots that cannot be cleanly equated due to value collision or non-CID semantics:

| slot | ROM addr | value | slot_label | eol_ascii |
|---|---|---|---|---|
| DAT_0805009c | 0x0805009c | 0x00001281 | check_equip_chain_type_d_node_exists_state_a | equip chain type D active state; value 0x1281 also = RELINQUISHED_CID in card_info.inc (different domain) |
| DAT_08050d20 | 0x08050d20 | 0x00001cb8 | check_equip_slot_eligible_with_bst_filter_gdfs_off | gDuelFieldSlots offset to gEquipZoneCountTable (gDuelFieldSlots+0x1cb8=0x0201e1c8); differs from DUEL_ACTIVE_PLAYER_OFF which is gP1LifePoints relative |
| DAT_08050d40 | 0x08050d40 | 0x7f280000 | check_equip_slot_eligible_with_bst_filter_type_sentinel | low-conf sentinel used in TRIANGLE_ECSTASY_SPARK (0x1840) branch; slot[0]<<19 exact semantics not decoded |

Rationale:
- DAT_0805009c (0x1281): RELINQUISHED_CID=0x1281 exists in card_info.inc. C5 strict dedup
  forbids creating STATE_CODE_1281 at same value. Used as equip chain node state_code here
  (ldrh [slot+8] = state_code halfword, compared vs 0x1281 or 0x1284). Different semantic
  domain but same numeric value -> RENAME only. Evidence: asm/05 L15552 check_equip_chain_type_d_node_exists.
- DAT_08050d20 (0x1cb8): Used via add r0,r8 where r8=gDuelFieldSlots. Resolves to
  gDuelFieldSlots+0x1cb8=0x0201e1c8=gEquipZoneCountTable (ewram.inc). DUEL_ACTIVE_PLAYER_OFF=0x1cb8
  exists in duel_field.inc but is gP1LifePoints relative (different base, different address).
  Per C5 relaxed policy (different base = benign collision), a new constant would be valid,
  but single occurrence + confusion risk -> RENAME with EOL. Med-conf.
- DAT_08050d40 (0x7f280000): Used in cmp after lsls slot[0],#0x13 in TRIANGLE_ECSTASY_SPARK
  (0x1840) branch. Exact decomposition unclear: 0x7f280000 >> 19 = 0x0fe5, not 0x1840 directly.
  Not a CID sentinel in the standard card_id<<19 pattern. Low-conf; RENAME only with neutral label.

### FUNC_RENAME (误名订正)

None. All 24 functions in Seg-7 have semantically accurate names. No contradictions between
function body operations and function names detected.

Note: The plate comment of eval_equip_slot_score_by_card_state (0x080502b0) incorrectly
labels the BST dispatch keys as "state_code values" (they are card_id values from ldrh[r7+0]).
This is a plate prose issue, not a function rename. Correction: update plate wording to
"dispatches on equip card id (card_ptr[+0])..." during PLATE pass.

### PLATE (R5; substring FUN_ replacements)

2 functions with stale FUN_ references in plate text:

**check_equip_slot_eligible_by_card_id_and_prereqs (0x0805000c)**
- Plate substring: FUN_080538e8 -> check_equip_slot_eligible_by_type_and_chain
- Plate substring: FUN_080af120 -> find_best_equip_target_slot_scored
- Evidence: asm/05 L15466 plate. naming-proposals.csv confirms both names. ASCII check: pass.

**eval_equip_slot_score_by_card_state (0x080502b0)**
- Plate substring: FUN_0809078c -> count_zone_pair_hits_with_fn_ptr
- Evidence: asm/05 L15919 plate. naming-proposals.csv confirms name. ASCII check: pass.
- Also: correct "dispatches on known state_code values" -> "dispatches on equip card id (card_ptr[+0])"
  in plate text (substring replace to preserve rest of plate; the state_code r2 is used in
  sub-dispatch branches, not in the top-level BST key).

All plate text replacements are substring operations, no full rewrites needed (no CJK present).

## carve 计划 (R7)

None. No inter-function ROM_INCBIN blocks in Seg-7.

## disasm 计划 (R4)

None. No misidentified data blocks. No switchD_/switchdataD_ jump tables in Seg-7.
All code is properly disassembled.

## 新增 constants / 全局

**card_info.inc** -- 18 new named CID equates:
```
.equ INFERNALQUEEN_ARCHFIEND_CID,    0x00001690
.equ THROWSTONE_UNIT_CID,            0x000014c5
.equ DRAGON_SEEKER_CID,              0x0000119a
.equ WINGED_MINION_CID,              0x000014b9
.equ COMBINATION_ATTACK_CID,         0x000015e4
.equ WILD_NATURES_RELEASE_CID,       0x000016ce
.equ CYBER_LASER_DRAGON_CID,         0x000019a9
.equ TRIBE_INFECTING_VIRUS_CID,      0x0000161c
.equ BURST_BREATH_CID,               0x000014e4
.equ NEEDLE_CEILING_CID,             0x00001542
.equ OJAMUSCLE_CID,                  0x00001945
.equ REALLY_ETERNAL_REST_CID,        0x0000166d
.equ WEED_OUT_CID,                   0x00001977
.equ CURSE_OF_ANUBIS_CID,            0x000017b3
.equ ROULETTE_BARREL_CID,            0x000015df
.equ ZERO_GRAVITY_CID,               0x000016e1
.equ BURST_RETURN_CID,               0x00001988
.equ EHERO_BURSTINATRIX_CID,         0x000018a7
```

**card_info.inc** -- 4 unallocated CID equates (low-conf, neutral names per naming policy):
```
.equ cid_1304,    0x00001304   @ unallocated slot_id; BST root in check_equip_slot_eligible_by_card_id_bst
.equ cid_1305,    0x00001305   @ unallocated slot_id; BST node adjacent to cid_1304
.equ cid_123d,    0x0000123d   @ unallocated slot_id; BST node in check_equip_slot_eligible_by_card_id_bst
.equ cid_123e,    0x0000123e   @ unallocated slot_id; BST node adjacent to cid_123d
```

Pre-check grep results (all NOT found in existing constants/*.inc prior to proposal):
- 0x1690, 0x14c5, 0x119a, 0x14b9, 0x15e4, 0x16ce, 0x19a9: confirmed new
- 0x161c, 0x14e4, 0x1542, 0x1945, 0x166d, 0x1977: confirmed new
- 0x17b3, 0x15df, 0x16e1, 0x1988, 0x18a7: confirmed new
- 0x1304, 0x1305, 0x123d, 0x123e: confirmed new

Existing reused (already in card_info.inc):
- ELEMENTAL_HERO_THUNDER_GIANT_CID=0x18c9, BLAST_MAGICIAN_CID=0x186a, GREAT_SPIRIT_CID=0x19f1,
  SHIELD_AND_SWORD_CID=0x12cb

## §5.1 登记 (Rule 3) -- 0 引用块

None. No orphan data blocks in Seg-7. All code is reachable.

## 消费者证据 (R6) -- 关键槽语义

**check_equip_chain_type_d_node_exists (0x08050038)**
- Uses PTR_gP1LifePoints_08050510 (+0x40 offset reaches gDuelFieldSlots+0x10=0x0201c520)
  for slot address calculation. high-conf: explicit +0x40 arithmetic visible in asm L16246.
- Compares ldrh[slot+8] vs 0x1281 or 0x1284 (state_code). Evidence: L15552/15553/15534/15535.
  State_code 0x1281 is equip chain type D active state. high-conf from plate comment.

**eval_equip_slot_score_by_card_state (0x080502b0)**
- BST dispatch key = ldrh [r7,#0] = card_ptr[+0] = equip card's own card_id halfword.
  Evidence: asm/05 L16000 (ldrh r1,[r7,#0x0]) then BST compares vs DAT_ CID values.
  high-conf: pattern matches all other check_equip_slot_eligible_* functions in same segment.
- Callee via fn-ptr: DAT_08050ff4 holds 0x080502b1 (THUMB ptr). Indirect caller:
  count_zone_pair_hits_with_fn_ptr (0x0809078c). med-conf (indirection chain).

**check_equip_slot_eligible_by_card_id_bst (0x08050a54)**
- BST key = ldrh [r6,#0] = card_ptr[+0] = equip card slot_id. high-conf.
- 0x1236 (Eternal Rest) branch calls count_active_extended_chain_nodes.
  This matches known Eternal Rest effect (counts active equip chain nodes). high-conf.
- 0x1945 (Ojamuscle) branch calls check_card_id_is_effect_monster_type_c.
  Ojamuscle equips to Ojama types. high-conf.
- 0x1977 (Weed Out) branch calls eval_equip_chain_score_for_slot.
  Weed Out eliminates weakest ATK monster. high-conf.

**check_equip_slot_eligible_with_bst_filter (0x08050c58)**
- 0x12cb (Shield & Sword) branch reads gDuelFieldSlots+0x1cb8=gEquipZoneCountTable field,
  compares active player. Shield & Sword swaps ATK/DEF - player-ownership check makes sense.
  med-conf (indirect slot access pattern).
- 0x7f280000 sentinel: used in cmp after lsls slot[0],#0x13 in TRIANGLE_ECSTASY_SPARK (0x1840)
  branch. Exact decomposition unclear: 0x7f280000 >> 19 = 0x0fe5, not 0x1840 directly. low-conf.

## 求助

None. All semantics have sufficient evidence at med or high confidence.

The 4 unallocated CIDs (0x1304, 0x1305, 0x123d, 0x123e) are named neutrally per policy
(no card in card-stats.s assigned these slot_ids). Low-conf by definition.

The DAT_08050d20 (0x1cb8 as gDuelFieldSlots offset) interpretation as gEquipZoneCountTable
is med-conf based on ewram.inc address arithmetic (gDuelFieldSlots+0x1cb8=0x0201e1c8=gEquipZoneCountTable).
