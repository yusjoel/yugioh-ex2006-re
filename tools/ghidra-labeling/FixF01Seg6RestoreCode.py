# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF01Seg6RestoreCode.py -- restore 0x0801fbc0 as code after DWORD fix
#   createDWord at 0x0801fbc0 was incorrect (it's a branch target/code)
#   Restore it to THUMB code by clearListing + setTMode + DisassembleCommand

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

# 0x0801fbc0 is a THUMB code target (bgt/b from 0x1fba4/0x1fbb0)
# It was incorrectly forced to DWORD in FixF01Seg6LiteralPools.py
# Restore by disassembling this area
# Range: restore the sub-handler starting at 0x0801fbc0
# End: the next labeled item (0x0801fbd4 = LAB_0801fbd4 from surrounding asm)
RESTORE_ADDR = 0x0801fbc0
RESTORE_HI = 0x0801fbcf  # just enough to restore; let flow handle the rest


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF01Seg6RestoreCode (DRY=%s) ===" % DRY)
    print("  Restoring 0x%08x as THUMB code (incorrectly set to DWORD)" % RESTORE_ADDR)

    lo = _addr(RESTORE_ADDR)
    hi = _addr(RESTORE_HI)

    if DRY:
        print("[dry] would clearListing(0x%08x..0x%08x) + setTMode=THUMB + DisassembleCommand" % (
            RESTORE_ADDR, RESTORE_HI))
        return

    # 1) Clear the data we incorrectly created
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (RESTORE_ADDR, RESTORE_HI))
    except Exception as e:
        print("[warn] clearListing: %s" % e)

    # 2) Set TMode=THUMB
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (RESTORE_ADDR, RESTORE_HI))

    # 3) Disassemble from RESTORE_ADDR
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (RESTORE_ADDR, cmd.getStatusMsg()))
    else:
        print("[ok ] disassembled 0x%08x" % RESTORE_ADDR)

    print("=== FixF01Seg6RestoreCode DONE ===")


main()
