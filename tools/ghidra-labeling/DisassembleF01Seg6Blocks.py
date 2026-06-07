# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF01Seg6Blocks.py -- f01 Seg-6 R4 disasm (4 blocks)
#   Block1: 0x0801f4d0..0x0801fb5f (0x690 B) -- tick_duel_puzzle_scene_step cases 0..7
#   Block2: 0x0801fb90..0x0801fe91 (0x302 B) -- tick_duel_puzzle_scene_step cases 8..13,20
#   Block3: 0x080202fe..0x08020333 (0x36 B)  -- 2-byte pad + tick_lp_record_scene_step
#   Block4: 0x08020370..0x08020db3 (0xa44 B) -- tick_lp_record_scene_step cases 0..13
#
#   Pattern: DisassembleSeg9BlockB.py / DisassembleSeg5cJpHandlers.py
#   - clearListing entire block range first (avoid ContextChangeException)
#   - setTMode=THUMB for entire range
#   - per-stub DisassembleCommand for each entry point
#   - createFunction for named functions (tick_lp_record_scene_step in Block3)
#
#   Block1 entry points (step cases 0..7 + sub-handler cluster):
#     case 0: 0x0801f4d0
#     case 1: 0x0801f5ec
#     case 2: 0x0801f60c
#     case 3: 0x0801f738
#     case 4: 0x0801f9c4
#     case 5: 0x0801f9e0
#     case 6: 0x0801fb20
#     case 7: 0x0801fb2c
#
#   Block2 entry points (step cases 8..13, 20 + sub-dispatch cluster):
#     sub-dispatch: 0x0801fb90, 0x0801fb94, 0x0801fb98, 0x0801fb9c, 0x0801fbb2
#     (repeated): 0x0801fbbe (6 table entries, 1 label)
#     case 8:  0x0801fbe4
#     case 9:  0x0801fc18
#     case 10: 0x0801fd48
#     case 11: 0x0801fd80
#     case 12: 0x0801fe14
#     case 13: 0x0801fe54
#     case 20: 0x0801fe7c
#
#   Block3: 0x080202fe (2B pad=0x0000), 0x08020300 = tick_lp_record_scene_step
#
#   Block4 entry points (14 cases of tick_lp_record_scene_step):
#     case 0:  0x08020370
#     case 1:  0x08020524
#     case 2:  0x08020544
#     case 3:  0x08020670
#     case 4:  0x080209f4
#     case 5:  0x08020a10
#     case 6:  0x08020b50
#     case 7:  0x08020b6c
#     case 8:  0x08020b88
#     case 9:  0x08020ba4
#     case 10: 0x08020d00
#     case 11: 0x08020d34
#     case 12: 0x08020d94
#     case 13: 0x08020d4c
#
#   backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260607-092723-pre-f01s6

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
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


def _disasm_stub(addr, size):
    """Disassemble a single stub at addr for size bytes."""
    lo = _addr(addr)
    hi = _addr(addr + size - 1)
    cmd = DisassembleCommand(lo, AddressSet(lo, hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x (%dB): %s" % (addr, size, cmd.getStatusMsg()))
        return False
    return True


def _disasm_flow(addr):
    """Disassemble at addr, let flow continue naturally (no size limit)."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


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


def _create_function(addr, name):
    """Create a named function at addr."""
    a = _addr(addr)
    sym_tbl = currentProgram.getSymbolTable()
    fn_mgr = currentProgram.getFunctionManager()

    # Check if function already exists
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing function at 0x%08x -> %s" % (addr, name))
        else:
            print("[FN ] function already exists at 0x%08x: %s" % (addr, name))
        return

    # Create function via command
    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr, cmd.getStatusMsg()))
        # Try label creation as fallback
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr))


# ---------------------------------------------------------------------------
# Block1: 0x0801f4d0..0x0801fb5f (0x690 B = 1680 B)
# Entry points: step cases 0..7 + sub-dispatch at end
# Each stub flows until a branch (bx/pop+bx/b) exits
# ---------------------------------------------------------------------------
BLOCK1_LO = 0x0801f4d0
BLOCK1_HI = 0x0801fb5f  # exclusive end: 0x0801fb60 -> HI = 0x0801fb5f

# Entry points from step table PTR_DAT_0801f47c and sub-dispatch PTR_DAT_0801fb64
BLOCK1_ENTRIES = [
    0x0801f4d0,  # case 0 (step 0)
    0x0801f5ec,  # case 1
    0x0801f60c,  # case 2
    0x0801f738,  # case 3
    0x0801f9c4,  # case 4
    0x0801f9e0,  # case 5
    0x0801fb20,  # case 6
    0x0801fb2c,  # case 7
]

# ---------------------------------------------------------------------------
# Block2: 0x0801fb90..0x0801fe91 (0x302 B = 770 B)
# Entry points: sub-dispatch cluster + step cases 8..13,20
# ---------------------------------------------------------------------------
BLOCK2_LO = 0x0801fb90
BLOCK2_HI = 0x0801fe91  # exclusive end: 0x0801fe92 -> HI = 0x0801fe91

BLOCK2_ENTRIES = [
    0x0801fb90,  # sub-dispatch handler 0
    0x0801fb94,  # sub-dispatch handler 1
    0x0801fb98,  # sub-dispatch handler 4
    0x0801fb9c,  # sub-dispatch handler 9
    0x0801fbb2,  # sub-dispatch handler target
    0x0801fbbe,  # sub-dispatch default/overflow handler (6 table entries)
    0x0801fbe4,  # case 8
    0x0801fc18,  # case 9
    0x0801fd48,  # case 10
    0x0801fd80,  # case 11
    0x0801fe14,  # case 12
    0x0801fe54,  # case 13
    0x0801fe7c,  # case 20
]

# ---------------------------------------------------------------------------
# Block3: 0x080202fe..0x08020333 (0x36 B = 54 B)
# Layout: 2B pad (0x0000) at 0x202fe, then function at 0x08020300
# Function name: tick_lp_record_scene_step (med-conf, reviewer creat)
# ---------------------------------------------------------------------------
BLOCK3_LO = 0x080202fe
BLOCK3_HI = 0x08020333  # exclusive end: 0x08020334 -> HI = 0x08020333
BLOCK3_FN_ADDR = 0x08020300
BLOCK3_FN_NAME = "tick_lp_record_scene_step"

# ---------------------------------------------------------------------------
# Block4: 0x08020370..0x08020db3 (0xa44 B = 2628 B)
# Entry points: 14 cases from PTR_DAT_08020338 step table
# ---------------------------------------------------------------------------
BLOCK4_LO = 0x08020370
BLOCK4_HI = 0x08020db3  # exclusive end: 0x08020db4 = render_lp_record_text_set_a

BLOCK4_ENTRIES = [
    0x08020370,  # case 0
    0x08020524,  # case 1
    0x08020544,  # case 2
    0x08020670,  # case 3
    0x080209f4,  # case 4
    0x08020a10,  # case 5
    0x08020b50,  # case 6
    0x08020b6c,  # case 7
    0x08020b88,  # case 8
    0x08020ba4,  # case 9
    0x08020d00,  # case 10
    0x08020d34,  # case 11
    0x08020d94,  # case 12
    0x08020d4c,  # case 13
]


def main():
    print("=== DisassembleF01Seg6Blocks (DRY=%s) ===" % DRY)
    print("  4 blocks: B1(0x%08x..0x%08x) B2(0x%08x..0x%08x)" % (
        BLOCK1_LO, BLOCK1_HI, BLOCK2_LO, BLOCK2_HI))
    print("           B3(0x%08x..0x%08x) B4(0x%08x..0x%08x)" % (
        BLOCK3_LO, BLOCK3_HI, BLOCK4_LO, BLOCK4_HI))

    if DRY:
        print("[dry] Block1: clearListing+setTMode+%d stubs" % len(BLOCK1_ENTRIES))
        for e in BLOCK1_ENTRIES:
            print("  entry 0x%08x" % e)
        print("[dry] Block2: clearListing+setTMode+%d stubs" % len(BLOCK2_ENTRIES))
        for e in BLOCK2_ENTRIES:
            print("  entry 0x%08x" % e)
        print("[dry] Block3: clearListing+setTMode+2B_pad+fn@0x%08x=%s" % (
            BLOCK3_FN_ADDR, BLOCK3_FN_NAME))
        print("[dry] Block4: clearListing+setTMode+%d stubs" % len(BLOCK4_ENTRIES))
        for e in BLOCK4_ENTRIES:
            print("  entry 0x%08x" % e)
        return

    # --- Block 1 ---
    print("\n--- Block1: 0x%08x..0x%08x (%d entries) ---" % (
        BLOCK1_LO, BLOCK1_HI, len(BLOCK1_ENTRIES)))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)

    b1_ok = 0
    for entry in BLOCK1_ENTRIES:
        if _disasm_flow(entry):
            b1_ok += 1
            print("[ok ] Block1 entry 0x%08x" % entry)
        else:
            print("[warn] Block1 entry 0x%08x FAILED" % entry)

    n1 = _count_instructions(BLOCK1_LO, BLOCK1_HI)
    print("[Block1] %d instructions, %d/%d entries ok" % (n1, b1_ok, len(BLOCK1_ENTRIES)))

    # --- Block 2 ---
    print("\n--- Block2: 0x%08x..0x%08x (%d entries) ---" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_ENTRIES)))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)

    b2_ok = 0
    for entry in BLOCK2_ENTRIES:
        if _disasm_flow(entry):
            b2_ok += 1
            print("[ok ] Block2 entry 0x%08x" % entry)
        else:
            print("[warn] Block2 entry 0x%08x FAILED" % entry)

    n2 = _count_instructions(BLOCK2_LO, BLOCK2_HI)
    print("[Block2] %d instructions, %d/%d entries ok" % (n2, b2_ok, len(BLOCK2_ENTRIES)))

    # --- Block 3 ---
    print("\n--- Block3: 0x%08x..0x%08x (2B pad + fn@0x%08x=%s) ---" % (
        BLOCK3_LO, BLOCK3_HI, BLOCK3_FN_ADDR, BLOCK3_FN_NAME))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)

    # Disassemble from function start (skip 2B pad at 0x202fe)
    if _disasm_flow(BLOCK3_FN_ADDR):
        print("[ok ] Block3 fn 0x%08x" % BLOCK3_FN_ADDR)
    else:
        print("[warn] Block3 fn 0x%08x FAILED" % BLOCK3_FN_ADDR)

    # Create named function
    _create_function(BLOCK3_FN_ADDR, BLOCK3_FN_NAME)

    n3 = _count_instructions(BLOCK3_FN_ADDR, BLOCK3_HI)
    print("[Block3] %d instructions (fn range)" % n3)

    # --- Block 4 ---
    print("\n--- Block4: 0x%08x..0x%08x (%d entries) ---" % (
        BLOCK4_LO, BLOCK4_HI, len(BLOCK4_ENTRIES)))
    _clear_and_set_thumb(BLOCK4_LO, BLOCK4_HI)

    b4_ok = 0
    for entry in BLOCK4_ENTRIES:
        if _disasm_flow(entry):
            b4_ok += 1
            print("[ok ] Block4 entry 0x%08x" % entry)
        else:
            print("[warn] Block4 entry 0x%08x FAILED" % entry)

    n4 = _count_instructions(BLOCK4_LO, BLOCK4_HI)
    print("[Block4] %d instructions, %d/%d entries ok" % (n4, b4_ok, len(BLOCK4_ENTRIES)))

    # Summary
    total = n1 + n3 + n4 + n2
    print("\n=== DisassembleF01Seg6Blocks DONE ===")
    print("  Block1=%d instr  Block2=%d instr  Block3=%d instr  Block4=%d instr" % (
        n1, n2, n3, n4))
    print("  Total=%d instructions disassembled across 4 blocks" % total)
    print("  tick_lp_record_scene_step created @ 0x%08x" % BLOCK3_FN_ADDR)


main()
