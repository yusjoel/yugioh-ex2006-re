# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg2PoolFix.py -- fix literal pool slots at 0x08086424/28/2c
#
# After DisassembleF11Seg2.py ran, code at LAB_08086400 (within the disasm block)
# references a literal pool at 0x08086424 (outside block, in dispatch_equip_slot_state body).
# These 3 words were previously grouped as a .byte DAT_08086424 block.
# createDWord them individually to allow GAS ldr resolution.
#
# 0x08086424 = 0x0201c4e0 = gP1LifePoints
# 0x08086428 = 0x00001d68 = ELIGIB_SPRITE_CTRL_OFF
# 0x0808642c = 0x00001d6c = ELIGIB_ANIM_STATE_OFF

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
        print("[dry] createDWord 0x%08x label=%s" % (addr_int, label))
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
    print("[dword] 0x%08x" % addr_int)


def main():
    print("=== RefineF11Seg2PoolFix (DRY=%s) ===" % DRY)
    print("Fix literal pool at 0x08086424/28/2c used by LAB_08086400 code")

    _create_dword(0x08086424, 'gp1lp_pool_86424',
                  'gP1LifePoints=0x0201c4e0 (ewram.inc); literal pool for LAB_08086400')
    _create_dword(0x08086428, 'eligib_spr_ctrl_86428',
                  'ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc); literal pool for LAB_08086400')
    _create_dword(0x0808642c, 'eligib_anim_st_8642c',
                  'ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc); literal pool for LAB_08086400')

    print("=== RefineF11Seg2PoolFix DONE ===")


main()
