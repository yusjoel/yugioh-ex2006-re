# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg8bLiteralPools.py -- Fix literal pool DWORD labels in F08 Seg-8b
#
# Problem: After disassembly of 5 blocks, literal pool words within the blocks
# were exported as large .byte sequences without individual DAT_ labels.
# GAS then fails with "invalid offset, value too big" on ldr DAT_XXXXXXXX refs.
#
# Solution: Force createDWord at each missing literal pool address, then re-export.
# This creates individual DWORD data items with DAT_ labels in Ghidra, which
# the exporter will then emit as separate labeled .word lines.
#
# 32 missing DAT_ addresses (from build error analysis):
#   Block1 literal pool (0x0806b784..0x0806b7cf):
#     0x0806b7c4, 0x0806b7c8, 0x0806b7cc
#   Block2 literal pools (0x0806b7fc..0x0806ba77):
#     0x0806b8a0, 0x0806b8a4
#     0x0806b938, 0x0806b93c, 0x0806b940
#     0x0806b98c
#     0x0806b9e4, 0x0806b9e8, 0x0806b9ec
#     0x0806ba20
#     0x0806ba50
#   Block3 literal pool (0x0806bb74..0x0806bbb7):
#     0x0806bbb0, 0x0806bbb4
#   Block4 literal pools (0x0806bc2c..0x0806bf9f):
#     0x0806bd18, 0x0806bd1c, 0x0806bd20
#     0x0806bd44, 0x0806bd48
#     0x0806bd9c
#     0x0806beec, 0x0806bef0, 0x0806bef4, 0x0806bef8, 0x0806befc, 0x0806bf00, 0x0806bf04, 0x0806bf08, 0x0806bf0c
#   Block5 literal pool (0x0806bfbc..0x0806c0cb):
#     0x0806c028
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_053928-pre-F08Seg8b

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# All 32 missing literal pool DWORD addresses
MISSING_POOL_ADDRS = [
    # Block1 literal pool (check_equip_eligible_cid_135b at 0x0806b784)
    0x0806b7c4,  # DAT_0806b7c4
    0x0806b7c8,  # DAT_0806b7c8
    0x0806b7cc,  # DAT_0806b7cc
    # Block2 literal pools (cid_135b state stubs)
    0x0806b8a0,  # DAT_0806b8a0 (in cid_135b_state_stub_b8a8 area)
    0x0806b8a4,  # DAT_0806b8a4
    0x0806b938,  # DAT_0806b938 (in cid_135b_state_stub_b8d4 area)
    0x0806b93c,  # DAT_0806b93c
    0x0806b940,  # DAT_0806b940
    0x0806b98c,  # DAT_0806b98c (in cid_135b_state_stub_b950 area)
    0x0806b9e4,  # DAT_0806b9e4 (in cid_135b_state_stub_b990 area)
    0x0806b9e8,  # DAT_0806b9e8
    0x0806b9ec,  # DAT_0806b9ec
    0x0806ba20,  # DAT_0806ba20 (in cid_135b_state_stub_ba00 area)
    0x0806ba50,  # DAT_0806ba50 (in cid_135b_state_stub_ba28 area)
    # Block3 literal pool (check_equip_eligible_magical_hats at 0x0806bb74)
    0x0806bbb0,  # DAT_0806bbb0 (.word gDuelPhaseFlags)
    0x0806bbb4,  # DAT_0806bbb4 (.word 0x0806bbb8 = 29-entry jump table)
    # Block4 literal pools (Magical Hats state stubs)
    0x0806bd18,  # DAT_0806bd18 (in magical_hats_state_stub_bc2c area)
    0x0806bd1c,  # DAT_0806bd1c
    0x0806bd20,  # DAT_0806bd20
    0x0806bd44,  # DAT_0806bd44 (in magical_hats_state_stub_bc86 area)
    0x0806bd48,  # DAT_0806bd48
    0x0806bd9c,  # DAT_0806bd9c (in magical_hats_state_stub_bcaa area)
    0x0806beec,  # DAT_0806beec (in magical_hats_state_stub_bdf2 area - large)
    0x0806bef0,  # DAT_0806bef0
    0x0806bef4,  # DAT_0806bef4
    0x0806bef8,  # DAT_0806bef8
    0x0806befc,  # DAT_0806befc
    0x0806bf00,  # DAT_0806bf00
    0x0806bf04,  # DAT_0806bf04
    0x0806bf08,  # DAT_0806bf08
    0x0806bf0c,  # DAT_0806bf0c
    # Block5 literal pool (magical_hats_zone_state_stub_bfbc area)
    0x0806c028,  # DAT_0806c028
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _force_dword(addr):
    a = _addr(addr)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()

    if DRY:
        print("[dry] DWORD 0x%08x" % addr)
        return True

    # Clear any existing code/data at this address
    existing = listing.getDataAt(a)
    if existing is not None and existing.getLength() == 4:
        # Check if label already exists
        syms = list(sym_tbl.getSymbols(a))
        if syms:
            print("[SKIP] DWORD 0x%08x: already has label(s) %s" % (
                addr, [s.getName() for s in syms]))
            return True

    # Clear and create DWORD
    try:
        clearListing(a, a)
    except Exception as e:
        print("[warn] clearListing 0x%08x: %s" % (addr, e))

    try:
        listing.createData(a, DWordDataType.dataType)
        print("[DWORD] created at 0x%08x" % addr)
        return True
    except Exception as e:
        print("[FAIL] createDWord 0x%08x: %s" % (addr, e))
        return False


def main():
    print("=== FixF08Seg8bLiteralPools (DRY=%s) ===" % DRY)
    print("  Fixing %d missing literal pool DWORD labels" % len(MISSING_POOL_ADDRS))

    ok = fail = 0
    for addr in MISSING_POOL_ADDRS:
        if _force_dword(addr):
            ok += 1
        else:
            fail += 1

    print("\n=== FixF08Seg8bLiteralPools DONE ===")
    print("  DWORD created: %d ok, %d fail" % (ok, fail))
    if fail > 0:
        print("  !!! %d FAILURES -- check output !!!" % fail)
    else:
        print("  All literal pool DWORDs created. Re-export and rebuild.")


main()
