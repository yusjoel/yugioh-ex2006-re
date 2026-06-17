# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg8cBlocks.py -- F08 Seg-8c R4 disasm (2 blocks)
#
# Block1: 0x0806c3d8..0x0806c41b (0x44 B)
#   fn_eligible handler for CID=0x1369 (Morphing Jar #2); THUMB+1 ref @0x1e43760
#   Literal pool inside block at 0x0806c418: .word 0x0806c41c (jump table start ptr)
#   1 function: check_equip_eligible_morphing_jar_2 @ 0x0806c3d8
#
# Block2: 0x0806c440..0x0806c6d7 (0x298 B)
#   9-entry raw-addr jump table at 0x0806c41c..0x0806c43c (ALREADY structured in asm as .word)
#   raw ref @0x0806c43c (entry[8] = block start 0x0806c440)
#   8 unique stub entry points (entry[1] and entry[2] share 0x0806c6c0)
#
# NOTE: Each block: clearListing + setTMode(THUMB) on full range first,
#   then DisassembleCommand per stub entry point (single-range only disasms first stub).
#   Literal pool at 0x0806c418 handled by createDWord before disasm to prevent
#   Ghidra treating it as code.
#
# NOTE: All plate text is pure ASCII (no CJK). Jython CJK = double-UTF-8 mojibake.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_pre-F08Seg8c

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
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


def _create_dword(addr):
    """Force a DWORD data item at addr to split any existing code/data."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    existing = listing.getCodeUnitAt(a)
    if existing is not None:
        try:
            clearListing(a, a)
        except Exception as e:
            print("[warn] clearListing for dword at 0x%08x: %s" % (addr, e))
    try:
        listing.createData(a, DWordDataType.dataType)
        print("[DWORD] created at 0x%08x" % addr)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr, e))


def _disasm_flow(addr):
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
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
        print("[FN ] label fallback %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
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


# ===========================================================================
# BLOCK 1: 0x0806c3d8..0x0806c41b (0x44 B)
#   fn_eligible handler for CID=0x1369 Morphing Jar #2
#   THUMB+1 ref @0x1e43760 -> 0x0806c3d9 = block+1
#   Literal pool at 0x0806c418: .word 0x0806c41c (9-entry jump table ptr)
#   1 function
# ===========================================================================
BLOCK1_LO = 0x0806c3d8
BLOCK1_HI = 0x0806c41b

# Literal pool word inside block -- must createDWord before disasm
BLOCK1_LIT_POOL = 0x0806c418

BLOCK1_FNS = [
    (0x0806c3d8, 'check_equip_eligible_morphing_jar_2',
     'fn_eligible handler for MORPHING_JAR_2_CID=0x1369 (Morphing Jar #2 pw=79106360; card-stats.s card_0774). '
     'THUMB+1 ref at dispatch table @0x1e43760: entry layout [fn_activate+1, pad, CID=0x1369, fn_eligible+1=0x0806c3d9, pad]. '
     'Reads gDuelPhaseFlags+EQUIP_PHASE_FRAME_OFF state; dispatches via 9-entry raw-addr jump table at 0x0806c41c. '
     'Literal pool at 0x0806c418: .word 0x0806c41c. '
     'Block range 0x0806c3d8..0x0806c41b.'),
]

# ===========================================================================
# BLOCK 2: 0x0806c440..0x0806c6d7 (0x298 B)
#   9-entry raw-addr jump table at 0x0806c41c..0x0806c43c (already structured in asm)
#   raw ref @0x0806c43c (entry[8] = block start 0x0806c440)
#   8 unique stub entry points (entry[1,2] shared -> 0x0806c6c0)
# ===========================================================================
BLOCK2_LO = 0x0806c440
BLOCK2_HI = 0x0806c6d7

BLOCK2_FNS = [
    # Ordered by stub address (not table index)
    (0x0806c440, 'morphing_jar2_state_stub_c440',
     'Entry[8]/block-start stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table @0x0806c41c, entry[8] at 0x0806c43c -> 0x0806c440. '
     'movs r0,#0 path: default/case8 state init. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c4e8, 'morphing_jar2_state_stub_c4e8',
     'Entry[7] stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table entry[7] at 0x0806c438 -> 0x0806c4e8. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c52c, 'morphing_jar2_state_stub_c52c',
     'Entry[6] stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table entry[6] at 0x0806c434 -> 0x0806c52c. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c5f8, 'morphing_jar2_state_stub_c5f8',
     'Entry[5] stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table entry[5] at 0x0806c430 -> 0x0806c5f8. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c63c, 'morphing_jar2_state_stub_c63c',
     'Entry[4] stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table entry[4] at 0x0806c42c -> 0x0806c63c. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c65a, 'morphing_jar2_state_stub_c65a',
     'Entry[3] stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table entry[3] at 0x0806c428 -> 0x0806c65a. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c69c, 'morphing_jar2_state_stub_c69c',
     'Entry[0] stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table entry[0] at 0x0806c41c -> 0x0806c69c. '
     'Block range 0x0806c440..0x0806c6d7.'),
    (0x0806c6c0, 'morphing_jar2_state_stub_c6c0',
     'Entry[1,2] shared stub for Morphing Jar #2 state dispatch. '
     '9-entry raw-addr jump table: entry[1] at 0x0806c420 -> 0x0806c6c0, entry[2] at 0x0806c424 -> 0x0806c6c0. '
     'Block range 0x0806c440..0x0806c6d7.'),
]


def main():
    total_fns = len(BLOCK1_FNS) + len(BLOCK2_FNS)
    print("=== DisassembleF08Seg8cBlocks (DRY=%s) ===" % DRY)
    print("  Block1: 0x%08x..0x%08x (%d fn, fn_eligible morphing_jar_2)" % (
        BLOCK1_LO, BLOCK1_HI, len(BLOCK1_FNS)))
    print("  Block2: 0x%08x..0x%08x (%d stubs, morphing_jar2_state_stub_*)" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    print("  Total new functions: %d" % total_fns)

    if DRY:
        for addr, name, _ in BLOCK1_FNS:
            print("[dry] Block1 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK2_FNS:
            print("[dry] Block2 fn: %s @ 0x%08x" % (name, addr))
        print("[dry] total fns=%d" % total_fns)
        return

    # =========================================================================
    # Block1: 0x0806c3d8..0x0806c41b
    # fn_eligible for CID=0x1369 Morphing Jar #2
    # Literal pool at 0x0806c418 must be forced DWORD before disasm
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (fn_eligible Morphing Jar #2) ---" % (BLOCK1_LO, BLOCK1_HI))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    # Force DWORD at literal pool to prevent disasm from eating it
    _create_dword(BLOCK1_LIT_POOL)
    for addr, name, _ in BLOCK1_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK1_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block1: %d fn created" % len(BLOCK1_FNS))

    # =========================================================================
    # Block2: 0x0806c440..0x0806c6d7
    # 8 state stubs for Morphing Jar #2 (jump table already structured in asm)
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (%d stubs, morphing_jar2) ---" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    for addr, name, _ in BLOCK2_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK2_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block2: %d stubs created" % len(BLOCK2_FNS))

    print("\n=== DisassembleF08Seg8cBlocks DONE ===")
    print("  Total new functions: %d" % total_fns)
    print("  Block1: %d (check_equip_eligible_morphing_jar_2)" % len(BLOCK1_FNS))
    print("  Block2: %d (morphing_jar2_state_stub_*)" % len(BLOCK2_FNS))


main()
