# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg10Blocks.py -- F07 Seg-10 R4 disasm (4 blocks, 4 new functions)
#
# Block1: 0x0806384e..0x08063877 (0x2a B)
#   2B alignment pad at 0x0806384e
#   fn entry @ 0x08063850: check_zone_field0c_is_zero_for_player
#   fn_eligible for: CID=0x1926 (Fire Darts) via 0x09e42ad8
#                    CID=0x1775 (Return Zombie) via 0x09e45e38
#   Code: 0x3850..0x3867 (0x18 B); zero pad: 0x3868..0x3869 (2B)
#   Lit pool: 0x3870(gP1LifePoints=0x0201c4e0), 0x3874(PLAYER_BLOCK_STRIDE=0x868)
#   bx lr @ 0x08063866 (pop {r3}/bx r3 epilogue at 0x08063862..0x08063866)
#   Semantics: reads gP1LP[player*0x868+0xc]; returns 1 if field_0xc==0, 0 if nonzero
#
# Block2: 0x08063cf0..0x08063d03 (0x14 B)
#   fn entry @ 0x08063cf0: check_chain_field8_is_zero
#   fn_eligible for: CID=0x1954 (VWXYZ-Dragon Catapult Cannon) via 0x09e45328
#   Code: 0x3cf0..0x3cfb (0xc B), lit pool at 0x3cfc, code: 0x3d00..0x3d03
#   Lit pool: 0x3cfc(gEquipChainSlotRefs=0x0201bb90)
#   bx lr @ 0x08063d02; end @ 0x08063d03
#   Semantics: reads [gEquipChainSlotRefs+8]; returns 1 if zero, 0 if nonzero
#
# Block3: 0x08063db4..0x08063df3 (0x40 B)
#   fn entry @ 0x08063db4: check_slot_zone_code_and_link_field_for_cid_195e
#   fn_eligible for: CID=0x195e (Chthonian Blast) via 0x09e42cd0
#   Code: 0x3db4..0x3deb (0x38 B); lit pool: 0x3dec(0x00fa8000)
#   bx lr @ 0x08063df0; end @ 0x08063df3
#   Semantics:
#     zone type bits[11:6] must be 0x16 or 0x1b;
#     bit9 of slot[+0x14] must match slot.player_id;
#     lsrs chain (always r0=0 for 32-bit), bgt(0>4)=false -> falls through;
#     (slot[+0x14] & 0x00fa8000) must == 0x00728000 (0xe5<<15)
#   NOTE: ands r2,r0 (0x4002 = ANDS Rd=r2, Rs=r0); 0xe5<<15=0x00728000 (not 0x72800000)
#
# Block4: 0x08063fc4..0x08063fe7 (0x24 B)
#   fn entry @ 0x08063fc4: check_either_player_lp_slot_active
#   fn_eligible for: CID=0x1976 (Simultaneous Loss) via 0x09e42da8
#   Code: 0x3fc4..0x3fd9 (0x16 B); zero pad: 0x3fda..0x3fdb (2B)
#   Lit pool: 0x3fdc(gP1LifePoints=0x0201c4e0), 0x3fe0(0x00000878)
#   Code: 0x3fe4..0x3fe7 (bne target: movs r0,#1; bx lr)
#   bx lr @ 0x08063fe6; end @ 0x08063fe7
#   Semantics: slot_ptr (r0) unused; checks gP1LP[+0x10] (player0) OR gP1LP[+0x878] (player1)
#              returns 1 if either nonzero (LP zone active)
#   NOTE: both bne targets land at 0x08063fe4 (NOT 0x08063fe2 which is alignment pad)
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_204519-pre-F07Seg10

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


def _create_dword_raw(slot_addr, label_name, eol=None):
    """Force a DWORD at slot_addr with plain label (no equate), optional EOL."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[DW+LBL] 0x%08x -> %s" % (slot_addr, label_name))


# ---------------------------------------------------------------------------
# BLOCK1: 0x0806384e..0x08063877 (0x2a B)
#   2B alignment pad at 0x0806384e, fn entry @ 0x08063850
# ---------------------------------------------------------------------------
BLOCK1_LO  = 0x0806384e
BLOCK1_HI  = 0x08063877
BLOCK1_FN  = (0x08063850, 'check_zone_field0c_is_zero_for_player')
BLOCK1_POOL = [
    (0x08063870, 'gp1lp_ptr_08063870',         'gP1LifePoints',       0x0201c4e0),
    (0x08063874, 'player_stride_08063874',      'PLAYER_BLOCK_STRIDE', 0x00000868),
]
BLOCK1_PLATE = (
    'fn_eligible for CID=0x1926 (Fire Darts, pw=43061293) + CID=0x1775 (Return Zombie, pw=28205952). '
    'Reached via card effect handler dispatch table at ROM 0x09e42ad8 + 0x09e45e38. '
    '2B alignment pad at 0x0806384e; fn entry at 0x08063850. '
    'Reads gP1LP[player_id * PLAYER_BLOCK_STRIDE + 0xc] (zone placement state field). '
    'Returns 1 if field_0xc == 0 (zone placement inactive), 0 if nonzero. '
    'player_id extracted from slot byte[+2] bit0. '
    'Lit pool @ 0x08063870: gP1LifePoints(0x0201c4e0) / PLAYER_BLOCK_STRIDE(0x868).'
)

# ---------------------------------------------------------------------------
# BLOCK2: 0x08063cf0..0x08063d03 (0x14 B)
#   fn entry @ 0x08063cf0
# ---------------------------------------------------------------------------
BLOCK2_LO  = 0x08063cf0
BLOCK2_HI  = 0x08063d03
BLOCK2_FN  = (0x08063cf0, 'check_chain_field8_is_zero')
BLOCK2_POOL = [
    (0x08063cfc, 'chain_state_ptr_08063cfc', 'gEquipChainSlotRefs', 0x0201bb90),
]
BLOCK2_PLATE = (
    'fn_eligible for CID=0x1954 (VWXYZ-Dragon Catapult Cannon, pw=84243274). '
    'Reached via card effect handler dispatch table at ROM 0x09e45328. '
    'Reads [gEquipChainSlotRefs+0x8] (chain interrupt field). '
    'Returns 1 if [gEquipChainSlotRefs+8] == 0 (no chain interrupt active), 0 if nonzero. '
    'Lit pool @ 0x08063cfc: gEquipChainSlotRefs(0x0201bb90).'
)

# ---------------------------------------------------------------------------
# BLOCK3: 0x08063db4..0x08063df3 (0x40 B)
#   fn entry @ 0x08063db4
# ---------------------------------------------------------------------------
BLOCK3_LO  = 0x08063db4
BLOCK3_HI  = 0x08063df3
BLOCK3_FN  = (0x08063db4, 'check_slot_zone_code_and_link_field_for_cid_195e')
BLOCK3_POOL_RAW = [
    # raw literal (no equate), label + EOL only
    (0x08063dec, 'field_mask_08063dec',
     'slot[+0x14] bit-match mask 0x00fa8000 for Chthonian Blast fn_eligible check'),
]
BLOCK3_PLATE = (
    'fn_eligible for CID=0x195e (Chthonian Blast, pw=18271561). '
    'Reached via card effect handler dispatch table at ROM 0x09e42cd0. '
    'Checks: (1) zone type bits[11:6] of slot[+2] must be 0x16 or 0x1b. '
    '(2) bit9 of slot[+0x14] must match slot.player_id (bit0 of slot[+2]). '
    '(3) lsrs r0,r2,#18 + lsrs r0,r0,#28: result always 0 for 32-bit r2 (r2>>46); '
    '    bgt(0>4)=false -> falls through. '
    '(4) ands r2,r0 [0x4002=ANDS Rd=r2,Rs=r0]: slot[+0x14] & 0x00fa8000. '
    '(5) movs r0,#0xe5; lsls r0,r0,#15 -> r0=0x00728000 (0xe5<<15). '
    '(6) cmp r2,r0: (slot[+0x14] & 0x00fa8000) must == 0x00728000. '
    'Lit pool @ 0x08063dec: 0x00fa8000 (bit-match mask).'
)

# ---------------------------------------------------------------------------
# BLOCK4: 0x08063fc4..0x08063fe7 (0x24 B)
#   fn entry @ 0x08063fc4
# ---------------------------------------------------------------------------
BLOCK4_LO  = 0x08063fc4
BLOCK4_HI  = 0x08063fe7
BLOCK4_FN  = (0x08063fc4, 'check_either_player_lp_slot_active')
BLOCK4_POOL = [
    (0x08063fdc, 'gp1lp_ptr_08063fdc',      'gP1LifePoints',       0x0201c4e0),
]
# 0x08063fe0 = 0x00000878 = PLAYER_BLOCK_STRIDE(0x868) + LP_SLOT_ACTIVE_OFF(0x10)
# This is a compound literal; label with EOL explanation, no equate (compound value)
BLOCK4_RAW_POOL = [
    (0x08063fe0, 'p1_lp_zone_off_08063fe0',
     'PLAYER_BLOCK_STRIDE(0x868) + LP_SLOT_ACTIVE_OFF(0x10) = player1 LP zone active offset 0x878'),
]
BLOCK4_PLATE = (
    'fn_eligible for CID=0x1976 (Simultaneous Loss, pw=92219931). '
    'Reached via card effect handler dispatch table at ROM 0x09e42da8. '
    'slot_ptr (r0 on entry) is NOT used -- pure global read. '
    'Checks gP1LP[+0x10] (player0 LP_SLOT_ACTIVE_OFF) OR gP1LP[+0x878] (player1 LP_SLOT_ACTIVE_OFF). '
    '0x878 = PLAYER_BLOCK_STRIDE(0x868) + LP_SLOT_ACTIVE_OFF(0x10). '
    'Both bne branch targets land at 0x08063fe4 (movs r0,#1; bx lr). '
    '0x08063fe2 is alignment pad (0x0000), NOT a branch target, not executed. '
    'Returns 1 if either player LP_SLOT_ACTIVE field is nonzero, 0 if both zero. '
    'Lit pool @ 0x08063fdc: gP1LifePoints(0x0201c4e0). '
    'Lit pool @ 0x08063fe0: 0x00000878 (player1 stride+LP_SLOT_ACTIVE_OFF).'
)


def main():
    print("=== DisassembleF07Seg10Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] Would process 4 blocks, 4 functions:")
        print("  Block1 0x%08x..0x%08x fn@0x%08x (2B pad at 0x0806384e)" % (
            BLOCK1_LO, BLOCK1_HI, BLOCK1_FN[0]))
        print("  Block2 0x%08x..0x%08x fn@0x%08x" % (BLOCK2_LO, BLOCK2_HI, BLOCK2_FN[0]))
        print("  Block3 0x%08x..0x%08x fn@0x%08x" % (BLOCK3_LO, BLOCK3_HI, BLOCK3_FN[0]))
        print("  Block4 0x%08x..0x%08x fn@0x%08x" % (BLOCK4_LO, BLOCK4_HI, BLOCK4_FN[0]))
        print("[dry] Literal pool slots: 7 total (4 EQ + 3 raw label)")
        return

    # =========================================================================
    # Block1: 0x0806384e..0x08063877 (1 fn, 2B pad at 0x0806384e)
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (1 fn; 2B pad) ---" % (BLOCK1_LO, BLOCK1_HI))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    # fn entry at 0x08063850 (2B pad at 0x0806384e skipped by disasm flow)
    _disasm_flow(BLOCK1_FN[0])
    # Literal pool slots
    for sp, ln, cn, val in BLOCK1_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK1_FN[0], BLOCK1_FN[1])
    _set_plate(BLOCK1_FN[0], BLOCK1_PLATE)

    # =========================================================================
    # Block2: 0x08063cf0..0x08063d03 (1 fn, no leading pad)
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (1 fn) ---" % (BLOCK2_LO, BLOCK2_HI))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    _disasm_flow(BLOCK2_FN[0])
    for sp, ln, cn, val in BLOCK2_POOL:
        _create_dword_eq(sp, ln, cn, val)
    _create_function(BLOCK2_FN[0], BLOCK2_FN[1])
    _set_plate(BLOCK2_FN[0], BLOCK2_PLATE)

    # =========================================================================
    # Block3: 0x08063db4..0x08063df3 (1 fn, no leading pad)
    # =========================================================================
    print("\n--- Block3: 0x%08x..0x%08x (1 fn) ---" % (BLOCK3_LO, BLOCK3_HI))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)
    _disasm_flow(BLOCK3_FN[0])
    # Raw literal pool (no equate, plain label + EOL)
    for sp, ln, eol in BLOCK3_POOL_RAW:
        _create_dword_raw(sp, ln, eol)
    _create_function(BLOCK3_FN[0], BLOCK3_FN[1])
    _set_plate(BLOCK3_FN[0], BLOCK3_PLATE)

    # =========================================================================
    # Block4: 0x08063fc4..0x08063fe7 (1 fn, no leading pad)
    # =========================================================================
    print("\n--- Block4: 0x%08x..0x%08x (1 fn) ---" % (BLOCK4_LO, BLOCK4_HI))
    _clear_and_set_thumb(BLOCK4_LO, BLOCK4_HI)
    _disasm_flow(BLOCK4_FN[0])
    # EQ pool slots
    for sp, ln, cn, val in BLOCK4_POOL:
        _create_dword_eq(sp, ln, cn, val)
    # Raw pool slots (compound literal)
    for sp, ln, eol in BLOCK4_RAW_POOL:
        _create_dword_raw(sp, ln, eol)
    _create_function(BLOCK4_FN[0], BLOCK4_FN[1])
    _set_plate(BLOCK4_FN[0], BLOCK4_PLATE)

    print("\n=== DisassembleF07Seg10Blocks DONE ===")
    print("  4 functions created across 4 blocks")
    print("  7 literal pool slots (4 EQ + 3 raw label)")
    print("  All blocks cleared + THUMB mode set before disassembly")


main()
