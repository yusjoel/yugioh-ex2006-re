# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2Disasm.py -- F09 Seg-2 disasm R4
#   Block: ROM_INCBIN 0x08070476 size 0x90
#   = fn_eligible_bazoo_the_soul_eater THUMB stub at 0x08070478
#     (FS table @GBA:0x09e46658, CID=0x1482 Bazoo the Soul-Eater)
#   + 2-byte pad at 0x08070506
#   + literal pool at 0x08070514/0x08070518:
#       .word PLAYER_BLOCK_STRIDE (0x00000868)
#       .word gDuelFieldSlots     (0x0201c510)
#
# Procedure:
#   1. clearListing 0x08070476..0x0807051b (whole block + literal pool range)
#   2. setTMode THUMB=1 for range
#   3. DisassembleCommand for fn_eligible_bazoo stub at 0x08070478 (single stub only)
#   4. createLabel 0x08070478 = fn_eligible_bazoo_the_soul_eater + EOL
#   5. createDWord at 0x08070514 (PLAYER_BLOCK_STRIDE literal pool)
#   6. createDWord at 0x08070518 (gDuelFieldSlots literal pool)
#   7. Label the literal pool words
#
# NOTE: All text is pure ASCII (no CJK).
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_205456-pre-F09Seg2

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
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
    print("=== RefineF09Seg2Disasm (DRY=%s) ===" % DRY)

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ctx     = currentProgram.getProgramContext()

    # Range: incbin block 0x08070476..0x08070505 (0x90 bytes)
    # + post-incbin literal pool ending at 0x0807051b (4 bytes coverage)
    RANGE_START = 0x08070476
    RANGE_END   = 0x0807051b  # inclusive

    # fn_eligible_bazoo stub entry (raw GBA addr; THUMB+1=0x08070479)
    STUB_ENTRY  = 0x08070478
    STUB_LABEL  = 'fn_eligible_bazoo_the_soul_eater'
    STUB_EOL    = 'fn_eligible stub for Bazoo the Soul-Eater CID=0x1482; FS table ref at GBA:0x09e46658'

    # Literal pool words after incbin block
    POOL_STRIDE = 0x08070514
    POOL_SLOTS  = 0x08070518

    a_lo = _addr(RANGE_START)
    a_hi = _addr(RANGE_END)
    stub_a = _addr(STUB_ENTRY)

    if DRY:
        print("[dry] Would clearListing 0x%08x..0x%08x" % (RANGE_START, RANGE_END))
        print("[dry] Would setTMode THUMB=1 for range")
        print("[dry] Would DisassembleCommand at 0x%08x (fn_eligible_bazoo)" % STUB_ENTRY)
        print("[dry] Would createLabel %s @ 0x%08x + EOL" % (STUB_LABEL, STUB_ENTRY))
        print("[dry] Would createDWord at 0x%08x (PLAYER_BLOCK_STRIDE)" % POOL_STRIDE)
        print("[dry] Would createDWord at 0x%08x (gDuelFieldSlots)" % POOL_SLOTS)
        print("=== RefineF09Seg2Disasm DRY DONE ===")
        return

    # Step 1: clearListing for the entire range
    print("[1] clearListing 0x%08x..0x%08x" % (RANGE_START, RANGE_END))
    try:
        clearListing(a_lo, a_hi)
        print("    clearListing done")
    except Exception as e:
        print("[WARN] clearListing error: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1 0x%08x..0x%08x" % (RANGE_START, RANGE_END))
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
        print("    TMode set THUMB=1")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand for stub at 0x08070478
    # Use restrict=False so Ghidra follows the flow through the whole stub body.
    # The range has already been cleared and TMode=THUMB set.
    print("[3] DisassembleCommand at 0x%08x (unrestricted flow-follow)" % STUB_ENTRY)
    cmd = DisassembleCommand(stub_a, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok at 0x%08x" % STUB_ENTRY)
    else:
        print("[WARN] disasm 0x%08x: %s" % (STUB_ENTRY, cmd.getStatusMsg()))

    # Step 4: label stub entry + EOL
    print("[4] createLabel %s @ 0x%08x" % (STUB_LABEL, STUB_ENTRY))
    existing = [s.getName() for s in sym_tbl.getSymbols(stub_a)]
    if STUB_LABEL not in existing:
        sym_tbl.createLabel(stub_a, STUB_LABEL, SourceType.USER_DEFINED)
        print("    label created")
    else:
        print("    label already present")

    cu = listing.getCodeUnitAt(stub_a)
    if cu is not None:
        cu.setComment(CodeUnit.EOL_COMMENT, STUB_EOL)
        print("    EOL set")
    else:
        print("[WARN] no CodeUnit at 0x%08x after disasm" % STUB_ENTRY)

    # Step 5: createDWord for PLAYER_BLOCK_STRIDE literal pool
    print("[5] createDWord at 0x%08x (PLAYER_BLOCK_STRIDE pool)" % POOL_STRIDE)
    pool_stride_a = _addr(POOL_STRIDE)
    try:
        clearListing(pool_stride_a, _addr(POOL_STRIDE + 3))
    except Exception as e:
        print("[WARN] clearListing pool_stride: %s" % e)
    d = listing.createData(pool_stride_a, DWordDataType.dataType)
    if d is not None:
        print("    DWord created @ 0x%08x" % POOL_STRIDE)
    else:
        print("[WARN] createData failed @ 0x%08x" % POOL_STRIDE)
    stride_label = 'player_stride_pool_0514'
    existing_s = [s.getName() for s in sym_tbl.getSymbols(pool_stride_a)]
    if stride_label not in existing_s:
        sym_tbl.createLabel(pool_stride_a, stride_label, SourceType.USER_DEFINED)
    cu2 = listing.getCodeUnitAt(pool_stride_a)
    if cu2 is not None:
        cu2.setComment(CodeUnit.EOL_COMMENT,
            'PLAYER_BLOCK_STRIDE=0x868; literal pool for invoke_equip_oam_setup_if_tile_count_match_and_neo_daedalus')
    print("    pool stride done")

    # Step 6: createDWord for gDuelFieldSlots literal pool
    print("[6] createDWord at 0x%08x (gDuelFieldSlots pool)" % POOL_SLOTS)
    pool_slots_a = _addr(POOL_SLOTS)
    try:
        clearListing(pool_slots_a, _addr(POOL_SLOTS + 3))
    except Exception as e:
        print("[WARN] clearListing pool_slots: %s" % e)
    d2 = listing.createData(pool_slots_a, DWordDataType.dataType)
    if d2 is not None:
        print("    DWord created @ 0x%08x" % POOL_SLOTS)
    else:
        print("[WARN] createData failed @ 0x%08x" % POOL_SLOTS)
    slots_label = 'gduel_slots_pool_0518'
    existing_s2 = [s.getName() for s in sym_tbl.getSymbols(pool_slots_a)]
    if slots_label not in existing_s2:
        sym_tbl.createLabel(pool_slots_a, slots_label, SourceType.USER_DEFINED)
    cu3 = listing.getCodeUnitAt(pool_slots_a)
    if cu3 is not None:
        cu3.setComment(CodeUnit.EOL_COMMENT,
            'gDuelFieldSlots=0x0201c510; literal pool for invoke_equip_oam_setup_if_tile_count_match_and_neo_daedalus')
    print("    pool slots done")

    print("\n=== RefineF09Seg2Disasm DONE ===")
    print("  stub fn_eligible_bazoo_the_soul_eater at 0x%08x" % STUB_ENTRY)
    print("  literal pool words at 0x%08x and 0x%08x" % (POOL_STRIDE, POOL_SLOTS))


main()
