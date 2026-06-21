# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# NameF10Seg1FnEligible.py -- Name the 4 fn_eligible stubs in f10 Seg-1
#   These stubs were disassembled by DisassembleF10Seg1Blocks.py but left without
#   function objects / named labels. This script creates / renames each one.
#
#   0x08079fac  fn_eligible_abyssal_designator     CID=0x17f4 (Abyssal Designator)
#   0x0807a138  fn_eligible_big_wave_small_wave     CID=0x17f9 (Big Wave Small Wave)
#   0x0807a3b8  fn_eligible_cid_15de               CID=0x1803 (unassigned) + 0x15de (unassigned)
#   0x0807a688  fn_eligible_magicians_circle        CID=0x1818 (Magician's Circle)
#
# Naming convention matches file-09 fn_eligible stubs (fn_eligible_<card_name_snake_case>).
# For the shared stub (CID 0x1803 + 0x15de), both CIDs are unassigned in card-stats.s,
# so the neutral form fn_eligible_cid_15de is used (0x15de is the lower/assigned-side CID).
#
# NOTE: All text is pure ASCII.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260621_131103-pre-F10Seg1FnEligible

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.address import AddressSet

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


STUBS = [
    (0x08079fac, "fn_eligible_abyssal_designator"),
    (0x0807a138, "fn_eligible_big_wave_small_wave"),
    (0x0807a3b8, "fn_eligible_cid_15de"),
    (0x0807a688, "fn_eligible_magicians_circle"),
]


def name_stub(addr_int, name):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()

    fn = fm.getFunctionAt(a)
    if fn is None:
        fn = fm.getFunctionContaining(a)
        if fn is not None:
            entry = fn.getEntryPoint()
            if entry.getOffset() != addr_int:
                print("[WARN] getFunctionContaining mismatch: expected 0x%08x, got 0x%s" % (addr_int, entry))
                fn = None

    if fn is not None:
        old_name = fn.getName()
        if DRY:
            print("[dry] RENAME 0x%08x: %s -> %s" % (addr_int, old_name, name))
        else:
            fn.setName(name, SourceType.USER_DEFINED)
            print("[RENAME] 0x%08x: %s -> %s" % (addr_int, old_name, name))
    else:
        # No function object -- create one.
        # Use a conservatively large body bound; Ghidra will trim to actual body.
        body = AddressSet(a, _addr(addr_int + 0x80))
        if DRY:
            print("[dry] CREATE fn %s @ 0x%08x" % (name, addr_int))
        else:
            try:
                fn2 = fm.createFunction(name, a, body, SourceType.USER_DEFINED)
                if fn2 is not None:
                    print("[CREATE] fn %s @ 0x%08x" % (name, addr_int))
                else:
                    print("[WARN] createFunction returned None @ 0x%08x" % addr_int)
                    # Fallback: ensure label
                    existing = [s.getName() for s in sym_tbl.getSymbols(a)]
                    if name not in existing:
                        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
                        print("[LABEL] created %s @ 0x%08x" % (name, addr_int))
            except Exception as e:
                print("[WARN] createFunction error @ 0x%08x: %s" % (addr_int, e))
                # Fallback: ensure label
                existing = [s.getName() for s in sym_tbl.getSymbols(a)]
                if name not in existing:
                    sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
                    print("[LABEL] created %s @ 0x%08x" % (name, addr_int))


def main():
    print("=== NameF10Seg1FnEligible (DRY=%s) ===" % DRY)
    for addr_int, name in STUBS:
        name_stub(addr_int, name)
    print("=== NameF10Seg1FnEligible DONE (%d stubs) ===" % len(STUBS))


main()
