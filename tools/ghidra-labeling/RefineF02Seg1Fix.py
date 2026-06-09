# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF02Seg1Fix.py -- fix DE/IT swap + aob_ctx_sub REF removal
# Removes the wrong gDuelSceneBase REF at 0x0802dedc (was accidentally set)
# and fixes game_str_de/it swap for slots 0x0802df04/0x0802df14/0x0802df48/0x0802df58

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

def _check(slot_addr, expected_val, label):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _remove_ref(slot_addr, target_vaddr, gas_label):
    """Remove a DATA ref from slot to target, and remove wrong label at slot if any."""
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    ref_mgr = currentProgram.getReferenceManager()
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] REMOVE_REF 0x%08x -> 0x%08x  %s" % (slot_addr, target_vaddr, gas_label))
        return

    # Remove the reference from slot to target
    removed = False
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.delete(ref)
            removed = True
    if removed:
        print("[REM_REF] 0x%08x -> 0x%08x  %s" % (slot_addr, target_vaddr, gas_label))
    else:
        print("[WARN] no ref found at 0x%08x -> 0x%08x" % (slot_addr, target_vaddr))

    # Also remove any user label at slot that was wrongly set
    # (the slot was labeled 'init_opp_card_display_vram_aob_ctx_sub' pointing to gDuelSceneBase)

def _apply_ref(slot_addr, target_vaddr, gas_label, slot_label, eol):
    sa = _addr(slot_addr)
    ta = _addr(target_vaddr)
    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    if DRY:
        print("[dry] REF 0x%08x -> 0x%08x  %s  slot=%s" % (
            slot_addr, target_vaddr, gas_label, slot_label))
        return

    tgt_syms = sym_tbl.getSymbols(ta)
    tgt_names = [s.getName() for s in tgt_syms]
    if gas_label not in tgt_names:
        sym_tbl.createLabel(ta, gas_label, SourceType.USER_DEFINED)

    ref_mgr.addMemoryReference(sa, ta, RefType.DATA, SourceType.USER_DEFINED, 0)
    for ref in ref_mgr.getReferencesFrom(sa):
        if ref.getToAddress().equals(ta):
            ref_mgr.setPrimary(ref, True)

    s_syms = sym_tbl.getSymbols(sa)
    s_names = [s.getName() for s in s_syms]
    if slot_label not in s_names:
        sym_tbl.createLabel(sa, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(sa)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[REF] 0x%08x -> 0x%08x  %s  slot=%s" % (
        slot_addr, target_vaddr, gas_label, slot_label))

def _apply_rename(slot_addr, slot_label, eol):
    a = _addr(slot_addr)
    sym_tbl = currentProgram.getSymbolTable()
    if DRY:
        print("[dry] RENAME 0x%08x -> %s" % (slot_addr, slot_label))
        return
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if slot_label not in names:
        sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)
    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[REN] 0x%08x -> %s" % (slot_addr, slot_label))

def main():
    print("=== RefineF02Seg1Fix (DRY=%s) ===" % DRY)

    # 1. Remove wrong REF at 0x0802dedc -> 0x02023360 (gDuelSceneBase)
    #    The slot value is 0x020233ac (gDuelSceneBase+0x4c), not 0x02023360
    print("\n--- Fix 1: Remove wrong gDuelSceneBase REF at 0x0802dedc ---")
    _remove_ref(0x0802dedc, 0x02023360, 'gDuelSceneBase')

    # 2. Fix game_str DE/IT swap: correct the REF labels
    #    slot 0x0802df04 = 0x09dec2de = IT 0326 (NOT DE)
    #    slot 0x0802df14 = 0x09dd3d04 = DE 0326 (NOT IT)
    #    slot 0x0802df48 = 0x09dec2e6 = IT 0327 (NOT DE)
    #    slot 0x0802df58 = 0x09dd3d0e = DE 0327 (NOT IT)
    print("\n--- Fix 2: Correct game_str DE/IT REF labels ---")

    # Remove wrong IT ref from 0x0802df14 (was set to game_str_it_0326 at 0x09dd3d04)
    # Remove wrong DE ref from 0x0802df04 (was set to game_str_de_0326 at 0x09dec2de)
    # Actually the first run set them with old (wrong) labels. We need to:
    # a) remove the wrong refs
    # b) add correct refs

    # Slot 0x0802df04: should be game_str_it_0326 @ 0x09dec2de
    # But was set as game_str_de_0326 @ 0x09dec2de in first run
    # The target label game_str_it_0326 needs to be at 0x09dec2de
    # The target label game_str_de_0326 was wrongly placed at 0x09dec2de - need to remove it
    sa04 = _addr(0x0802df04)
    sa14 = _addr(0x0802df14)
    sa48 = _addr(0x0802df48)
    sa58 = _addr(0x0802df58)

    t_de0326 = _addr(0x09dec2de)  # old wrong DE target (actually IT)
    t_it0326 = _addr(0x09dd3d04)  # old wrong IT target (actually DE)
    t_de0327 = _addr(0x09dec2e6)  # old wrong DE target (actually IT)
    t_it0327 = _addr(0x09dd3d0e)  # old wrong IT target (actually DE)

    sym_tbl = currentProgram.getSymbolTable()
    ref_mgr = currentProgram.getReferenceManager()

    # Remove wrong game_str_de_0326 label from 0x09dec2de and
    # remove wrong game_str_it_0326 label from 0x09dd3d04
    def _remove_label_at(addr_val, label_name):
        a = _addr(addr_val)
        for sym in sym_tbl.getSymbols(a):
            if sym.getName() == label_name:
                if DRY:
                    print("[dry] REMOVE_LABEL 0x%08x %s" % (addr_val, label_name))
                else:
                    sym.delete()
                    print("[REM_LABEL] 0x%08x %s" % (addr_val, label_name))
                return
        print("[WARN] label %s not found at 0x%08x" % (label_name, addr_val))

    # Remove wrongly-placed labels
    _remove_label_at(0x09dec2de, 'game_str_de_0326')
    _remove_label_at(0x09dd3d04, 'game_str_it_0326')
    _remove_label_at(0x09dec2e6, 'game_str_de_0327')
    _remove_label_at(0x09dd3d0e, 'game_str_it_0327')

    # Remove wrong refs from slots
    _remove_ref(0x0802df04, 0x09dec2de, 'game_str_de_0326(wrong)')
    _remove_ref(0x0802df14, 0x09dd3d04, 'game_str_it_0326(wrong)')
    _remove_ref(0x0802df48, 0x09dec2e6, 'game_str_de_0327(wrong)')
    _remove_ref(0x0802df58, 0x09dd3d0e, 'game_str_it_0327(wrong)')

    # Now add correct refs
    print("\n--- Fix 3: Add correct game_str DE/IT REFs ---")
    _apply_ref(0x0802df04, 0x09dec2de, 'game_str_it_0326',
               'init_opp_card_display_str_it_0326', None)
    _apply_ref(0x0802df14, 0x09dd3d04, 'game_str_de_0326',
               'init_opp_card_display_str_de_0326', None)
    _apply_ref(0x0802df48, 0x09dec2e6, 'game_str_it_0327',
               'init_opp_card_display_str_it_0327', None)
    _apply_ref(0x0802df58, 0x09dd3d0e, 'game_str_de_0327',
               'init_opp_card_display_str_de_0327', None)

    print("\n=== RefineF02Seg1Fix DONE ===")

main()
