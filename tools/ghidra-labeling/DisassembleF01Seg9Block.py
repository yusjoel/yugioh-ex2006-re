# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# DisassembleF01Seg9Block.py -- f01 Seg-9 R4 disasm
#   Block: 0x08027e50..0x08027ebc (0x6c bytes)
#   Function: tick_campaign_card_select_display_state
#   18 BL callers from file 02 range (0x08029478..0x0802aa92)
#   Literal pool: 0x08027eac..0x08027ebb (4 DWORDs)
#
# Strategy: clearListing + setTMode(THUMB) + DisassembleCommand + createFunction
# + guard literal pool (createDWord for 4 words at 0x08027eac..0x08027eb8)

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

BLOCK_LO      = 0x08027e50
BLOCK_HI_EXCL = 0x08027ebc  # exclusive (0x08027ebc is the PTR_ slot, outside code)
LP_START      = 0x08027eac
LP_END_EXCL   = 0x08027ebc  # 4 DWORDs: eac, eb0, eb4, eb8
FN_ADDR       = 0x08027e50
FN_NAME       = 'tick_campaign_card_select_display_state'


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


def _guard_literal_pool(pool_start_int, pool_end_excl_int):
    n = (pool_end_excl_int - pool_start_int) // 4
    print("[LP] guarding literal pool 0x%08x..0x%08x (%d DWORDs)" % (
        pool_start_int, pool_end_excl_int, n))
    for i in range(n):
        addr_int = pool_start_int + i * 4
        try:
            clearListing(_addr(addr_int), _addr(addr_int + 3))
            createDWord(_addr(addr_int))
        except Exception as e:
            print("[warn] createDWord @ 0x%08x: %s" % (addr_int, e))


def _create_fn(addr_int, name):
    a = _addr(addr_int)
    fn_mgr = currentProgram.getFunctionManager()
    sym_tbl = currentProgram.getSymbolTable()
    existing = fn_mgr.getFunctionAt(a)
    if existing is not None:
        if existing.getName() != name:
            existing.setName(name, SourceType.USER_DEFINED)
            print("[FN ] renamed @ 0x%08x -> %s" % (addr_int, name))
        else:
            print("[FN ] exists @ 0x%08x: %s" % (addr_int, name))
        return
    cmd = CreateFunctionCmd(name, a, None, SourceType.USER_DEFINED)
    if cmd.applyTo(currentProgram):
        print("[FN ] created %s @ 0x%08x" % (name, addr_int))
    else:
        print("[warn] createFunction @ 0x%08x: %s" % (addr_int, cmd.getStatusMsg()))
        sym_tbl.createLabel(a, name, SourceType.USER_DEFINED)
        print("[FN ] label fallback %s @ 0x%08x" % (name, addr_int))


def main():
    print("=== DisassembleF01Seg9Block (DRY=%s) ===" % DRY)
    print("Block: 0x%08x..0x%08x (0x%x bytes)" % (BLOCK_LO, BLOCK_HI_EXCL, BLOCK_HI_EXCL - BLOCK_LO))
    print("Function: %s @ 0x%08x" % (FN_NAME, FN_ADDR))

    if DRY:
        print("[dry] would: clearListing 0x%08x..0x%08x" % (BLOCK_LO, BLOCK_HI_EXCL - 1))
        print("[dry] would: setTMode=THUMB 0x%08x..0x%08x" % (BLOCK_LO, BLOCK_HI_EXCL - 1))
        print("[dry] would: DisassembleCommand @ 0x%08x" % FN_ADDR)
        print("[dry] would: guard literal pool 0x%08x..0x%08x (4 DWORDs)" % (LP_START, LP_END_EXCL))
        print("[dry] would: createFunction %s @ 0x%08x" % (FN_NAME, FN_ADDR))
        print("[done] DRY complete")
        return

    # 1. Clear entire block and set THUMB mode
    _clear_and_set_thumb(BLOCK_LO, BLOCK_HI_EXCL - 1)

    # 2. Disassemble from function entry (flow-based)
    lo = _addr(FN_ADDR)
    cmd = DisassembleCommand(lo, None, True)
    if cmd.applyTo(currentProgram):
        print("[ok ] DisassembleCommand @ 0x%08x" % FN_ADDR)
    else:
        print("[warn] DisassembleCommand @ 0x%08x: %s" % (FN_ADDR, cmd.getStatusMsg()))

    # 3. Guard literal pool (prevent flow disasm from treating pool as code)
    _guard_literal_pool(LP_START, LP_END_EXCL)

    # 4. Create function
    _create_fn(FN_ADDR, FN_NAME)

    print("=== DisassembleF01Seg9Block COMPLETE ===")


main()
