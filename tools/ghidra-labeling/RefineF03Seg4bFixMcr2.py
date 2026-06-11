# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg4bFixMcr2.py -- file 03 Seg-4b mcr2 literal pool fix
#   Four literal pool addresses inside disassembled stubs got decoded as
#   ARM mcr2 instructions instead of DWORD literals. Clear and create DWORD.
#   Addresses: 0x080397b8, 0x08039850, 0x080398dc, 0x08039a24
#   All contain value 0xfffffe0c = SCORE_DELTA_NEG_500.

from ghidra.program.model.data import DWordDataType

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

def _addr(val):
    return toAddr(val)

MCR2_ADDRS = [
    0x080397b8,
    0x08039850,
    0x080398dc,
    0x08039a24,
]

print("=== RefineF03Seg4bFixMcr2.py DRY=%s ===" % DRY)

applied = 0
skipped = 0
for addr_val in MCR2_ADDRS:
    addr = _addr(addr_val)
    if DRY:
        print("DRY: clearListing + createDWord at 0x%08x" % addr_val)
        applied += 1
        continue
    try:
        # Clear the ARM-decoded instruction
        clearListing(addr, toAddr(addr_val + 3))
        # Create a DWORD data type
        dt = DWordDataType()
        currentProgram.getListing().createData(addr, dt)
        print("Applied: 0x%08x -> DWORD" % addr_val)
        applied += 1
    except Exception as e:
        print("WARN: 0x%08x failed: %s" % (addr_val, str(e)))
        skipped += 1

print("=== DONE: applied=%d skipped=%d ===" % (applied, skipped))
