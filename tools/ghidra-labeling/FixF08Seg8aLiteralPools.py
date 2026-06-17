# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg8aLiteralPools.py -- Fix literal pool DWORD entries in F08 Seg-8a disasm blocks
#
# Problem: After clearListing + flow disasm, Ghidra exported many literal pool entries
# as .byte blobs without individual DWORD labels. GAS assembler then fails with
# "invalid offset, value too big (0xFFFFFFFC)" for ldr rN, DAT_XXXXXXXX references.
#
# Fix: Create DWORD data items at all 21 missing literal pool addresses.
# The DAT_XXXXXXXX label will be auto-applied by Ghidra's naming scheme, or we create
# explicit labels matching what was exported.
#
# All 21 entries are within Block1 (0x6ae18..0x6b073) or Block2 (0x6b098..0x6b233).
#
# Values verified from ROM roms/2343.gba.

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (addr, expected_value, label_name)
# label_name = None -> use Ghidra auto-generated DAT_ label
LITERAL_POOL_DWORDS = [
    # Block1: 0x0806ae18..0x0806b073
    # Sub-pool at 0x0806ae82 (2 pad bytes + 3 DWORDS):
    (0x0806ae84, 0x000004a4, 'DAT_0806ae84'),  # EQUIP_PHASE_FRAME_OFF
    (0x0806ae88, 0x0201c4e0, 'DAT_0806ae88'),  # gP1LifePoints
    (0x0806ae8c, 0x00001ce8, 'DAT_0806ae8c'),  # P1LP_BLOCK2_OFF_1CE8
    # Sub-pool at 0x0806af34 (already labeled, but +4 and +8 not labeled):
    (0x0806af38, 0x000004a4, 'DAT_0806af38'),  # EQUIP_PHASE_FRAME_OFF
    (0x0806af3c, 0x00000868, 'DAT_0806af3c'),  # PLAYER_BLOCK_STRIDE
    # Sub-pool at 0x0806af7e (2 pad bytes + DWORD at +2):
    (0x0806af80, 0x0201b748, 'DAT_0806af80'),  # gDuelEquipCtx or similar global @0x0201b748
    # Sub-pool at 0x0806af9e (2 pad bytes + 3 DWORDS):
    (0x0806afa0, 0x000004a4, 'DAT_0806afa0'),  # EQUIP_PHASE_FRAME_OFF
    (0x0806afa4, 0x00000868, 'DAT_0806afa4'),  # PLAYER_BLOCK_STRIDE
    (0x0806afa8, 0x0201c740, 'DAT_0806afa8'),  # gP1SlotSetCodeArray
    # Sub-pool at 0x0806afe0 (already labeled DAT_0806afe0, but +4 and +8 not labeled):
    (0x0806afe4, 0x0201c4e0, 'DAT_0806afe4'),  # gP1LifePoints
    (0x0806afe8, 0x00001ce8, 'DAT_0806afe8'),  # P1LP_BLOCK2_OFF_1CE8
    # ROM_INCBIN 0x6b02a/0x4a: single DWORD at 0x0806b02c
    (0x0806b02c, 0x0201e1c8, 'DAT_0806b02c'),  # gEquipZoneCountTable
    # Block2: 0x0806b098..0x0806b233
    # Sub-pool at 0x0806b0ea (2 pad + 2 DWORDS):
    (0x0806b0ec, 0x000014dd, 'DAT_0806b0ec'),  # CID 0x14dd
    (0x0806b0f0, 0x0000136a, 'DAT_0806b0f0'),  # CID 0x136a
    # Sub-pool at 0x0806b10a (2 pad + 3 DWORDS):
    (0x0806b10c, 0x000015b6, 'DAT_0806b10c'),  # CID 0x15b6
    (0x0806b110, 0x0000194f, 'DAT_0806b110'),  # CID 0x194f
    (0x0806b114, 0x0201e4f0, 'DAT_0806b114'),  # global @0x0201e4f0
    # Sub-pool at 0x0806b156 (2 pad + 2 DWORDS):
    (0x0806b158, 0x000015b6, 'DAT_0806b158'),  # CID 0x15b6
    (0x0806b15c, 0x0000136a, 'DAT_0806b15c'),  # CID 0x136a
    # Sub-pool at 0x0806b16e (2 pad + DWORD):
    (0x0806b170, 0x0000152f, 'DAT_0806b170'),  # CID 0x152f
    # Sub-pool at 0x0806b18c (part of DAT_0806b188 blob; +4 not labeled):
    (0x0806b18c, 0x00001612, 'DAT_0806b18c'),  # CID 0x1612
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_value(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] read 0x%08x: %s" % (addr_int, e))
        return False
    if actual != (expected & 0xFFFFFFFF):
        print("[FAIL] 0x%08x: got 0x%08x expected 0x%08x" % (addr_int, actual, expected & 0xFFFFFFFF))
        return False
    return True


def main():
    print("=== FixF08Seg8aLiteralPools (DRY=%s) ===" % DRY)
    print("  Creating DWORD data items at %d literal pool addresses" % len(LITERAL_POOL_DWORDS))

    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    ok = 0
    fail = 0

    for addr_int, expected_val, label in LITERAL_POOL_DWORDS:
        a = _addr(addr_int)

        # Verify value
        if not _check_value(addr_int, expected_val):
            fail += 1
            continue

        if DRY:
            print("[dry] DWORD 0x%08x = 0x%08x label=%s" % (addr_int, expected_val, label))
            ok += 1
            continue

        # Clear existing data/code at this address (4 bytes)
        try:
            clearListing(a, a.add(3))
        except Exception as e:
            print("[warn] clearListing @ 0x%08x: %s" % (addr_int, e))

        # Create DWORD data type
        try:
            listing.createData(a, DWordDataType.dataType)
            print("[DW ] 0x%08x = 0x%08x" % (addr_int, expected_val))
        except Exception as e:
            print("[FAIL] createData @ 0x%08x: %s" % (addr_int, e))
            fail += 1
            continue

        # Create label if specified
        if label:
            existing = list(sym_tbl.getSymbols(a))
            existing_names = [s.getName() for s in existing]
            if label not in existing_names:
                try:
                    sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
                    print("[LBL] 0x%08x -> %s" % (addr_int, label))
                except Exception as e:
                    print("[warn] createLabel @ 0x%08x (%s): %s" % (addr_int, label, e))

        ok += 1

    print("=== FixF08Seg8aLiteralPools DONE: ok=%d fail=%d ===" % (ok, fail))


main()
