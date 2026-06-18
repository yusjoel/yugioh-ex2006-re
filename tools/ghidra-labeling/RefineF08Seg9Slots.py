# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg9Slots.py -- F08 Seg-9 (0x0806cbe8..0x0806d960)
#   tick_equip_target_query_display_seq cluster (20 fn)
#   EQ=51 (47 reuse + 4 NEW: MAGIC_CYLINDER_CID / DRAINING_SHIELD_CID /
#           RING_OF_DESTRUCTION_CID / SPRITE_RECORD_P2_SIDE)
#   REF=0
#   RENAME=12 (PTR_gP1LifePoints_* x11 + DWORD_0806d678 -> gp1lifepoints_<addr>)
#   FUNC_RENAME=0
#   PLATE=3:
#     tick_equip_lp_display_state_by_zone_match @ 0x0806d3d8: CJK mojibake -> ASCII 741-char rewrite
#     enqueue_zone_equip_sprite_if_slot_matches @ 0x0806d514: FUN_08071404 -> enqueue_equip_sprite_guarded_by_zone_type13
#     enqueue_spirit_zone_sprite_with_lp_check @ 0x0806d680: FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id
#
# NEW constants added to constants/*.inc before running:
#   card_info.inc: RING_OF_DESTRUCTION_CID=0x138d, MAGIC_CYLINDER_CID=0x1404, DRAINING_SHIELD_CID=0x176a
#   oam_attr.inc:  SPRITE_RECORD_P2_SIDE=0x8020
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_080758-pre-F08Seg9

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
#    51 slots total
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- gDuelPhaseFlags = 0x0201b290 (4 slots, reuse ewram.inc) ----
    (0x0806cc1c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806cc1c', None),
    (0x0806d160, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806d160', None),
    (0x0806d1d4, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806d1d4', None),
    (0x0806d3f4, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806d3f4', None),
    (0x0806d78c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflags_0806d78c', None),

    # ---- LP_CARD_TRACK_BASE_OFF = 0x1da8 (1 slot, reuse ewram.inc) ----
    (0x0806cc60, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_0806cc60', None),

    # ---- LP_CARD_TRACK_NEXT_OFF = 0x1daa (3 slots, reuse ewram.inc) ----
    (0x0806cc94, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_0806cc94', None),
    (0x0806ccb8, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_0806ccb8', None),
    (0x0806d498, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'lp_card_track_next_off_0806d498', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (14 slots, reuse ewram.inc) ----
    (0x0806cd38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806cd38', None),
    (0x0806cdb8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806cdb8', None),
    (0x0806cf38, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806cf38', None),
    (0x0806cfe0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806cfe0', None),
    (0x0806d0c4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d0c4', None),
    (0x0806d284, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d284', None),
    (0x0806d3d0, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d3d0', None),
    (0x0806d50c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d50c', None),
    (0x0806d5a8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d5a8', None),
    (0x0806d610, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d610', None),
    (0x0806d764, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d764', None),
    (0x0806d7cc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d7cc', None),
    (0x0806d800, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d800', None),
    (0x0806d8b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806d8b8', None),

    # ---- gDuelFieldSlots = 0x0201c510 (8 slots, reuse ewram.inc) ----
    (0x0806cd3c, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806cd3c', None),
    (0x0806cf3c, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806cf3c', None),
    (0x0806cfe4, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806cfe4', None),
    (0x0806d0c8, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806d0c8', None),
    (0x0806d288, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806d288', None),
    (0x0806d3d4, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806d3d4', None),
    (0x0806d5ac, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806d5ac', None),
    (0x0806d614, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806d614', None),
    (0x0806d768, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806d768', None),

    # ---- LP_ACTIVATION_LINK_FLAG_OFF = 0x10d0 (1 slot, reuse ewram.inc) ----
    (0x0806cdb4, 0x000010d0, 'LP_ACTIVATION_LINK_FLAG_OFF', 'lp_activation_link_flag_off_0806cdb4', None),

    # ---- MAGIC_CYLINDER_CID = 0x1404 (1 slot, NEW card_info.inc) ----
    (0x0806cdbc, 0x00001404, 'MAGIC_CYLINDER_CID', 'magic_cylinder_cid_0806cdbc',
     'MAGIC_CYLINDER_CID=0x1404: Magic Cylinder (pw=62279055); dispatch_equip_lp_sprite_by_trap_card_id BST dispatch'),

    # ---- DRAINING_SHIELD_CID = 0x176a (1 slot, NEW card_info.inc) ----
    (0x0806cdc8, 0x0000176a, 'DRAINING_SHIELD_CID', 'draining_shield_cid_0806cdc8',
     'DRAINING_SHIELD_CID=0x176a: Draining Shield (pw=43250041); dispatch_equip_lp_sprite_by_trap_card_id second BST target'),

    # ---- SPRITE_RECORD_P2_SIDE = 0x8020 (2 slots, NEW oam_attr.inc) ----
    (0x0806ce1c, 0x00008020, 'SPRITE_RECORD_P2_SIDE', 'sprite_record_p2_side_0806ce1c',
     'SPRITE_RECORD_P2_SIDE=0x8020: P2-side sprite record (bit15+0x20); player==1 path in dispatch_equip_lp_sprite_by_trap_card_id'),
    (0x0806ce64, 0x00008020, 'SPRITE_RECORD_P2_SIDE', 'sprite_record_p2_side_0806ce64',
     'SPRITE_RECORD_P2_SIDE=0x8020: P2-side sprite record (bit15+0x20); second slot in dispatch_equip_lp_sprite_by_trap_card_id'),

    # ---- gEquipChainSlotRefs = 0x0201bb90 (1 slot, reuse ewram.inc) ----
    (0x0806cf34, 0x0201bb90, 'gEquipChainSlotRefs', 'gequipchainslot_refs_0806cf34', None),

    # ---- gEquipZoneCountTable = 0x0201e1c8 (1 slot, reuse ewram.inc) ----
    (0x0806d120, 0x0201e1c8, 'gEquipZoneCountTable', 'gequipzonecounttable_0806d120', None),

    # ---- VALKYRION_THE_MAGNA_WARRIOR_CID = 0x138a (1 slot, reuse card_info.inc) ----
    (0x0806d138, 0x0000138a, 'VALKYRION_THE_MAGNA_WARRIOR_CID', 'valkyrion_the_magna_warrior_cid_0806d138',
     'VALKYRION_THE_MAGNA_WARRIOR_CID=0x138a: dispatch_neo_space_placement_by_card_id_and_state r7=3 path'),

    # ---- PUPPET_MASTER_CID = 0x156a (1 slot, reuse card_info.inc) ----
    (0x0806d13c, 0x0000156a, 'PUPPET_MASTER_CID', 'puppet_master_cid_0806d13c',
     'PUPPET_MASTER_CID=0x156a: dispatch_neo_space_placement_by_card_id_and_state r7=2 path'),

    # ---- EQUIP_PHASE_FRAME_OFF = 0x4a4 (2 slots, reuse ewram.inc) ----
    (0x0806d1d8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806d1d8', None),
    (0x0806d210, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'equip_phase_frame_off_0806d210', None),

    # ---- RING_OF_DESTRUCTION_CID = 0x138d (1 slot, NEW card_info.inc) ----
    (0x0806d28c, 0x0000138d, 'RING_OF_DESTRUCTION_CID', 'ring_of_destruction_cid_0806d28c',
     'RING_OF_DESTRUCTION_CID=0x138d: Ring of Destruction (pw=83555666); submit_ring_of_destruction_lp_indicators_if_zone_matched CID gate'),

    # ---- gDuelCardCtxBase = 0x0201e2a0 (1 slot, reuse ewram.inc) ----
    (0x0806d44c, 0x0201e2a0, 'gDuelCardCtxBase', 'gduelcardctxbase_0806d44c', None),

    # ---- gP1HandSlotArray = 0x0201c8f8 (2 slots, reuse ewram.inc) ----
    (0x0806d510, 0x0201c8f8, 'gP1HandSlotArray', 'gp1handslotarray_0806d510', None),
    (0x0806d8bc, 0x0201c8f8, 'gP1HandSlotArray', 'gp1handslotarray_0806d8bc', None),

    # ---- EQUIP_ZONE_COUNT_TABLE_OFF = 0x1cb8 (1 slot, reuse duel_field.inc) ----
    (0x0806d76c, 0x00001cb8, 'EQUIP_ZONE_COUNT_TABLE_OFF', 'equip_zone_count_table_off_0806d76c',
     'EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8: base=gDuelFieldSlots; ldr+add -> gDuelFieldSlots+0x1cb8=gEquipZoneCountTable; Seg-7 domain exception confirmed'),

    # ---- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (3 slots, reuse ewram.inc) ----
    (0x0806d67c, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0806d67c', None),
    (0x0806d6bc, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0806d6bc', None),
    (0x0806d850, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'p1lp_block2_off_0806d850', None),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: none
# ---------------------------------------------------------------------------
REF_SLOTS = []

# ---------------------------------------------------------------------------
# C. RENAME_SLOTS: PTR_ label -> gp1lifepoints_<addr>
#    12 entries
# ---------------------------------------------------------------------------
RENAME_SLOTS = [
    (0x0806cc5c, 'PTR_gP1LifePoints_0806cc5c', 'gp1lifepoints_0806cc5c'),
    (0x0806cc90, 'PTR_gP1LifePoints_0806cc90', 'gp1lifepoints_0806cc90'),
    (0x0806ccb4, 'PTR_gP1LifePoints_0806ccb4', 'gp1lifepoints_0806ccb4'),
    (0x0806cdb0, 'PTR_gP1LifePoints_0806cdb0', 'gp1lifepoints_0806cdb0'),
    (0x0806d450, 'PTR_gP1LifePoints_0806d450', 'gp1lifepoints_0806d450'),
    (0x0806d47c, 'PTR_gP1LifePoints_0806d47c', 'gp1lifepoints_0806d47c'),
    (0x0806d494, 'PTR_gP1LifePoints_0806d494', 'gp1lifepoints_0806d494'),
    (0x0806d6b8, 'PTR_gP1LifePoints_0806d6b8', 'gp1lifepoints_0806d6b8'),
    (0x0806d7c8, 'PTR_gP1LifePoints_0806d7c8', 'gp1lifepoints_0806d7c8'),
    (0x0806d7fc, 'PTR_gP1LifePoints_0806d7fc', 'gp1lifepoints_0806d7fc'),
    (0x0806d84c, 'PTR_gP1LifePoints_0806d84c', 'gp1lifepoints_0806d84c'),
    (0x0806d678, 'DWORD_0806d678', 'gp1lifepoints_0806d678'),
]

# ---------------------------------------------------------------------------
# D. FUNC_RENAMES: none
# ---------------------------------------------------------------------------
FUNC_RENAMES = []

# ---------------------------------------------------------------------------
# E. PLATE content
#    PLATE#3: tick_equip_lp_display_state_by_zone_match @ 0x0806d3d8
#             CJK mojibake -> full ASCII rewrite (741 chars)
#    PLATE#1: enqueue_zone_equip_sprite_if_slot_matches @ 0x0806d514
#             substring FUN_08071404 -> enqueue_equip_sprite_guarded_by_zone_type13
#    PLATE#2: enqueue_spirit_zone_sprite_with_lp_check @ 0x0806d680
#             substring FUN_08071d64 -> dispatch_spirit_monster_zone_sprite_by_card_id
#    All text MUST be pure ASCII.
# ---------------------------------------------------------------------------

TICK_EQUIP_LP_DISPLAY_PLATE = (
    "Equip LP display state machine tick. "
    "Reads gDuelPhaseFlags+0x4a0 current step code and dispatches: "
    "step=0x80: calls check_effect_slot_matches_zone_entry to verify slot-zone match; "
    "on match calls read_effect_slot_side_and_type + invoke_effect_node_with_active_flag_3arg to activate; "
    "if activated reads [gDuelCardCtxBase+player*4+8] confirm_flag: "
    "if==1 calls sample_prng_scaled(2) and writes result to gP1LifePoints+0x1d40, returns 0x7f; "
    "if==0 calls invoke_card_display_op_0x31_sub8(0x38), returns 0x7f. "
    "step=0x7f: reads player/slot fields, calls enqueue_lp_display_row_type17, returns 0x7e. "
    "step=0x7e: checks gP1LifePoints+0x1daa non-zero gate, "
    "calls invoke_equip_slot_eligibility_via_effect_node_bitmap, returns result. "
    "Other steps return 0."
)

ENQUEUE_ZONE_EQUIP_PLATE_OLD = 'FUN_08071404'
ENQUEUE_ZONE_EQUIP_PLATE_NEW = 'enqueue_equip_sprite_guarded_by_zone_type13'

ENQUEUE_SPIRIT_ZONE_PLATE_OLD = 'FUN_08071d64'
ENQUEUE_SPIRIT_ZONE_PLATE_NEW = 'dispatch_spirit_monster_zone_sprite_by_card_id'


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
    print("=== RefineF08Seg9Slots (DRY=%s) ===" % DRY)
    print("  Seg-9: 0x0806cbe8..0x0806d960")
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

    # D. FUNC_RENAME (none)
    print("\n--- D. FUNC_RENAME (%d) ---" % len(FUNC_RENAMES))

    # E. PLATE#3: tick_equip_lp_display_state_by_zone_match -- full ASCII rewrite (CJK mojibake fix)
    print("\n--- E. PLATE #3: tick_equip_lp_display_state_by_zone_match (CJK->ASCII rewrite) ---")
    _set_plate(0x0806d3d8, TICK_EQUIP_LP_DISPLAY_PLATE)

    # F. PLATE FIX #1: enqueue_zone_equip_sprite_if_slot_matches -- FUN_08071404 -> current name
    print("\n--- F. PLATE FIX #1 (enqueue_zone_equip_sprite_if_slot_matches) ---")
    _apply_plate_fix(0x0806d514, ENQUEUE_ZONE_EQUIP_PLATE_OLD, ENQUEUE_ZONE_EQUIP_PLATE_NEW)

    # G. PLATE FIX #2: enqueue_spirit_zone_sprite_with_lp_check -- FUN_08071d64 -> current name
    print("\n--- G. PLATE FIX #2 (enqueue_spirit_zone_sprite_with_lp_check) ---")
    _apply_plate_fix(0x0806d680, ENQUEUE_SPIRIT_ZONE_PLATE_OLD, ENQUEUE_SPIRIT_ZONE_PLATE_NEW)

    print("\n=== RefineF08Seg9Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  RENAME=%d  FUNC_RENAME=%d" % (
        eq_ok, len(EQ_SLOTS),
        len(REF_SLOTS),
        len(RENAME_SLOTS),
        len(FUNC_RENAMES)))


main()
