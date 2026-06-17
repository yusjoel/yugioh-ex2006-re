# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg8cLiteralPools.py -- fix literal pool .byte sequences in Seg-8c stubs
#
# Problem: after DisassembleF08Seg8cBlocks.py, some literal pool words are exported
# as .byte sequences because Ghidra did not create DWord data at those addresses.
# GAS ldr-to-.byte causes "invalid offset, value too big (0xFFFFFFFC)" build errors.
#
# Fix: createDWord at each offending literal pool address within the disassembled
# blocks (Block1: 0x806c3d8..0x806c41b, Block2: 0x806c440..0x806c6d7).
#
# Literal pool addresses identified from build errors:
#   Block1: 0x806c414 (gDuelPhaseFlags = 0x0201b290)
#   Block2 stubs:
#     0x806c4d8 (PLAYER_BLOCK_STRIDE=0x868)
#     0x806c4dc (gDuelFieldSlots=0x0201c510)
#     0x806c4e0 (0x001f001f)
#     0x806c4e4 (gEquipZoneCountTable=0x0201e1c8)
#     0x806c520 (EQUIP_PHASE_FRAME_OFF=0x4a4)
#     0x806c524 (gP1LifePoints=0x0201c4e0)
#     0x806c528 (P1LP_BLOCK2_OFF_1CE8=0x1ce8)
#     0x806c5e8 (gP1LifePoints=0x0201c4e0)
#     0x806c5ec (EQUIP_PHASE_FRAME_OFF=0x4a4)
#     0x806c5f0 (PLAYER_BLOCK_STRIDE=0x868)
#     0x806c638 (0x0201b748)
#     0x806c68c (gDuelPhaseFlags=0x0201b290)
#     0x806c690 (EQUIP_PHASE_FRAME_OFF=0x4a4)
#     0x806c694 (gP1LifePoints=0x0201c4e0)
#     0x806c698 (P1LP_BLOCK2_OFF_1CE8=0x1ce8)
#     0x806c6d4 (gEquipZoneCountTable=0x0201e1c8)
#
# backup: ghidra/Yu-Gi-Oh WCT 2006.rep.bak-20260618_pre-F08Seg8c

from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


LITERAL_POOL_ADDRS = [
    # Block1
    0x0806c414,
    # Block2 - stub c4e8 pool
    0x0806c4d8,
    0x0806c4dc,
    0x0806c4e0,
    0x0806c4e4,
    # Block2 - stub c4e8 pool (at c520)
    0x0806c520,
    0x0806c524,
    0x0806c528,
    # Block2 - stub c52c pool
    0x0806c5e8,
    0x0806c5ec,
    0x0806c5f0,
    # Block2 - stub c5f8 pool
    0x0806c638,
    # Block2 - stub c63c/c65a shared pool
    0x0806c68c,
    0x0806c690,
    # Block2 - stub c69c pool
    0x0806c694,
    0x0806c698,
    # Block2 - stub c69c pool end
    0x0806c6d4,
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _create_dword(addr):
    a = _addr(addr)
    if DRY:
        print("[dry] DWORD 0x%08x" % addr)
        return
    listing = currentProgram.getListing()
    existing = listing.getCodeUnitAt(a)
    if existing is not None:
        try:
            clearListing(a, a)
        except Exception as e:
            print("[warn] clearListing for dword at 0x%08x: %s" % (addr, e))
    try:
        listing.createData(a, DWordDataType.dataType)
        print("[DWORD] created at 0x%08x" % addr)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr, e))


def main():
    print("=== FixF08Seg8cLiteralPools (DRY=%s) ===" % DRY)
    print("  %d literal pool addresses to createDWord" % len(LITERAL_POOL_ADDRS))
    for addr in LITERAL_POOL_ADDRS:
        _create_dword(addr)
    print("=== FixF08Seg8cLiteralPools DONE ===")


main()
