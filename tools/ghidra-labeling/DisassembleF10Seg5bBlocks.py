# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF10Seg5bBlocks.py -- f10 Seg-5b R4 disasm (2 ROM_INCBIN blocks)
#
#   BLK7: fn_eligible_flute_summoning_kuriboh [0x0807f280..0x0807f2bc)  60B
#     THUMB+1 ref: ROM[0x09e430d0]=0x0807f281 (FS dispatch table entry)
#     CID 0x000019ec = FLUTE_SUMMONING_KURIBOH_CID at FS entry [+12]
#     MOV PC,r0 dispatch at 0x7f2b0 = 0x4687 (THUMB code -- do NOT createDWord)
#     Pool words: 0x7f2b4=gDuelPhaseFlags(0x0201b290), 0x7f2b8=JT-base(0x0807f2bc)
#     Jump table at 0x7f2bc..0x7f330 is ALREADY DECODED as .word in asm -- no action.
#
#   BLK8: dispatch_flute_summoning_kuriboh_by_state_code [0x0807f330..0x0807f458)  296B
#     raw ref: 0x7f32c = .word 0x0807f330 (last decoded JT entry points here)
#     ONE function body; 6 case entry points + default:
#       0x7f330: case state 0x80; 0x7f35e: case 0x7e; 0x7f376: case 0x7d
#       0x7f404: case 0x7c; 0x7f43a: case 0x78; 0x7f446: case 0x64; 0x7f44c: default
#     Epilogue: pop {r4,r5,r6} (0xbc70) + pop {r1} (0xbc02) + bx r1 (0x4708) @ 0x7f450
#     Pool words in BLK8: 0x7f3c4=0x0201e2a0, 0x7f3c8=0x0201c4e0,
#                         0x7f400=0x0201c4e0, 0x7f428=0x0201c4e0
#
# NOTE: All EOL/plate text is pure ASCII (no CJK). Ghidra Jython mojibake prevention.

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
    print("=== DisassembleF10Seg5bBlocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[DRY] BLK7 0x0807f280/0x3c: fn_eligible_flute_summoning_kuriboh")
        print("[DRY]   clearListing + setTMode 0x7f280..0x7f2bb")
        print("[DRY]   disasm_stub 0x7f280 (push {r4,r5,r6,lr} entry)")
        print("[DRY]   NOTE: 0x7f2b0=0x4687 MOV PC,r0 is THUMB CODE -- NOT createDWord")
        print("[DRY]   createDWord 0x7f2b4 = gDuelPhaseFlags=0x0201b290")
        print("[DRY]   createDWord 0x7f2b8 = JT-base 0x0807f2bc")
        print("[DRY]   createFunction 0x7f280 fn_eligible_flute_summoning_kuriboh")
        print("[DRY] BLK8 0x0807f330/0x128: dispatch_flute_summoning_kuriboh_by_state_code")
        print("[DRY]   clearListing + setTMode 0x7f330..0x7f457")
        print("[DRY]   disasm_stub 0x7f330 (single function body entry)")
        print("[DRY]   case labels: 0x7f330/0x7f35e/0x7f376/0x7f404/0x7f43a/0x7f446/0x7f44c")
        print("[DRY]   pool DWords: 0x7f3c4/0x7f3c8/0x7f400/0x7f428")
        print("[DRY]   createFunction 0x7f330 dispatch_flute_summoning_kuriboh_by_state_code")
        return

    # -----------------------------------------------------------------------
    # BLK7: fn_eligible_flute_summoning_kuriboh (0x0807f280..0x0807f2bb, 60B)
    # -----------------------------------------------------------------------
    print("--- BLK7: fn_eligible_flute_summoning_kuriboh ---")
    _clear_and_tmode(0x0807f280, 0x0807f2bb)
    _disasm_stub(0x0807f280)  # push {r4,r5,r6,lr} THUMB entry

    # Pool words: 0x7f2b4 = gDuelPhaseFlags, 0x7f2b8 = jump table ptr
    # NOTE: 0x7f2b0 = 0x4687 = MOV PC,r0 THUMB code -- do NOT createDWord here
    _create_dword(0x0807f2b4, 'flute_eligible_phase_flags',
                  'gDuelPhaseFlags=0x0201b290: duel phase flags struct base')
    _create_dword(0x0807f2b8, 'flute_eligible_jtable_ptr',
                  '0x0807f2bc: Flute of Summoning Kuriboh dispatch jump table base (29 entries)')

    _create_function(0x0807f280, 'fn_eligible_flute_summoning_kuriboh')

    # -----------------------------------------------------------------------
    # BLK8: dispatch_flute_summoning_kuriboh_by_state_code (0x0807f330..0x0807f457, 296B)
    # -----------------------------------------------------------------------
    print("--- BLK8: dispatch_flute_summoning_kuriboh_by_state_code ---")
    _clear_and_tmode(0x0807f330, 0x0807f457)

    # Per-case-stub DisassembleCommand (7 unique entry points from JT)
    # Each case stub branches independently and must be disassembled separately.
    _disasm_stub(0x0807f330)  # case state 0x80 (function entry / JT[28])
    _disasm_stub(0x0807f35e)  # case state 0x7e
    _disasm_stub(0x0807f376)  # case state 0x7d
    _disasm_stub(0x0807f404)  # case state 0x7c
    _disasm_stub(0x0807f43a)  # case state 0x78
    _disasm_stub(0x0807f446)  # case state 0x64 (return 0x64)
    _disasm_stub(0x0807f44c)  # default (return 0x0)

    # Pool DWords in BLK8 (4 total)
    _create_dword(0x0807f3c4, 'flute_dispatch_card_ctx',
                  'gDuelCardCtxBase=0x0201e2a0: duel card activation context base')
    _create_dword(0x0807f3c8, 'flute_dispatch_lp_base_a',
                  'gP1LifePoints=0x0201c4e0: LP state struct base')
    _create_dword(0x0807f400, 'flute_dispatch_lp_base_b',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (case 0x7e path)')
    _create_dword(0x0807f428, 'flute_dispatch_lp_base_c',
                  'gP1LifePoints=0x0201c4e0: LP state struct base (case 0x7d path)')

    # Case entry labels (6 cases + default)
    _create_label(0x0807f330, 'flute_case_0x80_0807f330',
                  'Flute dispatch case 0x80: state_reset_path (JT entry[28])')
    _create_label(0x0807f35e, 'flute_case_0x7e_0807f35e',
                  'Flute dispatch case 0x7e')
    _create_label(0x0807f376, 'flute_case_0x7d_0807f376',
                  'Flute dispatch case 0x7d')
    _create_label(0x0807f404, 'flute_case_0x7c_0807f404',
                  'Flute dispatch case 0x7c')
    _create_label(0x0807f43a, 'flute_case_0x78_0807f43a',
                  'Flute dispatch case 0x78')
    _create_label(0x0807f446, 'flute_case_0x64_0807f446',
                  'Flute dispatch case 0x64 (return 0x64)')
    _create_label(0x0807f44c, 'flute_case_default_0807f44c',
                  'Flute dispatch default (return 0x0)')

    _create_function(0x0807f330, 'dispatch_flute_summoning_kuriboh_by_state_code')

    print("")
    print("=== DisassembleF10Seg5bBlocks DONE ===")
    print("=== BLK7: fn_eligible_flute_summoning_kuriboh @ 0x0807f280 (2 pool DWords) ===")
    print("=== BLK8: dispatch_flute_summoning_kuriboh_by_state_code @ 0x0807f330 (4 pool DWords) ===")


main()
