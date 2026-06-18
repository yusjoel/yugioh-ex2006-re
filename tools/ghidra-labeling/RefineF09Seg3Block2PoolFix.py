# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF09Seg3Block2PoolFix.py -- Fix Block2 literal pool words in F09 Seg-3
#
# Problem: After RefineF09Seg3Disasm.py, Ghidra exported some Block2 literal
# pool words as .byte sequences without proper per-word labels. This causes
# "invalid offset" GAS errors because DAT_08071778 / DAT_080717a0 / DAT_080717b8
# are referenced by ldr instructions but not defined as labels.
#
# Block2 literal pools (inside 0x08071754..0x080717ef):
#   0x08071774: 0x00000874 (equip field offset 0x874 = stride+0xc)
#   0x08071778: 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
#   0x080717a0: 0x00001da8 (LP_CARD_TRACK_BASE_OFF)
#   0x080717b8: 0x000004a4 (EQUIP_PHASE_FRAME_OFF again)
#
# Fix: clearListing at each pool word, createDWord, createLabel.
#
# NOTE: All text is pure ASCII.
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_220254-pre-F09Seg3

from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (addr, value, label, eol)
POOL_WORDS = [
    (0x08071774, 0x00000874, 'dat_08071774_pool',
     '0x874=PLAYER_BLOCK_STRIDE(0x868)+0xc; literal pool equip_lp_sub_754'),
    (0x08071778, 0x000004a4, 'dat_08071778_pool',
     'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool equip_lp_sub_754'),
    (0x080717a0, 0x00001da8, 'dat_080717a0_pool',
     'LP_CARD_TRACK_BASE_OFF=0x1da8; literal pool equip_lp_sub_78a'),
    (0x080717b8, 0x000004a4, 'dat_080717b8_pool',
     'EQUIP_PHASE_FRAME_OFF=0x4a4; literal pool equip_lp_sub_7a4'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_val(addr, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] read 0x%08x: %s" % (addr, e))
        return False
    if actual != (expected & 0xFFFFFFFF):
        print("[FAIL] 0x%08x: got 0x%08x expected 0x%08x" % (addr, actual, expected & 0xFFFFFFFF))
        return False
    return True


def main():
    print("=== RefineF09Seg3Block2PoolFix (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()

    ok = fail = 0
    for addr, value, label, eol in POOL_WORDS:
        if not _check_val(addr, value):
            print("[SKIP] 0x%08x value mismatch" % addr)
            fail += 1
            continue

        if DRY:
            print("[dry] createDWord @ 0x%08x  label=%s  eol=%s" % (addr, label, eol[:40]))
            ok += 1
            continue

        a = _addr(addr)
        try:
            clearListing(a, _addr(addr + 3))
        except Exception as e:
            print("[WARN] clearListing @ 0x%08x: %s" % (addr, e))

        d = listing.createData(a, DWordDataType.dataType)
        if d is None:
            print("[WARN] createData failed @ 0x%08x" % addr)
        else:
            print("[POOL] created DWord @ 0x%08x" % addr)

        existing = [s.getName() for s in sym_tbl.getSymbols(a)]
        if label not in existing:
            sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)

        if eol:
            bad = any(ord(ch) > 127 for ch in eol)
            if not bad:
                cu = listing.getCodeUnitAt(a)
                if cu is not None:
                    cu.setComment(CodeUnit.EOL_COMMENT, eol)

        print("[POOL] 0x%08x  label=%s" % (addr, label))
        ok += 1

    print("\n  Pool fix done: %d ok, %d fail" % (ok, fail))
    print("=== RefineF09Seg3Block2PoolFix DONE ===")


main()
