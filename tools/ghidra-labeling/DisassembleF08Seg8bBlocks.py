# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg8bBlocks.py -- F08 Seg-8b R4 disasm (5 blocks)
#
# Block1: 0x0806b784..0x0806b7cf (0x4c B)
#   fn_eligible handler for CID=0x135b (unassigned); THUMB+1 ref @0x1e40448
#   Literal pool at 0x6b7cc: .word gDuelPhaseFlags; .word 0x0806b7d4 (at 0x6b7d0, outside block)
#   1 function: check_equip_eligible_cid_135b @ 0x0806b784
#
# Block2: 0x0806b7fc..0x0806ba77 (0x27c B)
#   10-entry raw-addr jump table at 0x0806b7d4..0x0806b7f8 dispatches stubs in this block
#   raw ref @0x6b7f8 (table entry[9] = block start)
#   10 unique entry points
#
# Block3: 0x0806bb74..0x0806bbb7 (0x44 B)
#   fn_eligible handler for CID=0x1362 (Magical Hats); THUMB+1 ref @0x1e40490
#   Literal pool at 0x6bbb0: .word gDuelPhaseFlags; .word 0x0806bbb8 (ptr to 29-entry table)
#   1 function: check_equip_eligible_magical_hats @ 0x0806bb74
#
# Block4: 0x0806bc2c..0x0806bf9f (0x374 B)
#   29-entry raw-addr jump table at 0x0806bbb8..0x0806bc28 dispatches stubs in this block
#   raw ref @0x6bc28 (table entry[28] = block start)
#   11 unique entry points
#   NESTED: literal pool at 0x6bf9c (offset 0x370) -> 7-entry sub-table at 0x6bfa0..0x6bfb8
#   createDWord at 0x6bf9c and 0x6bfa0..0x6bfb8 to force split before disasm
#
# Block5: 0x0806bfbc..0x0806c0cb (0x110 B)
#   7-entry sub-dispatch table at 0x0806bfa0..0x0806bfb8 (nested within Block4 literal pool region)
#   raw ref @0x6bfb8 (table entry[6] = block start)
#   7 unique entry points
#
# NOTE: Each block uses clearListing + setTMode(THUMB) on full range first,
#   then individual DisassembleCommand per entry point (single-range only disasms first stub).
#   Nested literal pool words use createDWord to force split before disasm.
#
# NOTE: All plate text is pure ASCII (no CJK). Jython CJK = double-UTF-8 mojibake.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_053928-pre-F08Seg8b

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
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


def _create_dword(addr):
    """Force a DWORD data item at addr to split any existing code/data."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    existing = listing.getCodeUnitAt(a)
    if existing is not None:
        try:
            clearListing(a, a)
        except Exception as e:
            print("[warn] clearListing for dword at 0x%08x: %s" % (addr, e))
    try:
        listing.createData(a, DWordDataType.dataType)
        print("[DWORD] created at 0x%08x" % addr)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr, e))


def _disasm_flow(addr):
    lo = _addr(addr)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm_flow 0x%08x: %s" % (addr, cmd.getStatusMsg()))
        return False
    return True


def _create_function(addr, name):
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
        print("[FN ] label fallback %s @ 0x%08x" % (name, addr))


def _set_plate(addr, text):
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


# ===========================================================================
# BLOCK 1: 0x0806b784..0x0806b7cf (0x4c B)
#   fn_eligible handler for CID=0x135b
#   THUMB+1 ref @0x1e40448 -> 0x0806b785 = block+1
#   1 function
# ===========================================================================
BLOCK1_LO = 0x0806b784
BLOCK1_HI = 0x0806b7cf

BLOCK1_FNS = [
    (0x0806b784, 'check_equip_eligible_cid_135b',
     'fn_eligible handler for CID=0x135b (unassigned slot; neighbor: 0x135c=Ceasefire). '
     'THUMB+1 ref at dispatch table @0x1e40448: entry+0=CID=0x135b, entry+4=0x0806b785 (fn_eligible+1). '
     'Reads gDuelPhaseFlags+0x4a0 state; dispatches via 10-entry raw-addr table cid_135b_dispatch_jump_table at 0x0806b7d4. '
     'Block range 0x0806b784..0x0806b7cf.'),
]

# ===========================================================================
# BLOCK 2: 0x0806b7fc..0x0806ba77 (0x27c B)
#   10-entry raw-addr jump table at 0x0806b7d4..0x0806b7f8
#   raw ref @0x6b7f8 (table[9] = block start 0x0806b7fc)
#   10 unique entry points
# ===========================================================================
BLOCK2_LO = 0x0806b7fc
BLOCK2_HI = 0x0806ba77

BLOCK2_FNS = [
    # Ordered by stub address (not table index)
    (0x0806b7fc, 'cid_135b_state_stub_b7fc',
     'Default/case9 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table (0x0806b7d4) entry[9] at 0x0806b7f8 -> 0x0806b7fc (block start). '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806b8a8, 'cid_135b_state_stub_b8a8',
     'Case8 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[8] -> 0x0806b8a8. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806b8d4, 'cid_135b_state_stub_b8d4',
     'Case7 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[7] -> 0x0806b8d4. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806b944, 'cid_135b_state_stub_b944',
     'Case6 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[6] -> 0x0806b944. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806b950, 'cid_135b_state_stub_b950',
     'Case5 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[5] -> 0x0806b950. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806b990, 'cid_135b_state_stub_b990',
     'Case4 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[4] -> 0x0806b990. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806b9f0, 'cid_135b_state_stub_b9f0',
     'Case2 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[2] -> 0x0806b9f0. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806ba00, 'cid_135b_state_stub_ba00',
     'Case1 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[1] -> 0x0806ba00. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806ba28, 'cid_135b_state_stub_ba28',
     'Case0 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[0] -> 0x0806ba28. '
     'Block range 0x0806b7fc..0x0806ba77.'),
    (0x0806ba64, 'cid_135b_state_stub_ba64',
     'Case3 stub for CID=0x135b state dispatch. '
     'cid_135b_dispatch_jump_table entry[3] -> 0x0806ba64. '
     'Block range 0x0806b7fc..0x0806ba77.'),
]

# ===========================================================================
# BLOCK 3: 0x0806bb74..0x0806bbb7 (0x44 B)
#   fn_eligible handler for CID=0x1362 Magical Hats
#   THUMB+1 ref @0x1e40490 -> 0x0806bb75 = block+1
#   Literal pool inside block:
#     0x6bbb0: .word gDuelPhaseFlags (0x0201b290)
#     0x6bbb4: .word 0x0806bbb8 (29-entry jump table immediately following)
#   1 function
# ===========================================================================
BLOCK3_LO = 0x0806bb74
BLOCK3_HI = 0x0806bbb7

BLOCK3_FNS = [
    (0x0806bb74, 'check_equip_eligible_magical_hats',
     'fn_eligible handler for CID=0x1362 (Magical Hats pw=81210420; card-stats.s card_0769). '
     'THUMB+1 ref at dispatch table @0x1e40490: entry+0=CID=0x1362, entry+4=0x0806bb75 (fn_eligible+1). '
     'Reads gDuelPhaseFlags+0x4a0 state; dispatches via 29-entry raw-addr table at 0x0806bbb8. '
     'Block range 0x0806bb74..0x0806bbb7.'),
]

# ===========================================================================
# BLOCK 4: 0x0806bc2c..0x0806bf9f (0x374 B)
#   29-entry raw-addr jump table at 0x0806bbb8..0x0806bc28
#   raw ref @0x6bc28 (table[28] = block start 0x0806bc2c)
#   11 unique entry points
#   NESTED literal pool at 0x6bf9c: .word 0x0806bfa0 (7-entry sub-table for nested dispatch)
#     sub-table entries 0x6bfa0..0x6bfb8 point into Block5 (0x0806bfbc..0x0806c0cb)
# ===========================================================================
BLOCK4_LO = 0x0806bc2c
BLOCK4_HI = 0x0806bf9f

# Nested jump table region: literal pool dword @0x6bf9c + table body @0x6bfa0..0x6bfb8
BLOCK4_NESTED_LIT_POOL = 0x0806bf9c   # createDWord here to force split
BLOCK4_NESTED_TABLE_LO = 0x0806bfa0
BLOCK4_NESTED_TABLE_HI = 0x0806bfbb   # 7 entries * 4B = 0x1c B; last entry @0x6bfb8..0x6bfbb

BLOCK4_FNS = [
    # entry[28] = block start (29-entry table; 0-indexed)
    (0x0806bc2c, 'magical_hats_state_stub_bc2c',
     'Case28/block-start stub: check_equip_eligible_magical_hats (0x0806bb74) '
     '29-entry raw-addr dispatch table entry[28] at 0x0806bc28 -> 0x0806bc2c. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bc86, 'magical_hats_state_stub_bc86',
     'Case26 stub: check_equip_eligible_magical_hats dispatch table entry[26] -> 0x0806bc86. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bc96, 'magical_hats_state_stub_bc96',
     'Case25 stub: check_equip_eligible_magical_hats dispatch table entry[25] -> 0x0806bc96. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bcaa, 'magical_hats_state_stub_bcaa',
     'Case24 stub: check_equip_eligible_magical_hats dispatch table entry[24] -> 0x0806bcaa. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bd4c, 'magical_hats_state_stub_bd4c',
     'Case23 stub: check_equip_eligible_magical_hats dispatch table entry[23] -> 0x0806bd4c. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bda8, 'magical_hats_state_stub_bda8',
     'Case22 stub: check_equip_eligible_magical_hats dispatch table entry[22] -> 0x0806bda8. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bdce, 'magical_hats_state_stub_bdce',
     'Case21 stub: check_equip_eligible_magical_hats dispatch table entry[21] -> 0x0806bdce. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bdf2, 'magical_hats_state_stub_bdf2',
     'Case20 stub: check_equip_eligible_magical_hats dispatch table entry[20] -> 0x0806bdf2. '
     'Contains nested sub-dispatch: literal pool at 0x0806bf9c -> 7-entry table at 0x0806bfa0. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bf3a, 'magical_hats_state_stub_bf3a',
     'Case10 stub: check_equip_eligible_magical_hats dispatch table entry[10] -> 0x0806bf3a. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bf4c, 'magical_hats_state_stub_bf4c',
     'Case0 stub: check_equip_eligible_magical_hats dispatch table entry[0] -> 0x0806bf4c. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
    (0x0806bf56, 'magical_hats_state_stub_default_bf56',
     'Default stub (entries 1..9,11..19,27): check_equip_eligible_magical_hats dispatch table. '
     'Majority of entries point here; handles unimplemented state indices. '
     'Block range 0x0806bc2c..0x0806bf9f.'),
]

# ===========================================================================
# BLOCK 5: 0x0806bfbc..0x0806c0cb (0x110 B)
#   7-entry sub-dispatch table at 0x0806bfa0..0x0806bfb8 (nested within Block4)
#   raw ref @0x6bfb8 (table[6] = block start 0x0806bfbc)
#   7 unique entry points
# ===========================================================================
BLOCK5_LO = 0x0806bfbc
BLOCK5_HI = 0x0806c0cb

BLOCK5_FNS = [
    # entry[6] = block start (7-entry sub-table at 0x6bfa0)
    (0x0806bfbc, 'magical_hats_zone_state_stub_bfbc',
     'Sub-entry6/block-start: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[6] at 0x0806bfb8 -> 0x0806bfbc. '
     'Sub-table reached from magical_hats_state_stub_bdf2 via literal pool at 0x0806bf9c. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
    (0x0806c050, 'magical_hats_zone_state_stub_c050',
     'Sub-entry5: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[5] at 0x0806bfb4 -> 0x0806c050. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
    (0x0806c066, 'magical_hats_zone_state_stub_c066',
     'Sub-entry4: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[4] at 0x0806bfb0 -> 0x0806c066. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
    (0x0806c080, 'magical_hats_zone_state_stub_c080',
     'Sub-entry3: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[3] at 0x0806bfac -> 0x0806c080. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
    (0x0806c08e, 'magical_hats_zone_state_stub_c08e',
     'Sub-entry2: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[2] at 0x0806bfa8 -> 0x0806c08e. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
    (0x0806c0a0, 'magical_hats_zone_state_stub_c0a0',
     'Sub-entry1: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[1] at 0x0806bfa4 -> 0x0806c0a0. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
    (0x0806c0ae, 'magical_hats_zone_state_stub_c0ae',
     'Sub-entry0: 7-entry nested sub-dispatch table at 0x0806bfa0, '
     'entry[0] at 0x0806bfa0 -> 0x0806c0ae. '
     'Block range 0x0806bfbc..0x0806c0cb.'),
]


def main():
    total_fns = (len(BLOCK1_FNS) + len(BLOCK2_FNS) + len(BLOCK3_FNS) +
                 len(BLOCK4_FNS) + len(BLOCK5_FNS))
    print("=== DisassembleF08Seg8bBlocks (DRY=%s) ===" % DRY)
    print("  Block1: 0x%08x..0x%08x (%d fn)" % (BLOCK1_LO, BLOCK1_HI, len(BLOCK1_FNS)))
    print("  Block2: 0x%08x..0x%08x (%d stubs)" % (BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    print("  Block3: 0x%08x..0x%08x (%d fn)" % (BLOCK3_LO, BLOCK3_HI, len(BLOCK3_FNS)))
    print("  Block4: 0x%08x..0x%08x (%d stubs, nested sub-table at 0x%08x)" % (
        BLOCK4_LO, BLOCK4_HI, len(BLOCK4_FNS), BLOCK4_NESTED_LIT_POOL))
    print("  Block5: 0x%08x..0x%08x (%d sub-stubs)" % (BLOCK5_LO, BLOCK5_HI, len(BLOCK5_FNS)))
    print("  Total new functions: %d" % total_fns)

    if DRY:
        for addr, name, _ in BLOCK1_FNS:
            print("[dry] Block1 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK2_FNS:
            print("[dry] Block2 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK3_FNS:
            print("[dry] Block3 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK4_FNS:
            print("[dry] Block4 fn: %s @ 0x%08x" % (name, addr))
        for addr, name, _ in BLOCK5_FNS:
            print("[dry] Block5 fn: %s @ 0x%08x" % (name, addr))
        print("[dry] total fns=%d" % total_fns)
        return

    # =========================================================================
    # Block1: 0x0806b784..0x0806b7cf
    # fn_eligible for CID=0x135b
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (fn_eligible cid_135b) ---" % (BLOCK1_LO, BLOCK1_HI))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    for addr, name, _ in BLOCK1_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK1_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block1: %d fn created" % len(BLOCK1_FNS))

    # =========================================================================
    # Block2: 0x0806b7fc..0x0806ba77
    # 10 state stubs for CID=0x135b
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (%d stubs, cid_135b) ---" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    _clear_and_set_thumb(BLOCK2_LO, BLOCK2_HI)
    for addr, name, _ in BLOCK2_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK2_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block2: %d stubs created" % len(BLOCK2_FNS))

    # =========================================================================
    # Block3: 0x0806bb74..0x0806bbb7
    # fn_eligible for CID=0x1362 Magical Hats
    # =========================================================================
    print("\n--- Block3: 0x%08x..0x%08x (fn_eligible Magical Hats) ---" % (BLOCK3_LO, BLOCK3_HI))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)
    for addr, name, _ in BLOCK3_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK3_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block3: %d fn created" % len(BLOCK3_FNS))

    # =========================================================================
    # Block4: 0x0806bc2c..0x0806bf9f
    # 11 state stubs for Magical Hats CID=0x1362
    # NESTED: literal pool @0x6bf9c + sub-table @0x6bfa0..0x6bfb8 -> createDWord first
    # =========================================================================
    print("\n--- Block4: 0x%08x..0x%08x (%d stubs, Magical Hats) ---" % (
        BLOCK4_LO, BLOCK4_HI, len(BLOCK4_FNS)))
    _clear_and_set_thumb(BLOCK4_LO, BLOCK4_HI)
    # Force DWORD split at nested literal pool (0x6bf9c) and sub-table entries (0x6bfa0..0x6bfb8)
    # This prevents Ghidra from trying to disassemble the sub-table as code
    for dw_addr in [BLOCK4_NESTED_LIT_POOL,
                    0x0806bfa0, 0x0806bfa4, 0x0806bfa8,
                    0x0806bfac, 0x0806bfb0, 0x0806bfb4, 0x0806bfb8]:
        _create_dword(dw_addr)
    for addr, name, _ in BLOCK4_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK4_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block4: %d stubs created" % len(BLOCK4_FNS))

    # =========================================================================
    # Block5: 0x0806bfbc..0x0806c0cb
    # 7 sub-stubs from Magical Hats nested sub-dispatch
    # =========================================================================
    print("\n--- Block5: 0x%08x..0x%08x (%d sub-stubs, Magical Hats nested) ---" % (
        BLOCK5_LO, BLOCK5_HI, len(BLOCK5_FNS)))
    _clear_and_set_thumb(BLOCK5_LO, BLOCK5_HI)
    for addr, name, _ in BLOCK5_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK5_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block5: %d sub-stubs created" % len(BLOCK5_FNS))

    print("\n=== DisassembleF08Seg8bBlocks DONE ===")
    print("  Total new functions: %d" % total_fns)
    print("  Block1: %d (check_equip_eligible_cid_135b)" % len(BLOCK1_FNS))
    print("  Block2: %d (cid_135b_state_stub_*)" % len(BLOCK2_FNS))
    print("  Block3: %d (check_equip_eligible_magical_hats)" % len(BLOCK3_FNS))
    print("  Block4: %d (magical_hats_state_stub_*)" % len(BLOCK4_FNS))
    print("  Block5: %d (magical_hats_zone_state_stub_*)" % len(BLOCK5_FNS))


main()
