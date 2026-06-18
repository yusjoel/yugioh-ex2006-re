# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg8Slots.py -- p5 file09 Seg-8 (0x0807629c..0x0807738c)
#   enqueue_hand_spell_sprite_with_lp_counter + tick_equip_zone_bitmap_display_seq
#   + fn_eligible_mustering_dark_scorpions cluster + fn_eligible_spell_vanishing cluster
#   + enqueue_equip_zone_sprite_with_neo_daedalus_and_chain + dispatch_equip_effect_node_by_opcode
#   21 functions (19 distinct entries)
#
# Sections:
#   A. EQ_SLOTS   -- 68 slots: 63 REUSE + 5 NEW
#   B. REF_SLOTS  -- 0 slots (all globals via EQ pc-relative literal pool)
#   C. RENAME_SLOTS -- 8 slots
#   D. PLATE_REWRITES -- 0 updates
#
# Non-blocking corrections applied per reviewer:
#   - DWORD_080769d4 (0xcc8) EOL: "bits[12:0]" NOT "bits[23:22]"
#     (ldrh + lsls#19 + lsrs#19 = 13-bit field extraction)
#
# New constants added to constants/ before this script:
#   card_info.inc +5:
#     DARK_SCORPION_BURGLARS_CID = 0x00001531
#     DD_SCOUT_PLANE_CID         = 0x000016be
#     ENERGY_DRAIN_CID           = 0x000016e3
#     GIFT_OF_THE_MARTYR_CID     = 0x000018ca
#     DEAL_OF_PHANTOM_CID        = 0x00001492  (doc-only, no literal pool slot)
#   ewram.inc +1:
#     HAND_SPELL_SLOT_CC8_OFF    = 0x00000cc8
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0; disasm handled by DisassembleF09Seg8Blocks.py
# NOTE: PLATE=0 (all Seg-8 plates are ASCII-clean, no stale FUN_ found)

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
#    68 slots: 63 REUSE + 5 NEW
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # =========================================================================
    # Seg-8a slots (0x7629c..0x76908): 27 slots
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (multiple) ---
    (0x08076334, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6334',
     'PLAYER_BLOCK_STRIDE: byte stride per player data block'),

    # --- ewram.inc: gP1HandSlotArray = 0x0201c8f8 ---
    (0x08076338, 0x0201c8f8, 'gP1HandSlotArray',
     'gP1HandSlotArray_pool_6338',
     'gP1HandSlotArray: P1 hand slot array base (EWRAM)'),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08076358, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_6358',
     'gDuelPhaseFlags: duel phase flags global'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08076390, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_6390',
     'gP1LifePoints: P1 LP tracking block base (EWRAM)'),

    # --- ewram.inc: LP_CARD_TRACK_BASE_OFF = 0x00001da8 ---
    (0x08076394, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_off_pool_6394',
     'LP_CARD_TRACK_BASE_OFF: LP card tracking base offset'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08076448, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_6448', None),

    # --- ewram.inc: ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 ---
    (0x0807644c, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_pool_644c',
     'ELIGIB_SPRITE_CTRL_OFF: eligibility sprite display control offset'),

    # --- ewram.inc: ELIGIB_ANIM_STATE_OFF = 0x00001d6c ---
    (0x08076450, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_off_pool_6450',
     'ELIGIB_ANIM_STATE_OFF: eligibility animation state index offset'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08076488, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_6488', None),

    # --- ewram.inc: P1LP_TIMER_OFF = 0x00001cec ---
    (0x0807648c, 0x00001cec, 'P1LP_TIMER_OFF',
     'p1lp_timer_off_pool_648c',
     'P1LP_TIMER_OFF: P1 LP timer field offset'),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x080764ec, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_64ec', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080764f0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_64f0', None),

    # --- ewram.inc: gP1SlotSetCodeArray = 0x0201c740 ---
    (0x080764f4, 0x0201c740, 'gP1SlotSetCodeArray',
     'gP1SlotSetCodeArray_pool_64f4',
     'gP1SlotSetCodeArray: P1 slot set-code array base (EWRAM)'),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x0807655c, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_655c', None),

    # --- duel_field.inc: EQUIP_ACTIVE_CTX_OFF = 0x00000484 ---
    (0x08076560, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'equip_active_ctx_off_pool_6560',
     'EQUIP_ACTIVE_CTX_OFF: equip activation context byte offset'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076564, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6564', None),

    # --- ewram.inc: gP1FieldArrayCBase = 0x0201c600 ---
    (0x08076568, 0x0201c600, 'gP1FieldArrayCBase',
     'gP1FieldArrayCBase_pool_6568',
     'gP1FieldArrayCBase: P1 field array C base (EWRAM)'),

    # --- card_info.inc: DARK_SCORPION_CHICK_CID = 0x00001656 ---
    (0x0807656c, 0x00001656, 'DARK_SCORPION_CHICK_CID',
     'dark_scorpion_chick_cid_pool_656c',
     'DARK_SCORPION_CHICK_CID: Dark Scorpion - Chick the Yellow (0x1656)'),

    # --- card_info.inc: DARK_SCORPION_BURGLARS_CID = 0x00001531 (NEW) ---
    (0x08076570, 0x00001531, 'DARK_SCORPION_BURGLARS_CID',
     'dark_scorpion_burglars_cid_pool_6570',
     'DARK_SCORPION_BURGLARS_CID: Dark Scorpion Burglars (pw=40933924; 0x1531)'),

    # --- card_info.inc: DARK_SCORPION_GORG_THE_STRONG_CID = 0x00001685 ---
    (0x08076584, 0x00001685, 'DARK_SCORPION_GORG_THE_STRONG_CID',
     'dark_scorpion_gorg_cid_pool_6584',
     'DARK_SCORPION_GORG_THE_STRONG_CID: Dark Scorpion - Gorg the Strong (0x1685)'),

    # =========================================================================
    # Seg-8b slots (0x76908..0x7738c): 49 slots
    # =========================================================================

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x080769c4, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_69c4', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x080769c8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_69c8',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter byte offset'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080769cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_69cc', None),

    # --- ewram.inc: gP1HandSlotArray = 0x0201c8f8 ---
    (0x080769d0, 0x0201c8f8, 'gP1HandSlotArray',
     'gP1HandSlotArray_pool_69d0', None),

    # --- ewram.inc: HAND_SPELL_SLOT_CC8_OFF = 0x00000cc8 (NEW) ---
    # Reviewer correction: bits[12:0] extracted via ldrh + lsls#19 + lsrs#19
    (0x080769d4, 0x00000cc8, 'HAND_SPELL_SLOT_CC8_OFF',
     'hand_spell_slot_cc8_off_pool_69d4',
     'HAND_SPELL_SLOT_CC8_OFF: gGraveyardSlots slot+0xcc8 set_code field; bits[12:0] via ldrh+lsls#19+lsrs#19'),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x080769f8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_69f8', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076ae0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6ae0', None),

    # --- duel_field.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08076ae4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_6ae4',
     'gDuelFieldSlots: duel field zone slot array base'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08076b14, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_6b14', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076b18, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6b18', None),

    # --- card_info.inc: DD_SCOUT_PLANE_CID = 0x000016be (NEW) ---
    (0x08076ba4, 0x000016be, 'DD_SCOUT_PLANE_CID',
     'dd_scout_plane_cid_pool_6ba4',
     'DD_SCOUT_PLANE_CID: D. D. Scout Plane (pw=03773196; 0x16be)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076ba8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6ba8', None),

    # --- ewram.inc: gP1AltHandSlotArray = 0x0201cab0 ---
    (0x08076bac, 0x0201cab0, 'gP1AltHandSlotArray',
     'gP1AltHandSlotArray_pool_6bac',
     'gP1AltHandSlotArray: P1 alt hand slot array base (EWRAM)'),

    # --- card_info.inc: DD_SCOUT_PLANE_CID = 0x000016be (REUSE after declaring above) ---
    (0x08076be8, 0x000016be, 'DD_SCOUT_PLANE_CID',
     'dd_scout_plane_cid_pool_6be8', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076c48, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6c48', None),

    # --- duel_field.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08076c4c, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_6c4c', None),

    # --- ewram.inc: gEquipChainSlotRefs = 0x0201bb90 ---
    (0x08076c8c, 0x0201bb90, 'gEquipChainSlotRefs',
     'gEquipChainSlotRefs_pool_6c8c',
     'gEquipChainSlotRefs: equip chain slot refs struct base (EWRAM)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076d1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6d1c', None),

    # --- duel_field.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08076d20, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_6d20', None),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08076d24, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_6d24', None),

    # --- duel_field.inc: DISPLAY_SEQ_ACTIVE_PLAYER_OFF = 0x00001d10 ---
    (0x08076dd8, 0x00001d10, 'DISPLAY_SEQ_ACTIVE_PLAYER_OFF',
     'display_seq_active_player_off_pool_6dd8',
     'DISPLAY_SEQ_ACTIVE_PLAYER_OFF: display sequence active player field offset'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08076ddc, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_6ddc', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076eb0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6eb0', None),

    # --- duel_field.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08076eb4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_6eb4', None),

    # --- card_info.inc: BLACK_LUSTER_SOLDIER_ENVOY_CID = 0x000016cb ---
    (0x08076eb8, 0x000016cb, 'BLACK_LUSTER_SOLDIER_ENVOY_CID',
     'black_luster_soldier_envoy_cid_pool_6eb8',
     'BLACK_LUSTER_SOLDIER_ENVOY_CID: Black Luster Soldier - Envoy of the Beginning (0x16cb)'),

    # --- card_info.inc: ENERGY_DRAIN_CID = 0x000016e3 (NEW) ---
    (0x08076f1c, 0x000016e3, 'ENERGY_DRAIN_CID',
     'energy_drain_cid_pool_6f1c',
     'ENERGY_DRAIN_CID: Energy Drain (pw=56916805; 0x16e3)'),

    # --- card_info.inc: BARK_OF_DARK_RULER_CID = 0x000014be ---
    (0x08076f20, 0x000014be, 'BARK_OF_DARK_RULER_CID',
     'bark_of_dark_ruler_cid_pool_6f20',
     'BARK_OF_DARK_RULER_CID: Bark of Dark Ruler (0x14be); runtime: subs #0x2c -> DEAL_OF_PHANTOM_CID=0x1492'),

    # --- card_info.inc: SECRET_OF_THE_BANDIT_CID = 0x00001511 ---
    (0x08076f34, 0x00001511, 'SECRET_OF_THE_BANDIT_CID',
     'secret_of_the_bandit_cid_pool_6f34',
     'SECRET_OF_THE_BANDIT_CID: Secret of the Bandit (0x1511)'),

    # --- card_info.inc: WILD_NATURES_RELEASE_CID = 0x000016ce ---
    (0x08076f38, 0x000016ce, 'WILD_NATURES_RELEASE_CID',
     'wild_natures_release_cid_pool_6f38',
     "WILD_NATURES_RELEASE_CID: Wild Nature's Release (0x16ce)"),

    # --- card_info.inc: GIFT_OF_THE_MARTYR_CID = 0x000018ca (NEW) ---
    (0x08076f50, 0x000018ca, 'GIFT_OF_THE_MARTYR_CID',
     'gift_of_the_martyr_cid_pool_6f50',
     'GIFT_OF_THE_MARTYR_CID: Gift of the Martyr (pw=98792570; 0x18ca)'),

    # --- card_info.inc: HERO_HEART_CID = 0x000019ab ---
    (0x08076f68, 0x000019ab, 'HERO_HEART_CID',
     'hero_heart_cid_pool_6f68',
     'HERO_HEART_CID: Hero Heart (0x19ab)'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08076fb8, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_6fb8', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08076fbc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_6fbc', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x0807703c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_703c', None),

    # --- duel_field.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08077040, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_7040', None),

    # --- oam_attr.inc: EQUIP_SLOT_SCORE_CAP = 0x0000ffff ---
    (0x08077044, 0x0000ffff, 'EQUIP_SLOT_SCORE_CAP',
     'equip_slot_score_cap_pool_7044',
     'EQUIP_SLOT_SCORE_CAP: equip slot score ceiling value (0xffff)'),

    # --- card_info.inc: HERO_KID_CID = 0x000019a7 ---
    (0x080770b0, 0x000019a7, 'HERO_KID_CID',
     'hero_kid_cid_pool_70b0',
     'HERO_KID_CID: Hero Kid (0x19a7)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08077110, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_7110', None),

    # --- duel_field.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08077114, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_7114', None),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08077148, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_7148', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08077278, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_7278', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x0807727c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_727c', None),

    # --- ewram.inc: EQUIP_CHAIN_BASE_OFF = 0x00001c88 ---
    (0x08077280, 0x00001c88, 'EQUIP_CHAIN_BASE_OFF',
     'equip_chain_base_off_pool_7280',
     'EQUIP_CHAIN_BASE_OFF: equip chain entry base offset'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080772cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_72cc', None),

    # --- ewram.inc: gP1FieldArrayCBase = 0x0201c600 ---
    (0x080772d0, 0x0201c600, 'gP1FieldArrayCBase',
     'gP1FieldArrayCBase_pool_72d0', None),

    # --- ewram.inc: EQUIP_CHAIN_BASE_OFF = 0x00001c88 ---
    (0x080772d4, 0x00001c88, 'EQUIP_CHAIN_BASE_OFF',
     'equip_chain_base_off_pool_72d4', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x0807737c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_737c', None),

    # --- ewram.inc: gP1AltHandSlotArray = 0x0201cab0 ---
    (0x08077380, 0x0201cab0, 'gP1AltHandSlotArray',
     'gP1AltHandSlotArray_pool_7380', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: 0 slots (all globals accessed via EQ pc-relative literal pool)
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    8 slots: switch table ptrs + code ptr stubs + sub-stub first entries
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_switchdataD_0807639c_08076398 -> bitmap_dispatch_switch_table_ptr_6398
    # .word 0x0807639c = 6-entry jump table base for switchD_0807638c (already decoded)
    (0x08076398, 'bitmap_dispatch_switch_table_ptr_6398',
     '.word 0x0807639c; jump-table base for switchD_0807638c (6-entry LP-count 1-6); '
     'tick_equip_zone_bitmap_display_seq'),

    # DAT_080763c8 -> check_equip_slot_eligible_by_type_query_ptr_63c8
    # .word 0x080507ad = check_equip_slot_eligible_by_type_query+1 (raw THUMB code addr)
    # Ruling A: RENAME_ONLY + ASCII EOL (non-FS raw code ptr)
    (0x080763c8, 'check_equip_slot_eligible_by_type_query_ptr_63c8',
     '.word 0x080507ad (check_equip_slot_eligible_by_type_query+1); '
     'predicate for build_equip_zone_bitmap_for_player caseD_1/2; Ruling A raw code ptr'),

    # DAT_080763dc -> check_equip_slot_eligible_by_type_query_ptr_63dc
    # .word 0x080507ad (same predicate, zone_pair_hit path caseD_3..5)
    (0x080763dc, 'check_equip_slot_eligible_by_type_query_ptr_63dc',
     '.word 0x080507ad (check_equip_slot_eligible_by_type_query+1); '
     'zone_pair_hit path caseD_3..5; Ruling A raw code ptr'),

    # DAT_080763f4 -> check_equip_slot_eligible_by_side_match_ptr_63f4
    # .word 0x08053f11 = check_equip_slot_eligible_by_side_match_and_type+1
    (0x080763f4, 'check_equip_slot_eligible_by_side_match_ptr_63f4',
     '.word 0x08053f11 (check_equip_slot_eligible_by_side_match_and_type+1); '
     'caseD_6 predicate; Ruling A raw code ptr'),

    # DAT_08076418 -> check_equip_slot_eligible_by_type_query_ptr_6418
    # .word 0x080507ad (same predicate, state 0x7e path)
    (0x08076418, 'check_equip_slot_eligible_by_type_query_ptr_6418',
     '.word 0x080507ad (check_equip_slot_eligible_by_type_query+1); '
     'state 0x7e path for set_equip_activation_state_by_mode; Ruling A raw code ptr'),

    # DAT_080765f0 -> mustering_dark_scorpions_dispatch_sub_stubs_65f0
    # B2 first sub-stub start addr; dispatch table 0x765dc..0x765ef 5-entry raw ptrs
    (0x080765f0, 'mustering_dark_scorpions_dispatch_sub_stubs_65f0',
     'B2 first sub-stub entry; 5 targets via 5-entry dispatch table '
     '(0x765dc..0x765ef); fn_eligible_mustering_dark_scorpions pool ptr'),

    # DAT_080767f8 -> spell_vanishing_dispatch_sub_stubs_67f8
    # B4 first sub-stub start addr; dispatch table 0x767dc..0x767f7 7-entry raw ptrs
    (0x080767f8, 'spell_vanishing_dispatch_sub_stubs_67f8',
     'B4 first sub-stub entry; 7 targets via 7-entry dispatch table '
     '(0x767dc..0x767f7); fn_eligible_spell_vanishing pool ptr'),

    # DAT_0807714c -> equip_effect_opcode_switch_table_ptr_714c
    # .word 0x08077150 = switchdataD start (29-entry table); switchD_08077144
    (0x0807714c, 'equip_effect_opcode_switch_table_ptr_714c',
     '.word 0x08077150 (switchdataD 29-entry table start); switchD_08077144 in '
     'dispatch_equip_effect_node_by_opcode; Ruling A raw table ptr'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: 0 updates (all Seg-8 plates are ASCII-clean, no FUN_ found)
# ---------------------------------------------------------------------------
PLATE_REWRITES = []

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

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

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

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg8Slots (DRY=%s) ===" % DRY)
    print("  EQ=%d  REF=%d  RENAME=%d" % (len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS)))

    fail_count = 0

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS ---")
    for (sa, val, eq_name, slot_label, eol) in EQ_SLOTS:
        _apply_eq(sa, val, eq_name, slot_label, eol)

    # B. REF_SLOTS (none)
    print("\n--- B. REF_SLOTS (0 slots) ---")

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS ---")
    for (sa, label, eol) in RENAME_SLOTS:
        _apply_rename(sa, label, eol)

    # D. PLATE_REWRITES (none)
    print("\n--- D. PLATE_REWRITES (0 updates) ---")

    print("\n=== RefineF09Seg8Slots DONE ===")
    print("  EQ_SLOTS applied: %d" % len(EQ_SLOTS))
    print("  RENAME_SLOTS applied: %d" % len(RENAME_SLOTS))
    print("  fail_count: %d" % fail_count)

main()
