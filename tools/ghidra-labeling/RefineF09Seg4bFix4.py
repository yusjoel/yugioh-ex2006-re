# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bFix4.py -- Disasm hidden region 0x726e6..0x726f3 (LAB_080726e6/e8)
#
# Problem: DisassembleCommand from 0x726d2 reaches branch 'b LAB_080726e8' at 0x726e4
# but only disasms starting from 0x726e8, leaving 0x726e6 (2 bytes earlier) as undisasmed.
# Branch at 0x726d0 targets LAB_080726e6 = 0x726e6, which is the entry.
# Both LAB_080726e6 and LAB_080726e8 are inside the same THUMB instruction stream.
# Solution: clearListing 0x726e6..0x726f3, setTMode, DisassembleCommand at 0x726e6.
# This produces sequential instructions at 0x726e6, 0x726e8, ..., covering both labels.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

listing = currentProgram.getListing()
sym_tbl = currentProgram.getSymbolTable()
ctx = currentProgram.getProgramContext()
tmode = ctx.getRegister("TMode")

print("=== RefineF09Seg4bFix4 ===")

# Region: 0x080726e6..0x080726f3 (14 bytes)
# LAB_080726e6 at 0x726e6 (entry from b at 0x726d0)
# LAB_080726e8 at 0x726e8 (entry from b at 0x726d4/0x7260a/0x72622/0x72644/0x72672/0x726ae/0x726e4)
R_START = 0x080726e6
R_END   = 0x080726f3

print("--- Region 0x%08x..0x%08x ---" % (R_START, R_END))
a_lo = _addr(R_START)
a_hi = _addr(R_END)

try:
    clearListing(a_lo, a_hi)
    print("[CLEAR] done")
except Exception as e:
    print("[WARN] clearListing: %s" % e)

if tmode is not None:
    ctx.setValue(tmode, a_lo, a_hi, BigInteger.ONE)
    print("[TMODE] set")

cmd = DisassembleCommand(a_lo, None, False)
if cmd.applyTo(currentProgram):
    print("[DISASM] ok @ 0x%08x" % R_START)
else:
    print("[WARN] disasm: %s" % cmd.getStatusMsg())

# Ensure USER_DEFINED labels for both targets
for addr_val, label_name in [
    (0x080726e6, 'LAB_080726e6'),
    (0x080726e8, 'LAB_080726e8'),
]:
    addr = _addr(addr_val)
    ud_exists = any(s.getName() == label_name and str(s.getSource()) == 'USER_DEFINED'
                   for s in sym_tbl.getSymbols(addr))
    if not ud_exists:
        try:
            sym_tbl.createLabel(addr, label_name, SourceType.USER_DEFINED)
            print("[LABEL] %s @ 0x%08x created" % (label_name, addr_val))
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (label_name, e))
    else:
        print("[LABEL] %s already USER_DEFINED" % label_name)

print("=== RefineF09Seg4bFix4 DONE ===")
