# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF06Seg6Slots.py -- F06 Seg-6 (0x08057458..0x08058550)
#   ROM range: set_lp_row_type2_fixed_for_equip_player .. tick_equip_activation_neo_daedalus_gate
#   22 named fn + 1 unlabeled fn (check_equip_slot_active_for_player_and_group @ 0x57678)
#   120 self-name slots (86 EQ + 4 fn-ptr REF + 1 PTR_DAT REF + 28 gP1LP RENAME + 1 disasm DAT)
#
# Sections:
#   A. EQ_SLOTS  -- 86 data-equate slots (nul constant or existing constant)
#   B. REF_SLOTS -- 4 fn-ptr REF (invoke_effect_node_handler_3arg+1 x2,
#                                   check_equip_slot_active_for_player_and_group+1 x2)
#                   + 1 PTR_DAT REF (dispatch_emergency_provisions_ptr_table_ref)
#   C. RENAME_SLOTS -- 28 gP1LP slot_label renames
#   D. FUNC_RENAME -- 1 function rename (Otohime naming error correction)
#   E. PLATE_SET  -- 2 full ASCII plate rewrites (P1: CJK mojibake at 0x57f98; P2: CJK at 0x58550)
#
# New constants added to constants files BEFORE running this script:
#   duel_field.inc: +2 (EQUIP_ACTIVATION_AUX_OFF=0x4b4, EQUIP_ZONE_SPRITE_ATTR_MODE1=0x152a)
#   card_info.inc:  +2 (CLIFF_THE_TRAP_REMOVER_CID=0x161e, OTOHIME_CID=0x1503)
#
# Reused constants (must exist in constants/*.inc):
#   ewram.inc:       gDuelPhaseFlags=0x0201b290, PLAYER_BLOCK_STRIDE=0x868,
#                    gDuelFieldSlots=0x0201c510, gDuelCardCtxBase=0x0201e2a0,
#                    ELIGIB_SPRITE_CTRL_OFF=0x1d68, ELIGIB_ANIM_STATE_OFF=0x1d6c,
#                    P1LP_BLOCK2_OFF_1CE8=0x1ce8, gP1LifePoints=0x0201c4e0
#   duel_field.inc:  EQUIP_ACTIVATION_STEP_OFF=0x4ac, FIELD_STATE_OFF=0x1cf4,
#                    EQUIP_ACT_SCORE_MODE_103=0x103
#   card_info.inc:   DON_ZALOOG_CID=0x1532, lookup_equip_card_score_cid_1388=0x1388,
#                    DARK_SCORPION_GORG_THE_STRONG_CID=0x1685, DARK_SCORPION_MEANAE_CID=0x1686
#   oam_attr.inc:    OAM_ATTR0_HIDDEN=0xffff
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_052051-pre-f06seg6

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
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    const_name must already exist in constants/*.inc.
#    slot_label != const_name; all ^[a-z][a-z0-9_]+$
#    Values verified against ROM (proposal self-check + reviewer C4).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ==== gDuelPhaseFlags = 0x0201b290 (ewram.inc) x17 ====
    (0x08057488, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_display_seq_duel_phase_base'),
    (0x08057504, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_display_seq_phase_base_b'),
    (0x080575cc, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_bar_z14_phase_base'),
    (0x08057708, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_chain_phase_base_a'),
    (0x0805772c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_chain_phase_base_b'),
    (0x080577e0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_chain_phase_base_c'),
    (0x08057864, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_chain_phase_base_d'),
    (0x080578b4, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_slot_score_phase_base'),
    (0x080579f0, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_slot_score_phase_base_b'),
    (0x08057b64, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_slot_score_phase_base_c'),
    (0x08057b8c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_slot_score_phase_base_d'),
    (0x08057c44, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_banisher_phase_base'),
    (0x08057f08, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_sprite_eff_phase_base'),
    (0x08058018, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_score_phase_base'),
    (0x0805834c, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_lp_score_phase_base_b'),
    (0x080583d4, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_bitmap_chain_phase_base'),
    (0x080584e4, 0x0201b290, 'gDuelPhaseFlags', 'tick_equip_zone_bitmap_phase_base'),

    # ==== EQUIP_ACTIVATION_STEP_OFF = 0x000004ac (duel_field.inc) x17 ====
    (0x0805748c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_display_seq_step_off'),
    (0x08057508, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_display_seq_step_off_b'),
    (0x080575d0, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_bar_z14_step_off'),
    (0x0805770c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_chain_step_off_a'),
    (0x08057730, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_chain_step_off_b'),
    (0x080577e4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_chain_step_off_c'),
    (0x08057868, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_chain_step_off_d'),
    (0x080578b8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_slot_score_step_off'),
    (0x080579f4, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_slot_score_step_off_b'),
    (0x08057b68, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_slot_score_step_off_c'),
    (0x08057b90, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_slot_score_step_off_d'),
    (0x08057c48, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_banisher_step_off'),
    (0x08057f0c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_sprite_eff_step_off'),
    (0x0805801c, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_score_step_off'),
    (0x08058350, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_lp_score_step_off_b'),
    (0x080583d8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_bitmap_chain_step_off'),
    (0x080584e8, 0x000004ac, 'EQUIP_ACTIVATION_STEP_OFF', 'tick_equip_zone_bitmap_step_off'),

    # ==== EQUIP_ACTIVATION_AUX_OFF = 0x000004b4 (duel_field.inc, NEW) x8 ====
    (0x080579f8, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off'),
    (0x08057a50, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_b'),
    (0x08057a8c, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_c'),
    (0x08057acc, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_d'),
    (0x08057b04, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_e'),
    (0x08057bd8, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_f'),
    (0x08057bfc, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_g'),
    (0x08057c10, 0x000004b4, 'EQUIP_ACTIVATION_AUX_OFF', 'tick_equip_slot_score_aux_off_h'),

    # ==== PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc) x13 ====
    (0x080576a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_chain_player_stride'),
    (0x08057b5c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_slot_score_player_stride'),
    (0x08057c80, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_banisher_player_stride'),
    (0x08057f04, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_sprite_eff_player_stride'),
    (0x080580b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_lp_score_player_stride_a'),
    (0x080580f4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_lp_score_player_stride_b'),
    (0x08058120, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_lp_score_player_stride_c'),
    (0x0805814c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_lp_score_player_stride_d'),
    (0x08058178, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_lp_score_player_stride_e'),
    (0x080581ec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_lp_score_player_stride_f'),
    (0x08058434, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_bitmap_chain_player_stride'),
    (0x080584c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'enqueue_equip_slot_sprite_fd_player_stride'),
    (0x08058540, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_zone_bitmap_player_stride'),

    # ==== gDuelFieldSlots = 0x0201c510 (ewram.inc) x3 ====
    (0x080576a8, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_chain_slot_base'),
    (0x08057b60, 0x0201c510, 'gDuelFieldSlots', 'tick_equip_slot_score_slot_base'),
    (0x080584c8, 0x0201c510, 'gDuelFieldSlots', 'enqueue_equip_slot_sprite_fd_slot_base'),

    # ==== gDuelCardCtxBase = 0x0201e2a0 (ewram.inc) x4 ====
    (0x080574d4, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_lp_display_seq_ctx_base'),
    (0x08057904, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_slot_score_ctx_base'),
    (0x08057988, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_slot_score_ctx_base_b'),
    (0x080581f0, 0x0201e2a0, 'gDuelCardCtxBase', 'tick_equip_lp_score_ctx_base'),

    # ==== ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (ewram.inc) x4 ====
    (0x0805765c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_lp_bar_z14_sprite_ctrl_off'),
    (0x080577bc, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_chain_sprite_ctrl_off'),
    (0x08057bd0, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_slot_score_sprite_ctrl_off'),
    (0x08057f80, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'tick_equip_sprite_eff_sprite_ctrl_off'),

    # ==== ELIGIB_ANIM_STATE_OFF = 0x00001d6c (ewram.inc) x1 ====
    (0x08057bd4, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'tick_equip_slot_score_anim_state_off'),

    # ==== P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 (ewram.inc) x1 ====
    (0x08058284, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'tick_equip_lp_score_lp_block2_off'),

    # ==== FIELD_STATE_OFF = 0x00001cf4 (duel_field.inc) x1 ====
    (0x08058288, 0x00001cf4, 'FIELD_STATE_OFF', 'tick_equip_lp_score_field_state_off'),

    # ==== OAM_ATTR0_HIDDEN = 0x0000ffff (oam_attr.inc) x3 ====
    (0x08057584, 0x0000ffff, 'OAM_ATTR0_HIDDEN', 'enqueue_lp_row_type2_lp_row_clear'),
    (0x08058408, 0x0000ffff, 'OAM_ATTR0_HIDDEN', 'tick_equip_bitmap_chain_full_mask'),
    (0x08058514, 0x0000ffff, 'OAM_ATTR0_HIDDEN', 'tick_equip_zone_bitmap_full_mask'),

    # ==== DON_ZALOOG_CID = 0x00001532 (card_info.inc) x2 ====
    (0x0805804c, 0x00001532, 'DON_ZALOOG_CID', 'tick_equip_lp_score_don_zaloog_cid_a'),
    (0x080581fc, 0x00001532, 'DON_ZALOOG_CID', 'tick_equip_lp_score_don_zaloog_cid_b'),

    # ==== lookup_equip_card_score_cid_1388 = 0x00001388 (card_info.inc) x3 ====
    (0x08058048, 0x00001388, 'lookup_equip_card_score_cid_1388', 'tick_equip_lp_score_cid_1388_a'),
    (0x080581f8, 0x00001388, 'lookup_equip_card_score_cid_1388', 'tick_equip_lp_score_cid_1388_b'),
    (0x080583a8, 0x00001388, 'lookup_equip_card_score_cid_1388', 'tick_equip_bitmap_cid_1388'),

    # ==== DARK_SCORPION_GORG_THE_STRONG_CID = 0x00001685 (card_info.inc) x2 ====
    (0x08058064, 0x00001685, 'DARK_SCORPION_GORG_THE_STRONG_CID', 'tick_equip_lp_score_gorg_cid_a'),
    (0x08058214, 0x00001685, 'DARK_SCORPION_GORG_THE_STRONG_CID', 'tick_equip_lp_score_gorg_cid_b'),

    # ==== DARK_SCORPION_MEANAE_CID = 0x00001686 (card_info.inc) x2 ====
    (0x08058074, 0x00001686, 'DARK_SCORPION_MEANAE_CID', 'tick_equip_lp_score_meanae_cid_a'),
    (0x08058238, 0x00001686, 'DARK_SCORPION_MEANAE_CID', 'tick_equip_lp_score_meanae_cid_b'),

    # ==== CLIFF_THE_TRAP_REMOVER_CID = 0x0000161e (card_info.inc, NEW) x2 ====
    (0x08058044, 0x0000161e, 'CLIFF_THE_TRAP_REMOVER_CID', 'tick_equip_lp_score_cliff_cid_a'),
    (0x080581f4, 0x0000161e, 'CLIFF_THE_TRAP_REMOVER_CID', 'tick_equip_lp_score_cliff_cid_b'),

    # ==== OTOHIME_CID = 0x00001503 (card_info.inc, NEW) x1 ====
    (0x08057fbc, 0x00001503, 'OTOHIME_CID', 'tick_equip_activation_if_not_otohime_cid'),

    # ==== EQUIP_ZONE_SPRITE_ATTR_MODE1 = 0x0000152a (duel_field.inc, NEW) x1 ====
    (0x08057ff0, 0x0000152a, 'EQUIP_ZONE_SPRITE_ATTR_MODE1', 'enqueue_equip_zone_sprite_mode1_attr'),

    # ==== EQUIP_ACT_SCORE_MODE_103 = 0x00000103 (duel_field.inc) x1 ====
    (0x08058348, 0x00000103, 'EQUIP_ACT_SCORE_MODE_103', 'tick_equip_lp_score_mode_103'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    For fn-ptr: stored value = target|1 (THUMB).  Check accepts |1.
#    For ptr_table: stored value = raw target addr (not THUMB+1).
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # fn-ptr REF x2: invoke_effect_node_handler_3arg+1 = 0x080905e9
    # (NOTE: gas_label maps to invoke_effect_node_handler_3arg @ 0x080905e8)
    (0x080575fc, 0x080905e8, 'invoke_effect_node_handler_3arg',
     'tick_equip_lp_bar_z14_mode_fn'),
    (0x08057f48, 0x080905e8, 'invoke_effect_node_handler_3arg',
     'tick_equip_sprite_eff_mode_fn'),

    # fn-ptr REF x2: check_equip_slot_active_for_player_and_group+1 = 0x08057679
    # (the fn is labeled by DisassembleF06Seg6Blocks.py; listed here for slot labels)
    (0x08057778, 0x08057678, 'check_equip_slot_active_for_player_and_group',
     'tick_equip_chain_slot_active_fn'),
    (0x08057b88, 0x08057678, 'check_equip_slot_active_for_player_and_group',
     'tick_equip_slot_score_slot_active_fn'),

    # ptr_table REF x1: .word 0x08057d38 (ptr-to-table for block1 dispatch fn)
    # This is a raw pointer, not THUMB+1
    (0x08057d34, 0x08057d38, 'ep_state_dispatch_table',
     'dispatch_emergency_provisions_ptr_table_ref'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, old_label, new_label)
#    gP1LifePoints slots already hold correct .word value -- only label rename needed.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x080574a8, 'DWORD_080574a8', 'tick_equip_lp_display_seq_gp1lp'),
    (0x080574d8, 'DWORD_080574d8', 'tick_equip_lp_display_seq_gp1lp_b'),
    (0x08057500, 'DWORD_08057500', 'tick_equip_lp_display_seq_gp1lp_c'),
    (0x08057534, 'DWORD_08057534', 'tick_equip_lp_display_seq_gp1lp_d'),
    (0x08057658, 'DWORD_08057658', 'tick_equip_lp_bar_z14_gp1lp'),
    (0x080577b8, 'PTR_gP1LifePoints_080577b8', 'tick_equip_chain_gp1lp_a'),
    (0x08057860, 'PTR_gP1LifePoints_08057860', 'tick_equip_chain_gp1lp_b'),
    (0x080578d4, 'PTR_gP1LifePoints_080578d4', 'tick_equip_slot_score_gp1lp_a'),
    (0x08057908, 'PTR_gP1LifePoints_08057908', 'tick_equip_slot_score_gp1lp_b'),
    (0x08057924, 'PTR_gP1LifePoints_08057924', 'tick_equip_slot_score_gp1lp_c'),
    (0x08057940, 'PTR_gP1LifePoints_08057940', 'tick_equip_slot_score_gp1lp_d'),
    (0x08057a40, 'PTR_gP1LifePoints_08057a40', 'tick_equip_slot_score_gp1lp_e'),
    (0x08057a90, 'PTR_gP1LifePoints_08057a90', 'tick_equip_slot_score_gp1lp_f'),
    (0x08057bcc, 'PTR_gP1LifePoints_08057bcc', 'tick_equip_slot_score_gp1lp_g'),
    (0x08057c7c, 'DWORD_08057c7c', 'tick_equip_banisher_gp1lp'),
    (0x08057f00, 'DWORD_08057f00', 'tick_equip_sprite_eff_gp1lp'),
    (0x080580b4, 'PTR_gP1LifePoints_080580b4', 'tick_equip_lp_score_gp1lp_a'),
    (0x080580f0, 'PTR_gP1LifePoints_080580f0', 'tick_equip_lp_score_gp1lp_b'),
    (0x0805811c, 'PTR_gP1LifePoints_0805811c', 'tick_equip_lp_score_gp1lp_c'),
    (0x08058148, 'PTR_gP1LifePoints_08058148', 'tick_equip_lp_score_gp1lp_d'),
    (0x08058174, 'PTR_gP1LifePoints_08058174', 'tick_equip_lp_score_gp1lp_e'),
    (0x080581e8, 'PTR_gP1LifePoints_080581e8', 'tick_equip_lp_score_gp1lp_f'),
    (0x080582b0, 'PTR_gP1LifePoints_080582b0', 'tick_equip_lp_score_gp1lp_g'),
    (0x080582dc, 'PTR_gP1LifePoints_080582dc', 'tick_equip_lp_score_gp1lp_h'),
    (0x080582f8, 'PTR_gP1LifePoints_080582f8', 'tick_equip_lp_score_gp1lp_i'),
    (0x08058378, 'PTR_gP1LifePoints_08058378', 'tick_equip_lp_score_gp1lp_j'),
    (0x08058430, 'PTR_gP1LifePoints_08058430', 'tick_equip_bitmap_chain_gp1lp'),
    (0x0805853c, 'DWORD_0805853c', 'tick_equip_zone_bitmap_gp1lp'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: [(addr_int, new_name)]
#    CID 0x1503 = Otohime; naming-phase confused card_record#1503 (D.D.Assailant)
#    with slot_id 0x1503 (Otohime). FUNC_RENAME corrects this.
# ---------------------------------------------------------------------------
FUNC_RENAME = [
    (0x08057f98, 'tick_equip_activation_if_not_otohime'),
]

# ---------------------------------------------------------------------------
# E. PLATE_SET: (func_entry_addr, new_plate_text)
#    P1: tick_equip_activation_if_not_otohime (formerly tick_equip_activation_if_not_dd_assailant)
#        Full ASCII rewrite (old plate had CJK mojibake + wrong card name).
#    P2: tick_equip_activation_neo_daedalus_gate (0x08058550, Seg-7 boundary fn)
#        First instruction is in Seg-6 asm range; plate rewrite for CJK mojibake.
# ---------------------------------------------------------------------------
PLATE_SET = [
    # P1: tick_equip_activation_if_not_otohime @ 0x08057f98
    (0x08057f98,
     'tick_equip_activation_if_not_otohime @ 0x08057f98\n'
     'Equip activation guard: filters out two card cases before invoking\n'
     'tick_equip_activation_state_machine.\n'
     'Reads card_entry[+2].hword bits[13:6] (mask 0xff<<6=0x3fc0 via movs/lsls);\n'
     'if bits equal 0x8a<<5=0x1140 (type_code sentinel), skips and returns 1.\n'
     'Otherwise reads card_entry[+0].u16 card_id; if card_id == 0x1503\n'
     '(OTOHIME_CID, Otohime, pw=39751093), also skips and returns 1.\n'
     'Both exclusions bypass equip activation state machine. Only if neither\n'
     'condition met: transparently calls tick_equip_activation_state_machine\n'
     '(r0=card_entry, r1=secondary_ptr) and returns its value.\n'
     'indeg=0, Sub-type A (step-table dispatch). Exit: pop{r1}; bx r1.\n'
     'NOTE: old name tick_equip_activation_if_not_dd_assailant was incorrect;\n'
     'CID 0x1503 = Otohime not D.D.Assailant (D.D.Assailant slot=0x172c).'),

    # P2: tick_equip_activation_neo_daedalus_gate @ 0x08058550
    (0x08058550,
     'tick_equip_activation_neo_daedalus_gate @ 0x08058550\n'
     'Equip activation Neo Daedalus path conditional gate.\n'
     'Reads card_entry[+2].hword bits[11:2] (mask 0xfc<<4=0xfc0 via movs/lsls);\n'
     'if bits equal 0xf0<<2=0x3c0 (slot_type_code sentinel), skips and returns 1.\n'
     'If not equal to 0x3c0, transparently passes r0/r1 to\n'
     'tick_equip_activation_if_neo_daedalus_with_lp_row and returns its value.\n'
     'Sibling gate stub of function at 0x08057430 (same family, opposite direction).\n'
     'indeg=0 fn-ptr driven. Exit: pop{r1}; bx r1.'),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    """Verify 4-byte little-endian value at slot_int == want (or want|1 for THUMB fn-ptr)."""
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data at 0x%08x" % slot_int
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF06Seg6Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    sm      = currentProgram.getSymbolTable()
    fm      = currentProgram.getFunctionManager()
    nA = nB = nC = nD = nE = 0
    made_targets = set()
    fail_count = 0

    # -------------------------------------------------------------------------
    # A. EQ_SLOTS
    # -------------------------------------------------------------------------
    print("--- A. EQ_SLOTS (%d slots) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s (const=%s want=0x%x)" % (slot_int, err, cname, value))
            fail_count += 1
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    # -------------------------------------------------------------------------
    # B. REF_SLOTS
    # -------------------------------------------------------------------------
    print("--- B. REF_SLOTS (%d slots) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        ok, err = _check(slot_int, tgt_int)
        if not ok:
            # fn-ptr slots store THUMB+1 (odd); also try tgt_int|1
            ok2, _ = _check(slot_int, tgt_int | 1)
            if not ok2:
                print("[B FAIL] 0x%08x: %s (target=%s want=0x%x)" % (
                    slot_int, err, gas_label, tgt_int))
                fail_count += 1
                continue
        if DRY:
            print("[B dry] 0x%08x -> %s (0x%08x) slot_label=%s" % (
                slot_int, gas_label, tgt_int, slot_label))
            nB += 1
            continue
        target_addr = _addr(tgt_int)
        if tgt_int not in made_targets:
            createLabel(target_addr, gas_label, True, SourceType.USER_DEFINED)
            made_targets.add(tgt_int)
        ref = rm.addMemoryReference(
            _addr(slot_int), target_addr, RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s @ 0x%08x)" % (
            slot_int, slot_label, gas_label, tgt_int))
        nB += 1

    # -------------------------------------------------------------------------
    # C. RENAME_SLOTS (pure label rename; value already correct)
    # -------------------------------------------------------------------------
    print("--- C. RENAME_SLOTS (%d slots) ---" % len(RENAME_SLOTS))
    for slot_int, old_label, new_label in RENAME_SLOTS:
        if DRY:
            print("[C dry] 0x%08x: '%s' -> '%s'" % (slot_int, old_label, new_label))
            nC += 1
            continue
        # Create new label (primary); old auto-label will lose primary status
        createLabel(_addr(slot_int), new_label, True, SourceType.USER_DEFINED)
        print("[C ok] 0x%08x: -> %s" % (slot_int, new_label))
        nC += 1

    # -------------------------------------------------------------------------
    # D. FUNC_RENAME
    # -------------------------------------------------------------------------
    print("--- D. FUNC_RENAME (%d items) ---" % len(FUNC_RENAME))
    for fn_addr, new_name in FUNC_RENAME:
        fn = fm.getFunctionAt(_addr(fn_addr))
        if fn is None:
            print("[D FAIL] no Function at 0x%08x" % fn_addr)
            fail_count += 1
            continue
        old_name = fn.getName()
        if DRY:
            print("[D dry] 0x%08x: '%s' -> '%s'" % (fn_addr, old_name, new_name))
            nD += 1
            continue
        fn.setName(new_name, SourceType.USER_DEFINED)
        print("[D ok] 0x%08x: '%s' -> '%s'" % (fn_addr, old_name, new_name))
        nD += 1

    # -------------------------------------------------------------------------
    # E. PLATE_SET (full ASCII rewrite)
    # -------------------------------------------------------------------------
    print("--- E. PLATE_SET (%d items) ---" % len(PLATE_SET))
    for func_int, new_text in PLATE_SET:
        cu = listing.getCodeUnitAt(_addr(func_int))
        if cu is None:
            print("[E FAIL] no CodeUnit @ 0x%08x" % func_int)
            fail_count += 1
            continue
        if DRY:
            print("[E dry] 0x%08x full plate rewrite (%d chars)" % (func_int, len(new_text)))
            nE += 1
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_text)
        print("[E ok] 0x%08x plate set (%d chars)" % (func_int, len(new_text)))
        nE += 1

    print("[done] A=%d B=%d C=%d D=%d E=%d FAIL=%d (DRY=%s)" % (
        nA, nB, nC, nD, nE, fail_count, DRY))
    if fail_count > 0:
        print("[WARN] %d FAIL(s) above -- review before using non-dry run" % fail_count)


main()
