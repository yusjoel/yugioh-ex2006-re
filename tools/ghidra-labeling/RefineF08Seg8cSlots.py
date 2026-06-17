# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg8cSlots.py -- F08 Seg-8c (0x0806c0cc..0x0806cbe8)
#   tick_spear_cretin_placement_state_machine + enqueue_equip_zone_sprite_chain_if_slot_matches
#   + enqueue_spirit_monster_zone_sprite_otohime + 7 other fns
#   EQ=39 (34 reuse + 3 NEW: OAM_EQUIP_ZONE_CHAIN_SPRITE_P2 / SOLOMONS_LAWBOOK_CID / P2LP_BLOCK2_OFF_1CF4
#           + 2 RENAME for PTR_gP1LifePoints already-sym slots)
#   REF=0
#   RENAME=2 (PTR_gP1LifePoints_0806cb98 -> gp1lifepoints_0806cb98, idem 0806cbe0)
#   FUNC_RENAME=1 (dispatch_neo_daedalus_placement_check_by_state -> tick_spear_cretin_placement_state_machine)
#   PLATE=2:
#     tick_spear_cretin_placement_state_machine @ 0x0806c0cc: full rewrite
#     enqueue_spirit_monster_zone_sprite_otohime @ 0x0806cb54: FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id
#
# NEW constants added to constants/*.inc before running:
#   card_info.inc: MORPHING_JAR_2_CID=0x1369, SOLOMONS_LAWBOOK_CID=0x137e
#   oam_attr.inc:  OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052
#   ewram.inc:     P2LP_BLOCK2_OFF_1CF4=0x1cf4
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_pre-F08Seg8c

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
#    39 slots total
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- gDuelPhaseFlags = 0x0201b290 (4 slots, reuse ewram.inc) ----
    (0x0806c10c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806c10c', None),
    (0x0806c858, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806c858', None),
    (0x0806c9ec, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806c9ec', None),

    # ---- EQUIP_PHASE_FRAME_OFF = 0x4a4 (1 slot, reuse ewram.inc) ----
    (0x0806c110, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806c110', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (6 slots, reuse ewram.inc) ----
    (0x0806c1ac, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806c1ac', None),
    (0x0806c35c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806c35c', None),
    (0x0806c3d0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806c3d0', None),
    (0x0806c800, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806c800', None),
    (0x0806c8f0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806c8f0', None),
    (0x0806c9e4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806c9e4', None),

    # ---- gP1HandSlotArray = 0x0201c8f8 (2 slots, reuse ewram.inc) ----
    (0x0806c1b0, 0x0201c8f8, 'gP1HandSlotArray', 'gp1handslotarray_0806c1b0', None),
    (0x0806c804, 0x0201c8f8, 'gP1HandSlotArray', 'gp1handslotarray_0806c804', None),

    # ---- SPEAR_CRETIN_CID = 0x133b (1 slot, reuse card_info.inc) ----
    (0x0806c1b4, 0x0000133b, 'SPEAR_CRETIN_CID', 'spear_cretin_cid_0806c1b4',
     'SPEAR_CRETIN_CID=0x133b: Spear Cretin (pw=58551308); tick_spear_cretin_placement_state_machine CID dispatch'),

    # ---- gDuelFieldSlots = 0x0201c510 (3 slots, reuse ewram.inc) ----
    (0x0806c360, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806c360', None),
    (0x0806c3d4, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806c3d4', None),
    (0x0806c9e8, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806c9e8', None),

    # ---- OAM_EQUIP_ZONE_CHAIN_SPRITE_P2 = 0x8052 (1 slot, NEW oam_attr.inc) ----
    (0x0806c364, 0x00008052, 'OAM_EQUIP_ZONE_CHAIN_SPRITE_P2', 'oam_equip_zone_chain_sprite_p2_0806c364',
     'OAM_EQUIP_ZONE_CHAIN_SPRITE_P2=0x8052: equip zone chain sprite OAM attr0 P2 (bit15+0x52); P1=0x52 inline; 4 raw ROM refs'),

    # ---- gEquipChainSlotRefs = 0x0201bb90 (1 slot, reuse ewram.inc) ----
    (0x0806c738, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainslot_refs_0806c738', None),

    # ---- gP1LifePoints = 0x0201c4e0 (4 slots, reuse ewram.inc; already sym in asm) ----
    (0x0806c8ec, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806c8ec', None),
    (0x0806c91c, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806c91c', None),
    (0x0806c948, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806c948', None),
    (0x0806c970, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806c970', None),

    # ---- gDuelCardCtxBase = 0x0201e2a0 (1 slot, reuse ewram.inc) ----
    (0x0806c918, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_0806c918', None),

    # ---- LP_CARD_TRACK_BASE_OFF = 0x1da8 (1 slot, reuse ewram.inc) ----
    (0x0806c974, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_0806c974', None),

    # ---- RE_FUSION_CID = 0x1881 (1 slot, reuse card_info.inc) ----
    (0x0806ca5c, 0x00001881, 'RE_FUSION_CID', 're_fusion_cid_0806ca5c',
     'RE_FUSION_CID=0x1881: Re-Fusion (pw=4718022); dispatch_special_card_zone_sprite_by_type_and_state CID path'),

    # ---- SYMBOL_OF_HERITAGE_CID = 0x19d7 (2 slots, reuse card_info.inc) ----
    (0x0806ca68, 0x000019d7, 'SYMBOL_OF_HERITAGE_CID', 'symbol_of_heritage_cid_0806ca68',
     'SYMBOL_OF_HERITAGE_CID=0x19d7: Symbol of Heritage; dispatch_special_card_zone_sprite_by_type_and_state'),
    (0x0806caec, 0x000019d7, 'SYMBOL_OF_HERITAGE_CID', 'symbol_of_heritage_cid_0806caec', None),

    # ---- SOUL_RESURRECTION_CID = 0x17b7 (1 slot, reuse card_info.inc) ----
    (0x0806cac4, 0x000017b7, 'SOUL_RESURRECTION_CID', 'soul_resurrection_cid_0806cac4',
     'SOUL_RESURRECTION_CID=0x17b7: Soul Resurrection; dispatch_special_card_zone_sprite_by_type_and_state'),

    # ---- CALL_OF_THE_HAUNTED_CID = 0x137d (1 slot, reuse card_info.inc) ----
    (0x0806cac8, 0x0000137d, 'CALL_OF_THE_HAUNTED_CID', 'call_of_the_haunted_cid_0806cac8',
     'CALL_OF_THE_HAUNTED_CID=0x137d: Call of the Haunted; dispatch_special_card_zone_sprite_by_type_and_state'),

    # ---- AUTONOMOUS_ACTION_UNIT_CID = 0x15e6 (1 slot, reuse card_info.inc) ----
    (0x0806cad0, 0x000015e6, 'AUTONOMOUS_ACTION_UNIT_CID', 'autonomous_action_unit_cid_0806cad0',
     'AUTONOMOUS_ACTION_UNIT_CID=0x15e6: Autonomous Action Unit; dispatch_special_card_zone_sprite_by_type_and_state'),

    # ---- gEquipZoneRankState = 0x0201e4d0 (2 slots, reuse ewram.inc) ----
    (0x0806cb14, 0x0201e4d0, 'gEquipZoneRankState', 'gequipzonerankstate_0806cb14', None),
    (0x0806cb40, 0x0201e4d0, 'gEquipZoneRankState', 'gequipzonerankstate_0806cb40', None),

    # ---- SOLOMONS_LAWBOOK_CID = 0x137e (1 slot, NEW card_info.inc) ----
    (0x0806cb6c, 0x0000137e, 'SOLOMONS_LAWBOOK_CID', 'solomons_lawbook_cid_0806cb6c',
     "SOLOMONS_LAWBOOK_CID=0x137e: Solomon's Lawbook (pw=23471572); enqueue_spirit_monster_zone_sprite_otohime special case"),

    # ---- MAHARAGHI_CID = 0x14fd (1 slot, reuse card_info.inc) ----
    (0x0806cb70, 0x000014fd, 'MAHARAGHI_CID', 'maharaghi_cid_0806cb70',
     'MAHARAGHI_CID=0x14fd: Maharaghi (pw=40695128); enqueue_spirit_monster_zone_sprite_otohime special case'),

    # ---- gP1LifePoints PTR slots (2 RENAME slots; already symbolized) ----
    (0x0806cb98, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806cb98', None),
    (0x0806cbe0, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806cbe0', None),

    # ---- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (2 slots, reuse ewram.inc) ----
    (0x0806cb9c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0806cb9c', None),
    (0x0806cbe4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0806cbe4', None),

    # ---- P2LP_BLOCK2_OFF_1CF4 = 0x1cf4 (1 slot, NEW ewram.inc) ----
    (0x0806cba0, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_block2_off_0806cba0',
     'P2LP_BLOCK2_OFF_1CF4=0x1cf4: [gP1LifePoints+0x1cf4] P2 LP display block2 (opponent); distinct from FIELD_STATE_OFF=0x1cf4 (base=gDuelFieldSlots); abs=0x0201e1d4'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: PTR_ label -> user label
#    (handled above in EQ_SLOTS by createLabel; these are for primary label rename only)
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    # PTR_gP1LifePoints_0806cb98 -> gp1lifepoints_0806cb98
    (0x0806cb98, 'PTR_gP1LifePoints_0806cb98', 'gp1lifepoints_0806cb98'),
    # PTR_gP1LifePoints_0806cbe0 -> gp1lifepoints_0806cbe0
    (0x0806cbe0, 'PTR_gP1LifePoints_0806cbe0', 'gp1lifepoints_0806cbe0'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAMES: (old_addr, old_name, new_name)
#    1 entry: dispatch_neo_daedalus_placement_check_by_state -> tick_spear_cretin_placement_state_machine
# ---------------------------------------------------------------------------
FUNC_RENAMES = [
    (0x0806c0cc,
     'dispatch_neo_daedalus_placement_check_by_state',
     'tick_spear_cretin_placement_state_machine'),
]

# ---------------------------------------------------------------------------
# E. PLATE_REWRITES for tick_spear_cretin_placement_state_machine (full rewrite)
#    and enqueue_spirit_monster_zone_sprite_otohime (substring fix)
#    All text MUST be pure ASCII.
# ---------------------------------------------------------------------------
TICK_SPEAR_CRETIN_PLATE = (
    "tick_spear_cretin_placement_state_machine @ 0x0806c0cc. "
    "Spear Cretin (CID=SPEAR_CRETIN_CID=0x133b) placement state machine. "
    "Three-step state dispatch on gDuelPhaseFlags[+EQUIP_PHASE_FRAME_OFF=0x4a4]: "
    "state=0x80: checks field spell Neo Daedalus group placeable and finds hand slot by set_code, returns 0x7f. "
    "state=0x7f: checks zone slot equip eligibility, constructs target ptr, dispatches by card_id (0x133b vs 0x133b+0x2a), "
    "calls invoke_setup_equip_oam_with_attr2 or setup_equip_oam_entry_with_sprite_attr. Returns 0x7e. "
    "state=0x7e: increments internal counter; when >1 returns 0x64. Returns 0x7e. "
    "state=0x64: calls decrement_lp_bar_display_counter. Returns 0. "
    "Called via bl by dispatch_spear_cretin_activate_if_chain_subtype (indeg=1). "
    "Renamed from dispatch_neo_daedalus_placement_check_by_state (neo_daedalus was callee, not this fn). "
    "Constants: gDuelPhaseFlags=0x0201b290, EQUIP_PHASE_FRAME_OFF=0x4a4, SPEAR_CRETIN_CID=0x133b, "
    "PLAYER_BLOCK_STRIDE=0x868, gP1HandSlotArray=0x0201c8f8."
)

SPIRIT_OTOHIME_PLATE_OLD = 'FUN_08071d64'
SPIRIT_OTOHIME_PLATE_NEW = 'dispatch_spirit_monster_zone_sprite_by_card_id'

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


def _apply_rename_slot(slot_addr, old_label, new_label):
    if DRY:
        print("[dry] RENAME 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
        return
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    syms = list(sym_tbl.getSymbols(a))
    for s in syms:
        if s.getName() == old_label:
            s.setName(new_label, SourceType.USER_DEFINED)
            print("[REN] 0x%08x  %s -> %s" % (slot_addr, old_label, new_label))
            return
    # old label not found; create new label if not present
    names = [s.getName() for s in list(sym_tbl.getSymbols(a))]
    if new_label not in names:
        sym_tbl.createLabel(a, new_label, SourceType.USER_DEFINED)
        print("[REN] 0x%08x  old='%s' not found; created new label %s" % (
            slot_addr, old_label, new_label))
    else:
        print("[REN] 0x%08x  %s already present" % (slot_addr, new_label))


def _apply_func_rename(func_addr, old_name, new_name):
    if DRY:
        print("[dry] FUNC_RENAME 0x%08x  %s -> %s" % (func_addr, old_name, new_name))
        return
    a = _addr(func_addr)
    fn_mgr = currentProgram.getFunctionManager()
    fn = fn_mgr.getFunctionAt(a)
    if fn is None:
        print("[WARN] FUNC_RENAME 0x%08x: no function found" % func_addr)
        return
    fn.setName(new_name, SourceType.USER_DEFINED)
    print("[FUNC_RENAME] 0x%08x  %s -> %s" % (func_addr, old_name, new_name))


def _set_plate(func_addr, plate_text):
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x -- SKIPPING" % func_addr)
        return False
    if DRY:
        print("[dry] PLATE 0x%08x  (%d chars)" % (func_addr, len(plate_text)))
        return True
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(func_addr))
    if cu is None:
        print("[PLATE FAIL] no CodeUnit at 0x%08x" % func_addr)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
    print("[PLATE ok] 0x%08x (%d chars)" % (func_addr, len(plate_text)))
    return True


def _apply_plate_fix(func_addr, old_text, new_text):
    for txt in [old_text, new_text]:
        if any(ord(ch) > 127 for ch in txt):
            print("[PLATE FAIL] non-ASCII in plate_fix @ 0x%08x -- SKIPPING" % func_addr)
            return False
    a = _addr(func_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[WARN] plate_fix 0x%08x: no code unit" % func_addr)
        return False
    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    if existing is None:
        print("[WARN] plate_fix 0x%08x: no plate comment -- FAIL" % func_addr)
        return False
    if old_text not in existing:
        print("[WARN] plate_fix 0x%08x: '%s' not found -- FAIL" % (func_addr, old_text))
        return False
    if DRY:
        print("[dry] PLATE_FIX 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
        return True
    new_plate = existing.replace(old_text, new_text)
    cu.setComment(CodeUnit.PLATE_COMMENT, new_plate)
    print("[PFX] 0x%08x: '%s' -> '%s'" % (func_addr, old_text, new_text))
    return True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg8cSlots (DRY=%s) ===" % DRY)
    print("  Seg-8c: 0x0806c0cc..0x0806cbe8")
    print("  EQ=%d  REF=%d  RENAME=%d  FUNC_RENAME=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(RENAME_SLOTS), len(FUNC_RENAMES)))

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

    # B. REF_SLOTS (none)
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))

    # C. RENAME_SLOTS
    print("\n--- C. RENAME_SLOTS (%d) ---" % len(RENAME_SLOTS))
    for slot_addr, old_label, new_label in RENAME_SLOTS:
        _apply_rename_slot(slot_addr, old_label, new_label)

    # D. FUNC_RENAME
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))
    for func_addr, old_name, new_name in FUNC_RENAMES:
        _apply_func_rename(func_addr, old_name, new_name)

    # E. PLATE: tick_spear_cretin_placement_state_machine -- full rewrite
    print("\n--- E. PLATE (tick_spear_cretin_placement_state_machine) ---")
    # After FUNC_RENAME, function is at 0x0806c0cc with new name
    _set_plate(0x0806c0cc, TICK_SPEAR_CRETIN_PLATE)

    # F. PLATE FIX: enqueue_spirit_monster_zone_sprite_otohime -- substring replace stale FUN_
    print("\n--- F. PLATE FIX (enqueue_spirit_monster_zone_sprite_otohime) ---")
    _apply_plate_fix(0x0806cb54, SPIRIT_OTOHIME_PLATE_OLD, SPIRIT_OTOHIME_PLATE_NEW)

    print("\n=== RefineF08Seg8cSlots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  RENAME=%d  FUNC_RENAME=%d" % (
        eq_ok, len(EQ_SLOTS),
        len(REF_SLOTS),
        len(RENAME_SLOTS),
        len(FUNC_RENAMES)))


main()
