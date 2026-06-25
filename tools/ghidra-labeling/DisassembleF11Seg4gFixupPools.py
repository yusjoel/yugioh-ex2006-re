# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg4gFixupPools.py -- fixup literal pool DWords for helper stubs in asm/12
# that were disassembled by the Seg-4g disasm pass (fn20 BL targets at 0x08097104/d4/e4/f4)
#
# Problem: Ghidra exported the pool data of SUB_080970d4, SUB_080970e4, SUB_080970e4 as
# .byte sequences without labels, causing build errors:
#   "invalid offset, value too big" for DAT_080970e0, DAT_080970fc, DAT_08097100
#
# Fix: force-createDWord the 3 pool slots so Ghidra emits them with labels.
#
# Pool slots to fix:
#   0x080970e0  (pool for SUB_080970d4: ldr r1,[PC+0x8] @0x080970d4+4+8=0x080970e0)
#   0x080970fc  (pool for SUB_080970e4: ldr r1,[PC+0x14] @0x080970e4+4+0x14=0x080970fc)
#   0x08097100  (pool for SUB_080970e4: ldr r0,[PC+0x10] @0x080970ee+4+0x10=0x08097100)
#
# All EOL/plate text is pure ASCII. Ghidra Jython mojibake prevention.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _create_dword(addr_int, label=None, eol=None):
    if DRY:
        print("[dry] createDWord 0x%08x  label=%s" % (addr_int, label or 'none'))
        return
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sym_table = currentProgram.getSymbolTable()
        try:
            sym_table.createLabel(a, label, SourceType.USER_DEFINED)
            for s in sym_table.getSymbols(a):
                if s.getName() == label:
                    s.setPrimary()
                    break
        except Exception as e:
            print("[warn] label dword 0x%08x %s: %s" % (addr_int, label, e))
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[dword] 0x%08x  label=%s" % (addr_int, label or 'none'))


# The 2-byte pad before DAT_080970e0 at 0x080970de - just create dword including pad
# Actually these pools are 4-byte aligned, so:
# 0x080970de: 2-byte pad, 0x080970e0: 4-byte pool word (target for DAT_080970e0)
# 0x080970fa: 2-byte pad, 0x080970fc: 4-byte pool word, 0x08097100: 4-byte pool word

POOL_DWORDS = [
    (0x080970e0, None),   # DAT_080970e0: pool for SUB_080970d4 (value=0x09e47560)
    (0x080970fc, None),   # DAT_080970fc: pool1 for SUB_080970e4 (value=0x09e47560)
    (0x08097100, None),   # DAT_08097100: pool2 for SUB_080970e4 (XOR key)
]


def main():
    if DRY:
        print("DRY RUN -- DisassembleF11Seg4gFixupPools:")
        for addr, lbl in POOL_DWORDS:
            _create_dword(addr, lbl)
        return

    print("=== DisassembleF11Seg4gFixupPools ===")
    for addr, lbl in POOL_DWORDS:
        _create_dword(addr, lbl)
    print("=== DisassembleF11Seg4gFixupPools DONE ===")
    print("  %d pool DWords fixed" % len(POOL_DWORDS))


main()
