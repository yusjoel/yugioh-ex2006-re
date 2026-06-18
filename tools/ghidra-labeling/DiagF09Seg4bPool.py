# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DiagF09Seg4bPool.py -- Diagnose pool issue at B6 area

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def diag_addr(addr_val):
    pa = _addr(addr_val)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(pa)
    cu_containing = listing.getCodeUnitContaining(pa)
    print("  0x%08x: cu=%s  cu_containing=%s" % (
        addr_val,
        cu.getMnemonicString() if cu else 'None',
        ('%s @0x%s' % (cu_containing.getMnemonicString(), cu_containing.getAddress())) if cu_containing else 'None'
    ))

print("=== B6 pool diagnostic ===")
# Check addresses that may be in the pool area
for a in [0x72478, 0x7247c, 0x724a8, 0x72500, 0x72508, 0x72530, 0x72574, 0x72578]:
    diag_addr(a)

print()
print("=== B6 range code units from 0x72444 to 0x7257c ===")
listing = currentProgram.getListing()
a_lo = _addr(0x08072444)
a_hi = _addr(0x0807257c)
cuit = listing.getCodeUnits(a_lo, a_hi, True)
count = 0
while cuit.hasNext() and count < 50:
    cu = cuit.next()
    print("  0x%s: %s" % (cu.getAddress(), cu.getMnemonicString()))
    count += 1
print("(shown %d code units)" % count)
