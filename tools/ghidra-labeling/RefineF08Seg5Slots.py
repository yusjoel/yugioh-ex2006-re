# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF08Seg5Slots.py -- F08 Seg-5 (0x08067fa4..0x080690dc)
#   scan_effect_slots_for_equip_sprite_field6 cluster + check_equip_eligible_always_false stub
#   EQ=62 (reuse constants) + REF=4 + RENAME=65 (all auto-name slots)
#   DISASM=1 (THUMB stub @ 0x08068828, 4B: movs r0,#0; bx lr)
#   PLATE_REWRITE=1 (dispatch_equip_slot_sprite_by_zone_type @ 0x0806882c: CJK->ASCII)
#   CREATE_FUNC=1 (check_equip_eligible_always_false @ 0x08068828)
#   FUNC_RENAME=0 / carve=0 / ROM_INCBIN=0
#
# NEW constants added to constants/ files (done before running this script):
#   card_info.inc: BLAST_SPHERE_CID=0x1286 / BIRDFACE_CID=0x139d / IMPERIAL_ORDER_CID=0x1360
#   ewram.inc:     gEquipLpZoneEntryBase=0x0201e500 / EQUIP_OAM_ENTRY_ATTR_14F8=0x14f8
#   oam_attr.inc:  OAM_EQUIP_SPRITE_TILE_P2_1B=0x801b / OAM_EQUIP_SPRITE_TILE_P2_1C=0x801c
#                  EQUIP_SLOT_SCORE_CAP=0xffff
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Jython encodes CJK as
# double-UTF-8 mojibake -- CJK in plate/EOL is a red-line error.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_001839-pre-F08Seg5

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# A. EQ_SLOTS: (slot_addr, value, eq_name, slot_label, eol_ascii_or_None)
#    Creates equate (value->name) and references it from slot address.
#    All 62 EQ slots; all values ROM-byte-verified by reviewer C4.
# ---------------------------------------------------------------------------
EQ_SLOTS = [

    # ---- PLAYER_BLOCK_STRIDE = 0x868 (18 slots) ----
    (0x0806805c, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'scan_effect_stride', None),
    (0x08068178, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_sprite3_stride', None),
    (0x080681fc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_sprite3b_stride', None),
    (0x080682a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_sp3_zone14_stride', None),
    (0x08068348, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_sp3_zone14b_stride', None),
    (0x08068418, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_lp_ind_stride', None),
    (0x080684b8, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_lp_chain_stride', None),
    (0x08068548, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'advance_guard_stride', None),
    (0x080688d4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_slot_act_stride', None),
    (0x08068988, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_sp_state_stride', None),
    (0x08068a44, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_act_zone_stride', None),
    (0x08068abc, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_act_zone_b_stride', None),
    (0x08068b18, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_act_zone_b2_stride', None),
    (0x08068bec, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_lp_field_stride', None),
    (0x08068d84, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_oam_zone_stride', None),
    (0x08068f00, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'apply_slot_score_stride', None),
    (0x08069060, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'dispatch_zone11_stride', None),
    (0x08068820, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'invoke_hand_slot_stride', None),

    # ---- gDuelFieldSlots = 0x0201c510 (14 slots) ----
    (0x08068060, 0x0201c510, 'gDuelFieldSlots', 'scan_field_slots_base', None),
    (0x0806817c, 0x0201c510, 'gDuelFieldSlots', 'invoke_sp3_field_slots_base', None),
    (0x08068200, 0x0201c510, 'gDuelFieldSlots', 'invoke_sp3b_field_slots_base', None),
    (0x080682a8, 0x0201c510, 'gDuelFieldSlots', 'invoke_sp3_zone14_field_base', None),
    (0x0806834c, 0x0201c510, 'gDuelFieldSlots', 'invoke_sp3_zone14b_field_base', None),
    (0x0806841c, 0x0201c510, 'gDuelFieldSlots', 'apply_lp_ind_field_base', None),
    (0x080684bc, 0x0201c510, 'gDuelFieldSlots', 'invoke_lp_chain_field_base', None),
    (0x0806854c, 0x0201c510, 'gDuelFieldSlots', 'advance_guard_field_base', None),
    (0x080688d8, 0x0201c510, 'gDuelFieldSlots', 'apply_slot_act_field_base', None),
    (0x0806898c, 0x0201c510, 'gDuelFieldSlots', 'dispatch_sp_state_field_base', None),
    (0x08068a48, 0x0201c510, 'gDuelFieldSlots', 'apply_act_zone_field_base', None),
    (0x08068bf0, 0x0201c510, 'gDuelFieldSlots', 'dispatch_lp_field_slot_base', None),
    (0x08068d88, 0x0201c510, 'gDuelFieldSlots', 'apply_oam_zone_field_base', None),
    (0x08068f04, 0x0201c510, 'gDuelFieldSlots', 'apply_slot_score_field_base', None),

    # ---- gDuelPhaseFlags = 0x0201b290 (6 slots) ----
    (0x0806865c, 0x0201b290, 'gDuelPhaseFlags', 'advance_guard_phase_flags_base', None),
    (0x080686a4, 0x0201b290, 'gDuelPhaseFlags', 'tick_sm_phase_flags_base', None),
    (0x08068a64, 0x0201b290, 'gDuelPhaseFlags', 'apply_act_zone_phase_flags_base', None),
    (0x08068c34, 0x0201b290, 'gDuelPhaseFlags', 'apply_act_from_zone_phase_flags_base', None),
    (0x08068fb0, 0x0201b290, 'gDuelPhaseFlags', 'enqueue_sprite_phase_flags_base', None),
    (0x08069058, 0x0201b290, 'gDuelPhaseFlags', 'dispatch_zone11_phase_flags_base', None),

    # ---- gP1FieldArrayCBase = 0x0201c600 (2 slots) ----
    (0x08068ac0, 0x0201c600, 'gP1FieldArrayCBase', 'dispatch_state_zone_field_c_base', None),
    (0x08068b1c, 0x0201c600, 'gP1FieldArrayCBase', 'dispatch_state_zone_field_c_base_b', None),

    # ---- EQUIP_PHASE_FRAME_OFF = 0x4a4 (2 slots) ----
    (0x08068ad0, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'dispatch_state_zone_phase_frame_off',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),
    (0x08068b14, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF', 'dispatch_state_zone_phase_frame_off_b',
     'EQUIP_PHASE_FRAME_OFF=0x4a4: [gDuelPhaseFlags+0x4a4] equip effect frame counter'),

    # ---- gP1HandSlotArray = 0x0201c8f8 (1 slot) ----
    (0x08068824, 0x0201c8f8, 'gP1HandSlotArray', 'invoke_hand_slot_oam_hand_base', None),

    # ---- LP_CARD_TRACK_NEXT_OFF = 0x1daa (1 slot) ----
    (0x08068680, 0x00001daa, 'LP_CARD_TRACK_NEXT_OFF', 'advance_guard_lp_track_next_off',
     'LP_CARD_TRACK_NEXT_OFF=0x1daa: [gP1LifePoints+0x1daa] LP card-ref next array slot'),

    # ---- LP_CARD_TRACK_BASE_OFF = 0x1da8 (1 slot) ----
    (0x080690d4, 0x00001da8, 'LP_CARD_TRACK_BASE_OFF', 'dispatch_zone11_lp_track_base_off',
     'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card-ref tracking array base'),

    # ---- P1LP_BLOCK2_OFF_1CE8 = 0x1ce8 (1 slot) ----
    (0x080690d8, 0x00001ce8, 'P1LP_BLOCK2_OFF_1CE8', 'dispatch_zone11_lp_block2_off',
     'P1LP_BLOCK2_OFF_1CE8=0x1ce8: [gP1LifePoints+0x1ce8] LP display block2 field'),

    # ---- OAM_EFFECT_SLOT_TILE_P1 = 0x8056 (1 slot) ----
    (0x08068c70, 0x00008056, 'OAM_EFFECT_SLOT_TILE_P1', 'dispatch_lp_field_tile_p2',
     'OAM_EFFECT_SLOT_TILE_P1=0x8056: player_id==1 path selects tile P1 in dispatch_equip_lp_field_state_by_card_id'),

    # ---- CID reuse slots ----
    (0x08068064, 0x0000131c, 'cid_131c', 'scan_effect_cid_131c', None),
    (0x08068068, 0x000011f0, 'GREENKAPPA_CID', 'scan_effect_greenkappa_cid', None),
    (0x0806806c, 0x00000ffa, 'REAPER_OF_CARDS_CID', 'scan_effect_reaper_cid', None),
    (0x0806807c, 0x00001246, 'HARPIES_FEATHER_DUSTER_CID', 'scan_effect_hfd_cid', None),
    (0x08068098, 0x0000134d, 'DRIVING_SNOW_CID', 'scan_effect_driving_snow_cid', None),
    (0x080680b0, 0x0000149b, 'BAIT_DOLL_CID', 'scan_effect_bait_doll_cid', None),
    (0x080680b4, 0x00001364, 'NOBLEMAN_EXTERMINATION_CID', 'scan_effect_nobleman_ext_cid', None),
    (0x08068174, 0x000016b8, 'CRIMSON_NINJA_CID', 'scan_effect_crimson_ninja_cid', None),

    # ---- BLAST_SPHERE_CID = 0x1286 (1 slot) -- NEW card_info.inc ----
    (0x08068600, 0x00001286, 'BLAST_SPHERE_CID', 'invoke_lp_chain_blast_sphere_cid',
     'BLAST_SPHERE_CID=0x1286: pw=26302522; cmp card_id==0x1286 for Blast Sphere LP chain state'),

    # ---- BIRDFACE_CID = 0x139d (1 slot) -- NEW card_info.inc ----
    (0x08068760, 0x0000139d, 'BIRDFACE_CID', 'tick_sm_birdface_cid',
     'BIRDFACE_CID=0x139d: pw=45547649; named card branch in tick_equip_effect_display_state_machine caseD_7f'),

    # ---- gEquipLpZoneEntryBase = 0x0201e500 (1 slot) -- NEW ewram.inc ----
    (0x08068c74, 0x0201e500, 'gEquipLpZoneEntryBase', 'dispatch_lp_field_zone_entry_base',
     'gEquipLpZoneEntryBase=0x0201e500: EWRAM equip LP zone entry buffer base; reads card_type bits for sprite_code'),

    # ---- EQUIP_SLOT_SCORE_CAP = 0xffff (1 slot) -- NEW oam_attr.inc (domain: score saturation cap) ----
    (0x08068f08, 0x0000ffff, 'EQUIP_SLOT_SCORE_CAP', 'apply_slot_score_cap',
     'EQUIP_SLOT_SCORE_CAP=0xffff: score saturation cap in apply_equip_slot_sprite_via_zone_match_and_score'),

    # ---- OAM_EQUIP_SPRITE_TILE_P2_1B = 0x801b (1 slot) -- NEW oam_attr.inc ----
    (0x08068f70, 0x0000801b, 'OAM_EQUIP_SPRITE_TILE_P2_1B', 'enqueue_sprite_tile_p2_1b',
     'OAM_EQUIP_SPRITE_TILE_P2_1B=0x801b: P2 equip sprite tile region; player_id==1 first sprite code'),

    # ---- OAM_EQUIP_SPRITE_TILE_P2_1C = 0x801c (1 slot) -- NEW oam_attr.inc ----
    (0x08068f74, 0x0000801c, 'OAM_EQUIP_SPRITE_TILE_P2_1C', 'enqueue_sprite_tile_p2_1c',
     'OAM_EQUIP_SPRITE_TILE_P2_1C=0x801c: P2 equip sprite tile region; player_id==1 second sprite code'),

    # ---- EQUIP_OAM_ENTRY_ATTR_14F8 = 0x14f8 (1 slot) -- NEW ewram.inc ----
    (0x08068ff0, 0x000014f8, 'EQUIP_OAM_ENTRY_ATTR_14F8', 'dispatch_neo_daedalus_oam_entry_attr',
     'EQUIP_OAM_ENTRY_ATTR_14F8=0x14f8: OR component for OAM entry attr word; orrs r1,r2 then sp[0x4]'),
]

# ---------------------------------------------------------------------------
# B. REF_SLOTS: (slot_addr, target_addr, gas_label, slot_label, eol_ascii_or_None)
#    Adds a DATA reference from slot_addr to target_addr; sets labels on both.
# ---------------------------------------------------------------------------
REF_SLOTS = [
    # PTR_gP1LifePoints_0806867c -- already emits .word gP1LifePoints; only rename slot label
    (0x0806867c, 0x0201c4e0, 'gP1LifePoints',
     'advance_guard_lp_track_base_ptr',
     'gP1LifePoints=0x0201c4e0: LP track base for advance_equip_effect_display_zone_match_guard'),

    # DAT_080686a8 -- switch table ptr -> switchD_080686a2__switchdataD_080686ac
    (0x080686a8, 0x080686ac, 'switchD_080686a2__switchdataD_080686ac',
     'tick_sm_switch_table_ptr',
     'switch table ptr for tick_equip_effect_display_state_machine (28 entries, state-0x64 range)'),

    # DWORD_0806905c -- gP1LifePoints ref slot A
    (0x0806905c, 0x0201c4e0, 'gP1LifePoints',
     'dispatch_zone11_gp1lp_base_a',
     'gP1LifePoints=0x0201c4e0: LP base for dispatch_equip_zone11_sprite_or_lp_row_by_state path A'),

    # DWORD_080690d0 -- gP1LifePoints ref slot B
    (0x080690d0, 0x0201c4e0, 'gP1LifePoints',
     'dispatch_zone11_gp1lp_base_b',
     'gP1LifePoints=0x0201c4e0: LP base for dispatch_equip_zone11_sprite_or_lp_row_by_state path B'),
]

# ---------------------------------------------------------------------------
# C. PLATE_REWRITES: (func_addr, func_name, new_plate_ascii)
#    Rewrites existing CJK-mojibake plate with correct ASCII text.
#    All text must be pure ASCII.
# ---------------------------------------------------------------------------
PLATE_REWRITES = [
    # dispatch_equip_slot_sprite_by_zone_type @ 0x0806882c (asm line 10092)
    # CJK mojibake plate -> ASCII replacement
    (0x0806882c,
     'dispatch_equip_slot_sprite_by_zone_type',
     'Dispatches equip slot sprite based on zone_type code in effect_slot[+0xc]. '
     'type==1: calls invoke_equip_slot_eligibility_via_effect_node_bitmap(slot). '
     'type==2: aggregates col_nibble from both player sides of gDuelFieldSlots (stride 0x868), '
     'compares sum with slot[+0x4] bits[14:8] target; on match calls '
     'check_effect_slot_matches_zone_entry + read_effect_slot_side_and_type + '
     'invoke_effect_node_with_active_flag_3arg; on activation extracts player_id/slot_group '
     'and calls enqueue_equip_chain_slot_sprite_with_pair_lookup. '
     'Other type or mismatch: returns 0. indeg=0, Sub-type A.'),
]

# ---------------------------------------------------------------------------
# D. DISASM + CREATE_FUNC: THUMB stub @ 0x08068828 (4B: movs r0,#0; bx lr)
#    Creates check_equip_eligible_always_false with plate comment.
# ---------------------------------------------------------------------------
DISASM_STUBS = [
    # (start_addr, length_bytes, func_name, plate_ascii)
    (0x08068828, 4,
     'check_equip_eligible_always_false',
     'Always-false equip eligibility stub; referenced by Royal Decree (0x1302), '
     'Imperial Order (0x1360), The Emperor\'s Holiday (0x1495) handler table fn_eligible slots; '
     'movs r0,#0; bx lr. indeg=0 (dispatch table only).'),
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
        print("[SKIP] EQ 0x%08x (%s) value mismatch -- WARN treated as FAIL" % (slot_addr, eq_name))
        return False

    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%x  label=%s" % (slot_addr, eq_name, value, slot_label))
        return True

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

    # EOL comment (ASCII only)
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


def _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol):
    """Add DATA reference from slot_addr to target_addr; set labels on both."""
    a_slot = _addr(slot_addr)
    a_target = _addr(target_addr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  target=%s  slot=%s" % (
            slot_addr, target_addr, gas_label, slot_label))
        return

    # Label on target (only if not already present with this name)
    existing_t = list(sym_tbl.getSymbols(a_target))
    tnames = [s.getName() for s in existing_t]
    if gas_label not in tnames:
        sym_tbl.createLabel(a_target, gas_label, SourceType.USER_DEFINED)

    # DATA reference slot -> target
    ref_mgr.addMemoryReference(a_slot, a_target, RefType.DATA, SourceType.USER_DEFINED, 0)
    # Set primary for target label
    syms = list(sym_tbl.getSymbols(a_target))
    for s in syms:
        if s.getName() == gas_label:
            s.setPrimary()
            break

    # Slot label
    existing_s = list(sym_tbl.getSymbols(a_slot))
    snames = [s.getName() for s in existing_s]
    if slot_label not in snames:
        sym_tbl.createLabel(a_slot, slot_label, SourceType.USER_DEFINED)

    # EOL on slot
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a_slot)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if bad:
                print("[WARN] non-ASCII in REF EOL @ 0x%08x -- skipping" % slot_addr)
            else:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr, target_addr, gas_label, slot_label))


def _set_plate(func_addr, func_name, plate_text):
    """Set (rewrite) plate comment for a function. plate_text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x %s -- aborting" % (func_addr, func_name))
        return False

    a = _addr(func_addr)
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] PLATE @ 0x%08x %s (%d chars)" % (func_addr, func_name, len(plate_text)))
        return True

    cu = listing.getCodeUnitAt(a)
    if cu is None:
        # Try to find the function
        fn_mgr = currentProgram.getFunctionManager()
        fn = fn_mgr.getFunctionAt(a)
        if fn is not None:
            cu = listing.getCodeUnitAt(a)
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLATE ok] %s @ 0x%08x (%d chars)" % (func_name, func_addr, len(plate_text)))
        return True
    else:
        print("[PLATE WARN] no code unit @ 0x%08x %s" % (func_addr, func_name))
        return False


def _disasm_thumb_and_create_func(start_addr, length, func_name, plate_text):
    """
    Disassemble a THUMB stub at start_addr for `length` bytes,
    create function, set plate comment. All text must be pure ASCII.
    """
    bad = any(ord(ch) > 127 for ch in plate_text)
    if bad:
        print("[DISASM FAIL] non-ASCII in plate @ 0x%08x %s -- aborting" % (start_addr, func_name))
        return

    a_start = _addr(start_addr)
    a_end = _addr(start_addr + length - 1)
    sym_tbl = currentProgram.getSymbolTable()
    fn_mgr = currentProgram.getFunctionManager()
    listing = currentProgram.getListing()

    if DRY:
        print("[dry] DISASM THUMB @ 0x%08x len=%d -> %s" % (start_addr, length, func_name))
        return

    # 1. Clear listing for the range
    addr_set = AddressSet(a_start, a_end)
    listing.clearCodeUnits(a_start, a_end, False)

    # 2. Set THUMB mode context (tMode=1)
    ctx = currentProgram.getProgramContext()
    try:
        tmode_reg = ctx.getRegister("TMode")
        if tmode_reg is not None:
            ctx.setValue(tmode_reg, a_start, a_end, java.math.BigInteger.ONE)
            print("[DISASM] setTMode THUMB @ 0x%08x..0x%08x" % (start_addr, start_addr + length - 1))
    except Exception as e:
        print("[DISASM WARN] setTMode failed @ 0x%08x: %s" % (start_addr, e))

    # 3. Disassemble (restrict to exact range)
    cmd = DisassembleCommand(a_start, addr_set, True)
    cmd.applyTo(currentProgram, monitor)
    print("[DISASM] DisassembleCommand @ 0x%08x len=%d" % (start_addr, length))

    # 4. Create function
    existing = fn_mgr.getFunctionAt(a_start)
    if existing is not None:
        if existing.getName() != func_name:
            existing.setName(func_name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing @ 0x%08x -> %s" % (start_addr, func_name))
        else:
            print("[FN ] already exists: %s @ 0x%08x" % (func_name, start_addr))
    else:
        cmd2 = CreateFunctionCmd(func_name, a_start, None, SourceType.USER_DEFINED)
        if cmd2.applyTo(currentProgram):
            print("[FN ] created %s @ 0x%08x" % (func_name, start_addr))
        else:
            print("[warn] createFunction failed @ 0x%08x: %s" % (start_addr, cmd2.getStatusMsg()))
            # Fallback: create label
            existing_s = list(sym_tbl.getSymbols(a_start))
            snames = [s.getName() for s in existing_s]
            if func_name not in snames:
                sym_tbl.createLabel(a_start, func_name, SourceType.USER_DEFINED)
            print("[FN ] created label (fallback) %s @ 0x%08x" % (func_name, start_addr))

    # 5. Set plate comment
    cu = listing.getCodeUnitAt(a_start)
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, plate_text)
        print("[PLATE ok] %s @ 0x%08x (%d chars)" % (func_name, start_addr, len(plate_text)))
    else:
        print("[PLATE WARN] no code unit @ 0x%08x after disasm" % start_addr)

    # 6. Create USER label at start (ensure it's primary)
    existing_s = list(sym_tbl.getSymbols(a_start))
    snames = [s.getName() for s in existing_s]
    if func_name not in snames:
        sym_tbl.createLabel(a_start, func_name, SourceType.USER_DEFINED)
    for s in list(sym_tbl.getSymbols(a_start)):
        if s.getName() == func_name:
            s.setPrimary()
            break
    print("[DISASM] done: %s @ 0x%08x" % (func_name, start_addr))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== RefineF08Seg5Slots (DRY=%s) ===" % DRY)
    print("  Seg-5: 0x08067fa4..0x080690dc")
    print("  EQ=%d  REF=%d  PLATE_REWRITES=%d  DISASM_STUBS=%d" % (
        len(EQ_SLOTS), len(REF_SLOTS), len(PLATE_REWRITES), len(DISASM_STUBS)))

    # A. EQ_SLOTS
    print("\n--- A. EQ_SLOTS (%d) ---" % len(EQ_SLOTS))
    eq_ok = 0
    eq_fail = 0
    for entry in EQ_SLOTS:
        slot_addr, value, eq_name, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        # pre-check value
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

    # B. REF_SLOTS
    print("\n--- B. REF_SLOTS (%d) ---" % len(REF_SLOTS))
    ref_ok = 0
    for entry in REF_SLOTS:
        slot_addr, target_addr, gas_label, slot_label = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        _apply_ref(slot_addr, target_addr, gas_label, slot_label, eol)
        ref_ok += 1
    print("  REF done: %d" % ref_ok)

    # C. PLATE_REWRITES
    print("\n--- C. PLATE_REWRITES (%d) ---" % len(PLATE_REWRITES))
    plate_ok = 0
    for func_addr, func_name, plate_text in PLATE_REWRITES:
        if _set_plate(func_addr, func_name, plate_text):
            plate_ok += 1
    print("  PLATE_REWRITES done: %d" % plate_ok)

    # D. DISASM_STUBS (THUMB) + CREATE_FUNC
    print("\n--- D. DISASM_STUBS (%d) ---" % len(DISASM_STUBS))
    for start_addr, length, func_name, plate_text in DISASM_STUBS:
        _disasm_thumb_and_create_func(start_addr, length, func_name, plate_text)

    print("\n=== RefineF08Seg5Slots DONE ===")
    print("  EQ=%d/%d ok  REF=%d  PLATE_REWRITES=%d  DISASM_STUBS=%d" % (
        eq_ok, len(EQ_SLOTS), ref_ok, plate_ok, len(DISASM_STUBS)))


main()
