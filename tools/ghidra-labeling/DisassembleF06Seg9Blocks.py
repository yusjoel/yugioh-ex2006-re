# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF06Seg9Blocks.py -- F06 Seg-9 R4 disasm (2 ranges)
#
# Block1 @ 0x0805a0aa..0x0805a0df (ROM_INCBIN 0x5a0aa 0x36)
#   2-byte alignment pad at 0x0805a0aa..0x0805a0ab (leave as data).
#   THUMB code entry: 0x0805a0ac..0x0805a0df (0x34 bytes = 1 new function)
#   Function: tick_bonding_or_photon_activation_seq @ 0x0805a0ac
#   Literal pool 0x0805a0d4..0x0805a0df:
#     [0x5a0d4] = CID 0x0000195c (Bonding-H2O)
#     [0x5a0d8] = CID 0x000019b1 (Photon Generator Unit)
#     [0x5a0dc] = gDuelPhaseFlags = 0x0201b290
#   THUMB+1 refs: 0x0805a0ad at 0x9e42ca4 (CID 0x195c) + 0x9e42f74 (CID 0x19b1)
#   NOTE: 0x0805a0e0..0x0805a0e3 holds .word 0x0805a0e4 (already decoded asm, NOT in incbin)
#   NOTE: 0x0805a0e4..0x0805a0f7 is dispatch table PTR_DAT_0805a0e4 (already decoded .word entries)
#
# Block2 @ 0x0805a0f8..0x0805a1db (ROM_INCBIN 0x5a0f8 0xe4)
#   5 THUMB sub-functions reached via raw-ptr dispatch table at 0x0805a0e4
#   (dispatch table uses raw addresses, NOT THUMB+1, because dispatcher uses mov pc,r0 not BX)
#   All 5 sub-functions need createFunction + setName + plate
#
# NOTE: 0x0805a0e0..0x0805a0e3: .word 0x0805a0e4 is OUTSIDE the Block1 incbin (ends at 0x5a0df).
#   The literal pool at 0x5a0d4..0x5a0df is inside Block1 and will be decoded as data by Ghidra.
#   After disasm, createDWord on literal pool slots forces data type.
#
# All plate comments: ASCII only (no CJK -- Jython double UTF-8 mojibake prevention).
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_084354-pre-F06Seg9

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
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


def _clear_and_set_thumb(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_addr, hi_addr))
    except Exception as e:
        print("[warn] clearListing(0x%08x..0x%08x): %s" % (lo_addr, hi_addr, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_addr, hi_addr))
    else:
        print("[warn] TMode register not found")


def _disasm_at(ep_int, block_lo, block_hi):
    """Disassemble at ep_int, restricted to [block_lo..block_hi]."""
    ep_addr = _addr(ep_int)
    lo = _addr(block_lo)
    hi = _addr(block_hi)
    cmd = DisassembleCommand(ep_addr, AddressSet(lo, hi), True)
    if cmd.applyTo(currentProgram):
        print("[ok ] disasm @ 0x%08x" % ep_int)
        return True
    else:
        print("[warn] disasm @ 0x%08x: %s" % (ep_int, cmd.getStatusMsg()))
        return False


def _create_dword(addr_int):
    """Force a DWORD data item at addr_int (literal pool slot).
    Clears any existing instruction/data at the 4-byte range first."""
    a = _addr(addr_int)
    hi = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.DWordDataType.dataType
    try:
        existing = listing.getDataAt(a)
        if existing is not None and existing.getDataType().equals(dt):
            print("[DW ] already DWORD @ 0x%08x" % addr_int)
            return True
        try:
            clearListing(a, hi)
        except Exception:
            pass
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr_int)
        return True
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
        return False


def _create_fn_or_label(addr_int, name):
    """Create function (or fallback label) at addr_int with name."""
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    sm = currentProgram.getSymbolTable()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        fn.setName(name, SourceType.USER_DEFINED)
        print("[FN ] renamed existing: %s @ 0x%08x" % (name, addr_int))
        return fn
    fn = createFunction(a, name)
    if fn is not None:
        fn.setName(name, SourceType.USER_DEFINED)
        print("[FN ] created: %s @ 0x%08x" % (name, addr_int))
        return fn
    sm.createLabel(a, name, SourceType.USER_DEFINED)
    print("[FN ] label fallback: %s @ 0x%08x" % (name, addr_int))
    return None


def _set_plate(addr_int, text):
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr_int))
    if cu is not None:
        cu.setComment(CodeUnit.PLATE_COMMENT, text)
        print("[ok ] plate set @ 0x%08x (%d chars)" % (addr_int, len(text)))
    else:
        print("[warn] no CodeUnit @ 0x%08x for plate" % addr_int)


def _count_instrs(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    listing = currentProgram.getListing()
    n = 0
    inst = listing.getInstructionAt(lo)
    while inst is not None and inst.getAddress().compareTo(hi) <= 0:
        n += 1
        inst = listing.getInstructionAfter(inst.getAddress())
    return n


# =========================================================================
# Block1: tick_bonding_or_photon_activation_seq @ 0x0805a0ac
#   ROM_INCBIN 0x5a0aa 0x36 covers 0x0805a0aa..0x0805a0df
#   Clear range: 0x0805a0aa..0x0805a0df (entire incbin range including pad)
#   Disasm entry: 0x0805a0ac (skip 2-byte pad at 0x0805a0aa..0x0805a0ab)
#   Literal pool: 0x0805a0d4..0x0805a0df (3 dwords: CID 0x195c, CID 0x19b1, gDuelPhaseFlags)
#   THUMB+1 refs: 0x0805a0ad (= 0x0805a0ac|1) at ROM 0x9e42ca4 + 0x9e42f74
# =========================================================================
BLOCK1_CLEAR_LO = 0x0805a0aa
BLOCK1_CLEAR_HI = 0x0805a0df  # inclusive: last byte of incbin range
BLOCK1_ENTRY    = 0x0805a0ac  # THUMB entry point (after 2-byte pad)
BLOCK1_POOL     = [
    0x0805a0d4,  # CID 0x0000195c (Bonding-H2O)
    0x0805a0d8,  # CID 0x000019b1 (Photon Generator Unit)
    0x0805a0dc,  # gDuelPhaseFlags = 0x0201b290
]
BLOCK1_NAME  = 'tick_bonding_or_photon_activation_seq'
BLOCK1_PLATE = (
    'tick_bonding_or_photon_activation_seq @ 0x0805a0ac\n'
    '5-state equip-activation dispatcher for Bonding-H2O (CID 0x195c) and\n'
    'Photon Generator Unit (CID 0x19b1) card pairs.\n'
    'THUMB+1 refs: 0x0805a0ad at CID dispatch table 0x9e42ca4 (0x195c) + 0x9e42f74 (0x19b1).\n'
    'Reads [gDuelPhaseFlags + EQUIP_ACTIVATION_STEP_OFF(0x4ac)]; state=0..4.\n'
    'If state > 4: returns 1 (sequence complete).\n'
    'Otherwise: loads tick_bonding_photon_state_table raw entry, branches via raw-addr dispatch.\n'
    'Dead code: sets r5=3 if CID==0x195c else r5=2; r5 never used after (compiler artifact).\n'
    'Literal pool at 0x0805a0d4: CID_H2O=0x195c, CID_PHOTON=0x19b1, gDuelPhaseFlags=0x0201b290.\n'
    'Dispatch table at 0x0805a0e4 (PTR_DAT_0805a0e4, renamed tick_bonding_photon_state_table):\n'
    '  5 raw-ptr entries (non-THUMB+1, lsb=0) for state handlers 0..4 in Block2.\n'
    'Returns u32 (0=in-progress, 1=complete).'
)

# =========================================================================
# Block2: 5 THUMB sub-fns @ 0x0805a0f8..0x0805a1db (ROM_INCBIN 0x5a0f8 0xe4)
#   Reached via raw-addr dispatch from tick_bonding_or_photon_activation_seq
#   (dispatch table at 0x0805a0e4 uses raw ptrs, NOT THUMB+1; dispatcher uses mov-pc-style)
# =========================================================================
BLOCK2_LO = 0x0805a0f8
BLOCK2_HI = 0x0805a1db  # inclusive: 0x0805a0f8 + 0xe4 - 1
BLOCK2_ENTRIES = [
    (0x0805a0f8, 'tick_bonding_photon_state0_start_lp_bar',
     'tick_bonding_photon_state0_start_lp_bar @ 0x0805a0f8\n'
     'Bonding/Photon state-machine handler: state 0 (start LP bar display).\n'
     'Reached via raw-addr dispatch from tick_bonding_or_photon_activation_seq.\n'
     'Calls increment_lp_bar_display_counter; advances step counter; returns 0.\n'
     'Dispatch table ref: tick_bonding_photon_state_table[0] = 0x0805a0f8 (raw ptr, lsb=0).\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x0805a118, 'tick_bonding_photon_state1_trigger_display',
     'tick_bonding_photon_state1_trigger_display @ 0x0805a118\n'
     'Bonding/Photon state-machine handler: state 1 (trigger card display).\n'
     'Reached via raw-addr dispatch from tick_bonding_or_photon_activation_seq.\n'
     'Reads player_id from context; calls trigger_card_display_op31_if_not_active(player, 0x12);\n'
     'advances step counter; returns 0.\n'
     'Dispatch table ref: tick_bonding_photon_state_table[1] = 0x0805a118 (raw ptr, lsb=0).\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x0805a134, 'tick_bonding_photon_state2_set_activation',
     'tick_bonding_photon_state2_set_activation @ 0x0805a134\n'
     'Bonding/Photon state-machine handler: state 2 (set equip activation state).\n'
     'Reached via raw-addr dispatch from tick_bonding_or_photon_activation_seq.\n'
     'Reads player_id; calls set_equip_activation_state_by_mode(player, 1,\n'
     '  set_equip_activation_state_by_mode_alt+1); advances step; returns 0.\n'
     'Dispatch table ref: tick_bonding_photon_state_table[2] = 0x0805a134 (raw ptr, lsb=0).\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x0805a148, 'tick_bonding_photon_state3_confirm_sprite',
     'tick_bonding_photon_state3_confirm_sprite @ 0x0805a148\n'
     'Bonding/Photon state-machine handler: state 3 (confirm sprite display).\n'
     'Reached via raw-addr dispatch from tick_bonding_or_photon_activation_seq.\n'
     'Calls check_activation_display_state_is_confirmed;\n'
     '  if confirmed: reads gP1LP+ELIGIB_SPRITE_CTRL_OFF/ELIGIB_ANIM_STATE_OFF;\n'
     '    calls submit_equip_sprite_if_slot_eligible; advances step.\n'
     '  else: step-- (retry next frame).\n'
     'Returns 0.\n'
     'Dispatch table ref: tick_bonding_photon_state_table[3] = 0x0805a148 (raw ptr, lsb=0).\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),

    (0x0805a1cc, 'tick_bonding_photon_state4_end_lp_bar',
     'tick_bonding_photon_state4_end_lp_bar @ 0x0805a1cc\n'
     'Bonding/Photon state-machine handler: state 4 (end LP bar display).\n'
     'Reached via raw-addr dispatch from tick_bonding_or_photon_activation_seq.\n'
     'Calls decrement_lp_bar_display_counter; returns 1 (sequence complete).\n'
     'Dispatch table ref: tick_bonding_photon_state_table[4] = 0x0805a1cc (raw ptr, lsb=0).\n'
     'Uses shared caller stack frame from Block1 dispatcher.'),
]


def main():
    print("=== DisassembleF06Seg9Blocks (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()

    # =====================================================================
    # Block1: tick_bonding_or_photon_activation_seq
    # =====================================================================
    print("\n--- Block1: %s @ 0x%08x ---" % (BLOCK1_NAME, BLOCK1_ENTRY))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI))
        print("[dry] disasm @ 0x%08x (skip 2-byte pad at 0x%08x)" % (BLOCK1_ENTRY, BLOCK1_CLEAR_LO))
        for p in BLOCK1_POOL:
            print("[dry] createDWord @ 0x%08x" % p)
        print("[dry] createFunction + setName '%s'" % BLOCK1_NAME)
        print("[dry] setPlateComment (%d chars)" % len(BLOCK1_PLATE))
    else:
        _clear_and_set_thumb(BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI)
        _disasm_at(BLOCK1_ENTRY, BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI)
        for p in BLOCK1_POOL:
            _create_dword(p)
        _create_fn_or_label(BLOCK1_ENTRY, BLOCK1_NAME)
        _set_plate(BLOCK1_ENTRY, BLOCK1_PLATE)
        n = _count_instrs(BLOCK1_CLEAR_LO, BLOCK1_CLEAR_HI)
        print("[ok ] Block1: %d instructions" % n)

    # =====================================================================
    # Block2: 5 sub-fns (ROM_INCBIN 0x5a0f8 0xe4)
    # =====================================================================
    print("\n--- Block2: sub-fns 0x%08x..0x%08x ---" % (BLOCK2_LO, BLOCK2_HI))
    if DRY:
        print("[dry] clearListing+setTMode(0x%08x..0x%08x)" % (BLOCK2_LO, BLOCK2_HI))
        for ep, lbl, plate in BLOCK2_ENTRIES:
            print("[dry] disasm @ 0x%08x label=%s" % (ep, lbl))
            print("[dry] setPlateComment @ 0x%08x (%d chars)" % (ep, len(plate)))
    else:
        _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
        ok_count = 0
        for ep_int, ep_label, ep_plate in BLOCK2_ENTRIES:
            if _disasm_at(ep_int, BLOCK2_LO, BLOCK2_HI):
                ok_count += 1
            ep_addr = _addr(ep_int)
            try:
                sm.createLabel(ep_addr, ep_label, SourceType.USER_DEFINED)
                print("[ok ] label '%s' @ 0x%08x" % (ep_label, ep_int))
            except Exception as le:
                print("[warn] label @ 0x%08x: %s" % (ep_int, le))
            fn = fm.getFunctionAt(ep_addr)
            if fn is None:
                fn = createFunction(ep_addr, ep_label)
                if fn is not None:
                    print("[FN ] created: %s @ 0x%08x" % (ep_label, ep_int))
                else:
                    print("[FN ] label-only: %s @ 0x%08x" % (ep_label, ep_int))
            else:
                fn.setName(ep_label, SourceType.USER_DEFINED)
                print("[FN ] renamed: %s @ 0x%08x" % (ep_label, ep_int))
            _set_plate(ep_int, ep_plate)
        n_total = _count_instrs(BLOCK2_LO, BLOCK2_HI)
        print("[ok ] Block2: %d/%d stubs disasmd, %d instructions total" % (
            ok_count, len(BLOCK2_ENTRIES), n_total))

    print("\n=== DisassembleF06Seg9Blocks DONE (DRY=%s) ===" % DRY)


main()
