# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF06Seg3Block.py -- F06 Seg-3 R4 disasm
#
#   Block: 0x08055188..0x080551bb (0x34 = 52 bytes)
#     ROM_INCBIN misidentified -- actually THUMB code (fn-ptr2 in card effect handler
#     dispatch tables at 0x09e4365c (CID 0x130f) and 0x09e43b84 (CID 0x14b4 Byser Shock)).
#     Function: check_zone_slot_occupied_with_clear_equip_flag
#     Checks: gDuelFieldSlots[player_id&1][slot_idx] bits[12:0] != 0 (occupied)
#             AND zone[+8] (equip valid flag) == 0 (equip chain head empty)
#     Returns 1 if both pass, 0 if fail.
#     Leaf function (bx lr, NOT pop{r1};bx r1).
#     Literal pool: 2 dwords at 0x080551b0 (PLAYER_BLOCK_STRIDE) / 0x080551b4 (gDuelFieldSlots)
#     These pool slots are covered by EQ in RefineF06Seg3Slots.py.
#
#   Pattern: DisassembleF06Seg2Block.py
#     - clearListing entire block range first (avoid ContextChangeException)
#     - setTMode=THUMB for entire range
#     - single DisassembleCommand (leaf fn, one entry point, flow continues naturally)
#     - createDWord for literal pool slots
#     - createFunction + setName (USER_DEFINED)
#     - setPlateComment (ASCII only)
#
#   Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_024140-pre-f06seg3

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
BLOCK_LO    = 0x08055188
BLOCK_HI    = 0x080551bb  # inclusive end (0x080551bc = next fn check_equip_slot_eligible_by_setcode_g_and_field5)
BLOCK_ENTRY = 0x08055188
# Literal pool (after b @ 0x080551ac and the zero pad 0x080551ae)
LIT_POOL_STRIDE = 0x080551b0  # PLAYER_BLOCK_STRIDE = 0x00000868
LIT_POOL_SLOTS  = 0x080551b4  # gDuelFieldSlots     = 0x0201c510

FUNC_ADDR = 0x08055188
FUNC_NAME = 'check_zone_slot_occupied_with_clear_equip_flag'
PLATE_TEXT = (
    'check_zone_slot_occupied_with_clear_equip_flag @ 0x08055188\n'
    'Equip target slot eligibility predicate: slot has card AND equip-valid flag is clear.\n'
    'Called as fn_ptr2 for CID 0x130f (unassigned) @ dispatch_table 0x09e43654\n'
    '  and CID 0x14b4 (Byser Shock) @ dispatch_table 0x09e43b7c.\n'
    'Checks in order: (1) gDuelFieldSlots[player_id&1][slot_idx] zone_word bits[12:0] != 0\n'
    '(occupied, alt is_present check via lsls #19); (2) zone[+8] (equip valid flag) == 0.\n'
    'Returns 1 if both pass (slot occupied + equip chain head empty).\n'
    'Leaf fn using bx lr (NOT pop{r1};bx r1). Inputs: r0=ignored, r1=player_id, r2=slot_idx.\n'
    'Constants: PLAYER_BLOCK_STRIDE=0x868, gDuelFieldSlots=0x0201c510.'
)


def main():
    print("=== DisassembleF06Seg3Block (DRY=%s) ===" % DRY)
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

    n_instr = _count_instructions(BLOCK_LO, LIT_POOL_STRIDE - 1)  # exclude literal pool region
    print("[ok ] disasm: %d instructions in code region" % n_instr)

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
    print("\n=== DisassembleF06Seg3Block DONE ===")
    print("  Instructions in block (incl pool region): %d" % n_total)
    print("  Function: %s" % FUNC_NAME)


main()
