# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF06Seg2Block.py -- F06 Seg-2 R4 disasm
#
#   Block: 0x08054614..0x0805465b (0x48 = 72 bytes)
#     ROM_INCBIN that was misidentified -- actually THUMB code (fn-ptr2 in Desert Sunlight
#     card effect handler dispatch table at 0x09e421d4; ROM[0x09e421d4]=0x08054615).
#     Function: check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight
#     Checks: same-side + zone[0..4] boundary + slot occupied + slot[+8]/[+6] predicates
#     Leaf function (no push lr), bx lr at 0x0805465a.
#     Literal pool: 2 dwords at 0x08054650/0x08054654 (covered by EQ in slot script).
#
#   Pattern: DisassembleF01Seg6Blocks.py
#     - clearListing entire block range first (avoid ContextChangeException)
#     - setTMode=THUMB for entire range
#     - single DisassembleCommand (leaf fn, one entry point, flow continues naturally)
#     - createDWord for literal pool slots (so Ghidra exports them as DWORD labels)
#     - createFunction + setName (USER_DEFINED)
#     - setPlateComment (ASCII only)
#
#   Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614-020741-pre-f06seg2

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
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


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_flow(addr):
    """Disassemble at addr, let flow continue naturally."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_dword(addr):
    """Create a DWORD data item at addr (for literal pool PC-relative ldr targets)."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.DWordDataType.dataType
    try:
        existing = listing.getDataAt(a)
        if existing is not None and existing.getDataType().equals(dt):
            print("[DW ] already DWORD @ 0x%08x" % addr)
            return True
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr)
        return True
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr, e))
        return False


def _count_instructions(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    listing = currentProgram.getListing()
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


# Block constants
BLOCK_LO    = 0x08054614
BLOCK_HI    = 0x0805465b  # inclusive end (0x0805465c = next fn check_equip_slot_type_and_score_match)
BLOCK_ENTRY = 0x08054614
# Literal pool (after bx lr at 0x0805465a)
LIT_POOL_STRIDE = 0x08054650  # PLAYER_BLOCK_STRIDE = 0x00000868
LIT_POOL_SLOTS  = 0x08054654  # gDuelFieldSlots     = 0x0201c510

FUNC_ADDR = 0x08054614
FUNC_NAME = 'check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight'
PLATE_TEXT = (
    'Desert Sunlight (CID 0x17B4) equip eligibility predicate #2; '
    'reached via card effect handler dispatch table 0x09e421d4 (fn-ptr2=0x08054615); '
    'checks same-side + zone[0..4] boundary + slot occupied + slot[+8]/[+6] predicates; '
    'no push lr -- leaf function'
)


def main():
    print("=== DisassembleF06Seg2Block (DRY=%s) ===" % DRY)
    print("  Block: 0x%08x..0x%08x (0x%x B)" % (BLOCK_LO, BLOCK_HI, BLOCK_HI - BLOCK_LO + 1))
    print("  Entry: 0x%08x" % BLOCK_ENTRY)
    print("  Name:  %s" % FUNC_NAME)

    if DRY:
        print("[dry] Step 1: clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK_LO, BLOCK_HI))
        print("[dry] Step 2: disasm_flow(0x%08x)" % BLOCK_ENTRY)
        print("[dry] Step 3: createDWord(0x%08x) = LIT_POOL_STRIDE" % LIT_POOL_STRIDE)
        print("[dry] Step 4: createDWord(0x%08x) = LIT_POOL_SLOTS" % LIT_POOL_SLOTS)
        print("[dry] Step 5: createFunction(0x%08x)" % FUNC_ADDR)
        print("[dry] Step 6: setName('%s', USER)" % FUNC_NAME)
        print("[dry] Step 7: setPlateComment (%d chars)" % len(PLATE_TEXT))
        return

    listing = currentProgram.getListing()

    # Step 1: clear and set THUMB mode
    _clear_and_set_thumb(BLOCK_LO, BLOCK_HI)

    # Step 2: disassemble from entry point
    if not _disasm_flow(BLOCK_ENTRY):
        print("[FAIL] disasm failed at 0x%08x -- aborting" % BLOCK_ENTRY)
        return

    n_instr = _count_instructions(BLOCK_LO, BLOCK_HI - 4)  # exclude literal pool region
    print("[ok ] disasm: %d instructions" % n_instr)

    # Step 3+4: ensure literal pool slots are DWORD (Ghidra may not parse them from disasm)
    _create_dword(LIT_POOL_STRIDE)
    _create_dword(LIT_POOL_SLOTS)

    # Step 5+6: create / name function
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(_addr(FUNC_ADDR))
    if fn is None:
        fn = createFunction(_addr(FUNC_ADDR), FUNC_NAME)
        if fn is None:
            print("[warn] createFunction failed at 0x%08x -- trying getFunctionContaining" % FUNC_ADDR)
            fn = fm.getFunctionContaining(_addr(FUNC_ADDR))
    if fn is not None:
        fn.setName(FUNC_NAME, SourceType.USER_DEFINED)
        print("[ok ] function named: %s @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
    else:
        print("[warn] could not obtain Function object at 0x%08x" % FUNC_ADDR)

    # Step 7: set plate comment (ASCII only)
    cu = listing.getCodeUnitAt(_addr(FUNC_ADDR))
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, PLATE_TEXT)
        print("[ok ] plate set (%d chars)" % len(PLATE_TEXT))
    else:
        print("[warn] no CodeUnit at 0x%08x for plate" % FUNC_ADDR)

    n_total = _count_instructions(BLOCK_LO, BLOCK_HI)
    print("\n=== DisassembleF06Seg2Block DONE ===")
    print("  Instructions in block: %d" % n_total)
    print("  Function: %s" % FUNC_NAME)


main()
