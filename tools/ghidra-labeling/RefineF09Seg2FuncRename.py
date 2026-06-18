# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg2FuncRename.py -- Rename function at 0x08070900
#   Uses getFunctionContaining to find the function even if entry is offset.

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


def main():
    print("=== RefineF09Seg2FuncRename (DRY=%s) ===" % DRY)

    FUNC_ADDR = 0x08070900
    FUNC_NAME = 'check_zone_tile_count_and_set_summon_restriction_flag'

    func_a = _addr(FUNC_ADDR)
    fm = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()

    # Try getFunctionAt first
    fn = fm.getFunctionAt(func_a)
    if fn is None:
        # Try getFunctionContaining
        fn = fm.getFunctionContaining(func_a)
        if fn is not None:
            entry = fn.getEntryPoint()
            print("[INFO] getFunctionContaining: fn=%s entry=0x%s" % (fn.getName(), entry))
            if entry.getOffset() != FUNC_ADDR:
                print("[WARN] function entry 0x%s != expected 0x%08x -- skipping" % (entry, FUNC_ADDR))
                fn = None

    if fn is None:
        # Ensure USER label exists (will be picked up as function on export)
        existing = [s.getName() for s in sym_tbl.getSymbols(func_a)]
        print("[INFO] No function at 0x%08x. Labels: %s" % (FUNC_ADDR, existing))
        if FUNC_NAME not in existing:
            if DRY:
                print("[dry] Would createLabel %s @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
            else:
                sym_tbl.createLabel(func_a, FUNC_NAME, SourceType.USER_DEFINED)
                print("[LABEL] created %s @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
        else:
            print("[LABEL] %s already present @ 0x%08x" % (FUNC_NAME, FUNC_ADDR))
    else:
        old_name = fn.getName()
        if DRY:
            print("[dry] FUNC_RENAME 0x%08x: %s -> %s" % (FUNC_ADDR, old_name, FUNC_NAME))
        else:
            fn.setName(FUNC_NAME, SourceType.USER_DEFINED)
            print("[FUNC_RENAME] 0x%08x: %s -> %s" % (FUNC_ADDR, old_name, FUNC_NAME))

    print("=== RefineF09Seg2FuncRename DONE ===")


main()
