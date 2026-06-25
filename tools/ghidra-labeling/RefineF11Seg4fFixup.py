# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg4fFixup.py -- f11 Seg-4f fixup: missed fn19 pool stride slot 0x0808c4a0
#
# The disasm script missed creating a DWord at 0x0808c4a0 (fn19 pool, PLAYER_BLOCK_STRIDE=0x868).
# The slot was referenced by LDR at 0x0808c468 but not included in POOL_DWORDS.
# Ghidra left it as .byte -- fix: createDWord + apply STRIDE equate.
#
# NOTE: All text is pure ASCII. Ghidra Jython mojibake prevention.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check(slot_addr, expected_val, name='?'):
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(_addr(slot_addr)) & 0xFFFFFFFF
        if actual != (expected_val & 0xFFFFFFFF):
            print("FAIL value @0x%08x %s: expected=0x%08x actual=0x%08x" % (
                slot_addr, name, expected_val & 0xFFFFFFFF, actual))
            return False
    except Exception as e:
        print("FAIL read @0x%08x %s: %s" % (slot_addr, name, e))
        return False
    return True


def main():
    slot_addr = 0x0808c4a0
    value = 0x00000868
    eq_name = 'PLAYER_BLOCK_STRIDE'
    slot_label = 'stride_8c4a0'

    if not _check(slot_addr, value, eq_name):
        return

    if DRY:
        print("[dry] createDWord + EQ 0x%08x  %s  label=%s" % (slot_addr, eq_name, slot_label))
        return

    a = _addr(slot_addr)

    # Step 1: createDWord
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(slot_addr + 3), False)
        listing.createData(a, dt)
        print("[DW] createDWord 0x%08x ok" % slot_addr)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (slot_addr, e))

    # Step 2: apply EQ
    sym_tbl = currentProgram.getSymbolTable()
    eq_tbl = currentProgram.getEquateTable()
    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
    eq.addReference(a, 0)

    # Step 3: label
    names = [s.getName() for s in sym_tbl.getSymbols(a)]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    for s in sym_tbl.getSymbols(a):
        if s.getName() == slot_label:
            s.setPrimary()
            break

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))
    print("=== RefineF11Seg4fFixup DONE ===")


main()
