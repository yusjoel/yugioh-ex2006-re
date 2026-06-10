# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg8Slots.py -- file 02 Seg-8 (0x08032e80..0x08033654)
#   monster/field zone slot count + field spell placement check
#   (23 fn, 44 slots: 38 EQ + 6 RENAME)
#
# Sections:
#   A. EQ_SLOTS   -- 38 slots (33 EQ_REUSE + 5 EQ_NEW)
#                    New constants added to:
#                      card_info.inc (+4: TOON_WORLD_CARD_ID, GROUND_COLLAPSE_FIELD_CARD_ID,
#                                        OJAMA_KING_CARD_ID, SPATIAL_COLLAPSE_CARD_ID)
#                      ewram.inc     (+1: gDuelFieldSpellZoneBase)
#   B. REF_SLOTS  -- 0 slots
#   C. RENAME_SLOTS -- 6 slots (4 PTR_gP1LifePoints + 2 independent DAT)
#   D. PLATE_FULL -- 3 full plate rewrites (C8: entire plate replaced)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: carve=0, disasm=0 for this segment.
# NOTE: New constants added to inc files before running this script.
# NOTE: FUNC_RENAME=0; no CSV sync needed.
# NOTE: EQ slot labels differ from eq_name (avoids GAS PC-relative "value too big").

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
#    Slot label MUST differ from eq_name (avoids GAS PC-relative "value too big").
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, reuse, 16 slots) ---
    (0x08032ee8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_monster_slots_by_state_stride', None),
    (0x08032f64, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_eligible_zone_slots_stride', None),
    (0x0803307c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_cards_pair_stride', None),
    (0x08033104, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_active_field6_stride', None),
    (0x0803317c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_occupied_all_zones_stride', None),
    (0x080331b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_occupied_monster_zones_stride', None),
    (0x08033250, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_monster_by_fnptr_stride', None),
    (0x0803328c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field8_is_9_stride', None),
    (0x080332ec, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_chain_field_match_stride', None),
    (0x0803332c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_slots_card_pair_stride', None),
    (0x08033368, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_monster_chain_head_stride', None),
    (0x080333a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_active_zone_card_stride', None),
    (0x080334c0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_blocked_field_stride', None),
    (0x080335a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_monster_slot_accepts_stride', None),

    # --- gDuelFieldSlots = 0x0201c510 (ewram.inc, reuse, 14 slots) ---
    (0x08032eec, 0x0201c510, 'gDuelFieldSlots',
     'count_monster_slots_by_state_base', None),
    (0x08032f68, 0x0201c510, 'gDuelFieldSlots',
     'count_eligible_zone_slots_base', None),
    (0x08033080, 0x0201c510, 'gDuelFieldSlots',
     'count_field_cards_pair_base', None),
    (0x08033108, 0x0201c510, 'gDuelFieldSlots',
     'count_active_field6_base', None),
    (0x080331b8, 0x0201c510, 'gDuelFieldSlots',
     'count_occupied_monster_zones_base', None),
    (0x08033254, 0x0201c510, 'gDuelFieldSlots',
     'count_monster_by_fnptr_base', None),
    (0x08033290, 0x0201c510, 'gDuelFieldSlots',
     'count_field8_is_9_base', None),
    (0x080332e8, 0x0201c510, 'gDuelFieldSlots',
     'count_chain_field_match_base', None),
    (0x08033330, 0x0201c510, 'gDuelFieldSlots',
     'count_slots_card_pair_base', None),
    (0x0803336c, 0x0201c510, 'gDuelFieldSlots',
     'count_monster_chain_head_base', None),
    (0x080333a8, 0x0201c510, 'gDuelFieldSlots',
     'count_active_zone_card_base', None),
    (0x080335a8, 0x0201c510, 'gDuelFieldSlots',
     'check_monster_slot_accepts_base', None),

    # --- EFFECT_ZONE_BITMASK_OFF = 0x000010d0 (duel_field.inc, reuse, 2 slots) ---
    (0x08033180, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'count_occupied_all_zones_bitmask_off',
     'gDuelFieldSlots+0x10d0 effect zone occupation bitmask word offset'),
    (0x0803320c, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'count_occ_monster_bonus_bitmask_off',
     'gDuelFieldSlots+0x10d0 effect zone occupation bitmask word offset'),

    # --- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc, reuse, 3 slots) ---
    (0x08033184, 0x0201bb90, 'gEquipChainSlotRefs',
     'count_occupied_all_zones_effect_ctx', None),
    (0x08033210, 0x0201bb90, 'gEquipChainSlotRefs',
     'count_occ_monster_bonus_effect_ctx', None),
    (0x080335ac, 0x0201bb90, 'gEquipChainSlotRefs',
     'check_monster_slot_effect_ctx', None),

    # --- NODE_POOL_NEG_OFFSET = 0xffffeb50 (duel_field.inc, reuse, 1 slot) ---
    (0x080334c8, 0xffffeb50, 'NODE_POOL_NEG_OFFSET',
     'check_slot_blocked_node_neg_off', None),

    # --- gP1AltHandCountBase = 0x0201c4fc (ewram.inc, reuse, 1 slot) ---
    (0x080334d4, 0x0201c4fc, 'gP1AltHandCountBase',
     'check_slot_blocked_alt_hand_base', None),

    # --- EQ_NEW: gDuelFieldSpellZoneBase = 0x0201c5ec (ewram.inc NEW, 1 slot) ---
    (0x080334bc, 0x0201c5ec, 'gDuelFieldSpellZoneBase',
     'check_slot_blocked_fz_base',
     'gDuelFieldSlots+11*0x14=P0 field-spell zone slot entry base; r10 scan base'),

    # --- EQ_NEW: TOON_WORLD_CARD_ID = 0x000012be (card_info.inc NEW, 1 slot) ---
    (0x08033098, 0x000012be, 'TOON_WORLD_CARD_ID',
     'check_toon_world_card_id',
     '0x12be (Toon World); presence check via equip-zone scan'),

    # --- EQ_NEW: GROUND_COLLAPSE_FIELD_CARD_ID = 0x00001432 (card_info.inc NEW, 1 slot) ---
    (0x080334cc, 0x00001432, 'GROUND_COLLAPSE_FIELD_CARD_ID',
     'check_slot_blocked_ground_collapse_id',
     'Ground Collapse field spell id (data.md line 900); monster-zone placement block'),

    # --- EQ_NEW: OJAMA_KING_CARD_ID = 0x000017ee (card_info.inc NEW, 1 slot) ---
    (0x080334d0, 0x000017ee, 'OJAMA_KING_CARD_ID',
     'check_slot_blocked_ojama_king_id',
     'Ojama King id (data.md line 1639); monster-zone limit effect placement block'),

    # --- EQ_NEW: SPATIAL_COLLAPSE_CARD_ID = 0x000016df (card_info.inc NEW, 1 slot) ---
    (0x080335f8, 0x000016df, 'SPATIAL_COLLAPSE_CARD_ID',
     'count_avail_monster_spatial_id',
     'Spatial Collapse field spell id; monster zone clamp'),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: empty
# ---------------------------------------------------------------------------
REF_SLOTS = [
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    6 slots: 4 PTR_gP1LifePoints + 2 independent DAT
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # --- PTR_gP1LifePoints slots (already DATA-ref form, rename only) ---
    (0x08033084, 'count_field_cards_pair_lp_base',
     'gP1LifePoints: hand count[+0x14] + alt zone array 0x83<<3=0x418'),
    (0x08033178, 'count_occupied_all_zones_lp_base',
     'gP1LifePoints: +0x30=gDuelFieldSlots scan base; +0x10d0=EFFECT_ZONE_BITMASK_OFF'),
    (0x08033208, 'count_occ_monster_bonus_lp_base',
     'gP1LifePoints: +0x10d0=EFFECT_ZONE_BITMASK_OFF bitmask flag'),
    (0x080334d8, 'check_slot_blocked_lp_base',
     'gP1LifePoints: effect entity ctx slot+0x1c(P0_idx)/+0x20(P1_idx)'),

    # --- Independent DAT slots ---
    (0x08033528, 'check_slot_blocked_equip_key',
     '0x1472: equip-whitelist chain key; spell/trap zone path; 31 raw refs'),
    (0x080334c4, 'check_slot_blocked_node_pool_off',
     '0x13d4 = gEquipNodePool - gDuelFieldSpellZoneBase (1 raw ref; derived offset)'),

]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: 3 full plate rewrites (C8: entire plate replaced, not substring)
#    All stale FUN_ -> current function names. Pure ASCII.
#    Format: (func_addr, new_plate_text)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: count_slots_with_chain_field_match (0x08033294) -- CJK plate rewrite
    (0x08033294,
     "Counts player (r0 bit0) monster zone slots 0..4 satisfying:"
     " slot occupied (bit9 set);"
     " if cond_a(r1!=0): slot[+0x8](equip_chain_head)!=0;"
     " if cond_b(r2!=0): slot[+0x6](chain_field)!=0."
     " Both conditions pass -> count++."
     " Pure leaf, no side effects."
     " r0=u32 player_side [0..1]; r1=u32 cond_a_flag; r2=u32 cond_b_flag."
     " Returns u32 count [0..5]."
     " Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868,"
     " slot_entry=0x14, slot+0x8=equip_chain_head, slot+0x6=chain_field."),

    # PLATE-2: count_monster_slots_by_chain_head_id (0x08033334) -- CJK plate rewrite
    (0x08033334,
     "Counts player (r0 bit0) monster zone slots 0..4 where:"
     " slot occupied (bit19 set) AND slot[+8] low16 == r1 (target_chain_head_id)."
     " Loop stride 0x14, descending r3=4..0. Returns hit count."
     " Used to detect if a card is currently mounted as equip chain head"
     " on a monster zone slot."
     " r0=u32 player_side [0..1]; r1=u32 target_chain_head_id."
     " Returns u32 count [0..5]."
     " Constants: gDuelFieldSlots=0x0201c510, player_stride=0x868, slot_entry=0x14."
     " Field-spell IDs checked in caller check_slot_placement_blocked_by_field_effect:"
     " Ground_Collapse_id=0x1432, OjamaKing_id=0x17ee."),

    # PLATE-3: count_eligible_zone_slots_all_flags (0x08032f6c)
    # stale FUN_08032f00 -> count_eligible_zone_slots_for_player
    (0x08032f6c,
     "Thin wrapper around count_eligible_zone_slots_for_player."
     " Sets r2=-1 (movs r2,#1; rsbs r2,r2,#0 = all-flags)"
     " then calls count_eligible_zone_slots_for_player."
     " Counts all eligible zone slots for given player side with all zone bits selected."
     " r0=u8 player_id [0..1]. Returns r0=u8 count [0..5]."
     " Constants: ZONE_FLAG_ALL=-1."),

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
    print("=== RefineF02Seg8Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-8: 0x08032e80..0x08033654, 23 fn, 44 slots")
    print("  EQ=%d REF=%d RENAME=%d PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS (empty)
    print("\n--- B. REF_SLOTS (%d) [empty] ---" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_FULL (3 full plate rewrites -- C8 entire plate, no stale FUN_)
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    print("\n=== RefineF02Seg8Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
