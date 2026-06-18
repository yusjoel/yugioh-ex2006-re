# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bPoolFix.py -- Fix remaining pool words in B7/B8 that caused GAS errors
#   DAT_08072618 = 0x00001d6c  (LP offset, ldr in vampire_sub_25e8)
#   DAT_0807261c = 0x00001d70  (LP offset, ldr in vampire_sub_25e8)
#   DAT_08072834 = 0x00001daa  (LP_CARD_TRACK_NEXT_OFF, ldr in equip_zone_sub_2804)

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.util import CodeUnitInsertionException
from java.math import BigInteger

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol=None):
    pa = _addr(pool_addr)
    try:
        clearListing(pa, _addr(pool_addr + 7))
    except Exception as e:
        print("[WARN] clearListing pool @ 0x%08x: %s" % (pool_addr, e))
    try:
        d = listing.createData(pa, DWordDataType.dataType)
        if d is not None:
            print("[POOL] DWord @ 0x%08x (%s)" % (pool_addr, pool_label))
        else:
            print("[WARN] createData None @ 0x%08x" % pool_addr)
    except CodeUnitInsertionException as e:
        try:
            clearListing(pa, _addr(pool_addr + 11))
            d2 = listing.createData(pa, DWordDataType.dataType)
            if d2 is not None:
                print("[POOL] DWord @ 0x%08x (%s) [retry ok]" % (pool_addr, pool_label))
            else:
                print("[WARN] retry None @ 0x%08x" % pool_addr)
        except Exception as e2:
            print("[WARN] failed even after retry @ 0x%08x: %s" % (pool_addr, e2))
    except Exception as e:
        print("[WARN] unexpected @ 0x%08x: %s" % (pool_addr, e))
    existing_p = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label not in existing_p:
        try:
            sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (pool_label, e))
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)

listing = currentProgram.getListing()
sym_tbl = currentProgram.getSymbolTable()

print("=== RefineF09Seg4bPoolFix ===")

EXTRA_POOLS = [
    # B7 vampire_sub_25e8 pool words missed in first pass
    (0x08072618, 'pool_b7_2618', '0x1d6c LP offset; ldr in vampire_sub_25e8'),
    (0x0807261c, 'pool_b7_261c', '0x1d70 LP offset; ldr in vampire_sub_25e8'),
    # B8 equip_zone_sub_2804 pool word missed in first pass
    (0x08072834, 'pool_b8_2834', 'LP_CARD_TRACK_NEXT_OFF=0x1daa; ldr in equip_zone_sub_2804'),
]

for pool_addr, pool_label, pool_eol in EXTRA_POOLS:
    force_dword(listing, sym_tbl, pool_addr, pool_label, pool_eol)

print("=== RefineF09Seg4bPoolFix DONE ===")
