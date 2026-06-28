# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg5Slots.py -- file 12 Seg-5 [0x08097828, 0x080984d0)
#   asm/12_equip_activation_scan.s slot symbolization + plate fixes.
#   5 function entries (all named), 0 ROM_INCBIN blocks.
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (115 slots including Fix#1 DAT_080979bc)
#   B. REF_SLOTS  -- 6 slots (2 switchD ptr + 4 THUMB fn-ptr)
#   C. RENAME_SLOTS -- 31 PTR_gP1LifePoints_* -> gp1lp_ptr_*
#   D. PLATE_FULL   -- 5 full plate rewrites (pure ASCII, <=500 chars)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK -- Jython UTF-8 mojibake risk).
# No ROM_INCBIN, no carve, no disasm in Seg-5.
#
# New constants (add to .inc files BEFORE running real mode):
#   oam_attr.inc:
#     OAM_EQUIP_SPRITE_P2_15     = 0x00008015
#   card_info.inc:
#     JIRAI_GUMO_CID             = 0x00001115
#     PATRICIAN_OF_DARKNESS_CID  = 0x0000139c

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
import ghidra.program.model.data as DataTypes

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return toAddr(v)

def _check(slot, expected):
    """Verify ROM 4-byte LE value at slot matches expected; return False if mismatch."""
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(_addr(slot)) & 0xFFFFFFFF
        if actual != (expected & 0xFFFFFFFF):
            print("VALUE_MISMATCH @ 0x{:08x}: expected=0x{:08x} got=0x{:08x}".format(
                slot, expected & 0xFFFFFFFF, actual))
            return False
        return True
    except Exception as e:
        print("READ_ERROR @ 0x{:08x}: {}".format(slot, e))
        return False

fails = []
applied = 0

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # ---- Group A: EQUIP_CHAIN_ACTIVE_OFF (duel_field.inc, 0x00001d2c) -- 43 slots ----
    (0x0809785c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_785c'),
    (0x080978a4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_78a4'),
    (0x0809792c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_792c'),
    (0x08097a50, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7a50'),
    (0x08097a80, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7a80'),
    (0x08097ab8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7ab8'),
    (0x08097ae4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7ae4'),
    (0x08097b08, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7b08'),
    (0x08097b34, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7b34'),
    (0x08097b64, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7b64'),
    (0x08097b80, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7b80'),
    (0x08097bac, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7bac'),
    (0x08097be4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7be4'),
    (0x08097c64, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7c64'),
    (0x08097d04, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7d04'),
    (0x08097d28, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7d28'),
    (0x08097d4c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7d4c'),
    (0x08097d88, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7d88'),
    (0x08097da8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7da8'),
    (0x08097e1c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7e1c'),
    (0x08097e30, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7e30'),
    (0x08097e60, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7e60'),
    (0x08097ea8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7ea8'),
    (0x08097ed4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7ed4'),
    (0x08097ee8, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7ee8'),
    (0x08097f10, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7f10'),
    (0x08097f28, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7f28'),
    (0x08097f3c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7f3c'),
    (0x08097f58, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7f58'),
    (0x08097fa4, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7fa4'),
    (0x08097fdc, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_7fdc'),
    (0x08098050, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_98050'),
    (0x0809810c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_9810c'),
    (0x08098158, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_98158'),
    (0x0809816c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_9816c'),
    (0x080981fc, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_981fc'),
    (0x08098218, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_98218'),
    (0x0809828c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_9828c'),
    (0x08098398, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_98398'),
    (0x080983d0, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_983d0'),
    (0x0809841c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_9841c'),
    (0x0809846c, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_9846c'),
    # Fix#1: DAT_080979bc -- missing from original, ASM L7635 caseD_2 fail-path
    (0x080979bc, 0x00001d2c, 'EQUIP_CHAIN_ACTIVE_OFF', 'eqchain_act_79bc'),

    # ---- Group B: EQUIP_CHAIN_STEP_OFF (duel_field.inc, 0x00001d28) -- 9 slots ----
    (0x08097928, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7928'),
    (0x080979b8, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_79b8'),
    (0x08097ab4, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7ab4'),
    (0x08097ae0, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7ae0'),
    (0x08097b30, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7b30'),
    (0x08097ba8, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7ba8'),
    (0x08097be0, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7be0'),
    (0x08097da4, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_7da4'),
    (0x080982e4, 0x00001d28, 'EQUIP_CHAIN_STEP_OFF', 'eqchain_step_982e4'),

    # ---- Group C: EQUIP_CHAIN_CANCEL_OFF (duel_field.inc, 0x00001d30) -- 5 slots ----
    (0x080979c0, 0x00001d30, 'EQUIP_CHAIN_CANCEL_OFF', 'eqchain_cancel_79c0'),
    (0x08097abc, 0x00001d30, 'EQUIP_CHAIN_CANCEL_OFF', 'eqchain_cancel_7abc'),
    (0x08097ae8, 0x00001d30, 'EQUIP_CHAIN_CANCEL_OFF', 'eqchain_cancel_7ae8'),
    (0x08097bb0, 0x00001d30, 'EQUIP_CHAIN_CANCEL_OFF', 'eqchain_cancel_7bb0'),
    (0x08097be8, 0x00001d30, 'EQUIP_CHAIN_CANCEL_OFF', 'eqchain_cancel_7be8'),

    # ---- Group D: gEquipChainSlotRefs (ewram.inc, 0x0201bb90) -- 14 slots ----
    (0x08097854, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97854'),
    (0x08097904, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97904'),
    (0x08097994, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97994'),
    (0x08097c1c, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97c1c'),
    (0x08097c5c, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97c5c'),
    (0x08097e14, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97e14'),
    (0x08097e58, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_97e58'),
    (0x08098008, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_98008'),
    (0x08098044, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_98044'),
    (0x080980e8, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_980e8'),
    (0x080981ac, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_981ac'),
    (0x08098258, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_98258'),
    (0x080982dc, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_982dc'),
    (0x0809849c, 0x0201bb90, 'gEquipChainSlotRefs', 'geqchain_9849c'),

    # ---- Group E: gEquipLpScoreBase (ewram.inc, 0x0201afe0) -- 2 slots ----
    (0x08097998, 0x0201afe0, 'gEquipLpScoreBase', 'geqlp_score_7998'),
    (0x08098048, 0x0201afe0, 'gEquipLpScoreBase', 'geqlp_score_98048'),

    # ---- Group F: gDuelCardCtxBase (ewram.inc, 0x0201e2a0) -- 6 slots ----
    (0x0809796c, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_796c'),
    (0x08097ce4, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_7ce4'),
    (0x08097f08, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_7f08'),
    (0x08098004, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_98004'),
    (0x080983b4, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_983b4'),
    (0x080983f8, 0x0201e2a0, 'gDuelCardCtxBase', 'gduecardctx_983f8'),

    # ---- Group G: ELIGIB_STATE_CTRL_OFF (ewram.inc, 0x00001d54) -- 3 slots ----
    (0x08097a30, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_7a30'),
    (0x08098140, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_98140'),
    (0x08098450, 0x00001d54, 'ELIGIB_STATE_CTRL_OFF', 'eligib_state_98450'),

    # ---- Group H: ELIGIB_ACT_TYPE_OFF (ewram.inc, 0x00001d5c) -- 4 slots ----
    (0x08097a34, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_acttype_7a34'),
    (0x08097a98, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_acttype_7a98'),
    (0x08098144, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_acttype_98144'),
    (0x08098454, 0x00001d5c, 'ELIGIB_ACT_TYPE_OFF', 'eligib_acttype_98454'),

    # ---- Group I: ELIGIB_ACT_COUNT_OFF (ewram.inc, 0x00001d58) -- 2 slots ----
    (0x08097974, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_actcnt_7974'),
    (0x08097a4c, 0x00001d58, 'ELIGIB_ACT_COUNT_OFF', 'eligib_actcnt_7a4c'),

    # ---- Group J: ELIGIB_ANIM_STATE_OFF (ewram.inc, 0x00001d6c) -- 1 slot ----
    (0x08098148, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF', 'eligib_anim_98148'),

    # ---- Group K: ELIGIB_SPRITE_CTRL_OFF (ewram.inc, 0x00001d68) -- 1 slot ----
    (0x08098458, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF', 'eligib_spr_ctrl_98458'),

    # ---- Group L: LP_CARD_TRACK_BASE_OFF (ewram.inc, 0x00001da8) -- 2 slots ----
    (0x080981dc, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_981dc'),
    (0x08098214, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_98214'),

    # ---- Group M: LP_CARD_TRACK_NEXT_OFF (ewram.inc, 0x00001daa) -- 1 slot ----
    (0x080984c8, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_nxt_984c8'),

    # ---- Group N: PLAYER_BLOCK_STRIDE (ewram.inc, 0x00000868) -- 2 slots ----
    (0x0809834c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_9834c'),
    (0x080984cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_stride_984cc'),

    # ---- Group O: OAM sprite attr constants ----
    # NEW: OAM_EQUIP_SPRITE_P2_15 (oam_attr.inc, 0x00008015)
    (0x0809789c, 0x00008015, 'OAM_EQUIP_SPRITE_P2_15', 'oam_p2_15_789c'),
    # REUSE: OAM_SPRITE_CODE_P1_ACTIVATION (oam_attr.inc, 0x00008019)
    (0x08098078, 0x00008019, 'OAM_SPRITE_CODE_P1_ACTIVATION', 'oam_p1_act_98078'),
    # REUSE: OAM_EQUIP_SPRITE_P2_1A (oam_attr.inc, 0x0000801a)
    (0x080981b0, 0x0000801a, 'OAM_EQUIP_SPRITE_P2_1A', 'oam_p2_1a_981b0'),
    # REUSE: OAM_SPRITE_CODE_P1_ACTIVATION (oam_attr.inc, 0x00008019)
    (0x080981c8, 0x00008019, 'OAM_SPRITE_CODE_P1_ACTIVATION', 'oam_p1_act_981c8'),
    # REUSE: OAM_EQUIP_SPRITE_TILE_P2_1B (oam_attr.inc, 0x0000801b)
    (0x080982e0, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'oam_p2_1b_982e0'),

    # ---- Group P: Card ID constants ----
    # REUSE: eval_gap_cid_11ed (card_info.inc, 0x000011ed)
    (0x08097a7c, 0x000011ed, 'eval_gap_cid_11ed', 'cid_11ed_7a7c'),
    (0x08097bb4, 0x000011ed, 'eval_gap_cid_11ed', 'cid_11ed_7bb4'),
    # REUSE: LAST_TURN_CID (card_info.inc, 0x0000151e)
    (0x08097d80, 0x0000151e, 'LAST_TURN_CID', 'last_turn_7d80'),
    # REUSE: RING_OF_MAGNETISM_CID (card_info.inc, 0x00001318)
    (0x08097de8, 0x00001318, 'RING_OF_MAGNETISM_CID', 'ring_of_mag_7de8'),
    (0x08097e10, 0x00001318, 'RING_OF_MAGNETISM_CID', 'ring_of_mag_7e10'),
    # NEW: PATRICIAN_OF_DARKNESS_CID (card_info.inc, 0x0000139c)
    (0x08097ea0, 0x0000139c, 'PATRICIAN_OF_DARKNESS_CID', 'patrician_7ea0'),
    # REUSE: EARTHBOUND_INVITATION_CID (card_info.inc, 0x0000177a)
    (0x08097ecc, 0x0000177a, 'EARTHBOUND_INVITATION_CID', 'earthbound_inv_7ecc'),
    # NEW: PATRICIAN_OF_DARKNESS_CID (card_info.inc, 0x0000139c)
    (0x08097fa8, 0x0000139c, 'PATRICIAN_OF_DARKNESS_CID', 'patrician_7fa8'),
    # REUSE: EARTHBOUND_INVITATION_CID (card_info.inc, 0x0000177a)
    (0x08097fd4, 0x0000177a, 'EARTHBOUND_INVITATION_CID', 'earthbound_inv_7fd4'),
    # REUSE: EARTHBOUND_INVITATION_CID (card_info.inc, 0x0000177a)
    (0x080981a8, 0x0000177a, 'EARTHBOUND_INVITATION_CID', 'earthbound_inv_981a8'),
    # NEW: PATRICIAN_OF_DARKNESS_CID (card_info.inc, 0x0000139c)
    (0x080981f8, 0x0000139c, 'PATRICIAN_OF_DARKNESS_CID', 'patrician_981f8'),
    # REUSE: TOON_SUMMONED_SKULL_CID (card_info.inc, 0x0000127f)
    (0x08098350, 0x0000127f, 'TOON_SUMMONED_SKULL_CID', 'toon_skull_98350'),
    # NEW: JIRAI_GUMO_CID (card_info.inc, 0x00001115)
    (0x08098354, 0x00001115, 'JIRAI_GUMO_CID', 'jirai_gumo_98354'),
    # REUSE: BLUE_EYES_TOON_DRAGON_CID (card_info.inc, 0x000012a5)
    (0x08098380, 0x000012a5, 'BLUE_EYES_TOON_DRAGON_CID', 'blue_eyes_toon_98380'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: switchD ptr slots + THUMB fn-ptr slots
# (target_label, target_addr, slot_addr, slot_label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # REF-1: PTR_switchdataD_ slots (2 slots)
    # Fix#2: slot labels all lowercase
    ('switchD_08097850__switchdataD_08097864', 0x08097864, 0x08097860, 'switchdata_ptr_97860'),
    ('switchD_08097c58__switchdataD_08097c6c', 0x08097c6c, 0x08097c68, 'switchdata_ptr_97c68'),
    # REF-2: THUMB fn-ptr slots (4 slots)
    ('check_equip_target_slot_eligibility', 0x08097bec, 0x080980ec, 'eq_tgt_elig_fn_980ec'),
    ('check_equip_target_slot_eligibility', 0x08097bec, 0x08098104, 'eq_tgt_elig_fn_98104'),
    ('check_slot_equippable_excluding_self', 0x0809822c, 0x080983fc, 'slot_eq_excl_fn_983fc'),
    ('check_slot_equippable_excluding_self', 0x0809822c, 0x08098414, 'slot_eq_excl_fn_98414'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: PTR_gP1LifePoints_* -> gp1lp_ptr_*
# (slot_addr, new_label)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08097858, 'gp1lp_ptr_97858'),
    (0x080978a0, 'gp1lp_ptr_978a0'),
    (0x08097924, 'gp1lp_ptr_97924'),
    (0x08097970, 'gp1lp_ptr_97970'),
    (0x080979b4, 'gp1lp_ptr_979b4'),
    (0x08097b04, 'gp1lp_ptr_97b04'),
    (0x08097b60, 'gp1lp_ptr_97b60'),
    (0x08097c60, 'gp1lp_ptr_97c60'),
    (0x08097cbc, 'gp1lp_ptr_97cbc'),
    (0x08097ce8, 'gp1lp_ptr_97ce8'),
    (0x08097d00, 'gp1lp_ptr_97d00'),
    (0x08097d48, 'gp1lp_ptr_97d48'),
    (0x08097d84, 'gp1lp_ptr_97d84'),
    (0x08097da0, 'gp1lp_ptr_97da0'),
    (0x08097e18, 'gp1lp_ptr_97e18'),
    (0x08097e2c, 'gp1lp_ptr_97e2c'),
    (0x08097e5c, 'gp1lp_ptr_97e5c'),
    (0x08097ea4, 'gp1lp_ptr_97ea4'),
    (0x08097ed0, 'gp1lp_ptr_97ed0'),
    (0x08097ee4, 'gp1lp_ptr_97ee4'),
    (0x08097f0c, 'gp1lp_ptr_97f0c'),
    (0x08097f24, 'gp1lp_ptr_97f24'),
    (0x08097f38, 'gp1lp_ptr_97f38'),
    (0x08097fac, 'gp1lp_ptr_97fac'),
    (0x08097fd8, 'gp1lp_ptr_97fd8'),
    (0x0809804c, 'gp1lp_ptr_9804c'),
    (0x08098108, 'gp1lp_ptr_98108'),
    (0x08098288, 'gp1lp_ptr_98288'),
    (0x08098394, 'gp1lp_ptr_98394'),
    (0x080983cc, 'gp1lp_ptr_983cc'),
    (0x08098418, 'gp1lp_ptr_98418'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: (fn_addr, plate_text)
# All text pure ASCII, <= 500 chars
# ---------------------------------------------------------------------------
PLATE_FULL = [
    (0x08097828,
     "Equip activation substate driver: r0=player_side -> r5; [gEquipChainSlotRefs+0]=player_side. Reads [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF] -> 5-way jump. case_0: enqueue OAM(0x15/OAM_EQUIP_SPRITE_P2_15), inc phase; case_1: phase_counter==6+slot_search+eval_slot_activation_eligibility_full; case_2: chain-blocked check+eval_equip_monster_zone_score; case_3: slot_guard/toon_scan/display_op; case_4: step 4/5 -> write STEP/ACTIVE/CANCEL fields. Returns 1=stepped, 0=noop."),
    (0x08097bec,
     "Checks if slot (r1+r2) can receive equip from card at r0. Returns 0 if: same active player as r0, or combined_slot>4, or eval_slot_activation_eligibility_full returns 0. Returns 0x800 (bit11) if eligible. gEquipChainSlotRefs+0=active_player; +0x1c=context_slot. Called via fn-ptr by dispatch_equip_slot_display_state_by_phase and tick_activation_display_state_machine. MAX_SLOT=4, ELIGIBLE_FLAG=0x800."),
    (0x08097c2c,
     "Equip slot display state machine: r0=player_side -> r6. Writes (1-r6) to [gEquipChainSlotRefs+4]; reads [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF] -> 12-case switch (0..0xb); >0xb -> caseD_6. Cases: 0=chain-blocked/field-score/display; 1=find_equip_slot/field_spell_chain; 2=slot-display count; 3=multi-slot scan; 4=display row; 5=sprite enqueue; a/b=card_track read. Driven by advance_equip_display_phase_via_table."),
    (0x0809822c,
     "Checks if slot (r1+r2) can be equipped by card, excluding self-targeting. Returns 0 if combined_slot>4, card not equippable via check_slot_card_can_be_equipped, or same-player+same-slot as gEquipChainSlotRefs record. Returns 0x800 (bit11) if equippable. Called via fn-ptr by dispatch_equip_slot_display_state_by_phase case_5/case_6. gEquipChainSlotRefs base=0x0201bb90, MAX_SLOT=4, ELIGIBLE_FLAG=0x800."),
    (0x08098264,
     "Single-tick activation display state machine. r0=slot_display_ctx -> r4; reads [gP1LifePoints+EQUIP_CHAIN_ACTIVE_OFF]. State 0: check_slot_card_activatable; if no: enqueue OAM(OAM_EQUIP_SPRITE_TILE_P2_1B/0x1b), set [+EQUIP_CHAIN_STEP_OFF]=1; if yes: fill_slot_activation_state_array+[base+0xc]=1+card_id range check (JIRAI_GUMO/TOON range). State 0x64/0x65/0x66: refresh paths. State 0xc8/0xc9: completion. Driven by advance_equip_display_phase_via_table."),
]

# ============================================================================
# EXECUTION
# ============================================================================
symTbl = currentProgram.getSymbolTable()
refMgr = currentProgram.getReferenceManager()
listing = currentProgram.getListing()
eqTbl = currentProgram.getEquateTable()

print("=== RefineF12Seg5Slots {} ===".format("DRY-RUN" if DRY else "REAL"))

# ---------------------------------------------------------------------------
# Section A: EQ_SLOTS
# ---------------------------------------------------------------------------
print("\n--- Section A: EQ_SLOTS ({} entries) ---".format(len(EQ_SLOTS)))
for (slot, val, eq_name, slot_label) in EQ_SLOTS:
    if not _check(slot, val):
        fails.append('EQ_FAIL @ 0x{:08x} ({})'.format(slot, eq_name))
        continue
    if DRY:
        print("  DRY EQ 0x{:08x} {} -> {}".format(slot, eq_name, slot_label))
        applied += 1
        continue
    try:
        # Create or get equate
        eq = eqTbl.getEquate(eq_name)
        if eq is None:
            eq = eqTbl.createEquate(eq_name, val)
        eq.addReference(_addr(slot), 0)
        # Create slot label
        existing = symTbl.getGlobalSymbol(slot_label, _addr(slot))
        if existing is None:
            symTbl.createLabel(_addr(slot), slot_label, SourceType.USER_DEFINED)
        print("  EQ OK 0x{:08x} {} -> {}".format(slot, eq_name, slot_label))
        applied += 1
    except Exception as e:
        fails.append('EQ_ERR @ 0x{:08x} {}: {}'.format(slot, eq_name, e))

# ---------------------------------------------------------------------------
# Section B: REF_SLOTS
# ---------------------------------------------------------------------------
print("\n--- Section B: REF_SLOTS ({} entries) ---".format(len(REF_SLOTS)))
for (target_label, target_addr, slot_addr, slot_label) in REF_SLOTS:
    if not _check(slot_addr, target_addr):
        # For THUMB fn-ptr slots the stored value is target_addr | 1
        thumb_val = target_addr | 1
        if not _check(slot_addr, thumb_val):
            fails.append('REF_FAIL @ 0x{:08x} ({})'.format(slot_addr, target_label))
            continue
        target_val = thumb_val
    else:
        target_val = target_addr
    if DRY:
        print("  DRY REF 0x{:08x} -> {} ({})".format(slot_addr, target_label, slot_label))
        applied += 1
        continue
    try:
        # Create label at target (may already exist)
        t_addr = _addr(target_addr)
        existing_tgt = symTbl.getGlobalSymbol(target_label, t_addr)
        if existing_tgt is None:
            symTbl.createLabel(t_addr, target_label, SourceType.USER_DEFINED)
        # Add DATA reference from slot to target
        refMgr.addMemoryReference(_addr(slot_addr), t_addr, RefType.DATA,
                                   SourceType.USER_DEFINED, 0)
        # Set primary
        refs = list(refMgr.getReferencesFrom(_addr(slot_addr)))
        for r in refs:
            if r.getToAddress().equals(t_addr):
                refMgr.setPrimary(r, True)
                break
        # Create slot label
        existing_sl = symTbl.getGlobalSymbol(slot_label, _addr(slot_addr))
        if existing_sl is None:
            symTbl.createLabel(_addr(slot_addr), slot_label, SourceType.USER_DEFINED)
        print("  REF OK 0x{:08x} -> {} ({})".format(slot_addr, target_label, slot_label))
        applied += 1
    except Exception as e:
        fails.append('REF_ERR @ 0x{:08x} {}: {}'.format(slot_addr, target_label, e))

# ---------------------------------------------------------------------------
# Section C: RENAME_SLOTS
# ---------------------------------------------------------------------------
print("\n--- Section C: RENAME_SLOTS ({} entries) ---".format(len(RENAME_SLOTS)))
for (slot_addr, new_label) in RENAME_SLOTS:
    if DRY:
        print("  DRY RENAME 0x{:08x} -> {}".format(slot_addr, new_label))
        applied += 1
        continue
    try:
        a = _addr(slot_addr)
        # Remove old PTR_ prefixed symbols
        old_syms = list(symTbl.getSymbols(a))
        for s in old_syms:
            if s.getName().startswith('PTR_'):
                s.delete()
        # Create new label
        existing = symTbl.getGlobalSymbol(new_label, a)
        if existing is None:
            symTbl.createLabel(a, new_label, SourceType.USER_DEFINED)
        print("  RENAME OK 0x{:08x} -> {}".format(slot_addr, new_label))
        applied += 1
    except Exception as e:
        fails.append('RENAME_ERR @ 0x{:08x} {}: {}'.format(slot_addr, new_label, e))

# ---------------------------------------------------------------------------
# Section D: PLATE_FULL
# ---------------------------------------------------------------------------
print("\n--- Section D: PLATE_FULL ({} entries) ---".format(len(PLATE_FULL)))
for (fn_addr, plate_text) in PLATE_FULL:
    # ASCII check
    non_ascii = [c for c in plate_text if ord(c) > 127]
    if non_ascii:
        fails.append('PLATE_ASCII_FAIL @ 0x{:08x}: non-ASCII chars found'.format(fn_addr))
        continue
    if len(plate_text) > 500:
        fails.append('PLATE_LEN_FAIL @ 0x{:08x}: {} chars > 500'.format(fn_addr, len(plate_text)))
        continue
    if DRY:
        print("  DRY PLATE 0x{:08x} ({} chars)".format(fn_addr, len(plate_text)))
        applied += 1
        continue
    try:
        cu = listing.getCodeUnitAt(_addr(fn_addr))
        if cu is None:
            fails.append('PLATE_ERR @ 0x{:08x}: no code unit'.format(fn_addr))
            continue
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("  PLATE OK 0x{:08x} ({} chars)".format(fn_addr, len(plate_text)))
        applied += 1
    except Exception as e:
        fails.append('PLATE_ERR @ 0x{:08x}: {}'.format(fn_addr, e))

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n=== SUMMARY ===")
print("Applied: {}".format(applied))
print("Fails:   {}".format(len(fails)))
for f in fails:
    print("  FAIL: " + f)
if fails:
    print("STATUS: FAIL ({} errors)".format(len(fails)))
else:
    print("STATUS: OK")
