# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF06Seg6Range1Pool.py
# Fix literal pool DWORDs for check_equip_slot_active_for_player_and_group:
#   Correct: 0x080576a4 (PLAYER_BLOCK_STRIDE=0x868) and 0x080576a8 (gDuelFieldSlots=0x0201c510)
#   Note: DisassembleF06Seg6Blocks.py erroneously created DWORDs at 0x576a2/0x576a6 (off by 2)

from ghidra.program.model.symbol import SourceType
from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception: pass

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

listing = currentProgram.getListing()
dt = ghidra.program.model.data.DWordDataType.dataType
sm = currentProgram.getSymbolTable()
et = currentProgram.getEquateTable()

POOLS = [
    (0x080576a4, 0x00000868, 'PLAYER_BLOCK_STRIDE', 'tick_equip_chain_player_stride'),
    (0x080576a8, 0x0201c510, 'gDuelFieldSlots',    'tick_equip_chain_slot_base'),
]

print("=== FixF06Seg6Range1Pool (DRY=%s) ===" % DRY)
for addr_int, value, cname, label in POOLS:
    a = _addr(addr_int)
    existing = listing.getDataAt(a)
    print("  @ 0x%08x: existing=%s" % (addr_int, existing))
    if DRY:
        print("  [dry] createDWord + equate %s + label %s" % (cname, label))
        continue
    # Ensure DWORD -- clear full 4-byte range first (remove conflicting data/instrs)
    end_a = _addr(addr_int + 3)
    if existing is None or not existing.getDataType().equals(dt):
        try:
            clearListing(a, end_a)
            listing.createData(a, dt)
            print("  [ok] createDWord @ 0x%08x" % addr_int)
        except Exception as e:
            print("  [warn] createDWord @ 0x%08x: %s" % (addr_int, e))
    else:
        print("  [ok] already DWORD @ 0x%08x" % addr_int)
    # Apply equate
    eq = et.getEquate(cname)
    if eq is None:
        eq = et.createEquate(cname, value)
    eq.addReference(a, 0)
    print("  [ok] equate %s=0x%x @ 0x%08x" % (cname, value, addr_int))
    # Apply label
    createLabel(a, label, True, SourceType.USER_DEFINED)
    print("  [ok] label %s @ 0x%08x" % (label, addr_int))

print("=== Done ===")
