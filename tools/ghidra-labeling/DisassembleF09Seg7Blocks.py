# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg7Blocks.py -- p5 file09 Seg-7 R4 disasm (blocks B1..B6)
#
# B1: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378 (ROM_INCBIN 0x75378/0x28)
#   - THUMB+1 ref: 0x08075379 from FS table at GBA:0x09e41678 (CID=0x1629)
#   - fn body: 0x08075378..0x0807539f (0x28 bytes)
#   - Literal pool at +0x24=0x0807539c: 0x080753a0 (dispatch table base for B2)
#     NOTE: pool word at 0x0807539c IS inside the 0x28-byte incbin range
#     (0x75378 + 0x28 = 0x753a0, so range is [0x75378, 0x7539f])
#     pool at 0x0807539c is the last 4 bytes of the block
#
# B2: emblem_dispatch_sub_stubs @ 0x08075414 (ROM_INCBIN 0x75414/0xa4)
#   - dispatch table 0x753a0..0x75413 (29 entries, raw ptr); already in asm
#   - 6 unique sub-stub entry points:
#     emblem_sub_5414 @ 0x08075414
#     emblem_sub_5446 @ 0x08075446
#     emblem_sub_545a @ 0x0807545a
#     emblem_sub_5492 @ 0x08075492
#     emblem_sub_54a4 @ 0x080754a4
#     emblem_default_54ae @ 0x080754ae (default/noop)
#   - Block range: [0x08075414, 0x080754b7]
#
# B3: fn_eligible_magical_dimension @ 0x08075d0c (ROM_INCBIN 0x75d0c/0x2c)
#   - THUMB+1 ref: 0x08075d0d from FS table at GBA:0x09e41948 (CID=0x1678)
#   - fn body: 0x08075d0c..0x08075d37 (0x2c bytes)
#   - Literal pool: 2 DWords at 0x08075d30 (+0x24) and 0x08075d34 (+0x28)
#     0x08075d30: 0x0201b290 (gDuelPhaseFlags)
#     0x08075d34: 0x08075d38 (dispatch table base for B4)
#     Both inside the 0x2c range [0x75d0c, 0x75d37]
#
# B4: magical_dim_dispatch_sub_stubs @ 0x08075d5c (ROM_INCBIN 0x75d5c/0x214)
#   - dispatch table 0x75d38..0x75d5b (9 entries, raw ptr); already in asm
#   - 9 unique sub-stub entry points:
#     magical_dim_sub_5d5c @ 0x08075d5c
#     magical_dim_sub_5dc4 @ 0x08075dc4
#     magical_dim_sub_5de8 @ 0x08075de8
#     magical_dim_sub_5e20 @ 0x08075e20
#     magical_dim_sub_5e60 @ 0x08075e60
#     magical_dim_sub_5e8c @ 0x08075e8c
#     magical_dim_sub_5ec0 @ 0x08075ec0
#     magical_dim_sub_5f02 @ 0x08075f02
#     magical_dim_sub_5f2c @ 0x08075f2c
#   - Block range: [0x08075d5c, 0x08075f6f]
#   - Internal THUMB+1 literal pool words (callee fn-ptrs, not dispatch table):
#     B4+0x088=0x08075de4: 0x08053e15 (check_equip_slot_eligible_by_type_and_space+1)
#     B4+0x0e8=0x08075e44: 0x08065991 (check_equip_activation_at_slot11+1)
#     B4+0x100=0x08075e5c: 0x08065991 (same callee)
#     B4+0x190=0x08075eec: 0x08050751 (check_equip_slot_eligible_type_and_card_match+1)
#     B4+0x1cc=0x08075f28: 0x08050751 (same callee)
#   - Additional pool DWords in B4 (non-THUMB+1, plain data values):
#     Need to discover during disasm; pre-force at known callee ptr positions
#
# B5: fn_eligible_friendship @ 0x08075f90 (ROM_INCBIN 0x75f8e/0x2e)
#   - 2-byte alignment pad (0x0000) at 0x08075f8e (+0x00 of incbin)
#   - fn code starts at 0x08075f90 (+0x02 of incbin)
#   - THUMB+1 ref: 0x08075f91 from FS table at GBA:0x09e41978 (CID=0x167a FRIENDSHIP_CID)
#   - fn body: 0x08075f90..0x08075fbb (0x2c bytes of code; incbin is 0x2e)
#   - Literal pool: 2 DWords
#     0x08075fb4 (+0x26 from 0x75f8e): 0x0201b290 (gDuelPhaseFlags)
#     0x08075fb8 (+0x2a from 0x75f8e): 0x08075fbc (dispatch table base for B6)
#     NOTE: incbin 0x2e = [0x75f8e, 0x75fbb]; pool at 0x75fb4 inside range
#     0x75f8e + 0x2e = 0x75fbc -> range [0x75f8e, 0x75fbb] inclusive
#   - Procedure: do NOT clearListing the 2B pad at 0x08075f8e
#                clearListing 0x08075f90..0x08075fbb (fn code + pool, 0x2c bytes)
#                setTMode from 0x08075f90
#                DisassembleCommand from 0x08075f90
#                createFunction fn_eligible_friendship @ 0x08075f90
#                force_dword for pool at 0x08075fb4 and 0x08075fb8
#
# B6: friendship_dispatch_sub_stubs @ 0x08075fe0 (ROM_INCBIN 0x75fe0/0x17c)
#   - dispatch table 0x75fbc..0x75fdb (9 entries, raw ptr); already in asm
#   - 6 unique sub-stub entry points:
#     friendship_sub_5fe0 @ 0x08075fe0
#     friendship_sub_5ff4 @ 0x08075ff4
#     friendship_sub_6030 @ 0x08076030
#     friendship_sub_609e @ 0x0807609e
#     friendship_sub_6100 @ 0x08076100
#     friendship_default_6146 @ 0x08076146 (default/noop)
#   - Block range: [0x08075fe0, 0x0807615b]
#
# Pattern: clearListing -> setTMode -> per-stub DisassembleCommand -> force-DWord pool words
#
# NOTE: All labels are pure ASCII. No CJK in EOL/plate.

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
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

# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

# B1: fn_eligible_emblem_of_dragon_destroyer
B1_LO   = 0x08075378   # fn body start (no pad before)
B1_HI   = 0x0807539f   # end of incbin (0x28 bytes from 0x75378)
B1_POOL_DWORDS = [0x0807539c]  # last 4 bytes of block: ptr to dispatch table

# B2: emblem sub-stubs
B2_LO = 0x08075414
B2_HI = 0x080754b7   # 0x75414 + 0xa4 - 1
B2_STUBS = [
    (0x08075414, 'emblem_sub_5414'),
    (0x08075446, 'emblem_sub_5446'),
    (0x0807545a, 'emblem_sub_545a'),
    (0x08075492, 'emblem_sub_5492'),
    (0x080754a4, 'emblem_sub_54a4'),
    (0x080754ae, 'emblem_default_54ae'),
]
# Pool DWords in B2: discover during disasm; pre-force known ones
# Based on instruction analysis: pool words between sub-stub bodies
# Conservative: no pre-known pool dwords; let disasm handle, fix if needed
B2_POOL_DWORDS = []

# B3: fn_eligible_magical_dimension
B3_LO   = 0x08075d0c   # fn body start (no pad)
B3_HI   = 0x08075d37   # end of incbin (0x2c bytes from 0x75d0c)
B3_POOL_DWORDS = [0x08075d30, 0x08075d34]  # gDuelPhaseFlags + dispatch table ptr

# B4: magical_dim sub-stubs
B4_LO = 0x08075d5c
B4_HI = 0x08075f6f   # 0x75d5c + 0x214 - 1
B4_STUBS = [
    (0x08075d5c, 'magical_dim_sub_5d5c'),
    (0x08075dc4, 'magical_dim_sub_5dc4'),
    (0x08075de8, 'magical_dim_sub_5de8'),
    (0x08075e20, 'magical_dim_sub_5e20'),
    (0x08075e60, 'magical_dim_sub_5e60'),
    (0x08075e8c, 'magical_dim_sub_5e8c'),
    (0x08075ec0, 'magical_dim_sub_5ec0'),
    (0x08075f02, 'magical_dim_sub_5f02'),
    (0x08075f2c, 'magical_dim_sub_5f2c'),
]
# Pool DWords in B4: THUMB+1 callee pointers (must be force-DWord to avoid GAS "value too big")
B4_POOL_DWORDS = [
    0x08075de4,  # B4+0x088: 0x08053e15 (check_equip_slot_eligible_by_type_and_space+1)
    0x08075e44,  # B4+0x0e8: 0x08065991 (check_equip_activation_at_slot11+1)
    0x08075e5c,  # B4+0x100: 0x08065991 (duplicate)
    0x08075eec,  # B4+0x190: 0x08050751 (check_equip_slot_eligible_type_and_card_match+1)
    0x08075f28,  # B4+0x1cc: 0x08050751 (duplicate)
]

# B5: fn_eligible_friendship (2B pad at 0x08075f8e, fn starts at 0x08075f90)
B5_PAD  = 0x08075f8e   # 2B alignment pad (DO NOT clearListing)
B5_LO   = 0x08075f90   # fn body start
B5_HI   = 0x08075fbb   # end of incbin code+pool region (0x2e - 2B pad = 0x2c from 0x75f90)
B5_POOL_DWORDS = [0x08075fb4, 0x08075fb8]  # gDuelPhaseFlags + dispatch table ptr

# B6: friendship sub-stubs
B6_LO = 0x08075fe0
B6_HI = 0x0807615b   # 0x75fe0 + 0x17c - 1
B6_STUBS = [
    (0x08075fe0, 'friendship_sub_5fe0'),
    (0x08075ff4, 'friendship_sub_5ff4'),
    (0x08076030, 'friendship_sub_6030'),
    (0x0807609e, 'friendship_sub_609e'),
    (0x08076100, 'friendship_sub_6100'),
    (0x08076146, 'friendship_default_6146'),
]
B6_POOL_DWORDS = []  # Discover during disasm; fix if GAS errors occur

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=1 for 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")

def _clear_listing(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing 0x%08x..0x%08x" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))

def _disasm_at(sa, hi, label):
    stub_lo = _addr(sa)
    stub_hi = _addr(hi)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x" % (label, sa))

def _disasm_stubs(stubs, block_hi, block_name):
    """Disassemble a list of (start_addr, label) sub-stubs up to block_hi."""
    for i, (sa, label) in enumerate(stubs):
        # end address: next stub start - 1, or block_hi for last stub
        if i + 1 < len(stubs):
            hi = stubs[i + 1][0] - 1
        else:
            hi = block_hi
        _disasm_at(sa, hi, label)
        _add_label(sa, label)

def _force_dword(addr_int):
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

def _add_label(addr_int, label):
    sym_tbl = currentProgram.getSymbolTable()
    a = _addr(addr_int)
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if label not in names:
        sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
        print("[ok ] label 0x%08x -> %s" % (addr_int, label))
    else:
        print("[ok ] label 0x%08x -> %s (already exists)" % (addr_int, label))

def _create_function(addr_int, name, body_hi):
    a = _addr(addr_int)
    fm = currentProgram.getFunctionManager()
    fn = fm.getFunctionAt(a)
    if fn is not None:
        if fn.getName() != name:
            fn.setName(name, SourceType.USER_DEFINED)
            print("[ok ] function renamed 0x%08x -> %s" % (addr_int, name))
        else:
            print("[ok ] function 0x%08x already named %s" % (addr_int, name))
    else:
        try:
            fm.createFunction(name, a,
                              AddressSet(_addr(addr_int), _addr(body_hi)),
                              SourceType.USER_DEFINED)
            print("[ok ] createFunction %s @ 0x%08x" % (name, addr_int))
        except Exception as e:
            print("[warn] createFunction %s @ 0x%08x: %s" % (name, addr_int, e))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg7Blocks (DRY=%s) ===" % DRY)
    print("  B1: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378 (0x28B)")
    print("  B2: emblem_dispatch_sub_stubs @ 0x08075414 (0xa4B, 6 stubs)")
    print("  B3: fn_eligible_magical_dimension @ 0x08075d0c (0x2cB)")
    print("  B4: magical_dim_dispatch_sub_stubs @ 0x08075d5c (0x214B, 9 stubs)")
    print("  B5: fn_eligible_friendship @ 0x08075f90 (2B pad at 0x75f8e, 0x2eB total)")
    print("  B6: friendship_dispatch_sub_stubs @ 0x08075fe0 (0x17cB, 6 stubs)")

    if DRY:
        print("[dry] B1: clearListing(0x08075378..0x0807539f) + setTMode + disasm + pool x1 + createFn")
        print("[dry] B2: clearListing(0x08075414..0x080754b7) + setTMode + 6x disasm + labels")
        print("[dry] B3: clearListing(0x08075d0c..0x08075d37) + setTMode + disasm + pool x2 + createFn")
        print("[dry] B4: clearListing(0x08075d5c..0x08075f6f) + setTMode + pool x5 + 9x disasm + labels")
        print("[dry] B5: clearListing(0x08075f90..0x08075fbb) [NOT 0x75f8e pad] + setTMode + disasm + pool x2 + createFn")
        print("[dry] B6: clearListing(0x08075fe0..0x0807615b) + setTMode + 6x disasm + labels")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Block1: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378
    # -----------------------------------------------------------------------
    print("\n--- Block1: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378 ---")
    print("    CID=0x1629 Emblem of Dragon Destroyer; FS THUMB+1 @ 0x09e41678")
    print("    Range: 0x%08x..0x%08x (0x28 bytes)" % (B1_LO, B1_HI))

    _clear_listing(B1_LO, B1_HI)
    _set_tmode(B1_LO, B1_HI)

    # Disassemble fn body (code ends before literal pool at 0x0807539c)
    b1_code_hi = B1_POOL_DWORDS[0] - 1  # 0x0807539b
    _disasm_at(B1_LO, b1_code_hi, 'fn_eligible_emblem_of_dragon_destroyer')

    # Force DWord for literal pool
    for dw_addr in B1_POOL_DWORDS:
        _force_dword(dw_addr)

    # createFunction
    _create_function(B1_LO, 'fn_eligible_emblem_of_dragon_destroyer', B1_HI)
    _add_label(B1_LO, 'fn_eligible_emblem_of_dragon_destroyer')

    # -----------------------------------------------------------------------
    # Block2: emblem_dispatch_sub_stubs @ 0x08075414
    # -----------------------------------------------------------------------
    print("\n--- Block2: emblem_dispatch_sub_stubs @ 0x08075414 ---")
    print("    ROM_INCBIN 0x75414/0xa4; 6 sub-stubs via 29-entry dispatch table")

    _clear_listing(B2_LO, B2_HI)
    _set_tmode(B2_LO, B2_HI)

    # Force any pre-known pool DWords
    for dw_addr in B2_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B2_STUBS, B2_HI, "B2")

    # -----------------------------------------------------------------------
    # Block3: fn_eligible_magical_dimension @ 0x08075d0c
    # -----------------------------------------------------------------------
    print("\n--- Block3: fn_eligible_magical_dimension @ 0x08075d0c ---")
    print("    CID=0x1678 Magical Dimension; FS THUMB+1 @ 0x09e41948")
    print("    Range: 0x%08x..0x%08x (0x2c bytes)" % (B3_LO, B3_HI))

    _clear_listing(B3_LO, B3_HI)
    _set_tmode(B3_LO, B3_HI)

    # Disassemble fn body (code ends before literal pool at 0x08075d30)
    b3_code_hi = B3_POOL_DWORDS[0] - 1  # 0x08075d2f
    _disasm_at(B3_LO, b3_code_hi, 'fn_eligible_magical_dimension')

    # Force DWords for literal pool (2 DWords: gDuelPhaseFlags + dispatch table ptr)
    for dw_addr in B3_POOL_DWORDS:
        _force_dword(dw_addr)

    # createFunction
    _create_function(B3_LO, 'fn_eligible_magical_dimension', B3_HI)
    _add_label(B3_LO, 'fn_eligible_magical_dimension')

    # -----------------------------------------------------------------------
    # Block4: magical_dim_dispatch_sub_stubs @ 0x08075d5c
    # -----------------------------------------------------------------------
    print("\n--- Block4: magical_dim_dispatch_sub_stubs @ 0x08075d5c ---")
    print("    ROM_INCBIN 0x75d5c/0x214; 9 sub-stubs via 9-entry dispatch table")
    print("    Internal THUMB+1 callee ptrs at 0x5de4/5e44/5e5c/5eec/5f28 -- force-DWord")

    _clear_listing(B4_LO, B4_HI)
    _set_tmode(B4_LO, B4_HI)

    # Force DWords for callee THUMB+1 literal pool words BEFORE disasm
    for dw_addr in B4_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B4_STUBS, B4_HI, "B4")

    # -----------------------------------------------------------------------
    # Block5: fn_eligible_friendship @ 0x08075f90 (2B pad at 0x08075f8e)
    # -----------------------------------------------------------------------
    print("\n--- Block5: fn_eligible_friendship @ 0x08075f90 ---")
    print("    CID=0x167a Friendship (REUSE FRIENDSHIP_CID); FS THUMB+1 @ 0x09e41978")
    print("    2B alignment pad at 0x08075f8e (NOT cleared); fn code at 0x08075f90")
    print("    fn code range: 0x%08x..0x%08x (0x2c bytes incl pool)" % (B5_LO, B5_HI))

    # NOTE: Do NOT clearListing the 2B pad at 0x08075f8e
    _clear_listing(B5_LO, B5_HI)
    _set_tmode(B5_LO, B5_HI)

    # Disassemble fn body (code ends before literal pool at 0x08075fb4)
    b5_code_hi = B5_POOL_DWORDS[0] - 1  # 0x08075fb3
    _disasm_at(B5_LO, b5_code_hi, 'fn_eligible_friendship')

    # Force DWords for literal pool (2 DWords: gDuelPhaseFlags + dispatch table ptr)
    for dw_addr in B5_POOL_DWORDS:
        _force_dword(dw_addr)

    # createFunction
    _create_function(B5_LO, 'fn_eligible_friendship', B5_HI)
    _add_label(B5_LO, 'fn_eligible_friendship')

    # -----------------------------------------------------------------------
    # Block6: friendship_dispatch_sub_stubs @ 0x08075fe0
    # -----------------------------------------------------------------------
    print("\n--- Block6: friendship_dispatch_sub_stubs @ 0x08075fe0 ---")
    print("    ROM_INCBIN 0x75fe0/0x17c; 6 sub-stubs via 9-entry dispatch table")

    _clear_listing(B6_LO, B6_HI)
    _set_tmode(B6_LO, B6_HI)

    # Force any pre-known pool DWords
    for dw_addr in B6_POOL_DWORDS:
        _force_dword(dw_addr)

    # Disassemble each sub-stub
    _disasm_stubs(B6_STUBS, B6_HI, "B6")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B1_LO, B1_HI, "B1"),
        (B2_LO, B2_HI, "B2"),
        (B3_LO, B3_HI, "B3"),
        (B4_LO, B4_HI, "B4"),
        (B5_LO, B5_HI, "B5"),
        (B6_LO, B6_HI, "B6"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg7Blocks DONE ===")
    print("  New functions: fn_eligible_emblem_of_dragon_destroyer @ 0x08075378")
    print("                 fn_eligible_magical_dimension @ 0x08075d0c")
    print("                 fn_eligible_friendship @ 0x08075f90")
    print("  Sub-stub labels: B2=6 + B4=9 + B6=6 = 21 total")


main()
