# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg10bSlots.py -- p5 file09 Seg-10b (0x08079500..0x08079e60)
#   apply_equip_activation_for_all_slots_both_players (0x08079500)
#   dispatch_equip_slot_activation_seq_by_lp_state    (0x08079594)
#   dispatch_equip_slot_sprite_by_zone_flag_and_count (0x080797d0)
#   tick_neo_daedalus_equip_lp_state                  (0x08079944)
#
# Sections:
#   A. EQ_SLOTS   -- 15 slots (all REUSE)
#   B. REF_SLOTS  -- 3 slots (scalar ptr-to-table .word slots)
#   C. RENAME_SLOTS -- 0 slots
#   D. PLATE_REWRITES -- 0 updates
#
# Constants (all REUSE from constants/ewram.inc + constants/card_info.inc):
#   PLAYER_BLOCK_STRIDE       = 0x868   (ewram.inc:250)
#   EQUIP_PHASE_FRAME_OFF     = 0x4a4   (ewram.inc:436)
#   gEquipZoneCountTable      = 0x0201e1c8 (ewram.inc:396)
#   gDuelFieldSlots           = 0x0201c510 (ewram.inc:313)
#   gDuelPhaseFlags           = 0x0201b290 (ewram.inc:352)
#   CARD_DISPLAY_OP31_LP_BAR_SUB = 0x11d (card_info.inc:1497)
#
# NEW constant added to constants/card_info.inc BEFORE this script:
#   INFERNO_TEMPEST_CID = 0x000017ca (fn_eligible @ 0x08079bdc)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0; disasm handled by DisassembleF09Seg10bBlocks.py

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
#    15 slots -- all REUSE
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # =========================================================================
    # apply_equip_activation_for_all_slots_both_players (0x08079500)
    # =========================================================================

    (0x08079588, 0x0201e1c8, 'gEquipZoneCountTable',
     'EQ_gEquipZoneCountTable',
     'gEquipZoneCountTable: equip zone count tracking table base (EWRAM)'),

    (0x0807958c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'EQ_PLAYER_STRIDE',
     'PLAYER_BLOCK_STRIDE: byte stride per player data block (0x868)'),

    (0x08079590, 0x0201c510, 'gDuelFieldSlots',
     'EQ_gDuelFieldSlots',
     'gDuelFieldSlots: duel field zone slot array base (EWRAM)'),

    # =========================================================================
    # dispatch_equip_slot_activation_seq_by_lp_state (0x08079594)
    # =========================================================================

    (0x080795b8, 0x0201b290, 'gDuelPhaseFlags',
     'EQ_gDuelPhaseFlags',
     'gDuelPhaseFlags: duel phase flags struct base (EWRAM)'),

    (0x08079640, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'EQ_PLAYER_STRIDE',
     None),

    (0x08079644, 0x0201c510, 'gDuelFieldSlots',
     'EQ_gDuelFieldSlots',
     None),

    # =========================================================================
    # dispatch_equip_slot_sprite_by_zone_flag_and_count (0x080797d0)
    # =========================================================================

    (0x0807985c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'EQ_PLAYER_STRIDE',
     None),

    (0x08079860, 0x0201c510, 'gDuelFieldSlots',
     'EQ_gDuelFieldSlots',
     None),

    (0x08079898, 0x0201b290, 'gDuelPhaseFlags',
     'EQ_gDuelPhaseFlags',
     None),

    (0x0807989c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'EQ_EQUIP_PHASE_FRAME_OFF',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter [gDuelPhaseFlags+0x4a4]'),

    (0x08079938, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'EQ_PLAYER_STRIDE',
     None),

    (0x0807993c, 0x0201c510, 'gDuelFieldSlots',
     'EQ_gDuelFieldSlots',
     None),

    (0x08079940, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'EQ_EQUIP_PHASE_FRAME_OFF',
     None),

    # =========================================================================
    # tick_neo_daedalus_equip_lp_state (0x08079944)
    # =========================================================================

    (0x08079970, 0x0201b290, 'gDuelPhaseFlags',
     'EQ_gDuelPhaseFlags',
     None),

    (0x080799c0, 0x0000011d, 'CARD_DISPLAY_OP31_LP_BAR_SUB',
     'EQ_CARD_DISPLAY_OP31_LP_BAR_SUB',
     'CARD_DISPLAY_OP31_LP_BAR_SUB: sub-op 0x11d to trigger_card_display_op31_if_not_active LP-bar path'),

]  # end EQ_SLOTS (15 slots)

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    3 slots -- scalar .word ptr-to-table
#    Note: these are raw .word pointers (not THUMB+1), target is a dispatch table.
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # 0x080796ac -> PTR_DAT_080796b0 (B7 5-entry dispatch table)
    (0x080796ac, 0x080796b0,
     'PTR_DAT_080796b0',
     'ptr_to_PTR_DAT_080796b0',
     'raw ptr: 5-entry dispatch table for equip slot activation sub-stubs (B7)'),

    # 0x08079a64 -> PTR_DAT_08079a68 (B9 29-entry dispatch table)
    (0x08079a64, 0x08079a68,
     'PTR_DAT_08079a68',
     'ptr_to_PTR_DAT_08079a68',
     'raw ptr: 29-entry dispatch table for equip zone sprite sub-stubs (B9)'),

    # 0x08079c18 -> PTR_DAT_08079c1c (B10 32-entry dispatch table)
    (0x08079c18, 0x08079c1c,
     'PTR_DAT_08079c1c',
     'ptr_to_PTR_DAT_08079c1c',
     'raw ptr: 32-entry dispatch table for Neo Daedalus equip LP sub-stubs (B10)'),

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

    # create USER label at target (raw ptr, no -1 needed for non-THUMB dispatch tables)
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

    # USER label at slot
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
    print("=== RefineF09Seg10bSlots (DRY=%s) ===" % DRY)
    print("  EQ=%d  REF=%d  RENAME=%d" % (len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS)))
    print("  Range: [0x08079500..0x08079e60)")

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

    print("\n=== RefineF09Seg10bSlots DONE ===")
    print("  EQ_SLOTS applied: %d" % len(EQ_SLOTS))
    print("  REF_SLOTS applied: %d" % len(REF_SLOTS))
    print("  NOTE: Run DisassembleF09Seg10bBlocks.py for B6-B10 disasm")

main()
