# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg8aSlots.py -- F08 Seg-8a (0x0806ab0c..0x0806b56c)
#   LP row dispatch + switchD + Germ/Momonga/Spear Cretin handlers
#   EQ=22 (21 reuse + 1 NEW: GIANT_GERM_CID)
#   REF=1  (switchD_0806ac1e data ptr)
#   RENAME=5 (PTR_gP1LifePoints_* -> descriptive labels)
#   FUNC_RENAME=2 (dispatch_neo_daedalus_* -> dispatch_germ_momonga_* / dispatch_spear_cretin_*)
#   PLATE=2 (substring replace on renamed functions)
#   carve=0  disasm handled in DisassembleF08Seg8aBlocks.py
#   SS5.1: 0x0806adb6 (0x3e orphan, 0 refs) -- .byte unchanged, not touched
#
# Mode A fixes applied (2 items):
#   #1 (C6): gduelvardctxbase_0806b41c -> gduelcardctxbase_0806b41c (typo fix)
#   #2 (C11): FUNC_RENAME ripple checklist: CSV sync + cross-module plate asm/05
#
# NEW constants added to constants/ before running:
#   card_info.inc: GIANT_GERM_CID=0x1339 (between KARATE_MAN_CID and NIMBLE_MOMONGA_CID)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_040745-pre-F08Seg8a

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
#    22 slots total (21 reuse + 1 NEW: GIANT_GERM_CID=0x1339)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- gDuelPhaseFlags = 0x0201b290 (6 slots, reuse ewram.inc) ----
    (0x0806ab60, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806ab60', None),
    (0x0806ac20, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806ac20', None),
    (0x0806b340, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806b340', None),
    (0x0806b3d4, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806b3d4', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (5 slots, reuse ewram.inc) ----
    (0x0806ab68, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806ab68', None),
    (0x0806ab94, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806ab94', None),
    (0x0806ad24, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806ad24', None),
    (0x0806b4d8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806b4d8', None),
    (0x0806b510, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806b510', None),

    # ---- LP_CARD_TRACK_BASE_OFF = 0x1da8 (2 slots, reuse ewram.inc L247) ----
    (0x0806abc8, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_0806abc8', None),
    (0x0806ad5c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_0806ad5c', None),

    # ---- gP1SlotSetCodeArray = 0x0201c740 (1 slot, reuse ewram.inc L330) ----
    (0x0806ad28, 0x0201c740, 'gP1SlotSetCodeArray', 'gp1slotsetcodearray_0806ad28', None),

    # ---- LP_CARD_TRACK_NEXT_OFF = 0x1daa (1 slot, reuse ewram.inc L248) ----
    (0x0806ad84, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_0806ad84', None),

    # ---- GIANT_GERM_CID = 0x1339 (3 slots: 1 NEW + 2 reuse) ----
    # NEW: card_info.inc GIANT_GERM_CID added before running script
    (0x0806b360, 0x00001339, 'GIANT_GERM_CID', 'giant_germ_cid_0806b360',
     'GIANT_GERM_CID=0x1339: Giant Germ; dispatch_germ_momonga_trigger_display_by_state CID check'),
    (0x0806b434, 0x00001339, 'GIANT_GERM_CID', 'giant_germ_cid_0806b434', None),
    (0x0806b4a0, 0x00001339, 'GIANT_GERM_CID', 'giant_germ_cid_0806b4a0', None),

    # ---- EQUIP_PHASE_FRAME_OFF = 0x4a4 (3 slots, reuse ewram.inc L434) ----
    (0x0806b3d8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806b3d8', None),
    (0x0806b49c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806b49c', None),
    (0x0806b538, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806b538', None),

    # ---- gDuelCardCtxBase = 0x0201e2a0 (1 slot, reuse ewram.inc L218) ----
    # Note: slot_label corrected from gduelvardctxbase -> gduelcardctxbase (Mode A fix #1)
    (0x0806b41c, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_0806b41c', None),

    # ---- gP1LifePoints = 0x0201c4e0 (2 slots, reuse ewram.inc) ----
    (0x0806b420, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806b420', None),
    (0x0806b498, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806b498', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    1 slot: switchD_0806ac1e data pointer
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DAT_0806ac24 -> switchD jump table data at 0x0806ac28
    (0x0806ac24, 0x0806ac28, 'switchD_0806ac1e__switchdataD_0806ac28',
     'switchd_0806ac1e_data_ptr_0806ac24',
     'switchD_0806ac1e data table ptr; table at 0x0806ac28 (inline in dispatch_equip_effect_slot_display_by_state_and_card)'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, new_label, eol_ascii_or_None)
#    5 slots: PTR_gP1LifePoints_* -> descriptive labels
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0806ab64, 'lp_base_slot_player_0806ab64', None),
    (0x0806ab90, 'lp_base_opponent_0806ab90', None),
    (0x0806abc4, 'lp_base_face_down_0806abc4', None),
    (0x0806ad58, 'lp_base_card_lookup_0806ad58', None),
    (0x0806ad80, 'lp_base_hand_sprite_0806ad80', None),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: (func_addr, new_name)
#    2 function renames (misnamed -- CID evidence)
#    Ripple: bl refs updated automatically; plate/CSV must be updated separately
# ---------------------------------------------------------------------------
FUNC_RENAMES = [
    # dispatch_neo_daedalus_effect_display_by_state -> dispatch_germ_momonga_trigger_display_by_state
    # Evidence: CID 0x1339=Giant Germ + 0x133a=Nimble Momonga (not Neo Daedalus)
    (0x0806b31c, 'dispatch_germ_momonga_trigger_display_by_state'),
    # dispatch_neo_daedalus_placement_check_if_chain_subtype -> dispatch_spear_cretin_activate_if_chain_subtype
    # Evidence: CID 0x133b=Spear Cretin (dispatch table @0x9e436d0 + 0x9e45830)
    (0x0806b53c, 'dispatch_spear_cretin_activate_if_chain_subtype'),
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (func_addr, old_text, new_text)
#    Applied AFTER FUNC_RENAME. All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # dispatch_germ_momonga_trigger_display_by_state (0x0806b31c) plate rewrites (5 substrings)
    (0x0806b31c, 'Neo-Daedalus group A', 'Giant Germ (CID=0x1339)'),
    (0x0806b31c, 'Neo-Daedalus group B', 'Nimble Momonga (CID=0x133a)'),
    (0x0806b31c, 'Neo-Daedalus effect series', 'Giant Germ / Nimble Momonga trigger effect'),
    (0x0806b31c, 'CARD_ID_0x1339=0x1339 (Neo-Daedalus group A)', 'GIANT_GERM_CID=0x1339 (Giant Germ)'),
    (0x0806b31c, 'CARD_ID_0x133a=0x133a (Neo-Daedalus group B)', 'NIMBLE_MOMONGA_CID=0x133a (Nimble Momonga)'),
    # dispatch_spear_cretin_activate_if_chain_subtype (0x0806b53c) plate rewrite (1 substring)
    (0x0806b53c, 'Neo Daedalus placement check by equip-slot subtype',
     'Spear Cretin activate by equip-slot chain subtype'),
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

    existing_t = sym_tbl.getSymbols(a_target)
    tnames = [s.getName() for s in existing_t]
    if gas_label not in tnames:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    syms = list(sym_tbl.getSymbols(a_target))
    for s in syms:
        if s.getName() == gas_label:
            s.setPrimary()
            break

    existing_s = sym_tbl.getSymbols(a_slot)
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


def _apply_rename(slot_addr, new_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, new_label))
        return

    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if new_label not in names:
        sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in RENAME EOL @ 0x%08x -- skipping" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REN] 0x%08x -> %s" % (slot_addr, new_label))


def _apply_func_rename(func_addr, new_name):
    a = _addr(func_addr)
    fn_mgr = currentProgram.getFunctionManager()

    if DRY:
        print("[dry] FUNC_RENAME 0x%08x -> %s" % (func_addr, new_name))
        return True

    fn = fn_mgr.getFunctionAt(a)
    if fn is None:
        print("[FAIL] FUNC_RENAME 0x%08x: no function found" % func_addr)
        return False

    old_name = fn.getName()
    if old_name == new_name:
        print("[SKIP] FUNC_RENAME 0x%08x: already named %s" % (func_addr, new_name))
        return True

    fn.setName(new_name, SourceType.USER_DEFINED)
    print("[FRN] 0x%08x: %s -> %s" % (func_addr, old_name, new_name))
    return True


def _apply_plate_fix(func_addr, old_text, new_text):
    for txt in [old_text, new_text]:
        if any(ord(ch) > 127 for ch in txt):
            print("[PLATE FAIL] non-ASCII in plate_fix text @ 0x%08x -- skipping" % func_addr)
            return

    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment -- FAIL" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate -- FAIL" % (func_addr, old_text))
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
    print("=== RefineF08Seg8aSlots (DRY=%s) ===" % DRY)
    print("  Seg-8a: 0x0806ab0c..0x0806b56c")
    print("  EQ=%d  REF=%d  RENAME=%d  FUNC_RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS),
        len(FUNC_RENAMES), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES !!!" % eq_fail)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for entry in RENAME_SLOTS:
        slot_addr, new_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, new_label, eol)

    # D. FUNC_RENAME
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))
    fn_ok = fn_fail = 0
    for func_addr, new_name in FUNC_RENAMES:
        if _apply_func_rename(func_addr, new_name):
            fn_ok += 1
        else:
            fn_fail += 1
    print("  FUNC_RENAME done: %d ok, %d fail" % (fn_ok, fn_fail))
    if fn_fail > 0:
        print("  !!! %d FUNC_RENAME FAILURES !!!" % fn_fail)

    # E. PLATE_REWRITES (run after FUNC_RENAME so addresses are stable)
    print("\n--- E. PLATE_REWRITES (%d entries) ---" % len(PLATE_REWRITES))
    plate_ok = plate_fail = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        a = _addr(func_addr)
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is None:
            print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
            plate_fail += 1
            continue
        existing = cu.getComment(CodeUnit.PLATE_COMMENT)
        if existing is None:
            print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
            plate_fail += 1
            continue
        if old_text not in existing:
            print("[WARN] plate_fix 0x%08x: '%s' not found -- FAIL" % (func_addr, old_text))
            plate_fail += 1
            continue
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1
    print("  PLATE done: %d ok, %d fail" % (plate_ok, plate_fail))
    if plate_fail > 0:
        print("  !!! %d PLATE FAILURES !!!" % plate_fail)

    print("\n=== RefineF08Seg8aSlots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  RENAME=%d  FUNC_RENAME=%d/%d ok  PLATE=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS),
        len(REF_SLOTS),
        len(RENAME_SLOTS),
        fn_ok, len(FUNC_RENAMES),
        plate_ok, len(PLATE_REWRITES)))
    print("  REMINDER: After real run, manually update:")
    print("    - doc/dev/naming-proposals.csv row 2009 (0x0806b31c)")
    print("    - doc/dev/naming-proposals.csv row 2010 (0x0806b53c)")
    print("    - asm/05_equip_eligibility_a.s line 4 plate: dispatch_neo_daedalus_effect_display_by_state -> dispatch_germ_momonga_trigger_display_by_state")


main()
