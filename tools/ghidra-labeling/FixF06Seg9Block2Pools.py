# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF06Seg9Block2Pools.py -- fix literal pool labels in Block2 0x0805a0f8..0x0805a1db
#
# After DisassembleF06Seg9Blocks.py, some literal pool slots in Block2 sub-functions
# lack labels (exported as raw .byte sequences). This script forces DWORDs + labels
# so GAS can resolve the ldr Rn, DAT_xxx references.
#
# Literal pool addresses inside Block2 (found via THUMB ldr Rn,[pc,#off] scan):
#   0x0805a110 = 0x0201b290 (gDuelPhaseFlags)
#   0x0805a114 = 0x000004ac (EQUIP_ACTIVATION_STEP_OFF)
#   0x0805a12c = 0x0201b290
#   0x0805a130 = 0x000004ac
#   0x0805a144 = 0x080905e9 (set_equip_activation_state_by_mode_alt+1)
#   gap 0x0805a186..0x0805a187 = 0x0000 (alignment pad)
#   0x0805a188 = 0x0201c4e0 (gP1LifePoints)
#   0x0805a18c = 0x00001d68 (ELIGIB_SPRITE_CTRL_OFF)
#   0x0805a190 = 0x00001d6c (ELIGIB_ANIM_STATE_OFF)
#   0x0805a194 = 0x0201b290
#   0x0805a198 = 0x000004ac
#   0x0805a1ac = 0x0201b290
#   0x0805a1b0 = 0x000004ac
#   0x0805a1c4 = 0x0201b290
#   0x0805a1c8 = 0x000004ac
#
# Strategy:
#   - For the gap 0x0805a186..0x0805a187 (2 zero bytes): clearListing + create HWord data
#   - For each DWORD pool slot: clearListing(4B) + createData(DWord) + createLabel(DAT_xxx)
#   This gives GAS the labels it needs to resolve ldr Rn, DAT_xxx.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _create_dword_labeled(addr_int):
    """Force DWord data + DAT_xxxxxxxx label at addr_int."""
    a = _addr(addr_int)
    hi4 = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    sm = currentProgram.getSymbolTable()
    dt = ghidra.program.model.data.DWordDataType.dataType
    label = "DAT_%08x" % addr_int

    if DRY:
        print("[dry] createDWord+label %s @ 0x%08x" % (label, addr_int))
        return

    try:
        clearListing(a, hi4)
    except Exception:
        pass
    try:
        listing.createData(a, dt)
        print("[DW ] createDWord @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createDWord 0x%08x: %s" % (addr_int, e))

    syms = sm.getSymbols(a)
    names = [s.getName() for s in syms]
    if label not in names:
        sm.createLabel(a, label, SourceType.USER_DEFINED)
        print("[LBL] %s @ 0x%08x" % (label, addr_int))
    else:
        print("[LBL] already exists: %s @ 0x%08x" % (label, addr_int))


def _create_hword_pad(addr_int):
    """Force HWord data at addr_int (alignment pad)."""
    a = _addr(addr_int)
    hi2 = _addr(addr_int + 1)
    listing = currentProgram.getListing()
    dt = ghidra.program.model.data.WordDataType.dataType

    if DRY:
        print("[dry] createHWord (pad) @ 0x%08x" % addr_int)
        return

    try:
        clearListing(a, hi2)
    except Exception:
        pass
    try:
        listing.createData(a, dt)
        print("[HW ] createHWord(pad) @ 0x%08x" % addr_int)
    except Exception as e:
        print("[warn] createHWord 0x%08x: %s" % (addr_int, e))


# All literal pool DWORD addresses in Block2
POOL_DWORDS = [
    0x0805a110,  # gDuelPhaseFlags = 0x0201b290
    0x0805a114,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    0x0805a12c,  # gDuelPhaseFlags = 0x0201b290
    0x0805a130,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    0x0805a144,  # set_equip_activation_state_by_mode_alt+1 = 0x080905e9
    0x0805a188,  # gP1LifePoints = 0x0201c4e0
    0x0805a18c,  # ELIGIB_SPRITE_CTRL_OFF = 0x00001d68
    0x0805a190,  # ELIGIB_ANIM_STATE_OFF = 0x00001d6c
    0x0805a194,  # gDuelPhaseFlags = 0x0201b290
    0x0805a198,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    0x0805a1ac,  # gDuelPhaseFlags = 0x0201b290
    0x0805a1b0,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
    0x0805a1c4,  # gDuelPhaseFlags = 0x0201b290
    0x0805a1c8,  # EQUIP_ACTIVATION_STEP_OFF = 0x000004ac
]

# 2-byte alignment pad at 0x0805a186..0x0805a187
PAD_HWORD = 0x0805a186


def main():
    print("=== FixF06Seg9Block2Pools (DRY=%s) ===" % DRY)

    print("\n--- Alignment pad ---")
    _create_hword_pad(PAD_HWORD)

    print("\n--- Literal pool DWORDs (%d) ---" % len(POOL_DWORDS))
    for addr in POOL_DWORDS:
        _create_dword_labeled(addr)

    print("\n=== FixF06Seg9Block2Pools DONE ===")


main()
