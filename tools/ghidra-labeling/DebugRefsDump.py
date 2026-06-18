# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# Debug: dump all refs from key slots

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def dump_refs(slot_int):
    ref_mgr = currentProgram.getReferenceManager()
    a_slot = _addr(slot_int)
    refs = list(ref_mgr.getReferencesFrom(a_slot))
    sym_tbl = currentProgram.getSymbolTable()
    print("=== refs from 0x%08x (%d refs) ===" % (slot_int, len(refs)))
    for r in refs:
        to = r.getToAddress()
        prim = r.isPrimary()
        syms = list(sym_tbl.getSymbols(to))
        primary_sym = sym_tbl.getPrimarySymbol(to)
        psym_name = primary_sym.getName() if primary_sym else "(none)"
        all_names = [s.getName() for s in syms]
        print("  -> 0x%08x  primary=%s  primarySym=%s  allSyms=%s  type=%s  src=%s" % (
            to.getOffset(), prim, psym_name, all_names, r.getReferenceType(), r.getSource()))

for slot_int in [0x08040ab4, 0x080478f0, 0x0805b888]:
    dump_refs(slot_int)

