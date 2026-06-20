# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF09Seg10aPoolFix.py -- fix missing literal pool DWords in B3/B4/B5
# After initial disasm, some small-value pool words (offsets/CIDs) were not
# converted to DWord data by Ghidra, causing DAT_ label references in export.
#
# This script force_dword's all remaining pool words in B3/B4/B5 ranges
# that were missed in the initial DisassembleF09Seg10aBlocks.py run.
#
# Identified from build errors (ldr rN, DAT_0807XXXX):
#   B3: 0x79094 (PLAYER_BLOCK_STRIDE=0x868), 0x790a4 (0x17ae), 0x790c8 (0x17ad)
#   B4: 0x79184 (EQUIP_PHASE_FRAME_OFF=0x4a4), 0x79218 (0x1379?), 0x79220 (0x4a4)
#       0x79298 (0x17ae), 0x7929c (0x17ad), 0x792a0 (PLAYER_BLOCK_STRIDE=0x868)
#   B5: 0x7942c (0x4a4), 0x79474 (0x4a4), 0x794c8 (0x4a4)
#
# After force_dword, the disasm is NOT re-run (code instructions unchanged).
# The DWord data items will properly anchor the pool labels in the export.

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

# All pool words that need force_dword (missed in initial script)
POOL_WORDS = [
    # B3 missing pools
    (0x08079094, 0x00000868, 'PLAYER_BLOCK_STRIDE'),   # DAT_08079094
    (0x080790a4, 0x000017ae, '0x17ae'),                 # DAT_080790a4
    (0x080790c8, 0x000017ad, '0x17ad'),                 # DAT_080790c8

    # B4 missing pools
    (0x08079184, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF'),  # DAT_08079184
    (0x08079218, 0x00001379, '0x1379'),                 # DAT_08079218
    (0x08079220, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF'),  # DAT_08079220
    (0x08079298, 0x000017ae, '0x17ae'),                 # DAT_08079298
    (0x0807929c, 0x000017ad, '0x17ad'),                 # DAT_0807929c
    (0x080792a0, 0x00000868, 'PLAYER_BLOCK_STRIDE'),    # DAT_080792a0

    # B5 missing pools
    (0x0807942c, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF'),  # DAT_0807942c
    (0x08079474, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF'),  # DAT_08079474
    (0x080794c8, 0x000004a4, 'EQUIP_PHASE_FRAME_OFF'),  # DAT_080794c8
]

def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)

def _check_val(addr_int, expected):
    mem = currentProgram.getMemory()
    a = _addr(addr_int)
    try:
        actual = mem.getInt(a) & 0xFFFFFFFF
        return actual == (expected & 0xFFFFFFFF)
    except:
        return False

def _force_dword(addr_int, expected_val, name):
    if not _check_val(addr_int, expected_val):
        print("[FAIL] 0x%08x: ROM value mismatch for %s (expected 0x%08x)" % (addr_int, name, expected_val))
        return

    if DRY:
        print("[dry] force_dword 0x%08x = 0x%08x (%s)" % (addr_int, expected_val, name))
        return

    a = _addr(addr_int)
    a_end = _addr(addr_int + 3)
    listing = currentProgram.getListing()
    try:
        clearListing(a, a_end)
    except Exception as e:
        print("[warn] force_dword clearListing @ 0x%08x: %s" % (addr_int, e))
    try:
        listing.createData(a, ghidra.program.model.data.DWordDataType.dataType)
        print("[ok ] force_dword 0x%08x = 0x%08x (%s)" % (addr_int, expected_val, name))
    except Exception as e:
        print("[warn] force_dword createData @ 0x%08x: %s" % (addr_int, e))

def main():
    print("=== DisassembleF09Seg10aPoolFix (DRY=%s) ===" % DRY)
    print("  Pool words to force_dword: %d" % len(POOL_WORDS))

    for (addr_int, expected_val, name) in POOL_WORDS:
        _force_dword(addr_int, expected_val, name)

    print("\n=== DisassembleF09Seg10aPoolFix DONE ===")
    print("  %d pool words processed" % len(POOL_WORDS))
    print("  NOTE: Re-export Ghidra and rebuild after this fix.")

main()
