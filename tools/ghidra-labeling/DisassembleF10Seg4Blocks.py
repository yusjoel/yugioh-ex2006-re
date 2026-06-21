# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg4Blocks.py -- f10 Seg-4 R4 disasm (2 ROM_INCBIN + 1 inline .byte)
#
#   BLK1 0x0807d7e8/0x2c (44B): fn_eligible_sillva_warlord_of_dark_world
#     THUMB+1 ref 0x0807d7e9 at FS table 0x09e46220
#     CID @ 0x09e4621c = 0x00001968 = SILLVA_WARLORD_OF_DARK_WORLD_CID
#     Bytes: push{r4,r5,lr}; state dispatch; indirect branch at +0x20 = 0x4687 (MOV PC,r0) -- CODE!
#     Pool 1 @ 0x0807d80c = 0x0201b290 (gDuelPhaseFlags)
#     Pool 2 @ 0x0807d810 = 0x0807d814 (Sillva dispatch JT base)
#     TRAP: 0x4687 at 0x0807d808 = THUMB MOV PC,r0 -- do NOT createDWord!
#
#   BLK2 0x0807d830/0xfc (252B): sillva_dispatch_stubs (5 unique sub-stubs)
#     JT at 0x7d814..0x7d82c (7 entries) points here (raw ptr, not THUMB+1)
#     Sub-stubs: A@0x7d830, B@0x7d880, C@0x7d898, D@0x7d8d4, E@0x7d920
#     9 pool words (createDWord); no 0x4687 in BLK2 (safe)
#
#   inline .byte @ 0x0807db14/0xc (12B): fn_eligible_dark_deal
#     THUMB+1 ref 0x0807db15 at FS table 0x09e42d88
#     CID @ 0x09e42d84 = 0x00001975 = DARK_DEAL_CID
#     Bytes: 20 20 0a 79 10 43 08 71 00 20 70 47 (no pool, leaf, bx lr)
#     Ends at 0x0807db20 = Seg-4 boundary
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
    print("=== DisassembleF10Seg4Blocks (DRY=%s) ===" % DRY)
    if DRY:
        print("[DRY] No Ghidra state changes will be made.")
        print("[DRY] Would clear+disasm BLK1 0x0807d7e8..0x0807d813 (fn_eligible_sillva)")
        print("[DRY] Would createDWord at 2 BLK1 pool addresses (0x0807d80c, 0x0807d810)")
        print("[DRY]   NOTE: 0x0807d808=0x4687 is THUMB MOV PC,r0 -- NOT createDWord!")
        print("[DRY] Would createFunction fn_eligible_sillva_warlord_of_dark_world @ 0x0807d7e8")
        print("[DRY] Would clear+disasm BLK2 0x0807d830..0x0807d92b (5 Sillva sub-stubs)")
        print("[DRY] Would createDWord at 9 BLK2 pool addresses")
        print("[DRY] Would clear+disasm inline 0x0807db14..0x0807db1f (fn_eligible_dark_deal)")
        print("[DRY] Would createFunction fn_eligible_dark_deal @ 0x0807db14")
        return

    # -----------------------------------------------------------------------
    # BLK1: fn_eligible_sillva_warlord_of_dark_world (0x0807d7e8..0x0807d813, 44B)
    # -----------------------------------------------------------------------
    print("--- BLK1: fn_eligible_sillva_warlord_of_dark_world ---")
    _clear_and_tmode(0x0807d7e8, 0x0807d813)
    _disasm_stub(0x0807d7e8)  # push {r4,r5,lr} THUMB entry

    # Pool words at +0x24 and +0x28; NOT the 0x4687 at +0x20 (0x0807d808 = MOV PC,r0 code)
    _create_dword(0x0807d80c, 'sillva_eligible_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807d810, 'sillva_eligible_jtable_ptr',
                  '0x0807d814: Sillva dispatch jump table base (7 entries)')

    # Create function at THUMB entry
    _create_function(0x0807d7e8, 'fn_eligible_sillva_warlord_of_dark_world')

    # -----------------------------------------------------------------------
    # BLK2: Sillva dispatch sub-stubs A..E (0x0807d830..0x0807d92b, 252B)
    # -----------------------------------------------------------------------
    print("--- BLK2: Sillva dispatch sub-stubs A..E ---")
    _clear_and_tmode(0x0807d830, 0x0807d92b)

    # Per-stub DisassembleCommand (do NOT use single-range; only first stub would disasm)
    _disasm_stub(0x0807d830)  # sub-stub A: state 0x80 activate
    _disasm_stub(0x0807d880)  # sub-stub B: state 0x7f trigger
    _disasm_stub(0x0807d898)  # sub-stub C: states 0x7c/0x7e hand enqueue
    _disasm_stub(0x0807d8d4)  # sub-stub D: states 0x7b/0x7d LP display
    _disasm_stub(0x0807d920)  # sub-stub E: state 0x7a counter

    # createDWord for 9 inline literal pools in BLK2
    _create_dword(0x0807d878, 'sillva_stub_a_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (sub-stub A)')
    _create_dword(0x0807d87c, 'sillva_stub_a_player_stride',
                  'PLAYER_BLOCK_STRIDE=0x868: byte stride between P1/P2 data blocks (sub-stub A)')
    _create_dword(0x0807d8c8, 'sillva_stub_c_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (sub-stub C/D shared)')
    _create_dword(0x0807d8cc, 'sillva_stub_c_player_stride',
                  'PLAYER_BLOCK_STRIDE=0x868: byte stride (sub-stub C/D shared)')
    _create_dword(0x0807d8d0, 'sillva_stub_c_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub C/D shared)')
    _create_dword(0x0807d910, 'sillva_stub_d_lp_base',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (sub-stub D)')
    _create_dword(0x0807d914, 'sillva_stub_d_player_stride',
                  'PLAYER_BLOCK_STRIDE=0x868: byte stride (sub-stub D)')
    _create_dword(0x0807d918, 'sillva_stub_d_lp_track_base',
                  'LP_CARD_TRACK_BASE_OFF=0x1da8: [gP1LifePoints+0x1da8] LP card tracking base (sub-stub D)')
    _create_dword(0x0807d91c, 'sillva_stub_d_phase_flags_b',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base (sub-stub D dup)')

    # Sub-stub labels
    _create_label(0x0807d830, 'sillva_state_80_activate',
                  'Sillva sub-stub A: state 0x80 activate')
    _create_label(0x0807d880, 'sillva_state_7f_trigger',
                  'Sillva sub-stub B: state 0x7f trigger')
    _create_label(0x0807d898, 'sillva_state_7c_7e_hand_enqueue',
                  'Sillva sub-stub C: states 0x7c/0x7e hand enqueue')
    _create_label(0x0807d8d4, 'sillva_state_7b_7d_lp_display',
                  'Sillva sub-stub D: states 0x7b/0x7d LP display')
    _create_label(0x0807d920, 'sillva_state_7a_counter',
                  'Sillva sub-stub E: state 0x7a counter')

    # -----------------------------------------------------------------------
    # inline .byte: fn_eligible_dark_deal (0x0807db14..0x0807db1f, 12B)
    # -----------------------------------------------------------------------
    print("--- inline .byte: fn_eligible_dark_deal ---")
    _clear_and_tmode(0x0807db14, 0x0807db1f)
    _disasm_stub(0x0807db14)  # movs r0,#0x20 / ldrb r2,[r1,#0xa] / orrs r0,r2 / strb r0,[r1,#0x1] / movs r0,#0 / bx lr

    # Create function at THUMB entry (no pool needed, leaf fn, bx lr)
    _create_function(0x0807db14, 'fn_eligible_dark_deal')

    # EOL at entry
    _create_label(0x0807db14, 'fn_eligible_dark_deal',
                  'fn_eligible_dark_deal: CID=DARK_DEAL_CID=0x1975; ORs 0x20 into [r1+4]; returns 0 (leaf, bx lr, no pool)')

    print("")
    print("=== DisassembleF10Seg4Blocks DONE ===")
    print("=== BLK1: fn_eligible_sillva_warlord_of_dark_world @ 0x0807d7e8 (2 pool dwords) ===")
    print("=== BLK2: 5 Sillva sub-stubs A..E @ 0x0807d830 (9 pool dwords) ===")
    print("=== inline: fn_eligible_dark_deal @ 0x0807db14 (no pool, bx lr) ===")
    print("=== createFunction: fn_eligible_sillva_warlord_of_dark_world + fn_eligible_dark_deal ===")


main()
