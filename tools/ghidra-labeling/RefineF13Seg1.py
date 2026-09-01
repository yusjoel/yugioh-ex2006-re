# -*- coding: ascii -*-
#@runtime Jython
#@category Ygo-ex2006
# F13-Seg-1. Final PASS proposal: fd84b9c4fcffb99261851465d7f1bf2033fd0133009e4b0b070b1f06e6bdb1a7
# dry/check require direct headless -noanalysis -readOnly. Never stage or commit.
# No data creation, disassembly, memory writes, or function creation.

EQ_SLOTS = [(134862680, 5406, 'LAST_TURN_CID', 'last_turn_cid_9d758'),
 (134862716, 5406, 'LAST_TURN_CID', 'last_turn_cid_9d77c'),
 (134862772, 6398, 'POWER_BOND_CID', 'power_bond_cid_9d7b4'),
 (134862940, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9d85c'),
 (134862952, 32827, 'OAM_EQUIP_SET_SLOT_P2', 'sprite_counter_p2_9d868'),
 (134862972, 4667, 'CRUSH_CARD_CID', 'crush_card_cid_9d87c'),
 (134862992, 6284, 'DECK_DEVASTATION_VIRUS_CID', 'deck_devastation_cid_9d890'),
 (134863012, 6357, 'PIKERU_SECOND_SIGHT_CID', 'pikeru_second_sight_cid_9d8a4'),
 (134863112, 5788, 'FINAL_COUNTDOWN_CID', 'final_countdown_cid_9d908'),
 (134863120, 32827, 'OAM_EQUIP_SET_SLOT_P2', 'sprite_counter_p2_9d910'),
 (134863212, 5121, 'INFINITE_CARDS_CID', 'infinite_cards_cid_9d96c'),
 (134863216, 5535, 'HIEROGLYPH_LITHOGRAPH_CID', 'hieroglyph_cid_9d970'),
 (134863224, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9d978'),
 (134863312, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'player_off_9d9d0'),
 (134863316, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9d9d4'),
 (134863320, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9d9d8'),
 (134863352, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9d9f8'),
 (134863500, 32785, 'OAM_EQUIP_SPRITE_P2_11', 'sprite_p2_11_9da8c'),
 (134863508, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9da94'),
 (134863512, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9da98'),
 (134863548, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9dabc'),
 (134863680, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9db40'),
 (134863684, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9db44'),
 (134863688, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9db48'),
 (134863692, 4078, 'COCOON_OF_EVOLUTION_CID', 'cocoon_cid_9db4c'),
 (134863696, 5390, 'SPIRITUAL_ENERGY_SETTLE_CID', 'spiritual_energy_cid_9db50'),
 (134864028, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9dc9c'),
 (134864032, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9dca0'),
 (134864036, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9dca4'),
 (134864040, 4354, 'SWORDS_OF_REVEALING_LIGHT_CID', 'swords_cid_9dca8'),
 (134864164, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9dd24'),
 (134864608, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9dee0'),
 (134864616, 5277, 'EKIBYO_DRAKMORD_CID', 'ekibyo_cid_9dee8'),
 (134864624, 4294959104, 'OAM_ATTR2_TILE_CLEAR', 'low13_clear_mask_9def0'),
 (134864632, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9def8'),
 (134864636, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9defc'),
 (134864640, 32838, 'OAM_EQUIP_SPRITE_P2_46', 'sprite_p2_46_9df00'),
 (134864772, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9df84'),
 (134864780, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9df8c'),
 (134864860, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9dfdc'),
 (134864868, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9dfe4'),
 (134864968, 7460, 'EQUIP_ACTIVATION_SCAN_CURSOR_OFF', 'scan_cursor_off_9e048'),
 (134864972, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e04c'),
 (134865048, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'player_off_9e098'),
 (134865052, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e09c'),
 (134865108, 32770, 'OAM_EQUIP_SPRITE_P2_02', 'sprite_p2_02_9e0d4'),
 (134865236, 4950, 'GAMBLE_CID', 'gamble_cid_9e154'),
 (134865240, 7428, 'PUZZLE_READY_FLAG_OFF', 'timer_notice_gate_off_9e158'),
 (134865244, 7404, 'P1LP_TIMER_OFF', 'timer_off_9e15c'),
 (134865248, 32779, 'SPRITE_ATTR_DUEL_PHASE_P2', 'sprite_phase_p2_9e160'),
 (134865328, 7400, 'P1LP_BLOCK2_OFF_1CE8', 'player_off_9e1b0'),
 (134865332, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9e1b4'),
 (134865336, 5041, 'TIMEATER_CID', 'timeater_cid_9e1b8'),
 (134865340, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e1bc'),
 (134865508, 7472, 'EQUIP_CHAIN_CANCEL_OFF', 'chain_cancel_off_9e264'),
 (134865512, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e268'),
 (134865552, 32782, 'OAM_EQUIP_SPRITE_P2_0E', 'sprite_p2_0e_9e290'),
 (134865556, 7508, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_off_9e294'),
 (134865560, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e298'),
 (134865636, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e2e4'),
 (134865664, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e300'),
 (134865704, 7508, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_off_9e328'),
 (134865708, 7512, 'ELIGIB_ACT_COUNT_OFF', 'eligib_count_off_9e32c'),
 (134865712, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e330'),
 (134865736, 7516, 'ELIGIB_ACT_TYPE_OFF', 'eligib_type_off_9e348'),
 (134865772, 7472, 'EQUIP_CHAIN_CANCEL_OFF', 'chain_cancel_off_9e36c'),
 (134865776, 7464, 'EQUIP_CHAIN_STEP_OFF', 'chain_step_off_9e370'),
 (134865780, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e374'),
 (134865804, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e38c'),
 (134865840, 7412, 'P2LP_BLOCK2_OFF_1CF4', 'field_phase_off_9e3b0'),
 (134865884, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e3dc'),
 (134865956, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e424'),
 (134865976, 309, 'CARD_DISPLAY_OP31_PARAM_0135', 'display_op31_param_9e438'),
 (134865984, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e440'),
 (134866048, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e480'),
 (134866108, 7472, 'EQUIP_CHAIN_CANCEL_OFF', 'chain_cancel_off_9e4bc'),
 (134866112, 7464, 'EQUIP_CHAIN_STEP_OFF', 'chain_step_off_9e4c0'),
 (134866124, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e4cc'),
 (134866144, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e4e0'),
 (134866184, 7412, 'P2LP_BLOCK2_OFF_1CF4', 'field_phase_off_9e508'),
 (134866188, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e50c'),
 (134866244, 7472, 'EQUIP_CHAIN_CANCEL_OFF', 'chain_cancel_off_9e544'),
 (134866248, 32784, 'OAM_EQUIP_SPRITE_P2_10', 'sprite_p2_10_9e548'),
 (134866252, 7452, 'CARD_PLAY_PHASE_CTR_OFF', 'phase_off_9e54c'),
 (134866376, 7412, 'P2LP_BLOCK2_OFF_1CF4', 'field_phase_off_9e5c8'),
 (134866380, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9e5cc'),
 (134866388, 6484, 'VWXYZ_DRAGON_CATAPULT_CANNON_CID', 'vwxyz_cid_9e5d4'),
 (134866488, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9e638'),
 (134866496, 6484, 'VWXYZ_DRAGON_CATAPULT_CANNON_CID', 'vwxyz_cid_9e640'),
 (134866564, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9e684'),
 (134866572, 5406, 'LAST_TURN_CID', 'last_turn_cid_9e68c'),
 (134866644, 2152, 'PLAYER_BLOCK_STRIDE', 'player_stride_9e6d4'),
 (134866652, 5406, 'LAST_TURN_CID', 'last_turn_cid_9e6dc')]

REF_SLOTS = [(134862944, 33670636, 'gDuelFieldSpellZoneBase', 'chain_slot11_base_9d860'),
 (134862948, 33675712, 'gEquipNodePool', 'chain_nodes_base_9d864'),
 (134863116, 33677772, 'gP1LpTimer', 'lp_timer_base_9d90c'),
 (134863356, 134863360, 'switchD_0809d9f2__switchdataD_0809da00', 'activation_phase_switch_9d9fc'),
 (134863820, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_base_9dbcc'),
 (134864612, 33670416, 'gDuelFieldSlots', 'field_slots_base_9dee4'),
 (134864620, 33670432, 'gDuelFieldSlotState', 'field_slot_state_base_9deec'),
 (134864776, 165967536, 'equip_activation_phase11_callbacks', 'phase11_callbacks_9df88'),
 (134864864, 165967672, 'equip_activation_phase12_callbacks', 'phase12_callbacks_9dfe0'),
 (134864964, 165967772, 'equip_activation_phase20_callbacks', 'phase20_callbacks_9e044'),
 (134865112, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_base_9e0d8'),
 (134865116, 33664992, 'gEquipLpScoreBase', 'lp_score_base_9e0dc'),
 (134865344, 134865348, 'switchD_0809e1aa__switchdataD_0809e1c4', 'field_phase_switch_9e1c0'),
 (134865640, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_base_9e2e8'),
 (134865924, 33677984, 'gDuelCardCtxBase', 'duel_card_ctx_base_9e404'),
 (134866384, 33670416, 'gDuelFieldSlots', 'field_slots_base_9e5d0'),
 (134866492, 33670416, 'gDuelFieldSlots', 'field_slots_base_9e63c'),
 (134866568, 33670416, 'gDuelFieldSlots', 'field_slots_base_9e688'),
 (134866648, 33670416, 'gDuelFieldSlots', 'field_slots_base_9e6d8')]

RENAME_SLOTS = [(134863220, 'gp1lp_base_9d974', 'Player-state base; read the hand-count word at base+(player&1)*PLAYER_BLOCK_STRIDE+0xc.'),
 (134863308, 'gp1lp_base_9d9cc', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863348, 'gp1lp_base_9d9f4', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863504, 'gp1lp_base_9da90', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863544, 'gp1lp_base_9dab8', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863676, 'gp1lp_base_9db3c', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864024, 'gp1lp_base_9dc98', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864160, 'gp1lp_base_9dd20', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864628, 'gp1lp_base_9def4', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864768, 'gp1lp_base_9df80', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864856, 'gp1lp_base_9dfd8', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864960, 'gp1lp_base_9e040', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865044, 'gp1lp_base_9e094', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865252, 'gp1lp_base_9e164', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865324, 'gp1lp_base_9e1ac', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865504, 'gp1lp_base_9e260', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865632, 'gp1lp_base_9e2e0', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865660, 'gp1lp_base_9e2fc', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865700, 'gp1lp_base_9e324', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865836, 'gp1lp_base_9e3ac', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865880, 'gp1lp_base_9e3d8', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865928, 'gp1lp_base_9e408', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865952, 'gp1lp_base_9e420', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865980, 'gp1lp_base_9e43c', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866044, 'gp1lp_base_9e47c', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866072, 'gp1lp_base_9e498', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866140, 'gp1lp_base_9e4dc', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866180, 'gp1lp_base_9e504', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866240, 'gp1lp_base_9e540', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866372, 'gp1lp_base_9e5c4', 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.')]

PLATES = [(134862616,
  'scan_equip_zone_for_last_turn_activation',
  'r0=player. Require LAST_TURN_CID in chain slot11, at least one occupied monster slot for this player, and none for 1-player. On success '
  'enqueue the card sprite and type11(player,CID,5,0), then return0. Return1 when any gate fails.'),
 (134862692,
  'scan_equip_zone_for_last_turn_sprite',
  'r0=player. Test LAST_TURN_CID in chain slot11. If absent return1. Otherwise enqueue the equip-zone card sprite and '
  "type11(player,CID,5,0), then return0. This path does not test either player's occupied monster count."),
 (134862748,
  'scan_equip_chain_for_power_bond_sprite_and_lp_indicator',
  'r0=player. If POWER_BOND_CID is absent from chain slot11, return1. Otherwise read its entity value, enqueue the card sprite, submit the '
  'LP indicator as (player,entity,0,CID), and enqueue the equip-slot sprite as (player,11,CID,0). Return0 after these submissions.'),
 (134862828,
  'enqueue_equip_chain_counter_sprites_by_card',
  'r0=player, r1=CID, r2=counter_base. Require CID in chain slot11. Follow the head at '
  'gDuelFieldSpellZoneBase+(player&1)*PLAYER_BLOCK_STRIDE+0xa through 8-byte gEquipNodePool nodes, using next=u16[node+6]. Match '
  'u16[node]==CID and (byte[node+2]&15)==1. Submit type0x3b/0x803b with (CID&0xffff,1,(counter_base-(byte[node+2]>>5))&0xffff) for every '
  'match. r2 is not a zone filter. Always return1.'),
 (134862956,
  'scan_equip_chain_list_for_sprite_crush_card',
  'r0=player. Call enqueue_equip_chain_counter_sprites_by_card(player,CRUSH_CARD_CID,3). The third argument is a counter base; the callee '
  'fixes the node-type filter to1. Return the callee result, always1. Sprite submissions occur for matching chain nodes.'),
 (134862976,
  'scan_equip_chain_list_for_sprite_deck_devastation_virus',
  'r0=player. Call enqueue_equip_chain_counter_sprites_by_card(player,DECK_DEVASTATION_VIRUS_CID,3). The third argument is a counter base, '
  'not a zone index. Return the callee result, always1. Matching chain nodes enqueue counter sprites.'),
 (134862996,
  'scan_equip_chain_list_for_sprite_pikeru_second_sight',
  'r0=player. Call enqueue_equip_chain_counter_sprites_by_card(player,PIKERU_SECOND_SIGHT_CID,2). The third argument is a counter base, '
  'not a zone index. Return the callee result, always1. Matching chain nodes enqueue counter sprites.'),
 (134863016,
  'scan_equip_zone_for_final_countdown_sprite',
  'r0=starting player. Visit that player and player^1. For a nonnegative FINAL_COUNTDOWN_CID entity value in chain slot11, compute '
  'count=word[gP1LpTimer]-entity+1. Enqueue type0x3b/0x803b with (CID,1,count&0xffff). If signed count>19, also enqueue '
  'type11(player,CID,1,1). Always return1 after both sides. The timer is gP1LifePoints+P1LP_TIMER_OFF.'),
 (134863124,
  'scan_equip_zone_for_infinite_cards_lp_display_update',
  'r0=player. Return1 if count_field_copies_of_card(INFINITE_CARDS_CID) is nonzero. Otherwise limit=6, raised to7 by '
  'HIEROGLYPH_LITHOGRAPH_CID in chain slot11 and overridden to5 by available Enervating Mist(0x1800) zones for 1-player. Read count at '
  'gP1ZoneHandCount+(player&1)*PLAYER_BLOCK_STRIDE. If unsigned count>limit, submit set_lp_display_row_if_nonzero(player,count-limit) and '
  'return0; else return1.'),
 (134863236,
  'run_equip_activation_phase_by_counter',
  'No inputs. Read player at gP1LifePoints+0x1ce8, bit23 at base+(player&1)*0x868+0x11c, and phase at+0x1d1c. For nonzero phase, a '
  'successful Last Turn scan returns0. Phase0..20 selects21 even MOV-pc targets; default/unused phases return1. Active paths update '
  'phase/cursors, submit sprites and test slots. Phase11/20 resume34/4 callback tables; phase12 restarts25 callbacks each tick. A callback '
  'returning0 yields0. All paths restore the shared0x120-byte frame.'),
 (134865016,
  'dispatch_field_spell_phase_by_display_state',
  'No inputs. Read player at gP1LifePoints+0x1ce8 and CARD_PLAY_PHASE_CTR_OFF. Phase0 enqueues type2/0x8002, clears0x1cc bytes at '
  'gEquipLpScoreBase if the player context word is1, advances phase and returns0. Phase1 tests GAMBLE_CID in chain slot11 and sets player '
  'flag0x17 on a hit. It submits timer notices at backup+1 when the +0x1d04 gate is0, and at backup+4 unconditionally. Phase1 and all '
  'other phases return1.'),
 (134865256,
  'tick_duel_field_spell_activation_state',
  'No inputs. Read player, its flag bit23, TIMEATER_CID chain membership and CARD_PLAY_PHASE_CTR_OFF. Dispatch phase0..30 through31 even '
  'MOV-pc targets; unused/default entries return0. Routes display selection, AI progress and equip gates, updating phase and '
  'control/cancel fields. Phase30 scans five field slots for VWXYZ_DRAGON_CATAPULT_CANNON_CID in field phases2/4. Return1 on the '
  'flag/cancel exit or completed final path; pending work and ordinary phase changes return0.'),
 (134866400,
  'scan_field_slots_for_vwxyz_dragon_catapult_cannon_activation',
  'r0=player. Scan five 20-byte entries at gDuelFieldSlots+(player&1)*PLAYER_BLOCK_STRIDE. Require low13 '
  'CID=VWXYZ_DRAGON_CATAPULT_CANNON_CID and u16[slot+8]!=0. Call apply_equip_activation_via_packed_attr with '
  '(slot_index<<16)|0x600000|(player<<31)|CID, the packed entry flags, and0. Return0 only when that call returns nonzero; otherwise '
  'continue scanning and return1 after all five fail.'),
 (134866516,
  'find_equip_slot_idx_with_entity_id_one',
  'r0=player. Scan slot indices0..4 at gDuelFieldSlots+(player&1)*PLAYER_BLOCK_STRIDE with stride20. Skip entries whose low13 CID bits '
  'are0. Return the first index where get_node_entity_id_in_slot(player,index,LAST_TURN_CID)==1. Return-1 when no entry matches. The input '
  'is a player value, not a slot pointer.'),
 (134866596,
  'find_equip_slot_idx_with_entity_id_zero',
  'r0=player. Scan slot indices0..4 at gDuelFieldSlots+(player&1)*PLAYER_BLOCK_STRIDE with stride20. Skip entries whose low13 CID bits '
  'are0. Return the first index where get_node_entity_id_in_slot(player,index,LAST_TURN_CID)==0. Return-1 when no entry matches. A missing '
  'node returns-1 from the lookup and does not satisfy the zero test.')]

FUNC_RENAME = [(134862828, 'scan_equip_chain_list_for_sprite_by_card_and_zone', 'enqueue_equip_chain_counter_sprites_by_card'),
 (134866400, 'scan_equip_zone_for_toon_card_activation', 'scan_field_slots_for_vwxyz_dragon_catapult_cannon_activation')]

SLOT_EOLS = [(134862680, 'CID for the Last Turn chain-membership or entity-value lookup.'),
 (134862716, 'CID for the Last Turn chain-membership or entity-value lookup.'),
 (134862772, 'CID for chain slot11 membership, entity lookup and sprite/LP-indicator submissions.'),
 (134862940, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134862944, 'Chain slot11 base, gDuelFieldSlots+11*20; read u16[base+(player&1)*stride+0xa] as the node-head index.'),
 (134862948, 'Global 8-byte node pool indexed by chain-head/next indices; no player stride is added to this base.'),
 (134862952, 'Nonzero-player counter-sprite selector; the zero-player branch uses0x3b.'),
 (134862972, 'CID argument for the chain counter-sprite wrapper.'),
 (134862992, 'CID argument for the chain counter-sprite wrapper.'),
 (134863012, 'CID argument for the chain counter-sprite wrapper.'),
 (134863112, 'CID for chain slot11 entity lookup and progress-sprite arguments.'),
 (134863116, 'Absolute u32 timer address, equal to gP1LifePoints+P1LP_TIMER_OFF; used for Final Countdown progress.'),
 (134863120, 'Nonzero-player counter-sprite selector; the zero-player branch uses0x3b.'),
 (134863212, 'CID passed to count_field_copies_of_card; nonzero count bypasses the hand-limit row update.'),
 (134863216, 'CID passed to check_value_in_slot_chain(player,11,CID); a hit raises the hand limit to7.'),
 (134863220, 'Player-state base; read the hand-count word at base+(player&1)*PLAYER_BLOCK_STRIDE+0xc.'),
 (134863224, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134863308, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863312, 'Byte offset from gP1LifePoints to the player word used by this dispatcher.'),
 (134863316, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134863320, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134863348, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863352, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134863356, '21 even-address phase0..20 targets, dispatched by MOV pc,r0 while retaining Thumb state.'),
 (134863500, 'Nonzero-player sprite selector; the zero-player branch uses0x11. Argument0 of enqueue_sprite_attr_record.'),
 (134863504, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863508, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134863512, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134863544, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863548, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134863676, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134863680, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134863684, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134863688, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134863692, 'Compare with the low13 CID bits of a field-slot word; not the same-valued animation sentinel.'),
 (134863696, 'CID comparison selecting the multi-step display path for field slots5..9.'),
 (134863820, 'Duel card context base; reads word[base+8+4*player] to select the display/AI route.'),
 (134864024, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864028, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134864032, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134864036, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134864040, 'CID comparison in the opposite-player slot5..9 scan.'),
 (134864160, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864164, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134864608, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134864612, 'Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index.'),
 (134864616, 'CID matched in field slots5..9 before pair lookup and eligibility checks.'),
 (134864620, 'Field-slot state-word base, gDuelFieldSlots+0x10; consumer tests bit5 with the same player/slot displacement.'),
 (134864624, 'AND mask clearing low13 CID bits of a slot halfword before the eligibility call; the saved CID is restored afterward.'),
 (134864628, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864632, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134864636, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134864640, 'Nonzero-player sprite selector; the zero-player branch uses0x46.'),
 (134864768, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864772, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134864776, '34 Thumb callbacks, indexed by the persistent phase11 cursor; a callback returning0 yields for this tick.'),
 (134864780, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134864856, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864860, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134864864, '25 Thumb callbacks; phase12 restarts the local table index at0 on each tick and yields on callback result0.'),
 (134864868, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134864960, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134864964, '4 Thumb callbacks, indexed by the persistent phase20 cursor; a callback returning0 yields for this tick.'),
 (134864968, 'Byte offset from gP1LifePoints to the u32 slot/callback scan cursor.'),
 (134864972, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865044, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865048, 'Byte offset from gP1LifePoints to the player word used by this dispatcher.'),
 (134865052, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865108, 'Nonzero-player sprite selector; the zero-player branch uses2. Argument0 of enqueue_sprite_attr_record.'),
 (134865112, 'Duel card context base; reads word[base+8+4*player] to select the display/AI route.'),
 (134865116, 'Base of the 0x1cc-byte zero-fill when the selected player context word equals1.'),
 (134865236, 'CID passed to check_value_in_slot_chain(player,11,CID).'),
 (134865240, 'Byte offset from gP1LifePoints; a nonzero word suppresses only the backup+1 timer notice.'),
 (134865244, 'Byte offset from gP1LifePoints to the u32 timer; offset+4 addresses its backup field.'),
 (134865248, 'Nonzero-player timer-notice sprite selector; the zero-player branch uses0xb.'),
 (134865252, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865324, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865328, 'Byte offset from gP1LifePoints to the player word used by this dispatcher.'),
 (134865332, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134865336, 'CID passed to check_value_in_slot_chain(player,11,CID); saves its result as a phase gate.'),
 (134865340, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865344, '31 even-address phase0..30 targets, dispatched by MOV pc,r0 while retaining Thumb state.'),
 (134865504, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865508, 'Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases.'),
 (134865512, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865552, 'Nonzero-player sprite selector; the zero-player branch uses0xe. Argument0 of enqueue_sprite_attr_record.'),
 (134865556, 'Byte offset from gP1LifePoints to the eligibility state-control word.'),
 (134865560, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865632, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865636, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865640, 'Duel card context base; reads word[base+8+4*player] to select the display/AI route.'),
 (134865660, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865664, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865700, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865704, 'Byte offset from gP1LifePoints to the eligibility state-control word.'),
 (134865708, 'Byte offset from gP1LifePoints; phase3 writes1 to the eligibility activation-count word.'),
 (134865712, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865736, 'Byte offset from gP1LifePoints; phase3 compares activation type against16 and18.'),
 (134865772, 'Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases.'),
 (134865776, 'Byte offset from gP1LifePoints; this path clears the chain-step word before advancing phase.'),
 (134865780, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865804, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865836, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865840, 'Byte offset from gP1LifePoints; this consumer reads the field-phase word, not a gDuelFieldSlots-relative cursor.'),
 (134865880, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865884, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865924, 'Duel card context base; reads word[base+8+4*player] to select the display/AI route.'),
 (134865928, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865952, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865956, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134865976, 'Display op0x31 parameter, forwarded from r1 by trigger_card_display_op31_if_not_active.'),
 (134865980, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134865984, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134866044, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866048, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134866072, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866108, 'Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases.'),
 (134866112, 'Byte offset from gP1LifePoints; this path clears the chain-step word before advancing phase.'),
 (134866124, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134866140, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866144, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134866180, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866184, 'Byte offset from gP1LifePoints; this consumer reads the field-phase word, not a gDuelFieldSlots-relative cursor.'),
 (134866188, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134866240, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866244, 'Byte offset from gP1LifePoints to the chain-cancel word cleared or tested by these phases.'),
 (134866248, 'Nonzero-player sprite selector; the zero-player branch uses0x10. Argument0 of enqueue_sprite_attr_record.'),
 (134866252, 'Byte offset from gP1LifePoints to the dispatcher phase word.'),
 (134866372, 'gP1LifePoints base; preserve the existing DATA reference and use the offsets loaded by this path.'),
 (134866376, 'Byte offset from gP1LifePoints; this consumer reads the field-phase word, not a gDuelFieldSlots-relative cursor.'),
 (134866380, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134866384, 'Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index.'),
 (134866388, 'Compare with low13 CID bits of five field-slot words; this CID names VWXYZ-Dragon Catapult Cannon.'),
 (134866488, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134866492, 'Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index.'),
 (134866496, 'Compare with low13 CID bits of five field-slot words; this CID names VWXYZ-Dragon Catapult Cannon.'),
 (134866564, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134866568, 'Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index.'),
 (134866572, 'CID for the Last Turn chain-membership or entity-value lookup.'),
 (134866644, 'Byte stride of player blocks; the consumer multiplies it by player&1.'),
 (134866648, 'Field-slot array base; consumers add (player&1)*PLAYER_BLOCK_STRIDE and 20*slot_index.'),
 (134866652, 'CID for the Last Turn chain-membership or entity-value lookup.')]

INPUT_HASHES = [('doc/dev/refine/F13-Seg-1.proposal.md', 'fd84b9c4fcffb99261851465d7f1bf2033fd0133009e4b0b070b1f06e6bdb1a7'),
 ('doc/dev/refine/F13-Seg-1.review.md', '1b5146d8697bf6ccbe03f259dc941fc287e30ffb4f38fe6ae74030f34b86c022'),
 ('output/refine-run-20260831-194634/f13-seg1-plan.json', '6eb02a8e5b14f900f14119eac9c648589c5abc8d14a7cdd850dc8cca9c47f75f'),
 ('output/refine-run-20260831-194634/f13-seg1-plates.json', '478ce86a54ba46ff7d370ef6a36454c25001f39e40b1c0ae0f8d3750457e244e'),
 ('output/refine-run-20260831-194634/root-f13-seg1-targets-before.json',
  '198fc98191cd255f4f87ae6ea575b4224c2bf24595253423adf2ce4c4caab066')]

# Runtime follows the literal proposal tables in RefineF13Seg1.py.
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


def fail(message):
    FAILS.append(message)
    print('FAIL: ' + message)


def require(condition, message):
    if not condition:
        fail(message)


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def read_json(path):
    with open(path, 'r') as stream:
        return json.load(stream)


def write_json(name, value):
    with open(os.path.join(RUN, name), 'w') as stream:
        stream.write(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n')


for relative, expected_hash in INPUT_HASHES:
    require(file_hash(os.path.join(ROOT, relative)) == expected_hash, 'INPUT_HASH ' + relative)
if FAILS:
    raise RuntimeError('Frozen input mismatch; no writes performed')
PLAN = read_json(os.path.join(RUN, 'f13-seg1-plan.json'))
SCRIPT_HASH = file_hash(getSourceFile().getAbsolutePath())


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
    # No uninitialized RAM value is read, including either Data=None target.
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
    result.pop('input_label', None)
    for key in ('symbols', 'equates', 'references_from', 'references_to'):
        if key in result:
            result[key] = sorted(result[key], key=lambda item: json.dumps(item, sort_keys=True))
    return result


BASE = {}


def add_base(value):
    addr = value['address']
    require(addr not in BASE or canonical(BASE[addr]) == canonical(value), 'BASE_DUPLICATE %08x' % addr)
    BASE[addr] = copy.deepcopy(value)


SLOTS = dict((s['addr'], s) for s in PLAN['slots'])
TARGETS = {}
for slot in PLAN['slots']:
    add_base(slot['expected'])
    if slot['kind'] == 'REF':
        add_base(slot['target_expected'])
        TARGETS[slot['value']] = slot
    elif slot['kind'] == 'RENAME':
        require(slot['value'] == 0x0201c4e0, 'RENAME_TARGET_VALUE')
for item in PLAN['switch_expected'] + PLAN['carve_expected_data'] + [PLAN['carve_boundary_expected']]:
    add_base(item)
lp_snapshot = read_json(os.path.join(RUN, 'root-f13-seg1-targets-before.json'))
add_base(next(item for item in lp_snapshot['extra_targets'] if item['address'] == 0x0201c4e0))
RENAMES = dict((addr, new) for addr, old, new in FUNC_RENAME)
PLATE_MAP = dict((addr, text) for addr, name, text in PLATES)
EOL_MAP = dict(SLOT_EOLS)
NEW_IDS = set()
LABEL_AFTER = {}
for addr, slot in SLOTS.items():
    LABEL_AFTER[addr] = {'id': 0, 'name': slot['slot_label'], 'qualified_name': slot['slot_label'],
                         'source': 'USER_DEFINED', 'type': 'Label', 'primary': True}
    NEW_IDS.add(addr)
for addr, slot in TARGETS.items():
    old_symbols = BASE[addr]['symbols']
    if slot['target_action'] == 'reuse_existing_user_label':
        expected = next(s for s in old_symbols if s['primary'])
        require(expected['name'] == slot['symbol'] and expected['source'] == 'USER_DEFINED', 'REUSE_TARGET')
        LABEL_AFTER[addr] = copy.deepcopy(expected)
    else:
        ident = old_symbols[0]['id'] if slot['target_action'] == 'normalize_existing_symbol_global' else 0
        if not ident:
            NEW_IDS.add(addr)
        LABEL_AFTER[addr] = {'id': ident, 'name': slot['symbol'], 'qualified_name': slot['symbol'],
                             'source': 'USER_DEFINED', 'type': 'Label', 'primary': True}


def planned_ref(slot, navigation=False):
    item = {'from': '%08x' % slot['addr'], 'to': '%08x' % slot['value'], 'operand': 0,
            'type': 'DATA', 'source': 'USER_DEFINED', 'primary': True}
    if navigation:
        item['target_primary'] = copy.deepcopy(LABEL_AFTER[slot['value']])
        item['target_primary'].pop('primary')
    return item


def memory_target(ref):
    # Stack/register address strings are preserved verbatim, not ROM integers.
    try:
        return int(ref['to'], 16)
    except ValueError:
        return None


def expected_after(addr):
    result = canonical(BASE[addr])
    if addr in LABEL_AFTER:
        result['symbols'] = [copy.deepcopy(LABEL_AFTER[addr])]
    if addr in SLOTS:
        slot = SLOTS[addr]
        result['comments']['EOL'] = EOL_MAP[addr]
        if slot['kind'] == 'EQ':
            result['equates'] = [{'name': slot['symbol'], 'value': slot['value']}]
        elif slot['kind'] == 'REF':
            result['references_from'] = [r for r in result['references_from']
                if not (r['operand'] == 0 and r['to'] == '%08x' % slot['value'])]
            result['references_from'].append(planned_ref(slot, True))
    for slot in PLAN['slots']:
        if slot['kind'] == 'REF' and slot['value'] == addr:
            result['references_to'] = [r for r in result['references_to']
                if not (r['operand'] == 0 and r['from'] == '%08x' % slot['addr'])]
            result['references_to'].append(planned_ref(slot))
    # Resolve derived navigation separately; preserved reference bodies are unchanged.
    for ref in result['references_from']:
        target = memory_target(ref)
        if target in LABEL_AFTER:
            ref['target_primary'] = copy.deepcopy(LABEL_AFTER[target])
            ref['target_primary'].pop('primary')
        elif target in RENAMES and ref['target_primary'] is not None:
            ref['target_primary']['name'] = RENAMES[target]
            ref['target_primary']['qualified_name'] = RENAMES[target]
    owner = result['containing_function']
    if owner is not None and int(owner['entry'], 16) in RENAMES:
        owner['name'] = RENAMES[int(owner['entry'], 16)]
    if addr in PLATE_MAP:
        result['comments']['PLATE'] = PLATE_MAP[addr]
    return canonical(result)


def normalize_new_ids(value):
    result = copy.deepcopy(value)
    addr = result['address']
    if addr in NEW_IDS:
        for symbol in result['symbols']:
            if symbol['name'] == LABEL_AFTER[addr]['name']:
                require(symbol['id'] > 0, 'NEW_ID %08x' % addr)
                symbol['id'] = 0
    for ref in result['references_from']:
        target = memory_target(ref)
        primary = ref['target_primary']
        if target in NEW_IDS and primary is not None and primary['name'] == LABEL_AFTER[target]['name']:
            require(primary['id'] > 0, 'NEW_NAV_ID %08x' % target)
            primary['id'] = 0
    return canonical(result)


def verify_addresses(post=False):
    observed = []
    for addr in sorted(BASE):
        actual = describe(addr)
        expected = expected_after(addr) if post else canonical(BASE[addr])
        normalized = normalize_new_ids(actual) if post else canonical(actual)
        if normalized != expected:
            keys = [key for key in expected if expected[key] != normalized.get(key)]
            fail('%s_ADDRESS %08x fields=%s' % ('POST' if post else 'PRE', addr, ','.join(keys)))
            write_json('f13-seg1-mismatch-%s-%08x.json' % (MODE, addr),
                       {'expected': expected, 'actual': actual, 'normalized': normalized})
        observed.append(actual)
    return observed


def verify_functions(post=False):
    require(currentProgram.getFunctionManager().getFunctionCount() == 5209, 'FUNCTION_COUNT_5209')
    states = []
    for plate in PLAN['plates']:
        addr, guard = plate['addr'], plate['expected_function']
        fn = getFunctionAt(toAddr(addr))
        require(fn is not None, 'FUNCTION_MISSING %08x' % addr)
        if fn is None:
            continue
        symbol = fn.getSymbol()
        name = RENAMES.get(addr, guard['name']) if post else guard['name']
        require(fn.getEntryPoint() == toAddr(addr) and symbol.getID() == guard['symbol_id'] and
                str(symbol.getSymbolType()) == guard['symbol_type'] and
                str(symbol.getSource()) == guard['source'] and symbol.isPrimary() and
                fn.getName() == name, 'FUNCTION_ID_NAME %08x' % addr)
        require(str(fn.getBody()) == guard['body'] and fn.getBody().getNumAddresses() == guard['body_size'],
                'FUNCTION_BODY %08x' % addr)
        values, eols, body_refs = [], [], []
        iterator = fn.getBody().getAddresses(True)
        while iterator.hasNext():
            pos = iterator.next()
            values.append(chr(memory.getByte(pos) & 255))
            eol = listing.getComment(CodeUnit.EOL_COMMENT, pos)
            if eol is not None:
                eols.append([str(pos), unicode(eol)])
            body_refs.extend(basic_ref(ref) for ref in references.getReferencesFrom(pos))
        require(hashlib.sha256(''.join(values)).hexdigest() == guard['body_sha256'], 'FUNCTION_BYTES %08x' % addr)
        require(eols == guard['eols'], 'FUNCTION_INSTRUCTION_EOLS %08x' % addr)
        incoming = [basic_ref(ref) for ref in references.getReferencesTo(toAddr(addr))]
        sort_refs = lambda refs: sorted(refs, key=lambda item: json.dumps(item, sort_keys=True))
        require(sort_refs(incoming) == sort_refs(guard['incoming']), 'FUNCTION_INCOMING %08x' % addr)
        text = listing.getComment(CodeUnit.PLATE_COMMENT, toAddr(addr))
        wanted = plate['text'] if post else plate['expected_old_text']
        require(text == wanted, 'FUNCTION_PLATE %08x' % addr)
        if not post:
            require(hashlib.sha256(unicode(text).encode('utf8')).hexdigest() == plate['expected_old_sha256'],
                    'OLD_PLATE_HASH %08x' % addr)
        states.append({'addr': addr, 'symbol_id': symbol.getID(), 'name': str(fn.getName()),
                       'body': str(fn.getBody()), 'body_sha256': hashlib.sha256(''.join(values)).hexdigest(),
                       'incoming': sort_refs(incoming), 'body_refs': sort_refs(body_refs), 'eols': eols,
                       'plate': unicode(text)})
    return states


def verify_structure():
    for item in PLAN['coverage']['items']:
        addr = toAddr(item['addr'])
        actual = ''.join('%02x' % (memory.getByte(addr.add(i)) & 255) for i in range(item['size']))
        require(actual == item['hex'], 'SEGMENT_BYTES %08x' % item['addr'])
        if item['kind'] in ('instruction', 'hword_instruction'):
            ins = getInstructionAt(addr)
            require(ins is not None and ins.getLength() == item['size'], 'INSTRUCTION_BOUNDARY %08x' % item['addr'])
    for switch in PLAN['switches']:
        require(memory.getShort(toAddr(switch['mov_pc'])) & 0xffff == 0x4687, 'SWITCH_MOV_PC')
        for index, target in enumerate(switch['values']):
            require(memory.getInt(toAddr(switch['addr'] + index * 4)) & 0xffffffff == target,
                    'SWITCH_WORD')
            mode = currentProgram.getProgramContext().getValue(currentProgram.getRegister('TMode'), toAddr(target), False)
            require(target % 2 == 0 and getInstructionAt(toAddr(target)) is not None and int(mode) == 1,
                    'SWITCH_EVEN_THUMB')
    for table in PLAN['carves']:
        for word in table['words']:
            fn = getFunctionAt(toAddr(word['target']))
            require(word['value'] == (word['target'] | 1) and fn is not None and fn.getName() == word['name'],
                    'CARVE_THUMB_FUNCTION %08x' % word['addr'])
    for tail in PLAN['shared_tails']:
        addr = toAddr(tail['addr'])
        fn = getFunctionContaining(addr)
        require(getFunctionAt(addr) is None and fn is not None and fn.getEntryPoint() == toAddr(tail['owner']),
                'SHARED_TAIL_NO_NEW_FUNCTION %08x' % tail['addr'])


def require_name(name, addr, post=False):
    matches = list(symbols.getGlobalSymbols(name))
    require(all(s.getAddress() == toAddr(addr) for s in matches), 'NAME_COLLISION ' + name)
    if post:
        require(len(matches) == 1, 'POST_GLOBAL_NAME_COUNT ' + name)


def verify_tables_and_names(post=False):
    require((len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATES), len(SLOT_EOLS), len(FUNC_RENAME)) ==
            (93, 19, 30, 15, 142, 2), 'COUNTS')
    require(len(SLOTS) == 142 and set(EOL_MAP) == set(SLOTS), 'SLOT_UNION')
    for addr, name, text in PLATES:
        require(all(ord(c) < 128 for c in text) and len(text) <= 500, 'ASCII_PLATE %08x' % addr)
    for addr, text in SLOT_EOLS:
        require(all(ord(c) < 128 for c in text), 'ASCII_EOL %08x' % addr)
    for addr, value, name, label in EQ_SLOTS:
        eq = equates.getEquate(name)
        require(eq is None or (eq.getValue() & 0xffffffff) == value, 'GLOBAL_EQUATE_VALUE ' + name)
        if not post and SLOTS[addr]['source'] == 'NEW':
            require(eq is None, 'NEW_EQUATE_ALREADY_EXISTS ' + name)
        if post:
            require(eq is not None and len([ref for ref in eq.getReferences()
                    if ref.getAddress() == toAddr(addr) and ref.getOpIndex() == 0]) == 1,
                    'EQUATE_OPERAND_ZERO %08x' % addr)
    for addr, label in [(s['addr'], s['slot_label']) for s in PLAN['slots']]:
        require_name(label, addr, post)
    for addr, slot in TARGETS.items():
        require_name(slot['symbol'], addr, post)
        if slot['target_action'] == 'normalize_existing_symbol_global':
            sym = symbols.getSymbol(slot['target_expected']['symbols'][0]['id'])
            require(sym is not None and sym.getAddress() == toAddr(addr) and sym.getSymbolType() == SymbolType.LABEL,
                    'SWITCH_SAME_SYMBOL_ID %08x' % addr)
            if post:
                require(sym.getParentNamespace() == currentProgram.getGlobalNamespace(), 'SWITCH_GLOBAL_NAMESPACE')
    for addr, old, new in FUNC_RENAME:
        require_name(new, addr, post)


def user_slot_label(addr, name):
    created = symbols.createLabel(toAddr(addr), name, SourceType.USER_DEFINED)
    for old in list(symbols.getSymbols(toAddr(addr))):
        if old.getID() == created.getID():
            continue
        allowed = SLOTS[addr]['expected']['symbols'][0]
        if (old.getID() == allowed['id'] and str(old.getSource()) == 'DEFAULT' and
                old.getSymbolType() == SymbolType.LABEL and old.getName() == allowed['name']):
            old.delete()
        else:
            raise RuntimeError('Unexpected alias at slot %08x' % addr)
    created.setPrimary()


def apply_ref(slot):
    addr, target = toAddr(slot['addr']), toAddr(slot['value'])
    action = slot['target_action']
    if action == 'normalize_existing_symbol_global':
        symbol = symbols.getSymbol(slot['target_expected']['symbols'][0]['id'])
        symbol.setNamespace(currentProgram.getGlobalNamespace())
        symbol.setName(slot['symbol'], SourceType.USER_DEFINED)
    elif action == 'reuse_existing_user_label':
        symbol = symbols.getGlobalSymbol(slot['symbol'], target)
    else:
        symbol = symbols.getGlobalSymbol(slot['symbol'], target)
        if symbol is None:
            symbol = symbols.createLabel(target, slot['symbol'], SourceType.USER_DEFINED)
    symbol.setPrimary()
    # Only these 19 REF slots enter this function. LP RENAME refs never do.
    for old in list(references.getReferencesFrom(addr)):
        if old.getOperandIndex() == 0 and old.getToAddress() == target:
            references.delete(old)
    ref = references.addMemoryReference(addr, target, RefType.DATA, SourceType.USER_DEFINED, 0)
    references.setPrimary(ref, True)


def apply_all():
    # All primary actions are executed in ascending ROM address order.
    events = [(addr, 'PLATE') for addr, name, text in PLATES] + [(addr, 'SLOT') for addr in SLOTS]
    for addr, event in sorted(events):
        if event == 'PLATE':
            if addr in RENAMES:
                getFunctionAt(toAddr(addr)).setName(RENAMES[addr], SourceType.USER_DEFINED)
                COUNTS['FUNC_RENAME'] += 1
            listing.setComment(toAddr(addr), CodeUnit.PLATE_COMMENT, PLATE_MAP[addr])
            COUNTS['PLATE'] += 1
            continue
        slot = SLOTS[addr]
        if slot['kind'] == 'EQ':
            eq = equates.getEquate(slot['symbol'])
            if eq is None:
                eq = equates.createEquate(slot['symbol'], slot['value'])
            eq.addReference(toAddr(addr), 0)
        elif slot['kind'] == 'REF':
            apply_ref(slot)
        # RENAME changes only the pool label and EOL; its DEFAULT ref is untouched.
        user_slot_label(addr, slot['slot_label'])
        listing.setComment(toAddr(addr), CodeUnit.EOL_COMMENT, EOL_MAP[addr])
        COUNTS[slot['kind']] += 1
        COUNTS['EOL'] += 1


def capture(post=False):
    verify_tables_and_names(post)
    verify_structure()
    addresses = verify_addresses(post)
    functions = verify_functions(post)
    return {'addresses': addresses, 'functions': functions,
            'function_count': currentProgram.getFunctionManager().getFunctionCount()}


print('=== RefineF13Seg1 mode=%s ===' % MODE)
before = capture(MODE == 'check')
print('PREFLIGHT slots=142 EQ=93 REF=19 RENAME=30 PLATE=15 EOL=142 FUNC_RENAME=2 FAIL=%d' % len(FAILS))
if FAILS:
    write_json('f13-seg1-%s-failures.json' % MODE, FAILS)
    raise RuntimeError('PREFLIGHT FAIL; no writes performed')
if MODE == 'apply':
    write_json('f13-seg1-apply-before.json', before)
    transaction = currentProgram.startTransaction('Refine F13-Seg-1 exact reviewed actions')
    success = False
    try:
        apply_all()
        after = capture(True)
        for old, new in zip(before['functions'], after['functions']):
            require(old['body_refs'] == new['body_refs'], 'FUNCTION_BODY_REFS %08x' % old['addr'])
        if FAILS:
            write_json('f13-seg1-apply-failures.json', FAILS)
            raise RuntimeError('POSTCHECK FAIL; transaction rolled back')
        success = True
    finally:
        currentProgram.endTransaction(transaction, success)
    write_json('f13-seg1-apply-receipt.json', {'script_sha256': SCRIPT_HASH, 'input_hashes': INPUT_HASHES,
               'counts': COUNTS, 'state': after, 'status': 'APPLIED_TRANSACTION_POSTCHECK_OK'})
elif MODE == 'check':
    receipt = read_json(os.path.join(RUN, 'f13-seg1-apply-receipt.json'))
    require(receipt['script_sha256'] == SCRIPT_HASH, 'PERSISTED_SCRIPT_HASH')
    require(json.dumps(receipt['input_hashes']) == json.dumps(INPUT_HASHES), 'PERSISTED_INPUT_HASHES')
    require(receipt['state'] == before, 'PERSISTED_EXACT_POST_STATE')
    COUNTS = receipt['counts']
    write_json('f13-seg1-persisted-check.json', {'status': 'PERSISTED_CHECK_OK' if not FAILS else 'FAIL',
               'script_sha256': SCRIPT_HASH, 'counts': COUNTS, 'failures': FAILS,
               'exact_saved_state': receipt['state'] == before})
else:
    write_json('f13-seg1-dry-state.json', before)
    rollback_path = os.path.join(RUN, 'f13-seg1-apply-before-attempt1.json')
    if os.path.exists(rollback_path):
        prior = read_json(rollback_path)
        require(before == prior, 'ROLLBACK_COMPLETE_PRESTATE_INCLUDING_BODY_REFS')
        write_json('f13-seg1-rollback-verification.json', {
            'status': 'ROLLBACK_COMPLETE_STATE_MATCH' if before == prior else 'FAIL',
            'prior_sha256': file_hash(rollback_path), 'current_capture': 'f13-seg1-dry-state.json',
            'current_sha256': file_hash(os.path.join(RUN, 'f13-seg1-dry-state.json')),
            'address_count': len(before['addresses']), 'function_count': len(before['functions']),
            'all_fields_equal': before == prior, 'database_file_bytes_claimed_unchanged': False})
    COUNTS.update({'EQ': 93, 'REF': 19, 'RENAME': 30, 'PLATE': 15, 'EOL': 142, 'FUNC_RENAME': 2})
    write_json('f13-seg1-dry-check.json', {'status': 'DRY_PREFLIGHT_OK', 'script_sha256': SCRIPT_HASH,
               'counts': COUNTS, 'addresses': len(BASE), 'failures': FAILS})
if FAILS:
    raise RuntimeError('CHECK FAIL')
print('COUNTS ' + ' '.join('%s=%d' % (key, COUNTS[key]) for key in ('EQ', 'REF', 'RENAME', 'PLATE', 'EOL', 'FUNC_RENAME')))
print('STATUS: OK mode=%s FAIL=0' % MODE)
