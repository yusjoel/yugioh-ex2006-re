# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg4bDisasm.py -- file 03 Seg-4b R4 disasm
#   ROM_INCBIN 0x39350/0x10ce (0x08039350..0x0803a41d)
#   Dispatch: dispatch_equip_node_by_type (mov pc,r0 jump table)
#   6 sub-stubs via jump table at 0x0803931c (13 entries, types 1..13)
#
# Steps:
#   1. clearListing(0x08039350, 0x0803a41d)
#   2. setTMode(THUMB=1) for entire range
#   3. DisassembleCommand per stub (per-stub, not whole range at once)
#   4. createFunction per stub
#   5. Rename stubs to semantic names

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

def _addr(val):
    return toAddr(val)

print("=== RefineF03Seg4bDisasm.py DRY=%s ===" % DRY)

lo = _addr(0x08039350)
hi = _addr(0x0803a41d)

if not DRY:
    # Step 1: clear listing
    print("clearListing 0x08039350..0x0803a41d")
    clearListing(lo, hi)

    # Step 2: set THUMB mode for full range
    print("setTMode 0x08039350..0x0803a41d")
    ctx = currentProgram.getProgramContext()
    tmode_reg = ctx.getRegister("TMode")
    ctx.setValue(tmode_reg, lo, hi, BigInteger.ONE)
else:
    print("DRY: would clearListing + setTMode 0x08039350..0x0803a41d")

# Step 3: disasm each sub-stub individually
# NOTE: per-stub DisassembleCommand required (single whole-range disasm only does first stub)
stubs = [
    (0x08039350, 0x08039a61, 'eval_equip_node_type_1_to_4'),   # types 1,2,3,4
    (0x08039a62, 0x08039a7b, 'eval_equip_node_type_5'),         # type 5
    (0x08039a7c, 0x08039c1b, 'eval_equip_node_type_6_to_9'),    # types 6,7,8,9
    (0x08039c1c, 0x0803a2fb, 'eval_equip_node_type_10_to_11'), # types 10,11
    (0x0803a2fc, 0x0803a3c3, 'eval_equip_node_type_13'),        # type 13
    (0x0803a3c4, 0x0803a41d, 'eval_equip_node_type_12'),        # type 12
]

applied = 0
for (start, end, name) in stubs:
    s = _addr(start)
    e = _addr(end)
    if DRY:
        print("DRY DISASM: 0x%08x..0x%08x -> %s" % (start, end, name))
    else:
        print("Disasm: 0x%08x..0x%08x -> %s" % (start, end, name))
        cmd = DisassembleCommand(s, AddressSet(s, e), True)
        cmd.applyTo(currentProgram)
        createFunction(s, None)
        # Rename function to semantic name
        fn = getFunctionAt(s)
        if fn is not None:
            fn.setName(name, SourceType.USER_DEFINED)
            print("  Renamed function to %s" % name)
        else:
            print("  WARN: no function at 0x%08x, creating label" % start)
            currentProgram.getSymbolTable().createLabel(s, name, SourceType.USER_DEFINED)
    applied += 1

print("=== DONE: %d stubs processed ===" % applied)
