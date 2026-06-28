# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg1Block2Disasm.py -- file 12 Seg-1 Block2 R4 disasm
#
# Block2: ROM_INCBIN 0x080943e8 / 0x12 (0x080943e8..0x080943f9)
#   5 case blocks for dispatch_effect_ctx_slot_by_zone_type (zone_type - 0xb).
#   Dispatched via `mov pc, r0` (raw ptr, not THUMB+1).
#   Jump table at 0x080943d0 (5 .word entries):
#     [0]=0x80943e8, [1]=0x80943f4, [2]=0x80943ec, [3]=0x80943f0, [4]=0x80943f8
#   (Reviewer note: case order in jump table != sequential address order.)
#
# Case blocks at addresses (all set movs r6,#N; b LAB_080943fa, or fall-through):
#   0x080943e8: movs r6,#0x02; b 0x080943fa
#   0x080943ec: movs r6,#0x04; b 0x080943fa
#   0x080943f0: movs r6,#0x08; b 0x080943fa
#   0x080943f4: movs r6,#0x10; b 0x080943fa
#   0x080943f8: movs r6,#0x20             (fall-through to LAB_080943fa)
#
# Procedure:
#   1. clearListing 0x080943e8..0x080943f9
#   2. setTMode THUMB=1 for [0x080943e8, 0x080943f9]
#   3. DisassembleCommand per case block (5 individual calls)
#   4. createLabel for each case block entry
#   (No createFunction -- these are jump targets, not standalone functions)
#
# NOTE: All text is pure ASCII.
# Block1 (0x0809437c) and Block3 (0x08094c3e) are §5.1 only -- NOT touched here.

from ghidra.app.cmd.disassemble import DisassembleCommand
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


def main():
    print("=== RefineF12Seg1Block2Disasm (DRY=%s) ===" % DRY)

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()
    tmode   = ctx.getRegister("TMode")

    B2_RANGE_START = 0x080943e8
    B2_RANGE_END   = 0x080943f9  # inclusive (size 0x12 -> 0x080943e8 + 0x12 - 1 = 0x080943f9)

    # Case blocks: (addr, label, eol)
    B2_CASES = [
        (0x080943e8, 'zone_case_e8_bit1',
         'zone_type=0x0b dispatch: movs r6,#2 (bit1); b LAB_080943fa'),
        (0x080943ec, 'zone_case_ec_bit2',
         'zone_type=0x0c dispatch: movs r6,#4 (bit2); b LAB_080943fa'),
        (0x080943f0, 'zone_case_f0_bit3',
         'zone_type=0x0d dispatch: movs r6,#8 (bit3); b LAB_080943fa'),
        (0x080943f4, 'zone_case_f4_bit4',
         'zone_type=0x0e dispatch: movs r6,#0x10 (bit4); b LAB_080943fa'),
        (0x080943f8, 'zone_case_f8_bit5',
         'zone_type=0x0f dispatch: movs r6,#0x20 (bit5); fall-through to LAB_080943fa'),
    ]

    a_lo = _addr(B2_RANGE_START)
    a_hi = _addr(B2_RANGE_END)

    if DRY:
        print("[dry] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
        print("[dry] setTMode THUMB=1")
        for case_addr, case_label, case_eol in B2_CASES:
            print("[dry] DisassembleCommand @ 0x%08x  label=%s" % (case_addr, case_label))
        print("[dry] done -- 5 case blocks, no createFunction")
        return

    # Step 1: clearListing entire block
    print("[1] clearListing 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
    try:
        clearListing(a_lo, a_hi)
        print("    done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1 for 0x%08x..0x%08x" % (B2_RANGE_START, B2_RANGE_END))
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("    TMode set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand per case block
    print("[3] DisassembleCommand per case block (5 individual calls)")
    for case_addr, case_label, case_eol in B2_CASES:
        print("    [3.x] @ 0x%08x (%s)" % (case_addr, case_label))
        ca = _addr(case_addr)
        cmd = DisassembleCommand(ca, None, False)
        if cmd.applyTo(currentProgram):
            print("          disasm ok")
        else:
            print("          [WARN] disasm: %s" % cmd.getStatusMsg())

    # Step 4: createLabel + EOL for each case block
    print("[4] createLabel + EOL for each case block")
    for case_addr, case_label, case_eol in B2_CASES:
        ca = _addr(case_addr)
        existing = [s.getName() for s in sym_tbl.getSymbols(ca)]
        if case_label not in existing:
            sym_tbl.createLabel(ca, case_label, SourceType.USER_DEFINED)
            print("    [4.x] label created: %s @ 0x%08x" % (case_label, case_addr))
        else:
            print("    [4.x] label already present: %s" % case_label)

        if case_eol:
            cu = listing.getCodeUnitAt(ca)
            if cu is not None:
                cu.setComment(CodeUnit.EOL_COMMENT, case_eol)
                print("          EOL set")
            else:
                print("          [WARN] no CodeUnit at 0x%08x after disasm" % case_addr)

    print("\n=== RefineF12Seg1Block2Disasm DONE ===")
    print("  Block2: 5 case blocks 0x080943e8..0x080943f9 disassembled")
    print("  No createFunction (jump targets, not standalone functions)")


main()
