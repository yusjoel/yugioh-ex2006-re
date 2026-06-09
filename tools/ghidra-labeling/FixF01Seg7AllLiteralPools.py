# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF01Seg7AllLiteralPools.py -- f01 Seg-7 comprehensive literal pool fix
#
# Scans ALL instructions in blocks 2/3/4 for PC-relative ldr targets
# and creates DWORDs at each target address that falls within the block range.
# This is the comprehensive fix for all mis-decoded literal pool entries.
#
# Strategy:
#   1. Iterate all instructions in range [0x080211b4..0x0802385e)
#   2. For each ldr/ldrh etc instruction that uses PC-relative addressing
#      (i.e., has a memory ref to a literal pool address within the range),
#      clearListing + createDWord at that target
#
# Alternative (more reliable): scan ALL addresses in the range that Ghidra
# has marked as data or instructions, and if the 4 bytes form a "value"
# (not a valid instruction pair), convert to DWORD.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.address import AddressSet

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF01Seg7AllLiteralPools (DRY=%s) ===" % DRY)

    RANGES = [
        (0x080211b4, 0x08021278),  # Block2
        (0x0802134c, 0x08022e2c),  # Block3
        (0x08022eb8, 0x0802385e),  # Block4
    ]
    # Also fix orphan block literal pools (already fixed in FixF01Seg7OrphanBlock.py but re-verify)
    # (0x08021090, 0x0802114c),  # Block1 orphan

    listing = currentProgram.getListing()
    rm = currentProgram.getReferenceManager()
    dt = DWordDataType()

    # Collect all PC-relative ldr targets within block ranges
    ldr_targets = set()

    for lo_int, hi_int in RANGES:
        lo = _addr(lo_int)
        hi = _addr(hi_int - 1)

        # Iterate all instructions in range
        inst_iter = listing.getInstructions(lo, True)
        while inst_iter.hasNext():
            inst = inst_iter.next()
            if inst.getAddress().compareTo(hi) > 0:
                break

            # Check for memory references from this instruction
            refs = rm.getReferencesFrom(inst.getAddress())
            for ref in refs:
                tgt = ref.getToAddress()
                tgt_int = tgt.getOffset()
                # Only care about targets within our blocks
                in_range = False
                for lo2, hi2 in RANGES:
                    if lo2 <= tgt_int < hi2:
                        in_range = True
                        break
                if in_range:
                    ldr_targets.add(tgt_int)

    print("[scan] Found %d PC-relative ldr targets" % len(ldr_targets))

    nok = nfail = 0
    for tgt_int in sorted(ldr_targets):
        if DRY:
            print("[dry] createDWord @ 0x%08x" % tgt_int)
            nok += 1
            continue
        try:
            addr = _addr(tgt_int)
            clearListing(addr, _addr(tgt_int + 3))
            du = listing.createData(addr, dt)
            if du is not None:
                nok += 1
            else:
                nfail += 1
        except Exception as e:
            print("[warn] @ 0x%08x: %s" % (tgt_int, e))
            nfail += 1

    print("=== DONE: ok=%d fail=%d ===" % (nok, nfail))


main()
