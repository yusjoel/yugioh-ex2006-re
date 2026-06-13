# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# FixF06Seg6Block2LiteralPools.py
# Create DWORDs at all literal pool slots within block2 sub-fns (0x57d4c..0x57ea7)
# These pools were cleared by DisassembleF06Seg6Blocks.py (clearListing range3) but
# not re-created as DWORDs, causing the assembler "invalid offset" errors when
# code references ldr rN, DAT_xxx to these pool slots.
#
# Pool layout (from asm export analysis):
#   sub-fn A pool:  0x57dbc..0x57dcf (5 DWORDs, 2-byte zero-pad at 0x57dba)
#   sub-fn A pool2: 0x57dec..0x57df7 (3 DWORDs, 2-byte zero-pad at 0x57dea)
#   sub-fn B pool:  0x57e30..0x57e3f (4 DWORDs, 2-byte zero-pad at 0x57e2e)
#   sub-fn C pool:  0x57e74..0x57e87 (5 DWORDs, no pad needed)
#   sub-fn C pool2: 0x57e98..0x57e9f (2 DWORDs, 2-byte zero-pad at 0x57e96)

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception: pass

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

listing = currentProgram.getListing()
dt = ghidra.program.model.data.DWordDataType.dataType

# Exact DWORD-aligned pool addresses (excludes zero-pad alignment bytes)
BLOCK2_POOL_DWORDS = [
    # sub-fn A pool @ 0x57dbc..0x57dcf (referenced by ldr instructions in dispatch_ep_state0)
    0x08057dbc,
    0x08057dc0,
    0x08057dc4,
    0x08057dc8,
    0x08057dcc,
    # sub-fn A pool2 @ 0x57dec..0x57df7 (referenced by ldr after LAB_08057dd0)
    0x08057dec,
    0x08057df0,
    0x08057df4,
    # sub-fn B pool @ 0x57e30..0x57e3f (referenced by ldr in dispatch_ep_state2)
    0x08057e30,
    0x08057e34,
    0x08057e38,
    0x08057e3c,
    # sub-fn C pool @ 0x57e74..0x57e87 (referenced by ldr in dispatch_ep_state1)
    0x08057e74,
    0x08057e78,
    0x08057e7c,
    0x08057e80,
    0x08057e84,
    # sub-fn C pool2 @ 0x57e98..0x57e9f (referenced by ldr in LAB_08057e88 block)
    0x08057e98,
    0x08057e9c,
]

print("=== FixF06Seg6Block2LiteralPools (DRY=%s) ===" % DRY)
print("  %d pool DWORDs to create" % len(BLOCK2_POOL_DWORDS))
ok_count = 0
fail_count = 0

for addr_int in BLOCK2_POOL_DWORDS:
    a = _addr(addr_int)
    end_a = _addr(addr_int + 3)
    existing = listing.getDataAt(a)
    if DRY:
        print("  [dry] 0x%08x: existing=%s -> clearListing+createDWord" % (addr_int, existing))
        ok_count += 1
        continue
    try:
        clearListing(a, end_a)
        listing.createData(a, dt)
        print("  [ok] createDWord @ 0x%08x" % addr_int)
        ok_count += 1
    except Exception as e:
        print("  [warn] 0x%08x: %s" % (addr_int, e))
        fail_count += 1

print("=== Done: ok=%d fail=%d ===" % (ok_count, fail_count))
