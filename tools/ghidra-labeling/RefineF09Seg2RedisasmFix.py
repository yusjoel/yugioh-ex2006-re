# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2RedisasmFix.py -- Re-disassemble test_equip_zone_target_with_activation_state
#   Range cleared by RefineF09Seg2FuncFix: 0x08070900..0x080709ff
#   Function test_equip_zone_target_with_activation_state starts at 0x0807097c
#   After pool fix (0x08070974/0x08070978 as DWord), the cleared range 0x0807097c..0x080709ff
#   needs re-disassembly.
#
# NOTE: All text is pure ASCII.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_205456-pre-F09Seg2

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
    print("=== RefineF09Seg2RedisasmFix (DRY=%s) ===" % DRY)

    # test_equip_zone_target_with_activation_state starts at 0x0807097c
    # (cleared area: 0x0807097c..0x080709ff)
    FN_ENTRY = 0x0807097c
    FN_END   = 0x080709ff

    fn_a = _addr(FN_ENTRY)
    ctx = currentProgram.getProgramContext()

    if DRY:
        print("[dry] Would setTMode THUMB=1 for 0x%08x..0x%08x" % (FN_ENTRY, FN_END))
        print("[dry] Would DisassembleCommand at 0x%08x" % FN_ENTRY)
        print("=== RefineF09Seg2RedisasmFix DRY DONE ===")
        return

    # Step 1: clearListing just the affected range (not the pool!)
    print("[1] clearListing 0x%08x..0x%08x" % (FN_ENTRY, FN_END))
    try:
        clearListing(fn_a, _addr(FN_END))
        print("    clearListing done")
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Step 2: setTMode THUMB=1
    print("[2] setTMode THUMB=1")
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, fn_a, _addr(FN_END), BigInteger.ONE)
        print("    TMode THUMB=1 set")
    else:
        print("[WARN] TMode register not found")

    # Step 3: DisassembleCommand at function entry (unrestricted)
    print("[3] DisassembleCommand at 0x%08x" % FN_ENTRY)
    cmd = DisassembleCommand(fn_a, None, False)
    if cmd.applyTo(currentProgram):
        print("    disasm ok")
    else:
        print("[WARN] disasm: %s" % cmd.getStatusMsg())

    print("\n=== RefineF09Seg2RedisasmFix DONE ===")


main()
