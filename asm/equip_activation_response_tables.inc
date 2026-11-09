@ Yu-Gi-Oh! Ultimate Masters: WCT 2006
@ Equip activation response tables (file 15 Seg-2).
@ Callback words store THUMB entry addresses (function + 1).

@ Future callback entry aliases; code ownership remains with later segments.

equip_ai_phase_response_table:
equip_ai_phase_response_table:
	.word 0x00001407                                                           @ 09e481e8 07140000
equip_ai_phase_response_table_row_000_callback:
	.word check_zone_score_advantage_for_self+1                                @ 09e481ec dd770b08
equip_ai_phase_response_table_row_001_cid:
	.word 0x00001246                                                           @ 09e481f0 46120000
equip_ai_phase_response_table_row_001_callback:
	.word check_opponent_equip_count_exceeds_one+1                             @ 09e481f4 39780b08
equip_ai_phase_response_table_row_002_cid:
	.word 0x0000131b                                                           @ 09e481f8 1b130000
equip_ai_phase_response_table_row_002_callback:
	.word check_equip_activation_valid_under_level_restriction+1               @ 09e481fc 35790b08
equip_ai_phase_response_table_row_003_cid:
	.word 0x000012eb                                                           @ 09e48200 eb120000
equip_ai_phase_response_table_row_003_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48204 a9760b08
equip_ai_phase_response_table_row_004_cid:
	.word 0x000012e6                                                           @ 09e48208 e6120000
equip_ai_phase_response_table_row_004_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e4820c a9760b08
equip_ai_phase_response_table_row_005_cid:
	.word 0x0000149b                                                           @ 09e48210 9b140000
equip_ai_phase_response_table_row_005_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48214 a9760b08
equip_ai_phase_response_table_row_006_cid:
	.word 0x0000132d                                                           @ 09e48218 2d130000
equip_ai_phase_response_table_row_006_callback:
	.word check_opponent_equip_whitelist_cards_present+1                       @ 09e4821c 59780b08
equip_ai_phase_response_table_row_007_cid:
	.word 0x0000137c                                                           @ 09e48220 7c130000
equip_ai_phase_response_table_row_007_callback:
	.word check_opponent_equip_whitelist_cards_present+1                       @ 09e48224 59780b08
equip_ai_phase_response_table_row_008_cid:
	.word 0x0000132e                                                           @ 09e48228 2e130000
equip_ai_phase_response_table_row_008_callback:
	.word check_premature_burial_or_coth_equip_eligible+1                      @ 09e4822c 79780b08
equip_ai_phase_response_table_row_009_cid:
	.word 0x00001363                                                           @ 09e48230 63130000
equip_ai_phase_response_table_row_009_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48234 a9760b08
equip_ai_phase_response_table_row_010_cid:
	.word 0x00001364                                                           @ 09e48238 64130000
equip_ai_phase_response_table_row_010_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e4823c a9760b08
equip_ai_phase_response_table_row_011_cid:
	.word 0x000010f8                                                           @ 09e48240 f8100000
equip_ai_phase_response_table_row_011_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48244 7d770b08
equip_ai_phase_response_table_row_012_cid:
	.word 0x000010f9                                                           @ 09e48248 f9100000
equip_ai_phase_response_table_row_012_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4824c 7d770b08
equip_ai_phase_response_table_row_013_cid:
	.word 0x000010fa                                                           @ 09e48250 fa100000
equip_ai_phase_response_table_row_013_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48254 7d770b08
equip_ai_phase_response_table_row_014_cid:
	.word 0x000010fb                                                           @ 09e48258 fb100000
equip_ai_phase_response_table_row_014_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4825c 7d770b08
equip_ai_phase_response_table_row_015_cid:
	.word 0x000010fc                                                           @ 09e48260 fc100000
equip_ai_phase_response_table_row_015_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48264 7d770b08
equip_ai_phase_response_table_row_016_cid:
	.word 0x000012e8                                                           @ 09e48268 e8120000
equip_ai_phase_response_table_row_016_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4826c 7d770b08
equip_ai_phase_response_table_row_017_cid:
	.word 0x00001761                                                           @ 09e48270 61170000
equip_ai_phase_response_table_row_017_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48274 7d770b08
equip_ai_phase_response_table_row_018_cid:
	.word 0x0000141f                                                           @ 09e48278 1f140000
equip_ai_phase_response_table_row_018_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4827c 7d770b08
equip_ai_phase_response_table_row_019_cid:
	.word 0x000015e7                                                           @ 09e48280 e7150000
equip_ai_phase_response_table_row_019_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48284 7d770b08
equip_ai_phase_response_table_row_020_cid:
	.word 0x0000159b                                                           @ 09e48288 9b150000
equip_ai_phase_response_table_row_020_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4828c e5760b08
equip_ai_phase_response_table_row_021_cid:
	.word 0x00001460                                                           @ 09e48290 60140000
equip_ai_phase_response_table_row_021_callback:
	.word return_true_response_callback+1                                      @ 09e48294 a5760b08
equip_ai_phase_response_table_row_022_cid:
	.word 0x00001101                                                           @ 09e48298 01110000
equip_ai_phase_response_table_row_022_callback:
	.word check_opponent_lp_below_self_plus_500+1                              @ 09e4829c f9770b08
equip_ai_phase_response_table_row_023_cid:
	.word 0x00001100                                                           @ 09e482a0 00110000
equip_ai_phase_response_table_row_023_callback:
	.word check_dark_room_activation_slots_available+1                         @ 09e482a4 8d770b08
equip_ai_phase_response_table_row_024_cid:
	.word 0x000010ff                                                           @ 09e482a8 ff100000
equip_ai_phase_response_table_row_024_callback:
	.word check_dark_room_activation_slots_available+1                         @ 09e482ac 8d770b08
equip_ai_phase_response_table_row_025_cid:
	.word 0x000010fd                                                           @ 09e482b0 fd100000
equip_ai_phase_response_table_row_025_callback:
	.word check_dark_room_activation_slots_available+1                         @ 09e482b4 8d770b08
equip_ai_phase_response_table_row_026_cid:
	.word 0x000010fe                                                           @ 09e482b8 fe100000
equip_ai_phase_response_table_row_026_callback:
	.word check_dark_room_activation_slots_available+1                         @ 09e482bc 8d770b08
equip_ai_phase_response_table_row_027_cid:
	.word 0x000012e9                                                           @ 09e482c0 e9120000
equip_ai_phase_response_table_row_027_callback:
	.word check_dark_room_activation_slots_available+1                         @ 09e482c4 8d770b08
equip_ai_phase_response_table_row_028_cid:
	.word 0x00001460                                                           @ 09e482c8 60140000
equip_ai_phase_response_table_row_028_callback:
	.word check_dark_room_activation_slots_available+1                         @ 09e482cc 8d770b08
equip_ai_phase_response_table_row_029_cid:
	.word 0x00001324                                                           @ 09e482d0 24130000
equip_ai_phase_response_table_row_029_callback:
	.word return_true_response_callback+1                                      @ 09e482d4 a5760b08
equip_ai_phase_response_table_row_030_cid:
	.word 0x00001325                                                           @ 09e482d8 25130000
equip_ai_phase_response_table_row_030_callback:
	.word return_true_response_callback+1                                      @ 09e482dc a5760b08
equip_ai_phase_response_table_row_031_cid:
	.word 0x0000132b                                                           @ 09e482e0 2b130000
equip_ai_phase_response_table_row_031_callback:
	.word return_true_response_callback+1                                      @ 09e482e4 a5760b08
equip_ai_phase_response_table_row_032_cid:
	.word 0x000012c8                                                           @ 09e482e8 c8120000
equip_ai_phase_response_table_row_032_callback:
	.word return_true_response_callback+1                                      @ 09e482ec a5760b08
equip_ai_phase_response_table_row_033_cid:
	.word 0x0000159a                                                           @ 09e482f0 9a150000
equip_ai_phase_response_table_row_033_callback:
	.word return_true_response_callback+1                                      @ 09e482f4 a5760b08
equip_ai_phase_response_table_row_034_cid:
	.word 0x000017a7                                                           @ 09e482f8 a7170000
equip_ai_phase_response_table_row_034_callback:
	.word return_true_response_callback+1                                      @ 09e482fc a5760b08
equip_ai_phase_response_table_row_035_cid:
	.word 0x000017dd                                                           @ 09e48300 dd170000
equip_ai_phase_response_table_row_035_callback:
	.word return_true_response_callback+1                                      @ 09e48304 a5760b08
equip_ai_phase_response_table_row_036_cid:
	.word 0x0000114f                                                           @ 09e48308 4f110000
equip_ai_phase_response_table_row_036_callback:
	.word check_thunder_dragon_zone_pair_response_eligible+1                            @ 09e4830c 09a70b08
equip_ai_phase_response_table_row_037_cid:
	.word 0x0000179c                                                           @ 09e48310 9c170000
equip_ai_phase_response_table_row_037_callback:
	.word check_king_of_swamp_fusion_response_eligible+1                            @ 09e48314 1da70b08
equip_ai_phase_response_table_row_038_cid:
	.word 0x0000132f                                                           @ 09e48318 2f130000
equip_ai_phase_response_table_row_038_callback:
	.word return_true_response_callback+1                                      @ 09e4831c a5760b08
equip_ai_phase_response_table_row_039_cid:
	.word 0x000012f9                                                           @ 09e48320 f9120000
equip_ai_phase_response_table_row_039_callback:
	.word check_soul_release_response_eligible+1                            @ 09e48324 d97c0b08
equip_ai_phase_response_table_row_040_cid:
	.word 0x00001389                                                           @ 09e48328 89130000
equip_ai_phase_response_table_row_040_callback:
	.word check_windstorm_score_pair_straddles_player_max+1                            @ 09e4832c 6d7d0b08
equip_ai_phase_response_table_row_041_cid:
	.word 0x000015c7                                                           @ 09e48330 c7150000
equip_ai_phase_response_table_row_041_callback:
	.word check_hand_equip_target_bonus_above_four_eligible+1                              @ 09e48334 c5880b08
equip_ai_phase_response_table_row_042_cid:
	.word 0x000012be                                                           @ 09e48338 be120000
equip_ai_phase_response_table_row_042_callback:
	.word check_toon_world_player_list_has_field8_6+1                            @ 09e4833c 2d7e0b08
equip_ai_phase_response_table_row_043_cid:
	.word 0x000015a1                                                           @ 09e48340 a1150000
equip_ai_phase_response_table_row_043_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48344 1d770b08
equip_ai_phase_response_table_row_044_cid:
	.word 0x00001534                                                           @ 09e48348 34150000
equip_ai_phase_response_table_row_044_callback:
	.word check_effect_handler_result_positive+1                               @ 09e4834c 1d770b08
equip_ai_phase_response_table_row_045_cid:
	.word 0x00001238                                                           @ 09e48350 38120000
equip_ai_phase_response_table_row_045_callback:
	.word check_metalmorph_effect_zone_response_eligible+1                            @ 09e48354 a5950b08
equip_ai_phase_response_table_row_046_cid:
	.word 0x000015a2                                                           @ 09e48358 a2150000
equip_ai_phase_response_table_row_046_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4835c e5760b08
equip_ai_phase_response_table_row_047_cid:
	.word 0x000015ec                                                           @ 09e48360 ec150000
equip_ai_phase_response_table_row_047_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e48364 e5760b08
equip_ai_phase_response_table_row_048_cid:
	.word 0x0000187b                                                           @ 09e48368 7b180000
equip_ai_phase_response_table_row_048_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4836c e5760b08
equip_ai_phase_response_table_row_049_cid:
	.word 0x0000150f                                                           @ 09e48370 0f150000
equip_ai_phase_response_table_row_049_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e48374 e5760b08
equip_ai_phase_response_table_row_050_cid:
	.word 0x00001403                                                           @ 09e48378 03140000
equip_ai_phase_response_table_row_050_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4837c e5760b08
equip_ai_phase_response_table_row_051_cid:
	.word 0x0000146f                                                           @ 09e48380 6f140000
equip_ai_phase_response_table_row_051_callback:
	.word check_cathedral_of_nobles_response_eligible+1                            @ 09e48384 99830b08
equip_ai_phase_response_table_row_052_cid:
	.word 0x000014cf                                                           @ 09e48388 cf140000
equip_ai_phase_response_table_row_052_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4838c e5760b08
equip_ai_phase_response_table_row_053_cid:
	.word 0x000015fe                                                           @ 09e48390 fe150000
equip_ai_phase_response_table_row_053_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e48394 e5760b08
equip_ai_phase_response_table_row_054_cid:
	.word 0x000017a3                                                           @ 09e48398 a3170000
equip_ai_phase_response_table_row_054_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4839c e5760b08
equip_ai_phase_response_table_row_055_cid:
	.word 0x000016da                                                           @ 09e483a0 da160000
equip_ai_phase_response_table_row_055_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e483a4 e5760b08
equip_ai_phase_response_table_row_056_cid:
	.word 0x000019da                                                           @ 09e483a8 da190000
equip_ai_phase_response_table_row_056_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e483ac e5760b08
equip_activation_response_table:
equip_activation_response_table:
	.word 0x000012cc                                                           @ 09e483b0 cc120000
equip_activation_response_table_row_000_callback:
	.word return_true_response_callback+1                                      @ 09e483b4 a5760b08
equip_activation_response_table_row_001_cid:
	.word 0x00001308                                                           @ 09e483b8 08130000
equip_activation_response_table_row_001_callback:
	.word return_true_response_callback+1                                      @ 09e483bc a5760b08
equip_activation_response_table_row_002_cid:
	.word 0x00001739                                                           @ 09e483c0 39170000
equip_activation_response_table_row_002_callback:
	.word return_true_response_callback+1                                      @ 09e483c4 a5760b08
equip_activation_response_table_row_003_cid:
	.word 0x00001548                                                           @ 09e483c8 48150000
equip_activation_response_table_row_003_callback:
	.word return_true_response_callback+1                                      @ 09e483cc a5760b08
equip_activation_response_table_row_004_cid:
	.word 0x00001104                                                           @ 09e483d0 04110000
equip_activation_response_table_row_004_callback:
	.word return_true_response_callback+1                                      @ 09e483d4 a5760b08
equip_activation_response_table_row_005_cid:
	.word 0x00001233                                                           @ 09e483d8 33120000
equip_activation_response_table_row_005_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e483dc 61770b08
equip_activation_response_table_row_006_cid:
	.word 0x00001236                                                           @ 09e483e0 36120000
equip_activation_response_table_row_006_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e483e4 61770b08
equip_activation_response_table_row_007_cid:
	.word 0x0000123a                                                           @ 09e483e8 3a120000
equip_activation_response_table_row_007_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e483ec 61770b08
equip_activation_response_table_row_008_cid:
	.word 0x0000123c                                                           @ 09e483f0 3c120000
equip_activation_response_table_row_008_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e483f4 61770b08
equip_activation_response_table_row_009_cid:
	.word 0x0000123d                                                           @ 09e483f8 3d120000
equip_activation_response_table_row_009_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e483fc 61770b08
equip_activation_response_table_row_010_cid:
	.word 0x0000123e                                                           @ 09e48400 3e120000
equip_activation_response_table_row_010_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e48404 61770b08
equip_activation_response_table_row_011_cid:
	.word 0x00001304                                                           @ 09e48408 04130000
equip_activation_response_table_row_011_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e4840c 61770b08
equip_activation_response_table_row_012_cid:
	.word 0x00001305                                                           @ 09e48410 05130000
equip_activation_response_table_row_012_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e48414 61770b08
equip_activation_response_table_row_013_cid:
	.word 0x0000179e                                                           @ 09e48418 9e170000
equip_activation_response_table_row_013_callback:
	.word check_special_hurricane_response_eligible+1                            @ 09e4841c 39860b08
equip_activation_response_table_row_014_cid:
	.word 0x000010f7                                                           @ 09e48420 f7100000
equip_activation_response_table_row_014_callback:
	.word check_mass_removal_score_response_eligible+1                            @ 09e48424 59860b08
equip_activation_response_table_row_015_cid:
	.word 0x00001461                                                           @ 09e48428 61140000
equip_activation_response_table_row_015_callback:
	.word check_mass_removal_score_response_eligible+1                            @ 09e4842c 59860b08
equip_activation_response_table_row_016_cid:
	.word 0x000010f6                                                           @ 09e48430 f6100000
equip_activation_response_table_row_016_callback:
	.word check_dark_hole_score_response_eligible+1                            @ 09e48434 0d860b08
equip_activation_response_table_row_017_cid:
	.word 0x000014aa                                                           @ 09e48438 aa140000
equip_activation_response_table_row_017_callback:
	.word return_true_response_callback+1                                      @ 09e4843c a5760b08
equip_activation_response_table_row_018_cid:
	.word 0x000012fc                                                           @ 09e48440 fc120000
equip_activation_response_table_row_018_callback:
	.word check_control_change_hand_target_response_eligible+1                            @ 09e48444 21870b08
equip_activation_response_table_row_019_cid:
	.word 0x000012c3                                                           @ 09e48448 c3120000
equip_activation_response_table_row_019_callback:
	.word check_control_change_hand_target_response_eligible+1                            @ 09e4844c 21870b08
equip_activation_response_table_row_020_cid:
	.word 0x000018c6                                                           @ 09e48450 c6180000
equip_activation_response_table_row_020_callback:
	.word check_control_change_hand_target_response_eligible+1                            @ 09e48454 21870b08
equip_activation_response_table_row_021_cid:
	.word 0x000013eb                                                           @ 09e48458 eb130000
equip_activation_response_table_row_021_callback:
	.word check_opponent_equip_blockers_absent_then_control_change_eligible+1                            @ 09e4845c 5d880b08
equip_activation_response_table_row_022_cid:
	.word 0x00001322                                                           @ 09e48460 22130000
equip_activation_response_table_row_022_callback:
	.word check_snatch_steal_high_value_target_response_eligible+1                            @ 09e48464 858a0b08
equip_activation_response_table_row_023_cid:
	.word 0x0000169a                                                           @ 09e48468 9a160000
equip_activation_response_table_row_023_callback:
	.word check_falling_down_archfiend_target_response_eligible+1                            @ 09e4846c 398b0b08
equip_activation_response_table_row_024_cid:
	.word 0x000012d1                                                           @ 09e48470 d1120000
equip_activation_response_table_row_024_callback:
	.word check_mind_control_zone_response_eligible+1                            @ 09e48474 658b0b08
equip_activation_response_table_row_025_cid:
	.word 0x000014e0                                                           @ 09e48478 e0140000
equip_activation_response_table_row_025_callback:
	.word return_true_response_callback+1                                      @ 09e4847c a5760b08
equip_activation_response_table_row_026_cid:
	.word 0x000017f2                                                           @ 09e48480 f2170000
equip_activation_response_table_row_026_callback:
	.word check_hammer_shot_highest_score_on_opponent+1                            @ 09e48484 99860b08
equip_activation_response_table_row_027_cid:
	.word 0x000012f8                                                           @ 09e48488 f8120000
equip_activation_response_table_row_027_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e4848c a9760b08
equip_activation_response_table_row_028_cid:
	.word 0x0000145e                                                           @ 09e48490 5e140000
equip_activation_response_table_row_028_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48494 a9760b08
equip_activation_response_table_row_029_cid:
	.word 0x00001773                                                           @ 09e48498 73170000
equip_activation_response_table_row_029_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e4849c a9760b08
equip_activation_response_table_row_030_cid:
	.word 0x00001970                                                           @ 09e484a0 70190000
equip_activation_response_table_row_030_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e484a4 a9760b08
equip_activation_response_table_row_031_cid:
	.word 0x0000166f                                                           @ 09e484a8 6f160000
equip_activation_response_table_row_031_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e484ac a9760b08
equip_activation_response_table_row_032_cid:
	.word 0x00001319                                                           @ 09e484b0 19130000
equip_activation_response_table_row_032_callback:
	.word check_equip_owner_has_more_occupied_monster_zones+1                  @ 09e484b4 258a0b08
equip_activation_response_table_row_033_cid:
	.word 0x00001711                                                           @ 09e484b8 11170000
equip_activation_response_table_row_033_callback:
	.word return_true_response_callback+1                                      @ 09e484bc a5760b08
equip_activation_response_table_row_034_cid:
	.word 0x000012e3                                                           @ 09e484c0 e3120000
equip_activation_response_table_row_034_callback:
	.word return_true_response_callback+1                                      @ 09e484c4 a5760b08
equip_activation_response_table_row_035_cid:
	.word 0x00001430                                                           @ 09e484c8 30140000
equip_activation_response_table_row_035_callback:
	.word check_mystic_box_zone_count_response_eligible+1                            @ 09e484cc 558a0b08
equip_activation_response_table_row_036_cid:
	.word 0x000015e9                                                           @ 09e484d0 e9150000
equip_activation_response_table_row_036_callback:
	.word check_discard_bounce_target_response_eligible+1                            @ 09e484d4 15a90b08
equip_activation_response_table_row_037_cid:
	.word 0x00001844                                                           @ 09e484d8 44180000
equip_activation_response_table_row_037_callback:
	.word check_discard_bounce_target_response_eligible+1                            @ 09e484dc 15a90b08
equip_activation_response_table_row_038_cid:
	.word 0x000018cc                                                           @ 09e484e0 cc180000
equip_activation_response_table_row_038_callback:
	.word check_battery_charger_response_eligible+1                            @ 09e484e4 49a90b08
equip_activation_response_table_row_039_cid:
	.word 0x000012ea                                                           @ 09e484e8 ea120000
equip_activation_response_table_row_039_callback:
	.word check_monster_reborn_target_response_eligible+1                            @ 09e484ec b98b0b08
equip_activation_response_table_row_040_cid:
	.word 0x000014f7                                                           @ 09e484f0 f7140000
equip_activation_response_table_row_040_callback:
	.word check_silent_fiend_target_attribute_response_eligible+1                            @ 09e484f4 558c0b08
equip_activation_response_table_row_041_cid:
	.word 0x00001366                                                           @ 09e484f8 66130000
equip_activation_response_table_row_041_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e484fc 8d8c0b08
equip_activation_response_table_row_042_cid:
	.word 0x0000137d                                                           @ 09e48500 7d130000
equip_activation_response_table_row_042_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e48504 8d8c0b08
equip_activation_response_table_row_043_cid:
	.word 0x00001536                                                           @ 09e48508 36150000
equip_activation_response_table_row_043_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e4850c 8d8c0b08
equip_activation_response_table_row_044_cid:
	.word 0x000015e6                                                           @ 09e48510 e6150000
equip_activation_response_table_row_044_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e48514 8d8c0b08
equip_activation_response_table_row_045_cid:
	.word 0x000014f7                                                           @ 09e48518 f7140000
equip_activation_response_table_row_045_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e4851c 8d8c0b08
equip_activation_response_table_row_046_cid:
	.word 0x00001880                                                           @ 09e48520 80180000
equip_activation_response_table_row_046_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e48524 8d8c0b08
equip_activation_response_table_row_047_cid:
	.word 0x00001881                                                           @ 09e48528 81180000
equip_activation_response_table_row_047_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e4852c 8d8c0b08
equip_activation_response_table_row_048_cid:
	.word 0x000019d7                                                           @ 09e48530 d7190000
equip_activation_response_table_row_048_callback:
	.word check_grave_revival_target_response_eligible+1                            @ 09e48534 8d8c0b08
equip_activation_response_table_row_049_cid:
	.word 0x00001365                                                           @ 09e48538 65130000
equip_activation_response_table_row_049_callback:
	.word check_shallow_grave_dual_target_response_eligible+1                            @ 09e4853c 6d8d0b08
equip_activation_response_table_row_050_cid:
	.word 0x000015ed                                                           @ 09e48540 ed150000
equip_activation_response_table_row_050_callback:
	.word check_tribute_doll_target_score_response_eligible+1                            @ 09e48544 2d8e0b08
equip_activation_response_table_row_051_cid:
	.word 0x000012de                                                           @ 09e48548 de120000
equip_activation_response_table_row_051_callback:
	.word check_dark_magic_curtain_handler_response_eligible+1                            @ 09e4854c 698e0b08
equip_activation_response_table_row_052_cid:
	.word 0x00001600                                                           @ 09e48550 00160000
equip_activation_response_table_row_052_callback:
	.word return_true_response_callback+1                                      @ 09e48554 a5760b08
equip_activation_response_table_row_053_cid:
	.word 0x00001712                                                           @ 09e48558 12170000
equip_activation_response_table_row_053_callback:
	.word check_mass_revive_zone_capacity_response_eligible+1                            @ 09e4855c bd9a0b08
equip_activation_response_table_row_054_cid:
	.word 0x000017be                                                           @ 09e48560 be170000
equip_activation_response_table_row_054_callback:
	.word check_mass_revive_zone_capacity_response_eligible+1                            @ 09e48564 bd9a0b08
equip_activation_response_table_row_055_cid:
	.word 0x00001944                                                           @ 09e48568 44190000
equip_activation_response_table_row_055_callback:
	.word check_level_modulation_target_response_eligible+1                            @ 09e4856c f19b0b08
equip_activation_response_table_row_056_cid:
	.word 0x00001379                                                           @ 09e48570 79130000
equip_activation_response_table_row_056_callback:
	.word check_graverobber_target_response_eligible+1                            @ 09e48574 ad8e0b08
equip_activation_response_table_row_057_cid:
	.word 0x000019b1                                                           @ 09e48578 b1190000
equip_activation_response_table_row_057_callback:
	.word return_true_response_callback+1                                      @ 09e4857c a5760b08
equip_activation_response_table_row_058_cid:
	.word 0x00001247                                                           @ 09e48580 47120000
equip_activation_response_table_row_058_callback:
	.word return_true_response_callback+1                                      @ 09e48584 a5760b08
equip_activation_response_table_row_059_cid:
	.word 0x00001245                                                           @ 09e48588 45120000
equip_activation_response_table_row_059_callback:
	.word return_true_response_callback+1                                      @ 09e4858c a5760b08
equip_activation_response_table_row_060_cid:
	.word 0x00001244                                                           @ 09e48590 44120000
equip_activation_response_table_row_060_callback:
	.word return_true_response_callback+1                                      @ 09e48594 a5760b08
equip_activation_response_table_row_061_cid:
	.word 0x00001248                                                           @ 09e48598 48120000
equip_activation_response_table_row_061_callback:
	.word return_true_response_callback+1                                      @ 09e4859c a5760b08
equip_activation_response_table_row_062_cid:
	.word 0x0000124a                                                           @ 09e485a0 4a120000
equip_activation_response_table_row_062_callback:
	.word return_true_response_callback+1                                      @ 09e485a4 a5760b08
equip_activation_response_table_row_063_cid:
	.word 0x0000124b                                                           @ 09e485a8 4b120000
equip_activation_response_table_row_063_callback:
	.word return_true_response_callback+1                                      @ 09e485ac a5760b08
equip_activation_response_table_row_064_cid:
	.word 0x0000124d                                                           @ 09e485b0 4d120000
equip_activation_response_table_row_064_callback:
	.word return_true_response_callback+1                                      @ 09e485b4 a5760b08
equip_activation_response_table_row_065_cid:
	.word 0x0000125c                                                           @ 09e485b8 5c120000
equip_activation_response_table_row_065_callback:
	.word return_true_response_callback+1                                      @ 09e485bc a5760b08
equip_activation_response_table_row_066_cid:
	.word 0x0000125a                                                           @ 09e485c0 5a120000
equip_activation_response_table_row_066_callback:
	.word return_true_response_callback+1                                      @ 09e485c4 a5760b08
equip_activation_response_table_row_067_cid:
	.word 0x0000125f                                                           @ 09e485c8 5f120000
equip_activation_response_table_row_067_callback:
	.word return_true_response_callback+1                                      @ 09e485cc a5760b08
equip_activation_response_table_row_068_cid:
	.word 0x0000125e                                                           @ 09e485d0 5e120000
equip_activation_response_table_row_068_callback:
	.word return_true_response_callback+1                                      @ 09e485d4 a5760b08
equip_activation_response_table_row_069_cid:
	.word 0x00001262                                                           @ 09e485d8 62120000
equip_activation_response_table_row_069_callback:
	.word return_true_response_callback+1                                      @ 09e485dc a5760b08
equip_activation_response_table_row_070_cid:
	.word 0x00001261                                                           @ 09e485e0 61120000
equip_activation_response_table_row_070_callback:
	.word return_true_response_callback+1                                      @ 09e485e4 a5760b08
equip_activation_response_table_row_071_cid:
	.word 0x00001277                                                           @ 09e485e8 77120000
equip_activation_response_table_row_071_callback:
	.word return_true_response_callback+1                                      @ 09e485ec a5760b08
equip_activation_response_table_row_072_cid:
	.word 0x000012c2                                                           @ 09e485f0 c2120000
equip_activation_response_table_row_072_callback:
	.word check_opponent_chain_field_match_present+1                            @ 09e485f4 b1850b08
equip_activation_response_table_row_073_cid:
	.word 0x000013ef                                                           @ 09e485f8 ef130000
equip_activation_response_table_row_073_callback:
	.word return_true_response_callback+1                                      @ 09e485fc a5760b08
equip_activation_response_table_row_074_cid:
	.word 0x000015e1                                                           @ 09e48600 e1150000
equip_activation_response_table_row_074_callback:
	.word return_true_response_callback+1                                      @ 09e48604 a5760b08
equip_activation_response_table_row_075_cid:
	.word 0x00001659                                                           @ 09e48608 59160000
equip_activation_response_table_row_075_callback:
	.word return_true_response_callback+1                                      @ 09e4860c a5760b08
equip_activation_response_table_row_076_cid:
	.word 0x00001697                                                           @ 09e48610 97160000
equip_activation_response_table_row_076_callback:
	.word return_true_response_callback+1                                      @ 09e48614 a5760b08
equip_activation_response_table_row_077_cid:
	.word 0x00001699                                                           @ 09e48618 99160000
equip_activation_response_table_row_077_callback:
	.word return_true_response_callback+1                                      @ 09e4861c a5760b08
equip_activation_response_table_row_078_cid:
	.word 0x000018ce                                                           @ 09e48620 ce180000
equip_activation_response_table_row_078_callback:
	.word return_true_response_callback+1                                      @ 09e48624 a5760b08
equip_activation_response_table_row_079_cid:
	.word 0x000018cf                                                           @ 09e48628 cf180000
equip_activation_response_table_row_079_callback:
	.word return_true_response_callback+1                                      @ 09e4862c a5760b08
equip_activation_response_table_row_080_cid:
	.word 0x00001698                                                           @ 09e48630 98160000
equip_activation_response_table_row_080_callback:
	.word return_true_response_callback+1                                      @ 09e48634 a5760b08
equip_activation_response_table_row_081_cid:
	.word 0x00001716                                                           @ 09e48638 16170000
equip_activation_response_table_row_081_callback:
	.word return_true_response_callback+1                                      @ 09e4863c a5760b08
equip_activation_response_table_row_082_cid:
	.word 0x000019d9                                                           @ 09e48640 d9190000
equip_activation_response_table_row_082_callback:
	.word return_true_response_callback+1                                      @ 09e48644 a5760b08
equip_activation_response_table_row_083_cid:
	.word 0x00001237                                                           @ 09e48648 37120000
equip_activation_response_table_row_083_callback:
	.word check_megamorph_target_score_response_eligible+1                            @ 09e4864c 15950b08
equip_activation_response_table_row_084_cid:
	.word 0x000010d3                                                           @ 09e48650 d3100000
equip_activation_response_table_row_084_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48654 35970b08
equip_activation_response_table_row_085_cid:
	.word 0x000010d4                                                           @ 09e48658 d4100000
equip_activation_response_table_row_085_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4865c 35970b08
equip_activation_response_table_row_086_cid:
	.word 0x000010d5                                                           @ 09e48660 d5100000
equip_activation_response_table_row_086_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48664 35970b08
equip_activation_response_table_row_087_cid:
	.word 0x000010d6                                                           @ 09e48668 d6100000
equip_activation_response_table_row_087_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4866c 35970b08
equip_activation_response_table_row_088_cid:
	.word 0x000010d7                                                           @ 09e48670 d7100000
equip_activation_response_table_row_088_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48674 35970b08
equip_activation_response_table_row_089_cid:
	.word 0x000010d8                                                           @ 09e48678 d8100000
equip_activation_response_table_row_089_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4867c 35970b08
equip_activation_response_table_row_090_cid:
	.word 0x000010d9                                                           @ 09e48680 d9100000
equip_activation_response_table_row_090_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48684 35970b08
equip_activation_response_table_row_091_cid:
	.word 0x000010da                                                           @ 09e48688 da100000
equip_activation_response_table_row_091_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4868c 35970b08
equip_activation_response_table_row_092_cid:
	.word 0x000010db                                                           @ 09e48690 db100000
equip_activation_response_table_row_092_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48694 35970b08
equip_activation_response_table_row_093_cid:
	.word 0x000010dc                                                           @ 09e48698 dc100000
equip_activation_response_table_row_093_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4869c 35970b08
equip_activation_response_table_row_094_cid:
	.word 0x000010dd                                                           @ 09e486a0 dd100000
equip_activation_response_table_row_094_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486a4 35970b08
equip_activation_response_table_row_095_cid:
	.word 0x000010de                                                           @ 09e486a8 de100000
equip_activation_response_table_row_095_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486ac 35970b08
equip_activation_response_table_row_096_cid:
	.word 0x000010df                                                           @ 09e486b0 df100000
equip_activation_response_table_row_096_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486b4 35970b08
equip_activation_response_table_row_097_cid:
	.word 0x000010e0                                                           @ 09e486b8 e0100000
equip_activation_response_table_row_097_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486bc 35970b08
equip_activation_response_table_row_098_cid:
	.word 0x000010e1                                                           @ 09e486c0 e1100000
equip_activation_response_table_row_098_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486c4 35970b08
equip_activation_response_table_row_099_cid:
	.word 0x000010e2                                                           @ 09e486c8 e2100000
equip_activation_response_table_row_099_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486cc 35970b08
equip_activation_response_table_row_100_cid:
	.word 0x000010e3                                                           @ 09e486d0 e3100000
equip_activation_response_table_row_100_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486d4 35970b08
equip_activation_response_table_row_101_cid:
	.word 0x000010e5                                                           @ 09e486d8 e5100000
equip_activation_response_table_row_101_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486dc 35970b08
equip_activation_response_table_row_102_cid:
	.word 0x000010e7                                                           @ 09e486e0 e7100000
equip_activation_response_table_row_102_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486e4 35970b08
equip_activation_response_table_row_103_cid:
	.word 0x000010e8                                                           @ 09e486e8 e8100000
equip_activation_response_table_row_103_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486ec 35970b08
equip_activation_response_table_row_104_cid:
	.word 0x000010e9                                                           @ 09e486f0 e9100000
equip_activation_response_table_row_104_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486f4 35970b08
equip_activation_response_table_row_105_cid:
	.word 0x000010ea                                                           @ 09e486f8 ea100000
equip_activation_response_table_row_105_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e486fc 35970b08
equip_activation_response_table_row_106_cid:
	.word 0x000010eb                                                           @ 09e48700 eb100000
equip_activation_response_table_row_106_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48704 35970b08
equip_activation_response_table_row_107_cid:
	.word 0x000010ec                                                           @ 09e48708 ec100000
equip_activation_response_table_row_107_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4870c 35970b08
equip_activation_response_table_row_108_cid:
	.word 0x000010ed                                                           @ 09e48710 ed100000
equip_activation_response_table_row_108_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48714 35970b08
equip_activation_response_table_row_109_cid:
	.word 0x000010ee                                                           @ 09e48718 ee100000
equip_activation_response_table_row_109_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4871c 35970b08
equip_activation_response_table_row_110_cid:
	.word 0x00001234                                                           @ 09e48720 34120000
equip_activation_response_table_row_110_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48724 35970b08
equip_activation_response_table_row_111_cid:
	.word 0x00001238                                                           @ 09e48728 38120000
equip_activation_response_table_row_111_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4872c 35970b08
equip_activation_response_table_row_112_cid:
	.word 0x00001242                                                           @ 09e48730 42120000
equip_activation_response_table_row_112_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48734 35970b08
equip_activation_response_table_row_113_cid:
	.word 0x000012c6                                                           @ 09e48738 c6120000
equip_activation_response_table_row_113_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4873c 35970b08
equip_activation_response_table_row_114_cid:
	.word 0x000012ee                                                           @ 09e48740 ee120000
equip_activation_response_table_row_114_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48744 35970b08
equip_activation_response_table_row_115_cid:
	.word 0x000012ef                                                           @ 09e48748 ef120000
equip_activation_response_table_row_115_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4874c 35970b08
equip_activation_response_table_row_116_cid:
	.word 0x00001309                                                           @ 09e48750 09130000
equip_activation_response_table_row_116_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48754 35970b08
equip_activation_response_table_row_117_cid:
	.word 0x0000131a                                                           @ 09e48758 1a130000
equip_activation_response_table_row_117_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4875c 35970b08
equip_activation_response_table_row_118_cid:
	.word 0x00001392                                                           @ 09e48760 92130000
equip_activation_response_table_row_118_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48764 35970b08
equip_activation_response_table_row_119_cid:
	.word 0x000013f4                                                           @ 09e48768 f4130000
equip_activation_response_table_row_119_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4876c 35970b08
equip_activation_response_table_row_120_cid:
	.word 0x000013f6                                                           @ 09e48770 f6130000
equip_activation_response_table_row_120_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48774 35970b08
equip_activation_response_table_row_121_cid:
	.word 0x0000145c                                                           @ 09e48778 5c140000
equip_activation_response_table_row_121_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4877c 35970b08
equip_activation_response_table_row_122_cid:
	.word 0x0000145d                                                           @ 09e48780 5d140000
equip_activation_response_table_row_122_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48784 35970b08
equip_activation_response_table_row_123_cid:
	.word 0x00001467                                                           @ 09e48788 67140000
equip_activation_response_table_row_123_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4878c 35970b08
equip_activation_response_table_row_124_cid:
	.word 0x00001496                                                           @ 09e48790 96140000
equip_activation_response_table_row_124_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e48794 8d970b08
equip_activation_response_table_row_125_cid:
	.word 0x0000149f                                                           @ 09e48798 9f140000
equip_activation_response_table_row_125_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e4879c 35970b08
equip_activation_response_table_row_126_cid:
	.word 0x00001625                                                           @ 09e487a0 25160000
equip_activation_response_table_row_126_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e487a4 8d970b08
equip_activation_response_table_row_127_cid:
	.word 0x0000165c                                                           @ 09e487a8 5c160000
equip_activation_response_table_row_127_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487ac 35970b08
equip_activation_response_table_row_128_cid:
	.word 0x0000165d                                                           @ 09e487b0 5d160000
equip_activation_response_table_row_128_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e487b4 8d970b08
equip_activation_response_table_row_129_cid:
	.word 0x0000165e                                                           @ 09e487b8 5e160000
equip_activation_response_table_row_129_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487bc 35970b08
equip_activation_response_table_row_130_cid:
	.word 0x0000165f                                                           @ 09e487c0 5f160000
equip_activation_response_table_row_130_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e487c4 8d970b08
equip_activation_response_table_row_131_cid:
	.word 0x000017fa                                                           @ 09e487c8 fa170000
equip_activation_response_table_row_131_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487cc 35970b08
equip_activation_response_table_row_132_cid:
	.word 0x000017fb                                                           @ 09e487d0 fb170000
equip_activation_response_table_row_132_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487d4 35970b08
equip_activation_response_table_row_133_cid:
	.word 0x0000145b                                                           @ 09e487d8 5b140000
equip_activation_response_table_row_133_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e487dc 8d970b08
equip_activation_response_table_row_134_cid:
	.word 0x000014ed                                                           @ 09e487e0 ed140000
equip_activation_response_table_row_134_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487e4 35970b08
equip_activation_response_table_row_135_cid:
	.word 0x0000150c                                                           @ 09e487e8 0c150000
equip_activation_response_table_row_135_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487ec 35970b08
equip_activation_response_table_row_136_cid:
	.word 0x0000193a                                                           @ 09e487f0 3a190000
equip_activation_response_table_row_136_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e487f4 35970b08
equip_activation_response_table_row_137_cid:
	.word 0x00001992                                                           @ 09e487f8 92190000
equip_activation_response_table_row_137_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e487fc 8d970b08
equip_activation_response_table_row_138_cid:
	.word 0x0000197c                                                           @ 09e48800 7c190000
equip_activation_response_table_row_138_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e48804 8d970b08
equip_activation_response_table_row_139_cid:
	.word 0x00001841                                                           @ 09e48808 41180000
equip_activation_response_table_row_139_callback:
	.word check_generic_equip_target_available_response_eligible+1                            @ 09e4880c 71970b08
equip_activation_response_table_row_140_cid:
	.word 0x0000150a                                                           @ 09e48810 0a150000
equip_activation_response_table_row_140_callback:
	.word check_heart_of_clear_water_target_response_eligible+1                            @ 09e48814 1d980b08
equip_activation_response_table_row_141_cid:
	.word 0x00001514                                                           @ 09e48818 14150000
equip_activation_response_table_row_141_callback:
	.word check_blast_with_chain_target_score_response_eligible+1                            @ 09e4881c c5960b08
equip_activation_response_table_row_142_cid:
	.word 0x00001759                                                           @ 09e48820 59170000
equip_activation_response_table_row_142_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e48824 8d970b08
equip_activation_response_table_row_143_cid:
	.word 0x00001660                                                           @ 09e48828 60160000
equip_activation_response_table_row_143_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e4882c 8d970b08
equip_activation_response_table_row_144_cid:
	.word 0x00001391                                                           @ 09e48830 91130000
equip_activation_response_table_row_144_callback:
	.word check_riryoku_chain_match_response_eligible+1                            @ 09e48834 bd980b08
equip_activation_response_table_row_145_cid:
	.word 0x00001257                                                           @ 09e48838 57120000
equip_activation_response_table_row_145_callback:
	.word check_reverse_trap_zone_score_response_eligible+1                            @ 09e4883c 11930b08
equip_activation_response_table_row_146_cid:
	.word 0x000014d0                                                           @ 09e48840 d0140000
equip_activation_response_table_row_146_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48844 1d770b08
equip_activation_response_table_row_147_cid:
	.word 0x000014d2                                                           @ 09e48848 d2140000
equip_activation_response_table_row_147_callback:
	.word return_true_response_callback+1                                      @ 09e4884c a5760b08
equip_activation_response_table_row_148_cid:
	.word 0x000017b3                                                           @ 09e48850 b3170000
equip_activation_response_table_row_148_callback:
	.word check_curse_of_anubis_multi_target_response_eligible+1                            @ 09e48854 91900b08
equip_activation_response_table_row_149_cid:
	.word 0x0000130a                                                           @ 09e48858 0a130000
equip_activation_response_table_row_149_callback:
	.word check_block_attack_target_score_response_eligible+1                            @ 09e4885c d1900b08
equip_activation_response_table_row_150_cid:
	.word 0x00001913                                                           @ 09e48860 13190000
equip_activation_response_table_row_150_callback:
	.word check_block_attack_target_score_response_eligible+1                            @ 09e48864 d1900b08
equip_activation_response_table_row_151_cid:
	.word 0x000010e6                                                           @ 09e48868 e6100000
equip_activation_response_table_row_151_callback:
	.word check_stop_defense_target_score_response_eligible+1                            @ 09e4886c 698f0b08
equip_activation_response_table_row_152_cid:
	.word 0x00001581                                                           @ 09e48870 81150000
equip_activation_response_table_row_152_callback:
	.word check_enemy_controller_target_score_response_eligible+1                            @ 09e48874 f9910b08
equip_activation_response_table_row_153_cid:
	.word 0x000012cb                                                           @ 09e48878 cb120000
equip_activation_response_table_row_153_callback:
	.word check_shield_and_sword_zone_score_response_eligible+1                            @ 09e4887c 99930b08
equip_activation_response_table_row_154_cid:
	.word 0x000012d5                                                           @ 09e48880 d5120000
equip_activation_response_table_row_154_callback:
	.word check_card_destruction_hand_response_eligible+1                            @ 09e48884 f1930b08
equip_activation_response_table_row_155_cid:
	.word 0x00001462                                                           @ 09e48888 62140000
equip_activation_response_table_row_155_callback:
	.word check_exchange_hand_target_response_eligible+1                            @ 09e4888c fd940b08
equip_activation_response_table_row_156_cid:
	.word 0x0000147e                                                           @ 09e48890 7e140000
equip_activation_response_table_row_156_callback:
	.word return_true_response_callback+1                                      @ 09e48894 a5760b08
equip_activation_response_table_row_157_cid:
	.word 0x00001321                                                           @ 09e48898 21130000
equip_activation_response_table_row_157_callback:
	.word check_final_destiny_opponent_score_advantage+1                            @ 09e4889c 0d870b08
equip_activation_response_table_row_158_cid:
	.word 0x000017f9                                                           @ 09e488a0 f9170000
equip_activation_response_table_row_158_callback:
	.word check_big_wave_small_wave_response_eligible+1                            @ 09e488a4 7d9b0b08
equip_activation_response_table_row_159_cid:
	.word 0x00001769                                                           @ 09e488a8 69170000
equip_activation_response_table_row_159_callback:
	.word check_beckoning_light_response_eligible+1                            @ 09e488ac b99b0b08
equip_activation_response_table_row_160_cid:
	.word 0x0000198d                                                           @ 09e488b0 8d190000
equip_activation_response_table_row_160_callback:
	.word check_magical_mallet_hand_response_eligible+1                            @ 09e488b4 b1990b08
equip_activation_response_table_row_161_cid:
	.word 0x000016d9                                                           @ 09e488b8 d9160000
equip_activation_response_table_row_161_callback:
	.word check_hand_reload_response_eligible+1                            @ 09e488bc f1980b08
equip_activation_response_table_row_162_cid:
	.word 0x000014e8                                                           @ 09e488c0 e8140000
equip_activation_response_table_row_162_callback:
	.word check_hand_reload_response_eligible+1                            @ 09e488c4 f1980b08
equip_activation_response_table_row_163_cid:
	.word 0x0000187a                                                           @ 09e488c8 7a180000
equip_activation_response_table_row_163_callback:
	.word check_discard_recovery_spell_response_eligible+1                            @ 09e488cc c9950b08
equip_activation_response_table_row_164_cid:
	.word 0x000014ea                                                           @ 09e488d0 ea140000
equip_activation_response_table_row_164_callback:
	.word check_discard_recovery_spell_response_eligible+1                            @ 09e488d4 c9950b08
@ F15-Seg-5: three equip activation response rows.
equip_activation_three_row_response_table:
	.word WILD_NATURES_RELEASE_CID                              @ 09e488d8 ce160000
equip_activation_three_row_response_table_row_000_callback:
	.word check_effect_node_eligible_in_any_slot_with_field6_score+1 @ 09e488dc f9790b08
equip_activation_three_row_response_table_row_001_cid:
	.word METEORAIN_CID                                         @ 09e488e0 f2150000
equip_activation_three_row_response_table_row_001_callback:
	.word check_opponent_active_zone_cards_present+1            @ 09e488e4 497a0b08
equip_activation_three_row_response_table_row_002_cid:
	.word DRAGONS_RAGE_CID                                      @ 09e488e8 e3140000
equip_activation_three_row_response_table_row_002_callback:
	.word check_opponent_active_zone_cards_present+1            @ 09e488ec 497a0b08

equip_activation_secondary_response_table:
equip_activation_secondary_response_table:
	.word 0x000015e4                                                           @ 09e488f0 e4150000
equip_activation_secondary_response_table_row_000_callback:
	.word return_true_response_callback+1                                      @ 09e488f4 a5760b08
equip_activation_secondary_response_table_row_001_cid:
	.word 0x0000192f                                                           @ 09e488f8 2f190000
equip_activation_secondary_response_table_row_001_callback:
	.word return_true_response_callback+1                                      @ 09e488fc a5760b08
equip_activation_secondary_response_table_row_002_cid:
	.word 0x000013fe                                                           @ 09e48900 fe130000
equip_activation_secondary_response_table_row_002_callback:
	.word check_de_fusion_response_eligible+1                            @ 09e48904 b97b0b08
equip_activation_secondary_response_table_row_003_cid:
	.word 0x00001889                                                           @ 09e48908 89180000
equip_activation_secondary_response_table_row_003_callback:
	.word check_beast_soul_swap_target_slot_eligible+1                            @ 09e4890c 697a0b08
equip_activation_secondary_response_table_row_004_cid:
	.word 0x00001927                                                           @ 09e48910 27190000
equip_activation_secondary_response_table_row_004_callback:
	.word check_spiritual_earth_art_target_slot_eligible+1                            @ 09e48914 197b0b08
effect_zone_response_table:
effect_zone_response_table:
	.word 0x000010f8                                                           @ 09e48918 f8100000
effect_zone_response_table_row_000_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4891c 7d770b08
effect_zone_response_table_row_001_cid:
	.word 0x000010f9                                                           @ 09e48920 f9100000
effect_zone_response_table_row_001_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48924 7d770b08
effect_zone_response_table_row_002_cid:
	.word 0x000010fa                                                           @ 09e48928 fa100000
effect_zone_response_table_row_002_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4892c 7d770b08
effect_zone_response_table_row_003_cid:
	.word 0x000010fb                                                           @ 09e48930 fb100000
effect_zone_response_table_row_003_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48934 7d770b08
effect_zone_response_table_row_004_cid:
	.word 0x000010fc                                                           @ 09e48938 fc100000
effect_zone_response_table_row_004_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4893c 7d770b08
effect_zone_response_table_row_005_cid:
	.word 0x000012e8                                                           @ 09e48940 e8120000
effect_zone_response_table_row_005_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48944 7d770b08
effect_zone_response_table_row_006_cid:
	.word 0x0000141f                                                           @ 09e48948 1f140000
effect_zone_response_table_row_006_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e4894c 7d770b08
effect_zone_response_table_row_007_cid:
	.word 0x000015e7                                                           @ 09e48950 e7150000
effect_zone_response_table_row_007_callback:
	.word check_effect_zone_available_from_zone_ptr+1                          @ 09e48954 7d770b08
effect_zone_response_table_row_008_cid:
	.word 0x000012ec                                                           @ 09e48958 ec120000
effect_zone_response_table_row_008_callback:
	.word check_pot_draw_count_response_eligible+1                            @ 09e4895c 299c0b08
effect_zone_response_table_row_009_cid:
	.word 0x0000196f                                                           @ 09e48960 6f190000
effect_zone_response_table_row_009_callback:
	.word check_pot_draw_count_response_eligible+1                            @ 09e48964 299c0b08
effect_zone_response_table_row_010_cid:
	.word 0x0000131f                                                           @ 09e48968 1f130000
effect_zone_response_table_row_010_callback:
	.word return_true_response_callback+1                                      @ 09e4896c a5760b08
effect_zone_response_table_row_011_cid:
	.word 0x0000145a                                                           @ 09e48970 5a140000
effect_zone_response_table_row_011_callback:
	.word return_true_response_callback+1                                      @ 09e48974 a5760b08
effect_zone_response_table_row_012_cid:
	.word 0x00001776                                                           @ 09e48978 76170000
effect_zone_response_table_row_012_callback:
	.word return_true_response_callback+1                                      @ 09e4897c a5760b08
effect_zone_response_table_row_013_cid:
	.word 0x000012ca                                                           @ 09e48980 ca120000
effect_zone_response_table_row_013_callback:
	.word return_true_response_callback+1                                      @ 09e48984 a5760b08
effect_zone_response_table_row_014_cid:
	.word 0x0000175b                                                           @ 09e48988 5b170000
effect_zone_response_table_row_014_callback:
	.word return_true_response_callback+1                                      @ 09e4898c a5760b08
effect_zone_response_table_row_015_cid:
	.word 0x0000142e                                                           @ 09e48990 2e140000
effect_zone_response_table_row_015_callback:
	.word return_true_response_callback+1                                      @ 09e48994 a5760b08
effect_zone_response_table_row_016_cid:
	.word 0x000017a9                                                           @ 09e48998 a9170000
effect_zone_response_table_row_016_callback:
	.word return_true_response_callback+1                                      @ 09e4899c a5760b08
effect_zone_response_table_row_017_cid:
	.word 0x000016cf                                                           @ 09e489a0 cf160000
effect_zone_response_table_row_017_callback:
	.word return_true_response_callback+1                                      @ 09e489a4 a5760b08
effect_zone_response_table_row_018_cid:
	.word 0x00001923                                                           @ 09e489a8 23190000
effect_zone_response_table_row_018_callback:
	.word return_true_response_callback+1                                      @ 09e489ac a5760b08
effect_zone_response_table_row_019_cid:
	.word 0x000010e4                                                           @ 09e489b0 e4100000
effect_zone_response_table_row_019_callback:
	.word return_true_response_callback+1                                      @ 09e489b4 a5760b08
effect_zone_response_table_row_020_cid:
	.word 0x0000165b                                                           @ 09e489b8 5b160000
effect_zone_response_table_row_020_callback:
	.word return_true_response_callback+1                                      @ 09e489bc a5760b08
effect_zone_response_table_row_021_cid:
	.word 0x00001714                                                           @ 09e489c0 14170000
effect_zone_response_table_row_021_callback:
	.word return_true_response_callback+1                                      @ 09e489c4 a5760b08
effect_zone_response_table_row_022_cid:
	.word 0x000017f1                                                           @ 09e489c8 f1170000
effect_zone_response_table_row_022_callback:
	.word return_true_response_callback+1                                      @ 09e489cc a5760b08
effect_zone_response_table_row_023_cid:
	.word 0x000017a2                                                           @ 09e489d0 a2170000
effect_zone_response_table_row_023_callback:
	.word return_true_response_callback+1                                      @ 09e489d4 a5760b08
effect_zone_response_table_row_024_cid:
	.word 0x00001664                                                           @ 09e489d8 64160000
effect_zone_response_table_row_024_callback:
	.word return_true_response_callback+1                                      @ 09e489dc a5760b08
effect_zone_response_table_row_025_cid:
	.word 0x0000162d                                                           @ 09e489e0 2d160000
effect_zone_response_table_row_025_callback:
	.word return_true_response_callback+1                                      @ 09e489e4 a5760b08
effect_zone_response_table_row_026_cid:
	.word 0x00001509                                                           @ 09e489e8 09150000
effect_zone_response_table_row_026_callback:
	.word return_true_response_callback+1                                      @ 09e489ec a5760b08
effect_zone_response_table_row_027_cid:
	.word 0x000015ef                                                           @ 09e489f0 ef150000
effect_zone_response_table_row_027_callback:
	.word return_true_response_callback+1                                      @ 09e489f4 a5760b08
effect_zone_response_table_row_028_cid:
	.word 0x00001629                                                           @ 09e489f8 29160000
effect_zone_response_table_row_028_callback:
	.word return_true_response_callback+1                                      @ 09e489fc a5760b08
effect_zone_response_table_row_029_cid:
	.word 0x00001713                                                           @ 09e48a00 13170000
effect_zone_response_table_row_029_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a04 1d770b08
effect_zone_response_table_row_030_cid:
	.word 0x0000187e                                                           @ 09e48a08 7e180000
effect_zone_response_table_row_030_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a0c 1d770b08
effect_zone_response_table_row_031_cid:
	.word 0x0000167e                                                           @ 09e48a10 7e160000
effect_zone_response_table_row_031_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a14 1d770b08
effect_zone_response_table_row_032_cid:
	.word 0x000015e0                                                           @ 09e48a18 e0150000
effect_zone_response_table_row_032_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a1c 1d770b08
effect_zone_response_table_row_033_cid:
	.word 0x00001529                                                           @ 09e48a20 29150000
effect_zone_response_table_row_033_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a24 1d770b08
effect_zone_response_table_row_034_cid:
	.word 0x0000195c                                                           @ 09e48a28 5c190000
effect_zone_response_table_row_034_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a2c 1d770b08
effect_zone_response_table_row_035_cid:
	.word 0x00001626                                                           @ 09e48a30 26160000
effect_zone_response_table_row_035_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48a34 1d770b08
effect_zone_response_table_row_036_cid:
	.word 0x000012c5                                                           @ 09e48a38 c5120000
effect_zone_response_table_row_036_callback:
	.word return_true_response_callback+1                                      @ 09e48a3c a5760b08
effect_zone_response_table_row_037_cid:
	.word 0x000017f7                                                           @ 09e48a40 f7170000
effect_zone_response_table_row_037_callback:
	.word return_true_response_callback+1                                      @ 09e48a44 a5760b08
effect_zone_response_table_row_038_cid:
	.word 0x00001820                                                           @ 09e48a48 20180000
effect_zone_response_table_row_038_callback:
	.word check_hand_equip_target_available_for_zone+1                         @ 09e48a4c 45770b08
effect_zone_response_table_row_039_cid:
	.word 0x000014e1                                                           @ 09e48a50 e1140000
effect_zone_response_table_row_039_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48a54 a9760b08
effect_zone_response_table_row_040_cid:
	.word 0x00001842                                                           @ 09e48a58 42180000
effect_zone_response_table_row_040_callback:
	.word check_equip_debuff_target_score_response_eligible+1                            @ 09e48a5c 69980b08
effect_zone_response_table_row_041_cid:
	.word 0x000018d1                                                           @ 09e48a60 d1180000
effect_zone_response_table_row_041_callback:
	.word check_equip_debuff_target_score_response_eligible+1                            @ 09e48a64 69980b08
effect_zone_response_table_row_042_cid:
	.word 0x00001876                                                           @ 09e48a68 76180000
effect_zone_response_table_row_042_callback:
	.word check_rescue_cat_handler_response_eligible+1                            @ 09e48a6c 299d0b08
effect_zone_response_table_row_043_cid:
	.word 0x0000167d                                                           @ 09e48a70 7d160000
effect_zone_response_table_row_043_callback:
	.word check_knights_title_handler_response_eligible+1                            @ 09e48a74 dd9c0b08
effect_zone_response_table_row_044_cid:
	.word 0x00001475                                                           @ 09e48a78 75140000
effect_zone_response_table_row_044_callback:
	.word check_makiu_target_score_response_eligible+1                            @ 09e48a7c 519c0b08
effect_zone_response_table_row_045_cid:
	.word 0x000017f6                                                           @ 09e48a80 f6170000
effect_zone_response_table_row_045_callback:
	.word check_inferno_fire_blast_active_equip_response_eligible+1                            @ 09e48a84 099d0b08
effect_zone_response_table_row_046_cid:
	.word 0x000017ab                                                           @ 09e48a88 ab170000
effect_zone_response_table_row_046_callback:
	.word check_slot_chain_value_absent_response_eligible+1                            @ 09e48a8c 519d0b08
effect_zone_response_table_row_047_cid:
	.word 0x000017ac                                                           @ 09e48a90 ac170000
effect_zone_response_table_row_047_callback:
	.word check_slot_chain_value_absent_response_eligible+1                            @ 09e48a94 519d0b08
effect_zone_response_table_row_048_cid:
	.word 0x00001840                                                           @ 09e48a98 40180000
effect_zone_response_table_row_048_callback:
	.word check_slot_chain_value_absent_response_eligible+1                            @ 09e48a9c 519d0b08
effect_zone_response_table_row_049_cid:
	.word 0x000015e2                                                           @ 09e48aa0 e2150000
effect_zone_response_table_row_049_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e48aa4 e5760b08
effect_zone_response_table_row_050_cid:
	.word 0x0000153b                                                           @ 09e48aa8 3b150000
effect_zone_response_table_row_050_callback:
	.word check_call_of_the_mummy_response_eligible+1                            @ 09e48aac 719d0b08
effect_zone_response_table_row_051_cid:
	.word 0x0000146f                                                           @ 09e48ab0 6f140000
effect_zone_response_table_row_051_callback:
	.word check_cathedral_of_nobles_response_eligible+1                            @ 09e48ab4 99830b08
effect_zone_response_table_row_052_cid:
	.word 0x00001232                                                           @ 09e48ab8 32120000
effect_zone_response_table_row_052_callback:
	.word check_special_equip_target_handler_response_eligible+1                            @ 09e48abc b5970b08
effect_zone_response_table_row_053_cid:
	.word 0x000012d3                                                           @ 09e48ac0 d3120000
effect_zone_response_table_row_053_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48ac4 35970b08
effect_zone_response_table_row_054_cid:
	.word 0x00001408                                                           @ 09e48ac8 08140000
effect_zone_response_table_row_054_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e48acc 8d970b08
effect_zone_response_table_row_055_cid:
	.word 0x00001661                                                           @ 09e48ad0 61160000
effect_zone_response_table_row_055_callback:
	.word check_generic_equip_target_score_response_eligible+1                            @ 09e48ad4 35970b08
effect_zone_response_table_row_056_cid:
	.word 0x000016cc                                                           @ 09e48ad8 cc160000
effect_zone_response_table_row_056_callback:
	.word check_generic_equip_target_available_response_eligible+1                            @ 09e48adc 71970b08
effect_zone_response_table_row_057_cid:
	.word 0x00001989                                                           @ 09e48ae0 89190000
effect_zone_response_table_row_057_callback:
	.word check_generic_equip_target_available_response_eligible+1                            @ 09e48ae4 71970b08
effect_zone_response_table_row_058_cid:
	.word 0x000019b0                                                           @ 09e48ae8 b0190000
effect_zone_response_table_row_058_callback:
	.word check_generic_equip_target_available_response_eligible+1                            @ 09e48aec 71970b08
effect_zone_response_table_row_059_cid:
	.word 0x000019d8                                                           @ 09e48af0 d8190000
effect_zone_response_table_row_059_callback:
	.word check_special_equip_target_handler_response_eligible+1                            @ 09e48af4 b5970b08
effect_zone_response_table_row_060_cid:
	.word 0x00001562                                                           @ 09e48af8 62150000
effect_zone_response_table_row_060_callback:
	.word check_toon_table_contents_search_response_eligible+1                            @ 09e48afc 8d9d0b08
effect_zone_response_table_row_061_cid:
	.word 0x00001474                                                           @ 09e48b00 74140000
effect_zone_response_table_row_061_callback:
	.word return_true_response_callback+1                                      @ 09e48b04 a5760b08
effect_zone_response_table_row_062_cid:
	.word 0x00000fee                                                           @ 09e48b08 ee0f0000
effect_zone_response_table_row_062_callback:
	.word check_self_effect_node_active+1                                      @ 09e48b0c c9760b08
effect_zone_response_table_row_063_cid:
	.word 0x00001624                                                           @ 09e48b10 24160000
effect_zone_response_table_row_063_callback:
	.word check_self_effect_node_active+1                                      @ 09e48b14 c9760b08
effect_zone_response_table_row_064_cid:
	.word 0x00001636                                                           @ 09e48b18 36160000
effect_zone_response_table_row_064_callback:
	.word check_metal_reflect_slime_pair_response_eligible+1                            @ 09e48b1c f19e0b08
effect_zone_response_table_row_065_cid:
	.word 0x000015a3                                                           @ 09e48b20 a3150000
effect_zone_response_table_row_065_callback:
	.word check_metamorphosis_nonspell_target_response_eligible+1                            @ 09e48b24 099f0b08
effect_zone_response_table_row_066_cid:
	.word 0x00001717                                                           @ 09e48b28 17170000
effect_zone_response_table_row_066_callback:
	.word check_jade_insect_whistle_chain_response_eligible+1                            @ 09e48b2c b59e0b08
effect_zone_response_table_row_067_cid:
	.word 0x0000142a                                                           @ 09e48b30 2a140000
effect_zone_response_table_row_067_callback:
	.word check_creature_swap_response_eligible+1                            @ 09e48b34 31830b08
effect_zone_response_table_row_068_cid:
	.word 0x000018ca                                                           @ 09e48b38 ca180000
effect_zone_response_table_row_068_callback:
	.word check_tribute_handler_response_eligible+1                            @ 09e48b3c 19a00b08
effect_zone_response_table_row_069_cid:
	.word 0x000016a0                                                           @ 09e48b40 a0160000
effect_zone_response_table_row_069_callback:
	.word check_tribute_handler_response_eligible+1                            @ 09e48b44 19a00b08
effect_zone_response_table_row_070_cid:
	.word 0x00001893                                                           @ 09e48b48 93180000
effect_zone_response_table_row_070_callback:
	.word check_overpowering_eye_peak_score_response_eligible+1                            @ 09e48b4c c19f0b08
effect_zone_response_table_row_071_cid:
	.word 0x00001845                                                           @ 09e48b50 45180000
effect_zone_response_table_row_071_callback:
	.word check_monster_reincarnation_source_response_eligible+1                            @ 09e48b54 5d9f0b08
effect_zone_response_table_row_072_cid:
	.word 0x000013fc                                                           @ 09e48b58 fc130000
effect_zone_response_table_row_072_callback:
	.word check_multiplication_of_ants_response_eligible+1                            @ 09e48b5c b5820b08
effect_zone_response_table_row_073_cid:
	.word 0x00001638                                                           @ 09e48b60 38160000
effect_zone_response_table_row_073_callback:
	.word check_excavation_mage_stones_response_eligible+1                            @ 09e48b64 359e0b08
effect_zone_response_table_row_074_cid:
	.word 0x000017f5                                                           @ 09e48b68 f5170000
effect_zone_response_table_row_074_callback:
	.word check_level_up_evolution_target_response_eligible+1                            @ 09e48b6c 6d9e0b08
effect_zone_response_table_row_075_cid:
	.word 0x000015ff                                                           @ 09e48b70 ff150000
effect_zone_response_table_row_075_callback:
	.word check_diffusion_wave_motion_response_eligible+1                            @ 09e48b74 4da80b08
effect_zone_response_table_row_076_cid:
	.word 0x0000169b                                                           @ 09e48b78 9b160000
effect_zone_response_table_row_076_callback:
	.word check_checkmate_archfiend_count_response_eligible+1                            @ 09e48b7c 91a80b08
effect_zone_response_table_row_077_cid:
	.word 0x000016a3                                                           @ 09e48b80 a3160000
effect_zone_response_table_row_077_callback:
	.word check_dark_scorpion_combination_response_eligible+1                            @ 09e48b84 e5a80b08
effect_zone_response_table_row_078_cid:
	.word 0x000012ed                                                           @ 09e48b88 ed120000
effect_zone_response_table_row_078_callback:
	.word check_gravedigger_ghoul_opponent_hand_targets_available+1                            @ 09e48b8c 71820b08
effect_zone_response_table_row_079_cid:
	.word 0x0000175c                                                           @ 09e48b90 5c170000
effect_zone_response_table_row_079_callback:
	.word check_monster_gate_target_slot_available+1                            @ 09e48b94 85840b08
effect_zone_response_table_row_080_cid:
	.word 0x0000169e                                                           @ 09e48b98 9e160000
effect_zone_response_table_row_080_callback:
	.word check_mustering_dark_scorpions_response_eligible+1                            @ 09e48b9c e5830b08
effect_zone_response_table_row_081_cid:
	.word 0x0000140b                                                           @ 09e48ba0 0b140000
effect_zone_response_table_row_081_callback:
	.word check_insect_imitation_slot_handler_eligible+1                            @ 09e48ba4 e9820b08
effect_zone_response_table_row_082_cid:
	.word 0x000017a1                                                           @ 09e48ba8 a1170000
effect_zone_response_table_row_082_callback:
	.word check_dust_barrier_response_eligible+1                            @ 09e48bac 9d840b08
effect_zone_response_table_row_083_cid:
	.word 0x00001954                                                           @ 09e48bb0 54190000
effect_zone_response_table_row_083_callback:
	.word return_true_response_callback+1                                      @ 09e48bb4 a5760b08
effect_zone_response_table_row_084_cid:
	.word 0x00001281                                                           @ 09e48bb8 81120000
effect_zone_response_table_row_084_callback:
	.word return_true_response_callback+1                                      @ 09e48bbc a5760b08
effect_zone_response_table_row_085_cid:
	.word 0x00001284                                                           @ 09e48bc0 84120000
effect_zone_response_table_row_085_callback:
	.word return_true_response_callback+1                                      @ 09e48bc4 a5760b08
effect_zone_response_table_row_086_cid:
	.word 0x0000128d                                                           @ 09e48bc8 8d120000
effect_zone_response_table_row_086_callback:
	.word return_true_response_callback+1                                      @ 09e48bcc a5760b08
effect_zone_response_table_row_087_cid:
	.word 0x0000174c                                                           @ 09e48bd0 4c170000
effect_zone_response_table_row_087_callback:
	.word return_true_response_callback+1                                      @ 09e48bd4 a5760b08
effect_zone_response_table_row_088_cid:
	.word 0x0000161a                                                           @ 09e48bd8 1a160000
effect_zone_response_table_row_088_callback:
	.word return_true_response_callback+1                                      @ 09e48bdc a5760b08
effect_zone_response_table_row_089_cid:
	.word 0x000019c8                                                           @ 09e48be0 c8190000
effect_zone_response_table_row_089_callback:
	.word return_true_response_callback+1                                      @ 09e48be4 a5760b08
effect_zone_response_table_row_090_cid:
	.word 0x000019a3                                                           @ 09e48be8 a3190000
effect_zone_response_table_row_090_callback:
	.word return_true_response_callback+1                                      @ 09e48bec a5760b08
effect_zone_response_table_row_091_cid:
	.word 0x00001895                                                           @ 09e48bf0 95180000
effect_zone_response_table_row_091_callback:
	.word return_true_response_callback+1                                      @ 09e48bf4 a5760b08
effect_zone_response_table_row_092_cid:
	.word 0x000017dd                                                           @ 09e48bf8 dd170000
effect_zone_response_table_row_092_callback:
	.word return_true_response_callback+1                                      @ 09e48bfc a5760b08
effect_zone_response_table_row_093_cid:
	.word 0x000018f0                                                           @ 09e48c00 f0180000
effect_zone_response_table_row_093_callback:
	.word return_true_response_callback+1                                      @ 09e48c04 a5760b08
effect_zone_response_table_row_094_cid:
	.word 0x00001748                                                           @ 09e48c08 48170000
effect_zone_response_table_row_094_callback:
	.word return_true_response_callback+1                                      @ 09e48c0c a5760b08
effect_zone_response_table_row_095_cid:
	.word 0x00001879                                                           @ 09e48c10 79180000
effect_zone_response_table_row_095_callback:
	.word return_true_response_callback+1                                      @ 09e48c14 a5760b08
effect_zone_response_table_row_096_cid:
	.word 0x000016b2                                                           @ 09e48c18 b2160000
effect_zone_response_table_row_096_callback:
	.word return_true_response_callback+1                                      @ 09e48c1c a5760b08
effect_zone_response_table_row_097_cid:
	.word 0x0000189a                                                           @ 09e48c20 9a180000
effect_zone_response_table_row_097_callback:
	.word return_true_response_callback+1                                      @ 09e48c24 a5760b08
effect_zone_response_table_row_098_cid:
	.word 0x0000186f                                                           @ 09e48c28 6f180000
effect_zone_response_table_row_098_callback:
	.word return_true_response_callback+1                                      @ 09e48c2c a5760b08
effect_zone_response_table_row_099_cid:
	.word 0x00001482                                                           @ 09e48c30 82140000
effect_zone_response_table_row_099_callback:
	.word return_true_response_callback+1                                      @ 09e48c34 a5760b08
effect_zone_response_table_row_100_cid:
	.word 0x000016c4                                                           @ 09e48c38 c4160000
effect_zone_response_table_row_100_callback:
	.word return_true_response_callback+1                                      @ 09e48c3c a5760b08
effect_zone_response_table_row_101_cid:
	.word 0x00001870                                                           @ 09e48c40 70180000
effect_zone_response_table_row_101_callback:
	.word return_true_response_callback+1                                      @ 09e48c44 a5760b08
effect_zone_response_table_row_102_cid:
	.word 0x00001871                                                           @ 09e48c48 71180000
effect_zone_response_table_row_102_callback:
	.word return_true_response_callback+1                                      @ 09e48c4c a5760b08
effect_zone_response_table_row_103_cid:
	.word 0x00001872                                                           @ 09e48c50 72180000
effect_zone_response_table_row_103_callback:
	.word return_true_response_callback+1                                      @ 09e48c54 a5760b08
effect_zone_response_table_row_104_cid:
	.word 0x00001821                                                           @ 09e48c58 21180000
effect_zone_response_table_row_104_callback:
	.word return_true_response_callback+1                                      @ 09e48c5c a5760b08
effect_zone_response_table_row_105_cid:
	.word 0x00001708                                                           @ 09e48c60 08170000
effect_zone_response_table_row_105_callback:
	.word return_true_response_callback+1                                      @ 09e48c64 a5760b08
effect_zone_response_table_row_106_cid:
	.word 0x0000191e                                                           @ 09e48c68 1e190000
effect_zone_response_table_row_106_callback:
	.word return_true_response_callback+1                                      @ 09e48c6c a5760b08
effect_zone_response_table_row_107_cid:
	.word 0x000019a9                                                           @ 09e48c70 a9190000
effect_zone_response_table_row_107_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48c74 a9760b08
effect_zone_response_table_row_108_cid:
	.word 0x000018c9                                                           @ 09e48c78 c9180000
effect_zone_response_table_row_108_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48c7c a9760b08
effect_zone_response_table_row_109_cid:
	.word 0x00001962                                                           @ 09e48c80 62190000
effect_zone_response_table_row_109_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48c84 a9760b08
effect_zone_response_table_row_110_cid:
	.word 0x000014b8                                                           @ 09e48c88 b8140000
effect_zone_response_table_row_110_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48c8c a9760b08
effect_zone_response_table_row_111_cid:
	.word 0x0000178f                                                           @ 09e48c90 8f170000
effect_zone_response_table_row_111_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48c94 a9760b08
effect_zone_response_table_row_112_cid:
	.word 0x000015b1                                                           @ 09e48c98 b1150000
effect_zone_response_table_row_112_callback:
	.word check_hand_equip_target_available_for_zone+1                         @ 09e48c9c 45770b08
effect_zone_response_table_row_113_cid:
	.word 0x000015f9                                                           @ 09e48ca0 f9150000
effect_zone_response_table_row_113_callback:
	.word check_hand_equip_target_available_for_zone+1                         @ 09e48ca4 45770b08
effect_zone_response_table_row_114_cid:
	.word 0x000015fa                                                           @ 09e48ca8 fa150000
effect_zone_response_table_row_114_callback:
	.word check_hand_equip_target_available_for_zone+1                         @ 09e48cac 45770b08
effect_zone_response_table_row_115_cid:
	.word 0x000015b4                                                           @ 09e48cb0 b4150000
effect_zone_response_table_row_115_callback:
	.word check_xyz_dragon_cannon_zone_response_eligible+1                            @ 09e48cb4 01a40b08
effect_zone_response_table_row_116_cid:
	.word 0x00001953                                                           @ 09e48cb8 53190000
effect_zone_response_table_row_116_callback:
	.word check_vw_tiger_catapult_zone_response_eligible+1                            @ 09e48cbc 51a40b08
effect_zone_response_table_row_117_cid:
	.word 0x0000186a                                                           @ 09e48cc0 6a180000
effect_zone_response_table_row_117_callback:
	.word apply_blast_magician_slot_value_and_check_response+1                            @ 09e48cc4 19a50b08
effect_zone_response_table_row_118_cid:
	.word 0x000018e8                                                           @ 09e48cc8 e8180000
effect_zone_response_table_row_118_callback:
	.word check_neo_daedalus_field_clear_response_eligible+1                            @ 09e48ccc 3da50b08
effect_zone_response_table_row_119_cid:
	.word 0x00001707                                                           @ 09e48cd0 07170000
effect_zone_response_table_row_119_callback:
	.word check_ritual_field_clear_response_eligible+1                            @ 09e48cd4 89a40b08
effect_zone_response_table_row_120_cid:
	.word 0x00001695                                                           @ 09e48cd8 95160000
effect_zone_response_table_row_120_callback:
	.word check_ritual_field_clear_response_eligible+1                            @ 09e48cdc 89a40b08
effect_zone_response_table_row_121_cid:
	.word 0x000019d5                                                           @ 09e48ce0 d5190000
effect_zone_response_table_row_121_callback:
	.word check_ritual_field_clear_response_eligible+1                            @ 09e48ce4 89a40b08
effect_zone_response_table_row_122_cid:
	.word 0x00001153                                                           @ 09e48ce8 53110000
effect_zone_response_table_row_122_callback:
	.word check_goddess_of_whim_slot_response_eligible+1                            @ 09e48cec cda30b08
effect_zone_response_table_row_123_cid:
	.word 0x0000152a                                                           @ 09e48cf0 2a150000
effect_zone_response_table_row_123_callback:
	.word mark_swarm_effect_mode_and_check_response+1                            @ 09e48cf4 c5a50b08
effect_zone_response_table_row_124_cid:
	.word 0x0000152b                                                           @ 09e48cf8 2b150000
effect_zone_response_table_row_124_callback:
	.word mark_swarm_effect_mode_and_check_response+1                            @ 09e48cfc c5a50b08
effect_zone_response_table_row_125_cid:
	.word 0x000016cb                                                           @ 09e48d00 cb160000
effect_zone_response_table_row_125_callback:
	.word check_chaos_banish_response_eligible+1                            @ 09e48d04 e1a70b08
effect_zone_response_table_row_126_cid:
	.word 0x000016c9                                                           @ 09e48d08 c9160000
effect_zone_response_table_row_126_callback:
	.word check_chaos_banish_response_eligible+1                            @ 09e48d0c e1a70b08
effect_zone_response_table_row_127_cid:
	.word 0x00001727                                                           @ 09e48d10 27170000
effect_zone_response_table_row_127_callback:
	.word check_discard_bounce_target_response_eligible+1                            @ 09e48d14 15a90b08
effect_zone_response_table_row_128_cid:
	.word 0x00001611                                                           @ 09e48d18 11160000
effect_zone_response_table_row_128_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48d1c 1d770b08
effect_zone_response_table_row_129_cid:
	.word 0x00001610                                                           @ 09e48d20 10160000
effect_zone_response_table_row_129_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48d24 1d770b08
effect_zone_response_table_row_130_cid:
	.word 0x00001900                                                           @ 09e48d28 00190000
effect_zone_response_table_row_130_callback:
	.word check_effect_handler_result_positive+1                               @ 09e48d2c 1d770b08
effect_zone_response_table_row_131_cid:
	.word 0x00000fb6                                                           @ 09e48d30 b60f0000
effect_zone_response_table_row_131_callback:
	.word check_time_wizard_zone_score_response_eligible+1                            @ 09e48d34 d5a10b08
effect_zone_response_table_row_132_cid:
	.word 0x0000147f                                                           @ 09e48d38 7f140000
effect_zone_response_table_row_132_callback:
	.word check_jowgen_zone_activation_absent_response_eligible+1                            @ 09e48d3c f1a10b08
effect_zone_response_table_row_133_cid:
	.word 0x0000144b                                                           @ 09e48d40 4b140000
effect_zone_response_table_row_133_callback:
	.word check_amazon_archer_monster_count_response_eligible+1                            @ 09e48d44 0da20b08
effect_zone_response_table_row_134_cid:
	.word 0x0000144c                                                           @ 09e48d48 4c140000
effect_zone_response_table_row_134_callback:
	.word check_forgiving_maiden_target_response_eligible+1                            @ 09e48d4c 4da20b08
effect_zone_response_table_row_135_cid:
	.word 0x00001457                                                           @ 09e48d50 57140000
effect_zone_response_table_row_135_callback:
	.word check_forgiving_maiden_target_response_eligible+1                            @ 09e48d54 4da20b08
effect_zone_response_table_row_136_cid:
	.word 0x00001337                                                           @ 09e48d58 37130000
effect_zone_response_table_row_136_callback:
	.word check_karate_man_slot_score_response_eligible+1                            @ 09e48d5c 9da20b08
effect_zone_response_table_row_137_cid:
	.word 0x0000138a                                                           @ 09e48d60 8a130000
effect_zone_response_table_row_137_callback:
	.word check_valkyrion_opponent_zone_empty_response_eligible+1                            @ 09e48d64 59a30b08
effect_zone_response_table_row_138_cid:
	.word 0x0000114a                                                           @ 09e48d68 4a110000
effect_zone_response_table_row_138_callback:
	.word check_cyber_stein_target_response_eligible+1                            @ 09e48d6c 89a30b08
effect_zone_response_table_row_139_cid:
	.word 0x000015b0                                                           @ 09e48d70 b0150000
effect_zone_response_table_row_139_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48d74 29a60b08
effect_zone_response_table_row_140_cid:
	.word 0x000015b3                                                           @ 09e48d78 b3150000
effect_zone_response_table_row_140_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48d7c 29a60b08
effect_zone_response_table_row_141_cid:
	.word 0x000015ce                                                           @ 09e48d80 ce150000
effect_zone_response_table_row_141_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48d84 29a60b08
effect_zone_response_table_row_142_cid:
	.word 0x000015cf                                                           @ 09e48d88 cf150000
effect_zone_response_table_row_142_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48d8c 29a60b08
effect_zone_response_table_row_143_cid:
	.word 0x000015d1                                                           @ 09e48d90 d1150000
effect_zone_response_table_row_143_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48d94 29a60b08
effect_zone_response_table_row_144_cid:
	.word 0x000015d3                                                           @ 09e48d98 d3150000
effect_zone_response_table_row_144_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48d9c 29a60b08
effect_zone_response_table_row_145_cid:
	.word 0x000015d5                                                           @ 09e48da0 d5150000
effect_zone_response_table_row_145_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48da4 29a60b08
effect_zone_response_table_row_146_cid:
	.word 0x000015d6                                                           @ 09e48da8 d6150000
effect_zone_response_table_row_146_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48dac 29a60b08
effect_zone_response_table_row_147_cid:
	.word 0x000015d7                                                           @ 09e48db0 d7150000
effect_zone_response_table_row_147_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48db4 29a60b08
effect_zone_response_table_row_148_cid:
	.word 0x00001620                                                           @ 09e48db8 20160000
effect_zone_response_table_row_148_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48dbc 29a60b08
effect_zone_response_table_row_149_cid:
	.word 0x00001693                                                           @ 09e48dc0 93160000
effect_zone_response_table_row_149_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48dc4 29a60b08
effect_zone_response_table_row_150_cid:
	.word 0x00001825                                                           @ 09e48dc8 25180000
effect_zone_response_table_row_150_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48dcc 29a60b08
effect_zone_response_table_row_151_cid:
	.word 0x00001916                                                           @ 09e48dd0 16190000
effect_zone_response_table_row_151_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48dd4 29a60b08
effect_zone_response_table_row_152_cid:
	.word 0x00001917                                                           @ 09e48dd8 17190000
effect_zone_response_table_row_152_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48ddc 29a60b08
effect_zone_response_table_row_153_cid:
	.word 0x0000194b                                                           @ 09e48de0 4b190000
effect_zone_response_table_row_153_callback:
	.word check_union_equip_chain_absent_response_eligible+1                            @ 09e48de4 29a60b08
effect_zone_response_table_row_154_cid:
	.word 0x0000161c                                                           @ 09e48de8 1c160000
effect_zone_response_table_row_154_callback:
	.word check_tribe_infecting_virus_response_eligible+1                            @ 09e48dec d5850b08
effect_zone_response_table_row_155_cid:
	.word 0x000014cb                                                           @ 09e48df0 cb140000
effect_zone_response_table_row_155_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48df4 a9760b08
effect_zone_response_table_row_156_cid:
	.word 0x00001386                                                           @ 09e48df8 86130000
effect_zone_response_table_row_156_callback:
	.word invoke_count_occupied_monster_zones+1                                @ 09e48dfc fdac0b08
effect_zone_response_table_row_157_cid:
	.word 0x00001617                                                           @ 09e48e00 17160000
effect_zone_response_table_row_157_callback:
	.word check_breaker_whitelist_response_eligible+1                            @ 09e48e04 79a60b08
effect_zone_response_table_row_158_cid:
	.word 0x0000128e                                                           @ 09e48e08 8e120000
effect_zone_response_table_row_158_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48e0c a9760b08
effect_zone_response_table_row_159_cid:
	.word 0x00001295                                                           @ 09e48e10 95120000
effect_zone_response_table_row_159_callback:
	.word check_gear_golem_slot_score_response_eligible+1                            @ 09e48e14 75a70b08
effect_zone_response_table_row_160_cid:
	.word 0x00001857                                                           @ 09e48e18 57180000
effect_zone_response_table_row_160_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e48e1c a9760b08
effect_zone_response_table_row_161_cid:
	.word 0x000019b2                                                           @ 09e48e20 b2190000
effect_zone_response_table_row_161_callback:
	.word return_true_response_callback+1                                      @ 09e48e24 a5760b08
effect_zone_response_table_row_162_cid:
	.word 0x00001741                                                           @ 09e48e28 41170000
effect_zone_response_table_row_162_callback:
	.word return_true_response_callback+1                                      @ 09e48e2c a5760b08
effect_zone_response_table_row_163_cid:
	.word 0x0000173f                                                           @ 09e48e30 3f170000
effect_zone_response_table_row_163_callback:
	.word check_agent_saturn_lp_ratio_response_eligible+1                            @ 09e48e34 ada60b08
effect_zone_response_table_row_164_cid:
	.word 0x0000198c                                                           @ 09e48e38 8c190000
effect_zone_response_table_row_164_callback:
	.word check_armed_dragon_lv10_response_eligible+1                            @ 09e48e3c f5a90b08
effect_zone_response_table_row_165_cid:
	.word 0x000017db                                                           @ 09e48e40 db170000
effect_zone_response_table_row_165_callback:
	.word check_armed_dragon_lv7_response_eligible+1                            @ 09e48e44 a9a90b08
effect_zone_response_table_row_166_cid:
	.word 0x000017da                                                           @ 09e48e48 da170000
effect_zone_response_table_row_166_callback:
	.word check_armed_dragon_lv5_response_eligible+1                            @ 09e48e4c 89a90b08
effect_zone_response_table_row_167_cid:
	.word 0x00001835                                                           @ 09e48e50 35180000
effect_zone_response_table_row_167_callback:
	.word check_gaia_soul_target_response_eligible+1                            @ 09e48e54 2daa0b08
effect_zone_response_table_row_168_cid:
	.word 0x00001696                                                           @ 09e48e58 96160000
effect_zone_response_table_row_168_callback:
	.word check_zorc_opponent_monster_present_response_eligible+1                            @ 09e48e5c 89aa0b08
effect_zone_response_table_row_169_cid:
	.word 0x00001878                                                           @ 09e48e60 78180000
effect_zone_response_table_row_169_callback:
	.word check_gatling_dragon_multiple_opponents_response_eligible+1                            @ 09e48e64 c9aa0b08
effect_zone_response_table_row_170_cid:
	.word 0x00001507                                                           @ 09e48e68 07150000
effect_zone_response_table_row_170_callback:
	.word check_zorc_opponent_monster_present_response_eligible+1                            @ 09e48e6c 89aa0b08
effect_zone_response_table_row_171_cid:
	.word 0x00001508                                                           @ 09e48e70 08150000
effect_zone_response_table_row_171_callback:
	.word check_super_robolady_opponent_zone_empty_response_eligible+1                            @ 09e48e74 a9aa0b08
effect_zone_response_table_row_172_cid:
	.word 0x0000185d                                                           @ 09e48e78 5d180000
effect_zone_response_table_row_172_callback:
	.word check_hand_of_nephthys_target_response_eligible+1                            @ 09e48e7c e9aa0b08
effect_zone_response_table_row_173_cid:
	.word 0x00001957                                                           @ 09e48e80 57190000
effect_zone_response_table_row_173_callback:
	.word check_elemental_hero_tempest_whitelist_response_eligible+1                            @ 09e48e84 1dab0b08
effect_zone_response_table_row_174_cid:
	.word 0x000019a5                                                           @ 09e48e88 a5190000
effect_zone_response_table_row_174_callback:
	.word check_raviel_token_pair_response_eligible+1                            @ 09e48e8c 3dab0b08
effect_zone_response_table_row_175_cid:
	.word 0x00001758                                                           @ 09e48e90 58170000
effect_zone_response_table_row_175_callback:
	.word check_archlord_zerato_field_spell_response_eligible+1                            @ 09e48e94 a9ab0b08
effect_zone_response_table_row_176_cid:
	.word 0x00001810                                                           @ 09e48e98 10180000
effect_zone_response_table_row_176_callback:
	.word check_selected_slot_word12_above_one_response_eligible+1                            @ 09e48e9c cdac0b08
effect_zone_response_table_row_177_cid:
	.word 0x000015bc                                                           @ 09e48ea0 bc150000
effect_zone_response_table_row_177_callback:
	.word check_hand_equip_target_meets_bonus_4+1                              @ 09e48ea4 d5ab0b08
effect_zone_response_table_row_178_cid:
	.word 0x0000150b                                                           @ 09e48ea8 0b150000
effect_zone_response_table_row_178_callback:
	.word check_field_spell_slot_empty_or_umi+1                            @ 09e48eac 1d850b08
effect_zone_response_table_row_179_cid:
	.word 0x0000183f                                                           @ 09e48eb0 3f180000
effect_zone_response_table_row_179_callback:
	.word check_harpies_hunting_ground_response_eligible+1                            @ 09e48eb4 69850b08
effect_zone_response_table_row_180_cid:
	.word 0x000010f0                                                           @ 09e48eb8 f0100000
effect_zone_response_table_row_180_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48ebc d9840b08
effect_zone_response_table_row_181_cid:
	.word 0x000010f1                                                           @ 09e48ec0 f1100000
effect_zone_response_table_row_181_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48ec4 d9840b08
effect_zone_response_table_row_182_cid:
	.word 0x000010f2                                                           @ 09e48ec8 f2100000
effect_zone_response_table_row_182_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48ecc d9840b08
effect_zone_response_table_row_183_cid:
	.word 0x000010f3                                                           @ 09e48ed0 f3100000
effect_zone_response_table_row_183_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48ed4 d9840b08
effect_zone_response_table_row_184_cid:
	.word 0x000010f4                                                           @ 09e48ed8 f4100000
effect_zone_response_table_row_184_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48edc d9840b08
effect_zone_response_table_row_185_cid:
	.word 0x000010f5                                                           @ 09e48ee0 f5100000
effect_zone_response_table_row_185_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48ee4 d9840b08
effect_zone_response_table_row_186_cid:
	.word 0x00001323                                                           @ 09e48ee8 23130000
effect_zone_response_table_row_186_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48eec d9840b08
effect_zone_response_table_row_187_cid:
	.word 0x00001344                                                           @ 09e48ef0 44130000
effect_zone_response_table_row_187_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48ef4 d9840b08
effect_zone_response_table_row_188_cid:
	.word 0x00001345                                                           @ 09e48ef8 45130000
effect_zone_response_table_row_188_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48efc d9840b08
effect_zone_response_table_row_189_cid:
	.word 0x00001346                                                           @ 09e48f00 46130000
effect_zone_response_table_row_189_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f04 d9840b08
effect_zone_response_table_row_190_cid:
	.word 0x00001347                                                           @ 09e48f08 47130000
effect_zone_response_table_row_190_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f0c d9840b08
effect_zone_response_table_row_191_cid:
	.word 0x00001348                                                           @ 09e48f10 48130000
effect_zone_response_table_row_191_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f14 d9840b08
effect_zone_response_table_row_192_cid:
	.word 0x00001349                                                           @ 09e48f18 49130000
effect_zone_response_table_row_192_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f1c d9840b08
effect_zone_response_table_row_193_cid:
	.word 0x000014d1                                                           @ 09e48f20 d1140000
effect_zone_response_table_row_193_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f24 d9840b08
effect_zone_response_table_row_194_cid:
	.word 0x0000159d                                                           @ 09e48f28 9d150000
effect_zone_response_table_row_194_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f2c d9840b08
effect_zone_response_table_row_195_cid:
	.word 0x0000169f                                                           @ 09e48f30 9f160000
effect_zone_response_table_row_195_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f34 d9840b08
effect_zone_response_table_row_196_cid:
	.word 0x0000175e                                                           @ 09e48f38 5e170000
effect_zone_response_table_row_196_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f3c d9840b08
effect_zone_response_table_row_197_cid:
	.word 0x0000187f                                                           @ 09e48f40 7f180000
effect_zone_response_table_row_197_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f44 d9840b08
effect_zone_response_table_row_198_cid:
	.word 0x000018ff                                                           @ 09e48f48 ff180000
effect_zone_response_table_row_198_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f4c d9840b08
effect_zone_response_table_row_199_cid:
	.word 0x000019f2                                                           @ 09e48f50 f2190000
effect_zone_response_table_row_199_callback:
	.word check_player_field_spell_slot_empty+1                            @ 09e48f54 d9840b08
effect_zone_response_table_row_200_cid:
	.word 0x000012e5                                                           @ 09e48f58 e5120000
effect_zone_response_table_row_200_callback:
	.word return_true_response_callback+1                                      @ 09e48f5c a5760b08
effect_zone_response_table_row_201_cid:
	.word 0x00001303                                                           @ 09e48f60 03130000
effect_zone_response_table_row_201_callback:
	.word return_true_response_callback+1                                      @ 09e48f64 a5760b08
effect_zone_response_table_row_202_cid:
	.word 0x000018fe                                                           @ 09e48f68 fe180000
effect_zone_response_table_row_202_callback:
	.word return_true_response_callback+1                                      @ 09e48f6c a5760b08
effect_zone_response_table_row_203_cid:
	.word 0x0000149c                                                           @ 09e48f70 9c140000
effect_zone_response_table_row_203_callback:
	.word check_fusion_gate_response_eligible+1                            @ 09e48f74 01850b08
effect_zone_response_table_row_204_cid:
	.word 0x00001920                                                           @ 09e48f78 20190000
effect_zone_response_table_row_204_callback:
	.word return_true_response_callback+1                                      @ 09e48f7c a5760b08
effect_zone_response_table_row_205_cid:
	.word 0x00001921                                                           @ 09e48f80 21190000
effect_zone_response_table_row_205_callback:
	.word return_true_response_callback+1                                      @ 09e48f84 a5760b08
effect_zone_response_table_row_206_cid:
	.word 0x0000191f                                                           @ 09e48f88 1f190000
effect_zone_response_table_row_206_callback:
	.word return_true_response_callback+1                                      @ 09e48f8c a5760b08
field_spell_activation_response_table:
field_spell_activation_response_table:
	.word 0x00001527                                                           @ 09e48f90 27150000
field_spell_activation_response_table_row_000_callback:
	.word return_true_response_callback+1                                      @ 09e48f94 a5760b08
field_spell_activation_response_table_row_001_cid:
	.word 0x0000152a                                                           @ 09e48f98 2a150000
field_spell_activation_response_table_row_001_callback:
	.word return_true_response_callback+1                                      @ 09e48f9c a5760b08
field_spell_activation_response_table_row_002_cid:
	.word 0x0000152b                                                           @ 09e48fa0 2b150000
field_spell_activation_response_table_row_002_callback:
	.word return_true_response_callback+1                                      @ 09e48fa4 a5760b08
field_spell_activation_response_table_row_003_cid:
	.word 0x0000152c                                                           @ 09e48fa8 2c150000
field_spell_activation_response_table_row_003_callback:
	.word return_true_response_callback+1                                      @ 09e48fac a5760b08
field_spell_activation_response_table_row_004_cid:
	.word 0x0000152d                                                           @ 09e48fb0 2d150000
field_spell_activation_response_table_row_004_callback:
	.word return_true_response_callback+1                                      @ 09e48fb4 a5760b08
field_spell_activation_response_table_row_005_cid:
	.word 0x0000152e                                                           @ 09e48fb8 2e150000
field_spell_activation_response_table_row_005_callback:
	.word return_true_response_callback+1                                      @ 09e48fbc a5760b08
field_spell_activation_response_table_row_006_cid:
	.word 0x00001533                                                           @ 09e48fc0 33150000
field_spell_activation_response_table_row_006_callback:
	.word return_true_response_callback+1                                      @ 09e48fc4 a5760b08
field_spell_activation_response_table_row_007_cid:
	.word 0x00001535                                                           @ 09e48fc8 35150000
field_spell_activation_response_table_row_007_callback:
	.word return_true_response_callback+1                                      @ 09e48fcc a5760b08
field_spell_activation_response_table_row_008_cid:
	.word 0x000016fa                                                           @ 09e48fd0 fa160000
field_spell_activation_response_table_row_008_callback:
	.word return_true_response_callback+1                                      @ 09e48fd4 a5760b08
field_spell_activation_response_table_row_009_cid:
	.word 0x0000186e                                                           @ 09e48fd8 6e180000
field_spell_activation_response_table_row_009_callback:
	.word return_true_response_callback+1                                      @ 09e48fdc a5760b08
field_spell_activation_response_table_row_010_cid:
	.word 0x000018b3                                                           @ 09e48fe0 b3180000
field_spell_activation_response_table_row_010_callback:
	.word return_true_response_callback+1                                      @ 09e48fe4 a5760b08
field_spell_activation_response_table_row_011_cid:
	.word 0x000018ba                                                           @ 09e48fe8 ba180000
field_spell_activation_response_table_row_011_callback:
	.word return_true_response_callback+1                                      @ 09e48fec a5760b08
field_spell_activation_response_table_row_012_cid:
	.word 0x000018bb                                                           @ 09e48ff0 bb180000
field_spell_activation_response_table_row_012_callback:
	.word return_true_response_callback+1                                      @ 09e48ff4 a5760b08
field_spell_activation_response_table_row_013_cid:
	.word 0x000018bd                                                           @ 09e48ff8 bd180000
field_spell_activation_response_table_row_013_callback:
	.word return_true_response_callback+1                                      @ 09e48ffc a5760b08
field_spell_activation_response_table_row_014_cid:
	.word 0x000019f1                                                           @ 09e49000 f1190000
field_spell_activation_response_table_row_014_callback:
	.word return_true_response_callback+1                                      @ 09e49004 a5760b08
field_spell_activation_response_table_row_015_cid:
	.word 0x000016e4                                                           @ 09e49008 e4160000
field_spell_activation_response_table_row_015_callback:
	.word check_lp_below_zone_count_threshold+1                                @ 09e4900c 11ad0b08
field_spell_activation_response_table_row_016_cid:
	.word 0x000011a6                                                           @ 09e49010 a6110000
field_spell_activation_response_table_row_016_callback:
	.word check_cannon_soldier_target_response_eligible+1                            @ 09e49014 35a10b08
field_spell_activation_response_table_row_017_cid:
	.word 0x00001565                                                           @ 09e49018 65150000
field_spell_activation_response_table_row_017_callback:
	.word check_cannon_soldier_target_response_eligible+1                            @ 09e4901c 35a10b08
field_spell_activation_response_table_row_018_cid:
	.word 0x00000fff                                                           @ 09e49020 ff0f0000
field_spell_activation_response_table_row_018_callback:
	.word check_catapult_turtle_target_score_response_eligible+1                            @ 09e49024 91a00b08
field_spell_activation_response_table_row_019_cid:
	.word 0x000017e1                                                           @ 09e49028 e1170000
field_spell_activation_response_table_row_019_callback:
	.word check_ultimate_baseball_kid_threshold_response_eligible+1                            @ 09e4902c 95a10b08
field_spell_activation_response_table_row_020_cid:
	.word 0x00001627                                                           @ 09e49030 27160000
field_spell_activation_response_table_row_020_callback:
	.word check_cannon_soldier_target_response_eligible+1                            @ 09e49034 35a10b08
field_spell_activation_response_table_row_021_cid:
	.word 0x00001984                                                           @ 09e49038 84190000
field_spell_activation_response_table_row_021_callback:
	.word check_equip_effect_zone_eligible_for_rapid_fire_and_warlock+1        @ 09e4903c f5ad0b08
field_spell_activation_response_table_row_022_cid:
	.word 0x00001710                                                           @ 09e49040 10170000
field_spell_activation_response_table_row_022_callback:
	.word return_true_response_callback+1                                      @ 09e49044 a5760b08
field_spell_activation_response_table_row_023_cid:
	.word 0x0000175f                                                           @ 09e49048 5f170000
field_spell_activation_response_table_row_023_callback:
	.word check_earthquake_pair_response_eligible+1                            @ 09e4904c d19e0b08
field_spell_activation_response_table_row_024_cid:
	.word 0x00001537                                                           @ 09e49050 37150000
field_spell_activation_response_table_row_024_callback:
	.word check_book_of_taiyou_restricted_inactive_target_available+1                            @ 09e49054 65810b08
field_spell_activation_response_table_row_025_cid:
	.word 0x0000169c                                                           @ 09e49058 9c160000
field_spell_activation_response_table_row_025_callback:
	.word check_slot_chain_value_absent_response_eligible+1                            @ 09e4905c 519d0b08
field_spell_activation_response_table_row_026_cid:
	.word 0x00001315                                                           @ 09e49060 15130000
field_spell_activation_response_table_row_026_callback:
	.word check_last_will_player_state_bit0+1                            @ 09e49064 91820b08
field_spell_activation_response_table_row_027_cid:
	.word 0x000012ce                                                           @ 09e49068 ce120000
field_spell_activation_response_table_row_027_callback:
	.word check_mesmeric_control_lower_opponent_score_target+1                            @ 09e4906c b97e0b08
field_spell_activation_response_table_row_028_cid:
	.word 0x0000159f                                                           @ 09e49070 9f150000
field_spell_activation_response_table_row_028_callback:
	.word check_hieroglyph_lithograph_chain_clear_and_count_above_six+1                            @ 09e49074 d1810b08
field_spell_activation_response_table_row_029_cid:
	.word 0x0000130d                                                           @ 09e49078 0d130000
field_spell_activation_response_table_row_029_callback:
	.word check_equip_debuff_target_score_response_eligible+1                            @ 09e4907c 69980b08
field_spell_activation_response_table_row_030_cid:
	.word 0x0000130e                                                           @ 09e49080 0e130000
field_spell_activation_response_table_row_030_callback:
	.word check_equip_debuff_target_score_response_eligible+1                            @ 09e49084 69980b08
field_spell_activation_response_table_row_031_cid:
	.word 0x000013f3                                                           @ 09e49088 f3130000
field_spell_activation_response_table_row_031_callback:
	.word check_equip_debuff_target_score_response_eligible+1                            @ 09e4908c 69980b08
field_spell_activation_response_table_row_032_cid:
	.word 0x0000149d                                                           @ 09e49090 9d140000
field_spell_activation_response_table_row_032_callback:
	.word check_equip_debuff_target_score_response_eligible+1                            @ 09e49094 69980b08
field_spell_activation_response_table_row_033_cid:
	.word 0x00001318                                                           @ 09e49098 18130000
field_spell_activation_response_table_row_033_callback:
	.word check_equip_pair_and_target_response_eligible+1                            @ 09e4909c 8d970b08
field_spell_activation_response_table_row_034_cid:
	.word 0x000015ee                                                           @ 09e490a0 ee150000
field_spell_activation_response_table_row_034_callback:
	.word check_wave_motion_cannon_response_eligible+1                            @ 09e490a4 09820b08
field_spell_activation_response_table_row_035_cid:
	.word 0x00001429                                                           @ 09e490a8 29140000
field_spell_activation_response_table_row_035_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490ac e5760b08
field_spell_activation_response_table_row_036_cid:
	.word 0x000012dc                                                           @ 09e490b0 dc120000
field_spell_activation_response_table_row_036_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490b4 e5760b08
field_spell_activation_response_table_row_037_cid:
	.word 0x0000162e                                                           @ 09e490b8 2e160000
field_spell_activation_response_table_row_037_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490bc e5760b08
field_spell_activation_response_table_row_038_cid:
	.word 0x00001510                                                           @ 09e490c0 10150000
field_spell_activation_response_table_row_038_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490c4 e5760b08
field_spell_activation_response_table_row_039_cid:
	.word 0x000016d0                                                           @ 09e490c8 d0160000
field_spell_activation_response_table_row_039_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490cc e5760b08
field_spell_activation_response_table_row_040_cid:
	.word 0x00001662                                                           @ 09e490d0 62160000
field_spell_activation_response_table_row_040_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490d4 e5760b08
field_spell_activation_response_table_row_041_cid:
	.word 0x000016d4                                                           @ 09e490d8 d4160000
field_spell_activation_response_table_row_041_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e490dc e5760b08
field_spell_activation_response_table_row_042_cid:
	.word 0x0000159c                                                           @ 09e490e0 9c150000
field_spell_activation_response_table_row_042_callback:
	.word check_effect_handler_result_positive+1                               @ 09e490e4 1d770b08
field_spell_activation_response_table_row_043_cid:
	.word 0x000013f5                                                           @ 09e490e8 f5130000
field_spell_activation_response_table_row_043_callback:
	.word check_effect_handler_result_positive+1                               @ 09e490ec 1d770b08
field_spell_activation_response_table_row_044_cid:
	.word 0x00001102                                                           @ 09e490f0 02110000
field_spell_activation_response_table_row_044_callback:
	.word check_lock_card_counts_and_opponent_score_advantage+1                            @ 09e490f4 bd800b08
field_spell_activation_response_table_row_045_cid:
	.word 0x00001400                                                           @ 09e490f8 00140000
field_spell_activation_response_table_row_045_callback:
	.word check_lock_card_counts_and_opponent_score_advantage+1                            @ 09e490fc bd800b08
field_spell_activation_response_table_row_046_cid:
	.word 0x0000187c                                                           @ 09e49100 7c180000
field_spell_activation_response_table_row_046_callback:
	.word check_lock_card_counts_and_opponent_score_advantage+1                            @ 09e49104 bd800b08
field_spell_activation_response_table_row_047_cid:
	.word 0x0000134a                                                           @ 09e49108 4a130000
field_spell_activation_response_table_row_047_callback:
	.word check_lock_card_counts_and_opponent_score_advantage+1                            @ 09e4910c bd800b08
field_spell_activation_response_table_row_048_cid:
	.word 0x000018d2                                                           @ 09e49110 d2180000
field_spell_activation_response_table_row_048_callback:
	.word check_equip_eligible_by_slot_flag_or_pair_count+1                    @ 09e49114 6dad0b08
field_spell_activation_response_table_row_049_cid:
	.word 0x0000131d                                                           @ 09e49118 1d130000
field_spell_activation_response_table_row_049_callback:
	.word return_true_response_callback+1                                      @ 09e4911c a5760b08
field_spell_activation_response_table_row_050_cid:
	.word 0x00001320                                                           @ 09e49120 20130000
field_spell_activation_response_table_row_050_callback:
	.word return_true_response_callback+1                                      @ 09e49124 a5760b08
field_spell_activation_response_table_row_051_cid:
	.word 0x000017a5                                                           @ 09e49128 a5170000
field_spell_activation_response_table_row_051_callback:
	.word return_true_response_callback+1                                      @ 09e4912c a5760b08
field_spell_activation_response_table_row_052_cid:
	.word 0x00001432                                                           @ 09e49130 32140000
field_spell_activation_response_table_row_052_callback:
	.word check_opponent_monster_zone_has_multiple_vacancies+1                                     @ 09e49134 957f0b08
field_spell_activation_response_table_row_053_cid:
	.word 0x00001406                                                           @ 09e49138 06140000
field_spell_activation_response_table_row_053_callback:
	.word check_opponent_lp_at_most_500_or_self_above_1500+1                                        @ 09e4913c b57f0b08
field_spell_activation_response_table_row_054_cid:
	.word 0x00001469                                                           @ 09e49140 69140000
field_spell_activation_response_table_row_054_callback:
	.word check_equip_eligible_with_pair_slot_and_chain_gate+1                 @ 09e49144 657f0b08
field_spell_activation_response_table_row_055_cid:
	.word 0x000012e0                                                           @ 09e49148 e0120000
field_spell_activation_response_table_row_055_callback:
	.word check_pair_limit_and_opponent_state10_present+1                            @ 09e4914c 39810b08
field_spell_activation_response_table_row_056_cid:
	.word 0x00001401                                                           @ 09e49150 01140000
field_spell_activation_response_table_row_056_callback:
	.word check_infinite_cards_count_above_five+1                            @ 09e49154 05800b08
field_spell_activation_response_table_row_057_cid:
	.word 0x00001627                                                           @ 09e49158 27160000
field_spell_activation_response_table_row_057_callback:
	.word check_mass_driver_response_eligible+1                            @ 09e4915c 91800b08
field_spell_activation_response_table_row_058_cid:
	.word 0x000013ff                                                           @ 09e49160 ff130000
field_spell_activation_response_table_row_058_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e49164 e5760b08
field_spell_activation_response_table_row_059_cid:
	.word 0x000013f0                                                           @ 09e49168 f0130000
field_spell_activation_response_table_row_059_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e4916c a9760b08
field_spell_activation_response_table_row_060_cid:
	.word 0x00001738                                                           @ 09e49170 38170000
field_spell_activation_response_table_row_060_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e49174 e5760b08
field_spell_activation_response_table_row_061_cid:
	.word 0x00001628                                                           @ 09e49178 28160000
field_spell_activation_response_table_row_061_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4917c e5760b08
field_spell_activation_response_table_row_062_cid:
	.word 0x000017a6                                                           @ 09e49180 a6170000
field_spell_activation_response_table_row_062_callback:
	.word check_level_limit_area_b_response_eligible+1                            @ 09e49184 3d9b0b08
field_spell_activation_response_table_row_063_cid:
	.word 0x000016cd                                                           @ 09e49188 cd160000
field_spell_activation_response_table_row_063_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4918c e5760b08
field_spell_activation_response_table_row_064_cid:
	.word 0x000014a1                                                           @ 09e49190 a1140000
field_spell_activation_response_table_row_064_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e49194 e5760b08
field_spell_activation_response_table_row_065_cid:
	.word 0x000015a0                                                           @ 09e49198 a0150000
field_spell_activation_response_table_row_065_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e4919c e5760b08
field_spell_activation_response_table_row_066_cid:
	.word 0x000017f8                                                           @ 09e491a0 f8170000
field_spell_activation_response_table_row_066_callback:
	.word check_card_pair_slot_count_below_requirement+1                       @ 09e491a4 e5760b08
field_spell_activation_response_table_row_067_cid:
	.word 0x00001539                                                           @ 09e491a8 39150000
field_spell_activation_response_table_row_067_callback:
	.word check_mirage_of_nightmare_zone_count_eligible+1                            @ 09e491ac 75800b08
field_spell_activation_response_table_row_068_cid:
	.word 0x0000150e                                                           @ 09e491b0 0e150000
field_spell_activation_response_table_row_068_callback:
	.word check_spiritual_energy_settle_zone_count_eligible+1                            @ 09e491b4 3d800b08
field_spell_activation_response_table_row_069_cid:
	.word 0x0000132c                                                           @ 09e491b8 2c130000
field_spell_activation_response_table_row_069_callback:
	.word return_true_response_callback+1                                      @ 09e491bc a5760b08
