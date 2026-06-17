# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg7Slots.py -- F08 Seg-7 (0x0806a118..0x0806ab0c)
#   dispatch_equip_zone_sprite_by_lp_state_with_placement_check cluster
#   EQ=40 (37 reuse + 3 new)  REF=0  RENAME_ONLY=0  PLATE=0  DISASM=0  FUNC_RENAME=0
#   carve=0  disasm=0
#   §5.1: 0x0806a544 (4B orphan, 0 refs) -- .byte unchanged, not touched
#
# Mode A fixes applied:
#   #1 (C2/C3): 0x0806a544 4B orphan stub added to §5.1 (no disasm/carve, 0 refs)
#   #2 (name):  ZONE14_CHAIN_SLOT_FLAG_OFF -> EQUIP_ZONE_COUNT_TABLE_OFF (reviewer confirmed
#               gDuelFieldSlots+0x1cb8=gEquipZoneCountTable=0x0201e1c8)
#
# NEW constants added to constants/ files before running this script:
#   duel_field.inc: EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8 (gDuelFieldSlots base; domain != DUEL_ACTIVE_PLAYER_OFF)
#                   LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff (LP display all-slots; domain != EQUIP_SLOT_SCORE_CAP etc.)
#   oam_attr.inc:   OAM_ZONE_SPRITE_PAIR_P2_FIRST=0x8028 (P2 first zone sprite pair)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_030235-pre-f08seg7

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    40 slots total (37 reuse + 3 new)
#    Order follows proposal EQ table (address-ascending)
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- gP1LifePoints = 0x0201c4e0 (slots 1-2 of 4) ----
    (0x0806a1ec, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806a1ec', None),
    (0x0806a210, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806a210', None),

    # ---- gDuelFieldSlots = 0x0201c510 (slot 1 of 7) ----
    (0x0806a2e0, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806a2e0', None),

    # ---- EQUIP_ZONE_COUNT_TABLE_OFF = 0x1cb8  NEW duel_field.inc ----
    (0x0806a2e4, 0x00001cb8, 'EQUIP_ZONE_COUNT_TABLE_OFF', 'equip_zone_count_table_off_0806a2e4',
     'EQUIP_ZONE_COUNT_TABLE_OFF=0x1cb8: gDuelFieldSlots+0x1cb8=gEquipZoneCountTable(0x0201e1c8)'),

    # ---- MONSTER_REBORN_CID = 0x12ea ----
    (0x0806a2e8, 0x000012ea, 'MONSTER_REBORN_CID', 'monster_reborn_cid_0806a2e8', None),

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (slot 1 of 9) ----
    (0x0806a3e4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a3e4', None),

    # ---- gDuelFieldSlots (slot 2 of 7) ----
    (0x0806a3e8, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806a3e8', None),

    # ---- gDuelPhaseFlags = 0x0201b290 (slot 1 of 5) ----
    (0x0806a440, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806a440', None),

    # ---- POLYMERIZATION_CID = 0x12e5 ----
    (0x0806a47c, 0x000012e5, 'POLYMERIZATION_CID', 'polymerization_cid_0806a47c', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 2 of 9) ----
    (0x0806a480, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a480', None),

    # ---- gP1SlotSetCodeArray = 0x0201c740 ----
    (0x0806a484, 0x0201c740, 'gP1SlotSetCodeArray', 'gp1slotsetcodearray_0806a484', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 3 of 9) ----
    (0x0806a518, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a518', None),

    # ---- gDuelFieldSlots (slot 3 of 7) ----
    (0x0806a51c, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806a51c', None),

    # ---- OAM_EQUIP_SPRITE_TILE_P2_1C = 0x801c ----
    (0x0806a540, 0x0000801c, 'OAM_EQUIP_SPRITE_TILE_P2_1C', 'oam_equip_sprite_tile_p2_1c_0806a540', None),

    # ---- gDuelPhaseFlags (slot 2 of 5) ----
    (0x0806a614, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806a614', None),

    # ---- MIND_HAXORZ_CID = 0x184d (slot 1 of 2) ----
    (0x0806a618, 0x0000184d, 'MIND_HAXORZ_CID', 'mind_haxorz_cid_0806a618',
     'MIND_HAXORZ_CID=0x184d: gate in dispatch_zone_sprite_with_effect_node_and_state'),

    # ---- OAM_ZONE_SPRITE_PAIR_P2_FIRST = 0x8028  NEW oam_attr.inc ----
    (0x0806a61c, 0x00008028, 'OAM_ZONE_SPRITE_PAIR_P2_FIRST', 'oam_zone_sprite_pair_p2_first_0806a61c',
     'OAM_ZONE_SPRITE_PAIR_P2_FIRST=0x8028: P2 first zone sprite pair; second=0x8029'),

    # ---- OAM_EQUIP_SLOT_SPRITE_P2 = 0x8029 ----
    (0x0806a620, 0x00008029, 'OAM_EQUIP_SLOT_SPRITE_P2', 'oam_equip_slot_sprite_p2_0806a620', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 4 of 9) ----
    (0x0806a624, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a624', None),

    # ---- gDuelFieldSlots (slot 4 of 7) ----
    (0x0806a628, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806a628', None),

    # ---- MIND_HAXORZ_CID (slot 2 of 2) ----
    (0x0806a690, 0x0000184d, 'MIND_HAXORZ_CID', 'mind_haxorz_cid_0806a690', None),

    # ---- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 ----
    (0x0806a6f4, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'lp_zone_off_1ce8_0806a6f4',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8'),

    # ---- gDuelEquipCtx = 0x0201bbbc ----
    (0x0806a6f8, 0x0201bbbc, 'gDuelEquipCtx', 'gduelequipctx_0806a6f8', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 5 of 9) ----
    (0x0806a6fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a6fc', None),

    # ---- gDuelPhaseFlags (slot 3 of 5) ----
    (0x0806a75c, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806a75c', None),

    # ---- LP_ROW_TYPE8_ALL_SLOTS_MASK = 0xffff  NEW duel_field.inc ----
    (0x0806a7c0, 0x0000ffff, 'LP_ROW_TYPE8_ALL_SLOTS_MASK', 'lp_row_type8_all_slots_mask_0806a7c0',
     'LP_ROW_TYPE8_ALL_SLOTS_MASK=0xffff: all equip slots selected for set_lp_display_row_type8'),

    # ---- PLAYER_BLOCK_STRIDE (slot 6 of 9) ----
    (0x0806a87c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a87c', None),

    # ---- gDuelFieldSlots (slot 5 of 7) ----
    (0x0806a880, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806a880', None),

    # ---- gDuelPhaseFlags (slot 4 of 5) ----
    (0x0806a8fc, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806a8fc', None),

    # ---- gP1LifePoints (slot 3 of 4) ----
    (0x0806a924, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806a924', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 7 of 9) ----
    (0x0806a928, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806a928', None),

    # ---- gP1LifePoints (slot 4 of 4) ----
    (0x0806a94c, 0x0201c4e0, 'gP1LifePoints', 'gp1lifepoints_0806a94c', None),

    # ---- LP_CARD_TRACK_BASE_OFF = 0x1da8 ----
    (0x0806a950, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'lp_card_track_base_off_0806a950',
     'LP_CARD_TRACK_BASE_OFF=0x1da8'),

    # ---- gDuelPhaseFlags (slot 5 of 5) ----
    (0x0806a988, 0x0201b290, 'gDuelPhaseFlags', 'gduelphaseflagss_0806a988', None),

    # ---- LIGHT_OF_INTERVENTION_CID = 0x135d ----
    (0x0806aa08, 0x0000135d, 'LIGHT_OF_INTERVENTION_CID', 'light_of_intervention_cid_0806aa08', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 8 of 9) ----
    (0x0806aa0c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806aa0c', None),

    # ---- gDuelFieldSlots (slot 6 of 7) ----
    (0x0806aa10, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806aa10', None),

    # ---- PLAYER_BLOCK_STRIDE (slot 9 of 9) ----
    (0x0806aa5c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'player_block_stride_0806aa5c', None),

    # ---- gDuelFieldSlots (slot 7 of 7) ----
    (0x0806aa60, 0x0201c510, 'gDuelFieldSlots', 'gduelfieldslots_0806aa60', None),

    # ---- EQUIP_CHAIN_SENTINEL = 0xffff0000 ----
    (0x0806ab08, 0xffff0000, 'EQUIP_CHAIN_SENTINEL', 'equip_chain_sentinel_0806ab08',
     'EQUIP_CHAIN_SENTINEL=0xffff0000: gEquipChainSlotRefs list terminator'),
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


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg7Slots (DRY=%s) ===" % DRY)
    print("  Seg-7: 0x0806a118..0x0806ab0c")
    print("  EQ=%d  REF=0  RENAME_ONLY=0  PLATE=0  DISASM=0  FUNC_RENAME=0" % len(EQ_SLOTS))
    print("  §5.1: 0x0806a544 (4B orphan, 0 refs) -- .byte unchanged, not touched")

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        mem = currentProgram.getMemory()
        a = _addr(slot_addr)
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
            if actual != (value & 0xFFFFFFFF):
                eq_fail += 1
                print("[FAIL] 0x%08x (%s): rom=0x%08x expect=0x%08x" % (
                    slot_addr, eq_name, actual, value & 0xFFFFFFFF))
                continue
        except Exception as e:
            eq_fail += 1
            print("[FAIL] 0x%08x (%s): read error %s" % (slot_addr, eq_name, e))
            continue
        if _apply_eq(slot_addr, value, eq_name, slot_label, eol):
            eq_ok += 1
        else:
            eq_fail += 1
    print("  EQ done: %d ok, %d fail" % (eq_ok, eq_fail))
    if eq_fail > 0:
        print("  !!! %d EQ FAILURES -- abort and investigate !!!" % eq_fail)

    print("\n=== RefineF08Seg7Slots DONE ===")
    print("  EQ=%d/%d ok  (fail=%d)" % (eq_ok, len(EQ_SLOTS), eq_fail))


main()
