# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg9aSlots.py -- p5 file09 Seg-9a (0x0807738c..0x08077c50)
#   invoke_setup_equip_oam_if_neo_daedalus_zone_f / dispatch_equip_lp_bar_display_by_state
#   / route_equip_partner_setup_by_lp_state / submit_equip_bitmap_and_lp_indicator_by_slot
#   / render_equip_pair_zone_sprites_by_card_match / refresh_equip_bitmap_if_zone_flag_clear
#   / dispatch_equip_slot_eligible_count_by_lp_state / check_equip_activation_by_special_card_id
#   / check_equip_target_by_chain_then_bitmap
#   (9 named functions; B1..B5 are ROM_INCBIN handled by DisassembleF09Seg9aBlocks.py)
#
# Sections:
#   A. EQ_SLOTS   -- 26 slots: all REUSE (except NEW: LEGENDARY_JUJITSU_MASTER_CID + KANGAROO_CHAMP_CID
#                    already added to card_info.inc before running this script)
#   B. REF_SLOTS  -- 5 slots (dispatch table ptrs + sub-stub block starts)
#   C. RENAME_SLOTS -- 0 slots
#   D. PLATE_REWRITES -- 0 updates
#
# New constants added to constants/card_info.inc BEFORE this script:
#   JADE_INSECT_WHISTLE_CID     = 0x00001717  (fn_eligible B4-embedded)
#   LEGENDARY_JUJITSU_MASTER_CID = 0x00001749 (check_equip_activation zone13)
#   KANGAROO_CHAMP_CID          = 0x00001866  (check_equip_activation activation)
#   (PRICKLE_FAIRY_CID=0x1703 and SPATIAL_COLLAPSE_CARD_ID=0x16df already exist -- REUSE)
#   (DIMENSION_FUSION_CID=0x1712 already exists -- REUSE)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0; disasm handled by DisassembleF09Seg9aBlocks.py
# NOTE: PLATE=0 (no stale FUN_ or CJK found in Seg-9a lines 19213..20094)

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
#    26 slots -- all REUSE from ewram.inc / card_info.inc
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # =========================================================================
    # invoke_setup_equip_oam_if_neo_daedalus_zone_f (0x0807738c)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x0807740c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_740c',
     'PLAYER_BLOCK_STRIDE: byte stride per player data block'),

    # --- ewram.inc: gP1AltHandSlotArray = 0x0201cab0 ---
    (0x08077410, 0x0201cab0, 'gP1AltHandSlotArray',
     'gP1AltHandSlotArray_pool_7410',
     'gP1AltHandSlotArray: P1 alt hand slot array base (EWRAM)'),

    # =========================================================================
    # dispatch_equip_lp_bar_display_by_state (0x08077414)
    # =========================================================================

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 ---
    (0x0807744c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_block2_off_pool_744c',
     'P1LP_BLOCK2_OFF_1CE8: P1 LP block-2 base offset (gP1LifePoints+0x1ce8)'),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08077450, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_7450',
     'gDuelPhaseFlags: duel phase flags global'),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x08077454, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_7454',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter offset'),

    # =========================================================================
    # route_equip_partner_setup_by_lp_state (0x080774f4)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080774ac, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_74ac', None),

    # =========================================================================
    # submit_equip_bitmap_and_lp_indicator_by_slot (0x08077538)
    # =========================================================================

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08077524, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_7524', None),

    # --- card_info.inc: CARD_STAT_LP_THRESHOLD = 0x00000bb8 ---
    (0x08077578, 0x00000bb8, 'CARD_STAT_LP_THRESHOLD',
     'lp_threshold_pool_7578',
     'CARD_STAT_LP_THRESHOLD: 3000 LP threshold for card stat display branch'),

    # =========================================================================
    # render_equip_pair_zone_sprites_by_card_match (0x08077678)
    # =========================================================================

    # --- ewram.inc: gEquipZoneCountTable = 0x0201e1c8 ---
    (0x080777a0, 0x0201e1c8, 'gEquipZoneCountTable',
     'gEquipZoneCountTable_pool_77a0',
     'gEquipZoneCountTable: equip zone count table base (EWRAM)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080777a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_77a4', None),

    # --- ewram.inc: gP1ZoneHandCount = 0x0201c4ec ---
    (0x080777a8, 0x0201c4ec, 'gP1ZoneHandCount',
     'gP1ZoneHandCount_pool_77a8',
     'gP1ZoneHandCount: P1 zone hand count base (EWRAM)'),

    # --- ewram.inc: gP1FieldArrayCBase = 0x0201c600 ---
    (0x080777ac, 0x0201c600, 'gP1FieldArrayCBase',
     'gP1FieldArrayCBase_pool_77ac',
     'gP1FieldArrayCBase: P1 field array C base (EWRAM)'),

    # =========================================================================
    # refresh_equip_bitmap_if_zone_flag_clear (0x080777d8)
    # =========================================================================

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x080777f8, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_77f8', None),

    # =========================================================================
    # dispatch_equip_slot_eligible_count_by_lp_state (0x080777d8)
    # =========================================================================

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x08077848, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_7848', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x0807788c, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_788c',
     'gP1LifePoints: P1 LP tracking block base (EWRAM)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08077890, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_7890', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x08077894, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_7894', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080778e0, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_78e0', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080778e4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_78e4', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x080778e8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_78e8', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x0807791c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_791c', None),

    # =========================================================================
    # check_equip_activation_by_special_card_id (0x08077920)
    # =========================================================================

    # --- card_info.inc: PRICKLE_FAIRY_CID = 0x00001703 (REUSE) ---
    (0x0807794c, 0x00001703, 'PRICKLE_FAIRY_CID',
     'prickle_fairy_cid_pool_794c',
     'PRICKLE_FAIRY_CID: zone11 test path in check_equip_activation_by_special_card_id'),

    # --- card_info.inc: LEGENDARY_JUJITSU_MASTER_CID = 0x00001749 (NEW -> now in card_info.inc) ---
    (0x08077960, 0x00001749, 'LEGENDARY_JUJITSU_MASTER_CID',
     'legendary_jujitsu_master_cid_pool_7960',
     'LEGENDARY_JUJITSU_MASTER_CID: zone13 test path (pw=25773409; slot=0x1749)'),

    # --- card_info.inc: KANGAROO_CHAMP_CID = 0x00001866 (NEW -> now in card_info.inc) ---
    (0x08077964, 0x00001866, 'KANGAROO_CHAMP_CID',
     'kangaroo_champ_cid_pool_7964',
     'KANGAROO_CHAMP_CID: activation check path (pw=95789089; slot=0x1866)'),

    # =========================================================================
    # check_equip_target_by_chain_then_bitmap (0x080779bc)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080779b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_79b4', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x080779b8, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_79b8',
     'gDuelFieldSlots: duel field zone slot array base (EWRAM)'),

]  # end EQ_SLOTS

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    5 slots -- dispatch table ptrs + sub-stub block starts
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # PTR_DAT_080775ac -> spatial_collapse_dispatch_table_75ac
    # .word 0x08077648 = entry[0] of 9-entry raw-ptr dispatch table
    # referenced by fn_eligible_spatial_collapse literal pool
    (0x080775ac, 0x08077648, 'spatial_collapse_dispatch_table_75ac',
     'spatial_collapse_dispatch_table_75ac',
     '.word 0x08077648; 9-entry raw-ptr dispatch table base; fn_eligible_spatial_collapse pool ptr'),

    # DAT_080775d0 -> spatial_collapse_dispatch_sub_stubs_75d0
    # B2 sub-stubs block start; entry[8] of PTR_DAT_080775ac = 0x080775d0
    (0x080775d0, 0x080775d0, 'spatial_collapse_dispatch_sub_stubs_75d0',
     'spatial_collapse_dispatch_sub_stubs_75d0',
     'B2 sub-stubs block start; entry[8] of 9-entry dispatch table @0x080775ac'),

    # PTR_DAT_08077a18 -> jade_insect_dispatch_table_7a18
    # .word 0x08077b00 = entry[0] of 9-entry raw-ptr dispatch table
    # referenced by fn_eligible_jade_insect_whistle literal pool
    (0x08077a18, 0x08077b00, 'jade_insect_dispatch_table_7a18',
     'jade_insect_dispatch_table_7a18',
     '.word 0x08077b00; 9-entry raw-ptr dispatch table base; fn_eligible_jade_insect_whistle pool ptr'),

    # DAT_08077a3c -> jade_insect_dispatch_sub_stubs_7a3c
    # B4 sub-stubs block start; entry[8] of PTR_DAT_08077a18 = 0x08077a3c
    (0x08077a3c, 0x08077a3c, 'jade_insect_dispatch_sub_stubs_7a3c',
     'jade_insect_dispatch_sub_stubs_7a3c',
     'B4 sub-stubs block start; entry[8] of 9-entry dispatch table @0x08077a18'),

    # DAT_08077b88 -> dimension_fusion_dispatch_sub_stubs_7b88
    # B5 sub-stubs block start; last entry of B4-trailing dispatch table @0x08077b84 = 0x08077b88
    (0x08077b88, 0x08077b88, 'dimension_fusion_dispatch_sub_stubs_7b88',
     'dimension_fusion_dispatch_sub_stubs_7b88',
     'B5 sub-stubs block start; dispatch table @0x08077b5c entry[10]=0x08077b88'),

]  # end REF_SLOTS

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: 0 slots
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: 0 updates
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

def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    a_slot   = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl  = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  gas=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return

    # create USER label at target
    tgt_syms = sym_tbl.getSymbols(a_target)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    # add DATA reference slot -> target
    refMgr = currentProgram.getReferenceManager()
    refMgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)

    # set primary on target
    for sym in sym_tbl.getSymbols(a_target):
        if sym.getName() == gas_label:
            sym.setPrimary()
            break

    # USER label at slot (rename)
    slot_syms = sym_tbl.getSymbols(a_slot)
    slot_names = [s.getName() for s in slot_syms]
    if slot_label not in slot_names:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a_slot)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s" % (slot_addr, target_addr, slot_label))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF09Seg9aSlots (DRY=%s) ===" % DRY)
    print("  EQ=%d  REF=%d  RENAME=%d" % (len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS ---")
    for (sa, val, eq_name, slot_label, eol) in EQ_SLOTS:
        _apply_eq(sa, val, eq_name, slot_label, eol)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS ---")
    for (sa, ta, gas_label, slot_label, eol) in REF_SLOTS:
        _apply_ref(sa, ta, gas_label, slot_label, eol)

    # C. RENAME_SLOTS (none)
    print("\n--- C. RENAME_SLOTS (0 slots) ---")

    # D. PLATE_REWRITES (none)
    print("\n--- D. PLATE_REWRITES (0 updates) ---")

    print("\n=== RefineF09Seg9aSlots DONE ===")
    print("  EQ_SLOTS applied: %d" % len(EQ_SLOTS))
    print("  REF_SLOTS applied: %d" % len(REF_SLOTS))

main()
