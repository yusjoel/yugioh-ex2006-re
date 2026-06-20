# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg1RCluster1.py -- F09 Seg-1 REMEDIATION Cluster-1
#   Remediates partial-disasm residue from commit 08b3db1 in [0x0806f008..0x0806f1c4).
#   5 ROM_INCBIN blocks + 2 companion .byte blocks -> full THUMB disasm.
#
#   Execution order (B2d first: creates shared epilogue labels LAB_f1b6/LAB_f1b8):
#     B2d: equip_disp_sub_f188 body + shared epilogue @ 0x6f18a..0x6f1c3 (ROM_INCBIN 0x6f18a/0x3a)
#     B2c: equip_disp_sub_f0cc body + b+pad @ 0x6f0ce..0x6f183 (ROM_INCBIN 0x6f0ce/0xb2)
#     B2b: equip_disp_sub_f0ac body + b+pad @ 0x6f0ae..0x6f0c3 (ROM_INCBIN 0x6f0ae/0x12)
#     B2a: equip_disp_sub_f078 body + b+pad @ 0x6f07a..0x6f09f (ROM_INCBIN 0x6f07a/0x22)
#     B1:  eligible_creature_swap_f008 body @ 0x6f00a..0x6f031 (ROM_INCBIN 0x6f00a/0x32)
#          + createDWord @ 0x6f034 (gDuelPhaseFlags) + 0x6f038 (equip_disp_table_f03c)
#          + REF labels gduel_phase_f034 / equip_disp_tbl_f038
#     B2e: eligible_sub_stubs_f054 body @ 0x6f056..0x6f065 (.byte block)
#     B2f: equip_disp_sub_f066 body @ 0x6f068..0x6f077 (.byte block)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).
# NOTE: Pool DWORDs at 0x6f0a0/a4/a8, 0x6f0c4/c8, 0x6f184, 0x6f1c4 are OUTSIDE their
#       ROM_INCBIN ranges - already in asm as .word entries; no createDWord needed.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
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


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")

def _clear_listing(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))

def _disasm_at(stub_lo_int, stub_hi_int, label):
    lo = _addr(stub_lo_int)
    hi = _addr(stub_hi_int)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, stub_lo_int, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, stub_lo_int))

def _add_label(addr_int, label):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
    if label not in existing:
        sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
        print("[ok ] label 0x%08x -> %s" % (addr_int, label))
    else:
        print("[ok ] label 0x%08x -> %s (already exists)" % (addr_int, label))

def _force_dword(addr_int):
    """Force a DWORD data item at addr_int (clears listing first)."""
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

def _apply_ref(slot_addr_int, target_int, gas_label, slot_label):
    """Create USER_DEFINED label at target + DATA ref from slot + slot label."""
    sa = _addr(slot_addr_int)
    ta = _addr(target_int)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    # label at target
    tgt_names = [s.getName() for s in sym_tbl.getSymbols(ta)]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    # DATA ref slot -> target
    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    # slot label
    slot_names = [s.getName() for s in sym_tbl.getSymbols(sa)]
    if slot_label not in slot_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (slot_addr_int, target_int, gas_label, slot_label))

def _count_instrs(lo_int, hi_int):
    """Count instructions in range [lo_int..hi_int]."""
    listing = currentProgram.getListing()
    lo_a = _addr(lo_int)
    hi_a = _addr(hi_int)
    n = 0
    inst = listing.getInstructionAt(lo_a)
    while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg1RCluster1 (DRY=%s) ===" % DRY)
    print("  Remediates [0x0806f008..0x0806f1c4)")
    print("  5 ROM_INCBIN + 2 .byte blocks -> full THUMB disasm")
    print("  B2d-first ordering to create shared epilogue labels")

    if DRY:
        print("[dry] Step 1: B2d clearListing(0x0806f18a..0x0806f1c3) + setTMode + disasm")
        print("[dry] Step 2: B2c clearListing(0x0806f0ce..0x0806f183) + setTMode + disasm")
        print("[dry] Step 3: B2b clearListing(0x0806f0ae..0x0806f0c3) + setTMode + disasm")
        print("[dry] Step 4: B2a clearListing(0x0806f07a..0x0806f09f) + setTMode + disasm")
        print("[dry] Step 5: B1  clearListing(0x0806f00a..0x0806f031) + setTMode + disasm + 2xcreateDWord + 2xREF")
        print("[dry] Step 6: B2e clearListing(0x0806f056..0x0806f065) + setTMode + disasm")
        print("[dry] Step 7: B2f clearListing(0x0806f068..0x0806f077) + setTMode + disasm")
        return

    # -----------------------------------------------------------------------
    # Step 1: B2d -- equip_disp_sub_f188 body + shared epilogue
    #   ROM_INCBIN 0x6f18a/0x3a -> [0x0806f18a, 0x0806f1c3]
    #   29 instructions: lsls..bx r1 @ 0x6f1c2
    #   Shared epilogue @ 0x6f1b6..0x6f1c3 (movs r0,#0 / add sp / pop / bx r1)
    #   Pool at 0x6f1c4 is OUTSIDE range - do NOT include in clearListing
    # -----------------------------------------------------------------------
    print("\n--- Step 1: B2d equip_disp_sub_f188 body + shared epilogue ---")
    print("    ROM_INCBIN 0x6f18a/0x3a -> [0x0806f18a, 0x0806f1c3]")
    print("    Pool at 0x6f1c4 (.word 0x000004a4) is OUTSIDE range -- not cleared")
    _clear_listing(0x0806f18a, 0x0806f1c3)
    _set_tmode(0x0806f18a, 0x0806f1c3)
    # Disassemble full block: 29 instrs through bx r1 @ 0x6f1c2
    # Shared epilogue labels LAB_0806f1b6 + LAB_0806f1b8 auto-created as branch targets
    _disasm_at(0x0806f18a, 0x0806f1c3, 'equip_disp_sub_f188_body')
    n = _count_instrs(0x0806f18a, 0x0806f1c3)
    print("    [check] %d instructions in B2d" % n)

    # -----------------------------------------------------------------------
    # Step 2: B2c -- equip_disp_sub_f0cc body + b+pad
    #   ROM_INCBIN 0x6f0ce/0xb2 -> [0x0806f0ce, 0x0806f17f]
    #   b+pad at 0x6f180..0x6f183 (currently .word 0x0000e01a, byte-identical to b+.zero2)
    #   clearListing up to 0x6f183 to fix b+pad semantic
    #   Pool at 0x6f184 (.word 0x000004a4) is OUTSIDE range -- DO NOT CLEAR
    #   89 instructions + b + .zero 2; fail branches -> LAB_0806f1b6 (created by Step 1)
    # -----------------------------------------------------------------------
    print("\n--- Step 2: B2c equip_disp_sub_f0cc body ---")
    print("    ROM_INCBIN 0x6f0ce/0xb2 + b+pad @0x6f180..0x6f183")
    print("    Pool at 0x6f184 is OUTSIDE range -- not cleared")
    _clear_listing(0x0806f0ce, 0x0806f183)
    _set_tmode(0x0806f0ce, 0x0806f183)
    _disasm_at(0x0806f0ce, 0x0806f183, 'equip_disp_sub_f0cc_body')
    n = _count_instrs(0x0806f0ce, 0x0806f183)
    print("    [check] %d instructions in B2c" % n)

    # -----------------------------------------------------------------------
    # Step 3: B2b -- equip_disp_sub_f0ac body + b+pad
    #   ROM_INCBIN 0x6f0ae/0x12 -> [0x0806f0ae, 0x0806f0bf]
    #   b+pad at 0x6f0c0..0x6f0c3 (currently .word 0x0000e07a, byte-identical to b+.zero2)
    #   clearListing up to 0x6f0c3
    #   Pool at 0x6f0c4/0x6f0c8 is OUTSIDE range -- DO NOT CLEAR
    #   9 instructions + b + .zero 2
    # -----------------------------------------------------------------------
    print("\n--- Step 3: B2b equip_disp_sub_f0ac body ---")
    print("    ROM_INCBIN 0x6f0ae/0x12 + b+pad @0x6f0c0..0x6f0c3")
    print("    Pool at 0x6f0c4/0x6f0c8 is OUTSIDE range -- not cleared")
    _clear_listing(0x0806f0ae, 0x0806f0c3)
    _set_tmode(0x0806f0ae, 0x0806f0c3)
    _disasm_at(0x0806f0ae, 0x0806f0c3, 'equip_disp_sub_f0ac_body')
    n = _count_instrs(0x0806f0ae, 0x0806f0c3)
    print("    [check] %d instructions in B2b" % n)

    # -----------------------------------------------------------------------
    # Step 4: B2a -- equip_disp_sub_f078 body + b+pad
    #   ROM_INCBIN 0x6f07a/0x22 -> [0x0806f07a, 0x0806f09b]
    #   b+pad at 0x6f09c..0x6f09f (currently .word 0x0000e08c, byte-identical to b+.zero2)
    #   clearListing up to 0x6f09f
    #   Pool at 0x6f0a0/0x6f0a4/0x6f0a8 is OUTSIDE range -- DO NOT CLEAR
    #   17 instructions + b + .zero 2
    # -----------------------------------------------------------------------
    print("\n--- Step 4: B2a equip_disp_sub_f078 body ---")
    print("    ROM_INCBIN 0x6f07a/0x22 + b+pad @0x6f09c..0x6f09f")
    print("    Pool at 0x6f0a0/a4/a8 is OUTSIDE range -- not cleared")
    _clear_listing(0x0806f07a, 0x0806f09f)
    _set_tmode(0x0806f07a, 0x0806f09f)
    _disasm_at(0x0806f07a, 0x0806f09f, 'equip_disp_sub_f078_body')
    n = _count_instrs(0x0806f07a, 0x0806f09f)
    print("    [check] %d instructions in B2a" % n)

    # -----------------------------------------------------------------------
    # Step 5: B1 -- eligible_creature_swap_f008 body (after push @ 0x6f008)
    #   ROM_INCBIN 0x6f00a/0x32 -> [0x0806f00a, 0x0806f03b]
    #   clearListing only [0x6f00a..0x6f031] (code only, before pad+pool)
    #   The 2-byte pad @ 0x6f032..0x6f033 (0x0000) will be emitted as .byte 0x00 0x00 or .hword
    #   Pool at 0x6f034 (gDuelPhaseFlags=0x0201b290) and 0x6f038 (equip_disp_table_f03c=0x0806f03c)
    #   are INSIDE the ROM_INCBIN range -> need createDWord after disasm
    #
    #   DisassembleCommand from 0x6f00a stops at mov r15,r0 @ 0x6f030 (computed jump).
    #   Ghidra will NOT auto-decode 0x6f032..0x6f03b after computed branch.
    # -----------------------------------------------------------------------
    print("\n--- Step 5: B1 eligible_creature_swap_f008 body ---")
    print("    ROM_INCBIN 0x6f00a/0x32; code 0x6f00a..0x6f031; pad 0x6f032..0x6f033")
    print("    Pool INSIDE range: 0x6f034 (gDuelPhaseFlags) + 0x6f038 (equip_disp_table_f03c)")
    _clear_listing(0x0806f00a, 0x0806f031)
    _set_tmode(0x0806f00a, 0x0806f03b)
    # Disassemble code only up to 0x6f031 (stops at mov r15,r0 @ 0x6f030)
    _disasm_at(0x0806f00a, 0x0806f031, 'eligible_creature_swap_f008_body')
    n = _count_instrs(0x0806f00a, 0x0806f031)
    print("    [check] %d instructions in B1 code" % n)

    # Create DWORDs for pool entries inside ROM_INCBIN range
    print("    Creating DWORDs for pool @ 0x6f034 and 0x6f038")
    _force_dword(0x0806f034)
    _force_dword(0x0806f038)

    # Apply REF labels for the 2 pool DWORDs
    print("    Applying REF labels")
    # REF 1: slot 0x6f034 -> gDuelPhaseFlags @ 0x0201b290
    _apply_ref(0x0806f034, 0x0201b290, 'gDuelPhaseFlags', 'gduel_phase_f034')
    # REF 2: slot 0x6f038 -> equip_disp_table_f03c @ 0x0806f03c
    _apply_ref(0x0806f038, 0x0806f03c, 'equip_disp_table_f03c', 'equip_disp_tbl_f038')

    # -----------------------------------------------------------------------
    # Step 6: B2e -- eligible_sub_stubs_f054 body (.byte block)
    #   .byte 16B @ 0x6f056..0x6f065
    #   Entry at 0x6f054 (adds r0,r5,#0) already decoded in asm
    #   clearListing [0x6f056..0x6f065] to remove .byte
    #   8 instructions: adds,bl,cmp,bne,b,movs,b  (branches -> LAB_f1b6/LAB_f1b8)
    # -----------------------------------------------------------------------
    print("\n--- Step 6: B2e eligible_sub_stubs_f054 body ---")
    print("    .byte 0x10 @ 0x6f056..0x6f065")
    _clear_listing(0x0806f056, 0x0806f065)
    _set_tmode(0x0806f056, 0x0806f065)
    _disasm_at(0x0806f056, 0x0806f065, 'eligible_sub_stubs_f054_body')
    n = _count_instrs(0x0806f056, 0x0806f065)
    print("    [check] %d instructions in B2e" % n)

    # -----------------------------------------------------------------------
    # Step 7: B2f -- equip_disp_sub_f066 body (.byte block)
    #   .byte 16B @ 0x6f068..0x6f077
    #   Entry at 0x6f066 (ldrb r4,[r5,#2]) already decoded in asm
    #   clearListing [0x6f068..0x6f077] to remove .byte
    #   7 instructions: lsls,lsrs,ldrh,adds,bl,movs,b  (b -> LAB_f1b8)
    # -----------------------------------------------------------------------
    print("\n--- Step 7: B2f equip_disp_sub_f066 body ---")
    print("    .byte 0x10 @ 0x6f068..0x6f077")
    _clear_listing(0x0806f068, 0x0806f077)
    _set_tmode(0x0806f068, 0x0806f077)
    _disasm_at(0x0806f068, 0x0806f077, 'equip_disp_sub_f066_body')
    n = _count_instrs(0x0806f068, 0x0806f077)
    print("    [check] %d instructions in B2f" % n)

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n=== DisassembleF09Seg1RCluster1 DONE ===")
    total_b1  = _count_instrs(0x0806f00a, 0x0806f031)
    total_b2a = _count_instrs(0x0806f07a, 0x0806f09f)
    total_b2b = _count_instrs(0x0806f0ae, 0x0806f0c3)
    total_b2c = _count_instrs(0x0806f0ce, 0x0806f183)
    total_b2d = _count_instrs(0x0806f18a, 0x0806f1c3)
    total_b2e = _count_instrs(0x0806f056, 0x0806f065)
    total_b2f = _count_instrs(0x0806f068, 0x0806f077)
    print("  B1  (0x6f00a..0x6f031): %d instrs" % total_b1)
    print("  B2a (0x6f07a..0x6f09f): %d instrs" % total_b2a)
    print("  B2b (0x6f0ae..0x6f0c3): %d instrs" % total_b2b)
    print("  B2c (0x6f0ce..0x6f183): %d instrs" % total_b2c)
    print("  B2d (0x6f18a..0x6f1c3): %d instrs" % total_b2d)
    print("  B2e (0x6f056..0x6f065): %d instrs" % total_b2e)
    print("  B2f (0x6f068..0x6f077): %d instrs" % total_b2f)
    print("  EQ=0 REF=2 (gduel_phase_f034 + equip_disp_tbl_f038)")
    print("  7 blocks disassembled: 5 ROM_INCBIN + 2 .byte")


main()
