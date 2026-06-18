# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2BodyFix.py -- Re-disassemble function body stub at 0x0807098c
#   This is the branch target LAB_0807098c within test_equip_zone_target_with_activation_state.
#   After multiple clearListing/disasm cycles the body at 0x0807098c..0x080709ff
#   is still showing as ROM_INCBIN.
#   This script clears and directly disassembles at 0x0807098c.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
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
    print("=== RefineF09Seg2BodyFix (DRY=%s) ===" % DRY)

    BODY_LO = 0x0807098c
    BODY_HI = 0x080709ff
    lo_a = _addr(BODY_LO)
    hi_a = _addr(BODY_HI)
    ctx = currentProgram.getProgramContext()

    if DRY:
        print("[dry] Would clearListing 0x%08x..0x%08x + disasm" % (BODY_LO, BODY_HI))
        return

    # clearListing
    print("[1] clearListing 0x%08x..0x%08x" % (BODY_LO, BODY_HI))
    try:
        clearListing(lo_a, hi_a)
        print("    done")
    except Exception as e:
        print("[WARN] %s" % e)

    # setTMode THUMB=1
    print("[2] setTMode THUMB=1")
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo_a, hi_a, BigInteger.ONE)
        print("    TMode set")

    # DisassembleCommand AT 0x0807098c directly (the body branch target)
    print("[3] DisassembleCommand at 0x%08x" % BODY_LO)
    cmd = DisassembleCommand(lo_a, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok at 0x%08x" % BODY_LO)
    else:
        print("[WARN] disasm 0x%08x: %s" % (BODY_LO, cmd.getStatusMsg()))

    print("=== RefineF09Seg2BodyFix DONE ===")


main()
