# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg7Slots.py -- F07 Seg-7 (0x080613b4..0x08061eb4)
#   Symbolizes 65 auto-name slots: EQ=44 + REF=18 + RENAME=2 + FUNC_RENAME=1
#   Proposal: doc/dev/refine/F07-Seg-7.proposal.md (PASS)
#
# Sections:
#   A. EQ_SLOTS  -- data-equate (44 slots; excludes 18 REF + 2 RENAME which are in B/C)
#   B. REF_SLOTS -- USER-label on target + DATA-ref from slot + rename slot (18 slots)
#   C. RENAME_SLOTS -- pure rename + EOL (2 fn-ptr slots)
#   F. FUNC_RENAME -- misname correction (1 function: check_zera_ritual -> check_banisher_of_light)
#   E. PLATE_REWRITES -- 11 plate rewrites (7 CJK full rewrite + 3 gDuelEffectCtx->gEquipChainSlotRefs + 1 post-rename)
#
# Prerequisites (added to constants/ before running this script):
#   card_info.inc +7 NEW:
#     REVERSAL_OF_GRAVES_CID=0x14f0, BLASTING_THE_RUINS_CID=0x16dc
#     BURST_STREAM_OF_DESTRUCTION_CID=0x175b, SANCTUARY_IN_THE_SKY_CID=0x175e
#     INFERNO_FIRE_BLAST_CID=0x17f6, PROTECTOR_OF_SANCTUARY_CID=0x178b
#     MASK_OF_RESTRICT_CID=0x13f2
#   ewram.inc +1 NEW:
#     LP_GAP_THRESHOLD_7000=0x1b58
#   (all already in ewram.inc REUSE):
#     gP1LifePoints=0x0201c4e0, PLAYER_BLOCK_STRIDE=0x868
#     gDuelFieldSlots=0x0201c510, gDuelFieldSlots_p2_base=0x0201c5d8
#     gEquipChainSlotRefs=0x0201bb90, gP1FieldArrayCBase=0x0201c600
#     gP1ZoneHandCount=0x0201c4ec, FIELD5_SCORE_THRESHOLD_1999=0x7cf
#   (all already in card_info.inc REUSE):
#     BANISHER_OF_THE_LIGHT_CID=0x1332, UMI_CARD_ID=0x10f4
#     BLUE_EYES_WHITE_DRAGON_CID=0x0fa7, RED_EYES_B_DRAGON_CID=0x0ff8
#     FIELD_STATE_OFF=0x1cf4 (duel_field.inc reuse)
#
# FUNC_RENAME=1: check_zera_ritual_absent_from_field -> check_banisher_of_light_absent_from_field
# carve=0, disasm=1 block (handled by DisassembleF07Seg7Block.py)
# REF disasm slots handled in DisassembleF07Seg7Block.py (gp1lp_ptr_08061c84, player_stride_08061c88)
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614172914-pre-F07Seg7

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, const_name, slot_label)
#    44 slots: does NOT include the 16 gP1LP DWORD_ / 6 PTR_ / 1 gP1ZoneHandCount DAT_ (those are in B)
#    nor the 2 fn-ptr RENAME-only slots (those are in C).
#    All values verified by proposal review C4.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ===== CID NEW: REVERSAL_OF_GRAVES_CID = 0x14f0 =====
    (0x080613cc, 0x000014f0, 'REVERSAL_OF_GRAVES_CID',    'reversal_of_graves_cid_080613cc'),

    # ===== CID NEW: BLASTING_THE_RUINS_CID = 0x16dc =====
    (0x080613d0, 0x000016dc, 'BLASTING_THE_RUINS_CID',    'blasting_the_ruins_cid_080613d0'),

    # ===== PLAYER_BLOCK_STRIDE = 0x868 (ewram.inc REUSE; 14 slots) =====
    (0x08061400, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061400'),
    (0x08061500, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061500'),
    (0x08061538, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061538'),
    (0x080615c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080615c4'),
    (0x080616bc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080616bc'),
    (0x080617a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080617a4'),
    (0x0806186c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0806186c'),
    (0x080618ac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080618ac'),
    (0x08061934, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061934'),
    (0x0806197c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_0806197c'),
    (0x080619b4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_080619b4'),
    (0x08061ab8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061ab8'),
    (0x08061b48, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061b48'),
    (0x08061b98, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061b98'),
    (0x08061c0c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061c0c'),
    (0x08061df8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061df8'),
    (0x08061e8c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_08061e8c'),

    # ===== CID REUSE: BANISHER_OF_THE_LIGHT_CID = 0x1332 (card_info.inc reuse; 3 slots) =====
    (0x080614fc, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_080614fc'),
    (0x080615c0, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_080615c0'),
    (0x08061a08, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_08061a08'),

    # ===== gDuelFieldSlots = 0x0201c510 (ewram.inc REUSE; 3 slots) =====
    (0x08061504, 0x0201c510, 'gDuelFieldSlots', 'gdfs_ref_08061504'),
    (0x080616c0, 0x0201c510, 'gDuelFieldSlots', 'gdfs_ref_080616c0'),
    (0x080617a8, 0x0201c510, 'gDuelFieldSlots', 'gdfs_ref_080617a8'),

    # ===== gP1FieldArrayCBase = 0x0201c600 (ewram.inc REUSE; 2 slots) =====
    (0x0806150c, 0x0201c600, 'gP1FieldArrayCBase', 'gp1fac_ref_0806150c'),
    (0x08061870, 0x0201c600, 'gP1FieldArrayCBase', 'gp1fac_ref_08061870'),

    # ===== gEquipChainSlotRefs = 0x0201bb90 (ewram.inc REUSE; 5 slots) =====
    # Note: several of these have plates calling it gDuelEffectCtx -- plates corrected in section E.
    (0x08061578, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_ctx_ref_08061578'),
    (0x080617e8, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_ctx_ref_080617e8'),
    (0x080619e0, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_ctx_ref_080619e0'),
    (0x08061cbc, 0x0201bb90, 'gEquipChainSlotRefs', 'gequip_ctx_ref_08061cbc'),
    # DWORD_08061abc is in REF_SLOTS (gP1ZoneHandCount DAT ref)

    # ===== gDuelFieldSlots_p2_base = 0x0201c5d8 (ewram.inc REUSE; 1 slot) =====
    (0x080615c8, 0x0201c5d8, 'gDuelFieldSlots_p2_base', 'gdfs_p2_ref_080615c8'),

    # ===== UMI_CARD_ID = 0x10f4 (card_info.inc REUSE; 1 slot) =====
    (0x080615cc, 0x000010f4, 'UMI_CARD_ID', 'umi_cid_080615cc'),

    # ===== LP_GAP_THRESHOLD_7000 = 0x1b58 (ewram.inc NEW; 1 slot) =====
    (0x080618b0, 0x00001b58, 'LP_GAP_THRESHOLD_7000', 'lp_gap_7000_080618b0'),

    # ===== FIELD5_SCORE_THRESHOLD_1999 = 0x7cf (card_info.inc REUSE; 1 slot) =====
    (0x080619e4, 0x000007cf, 'FIELD5_SCORE_THRESHOLD_1999', 'score_thresh_1999_080619e4'),

    # ===== DAT_ gEquipChainSlotRefs slots (same 0x0201bb90; no DWORD_ prefix) =====
    # Plate for check_equip_slot_eligible_field_spell_with_effect_context_zone_val10 (0x0806153c)
    # says gDuelEffectCtx -> FIX in plates section

    # ===== FIELD_STATE_OFF = 0x1cf4 (duel_field.inc REUSE; 2 slots) =====
    (0x08061900, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_08061900'),
    (0x08061dbc, 0x00001cf4, 'FIELD_STATE_OFF', 'field_state_off_08061dbc'),

    # ===== CID NEW: BURST_STREAM_OF_DESTRUCTION_CID = 0x175b (card_info.inc NEW; 1 slot) =====
    (0x08061ad4, 0x0000175b, 'BURST_STREAM_OF_DESTRUCTION_CID', 'burst_stream_cid_08061ad4'),

    # ===== BLUE_EYES_WHITE_DRAGON_CID = 0x0fa7 (card_info.inc REUSE; 1 slot) =====
    (0x08061adc, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID', 'blue_eyes_cid_08061adc'),

    # ===== RED_EYES_B_DRAGON_CID = 0x0ff8 (card_info.inc REUSE; 1 slot) =====
    (0x08061b08, 0x00000ff8, 'RED_EYES_B_DRAGON_CID', 'red_eyes_cid_08061b08'),

    # ===== SANCTUARY_IN_THE_SKY_CID = 0x175e (card_info.inc NEW; 1 slot) =====
    (0x08061b90, 0x0000175e, 'SANCTUARY_IN_THE_SKY_CID', 'sanctuary_cid_08061b90'),

    # ===== MASK_OF_RESTRICT_CID = 0x13f2 (card_info.inc NEW; 1 slot) =====
    (0x08061c5c, 0x000013f2, 'MASK_OF_RESTRICT_CID', 'mask_restrict_cid_08061c5c'),

    # ===== DAT_ BANISHER slot (reuse; 1 slot) =====
    (0x08061d50, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID', 'banisher_cid_08061d50'),

    # ===== PROTECTOR_OF_SANCTUARY_CID = 0x178b (card_info.inc NEW; 1 slot) =====
    (0x08061dc0, 0x0000178b, 'PROTECTOR_OF_SANCTUARY_CID', 'protector_sanctuary_cid_08061dc0'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label)
#    18 slots: 16 gP1LifePoints (10 DWORD_ + 6 PTR_) + 1 gP1ZoneHandCount + (2 new from disasm handled in DisassembleF07Seg7Block.py)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # ===== gP1LifePoints = 0x0201c4e0 (ewram.inc; 16 pre-existing slots) =====
    # 10 DWORD_ slots
    (0x08061508, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061508'),
    (0x08061868, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061868'),
    (0x080618a8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080618a8'),
    (0x08061c08, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061c08'),
    (0x08061d34, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061d34'),
    (0x08061db8, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061db8'),
    (0x08061df4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061df4'),
    (0x08061e88, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061e88'),
    (0x080613fc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080613fc'),
    (0x08061618, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061618'),
    # 6 PTR_ slots
    (0x080618fc, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080618fc'),
    (0x08061978, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061978'),
    (0x080619b0, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_080619b0'),
    (0x08061ab4, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061ab4'),
    (0x08061b44, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061b44'),
    (0x08061b94, 0x0201c4e0, 'gP1LifePoints', 'gp1lp_ptr_08061b94'),
    # ===== gP1ZoneHandCount = 0x0201c4ec (ewram.inc; 1 DAT_ slot) =====
    (0x08061abc, 0x0201c4ec, 'gP1ZoneHandCount', 'gp1zonehandcount_ref_08061abc'),
    # NOTE: 2 additional REF slots from disasm block (gp1lp_ptr_08061c84 + player_stride_08061c88)
    # are handled in DisassembleF07Seg7Block.py
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, label, eol_ascii_or_None)
#    2 fn-ptr slots: RENAME-only + EOL comment
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08061d74, 'zone_pair_pred_07ad_ptr_08061d74',
     '[fn-ptr] check_equip_slot_eligible_by_type_query+1'),
    (0x08061eb0, 'zone_pair_pred_1e95_ptr_08061eb0',
     '[fn-ptr] check_equip_slot_eligible_by_side_mismatch_and_prereqs+1'),
]

# ---------------------------------------------------------------------------
# F. FUNC_RENAME: (fn_addr, old_name, new_name)
#    Misname correction: 0x1332 = BANISHER_OF_THE_LIGHT_CID (not Zera Ritual 0x1245)
# ---------------------------------------------------------------------------
FUNC_RENAME = [
    (0x08061d40,
     'check_zera_ritual_absent_from_field',
     'check_banisher_of_light_absent_from_field'),
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (fn_entry_addr, new_plate_text)
#    11 plates: 7 CJK full rewrites + 3 gDuelEffectCtx name corrections + 1 post-FUNC_RENAME
#    All new_plate_text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # 1. check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect @ 0x08061660
    #    CJK plate -> full ASCII rewrite
    (0x08061660,
     'Equip slot activation eligibility predicate, two-level condition: '
     '(1) check_field_spell_neo_daedalus_group_placeable(player_id) == 0 return 0; '
     '(2) check_equip_slot_eligible_by_lp_slot_and_effect_dispatch(slot_ptr, arg) pass-through. '
     'Semantics: Neo Daedalus field group condition must be satisfied before evaluating '
     'LP slot effect dispatch eligibility.'
    ),

    # 3. check_equip_slot_eligible_type480_with_neo_daedalus_field5_loop @ 0x080617ac
    #    CJK plate -> full ASCII rewrite; also fixes gDuelEffectCtx -> gEquipChainSlotRefs
    (0x080617ac,
     'Equip slot activation eligibility predicate, five-level condition: '
     '(1) slot[+2] halfword bits[10:6] must be 0x16 (zone_type mask 0xfc0 == 0x480, 0x90<<3); '
     '(2) slot[+0x14] must be nonzero; '
     '(3) gEquipChainSlotRefs[+0x4] (activation context player id) != player_id (direction check); '
     '(4) check_neo_daedalus_placement_eligible must pass; '
     '(5) loop over gP1FieldArrayCBase[player*PLAYER_BLOCK_STRIDE] entries '
     '(LP_LOOP_CEIL_OFF=0xc count bound): for each LP zone entry extracts 13-bit card_id, '
     'calls check_card_field5_is_nonzero; if nonzero calls '
     'eval_equip_placement_full_check(player_id, card_id, 0); if any pass returns 1. '
     'Returns 0 if all fail. '
     'Constants: ZONE_TYPE_MASK=0xfc0, ZONE_TYPE_480=0x480, LP_SLOT_ACTIVE_OFF=0x10, '
     'gEquipChainSlotRefs=0x0201bb90, LP_LOOP_CEIL_OFF=0xc, PLAYER_BLOCK_STRIDE=0x868.'
    ),

    # 4. check_equip_slot_eligible_neo_daedalus_with_lp_status_lookup @ 0x08061938
    #    CJK plate -> full ASCII rewrite
    (0x08061938,
     'Equip slot activation eligibility predicate, two-level condition with early fast-path: '
     '(1) check_neo_daedalus_placement_eligible must pass else return 0; '
     '(2) read gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)] '
     '(player LP status word); if nonzero return 1 (fast pass); if zero: call '
     'lookup_slot_display_value_by_card_id(slot_ptr)->r2, then '
     'dispatch_effect_handler_by_card_id(player_id, card_id, display_value); '
     'return 1 if dispatch nonzero else 0. '
     'Constants: PLAYER_BLOCK_STRIDE=0x868, LP_SLOT_ACTIVE_OFF=0x10.'
    ),

    # 5. check_equip_slot_eligible_by_active_ctx_score_threshold @ 0x080619c0
    #    CJK plate -> full ASCII rewrite; also fixes gDuelEffectCtx -> gEquipChainSlotRefs
    (0x080619c0,
     'Equip slot activation eligibility predicate, two-level condition: '
     '(1) check_equip_slot_state_active_with_card_present must pass else return 0; '
     '(2) load gEquipChainSlotRefs[+0x4] (activation context player id) and '
     '[+0x20] (context zone_idx); call get_slot_field6_score(player_id, zone_idx); '
     'if score > FIELD5_SCORE_THRESHOLD_1999(0x7cf=1999) return 1 else return 0. '
     'Semantics: equip slot active and activation context target zone field6 score exceeds 1999. '
     'Constants: gEquipChainSlotRefs=0x0201bb90, offset+0x4=activation_player, '
     'offset+0x20=context_zone_idx, FIELD5_SCORE_THRESHOLD_1999=0x7cf.'
    ),

    # 6. dispatch_effect_via_hand_slot_setcode @ 0x080619f0
    #    Existing plate has "Zera Ritual (passcode=81756897)" for CID 0x1332 -- WRONG.
    #    CID 0x1332 = Banisher of the Light. Full ASCII rewrite correcting this.
    (0x080619f0,
     'Step 1: count_field_copies_of_card(BANISHER_OF_THE_LIGHT_CID=0x1332) '
     '-- Banisher of the Light (pw=61528025). '
     'If > 0 -> return 0 (Banisher on field blocks activation). '
     'Step 2: read hand_count from gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_LOOP_CEIL_OFF(0xc)]. '
     'Iterate hand slots (index 0..hand_count-1): '
     '- read zone descriptor from gP1FieldArrayCBase[player*stride+zone_idx*4]; '
     'extract bits[23:16] then <<1 -> zone_setcode. '
     '- read slot[+4] bits[14:8] (7-bit set_code) -> slot_setcode. '
     '- if zone_setcode == slot_setcode: '
     'dispatch_effect_handler_by_card_id(player_id, card_id, zone_idx). '
     'If dispatch returns nonzero -> return 1. '
     'Returns 0 if loop exhausted without match or Banisher present. '
     'Called by 6+ callers; core hand-slot set_code matching logic.'
    ),

    # 7. check_equip_slot_eligible_zone_e_type580_with_neo_daedalus @ 0x08061cc8
    #    CJK plate -> full ASCII rewrite
    (0x08061cc8,
     'Equip slot activation eligibility predicate, five-level condition: '
     '(1) slot[+2] halfword bits[10:6] must be 0x16 (zone_type mask 0xfc0 == 0x580, 0xb0<<3); '
     '(2) slot[+0x14] bit9 (lsls#0x16/lsrs#0x1f) must equal 1-player_id (direction check); '
     '(3) slot[+0x14] bits[22:19] must be 0xe (zone E index); '
     '(4) read gP1LifePoints zone card_id, call check_card_field5_is_nonzero; '
     '(5) slot[+0x14] bits[8:0] bit0 must equal 1-player_id (second direction check); '
     'all pass: call check_neo_daedalus_placement_eligible(slot_ptr, arg) and return its value. '
     'Sibling of check_equip_slot_eligible_field_spell_effect_type_e_with_zone_field5 '
     'with added fifth check and Neo Daedalus call. '
     'Constants: ZONE_TYPE_MASK=0xfc0, ZONE_TYPE_FIELD_SPELL=0x580, ZONE_E_INDEX=0xe, '
     'LP_ZONE_OFFSET=0x10e0 (0x87<<5), PLAYER_BLOCK_STRIDE=0x868.'
    ),

    # 8. check_equip_slot_eligible_by_lp_status_tier3_neo_daedalus @ 0x08061dcc
    #    CJK plate -> full ASCII rewrite
    (0x08061dcc,
     'Equip slot activation eligibility predicate, two-level condition: '
     '(1) read gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)] '
     '(player LP status word); if <= 3 return 0 (bls path); '
     '(2) check_neo_daedalus_placement_eligible(slot_ptr, arg) pass-through. '
     'Semantics: LP status word must be > 3 to proceed to Neo Daedalus placement check. '
     'Isomorphic to check_equip_slot_eligible_by_duel_phase3_neo_daedalus (0x08060484) '
     'but threshold > 3 vs == 3. '
     'Constants: PLAYER_BLOCK_STRIDE=0x868, LP_SLOT_ACTIVE_OFF=0x10.'
    ),

    # 9. check_equip_slot_eligible_chain_present_with_lp_status_neo_daedalus @ 0x08061e50
    #    CJK plate -> full ASCII rewrite
    (0x08061e50,
     'Equip slot activation eligibility predicate, three-level condition: '
     '(1) check_value_in_slot_chain(player_id, card_id, CHAIN_TYPE=0xb) -- '
     'if chain node absent return 0; '
     '(2) read gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)] '
     '(LP status word) -- if zero return 0; '
     '(3) check_neo_daedalus_placement_eligible(slot_ptr, arg) pass-through. '
     'Semantics: equip chain already contains target value AND LP status nonzero before '
     'evaluating Neo Daedalus condition. '
     'Constants: CHAIN_TYPE=0xb, PLAYER_BLOCK_STRIDE=0x868, LP_SLOT_ACTIVE_OFF=0x10.'
    ),

    # 10. check_equip_slot_eligible_field_spell_with_effect_context_zone_val10 @ 0x0806153c
    #     Non-CJK plate; gDuelEffectCtx -> gEquipChainSlotRefs fix
    (0x0806153c,
     'Equip slot activation eligibility predicate, three-level condition: '
     '(1) slot[+2] halfword bits[10:6] must be 0x16 (zone_type mask 0xfc0 == 0x580, 0xb0<<3); '
     '(2) read slot[+0x14] bits[8:0] and compare with gEquipChainSlotRefs[+0x70]; '
     'if match use offset=0x88, else use offset=0x50; '
     '(3) read gEquipChainSlotRefs[+offset], if == 0xa (10) return 1 else return 0. '
     'Constants: SPELL_TYPE_MASK=0xfc0, FIELD_SPELL_TYPE=0x580, gEquipChainSlotRefs=0x0201bb90, '
     'CTX_ZONE_REF_OFF=0x70, CTX_SLOT_MATCH_OFF=0x88, CTX_SLOT_NOMATCH_OFF=0x50, EXPECTED_VAL=0xa.'
    ),

    # 11. check_banisher_of_light_absent_from_field @ 0x08061d40 (post-FUNC_RENAME)
    #     Was check_zera_ritual_absent_from_field; plate said "Zera Ritual" -- WRONG.
    #     CID 0x1332 = Banisher of the Light (pw=61528025)
    (0x08061d40,
     'Void-param predicate: r0 overwritten at entry by '
     'ldr DAT_08061d50=BANISHER_OF_THE_LIGHT_CID(0x1332=Banisher of the Light, pw=61528025). '
     'Calls count_field_copies_of_card(0x1332). '
     'Returns 1 if count==0 (absent); 0 if any copy present. '
     'Inverse of Banisher presence check. '
     'Distinct from check_equip_slot_eligible_banisher_absent_with_umi_pair '
     'which also checks Umi pairing.'
    ),
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF07Seg7Slots (DRY=%s) ===" % DRY)
    rm      = currentProgram.getReferenceManager()
    et      = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    fn_mgr  = currentProgram.getFunctionManager()
    nA = nB = nC = nF = nE = 0
    made = set()

    # --- A. EQ_SLOTS ---
    print("--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err)); continue
        if DRY:
            print("[A dry] 0x%08x equate %s=0x%x rename %s" % (slot_int, cname, value, label))
            nA += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname)); nA += 1

    # --- B. REF_SLOTS ---
    print("--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for slot_int, tgt_int, gas_label, slot_label in REF_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[B FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[B dry] 0x%08x ref->0x%08x (%s) rename %s" % (slot_int, tgt_int, gas_label, slot_label))
            nB += 1; continue
        if tgt_int not in made:
            createLabel(_addr(tgt_int), gas_label, True, SourceType.USER_DEFINED)
            made.add(tgt_int)
        ref = rm.addMemoryReference(_addr(slot_int), _addr(tgt_int), RefType.DATA, SourceType.USER_DEFINED, 0)
        rm.setPrimary(ref, True)
        createLabel(_addr(slot_int), slot_label, True, SourceType.USER_DEFINED)
        print("[B ok] 0x%08x -> %s (ref->%s)" % (slot_int, slot_label, gas_label)); nB += 1

    # --- C. RENAME_SLOTS ---
    print("--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int); continue
        if DRY:
            print("[C dry] 0x%08x rename %s eol=%s" % (slot_int, label, repr(eol))); nC += 1; continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            cu = listing.getCodeUnitAt(_addr(slot_int))
            if cu is not None:
                bad = any(ord(ch) > 127 for ch in eol)
                if bad:
                    print("[C WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_int)
                else:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label)); nC += 1

    # --- F. FUNC_RENAME ---
    print("--- F. FUNC_RENAME (%d) ---" % len(FUNC_RENAME))
    for fn_int, old_name, new_name in FUNC_RENAME:
        fn = fn_mgr.getFunctionAt(_addr(fn_int))
        if fn is None:
            print("[F FAIL] no function at 0x%08x" % fn_int); continue
        actual = fn.getName()
        if actual == new_name:
            print("[F skip] 0x%08x already named %s" % (fn_int, new_name)); nF += 1; continue
        if DRY:
            print("[F dry] 0x%08x: '%s' -> '%s'" % (fn_int, actual, new_name)); nF += 1; continue
        fn.setName(new_name, SourceType.USER_DEFINED)
        print("[F ok] 0x%08x: '%s' -> '%s'" % (fn_int, old_name, new_name)); nF += 1

    # --- E. PLATE_REWRITES ---
    print("--- E. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    for fn_int, new_plate in PLATE_REWRITES:
        cu = listing.getCodeUnitAt(_addr(fn_int))
        if cu is None:
            print("[E FAIL] no CodeUnit at 0x%08x" % fn_int); continue
        bad = any(ord(ch) > 127 for ch in new_plate)
        if bad:
            print("[E FAIL] non-ASCII in new_plate @ 0x%08x -- skipping" % fn_int)
            continue
        if DRY:
            existing = cu.getComment(CodeUnit.PLATE_COMMENT)
            has_cjk = existing is not None and any(ord(ch) > 127 for ch in existing)
            print("[E dry] 0x%08x: rewrite plate (%d chars); existing has_cjk=%s" % (
                fn_int, len(new_plate), has_cjk))
            nE += 1; continue
        cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
        print("[E ok] 0x%08x plate rewrite (%d chars)" % (fn_int, len(new_plate))); nE += 1

    print("[done] A=%d B=%d C=%d F=%d E=%d (DRY=%s)" % (nA, nB, nC, nF, nE, DRY))
    print("EQ=%d REF=%d RENAME=%d FUNC_RENAME=%d PLATE=%d (expected 44+17+2+1+11)" % (
        nA, nB, nC, nF, nE))


main()
