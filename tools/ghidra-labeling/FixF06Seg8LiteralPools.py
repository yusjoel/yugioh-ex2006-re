# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF06Seg8LiteralPools.py -- Fix literal pool DWORD data in F06 Seg-8 disasm blocks
#
# After DisassembleF06Seg8Blocks.py ran, the literal pool entries inside
# Block2 and Block4 sub-fns were exported as raw .byte sequences because
# Ghidra did not have DWORD data items at those addresses.
# Also Block3's literal pool at 0x59ce8/0xce/0xcf0 needs DWORDs (not 0xce0/0xce4 which are code).
# Additionally, Block1's literal pool at 0x5955c/0x59560/0x59564 needs
# re-disasm of Block1 code area after proper pool handling.
#
# This script:
# 1. Creates DWORD data at all missing literal pool addresses in Block2, Block3, Block4
# 2. Re-clears and re-disassembles Block3 (0x8059cc8..0x8059cdf) to fix the code region
#    (must NOT createDWord at 0x8059ce0/ce4 which are instructions)
# 3. Re-disassembles Block1 code (0x8059c3c..0x805955b) after fixing
#
# Backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260614_071238-pre-F06Seg8 (taken before all changes)

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


def _create_dword_forced(addr_int):
    """Force a DWORD data item at addr_int, clearing any conflicting data first."""
    a = _addr(addr_int)
    hi = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.DWordDataType.dataType
    try:
        # Check if already correct
        existing = listing.getDataAt(a)
        if existing is not None and existing.getDataType().equals(dt):
            print("[DW ] already DWORD @ 0x%08x" % addr_int)
            return True
        # Clear conflicting instructions/data
        clearListing(a, hi)
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr_int)
        return True
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))
        return False


def _disasm_at(ep_int, block_lo, block_hi):
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


def _set_tmode(lo_addr, hi_addr):
    lo = _addr(lo_addr)
    hi = _addr(hi_addr)
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)


def main():
    print("=== FixF06Seg8LiteralPools (DRY=%s) ===" % DRY)
    n = 0

    # =========================================================================
    # 1. Block2 literal pool DWORDs (18 missing labels)
    #    All inside 0x08059588..0x080596eb
    # =========================================================================
    BLOCK2_POOLS = [
        0x080595a0,  # gDuelPhaseFlags
        0x080595a4,  # EQUIP_STEP_OFF
        0x080595cc,  # gDuelPhaseFlags
        0x080595d0,  # EQUIP_STEP_OFF
        0x080595f0,  # EQUIP_STEP_OFF
        0x0805960c,  # set_equip_activation_state_by_mode_alt+1 = 0x080905e9
        0x08059610,  # gDuelPhaseFlags
        0x08059614,  # EQUIP_STEP_OFF
        0x0805964c,  # ELIGIB_SPRITE_CTRL_OFF = 0x1d68
        0x08059650,  # gDuelPhaseFlags
        0x08059654,  # EQUIP_STEP_OFF
        0x08059668,  # gDuelPhaseFlags
        0x0805966c,  # EQUIP_STEP_OFF
        0x08059688,  # gDuelPhaseFlags
        0x0805968c,  # EQUIP_STEP_OFF
        0x080596b4,  # gDuelCardCtxBase = 0x0201e2a0
        0x080596b8,  # gP1LifePoints = 0x0201c4e0
        0x080596d0,  # EQUIP_STEP_OFF
    ]
    print("\n--- Block2 literal pool DWORDs (%d) ---" % len(BLOCK2_POOLS))
    for addr in BLOCK2_POOLS:
        if DRY:
            print("[dry] createDWord @ 0x%08x" % addr)
            n += 1
        else:
            if _create_dword_forced(addr):
                n += 1

    # =========================================================================
    # 2. Block3 literal pool DWORDs
    #    0x08059ce8 = gDuelPhaseFlags, 0x08059cec = EQUIP_STEP_OFF
    #    0x08059cf0 = ptr-to-table (already should be DWORD from prev run)
    #    NOTE: 0x08059ce0 and 0x08059ce4 are INSTRUCTIONS -- do NOT createDWord there
    # =========================================================================
    BLOCK3_POOLS = [
        0x08059ce8,  # gDuelPhaseFlags = 0x0201b290
        0x08059cec,  # EQUIP_STEP_OFF = 0x000004ac
        0x08059cf0,  # ptr-to-table = 0x08059cf4
    ]
    print("\n--- Block3 literal pool DWORDs (%d) ---" % len(BLOCK3_POOLS))

    # First re-clear and re-disasm Block3 CODE region (0x8059cc8..0x8059ce7)
    # to undo damage from previous createDWord(0x8059ce0/ce4) that cleared instructions
    BLOCK3_CODE_LO = 0x08059cc8
    BLOCK3_CODE_HI = 0x08059cdf  # inclusive end of code region (before literal pool at 0xce8)
    if DRY:
        print("[dry] clearListing+setTMode 0x%08x..0x%08x" % (BLOCK3_CODE_LO, BLOCK3_CODE_HI))
        print("[dry] disasm @ 0x%08x" % BLOCK3_CODE_LO)
        for addr in BLOCK3_POOLS:
            print("[dry] createDWord @ 0x%08x" % addr)
            n += 1
    else:
        # Re-clear the code region (was damaged by createDWord on instruction addresses)
        try:
            clearListing(_addr(BLOCK3_CODE_LO), _addr(BLOCK3_CODE_HI))
            print("[ok ] clearListing code region 0x%08x..0x%08x" % (BLOCK3_CODE_LO, BLOCK3_CODE_HI))
        except Exception as e:
            print("[warn] clearListing: %s" % e)
        _set_tmode(BLOCK3_CODE_LO, BLOCK3_CODE_HI)
        _disasm_at(BLOCK3_CODE_LO, BLOCK3_CODE_LO, BLOCK3_CODE_HI)
        # Now create DWORDs for the actual literal pool (AFTER code, so no conflict)
        for addr in BLOCK3_POOLS:
            if _create_dword_forced(addr):
                n += 1

    # =========================================================================
    # 3. Block4 literal pool DWORDs (4 missing)
    # =========================================================================
    BLOCK4_POOLS = [
        0x08059d30,  # gDuelPhaseFlags
        0x08059d34,  # EQUIP_STEP_OFF
        0x08059d50,  # EQUIP_STEP_OFF
        0x08059d8c,  # EQUIP_STEP_OFF
    ]
    print("\n--- Block4 literal pool DWORDs (%d) ---" % len(BLOCK4_POOLS))
    for addr in BLOCK4_POOLS:
        if DRY:
            print("[dry] createDWord @ 0x%08x" % addr)
            n += 1
        else:
            if _create_dword_forced(addr):
                n += 1

    # =========================================================================
    # 4. Block1 literal pool DWORDs - also need re-disasm of code after pool fix
    #    Block1 code: 0x8059c3c..0x8059c5b (before pool at 0x5955c)
    #    Literal pool: 0x8059c5c, 0x8059c60, 0x8059c64
    # =========================================================================
    BLOCK1_CODE_LO = 0x0805953c
    BLOCK1_CODE_HI = 0x0805955b  # inclusive end of code
    BLOCK1_POOLS = [
        0x0805955c,  # gDuelPhaseFlags
        0x08059560,  # EQUIP_STEP_OFF
        0x08059564,  # ptr-to-table (0x08059568)
    ]
    print("\n--- Block1 code re-disasm + literal pool DWORDs ---")
    if DRY:
        print("[dry] clearListing+setTMode 0x%08x..0x%08x" % (BLOCK1_CODE_LO, BLOCK1_CODE_HI))
        print("[dry] disasm @ 0x%08x" % BLOCK1_CODE_LO)
        for addr in BLOCK1_POOLS:
            print("[dry] createDWord @ 0x%08x" % addr)
            n += 1
    else:
        try:
            clearListing(_addr(BLOCK1_CODE_LO), _addr(BLOCK1_CODE_HI))
            print("[ok ] clearListing Block1 code 0x%08x..0x%08x" % (BLOCK1_CODE_LO, BLOCK1_CODE_HI))
        except Exception as e:
            print("[warn] clearListing Block1: %s" % e)
        _set_tmode(BLOCK1_CODE_LO, BLOCK1_CODE_HI)
        _disasm_at(BLOCK1_CODE_LO, BLOCK1_CODE_LO, BLOCK1_CODE_HI)
        for addr in BLOCK1_POOLS:
            if _create_dword_forced(addr):
                n += 1

    print("\n[done] total DWORDs created/checked=%d (DRY=%s)" % (n, DRY))


main()
