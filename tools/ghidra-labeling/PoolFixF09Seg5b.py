# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg5b.py -- fix inline literal pool DWords for Seg-5b B7/B8/B9/B10
#
# Problem: DisassembleF09Seg5bBlocks.py used wrong pool addresses for:
#   - B8 sub_3bc8: pool needs force_dword at 0x08073bf0, 0x08073bf4
#   - B8 sub_3c0c: pool needs force_dword at 0x08073c44, 0x08073c48, 0x08073c4c
#   - B8 sub_3c58: force_dword was applied at 0x08073d12/16/1a/1e (pad+pool),
#     but correct pool DWords are at 0x08073d14/18/1c/20 (4 bytes after pad)
#   - B10 sub_4080: pool at 0x080740b8/bc/c0 + 0x080740e4
#   - B10 sub_40e8: pool at 0x0807410c/10
#   - B10 sub_4148: pool at 0x08074170/74/78
#   - B10 sub_41e4 area: pool at 0x080741dc/e0
#
# Also: incorrect DWords at 0x08073d12/16/1a/1e need to be cleared (4B each)
# and replaced by 2B undefined pad + 4 correct DWords starting at 0x08073d14.
# Same for 0x080740b6 and 0x080740e2.
#
# Strategy:
# 1. clearListing entire B8 and B10 ranges again
# 2. Re-run setTMode
# 3. Redo per-stub disasm
# 4. Force correct DWords for ALL inline pools
# 5. Redo dispatch table for sub_3bc8/3c0c sections (the branches to code after pools)

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
# All inline literal pool DWord addresses (4-byte aligned, correct)
# ---------------------------------------------------------------------------
# B8
B8_POOL_DWORDS = [
    # sub_3bc8 pool (0x08073bf0..0x08073bf7, 2 DWords)
    0x08073bf0,   # gP1LifePoints = 0x0201c4e0
    0x08073bf4,   # PLAYER_BLOCK_STRIDE = 0x00000868
    # sub_3c0c pool (0x08073c44..0x08073c4f, 3 DWords; 2B pad at 0x08073c42)
    0x08073c44,   # EQUIP_PHASE_FRAME_OFF = 0x000004a4
    0x08073c48,   # gP1LifePoints = 0x0201c4e0
    0x08073c4c,   # offset 0x00001da8
    # sub_3c58 pool (0x08073d14..0x08073d23, 4 DWords; 2B pad at 0x08073d12)
    # OLD (wrong): 0x08073d12, 0x08073d16, 0x08073d1a, 0x08073d1e
    0x08073d14,   # gP1LifePoints = 0x0201c4e0
    0x08073d18,   # PLAYER_BLOCK_STRIDE = 0x00000868
    0x08073d1c,   # gDuelPhaseFlags = 0x0201b290
    0x08073d20,   # EQUIP_PHASE_FRAME_OFF = 0x000004a4
]

# B10
B10_POOL_DWORDS = [
    # sub_4080 pool 1 (0x080740b8..0x080740c3, 3 DWords; 2B pad at 0x080740b6)
    0x080740b8,   # gP1LifePoints = 0x0201c4e0
    0x080740bc,   # PLAYER_BLOCK_STRIDE = 0x00000868
    0x080740c0,   # 0x0201e2a0
    # sub_4080 pool 2 (0x080740e4..0x080740e7, 1 DWord; 2B pad at 0x080740e2)
    0x080740e4,   # 0x000001b9
    # sub_40e8 pool (0x0807410c..0x08074113, 2 DWords)
    0x0807410c,   # EQUIP_PHASE_FRAME_OFF = 0x000004a4
    0x08074110,   # gP1LifePoints = 0x0201c4e0
    # sub_4148 pool (0x08074170..0x0807417b, 3 DWords)
    0x08074170,   # PLAYER_BLOCK_STRIDE = 0x00000868
    0x08074174,   # 0x0201c740
    0x08074178,   # EQUIP_PHASE_FRAME_OFF = 0x000004a4
    # sub_4148 pool 2 (0x080741dc..0x080741e3, 2 DWords)
    0x080741dc,   # gP1LifePoints = 0x0201c4e0
    0x080741e0,   # PLAYER_BLOCK_STRIDE = 0x00000868
]

# Block ranges for clearListing + setTMode
B8_LO = 0x08073bc8
B8_HI = 0x08073d83

B10_LO = 0x08074080
B10_HI = 0x080741f7

# B8 sub-stub entry points and sizes
# stub[3] (reasoning_sub_3c58) needs split handling around sub_3c58 pool
B8_STUBS = [
    (0x08073bc8, 68,   'reasoning_sub_3bc8'),   # 68B
    (0x08073c0c, 68,   'reasoning_sub_3c0c'),   # 68B
    (0x08073c50, 8,    'reasoning_sub_3c50'),   # 8B
    (0x08073c58, None, 'reasoning_sub_3c58'),   # split: 186B + 30B
    (0x08073d42, 6,    'reasoning_sub_3d42'),   # 6B
    (0x08073d48, 16,   'reasoning_sub_3d48'),   # 16B
    (0x08073d58, 18,   'reasoning_sub_3d58'),   # 18B
    (0x08073d6a, 10,   'reasoning_sub_3d6a'),   # 10B
    (0x08073d74, 16,   'reasoning_default_3d74'), # 16B
]

# B10 sub-stub entry points and sizes
B10_STUBS = [
    (0x08074080, 104, 'reversal_quiz_sub_4080'),
    (0x080740e8, 44,  'reversal_quiz_sub_40e8'),
    (0x08074114, 52,  'reversal_quiz_sub_4114'),
    (0x08074148, 156, 'reversal_quiz_sub_4148'),
    (0x080741e4, 10,  'reversal_quiz_sub_41e4'),
    (0x080741ee, 10,  'reversal_quiz_default_41ee'),
]

# B8 sub_3c58 split details
B8_SUB3C58_PART1_START = 0x08073c58
B8_SUB3C58_PAD_ADDR = 0x08073d12   # 2B pad here
B8_SUB3C58_POOL_START = 0x08073d14  # correct pool start
B8_SUB3C58_PART2_START = 0x08073d24 # code resumes here (b+pad+pool = 0x10+0xe = end at 0x08073d24)
B8_SUB3C58_PART2_END = 0x08073d42  # exclusive (next stub)

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
    stub_lo = _addr(sa)
    stub_hi = _addr(sa + size - 1)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s @ 0x%08x (%dB)" % (label, sa, size))

def _force_dword_4b(addr_int):
    """Clear 4 bytes only and create DWord at the correct 4-byte aligned address."""
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing4b @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print("=== PoolFixF09Seg5b (DRY=%s) ===" % DRY)
    print("  Fix inline literal pool DWords for B8/B10")

    if DRY:
        print("[dry] would clearListing B8(%d stubs) + B10(%d stubs) + force_dword(%d+%d pools)" % (
            len(B8_STUBS), len(B10_STUBS), len(B8_POOL_DWORDS), len(B10_POOL_DWORDS)))
        return

    listing = currentProgram.getListing()

    # -----------------------------------------------------------------------
    # Re-clear and re-disasm B8
    # -----------------------------------------------------------------------
    print("\n--- Re-clearing B8 (0x08073bc8..0x08073d83) ---")
    lo8 = _addr(B8_LO)
    hi8 = _addr(B8_HI)
    try:
        clearListing(lo8, hi8)
        print("[ok ] clearListing B8")
    except Exception as e:
        print("[warn] clearListing B8: %s" % e)
    _set_tmode(lo8, hi8)

    print("\n--- Re-disasm B8 stubs ---")
    for sa, size, label in B8_STUBS:
        if size is not None:
            _disasm_stub(sa, size, label)
        else:
            # reasoning_sub_3c58: split mode
            # Part 1: 0x08073c58 to 0x08073d11 (186B = 0x08073d12 - 0x08073c58)
            p1_size = B8_SUB3C58_PAD_ADDR - sa   # = 0x08073d12 - 0x08073c58 = 0xba = 186B
            p1_lo = _addr(sa)
            p1_hi = _addr(sa + p1_size - 1)
            cmd = DisassembleCommand(p1_lo, AddressSet(p1_lo, p1_hi), True)
            if not cmd.applyTo(currentProgram):
                print("[warn] reasoning_sub_3c58 part1: %s" % cmd.getStatusMsg())
            else:
                print("[ok ] reasoning_sub_3c58 part1 @ 0x%08x (%dB)" % (sa, p1_size))

            # force_dword x4 at correct pool start (0x08073d14)
            for dw in [B8_SUB3C58_POOL_START,
                       B8_SUB3C58_POOL_START+4,
                       B8_SUB3C58_POOL_START+8,
                       B8_SUB3C58_POOL_START+12]:
                _force_dword_4b(dw)

            # Part 2: 0x08073d24 to 0x08073d41 (30B)
            p2_size = B8_SUB3C58_PART2_END - B8_SUB3C58_PART2_START  # = 0x08073d42 - 0x08073d24 = 0x1e = 30B
            p2_lo = _addr(B8_SUB3C58_PART2_START)
            p2_hi = _addr(B8_SUB3C58_PART2_START + p2_size - 1)
            cmd = DisassembleCommand(p2_lo, AddressSet(p2_lo, p2_hi), True)
            if not cmd.applyTo(currentProgram):
                print("[warn] reasoning_sub_3c58 part2: %s" % cmd.getStatusMsg())
            else:
                print("[ok ] reasoning_sub_3c58 part2 @ 0x08073d24 (%dB)" % p2_size)

    print("\n--- Force DWords for B8 inline pools ---")
    for dw_addr in B8_POOL_DWORDS:
        _force_dword_4b(dw_addr)

    # -----------------------------------------------------------------------
    # Re-clear and re-disasm B10
    # -----------------------------------------------------------------------
    print("\n--- Re-clearing B10 (0x08074080..0x080741f7) ---")
    lo10 = _addr(B10_LO)
    hi10 = _addr(B10_HI)
    try:
        clearListing(lo10, hi10)
        print("[ok ] clearListing B10")
    except Exception as e:
        print("[warn] clearListing B10: %s" % e)
    _set_tmode(lo10, hi10)

    print("\n--- Re-disasm B10 stubs ---")
    for sa, size, label in B10_STUBS:
        _disasm_stub(sa, size, label)

    print("\n--- Force DWords for B10 inline pools ---")
    for dw_addr in B10_POOL_DWORDS:
        _force_dword_4b(dw_addr)

    # -----------------------------------------------------------------------
    # Count results
    # -----------------------------------------------------------------------
    print("\n--- Instruction counts ---")
    for lo_int, hi_int, name in [(B8_LO, B8_HI, "B8"), (B10_LO, B10_HI, "B10")]:
        lo_a = _addr(lo_int)
        hi_a = _addr(hi_int)
        n = 0
        inst = listing.getInstructionAt(lo_a)
        while inst is not None and inst.getAddress().compareTo(hi_a) <= 0:
            n += 1
            inst = listing.getInstructionAfter(inst.getAddress())
        print("  %s: %d instructions" % (name, n))

    print("\n=== PoolFixF09Seg5b DONE ===")


main()
