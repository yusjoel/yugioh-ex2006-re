# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg4Slots.py -- file 04 Seg-4 (0x080417f0..0x0804308c)
#   19 functions:
#   tick_zone_slot_ref_track_display_seq / tick_equip_attach_display_sequence /
#   tick_card_display_op3e_seq / tick_equip_zone_shuffle_display_seq /
#   tick_card_display_op43_seq / tick_zone_equip_link_placement_seq /
#   tick_card_flip_reveal_display_seq / tick_zone_card_relocate_display_seq /
#   tick_normal_summon_zone_placement_seq / tick_equip_chain_count_check_sequence /
#   tick_card_discard_display_seq / tick_draw_card_display_seq /
#   invoke_draw_display_seq_forward / invoke_draw_display_seq_reverse /
#   tick_display_op0d_with_lp_update_seq / reset_equip_chain_entry_by_player /
#   resolve_equip_target_slot_for_enqueue / dispatch_equip_chain_slot_scan_by_player /
#   enqueue_sprite_attr_with_mode
#
# Sections:
#   A. EQ_SLOTS    -- 141 slots (all reuse except 10 new constants)
#   B. REF_SLOTS   -- 15 slots (12x PTR_gP1LifePoints + 3 new)
#   C. RENAME_SLOTS -- 3 BLOCKED CID slots
#   D. PLATE_REWRITES -- 9 functions with stale FUN_0803be4c
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).
# NOTE: FUNC_RENAME = 0 (no function renames in this segment).

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
#    All values verified against roms/2343.gba (python struct.unpack_from).
#    PTR_gP1LifePoints_* slots handled in REF_SLOTS below.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # === tick_zone_slot_ref_track_display_seq (0x080417f0) ===
    (0x0804185c, 0x0201bcc0, 'gDuelDisplaySeqState',       'track_state_base',              None),
    (0x08041864, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',     'track_lp_track_base_off',       None),
    (0x08041868, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'track_step_lock_off',           None),
    # === tick_equip_attach_display_sequence (0x0804186c) ===
    (0x080418a0, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_attach_state_base',       None),
    (0x080418a4, 0x0201e2a0, 'gDuelCardCtxBase',           'equip_attach_card_ctx',         None),
    (0x08041904, 0x000012e5, 'POLYMERIZATION_CID',         'equip_attach_poly_cid',
     'POLYMERIZATION_CID=0x12e5: equip chain node depth table index check'),
    (0x08041908, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_attach_state_base_b',     None),
    (0x08041924, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_attach_state_base_c',     None),
    (0x08041928, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'equip_attach_step_lock_off',    None),
    # === tick_card_display_op3e_seq (0x0804192c) ===
    (0x08041980, 0x0201bcc0, 'gDuelDisplaySeqState',       'op3e_state_base',               None),
    (0x08041984, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'op3e_step_lock_off',            None),
    # === tick_equip_zone_shuffle_display_seq (0x08041988) ===
    (0x080419c0, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_shuffle_state_base',      None),
    (0x080419f0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'equip_shuffle_step_lock_off',   None),
    # === tick_card_display_op43_seq (0x08041b70) ===
    (0x08041b44, 0x0201bcc0, 'gDuelDisplaySeqState',       'op43_state_base',               None),
    (0x08041b6c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'op43_step_lock_off',            None),
    # === tick_zone_equip_link_placement_seq (0x08041bb4) ===
    (0x08041bac, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_link_state_base',         None),
    (0x08041bb0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'equip_link_step_lock_off',      None),
    (0x08041bf4, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_link_state_base_b',       None),
    (0x08041bf8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'equip_link_step_lock_b_off',    None),
    (0x08041b38, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'equip_link_player_stride',      None),
    (0x08041b3c, 0x0201c510, 'gDuelFieldSlots',            'equip_link_field_slots',        None),
    (0x08041b40, 0x0201c520, 'gDuelFieldSlotState',        'equip_link_slot_state',         None),
    (0x08041b44, 0x0201bcc0, 'gDuelDisplaySeqState',       'equip_link_state_base_c',       None),
    (0x08041c28, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',  'equip_link_seq_step_off',       None),
    # === tick_card_flip_reveal_display_seq (0x08041ef0) ===
    (0x08041e30, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'flip_reveal_player_stride',     None),
    (0x08041e34, 0x0000165a, 'A_DEAL_WITH_DARK_RULER_CID', 'flip_reveal_dark_ruler_cid',
     'A_DEAL_WITH_DARK_RULER_CID=0x165a: chain_type arg check in tick_card_flip_reveal_display_seq'),
    (0x08041e38, 0x000016da, 'SOUL_ABSORPTION_CID',        'flip_reveal_soul_absorb_cid',
     'SOUL_ABSORPTION_CID=0x16da: second chain_type arg check'),
    (0x08041e3c, 0x0201c510, 'gDuelFieldSlots',            'flip_reveal_field_slots',       None),
    (0x08041e40, 0x0201e2a0, 'gDuelCardCtxBase',           'flip_reveal_card_ctx',          None),
    (0x08041e44, 0x0201c4d8, 'gDuelChainDescBase',         'flip_reveal_chain_desc',        None),
    (0x08041e48, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',        'flip_reveal_slot_mask_a',       None),
    (0x08041e4c, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',      'flip_reveal_slot_mask_b',       None),
    (0x08041e50, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',      'flip_reveal_slot_mask_c',       None),
    (0x08041ee4, 0x0201c4d8, 'gDuelChainDescBase',         'flip_reveal_chain_desc_b',      None),
    (0x08041ee8, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',      'flip_reveal_slot_mask_d',       None),
    (0x08041eec, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',      'flip_reveal_slot_mask_e',       None),
    (0x08041f14, 0x0201bcc0, 'gDuelDisplaySeqState',       'flip_reveal_state_base',        None),
    (0x08041f74, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'flip_reveal_player_stride_b',   None),
    (0x08041f78, 0x0201c510, 'gDuelFieldSlots',            'flip_reveal_field_slots_b',     None),
    (0x08041fb4, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'flip_reveal_player_stride_c',   None),
    (0x08041fb8, 0x0201c510, 'gDuelFieldSlots',            'flip_reveal_field_slots_c',     None),
    (0x08041fbc, 0x0201bcc0, 'gDuelDisplaySeqState',       'flip_reveal_state_base_b',      None),
    (0x08041fe0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'flip_reveal_step_lock_off',     None),
    # === tick_zone_card_relocate_display_seq (0x08041fe4) ===
    (0x08042020, 0x0201bcc0, 'gDuelDisplaySeqState',       'relocate_state_base',           None),
    (0x080421a8, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',  'relocate_seq_step_off',         None),
    (0x080421ac, 0x00000818, 'DISP_SEQ_CARD_SET_CTR_OFF',  'relocate_card_set_ctr_off',     None),
    (0x080421b0, 0x0201e2a0, 'gDuelCardCtxBase',           'relocate_card_ctx',             None),
    (0x080421b4, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',        'relocate_slot_mask_a',          None),
    (0x080421b8, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',      'relocate_slot_mask_b',          None),
    (0x080421bc, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',      'relocate_slot_mask_c',          None),
    (0x080421c0, 0x0201c4d8, 'gDuelChainDescBase',         'relocate_chain_desc',           None),
    (0x08042284, 0x00001cf4, 'FIELD_STATE_OFF',            'relocate_field_state_off',      None),
    (0x08042288, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'relocate_player_stride',        None),
    (0x0804228c, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',  'relocate_seq_step_off_b',       None),
    (0x08042290, 0x000015c7, 'COST_DOWN_CID',              'relocate_cost_down_cid',
     'COST_DOWN_CID=0x15c7: chain cost check in tick_zone_card_relocate_display_seq'),
    (0x08042294, 0x0201c510, 'gDuelFieldSlots',            'relocate_field_slots',          None),
    (0x08042298, 0x0201bcc0, 'gDuelDisplaySeqState',       'relocate_state_base_b',         None),
    (0x080422c0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'relocate_step_lock_off',        None),
    # === tick_normal_summon_zone_placement_seq (0x080422c4) ===
    (0x08042310, 0x0201bcc0, 'gDuelDisplaySeqState',       'nsummon_state_base',            None),
    (0x080423e4, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',    'nsummon_set_code_mask',         None),
    (0x080423e8, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',       'nsummon_oam_tile_clear',        None),
    (0x080423ec, 0xc03fffff, 'SLOT_CHAIN_CTR_CLR',         'nsummon_chain_ctr_clr',         None),
    (0x080423f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'nsummon_player_stride',         None),
    (0x080423f8, 0x0201c510, 'gDuelFieldSlots',            'nsummon_field_slots',           None),
    (0x080423fc, 0x0201bcc0, 'gDuelDisplaySeqState',       'nsummon_state_base_b',          None),
    (0x08042440, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'nsummon_player_stride_b',       None),
    (0x08042444, 0x0201c510, 'gDuelFieldSlots',            'nsummon_field_slots_b',         None),
    (0x0804246c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'nsummon_step_lock_off',         None),
    (0x08042498, 0x0201bcc0, 'gDuelDisplaySeqState',       'nsummon_state_base_c',          None),
    (0x080424c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'nsummon_player_stride_c',       None),
    (0x080424c4, 0x0201c510, 'gDuelFieldSlots',            'nsummon_field_slots_c',         None),
    (0x080424c8, 0x0201bcc0, 'gDuelDisplaySeqState',       'nsummon_state_base_d',          None),
    (0x080424cc, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'nsummon_step_lock_off_c',       None),
    (0x080424e8, 0x0201bcc0, 'gDuelDisplaySeqState',       'nsummon_state_base_e',          None),
    # === tick_equip_chain_count_check_sequence (0x08042470) ===
    (0x08042498, 0x0201bcc0, 'gDuelDisplaySeqState',       'chain_chk_state_base',          None),
    (0x0804251c, 0x00001130, 'EQUIP_CHAIN_STEP_BASE_OFF',  'chain_chk_step_base_off',
     'EQUIP_CHAIN_STEP_BASE_OFF=0x1130: [gEquipChainSlotRefs+0x1130] step array base arg'),
    (0x08042540, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'chain_chk_step_lock_off',       None),
    # === tick_card_discard_display_seq (0x08042544) ===
    (0x08042564, 0x0201bcc0, 'gDuelDisplaySeqState',       'discard_state_base',            None),
    (0x080425e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'discard_player_stride',         None),
    (0x080425ec, 0x000010dc, 'LP_DISCARD_ZONE_OFF',        'discard_lp_zone_off',
     'LP_DISCARD_ZONE_OFF=0x10dc: [gP1LifePoints+player*0x868+0x10dc] LP discard zone field'),
    (0x080425f0, 0x00001cfc, 'DISP_SET_VARIANT_OFF',       'discard_disp_variant_off',      None),
    (0x080425f8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'discard_step_lock_off',         None),
    # === tick_draw_card_display_seq (0x080425fc) ===
    (0x08042634, 0x0201bcc0, 'gDuelDisplaySeqState',       'draw_state_base',               None),
    (0x08042750, 0x0201bb90, 'gEquipChainSlotRefs',        'draw_equip_chain_refs',         None),
    (0x0804275c, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'draw_player_stride',            None),
    (0x08042758, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',       'draw_lp_block2_off',            None),
    (0x08042760, 0x000016ec, 'VICTORY_D_CID',              'draw_victory_d_cid',
     'VICTORY_D_CID=0x16ec: zone_ref==VICTORY_D_CID branch in tick_draw_card_display_seq step0'),
    (0x08042764, 0x00000fbe, 'SKULL_SERVANT_CID',          'draw_skull_servant_cid',
     'SKULL_SERVANT_CID=0x0fbe: card_id range check in tick_draw_card_display_seq'),
    (0x08042768, 0x00001388, 'EQUIP_SLOT_CARD_ID_RANGE_MAX', 'draw_equip_cid_range_max',    None),
    (0x0804274c, 0x0201e2a0, 'gDuelCardCtxBase',           'draw_card_ctx',                 None),
    (0x080427bc, 0x0201bb90, 'gEquipChainSlotRefs',        'draw_equip_chain_refs_b',       None),
    (0x080427c4, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'draw_player_stride_b',          None),
    (0x080428a0, 0x0201bcc0, 'gDuelDisplaySeqState',       'draw_state_base_b',             None),
    (0x080428a4, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',  'draw_seq_step_off_a',           None),
    (0x080428cc, 0x0201bcc0, 'gDuelDisplaySeqState',       'draw_state_base_c',             None),
    (0x080428d0, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',  'draw_seq_step_off_b',           None),
    (0x080428f4, 0x0201bcc0, 'gDuelDisplaySeqState',       'draw_state_base_d',             None),
    (0x08042868, 0x00000868, 'PLAYER_BLOCK_STRIDE',         'draw_player_stride_bb',         None),
    (0x0804286c, 0x0201e2a0, 'gDuelCardCtxBase',           'draw_card_ctx_b',               None),
    (0x08042920, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'draw_player_stride_c',          None),
    (0x080429c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'draw_player_stride_d',          None),
    (0x080429c4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',       'draw_lp_block2_off_b',          None),
    (0x080429c8, 0x0201e2a0, 'gDuelCardCtxBase',           'draw_card_ctx_d',               None),
    (0x080429cc, 0x0201bcc0, 'gDuelDisplaySeqState',       'draw_state_base_e',             None),
    (0x080429d0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'draw_step_lock_off',            None),
    # === invoke_draw_display_seq_forward (0x080429d4) ===
    # (no literal pool slots beyond what tick_draw_card_display_seq covers)
    # === invoke_draw_display_seq_reverse (0x080429e0) ===
    # (no literal pool slots beyond what tick_draw_card_display_seq covers)
    # === tick_display_op0d_with_lp_update_seq (0x080429ec) ===
    (0x08042a0c, 0x0201bcc0, 'gDuelDisplaySeqState',       'op0d_state_base',               None),
    (0x08042aa4, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'op0d_player_stride',            None),
    (0x08042aa8, 0x0201e2a0, 'gDuelCardCtxBase',           'op0d_card_ctx',                 None),
    (0x08042aac, 0x0201bcc0, 'gDuelDisplaySeqState',       'op0d_state_base_b',             None),
    (0x08042ab0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'op0d_step_lock_off',            None),
    (0x08042ad4, 0x0201bcc0, 'gDuelDisplaySeqState',       'op0d_state_base_c',             None),
    # === reset_equip_chain_entry_by_player (0x08042ab4) ===
    # (no additional literal pool beyond those already covered by op0d above)
    # === resolve_equip_target_slot_for_enqueue (0x08042b24) ===
    (0x08042b1c, 0x0201bcc0, 'gDuelDisplaySeqState',       'resolve_equip_state_base',      None),
    (0x08042b20, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',  'resolve_equip_step_lock_off',   None),
    (0x08042ba0, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'resolve_equip_player_stride',   None),
    (0x08042ba4, 0x0201c510, 'gDuelFieldSlots',            'resolve_equip_field_slots',     None),
    # === dispatch_equip_chain_slot_scan_by_player (0x08042bd0) ===
    (0x08042c0c, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride',            None),
    (0x08042c10, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots',              None),
    (0x08042c98, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride_b',          None),
    (0x08042c9c, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots_b',            None),
    (0x08042ca0, 0x000014ca, 'FRONTIER_WISEMAN_CID',       'scan_frontier_wiseman_cid',
     'FRONTIER_WISEMAN_CID=0x14ca: BST gate in dispatch_equip_chain_slot_scan_by_player'),
    (0x08042cf0, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride_c',          None),
    (0x08042cf4, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots_c',            None),
    (0x08042cf8, 0x000017c2, 'BLUE_EYES_SHINING_DRAGON_CID', 'scan_blue_eyes_shining_cid',
     'BLUE_EYES_SHINING_DRAGON_CID=0x17c2: enqueue_field_slot path gate'),
    (0x08042d48, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride_d',          None),
    (0x08042d4c, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots_d',            None),
    (0x08042d50, 0x000014da, 'FIEND_SKULL_DRAGON_CID',     'scan_fiend_skull_dragon_cid',
     'FIEND_SKULL_DRAGON_CID=0x14da: BST boundary in dispatch_equip_chain_slot_scan_by_player'),
    (0x08042e90, 0x000014ca, 'FRONTIER_WISEMAN_CID',       'scan_frontier_wiseman_cid_b',
     'FRONTIER_WISEMAN_CID=0x14ca: count_available_effect_zones arg'),
    (0x08042e94, 0x0000184b, 'RARE_METALMORPH_CID',        'scan_rare_metalmorph_cid',
     'RARE_METALMORPH_CID=0x184b: find_equip_slot arg in dispatch_equip_chain_slot_scan_by_player'),
    (0x08042e98, 0x0201d9c0, 'gEquipNodePool',             'scan_equip_node_pool',          None),
    (0x08042e9c, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride_e',          None),
    (0x08042ea0, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots_e',            None),
    (0x08042ea4, 0x0000ffff, 'SLOT_CARD_EMPTY',            'scan_slot_card_empty',
     'SLOT_CARD_EMPTY=0xffff: empty slot sentinel check'),
    (0x08042eac, 0x000014c7, 'RYU_SENSHI_CID',             'scan_ryu_senshi_cid',
     'RYU_SENSHI_CID=0x14c7: BST card_id gate (lower) in dispatch_equip_chain_slot_scan_by_player'),
    (0x08042ec0, 0x000014d5, 'TYRANT_DRAGON_CARD_ID',      'scan_tyrant_dragon_cid',
     'TYRANT_DRAGON_CARD_ID=0x14d5: equip eligibility check'),
    (0x08042ea8, 0x0201c520, 'gDuelFieldSlotState',        'scan_slot_state',               None),
    (0x08042f44, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride_f',          None),
    (0x08042f48, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots_f',            None),
    (0x0804301c, 0x00000868, 'PLAYER_BLOCK_STRIDE',        'scan_player_stride_g',          None),
    (0x08043020, 0x0201c510, 'gDuelFieldSlots',            'scan_field_slots_g',            None),
    (0x08043024, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',  'scan_chain_clr',
     'SCROLLBAR_CLEAR_BITS_14_6=0xffff803f: clear bits[14:6] of chain slot word'),
    (0x08043050, 0x0000184b, 'RARE_METALMORPH_CID',        'scan_rare_metalmorph_cid_b',
     'RARE_METALMORPH_CID=0x184b: final BST boundary in dispatch_equip_chain_slot_scan_by_player'),
    # === enqueue_sprite_attr_with_mode (0x08043054) ===
    (0x08043088, 0x00008036, 'OAM_SPRITE_PAL_P1',          'enqueue_oam_pal_p1',
     'OAM_SPRITE_PAL_P1=0x8036: OAM sprite palette selector for player 1 (bit15=1)'),
]

# Note: Some addresses appear in both tick_zone_equip_link_placement_seq and surrounding
# functions due to shared literal pool. The EQ list above is deduplicated by address;
# when the same address appears multiple times in the proposal, only one entry is kept.

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # PTR_gP1LifePoints slots (12 unique addresses in [0x417f0..0x4308c))
    (0x08041860, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08041860', None),
    (0x08041b34, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08041b34', None),
    (0x08041e2c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08041e2c', None),
    (0x08042280, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08042280', None),
    (0x080423f0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_080423f0', None),
    (0x08042754, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08042754', None),
    (0x080427c0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_080427c0', None),
    (0x08042864, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08042864', None),
    (0x0804291c, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_0804291c', None),
    (0x080429bc, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_080429bc', None),
    (0x08042aa0, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_08042aa0', None),
    (0x080425e4, 0x0201c4e0, 'gP1LifePoints', 'ptr_lp_080425e4', None),
    # DAT_08042ad8: gEquipChainSlotRefs base (0x0201bb90)
    (0x08042ad8, 0x0201bb90, 'gEquipChainSlotRefs', 'equip_chain_refs_08042ad8', None),
    # DAT_08041900: gEquipChainEntryBase (NEW global 0x0201e288)
    (0x08041900, 0x0201e288, 'gEquipChainEntryBase', 'equip_chain_entry_08041900',
     'gEquipChainEntryBase=0x0201e288: equip chain node depth array base'),
    # DAT_08042638: tick_draw_card_switch_table (ROM switch byte-offset table base 0x0804263c)
    (0x08042638, 0x0804263c, 'tick_draw_card_switch_table', 'draw_switch_table_ptr_08042638',
     'tick_draw_card_switch_table: inline switch table base for switchD_08042632 (not THUMB+1)'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    BLOCKED CID sentinels: not in card-stats.s, low confidence
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x080423e0, 'nsummon_cid_1672_080423e0',
     'cid sentinel 0x1672; not in card-stats.s; normal summon seq r10 range gate'),
    (0x08042780, 'draw_seq_cid_1729_08042780',
     'cid sentinel 0x1729; not in card-stats.s; draw card display step0 special path'),
    (0x08042794, 'draw_seq_cid_1986_08042794',
     'cid sentinel 0x1986; not in card-stats.s; draw card display step0 upper gate'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    9 functions with stale FUN_0803be4c -> dispatch_duel_event_display_seq
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # tick_equip_attach_display_sequence (0x0804186c)
    (0x0804186c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_op3e_seq (0x0804192c)
    (0x0804192c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_equip_zone_shuffle_display_seq (0x08041988)
    (0x08041988, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_op43_seq (0x08041b70)
    (0x08041b70, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_flip_reveal_display_seq (0x08041ef0)
    (0x08041ef0, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_normal_summon_zone_placement_seq (0x080422c4)
    (0x080422c4, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_equip_chain_count_check_sequence (0x08042470)
    (0x08042470, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_discard_display_seq (0x08042544)
    (0x08042544, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # reset_equip_chain_entry_by_player (0x08042ab4)
    (0x08042ab4, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
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

def _apply_eq(slot_addr, value, eq_name, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()

    if not _check(slot_addr, value, eq_name):
        print("[SKIP] EQ 0x%08x (%s) value mismatch" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
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

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (
            slot_addr, target_vaddr, gas_label, slot_label))
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

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (
        slot_addr, target_vaddr, gas_label, slot_label))

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

def _apply_plate_fix(func_addr, old_text, new_text):
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
        return

    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return

    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF04Seg4Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-4: 0x080417f0..0x0804308c, 19 fn, 159 slots")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1
    print("  PLATE done: %d" % plate_ok)

    print("\n=== RefineF04Seg4Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d (DRY=%s)" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES), DRY))

main()
