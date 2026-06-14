# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF07Seg9Slots.py -- F07 Seg-9 (0x08062d28..0x08063830)
#   equip effect chain cluster: 35 named fn + 3 disasm blocks (3 new fn)
#   EQ=40 (43 auto-name slots minus 3 PTR_ which are RENAME)
#   RENAME=3 (PTR_gP1LifePoints_ -> gp1lp_ptr_*)
#   PLATE=0 (no stale FUN_, no CJK in segment)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- any CJK here is a red-line error.

from ghidra.program.model.symbol import SourceType
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
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- card_info.inc: BANISHER_OF_THE_LIGHT_CID = 0x00001332 ---
    (0x08062de8, 0x00001332, 'BANISHER_OF_THE_LIGHT_CID',
     'banisher_cid_08062de8', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08062df0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08062df0', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08062e84, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_08062e84', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08062e88, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08062e88', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08062f30, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_08062f30', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08062f34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08062f34', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08062fd8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08062fd8', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08062fdc, 0x0201c510, 'gDuelFieldSlots',
     'duel_field_slots_08062fdc', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x08063048, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_08063048', None),

    # --- duel_field.inc: FIELD_STATE_OFF = 0x00001cf4 ---
    (0x0806304c, 0x00001cf4, 'FIELD_STATE_OFF',
     'field_state_off_0806304c', None),

    # --- card_info.inc: RING_OF_MAGNETISM_CID = 0x00001318 ---
    (0x08063050, 0x00001318, 'RING_OF_MAGNETISM_CID',
     'ring_mag_cid_08063050',
     'RING_OF_MAGNETISM_CID=0x1318: count_equip_slots_with_active_chain config constant'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080630f0, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_080630f0', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080630f4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080630f4', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08063180, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063180', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08063184, 0x0201c510, 'gDuelFieldSlots',
     'duel_field_slots_08063184', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08063240, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063240', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 ---
    (0x08063244, 0x0201c510, 'gDuelFieldSlots',
     'duel_field_slots_08063244', None),

    # --- duel_field.inc: FIELD_STATE_OFF = 0x00001cf4 ---
    (0x080632f0, 0x00001cf4, 'FIELD_STATE_OFF',
     'field_state_off_080632f0', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x0806339c, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_0806339c', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080633a0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080633a0', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080633e4, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_080633e4', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x0806343c, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_0806343c', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x0806347c, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_0806347c', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08063480, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063480', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080634f4, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_080634f4', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080634f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080634f8', None),

    # --- duel_field.inc: FIELD_STATE_OFF = 0x00001cf4 ---
    (0x080634fc, 0x00001cf4, 'FIELD_STATE_OFF',
     'field_state_off_080634fc', None),

    # --- card_info.inc: PROTECTOR_OF_SANCTUARY_CID = 0x0000178b ---
    (0x08063500, 0x0000178b, 'PROTECTOR_OF_SANCTUARY_CID',
     'protector_cid_08063500',
     'PROTECTOR_OF_SANCTUARY_CID=0x178b: effect zone scan param'),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080635b0, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_080635b0', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080635b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080635b4', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080635ec, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_080635ec', None),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 ---
    (0x080635f0, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'p1lp_block2_off_080635f0', None),

    # --- duel_field.inc: FIELD_STATE_OFF = 0x00001cf4 ---
    (0x080635f4, 0x00001cf4, 'FIELD_STATE_OFF',
     'field_state_off_080635f4', None),

    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 ---
    (0x080636c4, 0x0201c4e0, 'gP1LifePoints',
     'gp1lp_ref_080636c4', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x080636c8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_080636c8', None),

    # --- card_info.inc: DARK_RULER_VANDALGYON_CID = 0x0000190a ---
    (0x080636ec, 0x0000190a, 'DARK_RULER_VANDALGYON_CID',
     'vandalgyon_cid_080636ec', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 ---
    (0x08063784, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_stride_08063784', None),

    # --- card_info.inc: TADPOLE_CID = 0x00001919 ---
    (0x08063788, 0x00001919, 'TADPOLE_CID',
     'tadpole_cid_08063788', None),

    # --- card_info.inc: POLYMERIZATION_CID = 0x000012e5 ---
    (0x080637b4, 0x000012e5, 'POLYMERIZATION_CID',
     'poly_cid_080637b4', None),

    # --- card_info.inc: DES_FROG_CID = 0x00001918 (NEW) ---
    (0x08063810, 0x00001918, 'DES_FROG_CID',
     'des_frog_cid_08063810', None),
]

# ---------------------------------------------------------------------------
# B. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename + optional EOL comment (pure ASCII, no CJK).
#    Used for PTR_gP1LifePoints_* slots (value is a pointer, not a CID equate)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08062dec, 'gp1lp_ptr_08062dec', 'gP1LifePoints ptr'),
    (0x080632ec, 'gp1lp_ptr_080632ec', 'gP1LifePoints ptr'),
    (0x08063780, 'gp1lp_ptr_08063780', 'gP1LifePoints ptr'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- DRY WARN treated as FAIL" % (slot_addr, eq_name))
        return

    if DRY:
        print("[dry] EQ 0x%08x  %s=%s  label=%s" % (slot_addr, eq_name, hex(value), slot_label))
        return

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
    print("=== RefineF07Seg9Slots (DRY=%s) ===" % DRY)
    print("  Seg-9: 0x08062d28..0x08063830")
    print("  35 named fn + 3 disasm blocks (processed in DisassembleF07Seg9Blocks.py)")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        before_fail = eq_fail
        # Count fails via _check pre-call
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
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES -- check values before real run !!!" % eq_fail)

    # B. RENAME_SLOTS
    print("\n--- B. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    print("\n=== RefineF07Seg9Slots DONE ===")
    print("  EQ=%d  RENAME=%d" % (len(EQ_SLOTS), len(RENAME_SLOTS)))

main()
