# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2FuncFix.py -- Create function at 0x08070900
#   check_zone_tile_count_and_set_summon_restriction_flag
#   Body: starts at 0x08070900 (push {r4-r7,lr} = 0xf0b5),
#   preceded by 2-byte alignment pad at 0x080708fe.
#   Currently exported as .byte because Ghidra has no function object.
#   This script:
#   1. Clears listing at 0x08070900..0x080708ff+stub_size
#   2. Sets TMode=THUMB
#   3. Runs DisassembleCommand at 0x08070900 (unrestricted)
#   4. Creates Ghidra function at 0x08070900 named check_zone_tile_count_and_set_summon_restriction_flag
#
# NOTE: All text is pure ASCII.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_205456-pre-F09Seg2

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


def main():
    print("=== RefineF09Seg2FuncFix (DRY=%s) ===" % DRY)

    FUNC_ADDR = 0x08070900
    FUNC_NAME = 'check_zone_tile_count_and_set_summon_restriction_flag'
    # Approximate end of function (conservatively large; disasm will stop at bx/pop{pc}/ret)
    FUNC_END  = 0x080709ff  # safe upper bound

    func_a = _addr(FUNC_ADDR)
    ctx = currentProgram.getProgramContext()
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()

    if DRY:
        print("[dry] Would clearListing 0x%08x..0x%08x" % (FUNC_ADDR, FUNC_END))
        print("[dry] Would setTMode THUMB=1")
        print("[dry] Would DisassembleCommand at 0x%08x" % FUNC_ADDR)
        fn = fm.getFunctionAt(func_a)
        if fn is not None:
            print("[dry] Function already exists: %s" % fn.getName())
        else:
            print("[dry] Would createFunction %s @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
        print("=== RefineF09Seg2FuncFix DRY DONE ===")
        return

    # Step 1: clearListing
    print("[1] clearListing 0x%08x..0x%08x" % (FUNC_ADDR, FUNC_END))
    try:
        clearListing(func_a, _addr(FUNC_END))
        print("    clearListing done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1")
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, func_a, _addr(FUNC_END), BigInteger.ONE)
        print("    TMode THUMB=1 set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand (unrestricted -- follow flow)
    print("[3] DisassembleCommand at 0x%08x" % FUNC_ADDR)
    cmd = DisassembleCommand(func_a, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    # Step 4: Create function object at FUNC_ADDR
    print("[4] createFunction %s @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
    fn = fm.getFunctionAt(func_a)
    if fn is not None:
        old_name = fn.getName()
        fn.setName(FUNC_NAME, SourceType.USER_DEFINED)
        print("[FUNC] 0x%08x: renamed %s -> %s" % (FUNC_ADDR, old_name, FUNC_NAME))
    else:
        # Try to create function
        try:
            from ghidra.program.model.symbol import SourceType as ST
            fn2 = fm.createFunction(FUNC_NAME, func_a,
                                    AddressSet(func_a, _addr(FUNC_ADDR + 0x100)),
                                    SourceType.USER_DEFINED)
            if fn2 is not None:
                print("[FUNC] created function %s @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
            else:
                print("[WARN] createFunction returned None")
        except Exception as e:
            print("[WARN] createFunction error: %s" % e)
            # Fallback: ensure label exists
            existing = [s.getName() for s in sym_tbl.getSymbols(func_a)]
            if FUNC_NAME not in existing:
                sym_tbl.createLabel(func_a, FUNC_NAME, SourceType.USER_DEFINED)
            print("[FUNC] label ensured @ 0x%08x" % FUNC_ADDR)

    print("\n=== RefineF09Seg2FuncFix DONE ===")


main()
