# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg6Slots.py -- p5 file09 Seg-6 (0x08074338..0x080752cc)
#   equip zone dispatch + fn_eligible + LP display state machines
#   20 functions including dispatch_equip_zone_bitmap_or_neo_daedalus_sprite,
#   tick_equip_activation_lp_display_seq, tick_equip_oam_display_by_state_7x,
#   tick_equip_display_seq_when_fewer_monster_zones, dispatch_equip_display_state_by_code
#
# Sections:
#   A. EQ_SLOTS   -- data-equate (55 slots: all REUSE)
#   B. REF_SLOTS  -- USER label + DATA ref + slot rename (5 slots)
#   C. RENAME_SLOTS -- plain rename + optional EOL (pure ASCII) (5 slots)
#   D. PLATE_REWRITES -- FUN_ -> current name in plate comments (pure ASCII) (1 entry)
#
# New constants added to constants/*.inc before this script:
#   card_info.inc: DIMENSION_JAR_CID = 0x000015dd
#   ewram.inc:     gEquipLpActivBitmap = 0x0201e220
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: DWORD_08074d4c has THUMB+1 value 0x080507ad (odd, correct).

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
#    55 slots, all REUSE (0 NEW in this section)
# ---------------------------------------------------------------------------
EQ_SLOTS = [
    # --- ewram.inc: gDuelPhaseFlags = 0x0201b290 (12 slots) ---
    (0x08074428, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4428', 'gDuelPhaseFlags: duel phase flags global'),
    (0x08074640, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4640', None),
    (0x080749fc, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_49fc', None),
    (0x08074b28, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4b28', None),
    (0x08074b60, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4b60', None),
    (0x08074d20, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4d20', None),
    (0x08074dac, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4dac', None),
    (0x08074e90, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_4e90', None),
    (0x0807514c, 0x0201b290, 'gDuelPhaseFlags',
     'gDuelPhaseFlags_pool_514c', None),

    # --- ewram.inc: PLAYER_BLOCK_STRIDE = 0x00000868 (13 slots) ---
    (0x0807442c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_442c', 'PLAYER_BLOCK_STRIDE: byte stride per player data block'),
    (0x080745b4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_45b4', None),
    (0x080746e4, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_46e4', None),
    (0x08074758, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_4758', None),
    (0x080747f8, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_47f8', None),
    (0x08074c04, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_4c04', None),
    (0x08074c80, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_4c80', None),
    (0x08074ce0, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_4ce0', None),
    (0x08074f30, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_4f30', None),
    (0x0807506c, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_506c', None),
    (0x08075204, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5204', None),
    (0x08075280, 0x00000868, 'PLAYER_BLOCK_STRIDE',
     'player_block_stride_pool_5280', None),

    # --- ewram.inc: gDuelFieldSlots = 0x0201c510 (8 slots) ---
    (0x08074430, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_4430', 'gDuelFieldSlots: duel field zone slot array base'),
    (0x080745b8, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_45b8', None),
    (0x0807475c, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_475c', None),
    (0x080747fc, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_47fc', None),
    (0x08074c08, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_4c08', None),
    (0x08074c84, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_4c84', None),
    (0x08074f34, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_4f34', None),
    (0x08075070, 0x0201c510, 'gDuelFieldSlots',
     'gDuelFieldSlots_pool_5070', None),

    # --- ewram.inc: EQUIP_PHASE_FRAME_OFF = 0x000004a4 (11 slots) ---
    (0x08074434, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4434',
     'EQUIP_PHASE_FRAME_OFF: equip phase frame counter byte offset'),
    (0x08074484, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4484', None),
    (0x080744ec, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_44ec', None),
    (0x08074644, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4644', None),
    (0x08074688, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4688', None),
    (0x080746e0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_46e0', None),
    (0x08074c00, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4c00', None),
    (0x08074c38, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4c38', None),
    (0x08074e94, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4e94', None),
    (0x08074f2c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4f2c', None),
    (0x08074f6c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF',
     'equip_phase_frame_off_pool_4f6c', None),

    # --- duel_field.inc: EQUIP_ZONE_SPRITE_ATTR = 0x00000fb6 (6 slots) ---
    (0x080744f0, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR',
     'equip_zone_sprite_attr_pool_44f0',
     'EQUIP_ZONE_SPRITE_ATTR: OAM attr for equip zone sprite enqueue'),
    (0x08074bfc, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR',
     'equip_zone_sprite_attr_pool_4bfc', None),
    (0x08074c3c, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR',
     'equip_zone_sprite_attr_pool_4c3c', None),
    (0x08074e8c, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR',
     'equip_zone_sprite_attr_pool_4e8c', None),
    (0x08074f28, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR',
     'equip_zone_sprite_attr_pool_4f28', None),
    (0x08074f70, 0x00000fb6, 'EQUIP_ZONE_SPRITE_ATTR',
     'equip_zone_sprite_attr_pool_4f70', None),

    # --- ewram.inc: gDuelCardCtxBase = 0x0201e2a0 (2 slots) ---
    (0x080744f4, 0x0201e2a0, 'gDuelCardCtxBase',
     'gDuelCardCtxBase_pool_44f4', 'gDuelCardCtxBase: duel card activation context base'),
    (0x08074e98, 0x0201e2a0, 'gDuelCardCtxBase',
     'gDuelCardCtxBase_pool_4e98', None),

    # --- ewram.inc: LP_CARD_TRACK_BASE_OFF = 0x00001da8 (2 slots) ---
    (0x08074a4c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_off_pool_4a4c',
     'LP_CARD_TRACK_BASE_OFF: LP card tracking base byte offset'),
    (0x08074d6c, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF',
     'lp_card_track_base_off_pool_4d6c', None),

    # --- ewram.inc: LP_CARD_TRACK_NEXT_OFF = 0x00001daa (1 slot) ---
    (0x08074a50, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF',
     'lp_card_track_next_off_pool_4a50',
     'LP_CARD_TRACK_NEXT_OFF: LP card tracking next byte offset'),

    # --- ewram.inc: ELIGIB_SPRITE_CTRL_OFF = 0x00001d68 (1 slot) ---
    (0x08074ae0, 0x00001d68, 'ELIGIB_SPRITE_CTRL_OFF',
     'eligib_sprite_ctrl_off_pool_4ae0',
     'ELIGIB_SPRITE_CTRL_OFF: eligibility sprite control byte offset'),

    # --- ewram.inc: ELIGIB_ANIM_STATE_OFF = 0x00001d6c (1 slot) ---
    (0x08074ae4, 0x00001d6c, 'ELIGIB_ANIM_STATE_OFF',
     'eligib_anim_state_off_pool_4ae4',
     'ELIGIB_ANIM_STATE_OFF: eligibility anim state byte offset'),

    # --- oam_attr.inc: OAM_EQUIP_SPRITE_TILE_P2_1B = 0x0000801b (1 slot) ---
    (0x08074c88, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B',
     'oam_equip_sprite_tile_p2_1b_pool_4c88',
     'OAM_EQUIP_SPRITE_TILE_P2_1B: OAM attr0 equip sprite tile P2 (bit15+0x1b)'),

    # --- ewram.inc: gEquipZoneCountTable = 0x0201e1c8 (1 slot) ---
    (0x080750bc, 0x0201e1c8, 'gEquipZoneCountTable',
     'equip_zone_count_table_pool_50bc',
     'gEquipZoneCountTable: equip zone count tracking table base (EWRAM)'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_vaddr, gas_label, slot_label, eol_or_None)
#    5 slots: 4x gP1LifePoints + 1x gEquipLpActivBitmap (NEW global)
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # gP1LifePoints = 0x0201c4e0 (4 slots)
    (0x08074a48, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_4a48',
     'gP1LifePoints: P1 LP tracking block base (EWRAM)'),
    (0x08074adc, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_4adc', None),
    (0x08074cdc, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_4cdc', None),
    (0x08074d68, 0x0201c4e0, 'gP1LifePoints',
     'gP1LifePoints_pool_4d68', None),

    # gEquipLpActivBitmap = 0x0201e220 (NEW -- 3 ROM refs total; this is first)
    (0x08074ab0, 0x0201e220, 'gEquipLpActivBitmap',
     'equip_lp_activ_bitmap_pool_4ab0',
     'gEquipLpActivBitmap=0x0201e220: LP activation zone-hit bitmap (EWRAM); 3 ROM refs'),
]

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: (slot_addr, slot_label, eol_ascii_or_None)
#    5 slots: dispatch table label, Block2 stubs label, 2 fn-ptr+1 slots, switchD ptr
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_DAT_080748a0 -> equip_zone_dispatch_table_48a0
    # 29-entry raw-ptr dispatch table; base ref'd from fn_eligible_dimension_jar pool @0x7489c
    (0x080748a0, 'equip_zone_dispatch_table_48a0',
     '29-entry raw ptr dispatch table for equip zone sub-stubs; '
     'base referenced from fn_eligible_dimension_jar literal pool @0x7489c; '
     'entries: [0]=sub_9b8 [1..24]=epilogue_9d4 [25]=sub_964 [26]=sub_948 [27]=sub_920 [28]=sub_914'),

    # DAT_08074914 -> equip_zone_sub_stubs_4914
    (0x08074914, 'equip_zone_sub_stubs_4914',
     'Block2 dispatch sub-stubs start (R4 disasm); '
     '6 targets: sub_914/920/948/964/9b8 + epilogue_9d4; raw ptr dispatch from table_48a0'),

    # DWORD_08074aac -> check_equip_slot_eligible_bst_filter_ptr_4aac
    # fn-ptr THUMB+1 value 0x08050c59 = check_equip_slot_eligible_with_bst_filter+1
    (0x08074aac, 'check_equip_slot_eligible_bst_filter_ptr_4aac',
     'fn-ptr+1=0x08050c59 for check_equip_slot_eligible_with_bst_filter (0x08050c58); '
     'zone-pair predicate passed to invoke_count_zone_pair_hits_full_range; '
     'tick_equip_activation_lp_display_seq state 0x7e'),

    # DWORD_08074d4c -> check_equip_slot_eligible_by_type_query_ptr_4d4c
    # fn-ptr THUMB+1 value 0x080507ad = check_equip_slot_eligible_by_type_query+1 (odd=THUMB+1)
    (0x08074d4c, 'check_equip_slot_eligible_by_type_query_ptr_4d4c',
     'fn-ptr THUMB+1=0x080507ad for check_equip_slot_eligible_by_type_query '
     '(0x080507ac, asm/05:16635); zone pair predicate passed to '
     'invoke_count_zone_pair_hits_full_range; tick_equip_display_seq_when_fewer_monster_zones state 0x7f'),

    # DAT_08075150 -> equip_display_switch_table_ptr_5150
    (0x08075150, 'equip_display_switch_table_ptr_5150',
     'ptr to switchD_0807514a dispatch table (0x08075154); '
     '31 entries states 0x62..0x80; dispatch_equip_display_state_by_code @0x0807512c'),
]

# ---------------------------------------------------------------------------
# D. PLATE_REWRITES: (func_addr, old_text, new_text)
#    C8 stale FUN_ fix -- text pure ASCII.
#    WARN/not-found treated as FAIL.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # C8 fix: enqueue_effect_slot_sprite_by_zone_capacity_check @ 0x0807500c
    # Plate line: "@ Called by FUN_0807a680 (0x0807a680, duel_field context)."
    # 0x0807a680 is a bl instruction site in asm/10, not a function entry.
    # Enclosing function: dispatch_equip_sprite_by_zone_or_capacity_guard (asm/10:583)
    (0x0807500c,
     'FUN_0807a680',
     'dispatch_equip_sprite_by_zone_or_capacity_guard'),
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

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_vaddr, gas_label, slot_label))
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
    """Replace old_text with new_text in existing plate comment. WARN=FAIL."""
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
    print("=== RefineF09Seg6Slots (DRY=%s) ===" % DRY)
    print("  Seg-6: 0x08074338..0x080752cc  (20 fn)")
    print("  EQ=%d REF=%d RENAME=%d PLATE=%d" % (
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
    print("\n--- D. PLATE_REWRITES: FUN_ fixes (%d) ---" % len(PLATE_REWRITES))
    for func_addr, old_text, new_text in PLATE_REWRITES:
        _apply_plate_fix(func_addr, old_text, new_text)

    print("\n=== RefineF09Seg6Slots DONE ===")
    print("  EQ=%d  REF=%d  RENAME=%d  PLATE_FIX=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(PLATE_REWRITES)))


main()
