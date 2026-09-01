# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F13-Seg-2 final PASS landing. dry/check must use direct -noanalysis -readOnly.
# No carve and no new Function. Never stage or commit.

EQ_SLOTS = [(134866720, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'equip_scan_player_offset_9e720'),
 (134866724, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e724'),
 (134866784, 7416, 'EQUIP_ACTIVATION_SAVED_PHASE_OFF', 'equip_scan_saved_phase_offset_9e760'),
 (134866788, 7412, 'P2LP_BLOCK2_OFF_1CF4', 'equip_scan_phase_offset_9e764'),
 (134866792, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e768'),
 (134866848, 5406, 'LAST_TURN_CID', 'equip_scan_cid_9e7a0'),
 (134866852, 285, 'CARD_DISPLAY_OP31_LP_BAR_SUB', 'equip_scan_display_op31_subtype_9e7a4'),
 (134866860, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e7ac'),
 (134866880, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e7c0'),
 (134866900, 5406, 'LAST_TURN_CID', 'equip_scan_cid_9e7d4'),
 (134866932, 354287616, 'LAST_TURN_SETUP_EXTRA_WORD', 'equip_scan_last_turn_extra_9e7f4'),
 (134866940, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e7fc'),
 (134867020, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e84c'),
 (134867052, 7416, 'EQUIP_ACTIVATION_SAVED_PHASE_OFF', 'equip_scan_saved_phase_offset_9e86c'),
 (134867056, 7464, 'EQUIP_CHAIN_STEP_OFF', 'equip_scan_chain_step_offset_9e870'),
 (134867080, 7464, 'EQUIP_CHAIN_STEP_OFF', 'equip_scan_chain_step_offset_9e888'),
 (134867084, 7468, 'EQUIP_CHAIN_ACTIVE_OFF', 'equip_scan_chain_active_offset_9e88c'),
 (134867088, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e890'),
 (134867116, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e8ac'),
 (134867180, 7416, 'EQUIP_ACTIVATION_SAVED_PHASE_OFF', 'equip_scan_saved_phase_offset_9e8ec'),
 (134867184, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e8f0'),
 (134867228, 7476, 'EQUIP_ACTIVATION_SUBPHASE_OFF', 'equip_scan_subphase_offset_9e91c'),
 (134867380, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9e9b4'),
 (134867384, 65535, 'EQUIP_ACTIVATION_CID_U16_MASK', 'equip_scan_cid_mask_9e9b8'),
 (134867388, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9e9bc'),
 (134867572, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9ea74'),
 (134867576, 65535, 'EQUIP_ACTIVATION_CID_U16_MASK', 'equip_scan_cid_mask_9ea78'),
 (134867580, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9ea7c'),
 (134867628, 5119, 'JAM_BREEDING_MACHINE_CID', 'equip_scan_cid_9eaac'),
 (134867644, 5268, 'BLIND_DESTRUCTION_CID', 'equip_scan_cid_9eabc'),
 (134867660, 5401, 'OMINOUS_FORTUNETELLING_CID', 'equip_scan_cid_9eacc'),
 (134867676, 5445, 'NEEDLE_WALL_CID', 'equip_scan_cid_9eadc'),
 (134867692, 5944, 'DANGEROUS_MACHINE_TYPE6_CID', 'equip_scan_cid_9eaec'),
 (134867748, 5132, 'DIMENSIONHOLE_CID', 'equip_scan_cid_9eb24'),
 (134867752, 72356876, 'DIMENSIONHOLE_PACKED_ACTIVATION_ATTR', 'equip_scan_dimensionhole_attr_9eb28'),
 (134867776, 4559, 'get_card_lp_cost_by_id_cid_11cf', 'equip_scan_cid_9eb40'),
 (134867792, 5496, 'LAVA_GOLEM_CID', 'equip_scan_cid_9eb50'),
 (134867936, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9ebe0'),
 (134867940, 4920, 'EQUIP_ACTIVATION_UNMAPPED_CID_1338', 'equip_scan_cid_9ebe4'),
 (134867944, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9ebe8'),
 (134867984, 5200, 'SPIRIT_OF_THE_BREEZE_CID', 'equip_scan_cid_9ec10'),
 (134868000, 5201, 'DANCING_FAIRY_CID', 'equip_scan_cid_9ec20'),
 (134868016, 5204, 'CURE_MERMAID_CID', 'equip_scan_cid_9ec30'),
 (134868048, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9ec50'),
 (134868168, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9ecc8'),
 (134868172, 2105343, 'CARD_WORD_CID_AND_BIT21_MASK', 'equip_scan_cid_bit21_mask_9eccc'),
 (134868176, 5209, 'MARIE_THE_FALLEN_ONE_CID', 'equip_scan_cid_9ecd0'),
 (134868180, 72220672, 'EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX', 'equip_scan_array_attr_prefix_9ecd4'),
 (134868188, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9ecdc'),
 (134868220, 5672, 'SENRI_EYE_CID', 'equip_scan_cid_9ecfc'),
 (134868236, 5975, 'WHITE_MAGICIAN_PIKERU_CID', 'equip_scan_cid_9ed0c'),
 (134868252, 6429, 'EBON_MAGICIAN_CURRAN_CID', 'equip_scan_cid_9ed1c'),
 (134868268, 6605, 'PRINCESS_PIKERU_CID', 'equip_scan_cid_9ed2c'),
 (134868284, 6606, 'PRINCESS_CURRAN_CID', 'equip_scan_cid_9ed3c'),
 (134868300, 5687, 'BOWGANIAN_CID', 'equip_scan_cid_9ed4c'),
 (134868460, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9edec'),
 (134868464, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9edf0'),
 (134868468, 5776, 'INFERNALQUEEN_ARCHFIEND_CID', 'equip_scan_cid_9edf4'),
 (134868652, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9eeac'),
 (134868656, 5265, 'GRAVEROBBERS_RETRIBUTION_CID', 'equip_scan_cid_9eeb0'),
 (134868660, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9eeb4'),
 (134868836, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9ef64'),
 (134868840, 5126, 'BURNING_LAND_CID', 'equip_scan_cid_9ef68'),
 (134868844, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9ef6c'),
 (134868884, 5104, 'MASK_OF_DISPEL_CID', 'equip_scan_cid_9ef94'),
 (134868900, 5107, 'MASK_OF_THE_ACCURSED_CID', 'equip_scan_cid_9efa4'),
 (134868916, 5298, 'NIGHTMARE_WHEEL_CID', 'equip_scan_cid_9efb4'),
 (134868940, 4898, 'SNATCH_STEAL_CID', 'equip_scan_cid_9efcc'),
 (134868964, 6263, 'BRAIN_JACKER_CID', 'equip_scan_cid_9efe4'),
 (134868988, 5786, 'FALLING_DOWN_CID', 'equip_scan_cid_9effc'),
 (134869012, 4987, 'EYE_OF_TRUTH_CID', 'equip_scan_cid_9f014'),
 (134869036, 4949, 'MINOR_GOBLIN_OFFICIAL_CID', 'equip_scan_cid_9f02c'),
 (134869060, 4742, 'BLAST_SPHERE_CID', 'equip_scan_cid_9f044'),
 (134869084, 6589, 'ADHESIVE_EXPLOSIVE_CID', 'equip_scan_cid_9f05c'),
 (134869108, 6608, 'MALICE_ASCENDANT_CID', 'equip_scan_cid_9f074'),
 (134869292, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9f12c'),
 (134869296, 4976, 'KISEITAI_CID', 'equip_scan_cid_9f130'),
 (134869300, 65535, 'EQUIP_CHAIN_PAIR_MISSING', 'equip_scan_chain_pair_missing_f134'),
 (134869304, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f138'),
 (134869456, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f1d0'),
 (134869464, 72220672, 'EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX', 'equip_scan_array_attr_prefix_9f1d8'),
 (134869496, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f1f8'),
 (134869512, 4481, 'SINISTER_SERPENT_CID', 'equip_scan_cid_9f208'),
 (134869528, 6603, 'TREEBORN_FROG_CID', 'equip_scan_cid_9f218'),
 (134869756, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f2fc'),
 (134869764, 2105343, 'CARD_WORD_CID_AND_BIT21_MASK', 'equip_scan_cid_bit21_mask_9f304'),
 (134869768, 6005, 'RETURN_ZOMBIE_CID', 'equip_scan_cid_9f308'),
 (134869772, 4294963263, 'ACTIVATION_ENTRY_CLR_BITS_11_6', 'equip_scan_clear_bits_11_6_9f30c'),
 (134869776, 4294934591, 'ACTIVATION_ENTRY_CLR_BITS_14_6', 'equip_scan_clear_bits_14_6_9f310'),
 (134869780, 72220672, 'EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX', 'equip_scan_array_attr_prefix_9f314'),
 (134869828, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f344'),
 (134869980, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9f3dc'),
 (134869984, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f3e0'),
 (134869992, 5042, 'MUCUS_YOLK_CID', 'equip_scan_cid_9f3e8'),
 (134870040, 5453, 'LEGENDARY_FIEND_CID', 'equip_scan_cid_9f418'),
 (134870056, 5701, 'EXODIA_NECROSS_CID', 'equip_scan_cid_9f428'),
 (134870072, 5646, 'AMAZONESS_BLOWPIPER_CID', 'equip_scan_cid_9f438'),
 (134870168, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9f498'),
 (134870172, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f49c'),
 (134870176, 6162, 'SILENT_SWORDSMAN_LV3_CID', 'equip_scan_cid_9f4a0'),
 (134870184, 6105, 'ARMED_DRAGON_LV3_CID', 'equip_scan_cid_9f4a8'),
 (134870208, 6167, 'SILENT_MAGICIAN_LV4_CID', 'equip_scan_cid_9f4c0'),
 (134870296, 6178, 'ULTIMATE_INSECT_LV3_CID', 'equip_scan_cid_9f518'),
 (134870304, 7412, 'FIELD_STATE_OFF', 'equip_scan_cursor_from_field_offset_f520'),
 (134870396, 65535, 'EQUIP_ACTIVATION_CID_U16_MASK', 'equip_scan_cid_mask_9f57c'),
 (134870400, 72220672, 'EQUIP_ACTIVATION_CARD_ARRAY_ATTR_PREFIX', 'equip_scan_array_attr_prefix_9f580'),
 (134870416, 5063, 'REVIVAL_JAM_CID', 'equip_scan_cid_9f590'),
 (134870432, 5410, 'VAMPIRE_LORD_CID', 'equip_scan_cid_9f5a0'),
 (134870448, 6236, 'SACRED_PHOENIX_CID', 'equip_scan_cid_9f5b0'),
 (134870464, 6287, 'CURSE_OF_VAMPIRE_CID', 'equip_scan_cid_9f5c0'),
 (134870488, 6287, 'CURSE_OF_VAMPIRE_CID', 'equip_scan_cid_9f5d8'),
 (134870656, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_scan_cursor_offset_9f680'),
 (134870660, 65535, 'EQUIP_ACTIVATION_CID_U16_MASK', 'equip_scan_cid_mask_9f684'),
 (134870664, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f688'),
 (134870748, 7592, 'LP_CARD_TRACK_BASE_OFF', 'equip_scan_lp_track_offset_9f6dc'),
 (134870752, 2152, 'PLAYER_BLOCK_STRIDE', 'equip_scan_player_stride_9f6e0'),
 (134870808, 4967, 'EQUIP_ACTIVATION_UNMAPPED_CID_1367', 'equip_scan_cid_9f718'),
 (134870824, 5845, 'RECYCLE_CID', 'equip_scan_cid_9f728'),
 (134870848, 5253, 'AQUA_SPIRIT_CID', 'equip_scan_cid_9f740')]

REF_SLOTS = [(134866728, 134866732, 'equip_activation_subphase_targets', 'equip_scan_subphase_table_9e728'),
 (134866732, 134866764, 'equip_activation_subphase_case0', 'equip_activation_subphase_targets'),
 (134866736, 134866796, 'equip_activation_subphase_case1', 'equip_activation_subphase_case1_ptr'),
 (134866740, 134866884, 'equip_activation_subphase_case2', 'equip_activation_subphase_case2_ptr'),
 (134866744, 134866904, 'equip_activation_subphase_case3', 'equip_activation_subphase_case3_ptr'),
 (134866748, 134866944, 'equip_activation_subphase_case4', 'equip_activation_subphase_case4_ptr'),
 (134866752, 134867024, 'equip_activation_subphase_case5', 'equip_activation_subphase_case5_ptr'),
 (134866756, 134867092, 'equip_activation_subphase_case6', 'equip_activation_subphase_case6_ptr'),
 (134866760, 134867120, 'equip_activation_subphase_case7', 'equip_activation_subphase_case7_ptr'),
 (134866856, 33670368, 'gP1LifePoints', 'equip_scan_lp_base_9e7a8'),
 (134866876, 33670368, 'gP1LifePoints', 'equip_scan_lp_base_9e7bc'),
 (134866936, 33670368, 'gP1LifePoints', 'equip_scan_lp_base_9e7f8'),
 (134867016, 33670368, 'gP1LifePoints', 'equip_scan_lp_base_9e848'),
 (134867112, 33670368, 'gP1LifePoints', 'equip_scan_lp_base_9e8a8'),
 (134867176, 33670368, 'gP1LifePoints', 'equip_scan_lp_base_9e8e8'),
 (134868664, 33670416, 'gDuelFieldSlots', 'equip_scan_field_base_9eeb8'),
 (134869460, 33671416, 'gP1HandSlotArray', 'equip_scan_card_array_base_9f1d4'),
 (134869760, 33671416, 'gP1HandSlotArray', 'equip_scan_card_array_base_9f300'),
 (134869988, 33670416, 'gDuelFieldSlots', 'equip_scan_field_base_9f3e4'),
 (134870300, 33670416, 'gDuelFieldSlots', 'equip_scan_field_base_9f51c')]

RENAME_SLOTS = [(134866716,
  'equip_scan_lp_base_9e71c',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867224,
  'equip_scan_lp_base_9e918',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867376,
  'equip_scan_lp_base_9e9b0',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867420,
  'equip_scan_lp_base_9e9dc',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867568,
  'equip_scan_lp_base_9ea70',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867612,
  'equip_scan_lp_base_9ea9c',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867932,
  'equip_scan_lp_base_9ebdc',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868044,
  'equip_scan_lp_base_9ec4c',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868184,
  'equip_scan_lp_base_9ecd8',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868456,
  'equip_scan_lp_base_9ede8',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868648,
  'equip_scan_lp_base_9eea8',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868832,
  'equip_scan_lp_base_9ef60',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869288,
  'equip_scan_lp_base_9f128',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869452,
  'equip_scan_lp_base_9f1cc',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869752,
  'equip_scan_lp_base_9f2f8',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869824,
  'equip_scan_lp_base_9f340',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869976,
  'equip_scan_lp_base_9f3d8',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134870164,
  'equip_scan_lp_base_9f494',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134870652,
  'equip_scan_lp_base_9f67c',
  'Base/target gP1LifePoints; preserve the stored address and all unrelated references.')]

PLATES = [(134866676,
  'dispatch_equip_activation_state_by_subphase',
  'No arguments. Dispatch LP+0x1d34 subphase 0..7 through eight even Thumb targets using MOV pc,r0. Player comes '
  'from LP+0x1ce8. Cases share this frame and return path: save phase, gate Last Turn, set display context, set '
  'sprite data, validate slots, set chain state, advance display, submit final sprite. Returns 1 for subphase >7 or '
  'case-4 rejection; otherwise 0. Case-1 rejection sets subphase=8; case 6 waits for a nonzero helper result. No '
  'independent case functions.'),
 (134867204,
  'check_activation_phase_counter_is_six',
  'No arguments. Return 1 exactly when the u32 activation subphase at gP1LifePoints+0x1d34 equals 6, else 0. '
  'Read-only leaf; no stack frame.'),
 (134867232,
  'scan_monster_zone_for_equip_activation_by_card',
  'r0=player, r1=internal CID. Resume monster slots 0..4 using the u32 cursor at LP+0x1d24. For each active CID '
  'match, build player/slot/CID packed attributes and pass decoded entry flags to '
  'apply_equip_activation_with_id_lookup. A nonzero helper result advances the cursor once and returns 0; zero '
  'continues scanning. Every rejected slot also advances. Return 1 on exhaustion.'),
 (134867424,
  'scan_trap_zone_for_equip_activation_by_card',
  'r0=player, r1=internal CID. Resume five spell/trap slots cursor+5 using LP+0x1d24 cursor 0..4. For active CID '
  'matches, pack player/slot/CID and decoded entry flags for apply_equip_activation_with_id_lookup. A nonzero helper '
  'result advances cursor and returns 0; zero continues scanning. Rejected slots also advance. Return 1 on '
  'exhaustion.'),
 (134867616,
  'scan_trap_zone_for_equip_activation_jam_breeding_machine',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x13ff) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867632,
  'scan_trap_zone_for_equip_activation_blind_destruction',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1494) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867648,
  'scan_trap_zone_for_equip_activation_ominous_fortunetelling',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1519) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867664,
  'scan_trap_zone_for_equip_activation_needle_wall',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1545) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867680,
  'scan_trap_zone_for_equip_activation_dangerous_machine_type6',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1738) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867696,
  'scan_equip_zone_for_dimensionhole',
  'r0=player. Query zone 11 for Dimensionhole. Missing entity returns 1. Otherwise call '
  'apply_equip_activation_with_id_lookup with player bit OR 0x0450140c and zero entity/payload. If it returns zero, '
  'enqueue the zone-11 Dimensionhole sprite. Return 0 whenever the entity query succeeded, independent of activation '
  'result.'),
 (134867764,
  'scan_monster_zone_for_equip_activation_reserved_icid_f',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x11cf) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867780,
  'scan_monster_zone_for_equip_activation_lava_golem',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1578) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867796,
  'scan_monster_zone_slots_for_equip_activation_reserved_icid_g',
  'r0=player. Resume monster slots 0..4 via LP+0x1d24. Require active CID 0x1338 and exactly one occupied monster '
  'slot. Enqueue entry flags; if entry+6 is zero, invoke activation with zero arguments. Set slot field bit 0x15, '
  'advance cursor and return 0. Other slots advance without emission; exhaustion returns 1. CID 0x1338 has no card '
  'mapping.'),
 (134867972,
  'scan_monster_zone_for_equip_activation_spirit_of_the_breeze',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1450) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134867988,
  'scan_monster_zone_for_equip_activation_dancing_fairy',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1451) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868004,
  'scan_monster_zone_for_equip_activation_cure_mermaid',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1454) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868020,
  'scan_player_card_array_for_equip_activation_marie_the_fallen_one',
  'r0=player. If LP+0x1d24 is nonzero, return 1. Otherwise scan the player 4-byte card-word array at '
  'gP1HandSlotArray with count LP+0x14 and stride 0x868. Match (word & 0x00201fff)==MARIE_THE_FALLEN_ONE_CID, pack '
  'each match with 0x044e0000 and player bit, and call activation with decoded flags. Ignore each result. Increment '
  'the shared cursor and return 0 even if no entry matched.'),
 (134868192,
  'scan_trap_zone_for_equip_activation_life_absorbing_machine',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x14c0) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868208,
  'scan_trap_zone_for_equip_activation_senri_eye',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x1628) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868224,
  'scan_monster_zone_for_equip_activation_white_magician_pikeru',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1757) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868240,
  'scan_monster_zone_for_equip_activation_ebon_magician_curran',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x191d) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868256,
  'scan_monster_zone_for_equip_activation_princess_pikeru',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x19cd) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868272,
  'scan_monster_zone_for_equip_activation_princess_curran',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x19ce) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868288,
  'scan_monster_zone_for_equip_activation_bowganian',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1637) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868304,
  'scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend',
  'r0=player. Resume ten monster slots with LP+0x1d24 cursor: side=(cursor/5)^player, slot=cursor%5. For active '
  'Infernalqueen Archfiend, pack the actual entry CID, side and slot, then call activation with decoded flags. '
  'Ignore its result; advance cursor and return 0 after the first match. Other entries advance and continue. Return '
  '1 after cursor 9.'),
 (134868500,
  'scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution',
  "r0=player. Start LP+0x1d24 at 5 when zero and scan spell/trap slots through 9. Require active Graverobber's "
  'Retribution and nonzero count_zone_slots_with_card_field5(1-player). Enqueue entry flags, then the opponent LP '
  'indicator with amount=count*100, mode=1 and this CID. Advance cursor and return 0 on emission; rejected slots '
  'advance. Exhaustion returns 1.'),
 (134868696,
  'scan_all_zone_slots_for_lp_indicator_burning_land',
  'r0=player. Resume ten spell/trap slots: side=(cursor/5)^player, slot=cursor%5+5, cursor at LP+0x1d24. On active '
  'Burning Land, enqueue entry flags and an LP indicator for the input player, amount 500, mode=(side!=player), CID '
  'Burning Land. Advance cursor and return 0; rejected entries advance. Return 1 after cursor 9.'),
 (134868872,
  'scan_trap_zone_for_equip_activation_mask_of_dispel',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x13f0) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868888,
  'scan_trap_zone_for_equip_activation_mask_of_accursed',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x13f3) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868904,
  'scan_trap_zone_for_equip_activation_nightmare_wheel',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(player, CID 0x14b2) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868920,
  'scan_trap_zone_for_equip_activation_snatch_steal',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1322) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868944,
  'scan_trap_zone_for_equip_activation_brain_jacker',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1877) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868968,
  'scan_trap_zone_for_equip_activation_falling_down',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x169a) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134868992,
  'scan_trap_zone_for_equip_activation_the_eye_of_truth',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x137b) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869016,
  'scan_trap_zone_for_equip_activation_minor_goblin_official',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1355) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869040,
  'scan_trap_zone_for_equip_activation_blast_sphere',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x1286) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869064,
  'scan_trap_zone_for_equip_activation_adhesive_explosive',
  'r0=player. Call scan_trap_zone_for_equip_activation_by_card(1-player, CID 0x19bd) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869088,
  'scan_monster_zone_for_equip_activation_malice_ascendant',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(1-player, CID 0x19d0) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869112,
  'scan_trap_slots_for_kiseitai_equip_chain_sprite',
  'r0=player. Scan opponent slots cursor+5 for cursor 0..4 at LP+0x1d24. Require active Kiseitai, a non-0xffff equip '
  'pair, and pair lookup result 0xa. Enqueue opponent slot flags and submit opponent LP/shape sprites with '
  '(get_slot_field5_score(pair)+1)>>1. Advance cursor and return 0 on emission. Rejected slots advance; exhaustion '
  'returns 1.'),
 (134869336,
  'scan_player_card_array_for_equip_activation_by_cid',
  'r0=player, r1=internal CID. Return 1 if zone-11 chain already contains the CID. Scan the player 4-byte card array '
  'at gP1HandSlotArray, count LP+0x14, stride 0x868; require matching low13 CID and clear bit21. Pack 0x044e0000, '
  'player and CID, and call activation with decoded flags. Return 0 on a nonzero helper result; return 1 when all '
  'entries fail. Does not use the shared scan cursor.'),
 (134869500,
  'scan_player_card_array_for_equip_activation_sinister_serpent',
  'r0=player. Call scan_player_card_array_for_equip_activation_by_cid(player, CID 0x1181) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869516,
  'scan_player_card_array_for_equip_activation_treeborn_frog',
  'r0=player. Call scan_player_card_array_for_equip_activation_by_cid(player, CID 0x19cb) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134869532,
  'scan_equip_zone_for_special_summon_activation_return_zombie',
  'r0=player. Scan the player 4-byte card-word array, count LP+0x14, stride 0x868. Match Return Zombie with bit21 '
  'clear. Build a zeroed 0x18-byte local entry, set CID/player/decoded flags and the eligibility fields. Only '
  'check_card_special_summon_eligible_full(entry)==0 proceeds to packed activation with prefix 0x044e0000. Return 0 '
  'on a nonzero activation result; continue otherwise. Return 1 on exhaustion.'),
 (134869832,
  'scan_monster_zone_slots_for_equip_activation_mucus_yolk',
  'r0=player. Resume monster slots 0..4 with cursor at LP+0x1d24. Require active Mucus Yolk and a nonzero '
  'check_node_in_slot_chain(player,slot,CID,2). Enqueue entry flags and '
  'enqueue_sprite_attr_with_mode(player,slot,actual_entry_CID,3,1). Advance cursor and return 0 on emission; '
  'rejected slots advance. Return 1 on exhaustion.'),
 (134870028,
  'scan_monster_zone_for_equip_activation_legendary_fiend',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x154d) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870044,
  'scan_monster_zone_for_equip_activation_exodia_necross',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1645) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870060,
  'scan_monster_zone_for_equip_activation_amazoness_blowpiper',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x160e) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870076,
  'scan_monster_zone_for_equip_activation_agent_of_wisdom_mercury',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(player, CID 0x1740) with an ordinary BL and return '
  'its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870092,
  'scan_field_slots_for_lv_monster_equip_activation',
  'r0=player. Resume monster slots 0..4 with cursor at LP+0x1d24. Match CID in '
  '{0x1812,0x17d5,0x17d1,0x17d9,0x1817,0x1814,0x1822,0x185e} and require nonzero entry+8. Pack entry CID/player/slot '
  'and call activation with decoded flags, ignoring its result. Increment the same cursor via gDuelFieldSlots+0x1cf4 '
  'and return 0. Rejected entries advance; exhaustion returns 1.'),
 (134870328,
  'scan_equip_zone_for_entity_sprite_and_activation',
  'r0=player, r1=internal CID. Query zone 11 for a matching entity; a negative result returns 1. Otherwise enqueue '
  'the chain-match sprite, build player bit OR 0x044e0000 OR CID low16, and call '
  'apply_equip_activation_with_id_lookup with the entity low16 and zero payload. Ignore the activation result and '
  'return 0.'),
 (134870404,
  'scan_equip_zone_for_equip_activation_revival_jam',
  'r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x13c7) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870420,
  'scan_equip_zone_for_equip_activation_vampire_lord',
  'r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x1522) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870436,
  'scan_equip_zone_for_equip_activation_sacred_phoenix',
  'r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x185c) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870452,
  'scan_equip_zone_for_entity_sprite_activation_curse_of_vampire',
  'r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(player, CID 0x188f) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870468,
  'scan_equip_zone_for_entity_sprite_activation_curse_of_vampire_opponent',
  'r0=player. Call scan_equip_zone_for_entity_sprite_and_activation(1-player, CID 0x188f) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870492,
  'scan_spell_trap_zone_for_equip_activation_via_packed_attr',
  'r0=player, r1=internal CID. Cursor LP+0x1d24==0 starts a scan at slot 5 through 9. On successful packed '
  'activation, set the LP row and return 0 without advancing that slot. Exhaustion returns 1 with cursor 10. On '
  'entry with nonzero cursor, zero u16 at LP+0x1da8 returns 1 unchanged; nonzero submits that cursor slot as packed '
  'sprite data, clears cursor and returns 0.'),
 (134870788,
  'scan_spell_trap_zone_for_equip_activation_reserved_icid_e',
  'r0=player. Call scan_spell_trap_zone_for_equip_activation_via_packed_attr(1-player, CID 0x1367) with an ordinary '
  'BL and return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870812,
  'scan_spell_trap_zone_for_equip_activation_recycle',
  'r0=player. Call scan_spell_trap_zone_for_equip_activation_via_packed_attr(player, CID 0x16d5) with an ordinary BL '
  'and return its result unchanged. The callee owns scan state and sprite side effects.'),
 (134870828,
  'scan_monster_zone_for_equip_activation_aqua_spirit_opponent',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card(1-player, CID 0x1485) with an ordinary BL and '
  'return its result unchanged. The callee owns scan state and sprite side effects.')]

SLOT_EOLS = [(134866716, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134866720, 'Byte offset from gP1LifePoints; player offset.'),
 (134866724, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134866728,
  'Base/target equip_activation_subphase_targets; preserve the stored address and all unrelated references.'),
 (134866732,
  'Base/target equip_activation_subphase_case0; preserve the stored address and all unrelated references.'),
 (134866736,
  'Base/target equip_activation_subphase_case1; preserve the stored address and all unrelated references.'),
 (134866740,
  'Base/target equip_activation_subphase_case2; preserve the stored address and all unrelated references.'),
 (134866744,
  'Base/target equip_activation_subphase_case3; preserve the stored address and all unrelated references.'),
 (134866748,
  'Base/target equip_activation_subphase_case4; preserve the stored address and all unrelated references.'),
 (134866752,
  'Base/target equip_activation_subphase_case5; preserve the stored address and all unrelated references.'),
 (134866756,
  'Base/target equip_activation_subphase_case6; preserve the stored address and all unrelated references.'),
 (134866760,
  'Base/target equip_activation_subphase_case7; preserve the stored address and all unrelated references.'),
 (134866784, 'Byte offset from gP1LifePoints; saved phase offset.'),
 (134866788, 'Byte offset from gP1LifePoints; phase offset.'),
 (134866792, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134866848, 'Internal CID 0x151e; see verified card mapping.'),
 (134866852, 'Value for display op31 subtype.'),
 (134866856, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134866860, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134866876, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134866880, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134866900, 'Internal CID 0x151e; see verified card mapping.'),
 (134866932, 'Value for last turn extra.'),
 (134866936, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134866940, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134867016, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867020, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134867052, 'Byte offset from gP1LifePoints; saved phase offset.'),
 (134867056, 'Byte offset from gP1LifePoints; chain step offset.'),
 (134867080, 'Byte offset from gP1LifePoints; chain step offset.'),
 (134867084, 'Byte offset from gP1LifePoints; chain active offset.'),
 (134867088, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134867112, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867116, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134867176, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867180, 'Byte offset from gP1LifePoints; saved phase offset.'),
 (134867184, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134867224, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867228, 'Byte offset from gP1LifePoints; subphase offset.'),
 (134867376, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867380, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134867384, 'Value for cid mask.'),
 (134867388, 'Value for player stride.'),
 (134867420, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867568, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867572, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134867576, 'Value for cid mask.'),
 (134867580, 'Value for player stride.'),
 (134867612, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867628, 'Internal CID 0x13ff; see verified card mapping.'),
 (134867644, 'Internal CID 0x1494; see verified card mapping.'),
 (134867660, 'Internal CID 0x1519; see verified card mapping.'),
 (134867676, 'Internal CID 0x1545; see verified card mapping.'),
 (134867692, 'Internal CID 0x1738; see verified card mapping.'),
 (134867748, 'Internal CID 0x140c; see verified card mapping.'),
 (134867752, 'Value for dimensionhole attr.'),
 (134867776, 'Internal CID 0x11cf; see verified card mapping.'),
 (134867792, 'Internal CID 0x1578; see verified card mapping.'),
 (134867932, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134867936, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134867940, 'Internal CID 0x1338; see verified card mapping.'),
 (134867944, 'Value for player stride.'),
 (134867984, 'Internal CID 0x1450; see verified card mapping.'),
 (134868000, 'Internal CID 0x1451; see verified card mapping.'),
 (134868016, 'Internal CID 0x1454; see verified card mapping.'),
 (134868044, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868048, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134868168, 'Value for player stride.'),
 (134868172, 'Value for cid bit21 mask.'),
 (134868176, 'Internal CID 0x1459; see verified card mapping.'),
 (134868180, 'Value for array attr prefix.'),
 (134868184, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868188, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134868220, 'Internal CID 0x1628; see verified card mapping.'),
 (134868236, 'Internal CID 0x1757; see verified card mapping.'),
 (134868252, 'Internal CID 0x191d; see verified card mapping.'),
 (134868268, 'Internal CID 0x19cd; see verified card mapping.'),
 (134868284, 'Internal CID 0x19ce; see verified card mapping.'),
 (134868300, 'Internal CID 0x1637; see verified card mapping.'),
 (134868456, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868460, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134868464, 'Value for player stride.'),
 (134868468, 'Internal CID 0x1690; see verified card mapping.'),
 (134868648, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868652, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134868656, 'Internal CID 0x1491; see verified card mapping.'),
 (134868660, 'Value for player stride.'),
 (134868664, 'Base/target gDuelFieldSlots; preserve the stored address and all unrelated references.'),
 (134868832, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134868836, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134868840, 'Internal CID 0x1406; see verified card mapping.'),
 (134868844, 'Value for player stride.'),
 (134868884, 'Internal CID 0x13f0; see verified card mapping.'),
 (134868900, 'Internal CID 0x13f3; see verified card mapping.'),
 (134868916, 'Internal CID 0x14b2; see verified card mapping.'),
 (134868940, 'Internal CID 0x1322; see verified card mapping.'),
 (134868964, 'Internal CID 0x1877; see verified card mapping.'),
 (134868988, 'Internal CID 0x169a; see verified card mapping.'),
 (134869012, 'Internal CID 0x137b; see verified card mapping.'),
 (134869036, 'Internal CID 0x1355; see verified card mapping.'),
 (134869060, 'Internal CID 0x1286; see verified card mapping.'),
 (134869084, 'Internal CID 0x19bd; see verified card mapping.'),
 (134869108, 'Internal CID 0x19d0; see verified card mapping.'),
 (134869288, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869292, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134869296, 'Internal CID 0x1370; see verified card mapping.'),
 (134869300, 'Value for cid mask.'),
 (134869304, 'Value for player stride.'),
 (134869452, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869456, 'Value for player stride.'),
 (134869460, 'Base/target gP1HandSlotArray; preserve the stored address and all unrelated references.'),
 (134869464, 'Value for array attr prefix.'),
 (134869496, 'Value for player stride.'),
 (134869512, 'Internal CID 0x1181; see verified card mapping.'),
 (134869528, 'Internal CID 0x19cb; see verified card mapping.'),
 (134869752, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869756, 'Value for player stride.'),
 (134869760, 'Base/target gP1HandSlotArray; preserve the stored address and all unrelated references.'),
 (134869764, 'Value for cid bit21 mask.'),
 (134869768, 'Internal CID 0x1775; see verified card mapping.'),
 (134869772, 'Value for clear bits 11 6.'),
 (134869776, 'Value for clear bits 14 6.'),
 (134869780, 'Value for array attr prefix.'),
 (134869824, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869828, 'Value for player stride.'),
 (134869976, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134869980, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134869984, 'Value for player stride.'),
 (134869988, 'Base/target gDuelFieldSlots; preserve the stored address and all unrelated references.'),
 (134869992, 'Internal CID 0x13b2; see verified card mapping.'),
 (134870040, 'Internal CID 0x154d; see verified card mapping.'),
 (134870056, 'Internal CID 0x1645; see verified card mapping.'),
 (134870072, 'Internal CID 0x160e; see verified card mapping.'),
 (134870164, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134870168, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134870172, 'Value for player stride.'),
 (134870176, 'Internal CID 0x1812; see verified card mapping.'),
 (134870184, 'Internal CID 0x17d9; see verified card mapping.'),
 (134870208, 'Internal CID 0x1817; see verified card mapping.'),
 (134870296, 'Internal CID 0x1822; see verified card mapping.'),
 (134870300, 'Base/target gDuelFieldSlots; preserve the stored address and all unrelated references.'),
 (134870304, 'Byte offset from gDuelFieldSlots to the shared scan cursor; equals LP+0x1d24.'),
 (134870396, 'Value for cid mask.'),
 (134870400, 'Value for array attr prefix.'),
 (134870416, 'Internal CID 0x13c7; see verified card mapping.'),
 (134870432, 'Internal CID 0x1522; see verified card mapping.'),
 (134870448, 'Internal CID 0x185c; see verified card mapping.'),
 (134870464, 'Internal CID 0x188f; see verified card mapping.'),
 (134870488, 'Internal CID 0x188f; see verified card mapping.'),
 (134870652, 'Base/target gP1LifePoints; preserve the stored address and all unrelated references.'),
 (134870656, 'Byte offset from gP1LifePoints; cursor offset.'),
 (134870660, 'Value for cid mask.'),
 (134870664, 'Value for player stride.'),
 (134870748, 'Byte offset from gP1LifePoints; lp track offset.'),
 (134870752, 'Value for player stride.'),
 (134870808, 'Internal CID 0x1367; see verified card mapping.'),
 (134870824, 'Internal CID 0x16d5; see verified card mapping.'),
 (134870848, 'Internal CID 0x1485; see verified card mapping.')]

FUNC_RENAME = [(134868020,
  'scan_monster_slots_for_equip_activation_marie_the_fallen_one',
  'scan_player_card_array_for_equip_activation_marie_the_fallen_one'),
 (134869336, 'scan_monster_zone_chain_for_equip_activation', 'scan_player_card_array_for_equip_activation_by_cid'),
 (134869500,
  'scan_monster_zone_chain_for_equip_activation_sinister_serpent',
  'scan_player_card_array_for_equip_activation_sinister_serpent'),
 (134869516,
  'scan_monster_zone_chain_for_equip_activation_treeborn_frog',
  'scan_player_card_array_for_equip_activation_treeborn_frog')]

CASE_LABELS = [(134866764, 'equip_activation_subphase_case0', 'Case 0: copy LP+0x1cf4 to LP+0x1cf8, increment subphase, return 0.'),
 (134866796,
  'equip_activation_subphase_case1',
  'Case 1: require available slot, group placement and Last Turn effect gates; failure sets subphase 8, success '
  'emits op31 and advances.'),
 (134866884,
  'equip_activation_subphase_case2',
  'Case 2: initialize player display context with zone 6, Last Turn CID and zero flags, then advance.'),
 (134866904,
  'equip_activation_subphase_case3',
  'Case 3: submit monster-entry pointer with flags 1, mode 0 and stack extra Last Turn CID in high16, then advance.'),
 (134866944,
  'equip_activation_subphase_case4',
  'Case 4: require own entity-1 and opponent entity-0 slots plus both activation checks; reject with 1 or advance '
  'with 0.'),
 (134867024,
  'equip_activation_subphase_case5',
  'Case 5: write chain step 1 iff saved phase equals 3, else 0; clear chain active word and advance.'),
 (134867092,
  'equip_activation_subphase_case6',
  'Case 6: wait until display advance returns nonzero; then increment subphase. Return 0 in both paths.'),
 (134867120,
  'equip_activation_subphase_case7',
  'Case 7: unless saved phase is 3, enqueue type saved_phase+12 with player side bit; increment subphase and return '
  '0.')]

DISASM_INSTRUCTIONS = [(134866764, 2, '0448', 'ldr', 'r0, [pc, #16]'),
 (134866766, 2, '1118', 'adds', 'r1, r2, r0'),
 (134866768, 2, '044b', 'ldr', 'r3, [pc, #16]'),
 (134866770, 2, 'd018', 'adds', 'r0, r2, r3'),
 (134866772, 2, '0068', 'ldr', 'r0, [r0, #0]'),
 (134866774, 2, '0860', 'str', 'r0, [r1, #0]'),
 (134866776, 2, '0348', 'ldr', 'r0, [pc, #12]'),
 (134866778, 2, '1118', 'adds', 'r1, r2, r0'),
 (134866780, 2, 'bfe0', 'b.n', '0x809e8de'),
 (134866796, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866798, 4, '94f723ff', 'bl', '0x80335b8'),
 (134866802, 2, '0028', 'cmp', 'r0, #0'),
 (134866804, 2, '1cd0', 'beq.n', '0x809e7b0'),
 (134866806, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866808, 4, '9df700fa', 'bl', '0x803bb7c'),
 (134866812, 2, '0028', 'cmp', 'r0, #0'),
 (134866814, 2, '17d0', 'beq.n', '0x809e7b0'),
 (134866816, 2, '0749', 'ldr', 'r1, [pc, #28]'),
 (134866818, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866820, 2, '0022', 'movs', 'r2, #0'),
 (134866822, 4, 'eff793f9', 'bl', '0x808dab0'),
 (134866826, 2, '0028', 'cmp', 'r0, #0'),
 (134866828, 2, '10d0', 'beq.n', '0x809e7b0'),
 (134866830, 2, '0549', 'ldr', 'r1, [pc, #20]'),
 (134866832, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866834, 4, 'f4f7fdfd', 'bl', '0x8093390'),
 (134866838, 2, '0449', 'ldr', 'r1, [pc, #16]'),
 (134866840, 2, '044a', 'ldr', 'r2, [pc, #16]'),
 (134866842, 2, '8918', 'adds', 'r1, r1, r2'),
 (134866844, 2, '9fe0', 'b.n', '0x809e8de'),
 (134866864, 2, '0248', 'ldr', 'r0, [pc, #8]'),
 (134866866, 2, '034b', 'ldr', 'r3, [pc, #12]'),
 (134866868, 2, 'c018', 'adds', 'r0, r0, r3'),
 (134866870, 2, '0821', 'movs', 'r1, #8'),
 (134866872, 2, '0160', 'str', 'r1, [r0, #0]'),
 (134866874, 2, '93e0', 'b.n', '0x809e8e4'),
 (134866884, 2, '034a', 'ldr', 'r2, [pc, #12]'),
 (134866886, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866888, 2, '0621', 'movs', 'r1, #6'),
 (134866890, 2, '0023', 'movs', 'r3, #0'),
 (134866892, 4, 'f5f7fafc', 'bl', '0x80941c4'),
 (134866896, 2, '82e0', 'b.n', '0x809e8d8'),
 (134866904, 4, 'f5f780fd', 'bl', '0x80942dc'),
 (134866908, 2, '011c', 'adds', 'r1, r0, #0'),
 (134866910, 2, '0548', 'ldr', 'r0, [pc, #20]'),
 (134866912, 2, '0090', 'str', 'r0, [sp, #0]'),
 (134866914, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866916, 2, '0122', 'movs', 'r2, #1'),
 (134866918, 2, '0023', 'movs', 'r3, #0'),
 (134866920, 4, '0df0bafa', 'bl', '0x80abd60'),
 (134866924, 2, '0249', 'ldr', 'r1, [pc, #8]'),
 (134866926, 2, '034a', 'ldr', 'r2, [pc, #12]'),
 (134866928, 2, '8918', 'adds', 'r1, r1, r2'),
 (134866930, 2, '74e0', 'b.n', '0x809e8de'),
 (134866944, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866946, 4, 'fff727ff', 'bl', '0x809e654'),
 (134866950, 2, '051c', 'adds', 'r5, r0, #0'),
 (134866952, 2, '0123', 'movs', 'r3, #1'),
 (134866954, 2, '9846', 'mov', 'r8, r3'),
 (134866956, 2, '1f1b', 'subs', 'r7, r3, r4'),
 (134866958, 2, '381c', 'adds', 'r0, r7, #0'),
 (134866960, 4, 'fff748ff', 'bl', '0x809e6a4'),
 (134866964, 2, '061c', 'adds', 'r6, r0, #0'),
 (134866966, 2, '002d', 'cmp', 'r5, #0'),
 (134866968, 2, '6cdb', 'blt.n', '0x809e8f4'),
 (134866970, 2, '002e', 'cmp', 'r6, #0'),
 (134866972, 2, '6adb', 'blt.n', '0x809e8f4'),
 (134866974, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866976, 2, '291c', 'adds', 'r1, r5, #0'),
 (134866978, 2, '0122', 'movs', 'r2, #1'),
 (134866980, 4, '96f7c4f8', 'bl', '0x80349b0'),
 (134866984, 2, '0028', 'cmp', 'r0, #0'),
 (134866986, 2, '63d0', 'beq.n', '0x809e8f4'),
 (134866988, 2, '4046', 'mov', 'r0, r8'),
 (134866990, 2, '0090', 'str', 'r0, [sp, #0]'),
 (134866992, 2, '201c', 'adds', 'r0, r4, #0'),
 (134866994, 2, '291c', 'adds', 'r1, r5, #0'),
 (134866996, 2, '3a1c', 'adds', 'r2, r7, #0'),
 (134866998, 2, '331c', 'adds', 'r3, r6, #0'),
 (134867000, 4, '96f73afd', 'bl', '0x80352b0'),
 (134867004, 2, '0028', 'cmp', 'r0, #0'),
 (134867006, 2, '59d0', 'beq.n', '0x809e8f4'),
 (134867008, 2, '0149', 'ldr', 'r1, [pc, #4]'),
 (134867010, 2, '024a', 'ldr', 'r2, [pc, #8]'),
 (134867012, 2, '8918', 'adds', 'r1, r1, r2'),
 (134867014, 2, '4ae0', 'b.n', '0x809e8de'),
 (134867024, 2, '064b', 'ldr', 'r3, [pc, #24]'),
 (134867026, 2, 'd018', 'adds', 'r0, r2, r3'),
 (134867028, 2, '0068', 'ldr', 'r0, [r0, #0]'),
 (134867030, 2, '0328', 'cmp', 'r0, #3'),
 (134867032, 2, '0cd1', 'bne.n', '0x809e874'),
 (134867034, 2, '0548', 'ldr', 'r0, [pc, #20]'),
 (134867036, 2, '1118', 'adds', 'r1, r2, r0'),
 (134867038, 2, '0120', 'movs', 'r0, #1'),
 (134867040, 2, '0860', 'str', 'r0, [r1, #0]'),
 (134867042, 2, '3433', 'adds', 'r3, #52'),
 (134867044, 2, 'd118', 'adds', 'r1, r2, r3'),
 (134867046, 2, '0020', 'movs', 'r0, #0'),
 (134867048, 2, '0860', 'str', 'r0, [r1, #0]'),
 (134867050, 2, '0ae0', 'b.n', '0x809e882'),
 (134867060, 2, '0449', 'ldr', 'r1, [pc, #16]'),
 (134867062, 2, '5018', 'adds', 'r0, r2, r1'),
 (134867064, 2, '0021', 'movs', 'r1, #0'),
 (134867066, 2, '0160', 'str', 'r1, [r0, #0]'),
 (134867068, 2, '034b', 'ldr', 'r3, [pc, #12]'),
 (134867070, 2, 'd018', 'adds', 'r0, r2, r3'),
 (134867072, 2, '0160', 'str', 'r1, [r0, #0]'),
 (134867074, 2, '0348', 'ldr', 'r0, [pc, #12]'),
 (134867076, 2, '1118', 'adds', 'r1, r2, r0'),
 (134867078, 2, '2ae0', 'b.n', '0x809e8de'),
 (134867092, 2, '201c', 'adds', 'r0, r4, #0'),
 (134867094, 4, 'fdf7ebfa', 'bl', '0x809be70'),
 (134867098, 2, '0028', 'cmp', 'r0, #0'),
 (134867100, 2, '22d0', 'beq.n', '0x809e8e4'),
 (134867102, 2, '0249', 'ldr', 'r1, [pc, #8]'),
 (134867104, 2, '024a', 'ldr', 'r2, [pc, #8]'),
 (134867106, 2, '8918', 'adds', 'r1, r1, r2'),
 (134867108, 2, '1be0', 'b.n', '0x809e8de'),
 (134867120, 2, '0d48', 'ldr', 'r0, [pc, #52]'),
 (134867122, 2, '0e4b', 'ldr', 'r3, [pc, #56]'),
 (134867124, 2, 'c018', 'adds', 'r0, r0, r3'),
 (134867126, 2, '0068', 'ldr', 'r0, [r0, #0]'),
 (134867128, 2, '0328', 'cmp', 'r0, #3'),
 (134867130, 2, '0dd0', 'beq.n', '0x809e8d8'),
 (134867132, 2, '011c', 'adds', 'r1, r0, #0'),
 (134867134, 2, '0c31', 'adds', 'r1, #12'),
 (134867136, 2, '002c', 'cmp', 'r4, #0'),
 (134867138, 2, '02d0', 'beq.n', '0x809e8ca'),
 (134867140, 2, '8020', 'movs', 'r0, #128'),
 (134867142, 2, '0002', 'lsls', 'r0, r0, #8'),
 (134867144, 2, '0143', 'orrs', 'r1, r0'),
 (134867146, 2, '0804', 'lsls', 'r0, r1, #16'),
 (134867148, 2, '000c', 'lsrs', 'r0, r0, #16'),
 (134867150, 2, '0021', 'movs', 'r1, #0'),
 (134867152, 2, '0022', 'movs', 'r2, #0'),
 (134867154, 2, '0023', 'movs', 'r3, #0'),
 (134867156, 4, '9df72afa', 'bl', '0x803bd2c'),
 (134867160, 2, '0349', 'ldr', 'r1, [pc, #12]'),
 (134867162, 2, '0548', 'ldr', 'r0, [pc, #20]'),
 (134867164, 2, '0918', 'adds', 'r1, r1, r0'),
 (134867166, 2, '0868', 'ldr', 'r0, [r1, #0]'),
 (134867168, 2, '0130', 'adds', 'r0, #1'),
 (134867170, 2, '0860', 'str', 'r0, [r1, #0]'),
 (134867172, 2, '0020', 'movs', 'r0, #0'),
 (134867174, 2, '06e0', 'b.n', '0x809e8f6')]

BODY_RANGES = [(134866676, 134866716),
 (134866764, 134866782),
 (134866796, 134866846),
 (134866864, 134866876),
 (134866884, 134866898),
 (134866904, 134866932),
 (134866944, 134867016),
 (134867024, 134867052),
 (134867060, 134867080),
 (134867092, 134867110),
 (134867120, 134867176),
 (134867188, 134867202)]

PADDING = [(134866782, 2, '0000'), (134866846, 2, '0000'), (134866898, 2, '0000'), (134867110, 2, '0000')]

NEW_POOLS = [134866784,
 134866788,
 134866792,
 134866848,
 134866852,
 134866856,
 134866860,
 134866876,
 134866880,
 134866900,
 134866932,
 134866936,
 134866940,
 134867016,
 134867020,
 134867052,
 134867056,
 134867080,
 134867084,
 134867088,
 134867112,
 134867116,
 134867176,
 134867180,
 134867184]

NEW_CALLS = [(134866798, 134428088, 'count_available_monster_slots', '94f723ff'),
 (134866808, 134462332, 'check_field_spell_neo_daedalus_group_placeable', '9df700fa'),
 (134866822, 134798000, 'dispatch_effect_handler_by_card_id', 'eff793f9'),
 (134866834, 134820752, 'trigger_card_display_op31_if_not_active', 'f4f7fdfd'),
 (134866892, 134824388, 'init_effect_slot_display_context', 'f5f7fafc'),
 (134866904, 134824668, 'get_monster_slot_entry_ptr', 'f5f780fd'),
 (134866920, 134921568, 'setup_equip_oam_entry_with_sprite_attr', '0df0bafa'),
 (134866946, 134866516, 'find_equip_slot_idx_with_entity_id_one', 'fff727ff'),
 (134866960, 134866596, 'find_equip_slot_idx_with_entity_id_zero', 'fff748ff'),
 (134866980, 134433200, 'check_slot_card_activatable', '96f7c4f8'),
 (134867000, 134435504, 'eval_slot_activation_eligibility_full', '96f73afd'),
 (134867094, 134856304, 'advance_equip_display_phase_via_table', 'fdf7ebfa'),
 (134867156, 134462764, 'enqueue_sprite_attr_record', '9df72afa')]

BRANCH_FLOWS = [(134866780, 134867166, 'jump', 'bfe0'),
 (134866804, 134866864, 'conditional', '1cd0'),
 (134866814, 134866864, 'conditional', '17d0'),
 (134866828, 134866864, 'conditional', '10d0'),
 (134866844, 134867166, 'jump', '9fe0'),
 (134866874, 134867172, 'jump', '93e0'),
 (134866896, 134867160, 'jump', '82e0'),
 (134866930, 134867166, 'jump', '74e0'),
 (134866968, 134867188, 'conditional', '6cdb'),
 (134866972, 134867188, 'conditional', '6adb'),
 (134866986, 134867188, 'conditional', '63d0'),
 (134867006, 134867188, 'conditional', '59d0'),
 (134867014, 134867166, 'jump', '4ae0'),
 (134867032, 134867060, 'conditional', '0cd1'),
 (134867050, 134867074, 'jump', '0ae0'),
 (134867078, 134867166, 'jump', '2ae0'),
 (134867100, 134867172, 'conditional', '22d0'),
 (134867108, 134867166, 'jump', '1be0'),
 (134867130, 134867160, 'conditional', '0dd0'),
 (134867138, 134867146, 'conditional', '02d0'),
 (134867174, 134867190, 'jump', '06e0')]

LITERAL_READS = [(134866764, 134866784, 1, 'READ', 'DEFAULT', True),
 (134866768, 134866788, 1, 'READ', 'DEFAULT', True),
 (134866776, 134866792, 1, 'READ', 'DEFAULT', True),
 (134866816, 134866848, 1, 'READ', 'DEFAULT', True),
 (134866830, 134866852, 1, 'READ', 'DEFAULT', True),
 (134866838, 134866856, 1, 'READ', 'DEFAULT', True),
 (134866840, 134866860, 1, 'READ', 'DEFAULT', True),
 (134866864, 134866876, 1, 'READ', 'DEFAULT', True),
 (134866866, 134866880, 1, 'READ', 'DEFAULT', True),
 (134866884, 134866900, 1, 'READ', 'DEFAULT', True),
 (134866910, 134866932, 1, 'READ', 'DEFAULT', True),
 (134866924, 134866936, 1, 'READ', 'DEFAULT', True),
 (134866926, 134866940, 1, 'READ', 'DEFAULT', True),
 (134867008, 134867016, 1, 'READ', 'DEFAULT', True),
 (134867010, 134867020, 1, 'READ', 'DEFAULT', True),
 (134867024, 134867052, 1, 'READ', 'DEFAULT', True),
 (134867034, 134867056, 1, 'READ', 'DEFAULT', True),
 (134867060, 134867080, 1, 'READ', 'DEFAULT', True),
 (134867068, 134867084, 1, 'READ', 'DEFAULT', True),
 (134867074, 134867088, 1, 'READ', 'DEFAULT', True),
 (134867102, 134867112, 1, 'READ', 'DEFAULT', True),
 (134867104, 134867116, 1, 'READ', 'DEFAULT', True),
 (134867120, 134867176, 1, 'READ', 'DEFAULT', True),
 (134867160, 134867176, 1, 'READ', 'DEFAULT', True),
 (134867122, 134867180, 1, 'READ', 'DEFAULT', True),
 (134867162, 134867184, 1, 'READ', 'DEFAULT', True)]

SWITCH_WORDS = [(134866732, 134866764, 'equip_activation_subphase_case0'),
 (134866736, 134866796, 'equip_activation_subphase_case1'),
 (134866740, 134866884, 'equip_activation_subphase_case2'),
 (134866744, 134866904, 'equip_activation_subphase_case3'),
 (134866748, 134866944, 'equip_activation_subphase_case4'),
 (134866752, 134867024, 'equip_activation_subphase_case5'),
 (134866756, 134867092, 'equip_activation_subphase_case6'),
 (134866760, 134867120, 'equip_activation_subphase_case7')]

MNEMONIC_DISPLAY_MAP = {'adds': 'add',
 'movs': 'mov',
 'b.n': 'b',
 'beq.n': 'beq',
 'blt.n': 'blt',
 'lsls': 'lsl',
 'subs': 'sub',
 'bne.n': 'bne',
 'orrs': 'orr',
 'lsrs': 'lsr'}

FROZEN_INPUTS = [('doc/dev/refine/F13-Seg-2.proposal.md', '60370c445976ffe021413cdea6410e9bce8e9ab134613e4a91dd193bfb03b8b4'),
 ('doc/dev/refine/F13-Seg-2.review.md', '2a757d6db38da4943ec3f84894f48130fb415326dd415f0329221c570bb3523a'),
 ('output/refine-run-20260831-194634/f13-seg2-plan.json',
  'b54987a1ad0cc564e5e6bfa3693b8e435d5700ace3e38f4d1facb7f5b1b4fd0a'),
 ('output/refine-run-20260831-194634/f13-seg2-plates.json',
  '2b1709da950ac59407c9e407869202f74e1825af130619ab50d7747299ca1d44'),
 ('output/refine-run-20260831-194634/f13-seg2-selfcheck.json',
  'aea62c60ee87219d8ff1bdaa9cdcbcf21ee086893791cec2925cf955e123531a'),
 ('output/refine-run-20260831-194634/f13-seg2-review-round2-diff.json',
  'f08eb251c16b9e0133e61bd2aa9de2105ecb7f08efb6ea927595e953de29e145'),
 ('output/refine-run-20260831-194634/root-f13-seg2-before-modeb.json',
  'f1e71507fd17f4fc67d6b19a545c32f74f1f8b4de18a736a43c3d4dd8fa27e88'),
 ('output/refine-run-20260831-194634/root-f13-seg2-all-slots-before.json',
  '76f1c508fa49b35ce1b1f65c909ea128c2204cfacf3177ead5101e7a02490308'),
 ('output/refine-run-20260831-194634/root-f13-seg2-disasm-targets-before.json',
  'a0f65a45626d93704f0b6ec25ea868185907b02e0b0c5393a91098c15d37dfe5'),
 ('output/refine-run-20260831-194634/root-f13-seg2-dispatch-code-before.json',
  '42b3628141ee21a7556c3e63f54466074c550139ab348fa4cf101327c2bfcb83'),
 ('output/refine-run-20260831-194634/root-f13-seg2-functions-before.json',
  '77fe64e2ca46a38f17ff256abf5985c8d511af6f9fd5215fce55ce8ab02a2b3f'),
 ('output/refine-run-20260831-194634/root-f13-seg2-callees-before.json',
  '65218f224ec9997522d183def7365d6fd5c88277feb89a37ae6039641090ec9b'),
 ('output/refine-run-20260831-194634/root-f13-seg2-targets-before.json',
  '806050903ea29829e627f974c12b75721ad177de76d2f03e08abe381b1bfae41'),
 ('output/refine-run-20260831-194634/root-f13-seg2-odd-pointers-before.json',
  '3d7e01f3cf57d9b2e18eb0a3350502b455d8a1369b2e60a75fbcc3130a39ac45')]

SEGMENT_RANGE_SHA256 = '46e20aba25cfd3417fcd388f095b0eb9fcd79b028c2786c6c72be69798bde64d'

import copy
import hashlib
import json
import os
from java.math import BigInteger
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import RefType, SourceType, SymbolType

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
ROOT = os.path.abspath(os.path.join(str(getSourceFile().getParentFile()), '..', '..'))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
memory = currentProgram.getMemory()
equates = currentProgram.getEquateTable()
context = currentProgram.getProgramContext()
tmode = context.getRegister('TMode')
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME', 'CASE_LABEL', 'CASE_EOL', 'DISASM', 'POOL_DATA'))


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def read_json(name):
    with open(os.path.join(RUN, name), 'rb') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def fail(message, actual=None, expected=None):
    FAILS.append(message)
    print('FAIL: ' + message)
    if actual is not None or expected is not None:
        print('DETAIL ' + json.dumps({'actual': actual, 'expected': expected}, ensure_ascii=True, sort_keys=True))


def require(condition, message):
    if not condition:
        fail(message)


def canonical(value):
    if isinstance(value, dict):
        value = dict((key, canonical(item)) for key, item in value.items() if key != 'input_label')
    elif isinstance(value, list):
        value = sorted((canonical(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    return value


def same(message, actual, expected):
    if canonical(actual) != canonical(expected):
        fail(message, actual, expected)


def basic_ref(ref):
    return {'from': str(ref.getFromAddress()), 'to': str(ref.getToAddress()),
            'operand': ref.getOperandIndex(), 'type': str(ref.getReferenceType()),
            'source': str(ref.getSource()), 'primary': bool(ref.isPrimary())}


def symbol_info(symbol, with_primary=True):
    if symbol is None:
        return None
    result = {'id': long(symbol.getID()), 'name': unicode(symbol.getName()),
              'qualified_name': unicode(symbol.getName(True)),
              'type': str(symbol.getSymbolType()), 'source': str(symbol.getSource())}
    if with_primary:
        result['primary'] = bool(symbol.isPrimary())
    return result


def describe(value):
    addr = toAddr(value)
    data = listing.getDefinedDataAt(addr)
    unit = listing.getCodeUnitContaining(addr)
    fn = getFunctionContaining(addr)
    result = {'address': value, 'symbols': [symbol_info(item) for item in symbols.getSymbols(addr)],
              'defined_data': None if data is None else {
                  'address': str(data.getAddress()), 'length': data.getLength(),
                  'type': unicode(data.getDataType().getPathName()),
                  'min': str(data.getMinAddress()), 'max': str(data.getMaxAddress())},
              'containing_code_unit': None if unit is None else {
                  'address': str(unit.getAddress()), 'length': unit.getLength(),
                  'class': str(unit.getClass().getSimpleName())},
              'instruction_at': None if getInstructionAt(addr) is None else str(getInstructionAt(addr)),
              'containing_function': None if fn is None else {
                  'entry': str(fn.getEntryPoint()), 'name': str(fn.getName()), 'body': str(fn.getBody())},
              'equates': [{'name': str(eq.getName()), 'value': long(eq.getValue())}
                          for eq in equates.getEquates(addr)],
              'comments': {}, 'rom_word': None, 'references_from': [], 'references_to': []}
    for key, kind in [('EOL', CodeUnit.EOL_COMMENT), ('PLATE', CodeUnit.PLATE_COMMENT)]:
        text = listing.getComment(kind, addr)
        result['comments'][key] = None if text is None else unicode(text)
    if 0x08000000 <= value <= 0x09fffffc:
        result['rom_word'] = memory.getInt(addr) & 0xffffffff
    for ref in references.getReferencesFrom(addr):
        item = basic_ref(ref)
        item['target_primary'] = symbol_info(symbols.getPrimarySymbol(ref.getToAddress()), False)
        result['references_from'].append(item)
    result['references_to'] = [basic_ref(ref) for ref in references.getReferencesTo(addr)]
    return result


def mode_at(value):
    mode = context.getValue(tmode, toAddr(value), False)
    return None if mode is None else int(mode)


def function_state(value, extended=False):
    fn = getFunctionAt(toAddr(value))
    if fn is None:
        return None
    symbol = fn.getSymbol()
    values, eols, body_refs = [], [], []
    iterator = fn.getBody().getAddresses(True)
    while iterator.hasNext():
        pos = iterator.next()
        values.append(chr(memory.getByte(pos) & 255))
        eol = listing.getComment(CodeUnit.EOL_COMMENT, pos)
        if eol is not None:
            eols.append([str(pos), unicode(eol)])
        body_refs.extend(basic_ref(ref) for ref in references.getReferencesFrom(pos))
    text = listing.getComment(CodeUnit.PLATE_COMMENT, fn.getEntryPoint())
    result = {'plate_chars': 0 if text is None else len(text),
              'incoming': [basic_ref(ref) for ref in references.getReferencesTo(fn.getEntryPoint())],
              'plate_sha256': None if text is None else hashlib.sha256(unicode(text).encode('utf8')).hexdigest(),
              'body_sha256': hashlib.sha256(''.join(values)).hexdigest(),
              'plate': None if text is None else unicode(text),
              'source': str(symbol.getSource()), 'body': str(fn.getBody()),
              'body_size': fn.getBody().getNumAddresses(), 'name': unicode(fn.getName()),
              'symbol_type': str(symbol.getSymbolType()), 'addr': value,
              'symbol_id': long(symbol.getID()), 'eols': eols}
    if extended:
        result['body_refs'] = body_refs
        result['prototype'] = unicode(fn.getPrototypeString(True, True))
    return result


def instruction_state(value):
    addr = toAddr(value)
    unit = listing.getCodeUnitAt(addr)
    ins = getInstructionAt(addr)
    fn = getFunctionContaining(addr)
    data = listing.getDefinedDataAt(addr)
    if unit is None:
        return None
    raw = ''.join('%02x' % (memory.getByte(addr.add(index)) & 255) for index in range(unit.getLength()))
    state = {'tmode': mode_at(value), 'address': value,
             'eol': None if listing.getComment(CodeUnit.EOL_COMMENT, addr) is None else unicode(listing.getComment(CodeUnit.EOL_COMMENT, addr)),
             'kind': str(unit.getClass().getSimpleName()), 'length': unit.getLength(),
             'references_to': [basic_ref(ref) for ref in references.getReferencesTo(addr)],
             'references_from': [basic_ref(ref) for ref in references.getReferencesFrom(addr)],
             'plate': None if listing.getComment(CodeUnit.PLATE_COMMENT, addr) is None else unicode(listing.getComment(CodeUnit.PLATE_COMMENT, addr)),
             'bytes': raw, 'instruction': None,
             'function': None if fn is None else str(fn.getEntryPoint()),
             'defined_data': None if data is None else unicode(data.getDataType().getPathName())}
    if ins is not None:
        state['instruction'] = {'operands': [unicode(ins.getDefaultOperandRepresentation(index)) for index in range(ins.getNumOperands())],
                                'flow_type': str(ins.getFlowType()),
                                'flows': [str(target) for target in ins.getFlows()],
                                'mnemonic': unicode(ins.getMnemonicString()).lower(),
                                'text': unicode(str(ins)),
                                'fallthrough': None if ins.getFallThrough() is None else str(ins.getFallThrough())}
    return state


def raw_hex(value, size):
    return ''.join('%02x' % (memory.getByte(toAddr(value + index)) & 255) for index in range(size))


def range_hash():
    values = ''.join(chr(memory.getByte(toAddr(value)) & 255) for value in range(0x0809e6f4, 0x0809f744))
    return hashlib.sha256(values).hexdigest()


PLAN = read_json('f13-seg2-plan.json')
ROOT_SLOTS = read_json('root-f13-seg2-all-slots-before.json')
ROOT_TARGETS = read_json('root-f13-seg2-targets-before.json')
ROOT_DISASM = read_json('root-f13-seg2-disasm-targets-before.json')
ROOT_CODE = read_json('root-f13-seg2-dispatch-code-before.json')
ROOT_FUNCTIONS = read_json('root-f13-seg2-functions-before.json')
ROOT_CALLEES = read_json('root-f13-seg2-callees-before.json')
ROOT_ODD = read_json('root-f13-seg2-odd-pointers-before.json')
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())
SLOTS = dict((row['addr'], row) for row in PLAN['actions'])
PLATE_MAP = dict((addr, text) for addr, name, text in PLATES)
EOL_MAP = dict(SLOT_EOLS)
RENAMES = dict((addr, new) for addr, old, new in FUNC_RENAME)
CASE_MAP = dict((addr, (label, text)) for addr, label, text in CASE_LABELS)
NEW_POOL_SET = set(NEW_POOLS)
INSTRUCTION_MAP = dict((row[0], row) for row in DISASM_INSTRUCTIONS)
ROM_TARGETS_BY_ADDRESS = {}
for _target_source in (ROOT_SLOTS['slots'], ROOT_TARGETS['extra_targets'], ROOT_DISASM['extra_targets']):
    for _target_state in _target_source:
        _target_addr = _target_state['address']
        _target_core = copy.deepcopy(_target_state)
        _target_core.pop('input_label', None)
        if _target_addr in ROM_TARGETS_BY_ADDRESS:
            _old_core = copy.deepcopy(ROM_TARGETS_BY_ADDRESS[_target_addr])
            _old_core.pop('input_label', None)
            if canonical(_old_core) != canonical(_target_core):
                raise RuntimeError('Conflicting ROM target snapshots at %08x' % _target_addr)
        else:
            ROM_TARGETS_BY_ADDRESS[_target_addr] = _target_state


def verify_frozen_and_tables():
    for relative, digest in FROZEN_INPUTS:
        same('INPUT_HASH ' + relative, file_hash(os.path.join(ROOT, relative)), digest)
    same('TABLE_EQ', [list(row) for row in EQ_SLOTS], [row['tuple'] for row in PLAN['actions'] if row['action'] == 'EQ'])
    same('TABLE_REF', [list(row) for row in REF_SLOTS], [row['tuple'] for row in PLAN['actions'] if row['action'] == 'REF'])
    same('TABLE_RENAME', [list(row) for row in RENAME_SLOTS], [row['tuple'] for row in PLAN['actions'] if row['action'] == 'RENAME'])
    same('TABLE_PLATES', [list(row) for row in PLATES], [[row['addr'], row['name'], row['new_text']] for row in PLAN['plates']])
    same('TABLE_SLOT_EOLS', [list(row) for row in SLOT_EOLS], [[row['addr'], row['eol']] for row in PLAN['actions']])
    same('TABLE_FUNC_RENAME', [list(row) for row in FUNC_RENAME], [[row['addr'], row['old'], row['new']] for row in PLAN['function_renames']])
    same('TABLE_CASE_LABELS', [list(row) for row in CASE_LABELS], [[row['addr'], row['label'], row['eol']] for row in PLAN['case_labels']])
    same('TABLE_DISASM', [list(row) for row in DISASM_INSTRUCTIONS],
         [[row['addr'], row['size'], row['hex'], row['mnemonic'], row['operands']] for row in PLAN['disasm']['instructions']])
    same('TABLE_BODY_RANGES', [list(row) for row in BODY_RANGES], PLAN['disasm']['new_body_half_open'])
    same('COUNTS', [len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATES), len(SLOT_EOLS), len(FUNC_RENAME), len(CASE_LABELS), len(DISASM_INSTRUCTIONS)],
         [119, 20, 19, 59, 158, 4, 8, 145])
    require(len(SLOTS) == 158 and len(set(SLOTS)) == 158 and set(EOL_MAP) == set(SLOTS), 'SLOT_UNION')
    require(len(NEW_POOLS) == 25 and len(PADDING) == 4 and len(NEW_CALLS) == 13 and len(BRANCH_FLOWS) == 21 and len(LITERAL_READS) == 26, 'STRUCTURE_COUNTS')
    same('MNEMONIC_DISPLAY_MAP_EXACT', MNEMONIC_DISPLAY_MAP,
         {'adds': 'add', 'movs': 'mov', 'b.n': 'b', 'beq.n': 'beq', 'blt.n': 'blt',
          'lsls': 'lsl', 'subs': 'sub', 'bne.n': 'bne', 'orrs': 'orr', 'lsrs': 'lsr'})
    require(0x0809e72c in ROM_TARGETS_BY_ADDRESS and len(ROM_TARGETS_BY_ADDRESS) == len(set(ROM_TARGETS_BY_ADDRESS)), 'ROM_TARGET_ADDRESS_MAP')
    require(PLAN['carve'] == [] and PLAN['section_5_1'] == [] and PLAN['function_count_delta'] == 0, 'NO_CARVE_NO_FUNCTION_DELTA')
    for addr, name, text in PLATES:
        require(text and len(text) <= 500 and all(ord(ch) < 128 for ch in text), 'PLATE_ASCII %08x' % addr)
    for addr, text in SLOT_EOLS:
        require(all(ord(ch) < 128 for ch in text), 'SLOT_EOL_ASCII %08x' % addr)
    for addr, label, text in CASE_LABELS:
        require(all(ord(ch) < 128 for ch in text), 'CASE_EOL_ASCII %08x' % addr)


def verify_name_available(name, value, post=False):
    matches = list(symbols.getGlobalSymbols(name))
    require(all(item.getAddress() == toAddr(value) for item in matches), 'NAME_COLLISION ' + name)
    if post:
        require(len(matches) == 1, 'NAME_EXACT_ONE ' + name)


def verify_prestate():
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_PRE')
    same('SEGMENT_RANGE_SHA', range_hash(), SEGMENT_RANGE_SHA256)
    observed_slots = dict((item['address'], item) for item in ROOT_SLOTS['slots'])
    same('ROOT_SLOT_ADDRESSES', set(observed_slots), set(SLOTS))
    for value, row in SLOTS.items():
        same('SLOT_PLAN_BEFORE %08x' % value, row['before'], observed_slots[value])
        same('SLOT_DB_BEFORE %08x' % value, describe(value), row['before'])
        same('SLOT_ROM_VALUE %08x' % value, memory.getInt(toAddr(value)) & 0xffffffff, row['value'])
        verify_name_available(row['slot_label'], value, False)
    for source in (ROOT_TARGETS['extra_targets'], ROOT_DISASM['extra_targets'], ROOT_ODD['extra_targets']):
        for expected in source:
            same('TARGET_DB_BEFORE %08x' % expected['address'], describe(expected['address']), expected)
    root_functions = dict((item['addr'], item) for item in ROOT_FUNCTIONS['functions'])
    root_callees = dict((item['addr'], item) for item in ROOT_CALLEES['functions'])
    require(len(root_functions) == 59 and len(root_callees) == 13, 'FUNCTION_GUARD_COUNTS')
    for value, expected in root_functions.items():
        same('FUNCTION_BEFORE %08x' % value, function_state(value, False), expected)
    for value, expected in root_callees.items():
        same('CALLEE_BEFORE %08x' % value, function_state(value, False), expected)
    actual_units = [instruction_state(item['address']) for item in ROOT_CODE['units']]
    same('DISPATCH_CODE_BEFORE', actual_units, ROOT_CODE['units'])
    require(ROOT_CODE['function_count'] == 5209 and ROOT_CODE['byte_count'] == 528 and len(ROOT_CODE['units']) == 465, 'ROOT_CODE_BOUND')
    for addr, size, raw, mnemonic, operands in DISASM_INSTRUCTIONS:
        same('DISASM_RAW %08x' % addr, raw_hex(addr, size), raw)
        require(getInstructionAt(toAddr(addr)) is None and getFunctionContaining(toAddr(addr)) is None, 'DISASM_PRE_UNDEFINED %08x' % addr)
        require(listing.getDefinedDataAt(toAddr(addr)) is None, 'DISASM_PRE_NO_DATA %08x' % addr)
        unit = listing.getCodeUnitContaining(toAddr(addr))
        require(unit is not None and unit.getLength() == 1 and str(unit.getClass().getSimpleName()) == 'DataDB', 'DISASM_PRE_UNIT1 %08x' % addr)
        require(mode_at(addr) == 0, 'DISASM_PRE_TMODE0 %08x' % addr)
    for addr, size, raw in PADDING:
        same('PAD_RAW %08x' % addr, raw_hex(addr, size), raw)
        for value in range(addr, addr + size):
            state = describe(value)
            require(state['defined_data'] is None and state['instruction_at'] is None and state['symbols'] == [] and state['references_from'] == [] and state['references_to'] == [], 'PAD_PRE_EMPTY %08x' % value)
            require(state['containing_code_unit']['length'] == 1 and mode_at(value) == 0, 'PAD_PRE_UNIT1 %08x' % value)
    mov = getInstructionAt(toAddr(0x0809e71a))
    require(mov is not None and raw_hex(0x0809e71a, 2) == '8746' and [str(x) for x in mov.getFlows()] == [] and list(references.getReferencesFrom(toAddr(0x0809e71a))) == [] and mov.getFallThrough() is None, 'MOV_PC_PRE_EMPTY')
    for addr, value, label in SWITCH_WORDS:
        require(value % 2 == 0 and memory.getInt(toAddr(addr)) & 0xffffffff == value, 'SWITCH_WORD_PRE %08x' % addr)
    for addr, value, name, label in EQ_SLOTS:
        eq = equates.getEquate(name)
        require(eq is None or (eq.getValue() & 0xffffffff) == value, 'EQUATE_VALUE_PRE ' + name)
        if addr in NEW_POOL_SET:
            require(eq is None if next(row for row in PLAN['actions'] if row['addr'] == addr)['reuse'] == 'NEW' else True, 'NEW_EQUATE_ABSENT ' + name)
    for value, old, new in FUNC_RENAME:
        verify_name_available(new, value, False)
    # Three odd raw pointers have deliberately different metadata contracts.
    odd = dict((item['address'], item) for item in ROOT_ODD['extra_targets'])
    ref477 = [dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary')) for ref in odd[0x09e477c0]['references_from']]
    same('ODD_477C0_REF_BODY', ref477, [{'from': '09e477c0', 'to': '0809ec35', 'operand': 0, 'type': 'DATA', 'source': 'DEFAULT', 'primary': True}])
    for value, target in ((0x09e4788c, 0x0809f1fd), (0x09e47890, 0x0809f20d)):
        state = odd[value]
        require(state['rom_word'] == target and state['defined_data'] is None and state['symbols'] == [] and state['references_from'] == [] and state['references_to'] == [] and state['containing_code_unit']['length'] == 1, 'ODD_WRAPPER_EMPTY %08x' % value)
    print('PREFLIGHT slots=158 EQ=119 REF=20 RENAME=19 PLATE=59 EOL=158 FUNC_RENAME=4 CASE=8 DISASM=145 POOL=25 PAD_BYTES=8 FUNCTIONS=59 CALLEES=13 FAIL=%d' % len(FAILS))


def ensure_user_label(value, name, allowed_old):
    addr = toAddr(value)
    matches = [item for item in symbols.getSymbols(addr) if item.getName() == name and str(item.getSource()) == 'USER_DEFINED' and item.getSymbolType() == SymbolType.LABEL]
    if len(matches) > 1:
        raise RuntimeError('Duplicate USER label %s' % name)
    label = matches[0] if matches else symbols.createLabel(addr, name, SourceType.USER_DEFINED)
    label.setPrimary()
    allowed = dict((long(item['id']), item) for item in allowed_old)
    for old in list(symbols.getSymbols(addr)):
        if old.getID() == label.getID():
            continue
        expected = allowed.get(long(old.getID()))
        if expected is not None and expected['name'] == old.getName() and expected['source'] == str(old.getSource()) and expected['type'] == str(old.getSymbolType()):
            old.delete()
        else:
            raise RuntimeError('Unexpected alias at %08x: %s' % (value, old))
    return label


def apply_ref(row):
    value, target = row['addr'], row['value']
    if 0x08000000 <= target < 0x0a000000:
        expected = ROM_TARGETS_BY_ADDRESS.get(target)
        if expected is None:
            raise RuntimeError('Missing frozen ROM target at %08x' % target)
        ensure_user_label(target, row['target_label'], expected['symbols'])
    else:
        target_symbol = symbols.getPrimarySymbol(toAddr(target))
        if target_symbol is None or target_symbol.getName() != row['target_label'] or str(target_symbol.getSource()) != 'USER_DEFINED':
            raise RuntimeError('RAM target mismatch %08x' % target)
    for old in list(references.getReferencesFrom(toAddr(value))):
        if old.getOperandIndex() == 0 and old.getToAddress() == toAddr(target):
            references.delete(old)
    ref = references.addMemoryReference(toAddr(value), toAddr(target), RefType.DATA, SourceType.USER_DEFINED, 0)
    references.setPrimary(ref, True)


def disassemble_one(row):
    addr, size, raw, mnemonic, operands = row
    context.setValue(tmode, toAddr(addr), toAddr(addr + size - 1), BigInteger.ONE)
    command = DisassembleCommand(toAddr(addr), AddressSet(toAddr(addr), toAddr(addr + size - 1)), False)
    command.enableCodeAnalysis(False)
    if not command.applyTo(currentProgram, monitor):
        raise RuntimeError('DISASM_COMMAND %08x %s' % (addr, command.getStatusMsg()))
    result = command.getDisassembledAddressSet()
    if result.getNumAddresses() != size or str(result.getMinAddress()) != '%08x' % addr or str(result.getMaxAddress()) != '%08x' % (addr + size - 1):
        raise RuntimeError('DISASM_RANGE %08x %s' % (addr, result))


def apply_slot(row):
    addr = row['addr']
    if addr in NEW_POOL_SET:
        created = createData(toAddr(addr), DWordDataType.dataType)
        if created is None or created.getLength() != 4 or unicode(created.getDataType().getPathName()) != '/dword':
            raise RuntimeError('POOL_DATA %08x' % addr)
        COUNTS['POOL_DATA'] += 1
    if row['action'] == 'EQ':
        eq = equates.getEquate(row['constant'])
        if eq is None:
            eq = equates.createEquate(row['constant'], row['value'])
        eq.addReference(toAddr(addr), 0)
    elif row['action'] == 'REF':
        apply_ref(row)
    elif row['action'] != 'RENAME':
        raise RuntimeError('Unknown action at %08x' % addr)
    ensure_user_label(addr, row['slot_label'], row['before']['symbols'])
    listing.setComment(toAddr(addr), CodeUnit.EOL_COMMENT, row['eol'])
    COUNTS[row['action']] += 1
    COUNTS['EOL'] += 1


def set_dispatch_body():
    fn = getFunctionAt(toAddr(0x0809e6f4))
    if fn is None or fn.getSymbol().getID() != 16934:
        raise RuntimeError('Dispatcher identity')
    body = AddressSet()
    for lo, hi in BODY_RANGES:
        body.addRange(toAddr(lo), toAddr(hi - 1))
    fn.setBody(body)


def apply_all():
    events = []
    events.extend((addr, 0, 'PLATE') for addr, name, text in PLATES)
    events.extend((addr, 1, 'DISASM') for addr, size, raw, mnemonic, operands in DISASM_INSTRUCTIONS)
    events.extend((addr, 2, 'CASE') for addr, label, text in CASE_LABELS)
    events.extend((addr, 3, 'SLOT') for addr in SLOTS)
    for addr, order, kind in sorted(events):
        if kind == 'PLATE':
            if addr in RENAMES:
                getFunctionAt(toAddr(addr)).setName(RENAMES[addr], SourceType.USER_DEFINED)
                COUNTS['FUNC_RENAME'] += 1
            listing.setComment(toAddr(addr), CodeUnit.PLATE_COMMENT, PLATE_MAP[addr])
            COUNTS['PLATE'] += 1
        elif kind == 'DISASM':
            disassemble_one(INSTRUCTION_MAP[addr])
            COUNTS['DISASM'] += 1
        elif kind == 'CASE':
            label, text = CASE_MAP[addr]
            expected = next(item for item in ROOT_DISASM['extra_targets'] if item['address'] == addr)
            ensure_user_label(addr, label, expected['symbols'])
            listing.setComment(toAddr(addr), CodeUnit.EOL_COMMENT, text)
            COUNTS['CASE_LABEL'] += 1
            COUNTS['CASE_EOL'] += 1
        elif kind == 'SLOT':
            apply_slot(SLOTS[addr])
    set_dispatch_body()


def planned_ref(value, target, operand, ref_type, source='DEFAULT', primary=True):
    return {'from': '%08x' % value, 'to': '%08x' % target, 'operand': operand,
            'type': ref_type, 'source': source, 'primary': primary}


def verify_post(before):
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_POST')
    same('SEGMENT_RANGE_SHA_POST', range_hash(), SEGMENT_RANGE_SHA256)
    for addr, size, raw, mnemonic, operands in DISASM_INSTRUCTIONS:
        ins = getInstructionAt(toAddr(addr))
        require(ins is not None and ins.getLength() == size, 'DISASM_POST %08x' % addr)
        same('DISASM_BYTES_POST %08x' % addr, raw_hex(addr, size), raw)
        same('DISASM_MNEMONIC_POST %08x' % addr, unicode(ins.getMnemonicString()).lower(),
             MNEMONIC_DISPLAY_MAP.get(mnemonic, mnemonic))
        require(mode_at(addr) == 1 and getFunctionContaining(toAddr(addr)).getEntryPoint() == toAddr(0x0809e6f4), 'DISASM_OWNER_TMODE %08x' % addr)
        require(getFunctionAt(toAddr(addr)) is None, 'NO_CASE_FUNCTION %08x' % addr)
    for addr, size, raw in PADDING:
        same('PAD_BYTES_POST %08x' % addr, raw_hex(addr, size), raw)
        for value in range(addr, addr + size):
            state = describe(value)
            require(state['defined_data'] is None and state['instruction_at'] is None and state['symbols'] == [] and state['references_from'] == [] and state['references_to'] == [], 'PAD_POST_EMPTY %08x' % value)
            require(state['containing_code_unit']['length'] == 1 and mode_at(value) == 0, 'PAD_POST_UNIT1 %08x' % value)
    expected_refs = {}
    for addr, target, operand, ref_type, source, primary in LITERAL_READS:
        expected_refs.setdefault(addr, []).append(planned_ref(addr, target, operand, ref_type, source, primary))
    for addr, target, name, raw in NEW_CALLS:
        expected_refs.setdefault(addr, []).append(planned_ref(addr, target, 0, 'UNCONDITIONAL_CALL'))
    for addr, target, kind, raw in BRANCH_FLOWS:
        ref_type = 'CONDITIONAL_JUMP' if kind == 'conditional' else 'UNCONDITIONAL_JUMP'
        expected_refs.setdefault(addr, []).append(planned_ref(addr, target, 0, ref_type))
    for addr, refs in expected_refs.items():
        same('NEW_INSTRUCTION_REFS %08x' % addr, [basic_ref(ref) for ref in references.getReferencesFrom(toAddr(addr))], refs)
    mov = getInstructionAt(toAddr(0x0809e71a))
    require(mov is not None and [str(x) for x in mov.getFlows()] == [] and list(references.getReferencesFrom(toAddr(0x0809e71a))) == [] and mov.getFallThrough() is None, 'MOV_PC_POST_EMPTY')
    for addr, target, kind, raw in BRANCH_FLOWS:
        ins = getInstructionAt(toAddr(addr))
        same('BRANCH_FLOW_POST %08x' % addr, [str(x) for x in ins.getFlows()], ['%08x' % target])
    for addr, target, name, raw in NEW_CALLS:
        ins = getInstructionAt(toAddr(addr))
        same('CALL_FLOW_POST %08x' % addr, [str(x) for x in ins.getFlows()], ['%08x' % target])
    for value, row in SLOTS.items():
        state = describe(value)
        same('SLOT_VALUE_POST %08x' % value, state['rom_word'], row['value'])
        require(state['comments']['EOL'] == row['eol'], 'SLOT_EOL_POST %08x' % value)
        verify_name_available(row['slot_label'], value, True)
        if value in NEW_POOL_SET:
            require(state['defined_data'] is not None and state['defined_data']['type'] == '/dword' and state['defined_data']['length'] == 4, 'POOL_DATA_POST %08x' % value)
        else:
            same('OLD_DATA_TYPE_POST %08x' % value, state['defined_data'], row['before']['defined_data'])
        if row['action'] == 'EQ':
            eq = equates.getEquate(row['constant'])
            require(eq is not None and (eq.getValue() & 0xffffffff) == row['value'], 'EQUATE_POST %08x' % value)
            refs = [ref for ref in eq.getReferences() if ref.getAddress() == toAddr(value) and ref.getOpIndex() == 0]
            require(len(refs) == 1, 'EQUATE_REF_POST %08x' % value)
            same('EQ_DATA_REFS_POST %08x' % value, state['references_from'], row['before']['references_from'])
        elif row['action'] == 'REF':
            expected = [copy.deepcopy(ref) for ref in row['before']['references_from'] if not (ref['operand'] == 0 and ref['to'] == '%08x' % row['value'])]
            expected.append(planned_ref(value, row['value'], 0, 'DATA', 'USER_DEFINED', True))
            actual = [dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary')) for ref in state['references_from']]
            same('REF_BODY_POST %08x' % value, actual, expected)
        else:
            actual = [dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary')) for ref in state['references_from']]
            expected = [dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary')) for ref in row['before']['references_from']]
            same('RENAME_REF_BODY_POST %08x' % value, actual, expected)
    for addr, label, text in CASE_LABELS:
        verify_name_available(label, addr, True)
        require(listing.getComment(CodeUnit.EOL_COMMENT, toAddr(addr)) == text, 'CASE_EOL_POST %08x' % addr)
    dispatcher = getFunctionAt(toAddr(0x0809e6f4))
    same('DISPATCH_BODY_POST', str(dispatcher.getBody()), '[' + ' '.join('[%08x, %08x]' % (lo, hi - 1) for lo, hi in BODY_RANGES) + ']')
    require(dispatcher.getBody().getNumAddresses() == 370 and dispatcher.getSymbol().getID() == 16934, 'DISPATCH_ID_SIZE_POST')
    root_functions = dict((item['addr'], item) for item in ROOT_FUNCTIONS['functions'])
    before_functions = dict((item['addr'], item) for item in before['functions'])
    for value, old in root_functions.items():
        actual = function_state(value, True)
        require(actual['symbol_id'] == old['symbol_id'] and actual['source'] == old['source'] and actual['symbol_type'] == old['symbol_type'], 'FUNCTION_ID_POST %08x' % value)
        require(actual['name'] == RENAMES.get(value, old['name']), 'FUNCTION_NAME_POST %08x' % value)
        require(actual['plate'] == PLATE_MAP[value], 'FUNCTION_PLATE_POST %08x' % value)
        expected_prototype = before_functions[value]['prototype']
        if value in RENAMES:
            require(expected_prototype.count(old['name']) == 1, 'FUNCTION_PROTOTYPE_OLD_NAME_ONCE %08x' % value)
            expected_prototype = expected_prototype.replace(old['name'], RENAMES[value], 1)
        same('FUNCTION_PROTOTYPE_POST %08x' % value, actual['prototype'], expected_prototype)
        if value == 0x0809e6f4:
            require(actual['body_size'] == 370 and actual['body'] == str(dispatcher.getBody()), 'DISPATCH_BODY_STATE')
            same('DISPATCH_EOLS_POST', actual['eols'], [['%08x' % addr, text] for addr, label, text in CASE_LABELS])
        else:
            require(actual['body'] == old['body'] and actual['body_size'] == old['body_size'] and actual['body_sha256'] == old['body_sha256'], 'FUNCTION_BODY_POST %08x' % value)
            same('FUNCTION_EOLS_POST %08x' % value, actual['eols'], old['eols'])
            same('FUNCTION_BODY_REFS_POST %08x' % value, actual['body_refs'], before_functions[value]['body_refs'])
        same('FUNCTION_INCOMING_POST %08x' % value, actual['incoming'], old['incoming'])
    before_callees = dict((item['addr'], item) for item in before['callees'])
    call_by_target = dict((target, addr) for addr, target, name, raw in NEW_CALLS)
    for old in ROOT_CALLEES['functions']:
        actual = function_state(old['addr'], True)
        expected_incoming = copy.deepcopy(old['incoming'])
        expected_incoming.append(planned_ref(call_by_target[old['addr']], old['addr'], 0, 'UNCONDITIONAL_CALL'))
        same('CALLEE_INCOMING_POST %08x' % old['addr'], actual['incoming'], expected_incoming)
        for key in ('symbol_id', 'name', 'body', 'body_size', 'body_sha256', 'plate', 'plate_sha256', 'eols', 'source', 'symbol_type'):
            same('CALLEE_%s_POST %08x' % (key, old['addr']), actual[key], old[key])
        require(actual['prototype'] == before_callees[old['addr']]['prototype'], 'CALLEE_PROTOTYPE_POST %08x' % old['addr'])
    odd_now = dict((item['address'], describe(item['address'])) for item in ROOT_ODD['extra_targets'])
    odd_old = dict((item['address'], item) for item in ROOT_ODD['extra_targets'])
    for value in (0x09e477c0, 0x09e4788c, 0x09e47890):
        require(odd_now[value]['rom_word'] == odd_old[value]['rom_word'], 'ODD_VALUE_POST %08x' % value)
    ref_body = lambda refs: [dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary')) for ref in refs]
    same('ODD_477C0_REF_BODY_POST', ref_body(odd_now[0x09e477c0]['references_from']), ref_body(odd_old[0x09e477c0]['references_from']))
    same('ODD_477C0_DATA_POST', odd_now[0x09e477c0]['defined_data'], odd_old[0x09e477c0]['defined_data'])
    for value in (0x09e4788c, 0x09e47890):
        state = odd_now[value]
        require(state['defined_data'] is None and state['symbols'] == [] and state['references_from'] == [] and state['references_to'] == [] and state['containing_code_unit']['length'] == 1, 'ODD_EMPTY_POST %08x' % value)
    # Original 27 dispatcher instructions retain bytes, instruction semantics and reference bodies.
    old_ranges = ((0x0809e6f4, 0x0809e71c), (0x0809e8f4, 0x0809e902))
    for expected in ROOT_CODE['units']:
        value = expected['address']
        if expected['kind'] == 'InstructionDB' and any(lo <= value < hi for lo, hi in old_ranges):
            actual = instruction_state(value)
            approved_incoming = [planned_ref(addr, target, 0,
                                  'CONDITIONAL_JUMP' if kind == 'conditional' else 'UNCONDITIONAL_JUMP')
                                 for addr, target, kind, raw in BRANCH_FLOWS if target == value]
            for key in ('tmode', 'address', 'eol', 'kind', 'length', 'references_to', 'references_from', 'bytes', 'instruction', 'function', 'defined_data'):
                expected_value = expected[key] + approved_incoming if key == 'references_to' else expected[key]
                same('ORIGINAL_INSTRUCTION_%s_POST %08x' % (key, value), actual[key], expected_value)
    approved_old_targets = [(target, len([1 for addr, candidate, kind, raw in BRANCH_FLOWS if candidate == target]))
                            for target in (0x0809e8f4, 0x0809e8f6)]
    same('ORIGINAL_INSTRUCTION_APPROVED_INCOMING_COUNTS', approved_old_targets,
         [(0x0809e8f4, 4), (0x0809e8f6, 1)])
    print('POSTCHECK slots=158 EQ=119 REF=20 RENAME=19 PLATE=59 EOL=158 FUNC_RENAME=4 CASE=8 DISASM=145 POOL=25 PAD_BYTES=8 FUNCTIONS=59 CALLEES=13 FAIL=%d' % len(FAILS))


def capture():
    addresses = set(SLOTS)
    for source in (ROOT_TARGETS['extra_targets'], ROOT_DISASM['extra_targets'], ROOT_ODD['extra_targets']):
        addresses.update(item['address'] for item in source)
    for addr, size, raw in PADDING:
        addresses.update(range(addr, addr + size))
    functions = [function_state(item['addr'], True) for item in ROOT_FUNCTIONS['functions']]
    callees = [function_state(item['addr'], True) for item in ROOT_CALLEES['functions']]
    units = [instruction_state(item['address']) for item in ROOT_CODE['units']]
    return {'script_sha256': SCRIPT_HASH, 'function_count': currentProgram.getFunctionManager().getFunctionCount(),
            'range_sha256': range_hash(), 'addresses': [describe(value) for value in sorted(addresses)],
            'functions': functions, 'callees': callees, 'dispatch_units': units}


def reject(phase):
    if FAILS:
        write_json('f13-seg2-%s-failures.json' % MODE, {'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


print('=== RefineF13Seg2 mode=%s ===' % MODE)
verify_frozen_and_tables()
reject('FROZEN_TABLES')
if MODE == 'check':
    receipt = read_json('f13-seg2-apply-receipt.json')
    require(receipt['script_sha256'] == SCRIPT_HASH, 'PERSISTED_SCRIPT_HASH')
    require(receipt['input_hashes'] == [list(row) for row in FROZEN_INPUTS], 'PERSISTED_INPUT_HASHES')
    state = capture()
    verify_post(receipt['before'])
    require(canonical(state) == canonical(receipt['after']), 'PERSISTED_EXACT_POST_STATE')
    reject('PERSISTED_CHECK')
    COUNTS = receipt['counts']
    write_json('f13-seg2-persisted-check.json', {'status': 'PERSISTED_CHECK_OK', 'FAIL': 0,
               'script_sha256': SCRIPT_HASH, 'counts': COUNTS, 'exact_saved_state': True})
else:
    verify_prestate()
    reject('PREFLIGHT')
    before = capture()
    if MODE == 'dry':
        write_json('f13-seg2-dry-state.json', before)
        COUNTS.update({'EQ': 119, 'REF': 20, 'RENAME': 19, 'PLATE': 59, 'EOL': 158,
                       'FUNC_RENAME': 4, 'CASE_LABEL': 8, 'CASE_EOL': 8, 'DISASM': 145, 'POOL_DATA': 25})
        write_json('f13-seg2-dry-check.json', {'status': 'DRY_PREFLIGHT_OK', 'FAIL': 0,
                   'script_sha256': SCRIPT_HASH, 'input_hashes': FROZEN_INPUTS, 'counts': COUNTS,
                   'address_count': len(before['addresses']), 'function_count': len(before['functions']),
                   'callee_count': len(before['callees']), 'dispatch_unit_count': len(before['dispatch_units']),
                   'complete_state': 'f13-seg2-dry-state.json'})
    else:
        write_json('f13-seg2-apply-before.json', before)
        transaction = currentProgram.startTransaction('Refine F13-Seg-2 final PASS actions')
        success = False
        after = None
        try:
            apply_all()
            verify_post(before)
            reject('POSTCHECK')
            after = capture()
            success = True
        finally:
            currentProgram.endTransaction(transaction, success)
        write_json('f13-seg2-apply-receipt.json', {'status': 'APPLIED_TRANSACTION_POSTCHECK_OK',
                   'FAIL': 0, 'script_sha256': SCRIPT_HASH, 'input_hashes': FROZEN_INPUTS,
                   'counts': COUNTS, 'before': before, 'after': after})
reject('FINAL')
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME', 'CASE_LABEL', 'CASE_EOL', 'DISASM', 'POOL_DATA')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
