# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4aPoolFix.py -- F09 Seg-4a literal pool DWord fixes
#
# Fixes GAS "invalid offset, value too big" errors from pool words
# exported as .byte sequences by Ghidra after disasm.
#
# Pool groups:
#   1. B2 sub_1b64 pool @ 0x08071b90..0x08071b9b
#      0x08071b90: DAT_08071b90 (gP1LifePoints = 0x0201c4e0)
#      0x08071b94: DAT_08071b94 (LP offset 0x1ce8? - check below)
#      0x08071b98: DAT_08071b98 (PLAYER_BLOCK_STRIDE = 0x868)
#
#   2. B4 sub_2088 pool @ 0x080720a4..0x080720ab
#      0x080720a4: DAT_080720a4
#      0x080720a8: DAT_080720a8
#
# NOTE: All text is pure ASCII.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_230753-pre-F09Seg4a

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
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


def force_dword(pool_addr, pool_label, pool_eol):
    """Force a DWord data type at pool_addr with label and EOL."""
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
        print("       DWord created")
    else:
        print("[WARN] createData failed @ 0x%08x" % pool_addr)
    existing = [s.getName() for s in sym_tbl.getSymbols(pa)]
    if pool_label not in existing:
        sym_tbl.createLabel(pa, pool_label, SourceType.USER_DEFINED)
        print("       label: %s" % pool_label)
    if pool_eol:
        cu = listing.getCodeUnitAt(pa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, pool_eol)


def main():
    print("=== RefineF09Seg4aPoolFix (DRY=%s) ===" % DRY)

    # Read actual ROM values at pool addresses for verification
    mem = currentProgram.getMemory()

    POOLS = [
        # B2 sub_1b64 literal pool @ 0x08071b90..0x08071b9b
        (0x08071b90, 'pool_1b90', 'literal pool field_spell_sub_1b64 word 0'),
        (0x08071b94, 'pool_1b94', 'literal pool field_spell_sub_1b64 word 1'),
        (0x08071b98, 'pool_1b98', 'literal pool field_spell_sub_1b64 word 2'),
        # B4 sub_2088 literal pool @ 0x080720a4..0x080720ab
        (0x080720a4, 'pool_20a4', 'literal pool field_spell_sub_2088 word 0'),
        (0x080720a8, 'pool_20a8', 'literal pool field_spell_sub_2088 word 1'),
    ]

    if DRY:
        print("[dry] Would fix %d pool DWords" % len(POOLS))
        for pa, pl, pe in POOLS:
            print("  0x%08x  %s" % (pa, pl))
    else:
        for pool_addr, pool_label, pool_eol in POOLS:
            force_dword(pool_addr, pool_label, pool_eol)

    print("\n=== RefineF09Seg4aPoolFix DONE ===")
    print("  Fixed %d pool DWords" % len(POOLS))


main()
