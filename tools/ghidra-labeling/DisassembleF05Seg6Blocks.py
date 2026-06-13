# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF05Seg6Blocks.py -- file-05 Seg-6 R4 disasm
#   Block 1: ROM_INCBIN 0x0804d294 sz 0x862 (13 THUMB case stubs)
#             dispatch_sprite_row_anim_by_state jump table targets
#   Block 2: ROM_INCBIN 0x0804dd58 sz 0x136a (12 THUMB case stubs)
#             dispatch_sprite_row_queue_by_state jump table targets
#
# Method (per Seg-5c pattern):
#   clearListing(whole_range) -> setTMode=THUMB -> per-entry-point DisassembleCommand
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


def disasm_block(block_start, block_end_incl, entry_points, label_prefix, listing):
    """
    Clear listing for [block_start..block_end_incl], set TMode=THUMB,
    then DisassembleCommand per entry point.
    entry_points: list of (addr_int, label_name)
    """
    lo = _addr(block_start)
    hi = _addr(block_end_incl)

    if DRY:
        print("[dry] block 0x%08x..0x%08x: clearListing + setTMode + %d per-stub disasms" % (
            block_start, block_end_incl, len(entry_points)))
        for ep, lbl in entry_points:
            print("  [dry] disasm 0x%08x label=%s" % (ep, lbl))
        return

    # 1) Clear listing for entire block
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (block_start, block_end_incl, str(e)))

    # 2) Set TMode=1 (THUMB) for entire block
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
    else:
        print("[warn] TMode register not found")

    # 3) Per entry-point DisassembleCommand
    ok_count = 0
    sm = currentProgram.getSymbolTable()
    for ep_int, ep_label in entry_points:
        ep_addr = _addr(ep_int)
        # Disassemble just this entry point (restrict to 1 instruction boundary)
        # Use AddressSet spanning the full block to allow fall-through
        cmd = DisassembleCommand(ep_addr, AddressSet(lo, hi), True)
        if cmd.applyTo(currentProgram):
            ok_count += 1
        else:
            print("[warn] disasm 0x%08x: %s" % (ep_int, cmd.getStatusMsg()))
        # Apply stub label
        try:
            sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
        except Exception as le:
            print("[warn] label 0x%08x %s: %s" % (ep_int, ep_label, str(le)))

    # Count instructions in block
    n_inst = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n_inst += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    print("[done] block 0x%08x: %d/%d stubs disasmed, %d instructions total" % (
        block_start, ok_count, len(entry_points), n_inst))


def main():
    listing = currentProgram.getListing()
    print("=== DisassembleF05Seg6Blocks (DRY=%s) ===" % DRY)

    # -------------------------------------------------------------------------
    # Block 1: dispatch_sprite_row_anim_by_state cases
    # ROM_INCBIN 0x0804d294, sz 0x862 -> end = 0x0804daf5
    # 13 unique THUMB entry points (0x0804daf6 = reset_sprite_row_queue_tail is OUTSIDE block)
    # -------------------------------------------------------------------------
    BLOCK1_START = 0x0804d294
    BLOCK1_END   = 0x0804daf5  # 0x4d294 + 0x862 - 1

    block1_entries = [
        (0x0804d294, 'dispatch_sprite_row_anim_case_0'),   # table[0]
        (0x0804d2f0, 'dispatch_sprite_row_anim_case_1'),   # table[1]
        (0x0804d458, 'dispatch_sprite_row_anim_case_2'),   # table[2]
        (0x0804d4bc, 'dispatch_sprite_row_anim_case_3'),   # table[3]
        (0x0804d548, 'dispatch_sprite_row_anim_case_4'),   # table[4]
        (0x0804d5a8, 'dispatch_sprite_row_anim_case_5'),   # table[5]
        (0x0804d634, 'dispatch_sprite_row_anim_case_6'),   # table[6]
        (0x0804d7ac, 'dispatch_sprite_row_anim_case_7'),   # table[7]
        (0x0804d7ee, 'dispatch_sprite_row_anim_case_8'),   # table[8]
        (0x0804d868, 'dispatch_sprite_row_anim_case_9'),   # table[9]
        (0x0804da52, 'dispatch_sprite_row_anim_case_10'),  # table[10]
        (0x0804da9a, 'dispatch_sprite_row_anim_case_11'),  # table[11]
        (0x0804dab4, 'dispatch_sprite_row_anim_case_12'),  # table[12]
    ]

    disasm_block(BLOCK1_START, BLOCK1_END, block1_entries,
                 'dispatch_sprite_row_anim_case_', listing)

    # -------------------------------------------------------------------------
    # Block 2: dispatch_sprite_row_queue_by_state cases
    # ROM_INCBIN 0x0804dd58, sz 0x136a -> end = 0x0804f0c1
    # 12 unique THUMB entry points (0x0804f0c2 = clear_sprite_row_queue_overflow_flag is OUTSIDE)
    # -------------------------------------------------------------------------
    BLOCK2_START = 0x0804dd58
    BLOCK2_END   = 0x0804f0c1  # 0x4dd58 + 0x136a - 1

    block2_entries = [
        (0x0804dd58, 'dispatch_sprite_row_queue_case_0'),   # table[0]
        (0x0804ddac, 'dispatch_sprite_row_queue_case_1'),   # table[1]
        (0x0804de00, 'dispatch_sprite_row_queue_case_2'),   # table[2]
        (0x0804de42, 'dispatch_sprite_row_queue_case_3'),   # table[3]
        (0x0804deb8, 'dispatch_sprite_row_queue_case_4'),   # table[4]
        (0x0804e900, 'dispatch_sprite_row_queue_case_5'),   # table[5]
        (0x0804e9d0, 'dispatch_sprite_row_queue_case_6'),   # table[6]
        (0x0804ea10, 'dispatch_sprite_row_queue_case_7'),   # table[7]
        (0x0804ee74, 'dispatch_sprite_row_queue_case_8'),   # table[8]
        (0x0804eee4, 'dispatch_sprite_row_queue_case_9'),   # table[9]
        (0x0804ef1a, 'dispatch_sprite_row_queue_case_10'),  # table[10]
        (0x0804f070, 'dispatch_sprite_row_queue_case_11'),  # table[11]
    ]

    disasm_block(BLOCK2_START, BLOCK2_END, block2_entries,
                 'dispatch_sprite_row_queue_case_', listing)

    print("=== DisassembleF05Seg6Blocks complete ===")


main()
