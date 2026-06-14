# Refine Proposal: F08-Seg-1  [0x080643e0..0x0806544c)

## 段测绘

- 函数入口 x10 (含多个 inline fragment):
  - 0x080643e0  check_equip_slot_eligible_neo_daedalus_with_zero_active_equip
  - 0x08064418  dispatch_equip_slot_eligible_by_zone_type
  - 0x080644b4  check_slot_equip_chain_pair_eligible_by_card
  - 0x08064598  check_slot_equip_target_has_field5
  - 0x0806460c  check_equip_slot_eligible_via_effect_node_and_bitmap
  - 0x08064654  invoke_equip_slot_eligibility_via_effect_node_bitmap
  - 0x08064660  submit_equip_zone_bitmap_pair_update
  - 0x08064678  invoke_equip_slot_sprite_update_with_zone_check
  - 0x08064760  dispatch_equip_sprite_update_by_card_type
  - 0x08064880  dispatch_equip_lp_delta_by_card_id  (大函数; 多 inline fragment 子函数 0x65018..0x6544a)

- 残留自动名槽: DAT_/DWORD_ x87 (详见 EQ_SLOTS 表); PTR_ x13 (已符号化, 见 REF_SLOTS)

- ROM_INCBIN 块 x2:
  - 0x6456c  size 0x2c (44 B)
  - 0x645ee  size 0x1e (30 B)

---

## 数据块分类 (Rule 2/3) — ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x6456c sz=0x2c | raw=0 thumb+1=1 (at 0x09e43078) | R4 disasm | THUMB+1 命中 => 0x09e43078 属 0x09e4xxxx handler table; entry start @0x09e4306c: CID=0x19df (Success Probability 0%); fn_eligible+1=0x0806456d; 真函数指针引用 |
| 0x645ee sz=0x1e | raw=0 thumb+1=1 (at 0x09e45580) + raw=1 at 0x088bbb8d (non-4B-aligned, 压缩资产内噪声) | R4 disasm (0x645f0 处 14B 函数; 0x645ee 2B padding) | THUMB+1 命中 => 0x09e45580 handler table; entry start @0x09e45574: CID=0x19ef (Elemental Hero Erikshieler); fn_eligible+1=0x080645f1; raw ref 不对齐=压缩资产伪命中不算真引用 |

### Block 1 解码 (0x0806456c, 0x2c): check_opponent_chain_zone_count_gt1_for_cid_19df

THUMB code (22B code + 8B literal pool):
```
0x6456c: ldr r2,[pc,#0x1c]       @ target 0x0806458c = gP1LifePoints (0x0201c4e0)
0x6456e: ldrb r0,[r0,#0x2]       @ r0 = slot[+2] byte (player_id+zone bits)
0x64570: lsls r0,r0,#0x1f        @ isolate bit0
0x64572: lsrs r0,r0,#0x1f        @ r0 = player_id
0x64574: movs r1,#0x1
0x64576: eors r0,r1               @ r0 = 1-player_id = opponent_player_id
0x64578: ldr r1,[pc,#0x14]       @ target 0x08064590 = PLAYER_BLOCK_STRIDE (0x00000868)
0x6457a: muls r0,r1               @ r0 = opponent_player_id * 0x868
0x6457c: adds r2,#0x18            @ r2 = gP1LifePoints + 0x18 = gP1ChainZoneCountBase (ewram.inc:333)
0x6457e: adds r0,r0,r2            @ r0 = gP1ChainZoneCountBase + opp*0x868
0x64580: ldr r0,[r0,#0x0]        @ r0 = [gP1ChainZoneCountBase + opp*0x868] (opponent chain zone count)
0x64582: cmp r0,#0x1
0x64584: bls LAB_64594            @ if <=1 -> return 0
0x64586: movs r0,#0x1
0x64588: b +10 (exit r0=1)
   (fall: r0=0)
0x64594: movs r0,#0x0
0x64596: bx lr
literal pool: [0x6458c]=0x0201c4e0 (gP1LifePoints), [0x64590]=0x00000868 (PLAYER_BLOCK_STRIDE)
```
Semantic: eligibility check for CID 0x19df (Success Probability 0%): loads opponent chain zone count (gP1ChainZoneCountBase + opp*0x868), returns 1 if >1, else 0.
Name (R4 disasm): `check_opponent_chain_zone_count_gt1_for_cid_19df`

### Block 2 解码 (0x080645ee, 0x1e): .hword 0x0000 padding + check_alt_hand_sum_nonzero_for_cid_19ef

```
0x645ee: .hword 0x0000   (2B alignment padding)
fn entry at 0x080645f0 (14B code + 8B literal pool):
0x645f0: ldr r0,[pc,#0x10]  -> target 0x08064604 = gP1LifePoints (0x0201c4e0)
0x645f2: ldr r2,[pc,#0x14]  -> target 0x08064608 = 0x00000884
0x645f4: adds r1,r0,r2       @ r1 = gP1LifePoints + 0x884
0x645f6: ldr r2,[r0,#0x1c]  @ r2 = [gP1LifePoints+0x1c] = gP1AltHandCountBase[0]
0x645f8: ldr r0,[r1,#0x0]   @ r0 = [gP1LifePoints+0x884]
0x645fa: adds r0,r2,r0       @ r0 = P1_alt_count + P2_alt_count(or related field)
0x645fc: cmp r0,#0x0
0x645fe: beq LAB -> return 0
0x64600: movs r0,#0x1
0x64602: bx lr
literal pool: [0x64604]=0x0201c4e0 (gP1LifePoints), [0x64608]=0x00000884
```
Semantic: eligibility check for CID 0x19ef (Elemental Hero Erikshieler): sums [gP1LifePoints+0x1c] and [gP1LifePoints+0x884]; returns 1 if nonzero. 0x884=0x1c+0x868, so checks P1 and P2 alt-hand counts at same field offset.
Name (R4 disasm): `check_alt_hand_sum_nonzero_for_cid_19ef`

Literal pool constant 0x00000884: no existing equate. This is an offset used once here; named `P2_ALT_HAND_COUNT_OFF` or as raw offset. Since it computes as `PLAYER_BLOCK_STRIDE + 0x1c`, could annotate as such in EOL. Not a standalone named equate needed (the offset 0x1c is already gP1AltHandCountBase's offset). Mark as EOL comment only; no new equate.

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All 87 DAT_/DWORD_ slots. 52 reuse existing equates; 35 are new CID/LP constants (29 CID + 8 LP delta - 2 LP delta already counted as new). Grouped by function and value:

#### REUSE equates (52 slots)

| slot_addr | value | existing_const | source_inc | slot_label |
|---|---|---|---|---|
| 0x0806446c | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | dispatch_equip_slot_eligible_by_zone_type_stride_a |
| 0x08064470 | 0x0201c510 | gDuelFieldSlots | ewram.inc | dispatch_equip_slot_eligible_by_zone_type_slots_a |
| 0x080644a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | dispatch_equip_slot_eligible_by_zone_type_stride_b |
| 0x080644a8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | dispatch_equip_slot_eligible_by_zone_type_slots_b |
| 0x08064558 | 0x0000ffff | SLOT_CARD_EMPTY | card_info.inc | check_slot_equip_chain_pair_pair_not_found |
| 0x0806455c | 0x0201c4e0 | gP1LifePoints | ewram.inc | check_slot_equip_chain_pair_lp_base |
| 0x08064560 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_slot_equip_chain_pair_stride |
| 0x080646f4 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | invoke_equip_slot_sprite_stride_a |
| 0x080646f8 | 0x0201c510 | gDuelFieldSlots | ewram.inc | invoke_equip_slot_sprite_slots_a |
| 0x08064758 | 0x000012c6 | cid_12c6 | card_info.inc | invoke_equip_slot_sprite_cid_a |
| 0x0806475c | 0x0000145b | SCROLL_OF_BEWITCHMENT_CID | card_info.inc | invoke_equip_slot_sprite_cid_b |
| 0x08064874 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | dispatch_equip_sprite_stride |
| 0x08064878 | 0x0201c5d8 | gDuelFieldSlots_p2_base | ewram.inc | dispatch_equip_sprite_slots_p2 |
| 0x0806487c | 0x0201c510 | gDuelFieldSlots | ewram.inc | dispatch_equip_sprite_slots |
| 0x08064914 | 0x0000118a | AMEBA_CID | card_info.inc | dispatch_equip_lp_ameba_cid |
| 0x0806492c | 0x000010f8 | MOOYAN_CURRY_CID | card_info.inc | dispatch_equip_lp_mooyan_curry_cid |
| 0x080649a4 | 0x000011bc | MINAR_CID | card_info.inc | dispatch_equip_lp_minar_cid |
| 0x080649cc | 0x000012a2 | SKULL_MARK_LADYBUG_CID | card_info.inc | dispatch_equip_lp_skull_ladybug_cid |
| 0x080649f4 | 0x00001322 | SNATCH_STEAL_CID | card_info.inc | dispatch_equip_lp_snatch_steal_cid |
| 0x08064a04 | 0x00001307 | RESTRUCTER_REVOLUTION_CID | card_info.inc | dispatch_equip_lp_restructer_cid |
| 0x08064a20 | 0x0000137b | EYE_OF_TRUTH_CID | card_info.inc | dispatch_equip_lp_eye_of_truth_cid |
| 0x08064b64 | 0x0000159b | DARK_ROOM_OF_NIGHTMARE_CID | card_info.inc | dispatch_equip_lp_dark_room_cid |
| 0x08064b74 | 0x0000158c | GRAVEKEEPERS_CANNONHOLDER_CID | card_info.inc | dispatch_equip_lp_gk_cannonholder_cid |
| 0x08064b90 | 0x000015ee | WAVE_MOTION_CANNON_CID | card_info.inc | dispatch_equip_lp_wave_cannon_cid |
| 0x08064bf4 | 0x000017c8 | SPHINX_TELEIA_CID | card_info.inc | dispatch_equip_lp_sphinx_teleia_cid |
| 0x08064c08 | 0x0000163f | GRANADORA_CID | card_info.inc | dispatch_equip_lp_granadora_cid |
| 0x08064c70 | 0x000016f5 | BURNING_ALGAE_CID | card_info.inc | dispatch_equip_lp_burning_algae_cid |
| 0x08064c84 | 0x0000170b | GUARDIAN_ANGEL_JOAN_CID | card_info.inc | dispatch_equip_lp_guardian_joan_cid |
| 0x08064c98 | 0x0000173f | AGENT_OF_JUDGMENT_SATURN_CID | card_info.inc | dispatch_equip_lp_saturn_cid |
| 0x08064cec | 0x00001762 | BACKFIRE_CID | card_info.inc | dispatch_equip_lp_backfire_cid |
| 0x08064d34 | 0x000017a5 | CARD_7_CID | card_info.inc | dispatch_equip_lp_card7_cid |
| 0x08064d80 | 0x0000190a | DARK_RULER_VANDALGYON_CID | card_info.inc | dispatch_equip_lp_vandalgyon_cid |
| 0x08064d90 | 0x00001804 | CEMETARY_BOMB_CID | card_info.inc | dispatch_equip_lp_cemetary_bomb_cid |
| 0x08064db0 | 0x00001877 | BRAIN_JACKER_CID | card_info.inc | dispatch_equip_lp_brain_jacker_cid |
| 0x08064dc0 | 0x0000187b | POISON_FANGS_CID | card_info.inc | dispatch_equip_lp_poison_fangs_cid |
| 0x08064de8 | 0x000018d0 | LEGENDARY_BLACK_BELT_CID | card_info.inc | dispatch_equip_lp_legendary_belt_cid |
| 0x08064e04 | 0x000018d7 | KOZAKYS_SELF_DESTRUCT_CID | card_info.inc | dispatch_equip_lp_kozaky_cid |
| 0x08064e48 | 0x00001987 | ELEMENTAL_HERO_STEAM_HEALER_CID | card_info.inc | dispatch_equip_lp_steam_healer_cid |
| 0x08064e50 | 0x00001929 | SPIRITUAL_FIRE_ART_CID | card_info.inc | dispatch_equip_lp_spiritual_fire_cid |
| 0x08064e6c | 0x00001950 | OXYGEDDON_CID | card_info.inc | dispatch_equip_lp_oxygeddon_cid |
| 0x08065014 | 0xfffffc18 | PUZZLE_LP_STEP_1000 | duel_field.inc | write_equip_lp_delta_snatch_steal_neg1000 |
| 0x080650d4 | 0x00000bb8 | LP_COST_3000 | duel_field.inc | write_equip_lp_delta_des_koala_max_3000 |
| 0x080650ec | 0xfffffe70 | ZONE_EFFECT_ATK_PENALTY_500 (= -400; NOTE: const name wrong, value correct) | field_spell_bonus.inc | write_equip_lp_delta_neg400 |
| 0x080651bc | 0x0201c510 | gDuelFieldSlots | ewram.inc | write_equip_lp_delta_slots_ref |
| 0x0806526c | 0x0201bb90 | gEquipChainSlotRefs | ewram.inc | write_equip_lp_delta_equip_chain_ref |
| 0x080653d0 | 0xfffffd44 | SCORE_DELTA_NEG_700 | duel_field.inc | write_equip_lp_delta_fuhma_neg700 |
| 0x08065148 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | write_equip_lp_des_koala_stride |
| 0x08065174 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | write_equip_lp_alt_player_stride |
| 0x080651b8 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | write_equip_lp_ka2_stride |
| 0x08065258 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | write_equip_lp_minar_stride |
| 0x08065420 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | write_equip_lp_vandalgyon_stride_a |
| 0x08065448 | 0x00000868 | PLAYER_BLOCK_STRIDE | ewram.inc | write_equip_lp_vandalgyon_stride_b |

NOTE on reuse conflicts:
- `SCORE_DELTA_NEG_700 = 0xfffffd44 = -700` is an ATK/DEF score delta; slot 0x080653d0 uses it as LP delta (Fuhma Shuriken -700 LP). Semantic domains differ, BUT same integer value. Per C5 rule: since values collide AND we cannot prove they are "截然不同的两实体" (both are negative integer penalties, just in different contexts), REUSE is acceptable to avoid constant proliferation. Mark EOL to disambiguate.

NOTE on `ZONE_EFFECT_ATK_PENALTY_500 = 0xfffffe70`:
- This constant's name says "500" but its value is -400 (two's complement: 0xfffffe70 = -400). This is a pre-existing naming error in `constants/field_spell_bonus.inc`. The slot 0x080650ec uses -400 as LP penalty. Document the existing misname in EOL.

NOTE on `SCORE_DELTA_NEG_300 = 0xfffffed4 = -300` (slot 0x08065104) and `SCORE_DELTA_NEG_500 = 0xfffffe0c = -500` (slot 0x080651c0):
- Both have existing equates in duel_field.inc for ATK/DEF score purposes. For LP equip delta domain, new constants needed (semantically different). However the values collide. Decision: create new `LP_EQUIP_DELTA_NEG_300` and `LP_EQUIP_DELTA_NEG_500` for clarity. But see C5 policy: if value collision, reviewer to decide.
- **Proposal: create new LP_EQUIP_DELTA_NEG_300/500 in new constants/equip_lp_delta.inc** to avoid semantic ambiguity.

#### NEW EQ_SLOTS (35 slots -> 29 new CIDs + 6 LP deltas + 2 for 300/500)

New CID constants (add to constants/card_info.inc):

| value | name | card_name | passcode |
|---|---|---|---|
| 0x0000161d | DES_KOALA_CID | Des Koala | pw=69579761; card_1589 verified in card-stats.s |
| 0x000013a8 | WOODLAND_SPRITE_CID | Woodland Sprite | pw=06979239; card_1178 |
| 0x000010fe | cid_10fe | unallocated | not found in card-stats.s; neutral name |
| 0x000012e8 | cid_12e8 | unallocated | not found in card-stats.s; neutral name |
| 0x000011c9 | GRIGGLE_CID | Griggle | pw=95744531; card_0393 |
| 0x0000129a | REFLECT_BOUNDER_CID | Reflect Bounder | pw=02851070; card_0670 |
| 0x0000137a | GIFT_OF_MYSTICAL_ELF_CID | Gift of The Mystical Elf | pw=98299011; card_0788 |
| 0x0000141f | RAIN_OF_MERCY_CID | Rain of Mercy | pw=66719324; card_0899 |
| 0x0000144b | AMAZON_ARCHER_CID | Amazon Archer | pw=91869203; card_0944 |
| 0x00001459 | MARIE_THE_FALLEN_ONE_CID | Marie the Fallen One | pw=57579381; card_0948 |
| 0x00001467 | DARK_MAGICIAN_TOME_CID | Dark Magician's Tome of Black Magic | pw=67227834; card_0960 |
| 0x000014b2 | NIGHTMARE_WHEEL_CID | Nightmare Wheel | pw=54704216; card_1018 |
| 0x00001565 | TOON_CANNON_SOLDIER_CID | Toon Cannon Soldier | pw=79875176; card_1128 |
| 0x000014f3 | ZOLGA_CID | Zolga | pw=16268841; card_1068 |
| 0x00001525 | POISON_MUMMY_CID | Poison Mummy | pw=43716289; card_1096 |
| 0x000015f4 | SECRET_BARREL_CID | Secret Barrel | pw=27053506; card_1175 |
| 0x000016c5 | INFERNO_CID | Inferno | pw=74823665; card_1301 |
| 0x000016fa | STEALTH_BIRD_CID | Stealth Bird | pw=03510565; card_1347 |
| 0x00001767 | SOLAR_RAY_CID | Solar Ray | pw=44472639; card_1342 |
| 0x00001761 | GOBLIN_THIEF_CID | Goblin Thief | pw=45311864; card_1338 |
| 0x00001794 | ELEPHANT_STATUE_CID | Elephant Statue of Disaster | pw=12160911; card_1381 |
| 0x000017c7 | ANDRO_SPHINX_CID | Andro Sphinx | pw=15013468; card_1442 |
| 0x000018c8 | ELEMENTAL_HERO_FLAME_WINGMAN_CID | Elemental Hero Flame Wingman | pw=35809262; card_1688 |
| 0x000018da | ROCK_BOMBARDMENT_CID | Rock Bombardment | pw=20781762; card_1695 |
| 0x00001984 | MAGICAL_BLAST_CID | Magical Blast | pw=91819979; card_1751 |
| 0x000019cf | MEMORY_CRUSHER_CID | Memory Crusher | pw=48700891; card_2058; NEW - not in card_info.inc |
| 0x000019f0 | GUARDIAN_EXODE_CID | Guardian Exode | pw=55737443; card_2064 |

New LP delta constants (new file: constants/equip_lp_delta.inc, or add to duel_field.inc):

| value | name | decimal | context |
|---|---|---|---|
| 0xfffffda8 | LP_EQUIP_DELTA_NEG_600 | -600 | Solar Ray penalty per eligible zone (slot 0x08065098) |
| 0xfffffb50 | LP_EQUIP_DELTA_NEG_1200 | -1200 | Toon Cannon Soldier / Secret Barrel range (slot 0x080651d4) |
| 0xfffffce0 | LP_EQUIP_DELTA_NEG_800 | -800 | Dragon's Gunfire / shared path (slot 0x080651e8) |
| 0xfffffa24 | LP_EQUIP_DELTA_NEG_1500 | -1500 | Inferno penalty (slot 0x080653bc) |
| 0xfffff448 | LP_EQUIP_DELTA_NEG_3000 | -3000 | Blasting the Ruins penalty (slot 0x080653e4) |
| 0xfffff830 | LP_EQUIP_DELTA_NEG_2000 | -2000 | Granadora attack-position penalty (slot 0x080653f8) |
| 0xfffffed4 | LP_EQUIP_DELTA_NEG_300 | -300 | Legendary Black Belt path (slot 0x08065104; SCORE_DELTA_NEG_300 value conflict, new for LP domain) |
| 0xfffffe0c | LP_EQUIP_DELTA_NEG_500 | -500 | Woodland Sprite / Goblin Thief opponent side (slot 0x080651c0; SCORE_DELTA_NEG_500 value conflict, new for LP domain) |

### REF_SLOTS (USER-label + DATA-ref)

The 13 PTR_gP1LifePoints_* slots already use symbol `gP1LifePoints` in .word. They need label RENAME only (not EQ change). These are RENAME_SLOTS (see below).

No new RAM/ROM global carve labels needed for Seg-1.

### RENAME_SLOTS (纯改名 + EOL)

| slot_addr | old_label | new_label | eol |
|---|---|---|---|
| 0x0806446c | DWORD_0806446c | dispatch_equip_eligible_zone_type_stride_a | PLAYER_BLOCK_STRIDE |
| 0x08064470 | DWORD_08064470 | dispatch_equip_eligible_zone_type_slots_a | gDuelFieldSlots |
| 0x080644a4 | DWORD_080644a4 | dispatch_equip_eligible_zone_type_stride_b | PLAYER_BLOCK_STRIDE |
| 0x080644a8 | DWORD_080644a8 | dispatch_equip_eligible_zone_type_slots_b | gDuelFieldSlots |
| 0x08064558 | DWORD_08064558 | check_chain_pair_pair_not_found | SLOT_CARD_EMPTY sentinel |
| 0x0806455c | DWORD_0806455c | check_chain_pair_lp_base | gP1LifePoints |
| 0x08064560 | DWORD_08064560 | check_chain_pair_stride | PLAYER_BLOCK_STRIDE |
| 0x080645e4 | PTR_gP1LifePoints_080645e4 | check_equip_target_lp_base | gP1LifePoints |
| 0x080646f4 | DAT_080646f4 | invoke_equip_sprite_stride_a | PLAYER_BLOCK_STRIDE |
| 0x080646f8 | DAT_080646f8 | invoke_equip_sprite_slots_a | gDuelFieldSlots |
| 0x08064758 | DAT_08064758 | invoke_equip_sprite_cid_a | cid_12c6 (unallocated) |
| 0x0806475c | DAT_0806475c | invoke_equip_sprite_cid_b | SCROLL_OF_BEWITCHMENT_CID |
| 0x08064874 | DAT_08064874 | dispatch_equip_sprite_stride | PLAYER_BLOCK_STRIDE |
| 0x08064878 | DAT_08064878 | dispatch_equip_sprite_slots_p2 | gDuelFieldSlots_p2_base |
| 0x0806487c | DAT_0806487c | dispatch_equip_sprite_slots | gDuelFieldSlots |
| 0x0806490c | DAT_0806490c | dispatch_equip_lp_des_koala_cid | DES_KOALA_CID [new] |
| 0x08064910 | DAT_08064910 | dispatch_equip_lp_woodland_sprite_cid | WOODLAND_SPRITE_CID [new] |
| 0x08064914 | DAT_08064914 | dispatch_equip_lp_ameba_cid | AMEBA_CID |
| 0x0806492c | DAT_0806492c | dispatch_equip_lp_mooyan_curry_cid | MOOYAN_CURRY_CID |
| 0x08064950 | DAT_08064950 | dispatch_equip_lp_cid_10fe | cid_10fe [new] |
| 0x08064998 | DAT_08064998 | dispatch_equip_lp_cid_12e8 | cid_12e8 [new] |
| 0x0806499c | DAT_0806499c | dispatch_equip_lp_griggle_cid | GRIGGLE_CID [new] |
| 0x080649a4 | DAT_080649a4 | dispatch_equip_lp_minar_cid | MINAR_CID |
| 0x080649c4 | DAT_080649c4 | dispatch_equip_lp_reflect_bounder_cid | REFLECT_BOUNDER_CID [new] |
| 0x080649cc | DAT_080649cc | dispatch_equip_lp_skull_ladybug_cid | SKULL_MARK_LADYBUG_CID |
| 0x080649f4 | DAT_080649f4 | dispatch_equip_lp_snatch_steal_cid | SNATCH_STEAL_CID |
| 0x08064a04 | DAT_08064a04 | dispatch_equip_lp_restructer_cid | RESTRUCTER_REVOLUTION_CID |
| 0x08064a18 | DAT_08064a18 | dispatch_equip_lp_mystical_elf_cid | GIFT_OF_MYSTICAL_ELF_CID [new] |
| 0x08064a20 | DAT_08064a20 | dispatch_equip_lp_eye_of_truth_cid | EYE_OF_TRUTH_CID |
| 0x08064a74 | DAT_08064a74 | dispatch_equip_lp_rain_of_mercy_cid | RAIN_OF_MERCY_CID [new] |
| 0x08064a94 | DAT_08064a94 | dispatch_equip_lp_amazon_archer_cid | AMAZON_ARCHER_CID [new] |
| 0x08064ab8 | DAT_08064ab8 | dispatch_equip_lp_marie_cid | MARIE_THE_FALLEN_ONE_CID [new] |
| 0x08064acc | DAT_08064acc | dispatch_equip_lp_dm_tome_cid | DARK_MAGICIAN_TOME_CID [new] |
| 0x08064ad4 | DAT_08064ad4 | dispatch_equip_lp_nightmare_wheel_cid | NIGHTMARE_WHEEL_CID [new] |
| 0x08064b08 | DAT_08064b08 | dispatch_equip_lp_toon_cannon_cid | TOON_CANNON_SOLDIER_CID [new] |
| 0x08064b18 | DAT_08064b18 | dispatch_equip_lp_zolga_cid | ZOLGA_CID [new] |
| 0x08064b3c | DAT_08064b3c | dispatch_equip_lp_poison_mummy_cid | POISON_MUMMY_CID [new] |
| 0x08064b64 | DAT_08064b64 | dispatch_equip_lp_dark_room_cid | DARK_ROOM_OF_NIGHTMARE_CID |
| 0x08064b74 | DAT_08064b74 | dispatch_equip_lp_gk_cannonholder_cid | GRAVEKEEPERS_CANNONHOLDER_CID |
| 0x08064b90 | DAT_08064b90 | dispatch_equip_lp_wave_cannon_cid | WAVE_MOTION_CANNON_CID |
| 0x08064ba0 | DAT_08064ba0 | dispatch_equip_lp_secret_barrel_cid | SECRET_BARREL_CID [new] |
| 0x08064bf4 | DAT_08064bf4 | dispatch_equip_lp_sphinx_teleia_cid | SPHINX_TELEIA_CID |
| 0x08064c08 | DAT_08064c08 | dispatch_equip_lp_granadora_cid | GRANADORA_CID |
| 0x08064c34 | DAT_08064c34 | dispatch_equip_lp_inferno_cid | INFERNO_CID [new] |
| 0x08064c60 | DAT_08064c60 | dispatch_equip_lp_stealth_bird_cid | STEALTH_BIRD_CID [new] |
| 0x08064c70 | DAT_08064c70 | dispatch_equip_lp_burning_algae_cid | BURNING_ALGAE_CID |
| 0x08064c84 | DAT_08064c84 | dispatch_equip_lp_guardian_joan_cid | GUARDIAN_ANGEL_JOAN_CID |
| 0x08064c98 | DAT_08064c98 | dispatch_equip_lp_saturn_cid | AGENT_OF_JUDGMENT_SATURN_CID |
| 0x08064cc4 | DAT_08064cc4 | dispatch_equip_lp_solar_ray_cid | SOLAR_RAY_CID [new] |
| 0x08064ce4 | DAT_08064ce4 | dispatch_equip_lp_goblin_thief_cid | GOBLIN_THIEF_CID [new] |
| 0x08064cec | DAT_08064cec | dispatch_equip_lp_backfire_cid | BACKFIRE_CID |
| 0x08064d18 | DAT_08064d18 | dispatch_equip_lp_elephant_statue_cid | ELEPHANT_STATUE_CID [new] |
| 0x08064d34 | DAT_08064d34 | dispatch_equip_lp_card7_cid | CARD_7_CID |
| 0x08064d44 | DAT_08064d44 | dispatch_equip_lp_andro_sphinx_cid | ANDRO_SPHINX_CID [new] |
| 0x08064d80 | DAT_08064d80 | dispatch_equip_lp_vandalgyon_cid | DARK_RULER_VANDALGYON_CID |
| 0x08064d90 | DAT_08064d90 | dispatch_equip_lp_cemetary_bomb_cid | CEMETARY_BOMB_CID |
| 0x08064db0 | DAT_08064db0 | dispatch_equip_lp_brain_jacker_cid | BRAIN_JACKER_CID |
| 0x08064dc0 | DAT_08064dc0 | dispatch_equip_lp_poison_fangs_cid | POISON_FANGS_CID |
| 0x08064de8 | DAT_08064de8 | dispatch_equip_lp_legendary_belt_cid | LEGENDARY_BLACK_BELT_CID |
| 0x08064df0 | DAT_08064df0 | dispatch_equip_lp_eh_flame_wingman_cid | ELEMENTAL_HERO_FLAME_WINGMAN_CID [new] |
| 0x08064e04 | DAT_08064e04 | dispatch_equip_lp_kozaky_cid | KOZAKYS_SELF_DESTRUCT_CID |
| 0x08064e14 | DAT_08064e14 | dispatch_equip_lp_rock_bombardment_cid | ROCK_BOMBARDMENT_CID [new] |
| 0x08064e48 | DAT_08064e48 | dispatch_equip_lp_steam_healer_cid | ELEMENTAL_HERO_STEAM_HEALER_CID |
| 0x08064e50 | DAT_08064e50 | dispatch_equip_lp_spiritual_fire_cid | SPIRITUAL_FIRE_ART_CID |
| 0x08064e6c | DAT_08064e6c | dispatch_equip_lp_oxygeddon_cid | OXYGEDDON_CID |
| 0x08064e70 | DAT_08064e70 | dispatch_equip_lp_magical_blast_cid | MAGICAL_BLAST_CID [new] |
| 0x08064e90 | DAT_08064e90 | dispatch_equip_lp_memory_crusher_cid | MEMORY_CRUSHER_CID [new] |
| 0x08064eb8 | DAT_08064eb8 | dispatch_equip_lp_guardian_exode_cid | GUARDIAN_EXODE_CID [new] |
| 0x08065014 | DAT_08065014 | write_equip_lp_snatch_steal_neg1000 | PUZZLE_LP_STEP_1000 (-1000) |
| 0x08065098 | DAT_08065098 | write_equip_lp_solar_ray_neg600 | LP_EQUIP_DELTA_NEG_600 [new] |
| 0x080650d4 | DAT_080650d4 | write_equip_lp_des_koala_max_3000 | LP_COST_3000 (reuse 3000 threshold) |
| 0x080650ec | DAT_080650ec | write_equip_lp_neg400 | ZONE_EFFECT_ATK_PENALTY_500 (-400; existing name misleading) |
| 0x08065104 | DAT_08065104 | write_equip_lp_legendary_belt_neg300 | LP_EQUIP_DELTA_NEG_300 [new; SCORE_DELTA_NEG_300 domain differs] |
| 0x08065144 | PTR_gP1LifePoints_08065144 | write_equip_lp_des_koala_lp_base | gP1LifePoints |
| 0x08065148 | DAT_08065148 | write_equip_lp_des_koala_stride | PLAYER_BLOCK_STRIDE |
| 0x08065170 | PTR_gP1LifePoints_08065170 | write_equip_lp_alt_player_lp_base | gP1LifePoints |
| 0x08065174 | DAT_08065174 | write_equip_lp_alt_player_stride | PLAYER_BLOCK_STRIDE |
| 0x080651b8 | DAT_080651b8 | write_equip_lp_ka2_stride | PLAYER_BLOCK_STRIDE |
| 0x080651bc | DAT_080651bc | write_equip_lp_ka2_slots | gDuelFieldSlots |
| 0x080651c0 | DAT_080651c0 | write_equip_lp_woodland_neg500 | LP_EQUIP_DELTA_NEG_500 [new; SCORE_DELTA_NEG_500 domain differs] |
| 0x080651d4 | DAT_080651d4 | write_equip_lp_gk_cannon_neg1200 | LP_EQUIP_DELTA_NEG_1200 [new] |
| 0x080651e8 | DAT_080651e8 | write_equip_lp_dragon_gunfire_neg800 | LP_EQUIP_DELTA_NEG_800 [new] |
| 0x08065254 | PTR_gP1LifePoints_08065254 | write_equip_lp_minar_lp_base | gP1LifePoints |
| 0x08065258 | DAT_08065258 | write_equip_lp_minar_stride | PLAYER_BLOCK_STRIDE |
| 0x0806526c | DAT_0806526c | write_equip_lp_equip_chain_ref | gEquipChainSlotRefs |
| 0x08065290 | PTR_gP1LifePoints_08065290 | write_equip_lp_wave_cannon_lp_base_a | gP1LifePoints |
| 0x080652b8 | PTR_gP1LifePoints_080652b8 | write_equip_lp_wave_cannon_lp_base_b | gP1LifePoints |
| 0x080652ec | PTR_gP1LifePoints_080652ec | write_equip_lp_greed_lp_base_a | gP1LifePoints |
| 0x08065320 | PTR_gP1LifePoints_08065320 | write_equip_lp_greed_lp_base_b | gP1LifePoints |
| 0x08065344 | PTR_gP1LifePoints_08065344 | write_equip_lp_secret_barrel_lp_base | gP1LifePoints |
| 0x08065378 | PTR_gP1LifePoints_08065378 | write_equip_lp_snatch_steal_lp_base | gP1LifePoints |
| 0x080653a8 | PTR_gP1LifePoints_080653a8 | write_equip_lp_guardian_joan_lp_base | gP1LifePoints |
| 0x080653bc | DAT_080653bc | write_equip_lp_inferno_neg1500 | LP_EQUIP_DELTA_NEG_1500 [new] |
| 0x080653d0 | DAT_080653d0 | write_equip_lp_fuhma_neg700 | SCORE_DELTA_NEG_700 (reuse; -700 same value; EOL clarifies LP domain) |
| 0x080653e4 | DAT_080653e4 | write_equip_lp_blasting_ruins_neg3000 | LP_EQUIP_DELTA_NEG_3000 [new] |
| 0x080653f8 | DAT_080653f8 | write_equip_lp_granadora_atk_neg2000 | LP_EQUIP_DELTA_NEG_2000 [new] |
| 0x0806541c | PTR_gP1LifePoints_0806541c | write_equip_lp_vandalgyon_lp_base_a | gP1LifePoints |
| 0x08065420 | DAT_08065420 | write_equip_lp_vandalgyon_stride_a | PLAYER_BLOCK_STRIDE |
| 0x08065444 | PTR_gP1LifePoints_08065444 | write_equip_lp_vandalgyon_lp_base_b | gP1LifePoints |
| 0x08065448 | DAT_08065448 | write_equip_lp_vandalgyon_stride_b | PLAYER_BLOCK_STRIDE |

Total RENAME: 100 (87 DAT_/DWORD_ + 13 PTR_gP1LifePoints_*)

### FUNC_RENAME (误名订正)

No function renames needed in Seg-1. All 10 function names correctly match their function bodies (evidence: function body descriptions in existing plates are accurate).

### PLATE (R5)

Stale FUN_ in plates (C8 violation) -- 3 unique stale names in Seg-1 scope:

| plate_location | stale_text | replacement |
|---|---|---|
| submit_equip_zone_bitmap_pair_update plate (line 345) | FUN_080714ec | dispatch_equip_zone11_target_by_activation_state |
| dispatch_equip_sprite_update_by_card_type plate (line 503) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_by_opponent_side plate (line 1823) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_by_opponent_side plate (line 1823) | FUN_080655da | restore_equip_effect_frame |
| write_equip_lp_delta_by_own_side plate (line 1887) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_by_own_side plate (line 1887) | FUN_080655da | restore_equip_effect_frame |
| write_equip_lp_delta_scaled_by_lp_count plate (line 1973) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_by_alt_player plate (line 2054) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_by_alt_player plate (line 2054) | FUN_080655da | restore_equip_effect_frame |
| write_equip_lp_delta_negated_atk plate (line 2071) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_negated_atk plate (line 2071) | FUN_080655da | restore_equip_effect_frame |
| write_equip_lp_delta_minar plate (line 2134) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_ka2_des_scissors plate (line 2259) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_inferno plate (line 2318) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_fuhma_shuriken plate (line 2336) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_blasting_the_ruins plate (line 2354) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |
| write_equip_lp_delta_goblin_thief plate (line 2425) | FUN_08064880 | dispatch_equip_lp_delta_by_card_id |

File header line 2 non-ASCII mojibake: `@ neo daedalus 资格 + 装备 OAM 写入 + zone tile 计数` -- rewrite as ASCII:
`@ neo daedalus eligibility + equip OAM write + zone tile count`

PLATE strategy: substring replacement of `FUN_08064880` -> `dispatch_equip_lp_delta_by_card_id`, `FUN_080714ec` -> `dispatch_equip_zone11_target_by_activation_state`, and `FUN_080655da` -> `restore_equip_effect_frame` throughout Seg-1 plates. All three stale FUN_ names appear within Seg-1 code range and must be replaced here. Post-landing grep `FUN_[0-9a-f]{8}` in Seg-1 range must return 0.

---

## carve 计划 (R7, 如有)

None for Seg-1 -- both ROM_INCBIN blocks are handler code (R4 disasm), not data tables.

---

## disasm 计划 (R4)

Two THUMB handler functions disassembled from ROM_INCBIN blocks:

### Block 1: 0x0806456c, size 0x2c

- fn entry: 0x0806456c (THUMB+1 ref confirmed at 0x09e43078 in handler table CID=0x19df)
- code: 0x0806456c .. 0x08064597 (code 0x22B + 2B pad at 0x0806458a + literal pool 0x8B)
- Procedure:
  1. clearListing 0x0806456c .. 0x08064598
  2. setTMode 0x0806456c .. 0x08064598
  3. DisassembleCommand at 0x0806456c
  4. createDWord at 0x0806458c (gP1LifePoints literal)
  5. createDWord at 0x08064590 (PLAYER_BLOCK_STRIDE literal)
  6. setEOL at 0x0806458a: "alignment pad"
- Label: `check_opponent_chain_zone_count_gt1_for_cid_19df:` at 0x0806456c
- EOL at entry: `cid_19df = Success Probability 0%; fn_eligible at handler table 0x09e4306c; reads gP1ChainZoneCountBase+opp*0x868, returns 1 if >1`
- Literal pool EOL at 0x0806458c: `gP1LifePoints (base for gP1ChainZoneCountBase +0x18)`; at 0x08064590: `PLAYER_BLOCK_STRIDE`

### Block 2: 0x080645ee, size 0x1e

- 2B padding at 0x080645ee (.hword 0x0000 alignment)
- fn entry: 0x080645f0 (THUMB+1 ref confirmed at 0x09e45580 in handler table CID=0x19ef)
- code: 0x080645f0 .. 0x08064609 (code 0x12B + literal pool 0x8B at 0x08064604)
- Procedure:
  1. clearListing 0x080645ee .. 0x0806460c
  2. createWord at 0x080645ee (alignment .hword 0x0000)
  3. setTMode 0x080645f0 .. 0x0806460c
  4. DisassembleCommand at 0x080645f0
  5. createDWord at 0x08064604 (gP1LifePoints)
  6. createDWord at 0x08064608 (0x00000884 = PLAYER_BLOCK_STRIDE+0x1c = P2 alt-hand offset)
- Label: `check_alt_hand_sum_nonzero_for_cid_19ef:` at 0x080645f0
- EOL at 0x080645ee: "alignment padding 2B before fn entry 0x080645f0"
- EOL at entry: `cid_19ef = Elemental Hero Erikshieler; fn_eligible at handler table 0x09e45574`
- EOL at 0x08064604: `gP1LifePoints`; at 0x08064608: `0x884 = PLAYER_BLOCK_STRIDE+gP1AltHandCountBase_offset`

---

## 新增 constants / 全局

### constants/card_info.inc 追加 (29 new CID equates)

Confirmed: each value grep-checked in card-stats.s or confirmed unallocated. None of these exist in any .inc file (verified by python equate map scan showing 0 matches).

```
.equ DES_KOALA_CID,                    0x0000161d  @ Des Koala (pw=69579761); dispatch_equip_lp_delta_by_card_id scaled-LP-count path
.equ WOODLAND_SPRITE_CID,              0x000013a8  @ Woodland Sprite (pw=06979239); write_equip_lp_delta_by_opponent_side dispatch
.equ cid_10fe,                         0x000010fe  @ unallocated slot 0x10fe; not in card-stats.s; dispatch_equip_lp_delta_by_card_id node
.equ cid_12e8,                         0x000012e8  @ unallocated slot 0x12e8; not in card-stats.s; dispatch node
.equ GRIGGLE_CID,                      0x000011c9  @ Griggle (pw=95744531); dispatch node
.equ REFLECT_BOUNDER_CID,              0x0000129a  @ Reflect Bounder (pw=02851070); dispatch node
.equ GIFT_OF_MYSTICAL_ELF_CID,         0x0000137a  @ Gift of The Mystical Elf (pw=98299011)
.equ RAIN_OF_MERCY_CID,                0x0000141f  @ Rain of Mercy (pw=66719324)
.equ AMAZON_ARCHER_CID,                0x0000144b  @ Amazon Archer (pw=91869203)
.equ MARIE_THE_FALLEN_ONE_CID,         0x00001459  @ Marie the Fallen One (pw=57579381)
.equ DARK_MAGICIAN_TOME_CID,           0x00001467  @ Dark Magician's Tome of Black Magic (pw=67227834)
.equ NIGHTMARE_WHEEL_CID,              0x000014b2  @ Nightmare Wheel (pw=54704216)
.equ ZOLGA_CID,                        0x000014f3  @ Zolga (pw=16268841)
.equ POISON_MUMMY_CID,                 0x00001525  @ Poison Mummy (pw=43716289)
.equ TOON_CANNON_SOLDIER_CID,          0x00001565  @ Toon Cannon Soldier (pw=79875176)
.equ SECRET_BARREL_CID,                0x000015f4  @ Secret Barrel (pw=27053506)
.equ INFERNO_CID,                      0x000016c5  @ Inferno (pw=74823665)
.equ GOBLIN_THIEF_CID,                 0x00001761  @ Goblin Thief (pw=45311864)
.equ SOLAR_RAY_CID,                    0x00001767  @ Solar Ray (pw=44472639)
.equ ELEPHANT_STATUE_CID,              0x00001794  @ Elephant Statue of Disaster (pw=12160911)
.equ ANDRO_SPHINX_CID,                 0x000017c7  @ Andro Sphinx (pw=15013468)
.equ STEALTH_BIRD_CID,                 0x000016fa  @ Stealth Bird (pw=03510565)
.equ ELEMENTAL_HERO_FLAME_WINGMAN_CID, 0x000018c8  @ Elemental Hero Flame Wingman (pw=35809262)
.equ ROCK_BOMBARDMENT_CID,             0x000018da  @ Rock Bombardment (pw=20781762)
.equ MAGICAL_BLAST_CID,                0x00001984  @ Magical Blast (pw=91819979)
.equ MEMORY_CRUSHER_CID,              0x000019cf  @ Memory Crusher (pw=48700891)
.equ GUARDIAN_EXODE_CID,               0x000019f0  @ Guardian Exode (pw=55737443)
```

### constants/equip_lp_delta.inc (new file, 8 LP penalty equates)

Values confirmed via python ROM ref counts; semantically distinct from SCORE_DELTA_* (equip LP penalty vs ATK/DEF score adjustment):

```
@ Equip card LP delta penalty constants (s32, stored in gDuelFieldOutput player slot)
@ used by dispatch_equip_lp_delta_by_card_id sub-functions
.equ LP_EQUIP_DELTA_NEG_300,  0xfffffed4  @ -300 (s32); Legendary Black Belt / range path; 6 ROM refs
.equ LP_EQUIP_DELTA_NEG_500,  0xfffffe0c  @ -500 (s32); Woodland Sprite / Goblin Thief opp; 27 ROM refs
.equ LP_EQUIP_DELTA_NEG_600,  0xfffffda8  @ -600 (s32); Solar Ray per zone; 4 ROM refs
.equ LP_EQUIP_DELTA_NEG_800,  0xfffffce0  @ -800 (s32); Dragon's Gunfire shared path; 5 ROM refs
.equ LP_EQUIP_DELTA_NEG_1200, 0xfffffb50  @ -1200 (s32); Toon Cannon Soldier range; 3 ROM refs
.equ LP_EQUIP_DELTA_NEG_1500, 0xfffffa24  @ -1500 (s32); Inferno equip penalty; 1 ROM ref
.equ LP_EQUIP_DELTA_NEG_2000, 0xfffff830  @ -2000 (s32); Granadora atk-position; 8 ROM refs
.equ LP_EQUIP_DELTA_NEG_3000, 0xfffff448  @ -3000 (s32); Blasting the Ruins penalty; 1 ROM ref
```

---

## §5.1 登记 (Rule 3) -- 0 引用块

None in Seg-1. Both ROM_INCBIN blocks have THUMB+1 references confirmed. No §5.1 entries.

---

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 槽/常量 | 消费者 file:line | 语义 | 置信度 |
|---|---|---|---|
| PLAYER_BLOCK_STRIDE (0x868) | asm/08 line 80: muls r0,r7; comment "player_stride=0x868" in existing plate | 每 player 数据块步长 | high |
| gDuelFieldSlots (0x0201c510) | asm/08 line 82: ldr r0, DWORD_08064470; plate "gDuelFieldSlots=0x0201c510"; ewram.inc line confirms | 区位数组基址 | high |
| SLOT_CARD_EMPTY (0x0000ffff) | asm/08 line 164: ldr r0, DWORD_08064558; cmp r5,r0 @ compare pair_id with PAIR_NOT_FOUND sentinel; card_info.inc line 386 | 空槽哨兵 | high |
| gP1LifePoints (0x0201c4e0) | asm/08 line 201: ldr r1, DWORD_0806455c; ewram.inc line "gP1LifePoints 0x0201C4E0" | P1 LP 基址 | high |
| cid_12c6 (0x000012c6) | asm/08 line 477-480: ldrh r1,[r7,#0x0]; ldr r0, DAT_08064758; cmp r1,r0; beq -> trigger enqueue_sprite_attr_with_xy_split; unallocated CID confirmed not in card-stats.s | 无分配 CID | high |
| SCROLL_OF_BEWITCHMENT_CID (0x0000145b) | asm/08 line 480-482: second cid check in same conditional | Scroll of Bewitchment card | high |
| gDuelFieldSlots_p2_base (0x0201c5d8) | asm/08 line 649: DAT_08064878; dispatch_equip_sprite_update_by_card_type uses as base for field output buffer | P2 slot base | high |
| AMEBA_CID (0x0000118a) | asm/08 line 716: ldr r0, DAT_08064914; cmp r3,r0 -> routes to write_equip_lp_delta_by_own_side | Ameba card equip delta | high |
| DES_KOALA_CID (0x0000161d) | asm/08 line 698: ldr r0, DAT_0806490c; cmp r3,r0; bne/bl write_equip_lp_delta_scaled_by_lp_count | Des Koala card | high |
| LP_EQUIP_DELTA_NEG_1500 (0xfffffa24) | asm/08 line 2329: ldr r1, DAT_080653bc; str r1,[r0,#0x0]; plate "Inferno equip effect...writes fixed value -1500" | Inferno -1500 LP | high |
| LP_EQUIP_DELTA_NEG_3000 (0xfffff448) | asm/08 line 2364: ldr r1, DAT_080653e4; plate "Blasting the Ruins...writes fixed value -3000" | Blasting the Ruins -3000 LP | high |
| block1 fn semantic | 0x09e4306c handler table entry: CID=0x19df fn_eligible=0x0806456d; fn_eligible reads gP1ChainZoneCountBase+opp*0x868, returns 1 if opponent chain zone count >1 | eligibility for Success Probability 0% | high |
| block2 fn semantic | 0x09e45574 handler table entry: CID=0x19ef fn_eligible=0x080645f1; checks sum of P1+P2 field @+0x1c nonzero | eligibility for Elemental Hero Erikshieler | med (0x884 offset semantic not fully mapped) |

---

## 求助

1. **Block 2 offset 0x884**: `[gP1LifePoints + 0x884]` = `[gP1LifePoints + 0x868 + 0x1c]` = `[gP2LP_base + 0x1c]`. Since `gP1AltHandCountBase = gP1LifePoints + 0x1c` (ewram.inc line 335), this would be P2's equivalent. The function sums both and checks nonzero. Semantic confidence: med. No blocker for disasm - just EOL annotation.

2. **ZONE_EFFECT_ATK_PENALTY_500 pre-existing name error**: the constant `ZONE_EFFECT_ATK_PENALTY_500 = 0xfffffe70` in field_spell_bonus.inc has a name saying "500" but the value is -400. This is a pre-existing bug outside Seg-1 scope. Recommend reviewer to flag CONST_RENAME for that constant separately (out of Seg-1 scope).

3. **C5 decision on SCORE_DELTA_NEG_300/500**: proposal creates new `LP_EQUIP_DELTA_NEG_300/500` in equip_lp_delta.inc. Reviewer to confirm whether value collision warrants new constants vs reuse of SCORE_DELTA names.
