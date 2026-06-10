# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg9Slots.py -- file 02 Seg-9 (0x08033654..0x0803407c)
#   equip slot eligibility / field spell placement / graveyard counting
#   (23 fn, 63 slots: 45 EQ + 18 RENAME, 3 PLATE_FULL)
#
# Sections:
#   A. EQ_SLOTS   -- 45 slots (all reuse existing constants from ewram.inc / card_info.inc)
#   B. REF_SLOTS  -- 0 slots
#   C. RENAME_SLOTS -- 18 slots (new constants from card_info.inc already added)
#   D. PLATE_FULL -- 3 full plate rewrites (C8: entire plate replaced, not substring)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=2 (monster_slot_order_table / available_slot_order_table in rom.s)
# NOTE: disasm=0 for this segment.
# NOTE: FUNC_RENAME=0; no CSV sync needed.
# NOTE: New constants added to constants/card_info.inc before running this script.
# NOTE: EQ slot labels MUST differ from eq_name (avoids GAS PC-relative "value too big").

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
#    45 slots -- all reuse existing constants
#    Slot label MUST differ from eq_name (avoids GAS PC-relative "value too big").
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, reuse, 20 slots) ---
    (0x080336bc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_elig_stride', None),
    (0x080336c0, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_equip_elig_slots', None),
    (0x080337d0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_can_equip_stride', None),
    (0x080337d4, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_can_equip_slots', None),
    (0x08033854, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_equip_share_f7_stride', None),
    (0x080338a8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_equip_share_f7_stride_b', None),
    (0x080338ac, 0x0201c510, 'gDuelFieldSlots',
     'check_equip_share_f7_slots', None),
    (0x080339cc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_placements_stride', None),
    (0x080339d0, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_placements_slots', None),
    (0x08033a64, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equippable_slots_stride', None),
    (0x08033a68, 0x0201c510, 'gDuelFieldSlots',
     'count_equippable_slots_slots', None),
    (0x08033b00, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_slots_by_state_stride', None),
    (0x08033b04, 0x0201c510, 'gDuelFieldSlots',
     'count_slots_by_state_slots', None),
    (0x08033b74, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_whitelist_stride', None),
    (0x08033b78, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_whitelist_slots', None),
    (0x08033be4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_available_stride', None),
    (0x08033be8, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_available_slots', None),
    (0x08033cd8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_field_spell_place_stride', None),
    (0x08033d2c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_has_equip_type_stride', None),
    (0x08033d30, 0x0201c510, 'gDuelFieldSlots',
     'check_has_equip_type_slots', None),
    (0x08033d80, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_fieldspell_zone_elig_stride', None),
    (0x08033d84, 0x0201c510, 'gDuelFieldSlots',
     'check_fieldspell_zone_elig_slots', None),
    (0x08033ddc, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_hand_slots_f6_17_stride', None),
    (0x08033de0, 0x0201c510, 'gDuelFieldSlots',
     'count_hand_slots_f6_17_slots', None),
    (0x08033e28, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_hand_slots_f6_16_stride', None),
    (0x08033e2c, 0x0201c510, 'gDuelFieldSlots',
     'count_hand_slots_f6_16_slots', None),
    (0x08033e68, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_spell_zone_empty_stride', None),
    (0x08033e6c, 0x0201c510, 'gDuelFieldSlots',
     'count_spell_zone_empty_slots', None),
    (0x08033ec8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_hand_f6_stride', None),
    (0x08033f24, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_gy_f7_stride', None),
    (0x08033f9c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_gy_equip_stride', None),
    (0x08034018, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_gy_fieldspell_stride', None),
    (0x08034078, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_hand_f6_alt_stride', None),

    # --- SPATIAL_COLLAPSE_CARD_ID = 0x000016df (card_info.inc, reuse, 3 slots) ---
    (0x08033c10, 0x000016df, 'SPATIAL_COLLAPSE_CARD_ID',
     'find_first_avail_slot_spatial_cid',
     'Spatial Collapse field spell; >4 occupied zones -> return -1'),
    (0x08033c84, 0x000016df, 'SPATIAL_COLLAPSE_CARD_ID',
     'count_avail_field_zones_spatial_cid',
     'Spatial Collapse: count zone penalty'),
    (0x08033cd4, 0x000016df, 'SPATIAL_COLLAPSE_CARD_ID',
     'check_field_spell_place_spatial_cid',
     'Spatial Collapse: field spell placement block check'),

    # --- gDuelFieldSlots_p2_base = 0x0201c5d8 (ewram.inc, Seg-7, reuse, 1 slot) ---
    (0x08033cdc, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'check_field_spell_place_p2base', None),

    # --- gP1LifePoints reuse (ewram.inc) -- slot label != eq_name ---
    # Note: these are PTR_gP1LifePoints_* already DATA-ref form, EQ not needed;
    # they will be handled in RENAME section instead.
    # DO NOT duplicate here.

    # --- gP1HandSlotArray = 0x0201c8f8 (ewram.inc, reuse, 2 slots) ---
    (0x08033fa0, 0x0201c8f8, 'gP1HandSlotArray',
     'count_gy_equip_gy_base',
     'gP1HandSlotArray+player*0x868: graveyard scan base for equip cards'),
    (0x0803401c, 0x0201c8f8, 'gP1HandSlotArray',
     'count_gy_fieldspell_gy_base',
     'gP1HandSlotArray+player*0x868: graveyard scan base for field spell cards'),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: empty
# ---------------------------------------------------------------------------
REF_SLOTS = [
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    18 slots: new-const EQ action via RENAME path + PTR_gP1LifePoints renames
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # --- New-const slots: use createLabel only (equate applied via EQ path below,
    #     but these new-const slots need the equate created first then referenced)
    # IMPORTANT: For slots with new constants, we do EQ directly here via _apply_eq.
    # Listed here as RENAME only for labeling; EQ for new consts is handled separately.
    # Actually: proposal says EQ=45 all reuse + RENAME=18 includes new-const slots.
    # The new-const slots need: createEquate(new_name, val) + addReference + createLabel.
    # We include them in EQ_SLOTS_NEW below and apply them in section C.

    # --- PTR_gP1LifePoints slots (already DATA-ref form, rename label only) ---
    (0x08033850, 'check_equip_share_f7_gp1lp',
     'gP1LifePoints: P1 life points base for field7 equip pair check'),
    (0x08033ec4, 'count_hand_f6_gp1lp',
     'gP1LifePoints: player struct base for hand card field6 count'),
    (0x08033f20, 'count_gy_f7_gp1lp',
     'gP1LifePoints: player struct base for graveyard field7 count'),
    (0x08033f98, 'count_gy_equip_gp1lp',
     'gP1LifePoints: player struct base for graveyard equip field9 count'),
    (0x08034014, 'count_gy_fieldspell_gp1lp',
     'gP1LifePoints: player struct base for graveyard fieldspell field9 count'),
    (0x08034074, 'count_hand_f6_alt_gp1lp',
     'gP1LifePoints: player struct base for hand field6 alt count'),

]

# ---------------------------------------------------------------------------
# C2. EQ_SLOTS_NEW: new constants that need createEquate (from card_info.inc additions)
#    (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
# ---------------------------------------------------------------------------
EQ_SLOTS_NEW = [

    # --- monster_slot_order_table ptr (carve label, use RENAME for DAT_ slot) ---
    (0x08033670, 0x09e3ef4c, 'MONSTER_SLOT_ORDER_TABLE',
     'find_first_place_slot_order_tbl',
     'slot priority order table ptr [2,3,1,4,0]; GBA 0x09e3ef4c'),

    # --- EQUIP_ELIG_EXCL_A = 0x000014f9 (card_info.inc NEW) ---
    (0x080336c4, 0x000014f9, 'EQUIP_ELIG_EXCL_A',
     'check_slot_equip_elig_excl_a',
     'equip elig exclusion id A (blocks equip, unoccupied check)'),

    # --- EQUIP_ELIG_EXCL_B = 0x00001836 (card_info.inc NEW) ---
    (0x080336dc, 0x00001836, 'EQUIP_ELIG_EXCL_B',
     'check_slot_equip_elig_excl_b',
     'equip elig exclusion id B (blocks equip, bit-flag check)'),

    # --- EQUIP_ELIG_EXCL_C = 0x00001670 (card_info.inc NEW) ---
    (0x080336e0, 0x00001670, 'EQUIP_ELIG_EXCL_C',
     'check_slot_equip_elig_excl_c',
     'equip elig exclusion id C'),

    # --- EQUIP_ELIG_EXCL_D = 0x000019ee (card_info.inc NEW) ---
    (0x080336f8, 0x000019ee, 'EQUIP_ELIG_EXCL_D',
     'check_slot_equip_elig_excl_d',
     'equip elig exclusion id D (bit18 check)'),

    # --- EQUIP_LOCKDOWN_CID = 0x000013f2 (card_info.inc NEW, 4 slots) ---
    (0x080337d8, 0x000013f2, 'EQUIP_LOCKDOWN_CID',
     'check_slot_can_equip_lockdown',
     'equip lockdown effect: count_field_copies>0 blocks all equip placement'),
    (0x080338dc, 0x000013f2, 'EQUIP_LOCKDOWN_CID',
     'count_equip_placements_lockdown',
     'same lockdown cid as check_slot_can_equip_lockdown'),
    (0x080339fc, 0x000013f2, 'EQUIP_LOCKDOWN_CID',
     'count_equippable_slots_lockdown',
     'same lockdown cid'),
    (0x08033a90, 0x000013f2, 'EQUIP_LOCKDOWN_CID',
     'count_slots_by_state_lockdown',
     'same lockdown cid'),

    # --- EQUIP_ZONE_BLOCKER_CID = 0x000013eb (card_info.inc NEW) ---
    (0x080337dc, 0x000013eb, 'EQUIP_ZONE_BLOCKER_CID',
     'check_slot_can_equip_blocker',
     'cross-player equip blocker: absent -> return 0'),

    # --- EQUIP_LOCK_A_CID = 0x000016a4 (card_info.inc NEW) ---
    (0x080337e0, 0x000016a4, 'EQUIP_LOCK_A_CID',
     'check_slot_can_equip_lock_a',
     'equip lock chain effect A (check_value_in_slot_chain)'),

    # --- EQUIP_LOCK_B_CID = 0x000012d1 (card_info.inc NEW) ---
    (0x080337e4, 0x000012d1, 'EQUIP_LOCK_B_CID',
     'check_slot_can_equip_lock_b',
     'equip lock chain effect B (check_value_in_slot_chain)'),

    # --- EQUIP_PAIR_EXCL_A = 0x000017e9 (card_info.inc NEW) ---
    (0x08033858, 0x000017e9, 'EQUIP_PAIR_EXCL_A',
     'check_equip_share_f7_excl_a',
     'field7-match pair exclusion id A (BST whitelist)'),

    # --- EQUIP_PAIR_EXCL_B = 0x00001521 (card_info.inc NEW) ---
    (0x0803385c, 0x00001521, 'EQUIP_PAIR_EXCL_B',
     'check_equip_share_f7_excl_b',
     'field7-match pair exclusion id B'),

    # --- EQUIP_PAIR_EXCL_C = 0x00001798 (card_info.inc NEW) ---
    (0x08033860, 0x00001798, 'EQUIP_PAIR_EXCL_C',
     'check_equip_share_f7_excl_c',
     'field7-match pair exclusion id C'),

    # --- EQUIP_PAIR_RANGE_MAX = 0x00001874 (card_info.inc NEW) ---
    (0x080338a4, 0x00001874, 'EQUIP_PAIR_RANGE_MAX',
     'check_equip_share_f7_range_max',
     'BST range max for field7 pair check: IDs in [0x1873..0x1874] pass'),

    # --- EQUIP_CHAIN_PAIR_CARD_MAX = 0x0000164f (card_info.inc NEW) ---
    (0x080339d4, 0x0000164f, 'EQUIP_CHAIN_PAIR_CARD_MAX',
     'count_equip_placements_pair_max',
     'max card_id threshold for chain pairing path in count_equip_placements_with_chain_check'),

    # --- available_slot_order_table ptr (carve label) ---
    (0x08033c40, 0x09e3ef60, 'AVAIL_SLOT_ORDER_TABLE',
     'find_first_avail_slot_order_tbl',
     'available slot priority order table ptr [2,3,1,4,0]; GBA 0x09e3ef60'),

]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: 3 full plate rewrites (C8: entire plate replaced, not substring)
#    All stale FUN_ -> current function names. Pure ASCII.
#    Format: (func_addr, new_plate_text)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: check_any_slot_fieldspell_zone_eligible (0x08033d44) -- CJK plate rewrite
    (0x08033d44,
     "Scans player (r0 bit0) 5 monster zone slots (idx 0..4)."
     " Per slot: (1) bit19 occupied;"
     " (2) ldrh [slot+8] equip_chain_head nonzero;"
     " (3) compute_slot_zone_eligibility_mask & 0x7 nonzero"
     " -> return 0 immediately (eligible slot found)."
     " All slots fail -> return 1."
     " Read-only."
     " r0=u32 player_side [0..1]."
     " Returns u32 (0=eligible slot exists, 1=none)."
     " Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868,"
     " slot_entry=0x14, slot_count=5."),

    # PLATE-2: count_spell_zone_slots_with_empty_chain (0x08033e30) -- CJK plate rewrite
    (0x08033e30,
     "Count player-side spell/trap zone slots (idx 0..4, base_offset=0x64)"
     " satisfying: (1) slot[0] bit19 occupied;"
     " (2) slot[+8] equip_chain_head==0."
     " Spell-zone variant of count_monster_slots_by_chain_head_id (0x08033334)."
     " r0=u32 player_side [0..1]."
     " Returns u32 count [0..5]."
     " Constants: gDuelFieldSlots=0x0201c510, PLAYER_BLOCK_STRIDE=0x868,"
     " spell_zone_offset=0x64."),

    # PLATE-3: count_graveyard_equip_cards_by_field9 (0x08033f28) -- CJK plate rewrite
    (0x08033f28,
     "Count graveyard cards where field6==0x16 (equip type) AND field9==r8."
     " r0=u32 player_side [0..1]; r1=u8 field9_target_value (saved to r8 at entry)."
     " Base: gP1HandSlotArray+player*0x868; count from +0x14."
     " Calls get_card_extended_stat_field6 then get_card_extended_stat_field9."
     " Returns u32 count."
     " Read-only."
     " Constants: gP1HandSlotArray=0x0201c8f8, PLAYER_BLOCK_STRIDE=0x868,"
     " EQUIP_FIELD6=0x16."),

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

def _apply_plate_full(func_addr, new_plate):
    """Replace entire plate comment at func_addr with new_plate (pure ASCII).
    After setting, reads back and verifies no FUN_[0-9a-f]{8} remains.
    """
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_full 0x%08x: no code unit" % func_addr)
        return

    if DRY:
        print("[dry] PLATE_FULL 0x%08x (len=%d)" % (func_addr, len(new_plate)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)

    # Readback verification: confirm no FUN_[0-9a-f]{8} pattern remains
    readback = cu.getComment(CodeUnit.PLATE_COMMENT)
    if readback is None:
        print("[WARN] plate_full 0x%08x: readback returned None" % func_addr)
        return

    import re
    stale = re.findall(r'FUN_[0-9a-fA-F]{8}', readback)
    if stale:
        print("[FAIL] plate_full 0x%08x: stale FUN_ still present after write: %s" % (
            func_addr, stale))
    else:
        print("[PLF] 0x%08x: plate replaced OK, no stale FUN_ (len=%d)" % (
            func_addr, len(new_plate)))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF02Seg9Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-9: 0x08033654..0x0803407c, 23 fn, 63 slots")
    print("  EQ=%d EQ_NEW=%d REF=%d RENAME=%d PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(EQ_SLOTS_NEW), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

    # A. EQ_SLOTS (reuse existing constants)
    print("\n--- A. EQ_SLOTS reuse (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ reuse done: %d" % eq_ok)

    # B. REF_SLOTS (empty)
    print("\n--- B. REF_SLOTS (%d) [empty] ---" % len(REF_SLOTS))

    # C. RENAME_SLOTS (PTR_gP1LifePoints label renames)
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # C2. EQ_SLOTS_NEW (new constants -- createEquate if needed, addReference, createLabel)
    print("\n--- C2. EQ_SLOTS_NEW new-const (%d) ---" % len(EQ_SLOTS_NEW))
    eq_new_ok = 0
    for entry in EQ_SLOTS_NEW:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_new_ok += 1
    print("  EQ_NEW done: %d" % eq_new_ok)

    # D. PLATE_FULL (3 full plate rewrites -- C8 entire plate, no stale FUN_)
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    total_eq = len(EQ_SLOTS) + len(EQ_SLOTS_NEW)
    print("\n=== RefineF02Seg9Slots DONE ===")
    print("  EQ_total=%d  REF=%d  RENAME=%d  PLATE_FULL=%d" % (
        total_eq, len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
