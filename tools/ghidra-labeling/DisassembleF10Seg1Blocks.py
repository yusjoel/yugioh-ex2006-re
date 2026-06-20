# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg1Blocks.py -- f10 Seg-1 R4 disasm (8 ROM_INCBIN blocks)
#   BLK1 0x79fac/0x30: fn_eligible Abyssal Designator (THUMB+1 ref @0x9e42290)
#   BLK2 0x7a00c/0xe8: dispatch sub-stubs zone-type routing (7 entries)
#   BLK3 0x7a138/0x28: fn_eligible Big Wave Small Wave (THUMB+1 ref @0x9e422f0)
#   BLK4 0x7a178/0x14c: dispatch sub-stubs Red-Eyes LP routing (6 entries)
#   BLK5 0x7a3b8/0x38: fn_eligible shared CID 0x1803+0x15de (THUMB+1 @0x9e42398,0x9e442b8)
#   BLK6 0x7a464/0x11c: dispatch sub-stubs player-type equip sprite (6 entries)
#   BLK7 0x7a688/0x44: fn_eligible Magician's Circle (THUMB+1 @0x9e42410)
#   BLK8 0x7a71c/0xf8: dispatch sub-stubs zone-capacity routing (8 entries)
#
# Literal pool force-splits (createDWord):
#   BLK1: 0x79fd4 (gDuelPhaseFlags), 0x79fd8 (dispatch table ptr)
#   BLK5: 0x7a3e8 (gDuelPhaseFlags), 0x7a3ec (dispatch table ptr) -- NOT 0x7a3e4 (MOV PC,r0 code!)
#   BLK7: 0x7a6bc (gP1LifePoints), 0x7a6c0 (P1LP_BLOCK2_OFF_1CE8), 0x7a6c4 (gDuelPhaseFlags), 0x7a6c8 (EQUIP_PHASE_FRAME_OFF)
#
# NOTE: All EOL text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
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


def _clear_and_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)


def _disasm_stub(entry_int):
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def _create_dword(addr_int, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if eol:
        try:
            listing.setComment(a, CodeUnit.EOL_COMMENT, eol)
        except Exception as e:
            print("[warn] EOL 0x%08x: %s" % (addr_int, e))


def _set_eol(addr_int, text):
    listing = currentProgram.getListing()
    try:
        listing.setComment(_addr(addr_int), CodeUnit.EOL_COMMENT, text)
    except Exception as e:
        print("[warn] EOL 0x%08x: %s" % (addr_int, e))


def main():
    print("=== DisassembleF10Seg1Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] would disasm BLK1-8, createDWord pools; see script comments for details")
        return

    # ------------------------------------------------------------------
    # BLK1: 0x08079fac / 0x30 (48B) -- fn_eligible Abyssal Designator
    #   Single fn entry. Pool at +0x28/+0x2c (0x79fd4/0x79fd8).
    # ------------------------------------------------------------------
    print("--- BLK1: fn_eligible Abyssal Designator (0x79fac/0x30) ---")
    _clear_and_tmode(0x08079fac, 0x08079fdb)
    _disasm_stub(0x08079fac)
    # Force literal pool split
    _create_dword(0x08079fd4, 'gDuelPhaseFlags pool word: ldr r0,[pc,#24] from BLK1+0x0c')
    _create_dword(0x08079fd8, 'dispatch table ptr 0x08079fdc pool word: ldr from BLK1+0x10')
    _set_eol(0x08079fac, 'fn_eligible Abyssal Designator CID=ABYSSAL_DESIGNATOR_CID (0x17f4)')

    # ------------------------------------------------------------------
    # BLK2: 0x0807a00c / 0xe8 (232B) -- dispatch sub-stubs zone-type routing
    #   7 unique entry-points from dispatch table at 0x79fdc.
    # ------------------------------------------------------------------
    print("--- BLK2: dispatch sub-stubs zone-type (0x7a00c/0xe8) ---")
    _clear_and_tmode(0x0807a00c, 0x0807a0f3)
    for entry in [0x0807a00c, 0x0807a03a, 0x0807a0a8, 0x0807a0bc, 0x0807a0cc, 0x0807a0da, 0x0807a0ea]:
        _disasm_stub(entry)
    _set_eol(0x0807a00c, 'zone-type dispatch stub[0]: BLK2 base entry')
    _set_eol(0x0807a0ea, 'zone-type dispatch stub[default]: default-return stub (6 table slots)')

    # ------------------------------------------------------------------
    # BLK3: 0x0807a138 / 0x28 (40B) -- fn_eligible Big Wave Small Wave
    #   Single fn entry. Pool at +0x18..+0x1f (approx 0x7a150..0x7a15f).
    # ------------------------------------------------------------------
    print("--- BLK3: fn_eligible Big Wave Small Wave (0x7a138/0x28) ---")
    _clear_and_tmode(0x0807a138, 0x0807a15f)
    _disasm_stub(0x0807a138)
    _set_eol(0x0807a138, 'fn_eligible Big Wave Small Wave CID=BIG_WAVE_SMALL_WAVE_CID (0x17f9)')

    # ------------------------------------------------------------------
    # BLK4: 0x0807a178 / 0x14c (332B) -- dispatch sub-stubs Red-Eyes LP routing
    #   6 unique entry-points from dispatch table at 0x7a160.
    # ------------------------------------------------------------------
    print("--- BLK4: dispatch sub-stubs Red-Eyes LP (0x7a178/0x14c) ---")
    _clear_and_tmode(0x0807a178, 0x0807a2c3)
    for entry in [0x0807a178, 0x0807a1ae, 0x0807a21a, 0x0807a240, 0x0807a25e, 0x0807a278]:
        _disasm_stub(entry)
    _set_eol(0x0807a178, 'Red-Eyes LP dispatch stub[0]: BLK4 base entry')

    # ------------------------------------------------------------------
    # BLK5: 0x0807a3b8 / 0x38 (56B) -- fn_eligible shared CID 0x1803 + 0x15de
    #   Single fn entry. Pool at +0x30/+0x34 (0x7a3e8/0x7a3ec).
    #   IMPORTANT: 0x7a3e4 (+0x2c) = MOV PC,r0 code -- DO NOT createDWord there!
    # ------------------------------------------------------------------
    print("--- BLK5: fn_eligible shared CID 0x1803+0x15de (0x7a3b8/0x38) ---")
    _clear_and_tmode(0x0807a3b8, 0x0807a3ef)
    _disasm_stub(0x0807a3b8)
    # Pool is at +0x30 and +0x34 only (NOT +0x2c which is code)
    _create_dword(0x0807a3e8, 'gDuelPhaseFlags pool word: ldr r0,[pc,#28] from BLK5+0x12')
    _create_dword(0x0807a3ec, 'dispatch table ptr 0x0807a3f0 pool word: ldr r1,[pc,#12] from BLK5+0x26')
    _set_eol(0x0807a3b8, 'fn_eligible shared stub: CID 0x1803 (unassigned) + equip_cid_15de_08048a68 (0x15de)')

    # ------------------------------------------------------------------
    # BLK6: 0x0807a464 / 0x11c (284B) -- dispatch sub-stubs player-type equip sprite
    #   6 unique entry-points from dispatch table at 0x7a3f0 (29 entries).
    # ------------------------------------------------------------------
    print("--- BLK6: dispatch sub-stubs player-type (0x7a464/0x11c) ---")
    _clear_and_tmode(0x0807a464, 0x0807a57f)
    for entry in [0x0807a464, 0x0807a4ac, 0x0807a534, 0x0807a544, 0x0807a560, 0x0807a570]:
        _disasm_stub(entry)
    _set_eol(0x0807a464, 'player-type dispatch stub[0]: BLK6 base entry')
    _set_eol(0x0807a570, 'player-type dispatch stub[default]: default-return stub (24 table slots)')

    # ------------------------------------------------------------------
    # BLK7: 0x0807a688 / 0x44 (68B) -- fn_eligible Magician's Circle
    #   Single fn entry. Pool at +0x34..+0x43 (0x7a6bc/0x7a6c0/0x7a6c4/0x7a6c8).
    # ------------------------------------------------------------------
    print("--- BLK7: fn_eligible Magician's Circle (0x7a688/0x44) ---")
    _clear_and_tmode(0x0807a688, 0x0807a6cb)
    _disasm_stub(0x0807a688)
    _create_dword(0x0807a6bc, 'gP1LifePoints pool word')
    _create_dword(0x0807a6c0, 'P1LP_BLOCK2_OFF_1CE8 (0x1ce8) pool word -- REUSE ewram.inc line 275')
    _create_dword(0x0807a6c4, 'gDuelPhaseFlags pool word')
    _create_dword(0x0807a6c8, 'EQUIP_PHASE_FRAME_OFF (0x4a4) pool word')
    _set_eol(0x0807a688, "fn_eligible Magicians Circle CID=MAGICIANS_CIRCLE_CID (0x1818); dispatch table at 0x0807a6d0")
    # P1LP_BLOCK2_OFF_1CE8 equate reference
    try:
        et = currentProgram.getEquateTable()
        eq = et.getEquate('P1LP_BLOCK2_OFF_1CE8')
        if eq is None:
            eq = et.createEquate('P1LP_BLOCK2_OFF_1CE8', 0x1ce8)
        eq.addReference(_addr(0x0807a6c0), 0)
        print("[BLK7 pool] P1LP_BLOCK2_OFF_1CE8 equate ref added at 0x7a6c0")
    except Exception as e:
        print("[warn] BLK7 P1LP_BLOCK2_OFF_1CE8 equate: %s" % e)

    # ------------------------------------------------------------------
    # BLK8: 0x0807a71c / 0xf8 (248B) -- dispatch sub-stubs zone-capacity routing
    #   8 unique entry-points from dispatch table PTR_DAT_0807a6d0 (19 entries).
    # ------------------------------------------------------------------
    print("--- BLK8: dispatch sub-stubs zone-capacity (0x7a71c/0xf8) ---")
    _clear_and_tmode(0x0807a71c, 0x0807a813)
    for entry in [0x0807a71c, 0x0807a730, 0x0807a764, 0x0807a77c, 0x0807a786, 0x0807a7a8, 0x0807a7ec, 0x0807a804]:
        _disasm_stub(entry)
    _set_eol(0x0807a71c, 'zone-capacity dispatch stub[0]: BLK8 base entry')
    _set_eol(0x0807a804, 'zone-capacity dispatch stub[default]: default-return stub (12 table slots)')

    print("=== DisassembleF10Seg1Blocks Done ===")


main()
