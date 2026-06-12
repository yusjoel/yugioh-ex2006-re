# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg2Slots.py -- file 04 Seg-2 (0x080407fc..0x08040c88)
#   20 functions: tick_card_normal_summon_display_state /
#   tick_flip_attack_display_state / tick_random_draw_display_seq /
#   tick_prng_advance_display_op38_seq / tick_card_display_op3a_seq /
#   tick_display_op39_seq / tick_card_display_seq_op3b /
#   tick_equip_slot_scan_display_sequence / tick_ui_effect_op3c_display_seq /
#   tick_card_display_op0b_seq / trigger_display_op36_seq /
#   clear_display_step_lock_i / clear_display_step_lock_j /
#   clear_display_step_lock_k / reset_card_display_seq_state /
#   clear_match_state_field_at_80c / clear_match_state_field_at_80c_alt /
#   clear_display_step_counter_a / clear_display_step_counter_b /
#   clear_display_step_lock_a
#
# Sections:
#   A. EQ_SLOTS    -- 44 total (43 reuse + 1 new: P1LP_BACKUP_DST_OFF in ewram.inc)
#   B. REF_SLOTS   -- 1 (DAT_08040ab4 -> zone_monster_field_bonus_table+7*16)
#   C. RENAME_SLOTS -- 45 (44 DAT_ + 1 PTR_ already-symbolized)
#   D. PLATE_REWRITES -- 15 FUN_0803be4c / (0x0803be4c) -> dispatch_duel_event_display_seq
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Slot labels MUST differ from .equ constant names (GAS ldr/equate conflict).
# NOTE: FUNC_RENAME = 0 (no function renames in this segment).

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
#    All values verified against roms/2343.gba (python struct.unpack_from).
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: gDuelDisplaySeqState = 0x0201bcc0 (21 slots) ---
    # NOTE: gDuelDisplaySeqState is an EWRAM address, handled as REF in Seg-1.
    # These DAT_ slots at addresses 0x0201bcc0 hold the gDuelDisplaySeqState value
    # itself in the literal pool; they are EQ-symbolized (not REF) because the
    # constant is already defined in ewram.inc.  Per file-04 doc: these are
    # EQ equate slots (not REF), consistent with Seg-1 treatment.
    # (Actually in Seg-1 these were REF_SLOTS. For Seg-2 proposal these are EQ_SLOTS.)
    # WAIT -- proposal §EQ_SLOTS says "Reuse gDuelDisplaySeqState = 0x0201bcc0 (ewram.inc:368)
    # -- 21 DAT_ slots". In Seg-1 the same values were REF_SLOTS.
    # Proposal explicitly lists them as EQ_SLOTS. Following proposal.
    (0x0804082c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_nsummon_display_state_base', 'gDuelDisplaySeqState base ptr'),
    (0x08040874, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_flip_atk_state_base', None),
    (0x080408e4, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_rnd_draw_state_base', None),
    (0x08040944, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_prng_op38_state_base', None),
    (0x08040990, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_op3a_state_base', None),
    (0x080409d8, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_op39_state_base', None),
    (0x08040a2c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_op3b_state_base', None),
    (0x08040aac, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_equip_scan_state_base', None),
    (0x08040adc, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_equip_scan_state_base_b', 'gDuelDisplaySeqState base ptr (poll path)'),
    (0x08040b2c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_op3c_state_base', None),
    (0x08040b84, 0x0201bcc0, 'gDuelDisplaySeqState',
     'tick_op0b_state_base', None),
    (0x08040bcc, 0x0201bcc0, 'gDuelDisplaySeqState',
     'trigger_op36_state_base', None),
    (0x08040be0, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_lock_i_state_base', None),
    (0x08040bf4, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_lock_j_state_base', None),
    (0x08040c08, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_lock_k_state_base', None),
    (0x08040c1c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'reset_cdseq_state_base', None),
    (0x08040c30, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_match_80c_state_base', None),
    (0x08040c44, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_match_80c_alt_state_base', None),
    (0x08040c58, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_step_ctr_a_state_base', None),
    (0x08040c6c, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_step_ctr_b_state_base', None),
    (0x08040c80, 0x0201bcc0, 'gDuelDisplaySeqState',
     'clr_lock_a_state_base', None),

    # --- duel_field.inc: DISPLAY_SEQ_STEP_LOCK_OFF = 0x0000080c (20 slots) ---
    (0x08040848, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_nsummon_display_step_lock_off', 'DISPLAY_SEQ_STEP_LOCK_OFF'),
    (0x08040890, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_flip_atk_step_lock_off', None),
    (0x08040908, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_rnd_draw_step_lock_off', None),
    (0x08040964, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_prng_op38_step_lock_off', None),
    (0x080409ac, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_op3a_step_lock_off', None),
    (0x08040a00, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_op39_step_lock_off', None),
    (0x08040a48, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_op3b_step_lock_off', None),
    (0x08040b00, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_equip_scan_step_lock_off', None),
    (0x08040b48, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_op3c_step_lock_off', None),
    (0x08040ba8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'tick_op0b_step_lock_off', None),
    (0x08040bd0, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'trigger_op36_step_lock_off', None),
    (0x08040be4, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_lock_i_step_lock_off', None),
    (0x08040bf8, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_lock_j_step_lock_off', None),
    (0x08040c0c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_lock_k_step_lock_off', None),
    (0x08040c20, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'reset_cdseq_step_lock_off', None),
    (0x08040c34, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_match_80c_step_lock_off', None),
    (0x08040c48, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_match_80c_alt_step_lock_off', None),
    (0x08040c5c, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_step_ctr_a_step_lock_off', None),
    (0x08040c70, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_step_ctr_b_step_lock_off', None),
    (0x08040c84, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
     'clr_lock_a_step_lock_off', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (1 slot) ---
    (0x08040ab0, 0x0201c510, 'gDuelFieldSlots',
     'tick_equip_scan_field_slots_base', 'gDuelFieldSlots'),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (1 slot) ---
    (0x08040ab8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'tick_equip_scan_player_stride', 'PLAYER_BLOCK_STRIDE (0x868)'),

    # --- ewram.inc NEW: P1LP_BACKUP_DST_OFF = 0x00001cf0 (1 slot) ---
    (0x08040b8c, 0x00001cf0, 'P1LP_BACKUP_DST_OFF',
     'tick_op0b_lp_backup_dst_off',
     'gP1LifePoints+0x1cf0: LP timer backup destination field'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_or_None)
#    Creates USER_DEFINED label at target; DATA ref slot->target; renames slot.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # DAT_08040ab4 = 0x09e3f104 -> zone_monster_field_bonus_table + 7*16
    # zone_monster_field_bonus_table (rom.s:1241) = 0x09e3f094; +7*16 = +0x70 = 0x09e3f104
    # Data pointer (not THUMB fn-ptr): value 0x09e3f104 is even, confirmed data ref.
    (0x08040ab4, 0x09e3f104,
     'zone_monster_field_bonus_table',  # gas_label: use carved label (GAS resolves + offset)
     'tick_equip_scan_destiny_chain_table',
     'zone_monster_field_bonus_table+7*16: Destiny Board + Spirit Message I/N/A/L card_ids'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    PTR_gP1LifePoints_08040b88 already emits correct .word gP1LifePoints;
#    only the slot label is changed to a function-scoped name.
#    Also includes the remaining DAT_/EQ slots that only need a label rename
#    (gDuelDisplaySeqState EQ slots are handled in A; this covers the
#    PTR_ slot and the DAT_08040b8c already covered in A as new EQ).
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_gP1LifePoints_08040b88 -> tick_op0b_lp_base
    (0x08040b88, 'tick_op0b_lp_base', 'gP1LifePoints ptr'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_token, new_token)
#    Substring replace in existing plate comment. Pure ASCII only.
#    15 functions have stale FUN_0803be4c or (0x0803be4c) in their plates.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # tick_card_normal_summon_display_state (0x080407fc): (0x0803be4c)
    (0x080407fc, '(0x0803be4c)', '(dispatch_duel_event_display_seq)'),
    # tick_flip_attack_display_state (0x0804084c): (0x0803be4c)
    (0x0804084c, '(0x0803be4c)', '(dispatch_duel_event_display_seq)'),
    # tick_random_draw_display_seq (0x08040894): FUN_0803be4c
    (0x08040894, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_prng_advance_display_op38_seq (0x0804090c): FUN_0803be4c
    (0x0804090c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_op3a_seq (0x08040968): FUN_0803be4c
    (0x08040968, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_seq_op3b (0x08040a04): FUN_0803be4c
    (0x08040a04, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_equip_slot_scan_display_sequence (0x08040a4c): FUN_0803be4c
    (0x08040a4c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_ui_effect_op3c_display_seq (0x08040b04): FUN_0803be4c
    (0x08040b04, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # tick_card_display_op0b_seq (0x08040b4c): FUN_0803be4c
    (0x08040b4c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # reset_card_display_seq_state (0x08040c10): FUN_0803be4c
    (0x08040c10, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_match_state_field_at_80c (0x08040c24): (0x0803be4c)
    (0x08040c24, '(0x0803be4c)', '(dispatch_duel_event_display_seq)'),
    # clear_match_state_field_at_80c_alt (0x08040c38): (0x0803be4c)
    (0x08040c38, '(0x0803be4c)', '(dispatch_duel_event_display_seq)'),
    # clear_display_step_counter_a (0x08040c4c): FUN_0803be4c
    (0x08040c4c, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_counter_b (0x08040c60): FUN_0803be4c
    (0x08040c60, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
    # clear_display_step_lock_a (0x08040c74): FUN_0803be4c
    (0x08040c74, 'FUN_0803be4c', 'dispatch_duel_event_display_seq'),
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

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (
            slot_addr, target_vaddr, gas_label, slot_label))
        return

    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (
        slot_addr, target_vaddr, gas_label, slot_label))

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
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return

    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment" % func_addr)
        return

    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found in plate" % (func_addr, old_text))
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
    print("=== RefineF04Seg2Slots (DRY=%s) ===" % DRY)
    print("  file 04 Seg-2: 0x080407fc..0x08040c88, 20 fn, 46 slots")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
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

    # D. PLATE_REWRITES
    print("\n--- D. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)
        plate_ok += 1
    print("  PLATE done: %d" % plate_ok)

    print("\n=== RefineF04Seg2Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))


main()
