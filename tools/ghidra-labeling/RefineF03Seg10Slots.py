# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg10Slots.py -- file 03 Seg-10 (0x0803efcc..0x0804020c)
#   tick_zone_desc_card_move_display_seq .. tick_hand_zone_swap_display_seq
#   EQ=63 (60 reuse + 3 new), REF=57, RENAME=1, FUNC_RENAME=0, PLATE=9
#   carve=0, disasm=0, §5.1=0
#
# New constants added to .inc files before running this script:
#   card_info.inc: HELPOEMER_CID_SHIFTED=0xab880000
#   duel_field.inc: SLOT_CHAIN_CTR_CLR=0xc03fffff, SLOT_BIT20_CLR=0xffefffff
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
# Helpers
# ---------------------------------------------------------------------------

def _addr(val):
    return toAddr(val)

def _check(slot_addr, expected):
    addr = _addr(slot_addr)
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(addr) & 0xffffffff
        if actual != (expected & 0xffffffff):
            print("WARN: slot 0x%08x expected 0x%08x got 0x%08x -- SKIP" % (slot_addr, expected & 0xffffffff, actual))
            return False
        return True
    except Exception as e:
        print("WARN: slot 0x%08x read error: %s" % (slot_addr, e))
        return False

def _eq(slot_addr, value, eq_name, slot_label, eol=None):
    if not _check(slot_addr, value):
        return
    if DRY:
        print("DRY EQ: 0x%08x %s=%s sl=%s" % (slot_addr, eq_name, hex(value & 0xffffffff), slot_label))
        return
    addr = _addr(slot_addr)
    et = currentProgram.getEquateTable()
    eq = et.getEquate(eq_name)
    if eq is None:
        eq = et.createEquate(eq_name, value & 0xffffffff)
    eq.addReference(addr, 0)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(addr, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _ref(slot_addr, target_addr, gas_label, slot_label, eol=None):
    if DRY:
        print("DRY REF: 0x%08x -> 0x%08x gas=%s sl=%s" % (slot_addr, target_addr, gas_label, slot_label))
        return
    tgt = _addr(target_addr)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(tgt, gas_label, SourceType.USER_DEFINED)
    rm = currentProgram.getReferenceManager()
    src = _addr(slot_addr)
    rm.addMemoryReference(src, tgt, RefType.DATA, SourceType.USER_DEFINED, 0)
    ref_list = rm.getReferencesFrom(src)
    for r in ref_list:
        if r.getToAddress().equals(tgt):
            rm.setPrimary(r, True)
    sm.createLabel(src, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(src)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

def _rename(slot_addr, old_label, new_label, eol=None):
    if DRY:
        print("DRY RENAME: 0x%08x %s->%s" % (slot_addr, old_label, new_label))
        return
    addr = _addr(slot_addr)
    sm = currentProgram.getSymbolTable()
    syms = list(sm.getSymbols(addr))
    renamed = False
    for sym in syms:
        if sym.getName() == old_label:
            sym.setName(new_label, SourceType.USER_DEFINED)
            renamed = True
            break
    if not renamed:
        sm.createLabel(addr, new_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(addr)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

# ---------------------------------------------------------------------------
# A. EQ_SLOTS (63 total: 60 reuse + 3 new)
#
# Slot addresses taken verbatim from F03-Seg-10.proposal.md EQ table.
# All addresses are in segment [0x0803efcc, 0x0804020c).
# ---------------------------------------------------------------------------

# DISPLAY_SEQ_STEP_LOCK_OFF = 0x0000080c (20 slots)
# Slots: f0f8, f3d8, f57c, f614, f78c, f7d8, f824, f898, f944, fa34,
#        fc6c, fce4, fe20, fe6c, fe88, feb8, 080400f0, 8040140, 8040190, 8040208
EQ_STEP_LOCK = [
    0x0803f0f8, 0x0803f3d8, 0x0803f57c, 0x0803f614, 0x0803f78c,
    0x0803f7d8, 0x0803f824, 0x0803f898, 0x0803f944, 0x0803fa34,
    0x0803fc6c, 0x0803fce4, 0x0803fe20, 0x0803fe6c, 0x0803fe88,
    0x0803feb8, 0x080400f0, 0x08040140, 0x08040190, 0x08040208,
]

# PLAYER_BLOCK_STRIDE = 0x00000868 (15 slots)
# Slots: f098, f350, f494, f578, f760, f818, f904, f9f4, fbfc, fc60, fce0, fda4, feb4, 8040028, 80400ec
EQ_STRIDE = [
    0x0803f098, 0x0803f350, 0x0803f494, 0x0803f578, 0x0803f760,
    0x0803f818, 0x0803f904, 0x0803f9f4, 0x0803fbfc, 0x0803fc60,
    0x0803fce0, 0x0803fda4, 0x0803feb4, 0x08040028, 0x080400ec,
]

# GPRNG_STEP_CTR_MASK = 0xffffc03f (4 slots)
# Slots: f360, fb38, fdb0, 8040003c
EQ_STEP_CTR = [
    0x0803f360, 0x0803fb38, 0x0803fdb0, 0x0804003c,
]

# SLOT_ACTIVE_BIT15_CLR = 0xffff7fff (4 slots)
# Slots: f364, fb40, fdb4, 8040040
EQ_BIT15 = [
    0x0803f364, 0x0803fb40, 0x0803fdb4, 0x08040040,
]

# SLOT_ACTIVE_BIT14_CLR = 0xffffbfff (4 slots)
# Slots: f368, fb3c, fbf0, fdb8
EQ_BIT14 = [
    0x0803f368, 0x0803fb3c, 0x0803fbf0, 0x0803fdb8,
]

# SOUL_ABSORPTION_CID = 0x000016da (2 slots)
# Slots: f354, 804002c
EQ_SOUL_ABS = [0x0803f354, 0x0804002c]

# SLOT_CARD_SET_CODE_MASK = 0x00001fff (2 slots)
# Slots: fb44, fbe8
EQ_SET_CODE = [0x0803fb44, 0x0803fbe8]

# OAM_ATTR2_TILE_CLEAR = 0xffffe000 (2 slots)
# Slots: fb48, fbec
EQ_OAM_CLR = [0x0803fb48, 0x0803fbec]

# DUEL_FIELD_OAM_TILE_IDX_A = 0x00000814 (2 slots)
# Slots: fe84, 8040090
EQ_OAM_TILE = [0x0803fe84, 0x08040090]

# Single-slot reuse constants
EQ_SINGLE = [
    (0x0803f348, 0xfffe7fff, 'SLOT_BITS14_15_CLR',       'seg10_bits14_15_clr_a'),
    (0x0803f574, 0x00001cf4, 'FIELD_STATE_OFF',           'seg10_field_state_off_a'),
    (0x0803fc00, 0xffdfffff, 'SLOT_BIT21_CLR',            'seg10_slot_bit21_clr_a'),
    (0x0803fe18, 0x000010d0, 'EFFECT_ZONE_BITMASK_OFF',   'seg10_effect_zone_mask_a'),
    (0x08040024, 0x00000818, 'DISP_SEQ_CARD_SET_CTR_OFF', 'seg10_card_set_ctr_off_a'),
    # New constants
    (0x0803f874, 0xab880000, 'HELPOEMER_CID_SHIFTED',     'seg10_helpoemer_shifted_a'),
    (0x0803fbf4, 0xc03fffff, 'SLOT_CHAIN_CTR_CLR',        'seg10_chain_ctr_clr_a'),
    (0x0803fc64, 0xffefffff, 'SLOT_BIT20_CLR',            'seg10_slot_bit20_clr_a'),
]

def _suffix(addr):
    return "%08x" % addr

EQ_SLOTS = []
for a in EQ_STEP_LOCK:
    EQ_SLOTS.append((a, 0x0000080c, 'DISPLAY_SEQ_STEP_LOCK_OFF',
                     'seg10_step_lock_%s' % _suffix(a), None))
for a in EQ_STRIDE:
    EQ_SLOTS.append((a, 0x00000868, 'PLAYER_BLOCK_STRIDE',
                     'seg10_stride_%s' % _suffix(a), None))
for a in EQ_STEP_CTR:
    EQ_SLOTS.append((a, 0xffffc03f, 'GPRNG_STEP_CTR_MASK',
                     'seg10_step_ctr_%s' % _suffix(a), None))
for a in EQ_BIT15:
    EQ_SLOTS.append((a, 0xffff7fff, 'SLOT_ACTIVE_BIT15_CLR',
                     'seg10_bit15_clr_%s' % _suffix(a), None))
for a in EQ_BIT14:
    EQ_SLOTS.append((a, 0xffffbfff, 'SLOT_ACTIVE_BIT14_CLR',
                     'seg10_bit14_clr_%s' % _suffix(a), None))
for a in EQ_SOUL_ABS:
    EQ_SLOTS.append((a, 0x000016da, 'SOUL_ABSORPTION_CID',
                     'seg10_soul_abs_%s' % _suffix(a), None))
for a in EQ_SET_CODE:
    EQ_SLOTS.append((a, 0x00001fff, 'SLOT_CARD_SET_CODE_MASK',
                     'seg10_set_code_%s' % _suffix(a), None))
for a in EQ_OAM_CLR:
    EQ_SLOTS.append((a, 0xffffe000, 'OAM_ATTR2_TILE_CLEAR',
                     'seg10_oam_tile_clr_%s' % _suffix(a), None))
for a in EQ_OAM_TILE:
    EQ_SLOTS.append((a, 0x00000814, 'DUEL_FIELD_OAM_TILE_IDX_A',
                     'seg10_oam_tile_idx_%s' % _suffix(a), None))
for (a, v, n, sl) in EQ_SINGLE:
    EQ_SLOTS.append((a, v, n, sl, None))

# ---------------------------------------------------------------------------
# B. REF_SLOTS (57 total)
# ---------------------------------------------------------------------------
REF_SLOTS = [

    # === gDuelDisplaySeqState = 0x0201bcc0 (26 slots) ===
    # Slots from proposal: eff8, f034, f09c, f0f4, f3ac, f3d4, f430, f51c,
    #   f5ac, f64c, f764, f7c0, f820, f878, f900, f994,
    #   fa30, fb34, fc68, fc98, fe1c, fe68, 080400cc, 0804018c, 080401d8, 08040204

    (0x0803eff8, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803eff8', None),
    (0x0803f034, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f034', None),
    (0x0803f09c, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f09c', None),
    (0x0803f0f4, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f0f4', None),
    (0x0803f3ac, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f3ac', None),
    (0x0803f3d4, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f3d4', None),
    (0x0803f430, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f430', None),
    (0x0803f51c, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f51c', None),
    (0x0803f5ac, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f5ac', None),
    (0x0803f64c, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f64c', None),
    (0x0803f764, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f764', None),
    (0x0803f7c0, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f7c0', None),
    (0x0803f820, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f820', None),
    (0x0803f878, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f878', None),
    (0x0803f900, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f900', None),
    (0x0803f994, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803f994', None),
    (0x0803fa30, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803fa30', None),
    (0x0803fb34, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803fb34', None),
    (0x0803fc68, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803fc68', None),
    (0x0803fc98, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803fc98', None),
    (0x0803fe1c, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803fe1c', None),
    (0x0803fe68, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0803fe68', None),
    (0x080400cc, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_080400cc', None),
    (0x0804018c, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_0804018c', None),
    (0x080401d8, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_080401d8', None),
    (0x08040204, 0x0201bcc0, 'gDuelDisplaySeqState', 'seg10_disp_seq_state_08040204', None),

    # === gP1LifePoints = 0x0201c4e0 (12 PTR_ slots) ===
    # Slots: f094, f36c, f490, f570, f870, fb4c, fbf8, fcdc, fe14, feb0, 080400e8, 0804013c

    (0x0803f094, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803f094', None),
    (0x0803f36c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803f36c', None),
    (0x0803f490, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803f490', None),
    (0x0803f570, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803f570', None),
    (0x0803f870, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803f870', None),
    (0x0803fb4c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803fb4c', None),
    (0x0803fbf8, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803fbf8', None),
    (0x0803fcdc, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803fcdc', None),
    (0x0803fe14, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803fe14', None),
    (0x0803feb0, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0803feb0', None),
    (0x080400e8, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_080400e8', None),
    (0x0804013c, 0x0201c4e0, 'gP1LifePoints', 'PTR_gP1LifePoints_0804013c', None),

    # === gDuelFieldSlots = 0x0201c510 (6 slots) ===
    # Slots: f358, f75c, f81c, f908, f9f8, 8040030

    (0x0803f358, 0x0201c510, 'gDuelFieldSlots', 'seg10_field_slots_0803f358', None),
    (0x0803f75c, 0x0201c510, 'gDuelFieldSlots', 'seg10_field_slots_0803f75c', None),
    (0x0803f81c, 0x0201c510, 'gDuelFieldSlots', 'seg10_field_slots_0803f81c', None),
    (0x0803f908, 0x0201c510, 'gDuelFieldSlots', 'seg10_field_slots_0803f908', None),
    (0x0803f9f8, 0x0201c510, 'gDuelFieldSlots', 'seg10_field_slots_0803f9f8', None),
    (0x08040030, 0x0201c510, 'gDuelFieldSlots', 'seg10_field_slots_08040030', None),

    # === gDuelChainDescBase = 0x0201c4d8 (5 slots) ===
    # Slots: f34c, f3a8, fdac, 8040038, 8040078

    (0x0803f34c, 0x0201c4d8, 'gDuelChainDescBase', 'seg10_chain_desc_0803f34c', None),
    (0x0803f3a8, 0x0201c4d8, 'gDuelChainDescBase', 'seg10_chain_desc_0803f3a8', None),
    (0x0803fdac, 0x0201c4d8, 'gDuelChainDescBase', 'seg10_chain_desc_0803fdac', None),
    (0x08040038, 0x0201c4d8, 'gDuelChainDescBase', 'seg10_chain_desc_08040038', None),
    (0x08040078, 0x0201c4d8, 'gDuelChainDescBase', 'seg10_chain_desc_08040078', None),

    # === gDuelChainStepCounter = 0x0201c4d0 (4 slots) ===
    # Slots: fc9c, fcd8, fdc0, fdd8

    (0x0803fc9c, 0x0201c4d0, 'gDuelChainStepCounter', 'seg10_chain_step_ctr_0803fc9c', None),
    (0x0803fcd8, 0x0201c4d0, 'gDuelChainStepCounter', 'seg10_chain_step_ctr_0803fcd8', None),
    (0x0803fdc0, 0x0201c4d0, 'gDuelChainStepCounter', 'seg10_chain_step_ctr_0803fdc0', None),
    (0x0803fdd8, 0x0201c4d0, 'gDuelChainStepCounter', 'seg10_chain_step_ctr_0803fdd8', None),

    # === gDuelCardCtxBase = 0x0201e2a0 (2 slots) ===
    # Slots: f35c, 8040034

    (0x0803f35c, 0x0201e2a0, 'gDuelCardCtxBase', 'seg10_card_ctx_0803f35c', None),
    (0x08040034, 0x0201e2a0, 'gDuelCardCtxBase', 'seg10_card_ctx_08040034', None),

    # === gP1SlotSetCodeArray = 0x0201c740 (1 slot) ===
    # Slot: fda8

    (0x0803fda8, 0x0201c740, 'gP1SlotSetCodeArray', 'seg10_set_code_arr_0803fda8', None),

    # === gP1ZoneHandCount = 0x0201c4ec (1 slot) ===
    # Slot: fdbc

    (0x0803fdbc, 0x0201c4ec, 'gP1ZoneHandCount', 'seg10_hand_count_0803fdbc', None),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS (1 total)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0803f038, 'DAT_0803f038', 'zone_desc_move_switch_table_ptr',
     'ptr to switchD_0803f030__switchdataD_0803f03c; dispatch in tick_zone_desc_card_move_display_seq'),
]

# ---------------------------------------------------------------------------
# D. PLATE_FIXES (9 functions, 10 stale-FUN_ substring occurrences)
#   FUN_0803be4c -> dispatch_duel_event_display_seq  (9 occurrences)
#   FUN_08031668 -> shuffle_player_hand_list          (1 occurrence, in fix 7)
# ---------------------------------------------------------------------------

def _get_plate(addr_int):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        return None
    return cu.getComment(CodeUnit.PLATE_COMMENT)

def _set_plate(addr_int, text):
    cu = currentProgram.getListing().getCodeUnitAt(_addr(addr_int))
    if cu is None:
        print("WARN: no code unit at 0x%08x for plate" % addr_int)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    return True

def _plate_subst(addr_int, old_str, new_str, fix_label):
    old_text = _get_plate(addr_int)
    if old_text is None:
        print("WARN: no plate at 0x%08x (%s)" % (addr_int, fix_label))
        return
    if old_str in old_text:
        new_text = old_text.replace(old_str, new_str)
        if DRY:
            print("DRY PLATE %s: 0x%08x %s->%s" % (fix_label, addr_int, old_str, new_str))
        else:
            _set_plate(addr_int, new_text)
            print("PLATE %s ok: 0x%08x" % (fix_label, addr_int))
    else:
        print("PLATE %s: '%s' not found at 0x%08x (already fixed?)" % (fix_label, old_str, addr_int))

def apply_plate_fixes():
    # Fix 1: tick_card_display_op41_multi_seq @ 0x0803f580
    _plate_subst(0x0803f580, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix1")

    # Fix 2: tick_card_display_seq_op41 @ 0x0803f618
    _plate_subst(0x0803f618, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix2")

    # Fix 3: tick_zone_slot_equip_detach_display_seq @ 0x0803f790
    _plate_subst(0x0803f790, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix3")

    # Fix 4: tick_equip_link_display_seq @ 0x0803f89c
    _plate_subst(0x0803f89c, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix4")

    # Fix 5: tick_dual_list_slot_find_display_seq @ 0x0803f948
    _plate_subst(0x0803f948, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix5")

    # Fix 6: tick_equip_detach_sequence @ 0x0803fc70
    _plate_subst(0x0803fc70, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix6")

    # Fix 7a: tick_hand_shuffle_display_seq @ 0x080400a8
    _plate_subst(0x080400a8, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix7a")
    # Fix 7b: FUN_08031668 -> shuffle_player_hand_list
    _plate_subst(0x080400a8, "FUN_08031668", "shuffle_player_hand_list", "fix7b")

    # Fix 8: tick_hand_sort_display_init_seq @ 0x08040144
    _plate_subst(0x08040144, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix8")

    # Fix 9: tick_hand_zone_swap_display_seq @ 0x08040194
    _plate_subst(0x08040194, "FUN_0803be4c", "dispatch_duel_event_display_seq", "fix9")


# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------

print("=== RefineF03Seg10Slots.py DRY=%s ===" % DRY)

for (sa, val, eqn, sl, eol) in EQ_SLOTS:
    _eq(sa, val, eqn, sl, eol)

print("EQ done: %d slots" % len(EQ_SLOTS))

for (sa, ta, gl, sl, eol) in REF_SLOTS:
    _ref(sa, ta, gl, sl, eol)

print("REF done: %d slots" % len(REF_SLOTS))

for (sa, ol, nl, eol) in RENAME_SLOTS:
    _rename(sa, ol, nl, eol)

print("RENAME done: %d slots" % len(RENAME_SLOTS))

apply_plate_fixes()
print("PLATE done: 9 fixes (10 FUN_ occurrences)")

print("=== COMPLETE: EQ=%d REF=%d RENAME=%d PLATE=9 DRY=%s ===" % (
    len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), DRY))
