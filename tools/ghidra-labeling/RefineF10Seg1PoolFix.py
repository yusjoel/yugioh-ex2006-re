# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg1PoolFix.py -- f10 Seg-1 literal pool force-split fix
#   After DisassembleF10Seg1Blocks.py, sub-stub inline literal pool words
#   were emitted as .byte blobs by ExportRangeToGas -- causing GAS
#   "invalid offset, value too big (0xFFFFFFFC)" errors.
#   This script calls createDWord on each pool address to force individual
#   4B DWORD items, so the exporter emits proper .word lines.
#
# Pool addresses identified from build errors (all within BLK2/4/6/8):
#   BLK2 (0x7a00c/0xe8): 0x7a07c, 0x7a080, 0x7a084 (3 words)
#   BLK4 (0x7a178/0x14c): 0x7a158, 0x7a15c, 0x7a208, 0x7a20c, 0x7a238, 0x7a23c,
#                          0x7a2aa(align), 0x7a2ac, 0x7a2b0, 0x7a2b4
#   BLK6 (0x7a464/0x11c): 0x7a52c, 0x7a530, 0x7a55c
#   BLK8 (0x7a71c/0xf8):  0x7a72c, 0x7a778, 0x7a798, 0x7a7e0, 0x7a7e4, 0x7a810
#
# NOTE: Only force-split word-aligned pool addresses. Do NOT split non-word-aligned bytes.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# All pool word addresses that need createDWord (4B word-aligned)
POOL_ADDRS = [
    # BLK2 (0x0807a07c blob: gP1LifePoints 0x0201c4e0, LP_CARD_TRACK_NEXT_OFF 0x1daa, PLAYER_BLOCK_STRIDE 0x868)
    0x0807a07c,  # 0x0201c4e0 (gP1LifePoints)
    0x0807a080,  # 0x00001daa (LP_CARD_TRACK_NEXT_OFF)
    0x0807a084,  # 0x00000868 (PLAYER_BLOCK_STRIDE)

    # BLK4 (0x0807a158 blob: gDuelPhaseFlags 0x0201b290 + fn-ptr 0x0807a160)
    0x0807a158,  # 0x0201b290 (gDuelPhaseFlags)
    0x0807a15c,  # 0x0807a160 (dispatch table ptr)

    # BLK4 (0x0807a208 blob: gDuelCardCtxBase 0x0201e2a0 + gP1LifePoints 0x0201c4e0)
    0x0807a208,  # 0x0201e2a0 (gDuelCardCtxBase)
    0x0807a20c,  # 0x0201c4e0 (gP1LifePoints)

    # BLK4 (0x0807a238 blob: gP1LifePoints + 0x11d)
    0x0807a238,  # 0x0201c4e0 (gP1LifePoints)
    0x0807a23c,  # 0x0000011d or similar constant

    # BLK4 (0x0807a2aa/0x2b area: 2-byte pad + gDuelPhaseFlags + EQUIP_PHASE_FRAME_OFF + gP1LifePoints)
    # 0x7a2aa and 0x7a2ab are alignment bytes (not pool words), skip them
    0x0807a2ac,  # 0x0201b290 (gDuelPhaseFlags)
    0x0807a2b0,  # 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
    0x0807a2b4,  # 0x0201c4e0 (gP1LifePoints)

    # BLK6 (0x0807a52c/0x530 blob: 0x00001803 + gDuelPhaseFlags or similar)
    0x0807a52c,  # pool word at BLK6+0xc8
    0x0807a530,  # pool word at BLK6+0xcc
    0x0807a55c,  # pool word (1 dword: 0x00001803 CID)

    # BLK8 (various pool blobs)
    0x0807a72c,  # pool word (0x000004a4 EQUIP_PHASE_FRAME_OFF)
    0x0807a778,  # pool word (0x00001daa LP_CARD_TRACK_NEXT_OFF)
    0x0807a798,  # pool word (0x000004a4)
    0x0807a7e0,  # 0x0201b290 (gDuelPhaseFlags)
    0x0807a7e4,  # 0x000004a4 (EQUIP_PHASE_FRAME_OFF)
    0x0807a810,  # pool word at BLK8+0xf4
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _create_dword(addr_int):
    a = _addr(addr_int)
    listing = currentProgram.getListing()
    dt = DWordDataType.dataType
    try:
        listing.clearCodeUnits(a, _addr(addr_int + 3), False)
        listing.createData(a, dt)
        print("[dword ok] 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))


def main():
    print("=== RefineF10Seg1PoolFix (DRY=%s) ===" % DRY)
    if DRY:
        print("[dry] would createDWord at %d pool addresses" % len(POOL_ADDRS))
        for a in POOL_ADDRS:
            print("[dry] 0x%08x" % a)
        return
    for a in POOL_ADDRS:
        _create_dword(a)
    print("=== PoolFix Done: %d addresses ===" % len(POOL_ADDRS))


main()
