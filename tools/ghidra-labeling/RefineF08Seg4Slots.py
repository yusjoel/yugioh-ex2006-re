# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg4Slots.py -- F08 Seg-4 (0x08067160..0x08067fa4)
#   dispatch_effect_zone_lp_sprites_by_slot_flags cluster + check_activation_ctx_zone11_match_cb
#   EQ=73 slots (13 gDuelPhaseFlags + 8 gDuelFieldSlots + 14 PLAYER_BLOCK_STRIDE + ...)
#   REF=1 (fn-ptr DAT_08067270 -> check_activation_ctx_zone11_match_cb+1)
#   CREATE_FUNC=1 (check_activation_ctx_zone11_match_cb @ 0x080671bc + plate)
#   PLATE=1 (new function plate)
#   FUNC_RENAME=0 / PLATE_REWRITES=0 (no stale FUN_ in existing plates)
#   carve=0 / disasm=0 (pure function body segment, 0 ROM_INCBIN/switchD)
#
# NEW constants added to constants/card_info.inc (done separately, before running this script):
#   SOUL_ABSORBING_BONE_TOWER_CID = 0x1744
#   MALICE_ASCENDANT_CID          = 0x19d0
#   CARD_FIELD3_THRESHOLD_1499    = 0x5db
#   CARD_FIELD3_THRESHOLD_1500    = 0x5dc
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260617_225226-pre-F08Seg4

from ghidra.app.cmd.function import CreateFunctionCmd
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
#    Creates equate (value->name) and references it from slot address.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- gDuelPhaseFlags = 0x0201b290 (13 slots) ----
    (0x080671dc, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_dispatch_effect_zone_80671dc', None),
    (0x08067228, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_dispatch_act_08067228', None),
    (0x080672cc, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_dispatch_oam_080672cc', None),
    (0x0806763c, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_banisher_0806763c', None),
    (0x0806776c, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_chain_ban_0806776c', None),
    (0x08067a14, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_act_eligib_08067a14', None),
    (0x08067a9c, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_act_08067a9c', None),
    (0x08067ba4, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_neodaed_08067ba4', None),
    (0x08067c40, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_head_07c40', None),
    (0x08067d60, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_head_07d60', None),
    (0x08067e40, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_head_07e40', None),
    (0x08067e58, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_tick_head_07e58', None),
    (0x08067ef8, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_dispatch_f6_07ef8', None),

    # ---- gDuelCardCtxBase = 0x0201e2a0 (1 slot) ----
    (0x08067224, 0x0201e2a0, 'gDuelCardCtxBase',
     'gDuelCardCtxBase_dispatch_act_80067224', None),

    # ---- gDuelFieldSlots = 0x0201c510 (8 slots) ----
    (0x080674b4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_invoke_slot_ind_074b4', None),
    (0x08067580, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_emit_bitmap_08067580', None),
    (0x0806789c, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_enq_chain_link_0806789c', None),
    (0x080679d4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_enq_dual_080679d4', None),
    (0x08067a98, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_tick_act_08067a98', None),
    (0x08067b38, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_tick_act_08067b38', None),
    (0x08067ca4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_tick_head_07ca4', None),
    (0x08067ef4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_dispatch_f6_07ef4', None),

    # ---- gP1SlotSetCodeArray = 0x0201c740 (1 slot) ----
    (0x08067bf8, 0x0201c740, 'gP1SlotSetCodeArray',
     'gP1SlotSetCodeArray_tick_neodaed_08067bf8', None),

    # ---- gP1LifePoints = 0x0201c4e0 (2 DWORD_ slots; PTR_gP1LifePoints_* already named) ----
    (0x08067de4, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_tick_head_07de4', None),
    (0x08067e98, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_tick_head_07e98', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (14 slots) ----
    (0x08067250, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_dispatch_act_08067250', None),
    (0x080672fc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_dispatch_oam_080672fc', None),
    (0x080674b0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_invoke_slot_ind_074b0', None),
    (0x0806757c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_emit_bitmap_0806757c', None),
    (0x08067670, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_banisher_08067670', None),
    (0x080676a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_banisher_080676a4', None),
    (0x08067898, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_enq_chain_link_08067898', None),
    (0x080679d0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_enq_dual_080679d0', None),
    (0x08067a94, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_act_08067a94', None),
    (0x08067b34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_act_08067b34', None),
    (0x08067bf4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_neodaed_08067bf4', None),
    (0x08067ca0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_head_07ca0', None),
    (0x08067de8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_tick_head_07de8', None),
    (0x08067ef0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_dispatch_f6_07ef0', None),

    # ---- EQUIP_PHASE_FRAME_OFF = 0x4a4 (6 slots) ----
    (0x08067a90, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_tick_act_08067a90',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08067b30, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_tick_act_08067b30',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08067d64, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_tick_head_07d64',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08067de0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_tick_head_07de0',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08067e44, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_tick_head_07e44',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08067e5c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_tick_head_07e5c',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),

    # ---- EQUIP_ACTIVE_CTX_OFF = 0x484 (1 slot) ----
    (0x080671e0, 0x00000484, 'EQUIP_ACTIVE_CTX_OFF',
     'equip_active_ctx_off_dispatch_effect_zone_80671e0',
     'EQUIP_ACTIVE_CTX_OFF=0x484: [gDuelPhaseFlags+0x484] equip active ctx slot ptr'),

    # ---- LP_BANISHER_CTX_OFF = 0x1d70 (1 slot) ----
    (0x08067298, 0x00001d70, 'LP_BANISHER_CTX_OFF',
     'lp_banisher_ctx_off_dispatch_act_08067298',
     'LP_BANISHER_CTX_OFF=0x1d70: [gP1LifePoints+0x1d70] face-down slot list ctx ptr'),

    # ---- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (2 slots) ----
    (0x0806758c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_block2_off_emit_bitmap_0806758c',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8: LP display block2 offset in gP1LifePoints'),
    (0x08067e9c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_block2_off_tick_head_07e9c',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8: LP display block2 offset in gP1LifePoints'),

    # ---- FIELD_STATE_OFF = 0x1cf4 (1 slot) ----
    (0x08067590, 0x00001cf4, 'FIELD_STATE_OFF',
     'field_state_off_emit_bitmap_08067590',
     'FIELD_STATE_OFF=0x1cf4: [gP1LifePoints+0x1cf4] activation phase state'),

    # ---- CHAIN_LINK_COUNTER_OFF = 0x1cbc (1 slot) ----
    (0x080678a0, 0x00001cbc, 'CHAIN_LINK_COUNTER_OFF',
     'chain_link_ctr_off_enq_chain_link_080678a0',
     'CHAIN_LINK_COUNTER_OFF=0x1cbc: [gP1LifePoints+0x1cbc] chain link counter'),

    # ---- DUEL_ACTIVE_PLAYER_OFF = 0x1cb8 (1 slot) ----
    (0x080678a4, 0x00001cb8, 'DUEL_ACTIVE_PLAYER_OFF',
     'duel_active_player_off_enq_chain_link_080678a4',
     'DUEL_ACTIVE_PLAYER_OFF=0x1cb8: [gP1LifePoints+0x1cb8] active turn player id'),

    # ---- LP_COST_3000 = 0xbb8 (2 slots) ----
    (0x08067188, 0x00000bb8, 'LP_COST_3000',
     'lp_cost_3000_dispatch_07188',
     'LP_COST_3000=0xbb8: r1 arg to submit_effect_zone_lp_and_shape_sprites (3000 LP amount)'),
    (0x080671b4, 0x00000bb8, 'LP_COST_3000',
     'lp_cost_3000_dispatch_071b4',
     'LP_COST_3000=0xbb8: r1 arg to submit_effect_zone_lp_and_shape_sprites (3000 LP amount)'),

    # ---- LP_COST_5000 = 0x1388 (1 slot) ----
    (0x080671b8, 0x00001388, 'LP_COST_5000',
     'lp_cost_5000_dispatch_071b8',
     'LP_COST_5000=0x1388: r1 arg to enqueue_sprite_attr_record_with_cap (5000 LP cap param)'),

    # ---- SWORDS_OF_REVEALING_LIGHT_CID = 0x1102 (1 slot) ----
    (0x08067584, 0x00001102, 'SWORDS_OF_REVEALING_LIGHT_CID',
     'swords_cid_emit_bitmap_08067584',
     'SWORDS_OF_REVEALING_LIGHT_CID=0x1102: Swords filter in emit_equip_zone_bitmap_sprite_type11'),

    # ---- CRUSH_CARD_CID = 0x123b (3 slots) ----
    (0x08067ca8, 0x0000123b, 'CRUSH_CARD_CID',
     'crush_card_cid_tick_head_07ca8', None),
    (0x08067d08, 0x0000123b, 'CRUSH_CARD_CID',
     'crush_card_cid_tick_head_07d08', None),
    (0x08067dec, 0x0000123b, 'CRUSH_CARD_CID',
     'crush_card_cid_tick_head_07dec', None),

    # ---- DECK_DEVASTATION_VIRUS_CID = 0x188c (3 slots) ----
    (0x08067cac, 0x0000188c, 'DECK_DEVASTATION_VIRUS_CID',
     'ddv_cid_tick_head_07cac', None),
    (0x08067d0c, 0x0000188c, 'DECK_DEVASTATION_VIRUS_CID',
     'ddv_cid_tick_head_07d0c', None),
    (0x08067df0, 0x0000188c, 'DECK_DEVASTATION_VIRUS_CID',
     'ddv_cid_tick_head_07df0', None),

    # ---- MAGICAL_LABYRINTH_CID = 0x1232 (1 slot) ----
    (0x08067b9c, 0x00001232, 'MAGICAL_LABYRINTH_CID',
     'magical_labyrinth_cid_08067b9c', None),

    # ---- WALL_SHADOW_CID = 0x1117 (1 slot) ----
    (0x08067ba0, 0x00001117, 'WALL_SHADOW_CID',
     'wall_shadow_cid_08067ba0', None),

    # ---- NEEDLE_WORM_CID = 0x11d8 (1 slot) ----
    (0x08067400, 0x000011d8, 'NEEDLE_WORM_CID',
     'needle_worm_cid_07400', None),

    # ---- SOUL_ABSORBING_BONE_TOWER_CID = 0x1744 (1 slot) -- NEW card_info.inc ----
    (0x080673fc, 0x00001744, 'SOUL_ABSORBING_BONE_TOWER_CID',
     'soul_absorbing_bone_tower_cid_073fc',
     'SOUL_ABSORBING_BONE_TOWER_CID=0x1744: pw=63012333; deck-count=2 in enqueue_equip_zone_sprite_with_deck_count'),

    # ---- MALICE_ASCENDANT_CID = 0x19d0 (1 slot) -- NEW card_info.inc ----
    (0x0806740c, 0x000019d0, 'MALICE_ASCENDANT_CID',
     'malice_ascendant_cid_0740c',
     'MALICE_ASCENDANT_CID=0x19d0: pw=14255590; count_extra_deck_cards_by_id path in enqueue_equip_zone_sprite_with_deck_count'),

    # ---- CARD_FIELD3_THRESHOLD_1499 = 0x5db (3 slots) -- NEW card_info.inc ----
    # field3=ATK targeting threshold; Crush Card Virus: field3>1499 -> target (ATK>=1500 monster)
    # domain-distinct from FIELD5_SCORE_THRESHOLD_1499 (field5 score gate) -- new constant
    (0x08067cc0, 0x000005db, 'CARD_FIELD3_THRESHOLD_1499',
     'field3_threshold_1499_07cc0',
     'CARD_FIELD3_THRESHOLD_1499=0x5db: Crush Card ATK>1499 targeting gate; field3(ATK) domain'),
    (0x08067d20, 0x000005db, 'CARD_FIELD3_THRESHOLD_1499',
     'field3_threshold_1499_07d20',
     'CARD_FIELD3_THRESHOLD_1499=0x5db: Crush Card ATK>1499 targeting gate; field3(ATK) domain'),
    (0x08067e04, 0x000005db, 'CARD_FIELD3_THRESHOLD_1499',
     'field3_threshold_1499_07e04',
     'CARD_FIELD3_THRESHOLD_1499=0x5db: Crush Card ATK>1499 targeting gate; field3(ATK) domain'),

    # ---- CARD_FIELD3_THRESHOLD_1500 = 0x5dc (3 slots) -- NEW card_info.inc ----
    # Deck Devastation Virus: field3_raw<=1500 -> target (ATK<=1500 monster)
    # domain-distinct from CARD_STAT_LP_THRESHOLD_1500/LP_COST_1500 -- new constant
    (0x08067ce4, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500',
     'field3_threshold_1500_07ce4',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc: DDV ATK<=1500 targeting gate; field3(ATK) domain'),
    (0x08067d5c, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500',
     'field3_threshold_1500_07d5c',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc: DDV ATK<=1500 targeting gate; field3(ATK) domain'),
    (0x08067e3c, 0x000005dc, 'CARD_FIELD3_THRESHOLD_1500',
     'field3_threshold_1500_07e3c',
     'CARD_FIELD3_THRESHOLD_1500=0x5dc: DDV ATK<=1500 targeting gate; field3(ATK) domain'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    Adds a DATA reference from slot_addr to target_addr; sets labels on both.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DAT_08067270 = fn-ptr 0x080671bd = check_activation_ctx_zone11_match_cb+1 (THUMB+1)
    (0x08067270, 0x080671bd, 'check_activation_ctx_zone11_match_cb+1',
     'cb_check_zone11_match_08067270',
     'fn-ptr: check_activation_ctx_zone11_match_cb+1 (THUMB+1=0x080671bd); '
     'callback arg to init_zone_activation_display_fields; 1 THUMB+1 ref raw=0'),
]

# ---------------------------------------------------------------------------
# C. CREATE_FUNC: (func_addr, func_name, plate_text_ascii)
#    Creates a new function label + sets plate comment. text must be pure ASCII.
# ---------------------------------------------------------------------------
CREATE_FUNCS = [
    (0x080671bc,
     'check_activation_ctx_zone11_match_cb',
     'Callback: given (r0=player_id, r1=zone_idx), checks if gDuelPhaseFlags[EQUIP_ACTIVE_CTX_OFF] '
     'slot player_id matches r0 AND r1==0xb (chain zone 11). '
     'Returns 0x800 on match, 0 on mismatch. '
     'Called via fn-ptr stored at DAT_08067270. '
     'Params: r0=player_id, r1=zone_idx. Returns: r0=u32 (0x800 or 0). '
     'indeg=0 (fn-ptr only: 1 THUMB+1 ref, raw=0).'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- WARN treated as FAIL" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

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

    # EOL comment (ASCII only)
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
    """Add DATA reference from slot_addr to target_addr; set labels on both."""
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  target=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return

    # Label on target
    existing_t = list(sym_tbl.getSymbols(a_target))
    tnames = [s.getName() for s in existing_t]
    if gas_label not in tnames:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    # DATA reference slot -> target
    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    # Set primary for target label
    syms = list(sym_tbl.getSymbols(a_target))
    for s in syms:
        if s.getName() == gas_label:
            s.setPrimary()
            break

    # Slot label
    existing_s = list(sym_tbl.getSymbols(a_slot))
    snames = [s.getName() for s in existing_s]
    if slot_label not in snames:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # EOL on slot
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a_slot)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in REF EOL @ 0x%08x -- skipping" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_addr, gas_label, slot_label))


def _create_function_with_plate(func_addr, func_name, plate_text):
    """Create a function label and set plate comment. plate_text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x %s -- skipping" % (func_addr, func_name))
        return

    a = _addr(func_addr)
    sym_tbl = currentProgram.getSymbolTable()
    fn_mgr = currentProgram.getFunctionManager()

    if DRY:
        print("[dry] CREATE_FUNC %s @ 0x%08x (plate %d chars)" % (
            func_name, func_addr, len(plate_text)))
        return

    # Create or rename function
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != func_name:
            existing.setName(func_name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing @ 0x%08x -> %s" % (func_addr, func_name))
        else:
            print("[FN ] already exists: %s @ 0x%08x" % (func_name, func_addr))
    else:
        cmd = CreateFunctionCmd(func_name, a, None, SourceType.USER_DEFINED)
        if cmd.applyTo(currentProgram):
            print("[FN ] created %s @ 0x%08x" % (func_name, func_addr))
        else:
            print("[warn] createFunction failed @ 0x%08x: %s" % (func_addr, cmd.getStatusMsg()))
            # Fallback: create label
            existing_s = list(sym_tbl.getSymbols(a))
            snames = [s.getName() for s in existing_s]
            if func_name not in snames:
                sym_tbl.createLabel(a, func_name, SourceType.USER_DEFINED)
            print("[FN ] created label (fallback) %s @ 0x%08x" % (func_name, func_addr))

    # Set plate comment
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLATE ok] %s @ 0x%08x (%d chars)" % (func_name, func_addr, len(plate_text)))
    else:
        print("[PLATE FAIL] no code unit @ 0x%08x" % func_addr)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg4Slots (DRY=%s) ===" % DRY)
    print("  Seg-4: 0x08067160..0x08067fa4")
    print("  EQ=%d  REF=%d  CREATE_FUNC=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(CREATE_FUNCS)))

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
        print("  !!! %d EQ FAILURES -- check values before real run !!!" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. CREATE_FUNCS
    print("\n--- C. CREATE_FUNCS (%d) ---" % len(CREATE_FUNCS))
    for func_addr, func_name, plate_text in CREATE_FUNCS:
        _create_function_with_plate(func_addr, func_name, plate_text)
    print("  CREATE_FUNC done: %d" % len(CREATE_FUNCS))

    print("\n=== RefineF08Seg4Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  CREATE_FUNC=%d" % (
        eq_ok, len(EQ_SLOTS), ref_ok, len(CREATE_FUNCS)))


main()
