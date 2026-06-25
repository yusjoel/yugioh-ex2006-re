# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg7Stubs.py -- f11 Seg-7 THUMB disassembly of 2 callback stubs
#
# Range: 0x080904ec .. 0x080904f4 (8 bytes total)
#
# return_effect_node_result_0 @ 0x080904ec:
#   movs r0,#0  (0x2000)
#   bx lr       (0x4770)
#   indeg=10 THUMB+1 refs from effect node descriptor tables
#
# return_effect_node_result_2 @ 0x080904f0:
#   movs r0,#2  (0x2002)
#   bx lr       (0x4770)
#   indeg=9 THUMB+1 refs from effect node descriptor tables
#
# Post-disasm gate: grep asm/11 for ROM_INCBIN/.byte in [0x080904ec,0x080904f4) == 0
# All EOL/plate text is pure ASCII. Ghidra Jython mojibake prevention.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.listing import CodeUnit
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


def _check_bytes(addr_val, expected_bytes):
    mem = currentProgram.getMemory()
    a = _addr(addr_val)
    for i, b in enumerate(expected_bytes):
        actual = mem.getByte(_addr(addr_val + i)) & 0xFF
        if actual != b:
            print("FAIL byte check @0x%08x+%d: expected=0x%02x actual=0x%02x" % (
                addr_val, i, b, actual))
            return False
    return True


def _clear_and_setTMode(start_addr, end_addr):
    listing = currentProgram.getListing()
    a_start = _addr(start_addr)
    a_end   = _addr(end_addr)
    as_ = AddressSet(a_start, a_end.subtract(1))
    listing.clearCodeUnits(a_start, a_end.subtract(1), False)
    print("[DC] clearListing 0x%08x..0x%08x done" % (start_addr, end_addr))
    # set THUMB mode (TMode=1)
    ctx = currentProgram.getProgramContext()
    reg = ctx.getRegister("TMode")
    if reg is not None:
        ctx.setValue(reg, a_start, a_end.subtract(1), BigInteger.ONE)
        print("[DC] setTMode THUMB=1 for range done")
    else:
        print("WARN: TMode register not found")


def _disasm_at(addr_val):
    a = _addr(addr_val)
    as_ = AddressSet(a, a)
    cmd = DisassembleCommand(a, as_, True)
    cmd.applyTo(currentProgram)
    print("[DC] DisassembleCommand at 0x%08x done" % addr_val)


def _create_function(addr_val, name):
    a = _addr(addr_val)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is None:
        fn = fm.createFunction(name, a,
                               AddressSet(a, _addr(addr_val + 3)),
                               SourceType.USER_DEFINED)
        if fn is None:
            print("FAIL createFunction at 0x%08x %s" % (addr_val, name))
            return False
        print("[FN] createFunction 0x%08x  %s" % (addr_val, name))
    else:
        fn.setName(name, SourceType.USER_DEFINED)
        print("[FN] renamed existing function at 0x%08x  -> %s" % (addr_val, name))
    return True


def _set_plate(addr_val, text):
    a = _addr(addr_val)
    cu = currentProgram.getListing().getCodeUnitAt(a)
    if cu is None:
        print("FAIL PLATE 0x%08x: no code unit (WARN=FAIL)" % addr_val)
        return False
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[PLT] 0x%08x OK  len=%d" % (addr_val, len(text)))
    return True


def main():
    print("=== DisassembleF11Seg7Stubs (DRY=%s) ===" % DRY)
    print("  Range: 0x080904ec..0x080904f4 (8 bytes, 2 stubs)")

    # Verify ROM bytes
    print("\n--- Byte verification ---")
    ok0 = _check_bytes(0x080904ec, [0x00, 0x20, 0x70, 0x47])  # movs r0,#0; bx lr
    ok2 = _check_bytes(0x080904f0, [0x02, 0x20, 0x70, 0x47])  # movs r0,#2; bx lr
    if not ok0 or not ok2:
        print("ABORT: byte verification failed")
        return
    print("Byte verification PASS")

    if DRY:
        print("[dry] Would: clearListing+setTMode 0x080904ec..0x080904f4")
        print("[dry] Would: DisassembleCommand at 0x080904ec")
        print("[dry] Would: DisassembleCommand at 0x080904f0")
        print("[dry] Would: createFunction return_effect_node_result_0 @ 0x080904ec")
        print("[dry] Would: createFunction return_effect_node_result_2 @ 0x080904f0")
        print("[dry] Would: PLATE @ 0x080904ec")
        print("[dry] Would: PLATE @ 0x080904f0")
        print("=== DRY RUN COMPLETE ===")
        return

    # Step 1: clearListing + setTMode for full range
    print("\n--- Step 1: clearListing + setTMode ---")
    _clear_and_setTMode(0x080904ec, 0x080904f4)

    # Step 2: DisassembleCommand for each 4-byte stub separately
    print("\n--- Step 2: DisassembleCommand ---")
    _disasm_at(0x080904ec)
    _disasm_at(0x080904f0)

    # Step 3: createFunction + name
    print("\n--- Step 3: createFunction + name ---")
    _create_function(0x080904ec, "return_effect_node_result_0")
    _create_function(0x080904f0, "return_effect_node_result_2")

    # Step 4: PLATE comments (ASCII only)
    print("\n--- Step 4: PLATE ---")
    _set_plate(0x080904ec,
        "Effect-node callback stub: returns 0. Stored as fn_activate/fn_eligible pointer in "
        "effect node descriptor tables (TYPE0/1/2/3 at 0x09e40xxx-0x09e42c58); 10 THUMB+1 refs.")
    _set_plate(0x080904f0,
        "Effect-node callback stub: returns 2. Stored as fn_activate/fn_eligible pointer in "
        "effect node descriptor tables (TYPE0/1/2/3 at 0x09e3f6xx-0x09e452xx); 9 THUMB+1 refs.")

    print("\n=== DisassembleF11Seg7Stubs COMPLETE ===")


main()
