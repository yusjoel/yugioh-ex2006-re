# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg1Fix2.py -- remove wrong gDuelSceneBase label at 0x020233ac
# The first run of RefineF02Seg1Slots.py set REF(0x0802dedc -> 0x020233ac, 'gDuelSceneBase')
# which created a USER_DEFINED label 'gDuelSceneBase' at 0x020233ac.
# This causes the exporter to emit .word gDuelSceneBase (= 0x020233ac) instead of
# .word 0x020233ac. But gDuelSceneBase is at 0x02023360, so assembled value = 0x02023360 != 0x020233ac.
# Fix: remove the wrongly-placed gDuelSceneBase label at 0x020233ac.

from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit

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
    print("=== RefineF02Seg1Fix2 (DRY=%s) ===" % DRY)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    # 1. Remove wrongly-placed gDuelSceneBase label at 0x020233ac
    a_wrong = _addr(0x020233ac)
    for sym in sym_tbl.getSymbols(a_wrong):
        if sym.getName() == 'gDuelSceneBase':
            if DRY:
                print("[dry] REMOVE gDuelSceneBase @ 0x020233ac")
            else:
                sym.delete()
                print("[REM] gDuelSceneBase @ 0x020233ac deleted")

    # 2. Remove any DATA ref from slot 0x0802dedc to 0x020233ac
    sa = _addr(0x0802dedc)
    ta = _addr(0x020233ac)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            if DRY:
                print("[dry] REMOVE_REF 0x0802dedc -> 0x020233ac")
            else:
                ref_mgr.delete(ref)
                print("[REM_REF] 0x0802dedc -> 0x020233ac")

    # 3. Also remove the slot label 'init_opp_card_display_vram_aob_ctx_sub' at 0x0802dedc
    #    since the RENAME_SLOT in the updated script will re-add it
    #    (keep it - rename_slot won't duplicate)

    # 4. Verify gDuelSceneBase still at 0x02023360
    a_correct = _addr(0x02023360)
    names = [s.getName() for s in sym_tbl.getSymbols(a_correct)]
    print("  gDuelSceneBase @ 0x02023360: labels=%s" % names)

    print("=== RefineF02Seg1Fix2 DONE ===")

main()
