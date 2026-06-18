# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF08Seg10CidStateLiteralPools2.py
#   Additional literal pool DWORD fix for asm/08 Seg-10 cid_13ed state stubs.
#   These 8 addresses in 0x0806dc6c..0x0806ddb4 were missed in the first pass
#   (FixF08Seg10AndF09Seg1LiteralPools.py covered 0x0806de34+).
#
#   Without this, `ldr rN, DAT_0806dcXX` references in cid_13ed state stubs
#   have no corresponding .word label in the export => "invalid offset" build error.

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

# Literal pool DWORDs missing from cid_13ed state stubs (0x0806dc3c..0x0806dfff)
# All confirmed undefined in latest asm/08 export.
MISSING_POOLS = [
    0x0806dc6c,  # gDuelActDisplayCtx = 0x0806db11 (fn-ptr, THUMB+1)
    0x0806dcec,  # gP1LifePoints = 0x0201c4e0
    0x0806dcf0,  # LP_BANISHER_CTX_OFF = 0x1d70
    0x0806dcf4,  # PLAYER_BLOCK_STRIDE = 0x868
    # 0x0806dd1c already defined as DAT_ label in export (state_stub_7e literal pool)
    0x0806dd9c,  # gP1LifePoints = 0x0201c4e0
    0x0806dda0,  # LP_BANISHER_CTX_OFF = 0x1d70
    0x0806dda4,  # PLAYER_BLOCK_STRIDE = 0x868
    0x0806ddb4,  # gDuelActDisplayCtx = 0x0806db11 (fn-ptr, THUMB+1)
]

print("=== FixF08Seg10CidStateLiteralPools2.py DRY=%s ===" % DRY)
print("Processing %d literal pool addresses..." % len(MISSING_POOLS))

applied = 0
skipped = 0
for addr_val in MISSING_POOLS:
    addr = _addr(addr_val)
    if DRY:
        print("DRY: createDWord at 0x%08x" % addr_val)
        applied += 1
        continue
    try:
        clearListing(addr, toAddr(addr_val + 3))
        dt = DWordDataType()
        currentProgram.getListing().createData(addr, dt)
        applied += 1
        print("[OK] createDWord 0x%08x" % addr_val)
    except Exception as e:
        print("[WARN] 0x%08x createDWord failed: %s" % (addr_val, str(e)))
        skipped += 1

print("=== DONE: applied=%d skipped=%d ===" % (applied, skipped))
