# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg6Slots.py -- F08 Seg-6 (0x080690dc..0x0806a118)
#   tick_dragon_summon_display_if_slots_paired cluster + equip sprite dispatch
#   EQ=82 + REF=3 + RENAME(covered by EQ/REF labels)=96 + CREATE_FUNC=1 + PLATE=1
#   DISASM=1 (THUMB fn @ 0x080696d8, 0x1c bytes = check_equip_eligible_set_slot8_flag_for_cid_12da)
#   FUNC_RENAME=0 / carve=0
#
# Review fixes applied (4 items):
#   #1: SCAPEGOAT/STRAY_LAMBS token-table addrs -> RENAME-only (no equate, Ruling A)
#   #2: DAT_08069778 -> LP_CARD_TRACK_BASE_OFF=0x1da8 (was LP_BANISHER_CTX_OFF, wrong value)
#   #3: DAT_08069f54/DWORD_0806a050 label prefix -> gduelcardctxbase_* (was gduelphaseflagss_*)
#   #4: ZONE_ENTRY_FLAGS_CLR_MASK -> oam_attr.inc (no equip_sprite.inc, Ruling B)
#
# NEW constants added to constants/ files (done before running this script):
#   card_info.inc:  WIDESPREAD_RUIN_CID=0x1254, BOTTOMLESS_SHIFTING_SAND_CID=0x1540
#                   HAMMER_SHOT_CID=0x17f2, cid_12da=0x12da
#   ewram.inc:      LP_ACTIVATION_LINK_FLAG_OFF=0x10d0 (domain gP1LifePoints)
#   oam_attr.inc:   OAM_SPRITE_CODE_P1_ACTIVATION=0x8019, ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_014310-pre-f08seg6

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    82 slots total (84 original minus 2 token-table addr equates per Ruling A).
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- CID constants (card_info.inc) ----
    (0x080690f8, 0x0000128b, 'LORD_OF_D_CID', 'lord_of_d_cid_080690f8',
     'LORD_OF_D_CID=0x128b: pw=17985575 card_0599'),
    (0x08069164, 0x000012cc, 'GRACEFUL_CHARITY_CID', 'graceful_charity_cid_08069164', None),
    (0x08069168, 0x0000187d, 'SPIRAL_SPEAR_STRIKE_CID', 'spiral_spear_strike_cid_08069168', None),
    (0x0806924c, 0x000012a1, 'PARASITE_PARACIDE_CID', 'parasite_paracide_cid_0806924c', None),
    (0x080694c4, 0x000012d2, 'SCAPEGOAT_CID', 'scapegoat_cid_080694c4', None),
    (0x080694c8, 0x00001710, 'STRAY_LAMBS_CID', 'stray_lambs_cid_080694c8', None),
    (0x08069a00, 0x00001254, 'WIDESPREAD_RUIN_CID', 'widespread_ruin_cid_08069a00',
     'WIDESPREAD_RUIN_CID=0x1254: pw=77754944'),
    (0x08069a18, 0x000017f2, 'HAMMER_SHOT_CID', 'hammer_shot_cid_08069a18',
     'HAMMER_SHOT_CID=0x17f2: pw=26412047'),
    (0x08069a24, 0x0000195e, 'CHTHONIAN_BLAST_CID', 'chthonian_blast_cid_08069a24', None),
    (0x08069a9c, 0x000017f2, 'HAMMER_SHOT_CID', 'hammer_shot_cid_08069a9c', None),
    (0x08069aa8, 0x0000195e, 'CHTHONIAN_BLAST_CID', 'chthonian_blast_cid_08069aa8', None),
    (0x08069c5c, 0x000012fb, 'cid_12fb', 'cid_12fb_08069c5c', None),
    (0x0806a07c, 0x000012f7, 'cid_12f7', 'cid_12f7_0806a07c', None),
    (0x0806a090, 0x0000131c, 'cid_131c', 'cid_131c_0806a090', None),
    (0x0806a094, 0x0000162a, 'JAR_ROBBER_CID', 'jar_robber_cid_0806a094', None),

    # ---- gDuelPhaseFlags = 0x0201b290 (12 in Seg-6 boundary; 1 more below as EQ-only) ----
    (0x080691b4, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_080691b4', None),
    (0x0806929c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806929c', None),
    (0x08069450, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069450', None),
    (0x08069508, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069508', None),
    (0x08069604, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069604', None),
    (0x0806972c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806972c', None),
    (0x080697a8, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_080697a8', None),
    (0x08069958, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069958', None),
    (0x080699b4, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_080699b4', None),
    (0x08069cfc, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069cfc', None),
    (0x08069d78, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069d78', None),
    (0x08069ee8, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_08069ee8', None),

    # ---- EQUIP_PHASE_FRAME_OFF = 0x4a4 (8 slots in Seg-6 boundary; 3 more below as EQ-only) ----
    (0x080691b8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_080691b8',
     'EQUIP_PHASE_FRAME_OFF=0x4a4'),
    (0x08069248, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_08069248', None),
    (0x08069560, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_08069560', None),
    (0x0806959c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806959c', None),
    (0x08069ab8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_08069ab8', None),
    (0x08069afc, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_08069afc', None),
    (0x08069b3c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_08069b3c', None),
    (0x08069b58, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_08069b58', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (10 in Seg-6 boundary; 2 more below as EQ-only) ----
    (0x080691c0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_080691c0', None),
    (0x08069244, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069244', None),
    (0x08069308, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069308', None),
    (0x080693b0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_080693b0', None),
    (0x08069810, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069810', None),
    (0x0806955c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806955c', None),
    (0x08069670, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069670', None),
    (0x08069d74, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069d74', None),
    (0x08069ee0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069ee0', None),
    (0x0806a04c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a04c', None),

    # ---- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (6 slots) ----
    (0x0806941c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_0806941c',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8'),
    (0x0806966c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_0806966c', None),
    (0x08069698, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_08069698', None),
    (0x080696c4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_080696c4', None),
    (0x08069734, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_08069734', None),
    (0x0806977c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_0806977c', None),

    # ---- EQUIP_ACTIVE_CTX_OFF = 0x484 (1 slot) ----
    (0x08069d00, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF', 'equip_active_ctx_off_08069d00',
     'EQUIP_ACTIVE_CTX_OFF=0x484'),

    # ---- LP_CARD_TRACK_BASE_OFF = 0x1da8 (1 slot; fix #2: was LP_BANISHER_CTX_OFF) ----
    (0x08069778, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_08069778',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card-ref tracking array base'),

    # ---- ELIGIB_SPRITE_CTRL_OFF = 0x1d68 / ELIGIB_ANIM_STATE_OFF = 0x1d6c (2 slots) ----
    (0x08069b34, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_off_08069b34',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68'),
    (0x08069b38, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_state_off_08069b38',
     'ELIGIB_ANIM_STATE_OFF=0x1d6c'),

    # ---- ELIGIB_SPRITE_CTRL_OFF = 0x1d68 (1 more slot in enqueue_slot_card_sprite_for_zone_entry) ----
    (0x08069df0, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_sprite_ctrl_off_08069df0', None),

    # ---- LP_BANISHER_CTX_OFF = 0x1d70 (1 slot in enqueue_slot_card_sprite_for_zone_entry) ----
    (0x08069df4, 0x00001d70, 'LP_BANISHER_CTX_OFF', 'lp_banisher_ctx_off_08069df4',
     'LP_BANISHER_CTX_OFF=0x1d70'),

    # ---- ELIGIB_STATE_CTRL_OFF = 0x1d54 (1 slot) ----
    (0x08069f78, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_ctrl_off_08069f78',
     'ELIGIB_STATE_CTRL_OFF=0x1d54'),

    # ---- ELIGIB_ACT_TYPE_OFF = 0x1d5c (1 slot) ----
    (0x08069fa8, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_act_type_off_08069fa8',
     'ELIGIB_ACT_TYPE_OFF=0x1d5c'),

    # ---- LP_ACTIVATION_LINK_FLAG_OFF = 0x10d0 NEW ewram.inc (1 slot) ----
    (0x08069960, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'lp_act_link_flag_off_08069960',
     'LP_ACTIVATION_LINK_FLAG_OFF=0x10d0: [gP1LifePoints+0x10d0] activation link flag'),

    # ---- gEquipChainEntryBase = 0x0201e288 (1 slot) ----
    (0x080694a4, 0x0201e288, 'gEquipChainEntryBase', 'gequipchainentrybase_080694a4', None),

    # ---- gP1FieldArrayCBase = 0x0201c600 (1 slot) ----
    (0x0806930c, 0x0201c600, 'gP1FieldArrayCBase', 'gp1fieldarraycbase_0806930c', None),

    # ---- gP1SlotSetCodeArray = 0x0201c740 (1 slot) ----
    (0x080693b4, 0x0201c740, 'gP1SlotSetCodeArray', 'gp1slotsetcodearray_080693b4', None),

    # ---- gP1ChainZoneArray = 0x0201c880 (1 slot) ----
    (0x080693b8, 0x0201c880, 'gP1ChainZoneArray', 'gp1chainzonearray_080693b8', None),

    # ---- gEquipLpZoneEntryBase = 0x0201e500 (1 slot) ----
    (0x0806982c, 0x0201e500, 'gEquipLpZoneEntryBase', 'gequiplpzoneentrybase_0806982c', None),

    # ---- gEquipChainSlotRefs = 0x0201bb90 (1 slot) ----
    (0x08069964, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainslotref_08069964', None),

    # ---- gDuelFieldSlots = 0x0201c510 (1 slot) ----
    (0x08069ee4, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_08069ee4', None),

    # ---- gP1HandSlotArray = 0x0201c8f8 (1 slot) ----
    (0x08069c64, 0x0201c8f8, 'gP1HandSlotArray', 'gp1handslotarray_08069c64', None),

    # ---- gDuelCardCtxBase = 0x0201e2a0 (2 in Seg-6 boundary; 1 more below as EQ-only) ----
    (0x08069f54, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_08069f54', None),
    (0x0806a050, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_0806a050', None),

    # ---- gEquipZoneRankState = 0x0201e4d0 (1 slot) ----
    (0x08069fc8, 0x0201e4d0, 'gEquipZoneRankState', 'gequipzonerankstate_08069fc8', None),

    # ---- OAM_SPRITE_CODE_P1_ACTIVATION = 0x8019 NEW oam_attr.inc (1 slot) ----
    (0x08069968, 0x00008019, 'OAM_SPRITE_CODE_P1_ACTIVATION', 'oam_sprite_code_p1_act_08069968',
     'OAM_SPRITE_CODE_P1_ACTIVATION=0x8019: P1 activation sprite code'),

    # ---- ZONE_ENTRY_FLAGS_CLR_MASK = 0x1fff NEW oam_attr.inc (1 slot; Ruling B) ----
    (0x080695a0, 0x00001fff, 'ZONE_ENTRY_FLAGS_CLR_MASK', 'zone_entry_flags_clr_mask_080695a0',
     'ZONE_ENTRY_FLAGS_CLR_MASK=0x1fff: clears zone entry sprite bits[12:0]'),

    # ---- gP1LifePoints = 0x0201c4e0 (already named PTR_gP1LifePoints_* for most) ----
    # These DWORD_* slots still need EQ to be renamed to gp1lifepoints_*
    (0x080691bc, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_080691bc', None),
    (0x08069240, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069240', None),
    (0x08069304, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069304', None),
    (0x080693ac, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_080693ac', None),
    (0x08069418, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069418', None),
    (0x08069558, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069558', None),
    (0x08069668, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069668', None),
    (0x08069694, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069694', None),
    (0x080696c0, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_080696c0', None),
    (0x08069b30, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_08069b30', None),
    (0x0806a048, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806a048', None),

    # ---- DWORD_08069c60 = 0x868 ----
    (0x08069c60, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_08069c60', None),

    # ---- EQ-only slots beyond Seg-6 boundary (0x0806a118) -- literal pool extends into Seg-7 ----
    # These are not in RENAME table but should still have equates (Seg-7 literal pool slots)
    (0x0806a150, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806a150', None),
    (0x0806a168, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806a168', None),
    (0x0806a1e4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806a1e4', None),
    (0x0806a1e8, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_0806a1e8', None),
    (0x0806a1f0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a1f0', None),
    (0x0806a230, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806a230', None),
    (0x0806a2dc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a2dc', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    3 slots: fn-ptr invoke_effect_node, fn-ptr check_zone_match_cb, switch table ptr
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DWORD_08069ae8 = invoke_effect_node_with_active_flag_3arg+1 (THUMB fn ptr)
    (0x08069ae8, 0x08090625, 'invoke_effect_node_with_active_flag_3arg+1',
     'fn_ptr_invoke_effect_node_08069ae8',
     'invoke_effect_node_with_active_flag_3arg+1 (THUMB+1=0x08090625); asm/11 L11824 func 0x08090624'),

    # DAT_08069d7c = check_zone_activation_ctx_match_cb+1 (THUMB fn ptr)
    (0x08069d7c, 0x08069cdd, 'check_zone_activation_ctx_match_cb+1',
     'fn_ptr_check_zone_match_cb_08069d7c',
     'check_zone_activation_ctx_match_cb+1 (THUMB+1=0x08069cdd); callback to init_zone_activation_display_fields'),

    # DAT_08069eec = switchD_08069edc table base ptr
    (0x08069eec, 0x08069ef0, 'switchD_08069edc__switchdataD_08069ef0',
     'switch_table_ptr_08069eec',
     'switch table ptr for switchD_08069edc (10 entries, 0x08069ef0..0x08069f14)'),
]

# ---------------------------------------------------------------------------
# C. RENAME_ONLY_SLOTS: (slot_addr, new_label, eol_ascii_or_None)
#    PTR_gP1LifePoints_* slots and the 2 token-table addr slots (Ruling A: no equate).
#    For PTR_ slots: gP1LifePoints already set as equate target; just rename slot label.
#    For token-table addr slots: raw .word, RENAME label + ASCII EOL only.
# ---------------------------------------------------------------------------
RENAME_ONLY_SLOTS = [
    # PTR_gP1LifePoints_* slots (value already 0x0201c4e0; just rename slot label)
    (0x08069730, 'gp1lifepoints_08069730', None),
    (0x08069774, 'gp1lifepoints_08069774', None),
    (0x0806980c, 'gp1lifepoints_0806980c', None),
    (0x0806995c, 'gp1lifepoints_0806995c', None),
    (0x08069d70, 'gp1lifepoints_08069d70', None),
    (0x08069f74, 'gp1lifepoints_08069f74', None),

    # Token-table addr slots (Ruling A: raw .word, RENAME label + EOL only, no equate)
    (0x080694d4, 'scapegoat_token_tbl_080694d4',
     'ROM ptr: Scapegoat OAM token slot-id table, 8 hwords @ 0x09e3f11c'),
    (0x08069504, 'stray_lambs_token_tbl_08069504',
     'ROM ptr: Stray Lambs OAM token slot-id table, 8 hwords @ 0x09e3f12c'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, func_name, new_plate_ascii)
#    Fix CJK mojibake + wrong card name at tick_dragon_summon_display_if_slots_paired
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    (0x080690dc,
     'tick_dragon_summon_display_if_slots_paired',
     'Drive dragon-summon display state machine after equip-chain paired-slot check. '
     'r0=card_entry_ptr, r1=scene_ptr. Loads fixed CID 0x128b (Lord of D.) and calls '
     'count_paired_slots_both_sides; if 0 paired slots returns 0. Else calls '
     'tick_dragon_summon_effect_display_state_machine(r4,r5) and returns result. '
     'fn-ptr dispatch (indeg=0).'),
]

# ---------------------------------------------------------------------------
# E. DISASM + CREATE_FUNC: check_equip_eligible_set_slot8_flag_for_cid_12da @ 0x080696d8
#    ROM_INCBIN 0x080696d8/0x1c (28 bytes = 14 THUMB halfwords)
#    THUMB+1 ref at 0x09e3fba8 (dispatch table entry CID=0x12da)
# ---------------------------------------------------------------------------
DISASM_STUBS = [
    (0x080696d8, 0x1c,
     'check_equip_eligible_set_slot8_flag_for_cid_12da',
     'fn_eligible handler for unassigned CID=0x12da; tests slot[+4] flags bit2, reads secondary '
     'field; sets bit0 of result field if slot eligible. Called from dispatch table at 0x09e3fba4. '
     'CID 0x12da absent from card-stats.s (gap 0x12D7=Tragedy..0x12DC=Ectoplasmer). indeg=0 '
     '(dispatch table only, THUMB+1 ref at 0x09e3fba8).'),
]

# ---------------------------------------------------------------------------
# F. CREATE_FUNC (inline unnamed callback, no disasm needed -- already disasm'd inline)
# ---------------------------------------------------------------------------
CREATE_FUNCS = [
    (0x08069cdc,
     'check_zone_activation_ctx_match_cb',
     'Inline callback between enqueue_equip_zone_sprites_for_spell_slot_entries and '
     'dispatch_zone_activation_display_by_confirm_state. r0=player_id, r1=zone_type. '
     'Loads [gDuelPhaseFlags+EQUIP_ACTIVE_CTX_OFF], checks active zone player_id; '
     'returns 0x800 if player mismatch AND zone_type==0xb, else 0. indeg=1 (fn-ptr DAT_08069d7c).'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- FAIL" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

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
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in EOL @ 0x%08x -- skipping EOL" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    return True


def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  target=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return

    existing_t = list(sym_tbl.getSymbols(a_target))
    tnames = [s.getName() for s in existing_t]
    if gas_label not in tnames:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    syms = list(sym_tbl.getSymbols(a_target))
    for s in syms:
        if s.getName() == gas_label:
            s.setPrimary()
            break

    existing_s = list(sym_tbl.getSymbols(a_slot))
    snames = [s.getName() for s in existing_s]
    if slot_label not in snames:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a_slot)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in REF EOL @ 0x%08x -- skipping" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_addr, gas_label, slot_label))


def _rename_only(slot_addr, new_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x  -> %s" % (slot_addr, new_label))
        return

    existing = list(sym_tbl.getSymbols(a))
    names = [s.getName() for s in existing]
    if new_label not in names:
        sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)

    # Make new label primary
    for s in list(sym_tbl.getSymbols(a)):
        if s.getName() == new_label:
            s.setPrimary()
            break

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in RENAME EOL @ 0x%08x -- skipping" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x  -> %s" % (slot_addr, new_label))


def _set_plate(func_addr, func_name, plate_text):
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x %s -- aborting" % (func_addr, func_name))
        return False

    a = _addr(func_addr)
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] PLATE @ 0x%08x %s (%d chars)" % (func_addr, func_name, len(plate_text)))
        return True

    cu = listing.getCodeUnitAt(a)
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLATE ok] %s @ 0x%08x (%d chars)" % (func_name, func_addr, len(plate_text)))
        return True
    else:
        print("[PLATE WARN] no code unit @ 0x%08x %s" % (func_addr, func_name))
        return False


def _disasm_thumb_and_create_func(start_addr, length, func_name, plate_text):
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[DISASM FAIL] non-ASCII in plate @ 0x%08x %s" % (start_addr, func_name))
        return

    a_start = _addr(start_addr)
    a_end = _addr(start_addr + length - 1)
    sym_tbl = currentProgram.getSymbolTable()
    fn_mgr = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] DISASM THUMB @ 0x%08x len=0x%x -> %s" % (start_addr, length, func_name))
        return

    # 1. Clear listing
    addr_set = AddressSet(a_start, a_end)
    listing.clearCodeUnits(a_start, a_end, False)

    # 2. Set THUMB mode
    ctx = currentProgram.getProgramContext()
    try:
        tmode_reg = ctx.getRegister("TMode")
        if tmode_reg is not None:
            ctx.setValue(tmode_reg, a_start, a_end, java.math.BigInteger.ONE)
            print("[DISASM] setTMode THUMB @ 0x%08x..0x%08x" % (start_addr, start_addr + length - 1))
    except Exception as e:
        print("[DISASM WARN] setTMode failed: %s" % e)

    # 3. Disassemble
    cmd = DisassembleCommand(a_start, addr_set, True)
    cmd.applyTo(currentProgram, monitor)
    print("[DISASM] DisassembleCommand @ 0x%08x len=0x%x" % (start_addr, length))

    # 4. Create function
    existing = fn_mgr.getFunctionAt(a_start)
    if existing is not None:
        if existing.getName() != func_name:
            existing.setName(func_name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing @ 0x%08x -> %s" % (start_addr, func_name))
        else:
            print("[FN ] already exists: %s" % func_name)
    else:
        cmd2 = CreateFunctionCmd(func_name, a_start, None, SourceType.USER_DEFINED)
        if cmd2.applyTo(currentProgram):
            print("[FN ] created %s @ 0x%08x" % (func_name, start_addr))
        else:
            print("[warn] createFunction failed: %s" % cmd2.getStatusMsg())
            existing_s = list(sym_tbl.getSymbols(a_start))
            snames = [s.getName() for s in existing_s]
            if func_name not in snames:
                sym_tbl.createLabel(a_start, func_name, SourceType.USER_DEFINED)
            print("[FN ] created label (fallback) %s" % func_name)

    # 5. Set plate
    cu = listing.getCodeUnitAt(a_start)
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLATE ok] %s (%d chars)" % (func_name, len(plate_text)))
    else:
        print("[PLATE WARN] no code unit after disasm @ 0x%08x" % start_addr)

    # 6. Ensure label is primary
    existing_s = list(sym_tbl.getSymbols(a_start))
    snames = [s.getName() for s in existing_s]
    if func_name not in snames:
        sym_tbl.createLabel(a_start, func_name, SourceType.USER_DEFINED)
    for s in list(sym_tbl.getSymbols(a_start)):
        if s.getName() == func_name:
            s.setPrimary()
            break
    print("[DISASM] done: %s @ 0x%08x" % (func_name, start_addr))


def _create_func(func_addr, func_name, plate_text):
    """Create a function (already disasm'd) and set plate."""
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[CREATE_FUNC FAIL] non-ASCII in plate @ 0x%08x %s" % (func_addr, func_name))
        return

    a = _addr(func_addr)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] CREATE_FUNC @ 0x%08x %s" % (func_addr, func_name))
        return

    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != func_name:
            existing.setName(func_name, SourceType.USER_DEFINED)
        print("[FN ] existing renamed to %s @ 0x%08x" % (func_name, func_addr))
    else:
        cmd = CreateFunctionCmd(func_name, a, None, SourceType.USER_DEFINED)
        if cmd.applyTo(currentProgram):
            print("[FN ] created %s @ 0x%08x" % (func_name, func_addr))
        else:
            print("[warn] createFunction failed @ 0x%08x: %s" % (func_addr, cmd.getStatusMsg()))
            existing_s = list(sym_tbl.getSymbols(a))
            snames = [s.getName() for s in existing_s]
            if func_name not in snames:
                sym_tbl.createLabel(a, func_name, SourceType.USER_DEFINED)

    cu = listing.getCodeUnitAt(a)
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLATE ok] %s (%d chars)" % (func_name, len(plate_text)))
    for s in list(sym_tbl.getSymbols(a)):
        if s.getName() == func_name:
            s.setPrimary()
            break


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg6Slots (DRY=%s) ===" % DRY)
    print("  Seg-6: 0x080690dc..0x0806a118")
    print("  EQ=%d  REF=%d  RENAME_ONLY=%d  PLATE=%d  DISASM=%d  CREATE_FUNC=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_ONLY_SLOTS),
        len(PLATE_REWRITES), len(DISASM_STUBS), len(CREATE_FUNCS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        mem = currentProgram.getMemory()
        a = _addr(slot_addr)
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
            if actual != (value & 0xFFFFFFFF):
                eq_fail += 1
                print("[FAIL] 0x%08x (%s): rom=0x%08x expect=0x%08x" % (
                    slot_addr, eq_name, actual, value & 0xFFFFFFFF))
                continue
        except Exception as e:
            eq_fail += 1
            print("[FAIL] 0x%08x (%s): read error %s" % (slot_addr, eq_name, e))
            continue
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES -- abort and investigate !!!" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_ONLY
    print("\n--- C. RENAME_ONLY (%d) ---" % len(RENAME_ONLY_SLOTS))
    ren_ok = 0
    for entry in RENAME_ONLY_SLOTS:
        slot_addr, new_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _rename_only(slot_addr, new_label, eol)
        ren_ok += 1
    print("  RENAME_ONLY done: %d" % ren_ok)

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for func_addr, func_name, plate_text in PLATE_REWRITES:
        if _set_plate(func_addr, func_name, plate_text):
            plate_ok += 1
    print("  PLATE done: %d" % plate_ok)

    # E. DISASM_STUBS
    print("\n--- E. DISASM_STUBS (%d) ---" % len(DISASM_STUBS))
    for start_addr, length, func_name, plate_text in DISASM_STUBS:
        _disasm_thumb_and_create_func(start_addr, length, func_name, plate_text)

    # F. CREATE_FUNCS (inline callbacks already in disasm'd region)
    print("\n--- F. CREATE_FUNCS (%d) ---" % len(CREATE_FUNCS))
    for func_addr, func_name, plate_text in CREATE_FUNCS:
        _create_func(func_addr, func_name, plate_text)

    print("\n=== RefineF08Seg6Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  RENAME_ONLY=%d  PLATE=%d  DISASM=%d  CREATE_FUNC=%d" % (
        eq_ok, len(EQ_SLOTS), ref_ok, ren_ok, plate_ok, len(DISASM_STUBS), len(CREATE_FUNCS)))


main()
