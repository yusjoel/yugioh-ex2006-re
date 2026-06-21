# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg3Blocks.py -- f10 Seg-3 R4 disasm (2 ROM_INCBIN blocks)
#
#   BLK1 0x0807c87a/0x3e (62B):
#     +0x00: des_frog_fn_eligible_pad (2B pad, 0x0000)
#     +0x02: fn_eligible_des_frog (THUMB fn_eligible stub, CID=DES_FROG_CID=0x1918)
#            THUMB+1 ref 0x0807c87d at FS table 0x09e45290
#            pool: +0x36=gDuelPhaseFlags (0x0201b290), +0x3a=0x0807c8b8 (dispatch table base)
#            POOL-vs-CODE trap: +0x32 = 0x4687 = MOV PC,r0 -- NOT createDWord!
#     createDWord: 0x0807c8b0 (gDuelPhaseFlags), 0x0807c8b4 (dispatch_table_base)
#
#   BLK2 0x0807c92c/0x158 (344B):
#     9 unique dispatch sub-stubs A..I for Des Frog card effect dispatch
#     Dispatch table 0x0807c8b8..0x0807c928 (29 entries, already .word in asm) points here
#     All 9 sub-stubs get per-stub DisassembleCommand
#     11 createDWord calls for inline literal pools
#
# fn_eligible function created:
#   fn_eligible_des_frog @ 0x0807c87c (CID=DES_FROG_CID=0x1918)
#
# NOTE: All EOL/plate text is pure ASCII (no CJK).

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType, DataTypeConflictHandler
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)


def _disasm_stub(entry_int):
    a = _addr(entry_int)
    cmd = DisassembleCommand(a, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (entry_int, cmd.getStatusMsg()))
    else:
        print("[disasm ok] 0x%08x" % entry_int)


def _create_dword(addr_int, label=None, eol=None):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sm = currentProgram.getSymbolTable()
        sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)


def _create_label(addr_int, label, eol=None):
    a = _addr(addr_int)
    sm = currentProgram.getSymbolTable()
    sm.createLabel(a, label, SourceType.USER_DEFINED)
    if eol:
        listing = currentProgram.getListing()
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[label ok] 0x%08x %s" % (addr_int, label))


def _create_function(addr_int, fn_name):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        fn.setName(fn_name, SourceType.USER_DEFINED)
        print("[fn rename] 0x%08x -> %s" % (addr_int, fn_name))
    else:
        fn = createFunction(a, fn_name)
        if fn is not None:
            print("[fn create] 0x%08x %s" % (addr_int, fn_name))
        else:
            print("[warn] createFunction 0x%08x %s failed" % (addr_int, fn_name))


def main():
    print("=== DisassembleF10Seg3Blocks (DRY=%s) ===" % DRY)
    if DRY:
        print("[DRY] No Ghidra state changes will be made.")
        print("[DRY] Would clear+disasm BLK1 0x0807c87a..0x0807c8b8")
        print("[DRY] Would clear+disasm BLK2 0x0807c92c..0x0807ca84")
        print("[DRY] Would createDWord at 13 pool addresses")
        print("[DRY] Would createFunction fn_eligible_des_frog @ 0x0807c87c")
        return

    # -----------------------------------------------------------------------
    # BLK1: fn_eligible_des_frog (0x0807c87a..0x0807c8b8, 62B)
    # -----------------------------------------------------------------------
    print("--- BLK1: fn_eligible_des_frog ---")
    _clear_and_tmode(0x0807c87a, 0x0807c8b7)  # hi inclusive for context; 0x87a..0x8b7
    # Disassemble from fn start (skip 2B pad at +0x00)
    _disasm_stub(0x0807c87c)  # fn_eligible_des_frog (THUMB; push {r4..r7,lr} at +0x02)

    # Force-split literal pool words (NOT the 0x4687 code word at 0x0807c8ac)
    _create_dword(0x0807c8b0, 'blk1_pool_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807c8b4, 'blk1_pool_dispatch_table',
                  '0x0807c8b8: Des Frog dispatch table base (29 entries)')

    # Labels
    _create_label(0x0807c87a, 'des_frog_fn_eligible_pad',
                  '2B pad before fn_eligible_des_frog THUMB stub')
    # createFunction at THUMB entry (even addr; Ghidra infers THUMB from TMode)
    _create_function(0x0807c87c, 'fn_eligible_des_frog')

    # -----------------------------------------------------------------------
    # BLK2: Des Frog dispatch sub-stubs A..I (0x0807c92c..0x0807ca84, 344B)
    # -----------------------------------------------------------------------
    print("--- BLK2: Des Frog dispatch sub-stubs A..I ---")
    _clear_and_tmode(0x0807c92c, 0x0807ca83)  # 0x92c..0xa83

    # Per-stub DisassembleCommand (do NOT use single-range; only first stub disasms)
    _disasm_stub(0x0807c92c)   # sub-stub A: zone check (check_neo_daedalus_placement_eligible)
    _disasm_stub(0x0807c9c0)   # sub-stub B: display init (trigger+init_effect_slot_display_context)
    _disasm_stub(0x0807c9ec)   # sub-stub C: incr counter (increment_lp_bar_display_counter)
    _disasm_stub(0x0807ca18)   # sub-stub D: OAM setup (get_effect_slot + lookup + invoke_setup_equip_oam)
    _disasm_stub(0x0807ca50)   # sub-stub E: ret 0x77 (check_zone_eligible_with_deck_flag)
    _disasm_stub(0x0807ca5c)   # sub-stub F: ret 0x76 (set_lp_row_type7_if_opponent_linked)
    _disasm_stub(0x0807ca68)   # sub-stub G: ret 0x64 (decrement_lp_bar_display_counter)
    _disasm_stub(0x0807ca74)   # sub-stub H: enqueue_lp (enqueue_lp_counter_sprite_by_player)
    _disasm_stub(0x0807ca7a)   # sub-stub I: default exit (movs r0,#0; pop; bx)

    # createDWord for inline literal pools in BLK2
    # (11 pool words; excluding 0x0807c95c=0xe00a and 0x0807ca08=0xe038 which are THUMB branches)
    _create_dword(0x0807c960, 'blk2_pool_tadpole_cid',
                  'TADPOLE_CID=0x00001919: Tadpole card ID (adjacent to Des Frog, used in sub-stub A)')
    _create_dword(0x0807c964, 'blk2_pool_phase_flags_a',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807c968, 'blk2_pool_frame_off_a',
                  'EQUIP_PHASE_FRAME_OFF=0x4a4: equip phase frame slot')
    _create_dword(0x0807c9a8, 'blk2_pool_phase_flags_b',
                  'gDuelPhaseFlags=0x0201b290: dup in sub-stub B')
    _create_dword(0x0807c9ac, 'blk2_pool_frame_off_b',
                  'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in sub-stub B')
    _create_dword(0x0807c9bc, 'blk2_pool_card_display_op31',
                  'CARD_DISPLAY_OP31_LP_BAR_SUB=0x11d: card display op31 LP bar sub-type')
    _create_dword(0x0807c9e8, 'blk2_pool_frame_off_c',
                  'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in sub-stub C')
    _create_dword(0x0807ca0c, 'blk2_pool_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base')
    _create_dword(0x0807ca10, 'blk2_pool_phase_flags_c',
                  'gDuelPhaseFlags=0x0201b290: dup in sub-stub D')
    _create_dword(0x0807ca14, 'blk2_pool_frame_off_d',
                  'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in sub-stub D')
    _create_dword(0x0807ca44, 'blk2_pool_frame_off_e',
                  'EQUIP_PHASE_FRAME_OFF=0x4a4: dup in sub-stub E')

    # Sub-stub labels
    _create_label(0x0807c92c, 'des_frog_stub_a_zone_check',
                  'Des Frog sub-stub A: check neo-daedalus placement + extra-deck + monster count')
    _create_label(0x0807c9c0, 'des_frog_stub_b_display_init',
                  'Des Frog sub-stub B: trigger card display op31 + init effect slot display ctx')
    _create_label(0x0807c9ec, 'des_frog_stub_c_incr_counter',
                  'Des Frog sub-stub C: increment LP bar display counter; returns 0x7d')
    _create_label(0x0807ca18, 'des_frog_stub_d_oam_setup',
                  'Des Frog sub-stub D: effect slot entry + lookup + invoke_setup_equip_oam; returns 0x7d')
    _create_label(0x0807ca50, 'des_frog_stub_e_ret77',
                  'Des Frog sub-stub E: check_zone_eligible_with_deck_flag; movs r0,#0x77; b I+2')
    _create_label(0x0807ca5c, 'des_frog_stub_f_ret76',
                  'Des Frog sub-stub F: set_lp_row_type7_if_opponent_linked; movs r0,#0x76; b I+2')
    _create_label(0x0807ca68, 'des_frog_stub_g_ret64',
                  'Des Frog sub-stub G: decrement_lp_bar_display_counter; movs r0,#0x64; b I+2')
    _create_label(0x0807ca74, 'des_frog_stub_h_enqueue_lp',
                  'Des Frog sub-stub H: enqueue_lp_counter_sprite_by_player; movs r0,#0 -> falls through to I')
    _create_label(0x0807ca7a, 'des_frog_stub_i_default_exit',
                  'Des Frog sub-stub I: default exit (raw=21/29); movs r0,#0; pop {r4..r7}; pop {r1}; bx r1')

    print("")
    print("=== DisassembleF10Seg3Blocks DONE: BLK1(fn_eligible_des_frog) BLK2(9 sub-stubs) ===")
    print("=== createDWord: 2(BLK1) + 11(BLK2) = 13 total ===")
    print("=== createFunction: fn_eligible_des_frog @ 0x0807c87c ===")


main()
