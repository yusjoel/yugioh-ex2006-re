# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F13-Seg-3 final PASS materialization. Dry/check must use direct -noanalysis -readOnly.
# No data creation, disassembly, memory writes, or function creation.

EQ_SLOTS = [(134871008, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9f7e0'),
 (134871012, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9f7e4'),
 (134871016, 5433, 'MIRAGE_OF_NIGHTMARE_CID', 'mirage_of_nightmare_cid_9f7e8'),
 (134871112, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9f848'),
 (134871144, 4738, 'EQUIP_ACTIVATION_UNMAPPED_CID_1282', 'equip_activation_unmapped_cid_1282_9f868'),
 (134871160, 4586, 'EQUIP_ACTIVATION_UNMAPPED_CID_11EA', 'equip_activation_unmapped_cid_11ea_9f878'),
 (134871176, 5518, 'A_MAN_WITH_WDJAT_CID', 'a_man_with_wdjat_cid_9f888'),
 (134871192, 4423, 'EQUIP_ACTIVATION_UNMAPPED_CID_1147', 'equip_activation_unmapped_cid_1147_9f898'),
 (134871232, 5772, 'VILEPAWN_ARCHFIEND_CID', 'vilepawn_archfiend_cid_9f8c0'),
 (134871236, 4993, 'MIRROR_WALL_CID', 'mirror_wall_cid_9f8c4'),
 (134871256, 5113, 'FAIRY_BOX_CID', 'fairy_box_cid_9f8d8'),
 (134871268, 5689, 'TOKEN_1639_CID', 'token_1639_cid_9f8e4'),
 (134871292, 5775, 'DESROOK_ARCHFIEND_CID', 'desrook_archfiend_cid_9f8fc'),
 (134871316, 5777, 'TERRORKING_ARCHFIEND_CID', 'terrorking_archfiend_cid_9f914'),
 (134871420, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_9f97c'),
 (134871424, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9f980'),
 (134871488, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_9f9c0'),
 (134871624, 4294966632, 'EQUIP_PHASE_FRAME_ALLOC_NEG_0X298', 'equip_phase_frame_alloc_neg_0x298_9fa48'),
 (134871632, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_9fa50'),
 (134871636, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9fa54'),
 (134871640, 4990, 'SOLOMONS_LAWBOOK_CID', 'solomons_lawbook_cid_9fa58'),
 (134871644, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_9fa5c'),
 (134871784, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_9fae8'),
 (134871836, 32781, 'OAM_EQUIP_SPRITE_P2_0D', 'oam_equip_sprite_p2_0d_9fb1c'),
 (134871840, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9fb20'),
 (134871952, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9fb90'),
 (134871956, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_9fb94'),
 (134872020, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_9fbd4'),
 (134872180, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9fc74'),
 (134872188, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9fc7c'),
 (134872228, 5108, 'MASK_OF_BRUTALITY_CID', 'mask_of_brutality_cid_9fca4'),
 (134872260, 5194, 'EQUIP_ACTIVATION_UNMAPPED_CID_144A', 'equip_activation_unmapped_cid_144a_9fcc4'),
 (134872280, 5659, 'ARMOR_EXE_CID', 'armor_exe_cid_9fcd8'),
 (134872424, 7404, 'P1LP_TIMER_OFF', 'p1lp_timer_off_9fd68'),
 (134872492, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9fdac'),
 (134872500, 7404, 'P1LP_TIMER_OFF', 'p1lp_timer_off_9fdb4'),
 (134872580, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_9fe04'),
 (134872668, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9fe5c'),
 (134872676, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9fe64'),
 (134872924, 5778, 'SKULL_ARCHFIEND_OF_LIGHTNING_CID', 'skull_archfiend_of_lightning_cid_9ff5c'),
 (134872928, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9ff60'),
 (134872936, 7412, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_block2_off_1cf4_9ff68'),
 (134872940, 5794, 'BATTLE_SCARRED_CID', 'battle_scarred_cid_9ff6c'),
 (134872984, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_9ff98'),
 (134873064, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_9ffe8'),
 (134873068, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_9ffec'),
 (134873076, 4993, 'MIRROR_WALL_CID', 'mirror_wall_cid_9fff4'),
 (134873088, 5689, 'TOKEN_1639_CID', 'token_1639_cid_a0000'),
 (134873112, 6000, 'LP_DELTA_6000', 'lp_delta_6000_a0018'),
 (134873224, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a0088'),
 (134873228, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a008c'),
 (134873288, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_a00c8'),
 (134873356, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a010c'),
 (134873360, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a0110'),
 (134873400, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a0138'),
 (134873408, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_a0140'),
 (134873516, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a01ac'),
 (134873520, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a01b0'),
 (134873544,
  134871365,
  'CHECK_SLOT_EQUIPPABLE_FOR_ACTIVE_PLAYER_THUMB_PTR',
  'check_slot_equippable_for_active_player_thumb_ptr_a01c8'),
 (134873576, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a01e8'),
 (134873628, 7528, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_off_a021c'),
 (134873632, 7532, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_state_off_a0220'),
 (134873636, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a0224'),
 (134873752, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a0298'),
 (134873756, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a029c'),
 (134873784,
  134871437,
  'CHECK_SLOT_EFFECT_VALID_FOR_ACTIVE_PLAYER_THUMB_PTR',
  'check_slot_effect_valid_for_active_player_thumb_ptr_a02b8'),
 (134873828, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a02e4'),
 (134873884, 7528, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_off_a031c'),
 (134873888, 7532, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_state_off_a0320'),
 (134873892, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'equip_activation_scan_cursor_off_a0324'),
 (134873960, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a0368'),
 (134873968, 4089, 'CASTLE_OF_DARK_ILLUSIONS_CID', 'castle_of_dark_illusions_cid_a0370'),
 (134873972, 5292, 'VISER_DES_CID', 'viser_des_cid_a0374'),
 (134874100, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a03f4'),
 (134874108, 4890, 'STIM_PACK_CID', 'stim_pack_cid_a03fc'),
 (134874120, 5532, 'DIFFERENT_DIMENSION_CAPSULE_CID', 'different_dimension_capsule_cid_a0408'),
 (134874148, 6049, 'DUST_BARRIER_CID', 'dust_barrier_cid_a0424'),
 (134874152, 5614, 'WAVE_MOTION_CANNON_CID', 'wave_motion_cannon_cid_a0428'),
 (134874168, 6268, 'SWORDS_OF_CONCEALING_LIGHT_CID', 'swords_of_concealing_light_cid_a0438'),
 (134874732, 4808, 'LIGHTFORCE_SWORD_CID', 'lightforce_sword_cid_a066c'),
 (134874736, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a0670'),
 (134874744,
  4294967040,
  'FIELD_SPELL_TO_ZONE_COUNT_DELTA_NEG_0X100',
  'field_spell_to_zone_count_delta_neg_0x100_a0678'),
 (134874752, 1048575, 'EQUIP_NODE_TAG_MASK', 'equip_node_tag_mask_a0680'),
 (134874756, 70344, 'LIGHTFORCE_SWORD_CHAIN_NODE_TAG', 'lightforce_sword_chain_node_tag_a0684'),
 (134874760, 32827, 'OAM_EQUIP_SET_SLOT_P2', 'oam_equip_set_slot_p2_a0688'),
 (134874768, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_a0690'),
 (134874784, 7404, 'P1LP_TIMER_OFF', 'p1lp_timer_off_a06a0'),
 (134874852, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_1ce8_a06e4'),
 (134874856, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_a06e8'),
 (134874888, 32771, 'OAM_EQUIP_SPRITE_P2_03', 'oam_equip_sprite_p2_03_a0708'),
 (134875004, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a077c'),
 (134875016, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_a0788'),
 (134875124, 7404, 'P1LP_TIMER_OFF', 'p1lp_timer_off_a07f4'),
 (134875128, 2152, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_a07f8'),
 (134875132, 7420, 'DISP_SET_VARIANT_OFF', 'disp_set_variant_off_a07fc'),
 (134875140, 4316, 'LP_DISCARD_ZONE_OFF', 'lp_discard_zone_off_a0804'),
 (134875188, 32772, 'OAM_EQUIP_SPRITE_P2_04', 'oam_equip_sprite_p2_04_a0834'),
 (134875196, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'card_play_phase_ctr_off_a083c')]

REF_SLOTS = [(134871940, 165968004, 'equip_activation_phase1_callbacks', 'equip_activation_phase1_callbacks_9fb84'),
 (134871948, 165967788, 'equip_activation_phase3_callbacks', 'equip_activation_phase3_callbacks_9fb8c'),
 (134872012, 165968004, 'equip_activation_phase1_callbacks', 'equip_activation_phase1_callbacks_9fbcc'),
 (134872192, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_9fc80'),
 (134872352, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_9fd20'),
 (134872420, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_9fd64'),
 (134872496, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_9fdb0'),
 (134872672, 33677828, 'gEquipActivationScanCursor', 'gequipactivationscancursor_9fe60'),
 (134872680, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_9fe68'),
 (134872932, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_9ff64'),
 (134872948, 33677828, 'gEquipActivationScanCursor', 'gequipactivationscancursor_9ff74'),
 (134872976, 33677828, 'gEquipActivationScanCursor', 'gequipactivationscancursor_9ff90'),
 (134873072, 33677984, 'gDuelCardCtxBase', 'gduelcardctxbase_9fff0'),
 (134873444, 33677984, 'gDuelCardCtxBase', 'gduelcardctxbase_a0164'),
 (134873684, 33677984, 'gDuelCardCtxBase', 'gduelcardctxbase_a0254'),
 (134873964, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_a036c'),
 (134874104, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_a03f8'),
 (134874740, 33670636, 'gDuelFieldSpellZoneBase', 'gduelfieldspellzonebase_a0674'),
 (134874748, 33675712, 'gEquipNodePool', 'gequipnodepool_a067c'),
 (134875008, 33670416, 'gDuelFieldSlots', 'gduelfieldslots_a0780'),
 (134875136, 33677984, 'gDuelCardCtxBase', 'gduelcardctxbase_a0800')]

RENAME_SLOTS = [(134871004, 'gp1lp_base_9f7dc', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871108, 'gp1lp_base_9f844', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871416, 'gp1lp_base_9f978', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871484, 'gp1lp_base_9f9bc', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871628, 'gp1lp_base_9fa4c', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871780, 'gp1lp_base_9fae4', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871944, 'gp1lp_base_9fb88', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872016, 'gp1lp_base_9fbd0', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872184, 'gp1lp_base_9fc78', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872576, 'gp1lp_base_9fe00', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872944, 'gp1lp_base_9ff70', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872980, 'gp1lp_base_9ff94', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134873220, 'gp1lp_base_a0084', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134873284, 'gp1lp_base_a00c4', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134873404, 'gp1lp_base_a013c', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134874764, 'gp1lp_base_a068c', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134874848, 'gp1lp_base_a06e0', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134875012, 'gp1lp_base_a0784', 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134875192, 'gp1lp_base_a0838', 'gP1LifePoints base; preserve the existing DATA reference and its source.')]

PLATES = [(134870852,
  'scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare',
  'r0=player. Resume cursor 0..9 at gP1LifePoints+EQUIP_ACTIVATION_SCAN_CURSOR_OFF. Decode side=player^(cursor/5) and '
  'spell/trap slot=cursor%5+5. On an active Mirage of Nightmare, pack the slot entry and call '
  'apply_equip_activation_with_id_lookup, advance the cursor, and return0. Misses advance and continue; exhaustion '
  'returns1.'),
 (134871048,
  'scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand',
  'r0=player. If the per-player zone count at base+0xc exceeds4, return1. Otherwise scan spell/trap slots5..9 for '
  'Bottomless Shifting Sand (ICID 0x1540). On the first active match, enqueue its equip-slot bitmap and return0. '
  'Return1 when no active match remains.'),
 (134871132,
  'scan_monster_zone_for_equip_activation_reserved_icid_a',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card with the unmapped internal CID 0x1282. Return the '
  'callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own '
  'epilogue.'),
 (134871148,
  'scan_monster_zone_for_equip_activation_reserved_icid_b',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card with the unmapped internal CID 0x11ea. Return the '
  'callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own '
  'epilogue.'),
 (134871164,
  'scan_monster_zone_for_equip_activation_a_man_with_wdjat',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card with A_MAN_WITH_WDJAT_CID. Return the callee result: '
  '0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own epilogue.'),
 (134871180,
  'scan_monster_zone_for_equip_activation_reserved_icid_c',
  'r0=player. Call scan_monster_zone_for_equip_activation_by_card with the unmapped internal CID 0x1147. Return the '
  'callee result: 0 after one activation, 1 after scan exhaustion. The wrapper uses BL and returns through its own '
  'epilogue.'),
 (134871196,
  'get_maintenance_lp_cost_by_icid',
  'r0=internal CID. Return the periodic LP maintenance cost, or0 when unmatched. Mappings are Messenger100, Imperial '
  'Order700, Mirror Wall2000, Mask of Brutality1000, Fairy Box500, token1639=1000, Vilepawn500, Shadowknight900, '
  'Darkbishop500, Desrook500, Infernalqueen500, Terrorking800, and Skull Archfiend500. Pure lookup.'),
 (134871364,
  'check_slot_equippable_for_active_player',
  'r0=player, r1+r2=monster slot. Require slot<=4, player equal to the active selector at gP1LifePoints+0x1ce8, '
  'check_slot_card_can_be_equipped nonzero, and slot different from the shared scan cursor. Return0x800 when all '
  'checks pass, else0. Stored as a THUMB callback at 0x080a01c8.'),
 (134871436,
  'check_slot_effect_valid_for_active_player',
  'r0=player, r1+r2=slot. Require player to match the XOR-derived side from gP1LifePoints+0x1ce8/+0x1d20, slot<=10, '
  'and get_slot_effect_card_value nonzero. Return0x800 on success, else0. Stored as a THUMB callback at 0x080a02b8.'),
 (134871500,
  'run_equip_activation_display_phase_by_state_code',
  'No APCS inputs. Allocate0x298 bytes, read player and equip-display phase from gP1LifePoints, and drive the large '
  'phase tree. Paths run the 4-entry phase-1 callbacks, resume the 54-entry phase-3 callbacks by cursor, scan slots, '
  'render maintenance LP values, initialize validation callbacks, or dispatch special equip sprites. Return0 while '
  'work remains and1 when complete through the shared frame epilogue.'),
 (134871830,
  'return_zero_from_equip_activation_display_phase',
  'Entry sets r0=0 and calls release_equip_activation_display_phase_frame. Ghidra body also owns pools at0x0809fb1c/20 '
  'and the parent phase fragment at0x0809fb24..80, reached from the parent branch at0x0809fa32. That fragment runs '
  'four phase-1 callbacks, then resumes one of 54 phase-3 callbacks by cursor. Preserve the discontiguous parent-flow '
  'ownership.'),
 (134873760,
  'advance_display_slot_if_zone_active',
  'Shared parent fragment; non-APCS r4=state base, r1=slot, r7=slot-index pointer. If state+0x1d40 is set, advance '
  '*r7, initialize the effect-valid callback, and return0. Otherwise enqueue the slot bitmap using state+0x1d20, '
  'advance the shared cursor, write phase0x65, and return0 through the parent epilogue.'),
 (134873832,
  'advance_effect_card_slot_display_if_zone_active',
  'Shared parent fragment; non-APCS r4=state base and r7=phase pointer. If display state is unconfirmed, write '
  'phase0x82 and return0. Otherwise enqueue an effect-card slot sprite from offsets0x1d68/0x1d6c/0x1d74, advance the '
  'shared cursor, write phase0x65, and return0.'),
 (134873900,
  'set_phase_code_c8_exit_zero',
  'Shared parent exit with non-APCS r7=phase pointer. Write0xc8 to *r7, then call '
  'return_zero_from_equip_activation_display_phase. Returns0 after releasing the parent frame.'),
 (134873908,
  'dispatch_equip_sprite_update_by_slot_icid',
  'Shared parent fragment with non-APCS r8=player. Scan monster slots0..4 for Castle of Dark Illusions and Viser Des '
  'sprite paths, then spell/trap slots5..9 for card-specific set-slot, bitmap, and LP indicator paths. After the slot '
  'scan, handle Lightforce Sword chain nodes, advance the equip-display phase, and return0 through the parent '
  'epilogue.'),
 (134874772,
  'set_display_phase_code_78_exit_zero',
  'Shared parent entry with non-APCS r4=state base. Form r1=r4+P1LP_TIMER_OFF and r0=0x78, then fall through to '
  'write_display_code_exit_zero. The combined path writes0x78 and returns0 through the parent epilogue.'),
 (134874778,
  'write_display_code_exit_zero',
  'Shared parent exit. Inputs r0=value and r1=target word. Store r0 to *r1, then call '
  'return_zero_from_equip_activation_display_phase. Returns0 after releasing the parent frame. Eight explicit incoming '
  'jumps/calls are preserved.'),
 (134874788,
  'return_one_from_equip_activation_display_phase',
  'Shared parent return entry. Set r0=1 and fall through to release_equip_activation_display_phase_frame. Returns1 '
  'after the common frame release. Five explicit incoming jumps are preserved.'),
 (134874790,
  'release_equip_activation_display_phase_frame',
  'Shared epilogue for run_equip_activation_display_phase_by_state_code. Preserve incoming r0, add0x298 to sp, restore '
  'r8-r10 and r4-r7, then return through the saved link register. The explicit incoming call is from return_zero; '
  'return_one reaches it by fallthrough.'),
 (134874812,
  'tick_equip_display_phase_by_state_code',
  'No APCS inputs. Read player and display phase from gP1LifePoints. Phase0 enqueues side-specific sprite code3. '
  'Phase1 scans five monster slots for CID0x1740 and advances the phase. Phase2 compares timer/LP state, writes '
  'DISP_SET_VARIANT_OFF and LP_DISCARD_ZONE_OFF, and enqueues side-specific code4. All handled paths advance '
  'CARD_PLAY_PHASE_CTR_OFF and return0.')]

SLOT_EOLS = [(134871004, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871008, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134871012, 'Byte stride between the two player state blocks.'),
 (134871016, 'Internal CID 0x1539 for Mirage of Nightmare; card mapping and password cross-check are recorded.'),
 (134871108, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871112, 'Byte stride between the two player state blocks.'),
 (134871144, 'Unmapped internal CID 0x1282; inverse table is 0xffff and no card-stat record exists.'),
 (134871160, 'Unmapped internal CID 0x11ea; inverse table is 0xffff and no card-stat record exists.'),
 (134871176, 'Internal CID 0x158e for A Man with Wdjat; card mapping and password cross-check are recorded.'),
 (134871192, 'Unmapped internal CID 0x1147; inverse table is 0xffff and no card-stat record exists.'),
 (134871232, 'Internal CID 0x168c for Vilepawn Archfiend; card mapping and password cross-check are recorded.'),
 (134871236, 'Internal CID 0x1381 for Mirror Wall; card mapping and password cross-check are recorded.'),
 (134871256, 'Internal CID 0x13f9 for Fairy Box; card mapping and password cross-check are recorded.'),
 (134871268, 'Special token CID 0x1639; inverse index 2090 has no ordinary card-stat record.'),
 (134871292, 'Internal CID 0x168f for Desrook Archfiend; card mapping and password cross-check are recorded.'),
 (134871316, 'Internal CID 0x1691 for Terrorking Archfiend; card mapping and password cross-check are recorded.'),
 (134871416, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871420, 'Byte offset from gP1LifePoints to the active-player selector word.'),
 (134871424, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134871484, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871488, 'Byte offset from gP1LifePoints to the active-player selector word.'),
 (134871624, 'Signed frame allocation used by add sp.'),
 (134871628, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871632, 'Byte offset from gP1LifePoints to the active-player selector word.'),
 (134871636, 'Byte stride between the two player state blocks.'),
 (134871640, "Internal CID 0x137e for Solomon's Lawbook; card mapping and password cross-check are recorded."),
 (134871644, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134871780, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871784, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134871836, 'Player-side sprite code 0x0d with bit15 set.'),
 (134871840, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134871940, 'Base of the 4-entry phase-1 THUMB callback table.'),
 (134871944, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134871948, 'Base of the 54-entry phase-3 THUMB callback table.'),
 (134871952, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134871956, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134872012, 'Base of the 4-entry phase-1 THUMB callback table.'),
 (134872016, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872020, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134872180, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134872184, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872188, 'Byte stride between the two player state blocks.'),
 (134872192, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134872228, 'Internal CID 0x13f4 for Mask of Brutality; card mapping and password cross-check are recorded.'),
 (134872260, 'Unmapped internal CID 0x144a; inverse table is 0xffff and no card-stat record exists.'),
 (134872280, 'Internal CID 0x161b for Armor Exe; card mapping and password cross-check are recorded.'),
 (134872352, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134872420, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134872424, 'Byte offset from gP1LifePoints to the duel display timer word.'),
 (134872492, 'Byte stride between the two player state blocks.'),
 (134872496, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134872500, 'Byte offset from gP1LifePoints to the duel display timer word.'),
 (134872576, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872580, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134872668, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134872672, 'Absolute u32 shared equip activation scan cursor.'),
 (134872676, 'Byte stride between the two player state blocks.'),
 (134872680, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134872924,
  'Internal CID 0x1692 for Skull Archfiend of Lightning; card mapping and password cross-check are recorded.'),
 (134872928, 'Byte stride between the two player state blocks.'),
 (134872932, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134872936, 'Byte offset from gP1LifePoints to the paired LP/display state word.'),
 (134872940, 'Internal CID 0x16a2 for Battle-Scarred; card mapping and password cross-check are recorded.'),
 (134872944, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872948, 'Absolute u32 shared equip activation scan cursor.'),
 (134872976, 'Absolute u32 shared equip activation scan cursor.'),
 (134872980, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134872984, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134873064, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873068, 'Byte stride between the two player state blocks.'),
 (134873072, 'Duel card activation context base.'),
 (134873076, 'Internal CID 0x1381 for Mirror Wall; card mapping and password cross-check are recorded.'),
 (134873088, 'Special token CID 0x1639; inverse index 2090 has no ordinary card-stat record.'),
 (134873112, 'LP threshold value 6000; this consumer compares an LP word, not a CID.'),
 (134873220, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134873224, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873228, 'Byte stride between the two player state blocks.'),
 (134873284, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134873288, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134873356, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873360, 'Byte stride between the two player state blocks.'),
 (134873400, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873404, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134873408, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134873444, 'Duel card activation context base.'),
 (134873516, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873520, 'Byte stride between the two player state blocks.'),
 (134873544, 'Stored THUMB callback value; the auxiliary reference targets the even Function entry.'),
 (134873576, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873628, 'Byte offset from gP1LifePoints to the eligibility sprite-control word.'),
 (134873632, 'Byte offset from gP1LifePoints to the eligibility animation-state word.'),
 (134873636, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873684, 'Duel card activation context base.'),
 (134873752, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873756, 'Byte stride between the two player state blocks.'),
 (134873784, 'Stored THUMB callback value; the auxiliary reference targets the even Function entry.'),
 (134873828, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873884, 'Byte offset from gP1LifePoints to the eligibility sprite-control word.'),
 (134873888, 'Byte offset from gP1LifePoints to the eligibility animation-state word.'),
 (134873892, 'Byte offset from gP1LifePoints to the shared activation scan cursor.'),
 (134873960, 'Byte stride between the two player state blocks.'),
 (134873964, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134873968, 'Internal CID 0x0ff9 for Castle of Dark Illusions; card mapping and password cross-check are recorded.'),
 (134873972, 'Internal CID 0x14ac for Viser Des; card mapping and password cross-check are recorded.'),
 (134874100, 'Byte stride between the two player state blocks.'),
 (134874104, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134874108, 'Internal CID 0x131a for Stim-Pack; card mapping and password cross-check are recorded.'),
 (134874120,
  'Internal CID 0x159c for Different Dimension Capsule; card mapping and password cross-check are recorded.'),
 (134874148, 'Internal CID 0x17a1 for Dust Barrier; card mapping and password cross-check are recorded.'),
 (134874152, 'Internal CID 0x15ee for Wave-Motion Cannon; card mapping and password cross-check are recorded.'),
 (134874168, 'Internal CID 0x187c for Swords of Concealing Light; card mapping and password cross-check are recorded.'),
 (134874732, 'Internal CID 0x12c8 for Lightforce Sword; card mapping and password cross-check are recorded.'),
 (134874736, 'Byte stride between the two player state blocks.'),
 (134874740, 'Field-spell slot base; this consumer derives the zone-count base with -0x100.'),
 (134874744, 'Signed delta from gDuelFieldSpellZoneBase to the per-player zone-count base.'),
 (134874748, 'Equip-chain node pool base; entries use an 8-byte stride.'),
 (134874752, 'Mask selecting the low 20-bit equip-chain node tag.'),
 (134874756, 'Equip-chain node low-20-bit tag for Lightforce Sword.'),
 (134874760, 'Player-side equip set-slot sprite code.'),
 (134874764, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134874768, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134874784, 'Byte offset from gP1LifePoints to the duel display timer word.'),
 (134874848, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134874852, 'Byte offset from gP1LifePoints to the active-player selector word.'),
 (134874856, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134874888, 'Player-side sprite code 3 with bit15 set.'),
 (134875004, 'Byte stride between the two player state blocks.'),
 (134875008, 'Field-slot array base; consumers add player stride and 20-byte slot offsets.'),
 (134875012, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134875016, 'Byte offset from gP1LifePoints to the equip display phase word.'),
 (134875124, 'Byte offset from gP1LifePoints to the duel display timer word.'),
 (134875128, 'Byte stride between the two player state blocks.'),
 (134875132, 'Byte offset from gP1LifePoints to display variant 1/2.'),
 (134875136, 'Duel card activation context base.'),
 (134875140, 'Byte offset from gP1LifePoints to LP discard-zone tracking.'),
 (134875188, 'Player-side sprite code 4 with bit15 set.'),
 (134875192, 'gP1LifePoints base; preserve the existing DATA reference and its source.'),
 (134875196, 'Byte offset from gP1LifePoints to the equip display phase word.')]

FUNC_RENAME = [(134870852,
  'scan_all_monster_zone_slots_for_equip_activation_mirage_of_nightmare',
  'scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare'),
 (134871196, 'get_lp_cost_by_field_spell_icid', 'get_maintenance_lp_cost_by_icid'),
 (134871500, 'dispatch_duel_field_ai_phase_by_state_code', 'run_equip_activation_display_phase_by_state_code'),
 (134871830, 'return_zero_from_duel_ai_main', 'return_zero_from_equip_activation_display_phase'),
 (134874788, 'return_one_from_duel_ai_main', 'return_one_from_equip_activation_display_phase'),
 (134874790, 'release_duel_ai_main_frame', 'release_equip_activation_display_phase_frame')]

AUX_REFS = [(134873544, 134871364, 'DATA', 'USER_DEFINED', 0), (134873784, 134871436, 'DATA', 'USER_DEFINED', 0)]

NEW_DEFINITIONS = [('EQUIP_ACTIVATION_UNMAPPED_CID_1147', 4423, 'constants/card_info.inc'),
 ('EQUIP_ACTIVATION_UNMAPPED_CID_11EA', 4586, 'constants/card_info.inc'),
 ('EQUIP_ACTIVATION_UNMAPPED_CID_1282', 4738, 'constants/card_info.inc'),
 ('EQUIP_ACTIVATION_UNMAPPED_CID_144A', 5194, 'constants/card_info.inc'),
 ('LIGHTFORCE_SWORD_CID', 4808, 'constants/card_info.inc'),
 ('MASK_OF_BRUTALITY_CID', 5108, 'constants/card_info.inc'),
 ('MIRAGE_OF_NIGHTMARE_CID', 5433, 'constants/card_info.inc'),
 ('ARMOR_EXE_CID', 5659, 'constants/card_info.inc'),
 ('OAM_EQUIP_SPRITE_P2_03', 32771, 'constants/oam_attr.inc'),
 ('OAM_EQUIP_SPRITE_P2_04', 32772, 'constants/oam_attr.inc'),
 ('OAM_EQUIP_SPRITE_P2_0D', 32781, 'constants/oam_attr.inc'),
 ('LIGHTFORCE_SWORD_CHAIN_NODE_TAG', 70344, 'constants/card_info.inc'),
 ('CHECK_SLOT_EQUIPPABLE_FOR_ACTIVE_PLAYER_THUMB_PTR', 134871365, 'constants/duel_field.inc'),
 ('CHECK_SLOT_EFFECT_VALID_FOR_ACTIVE_PLAYER_THUMB_PTR', 134871437, 'constants/duel_field.inc'),
 ('EQUIP_PHASE_FRAME_ALLOC_NEG_0X298', 4294966632, 'constants/duel_field.inc'),
 ('FIELD_SPELL_TO_ZONE_COUNT_DELTA_NEG_0X100', 4294967040, 'constants/duel_field.inc'),
 ('gEquipActivationScanCursor', 33677828, 'constants/ewram.inc')]

CALLBACK_TABLES = [('equip_activation_phase3_callbacks',
  165967788,
  165968004,
  [(165967788, 134867697, 'scan_equip_zone_for_dimensionhole'),
   (165967792, 134867797, 'scan_monster_zone_slots_for_equip_activation_reserved_icid_g'),
   (165967796, 134867973, 'scan_monster_zone_for_equip_activation_spirit_of_the_breeze'),
   (165967800, 134867989, 'scan_monster_zone_for_equip_activation_dancing_fairy'),
   (165967804, 134868005, 'scan_monster_zone_for_equip_activation_cure_mermaid'),
   (165967808, 134868021, 'scan_player_card_array_for_equip_activation_marie_the_fallen_one'),
   (165967812, 134868193, 'scan_trap_zone_for_equip_activation_life_absorbing_machine'),
   (165967816, 134868225, 'scan_monster_zone_for_equip_activation_white_magician_pikeru'),
   (165967820, 134868257, 'scan_monster_zone_for_equip_activation_princess_pikeru'),
   (165967824, 134868289, 'scan_monster_zone_for_equip_activation_bowganian'),
   (165967828, 134868501, 'scan_all_zone_slots_for_equip_lp_indicator_graverobbers_retribution'),
   (165967832, 134868873, 'scan_trap_zone_for_equip_activation_mask_of_dispel'),
   (165967836, 134868889, 'scan_trap_zone_for_equip_activation_mask_of_accursed'),
   (165967840, 134868905, 'scan_trap_zone_for_equip_activation_nightmare_wheel'),
   (165967844, 134867649, 'scan_trap_zone_for_equip_activation_ominous_fortunetelling'),
   (165967848, 134868241, 'scan_monster_zone_for_equip_activation_ebon_magician_curran'),
   (165967852, 134868273, 'scan_monster_zone_for_equip_activation_princess_curran'),
   (165967856, 134871149, 'scan_monster_zone_for_equip_activation_reserved_icid_b'),
   (165967860, 134871165, 'scan_monster_zone_for_equip_activation_a_man_with_wdjat'),
   (165967864, 134871181, 'scan_monster_zone_for_equip_activation_reserved_icid_c'),
   (165967868, 134867633, 'scan_trap_zone_for_equip_activation_blind_destruction'),
   (165967872, 134867665, 'scan_trap_zone_for_equip_activation_needle_wall'),
   (165967876, 134867681, 'scan_trap_zone_for_equip_activation_dangerous_machine_type6'),
   (165967880, 134869833, 'scan_monster_zone_slots_for_equip_activation_mucus_yolk'),
   (165967884, 134870029, 'scan_monster_zone_for_equip_activation_legendary_fiend'),
   (165967888, 134870045, 'scan_monster_zone_for_equip_activation_exodia_necross'),
   (165967892, 134870853, 'scan_all_spell_trap_zone_slots_for_equip_activation_mirage_of_nightmare'),
   (165967896, 134870077, 'scan_monster_zone_for_equip_activation_agent_of_wisdom_mercury'),
   (165967900, 134870061, 'scan_monster_zone_for_equip_activation_amazoness_blowpiper'),
   (165967904, 134870093, 'scan_field_slots_for_lv_monster_equip_activation'),
   (165967908, 134871133, 'scan_monster_zone_for_equip_activation_reserved_icid_a'),
   (165967912, 134867765, 'scan_monster_zone_for_equip_activation_reserved_icid_f'),
   (165967916, 134868697, 'scan_all_zone_slots_for_lp_indicator_burning_land'),
   (165967920, 134867781, 'scan_monster_zone_for_equip_activation_lava_golem'),
   (165967924, 134869113, 'scan_trap_slots_for_kiseitai_equip_chain_sprite'),
   (165967928, 134869041, 'scan_trap_zone_for_equip_activation_blast_sphere'),
   (165967932, 134869065, 'scan_trap_zone_for_equip_activation_adhesive_explosive'),
   (165967936, 134869017, 'scan_trap_zone_for_equip_activation_minor_goblin_official'),
   (165967940, 134869089, 'scan_monster_zone_for_equip_activation_malice_ascendant'),
   (165967944, 134868921, 'scan_trap_zone_for_equip_activation_snatch_steal'),
   (165967948, 134868945, 'scan_trap_zone_for_equip_activation_brain_jacker'),
   (165967952, 134868993, 'scan_trap_zone_for_equip_activation_the_eye_of_truth'),
   (165967956, 134868969, 'scan_trap_zone_for_equip_activation_falling_down'),
   (165967960, 134870421, 'scan_equip_zone_for_equip_activation_vampire_lord'),
   (165967964, 134870437, 'scan_equip_zone_for_equip_activation_sacred_phoenix'),
   (165967968, 134870405, 'scan_equip_zone_for_equip_activation_revival_jam'),
   (165967972, 134870453, 'scan_equip_zone_for_entity_sprite_activation_curse_of_vampire'),
   (165967976, 134870469, 'scan_equip_zone_for_entity_sprite_activation_curse_of_vampire_opponent'),
   (165967980, 134867617, 'scan_trap_zone_for_equip_activation_jam_breeding_machine'),
   (165967984, 134868305, 'scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend'),
   (165967988, 134870789, 'scan_spell_trap_zone_for_equip_activation_reserved_icid_e'),
   (165967992, 134870813, 'scan_spell_trap_zone_for_equip_activation_recycle'),
   (165967996, 134870829, 'scan_monster_zone_for_equip_activation_aqua_spirit_opponent'),
   (165968000, 134868209, 'scan_trap_zone_for_equip_activation_senri_eye')]),
 ('equip_activation_phase1_callbacks',
  165968004,
  165968020,
  [(165968004, 134871049, 'scan_trap_zone_for_equip_bitmap_update_bottomless_shifting_sand'),
   (165968008, 134869533, 'scan_equip_zone_for_special_summon_activation_return_zombie'),
   (165968012, 134869501, 'scan_player_card_array_for_equip_activation_sinister_serpent'),
   (165968016, 134869517, 'scan_player_card_array_for_equip_activation_treeborn_frog')])]

REGISTRY_SIBLING = ('FUN_0809ed50',
 'scan_all_monster_zone_slots_for_equip_activation_infernalqueen_archfiend',
 'Infernalqueen Archfiend (0x1690) all-monster-zone-slot equip activation scan. r0=player_id([0..1]). Uses '
 'gP1LifePoints+0x1d24 counter, scans 10 slots. Each slot: udivsi3/umodsi3 compute col=slot%5, side=slot/5; '
 'test_slot_has_active_card(side, col, 0x1690); on hit build OAM attr (0x84<<0x13 prefix + player_bit + col_encoded); '
 'apply_equip_activation_with_id_lookup. Success: counter++, return 0; else return 1. Structurally identical to '
 'scan_all_monster_zone_slots_for_equip_activation_mirage_of_nightmare(0x0809f744). Constants: '
 'CARD_ID=0x1690=Infernalqueen Archfiend, COUNTER_OFFSET=0x1d24, SLOT_COUNT=10, OAM_PREFIX=0x84<<0x13.',
 '93c4ad8ba5f608c53307a5e3cd98628a7525395d7ebed53f713e833675c0afcc',
 'r0=player. Resume ten monster slots with LP+0x1d24 cursor: side=(cursor/5)^player, slot=cursor%5. For active '
 'Infernalqueen Archfiend, pack the actual entry CID, side and slot, then call activation with decoded flags. Ignore '
 'its result; advance cursor and return 0 after the first match. Other entries advance and continue. Return 1 after '
 'cursor 9.',
 'a4e4cb281edffe3e3534690a3883fdd4b69ae802c1c14e6732199205273b27e1')

INPUT_HASHES = [('doc/dev/refine/F13-Seg-3.proposal.md', 'f00685aad1690e7c4264311ecbe941e429c0e7a400136a882497725643fea89c'),
 ('doc/dev/refine/F13-Seg-3.review.md', 'a528e345bf7585aef15131b8b0247433d081ac1171b8633d57108009d9781919'),
 ('output/refine-run-20260831-194634/f13-seg3-plan.json',
  'c0438860bcdbfc05f8a4db4be8fe2e347362b8cb007247e3ccf15fe64ac90b12'),
 ('output/refine-run-20260831-194634/f13-seg3-plates.json',
  '5eab55dbf65fe3792d0efd1e189ddf5646ff456bc82eefbb7e52dcad0c5c53f5'),
 ('output/refine-run-20260831-194634/f13-seg3-selfcheck.json',
  'ab377e76cbd2ff22c586fef9da364039a5a675bb82940b790f3a43b3ae76f114'),
 ('output/refine-run-20260831-194634/f13-seg3-slots-before.json',
  'a32394f31bfe2e12d0d399fa8ff5f0716e4cbe8dc8f258a3b939c8d22f73eb35'),
 ('output/refine-run-20260831-194634/f13-seg3-functions-before.json',
  'd4666dd3f4a3aaba1c4ad12a5409f0b3348059405665bc50754d75f824180536'),
 ('output/refine-run-20260831-194634/f13-seg3-rom-tables-before.json',
  '921cb2eed008ba89a7c66ee17d1c70057723d112f713a63c53ed6f4587a05534'),
 ('output/refine-run-20260831-194634/f13-seg3-rename-dependencies.json',
  '4d46c2a25078fada9712a3e352827dbd13204afc4693e1aef7abd67b95114264'),
 ('output/refine-run-20260831-194634/f13-seg3-review-registry-plate.json',
  '0a90d7514a8bc753b8cf0c3e15d5d38688ab93f2f1a766c32677b53598b172d8')]

import copy
import hashlib
import json
import os

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType, SymbolType

MODE = list(getScriptArgs())[0].lower() if list(getScriptArgs()) else 'dry'
if MODE not in ('dry', 'apply', 'check'):
    raise RuntimeError('Expected dry, apply, or check')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(getSourceFile().getAbsolutePath())))
RUN = os.path.join(ROOT, 'output', 'refine-run-20260831-194634')
listing = currentProgram.getListing()
symbols = currentProgram.getSymbolTable()
references = currentProgram.getReferenceManager()
memory = currentProgram.getMemory()
equates = currentProgram.getEquateTable()
FAILS = []
COUNTS = dict((key, 0) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME'))
SEGMENT_START = 0x0809f744
SEGMENT_END = 0x080a0840
SEGMENT_RANGE_SHA256 = 'c5e29fb9ace64f87ae7a81edab548a0811a05f392320b999c9b1628af1bc36fa'


def fail(message):
    FAILS.append(message)
    print('FAIL: ' + message)


def require(condition, message):
    if not condition:
        fail(message)


def same(message, actual, expected):
    if canonical(actual) != canonical(expected):
        fail(message)


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def read_json(name):
    with open(os.path.join(RUN, name), 'r') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


def raw_hex(value, size):
    return ''.join('%02x' % (memory.getByte(toAddr(value + index)) & 255) for index in range(size))


def range_hash():
    raw = ''.join(chr(memory.getByte(toAddr(value)) & 255) for value in range(SEGMENT_START, SEGMENT_END))
    return hashlib.sha256(raw).hexdigest()


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
    result = {'address': value, 'symbols': [symbol_info(s) for s in symbols.getSymbols(addr)],
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
    # Never read uninitialized RAM values.
    if 0x08000000 <= value <= 0x09fffffc:
        result['rom_word'] = memory.getInt(addr) & 0xffffffff
    for ref in references.getReferencesFrom(addr):
        item = basic_ref(ref)
        item['target_primary'] = symbol_info(symbols.getPrimarySymbol(ref.getToAddress()), False)
        result['references_from'].append(item)
    result['references_to'] = [basic_ref(ref) for ref in references.getReferencesTo(addr)]
    return result


def canonical(value):
    result = copy.deepcopy(value)
    if isinstance(result, dict):
        result.pop('input_label', None)
        for key in ('symbols', 'equates', 'references_from', 'references_to', 'incoming', 'body_refs'):
            if key in result and isinstance(result[key], list):
                result[key] = sorted(result[key], key=lambda item: json.dumps(item, sort_keys=True))
    return result


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


PLAN = read_json('f13-seg3-plan.json')
ROOT_SLOTS = read_json('f13-seg3-slots-before.json')
ROOT_FUNCTIONS = read_json('f13-seg3-functions-before.json')
ROOT_TABLES = read_json('f13-seg3-rom-tables-before.json')
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())
SLOTS = dict((row['slot'], row) for row in PLAN['actions'])
RENAMES = dict((addr, new) for addr, old, new in FUNC_RENAME)
OLD_NAMES = dict((addr, old) for addr, old, new in FUNC_RENAME)
PLATE_MAP = dict((addr, text) for addr, name, text in PLATES)
EOL_MAP = dict(SLOT_EOLS)
AUX_MAP = dict((addr, (target, ref_type, source, operand)) for addr, target, ref_type, source, operand in AUX_REFS)
REF_TARGETS = dict((addr, (value, name)) for addr, value, name, label in REF_SLOTS)
NEW_NAMES = set(name for name, value, path in NEW_DEFINITIONS)

BASE = {}


def add_base(item):
    addr = item['address']
    require(addr not in BASE or canonical(BASE[addr]) == canonical(item), 'BASE_DUPLICATE %08x' % addr)
    BASE[addr] = canonical(item)


for row in PLAN['actions']:
    add_base(row['before'])
for item in ROOT_SLOTS['extra_targets']:
    add_base(item)
for item in ROOT_TABLES['extra_targets']:
    add_base(item)

LABEL_AFTER = {}
NEW_IDS = set()
for addr, row in SLOTS.items():
    LABEL_AFTER[addr] = {'id': 0, 'name': row['slot_label'], 'qualified_name': row['slot_label'],
                         'source': 'USER_DEFINED', 'type': 'Label', 'primary': True}
    NEW_IDS.add(addr)
for slot_addr, (target, name) in REF_TARGETS.items():
    old = BASE[target]['symbols']
    existing = [s for s in old if s['name'] == name and s['source'] == 'USER_DEFINED']
    if existing:
        LABEL_AFTER[target] = copy.deepcopy(existing[0])
        LABEL_AFTER[target]['primary'] = True
    else:
        LABEL_AFTER[target] = {'id': 0, 'name': name, 'qualified_name': name,
                               'source': 'USER_DEFINED', 'type': 'Label', 'primary': True}
        NEW_IDS.add(target)


def memory_target(ref):
    try:
        return int(ref['to'], 16)
    except (ValueError, TypeError):
        return None


def planned_ref(source, target, operand=0, ref_type='DATA', ref_source='USER_DEFINED', primary=True, navigation=False):
    result = {'from': '%08x' % source, 'to': '%08x' % target, 'operand': operand,
              'type': ref_type, 'source': ref_source, 'primary': primary}
    if navigation:
        primary_symbol = LABEL_AFTER.get(target)
        if primary_symbol is None:
            primary_symbol = symbol_info(symbols.getPrimarySymbol(toAddr(target)), False)
        else:
            primary_symbol = copy.deepcopy(primary_symbol)
            primary_symbol.pop('primary', None)
        result['target_primary'] = primary_symbol
    return result


def expected_after(addr):
    result = copy.deepcopy(BASE[addr])
    if addr in LABEL_AFTER:
        result['symbols'] = [copy.deepcopy(LABEL_AFTER[addr])]
    if addr in SLOTS:
        row = SLOTS[addr]
        result['comments']['EOL'] = row['eol']
        if row['kind'] == 'EQ':
            result['equates'] = [{'name': row['const_name'], 'value': row['value']}]
            if addr in AUX_MAP:
                target, ref_type, source, operand = AUX_MAP[addr]
                result['references_from'].append(planned_ref(addr, target, operand, ref_type, source, True, True))
        elif row['kind'] == 'REF':
            target = row['value']
            result['references_from'].append(planned_ref(addr, target, 0, 'DATA', 'USER_DEFINED', True, True))
    for slot_addr, (target, name) in REF_TARGETS.items():
        if target == addr:
            result['references_to'].append(planned_ref(slot_addr, target))
    for slot_addr, (target, ref_type, source, operand) in AUX_MAP.items():
        if target == addr:
            result['references_to'].append(planned_ref(slot_addr, target, operand, ref_type, source))
    for ref in result['references_from']:
        target = memory_target(ref)
        if target in LABEL_AFTER:
            primary = copy.deepcopy(LABEL_AFTER[target])
            primary.pop('primary', None)
            ref['target_primary'] = primary
        elif target is not None and (target & ~1) in RENAMES and ref.get('target_primary') is not None:
            suffix = '+1' if target & 1 else ''
            ref['target_primary']['name'] = RENAMES[target & ~1] + suffix
            ref['target_primary']['qualified_name'] = RENAMES[target & ~1] + suffix
    owner = result.get('containing_function')
    if owner is not None and int(owner['entry'], 16) in RENAMES:
        owner['name'] = RENAMES[int(owner['entry'], 16)]
    return canonical(result)


def normalize_new_ids(state):
    result = copy.deepcopy(state)
    addr = result['address']
    if addr in NEW_IDS:
        for symbol in result['symbols']:
            if symbol['name'] == LABEL_AFTER[addr]['name']:
                require(symbol['id'] > 0, 'NEW_SYMBOL_ID %08x' % addr)
                symbol['id'] = 0
    for ref in result['references_from']:
        target = memory_target(ref)
        if target in NEW_IDS and ref.get('target_primary') is not None:
            if ref['target_primary']['name'] == LABEL_AFTER[target]['name']:
                require(ref['target_primary']['id'] > 0, 'NEW_NAV_ID %08x' % target)
                ref['target_primary']['id'] = 0
    return canonical(result)


def require_name(name, addr, post=False):
    matches = list(symbols.getGlobalSymbols(name))
    require(all(symbol.getAddress() == toAddr(addr) for symbol in matches), 'NAME_COLLISION ' + name)
    if post:
        require(len(matches) == 1, 'NAME_COUNT ' + name)


def verify_literal_tables():
    expected_eq = [(a['slot'], a['value'], a['const_name'], a['slot_label']) for a in PLAN['actions'] if a['kind'] == 'EQ']
    expected_ref = [(a['slot'], a['value'], a['const_name'], a['slot_label']) for a in PLAN['actions'] if a['kind'] == 'REF']
    expected_rename = [(a['slot'], a['slot_label'], a['eol']) for a in PLAN['actions'] if a['kind'] == 'RENAME']
    expected_plates = [(p['addr'], p['new_name'], p['text']) for p in PLAN['plates']]
    expected_eols = [(a['slot'], a['eol']) for a in PLAN['actions']]
    expected_functions = [(r['addr'], r['old'], r['new']) for r in PLAN['renames']]
    expected_aux = [(a['slot'], a['aux_ref']['target'], a['aux_ref']['type'], a['aux_ref']['source'], a['aux_ref']['operand'])
                    for a in PLAN['actions'] if 'aux_ref' in a]
    expected_new = [(d['name'], d['value'], d['path']) for d in PLAN['new_definitions']]
    expected_tables = [(t['name'], t['start'], t['end'], [(e['address'], e['raw'], e['function']) for e in t['entries']])
                       for t in PLAN['tables']]
    sibling = PLAN['registry_sync']['sibling_plate']
    expected_registry = (sibling['key'], sibling['target'], sibling['expected_old_text'], sibling['expected_old_sha256'],
                         sibling['replacement_text'], sibling['replacement_sha256'])
    same('TABLE_EQ', EQ_SLOTS, expected_eq)
    same('TABLE_REF', REF_SLOTS, expected_ref)
    same('TABLE_RENAME', RENAME_SLOTS, expected_rename)
    same('TABLE_PLATE', PLATES, expected_plates)
    same('TABLE_EOL', SLOT_EOLS, expected_eols)
    same('TABLE_FUNC_RENAME', FUNC_RENAME, expected_functions)
    same('TABLE_AUX', AUX_REFS, expected_aux)
    same('TABLE_NEW', NEW_DEFINITIONS, expected_new)
    same('TABLE_CALLBACKS', CALLBACK_TABLES, expected_tables)
    same('TABLE_REGISTRY_SIBLING', REGISTRY_SIBLING, expected_registry)
    require((len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATES), len(SLOT_EOLS), len(FUNC_RENAME),
             len(AUX_REFS), len(NEW_DEFINITIONS), sum(len(row[3]) for row in CALLBACK_TABLES)) ==
            (98, 21, 19, 20, 138, 6, 2, 17, 58), 'COUNTS')
    require(len(SLOTS) == 138 and set(EOL_MAP) == set(SLOTS), 'SLOT_UNION')
    for addr, name, text in PLATES:
        require(all(ord(char) < 128 for char in text) and len(text) <= 500, 'ASCII_PLATE %08x' % addr)
    for addr, text in SLOT_EOLS:
        require(all(ord(char) < 128 for char in text), 'ASCII_EOL %08x' % addr)
    require(all(ord(char) < 128 for char in REGISTRY_SIBLING[2] + REGISTRY_SIBLING[4]), 'REGISTRY_ASCII')
    require(len(REGISTRY_SIBLING[2]) == 630 and len(REGISTRY_SIBLING[4]) == 347, 'REGISTRY_LENGTHS')
    require(hashlib.sha256(REGISTRY_SIBLING[2].encode('utf8')).hexdigest() == REGISTRY_SIBLING[3], 'REGISTRY_OLD_HASH')
    require(hashlib.sha256(REGISTRY_SIBLING[4].encode('utf8')).hexdigest() == REGISTRY_SIBLING[5], 'REGISTRY_NEW_HASH')


def verify_names_and_equates(post=False):
    for addr, value, name, label in EQ_SLOTS:
        eq = equates.getEquate(name)
        require(eq is None or (eq.getValue() & 0xffffffff) == value, 'EQUATE_VALUE ' + name)
        if name in NEW_NAMES and not post:
            require(eq is None, 'NEW_EQUATE_PREEXISTS ' + name)
        if post:
            require(eq is not None and len([ref for ref in eq.getReferences()
                    if ref.getAddress() == toAddr(addr) and ref.getOpIndex() == 0]) == 1,
                    'EQUATE_REFERENCE %08x' % addr)
    for row in PLAN['actions']:
        require_name(row['slot_label'], row['slot'], post)
    for slot_addr, (target, name) in REF_TARGETS.items():
        require_name(name, target, post)
    for addr, old, new in FUNC_RENAME:
        require_name(new, addr, post)


def verify_tables(post=False):
    for name, start, end, entries in CALLBACK_TABLES:
        require(end - start == len(entries) * 4, 'TABLE_RANGE ' + name)
        for address, raw, function_name in entries:
            require(memory.getInt(toAddr(address)) & 0xffffffff == raw and raw & 1, 'TABLE_RAW %08x' % address)
            fn = getFunctionAt(toAddr(raw & ~1))
            expected_name = RENAMES.get(raw & ~1, function_name) if post else OLD_NAMES.get(raw & ~1, function_name)
            require(fn is not None and fn.getName() == expected_name, 'TABLE_FUNCTION %08x' % address)
    # Four phase-1 words and the following boundary retain their mixed pre-existing Data/ref state.
    for value in range(0x09e47884, 0x09e47894, 4):
        state = describe(value)
        old = BASE[value]
        same('PHASE1_DATA %08x' % value, state['defined_data'], old['defined_data'])
        same('PHASE1_REF_BODY %08x' % value,
             [basic_ref(ref) for ref in references.getReferencesFrom(toAddr(value))],
             [dict((key, ref[key]) for key in ('from', 'to', 'operand', 'type', 'source', 'primary'))
              for ref in old['references_from']])
    boundary = describe(0x09e47894)
    require(boundary['defined_data'] is None and boundary['symbols'] == [] and
            boundary['references_from'] == [] and boundary['references_to'] == [] and
            boundary['containing_code_unit']['length'] == 1, 'TABLE_BOUNDARY_09e47894')


def verify_functions(post=False, extended=False):
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_5209')
    old_by_addr = dict((item['addr'], item) for item in ROOT_FUNCTIONS['functions'])
    plate_by_addr = dict((item['addr'], item) for item in PLAN['plates'])
    result = []
    for addr in sorted(old_by_addr):
        old = old_by_addr[addr]
        actual = function_state(addr, extended)
        require(actual is not None, 'FUNCTION_MISSING %08x' % addr)
        if actual is None:
            continue
        expected_name = RENAMES.get(addr, old['name']) if post else old['name']
        for key in ('symbol_id', 'source', 'symbol_type', 'body', 'body_size', 'body_sha256'):
            same('FUNCTION_%s %08x' % (key, addr), actual[key], old[key])
        expected_eols = copy.deepcopy(old['eols'])
        if post and addr == 0x0809fb16:
            expected_eols.extend([['%08x' % slot_addr, text] for slot_addr, text in SLOT_EOLS
                                  if 0x0809fb16 <= slot_addr < 0x0809fb82])
        same('FUNCTION_eols %08x' % addr, actual['eols'], expected_eols)
        same('FUNCTION_NAME %08x' % addr, actual['name'], expected_name)
        expected_incoming = copy.deepcopy(old['incoming'])
        if post:
            for slot_addr, (target, ref_type, source, operand) in AUX_MAP.items():
                if target == addr:
                    expected_incoming.append(planned_ref(slot_addr, target, operand, ref_type, source))
        same('FUNCTION_INCOMING %08x' % addr, actual['incoming'], expected_incoming)
        plate = plate_by_addr[addr]
        expected_plate = plate['text'] if post else plate['expected_old_text']
        same('FUNCTION_PLATE %08x' % addr, actual['plate'], expected_plate)
        if not post:
            require(actual['plate_sha256'] == plate['expected_old_sha256'], 'OLD_PLATE_HASH %08x' % addr)
        result.append(actual)
    return result


def verify_addresses(post=False):
    result = []
    for addr in sorted(BASE):
        actual = describe(addr)
        expected = expected_after(addr) if post else BASE[addr]
        normalized = normalize_new_ids(actual) if post else canonical(actual)
        if normalized != canonical(expected):
            keys = [key for key in expected if canonical(expected[key]) != canonical(normalized.get(key))]
            fail('%s_ADDRESS %08x fields=%s' % ('POST' if post else 'PRE', addr, ','.join(keys)))
            write_json('f13-seg3-mismatch-%s-%08x.json' % (MODE, addr),
                       {'expected': expected, 'actual': actual, 'normalized': normalized})
        result.append(actual)
    return result


def verify_prestate():
    same('SEGMENT_RANGE_SHA_PRE', range_hash(), SEGMENT_RANGE_SHA256)
    verify_names_and_equates(False)
    verify_tables(False)
    addresses = verify_addresses(False)
    functions = verify_functions(False, True)
    print('PREFLIGHT addresses=%d functions=%d tables=58 slots=138 EQ=98 REF=21 RENAME=19 PLATE=20 EOL=138 FUNC_RENAME=6 FAIL=%d' %
          (len(addresses), len(functions), len(FAILS)))


def ensure_user_label(addr_value, name, expected_symbols):
    addr = toAddr(addr_value)
    existing = symbols.getGlobalSymbol(name, addr)
    if existing is None:
        existing = symbols.createLabel(addr, name, SourceType.USER_DEFINED)
    require(existing.getSymbolType() == SymbolType.LABEL and existing.getAddress() == addr,
            'LABEL_TYPE_ADDRESS %08x' % addr_value)
    expected_ids = set(item['id'] for item in expected_symbols)
    for old in list(symbols.getSymbols(addr)):
        if old.getID() == existing.getID():
            continue
        if (old.getID() in expected_ids and str(old.getSource()) == 'DEFAULT' and
                old.getSymbolType() == SymbolType.LABEL):
            old.delete()
        else:
            raise RuntimeError('Unexpected alias at %08x' % addr_value)
    existing.setPrimary()
    return existing


def apply_ref(row):
    addr, target = toAddr(row['slot']), toAddr(row['value'])
    ensure_user_label(row['value'], row['const_name'], BASE[row['value']]['symbols'])
    old_refs = list(references.getReferencesFrom(addr))
    if old_refs:
        raise RuntimeError('REF prestate not empty at %08x' % row['slot'])
    ref = references.addMemoryReference(addr, target, RefType.DATA, SourceType.USER_DEFINED, 0)
    references.setPrimary(ref, True)


def apply_aux(row):
    target, ref_type, source, operand = AUX_MAP[row['slot']]
    fn = getFunctionAt(toAddr(target))
    if fn is None or fn.getEntryPoint() != toAddr(target) or not fn.getSymbol().isPrimary():
        raise RuntimeError('AUX target Function identity %08x' % target)
    if list(references.getReferencesFrom(toAddr(row['slot']))):
        raise RuntimeError('AUX prestate not empty %08x' % row['slot'])
    ref = references.addMemoryReference(toAddr(row['slot']), toAddr(target), RefType.DATA, SourceType.USER_DEFINED, operand)
    references.setPrimary(ref, True)


def apply_slot(row):
    addr = row['slot']
    if row['kind'] == 'EQ':
        eq = equates.getEquate(row['const_name'])
        if eq is None:
            eq = equates.createEquate(row['const_name'], row['value'])
        eq.addReference(toAddr(addr), 0)
        if addr in AUX_MAP:
            apply_aux(row)
    elif row['kind'] == 'REF':
        apply_ref(row)
    elif row['kind'] != 'RENAME':
        raise RuntimeError('Unknown slot action %08x' % addr)
    ensure_user_label(addr, row['slot_label'], row['before']['symbols'])
    listing.setComment(toAddr(addr), CodeUnit.EOL_COMMENT, row['eol'])
    COUNTS[row['kind']] += 1
    COUNTS['EOL'] += 1


def apply_all():
    events = [(addr, 0, 'PLATE') for addr, name, text in PLATES]
    events.extend((addr, 1, 'SLOT') for addr in SLOTS)
    for addr, order, kind in sorted(events):
        if kind == 'PLATE':
            if addr in RENAMES:
                getFunctionAt(toAddr(addr)).setName(RENAMES[addr], SourceType.USER_DEFINED)
                COUNTS['FUNC_RENAME'] += 1
            listing.setComment(toAddr(addr), CodeUnit.PLATE_COMMENT, PLATE_MAP[addr])
            COUNTS['PLATE'] += 1
        else:
            apply_slot(SLOTS[addr])


def verify_post(before):
    same('SEGMENT_RANGE_SHA_POST', range_hash(), SEGMENT_RANGE_SHA256)
    verify_names_and_equates(True)
    verify_tables(True)
    verify_addresses(True)
    functions = verify_functions(True, True)
    before_functions = dict((item['addr'], item) for item in before['functions'])
    old_functions = dict((item['addr'], item) for item in ROOT_FUNCTIONS['functions'])
    for actual in functions:
        addr = actual['addr']
        same('FUNCTION_BODY_REFS_POST %08x' % addr, actual['body_refs'], before_functions[addr]['body_refs'])
        expected_prototype = before_functions[addr]['prototype']
        if addr in RENAMES:
            old_name = old_functions[addr]['name']
            require(expected_prototype.count(old_name) == 1, 'PROTOTYPE_OLD_NAME_ONCE %08x' % addr)
            expected_prototype = expected_prototype.replace(old_name, RENAMES[addr], 1)
        same('FUNCTION_PROTOTYPE_POST %08x' % addr, actual['prototype'], expected_prototype)
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_POST')
    print('POSTCHECK slots=138 EQ=98 REF=21 RENAME=19 PLATE=20 EOL=138 FUNC_RENAME=6 TABLE_WORDS=58 NEW=17 FAIL=%d' % len(FAILS))


def capture():
    return {'script_sha256': SCRIPT_HASH, 'input_hashes': [list(row) for row in INPUT_HASHES],
            'function_count': currentProgram.getFunctionManager().getFunctionCount(),
            'range_sha256': range_hash(),
            'addresses': [describe(addr) for addr in sorted(BASE)],
            'functions': [function_state(item['addr'], True) for item in ROOT_FUNCTIONS['functions']]}


def reject(phase):
    if FAILS:
        write_json('f13-seg3-%s-failures.json' % MODE, {'phase': phase, 'FAIL': len(FAILS), 'failures': FAILS})
        raise RuntimeError('%s FAIL=%d' % (phase, len(FAILS)))


print('=== RefineF13Seg3 mode=%s ===' % MODE)
for relative, expected_hash in INPUT_HASHES:
    require(file_hash(os.path.join(ROOT, relative)) == expected_hash, 'INPUT_HASH ' + relative)
verify_literal_tables()
reject('FROZEN_TABLES')
if MODE == 'check':
    receipt = read_json('f13-seg3-apply-receipt.json')
    require(receipt['script_sha256'] == SCRIPT_HASH, 'PERSISTED_SCRIPT_HASH')
    require(receipt['input_hashes'] == [list(row) for row in INPUT_HASHES], 'PERSISTED_INPUT_HASHES')
    state = capture()
    verify_post(receipt['before'])
    require(canonical(state) == canonical(receipt['after']), 'PERSISTED_EXACT_POST_STATE')
    reject('PERSISTED_CHECK')
    COUNTS = receipt['counts']
    write_json('f13-seg3-persisted-check.json', {'status': 'PERSISTED_CHECK_OK', 'FAIL': 0,
               'script_sha256': SCRIPT_HASH, 'counts': COUNTS, 'exact_saved_state': True})
else:
    verify_prestate()
    reject('PREFLIGHT')
    before = capture()
    if MODE == 'dry':
        write_json('f13-seg3-dry-state.json', before)
        COUNTS.update({'EQ': 98, 'REF': 21, 'RENAME': 19, 'PLATE': 20, 'EOL': 138, 'FUNC_RENAME': 6})
        write_json('f13-seg3-dry-check.json', {'status': 'DRY_PREFLIGHT_OK', 'FAIL': 0,
                   'script_sha256': SCRIPT_HASH, 'input_hashes': [list(row) for row in INPUT_HASHES],
                   'counts': COUNTS, 'address_count': len(before['addresses']),
                   'function_count': len(before['functions']), 'callback_words': 58, 'new_definitions': 17,
                   'complete_state': 'f13-seg3-dry-state.json'})
    else:
        write_json('f13-seg3-apply-before.json', before)
        transaction = currentProgram.startTransaction('Refine F13-Seg-3 final PASS actions')
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
        write_json('f13-seg3-apply-receipt.json', {'status': 'APPLIED_TRANSACTION_POSTCHECK_OK',
                   'FAIL': 0, 'script_sha256': SCRIPT_HASH, 'input_hashes': [list(row) for row in INPUT_HASHES],
                   'counts': COUNTS, 'before': before, 'after': after})
reject('FINAL')
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
