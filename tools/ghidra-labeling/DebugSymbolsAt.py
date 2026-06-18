# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# Debug: dump all symbols at key addresses

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

sym_tbl = currentProgram.getSymbolTable()

for addr_int in [0x09e3f094, 0x09e3f104, 0x0201c510, 0x0201d5b4]:
    a = _addr(addr_int)
    syms = list(sym_tbl.getSymbols(a))
    primary = sym_tbl.getPrimarySymbol(a)
    pname = primary.getName() if primary else "(none)"
    print("0x%08x: primary='%s'  all=%s" % (addr_int, pname, [s.getName() for s in syms]))

