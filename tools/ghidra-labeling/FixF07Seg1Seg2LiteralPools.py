# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF07Seg1Seg2LiteralPools.py -- Force createDWord on literal pool DWORD slots
#   that were exported as raw .byte blocks, causing "invalid offset too big" assembler errors.
#
# Problem: After R4 disasm, Ghidra exports literal pool entries as ".byte <raw>" blocks
#   when the DWORD slots inside aren't split as individual 4B data items.
#   Fix: clearListing + createDWord on each 4B slot to force proper ".word <label>" export.
#
# Seg-1 literal pools (from DisassembleF07Seg1Blocks.py output):
#   Block A fn1: DAT_0805c430 (0x0201c4e0=gP1LP) + DAT_0805c434 (0x0201c510=gDuelFieldSlots)
#   Block A fn2: DAT_0805c460 (0x0201c4e0=gP1LP) + DAT_0805c464 (0x00000868=PLAYER_BLOCK_STRIDE)
#   Block B fn:  DAT_0805c624 (0x0201c4e0=gP1LP) + DAT_0805c628 (0x00000868=PLAYER_BLOCK_STRIDE)
#   Block C fn:  DAT_0805cda8 (0x0201c4e0=gP1LP) + DAT_0805cdac (0x00000868=PLAYER_BLOCK_STRIDE)
#
# Seg-2 literal pools (from DisassembleF07Seg2Blocks.py output):
#   Block 2 fn2 (check_equip_zone_eligible_appropriate):
#     DAT_0805de44 (0x0201c4e0=gP1LP) + DAT_0805de48 (0x00001cf4=FIELD_STATE_OFF)
#   Block 2 fn4 (check_equip_zone_eligible_minor_goblin_official):
#     DAT_0805dea0 (0x0201c4e0=gP1LP) + DAT_0805dea4 (0x00000868=PLAYER_BLOCK_STRIDE) +
#     DAT_0805dea8 (0x00000bb8 = 3000 decimal LP threshold)
#
# After createDWord, the slots will be exported as:
#   DAT_<addr>:
#       .word 0x<value>
# instead of the current ".byte ..." blob.

from ghidra.program.model.symbol import SourceType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _fix_dword(addr_int, expected_val, comment):
    """clearListing at addr_int, createDWord, verify value."""
    a = _addr(addr_int)
    if DRY:
        print("[dry] createDWord @ 0x%08x (expect=0x%08x) -- %s" % (addr_int, expected_val, comment))
        return
    try:
        clearListing(a, _addr(addr_int + 3))
        createDWord(a)
    except Exception as e:
        print("[WARN] clearListing/createDWord @ 0x%08x: %s" % (addr_int, e))
        return
    d = getDataAt(a)
    if d is None or d.getLength() != 4:
        print("[FAIL] no 4B data @ 0x%08x after createDWord" % addr_int)
        return
    try:
        dv = d.getValue()
        iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
    except Exception:
        iv = None
    if iv is not None and iv != (expected_val & 0xffffffff):
        print("[WARN] value mismatch @ 0x%08x: got=0x%x want=0x%x" % (addr_int, iv, expected_val))
    else:
        print("[ok ] createDWord @ 0x%08x = 0x%08x (%s)" % (addr_int, expected_val, comment))


POOLS = [
    # Seg-1 Block A fn1 literal pool (after bx lr @ 0x0805c43a, before LAB_0805c438)
    # 8 bytes at 0x5c430: gP1LP + gDuelFieldSlots
    (0x0805c430, 0x0201c4e0, 'gP1LifePoints'),
    (0x0805c434, 0x0201c510, 'gDuelFieldSlots'),

    # Seg-1 Block A fn2 literal pool (after bx lr @ 0x0805c45c)
    # 8 bytes at 0x5c45e: gP1LP + PLAYER_BLOCK_STRIDE
    # Note: ldr r2 @ 0x5c43c => pc+0x1c = 0x5c460 and ldr r0 @ 0x5c44c => pc+0x14 = 0x5c464
    (0x0805c460, 0x0201c4e0, 'gP1LifePoints'),
    (0x0805c464, 0x00000868, 'PLAYER_BLOCK_STRIDE'),

    # Seg-1 Block B fn literal pool (after b LAB_0805c62e @ 0x0805c620)
    # 10 bytes at 0x5c622: gP1LP + PLAYER_BLOCK_STRIDE
    # ldr r2 @ 0x5c608 => pc+0x18 = 0x5c624; ldr r1 @ 0x5c610 => pc+0x14 = 0x5c628
    (0x0805c624, 0x0201c4e0, 'gP1LifePoints'),
    (0x0805c628, 0x00000868, 'PLAYER_BLOCK_STRIDE'),

    # Seg-1 Block C fn literal pool (after bx lr @ 0x0805cdaa)
    # ldr r2 @ 0x5cd88 => pc+0x1c = 0x5cda8; ldr r1 @ 0x5cd94 => pc+0x14 = 0x5cdac
    (0x0805cda8, 0x0201c4e0, 'gP1LifePoints'),
    (0x0805cdac, 0x00000868, 'PLAYER_BLOCK_STRIDE'),

    # Seg-2 Block 2 fn2 (check_equip_zone_eligible_appropriate) literal pool
    # (after bx lr @ 0x0805de4e; literal pool in the .byte block at 0x5de3e)
    # ldr r0 @ 0x5de32 => pc+0xe = 0x5de44; ldr r1 @ 0x5de34 => pc+0x10 = 0x5de48
    (0x0805de44, 0x0201c4e0, 'gP1LifePoints'),
    (0x0805de48, 0x00001cf4, 'FIELD_STATE_OFF'),

    # Seg-2 Block 2 fn4 (check_equip_zone_eligible_minor_goblin_official) literal pool
    # (after bx lr @ 0x0805de9c)
    # ldr r2 @ 0x5de7e => pc+0x20 = 0x5dea0; ldr r1 @ 0x5de8a => pc+0x16 = 0x5dea4; ldr r0 @ 0x5de92 => pc+0x12 = 0x5dea8
    (0x0805dea0, 0x0201c4e0, 'gP1LifePoints'),
    (0x0805dea4, 0x00000868, 'PLAYER_BLOCK_STRIDE'),
    (0x0805dea8, 0x00000bb8, '3000_lp_threshold'),
]


def main():
    print("=== FixF07Seg1Seg2LiteralPools (DRY=%s) ===" % DRY)
    print("Fixing %d literal pool DWORD slots" % len(POOLS))
    for addr_int, expected_val, comment in POOLS:
        _fix_dword(addr_int, expected_val, comment)
    print("=== Done ===")


main()
