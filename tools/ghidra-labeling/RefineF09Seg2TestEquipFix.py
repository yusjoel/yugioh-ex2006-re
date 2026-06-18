# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2TestEquipFix.py -- Re-disassemble test_equip_zone_target_with_activation_state
#   Function range: 0x0807097c..0x08070aff (upper bound safe; ends before next function)
#   The internal ROM_INCBIN 0x7098c, 0x74 needs to be replaced by proper disasm.

from ghidra.app.cmd.disassemble import DisassembleCommand
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


def main():
    print("=== RefineF09Seg2TestEquipFix (DRY=%s) ===" % DRY)

    # Function range for test_equip_zone_target_with_activation_state
    # Previous ROM_INCBIN covered 0x0807098c..0x080709ff (0x74 bytes)
    # The function body continues past 0x08070a00 as well (already disassembled)
    # We need to clear+disasm the internal gap at 0x0807098c..0x080709ff
    CLEAR_LO = 0x0807098c
    CLEAR_HI = 0x080709ff
    ENTRY    = 0x0807098c  # start of the stub body gap (LAB_0807098c branch target)

    lo_a = _addr(CLEAR_LO)
    hi_a = _addr(CLEAR_HI)
    ctx = currentProgram.getProgramContext()

    if DRY:
        print("[dry] Would clearListing 0x%08x..0x%08x" % (CLEAR_LO, CLEAR_HI))
        print("[dry] Would setTMode THUMB=1")
        print("[dry] Would DisassembleCommand at 0x%08x" % ENTRY)
        print("=== RefineF09Seg2TestEquipFix DRY DONE ===")
        return

    # Step 1: clearListing the internal gap
    print("[1] clearListing 0x%08x..0x%08x" % (CLEAR_LO, CLEAR_HI))
    try:
        clearListing(lo_a, hi_a)
        print("    clearListing done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1")
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo_a, hi_a, BigInteger.ONE)
        print("    TMode THUMB=1 set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand (unrestricted -- follow flow from function start)
    # Re-disassemble from function entry to rebuild the full CFG
    fn_entry = _addr(0x0807097c)
    print("[3] DisassembleCommand at 0x0807097c (function entry, unrestricted)")
    cmd = DisassembleCommand(fn_entry, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    print("\n=== RefineF09Seg2TestEquipFix DONE ===")


main()
