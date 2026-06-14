# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg8Blocks.py -- F07 Seg-8 R4 disasm (5 blocks, 6 new functions)
#
# Block1: 0x08062378..0x080623a3 (0x2c B)
#   fn entry @ 0x08062378: check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3
#   Dispatch table 0x09e42274; CID=0x17f3 (Mind Wipe, pw=52817046)
#   fn_eligible ptr: 0x09e42280 value=0x08062379 (fn+1 THUMB)
#   bx lr @ 0x0806239a; lit pool: 0x0806239c(gP1LifePoints), 0x080623a0(PLAYER_BLOCK_STRIDE)
#   Semantics: subs r0,#1; cmp r0,#2; bhi->return 0; else return 1
#              pass: opp_zone_count in {1,2,3}
#
# Block2: 0x080623ec..0x0806244b (0x60 B) -- 2 functions
#   F1 entry @ 0x080623ec: check_equip_slot_eligible_opp_is_active_field_eq2_for_cid_17fc
#   Dispatch table 0x09e42334; CID=0x17fc (Taunt, pw=90740329)
#   F1 lit pool embedded: 0x08062410(gP1LifePoints), 0x08062414(P1LP_BLOCK2_OFF_1CE8=0x1ce8), 0x08062418(FIELD_STATE_OFF=0x1cf4)
#   F1 bx lr @ 0x0806241e; F1 end @ 0x08062420
#   Semantics: opp_player==gP1LP[0x1ce8] AND field_state==2 -> return 1
#
#   F2 entry @ 0x08062420: check_equip_slot_eligible_opp_lp_zone_count_above7_for_cid_1801
#   Dispatch table 0x09e4237c; CID=0x1801 (Heavy Slump, pw=52417194)
#   F2 lit pool: 0x08062444(gP1LifePoints), 0x08062448(PLAYER_BLOCK_STRIDE=0x868)
#   F2 bx lr @ 0x08062440; F2 end @ 0x08062442
#   Semantics: gP1LP[(1-player)*0x868+0xc] > 7 -> return 1
#
# Block3: 0x0806246e..0x08062497 (0x2a B)
#   2B alignment pad at 0x0806246e
#   fn entry @ 0x08062470: check_equip_slot_eligible_opp_lp_field14_nonzero_for_cid_1804
#   Dispatch table 0x09e423ac; CID=0x1804 (Cemetary Bomb, pw=51394546)
#   bx lr @ 0x0806248c; lit pool: 0x08062490(gP1LifePoints), 0x08062494(PLAYER_BLOCK_STRIDE)
#   Semantics: gP1LP[(1-player)*0x868+0x14] != 0 -> return 1
#
# Block4: 0x08062a9c..0x08062ac7 (0x2c B)
#   fn entry @ 0x08062a9c: check_equip_slot_eligible_opp_lp_field0c_zero_for_cid_184d
#   Dispatch table 0x09e42574; CID=0x184d (Mind Haxorz, pw=75392615)
#   lit pool embedded: 0x08062abc(gP1LifePoints), 0x08062ac0(PLAYER_BLOCK_STRIDE)
#   bx lr @ 0x08062ac6; end @ 0x08062ac8
#   Semantics: gP1LP[(1-player)*0x868+0xc] == 0 -> return 1; else return 2
#
# Block5: 0x08062c52..0x08062cb7 (0x66 B)
#   2B alignment pad at 0x08062c52
#   fn entry @ 0x08062c54: check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853
#   Dispatch table 0x09e425ec; CID=0x1853 (Covering Fire, pw=74458486)
#   lit pool: 0x08062ca8(gEquipChainSlotRefs), 0x08062cac(PLAYER_BLOCK_STRIDE), 0x08062cb0(gDuelFieldSlots)
#   bx lr @ 0x08062cb6; end @ 0x08062cb8
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_183408-pre-F07Seg8

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_flow(addr):
    """Disassemble at addr using flow continuation."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
    """Create a named function at addr."""
    a = _addr(addr)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing function at 0x%08x -> %s" % (addr, name))
        else:
            print("[FN ] function already exists at 0x%08x: %s" % (addr, name))
        return
    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
    """Set PLATE_COMMENT. text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x -- skipping" % addr)
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr))
    if cu is None:
        print("[PLATE FAIL] no CodeUnit at 0x%08x" % addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[PLATE ok] 0x%08x (%d chars)" % (addr, len(text)))


def _create_dword_eq(slot_addr, label_name, const_name, value):
    """Force a DWORD at slot_addr, set label, add equate."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    et = currentProgram.getEquateTable()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    eq = et.getEquate(const_name)
    if eq is None:
        eq = et.createEquate(const_name, value)
    eq.addReference(a, 0)
    print("[DW+EQ] 0x%08x -> %s (%s=0x%x)" % (slot_addr, label_name, const_name, value))


# ---------------------------------------------------------------------------
# BLOCK definitions: (block_lo, block_hi, [(fn_addr, fn_name)], pool_slots, plate)
#
# pool_slots: list of (slot_addr, label_name, const_name, value)
# ---------------------------------------------------------------------------

# ---- Block1 ----
BLOCK1_LO   = 0x08062378
BLOCK1_HI   = 0x080623a3
BLOCK1_FNS  = [
    (0x08062378, 'check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3'),
]
BLOCK1_POOL = [
    (0x0806239c, 'gp1lp_ref_08062378_lp0', 'gP1LifePoints',     0x0201c4e0),
    (0x080623a0, 'player_stride_08062378_lp1', 'PLAYER_BLOCK_STRIDE', 0x00000868),
]
BLOCK1_PLATE = (
    'fn_eligible for CID 0x17f3 (Mind Wipe, pw=52817046); '
    'reached via card effect handler dispatch table at ROM 0x09e42274. '
    'Reads gP1LifePoints[(1-player)*PLAYER_BLOCK_STRIDE+0xc] (opp LP zone count); '
    'returns 1 if opp_zone_count in {1,2,3} (zone_count-1 <= 2 unsigned), else 0. '
    'Logic: subs r0,#1; cmp r0,#2; bhi->r3=0; else r3=1. '
    'Note: zone_count=0 wraps to 0xFFFFFFFF (unsigned > 2) -> also returns 0. '
    'bx lr exit. Lit pool: gP1LifePoints(0x0201c4e0), PLAYER_BLOCK_STRIDE(0x868).'
)

# ---- Block2-F1 ----
BLOCK2_LO   = 0x080623ec
BLOCK2_HI   = 0x0806244b
# Two functions in this block; disasm from F1 entry first, then F2
BLOCK2_FNS  = [
    (0x080623ec, 'check_equip_slot_eligible_opp_is_active_field_eq2_for_cid_17fc'),
    (0x08062420, 'check_equip_slot_eligible_opp_lp_zone_count_above7_for_cid_1801'),
]
# F1 embedded lit pool + F2 lit pool
BLOCK2_POOL = [
    # F1 embedded lit pool (3 slots)
    (0x08062410, 'gp1lp_ref_08062410',           'gP1LifePoints',          0x0201c4e0),
    (0x08062414, 'block2_f1_off_1ce8_08062414',   'P1LP_BLOCK2_OFF_1CE8',   0x00001ce8),
    (0x08062418, 'block2_f1_field_state_08062418','FIELD_STATE_OFF',        0x00001cf4),
    # F2 lit pool (2 slots)
    (0x08062444, 'gp1lp_ref_08062444',            'gP1LifePoints',          0x0201c4e0),
    (0x08062448, 'player_stride_08062448',         'PLAYER_BLOCK_STRIDE',    0x00000868),
]
BLOCK2_F1_PLATE = (
    'fn_eligible for CID 0x17fc (Taunt, pw=90740329); '
    'reached via card effect handler dispatch table at ROM 0x09e42334. '
    'Guards: (1) opp_player == gP1LP[0x1ce8] (P1LP_BLOCK2_OFF_1CE8; active player id); '
    '(2) gP1LP[0x1cf4] (FIELD_STATE_OFF; field state) == 2. '
    'Returns 1 on pass, 0 otherwise. bx lr exit. '
    'Lit pool embedded at 0x8062410: gP1LifePoints/DUEL_ACTIVE_PLAYER_OFF/FIELD_STATE_OFF.'
)
BLOCK2_F2_PLATE = (
    'fn_eligible for CID 0x1801 (Heavy Slump, pw=52417194); '
    'reached via card effect handler dispatch table at ROM 0x09e4237c. '
    'Reads gP1LifePoints[(1-player)*PLAYER_BLOCK_STRIDE+0xc] (opp LP zone count); '
    'returns 1 if opp_count > 7 (bls->fail path), else 0. '
    'bx lr exit. Lit pool: gP1LifePoints(0x0201c4e0)/PLAYER_BLOCK_STRIDE(0x868) @ 0x8062444.'
)

# ---- Block3 ----
BLOCK3_LO   = 0x0806246e
BLOCK3_HI   = 0x08062497
BLOCK3_FNS  = [
    (0x08062470, 'check_equip_slot_eligible_opp_lp_field14_nonzero_for_cid_1804'),
]
BLOCK3_POOL = [
    (0x08062490, 'gp1lp_ref_08062490',     'gP1LifePoints',      0x0201c4e0),
    (0x08062494, 'player_stride_08062494', 'PLAYER_BLOCK_STRIDE', 0x00000868),
]
BLOCK3_PLATE = (
    'fn_eligible for CID 0x1804 (Cemetary Bomb, pw=51394546); '
    'reached via card effect handler dispatch table at ROM 0x09e423ac. '
    'Reads gP1LifePoints[(1-player)*PLAYER_BLOCK_STRIDE+0x14] (opp field[+0x14]); '
    'returns 1 if nonzero, else 0. '
    '.zero 2 alignment pad at 0x806246e before fn entry at 0x8062470. '
    'bx lr exit. Lit pool: gP1LifePoints/PLAYER_BLOCK_STRIDE @ 0x8062490.'
)

# ---- Block4 ----
BLOCK4_LO   = 0x08062a9c
BLOCK4_HI   = 0x08062ac7
BLOCK4_FNS  = [
    (0x08062a9c, 'check_equip_slot_eligible_opp_lp_field0c_zero_for_cid_184d'),
]
BLOCK4_POOL = [
    # Embedded lit pool before bx lr
    (0x08062abc, 'gp1lp_ref_08062abc',     'gP1LifePoints',      0x0201c4e0),
    (0x08062ac0, 'player_stride_08062ac0', 'PLAYER_BLOCK_STRIDE', 0x00000868),
]
BLOCK4_PLATE = (
    'fn_eligible for CID 0x184d (Mind Haxorz, pw=75392615); '
    'reached via card effect handler dispatch table at ROM 0x09e42574. '
    'Reads gP1LifePoints[(1-player)*PLAYER_BLOCK_STRIDE+0xc] (opp LP zone count); '
    'returns 1 if zero (no opp LP zones), returns 2 if nonzero. '
    'bx lr exit. Lit pool embedded @ 0x8062abc: gP1LifePoints(0x0201c4e0)/PLAYER_BLOCK_STRIDE(0x868).'
)

# ---- Block5 ----
BLOCK5_LO   = 0x08062c52
BLOCK5_HI   = 0x08062cb7
BLOCK5_FNS  = [
    (0x08062c54, 'check_equip_slot_eligible_chain_refs_slot_status_for_cid_1853'),
]
BLOCK5_POOL = [
    (0x08062ca8, 'equip_chain_refs_08062ca8', 'gEquipChainSlotRefs', 0x0201bb90),
    (0x08062cac, 'player_stride_08062cac',    'PLAYER_BLOCK_STRIDE', 0x00000868),
    (0x08062cb0, 'duel_field_slots_08062cb0', 'gDuelFieldSlots',     0x0201c510),
]
BLOCK5_PLATE = (
    'fn_eligible for CID 0x1853 (Covering Fire, pw=74458486); '
    'reached via card effect handler dispatch table at ROM 0x09e425ec. '
    'Guards: reads gEquipChainSlotRefs[+0x8]/[+0x18] fields + slot byte[+2] player bit '
    '+ gDuelFieldSlots slot halfword[+0x8]/[+0x6]; zone-type pre-filter (cmp vs 0xd and 0x14). '
    '.zero 2 alignment pad at 0x8062c52 before fn entry at 0x8062c54. '
    'bx lr exit. Lit pool @ 0x8062ca8: '
    'gEquipChainSlotRefs(0x0201bb90)/PLAYER_BLOCK_STRIDE(0x868)/gDuelFieldSlots(0x0201c510).'
)

# ---- P1LP_BLOCK2_OFF_1CE8 (0x1ce8) ----
# Already defined in ewram.inc: P1LP_BLOCK2_OFF_1CE8 = 0x1ce8
# Distinct from DUEL_ACTIVE_PLAYER_OFF=0x1cb8 in duel_field.inc.


def main():
    print("=== DisassembleF07Seg8Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] Would process 5 blocks, 6 functions:")
        print("  Block1 0x%08x..0x%08x fn@0x%08x" % (BLOCK1_LO, BLOCK1_HI, BLOCK1_FNS[0][0]))
        print("  Block2 0x%08x..0x%08x fn@0x%08x + fn@0x%08x" % (BLOCK2_LO, BLOCK2_HI, BLOCK2_FNS[0][0], BLOCK2_FNS[1][0]))
        print("  Block3 0x%08x..0x%08x fn@0x%08x (2B pad at 0x0806246e)" % (BLOCK3_LO, BLOCK3_HI, BLOCK3_FNS[0][0]))
        print("  Block4 0x%08x..0x%08x fn@0x%08x" % (BLOCK4_LO, BLOCK4_HI, BLOCK4_FNS[0][0]))
        print("  Block5 0x%08x..0x%08x fn@0x%08x (2B pad at 0x08062c52)" % (BLOCK5_LO, BLOCK5_HI, BLOCK5_FNS[0][0]))
        print("[dry] 14 literal pool slots: all EQ")
        return

    # =========================================================================
    # Block1: 0x08062378..0x080623a3 (1 fn)
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x ---" % (BLOCK1_LO, BLOCK1_HI))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    _disasm_flow(BLOCK1_FNS[0][0])
    for sp, ln, cn, val in BLOCK1_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK1_FNS[0][0], BLOCK1_FNS[0][1])
    _set_plate(BLOCK1_FNS[0][0], BLOCK1_PLATE)

    # =========================================================================
    # Block2: 0x080623ec..0x0806244b (2 fn: F1 @ 0x080623ec, F2 @ 0x08062420)
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (2 fn) ---" % (BLOCK2_LO, BLOCK2_HI))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    # Disassemble F1 first; F2 is a separate function starting at 0x08062420
    _disasm_flow(BLOCK2_FNS[0][0])   # F1 @ 0x080623ec
    _disasm_flow(BLOCK2_FNS[1][0])   # F2 @ 0x08062420
    # Literal pool slots (both F1 embedded and F2 tail)
    for sp, ln, cn, val in BLOCK2_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK2_FNS[0][0], BLOCK2_FNS[0][1])
    _set_plate(BLOCK2_FNS[0][0], BLOCK2_F1_PLATE)
    _create_function(BLOCK2_FNS[1][0], BLOCK2_FNS[1][1])
    _set_plate(BLOCK2_FNS[1][0], BLOCK2_F2_PLATE)

    # =========================================================================
    # Block3: 0x0806246e..0x08062497 (1 fn, 2B pad at 0x0806246e)
    # =========================================================================
    print("\n--- Block3: 0x%08x..0x%08x (1 fn; 2B pad) ---" % (BLOCK3_LO, BLOCK3_HI))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)
    # fn entry at 0x08062470 (pad at 0x0806246e skipped)
    _disasm_flow(BLOCK3_FNS[0][0])
    for sp, ln, cn, val in BLOCK3_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK3_FNS[0][0], BLOCK3_FNS[0][1])
    _set_plate(BLOCK3_FNS[0][0], BLOCK3_PLATE)

    # =========================================================================
    # Block4: 0x08062a9c..0x08062ac7 (1 fn, embedded lit pool)
    # =========================================================================
    print("\n--- Block4: 0x%08x..0x%08x (1 fn) ---" % (BLOCK4_LO, BLOCK4_HI))
    _clear_and_set_thumb(BLOCK4_LO, BLOCK4_HI)
    _disasm_flow(BLOCK4_FNS[0][0])
    for sp, ln, cn, val in BLOCK4_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK4_FNS[0][0], BLOCK4_FNS[0][1])
    _set_plate(BLOCK4_FNS[0][0], BLOCK4_PLATE)

    # =========================================================================
    # Block5: 0x08062c52..0x08062cb7 (1 fn, 2B pad at 0x08062c52)
    # =========================================================================
    print("\n--- Block5: 0x%08x..0x%08x (1 fn; 2B pad) ---" % (BLOCK5_LO, BLOCK5_HI))
    _clear_and_set_thumb(BLOCK5_LO, BLOCK5_HI)
    # fn entry at 0x08062c54 (pad at 0x08062c52 skipped)
    _disasm_flow(BLOCK5_FNS[0][0])
    for sp, ln, cn, val in BLOCK5_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK5_FNS[0][0], BLOCK5_FNS[0][1])
    _set_plate(BLOCK5_FNS[0][0], BLOCK5_PLATE)

    print("\n=== DisassembleF07Seg8Blocks DONE ===")
    print("  6 functions created across 5 blocks")
    print("  14 literal pool slots (all EQ)")
    print("  All blocks cleared + THUMB mode set before disassembly")


main()
