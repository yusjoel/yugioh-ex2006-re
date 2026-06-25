# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF11Seg1PoolFix.py -- fix literal pool DWord data items inside BLK1+BLK2 regions
#
# Problem: After clearListing + DisassembleCommand, literal pool words within the
# disassembled function bodies were not created as DWord data items. Ghidra exports
# them as raw .byte blocks. GAS ldr instructions reference the labels but some are
# either missing or only the outer block label exists (not the inner offsets).
#
# This causes "invalid offset, value too big (0xFFFFFFFC)" errors in GAS because
# the referenced label is not defined (resolves to 0, giving PC-relative offset -4).
#
# Fix: Force-createDWord at each literal pool slot address with a USER label.
# This makes Ghidra export them as .word with proper labels.
#
# All 14 pool slots with ROM values verified:
#   BLK1 pool (2 slots):
#     0x08085110 = gDuelPhaseFlags   (0x0201b290)
#     0x08085114 = blk1_jt_base      (0x08085118)
#   BLK2 pool (12 slots):
#     0x08085184 = dual_label_mask   (0xfffc7fff)   -- already labeled, verify
#     0x08085188 = gDuelCardCtxBase  (0x0201e2a0)
#     0x0808518c = gP1LifePoints     (0x0201c4e0)
#     0x080851a4 = gDuelPhaseFlags   (0x0201b290)
#     0x080851bc = gP1LifePoints     (0x0201c4e0)
#     0x08085214 = ELIGIB_SPRITE_CTRL_OFF (0x00001d68)
#     0x08085218 = ELIGIB_ANIM_STATE_OFF  (0x00001d6c)
#     0x0808522c = gDuelPhaseFlags   (0x0201b290)
#     0x08085250 = gDuelCardCtxBase  (0x0201e2a0)
#     0x08085254 = gP1LifePoints     (0x0201c4e0)
#     0x08085274 = 0x0000013b        (invoke_card_display_op arg 0x13b)
#     0x08085278 = gDuelPhaseFlags   (0x0201b290)
#
# All ROM values verified via python struct.unpack_from.
# NOTE: All EOL text is pure ASCII.

from ghidra.program.model.data import DWordDataType
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


def _check(addr_int, expected_val):
    mem = currentProgram.getMemory()
    try:
        actual = mem.getInt(_addr(addr_int)) & 0xFFFFFFFF
        if actual != (expected_val & 0xFFFFFFFF):
            print("FAIL check @0x%08x: expected=0x%08x actual=0x%08x" % (
                addr_int, expected_val & 0xFFFFFFFF, actual))
            return False
    except Exception as e:
        print("FAIL read @0x%08x: %s" % (addr_int, e))
        return False
    return True


def _create_dword(addr_int, label, eol, expected_val):
    if not _check(addr_int, expected_val):
        print("SKIP 0x%08x (value mismatch)" % addr_int)
        return False
    if DRY:
        print("[dry] DWord 0x%08x = 0x%08x  label=%s" % (addr_int, expected_val, label))
        return True
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    sym_table = currentProgram.getSymbolTable()
    try:
        sym_table.createLabel(a, label, SourceType.USER_DEFINED)
        for s in sym_table.getSymbols(a):
            if s.getName() == label:
                s.setPrimary()
                break
    except Exception as e:
        print("[warn] label 0x%08x %s: %s" % (addr_int, label, e))
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[dword] 0x%08x  %s" % (addr_int, label))
    return True


# (addr, label, eol, expected_val)
POOL_DWORDS = [
    # BLK1 literal pool (0x080850f0..0x08085118)
    (0x08085110, 'gduelphaseflag_85110',
     'gDuelPhaseFlags pool (dispatch_equip_slot_display_by_type_scarr)',
     0x0201b290),
    (0x08085114, 'blk1_jt_base_85114',
     'fn-ptr table base = 0x08085118 (6-entry raw pointer dispatch table)',
     0x08085118),

    # BLK2 literal pool words (0x08085130..0x0808527c)
    # eval_equip_slot_player_match_and_set_lp_active pool area (0x08085184..0x0808518f)
    (0x08085184, 'dual_label_clear_mask_85184',
     'DUAL_LABEL_RENDER_STATE_CLEAR=0xfffc7fff: clears bits 15-17 of sprite attr word',
     0xfffc7fff),
    (0x08085188, 'gduecardctx_85188',
     'gDuelCardCtxBase pool (eval_equip_slot_player_match_and_set_lp_active)',
     0x0201e2a0),
    (0x0808518c, 'gp1lp_ptr_8518c',
     'gP1LifePoints pool (eval_equip_slot_player_match_and_set_lp_active)',
     0x0201c4e0),

    # LAB_08085198 pool area (0x080851a2..0x080851a7 -> DWord at 0x080851a4)
    (0x080851a4, 'gduelphaseflag_851a4',
     'gDuelPhaseFlags pool (eval: SLOT_DISPLAY_TYPE_OFF increment path)',
     0x0201b290),

    # check_lp_pending pool area (0x080851ba..0x080851bf -> DWord at 0x080851bc)
    (0x080851bc, 'gp1lp_ptr_851bc',
     'gP1LifePoints pool (check_lp_pending_and_set_equip_activation_state)',
     0x0201c4e0),

    # enqueue_equip_slot_sprite pool area (0x08085214..0x0808521b)
    (0x08085214, 'eligib_sprite_ctrl_off_85214',
     'ELIGIB_SPRITE_CTRL_OFF=0x1d68 pool (enqueue_equip_slot_sprite_if_display_confirmed)',
     0x00001d68),
    (0x08085218, 'eligib_anim_state_off_85218',
     'ELIGIB_ANIM_STATE_OFF=0x1d6c pool (enqueue_equip_slot_sprite_if_display_confirmed)',
     0x00001d6c),

    # store_decremented_display_type pool area (0x0808522a..0x0808522f -> DWord at 0x0808522c)
    (0x0808522c, 'gduelphaseflag_8522c',
     'gDuelPhaseFlags pool (store_decremented_display_type_and_return SLOT_DISPLAY_TYPE_OFF)',
     0x0201b290),

    # activate_or_enqueue_type3 pool area (0x08085250..0x08085257)
    (0x08085250, 'gduecardctx_85250',
     'gDuelCardCtxBase pool (activate_or_enqueue_type3_equip_slot_display)',
     0x0201e2a0),
    (0x08085254, 'gp1lp_ptr_85254',
     'gP1LifePoints pool (activate_or_enqueue_type3_equip_slot_display)',
     0x0201c4e0),

    # LAB_08085258 pool area (0x08085274..0x0808527b)
    (0x08085274, 'invoke_disp_arg_13b_85274',
     '0x0000013b: arg to invoke_card_display_op_0x31_sub1 (type-3 enqueue path)',
     0x0000013b),
    (0x08085278, 'gduelphaseflag_85278',
     'gDuelPhaseFlags pool (shared SLOT_DISPLAY_TYPE_OFF increment path)',
     0x0201b290),
]


def main():
    print("=== RefineF11Seg1PoolFix (DRY=%s) ===" % DRY)
    print("  Creating %d literal pool DWord data items" % len(POOL_DWORDS))

    ok = fail = 0
    for (addr, label, eol, val) in POOL_DWORDS:
        if _create_dword(addr, label, eol, val):
            ok += 1
        else:
            fail += 1

    print("\n=== RefineF11Seg1PoolFix DONE ===")
    print("  DWord: %d/%d OK  FAIL: %d" % (ok, len(POOL_DWORDS), fail))


main()
