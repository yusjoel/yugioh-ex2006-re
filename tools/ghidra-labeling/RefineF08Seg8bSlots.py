# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg8bSlots.py -- F08 Seg-8b (0x0806b56c..0x0806c0cc)
#   CID 135b stubs + Magical Hats stubs + tick_equip_zone_slot_and_lp_indicator_state_machine
#   EQ=17 (15 reuse + 2 NEW: CEASEFIRE_CID, SPELL_ABSORBING_LIFE_CID)
#   REF=2  (check_equip_slot_eligible_by_equip_type fn-ptr + cid_135b_dispatch_jump_table)
#   RENAME=0 (disasm phase handles ROM_INCBIN start label renames)
#   FUNC_RENAME=0
#   PLATE=2 (dispatch_neo_daedalus_placement_check_by_state stale FUN_
#            + dispatch_numinous_healer_lp_zone_sprites EOL/inline const symbolize)
#   carve=0  disasm handled in DisassembleF08Seg8bBlocks.py
#   SS5.1: none
#
# NEW constants added to constants/card_info.inc before running:
#   CEASEFIRE_CID=0x135c (card_0764 pw=36468556)
#   MAGICAL_HATS_CID=0x1362 (card_0769 pw=81210420)
#   SPELL_ABSORBING_LIFE_CID=0x1635 (card_1301 pw=99517131)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_053928-pre-F08Seg8b

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
#    17 slots total (15 reuse + 2 NEW: CEASEFIRE_CID, SPELL_ABSORBING_LIFE_CID)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- NUMINOUS_HEALER_CID = 0x1352 (1 slot, reuse card_info.inc L1154) ----
    (0x0806b58c, 0x00001352, 'NUMINOUS_HEALER_CID', 'numinous_healer_cid_0806b58c',
     'NUMINOUS_HEALER_CID=0x1352: Numinous Healer; dispatch_numinous_healer_lp_zone_sprites CID check'),

    # ---- gDuelPhaseFlags = 0x0201b290 (3 slots, reuse ewram.inc) ----
    (0x0806b638, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806b638', None),
    (0x0806b6bc, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806b6bc', None),
    (0x0806bafc, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806bafc', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (3 slots, reuse ewram.inc) ----
    (0x0806b68c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806b68c', None),
    (0x0806b764, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806b764', None),
    (0x0806bb00, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806bb00', None),

    # ---- gDuelFieldSlots = 0x0201c510 (2 slots, reuse ewram.inc) ----
    (0x0806b690, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslotsbase_0806b690', None),
    (0x0806bb08, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslotsbase_0806bb08', None),

    # ---- gDuelCardCtxBase = 0x0201e2a0 (1 slot, reuse ewram.inc) ----
    (0x0806b6ec, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_0806b6ec', None),

    # ---- gP1LifePoints = 0x0201c4e0 (3 slots, reuse ewram.inc)
    #      Note: asm already shows .word gP1LifePoints but label still DWORD_ ----
    (0x0806b6f0, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806b6f0', None),
    (0x0806b71c, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806b71c', None),
    (0x0806b75c, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806b75c', None),

    # ---- LP_CARD_TRACK_NEXT_OFF = 0x1daa (1 slot, reuse ewram.inc) ----
    (0x0806b760, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_0806b760', None),

    # ---- gEquipZoneCountTable = 0x0201e1c8 (1 slot, reuse ewram.inc) ----
    (0x0806bb04, 0x0201e1c8, 'gEquipZoneCountTable', 'gequipzonecounttable_0806bb04', None),

    # ---- CEASEFIRE_CID = 0x135c (1 slot, NEW card_info.inc) ----
    (0x0806bb2c, 0x0000135c, 'CEASEFIRE_CID', 'ceasefire_cid_0806bb2c',
     'CEASEFIRE_CID=0x135c: Ceasefire (pw=36468556); tick_equip_zone_slot_and_lp_indicator_state_machine CID path'),

    # ---- SPELL_ABSORBING_LIFE_CID = 0x1635 (1 slot, NEW card_info.inc) ----
    (0x0806bb30, 0x00001635, 'SPELL_ABSORBING_LIFE_CID', 'spell_absorbing_life_cid_0806bb30',
     'SPELL_ABSORBING_LIFE_CID=0x1635: The Spell Absorbing Life (pw=99517131); tick_equip_zone_slot_and_lp_indicator_state_machine CID path'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    2 slots:
#      DWORD_0806bb28 -> check_equip_slot_eligible_by_equip_type+1 (THUMB+1 fn ptr)
#      PTR_DAT_0806b7d4 -> cid_135b_dispatch_jump_table (jump table base label)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DWORD_0806bb28: THUMB+1 fn ptr -> check_equip_slot_eligible_by_equip_type (0x08051318)
    # Used as callback to invoke_count_zone_pair_hits_full_range at 0x0806bb0c
    (0x0806bb28, 0x08051319, 'check_equip_slot_eligible_by_equip_type',
     'check_equip_slot_eligible_by_equip_type_ptr_0806bb28',
     'THUMB+1 fn ptr: check_equip_slot_eligible_by_equip_type (0x08051318)+1; callback in tick_equip_zone_slot_and_lp_indicator_state_machine'),

    # PTR_DAT_0806b7d4: label rename to cid_135b_dispatch_jump_table
    # 10-entry raw-addr jump table for check_equip_eligible_cid_135b dispatch
    (0x0806b7d4, 0x0806b7d4, 'cid_135b_dispatch_jump_table',
     'cid_135b_dispatch_jump_table',
     'cid_135b 10-entry raw-addr jump table; dispatched from check_equip_eligible_cid_135b state dispatch'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: none (disasm phase handles ROM_INCBIN start label renames)
# ---------------------------------------------------------------------------
RENAME_SLOTS = []

# ---------------------------------------------------------------------------
# D. FUNC_RENAME: none
# ---------------------------------------------------------------------------
FUNC_RENAMES = []

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES: (func_addr, old_text, new_text)
#    2 entries:
#      1. dispatch_neo_daedalus_placement_check_by_state @ 0x0806c0cc:
#         stale FUN_0806b53c -> dispatch_spear_cretin_activate_if_chain_subtype (Seg-8a rename)
#      2. dispatch_numinous_healer_lp_zone_sprites @ 0x0806b56c:
#         inline const name symbolize
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # Seg-8a rename ripple: update plate of dispatch_neo_daedalus_placement_check_by_state
    # (at 0x0806c0cc, boundary fn; its plate is at asm line 17183 between last ROM_INCBIN
    #  and the function label -- contains stale FUN_0806b53c from before Seg-8a FUNC_RENAME)
    (0x0806c0cc, 'FUN_0806b53c', 'dispatch_spear_cretin_activate_if_chain_subtype'),

    # dispatch_numinous_healer_lp_zone_sprites: symbolize inline const references in plate
    (0x0806b56c, 'CARD_ID_Numinous_Healer=0x1352', 'NUMINOUS_HEALER_CID=0x1352'),
    (0x0806b56c, 'CARD_ID_Attack_and_Receive=0x135a', 'ATTACK_AND_RECEIVE_CID=0x135a'),
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
    print("=== RefineF08Seg8bSlots (DRY=%s) ===" % DRY)
    print("  Seg-8b: 0x0806b56c..0x0806c0cc")
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

    # C. RENAME_SLOTS (none)
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))

    # D. FUNC_RENAME (none)
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))

    # E. PLATE_REWRITES (3 entries for 2 functions)
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

    print("\n=== RefineF08Seg8bSlots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  RENAME=%d  FUNC_RENAME=%d  PLATE=%d/%d ok" % (
        eq_ok, len(EQ_SLOTS),
        len(REF_SLOTS),
        len(RENAME_SLOTS),
        len(FUNC_RENAMES),
        plate_ok, len(PLATE_REWRITES)))


main()
