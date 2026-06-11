# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF03Seg4bFixLiteralPools.py -- file 03 Seg-4b literal pool fix
#   After R4 disasm, PC-relative ldr targets within 0x08039350..0x0803a41d
#   may be exported as .byte sequences without explicit labels.
#   This script calls createDWord at each PC-relative ldr target address
#   to force Ghidra to emit them as labeled .word in the GAS export.
#   All 52 addresses from missing-label analysis.

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

# All PC-relative ldr targets inside 0x08039350..0x0803a41d that are
# missing explicit DAT_ labels in the export
MISSING_POOL_ADDRS = [
    0x08039528,
    0x080397e8,
    0x0803995c,
    0x08039a08,
    0x08039a0c,
    0x08039afc,
    0x08039b18,
    0x08039b1c,
    0x08039b20,
    0x08039c78,
    0x08039c7c,
    0x08039ce8,
    0x08039cec,
    0x08039d0c,
    0x08039d28,
    0x08039d50,
    0x08039d80,
    0x08039d9c,
    0x08039da0,
    0x08039db0,
    0x08039de8,
    0x08039e04,
    0x08039e1c,
    0x08039e58,
    0x08039e7c,
    0x08039e94,
    0x08039ecc,
    0x08039ee8,
    0x08039f24,
    0x08039f70,
    0x08039fb0,
    0x0803a030,
    0x0803a040,
    0x0803a04c,
    0x0803a080,
    0x0803a0c0,
    0x0803a0c4,
    0x0803a0f8,
    0x0803a1f0,
    0x0803a224,
    0x0803a2ec,
    0x0803a2f0,
    0x0803a2f4,
    0x0803a2f8,
    0x0803a34c,
    0x0803a350,
    0x0803a354,
    0x0803a358,
    0x0803a36c,
    0x0803a388,
    0x0803a408,
    0x0803a40c,
]

print("=== RefineF03Seg4bFixLiteralPools.py DRY=%s ===" % DRY)
print("Processing %d missing pool addresses..." % len(MISSING_POOL_ADDRS))

applied = 0
skipped = 0
for addr_val in MISSING_POOL_ADDRS:
    addr = _addr(addr_val)
    if DRY:
        print("DRY: createDWord at 0x%08x" % addr_val)
        applied += 1
        continue
    try:
        # clearListing at just this address to remove any conflicting code unit
        clearListing(addr, toAddr(addr_val + 3))
        # Create a DWORD data type at this address
        dt = DWordDataType()
        currentProgram.getListing().createData(addr, dt)
        applied += 1
    except Exception as e:
        print("WARN: 0x%08x createDWord failed: %s" % (addr_val, str(e)))
        skipped += 1

print("=== DONE: applied=%d skipped=%d ===" % (applied, skipped))
