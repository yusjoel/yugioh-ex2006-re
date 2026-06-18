# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bLabelFix3.py -- Create USER_DEFINED copies of DEFAULT branch-target labels
#   DEFAULT source labels from disasm are not exported; create USER_DEFINED versions.

from ghidra.program.model.symbol import SourceType

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

sym_tbl = currentProgram.getSymbolTable()

LABELS = [
    (0x08072486, 'LAB_08072486'),
    (0x0807252a, 'LAB_0807252a'),
    (0x080726e6, 'LAB_080726e6'),
    (0x080726e8, 'LAB_080726e8'),
]

print("=== RefineF09Seg4bLabelFix3 ===")
for addr_val, label_name in LABELS:
    addr = _addr(addr_val)
    # Check if USER_DEFINED version already exists
    syms = list(sym_tbl.getSymbols(addr))
    user_exists = any(sym.getName() == label_name and str(sym.getSource()) == 'USER_DEFINED' for sym in syms)
    if user_exists:
        print("[OK] %s @ 0x%08x already USER_DEFINED" % (label_name, addr_val))
        continue
    # Create a USER_DEFINED label (may coexist with DEFAULT)
    try:
        sym_tbl.createLabel(addr, label_name, SourceType.USER_DEFINED)
        print("[LABEL] %s @ 0x%08x created USER_DEFINED" % (label_name, addr_val))
    except Exception as e:
        print("[WARN] createLabel %s: %s" % (label_name, e))
print("=== RefineF09Seg4bLabelFix3 DONE ===")
