# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF01Seg8Blocks.py -- f01 Seg-8 R4 disasm
#   Block1: 0x0802497c..0x080249f3 (0x78 bytes, 15 unique entry points)
#     Dispatched from build_field_slot_bitmask via bx r12 jump table
#     PTR_LAB_08024910 entries [5..26] -> 15 unique THUMB handlers
#   Block2: 0x080258f0..0x08025b1f (0x230 bytes, 6 unique entry points)
#     Dispatched from render_card_stats_to_line_buf via jump table at 0x080258d8
#     6 font-select card stat render variants
#
# Strategy: clearListing + setTMode + per-stub DisassembleCommand + createFunction
# (same pattern as DisassembleF01Seg7Blocks.py)
#
# NOTES:
#   * Block1 is THUMB code dispatched via raw address (bx r12 in existing THUMB context)
#   * Block2 has literal pools with EWRAM_BASE/GSETTINGS/font ptrs embedded as .byte blocks
#     -> Must use _guard_literal_pool on these ranges to force DWORD export

from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.app.cmd.function import CreateFunctionCmd
from ghidra.program.model.address import AddressSet
from ghidra.program.model.symbol import SourceType
from java.math import BigInteger

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"): DRY = True
except Exception:
    pass


def _addr(v):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v)


def _clear_and_set_thumb(lo_int, hi_int):
    lo = _addr(lo_int)
    hi = _addr(hi_int)
    try:
        clearListing(lo, hi)
        print("[ok ] clearListing(0x%08x..0x%08x)" % (lo_int, hi_int))
    except Exception as e:
        print("[warn] clearListing 0x%08x..0x%08x: %s" % (lo_int, hi_int, e))
    ctx = currentProgram.getProgramContext()
    tmode = ctx.getRegister("TMode")
    if tmode is not None:
        ctx.setValue(tmode, lo, hi, BigInteger.ONE)
        print("[ok ] setTMode=THUMB 0x%08x..0x%08x" % (lo_int, hi_int))
    else:
        print("[warn] TMode register not found")


def _disasm_stub(addr_int):
    """Disassemble single entry via flow."""
    lo = _addr(addr_int)
    cmd = DisassembleCommand(lo, None, True)
    if not cmd.applyTo(currentProgram):
        print("[warn] disasm 0x%08x: %s" % (addr_int, cmd.getStatusMsg()))
        return False
    return True


def _create_fn(addr_int, name=None):
    a = _addr(addr_int)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        print("[FN ] exists @ 0x%08x: %s" % (addr_int, existing.getName()))
        return
    fn_name = name if name else ("FUN_%08x" % addr_int)
    cmd = CreateFunctionCmd(fn_name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (fn_name, addr_int))
    else:
        print("[warn] createFunction @ 0x%08x: %s" % (addr_int, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, fn_name, SourceType.USER_DEFINED)
        print("[FN ] label fallback %s @ 0x%08x" % (fn_name, addr_int))


def _guard_literal_pool(pool_start_int, pool_end_exclusive_int):
    """Create DWORDs in literal pool range to prevent mis-decode."""
    n = (pool_end_exclusive_int - pool_start_int) // 4
    print("[LP] guarding literal pool 0x%08x..0x%08x (%d DWORDs)" % (
        pool_start_int, pool_end_exclusive_int, n))
    for i in range(n):
        addr_int = pool_start_int + i * 4
        try:
            clearListing(_addr(addr_int), _addr(addr_int + 3))
            createDWord(_addr(addr_int))
        except Exception as e:
            print("[warn] createDWord @ 0x%08x: %s" % (addr_int, e))


def process_block(name, lo_int, hi_int, entries, literal_pools=None):
    """Process one R4 disasm block."""
    print("\n=== %s [0x%08x..0x%08x) %d entries ===" % (name, lo_int, hi_int, len(entries)))
    if DRY:
        print("[dry] would: clearListing + setTMode + %d DisassembleCommand + createFunction" % len(entries))
        if literal_pools:
            print("[dry] would: guard %d literal pool regions" % len(literal_pools))
        return

    # 1. Clear and set THUMB for entire block
    _clear_and_set_thumb(lo_int, hi_int - 1)

    # 2. Per-entry disasm
    for entry in entries:
        _disasm_stub(entry)

    # 3. Create functions
    for entry in entries:
        _create_fn(entry)

    # 4. Guard literal pools AFTER disasm
    if literal_pools:
        for pool_start, pool_end in literal_pools:
            _guard_literal_pool(pool_start, pool_end)

    print("[%s] DONE" % name)


# ---------------------------------------------------------------------------
# Block1: 0x0802497c..0x080249f3 (0x78 bytes)
# 15 unique entry points from PTR_LAB_08024910 table entries [5..26]
# Each handler: sets r1=0/1 (slot-active flag) and returns via shared epilogue
# Dispatch via .hword 0x4687 (bx r12) at 0x08024908 (already in THUMB mode)
# No literal pools in block1 (stubs are too short, use shared epilogue)
# ---------------------------------------------------------------------------
BLOCK1_LO = 0x0802497c
BLOCK1_HI = 0x080249f4   # exclusive

BLOCK1_ENTRIES = [
    0x0802497c,  # entry [5]
    0x08024982,  # entry [6,7]
    0x08024988,  # entry [8,9]
    0x0802498c,  # entry [10]
    0x08024992,  # entry [11,12]
    0x08024998,  # entry [13,14]
    0x0802499c,  # entry [15]
    0x080249a2,  # entry [16,17]
    0x080249a8,  # entry [18,19]
    0x080249ac,  # entry [20,21]
    0x080249b8,  # entry [22]
    0x080249c4,  # entry [23]
    0x080249d0,  # entry [24]
    0x080249dc,  # entry [25]
    0x080249e8,  # entry [26]
]

# ---------------------------------------------------------------------------
# Block2: 0x080258f0..0x08025b1f (0x230 bytes)
# 6 unique entry points from DWORD_080258d8 table entries [0..5]
# Sorted entry order: [1]=0x080258f0, [2]=0x0802594c, [0]=0x080259a8,
#                     [5]=0x08025a08,  [4]=0x08025a68,  [3]=0x08025ac8
# Each handler: selects font ptr from gSettings+0x6c2c lang bits[2:0]
#               and calls render_card_stat_with_number_alt
#
# LITERAL POOLS: Each stub has 3-4 DWORDs (EWRAM_BASE, GSETTINGS_OFFSET,
#   font5_base, font5_off) embedded inline as .byte blocks or small incbins.
#   These must be guarded as DWORDs or GAS will fail to resolve ldr labels.
# ---------------------------------------------------------------------------
BLOCK2_LO = 0x080258f0
BLOCK2_HI = 0x08025b20   # exclusive

BLOCK2_ENTRIES = [
    0x080258f0,  # table[1]
    0x0802594c,  # table[2]
    0x080259a8,  # table[0]
    0x08025a08,  # table[5]
    0x08025a68,  # table[4]
    0x08025ac8,  # table[3]
]

# Literal pool ranges that need guarding (each contains 4 DWORDs):
# stub [1] @ 0x080258f0: pool at 0x0802591c (EWRAM/GSETTINGS/font5_base/off)
# stub [2] @ 0x0802594c: pool at 0x08025978
# stub [0] @ 0x080259a8: pool at 0x080259d0
# stub [5] @ 0x08025a08: pool at 0x08025a30
# stub [4] @ 0x08025a68: pool at 0x08025a90
# stub [3] @ 0x08025ac8: pool at 0x08025af0
BLOCK2_LITERAL_POOLS = [
    (0x0802591c, 0x0802592c),  # 4 DWORDs: EWRAM_BASE/GSETTINGS/font5_base/off
    (0x08025978, 0x08025988),  # 4 DWORDs
    (0x080259d0, 0x080259e0),  # 4 DWORDs
    (0x08025a30, 0x08025a40),  # 4 DWORDs
    (0x08025a90, 0x08025aa0),  # 4 DWORDs
    (0x08025af0, 0x08025b00),  # 4 DWORDs
]


def main():
    print("=== DisassembleF01Seg8Blocks (DRY=%s) ===" % DRY)

    process_block("Block1", BLOCK1_LO, BLOCK1_HI, BLOCK1_ENTRIES)

    process_block("Block2", BLOCK2_LO, BLOCK2_HI, BLOCK2_ENTRIES,
                  literal_pools=BLOCK2_LITERAL_POOLS)

    print("\n=== DisassembleF01Seg8Blocks COMPLETE ===")


main()
