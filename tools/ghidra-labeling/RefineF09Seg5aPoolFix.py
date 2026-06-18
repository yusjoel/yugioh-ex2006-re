# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5aPoolFix.py -- Fix for disrupted stubs after RefineF09Seg5aSlots.py
#
# Problem: force_dword(pool_addr) clears 8 bytes, disrupting code immediately following
# the pool word when the pool is an INLINE literal pool (mid-stub, not at stub end).
#
# Affected:
#   B4 machine_dup_sub_3690: pool words at 0x080736a0 and 0x080736a4 are inline
#     (referenced via ldr r0,[pc,#3*4] at 0x08073690, ldr r0,[pc,#2*4] at 0x08073698)
#     The 8-byte clearListing for 0x080736a0 cleared code at 0x080736a4..0x080736a7
#     The 8-byte clearListing for 0x080736a4 also cleared code at 0x080736a8..0x080736ab
#   B6 cat_ill_omen_sub_3968: pool word at 0x08073998 is inline, followed immediately
#     by 2B padding (0x0000) and then ldr code at 0x0807399c
#     The 8-byte clearListing for 0x08073998 cleared code at 0x0807399c..0x0807399f
#
# Fix: Re-disasm disrupted stub ranges after minimal pool force (4 bytes only, not 8).
# Then re-run DisassembleCommand on each affected stub.
#
# After this fix, the LAB_ targets (LAB_080736d2, LAB_080736ea, LAB_080739a6) will be
# created by Ghidra during disasm as flow targets.
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
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


def force_dword_4b(listing, sym_tbl, pool_addr, pool_label, pool_eol=None):
    """Force a DWord at pool_addr, clearing ONLY 4 bytes (not 8) to avoid disrupting adjacent code."""
    pa = _addr(pool_addr)
    # Clear exactly 4 bytes (just the dword itself)
    try:
        clearListing(pa, _addr(pool_addr + 3))
    except Exception as e:
        print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
    try:
        d = listing.createData(pa, DWordDataType.dataType)
        if d is not None:
            print("[POOL-4B] DWord @ 0x%08x (%s)" % (pool_addr, pool_label))
        else:
            print("[WARN] createData DWord returned None @ 0x%08x" % pool_addr)
    except CodeUnitInsertionException as e:
        print("[WARN] createData DWord insertion error @ 0x%08x: %s" % (pool_addr, e))
    except Exception as e:
        print("[WARN] createData DWord error @ 0x%08x: %s" % (pool_addr, e))
    existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label not in existing_p:
        try:
            sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("[WARN] createLabel pool %s: %s" % (pool_label, e))
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)


def main():
    print("=== RefineF09Seg5aPoolFix (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    # =========================================================================
    # FIX-1: machine_dup_sub_3690 in B4 (0x08073690..0x080736ed)
    #   Inline pool words at 0x080736a0 (0x157a) and 0x080736a4 (0x1978)
    #   force_dword with 8B clear disrupted code at 0x080736a4..0x080736ab
    #   Re-do with 4B clear, then re-disasm entire sub_3690
    # =========================================================================
    print("\n--- FIX-1: machine_dup_sub_3690 @ 0x08073690 ---")
    FIX1_RANGE_START = 0x08073690
    FIX1_RANGE_END   = 0x080736ed  # inclusive (machine_dup_sub_3690 ends before 0x080736ee)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (FIX1_RANGE_START, FIX1_RANGE_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] force_dword_4b 0x080736a0 (0x157a)")
        print("[dry] force_dword_4b 0x080736a4 (0x1978)")
        print("[dry] DisassembleCommand @ 0x08073690")
    else:
        a_lo = _addr(FIX1_RANGE_START)
        a_hi = _addr(FIX1_RANGE_END)
        print("[FIX1.1] clearListing 0x%08x..0x%08x" % (FIX1_RANGE_START, FIX1_RANGE_END))
        try:
            clearListing(a_lo, a_hi)
            print("         done")
        except Exception as e:
            print("[WARN] clearListing: %s" % e)
        print("[FIX1.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("         TMode set")
        # Re-apply inline pool DWords (4B clear only)
        force_dword_4b(listing, sym_tbl, 0x080736a0, 'pool_b4_36a0',
                       '0x157a=MACHINE_DUPLICATION_CID; inline literal pool machine_dup_sub_3690')
        force_dword_4b(listing, sym_tbl, 0x080736a4, 'pool_b4_36a4',
                       '0x1978=LEAGUE_OF_UNIFORMITY_CID; inline literal pool machine_dup_sub_3690')
        print("[FIX1.3] DisassembleCommand @ 0x08073690")
        cmd = DisassembleCommand(_addr(0x08073690), None, False)
        if cmd.applyTo(currentProgram):
            print("         disasm ok")
        else:
            print("[WARN] disasm: %s" % cmd.getStatusMsg())

    # =========================================================================
    # FIX-2: cat_ill_omen_sub_3968 in B6 (0x08073968..0x080739af)
    #   Inline pool word at 0x08073998 (0x131) followed by 2B pad (0x0000) then code
    #   force_dword with 8B clear disrupted code at 0x0807399c..0x0807399f
    #   Re-do with 4B clear, then re-disasm sub_3968
    # =========================================================================
    print("\n--- FIX-2: cat_ill_omen_sub_3968 @ 0x08073968 ---")
    FIX2_RANGE_START = 0x08073968
    FIX2_RANGE_END   = 0x080739af  # inclusive (cat_ill_omen_sub_3968 ends before 0x080739b0)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (FIX2_RANGE_START, FIX2_RANGE_END))
        print("[dry] setTMode THUMB=1")
        print("[dry] force_dword_4b 0x08073990 (0x159d=NECROVALLEY_CID)")
        print("[dry] force_dword_4b 0x08073994 (0x0201e2a0=gDuelCardCtxBase)")
        print("[dry] force_dword_4b 0x08073998 (0x131)")
        print("[dry] DisassembleCommand @ 0x08073968")
    else:
        a_lo = _addr(FIX2_RANGE_START)
        a_hi = _addr(FIX2_RANGE_END)
        print("[FIX2.1] clearListing 0x%08x..0x%08x" % (FIX2_RANGE_START, FIX2_RANGE_END))
        try:
            clearListing(a_lo, a_hi)
            print("         done")
        except Exception as e:
            print("[WARN] clearListing: %s" % e)
        print("[FIX2.2] setTMode THUMB=1")
        if tmode is not None:
            ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
            print("         TMode set")
        # Re-apply pool DWords (4B clear only to not disrupt code at 0x0807399c)
        force_dword_4b(listing, sym_tbl, 0x08073990, 'pool_b6_3990',
                       'NECROVALLEY_CID=0x159d; inline literal pool cat_ill_omen_sub_3968')
        force_dword_4b(listing, sym_tbl, 0x08073994, 'pool_b6_3994',
                       'gDuelCardCtxBase=0x0201e2a0; inline literal pool cat_ill_omen_sub_3968')
        force_dword_4b(listing, sym_tbl, 0x08073998, 'pool_b6_3998',
                       '0x131=305; inline literal pool cat_ill_omen_sub_3968')
        print("[FIX2.3] DisassembleCommand @ 0x08073968")
        cmd = DisassembleCommand(_addr(0x08073968), None, False)
        if cmd.applyTo(currentProgram):
            print("         disasm ok")
        else:
            print("[WARN] disasm: %s" % cmd.getStatusMsg())

    print("\n=== RefineF09Seg5aPoolFix DONE ===")
    print("  FIX-1: machine_dup_sub_3690 with inline pools 0x36a0/0x36a4 re-disasmed")
    print("  FIX-2: cat_ill_omen_sub_3968 with inline pools 0x3990/0x3994/0x3998 re-disasmed")
    print("  LAB_ targets should now be defined: LAB_080736d2, LAB_080736ea, LAB_080739a6")


main()
