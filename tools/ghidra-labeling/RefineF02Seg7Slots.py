# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg7Slots.py -- file 02 Seg-7 (0x0803217c..0x08032e80)
#   zone slot chain refs clear/dispatch + card effect category + equip eligibility
#   (23 fn, 67 slots: all DAT_/DWORD_)
#
# Sections:
#   A. EQ_SLOTS   -- 48 slots (40 EQ_REUSE + 8 EQ_NEW)
#                    New constants added to:
#                      duel_field.inc (+2: EFFECT_ZONE_PARTITION_OFF, EFFECT_ZONE_BITMASK_OFF)
#                      ewram.inc      (+1: gDuelFieldSlots_p2_base)
#   B. REF_SLOTS  -- 0 slots
#   C. RENAME_SLOTS -- 19 slots (2 switchD ptr + 13 classify_cid + 4 equip_elig_cid)
#   D. PLATE_FULL -- 5 full plate rewrites (C8: entire plate replaced to guarantee no stale FUN_)
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

    # --- PLAYER_BLOCK_STRIDE = 0x00000868 (ewram.inc, reuse, 20 slots) ---
    (0x08032274, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'erase_slot_zone_player_stride', None),
    (0x080324e4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_equip_slot_player_stride', None),
    (0x0803252c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_field_slot_player_stride', None),
    (0x08032594, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'test_slot_active_player_stride', None),
    (0x080325d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'check_slot_equip_elig_player_stride', None),
    (0x080326e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_avail_effect_zones_player_stride', None),
    (0x08032744, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_avail_effect_zones_player_stride_b', None),
    (0x08032794, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_avail_effect_zones_player_stride_c', None),
    (0x08032838, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_copies_player_stride', None),
    (0x080328a4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_copies_player_stride_b', None),
    (0x08032900, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_field_copies_player_stride_c', None),
    (0x08032a60, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_elig_player_stride', None),
    (0x08032b20, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_best_slot_player_stride', None),
    (0x08032b94, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'find_best_slot_player_stride_b', None),
    (0x08032c34, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_paired_slots_player_stride', None),
    (0x08032c90, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_paired_slots_player_stride_b', None),
    (0x08032d14, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_paired_player_stride', None),
    (0x08032da8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_set_player_stride', None),
    (0x08032e1c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_zone_player_stride', None),
    (0x08032e7c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'count_equip_atk_player_stride', None),

    # --- gDuelFieldSlots = 0x0201c510 (ewram.inc, reuse, 18 slots) ---
    (0x08032278, 0x0201c510, 'gDuelFieldSlots',
     'erase_slot_zone_field_slots', None),
    (0x080324e8, 0x0201c510, 'gDuelFieldSlots',
     'find_equip_slot_field_slots', None),
    (0x08032530, 0x0201c510, 'gDuelFieldSlots',
     'find_field_slot_field_slots', None),
    (0x08032598, 0x0201c510, 'gDuelFieldSlots',
     'test_slot_active_field_slots', None),
    (0x080325d8, 0x0201c510, 'gDuelFieldSlots',
     'check_slot_equip_elig_field_slots', None),
    (0x080326e0, 0x0201c510, 'gDuelFieldSlots',
     'count_avail_effect_zones_field_slots', None),
    (0x08032740, 0x0201c510, 'gDuelFieldSlots',
     'count_avail_effect_zones_field_slots_b', None),
    (0x08032830, 0x0201c510, 'gDuelFieldSlots',
     'count_field_copies_field_slots', None),
    (0x080328a0, 0x0201c510, 'gDuelFieldSlots',
     'count_field_copies_field_slots_b', None),
    (0x08032a58, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_elig_field_slots', None),
    (0x08032b18, 0x0201c510, 'gDuelFieldSlots',
     'find_best_slot_field_slots', None),
    (0x08032b90, 0x0201c510, 'gDuelFieldSlots',
     'find_best_slot_field_slots_b', None),
    (0x08032c38, 0x0201c510, 'gDuelFieldSlots',
     'count_paired_slots_field_slots', None),
    (0x08032c8c, 0x0201c510, 'gDuelFieldSlots',
     'count_paired_slots_field_slots_b', None),
    (0x08032d18, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_paired_field_slots', None),
    (0x08032da4, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_set_field_slots', None),
    (0x08032e18, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_zone_field_slots', None),
    (0x08032e78, 0x0201c510, 'gDuelFieldSlots',
     'count_equip_atk_field_slots', None),

    # --- gDuelEffectChainSlots = 0x0201bc54 (ewram.inc, reuse, 1 slot) ---
    (0x08032230, 0x0201bc54, 'gDuelEffectChainSlots',
     'erase_slot_effect_chain_slots', None),

    # --- gEquipChainSlotRefs = 0x0201bb90 (ewram.inc, reuse, 1 slot) ---
    (0x08032a68, 0x0201bb90, 'gEquipChainSlotRefs',
     'count_equip_elig_chain_slot_refs', None),

    # --- EFFECT_ZONE_PARTITION_OFF = 0x000010a4 (duel_field.inc NEW, 5 slots) ---
    (0x0803227c, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',
     'erase_slot_zone_effect_zone_off',
     'gDuelFieldSlots+0x10a4 = effect zone slot array base offset'),
    (0x080326e4, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',
     'count_avail_effect_zone_off',
     'gDuelFieldSlots+0x10a4 = effect zone slot array base offset'),
    (0x08032834, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',
     'count_field_copies_effect_zone_off',
     'gDuelFieldSlots+0x10a4 = effect zone slot array base offset'),
    (0x08032a5c, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',
     'count_equip_elig_effect_zone_off',
     'gDuelFieldSlots+0x10a4 = effect zone slot array base offset'),
    (0x08032b1c, 0x000010a4, 'EFFECT_ZONE_PARTITION_OFF',
     'find_best_slot_effect_zone_off',
     'gDuelFieldSlots+0x10a4 = effect zone slot array base offset'),

    # --- gDuelFieldSlots_p2_base = 0x0201c5d8 (ewram.inc NEW, 2 slots) ---
    (0x08032798, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'count_avail_effect_zones_p2_slot',
     'gDuelFieldSlots+0xc8 = slot[10] base for field9==2 path'),
    (0x080328fc, 0x0201c5d8, 'gDuelFieldSlots_p2_base',
     'count_field_copies_p2_slot',
     'gDuelFieldSlots+0xc8 = slot[10] base for field9==2 path'),

    # --- EFFECT_ZONE_BITMASK_OFF = 0x000010d0 (duel_field.inc NEW, 1 slot) ---
    (0x08032a64, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',
     'count_equip_elig_bitmask_off',
     'r10+0x10d0=gDuelFieldSlots+0x10a0=0x0201d5b0 effect zone occupation bitmask bit0'),

]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: empty
# ---------------------------------------------------------------------------
REF_SLOTS = [
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    19 slots: 2 switchD ptr + 13 classify_cid + 4 equip_elig_cid
# ---------------------------------------------------------------------------
RENAME_SLOTS = [

    # --- switchD table pointers (2 slots) ---
    (0x080321bc, 'erase_slot_zone_switch_data',
     'switchD dispatch table for erase_slot_from_zone_array_by_type'),
    (0x0803229c, 'dispatch_card_placement_switch_data',
     'switchD dispatch table for dispatch_card_placement_by_zone_type'),

    # --- card_id whitelist: classify_card_effect_category (13 slots) ---
    (0x0803238c, 'classify_card_effect_category_cid_1348',
     'card_id 0x1348 effect category whitelist entry'),
    (0x08032390, 'classify_card_effect_category_cid_10f5',
     'card_id 0x10f5 effect category whitelist entry'),
    (0x080323a4, 'classify_card_effect_category_cid_10f3',
     'card_id 0x10f3 effect category whitelist entry'),
    (0x080323c0, 'classify_card_effect_category_cid_1345',
     'card_id 0x1345 effect category whitelist entry'),
    (0x080323d4, 'classify_card_effect_category_cid_1346',
     'card_id 0x1346 effect category whitelist entry'),
    (0x080323fc, 'classify_card_effect_category_cid_169f',
     'card_id 0x169f effect category whitelist entry'),
    (0x08032400, 'classify_card_effect_category_cid_14d1',
     'card_id 0x14d1 effect category whitelist entry'),
    (0x08032404, 'classify_card_effect_category_cid_1349',
     'card_id 0x1349 effect category whitelist entry'),
    (0x08032408, 'classify_card_effect_category_cid_149c',
     'card_id 0x149c effect category whitelist entry'),
    (0x0803241c, 'classify_card_effect_category_cid_150b',
     'card_id 0x150b effect category whitelist entry'),
    (0x08032438, 'classify_card_effect_category_cid_187f',
     'card_id 0x187f effect category whitelist entry'),
    (0x0803243c, 'classify_card_effect_category_cid_175e',
     'card_id 0x175e effect category whitelist entry'),
    (0x08032450, 'classify_card_effect_category_cid_18ff',
     'card_id 0x18ff effect category whitelist entry'),

    # --- card_id slots: check_card_equip_eligibility_in_field (4 slots) ---
    (0x0803263c, 'check_card_equip_eligibility_in_field_cid_166c',
     'same-name field limit guard (max 1 copy)'),
    (0x08032640, 'check_card_equip_eligibility_in_field_cid_12bf',
     'chain eligibility guard: check_value_in_slot_chain zone=0xb'),
    (0x08032644, 'check_card_equip_eligibility_in_field_cid_148e',
     'summon restriction type==1 copy check A'),
    (0x08032648, 'check_card_equip_eligibility_in_field_cid_14da',
     'summon restriction type==1 copy check B'),

]

# ---------------------------------------------------------------------------
# D. PLATE_FULL: 5 full plate rewrites (C8: entire plate replaced, not substring)
#    All stale FUN_ -> current function names. Pure ASCII.
#    Format: (func_addr, new_plate_text)
# ---------------------------------------------------------------------------
PLATE_FULL = [

    # PLATE-1: dispatch_card_placement_by_zone_type (0x08032280)
    # FUN_08037630 -> place_equip_card_if_type_matches
    # FUN_08031630 -> append_slot_ref_to_equip_array
    # FUN_08031578 -> insert_slot_ref_into_hand_array
    # FUN_080315f8 -> append_slot_ref_to_hand_array
    # FUN_08036cb8 -> place_card_into_graveyard_slot
    # FUN_08036d08 -> place_card_into_graveyard_slot_with_seq
    (0x08032280,
     "Routes a card placement to the appropriate zone handler by zone_type (r1)."
     " 6-case switch + default dual-branch:"
     " case 0xb=equip-type-check insert (place_equip_card_if_type_matches),"
     " case 0xc=direct equip insert (append_slot_ref_to_equip_array),"
     " case 0xd=hand insert or append (insert_slot_ref_into_hand_array / append_slot_ref_to_hand_array),"
     " case 0xe=graveyard check insert (place_card_into_graveyard_slot),"
     " case 0xf=graveyard insert with seq (place_card_into_graveyard_slot_with_seq),"
     " case 0x10=general branch;"
     " default<=4=monster zone (place_card_into_monster_zone_slot),"
     " default>4=spell/trap zone (place_card_into_spelltrap_zone_slot)."
     " After switch, optionally calls clear_equip_refs_for_leaving_slot and clear_equip_chain_refs_for_slot_zone."
     " r0=u8 player_id, r1=u8 zone_type, r2=u8 flags, r3=ptr slot_ref. Returns void. indeg=10."),

    # PLATE-2: classify_card_effect_category (0x08032358)
    # FUN_0803412c -> check_card_matches_active_effect_slot
    # FUN_0804074c -> tick_card_effect_category_display_seq
    (0x08032358,
     "Maps card_id (r0) to an effect category code [1..0x17] (23 categories)"
     " via multi-level cmp/beq tree."
     " Hardcoded whitelist: 0x1348/0x10f5/0x10f3/0x10f1/0x10f2/0x1345/0x1346/0x169f/0x14d1"
     "/0x1349/0x149c/0x150b/0x175e/0x187f/0x18ff and others."
     " card_id not in whitelist -> returns 0."
     " r0=u16 card_id. Returns u8 effect_category [1..0x17] or 0."
     " Callers: check_card_matches_active_effect_slot, tick_card_effect_category_display_seq,"
     " dispatch_equip_pair_sprites_by_state, 0x080c8f48."),

    # PLATE-3: check_card_equip_eligibility_in_field (0x080325dc)
    # FUN_08032960 (x2) -> count_equip_eligible_slots_for_player
    # FUN_08048020 -> render_slot_card_sprite_and_effects
    # FUN_08048364 -> render_slot_card_sprite_with_chaos_equip_check
    # FUN_08099aac -> run_equip_slot_display_update_state_machine
    # FUN_08099e0c -> run_equip_spell_display_state_machine
    (0x080325dc,
     "Multi-layer equip eligibility check for a field slot entry ptr (r0)."
     " Checks: (1) check_card_field8_is_normal;"
     " (2) slot[+0x34] existing equip bind == 0;"
     " (3) count_field_copies_of_card(0x166c) == 0 (same-name field limit);"
     " (4) if slot[+0x8] nonzero: check_value_in_slot_chain(0x12bf, zone=0xb) == 0;"
     " (5) get_card_field_summon_restriction: if type==1 checks copies of 0x148e and 0x14da;"
     " (6) check_card_targeted_by_spell_zone_effect."
     " Returns 1 if all pass, 0 on any failure. No write side effects. indeg=6."
     " Callers: count_equip_eligible_slots_for_player, render_slot_card_sprite_and_effects,"
     " render_slot_card_sprite_with_chaos_equip_check,"
     " run_equip_slot_display_update_state_machine, run_equip_spell_display_state_machine."),

    # PLATE-4: count_equip_eligible_slots_for_player (0x08032960)
    # FUN_08032a6c -> count_equip_eligible_slots_both_players
    # FUN_080490b4 -> tick_duel_field_zone_sprite_update_pipeline
    # FUN_080325dc -> check_card_equip_eligibility_in_field
    (0x08032960,
     "Counts equip-eligible monster-zone slots for player (r0) and card_id (r1)."
     " Scans 5 slots at gDuelFieldSlots + player*0x868 + 0x10a4 + slot*0x14 (slot 0..4):"
     " card_id match, active flags (bit5/bit1 clear), bitmask check,"
     " then calls check_card_equip_eligibility_in_field."
     " Also checks gEquipChainSlotRefs[0]/[4] for matching card_id via separate path."
     " Returns count of eligible slots. Pure query."
     " Callers: count_equip_eligible_slots_both_players, tick_duel_field_zone_sprite_update_pipeline."),

    # PLATE-5: count_equip_eligible_slots_both_players (0x08032a6c)
    # FUN_0808db90 -> dispatch_equip_pair_sprites_by_state
    # FUN_08032960 -> count_equip_eligible_slots_for_player
    (0x08032a6c,
     "Calls count_equip_eligible_slots_for_player(0, slot_ref)"
     " + count_equip_eligible_slots_for_player(1, slot_ref) and returns sum."
     " r0=ptr slot_ref. Returns u32 total eligible slot count (P1+P2). Pure wrapper."
     " Callers: dispatch_equip_pair_sprites_by_state."),

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
    print("=== RefineF02Seg7Slots (DRY=%s) ===" % DRY)
    print("  file 02 Seg-7: 0x0803217c..0x08032e80, 23 fn, 67 slots")
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

    # D. PLATE_FULL (5 full plate rewrites -- C8 entire plate, no stale FUN_)
    print("\n--- D. PLATE_FULL (%d) ---" % len(PLATE_FULL))
    for func_addr, new_plate in PLATE_FULL:
        _apply_plate_full(func_addr, new_plate)

    print("\n=== RefineF02Seg7Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FULL=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_FULL)))

main()
