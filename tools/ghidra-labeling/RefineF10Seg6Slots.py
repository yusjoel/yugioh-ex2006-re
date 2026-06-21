# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg6Slots.py -- f10 Seg-6 (0x0807f730..0x08080ba0)
#   18 functions: get_equip_display_criteria_code_by_card_and_slot /
#   fill_equip_criteria_display_code_array / check_equip_slot_criteria_by_ext_field6_any /
#   check_equip_slot_criteria_by_state_code_any / clear_equip_slot_criteria_on_ext_field6_match /
#   find_first_equip_slot_criteria_by_state_code /
#   check_equip_slot_eligible_with_criteria_and_target /
#   check_equip_slot_eligible_by_node_player / find_equip_eligible_slot_entry_for_player /
#   build_equip_slot_criteria_from_card_range / build_equip_set_f_criteria_state /
#   activate_field_spell_neo_daedalus_group_if_placeable /
#   dispatch_equip_criteria_display_by_type_code (switchD_0807fe22) /
#   check_equip_slot_eligible_with_criteria_and_prerequisites /
#   build_equip_eligibility_state_for_category3_card /
#   tick_equip_slot_sprite_display_6state (switchD_080806cc) /
#   build_equip_criteria_for_target_slots / push_to_effect_slot_array
#
# C13: 123 total slots (110 DAT_ + 13 DWORD_)
#   EQ=66 (24 unique values, 15 REUSE + 9 NEW)
#   REF=57 (15 unique addresses, 12 REUSE + 3 NEW abs-addr labels)
#
# NEW constants (already added to constants/*.inc):
#   card_info.inc +2: DRAGONS_MIRROR_CID=0x1921, NON_FUSION_AREA_CID=0x197a
#   duel_field.inc +4: EQUIP_ZONE_ATTR_COMPOSITE_OFF=0x59c,
#                      EQUIP_CRITERIA_TARGETED_FLAG_OFF=0x5a4,
#                      EQUIP_CRITERIA_DISPLAY_ARR_OFF=0x5ac,
#                      EQUIP_CRITERIA_ARR_NEG_OFF=0xfffffa54
#   oam_attr.inc +3: OAM_EQUIP_ZONE_SPRITE_P2_4A=0x804a,
#                    OAM_EQUIP_ZONE_SPRITE_P2_4B=0x804b,
#                    OAM_EQUIP_ZONE_SPRITE_P2_4C=0x804c
#   ewram.inc +3: gDuelPhaseFlags_criteria_count=0x0201b830,
#                 gDuelPhaseFlags_set_f_flag=0x0201b838,
#                 gDuelPhaseFlags_criteria_arr_base=0x0201b850
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

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
#    All values ROM-verified via python struct.unpack.
#    REUSE=15 unique values (confirmed in constants/*.inc), NEW=9 values (0 hits before).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== REUSE: EQUIP_ACTIVE_CTX_OFF=0x484 (duel_field.inc) x2 =====
    (0x0807fb08, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'check_slot_eligible_node_player_ctx_off'),
    (0x080803f4, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'check_slot_prereqs_ctx_off'),

    # ===== REUSE: PLAYER_BLOCK_STRIDE=0x868 (ewram.inc) x13 =====
    (0x0807f9fc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_eligible_criteria_target_stride_a'),
    (0x0807fa64, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_eligible_criteria_target_stride_b'),
    (0x0807fb54, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_eligible_slot_entry_stride_a'),
    (0x0807fb84, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_eligible_slot_entry_stride_b'),
    (0x08080168, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_eligib_cat3_stride_a'),
    (0x080801b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_eligib_cat3_stride_b'),
    (0x08080214, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_eligib_cat3_stride_c'),
    (0x08080340, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_prereqs_stride_a'),
    (0x080803e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_prereqs_stride_b'),
    (0x08080454, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_prereqs_ext_stride'),
    (0x08080674, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_criteria_target_stride_a'),
    (0x08080a84, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'build_equip_criteria_target_stride_b'),    # DWORD_08080a84 -> renamed in RENAME
    (0x08080b44, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'push_effect_slot_stride_b44'),             # DWORD_08080b44 -> renamed in RENAME

    # ===== REUSE: POLYMERIZATION_CID=0x12e5 (card_info.inc) x2 =====
    (0x0808015c, 0x000012e5, 'POLYMERIZATION_CID',
     'build_equip_eligib_cat3_poly_cid'),
    (0x08080274, 0x000012e5, 'POLYMERIZATION_CID',
     'check_slot_prereqs_poly_cid'),

    # ===== REUSE: FUSION_GATE_CID=0x149c (card_info.inc) x2 =====
    (0x08080164, 0x0000149c, 'FUSION_GATE_CID',
     'build_equip_eligib_cat3_fg_cid'),
    (0x0808027c, 0x0000149c, 'FUSION_GATE_CID',
     'check_slot_prereqs_fg_cid'),

    # ===== REUSE: FGD_CID=0x157e (card_info.inc) x2 =====
    (0x0807f744, 0x0000157e, 'FGD_CID',
     'get_equip_display_code_fgd_cid'),
    (0x080807dc, 0x0000157e, 'FGD_CID',
     'tick_equip_6state_caseD3_fgd_cid'),

    # ===== REUSE: EHERO_AVIAN_CID=0x18a6 (card_info.inc) x1 =====
    (0x0807f76c, 0x000018a6, 'EHERO_AVIAN_CID',
     'get_equip_display_code_avian_cid'),

    # ===== REUSE: EHERO_BURSTINATRIX_CID=0x18a7 (card_info.inc) x1 =====
    (0x0807f774, 0x000018a7, 'EHERO_BURSTINATRIX_CID',
     'get_equip_display_code_burst_cid'),

    # ===== REUSE: EHERO_CLAYMAN_CID=0x18a8 (card_info.inc) x1 =====
    (0x0807f77c, 0x000018a8, 'EHERO_CLAYMAN_CID',
     'get_equip_display_code_clay_cid'),

    # ===== REUSE: EHERO_BUBBLEMAN_CID=0x18f9 (card_info.inc) x1 =====
    (0x0807f784, 0x000018f9, 'EHERO_BUBBLEMAN_CID',
     'get_equip_display_code_bubble_cid'),

    # ===== REUSE: UFOROID_FIGHTER_CID=0x18fb (card_info.inc) x3 =====
    (0x080801bc, 0x000018fb, 'UFOROID_FIGHTER_CID',
     'build_equip_eligib_cat3_uforoid_cid_a'),
    (0x0808021c, 0x000018fb, 'UFOROID_FIGHTER_CID',
     'check_slot_prereqs_uforoid_cid_a'),
    (0x080802c8, 0x000018fb, 'UFOROID_FIGHTER_CID',
     'dispatch_criteria_display_uforoid_cid'),

    # ===== REUSE: EHERO_ERIKSHIELER_CID=0x19ef (card_info.inc) x1 =====
    (0x0807f748, 0x000019ef, 'EHERO_ERIKSHIELER_CID',
     'get_equip_display_code_erikshieler_cid'),

    # ===== REUSE: ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc) x1 =====
    (0x08080004, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'dispatch_criteria_caseD7c_sprite_ctrl_off'),

    # ===== REUSE: ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc) x1 =====
    (0x08080008, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'dispatch_criteria_caseD7c_anim_state_off'),

    # ===== REUSE: LP_BANISHER_CTX_OFF=0x1d70 (ewram.inc) x1 =====
    (0x0808000c, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'dispatch_criteria_caseD7c_lp_banisher_off'),

    # ===== REUSE: ACTIVATION_STATE_B_OFF=0x1d78 (duel_field.inc) x1 =====
    (0x0807fddc, 0x00001d78, 'ACTIVATION_STATE_B_OFF',
     'activate_nd_group_activation_state_b_off'),

    # ===== NEW: EQUIP_ZONE_ATTR_COMPOSITE_OFF=0x59c (duel_field.inc) x4 =====
    # DAT_ x3: 0x0807ff58, 0x0808033c, 0x080807a8; DWORD_08080a80 via DWORD_EQ_EXTRA
    (0x0807ff58, 0x0000059c, 'EQUIP_ZONE_ATTR_COMPOSITE_OFF',
     'build_equip_criteria_target_zone_attr_off_a'),
    (0x0808033c, 0x0000059c, 'EQUIP_ZONE_ATTR_COMPOSITE_OFF',
     'check_slot_prereqs_zone_attr_off_a'),
    (0x080807a8, 0x0000059c, 'EQUIP_ZONE_ATTR_COMPOSITE_OFF',
     'tick_equip_6state_caseD3_zone_attr_off'),

    # ===== NEW: EQUIP_CRITERIA_TARGETED_FLAG_OFF=0x5a4 (duel_field.inc) x11 =====
    # DAT_ x10: 0x0807fad4/fc6c/ff5c, 0x08080064/14c/2d0/4c4/670/7ac/8bc; DWORD_08080a8c via DWORD_EQ_EXTRA
    (0x0807fad4, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'check_slot_eligible_node_player_targeted_off'),
    (0x0807fc6c, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'build_equip_criteria_card_range_targeted_off'),
    (0x0807ff5c, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'build_equip_criteria_target_targeted_off_a'),
    (0x08080064, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'dispatch_criteria_caseD7c_targeted_off_a'),
    (0x0808014c, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'build_equip_eligib_cat3_targeted_off_a'),
    (0x080802d0, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'dispatch_criteria_display_targeted_off_a'),
    (0x080804c4, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'check_slot_eligible_node_map_targeted_off'),
    (0x08080670, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'build_equip_criteria_target_targeted_off_b'),
    (0x080807ac, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'tick_equip_6state_caseD3_targeted_off'),
    (0x080808bc, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF',
     'tick_equip_6state_caseD4_targeted_off'),
    # DWORD_08080a8c is also 0x5a4 -- handled via DWORD_EQ_EXTRA

    # ===== NEW: EQUIP_CRITERIA_DISPLAY_ARR_OFF=0x5ac (duel_field.inc) x9 =====
    (0x0807f7fc, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'fill_equip_criteria_arr_off_a'),
    (0x0807f834, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'check_ext_field6_any_arr_off_a'),
    (0x0807f884, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'check_state_code_any_arr_off_a'),
    (0x0807f8d8, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'clear_on_ext6_match_arr_off_a'),
    (0x0807f94c, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'find_first_by_state_code_arr_off_a'),
    (0x0807f970, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'find_first_by_state_code_arr_off_b'),
    (0x08080158, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'build_equip_eligib_cat3_arr_off_a'),
    (0x08080220, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'check_slot_prereqs_arr_off_a'),
    (0x080802cc, 0x000005ac, 'EQUIP_CRITERIA_DISPLAY_ARR_OFF',
     'dispatch_criteria_display_arr_off_a'),

    # ===== NEW: DRAGONS_MIRROR_CID=0x1921 (card_info.inc) x1 =====
    (0x08080280, 0x00001921, 'DRAGONS_MIRROR_CID',
     'check_slot_prereqs_dragons_mirror_cid'),

    # ===== NEW: NON_FUSION_AREA_CID=0x197a (card_info.inc) x2 =====
    # 0x0807fdd0 is DAT_; 0x08080a7c is DWORD_ (handled via RENAME)
    (0x0807fdd0, 0x0000197a, 'NON_FUSION_AREA_CID',
     'activate_nd_group_nfa_cid'),
    # 0x08080a7c handled in RENAME

    # ===== NEW: OAM_EQUIP_ZONE_SPRITE_P2_4A=0x804a (oam_attr.inc) x1 =====
    (0x08080150, 0x0000804a, 'OAM_EQUIP_ZONE_SPRITE_P2_4A',
     'build_equip_eligib_cat3_p2_4a_attr'),

    # ===== NEW: OAM_EQUIP_ZONE_SPRITE_P2_4B=0x804b (oam_attr.inc) x3 =====
    (0x08080160, 0x0000804b, 'OAM_EQUIP_ZONE_SPRITE_P2_4B',
     'build_equip_eligib_cat3_p2_4b_attr_a'),
    (0x08080210, 0x0000804b, 'OAM_EQUIP_ZONE_SPRITE_P2_4B',
     'check_slot_prereqs_p2_4b_attr_a'),
    (0x08080278, 0x0000804b, 'OAM_EQUIP_ZONE_SPRITE_P2_4B',
     'check_slot_prereqs_p2_4b_attr_b'),

    # ===== NEW: OAM_EQUIP_ZONE_SPRITE_P2_4C=0x804c (oam_attr.inc) x1 =====
    (0x08080338, 0x0000804c, 'OAM_EQUIP_ZONE_SPRITE_P2_4C',
     'check_slot_prereqs_p2_4c_attr'),

    # ===== NEW: EQUIP_CRITERIA_ARR_NEG_OFF=0xfffffa54 (duel_field.inc) x1 =====
    (0x0807f950, 0xfffffa54, 'EQUIP_CRITERIA_ARR_NEG_OFF',
     'find_first_by_state_code_arr_neg_off'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # ===== gDuelPhaseFlags = 0x0201b290 (ewram.inc, REUSE) x31 =====
    # DAT_ slots:
    (0x0807f7f8, 0x0201b290, 'gDuelPhaseFlags',
     'fill_equip_criteria_arr_gdf_a'),
    (0x0807f830, 0x0201b290, 'gDuelPhaseFlags',
     'check_ext_field6_any_gdf_a'),
    (0x0807f880, 0x0201b290, 'gDuelPhaseFlags',
     'check_state_code_any_gdf_a'),
    (0x0807f8d4, 0x0201b290, 'gDuelPhaseFlags',
     'clear_on_ext6_match_gdf_a'),
    (0x0807f948, 0x0201b290, 'gDuelPhaseFlags',
     'find_first_by_state_code_gdf_a'),
    (0x0807fa04, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_eligible_criteria_target_gdf_a'),
    (0x0807fa6c, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_eligible_criteria_target_gdf_b'),
    (0x0807fad0, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_eligible_node_player_gdf_a'),
    (0x0807fb04, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_eligible_node_player_gdf_b'),
    (0x0807fc68, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_criteria_card_range_gdf_a'),
    (0x0807fd5c, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_set_f_criteria_gdf_a'),
    (0x0807fe24, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_criteria_display_gdf_a'),
    (0x0807ff54, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_criteria_target_caseD7c_gdf_a'),
    (0x08080060, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_criteria_target_caseD7c_gdf_b'),
    (0x08080154, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_eligib_cat3_gdf_a'),
    (0x080801b8, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_eligib_cat3_gdf_b'),
    (0x080802c4, 0x0201b290, 'gDuelPhaseFlags',
     'dispatch_criteria_display_gdf_b'),
    (0x080803f0, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_prereqs_gdf_a'),
    (0x0808045c, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_prereqs_gdf_b'),
    (0x080804c0, 0x0201b290, 'gDuelPhaseFlags',
     'check_slot_eligible_node_map_gdf_a'),
    (0x0808066c, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_criteria_target_gdf_a'),
    (0x080806d0, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_gdf_a'),
    (0x080807a4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_caseD3_gdf_a'),
    (0x080807d8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_caseD3_gdf_b'),
    (0x08080800, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_caseD3_gdf_c'),
    (0x080808b8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_caseD4_gdf_a'),
    (0x0808091c, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_caseD5_gdf_a'),
    (0x08080704, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_gdf_b'),
    (0x08080720, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_6state_gdf_c'),
    # DWORD_ gDuelPhaseFlags refs (values in RENAME too):
    (0x08080a78, 0x0201b290, 'gDuelPhaseFlags',
     'build_equip_criteria_gdf_base_a78'),
    (0x08080b50, 0x0201b290, 'gDuelPhaseFlags',
     'push_effect_slot_gdf_base_b50'),

    # ===== NEW: gDuelPhaseFlags_criteria_count = 0x0201b830 x2 =====
    (0x08080688, 0x0201b830, 'gDuelPhaseFlags_criteria_count',
     'build_equip_criteria_target_criteria_cnt_a'),
    (0x08080b54, 0x0201b830, 'gDuelPhaseFlags_criteria_count',
     'push_effect_slot_criteria_cnt_b54'),

    # ===== NEW: gDuelPhaseFlags_set_f_flag = 0x0201b838 x3 =====
    (0x0808067c, 0x0201b838, 'gDuelPhaseFlags_set_f_flag',
     'build_equip_criteria_target_set_f_flag_a'),
    (0x08080a94, 0x0201b838, 'gDuelPhaseFlags_set_f_flag',
     'build_equip_criteria_set_f_flag_a94'),
    (0x08080b4c, 0x0201b838, 'gDuelPhaseFlags_set_f_flag',
     'push_effect_slot_set_f_flag_b4c'),

    # ===== NEW: gDuelPhaseFlags_criteria_arr_base = 0x0201b850 x1 =====
    (0x0807fc70, 0x0201b850, 'gDuelPhaseFlags_criteria_arr_base',
     'build_equip_criteria_card_range_arr_base'),

    # ===== gP1LifePoints = 0x0201c4e0 (ewram.inc, REUSE) x1 =====
    # DWORD_08080a90 -- handled via RENAME (value already symbolic gP1LifePoints)
    (0x08080a90, 0x0201c4e0, 'gP1LifePoints',
     'PTR_gP1LifePoints_08080a90'),

    # ===== gP1HandCountBase = 0x0201c4f4 (ewram.inc, REUSE) x1 =====
    (0x0808068c, 0x0201c4f4, 'gP1HandCountBase',
     'build_equip_criteria_target_hand_cnt_base'),

    # ===== gDuelFieldSlots = 0x0201c510 (ewram.inc, REUSE) x4 =====
    (0x0807fa00, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_eligible_criteria_target_dfs_a'),
    (0x0807fb88, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_eligible_slot_entry_dfs_a'),
    (0x080803ec, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_prereqs_dfs_a'),
    (0x08080678, 0x0201c510, 'gDuelFieldSlots',
     'build_equip_criteria_target_dfs_a'),

    # ===== gDuelFieldSlotState = 0x0201c520 (ewram.inc, REUSE) x1 =====
    # DWORD_08080b48
    (0x08080b48, 0x0201c520, 'gDuelFieldSlotState',
     'push_effect_slot_dfs_state_b48'),

    # ===== gP1FieldArrayCBase = 0x0201c600 (ewram.inc, REUSE) x3 =====
    (0x0807fa68, 0x0201c600, 'gP1FieldArrayCBase',
     'check_slot_eligible_criteria_target_p1farrC_a'),
    (0x080801b4, 0x0201c600, 'gP1FieldArrayCBase',
     'build_equip_eligib_cat3_p1farrC_a'),
    (0x0808016c, 0x0201c600, 'gP1FieldArrayCBase',
     'build_equip_eligib_cat3_p1farrC_b'),

    # ===== gP1ChainZoneArray = 0x0201c880 (ewram.inc, REUSE) x2 =====
    (0x08080344, 0x0201c880, 'gP1ChainZoneArray',
     'check_slot_prereqs_chain_zone_arr_a'),
    (0x08080a88, 0x0201c880, 'gP1ChainZoneArray',
     'build_equip_criteria_chain_zone_arr_a88'),

    # ===== gP1HandSlotArray = 0x0201c8f8 (ewram.inc, REUSE) x3 =====
    (0x08080218, 0x0201c8f8, 'gP1HandSlotArray',
     'check_slot_prereqs_hand_slot_arr_a'),
    (0x08080458, 0x0201c8f8, 'gP1HandSlotArray',
     'check_slot_prereqs_ext_hand_slot_arr_a'),
    (0x08080684, 0x0201c8f8, 'gP1HandSlotArray',
     'build_equip_criteria_target_hand_slot_arr_a'),

    # ===== gDuelCardCtxBase = 0x0201e2a0 (ewram.inc, REUSE) x2 =====
    (0x0807fdd4, 0x0201e2a0, 'gDuelCardCtxBase',
     'activate_nd_group_duel_card_ctx_a'),
    (0x0807ff60, 0x0201e2a0, 'gDuelCardCtxBase',
     'dispatch_criteria_caseD7c_duel_card_ctx_a'),

    # ===== check_equip_slot_eligible_by_node_player+1 = 0x0807fad9 (THUMB fn-ptr) x1 =====
    # DAT_0807ff88
    (0x0807ff88, 0x0807fad9, 'check_equip_slot_eligible_by_node_player_thumb',
     'dispatch_criteria_caseD7d_fn_ptr'),

    # ===== switchD_0807fe22__switchdataD_0807fe2c = 0x0807fe2c (table ptr) x1 =====
    # DAT_0807fe28
    (0x0807fe28, 0x0807fe2c, 'switchD_0807fe22__switchdataD_0807fe2c',
     'dispatch_criteria_display_switch_table_ptr'),

    # ===== switchD_080806cc__switchdataD_080806d8 = 0x080806d8 (table ptr) x1 =====
    # DAT_080806d4
    (0x080806d4, 0x080806d8, 'switchD_080806cc__switchdataD_080806d8',
     'tick_equip_6state_switch_table_ptr'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, new_label)
#    DWORD_ literal pool relabeling (values already handled in EQ/REF above).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # build_equip_criteria_for_target_slots literal pool (0x08080a78..0x08080a94):
    (0x08080a78, 'build_equip_criteria_gdf_base_a78'),
    (0x08080a7c, 'build_equip_criteria_nfa_cid_a7c'),
    (0x08080a80, 'build_equip_criteria_zone_attr_off_a80'),
    (0x08080a84, 'build_equip_criteria_stride_a84'),
    (0x08080a88, 'build_equip_criteria_chain_zone_arr_a88'),
    (0x08080a8c, 'build_equip_criteria_targeted_off_a8c'),
    (0x08080a90, 'PTR_gP1LifePoints_08080a90'),      # was DWORD_08080a90
    (0x08080a94, 'build_equip_criteria_set_f_flag_a94'),
    # push_to_effect_slot_array literal pool (0x08080b44..0x08080b54):
    (0x08080b44, 'push_effect_slot_stride_b44'),
    (0x08080b48, 'push_effect_slot_dfs_state_b48'),
    (0x08080b4c, 'push_effect_slot_set_f_flag_b4c'),
    (0x08080b50, 'push_effect_slot_gdf_base_b50'),
    (0x08080b54, 'push_effect_slot_criteria_cnt_b54'),
]

# Also add EQ reference for DWORD_08080a7c (NON_FUSION_AREA_CID)
# and DWORD_08080a80 (EQUIP_ZONE_ATTR_COMPOSITE_OFF)
# and DWORD_08080a8c (EQUIP_CRITERIA_TARGETED_FLAG_OFF)
# These need EQ treatment in addition to RENAME
DWORD_EQ_EXTRA = [
    (0x08080a7c, 0x0000197a, 'NON_FUSION_AREA_CID'),
    (0x08080a80, 0x0000059c, 'EQUIP_ZONE_ATTR_COMPOSITE_OFF'),
    (0x08080a8c, 0x000005a4, 'EQUIP_CRITERIA_TARGETED_FLAG_OFF'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    C8 stale FUN_ substitution. All text pure ASCII. WARN = FAIL.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # get_equip_display_criteria_code_by_card_and_slot (0x0807f730):
    #   L11931: FUN_0807f7bc -> fill_equip_criteria_display_code_array
    (0x0807f730, 'FUN_0807f7bc', 'fill_equip_criteria_display_code_array'),

    # check_equip_slot_criteria_by_ext_field6_any (0x0807f800):
    #   L12062: FUN_0807f974 -> check_equip_slot_eligible_with_criteria_and_target
    (0x0807f800, 'FUN_0807f974', 'check_equip_slot_eligible_with_criteria_and_target'),
    #   L12062: FUN_08080348 -> check_equip_slot_eligible_with_criteria_and_prerequisites
    (0x0807f800, 'FUN_08080348', 'check_equip_slot_eligible_with_criteria_and_prerequisites'),

    # activate_field_spell_neo_daedalus_group_if_placeable (0x0807fd84):
    #   L12847: FUN_0807fde8 -> dispatch_equip_criteria_display_by_type_code
    (0x0807fd84, 'FUN_0807fde8', 'dispatch_equip_criteria_display_by_type_code'),

    # dispatch_equip_criteria_display_by_type_code (0x0807fde8):
    #   L12904: FUN_08080944 -> build_equip_criteria_for_target_slots
    (0x0807fde8, 'FUN_08080944', 'build_equip_criteria_for_target_slots'),

    # push_to_effect_slot_array (0x08080b74):
    #   L14644: FUN_08081ce8 -> tick_equip_effect_slot_display_state
    (0x08080b74, 'FUN_08081ce8', 'tick_equip_effect_slot_display_state'),

    # Cross-file asm/11: render_field_card_copy_count (0x0808e5c4):
    #   L7484: FUN_0807fde8 -> dispatch_equip_criteria_display_by_type_code
    (0x0808e5c4, 'FUN_0807fde8', 'dispatch_equip_criteria_display_by_type_code'),
]

# ---------------------------------------------------------------------------
# E. CJK_PLATE_REWRITES: full ASCII plate replacement for 6 mojibake functions
#    All text pure ASCII. 11 total mojibake lines across 6 functions.
# ---------------------------------------------------------------------------
CJK_PLATE_REWRITES = [
    # 1. get_equip_display_criteria_code_by_card_and_slot (0x0807f730) -- L12017-12018
    (0x0807f730,
     "@ get_equip_display_criteria_code_by_card_and_slot: returns u16 criteria_code for (card_id, slot_idx). FGD_CID(0x157e)->1; EHERO_ERIKSHIELER(0x19ef)->slot0=AVIAN,slot1=BURSTINATRIX,slot2=CLAYMAN,slot3=BUBBLEMAN; other->find_equip_display_entry_by_card_id->slot0=+2,1=+4,2=+6; slot>=3->0.\n"
     "@ Called by fill_equip_criteria_display_code_array to write criteria_code to [gDuelPhaseFlags+EQUIP_CRITERIA_DISPLAY_ARR_OFF+idx*4]. No side effects. Void return (bx r1, Sub-case E via pop{r1})."),

    # 2. check_equip_slot_eligible_with_criteria_and_target (0x0807f974) -- L12274,12277-12279
    (0x0807f974,
     "@ check_equip_slot_eligible_with_criteria_and_target: equip eligibility composite check. Args: effect_node_ptr(r0), player_id(r1), slot_idx(r2). slot_idx<=4 path: check_equip_slot_criteria_by_state_code_any, check_card_id_is_equip_set_e, get_first_placeable_monster_slot, check_slot_placement_blocked_by_field_effect. slot_idx==0xb: find_paired_zone_entry_for_card. Returns 0=ineligible, 1=eligible. Direct callers: 0x0807fad8, 0x0807fb14.\n"
     "@ Constants: SLOT_IDX_MAX=4 (standard zone upper bound)\n"
     "@ ZONE_IDX_PAIR=0xb (paired zone index)\n"
     "@ ATTR_MASK=0xfffc7fff (AND mask clearing bits[14:15])"),

    # 3. find_equip_eligible_slot_entry_for_player (0x0807fb14) -- L12587
    (0x0807fb14,
     "@ find_equip_eligible_slot_entry_for_player: iterates equip eligibility state array and calls check_equip_slot_eligible_with_criteria_and_target per entry; returns first matching slot entry ptr or NULL. indeg=2."),

    # 4. activate_field_spell_neo_daedalus_group_if_placeable (0x0807fd84) -- L12904
    (0x0807fd84,
     "@ activate_field_spell_neo_daedalus_group_if_placeable: field-spell activation entry point. Called by dispatch_equip_criteria_display_by_type_code switchD caseD_80 (case index 0x80-0x63=0x1d). Checks Neo Daedalus group placeable and triggers field-spell effect."),

    # 5. check_equip_slot_eligible_with_criteria_and_prerequisites (0x08080348) -- L13566,13570
    (0x08080348,
     "@ check_equip_slot_eligible_with_criteria_and_prerequisites: equip slot eligibility composite check; near-symmetric sibling of check_equip_slot_eligible_with_criteria_and_target. Args: effect_node_ptr(r0), player_id(r1), slot_idx(r2). slot_idx<=4: check_equip_slot_criteria_by_state_code_any + check_card_id_is_equip_set_e + get_first_placeable_monster_slot + check_slot_placement_blocked_by_field_effect + check_zone_slot_equip_prerequisites. slot_idx==0xe: extended path. Returns 0/1.\n"
     "@ ZONE_IDX_EXT=0xe (extended zone index)"),

    # 6. build_equip_criteria_for_target_slots (0x08080944) -- L14361
    (0x08080944,
     "@ build_equip_criteria_for_target_slots: builds equip target candidate slots. indeg=0, fn-ptr table driven (THUMB+1 ref @ DAT_0807ff88). Extracts effective_player=player_id XOR team_flag; checks [gDuelPhaseFlags+0x4a0*8]==0x80; prereqs: Neo Daedalus placeable + no field duplicate + chain zone slot exists. Writes card_id/zone_attr/display_type to gDuelPhaseFlags+0x598..0x5a8; calls fill_equip_criteria_display_code_array. Loops: per effect_slot validates zone_entry+criteria match, calls push_to_effect_slot_array. Returns 0x64 if count>0 or blocked_flag==1, else 0."),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
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

def _apply_eq(slot_addr, value, eq_name, slot_label):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%08x  label=%s" % (slot_addr, eq_name, value & 0xFFFFFFFF, slot_label))
        return True

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

def _apply_rename(slot_addr, slot_label):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def _apply_plate_fix(func_addr, old_text, new_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[FAIL] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[FAIL] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

def _apply_cjk_plate(func_addr, new_plate_text):
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
    print("=== RefineF10Seg6Slots (DRY=%s) ===" % DRY)
    print("  Seg-6: 0x0807f730..0x08080ba0, 18 fn, 123 slots (EQ66+REF57), 0 ROM_INCBIN, 2 switchD")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d entries) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_skip = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        ok = _apply_eq(slot_addr, value, eq_name, slot_label)
        if ok:
            eq_ok += 1
        else:
            eq_skip += 1
    print("  EQ done: %d  fail: %d" % (eq_ok, eq_skip))

    # A-extra: EQ for DWORD_ slots (in addition to RENAME)
    print("\n--- A-extra: DWORD_EQ_EXTRA (%d) ---" % len(DWORD_EQ_EXTRA))
    for slot_addr, value, eq_name in DWORD_EQ_EXTRA:
        a = _addr(slot_addr)
        eq_tbl = currentProgram.getEquateTable()
        if not _check(slot_addr, value, eq_name):
            print("[SKIP] DWORD_EQ 0x%08x mismatch" % slot_addr)
            continue
        if DRY:
            print("[dry] DWORD_EQ 0x%08x  %s=0x%08x" % (slot_addr, eq_name, value))
            continue
        eq = eq_tbl.getEquate(eq_name)
        if eq is None:
            eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
        eq.addReference(a, 0)
        print("[EQ+] 0x%08x  %s" % (slot_addr, eq_name))

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d entries) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label)
    print("  REF done: %d" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, slot_label in RENAME_SLOTS:
        _apply_rename(slot_addr, slot_label)
    print("  RENAME done: %d" % len(RENAME_SLOTS))

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES: FUN_ substitutions (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1

    # E. CJK plate full rewrites
    print("\n--- E. CJK_PLATE_REWRITES: mojibake->ASCII (%d functions) ---" % len(CJK_PLATE_REWRITES))
    for func_addr, new_plate in CJK_PLATE_REWRITES:
        _apply_cjk_plate(func_addr, new_plate)

    print("\n=== RefineF10Seg6Slots DONE ===")
    print("  EQ=%d(+extra=%d)  REF=%d  RENAME=%d  PLATE_FIX=%d  CJK_PLATE=%d" % (
        len(EQ_SLOTS), len(DWORD_EQ_EXTRA), len(REF_SLOTS), len(RENAME_SLOTS),
        len(PLATE_REWRITES), len(CJK_PLATE_REWRITES)))

main()
