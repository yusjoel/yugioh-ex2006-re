# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg9bSlots.py -- p5 file09 Seg-9b (0x08077c50..0x0807850c)
#   dispatch_equip_lp_row_with_neo_daedalus_gate
#   / enqueue_position_sprites_for_both_players
#   / submit_lp_indicator_by_slot_type_and_score
#   / enqueue_equip_zone_sprite_by_state_and_equip_count
#   / dispatch_equip_zone_sprite_by_lp_state_with_ticker
#   / enqueue_equip_type11_sprite_and_lp_bar_if_signature_match
#   / refresh_equip_slot_bitmap_from_zone_struct
#   / invoke_equip_zone_bitmap_pair_if_spell_card_type
#   / enumerate_equip_slots_for_sprite_bitmap_pair
#   / scan_both_players_slots_for_equip_activation
#   (10 named functions; B6..B9 are ROM_INCBIN handled by DisassembleF09Seg9bBlocks.py)
#
# Sections:
#   A. EQ_SLOTS   -- 33 slots (all REUSE from ewram.inc / card_info.inc)
#   B. REF_SLOTS  -- 3 slots (dispatch table ptr + 2 sub-stub block starts)
#   C. RENAME_SLOTS -- 0 slots
#   D. PLATE_REWRITES -- 0 updates
#
# New constants added to constants/card_info.inc BEFORE this script:
#   DANGEROUS_MACHINE_TYPE6_CID = 0x00001738  (fn_eligible B6)
#   MONSTER_GATE_CID            = 0x0000175c  (fn_eligible B8)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0; disasm handled by DisassembleF09Seg9bBlocks.py
# NOTE: PLATE=0 (no stale FUN_ or CJK found in Seg-9b range)

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
#    33 slots -- all REUSE from ewram.inc / card_info.inc
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # =========================================================================
    # dispatch_equip_lp_row_with_neo_daedalus_gate (0x08077c50)
    # =========================================================================

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08077cb4, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_7cb4',
     'gDuelPhaseFlags: duel phase flags global (EWRAM)'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08077cb8, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_7cb8',
     'gP1LifePoints: P1 LP tracking block base (EWRAM)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08077cbc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_7cbc',
     'PLAYER_BLOCK_STRIDE: byte stride per player data block'),

    # =========================================================================
    # enqueue_position_sprites_for_both_players (0x08077d58)
    # =========================================================================

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08077d2c, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_7d2c', None),

    # --- ewram.inc: LP_CARD_TRACK_BASE_OFF = 0x00001da8 ---
    (0x08077d30, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_pool_7d30',
     'LP_CARD_TRACK_BASE_OFF: LP card track base offset (gP1LifePoints+0x1da8)'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08077d34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_7d34', None),

    # =========================================================================
    # submit_lp_indicator_by_slot_type_and_score (0x08077d80)
    # =========================================================================

    # --- ewram.inc: gEquipChainSlotRefs = 0x0201bb90 ---
    (0x08077dc8, 0x0201bb90, 'gEquipChainSlotRefs',
     'gequip_chain_refs_pool_7dc8',
     'gEquipChainSlotRefs: equip chain slot reference struct base (EWRAM)'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08077dfc, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_7dfc', None),

    # =========================================================================
    # enqueue_equip_zone_sprite_by_state_and_equip_count (0x08077e00)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08077e90, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_7e90', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08077e94, 0x0201c510, 'gDuelFieldSlots',
     'gduel_field_slots_pool_7e94',
     'gDuelFieldSlots: duel field zone slot array base (EWRAM)'),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08077e98, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_7e98', None),

    # --- duel_field.inc: ACTIVATION_STATE_B_OFF = 0x00001d78 ---
    (0x08077ec8, 0x00001d78, 'ACTIVATION_STATE_B_OFF',
     'activation_state_b_pool_7ec8',
     'ACTIVATION_STATE_B_OFF: activation state-B field offset in LP block'),

    # =========================================================================
    # dispatch_equip_zone_sprite_by_lp_state_with_ticker (0x08078004)
    # =========================================================================

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 ---
    (0x08078020, 0x0201b290, 'gDuelPhaseFlags',
     'gduel_phase_pool_8020', None),

    # --- ewram.inc: gDuelCardCtxBase = 0x0201e2a0 ---
    (0x08078050, 0x0201e2a0, 'gDuelCardCtxBase',
     'gduel_card_ctx_pool_8050',
     'gDuelCardCtxBase: duel card context base (EWRAM)'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08078054, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8054', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x0807808c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_808c',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter offset'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08078090, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_8090', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 ---
    (0x080780d0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_pool_80d0', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080780d4, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_pool_80d4', None),

    # --- ewram.inc: LP_CARD_TRACK_BASE_OFF = 0x00001da8 ---
    (0x080780d8, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_pool_80d8', None),

    # =========================================================================
    # enqueue_equip_type11_sprite_and_lp_bar_if_signature_match (0x080780f0)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08078144, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8144', None),

    # --- ewram.inc: gDuelFieldSlots_p2_base = 0x0201c5d8 ---
    (0x08078148, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'gduel_slots_p2_base_pool_8148',
     'gDuelFieldSlots_p2_base: P2 duel field slot array base (EWRAM)'),

    # --- card_info.inc: SANCTUARY_CID_SHIFTED = 0xbaf00000 ---
    (0x0807814c, 0xbaf00000, 'SANCTUARY_CID_SHIFTED',
     'sanctuary_cid_shifted_pool_814c',
     'SANCTUARY_CID_SHIFTED: SANCTUARY_IN_THE_SKY_CID<<19 sentinel for CID comparison'),

    # =========================================================================
    # refresh_equip_slot_bitmap_from_zone_struct (0x08078158)
    # =========================================================================

    # --- ewram.inc: gEquipChainSlotRefs = 0x0201bb90 ---
    (0x080781b8, 0x0201bb90, 'gEquipChainSlotRefs',
     'gequip_chain_refs_pool_81b8', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080781bc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_81bc', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x080781c0, 0x0201c510, 'gDuelFieldSlots',
     'gduel_field_slots_pool_81c0', None),

    # =========================================================================
    # invoke_equip_zone_bitmap_pair_if_spell_card_type (0x080781dc)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08078218, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_8218', None),

    # --- ewram.inc: gDuelFieldSlots_p2_base = 0x0201c5d8 ---
    (0x0807821c, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'gduel_slots_p2_base_pool_821c', None),

    # --- card_info.inc: SANCTUARY_CID_SHIFTED = 0xbaf00000 ---
    (0x08078220, 0xbaf00000, 'SANCTUARY_CID_SHIFTED',
     'sanctuary_cid_shifted_pool_8220', None),

    # =========================================================================
    # enumerate_equip_slots_for_sprite_bitmap_pair (0x0807822c)
    # =========================================================================

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080782b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_82b4', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x080782b8, 0x0201c510, 'gDuelFieldSlots',
     'gduel_field_slots_pool_82b8', None),

    # --- card_info.inc: BLUE_EYES_WHITE_DRAGON_CID = 0x00000fa7 ---
    (0x080782bc, 0x00000fa7, 'BLUE_EYES_WHITE_DRAGON_CID',
     'blue_eyes_cid_pool_82bc',
     'BLUE_EYES_WHITE_DRAGON_CID: card type pairing upper-bound key for check_card_pair_allowed'),

    # =========================================================================
    # scan_both_players_slots_for_equip_activation (0x080784b4)
    # =========================================================================

    # --- ewram.inc: gEquipZoneCountTable = 0x0201e1c8 ---
    (0x08078508, 0x0201e1c8, 'gEquipZoneCountTable',
     'gequip_zone_cnt_pool_8508',
     'gEquipZoneCountTable: equip zone count table base (EWRAM)'),

]  # end EQ_SLOTS (33 slots)

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    3 slots -- dispatch table ptr + 2 sub-stub block starts
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # PTR_DAT_08077f2c -> dangerous_machine_dispatch_table_7f44 (6-entry raw-ptr table)
    # .word 0x08077f44 = entry[0] of 6-entry raw dispatch table; slot at 0x08077f2c
    # Use unique slot label: dangerous_machine_dispatch_table_ptr_7f2c
    (0x08077f2c, 0x08077f44, 'dangerous_machine_dispatch_table_7f44',
     'dangerous_machine_dispatch_table_ptr_7f2c',
     '.word 0x08077f44; 6-entry raw-ptr dispatch table base; fn_eligible_dangerous_machine_type6 pool ptr'),

    # DAT_08077f44 -> dangerous_machine_dispatch_sub_stubs_7f44 (B7 sub-stubs block start)
    # entry[0] of PTR_DAT_08077f2c = 0x08077f44; self-target
    (0x08077f44, 0x08077f44, 'dangerous_machine_dispatch_sub_stubs_7f44',
     'dangerous_machine_dispatch_sub_stubs_7f44',
     'B7 sub-stubs block start; entry[0] of 6-entry dispatch table @0x08077f2c'),

    # DAT_08078368 -> monster_gate_dispatch_sub_stubs_8368 (B9 sub-stubs block start)
    # entry[30] of 31-entry dispatch table at 0x080782ec = 0x08078368; self-target
    (0x08078368, 0x08078368, 'monster_gate_dispatch_sub_stubs_8368',
     'monster_gate_dispatch_sub_stubs_8368',
     'B9 sub-stubs block start; entry[30] of 31-entry dispatch table @0x080782ec'),

]  # end REF_SLOTS (3 slots)

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

    # set primary on target label
    for sym in sym_tbl.getSymbols(a_target):
        if sym.getName() == gas_label:
            sym.setPrimary()
            break

    # USER label at slot (unique, != gas_label when slot != target)
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
    print("=== RefineF09Seg9bSlots (DRY=%s) ===" % DRY)
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

    print("\n=== RefineF09Seg9bSlots DONE ===")
    print("  EQ_SLOTS applied: %d" % len(EQ_SLOTS))
    print("  REF_SLOTS applied: %d" % len(REF_SLOTS))

main()
