# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF07Seg7Block.py -- F07 Seg-7 R4 disasm (1 block)
#   Block: 0x08061c66..0x08061c8f (0x2a B)
#     - 2B alignment pad: 0x08061c66 = 0x0000
#     - fn entry @ 0x08061c68: check_player_lp_status_nonzero_for_cid_1776
#       Dispatch table: 0x09e4204c, CID=0x1776 (Corpse of Yata-Garasu, pw=30461781)
#       fn_eligible ptr = 0x08061c69 at table[+0x0c]
#     - Literal pool @ 0x08061c84..0x08061c8b (2 dwords):
#         0x08061c84: gP1LifePoints = 0x0201c4e0
#         0x08061c88: PLAYER_BLOCK_STRIDE = 0x00000868
#     - return-2 arm: 0x08061c8c (movs r0,#2 / bx lr)
#     - return-0 arm: 0x08061c8e..0x08061c8f (already in code flow bx lr)
#
#   Function semantics:
#     Reads gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)].
#     If status word nonzero -> return 2; if zero -> return 0.
#
#   PC-relative pool verification (python-computed):
#     ldr r2,[pc,#24] @ 0x08061c68 -> pc=0x08061c6a -> +24=0x08061c82 -> word_aligned=0x08061c84 -> gP1LifePoints
#     ldr r1,[pc,#20] @ 0x08061c70 -> pc=0x08061c72 -> +20=0x08061c86 -> word_aligned=0x08061c88 -> PLAYER_BLOCK_STRIDE
#
#   backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614172914-pre-F07Seg7

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
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


def _create_function(addr, name):
    """Create a named function at addr."""
    a = _addr(addr)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()

    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing function at 0x%08x -> %s" % (addr, name))
        else:
            print("[FN ] function already exists at 0x%08x: %s" % (addr, name))
        return

    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
    """Set PLATE_COMMENT on the code unit at addr. text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x -- skipping" % addr)
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr))
    if cu is None:
        print("[PLATE FAIL] no CodeUnit at 0x%08x" % addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[PLATE ok] 0x%08x (%d chars)" % (addr, len(text)))


def _create_dword_with_ref(slot_addr, label_name, tgt_addr, tgt_label):
    """Force a DWORD at slot_addr, set label, add DATA ref to tgt_addr, set tgt_label."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    rm = currentProgram.getReferenceManager()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    sym_tbl.createLabel(a, label_name, SourceType.USER_DEFINED)
    # label the target
    createLabel(_addr(tgt_addr), tgt_label, True, SourceType.USER_DEFINED)
    # data ref slot -> target
    ref = rm.addMemoryReference(a, _addr(tgt_addr), RefType.DATA, SourceType.USER_DEFINED, 0)
    rm.setPrimary(ref, True)
    print("[DW+REF] 0x%08x -> %s (ref->%s @ 0x%08x)" % (slot_addr, label_name, tgt_label, tgt_addr))


def _create_dword_eq(slot_addr, label_name, const_name, value):
    """Force a DWORD at slot_addr, set label, add equate."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    et = currentProgram.getEquateTable()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    eq = et.getEquate(const_name)
    if eq is None:
        eq = et.createEquate(const_name, value)
    eq.addReference(a, 0)
    print("[DW+EQ] 0x%08x -> %s (%s=0x%x)" % (slot_addr, label_name, const_name, value))


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


# ---------------------------------------------------------------------------
# Block: 0x08061c66..0x08061c8f (0x2a B)
#   2B pad at 0x08061c66
#   fn entry @ 0x08061c68
#   Literal pool: 0x08061c84 (gP1LifePoints) + 0x08061c88 (PLAYER_BLOCK_STRIDE)
#   Return-2 arm: 0x08061c8c..0x08061c8f (in code flow)
# ---------------------------------------------------------------------------
BLOCK_LO   = 0x08061c66
BLOCK_HI   = 0x08061c8f
BLOCK_FN   = 0x08061c68
BLOCK_NAME = "check_player_lp_status_nonzero_for_cid_1776"

BLOCK_POOL_SLOTS = [
    # (slot_addr, label_name, target_addr_or_None, tgt_label_or_None, const_name_or_None, value_or_None)
    # Slot 1: gP1LifePoints REF
    # Slot 2: PLAYER_BLOCK_STRIDE EQ
]

BLOCK_PLATE = (
    "fn_eligible for CID 0x1776 (Corpse of Yata-Garasu, pw=30461781); "
    "reached via card effect handler dispatch table at ROM 0x09e4204c. "
    "Reads player LP status word gP1LifePoints[player*PLAYER_BLOCK_STRIDE+LP_SLOT_ACTIVE_OFF(0x10)]; "
    "if nonzero returns 2, if zero returns 0. indeg=0; runtime-only via fn-ptr."
)


def main():
    print("=== DisassembleF07Seg7Block (DRY=%s) ===" % DRY)
    print("  Block: 0x%08x..0x%08x (fn@0x%08x = %s)" % (BLOCK_LO, BLOCK_HI, BLOCK_FN, BLOCK_NAME))

    if DRY:
        print("[dry] clearListing+setTMode 0x%08x..0x%08x" % (BLOCK_LO, BLOCK_HI))
        print("[dry] DisassembleCommand @ 0x%08x" % BLOCK_FN)
        print("[dry] createFunction %s @ 0x%08x" % (BLOCK_NAME, BLOCK_FN))
        print("[dry] literal pool slot 0x08061c84 -> gp1lp_ptr_08061c84 (REF->gP1LifePoints)")
        print("[dry] literal pool slot 0x08061c88 -> player_stride_08061c88 (EQ PLAYER_BLOCK_STRIDE)")
        print("[dry] setPlateComment @ 0x%08x (%d chars)" % (BLOCK_FN, len(BLOCK_PLATE)))
        return

    # Step 1: clear listing and set THUMB mode for entire block
    _clear_and_set_thumb(BLOCK_LO, BLOCK_HI)

    # Step 2: Disassemble from function entry (2B pad at 0x08061c66 is skipped)
    if _disasm_flow(BLOCK_FN):
        print("[ok ] Block fn 0x%08x" % BLOCK_FN)
    else:
        print("[warn] Block fn 0x%08x FAILED -- continuing" % BLOCK_FN)

    # Step 3: Force literal pool slots as DWORDs
    # Slot at 0x08061c84: gP1LifePoints = 0x0201c4e0 (REF slot)
    _create_dword_with_ref(
        0x08061c84, 'gp1lp_ptr_08061c84',
        0x0201c4e0, 'gP1LifePoints'
    )
    # Slot at 0x08061c88: PLAYER_BLOCK_STRIDE = 0x868 (EQ slot)
    _create_dword_eq(
        0x08061c88, 'player_stride_08061c88',
        'PLAYER_BLOCK_STRIDE', 0x00000868
    )

    # Step 4: Create function and set plate
    _create_function(BLOCK_FN, BLOCK_NAME)
    _set_plate(BLOCK_FN, BLOCK_PLATE)

    n = _count_instructions(BLOCK_FN, 0x08061c83)
    print("[Block] %d instructions (fn body before literal pool)" % n)

    print("\n=== DisassembleF07Seg7Block DONE ===")
    print("  Function: %s @ 0x%08x" % (BLOCK_NAME, BLOCK_FN))
    print("  Pool slots: gp1lp_ptr_08061c84 (REF) + player_stride_08061c88 (EQ)")


main()
