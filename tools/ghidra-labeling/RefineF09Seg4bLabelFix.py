# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bLabelFix.py -- Add missing branch-target labels inside B6/B7 blocks
#   LAB_08072486 - branch target inside last_turn_sub_2444 (B6)
#   LAB_0807252a - branch target inside last_turn_sub_24b4 (B6)
#   LAB_080726e6 - branch target inside fn_eligible_last_turn / B7 stubs (shared exit)
#   LAB_080726e8 - branch target inside B7 stubs (shared exit at fn_eligible_vampire_lord_lady_26f4)

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

print("=== RefineF09Seg4bLabelFix ===")
for addr_val, label_name in LABELS:
    addr = _addr(addr_val)
    existing = [s.getName() for s in sym_tbl.getSymbols(addr)]
    if label_name not in existing:
        try:
            sym_tbl.createLabel(addr, label_name, SourceType.USER_DEFINED)
            print("[LABEL] %s @ 0x%08x created" % (label_name, addr_val))
        except Exception as e:
            print("[WARN] createLabel %s: %s" % (label_name, e))
    else:
        print("[LABEL] %s already present" % label_name)
print("=== RefineF09Seg4bLabelFix DONE ===")
