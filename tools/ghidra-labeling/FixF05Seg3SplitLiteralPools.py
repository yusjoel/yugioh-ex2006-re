# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF05Seg3SplitLiteralPools.py -- Split merged byte blobs into individual DWORD entries
#
# After disasm, Ghidra keeps literal pool data as merged byte blobs.
# The ldr instructions reference sub-labels within the blob that are not
# separately exported. We need to split these blobs at each 4-byte boundary
# and define individual DWORD entries.
#
# Strategy: for each literal pool address, call:
#   clearListing(addr, addr+3) to remove existing data
#   createDWord(addr) to create a proper 4-byte data item
#   createLabel(addr, label) to name it
#   addEquateReference to equate it
#
# This forces the exporter to emit individual .word lines for each slot.

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.data import DWordDataType
from ghidra.program.flatapi import FlatProgramAPI

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# ---------------------------------------------------------------------------
# Literal pool slots to split into individual DWORDs
# (addr, value, label, const_name)
# ---------------------------------------------------------------------------
POOL_SLOTS = [
    # Block A -- check_card_is_toon_type
    (0x0804ae60, 0x000012a5, 'toon_type_beyd_cid',          'BLUE_EYES_TOON_DRAGON_CID'),
    (0x0804ae64, 0x00001123, 'toon_type_alligator_cid',      'TOON_ALLIGATOR_CID'),
    (0x0804ae68, 0x0000127f, 'toon_type_summoned_skull_cid', 'TOON_SUMMONED_SKULL_CID'),
    (0x0804ae80, 0x0000154a, 'toon_type_dmg_cid',            'TOON_DARK_MAGICIAN_GIRL_CID'),
    (0x0804ae84, 0x000012be, 'toon_type_world_cid',          'TOON_WORLD_CARD_ID'),
    (0x0804ae98, 0x00001566, 'toon_type_goblin_af_cid',      'TOON_GOBLIN_AF_CID'),
    # Block B -- check_card_is_guardian_type
    (0x0804afa8, 0x0000152e, 'guardian_type_sphinx_cid',       'GUARDIAN_SPHINX_CID'),
    (0x0804afac, 0x000011a7, 'guardian_type_throne_room_cid',  'GUARDIAN_OF_THRONE_ROOM_CID'),
    (0x0804afb0, 0x00000ffe, 'guardian_type_metal_cid',        'METAL_GUARDIAN_CID'),
    (0x0804afb4, 0x0000111c, 'guardian_type_gate_cid',         'GATE_GUARDIAN_CID'),
    (0x0804afc8, 0x00001266, 'guardian_type_skull_cid',        'SKULL_GUARDIAN_CID'),
    (0x0804afcc, 0x00001452, 'check_card_is_guardian_type_cid_1452', None),
    (0x0804afe8, 0x0000170b, 'guardian_type_angel_joan_cid',   'GUARDIAN_ANGEL_JOAN_CID'),
    (0x0804affc, 0x000018b0, 'guardian_type_lost_cid',         'LOST_GUARDIAN_CID'),
    # Block B -- check_card_is_dark_scorpion_type
    (0x0804b020, 0x00001686, 'dark_scorpion_meanae_cid',       'DARK_SCORPION_MEANAE_CID'),
    (0x0804b02c, 0x00001656, 'dark_scorpion_chick_cid',        'DARK_SCORPION_CHICK_CID'),
    (0x0804b040, 0x0000169e, 'dark_scorpion_mustering_cid',    'MUSTERING_DARK_SCORPIONS_CID'),
    # Block C -- check_card_is_batteryman_type
    (0x0804b264, 0x000018c3, 'batteryman_type_aa_cid',         'BATTERYMAN_AA_CID'),
    # Block C -- check_card_is_dark_world_range_type
    (0x0804b280, 0xffffe69f, 'dark_world_range_base_neg',      None),
    (0x0804b284, 0x0804b288, 'dark_world_range_table_ptr',     None),
]


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def main():
    print("=== FixF05Seg3SplitLiteralPools (DRY=%s) ===" % DRY)
    listing = currentProgram.getListing()
    et      = currentProgram.getEquateTable()
    sym_tbl = currentProgram.getSymbolTable()
    n = 0

    for addr_int, value, label, cname in POOL_SLOTS:
        a = _addr(addr_int)
        a_end = _addr(addr_int + 3)

        if DRY:
            print("[dry] 0x%08x clearListing+createDWord+label=%s cname=%s" % (addr_int, label, cname))
            n += 1; continue

        # 1. Clear existing data at this 4-byte range
        try:
            clearListing(a, a_end)
        except Exception as e:
            print("[warn] clearListing @ 0x%08x: %s" % (addr_int, e))

        # 2. Create a DWORD data item
        try:
            listing.createData(a, DWordDataType.dataType)
        except Exception as e:
            print("[warn] createDWord @ 0x%08x: %s" % (addr_int, e))

        # 3. Verify value
        d = getDataAt(a)
        if d is not None and d.getLength() == 4:
            try:
                dv = d.getValue()
                iv = (int(dv.getValue()) & 0xffffffff) if hasattr(dv, 'getValue') else (int(dv) & 0xffffffff)
                if iv != (value & 0xffffffff):
                    print("[MISMATCH] 0x%08x: got=0x%x want=0x%x" % (addr_int, iv, value))
            except Exception:
                pass

        # 4. Create label
        try:
            sym_tbl.createLabel(a, label, SourceType.USER_DEFINED)
        except Exception as e:
            print("[warn] createLabel @ 0x%08x %s: %s" % (addr_int, label, e))

        # 5. Apply equate
        if cname is not None:
            try:
                eq = et.getEquate(cname)
                if eq is None:
                    eq = et.createEquate(cname, value & 0xffffffff)
                eq.addReference(a, 0)
            except Exception as e:
                print("[warn] equate %s @ 0x%08x: %s" % (cname, addr_int, e))

        print("[ok ] 0x%08x -> %s (%s)" % (addr_int, label, cname)); n += 1

    print("[done] n=%d (DRY=%s)" % (n, DRY))


main()
