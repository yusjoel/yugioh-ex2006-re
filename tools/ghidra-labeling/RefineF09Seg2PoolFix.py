# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2PoolFix.py -- Fix literal pool for check_zone_tile_count_and_set_summon_restriction_flag
#   After clearListing+disasm of 0x08070900..0x080709ff, the literal pool words
#   at 0x08070974 (PLAYER_BLOCK_STRIDE=0x868) and 0x08070978 (gDuelFieldSlots=0x0201c510)
#   need to be re-created as DWord data with their labels.
#   The 2-byte pad at 0x08070972 needs to be .zero 0x2.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, ByteDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== RefineF09Seg2PoolFix (DRY=%s) ===" % DRY)

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()

    # Pool words for check_zone_tile_count_and_set_summon_restriction_flag
    # 0x08070970: bx r1  (epilogue)
    # 0x08070972: 0x00,0x00 (2-byte pad)
    # 0x08070974: PLAYER_BLOCK_STRIDE=0x00000868
    # 0x08070978: gDuelFieldSlots=0x0201c510

    PAD_ADDR    = 0x08070972
    STRIDE_ADDR = 0x08070974
    SLOTS_ADDR  = 0x08070978

    entries = [
        (STRIDE_ADDR, 0x00000868, 'player_stride_0974',
         'PLAYER_BLOCK_STRIDE=0x868; literal pool for check_zone_tile_count_and_set_summon_restriction_flag'),
        (SLOTS_ADDR,  0x0201c510, 'gduel_slots_0978',
         'gDuelFieldSlots=0x0201c510; literal pool for check_zone_tile_count_and_set_summon_restriction_flag'),
    ]

    if DRY:
        print("[dry] Would clearListing + createData (2 x DWord) at 0x%08x, 0x%08x" % (STRIDE_ADDR, SLOTS_ADDR))
        for addr, val, lbl, eol in entries:
            print("[dry]   0x%08x  0x%08x  label=%s" % (addr, val, lbl))
        print("=== RefineF09Seg2PoolFix DRY DONE ===")
        return

    # Clear the pool area to remove any existing code units
    pool_a = _addr(STRIDE_ADDR)
    pool_end_a = _addr(SLOTS_ADDR + 3)
    try:
        clearListing(pool_a, pool_end_a)
        print("[1] clearListing 0x%08x..0x%08x done" % (STRIDE_ADDR, SLOTS_ADDR + 3))
    except Exception as e:
        print("[WARN] clearListing: %s" % e)

    # Create DWord entries
    for addr_int, expected_val, label, eol in entries:
        a = _addr(addr_int)

        # Verify value
        mem = currentProgram.getMemory()
        try:
            actual = mem.getInt(a) & 0xFFFFFFFF
        except Exception as e:
            print("[FAIL] read 0x%08x: %s" % (addr_int, e))
            continue
        if actual != (expected_val & 0xFFFFFFFF):
            print("[FAIL] value mismatch @ 0x%08x: got 0x%08x, expected 0x%08x" % (
                addr_int, actual, expected_val & 0xFFFFFFFF))
            continue

        # Create DWord
        d = listing.createData(a, DWordDataType.dataType)
        if d is not None:
            print("[DW] DWord created @ 0x%08x" % addr_int)
        else:
            print("[WARN] createData failed @ 0x%08x" % addr_int)

        # Create label
        existing = [s.getName() for s in sym_tbl.getSymbols(a)]
        if label not in existing:
            sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
            print("[LBL] label %s @ 0x%08x" % (label, addr_int))
        else:
            print("[LBL] label %s already present @ 0x%08x" % (label, addr_int))

        # EOL comment
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
            print("[EOL] set @ 0x%08x" % addr_int)
        else:
            print("[WARN] no CodeUnit for EOL @ 0x%08x" % addr_int)

    print("\n=== RefineF09Seg2PoolFix DONE ===")


main()
