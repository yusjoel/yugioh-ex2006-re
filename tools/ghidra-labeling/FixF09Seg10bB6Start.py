# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# Fix B6 start: clear+setTMode+disasm 0x0807965c..0x0807965f (4 bytes missed)
# fn_eligible_order_to_charge_or_smash starts at 0x7965c (PUSH {r4-r7,lr} = 0xb5f0)
# The main disasm script started at 0x79660 by mistake.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def main():
    print("=== Fix B6 start @ 0x0807965c ===")
    lo = _addr(0x0807965c)
    hi = _addr(0x0807965f)
    
    # clearListing
    clearListing(lo, hi)
    print("[ok] clearListing 0x0807965c..0x0807965f")
    
    # setTMode
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok] setTMode=1 for 0x0807965c..0x0807965f")
    
    # disasm at 0x7965c (will continue into already-decoded 0x79660+ range)
    cmd = DisassembleCommand(lo, AddressSet(lo, _addr(0x080796ab)), True)
    if cmd.applyTo(currentProgram):
        print("[ok] disasm fn_eligible_order_to_charge_or_smash @ 0x0807965c")
    else:
        print("[warn] disasm: %s" % cmd.getStatusMsg())
    
    # Add/update function at 0x7965c
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(lo)
    if fn is not None:
        print("[ok] function exists at 0x0807965c: %s" % fn.getName())
        if fn.getName() != 'fn_eligible_order_to_charge_or_smash':
            fn.setName('fn_eligible_order_to_charge_or_smash', SourceType.USER_DEFINED)
    else:
        try:
            fm.createFunction('fn_eligible_order_to_charge_or_smash', lo,
                              AddressSet(lo, _addr(0x080796ab)), SourceType.USER_DEFINED)
            print("[ok] createFunction fn_eligible_order_to_charge_or_smash @ 0x0807965c")
        except Exception as e:
            print("[warn] createFunction: %s" % e)
    
    # Add label
    sym_tbl = currentProgram.getSymbolTable()
    existing = sym_tbl.getSymbols(lo)
    names = [s.getName() for s in existing]
    if 'fn_eligible_order_to_charge_or_smash' not in names:
        sym_tbl.createLabel(lo, 'fn_eligible_order_to_charge_or_smash', SourceType.USER_DEFINED)
        print("[ok] label 0x0807965c -> fn_eligible_order_to_charge_or_smash")
    else:
        print("[ok] label exists")
    
    print("=== Fix B6 start DONE ===")

main()
