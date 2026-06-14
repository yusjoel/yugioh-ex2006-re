# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Header.py -- Fix CJK mojibake in file header comment for asm/08
# The file header line 2 'neo daedalus 资格...' is an EOL comment
# at the first instruction of asm/08 (0x080643e0).
# However the _rewrite_file_header in RefineF08Seg1Slots.py found it "already ASCII".
# This script checks the actual comment content and overwrites with ASCII if needed.

from ghidra.program.model.listing import CodeUnit

ASCII_TEXT = 'neo daedalus eligibility + equip OAM write + zone tile count'

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

# Check the code unit BEFORE 0x080643e0 (the last instruction of previous section)
# and AT 0x080643e0
for check_addr in [0x080643dc, 0x080643de, 0x080643e0]:
    a = _addr(check_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[INFO] 0x%08x: no code unit" % check_addr)
        continue
    eol = cu.getComment(CodeUnit.EOL_COMMENT)
    plate = cu.getComment(CodeUnit.PLATE_COMMENT)
    if eol:
        bad = any(ord(ch) > 127 for ch in eol)
        print("[INFO] 0x%08x: EOL (has_cjk=%s) first60='%s'" % (
            check_addr, bad, eol[:60].encode('ascii', errors='replace').decode()))
        if bad:
            cu.setComment(CodeUnit.EOL_COMMENT, ASCII_TEXT)
            print("[FIX ] 0x%08x: rewrote CJK EOL -> ASCII" % check_addr)
    else:
        print("[INFO] 0x%08x: no EOL" % check_addr)
    if plate:
        bad = any(ord(ch) > 127 for ch in plate)
        print("[INFO] 0x%08x: PLATE (has_cjk=%s) first60='%s'" % (
            check_addr, bad, plate[:60].encode('ascii', errors='replace').decode()))

print("Done")
