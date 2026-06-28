# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg1Slots.py -- file 12 Seg-1 [0x080941c4, 0x08094f20)
#   asm/12_equip_activation_scan.s slot symbolization
#   31 named functions, 3 ROM_INCBIN blocks (0x9437c/0x1c orphan, 0x943e8/0x12 R4, 0x94c3e/0x22 orphan)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (97 slots: 87 DAT_ + 10 DWORD_)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename (1 slot: jump table ptr)
#   C. RENAME_SLOTS -- PTR_gP1LifePoints_* -> snake_case (13 slots)
#   D. CJK_PLATE_REWRITES -- full ASCII rewrite for 2 CJK-mojibake plate comments
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython UTF-8 mojibake risk).
# Block1 (0x0809437c) and Block3 (0x08094c3e) are 0-ref orphan THUMB code -> §5.1 only, NOT disassembled here.
# Block2 (0x080943e8) R4 disasm is handled in RefineF12Seg1Block2Disasm.py.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- gEquipEffectZoneBase (ewram.inc:550, 0x0201e4f0) -- 14 slots ---
    (0x08094220, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_9220',
     'init_effect_slot_display_context: writes card_slot_ptr/card_type/0 to [+0]/[+4]/[+8]'),
    (0x080942a0, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_92a0',
     'get_clamped_tile_row_count: reads [+4]=tile_row_phase, [+c]=max_count'),
    (0x080942d8, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_92d8',
     'write_effect_ctx_slot_index: str slot_index to [+8]'),
    (0x080942e8, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_92e8',
     'get_monster_slot_entry_ptr: [+8]=count; base+0x10+count*4=entry ptr'),
    (0x08094310, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_9310',
     'get_current_slot_palette_color_index: [+8]=slot_idx, [+0x410+slot*2] halfword'),
    (0x0809431c, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_931c',
     'get_duel_activation_zone_id: [+c]=zone_id field'),
    (0x08094368, 0x0201e500, 'gEquipLpZoneEntryBase',
     'gequiplpzone_9368',
     'get_activation_zone_card_type_field: [slot*4] card attr word'),
    (0x0809436c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_936c',
     'get_activation_zone_card_type_field: [+4]=state check==4 for battle condition'),
    (0x08094370, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_9370',
     'get_activation_zone_card_type_field: [+4]=card_type check==0x49'),
    (0x080943c8, 0x0201e500, 'gEquipLpZoneEntryBase',
     'gequiplpzone_93c8',
     'dispatch_effect_ctx_slot_by_zone_type: slot_table base'),
    (0x08094484, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9484',
     'dispatch_effect_ctx_slot_by_zone_type: [+4]=player_id for zone_type==0xe/0xf paths'),
    (0x08094524, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_9524',
     'dispatch_effect_ctx_slot_by_zone_type: [+4]=card_type==0x49 check'),
    (0x08094528, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9528',
     'dispatch_effect_ctx_slot_by_zone_type: [+4]=player_id for opponent check'),
    (0x08094560, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_9560',
     'set_tile_palette_index_in_buf: [+0x410+2*slot] halfword'),
    (0x08094578, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_9578',
     'read_slot_palette_index: [+0x410+slot*2] high byte'),
    (0x080945b4, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_95b4',
     'reset_slots_above_palette_index: [+c]=slot count'),
    (0x080945dc, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_95dc',
     'find_slot_by_palette_id_in_table: attr table + slot idx field [+8]'),
    (0x0809461c, 0x0201e4f0, 'gEquipEffectZoneBase',
     'gequipeffzone_961c',
     'get_effect_slot_entry_ptr_by_palette_id: attr table base for search'),

    # --- gEquipLpZoneEntryBase (ewram.inc:476, 0x0201e500) -- 3 slots ---
    (0x080942f4, 0x0201e500, 'gEquipLpZoneEntryBase',
     'gequiplpzone_92f4',
     'get_effect_slot_entry_ptr: base+slot*4=entry ptr'),
    (0x08094638, 0x0201e500, 'gEquipLpZoneEntryBase',
     'gequiplpzone_9638',
     'get_effect_slot_entry_ptr_by_palette_id: extra data table base+0x10 return'),

    # --- gDuelCardCtxBase (ewram.inc:218, 0x0201e2a0) -- already listed above; more slots ---
    (0x08094224, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9224',
     'init_effect_slot_display_context: lsls r1,r6,#2; adds r0,#8; gDuelCardCtxBase[player*4+8]'),
    (0x08094748, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9748',
     'enqueue_duel_phase_sprite_by_side: [+4]=player_id to choose sprite attr'),
    (0x08094798, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9798',
     'init_duel_phase_display_flag_with_sprite: [+4]=player_id for P1/P2 sprite selection'),
    (0x080949e0, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_949e0',
     'check_normal_summon_eligibility: [+4]=player_id XOR operand'),
    (0x08094a54, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9a54',
     'process_card_play_ok_sequence: [+4]=current_player_id'),
    (0x08094cf4, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9cf4',
     'tick_equip_activation_main_sequence: [+8] check==3 early exit'),
    (0x08094d9c, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9d9c',
     'tick_equip_activation_main_sequence: [+4*r4+8] fn slot check==2'),
    (0x08094e44, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduecardctx_9e44',
     'advance_duel_turn_by_prng_anim: turn_fn_ptr==NULL path: write sprite variant'),
    (0x08094e48, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_9e48',
     'advance_duel_turn_by_prng_anim: [gP1LifePoints+0x1cfc] sprite variant'),
    (0x08094e70, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_9e70',
     'advance_duel_turn_by_prng_anim: muls r0,r1 for player phase_state read'),

    # --- gP1LifePoints (ewram.inc:79, 0x0201c4e0) -- DWORD_ slots --
    (0x080944e4, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_944e4',
     'dispatch_effect_ctx_slot_by_zone_type: [gP1LifePoints+player*0x868+0xf1*8] zone slot byte'),
    (0x08094c84, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_9c84',
     'tick_equip_activation_dispatch_hub: base for [+0x1ce8]'),
    (0x08094c88, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_9c88',
     'tick_equip_activation_dispatch_hub: [+0x1ce8] player_id raw'),
    (0x08094c8c, 0x0000151e, 'LAST_TURN_CID',
     'last_turn_9c8c',
     'tick_equip_activation_dispatch_hub: icid arg to check_value_in_slot_chain'),
    (0x08094cec, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_9cec',
     'tick_equip_activation_main_sequence: base'),
    (0x08094cf0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_9cf0',
     'tick_equip_activation_main_sequence: [+0x1ce8] player_id for dispatch'),
    # DWORD_08094cc0 and DWORD_08094d80 hold gP1LifePoints (EQ not REF)
    (0x08094cc0, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_9cc0',
     'tick_equip_activation_dispatch_hub: base [gP1LifePoints+0x1d18]'),
    (0x08094d80, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_9d80',
     'tick_equip_activation_main_sequence: base [gP1LifePoints+0x1d10]'),

    # --- PLAYER_BLOCK_STRIDE (ewram.inc:251, 0x00000868) -- 6 slots ---
    (0x080944e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_94e8',
     'dispatch_effect_ctx_slot_by_zone_type: muls r1,r3 for player offset'),
    (0x080946a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_96a4',
     'get_player_lp_by_field_type: type=0xc path muls'),
    (0x080946bc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_96bc',
     'get_player_lp_by_field_type: type=0xd path'),
    (0x080946d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_96d4',
     'get_player_lp_by_field_type: type=0xe path'),
    (0x080946f0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_96f0',
     'get_player_lp_by_field_type: type=0xf path'),
    (0x08094894, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_9894',
     'query_summon_eligibility_code: muls r1,r2 for opponent field addr'),
    (0x080949ec, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_949ec',
     'check_normal_summon_eligibility: muls for p1 code write offset'),
    (0x08094b74, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_9b74',
     'process_card_play_ok_sequence: muls r0,r1 for player offset in sub-phase select'),

    # --- TRIBE_INFECTING_VIRUS_CID (card_info.inc:912, 0x0000161c) -- 1 slot ---
    (0x0809426c, 0x0000161c, 'TRIBE_INFECTING_VIRUS_CID',
     'tribe_infect_926c',
     'init_effect_slot_display_context: type>0x49 -> [gP1LifePoints+LP_ACTIVATION_PENDING_OFF]=0x161c; may coincide with TRIBE_INFECTING_VIRUS_CID as sentinel; conf: med'),

    # --- ZONE_SLOT_ATTR_BIT12_CLEAR_MASK (ewram.inc new, 0xffffefff) -- 1 slot ---
    (0x0809453c, 0xffffefff, 'ZONE_SLOT_ATTR_BIT12_CLEAR_MASK',
     'zone_clear_mask_953c',
     'dispatch_effect_ctx_slot_by_zone_type: ands r6,r0 clears bit12 of zone attr word'),

    # --- LCG constants (prng.inc new) -- 2 slots ---
    (0x0809465c, 0x000343fd, 'LCG_MUL_343FD',
     'lcg_mul_965c',
     'advance_prng_state: seed*=LCG_MUL_343FD (standard C rand() multiplier)'),
    (0x08094660, 0x00269ec3, 'LCG_INC_269EC3',
     'lcg_inc_9660',
     'advance_prng_state: seed+=LCG_INC_269EC3 (standard C rand() increment)'),

    # --- P1LP_BACKUP_DST_OFF (ewram.inc:245, 0x00001cf0) -- 1 slot ---
    (0x0809473c, 0x00001cf0, 'P1LP_BACKUP_DST_OFF',
     'p1lp_backup_dst_973c',
     'enqueue_duel_phase_sprite_by_side: [gP1LifePoints+0x1cf0] guard check==UNINIT_GUARD_FFFF'),

    # --- UNINIT_GUARD_FFFF (duel_field.inc new, 0x0000ffff) -- 1 slot ---
    (0x08094740, 0x0000ffff, 'UNINIT_GUARD_FFFF',
     'uninit_guard_9740',
     '[gP1LifePoints+P1LP_BACKUP_DST_OFF]==0xffff means LP timer uninitialized; prevents double-init'),

    # --- P1LP_TIMER_OFF (ewram.inc:244, 0x00001cec) -- 2 slots ---
    (0x08094744, 0x00001cec, 'P1LP_TIMER_OFF',
     'p1lp_timer_9744',
     'enqueue_duel_phase_sprite_by_side: [gP1LifePoints+0x1cec] written to [+0x1cf0]'),
    (0x0809494c, 0x00001cec, 'P1LP_TIMER_OFF',
     'p1lp_timer_494c',
     'query_summon_eligibility_code: [gP1LifePoints+0x1cec] and [+0x1cf0] compared for summon gate'),

    # --- SPRITE_ATTR_DUEL_PHASE_P2 (duel_field.inc new, 0x0000800b) -- 1 slot ---
    (0x0809474c, 0x0000800b, 'SPRITE_ATTR_DUEL_PHASE_P2',
     'sprite_attr_p2_974c',
     'enqueue_duel_phase_sprite_by_side: P2 side duel phase sprite attr 0x800b'),

    # --- LP_DISCARD_ZONE_OFF (ewram.inc:390, 0x000010dc) -- 5 slots ---
    (0x08094790, 0x000010dc, 'LP_DISCARD_ZONE_OFF',
     'lp_discard_zone_9790',
     'init_duel_phase_display_flag_with_sprite: [gP1LifePoints+0x10dc] idempotent guard'),
    (0x080948f4, 0x000010dc, 'LP_DISCARD_ZONE_OFF',
     'lp_discard_zone_948f4',
     'query_summon_eligibility_code: [gP1LifePoints+0x10dc]:=1 after check_node_in_slot_chain success'),
    (0x080949e8, 0x000010dc, 'LP_DISCARD_ZONE_OFF',
     'lp_discard_zone_949e8',
     'check_normal_summon_eligibility: [gP1LifePoints+0x10dc] check when both codes==0'),
    (0x08094a1c, 0x000010dc, 'LP_DISCARD_ZONE_OFF',
     'lp_discard_zone_9a1c',
     'check_normal_summon_eligibility: [gP1LifePoints+0x10dc]:=1 at end of summon state write'),
    (0x08094d7c, 0x000010dc, 'LP_DISCARD_ZONE_OFF',
     'lp_discard_zone_9d7c',
     'tick_equip_activation_main_sequence: [gP1LifePoints+0x10dc] additional status check'),

    # --- DISP_SET_VARIANT_OFF (duel_field.inc:253, 0x00001cfc) -- 6 slots ---
    (0x08094794, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_9794',
     'init_duel_phase_display_flag_with_sprite: [gP1LifePoints+0x1cfc] sprite variant 1 or 2'),
    (0x080949f0, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_949f0',
     'check_normal_summon_eligibility: [gP1LifePoints+0x1cfc]:=1 when p0 nonzero'),
    (0x08094a00, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_9a00',
     'check_normal_summon_eligibility: [gP1LifePoints+0x1cfc]:=2 for p1-only nonzero'),
    (0x08094a18, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_9a18',
     'check_normal_summon_eligibility: [gP1LifePoints+0x1cfc]:=3 for p0-only nonzero alt path'),
    (0x08094b88, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_9b88',
     'process_card_play_ok_sequence: ldrh r1,[r0] reads current display variant'),
    (0x08094bdc, 0x00001cfc, 'DISP_SET_VARIANT_OFF',
     'disp_variant_9bdc',
     'process_card_play_ok_sequence: ldrh r1,[r0] reads variant for pack_sprite_row_attr_words call'),

    # --- SPRITE_ATTR_DUEL_PHASE_P2_B (duel_field.inc new, 0x00008023) -- 1 slot ---
    (0x0809479c, 0x00008023, 'SPRITE_ATTR_DUEL_PHASE_P2_B',
     'sprite_attr_p2b_979c',
     'init_duel_phase_display_flag_with_sprite: P2 attr 0x8023; companion P1=0x23'),

    # --- Exodia piece CIDs (card_info.inc) -- 5 slots ---
    (0x080947e4, 0x00000fb7, 'RIGHT_LEG_FORBIDDEN_ONE_CID',
     'right_leg_exo_97e4',
     'check_all_fusion_pair_slots_available: Exodia piece 1 of 5'),
    (0x080947e8, 0x00000fb8, 'LEFT_LEG_FORBIDDEN_ONE_CID',
     'left_leg_exo_97e8',
     'check_all_fusion_pair_slots_available: Exodia piece 2'),
    (0x080947ec, 0x00000fb9, 'RIGHT_ARM_FORBIDDEN_ONE_CID',
     'right_arm_exo_97ec',
     'check_all_fusion_pair_slots_available: Exodia piece 3'),
    (0x080947f0, 0x00000fba, 'LEFT_ARM_FORBIDDEN_ONE_CID',
     'left_arm_exo_97f0',
     'check_all_fusion_pair_slots_available: Exodia piece 4'),
    (0x080947f4, 0x00000fbb, 'EXODIA_THE_FORBIDDEN_ONE_CID',
     'exodia_cid_97f4',
     'check_all_fusion_pair_slots_available: Exodia piece 5'),

    # --- DESTINY_BOARD_CID + Spirit Message CIDs (card_info.inc) -- 5 slots ---
    (0x08094848, 0x00001468, 'DESTINY_BOARD_CID',
     'destiny_board_9848',
     'check_all_equip_target_slots_available: CID arg to count_available_effect_zones'),
    (0x0809484c, 0x00001497, 'SPIRIT_MESSAGE_I_CID',
     'spirit_msg_i_984c',
     'check_all_equip_target_slots_available: equip slot ID arg to find_equip_slot_by_card_id'),
    (0x08094850, 0x00001498, 'SPIRIT_MESSAGE_N_CID',
     'spirit_msg_n_9850',
     'check_all_equip_target_slots_available: equip slot ID 2'),
    (0x08094854, 0x00001499, 'SPIRIT_MESSAGE_A_CID',
     'spirit_msg_a_9854',
     'check_all_equip_target_slots_available: equip slot ID 3'),
    (0x08094858, 0x0000149a, 'SPIRIT_MESSAGE_L_CID',
     'spirit_msg_l_9858',
     'check_all_equip_target_slots_available: equip slot ID 4'),

    # --- P1LP_BLOCK2_OFF (ewram.inc:243, 0x00001d08) -- 7 slots ---
    (0x080948ec, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_948ec',
     'query_summon_eligibility_code: [gP1LifePoints+0x1ce8] player_id raw field'),
    (0x080948f0, 0x0000151e, 'LAST_TURN_CID',
     'last_turn_948f0',
     'query_summon_eligibility_code: chain slot value 0x151e for check_node_in_slot_chain'),
    (0x0809490c, 0x0000169c, 'FINAL_COUNTDOWN_CID',
     'final_cntdwn_490c',
     'query_summon_eligibility_code: second chain slot 0x169c for check_node_in_slot_chain'),
    (0x080949dc, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_949dc',
     'check_normal_summon_eligibility: [gP1LifePoints+0x1d08] guard field read'),
    (0x080949e4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_949e4',
     'check_normal_summon_eligibility: [gP1LifePoints+0x1ce8] vs [gDuelSettings+4]^1'),
    (0x08094a80, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_9a80',
     'process_card_play_ok_sequence: [gP1LifePoints+0x1d08] summon-phase guard'),
    (0x08094a84, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_blk2_9a84',
     'process_card_play_ok_sequence: [gP1LifePoints+0x1ce8] player match guard'),
    (0x08094bd8, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_9bd8',
     'process_card_play_ok_sequence: [gP1LifePoints+0x1d08] equip target count check'),
    (0x08094c00, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_9c00',
     'process_card_play_ok_sequence: LP_compare path [gP1LifePoints+0x1d08] check'),
    (0x08094d74, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_9d74',
     'tick_equip_activation_main_sequence: [gP1LifePoints+0x1d08] equip target count'),
    (0x08094e18, 0x00001d08, 'P1LP_BLOCK2_OFF',
     'p1lp_blk2_9e18',
     'advance_duel_turn_by_prng_anim: [gP1LifePoints+0x1d08] prng anim flag'),

    # --- SET_DISPLAY_STATE_SLOT_OFF (duel_field.inc:254, 0x00000894) -- 1 slot ---
    (0x08094b70, 0x00000894, 'SET_DISPLAY_STATE_SLOT_OFF',
     'set_disp_state_9b70',
     'process_card_play_ok_sequence: [gP1LifePoints+0x894] P2-analog display state slot'),

    # --- SPRITE_ATTR_SPELL_8006 (duel_field.inc new, 0x00008006) -- 1 slot ---
    (0x08094b78, 0x00008006, 'SPRITE_ATTR_SPELL_8006',
     'sprite_attr_spell_9b78',
     'process_card_play_ok_sequence: spell phase enqueue_sprite_attr_record arg'),

    # --- SPRITE_ATTR_TRAP_8007 (duel_field.inc new, 0x00008007) -- 1 slot ---
    (0x08094b7c, 0x00008007, 'SPRITE_ATTR_TRAP_8007',
     'sprite_attr_trap_9b7c',
     'process_card_play_ok_sequence: trap phase sprite attr'),

    # --- SPRITE_ATTR_MONSTER_8008 (duel_field.inc new, 0x00008008) -- 1 slot ---
    (0x08094b80, 0x00008008, 'SPRITE_ATTR_MONSTER_8008',
     'sprite_attr_mon_9b80',
     'process_card_play_ok_sequence: monster phase sprite attr; domain-distinct from CARD_DESC_RENDER_PARAM(jp-glyph)'),

    # --- SPRITE_ATTR_ALT_8005 (duel_field.inc new, 0x00008005) -- 1 slot ---
    (0x08094b84, 0x00008005, 'SPRITE_ATTR_ALT_8005',
     'sprite_attr_alt_9b84',
     'process_card_play_ok_sequence: P2==0 fallback sprite attr'),

    # --- CARD_PLAY_PHASE_CTR_OFF (ewram.inc new, 0x00001d1c) -- 3 slots ---
    (0x08094a5c, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF',
     'card_play_phase_9a5c',
     'process_card_play_ok_sequence: [gP1LifePoints+0x1d1c] phase counter'),
    (0x08094b8c, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF',
     'card_play_phase_9b8c',
     'process_card_play_ok_sequence: [gP1LifePoints+0x1d1c] incremented at end'),
    (0x08094cc8, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF',
     'card_play_phase_9cc8',
     'tick_equip_activation_dispatch_hub: [gP1LifePoints+0x1d1c]:=0 after phase step'),
    (0x08094e1c, 0x00001d1c, 'CARD_PLAY_PHASE_CTR_OFF',
     'card_play_phase_9e1c',
     'advance_duel_turn_by_prng_anim: [gP1LifePoints+0x1d1c]:=0 after turn fn step'),

    # --- gDuelDisplaySeqState (ewram.inc:377, 0x0201bcc0) -- 1 slot ---
    (0x08094bd0, 0x0201bcc0, 'gDuelDisplaySeqState',
     'gdueldispseq_9bd0',
     'process_card_play_ok_sequence draw_phase: [gDuelDisplaySeqState+0x808] check'),

    # --- DISPLAY_SEQ_SLOT_IDX_OFF (duel_field.inc:216, 0x00000808) -- 1 slot ---
    (0x08094bd4, 0x00000808, 'DISPLAY_SEQ_SLOT_IDX_OFF',
     'disp_seq_slot_9bd4',
     'process_card_play_ok_sequence: [gDuelDisplaySeqState+0x808] sprite write slot index'),

    # --- gSpriteAttrBuf (ewram.inc:378, 0x0201b870) -- 2 slots ---
    (0x08094c04, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9c04',
     'process_card_play_ok_sequence: [gSpriteAttrBuf+0xc0*4] byte check bit7'),
    (0x08094d78, 0x0201b870, 'gSpriteAttrBuf',
     'gsprattrb_9d78',
     'tick_equip_activation_main_sequence: [gSpriteAttrBuf+0xc0*4] bit7 check'),

    # --- EQUIP_PHASE_FN_TABLE_ROM (ewram.inc new, 0x09e5aac0) -- 1 slot ---
    (0x08094cbc, 0x09e5aac0, 'EQUIP_PHASE_FN_TABLE_ROM',
     'equip_phase_tbl_9cbc',
     'tick_equip_activation_dispatch_hub: ROM fn-ptr table; THUMB+1 entries indexed by EQUIP_MAIN_PHASE_OFF'),

    # --- EQUIP_MAIN_PHASE_OFF (duel_field.inc:255, 0x00001d18) -- 1 slot ---
    (0x08094cc4, 0x00001d18, 'EQUIP_MAIN_PHASE_OFF',
     'equip_main_phase_9cc4',
     'tick_equip_activation_dispatch_hub: [gP1LifePoints+0x1d18] phase index advanced after fn-ptr call'),

    # --- DISPLAY_SEQ_ACTIVE_PLAYER_OFF (duel_field.inc:218, 0x00001d10) -- 1 slot ---
    (0x08094d84, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF',
     'disp_seq_aplayer_9d84',
     'tick_equip_activation_main_sequence: [gP1LifePoints+0x1d10] phase step field written'),

    # --- DUEL_TURN_FN_TABLE_ROM (ewram.inc new, 0x09e5aadc) -- 1 slot ---
    (0x08094e0c, 0x09e5aadc, 'DUEL_TURN_FN_TABLE_ROM',
     'duel_turn_tbl_9e0c',
     'advance_duel_turn_by_prng_anim: ROM fn-ptr table; THUMB+1 entries indexed by DUEL_TURN_STATE_OFF'),

    # --- DUEL_TURN_STATE_OFF (ewram.inc new, 0x00001d14) -- 1 slot ---
    (0x08094e14, 0x00001d14, 'DUEL_TURN_STATE_OFF',
     'duel_turn_state_9e14',
     'advance_duel_turn_by_prng_anim: [gP1LifePoints+0x1d14] duel turn phase index'),

    # --- gPuzzleCardAnimBuf (ewram.inc:577, 0x0201b1b0) -- 4 slots ---
    (0x08094e84, 0x0201b1b0, 'gPuzzleCardAnimBuf',
     'gcarddisp_buf_9e84',
     'get_card_data_bit_by_index: table_a base for index<=0x34 direct read'),
    (0x08094eb0, 0x0201b1b0, 'gPuzzleCardAnimBuf',
     'gcarddisp_buf_9eb0',
     'get_card_data_bit_by_index: extended path base'),
    (0x08094ec4, 0x0201b1b0, 'gPuzzleCardAnimBuf',
     'gcarddisp_buf_9ec4',
     'write_card_display_index_entry: direct path'),
    (0x08094ef4, 0x0201b1b0, 'gPuzzleCardAnimBuf',
     'gcarddisp_buf_9ef4',
     'write_card_display_index_entry: extended path OR'),
    (0x08094f1c, 0x0201b1b0, 'gPuzzleCardAnimBuf',
     'gcarddisp_buf_9f1c',
     'write_card_display_index_entry: extended path BIC'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # --- jump table ptr for dispatch_effect_ctx_slot_by_zone_type ---
    (0x080943cc, 0x080943d0, 'zone_type_jump_table',
     'zone_type_jumptbl_93cc',
     'ptr to 5-entry raw-address jump table at 0x080943d0; dispatch via mov pc,r0'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    All 13 PTR_gP1LifePoints_ slots -> snake_case rename.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08094268, 'gp1lp_ptr_94268', None),
    (0x08094658, 'gp1lp_ptr_94658', None),
    (0x080946a0, 'gp1lp_ptr_946a0', None),
    (0x080946b8, 'gp1lp_ptr_946b8', None),
    (0x080946d0, 'gp1lp_ptr_946d0', None),
    (0x080946ec, 'gp1lp_ptr_946ec', None),
    (0x08094738, 'gp1lp_ptr_94738', None),
    (0x0809478c, 'gp1lp_ptr_9478c', None),
    (0x08094890, 'gp1lp_ptr_94890', None),
    (0x080949d8, 'gp1lp_ptr_949d8', None),
    (0x08094a58, 'gp1lp_ptr_94a58', None),
    (0x08094b6c, 'gp1lp_ptr_94b6c', None),
    (0x08094e10, 'gp1lp_ptr_94e10', None),
]

# ---------------------------------------------------------------------------
# D. CJK_PLATE_REWRITES: (func_addr, new_plate_ascii_text)
#    Full plate rewrite for CJK/mojibake plates.
#    All text MUST be pure ASCII.
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # get_effect_slot_entry_ptr (0x080942ec) - L172 CJK mojibake
    (0x080942ec,
     '@ get_effect_slot_entry_ptr: Pure 3-instruction leaf.\n'
     '@ r0=slot_idx -> returns gEquipLpZoneEntryBase + slot_idx*4 (entry ptr).\n'
     '@ No side effects. indeg>=6; callers include FUN_080bb414 (0x080bb576/0x080bb57e)\n'
     '@ and multiple duel_field callers.\n'
     '@ Constants: gEquipLpZoneEntryBase=0x0201e500, entry_size=4.'),

    # get_activation_zone_card_type_field (0x08094320) - L212 CJK mojibake
    (0x08094320,
     '@ get_activation_zone_card_type_field: r0=slot_idx.\n'
     '@ Reads gEquipLpZoneEntryBase[slot_idx*4] attr word; extracts bit13 as player_flag.\n'
     '@ If gDuelCardCtxBase[+4]==4 (battle state): XOR player_flag with 1;\n'
     '@   if XOR matches gDuelCardCtxBase[+4]: calls get_zone_card_attribute_by_type(player_flag, 0xf, slot_idx).\n'
     '@ If state!=4: if gEquipEffectZoneBase[+4]==0x49 returns 0;\n'
     '@   else extracts bits[12:0] of gEquipLpZoneEntryBase[slot_idx*4+0x10] and returns.\n'
     '@ Constants: gEquipLpZoneEntryBase=0x0201e500, gDuelCardCtxBase=0x0201e2a0,\n'
     '@ gEquipEffectZoneBase=0x0201e4f0, SPECIAL_ID=0x49.'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    """Verify ROM dword at slot_addr == expected_val. Return True if OK."""
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

    # create/get equate
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # create slot label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    # EOL comment
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_cjk_plate(func_addr, new_plate_text):
    """Full plate rewrite (for CJK->ASCII conversion)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] cjk_plate 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] CJK_PLATE 0x%08x: rewrite to ASCII" % func_addr)
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate_text)
    print("[PLT] 0x%08x: CJK plate replaced with ASCII" % func_addr)

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF12Seg1Slots (DRY=%s) ===" % DRY)
    print("  Seg-1: 0x080941c4..0x08094f20, file 12 equip_activation_scan")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_skip = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
    print("  REF done: %d" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. CJK plate full rewrites
    print("\n--- D. CJK_PLATE_REWRITES (%d) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineF12Seg1Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  CJK_PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(CJK_PLATE_REWRITES)))

main()
