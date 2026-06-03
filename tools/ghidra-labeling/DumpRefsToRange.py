# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DumpRefsToRange.py — dump 指向 [LO, HI) 的所有引用 (权威, 避免暴力指针扫的假阳性)
# 输出每条: to_addr <- from_addr (from_func)
# Usage: tools\asm-regen\ghidra-run-script.bat DumpRefsToRange.py 0800dd90 08013510

from ghidra.program.model.address import AddressSet

args = list(getScriptArgs())
LO = int(args[0], 16) if len(args) > 0 else 0x0800dd90
HI = int(args[1], 16) if len(args) > 1 else 0x08013510


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    rm = currentProgram.getReferenceManager()
    fm = currentProgram.getFunctionManager()
    aset = AddressSet(_addr(LO), _addr(HI - 1))
    it = rm.getReferenceDestinationIterator(aset, True)
    rows = []
    while it.hasNext():
        to = it.next()
        for r in rm.getReferencesTo(to):
            fa = r.getFromAddress()
            fn = fm.getFunctionContaining(fa)
            fn_name = fn.getName() if fn is not None else "?"
            rows.append((to.getOffset(), fa.getOffset(), fn_name, r.getReferenceType().toString()))
    rows.sort()
    print("=== refs into [0x%08x, 0x%08x): %d ===" % (LO, HI, len(rows)))
    for to, fa, fn, rt in rows:
        print("  0x%08x <- 0x%08x  %-45s %s" % (to, fa, fn, rt))


main()
