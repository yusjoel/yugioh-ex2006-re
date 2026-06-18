# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg7Slots.py -- p5 file09 Seg-7 (0x080752cc..0x0807629c)
#   enqueue_effect_card_sprite + tick_graveyard_spell_display +
#   dispatch_effect_activation + invoke_equip_zone_lp_shape cluster
#   19 functions (enqueue_effect_card_sprite_dual_with_negated ..
#                  tick_effect_display_by_state_and_type_code)
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (42 slots: all REUSE)
#   B. REF_SLOTS  -- 0 slots (all globals via EQ pc-relative literal pool)
#   C. RENAME_SLOTS -- 4 slots (dispatch stubs labels + FS ROM ptr + 2B pad area)
#   D. PLATE_REWRITES -- 1 update: enqueue_effect_slot_sprites_all_players plate
#                        gEffectSlots -> gEquipZoneCountTable
#                        gSlotData -> gDuelFieldSlots
#
# New constants added to constants/card_info.inc before this script:
#   EMBLEM_OF_DRAGON_DESTROYER_CID = 0x00001629
#   MAGICAL_DIMENSION_CID          = 0x00001678
#   (FRIENDSHIP_CID=0x167a REUSE -- already at line 1071)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: PLATE_REWRITES WARN/not-found treated as FAIL (report but do not abort).
# NOTE: carve=0; disasm handled by DisassembleF09Seg7Blocks.py

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
#    42 slots, all REUSE (0 NEW in this section)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: gP1LifePoints = 0x0201c4e0 (1 slot) ---
    (0x0807536c, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_536c',
     'gP1LifePoints: P1 LP tracking block base (EWRAM)'),

    # --- duel_field.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (14 slots) ---
    (0x08075370, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5370',
     'PLAYER_BLOCK_STRIDE: byte stride per player data block'),
    (0x08075524, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5524', None),
    (0x080755d4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_55d4', None),
    (0x08075660, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5660', None),
    (0x08075ca8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5ca8', None),
    (0x080761e0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_61e0', None),
    (0x080757e0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_57e0', None),
    (0x08075870, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5870', None),
    (0x080758e8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_58e8', None),
    (0x08075974, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5974', None),
    (0x080759b8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_59b8', None),
    (0x08075a74, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5a74', None),
    (0x08075ab8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5ab8', None),
    (0x08075b14, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5b14', None),

    # --- ewram.inc: gDuelCardCtxBase = 0x0201e2a0 (3 slots) ---
    (0x08075374, 0x0201e2a0, 'gDuelCardCtxBase',
     'gDuelCardCtxBase_pool_5374',
     'gDuelCardCtxBase: duel card activation context base'),
    (0x08075978, 0x0201e2a0, 'gDuelCardCtxBase',
     'gDuelCardCtxBase_pool_5978', None),
    (0x080759bc, 0x0201e2a0, 'gDuelCardCtxBase',
     'gDuelCardCtxBase_pool_59bc', None),

    # --- ewram.inc: gEquipZoneCountTable = 0x0201e1c8 (1 slot) ---
    (0x08075528, 0x0201e1c8, 'gEquipZoneCountTable',
     'equip_zone_count_table_pool_5528',
     'gEquipZoneCountTable: equip zone count tracking table base (EWRAM)'),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (6 slots) ---
    (0x0807552c, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_552c',
     'gDuelFieldSlots: duel field zone slot array base'),
    (0x080755d8, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_55d8', None),
    (0x08075664, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_5664', None),
    (0x08075cac, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_5cac', None),
    (0x080761e4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_61e4', None),
    (0x080757e4, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_57e4', None),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 (4 slots) ---
    (0x08075bc4, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_5bc4',
     'gDuelPhaseFlags: duel phase flags global'),
    (0x08075924, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_5924', None),
    (0x08075b10, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_5b10', None),
    (0x08076250, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_6250', None),

    # --- duel_field.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 (5 slots) ---
    (0x08075be8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_5be8',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter byte offset'),
    (0x08075c20, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_5c20', None),
    (0x08075a08, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_5a08', None),
    (0x08075a6c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_5a6c', None),

    # --- duel_field.inc: SLOT_CARD_SET_CODE_MASK = 0x00001fff (1 slot) ---
    (0x08075c28, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',
     'slot_card_set_code_mask_pool_5c28',
     'SLOT_CARD_SET_CODE_MASK: 13-bit card set code mask'),

    # --- gl_scrollbar.inc: SCROLLBAR_KEEP_BITS_8_0 = 0x000001ff (1 slot) ---
    (0x080757e8, 0x000001ff, 'SCROLLBAR_KEEP_BITS_8_0',
     'scrollbar_keep_bits_8_0_pool_57e8',
     'SCROLLBAR_KEEP_BITS_8_0: 9-bit zone slot field mask bits[8:0]'),

    # --- gl_scrollbar.inc: SCROLLBAR_CLEAR_BITS_14_6 = 0xffff803f (1 slot) ---
    (0x080757ec, 0xffff803f, 'SCROLLBAR_CLEAR_BITS_14_6',
     'scrollbar_clear_bits_14_6_pool_57ec',
     'SCROLLBAR_CLEAR_BITS_14_6: clears bits[14:6] in zone slot halfword'),

    # --- ewram.inc: gP1HandSlotArray = 0x0201c8f8 (3 slots) ---
    (0x080758ec, 0x0201c8f8, 'gP1HandSlotArray',
     'gP1HandSlotArray_pool_58ec',
     'gP1HandSlotArray: P1 hand slot array base (EWRAM)'),
    (0x08075abc, 0x0201c8f8, 'gP1HandSlotArray',
     'gP1HandSlotArray_pool_5abc', None),
    (0x08075b18, 0x0201c8f8, 'gP1HandSlotArray',
     'gP1HandSlotArray_pool_5b18', None),

    # --- duel_field.inc: lookup_equip_score_b_0x1b7 = 0x000001b7 (1 slot) ---
    (0x080759dc, 0x000001b7, 'lookup_equip_score_b_0x1b7',
     'lookup_equip_score_b_pool_59dc',
     'lookup_equip_score_b_0x1b7: equip score lookup offset 0x1b7'),

    # --- oam_attr.inc: OAM_EFFECT_SLOT_TILE_P1 = 0x00008056 (1 slot) ---
    (0x08075a70, 0x00008056, 'OAM_EFFECT_SLOT_TILE_P1',
     'oam_effect_slot_tile_p1_pool_5a70',
     'OAM_EFFECT_SLOT_TILE_P1: OAM attr tile code for effect slot P1 sprite'),

    # --- ewram.inc: gP1SlotSetCodeArray = 0x0201c740 (1 slot) ---
    (0x08075a78, 0x0201c740, 'gP1SlotSetCodeArray',
     'gP1SlotSetCodeArray_pool_5a78',
     'gP1SlotSetCodeArray: P1 slot set-code array base (EWRAM)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: 0 slots (all globals accessed via EQ pc-relative literal pool)
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    4 slots: 3 dispatch-stubs first-entry labels + 1 FS ROM ptr
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # DAT_08075414 -> emblem_dispatch_sub_stubs_5414
    # B2 first sub-stub entry point (emblem_of_dragon_destroyer sub-stubs)
    (0x08075414, 'emblem_dispatch_sub_stubs_5414',
     'B2 dispatch sub-stubs first entry; 6 targets via 29-entry raw ptr dispatch table '
     '(0x753a0..0x75413); base referenced from fn_eligible_emblem_of_dragon_destroyer pool'),

    # DWORD_08075c24 -> dispatch_eff_act_card_id_ptr_5c24
    # FS ROM ptr: 0x09e3f134 -> slot holds GBA ROM addr (0x09e3fXXX = FS data area)
    # Ruling A: RENAME_ONLY + ASCII EOL (no equate for FS ROM pointers)
    (0x08075c24, 'dispatch_eff_act_card_id_ptr_5c24',
     'FS ROM ptr=0x09e3f134; dereferences to card_id 0x1670 (unassigned slot); '
     'masked 0x1fff in dispatch_effect_activation_with_lp_counter state 0x7f'),

    # DAT_08075d5c -> magical_dim_dispatch_sub_stubs_5d5c
    # B4 first sub-stub entry point (magical_dimension sub-stubs)
    (0x08075d5c, 'magical_dim_dispatch_sub_stubs_5d5c',
     'B4 dispatch sub-stubs first entry; 9 targets via 9-entry raw ptr dispatch table '
     '(0x75d38..0x75d5b); base referenced from fn_eligible_magical_dimension pool'),

    # DAT_08075fe0 -> friendship_dispatch_sub_stubs_5fe0
    # B6 first sub-stub entry point (friendship sub-stubs)
    (0x08075fe0, 'friendship_dispatch_sub_stubs_5fe0',
     'B6 dispatch sub-stubs first entry; 6 targets via 9-entry raw ptr dispatch table '
     '(0x75fbc..0x75fdb); base referenced from fn_eligible_friendship pool'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    1 update: enqueue_effect_slot_sprites_all_players plate cleanup
#    Reviewer non-blocking note: gEffectSlots/gSlotData -> canonical names.
#    WARN/not-found treated as FAIL (report but do not block landing).
#    Text pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # enqueue_effect_slot_sprites_all_players @ 0x080754b8
    # Old informal: gEffectSlots=0x0201e1c8 -> canonical: gEquipZoneCountTable=0x0201e1c8
    (0x080754b8,
     'gEffectSlots=0x0201e1c8',
     'gEquipZoneCountTable=0x0201e1c8'),
    # Old informal: gSlotData=0x0201c510 -> canonical: gDuelFieldSlots=0x0201c510
    (0x080754b8,
     'gSlotData=0x0201c510',
     'gDuelFieldSlots=0x0201c510'),
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

def _apply_plate_fix(func_addr, old_text, new_text):
    """Replace old_text with new_text in existing plate comment. WARN/not-found = FAIL (reported)."""
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[FAIL] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[FAIL] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
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
    print("=== RefineF09Seg7Slots (DRY=%s) ===" % DRY)
    print("  Seg-7: 0x080752cc..0x0807629c  (19 fn)")
    print("  EQ=%d REF=%d RENAME=%d PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS (0 for this seg)
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    print("  (none in Seg-7)")

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES: informal name fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF09Seg7Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))


main()
