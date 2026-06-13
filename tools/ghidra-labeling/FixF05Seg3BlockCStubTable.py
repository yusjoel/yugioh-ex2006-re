# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF05Seg3BlockCStubTable.py -- Fix BlockC switch table and inline stub
#
# BlockC disasm left the switch table (0x0804b288..0x0804b2d3) and inline
# stub (0x0804b2d4..0x0804b2db) as a single ROM_INCBIN 0x4b288, 0x54.
#
# This script:
# 1. Creates DWORD data for the switch table entries (19 x 4B = 0x4c bytes)
#    - Labels them: dark_world_range_switch_table (first entry)
#    - Each entry points to either 0x0804b2d4 (return 1) or 0x0804b2d8 (return 0)
# 2. Disassembles the inline stub at 0x0804b2d4..0x0804b2db (8 bytes THUMB)
#    - This creates LAB_0804b2d4 (return-1 path) and LAB_0804b2d8 (return-0 path)
# 3. Creates labels: dark_world_range_case1_ret at 0x0804b2d4, LAB_0804b2d8 at 0x0804b2d8
#
# Pattern: The bhi instruction at 0x0804b272 branches to LAB_0804b2d8 (return 0).
# The switch table entries branch to LAB_0804b2d4 (return 1) or LAB_0804b2d8 (return 0).
#
# NOTE: The 0x0804b288 (dark_world_range_table_ptr) DWORD was already split in
#       FixF05Seg3SplitLiteralPools.py to hold value 0x0804b288 (ptr to switch table).
#       We don't need to redo that.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# Switch table: 19 entries x 4B at 0x0804b288..0x0804b2d3
SWITCH_TABLE_LO  = 0x0804b288
SWITCH_TABLE_HI  = 0x0804b2d3  # inclusive (last entry ends at 0x0804b2d3)
SWITCH_ENTRIES   = 19
SWITCH_ENTRY_SZ  = 4

# Each entry points to return-1 or return-0 stub
CASE1_ADDR = 0x0804b2d4  # return 1 (dark_world_range_case1_ret)
CASE0_ADDR = 0x0804b2d8  # return 0 (within inline stub)

# Inline stub: 0x0804b2d4..0x0804b2db (8 bytes)
STUB_LO = 0x0804b2d4
STUB_HI = 0x0804b2db  # inclusive

# Expected switch table entries (derived from proposal):
# Return-1 IDs -> case1_ret (0x0804b2d4): index 0,4,5,6,7,8,9,15,18 (9 entries)
# Return-0 IDs -> case0 (0x0804b2d8): index 1,2,3,10,11,12,13,14,16,17 (10 entries)
# Based on card_ids: 0x1961=Zure(1), 0x1962=BES Tetran(0), ..., 0x1973=Gateway(1)
SWITCH_TABLE_VALUES = [
    0x0804b2d4,  # index 0: 0x1961 Zure -> return 1
    0x0804b2d8,  # index 1: 0x1962 BES Tetran -> return 0
    0x0804b2d8,  # index 2: 0x1963 Nanobreaker -> return 0
    0x0804b2d8,  # index 3: 0x1964 Rapid-Fire Magician -> return 0
    0x0804b2d4,  # index 4: 0x1965 Beiige -> return 1
    0x0804b2d4,  # index 5: 0x1966 Broww -> return 1
    0x0804b2d4,  # index 6: 0x1967 Brron -> return 1
    0x0804b2d4,  # index 7: 0x1968 Sillva -> return 1
    0x0804b2d4,  # index 8: 0x1969 Goldd -> return 1
    0x0804b2d4,  # index 9: 0x196a Scarr -> return 1
    0x0804b2d8,  # index 10: 0x196b Familiar-Possessed -> return 0
    0x0804b2d8,  # index 11: 0x196c Familiar-Possessed -> return 0
    0x0804b2d8,  # index 12: 0x196d Familiar-Possessed -> return 0
    0x0804b2d8,  # index 13: 0x196e Familiar-Possessed -> return 0
    0x0804b2d8,  # index 14: 0x196f Pot of Avarice -> return 0
    0x0804b2d4,  # index 15: 0x1970 Dark World Lightning -> return 1
    0x0804b2d8,  # index 16: 0x1971 unassigned -> return 0
    0x0804b2d8,  # index 17: 0x1972 Boss Rush -> return 0
    0x0804b2d4,  # index 18: 0x1973 Gateway to Dark World -> return 1
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF05Seg3BlockCStubTable (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    rm      = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] Switch table 0x%08x..0x%08x (%d x 4B entries)" % (
            SWITCH_TABLE_LO, SWITCH_TABLE_HI, SWITCH_ENTRIES))
        print("[dry] Inline stub disasm 0x%08x..0x%08x (8B THUMB)" % (STUB_LO, STUB_HI))
        print("[dry] Labels: dark_world_range_case1_ret @ 0x%08x, dark_world_range_ret0 @ 0x%08x" % (
            CASE1_ADDR, CASE0_ADDR))
        return

    # --- 1. Disassemble inline stub first (0x0804b2d4..0x0804b2db) ---
    lo_stub = _addr(STUB_LO)
    hi_stub = _addr(STUB_HI)
    try:
        clearListing(lo_stub, hi_stub)
        print("[ok ] clearListing stub 0x%08x..0x%08x" % (STUB_LO, STUB_HI))
    except Exception as e:
        print("[warn] clearListing stub: %s" % e)

    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo_stub, hi_stub, BigInteger.ONE)
        print("[ok ] setTMode=THUMB stub 0x%08x..0x%08x" % (STUB_LO, STUB_HI))

    cmd = DisassembleCommand(lo_stub, AddressSet(lo_stub, hi_stub), True)
    if cmd.applyTo(currentProgram):
        print("[ok ] disasm stub 0x%08x..0x%08x" % (STUB_LO, STUB_HI))
    else:
        print("[warn] disasm stub: %s" % cmd.getStatusMsg())

    # --- 2. Label the two return paths ---
    # dark_world_range_case1_ret at 0x0804b2d4 (return-1 entry, movs r0,#1)
    try:
        sym_tbl.createLabel(_addr(CASE1_ADDR), 'dark_world_range_case1_ret', SourceType.USER_DEFINED)
        print("[ok ] label dark_world_range_case1_ret @ 0x%08x" % CASE1_ADDR)
    except Exception as e:
        print("[warn] label case1: %s" % e)

    # dark_world_range_ret0 at 0x0804b2d8 (return-0 entry, movs r0,#0)
    try:
        sym_tbl.createLabel(_addr(CASE0_ADDR), 'dark_world_range_ret0', SourceType.USER_DEFINED)
        print("[ok ] label dark_world_range_ret0 @ 0x%08x" % CASE0_ADDR)
    except Exception as e:
        print("[warn] label case0: %s" % e)

    # --- 3. Create DWORD data for switch table entries ---
    # First clear any existing listing in the switch table range
    lo_tbl = _addr(SWITCH_TABLE_LO)
    hi_tbl = _addr(SWITCH_TABLE_HI)
    try:
        clearListing(lo_tbl, hi_tbl)
        print("[ok ] clearListing switch_table 0x%08x..0x%08x" % (SWITCH_TABLE_LO, SWITCH_TABLE_HI))
    except Exception as e:
        print("[warn] clearListing switch_table: %s" % e)

    # Create individual DWORD entries for each table slot
    for i in range(SWITCH_ENTRIES):
        slot_addr = SWITCH_TABLE_LO + i * SWITCH_ENTRY_SZ
        a = _addr(slot_addr)
        try:
            listing.createData(a, DWordDataType.dataType)
        except Exception as e:
            print("[warn] createDWord @ 0x%08x: %s" % (slot_addr, e))

    print("[ok ] created %d DWORD entries in switch table" % SWITCH_ENTRIES)

    # --- 4. Label the switch table base ---
    try:
        sym_tbl.createLabel(_addr(SWITCH_TABLE_LO), 'dark_world_range_switch_table', SourceType.USER_DEFINED)
        print("[ok ] label dark_world_range_switch_table @ 0x%08x" % SWITCH_TABLE_LO)
    except Exception as e:
        print("[warn] label switch_table: %s" % e)

    # --- 5. Verify a few table entries ---
    for i, expected in enumerate(SWITCH_TABLE_VALUES[:5]):  # spot check first 5
        slot_addr = SWITCH_TABLE_LO + i * SWITCH_ENTRY_SZ
        d = getDataAt(_addr(slot_addr))
        if d is not None and d.getLength() == 4:
            try:
                dv = d.getValue()
                iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
                if iv != expected:
                    print("[WARN] tbl[%d]=0x%08x expected=0x%08x" % (i, iv, expected))
                else:
                    print("[ok ] tbl[%d]=0x%08x ok" % (i, iv))
            except Exception as e:
                print("[warn] verify tbl[%d]: %s" % (i, e))

    print("=== FixF05Seg3BlockCStubTable DONE ===")


main()
