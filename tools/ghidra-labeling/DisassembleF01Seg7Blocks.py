# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF01Seg7Blocks.py -- f01 Seg-7 R4 disasm
#   Block2: 0x080211b4..0x08021277 (2 entry points; literal pool 0x08021260..0x08021277)
#   Block3: 0x0802134c..0x08022e2b (51 unique entry points)
#   Block4: 0x08022eb8..0x0802385d (15 unique entry points)
#
# Strategy: clearListing + setTMode + per-stub DisassembleCommand + createFunction
# (same pattern as DisassembleF01Seg6Blocks.py)

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
    """Disassemble single entry via flow (no size limit per stub)."""
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
        # Fallback: label only
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


def process_block(name, lo_int, hi_int, entries, literal_pool_start=None, literal_pool_end=None):
    """Process one R4 disasm block."""
    print("\n=== %s [0x%08x..0x%08x) %d entries ===" % (name, lo_int, hi_int, len(entries)))
    if DRY:
        print("[dry] would: clearListing + setTMode + %d DisassembleCommand + createFunction" % len(entries))
        return

    # 1. Clear and set THUMB for entire block
    _clear_and_set_thumb(lo_int, hi_int - 1)

    # 2. Per-entry disasm (do NOT use whole-range flow -- only disasm first stub)
    for entry in entries:
        _disasm_stub(entry)

    # 3. Create functions for each unique entry point
    for entry in entries:
        _create_fn(entry)

    # 4. Guard literal pool AFTER disasm (if specified)
    if literal_pool_start and literal_pool_end:
        _guard_literal_pool(literal_pool_start, literal_pool_end)

    print("[%s] DONE" % name)


# ---------------------------------------------------------------------------
# Block2: 0x080211b4..0x08021277 (0xc4 bytes = 196 B)
# Literal pool: 0x08021260..0x08021277 (do not decode as code)
# 2 entry points: step handlers for PTR_DAT_08021150 dispatch
# ---------------------------------------------------------------------------
BLOCK2_LO = 0x080211b4
BLOCK2_HI = 0x08021278   # exclusive
BLOCK2_LP_START = 0x08021260
BLOCK2_LP_END   = 0x08021278

BLOCK2_ENTRIES = [
    0x080211b4,  # 17 raw refs from PTR_DAT_08021150
    0x080211fc,  # 8 raw refs from PTR_DAT_08021150
]

# ---------------------------------------------------------------------------
# Block3: 0x0802134c..0x08022e2c (0x1ae0 bytes = 6880 B)
# 51 unique entry points (52 table entries, 0x08022d22 appears at [31] and [32])
# ---------------------------------------------------------------------------
BLOCK3_LO = 0x0802134c
BLOCK3_HI = 0x08022e2c   # exclusive

BLOCK3_ENTRIES = [
    0x0802134c, 0x080213e0, 0x08021474, 0x08021508,
    0x08021674, 0x080216f4, 0x08021780, 0x0802180c,
    0x08021898, 0x08021924, 0x080219b0, 0x08021a3c,
    0x08021ac8, 0x08021b54, 0x08021be0, 0x08021c6c,
    0x08021cf8, 0x08021d84, 0x08021e10, 0x08021e9c,
    0x08021f30, 0x08021fbc, 0x08022048, 0x080220d4,
    0x08022160, 0x080221ec, 0x080222b4, 0x0802237c,
    0x08022440, 0x080224ec, 0x0802256c, 0x08022688,
    0x08022730, 0x080227a8, 0x08022874, 0x08022894,
    0x08022920, 0x08022940, 0x08022960, 0x08022980,
    0x0802299c, 0x080229b8, 0x08022a50, 0x08022b0c,
    0x08022bb4, 0x08022bd4, 0x08022bf4, 0x08022c14,
    0x08022c34, 0x08022c84, 0x08022d22,
]

# ---------------------------------------------------------------------------
# Block4: 0x08022eb8..0x0802385e (0x9a6 bytes = 2470 B)
# 15 unique entry points inside block4
# Note: table entries[14..19] -> 0x0802385e = fetch_duel_next_state_overflow_exit (outside block4)
# Note: table entry[20] = 0x08023844 (last inside block4)
# ---------------------------------------------------------------------------
BLOCK4_LO = 0x08022eb8
BLOCK4_HI = 0x0802385e   # exclusive (named fn boundary)

BLOCK4_ENTRIES = [
    0x08022eb8, 0x08022fdc, 0x08023010, 0x08023154,
    0x080233dc, 0x08023410, 0x08023558, 0x0802358c,
    0x080235c0, 0x08023614, 0x0802361c, 0x0802366c,
    0x08023774, 0x08023810, 0x08023844,
]


def main():
    print("=== DisassembleF01Seg7Blocks (DRY=%s) ===" % DRY)

    process_block("Block2", BLOCK2_LO, BLOCK2_HI, BLOCK2_ENTRIES,
                  literal_pool_start=BLOCK2_LP_START, literal_pool_end=BLOCK2_LP_END)

    process_block("Block3", BLOCK3_LO, BLOCK3_HI, BLOCK3_ENTRIES)

    process_block("Block4", BLOCK4_LO, BLOCK4_HI, BLOCK4_ENTRIES)

    print("\n=== DisassembleF01Seg7Blocks COMPLETE ===")


main()
