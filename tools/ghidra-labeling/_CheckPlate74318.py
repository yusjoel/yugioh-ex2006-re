# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# _CheckPlate74318.py -- check plate at 0x08074318

from ghidra.program.model.listing import CodeUnit

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

a = _addr(0x08074318)
listing = currentProgram.getListing()
cu = listing.getCodeUnitAt(a)
if cu is None:
    print("NO CODE UNIT at 0x08074318")
else:
    plate = cu.getComment(CodeUnit.PLATE_COMMENT)
    if plate is None:
        print("NO PLATE at 0x08074318")
    else:
        print("PLATE at 0x08074318 (first 300 chars):")
        print(plate[:300])
        print("---")
        print("Contains FUN_08071d64:", 'FUN_08071d64' in plate)
        print("Contains dispatch_spirit:", 'dispatch_spirit_monster_zone_sprite_by_card_id' in plate)
