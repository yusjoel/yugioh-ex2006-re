# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF01Seg8Block2Pools.py -- f01 Seg-8 Block2 literal pool EQ/RENAME
#   After DisassembleF01Seg8Blocks.py guards literal pools as DWORDs,
#   apply equates and renames to the newly-created DWORD entries.
#   6 stubs x 4 slots = 24 literal pool slots total.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass

# EQ_SLOTS for block2 literal pools (EWRAM_BASE + GSETTINGS_OFFSET)
EQ_SLOTS = [
    # stub b0 @ 0x080258f0 literal pool
    (0x0802591c, 0x02000000, 'EWRAM_BASE',      'fun_080258f0_b0_ewram_base'),
    (0x08025920, 0x00006c2c, 'GSETTINGS_OFFSET', 'fun_080258f0_b0_gsettings_off'),
    # stub b1 @ 0x0802594c literal pool
    (0x08025978, 0x02000000, 'EWRAM_BASE',      'fun_0802594c_b1_ewram_base'),
    (0x0802597c, 0x00006c2c, 'GSETTINGS_OFFSET', 'fun_0802594c_b1_gsettings_off'),
    # stub b2 @ 0x080259a8 literal pool
    (0x080259d0, 0x02000000, 'EWRAM_BASE',      'fun_080259a8_b2_ewram_base'),
    (0x080259d4, 0x00006c2c, 'GSETTINGS_OFFSET', 'fun_080259a8_b2_gsettings_off'),
    # stub b3 @ 0x08025a08 literal pool
    (0x08025a30, 0x02000000, 'EWRAM_BASE',      'fun_08025a08_b3_ewram_base'),
    (0x08025a34, 0x00006c2c, 'GSETTINGS_OFFSET', 'fun_08025a08_b3_gsettings_off'),
    # stub b4 @ 0x08025a68 literal pool
    (0x08025a90, 0x02000000, 'EWRAM_BASE',      'fun_08025a68_b4_ewram_base'),
    (0x08025a94, 0x00006c2c, 'GSETTINGS_OFFSET', 'fun_08025a68_b4_gsettings_off'),
    # stub b5 @ 0x08025ac8 literal pool
    (0x08025af0, 0x02000000, 'EWRAM_BASE',      'fun_08025ac8_b5_ewram_base'),
    (0x08025af4, 0x00006c2c, 'GSETTINGS_OFFSET', 'fun_08025ac8_b5_gsettings_off'),
]

# RENAME_SLOTS for font5_base/off in block2 literal pools
RENAME_SLOTS = [
    # stub b0
    (0x08025924, 'rcs_blk2_b0_font5_base', '0x09dbe804: block2 stub 0 font5 base'),
    (0x08025928, 'rcs_blk2_b0_font5_off',  '0x0003ab14: block2 stub 0 font5 off'),
    # stub b1
    (0x08025980, 'rcs_blk2_b1_font5_base', '0x09dbe816'),
    (0x08025984, 'rcs_blk2_b1_font5_off',  '0x0003ab1c'),
    # stub b2
    (0x080259d8, 'rcs_blk2_b2_font5_base', '0x09dbe826'),
    (0x080259dc, 'rcs_blk2_b2_font5_off',  '0x0003ab24'),
    # stub b3
    (0x08025a38, 'rcs_blk2_b3_font5_base', '0x09dbe836'),
    (0x08025a3c, 'rcs_blk2_b3_font5_off',  '0x0003ab28'),
    # stub b4
    (0x08025a98, 'rcs_blk2_b4_font5_base', '0x09dbe84a'),
    (0x08025a9c, 'rcs_blk2_b4_font5_off',  '0x0003ab2e'),
    # stub b5
    (0x08025af8, 'rcs_blk2_b5_font5_base', '0x09dbe85c'),
    (0x08025afc, 'rcs_blk2_b5_font5_off',  '0x0003ab30'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_int, want):
    d = getDataAt(_addr(slot_int))
    if d is None or d.getLength() != 4:
        return False, "no 4B data"
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (want & 0xffffffff):
        return False, "value mismatch got=0x%x want=0x%x" % (iv, want)
    return True, None


def main():
    print("=== RefineF01Seg8Block2Pools (DRY=%s) ===" % DRY)
    et = currentProgram.getEquateTable()
    listing = currentProgram.getListing()
    nA = nC = 0

    for slot_int, value, cname, label in EQ_SLOTS:
        ok, err = _check(slot_int, value)
        if not ok:
            print("[A FAIL] 0x%08x: %s" % (slot_int, err))
            continue
        if DRY:
            print("[A dry] 0x%08x equate %s rename %s" % (slot_int, cname, label))
            nA += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        eq = et.getEquate(cname)
        if eq is None:
            eq = et.createEquate(cname, value)
        eq.addReference(_addr(slot_int), 0)
        print("[A ok] 0x%08x -> %s (%s)" % (slot_int, label, cname))
        nA += 1

    for slot_int, label, eol in RENAME_SLOTS:
        d = getDataAt(_addr(slot_int))
        if d is None or d.getLength() != 4:
            print("[C FAIL] no 4B data @ 0x%08x" % slot_int)
            continue
        if DRY:
            print("[C dry] 0x%08x rename %s" % (slot_int, label))
            nC += 1
            continue
        createLabel(_addr(slot_int), label, True, SourceType.USER_DEFINED)
        if eol:
            listing.getCodeUnitAt(_addr(slot_int)).setComment(CodeUnit.EOL_COMMENT, eol)
        print("[C ok] 0x%08x -> %s" % (slot_int, label))
        nC += 1

    print("[done] A=%d C=%d (DRY=%s)" % (nA, nC, DRY))


main()
