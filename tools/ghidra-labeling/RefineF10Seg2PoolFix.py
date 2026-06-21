# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF10Seg2PoolFix.py -- f10 Seg-2 literal pool force-split fix
#   After DisassembleF10Seg2Blocks.py, sub-stub inline literal pool words
#   were emitted as .byte blobs or ROM_INCBIN by ExportRangeToGas,
#   causing GAS "invalid offset, value too big (0xFFFFFFFC)" errors.
#   This script calls createDWord on each pool address to force 4B DWORD items.
#
# Pool addresses from build errors and ROM_INCBIN residuals (BLK2/4/6/8):
#
#   BLK2 (0x7afb8..0x7b0c8):
#     0x7afe8, 0x7afec  (DAT_0807afe8/afec: gP1LifePoints + 0x807?? jump)
#     0x7b00c, 0x7b010  (DAT_0807b00c/b010: gDuelCardCtxBase + check_equip fn-ptr)
#     0x7b028           (DAT_0807b028: check_equip_activation fn-ptr)
#     0x7b048, 0x7b04c, 0x7b050, 0x7b054 (DAT_0807b048..054: 4 pool words)
#     0x7b08c, 0x7b090, 0x7b094          (DAT_0807b08c..094: 3 pool words)
#
#   BLK4 (0x7b574..0x7b6b8):
#     0x7b5cc           (DAT_0807b5cc: gP1LifePoints)
#     0x7b610, 0x7b614  (DAT_0807b610/b614: gDuelCardCtxBase + gP1LifePoints)
#     0x7b644           (DAT_0807b644: gP1LifePoints)
#     0x7b67c           (DAT_0807b67c: PLAYER_BLOCK_STRIDE)
#
#   BLK6 (0x7b878..0x7b958):
#     0x7b8c8           (DAT_0807b8c8: some offset const)
#     0x7b8f8           (DAT_0807b8f8: gP1LifePoints)
#
#   BLK8 (0x7ba30..0x7bb30):
#     0x7ba70, 0x7ba74, 0x7ba78, 0x7ba7c, 0x7ba80 (ROM_INCBIN 0x7ba70/0x14: 5 pool words)
#     0x7ba98           (DAT_0807ba98: from .byte blob)
#     0x7bac8, 0x7bacc  (DAT_0807bac8/bacc: gEquipChainSlotRefs + EQUIP_PHASE_FRAME_OFF)
#     0x7bb0c, 0x7bb10, 0x7bb14, 0x7bb18, 0x7bb1c, 0x7bb20 (ROM_INCBIN 0x7bb0c/0x18: 6 pool words)
#
# NOTE: Only force-split word-aligned addresses (0x4 aligned).
# NOTE: DAT_0807bb0c and DAT_0807ba70 are ROM_INCBIN residuals that need clearListing+createDWord.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

POOL_ADDRS = [
    # BLK2 (0x7afb8..0x7b0c8) -- Lighten the Load dispatch sub-stubs
    0x0807afe8,  # gP1LifePoints (0x0201c4e0) -- from DAT_0807afe8 blob
    0x0807afec,  # some ptr (0x08680000? check ROM) -- DAT_0807afec blob
    0x0807b00c,  # gDuelCardCtxBase or similar -- DAT_0807b00c blob
    0x0807b010,  # fn-ptr -- DAT_0807b010 blob
    0x0807b028,  # fn-ptr -- DAT_0807b028 blob
    0x0807b048,  # gEquipChainSlotRefs (0x0201bb90) -- DAT_0807b048
    0x0807b04c,  # EQUIP_PHASE_FRAME_OFF (0x4a4) -- DAT_0807b04c
    0x0807b050,  # gP1LifePoints (0x0201c4e0) -- DAT_0807b050
    0x0807b054,  # LP_BANISHER_CTX_OFF (0x1d70) -- DAT_0807b054
    0x0807b08c,  # EQUIP_PHASE_FRAME_OFF (0x4a4) -- DAT_0807b08c
    0x0807b090,  # PLAYER_BLOCK_STRIDE (0x868) -- DAT_0807b090
    0x0807b094,  # gP1FieldArrayCBase (0x0201c600) -- DAT_0807b094

    # BLK4 (0x7b574..0x7b6b8) -- Hero Kid/Hyena dispatch sub-stubs
    0x0807b5cc,  # gP1LifePoints (0x0201c4e0) -- DAT_0807b5cc
    0x0807b610,  # gDuelCardCtxBase (0x0201e2a0) -- DAT_0807b610
    0x0807b614,  # gP1LifePoints (0x0201c4e0) -- DAT_0807b614
    0x0807b644,  # gP1LifePoints (0x0201c4e0) -- DAT_0807b644
    0x0807b67c,  # PLAYER_BLOCK_STRIDE (0x868) -- DAT_0807b67c

    # BLK6 (0x7b878..0x7b958) -- Rescue Cat dispatch sub-stubs
    0x0807b8c8,  # some CID/offset -- DAT_0807b8c8
    0x0807b8f8,  # gP1LifePoints (0x0201c4e0) -- DAT_0807b8f8

    # BLK8 (0x7ba30..0x7bb30) -- Gatling Dragon dispatch sub-stubs
    # ROM_INCBIN 0x7ba70/0x14 (20B = 5 DWORDs)
    0x0807ba70,  # DAT_0807ba70: gDuelPhaseFlags or similar pool word
    0x0807ba74,  # DAT_0807ba74: pool word
    0x0807ba78,  # DAT_0807ba78: fn-ptr check_equip_slot_eligible+1
    0x0807ba7c,  # DAT_0807ba7c: gP1LifePoints
    0x0807ba80,  # DAT_0807ba80: EQUIP_PHASE_FRAME_OFF
    # .byte blob at 0x7ba96 (2B align + 6B)
    0x0807ba98,  # DAT_0807ba98: some ptr (0x08050751 or check_equip fn+1)
    # pool words within gatling_dragon_dispatch_bad0
    0x0807bac8,  # DAT_0807bac8: gEquipChainSlotRefs (0x0201bb90)
    0x0807bacc,  # DAT_0807bacc: EQUIP_PHASE_FRAME_OFF (0x4a4)
    # ROM_INCBIN 0x7bb0c/0x18 (24B = 6 DWORDs)
    0x0807bb0c,  # DAT_0807bb0c[0]: pool word
    0x0807bb10,  # DAT_0807bb0c[1]: pool word
    0x0807bb14,  # DAT_0807bb0c[2]: pool word
    0x0807bb18,  # DAT_0807bb0c[3]: pool word
    0x0807bb1c,  # DAT_0807bb0c[4]: pool word
    0x0807bb20,  # DAT_0807bb0c[5]: pool word
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
    print("=== RefineF10Seg2PoolFix (DRY=%s) ===" % DRY)
    if DRY:
        print("[dry] would createDWord at %d pool addresses" % len(POOL_ADDRS))
        for a in POOL_ADDRS:
            print("[dry] 0x%08x" % a)
        return
    for a in POOL_ADDRS:
        _create_dword(a)
    print("=== PoolFix Done: %d addresses ===" % len(POOL_ADDRS))


main()
