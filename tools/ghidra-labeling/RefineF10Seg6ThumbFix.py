# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg6ThumbFix.py -- fix THUMB fn-ptr slot 0x0807ff88
#   Problem: REF_SLOTS created label 'check_equip_slot_eligible_by_node_player_thumb'
#   at 0x0807fad9 (addr+1 THUMB ptr inside a code unit). GAS can't resolve this label.
#   Fix: remove that label, add EOL comment to slot 0x0807ff88 explaining the fn-ptr.
#   The slot label 'dispatch_criteria_caseD7d_fn_ptr' remains; value stays raw 0x0807fad9.

from ghidra.program.model.symbol import SourceType
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
    print("=== RefineF10Seg6ThumbFix (DRY=%s) ===" % DRY)
    sym_tbl = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()

    # 1. Remove 'check_equip_slot_eligible_by_node_player_thumb' label from 0x0807fad9
    #    (inside code, can't be used as GAS label)
    bad_label = 'check_equip_slot_eligible_by_node_player_thumb'
    bad_addr = 0x0807fad9
    a_bad = _addr(bad_addr)
    found = False
    for sym in sym_tbl.getSymbols(a_bad):
        if sym.getName() == bad_label:
            found = True
            if DRY:
                print("[dry] would delete label '%s' @ 0x%08x" % (bad_label, bad_addr))
            else:
                sym.delete()
                print("[DEL] label '%s' @ 0x%08x deleted" % (bad_label, bad_addr))
    if not found:
        print("[info] label '%s' @ 0x%08x not found (already gone)" % (bad_label, bad_addr))

    # 2. Also remove the DATA reference from 0x0807ff88 to 0x0807fad9
    #    (we added it in REF_SLOTS; it points into code at +1 address which is confusing)
    slot_addr = 0x0807ff88
    target_addr = 0x0807fad9
    a_slot = _addr(slot_addr)
    a_tgt = _addr(target_addr)
    ref_mgr = currentProgram.getReferenceManager()
    for ref in list(ref_mgr.getReferencesFrom(a_slot)):
        if ref.getToAddress().equals(a_tgt):
            if DRY:
                print("[dry] would remove ref 0x%08x -> 0x%08x" % (slot_addr, target_addr))
            else:
                ref_mgr.delete(ref)
                print("[REF-DEL] removed ref 0x%08x -> 0x%08x" % (slot_addr, target_addr))

    # 3. Add EOL comment at 0x0807ff88 to document the fn-ptr
    eol_text = "fn-ptr check_equip_slot_eligible_by_node_player+1 (THUMB+1=0x0807fad9); fn @ 0x0807fad8"
    cu = listing.getCodeUnitAt(a_slot)
    if cu is not None:
        if DRY:
            print("[dry] would set EOL @ 0x%08x: %s" % (slot_addr, eol_text))
        else:
            cu.setComment(CodeUnit.EOL_COMMENT, eol_text)
            print("[EOL] 0x%08x: %s" % (slot_addr, eol_text))

    print("=== RefineF10Seg6ThumbFix DONE ===")


main()
