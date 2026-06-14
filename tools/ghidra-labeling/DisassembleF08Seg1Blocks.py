# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg1Blocks.py -- F08 Seg-1 R4 disasm (2 blocks, 2 new functions)
#
# Block1: 0x0806456c..0x08064597 (0x2c B)
#   fn entry @ 0x0806456c: check_opponent_chain_zone_count_gt1_for_cid_19df
#   fn_eligible for: CID=0x19df (Success Probability 0%) via handler table 0x09e43078
#   Code: 0x6456c..0x6458b (0x20 B incl branch targets); zero pad 0x6458a..0x6458b (2B)
#   Lit pool: 0x6458c(gP1LifePoints=0x0201c4e0), 0x64590(PLAYER_BLOCK_STRIDE=0x00000868)
#   Semantics: reads gP1ChainZoneCountBase (gP1LifePoints+0x18) + opp*0x868;
#              returns 1 if opponent chain zone count >1, else 0
#   Key: ADDS r2,#0x18 at 0x6457c -> r2 = gP1LifePoints+0x18 = gP1ChainZoneCountBase
#
# Block2: 0x080645ee..0x0806460b (0x1e B)
#   2B alignment pad at 0x080645ee (.hword 0x0000)
#   fn entry @ 0x080645f0: check_alt_hand_sum_nonzero_for_cid_19ef
#   fn_eligible for: CID=0x19ef (Elemental Hero Erikshieler) via handler table 0x09e45580
#   Code: 0x645f0..0x64603 (0x14 B)
#   Lit pool: 0x64604(gP1LifePoints=0x0201c4e0), 0x64608(0x00000884=P2 alt-hand stride)
#   Semantics: sums [gP1LifePoints+0x1c] + [gP1LifePoints+0x884]; returns 1 if nonzero
#   0x884 = PLAYER_BLOCK_STRIDE(0x868) + gP1AltHandCountBase_offset(0x1c) = P2 alt-hand field
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_215427-pre-F08Seg1

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType, RefType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType, WordDataType
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
    """Disassemble at addr using flow continuation."""
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


def _create_word_raw(slot_addr, label_name, eol=None):
    """Force a WORD (2B) at slot_addr with plain label, optional EOL."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a.add(1))
    except Exception:
        pass
    listing.createData(a, WordDataType.dataType)
    createLabel(a, label_name, True, SourceType.USER_DEFINED)
    if eol:
        cu = listing.getCodeUnitAt(a)
        if cu is not None:
            bad = any(ord(ch) > 127 for ch in eol)
            if not bad:
                cu.setComment(CodeUnit.EOL_COMMENT, eol)
    print("[WD+LBL] 0x%08x -> %s" % (slot_addr, label_name))


# ---------------------------------------------------------------------------
# BLOCK1: 0x0806456c..0x08064597 (0x2c B)
#   fn entry @ 0x0806456c (no leading pad)
# ---------------------------------------------------------------------------
BLOCK1_LO  = 0x0806456c
BLOCK1_HI  = 0x08064597
BLOCK1_FN  = (0x0806456c, 'check_opponent_chain_zone_count_gt1_for_cid_19df')
BLOCK1_POOL = [
    (0x0806458c, 'gp1lp_ptr_0806458c',    'gP1LifePoints',       0x0201c4e0,
     'gP1LifePoints base for gP1ChainZoneCountBase (+0x18)'),
    (0x08064590, 'player_stride_08064590', 'PLAYER_BLOCK_STRIDE', 0x00000868,
     'PLAYER_BLOCK_STRIDE = 0x868'),
]
BLOCK1_PLATE = (
    'fn_eligible for CID=0x19df (Success Probability 0%). '
    'Reached via card effect handler dispatch table at ROM 0x09e4306c (entry start). '
    'fn_eligible+1 = 0x0806456d stored at ROM 0x09e43078. '
    'Reads gP1ChainZoneCountBase (gP1LifePoints+0x18) + opponent_id * PLAYER_BLOCK_STRIDE. '
    'player_id extracted from slot byte[+2] bit0; opponent = 1-player_id. '
    'Returns 1 if opponent chain zone count > 1, else 0. '
    'ADDS r2,#0x18 at 0x0806457c: r2 = gP1LifePoints+0x18 = gP1ChainZoneCountBase. '
    'Lit pool @ 0x0806458c: gP1LifePoints(0x0201c4e0) / PLAYER_BLOCK_STRIDE(0x868).'
)
BLOCK1_ALIGN_PAD = 0x0806458a  # 2B alignment pad between code and lit pool

# ---------------------------------------------------------------------------
# BLOCK2: 0x080645ee..0x0806460b (0x1e B)
#   2B alignment pad at 0x080645ee, fn entry @ 0x080645f0
# ---------------------------------------------------------------------------
BLOCK2_LO  = 0x080645ee
BLOCK2_HI  = 0x0806460b
BLOCK2_FN  = (0x080645f0, 'check_alt_hand_sum_nonzero_for_cid_19ef')
BLOCK2_POOL = [
    (0x08064604, 'gp1lp_ptr_08064604',    'gP1LifePoints',       0x0201c4e0,
     'gP1LifePoints base for P1+P2 alt-hand sum'),
    (0x08064608, 'p2_alt_hand_stride_08064608', None, 0x00000884,
     '0x884 = PLAYER_BLOCK_STRIDE(0x868) + gP1AltHandCountBase_offset(0x1c); P2 alt-hand field'),
]
BLOCK2_PLATE = (
    'fn_eligible for CID=0x19ef (Elemental Hero Erikshieler). '
    'Reached via card effect handler dispatch table at ROM 0x09e45574 (entry start). '
    'fn_eligible+1 = 0x080645f1 stored at ROM 0x09e45580. '
    '2B alignment pad at 0x080645ee; fn entry at 0x080645f0. '
    'Reads [gP1LifePoints+0x1c] (P1 alt-hand count) and [gP1LifePoints+0x884] (P2 alt-hand count). '
    '0x884 = PLAYER_BLOCK_STRIDE(0x868) + gP1AltHandCountBase_offset(0x1c). '
    'Sums both fields; returns 1 if sum nonzero, else 0. '
    'Lit pool @ 0x08064604: gP1LifePoints(0x0201c4e0). '
    'Lit pool @ 0x08064608: 0x00000884 (P2 alt-hand stride offset).'
)


def main():
    print("=== DisassembleF08Seg1Blocks (DRY=%s) ===" % DRY)

    if DRY:
        print("[dry] Would process 2 blocks, 2 functions:")
        print("  Block1 0x%08x..0x%08x fn@0x%08x" % (BLOCK1_LO, BLOCK1_HI, BLOCK1_FN[0]))
        print("  Block2 0x%08x..0x%08x fn@0x%08x (2B pad at 0x%08x)" % (
            BLOCK2_LO, BLOCK2_HI, BLOCK2_FN[0], BLOCK2_LO))
        print("[dry] Literal pool slots: 4 total (3 EQ + 1 raw label)")
        return

    # =========================================================================
    # Block1: 0x0806456c..0x08064597 (1 fn, no leading pad)
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (fn@0x%08x) ---" % (BLOCK1_LO, BLOCK1_HI, BLOCK1_FN[0]))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    _disasm_flow(BLOCK1_FN[0])
    # Mark 2B alignment pad between code and literal pool
    _set_eol(BLOCK1_ALIGN_PAD, 'alignment pad 2B before literal pool')
    # Literal pool slots
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
             'cid_19df = Success Probability 0%; fn_eligible at handler table 0x09e4306c; '
             'reads gP1ChainZoneCountBase+opp*0x868, returns 1 if >1')

    # =========================================================================
    # Block2: 0x080645ee..0x0806460b (2B pad + 1 fn)
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (2B pad@0x%08x + fn@0x%08x) ---" % (
        BLOCK2_LO, BLOCK2_HI, BLOCK2_LO, BLOCK2_FN[0]))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    # Mark 2B alignment pad at start of block
    _create_word_raw(BLOCK2_LO, 'pad_080645ee', 'alignment padding 2B before fn entry 0x080645f0')
    # Set THUMB mode only for the code range (after the pad)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        lo_fn = _addr(BLOCK2_FN[0])
        hi_fn = _addr(BLOCK2_HI)
        ctx.setValue(tmode, lo_fn, hi_fn, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x (fn range only)" % (BLOCK2_FN[0], BLOCK2_HI))
    _disasm_flow(BLOCK2_FN[0])
    # Literal pool slots
    for entry in BLOCK2_POOL:
        sp, ln, cn, val = entry[0], entry[1], entry[2], entry[3]
        eol = entry[4] if len(entry) > 4 else None
        if cn is not None:
            _create_dword_eq(sp, ln, cn, val, eol)
        else:
            _create_dword_raw(sp, ln, eol)
    _create_function(BLOCK2_FN[0], BLOCK2_FN[1])
    _set_plate(BLOCK2_FN[0], BLOCK2_PLATE)
    _set_eol(BLOCK2_FN[0],
             'cid_19ef = Elemental Hero Erikshieler; fn_eligible at handler table 0x09e45574')

    print("\n=== DisassembleF08Seg1Blocks DONE ===")
    print("  2 functions created across 2 blocks")
    print("  4 literal pool slots (3 EQ + 1 raw label)")
    print("  Block1: no leading pad; Block2: 2B pad at 0x080645ee")


main()
