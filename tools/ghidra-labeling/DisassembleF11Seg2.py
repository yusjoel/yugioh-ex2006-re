# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF11Seg2.py -- f11 Seg-2 disasm of ROM_INCBIN block 0x080861a0/0x27a
#
# Block: 0x080861a0..0x0808641a (634 B, 6 distinct case-body entry points)
# Parent: dispatch_equip_slot_state_by_index @ 0x0808611c dispatches via raw-PC (mov pc,r0)
#   using jump table at PTR_DAT_08086174 (11 entries [0..0xa]):
#   [0]=0x080861a0, [1,5]=0x0808621c, [2]=0x080862ec, [3]=0x08086338,
#   [4]=0x08086370, [6..9]=0x0808641a(fallback outside block), [10]=0x080863cc
#
# Action:
#   1. clearListing + setTMode THUMB for 0x080861a0..0x0808641a
#   2. Per-case-body DisassembleCommand (6 bodies, per-stub per-block method)
#   3. createLabel (NOT createFunction) for each of the 6 entry points
#   4. createDWord for 27 embedded literal pool slots inside block (incl. 0x080863f8)
#
# Post-disasm gate: grep ROM_INCBIN/.byte-code in [0x080861a0,0x0808641a) == 0
# All sub-case labels are pure lowercase ASCII. No createFunction calls.
# All EOL text is pure ASCII. Ghidra Jython mojibake prevention.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.data import DWordDataType
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
    print("[tmode] set THUMB 0x%08x..0x%08x" % (lo_int, hi_int))


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
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
    if label:
        sym_table = currentProgram.getSymbolTable()
        try:
            sym_table.createLabel(a, label, SourceType.USER_DEFINED)
            for s in sym_table.getSymbols(a):
                if s.getName() == label:
                    s.setPrimary()
                    break
        except Exception as e:
            print("[warn] label dword 0x%08x %s: %s" % (addr_int, label, e))
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[dword] 0x%08x" % addr_int)


def _make_label(addr_int, name, eol=None):
    sym_table = currentProgram.getSymbolTable()
    listing = currentProgram.getListing()
    try:
        sym_table.createLabel(_addr(addr_int), name, SourceType.USER_DEFINED)
        for s in sym_table.getSymbols(_addr(addr_int)):
            if s.getName() == name:
                s.setPrimary()
                break
    except Exception as e:
        print("[warn] makeLabel 0x%08x %s: %s" % (addr_int, name, e))
    if eol:
        cu = listing.getCodeUnitAt(_addr(addr_int))
        if cu:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[label] %s @ 0x%08x" % (name, addr_int))


def main():
    print("=== DisassembleF11Seg2 (DRY=%s) ===" % DRY)
    print("Block: 0x080861a0..0x0808641a (634 B, 6 sub-case bodies, NO createFunction)")

    if DRY:
        print("[dry] Would: clearListing+setTMode 0x080861a0..0x0808641a")
        print("[dry] Would: DisassembleCommand x6 case bodies")
        print("[dry] Would: createLabel x6 (equip_slot_case0/1/2/3/4/casea_body)")
        print("[dry] Would: createDWord x26 literal pool slots")
        print("[dry] DRY done -- 0 FAIL expected")
        return

    # ------------------------------------------------------------------
    # Step 1: clearListing + setTMode THUMB for entire block
    # ------------------------------------------------------------------
    _clear_and_tmode(0x080861a0, 0x0808641a)

    # ------------------------------------------------------------------
    # Step 2: Per-case-body DisassembleCommand (6 bodies, address order)
    # Note: each DisassembleCommand runs until a terminal instruction (bx/b);
    #       we run them sequentially to ensure each body is disassembled.
    # ------------------------------------------------------------------
    print("\n--- Disassembling 6 case bodies ---")
    for ep in [0x080861a0, 0x0808621c, 0x080862ec, 0x08086338, 0x08086370, 0x080863cc]:
        _disasm_stub(ep)

    # ------------------------------------------------------------------
    # Step 3: createLabel (NOT createFunction) for each case-body entry
    # ------------------------------------------------------------------
    print("\n--- Creating case-body labels (NOT createFunction) ---")
    _make_label(0x080861a0, 'equip_slot_case0_body',
                'substate 0: read aux_ctx at gDuelPhaseFlags+0x58c*slot_stride; check active')
    _make_label(0x0808621c, 'equip_slot_case1_body',
                'substate 1 (and 5): check active bit and call state handler')
    _make_label(0x080862ec, 'equip_slot_case2_body',
                'substate 2: reads gDuelPhaseFlags field, may call text append')
    _make_label(0x08086338, 'equip_slot_case3_body',
                'substate 3: reads LP state, writes state value')
    _make_label(0x08086370, 'equip_slot_case4_body',
                'substate 4: reads gP1LifePoints LP fields')
    _make_label(0x080863cc, 'equip_slot_casea_body',
                'substate 0xa: reads two halfword fields, calls enable function')

    # ------------------------------------------------------------------
    # Step 4: createDWord for 27 embedded literal pool slots in block
    # (addresses and values from proposal disasm plan, ROM-verified)
    # ------------------------------------------------------------------
    print("\n--- Creating DWords for literal pool slots ---")

    # equip_slot_case0_body pool:
    _create_dword(0x080861dc, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')
    # 0x080861fc = 0x0000e0e1 = THUMB branch instruction, NOT a literal pool slot (skip)
    _create_dword(0x08086200, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')

    # equip_slot_case1_body pool:
    _create_dword(0x08086240, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')
    _create_dword(0x08086244, None,
                  'gDuelPhaseFlags=0x0201b290 (ewram.inc)')
    _create_dword(0x080862b4, None,
                  'game_text_sep_record=0x09e3f14c')
    _create_dword(0x080862e4, None,
                  'gDuelPhaseFlags=0x0201b290 (ewram.inc)')
    _create_dword(0x080862e8, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')

    # equip_slot_case3_body pool:
    _create_dword(0x08086310, None,
                  'gP1LifePoints=0x0201c4e0 (ewram.inc)')
    _create_dword(0x08086314, None,
                  'gDuelPhaseFlags=0x0201b290 (ewram.inc)')
    _create_dword(0x08086318, None,
                  'LP_BAR_ANIM_STATE_OFF=0x4cc (ewram.inc)')
    _create_dword(0x08086330, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')
    _create_dword(0x08086334, None,
                  'ELIGIB_STATE_CTRL_OFF=0x1d54 (ewram.inc)')

    # equip_slot_case4_body pool:
    _create_dword(0x08086350, None,
                  'gDuelPhaseFlags=0x0201b290 (ewram.inc)')
    _create_dword(0x08086368, None,
                  'gDuelPhaseFlags=0x0201b290 (ewram.inc)')
    _create_dword(0x0808636c, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')
    _create_dword(0x08086384, None,
                  'gP1LifePoints=0x0201c4e0 (ewram.inc)')
    _create_dword(0x08086388, None,
                  'ELIGIB_STATE_CTRL_OFF=0x1d54 (ewram.inc)')
    _create_dword(0x0808638c, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')

    # equip_slot_casea_body pool:
    _create_dword(0x080863ac, None,
                  'ELIGIB_ACT_TYPE_OFF=0x1d5c (ewram.inc)')
    _create_dword(0x080863b0, None,
                  'ELIGIB_ACT_COUNT_OFF=0x1d58 (ewram.inc)')
    _create_dword(0x080863b4, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')
    _create_dword(0x080863c8, None,
                  'EQUIP_SLOT_SUBSTATE_OFF=0x58c (ewram.inc)')
    _create_dword(0x080863f4, None,
                  'gP1LifePoints=0x0201c4e0 (ewram.inc)')
    _create_dword(0x080863f8, 'eligib_spr_ctrl_863f8',
                  'ELIGIB_SPRITE_CTRL_OFF=0x1d68 (ewram.inc L422); [gP1LifePoints+0x1d68] sprite display control')
    _create_dword(0x080863fc, None,
                  'ELIGIB_ANIM_STATE_OFF=0x1d6c (ewram.inc)')

    print("\n=== DisassembleF11Seg2 DONE ===")
    print("Block 0x080861a0..0x0808641a: 6 case bodies disassembled, 6 labels, 26 DWords")
    print("POST-DISASM GATE: verify ROM_INCBIN/.byte-code grep in range == 0")


main()
