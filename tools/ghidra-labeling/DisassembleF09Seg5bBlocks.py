# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg5bBlocks.py -- p5 file09 Seg-5b R4 disasm (blocks B7-B10)
#
# Blocks:
#   B7: fn_eligible_reasoning @ 0x08073b1c (0x30 bytes, ends 0x08073b4c)
#       FS handler table THUMB+1 @GBA:0x09e412b8 -> CID 0x159a Reasoning
#       Literal pool: 0x08073b44=gDuelPhaseFlags, 0x08073b48=ptr-to-B8-table
#       NOTE: 0x4647 at 0x08073b1e is mov r7,r8 (THUMB high-reg), NOT data
#
#   B8: reasoning_dispatch_sub_stubs @ 0x08073bc8 (0x1bc bytes, ends 0x08073d84)
#       Dispatch table 0x08073b4c..0x08073bc7 (31 entries = 0x7c bytes)
#       9 unique entry points:
#         reasoning_sub_3bc8 @ 0x08073bc8 (68B)
#         reasoning_sub_3c0c @ 0x08073c0c (68B)
#         reasoning_sub_3c50 @ 0x08073c50 (8B)
#         reasoning_sub_3c58 @ 0x08073c58 (234B) -- has inline pool @0x08073d12
#         reasoning_sub_3d42 @ 0x08073d42 (6B)
#         reasoning_sub_3d48 @ 0x08073d48 (16B)
#         reasoning_sub_3d58 @ 0x08073d58 (18B)
#         reasoning_sub_3d6a @ 0x08073d6a (10B)
#         reasoning_default_3d74 @ 0x08073d74 (16B)
#
#   B9: fn_eligible_reversal_quiz @ 0x08073fe0 (0x2e bytes block, ends 0x0807400c)
#       Block starts at 0x08073fde with 2-byte align pad (0x0000)
#       fn_elig starts at 0x08073fe0
#       FS handler table THUMB+1 @GBA:0x09e41378 -> CID 0x15a5 Reversal Quiz
#       Literal pool: 0x08074004=gDuelPhaseFlags, 0x08074008=ptr-to-B10-table
#
#   B10: reversal_quiz_dispatch_sub_stubs @ 0x08074080 (0x178 bytes, ends 0x080741f8)
#        Dispatch table 0x0807400c..0x0807407f (29 entries = 0x74 bytes)
#        6 unique entry points:
#          reversal_quiz_sub_4080 @ 0x08074080 (104B)
#          reversal_quiz_sub_40e8 @ 0x080740e8 (44B)
#          reversal_quiz_sub_4114 @ 0x08074114 (52B)
#          reversal_quiz_sub_4148 @ 0x08074148 (156B)
#          reversal_quiz_sub_41e4 @ 0x080741e4 (10B)
#          reversal_quiz_default_41ee @ 0x080741ee (10B)
#
# Pattern: clearListing entire block -> setTMode=THUMB -> per-stub DisassembleCommand
# For B8 stub[3] (0x08073c58, 234B): has inline pool @0x08073d12..0x08073d23
#   -> disasm 0x08073c58..0x08073d11 (178B), force_dword x3, disasm 0x08073d24..0x08073d41 (30B)
# Literal pool DWords at B7/B9 ends: createDWord to force-split data.
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
# Block ranges
# ---------------------------------------------------------------------------
# B7: fn body only (literal pool is part of listing that gets cleared/reassigned)
B7_LO = 0x08073b1c
B7_HI = 0x08073b4b   # inclusive (4B literal pool at 0x08073b44/0x08073b48)

# B8: sub-stubs block
B8_LO = 0x08073bc8
B8_HI = 0x08073d83   # inclusive

# B9: 2-byte pad + fn body + literal pool
B9_LO = 0x08073fde
B9_HI = 0x0807400b   # inclusive (4B literal pool at 0x08074004/0x08074008)

# B10: sub-stubs block
B10_LO = 0x08074080
B10_HI = 0x080741f7  # inclusive

# ---------------------------------------------------------------------------
# B8 inline pool inside reasoning_sub_3c58
# Pool at 0x08073d12..0x08073d23 (3 DWords: 0x0201c4e0/0x00000868/0x0201b290/0x000004a4)
# -> wait, 0x08073d12..0x08073d22 = 18 bytes = 4.5 DWords? Let's use 4 DWords 0x08073d12..0x08073d21
# Actually: 0x08073d12=0x0201c4e0, 0x08073d16=0x00000868, 0x08073d1a=0x0201b290(?no...)
# From dump: d12=0xc4e0 d14=0x0201 -> 0x0201c4e0; d16=0x0868 d18=0x0000 -> 0x00000868
#            d1a=0xb290 d1c=0x0201 -> 0x0201b290; d1e=0x04a4 d20=0x0000 -> 0x000004a4
#            d22 = pad? no, code resumes at d24
# So pool = 4 DWords: 0x08073d12, 0x08073d16, 0x08073d1a, 0x08073d1e
# d1e = 0x000004a4 (4 bytes), ends at 0x08073d22
# Code resumes at 0x08073d24 (confirmed from dump: d24=0x1c20 = mov r0,r4)
B8_POOL_DWORDS = [0x08073d12, 0x08073d16, 0x08073d1a, 0x08073d1e]
B8_POOL_START = 0x08073d12
B8_POOL_END = 0x08073d21   # inclusive (4x4B = 0x10 bytes)
B8_CODE_RESUME = 0x08073d24

# B7 literal pool DWords
B7_POOL_DWORDS = [0x08073b44, 0x08073b48]

# B9 literal pool DWords
B9_POOL_DWORDS = [0x08074004, 0x08074008]

# ---------------------------------------------------------------------------
# Sub-stub definitions
# B8 stubs (9 unique targets, ordered by address)
# ---------------------------------------------------------------------------
B8_STUBS = [
    # (start_addr, size_bytes, label)
    (0x08073bc8, 68,  'reasoning_sub_3bc8'),
    (0x08073c0c, 68,  'reasoning_sub_3c0c'),
    (0x08073c50, 8,   'reasoning_sub_3c50'),
    # stub[3] has inline pool -- handle separately
    (0x08073c58, None, 'reasoning_sub_3c58'),   # None = split mode
    (0x08073d42, 6,   'reasoning_sub_3d42'),
    (0x08073d48, 16,  'reasoning_sub_3d48'),
    (0x08073d58, 18,  'reasoning_sub_3d58'),
    (0x08073d6a, 10,  'reasoning_sub_3d6a'),
    (0x08073d74, 16,  'reasoning_default_3d74'),
]

# B10 stubs (6 unique targets)
B10_STUBS = [
    (0x08074080, 104, 'reversal_quiz_sub_4080'),
    (0x080740e8, 44,  'reversal_quiz_sub_40e8'),
    (0x08074114, 52,  'reversal_quiz_sub_4114'),
    (0x08074148, 156, 'reversal_quiz_sub_4148'),
    (0x080741e4, 10,  'reversal_quiz_sub_41e4'),
    (0x080741ee, 10,  'reversal_quiz_default_41ee'),
]

# Dispatch table labels
DISPATCH_TABLE_LABELS = [
    (0x08073b4c, 'reasoning_dispatch_table_3b4c'),   # 31 entries = 0x7c bytes
    (0x0807400c, 'reversal_quiz_dispatch_table_400c'),  # 29 entries = 0x74 bytes
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _set_tmode(lo, hi):
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=1 for 0x%08x..0x%08x" % (lo.getOffset(), hi.getOffset()))
    else:
        print("[warn] TMode register not found")

def _disasm_stub(sa, size, label):
    """Disassemble a single THUMB stub of known size."""
    stub_lo = _addr(sa)
    stub_hi = _addr(sa + size - 1)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x (%dB)" % (label, sa, size))

def _force_dword(addr_int):
    """Clear 4 bytes and create a DWord data item."""
    try:
        from ghidra.program.model.listing import CodeUnitInsertionException
    except ImportError:
        pass
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

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== DisassembleF09Seg5bBlocks (DRY=%s) ===" % DRY)
    print("  B7 @ 0x08073b1c (0x30B)  B8 @ 0x08073bc8 (0x1bc B)")
    print("  B9 @ 0x08073fde (0x2eB)  B10 @ 0x08074080 (0x178B)")

    if DRY:
        print("[dry] B7: clearListing + setTMode + disasm(0x08073b1c..0x08073b43) + 2x force_dword")
        print("[dry] B8: clearListing + setTMode + 9 stubs (stub[3] split around inline pool)")
        print("[dry] B9: clearListing + setTMode + disasm(0x08073fe0..0x08074003) + 2x force_dword")
        print("[dry] B10: clearListing + setTMode + 6 stubs")
        print("[dry] dispatch table labels x2")
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # B7: fn_eligible_reasoning @ 0x08073b1c
    # -----------------------------------------------------------------------
    print("\n--- B7: fn_eligible_reasoning @ 0x08073b1c ---")
    lo7 = _addr(B7_LO)
    hi7 = _addr(B7_HI)

    # clearListing + setTMode
    try:
        clearListing(lo7, hi7)
        print("[ok ] clearListing B7 (0x%08x..0x%08x)" % (B7_LO, B7_HI))
    except Exception as e:
        print("[warn] clearListing B7: %s" % e)
    _set_tmode(lo7, hi7)

    # Disassemble fn body (0x08073b1c..0x08073b43 = 40B; pool at 0x08073b44/0x08073b48)
    b7_fn_lo = _addr(0x08073b1c)
    b7_fn_hi = _addr(0x08073b43)
    cmd = DisassembleCommand(b7_fn_lo, AddressSet(b7_fn_lo, b7_fn_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm B7 fn body: %s" % cmd.getStatusMsg())
    else:
        print("[ok ] disasm B7 fn_eligible_reasoning @ 0x08073b1c (40B)")

    # Force DWords for literal pool
    for dw_addr in B7_POOL_DWORDS:
        _force_dword(dw_addr)

    # -----------------------------------------------------------------------
    # B8: reasoning_dispatch_sub_stubs @ 0x08073bc8
    # -----------------------------------------------------------------------
    print("\n--- B8: reasoning_dispatch_sub_stubs @ 0x08073bc8 ---")
    lo8 = _addr(B8_LO)
    hi8 = _addr(B8_HI)

    # clearListing + setTMode for entire B8 range
    try:
        clearListing(lo8, hi8)
        print("[ok ] clearListing B8 (0x%08x..0x%08x)" % (B8_LO, B8_HI))
    except Exception as e:
        print("[warn] clearListing B8: %s" % e)
    _set_tmode(lo8, hi8)

    # Disassemble each stub
    for sa, size, label in B8_STUBS:
        if size is not None:
            # Normal stub
            _disasm_stub(sa, size, label)
        else:
            # reasoning_sub_3c58: split around inline pool at 0x08073d12
            print("[info] reasoning_sub_3c58 @ 0x08073c58: split mode (inline pool @ 0x08073d12)")
            # Part 1: 0x08073c58..0x08073d11 = 186B (wait: 0x08073d12 - 0x08073c58 = 0xba = 186B)
            # Actually B8_POOL_START=0x08073d12, stub starts at 0x08073c58
            # Part 1 end = pool_start - 1 = 0x08073d11 (or byte before pool)
            p1_lo = _addr(sa)
            p1_size = B8_POOL_START - sa  # 0x08073d12 - 0x08073c58 = 0xba = 186B
            p1_hi = _addr(sa + p1_size - 1)
            cmd = DisassembleCommand(p1_lo, AddressSet(p1_lo, p1_hi), True)
            if not cmd.applyTo(currentProgram):
                print("[warn] disasm reasoning_sub_3c58 part1: %s" % cmd.getStatusMsg())
            else:
                print("[ok ] disasm reasoning_sub_3c58 part1 @ 0x08073c58 (%dB)" % p1_size)

            # Force DWords for inline pool (4 DWords: 0x08073d12/16/1a/1e)
            for dw_addr in B8_POOL_DWORDS:
                _force_dword(dw_addr)

            # Part 2: 0x08073d24..0x08073d41 = 30B
            # B8_CODE_RESUME=0x08073d24, next stub at 0x08073d42
            p2_lo = _addr(B8_CODE_RESUME)
            p2_size = 0x08073d42 - B8_CODE_RESUME  # = 0x1e = 30B
            p2_hi = _addr(B8_CODE_RESUME + p2_size - 1)
            cmd = DisassembleCommand(p2_lo, AddressSet(p2_lo, p2_hi), True)
            if not cmd.applyTo(currentProgram):
                print("[warn] disasm reasoning_sub_3c58 part2: %s" % cmd.getStatusMsg())
            else:
                print("[ok ] disasm reasoning_sub_3c58 part2 @ 0x08073d24 (%dB)" % p2_size)

    # -----------------------------------------------------------------------
    # B9: fn_eligible_reversal_quiz @ 0x08073fe0
    # -----------------------------------------------------------------------
    print("\n--- B9: fn_eligible_reversal_quiz @ 0x08073fe0 (pad @ 0x08073fde) ---")
    lo9 = _addr(B9_LO)
    hi9 = _addr(B9_HI)

    # clearListing + setTMode for B9 range (including 2-byte pad)
    try:
        clearListing(lo9, hi9)
        print("[ok ] clearListing B9 (0x%08x..0x%08x)" % (B9_LO, B9_HI))
    except Exception as e:
        print("[warn] clearListing B9: %s" % e)
    _set_tmode(lo9, hi9)

    # Disassemble fn body only (starts at 0x08073fe0, not the pad)
    b9_fn_lo = _addr(0x08073fe0)
    b9_fn_hi = _addr(0x08074003)   # 0x08073fe0 + 0x24 - 1 = 0x08074003 (before pool)
    cmd = DisassembleCommand(b9_fn_lo, AddressSet(b9_fn_lo, b9_fn_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm B9 fn body: %s" % cmd.getStatusMsg())
    else:
        print("[ok ] disasm B9 fn_eligible_reversal_quiz @ 0x08073fe0 (36B)")

    # Force DWords for literal pool
    for dw_addr in B9_POOL_DWORDS:
        _force_dword(dw_addr)

    # -----------------------------------------------------------------------
    # B10: reversal_quiz_dispatch_sub_stubs @ 0x08074080
    # -----------------------------------------------------------------------
    print("\n--- B10: reversal_quiz_dispatch_sub_stubs @ 0x08074080 ---")
    lo10 = _addr(B10_LO)
    hi10 = _addr(B10_HI)

    # clearListing + setTMode for entire B10 range
    try:
        clearListing(lo10, hi10)
        print("[ok ] clearListing B10 (0x%08x..0x%08x)" % (B10_LO, B10_HI))
    except Exception as e:
        print("[warn] clearListing B10: %s" % e)
    _set_tmode(lo10, hi10)

    # Disassemble each stub
    for sa, size, label in B10_STUBS:
        _disasm_stub(sa, size, label)

    # -----------------------------------------------------------------------
    # Dispatch table labels (structural labels in asm/09)
    # These label the .word dispatch tables between B7/B8 and B9/B10
    # -----------------------------------------------------------------------
    print("\n--- Dispatch table labels ---")
    for tbl_addr, tbl_label in DISPATCH_TABLE_LABELS:
        _add_label(tbl_addr, tbl_label)

    # -----------------------------------------------------------------------
    # Count instructions disassembled in each block
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [
        (B7_LO, B7_HI, "B7"),
        (B8_LO, B8_HI, "B8"),
        (B9_LO, B9_HI, "B9"),
        (B10_LO, B10_HI, "B10"),
    ]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions in 0x%08x..0x%08x" % (name, n, lo_int, hi_int))

    print("\n=== DisassembleF09Seg5bBlocks DONE ===")


main()
