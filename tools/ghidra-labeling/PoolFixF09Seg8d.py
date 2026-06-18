# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# PoolFixF09Seg8d.py -- p5 file09 Seg-8 literal pool fix pass D (comprehensive)
#
# Problem: When clearListing a code range that includes pool DWords, Ghidra
# reverts the pool DWords back to .byte after re-disasm. Solution: clearListing
# ONLY the code sections (split at pool boundaries), then disasm each piece.
#
# B2 block 0x765f0..0x7678b:
# Known pool DWord clusters (all already force_dword'd from passes A/B):
#   0x0807666c..0x0807667b: 4 DWords (gP1LifePoints, PLAYER_BLOCK_STRIDE, EWRAM, code ptr)
#   0x08076688..0x0807668b: 1 DWord (code ptr)
#   0x080766a4..0x080766a7: 1 DWord (PLAYER_BLOCK_STRIDE)
#   0x080766c8..0x080766cf: 2 DWords (gDuelPhaseFlags, gP1LifePoints)
#   0x080766d0..0x080766d3: 1 DWord (LP_BANISHER_CTX_OFF)
#   0x08076714..0x08076717: 1 DWord (PLAYER_BLOCK_STRIDE)
#   0x08076718..0x0807671b: 1 DWord (gP1FieldArrayCBase)
#   0x0807671c..0x0807671f: 1 DWord (DARK_SCORPION_CHICK_CID)
#   0x08076720..0x08076723: 1 DWord (DARK_SCORPION_BURGLARS_CID)
#   0x08076734..0x08076737: 1 DWord (DARK_SCORPION_GORG_THE_STRONG_CID)
#
# Code sections to re-disasm (split around pools):
# 1. sub_65f0 body: 0x080765f0..0x0807666b (ends before pool cluster at 0x666c)
# 2. sub_6616 body (after pool at 0x678): 0x0807667c..0x08076687 (before pool at 0x688)
# 3. sub_6616 continued (after pool at 0x688): 0x0807668c..0x080766a3 (before pool at 0x6a4)
# 4. sub_66a8 body: 0x080766a8..0x080766c7 (before pool at 0x6c8)
# 5. sub_66d8 body: 0x080766d4..0x08076713 (skip over pool at 0x6d0 which is inside)
#    -- Actually: sub_66d8: 0x080766d8..0x08076713 (pool at 0x6d0 is before sub_66d8)
#    Wait: 0x080766d4 is LAB_080766d4 (movs r0), 0x080766d8 is sub_66d8 start
# 6. sub_66d8 body part 2: 0x08076724..0x08076733 (between pools at 0x720 and 0x734)
# 7. sub_66d8 body part 3: 0x08076738..0x0807677f (after pool at 0x734, up to sub_6780)
# 8. sub_6780 body: 0x08076780..0x0807678b
#
# For the .byte stubs (between pool and next stub) like the 2B/6B padding:
# Those are automatically handled by Ghidra

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# All pool DWords to ensure are DWordDataType BEFORE disasm
POOL_DWORDS = [
    # B2 cluster 1 at 0x666c
    (0x0807666c, 0x0201c4e0),
    (0x08076670, 0x00000868),
    (0x08076674, 0x0201e2a8),
    (0x08076678, 0x08076511),
    # B2 cluster 2 at 0x688
    (0x08076688, 0x08076511),
    # B2 cluster 3 at 0x6a4
    (0x080766a4, 0x00000868),
    # B2 cluster 4 at 0x6c8
    (0x080766c8, 0x0201b290),
    (0x080766cc, 0x0201c4e0),
    # B2 cluster 5 at 0x6d0
    (0x080766d0, 0x00001d70),
    # B2 cluster 6 at 0x714
    (0x08076714, 0x00000868),
    # B2 cluster 7 at 0x718
    (0x08076718, 0x0201c600),
    # B2 cluster 8 at 0x71c
    (0x0807671c, 0x00001656),
    # B2 cluster 9 at 0x720
    (0x08076720, 0x00001531),
    # B2 cluster 10 at 0x734
    (0x08076734, 0x00001685),
    # B4 cluster at 0x884
    (0x08076884, 0x0201c4e0),
    (0x08076888, 0x00000868),
    # B4 cluster at 0x88c
    (0x0807688c, 0xfffffeec),
]

# Code sections to (re-)disassemble in B2, NOT including pool addresses.
# Order matters: do these AFTER all force_dwords.
CODE_SECTIONS = [
    # B2 sub_65f0: 0x765f0..0x7666b (ends just before pool cluster at 0x666c)
    (0x080765f0, 0x0807666b, 'mustering_dark_scorpions_sub_65f0_body'),
    # B2 code after pool cluster (0x666c..0x667b): 0x7667c..0x76687
    (0x0807667c, 0x08076687, 'mustering_dark_scorpions_after_pool_cluster1'),
    # B2 code after pool at 0x688 (single DWord): 0x7668c..0x766a3
    (0x0807668c, 0x080766a3, 'mustering_dark_scorpions_after_pool_688'),
    # B2 sub_66a8: 0x766a8..0x766c7 (ends before pool at 0x6c8)
    (0x080766a8, 0x080766c7, 'mustering_dark_scorpions_sub_66a8_body'),
    # B2 code: 0x766d4..0x766d7 (LAB_766d4: movs + b; between pool 0x6d0 and sub_66d8)
    (0x080766d4, 0x080766d7, 'mustering_dark_scorpions_lab_66d4'),
    # B2 sub_66d8: 0x766d8..0x76713 (ends before pool at 0x714)
    (0x080766d8, 0x08076713, 'mustering_dark_scorpions_sub_66d8_body'),
    # B2 code: 0x76722..0x76733 (after pool at 0x720, before pool at 0x734)
    (0x08076722, 0x08076733, 'mustering_dark_scorpions_sub_66d8_part2'),
    # B2 code: 0x76738..0x7677f (after pool at 0x734, up to sub_6780)
    (0x08076738, 0x0807677f, 'mustering_dark_scorpions_sub_66d8_part3'),
    # B2 sub_6780: 0x76780..0x7678b
    (0x08076780, 0x0807678b, 'mustering_dark_scorpions_sub_6780_body'),
    # B4: spell_vanishing_sub_67f8..before pool at 0x884
    (0x080767f8, 0x08076883, 'spell_vanishing_sub_stubs_before_pool884'),
    # B4: code after pool at 0x88c
    (0x08076890, 0x08076907, 'spell_vanishing_sub_stubs_after_pool88c'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(addr_int, expected_val):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        return actual == (expected_val & 0xFFFFFFFF)
    except Exception:
        return False

def _force_dword(addr_int, expected_val):
    if not _check(addr_int, expected_val):
        print("[FAIL] _check 0x%08x: expected 0x%08x, got 0x%08x" % (
            addr_int, expected_val & 0xFFFFFFFF,
            currentProgram.getMemory().getInt(_addr(addr_int)) & 0xFFFFFFFF))
        return
    if DRY:
        print("[dry] force_dword 0x%08x (0x%08x)" % (addr_int, expected_val & 0xFFFFFFFF))
        return
    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword 0x%08x (0x%08x)" % (addr_int, expected_val & 0xFFFFFFFF))
    except Exception as e:
        print("[warn] force_dword createData 0x%08x: %s" % (addr_int, e))

def _set_tmode(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)

def _disasm_section(sa, hi, label):
    if DRY:
        print("[dry] disasm %s 0x%08x..0x%08x" % (label, sa, hi))
        return
    # clearListing ONLY this code section (not pools)
    stub_lo = _addr(sa)
    stub_hi = _addr(hi)
    try:
        clearListing(stub_lo, stub_hi)
    except Exception as e:
        print("[warn] clearListing 0x%08x: %s" % (sa, e))
    _set_tmode(sa, hi)
    cmd = DisassembleCommand(stub_lo, AddressSet(stub_lo, stub_hi), True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm %s @ 0x%08x: %s" % (label, sa, cmd.getStatusMsg()))
    else:
        print("[ok ] disasm %s 0x%08x..0x%08x" % (label, sa, hi))

def main():
    print("=== PoolFixF09Seg8d (DRY=%s) ===" % DRY)
    print("  %d pool DWords + %d code sections" % (len(POOL_DWORDS), len(CODE_SECTIONS)))

    print("\n--- Step 1: force_dword all pools ---")
    for (addr, val) in POOL_DWORDS:
        _force_dword(addr, val)

    print("\n--- Step 2: disasm code sections (avoiding pools) ---")
    for (sa, hi, label) in CODE_SECTIONS:
        _disasm_section(sa, hi, label)

    print("\n=== PoolFixF09Seg8d DONE ===")

main()
