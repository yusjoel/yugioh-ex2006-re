# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DebugF08Plates.py -- Debug: check plate/EOL comments at function entry addresses

from ghidra.program.model.listing import CodeUnit

ADDRS = [
    0x08064660,
    0x08064760,
    0x0806505c,
    0x080650bc,
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

for a_val in ADDRS:
    a = _addr(a_val)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[DEBUG] 0x%08x: NO CODE UNIT" % a_val)
        continue
    plate = cu.getComment(CodeUnit.PLATE_COMMENT)
    eol = cu.getComment(CodeUnit.EOL_COMMENT)
    pre = cu.getComment(CodeUnit.PRE_COMMENT)
    if plate:
        idx = plate.find("FUN_")
        print("[DEBUG] 0x%08x: plate(len=%d, has_FUN=%s)" % (a_val, len(plate), idx >= 0))
    else:
        print("[DEBUG] 0x%08x: plate=None eol=%s pre=%s" % (
            a_val,
            repr(eol[:40]) if eol else None,
            repr(pre[:40]) if pre else None,
        ))
print("Debug done")
