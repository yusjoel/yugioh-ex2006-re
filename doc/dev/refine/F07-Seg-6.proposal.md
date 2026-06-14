# Refine Proposal: F07-Seg-6  [0x08060898..0x080613b4)

## 段测绘
- 函数入口: 34 个 (all already named, no new FUN_ stubs)
  - check_equip_slot_eligible_by_lp_slot_and_effect_dispatch @ 0x08060898
  - check_equip_slot_eligible_by_effect_sum_vs_tier @ 0x080608e0
  - check_equip_slot_eligible_by_combined_player_effect_sum @ 0x08060908
  - check_equip_slot_eligible_by_owner_match_and_effect_dispatch @ 0x08060938
  - check_equip_slot_eligible_by_effect_sum_vs_tier__08060974 @ 0x08060974 (CJK plate)
  - check_equip_slot_eligible_neo_daedalus_with_monster_placeable @ 0x080609a4
  - check_equip_slot_eligible_by_tier_and_effect_handler @ 0x080609d0
  - check_equip_slot_eligible_zone_e_type580_with_field5 @ 0x080609fc
  - check_equip_slot_eligible_chain_present_with_neo_daedalus @ 0x08060a5c (CJK plate)
  - [Block1 fn] check_exodia_set_in_extra_for_cid_165b @ 0x08060a88 (in ROM_INCBIN)
  - check_equip_slot_eligible_by_tier_and_banisher_scan @ 0x08060b18
  - check_equip_slot_eligible_neo_daedalus_with_opponent_slot_count @ 0x08060b4c
  - check_equip_slot_eligible_neo_daedalus_with_state12_loop @ 0x08060b80
  - check_equip_slot_eligible_by_friendship_or_unity_in_extra @ 0x08060bf8
  - check_equip_slot_eligible_by_companion_card_and_paired_slot @ 0x08060c30 (CJK plate)
  - check_equip_slot_eligible_terrorking_archfiend_with_banisher_guard @ 0x08060c94
  - check_equip_slot_eligible_by_lp_advantage_2000 @ 0x08060d08
  - check_equip_slot_eligible_dark_scorpion_full_team_paired @ 0x08060d48
  - check_equip_slot_eligible_by_node_absent_in_chain_zone_b @ 0x08060de0
  - check_equip_slot_eligible_by_effect_dispatch_result @ 0x08060e04
  - check_equip_slot_eligible_by_field6_guard_and_chain_absent @ 0x08060e24 (CJK plate)
  - check_equip_slot_eligible_crimson_ninja_absent_with_spell_zone @ 0x08060e5c
  - check_equip_slot_eligible_with_chain_absent_and_spell_dispatch @ 0x08060ea8
  - check_equip_slot_eligible_by_effect_node_absent_in_zone_b @ 0x08060ee0
  - check_equip_slot_eligible_by_zone_slot_field_correlation @ 0x08060f08
  - check_equip_slot_eligible_chain_absent_with_spell_zone_and_display @ 0x08060fe8 (CJK plate)
  - check_slot_at_zone_e_with_field5_active @ 0x08061018
  - [Block2 fn] check_zone_type580_direction_mismatch_for_cid_16c6 @ 0x08061070 (in ROM_INCBIN)
  - check_equip_slot_eligible_by_dual_zone_flags_and_chain @ 0x0806109c
  - check_equip_slot_eligible_bls_envoy_absent_with_zone_field_match @ 0x08061110
  - check_ojama_trio_all_paired_slots_present @ 0x080611d0
  - [Block3 fn] check_lp_zone_hand_above6_for_cid_16d1 @ 0x0806121c (in ROM_INCBIN)
  - check_equip_slot_eligible_by_hand_count_and_zone_status @ 0x08061244
  - check_equip_slot_eligible_with_bls_or_ced_envoy_paired @ 0x0806129c
  - check_equip_slot_eligible_neo_daedalus_with_hand_empty @ 0x080612e4 (CJK plate)
  - check_equip_slot_eligible_by_lp_minus_zone_positive @ 0x0806131c
  - check_equip_slot_eligible_by_effect_type_e_and_zone_field5 @ 0x08061338
- 残留自动名槽: 47 个 DAT_/DWORD_ + 3 个 PTR_ = 50 total
  - PTR_gP1LifePoints_080608d0 = 0x0201c4e0  (PTR-style, already named, skip per scope convention)
  - PTR_gP1LifePoints_08061064 = 0x0201c4e0  (same, skip)
  - PTR_gP1LifePoints_080610fc = 0x0201c4e0  (same, skip)
  - DAT_080608d4 = 0x00000868
  - DWORD_08060954 = 0x0201c4e0
  - DWORD_08060958 = 0x00001ce8
  - DWORD_08060a50 = 0x0201c4e0
  - DWORD_08060bf0 = 0x0201c4e0
  - DWORD_08060bf4 = 0x00000868
  - DWORD_08060c20 = 0x0000167a
  - DWORD_08060c24 = 0x0000167b
  - DWORD_08060c50 = 0x0000167e
  - DWORD_08060c5c = 0x0000169e
  - DWORD_08060c64 = 0x0000157f
  - DWORD_08060c6c = 0x0000129e
  - DWORD_08060c88 = 0x00001532
  - DWORD_08060cf0 = 0x00001332
  - DWORD_08060cf4 = 0x00f88000
  - DWORD_08060cf8 = 0x0201c4e0
  - DWORD_08060cfc = 0x00001691
  - DWORD_08060d40 = 0x0201c4e0
  - DWORD_08060d44 = 0x00000868
  - DWORD_08060db8 = 0x0201c4e0
  - DWORD_08060dbc = 0x00001ce8
  - DWORD_08060dc0 = 0x00001cf4
  - DWORD_08060dc4 = 0x00001532
  - DWORD_08060dc8 = 0x0000161e
  - DWORD_08060dcc = 0x00001656
  - DWORD_08060dd0 = 0x00001685
  - DWORD_08060dd4 = 0x00001686
  - DWORD_08060e9c = 0x000016b8
  - DWORD_08060f9c = 0x00000868
  - DWORD_08060fa0 = 0x0201c510
  - DWORD_08060fd8 = 0x0201bb90
  - DAT_08061100 = 0x00000868
  - DAT_080611b4 = 0x00000868
  - DAT_080611b8 = 0x0201c510
  - DAT_080611bc = 0x000016cb
  - DAT_08061208 = 0x00001681
  - DAT_0806120c = 0x000016b3
  - DAT_08061210 = 0x000016b4
  - DWORD_08061294 = 0x0201c4e0
  - DWORD_08061298 = 0x00000868
  - DWORD_080612cc = 0x0201c4e0
  - DWORD_080612d0 = 0x00000868
  - DWORD_080612d4 = 0x000016cb
  - DWORD_080612d8 = 0x000016e4
  - DWORD_0806130c = 0x0201c4e0
  - DWORD_08061310 = 0x00000868
  - DWORD_080613b0 = 0x0201c4e0
- ROM_INCBIN / .byte 块: 3 blocks
  - 0x60a86 size 0x90  x1 (Block1)
  - 0x6106e size 0x2e  x1 (Block2)
  - 0x6121c size 0x28  x1 (Block3)

## 数据块分类 (Rule 2/3) -- 每块给 ref-scan 证据

| 块 | ref-scan (raw / THUMB+1) | 判定 | 理由 |
|---|---|---|---|
| 0x60a86 sz=0x90 | raw=0; THUMB+1: 1 hit at ROM file 0x1e417d0 (addr 0x09e417d0); in-block fn_elig=0x08060a89 | R4 disasm | THUMB+1 ptr 0x08060a89 found at dispatch table entry 0x09e417c0: [+0x04]=0x0000165b (CID=Contract with Exodia), [+0x10]=0x08060a89. fn_elig_addr=0x08060a88 in block. |
| 0x6106e sz=0x2e | raw=0; THUMB+1: 1 hit at ROM file 0x1e44668 (addr 0x09e44668); in-block fn_elig=0x08061071 | R4 disasm | THUMB+1 ptr 0x08061071 found at dispatch table entry 0x09e44658: [+0x04]=0x000016c6 (CID=Fenrir), [+0x10]=0x08061071. fn_elig_addr=0x08061070 in block. |
| 0x6121c sz=0x28 | raw=0; THUMB+1: 1 hit at ROM file 0x1e41bc0 (addr 0x09e41bc0); in-block fn_elig=0x0806121d | R4 disasm | THUMB+1 ptr 0x0806121d found at dispatch table entry 0x09e41bb0: [+0x04]=0x000016d1 (CID=Chaos End), [+0x10]=0x0806121d. fn_elig_addr=0x0806121c in block. |

Ref-scan python verification (all 3 blocks, entries at FS-area addr 0x09e4xxxx):
- Block1 entry 0x09e417c0: CID_rom=0x165b MATCH, fn_elig=0x08060a89 MATCH in_block=True
- Block2 entry 0x09e44658: CID_rom=0x16c6 MATCH, fn_elig=0x08061071 MATCH in_block=True
- Block3 entry 0x09e41bb0: CID_rom=0x16d1 MATCH, fn_elig=0x0806121d MATCH in_block=True

Dispatch table entry format (confirmed from ROM data):
- [+0x00] 0x00000000 (zero pad)
- [+0x04] CID (u32)
- [+0x08] fn_activate+1 (THUMB ptr)
- [+0x0C] fn_something+1 or 0
- [+0x10] fn_eligible+1 (THUMB ptr) -- searched value
- [+0x14] 0x00000000 (zero pad)
- Entry size = 0x18 bytes

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

All values verified via python struct.unpack_from('<I', rom, addr-0x08000000).

#### Reuse: gP1LifePoints = 0x0201c4e0 (ewram.inc, confirmed)
- DWORD_08060954 @ 0x08060954 -> .equ gp1lp_ptr_954, gP1LifePoints  [RENAME: use shared label]
- DWORD_08060a50 @ 0x08060a50 -> .equ gp1lp_ptr_a50, gP1LifePoints  [RENAME]
- DWORD_08060bf0 @ 0x08060bf0 -> .equ gp1lp_ptr_bf0, gP1LifePoints  [RENAME]
- DWORD_08060cf8 @ 0x08060cf8 -> .equ gp1lp_ptr_cf8, gP1LifePoints  [RENAME]
- DWORD_08060d40 @ 0x08060d40 -> .equ gp1lp_ptr_d40, gP1LifePoints  [RENAME]
- DWORD_08060db8 @ 0x08060db8 -> .equ gp1lp_ptr_db8, gP1LifePoints  [RENAME]
- DWORD_08061294 @ 0x08061294 -> .equ gp1lp_ptr_294, gP1LifePoints  [RENAME]
- DWORD_080612cc @ 0x080612cc -> .equ gp1lp_ptr_2cc, gP1LifePoints  [RENAME]
- DWORD_0806130c @ 0x0806130c -> .equ gp1lp_ptr_30c, gP1LifePoints  [RENAME]
- DWORD_080613b0 @ 0x080613b0 -> .equ gp1lp_ptr_3b0, gP1LifePoints  [RENAME]

NOTE: PTR_gP1LifePoints_080608d0, PTR_gP1LifePoints_08061064, PTR_gP1LifePoints_080610fc already named. Per scope convention, PTR_ slots are skipped (already resolved). All 3 confirm value = gP1LifePoints.

#### Reuse: PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc, confirmed)
- DAT_080608d4 @ 0x080608d4 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_8d4
- DWORD_08060bf4 @ 0x08060bf4 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_bf4
- DWORD_08060d44 @ 0x08060d44 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_d44
- DWORD_08060f9c @ 0x08060f9c -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_f9c
- DAT_08061100 @ 0x08061100 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_100
- DAT_080611b4 @ 0x080611b4 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_b4
- DWORD_08061298 @ 0x08061298 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_298
- DWORD_080612d0 @ 0x080612d0 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_2d0
- DWORD_08061310 @ 0x08061310 -> equate PLAYER_BLOCK_STRIDE; label: dat_player_stride_310

#### Reuse: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (ewram.inc, confirmed)
- DWORD_08060958 @ 0x08060958 = 0x00001ce8; label: dat_p1lp_off_1ce8_958
- DWORD_08060dbc @ 0x08060dbc = 0x00001ce8; label: dat_p1lp_off_1ce8_dbc

#### Reuse: FIELD_STATE_OFF = 0x1cf4 (duel_field.inc, confirmed)
- DWORD_08060dc0 @ 0x08060dc0 = 0x00001cf4; label: dat_field_state_off_dc0

#### Reuse: ZONE_DETAIL_FIELD_MASK_F88 = 0x00f88000 (duel_field.inc, confirmed)
- DWORD_08060cf4 @ 0x08060cf4 = 0x00f88000; label: dat_zone_field_mask_cf4

#### Reuse: gDuelFieldSlots = 0x0201c510 (ewram.inc, confirmed)
- DWORD_08060fa0 @ 0x08060fa0 = 0x0201c510; label: dat_duel_field_slots_fa0
- DAT_080611b8 @ 0x080611b8 = 0x0201c510; label: dat_duel_field_slots_b8

#### Reuse: gEquipChainSlotRefs = 0x0201bb90 (ewram.inc, confirmed)
- DWORD_08060fd8 @ 0x08060fd8 = 0x0201bb90; label: dat_equip_chain_slot_refs_fd8
  NOTE: Function plate check_equip_slot_eligible_by_zone_slot_field_correlation INCORRECTLY labels this "DUEL_STATE_PTR". Correct name is gEquipChainSlotRefs per ewram.inc L315. Plate ASCII rewrite must correct this error.

#### CID equates -- REUSE (all from constants/card_info.inc, C5 grep confirmed)
- DWORD_08060c20 @ 0x08060c20 = 0x0000167a; reuse FRIENDSHIP_CID (card_info.inc L1067); label: dat_friendship_cid_c20
- DWORD_08060c24 @ 0x08060c24 = 0x0000167b; reuse UNITY_CID (card_info.inc L1068); label: dat_unity_cid_c24
- DWORD_08060c6c @ 0x08060c6c = 0x0000129e; reuse DARK_MAGICIAN_GIRL_CID (card_info.inc L319); label: dat_dmg_cid_c6c
- DWORD_08060c88 @ 0x08060c88 = 0x00001532; reuse DON_ZALOOG_CID (card_info.inc L594); label: dat_don_zaloog_cid_c88
- DWORD_08060cf0 @ 0x08060cf0 = 0x00001332; reuse BANISHER_OF_THE_LIGHT_CID (card_info.inc L452); label: dat_banisher_cid_cf0
- DWORD_08060cfc @ 0x08060cfc = 0x00001691; reuse TERRORKING_ARCHFIEND_CID (card_info.inc L961); label: dat_terrorking_cid_cfc
- DWORD_08060dc4 @ 0x08060dc4 = 0x00001532; reuse DON_ZALOOG_CID; label: dat_don_zaloog_cid_dc4
- DWORD_08060dc8 @ 0x08060dc8 = 0x0000161e; reuse CLIFF_THE_TRAP_REMOVER_CID (card_info.inc L1076); label: dat_cliff_cid_dc8
- DWORD_08060dcc @ 0x08060dcc = 0x00001656; reuse DARK_SCORPION_CHICK_CID (card_info.inc L702); label: dat_ds_chick_cid_dcc
- DWORD_08060dd0 @ 0x08060dd0 = 0x00001685; reuse DARK_SCORPION_GORG_THE_STRONG_CID (card_info.inc L1026); label: dat_ds_gorg_cid_dd0
- DWORD_08060dd4 @ 0x08060dd4 = 0x00001686; reuse DARK_SCORPION_MEANAE_CID (card_info.inc L703); label: dat_ds_meanae_cid_dd4
- DWORD_08060e9c @ 0x08060e9c = 0x000016b8; reuse CRIMSON_NINJA_CID (card_info.inc L744); label: dat_crimson_ninja_cid_e9c
- DAT_080611bc @ 0x080611bc = 0x000016cb; reuse BLACK_LUSTER_SOLDIER_ENVOY_CID (card_info.inc L748); label: dat_bls_envoy_cid_bc
- DAT_08061208 @ 0x08061208 = 0x00001681; reuse OJAMA_GREEN_CID (card_info.inc L666); label: dat_ojama_green_cid_208
- DAT_08061210 @ 0x08061210 = 0x000016b4; reuse OJAMA_BLACK_CID (card_info.inc L668); label: dat_ojama_black_cid_210
- DWORD_080612d4 @ 0x080612d4 = 0x000016cb; reuse BLACK_LUSTER_SOLDIER_ENVOY_CID; label: dat_bls_envoy_cid_2d4

#### CID equates -- NEW (C5: grep card_info.inc 0 hits each)
- DWORD_08060c50 @ 0x08060c50 = 0x0000167e; NEW SAGES_STONE_CID (card_1355, pw=13604200); label: dat_sages_stone_cid_c50
- DWORD_08060c5c @ 0x08060c5c = 0x0000169e; reuse MUSTERING_DARK_SCORPIONS_CID (card_info.inc L704); label: dat_mustering_cid_c5c
  NOTE: 0x169e already has MUSTERING_DARK_SCORPIONS_CID so this is REUSE not NEW.
- DWORD_08060c64 @ 0x08060c64 = 0x0000157f; NEW QUEENS_KNIGHT_CID (card_1158, pw=25652259); label: dat_queens_knight_cid_c64
- DAT_0806120c @ 0x0806120c = 0x000016b3; NEW OJAMA_YELLOW_CID (card_1399, pw=42941100); label: dat_ojama_yellow_cid_20c
- DWORD_080612d8 @ 0x080612d8 = 0x000016e4; NEW CHAOS_EMPEROR_DRAGON_CID (card_1445, pw=82301904); label: dat_ced_cid_2d8

#### C5 double-check NEW CIDs (grep card_info.inc confirms 0 hits):
- 0x167e (SAGES_STONE_CID): "0x167e" -> 0 hits in card_info.inc [high confidence new]
- 0x157f (QUEENS_KNIGHT_CID): "0x157f" -> 0 hits in card_info.inc [high confidence new]
- 0x16b3 (OJAMA_YELLOW_CID): "0x16b3" -> 0 hits in card_info.inc [high confidence new]
- 0x16e4 (CHAOS_EMPEROR_DRAGON_CID): "0x16e4" -> 0 hits in card_info.inc [high confidence new]
- 0x169e (MUSTERING_DARK_SCORPIONS_CID): EXISTS in card_info.inc L704 -> REUSE

#### Block disasm literal pool slots (within ROM_INCBIN blocks, handled by R4 disasm)

Block1 literal pool (0x60af8..0x60b0c) -- 6 slots within block, will be named by disasm:
- 0x08060af8 = 0x00000fb7 -> NEW RIGHT_LEG_FORBIDDEN_ONE_CID (card_17, pw=08124921)
- 0x08060afc = 0x00000fb8 -> NEW LEFT_LEG_FORBIDDEN_ONE_CID (card_18, pw=44519536)
- 0x08060b00 = 0x00000fb9 -> NEW RIGHT_ARM_FORBIDDEN_ONE_CID (card_19, pw=70903634) -- NOTE: distinct slot_id 0x0fb9
- 0x08060b04 = 0x00000fba -> NEW LEFT_ARM_FORBIDDEN_ONE_CID (card_20, pw=07902349)
- 0x08060b08 = 0x00000fbb -> NEW EXODIA_THE_FORBIDDEN_ONE_CID (card_21, pw=33396948)
- 0x08060b0c = 0x00001645 -> reuse EXODIA_NECROSS_CID (card_info.inc, confirmed)

Block3 literal pool (0x6123c..0x61244) -- 2 slots within block, will be named by disasm:
- 0x0806123c = 0x0201c4e0 -> gP1LifePoints
- 0x08061240 = 0x00000868 -> PLAYER_BLOCK_STRIDE

### REF_SLOTS (USER-label + DATA-ref; RAM global)

No new global pointers to add beyond EQ treatment above. All 0x0201c4e0 slots treated as EQ to gP1LifePoints.

### RENAME_SLOTS (纯改名 + EOL)

All 47 DAT_/DWORD_ slots renamed using slot_label pattern. EOL text (ASCII only):

| slot | value | slot_label | eol_ascii |
|---|---|---|---|
| DAT_080608d4 | 0x868 | dat_player_stride_8d4 | PLAYER_BLOCK_STRIDE |
| DWORD_08060954 | gP1LifePoints | dat_gp1lp_ptr_954 | gP1LifePoints |
| DWORD_08060958 | 0x1ce8 | dat_p1lp_off_1ce8_958 | P1LP_BLOCK2_OFF_1CE8: owner block offset |
| DWORD_08060a50 | gP1LifePoints | dat_gp1lp_ptr_a50 | gP1LifePoints |
| DWORD_08060bf0 | gP1LifePoints | dat_gp1lp_ptr_bf0 | gP1LifePoints |
| DWORD_08060bf4 | 0x868 | dat_player_stride_bf4 | PLAYER_BLOCK_STRIDE |
| DWORD_08060c20 | 0x167a | dat_friendship_cid_c20 | FRIENDSHIP_CID |
| DWORD_08060c24 | 0x167b | dat_unity_cid_c24 | UNITY_CID |
| DWORD_08060c50 | 0x167e | dat_sages_stone_cid_c50 | SAGES_STONE_CID (new) |
| DWORD_08060c5c | 0x169e | dat_mustering_cid_c5c | MUSTERING_DARK_SCORPIONS_CID |
| DWORD_08060c64 | 0x157f | dat_queens_knight_cid_c64 | QUEENS_KNIGHT_CID (new) |
| DWORD_08060c6c | 0x129e | dat_dmg_cid_c6c | DARK_MAGICIAN_GIRL_CID |
| DWORD_08060c88 | 0x1532 | dat_don_zaloog_cid_c88 | DON_ZALOOG_CID |
| DWORD_08060cf0 | 0x1332 | dat_banisher_cid_cf0 | BANISHER_OF_THE_LIGHT_CID |
| DWORD_08060cf4 | 0xf88000 | dat_zone_field_mask_cf4 | ZONE_DETAIL_FIELD_MASK_F88 |
| DWORD_08060cf8 | gP1LifePoints | dat_gp1lp_ptr_cf8 | gP1LifePoints |
| DWORD_08060cfc | 0x1691 | dat_terrorking_cid_cfc | TERRORKING_ARCHFIEND_CID |
| DWORD_08060d40 | gP1LifePoints | dat_gp1lp_ptr_d40 | gP1LifePoints |
| DWORD_08060d44 | 0x868 | dat_player_stride_d44 | PLAYER_BLOCK_STRIDE |
| DWORD_08060db8 | gP1LifePoints | dat_gp1lp_ptr_db8 | gP1LifePoints |
| DWORD_08060dbc | 0x1ce8 | dat_p1lp_off_1ce8_dbc | P1LP_BLOCK2_OFF_1CE8 |
| DWORD_08060dc0 | 0x1cf4 | dat_field_state_off_dc0 | FIELD_STATE_OFF |
| DWORD_08060dc4 | 0x1532 | dat_don_zaloog_cid_dc4 | DON_ZALOOG_CID |
| DWORD_08060dc8 | 0x161e | dat_cliff_cid_dc8 | CLIFF_THE_TRAP_REMOVER_CID |
| DWORD_08060dcc | 0x1656 | dat_ds_chick_cid_dcc | DARK_SCORPION_CHICK_CID |
| DWORD_08060dd0 | 0x1685 | dat_ds_gorg_cid_dd0 | DARK_SCORPION_GORG_THE_STRONG_CID |
| DWORD_08060dd4 | 0x1686 | dat_ds_meanae_cid_dd4 | DARK_SCORPION_MEANAE_CID |
| DWORD_08060e9c | 0x16b8 | dat_crimson_ninja_cid_e9c | CRIMSON_NINJA_CID |
| DWORD_08060f9c | 0x868 | dat_player_stride_f9c | PLAYER_BLOCK_STRIDE |
| DWORD_08060fa0 | gDuelFieldSlots | dat_duel_field_slots_fa0 | gDuelFieldSlots |
| DWORD_08060fd8 | gEquipChainSlotRefs | dat_equip_chain_slot_refs_fd8 | gEquipChainSlotRefs (NOT DUEL_STATE_PTR -- plate correction) |
| DAT_08061100 | 0x868 | dat_player_stride_100 | PLAYER_BLOCK_STRIDE |
| DAT_080611b4 | 0x868 | dat_player_stride_b4 | PLAYER_BLOCK_STRIDE |
| DAT_080611b8 | gDuelFieldSlots | dat_duel_field_slots_b8 | gDuelFieldSlots |
| DAT_080611bc | 0x16cb | dat_bls_envoy_cid_bc | BLACK_LUSTER_SOLDIER_ENVOY_CID |
| DAT_08061208 | 0x1681 | dat_ojama_green_cid_208 | OJAMA_GREEN_CID |
| DAT_0806120c | 0x16b3 | dat_ojama_yellow_cid_20c | OJAMA_YELLOW_CID (new) |
| DAT_08061210 | 0x16b4 | dat_ojama_black_cid_210 | OJAMA_BLACK_CID |
| DWORD_08061294 | gP1LifePoints | dat_gp1lp_ptr_294 | gP1LifePoints |
| DWORD_08061298 | 0x868 | dat_player_stride_298 | PLAYER_BLOCK_STRIDE |
| DWORD_080612cc | gP1LifePoints | dat_gp1lp_ptr_2cc | gP1LifePoints |
| DWORD_080612d0 | 0x868 | dat_player_stride_2d0 | PLAYER_BLOCK_STRIDE |
| DWORD_080612d4 | 0x16cb | dat_bls_envoy_cid_2d4 | BLACK_LUSTER_SOLDIER_ENVOY_CID |
| DWORD_080612d8 | 0x16e4 | dat_ced_cid_2d8 | CHAOS_EMPEROR_DRAGON_CID (new) |
| DWORD_0806130c | gP1LifePoints | dat_gp1lp_ptr_30c | gP1LifePoints |
| DWORD_08061310 | 0x868 | dat_player_stride_310 | PLAYER_BLOCK_STRIDE |
| DWORD_080613b0 | gP1LifePoints | dat_gp1lp_ptr_3b0 | gP1LifePoints |

Total RENAME slots: 47

### FUNC_RENAME (误名订正, 如有)

None. All 34 named functions have semantics consistent with their names.
`check_equip_slot_eligible_by_effect_sum_vs_tier__08060974` has a double-underscore address suffix indicating a naming collision with the sibling at 0x080608e0; the current name is acceptable as-is. No rename needed.

Note on `check_equip_slot_eligible_by_zone_slot_field_correlation` plate: plate text says "DUEL_STATE_PTR = 0x0201bb90" but ewram.inc line 315 defines this address as gEquipChainSlotRefs. This is a semantic error in the plate comment, NOT a function misnaming (function logic reads [+0x4]=player, [+0x20]=zone_idx, [+0xd8]=slot_word -- these are fields of the equip chain slot ref struct, consistent with gEquipChainSlotRefs). Correct in plate rewrite.

### PLATE (R5; full ASCII rewrite of 6 CJK-mojibake functions)

All 6 plates need full ASCII rewrite (CJK present in file = Jython double-encode mojibake; substring replace is silent no-op on mojibake; must full-rewrite).

1. **check_equip_slot_eligible_by_effect_sum_vs_tier__08060974** @ 0x08060974  [L11728-L11732]
   Current: CJK mojibake  
   New (ASCII):
   ```
   Equip slot eligibility predicate. First calls sum_equip_slot_effect_values_for_player(player_id)
   -> r4 (effect sum). Then calls classify_equip_card_id_tier_abcx(slot_ptr) -> r0 (tier).
   If effect_sum < tier: return 0 (effect not yet at tier). Else: call
   dispatch_effect_for_neo_daedalus_eligible_slot(slot_ptr, arg) and return its result.
   Semantics: when cumulative equip effect sum reaches the tier threshold, fires Neo Daedalus
   effect dispatch. Sibling of check_equip_slot_eligible_by_effect_sum_vs_tier (0x080608e0).
   Constants: tier computed dynamically by classify_equip_card_id_tier_abcx (no static constant).
   Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to neo_daedalus dispatch)
   Returns: r0=u32 (0 if effect_sum < tier; else forwarded from neo_daedalus dispatch)
   Callees: sum_equip_slot_effect_values_for_player, classify_equip_card_id_tier_abcx,
            dispatch_effect_for_neo_daedalus_eligible_slot
   ```

2. **check_equip_slot_eligible_chain_present_with_neo_daedalus** @ 0x08060a5c  [L11894-L11897]
   Current: CJK mojibake  
   New (ASCII):
   ```
   Equip slot eligibility predicate, returns 0/1. Calls check_value_in_slot_chain(player_id,
   card_id, type=0xb); if target value absent returns 0. On match calls
   check_neo_daedalus_placement_eligible(slot_ptr, arg) and forwards result.
   Semantics: equip chain must contain the target card before Neo Daedalus placement check.
   Sibling of check_equip_slot_eligible_with_chain_absent_and_lp_slot (symmetric branch).
   Constants: CHAIN_TYPE = 0xb (equip node chain search type)
   Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to neo_daedalus check)
   Returns: r0=u32 (0 if chain absent; else forwarded from neo_daedalus check)
   Callees: check_value_in_slot_chain, check_neo_daedalus_placement_eligible
   ```

3. **check_equip_slot_eligible_by_companion_card_and_paired_slot** @ 0x08060c30  [L12142]
   Current: CJK mojibake  
   New (ASCII):
   ```
   Equip slot eligibility predicate, returns 0/1. Pre-cond: check_neo_daedalus_placement_eligible;
   on fail returns 0. Reads slot ldrh[+0] card_id, selects companion card via dispatch table:
   card_id == SAGES_STONE_CID (0x167e) -> companion = DARK_MAGICIAN_GIRL_CID (0x129e);
   card_id == SAGES_STONE_CID-0xc8 (0x15b6) -> companion = QUEENS_KNIGHT_CID (0x157f);
   card_id == MUSTERING_DARK_SCORPIONS_CID (0x169e) -> companion = DON_ZALOOG_CID (0x1532).
   Calls count_paired_slots_with_field5_default(player_id, companion_cid); returns 1 if nonzero.
   Constants: SAGES_STONE_CID=0x167e, MUSTERING_DARK_SCORPIONS_CID=0x169e,
              DARK_MAGICIAN_GIRL_CID=0x129e, QUEENS_KNIGHT_CID=0x157f, DON_ZALOOG_CID=0x1532
   Inputs: r0=SlotPtr* slot_ptr (ldrh[+0]=card_id, byte[+2] bit0=player_id)
   Returns: r0=u32 (1 if neo_daedalus ok and companion paired with field5, 0 otherwise)
   Callees: check_neo_daedalus_placement_eligible, count_paired_slots_with_field5_default
   ```

4. **check_equip_slot_eligible_by_field6_guard_and_chain_absent** @ 0x08060e24  [L12512-L12517]
   Current: CJK mojibake  
   New (ASCII):
   ```
   Equip slot eligibility predicate, returns 0/1. Extracts field6 from slot ldrh[+4] bits[13:6]
   (lsls #0x11; lsrs #0x17). Calls dispatch_equip_slot_scan_with_field6_guard(player_id, field6,
   arg3=1, sp[0]=0); if returns 0 returns 0. On pass calls check_equip_slot_chain_absent(slot_ptr,
   arg) and returns result. Semantics: field6 scan gate before equip chain absent check.
   Constants: FIELD6_SHIFT=lsls #0x11/lsrs #0x17 (net=6-bit field); SCAN_ARG3=1; SCAN_ARG4=0
   Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to chain_absent)
   Returns: r0=u32 (0 if scan fails; else forwarded from chain_absent)
   Callees: dispatch_equip_slot_scan_with_field6_guard, check_equip_slot_chain_absent
   ```

5. **check_equip_slot_eligible_chain_absent_with_spell_zone_and_display** @ 0x08060fe8  [L12824]
   Current: CJK mojibake  
   New (ASCII):
   ```
   Equip slot eligibility predicate, returns 0 or dispatch result. Three-level check:
   (1) check_equip_slot_chain_absent(slot_ptr) -- if 0 return 0;
   (2) check_spell_zone_slot_placeable(player_id) -- if 0 return 0;
   (3) dispatch_effect_by_card_id_with_display_lookup(slot_ptr, arg) -- return its value.
   Differs from check_equip_slot_eligible_with_chain_absent_and_spell_dispatch (0x08060ea8):
   uses dispatch_effect_by_card_id_with_display_lookup instead of dispatch_effect_handler_by_card_id.
   Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to display lookup)
   Returns: r0=u32 (0 if either guard fails; else forwarded from display dispatch)
   Callees: check_equip_slot_chain_absent, check_spell_zone_slot_placeable,
            dispatch_effect_by_card_id_with_display_lookup
   ```

6. **check_equip_slot_eligible_neo_daedalus_with_hand_empty** @ 0x080612e4  [L13282-L13293]
   Current: CJK mojibake  
   New (ASCII):
   ```
   Neo Daedalus equip slot eligibility predicate. Guard: when hand alt count field
   gP1LifePoints[player*0x868+0x14] != 0, returns 0 (hand not empty). When count == 0,
   calls dispatch_effect_for_neo_daedalus_eligible_slot(slot_ptr, aux) and returns its bool
   result (1=eligible, 0=rejected). Condition: equip hand count must be zero before dispatching
   Neo Daedalus effect eligibility logic.
   Constants: gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868,
              HAND_COUNT_OFFSET=0x14 (zone occupy count field; count==0 required),
              player_id from slot[+2] bit0
   Inputs: r0=SlotPtr* slot_ptr, r1=u32 aux_arg (forwarded to neo_daedalus dispatch)
   Returns: r0=u32 (0 if hand count != 0; else forwarded from neo_daedalus dispatch)
   Callees: dispatch_effect_for_neo_daedalus_eligible_slot
   ```

## disasm 计划 (R4, 如有)

### Block1: ROM_INCBIN 0x60a86, 0x90  -> R4 disasm
- CID: 0x165b (Contract with Exodia), dispatch entry @ 0x09e417c0
- fn_eligible entry: 0x08060a89 (THUMB ptr), fn target: 0x08060a88
- Function name: `check_exodia_set_in_extra_for_cid_165b`
- Semantics (from literal pool analysis): verifies 5 Exodia pieces in extra deck.
  Literal pool @ 0x60af8: 0x0fb7=RIGHT_LEG, 0x0fb8=LEFT_LEG, 0x0fb9=RIGHT_ARM,
  0x0fba=LEFT_ARM, 0x0fbb=EXODIA_THE_FORBIDDEN_ONE; then 0x1645=EXODIA_NECROSS_CID.
  Calls count_extra_deck_cards_by_id x5 for the 5 forbidden one pieces, plus
  check_neo_daedalus_placement_eligible and count_valid_monster_pair_slots.
- Plate: "reached via card effect handler dispatch table 0x09e417c0, Contract with Exodia CID 0x165b"
- New equates needed in new inc: RIGHT_LEG_FORBIDDEN_ONE_CID=0x0fb7, LEFT_LEG_FORBIDDEN_ONE_CID=0x0fb8,
  RIGHT_ARM_FORBIDDEN_ONE_CID=0x0fb9, LEFT_ARM_FORBIDDEN_ONE_CID=0x0fba,
  EXODIA_THE_FORBIDDEN_ONE_CID=0x0fbb; CONTRACT_WITH_EXODIA_CID=0x165b (for dispatch table comment)
- Disasm procedure: clearListing 0x60a86..0x60b16 -> setTMode -> DisassembleCommand(0x08060a88)
  (single sub-fn entry; literal pool follows at 0x60af8 -> createDWord each)

### Block2: ROM_INCBIN 0x6106e, 0x2e  -> R4 disasm
- CID: 0x16c6 (Fenrir), dispatch entry @ 0x09e44658
- fn_eligible entry: 0x08061071 (THUMB ptr), fn target: 0x08061070
- Function name: `check_zone_type580_direction_mismatch_for_cid_16c6`
- Semantics (from ROM bytes @ 0x6106e): 0x6106e-6106f = 0x0000 (2B padding). fn starts at 0x61070 with `adds r2,r0,#0` (0x1c02), leaf fn (no push/pop, exits via bx lr).
  Checks zone_type == 0x580 (0xb0<<3) from halfword[+2] AND detail_word bit9 != player_id.
  Returns 1 if both conditions pass.
- Plate: "reached via card effect handler dispatch table 0x09e44658, Fenrir CID 0x16c6"
- New equate: FENRIR_CID=0x16c6 (for comment)
- Disasm procedure: clearListing 0x6106e..0x6109c -> setTMode -> DisassembleCommand(0x08061070)

### Block3: ROM_INCBIN 0x6121c, 0x28  -> R4 disasm
- CID: 0x16d1 (Chaos End), dispatch entry @ 0x09e41bb0
- fn_eligible entry: 0x0806121d (THUMB ptr), fn target: 0x0806121c
- Function name: `check_lp_zone_hand_above6_for_cid_16d1`
- Semantics (from ROM bytes @ 0x6121c): THUMB code starts `movs r3,#0` (0x4a07 = ldr r2,[pc,#0x1c]).
  Reads gP1LifePoints[player*0x868+0x1c]; returns 1 if > 6.
  Literal pool @ 0x6123c: 0x0201c4e0=gP1LifePoints, 0x61240: 0x00000868=PLAYER_BLOCK_STRIDE.
- Plate: "reached via card effect handler dispatch table 0x09e41bb0, Chaos End CID 0x16d1"
- New equate: CHAOS_END_CID=0x16d1 (for comment)
- Disasm procedure: clearListing 0x6121c..0x61244 -> setTMode -> DisassembleCommand(0x0806121c)

## carve 计划 (R7, 如有)

None. All 3 ROM_INCBIN blocks are THUMB code (R4 disasm), not data tables. No carve needed.

## 新增 constants / 全局 (如有; 必须先证明现有 inc 无可复用)

新建 equate block (建议追加到 constants/card_info.inc):

```asm
@ Seg-6 new CIDs (verified 0 hits in card_info.inc before adding)
.equ QUEENS_KNIGHT_CID,             0x0000157f  @ Queen's Knight (pw=25652259); Seg-6 companion card
.equ CONTRACT_WITH_EXODIA_CID,      0x0000165b  @ Contract with Exodia (pw=33244944); dispatch handler fn 0x08060a88
.equ SAGES_STONE_CID,               0x0000167e  @ Sage's Stone (pw=13604200); companion dispatch table
.equ OJAMA_YELLOW_CID,              0x000016b3  @ Ojama Yellow (pw=42941100); Ojama trio check
.equ FENRIR_CID,                    0x000016c6  @ Fenrir (pw=00218704); dispatch handler fn 0x08061070
.equ CHAOS_END_CID,                 0x000016d1  @ Chaos End (pw=61044390); dispatch handler fn 0x0806121c

@ Exodia piece CIDs -- Block1 literal pool slots (all new; 0 hits in card_info.inc)
.equ RIGHT_LEG_FORBIDDEN_ONE_CID,   0x00000fb7  @ Right Leg of the Forbidden One (pw=08124921)
.equ LEFT_LEG_FORBIDDEN_ONE_CID,    0x00000fb8  @ Left Leg of the Forbidden One (pw=44519536)
.equ RIGHT_ARM_FORBIDDEN_ONE_CID,   0x00000fb9  @ Right Arm of the Forbidden One (pw=70903634)
.equ LEFT_ARM_FORBIDDEN_ONE_CID,    0x00000fba  @ Left Arm of the Forbidden One (pw=07902349)
.equ EXODIA_THE_FORBIDDEN_ONE_CID,  0x00000fbb  @ Exodia the Forbidden One (pw=33396948)

@ Chaos Emperor Dragon Envoy -- new (0x16e4; 0 hits in card_info.inc)
.equ CHAOS_EMPEROR_DRAGON_CID,      0x000016e4  @ Chaos Emperor Dragon - Envoy of the End (pw=82301904)
```

Total new equates: 12

Offsets LP_ZONE_ARRAY_OFF (0x10e0 = 0x87<<5) and ZONE_STRUCT_SIZE (0x14 = 20) appear in multiple functions but are NOT defined in any existing constants/*.inc (confirmed 0 hits). These are inline computed values (0x87 lsls #5 + index*4) and not parameterized via equate in prior segments. Low semantic value as standalone equates since they are always computed inline. Propose NOT adding standalone equates; instead, note in EOL as "LP zone array base = gP1LifePoints + 0x10e0 (0x87<<5)" in plate text.

## §5.1 登记 (Rule 3) -- 0 引用块

None. All 3 ROM_INCBIN blocks have confirmed dispatch table THUMB+1 references. No §5.1 entries.

## 消费者证据 (R6) -- 关键槽语义的 file:line + 置信度

| 槽 | 语义证据 | file:line | 置信度 |
|---|---|---|---|
| DWORD_08060fd8=0x0201bb90 | ewram.inc line 315: `.equ gEquipChainSlotRefs, 0x0201bb90`; plate error "DUEL_STATE_PTR" contradicted by ewram.inc | constants/ewram.inc:315 | high |
| DWORD_08060cf4=0x00f88000 | duel_field.inc: `.equ ZONE_DETAIL_FIELD_MASK_F88, 0x00f88000` | constants/duel_field.inc:378 | high |
| DWORD_08060dc0=0x1cf4 | duel_field.inc: `.equ FIELD_STATE_OFF, 0x00001cf4` | constants/duel_field.inc:205 | high |
| Block1 0x08060a88 fn | count_extra_deck_cards_by_id x5 for 0x0fb7/8/9/a/b; literal pool @ 0x60af8 python-verified | asm/07_equip_effect_chain.s:ROM bytes | high |
| Block2 0x08061070 fn | ROM bytes: zone_type 0x580 check + bit9 direction mismatch; plate `check_zone_type580_direction_mismatch_for_cid_16c6` | asm/07 ROM 0x6106e analysis | high |
| Block3 0x0806121c fn | ROM bytes: ldr r2,[pc+0x1c]->gP1LifePoints, *0x868+0x1c, cmp >6 | asm/07 ROM 0x6121c analysis | high |
| DON_ZALOOG_CID=0x1532 x2 | card_info.inc L594: DON_ZALOOG_CID; dark_scorpion plate confirms | constants/card_info.inc:594 | high |
| BLACK_LUSTER_SOLDIER_ENVOY_CID=0x16cb x2 | card_info.inc L748: confirmed; used in BLS envoy zone check | constants/card_info.inc:748 | high |
| CHAOS_EMPEROR_DRAGON_CID=0x16e4 | card_1445 header: "Chaos Emperor Dragon - Envoy of the End slot=0x16E4"; plate at 0x0806129c names it explicitly | data/card-stats.s:card_1445 | high |

## 求助 (如有低置信度语义)

None. All slots resolved with high or medium confidence.

Pending verification for fixer: confirm `check_exodia_set_in_extra_for_cid_165b` body logic -- the function name is inferred from literal pool CIDs (5 Exodia pieces + Exodia Necross) but exact call sequence (count_extra_deck_cards_by_id x5 then neo_daedalus + pair checks) cannot be verified without disasm. Fixer should confirm function structure after R4 disasm and adjust plate accordingly.

---

## Executor Report: F07-Seg-6
- 槽: EQ=47 (all 47 DWORD_/DAT_ slots, PTR_ slots skipped per scope convention) REF=0 RENAME=0 (EQ and RENAME are the same 47 slots; no separate RENAME-only slots) FUNC_RENAME=0 PLATE=6
- disasm=3 (Block1 0x60a86/0x90 fn@0x08060a88, Block2 0x6106e/0x2e fn@0x08061070, Block3 0x6121c/0x28 fn@0x0806121c)
- carve=0 §5.1=0
- 新增 constants/全局: 12 new CID equates (QUEENS_KNIGHT_CID, CONTRACT_WITH_EXODIA_CID, SAGES_STONE_CID, OJAMA_YELLOW_CID, FENRIR_CID, CHAOS_END_CID, CHAOS_EMPEROR_DRAGON_CID, RIGHT_LEG/LEFT_LEG/RIGHT_ARM/LEFT_ARM/EXODIA_THE_FORBIDDEN_ONE_CID); all in card_info.inc
- 求助: none
- proposal: doc/dev/refine/F07-Seg-6.proposal.md
