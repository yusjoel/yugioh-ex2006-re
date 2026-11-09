@ Yu-Gi-Oh! Ultimate Masters: WCT 2006
@ Normal-summon response callback tables (file 14 Seg-9).
@ Every callback word stores a THUMB entry address (function + 1).

@ Future callback entry aliases; their code remains outside Seg-9.

normal_summon_response_primary_table:
normal_summon_response_primary_row_000_cid:
	.word 0x000016a7                                                           @ 09e478d0 a7160000
normal_summon_response_primary_row_000_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e478d4 ed2e0b08
normal_summon_response_primary_row_001_cid:
	.word 0x000012e2                                                           @ 09e478d8 e2120000
normal_summon_response_primary_row_001_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e478dc ed2e0b08
normal_summon_response_primary_row_002_cid:
	.word 0x0000140a                                                           @ 09e478e0 0a140000
normal_summon_response_primary_row_002_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e478e4 ed2e0b08
normal_summon_response_primary_row_003_cid:
	.word 0x0000146b                                                           @ 09e478e8 6b140000
normal_summon_response_primary_row_003_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e478ec ed2e0b08
normal_summon_response_primary_row_004_cid:
	.word 0x00001316                                                           @ 09e478f0 16130000
normal_summon_response_primary_row_004_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e478f4 ed2e0b08
normal_summon_response_primary_row_005_cid:
	.word 0x00001805                                                           @ 09e478f8 05180000
normal_summon_response_primary_row_005_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e478fc ed2e0b08
normal_summon_response_primary_row_006_cid:
	.word 0x00001907                                                           @ 09e47900 07190000
normal_summon_response_primary_row_006_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47904 ed2e0b08
normal_summon_response_primary_row_007_cid:
	.word 0x000019ec                                                           @ 09e47908 ec190000
normal_summon_response_primary_row_007_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4790c ed2e0b08
normal_summon_response_primary_row_008_cid:
	.word 0x00001317                                                           @ 09e47910 17130000
normal_summon_response_primary_row_008_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47914 ed2e0b08
normal_summon_response_primary_row_009_cid:
	.word 0x000016e2                                                           @ 09e47918 e2160000
normal_summon_response_primary_row_009_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4791c ed2e0b08
normal_summon_response_primary_row_010_cid:
	.word 0x00001254                                                           @ 09e47920 54120000
normal_summon_response_primary_row_010_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47924 ed2e0b08
normal_summon_response_primary_row_011_cid:
	.word 0x000017b5                                                           @ 09e47928 b5170000
normal_summon_response_primary_row_011_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4792c ed2e0b08
normal_summon_response_primary_row_012_cid:
	.word 0x000013f9                                                           @ 09e47930 f9130000
normal_summon_response_primary_row_012_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47934 ed2e0b08
normal_summon_response_primary_row_013_cid:
	.word 0x00001381                                                           @ 09e47938 81130000
normal_summon_response_primary_row_013_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4793c ed2e0b08
normal_summon_response_primary_row_014_cid:
	.word 0x000012c4                                                           @ 09e47940 c4120000
normal_summon_response_primary_row_014_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47944 ed2e0b08
normal_summon_response_primary_row_015_cid:
	.word 0x00001404                                                           @ 09e47948 04140000
normal_summon_response_primary_row_015_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4794c ed2e0b08
normal_summon_response_primary_row_016_cid:
	.word 0x0000176a                                                           @ 09e47950 6a170000
normal_summon_response_primary_row_016_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47954 ed2e0b08
normal_summon_response_primary_row_017_cid:
	.word 0x00001380                                                           @ 09e47958 80130000
normal_summon_response_primary_row_017_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4795c ed2e0b08
normal_summon_response_primary_row_018_cid:
	.word 0x000014b2                                                           @ 09e47960 b2140000
normal_summon_response_primary_row_018_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47964 ed2e0b08
normal_summon_response_primary_row_019_cid:
	.word 0x00001243                                                           @ 09e47968 43120000
normal_summon_response_primary_row_019_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4796c ed2e0b08
normal_summon_response_primary_row_020_cid:
	.word 0x00001103                                                           @ 09e47970 03110000
normal_summon_response_primary_row_020_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47974 ed2e0b08
normal_summon_response_primary_row_021_cid:
	.word 0x0000140e                                                           @ 09e47978 0e140000
normal_summon_response_primary_row_021_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4797c ed2e0b08
normal_summon_response_primary_row_022_cid:
	.word 0x00001766                                                           @ 09e47980 66170000
normal_summon_response_primary_row_022_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47984 ed2e0b08
normal_summon_response_primary_row_023_cid:
	.word 0x000012d2                                                           @ 09e47988 d2120000
normal_summon_response_primary_row_023_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4798c ed2e0b08
normal_summon_response_primary_row_024_cid:
	.word 0x000017b7                                                           @ 09e47990 b7170000
normal_summon_response_primary_row_024_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47994 ed2e0b08
normal_summon_response_primary_row_025_cid:
	.word 0x0000137d                                                           @ 09e47998 7d130000
normal_summon_response_primary_row_025_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e4799c ed2e0b08
normal_summon_response_primary_row_026_cid:
	.word 0x000016a4                                                           @ 09e479a0 a4160000
normal_summon_response_primary_row_026_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479a4 ed2e0b08
normal_summon_response_primary_row_027_cid:
	.word 0x00001362                                                           @ 09e479a8 62130000
normal_summon_response_primary_row_027_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479ac ed2e0b08
normal_summon_response_primary_row_028_cid:
	.word 0x00001231                                                           @ 09e479b0 31120000
normal_summon_response_primary_row_028_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479b4 ed2e0b08
normal_summon_response_primary_row_029_cid:
	.word 0x0000153f                                                           @ 09e479b8 3f150000
normal_summon_response_primary_row_029_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479bc ed2e0b08
normal_summon_response_primary_row_030_cid:
	.word 0x00001402                                                           @ 09e479c0 02140000
normal_summon_response_primary_row_030_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479c4 ed2e0b08
normal_summon_response_primary_row_031_cid:
	.word 0x00001561                                                           @ 09e479c8 61150000
normal_summon_response_primary_row_031_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479cc ed2e0b08
normal_summon_response_primary_row_032_cid:
	.word 0x00001852                                                           @ 09e479d0 52180000
normal_summon_response_primary_row_032_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479d4 ed2e0b08
normal_summon_response_primary_row_033_cid:
	.word 0x000013fe                                                           @ 09e479d8 fe130000
normal_summon_response_primary_row_033_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479dc ed2e0b08
normal_summon_response_primary_row_034_cid:
	.word 0x00001538                                                           @ 09e479e0 38150000
normal_summon_response_primary_row_034_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479e4 ed2e0b08
normal_summon_response_primary_row_035_cid:
	.word 0x0000171a                                                           @ 09e479e8 1a170000
normal_summon_response_primary_row_035_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479ec ed2e0b08
normal_summon_response_primary_row_036_cid:
	.word 0x00001420                                                           @ 09e479f0 20140000
normal_summon_response_primary_row_036_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479f4 ed2e0b08
normal_summon_response_primary_row_037_cid:
	.word 0x000017b3                                                           @ 09e479f8 b3170000
normal_summon_response_primary_row_037_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e479fc ed2e0b08
normal_summon_response_primary_row_038_cid:
	.word 0x000019b5                                                           @ 09e47a00 b5190000
normal_summon_response_primary_row_038_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a04 ed2e0b08
normal_summon_response_primary_row_039_cid:
	.word 0x0000195f                                                           @ 09e47a08 5f190000
normal_summon_response_primary_row_039_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a0c ed2e0b08
normal_summon_response_primary_row_040_cid:
	.word 0x00001669                                                           @ 09e47a10 69160000
normal_summon_response_primary_row_040_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a14 ed2e0b08
normal_summon_response_primary_row_041_cid:
	.word 0x00001980                                                           @ 09e47a18 80190000
normal_summon_response_primary_row_041_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a1c ed2e0b08
normal_summon_response_primary_row_042_cid:
	.word 0x00001575                                                           @ 09e47a20 75150000
normal_summon_response_primary_row_042_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a24 ed2e0b08
normal_summon_response_primary_row_043_cid:
	.word 0x00001930                                                           @ 09e47a28 30190000
normal_summon_response_primary_row_043_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a2c ed2e0b08
normal_summon_response_primary_row_044_cid:
	.word 0x0000171e                                                           @ 09e47a30 1e170000
normal_summon_response_primary_row_044_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a34 ed2e0b08
normal_summon_response_primary_row_045_cid:
	.word 0x000017fe                                                           @ 09e47a38 fe170000
normal_summon_response_primary_row_045_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a3c ed2e0b08
normal_summon_response_primary_row_046_cid:
	.word 0x00001636                                                           @ 09e47a40 36160000
normal_summon_response_primary_row_046_callback:
	.word dispatch_reactive_summon_response_eligibility_by_card_id+1           @ 09e47a44 ed2e0b08
normal_summon_response_primary_row_047_cid:
	.word 0x000012cf                                                           @ 09e47a48 cf120000
normal_summon_response_primary_row_047_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a4c 8d390b08
normal_summon_response_primary_row_048_cid:
	.word 0x000012d0                                                           @ 09e47a50 d0120000
normal_summon_response_primary_row_048_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a54 8d390b08
normal_summon_response_primary_row_049_cid:
	.word 0x000012f1                                                           @ 09e47a58 f1120000
normal_summon_response_primary_row_049_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a5c 8d390b08
normal_summon_response_primary_row_050_cid:
	.word 0x00001329                                                           @ 09e47a60 29130000
normal_summon_response_primary_row_050_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a64 8d390b08
normal_summon_response_primary_row_051_cid:
	.word 0x000013ee                                                           @ 09e47a68 ee130000
normal_summon_response_primary_row_051_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a6c 8d390b08
normal_summon_response_primary_row_052_cid:
	.word 0x000012f2                                                           @ 09e47a70 f2120000
normal_summon_response_primary_row_052_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a74 8d390b08
normal_summon_response_primary_row_053_cid:
	.word 0x0000132a                                                           @ 09e47a78 2a130000
normal_summon_response_primary_row_053_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a7c 8d390b08
normal_summon_response_primary_row_054_cid:
	.word 0x00001330                                                           @ 09e47a80 30130000
normal_summon_response_primary_row_054_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a84 8d390b08
normal_summon_response_primary_row_055_cid:
	.word 0x00001492                                                           @ 09e47a88 92140000
normal_summon_response_primary_row_055_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a8c 8d390b08
normal_summon_response_primary_row_056_cid:
	.word 0x000014eb                                                           @ 09e47a90 eb140000
normal_summon_response_primary_row_056_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a94 8d390b08
normal_summon_response_primary_row_057_cid:
	.word 0x00001882                                                           @ 09e47a98 82180000
normal_summon_response_primary_row_057_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47a9c 8d390b08
normal_summon_response_primary_row_058_cid:
	.word 0x000014be                                                           @ 09e47aa0 be140000
normal_summon_response_primary_row_058_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47aa4 8d390b08
normal_summon_response_primary_row_059_cid:
	.word 0x00001514                                                           @ 09e47aa8 14150000
normal_summon_response_primary_row_059_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47aac 8d390b08
normal_summon_response_primary_row_060_cid:
	.word 0x0000192d                                                           @ 09e47ab0 2d190000
normal_summon_response_primary_row_060_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47ab4 8d390b08
normal_summon_response_primary_row_061_cid:
	.word 0x0000167b                                                           @ 09e47ab8 7b160000
normal_summon_response_primary_row_061_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47abc 8d390b08
normal_summon_response_primary_row_062_cid:
	.word 0x000016e3                                                           @ 09e47ac0 e3160000
normal_summon_response_primary_row_062_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47ac4 8d390b08
normal_summon_response_primary_row_063_cid:
	.word 0x0000153d                                                           @ 09e47ac8 3d150000
normal_summon_response_primary_row_063_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47acc 8d390b08
normal_summon_response_primary_row_064_cid:
	.word 0x00001763                                                           @ 09e47ad0 63170000
normal_summon_response_primary_row_064_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47ad4 8d390b08
normal_summon_response_primary_row_065_cid:
	.word 0x00001853                                                           @ 09e47ad8 53180000
normal_summon_response_primary_row_065_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47adc 8d390b08
normal_summon_response_primary_row_066_cid:
	.word 0x00001409                                                           @ 09e47ae0 09140000
normal_summon_response_primary_row_066_callback:
	.word dispatch_stat_modifier_summon_response_eligibility_by_card_id+1      @ 09e47ae4 8d390b08
normal_summon_response_primary_row_067_cid:
	.word 0x00001119                                                           @ 09e47ae8 19110000
normal_summon_response_primary_row_067_callback:
	.word check_gate_guardian_component_summon_response_eligible+1             @ 09e47aec 01190b08
normal_summon_response_primary_row_068_cid:
	.word 0x0000111a                                                           @ 09e47af0 1a110000
normal_summon_response_primary_row_068_callback:
	.word check_gate_guardian_component_summon_response_eligible+1             @ 09e47af4 01190b08
normal_summon_response_primary_row_069_cid:
	.word 0x0000111b                                                           @ 09e47af8 1b110000
normal_summon_response_primary_row_069_callback:
	.word check_gate_guardian_component_summon_response_eligible+1             @ 09e47afc 01190b08
normal_summon_response_primary_row_070_cid:
	.word 0x000013a7                                                           @ 09e47b00 a7130000
normal_summon_response_primary_row_070_callback:
	.word check_injection_fairy_lily_summon_response_eligible+1                @ 09e47b04 3d190b08
normal_summon_response_primary_row_071_cid:
	.word 0x00000fe0                                                           @ 09e47b08 e00f0000
normal_summon_response_primary_row_071_callback:
	.word check_kuriboh_summon_response_eligible+1                             @ 09e47b0c 99190b08
normal_summon_response_primary_row_072_cid:
	.word 0x00001906                                                           @ 09e47b10 06190000
normal_summon_response_primary_row_072_callback:
	.word return_true_response_callback+1                            @ 09e47b14 a5760b08
normal_summon_response_primary_row_073_cid:
	.word 0x000015f3                                                           @ 09e47b18 f3150000
normal_summon_response_primary_row_073_callback:
	.word return_true_response_callback+1                            @ 09e47b1c a5760b08
normal_summon_response_primary_row_074_cid:
	.word 0x0000124f                                                           @ 09e47b20 4f120000
normal_summon_response_primary_row_074_callback:
	.word return_true_response_callback+1                            @ 09e47b24 a5760b08
normal_summon_response_primary_row_075_cid:
	.word 0x00001250                                                           @ 09e47b28 50120000
normal_summon_response_primary_row_075_callback:
	.word return_true_response_callback+1                            @ 09e47b2c a5760b08
normal_summon_response_primary_row_076_cid:
	.word 0x000012e4                                                           @ 09e47b30 e4120000
normal_summon_response_primary_row_076_callback:
	.word return_true_response_callback+1                            @ 09e47b34 a5760b08
normal_summon_response_primary_row_077_cid:
	.word 0x000012d7                                                           @ 09e47b38 d7120000
normal_summon_response_primary_row_077_callback:
	.word return_true_response_callback+1                            @ 09e47b3c a5760b08
normal_summon_response_primary_row_078_cid:
	.word 0x0000168f                                                           @ 09e47b40 8f160000
normal_summon_response_primary_row_078_callback:
	.word return_true_response_callback+1                            @ 09e47b44 a5760b08
normal_summon_response_primary_row_079_cid:
	.word 0x000015f8                                                           @ 09e47b48 f8150000
normal_summon_response_primary_row_079_callback:
	.word check_adhesion_trap_hole_summon_response_eligible+1                  @ 09e47b4c c92a0b08
normal_summon_response_primary_row_080_cid:
	.word 0x00001352                                                           @ 09e47b50 52130000
normal_summon_response_primary_row_080_callback:
	.word return_true_response_callback+1                            @ 09e47b54 a5760b08
normal_summon_response_primary_row_081_cid:
	.word 0x0000135a                                                           @ 09e47b58 5a130000
normal_summon_response_primary_row_081_callback:
	.word return_true_response_callback+1                            @ 09e47b5c a5760b08
normal_summon_response_primary_row_082_cid:
	.word 0x00001353                                                           @ 09e47b60 53130000
normal_summon_response_primary_row_082_callback:
	.word return_true_response_callback+1                            @ 09e47b64 a5760b08
normal_summon_response_primary_row_083_cid:
	.word 0x00001354                                                           @ 09e47b68 54130000
normal_summon_response_primary_row_083_callback:
	.word return_true_response_callback+1                            @ 09e47b6c a5760b08
normal_summon_response_primary_row_084_cid:
	.word 0x0000140f                                                           @ 09e47b70 0f140000
normal_summon_response_primary_row_084_callback:
	.word return_true_response_callback+1                            @ 09e47b74 a5760b08
normal_summon_response_primary_row_085_cid:
	.word 0x000015b5                                                           @ 09e47b78 b5150000
normal_summon_response_primary_row_085_callback:
	.word return_true_response_callback+1                            @ 09e47b7c a5760b08
normal_summon_response_primary_row_086_cid:
	.word 0x000014d7                                                           @ 09e47b80 d7140000
normal_summon_response_primary_row_086_callback:
	.word return_true_response_callback+1                            @ 09e47b84 a5760b08
normal_summon_response_primary_row_087_cid:
	.word 0x0000195d                                                           @ 09e47b88 5d190000
normal_summon_response_primary_row_087_callback:
	.word return_true_response_callback+1                            @ 09e47b8c a5760b08
normal_summon_response_primary_row_088_cid:
	.word 0x00001572                                                           @ 09e47b90 72150000
normal_summon_response_primary_row_088_callback:
	.word return_true_response_callback+1                            @ 09e47b94 a5760b08
normal_summon_response_primary_row_089_cid:
	.word 0x00001493                                                           @ 09e47b98 93140000
normal_summon_response_primary_row_089_callback:
	.word return_true_response_callback+1                            @ 09e47b9c a5760b08
normal_summon_response_primary_row_090_cid:
	.word 0x00001883                                                           @ 09e47ba0 83180000
normal_summon_response_primary_row_090_callback:
	.word return_true_response_callback+1                            @ 09e47ba4 a5760b08
normal_summon_response_primary_row_091_cid:
	.word 0x0000198b                                                           @ 09e47ba8 8b190000
normal_summon_response_primary_row_091_callback:
	.word return_true_response_callback+1                            @ 09e47bac a5760b08
normal_summon_response_primary_row_092_cid:
	.word 0x0000151b                                                           @ 09e47bb0 1b150000
normal_summon_response_primary_row_092_callback:
	.word return_true_response_callback+1                            @ 09e47bb4 a5760b08
normal_summon_response_primary_row_093_cid:
	.word 0x0000151c                                                           @ 09e47bb8 1c150000
normal_summon_response_primary_row_093_callback:
	.word return_true_response_callback+1                            @ 09e47bbc a5760b08
normal_summon_response_primary_row_094_cid:
	.word 0x0000134c                                                           @ 09e47bc0 4c130000
normal_summon_response_primary_row_094_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e47bc4 a9760b08
normal_summon_response_primary_row_095_cid:
	.word 0x0000134d                                                           @ 09e47bc8 4d130000
normal_summon_response_primary_row_095_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e47bcc a9760b08
normal_summon_response_primary_row_096_cid:
	.word 0x0000134b                                                           @ 09e47bd0 4b130000
normal_summon_response_primary_row_096_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e47bd4 a9760b08
normal_summon_response_primary_row_097_cid:
	.word 0x000018d8                                                           @ 09e47bd8 d8180000
normal_summon_response_primary_row_097_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e47bdc 61770b08
normal_summon_response_primary_row_098_cid:
	.word 0x000014a7                                                           @ 09e47be0 a7140000
normal_summon_response_primary_row_098_callback:
	.word check_rope_of_life_summon_response_eligible+1                        @ 09e47be4 251b0b08
normal_summon_response_primary_row_099_cid:
	.word 0x000012ba                                                           @ 09e47be8 ba120000
normal_summon_response_primary_row_099_callback:
	.word check_time_machine_summon_response_eligible+1                        @ 09e47bec 751a0b08
normal_summon_response_primary_row_100_cid:
	.word 0x0000138f                                                           @ 09e47bf0 8f130000
normal_summon_response_primary_row_100_callback:
	.word check_sebeks_blessing_summon_response_eligible+1                     @ 09e47bf4 251d0b08
normal_summon_response_primary_row_101_cid:
	.word 0x000012cd                                                           @ 09e47bf8 cd120000
normal_summon_response_primary_row_101_callback:
	.word check_chain_destruction_summon_response_eligible+1                   @ 09e47bfc 6d220b08
normal_summon_response_primary_row_102_cid:
	.word 0x000016e0                                                           @ 09e47c00 e0160000
normal_summon_response_primary_row_102_callback:
	.word check_summon_removal_trap_response_eligible+1                        @ 09e47c04 5d230b08
normal_summon_response_primary_row_103_cid:
	.word 0x00001518                                                           @ 09e47c08 18150000
normal_summon_response_primary_row_103_callback:
	.word check_summon_removal_trap_response_eligible+1                        @ 09e47c0c 5d230b08
normal_summon_response_primary_row_104_cid:
	.word 0x000013fa                                                           @ 09e47c10 fa130000
normal_summon_response_primary_row_104_callback:
	.word check_torrential_tribute_summon_response_eligible+1                  @ 09e47c14 b5230b08
normal_summon_response_primary_row_105_cid:
	.word 0x000015ad                                                           @ 09e47c18 ad150000
normal_summon_response_primary_row_105_callback:
	.word check_non_aggression_area_summon_response_eligible+1                 @ 09e47c1c fd2a0b08
normal_summon_response_primary_row_106_cid:
	.word 0x0000132d                                                           @ 09e47c20 2d130000
normal_summon_response_primary_row_106_callback:
	.word check_mystical_space_typhoon_summon_response_eligible+1              @ 09e47c24 191e0b08
normal_summon_response_primary_row_107_cid:
	.word 0x0000137c                                                           @ 09e47c28 7c130000
normal_summon_response_primary_row_107_callback:
	.word check_dust_tornado_mind_haxorz_summon_response_eligible+1            @ 09e47c2c 811e0b08
normal_summon_response_primary_row_108_cid:
	.word 0x000018dc                                                           @ 09e47c30 dc180000
normal_summon_response_primary_row_108_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e47c34 a9760b08
normal_summon_response_primary_row_109_cid:
	.word 0x00001665                                                           @ 09e47c38 65160000
normal_summon_response_primary_row_109_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e47c3c a9760b08
normal_summon_response_primary_row_110_cid:
	.word 0x000015f0                                                           @ 09e47c40 f0150000
normal_summon_response_primary_row_110_callback:
	.word check_thunder_of_ruler_summon_response_eligible+1                    @ 09e47c44 992a0b08
normal_summon_response_primary_row_111_cid:
	.word 0x000012f3                                                           @ 09e47c48 f3120000
normal_summon_response_primary_row_111_callback:
	.word check_ultimate_offering_summon_response_eligible+1                   @ 09e47c4c 81240b08
normal_summon_response_primary_row_112_cid:
	.word 0x0000131e                                                           @ 09e47c50 1e130000
normal_summon_response_primary_row_112_callback:
	.word check_player_monster_zone_empty_summon_response_eligible+1           @ 09e47c54 d5250b08
normal_summon_response_primary_row_113_cid:
	.word 0x0000137e                                                           @ 09e47c58 7e130000
normal_summon_response_primary_row_113_callback:
	.word check_solomons_lawbook_summon_response_eligible+1                    @ 09e47c5c f1250b08
normal_summon_response_primary_row_114_cid:
	.word 0x000017fc                                                           @ 09e47c60 fc170000
normal_summon_response_primary_row_114_callback:
	.word check_taunt_summon_response_eligible+1                               @ 09e47c64 812b0b08
normal_summon_response_primary_row_115_cid:
	.word 0x00001973                                                           @ 09e47c68 73190000
normal_summon_response_primary_row_115_callback:
	.word check_gateway_zoma_summon_response_eligible+1                        @ 09e47c6c 392d0b08
normal_summon_response_primary_row_116_cid:
	.word 0x0000172f                                                           @ 09e47c70 2f170000
normal_summon_response_primary_row_116_callback:
	.word check_gateway_zoma_summon_response_eligible+1                        @ 09e47c74 392d0b08
normal_summon_response_primary_row_117_cid:
	.word 0x0000171b                                                           @ 09e47c78 1b170000
normal_summon_response_primary_row_117_callback:
	.word check_a_hero_emerges_summon_response_eligible+1                      @ 09e47c7c 452b0b08
normal_summon_response_primary_row_118_cid:
	.word 0x000018d4                                                           @ 09e47c80 d4180000
normal_summon_response_primary_row_118_callback:
	.word check_effect_handler_result_positive+1                                @ 09e47c84 1d770b08
normal_summon_response_primary_row_119_cid:
	.word 0x000019b6                                                           @ 09e47c88 b6190000
normal_summon_response_primary_row_119_callback:
	.word check_effect_handler_result_positive+1                                @ 09e47c8c 1d770b08
normal_summon_response_primary_row_120_cid:
	.word 0x0000198e                                                           @ 09e47c90 8e190000
normal_summon_response_primary_row_120_callback:
	.word check_inferno_reckless_summon_response_eligible+1                    @ 09e47c94 b12e0b08
normal_summon_response_primary_row_121_cid:
	.word 0x00001886                                                           @ 09e47c98 86180000
normal_summon_response_primary_row_121_callback:
	.word check_threatening_roar_summon_response_eligible+1                    @ 09e47c9c 992d0b08
normal_summon_response_primary_row_122_cid:
	.word 0x000019e0                                                           @ 09e47ca0 e0190000
normal_summon_response_primary_row_122_callback:
	.word check_option_hunter_summon_response_eligible+1                       @ 09e47ca4 652e0b08
normal_summon_response_primary_row_123_cid:
	.word 0x0000195e                                                           @ 09e47ca8 5e190000
normal_summon_response_primary_row_123_callback:
	.word check_chthonian_blast_summon_response_eligible+1                     @ 09e47cac cd2d0b08
normal_summon_response_primary_row_124_cid:
	.word 0x000014d3                                                           @ 09e47cb0 d3140000
normal_summon_response_primary_row_124_callback:
	.word check_position_change_summon_response_eligible+1                     @ 09e47cb4 f9280b08
normal_summon_response_primary_row_125_cid:
	.word 0x00001538                                                           @ 09e47cb8 38150000
normal_summon_response_primary_row_125_callback:
	.word check_position_change_summon_response_eligible+1                     @ 09e47cbc f9280b08
normal_summon_response_primary_row_126_cid:
	.word 0x000014f0                                                           @ 09e47cc0 f0140000
normal_summon_response_primary_row_126_callback:
	.word check_reversal_of_graves_summon_response_eligible+1                  @ 09e47cc4 e5270b08
normal_summon_response_primary_row_127_cid:
	.word 0x00001472                                                           @ 09e47cc8 72140000
normal_summon_response_primary_row_127_callback:
	.word return_true_response_callback+1                            @ 09e47ccc a5760b08
normal_summon_response_primary_row_128_cid:
	.word 0x00001809                                                           @ 09e47cd0 09180000
normal_summon_response_primary_row_128_callback:
	.word return_true_response_callback+1                            @ 09e47cd4 a5760b08
normal_summon_response_primary_row_129_cid:
	.word 0x0000130c                                                           @ 09e47cd8 0c130000
normal_summon_response_primary_row_129_callback:
	.word return_true_response_callback+1                            @ 09e47cdc a5760b08
normal_summon_response_primary_row_130_cid:
	.word 0x00001720                                                           @ 09e47ce0 20170000
normal_summon_response_primary_row_130_callback:
	.word return_true_response_callback+1                            @ 09e47ce4 a5760b08
normal_summon_response_primary_row_131_cid:
	.word 0x00001359                                                           @ 09e47ce8 59130000
normal_summon_response_primary_row_131_callback:
	.word return_true_response_callback+1                            @ 09e47cec a5760b08
normal_summon_response_primary_row_132_cid:
	.word 0x0000135d                                                           @ 09e47cf0 5d130000
normal_summon_response_primary_row_132_callback:
	.word return_true_response_callback+1                            @ 09e47cf4 a5760b08
normal_summon_response_primary_row_133_cid:
	.word 0x00001356                                                           @ 09e47cf8 56130000
normal_summon_response_primary_row_133_callback:
	.word return_true_response_callback+1                            @ 09e47cfc a5760b08
normal_summon_response_primary_row_134_cid:
	.word 0x000013f7                                                           @ 09e47d00 f7130000
normal_summon_response_primary_row_134_callback:
	.word return_true_response_callback+1                            @ 09e47d04 a5760b08
normal_summon_response_primary_row_135_cid:
	.word 0x00001468                                                           @ 09e47d08 68140000
normal_summon_response_primary_row_135_callback:
	.word return_true_response_callback+1                            @ 09e47d0c a5760b08
normal_summon_response_primary_row_136_cid:
	.word 0x000017af                                                           @ 09e47d10 af170000
normal_summon_response_primary_row_136_callback:
	.word return_true_response_callback+1                            @ 09e47d14 a5760b08
normal_summon_response_primary_row_137_cid:
	.word 0x00001405                                                           @ 09e47d18 05140000
normal_summon_response_primary_row_137_callback:
	.word return_true_response_callback+1                            @ 09e47d1c a5760b08
normal_summon_response_primary_row_138_cid:
	.word 0x0000135e                                                           @ 09e47d20 5e130000
normal_summon_response_primary_row_138_callback:
	.word return_true_response_callback+1                            @ 09e47d24 a5760b08
normal_summon_response_primary_row_139_cid:
	.word 0x00001361                                                           @ 09e47d28 61130000
normal_summon_response_primary_row_139_callback:
	.word return_true_response_callback+1                            @ 09e47d2c a5760b08
normal_summon_response_primary_row_140_cid:
	.word 0x0000123b                                                           @ 09e47d30 3b120000
normal_summon_response_primary_row_140_callback:
	.word return_true_response_callback+1                            @ 09e47d34 a5760b08
normal_summon_response_primary_row_141_cid:
	.word 0x0000188c                                                           @ 09e47d38 8c180000
normal_summon_response_primary_row_141_callback:
	.word return_true_response_callback+1                            @ 09e47d3c a5760b08
normal_summon_response_primary_row_142_cid:
	.word 0x00001306                                                           @ 09e47d40 06130000
normal_summon_response_primary_row_142_callback:
	.word return_true_response_callback+1                            @ 09e47d44 a5760b08
normal_summon_response_primary_row_143_cid:
	.word 0x00001355                                                           @ 09e47d48 55130000
normal_summon_response_primary_row_143_callback:
	.word return_true_response_callback+1                            @ 09e47d4c a5760b08
normal_summon_response_primary_row_144_cid:
	.word 0x000012c8                                                           @ 09e47d50 c8120000
normal_summon_response_primary_row_144_callback:
	.word return_true_response_callback+1                            @ 09e47d54 a5760b08
normal_summon_response_primary_row_145_cid:
	.word 0x00001357                                                           @ 09e47d58 57130000
normal_summon_response_primary_row_145_callback:
	.word return_true_response_callback+1                            @ 09e47d5c a5760b08
normal_summon_response_primary_row_146_cid:
	.word 0x00001545                                                           @ 09e47d60 45150000
normal_summon_response_primary_row_146_callback:
	.word return_true_response_callback+1                            @ 09e47d64 a5760b08
normal_summon_response_primary_row_147_cid:
	.word 0x000014a1                                                           @ 09e47d68 a1140000
normal_summon_response_primary_row_147_callback:
	.word return_true_response_callback+1                            @ 09e47d6c a5760b08
normal_summon_response_primary_row_148_cid:
	.word 0x000017b2                                                           @ 09e47d70 b2170000
normal_summon_response_primary_row_148_callback:
	.word return_true_response_callback+1                            @ 09e47d74 a5760b08
normal_summon_response_primary_row_149_cid:
	.word 0x000017b6                                                           @ 09e47d78 b6170000
normal_summon_response_primary_row_149_callback:
	.word return_true_response_callback+1                            @ 09e47d7c a5760b08
normal_summon_response_primary_row_150_cid:
	.word 0x00001256                                                           @ 09e47d80 56120000
normal_summon_response_primary_row_150_callback:
	.word return_true_response_callback+1                            @ 09e47d84 a5760b08
normal_summon_response_primary_row_151_cid:
	.word 0x0000171c                                                           @ 09e47d88 1c170000
normal_summon_response_primary_row_151_callback:
	.word return_true_response_callback+1                            @ 09e47d8c a5760b08
normal_summon_response_primary_row_152_cid:
	.word 0x00001630                                                           @ 09e47d90 30160000
normal_summon_response_primary_row_152_callback:
	.word return_true_response_callback+1                            @ 09e47d94 a5760b08
normal_summon_response_primary_row_153_cid:
	.word 0x000017f3                                                           @ 09e47d98 f3170000
normal_summon_response_primary_row_153_callback:
	.word return_true_response_callback+1                            @ 09e47d9c a5760b08
normal_summon_response_primary_row_154_cid:
	.word 0x000016a1                                                           @ 09e47da0 a1160000
normal_summon_response_primary_row_154_callback:
	.word return_true_response_callback+1                            @ 09e47da4 a5760b08
normal_summon_response_primary_row_155_cid:
	.word 0x00001762                                                           @ 09e47da8 62170000
normal_summon_response_primary_row_155_callback:
	.word return_true_response_callback+1                            @ 09e47dac a5760b08
normal_summon_response_primary_row_156_cid:
	.word 0x000017bf                                                           @ 09e47db0 bf170000
normal_summon_response_primary_row_156_callback:
	.word return_true_response_callback+1                            @ 09e47db4 a5760b08
normal_summon_response_primary_row_157_cid:
	.word 0x00001974                                                           @ 09e47db8 74190000
normal_summon_response_primary_row_157_callback:
	.word return_true_response_callback+1                            @ 09e47dbc a5760b08
normal_summon_response_primary_row_158_cid:
	.word 0x000014c0                                                           @ 09e47dc0 c0140000
normal_summon_response_primary_row_158_callback:
	.word return_true_response_callback+1                            @ 09e47dc4 a5760b08
normal_summon_response_primary_row_159_cid:
	.word 0x000017ca                                                           @ 09e47dc8 ca170000
normal_summon_response_primary_row_159_callback:
	.word return_true_response_callback+1                            @ 09e47dcc a5760b08
normal_summon_response_primary_row_160_cid:
	.word 0x0000192b                                                           @ 09e47dd0 2b190000
normal_summon_response_primary_row_160_callback:
	.word return_true_response_callback+1                            @ 09e47dd4 a5760b08
normal_summon_response_primary_row_161_cid:
	.word 0x000016df                                                           @ 09e47dd8 df160000
normal_summon_response_primary_row_161_callback:
	.word return_true_response_callback+1                            @ 09e47ddc a5760b08
normal_summon_response_primary_row_162_cid:
	.word 0x000016a8                                                           @ 09e47de0 a8160000
normal_summon_response_primary_row_162_callback:
	.word return_true_response_callback+1                            @ 09e47de4 a5760b08
normal_summon_response_primary_row_163_cid:
	.word 0x000016de                                                           @ 09e47de8 de160000
normal_summon_response_primary_row_163_callback:
	.word return_true_response_callback+1                            @ 09e47dec a5760b08
normal_summon_response_primary_row_164_cid:
	.word 0x00001390                                                           @ 09e47df0 90130000
normal_summon_response_primary_row_164_callback:
	.word return_true_response_callback+1                            @ 09e47df4 a5760b08
normal_summon_response_primary_row_165_cid:
	.word 0x000014bf                                                           @ 09e47df8 bf140000
normal_summon_response_primary_row_165_callback:
	.word return_true_response_callback+1                            @ 09e47dfc a5760b08
normal_summon_response_primary_row_166_cid:
	.word 0x00001631                                                           @ 09e47e00 31160000
normal_summon_response_primary_row_166_callback:
	.word return_true_response_callback+1                            @ 09e47e04 a5760b08
normal_summon_response_primary_row_167_cid:
	.word 0x0000166b                                                           @ 09e47e08 6b160000
normal_summon_response_primary_row_167_callback:
	.word return_true_response_callback+1                            @ 09e47e0c a5760b08
normal_summon_response_primary_row_168_cid:
	.word 0x000016dc                                                           @ 09e47e10 dc160000
normal_summon_response_primary_row_168_callback:
	.word return_true_response_callback+1                            @ 09e47e14 a5760b08
normal_summon_response_primary_row_169_cid:
	.word 0x00001801                                                           @ 09e47e18 01180000
normal_summon_response_primary_row_169_callback:
	.word return_true_response_callback+1                            @ 09e47e1c a5760b08
normal_summon_response_primary_row_170_cid:
	.word 0x00001976                                                           @ 09e47e20 76190000
normal_summon_response_primary_row_170_callback:
	.word return_true_response_callback+1                            @ 09e47e24 a5760b08
normal_summon_response_primary_row_171_cid:
	.word 0x00001926                                                           @ 09e47e28 26190000
normal_summon_response_primary_row_171_callback:
	.word return_true_response_callback+1                            @ 09e47e2c a5760b08
normal_summon_response_primary_row_172_cid:
	.word 0x0000192c                                                           @ 09e47e30 2c190000
normal_summon_response_primary_row_172_callback:
	.word return_true_response_callback+1                            @ 09e47e34 a5760b08
normal_summon_response_primary_row_173_cid:
	.word 0x000018d5                                                           @ 09e47e38 d5180000
normal_summon_response_primary_row_173_callback:
	.word return_true_response_callback+1                            @ 09e47e3c a5760b08
normal_summon_response_primary_row_174_cid:
	.word 0x00001800                                                           @ 09e47e40 00180000
normal_summon_response_primary_row_174_callback:
	.word return_true_response_callback+1                            @ 09e47e44 a5760b08
normal_summon_response_primary_row_175_cid:
	.word 0x000015fb                                                           @ 09e47e48 fb150000
normal_summon_response_primary_row_175_callback:
	.word return_true_response_callback+1                            @ 09e47e4c a5760b08
normal_summon_response_primary_row_176_cid:
	.word 0x000015ac                                                           @ 09e47e50 ac150000
normal_summon_response_primary_row_176_callback:
	.word return_true_response_callback+1                            @ 09e47e54 a5760b08
normal_summon_response_primary_row_177_cid:
	.word 0x00001546                                                           @ 09e47e58 46150000
normal_summon_response_primary_row_177_callback:
	.word return_true_response_callback+1                            @ 09e47e5c a5760b08
normal_summon_response_primary_row_178_cid:
	.word 0x00001519                                                           @ 09e47e60 19150000
normal_summon_response_primary_row_178_callback:
	.word return_true_response_callback+1                            @ 09e47e64 a5760b08
normal_summon_response_primary_row_179_cid:
	.word 0x000018da                                                           @ 09e47e68 da180000
normal_summon_response_primary_row_179_callback:
	.word check_effect_handler_result_positive+1                                @ 09e47e6c 1d770b08
normal_summon_response_primary_row_180_cid:
	.word 0x0000165a                                                           @ 09e47e70 5a160000
normal_summon_response_primary_row_180_callback:
	.word check_effect_handler_result_positive+1                                @ 09e47e74 1d770b08
normal_summon_response_primary_row_181_cid:
	.word 0x00001818                                                           @ 09e47e78 18180000
normal_summon_response_primary_row_181_callback:
	.word check_effect_handler_result_positive+1                                @ 09e47e7c 1d770b08
normal_summon_response_primary_row_182_cid:
	.word 0x00001979                                                           @ 09e47e80 79190000
normal_summon_response_primary_row_182_callback:
	.word check_effect_handler_result_positive+1                                @ 09e47e84 1d770b08
normal_summon_response_primary_row_183_cid:
	.word 0x00001253                                                           @ 09e47e88 53120000
normal_summon_response_primary_row_183_callback:
	.word check_opponent_effect_node_active+1                                  @ 09e47e8c a9760b08
normal_summon_response_primary_row_184_cid:
	.word 0x0000166d                                                           @ 09e47e90 6d160000
normal_summon_response_primary_row_184_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e47e94 61770b08
normal_summon_response_primary_row_185_cid:
	.word 0x00001633                                                           @ 09e47e98 33160000
normal_summon_response_primary_row_185_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e47e9c 61770b08
normal_summon_response_primary_row_186_cid:
	.word 0x00001977                                                           @ 09e47ea0 77190000
normal_summon_response_primary_row_186_callback:
	.word check_self_effect_node_inactive+1                                    @ 09e47ea4 61770b08
normal_summon_response_primary_row_187_cid:
	.word 0x00001678                                                           @ 09e47ea8 78160000
normal_summon_response_primary_row_187_callback:
	.word check_magical_dimension_summon_response_eligible+1                   @ 09e47eac 3d1c0b08
normal_summon_response_primary_row_188_cid:
	.word 0x0000151d                                                           @ 09e47eb0 1d150000
normal_summon_response_primary_row_188_callback:
	.word check_fiend_comedian_summon_response_eligible+1                      @ 09e47eb4 ad280b08
normal_summon_response_primary_row_189_cid:
	.word 0x0000166c                                                           @ 09e47eb8 6c160000
normal_summon_response_primary_row_189_callback:
	.word check_skill_drain_summon_response_eligible+1                         @ 09e47ebc f51b0b08
normal_summon_response_primary_row_190_cid:
	.word 0x00001378                                                           @ 09e47ec0 78130000
normal_summon_response_primary_row_190_callback:
	.word check_time_seal_summon_response_eligible+1                           @ 09e47ec4 35270b08
normal_summon_response_primary_row_191_cid:
	.word 0x000016a2                                                           @ 09e47ec8 a2160000
normal_summon_response_primary_row_191_callback:
	.word check_battle_scarred_summon_response_eligible+1                      @ 09e47ecc b91f0b08
normal_summon_response_primary_row_192_cid:
	.word 0x000013f2                                                           @ 09e47ed0 f2130000
normal_summon_response_primary_row_192_callback:
	.word check_mask_of_restrict_summon_response_eligible+1                    @ 09e47ed4 e1180b08
normal_summon_response_primary_row_193_cid:
	.word 0x0000148d                                                           @ 09e47ed8 8d140000
normal_summon_response_primary_row_193_callback:
	.word check_collected_power_summon_response_eligible+1                     @ 09e47edc d1190b08
normal_summon_response_primary_row_194_cid:
	.word 0x0000137f                                                           @ 09e47ee0 7f130000
normal_summon_response_primary_row_194_callback:
	.word check_opponent_distinct_field7_pair_summon_response_eligible+1       @ 09e47ee4 811c0b08
normal_summon_response_primary_row_195_cid:
	.word 0x00001358                                                           @ 09e47ee8 58130000
normal_summon_response_primary_row_195_callback:
	.word check_regulation_of_tribe_summon_response_eligible+1                 @ 09e47eec 751d0b08
normal_summon_response_primary_row_196_cid:
	.word 0x00001494                                                           @ 09e47ef0 94140000
normal_summon_response_primary_row_196_callback:
	.word check_blind_destruction_summon_response_eligible+1                   @ 09e47ef4 d51d0b08
normal_summon_response_primary_row_197_cid:
	.word 0x00001491                                                           @ 09e47ef8 91140000
normal_summon_response_primary_row_197_callback:
	.word check_graverobbers_retribution_summon_response_eligible+1            @ 09e47efc 051e0b08
normal_summon_response_primary_row_198_cid:
	.word 0x0000138d                                                           @ 09e47f00 8d130000
normal_summon_response_primary_row_198_callback:
	.word check_ring_of_destruction_summon_response_eligible+1                 @ 09e47f04 f11e0b08
normal_summon_response_primary_row_199_cid:
	.word 0x00001718                                                           @ 09e47f08 18170000
normal_summon_response_primary_row_199_callback:
	.word check_destruction_ring_summon_response_eligible+1                    @ 09e47f0c d51f0b08
normal_summon_response_primary_row_200_cid:
	.word 0x00001301                                                           @ 09e47f10 01130000
normal_summon_response_primary_row_200_callback:
	.word check_just_desserts_summon_response_eligible+1                       @ 09e47f14 29200b08
normal_summon_response_primary_row_201_cid:
	.word 0x0000137a                                                           @ 09e47f18 7a130000
normal_summon_response_primary_row_201_callback:
	.word check_gift_of_mystical_elf_summon_response_eligible+1                @ 09e47f1c 7d200b08
normal_summon_response_primary_row_202_cid:
	.word 0x00001804                                                           @ 09e47f20 04180000
normal_summon_response_primary_row_202_callback:
	.word check_field_count_burn_summon_response_eligible+1                    @ 09e47f24 b12b0b08
normal_summon_response_primary_row_203_cid:
	.word 0x000015f4                                                           @ 09e47f28 f4150000
normal_summon_response_primary_row_203_callback:
	.word check_field_count_burn_summon_response_eligible+1                    @ 09e47f2c b12b0b08
normal_summon_response_primary_row_204_cid:
	.word 0x00001767                                                           @ 09e47f30 67170000
normal_summon_response_primary_row_204_callback:
	.word check_field_count_burn_summon_response_eligible+1                    @ 09e47f34 b12b0b08
normal_summon_response_primary_row_205_cid:
	.word 0x0000135c                                                           @ 09e47f38 5c130000
normal_summon_response_primary_row_205_callback:
	.word check_reveal_effect_summon_response_eligible+1                       @ 09e47f3c d1200b08
normal_summon_response_primary_row_206_cid:
	.word 0x00001635                                                           @ 09e47f40 35160000
normal_summon_response_primary_row_206_callback:
	.word check_reveal_effect_summon_response_eligible+1                       @ 09e47f44 d1200b08
normal_summon_response_primary_row_207_cid:
	.word 0x0000138e                                                           @ 09e47f48 8e130000
normal_summon_response_primary_row_207_callback:
	.word check_aqua_chorus_summon_response_eligible+1                         @ 09e47f4c f9210b08
normal_summon_response_primary_row_208_cid:
	.word 0x000012e7                                                           @ 09e47f50 e7120000
normal_summon_response_primary_row_208_callback:
	.word check_two_pronged_attack_summon_response_eligible+1                  @ 09e47f54 d9230b08
normal_summon_response_primary_row_209_cid:
	.word 0x00001490                                                           @ 09e47f58 90140000
normal_summon_response_primary_row_209_callback:
	.word check_skull_lair_summon_response_eligible+1                          @ 09e47f5c 95260b08
normal_summon_response_primary_row_210_cid:
	.word 0x0000137b                                                           @ 09e47f60 7b130000
normal_summon_response_primary_row_210_callback:
	.word check_eye_of_truth_summon_response_eligible+1                        @ 09e47f64 b5200b08
normal_summon_response_primary_row_211_cid:
	.word 0x000015a8                                                           @ 09e47f68 a8150000
normal_summon_response_primary_row_211_callback:
	.word check_discard_removal_summon_response_eligible+1                     @ 09e47f6c 112a0b08
normal_summon_response_primary_row_212_cid:
	.word 0x000014e4                                                           @ 09e47f70 e4140000
normal_summon_response_primary_row_212_callback:
	.word check_burst_breath_summon_response_eligible+1                        @ 09e47f74 b5290b08
normal_summon_response_primary_row_213_cid:
	.word 0x00001887                                                           @ 09e47f78 87180000
normal_summon_response_primary_row_213_callback:
	.word check_discard_removal_summon_response_eligible+1                     @ 09e47f7c 112a0b08
normal_summon_response_primary_row_214_cid:
	.word 0x000019db                                                           @ 09e47f80 db190000
normal_summon_response_primary_row_214_callback:
	.word check_karma_cut_summon_response_eligible+1                           @ 09e47f84 552a0b08
normal_summon_response_primary_row_215_cid:
	.word 0x0000188a                                                           @ 09e47f88 8a180000
normal_summon_response_primary_row_215_callback:
	.word check_assault_on_ghq_summon_response_eligible+1                      @ 09e47f8c 712c0b08
normal_summon_response_primary_row_216_cid:
	.word 0x00001978                                                           @ 09e47f90 78190000
normal_summon_response_primary_row_216_callback:
	.word check_same_name_card_summon_response_eligible+1                      @ 09e47f94 e12c0b08
normal_summon_response_primary_row_217_cid:
	.word 0x000019dc                                                           @ 09e47f98 dc190000
normal_summon_response_primary_row_217_callback:
	.word check_same_name_card_summon_response_eligible+1                      @ 09e47f9c e12c0b08
normal_summon_response_primary_row_218_cid:
	.word 0x0000184d                                                           @ 09e47fa0 4d180000
normal_summon_response_primary_row_218_callback:
	.word check_dust_tornado_mind_haxorz_summon_response_eligible+1            @ 09e47fa4 811e0b08
normal_summon_response_primary_row_219_cid:
	.word 0x00001848                                                           @ 09e47fa8 48180000
normal_summon_response_primary_row_219_callback:
	.word check_spell_trap_cleanup_summon_response_eligible+1                  @ 09e47fac 112c0b08
normal_summon_response_primary_row_220_cid:
	.word 0x00001851                                                           @ 09e47fb0 51180000
normal_summon_response_primary_row_220_callback:
	.word check_spell_trap_cleanup_summon_response_eligible+1                  @ 09e47fb4 112c0b08
normal_summon_response_primary_row_221_cid:
	.word 0x0000184a                                                           @ 09e47fb8 4a180000
normal_summon_response_primary_row_221_callback:
	.word check_xing_zhen_hu_summon_response_eligible+1                        @ 09e47fbc 512c0b08
normal_summon_response_secondary_table:
normal_summon_response_secondary_row_000_cid:
	.word 0x000012f5                                                           @ 09e47fc0 f5120000
normal_summon_response_secondary_row_000_callback:
	.word return_true_response_callback+1                            @ 09e47fc4 a5760b08
normal_summon_response_secondary_row_001_cid:
	.word 0x000012f7                                                           @ 09e47fc8 f7120000
normal_summon_response_secondary_row_001_callback:
	.word return_true_response_callback+1                            @ 09e47fcc a5760b08
normal_summon_response_secondary_row_002_cid:
	.word 0x000012f6                                                           @ 09e47fd0 f6120000
normal_summon_response_secondary_row_002_callback:
	.word return_true_response_callback+1                            @ 09e47fd4 a5760b08
normal_summon_response_secondary_row_003_cid:
	.word 0x0000131c                                                           @ 09e47fd8 1c130000
normal_summon_response_secondary_row_003_callback:
	.word return_true_response_callback+1                            @ 09e47fdc a5760b08
normal_summon_response_secondary_row_004_cid:
	.word 0x00001258                                                           @ 09e47fe0 58120000
normal_summon_response_secondary_row_004_callback:
	.word return_true_response_callback+1                            @ 09e47fe4 a5760b08
normal_summon_response_secondary_row_005_cid:
	.word 0x000016db                                                           @ 09e47fe8 db160000
normal_summon_response_secondary_row_005_callback:
	.word return_true_response_callback+1                            @ 09e47fec a5760b08
normal_summon_response_secondary_row_006_cid:
	.word 0x000017c2                                                           @ 09e47ff0 c2170000
normal_summon_response_secondary_row_006_callback:
	.word check_cross_side_summon_response_eligible+1                          @ 09e47ff4 99400b08
normal_summon_response_secondary_row_007_cid:
	.word 0x000017d4                                                           @ 09e47ff8 d4170000
normal_summon_response_secondary_row_007_callback:
	.word check_cross_side_summon_response_eligible+1                          @ 09e47ffc 99400b08
normal_summon_response_secondary_row_008_cid:
	.word 0x000017c6                                                           @ 09e48000 c6170000
normal_summon_response_secondary_row_008_callback:
	.word check_cross_side_summon_response_eligible+1                          @ 09e48004 99400b08
normal_summon_response_secondary_row_009_cid:
	.word 0x000014b6                                                           @ 09e48008 b6140000
normal_summon_response_secondary_row_009_callback:
	.word check_cross_side_summon_response_eligible+1                          @ 09e4800c 99400b08
normal_summon_response_secondary_row_010_cid:
	.word 0x000014c7                                                           @ 09e48010 c7140000
normal_summon_response_secondary_row_010_callback:
	.word check_cross_side_summon_response_eligible+1                          @ 09e48014 99400b08
normal_summon_response_secondary_row_011_cid:
	.word 0x0000132d                                                           @ 09e48018 2d130000
normal_summon_response_secondary_row_011_callback:
	.word check_opposing_summon_response_slot_eligible+1                       @ 09e4801c 29470b08
normal_summon_response_secondary_row_012_cid:
	.word 0x0000137c                                                           @ 09e48020 7c130000
normal_summon_response_secondary_row_012_callback:
	.word check_opposing_summon_response_slot_eligible+1                       @ 09e48024 29470b08
normal_summon_response_secondary_row_013_cid:
	.word 0x00001379                                                           @ 09e48028 79130000
normal_summon_response_secondary_row_013_callback:
	.word check_graverobber_summon_response_eligible+1                         @ 09e4802c a93f0b08
normal_summon_response_secondary_row_014_cid:
	.word 0x00001515                                                           @ 09e48030 15150000
normal_summon_response_secondary_row_014_callback:
	.word check_disappear_summon_response_eligible+1                           @ 09e48034 31400b08
normal_summon_response_secondary_row_015_cid:
	.word 0x0000162a                                                           @ 09e48038 2a160000
normal_summon_response_secondary_row_015_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e4803c b9400b08
normal_summon_response_secondary_row_016_cid:
	.word 0x00001960                                                           @ 09e48040 60190000
normal_summon_response_secondary_row_016_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e48044 b9400b08
normal_summon_response_secondary_row_017_cid:
	.word 0x0000148f                                                           @ 09e48048 8f140000
normal_summon_response_secondary_row_017_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e4804c b9400b08
normal_summon_response_secondary_row_018_cid:
	.word 0x0000153e                                                           @ 09e48050 3e150000
normal_summon_response_secondary_row_018_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e48054 b9400b08
normal_summon_response_secondary_row_019_cid:
	.word 0x00001721                                                           @ 09e48058 21170000
normal_summon_response_secondary_row_019_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e4805c b9400b08
normal_summon_response_secondary_row_020_cid:
	.word 0x0000176b                                                           @ 09e48060 6b170000
normal_summon_response_secondary_row_020_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e48064 b9400b08
normal_summon_response_secondary_row_021_cid:
	.word 0x000018dd                                                           @ 09e48068 dd180000
normal_summon_response_secondary_row_021_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e4806c b9400b08
normal_summon_response_secondary_row_022_cid:
	.word 0x000018de                                                           @ 09e48070 de180000
normal_summon_response_secondary_row_022_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e48074 b9400b08
normal_summon_response_secondary_row_023_cid:
	.word 0x0000134f                                                           @ 09e48078 4f130000
normal_summon_response_secondary_row_023_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e4807c b9400b08
normal_summon_response_secondary_row_024_cid:
	.word 0x00001541                                                           @ 09e48080 41150000
normal_summon_response_secondary_row_024_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e48084 b9400b08
normal_summon_response_secondary_row_025_cid:
	.word 0x00001360                                                           @ 09e48088 60130000
normal_summon_response_secondary_row_025_callback:
	.word check_equip_slot_eligible_with_field6_0x16_cross_side+1              @ 09e4808c b5410b08
normal_summon_response_secondary_row_026_cid:
	.word 0x00001302                                                           @ 09e48090 02130000
normal_summon_response_secondary_row_026_callback:
	.word check_equip_slot_eligible_with_field6_0x17_cross_side+1              @ 09e48094 dd410b08
normal_summon_response_secondary_row_027_cid:
	.word 0x0000148c                                                           @ 09e48098 8c140000
normal_summon_response_secondary_row_027_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e4809c b9400b08
normal_summon_response_secondary_row_028_cid:
	.word 0x0000183a                                                           @ 09e480a0 3a180000
normal_summon_response_secondary_row_028_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e480a4 b9400b08
normal_summon_response_secondary_row_029_cid:
	.word 0x00001470                                                           @ 09e480a8 70140000
normal_summon_response_secondary_row_029_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e480ac b9400b08
normal_summon_response_secondary_row_030_cid:
	.word 0x000015fc                                                           @ 09e480b0 fc150000
normal_summon_response_secondary_row_030_callback:
	.word check_slot_card_is_equippable+1                                      @ 09e480b4 d9400b08
normal_summon_response_secondary_row_031_cid:
	.word 0x00001936                                                           @ 09e480b8 36190000
normal_summon_response_secondary_row_031_callback:
	.word check_slot_card_is_equippable+1                                      @ 09e480bc d9400b08
normal_summon_response_secondary_row_032_cid:
	.word 0x0000140d                                                           @ 09e480c0 0d140000
normal_summon_response_secondary_row_032_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e480c4 b9400b08
normal_summon_response_secondary_row_033_cid:
	.word 0x000012fe                                                           @ 09e480c8 fe120000
normal_summon_response_secondary_row_033_callback:
	.word check_slot_card_is_equippable+1                                      @ 09e480cc d9400b08
normal_summon_response_secondary_row_034_cid:
	.word 0x000012ff                                                           @ 09e480d0 ff120000
normal_summon_response_secondary_row_034_callback:
	.word check_slot_card_is_equippable+1                                      @ 09e480d4 d9400b08
normal_summon_response_secondary_row_035_cid:
	.word 0x000016a6                                                           @ 09e480d8 a6160000
normal_summon_response_secondary_row_035_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e480dc b9400b08
normal_summon_response_secondary_row_036_cid:
	.word 0x000016dd                                                           @ 09e480e0 dd160000
normal_summon_response_secondary_row_036_callback:
	.word check_slots_on_different_player_sides+1                              @ 09e480e4 b9400b08
normal_summon_response_secondary_row_037_cid:
	.word 0x000015f1                                                           @ 09e480e8 f1150000
normal_summon_response_secondary_row_037_callback:
	.word check_slot_card_is_equippable+1                                      @ 09e480ec d9400b08
normal_summon_response_secondary_row_038_cid:
	.word 0x000014de                                                           @ 09e480f0 de140000
normal_summon_response_secondary_row_038_callback:
	.word check_slot_card_is_equippable+1                                      @ 09e480f4 d9400b08
normal_summon_response_secondary_row_039_cid:
	.word 0x00001849                                                           @ 09e480f8 49180000
normal_summon_response_secondary_row_039_callback:
	.word check_effect_slot_cross_player_type_eligible+1                       @ 09e480fc 31490b08
normal_summon_response_secondary_row_040_cid:
	.word 0x000012fd                                                           @ 09e48100 fd120000
normal_summon_response_secondary_row_040_callback:
	.word check_slot_card_equippable_under_lp_threshold+1                      @ 09e48104 05420b08
normal_summon_response_secondary_row_041_cid:
	.word 0x000019e1                                                           @ 09e48108 e1190000
normal_summon_response_secondary_row_041_callback:
	.word check_slot_card_equippable_under_zone_state+1                        @ 09e4810c 41420b08
normal_summon_response_secondary_row_042_cid:
	.word 0x000019e2                                                           @ 09e48110 e2190000
normal_summon_response_secondary_row_042_callback:
	.word check_slot_card_equippable_under_zone_state+1                        @ 09e48114 41420b08
normal_summon_response_secondary_row_043_cid:
	.word 0x00001975                                                           @ 09e48118 75190000
normal_summon_response_secondary_row_043_callback:
	.word scan_player_zone_for_placement_allowed_card+1                        @ 09e4811c 81420b08
normal_summon_response_secondary_row_044_cid:
	.word 0x0000184b                                                           @ 09e48120 4b180000
normal_summon_response_secondary_row_044_callback:
	.word check_equip_slot_eligible_with_field6_0x16_and_effect_type+1         @ 09e48124 05430b08
normal_summon_response_secondary_row_045_cid:
	.word 0x000014d3                                                           @ 09e48128 d3140000
normal_summon_response_secondary_row_045_callback:
	.word check_cross_side_effect_slot_with_dual_handler+1                     @ 09e4812c 65440b08
normal_summon_response_secondary_row_046_cid:
	.word 0x00001538                                                           @ 09e48130 38150000
normal_summon_response_secondary_row_046_callback:
	.word check_cross_side_effect_slot_with_dual_handler+1                     @ 09e48134 65440b08
normal_summon_response_secondary_row_047_cid:
	.word 0x00001850                                                           @ 09e48138 50180000
normal_summon_response_secondary_row_047_callback:
	.word check_equip_lp_delta_sign_eligible+1                                 @ 09e4813c 71490b08
normal_summon_response_secondary_row_048_cid:
	.word 0x00001805                                                           @ 09e48140 05180000
normal_summon_response_secondary_row_048_callback:
	.word check_equip_lp_delta_sign_eligible+1                                 @ 09e48144 71490b08
normal_summon_response_secondary_row_049_cid:
	.word 0x000014e6                                                           @ 09e48148 e6140000
normal_summon_response_secondary_row_049_callback:
	.word check_effect_node_equip_target_eligible+1                            @ 09e4814c 79430b08
normal_summon_response_secondary_row_050_cid:
	.word 0x0000166a                                                           @ 09e48150 6a160000
normal_summon_response_secondary_row_050_callback:
	.word check_opponent_zone_full_and_effect_type_eligible+1                  @ 09e48154 11460b08
normal_summon_response_secondary_row_051_cid:
	.word 0x0000183e                                                           @ 09e48158 3e180000
normal_summon_response_secondary_row_051_callback:
	.word check_destruction_or_delinquent_eligible+1                           @ 09e4815c 79460b08
normal_summon_response_secondary_row_052_cid:
	.word 0x000015f7                                                           @ 09e48160 f7150000
normal_summon_response_secondary_row_052_callback:
	.word check_equip_slot_eligible_with_equip_target_and_neo_daedalus+1       @ 09e48164 19450b08
normal_summon_response_secondary_row_053_cid:
	.word 0x000012f1                                                           @ 09e48168 f1120000
normal_summon_response_secondary_row_053_callback:
	.word check_own_effect_nodes_summon_response_eligible+1                    @ 09e4816c f5470b08
normal_summon_response_secondary_row_054_cid:
	.word 0x000012f2                                                           @ 09e48170 f2120000
normal_summon_response_secondary_row_054_callback:
	.word check_own_effect_nodes_summon_response_eligible+1                    @ 09e48174 f5470b08
normal_summon_response_secondary_row_055_cid:
	.word 0x00001329                                                           @ 09e48178 29130000
normal_summon_response_secondary_row_055_callback:
	.word check_own_effect_nodes_summon_response_eligible+1                    @ 09e4817c f5470b08
normal_summon_response_secondary_row_056_cid:
	.word 0x0000132a                                                           @ 09e48180 2a130000
normal_summon_response_secondary_row_056_callback:
	.word check_own_effect_nodes_summon_response_eligible+1                    @ 09e48184 f5470b08
normal_summon_response_secondary_row_057_cid:
	.word 0x00001330                                                           @ 09e48188 30130000
normal_summon_response_secondary_row_057_callback:
	.word check_opposing_effect_nodes_summon_response_eligible+1               @ 09e4818c 21480b08
normal_summon_response_secondary_row_058_cid:
	.word 0x000012cf                                                           @ 09e48190 cf120000
normal_summon_response_secondary_row_058_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e48194 cd460b08
normal_summon_response_secondary_row_059_cid:
	.word 0x000012d0                                                           @ 09e48198 d0120000
normal_summon_response_secondary_row_059_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e4819c cd460b08
normal_summon_response_secondary_row_060_cid:
	.word 0x0000145a                                                           @ 09e481a0 5a140000
normal_summon_response_secondary_row_060_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481a4 cd460b08
normal_summon_response_secondary_row_061_cid:
	.word 0x00001548                                                           @ 09e481a8 48150000
normal_summon_response_secondary_row_061_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481ac cd460b08
normal_summon_response_secondary_row_062_cid:
	.word 0x00001776                                                           @ 09e481b0 76170000
normal_summon_response_secondary_row_062_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481b4 cd460b08
normal_summon_response_secondary_row_063_cid:
	.word 0x00001378                                                           @ 09e481b8 78130000
normal_summon_response_secondary_row_063_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481bc cd460b08
normal_summon_response_secondary_row_064_cid:
	.word 0x000012d2                                                           @ 09e481c0 d2120000
normal_summon_response_secondary_row_064_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481c4 cd460b08
normal_summon_response_secondary_row_065_cid:
	.word 0x00001316                                                           @ 09e481c8 16130000
normal_summon_response_secondary_row_065_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481cc cd460b08
normal_summon_response_secondary_row_066_cid:
	.word 0x0000195f                                                           @ 09e481d0 5f190000
normal_summon_response_secondary_row_066_callback:
	.word check_summon_response_slot_compatible+1                              @ 09e481d4 cd460b08
normal_summon_response_secondary_row_067_cid:
	.word 0x000019ec                                                           @ 09e481d8 ec190000
normal_summon_response_secondary_row_067_callback:
	.word check_effect_handler_summon_response_eligible+1                      @ 09e481dc 51480b08
normal_summon_response_secondary_row_068_cid:
	.word 0x000015b8                                                           @ 09e481e0 b8150000
normal_summon_response_secondary_row_068_callback:
	.word check_slot_effect_link_matches_equip_zone+1                          @ 09e481e4 79480b08
