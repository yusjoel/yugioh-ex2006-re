# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# _CheckB9Disasm.py -- check B9 disasm result

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

listing = currentProgram.getListing()

# Check instructions in B9 code range (0x08073fe0..0x0807400b)
lo = _addr(0x08073fe0)
hi = _addr(0x0807400b)
n = 0
inst = listing.getInstructionAt(lo)
while inst is not None and inst.getAddress().compareTo(hi) <= 0:
    n += 1
    inst = listing.getInstructionAfter(inst.getAddress())
print("B9 code range 0x08073fe0..0x0807400b: %d instructions" % n)

# Also check pad byte at 0x08073fde
a_pad = _addr(0x08073fde)
cu_pad = listing.getCodeUnitAt(a_pad)
print("0x08073fde: %s" % (cu_pad,))

# Check instruction at 0x08073fe0
inst_start = listing.getInstructionAt(lo)
print("First instruction at 0x08073fe0: %s" % (inst_start,))

# Check data items at pool
a_pool1 = _addr(0x08074004)
a_pool2 = _addr(0x08074008)
cu1 = listing.getDataAt(a_pool1)
cu2 = listing.getDataAt(a_pool2)
print("Pool @0x08074004: %s" % (cu1,))
print("Pool @0x08074008: %s" % (cu2,))
