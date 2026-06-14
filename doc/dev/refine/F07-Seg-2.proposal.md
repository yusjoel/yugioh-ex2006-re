# Refine Proposal: F07-Seg-2  [0x0805cfec..0x0805e358)

## Segment Survey

### Function Entries (34)

| addr | name |
|------|------|
| 0x0805cfec | check_spell_zone_effect_activatable |
| 0x0805d010 | check_monster_zone_field_state_eligible |
| 0x0805d118 | check_equip_zone_effect_eligible_by_card_id |
| 0x0805d740 | check_spell_zone_chain_occupied_eligible |
| 0x0805d7a4 | check_equip_zone_has_field5_card |
| 0x0805d808 | check_monster_slots_nonzero_for_card_player |
| 0x0805d830 | check_equip_slot_eligible_type_range1f21_with_target |
| 0x0805d860 | check_equip_slot_eligible_type_range1f21_with_equippable_count |
| 0x0805d8c0 | check_equip_slot_eligible_with_field_state_and_chain |
| 0x0805d910 | check_spell_type480_active_deck_matches |
| 0x0805d9a0 | check_any_equip_slot_available_either_player |
| 0x0805d9e0 | check_equip_zone_field_ownership_eligible |
| 0x0805da70 | check_equip_slot_eligible_field6_max5 |
| 0x0805daa4 | check_equip_slot_eligible_without_light_of_intervention_max2 |
| 0x0805dae0 | invoke_effect_node_handler_with_zone_flag_guard |
| 0x0805db60 | check_equip_zone14_eligible_both_players |
| 0x0805dbf0 | check_effect_dispatch_result_above4 |
| 0x0805dc28 | check_equip_zone_descriptor_field5_player_match |
| 0x0805dc6c | check_equip_slot_eligible_type6c0_by_gust_or_driving_snow |
| 0x0805dd58 | check_equip_slot_pair_field6_field9_eligible |
| 0x0805deac | check_equip_slot_eligible_with_lp_offset_threshold |
| 0x0805df18 | check_equip_slot_eligible_with_hand_field5_count |
| 0x0805df60 | check_field_active_slot_or_zone_pair |
| 0x0805dfac | check_equip_slot_eligible_with_active_player_and_lp_count |
| 0x0805e030 | check_equip_slot_eligible_with_neo_daedalus_and_both_players |
| 0x0805e094 | check_field_state1_player_not_active_with_opponent_monsters |
| 0x0805e0ec | check_spell_type500_deck_states_differ |
| 0x0805e150 | check_monster_zone_field6_equals22 |
| 0x0805e20c | check_equip_slot_absent_for_opponent |
| 0x0805e220 | check_chain_field_match_any_player |
| 0x0805e268 | check_equip_slot_eligible_by_deck_prereqs_and_card_type |
| 0x0805e308 | check_equip_slot_field6_score_within_2000 |
| 0x0805e320 | check_equip_eligible_with_magnet_warrior_trio |
| 0x0805e354 | check_equip_slot_eligible_type3c0_with_deck_prereqs_and_field14 |

Note: check_equip_zone_effect_eligible_by_card_id (0x0805d118..0x0805d73f) is a 0x628-byte BST
spanning 32 sub-branches. Sub-branches are reached via BST compare tree; each BST leaf calls
check_effect_slot_is_equip_activatable then a specialized eligibility predicate.

### Residual Auto-Name Slots: 92 total

- DAT_ slots: 56  (confirmed by grep, line range 2120-5060)
- DWORD_ slots: 27  (all DWORD_0805d... pattern)
- PTR_gP1LifePoints_* slots: 9  (uses PTR_ prefix; value = gP1LifePoints = 0x0201c4e0)

### ROM_INCBIN / .byte Blocks: 2

| addr | size | position |
|------|------|----------|
| 0x5dd3e | 0x1a (26B) | between check_equip_slot_pair_field6_field9_eligible and check_equip_slot_eligible_type6c0_by_gust_or_driving_snow (already listed) -- actually between check_equip_slot_eligible_type6c0_by_gust_or_driving_snow (ends 0x5dd3e) and check_equip_slot_pair_field6_field9_eligible (starts 0x5dd58) |
| 0x5ddda | 0xd2 (210B) | between check_equip_slot_pair_field6_field9_eligible (ends 0x5ddda) and check_equip_slot_eligible_with_lp_offset_threshold (starts 0x5deac) |

---

## Data Block Classification (Rule 2/3) -- ref-scan evidence

Ref-scan method: python reads roms/2343.gba, scans every 4B-aligned word in ROM for
struct.pack("<I", addr) (raw) and struct.pack("<I", addr|1) (THUMB). Dispatch table region
0x09e4xxxx confirmed: 24B records [CID u32][fn[0..4] u32x5], CID-adjacent THUMB+1 = true call ref.

### Block 1: 0x5dd3e, size 0x1a (26B)

Bytes (hex): 00000022fc21090140880140c020c000814200d10122101c7047

Structure:
- off=0x00: .zero 2 (alignment pad)
- off=0x02: THUMB sub-fn at 0x0805dd40 (24B THUMB: push {}, ldrb r0,[r0,#0x2], lsls/lsrs,
             ldr r2,[pc,#0x18], ldrb r1,[r2,r0], orrs r0,r1, movs r1,#0x1, ands r0,r1, bx lr)

ref-scan result (from background task output):
  off=0x02  addr=0x0805dd40  raw=0  thumb=1

Dispatch table lookup: THUMB ref 0x0805dd41 found at ROM offset 0x09e40318.
ROM record start 0x09e4030c: CID=0x0000134e (cid_134e, unassigned slot), fn[1]=0x0805dd41 at 0x09e40318
=> record: [0x134e][fn0][0x0805dd41][...] at 0x09e4030c

Judgment: **R4 DISASM** -- 1 THUMB hit, confirmed dispatch table CID 0x134e.
No sub-fn at off=0x00 (zero pad only).
1 sub-fn: fn_at_0x0805dd40.

| Block | sub-offset | thumb-ptr | raw | thumb | Judgment | Evidence |
|-------|-----------|-----------|-----|-------|----------|----------|
| 0x5dd3e (0x1a) | +0x02 -> 0x0805dd40 | 0x0805dd41 | 0 | 1 | disasm R4 | dispatch table record 0x09e4030c: CID=0x134e (cid_134e, REUSE card_info.inc line 1116), fn[1]=0x0805dd41 @ 0x09e40318 |

### Block 2: 0x5ddda, size 0xd2 (210B)

Bytes first 32 (hex): 0000021c51880805800e0f2802d0102804d00de051698902c90f02e00121d08a

Structure:
- off=0x00: .zero 2 (alignment pad)
- off=0x02: THUMB sub-fn at 0x0805dddc  (starts: 021c = adds r2,r0 / 5188 = ldrh r1,[r0])
- off=0x36: THUMB sub-fn at 0x0805de10
- off=0x76: THUMB sub-fn at 0x0805de50
- off=0xa2: THUMB sub-fn at 0x0805de7c

ref-scan result:
  off=0x02  addr=0x0805dddc  raw=0  thumb=2
  off=0x36  addr=0x0805de10  raw=0  thumb=2
  off=0x76  addr=0x0805de50  raw=0  thumb=1
  off=0xa2  addr=0x0805de7c  raw=0  thumb=1

Dispatch table lookup (per hit):
  0x0805dddd: 2 hits in 0x09e4xxxx region
    - 0x09e40378: CID=0x1352 (Numinous Healer), fn[1]=0x0805dddd
    - 0x09e40438: CID=0x135a (Attack and Receive), fn[1]=0x0805dddd
  0x0805de11: 2 hits in 0x09e4xxxx region
    - 0x09e40390: CID=0x1353 (Appropriate), fn[1]=0x0805de11
    - 0x09e43708: CID=0x1353 second dispatch entry, fn[1]=0x0805de11
  0x0805de51: 1 hit
    - 0x09e403a8: CID=0x1354 (Forced Requisition), fn[1]=0x0805de51
  0x0805de7d: 1 hit
    - 0x09e403c0: CID=0x1355 (Minor Goblin Official), fn[1]=0x0805de7d

Judgment: **R4 DISASM** -- 4 sub-functions, 6 total dispatch table THUMB hits.
All hits in confirmed 0x09e4xxxx dispatch table region. CIDs 0x1352/0x135a/0x1353/0x1354/0x1355
confirmed via card-stats.s slot= field lookups.

| Block | sub-offset | thumb-ptr | raw | thumb | Judgment | Evidence |
|-------|-----------|-----------|-----|-------|----------|----------|
| 0x5ddda (0xd2) | +0x02 -> 0x0805dddc | 0x0805dddd | 0 | 2 | disasm R4 | 0x09e40378 CID=0x1352(Numinous Healer), 0x09e40438 CID=0x135a(Attack and Receive) |
| 0x5ddda (0xd2) | +0x36 -> 0x0805de10 | 0x0805de11 | 0 | 2 | disasm R4 | 0x09e40390 CID=0x1353(Appropriate), 0x09e43708 same CID second entry |
| 0x5ddda (0xd2) | +0x76 -> 0x0805de50 | 0x0805de51 | 0 | 1 | disasm R4 | 0x09e403a8 CID=0x1354(Forced Requisition) |
| 0x5ddda (0xd2) | +0xa2 -> 0x0805de7c | 0x0805de7d | 0 | 1 | disasm R4 | 0x09e403c0 CID=0x1355(Minor Goblin Official) |

---

## Symbolization Plan

### EQ_SLOTS (data-equate -- 65 slots)

**Reuse ewram.inc: PLAYER_BLOCK_STRIDE = 0x868** (ewram.inc confirmed: ".equ PLAYER_BLOCK_STRIDE, 0x868"; 2146 raw refs)

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805d100 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d100 |
| 0x0805d4a4 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d4a4 |
| 0x0805d720 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d720 |
| 0x0805d7fc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d7fc |
| 0x0805d880 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d880 |
| 0x0805d908 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d908 |
| 0x0805d98c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805d98c |
| 0x0805db48 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805db48 |
| 0x0805df08 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805df08 |
| 0x0805df90 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805df90 |
| 0x0805dffc | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805dffc |
| 0x0805e090 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805e090 |
| 0x0805e148 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805e148 |
| 0x0805e250 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805e250 |
| 0x0805e27c | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805e27c |
| 0x0805e0e0 | 0x00000868 | PLAYER_BLOCK_STRIDE | player_block_stride_0805e0e0 |

**Reuse ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8** (ewram.inc confirmed: ".equ P1LP_BLOCK2_OFF_1CE8, 0x1ce8"; 184 ROM refs)

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805d058 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805d058 |
| 0x0805d640 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805d640 |
| 0x0805d984 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805d984 |
| 0x0805da68 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805da68 |
| 0x0805dff4 | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805dff4 |
| 0x0805e08c | 0x00001ce8 | P1LP_BLOCK2_OFF_1CE8 | p1lp_block2_off_0805e08c |

**Reuse duel_field.inc: FIELD_STATE_OFF = 0x1cf4** (duel_field.inc confirmed: ".equ FIELD_STATE_OFF, 0x00001cf4"; comment confirms asm/07 STAGE_OFF/FIELD_STATE_OFFSET)

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805d05c | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805d05c |
| 0x0805d0fc | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805d0fc |
| 0x0805d3cc | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805d3cc |
| 0x0805da64 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805da64 |
| 0x0805dff8 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805dff8 |
| 0x0805e088 | 0x00001cf4 | FIELD_STATE_OFF | field_state_off_0805e088 |

**Reuse duel_field.inc: EFFECT_ZONE_BITMASK_OFF = 0x10d0** (duel_field.inc confirmed: ".equ EFFECT_ZONE_BITMASK_OFF, 0x10d0"; comment: "[gP1LifePoints+0x10d0]")

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805d988 | 0x000010d0 | EFFECT_ZONE_BITMASK_OFF | effect_zone_bitmask_off_0805d988 |

**NEW ewram.inc: P2_ZONE1_LP_OFF = 0x87c** (not in any constants/*.inc; grep "0x87c" returns only SWORDS_OF_CONCEALING_LIGHT_CID=0x187c which is unrelated)
Consumer: check_spell_zone_chain_occupied_eligible (asm/07 line 3188-3240): reads [gP1LifePoints + 0x87c],
computes player_id via bit0, then adds r1=gP1LifePoints, r2=0x87c -> ldr r0,[r0+r1]. 0x87c = 0x868
(PLAYER_BLOCK_STRIDE) + 0x14 (one zone slot stride). The field at gP1LifePoints+0x87c is the first
slot entry of P2's zone array region (P2 block base + 0x14-stride offset). Semantics: P2 zone-1 LP field.
Confidence: med (offset derivation is structural; "zone-1 LP" label may overspecify -- mark for reviewer).

| slot | value | const_name | slot_label |
|------|-------|------------|------------|
| 0x0805d798 | 0x0000087c | P2_ZONE1_LP_OFF | p2_zone1_lp_off_0805d798 |

**CID EQ slots -- REUSE card_info.inc**
grep evidence per CID listed inline.

| slot | value | const_name | reuse/new | slot_label |
|------|-------|------------|-----------|------------|
| 0x0805d188 | 0x000015f1 | SPELL_SHIELD_TYPE8_CID | REUSE card_info.inc: ".equ SPELL_SHIELD_TYPE8_CID, 0x000015f1" | spell_shield_type8_cid_0805d188 |
| 0x0805d1a4 | 0x000012ff | SEVEN_TOOLS_OF_THE_BANDIT_CID | REUSE card_info.inc: ".equ SEVEN_TOOLS_OF_THE_BANDIT_CID, 0x000012ff" | seven_tools_cid_0805d1a4 |
| 0x0805d1b4 | 0x0000131c | cid_131c | REUSE card_info.inc: ".equ cid_131c, 0x0000131c" | cid_131c_0805d1b4 |
| 0x0805d1dc | 0x000014b6 | DARK_BALTER_THE_TERRIBLE_CID | REUSE card_info.inc: ".equ DARK_BALTER_THE_TERRIBLE_CID, 0x000014b6" | dark_balter_cid_0805d1dc |
| 0x0805d24c | 0x000017c6 | SORCERER_OF_DARK_MAGIC_CID | REUSE card_info.inc: ".equ SORCERER_OF_DARK_MAGIC_CID, 0x000017c6" | sorcerer_dark_magic_cid_0805d24c |
| 0x0805d250 | 0x000016a6 | SPELL_VANISHING_CID | REUSE card_info.inc: ".equ SPELL_VANISHING_CID, 0x000016a6" | spell_vanishing_cid_0805d250 |
| 0x0805d260 | 0x00001634 | ANTI_SPELL_CID | REUSE card_info.inc: ".equ ANTI_SPELL_CID, 0x00001634" | anti_spell_cid_0805d260 |
| 0x0805d2e0 | 0x000019e1 | GOBLIN_OUT_OF_FRYING_PAN_CID | REUSE card_info.inc: ".equ GOBLIN_OUT_OF_FRYING_PAN_CID, 0x000019e1" | goblin_frying_pan_cid_0805d2e0 |
| 0x0805d2f0 | 0x000019e2 | MALFUNCTION_CID | REUSE card_info.inc: ".equ MALFUNCTION_CID, 0x000019e2" | malfunction_cid_0805d2f0 |
| 0x0805d338 | 0x000012ea | MONSTER_REBORN_CID | REUSE card_info.inc: ".equ MONSTER_REBORN_CID, 0x000012ea" | monster_reborn_cid_0805d338 |
| 0x0805d384 | 0x00001246 | HARPIES_FEATHER_DUSTER_CID | REUSE card_info.inc: ".equ HARPIES_FEATHER_DUSTER_CID, 0x00001246" | harpies_feather_duster_cid_0805d384 |
| 0x0805d510 | 0x00001332 | BANISHER_OF_THE_LIGHT_CID | REUSE card_info.inc: ".equ BANISHER_OF_THE_LIGHT_CID, 0x00001332" | banisher_of_light_cid_0805d510 |
| 0x0805d524 | 0x000012ec | POT_OF_GREED_CID | REUSE card_info.inc: ".equ POT_OF_GREED_CID, 0x000012ec" | pot_of_greed_cid_0805d524 |
| 0x0805d5f0 | 0x000018a6 | EHERO_AVIAN_CID | REUSE card_info.inc: ".equ EHERO_AVIAN_CID, 0x000018a6" | ehero_avian_cid_0805d5f0 |
| 0x0805d6f0 | 0x00001325 | DELINQUENT_DUO_CID | REUSE card_info.inc: ".equ DELINQUENT_DUO_CID, 0x00001325" | delinquent_duo_cid_0805d6f0 |
| 0x0805d6fc | 0x0000132b | THE_FORCEFUL_SENTRY_CID | REUSE card_info.inc: ".equ THE_FORCEFUL_SENTRY_CID, 0x0000132b" | forceful_sentry_cid_0805d6fc |
| 0x0805dad4 | 0x0000135d | LIGHT_OF_INTERVENTION_CID | REUSE card_info.inc: ".equ LIGHT_OF_INTERVENTION_CID, 0x0000135d" | light_of_intervention_cid_0805dad4 |
| 0x0805dcc8 | 0x0000134d | DRIVING_SNOW_CID | REUSE card_info.inc: ".equ DRIVING_SNOW_CID, 0x0000134d" | driving_snow_cid_0805dcc8 |
| 0x0805dd80 | 0x00001350 | cid_1350 | REUSE card_info.inc: ".equ cid_1350, 0x00001350" | cid_1350_0805dd80 |
| 0x0805dd8c | 0x00001351 | cid_1351 | REUSE card_info.inc: ".equ cid_1351, 0x00001351" | cid_1351_0805dd8c |
| 0x0805d18c | 0x0000140d | MAGIC_DRAIN_CID | NEW -- card-stats.s "@ Magic Drain  slot=0x140D"; grep card_info.inc "0x140d": 0 hits | magic_drain_cid_0805d18c |
| 0x0805d190 | 0x000012f7 | cid_12f7 | NEW -- card-stats.s "slot=0x12f7": 0 records (UNASSIGNED); grep card_info.inc "0x12f7": 0 hits; neutral low-conf name | cid_12f7_0805d190 |
| 0x0805d1ec | 0x0000148f | RIRYOKU_FIELD_CID | NEW -- card-stats.s "@ Riryoku Field  slot=0x148F"; grep card_info.inc "0x148f": 0 hits | riryoku_field_cid_0805d1ec |
| 0x0805d208 | 0x0000153e | TUTAN_MASK_CID | NEW -- card-stats.s "@ Tutan Mask  slot=0x153E"; grep card_info.inc "0x153e": 0 hits | tutan_mask_cid_0805d208 |
| 0x0805d218 | 0x00001541 | CURSE_OF_ROYAL_CID | NEW -- card-stats.s "@ Curse of Royal  slot=0x1541"; grep card_info.inc "0x1541": 0 hits (NEEDLE_CEILING_CID=0x1542 present, this is 0x1541) | curse_of_royal_cid_0805d218 |
| 0x0805d27c | 0x00001721 | TRAP_JAMMER_CID | NEW -- card-stats.s "@ Trap Jammer  slot=0x1721"; grep card_info.inc "0x1721": 0 hits | trap_jammer_cid_0805d27c |
| 0x0805d28c | 0x0000176b | ARMOR_BREAK_CID | NEW -- card-stats.s "@ Armor Break  slot=0x176B"; grep card_info.inc "0x176b": 0 hits | armor_break_cid_0805d28c |
| 0x0805d2b4 | 0x000018de | ROYAL_SURRENDER_CID | NEW -- card-stats.s "@ Royal Surrender  slot=0x18DE"; grep card_info.inc "0x18de": 0 hits | royal_surrender_cid_0805d2b4 |
| 0x0805d2c4 | 0x000018dd | SPELL_STOPPING_STATUTE_CID | NEW -- card-stats.s "@ Spell-Stopping Statute  slot=0x18DD"; grep card_info.inc "0x18dd": 0 hits | spell_stopping_statute_cid_0805d2c4 |
| 0x0805d314 | 0x000010f6 | DARK_HOLE_CID | NEW -- card-stats.s "@ Dark Hole  slot=0x10F6"; grep card_info.inc "0x10f6": 0 hits | dark_hole_cid_0805d314 |
| 0x0805d35c | 0x000010f7 | RAIGEKI_CID | NEW -- card-stats.s "@ Raigeki  slot=0x10F7"; grep card_info.inc "0x10f7": 0 hits | raigeki_cid_0805d35c |
| 0x0805dcd4 | 0x0000135b | cid_135b | NEW -- card-stats.s "slot=0x135b": 0 records (UNASSIGNED); grep card_info.inc "0x135b": 0 hits; neutral low-conf name | cid_135b_0805dcd4 |
| 0x0805e2f8 | 0x00001288 | ALPHA_MAGNET_WARRIOR_CID | NEW -- card-stats.s "@ Alpha The Magnet Warrior  slot=0x1288"; grep card_info.inc "0x1288": 0 hits | alpha_magnet_warrior_cid_0805e2f8 |
| 0x0805e2fc | 0x0000129b | BETA_MAGNET_WARRIOR_CID | NEW -- card-stats.s "@ Beta The Magnet Warrior  slot=0x129B"; grep card_info.inc "0x129b": 0 hits | beta_magnet_warrior_cid_0805e2fc |
| 0x0805e300 | 0x000012b8 | GAMMA_MAGNET_WARRIOR_CID | NEW -- card-stats.s "@ Gamma The Magnet Warrior  slot=0x12B8"; grep card_info.inc "0x12b8": 0 hits | gamma_magnet_warrior_cid_0805e300 |

Appropriate/Numinous Healer/Forced Requisition/Minor Goblin Official/Attack and Receive
(CIDs 0x1352-0x1355, 0x135a) appear only in the disasm blocks (not as EQ_SLOTS in code).
The dispatch table entries reference them as handler targets. No DAT_/DWORD_ slots
in the main code section hold these CIDs as equates; they are identified only via ref-scan.

### REF_SLOTS (USER-label + DATA-ref -- 27 slots)

Note on PTR_ prefix: Ghidra auto-labels pointer slots as PTR_gP1LifePoints_<addr>. The fixer
should rename these slot labels; the Ghidra renaming of the slot data-label is what clears the DAT_/PTR_ prefix.

**gP1LifePoints = 0x0201c4e0** (ewram.inc confirmed: ".equ gP1LifePoints, 0x0201C4E0")
All 14 slots reference gP1LifePoints directly (pointer to P1 LP struct base used as indexed load base).

| slot | value | gas_label | slot_label |
|------|-------|-----------|------------|
| 0x0805d054 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d054 |
| 0x0805d3c8 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d3c8 |
| 0x0805d63c | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d63c |
| 0x0805d71c | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d71c |
| 0x0805d794 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d794 |
| 0x0805d7f8 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d7f8 |
| 0x0805da60 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805da60 |
| 0x0805dcc4 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805dcc4 |
| 0x0805d980 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805d980 |
| 0x0805df04 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805df04 |
| 0x0805dff0 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805dff0 |
| 0x0805e084 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805e084 |
| 0x0805e144 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805e144 |
| 0x0805e278 | 0x0201c4e0 | gP1LifePoints | p1lp_ptr_0805e278 |

**gDuelFieldSlots = 0x0201c510** (ewram.inc confirmed: ".equ gDuelFieldSlots, 0x0201c510"; 1007 raw refs)

| slot | value | gas_label | slot_label |
|------|-------|-----------|------------|
| 0x0805d4a8 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805d4a8 |
| 0x0805d884 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805d884 |
| 0x0805d90c | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805d90c |
| 0x0805db4c | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805db4c |
| 0x0805df8c | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805df8c |
| 0x0805e0e4 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805e0e4 |
| 0x0805e254 | 0x0201c510 | gDuelFieldSlots | duel_field_slots_0805e254 |

**gEquipChainSlotRefs = 0x0201bb90** (ewram.inc confirmed: ".equ gEquipChainSlotRefs, 0x0201bb90"; 260 raw refs)
Note: three of the four consumer functions use this as active-deck struct base
(check_spell_type480_active_deck_matches, check_spell_type500_deck_states_differ,
check_equip_slot_eligible_with_neo_daedalus_and_both_players,
check_equip_slot_eligible_type3c0_with_deck_prereqs_and_field14).
The address is the same global; dual usage confirmed in Seg-1 review (F07-Seg-1). Slot label
reflects the global name without disambiguation.

| slot | value | gas_label | slot_label |
|------|-------|-----------|------------|
| 0x0805d9c4 | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805d9c4 |
| 0x0805e0dc | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805e0dc |
| 0x0805e1fc | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805e1fc |
| 0x0805e34c | 0x0201bb90 | gEquipChainSlotRefs | equip_chain_slot_refs_0805e34c |

**gDuelPhaseFlags = 0x0201b290** (ewram.inc confirmed: ".equ gDuelPhaseFlags, 0x0201b290"; 676 raw refs)
Consumer: invoke_effect_node_handler_with_zone_flag_guard (asm/07 line 3844-3856): loads
gDuelPhaseFlags, computes movs r0,#0x98; lsls r0,#3 -> r0=0x4c0; adds gDuelPhaseFlags+0x4c0=0x0201b750;
stores result there (equip activation side flag field). Offset 0x4c0 is NOT defined in ewram.inc yet
(ewram.inc has LP_BAR_DISPLAY_CTR_OFF=0x4c4 and LP_BAR_ANIM_STATE_OFF=0x4cc, but not 0x4c0).
The 0x4c0 offset is encoded inline as an immediate computation; it does not appear as a literal pool
slot, so no additional EQ slot is needed for it -- the immediate is visible in asm as two instructions.

| slot | value | gas_label | slot_label |
|------|-------|-----------|------------|
| 0x0805db50 | 0x0201b290 | gDuelPhaseFlags | duel_phase_flags_0805db50 |

**check_equip_slot_eligible_by_equip_type+1 = 0x08051319** (fn ptr; THUMB bit set)
Consumer: check_field_active_slot_or_zone_pair (asm/07 line 4381-4435): calls
invoke_count_zone_pair_hits_full_range with fn_ptr=0x08051319. Target fn at 0x08051318 =
check_equip_slot_eligible_by_equip_type (asm/05_equip_eligibility_a.s line 18412, confirmed by
asm/02 plate comment listing 0x08051318 as caller context). ROM verify: struct.unpack_from('<I',
rom, 0x0805df94-0x8000000) = 0x08051319. Confidence: high.

| slot | value | gas_label | slot_label |
|------|-------|-----------|------------|
| 0x0805df94 | 0x08051319 | check_equip_slot_eligible_by_equip_type+1 | equip_type_check_fn_ptr_0805df94 |

### RENAME_SLOTS (slot label rename only; no equate change -- 0 slots)

All 92 slots receive a new label via EQ_SLOTS or REF_SLOTS above. No slot requires rename-only
treatment (all auto-names carry the DAT_/DWORD_/PTR_ prefix that needs clearing).

### FUNC_RENAME (none)

No function body contradicts its current name. All 35 function names are semantically consistent
with their observed behavior (predicate cluster for equip/spell/zone effect eligibility).

### PLATE (R5 -- 3 plates proposed)

**check_equip_zone_effect_eligible_by_card_id (0x0805d118)**
Existing plate (if any) should include: BST over 32+ card IDs routing to specialized eligibility
predicates. Replace or supplement existing plate with:
"BST gate: reads card_id from [r0+0], performs binary-search-style cmp/branch over 32 card IDs
(range 0x10f6..0x19e2). Each leaf: calls check_effect_slot_is_equip_activatable then a
per-card-set predicate (check_spell_zone_effect_activatable / check_equip_zone_has_field5_card /
check_monster_slots_nonzero_for_card_player etc). Returns r0=0 or 1."

**invoke_effect_node_handler_with_zone_flag_guard (0x0805dae0)**
"Zone flag guard: r0=effect_node_ptr, r1=player_id_byte, r2=slot_type. Guards: r0==0 or
zone_bit12==0 or side/type already matched (read_effect_slot_side_and_type) -> return 0.
Sets [gDuelPhaseFlags+0x4c0]=player_id_bit, calls
set_equip_activation_state_by_mode_alt(effect_node, player_id_byte, slot_type), then
clears [gDuelPhaseFlags+0x4c0]=0. Returns result of set_equip_activation_state_by_mode_alt."

**check_field_active_slot_or_zone_pair (0x0805df60)**
"Outer loop player=[0..1], inner loop slot=[0..4] x stride 0x14: checks gDuelFieldSlots entry
bit19 nonzero AND [+8]=0 AND [+6]!=0 => return 1 immediately. Fallback: calls
invoke_count_zone_pair_hits_full_range(equip_slot_ptr, fn_ptr=check_equip_slot_eligible_by_equip_type);
result>0 => return 1, else return 0."

---

## carve plan (R7) -- none

Both ROM_INCBIN blocks classify as R4 DISASM. No carve-to-rom.s plan.

---

## disasm plan (R4)

### Block 1: 0x5dd3e size 0x1a -- 1 THUMB sub-function

Range to disasm: 0x0805dd40..0x0805dd57 (24B = 12 THUMB instructions).
Steps (Ghidra):
1. clearListing 0x0805dd3e 0x0805dd57  (clears the ROM_INCBIN block + 2B pad)
2. createWord 0x0805dd3e  (re-label the 2B alignment pad [0x5dd3e,0x5dd3f] as .hword; does not overlap sub-fn at 0x5dd40)
3. setTMode 0x0805dd40 true
4. DisassembleCommand 0x0805dd40  (single sub-fn, 24B until bx lr)
5. createFunction 0x0805dd40  "check_equip_zone_eligible_cid_134e"

Function naming: The sub-fn serves CID 0x134e (unassigned slot). Name follows the dispatch
handler naming pattern: check_equip_zone_eligible_cid_134e. Confidence: med (based on
structural role; card name unknown for 0x134e).

### Block 2: 0x5ddda size 0xd2 -- 4 THUMB sub-functions

Range to disasm: 0x0805dddc..0x0805deab (4 sub-fns total).
Steps (Ghidra):
1. clearListing 0x0805ddda 0x0805deab  (full block range)
2. setTMode 0x0805dddc true
3. DisassembleCommand 0x0805dddc  (sub-fn 1: until bx; ends before 0x0805de10)
4. createFunction 0x0805dddc  "check_equip_zone_eligible_numinous_healer_and_recv"
   (serves CIDs 0x1352 Numinous Healer AND 0x135a Attack and Receive -- shared handler)
5. DisassembleCommand 0x0805de10  (sub-fn 2: ends before 0x0805de50)
6. createFunction 0x0805de10  "check_equip_zone_eligible_appropriate"
   (serves CID 0x1353 Appropriate)
7. DisassembleCommand 0x0805de50  (sub-fn 3: ends before 0x0805de7c)
8. createFunction 0x0805de50  "check_equip_zone_eligible_forced_requisition"
   (serves CID 0x1354 Forced Requisition)
9. DisassembleCommand 0x0805de7c  (sub-fn 4: ends before 0x0805deac)
10. createFunction 0x0805de7c  "check_equip_zone_eligible_minor_goblin_official"
    (serves CID 0x1355 Minor Goblin Official)

Note: sub-fn boundaries inferred from ref-scan offsets (0x02, 0x36, 0x76, 0xa2). Actual boundaries
may shift by a few bytes -- Ghidra disasm will show where each bx/pop{pc}/mov pc,lr ends.
The clearListing+setTMode+DisassembleCommand per-sub-fn sequence (not whole-block disasm) prevents
ContextChangeException as documented in MEMORY.md.

---

## New constants / globals required

### New in card_info.inc (19 CIDs)

| equate | value | card name | evidence |
|--------|-------|-----------|----------|
| DARK_HOLE_CID | 0x000010f6 | Dark Hole | card-stats.s "@ Dark Hole  slot=0x10F6 pw=53129443"; grep card_info.inc "0x10f6": 0 hits; conf: high |
| RAIGEKI_CID | 0x000010f7 | Raigeki | card-stats.s "@ Raigeki  slot=0x10F7 pw=12580477"; grep card_info.inc "0x10f7": 0 hits; conf: high |
| ALPHA_MAGNET_WARRIOR_CID | 0x00001288 | Alpha The Magnet Warrior | card-stats.s "@ Alpha The Magnet Warrior  slot=0x1288 pw=99785935"; grep card_info.inc "0x1288": 0 hits; conf: high |
| BETA_MAGNET_WARRIOR_CID | 0x0000129b | Beta The Magnet Warrior | card-stats.s "@ Beta The Magnet Warrior  slot=0x129B pw=39256679"; grep card_info.inc "0x129b": 0 hits; conf: high |
| GAMMA_MAGNET_WARRIOR_CID | 0x000012b8 | Gamma The Magnet Warrior | card-stats.s "@ Gamma The Magnet Warrior  slot=0x12B8 pw=27175001"; grep card_info.inc "0x12b8": 0 hits; conf: high |
| cid_12f7 | 0x000012f7 | UNASSIGNED | card-stats.s: no record with slot=0x12f7; neighbors 0x12f8=Tribute to the Doomed, 0x12f9=Soul Release; conf: low |
| MAGIC_DRAIN_CID | 0x0000140d | Magic Drain | card-stats.s "@ Magic Drain  slot=0x140D pw=59344077"; grep card_info.inc "0x140d": 0 hits; conf: high |
| RIRYOKU_FIELD_CID | 0x0000148f | Riryoku Field | card-stats.s "@ Riryoku Field  slot=0x148F pw=70344351"; grep card_info.inc "0x148f": 0 hits; conf: high |
| TUTAN_MASK_CID | 0x0000153e | Tutan Mask | card-stats.s "@ Tutan Mask  slot=0x153E pw=86120751"; grep card_info.inc "0x153e": 0 hits; conf: high |
| CURSE_OF_ROYAL_CID | 0x00001541 | Curse of Royal | card-stats.s "@ Curse of Royal  slot=0x1541 pw=02314238"; grep card_info.inc "0x1541": 0 hits (NEEDLE_CEILING_CID=0x1542 is different); conf: high |
| TRAP_JAMMER_CID | 0x00001721 | Trap Jammer | card-stats.s "@ Trap Jammer  slot=0x1721 pw=19737124"; grep card_info.inc "0x1721": 0 hits; conf: high |
| ARMOR_BREAK_CID | 0x0000176b | Armor Break | card-stats.s "@ Armor Break  slot=0x176B pw=79649195"; grep card_info.inc "0x176b": 0 hits; conf: high |
| NUMINOUS_HEALER_CID | 0x00001352 | Numinous Healer | card-stats.s "@ Numinous Healer  slot=0x1352 pw=02130625"; grep card_info.inc "0x1352": 0 hits; conf: high |
| FORCED_REQUISITION_CID | 0x00001354 | Forced Requisition | card-stats.s "@ Forced Requisition  slot=0x1354 pw=74923978"; grep card_info.inc "0x1354": 0 hits; conf: high |
| MINOR_GOBLIN_OFFICIAL_CID | 0x00001355 | Minor Goblin Official | card-stats.s "@ Minor Goblin Official  slot=0x1355 pw=01918087"; grep card_info.inc "0x1355": 0 hits; conf: high |
| ATTACK_AND_RECEIVE_CID | 0x0000135a | Attack and Receive | card-stats.s "@ Attack and Receive  slot=0x135A pw=93553943"; grep card_info.inc "0x135a": 0 hits; conf: high |
| cid_135b | 0x0000135b | UNASSIGNED | card-stats.s: no record with slot=0x135b; neighbors 0x135a=Attack and Receive, 0x135c=Ceasefire; conf: low |
| SPELL_STOPPING_STATUTE_CID | 0x000018dd | Spell-Stopping Statute | card-stats.s "@ Spell-Stopping Statute  slot=0x18DD pw=10048942"; grep card_info.inc "0x18dd": 0 hits; conf: high |
| ROYAL_SURRENDER_CID | 0x000018de | Royal Surrender | card-stats.s "@ Royal Surrender  slot=0x18DE pw=56058951"; grep card_info.inc "0x18de": 0 hits; conf: high |

### New in ewram.inc (1 offset)

| equate | value | context | confidence |
|--------|-------|---------|------------|
| P2_ZONE1_LP_OFF | 0x0000087c | [gP1LifePoints+0x87c] = P2 zone-1 LP region start; 0x87c = PLAYER_BLOCK_STRIDE(0x868) + 0x14 (one zone slot stride); check_spell_zone_chain_occupied_eligible asm/07 line 3228-3240; grep all constants/*.inc "0x87c": 0 semantic hits (0x187c is a CID value, unrelated) | med |

---

## Section 5.1 Registry (Rule 3 -- 0 reference blocks)

None. Both ROM_INCBIN blocks have confirmed ROM references (dispatch table THUMB hits). No blocks
qualify for Section 5.1.

---

## Consumer Evidence (R6) -- key slot semantics

| slot/global | value | consumer fn | file:line | semantic | confidence |
|-------------|-------|-------------|-----------|----------|------------|
| gP1LifePoints | 0x0201c4e0 | check_spell_zone_effect_activatable | asm/07 line 2172 | P1 LP base ptr for indexed load [gP1LP + player*0x868 + 0x1ce8] | high |
| P1LP_BLOCK2_OFF_1CE8 | 0x1ce8 | check_spell_zone_effect_activatable | asm/07 line 2173 | LP display block2 field offset | high |
| FIELD_STATE_OFF | 0x1cf4 | check_monster_zone_field_state_eligible | asm/07 line 2200 | equip activation phase/field state code at [gDuelFieldSlots+0x1cf4] | high |
| PLAYER_BLOCK_STRIDE | 0x868 | check_monster_zone_field_state_eligible | asm/07 line 2215 | multiplied by player_id to index P1/P2 LP block | high |
| SPELL_SHIELD_TYPE8_CID | 0x15f1 | check_equip_zone_effect_eligible_by_card_id | asm/07 line 2337 | BST leaf node (card ID 0x15f1 = Spell Shield Type-8) | high |
| gEquipChainSlotRefs | 0x0201bb90 | check_spell_type480_active_deck_matches | asm/07 line 3603 | loaded as deck struct base; compares [+0] vs [+player*4] | high |
| gDuelPhaseFlags | 0x0201b290 | invoke_effect_node_handler_with_zone_flag_guard | asm/07 line 3844 | base for +0x4c0 (=0x98<<3) equip activation side flag write | high |
| check_equip_slot_eligible_by_equip_type+1 | 0x08051319 | check_field_active_slot_or_zone_pair | asm/07 line 4423 | fn_ptr passed to invoke_count_zone_pair_hits_full_range as slot-test callback | high |
| gDuelFieldSlots | 0x0201c510 | check_any_equip_slot_available_either_player | asm/07 line 2814-2837 | outer player / inner slot iteration base: player*0x868 + slot*0x14 | high |
| P2_ZONE1_LP_OFF | 0x87c | check_spell_zone_chain_occupied_eligible | asm/07 line 3228 | adds r0=gP1LifePoints, r2=0x87c -> loads [gP1LP+0x87c] (P2 zone-1 entry) | med |

---

## Help requests

1. **P2_ZONE1_LP_OFF (0x87c)**: The offset 0x87c = PLAYER_BLOCK_STRIDE(0x868) + 0x14 is used in
   check_spell_zone_chain_occupied_eligible to read a word at [gP1LifePoints+0x87c]. The structural
   derivation is clear but the exact semantic of "P2 zone-1 LP field" may overspecify. If reviewer
   finds a better name or existing constant, please substitute.

2. **cid_12f7 (0x12f7) and cid_135b (0x135b)**: Both are unassigned slots with no card record in
   card-stats.s. Named with neutral low-confidence convention. If any cross-file evidence of a card
   name surfaces for these slots, please update.

3. **Sub-function boundary confirmation for Block 2 disasm**: The four sub-fn start offsets
   (+0x02, +0x36, +0x76, +0xa2) are confirmed by THUMB ref-scan hits. The end boundary of each
   sub-fn (bx lr / pop+bx pattern) should be confirmed after clearListing+DisassembleCommand in
   Ghidra before createFunction call.

---

## Executor Report: F07-Seg-2

- Slots: EQ=65 REF=27 RENAME=0 FUNC_RENAME=0 PLATE=3
- carve=0 disasm=2 blocks (1+4 sub-fns = 5 total sub-functions) Sec5.1=0
- New constants/globals: card_info.inc: 19 new CIDs (DARK_HOLE_CID/RAIGEKI_CID/ALPHA_MAGNET_WARRIOR_CID/BETA_MAGNET_WARRIOR_CID/GAMMA_MAGNET_WARRIOR_CID/cid_12f7/MAGIC_DRAIN_CID/RIRYOKU_FIELD_CID/TUTAN_MASK_CID/CURSE_OF_ROYAL_CID/TRAP_JAMMER_CID/ARMOR_BREAK_CID/NUMINOUS_HEALER_CID/FORCED_REQUISITION_CID/MINOR_GOBLIN_OFFICIAL_CID/ATTACK_AND_RECEIVE_CID/cid_135b/SPELL_STOPPING_STATUTE_CID/ROYAL_SURRENDER_CID); ewram.inc: P2_ZONE1_LP_OFF=0x87c (new, med-conf)
- Help: 3 items (P2_ZONE1_LP_OFF naming, cid_12f7/cid_135b unassigned, disasm boundary confirmation)
- proposal: doc/dev/refine/F07-Seg-2.proposal.md
