# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RepairF08Seg3DataLabels.py -- Restore data labels lost during Seg-6 Ghidra operations
#
# During the Seg-6 re-export, several DWORD data labels in F08 Seg-3 (~0x08066900..0x08066b00)
# lost their Ghidra data definitions and became ROM_INCBIN in the export.
# This script restores them as DWORD data units with USER_DEFINED labels.
#
# All values verified from ROM roms/2343.gba and from HEAD:asm/08_equip_oam_neodaed.s

from ghidra.program.model.data import DWordDataType
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# (addr, label, rom_value_hex, comment_ascii)
# rom_value is little-endian 4-byte value read from ROM at addr - 0x08000000
DATA_SLOTS = [
    (0x08066908, 'DAT_08066908', 0x000017f5, 'CID literal pool for dispatch_equip_effect_type_stub_80'),
    (0x08066960, 'DAT_08066960', 0x000017da, 'ARMED_DRAGON_LV5_CID'),
    (0x08066964, 'DAT_08066964', 0x0000165a, 'A_DEAL_WITH_DARK_RULER_CID'),
    (0x08066968, 'DAT_08066968', 0x00001529, 'GREAT_DEZARD_CID'),
    (0x0806696c, 'DAT_0806696c', 0x000010e4, 'CID 0x10e4 Elegant Egotist'),
    (0x08066988, 'DAT_08066988', 0x000017af, None),
    (0x0806698c, 'DAT_0806698c', 0x0000167d, None),
    (0x0806699c, 'DAT_0806699c', 0x000017c9, None),
    (0x080669d4, 'DAT_080669d4', 0x000019b1, None),
    (0x080669e8, 'DAT_080669e8', 0x000019b5, None),
    (0x08066a48, 'DAT_08066a48', 0x7f280000, 'filter mask for lsls r0,r0,#0x13 cmp in dispatch_equip_effect_type_stub_7e'),
    (0x08066a4c, 'DAT_08066a4c', 0x0201e2a0, 'gDuelCardCtxBase'),
    (0x08066a50, 'DAT_08066a50', 0x0201b290, 'gDuelPhaseFlags'),
    (0x08066a54, 'DAT_08066a54', 0x000004a4, 'EQUIP_PHASE_FRAME_OFF'),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_value(slot_addr, expected_val):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] read 0x%08x: %s" % (slot_addr, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] 0x%08x: rom=0x%08x expected=0x%08x" % (slot_addr, actual, expected_val & 0xFFFFFFFF))
        return False
    return True


def main():
    print("=== RepairF08Seg3DataLabels (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    sym_tbl = currentProgram.getSymbolTable()
    dword_dt = DWordDataType.dataType

    ok = 0
    fail = 0
    for slot_addr, label, expected_val, comment in DATA_SLOTS:
        a = _addr(slot_addr)

        if not _check_value(slot_addr, expected_val):
            fail += 1
            continue

        if DRY:
            print("[dry] RESTORE 0x%08x %s" % (slot_addr, label))
            ok += 1
            continue

        # 1. Clear existing code/data at this address
        listing.clearCodeUnits(a, a, False)

        # 2. Create DWORD data unit
        try:
            listing.createData(a, dword_dt)
            print("[DATA] created DWORD @ 0x%08x" % slot_addr)
        except Exception as e:
            print("[DATA WARN] createData @ 0x%08x: %s" % (slot_addr, e))

        # 3. Create USER label
        existing = list(sym_tbl.getSymbols(a))
        names = [s.getName() for s in existing]
        if label not in names:
            sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)

        # Make label primary
        for s in list(sym_tbl.getSymbols(a)):
            if s.getName() == label:
                s.setPrimary()
                break

        # 4. EOL comment if any
        if comment:
            cu = listing.getCodeUnitAt(a)
            if cu is not None:
                bad = any(ord(ch) > 127 for ch in comment)
                if not bad:
                    cu.setComment(CodeUnit.EOL_COMMENT, comment)

        print("[RESTORE] 0x%08x %s = 0x%08x" % (slot_addr, label, expected_val))
        ok += 1

    print("=== Done: %d ok, %d fail ===" % (ok, fail))


main()
