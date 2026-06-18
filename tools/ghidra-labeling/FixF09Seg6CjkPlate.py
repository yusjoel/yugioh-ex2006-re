# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF09Seg6CjkPlate.py -- fix CJK mojibake plate in Seg-6
#
# Target: dispatch_dragon_summon_or_lp_delta_by_slot_type @ 0x08074770
# Issue: plate comment contains CJK characters (Ghidra Jython double-UTF8 mojibake)
# Fix: replace with pure ASCII plate comment
#
# NOTE: All text must be pure ASCII.

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

NEW_PLATE = (
    "Equip slot type routing by slot type code: reads halfword[+2] bits[11:6] "
    "(mask 0xfc0 = 0xfc<<4); compares with 0x3c0 (0xf0<<2); "
    "if equal: calls apply_lp_delta_for_slot_player (direct LP delta update path); "
    "if not equal: calls tick_dragon_summon_effect_display_state_machine "
    "(advances dragon-summon display state machine). "
    "Returns callee return value. Short fn; type code 0x3c0 = specific equip slot path; indeg=0."
)

def main():
    print("=== FixF09Seg6CjkPlate (DRY=%s) ===" % DRY)
    fn_addr = 0x08074770
    a = _addr(fn_addr)
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(a)
    if cu is None:
        print("[FAIL] no code unit @ 0x%08x" % fn_addr)
        return
    existing = cu.getComment(CodeUnit.PLATE_COMMENT)
    print("  existing plate: %r" % (existing[:80] if existing else None,))

    if DRY:
        print("[dry] Would replace plate @ 0x%08x with ASCII text (%d chars)" % (fn_addr, len(NEW_PLATE)))
        return

    cu.setComment(CodeUnit.PLATE_COMMENT, NEW_PLATE)
    print("[ok ] set ASCII plate @ 0x%08x (%d chars)" % (fn_addr, len(NEW_PLATE)))
    print("=== FixF09Seg6CjkPlate DONE ===")


main()
