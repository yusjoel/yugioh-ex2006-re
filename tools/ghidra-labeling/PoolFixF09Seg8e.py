# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8e.py -- p5 file09 Seg-8 final pool fix pass E
#
# Remaining ROM_INCBIN blocks after pass D:
#   ROM_INCBIN 0x76616, 0x56 -- sub_6616 body before pool cluster at 0x666c
#   ROM_INCBIN 0x7673c, 0x16 -- code between pools 0x734 and 0x76780
#   ROM_INCBIN 0x76804, 0x80 -- sub_6804..sub_6818 bodies (stopped at end of sub_67f8)
#   ROM_INCBIN 0x768aa, 0x52 -- sub_68aa..sub_68cc bodies
#
# Root cause: DisassembleCommand stops after unconditional branch out of range.
# Fix: disassemble each sub-stub body separately with its own DisassembleCommand.
#
# Undefined labels to resolve:
#   LAB_08076640 -- in sub_65f0 body range 0x76616..0x7666b
#   LAB_08076744 -- in 0x7673c..0x76751 range (after pool 0x734)
#   LAB_08076748 -- in 0x7673c..0x76751 range
#   LAB_08076750 -- in 0x7673c..0x76751 range
#   LAB_080768fa -- in 0x768aa..0x768fb range (sub_68aa body)

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# Pools that may need re-forcing before code disasm in these ranges
POOL_DWORDS = [
    (0x0807666c, 0x0201c4e0),
    (0x08076670, 0x00000868),
    (0x08076674, 0x0201e2a8),
    (0x08076678, 0x08076511),
    (0x08076734, 0x00001685),
    (0x08076884, 0x0201c4e0),
    (0x08076888, 0x00000868),
    (0x0807688c, 0xfffffeec),
]

# Sub-stub pairs: (start, end_exclusive) to disassemble individually
# Each is a code-only range (no pool words inside)
SUB_STUBS = [
    # B2: sub_6616 body 0x76616..0x7666b (before pool cluster at 0x666c)
    # Note: sub_6616 code flow ends at unconditional branch before 0x666b
    # so range end can be 0x7666b
    (0x08076616, 0x0807666b, 'mustering_dark_scorpions_sub_6616_pre_pool'),
    # B2: code 0x7673c..0x76751 (between pool 0x734 and sub_6780)
    # This is the tail of sub_66d8 after the last pool
    (0x0807673c, 0x08076751, 'mustering_dark_scorpions_sub_66d8_tail'),
    # B4: sub_6804 body: 0x76804..0x76817 (before sub_6818)
    (0x08076804, 0x08076817, 'spell_vanishing_sub_6804_body'),
    # B4: sub_6818 body: 0x76818..0x7688f (before pool at 0x884)
    (0x08076818, 0x0807688f, 'spell_vanishing_sub_6818_body'),
    # B4: sub_68aa body: 0x768aa..0x768fb
    (0x080768aa, 0x080768fb, 'spell_vanishing_sub_68aa_body'),
    # B4: sub_68b8 body: 0x768b8..0x768cb (before sub_68cc)
    (0x080768b8, 0x080768cb, 'spell_vanishing_sub_68b8_body'),
    # B4: sub_68cc body: 0x768cc..0x76907
    (0x080768cc, 0x08076907, 'spell_vanishing_sub_68cc_body'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(addr_int, expected_val):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        return actual == (expected_val & 0xFFFFFFFF)
    except Exception:
        return False

def _force_dword(addr_int, expected_val):
    if DRY:
        print("[dry] force_dword 0x%08x" % addr_int)
        return
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        pass
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword 0x%08x (0x%08x)" % (addr_int, expected_val & 0xFFFFFFFF))
    except Exception as e:
        print("[warn] force_dword 0x%08x: %s" % (addr_int, e))

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)

def _disasm(sa, hi, label):
    if DRY:
        print("[dry] disasm %s 0x%08x..0x%08x" % (label, sa, hi))
        return
    stub_lo = _addr(sa)
    stub_hi = _addr(hi)
    try:
        clearListing(stub_lo, stub_hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x: %s" % (sa, e))
    _set_tmode(sa, hi)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s 0x%08x..0x%08x" % (label, sa, hi))

def main():
    print("=== PoolFixF09Seg8e (DRY=%s) ===" % DRY)
    print("  %d pool re-forces + %d sub-stub disasms" % (len(POOL_DWORDS), len(SUB_STUBS)))

    print("\n--- Step 1: Re-force pool DWords ---")
    for (addr, val) in POOL_DWORDS:
        _force_dword(addr, val)

    print("\n--- Step 2: Disasm each sub-stub body ---")
    for (sa, hi, label) in SUB_STUBS:
        _disasm(sa, hi, label)

    print("\n=== PoolFixF09Seg8e DONE ===")

main()
