# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF12Seg4Remediate.py
# Remediation script: 3 EQ slots missed by RefineF12Seg4Slots.py
#
# 1. DWORD_08097110 (0x09e47560): already DWORD_COERCE'd, needs equate+label
#    => EQUIP_ACTIVATION_HANDLER_TABLE / equip_act_tbl_7110
# 2. DAT_080972d0   (0x00001cf4): P2LP_BLOCK2_OFF_1CF4 (ewram.inc REUSE)
#    => p2lp_blk2_72d0
# 3. DAT_08097664   (0x0000177a): EARTHBOUND_INVITATION_CID (card_info.inc REUSE)
#    => earthbound_inv_7664

import sys
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.symbol import SourceType, RefType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
    elif _a and _a[0].lower() in ("run", "real", "0", "false"):
        DRY = False
except Exception:
    pass

MISSED_EQ = [
    (0x08097110, 0x09e47560, 'EQUIP_ACTIVATION_HANDLER_TABLE', 'equip_act_tbl_7110',
     'get_equip_handler_table_entry_param: coerced DWORD HANDLER_TABLE_BASE=0x09e47560'),
    (0x080972d0, 0x00001cf4, 'P2LP_BLOCK2_OFF_1CF4', 'p2lp_blk2_72d0',
     'check_equip_effect_zone_preconditions: [+0x1cf4] P2 LP block2 second occurrence'),
    (0x08097664, 0x0000177a, 'EARTHBOUND_INVITATION_CID', 'earthbound_inv_7664',
     'refresh_slot_activation_display_if_changed: check_value_in_slot_chain CID=0x177a'),
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check(slot_addr, expected_val, label):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] _check 0x%08x (%s): read error %s" % (slot_addr, label, e))
        return False
    if actual != (expected_val & 0xFFFFFFFF):
        print("[FAIL] _check 0x%08x (%s): got 0x%08x expected 0x%08x" % (
            slot_addr, label, actual, expected_val & 0xFFFFFFFF))
        return False
    return True

def _apply_eq(slot_addr, eq_val, eq_name, slot_label, eol):
    if not _check(slot_addr, eq_val, eq_name):
        print("[SKIP] value mismatch at 0x%08x" % slot_addr)
        return
    if DRY:
        print("[dry] EQ 0x%08x  %s=0x%08x  slot=%s" % (slot_addr, eq_name, eq_val, slot_label))
        return

    a = _addr(slot_addr)
    eq_tbl = currentProgram.getEquateTable()
    sym_tbl = currentProgram.getSymbolTable()

    eq = eq_tbl.getEquate(eq_name)
    if eq is None:
        eq = eq_tbl.createEquate(eq_name, eq_val & 0xFFFFFFFF)
    eq.addReference(a, 0)

    sym_tbl.createLabel(a, slot_label, SourceType.USER_DEFINED)

    if eol:
        cu = currentProgram.getListing().getCodeUnitAt(a)
        if cu is not None:
            cu.setComment(CodeUnit.EOL_COMMENT, eol)

    print("[EQ ] 0x%08x  %s  -> %s" % (slot_addr, eq_name, slot_label))

print("=== RefineF12Seg4Remediate (DRY=%s) ===" % DRY)
ok = 0
for (slot_addr, eq_val, eq_name, slot_label, eol) in MISSED_EQ:
    _apply_eq(slot_addr, eq_val, eq_name, slot_label, eol)
    ok += 1

print("=== DONE: %d slots ===" % ok)
