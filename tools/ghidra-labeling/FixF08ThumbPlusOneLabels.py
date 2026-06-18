# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08ThumbPlusOneLabels.py
#   Restore THUMB+1 entry-point labels for two function pointers in asm/08
#   that were dropped from the Ghidra .rep at some point during F09 Seg-1 work.
#
#   check_equip_activation_at_slot11 is at 0x08065990.
#   Its THUMB+1 value 0x08065991 is stored at 0x08065c50 and 0x08065c60.
#   Without the _1 label, ExportRangeToGas emits 'check_equip_activation_at_slot11'
#   (base addr = 0x08065990) giving wrong byte 0x90 instead of 0x91.
#
#   check_equip_slot_eligible_by_equip_type is at 0x08051318.
#   Its THUMB+1 value 0x08051319 is stored at 0x0806bb28.
#   Without the _1 label, export emits 0x18 instead of 0x19.

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

# (thumb_plus1_addr, label_name)
THUMB_PLUS1_LABELS = [
    (0x08065991, 'check_equip_activation_at_slot11_1'),
    (0x08051319, 'check_equip_slot_eligible_by_equip_type_1'),
]

print("=== FixF08ThumbPlusOneLabels.py DRY=%s ===" % DRY)

sym_tbl = currentProgram.getSymbolTable()
applied = 0
skipped = 0

for addr_val, lbl in THUMB_PLUS1_LABELS:
    a = _addr(addr_val)
    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
    if DRY:
        print("DRY: createLabel 0x%08x -> %s (existing: %s)" % (addr_val, lbl, existing))
        applied += 1
        continue
    if lbl in existing:
        print("[SKIP] 0x%08x %s already exists" % (addr_val, lbl))
        skipped += 1
        continue
    try:
        sym_tbl.createLabel(a, lbl, SourceType.USER_DEFINED)
        # Set as primary so ExportRangeToGas picks it as the label name
        for s in sym_tbl.getSymbols(a):
            if s.getName() == lbl:
                s.setPrimary()
                break
        print("[OK] createLabel 0x%08x -> %s" % (addr_val, lbl))
        applied += 1
    except Exception as e:
        print("[WARN] 0x%08x: %s" % (addr_val, str(e)))
        skipped += 1

print("=== DONE: applied=%d skipped=%d ===" % (applied, skipped))
