# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4aPoolFix2.py -- F09 Seg-4a second pass pool fixes
#
# Fixes remaining GAS error after PoolFix.py:
#   asm/09_equip_lp_display.s:6973: Error: invalid offset, value too big (0xFFFFFFFC)
#
# Root cause: DAT_08071bb8 referenced by ldr r5, DAT_08071bb8 in field_spell_sub_1ba0
# but the bytes 0x08071bb6..0x08071bbb are exported as a .byte sequence.
# Need to force:
#   0x08071b9c: DWord (dead bytes after b LAB_08071bd2 branch)
#   0x08071bb8: DWord = 0x0201e1c8 (gDuelCardCtxBase? check below)
#   Also 0x08071bb6: 2-byte align pad (create Word or leave as .byte - but split the 6-byte range)
#
# NOTE: All text is pure ASCII.

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType, WordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def force_dword(pool_addr, pool_label, pool_eol):
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    pa = _addr(pool_addr)
    print("[POOL] createDWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
    try:
        clearListing(pa, _addr(pool_addr + 3))
    except Exception as e:
        print("[WARN] clearListing @ 0x%08x: %s" % (pool_addr, e))
    d = listing.createData(pa, DWordDataType.dataType)
    if d is not None:
        print("       DWord created ok")
    else:
        print("[WARN] createData failed @ 0x%08x" % pool_addr)
    existing = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label and pool_label not in existing:
        sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        print("       label: %s" % pool_label)
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)


def force_word(pool_addr, pool_label, pool_eol):
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    pa = _addr(pool_addr)
    print("[PAD]  createWord @ 0x%08x  label=%s" % (pool_addr, pool_label))
    try:
        clearListing(pa, _addr(pool_addr + 1))
    except Exception as e:
        print("[WARN] clearListing @ 0x%08x: %s" % (pool_addr, e))
    d = listing.createData(pa, WordDataType.dataType)
    if d is not None:
        print("       Word created ok")
    else:
        print("[WARN] createData failed @ 0x%08x" % pool_addr)
    existing = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label and pool_label not in existing:
        sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)


def main():
    print("=== RefineF09Seg4aPoolFix2 (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] Would fix:")
        print("  0x08071b9c DWord (dead bytes after b LAB_08071bd2)")
        print("  0x08071bb6 Word (2-byte alignment pad)")
        print("  0x08071bb8 DWord (DAT_08071bb8 = 0x0201e1c8)")
        return

    # 1. 0x08071b9c: 4 dead bytes after b LAB_08071bd2; force DWord
    force_dword(0x08071b9c, 'dead_1b9c', 'dead bytes after b LAB_08071bd2')

    # 2. 0x08071bb6: 2-byte alignment pad; force Word to split the 6-byte .byte block
    force_word(0x08071bb6, 'pad_1bb6', '2-byte alignment pad before DAT_08071bb8')

    # 3. 0x08071bb8: DAT_08071bb8 = 0x0201e1c8; force DWord
    force_dword(0x08071bb8, 'dat_08071bb8_pool', 'literal pool field_spell_sub_1ba0; value=0x0201e1c8')

    print("\n=== RefineF09Seg4aPoolFix2 DONE ===")


main()
