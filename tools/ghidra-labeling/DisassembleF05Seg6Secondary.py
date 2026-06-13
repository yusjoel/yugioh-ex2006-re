# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF05Seg6Secondary.py -- f05 Seg-6 secondary THUMB disasm
#
# After disassembling the two jump-table blocks (Block1/Block2), three additional
# ROM_INCBIN regions were found to contain helper functions called by the case stubs:
#
#   Region A: ROM_INCBIN 0x4cca2, 0xea  (0x0804cca2..0x0804cd8b)
#             3 entry points called from Block1 case stubs:
#               SUB_0804cca4, SUB_0804cd00, SUB_0804cd74
#             Also contains: ROM_INCBIN 0x4cdac, 0x2c sub-orphan (NOT called externally,
#             but this block's disasm may fall through into it -- keep as INCBIN)
#
#   Region B: ROM_INCBIN 0x4e7ec, 0xd2  (0x0804e7ec..0x0804e8bd)
#             2 entry points called from Block2 case stubs:
#               SUB_0804e7f0, SUB_0804e888
#
# Method: clearListing(range) -> setTMode=THUMB -> per-entry DisassembleCommand
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

    # 1) Clear listing for entire region
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing: %s" % str(e))

    # 2) Set TMode=1 (THUMB) for entire region
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
    else:
        print("[warn] TMode not found")

    # 3) Per entry-point DisassembleCommand
    sm = currentProgram.getSymbolTable()
    ok = 0
    for ep_int, ep_label in entry_points:
        ep_addr = _addr(ep_int)
        cmd = DisassembleCommand(ep_addr, AddressSet(lo, hi), True)
        if cmd.applyTo(currentProgram):
            ok += 1
        else:
            print("[warn] disasm 0x%08x: %s" % (ep_int, cmd.getStatusMsg()))
        try:
            sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
        except Exception as le:
            print("[warn] label 0x%08x %s: %s" % (ep_int, ep_label, str(le)))

    # Count instructions
    n_inst = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n_inst += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[done] region 0x%08x: %d/%d entries ok, %d inst total" % (
        region_start, ok, len(entry_points), n_inst))


def main():
    listing = currentProgram.getListing()
    ctx = currentProgram.getProgramContext()
    print("=== DisassembleF05Seg6Secondary (DRY=%s) ===" % DRY)

    # ------------------------------------------------------------------
    # Region A: 0x0804cca2..0x0804cd8b (incbin 0x4cca2, sz 0xea)
    # 3 THUMB functions called from dispatch_sprite_row_anim_by_state cases
    # Note: 0x0804cd8c onward is a structured .word table in Ghidra (not INCBIN)
    # ------------------------------------------------------------------
    REGION_A_START = 0x0804cca2
    REGION_A_END   = 0x0804cd8b  # 0x4cca2 + 0xea - 1

    region_a_entries = [
        (0x0804cca4, 'SUB_0804cca4'),
        (0x0804cd00, 'SUB_0804cd00'),
        (0x0804cd74, 'SUB_0804cd74'),
    ]

    disasm_region(REGION_A_START, REGION_A_END, region_a_entries, listing, ctx)

    # ------------------------------------------------------------------
    # Region B: 0x0804e7ec..0x0804e8bd (incbin 0x4e7ec, sz 0xd2)
    # 2 THUMB functions called from dispatch_sprite_row_queue_by_state cases
    # ------------------------------------------------------------------
    REGION_B_START = 0x0804e7ec
    REGION_B_END   = 0x0804e8bd  # 0x4e7ec + 0xd2 - 1

    region_b_entries = [
        (0x0804e7f0, 'SUB_0804e7f0'),
        (0x0804e888, 'SUB_0804e888'),
    ]

    disasm_region(REGION_B_START, REGION_B_END, region_b_entries, listing, ctx)

    print("=== DisassembleF05Seg6Secondary complete ===")


main()
