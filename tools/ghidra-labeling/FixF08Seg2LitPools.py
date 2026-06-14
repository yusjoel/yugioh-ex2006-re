# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg2LitPools.py -- F08 Seg-2 Block2/Block3 literal pool DWORD fix
#
# After DisassembleF08Seg2Blocks.py, literal pool slots inside Block2 sub-fns
# were left as untyped data (.byte sequences). This script forces each to DWORD,
# sets labels, and adds equates where applicable.
#
# Block2 range: 0x08065e3c..0x080660d7
# Block3 range: 0x080662a4..0x0806630b (no extra lit pool fix needed)
#
# All 19 literal pool slots identified from asm grep + ROM byte read.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit
from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _check_val(slot_addr, expected):
    mem = currentProgram.getMemory()
    a = _addr(slot_addr)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
    except Exception as e:
        print("[FAIL] read 0x%08x: %s" % (slot_addr, e))
        return False
    if actual != (expected & 0xFFFFFFFF):
        print("[FAIL] 0x%08x: got 0x%08x expected 0x%08x" % (
            slot_addr, actual, expected & 0xFFFFFFFF))
        return False
    return True


def _fix_dword(slot_addr, label_name, eq_name=None, value=None):
    """Force DWORD type at slot_addr, set label, optionally add equate."""
    a = _addr(slot_addr)
    listing = currentProgram.getListing()
    et = currentProgram.getEquateTable()
    sym_tbl = currentProgram.getSymbolTable()

    if not _check_val(slot_addr, value if value is not None else 0):
        if value is not None:
            print("[SKIP] 0x%08x value mismatch" % slot_addr)
            return

    if DRY:
        eq_str = (' eq=%s' % eq_name) if eq_name else ''
        print("[dry] DWORD+LABEL 0x%08x -> %s%s" % (slot_addr, label_name, eq_str))
        return

    # Clear listing at this address (4 bytes)
    try:
        clearListing(a, a.add(3))
    except Exception as e:
        print("[warn] clearListing 0x%08x: %s" % (slot_addr, e))

    # Create DWORD data
    listing.createData(a, DWordDataType.dataType)

    # Set label
    existing = sym_tbl.getSymbols(a)
    names = [s.getName() for s in existing]
    if label_name not in names:
        sym_tbl.createLabel(a, label_name, SourceType.USER_DEFINED)

    # Add equate
    if eq_name is not None and value is not None:
        eq = et.getEquate(eq_name)
        if eq is None:
            eq = et.createEquate(eq_name, value & 0xFFFFFFFFFFFFFFFFL)
        eq.addReference(a, 0)

    eq_str = (' [%s]' % eq_name) if eq_name else ''
    print("[DW] 0x%08x -> %s%s" % (slot_addr, label_name, eq_str))


# ---------------------------------------------------------------------------
# Block2 literal pool slots
# (slot_addr, label_name, eq_name_or_None, value)
# ---------------------------------------------------------------------------
LIT_POOL = [
    # equip_state_stub_80 lit pool
    (0x08065e64, 'stub80_gDuelCardCtxBase', 'gDuelCardCtxBase', 0x0201e2a0),
    (0x08065e68, 'stub80_gP1LifePoints',    'gP1LifePoints',    0x0201c4e0),
    # equip_state_stub_7f lit pool
    (0x08065e94, 'stub7f_gP1LifePoints',    'gP1LifePoints',    0x0201c4e0),
    # equip_state_stub_7e lit pool (shared .byte block at 0x65ef0)
    (0x08065ef0, 'stub7e_gP1LifePoints',    'gP1LifePoints',    0x0201c4e0),
    (0x08065ef4, 'stub7e_lp_card_next_off', None,               0x00001daa),
    (0x08065ef8, 'stub7e_fn_ptr_check_act', None,               0x08065ce5),
    # equip_state_stub_7e continuation (lit pool at 0x65f50..)
    (0x08065f50, 'stub7e_player_stride',    'PLAYER_BLOCK_STRIDE', 0x00000868),
    (0x08065f54, 'stub7e_gDuelFieldSlots',  'gDuelFieldSlots',  0x0201c510),
    # equip_state_stub_78 lit pool
    (0x08065f7c, 'stub78_gDuelCardCtxBase', 'gDuelCardCtxBase', 0x0201e2a0),
    (0x08065f80, 'stub78_gP1LifePoints',    'gP1LifePoints',    0x0201c4e0),
    # equip_state_stub_78 cont
    (0x08065fb0, 'stub78_dm_cid',           'DARK_MAGICIAN_CID', 0x00000fc9),
    (0x08065fb4, 'stub78_cid_146e',         None,               0x0000146e),
    # equip_state_stub_77 lit pool
    (0x08065ff8, 'stub77_gP1LifePoints',    'gP1LifePoints',    0x0201c4e0),
    (0x08065ffc, 'stub77_dm_cid',           'DARK_MAGICIAN_CID', 0x00000fc9),
    (0x08066000, 'stub77_fn_ptr_check_act', None,               0x08065ce5),
    # equip_state_stub_6d lit pool
    (0x0806602c, 'stub6d_gP1LifePoints',    'gP1LifePoints',    0x0201c4e0),
    (0x08066030, 'stub6d_eligib_sprite_ctrl_off', 'ELIGIB_SPRITE_CTRL_OFF', 0x00001d68),
    # equip_state_stub_61 lit pool
    (0x08066088, 'stub61_cid_146e',         None,               0x0000146e),
    # equip_state_stub_60 lit pool
    (0x080660a0, 'stub60_cid_146e',         None,               0x0000146e),
]


def main():
    print("=== FixF08Seg2LitPools (DRY=%s) ===" % DRY)
    print("  %d literal pool slots to fix in Block2" % len(LIT_POOL))

    ok = 0
    fail = 0
    for entry in LIT_POOL:
        slot_addr, label_name = entry[0], entry[1]
        eq_name = entry[2] if len(entry) > 2 else None
        value = entry[3] if len(entry) > 3 else None
        if not _check_val(slot_addr, value):
            fail += 1
            continue
        _fix_dword(slot_addr, label_name, eq_name, value)
        ok += 1

    print("  Done: %d ok, %d fail" % (ok, fail))
    if fail > 0:
        print("  !!! %d FAILURES -- check slot addresses and values !!!" % fail)
    print("=== FixF08Seg2LitPools DONE ===")


main()
