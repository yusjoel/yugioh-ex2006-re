# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg6ThumbPlusPtrLabels.py
# Creates _1 labels at THUMB+1 addresses for fn-ptr slots that GAS needs.
# These addresses fall inside THUMB code (odd address), so they can't be
# normal function labels. We create USER_DEFINED labels with the _1 suffix.
#
# Problem: REF_SLOTS in RefineF08Seg6Slots.py created labels named
# "check_zone_activation_ctx_match_cb+1" with a '+' char -- GAS can't use
# '+' in label names. The asm/08 export references the _1 variant instead.
#
# Fix: Create labels with _1 suffix at the THUMB+1 addresses.

from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (thumb_plus_one_addr, label_name)
THUMB_PLUS_ONE_LABELS = [
    # check_activation_ctx_zone11_match_cb starts @ 0x080671bc, THUMB+1=0x080671bd
    (0x080671bd, 'check_activation_ctx_zone11_match_cb_1'),
    # check_zone_activation_ctx_match_cb starts @ 0x08069cdc, THUMB+1=0x08069cdd
    (0x08069cdd, 'check_zone_activation_ctx_match_cb_1'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF08Seg6ThumbPlusPtrLabels (DRY=%s) ===" % DRY)
    sym_tbl = currentProgram.getSymbolTable()
    ok = 0
    for addr_val, label in THUMB_PLUS_ONE_LABELS:
        a = _addr(addr_val)
        if DRY:
            print("[dry] label 0x%08x  %s" % (addr_val, label))
            ok += 1
            continue
        existing = list(sym_tbl.getSymbols(a))
        names = [s.getName() for s in existing]
        if label not in names:
            sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
            print("[LABEL] created 0x%08x  %s" % (addr_val, label))
        else:
            print("[LABEL] already exists 0x%08x  %s" % (addr_val, label))
        # Make primary
        for s in list(sym_tbl.getSymbols(a)):
            if s.getName() == label:
                s.setPrimary()
                break
        ok += 1
    print("=== Done: %d labels ===" % ok)


main()
