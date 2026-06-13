# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF05Seg6Tertiary.py -- f05 Seg-6 tertiary THUMB disasm
#
# After disassembling secondary regions, two more ROM_INCBIN blocks were found
# to contain branch/call targets:
#
#   Region C: ROM_INCBIN 0x4cdac, 0x2c  (0x0804cdac..0x0804cdd7)
#             Orphan jump table handlers called via orphan_slot_card_eligible_fn_table
#             Also target of 'bhi LAB_0804cdd2' from SUB_0804cd74
#             Entry points: 0x4cdac (3 unique handlers), 0x4cdb6, 0x4cdc2, 0x4cdd2
#
#   Region D: ROM_INCBIN 0x4f098, 0x2a  (0x0804f098..0x0804f0c1)
#             Contains SUB_0804f0b8, called by SUB_0804e7f0 (Region B)
#             Entry point: 0x4f098 (start of region) and 0x4f0b8
#
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def disasm_region(region_start, region_end_incl, entry_points, listing, ctx):
    lo = _addr(region_start)
    hi = _addr(region_end_incl)
    tmode = ctx.getRegister("TMode")

    if DRY:
        print("[dry] region 0x%08x..0x%08x: clearListing + setTMode + %d entries" % (
            region_start, region_end_incl, len(entry_points)))
        for ep, lbl in entry_points:
            print("  [dry] disasm 0x%08x label=%s" % (ep, lbl))
        return

    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing: %s" % str(e))

    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
    else:
        print("[warn] TMode not found")

    sm = currentProgram.getSymbolTable()
    ok = 0
    for ep_int, ep_label in entry_points:
        ep_addr = _addr(ep_int)
        cmd = DisassembleCommand(ep_addr, AddressSet(lo, hi), True)
        if cmd.applyTo(currentProgram):
            ok += 1
        else:
            print("[warn] disasm 0x%08x: %s" % (ep_int, cmd.getStatusMsg()))
        if ep_label:
            try:
                sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
            except Exception as le:
                print("[warn] label 0x%08x %s: %s" % (ep_int, ep_label, str(le)))

    n_inst = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n_inst += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[done] region 0x%08x: %d/%d entries ok, %d inst" % (
        region_start, ok, len(entry_points), n_inst))


def main():
    listing = currentProgram.getListing()
    ctx = currentProgram.getProgramContext()
    print("=== DisassembleF05Seg6Tertiary (DRY=%s) ===" % DRY)

    # ------------------------------------------------------------------
    # Region C: 0x0804cdac..0x0804cdd7 (ROM_INCBIN 0x4cdac, sz 0x2c)
    # Orphan dispatch handlers + branch target from SUB_0804cd74
    # Entry points: 3 handler entry points + bhi target at 0x4cdd2
    # ------------------------------------------------------------------
    REGION_C_START = 0x0804cdac
    REGION_C_END   = 0x0804cdd7

    region_c_entries = [
        (0x0804cdac, 'orphan_slot_card_eligible_handler_0'),
        (0x0804cdb6, 'orphan_slot_card_eligible_handler_1'),
        (0x0804cdc2, 'orphan_slot_card_eligible_handler_2'),
        (0x0804cdd2, 'LAB_0804cdd2'),
    ]

    disasm_region(REGION_C_START, REGION_C_END, region_c_entries, listing, ctx)

    # ------------------------------------------------------------------
    # Region D: 0x0804f098..0x0804f0c1 (ROM_INCBIN 0x4f098, sz 0x2a)
    # Contains SUB_0804f0b8, called by SUB_0804e7f0
    # Note: 0x0804f0c2 = clear_sprite_row_queue_overflow_flag is OUTSIDE
    # ------------------------------------------------------------------
    REGION_D_START = 0x0804f098
    REGION_D_END   = 0x0804f0c1

    region_d_entries = [
        (0x0804f098, 'SUB_0804f098'),
        (0x0804f0b8, 'SUB_0804f0b8'),
    ]

    disasm_region(REGION_D_START, REGION_D_END, region_d_entries, listing, ctx)

    print("=== DisassembleF05Seg6Tertiary complete ===")


main()
