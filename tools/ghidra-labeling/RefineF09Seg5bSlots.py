# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5bSlots.py -- p5 file09 Seg-5b (0x08073a5c..0x08074338)
#   equip zone eligibility display + LP counter state machine
#   Functions: test_equip_target_slot_by_zone_descriptor_match /
#              enqueue_lp_counter_sprite_by_mode_and_player /
#              tick_equip_zone_sprite_and_lp_counter_state /
#              enqueue_zone_sprite_type5_from_slot /
#              tick_equip_zone_eligibility_display_state_seq /
#              tick_equip_lp_counter_display_state_seq /
#              enqueue_spirit_zone_sprite_type11
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (21 slots: 19 REUSE + 2 NEW)
#   B. REF_SLOTS  -- USER label on target + DATA ref + slot rename (4 slots)
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII)
#   D. PLATE_REWRITES -- FUN_ -> current name in plate comments (pure ASCII)
#
# Reviewer-verified corrections vs proposal:
#   - B7 dispatch table: 0x7c bytes / 31 entries (not 0x78/30)
#     -> 9 unique targets; disasm script handles all 9
#   - B8 PLATE: stale FUN_ at absolute asm line 11952 (not 11513)
#   - B9/B10: dispatch table confirmed by ROM read (29 entries / 0x74 bytes)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

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
#    Creates equate (value -> name) and references it from slot address.
#    Slot label MUST differ from eq_name to avoid GAS ldr/equate conflict.
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: gEquipChainSlotRefs = 0x0201bb90 (1 slot) ---
    (0x08073aac, 0x0201bb90, 'gEquipChainSlotRefs',
     'test_equip_target_slot_zone_desc_match_ptr_gequipchainslotref',
     'gEquipChainSlotRefs: equip chain slot reference array'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (6 slots) ---
    (0x08073ae4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_lp_counter_sprite_player_block_stride_ae4',
     'PLAYER_BLOCK_STRIDE: byte stride per player block in gDuelFieldSlots'),
    (0x08073b18, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'enqueue_lp_counter_sprite_player_block_stride_b18', None),
    (0x08073e8c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_elig_seq_player_block_stride_e8c', None),
    (0x08073fa0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_zone_elig_seq_player_block_stride_fa0', None),
    (0x080742b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_lp_counter_seq_player_block_stride_2b4', None),

    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 (4 slots) ---
    (0x08073da8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_sprite_lp_state_ptr_gduelphaseflags_da8', None),
    (0x08073ed8, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_elig_seq_ptr_gduelphaseflags_ed8', None),
    (0x08073fa4, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_zone_elig_seq_ptr_gduelphaseflags_fa4', None),
    (0x08074250, 0x0201b290, 'gDuelPhaseFlags',
     'tick_equip_lp_counter_seq_ptr_gduelphaseflags_250', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (1 slot) ---
    (0x08073e90, 0x0201c510, 'gDuelFieldSlots',
     'tick_equip_zone_elig_seq_ptr_gduelfieldslots_e90', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 (5 slots) ---
    (0x08073f0c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_elig_seq_phase_frame_off_f0c',
     'EQUIP_PHASE_FRAME_OFF: phase frame counter byte offset in equip state'),
    (0x08073f9c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_zone_elig_seq_phase_frame_off_f9c', None),
    (0x080742ac, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_lp_counter_seq_phase_frame_off_2ac', None),
    (0x080742d4, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_lp_counter_seq_phase_frame_off_2d4', None),
    (0x0807430c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'tick_equip_lp_counter_seq_phase_frame_off_30c', None),

    # --- ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x00001ce8 (1 slot) ---
    (0x08073f98, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8',
     'tick_equip_zone_elig_seq_p1lp_block2_off_f98',
     'P1LP_BLOCK2_OFF_1CE8: P1 LP display block 2 byte offset in gP1LifePoints'),

    # --- card_info.inc: RELOAD_CID = 0x000016d9 (NEW, 1 slot) ---
    (0x08074210, 0x000016d9, 'RELOAD_CID',
     'tick_equip_lp_counter_seq_reload_cid_210',
     'RELOAD_CID=0x16d9: Reload (pw=22589918; card-stats.s L18657); BST case'),

    # --- card_info.inc: DISTURBANCE_STRATEGY_CID = 0x000015aa (NEW, 1 slot) ---
    (0x08074214, 0x000015aa, 'DISTURBANCE_STRATEGY_CID',
     'tick_equip_lp_counter_seq_disturbance_cid_214',
     'DISTURBANCE_STRATEGY_CID=0x15aa: Disturbance Strategy (pw=77561728; card-stats.s L15563); BST case'),

    # --- card_info.inc: MIND_WIPE_CID = 0x000017f3 (REUSE, 2 slots) ---
    (0x0807422c, 0x000017f3, 'MIND_WIPE_CID',
     'tick_equip_lp_counter_seq_mind_wipe_cid_22c', None),
    (0x080742b8, 0x000017f3, 'MIND_WIPE_CID',
     'tick_equip_lp_counter_seq_mind_wipe_cid_2b8', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target, DATA ref from slot, renames slot.
#    All 4 slots point to gP1LifePoints = 0x0201c4e0.
#    The DWORD_ auto-label on these slots is eliminated by adding USER label.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gP1LifePoints = 0x0201c4e0 (4 slots -- label rename to eliminate DWORD_ def label)
    (0x08073ae0, 0x0201c4e0, 'gP1LifePoints',
     'enqueue_lp_counter_sprite_ptr_gp1lifepoints_ae0', None),
    (0x08073b14, 0x0201c4e0, 'gP1LifePoints',
     'enqueue_lp_counter_sprite_ptr_gp1lifepoints_b14', None),
    (0x08073f94, 0x0201c4e0, 'gP1LifePoints',
     'tick_equip_zone_elig_seq_ptr_gp1lifepoints_f94', None),
    (0x080742b0, 0x0201c4e0, 'gP1LifePoints',
     'tick_equip_lp_counter_seq_ptr_gp1lifepoints_2b0', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    Plain rename (add USER label) + optional EOL comment (pure ASCII).
#    These are DAT_ auto-named dispatch sub-stub blocks.
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x08073bc8, 'reasoning_dispatch_sub_stubs_3bc8',
     'Reasoning CID=0x159a dispatch sub-stubs'),
    (0x08074080, 'reversal_quiz_dispatch_sub_stubs_4080',
     'Reversal Quiz CID=0x15a5 dispatch sub-stubs'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    C8 stale FUN_ fixes -- all text pure ASCII.
#    WARN/not-found treated as FAIL (per refine-loop methodology).
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # C8 fix: enqueue_spirit_zone_sprite_type11 @ 0x08074318
    # Plate at asm absolute line ~11952: FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id
    (0x08074318,
     'FUN_08071d64',
     'dispatch_spirit_monster_zone_sprite_by_card_id'),
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

    # EOL comment
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
        return

    # create USER_DEFINED label at target if not already there
    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # add DATA ref from slot to target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    # set primary
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # create slot label
    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))

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
    """Replace old_text with new_text in existing plate comment at func_addr.
    Treat WARN/not-found as FAIL per refine-loop methodology."""
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
    print("=== RefineF09Seg5bSlots (DRY=%s) ===" % DRY)
    print("  Seg-5b: 0x08073a5c..0x08074338  (8 fn, B7-B10)")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_eq(slot_addr, value, eq_name, slot_label, eol)
        eq_ok += 1
    print("  EQ done: %d" % eq_ok)

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_vaddr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    ren_ok = 0
    for entry in RENAME_SLOTS:
        slot_addr, slot_label = entry[0], entry[1]
        eol = entry[2] if len(entry) > 2 else None
        _apply_rename(slot_addr, slot_label, eol)
        ren_ok += 1
    print("  RENAME done: %d" % ren_ok)

    # D. PLATE_REWRITES (FUN_ substitutions -- WARN=FAIL)
    print("\n--- D. PLATE_REWRITES: FUN_ fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF09Seg5bSlots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))

main()
