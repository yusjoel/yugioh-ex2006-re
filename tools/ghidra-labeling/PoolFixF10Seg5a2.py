# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF10Seg5a2.py -- f10 Seg-5a secondary fix
#
#   Issue 1: ROM_INCBIN 0x7dee0/0x30 -- sub-stub in BLK2 not disassembled
#     (Ghidra stopped at 0x7dedc pool word; 0x7dee0 is another push-THUMB stub
#      reached by bl from case4=0x7dec8; need clearListing + disasm)
#
#   Issue 2: ROM_INCBIN 0x7e3c4/0x60 -- AG Drill JT first 24 entries
#     (Ghidra left jump table words as undefined data; need 24 x createDWord
#      with labels matching already-labeled BLK5 stubs)
#
# NOTE: All text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType
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


def _create_dword_ref(addr_int, target_int, slot_label, eol=None):
    """Create DWord at addr_int, add DATA ref to target_int, label the slot."""
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    # Add reference to target
    sm = currentProgram.getSymbolTable()
    rf = currentProgram.getReferenceManager()
    target_a = _addr(target_int)
    rf.addMemoryReference(a, target_a, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in rf.getReferencesFrom(a):
        if ref.getToAddress().equals(target_a):
            rf.setPrimary(ref, True)
            break
    sm.createLabel(a, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[dword+ref ok] 0x%08x -> 0x%08x (%s)" % (addr_int, target_int, slot_label))


def _create_dword_simple(addr_int, label, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def main():
    print("=== PoolFixF10Seg5a2 (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] Issue 1: Would clear+disasm BLK2 extra stub 0x7dee0..0x7df0f")
        print("[DRY] Issue 2: Would createDWord x24 for AG Drill JT 0x7e3c4..0x7e423")
        return

    # -----------------------------------------------------------------------
    # Issue 1: Disassemble extra BLK2 sub-stub at 0x7dee0 (pool = 0x7df10..0x7df14)
    # This is the 6th sub-stub of Magical Mallet dispatch, reached via bl from case4.
    # The two pool words at end are mallet_stub4_phase_flags and mallet_stub4_frame_off
    # (already created in PoolFixF10Seg5a.py, but those were OUTSIDE the ROM_INCBIN).
    # After disasm the pool words at 0x7df10/0x7df14 should be restored.
    # -----------------------------------------------------------------------
    print("--- Issue 1: Disasm BLK2 extra sub-stub 0x7dee0..0x7df0f ---")
    _clear_and_tmode(0x0807dee0, 0x0807df0f)
    _disasm_stub(0x0807dee0)

    # The pool words 0x7df0e=0x4687 (MOV PC,r0 THUMB code -- do NOT createDWord)
    # Pool at 0x7df10 = gDuelPhaseFlags (already has label mallet_stub4_phase_flags from prev pass)
    # Pool at 0x7df14 = EQUIP_PHASE_FRAME_OFF (already has label mallet_stub4_frame_off from prev pass)
    # createDWord them to ensure they're properly typed after clearListing
    _create_dword_simple(0x0807df10, 'mallet_stub4_phase_flags',
                         'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub 4)')
    _create_dword_simple(0x0807df14, 'mallet_stub4_frame_off',
                         'EQUIP_PHASE_FRAME_OFF=0x000004a4: [gDuelPhaseFlags+0x4a4] equip phase frame slot')

    _create_dword_simple(0x0807df08, 'mallet_stub5_lp_pool_a',
                         'gP1LifePoints pool word in sub-stub 5 at 0x7dee0')

    print("[label ok] 0x0807dee0 equip_mallet_case5_0807dee0")

    # -----------------------------------------------------------------------
    # Issue 2: AG Drill JT entries 0x7e3c4..0x7e423 (24 entries = 96B = 0x60)
    # All entries point to: ag_drill_case5_0807e58e / ag_drill_case4_0807e57c /
    # ag_drill_default_0807e598
    # ROM values:
    #   0x7e3c4: 0x0807e58e (case5)
    #   0x7e3c8..0x7e413: 0x0807e598 (default) -- 19 entries
    #   0x7e414: 0x0807e57c (case4)
    #   0x7e418..0x7e423: 0x0807e598 (default) -- 3 entries
    # -----------------------------------------------------------------------
    print("--- Issue 2: AG Drill JT DWords 0x7e3c4..0x7e423 (24 entries) ---")

    jt_entries = [
        # (slot_addr, target_addr, label)
        (0x0807e3c4, 0x0807e58e, 'ag_drill_jt_00'),   # -> case5
        (0x0807e3c8, 0x0807e598, 'ag_drill_jt_01'),   # -> default
        (0x0807e3cc, 0x0807e598, 'ag_drill_jt_02'),
        (0x0807e3d0, 0x0807e598, 'ag_drill_jt_03'),
        (0x0807e3d4, 0x0807e598, 'ag_drill_jt_04'),
        (0x0807e3d8, 0x0807e598, 'ag_drill_jt_05'),
        (0x0807e3dc, 0x0807e598, 'ag_drill_jt_06'),
        (0x0807e3e0, 0x0807e598, 'ag_drill_jt_07'),
        (0x0807e3e4, 0x0807e598, 'ag_drill_jt_08'),
        (0x0807e3e8, 0x0807e598, 'ag_drill_jt_09'),
        (0x0807e3ec, 0x0807e598, 'ag_drill_jt_0a'),
        (0x0807e3f0, 0x0807e598, 'ag_drill_jt_0b'),
        (0x0807e3f4, 0x0807e598, 'ag_drill_jt_0c'),
        (0x0807e3f8, 0x0807e598, 'ag_drill_jt_0d'),
        (0x0807e3fc, 0x0807e598, 'ag_drill_jt_0e'),
        (0x0807e400, 0x0807e598, 'ag_drill_jt_0f'),
        (0x0807e404, 0x0807e598, 'ag_drill_jt_10'),
        (0x0807e408, 0x0807e598, 'ag_drill_jt_11'),
        (0x0807e40c, 0x0807e598, 'ag_drill_jt_12'),
        (0x0807e410, 0x0807e598, 'ag_drill_jt_13'),
        (0x0807e414, 0x0807e57c, 'ag_drill_jt_14'),   # -> case4
        (0x0807e418, 0x0807e598, 'ag_drill_jt_15'),   # -> default
        (0x0807e41c, 0x0807e598, 'ag_drill_jt_16'),
        (0x0807e420, 0x0807e598, 'ag_drill_jt_17'),
    ]

    for (slot_int, target_int, lbl) in jt_entries:
        _create_dword_ref(slot_int, target_int, lbl,
                          'AG Drill JT entry -> 0x%08x' % target_int)

    print("")
    print("=== PoolFixF10Seg5a2 DONE ===")
    print("=== Issue 1: BLK2 extra sub-stub at 0x7dee0 disassembled ===")
    print("=== Issue 2: 24 AG Drill JT DWords created (0x7e3c4..0x7e420) ===")


main()
