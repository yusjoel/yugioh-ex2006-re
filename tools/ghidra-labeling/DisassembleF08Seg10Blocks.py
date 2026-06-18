# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF08Seg10Blocks.py -- F08 Seg-10 R4 disasm (4 blocks)
#
# Block1: 0x0806dbcc..0x0806e00b (0x44 B)
#   fn_eligible+state-dispatch handler for GAP_CID_13ED=0x13ed
#   THUMB+1 ref @0x09e406d0: entry [fn_act=0, pad=0x808198d, CID=0x13ed,
#     fn_elig+1=0x0806dbcd, 0x0805e579]
#   Literal pool inside: 0x0806dc04=0xfffffe00, 0x0806dc08=gDuelPhaseFlags,
#     0x0806dc0c=0x0806dc10 (table ptr)
#   1 function: check_equip_eligible_state_dispatch_cid_13ed @ 0x0806dbcc
#
# Block2: 0x0806dc3c..0x0806e00b (0x3d0 B)
#   11 THUMB state stubs for CID=0x13ed; dispatched via raw MOV PC,r0
#   from 11-entry table at 0x0806dc10 (states 0x76..0x80)
#   raw ref @0x6dc38 = table entry[10] = block start 0x0806dc3c (state=0x80)
#   Dispatcher: subs r1,#0x76; cmp r1,#0xa; bls => index=state-0x76
#   table[0]=state_0x76 at 0x0806dfa8, table[10]=state_0x80 at 0x0806dc3c
#
# Block3: 0x0806e3fa..0x0806e447 (0x4e B)
#   2B pad (0x0000) + fn_eligible+state-dispatch handler for DE_FUSION_CID=0x13fe
#   THUMB+1 ref @0x09e407f0: entry [fn_act+1=0x08056931, pad=0, CID=0x13fe,
#     fn_elig+1=0x0806e3fd]
#   1 function: check_equip_eligible_state_dispatch_de_fusion @ 0x0806e3fc
#
# Block4: 0x0806e460..0x0806e62b (0x1cc B)
#   6 THUMB state stubs for DE_FUSION_CID=0x13fe; dispatched via raw MOV PC,r0
#   from 6-entry table at 0x0806e448 (states 0x7b..0x80)
#   raw ref @0x6e45c = table entry[5] = lowest-addr stub 0x0806e460 (state=0x80)
#   Dispatcher: subs r1,#0x7b; cmp r1,#5; bls => index=state-0x7b
#   table[0]=state_0x7b at 0x0806e618, table[5]=state_0x80 at 0x0806e460
#
# NOTE: Each block: clearListing + setTMode(THUMB) on full range first,
#   then DisassembleCommand per stub entry point.
#   Block1 literal pool at 0x0806dc04..0x0806dc0f must createDWord x3 before
#   disasm to prevent Ghidra treating pool as code.
#   Block3 starts with 2B pad at 0x0806e3fa: createDWord/createWord before
#   disasm of fn at 0x0806e3fc.
#
# NOTE: All plate text is pure ASCII (no CJK). Jython CJK = double-UTF-8 mojibake.
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_091902-pre-F08Seg10

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
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


def _create_dword(addr):
    """Force a DWORD data item at addr to split any existing code/data."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a)
    except Exception as e:
        print("[warn] clearListing for dword at 0x%08x: %s" % (addr, e))
    try:
        listing.createData(a, DWordDataType.dataType)
        print("[DWORD] created at 0x%08x" % addr)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr, e))


def _create_word(addr):
    """Force a WORD (2B) data item at addr."""
    a = _addr(addr)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a)
    except Exception as e:
        print("[warn] clearListing for word at 0x%08x: %s" % (addr, e))
    try:
        listing.createData(a, WordDataType.dataType)
        print("[WORD] created at 0x%08x" % addr)
    except Exception as e:
        print("[warn] createWord 0x%08x: %s" % (addr, e))


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
# BLOCK 1: 0x0806dbcc..0x0806e00b (0x40 B code + 0x4 B literal pool tail)
#   fn_eligible+state-dispatch handler for GAP_CID_13ED=0x13ed
#   1 function
# ===========================================================================
BLOCK1_LO = 0x0806dbcc
BLOCK1_HI = 0x0806e00b

# Literal pool at end of function: 3 dwords at 0x0806dc04/dc08/dc0c
BLOCK1_LIT_POOLS = [0x0806dc04, 0x0806dc08, 0x0806dc0c]

BLOCK1_FNS = [
    (0x0806dbcc, 'check_equip_eligible_state_dispatch_cid_13ed',
     'fn_eligible+state-dispatch handler for GAP_CID_13ED=0x13ed (card_5101=card_stat_zero, unallocated). '
     'THUMB+1 ref at dispatch table @0x09e406d0: entry [fn_act=0, pad=0x808198d, CID=0x13ed, '
     'fn_elig+1=0x0806dbcd, 0x0805e579]. '
     'Checks guard bit2 of effect_node[+4]; exits if set. '
     'Reads gDuelPhaseFlags[+0x4a0] state. '
     'subs r1,#0x76; cmp r1,#0xa; bls -> dispatch range 0x76..0x80. '
     'Dispatches via 11-entry raw-addr table at 0x0806dc10 (MOV PC,r0). '
     'Literal pool at 0x0806dc04: 0xfffffe00, gDuelPhaseFlags=0x0201b290, table=0x0806dc10. '
     'Block range 0x0806dbcc..0x0806e00b.'),
]

# ===========================================================================
# BLOCK 2: 0x0806dc3c..0x0806e00b (0x3d0 B)
#   11 THUMB state stubs for CID=0x13ed (states 0x76..0x80)
#   Dispatcher: subs r1,#0x76; index=state-0x76
#   table[0]=state_0x76 @ 0x0806dfa8, table[10]=state_0x80 @ 0x0806dc3c
# ===========================================================================
BLOCK2_LO = 0x0806dc3c
BLOCK2_HI = 0x0806e00b

BLOCK2_FNS = [
    # table[10]=entry[10] -> state=0x80 = highest index = lowest state? NO.
    # index=state-0x76: state=0x76 -> index=0, state=0x80 -> index=0xa=10
    # table[0]=state_0x76 @ lowest index => addr 0x0806dfa8 (from proposal)
    # table[10]=state_0x80 @ index=10 => addr 0x0806dc3c (raw ref @0x6dc38=entry[10])
    # So: entry[i] = addr of state_(0x76+i)
    (0x0806dc3c, 'cid_13ed_state_stub_80',
     'State stub for state=0x80 (table entry[10]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[10] at 0x6dc38 -> 0x0806dc3c. '
     'index=state-0x76; state=0x80 -> index=10. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806dc70, 'cid_13ed_state_stub_7f',
     'State stub for state=0x7f (table entry[9]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[9]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806dcfc, 'cid_13ed_state_stub_7e',
     'State stub for state=0x7e (table entry[8]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[8]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806dd20, 'cid_13ed_state_stub_7d',
     'State stub for state=0x7d (table entry[7]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[7]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806dda8, 'cid_13ed_state_stub_7c',
     'State stub for state=0x7c (table entry[6]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[6]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806ddb8, 'cid_13ed_state_stub_7b',
     'State stub for state=0x7b (table entry[5]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[5]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806de40, 'cid_13ed_state_stub_7a',
     'State stub for state=0x7a (table entry[4]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[4]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806de7e, 'cid_13ed_state_stub_79',
     'State stub for state=0x79 (table entry[3]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[3]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806df14, 'cid_13ed_state_stub_78',
     'State stub for state=0x78 (table entry[2]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[2]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806df58, 'cid_13ed_state_stub_77',
     'State stub for state=0x77 (table entry[1]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[1]. '
     'Block range 0x0806dc3c..0x0806e00b.'),
    (0x0806dfa8, 'cid_13ed_state_stub_76',
     'State stub for state=0x76 (table entry[0]) in CID=0x13ed handler. '
     '11-entry raw-addr table at 0x0806dc10; entry[0] at lowest index. '
     'Block range 0x0806dc3c..0x0806e00b.'),
]

# ===========================================================================
# BLOCK 3: 0x0806e3fa..0x0806e447 (0x4e B)
#   2B pad (0x0000) at 0x0806e3fa + fn_eligible handler at 0x0806e3fc
#   fn_eligible for DE_FUSION_CID=0x13fe (De-Fusion pw=95286165)
#   1 function at 0x0806e3fc
# ===========================================================================
BLOCK3_LO = 0x0806e3fa
BLOCK3_HI = 0x0806e447

# 2B pad at block start
BLOCK3_PAD = 0x0806e3fa

# Literal pool inside fn: gDuelPhaseFlags=0x0201b290, table=0x0806e448
BLOCK3_LIT_POOLS = [0x0806e440, 0x0806e444]

BLOCK3_FNS = [
    (0x0806e3fc, 'check_equip_eligible_state_dispatch_de_fusion',
     'fn_eligible+state-dispatch handler for DE_FUSION_CID=0x13fe (De-Fusion pw=95286165). '
     'THUMB+1 ref at dispatch table @0x09e407f0: entry [fn_act+1=0x08056931, pad=0, '
     'CID=0x13fe, fn_elig+1=0x0806e3fd]. '
     'Block starts with 2B pad (0x0000) at 0x0806e3fa; fn entry at 0x0806e3fc. '
     'First checks zone entry match via check_effect_slot_matches_zone_entry. '
     'Checks guard bit2 of effect_node[+4]; exits if set. '
     'Reads gDuelPhaseFlags[+0x4a0] state. '
     'subs r1,#0x7b; cmp r1,#5; bls -> dispatch range 0x7b..0x80. '
     'Dispatches via 6-entry raw-addr table at 0x0806e448 (MOV PC,r7). '
     'Literal pool at 0x0806e440: gDuelPhaseFlags=0x0201b290, table=0x0806e448. '
     'Block range 0x0806e3fa..0x0806e447.'),
]

# ===========================================================================
# BLOCK 4: 0x0806e460..0x0806e62b (0x1cc B)
#   6 THUMB state stubs for DE_FUSION_CID=0x13fe (states 0x7b..0x80)
#   Dispatcher: subs r1,#0x7b; cmp r1,#5; bls => index=state-0x7b
#   Table at 0x0806e448: entry[0]=0x6e618(state=0x7b), entry[1]=0x6e5d4(state=0x7c),
#     entry[2]=0x6e5ae(state=0x7d), entry[3]=0x6e61c(state=0x7e),
#     entry[4]=0x6e518(state=0x7f), entry[5]=0x6e460(state=0x80)
#   raw ref @0x6e45c = entry[5] = lowest stub addr 0x6e460 (state=0x80)
#   CORRECTED: state is determined by table index, NOT stub address order.
#   The highest-address stub (0x0806e618) is entry[0] = state=0x7b.
# ===========================================================================
BLOCK4_LO = 0x0806e460
BLOCK4_HI = 0x0806e62b

BLOCK4_FNS = [
    # Ordered by stub address (block start first)
    (0x0806e460, 'de_fusion_state_stub_80',
     'State stub for state=0x80 (table entry[5]) in DE_FUSION_CID=0x13fe handler. '
     '6-entry raw-addr table at 0x0806e448; entry[5] at 0x6e45c -> 0x0806e460 (lowest addr). '
     'index=state-0x7b; state=0x80 -> index=5. '
     'Block range 0x0806e460..0x0806e62b.'),
    (0x0806e518, 'de_fusion_state_stub_7f',
     'State stub for state=0x7f (table entry[4]) in DE_FUSION_CID=0x13fe handler. '
     '6-entry raw-addr table at 0x0806e448; entry[4] at 0x6e458 -> 0x0806e518. '
     'index=state-0x7b; state=0x7f -> index=4. '
     'Block range 0x0806e460..0x0806e62b.'),
    (0x0806e5ae, 'de_fusion_state_stub_7d',
     'State stub for state=0x7d (table entry[2]) in DE_FUSION_CID=0x13fe handler. '
     '6-entry raw-addr table at 0x0806e448; entry[2] at 0x6e450 -> 0x0806e5ae. '
     'index=state-0x7b; state=0x7d -> index=2. '
     'Block range 0x0806e460..0x0806e62b.'),
    (0x0806e5d4, 'de_fusion_state_stub_7c',
     'State stub for state=0x7c (table entry[1]) in DE_FUSION_CID=0x13fe handler. '
     '6-entry raw-addr table at 0x0806e448; entry[1] at 0x6e44c -> 0x0806e5d4. '
     'index=state-0x7b; state=0x7c -> index=1. '
     'Block range 0x0806e460..0x0806e62b.'),
    (0x0806e61c, 'de_fusion_state_stub_7e',
     'State stub for state=0x7e (table entry[3]) in DE_FUSION_CID=0x13fe handler. '
     '6-entry raw-addr table at 0x0806e448; entry[3] at 0x6e454 -> 0x0806e61c. '
     'index=state-0x7b; state=0x7e -> index=3. '
     'Block range 0x0806e460..0x0806e62b.'),
    (0x0806e618, 'de_fusion_state_stub_7b',
     'State stub for state=0x7b (table entry[0]) in DE_FUSION_CID=0x13fe handler. '
     '6-entry raw-addr table at 0x0806e448; entry[0] at 0x6e448 -> 0x0806e618 (highest addr). '
     'index=state-0x7b; state=0x7b -> index=0. '
     'Block range 0x0806e460..0x0806e62b.'),
]


def main():
    total_fns = len(BLOCK1_FNS) + len(BLOCK2_FNS) + len(BLOCK3_FNS) + len(BLOCK4_FNS)
    print("=== DisassembleF08Seg10Blocks (DRY=%s) ===" % DRY)
    print("  Block1: 0x%08x..0x%08x (%d fn, fn_eligible GAP_CID_13ED)" % (
        BLOCK1_LO, BLOCK1_HI, len(BLOCK1_FNS)))
    print("  Block2: 0x%08x..0x%08x (%d stubs, cid_13ed_state_stub_*)" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    print("  Block3: 0x%08x..0x%08x (%d fn, fn_eligible DE_FUSION)" % (
        BLOCK3_LO, BLOCK3_HI, len(BLOCK3_FNS)))
    print("  Block4: 0x%08x..0x%08x (%d stubs, de_fusion_state_stub_*)" % (
        BLOCK4_LO, BLOCK4_HI, len(BLOCK4_FNS)))
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
        print("[dry] total fns=%d" % total_fns)
        return

    # =========================================================================
    # Block1: 0x0806dbcc..0x0806e00b
    # fn_eligible for GAP_CID_13ED=0x13ed
    # Literal pool at 0x0806dc04/dc08/dc0c must be forced DWORD before disasm
    # Note: Block2 starts at 0x0806dc3c, which is within this range after literal pool.
    # We disasm Block1 fn first, then use Block2 stubs.
    # The clearListing for Block1 covers 0x0806dbcc..0x0806e00b (overlaps with Block2),
    # but we must disasm Block1 fn before Block2 stubs.
    # =========================================================================
    print("\n--- Block1: 0x%08x..0x%08x (fn_eligible GAP_CID_13ED) ---" % (BLOCK1_LO, BLOCK1_HI))
    _clear_and_set_thumb(BLOCK1_LO, BLOCK1_HI)
    # Force DWORD at literal pool entries
    for pool_addr in BLOCK1_LIT_POOLS:
        _create_dword(pool_addr)
    for addr, name, _ in BLOCK1_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK1_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block1: %d fn created" % len(BLOCK1_FNS))

    # =========================================================================
    # Block2: 0x0806dc3c..0x0806e00b
    # 11 state stubs for CID=0x13ed (states 0x76..0x80)
    # Block1 clearListing+setTMode+disasm_flow already covered this range.
    # Do NOT re-setTMode (ContextChangeException on existing instructions).
    # Just call _disasm_flow on each stub entry point individually.
    # =========================================================================
    print("\n--- Block2: 0x%08x..0x%08x (%d stubs, cid_13ed_state_stub_*) ---" % (
        BLOCK2_LO, BLOCK2_HI, len(BLOCK2_FNS)))
    # TMode already set by Block1 pass; skip re-setTMode to avoid ContextChangeException
    for addr, name, _ in BLOCK2_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK2_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block2: %d stubs created" % len(BLOCK2_FNS))

    # =========================================================================
    # Block3: 0x0806e3fa..0x0806e447
    # 2B pad at 0x0806e3fa + fn_eligible handler at 0x0806e3fc (DE_FUSION)
    # Literal pool at 0x0806e440/e444 must be forced DWORD before disasm
    # =========================================================================
    print("\n--- Block3: 0x%08x..0x%08x (2B pad + fn_eligible DE_FUSION) ---" % (
        BLOCK3_LO, BLOCK3_HI))
    _clear_and_set_thumb(BLOCK3_LO, BLOCK3_HI)
    # Force WORD at 2B pad
    _create_word(BLOCK3_PAD)
    # Force DWORD at literal pool entries
    for pool_addr in BLOCK3_LIT_POOLS:
        _create_dword(pool_addr)
    for addr, name, _ in BLOCK3_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK3_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block3: %d fn created" % len(BLOCK3_FNS))

    # =========================================================================
    # Block4: 0x0806e460..0x0806e62b
    # 6 state stubs for DE_FUSION_CID=0x13fe (states 0x7b..0x80)
    # NOTE: state mapping CORRECTED from proposal - index=state-0x7b
    #   entry[0]=state_0x7b @ 0x0806e618 (highest addr)
    #   entry[5]=state_0x80 @ 0x0806e460 (lowest addr = block start)
    # =========================================================================
    print("\n--- Block4: 0x%08x..0x%08x (%d stubs, de_fusion_state_stub_*) ---" % (
        BLOCK4_LO, BLOCK4_HI, len(BLOCK4_FNS)))
    _clear_and_set_thumb(BLOCK4_LO, BLOCK4_HI)
    for addr, name, _ in BLOCK4_FNS:
        _disasm_flow(addr)
    for addr, name, plate_text in BLOCK4_FNS:
        _create_function(addr, name)
        _set_plate(addr, plate_text)
    print("  Block4: %d stubs created" % len(BLOCK4_FNS))

    print("\n=== DisassembleF08Seg10Blocks DONE ===")
    print("  Total new functions: %d" % total_fns)
    print("  Block1: %d (check_equip_eligible_state_dispatch_cid_13ed)" % len(BLOCK1_FNS))
    print("  Block2: %d (cid_13ed_state_stub_*)" % len(BLOCK2_FNS))
    print("  Block3: %d (check_equip_eligible_state_dispatch_de_fusion)" % len(BLOCK3_FNS))
    print("  Block4: %d (de_fusion_state_stub_*)" % len(BLOCK4_FNS))


main()
