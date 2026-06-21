# Refine Proposal: F10-Seg-7a  [0x08080ba0..0x08081900)

## 段测绘
- 范围: [0x08080ba0, 0x08081900), asm 行 14662..16793
- 函数入口 x9 (named):
  - 0x08080ba0  assemble_effect_slot_attr_with_zone_lookup  (line 14662)
  - 0x08080c3c  pack_effect_slot_attr_with_type_flags  (line 14749)
  - 0x08080c9c  enqueue_equip_slot_sprite_with_code_rotation  (line 14800)
  - 0x08080d28  pack_equip_slot_sprite_with_code_attr  (line 14872)
  - 0x08080d6c  read_effect_slot_side_and_type  (line 14907)
  - 0x08080d84  read_effect_slot_zone_type  (line 14930)
  - 0x08080d94  check_effect_slot_matches_zone_entry  (line 14947)
  - 0x08080e60  find_effect_slot_by_side_and_type  (line 15055)
  - 0x08080ea0  dispatch_equip_card_display_op_by_card_id  (line 15093)
    (BST hub with 28 named sub-stubs: dispatch_card_display_op_by_id_match + 27x trigger_card_display_op_0xNN,
     sub-stubs at 0x08081758..0x080818dc; all 33 named functions = 9 main + 24 sub-stubs + shared tail LAB)
- 残留自动名槽 x101:
  DAT_08080c28..DAT_08080ff0 (13 slots in first 4 fns)
  DWORD_08081008 (1)
  DAT_08081010..DAT_08081748 (83 slots in BST body)
  DAT_08081760..DAT_080818d4 (4 slots in named sub-stubs)
  = 101 total unique auto-name slots  [python count confirmed; corrected per review #A1/A2/A3/A4]
- ROM_INCBIN blocks: NONE in [0x80ba0, 0x81900)
- switchD: NONE in [0x80ba0, 0x81900)

## 数据块分类 (Rule 2/3)
No ROM_INCBIN or .byte blocks in this range.

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All 101 slots are literal-pool words in THUMB code. Classified by value:

**REUSE (constants already in inc files):**

| slot | value | const_name | inc_file | count |
|------|-------|-----------|---------|-------|
| DAT_08080c28 | 0x00000868 | PLAYER_BLOCK_STRIDE | duel_field.inc | 4x (c28/d18/e4c/b70) |
| DAT_08080c2c | 0x0201c510 | gDuelFieldSlots | ewram.inc | 4x (c2c/d1c/e50/b74) |
| DAT_08080c30 | 0xffffc01f | EFFECT_SLOT_TYPE_CLEAR_MASK | duel_field.inc | 2x (c30/c94) |
| DAT_08080c34 | 0x000010b1 | SLOT_FACE_STATUS_ARRAY_OFF | duel_field.inc | 2x (c34/e54) |
| DAT_08080c38 | 0xffff3fff | DEMO_CLEAR_BITS_15_14 | demo_state.inc | 2x (c38/c98) |
| DAT_08080d14 | 0xfffc7fff | DUAL_LABEL_RENDER_STATE_CLEAR | duel_field.inc | 3x (d14/d68/bf4) -- bf4 in 7b |
| DAT_08080d20 | 0x00001596 | SPIRIT_REAPER_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08080d24 | 0x00001598 | REAPER_ON_NIGHTMARE_CID | card_info.inc | 1x |
| DAT_08080f14 | 0xfffffe00 | STACK_ALLOC_NEG_512 | duel_field.inc | 1x (NEW -- see §新增) |
| DAT_08080f18 | 0x000015a8 | RAIGEKI_BREAK_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08080f1c | 0x000013ab | JOWLS_OF_DARK_DEMISE_CID | card_info.inc | 1x |
| DAT_08080f20 | 0x00001103 | SPELLBINDING_CIRCLE_CID | card_info.inc | 1x |
| DAT_08080f3c | 0x00001086 | TRAP_MASTER_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08080f68 | 0x0000119b | MAN_EATER_BUG_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08080f7c | 0x000011c3 | HANE_HANE_CID | card_info.inc | 1x |
| DAT_08080fb4 | 0x0000128a | cid_128a | -- | 1x (neutral: unassigned slot, not in card-stats.s) |
| DAT_08080fd0 | 0x00001281 | RELINQUISHED_CID | card_info.inc | 1x |
| DAT_08080ff0 | 0x00001298 | CYBER_RAIDER_CID | card_info.inc | 1x |
| DWORD_08081008 | 0x000012bb | COPYCAT_CID | card_info.inc | 1x |
| DAT_08081010 | 0x000012c3 | BRAIN_CONTROL_CID | card_info.inc | 1x |
| DAT_08081058 | 0x0000132a | THE_RELIABLE_GUARDIAN_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081074 | 0x000012f1 | REINFORCEMENTS_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080810a0 | 0x00001322 | SNATCH_STEAL_CID | card_info.inc | 1x |
| DAT_080810b4 | 0x00001326 | cid_1326 | -- | 1x (neutral: unassigned slot, not in card-stats.s) |
| DAT_080810e4 | 0x00001362 | MAGICAL_HATS_CID | card_info.inc | 1x |
| DAT_080810f4 | 0x0000134d | DRIVING_SNOW_CID | card_info.inc | 1x |
| DAT_08081118 | 0x0000137c | DUST_TORNADO_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_0808112c | 0x0000138d | RING_OF_DESTRUCTION_CID | card_info.inc | 1x |
| DAT_08081134 | 0x0000139e | KRYUEL_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081180 | 0x000014c3 | DOUBLE_SNARE_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081198 | 0x000013f0 | MASK_OF_DISPEL_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080811c8 | 0x0000142e | THOUSAND_KNIVES_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080811f8 | 0x0000148d | COLLECTED_POWER_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081210 | 0x00001485 | AQUA_SPIRIT_CID | card_info.inc | 1x |
| DAT_08081234 | 0x000014ac | VISER_DES_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081248 | 0x000014b9 | WINGED_MINION_CID | card_info.inc | 1x |
| DAT_08081250 | 0x000014bb | RYU_KISHIN_CLOWN_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081284 | 0x00001514 | BLAST_WITH_CHAIN_CID | card_info.inc | 1x |
| DAT_0808129c | 0x000014ce | DRAGON_MANIPULATOR_CID | card_info.inc | 1x |
| DAT_080812b8 | 0x000014eb | COLLAPSE_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080812d4 | 0x00001503 | OTOHIME_CID | card_info.inc | 1x |
| DAT_080812dc | 0x00001511 | SECRET_OF_THE_BANDIT_CID | card_info.inc | 1x |
| DAT_08081304 | 0x00001579 | MONSTER_RELIEF_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081314 | 0x00001538 | BOOK_OF_MOON_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081330 | 0x00001581 | ENEMY_CONTROLLER_CID | card_info.inc | 1x |
| DAT_0808134c | 0x0000158d | GRAVEKEEPERS_ASSAILANT_CID | card_info.inc | 1x |
| DAT_0808135c | 0x0000158e | A_MAN_WITH_WDJAT_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080813ac | 0x000017f6 | INFERNO_FIRE_BLAST_CID | card_info.inc | 1x |
| DAT_080813b0 | 0x0000169b | CHECKMATE_CID | card_info.inc | 1x |
| DAT_080813c8 | 0x000015d7 | FREEZING_BEAST_CID | card_info.inc | 1x |
| DAT_080813e4 | 0x000015fa | YZ_TANK_DRAGON_CID | card_info.inc | 1x |
| DAT_080813f4 | 0x000015ff | DIFFUSION_WAVE_MOTION_CID | card_info.inc | 1x |
| DAT_0808141c | 0x0000166f | SOUL_TAKER_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_0808142c | 0x0000164b | GUARDIAN_CEAL_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081448 | 0x00001685 | DARK_SCORPION_GORG_THE_STRONG_CID | card_info.inc | 1x |
| DAT_0808145c | 0x00001694 | TSUKUYOMI_CID | card_info.inc | 1x |
| DAT_0808146c | 0x0000169a | FALLING_DOWN_CID | card_info.inc | 1x |
| DAT_080814a0 | 0x0000171a | COMPULSORY_EVACUATION_DEVICE_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080814b0 | 0x000016ba | GALE_LIZARD_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080814cc | 0x000016e3 | ENERGY_DRAIN_CID | card_info.inc | 1x |
| DAT_080814e4 | 0x00001708 | ORCA_MEGA_FORTRESS_OF_DARKNESS_CID | card_info.inc | 1x |
| DAT_08081514 | 0x00001773 | SHIELD_CRASH_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081524 | 0x00001753 | ARCANE_ARCHER_OF_THE_FOREST_CID | card_info.inc | 1x |
| DAT_08081540 | 0x0000179f | ORDER_TO_CHARGE_CID | card_info.inc | 1x |
| DAT_08081554 | 0x000017da | ARMED_DRAGON_LV5_CID | card_info.inc | 1x |
| DAT_0808159c | 0x000018c9 | ELEMENTAL_HERO_THUNDER_GIANT_CID | card_info.inc | 1x |
| DAT_080815b4 | 0x0000183f | HARPIES_HUNTING_GROUND_CID | card_info.inc | 1x |
| DAT_080815d0 | 0x0000185f | GRANMARG_THE_ROCK_MONARCH_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080815e0 | 0x00001863 | CATNIPPED_KITTY_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081610 | 0x00001893 | OVERPOWERING_EYE_CID | card_info.inc | 1x |
| DAT_08081620 | 0x0000188a | ASSAULT_ON_GHQ_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081644 | 0x000018be | WHITE_NINJA_CID | card_info.inc | 1x |
| DAT_0808165c | 0x000018c2 | CHARMER_RANGE_MAX_CID | card_info.inc | 1x |
| DAT_08081698 | 0x00001957 | ELEMENTAL_HERO_TEMPEST_CID | card_info.inc | 1x |
| DAT_080816a8 | 0x000018f0 | PATROID_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_080816c8 | 0x0000192b | A_RIVAL_APPEARS_CID | card_info.inc | 1x |
| DAT_080816e4 | 0x00001945 | OJAMUSCLE_CID | card_info.inc | 1x |
| DAT_080816f0 | 0x00001953 | VW_TIGER_CATAPULT_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081718 | 0x000019ab | HERO_HEART_CID | card_info.inc | 1x |
| DAT_0808172c | 0x000019a3 | URIA_LORD_CID | card_info.inc | 1x |
| DAT_08081748 | 0x000019db | KARMA_CUT_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081760 | 0x000019dd | GENERATION_SHIFT_CID | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081774 | 0x000013ea | GAP_CID_13EA | card_info.inc | 1x |
| DAT_08081788 | 0x00000119 | EQUIP_DISP_OP_ID_0x119 | duel_field.inc | 2x (7788/8c4) (NEW -- see §新增) |
| DAT_080817bc | 0x000001f5 | HANE_HANE_INTERNAL_ID_0x1f5 | card_info.inc | 1x (NEW -- see §新增) |
| DAT_08081838 | 0x00000fbc | SUMMONED_SKULL_CID | card_info.inc | 1x |
| DAT_08081874 | 0x000013c7 | REVIVAL_JAM_CID | card_info.inc | 1x |
| DAT_08081880 | 0x00000127 | cid_127 | -- | 2x (880/8a0) (neutral: unassigned slot, not in card-stats.s) |
| DAT_08081884 | 0x00001414 | GRADIUS_CID | card_info.inc | 1x |
| DAT_080818a0 | 0x00000127 | cid_127 | -- | 1x (neutral: same as DAT_08081880; dedup) |
| DAT_080818a4 | 0x00000ff8 | RED_EYES_B_DRAGON_CID | card_info.inc | 1x |
| DAT_080818c4 | 0x00000119 | EQUIP_DISP_OP_ID_0x119 | duel_field.inc | 1x (dedup with DAT_08081788) |
| DAT_080818d4 | 0x00000125 | cid_125 | -- | 1x (neutral: unassigned slot, not in card-stats.s) |

Notes on special EQ values:
- 0xffffc01f: appears 2x (c30/c94); context = TYPE_MASK used to clear equip type field bits in zone attr computation. NEW const EFFECT_SLOT_TYPE_CLEAR_MASK in duel_field.inc. C5 grep 0xffffc01f = 0 hits in constants (confirmed).
- 0xffff3fff: DEMO_CLEAR_BITS_15_14 in demo_state.inc. REUSE (same semantic: clear bits[15:14]). C5: grep confirmed present.
- 0xfffc7fff: 3 uses total (d14, d68 in 7a; bf4 in 7b). REUSE DUAL_LABEL_RENDER_STATE_CLEAR (duel_field.inc). C5: grep confirmed present. No new constant created.
- 0xfffffe00: sub sp,#0x200 = allocate 512B stack frame for dispatch_equip_card_display_op_by_card_id. Context: `ldr r4, DAT_08080f14; add sp,r4` (add negative = sub). NEW const STACK_ALLOC_NEG_512. C5: 0 hits.
- 0x00000119: display op sub-id 0x119 = literal pool, used as `movs r2,r2` then b tail. 2 refs. NEW const EQUIP_DISP_OP_ID_0x119. Context: trigger_card_display_op_0x119 desc says "SUB_ID=0x119 exceeds 8-bit immediate range". Evidence: line 16748. C5: 0 hits.
- 0x000001f5: internal_id for Hane-Hane card name lookup (card_name_lookup_by_internal_id call at line 16657 with icid=0x1f5). Context: trigger_card_display_op_with_card_name_0x6c desc. NEW const. C5: 0 hits.
- 0x0000128a: not in card-stats.s (Skull Stalker actual slot=0x1088). Neutral label: cid_128a. EOL: "equip BST unassigned slot".
- 0x00001326: not in card-stats.s (Call of the Haunted actual slot=0x137d). Neutral label: cid_1326. EOL: "equip BST unassigned slot".
- 0x00000127: not in card-stats.s (Toon Summoned Skull actual slot=0x127f; Garma Sword Oath actual slot=0x125f). Neutral label: cid_127 for 0x127; cid_125 for 0x125. Both EOL: "equip BST unassigned slot".

**RENAME_SLOTS (label only, no new equate; literal pool value is raw):**

DAT_08081948 is 0x080905e9 (set_equip_activation_state_by_mode_alt+1), address 0x08081948 >= 0x08081900 -- this slot is in Seg-7b range, NOT 7a. Removed from 7a proposal per review #A4.

No RENAME_SLOTS in 7a range.

**DWORD_08081008:** No RENAME. This slot (value 0x000012bb = COPYCAT_CID) is handled as EQ_SLOT (REUSE COPYCAT_CID). No separate rename needed; the DWORD_ auto-name is resolved by the equate.

### REF_SLOTS (USER-label + DATA-ref)

No ROM_INCBIN base labels needed in 7a (no ROM_INCBIN blocks). No fn-ptr slots with THUMB+1 requiring REF_SLOTS in 7a range.

### FUNC_RENAME (misname corrections)
None detected. All 9 named functions in [0x80ba0, 0x81900) have plate descriptions consistent with function bodies. Evidence: plates match code structure (verified by reading lines 14655-16793).

### PLATE (R5; ASCII rewrites)

Mojibake found: **0 lines** in [0x80ba0, 0x81900). (All 14 mojibake lines are in 7b range.)

**C8 stale FUN_ plate fixes in 7a** (FUN_ names used in plate text that now have real names):
1. Line 14657: `FUN_08080c9c` -> `enqueue_equip_slot_sprite_with_code_rotation`
   (plate of assemble_effect_slot_attr_with_zone_lookup)
   setPlateComment("Called by enqueue_equip_slot_sprite_with_code_rotation after enqueue_equip_slot_sprite_by_player to update effect_node slot attribute.")
   Evidence: line 14657, fn at 0x08080c9c named enqueue_equip_slot_sprite_with_code_rotation.
2. Line 14744: `FUN_08080d28` -> `pack_equip_slot_sprite_with_code_attr`
   (plate of pack_effect_slot_attr_with_type_flags)
   Evidence: line 14744, fn at 0x08080d28 named pack_equip_slot_sprite_with_code_attr.

**Cross-file C8 stale FUN_ fix:**
3. asm/15_equip_target_summon_zoom.s line 2835: `FUN_08080c9c` -> `enqueue_equip_slot_sprite_with_code_rotation`
   Note: asm/all.s also has stale refs but is a derived file (auto-regenerated).

**Plates for sub-stub fns** (dispatch_equip_card_display_op_by_card_id hub and trigger_* fns):
Plates already contain full ASCII descriptions. No mojibake.
However multiple stale FUN_ in sub-stub plates:
- Lines 16407/16430/16450/...: `FUN_08080ea0` -> `dispatch_equip_card_display_op_by_card_id`
- Line 16407: `FUN_080817c8` -> `trigger_card_display_op_0x6f`
- Line 16407: `FUN_080818dc` -> `trigger_card_display_op_0x112`
Total C8 in 7a: ~29 occurrences of FUN_08080ea0 etc. across sub-stub plates. Fixer performs substring replace for each addr.

## carve 计划 (R7) -- 无
No ROM_INCBIN blocks in 7a. No carve needed.

## disasm 计划 (R4) -- 无
No ROM_INCBIN blocks in 7a needing disassembly. The dispatch_equip_card_display_op_by_card_id BST body (0x80ea0..0x81757) is fully decoded THUMB code already in asm file with LAB_ labels.

## 新增 constants (必须先证明现有 inc 无可复用)

**card_info.inc additions (truly NEW; C5 confirmed 0 hits by value in all constants/*.inc):**
- SPIRIT_REAPER_CID = 0x00001596  (Spirit Reaper pw=23205979; card-stats.s slot=0x1596)
- RAIGEKI_BREAK_CID = 0x000015a8  (Raigeki Break pw=04178474; card-stats.s slot=0x15a8)
- TRAP_MASTER_CID = 0x00001086  (Trap Master pw=46461247; card-stats.s slot=0x1086)
- MAN_EATER_BUG_CID = 0x0000119b  (Man-Eater Bug pw=54652250; card-stats.s slot=0x119b)
- THE_RELIABLE_GUARDIAN_CID = 0x0000132a  (The Reliable Guardian pw=16430187; card-stats.s card_0721 slot=0x132a)
- REINFORCEMENTS_CID = 0x000012f1  (Reinforcements pw=17814387; card-stats.s slot=0x12f1)
- DUST_TORNADO_CID = 0x0000137c  (Dust Tornado pw=60082869; card-stats.s slot=0x137c)
- KRYUEL_CID = 0x0000139e  (Kryuel pw=82642348; card-stats.s slot=0x139e)
- MASK_OF_DISPEL_CID = 0x000013f0  (Mask of Dispel pw=20765952; card-stats.s slot=0x13f0)
- THOUSAND_KNIVES_CID = 0x0000142e  (Thousand Knives pw=63391643; card-stats.s slot=0x142e)
- COLLECTED_POWER_CID = 0x0000148d  (Collected Power pw=07565547; card-stats.s slot=0x148d)
- VISER_DES_CID = 0x000014ac  (Viser Des pw=56043446; card-stats.s slot=0x14ac)
- RYU_KISHIN_CLOWN_CID = 0x000014bb  (Ryu-Kishin Clown pw=42647539; card-stats.s slot=0x14bb)
- DOUBLE_SNARE_CID = 0x000014c3  (Double Snare pw=03682106; card-stats.s slot=0x14c3)
- COLLAPSE_CID = 0x000014eb  (Collapse pw=55713623; card-stats.s slot=0x14eb)
- BOOK_OF_MOON_CID = 0x00001538  (Book of Moon pw=14087893; card-stats.s slot=0x1538)
- MONSTER_RELIEF_CID = 0x00001579  (Monster Relief pw=37507488; card-stats.s slot=0x1579)
- A_MAN_WITH_WDJAT_CID = 0x0000158e  (A Man with Wdjat pw=51351302; card-stats.s slot=0x158e)
- SOUL_TAKER_CID = 0x0000166f  (Soul Taker pw=81510157; card-stats.s slot=0x166f)
- GUARDIAN_CEAL_CID = 0x0000164b  (Guardian Ceal pw=10755153; card-stats.s card_1316 slot=0x164b)
- GALE_LIZARD_CID = 0x000016ba  (Gale Lizard pw=77491079; card-stats.s slot=0x16ba)
- COMPULSORY_EVACUATION_DEVICE_CID = 0x0000171a  (Compulsory Evacuation Device pw=94192409; card-stats.s slot=0x171a)
- SHIELD_CRASH_CID = 0x00001773  (Shield Crash pw=30683373; card-stats.s slot=0x1773)
- GRANMARG_THE_ROCK_MONARCH_CID = 0x0000185f  (Granmarg the Rock Monarch pw=60229110; card-stats.s slot=0x185f)
- CATNIPPED_KITTY_CID = 0x00001863  (Catnipped Kitty pw=96501677; card-stats.s slot=0x1863)
- ASSAULT_ON_GHQ_CID = 0x0000188a  (Assault on GHQ pw=62633180; card-stats.s slot=0x188a)
- PATROID_CID = 0x000018f0  (Patroid pw=71930383; card-stats.s slot=0x18f0)
- VW_TIGER_CATAPULT_CID = 0x00001953  (VW-Tiger Catapult pw=58859575; card-stats.s slot=0x1953)
- KARMA_CUT_CID = 0x000019db  (Karma Cut pw=71587526; card-stats.s slot=0x19db)
- GENERATION_SHIFT_CID = 0x000019dd  (Generation Shift pw=34460219; card-stats.s slot=0x19dd)
- HANE_HANE_INTERNAL_ID_0x1f5 = 0x000001f5  (internal lookup ID 0x1f5 passed to card_name_lookup_by_internal_id for Hane-Hane display; line 16523/16657)

**duel_field.inc additions (truly NEW; C5 confirmed 0 hits by value):**
- EFFECT_SLOT_TYPE_CLEAR_MASK = 0xffffc01f  (clear bits[13:5] for equip type field in zone attr; 2x refs in 7a: c30/c94)
- STACK_ALLOC_NEG_512 = 0xfffffe00  (add sp,r4 pattern for -0x200 stack alloc; 1x ref in dispatch_equip_card_display_op_by_card_id)
- EQUIP_DISP_OP_ID_0x119 = 0x00000119  (display op sub-id 0x119; 2x refs: DAT_08081788/DAT_080818c4; exceeds 8-bit immediate)

**Neutral CID labels (not in card-stats.s; added as equates with neutral names):**
- cid_128a  (0x0000128a: equip BST unassigned slot; Skull Stalker actual slot=0x1088)
- cid_1326  (0x00001326: equip BST unassigned slot; Call of the Haunted actual slot=0x137d)
- cid_127   (0x00000127: equip BST unassigned slot; Toon Summoned Skull actual slot=0x127f; 2x refs: 880/8a0)
- cid_125   (0x00000125: equip BST unassigned slot; Garma Sword Oath actual slot=0x125f)

**NOT created (corrected from earlier draft):**
- DISPLAY_CODE_CLEAR_MASK: REUSE DUAL_LABEL_RENDER_STATE_CLEAR (duel_field.inc) instead.
- SKULL_STALKER_CID, CALL_OF_HAUNTED_CID, TOON_SUMMONED_SKULL_CID, GARMA_SWORD_OATH_CID: slots not in card-stats.s; use neutral cid_NNN names.
- DARK_SNAKE_SYNDROME_CID, LIGHTNING_VORTEX_CID, etc.: values already exist in card_info.inc under different names (see #D correction table in review).

## §5.1 登记 (Rule 3)
No 0-reference blocks in 7a.

## 消费者证据 (R6) -- 关键槽语义
- 0xffffc01f (EFFECT_SLOT_TYPE_CLEAR_MASK): assemble_effect_slot_attr_with_zone_lookup line 14697 `ldr r2, DAT_08080c30; ands r6,r2` then `orrs r6,r1` for zone_type bits [confidence: high]
- 0xffff3fff (DEMO_CLEAR_BITS_15_14): line 14708 `ldr r2, DAT_08080c38; ands r6,r2` for direction bit[14] clear [confidence: high]
- 0xfffc7fff (DUAL_LABEL_RENDER_STATE_CLEAR): line 14861 `ldr r0, DAT_08080d14; ands r0,r2` clears bits[17:15] for display_code rotation field [confidence: high; Seg-6 uses same value for display code field in enqueue_equip_slot_sprite functions]
- 0xfffffe00 (STACK_ALLOC_NEG_512): line 15095-15096 `ldr r4, DAT_08080f14; add sp,r4` = allocate 512B stack buffer [confidence: high; dispatch_equip_card_display_op_by_card_id comment confirms "SP_FRAME=0x200"]
- 0x000001f5 (HANE_HANE_INTERNAL_ID_0x1f5): DAT_080817bc = 0x000001f5, used at line 16523 in trigger_card_display_op_with_card_name_0x6c plate: `icid=0x1f5` for Hane-Hane name lookup. Evidence: plate comment line 16516 says "looks up card name string by internal ID icid=0x1f5"; asm line 16523 `ldr r2, DAT_080817bc` with value 0x1f5 [confidence: high].
- 0x00000fbc (SUMMONED_SKULL_CID): DAT_08081838=0x0fbc; REUSE from card_info.inc [confidence: high].

## C13 残留 100% 覆盖 (Seg-7a)

Python count of unique auto-name slots with addresses in [0x8080ba0, 0x8081900): **101 slots**

Partition (corrected per review):
- EQ_SLOTS: 101 slots total
  - 93 primary rows explicit in the EQ table above
  - 8 secondary occurrences implied by multi-count notations:
    * PLAYER_BLOCK_STRIDE 4x: DAT_08080d18, DAT_08080e4c, DAT_08081b70 (3 additional; c28 = primary)
    * gDuelFieldSlots 4x: DAT_08080d1c, DAT_08080e50, DAT_08081b74 (3 additional; c2c = primary)
    * SLOT_FACE_STATUS_ARRAY_OFF 2x: DAT_08080e54 (1 additional; c34 = primary)
    * DUAL_LABEL_RENDER_STATE_CLEAR: DAT_08080d68 (1 additional in 7a; d14 = primary; bf4 is 7b)
  - Total: 93 + 8 = 101 unique auto-name slots in [0x8080ba0, 0x8081900)
- RENAME_SLOTS: 0 (DAT_08081948 removed; belongs to Seg-7b per review #A4)
- REF_SLOTS: 0

All 101 slots at addresses [0x8080ba0, 0x8081900) are covered. 0 residual DAT_/DWORD_ after fixer runs.

Correction notes applied from review:
- #A1: DAT_08080c94 added (EFFECT_SLOT_TYPE_CLEAR_MASK, same as c30)
- #A2: DAT_08080c98 added (DEMO_CLEAR_BITS_15_14, same as c38)
- #A3: DAT_080818a0 added (cid_127, same as DAT_08081880)
- #A4: DAT_08081948 removed (Seg-7b range, address >= 0x08081900)
- #B1: DAT_08080fb4 (0x128a) -> cid_128a (neutral, not SKULL_STALKER_CID)
- #B2: DAT_080810b4 (0x1326) -> cid_1326 (neutral, not CALL_OF_HAUNTED_CID)
- #C1: DAT_08081880/080818a0 (0x127) -> cid_127 (neutral, not TOON_SUMMONED_SKULL_CID)
- #C2: DAT_080818d4 (0x125) -> cid_125 (neutral, not GARMA_SWORD_OATH_CID)
- #D-all: 43 REUSE names corrected to actual card_info.inc names (see EQ table above)
- #D-spec1: DAT_08081058 (0x132a) -> THE_RELIABLE_GUARDIAN_CID (truly NEW, not REUSE)
- #D-spec2: DAT_0808142c (0x164b) -> GUARDIAN_CEAL_CID (truly NEW, not REUSE)
- #E1: DAT_08080d14/d68 (0xfffc7fff) -> DUAL_LABEL_RENDER_STATE_CLEAR (REUSE, not new DISPLAY_CODE_CLEAR_MASK)
- #F1: DWORD_08081008 (0x12bb) -> COPYCAT_CID (EQ REUSE, no RENAME)

**Note for fixer:** Process EQ_SLOTS in batches grouped by inc file. Neutral cid_NNN equates go in card_info.inc with EOL "equip BST unassigned slot".
