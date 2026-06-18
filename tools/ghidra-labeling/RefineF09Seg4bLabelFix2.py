# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg4bLabelFix2.py -- Ensure branch-target labels are USER_DEFINED for GAS export
#   These exist as ANALYSIS labels but need USER_DEFINED to be exported by ExportRangeToGas.py

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

print("=== RefineF09Seg4bLabelFix2 ===")
for addr_val, label_name in LABELS:
    addr = _addr(addr_val)
    syms = list(sym_tbl.getSymbols(addr))
    found = False
    for sym in syms:
        print("  0x%08x: sym='%s' source=%s" % (addr_val, sym.getName(), sym.getSource()))
        if sym.getName() == label_name:
            found = True
            if str(sym.getSource()) != 'USER_DEFINED':
                try:
                    sym.setSource(SourceType.USER_DEFINED)
                    print("    -> promoted to USER_DEFINED")
                except Exception as e:
                    # setSource may not exist; try recreating as USER_DEFINED
                    try:
                        sym_tbl.createLabel(addr, label_name, SourceType.USER_DEFINED)
                        print("    -> created USER_DEFINED copy")
                    except Exception as e2:
                        print("    [WARN] could not promote: %s" % e2)
            else:
                print("    -> already USER_DEFINED")
    if not found:
        print("  0x%08x: label %s NOT FOUND -- creating" % (addr_val, label_name))
        try:
            sym_tbl.createLabel(addr, label_name, SourceType.USER_DEFINED)
            print("  -> created")
        except Exception as e:
            print("  [WARN] createLabel: %s" % e)

print("=== RefineF09Seg4bLabelFix2 DONE ===")
