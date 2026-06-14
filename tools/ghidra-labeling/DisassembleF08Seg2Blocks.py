# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg2Blocks.py -- F08 Seg-2 R4 disasm (3 blocks, 17+ new functions)
#
# Block1: 0x08065d78..0x08065db3 (0x3c = 60B)
#   fn entry @ 0x08065d78: check_equip_eligible_state_dispatch_for_time_wizard
#   fn_eligible for: CID=0x0fb6 (Time Wizard) via handler table at 0x09e4631c
#   Code: 0x65d78..0x65da7 + lit pool 0x65da8..0x65db3
#   Semantics: checks slot[+4].bit2 (block flag); reads gDuelPhaseFlags[0x4a0]
#              state code (0x94<<3); subtracts 0x5f; dispatches via 34-entry
#              raw-address jump table at 0x08065db4 (states 0x5f..0x80)
#   Lit pool: 0x65da8(-768/0xfffffd00), 0x65dac(gDuelPhaseFlags=0x0201b290), 0x65db0(0x08065db4=table)
#
# Block2: 0x08065e3c..0x080660d7 (0x29c = 668B)
#   12 sub-fn stubs reached via raw-address bx dispatch from table at 0x08065db4..0x08065e3b
#   (34-entry .word table already in asm, pointing to these 12 unique entry points)
#   fn entries:
#     0x08065e3c: equip_state_stub_80_time_wizard  (state 0x80)
#     0x08065e76: equip_state_stub_7f_time_wizard  (state 0x7f)
#     0x08065e98: equip_state_stub_7e_time_wizard  (state 0x7e)
#     0x08065f58: equip_state_stub_78_time_wizard  (state 0x78)
#     0x08065fb8: equip_state_stub_77_time_wizard  (state 0x77)
#     0x08066004: equip_state_stub_6d_time_wizard  (state 0x6d)
#     0x08066038: equip_state_stub_64_time_wizard  (state 0x64)
#     0x0806604c: equip_state_stub_63_time_wizard  (state 0x63)
#     0x08066066: equip_state_stub_61_time_wizard  (state 0x61)
#     0x0806608c: equip_state_stub_60_time_wizard  (state 0x60)
#     0x080660a4: equip_state_stub_5f_time_wizard  (state 0x5f)
#     0x080660c8: equip_state_stub_default_time_wizard  (state 0x62+/default: movs r0,#0)
#
# Block3: 0x080662a4..0x0806630b (0x68 = 104B)
#   5 case stubs for dispatch_equip_chain_state_by_slot_ownership
#   jump table at 0x08066230 (within asm, 29 entries, base addr + bx r0)
#   fn entries:
#     0x080662a4: equip_chain_state_stub_80  (state 0x80)
#     0x080662d2: equip_chain_state_stub_7e  (state 0x7e)
#     0x080662ea: equip_chain_state_stub_7d  (state 0x7d)
#     0x080662fa: equip_chain_state_stub_78  (state 0x78)
#     0x08066306: equip_chain_state_stub_64  (state 0x64)
#
# Block 3 ends at 0x0806630b; next fn LAB_0806630c already in asm.
# No literal pool createDWord needed for Blocks 2 and 3 (sub-fns have inline lit pools
# reachable via flow disasm; only Block1 has explicit lit pool entries).
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_232422-pre-F08Seg2

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType
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


def _disasm_flow(addr):
    """Disassemble at addr using flow continuation (single DisassembleCommand)."""
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
    """Create a named function at addr."""
    a = _addr(addr)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed existing function at 0x%08x -> %s" % (addr, name))
        else:
            print("[FN ] function already exists at 0x%08x: %s" % (addr, name))
        return
    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr))
    else:
        print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] created label (fallback) %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
    """Set PLATE_COMMENT. text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in text)
    if bad:
        print("[PLATE FAIL] non-ASCII in plate @ 0x%08x -- skipping" % addr)
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr))
    if cu is None:
        print("[PLATE FAIL] no CodeUnit at 0x%08x" % addr)
        return
    cu.setComment(CodeUnit.PLATE_COMMENT, text)
    print("[PLATE ok] 0x%08x (%d chars)" % (addr, len(text)))


def _set_eol(addr, text):
    """Set EOL_COMMENT. text must be pure ASCII."""
    bad = any(ord(ch) > 127 for ch in text)
    if bad:
        print("[EOL FAIL] non-ASCII in EOL @ 0x%08x -- skipping" % addr)
        return
    listing = currentProgram.getListing()
    cu = listing.getCodeUnitAt(_addr(addr))
    if cu is None:
        print("[EOL WARN] no CodeUnit at 0x%08x" % addr)
        return
    cu.setComment(CodeUnit.EOL_COMMENT, text)
    print("[EOL ok] 0x%08x: %s" % (addr, text[:60]))


def _create_dword_eq(slot_addr, label_name, const_name, value, eol=None):
    """Force a DWORD at slot_addr, set label, add equate, optional EOL."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    et = currentProgram.getEquateTable()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    eq = et.getEquate(const_name)
    if eq is None:
        eq = et.createEquate(const_name, value)
    eq.addReference(a, 0)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if not bad:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[DW+EQ] 0x%08x -> %s (%s=0x%x)" % (slot_addr, label_name, const_name, value))


def _create_dword_raw(slot_addr, label_name, eol=None):
    """Force a DWORD at slot_addr with plain label (no equate), optional EOL."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a.add(3))
    except Exception:
        pass
    listing.createData(a, DWordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if not bad:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[DW+LBL] 0x%08x -> %s" % (slot_addr, label_name))


# ===========================================================================
# BLOCK 1: 0x08065d78..0x08065db3 (0x3c = 60B)
#   fn entry @ 0x08065d78: check_equip_eligible_state_dispatch_for_time_wizard
# ===========================================================================
BLOCK1_LO   = 0x08065d78
BLOCK1_HI   = 0x08065db3
BLOCK1_FN   = (0x08065d78, 'check_equip_eligible_state_dispatch_for_time_wizard')
# Literal pool at 0x65da8..0x65db3 (3 DWORD entries)
BLOCK1_POOL = [
    # 0x65da8: 0xfffffd00 = -768 (unknown literal; no equate, plain label)
    (0x08065da8, 'lit_pool_neg768_08065da8', None, 0xfffffd00,
     '0xfffffd00=-768 (unknown literal in fn_eligible check; usage context TBD)'),
    # 0x65dac: gDuelPhaseFlags = 0x0201b290
    (0x08065dac, 'lit_pool_phase_flags_08065dac', 'gDuelPhaseFlags', 0x0201b290,
     'gDuelPhaseFlags base: reads [+0x4a0] = 0x94<<3 for phase state code'),
    # 0x65db0: dispatch table base 0x08065db4
    (0x08065db0, 'lit_pool_dispatch_tbl_08065db0', None, 0x08065db4,
     '34-entry raw-addr dispatch table base at 0x08065db4 (states 0x5f..0x80)'),
]
BLOCK1_PLATE = (
    'fn_eligible for CID=0x0fb6 (Time Wizard, pw=71625222). '
    'Reached via card effect handler table at ROM 0x09e4631c: '
    '[+0x0]=fn_activate+1 [+0x8]=CID=0x0fb6 [+0xc]=fn_eligible+1=0x08065d79. '
    'Checks slot[+4].bit2 (block flag); if set returns 0. '
    'Reads gDuelPhaseFlags[0x4a0] (= 0x94<<3) for equip phase state code. '
    'Subtracts base 0x5f; checks in range [0..0x21] (states 0x5f..0x80 = 34). '
    'Dispatches via 34-entry raw-addr jump table at 0x08065db4 (bx, not THUMB+1). '
    '12 unique case stubs in Block2 (0x65e3c..0x660d7); remainder default to 0. '
    'Lit pool: 0x65da8(0xfffffd00=-768), 0x65dac(gDuelPhaseFlags), 0x65db0(table_base).'
)

# ===========================================================================
# BLOCK 2: 0x08065e3c..0x080660d7 (0x29c = 668B)
#   12 sub-fn stubs dispatched via raw-addr bx from table at 0x08065db4
# ===========================================================================
BLOCK2_LO   = 0x08065e3c
BLOCK2_HI   = 0x080660d7
# 12 entry points for DisassembleCommand (one per stub; raw-addr dispatch not THUMB+1)
# Must disassemble each individually to ensure all stubs are decoded
BLOCK2_FNS = [
    (0x08065e3c, 'equip_state_stub_80_time_wizard',
     'state=0x80 handler: Time Wizard equip effect (dispatch via table at 0x65db4)'),
    (0x08065e76, 'equip_state_stub_7f_time_wizard',
     'state=0x7f handler: Time Wizard equip effect'),
    (0x08065e98, 'equip_state_stub_7e_time_wizard',
     'state=0x7e handler: Time Wizard equip effect'),
    (0x08065f58, 'equip_state_stub_78_time_wizard',
     'state=0x78 handler: Time Wizard equip effect'),
    (0x08065fb8, 'equip_state_stub_77_time_wizard',
     'state=0x77 handler: Time Wizard equip effect'),
    (0x08066004, 'equip_state_stub_6d_time_wizard',
     'state=0x6d handler: Time Wizard equip effect'),
    (0x08066038, 'equip_state_stub_64_time_wizard',
     'state=0x64 handler: Time Wizard equip effect'),
    (0x0806604c, 'equip_state_stub_63_time_wizard',
     'state=0x63 handler: Time Wizard equip effect'),
    (0x08066066, 'equip_state_stub_61_time_wizard',
     'state=0x61 handler: Time Wizard equip effect'),
    (0x0806608c, 'equip_state_stub_60_time_wizard',
     'state=0x60 handler: Time Wizard equip effect'),
    (0x080660a4, 'equip_state_stub_5f_time_wizard',
     'state=0x5f handler: Time Wizard equip effect'),
    (0x080660c8, 'equip_state_stub_default_time_wizard',
     'default handler (state=0x62+ unmapped): returns 0 via movs r0,#0; bx lr'),
]
BLOCK2_PLATE_FMT = (
    '%s: Time Wizard (CID=0x0fb6) equip phase state handler. '
    'Reached via raw-addr bx dispatch from table at 0x08065db4 (34 entries, states 0x5f..0x80). '
    'Entry via check_equip_eligible_state_dispatch_for_time_wizard (Block1 0x08065d78). '
    '%s'
)

# ===========================================================================
# BLOCK 3: 0x080662a4..0x0806630b (0x68 = 104B)
#   5 case stubs for dispatch_equip_chain_state_by_slot_ownership
# ===========================================================================
BLOCK3_LO   = 0x080662a4
BLOCK3_HI   = 0x0806630b
BLOCK3_FNS = [
    (0x080662a4, 'equip_chain_state_stub_80',
     'state=0x80 case: dispatch_equip_chain_state_by_slot_ownership case handler'),
    (0x080662d2, 'equip_chain_state_stub_7e',
     'state=0x7e case: dispatch_equip_chain_state_by_slot_ownership case handler'),
    (0x080662ea, 'equip_chain_state_stub_7d',
     'state=0x7d case: dispatch_equip_chain_state_by_slot_ownership case handler'),
    (0x080662fa, 'equip_chain_state_stub_78',
     'state=0x78 case: dispatch_equip_chain_state_by_slot_ownership case handler'),
    (0x08066306, 'equip_chain_state_stub_64',
     'state=0x64 case: dispatch_equip_chain_state_by_slot_ownership case handler'),
]
BLOCK3_PLATE_FMT = (
    '%s: dispatch_equip_chain_state_by_slot_ownership (0x080661fc) case handler. '
    'Reached via raw-addr bx r0 jump table at 0x08066230 (29 entries). '
    '%s'
)
# add a label for the jump table if not already named
BLOCK3_JUMP_TABLE_LABEL = (0x08066230, 'dispatch_equip_chain_state_jump_table')


def main():
    print("=== DisassembleF08Seg2Blocks (DRY=%s) ===" % DRY)
    print("  Block1: 0x%08x..0x%08x (1 fn + lit pool)" % (BLOCK1_LO, BLOCK1_HI))
    print("  Block2: 0x%08x..0x%08x (12 sub-fn stubs)" % (BLOCK2_LO, BLOCK2_HI))
    print("  Block3: 0x%08x..0x%08x (5 chain-state stubs)" % (BLOCK3_LO, BLOCK3_HI))
    total_fns = 1 + len(BLOCK2_FNS) + len(BLOCK3_FNS)
    print("  Total: %d new functions" % total_fns)

    if DRY:
        print("[dry] Block1 fn: %s @ 0x%08x" % (BLOCK1_FN[1], BLOCK1_FN[0]))
        for addr, name, _ in BLOCK2_FNS:
            print("[dry] Block2 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK3_FNS:
            print("[dry] Block3 fn: %s @ 0x%08x" % (name, addr))
        return

    # =========================================================================
    # Block1: 0x08065d78..0x08065db3 (1 fn + 3 lit pool DWORDs)
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (fn@0x%08x) ---" % (
        BLOCK1_LO, BLOCK1_HI, BLOCK1_FN[0]))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    _disasm_flow(BLOCK1_FN[0])
    # Literal pool DWORDs (force split so flow stops at code boundary)
    for entry in BLOCK1_POOL:
        sp, ln, cn, val = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if cn is not None:
            _create_dword_eq(sp, ln, cn, val, eol)
        else:
            _create_dword_raw(sp, ln, eol)
    _create_function(BLOCK1_FN[0], BLOCK1_FN[1])
    _set_plate(BLOCK1_FN[0], BLOCK1_PLATE)
    _set_eol(BLOCK1_FN[0],
             'CID=0x0fb6 Time Wizard fn_eligible; state dispatch table 0x65db4 (34 entries, 0x5f..0x80)')

    # =========================================================================
    # Block2: 0x08065e3c..0x080660d7 (12 sub-fn stubs via raw-addr dispatch)
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (12 sub-fn stubs) ---" % (BLOCK2_LO, BLOCK2_HI))
    # Clear and set THUMB for entire block range first
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    # Disassemble each entry point individually (raw-addr dispatch, not flow-reachable from Block1)
    for addr, name, plate_detail in BLOCK2_FNS:
        _disasm_flow(addr)
    # Create functions and set plates
    for addr, name, plate_detail in BLOCK2_FNS:
        _create_function(addr, name)
        plate_text = BLOCK2_PLATE_FMT % (name, plate_detail)
        _set_plate(addr, plate_text)
    print("  Block2: %d stubs created" % len(BLOCK2_FNS))

    # =========================================================================
    # Block3: 0x080662a4..0x0806630b (5 chain-state stubs)
    # =========================================================================
    print("\n--- Block3: 0x%08x..0x%08x (5 chain-state stubs) ---" % (BLOCK3_LO, BLOCK3_HI))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)
    # Add label for the jump table (within asm, not in block)
    sym_tbl = currentProgram.getSymbolTable()
    a_tbl = _addr(BLOCK3_JUMP_TABLE_LABEL[0])
    existing_tbl = sym_tbl.getSymbols(a_tbl)
    tbl_names = [s.getName() for s in existing_tbl]
    if BLOCK3_JUMP_TABLE_LABEL[1] not in tbl_names:
        sym_tbl.createLabel(a_tbl, BLOCK3_JUMP_TABLE_LABEL[1], SourceType.USER_DEFINED)
        print("[LBL] added jump table label %s @ 0x%08x" % (
            BLOCK3_JUMP_TABLE_LABEL[1], BLOCK3_JUMP_TABLE_LABEL[0]))
    # Disassemble each entry point
    for addr, name, plate_detail in BLOCK3_FNS:
        _disasm_flow(addr)
    # Create functions and set plates
    for addr, name, plate_detail in BLOCK3_FNS:
        _create_function(addr, name)
        plate_text = BLOCK3_PLATE_FMT % (name, plate_detail)
        _set_plate(addr, plate_text)
    print("  Block3: %d stubs created" % len(BLOCK3_FNS))

    print("\n=== DisassembleF08Seg2Blocks DONE ===")
    print("  %d total new functions" % total_fns)
    print("  Block1: 1 fn + 3 lit pool DWORDs")
    print("  Block2: %d sub-fn stubs (12 unique states for Time Wizard)" % len(BLOCK2_FNS))
    print("  Block3: %d case stubs (dispatch_equip_chain_state)" % len(BLOCK3_FNS))


main()
