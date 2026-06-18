# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg5aPoolFix2.py -- Comprehensive fix for inline pool disruption in B4/B6
#
# After force_dword with 8B clear disrupted code following inline pool words,
# this script re-disassembles all code segments that follow inline pools.
#
# B4 machine_dup_sub_3690 layout:
#   0x08073690..0x0807369f: code (prefix)
#   0x080736a0: pool word 0x157a (4B) -- inline
#   0x080736a4: pool word 0x1978 (4B) -- inline
#   0x080736a8..0x080736ed: code continuation (LAB_080736a8)
#   -> Need DisassembleCommand @ 0x080736a8 (after pools)
#
# B6 cat_ill_omen dispatch stubs layout:
#   cat_ill_omen_sub_3968 @ 0x08073968..0x080739a9:
#     0x08073968..0x0807398f: code
#     0x08073990: pool 0x159d (4B) inline
#     0x08073994: pool 0x0201e2a0 (4B) inline
#     0x08073998: pool 0x131 (4B) inline
#     0x0807399a: 2B padding 0x0000
#     0x0807399c..0x080739a9: code continuation (LAB_0807399c..LAB_080739a6)
#     0x080739ac: pool 0x0201c4e0 (gP1LifePoints) -- after code
#   cat_ill_omen_sub_39b0 @ 0x080739b0..0x080739d3:
#     0x080739b0..0x080739d3: code
#     0x080739d4: pool 0x0201c4e0 (gP1LifePoints) -- inline
#   LAB_080739d8 (continuation of cat_ill_omen_sub_39b0) @ 0x080739d8..0x08073a2f:
#     0x080739d8..0x08073a2f: code continuation
#     0x08073a30: pool 0x8056 -- after code
#   -> Need DisassembleCommand @ 0x0807399c and @ 0x080739b0 and @ 0x080739d8 and @ 0x08073a34
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
    """Force a DWord at pool_addr, clearing ONLY 4 bytes to avoid disrupting adjacent code."""
    pa = _addr(pool_addr)
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
        print("[WARN] DWord insertion @ 0x%08x: %s" % (pool_addr, e))
    except Exception as e:
        print("[WARN] DWord error @ 0x%08x: %s" % (pool_addr, e))
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


def disasm_block(label, range_start, range_end, entry_list, tmode_ctx, ctx):
    """Clear+setTMode a range, then per-entry DisassembleCommand."""
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    a_lo = _addr(range_start)
    a_hi = _addr(range_end)
    print("[%s.1] clearListing 0x%08x..0x%08x" % (label, range_start, range_end))
    try:
        clearListing(a_lo, a_hi)
        print("       done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[%s.2] setTMode THUMB=1" % label)
    if tmode_ctx is not None:
        ctx.setValue(tmode_ctx, a_lo, a_hi, BigInteger.ONE)
        print("       TMode set")
    for entry_addr, entry_label in entry_list:
        print("[%s.3] DisassembleCommand @ 0x%08x (%s)" % (label, entry_addr, entry_label))
        cmd = DisassembleCommand(_addr(entry_addr), None, False)
        if cmd.applyTo(currentProgram):
            print("       disasm ok")
        else:
            print("[WARN] disasm: %s" % cmd.getStatusMsg())
        # Ensure label is set
        ea = _addr(entry_addr)
        existing = [s.getName() for s in sym_tbl.getSymbols(ea)]
        if entry_label and entry_label not in existing:
            try:
                sym_tbl.createLabel(ea, entry_label, SourceType.USER_DEFINED)
                print("       label created: %s" % entry_label)
            except Exception as e:
                print("[WARN] createLabel: %s" % e)


def main():
    print("=== RefineF09Seg5aPoolFix2 (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    if DRY:
        print("[dry] Would fix B4 machine_dup_sub_3690 code continuation @ LAB_080736a8")
        print("[dry] Would fix B6 cat_ill_omen_sub_3968 code continuation @ 0x0807399c")
        print("[dry] Would fix B6 cat_ill_omen_sub_39b0 @ 0x080739b0")
        print("[dry] Would fix B6 LAB_080739d8 code continuation @ 0x080739d8")
        print("[dry] Would fix B6 pool_b6_39ac @ 0x080739ac (4B)")
        print("[dry] Would fix B6 pool_b6_39d4 @ 0x080739d4 (4B)")
        print("[dry] Would fix B6 pool_b6_3a30 @ 0x08073a30 (4B)")
        return

    # =========================================================================
    # FIX-B4: machine_dup_sub_3690 code continuation @ LAB_080736a8
    # After inline pools at 0x080736a0/a4, code resumes at 0x080736a8
    # Range 0x080736a8..0x080736ed (0x46 bytes of code)
    # =========================================================================
    print("\n--- FIX-B4: LAB_080736a8 code continuation @ 0x080736a8..0x080736ed ---")
    a_lo = _addr(0x080736a8)
    a_hi = _addr(0x080736ed)
    print("[B4-FIX.1] clearListing 0x080736a8..0x080736ed")
    try:
        clearListing(a_lo, a_hi)
        print("           done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B4-FIX.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("           TMode set")
    print("[B4-FIX.3] DisassembleCommand @ 0x080736a8 (LAB_080736a8)")
    cmd = DisassembleCommand(_addr(0x080736a8), None, False)
    if cmd.applyTo(currentProgram):
        print("           disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())
    # The LAB_ labels should now be auto-created by Ghidra as flow targets

    # =========================================================================
    # FIX-B6-1: cat_ill_omen_sub_3968 code continuation @ 0x0807399c
    # After inline pools at 0x08073990/94/98 + 2B pad at 0x0807399a,
    # code resumes at 0x0807399c
    # Range 0x0807399c..0x080739a9 (then pool at 0x080739ac)
    # =========================================================================
    print("\n--- FIX-B6-1: cat_ill_omen_sub_3968 code continuation @ 0x0807399c ---")
    a_lo = _addr(0x0807399c)
    a_hi = _addr(0x080739ab)  # end before pool_b6_39ac at 0x080739ac
    print("[B6-FIX1.1] clearListing 0x0807399c..0x080739ab")
    try:
        clearListing(a_lo, a_hi)
        print("            done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B6-FIX1.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("            TMode set")
    print("[B6-FIX1.3] DisassembleCommand @ 0x0807399c")
    cmd = DisassembleCommand(_addr(0x0807399c), None, False)
    if cmd.applyTo(currentProgram):
        print("            disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())
    # pool_b6_39ac @ 0x080739ac = 0x0201c4e0 (gP1LifePoints)
    force_dword_4b(listing, sym_tbl, 0x080739ac, 'pool_b6_39ac',
                   'gP1LifePoints=0x0201c4e0; literal pool cat_ill_omen_sub_3968 (B6)')

    # =========================================================================
    # FIX-B6-2: cat_ill_omen_sub_39b0 @ 0x080739b0..0x080739d3
    # This is a separate sub-stub but it was not disassembled properly
    # because its pool (0x080739d4) was force_dword'd with 8B clear
    # =========================================================================
    print("\n--- FIX-B6-2: cat_ill_omen_sub_39b0 @ 0x080739b0..0x080739d3 ---")
    a_lo = _addr(0x080739b0)
    a_hi = _addr(0x080739d3)
    print("[B6-FIX2.1] clearListing 0x080739b0..0x080739d3")
    try:
        clearListing(a_lo, a_hi)
        print("            done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B6-FIX2.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("            TMode set")
    print("[B6-FIX2.3] DisassembleCommand @ 0x080739b0 (cat_ill_omen_sub_39b0)")
    cmd = DisassembleCommand(_addr(0x080739b0), None, False)
    if cmd.applyTo(currentProgram):
        print("            disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())
    # Ensure label
    ea = _addr(0x080739b0)
    existing = [s.getName() for s in sym_tbl.getSymbols(ea)]
    if 'cat_ill_omen_sub_39b0' not in existing:
        try:
            sym_tbl.createLabel(ea, 'cat_ill_omen_sub_39b0', SourceType.USER_DEFINED)
            print("            label created: cat_ill_omen_sub_39b0")
        except Exception as e:
            print("[WARN] createLabel: %s" % e)
    # pool_b6_39d4 @ 0x080739d4 (4B only)
    force_dword_4b(listing, sym_tbl, 0x080739d4, 'pool_b6_39d4',
                   'gP1LifePoints=0x0201c4e0; literal pool cat_ill_omen_sub_39b0 (B6)')

    # =========================================================================
    # FIX-B6-3: LAB_080739d8 code continuation @ 0x080739d8..0x08073a2f
    # This is the code that follows the inline pool at 0x080739d4
    # It branches to LAB_08073a56 (in cat_ill_omen_default_3a54/3a56 area)
    # =========================================================================
    print("\n--- FIX-B6-3: LAB_080739d8 code @ 0x080739d8..0x08073a2f ---")
    a_lo = _addr(0x080739d8)
    a_hi = _addr(0x08073a2f)
    print("[B6-FIX3.1] clearListing 0x080739d8..0x08073a2f")
    try:
        clearListing(a_lo, a_hi)
        print("            done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B6-FIX3.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("            TMode set")
    print("[B6-FIX3.3] DisassembleCommand @ 0x080739d8 (LAB_080739d8)")
    cmd = DisassembleCommand(_addr(0x080739d8), None, False)
    if cmd.applyTo(currentProgram):
        print("            disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())
    # pool_b6_3a30 @ 0x08073a30 (4B only -- after the code block)
    force_dword_4b(listing, sym_tbl, 0x08073a30, 'pool_b6_3a30',
                   'OAM_EFFECT_SLOT_TILE_P1=0x8056; literal pool B6 sub_39b0 tail')

    # =========================================================================
    # FIX-B6-4: cat_ill_omen_sub_3a34 and later stubs may also need re-disasm
    # if force_dword on pool_b6_3a30 disrupted them. Check if they need fixing.
    # =========================================================================
    print("\n--- FIX-B6-4: cat_ill_omen_sub_3a34 @ 0x08073a34 ---")
    a_lo = _addr(0x08073a34)
    a_hi = _addr(0x08073a53)
    print("[B6-FIX4.1] clearListing 0x08073a34..0x08073a53")
    try:
        clearListing(a_lo, a_hi)
        print("            done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)
    print("[B6-FIX4.2] setTMode THUMB=1")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("            TMode set")
    print("[B6-FIX4.3] DisassembleCommand @ 0x08073a34 (cat_ill_omen_sub_3a34)")
    cmd = DisassembleCommand(_addr(0x08073a34), None, False)
    if cmd.applyTo(currentProgram):
        print("            disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())
    ea = _addr(0x08073a34)
    existing = [s.getName() for s in sym_tbl.getSymbols(ea)]
    if 'cat_ill_omen_sub_3a34' not in existing:
        try:
            sym_tbl.createLabel(ea, 'cat_ill_omen_sub_3a34', SourceType.USER_DEFINED)
            print("            label created: cat_ill_omen_sub_3a34")
        except Exception as e:
            print("[WARN] createLabel: %s" % e)

    print("[B6-FIX4.4] DisassembleCommand @ 0x08073a46 (cat_ill_omen_sub_3a46)")
    cmd = DisassembleCommand(_addr(0x08073a46), None, False)
    if cmd.applyTo(currentProgram):
        print("            disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    print("[B6-FIX4.5] DisassembleCommand @ 0x08073a54 (cat_ill_omen_default_3a54)")
    cmd = DisassembleCommand(_addr(0x08073a54), None, False)
    if cmd.applyTo(currentProgram):
        print("            disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    print("\n=== RefineF09Seg5aPoolFix2 DONE ===")
    print("  B4: LAB_080736a8 code continuation disassembled -> LAB_080736d2/LAB_080736ea defined")
    print("  B6: sub_3968 code continuation @ 0x0807399c disassembled")
    print("  B6: sub_39b0 @ 0x080739b0 disassembled")
    print("  B6: LAB_080739d8 code continuation disassembled")
    print("  B6: sub_3a34/3a46/default_3a54 re-disassembled")


main()
